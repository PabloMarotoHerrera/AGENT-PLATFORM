export type RuntimeGatewayState =
  | "off"
  | "running"
  | "starting"
  | "stopped"
  | "failed"
  | "unknown";

export interface RuntimeOverviewSnapshot {
  readonly platform: Readonly<{
    version: string;
    releaseDate: string;
    configVersion: number;
    latestConfigVersion: number;
    updateAvailable: boolean;
  }>;
  readonly gateway: Readonly<{
    state: RuntimeGatewayState;
    running: boolean;
    busy: boolean;
    drainable: boolean;
  }>;
  readonly activity: Readonly<{
    activeSessions: number;
    activeAgents: number;
  }>;
  readonly access: Readonly<{
    authRequired: boolean;
  }>;
  readonly workflowControl: RuntimeWorkflowControl | null;
}

export interface RuntimeWorkflowControl {
  readonly productId: string;
  readonly projectId: string;
  readonly projectName: string;
  readonly macroprojectId: string;
  readonly currentTicketId: string | null;
  readonly currentTicketTitle: string | null;
  readonly mode: string;
  readonly readiness: string;
  readonly workflowState: string;
  readonly workflowStatus: string;
  readonly approvalState: string;
  readonly pendingApprovalCount: number;
  readonly pendingTicketApprovalCount: number;
  readonly queueState: string;
  readonly executionState: string;
  readonly executionCount: number;
  readonly activeExecutionCount: number;
  readonly validationState: string;
  readonly reviewState: string;
  readonly reviewDecisionRecorded: boolean;
  readonly reviewDecisionRequired: boolean;
  readonly humanAcceptanceRequired: boolean;
  readonly humanAcceptanceRecorded: boolean;
  readonly recoveryState: string;
  readonly failureCategory: string | null;
  readonly failureSummary: string | null;
  readonly gitHandoffState: string;
  readonly gitHandoffRequired: boolean;
  readonly defaultModeEnabled: boolean;
  readonly manualChatControlRequired: boolean;
  readonly manualOpenCodeTicketCopyRequired: boolean;
  readonly manualOpenCodeResultCopyRequired: boolean;
  readonly humanGitAuthority: string;
  readonly readyRequiresHumanSmoke: boolean;
  readonly closedGapCount: number;
  readonly remainingBlockerCount: number;
  readonly blockerCount: number;
  readonly warningCount: number;
  readonly nextActionId: string;
  readonly nextActionLabel: string;
  readonly nextActionTargetTicketId: string | null;
  readonly nextActionTargetTicketTitle: string | null;
  readonly nextActionRequiredHumanAction: string;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function asBoundedString(value: unknown, maxLength: number): string | null {
  if (typeof value !== "string") return null;
  const normalized = value.trim();
  return normalized.length > 0 && normalized.length <= maxLength ? normalized : null;
}

function asOptionalBoundedString(value: unknown, maxLength: number): string | null | undefined {
  if (value === null || value === undefined) return null;
  return asBoundedString(value, maxLength) ?? undefined;
}

function asOptionalNullableString(value: unknown, maxLength: number): string | null {
  if (value === null || value === undefined) return null;
  return asBoundedString(value, maxLength) ?? null;
}

function asNonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0
    ? value
    : null;
}

function asOptionalNonNegativeInteger(value: unknown, fallback: number): number | null {
  if (value === null || value === undefined) return fallback;
  return asNonNegativeInteger(value);
}

function asBoolean(value: unknown): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function asOptionalBoolean(value: unknown, fallback: boolean): boolean | null {
  if (value === null || value === undefined) return fallback;
  return asBoolean(value);
}

function parseWorkflowControl(value: unknown): RuntimeWorkflowControl | null {
  const source = asRecord(value);
  const nextAction = asRecord(source?.next_action);
  if (!source || !nextAction) return null;
  const productId = asBoundedString(source.product_id, 128);
  const projectId = asBoundedString(source.project_id, 128);
  const projectName = asBoundedString(source.project_name, 128);
  const macroprojectId = asBoundedString(source.macroproject_id, 128);
  const currentTicketId = asOptionalBoundedString(source.current_ticket_id, 128);
  const currentTicketTitle = asOptionalBoundedString(source.current_ticket_title, 240);
  const mode = asBoundedString(source.mode, 128);
  const readiness = asBoundedString(source.readiness, 128);
  const workflowState = asBoundedString(source.workflow_state, 160);
  const workflowStatus = asBoundedString(source.workflow_status, 160);
  const approvalState = asBoundedString(source.approval_state, 160);
  const pendingApprovalCount = asNonNegativeInteger(source.pending_approval_count);
  const pendingTicketApprovalCount = asOptionalNonNegativeInteger(source.pending_ticket_approval_count, pendingApprovalCount ?? 0);
  const queueState = asBoundedString(source.queue_state, 160);
  const executionState = asBoundedString(source.execution_state, 160);
  const executionCount = asOptionalNonNegativeInteger(source.execution_count, 0);
  const activeExecutionCount = asNonNegativeInteger(source.active_execution_count);
  const validationState = asBoundedString(source.validation_state, 160);
  const reviewState = asBoundedString(source.review_state, 160);
  const reviewDecisionRecorded = asOptionalBoolean(source.review_decision_recorded, false);
  const reviewDecisionRequired = asOptionalBoolean(source.review_decision_required, false);
  const humanAcceptanceRequired = asOptionalBoolean(source.human_acceptance_required, false);
  const humanAcceptanceRecorded = asOptionalBoolean(source.human_acceptance_recorded, false);
  const recoveryState = asBoundedString(source.recovery_state, 160);
  const failureCategory = asOptionalNullableString(source.failure_category, 160);
  const failureSummary = asOptionalNullableString(source.failure_summary, 240);
  const gitHandoffState = asBoundedString(source.git_handoff_state, 160);
  const gitHandoffRequired = asOptionalBoolean(source.git_handoff_required, false);
  const defaultModeEnabled = asBoolean(source.default_mode_enabled);
  const manualChatControlRequired = asBoolean(source.manual_chat_control_required);
  const manualOpenCodeTicketCopyRequired = asBoolean(source.manual_opencode_ticket_copy_required);
  const manualOpenCodeResultCopyRequired = asBoolean(source.manual_opencode_result_copy_required);
  const humanGitAuthority = asBoundedString(source.human_git_authority, 160);
  const readyRequiresHumanSmoke = asBoolean(source.ready_requires_human_smoke);
  const closedGaps = Array.isArray(source.closed_gaps) ? source.closed_gaps.length : null;
  const remainingBlockers = Array.isArray(source.remaining_blockers) ? source.remaining_blockers.length : null;
  const blockerCount = asOptionalNonNegativeInteger(source.blocker_count, remainingBlockers ?? 0);
  const warningCount = asOptionalNonNegativeInteger(source.warning_count, 0);
  const nextActionId = asBoundedString(nextAction.id, 160);
  const nextActionLabel = asBoundedString(nextAction.label, 240);
  const nextActionTargetTicketId = asOptionalBoundedString(nextAction.target_ticket_id, 128);
  const nextActionTargetTicketTitle = asOptionalBoundedString(nextAction.target_ticket_title, 240);
  const nextActionRequiredHumanAction = asBoundedString(nextAction.required_human_action, 160);
  if (
    productId === null || projectId === null || projectName === null ||
    macroprojectId === null ||
    currentTicketId === undefined || currentTicketTitle === undefined ||
    mode === null || readiness === null || defaultModeEnabled === null ||
    workflowState === null || workflowStatus === null || approvalState === null ||
    pendingApprovalCount === null || pendingTicketApprovalCount === null ||
    queueState === null || executionState === null || executionCount === null ||
    activeExecutionCount === null || validationState === null || reviewState === null ||
    reviewDecisionRecorded === null || reviewDecisionRequired === null ||
    humanAcceptanceRequired === null || humanAcceptanceRecorded === null ||
    recoveryState === null || gitHandoffState === null || gitHandoffRequired === null ||
    manualChatControlRequired === null || manualOpenCodeTicketCopyRequired === null ||
    manualOpenCodeResultCopyRequired === null || humanGitAuthority === null ||
    readyRequiresHumanSmoke === null || closedGaps === null || remainingBlockers === null ||
    blockerCount === null || warningCount === null || nextActionId === null ||
    nextActionLabel === null || nextActionTargetTicketId === undefined ||
    nextActionTargetTicketTitle === undefined || nextActionRequiredHumanAction === null
  ) return null;
  return Object.freeze({
    productId,
    projectId,
    projectName,
    macroprojectId,
    currentTicketId,
    currentTicketTitle,
    mode,
    readiness,
    workflowState,
    workflowStatus,
    approvalState,
    pendingApprovalCount,
    pendingTicketApprovalCount,
    queueState,
    executionState,
    executionCount,
    activeExecutionCount,
    validationState,
    reviewState,
    reviewDecisionRecorded,
    reviewDecisionRequired,
    humanAcceptanceRequired,
    humanAcceptanceRecorded,
    recoveryState,
    failureCategory,
    failureSummary,
    gitHandoffState,
    gitHandoffRequired,
    defaultModeEnabled,
    manualChatControlRequired,
    manualOpenCodeTicketCopyRequired,
    manualOpenCodeResultCopyRequired,
    humanGitAuthority,
    readyRequiresHumanSmoke,
    closedGapCount: closedGaps,
    remainingBlockerCount: remainingBlockers,
    blockerCount,
    warningCount,
    nextActionId,
    nextActionLabel,
    nextActionTargetTicketId,
    nextActionTargetTicketTitle,
    nextActionRequiredHumanAction,
  });
}

function normalizeGatewayState(value: unknown, running: boolean): RuntimeGatewayState {
  if (value === "running") return "running";
  if (value === "starting") return "starting";
  if (value === "stopped") return "stopped";
  if (value === "startup_failed") return "failed";
  if (value === null && !running) return "off";
  return running ? "running" : "unknown";
}

/** Project the public status response into the only fields this surface retains. */
export function parseRuntimeOverviewSnapshot(value: unknown): RuntimeOverviewSnapshot | null {
  const source = asRecord(value);
  if (!source) return null;

  const version = asBoundedString(source.version, 64);
  const releaseDate = asBoundedString(source.release_date, 32);
  const configVersion = asNonNegativeInteger(source.config_version);
  const latestConfigVersion = asNonNegativeInteger(source.latest_config_version);
  const canUpdateHermes = asBoolean(source.can_update_hermes);
  const gatewayRunning = asBoolean(source.gateway_running);
  const gatewayBusy = asBoolean(source.gateway_busy);
  const gatewayDrainable = asBoolean(source.gateway_drainable);
  const activeSessions = asNonNegativeInteger(source.active_sessions);
  const activeAgents = asNonNegativeInteger(source.active_agents);
  const authRequired = asBoolean(source.auth_required);

  if (
    version === null ||
    releaseDate === null ||
    configVersion === null ||
    latestConfigVersion === null ||
    canUpdateHermes === null ||
    gatewayRunning === null ||
    gatewayBusy === null ||
    gatewayDrainable === null ||
    activeSessions === null ||
    activeAgents === null ||
    authRequired === null
  ) {
    return null;
  }

  return Object.freeze({
    platform: Object.freeze({
      version,
      releaseDate,
      configVersion,
      latestConfigVersion,
      updateAvailable: canUpdateHermes && latestConfigVersion > configVersion,
    }),
    gateway: Object.freeze({
      state: normalizeGatewayState(source.gateway_state, gatewayRunning),
      running: gatewayRunning,
      busy: gatewayBusy,
      drainable: gatewayDrainable,
    }),
    activity: Object.freeze({ activeSessions, activeAgents }),
    access: Object.freeze({ authRequired }),
    workflowControl: parseWorkflowControl(source.agent_platform_workflow_control),
  });
}
