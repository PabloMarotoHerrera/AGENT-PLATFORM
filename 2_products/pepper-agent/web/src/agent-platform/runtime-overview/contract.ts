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
  readonly currentTicketId: string;
  readonly currentTicketTitle: string;
  readonly mode: string;
  readonly readiness: string;
  readonly workflowState: string;
  readonly workflowStatus: string;
  readonly approvalState: string;
  readonly pendingApprovalCount: number;
  readonly queueState: string;
  readonly executionState: string;
  readonly activeExecutionCount: number;
  readonly validationState: string;
  readonly reviewState: string;
  readonly recoveryState: string;
  readonly gitHandoffState: string;
  readonly defaultModeEnabled: boolean;
  readonly manualChatControlRequired: boolean;
  readonly manualOpenCodeTicketCopyRequired: boolean;
  readonly manualOpenCodeResultCopyRequired: boolean;
  readonly humanGitAuthority: string;
  readonly readyRequiresHumanSmoke: boolean;
  readonly closedGapCount: number;
  readonly remainingBlockerCount: number;
  readonly nextActionLabel: string;
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

function asNonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0
    ? value
    : null;
}

function asBoolean(value: unknown): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function parseWorkflowControl(value: unknown): RuntimeWorkflowControl | null {
  const source = asRecord(value);
  const nextAction = asRecord(source?.next_action);
  if (!source || !nextAction) return null;
  const productId = asBoundedString(source.product_id, 128);
  const projectId = asBoundedString(source.project_id, 128);
  const projectName = asBoundedString(source.project_name, 128);
  const macroprojectId = asBoundedString(source.macroproject_id, 128);
  const currentTicketId = asBoundedString(source.current_ticket_id, 128);
  const currentTicketTitle = asBoundedString(source.current_ticket_title, 240);
  const mode = asBoundedString(source.mode, 128);
  const readiness = asBoundedString(source.readiness, 128);
  const workflowState = asBoundedString(source.workflow_state, 160);
  const workflowStatus = asBoundedString(source.workflow_status, 160);
  const approvalState = asBoundedString(source.approval_state, 160);
  const pendingApprovalCount = asNonNegativeInteger(source.pending_approval_count);
  const queueState = asBoundedString(source.queue_state, 160);
  const executionState = asBoundedString(source.execution_state, 160);
  const activeExecutionCount = asNonNegativeInteger(source.active_execution_count);
  const validationState = asBoundedString(source.validation_state, 160);
  const reviewState = asBoundedString(source.review_state, 160);
  const recoveryState = asBoundedString(source.recovery_state, 160);
  const gitHandoffState = asBoundedString(source.git_handoff_state, 160);
  const defaultModeEnabled = asBoolean(source.default_mode_enabled);
  const manualChatControlRequired = asBoolean(source.manual_chat_control_required);
  const manualOpenCodeTicketCopyRequired = asBoolean(source.manual_opencode_ticket_copy_required);
  const manualOpenCodeResultCopyRequired = asBoolean(source.manual_opencode_result_copy_required);
  const humanGitAuthority = asBoundedString(source.human_git_authority, 160);
  const readyRequiresHumanSmoke = asBoolean(source.ready_requires_human_smoke);
  const closedGaps = Array.isArray(source.closed_gaps) ? source.closed_gaps.length : null;
  const remainingBlockers = Array.isArray(source.remaining_blockers) ? source.remaining_blockers.length : null;
  const nextActionLabel = asBoundedString(nextAction.label, 240);
  if (
    productId === null || projectId === null || projectName === null ||
    macroprojectId === null || currentTicketId === null || currentTicketTitle === null ||
    mode === null || readiness === null || defaultModeEnabled === null ||
    workflowState === null || workflowStatus === null || approvalState === null ||
    pendingApprovalCount === null || queueState === null || executionState === null ||
    activeExecutionCount === null || validationState === null || reviewState === null ||
    recoveryState === null || gitHandoffState === null ||
    manualChatControlRequired === null || manualOpenCodeTicketCopyRequired === null ||
    manualOpenCodeResultCopyRequired === null || humanGitAuthority === null ||
    readyRequiresHumanSmoke === null || closedGaps === null || remainingBlockers === null ||
    nextActionLabel === null
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
    queueState,
    executionState,
    activeExecutionCount,
    validationState,
    reviewState,
    recoveryState,
    gitHandoffState,
    defaultModeEnabled,
    manualChatControlRequired,
    manualOpenCodeTicketCopyRequired,
    manualOpenCodeResultCopyRequired,
    humanGitAuthority,
    readyRequiresHumanSmoke,
    closedGapCount: closedGaps,
    remainingBlockerCount: remainingBlockers,
    nextActionLabel,
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
