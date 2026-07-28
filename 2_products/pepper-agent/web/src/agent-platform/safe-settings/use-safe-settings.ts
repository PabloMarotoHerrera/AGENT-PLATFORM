import { useEffect, useRef, useState } from "react";

import { useProfileScope } from "@/contexts/useProfileScope";
import { useI18n } from "@/i18n/context";
import { useTheme } from "@/themes/context";

import { getProductExtensionPosture } from "../extensions";
import { useProductConfiguration } from "../product-config-context";
import {
  INITIAL_SAFE_SETTINGS_DATA_STATE,
  type SafeSettingsDataState,
} from "./contract";
import {
  createSafeSettingsAdapter,
  SafeSettingsUnavailableError,
  type SafeSettingsAdapter,
  type SafeSettingsSourceContext,
} from "./safe-settings-adapter";

export const SAFE_SETTINGS_POLL_MS = 10_000;
export const SAFE_SETTINGS_REQUEST_TIMEOUT_MS = 15_000;

export type SafeSettingsState = SafeSettingsDataState;

export interface SafeSettingsController {
  readonly start: () => Promise<boolean>;
  readonly refresh: () => Promise<boolean>;
  readonly stop: () => void;
}

interface SafeSettingsControllerOptions {
  readonly now?: () => number;
  readonly setTimer?: (callback: () => void, delay: number) => unknown;
  readonly clearTimer?: (timer: unknown) => void;
  readonly pollMs?: number;
  readonly requestTimeoutMs?: number;
}

const INITIAL_SAFE_SETTINGS_STATE: SafeSettingsState = Object.freeze({
  ...INITIAL_SAFE_SETTINGS_DATA_STATE,
});

export function createSafeSettingsController(
  adapter: SafeSettingsAdapter,
  publish: (state: SafeSettingsState) => void,
  options: SafeSettingsControllerOptions = {},
): SafeSettingsController {
  const now = options.now ?? Date.now;
  const setTimer = options.setTimer ?? ((callback, delay) => setTimeout(callback, delay));
  const clearTimer = options.clearTimer ?? ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  const pollMs = options.pollMs ?? SAFE_SETTINGS_POLL_MS;
  const requestTimeoutMs = options.requestTimeoutMs ?? SAFE_SETTINGS_REQUEST_TIMEOUT_MS;
  let stopped = false;
  let reading = false;
  let pollTimer: unknown = null;
  let requestController: AbortController | null = null;
  let snapshot = INITIAL_SAFE_SETTINGS_DATA_STATE.snapshot;
  let phase = INITIAL_SAFE_SETTINGS_DATA_STATE.phase;
  let lastSuccessAt = INITIAL_SAFE_SETTINGS_DATA_STATE.lastSuccessAt;

  const settleOnAbort = <T,>(promise: Promise<T>, signal: AbortSignal): Promise<T> =>
    new Promise<T>((resolve, reject) => {
      const rejectAborted = () => reject(new DOMException("Aborted", "AbortError"));
      if (signal.aborted) {
        rejectAborted();
        return;
      }
      signal.addEventListener("abort", rejectAborted, { once: true });
      promise.then(resolve, reject).finally(() => {
        signal.removeEventListener("abort", rejectAborted);
      });
    });

  const emit = (refreshing = false) => {
    publish(Object.freeze({ phase, snapshot, lastSuccessAt, refreshing }));
  };

  const clearPoll = () => {
    if (pollTimer !== null) clearTimer(pollTimer);
    pollTimer = null;
  };

  const schedule = () => {
    if (stopped) return;
    clearPoll();
    pollTimer = setTimer(() => {
      pollTimer = null;
      void run();
    }, pollMs);
  };

  const run = async (): Promise<boolean> => {
    if (stopped || reading) return false;
    reading = true;
    if (snapshot) emit(true);
    requestController = new AbortController();
    const activeController = requestController;
    const timeout = setTimer(() => activeController.abort(), requestTimeoutMs);
    try {
      const next = await settleOnAbort(
        adapter.readSafeSettings(activeController.signal),
        activeController.signal,
      );
      if (stopped || activeController.signal.aborted) return false;
      snapshot = next;
      lastSuccessAt = now();
      phase = "ready";
      emit();
      return true;
    } catch (error) {
      if (stopped) return false;
      if (error instanceof SafeSettingsUnavailableError) {
        phase = snapshot ? "stale" : "unavailable";
      } else {
        phase = snapshot ? "stale" : "error";
      }
      emit();
      return false;
    } finally {
      clearTimer(timeout);
      if (requestController === activeController) requestController = null;
      reading = false;
      schedule();
    }
  };

  return Object.freeze({
    start: run,
    refresh: () => {
      if (stopped || reading) return Promise.resolve(false);
      clearPoll();
      return run();
    },
    stop: () => {
      stopped = true;
      clearPoll();
      requestController?.abort();
      requestController = null;
    },
  });
}

export function useSafeSettings(): SafeSettingsState & {
  readonly refresh: () => void;
} {
  const productConfiguration = useProductConfiguration();
  const { profile, currentProfile } = useProfileScope();
  const theme = useTheme();
  const i18n = useI18n();
  const identity = profile || currentProfile;
  const sourceRef = useRef<SafeSettingsSourceContext>({
    productConfiguration,
    selectedProfileContext: identity,
    extensionPosture: getProductExtensionPosture(productConfiguration),
    themeId: theme.themeName,
    fontId: theme.fontId,
    localeId: i18n.locale,
    densityId: theme.theme.layout.density,
  });
  useEffect(() => {
    sourceRef.current = {
      productConfiguration,
      selectedProfileContext: identity,
      extensionPosture: getProductExtensionPosture(productConfiguration),
      themeId: theme.themeName,
      fontId: theme.fontId,
      localeId: i18n.locale,
      densityId: theme.theme.layout.density,
    };
  }, [
    productConfiguration,
    identity,
    theme.themeName,
    theme.fontId,
    theme.theme.layout.density,
    i18n.locale,
  ]);
  const [stored, setStored] = useState<{ readonly identity: string; readonly state: SafeSettingsState }>(
    () => ({ identity, state: INITIAL_SAFE_SETTINGS_STATE }),
  );
  const controllerRef = useRef<{ readonly identity: string; readonly controller: SafeSettingsController } | null>(null);

  useEffect(() => {
    const adapter = createSafeSettingsAdapter(
      () => sourceRef.current,
    );
    const controller = createSafeSettingsController(
      adapter,
      (state) => setStored({ identity, state }),
    );
    controllerRef.current = { identity, controller };
    void controller.start();
    return () => {
      controller.stop();
      if (controllerRef.current?.controller === controller) controllerRef.current = null;
    };
  }, [identity]);

  const state = stored.identity === identity ? stored.state : INITIAL_SAFE_SETTINGS_STATE;
  return {
    ...state,
    refresh: () => {
      const active = controllerRef.current;
      if (active?.identity === identity) void active.controller.refresh();
    },
  };
}
