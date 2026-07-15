import { useEffect, useRef, useState } from "react";

import { useProfileScope } from "@/contexts/useProfileScope";

import {
  isApprovalInboxViewEmpty,
  type ApprovalInboxDataState,
  type ApprovalInboxPhase,
  type ApprovalInboxRequest,
  type ApprovalInboxView,
} from "./contract";
import { loadApprovalInboxRequest, type ApprovalInboxLoader } from "./approval-client";

export const APPROVAL_INBOX_POLL_MS = 10_000;

export const INITIAL_APPROVAL_INBOX_STATE: ApprovalInboxDataState = Object.freeze({
  phase: "loading",
  snapshot: null,
  lastSuccessAt: null,
  refreshing: false,
});

export interface ApprovalInboxPoller {
  readonly start: () => Promise<boolean>;
  readonly refresh: () => Promise<boolean>;
  readonly stop: () => void;
}

interface ApprovalInboxPollerOptions {
  readonly now?: () => number;
  readonly setTimer?: (callback: () => void, delay: number) => unknown;
  readonly clearTimer?: (timer: unknown) => void;
}

export function approvalInboxRequestKey(request: ApprovalInboxRequest, profile: string): string {
  return request.kind === "inbox"
    ? `${profile}\0inbox`
    : `${profile}\0detail\0${request.approvalId}`;
}

export function createApprovalInboxPoller(
  load: () => Promise<ApprovalInboxView | null>,
  publish: (state: ApprovalInboxDataState) => void,
  options: ApprovalInboxPollerOptions = {},
): ApprovalInboxPoller {
  const now = options.now ?? Date.now;
  const setTimer = options.setTimer ?? ((callback, delay) => setTimeout(callback, delay));
  const clearTimer = options.clearTimer ?? ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  let stopped = false;
  let inFlight = false;
  let timer: unknown = null;
  let snapshot: ApprovalInboxView | null = null;
  let lastSuccessAt: number | null = null;
  let phase: ApprovalInboxPhase = "loading";

  const emit = (nextPhase: ApprovalInboxPhase, refreshing = false) => {
    phase = nextPhase;
    publish(Object.freeze({ phase, snapshot, lastSuccessAt, refreshing }));
  };

  const schedule = () => {
    if (stopped) return;
    timer = setTimer(() => {
      timer = null;
      void run();
    }, APPROVAL_INBOX_POLL_MS);
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
      emit(isApprovalInboxViewEmpty(next) ? "empty" : "ready");
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

export function useApprovalInbox(
  request: ApprovalInboxRequest,
  loader: ApprovalInboxLoader = loadApprovalInboxRequest,
): ApprovalInboxDataState & { readonly profile: string; readonly refresh: () => void } {
  const { profile, currentProfile } = useProfileScope();
  const selectedProfile = profile || currentProfile;
  const identity = approvalInboxRequestKey(request, selectedProfile);
  const [stored, setStored] = useState<{
    readonly identity: string;
    readonly state: ApprovalInboxDataState;
  }>(() => ({ identity, state: INITIAL_APPROVAL_INBOX_STATE }));
  const pollerRef = useRef<{ identity: string; poller: ApprovalInboxPoller } | null>(null);
  const approvalId = request.kind === "detail" ? request.approvalId : "";

  useEffect(() => {
    const exactRequest: ApprovalInboxRequest = request.kind === "inbox"
      ? { kind: "inbox" }
      : { kind: "detail", approvalId };
    const poller = createApprovalInboxPoller(
      () => loader(exactRequest, selectedProfile),
      (state) => setStored({ identity, state }),
    );
    pollerRef.current = { identity, poller };
    void poller.start();
    return () => {
      poller.stop();
      if (pollerRef.current?.poller === poller) pollerRef.current = null;
    };
  }, [approvalId, identity, loader, request.kind, selectedProfile]);

  const state = stored.identity === identity ? stored.state : INITIAL_APPROVAL_INBOX_STATE;
  return {
    ...state,
    profile: selectedProfile,
    refresh: () => {
      const active = pollerRef.current;
      if (active?.identity === identity) void active.poller.refresh();
    },
  };
}
