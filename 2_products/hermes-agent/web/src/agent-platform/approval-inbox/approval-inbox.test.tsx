import { readFileSync } from "node:fs";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  APPROVAL_LIVE_SOURCE_CLASSIFICATION,
  buildApprovalDetailPath,
  buildApprovalInboxPath,
  getApproval,
  listApprovals,
  loadApprovalInboxRequest,
} from "./approval-client";
import { ApprovalDetailView } from "./approval-detail-page";
import { ApprovalInboxView } from "./approval-inbox-page";
import {
  classifyApprovalSourceSemantics,
  parseApprovalDetailSource,
  parseApprovalInboxSource,
  validateApprovalId,
  validateProfileName,
  type ApprovalInboxDataState,
  type ApprovalInboxView as ApprovalInboxViewModel,
} from "./contract";
import {
  APPROVAL_DETAIL_DESCRIPTOR,
  APPROVAL_INBOX_DESCRIPTOR,
  APPROVAL_INBOX_DESCRIPTORS,
} from "./descriptors";
import {
  approvalInboxRequestKey,
  APPROVAL_INBOX_POLL_MS,
  createApprovalInboxPoller,
  INITIAL_APPROVAL_INBOX_STATE,
} from "./use-approval-inbox";

function approval(overrides: Record<string, unknown> = {}) {
  return {
    id: "a1b2c3d4",
    semantics: "explicit_approval_request",
    title: "Review staged memory write",
    summary: "A bounded source summary for human review.",
    status: "pending",
    request_type: "memory_write",
    requested_at: 1_700_000_100,
    expires_at: 1_700_003_600,
    requester: "foreground source",
    risk_label: "medium",
    target: { type: "configuration_action", label: "Memory entry" },
    reason: "The source requested an explicit decision before applying this staged write.",
    payload: { command: "rm -rf private", token: "private-token" },
    provider_id: "private-provider",
    model_id: "private-model",
    worker_pid: 4312,
    ...overrides,
  };
}

function inboxWire(values: unknown[] = [approval()]) {
  return {
    source_system: "hermes-write-approval",
    source_authority: "source-controlled",
    canonical_approval_authority: "source-claimed",
    approvals: values,
    raw_payload: { secret: "private" },
  };
}

function detailWire(overrides: Record<string, unknown> = {}) {
  return {
    source_system: "hermes-write-approval",
    approval: approval(),
    evidence: [{ id: "evidence:1", label: "Staged source summary" }],
    decisions: [{
      id: "decision:1",
      status: "approved",
      decided_at: 1_700_000_200,
      actor: "source operator",
      raw_result: { command: "private" },
    }],
    ...overrides,
  };
}

function inboxView(values: unknown[] = [approval()]): ApprovalInboxViewModel {
  return { kind: "inbox", approvals: parseApprovalInboxSource(inboxWire(values))! };
}

function detailView(raw = detailWire()): ApprovalInboxViewModel {
  return { kind: "detail", approval: parseApprovalDetailSource(raw, "a1b2c3d4")! };
}

function state(
  snapshot: ApprovalInboxViewModel | null,
  phase: ApprovalInboxDataState["phase"] = "ready",
): ApprovalInboxDataState {
  return { phase, snapshot, lastSuccessAt: 1_700_000_000_000, refreshing: false };
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("approval-source eligibility", () => {
  it("accepts only explicit approval, confirmation, permission, and allow-deny semantics", () => {
    for (const semantic of [
      "explicit_approval_request",
      "explicit_confirmation_request",
      "explicit_permission_decision_request",
      "explicit_allow_deny_decision_record",
    ]) expect(classifyApprovalSourceSemantics(semantic)).toBe("eligible");
  });

  it("rejects workflow, authentication, transport, runtime, warning, and log lookalikes", () => {
    for (const semantic of [
      "kanban_review",
      "kanban_blocked",
      "kanban_ready",
      "task_comment",
      "task_diagnostic",
      "task_run",
      "worker_claim",
      "provider_authentication",
      "oauth_state",
      "api_authentication",
      "gateway_busy",
      "generic_warning",
      "error_log",
      "chat_message",
      "filesystem_prompt",
      "terminal_prompt_without_durable_identity",
    ]) expect(classifyApprovalSourceSemantics(semantic)).toBe("ineligible");
  });
});

describe("safe approval projection", () => {
  it("preserves source-local identity, source facts, safe target metadata, and deterministic order", () => {
    const parsed = parseApprovalInboxSource(inboxWire([
      approval({ id: "history:2", status: "approved", requested_at: 1_700_000_300 }),
      approval({ id: "pending:2", requested_at: 1_700_000_200 }),
      approval({ id: "pending:1", requested_at: 1_700_000_100 }),
    ]));

    expect(parsed?.map((item) => item.sourceLocalApprovalId)).toEqual(["pending:2", "pending:1", "history:2"]);
    expect(parsed?.[0]).toMatchObject({
      source: {
        sourceSystem: "hermes-write-approval",
        sourceAuthority: "provisional",
        canonicalApprovalAuthority: "not_yet_established",
      },
      originalSourceStatus: "pending",
      visualStatus: "pending",
      originalSourceType: "memory_write",
      requestCategory: "approval",
      target: { sourceTargetType: "configuration action", sourceTargetLabel: "Memory entry" },
    });
  });

  it("maps unknown source statuses only to other without inferring from time or text", () => {
    const parsed = parseApprovalInboxSource(inboxWire([
      approval({ status: "awaiting_external_operator", summary: "approved words do not decide status", expires_at: 1 }),
    ]));
    expect(parsed?.[0]).toMatchObject({
      originalSourceStatus: "awaiting_external_operator",
      visualStatus: "other",
    });
  });

  it("rejects malformed records, unsafe IDs, overlong values, invalid timestamps, and oversized collections", () => {
    expect(parseApprovalInboxSource(null)).toBeNull();
    expect(parseApprovalInboxSource({ source_system: "other", approvals: [] })).toBeNull();
    expect(parseApprovalInboxSource(inboxWire([approval({ id: "../escape" })]))).toBeNull();
    expect(parseApprovalInboxSource(inboxWire([approval({ title: "x".repeat(301) })]))).toBeNull();
    expect(parseApprovalInboxSource(inboxWire([approval({ requested_at: -1 })]))).toBeNull();
    expect(parseApprovalInboxSource(inboxWire([approval({ requested_at: Number.POSITIVE_INFINITY })]))).toBeNull();
    expect(parseApprovalInboxSource(inboxWire(Array.from({ length: 501 }, () => approval())))).toBeNull();
    expect(parseApprovalInboxSource(inboxWire([approval({ semantics: "kanban_review" })]))).toBeNull();
  });

  it("redacts sensitive text and drops executable, runtime, provider, path, and raw payload fields", () => {
    const parsed = parseApprovalInboxSource(inboxWire([approval({
      summary: [
        "command=rm -rf private",
        "tool_args=--dangerous private",
        "TOKEN=private-token",
        "provider_id=private-provider model_id=private-model pid=4312",
        "workspace C:\\private\\workspace",
        "endpoint http://127.0.0.1:9125/private",
        "authorization=Bearer-private",
        "Traceback (most recent call last): private stack",
      ].join("\n"),
      target: { type: "tool_action", label: "token=target-secret /home/private/target" },
      requester: "provider=private-provider",
    })]));
    const serialized = JSON.stringify(parsed);
    for (const forbidden of [
      "rm -rf", "--dangerous", "private-token", "private-provider", "private-model", "4312",
      "private\\workspace", "/home/private", "127.0.0.1", "Bearer-private", "private stack",
      "raw_payload", "worker_pid", "provider_id", "model_id", "payload",
    ]) expect(serialized).not.toContain(forbidden);
    expect(serialized).toContain("[redacted");
  });

  it("does not retain raw references and freezes projections deeply", () => {
    const raw = approval();
    const wire = inboxWire([raw]);
    const parsed = parseApprovalInboxSource(wire)!;
    raw.title = "mutated after parse";
    expect(parsed[0].title).toBe("Review staged memory write");
    expect(Object.isFrozen(parsed)).toBe(true);
    expect(Object.isFrozen(parsed[0])).toBe(true);
    expect(Object.isFrozen(parsed[0].target)).toBe(true);
    expect(() => { (parsed[0].target as { sourceTargetLabel: string }).sourceTargetLabel = "mutated"; }).toThrow();
  });

  it("projects exact detail identity plus safe evidence and source decision history", () => {
    const parsed = parseApprovalDetailSource(detailWire(), "a1b2c3d4");
    expect(parsed).toMatchObject({
      sourceLocalApprovalId: "a1b2c3d4",
      sourceReason: "The source requested an explicit decision before applying this staged write.",
      evidence: { phase: "ready" },
      decisionHistory: { phase: "ready" },
    });
    expect(parsed?.evidence.items[0]).toMatchObject({
      sourceLocalEvidenceId: "evidence:1",
      sourceEvidenceLabel: "Staged source summary",
    });
    expect(parsed?.decisionHistory.items[0]).toMatchObject({
      sourceLocalDecisionId: "decision:1",
      originalSourceStatus: "approved",
      visualStatus: "approved",
      sourceActorLabel: "source operator",
    });
    expect(JSON.stringify(parsed)).not.toContain("raw_result");
  });

  it("models empty and unavailable optional detail sections independently", () => {
    const empty = parseApprovalDetailSource(detailWire({ evidence: [], decisions: [] }), "a1b2c3d4");
    expect([empty?.evidence.phase, empty?.decisionHistory.phase]).toEqual(["empty", "empty"]);
    const unavailable = parseApprovalDetailSource(detailWire({ evidence: "unsafe", decisions: [] }), "a1b2c3d4");
    expect([unavailable?.evidence.phase, unavailable?.decisionHistory.phase]).toEqual(["unavailable", "empty"]);
  });

  it("rejects detail responses for another or invalid source-local identity", () => {
    expect(parseApprovalDetailSource(detailWire(), "other:id")).toBeNull();
    expect(parseApprovalDetailSource(detailWire(), "../escape")).toBeNull();
  });

  it("validates source and profile identifiers before navigation or lookup", () => {
    expect(validateApprovalId("a1b2c3d4")).toBe("a1b2c3d4");
    expect(validateProfileName("review.profile-1")).toBe("review.profile-1");
    for (const unsafe of ["../escape", "C:\\private", "/absolute", "id/child", "id%2fchild", "id\nchild", ""]) {
      expect(validateApprovalId(unsafe)).toBeNull();
    }
  });
});

describe("unavailable read-only approval client", () => {
  it("classifies the audited source as partial but production-unavailable", () => {
    expect(APPROVAL_LIVE_SOURCE_CLASSIFICATION).toEqual(expect.objectContaining({
      classification: "safe_partial_read_source",
      productionAvailability: "unavailable",
    }));
  });

  it("preserves profile context and validates IDs before encoding deep links", () => {
    expect(buildApprovalInboxPath("review-profile")).toBe("/agent-platform/approvals?profile=review-profile");
    expect(buildApprovalDetailPath("a1b2c3d4", "review-profile"))
      .toBe("/agent-platform/approvals/a1b2c3d4?profile=review-profile");
    expect(buildApprovalDetailPath("../escape", "review-profile")).toBeNull();
    expect(buildApprovalInboxPath("../escape")).toBeNull();
  });

  it("makes no network or mutation request when no safe HTTP source exists", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    await expect(listApprovals("default")).resolves.toBeNull();
    await expect(getApproval("a1b2c3d4", "default")).resolves.toBeNull();
    await expect(loadApprovalInboxRequest({ kind: "inbox" }, "default")).resolves.toBeNull();
    await expect(loadApprovalInboxRequest({ kind: "detail", approvalId: "a1b2c3d4" }, "default"))
      .resolves.toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();

    const source = readFileSync(new URL("./approval-client.ts", import.meta.url), "utf8");
    expect(source).not.toMatch(/fetch\s*\(/);
    expect(source).not.toMatch(/\/api\//);
    expect(source).not.toMatch(/\b(?:POST|PUT|PATCH|DELETE)\b/);
    expect(source).not.toMatch(/approve|reject|confirm|deny|cancel|retry|execute|provider|worker/i);
  });
});

describe("approval polling and identity freshness", () => {
  it("polls recursively, prevents overlap, and retains the last success as stale", async () => {
    const scheduled: Array<() => void> = [];
    const states: ApprovalInboxDataState[] = [];
    let resolveFirst: (value: ApprovalInboxViewModel | null) => void = () => {};
    const load = vi
      .fn<() => Promise<ApprovalInboxViewModel | null>>()
      .mockImplementationOnce(() => new Promise((resolve) => { resolveFirst = resolve; }))
      .mockRejectedValueOnce(new Error("raw private transport error"));
    const poller = createApprovalInboxPoller(load, (next) => states.push(next), {
      now: () => 1234,
      setTimer: (callback, delay) => {
        expect(delay).toBe(APPROVAL_INBOX_POLL_MS);
        scheduled.push(callback);
        return callback;
      },
      clearTimer: () => {},
    });

    const first = poller.start();
    expect(await poller.refresh()).toBe(false);
    expect(load).toHaveBeenCalledOnce();
    resolveFirst(inboxView());
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
    const run = async (load: () => Promise<ApprovalInboxViewModel | null>) => {
      const states: ApprovalInboxDataState[] = [];
      const poller = createApprovalInboxPoller(load, (next) => states.push(next));
      await poller.start();
      poller.stop();
      return states.at(-1)?.phase;
    };
    expect(await run(async () => ({ kind: "inbox", approvals: [] }))).toBe("empty");
    expect(await run(async () => null)).toBe("unavailable");
    expect(await run(async () => { throw new Error("not retained"); })).toBe("error");
  });

  it("suppresses late responses after stop and keys every profile and approval identity", async () => {
    const states: ApprovalInboxDataState[] = [];
    let resolveLoad: (value: ApprovalInboxViewModel | null) => void = () => {};
    const poller = createApprovalInboxPoller(
      () => new Promise((resolve) => { resolveLoad = resolve; }),
      (next) => states.push(next),
    );
    const pending = poller.start();
    poller.stop();
    resolveLoad(inboxView());
    expect(await pending).toBe(false);
    expect(states).toEqual([]);

    const keys = new Set([
      approvalInboxRequestKey({ kind: "inbox" }, "default"),
      approvalInboxRequestKey({ kind: "inbox" }, "other"),
      approvalInboxRequestKey({ kind: "detail", approvalId: "approval:one" }, "default"),
      approvalInboxRequestKey({ kind: "detail", approvalId: "approval:two" }, "default"),
      approvalInboxRequestKey({ kind: "detail", approvalId: "approval:one" }, "other"),
    ]);
    expect(keys.size).toBe(5);
  });

  it("exposes a loading state before any source-qualified response", () => {
    expect(INITIAL_APPROVAL_INBOX_STATE).toEqual({
      phase: "loading",
      snapshot: null,
      lastSuccessAt: null,
      refreshing: false,
    });
  });
});

describe("read-only Approval Inbox pages", () => {
  it("renders provisional source facts, local filters, counts, and profile-preserving detail links", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter><ApprovalInboxView state={state(inboxView())} profile="review-profile" refresh={() => {}} /></MemoryRouter>,
    );
    expect(markup).toContain("Approval Inbox");
    expect(markup).toContain("Provisional source");
    expect(markup).toContain("No governed AGENT PLATFORM approval authority is active");
    expect(markup).toContain("Source pending is not governed pending approval");
    expect(markup).toContain("Pending in source");
    expect(markup).toContain("Historical source states");
    expect(markup).toContain("a1b2c3d4?profile=review-profile");
    expect(markup).toContain("Filter by title, source ID, target, or summary");
    for (const control of ["Approve", "Reject", "Allow", "Deny", "Confirm", "Execute", "Retry", "Assign", "Escalate"]) {
      expect(markup).not.toContain(`>${control}<`);
    }
  });

  it("renders empty, stale, error, and unavailable inbox states explicitly", () => {
    const empty = renderToStaticMarkup(<MemoryRouter><ApprovalInboxView state={state({ kind: "inbox", approvals: [] }, "empty")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const stale = renderToStaticMarkup(<MemoryRouter><ApprovalInboxView state={state(inboxView(), "stale")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const error = renderToStaticMarkup(<MemoryRouter><ApprovalInboxView state={state(null, "error")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const unavailable = renderToStaticMarkup(<MemoryRouter><ApprovalInboxView state={state(null, "unavailable")} profile="default" refresh={() => {}} /></MemoryRouter>);
    expect(empty).toContain("safe source returned no approval presentations");
    expect(stale).toContain("last validated provisional source projection");
    expect(error).toContain("Approval source could not be reached");
    expect(unavailable).toContain("Approval source unavailable");
    expect(unavailable).toContain("Kanban, Chat, logs, providers, workers, OAuth and transient prompts are not used as fallbacks");
  });

  it("renders safe detail and source-qualified optional sections without action controls", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter><ApprovalDetailView state={state(detailView())} profile="review-profile" refresh={() => {}} /></MemoryRouter>,
    );
    expect(markup).toContain("Source-local approval ID a1b2c3d4");
    expect(markup).toContain("Safe summary");
    expect(markup).toContain("Safe target metadata");
    expect(markup).toContain("Safe reason");
    expect(markup).toContain("Evidence summaries");
    expect(markup).toContain("Source decision history");
    expect(markup).toContain("No approval or rejection action is available in P13.5");
    expect(markup).toContain("not a canonical ApprovalRequest");
    expect(markup).toContain("/agent-platform/approvals?profile=review-profile");
    expect(markup).not.toContain("private-provider");
    expect(markup).not.toContain("rm -rf");
    for (const control of ["Approve", "Reject", "Allow", "Deny", "Confirm", "Cancel", "Retry", "Execute", "Open terminal", "Edit policy"]) {
      expect(markup).not.toContain(`>${control}<`);
    }
  });

  it("renders independently empty and unavailable detail sections", () => {
    const detail = parseApprovalDetailSource(detailWire({ evidence: [], decisions: "unsafe" }), "a1b2c3d4")!;
    const markup = renderToStaticMarkup(
      <MemoryRouter><ApprovalDetailView state={state({ kind: "detail", approval: detail })} profile="default" refresh={() => {}} /></MemoryRouter>,
    );
    expect(markup).toContain("No safe source evidence summaries");
    expect(markup).toContain("optional source section cannot be projected safely");
  });

  it("escapes long bounded plain text rather than rendering HTML or Markdown", () => {
    const raw = approval({
      title: "<script>Unsafe title</script>",
      summary: `**plain markdown** <img src=x> ${"bounded ".repeat(300)}`,
    });
    const markup = renderToStaticMarkup(
      <MemoryRouter><ApprovalInboxView state={state(inboxView([raw]))} profile="default" refresh={() => {}} /></MemoryRouter>,
    );
    expect(markup).toContain("&lt;script&gt;Unsafe title&lt;/script&gt;");
    expect(markup).toContain("**plain markdown** &lt;img src=x&gt;");
    expect(markup).not.toContain("<script>Unsafe title</script>");
  });
});

describe("Approval Inbox descriptors", () => {
  it("declares two deterministic contextual routes with one navigation entry", () => {
    expect(APPROVAL_INBOX_DESCRIPTORS).toEqual([APPROVAL_INBOX_DESCRIPTOR, APPROVAL_DETAIL_DESCRIPTOR]);
    expect(APPROVAL_INBOX_DESCRIPTORS.map((descriptor) => [
      descriptor.id,
      descriptor.route.path,
      descriptor.navigation?.label,
    ])).toEqual([
      ["agent_platform.ui.approvals", "/agent-platform/approvals", "Approvals"],
      ["agent_platform.ui.approval_detail", "/agent-platform/approvals/:approvalId", undefined],
    ]);
    expect(APPROVAL_INBOX_DESCRIPTORS.every((descriptor) =>
      descriptor.owner === "AGENT_PLATFORM" &&
      descriptor.featureId === "agent_platform.product_ui" &&
      descriptor.visibleWhenExperimental)).toBe(true);
  });
});
