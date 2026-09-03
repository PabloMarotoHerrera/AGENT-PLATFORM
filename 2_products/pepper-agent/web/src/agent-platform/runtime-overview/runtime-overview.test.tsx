import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import { RUNTIME_OVERVIEW_DESCRIPTOR } from "./descriptor";
import { parseRuntimeOverviewSnapshot } from "./contract";
import { RuntimeOverviewView } from "./runtime-overview-page";
import { ChatSidebarGovernedContext } from "@/components/ChatSidebar";
import {
  createRuntimeOverviewPoller,
  INITIAL_RUNTIME_OVERVIEW_STATE,
  RUNTIME_OVERVIEW_POLL_MS,
  type RuntimeOverviewState,
} from "./use-runtime-overview";

function workflowControl(overrides: Record<string, unknown> = {}) {
  return {
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
    pending_ticket_approval_count: 0,
    queue_state: "ready_to_generate_P18_9_0",
    execution_state: "no_active_executions",
    execution_count: 0,
    active_execution_count: 0,
    validation_state: "not_started_no_ticket_generated",
    review_state: "not_started_no_ticket_generated",
    review_decision_recorded: false,
    review_decision_required: false,
    human_acceptance_required: false,
    human_acceptance_recorded: false,
    recovery_state: "not_required",
    failure_category: null,
    failure_summary: null,
    git_handoff_state: "human_git_authority_preserved",
    git_handoff_required: false,
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
    blocker_count: 0,
    warning_count: 0,
    next_action: {
      id: "P18.9.0-next-ticket-generation",
      label: "Generate governed P18.9.0 Product UX / IA Baseline before execution.",
      target_ticket_id: "P18.9.0",
      target_ticket_title: "Product UX / IA Baseline",
      required_human_action: "ticket_generation",
    },
    ...overrides,
  };
}

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

function renderReady(controlOverrides: Record<string, unknown> = {}, statusOverrides: Record<string, unknown> = {}) {
  const snapshot = parseRuntimeOverviewSnapshot(statusResponse({
    agent_platform_workflow_control: workflowControl(controlOverrides),
    ...statusOverrides,
  }))!;
  return renderToStaticMarkup(
    <RuntimeOverviewView
      state={{ phase: "ready", snapshot, lastSuccessAt: 1234, refreshing: false }}
      refresh={() => {}}
    />,
  );
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

  it("projects bounded workflow-control fields including canonical action and human action", () => {
    const parsed = parseRuntimeOverviewSnapshot(statusResponse({
      agent_platform_workflow_control: workflowControl(),
    }));

    expect(parsed?.workflowControl).toMatchObject({
      projectId: "PEPPER",
      pendingApprovalCount: 0,
      pendingTicketApprovalCount: 0,
      executionCount: 0,
      reviewDecisionRecorded: false,
      gitHandoffRequired: false,
      blockerCount: 0,
      warningCount: 0,
      nextActionId: "P18.9.0-next-ticket-generation",
      nextActionRequiredHumanAction: "ticket_generation",
      nextActionTargetTicketId: "P18.9.0",
    });
  });

  it("falls back to pending approval count when ticket-specific approval count is absent", () => {
    const control = workflowControl({ pending_approval_count: 2 });
    delete (control as { pending_ticket_approval_count?: unknown }).pending_ticket_approval_count;

    expect(parseRuntimeOverviewSnapshot(statusResponse({
      agent_platform_workflow_control: control,
    }))?.workflowControl?.pendingTicketApprovalCount).toBe(2);
  });

  it("fails closed on malformed or incomplete status responses", () => {
    expect(parseRuntimeOverviewSnapshot(null)).toBeNull();
    expect(parseRuntimeOverviewSnapshot([])).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({ active_sessions: -1 }))).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({ auth_required: "false" }))).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({ version: "" }))).toBeNull();
    expect(parseRuntimeOverviewSnapshot(statusResponse({
      agent_platform_workflow_control: workflowControl({ next_action: { label: "missing governed action id" } }),
    }))?.workflowControl).toBeNull();
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
    expect(loading).toContain("Control Center Overview");
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
    expect(ready).toContain("Workflow-control unavailable");
    expect(ready).not.toContain("private");
  });

  it("answers the five required Control Center overview questions", () => {
    const ready = renderReady({
      current_ticket_id: "P18.9.2",
      current_ticket_title: "Control Center Overview",
    });

    expect(ready).toContain("Current Work");
    expect(ready).toContain("P18.9.2: Control Center Overview");
    expect(ready).toContain("Next Governed Action");
    expect(ready).toContain("Canonical action ID");
    expect(ready).toContain("P18.9.0-next-ticket-generation");
    expect(ready).toContain("Required human action");
    expect(ready).toContain("ticket_generation");
    expect(ready).toContain("Needs Attention");
    expect(ready).toContain("Execution");
    expect(ready).toContain("Governed State");
  });

  it("renders idle execution and no-current-work state", () => {
    const ready = renderReady();

    expect(ready).toContain("No current governed ticket is active.");
    expect(ready).toContain("No active executions are running.");
    expect(ready).toContain("No human-attention condition is currently raised.");
    expect(ready).toContain("Idle");
  });

  it("renders the Lead Agent sidebar governed workflow fields from backend projection", () => {
    const snapshot = parseRuntimeOverviewSnapshot(statusResponse({
      agent_platform_workflow_control: workflowControl({
        current_ticket_id: "P18.9.3",
        current_ticket_title: "Lead Agent Product Experience",
        workflow_status: "human_review_changes_requested",
        workflow_state: "P18.9-LEAD-AGENT-CORRECTION-RUNNING",
        recovery_state: "fresh_execution_after_review",
        execution_state: "retry_execution_in_flight",
        manual_chat_control_required: true,
        next_action: {
          id: "P18.9.3-render-workflow-context",
          label: "Render backend-projected workflow fields in Pepper Lead Agent context.",
          target_ticket_id: "P18.9.3",
          target_ticket_title: "Lead Agent Product Experience",
          required_human_action: "human_review_decision",
        },
      }),
    }))!;

    const ready = renderToStaticMarkup(
      <ChatSidebarGovernedContext workflowControl={snapshot.workflowControl} />,
    );

    expect(ready).toContain("Governed workflow context");
    expect(ready).toContain("Presentation-only view of the backend-projected runtime workflow-control read model.");
    expect(ready).toContain("P18.9.3: Lead Agent Product Experience");
    expect(ready).toContain("Workflow status");
    expect(ready).toContain("human_review_changes_requested");
    expect(ready).toContain("Workflow state");
    expect(ready).toContain("P18.9-LEAD-AGENT-CORRECTION-RUNNING");
    expect(ready).toContain("Recovery state");
    expect(ready).toContain("fresh_execution_after_review");
    expect(ready).toContain("P18.9.3-render-workflow-context");
    expect(ready).toContain("human_review_decision");
    expect(ready).toContain("retry_execution_in_flight");
    expect(ready).toContain("Manual chat control");
    expect(ready).toContain("Required");
    expect(ready).not.toContain("model switch");
  });

  it("renders active execution summary", () => {
    const ready = renderReady({
      execution_state: "executing",
      execution_count: 3,
      active_execution_count: 2,
    }, {
      gateway_running: true,
      gateway_state: "running",
      gateway_busy: true,
      active_agents: 2,
    });

    expect(ready).toContain("Running");
    expect(ready).toContain("Gateway work is currently in flight.");
    expect(ready).toContain("2 active execution(s); 3 total recorded.");
    expect(ready).toContain("Active");
  });

  it("renders human-attention and review-pending states", () => {
    const ready = renderReady({
      approval_state: "pending_ticket_approval",
      pending_approval_count: 1,
      pending_ticket_approval_count: 1,
      review_state: "pending_human_review",
      review_decision_required: true,
      human_acceptance_required: true,
      human_acceptance_recorded: false,
      ready_requires_human_smoke: true,
      next_action: {
        id: "P18.9.2-review-decision",
        label: "Human review decision is required before Git handoff.",
        target_ticket_id: "P18.9.2",
        target_ticket_title: "Control Center Overview",
        required_human_action: "human_review_decision",
      },
    });

    expect(ready).toContain("ticket approval pending; review decision required; human acceptance required; human smoke check required");
    expect(ready).toContain("pending_ticket_approval");
    expect(ready).toContain("human_review_decision");
    expect(ready).toContain("Decision recorded: No");
  });

  it("renders blocked recovery state", () => {
    const ready = renderReady({
      recovery_state: "blocked_recovery_required",
      failure_category: "validation_failure",
      failure_summary: "Validation failed and requires governed retry authorization.",
      remaining_blockers: [{ id: "B-1" }],
      blocker_count: 1,
      warning_count: 2,
      next_action: {
        id: "P18.9.2-retry-start",
        label: "Authorize retry start after recovery review.",
        target_ticket_id: "P18.9.2",
        target_ticket_title: "Control Center Overview",
        required_human_action: "retry_start_authorization",
      },
    });

    expect(ready).toContain("blockers remain; recovery evidence present");
    expect(ready).toContain("blocked_recovery_required");
    expect(ready).toContain("Validation failed and requires governed retry authorization.");
    expect(ready).toContain("retry_start_authorization");
    expect(ready).toContain("Warnings");
  });

  it("renders Git handoff state without implementing handoff UX", () => {
    const ready = renderReady({
      git_handoff_state: "awaiting_human_git_handoff",
      git_handoff_required: true,
      human_git_authority: "human_only_git_add_commit_push",
      next_action: {
        id: "P18.9.2-git-handoff",
        label: "Human Git handoff is required after review acceptance.",
        target_ticket_id: "P18.9.2",
        target_ticket_title: "Control Center Overview",
        required_human_action: "human_git_handoff",
      },
    });

    expect(ready).toContain("Git handoff required");
    expect(ready).toContain("awaiting_human_git_handoff");
    expect(ready).toContain("human_only_git_add_commit_push");
    expect(ready).toContain("human_git_handoff");
  });

  it("renders unavailable and error empty states", () => {
    const unavailable = renderToStaticMarkup(
      <RuntimeOverviewView state={{ phase: "unavailable", snapshot: null, lastSuccessAt: null, refreshing: false }} refresh={() => {}} />,
    );
    expect(unavailable).toContain("Runtime status unavailable");
    expect(unavailable).toContain("The service responded without the bounded status fields this overview requires.");

    const error = renderToStaticMarkup(
      <RuntimeOverviewView state={{ phase: "error", snapshot: null, lastSuccessAt: null, refreshing: false }} refresh={() => {}} />,
    );
    expect(error).toContain("Runtime status could not be reached");
    expect(error).toContain("No runtime details are shown until a validated status response succeeds.");
  });
});
