import { Activity } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { ExecutionDetailPage } from "./execution-detail-page";
import { ExecutionInspectorPage } from "./execution-inspector-page";

export const EXECUTION_INSPECTOR_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.executions",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/executions",
    component: ExecutionInspectorPage,
    title: "Executions",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Executions",
    icon: Activity,
    placement: Object.freeze({ kind: "end" }),
  }),
});

export const EXECUTION_DETAIL_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.execution_detail",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/executions/:executionId",
    component: ExecutionDetailPage,
    title: "Execution",
  }),
});

export const EXECUTION_INSPECTOR_DESCRIPTORS: readonly ProductExtensionDescriptor[] = Object.freeze([
  EXECUTION_INSPECTOR_DESCRIPTOR,
  EXECUTION_DETAIL_DESCRIPTOR,
]);
