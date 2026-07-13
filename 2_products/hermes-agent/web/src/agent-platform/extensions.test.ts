import type { ComponentType } from "react";
import { describe, expect, it } from "vitest";

import { parseProductConfiguration, type ProductFeatureState } from "./product-config";
import {
  mergeProductNavigation,
  resolveProductExtensions,
  type ProductExtensionDescriptor,
  type ProductExtensionNavigation,
} from "./extensions";

const Page: ComponentType = () => null;
const Icon: ComponentType<{ className?: string }> = () => null;

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
    navigation: { label: id, icon: Icon, placement },
  };
}

describe("AGENT PLATFORM frontend extensions", () => {
  it("uses configuration order and enables only explicitly enabled descriptors", () => {
    const first = descriptor("agent_platform.first", "/product-first");
    const second = descriptor("agent_platform.second", "/product-second");
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
    const extension = descriptor("agent_platform.example", "/product-example");

    for (const state of values) {
      const config = configuration([extension.id], { [extension.featureId]: state });
      expect(resolveProductExtensions(config, [extension], ["/sessions"])).toEqual([]);
    }
    expect(resolveProductExtensions(configuration([extension.id], {}), [extension], ["/sessions"]))
      .toEqual([]);
  });

  it("rejects duplicate identifiers, duplicate routes, and built-in route collisions", () => {
    const extension = descriptor("agent_platform.example", "/product-example");
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
      [descriptor("agent_platform.collision", "/sessions")],
      ["/sessions"],
    )).toThrow(/collides with built-in route/);
  });

  it("preserves configuration order for multiple entries at one navigation anchor", () => {
    const first = descriptor(
      "agent_platform.first",
      "/product-first",
      { kind: "after", path: "/sessions" },
    );
    const second = descriptor(
      "agent_platform.second",
      "/product-second",
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
    ).map((item) => item.path)).toEqual(["/sessions", "/product-first", "/product-second"]);
  });
});
