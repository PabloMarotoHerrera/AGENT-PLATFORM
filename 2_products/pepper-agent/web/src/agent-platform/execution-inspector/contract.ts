import {
  validateBoardSlug,
  validateProfileName,
  validateTaskId,
} from "../projects-tickets/contract";

export const EXECUTION_SOURCE = Object.freeze({
  sourceType: "hermes-kanban-task-run" as const,
  sourceSystem: "hermes-kanban" as const,
  sourceAuthority: "pepper-controlled-product-evidence" as const,
  futureAuthority: "P15/P17-controlled-worker-adapter" as const,
  retentionLimitation: "Run rows remain bounded source evidence; linked events may be pruned and are not a complete history. Human Git authority is preserved outside execution records.",
});

export const EXECUTION_SOURCE_POSTURES = Object.freeze([
  Object.freeze({
    sourceType: "Pepper controlled execution collection",
    availability: "controlled source" as const,
    boundary: "Authenticated product API lists bounded execution records across boards without raw logs, PIDs, paths, or provider payloads.",
  }),
  Object.freeze({
    sourceType: "Hermes Kanban task run",
    availability: "qualified detail source" as const,
    boundary: "Exact board and task qualifiers expose source-local run facts plus controlled workflow handoff metadata.",
  }),
  Object.freeze({
    sourceType: "Hermes API-server run",
    availability: "not collected" as const,
    boundary: "Process-local detail has no safe collection and is not used as fallback.",
  }),
  Object.freeze({
    sourceType: "Hermes cron agent session",
    availability: "evidence only" as const,
    boundary: "Session naming does not prove a complete scheduler attempt or outcome.",
  }),
] as const);

export type ExecutionInspectorPhase =
  | "loading"
  | "ready"
  | "empty"
  | "stale"
  | "error"
  | "unavailable";
export type ExecutionEvidenceSectionPhase = "ready" | "empty" | "unavailable";

export interface ExecutionInspectorSource {
  readonly sourceType: "hermes-kanban-task-run";
  readonly sourceSystem: "hermes-kanban";
  readonly sourceAuthority: "pepper-controlled-product-evidence";
  readonly futureAuthority: "P15/P17-controlled-worker-adapter";
  readonly retentionLimitation: string;
}

export interface ExecutionSourceProvenance {
  readonly source: ExecutionInspectorSource;
  readonly boardSlug: string;
  readonly taskId: string;
  readonly sourceProfile: string | null;
  readonly observedAt: number;
  readonly freshnessBasis: "adapter-fetch-time";
}

export interface ExecutionSummary extends ExecutionSourceProvenance {
  readonly sourceExecutionIdentity: string;
  readonly sourceLocalExecutionId: number;
  readonly taskTitle: string;
  readonly originalSourceStatus: string;
  readonly originalSourceOutcome: string | null;
  readonly startedAt: number;
  readonly endedAt: number | null;
  readonly workflowState: string | null;
  readonly workPacketId: string | null;
  readonly validationState: string | null;
  readonly reviewState: string | null;
  readonly gitHandoffState: string | null;
  readonly nextAction: string | null;
}

export interface ExecutionEventEvidence extends ExecutionSourceProvenance {
  readonly sourceLocalEventId: number;
  readonly sourceLocalExecutionId: number;
  readonly sourceEventKind: string;
  readonly occurredAt: number;
}

export interface ExecutionNarrativeEvidence extends ExecutionSourceProvenance {
  readonly sourceLocalExecutionId: number;
  readonly summaryType: "result" | "failure";
  readonly safeText: string;
  readonly executableContent: "excluded";
}

export interface ExecutionArtifactReference extends ExecutionSourceProvenance {
  readonly sourceLocalArtifactId: number;
  readonly displayFilename: string;
  readonly mediaType: string | null;
  readonly sizeBytes: number | null;
  readonly createdAt: number | null;
  readonly attribution: "task-level-not-run-attributed";
}

export interface ExecutionDiagnosticEvidence extends ExecutionSourceProvenance {
  readonly sourceLocalExecutionId: number;
  readonly sourceLocalDiagnosticId: string;
  readonly severity: "warning" | "error" | "critical";
  readonly count: number;
  readonly firstSeenAt: number | null;
  readonly lastSeenAt: number | null;
  readonly safeMessage: string;
}

export interface ExecutionEvidenceSection<T> {
  readonly phase: ExecutionEvidenceSectionPhase;
  readonly items: readonly T[];
}

export interface ExecutionCollection {
  readonly source: ExecutionInspectorSource;
  readonly boardSlug: string;
  readonly taskId: string;
  readonly taskTitle: string;
  readonly observedAt: number;
  readonly executions: readonly ExecutionSummary[];
}

export interface ExecutionDetail extends ExecutionSummary {
  readonly safeActionCategory: "Hermes Kanban task attempt";
  readonly executableContent: "excluded";
  readonly validationSummaries: readonly string[];
  readonly linkedEvents: ExecutionEvidenceSection<ExecutionEventEvidence>;
  readonly resultSummary: ExecutionEvidenceSection<ExecutionNarrativeEvidence>;
  readonly failureSummary: ExecutionEvidenceSection<ExecutionNarrativeEvidence>;
  readonly artifactReferences: ExecutionEvidenceSection<ExecutionArtifactReference>;
  readonly diagnostics: ExecutionEvidenceSection<ExecutionDiagnosticEvidence>;
}

export type ExecutionInspectorView =
  | { readonly kind: "executions"; readonly collection: ExecutionCollection }
  | { readonly kind: "detail"; readonly execution: ExecutionDetail };

export type ExecutionInspectorRequest =
  | { readonly kind: "executions"; readonly boardSlug: string; readonly taskId: string }
  | {
    readonly kind: "detail";
    readonly boardSlug: string;
    readonly taskId: string;
    readonly executionId: string;
  };

export interface ExecutionInspectorDataState {
  readonly phase: ExecutionInspectorPhase;
  readonly snapshot: ExecutionInspectorView | null;
  readonly lastSuccessAt: number | null;
  readonly refreshing: boolean;
}

const MAX_RUNS = 500;
const MAX_EVENTS = 2_000;
const MAX_ARTIFACTS = 200;
const MAX_DIAGNOSTICS = 200;
const WITHHELD_TASK_TITLE = "Source task title withheld by the execution projection";

const DIAGNOSTIC_MESSAGES: Readonly<Record<string, string>> = Object.freeze({
  hallucinated_cards: "Hermes reported unresolved source card references.",
  triage_aux_unavailable: "Hermes reported that optional triage assistance was unavailable.",
  prose_phantom_refs: "Hermes reported unresolved source references in task text.",
  repeated_failures: "Hermes reported repeated source-run failures.",
  repeated_crashes: "Hermes reported repeated source-run crashes.",
  stuck_in_blocked: "Hermes reported that this source task remained blocked.",
  block_unblock_cycling: "Hermes reported repeated source block-state changes.",
  stranded_in_ready: "Hermes reported that this source task remained ready.",
});

function asRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function asArray(value: unknown, max: number): readonly unknown[] | null {
  return Array.isArray(value) && value.length <= max ? value : null;
}

function safeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : null;
}

function nonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0 ? value : null;
}

function timestamp(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : null;
}

function optionalTimestamp(value: unknown): number | null {
  return value === null || value === undefined ? null : timestamp(value);
}

function redactUnsafeText(value: string): string {
  return value
    .replace(/```[\s\S]*?```/g, "[redacted executable content]")
    .replace(/-----BEGIN [^-\n]*PRIVATE KEY-----[\s\S]*?-----END [^-\n]*PRIVATE KEY-----/gi, "[redacted credential]")
    .replace(/(?:^|\n)\s*(?:\$|>|sudo\b|rm\b|curl\b|wget\b|powershell\b|cmd(?:\.exe)?\b)[^\n]*/gi, "\n[redacted executable content]")
    .replace(/\bBearer\s+[A-Za-z0-9._~+/-]{8,}/gi, "Bearer [redacted]")
    .replace(/\b[A-Za-z0-9_-]*(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|secret|password|authorization|oauth[_ -]?state)[A-Za-z0-9_-]*\b["']?\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\s,;]+)/gi, "credential=[redacted]")
    .replace(/\b(?:command|cmd|shell|tool[_ -]?args?|arguments?|environment|env|payload|raw[_ -]?(?:message|log))\b["']?\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\n,;]+)/gi, "executable=[redacted]")
    .replace(/[A-Za-z]:[\\/][^\s"'<>]+/g, "[redacted path]")
    .replace(/\\\\[^\\\s"'<>]+\\[^\s"'<>]+/g, "[redacted path]")
    .replace(/(?:^|\s)\/(?:Users|home|tmp|var|opt|etc|workspace|worktree)\/[^\s"'<>]+/g, " [redacted path]")
    .replace(/\b(?:https?|wss?):\/\/[^\s"'<>]+/gi, "[redacted URL]")
    .replace(/Traceback \(most recent call last\):[\s\S]*/gi, "[redacted failure detail]");
}

function plainText(value: unknown, max: number): string | null {
  if (typeof value !== "string" || value.length > max) return null;
  const withoutControls = [...value].filter((character) => {
    const code = character.charCodeAt(0);
    return character === "\n" || character === "\t" || code >= 32 && code !== 127;
  }).join("");
  const safe = redactUnsafeText(withoutControls).trim();
  return safe || null;
}

function hasBoundedText(value: unknown, max: number): boolean {
  if (typeof value !== "string" || value.length === 0 || value.length > max) return false;
  return [...value].every((character) => {
    const code = character.charCodeAt(0);
    return character === "\n" || character === "\t" || code >= 32 && code !== 127;
  }) && value.trim().length > 0;
}

function sourceToken(value: unknown, max = 64): string | null {
  if (typeof value !== "string" || value.length === 0 || value.length > max) return null;
  return /^[A-Za-z0-9][A-Za-z0-9._:-]*$/.test(value) ? value : null;
}

function optionalSourceToken(value: unknown, max = 64): string | null {
  return value === null || value === undefined || value === "" ? null : sourceToken(value, max);
}

function safeFilename(value: unknown): string | null {
  if (typeof value !== "string" || /[\\/:*?"<>]/.test(value)) return null;
  const filename = plainText(value, 255);
  return filename && filename !== "." && filename !== ".."
    ? filename
    : null;
}

function mediaType(value: unknown): string | null {
  if (value === null || value === undefined || value === "") return null;
  return typeof value === "string" && value.length <= 128 &&
    /^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*\/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*$/.test(value)
    ? value
    : null;
}

function deepFreeze<T>(value: T): T {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value as Record<string, unknown>)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
}

export function validateExecutionId(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const id = value;
  if (!/^[1-9][0-9]{0,15}$/.test(id)) return null;
  const numeric = Number(id);
  return Number.isSafeInteger(numeric) && String(numeric) === id ? id : null;
}

function projectionContext(
  boardSlug: unknown,
  taskId: unknown,
  observedAt: unknown,
): { boardSlug: string; taskId: string; observedAt: number } | null {
  const board = validateBoardSlug(boardSlug);
  const task = validateTaskId(taskId);
  const observed = timestamp(observedAt);
  return board && task && observed !== null ? { boardSlug: board, taskId: task, observedAt: observed } : null;
}

function sourceProfile(value: unknown): string | null | undefined {
  if (value === null || value === undefined || value === "") return null;
  const profile = validateProfileName(value);
  return profile ?? undefined;
}

function executionSummary(
  value: unknown,
  context: { boardSlug: string; taskId: string; taskTitle: string; observedAt: number },
): ExecutionSummary | null {
  const record = asRecord(value);
  const sourceLocalExecutionId = safeInteger(record?.id);
  const runTaskId = validateTaskId(record?.task_id);
  const profile = sourceProfile(record?.profile);
  const originalSourceStatus = sourceToken(record?.status);
  const originalSourceOutcome = optionalSourceToken(record?.outcome);
  const startedAt = timestamp(record?.started_at);
  const endedAt = optionalTimestamp(record?.ended_at);
  if (
    !record || sourceLocalExecutionId === null || runTaskId !== context.taskId || profile === undefined ||
    !originalSourceStatus || startedAt === null ||
    originalSourceOutcome === null && record.outcome !== null && record.outcome !== undefined && record.outcome !== "" ||
    endedAt === null && record.ended_at !== null && record.ended_at !== undefined
  ) return null;
  return {
    source: EXECUTION_SOURCE,
    sourceExecutionIdentity: `${context.boardSlug}:${context.taskId}:${sourceLocalExecutionId}`,
    boardSlug: context.boardSlug,
    taskId: context.taskId,
    sourceProfile: profile,
    observedAt: context.observedAt,
    freshnessBasis: "adapter-fetch-time",
    sourceLocalExecutionId,
    taskTitle: context.taskTitle,
    originalSourceStatus,
    originalSourceOutcome,
    startedAt,
    endedAt,
    workflowState: null,
    workPacketId: null,
    validationState: null,
    reviewState: null,
    gitHandoffState: null,
    nextAction: null,
  };
}

function controlledExecutionSummary(value: unknown, observedAt: number): ExecutionSummary | null {
  const record = asRecord(value);
  const boardSlug = validateBoardSlug(record?.board_slug);
  const taskId = validateTaskId(record?.task_id);
  const taskTitle = plainText(record?.task_title, 300);
  const sourceLocalExecutionId = safeInteger(record?.id);
  const profile = sourceProfile(record?.profile);
  const originalSourceStatus = sourceToken(record?.status);
  const originalSourceOutcome = optionalSourceToken(record?.outcome);
  const startedAt = timestamp(record?.started_at);
  const endedAt = optionalTimestamp(record?.ended_at);
  const workflowState = optionalSourceToken(record?.workflow_state, 128);
  const workPacketId = optionalSourceToken(record?.work_packet_id, 128);
  const validationState = optionalSourceToken(record?.validation_state, 128);
  const reviewState = optionalSourceToken(record?.review_state, 128);
  const gitHandoffState = optionalSourceToken(record?.git_handoff_state, 128);
  const nextAction = optionalSourceToken(record?.next_action, 128);
  if (
    !record || !boardSlug || !taskId || !taskTitle || sourceLocalExecutionId === null ||
    profile === undefined || !originalSourceStatus || startedAt === null ||
    originalSourceOutcome === null && record.outcome !== null && record.outcome !== undefined && record.outcome !== "" ||
    endedAt === null && record.ended_at !== null && record.ended_at !== undefined ||
    workflowState === undefined || workPacketId === undefined || validationState === undefined ||
    reviewState === undefined || gitHandoffState === undefined || nextAction === undefined
  ) return null;
  return {
    source: EXECUTION_SOURCE,
    sourceExecutionIdentity: `${boardSlug}:${taskId}:${sourceLocalExecutionId}`,
    boardSlug,
    taskId,
    sourceProfile: profile,
    observedAt,
    freshnessBasis: "adapter-fetch-time",
    sourceLocalExecutionId,
    taskTitle,
    originalSourceStatus,
    originalSourceOutcome,
    startedAt,
    endedAt,
    workflowState,
    workPacketId,
    validationState,
    reviewState,
    gitHandoffState,
    nextAction,
  };
}

function controlledExecutionCollection(value: Record<string, unknown>, observedAt: number): ExecutionCollection | null {
  if (value.source_system !== "pepper-controlled-execution") return null;
  const rawExecutions = asArray(value.executions, MAX_RUNS);
  if (!rawExecutions) return null;
  const executions = rawExecutions.map((item) => controlledExecutionSummary(item, observedAt));
  if (executions.some((execution) => execution === null)) return null;
  const safeExecutions = executions as ExecutionSummary[];
  if (new Set(safeExecutions.map((execution) => execution.sourceExecutionIdentity)).size !== safeExecutions.length) {
    return null;
  }
  safeExecutions.sort((left, right) =>
    right.startedAt - left.startedAt || right.sourceLocalExecutionId - left.sourceLocalExecutionId ||
    left.sourceExecutionIdentity.localeCompare(right.sourceExecutionIdentity));
  return deepFreeze({
    source: EXECUTION_SOURCE,
    boardSlug: "all",
    taskId: "all",
    taskTitle: "All controlled execution records",
    observedAt,
    executions: safeExecutions,
  });
}

export function parseExecutionCollectionSource(
  value: unknown,
  boardSlug: string,
  taskId: string,
  observedAt: number,
): ExecutionCollection | null {
  const context = projectionContext(boardSlug, taskId, observedAt);
  const record = asRecord(value);
  if (record?.source_system === "pepper-controlled-execution") {
    return controlledExecutionCollection(record, observedAt);
  }
  const task = asRecord(record?.task);
  const responseTaskId = validateTaskId(task?.id);
  const taskTitle = hasBoundedText(task?.title, 300) ? WITHHELD_TASK_TITLE : null;
  const runs = asArray(record?.runs, MAX_RUNS);
  if (!context || !record || !task || responseTaskId !== context.taskId || !taskTitle || !runs) return null;
  const projectionContextValue = { ...context, taskTitle };
  const executions = runs.map((run) => executionSummary(run, projectionContextValue));
  if (executions.some((execution) => execution === null)) return null;
  const safeExecutions = executions as ExecutionSummary[];
  if (new Set(safeExecutions.map((execution) => execution.sourceLocalExecutionId)).size !== safeExecutions.length) {
    return null;
  }
  safeExecutions.sort((left, right) =>
    right.startedAt - left.startedAt || right.sourceLocalExecutionId - left.sourceLocalExecutionId);
  return deepFreeze({
    source: EXECUTION_SOURCE,
    boardSlug: context.boardSlug,
    taskId: context.taskId,
    taskTitle,
    observedAt: context.observedAt,
    executions: safeExecutions,
  });
}

function linkedEventsSection(
  value: unknown,
  execution: ExecutionSummary,
): ExecutionEvidenceSection<ExecutionEventEvidence> {
  const values = asArray(value, MAX_EVENTS);
  if (!values) return deepFreeze({ phase: "unavailable", items: [] });
  const items: ExecutionEventEvidence[] = [];
  const eventIds = new Set<number>();
  for (const value of values) {
    const record = asRecord(value);
    const linkedExecutionId = safeInteger(record?.run_id);
    if (linkedExecutionId !== execution.sourceLocalExecutionId) continue;
    const sourceLocalEventId = safeInteger(record?.id);
    const taskId = validateTaskId(record?.task_id);
    const sourceEventKind = sourceToken(record?.kind, 128);
    const occurredAt = timestamp(record?.created_at);
    if (!record || sourceLocalEventId === null || taskId !== execution.taskId || !sourceEventKind || occurredAt === null) {
      return deepFreeze({ phase: "unavailable", items: [] });
    }
    if (eventIds.has(sourceLocalEventId)) return deepFreeze({ phase: "unavailable", items: [] });
    eventIds.add(sourceLocalEventId);
    items.push({
      source: EXECUTION_SOURCE,
      boardSlug: execution.boardSlug,
      taskId: execution.taskId,
      sourceProfile: execution.sourceProfile,
      observedAt: execution.observedAt,
      freshnessBasis: "adapter-fetch-time",
      sourceLocalEventId,
      sourceLocalExecutionId: execution.sourceLocalExecutionId,
      sourceEventKind,
      occurredAt,
    });
  }
  items.sort((left, right) => left.occurredAt - right.occurredAt || left.sourceLocalEventId - right.sourceLocalEventId);
  return deepFreeze({ phase: items.length ? "ready" : "empty", items });
}

function narrativeSection(
  value: unknown,
  execution: ExecutionSummary,
  summaryType: "result" | "failure",
): ExecutionEvidenceSection<ExecutionNarrativeEvidence> {
  if (value === undefined) return deepFreeze({ phase: "unavailable", items: [] });
  if (value === null || value === "") {
    return deepFreeze({ phase: "empty", items: [] });
  }
  if (typeof value !== "string" || value.length > 10_000) {
    return deepFreeze({ phase: "unavailable", items: [] });
  }
  if (!value.trim()) return deepFreeze({ phase: "empty", items: [] });
  const safeText = summaryType === "failure"
    ? "Hermes recorded a source-local failure summary; raw failure detail is excluded."
    : "Hermes recorded a source-local result summary; raw result detail is excluded.";
  return deepFreeze({
    phase: "ready",
    items: [{
      source: EXECUTION_SOURCE,
      boardSlug: execution.boardSlug,
      taskId: execution.taskId,
      sourceProfile: execution.sourceProfile,
      observedAt: execution.observedAt,
      freshnessBasis: "adapter-fetch-time",
      sourceLocalExecutionId: execution.sourceLocalExecutionId,
      summaryType,
      safeText,
      executableContent: "excluded",
    }],
  });
}

function artifactReferencesSection(
  value: unknown,
  execution: ExecutionSummary,
): ExecutionEvidenceSection<ExecutionArtifactReference> {
  const values = asArray(value, MAX_ARTIFACTS);
  if (!values) return deepFreeze({ phase: "unavailable", items: [] });
  const items: ExecutionArtifactReference[] = [];
  const ids = new Set<number>();
  for (const value of values) {
    const record = asRecord(value);
    const sourceLocalArtifactId = safeInteger(record?.id);
    const taskId = validateTaskId(record?.task_id);
    const displayFilename = safeFilename(record?.filename);
    const parsedMediaType = mediaType(record?.content_type);
    const sizeBytes = record?.size === null || record?.size === undefined
      ? null
      : nonNegativeInteger(record.size);
    const createdAt = optionalTimestamp(record?.created_at);
    if (
      !record || sourceLocalArtifactId === null || taskId !== execution.taskId || !displayFilename ||
      parsedMediaType === null && record.content_type !== null && record.content_type !== undefined && record.content_type !== "" ||
      sizeBytes === null && record.size !== null && record.size !== undefined ||
      createdAt === null && record.created_at !== null && record.created_at !== undefined ||
      ids.has(sourceLocalArtifactId)
    ) return deepFreeze({ phase: "unavailable", items: [] });
    ids.add(sourceLocalArtifactId);
    items.push({
      source: EXECUTION_SOURCE,
      boardSlug: execution.boardSlug,
      taskId: execution.taskId,
      sourceProfile: execution.sourceProfile,
      observedAt: execution.observedAt,
      freshnessBasis: "adapter-fetch-time",
      sourceLocalArtifactId,
      displayFilename,
      mediaType: parsedMediaType,
      sizeBytes,
      createdAt,
      attribution: "task-level-not-run-attributed",
    });
  }
  items.sort((left, right) => left.sourceLocalArtifactId - right.sourceLocalArtifactId);
  return deepFreeze({ phase: items.length ? "ready" : "empty", items });
}

function diagnosticsSection(
  value: unknown,
  execution: ExecutionSummary,
): ExecutionEvidenceSection<ExecutionDiagnosticEvidence> {
  const values = asArray(value, MAX_DIAGNOSTICS);
  if (!values) return deepFreeze({ phase: "unavailable", items: [] });
  const items: ExecutionDiagnosticEvidence[] = [];
  const ids = new Set<string>();
  for (const value of values) {
    const record = asRecord(value);
    const runId = safeInteger(record?.run_id);
    if (runId !== execution.sourceLocalExecutionId) continue;
    const sourceLocalDiagnosticId = sourceToken(record?.kind, 128);
    const severity = record?.severity;
    const count = nonNegativeInteger(record?.count);
    const firstSeenAt = optionalTimestamp(record?.first_seen_at);
    const lastSeenAt = optionalTimestamp(record?.last_seen_at);
    if (
      !record || !sourceLocalDiagnosticId || !["warning", "error", "critical"].includes(String(severity)) ||
      count === null ||
      firstSeenAt === null && record.first_seen_at !== null && record.first_seen_at !== undefined ||
      lastSeenAt === null && record.last_seen_at !== null && record.last_seen_at !== undefined ||
      ids.has(sourceLocalDiagnosticId)
    ) return deepFreeze({ phase: "unavailable", items: [] });
    ids.add(sourceLocalDiagnosticId);
    items.push({
      source: EXECUTION_SOURCE,
      boardSlug: execution.boardSlug,
      taskId: execution.taskId,
      sourceProfile: execution.sourceProfile,
      observedAt: execution.observedAt,
      freshnessBasis: "adapter-fetch-time",
      sourceLocalExecutionId: execution.sourceLocalExecutionId,
      sourceLocalDiagnosticId,
      severity: severity as ExecutionDiagnosticEvidence["severity"],
      count,
      firstSeenAt,
      lastSeenAt,
      safeMessage: DIAGNOSTIC_MESSAGES[sourceLocalDiagnosticId] ?? "Hermes reported a source-local diagnostic.",
    });
  }
  items.sort((left, right) => left.sourceLocalDiagnosticId.localeCompare(right.sourceLocalDiagnosticId));
  return deepFreeze({ phase: items.length ? "ready" : "empty", items });
}

export function parseExecutionDetailSource(
  value: unknown,
  boardSlug: string,
  taskId: string,
  executionId: string,
  observedAt: number,
): ExecutionDetail | null {
  const id = validateExecutionId(executionId);
  const collection = parseExecutionCollectionSource(value, boardSlug, taskId, observedAt);
  const record = asRecord(value);
  if (!id || !collection || !record) return null;
  const execution = collection.executions.find((item) => item.sourceLocalExecutionId === Number(id));
  if (!execution) return null;
  const rawRuns = asArray(record.runs, MAX_RUNS);
  const rawRun = rawRuns?.find((value) => safeInteger(asRecord(value)?.id) === execution.sourceLocalExecutionId);
  const rawRunRecord = asRecord(rawRun);
  const taskRecord = asRecord(record.task);
  const controlRecord = asRecord(record.control);
  if (!rawRunRecord || !taskRecord) return null;
  return deepFreeze({
    ...execution,
    workflowState: optionalSourceToken(controlRecord?.workflow_state, 128) ?? execution.workflowState,
    workPacketId: optionalSourceToken(controlRecord?.work_packet_id, 128) ?? execution.workPacketId,
    validationState: optionalSourceToken(controlRecord?.validation_state, 128) ?? execution.validationState,
    reviewState: optionalSourceToken(controlRecord?.review_state, 128) ?? execution.reviewState,
    gitHandoffState: optionalSourceToken(controlRecord?.git_handoff_state, 128) ?? execution.gitHandoffState,
    nextAction: optionalSourceToken(controlRecord?.next_action, 128) ?? execution.nextAction,
    safeActionCategory: "Hermes Kanban task attempt",
    executableContent: "excluded",
    validationSummaries: [
      "Exact board, task and source-local run association validated.",
      "Only events with an explicit matching source run ID are included.",
    ],
    linkedEvents: linkedEventsSection(record.events, execution),
    resultSummary: narrativeSection(rawRunRecord.summary, execution, "result"),
    failureSummary: narrativeSection(rawRunRecord.error, execution, "failure"),
    artifactReferences: artifactReferencesSection(record.attachments, execution),
    diagnostics: diagnosticsSection(taskRecord.diagnostics, execution),
  });
}

export function isExecutionInspectorViewEmpty(view: ExecutionInspectorView): boolean {
  return view.kind === "executions" && view.collection.executions.length === 0;
}
