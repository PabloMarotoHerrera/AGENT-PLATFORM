import type { ReactNode } from "react";
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  GitBranch,
  ListChecks,
  PlayCircle,
  Radio,
  RefreshCw,
  Server,
  ShieldCheck,
  Users,
} from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Button } from "@nous-research/ui/ui/components/button";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";
import { Spinner } from "@nous-research/ui/ui/components/spinner";

import type { RuntimeGatewayState, RuntimeWorkflowControl } from "./contract";
import {
  useRuntimeOverview,
  type RuntimeOverviewState,
} from "./use-runtime-overview";

interface RuntimeOverviewViewProps {
  readonly state: RuntimeOverviewState;
  readonly refresh: () => void;
}

const GATEWAY_LABELS: Record<RuntimeGatewayState, string> = {
  off: "Offline",
  running: "Running",
  starting: "Starting",
  stopped: "Stopped",
  failed: "Startup failed",
  unknown: "Unknown",
};

function phaseBadge(phase: RuntimeOverviewState["phase"]) {
  if (phase === "ready") return <Badge tone="success">Live</Badge>;
  if (phase === "stale") return <Badge tone="warning">Last known</Badge>;
  if (phase === "error") return <Badge tone="destructive">Connection error</Badge>;
  if (phase === "unavailable") return <Badge tone="secondary">Unavailable</Badge>;
  return <Badge tone="secondary">Loading</Badge>;
}

function yesNo(value: boolean) {
  return value ? "Yes" : "No";
}

function requiredLabel(value: boolean) {
  return value ? "Required" : "Not required";
}

function unavailableWorkflowMessage(phase: RuntimeOverviewState["phase"]) {
  if (phase === "loading") return "Loading bounded workflow-control read model…";
  if (phase === "error" || phase === "stale") return "Workflow-control read model is using no validated current response.";
  if (phase === "unavailable") return "Workflow-control provider did not expose the bounded Control Center fields.";
  return "Workflow-control provider is not configured for this runtime response.";
}

function Metric({
  icon: Icon,
  label,
  value,
  detail,
}: {
  readonly icon: typeof Activity;
  readonly label: string;
  readonly value: string | number;
  readonly detail: string;
}) {
  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="flex h-full flex-col gap-5 p-5">
        <div className="flex items-center justify-between gap-3 text-[var(--agent-platform-text-secondary)]">
          <span className="text-xs font-semibold uppercase tracking-[0.16em]">{label}</span>
          <Icon className="h-4 w-4" aria-hidden="true" />
        </div>
        <strong className="font-mono text-3xl font-medium tabular-nums text-[var(--agent-platform-text-primary)]">
          {value}
        </strong>
        <p className="text-sm leading-relaxed text-[var(--agent-platform-text-muted)]">{detail}</p>
      </CardContent>
    </Card>
  );
}

function Cell({ label, value, detail }: {
  readonly label: string;
  readonly value: string | number;
  readonly detail?: string;
}) {
  return (
    <div className="border-l-2 border-[var(--agent-platform-border-default)] pl-3">
      <dt className="text-xs text-[var(--agent-platform-text-muted)]">{label}</dt>
      <dd className="mt-1 break-words font-mono text-sm text-[var(--agent-platform-text-primary)]">{value}</dd>
      {detail && <dd className="mt-1 text-xs leading-relaxed text-[var(--agent-platform-text-muted)]">{detail}</dd>}
    </div>
  );
}

function OverviewQuestion({ title, answer, children }: {
  readonly title: string;
  readonly answer: string;
  readonly children?: ReactNode;
}) {
  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="space-y-4 p-5">
        <div>
          <h2 className="text-lg font-semibold text-[var(--agent-platform-text-primary)]">{title}</h2>
          <p className="mt-2 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">{answer}</p>
        </div>
        {children}
      </CardContent>
    </Card>
  );
}

function EmptyState({ phase, refresh }: Pick<RuntimeOverviewViewProps, "refresh"> & {
  readonly phase: "error" | "unavailable";
}) {
  const unavailable = phase === "unavailable";
  return (
    <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="flex min-h-72 flex-col items-center justify-center gap-4 p-8 text-center">
        <Server className="h-8 w-8 text-[var(--agent-platform-status-unavailable)]" aria-hidden="true" />
        <div className="max-w-md space-y-2">
          <h2 className="text-xl font-semibold text-[var(--agent-platform-text-primary)]">
            {unavailable ? "Runtime status unavailable" : "Runtime status could not be reached"}
          </h2>
          <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
            {unavailable
              ? "The service responded without the bounded status fields this overview requires."
              : "No runtime details are shown until a validated status response succeeds."}
          </p>
        </div>
        <Button outlined onClick={refresh} prefix={<RefreshCw className="h-4 w-4" />}>
          Try again
        </Button>
      </CardContent>
    </Card>
  );
}

function ControlCenter({ workflowControl }: { readonly workflowControl: RuntimeWorkflowControl }) {
  const currentWorkAnswer = workflowControl.currentTicketId
    ? `${workflowControl.currentTicketId}: ${workflowControl.currentTicketTitle ?? "Untitled governed ticket"}`
    : "No current governed ticket is active.";
  const attentionReasons = [
    workflowControl.pendingTicketApprovalCount > 0 ? "ticket approval pending" : null,
    workflowControl.reviewDecisionRequired ? "review decision required" : null,
    workflowControl.humanAcceptanceRequired && !workflowControl.humanAcceptanceRecorded ? "human acceptance required" : null,
    workflowControl.gitHandoffRequired ? "Git handoff required" : null,
    workflowControl.readyRequiresHumanSmoke ? "human smoke check required" : null,
    workflowControl.remainingBlockerCount > 0 ? "blockers remain" : null,
    workflowControl.failureCategory ? "recovery evidence present" : null,
  ].filter(Boolean).join("; ");
  const executionAnswer = workflowControl.activeExecutionCount > 0
    ? `${workflowControl.activeExecutionCount} active execution(s); ${workflowControl.executionCount} total recorded.`
    : "No active executions are running.";

  return (
    <section className="grid gap-4 lg:grid-cols-2" aria-label="Pepper Control Center overview questions">
      <OverviewQuestion title="Current Work" answer={currentWorkAnswer}>
        <dl className="grid gap-3 text-sm sm:grid-cols-2">
          <Cell label="Project" value={`${workflowControl.projectId} / ${workflowControl.macroprojectId}`} />
          <Cell label="Workflow status" value={workflowControl.workflowStatus} />
        </dl>
      </OverviewQuestion>

      <OverviewQuestion title="Next Governed Action" answer={workflowControl.nextActionLabel}>
        <dl className="grid gap-3 text-sm sm:grid-cols-2">
          <Cell label="Canonical action ID" value={workflowControl.nextActionId} />
          <Cell label="Required human action" value={workflowControl.nextActionRequiredHumanAction} />
          <Cell label="Target ticket" value={workflowControl.nextActionTargetTicketId ?? "No target ticket"} detail={workflowControl.nextActionTargetTicketTitle ?? undefined} />
        </dl>
      </OverviewQuestion>

      <OverviewQuestion title="Needs Attention" answer={attentionReasons || "No human-attention condition is currently raised."}>
        <dl className="grid gap-3 text-sm sm:grid-cols-2">
          <Cell label="Pending ticket approvals" value={workflowControl.pendingTicketApprovalCount} />
          <Cell label="Remaining blockers" value={workflowControl.remainingBlockerCount} />
          <Cell label="Warnings" value={workflowControl.warningCount} />
          <Cell label="Manual chat control" value={requiredLabel(workflowControl.manualChatControlRequired)} />
        </dl>
      </OverviewQuestion>

      <OverviewQuestion title="Execution" answer={executionAnswer}>
        <dl className="grid gap-3 text-sm sm:grid-cols-2">
          <Cell label="Execution state" value={workflowControl.executionState} />
          <Cell label="Gateway work" value={workflowControl.activeExecutionCount > 0 ? "Active" : "Idle"} />
        </dl>
      </OverviewQuestion>

      <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-elevated)] lg:col-span-2">
        <CardContent className="space-y-4 p-5 sm:p-6">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.16em] text-[var(--agent-platform-text-muted)]">Governed State</p>
              <h2 className="mt-2 text-xl font-semibold">Pepper Control Center</h2>
              <p className="mt-2 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                Read-only governed state composed from the bounded runtime status and workflow-control read models.
              </p>
            </div>
            <Badge tone={workflowControl.readyRequiresHumanSmoke || workflowControl.blockerCount > 0 ? "warning" : "success"}>{workflowControl.readiness}</Badge>
          </div>
          <dl className="grid gap-3 text-sm sm:grid-cols-2 lg:grid-cols-4">
            <Cell label="Approval" value={workflowControl.approvalState} detail={`${workflowControl.pendingApprovalCount} total pending`} />
            <Cell label="Queue" value={workflowControl.queueState} />
            <Cell label="Execution" value={workflowControl.executionState} detail={`${workflowControl.activeExecutionCount} active`} />
            <Cell label="Validation" value={workflowControl.validationState} />
            <Cell label="Review" value={workflowControl.reviewState} detail={`Decision recorded: ${yesNo(workflowControl.reviewDecisionRecorded)}`} />
            <Cell label="Recovery" value={workflowControl.recoveryState} detail={workflowControl.failureSummary ?? workflowControl.failureCategory ?? undefined} />
            <Cell label="Git handoff" value={workflowControl.gitHandoffState} detail={workflowControl.humanGitAuthority} />
            <Cell label="Default mode" value={workflowControl.defaultModeEnabled ? "Enabled" : "Disabled"} />
            <Cell label="Manual OpenCode ticket copy" value={requiredLabel(workflowControl.manualOpenCodeTicketCopyRequired)} />
            <Cell label="Manual OpenCode result copy" value={requiredLabel(workflowControl.manualOpenCodeResultCopyRequired)} />
            <Cell label="Closed P18.8 gaps" value={workflowControl.closedGapCount} />
            <Cell label="Blockers" value={workflowControl.blockerCount} />
          </dl>
        </CardContent>
      </Card>
    </section>
  );
}

export function RuntimeOverviewView({ state, refresh }: RuntimeOverviewViewProps) {
  const { snapshot } = state;
  const workflowControl = snapshot?.workflowControl ?? null;

  return (
    <div
      className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]"
      style={{ fontFamily: "var(--agent-platform-font-body)" }}
    >
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8" aria-labelledby="runtime-overview-title">
        <header className="flex flex-col gap-5 border-b border-[var(--agent-platform-border-default)] pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div className="space-y-2">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--agent-platform-text-muted)]">
              AGENT PLATFORM / Control Center
            </p>
            <h1
              id="runtime-overview-title"
              className="text-3xl font-semibold tracking-tight sm:text-4xl"
              style={{ fontFamily: "var(--agent-platform-font-display)" }}
            >
              Control Center Overview
            </h1>
            <p className="max-w-2xl text-sm leading-relaxed text-[var(--agent-platform-text-secondary)] sm:text-base">
              A read-only Pepper Control Center summary answering current work, next governed action, needs attention, execution, and governed-state questions.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span aria-live="polite">{phaseBadge(state.phase)}</span>
            <Button
              outlined
              onClick={refresh}
              disabled={state.refreshing || state.phase === "loading"}
              prefix={state.refreshing ? <Spinner className="h-4 w-4" /> : <RefreshCw className="h-4 w-4" />}
            >
              Refresh
            </Button>
          </div>
        </header>

        {state.phase === "loading" && (
          <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]" aria-busy="true">
            <CardContent className="flex min-h-72 items-center justify-center gap-3 p-8 text-[var(--agent-platform-text-secondary)]">
              <Spinner className="h-5 w-5" />
              <span>Loading bounded runtime status…</span>
            </CardContent>
          </Card>
        )}

        {(state.phase === "error" || state.phase === "unavailable") && snapshot === null && (
          <EmptyState phase={state.phase} refresh={refresh} />
        )}

        {snapshot && (
          <>
            {state.phase === "stale" && (
              <div
                role="status"
                className="border border-[var(--agent-platform-status-warning)] bg-[var(--agent-platform-surface-subtle)] px-4 py-3 text-sm text-[var(--agent-platform-text-secondary)]"
              >
                Live refresh failed. Showing the last validated response from{" "}
                {state.lastSuccessAt ? new Date(state.lastSuccessAt).toLocaleTimeString() : "an earlier check"}.
              </div>
            )}

            <Card className="overflow-hidden border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-elevated)]">
              <CardContent className="grid gap-6 p-6 md:grid-cols-[1.4fr_1fr] md:p-8">
                <div className="space-y-5">
                  <div className="flex items-center gap-3">
                    <span
                      className={`h-2.5 w-2.5 rounded-full ${snapshot.gateway.running ? "bg-[var(--agent-platform-status-success)]" : "bg-[var(--agent-platform-status-disabled)]"}`}
                      aria-hidden="true"
                    />
                    <span className="text-xs font-semibold uppercase tracking-[0.16em] text-[var(--agent-platform-text-secondary)]">
                      Gateway
                    </span>
                  </div>
                  <div>
                    <p className="text-4xl font-semibold tracking-tight sm:text-5xl" style={{ fontFamily: "var(--agent-platform-font-display)" }}>
                      {GATEWAY_LABELS[snapshot.gateway.state]}
                    </p>
                    <p className="mt-3 text-sm text-[var(--agent-platform-text-secondary)]">
                      {snapshot.gateway.busy
                        ? "Gateway work is currently in flight."
                        : snapshot.gateway.running
                          ? "Gateway is live with no in-flight activity."
                          : "No gateway process is active."}
                    </p>
                  </div>
                </div>
                <dl className="grid grid-cols-2 gap-px overflow-hidden border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-border-default)]">
                  <div className="bg-[var(--agent-platform-surface-panel)] p-4">
                    <dt className="text-xs text-[var(--agent-platform-text-muted)]">Drainable</dt>
                    <dd className="mt-2 font-mono text-sm">{snapshot.gateway.drainable ? "Yes" : "No"}</dd>
                  </div>
                  <div className="bg-[var(--agent-platform-surface-panel)] p-4">
                    <dt className="text-xs text-[var(--agent-platform-text-muted)]">Access gate</dt>
                    <dd className="mt-2 font-mono text-sm">{snapshot.access.authRequired ? "Required" : "Loopback"}</dd>
                  </div>
                  <div className="col-span-2 bg-[var(--agent-platform-surface-panel)] p-4">
                    <dt className="text-xs text-[var(--agent-platform-text-muted)]">Hermes version</dt>
                    <dd className="mt-2 font-mono text-sm">{snapshot.platform.version}</dd>
                  </div>
                </dl>
              </CardContent>
            </Card>

            <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-label="Runtime activity">
              <Metric
                icon={Users}
                label="Recent sessions"
                value={snapshot.activity.activeSessions}
                detail="Sessions active in the backend's recent five-minute window."
              />
              <Metric
                icon={Activity}
                label="Gateway activity"
                value={snapshot.activity.activeAgents}
                detail="In-flight Hermes gateway turns, not governed AGENT PLATFORM Agents."
              />
              <Metric
                icon={snapshot.access.authRequired ? ShieldCheck : Radio}
                label="Dashboard access"
                value={snapshot.access.authRequired ? "Gated" : "Local"}
                detail={snapshot.access.authRequired ? "Dashboard authentication is required." : "The dashboard is bound to its local trust envelope."}
              />
            </section>

            {workflowControl ? (
              <ControlCenter workflowControl={workflowControl} />
            ) : (
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="flex items-start gap-3 p-5 text-sm text-[var(--agent-platform-text-secondary)]">
                  <AlertTriangle className="mt-0.5 h-4 w-4 text-[var(--agent-platform-status-warning)]" aria-hidden="true" />
                  <div>
                    <h2 className="font-semibold text-[var(--agent-platform-text-primary)]">Workflow-control unavailable</h2>
                    <p className="mt-1 leading-relaxed">{unavailableWorkflowMessage(state.phase)}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            <section className="flex flex-col gap-4 border-t border-[var(--agent-platform-border-default)] pt-6 sm:flex-row sm:items-center sm:justify-between" aria-label="Platform version">
              <div className="flex flex-wrap items-center gap-3">
                <CheckCircle2 className="h-4 w-4 text-[var(--agent-platform-status-success)]" aria-hidden="true" />
                <ListChecks className="h-4 w-4 text-[var(--agent-platform-text-muted)]" aria-hidden="true" />
                <PlayCircle className="h-4 w-4 text-[var(--agent-platform-text-muted)]" aria-hidden="true" />
                <GitBranch className="h-4 w-4 text-[var(--agent-platform-text-muted)]" aria-hidden="true" />
                <div>
                  <h2 className="font-semibold">Platform contract</h2>
                  <p className="mt-1 text-sm text-[var(--agent-platform-text-secondary)]">
                    Config schema {snapshot.platform.configVersion} / latest {snapshot.platform.latestConfigVersion} · release {snapshot.platform.releaseDate}
                  </p>
                </div>
              </div>
              <Badge tone={snapshot.platform.updateAvailable ? "warning" : "success"}>
                {snapshot.platform.updateAvailable ? "Update available" : "Configuration current"}
              </Badge>
            </section>
          </>
        )}
      </div>
    </div>
  );
}

export function RuntimeOverviewPage() {
  const { refresh, ...state } = useRuntimeOverview();
  return <RuntimeOverviewView state={state} refresh={refresh} />;
}
