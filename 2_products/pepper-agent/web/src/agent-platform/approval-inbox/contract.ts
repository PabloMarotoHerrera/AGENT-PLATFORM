export const APPROVAL_SOURCE = Object.freeze({
  sourceSystem: "hermes-write-approval" as const,
  sourceAuthority: "provisional" as const,
  canonicalApprovalAuthority: "not_yet_established" as const,
});

export const APPROVAL_VISUAL_STATUSES = Object.freeze([
  "pending",
  "approved",
  "rejected",
  "expired",
  "cancelled",
] as const);

export const ELIGIBLE_APPROVAL_SEMANTICS = Object.freeze([
  "explicit_approval_request",
  "explicit_confirmation_request",
  "explicit_permission_decision_request",
  "explicit_allow_deny_decision_record",
] as const);

export type ApprovalVisualStatus = typeof APPROVAL_VISUAL_STATUSES[number] | "other";
export type ApprovalRequestCategory = "approval" | "confirmation" | "permission" | "allow-deny";
export type ApprovalTargetType =
  | "tool action"
  | "filesystem action"
  | "network action"
  | "configuration action"
  | "runtime action"
  | "other source action";
export type ApprovalInboxPhase = "loading" | "ready" | "empty" | "stale" | "error" | "unavailable";
export type ApprovalSectionPhase = "ready" | "empty" | "unavailable";

export interface ApprovalInboxSource {
  readonly sourceSystem: "hermes-write-approval";
  readonly sourceAuthority: "provisional";
  readonly canonicalApprovalAuthority: "not_yet_established";
}

export interface ApprovalTarget {
  readonly source: ApprovalInboxSource;
  readonly sourceTargetType: ApprovalTargetType;
  readonly sourceTargetLabel: string;
}

export interface ApprovalSummary {
  readonly source: ApprovalInboxSource;
  readonly sourceLocalApprovalId: string;
  readonly title: string;
  readonly summary: string;
  readonly originalSourceStatus: string;
  readonly visualStatus: ApprovalVisualStatus;
  readonly originalSourceType: string;
  readonly requestCategory: ApprovalRequestCategory;
  readonly requestedAt: number;
  readonly expiresAt: number | null;
  readonly sourceRequesterLabel: string | null;
  readonly sourceRiskLabel: "low" | "medium" | "high" | "critical" | "other" | null;
  readonly target: ApprovalTarget;
}

export interface ApprovalEvidenceSummary {
  readonly source: ApprovalInboxSource;
  readonly sourceLocalEvidenceId: string;
  readonly sourceEvidenceLabel: string;
}

export interface ApprovalDecisionSummary {
  readonly source: ApprovalInboxSource;
  readonly sourceLocalDecisionId: string;
  readonly originalSourceStatus: string;
  readonly visualStatus: ApprovalVisualStatus;
  readonly decidedAt: number;
  readonly sourceActorLabel: string | null;
}

export interface ApprovalSectionState<T> {
  readonly phase: ApprovalSectionPhase;
  readonly items: readonly T[];
}

export interface ApprovalDetail extends ApprovalSummary {
  readonly sourceReason: string | null;
  readonly evidence: ApprovalSectionState<ApprovalEvidenceSummary>;
  readonly decisionHistory: ApprovalSectionState<ApprovalDecisionSummary>;
}

export type ApprovalInboxView =
  | { readonly kind: "inbox"; readonly approvals: readonly ApprovalSummary[] }
  | { readonly kind: "detail"; readonly approval: ApprovalDetail };

export type ApprovalInboxRequest =
  | { readonly kind: "inbox" }
  | { readonly kind: "detail"; readonly approvalId: string };

export interface ApprovalInboxDataState {
  readonly phase: ApprovalInboxPhase;
  readonly snapshot: ApprovalInboxView | null;
  readonly lastSuccessAt: number | null;
  readonly refreshing: boolean;
}

const MAX = Object.freeze({
  approvals: 500,
  evidence: 200,
  decisions: 100,
});

const REQUEST_CATEGORIES: Readonly<Record<string, ApprovalRequestCategory>> = Object.freeze({
  explicit_approval_request: "approval",
  explicit_confirmation_request: "confirmation",
  explicit_permission_decision_request: "permission",
  explicit_allow_deny_decision_record: "allow-deny",
});

const TARGET_TYPES: Readonly<Record<string, ApprovalTargetType>> = Object.freeze({
  tool_action: "tool action",
  filesystem_action: "filesystem action",
  network_action: "network action",
  configuration_action: "configuration action",
  runtime_action: "runtime action",
  other_source_action: "other source action",
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

function timestamp(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : null;
}

function optionalTimestamp(value: unknown): number | null {
  if (value === null || value === undefined) return null;
  return timestamp(value);
}

function redactUnsafeText(value: string): string {
  return value
    .replace(/```[\s\S]*?```/g, "[redacted code]")
    .replace(/(?:^|\n)\s*(?:\$|>|sudo\b|rm\b|curl\b|wget\b|powershell\b|cmd(?:\.exe)?\b)[^\n]*/gi, "\n[redacted command]")
    .replace(/\bBearer\s+[A-Za-z0-9._~+/-]{8,}/gi, "Bearer [redacted]")
    .replace(/\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|secret|password|authorization|oauth[_ -]?state|cookie)\b\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\s,;]+)/gi, "credential=[redacted]")
    .replace(/\b(?:command|cmd|shell|tool[_ -]?args?|arguments?|spawn[_ -]?args?|environment|env|payload|result|response)\b\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\n,;]+)/gi, "executable=[redacted]")
    .replace(/\b(?:provider|provider[_ -]?id|model|model[_ -]?id|pid|process[_ -]?id|worker[_ -]?claim|heartbeat)\b\s*[:=]\s*[^\s,;]+/gi, "runtime=[redacted]")
    .replace(/\b[A-Z][A-Z0-9_]{2,}\s*=\s*[^\s,;]+/g, "environment=[redacted]")
    .replace(/\b(?:https?|wss?):\/\/[^\s"'<>]+/gi, "[redacted URL]")
    .replace(/\b(?:localhost|127\.0\.0\.1|0\.0\.0\.0):\d{2,5}\b/gi, "[redacted endpoint]")
    .replace(/[A-Za-z]:[\\/][^\s"'<>]+/g, "[redacted path]")
    .replace(/(?:^|\s)\/(?:Users|home|tmp|var|opt|etc|workspace|worktree)\/[^\s"'<>]+/g, " [redacted path]")
    .replace(/\b(?:sk|pk|ghp|github_pat)-[A-Za-z0-9_-]{8,}\b/g, "[redacted credential]")
    .replace(/Traceback \(most recent call last\):[\s\S]*/gi, "[redacted stack]");
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

function deepFreeze<T>(value: T): T {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value as Record<string, unknown>)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
}

export function validateApprovalId(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const id = value.trim();
  return id.length <= 128 && id !== "." && id !== ".." && /^[A-Za-z0-9][A-Za-z0-9._:-]*$/.test(id)
    ? id
    : null;
}

export function validateProfileName(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const name = value.trim();
  return name.length <= 128 && /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name) ? name : null;
}

export function classifyApprovalSourceSemantics(value: unknown): "eligible" | "ineligible" {
  return typeof value === "string" && (ELIGIBLE_APPROVAL_SEMANTICS as readonly string[]).includes(value)
    ? "eligible"
    : "ineligible";
}

function sourceEnvelope(value: unknown): Record<string, unknown> | null {
  const record = asRecord(value);
  return record?.source_system === APPROVAL_SOURCE.sourceSystem ? record : null;
}

function sourceStatus(value: unknown): { original: string; visual: ApprovalVisualStatus } | null {
  const original = boundedString(value, 64);
  if (!original) return null;
  const normalized = original.toLowerCase();
  return {
    original,
    visual: (APPROVAL_VISUAL_STATUSES as readonly string[]).includes(normalized)
      ? normalized as ApprovalVisualStatus
      : "other",
  };
}

function sourceRisk(value: unknown): ApprovalSummary["sourceRiskLabel"] {
  if (value === null || value === undefined || value === "") return null;
  const candidate = boundedString(value, 32)?.toLowerCase();
  return candidate && ["low", "medium", "high", "critical"].includes(candidate)
    ? candidate as Exclude<ApprovalSummary["sourceRiskLabel"], "other" | null>
    : "other";
}

function target(value: unknown): ApprovalTarget | null {
  const record = asRecord(value);
  const rawType = boundedString(record?.type, 64);
  const label = plainText(record?.label, 300);
  if (!record || !rawType || !label) return null;
  return {
    source: APPROVAL_SOURCE,
    sourceTargetType: TARGET_TYPES[rawType.toLowerCase()] ?? "other source action",
    sourceTargetLabel: label,
  };
}

function summary(value: unknown): ApprovalSummary | null {
  const record = asRecord(value);
  const sourceLocalApprovalId = validateApprovalId(record?.id);
  const title = plainText(record?.title, 300);
  const safeSummary = plainText(record?.summary, 4000);
  const status = sourceStatus(record?.status);
  const originalSourceType = boundedString(record?.request_type, 128);
  const semantics = boundedString(record?.semantics, 64);
  const requestedAt = timestamp(record?.requested_at);
  const expiresAt = optionalTimestamp(record?.expires_at);
  const sourceRequesterLabel = record?.requester === null || record?.requester === undefined
    ? null
    : plainText(record.requester, 200);
  const safeTarget = target(record?.target);
  if (
    !record || !sourceLocalApprovalId || !title || !safeSummary || !status || !originalSourceType ||
    !semantics || classifyApprovalSourceSemantics(semantics) !== "eligible" || requestedAt === null ||
    expiresAt === null && record.expires_at !== null && record.expires_at !== undefined ||
    sourceRequesterLabel === null && record.requester !== null && record.requester !== undefined || !safeTarget
  ) {
    return null;
  }
  return {
    source: APPROVAL_SOURCE,
    sourceLocalApprovalId,
    title,
    summary: safeSummary,
    originalSourceStatus: status.original,
    visualStatus: status.visual,
    originalSourceType,
    requestCategory: REQUEST_CATEGORIES[semantics]!,
    requestedAt,
    expiresAt,
    sourceRequesterLabel,
    sourceRiskLabel: sourceRisk(record.risk_label),
    target: safeTarget,
  };
}

function evidence(value: unknown): ApprovalEvidenceSummary | null {
  const record = asRecord(value);
  const sourceLocalEvidenceId = validateApprovalId(record?.id);
  const sourceEvidenceLabel = plainText(record?.label, 500);
  return record && sourceLocalEvidenceId && sourceEvidenceLabel
    ? { source: APPROVAL_SOURCE, sourceLocalEvidenceId, sourceEvidenceLabel }
    : null;
}

function decision(value: unknown): ApprovalDecisionSummary | null {
  const record = asRecord(value);
  const sourceLocalDecisionId = validateApprovalId(record?.id);
  const status = sourceStatus(record?.status);
  const decidedAt = timestamp(record?.decided_at);
  const sourceActorLabel = record?.actor === null || record?.actor === undefined
    ? null
    : plainText(record.actor, 200);
  if (
    !record || !sourceLocalDecisionId || !status || decidedAt === null ||
    sourceActorLabel === null && record.actor !== null && record.actor !== undefined
  ) {
    return null;
  }
  return {
    source: APPROVAL_SOURCE,
    sourceLocalDecisionId,
    originalSourceStatus: status.original,
    visualStatus: status.visual,
    decidedAt,
    sourceActorLabel,
  };
}

function section<T>(value: unknown, max: number, parse: (item: unknown) => T | null): ApprovalSectionState<T> {
  const values = asArray(value, max);
  if (!values) return deepFreeze({ phase: "unavailable", items: [] });
  const items = values.map(parse);
  if (items.some((item) => item === null)) return deepFreeze({ phase: "unavailable", items: [] });
  const safeItems = items as T[];
  return deepFreeze({ phase: safeItems.length ? "ready" : "empty", items: safeItems });
}

function compareApprovals(left: ApprovalSummary, right: ApprovalSummary): number {
  const leftPending = left.visualStatus === "pending" ? 0 : 1;
  const rightPending = right.visualStatus === "pending" ? 0 : 1;
  return leftPending - rightPending || right.requestedAt - left.requestedAt ||
    left.sourceLocalApprovalId.localeCompare(right.sourceLocalApprovalId);
}

export function parseApprovalInboxSource(value: unknown): readonly ApprovalSummary[] | null {
  const record = sourceEnvelope(value);
  const values = asArray(record?.approvals, MAX.approvals);
  if (!record || !values) return null;
  const approvals = values.map(summary);
  if (approvals.some((approval) => approval === null)) return null;
  const safeApprovals = approvals as ApprovalSummary[];
  safeApprovals.sort(compareApprovals);
  return deepFreeze(safeApprovals);
}

export function parseApprovalDetailSource(value: unknown, expectedApprovalId: string): ApprovalDetail | null {
  const expected = validateApprovalId(expectedApprovalId);
  const record = sourceEnvelope(value);
  const projected = summary(record?.approval);
  if (!record || !expected || !projected || projected.sourceLocalApprovalId !== expected) return null;
  const sourceReason = record.approval && asRecord(record.approval)?.reason !== null && asRecord(record.approval)?.reason !== undefined
    ? plainText(asRecord(record.approval)?.reason, 4000)
    : null;
  if (sourceReason === null && asRecord(record.approval)?.reason !== null && asRecord(record.approval)?.reason !== undefined) {
    return null;
  }
  return deepFreeze({
    ...projected,
    sourceReason,
    evidence: section(record.evidence, MAX.evidence, evidence),
    decisionHistory: section(record.decisions, MAX.decisions, decision),
  });
}

export function isApprovalInboxViewEmpty(view: ApprovalInboxView): boolean {
  return view.kind === "inbox" && view.approvals.length === 0;
}
