import { fetchJSON } from "@/lib/api";

export const PRODUCT_FEATURE_STATES = [
  "enabled",
  "disabled",
  "unavailable",
  "experimental",
] as const;

export type ProductFeatureState = (typeof PRODUCT_FEATURE_STATES)[number];

export interface ProductConfiguration {
  readonly schemaVersion: 1;
  readonly productId: string;
  readonly productDisplayName: string;
  readonly productVersion: string;
  readonly upstreamProductName: string;
  readonly upstreamVersion: string;
  readonly upstreamCommit: string;
  readonly featureFlags: Readonly<Record<string, ProductFeatureState>>;
  readonly extensionModules: readonly string[];
  readonly documentationUrl: string | null;
  readonly supportUrl: string | null;
}

const CONFIGURATION_KEYS = new Set([
  "schema_version",
  "product_id",
  "product_display_name",
  "product_version",
  "upstream_product_name",
  "upstream_version",
  "upstream_commit",
  "feature_flags",
  "extension_modules",
  "documentation_url",
  "support_url",
]);
const STABLE_IDENTIFIER = /^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$/;
const COMMIT_SHA = /^[0-9a-f]{40}$/;
const FEATURE_STATES = new Set<string>(PRODUCT_FEATURE_STATES);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function readString(value: unknown, field: string): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${field} must be a non-empty string`);
  }
  return value;
}

function readIdentifier(value: unknown, field: string): string {
  const identifier = readString(value, field);
  if (!STABLE_IDENTIFIER.test(identifier)) {
    throw new Error(`${field} must be a stable identifier`);
  }
  return identifier;
}

function readOptionalUrl(value: unknown, field: string): string | null {
  if (value === null) return null;
  const url = new URL(readString(value, field));
  if (url.protocol !== "http:" && url.protocol !== "https:") {
    throw new Error(`${field} must use HTTP or HTTPS`);
  }
  if (url.username || url.password) {
    throw new Error(`${field} must not contain credentials`);
  }
  return url.toString();
}

export function parseProductConfiguration(raw: unknown): ProductConfiguration {
  if (!isRecord(raw)) throw new Error("product configuration must be an object");
  const keys = Object.keys(raw);
  if (keys.length !== CONFIGURATION_KEYS.size || keys.some((key) => !CONFIGURATION_KEYS.has(key))) {
    throw new Error("product configuration contains missing or unknown fields");
  }
  if (raw.schema_version !== 1) throw new Error("unsupported product configuration schema");
  if (!isRecord(raw.feature_flags)) throw new Error("feature_flags must be an object");
  if (!Array.isArray(raw.extension_modules)) throw new Error("extension_modules must be an array");

  const featureFlags: Record<string, ProductFeatureState> = {};
  for (const [featureId, state] of Object.entries(raw.feature_flags)) {
    readIdentifier(featureId, "feature_flags key");
    if (typeof state !== "string" || !FEATURE_STATES.has(state)) {
      throw new Error(`feature_flags.${featureId} has an invalid state`);
    }
    featureFlags[featureId] = state as ProductFeatureState;
  }

  const extensionModules = raw.extension_modules.map((value, index) =>
    readIdentifier(value, `extension_modules[${index}]`),
  );
  if (new Set(extensionModules).size !== extensionModules.length) {
    throw new Error("extension_modules must contain unique identifiers");
  }

  const upstreamCommit = readString(raw.upstream_commit, "upstream_commit");
  if (!COMMIT_SHA.test(upstreamCommit)) throw new Error("upstream_commit must be a full SHA");

  return Object.freeze({
    schemaVersion: 1,
    productId: readIdentifier(raw.product_id, "product_id"),
    productDisplayName: readString(raw.product_display_name, "product_display_name"),
    productVersion: readString(raw.product_version, "product_version"),
    upstreamProductName: readString(raw.upstream_product_name, "upstream_product_name"),
    upstreamVersion: readString(raw.upstream_version, "upstream_version"),
    upstreamCommit,
    featureFlags: Object.freeze(featureFlags),
    extensionModules: Object.freeze(extensionModules),
    documentationUrl: readOptionalUrl(raw.documentation_url, "documentation_url"),
    supportUrl: readOptionalUrl(raw.support_url, "support_url"),
  });
}

export async function loadProductConfiguration(): Promise<ProductConfiguration | null> {
  try {
    const raw = await fetchJSON<unknown>("/api/agent-platform/product-configuration");
    return parseProductConfiguration(raw);
  } catch {
    return null;
  }
}

export function getProductFeatureState(
  configuration: ProductConfiguration | null,
  featureId: string,
): ProductFeatureState {
  if (configuration === null) return "unavailable";
  return configuration.featureFlags[featureId] ?? "disabled";
}
