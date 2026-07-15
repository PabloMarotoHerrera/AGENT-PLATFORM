import { ShieldCheck } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { ApprovalDetailPage } from "./approval-detail-page";
import { ApprovalInboxPage } from "./approval-inbox-page";

export const APPROVAL_INBOX_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.approvals",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/approvals",
    component: ApprovalInboxPage,
    title: "Approval Inbox",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Approvals",
    icon: ShieldCheck,
    placement: Object.freeze({ kind: "end" }),
  }),
});

export const APPROVAL_DETAIL_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.approval_detail",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/approvals/:approvalId",
    component: ApprovalDetailPage,
    title: "Approval",
  }),
});

export const APPROVAL_INBOX_DESCRIPTORS: readonly ProductExtensionDescriptor[] = Object.freeze([
  APPROVAL_INBOX_DESCRIPTOR,
  APPROVAL_DETAIL_DESCRIPTOR,
]);
