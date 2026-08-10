import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  parseExecutionCollectionSource,
  parseExecutionDetailSource,
  validateExecutionId,
  type ExecutionInspectorDataState,
  type ExecutionInspectorView as ExecutionInspectorViewModel,
} from "./contract";
import {
  EXECUTION_DETAIL_DESCRIPTOR,
  EXECUTION_INSPECTOR_DESCRIPTOR,
  EXECUTION_INSPECTOR_DESCRIPTORS,
} from "./descriptors";
import { ExecutionDetailView } from "./execution-detail-page";
import {
  buildExecutionDetailPath,
  buildExecutionsPath,
  EXECUTION_LIVE_SOURCE_CLASSIFICATION,
  getQualifiedExecutionSource,
  loadExecutionInspectorRequest,
} from "./execution-client";
import { ExecutionInspectorView } from "./execution-inspector-page";
import {
  createExecutionInspectorPoller,
  executionInspectorRequestKey,
  EXECUTION_INSPECTOR_POLL_MS,
  EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS,
  INITIAL_EXECUTION_INSPECTOR_STATE,
} from "./use-execution-inspector";

function run(overrides: Record<string, unknown> = {}) {
  return {
    id: 4,
    task_id: "t_alpha01",
    profile: "worker-profile",
    status: "done",
    outcome: "completed",
    started_at: 1_700_000_006,
    ended_at: 1_700_000_007,
    summary: "token=private-summary C:\\private\\result.txt",
    error: "private raw run error",
    metadata: { command: "rm -rf private", provider: "private-provider" },
    claim_lock: "private-claim",
    worker_pid: 991,
    ...overrides,
  };
}

function taskWire(overrides: Record<string, unknown> = {}) {
  return {
    task: {
      id: "t_alpha01",
      title: "Inspect source run",
      body: "Private task body",
      status: "done",
      workspace_path: "C:\\private\\workspace",
      result: "private task result",
      diagnostics: [{
        run_id: 4,
        kind: "repeated_failures",
        severity: "error",
        count: 2,
        first_seen_at: 1_700_000_006,
        last_seen_at: 1_700_000_009,
        title: "private diagnostic title",
        detail: "private diagnostic detail",
        actions: [{ command: "private diagnostic command" }],
      }],
    },
    runs: [run()],
    events: [
      {
        id: 11,
        task_id: "t_alpha01",
        run_id: 4,
        kind: "run_completed",
        created_at: 1_700_000_008,
        payload: { token: "private-event-token", command: "private-command" },
      },
      {
        id: 10,
        task_id: "t_alpha01",
        run_id: 4,
        kind: "run_started",
        created_at: 1_700_000_005,
      },
      {
        id: 12,
        task_id: "t_alpha01",
        run_id: null,
        kind: "task_wide_event",
        created_at: 1_700_000_009,
      },
      {
        id: 13,
        task_id: "t_alpha01",
        run_id: 5,
        kind: "another_run_event",
        created_at: 1_700_000_010,
      },
    ],
    comments: [{ body: "private comment" }],
    attachments: [{
      id: 21,
      task_id: "t_alpha01",
      filename: "result-summary.json",
      content_type: "application/json",
      size: 128,
      created_at: 1_700_000_010,
      stored_path: "/home/private/artifact",
    }],
    ...overrides,
  };
}

function collectionView(raw = taskWire()): ExecutionInspectorViewModel {
  return {
    kind: "executions",
    collection: parseExecutionCollectionSource(raw, "alpha-board", "t_alpha01", 1_700_000_100_000)!,
  };
}

function detailView(raw = taskWire()): ExecutionInspectorViewModel {
  return {
    kind: "detail",
    execution: parseExecutionDetailSource(raw, "alpha-board", "t_alpha01", "4", 1_700_000_100_000)!,
  };
}

function state(
  snapshot: ExecutionInspectorViewModel | null,
  phase: ExecutionInspectorDataState["phase"] = "ready",
): ExecutionInspectorDataState {
  return { phase, snapshot, lastSuccessAt: 1_700_000_000_000, refreshing: false };
}

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("safe source-qualified execution projection", () => {
  it("preserves exact composite identity, source facts, profile, freshness, and retention limits", () => {
    const parsed = parseExecutionCollectionSource(taskWire({
      runs: [
        run({ id: 3, status: "running", outcome: null, started_at: 1_700_000_001, ended_at: null }),
        run({ id: 4 }),
      ],
    }), "alpha-board", "t_alpha01", 1_700_000_100_000);

    expect(parsed?.executions.map((execution) => execution.sourceLocalExecutionId)).toEqual([4, 3]);
    expect(parsed?.executions[0]).toMatchObject({
      source: {
        sourceType: "hermes-kanban-task-run",
        sourceSystem: "hermes-kanban",
        sourceAuthority: "pepper-controlled-product-evidence",
        futureAuthority: "P15/P17-controlled-worker-adapter",
      },
      boardSlug: "alpha-board",
      taskId: "t_alpha01",
      sourceProfile: "worker-profile",
      observedAt: 1_700_000_100_000,
      freshnessBasis: "adapter-fetch-time",
      originalSourceStatus: "done",
      originalSourceOutcome: "completed",
      taskTitle: "Source task title withheld by the execution projection",
    });
    expect(parsed?.source.retentionLimitation).toContain("Human Git authority is preserved");
  });

  it("does not infer status or outcome from recency, task state, errors, summaries, or event text", () => {
    const parsed = parseExecutionCollectionSource(taskWire({
      task: { id: "t_alpha01", title: "Inspect source run", status: "running" },
      runs: [run({
        status: "source_custom_state",
        outcome: null,
        ended_at: 1_700_000_007,
        summary: "completed successfully",
        error: "failed words",
      })],
    }), "alpha-board", "t_alpha01", 1_700_000_100_000);
    expect(parsed?.executions[0]).toMatchObject({
      originalSourceStatus: "source_custom_state",
      originalSourceOutcome: null,
    });
  });

  it("drops raw summaries, errors, metadata, event payloads, task bodies, paths, claims, and PIDs", () => {
    const parsed = parseExecutionDetailSource(taskWire(), "alpha-board", "t_alpha01", "4", 1_700_000_100_000);
    const serialized = JSON.stringify(parsed);
    for (const forbidden of [
      "private-summary",
      "private raw run error",
      "rm -rf",
      "private-provider",
      "private-claim",
      "991",
      "private-event-token",
      "private-command",
      "Private task body",
      "private task result",
      "private\\workspace",
      "/home/private",
      "private comment",
      "private diagnostic title",
      "private diagnostic detail",
      "private diagnostic command",
    ]) expect(serialized).not.toContain(forbidden);
  });

  it("projects only explicitly linked retained events in source order without payloads", () => {
    const parsed = parseExecutionDetailSource(taskWire(), "alpha-board", "t_alpha01", "4", 1_700_000_100_000);
    expect(parsed?.linkedEvents.phase).toBe("ready");
    expect(parsed?.linkedEvents.items.map((event) => [event.sourceLocalEventId, event.sourceEventKind]))
      .toEqual([[10, "run_started"], [11, "run_completed"]]);
    expect(parsed?.linkedEvents.items[0]).toMatchObject({
      sourceLocalExecutionId: 4,
      sourceProfile: "worker-profile",
      observedAt: 1_700_000_100_000,
    });
  });

  it("projects bounded result, artifact, and diagnostic evidence while excluding executable failure detail", () => {
    const parsed = parseExecutionDetailSource(taskWire(), "alpha-board", "t_alpha01", "4", 1_700_000_100_000);
    expect(parsed).toMatchObject({
      safeActionCategory: "Hermes Kanban task attempt",
      executableContent: "excluded",
      resultSummary: { phase: "ready" },
      failureSummary: { phase: "ready" },
      artifactReferences: { phase: "ready" },
      diagnostics: { phase: "ready" },
    });
    expect(parsed?.validationSummaries).toHaveLength(2);
    expect(parsed?.resultSummary.items[0].safeText).toBe(
      "Hermes recorded a source-local result summary; raw result detail is excluded.",
    );
    expect(parsed?.failureSummary.items[0].safeText).toBe(
      "Hermes recorded a source-local failure summary; raw failure detail is excluded.",
    );
    expect(parsed?.artifactReferences.items[0]).toMatchObject({
      sourceLocalArtifactId: 21,
      displayFilename: "result-summary.json",
      mediaType: "application/json",
      sizeBytes: 128,
      attribution: "task-level-not-run-attributed",
    });
    expect(parsed?.diagnostics.items[0]).toMatchObject({
      sourceLocalDiagnosticId: "repeated_failures",
      severity: "error",
      count: 2,
      safeMessage: "Hermes reported repeated source-run failures.",
    });
  });

  it("models empty and unavailable optional evidence sections independently", () => {
    const empty = parseExecutionDetailSource(taskWire({
      task: { id: "t_alpha01", title: "Inspect source run", diagnostics: [] },
      runs: [run({ summary: null, error: null })],
      attachments: [],
    }), "alpha-board", "t_alpha01", "4", 1);
    const unavailable = parseExecutionDetailSource(taskWire({
      task: { id: "t_alpha01", title: "Inspect source run", diagnostics: "unsafe" },
      runs: [run({ summary: { raw: "unsafe" }, error: { raw: "unsafe" } })],
      attachments: "unsafe",
    }), "alpha-board", "t_alpha01", "4", 1);
    expect([
      empty?.resultSummary.phase,
      empty?.failureSummary.phase,
      empty?.artifactReferences.phase,
      empty?.diagnostics.phase,
    ]).toEqual(["empty", "empty", "empty", "empty"]);
    expect([
      unavailable?.resultSummary.phase,
      unavailable?.failureSummary.phase,
      unavailable?.artifactReferences.phase,
      unavailable?.diagnostics.phase,
    ]).toEqual(["unavailable", "unavailable", "unavailable", "unavailable"]);
  });

  it("treats omitted optional evidence as unavailable rather than confirmed empty", () => {
    const raw = taskWire({
      task: { id: "t_alpha01", title: "Inspect source run" },
      runs: [run({ summary: undefined, error: undefined })],
    });
    const parsed = parseExecutionDetailSource(raw, "alpha-board", "t_alpha01", "4", 1);
    expect([
      parsed?.resultSummary.phase,
      parsed?.failureSummary.phase,
      parsed?.diagnostics.phase,
    ]).toEqual(["unavailable", "unavailable", "unavailable"]);
  });

  it("never retains adversarial narrative content", () => {
    const parsed = parseExecutionDetailSource(taskWire({
      task: {
        id: "t_alpha01",
        title: "AWS_SECRET_ACCESS_KEY=private cat /srv/secrets",
        diagnostics: [],
      },
      runs: [run({
        summary: '{"command":"cat /srv/secrets"} AWS_SECRET_ACCESS_KEY=private \\\\server\\share\\secret',
        error: "-----BEGIN PRIVATE KEY-----\nprivate\n-----END PRIVATE KEY-----",
      })],
    }), "alpha-board", "t_alpha01", "4", 1);
    const serialized = JSON.stringify(parsed);
    for (const forbidden of ["cat /srv/secrets", "private", "server", "share", "BEGIN PRIVATE KEY"]) {
      expect(serialized).not.toContain(forbidden);
    }
  });

  it("keeps empty and unsafe linked-event sections explicit", () => {
    const empty = parseExecutionDetailSource(taskWire({ events: [] }), "alpha-board", "t_alpha01", "4", 1_700_000_100_000);
    const unavailable = parseExecutionDetailSource(taskWire({ events: "unsafe" }), "alpha-board", "t_alpha01", "4", 1_700_000_100_000);
    const duplicate = parseExecutionDetailSource(taskWire({
      events: [
        { id: 11, task_id: "t_alpha01", run_id: 4, kind: "run_started", created_at: 1 },
        { id: 11, task_id: "t_alpha01", run_id: 4, kind: "run_completed", created_at: 2 },
      ],
    }), "alpha-board", "t_alpha01", "4", 1_700_000_100_000);
    expect(empty?.linkedEvents.phase).toBe("empty");
    expect(unavailable?.linkedEvents.phase).toBe("unavailable");
    expect(duplicate?.linkedEvents.phase).toBe("unavailable");
  });

  it("fails closed on mismatched identity, malformed runs, invalid timestamps, and oversized collections", () => {
    expect(parseExecutionCollectionSource(null, "alpha-board", "t_alpha01", 1)).toBeNull();
    expect(parseExecutionCollectionSource(taskWire(), "../escape", "t_alpha01", 1)).toBeNull();
    expect(parseExecutionCollectionSource(taskWire(), "alpha-board", "another-task", 1)).toBeNull();
    expect(parseExecutionCollectionSource(taskWire({ runs: [run({ task_id: "another-task" })] }), "alpha-board", "t_alpha01", 1)).toBeNull();
    expect(parseExecutionCollectionSource(taskWire({ runs: [run({ started_at: -1 })] }), "alpha-board", "t_alpha01", 1)).toBeNull();
    expect(parseExecutionCollectionSource(taskWire({ runs: [run(), run()] }), "alpha-board", "t_alpha01", 1)).toBeNull();
    expect(parseExecutionCollectionSource(taskWire({ runs: Array.from({ length: 501 }, () => run()) }), "alpha-board", "t_alpha01", 1)).toBeNull();
    expect(parseExecutionDetailSource(taskWire(), "alpha-board", "t_alpha01", "5", 1)).toBeNull();
  });

  it("validates source-local run IDs canonically before navigation or lookup", () => {
    expect(validateExecutionId("4")).toBe("4");
    for (const unsafe of ["0", "04", "-1", "1.5", "../4", "4/child", "4%2fchild", "4\n", "", String(Number.MAX_SAFE_INTEGER + 1)]) {
      expect(validateExecutionId(unsafe)).toBeNull();
    }
  });

  it("deeply freezes the projection and retains no raw references", () => {
    const rawRun = run();
    const parsed = parseExecutionCollectionSource(taskWire({ runs: [rawRun] }), "alpha-board", "t_alpha01", 1)!;
    rawRun.status = "mutated";
    expect(parsed.executions[0].originalSourceStatus).toBe("done");
    expect(Object.isFrozen(parsed)).toBe(true);
    expect(Object.isFrozen(parsed.executions)).toBe(true);
    expect(Object.isFrozen(parsed.executions[0])).toBe(true);
  });
});

describe("controlled execution client", () => {
  it("classifies the source as controlled and production-available", () => {
    expect(EXECUTION_LIVE_SOURCE_CLASSIFICATION).toEqual(expect.objectContaining({
      classification: "safe_controlled_product_source",
      productionAvailability: "available",
      source: "pepper-controlled-execution",
      profileBehavior: expect.stringContaining("run.profile remains a source fact"),
      rawTransportExposure: expect.stringContaining("product response"),
    }));
  });

  it("preserves exact board, task, run, and profile qualifiers in navigation", () => {
    expect(buildExecutionsPath("review-profile")).toBe("/agent-platform/executions?profile=review-profile");
    expect(buildExecutionsPath("review-profile", "alpha-board", "t_alpha01"))
      .toBe("/agent-platform/executions?board=alpha-board&task=t_alpha01&profile=review-profile");
    expect(buildExecutionDetailPath(4, "alpha-board", "t_alpha01", "review-profile"))
      .toBe("/agent-platform/executions/4?board=alpha-board&task=t_alpha01&profile=review-profile");
    expect(buildExecutionDetailPath("04", "alpha-board", "t_alpha01", "review-profile")).toBeNull();
    expect(buildExecutionsPath("review-profile", "alpha-board", "../escape")).toBeNull();
  });

  it("reads one exact run through the authenticated product detail endpoint", async () => {
    vi.stubGlobal("window", { __HERMES_SESSION_TOKEN__: "synthetic-session" });
    const fetchMock = vi
      .fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>()
      .mockResolvedValueOnce(new Response(JSON.stringify(taskWire()), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    const loaded = await loadExecutionInspectorRequest(
      { kind: "detail", boardSlug: "alpha-board", taskId: "t_alpha01", executionId: "4" },
      "review-profile",
    );
    expect(loaded?.kind).toBe("detail");
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(String(fetchMock.mock.calls[0][0])).toBe("/api/agent-platform/executions/4?board=alpha-board&task=t_alpha01&profile=review-profile");
    for (const call of fetchMock.mock.calls) {
      expect(call[1]?.method).toBeUndefined();
      expect(new Headers(call[1]?.headers).get("X-Hermes-Session-Token")).toBe("synthetic-session");
    }
  });

  it("propagates one abort signal through the exact product GET", async () => {
    vi.stubGlobal("window", { __HERMES_SESSION_TOKEN__: "synthetic-session" });
    const fetchMock = vi
      .fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>()
      .mockResolvedValueOnce(new Response(JSON.stringify(taskWire()), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    const controller = new AbortController();

    await loadExecutionInspectorRequest(
      { kind: "detail", boardSlug: "alpha-board", taskId: "t_alpha01", executionId: "4" },
      "review-profile",
      controller.signal,
    );

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls.every((call) => call[1]?.signal === controller.signal)).toBe(true);
  });

  it("does not request a missing or invalid source context and never falls back to another board", async () => {
    vi.stubGlobal("window", {});
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(async () => new Response(JSON.stringify({ detail: "not found" }), { status: 404 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(getQualifiedExecutionSource("../escape", "t_alpha01", "default")).resolves.toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
    await expect(getQualifiedExecutionSource("missing-board", "t_alpha01", "default")).resolves.toBeNull();
    expect(fetchMock).toHaveBeenCalledOnce();
    expect(String(fetchMock.mock.calls[0][0])).toBe("/api/agent-platform/executions?board=missing-board&task=t_alpha01&profile=default");
  });

  it("rejects an invalid detail run ID before any source request", async () => {
    vi.stubGlobal("window", {});
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    await expect(loadExecutionInspectorRequest(
      { kind: "detail", boardSlug: "alpha-board", taskId: "t_alpha01", executionId: "04" },
      "default",
    )).resolves.toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });

});

describe("execution polling and identity freshness", () => {
  it("polls recursively, prevents overlap, and retains the last success as stale", async () => {
    const scheduled: Array<() => void> = [];
    const states: ExecutionInspectorDataState[] = [];
    let resolveFirst: (value: ExecutionInspectorViewModel | null) => void = () => {};
    const load = vi
      .fn<() => Promise<ExecutionInspectorViewModel | null>>()
      .mockImplementationOnce(() => new Promise((resolve) => { resolveFirst = resolve; }))
      .mockRejectedValueOnce(new Error("raw private transport error"));
    const poller = createExecutionInspectorPoller(load, (next) => states.push(next), {
      now: () => 1234,
      setTimer: (callback, delay) => {
        expect(delay).toBe(EXECUTION_INSPECTOR_POLL_MS);
        scheduled.push(callback);
        return callback;
      },
      clearTimer: () => {},
    });

    const first = poller.start();
    expect(await poller.refresh()).toBe(false);
    resolveFirst(collectionView());
    expect(await first).toBe(true);
    expect(states.at(-1)).toMatchObject({ phase: "ready", lastSuccessAt: 1234 });
    const snapshot = states.at(-1)?.snapshot;
    scheduled.shift()?.();
    await vi.waitFor(() => expect(states.at(-1)?.phase).toBe("stale"));
    expect(states.at(-1)?.snapshot).toBe(snapshot);
    expect(JSON.stringify(states)).not.toContain("raw private transport error");
    poller.stop();
  });

  it("distinguishes empty, unavailable, and initial error states", async () => {
    const runPoller = async (load: () => Promise<ExecutionInspectorViewModel | null>) => {
      const states: ExecutionInspectorDataState[] = [];
      const poller = createExecutionInspectorPoller(load, (next) => states.push(next));
      await poller.start();
      poller.stop();
      return states.at(-1)?.phase;
    };
    const empty: ExecutionInspectorViewModel = {
      kind: "executions",
      collection: parseExecutionCollectionSource(taskWire({ runs: [] }), "alpha-board", "t_alpha01", 1)!,
    };
    expect(await runPoller(async () => empty)).toBe("empty");
    expect(await runPoller(async () => null)).toBe("unavailable");
    expect(await runPoller(async () => { throw new Error("not retained"); })).toBe("error");
  });

  it("keys every profile, board, task, and run identity independently", () => {
    const keys = new Set([
      executionInspectorRequestKey({ kind: "executions", boardSlug: "alpha", taskId: "task" }, "default"),
      executionInspectorRequestKey({ kind: "executions", boardSlug: "beta", taskId: "task" }, "default"),
      executionInspectorRequestKey({ kind: "executions", boardSlug: "alpha", taskId: "other" }, "default"),
      executionInspectorRequestKey({ kind: "detail", boardSlug: "alpha", taskId: "task", executionId: "1" }, "default"),
      executionInspectorRequestKey({ kind: "detail", boardSlug: "alpha", taskId: "task", executionId: "2" }, "default"),
      executionInspectorRequestKey({ kind: "detail", boardSlug: "alpha", taskId: "task", executionId: "1" }, "other"),
    ]);
    expect(keys.size).toBe(6);
    expect(INITIAL_EXECUTION_INSPECTOR_STATE).toEqual({
      phase: "loading",
      snapshot: null,
      lastSuccessAt: null,
      refreshing: false,
    });
    expect(EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS).toBeGreaterThan(EXECUTION_INSPECTOR_POLL_MS);
  });

  it("aborts an unresolved request when polling stops", async () => {
    const requestSignals: AbortSignal[] = [];
    const load = vi.fn((signal: AbortSignal) => new Promise<ExecutionInspectorViewModel | null>((_resolve, reject) => {
      requestSignals.push(signal);
      signal.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")), { once: true });
    }));
    const publish = vi.fn();
    const poller = createExecutionInspectorPoller(load, publish);
    const started = poller.start();
    expect(requestSignals[0]?.aborted).toBe(false);
    poller.stop();
    await expect(started).resolves.toBe(false);
    expect(requestSignals[0]?.aborted).toBe(true);
    expect(publish).not.toHaveBeenCalled();
  });

  it("aborts an unresolved request at the bounded timeout", async () => {
    vi.useFakeTimers();
    const requestSignals: AbortSignal[] = [];
    const load = vi.fn((signal: AbortSignal) => new Promise<ExecutionInspectorViewModel | null>((_resolve, reject) => {
      requestSignals.push(signal);
      signal.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")), { once: true });
    }));
    const poller = createExecutionInspectorPoller(load, () => {});
    const started = poller.start();
    await vi.advanceTimersByTimeAsync(EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS);
    await expect(started).resolves.toBe(false);
    expect(requestSignals[0]?.aborted).toBe(true);
    poller.stop();
  });
});

describe("controlled Execution Inspector pages", () => {
  it("renders exact source facts, local filters, retention limits, and qualified detail links", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter><ExecutionInspectorView state={state(collectionView())} profile="review-profile" refresh={() => {}} /></MemoryRouter>,
    );
    expect(markup).toContain("Execution Inspector");
    expect(markup).toContain("Pepper controlled execution records");
    expect(markup).toContain("Git staging, commit, and push stay human-only");
    expect(markup).toContain("Hermes API-server run");
    expect(markup).toContain("Hermes cron agent session");
    expect(markup).toContain("Prepare controlled worker handoff");
    expect(markup).toContain("Source-local ID: 4");
    expect(markup).toContain("Board/task: alpha-board/t_alpha01");
    expect(markup).toContain("Source profile: worker-profile");
    expect(markup).toContain("Filter by run ID, profile, or outcome");
    expect(markup).toContain("Source task title withheld by the execution projection");
    expect(markup).toContain("/agent-platform/executions/4?board=alpha-board&amp;task=t_alpha01&amp;profile=review-profile");
    for (const control of ["Stop", "Retry", "Rollback", "Approve", "Assign", "Dispatch", "Open terminal"]) {
      expect(markup).not.toContain(`>${control}<`);
    }
  });

  it("renders empty, stale, error, and unavailable collection states explicitly", () => {
    const emptyView: ExecutionInspectorViewModel = {
      kind: "executions",
      collection: parseExecutionCollectionSource(taskWire({ runs: [] }), "alpha-board", "t_alpha01", 1)!,
    };
    const empty = renderToStaticMarkup(<MemoryRouter><ExecutionInspectorView state={state(emptyView, "empty")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const stale = renderToStaticMarkup(<MemoryRouter><ExecutionInspectorView state={state(collectionView(), "stale")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const error = renderToStaticMarkup(<MemoryRouter><ExecutionInspectorView state={state(null, "error")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const unavailable = renderToStaticMarkup(<MemoryRouter><ExecutionInspectorView state={state(null, "unavailable")} profile="default" refresh={() => {}} /></MemoryRouter>);
    expect(empty).toContain("exact source task returned no run records");
    expect(stale).toContain("last validated source-local projection");
    expect(error).toContain("Execution source could not be reached");
    expect(unavailable).toContain("Qualified execution source unavailable");
    expect(unavailable).toContain("controlled execution source");
    expect(unavailable).toContain("raw provider payloads");
  });

  it("renders safe detail facts, controlled handoff metadata, and explicitly linked event evidence", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter><ExecutionDetailView state={state(detailView())} profile="review-profile" refresh={() => {}} /></MemoryRouter>,
    );
    expect(markup).toContain("Run 4");
    expect(markup).toContain("Source timing and state");
    expect(markup).toContain("Retention and redaction");
    expect(markup).toContain("Workflow");
    expect(markup).toContain("Git handoff");
    expect(markup).toContain("Explicitly linked source events");
    expect(markup).toContain("Safe action category");
    expect(markup).toContain("Validation summaries");
    expect(markup).toContain("Result summary");
    expect(markup).toContain("Failure summary");
    expect(markup).toContain("Artifact-reference metadata");
    expect(markup).toContain("Diagnostics");
    expect(markup).toContain("Executable content excluded");
    expect(markup).toContain("Display timeline ordering is source-local presentation, not authoritative causality");
    expect(markup).toContain("run_started");
    expect(markup).toContain("Source event ID: 10");
    expect(markup).toContain("Worker handoff preparation is explicit and bounded to the accepted P15/P17 substrate");
    expect(markup).toContain("not a durable audit timeline");
    expect(markup).toContain("/agent-platform/executions?board=alpha-board&amp;task=t_alpha01&amp;profile=review-profile");
    expect(markup).not.toContain("private-event-token");
    expect(markup).not.toContain("private raw run error");
    for (const control of ["Stop", "Retry", "Rollback", "Approve", "Assign", "Dispatch", "Open terminal"]) {
      expect(markup).not.toContain(`>${control}<`);
    }
  });

  it("renders independently empty and unavailable linked-event sections", () => {
    const emptyMarkup = renderToStaticMarkup(
      <MemoryRouter><ExecutionDetailView state={state(detailView(taskWire({ events: [] })))} profile="default" refresh={() => {}} /></MemoryRouter>,
    );
    const unavailableMarkup = renderToStaticMarkup(
      <MemoryRouter><ExecutionDetailView state={state(detailView(taskWire({ events: "unsafe" })))} profile="default" refresh={() => {}} /></MemoryRouter>,
    );
    expect(emptyMarkup).toContain("No retained events explicitly reference this source run");
    expect(unavailableMarkup).toContain("linked event section could not be projected safely");
  });

  it("renders independently empty and unavailable optional evidence sections", () => {
    const emptyRaw = taskWire({
      task: { id: "t_alpha01", title: "Inspect source run", diagnostics: [] },
      runs: [run({ summary: null, error: null })],
      attachments: [],
    });
    const unavailableRaw = taskWire({
      task: { id: "t_alpha01", title: "Inspect source run", diagnostics: "unsafe" },
      runs: [run({ summary: { unsafe: true }, error: { unsafe: true } })],
      attachments: "unsafe",
    });
    const emptyMarkup = renderToStaticMarkup(
      <MemoryRouter><ExecutionDetailView state={state(detailView(emptyRaw))} profile="default" refresh={() => {}} /></MemoryRouter>,
    );
    const unavailableMarkup = renderToStaticMarkup(
      <MemoryRouter><ExecutionDetailView state={state(detailView(unavailableRaw))} profile="default" refresh={() => {}} /></MemoryRouter>,
    );
    expect(emptyMarkup).toContain("No safe source result summary");
    expect(emptyMarkup).toContain("No source failure summary");
    expect(emptyMarkup).toContain("No task-level artifact references");
    expect(emptyMarkup).toContain("No diagnostics explicitly reference this source run");
    expect(unavailableMarkup).toContain("source result summary could not be projected safely");
    expect(unavailableMarkup).toContain("source failure summary could not be projected safely");
    expect(unavailableMarkup).toContain("Artifact-reference metadata could not be projected safely");
    expect(unavailableMarkup).toContain("Diagnostics could not be projected safely");
  });

  it("preserves requested board and task context in an unavailable detail back link", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <ExecutionDetailView
          state={state(null, "unavailable")}
          profile="review-profile"
          refresh={() => {}}
          requestedBoardSlug="alpha-board"
          requestedTaskId="t_alpha01"
        />
      </MemoryRouter>,
    );
    expect(markup).toContain("/agent-platform/executions?board=alpha-board&amp;task=t_alpha01&amp;profile=review-profile");
  });
});

describe("Execution Inspector descriptors", () => {
  it("declares two deterministic contextual routes with one navigation entry", () => {
    expect(EXECUTION_INSPECTOR_DESCRIPTORS).toEqual([
      EXECUTION_INSPECTOR_DESCRIPTOR,
      EXECUTION_DETAIL_DESCRIPTOR,
    ]);
    expect(EXECUTION_INSPECTOR_DESCRIPTORS.map((descriptor) => [
      descriptor.id,
      descriptor.route.path,
      descriptor.navigation?.label,
    ])).toEqual([
      ["agent_platform.ui.executions", "/agent-platform/executions", "Executions"],
      ["agent_platform.ui.execution_detail", "/agent-platform/executions/:executionId", undefined],
    ]);
    expect(EXECUTION_INSPECTOR_DESCRIPTORS.every((descriptor) =>
      descriptor.owner === "AGENT_PLATFORM" &&
      descriptor.featureId === "agent_platform.product_ui" &&
      descriptor.visibleWhenExperimental)).toBe(true);
  });
});
