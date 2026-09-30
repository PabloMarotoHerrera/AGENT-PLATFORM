import { PlugZap, Workflow } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { AutomationPage, IntegrationsPage } from "./automation-integrations-page";

export const AUTOMATION_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.automation",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/automation",
    component: AutomationPage,
    title: "Automation",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Automation",
    icon: Workflow,
    placement: Object.freeze({ kind: "end" }),
  }),
});

export const INTEGRATIONS_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.integrations",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/integrations",
    component: IntegrationsPage,
    title: "Integrations",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Integrations",
    icon: PlugZap,
    placement: Object.freeze({ kind: "end" }),
  }),
});

export const AUTOMATION_INTEGRATIONS_DESCRIPTORS: readonly ProductExtensionDescriptor[] = Object.freeze([
  AUTOMATION_DESCRIPTOR,
  INTEGRATIONS_DESCRIPTOR,
]);
