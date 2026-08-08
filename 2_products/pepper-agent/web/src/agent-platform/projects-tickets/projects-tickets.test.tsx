import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  parseProjectSource,
  parseProjectsSource,
  parseTicketSource,
  validateBoardSlug,
  validateProfileName,
  validateTaskId,
  type ProjectSummary,
  type ProjectsWorkspaceDataState,
  type ProjectsWorkspaceView,
} from "./contract";
import {
  PROJECTS_DESCRIPTOR,
  PROJECT_DETAIL_DESCRIPTOR,
  PROJECTS_TICKETS_DESCRIPTORS,
  TICKET_DETAIL_DESCRIPTOR,
} from "./descriptors";
import {
  buildKanbanSourcePath,
  buildProjectPath,
  buildProjectsPath,
  buildTicketPath,
  getProjectSource,
  getTicketSource,
  listProjectsSource,
  loadProjectsWorkspaceRequest,
} from "./kanban-client";
import { ProjectDetailView } from "./project-detail-page";
import { ProjectsView } from "./projects-page";
import { TicketDetailView } from "./ticket-detail-page";
import {
  createProjectsWorkspacePoller,
  INITIAL_PROJECTS_WORKSPACE_STATE,
  PROJECTS_WORKSPACE_POLL_MS,
  projectsWorkspaceRequestKey,
} from "./use-projects-workspace";

function board(overrides: Record<string, unknown> = {}) {
  return {
    slug: "alpha-board",
    name: "Alpha Project",
    description: "Source-qualified project description",
    counts: { todo: 1, scheduled: 1, done: 1 },
    total: 3,
    db_path: "C:\\private\\kanban.db",
    default_workdir: "/home/private/repository",
    provider: "synthetic-provider",
    ...overrides,
  };
}

function task(overrides: Record<string, unknown> = {}) {
  return {
    id: "t_alpha01",
    title: "Parent Ticket",
    body: "Bounded plain-text description",
    status: "todo",
    priority: 7,
    tenant: "tenant-label",
    assignee: "profile-label",
    created_at: 1_700_000_000,
    started_at: null,
    completed_at: null,
    link_counts: { parents: 0, children: 1 },
    workspace_path: "C:\\private\\workspace",
    claim_lock: "worker-secret",
    worker_pid: 4312,
    last_failure_error: "private raw error",
    model_override: "synthetic-provider/model",
    ...overrides,
  };
}

function boardsWire(overrides: Record<string, unknown> = {}) {
  return { boards: [board()], current: "default", ...overrides };
}

function boardWire(tasks: unknown[] = [task()]) {
  return {
    columns: [
      { name: "todo", tasks },
      { name: "scheduled", tasks: [] },
      { name: "done", tasks: [] },
    ],
    tenants: ["tenant-label"],
    assignees: ["profile-label"],
    latest_event_id: 3,
    now: 1_700_000_100,
  };
}

function ticketWire(overrides: Record<string, unknown> = {}) {
  return {
    task: {
      ...task(),
      diagnostics: [{
        kind: "repeated_failures",
        severity: "error",
        title: "Raw private failure",
        detail: "Traceback private-stack",
        actions: [{ kind: "cli_hint", label: "Run", payload: { command: "rm -rf private" } }],
        first_seen_at: 1_700_000_001,
        last_seen_at: 1_700_000_002,
        count: 2,
        data: { last_error: "private raw error" },
      }],
    },
    links: { parents: ["t_parent01"], children: ["t_child01"] },
    comments: [{
      id: 1,
      task_id: "t_alpha01",
      author: "operator",
      body: "Evidence note token=comment-secret C:\\private\\comment.txt",
      created_at: 1_700_000_003,
    }],
    attachments: [{
      id: 2,
      task_id: "t_alpha01",
      filename: "evidence.txt",
      content_type: "text/plain",
      size: 42,
      stored_path: "C:\\private\\attachments\\evidence.txt",
      uploaded_by: "operator",
      created_at: 1_700_000_004,
    }],
    events: [{
      id: 3,
      task_id: "t_alpha01",
      run_id: 4,
      kind: "commented",
      payload: { command: "private-command", oauth_state: "private-oauth" },
      created_at: 1_700_000_005,
    }],
    runs: [{
      id: 4,
      task_id: "t_alpha01",
      profile: "profile-label",
      status: "completed",
      started_at: 1_700_000_006,
      ended_at: 1_700_000_007,
      summary: "Raw private result",
      worker_pid: 991,
      claim_lock: "private-claim",
      metadata: { path: "/home/private/output" },
      error: "private-run-error",
    }],
    ...overrides,
  };
}

function projectSummary(): ProjectSummary {
  return parseProjectsSource(boardsWire())![0];
}

function projectsView(): ProjectsWorkspaceView {
  return { kind: "projects", projects: parseProjectsSource(boardsWire())! };
}

function projectView(tasks: unknown[] = [task()]): ProjectsWorkspaceView {
  return { kind: "project", project: parseProjectSource(boardWire(tasks), projectSummary())! };
}

function ticketView(raw = ticketWire()): ProjectsWorkspaceView {
  return { kind: "ticket", ticket: parseTicketSource(raw, "alpha-board")! };
}

function state(
  snapshot: ProjectsWorkspaceView | null,
  phase: ProjectsWorkspaceDataState["phase"] = "ready",
): ProjectsWorkspaceDataState {
  return { phase, snapshot, lastSuccessAt: 1_700_000_000_000, refreshing: false };
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("Projects and Tickets projection contract", () => {
  it("parses board lists deterministically and excludes raw board authority fields", () => {
    const projects = parseProjectsSource({
      boards: [board({ slug: "zeta", name: "Zeta" }), board({ slug: "alpha", name: "Alpha" })],
    });

    expect(projects?.map((project) => project.boardSlug)).toEqual(["alpha", "zeta"]);
    expect(projects?.[0]).toMatchObject({
      source: {
        sourceSystem: "hermes-kanban",
        sourceAuthority: "provisional",
        futureAuthority: "paperclip-control-plane",
      },
      totalTaskCount: 3,
      sourceFreshness: "current-response",
    });
    expect(JSON.stringify(projects)).not.toContain("kanban.db");
    expect(JSON.stringify(projects)).not.toContain("repository");
    expect(JSON.stringify(projects)).not.toContain("synthetic-provider");
    expect(Object.isFrozen(projects)).toBe(true);
    expect(Object.isFrozen(projects?.[0])).toBe(true);
  });

  it("parses and sorts board-qualified task summaries without raw runtime fields", () => {
    const detail = parseProjectSource(
      boardWire([
        task({ id: "t_low", title: "Low", priority: 1 }),
        task({ id: "t_high", title: "High", priority: 9 }),
      ]),
      projectSummary(),
    );

    expect(detail?.tickets.map((ticket) => ticket.taskId)).toEqual(["t_high", "t_low"]);
    expect(detail?.tickets[0]).toMatchObject({
      boardSlug: "alpha-board",
      originalSourceStatus: "todo",
      visualStatus: "todo",
      sourcePriority: 9,
      parentCount: 0,
      childCount: 1,
    });
    const serialized = JSON.stringify(detail);
    for (const forbidden of ["workspace_path", "private\\workspace", "worker-secret", "4312", "private raw error", "synthetic-provider/model"]) {
      expect(serialized).not.toContain(forbidden);
    }
    expect(Object.isFrozen(detail?.tickets)).toBe(true);
  });

  it("projects bounded detail sections and removes sensitive nested data", () => {
    const detail = parseTicketSource(ticketWire(), "alpha-board");

    expect(detail).toMatchObject({
      boardSlug: "alpha-board",
      taskId: "t_alpha01",
      dependencies: { phase: "ready" },
      comments: { phase: "ready" },
      attachments: { phase: "ready" },
      events: { phase: "ready" },
      runs: { phase: "ready" },
      diagnostics: { phase: "ready" },
    });
    expect(detail?.comments.items[0].body).toContain("token=[redacted]");
    expect(detail?.comments.items[0].body).toContain("[redacted path]");
    expect(detail?.attachments.items[0]).toEqual(expect.objectContaining({
      sourceAttachmentId: 2,
      displayFilename: "evidence.txt",
      mediaType: "text/plain",
      sizeBytes: 42,
    }));
    expect(detail?.events.items[0]).toEqual(expect.objectContaining({ label: "commented" }));
    expect(detail?.runs.items[0]).toEqual(expect.objectContaining({
      sourceRunId: 4,
      sourceStatus: "completed",
      sourceLabel: "Hermes Kanban run",
    }));
    expect(detail?.diagnostics.items[0].message).toContain("repeated source-run failures");
    const serialized = JSON.stringify(detail);
    for (const forbidden of [
      "comment-secret", "private\\comment", "stored_path", "private\\attachments",
      "private-command", "private-oauth", "private result", "private-claim",
      "private-run-error", "/home/private", "private-stack", "rm -rf", "worker_pid",
    ]) expect(serialized).not.toContain(forbidden);
    expect(Object.isFrozen(detail)).toBe(true);
    expect(Object.isFrozen(detail?.comments.items)).toBe(true);
  });

  it("models empty and unavailable optional sections independently", () => {
    const empty = parseTicketSource(ticketWire({
      links: { parents: [], children: [] },
      comments: [],
      attachments: [],
      events: [],
      runs: [],
      task: { ...task() },
    }), "alpha-board");
    expect([
      empty?.dependencies.phase,
      empty?.comments.phase,
      empty?.attachments.phase,
      empty?.events.phase,
      empty?.runs.phase,
      empty?.diagnostics.phase,
    ]).toEqual(["empty", "empty", "empty", "empty", "empty", "empty"]);

    const unavailable = parseTicketSource(ticketWire({ comments: "not-an-array" }), "alpha-board");
    expect(unavailable?.comments.phase).toBe("unavailable");
    expect(unavailable?.events.phase).toBe("ready");
  });

  it("fails closed on malformed, unsafe, negative, and overlong core values", () => {
    expect(parseProjectsSource(null)).toBeNull();
    expect(parseProjectsSource({ boards: "invalid" })).toBeNull();
    expect(parseProjectsSource({ boards: [board({ counts: { todo: -1 } })] })).toBeNull();
    expect(parseProjectSource(boardWire([task({ priority: Number.MAX_SAFE_INTEGER + 1 })]), projectSummary())).toBeNull();
    expect(parseTicketSource(ticketWire({ task: task({ title: "x".repeat(301) }) }), "alpha-board")).toBeNull();
    expect(parseTicketSource(ticketWire({ task: task({ body: "x".repeat(20_001) }) }), "alpha-board")).toBeNull();
  });

  it("validates route identities before encoding or lookup", () => {
    expect(validateBoardSlug("Alpha_Board")).toBe("alpha_board");
    expect(validateTaskId("t_ABC-123.test")).toBe("t_ABC-123.test");
    expect(validateProfileName("review.profile-1")).toBe("review.profile-1");
    for (const unsafe of ["../alpha", "C:\\alpha", "/alpha", "alpha/child", "alpha%2fchild", "alpha\nchild", ""]) {
      expect(validateBoardSlug(unsafe)).toBeNull();
      expect(validateTaskId(unsafe)).toBeNull();
    }
  });

  it("keeps equal task IDs distinct through board-qualified identity", () => {
    const alpha = parseTicketSource(ticketWire(), "alpha-board")!;
    const beta = parseTicketSource(ticketWire(), "beta-board")!;
    expect(alpha.taskId).toBe(beta.taskId);
    expect(`${alpha.boardSlug}:${alpha.taskId}`).not.toBe(`${beta.boardSlug}:${beta.taskId}`);
  });
});

describe("GET-only Kanban client boundary", () => {
  it("reuses authenticated fetchJSON with explicit profile, board, and task scope", async () => {
    vi.stubGlobal("window", { __HERMES_SESSION_TOKEN__: "synthetic-session" });
    const requests: Array<{ input: string; init?: RequestInit }> = [];
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      requests.push({ input: String(input), init });
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    }));

    await listProjectsSource("review-profile");
    await getProjectSource("alpha-board", "review-profile");
    await getTicketSource("alpha-board", "t_alpha01", "review-profile");

    expect(requests.map((request) => request.input)).toEqual([
      "/api/plugins/kanban/boards?include_archived=false&profile=review-profile",
      "/api/plugins/kanban/board?board=alpha-board&include_archived=false&profile=review-profile",
      "/api/plugins/kanban/tasks/t_alpha01?board=alpha-board&profile=review-profile",
    ]);
    for (const request of requests) {
      expect(request.init?.method).toBeUndefined();
      expect(request.input).not.toMatch(/dispatch|worker|swarm|decompose|reclaim/);
      expect(new Headers(request.init?.headers).get("X-Hermes-Session-Token")).toBe("synthetic-session");
    }
  });

  it("does not issue requests for invalid route identifiers", async () => {
    vi.stubGlobal("window", {});
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    await expect(getProjectSource("../escape", "default")).resolves.toBeNull();
    await expect(getTicketSource("alpha-board", "../escape", "default")).resolves.toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(buildProjectPath("../escape", "default")).toBeNull();
    expect(buildTicketPath("alpha-board", "../escape", "default")).toBeNull();
  });

  it("builds activated Projects and Ticket routes without calling Kanban source APIs", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    expect(buildProjectsPath("review-profile")).toBe("/agent-platform/projects?profile=review-profile");
    expect(buildProjectPath("alpha-board", "review-profile")).toBe(
      "/agent-platform/projects/alpha-board?profile=review-profile",
    );
    expect(buildTicketPath("alpha-board", "t_alpha01", "review-profile")).toBe(
      "/agent-platform/projects/alpha-board/tickets/t_alpha01?profile=review-profile",
    );
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("builds the legacy Kanban source path only as outbound navigation", () => {
    expect(buildKanbanSourcePath("alpha-board", "review-profile")).toBe(
      "/kanban?board=alpha-board&profile=review-profile",
    );
    expect(buildKanbanSourcePath("../escape", "review-profile")).toBeNull();
    expect(buildKanbanSourcePath("alpha-board", "../escape")).toBeNull();
  });

  it("keeps a missing board unavailable without process-current fallback", async () => {
    vi.stubGlobal("window", {});
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      expect(String(input)).toContain("/boards?");
      expect(init?.method).toBeUndefined();
      return new Response(JSON.stringify(boardsWire()), { status: 200 });
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(loadProjectsWorkspaceRequest({ kind: "project", boardSlug: "missing-board" }, "default"))
      .resolves.toBeNull();
    expect(fetchMock).toHaveBeenCalledOnce();
    expect(String(fetchMock.mock.calls[0][0])).toContain("/boards?");
  });

  it("keeps a missing task unavailable in its selected board without cross-board retry", async () => {
    vi.stubGlobal("window", {});
    const fetchMock = vi
      .fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>()
      .mockResolvedValueOnce(new Response(JSON.stringify(boardsWire()), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ detail: "not found" }), { status: 404 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(loadProjectsWorkspaceRequest(
      { kind: "ticket", boardSlug: "alpha-board", taskId: "t_missing" },
      "default",
    )).resolves.toBeNull();
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(String(fetchMock.mock.calls[1][0])).toContain("tasks/t_missing?board=alpha-board");
  });

});

describe("workspace polling and identity freshness", () => {
  it("polls recursively, prevents overlap, and retains the last success as stale", async () => {
    const scheduled: Array<() => void> = [];
    const states: ProjectsWorkspaceDataState[] = [];
    let resolveFirst: (value: ProjectsWorkspaceView | null) => void = () => {};
    const load = vi
      .fn<() => Promise<ProjectsWorkspaceView | null>>()
      .mockImplementationOnce(() => new Promise((resolve) => { resolveFirst = resolve; }))
      .mockRejectedValueOnce(new Error("raw private failure"));
    const poller = createProjectsWorkspacePoller(load, (next) => states.push(next), {
      now: () => 1234,
      setTimer: (callback, delay) => {
        expect(delay).toBe(PROJECTS_WORKSPACE_POLL_MS);
        scheduled.push(callback);
        return callback;
      },
      clearTimer: () => {},
    });

    const first = poller.start();
    expect(await poller.refresh()).toBe(false);
    expect(load).toHaveBeenCalledOnce();
    resolveFirst(projectsView());
    expect(await first).toBe(true);
    expect(states.at(-1)).toMatchObject({ phase: "ready", lastSuccessAt: 1234 });
    const snapshot = states.at(-1)?.snapshot;
    scheduled.shift()?.();
    await vi.waitFor(() => expect(states.at(-1)?.phase).toBe("stale"));
    expect(states.at(-1)?.snapshot).toBe(snapshot);
    expect(JSON.stringify(states)).not.toContain("raw private failure");
    poller.stop();
  });

  it("distinguishes empty, unavailable, and initial error states", async () => {
    const states: ProjectsWorkspaceDataState[] = [];
    const run = async (load: () => Promise<ProjectsWorkspaceView | null>) => {
      const poller = createProjectsWorkspacePoller(load, (next) => states.push(next));
      await poller.start();
      poller.stop();
      return states.at(-1)?.phase;
    };
    expect(await run(async () => ({ kind: "projects", projects: [] }))).toBe("empty");
    expect(await run(async () => null)).toBe("unavailable");
    expect(await run(async () => { throw new Error("not retained"); })).toBe("error");
  });

  it("suppresses late responses after stop and keys every profile and route identity", async () => {
    const states: ProjectsWorkspaceDataState[] = [];
    let resolveLoad: (value: ProjectsWorkspaceView | null) => void = () => {};
    const poller = createProjectsWorkspacePoller(
      () => new Promise((resolve) => { resolveLoad = resolve; }),
      (next) => states.push(next),
    );
    const pending = poller.start();
    poller.stop();
    resolveLoad(projectsView());
    expect(await pending).toBe(false);
    expect(states).toEqual([]);

    const keys = new Set([
      projectsWorkspaceRequestKey({ kind: "projects" }, "default"),
      projectsWorkspaceRequestKey({ kind: "projects" }, "other"),
      projectsWorkspaceRequestKey({ kind: "project", boardSlug: "alpha" }, "default"),
      projectsWorkspaceRequestKey({ kind: "project", boardSlug: "beta" }, "default"),
      projectsWorkspaceRequestKey({ kind: "ticket", boardSlug: "alpha", taskId: "t_one" }, "default"),
      projectsWorkspaceRequestKey({ kind: "ticket", boardSlug: "alpha", taskId: "t_two" }, "default"),
    ]);
    expect(keys.size).toBe(6);
  });
});

describe("read-only workspace pages", () => {
  it("renders source-qualified Projects, filters, and profile-preserving links", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <ProjectsView state={state(projectsView())} profile="review-profile" refresh={() => {}} />
      </MemoryRouter>,
    );
    expect(markup).toContain("Source: Hermes Kanban");
    expect(markup).toContain("Authority: Provisional");
    expect(markup).toContain("alpha-board");
    expect(markup).toContain("/agent-platform/projects/alpha-board?profile=review-profile");
    expect(markup).toContain("/kanban?board=alpha-board&amp;profile=review-profile");
    expect(markup).toContain("Paperclip remains the future");
    for (const control of ["Create Project", "Delete Project", "Import Project", "Start Work", "Assign Agent"]) {
      expect(markup).not.toContain(control);
    }
  });

  it("renders Projects empty, stale, error, and unavailable states explicitly", () => {
    const empty = renderToStaticMarkup(<MemoryRouter><ProjectsView state={state({ kind: "projects", projects: [] }, "empty")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const stale = renderToStaticMarkup(<MemoryRouter><ProjectsView state={state(projectsView(), "stale")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const error = renderToStaticMarkup(<MemoryRouter><ProjectsView state={state(null, "error")} profile="default" refresh={() => {}} /></MemoryRouter>);
    const unavailable = renderToStaticMarkup(<MemoryRouter><ProjectsView state={state(null, "unavailable")} profile="default" refresh={() => {}} /></MemoryRouter>);
    expect(empty).toContain("returned no boards");
    expect(stale).toContain("Showing the last validated");
    expect(error).toContain("could not be reached");
    expect(unavailable).toContain("Projects source unavailable");
  });

  it("renders board-qualified Ticket links and source-state semantic disclaimers", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <ProjectDetailView state={state(projectView())} profile="default" refresh={() => {}} />
      </MemoryRouter>,
    );
    expect(markup).toContain("Hermes Kanban board alpha-board");
    expect(markup).toContain("Hermes priority: 7");
    expect(markup).toContain("/agent-platform/projects/alpha-board/tickets/t_alpha01?profile=default");
    expect(markup).toContain("not an ApprovalRequest");
    expect(markup).toContain("not executable here");
    for (const control of ["drag", "Change status", "Assign", "Delete", "Edit"] ) {
      expect(markup).not.toContain(`>${control}<`);
    }
  });

  it("renders Ticket plain text and independent safe detail sections without write controls", () => {
    const raw = ticketWire({
      task: { ...task({ title: "<script>Unsafe title</script>", body: "**plain markdown** <img src=x>" }) },
    });
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <TicketDetailView state={state(ticketView(raw))} profile="default" refresh={() => {}} />
      </MemoryRouter>,
    );
    expect(markup).toContain("&lt;script&gt;Unsafe title&lt;/script&gt;");
    expect(markup).toContain("**plain markdown** &lt;img src=x&gt;");
    expect(markup).toContain("Parent and dependencies");
    expect(markup).toContain("Comments");
    expect(markup).toContain("Attachment metadata");
    expect(markup).toContain("Events");
    expect(markup).toContain("Hermes run summaries");
    expect(markup).toContain("Diagnostics");
    expect(markup).toContain("not a WorkPacket");
    expect(markup).not.toContain("comment-secret");
    expect(markup).not.toContain("private\\");
    for (const control of ["Approve", "Reject", "Retry", "Reclaim", "Change status", "Upload", "Download", "Add comment"] ) {
      expect(markup).not.toContain(`>${control}<`);
    }
  });

  it("renders independently empty and unavailable Ticket sections", () => {
    const detail = parseTicketSource(ticketWire({
      task: { ...task() },
      links: { parents: [], children: [] },
      comments: [],
      attachments: "unavailable",
      events: [],
      runs: [],
    }), "alpha-board")!;
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <TicketDetailView state={state({ kind: "ticket", ticket: detail })} profile="default" refresh={() => {}} />
      </MemoryRouter>,
    );
    expect(markup).toContain("No source comments");
    expect(markup).toContain("optional source section cannot be projected safely");
  });
});

describe("Projects and Tickets descriptors", () => {
  it("declares three deterministic contextual routes with one navigation entry", () => {
    expect(PROJECTS_TICKETS_DESCRIPTORS).toEqual([
      PROJECTS_DESCRIPTOR,
      PROJECT_DETAIL_DESCRIPTOR,
      TICKET_DETAIL_DESCRIPTOR,
    ]);
    expect(PROJECTS_TICKETS_DESCRIPTORS.map((descriptor) => [
      descriptor.id,
      descriptor.route.path,
      descriptor.navigation?.label,
    ])).toEqual([
      ["agent_platform.ui.projects", "/agent-platform/projects", "Projects"],
      ["agent_platform.ui.project_detail", "/agent-platform/projects/:boardSlug", undefined],
      ["agent_platform.ui.ticket_detail", "/agent-platform/projects/:boardSlug/tickets/:taskId", undefined],
    ]);
    expect(PROJECTS_TICKETS_DESCRIPTORS.every((descriptor) =>
      descriptor.owner === "AGENT_PLATFORM" &&
      descriptor.featureId === "agent_platform.product_ui" &&
      descriptor.visibleWhenExperimental)).toBe(true);
  });

  it("exposes the loading state without source data", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <ProjectsView state={INITIAL_PROJECTS_WORKSPACE_STATE} profile="default" refresh={() => {}} />
      </MemoryRouter>,
    );
    expect(markup).toContain("Loading Hermes Kanban source");
    expect(markup).toContain("aria-busy=\"true\"");
  });
});
