import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import { RUNTIME_OVERVIEW_DESCRIPTOR } from "./descriptor";
import { parseRuntimeOverviewSnapshot } from "./contract";
import { RuntimeOverviewView } from "./runtime-overview-page";
import {
  createRuntimeOverviewPoller,
  INITIAL_RUNTIME_OVERVIEW_STATE,
  RUNTIME_OVERVIEW_POLL_MS,
  type RuntimeOverviewState,
} from "./use-runtime-overview";

function statusResponse(overrides: Record<string, unknown> = {}) {
  return {
    version: "0.19.0",
    release_date: "2026.7.7.2",
    config_version: 33,
    latest_config_version: 33,
    can_update_hermes: true,
    gateway_running: false,
    gateway_state: null,
    gateway_platforms: {},
    gateway_exit_reason: null,
    gateway_updated_at: null,
    active_agents: 0,
    gateway_busy: false,
    gateway_drainable: false,
    restart_drain_timeout: 0,
    active_sessions: 0,
    auth_required: false,
    auth_providers: [],
    nous_session_valid: "unknown",
    profiles: ["default"],
    gateway_mode: "none",
    hermes_home: "C:\\private\\runtime",
    config_path: "C:\\private\\runtime\\config.yaml",
    env_path: "C:\\private\\runtime\\.env",
    gateway_pid: null,
    gateway_health_url: null,
    gateways: [],
    secret: "must-not-survive",
    ...overrides,
  };
}

describe("Runtime Overview contract", () => {
  it("projects only bounded platform, gateway, activity, and access fields", () => {
    const parsed = parseRuntimeOverviewSnapshot(statusResponse());

    expect(parsed).toEqual({
      platform: {
        version: "0.19.0",
        releaseDate: "2026.7.7.2",
        configVersion: 33,
        latestConfigVersion: 33,
        updateAvailable: false,
      },
      gateway: { state: "off", running: false, busy: false, drainable: false },
      activity: { activeSessions: 0, activeAgents: 0 },
      access: { authRequired: false },
      workflowControl: null,
    });
    const retained = JSON.stringify(parsed);
    expect(retained).not.toContain("private");
    expect(retained).not.toContain("must-not-survive");
    expect(retained).not.toContain("auth_providers");
    expect(retained).not.toContain("profiles");
    expect(Object.isFrozen(parsed)).toBe(true);
    expect(Object.values(parsed ?? {}).every(Object.isFrozen)).toBe(true);
  });

  it("fails closed on malformed or incomplete status responses", () => {
    expect(parseRuntimeOverviewSnapshot(null)).toBeNull();
    expect(parseRuntimeOverviewSnapshot([])).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({ active_sessions: -1 }))).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({ auth_required: "false" }))).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({ version: "" }))).toBeNull();
  });
});

describe("Runtime Overview polling", () => {
  it("polls recursively, retains the last success, and marks later failure stale", async () => {
    const scheduled: Array<() => void> = [];
    const states: RuntimeOverviewState[] = [];
    const load = vi
      .fn<() => Promise<unknown>>()
      .mockResolvedValueOnce(statusResponse())
      .mockRejectedValueOnce(new Error("private transport detail"));
    const poller = createRuntimeOverviewPoller(load, (state) => states.push(state), {
      now: () => 1234,
      setTimer: (callback, delay) => {
        expect(delay).toBe(RUNTIME_OVERVIEW_POLL_MS);
        scheduled.push(callback);
        return callback;
      },
      clearTimer: (timer) => {
        const index = scheduled.indexOf(timer as () => void);
        if (index >= 0) scheduled.splice(index, 1);
      },
    });

    expect(await poller.start()).toBe(true);
    expect(states.at(-1)).toMatchObject({ phase: "ready", lastSuccessAt: 1234 });
    const firstSnapshot = states.at(-1)?.snapshot;
    scheduled.shift()?.();
    await vi.waitFor(() => expect(load).toHaveBeenCalledTimes(2));
    await vi.waitFor(() => expect(states.at(-1)?.phase).toBe("stale"));
    expect(states.at(-1)?.snapshot).toBe(firstSnapshot);
    expect(JSON.stringify(states)).not.toContain("private transport detail");
    poller.stop();
  });

  it("prevents overlapping refreshes and publishes nothing after stop", async () => {
    let resolveLoad: (value: unknown) => void = () => {};
    const states: RuntimeOverviewState[] = [];
    const load = vi.fn(() => new Promise<unknown>((resolve) => { resolveLoad = resolve; }));
    const poller = createRuntimeOverviewPoller(load, (state) => states.push(state));

    const initial = poller.start();
    expect(await poller.refresh()).toBe(false);
    expect(load).toHaveBeenCalledTimes(1);
    poller.stop();
    resolveLoad(statusResponse());
    expect(await initial).toBe(false);
    expect(states).toEqual([]);
  });

  it("distinguishes unavailable data from an initial transport error", async () => {
    const states: RuntimeOverviewState[] = [];
    const unavailable = createRuntimeOverviewPoller(
      async () => ({ unexpected: true }),
      (state) => states.push(state),
    );
    await unavailable.start();
    unavailable.stop();
    expect(states.at(-1)?.phase).toBe("unavailable");

    const error = createRuntimeOverviewPoller(
      async () => { throw new Error("not rendered"); },
      (state) => states.push(state),
    );
    await error.start();
    error.stop();
    expect(states.at(-1)?.phase).toBe("error");
  });
});

describe("Runtime Overview surface and descriptor", () => {
  it("declares the reviewed product-owned route and navigation metadata", () => {
    expect(RUNTIME_OVERVIEW_DESCRIPTOR).toMatchObject({
      id: "agent_platform.ui.overview",
      owner: "AGENT_PLATFORM",
      featureId: "agent_platform.product_ui",
      visibleWhenExperimental: true,
      route: { path: "/agent-platform/overview", title: "Runtime Overview" },
      navigation: { groupId: "agent-platform", label: "Overview", placement: { kind: "end" } },
    });
  });

  it("renders accessible loading and provider-null ready states", () => {
    const loading = renderToStaticMarkup(
      <RuntimeOverviewView state={INITIAL_RUNTIME_OVERVIEW_STATE} refresh={() => {}} />,
    );
    expect(loading).toContain("Runtime Overview");
    expect(loading).toContain("aria-busy=\"true\"");

    const snapshot = parseRuntimeOverviewSnapshot(statusResponse())!;
    const ready = renderToStaticMarkup(
      <RuntimeOverviewView
        state={{ phase: "ready", snapshot, lastSuccessAt: 1234, refreshing: false }}
        refresh={() => {}}
      />,
    );
    expect(ready).toContain("Offline");
    expect(ready).toContain("Recent sessions");
    expect(ready).toContain("not governed AGENT PLATFORM Agents");
    expect(ready).not.toContain("private");
  });

  it("renders controlled default-mode workflow control when present", () => {
    const snapshot = parseRuntimeOverviewSnapshot(statusResponse({
      agent_platform_workflow_control: {
        product_id: "pepper",
        project_id: "PEPPER",
        project_name: "Pepper",
        macroproject_id: "P18.9",
        current_ticket_id: null,
        current_ticket_title: null,
        mode: "controlled_default",
        readiness: "planning_approved_or_intake_ready",
        workflow_state: "P18.9-PEPPER-PRODUCT-PERSONALIZATION-INTAKE-READY",
        workflow_status: "planning_approved_or_intake_ready",
        approval_state: "no_pending_approvals",
        pending_approval_count: 0,
        queue_state: "ready_to_generate_P18_9_0",
        execution_state: "no_active_executions",
        active_execution_count: 0,
        validation_state: "not_started_no_ticket_generated",
        review_state: "not_started_no_ticket_generated",
        recovery_state: "not_required",
        git_handoff_state: "human_git_authority_preserved",
        default_mode_enabled: true,
        manual_chat_control_required: false,
        manual_opencode_ticket_copy_required: false,
        manual_opencode_result_copy_required: false,
        human_git_authority: "preserved_manual_git_add_commit_push_only",
        ready_requires_human_smoke: false,
        closed_gaps: [
          { id: "P18-8-GAP-001" },
          { id: "P18-8-GAP-002" },
          { id: "P18-8-GAP-003" },
          { id: "P18-8-GAP-004" },
          { id: "P18-8-GAP-005" },
        ],
        remaining_blockers: [],
        next_action: { label: "Generate governed P18.9.0 Product UX / IA Baseline before execution." },
      },
    }))!;
    const ready = renderToStaticMarkup(
      <RuntimeOverviewView
        state={{ phase: "ready", snapshot, lastSuccessAt: 1234, refreshing: false }}
        refresh={() => {}}
      />,
    );
    expect(ready).toContain("Pepper Workflow Control");
    expect(ready).toContain("PEPPER");
    expect(ready).toContain("None generated");
    expect(ready).toContain("Pending approvals");
    expect(ready).toContain("Active executions");
    expect(ready).toContain("Generate governed P18.9.0");
    expect(ready).toContain("Manual OpenCode copy");
    expect(ready).toContain("Remaining blockers");
  });
});
