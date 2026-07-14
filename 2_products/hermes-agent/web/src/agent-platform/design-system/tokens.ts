export type ProductDesignTokenCategory =
  | "surface"
  | "text"
  | "border"
  | "action"
  | "status"
  | "typography"
  | "shape"
  | "spacing"
  | "motion";

export interface ProductDesignTokenDefinition {
  readonly name: `--agent-platform-${string}`;
  readonly category: ProductDesignTokenCategory;
}

function token(
  name: ProductDesignTokenDefinition["name"],
  category: ProductDesignTokenCategory,
): Readonly<ProductDesignTokenDefinition> {
  return Object.freeze({ name, category });
}

export const PRODUCT_DESIGN_TOKENS: readonly Readonly<ProductDesignTokenDefinition>[] =
  Object.freeze([
    token("--agent-platform-surface-canvas", "surface"),
    token("--agent-platform-surface-panel", "surface"),
    token("--agent-platform-surface-subtle", "surface"),
    token("--agent-platform-surface-elevated", "surface"),
    token("--agent-platform-text-primary", "text"),
    token("--agent-platform-text-secondary", "text"),
    token("--agent-platform-text-muted", "text"),
    token("--agent-platform-text-inverse", "text"),
    token("--agent-platform-border-default", "border"),
    token("--agent-platform-border-strong", "border"),
    token("--agent-platform-focus-ring", "border"),
    token("--agent-platform-action-primary", "action"),
    token("--agent-platform-action-primary-foreground", "action"),
    token("--agent-platform-status-success", "status"),
    token("--agent-platform-status-warning", "status"),
    token("--agent-platform-status-danger", "status"),
    token("--agent-platform-status-info", "status"),
    token("--agent-platform-status-disabled", "status"),
    token("--agent-platform-status-unavailable", "status"),
    token("--agent-platform-status-experimental", "status"),
    token("--agent-platform-font-body", "typography"),
    token("--agent-platform-font-display", "typography"),
    token("--agent-platform-font-mono", "typography"),
    token("--agent-platform-radius-control", "shape"),
    token("--agent-platform-radius-panel", "shape"),
    token("--agent-platform-space-1", "spacing"),
    token("--agent-platform-space-2", "spacing"),
    token("--agent-platform-space-3", "spacing"),
    token("--agent-platform-space-4", "spacing"),
    token("--agent-platform-motion-fast", "motion"),
    token("--agent-platform-motion-standard", "motion"),
  ]);
