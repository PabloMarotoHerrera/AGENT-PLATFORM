import { Settings2 } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { SafeSettingsPage } from "./safe-settings-page";

export const SAFE_SETTINGS_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.settings",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/settings",
    component: SafeSettingsPage,
    title: "Safe Settings",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Settings",
    icon: Settings2,
    placement: Object.freeze({ kind: "end" }),
  }),
});
