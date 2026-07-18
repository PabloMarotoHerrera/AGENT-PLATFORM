import { useEffect, useRef, useState } from "react";

import { useProfileScope } from "@/contexts/useProfileScope";
import { fetchJSON } from "@/lib/api";

import {
  parseRuntimeOverviewSnapshot,
  type RuntimeOverviewSnapshot,
} from "./contract";

export const RUNTIME_OVERVIEW_POLL_MS = 10_000;
export const RUNTIME_OVERVIEW_REQUEST_TIMEOUT_MS = 15_000;

export type RuntimeOverviewPhase =
  | "loading"
  | "ready"
  | "stale"
  | "error"
  | "unavailable";

export interface RuntimeOverviewState {
  readonly phase: RuntimeOverviewPhase;
  readonly snapshot: RuntimeOverviewSnapshot | null;
  readonly lastSuccessAt: number | null;
  readonly refreshing: boolean;
}

export interface RuntimeOverviewPoller {
  start: () => Promise<boolean>;
  refresh: () => Promise<boolean>;
  stop: () => void;
}

interface RuntimeOverviewPollerOptions {
  readonly now?: () => number;
  readonly setTimer?: (callback: () => void, delay: number) => unknown;
  readonly clearTimer?: (timer: unknown) => void;
}

export const INITIAL_RUNTIME_OVERVIEW_STATE: RuntimeOverviewState = Object.freeze({
  phase: "loading",
  snapshot: null,
  lastSuccessAt: null,
  refreshing: false,
});

export function createRuntimeOverviewPoller(
  loadStatus: () => Promise<unknown>,
  publish: (state: RuntimeOverviewState) => void,
  options: RuntimeOverviewPollerOptions = {},
): RuntimeOverviewPoller {
  const now = options.now ?? Date.now;
  const setTimer = options.setTimer ?? ((callback, delay) => setTimeout(callback, delay));
  const clearTimer = options.clearTimer ?? ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));

  let stopped = false;
  let inFlight = false;
  let timer: unknown = null;
  let snapshot: RuntimeOverviewSnapshot | null = null;
  let lastSuccessAt: number | null = null;
  let phase: RuntimeOverviewPhase = "loading";
  let activeController: AbortController | null = null;

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

  const emit = (nextPhase: RuntimeOverviewPhase, refreshing = false) => {
    phase = nextPhase;
    publish(Object.freeze({ phase, snapshot, lastSuccessAt, refreshing }));
  };

  const schedule = () => {
    if (stopped) return;
    timer = setTimer(() => {
      timer = null;
      void run();
    }, RUNTIME_OVERVIEW_POLL_MS);
  };

  const run = async (): Promise<boolean> => {
    if (stopped || inFlight) return false;
    inFlight = true;
    const controller = new AbortController();
    activeController = controller;
    const requestTimeout = setTimeout(() => controller.abort(), RUNTIME_OVERVIEW_REQUEST_TIMEOUT_MS);
    if (snapshot) emit(phase, true);

    try {
      const parsed = parseRuntimeOverviewSnapshot(await settleOnAbort(loadStatus(), controller.signal));
      if (stopped || controller.signal.aborted) return false;
      if (parsed === null) {
        emit(snapshot ? "stale" : "unavailable");
        return false;
      }
      snapshot = parsed;
      lastSuccessAt = now();
      emit("ready");
      return true;
    } catch {
      if (!stopped) emit(snapshot ? "stale" : "error");
      return false;
    } finally {
      clearTimeout(requestTimeout);
      if (activeController === controller) activeController = null;
      inFlight = false;
      schedule();
    }
  };

  return Object.freeze({
    start: run,
    refresh: () => {
      if (stopped || inFlight) return Promise.resolve(false);
      if (timer !== null) {
        clearTimer(timer);
        timer = null;
      }
      return run();
    },
    stop: () => {
      stopped = true;
      activeController?.abort();
      activeController = null;
      if (timer !== null) clearTimer(timer);
      timer = null;
    },
  });
}

export function useRuntimeOverview(): RuntimeOverviewState & { readonly refresh: () => void } {
  const { profile } = useProfileScope();
  const [stored, setStored] = useState<{
    readonly profile: string;
    readonly state: RuntimeOverviewState;
  }>(() => ({ profile, state: INITIAL_RUNTIME_OVERVIEW_STATE }));
  const pollerRef = useRef<{ profile: string; poller: RuntimeOverviewPoller } | null>(null);

  useEffect(() => {
    const poller = createRuntimeOverviewPoller(
      () => fetchJSON<unknown>("/api/status"),
      (state) => setStored({ profile, state }),
    );
    pollerRef.current = { profile, poller };
    void poller.start();

    return () => {
      poller.stop();
      if (pollerRef.current?.poller === poller) pollerRef.current = null;
    };
  }, [profile]);

  const state = stored.profile === profile ? stored.state : INITIAL_RUNTIME_OVERVIEW_STATE;
  return {
    ...state,
    refresh: () => {
      const active = pollerRef.current;
      if (active?.profile === profile) void active.poller.refresh();
    },
  };
}
