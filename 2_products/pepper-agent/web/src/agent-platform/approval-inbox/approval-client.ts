import {
  parseApprovalDetailSource,
  parseApprovalInboxSource,
  validateApprovalId,
  validateProfileName,
  type ApprovalInboxRequest,
  type ApprovalInboxView,
} from "./contract";

export const APPROVAL_LIVE_SOURCE_CLASSIFICATION = Object.freeze({
  classification: "safe_partial_read_source" as const,
  productionAvailability: "unavailable" as const,
  reason: "Hermes staged writes have durable Python reads but no safe authenticated dashboard list/detail endpoint.",
});

function safeProfile(profile: string): string | null {
  return profile === "" ? "" : validateProfileName(profile);
}

function profileSuffix(profile: string): string | null {
  const validated = safeProfile(profile);
  if (validated === null) return null;
  return validated ? `?${new URLSearchParams({ profile: validated })}` : "";
}

export function buildApprovalInboxPath(profile: string): string | null {
  const suffix = profileSuffix(profile);
  return suffix === null ? null : `/agent-platform/approvals${suffix}`;
}

export function buildApprovalDetailPath(approvalId: string, profile: string): string | null {
  const id = validateApprovalId(approvalId);
  const suffix = profileSuffix(profile);
  if (!id || suffix === null) return null;
  return `/agent-platform/approvals/${encodeURIComponent(id)}${suffix}`;
}

/**
 * Production deliberately has no HTTP call here. The audited durable source
 * exposes only raw local Python reads, so inventing a dashboard endpoint or
 * scraping another surface would cross the P15.C3A authority boundary.
 */
export async function listApprovals(profile: string): Promise<unknown> {
  return safeProfile(profile) === null ? null : null;
}

export async function getApproval(approvalId: string, profile: string): Promise<unknown> {
  return validateApprovalId(approvalId) && safeProfile(profile) !== null ? null : null;
}

export type ApprovalInboxLoader = (
  request: ApprovalInboxRequest,
  profile: string,
) => Promise<ApprovalInboxView | null>;

export const loadApprovalInboxRequest: ApprovalInboxLoader = async (request, profile) => {
  if (request.kind === "inbox") {
    const approvals = parseApprovalInboxSource(await listApprovals(profile));
    return approvals ? Object.freeze({ kind: "inbox", approvals }) : null;
  }
  const id = validateApprovalId(request.approvalId);
  if (!id) return null;
  const approval = parseApprovalDetailSource(await getApproval(id, profile), id);
  return approval ? Object.freeze({ kind: "detail", approval }) : null;
};
