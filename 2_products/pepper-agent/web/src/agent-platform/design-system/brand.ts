import type { ProductConfiguration } from "../product-config";

export interface ProductBrandIdentity {
  readonly product: Readonly<{
    id: string;
    displayName: string;
    version: string;
    initials: string;
  }>;
  readonly upstream: Readonly<{
    displayName: string;
    version: string;
    commit: string;
    shortCommit: string;
  }>;
  readonly lockup: Readonly<{
    primaryLabel: string;
    decorativeInitials: string;
    upstreamAttribution: string;
    versionLabel: string;
  }>;
}

export function createProductInitials(displayName: string): string {
  const initials = displayName
    .trim()
    .split(/\s+/u)
    .filter(Boolean)
    .map((part) => part.charAt(0))
    .join("")
    .slice(0, 3)
    .toUpperCase();

  return initials || "P";
}

export function createProductBrandIdentity(
  configuration: ProductConfiguration | null,
): Readonly<ProductBrandIdentity> | null {
  if (configuration === null) return null;

  const productInitials = createProductInitials(configuration.productDisplayName);

  return Object.freeze({
    product: Object.freeze({
      id: configuration.productId,
      displayName: configuration.productDisplayName,
      version: configuration.productVersion,
      initials: productInitials,
    }),
    upstream: Object.freeze({
      displayName: configuration.upstreamProductName,
      version: configuration.upstreamVersion,
      commit: configuration.upstreamCommit,
      shortCommit: configuration.upstreamCommit.slice(0, 12),
    }),
    lockup: Object.freeze({
      primaryLabel: configuration.productDisplayName,
      decorativeInitials: productInitials,
      upstreamAttribution: `${configuration.upstreamProductName} ${configuration.upstreamVersion}`,
      versionLabel: configuration.productVersion,
    }),
  });
}
