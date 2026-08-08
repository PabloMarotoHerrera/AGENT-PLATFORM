import type { ComponentType } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  AGENT_PLATFORM_EXTENSIONS,
  mergeProductNavigation,
  resolveRegisteredProductExtensions,
} from "./extensions";
import { loadProjectsWorkspaceRequest } from "./projects-tickets";
import { parseProductConfiguration } from "./product-config";

const Icon: ComponentType<{ className?: string }> = () => null;
const ACTIVATED_PRODUCT_EXTENSION_IDS = Object.freeze([
  "agent_platform.ui.overview",
  "agent_platform.ui.projects",
  "agent_platform.ui.project_detail",
  "agent_platform.ui.ticket_detail",
  "agent_platform.ui.approvals",
  "agent_platform.ui.approval_detail",
  "agent_platform.ui.executions",
  "agent_platform.ui.execution_detail",
  "agent_platform.ui.settings",
]);

function productConfiguration(extensionModules: readonly string[]) {
  return parseProductConfiguration({
    schema_version: 1,
    product_id: "pepper",
    product_display_name: "Pepper",
    product_version: "0.1.0-dev",
    upstream_product_name: "Hermes Agent",
    upstream_version: "0.19.0",
    upstream_commit: "3ef6bbd201263d354fd83ec55b3c306ded2eb72a",
    feature_flags: { "agent_platform.product_ui": "enabled" },
    extension_modules: extensionModules,
    documentation_url: null,
    support_url: null,
  });
}

function board(overrides: Record<string, unknown> = {}) {
  return {
    slug: "alpha-board",
    name: "Alpha Project",
    description: "Source-qualified project description",
    counts: { todo: 1, scheduled: 1, done: 1 },
    total: 3,
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
    link_counts: { parents: 0, children: 1 },
    ...overrides,
  };
}

function boardsWire() {
  return { boards: [board()], current: "default" };
}

function boardWire() {
  return {
    columns: [
      { name: "todo", tasks: [task()] },
      { name: "scheduled", tasks: [] },
      { name: "done", tasks: [] },
    ],
    tenants: [],
    assignees: [],
    latest_event_id: 3,
    now: 1_700_000_100,
  };
}

function ticketWire() {
  return {
    task: task(),
    links: { parents: [], children: [] },
    comments: [],
    attachments: [],
    events: [],
    runs: [],
  };
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("P18.UI-A canonical activation evidence", () => {
  it("test_canonical_Pepper_product_UI_activation_flow", () => {
    const config = productConfiguration(ACTIVATED_PRODUCT_EXTENSION_IDS);
    const resolved = resolveRegisteredProductExtensions(config, ["/sessions", "/kanban"]);
    const navigation = mergeProductNavigation(
      [{ path: "/kanban", label: "Kanban", icon: Icon }],
      resolved,
    );

    expect(AGENT_PLATFORM_EXTENSIONS.map((extension) => extension.id)).toEqual(
      ACTIVATED_PRODUCT_EXTENSION_IDS,
    );
    expect(resolved.map((extension) => extension.route.path)).toEqual([
      "/agent-platform/overview",
      "/agent-platform/projects",
      "/agent-platform/projects/:boardSlug",
      "/agent-platform/projects/:boardSlug/tickets/:taskId",
      "/agent-platform/approvals",
      "/agent-platform/approvals/:approvalId",
      "/agent-platform/executions",
      "/agent-platform/executions/:executionId",
      "/agent-platform/settings",
    ]);
    expect(navigation.map((item) => item.path)).toContain("/agent-platform/projects");
    expect(navigation.map((item) => item.path)).toContain("/kanban");
    expect(new Set(navigation.map((item) => item.path)).size).toBe(navigation.length);
  });

  it("test_canonical_unapproved_extension_remains_inert", () => {
    const config = productConfiguration([
      "agent_platform.ui.projects",
      "agent_platform.ui.not_registered",
    ]);

    expect(resolveRegisteredProductExtensions(config, ["/sessions"]).map((extension) => extension.id))
      .toEqual(["agent_platform.ui.projects"]);
  });

  it("test_canonical_Projects_reuses_existing_Kanban_API", async () => {
    vi.stubGlobal("window", { __HERMES_SESSION_TOKEN__: "synthetic-session" });
    const requests: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      requests.push(String(input));
      expect(init?.method).toBeUndefined();
      expect(new Headers(init?.headers).get("X-Hermes-Session-Token")).toBe("synthetic-session");
      const url = String(input);
      if (url.startsWith("/api/plugins/kanban/boards?")) {
        return new Response(JSON.stringify(boardsWire()), { status: 200 });
      }
      if (url.startsWith("/api/plugins/kanban/board?")) {
        return new Response(JSON.stringify(boardWire()), { status: 200 });
      }
      if (url.startsWith("/api/plugins/kanban/tasks/t_alpha01?")) {
        return new Response(JSON.stringify(ticketWire()), { status: 200 });
      }
      return new Response(JSON.stringify({ detail: "unexpected" }), { status: 500 });
    }));

    await expect(loadProjectsWorkspaceRequest({ kind: "projects" }, "review-profile"))
      .resolves.toMatchObject({ kind: "projects" });
    await expect(loadProjectsWorkspaceRequest({ kind: "project", boardSlug: "alpha-board" }, "review-profile"))
      .resolves.toMatchObject({ kind: "project" });
    await expect(loadProjectsWorkspaceRequest(
      { kind: "ticket", boardSlug: "alpha-board", taskId: "t_alpha01" },
      "review-profile",
    )).resolves.toMatchObject({ kind: "ticket" });

    expect(requests).toEqual([
      "/api/plugins/kanban/boards?include_archived=false&profile=review-profile",
      "/api/plugins/kanban/boards?include_archived=false&profile=review-profile",
      "/api/plugins/kanban/board?board=alpha-board&include_archived=false&profile=review-profile",
      "/api/plugins/kanban/boards?include_archived=false&profile=review-profile",
      "/api/plugins/kanban/tasks/t_alpha01?board=alpha-board&profile=review-profile",
    ]);
    expect(requests.every((request) => request.startsWith("/api/plugins/kanban/"))).toBe(true);
    expect(requests.some((request) => request.startsWith("/api/agent-platform/projects"))).toBe(false);
  });
});
