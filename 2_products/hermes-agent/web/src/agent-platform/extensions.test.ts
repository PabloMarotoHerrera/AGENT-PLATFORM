import { readFileSync } from "node:fs";
import type { ComponentType } from "react";
import { describe, expect, it } from "vitest";

import { parseProductConfiguration, type ProductFeatureState } from "./product-config";
import {
  AGENT_PLATFORM_EXTENSIONS,
  getProductExtensionPosture,
  mergeProductNavigation,
  resolveProductExtensions,
  resolveRegisteredProductExtensions,
  type ProductExtensionDescriptor,
  type ProductExtensionNavigation,
} from "./extensions";
import { filterProtectedPluginManifests, groupShellNavigation } from "./shell";
import type { PluginManifest } from "@/plugins";

const Page: ComponentType = () => null;
const Icon: ComponentType<{ className?: string }> = () => null;
const ACTIVATED_PRODUCT_MODULES = [
  "agent_platform.ui.overview",
  "agent_platform.ui.projects",
  "agent_platform.ui.project_detail",
  "agent_platform.ui.ticket_detail",
  "agent_platform.ui.approvals",
  "agent_platform.ui.approval_detail",
  "agent_platform.ui.executions",
  "agent_platform.ui.execution_detail",
  "agent_platform.ui.settings",
] as const;

function configuration(
  extensionModules: string[],
  featureFlags: Record<string, ProductFeatureState>,
) {
  return parseProductConfiguration({
    schema_version: 1,
    product_id: "agent-platform-hermes",
    product_display_name: "AGENT PLATFORM Hermes",
    product_version: "0.1.0-dev",
    upstream_product_name: "Hermes Agent",
    upstream_version: "0.18.2",
    upstream_commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596",
    feature_flags: featureFlags,
    extension_modules: extensionModules,
    documentation_url: null,
    support_url: null,
  });
}

function descriptor(
  id: string,
  path: string,
  placement: ProductExtensionNavigation["placement"] = { kind: "end" },
): ProductExtensionDescriptor {
  return {
    id,
    owner: "AGENT_PLATFORM",
    featureId: `feature.${id}`,
    visibleWhenExperimental: false,
    route: { path, component: Page, title: id },
    navigation: { groupId: "agent-platform", label: id, icon: Icon, placement },
  };
}

describe("AGENT PLATFORM frontend extensions", () => {
  it("compiles and resolves the reviewed catalog from committed experimental activation", () => {
    expect(AGENT_PLATFORM_EXTENSIONS.map((entry) => entry.id)).toEqual(ACTIVATED_PRODUCT_MODULES);
    expect(AGENT_PLATFORM_EXTENSIONS.map((entry) => entry.route.path)).toEqual([
      "/agent-platform/overview",
      "/agent-platform/projects",
      "/agent-platform/projects/:boardSlug",
      "/agent-platform/projects/:boardSlug/tickets/:taskId",
      "/agent-platform/approvals",
      "/agent-platform/approvals/:approvalId",
      "/agent-platform/executions",
      "/agent-platform/executions/:executionId",
      "/agent-platform/settings",
    ]);
    expect(AGENT_PLATFORM_EXTENSIONS.every((entry) =>
      entry.owner === "AGENT_PLATFORM" &&
      entry.featureId === "agent_platform.product_ui" &&
      entry.visibleWhenExperimental)).toBe(true);
    expect(AGENT_PLATFORM_EXTENSIONS.filter((entry) => entry.navigation).map((entry) => entry.id))
      .toEqual([
        "agent_platform.ui.overview",
        "agent_platform.ui.projects",
        "agent_platform.ui.approvals",
        "agent_platform.ui.executions",
        "agent_platform.ui.settings",
      ]);

    const backendSource = readFileSync(
      new URL("../../../hermes_cli/agent_platform/product_config.py", import.meta.url),
      "utf8",
    );
    expect(backendSource).toContain('"agent_platform.product_ui": FeatureState.EXPERIMENTAL');
    for (const moduleId of ACTIVATED_PRODUCT_MODULES) {
      expect(backendSource).toContain(`"${moduleId}"`);
    }
    const committed = configuration([...ACTIVATED_PRODUCT_MODULES], {
      "agent_platform.product_ui": "experimental",
    });
    const resolved = resolveRegisteredProductExtensions(committed, ["/sessions"]);

    expect(resolved).toEqual(AGENT_PLATFORM_EXTENSIONS);
    expect(getProductExtensionPosture(committed)).toEqual({
      compiledDescriptorCount: 9,
      selectedModuleCount: 9,
      resolvedDescriptorCount: 9,
      registeredRouteCount: 9,
      registeredNavigationCount: 5,
    });
    expect(mergeProductNavigation(
      [{ path: "/sessions", label: "Sessions", icon: Icon }],
      resolved,
    ).map((item) => item.path)).toEqual([
      "/sessions",
      "/agent-platform/overview",
      "/agent-platform/projects",
      "/agent-platform/approvals",
      "/agent-platform/executions",
      "/agent-platform/settings",
    ]);
    expect(groupShellNavigation(
      mergeProductNavigation([{ path: "/sessions", label: "Sessions", icon: Icon }], resolved),
      [],
      {
        "agent-platform": "Synthetic Product",
        "hermes-tools": "Synthetic Upstream Tools",
        extensions: "Extensions",
        administration: "Administration",
      },
    ).map((group) => group.id)).toContain("agent-platform");
  });

  it("keeps dynamic plugins out of every product-owned route shape", () => {
    const manifest = (path: string): PluginManifest => ({
      name: `synthetic-${path}`,
      label: "Synthetic plugin",
      description: "Synthetic plugin",
      icon: "Puzzle",
      version: "1.0.0",
      tab: { path },
      entry: "index.js",
      has_api: false,
      source: "synthetic",
    });
    const filtered = filterProtectedPluginManifests([
      manifest("/kanban"),
      manifest("/agent-platform/projects"),
      manifest("/agent-platform/projects/:boardSlug"),
      manifest("/agent-platform/projects/:boardSlug/tickets/:taskId"),
      manifest("/agent-platform/approvals"),
      manifest("/agent-platform/approvals/:approvalId"),
      manifest("/agent-platform/executions"),
      manifest("/agent-platform/executions/:executionId"),
      manifest("/agent-platform/settings"),
      manifest("/:namespace/*"),
    ]);

    expect(filtered.manifests.map((entry) => entry.tab.path)).toEqual(["/kanban"]);
    expect(filtered.blockedManifestCount).toBe(9);
  });

  it("uses configuration order and enables only explicitly enabled descriptors", () => {
    const first = descriptor("agent_platform.first", "/agent-platform/first");
    const second = descriptor("agent_platform.second", "/agent-platform/second");
    const config = configuration(
      [second.id, first.id],
      {
        [first.featureId]: "disabled",
        [second.featureId]: "enabled",
      },
    );

    expect(resolveProductExtensions(config, [first, second], ["/sessions"])).toEqual([second]);
  });

  it("keeps missing, disabled, unavailable, and unapproved experimental features hidden", () => {
    const values: ProductFeatureState[] = ["disabled", "unavailable", "experimental"];
    const extension = descriptor("agent_platform.example", "/agent-platform/example");

    for (const state of values) {
      const config = configuration([extension.id], { [extension.featureId]: state });
      expect(resolveProductExtensions(config, [extension], ["/sessions"])).toEqual([]);
    }
    expect(resolveProductExtensions(configuration([extension.id], {}), [extension], ["/sessions"]))
      .toEqual([]);
  });

  it("rejects duplicate identifiers, duplicate routes, and built-in route collisions", () => {
    const extension = descriptor("agent_platform.example", "/agent-platform/example");
    const config = configuration([], {});

    expect(() => resolveProductExtensions(config, [extension, extension], ["/sessions"]))
      .toThrow(/duplicate product extension id/);
    expect(() => resolveProductExtensions(
      config,
      [extension, descriptor("agent_platform.other", extension.route.path)],
      ["/sessions"],
    )).toThrow(/duplicate product extension path/);
    expect(() => resolveProductExtensions(
      config,
      [descriptor("agent_platform.collision", "/agent-platform/collision")],
      ["/sessions", "/agent-platform/collision"],
    )).toThrow(/collides with built-in route/);
  });

  it("rejects routes outside the product namespace and ambiguous route patterns", () => {
    const config = configuration([], {});

    expect(() => resolveProductExtensions(
      config,
      [descriptor("agent_platform.outside", "/outside")],
      ["/sessions"],
    )).toThrow(/invalid product extension path/);
    expect(() => resolveProductExtensions(
      config,
      [descriptor("agent_platform.root", "/agent-platform")],
      ["/sessions"],
    )).toThrow(/invalid product extension path/);
    for (const path of [
      "/agent-platform/../sessions",
      "/agent-platform/%2e%2e/sessions",
      "/agent-platform/..\\sessions",
      "/agent-platform/.\t./sessions",
      "/agent-platform/.\n./sessions",
      "/agent-platform/.\r./sessions",
    ]) {
      expect(() => resolveProductExtensions(
        config,
        [descriptor("agent_platform.escape", path)],
        ["/sessions"],
      )).toThrow(/invalid product extension path/);
    }
    expect(() => resolveProductExtensions(
      config,
      [
        descriptor("agent_platform.by_id", "/agent-platform/projects/:projectId"),
        descriptor("agent_platform.by_slug", "/agent-platform/projects/:slug"),
      ],
      ["/sessions"],
    )).toThrow(/ambiguous product extension path/);
  });

  it("requires product navigation entries to use the product group", () => {
    const extension = descriptor("agent_platform.example", "/agent-platform/example");
    const invalid = {
      ...extension,
      navigation: {
        ...extension.navigation!,
        groupId: "administration" as "agent-platform",
      },
    };

    expect(() => resolveProductExtensions(configuration([], {}), [invalid], ["/sessions"]))
      .toThrow(/invalid product navigation group/);
  });

  it("preserves configuration order for multiple entries at one navigation anchor", () => {
    const first = descriptor(
      "agent_platform.first",
      "/agent-platform/first",
      { kind: "after", path: "/sessions" },
    );
    const second = descriptor(
      "agent_platform.second",
      "/agent-platform/second",
      { kind: "after", path: "/sessions" },
    );
    const config = configuration(
      [first.id, second.id],
      { [first.featureId]: "enabled", [second.featureId]: "enabled" },
    );
    const resolved = resolveProductExtensions(config, [second, first], ["/sessions"]);

    expect(mergeProductNavigation(
      [{ path: "/sessions", label: "Sessions", icon: Icon }],
      resolved,
    ).map((item) => [item.path, item.groupId])).toEqual([
      ["/sessions", undefined],
      ["/agent-platform/first", "agent-platform"],
      ["/agent-platform/second", "agent-platform"],
    ]);
  });
});
