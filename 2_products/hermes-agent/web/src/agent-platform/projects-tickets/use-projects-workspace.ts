import { useEffect, useRef, useState } from "react";

import { useProfileScope } from "@/contexts/useProfileScope";

import {
  isWorkspaceViewEmpty,
  type ProjectsWorkspaceDataState,
  type ProjectsWorkspacePhase,
  type ProjectsWorkspaceRequest,
  type ProjectsWorkspaceView,
} from "./contract";
import { loadProjectsWorkspaceRequest } from "./kanban-client";

export const PROJECTS_WORKSPACE_POLL_MS = 10_000;

export const INITIAL_PROJECTS_WORKSPACE_STATE: ProjectsWorkspaceDataState = Object.freeze({
  phase: "loading",
  snapshot: null,
  lastSuccessAt: null,
  refreshing: false,
});

export interface ProjectsWorkspacePoller {
  readonly start: () => Promise<boolean>;
  readonly refresh: () => Promise<boolean>;
  readonly stop: () => void;
}

interface ProjectsWorkspacePollerOptions {
  readonly now?: () => number;
  readonly setTimer?: (callback: () => void, delay: number) => unknown;
  readonly clearTimer?: (timer: unknown) => void;
}

export function projectsWorkspaceRequestKey(request: ProjectsWorkspaceRequest, profile: string): string {
  if (request.kind === "projects") return `${profile}\0projects`;
  if (request.kind === "project") return `${profile}\0project\0${request.boardSlug}`;
  return `${profile}\0ticket\0${request.boardSlug}\0${request.taskId}`;
}

export function createProjectsWorkspacePoller(
  load: () => Promise<ProjectsWorkspaceView | null>,
  publish: (state: ProjectsWorkspaceDataState) => void,
  options: ProjectsWorkspacePollerOptions = {},
): ProjectsWorkspacePoller {
  const now = options.now ?? Date.now;
  const setTimer = options.setTimer ?? ((callback, delay) => setTimeout(callback, delay));
  const clearTimer = options.clearTimer ?? ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  let stopped = false;
  let inFlight = false;
  let timer: unknown = null;
  let snapshot: ProjectsWorkspaceView | null = null;
  let lastSuccessAt: number | null = null;
  let phase: ProjectsWorkspacePhase = "loading";

  const emit = (nextPhase: ProjectsWorkspacePhase, refreshing = false) => {
    phase = nextPhase;
    publish(Object.freeze({ phase, snapshot, lastSuccessAt, refreshing }));
  };

  const schedule = () => {
    if (stopped) return;
    timer = setTimer(() => {
      timer = null;
      void run();
    }, PROJECTS_WORKSPACE_POLL_MS);
  };

  const run = async (): Promise<boolean> => {
    if (stopped || inFlight) return false;
    inFlight = true;
    if (snapshot) emit(phase, true);
    try {
      const next = await load();
      if (stopped) return false;
      if (next === null) {
        emit(snapshot ? "stale" : "unavailable");
        return false;
      }
      snapshot = next;
      lastSuccessAt = now();
      emit(isWorkspaceViewEmpty(next) ? "empty" : "ready");
      return true;
    } catch {
      if (!stopped) emit(snapshot ? "stale" : "error");
      return false;
    } finally {
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
      if (timer !== null) clearTimer(timer);
      timer = null;
    },
  });
}

export function useProjectsWorkspace(
  request: ProjectsWorkspaceRequest,
): ProjectsWorkspaceDataState & { readonly profile: string; readonly refresh: () => void } {
  const { profile, currentProfile } = useProfileScope();
  const selectedProfile = profile || currentProfile;
  const identity = projectsWorkspaceRequestKey(request, selectedProfile);
  const [stored, setStored] = useState<{
    readonly identity: string;
    readonly state: ProjectsWorkspaceDataState;
  }>(() => ({ identity, state: INITIAL_PROJECTS_WORKSPACE_STATE }));
  const pollerRef = useRef<{ identity: string; poller: ProjectsWorkspacePoller } | null>(null);
  const boardSlug = request.kind === "projects" ? "" : request.boardSlug;
  const taskId = request.kind === "ticket" ? request.taskId : "";

  useEffect(() => {
    const exactRequest: ProjectsWorkspaceRequest = request.kind === "projects"
      ? { kind: "projects" }
      : request.kind === "project"
        ? { kind: "project", boardSlug }
        : { kind: "ticket", boardSlug, taskId };
    const poller = createProjectsWorkspacePoller(
      () => loadProjectsWorkspaceRequest(exactRequest, selectedProfile),
      (state) => setStored({ identity, state }),
    );
    pollerRef.current = { identity, poller };
    void poller.start();
    return () => {
      poller.stop();
      if (pollerRef.current?.poller === poller) pollerRef.current = null;
    };
  }, [boardSlug, identity, request.kind, selectedProfile, taskId]);

  const state = stored.identity === identity ? stored.state : INITIAL_PROJECTS_WORKSPACE_STATE;
  return {
    ...state,
    profile: selectedProfile,
    refresh: () => {
      const active = pollerRef.current;
      if (active?.identity === identity) void active.poller.refresh();
    },
  };
}
