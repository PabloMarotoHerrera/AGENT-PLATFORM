import { readFileSync } from "node:fs";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import type { ProductBrandIdentity } from "../design-system";
import { ProductBrandLockup } from "./brand-lockup";
import {
  filterProtectedPluginManifests,
  groupShellNavigation,
  isAgentPlatformRoutePath,
} from "./navigation";
import type { PluginManifest } from "@/plugins";

const identity: Readonly<ProductBrandIdentity> = Object.freeze({
  product: Object.freeze({
    id: "synthetic-product",
    displayName: "Synthetic Product",
    version: "2.3.4-test",
  }),
  upstream: Object.freeze({
    displayName: "Synthetic Upstream",
    version: "8.9.0",
    commit: "0123456789abcdef0123456789abcdef01234567",
    shortCommit: "0123456789ab",
  }),
});

const navigationLabels = Object.freeze({
  "agent-platform": identity.product.displayName,
  "hermes-tools": `${identity.upstream.displayName} Tools`,
  extensions: "Extensions",
  administration: "Administration",
});

function manifest(path: string, override?: string): PluginManifest {
  return {
    name: `synthetic-${path}`,
    label: "Synthetic extension",
    description: "Synthetic extension manifest",
    icon: "Puzzle",
    version: "1.0.0",
    tab: { path, override },
    entry: "index.js",
    has_api: false,
    source: "synthetic",
  };
}

describe("product brand lockup", () => {
  it("renders configuration-projected product and upstream identity as text", () => {
    const markup = renderToStaticMarkup(
      <ProductBrandLockup fallback={<span>Fallback</span>} identity={identity} variant="sidebar" />,
    );

    expect(markup).toContain("Synthetic Product");
    expect(markup).toContain("2.3.4-test");
    expect(markup).toContain("Synthetic Upstream");
    expect(markup).toContain("8.9.0");
    expect(markup).toContain("0123456789ab");
    expect(markup).not.toContain("Fallback");
  });

  it("preserves the supplied Hermes fallback when product identity is unavailable", () => {
    expect(renderToStaticMarkup(
      <ProductBrandLockup fallback={<span>Hermes fallback</span>} identity={null} variant="mobile" />,
    )).toBe("<span>Hermes fallback</span>");
  });

  it("renders the short upstream commit visibly in the mobile treatment", () => {
    const markup = renderToStaticMarkup(
      <ProductBrandLockup fallback={null} identity={identity} variant="mobile" />,
    );

    expect(markup).toContain("8.9.0 @ 0123456789ab");
  });
});

describe("shell navigation", () => {
  it("creates stable non-empty groups while preserving relative item order", () => {
    const groups = groupShellNavigation(
      [
        { path: "/sessions", label: "Sessions" },
        { path: "/analytics", label: "Analytics" },
        { path: "/agent-platform/overview", label: "Overview", groupId: "agent-platform" as const },
        { path: "/models", label: "Models" },
        { path: "/logs", label: "Logs" },
        { path: "/agent-platform/settings", label: "Settings", groupId: "agent-platform" as const },
      ],
      [
        { path: "/kanban", label: "Kanban" },
        { path: "/achievements", label: "Achievements" },
      ],
      navigationLabels,
    );

    expect(groups.map((group) => group.id)).toEqual([
      "agent-platform",
      "hermes-tools",
      "extensions",
      "administration",
    ]);
    expect(groups.map((group) => group.items.map((item) => item.path))).toEqual([
      ["/agent-platform/overview", "/agent-platform/settings"],
      ["/sessions", "/models"],
      ["/kanban", "/achievements"],
      ["/analytics", "/logs"],
    ]);
    expect(groups.map((group) => group.label)).toEqual([
      identity.product.displayName,
      `${identity.upstream.displayName} Tools`,
      "Extensions",
      "Administration",
    ]);
    expect(Object.isFrozen(groups)).toBe(true);
    expect(groups.every((group) => Object.isFrozen(group.items))).toBe(true);
  });

  it("does not render empty product or extension groups", () => {
    const groups = groupShellNavigation(
      [{ path: "/sessions", label: "Sessions" }],
      [],
      navigationLabels,
    );

    expect(groups.map((group) => group.id)).toEqual(["hermes-tools"]);
  });

  it("does not hardcode product or upstream identity labels in navigation source", () => {
    const source = readFileSync(new URL("./navigation.ts", import.meta.url), "utf8");

    expect(source).not.toContain('"Pepper"');
    expect(source).not.toContain('"Hermes Tools"');
    expect(source).not.toContain('"Hermes Agent"');
  });
});

describe("protected product namespace", () => {
  it("matches only the root and descendants", () => {
    expect(isAgentPlatformRoutePath("/agent-platform")).toBe(true);
    expect(isAgentPlatformRoutePath("/agent-platform/overview")).toBe(true);
    expect(isAgentPlatformRoutePath("/AGENT-PLATFORM/overview")).toBe(true);
    expect(isAgentPlatformRoutePath("/%61gent-platform/overview")).toBe(true);
    expect(isAgentPlatformRoutePath("/agent-platform-other")).toBe(false);
    expect(isAgentPlatformRoutePath("/sessions")).toBe(false);
  });

  it("filters dynamic path and override claims without exposing manifest details", () => {
    const accepted = manifest("/kanban");
    const scopedDynamic = manifest("/plugins/:pluginId");
    const filtered = filterProtectedPluginManifests([
      accepted,
      scopedDynamic,
      manifest("/agent-platform/projects"),
      manifest("/replacement", "/agent-platform/settings"),
      manifest("/*"),
      manifest("/:namespace"),
      manifest("/replacement", "/:namespace/*"),
      manifest("\\agent-platform\\projects"),
      manifest("/prefix?/:namespace/*"),
      manifest("/safe?/agent-platform??/projects"),
      manifest("/agent-platfor?m/*"),
      manifest("/*?"),
      manifest("/safe??/agent-platformx??/x"),
      manifest("/safe/../agent-platform/projects"),
    ]);

    expect(filtered.manifests).toEqual([accepted, scopedDynamic]);
    expect(filtered.blockedManifestCount).toBe(12);
    expect(Object.isFrozen(filtered)).toBe(true);
    expect(Object.isFrozen(filtered.manifests)).toBe(true);
  });
});
