export type FrontendQualityEvidenceSource =
  | "unit"
  | "component"
  | "integration"
  | "browser"
  | "human"
  | "source-inspection"
  | "build";

export type FrontendQualityGateState =
  | "passed"
  | "passed_with_constraints"
  | "failed"
  | "unavailable"
  | "not_applicable";

export type FrontendQualitySurfaceId =
  | "application-shell"
  | "runtime-overview"
  | "projects"
  | "project-detail"
  | "ticket-detail"
  | "approval-inbox"
  | "approval-detail"
  | "execution-inspector"
  | "execution-detail"
  | "safe-settings";

export type FrontendQualityPageState =
  | "loading"
  | "ready"
  | "empty"
  | "stale"
  | "error"
  | "unavailable"
  | "not_configured";

export type FrontendQualityThemeId = "hermes-teal" | "nous-blue";
export type FrontendQualityViewportId =
  | "mobile_small"
  | "mobile_standard"
  | "tablet"
  | "desktop_standard"
  | "desktop_wide";

export type FrontendQualityAllowedAction =
  | "refresh"
  | "filter"
  | "navigate"
  | "trusted-display-write"
  | "retry-trusted-write";

export type FrontendQualityForbiddenCapability =
  | "work-mutation"
  | "approval-decision"
  | "execution-control"
  | "assignment-dispatch"
  | "feature-toggle"
  | "extension-module-selection"
  | "provider-model-mutation"
  | "secret-input"
  | "oauth-action"
  | "plugin-action"
  | "mcp-action"
  | "hook-action"
  | "gateway-lifecycle"
  | "worker-lifecycle"
  | "agent-lifecycle"
  | "raw-config";

export interface FrontendQualityRoute {
  readonly descriptorId: string;
  readonly path: string;
  readonly navigation: "top-level" | "contextual" | "none";
  readonly requiredQualifiers: readonly string[];
}

export interface FrontendQualityState {
  readonly id: FrontendQualityPageState;
  readonly meaning: string;
  readonly mustRetainLastSafeSnapshot: boolean;
}

export interface FrontendQualityTheme {
  readonly id: FrontendQualityThemeId;
  readonly sourceThemeId: "default" | "nous-blue";
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualityViewport {
  readonly id: FrontendQualityViewportId;
  readonly width: number;
  readonly height: number;
  readonly automated: boolean;
}

export interface FrontendQualityKeyboardCheck {
  readonly id: string;
  readonly controls: readonly FrontendQualityAllowedAction[];
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualitySemanticCheck {
  readonly id: string;
  readonly requirements: readonly string[];
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualitySecurityCheck {
  readonly id: string;
  readonly forbiddenPatterns: readonly string[];
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualityActivationCheck {
  readonly compiledDescriptorCount: number;
  readonly resolvedDescriptorCount: number;
  readonly runtimeRouteCount: number;
  readonly navigationItemCount: number;
  readonly productUiFeature: "disabled";
  readonly extensionModules: readonly string[];
}

export interface FrontendQualitySurface {
  readonly id: FrontendQualitySurfaceId;
  readonly label: string;
  readonly routes: readonly FrontendQualityRoute[];
  readonly states: readonly FrontendQualityPageState[];
  readonly authority: string;
  readonly allowedActions: readonly FrontendQualityAllowedAction[];
  readonly forbiddenCapabilities: readonly FrontendQualityForbiddenCapability[];
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualityConstraint {
  readonly id: string;
  readonly description: string;
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualityBrowserResult {
  readonly stateId: string;
  readonly status: FrontendQualityGateState;
  readonly viewport: FrontendQualityViewportId;
  readonly theme: FrontendQualityThemeId;
  readonly evidence: readonly FrontendQualityEvidenceSource[];
}

export interface FrontendQualityGateResult {
  readonly status: FrontendQualityGateState;
  readonly surfaces: readonly FrontendQualitySurface[];
  readonly activation: FrontendQualityActivationCheck;
  readonly constraints: readonly FrontendQualityConstraint[];
  readonly browserResults: readonly FrontendQualityBrowserResult[];
}

function deepFreezeQuality<T>(value: T): T {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value as Record<string, unknown>)) deepFreezeQuality(child);
    Object.freeze(value);
  }
  return value;
}

export function freezeQualityArray<T>(items: readonly T[]): readonly T[] {
  return deepFreezeQuality([...items]);
}
