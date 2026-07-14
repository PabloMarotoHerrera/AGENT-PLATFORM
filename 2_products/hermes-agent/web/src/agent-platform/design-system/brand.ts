import type { ProductConfiguration } from "../product-config";

export interface ProductBrandIdentity {
  readonly product: Readonly<{
    id: string;
    displayName: string;
    version: string;
  }>;
  readonly upstream: Readonly<{
    displayName: string;
    version: string;
    commit: string;
    shortCommit: string;
  }>;
}

export function createProductBrandIdentity(
  configuration: ProductConfiguration | null,
): Readonly<ProductBrandIdentity> | null {
  if (configuration === null) return null;

  return Object.freeze({
    product: Object.freeze({
      id: configuration.productId,
      displayName: configuration.productDisplayName,
      version: configuration.productVersion,
    }),
    upstream: Object.freeze({
      displayName: configuration.upstreamProductName,
      version: configuration.upstreamVersion,
      commit: configuration.upstreamCommit,
      shortCommit: configuration.upstreamCommit.slice(0, 12),
    }),
  });
}
