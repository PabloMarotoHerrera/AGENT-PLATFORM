import type { PluginManifest } from "@/plugins";

export const AGENT_PLATFORM_NAVIGATION_GROUP_ID = "agent-platform" as const;

export type ShellNavigationGroupId =
  | typeof AGENT_PLATFORM_NAVIGATION_GROUP_ID
  | "hermes-tools"
  | "extensions"
  | "administration";

export interface ShellNavigationItem {
  readonly groupId?: typeof AGENT_PLATFORM_NAVIGATION_GROUP_ID;
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

const HERMES_TOOL_PATHS = new Set([
  "/chat",
  "/sessions",
  "/files",
  "/models",
  "/cron",
  "/skills",
]);

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

export function groupShellNavigation<T extends ShellNavigationItem>(
  coreItems: readonly T[],
  extensionItems: readonly T[],
  labels: Readonly<Record<ShellNavigationGroupId, string>>,
): readonly ShellNavigationGroup<T>[] {
  const grouped: Record<ShellNavigationGroupId, T[]> = {
    "agent-platform": [],
    "hermes-tools": [],
    extensions: [...extensionItems],
    administration: [],
  };

  for (const item of coreItems) {
    if (item.groupId === AGENT_PLATFORM_NAVIGATION_GROUP_ID) {
      grouped["agent-platform"].push(item);
    } else if (HERMES_TOOL_PATHS.has(item.path)) {
      grouped["hermes-tools"].push(item);
    } else {
      grouped.administration.push(item);
    }
  }

  const order: readonly ShellNavigationGroupId[] = [
    "agent-platform",
    "hermes-tools",
    "extensions",
    "administration",
  ];

  return Object.freeze(
    order.flatMap((id) =>
      grouped[id].length === 0
        ? []
        : [
            Object.freeze({
              id,
              items: Object.freeze(grouped[id]),
              label: labels[id],
            }),
          ],
    ),
  );
}
