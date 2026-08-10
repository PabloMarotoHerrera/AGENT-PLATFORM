import { fetchJSON } from "@/lib/api";

import {
  parseApprovalDetailSource,
  parseApprovalInboxSource,
  validateApprovalId,
  validateProfileName,
  type ApprovalInboxRequest,
  type ApprovalInboxView,
} from "./contract";

const APPROVAL_API_ROOT = "/api/agent-platform/approvals";

export const APPROVAL_LIVE_SOURCE_CLASSIFICATION = Object.freeze({
  classification: "safe_controlled_product_source" as const,
  productionAvailability: "available" as const,
  reason: "Hermes staged writes are exposed through authenticated Pepper list/detail/decision endpoints.",
  decisionAuthority: "explicit-human-dashboard-action" as const,
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

export async function listApprovals(profile: string): Promise<unknown> {
  const suffix = profileSuffix(profile);
  return suffix === null ? null : fetchJSON<unknown>(`${APPROVAL_API_ROOT}${suffix}`);
}

export async function getApproval(approvalId: string, profile: string): Promise<unknown> {
  const id = validateApprovalId(approvalId);
  const suffix = profileSuffix(profile);
  return id && suffix !== null ? fetchJSON<unknown>(`${APPROVAL_API_ROOT}/${encodeURIComponent(id)}${suffix}`) : null;
}

export async function decideApproval(
  approvalId: string,
  decision: "approve" | "reject",
  profile: string,
): Promise<unknown> {
  const id = validateApprovalId(approvalId);
  const suffix = profileSuffix(profile);
  if (!id || suffix === null) return null;
  return fetchJSON<unknown>(
    `${APPROVAL_API_ROOT}/${encodeURIComponent(id)}/decision${suffix}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision }),
    },
  );
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
