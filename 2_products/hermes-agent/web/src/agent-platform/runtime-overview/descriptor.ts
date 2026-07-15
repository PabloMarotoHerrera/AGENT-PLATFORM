import { Activity } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { RuntimeOverviewPage } from "./runtime-overview-page";

export const RUNTIME_OVERVIEW_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.overview",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/overview",
    component: RuntimeOverviewPage,
    title: "Runtime Overview",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Overview",
    icon: Activity,
    placement: Object.freeze({ kind: "end" }),
  }),
});
