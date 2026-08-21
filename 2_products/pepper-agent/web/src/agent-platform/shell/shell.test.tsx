import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { mergeProductNavigation, resolveRegisteredProductExtensions } from "../extensions";
import { parseProductConfiguration } from "../product-config";
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
  control: "CONTROL",
  work: "WORK",
  agents: "AGENTS",
  automation: "AUTOMATION",
  resources: "RESOURCES",
  system: "SYSTEM",
});

const activatedProductExtensionIds = Object.freeze([
  "agent_platform.ui.overview",
  "agent_platform.ui.projects",
  "agent_platform.ui.project_detail",
  "agent_platform.ui.ticket_detail",
  "agent_platform.ui.approvals",
  "agent_platform.ui.approval_detail",
  "agent_platform.ui.executions",
  "agent_platform.ui.execution_detail",
  "agent_platform.ui.settings",
]);

function productConfiguration() {
  return parseProductConfiguration({
    schema_version: 1,
    product_id: "pepper",
    product_display_name: "Pepper",
    product_version: "0.1.0-dev",
    upstream_product_name: "Hermes Agent",
    upstream_version: "0.19.0",
    upstream_commit: "3ef6bbd201263d354fd83ec55b3c306ded2eb72a",
    feature_flags: { "agent_platform.product_ui": "enabled" },
    extension_modules: [...activatedProductExtensionIds],
    documentation_url: null,
    support_url: null,
  });
}

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
  it("creates exactly the six compact Pepper groups in accepted order", () => {
    const groups = groupShellNavigation(
      [
        { path: "/chat", label: "Lead Agent" },
        { path: "/agent-platform/overview", label: "Overview", groupId: "agent-platform" as const },
        { path: "/agent-platform/projects", label: "Projects", groupId: "agent-platform" as const },
        { path: "/skills", label: "Skills" },
        { path: "/cron", label: "Cron" },
        { path: "/files", label: "Files" },
        { path: "/agent-platform/settings", label: "Settings", groupId: "agent-platform" as const },
      ],
      [],
      navigationLabels,
    );

    expect(groups.map((group) => group.id)).toEqual([
      "control",
      "work",
      "agents",
      "automation",
      "resources",
      "system",
    ]);
    expect(groups.map((group) => group.label)).toEqual([
      "CONTROL",
      "WORK",
      "AGENTS",
      "AUTOMATION",
      "RESOURCES",
      "SYSTEM",
    ]);
    expect(groups.map((group) => group.items.map((item) => item.path))).toEqual([
      ["/agent-platform/overview", "/chat"],
      ["/agent-platform/projects"],
      ["/skills"],
      ["/cron"],
      ["/files"],
      ["/agent-platform/settings"],
    ]);
    expect(Object.isFrozen(groups)).toBe(true);
    expect(groups.every((group) => Object.isFrozen(group.items))).toBe(true);
  });

  it("keeps Lead Agent in CONTROL instead of AGENTS", () => {
    const groups = groupShellNavigation(
      [
        { path: "/chat", label: "Lead Agent" },
        { path: "/skills", label: "Skills" },
        { path: "/profiles", label: "Profiles" },
      ],
      [],
      navigationLabels,
    );

    expect(groups.find((group) => group.id === "control")?.items.map((item) => item.label)).toEqual([
      "Lead Agent",
    ]);
    expect(groups.find((group) => group.id === "agents")?.items.map((item) => item.path)).toEqual([
      "/skills",
      "/profiles",
    ]);
  });

  it("maps product routes into compact Pepper IA domains", () => {
    const groups = groupShellNavigation(
      [
        { path: "/agent-platform/overview", label: "Overview", groupId: "agent-platform" as const },
        { path: "/agent-platform/projects", label: "Projects", groupId: "agent-platform" as const },
        { path: "/agent-platform/projects/demo", label: "Project", groupId: "agent-platform" as const },
        { path: "/agent-platform/approvals", label: "Approvals", groupId: "agent-platform" as const },
        { path: "/agent-platform/executions", label: "Executions", groupId: "agent-platform" as const },
        { path: "/agent-platform/settings", label: "Settings", groupId: "agent-platform" as const },
      ],
      [],
      navigationLabels,
    );

    expect(groups.map((group) => [group.id, group.items.map((item) => item.path)])).toEqual([
      ["control", ["/agent-platform/overview"]],
      ["work", [
        "/agent-platform/projects",
        "/agent-platform/projects/demo",
        "/agent-platform/approvals",
        "/agent-platform/executions",
      ]],
      ["system", ["/agent-platform/settings"]],
    ]);
  });

  it("keeps plugin navigation reachable through AUTOMATION without a top-level extension group", () => {
    const groups = groupShellNavigation(
      [
        { path: "/plugins", label: "Plugins" },
        { path: "/webhooks", label: "Webhooks" },
        { path: "/files", label: "Files" },
      ],
      [
        { path: "/kanban", label: "Kanban" },
        { path: "/achievements", label: "Achievements" },
      ],
      navigationLabels,
    );

    expect(groups.map((group) => group.id)).toEqual(["automation", "resources"]);
    expect(groups.find((group) => group.id === "automation")?.items.map((item) => item.path)).toEqual([
      "/plugins",
      "/webhooks",
      "/kanban",
      "/achievements",
    ]);
    expect(groups.map((group) => group.id)).not.toContain("extensions");
  });

  it("accepts legacy label maps from existing callers while emitting compact groups", () => {
    const groups = groupShellNavigation(
      [{ path: "/agent-platform/overview", label: "Overview", groupId: "agent-platform" as const }],
      [],
      {
        "agent-platform": "Synthetic Product",
        "hermes-tools": "Synthetic Upstream Tools",
        extensions: "Extensions",
        administration: "Administration",
      },
    );

    expect(groups.map((group) => group.id)).toEqual(["control"]);
    expect(groups.map((group) => group.label)).toEqual(["CONTROL"]);
  });

  it("omits empty compact groups", () => {
    const groups = groupShellNavigation(
      [{ path: "/sessions", label: "Sessions" }],
      [],
      navigationLabels,
    );

    expect(groups.map((group) => group.id)).toEqual(["work"]);
  });

  it("keeps contextual detail routes resolved but absent from primary navigation", () => {
    const resolved = resolveRegisteredProductExtensions(productConfiguration(), ["/sessions"]);
    const navItems = mergeProductNavigation([], resolved);

    expect(resolved.map((descriptor) => descriptor.route.path)).toEqual([
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
    expect(navItems.map((item) => item.path)).toEqual([
      "/agent-platform/overview",
      "/agent-platform/projects",
      "/agent-platform/approvals",
      "/agent-platform/executions",
      "/agent-platform/settings",
    ]);
    expect(navItems.map((item) => item.path)).not.toContain("/agent-platform/projects/:boardSlug");
    expect(navItems.map((item) => item.path)).not.toContain("/agent-platform/projects/:boardSlug/tickets/:taskId");
    expect(navItems.map((item) => item.path)).not.toContain("/agent-platform/approvals/:approvalId");
    expect(navItems.map((item) => item.path)).not.toContain("/agent-platform/executions/:executionId");
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
