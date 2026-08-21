import type { PluginManifest } from "@/plugins";

export const AGENT_PLATFORM_NAVIGATION_GROUP_ID = "agent-platform" as const;

export type CompactShellNavigationGroupId =
  | "control"
  | "work"
  | "agents"
  | "automation"
  | "resources"
  | "system";

export type LegacyShellNavigationGroupId =
  | typeof AGENT_PLATFORM_NAVIGATION_GROUP_ID
  | "hermes-tools"
  | "extensions"
  | "administration";

export type ShellNavigationGroupId =
  | LegacyShellNavigationGroupId
  | CompactShellNavigationGroupId;

export interface ShellNavigationItem {
  readonly groupId?: typeof AGENT_PLATFORM_NAVIGATION_GROUP_ID;
  readonly label?: string;
  readonly path: string;
}

export interface ShellNavigationGroup<T extends ShellNavigationItem> {
  readonly id: ShellNavigationGroupId;
  readonly items: readonly T[];
  readonly label: string;
}

export interface FilteredPluginManifests {
  readonly blockedManifestCount: number;
  readonly manifests: readonly PluginManifest[];
}

const PRODUCT_ROUTE_ROOT = "/agent-platform";

const COMPACT_SHELL_NAVIGATION_GROUP_ORDER: readonly CompactShellNavigationGroupId[] = [
  "control",
  "work",
  "agents",
  "automation",
  "resources",
  "system",
];

const PRODUCT_ROUTE_GROUPS: readonly [RegExp, CompactShellNavigationGroupId][] = [
  [/^\/agent-platform\/overview(?:\/|$)/, "control"],
  [/^\/agent-platform\/(?:projects|approvals|executions)(?:\/|$)/, "work"],
  [/^\/agent-platform\/settings(?:\/|$)/, "system"],
];

const BUILTIN_ROUTE_GROUPS: Readonly<Record<string, CompactShellNavigationGroupId>> = Object.freeze({
  "/chat": "control",
  "/sessions": "work",
  "/files": "resources",
  "/analytics": "control",
  "/models": "resources",
  "/logs": "system",
  "/cron": "automation",
  "/skills": "agents",
  "/plugins": "automation",
  "/mcp": "automation",
  "/pairing": "automation",
  "/channels": "automation",
  "/webhooks": "automation",
  "/profiles": "agents",
  "/config": "system",
  "/env": "system",
  "/system": "system",
  "/docs": "resources",
});

export function isAgentPlatformRoutePath(path: string): boolean {
  let decodedPath = path;
  try {
    decodedPath = decodeURIComponent(path);
  } catch {
    // Keep the raw path so direct namespace claims still fail closed.
  }
  let normalizedPath = decodedPath.replaceAll("\\", "/");
  try {
    normalizedPath = new URL(normalizedPath, "https://agent-platform.invalid").pathname;
  } catch {
    normalizedPath = normalizedPath.split(/[?#]/, 1)[0] ?? normalizedPath;
  }
  normalizedPath = normalizedPath.replace(/\/{2,}/g, "/").toLowerCase();
  return (
    normalizedPath === PRODUCT_ROUTE_ROOT ||
    normalizedPath.startsWith(`${PRODUCT_ROUTE_ROOT}/`)
  );
}

function routePatternCanClaimAgentPlatform(path: string): boolean {
  if (isAgentPlatformRoutePath(path)) return true;

  let decodedPath = path;
  try {
    decodedPath = decodeURIComponent(path);
  } catch {
    return true;
  }
  const segments = (decodedPath.split("#", 1)[0] ?? decodedPath)
    .replaceAll("\\", "/")
    .split("/")
    .filter(Boolean);
  const firstSegment = segments[0]?.toLowerCase();
  if (firstSegment === undefined) return false;
  const hasControlOrSpace = Array.from(firstSegment).some((character) => {
    const codePoint = character.codePointAt(0) ?? 0;
    return codePoint <= 0x20 || codePoint === 0x7f;
  });

  return (
    firstSegment === "agent-platform" ||
    firstSegment.includes(":") ||
    firstSegment.includes("*") ||
    firstSegment.includes("?") ||
    hasControlOrSpace
  );
}

export function filterProtectedPluginManifests(
  manifests: readonly PluginManifest[],
): FilteredPluginManifests {
  const accepted: PluginManifest[] = [];
  let blockedManifestCount = 0;

  for (const manifest of manifests) {
    if (
      routePatternCanClaimAgentPlatform(manifest.tab.path) ||
      (manifest.tab.override !== undefined &&
        routePatternCanClaimAgentPlatform(manifest.tab.override))
    ) {
      blockedManifestCount += 1;
      continue;
    }
    accepted.push(manifest);
  }

  return Object.freeze({
    blockedManifestCount,
    manifests: Object.freeze(accepted),
  });
}

function normalizeNavigationPath(path: string): string {
  try {
    return new URL(path, "https://agent-platform.invalid").pathname.replace(/\/$/, "") || "/";
  } catch {
    return path.split(/[?#]/, 1)[0]?.replace(/\/$/, "") || path;
  }
}

function resolveProductRouteGroup(path: string): CompactShellNavigationGroupId {
  const normalizedPath = normalizeNavigationPath(path).toLowerCase();
  for (const [pattern, groupId] of PRODUCT_ROUTE_GROUPS) {
    if (pattern.test(normalizedPath)) return groupId;
  }
  return "resources";
}

function resolveNavigationGroup(item: ShellNavigationItem): CompactShellNavigationGroupId {
  if (item.groupId === AGENT_PLATFORM_NAVIGATION_GROUP_ID) {
    return resolveProductRouteGroup(item.path);
  }

  const normalizedPath = normalizeNavigationPath(item.path).toLowerCase();
  return BUILTIN_ROUTE_GROUPS[normalizedPath] ?? "automation";
}

function defaultCompactNavigationLabel(id: CompactShellNavigationGroupId): string {
  return id.toUpperCase();
}

function controlNavigationRank(item: ShellNavigationItem): number {
  const normalizedPath = normalizeNavigationPath(item.path).toLowerCase();
  if (normalizedPath === "/agent-platform/overview") return 0;
  if (normalizedPath === "/chat") return 1;
  return 2;
}

export function groupShellNavigation<T extends ShellNavigationItem>(
  coreItems: readonly T[],
  extensionItems: readonly T[],
  labels: Readonly<Partial<Record<ShellNavigationGroupId, string>>>,
): readonly ShellNavigationGroup<T>[] {
  const grouped = Object.fromEntries(
    COMPACT_SHELL_NAVIGATION_GROUP_ORDER.map((id) => [id, [] as T[]]),
  ) as Record<CompactShellNavigationGroupId, T[]>;

  for (const item of [...coreItems, ...extensionItems]) {
    grouped[resolveNavigationGroup(item)].push(item);
  }
  grouped.control.sort((left, right) => controlNavigationRank(left) - controlNavigationRank(right));

  return Object.freeze(
    COMPACT_SHELL_NAVIGATION_GROUP_ORDER.flatMap((id) =>
      grouped[id].length === 0
        ? []
        : [
            Object.freeze({
              id,
              items: Object.freeze(grouped[id]),
              label: labels[id] ?? defaultCompactNavigationLabel(id),
            }),
          ],
    ),
  );
}
