import { renderToStaticMarkup } from "react-dom/server";
import { afterEach, describe, expect, it, vi } from "vitest";

import { parseProductConfiguration, type ProductConfiguration } from "../product-config";
import {
  parseSafeSettingsSnapshot,
  type SafePreferenceWriteResult,
  type SafePreferenceWriteState,
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

function configuration(
  featureFlags: Record<string, string> = { "agent_platform.product_ui": "disabled" },
): ProductConfiguration {
  return parseProductConfiguration({
    schema_version: 1,
    product_id: "agent-platform-hermes",
    product_display_name: "AGENT PLATFORM Hermes",
    product_version: "0.1.0-dev",
    upstream_product_name: "Hermes Agent",
    upstream_version: "0.18.2",
    upstream_commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596",
    feature_flags: featureFlags,
    extension_modules: [],
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
      selectedModuleCount: 0,
      resolvedDescriptorCount: 0,
      registeredRouteCount: 0,
      registeredNavigationCount: 0,
    },
    themeId: "default",
    fontId: "theme",
    localeId: "en",
    densityId: "comfortable",
    ...overrides,
  };
}

function writers() {
  return {
    applyTheme: vi.fn(),
    applyFont: vi.fn(),
    applyLocale: vi.fn(),
    persistTheme: vi.fn(async (id: string) => ({ ok: true, theme: id })),
    persistFont: vi.fn(async (id: string) => ({ ok: true, font: id })),
    persistLocale: vi.fn(async (id: string) => ({ ok: true, locale: id })),
  };
}

async function snapshot(overrides: Partial<SafeSettingsSourceContext> = {}): Promise<SafeSettingsSnapshot> {
  return createSafeSettingsAdapter(() => source(overrides), writers(), () => 1_700_000_000_000)
    .readSafeSettings();
}

function readyState(value: SafeSettingsSnapshot, write?: SafePreferenceWriteState): SafeSettingsState {
  return {
    phase: "ready",
    snapshot: value,
    lastSuccessAt: 1_700_000_000_000,
    refreshing: false,
    write: write ?? {
      phase: "idle",
      preferenceId: null,
      draftValueId: null,
      lastSuccessfulWriteAt: null,
      message: null,
    },
  };
}

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});

describe("safe settings projection", () => {
  it("projects immutable product, upstream, feature, activation, profile, and preference facts", async () => {
    const value = await snapshot();

    expect(value.product).toEqual({
      id: "agent-platform-hermes",
      displayName: "AGENT PLATFORM Hermes",
      version: "0.1.0-dev",
    });
    expect(value.upstream).toEqual({
      displayName: "Hermes Agent",
      version: "0.18.2",
      commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596",
    });
    expect(value.features).toEqual([{
      id: "agent_platform.product_ui",
      state: "disabled",
      sourceAuthority: "read-only tracked product configuration",
    }]);
    expect(value.extensionPosture).toEqual({
      compiledDescriptorCount: 9,
      selectedModuleCount: 0,
      resolvedDescriptorCount: 0,
      registeredRouteCount: 0,
      registeredNavigationCount: 0,
    });
    expect(value.selectedProfileContext).toBe("reviewer");
    expect(value.preferences.map((item) => [item.id, item.classification, item.writeAvailable]))
      .toEqual([
        ["theme", "safe_read_write", true],
        ["font", "safe_read_write", true],
        ["language", "safe_read_write", true],
        ["layout-density", "unavailable", false],
        ["navigation", "unavailable", false],
      ]);
    expect(Object.isFrozen(value)).toBe(true);
    expect(Object.isFrozen(value.product)).toBe(true);
    expect(Object.isFrozen(value.features)).toBe(true);
    expect(Object.isFrozen(value.preferences[0]?.allowedValues)).toBe(true);
  });

  it("accepts every capability state and rejects an unknown state", async () => {
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
      registry_credentials: "SECRET_REGISTRY",
      env: { TOKEN: "SECRET_ENV" },
      raw_yaml: "gateway:\n  command: rm -rf private",
      mcp: { secret: "SECRET_MCP", command: "private-command" },
      plugins: { install: "private-plugin" },
      hooks: { command: "private-hook" },
      memory: { provider: "private-memory" },
      gateway: { restart: true },
      filesystem_path: "C:\\private\\settings.yaml",
    };
    const poisoned = { ...configuration(), ...blocked } as ProductConfiguration;
    const rawSource = source({ productConfiguration: poisoned });
    const value = await createSafeSettingsAdapter(() => rawSource, writers()).readSafeSettings();
    const serialized = JSON.stringify(value);

    for (const secret of [
      "SECRET_API_VALUE",
      "SECRET_PROVIDER_TOKEN",
      "SECRET_OAUTH_STATE",
      "https://private.invalid/token",
      "SECRET_REGISTRY",
      "SECRET_ENV",
      "rm -rf private",
      "SECRET_MCP",
      "private-command",
      "private-plugin",
      "private-hook",
      "private-memory",
      "C:\\private\\settings.yaml",
    ]) {
      expect(serialized).not.toContain(secret);
    }
    expect(value).not.toBe(rawSource);
    expect(serialized).not.toContain("SECRET_");
    expect(serialized).not.toContain("private.invalid");
    expect(serialized).not.toContain("private-command");
  });

  it("uses only trusted built-in themes, curated fonts, and supported locales", async () => {
    const value = await snapshot();
    const byId = Object.fromEntries(value.preferences.map((item) => [item.id, item]));

    expect(byId.theme?.allowedValues.map((item) => item.id)).toEqual([
      "default", "default-large", "nous-blue", "midnight", "ember", "mono", "cyberpunk", "rose",
    ]);
    expect(byId.font?.allowedValues.map((item) => item.id)).toEqual([
      "theme", "system-sans", "system-serif", "system-mono", "inter", "ibm-plex-sans",
      "work-sans", "atkinson-hyperlegible", "dm-sans", "spectral", "fraunces",
      "source-serif", "jetbrains-mono", "ibm-plex-mono", "space-mono",
    ]);
    expect(byId.language?.allowedValues.map((item) => item.id)).toEqual([
      "en", "zh", "zh-hant", "ja", "de", "es", "fr", "tr", "uk", "af", "ko", "it",
      "ga", "pt", "ru", "hu",
    ]);
    expect(JSON.stringify(byId.theme)).not.toContain("customCSS");
    expect(JSON.stringify(byId.font)).not.toContain("fonts.googleapis.com");
  });

  it("excludes untrusted current values without silently selecting a default", async () => {
    const value = await snapshot({ themeId: "https://evil.invalid/theme.css" });
    const theme = value.preferences.find((item) => item.id === "theme");
    expect(theme?.currentValueId).toBeNull();
    expect(theme?.currentValueLabel).toBe("Current value excluded");
    expect(theme?.writeAvailable).toBe(true);
  });
});

describe("safe preference writes", () => {
  it("writes one confirmed trusted preference and publishes its actual scope and impact", async () => {
    const calls = writers();
    const adapter = createSafeSettingsAdapter(() => source(), calls, () => 1_700_000_000_500);
    const result = await adapter.writeSafePreference({ preferenceId: "theme", valueId: "nous-blue" });

    expect(calls.persistTheme).toHaveBeenCalledWith("nous-blue", undefined);
    expect(calls.applyTheme).toHaveBeenCalledWith("nous-blue");
    expect(result).toEqual({
      ok: true,
      preferenceId: "theme",
      valueId: "nous-blue",
      completedAt: 1_700_000_000_500,
      message: "Preference saved through its existing safe authority.",
    });
    const updated = await adapter.readSafeSettings();
    expect(updated.preferences.find((item) => item.id === "theme")).toMatchObject({
      currentValueId: "nous-blue",
      persistenceAuthority: "existing Hermes display preference",
      targetScope: "current dashboard backend and this browser",
      impact: "dashboard reload required",
      lastSuccessfulWriteAt: 1_700_000_000_500,
    });
  });

  it("supports the existing language and curated-font setters", async () => {
    const calls = writers();
    const adapter = createSafeSettingsAdapter(() => source(), calls);
    await adapter.writeSafePreference({ preferenceId: "language", valueId: "fr" });
    await adapter.writeSafePreference({ preferenceId: "font", valueId: "inter" });
    expect(calls.persistLocale).toHaveBeenCalledWith("fr", undefined);
    expect(calls.applyLocale).toHaveBeenCalledWith("fr");
    expect(calls.persistFont).toHaveBeenCalledWith("inter", undefined);
    expect(calls.applyFont).toHaveBeenCalledWith("inter");
  });

  it.each([
    { preferenceId: "missing", valueId: "default" },
    { preferenceId: "theme", valueId: "untrusted-theme" },
    { preferenceId: "theme", valueId: "https://evil.invalid/theme.css" },
    { preferenceId: "font", valueId: "C:\\private\\font.woff" },
    { preferenceId: "language", valueId: "rm -rf private" },
    { preferenceId: "theme", valueId: "body{display:none}" },
    { preferenceId: "theme", valueId: '{"raw":true}' },
    { preferenceId: "theme", valueId: "gateway:\n  enabled: true" },
    { preferenceId: "theme", valueId: "api_key" },
    { preferenceId: "layout-density", valueId: "compact" },
    { preferenceId: "navigation", valueId: "collapsed" },
  ])("rejects non-allowlisted request $preferenceId/$valueId", async (request) => {
    const calls = writers();
    const adapter = createSafeSettingsAdapter(() => source(), calls);
    await expect(adapter.writeSafePreference(request)).rejects.toThrow();
    expect(calls.persistTheme).not.toHaveBeenCalled();
    expect(calls.persistFont).not.toHaveBeenCalled();
    expect(calls.applyLocale).not.toHaveBeenCalled();
  });

  it("retains the previous committed value when persistence fails", async () => {
    const calls = writers();
    calls.persistTheme.mockRejectedValueOnce(new Error("raw private failure"));
    const adapter = createSafeSettingsAdapter(() => source(), calls);
    const before = await adapter.readSafeSettings();
    await expect(adapter.writeSafePreference({ preferenceId: "theme", valueId: "nous-blue" }))
      .rejects.toThrow();
    const after = await adapter.readSafeSettings();

    expect(before.preferences.find((item) => item.id === "theme")?.currentValueId).toBe("default");
    expect(after.preferences.find((item) => item.id === "theme")?.currentValueId).toBe("default");
    expect(calls.applyTheme).not.toHaveBeenCalled();
  });

  it("does not optimistically replace the committed value before confirmation", async () => {
    let confirm!: (value: { readonly ok: boolean; readonly theme: string }) => void;
    const calls = writers();
    calls.persistTheme.mockImplementationOnce(() => new Promise((resolve) => { confirm = resolve; }));
    const adapter = createSafeSettingsAdapter(() => source(), calls);
    const pending = adapter.writeSafePreference({ preferenceId: "theme", valueId: "nous-blue" });

    expect((await adapter.readSafeSettings()).preferences.find((item) => item.id === "theme")?.currentValueId)
      .toBe("default");
    expect(calls.applyTheme).not.toHaveBeenCalled();
    confirm({ ok: true, theme: "nous-blue" });
    await pending;
    expect(calls.applyTheme).toHaveBeenCalledWith("nous-blue");
  });

  it("reconciles a confirmed write back to later authoritative context changes", async () => {
    let current = source();
    const calls = writers();
    const adapter = createSafeSettingsAdapter(() => current, calls, () => 1_700_000_000_500);
    await adapter.writeSafePreference({ preferenceId: "theme", valueId: "nous-blue" });
    expect((await adapter.readSafeSettings()).preferences.find((item) => item.id === "theme")?.currentValueId)
      .toBe("nous-blue");

    current = source({ themeId: "nous-blue" });
    await adapter.readSafeSettings();
    current = source({ themeId: "ember" });
    expect((await adapter.readSafeSettings()).preferences.find((item) => item.id === "theme")?.currentValueId)
      .toBe("ember");
  });

  it("rejects snapshots whose classification disagrees with write availability", async () => {
    const raw = JSON.parse(JSON.stringify(await snapshot())) as Record<string, unknown>;
    const preferences = raw.preferences as Array<Record<string, unknown>>;
    preferences[0]!.classification = "blocked_executable";
    expect(() => parseSafeSettingsSnapshot(raw)).toThrow(/classification and write availability/);
  });
});

describe("safe settings polling and write coordination", () => {
  it("loads, refreshes manually, retains stale data, and never overlaps reads", async () => {
    const value = await snapshot();
    let reject = false;
    let finish!: (value: SafeSettingsSnapshot) => void;
    const readSafeSettings = vi.fn(() => reject
      ? Promise.reject(new Error("private transport failure"))
      : new Promise<SafeSettingsSnapshot>((resolve) => { finish = resolve; }));
    const adapter: SafeSettingsAdapter = {
      readSafeSettings,
      writeSafePreference: vi.fn(),
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
      { readSafeSettings, writeSafePreference: vi.fn() },
      (state) => states.push(state),
    );
    const pending = controller.start();
    await vi.advanceTimersByTimeAsync(SAFE_SETTINGS_REQUEST_TIMEOUT_MS);
    expect(await pending).toBe(false);
    expect(states.at(-1)?.phase).toBe("error");

    const lateController = createSafeSettingsController(
      { readSafeSettings: () => Promise.resolve(value), writeSafePreference: vi.fn() },
      (state) => states.push(state),
    );
    const late = lateController.start();
    lateController.stop();
    await late;
    expect(states.at(-1)?.phase).not.toBe("ready");
  });

  it("uses recursive ten-second polling and blocks reads while a write is in flight", async () => {
    vi.useFakeTimers();
    const value = await snapshot();
    let finishWrite!: () => void;
    const adapter: SafeSettingsAdapter = {
      readSafeSettings: vi.fn(async () => value),
      writeSafePreference: vi.fn(() => new Promise<SafePreferenceWriteResult>((resolve) => {
        finishWrite = () => resolve({
          ok: true,
          preferenceId: "theme",
          valueId: "nous-blue",
          completedAt: 1_700_000_000_500,
          message: "Preference saved through its existing safe authority.",
        });
      })),
    };
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(adapter, (state) => states.push(state));
    await controller.start();
    const pendingWrite = controller.writePreference({ preferenceId: "theme", valueId: "nous-blue" });
    expect(await controller.refresh()).toBe(false);
    expect(states.at(-1)?.write.phase).toBe("saving");
    expect(states.at(-1)?.snapshot).toBe(value);
    finishWrite();
    await pendingWrite;
    expect(states.some((state) => state.write.phase === "saved")).toBe(true);
    expect(adapter.readSafeSettings).toHaveBeenCalledTimes(2);

    await vi.advanceTimersByTimeAsync(SAFE_SETTINGS_POLL_MS);
    expect(adapter.readSafeSettings).toHaveBeenCalledTimes(3);
    controller.stop();
  });

  it("publishes bounded write errors and permits explicit retry", async () => {
    const value = await snapshot();
    const writeSafePreference = vi.fn()
      .mockRejectedValueOnce(new Error("SECRET raw failure"))
      .mockResolvedValueOnce({
        ok: true,
        preferenceId: "theme",
        valueId: "nous-blue",
        completedAt: 1_700_000_000_500,
        message: "Preference saved through its existing safe authority.",
      });
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(
      { readSafeSettings: vi.fn(async () => value), writeSafePreference },
      (state) => states.push(state),
    );
    await controller.start();
    await controller.writePreference({ preferenceId: "theme", valueId: "nous-blue" });
    expect(states.at(-1)?.write).toMatchObject({
      phase: "error",
      message: "The safe preference could not be saved. The previous value is still shown.",
    });
    expect(JSON.stringify(states.at(-1))).not.toContain("SECRET");
    await controller.retryWrite();
    expect(writeSafePreference).toHaveBeenCalledTimes(2);
    controller.stop();
  });

  it("leaves saving state when an injected write ignores cancellation", async () => {
    vi.useFakeTimers();
    const value = await snapshot();
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(
      {
        readSafeSettings: vi.fn(async () => value),
        writeSafePreference: vi.fn(() => new Promise<SafePreferenceWriteResult>(() => {})),
      },
      (state) => states.push(state),
    );
    await controller.start();
    const pending = controller.writePreference({ preferenceId: "theme", valueId: "nous-blue" });
    await vi.advanceTimersByTimeAsync(SAFE_SETTINGS_REQUEST_TIMEOUT_MS);
    expect(await pending).toBe(false);
    expect(states.at(-1)?.write.phase).toBe("error");
    controller.stop();
  });

  it("maps an absent validated product source to unavailable", async () => {
    const states: SafeSettingsState[] = [];
    const controller = createSafeSettingsController(
      {
        readSafeSettings: () => Promise.reject(new SafeSettingsUnavailableError("unavailable")),
        writeSafePreference: vi.fn(),
      },
      (state) => states.push(state),
    );
    expect(await controller.start()).toBe(false);
    expect(states.at(-1)?.phase).toBe("unavailable");
    controller.stop();
  });
});

describe("safe settings page and descriptor", () => {
  it("renders identity, read-only activation, persistence, impact, and excluded boundaries", async () => {
    const html = renderToStaticMarkup(
      <SafeSettingsView
        state={readyState(await snapshot())}
        refresh={() => {}}
        writePreference={() => {}}
        retryWrite={() => {}}
      />,
    );
    for (const text of [
      "Safe Settings",
      "AGENT PLATFORM Hermes",
      "Hermes Agent",
      "agent_platform.product_ui",
      "Feature and module activation is read-only in P13.7",
      "P13.R owns any tracked activation decision",
      "current dashboard backend and this browser",
      "existing Hermes display preference",
      "dashboard reload required",
      "immediate",
      "Layout density",
      "Navigation preference",
      "Excluded settings boundary",
      "No secrets are exposed",
      "No raw configuration fallback exists",
    ]) {
      expect(html).toContain(text);
    }
    expect(html).toContain("sm:grid-cols-3");
    expect(html).toContain("lg:grid-cols-2");
    expect(html).toContain('role="combobox"');
    expect(html).not.toContain('type="password"');
    expect(html).not.toContain('type="url"');
    expect(html).not.toContain('type="checkbox"');
    expect(html).not.toContain("<textarea");
    expect(html).not.toContain("<a ");
  });

  it("renders stale, unavailable, not-configured, and bounded save-error states", async () => {
    const value = await snapshot({ themeId: "custom-untrusted" });
    const errorWrite: SafePreferenceWriteState = {
      phase: "error",
      preferenceId: "theme",
      draftValueId: "nous-blue",
      lastSuccessfulWriteAt: null,
      message: "The safe preference could not be saved. The previous value is still shown.",
    };
    const html = renderToStaticMarkup(
      <SafeSettingsView
        state={{ ...readyState(value, errorWrite), phase: "stale" }}
        refresh={() => {}}
        writePreference={() => {}}
        retryWrite={() => {}}
      />,
    );
    expect(html).toContain("Stale");
    expect(html).toContain("Current value excluded");
    expect(html).toContain("Unavailable");
    expect(html).toContain("Retry safe write");
    expect(html).not.toContain("custom-untrusted");

    const unavailable: SafeSettingsDataState = {
      phase: "unavailable",
      snapshot: null,
      lastSuccessAt: null,
      refreshing: false,
    };
    const unavailableHtml = renderToStaticMarkup(
      <SafeSettingsView
        state={{ ...unavailable, write: readyState(value).write }}
        refresh={() => {}}
        writePreference={() => {}}
        retryWrite={() => {}}
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
