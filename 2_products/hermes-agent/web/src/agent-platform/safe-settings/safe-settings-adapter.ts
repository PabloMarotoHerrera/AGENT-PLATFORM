import { fetchJSON } from "@/lib/api";
import { LOCALE_META } from "@/i18n/context";
import type { Locale } from "@/i18n/types";
import { FONT_CHOICES, THEME_DEFAULT_FONT_ID } from "@/themes/fonts";
import { BUILTIN_THEMES } from "@/themes/presets";

import type { ProductConfiguration } from "../product-config";
import {
  parseSafeSettingsSnapshot,
  validateSafePreferenceWriteRequest,
  type SafeExtensionPosture,
  type SafePreferenceAllowedValue,
  type SafePreferenceWriteRequest,
  type SafePreferenceWriteResult,
  type SafeSettingsSnapshot,
} from "./contract";

export interface SafeSettingsSourceContext {
  readonly productConfiguration: ProductConfiguration | null;
  readonly selectedProfileContext: string;
  readonly extensionPosture: SafeExtensionPosture;
  readonly themeId: string;
  readonly fontId: string;
  readonly localeId: Locale;
  readonly densityId: unknown;
}

export interface SafeSettingsWriteDependencies {
  readonly applyTheme: (id: string) => void;
  readonly applyFont: (id: string) => void;
  readonly applyLocale: (id: Locale) => void;
  readonly persistTheme?: (id: string, signal?: AbortSignal) => Promise<unknown>;
  readonly persistFont?: (id: string, signal?: AbortSignal) => Promise<unknown>;
  readonly persistLocale?: (id: Locale, signal?: AbortSignal) => Promise<unknown>;
}

export interface SafeSettingsAdapter {
  readonly readSafeSettings: (signal?: AbortSignal) => Promise<SafeSettingsSnapshot>;
  readonly writeSafePreference: (
    request: unknown,
    signal?: AbortSignal,
  ) => Promise<SafePreferenceWriteResult>;
}

export class SafeSettingsUnavailableError extends Error {}

const PROFILE = /^[a-z0-9][a-z0-9_-]{0,63}$/;
const THEME_VALUES: readonly SafePreferenceAllowedValue[] = Object.freeze(
  Object.values(BUILTIN_THEMES).map((theme) => Object.freeze({
    id: theme.name,
    label: theme.label,
    description: theme.description,
  })),
);
const FONT_VALUES: readonly SafePreferenceAllowedValue[] = Object.freeze([
  Object.freeze({
    id: THEME_DEFAULT_FONT_ID,
    label: "Theme default",
    description: "Use the active trusted theme's curated font stack.",
  }),
  ...FONT_CHOICES.map((font) => Object.freeze({
    id: font.id,
    label: font.label,
    description: `Curated ${font.category} identifier.`,
  })),
]);
const LANGUAGE_VALUES: readonly SafePreferenceAllowedValue[] = Object.freeze(
  Object.entries(LOCALE_META).map(([id, metadata]) => Object.freeze({
    id,
    label: metadata.name,
    description: "Existing Hermes dashboard locale.",
  })),
);
const DENSITY_VALUES: readonly SafePreferenceAllowedValue[] = Object.freeze([
  Object.freeze({ id: "compact", label: "Compact", description: "Theme-derived compact spacing." }),
  Object.freeze({ id: "comfortable", label: "Comfortable", description: "Theme-derived standard spacing." }),
  Object.freeze({ id: "spacious", label: "Spacious", description: "Theme-derived roomier spacing." }),
]);
const WRITE_RECONCILIATION_MS = 15_000;

function profileLabel(value: string): string {
  if (value === "") return "Current dashboard profile";
  return PROFILE.test(value) ? value : "Unavailable profile context";
}

function trustedCurrent(
  values: readonly SafePreferenceAllowedValue[],
  value: unknown,
): { id: string | null; label: string } {
  if (typeof value !== "string") return { id: null, label: "Not configured" };
  const match = values.find((item) => item.id === value);
  return match ? { id: match.id, label: match.label } : { id: null, label: "Current value excluded" };
}

function confirmedPreferenceResponse(
  value: unknown,
  field: "theme" | "font" | "locale",
  expected: string,
) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
  const source = value as Record<string, unknown>;
  return source.ok === true && source[field] === expected;
}

export function createSafeSettingsAdapter(
  getSource: () => unknown,
  writes: SafeSettingsWriteDependencies,
  now: () => number = Date.now,
): SafeSettingsAdapter {
  const lastWrites = new Map<string, number>();
  const pendingValues = new Map<string, { readonly id: string; readonly expiresAt: number }>();

  const reconciledValue = (preferenceId: string, currentValue: string): string => {
    const pending = pendingValues.get(preferenceId);
    if (!pending) return currentValue;
    if (pending.id === currentValue || now() >= pending.expiresAt) {
      pendingValues.delete(preferenceId);
      return currentValue;
    }
    return pending.id;
  };

  const source = (): SafeSettingsSourceContext => {
    const value = getSource();
    if (value === null || typeof value !== "object" || Array.isArray(value)) {
      throw new SafeSettingsUnavailableError("Safe settings source is unavailable");
    }
    return value as SafeSettingsSourceContext;
  };

  const readSafeSettings = async (signal?: AbortSignal): Promise<SafeSettingsSnapshot> => {
    if (signal?.aborted) throw new DOMException("Aborted", "AbortError");
    const current = source();
    const configuration = current.productConfiguration;
    if (configuration === null) {
      throw new SafeSettingsUnavailableError("Validated product configuration is unavailable");
    }
    const selectedProfileContext = profileLabel(current.selectedProfileContext);
    const theme = trustedCurrent(THEME_VALUES, reconciledValue("theme", current.themeId));
    const font = trustedCurrent(FONT_VALUES, reconciledValue("font", current.fontId));
    const language = trustedCurrent(LANGUAGE_VALUES, reconciledValue("language", current.localeId));
    const density = trustedCurrent(DENSITY_VALUES, current.densityId);
    return parseSafeSettingsSnapshot({
      product: {
        id: configuration.productId,
        displayName: configuration.productDisplayName,
        version: configuration.productVersion,
      },
      upstream: {
        displayName: configuration.upstreamProductName,
        version: configuration.upstreamVersion,
        commit: configuration.upstreamCommit,
      },
      features: Object.entries(configuration.featureFlags).map(([id, state]) => ({
        id,
        state,
        sourceAuthority: "read-only tracked product configuration",
      })),
      extensionPosture: current.extensionPosture,
      selectedProfileContext,
      preferences: [
        {
          id: "theme",
          label: "Theme",
          description: "Trusted built-in Hermes dashboard presets only; custom themes and CSS are excluded.",
          classification: "safe_read_write",
          currentValueId: theme.id,
          currentValueLabel: theme.label,
          allowedValues: THEME_VALUES,
          selectedProfileContext,
          persistenceAuthority: "existing Hermes display preference",
          targetScope: "current dashboard backend and this browser",
          impact: "dashboard reload required",
          writeAvailable: true,
          sourceOwner: "Hermes ThemeProvider and dashboard theme preference",
          lastSuccessfulWriteAt: lastWrites.get("theme") ?? null,
        },
        {
          id: "font",
          label: "Curated font",
          description: "Curated local identifiers and source-owned stylesheet URLs; arbitrary font URLs are excluded.",
          classification: "safe_read_write",
          currentValueId: font.id,
          currentValueLabel: font.label,
          allowedValues: FONT_VALUES,
          selectedProfileContext,
          persistenceAuthority: "existing Hermes display preference",
          targetScope: "current dashboard backend and this browser",
          impact: "dashboard reload required",
          writeAvailable: true,
          sourceOwner: "Hermes curated font catalog and dashboard font preference",
          lastSuccessfulWriteAt: lastWrites.get("font") ?? null,
        },
        {
          id: "language",
          label: "Language",
          description: "Existing supported Hermes dashboard locale identifiers only.",
          classification: "safe_read_write",
          currentValueId: language.id,
          currentValueLabel: language.label,
          allowedValues: LANGUAGE_VALUES,
          selectedProfileContext,
          persistenceAuthority: "browser-local",
          targetScope: "all profiles in this browser",
          impact: "immediate",
          writeAvailable: true,
          sourceOwner: "Hermes I18nProvider locale catalog",
          lastSuccessfulWriteAt: lastWrites.get("language") ?? null,
        },
        {
          id: "layout-density",
          label: "Layout density",
          description: "Density is owned by the selected theme and has no independent safe setter.",
          classification: "unavailable",
          currentValueId: density.id,
          currentValueLabel: density.label,
          allowedValues: DENSITY_VALUES,
          selectedProfileContext,
          persistenceAuthority: "unavailable",
          targetScope: "not applicable",
          impact: "not applicable",
          writeAvailable: false,
          sourceOwner: "Hermes theme layout definition",
          lastSuccessfulWriteAt: null,
        },
        {
          id: "navigation",
          label: "Navigation preference",
          description: "Desktop sidebar collapse is App-owned and has no reusable Safe Settings setter.",
          classification: "unavailable",
          currentValueId: null,
          currentValueLabel: "Unavailable from this surface",
          allowedValues: [],
          selectedProfileContext,
          persistenceAuthority: "unavailable",
          targetScope: "not applicable",
          impact: "not applicable",
          writeAvailable: false,
          sourceOwner: "Hermes dashboard shell",
          lastSuccessfulWriteAt: null,
        },
      ],
      sourceLabel: "Validated product configuration and existing Hermes display contexts",
      observedAt: now(),
    });
  };

  const writeSafePreference = async (
    value: unknown,
    signal?: AbortSignal,
  ): Promise<SafePreferenceWriteResult> => {
    const snapshot = await readSafeSettings(signal);
    const request: SafePreferenceWriteRequest = validateSafePreferenceWriteRequest(snapshot, value);
    if (signal?.aborted) throw new DOMException("Aborted", "AbortError");
    if (request.preferenceId === "theme") {
      const response = await (writes.persistTheme ?? ((id, activeSignal) => fetchJSON(
        "/api/dashboard/theme",
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: id }),
          signal: activeSignal,
        },
      )))(request.valueId, signal);
      if (signal?.aborted) throw new DOMException("Aborted", "AbortError");
      if (!confirmedPreferenceResponse(response, "theme", request.valueId)) {
        throw new Error("Theme persistence was not confirmed");
      }
      writes.applyTheme(request.valueId);
    } else if (request.preferenceId === "font") {
      const response = await (writes.persistFont ?? ((id, activeSignal) => fetchJSON(
        "/api/dashboard/font",
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ font: id }),
          signal: activeSignal,
        },
      )))(request.valueId, signal);
      if (signal?.aborted) throw new DOMException("Aborted", "AbortError");
      if (!confirmedPreferenceResponse(response, "font", request.valueId)) {
        throw new Error("Font persistence was not confirmed");
      }
      writes.applyFont(request.valueId);
    } else if (request.preferenceId === "language") {
      if (!writes.persistLocale) {
        throw new Error("Language persistence authority is unavailable");
      }
      const response = await writes.persistLocale(request.valueId as Locale, signal);
      if (signal?.aborted) throw new DOMException("Aborted", "AbortError");
      if (!confirmedPreferenceResponse(response, "locale", request.valueId)) {
        throw new Error("Language persistence was not confirmed");
      }
      writes.applyLocale(request.valueId as Locale);
    } else {
      throw new Error("Preference is not available for safe writes");
    }
    const completedAt = now();
    pendingValues.set(request.preferenceId, {
      id: request.valueId,
      expiresAt: completedAt + WRITE_RECONCILIATION_MS,
    });
    lastWrites.set(request.preferenceId, completedAt);
    return Object.freeze({
      ok: true,
      preferenceId: request.preferenceId,
      valueId: request.valueId,
      completedAt,
      message: "Preference saved through its existing safe authority.",
    });
  };

  return Object.freeze({ readSafeSettings, writeSafePreference });
}
