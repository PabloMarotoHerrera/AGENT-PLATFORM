import type { ComponentType } from "react";

import {
  getProductFeatureState,
  type ProductConfiguration,
} from "./product-config";
import { RUNTIME_OVERVIEW_DESCRIPTOR } from "./runtime-overview/descriptor";
import { PROJECTS_TICKETS_DESCRIPTORS } from "./projects-tickets/descriptors";
import { APPROVAL_INBOX_DESCRIPTORS } from "./approval-inbox/descriptors";

export interface ProductExtensionNavigation {
  readonly groupId: "agent-platform";
  readonly icon: ComponentType<{ className?: string }>;
  readonly label: string;
  readonly placement:
    | { readonly kind: "before"; readonly path: string }
    | { readonly kind: "after"; readonly path: string }
    | { readonly kind: "end" };
}

export interface ProductExtensionDescriptor {
  readonly id: string;
  readonly owner: "AGENT_PLATFORM";
  readonly featureId: string;
  readonly visibleWhenExperimental: boolean;
  readonly route: {
    readonly path: string;
    readonly component: ComponentType;
    readonly title: string;
  };
  readonly navigation?: ProductExtensionNavigation;
}

export interface ProductNavigationItem {
  readonly groupId?: "agent-platform";
  readonly icon: ComponentType<{ className?: string }>;
  readonly label: string;
  readonly labelKey?: string;
  readonly path: string;
}

// P13 registers reviewed, statically imported descriptors here. Backend data
// can select an ID but can never provide an import path or executable code.
export const AGENT_PLATFORM_EXTENSIONS: readonly ProductExtensionDescriptor[] = Object.freeze([
  RUNTIME_OVERVIEW_DESCRIPTOR,
  ...PROJECTS_TICKETS_DESCRIPTORS,
  ...APPROVAL_INBOX_DESCRIPTORS,
]);

function validateDescriptors(
  descriptors: readonly ProductExtensionDescriptor[],
  reservedPaths: ReadonlySet<string>,
): ReadonlyMap<string, ProductExtensionDescriptor> {
  const byId = new Map<string, ProductExtensionDescriptor>();
  const routePaths = new Set<string>();
  const routePatterns: string[] = [];

  for (const descriptor of descriptors) {
    if (byId.has(descriptor.id)) throw new Error(`duplicate product extension id: ${descriptor.id}`);
    if (!isValidProductExtensionPath(descriptor.route.path)) {
      throw new Error(`invalid product extension path: ${descriptor.route.path}`);
    }
    if (routePaths.has(descriptor.route.path)) {
      throw new Error(`duplicate product extension path: ${descriptor.route.path}`);
    }
    if (reservedPaths.has(descriptor.route.path)) {
      throw new Error(`product extension path collides with built-in route: ${descriptor.route.path}`);
    }
    if (routePatterns.some((path) => routePatternsOverlap(path, descriptor.route.path))) {
      throw new Error(`ambiguous product extension path: ${descriptor.route.path}`);
    }
    const placement = descriptor.navigation?.placement;
    if (descriptor.navigation && descriptor.navigation.groupId !== "agent-platform") {
      throw new Error(`invalid product navigation group: ${descriptor.navigation.groupId}`);
    }
    if (placement && placement.kind !== "end" && !reservedPaths.has(placement.path)) {
      throw new Error(`product navigation anchor is not a built-in route: ${placement.path}`);
    }
    byId.set(descriptor.id, descriptor);
    routePaths.add(descriptor.route.path);
    routePatterns.push(descriptor.route.path);
  }

  return byId;
}

function isValidProductExtensionPath(path: string): boolean {
  let decodedPath: string;
  let canonicalPath: string;
  try {
    decodedPath = decodeURIComponent(path);
    canonicalPath = new URL(path, "https://agent-platform.invalid").pathname;
  } catch {
    return false;
  }

  return (
    decodedPath === path &&
    canonicalPath === path &&
    path.startsWith("/agent-platform/") &&
    !path.includes("*") &&
    !path.includes("?") &&
    !path.includes("#") &&
    !path.includes("\\") &&
    !path.includes("//") &&
    !path.endsWith("/") &&
    !path.split("/").some((segment) => segment === "." || segment === "..")
  );
}

function routePatternsOverlap(left: string, right: string): boolean {
  const leftSegments = left.split("/");
  const rightSegments = right.split("/");
  if (leftSegments.length !== rightSegments.length) return false;

  return leftSegments.every(
    (segment, index) =>
      segment.toLowerCase() === rightSegments[index]?.toLowerCase() ||
      segment.startsWith(":") ||
      rightSegments[index]?.startsWith(":"),
  );
}

export function resolveProductExtensions(
  configuration: ProductConfiguration | null,
  descriptors: readonly ProductExtensionDescriptor[],
  reservedPaths: readonly string[],
): readonly ProductExtensionDescriptor[] {
  const byId = validateDescriptors(descriptors, new Set(reservedPaths));
  if (configuration === null) return [];

  const enabled: ProductExtensionDescriptor[] = [];
  for (const extensionId of configuration.extensionModules) {
    const descriptor = byId.get(extensionId);
    if (!descriptor) continue;
    const state = getProductFeatureState(configuration, descriptor.featureId);
    if (state === "enabled" || (state === "experimental" && descriptor.visibleWhenExperimental)) {
      enabled.push(descriptor);
    }
  }
  return enabled;
}

export function resolveRegisteredProductExtensions(
  configuration: ProductConfiguration | null,
  reservedPaths: readonly string[],
): readonly ProductExtensionDescriptor[] {
  try {
    return resolveProductExtensions(configuration, AGENT_PLATFORM_EXTENSIONS, reservedPaths);
  } catch {
    return [];
  }
}

export function mergeProductNavigation(
  builtIn: readonly ProductNavigationItem[],
  extensions: readonly ProductExtensionDescriptor[],
): ProductNavigationItem[] {
  const before = new Map<string, ProductNavigationItem[]>();
  const after = new Map<string, ProductNavigationItem[]>();
  const end: ProductNavigationItem[] = [];

  for (const extension of extensions) {
    if (!extension.navigation) continue;
    const item: ProductNavigationItem = {
      groupId: extension.navigation.groupId,
      path: extension.route.path,
      label: extension.navigation.label,
      icon: extension.navigation.icon,
    };
    const placement = extension.navigation.placement;
    if (placement.kind === "end") {
      end.push(item);
      continue;
    }
    const group = placement.kind === "before" ? before : after;
    group.set(placement.path, [...(group.get(placement.path) ?? []), item]);
  }

  return builtIn.flatMap((item) => [
    ...(before.get(item.path) ?? []),
    item,
    ...(after.get(item.path) ?? []),
  ]).concat(end);
}
