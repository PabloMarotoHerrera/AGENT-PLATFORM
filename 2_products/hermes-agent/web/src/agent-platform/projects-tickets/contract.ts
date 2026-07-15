export const KANBAN_SOURCE = Object.freeze({
  sourceSystem: "hermes-kanban" as const,
  sourceAuthority: "provisional" as const,
  futureAuthority: "paperclip-control-plane" as const,
});

export const KANBAN_STATUSES = Object.freeze([
  "triage",
  "todo",
  "scheduled",
  "ready",
  "running",
  "blocked",
  "review",
  "done",
  "archived",
] as const);

export type KanbanSourceStatus = typeof KANBAN_STATUSES[number] | "other";
export type ProjectsWorkspacePhase =
  | "loading"
  | "ready"
  | "empty"
  | "stale"
  | "error"
  | "unavailable";
export type WorkspaceSectionPhase = "ready" | "empty" | "unavailable";

export interface ProjectsWorkspaceSource {
  readonly sourceSystem: "hermes-kanban";
  readonly sourceAuthority: "provisional";
  readonly futureAuthority: "paperclip-control-plane";
}

export interface ProjectSummary {
  readonly source: ProjectsWorkspaceSource;
  readonly boardSlug: string;
  readonly displayName: string;
  readonly description: string | null;
  readonly taskCounts: Readonly<Record<string, number>>;
  readonly totalTaskCount: number;
  readonly sourceFreshness: "current-response";
}

export interface TicketSummary {
  readonly source: ProjectsWorkspaceSource;
  readonly boardSlug: string;
  readonly taskId: string;
  readonly title: string;
  readonly body: string;
  readonly originalSourceStatus: string;
  readonly visualStatus: KanbanSourceStatus;
  readonly sourcePriority: number;
  readonly tenantLabel: string | null;
  readonly profileAssigneeLabel: string | null;
  readonly parentCount: number;
  readonly childCount: number;
  readonly createdAt: number | null;
  readonly startedAt: number | null;
  readonly completedAt: number | null;
}

export interface ProjectDetail extends ProjectSummary {
  readonly tickets: readonly TicketSummary[];
}

export interface TicketDependency {
  readonly source: ProjectsWorkspaceSource;
  readonly boardSlug: string;
  readonly taskId: string;
  readonly relation: "parent" | "child";
}

export interface TicketComment {
  readonly source: ProjectsWorkspaceSource;
  readonly sourceCommentId: string | number;
  readonly authorLabel: string;
  readonly body: string;
  readonly createdAt: number | null;
}

export interface TicketAttachmentMetadata {
  readonly source: ProjectsWorkspaceSource;
  readonly sourceAttachmentId: string | number;
  readonly displayFilename: string;
  readonly mediaType: string | null;
  readonly sizeBytes: number | null;
  readonly createdAt: number | null;
}

export interface TicketEvent {
  readonly source: ProjectsWorkspaceSource;
  readonly sourceEventId: string | number;
  readonly sourceRunId: string | number | null;
  readonly label: string;
  readonly createdAt: number | null;
}

export interface TicketRunSummary {
  readonly source: ProjectsWorkspaceSource;
  readonly sourceRunId: string | number;
  readonly sourceStatus: string;
  readonly startedAt: number | null;
  readonly endedAt: number | null;
  readonly sourceLabel: "Hermes Kanban run";
}

export interface TicketDiagnostic {
  readonly source: ProjectsWorkspaceSource;
  readonly sourceKind: string;
  readonly severity: "warning" | "error" | "critical";
  readonly count: number;
  readonly firstSeenAt: number | null;
  readonly lastSeenAt: number | null;
  readonly message: string;
}

export interface WorkspaceSection<T> {
  readonly phase: WorkspaceSectionPhase;
  readonly items: readonly T[];
}

export interface TicketDetail extends TicketSummary {
  readonly dependencies: WorkspaceSection<TicketDependency>;
  readonly comments: WorkspaceSection<TicketComment>;
  readonly attachments: WorkspaceSection<TicketAttachmentMetadata>;
  readonly events: WorkspaceSection<TicketEvent>;
  readonly runs: WorkspaceSection<TicketRunSummary>;
  readonly diagnostics: WorkspaceSection<TicketDiagnostic>;
}

export type ProjectsWorkspaceView =
  | { readonly kind: "projects"; readonly projects: readonly ProjectSummary[] }
  | { readonly kind: "project"; readonly project: ProjectDetail }
  | { readonly kind: "ticket"; readonly ticket: TicketDetail };

export type ProjectsWorkspaceRequest =
  | { readonly kind: "projects" }
  | { readonly kind: "project"; readonly boardSlug: string }
  | { readonly kind: "ticket"; readonly boardSlug: string; readonly taskId: string };

export interface ProjectsWorkspaceDataState {
  readonly phase: ProjectsWorkspacePhase;
  readonly snapshot: ProjectsWorkspaceView | null;
  readonly lastSuccessAt: number | null;
  readonly refreshing: boolean;
}

const MAX = Object.freeze({
  boards: 200,
  tasks: 1000,
  dependencies: 500,
  comments: 500,
  attachments: 200,
  events: 500,
  runs: 100,
  diagnostics: 200,
});

const STATUS_ORDER = new Map<string, number>(
  KANBAN_STATUSES.map((status, index) => [status, index]),
);

const DIAGNOSTIC_MESSAGES: Readonly<Record<string, string>> = Object.freeze({
  hallucinated_cards: "Hermes reported source references that do not resolve to cards.",
  triage_aux_unavailable: "Hermes reported that optional triage assistance is unavailable.",
  prose_phantom_refs: "Hermes reported unresolved source references in task text.",
  repeated_failures: "Hermes reported repeated source-run failures.",
  repeated_crashes: "Hermes reported repeated source-run crashes.",
  stuck_in_blocked: "Hermes reported that this source task has remained blocked.",
  block_unblock_cycling: "Hermes reported repeated source block-state changes.",
  stranded_in_ready: "Hermes reported that this source task has remained ready.",
});

function asRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function asArray(value: unknown, max: number): readonly unknown[] | null {
  return Array.isArray(value) && value.length <= max ? value : null;
}

function boundedString(value: unknown, max: number): string | null {
  if (typeof value !== "string") return null;
  const normalized = value.trim();
  return normalized.length > 0 && normalized.length <= max ? normalized : null;
}

function optionalBoundedString(value: unknown, max: number): string | null {
  if (value === null || value === undefined || value === "") return null;
  return boundedString(value, max);
}

function safeInteger(value: unknown, minimum = 0): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= minimum
    ? value
    : null;
}

function timestamp(value: unknown): number | null {
  if (value === null || value === undefined) return null;
  return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : null;
}

function sourceLocalId(value: unknown): string | number | null {
  if (typeof value === "number") return safeInteger(value);
  return validateTaskId(value);
}

function redactUnsafeText(value: string): string {
  return value
    .replace(/\bBearer\s+[A-Za-z0-9._~+/-]{8,}/gi, "Bearer [redacted]")
    .replace(
      /\b(api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|secret|password|authorization|oauth[_ -]?state)\b\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\s,;]+)/gi,
      "$1=[redacted]",
    )
    .replace(
      /\b(dir|worktree|workspace_path|stored_path)\s*[:=]\s*[^\s,;]+/gi,
      (_match, label: string) => `${label}=[redacted path]`,
    )
    .replace(/[A-Za-z]:[\\/][^\s"'<>]+/g, "[redacted path]")
    .replace(/(?:^|\s)\/(?:Users|home|tmp|var|opt|etc)\/[^\s"'<>]+/g, " [redacted path]")
    .replace(/Traceback \(most recent call last\):[\s\S]*/gi, "[redacted stack]");
}

function plainText(value: unknown, max: number): string | null {
  if (typeof value !== "string" || value.length > max) return null;
  const withoutControls = [...value].filter((character) => {
    const code = character.charCodeAt(0);
    return character === "\n" || character === "\t" || code >= 32 && code !== 127;
  }).join("");
  return redactUnsafeText(withoutControls).trim();
}

function safeFilename(value: unknown): string | null {
  const filename = boundedString(value, 255);
  if (
    !filename ||
    /[\\/:*?"<>]/.test(filename) ||
    [...filename].some((character) => character.charCodeAt(0) < 32) ||
    filename === "." ||
    filename === ".."
  ) {
    return null;
  }
  return redactUnsafeText(filename);
}

function mediaType(value: unknown): string | null {
  const candidate = optionalBoundedString(value, 128);
  return candidate && /^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*\/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*$/.test(candidate)
    ? candidate
    : null;
}

function sourceStatus(value: unknown): { original: string; visual: KanbanSourceStatus } | null {
  const original = boundedString(value, 64);
  if (!original) return null;
  const normalized = original.toLowerCase();
  return {
    original,
    visual: (KANBAN_STATUSES as readonly string[]).includes(normalized)
      ? normalized as KanbanSourceStatus
      : "other",
  };
}

export function validateBoardSlug(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const slug = value.trim().toLowerCase();
  return slug.length <= 64 && /^[a-z0-9][a-z0-9_-]*$/.test(slug) ? slug : null;
}

export function validateTaskId(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const id = value.trim();
  return id.length <= 128 && id !== "." && id !== ".." && /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(id)
    ? id
    : null;
}

export function validateProfileName(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const name = value.trim();
  return name.length <= 128 && /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name) ? name : null;
}

function projectCounts(value: unknown): Readonly<Record<string, number>> | null {
  const record = asRecord(value);
  if (!record) return null;
  const counts: Record<string, number> = {};
  for (const status of KANBAN_STATUSES) {
    if (record[status] === undefined) continue;
    const count = safeInteger(record[status]);
    if (count === null) return null;
    counts[status] = count;
  }
  return Object.freeze(counts);
}

function projectSummary(value: unknown): ProjectSummary | null {
  const record = asRecord(value);
  if (!record) return null;
  const boardSlug = validateBoardSlug(record.slug);
  const displayName = boundedString(record.name, 300) ?? boardSlug;
  const description = optionalBoundedString(record.description, 2000);
  const taskCounts = projectCounts(record.counts);
  if (!boardSlug || !displayName || !taskCounts) return null;
  const totalTaskCount = Object.values(taskCounts).reduce((total, count) => total + count, 0);
  if (!Number.isSafeInteger(totalTaskCount)) return null;
  return {
    source: KANBAN_SOURCE,
    boardSlug,
    displayName: redactUnsafeText(displayName),
    description: description ? redactUnsafeText(description) : null,
    taskCounts,
    totalTaskCount,
    sourceFreshness: "current-response",
  };
}

function taskSummary(value: unknown, boardSlug: string, fallbackStatus?: string): TicketSummary | null {
  const record = asRecord(value);
  if (!record) return null;
  const taskId = validateTaskId(record.id);
  const title = plainText(record.title, 300);
  const body = plainText(record.body, 20_000);
  const status = sourceStatus(record.status ?? fallbackStatus);
  const priority = safeInteger(record.priority, -1000);
  const tenantLabel = optionalBoundedString(record.tenant, 128);
  const profileAssigneeLabel = optionalBoundedString(record.assignee, 128);
  const linkCounts = asRecord(record.link_counts);
  const parentCount = linkCounts ? safeInteger(linkCounts.parents) : 0;
  const childCount = linkCounts ? safeInteger(linkCounts.children) : 0;
  if (!taskId || title === null || body === null || !status || priority === null || parentCount === null || childCount === null) {
    return null;
  }
  return {
    source: KANBAN_SOURCE,
    boardSlug,
    taskId,
    title,
    body,
    originalSourceStatus: status.original,
    visualStatus: status.visual,
    sourcePriority: priority,
    tenantLabel: tenantLabel ? redactUnsafeText(tenantLabel) : null,
    profileAssigneeLabel: profileAssigneeLabel ? redactUnsafeText(profileAssigneeLabel) : null,
    parentCount,
    childCount,
    createdAt: timestamp(record.created_at),
    startedAt: timestamp(record.started_at),
    completedAt: timestamp(record.completed_at),
  };
}

function deepFreeze<T>(value: T): T {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value as Record<string, unknown>)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
}

export function parseProjectsSource(value: unknown): readonly ProjectSummary[] | null {
  const record = asRecord(value);
  const boards = asArray(record?.boards, MAX.boards);
  if (!record || !boards) return null;
  const projects = boards.map(projectSummary).filter((project): project is ProjectSummary => project !== null);
  if (boards.length > 0 && projects.length === 0) return null;
  projects.sort((left, right) => left.displayName.localeCompare(right.displayName) || left.boardSlug.localeCompare(right.boardSlug));
  return deepFreeze(projects);
}

export function parseProjectSource(value: unknown, project: ProjectSummary): ProjectDetail | null {
  const record = asRecord(value);
  const columns = asArray(record?.columns, KANBAN_STATUSES.length + 1);
  if (!record || !columns) return null;
  const tickets: TicketSummary[] = [];
  let rawTaskCount = 0;
  for (const columnValue of columns) {
    const column = asRecord(columnValue);
    const name = boundedString(column?.name, 64);
    const tasks = asArray(column?.tasks, MAX.tasks);
    if (!column || !name || !tasks || tickets.length + tasks.length > MAX.tasks) return null;
    rawTaskCount += tasks.length;
    for (const task of tasks) {
      const parsed = taskSummary(task, project.boardSlug, name);
      if (parsed) tickets.push(parsed);
    }
  }
  if (rawTaskCount > 0 && tickets.length === 0) return null;
  tickets.sort((left, right) =>
    (STATUS_ORDER.get(left.visualStatus) ?? 99) - (STATUS_ORDER.get(right.visualStatus) ?? 99) ||
    right.sourcePriority - left.sourcePriority ||
    left.title.localeCompare(right.title) ||
    left.taskId.localeCompare(right.taskId));
  return deepFreeze({ ...project, tickets });
}

function section<T>(value: unknown, max: number, parser: (item: unknown) => T | null): WorkspaceSection<T> {
  const values = asArray(value, max);
  if (!values) return deepFreeze({ phase: "unavailable", items: [] });
  const items = values.map(parser).filter((item): item is T => item !== null);
  if (values.length > 0 && items.length === 0) return deepFreeze({ phase: "unavailable", items: [] });
  return deepFreeze({ phase: items.length ? "ready" : "empty", items });
}

function dependenciesSection(value: unknown, boardSlug: string): WorkspaceSection<TicketDependency> {
  const links = asRecord(value);
  const parents = asArray(links?.parents, MAX.dependencies);
  const children = asArray(links?.children, MAX.dependencies);
  if (!links || !parents || !children || parents.length + children.length > MAX.dependencies) {
    return deepFreeze({ phase: "unavailable", items: [] });
  }
  const items: TicketDependency[] = [];
  for (const [relation, values] of [["parent", parents], ["child", children]] as const) {
    for (const value of values) {
      const taskId = validateTaskId(value);
      if (taskId) items.push({ source: KANBAN_SOURCE, boardSlug, taskId, relation });
    }
  }
  if (parents.length + children.length > 0 && items.length === 0) {
    return deepFreeze({ phase: "unavailable", items: [] });
  }
  items.sort((left, right) => left.relation.localeCompare(right.relation) || left.taskId.localeCompare(right.taskId));
  return deepFreeze({ phase: items.length ? "ready" : "empty", items });
}

function comment(value: unknown): TicketComment | null {
  const record = asRecord(value);
  const sourceCommentId = sourceLocalId(record?.id);
  const authorLabel = plainText(record?.author, 128);
  const body = plainText(record?.body, 10_000);
  if (!record || sourceCommentId === null || authorLabel === null || body === null) return null;
  return { source: KANBAN_SOURCE, sourceCommentId, authorLabel, body, createdAt: timestamp(record.created_at) };
}

function attachment(value: unknown): TicketAttachmentMetadata | null {
  const record = asRecord(value);
  const sourceAttachmentId = sourceLocalId(record?.id);
  const displayFilename = safeFilename(record?.filename);
  const sizeBytes = record?.size === null || record?.size === undefined ? null : safeInteger(record.size);
  if (!record || sourceAttachmentId === null || !displayFilename || sizeBytes === null && record.size !== null && record.size !== undefined) {
    return null;
  }
  return {
    source: KANBAN_SOURCE,
    sourceAttachmentId,
    displayFilename,
    mediaType: mediaType(record.content_type),
    sizeBytes,
    createdAt: timestamp(record.created_at),
  };
}

function event(value: unknown): TicketEvent | null {
  const record = asRecord(value);
  const sourceEventId = sourceLocalId(record?.id);
  const sourceRunId = record?.run_id === null || record?.run_id === undefined ? null : sourceLocalId(record.run_id);
  const label = plainText(record?.kind, 500);
  if (!record || sourceEventId === null || label === null || sourceRunId === null && record.run_id !== null && record.run_id !== undefined) {
    return null;
  }
  return { source: KANBAN_SOURCE, sourceEventId, sourceRunId, label, createdAt: timestamp(record.created_at) };
}

function run(value: unknown): TicketRunSummary | null {
  const record = asRecord(value);
  const sourceRunId = sourceLocalId(record?.id);
  const status = plainText(record?.status, 64);
  if (!record || sourceRunId === null || status === null) return null;
  return {
    source: KANBAN_SOURCE,
    sourceRunId,
    sourceStatus: status,
    startedAt: timestamp(record.started_at),
    endedAt: timestamp(record.ended_at),
    sourceLabel: "Hermes Kanban run",
  };
}

function diagnostic(value: unknown): TicketDiagnostic | null {
  const record = asRecord(value);
  const sourceKind = validateTaskId(record?.kind);
  const severity = record?.severity;
  const count = safeInteger(record?.count);
  if (!record || !sourceKind || !["warning", "error", "critical"].includes(String(severity)) || count === null) return null;
  return {
    source: KANBAN_SOURCE,
    sourceKind,
    severity: severity as TicketDiagnostic["severity"],
    count,
    firstSeenAt: timestamp(record.first_seen_at),
    lastSeenAt: timestamp(record.last_seen_at),
    message: DIAGNOSTIC_MESSAGES[sourceKind] ?? "Hermes reported a source-local diagnostic.",
  };
}

export function parseTicketSource(value: unknown, boardSlug: string): TicketDetail | null {
  const record = asRecord(value);
  const taskRecord = asRecord(record?.task);
  const summary = taskSummary(taskRecord, boardSlug);
  if (!record || !taskRecord || !summary) return null;
  const rawDiagnostics = taskRecord.diagnostics ?? [];
  const dependencies = dependenciesSection(record.links, boardSlug);
  const detail: TicketDetail = {
    ...summary,
    parentCount: dependencies.items.filter((item) => item.relation === "parent").length,
    childCount: dependencies.items.filter((item) => item.relation === "child").length,
    dependencies,
    comments: section(record.comments, MAX.comments, comment),
    attachments: section(record.attachments, MAX.attachments, attachment),
    events: section(record.events, MAX.events, event),
    runs: section(record.runs, MAX.runs, run),
    diagnostics: section(rawDiagnostics, MAX.diagnostics, diagnostic),
  };
  return deepFreeze(detail);
}

export function isWorkspaceViewEmpty(view: ProjectsWorkspaceView): boolean {
  if (view.kind === "projects") return view.projects.length === 0;
  if (view.kind === "project") return view.project.tickets.length === 0;
  return false;
}
