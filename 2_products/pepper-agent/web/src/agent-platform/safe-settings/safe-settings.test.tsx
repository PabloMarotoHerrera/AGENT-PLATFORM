import { renderToStaticMarkup } from "react-dom/server";
import { afterEach, describe, expect, it, vi } from "vitest";

import { parseProductConfiguration, type ProductConfiguration } from "../product-config";
import {
  parseSafeSettingsSnapshot,
  type SafeSettingsDataState,
  type SafeSettingsSnapshot,
} from "./contract";
import { SAFE_SETTINGS_DESCRIPTOR } from "./descriptor";
import {
  createSafeSettingsAdapter,
  SafeSettingsUnavailableError,
  type SafeSettingsAdapter,
  type SafeSettingsSourceContext,
} from "./safe-settings-adapter";
import { SafeSettingsView } from "./safe-settings-page";
import {
  createSafeSettingsController,
  SAFE_SETTINGS_POLL_MS,
  SAFE_SETTINGS_REQUEST_TIMEOUT_MS,
  type SafeSettingsState,
} from "./use-safe-settings";

const ACTIVATED_PRODUCT_EXTENSION_IDS = Object.freeze([
  "agent_platform.ui.overview",
  "agent_platform.ui.projects",
  "agent_platform.ui.project_detail",
  "agent_platform.ui.ticket_detail",
  "agent_platform.ui.approvals",
  "agent_platform.ui.approval_detail",
  "agent_platform.ui.executions",
  "agent_platform.ui.execution_detail",
  "agent_platform.ui.settings",
]);

function configuration(
  featureFlags: Record<string, string> = { "agent_platform.product_ui": "enabled" },
  extensionModules: readonly string[] = ACTIVATED_PRODUCT_EXTENSION_IDS,
): ProductConfiguration {
  return parseProductConfiguration({
    schema_version: 1,
    product_id: "pepper",
    product_display_name: "Pepper",
    product_version: "0.1.0-dev",
    upstream_product_name: "Hermes Agent",
    upstream_version: "0.19.0",
    upstream_commit: "3ef6bbd201263d354fd83ec55b3c306ded2eb72a",
    feature_flags: featureFlags,
    extension_modules: extensionModules,
    documentation_url: null,
    support_url: null,
  });
}

function source(overrides: Partial<SafeSettingsSourceContext> = {}): SafeSettingsSourceContext {
  return {
    productConfiguration: configuration(),
    selectedProfileContext: "reviewer",
    extensionPosture: {
      compiledDescriptorCount: 9,
      selectedModuleCount: 9,
      resolvedDescriptorCount: 9,
      registeredRouteCount: 9,
      registeredNavigationCount: 5,
    },
    themeId: "default",
    fontId: "theme",
    localeId: "en",
    densityId: "comfortable",
    ...overrides,
  };
}

async function snapshot(overrides: Partial<SafeSettingsSourceContext> = {}): Promise<SafeSettingsSnapshot> {
  return createSafeSettingsAdapter(() => source(overrides), () => 1_700_000_000_000)
    .readSafeSettings();
}

function readyState(value: SafeSettingsSnapshot): SafeSettingsState {
  return {
    phase: "ready",
    snapshot: value,
    lastSuccessAt: 1_700_000_000_000,
    refreshing: false,
  };
}

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("Pepper safe settings projection", () => {
  it("projects Pepper identity, activated extension posture, and read-only preference facts", async () => {
    const value = await snapshot();

    expect(value.product).toEqual({
      id: "pepper",
      displayName: "Pepper",
      version: "0.1.0-dev",
    });
    expect(value.upstream).toEqual({
      displayName: "Hermes Agent",
      version: "0.19.0",
      commit: "3ef6bbd201263d354fd83ec55b3c306ded2eb72a",
    });
    expect(value.features).toEqual([{
      id: "agent_platform.product_ui",
      state: "enabled",
      sourceAuthority: "read-only tracked product configuration",
    }]);
    expect(value.extensionPosture).toEqual({
      compiledDescriptorCount: 9,
      selectedModuleCount: 9,
      resolvedDescriptorCount: 9,
      registeredRouteCount: 9,
      registeredNavigationCount: 5,
    });
    expect(value.preferences.map((item) => [item.id, item.classification, item.writeAvailable]))
      .toEqual([
        ["theme", "safe_read_only", false],
        ["font", "safe_read_only", false],
        ["language", "safe_read_only", false],
        ["layout-density", "unavailable", false],
        ["navigation", "unavailable", false],
      ]);
    expect(Object.isFrozen(value)).toBe(true);
    expect(Object.isFrozen(value.preferences[0]?.allowedValues)).toBe(true);
  });

  it("accepts every feature state but rejects unsafe snapshot mutations", async () => {
    const value = await snapshot({
      productConfiguration: configuration({
        "feature.enabled": "enabled",
        "feature.disabled": "disabled",
        "feature.unavailable": "unavailable",
        "feature.experimental": "experimental",
      }),
    });
    expect(value.features.map((item) => item.state)).toEqual([
      "enabled", "disabled", "unavailable", "experimental",
    ]);

    const raw = JSON.parse(JSON.stringify(value)) as Record<string, unknown>;
    (raw.features as Array<Record<string, unknown>>)[0]!.state = "unknown";
    expect(() => parseSafeSettingsSnapshot(raw)).toThrow(/allowed value/);
  });

  it("does not retain raw source objects or blocked and sensitive fields", async () => {
    const blocked = {
      api_key: "SECRET_API_VALUE",
      provider_token: "SECRET_PROVIDER_TOKEN",
      oauth_state: "SECRET_OAUTH_STATE",
      private_endpoint: "https://private.invalid/token",
      env: { TOKEN: "SECRET_ENV" },
      raw_yaml: "gateway:\n  command: rm -rf private",
      filesystem_path: "C:\\private\\settings.yaml",
    };
    const poisoned = { ...configuration(), ...blocked } as ProductConfiguration;
    const rawSource = source({ productConfiguration: poisoned });
    const value = await createSafeSettingsAdapter(() => rawSource).readSafeSettings();
    const serialized = JSON.stringify(value);

    for (const secret of [
      "SECRET_API_VALUE",
      "SECRET_PROVIDER_TOKEN",
      "SECRET_OAUTH_STATE",
      "https://private.invalid/token",
      "SECRET_ENV",
      "rm -rf private",
      "C:\\private\\settings.yaml",
    ]) {
      expect(serialized).not.toContain(secret);
    }
    expect(value).not.toBe(rawSource);
    expect(serialized).not.toContain("SECRET_");
  });

  it("uses only trusted built-in themes, curated fonts, and supported locales", async () => {
    const value = await snapshot();
    const byId = Object.fromEntries(value.preferences.map((item) => [item.id, item]));

    expect(byId.theme?.allowedValues.some((item) => item.id === "nous-blue")).toBe(true);
    expect(byId.font?.allowedValues.some((item) => item.id === "inter")).toBe(true);
    expect(byId.language?.allowedValues.some((item) => item.id === "en")).toBe(true);
    expect(JSON.stringify(byId.theme)).not.toContain("customCSS");
    expect(JSON.stringify(byId.font)).not.toContain("fonts.googleapis.com");
  });

  it("excludes untrusted current values without silently selecting a default", async () => {
    const value = await snapshot({ themeId: "https://evil.invalid/theme.css" });
    const theme = value.preferences.find((item) => item.id === "theme");
    expect(theme?.currentValueId).toBeNull();
    expect(theme?.currentValueLabel).toBe("Current value excluded");
    expect(theme?.writeAvailable).toBe(false);
  });
});

describe("Pepper safe settings read-only boundary", () => {
  it("reads safe preference posture without network, storage, or reload side effects", async () => {
    const fetchMock = vi.fn();
    const localStorageSet = vi.fn();
    const reload = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("window", {
      localStorage: { setItem: localStorageSet, getItem: vi.fn() },
      location: { reload },
    });
    const adapter = createSafeSettingsAdapter(() => source());
    const value = await adapter.readSafeSettings();

    expect(value.preferences.every((preference) => !preference.writeAvailable)).toBe(true);
    expect(fetchMock).not.toHaveBeenCalled();
    expect(localStorageSet).not.toHaveBeenCalled();
    expect(reload).not.toHaveBeenCalled();
  });

  it("rejects snapshots whose classification disagrees with write availability", async () => {
    const raw = JSON.parse(JSON.stringify(await snapshot())) as Record<string, unknown>;
    const preferences = raw.preferences as Array<Record<string, unknown>>;
    preferences[0]!.writeAvailable = true;
    expect(() => parseSafeSettingsSnapshot(raw)).toThrow(/classification and write availability/);
  });
});

describe("safe settings polling", () => {
  it("loads, refreshes manually, retains stale data, and never overlaps reads", async () => {
    const value = await snapshot();
    let reject = false;
    let finish!: (value: SafeSettingsSnapshot) => void;
    const readSafeSettings = vi.fn(() => reject
      ? Promise.reject(new Error("private transport failure"))
      : new Promise<SafeSettingsSnapshot>((resolve) => { finish = resolve; }));
    const adapter: SafeSettingsAdapter = {
      readSafeSettings,
    };
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(adapter, (state) => states.push(state));
    const initial = controller.start();
    expect(await controller.refresh()).toBe(false);
    expect(readSafeSettings).toHaveBeenCalledTimes(1);
    finish(value);
    expect(await initial).toBe(true);
    expect(states.at(-1)?.phase).toBe("ready");

    reject = true;
    expect(await controller.refresh()).toBe(false);
    expect(states.at(-1)?.phase).toBe("stale");
    expect(states.at(-1)?.snapshot).toBe(value);
    controller.stop();
  });

  it("aborts a read at fifteen seconds and suppresses late results after stop", async () => {
    vi.useFakeTimers();
    const value = await snapshot();
    const readSafeSettings = vi.fn((signal?: AbortSignal) => new Promise<SafeSettingsSnapshot>((resolve, reject) => {
      signal?.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")));
      setTimeout(() => resolve(value), 60_000);
    }));
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(
      { readSafeSettings },
      (state) => states.push(state),
    );
    const pending = controller.start();
    await vi.advanceTimersByTimeAsync(SAFE_SETTINGS_REQUEST_TIMEOUT_MS);
    expect(await pending).toBe(false);
    expect(states.at(-1)?.phase).toBe("error");

    const lateController = createSafeSettingsController(
      { readSafeSettings: () => Promise.resolve(value) },
      (state) => states.push(state),
    );
    const late = lateController.start();
    lateController.stop();
    await late;
    expect(states.at(-1)?.phase).not.toBe("ready");
  });

  it("uses recursive ten-second polling", async () => {
    vi.useFakeTimers();
    const value = await snapshot();
    const adapter: SafeSettingsAdapter = {
      readSafeSettings: vi.fn(async () => value),
    };
    const controller = createSafeSettingsController(adapter, () => {});
    await controller.start();
    await vi.advanceTimersByTimeAsync(SAFE_SETTINGS_POLL_MS);
    expect(adapter.readSafeSettings).toHaveBeenCalledTimes(2);
    controller.stop();
  });

  it("maps an absent validated product source to unavailable", async () => {
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(
      {
        readSafeSettings: () => Promise.reject(new SafeSettingsUnavailableError("unavailable")),
      },
      (state) => states.push(state),
    );
    expect(await controller.start()).toBe(false);
    expect(states.at(-1)?.phase).toBe("unavailable");
    controller.stop();
  });
});

describe("safe settings page and descriptor", () => {
  it("renders identity, read-only activation, catalogs, and excluded boundaries without write controls", async () => {
    const html = renderToStaticMarkup(
      <SafeSettingsView
        state={readyState(await snapshot())}
        refresh={() => {}}
      />,
    );
    for (const text of [
      "Safe Settings",
      "Pepper",
      "Hermes Agent",
      "agent_platform.product_ui",
      "disabled",
      "Feature and module activation is read-only in P15.C3A",
      "later governed activation task owns any tracked activation decision",
      "Trusted catalog",
      "This Pepper reconciliation candidate does not write display preferences",
      "Layout density",
      "Navigation preference",
      "Excluded settings boundary",
      "No secrets are exposed",
      "No raw configuration fallback exists",
    ]) {
      expect(html).toContain(text);
    }
    expect(html).not.toContain('role="combobox"');
    expect(html).not.toContain("Apply preference");
    expect(html).not.toContain("Retry safe write");
    expect(html).not.toContain('type="password"');
    expect(html).not.toContain('type="url"');
    expect(html).not.toContain('type="checkbox"');
    expect(html).not.toContain("<textarea");
  });

  it("renders stale, unavailable, and untrusted current-value states", async () => {
    const value = await snapshot({ themeId: "custom-untrusted" });
    const html = renderToStaticMarkup(
      <SafeSettingsView
        state={{ ...readyState(value), phase: "stale" }}
        refresh={() => {}}
      />,
    );
    expect(html).toContain("Stale");
    expect(html).toContain("Current value excluded");
    expect(html).toContain("Unavailable");
    expect(html).not.toContain("custom-untrusted");

    const unavailable: SafeSettingsDataState = {
      phase: "unavailable",
      snapshot: null,
      lastSuccessAt: null,
      refreshing: false,
    };
    const unavailableHtml = renderToStaticMarkup(
      <SafeSettingsView
        state={unavailable}
        refresh={() => {}}
      />,
    );
    expect(unavailableHtml).toContain("Safe settings source unavailable");
  });

  it("declares one inert Settings descriptor under the protected product namespace", () => {
    expect(SAFE_SETTINGS_DESCRIPTOR).toMatchObject({
      id: "agent_platform.ui.settings",
      owner: "AGENT_PLATFORM",
      featureId: "agent_platform.product_ui",
      visibleWhenExperimental: true,
      route: { path: "/agent-platform/settings", title: "Safe Settings" },
      navigation: {
        groupId: "agent-platform",
        label: "Settings",
        placement: { kind: "end" },
      },
    });
  });
});
