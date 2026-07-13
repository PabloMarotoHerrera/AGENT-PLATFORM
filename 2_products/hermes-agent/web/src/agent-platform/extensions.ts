import type { ComponentType } from "react";

import {
  getProductFeatureState,
  type ProductConfiguration,
} from "./product-config";

export interface ProductExtensionNavigation {
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
  readonly icon: ComponentType<{ className?: string }>;
  readonly label: string;
  readonly labelKey?: string;
  readonly path: string;
}

// P13 registers reviewed, statically imported descriptors here. Backend data
// can select an ID but can never provide an import path or executable code.
export const AGENT_PLATFORM_EXTENSIONS: readonly ProductExtensionDescriptor[] = Object.freeze([]);

function validateDescriptors(
  descriptors: readonly ProductExtensionDescriptor[],
  reservedPaths: ReadonlySet<string>,
): ReadonlyMap<string, ProductExtensionDescriptor> {
  const byId = new Map<string, ProductExtensionDescriptor>();
  const routePaths = new Set<string>();

  for (const descriptor of descriptors) {
    if (byId.has(descriptor.id)) throw new Error(`duplicate product extension id: ${descriptor.id}`);
    if (!descriptor.route.path.startsWith("/") || descriptor.route.path.includes("*")) {
      throw new Error(`invalid product extension path: ${descriptor.route.path}`);
    }
    if (routePaths.has(descriptor.route.path)) {
      throw new Error(`duplicate product extension path: ${descriptor.route.path}`);
    }
    if (reservedPaths.has(descriptor.route.path)) {
      throw new Error(`product extension path collides with built-in route: ${descriptor.route.path}`);
    }
    const placement = descriptor.navigation?.placement;
    if (placement && placement.kind !== "end" && !reservedPaths.has(placement.path)) {
      throw new Error(`product navigation anchor is not a built-in route: ${placement.path}`);
    }
    byId.set(descriptor.id, descriptor);
    routePaths.add(descriptor.route.path);
  }

  return byId;
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
