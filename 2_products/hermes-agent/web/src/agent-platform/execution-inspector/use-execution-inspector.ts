import { useEffect, useRef, useState } from "react";

import { useProfileScope } from "@/contexts/useProfileScope";

import {
  isExecutionInspectorViewEmpty,
  type ExecutionInspectorDataState,
  type ExecutionInspectorPhase,
  type ExecutionInspectorRequest,
  type ExecutionInspectorView,
} from "./contract";
import {
  loadExecutionInspectorRequest,
  type ExecutionInspectorLoader,
} from "./execution-client";

export const EXECUTION_INSPECTOR_POLL_MS = 10_000;
export const EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS = 15_000;

export const INITIAL_EXECUTION_INSPECTOR_STATE: ExecutionInspectorDataState = Object.freeze({
  phase: "loading",
  snapshot: null,
  lastSuccessAt: null,
  refreshing: false,
});

export interface ExecutionInspectorPoller {
  readonly start: () => Promise<boolean>;
  readonly refresh: () => Promise<boolean>;
  readonly stop: () => void;
}

interface ExecutionInspectorPollerOptions {
  readonly now?: () => number;
  readonly setTimer?: (callback: () => void, delay: number) => unknown;
  readonly clearTimer?: (timer: unknown) => void;
}

export function executionInspectorRequestKey(request: ExecutionInspectorRequest, profile: string): string {
  return request.kind === "executions"
    ? `${profile}\0executions\0${request.boardSlug}\0${request.taskId}`
    : `${profile}\0detail\0${request.boardSlug}\0${request.taskId}\0${request.executionId}`;
}

export function createExecutionInspectorPoller(
  load: (signal: AbortSignal) => Promise<ExecutionInspectorView | null>,
  publish: (state: ExecutionInspectorDataState) => void,
  options: ExecutionInspectorPollerOptions = {},
): ExecutionInspectorPoller {
  const now = options.now ?? Date.now;
  const setTimer = options.setTimer ?? ((callback, delay) => setTimeout(callback, delay));
  const clearTimer = options.clearTimer ?? ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  let stopped = false;
  let inFlight = false;
  let timer: unknown = null;
  let snapshot: ExecutionInspectorView | null = null;
  let lastSuccessAt: number | null = null;
  let phase: ExecutionInspectorPhase = "loading";
  let activeController: AbortController | null = null;

  const emit = (nextPhase: ExecutionInspectorPhase, refreshing = false) => {
    phase = nextPhase;
    publish(Object.freeze({ phase, snapshot, lastSuccessAt, refreshing }));
  };

  const schedule = () => {
    if (stopped) return;
    timer = setTimer(() => {
      timer = null;
      void run();
    }, EXECUTION_INSPECTOR_POLL_MS);
  };

  const run = async (): Promise<boolean> => {
    if (stopped || inFlight) return false;
    inFlight = true;
    const controller = new AbortController();
    activeController = controller;
    const requestTimeout = setTimeout(() => controller.abort(), EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS);
    if (snapshot) emit(phase, true);
    try {
      const next = await load(controller.signal);
      if (stopped) return false;
      if (next === null) {
        emit(snapshot ? "stale" : "unavailable");
        return false;
      }
      snapshot = next;
      lastSuccessAt = now();
      emit(isExecutionInspectorViewEmpty(next) ? "empty" : "ready");
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

export function useExecutionInspector(
  request: ExecutionInspectorRequest,
  loader: ExecutionInspectorLoader = loadExecutionInspectorRequest,
): ExecutionInspectorDataState & { readonly profile: string; readonly refresh: () => void } {
  const { profile, currentProfile } = useProfileScope();
  const selectedProfile = profile || currentProfile;
  const identity = executionInspectorRequestKey(request, selectedProfile);
  const [stored, setStored] = useState<{
    readonly identity: string;
    readonly state: ExecutionInspectorDataState;
  }>(() => ({ identity, state: INITIAL_EXECUTION_INSPECTOR_STATE }));
  const pollerRef = useRef<{ identity: string; poller: ExecutionInspectorPoller } | null>(null);
  const executionId = request.kind === "detail" ? request.executionId : "";

  useEffect(() => {
    const exactRequest: ExecutionInspectorRequest = request.kind === "executions"
      ? { kind: "executions", boardSlug: request.boardSlug, taskId: request.taskId }
      : {
        kind: "detail",
        boardSlug: request.boardSlug,
        taskId: request.taskId,
        executionId,
    };
    const poller = createExecutionInspectorPoller(
      (signal) => loader(exactRequest, selectedProfile, signal),
      (state) => setStored({ identity, state }),
    );
    pollerRef.current = { identity, poller };
    void poller.start();
    return () => {
      poller.stop();
      if (pollerRef.current?.poller === poller) pollerRef.current = null;
    };
  }, [executionId, identity, loader, request.boardSlug, request.kind, request.taskId, selectedProfile]);

  const state = stored.identity === identity ? stored.state : INITIAL_EXECUTION_INSPECTOR_STATE;
  return {
    ...state,
    profile: selectedProfile,
    refresh: () => {
      const active = pollerRef.current;
      if (active?.identity === identity) void active.poller.refresh();
    },
  };
}
