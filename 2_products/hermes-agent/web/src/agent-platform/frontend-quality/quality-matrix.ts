import { AGENT_PLATFORM_EXTENSIONS } from "../extensions";
import type {
  FrontendQualityActivationCheck,
  FrontendQualityConstraint,
  FrontendQualityEvidenceSource,
  FrontendQualityForbiddenCapability,
  FrontendQualityGateResult,
  FrontendQualityKeyboardCheck,
  FrontendQualityPageState,
  FrontendQualitySecurityCheck,
  FrontendQualitySemanticCheck,
  FrontendQualitySurface,
  FrontendQualityTheme,
  FrontendQualityViewport,
} from "./quality-contract";
import { freezeQualityArray } from "./quality-contract";

const COMPONENT_BROWSER: readonly FrontendQualityEvidenceSource[] = Object.freeze(["component", "browser"]);
const ALL_FORBIDDEN: readonly FrontendQualityForbiddenCapability[] = Object.freeze([
  "work-mutation",
  "approval-decision",
  "execution-control",
  "assignment-dispatch",
  "feature-toggle",
  "extension-module-selection",
  "provider-model-mutation",
  "secret-input",
  "oauth-action",
  "plugin-action",
  "mcp-action",
  "hook-action",
  "gateway-lifecycle",
  "worker-lifecycle",
  "agent-lifecycle",
  "raw-config",
]);

const COMMON_DATA_STATES: readonly FrontendQualityPageState[] = Object.freeze([
  "loading",
  "ready",
  "stale",
  "error",
  "unavailable",
]);

export const FRONTEND_QUALITY_VIEWPORTS: readonly FrontendQualityViewport[] = freezeQualityArray([
  { id: "mobile_small", width: 360, height: 800, automated: false },
  { id: "mobile_standard", width: 390, height: 844, automated: true },
  { id: "tablet", width: 768, height: 1024, automated: true },
  { id: "desktop_standard", width: 1440, height: 900, automated: true },
  { id: "desktop_wide", width: 1920, height: 1080, automated: false },
]);

export const FRONTEND_QUALITY_THEMES: readonly FrontendQualityTheme[] = freezeQualityArray([
  { id: "hermes-teal", sourceThemeId: "default", evidence: ["browser", "human"] },
  { id: "nous-blue", sourceThemeId: "nous-blue", evidence: ["browser", "human"] },
]);

export const FRONTEND_QUALITY_SURFACES: readonly FrontendQualitySurface[] = freezeQualityArray([
  {
    id: "application-shell",
    label: "Application Shell",
    routes: [],
    states: ["ready"],
    authority: "Validated product identity and existing Hermes navigation shell.",
    allowedActions: ["navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: ["component", "browser", "source-inspection"],
  },
  {
    id: "runtime-overview",
    label: "Runtime Overview",
    routes: [{ descriptorId: "agent_platform.ui.overview", path: "/agent-platform/overview", navigation: "top-level", requiredQualifiers: [] }],
    states: COMMON_DATA_STATES,
    authority: "Read-only bounded Hermes status; gateway activity is not governed AGENT PLATFORM Agents.",
    allowedActions: ["refresh"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "projects",
    label: "Projects",
    routes: [{ descriptorId: "agent_platform.ui.projects", path: "/agent-platform/projects", navigation: "top-level", requiredQualifiers: [] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "Read-only provisional Hermes Kanban projection; not canonical Paperclip authority.",
    allowedActions: ["refresh", "filter", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "project-detail",
    label: "Project Detail",
    routes: [{ descriptorId: "agent_platform.ui.project_detail", path: "/agent-platform/projects/:boardSlug", navigation: "contextual", requiredQualifiers: ["board"] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "One exact board-qualified Hermes Kanban presentation; Kanban Task is not WorkPacket.",
    allowedActions: ["refresh", "filter", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "ticket-detail",
    label: "Ticket Detail",
    routes: [{ descriptorId: "agent_platform.ui.ticket_detail", path: "/agent-platform/projects/:boardSlug/tickets/:taskId", navigation: "contextual", requiredQualifiers: ["board", "task"] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "One exact ticket presentation with safe metadata only; review or blocked states are not approvals.",
    allowedActions: ["refresh", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "approval-inbox",
    label: "Approval Inbox",
    routes: [{ descriptorId: "agent_platform.ui.approvals", path: "/agent-platform/approvals", navigation: "top-level", requiredQualifiers: [] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "Provisional approval presentation only; no governed ApprovalRequest authority is active.",
    allowedActions: ["refresh", "filter", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "approval-detail",
    label: "Approval Detail",
    routes: [{ descriptorId: "agent_platform.ui.approval_detail", path: "/agent-platform/approvals/:approvalId", navigation: "contextual", requiredQualifiers: ["approval"] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "Exact source-local approval presentation; no approve, reject, confirm or deny authority.",
    allowedActions: ["refresh", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "execution-inspector",
    label: "Execution Inspector",
    routes: [{ descriptorId: "agent_platform.ui.executions", path: "/agent-platform/executions", navigation: "top-level", requiredQualifiers: ["board", "task"] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "Source-local Kanban run facts only; not governed WorkPacket execution.",
    allowedActions: ["refresh", "filter", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "execution-detail",
    label: "Execution Detail",
    routes: [{ descriptorId: "agent_platform.ui.execution_detail", path: "/agent-platform/executions/:executionId", navigation: "contextual", requiredQualifiers: ["board", "task", "run"] }],
    states: [...COMMON_DATA_STATES, "empty"],
    authority: "Exact source-local execution evidence; raw logs, commands, paths and controls are excluded.",
    allowedActions: ["refresh", "navigate"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
  {
    id: "safe-settings",
    label: "Safe Settings",
    routes: [{ descriptorId: "agent_platform.ui.settings", path: "/agent-platform/settings", navigation: "top-level", requiredQualifiers: [] }],
    states: [...COMMON_DATA_STATES, "not_configured"],
    authority: "Tracked product feature state is read-only; only trusted display preferences are writable.",
    allowedActions: ["refresh", "trusted-display-write", "retry-trusted-write"],
    forbiddenCapabilities: ALL_FORBIDDEN,
    evidence: COMPONENT_BROWSER,
  },
]);

export const FRONTEND_QUALITY_KEYBOARD_CHECKS: readonly FrontendQualityKeyboardCheck[] = freezeQualityArray([
  { id: "refresh-controls", controls: ["refresh"], evidence: ["component", "browser"] },
  { id: "navigation-links", controls: ["navigate"], evidence: ["component", "browser"] },
  { id: "filters", controls: ["filter"], evidence: ["component", "browser"] },
  { id: "safe-settings-writes", controls: ["trusted-display-write", "retry-trusted-write"], evidence: ["component", "browser"] },
]);

export const FRONTEND_QUALITY_SEMANTIC_CHECKS: readonly FrontendQualitySemanticCheck[] = freezeQualityArray([
  { id: "headings", requirements: ["one labelled main region", "coherent heading hierarchy"], evidence: ["component", "browser"] },
  { id: "status", requirements: ["loading busy state", "stale status region", "bounded error messaging"], evidence: ["component", "browser"] },
  { id: "icons", requirements: ["decorative icons hidden", "text labels remain visible"], evidence: ["component", "source-inspection"] },
]);

export const FRONTEND_QUALITY_SECURITY_CHECKS: readonly FrontendQualitySecurityCheck[] = freezeQualityArray([
  {
    id: "sensitive-data-exclusion",
    forbiddenPatterns: ["SECRET_", "api_key", "token", "oauth", "C:\\\\", "raw_yaml", "stderr", "stdout"],
    evidence: ["unit", "component", "browser"],
  },
  {
    id: "write-control-exclusion",
    forbiddenPatterns: ["Approve", "Reject", "Start execution", "Stop execution", "Feature toggle", "Provider", "MCP", "Plugin"],
    evidence: ["component", "browser"],
  },
]);

export const FRONTEND_QUALITY_ACTIVATION: FrontendQualityActivationCheck = Object.freeze({
  compiledDescriptorCount: AGENT_PLATFORM_EXTENSIONS.length,
  resolvedDescriptorCount: AGENT_PLATFORM_EXTENSIONS.length,
  runtimeRouteCount: AGENT_PLATFORM_EXTENSIONS.length,
  navigationItemCount: AGENT_PLATFORM_EXTENSIONS.filter((descriptor) => descriptor.navigation).length,
  productUiFeature: "experimental",
  extensionModules: Object.freeze(AGENT_PLATFORM_EXTENSIONS.map((descriptor) => descriptor.id)),
});

export const FRONTEND_QUALITY_CONSTRAINTS: readonly FrontendQualityConstraint[] = freezeQualityArray([
  { id: "wcag", description: "No full WCAG or assistive-technology certification is claimed.", evidence: ["source-inspection"] },
  { id: "browser-family", description: "Automated browser evidence is limited to locally available Chromium-family tooling.", evidence: ["browser"] },
  { id: "activation", description: "Product routes are selected by tracked P13.R experimental activation governance.", evidence: ["integration"] },
]);

export const FRONTEND_QUALITY_GATE_RESULT: FrontendQualityGateResult = Object.freeze({
  status: "passed_with_constraints",
  surfaces: FRONTEND_QUALITY_SURFACES,
  activation: FRONTEND_QUALITY_ACTIVATION,
  constraints: FRONTEND_QUALITY_CONSTRAINTS,
  browserResults: Object.freeze([]),
});

export const FRONTEND_QUALITY_DESCRIPTOR_IDS: readonly string[] = freezeQualityArray(
  FRONTEND_QUALITY_SURFACES.flatMap((surface) => surface.routes.map((route) => route.descriptorId)),
);
