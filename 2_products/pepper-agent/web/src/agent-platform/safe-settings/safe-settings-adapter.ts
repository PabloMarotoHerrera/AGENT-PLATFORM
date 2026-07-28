import { LOCALE_META } from "@/i18n/context";
import type { Locale } from "@/i18n/types";
import { FONT_CHOICES, THEME_DEFAULT_FONT_ID } from "@/themes/fonts";
import { BUILTIN_THEMES } from "@/themes/presets";

import type { ProductConfiguration } from "../product-config";
import {
  parseSafeSettingsSnapshot,
  type SafeExtensionPosture,
  type SafePreferenceAllowedValue,
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

export interface SafeSettingsAdapter {
  readonly readSafeSettings: (signal?: AbortSignal) => Promise<SafeSettingsSnapshot>;
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

export function createSafeSettingsAdapter(
  getSource: () => unknown,
  now: () => number = Date.now,
): SafeSettingsAdapter {
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
    const theme = trustedCurrent(THEME_VALUES, current.themeId);
    const font = trustedCurrent(FONT_VALUES, current.fontId);
    const language = trustedCurrent(LANGUAGE_VALUES, current.localeId);
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
          description: "Trusted built-in Hermes dashboard presets only; shown read-only here. Custom themes and CSS are excluded.",
          classification: "safe_read_only",
          currentValueId: theme.id,
          currentValueLabel: theme.label,
          allowedValues: THEME_VALUES,
          selectedProfileContext,
          persistenceAuthority: "existing Hermes display preference",
          targetScope: "current dashboard backend and this browser",
          impact: "dashboard reload required",
          writeAvailable: false,
          sourceOwner: "Hermes ThemeProvider and dashboard theme preference",
          lastSuccessfulWriteAt: null,
        },
        {
          id: "font",
          label: "Curated font",
          description: "Curated local identifiers and source-owned stylesheet URLs, shown read-only here; arbitrary font URLs are excluded.",
          classification: "safe_read_only",
          currentValueId: font.id,
          currentValueLabel: font.label,
          allowedValues: FONT_VALUES,
          selectedProfileContext,
          persistenceAuthority: "existing Hermes display preference",
          targetScope: "current dashboard backend and this browser",
          impact: "dashboard reload required",
          writeAvailable: false,
          sourceOwner: "Hermes curated font catalog and dashboard font preference",
          lastSuccessfulWriteAt: null,
        },
        {
          id: "language",
          label: "Language",
          description: "Existing supported Hermes dashboard locale identifiers only, shown read-only here.",
          classification: "safe_read_only",
          currentValueId: language.id,
          currentValueLabel: language.label,
          allowedValues: LANGUAGE_VALUES,
          selectedProfileContext,
          persistenceAuthority: "browser-local",
          targetScope: "all profiles in this browser",
          impact: "immediate",
          writeAvailable: false,
          sourceOwner: "Hermes I18nProvider locale catalog",
          lastSuccessfulWriteAt: null,
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
      sourceLabel: "Validated product configuration and existing Hermes display contexts (read-only)",
      observedAt: now(),
    });
  };

  return Object.freeze({ readSafeSettings });
}
