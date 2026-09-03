/**
 * ChatSidebar — structured-events panel that sits next to the xterm.js
 * terminal in the dashboard Chat tab.
 *
 * Two WebSockets, one per concern:
 *
 *   1. **JSON-RPC liveness** (`GatewayClient` → /api/ws) — a WebSocket used
 *      only for connection state (the "live" badge). It does not create a
 *      sidecar `session.create`, so Pepper Chat has no duplicate sidebar agent
 *      or provider runtime. Pepper chat intentionally does not expose the
 *      generic model picker here; the PTY child is bound to the governed Lead
 *      Agent runtime.
 *
 *   2. **Event subscriber** (/api/events?channel=…) — passive, receives
 *      every dispatcher emit from the PTY-side `tui_gateway.entry` that
 *      the dashboard fanned out.  The sidebar uses it for `session.info`
 *      (live chat title) and `dashboard.new_session_requested`.  The
 *      `channel` id ties this listener to the same chat tab's PTY child —
 *      see `ChatPage.tsx` for where the id is generated.
 *
 * Best-effort throughout: WS failures show in the badge / banner, the
 * terminal pane keeps working unimpaired.
 */

import { Button } from "@nous-research/ui/ui/components/button";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card } from "@nous-research/ui/ui/components/card";

import { GatewayClient, type ConnectionState } from "@/lib/gatewayClient";
import { buildWsUrl } from "@/lib/api";
import { titleFromSessionInfoPayload } from "@/lib/chat-title";
import { useRuntimeOverview } from "@/agent-platform/runtime-overview/use-runtime-overview";
import type { RuntimeWorkflowControl } from "@/agent-platform/runtime-overview/contract";

import { cn } from "@/lib/utils";
import { AlertCircle, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

interface RpcEnvelope {
  method?: string;
  params?: { type?: string; payload?: unknown };
}

const STATE_LABEL: Record<ConnectionState, string> = {
  idle: "idle",
  connecting: "connecting",
  open: "live",
  closed: "closed",
  error: "error",
};

const STATE_TONE: Record<
  ConnectionState,
  "secondary" | "warning" | "success" | "destructive"
> = {
  idle: "secondary",
  connecting: "warning",
  open: "success",
  closed: "secondary",
  error: "destructive",
};

interface ChatSidebarProps {
  channel: string;
  /** Chat profile from the dashboard switcher / URL scope. */
  profile?: string;
  className?: string;
  onDashboardNewSessionRequest?: () => void;
  onSessionTitleChange?: (title: string | null) => void;
}

function requiredLabel(value: boolean) {
  return value ? "Required" : "Not required";
}

function workflowCurrentWork(control: RuntimeWorkflowControl) {
  return control.currentTicketId
    ? `${control.currentTicketId}: ${control.currentTicketTitle ?? "Untitled governed ticket"}`
    : "No current governed ticket is active.";
}

function workflowAttention(control: RuntimeWorkflowControl) {
  return [
    control.pendingTicketApprovalCount > 0 ? "ticket approval pending" : null,
    control.reviewDecisionRequired ? "review decision required" : null,
    control.humanAcceptanceRequired && !control.humanAcceptanceRecorded ? "human acceptance required" : null,
    control.gitHandoffRequired ? "Git handoff required" : null,
    control.readyRequiresHumanSmoke ? "human smoke check required" : null,
    control.remainingBlockerCount > 0 ? "blockers remain" : null,
    control.failureCategory ? "recovery evidence present" : null,
  ].filter(Boolean).join("; ") || "No human-attention condition is currently raised.";
}

function SidebarCell({ label, value }: { readonly label: string; readonly value: string | number }) {
  return (
    <div className="min-w-0 rounded-md border border-border-subtle/70 px-2 py-1.5">
      <div className="text-[0.65rem] uppercase tracking-[0.12em] text-text-tertiary">{label}</div>
      <div className="mt-1 break-words font-mono text-xs text-text-primary">{value}</div>
    </div>
  );
}

export function ChatSidebarGovernedContext({
  workflowControl,
}: {
  readonly workflowControl: RuntimeWorkflowControl | null;
}) {
  return (
    <Card className="px-3 py-3 text-xs">
      <div className="text-display text-xs tracking-wider text-text-tertiary">
        Governed workflow context
      </div>
      <p className="mt-2 leading-relaxed text-text-secondary">
        Presentation-only view of the backend-projected runtime workflow-control read model.
      </p>

      {workflowControl ? (
        <div className="mt-3 space-y-3">
          <div>
            <div className="text-[0.65rem] uppercase tracking-[0.12em] text-text-tertiary">Current work</div>
            <div className="mt-1 break-words text-sm font-medium text-text-primary">
              {workflowCurrentWork(workflowControl)}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-2">
            <SidebarCell label="Workflow status" value={workflowControl.workflowStatus} />
            <SidebarCell label="Workflow state" value={workflowControl.workflowState} />
            <SidebarCell label="Recovery state" value={workflowControl.recoveryState} />
            <SidebarCell label="Next governed action" value={workflowControl.nextActionId} />
            <SidebarCell label="Required human action" value={workflowControl.nextActionRequiredHumanAction} />
            <SidebarCell label="Execution posture" value={workflowControl.executionState} />
            <SidebarCell label="Manual chat control" value={requiredLabel(workflowControl.manualChatControlRequired)} />
          </div>

          <p className="leading-relaxed text-text-secondary">{workflowControl.nextActionLabel}</p>
          <p className="leading-relaxed text-text-secondary">{workflowAttention(workflowControl)}</p>
        </div>
      ) : (
        <p className="mt-3 leading-relaxed text-text-secondary">
          Workflow-control read model unavailable; no lifecycle authority is derived locally.
        </p>
      )}
    </Card>
  );
}

export function ChatSidebar({
  channel,
  profile,
  className,
  onDashboardNewSessionRequest,
  onSessionTitleChange,
}: ChatSidebarProps) {
  // `version` bumps on reconnect; gw is derived so we never call setState
  // for it inside an effect (React 19's set-state-in-effect rule). The
  // counter is the dependency on purpose — it's not read in the memo body,
  // it's the signal that says "rebuild the client".
  const [version, setVersion] = useState(0);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const gw = useMemo(() => new GatewayClient(), [version]);

  const [state, setState] = useState<ConnectionState>("idle");
  const [error, setError] = useState<string | null>(null);

  // Profile or PTY channel change tears down both WebSockets. Bump `version`
  // (same path as the manual Reconnect button) so the gateway client is
  // recreated and the events feed resubscribes — otherwise the old events
  // socket's close handler can leave a stale error banner after a switch.
  const scopeKey = `${channel}\0${profile ?? ""}`;
  const prevScopeKey = useRef<string | null>(null);
  useEffect(() => {
    if (prevScopeKey.current === null) {
      prevScopeKey.current = scopeKey;
      return;
    }
    if (prevScopeKey.current === scopeKey) return;
    prevScopeKey.current = scopeKey;
    setError(null);
    setVersion((v) => v + 1);
  }, [scopeKey]);

  useEffect(() => {
    let cancelled = false;
    queueMicrotask(() => {
      if (cancelled) return;
      setError(null);
    });
    const offState = gw.onState(setState);

    const offError = gw.on<{ message?: string }>("error", (ev) => {
      const message = ev.payload?.message;

      if (message) {
        setError(message);
      }
    });

    // Connect only for liveness. Do not create a sidecar session: the PTY child
    // is the single Pepper chat session and owns provider/runtime binding.
    gw.connect()
      .catch((e: Error) => {
        if (!cancelled) {
          setError(e.message);
        }
      });

    return () => {
      cancelled = true;
      offState();
      offError();
      gw.close();
    };
    // `profile` is read from render; scope changes bump `version` → new `gw`.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gw]);

  // Event subscriber WebSocket — receives the rebroadcast of every
  // dispatcher emit from the PTY child's gateway.  See /api/pub +
  // /api/events in hermes_cli/web_server.py for the broadcast hop.
  //
  // Failures (auth/loopback rejection, server too old to expose the
  // endpoint, transient drops) surface in the same banner as the
  // JSON-RPC liveness socket so the sidebar matches its documented best-effort
  // UX and the user always has a reconnect affordance.
  useEffect(() => {
    if (!channel) {
      return;
    }
    // In loopback mode the legacy ?token=<session> path is fine; in gated
    // mode we have to mint a single-use ticket from the cookie. The IIFE
    // keeps the outer effect synchronous so its ``return cleanup`` stays
    // at the top level; the local ``ws`` is hoisted to a closed-over
    // binding the cleanup reads via ``wsRef``.
    let unmounting = false;
    let ws: WebSocket | null = null;
    void (async () => {
      const url = await buildWsUrl("/api/events", { channel });
      if (unmounting) {
        return;
      }
      ws = new WebSocket(url);

      // `unmounting` suppresses the banner during cleanup — `ws.close()`
      // from the effect's return fires a close event with code 1005 that
      // would otherwise look like an unexpected drop.
      const DISCONNECTED = "events feed disconnected — tool calls may not appear";
      const surface = (msg: string) => !unmounting && setError(msg);

      ws.addEventListener("error", () => surface(DISCONNECTED));

      ws.addEventListener("close", (ev) => {
        if (ev.code === 4401 || ev.code === 4403) {
          surface(`events feed rejected (${ev.code}) — reload the page`);
        } else if (ev.code !== 1000) {
          surface(DISCONNECTED);
        }
      });

      ws.addEventListener("message", (ev) => {
        let frame: RpcEnvelope;

        try {
          frame = JSON.parse(ev.data);
        } catch {
          return;
        }

        if (frame.method !== "event" || !frame.params) {
          return;
        }

        const { type, payload } = frame.params;

        if (type === "session.info") {
          const title = titleFromSessionInfoPayload(payload);
          if (title !== undefined) {
            onSessionTitleChange?.(title);
          }
        } else if (type === "dashboard.new_session_requested") {
          onDashboardNewSessionRequest?.();
        }
      });
    })();

    return () => {
      unmounting = true;
      ws?.close();
    };
  }, [channel, onDashboardNewSessionRequest, onSessionTitleChange, version]);

  const reconnect = useCallback(() => {
    setError(null);
    setVersion((v) => v + 1);
  }, []);

  const modelName = "gpt-5.5";
  const modelLabel = modelName.split("/").slice(-1)[0] ?? "gpt-5.5";
  const banner = error;
  const workflowControl = useRuntimeOverview().snapshot?.workflowControl ?? null;

  return (
    <aside
      className={cn(
        "flex h-full w-full min-w-0 shrink-0 flex-col gap-3 overflow-y-auto overflow-x-hidden pr-1",
        className,
      )}
    >
      <Card className="flex items-center justify-between gap-2 px-3 py-2">
        <div className="min-w-0 flex-1">
          <div className="text-display text-xs tracking-wider text-text-tertiary">
            Pepper Lead Agent
          </div>

          <div className="mt-1 min-w-0 text-sm font-medium text-text-primary">
            <span className="truncate">{modelLabel}</span>
          </div>
          <div className="mt-1 text-xs leading-relaxed text-text-secondary">
            Governed provider: OpenAI Codex OAuth. Generic model switching is
            disabled for Pepper Chat.
          </div>
        </div>

        <Badge tone={STATE_TONE[state]} className="shrink-0">
          {STATE_LABEL[state]}
        </Badge>
      </Card>

      {banner && (
        <Card className="flex items-start gap-2 border-destructive/40 bg-destructive/5 px-3 py-2 text-xs">
          <AlertCircle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-destructive" />

          <div className="min-w-0 flex-1">
            <div className="wrap-break-word text-destructive">{banner}</div>

            {error && (
              <Button
                size="sm"
                outlined
                className="mt-1"
                onClick={reconnect}
                prefix={<RefreshCw />}
              >
                reconnect tools feed
              </Button>
            )}
          </div>
        </Card>
      )}

      <ChatSidebarGovernedContext workflowControl={workflowControl} />

      <Card className="px-3 py-3 text-xs">
        <div className="text-display text-xs tracking-wider text-text-tertiary">
          WORK navigation
        </div>
        <div className="mt-3 grid gap-2">
          <a className="rounded-md border border-border-subtle/70 px-2 py-1.5 text-text-primary hover:bg-surface-hover" href="/agent-platform/projects">
            Projects and tickets
          </a>
          <a className="rounded-md border border-border-subtle/70 px-2 py-1.5 text-text-primary hover:bg-surface-hover" href="/agent-platform/approvals">
            Approvals
          </a>
          <a className="rounded-md border border-border-subtle/70 px-2 py-1.5 text-text-primary hover:bg-surface-hover" href="/agent-platform/executions">
            Executions
          </a>
        </div>
      </Card>

    </aside>
  );
}
