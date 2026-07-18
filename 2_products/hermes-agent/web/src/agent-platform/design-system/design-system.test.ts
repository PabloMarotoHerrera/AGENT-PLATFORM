import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import type { ComponentType } from "react";
import { describe, expect, it } from "vitest";

import {
  mergeProductNavigation,
  resolveProductExtensions,
  type ProductExtensionDescriptor,
} from "../extensions";
import { ProductConfigurationContext } from "../product-config-context";
import { ProductConfigurationProvider } from "../product-config-provider";
import type { ProductConfiguration } from "../product-config";
import { groupShellNavigation } from "../shell";
import { BUILTIN_THEMES } from "../../themes/presets";
import { createProductBrandIdentity } from "./brand";
import {
  PRODUCT_DESIGN_TOKENS,
  type ProductDesignTokenCategory,
} from "./tokens";

const EXPECTED_TOKEN_NAMES = [
  "--agent-platform-surface-canvas",
  "--agent-platform-surface-panel",
  "--agent-platform-surface-subtle",
  "--agent-platform-surface-elevated",
  "--agent-platform-text-primary",
  "--agent-platform-text-secondary",
  "--agent-platform-text-muted",
  "--agent-platform-text-inverse",
  "--agent-platform-border-default",
  "--agent-platform-border-strong",
  "--agent-platform-focus-ring",
  "--agent-platform-action-primary",
  "--agent-platform-action-primary-foreground",
  "--agent-platform-status-success",
  "--agent-platform-status-warning",
  "--agent-platform-status-danger",
  "--agent-platform-status-info",
  "--agent-platform-status-disabled",
  "--agent-platform-status-unavailable",
  "--agent-platform-status-experimental",
  "--agent-platform-font-body",
  "--agent-platform-font-display",
  "--agent-platform-font-mono",
  "--agent-platform-radius-control",
  "--agent-platform-radius-panel",
  "--agent-platform-space-1",
  "--agent-platform-space-2",
  "--agent-platform-space-3",
  "--agent-platform-space-4",
  "--agent-platform-motion-fast",
  "--agent-platform-motion-standard",
] as const;

const TOKEN_CATEGORIES = new Set<ProductDesignTokenCategory>([
  "surface",
  "text",
  "border",
  "action",
  "status",
  "typography",
  "shape",
  "spacing",
  "motion",
]);

const CSS_PATH = fileURLToPath(new URL("./tokens.css", import.meta.url));
const BRAND_SOURCE_PATH = fileURLToPath(new URL("./brand.ts", import.meta.url));
const PROVIDER_SOURCE_PATH = fileURLToPath(
  new URL("../product-config-provider.tsx", import.meta.url),
);
const BACKEND_CONFIG_PATH = fileURLToPath(
  new URL("../../../../hermes_cli/agent_platform/product_config.py", import.meta.url),
);

const CandidatePage: ComponentType = () => null;
const CandidateIcon: ComponentType<{ className?: string }> = () => null;

const COMPILED_DESCRIPTOR_CANDIDATE = Object.freeze({
  id: "agent_platform.ui.candidate",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/candidate",
    component: CandidatePage,
    title: "Candidate",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Candidate",
    icon: CandidateIcon,
    placement: Object.freeze({ kind: "end" }),
  }),
} satisfies ProductExtensionDescriptor);

function makeConfiguration(): ProductConfiguration {
  return Object.freeze({
    schemaVersion: 1,
    productId: "synthetic-product",
    productDisplayName: "Synthetic Product",
    productVersion: "2.3.4-test",
    upstreamProductName: "Synthetic Upstream",
    upstreamVersion: "8.9.0",
    upstreamCommit: "0123456789abcdef0123456789abcdef01234567",
    featureFlags: Object.freeze({ "agent_platform.product_ui": "experimental" as const }),
    extensionModules: Object.freeze([]),
    documentationUrl: null,
    supportUrl: null,
  });
}

describe("product design token catalog", () => {
  it("defines the exact stable token contract", () => {
    expect(PRODUCT_DESIGN_TOKENS).toHaveLength(31);
    expect(PRODUCT_DESIGN_TOKENS.map(({ name }) => name)).toEqual(EXPECTED_TOKEN_NAMES);
    expect(new Set(PRODUCT_DESIGN_TOKENS.map(({ name }) => name)).size).toBe(31);
    expect(PRODUCT_DESIGN_TOKENS.every(({ name }) => name.startsWith("--agent-platform-"))).toBe(
      true,
    );
    expect(PRODUCT_DESIGN_TOKENS.every(({ category }) => TOKEN_CATEGORIES.has(category))).toBe(
      true,
    );
  });

  it("is deeply immutable", () => {
    expect(Object.isFrozen(PRODUCT_DESIGN_TOKENS)).toBe(true);
    expect(PRODUCT_DESIGN_TOKENS.every(Object.isFrozen)).toBe(true);
  });
});

describe("product token stylesheet", () => {
  const css = readFileSync(CSS_PATH, "utf8");
  const reducedMotionStart = css.indexOf("@media (prefers-reduced-motion: reduce)");
  const normalContract = css.slice(0, reducedMotionStart);
  const reducedMotionContract = css.slice(reducedMotionStart);

  it("defines every catalog token once in the normal contract", () => {
    expect(reducedMotionStart).toBeGreaterThan(0);
    for (const { name } of PRODUCT_DESIGN_TOKENS) {
      expect(normalContract.match(new RegExp(`${name}\\s*:`, "g")) ?? []).toHaveLength(1);
    }

    const documented = new Set(PRODUCT_DESIGN_TOKENS.map(({ name }) => name));
    const defined = new Set(css.match(/--agent-platform-[a-z0-9-]+(?=\s*:)/g) ?? []);
    expect(defined).toEqual(documented);
  });

  it("overrides only motion durations for reduced motion", () => {
    expect(reducedMotionContract).toContain("--agent-platform-motion-fast: 0ms");
    expect(reducedMotionContract).toContain("--agent-platform-motion-standard: 0ms");
    for (const { name, category } of PRODUCT_DESIGN_TOKENS) {
      const count = reducedMotionContract.match(new RegExp(`${name}\\s*:`, "g"))?.length ?? 0;
      expect(count).toBe(category === "motion" ? 1 : 0);
    }
  });

  it("contains semantic variables only", () => {
    expect(css).not.toMatch(/#[0-9a-f]{3,8}\b/i);
    expect(css).not.toMatch(/\b(?:rgb|rgba|hsl|hsla)\s*\(/i);
    expect(css).not.toMatch(/url\s*\(|@font-face|@import/i);
    expect(css).not.toMatch(/AGENT PLATFORM|Hermes Agent|\/agent-platform/i);
    expect(css).not.toMatch(/(?:^|\})\s*(?:html|body|#root|\.[a-z])/m);
  });
});

describe("product brand identity", () => {
  it("projects exact product and upstream identity without mutating the source", () => {
    const configuration = makeConfiguration();
    const before = JSON.stringify(configuration);
    const identity = createProductBrandIdentity(configuration);

    expect(identity).toEqual({
      product: {
        id: "synthetic-product",
        displayName: "Synthetic Product",
        version: "2.3.4-test",
      },
      upstream: {
        displayName: "Synthetic Upstream",
        version: "8.9.0",
        commit: "0123456789abcdef0123456789abcdef01234567",
        shortCommit: "0123456789ab",
      },
    });
    expect(JSON.stringify(configuration)).toBe(before);
    expect(Object.isFrozen(identity)).toBe(true);
    expect(Object.isFrozen(identity?.product)).toBe(true);
    expect(Object.isFrozen(identity?.upstream)).toBe(true);
  });

  it("returns null without configuration", () => {
    expect(createProductBrandIdentity(null)).toBeNull();
  });

  it("contains no duplicated production identity constants", () => {
    const source = readFileSync(BRAND_SOURCE_PATH, "utf8");
    for (const forbidden of [
      "AGENT PLATFORM Hermes",
      "Hermes Agent",
      "0.1.0-dev",
      "0.18.2",
      "9de9c25f620ff7f1ce0fd5457d596052d5159596",
    ]) {
      expect(source).not.toContain(forbidden);
    }
  });
});

describe("existing theme compatibility", () => {
  it("provides every inherited field for every built-in theme", () => {
    for (const theme of Object.values(BUILTIN_THEMES)) {
      expect(theme.palette.background.hex).toBeTruthy();
      expect(theme.palette.midground.hex).toBeTruthy();
      expect(theme.palette.foreground.hex).toBeTruthy();
      expect(theme.typography.fontSans).toBeTruthy();
      expect(theme.typography.fontMono).toBeTruthy();
      expect(theme.typography.baseSize).toBeTruthy();
      expect(theme.typography.lineHeight).toBeTruthy();
      expect(theme.typography.letterSpacing).toBeDefined();
      expect(theme.layout.radius).toBeDefined();
      expect(theme.layout.density).toBeDefined();
    }
  });
});

describe("product design-system integration", () => {
  it("loads tokens exactly once without changing provider behavior", () => {
    const providerSource = readFileSync(PROVIDER_SOURCE_PATH, "utf8");
    expect(providerSource.match(/import "\.\/design-system\/tokens\.css";/g) ?? []).toHaveLength(
      1,
    );

    const configuration = makeConfiguration();
    const rendered = ProductConfigurationProvider({ children: "child", value: configuration });
    const props = rendered.props as { children: string; value: ProductConfiguration | null };
    expect(rendered.type).toBe(ProductConfigurationContext.Provider);
    expect(props.value).toBe(configuration);
    expect(props.children).toBe("child");
  });

  it("keeps unselected descriptor candidates inactive under committed activation", () => {
    const backendSource = readFileSync(BACKEND_CONFIG_PATH, "utf8");
    expect(backendSource).toContain('"agent_platform.product_ui": FeatureState.EXPERIMENTAL');
    expect(backendSource).not.toContain('"agent_platform.ui.candidate"');
    const configuration = makeConfiguration();
    const compiledDescriptors = Object.freeze([COMPILED_DESCRIPTOR_CANDIDATE]);

    expect(compiledDescriptors).toHaveLength(1);
    expect(configuration.featureFlags["agent_platform.product_ui"]).toBe("experimental");
    expect(configuration.extensionModules).toEqual([]);

    const resolvedDescriptors = resolveProductExtensions(
      configuration,
      compiledDescriptors,
      ["/sessions"],
    );
    const runtimeProductRoutes = Object.fromEntries(
      resolvedDescriptors.map((descriptor) => [
        descriptor.route.path,
        descriptor.route.component,
      ]),
    );
    const navigation = mergeProductNavigation(
      [{ path: "/sessions", label: "Sessions", icon: CandidateIcon }],
      resolvedDescriptors,
    );
    const navigationGroups = groupShellNavigation(navigation, [], {
      "agent-platform": "Synthetic Product",
      "hermes-tools": "Synthetic Upstream Tools",
      extensions: "Extensions",
      administration: "Administration",
    });

    expect(resolvedDescriptors).toEqual([]);
    expect(Object.keys(runtimeProductRoutes)).toEqual([]);
    expect(
      navigationGroups.some((group) => group.id === "agent-platform"),
    ).toBe(false);
    expect(navigationGroups.map((group) => group.id)).toEqual(["hermes-tools"]);
  });
});
