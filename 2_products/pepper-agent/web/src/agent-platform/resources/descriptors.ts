import { FolderOpen } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { ResourcesPage } from "./resources-page";

export const RESOURCES_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.resources",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/resources",
    component: ResourcesPage,
    title: "Resources",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Resources",
    icon: FolderOpen,
    placement: Object.freeze({ kind: "end" }),
  }),
});

export const RESOURCES_DESCRIPTORS: readonly ProductExtensionDescriptor[] = Object.freeze([
  RESOURCES_DESCRIPTOR,
]);
