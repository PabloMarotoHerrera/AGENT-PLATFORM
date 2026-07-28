import type { ProductFeatureState } from "../product-config";

export type SafePersistenceAuthority =
  | "browser-local"
  | "session-local"
  | "existing Hermes display preference"
  | "read-only tracked product configuration"
  | "unavailable";

export type SafeTargetScope =
  | "this browser"
  | "this dashboard session"
  | "all profiles in this browser"
  | "current dashboard backend and this browser"
  | "selected profile context only"
  | "tracked product configuration"
  | "not applicable";

export type SafeImpact =
  | "immediate"
  | "dashboard reload required"
  | "new dashboard session required"
  | "Hermes restart required"
  | "unknown"
  | "not applicable";

export type SafeSettingClassification =
  | "safe_read_write"
  | "safe_read_only"
  | "unavailable"
  | "blocked_sensitive"
  | "blocked_executable";

export type SafeSettingsPhase =
  | "loading"
  | "ready"
  | "stale"
  | "error"
  | "unavailable"
  | "not_configured";

export interface SafeProductIdentity {
  readonly id: string;
  readonly displayName: string;
  readonly version: string;
}

export interface SafeUpstreamIdentity {
  readonly displayName: string;
  readonly version: string;
  readonly commit: string;
}

export interface SafeFeatureState {
  readonly id: string;
  readonly state: ProductFeatureState;
  readonly sourceAuthority: "read-only tracked product configuration";
}

export interface SafeExtensionPosture {
  readonly compiledDescriptorCount: number;
  readonly selectedModuleCount: number;
  readonly resolvedDescriptorCount: number;
  readonly registeredRouteCount: number;
  readonly registeredNavigationCount: number;
}

export interface SafePreferenceAllowedValue {
  readonly id: string;
  readonly label: string;
  readonly description: string | null;
}

export interface SafePreferenceDescriptor {
  readonly id: string;
  readonly label: string;
  readonly description: string;
  readonly classification: SafeSettingClassification;
  readonly currentValueId: string | null;
  readonly currentValueLabel: string;
  readonly allowedValues: readonly SafePreferenceAllowedValue[];
  readonly selectedProfileContext: string;
  readonly persistenceAuthority: SafePersistenceAuthority;
  readonly targetScope: SafeTargetScope;
  readonly impact: SafeImpact;
  readonly writeAvailable: boolean;
  readonly sourceOwner: string;
  readonly lastSuccessfulWriteAt: number | null;
}

export interface SafeSettingsSnapshot {
  readonly product: SafeProductIdentity;
  readonly upstream: SafeUpstreamIdentity;
  readonly features: readonly SafeFeatureState[];
  readonly extensionPosture: SafeExtensionPosture;
  readonly selectedProfileContext: string;
  readonly preferences: readonly SafePreferenceDescriptor[];
  readonly sourceLabel: string;
  readonly observedAt: number;
}

export interface SafeSettingsDataState {
  readonly phase: SafeSettingsPhase;
  readonly snapshot: SafeSettingsSnapshot | null;
  readonly lastSuccessAt: number | null;
  readonly refreshing: boolean;
}

const IDENTIFIER = /^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$/;
const COMMIT = /^[0-9a-f]{40}$/;
const FEATURE_STATES = new Set<ProductFeatureState>([
  "enabled",
  "disabled",
  "unavailable",
  "experimental",
]);
const PERSISTENCE = new Set<SafePersistenceAuthority>([
  "browser-local",
  "session-local",
  "existing Hermes display preference",
  "read-only tracked product configuration",
  "unavailable",
]);
const TARGETS = new Set<SafeTargetScope>([
  "this browser",
  "this dashboard session",
  "all profiles in this browser",
  "current dashboard backend and this browser",
  "selected profile context only",
  "tracked product configuration",
  "not applicable",
]);
const IMPACTS = new Set<SafeImpact>([
  "immediate",
  "dashboard reload required",
  "new dashboard session required",
  "Hermes restart required",
  "unknown",
  "not applicable",
]);
const CLASSIFICATIONS = new Set<SafeSettingClassification>([
  "safe_read_write",
  "safe_read_only",
  "unavailable",
  "blocked_sensitive",
  "blocked_executable",
]);

function record(value: unknown, field: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${field} must be an object`);
  }
  return value as Record<string, unknown>;
}

function exactKeys(source: Record<string, unknown>, keys: readonly string[], field: string) {
  const actual = Object.keys(source);
  if (actual.length !== keys.length || actual.some((key) => !keys.includes(key))) {
    throw new Error(`${field} contains missing or unknown fields`);
  }
}

function text(value: unknown, field: string, max: number): string {
  if (typeof value !== "string" || value.length === 0 || value.length > max) {
    throw new Error(`${field} must be bounded text`);
  }
  if ([...value].some((character) => {
    const code = character.charCodeAt(0);
    return code < 32 || code === 127;
  })) {
    throw new Error(`${field} contains control characters`);
  }
  return value;
}

function identifier(value: unknown, field: string): string {
  const parsed = text(value, field, 128);
  if (!IDENTIFIER.test(parsed)) throw new Error(`${field} must be a stable identifier`);
  return parsed;
}

function count(value: unknown, field: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < 0 || value > 10_000) {
    throw new Error(`${field} must be a bounded count`);
  }
  return value;
}

function timestamp(value: unknown, field: string): number {
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
    throw new Error(`${field} must be a timestamp`);
  }
  return value;
}

function optionalTimestamp(value: unknown, field: string): number | null {
  return value === null ? null : timestamp(value, field);
}

function enumValue<T extends string>(value: unknown, values: ReadonlySet<T>, field: string): T {
  if (typeof value !== "string" || !values.has(value as T)) {
    throw new Error(`${field} is not an allowed value`);
  }
  return value as T;
}

function allowedValue(value: unknown, field: string): SafePreferenceAllowedValue {
  const source = record(value, field);
  exactKeys(source, ["id", "label", "description"], field);
  return Object.freeze({
    id: identifier(source.id, `${field}.id`),
    label: text(source.label, `${field}.label`, 300),
    description: source.description === null
      ? null
      : text(source.description, `${field}.description`, 1_000),
  });
}

function preference(value: unknown, index: number): SafePreferenceDescriptor {
  const field = `preferences[${index}]`;
  const source = record(value, field);
  exactKeys(source, [
    "id",
    "label",
    "description",
    "classification",
    "currentValueId",
    "currentValueLabel",
    "allowedValues",
    "selectedProfileContext",
    "persistenceAuthority",
    "targetScope",
    "impact",
    "writeAvailable",
    "sourceOwner",
    "lastSuccessfulWriteAt",
  ], field);
  if (!Array.isArray(source.allowedValues) || source.allowedValues.length > 100) {
    throw new Error(`${field}.allowedValues must be bounded`);
  }
  const allowedValues = source.allowedValues.map((item, allowedIndex) =>
    allowedValue(item, `${field}.allowedValues[${allowedIndex}]`));
  const allowedIds = new Set(allowedValues.map((item) => item.id));
  if (allowedIds.size !== allowedValues.length) throw new Error(`${field} has duplicate values`);
  const currentValueId = source.currentValueId === null
    ? null
    : identifier(source.currentValueId, `${field}.currentValueId`);
  const writeAvailable = source.writeAvailable;
  const classification = enumValue(source.classification, CLASSIFICATIONS, `${field}.classification`);
  const impact = enumValue(source.impact, IMPACTS, `${field}.impact`);
  if (typeof writeAvailable !== "boolean") throw new Error(`${field}.writeAvailable must be boolean`);
  if (writeAvailable !== (classification === "safe_read_write")) {
    throw new Error(`${field} classification and write availability must agree`);
  }
  if (writeAvailable && (allowedValues.length === 0 || impact === "unknown")) {
    throw new Error(`${field} cannot be writable without trusted values and known impact`);
  }
  if (currentValueId !== null && !allowedIds.has(currentValueId)) {
    throw new Error(`${field}.currentValueId is not trusted`);
  }
  return Object.freeze({
    id: identifier(source.id, `${field}.id`),
    label: text(source.label, `${field}.label`, 300),
    description: text(source.description, `${field}.description`, 1_000),
    classification,
    currentValueId,
    currentValueLabel: text(source.currentValueLabel, `${field}.currentValueLabel`, 300),
    allowedValues: Object.freeze(allowedValues),
    selectedProfileContext: text(source.selectedProfileContext, `${field}.selectedProfileContext`, 128),
    persistenceAuthority: enumValue(source.persistenceAuthority, PERSISTENCE, `${field}.persistenceAuthority`),
    targetScope: enumValue(source.targetScope, TARGETS, `${field}.targetScope`),
    impact,
    writeAvailable,
    sourceOwner: text(source.sourceOwner, `${field}.sourceOwner`, 300),
    lastSuccessfulWriteAt: optionalTimestamp(source.lastSuccessfulWriteAt, `${field}.lastSuccessfulWriteAt`),
  });
}

export function parseSafeSettingsSnapshot(value: unknown): SafeSettingsSnapshot {
  const source = record(value, "safe settings snapshot");
  exactKeys(source, [
    "product",
    "upstream",
    "features",
    "extensionPosture",
    "selectedProfileContext",
    "preferences",
    "sourceLabel",
    "observedAt",
  ], "safe settings snapshot");
  const product = record(source.product, "product");
  exactKeys(product, ["id", "displayName", "version"], "product");
  const upstream = record(source.upstream, "upstream");
  exactKeys(upstream, ["displayName", "version", "commit"], "upstream");
  const posture = record(source.extensionPosture, "extensionPosture");
  exactKeys(posture, [
    "compiledDescriptorCount",
    "selectedModuleCount",
    "resolvedDescriptorCount",
    "registeredRouteCount",
    "registeredNavigationCount",
  ], "extensionPosture");
  if (!Array.isArray(source.features) || source.features.length > 100) {
    throw new Error("features must be bounded");
  }
  const features = source.features.map((value, index) => {
    const item = record(value, `features[${index}]`);
    exactKeys(item, ["id", "state", "sourceAuthority"], `features[${index}]`);
    if (item.sourceAuthority !== "read-only tracked product configuration") {
      throw new Error(`features[${index}] has an invalid authority`);
    }
    return Object.freeze({
      id: identifier(item.id, `features[${index}].id`),
      state: enumValue(item.state, FEATURE_STATES, `features[${index}].state`),
      sourceAuthority: "read-only tracked product configuration" as const,
    });
  });
  if (new Set(features.map((feature) => feature.id)).size !== features.length) {
    throw new Error("features contain duplicate identifiers");
  }
  if (!Array.isArray(source.preferences) || source.preferences.length > 100) {
    throw new Error("preferences must be bounded");
  }
  const preferences = source.preferences.map(preference);
  if (new Set(preferences.map((item) => item.id)).size !== preferences.length) {
    throw new Error("preferences contain duplicate identifiers");
  }
  const commit = text(upstream.commit, "upstream.commit", 40);
  if (!COMMIT.test(commit)) throw new Error("upstream.commit must be immutable");
  return Object.freeze({
    product: Object.freeze({
      id: identifier(product.id, "product.id"),
      displayName: text(product.displayName, "product.displayName", 300),
      version: text(product.version, "product.version", 128),
    }),
    upstream: Object.freeze({
      displayName: text(upstream.displayName, "upstream.displayName", 300),
      version: text(upstream.version, "upstream.version", 128),
      commit,
    }),
    features: Object.freeze(features),
    extensionPosture: Object.freeze({
      compiledDescriptorCount: count(posture.compiledDescriptorCount, "compiledDescriptorCount"),
      selectedModuleCount: count(posture.selectedModuleCount, "selectedModuleCount"),
      resolvedDescriptorCount: count(posture.resolvedDescriptorCount, "resolvedDescriptorCount"),
      registeredRouteCount: count(posture.registeredRouteCount, "registeredRouteCount"),
      registeredNavigationCount: count(posture.registeredNavigationCount, "registeredNavigationCount"),
    }),
    selectedProfileContext: text(source.selectedProfileContext, "selectedProfileContext", 128),
    preferences: Object.freeze(preferences),
    sourceLabel: text(source.sourceLabel, "sourceLabel", 300),
    observedAt: timestamp(source.observedAt, "observedAt"),
  });
}

export const INITIAL_SAFE_SETTINGS_DATA_STATE: SafeSettingsDataState = Object.freeze({
  phase: "loading",
  snapshot: null,
  lastSuccessAt: null,
  refreshing: false,
});
