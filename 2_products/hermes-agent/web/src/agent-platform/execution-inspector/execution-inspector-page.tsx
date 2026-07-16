import { useDeferredValue, useState, type ReactNode } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Activity, Clock3, RefreshCw, Search, ShieldAlert } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Button } from "@nous-research/ui/ui/components/button";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";
import { Input } from "@nous-research/ui/ui/components/input";
import { Spinner } from "@nous-research/ui/ui/components/spinner";

import {
  EXECUTION_SOURCE_POSTURES,
  type ExecutionInspectorDataState,
} from "./contract";
import {
  buildExecutionDetailPath,
  type ExecutionInspectorLoader,
} from "./execution-client";
import { useExecutionInspector } from "./use-execution-inspector";

export interface ExecutionInspectorViewProps {
  readonly state: ExecutionInspectorDataState;
  readonly profile: string;
  readonly refresh: () => void;
}

function formatRefreshTime(value: number | null): string {
  return value === null ? "No successful refresh" : new Date(value).toLocaleTimeString();
}

function formatExecutionTimestamp(value: number | null): string {
  return value === null ? "not supplied" : new Date(value * 1000).toLocaleString();
}

export function ExecutionAuthorityNote() {
  return (
    <aside className="border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-subtle)] p-4 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
      <strong className="text-[var(--agent-platform-text-primary)]">Execution boundary.</strong>{" "}
      These are provisional source-local Hermes Kanban run facts. Governed execution authority is not active, and a source run is not a governed WorkPacket execution. No universal execution status or durable event history is inferred.
    </aside>
  );
}

export function ExecutionInspectorHeader({
  eyebrow,
  title,
  description,
  state,
  profile,
  refresh,
  children,
}: ExecutionInspectorViewProps & {
  readonly eyebrow: string;
  readonly title: string;
  readonly description: string;
  readonly children?: ReactNode;
}) {
  const tone = state.phase === "ready"
    ? "success"
    : state.phase === "stale"
      ? "warning"
      : state.phase === "error"
        ? "destructive"
        : "secondary";
  return (
    <header className="space-y-5 border-b border-[var(--agent-platform-border-default)] pb-6">
      <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0 space-y-2">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--agent-platform-text-muted)]">{eyebrow}</p>
          <h1 className="break-words text-3xl font-semibold tracking-tight sm:text-4xl" style={{ fontFamily: "var(--agent-platform-font-display)" }}>{title}</h1>
          <p className="max-w-3xl text-sm leading-relaxed text-[var(--agent-platform-text-secondary)] sm:text-base">{description}</p>
        </div>
        <Button
          outlined
          onClick={refresh}
          disabled={state.refreshing || state.phase === "loading"}
          prefix={state.refreshing ? <Spinner className="h-4 w-4" /> : <RefreshCw className="h-4 w-4" />}
        >
          Refresh
        </Button>
      </div>
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <Badge tone="secondary">Source: Hermes Kanban task runs</Badge>
        <Badge tone="warning">Provisional source</Badge>
        <Badge tone={tone}>{state.phase}</Badge>
        <span className="font-mono text-[var(--agent-platform-text-muted)]">Profile context: {profile}</span>
        <span className="font-mono text-[var(--agent-platform-text-muted)]">Last success: {formatRefreshTime(state.lastSuccessAt)}</span>
      </div>
      {children}
    </header>
  );
}

export function ExecutionBlockingState({
  state,
  refresh,
  unavailableLabel,
}: Pick<ExecutionInspectorViewProps, "state" | "refresh"> & { readonly unavailableLabel: string }) {
  if (state.snapshot || !["loading", "error", "unavailable"].includes(state.phase)) return null;
  const loading = state.phase === "loading";
  const title = loading
    ? "Loading exact execution source"
    : state.phase === "error"
      ? "Execution source could not be reached"
      : unavailableLabel;
  return (
    <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-panel)]" aria-busy={loading}>
      <CardContent className="flex min-h-64 flex-col items-center justify-center gap-4 p-8 text-center">
        {loading ? <Spinner className="h-5 w-5" /> : <ShieldAlert className="h-8 w-8 text-[var(--agent-platform-status-unavailable)]" />}
        <div className="max-w-2xl space-y-2">
          <h2 className="text-xl font-semibold">{title}</h2>
          <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
            {loading
              ? "Waiting for an exact board, task, and source-run response."
              : "Hermes has no safe universal execution collection. Select an exact Kanban board and task; API runs, cron sessions, general sessions, logs, PIDs and process telemetry are not used as fallbacks."}
          </p>
        </div>
        {!loading && <Button outlined onClick={refresh}>Try again</Button>}
      </CardContent>
    </Card>
  );
}

export function ExecutionStaleNotice({ state }: Pick<ExecutionInspectorViewProps, "state">) {
  if (state.phase !== "stale" || !state.snapshot) return null;
  return (
    <div role="status" className="border border-[var(--agent-platform-status-warning)] bg-[var(--agent-platform-surface-subtle)] px-4 py-3 text-sm text-[var(--agent-platform-text-secondary)]">
      Refresh failed. Showing only the last validated source-local projection from {formatRefreshTime(state.lastSuccessAt)}.
    </div>
  );
}

export function ExecutionInspectorView({ state, profile, refresh }: ExecutionInspectorViewProps) {
  const collection = state.snapshot?.kind === "executions" ? state.snapshot.collection : null;
  const filterIdentity = `${profile}\0${collection?.boardSlug ?? ""}\0${collection?.taskId ?? ""}`;
  const [storedFilter, setStoredFilter] = useState({ identity: filterIdentity, value: "" });
  const [storedStatus, setStoredStatus] = useState({ identity: filterIdentity, value: "all" });
  const filter = storedFilter.identity === filterIdentity ? storedFilter.value : "";
  const status = storedStatus.identity === filterIdentity ? storedStatus.value : "all";
  const deferredFilter = useDeferredValue(filter.trim().toLowerCase());
  const executions = collection?.executions ?? [];
  const statuses = [...new Set(executions.map((execution) => execution.originalSourceStatus))].sort();
  const visibleExecutions = executions.filter((execution) => {
    const matchesText = !deferredFilter || `${execution.sourceLocalExecutionId} ${execution.sourceProfile ?? ""} ${execution.originalSourceOutcome ?? ""}`.toLowerCase().includes(deferredFilter);
    return matchesText && (status === "all" || execution.originalSourceStatus === status);
  });

  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <ExecutionInspectorHeader
          eyebrow="AGENT PLATFORM / Source evidence"
          title="Execution Inspector"
          description="Read-only inspection of one exact Hermes Kanban task's source-local run records."
          state={state}
          profile={profile}
          refresh={refresh}
        />
        <ExecutionStaleNotice state={state} />
        <ExecutionBlockingState state={state} refresh={refresh} unavailableLabel="Qualified execution source unavailable" />
        <section className="grid gap-3 md:grid-cols-3" aria-label="Audited execution source kinds">
          {EXECUTION_SOURCE_POSTURES.map((source) => (
            <Card key={source.sourceType} className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
              <CardContent className="space-y-3 p-4">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <h2 className="text-sm font-semibold">{source.sourceType}</h2>
                  <Badge tone={source.availability === "qualified source" ? "warning" : "secondary"}>{source.availability}</Badge>
                </div>
                <p className="text-xs leading-relaxed text-[var(--agent-platform-text-secondary)]">{source.boundary}</p>
              </CardContent>
            </Card>
          ))}
        </section>

        {collection && (
          <>
            <ExecutionAuthorityNote />
            <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
              <CardContent className="grid gap-4 p-5 sm:grid-cols-3">
                <div><p className="text-xs uppercase tracking-wide text-[var(--agent-platform-text-muted)]">Board</p><p className="break-all font-mono text-sm">{collection.boardSlug}</p></div>
                <div><p className="text-xs uppercase tracking-wide text-[var(--agent-platform-text-muted)]">Task</p><p className="break-all font-mono text-sm">{collection.taskId}</p></div>
                <div><p className="text-xs uppercase tracking-wide text-[var(--agent-platform-text-muted)]">Source records</p><p className="text-2xl font-semibold">{executions.length}</p></div>
                <div className="sm:col-span-3"><p className="text-xs uppercase tracking-wide text-[var(--agent-platform-text-muted)]">Task title posture</p><p className="break-words text-sm">{collection.taskTitle}</p></div>
              </CardContent>
            </Card>
            <section className="grid gap-3 lg:grid-cols-[minmax(0,1fr)_14rem]" aria-label="Execution filters">
              <label className="relative block">
                <span className="sr-only">Filter source-local runs</span>
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--agent-platform-text-muted)]" />
                <Input className="pl-9" value={filter} onChange={(event) => setStoredFilter({ identity: filterIdentity, value: event.target.value })} placeholder="Filter by run ID, profile, or outcome" />
              </label>
              <label className="flex items-center gap-2 border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)] px-3">
                <span className="sr-only">Source run status</span>
                <select className="w-full bg-transparent py-2 text-sm outline-none" value={status} onChange={(event) => setStoredStatus({ identity: filterIdentity, value: event.target.value })}>
                  <option value="all">All source statuses</option>
                  {statuses.map((value) => <option key={value} value={value}>{value}</option>)}
                </select>
              </label>
            </section>

            {executions.length === 0 ? (
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="py-12 text-center text-[var(--agent-platform-text-secondary)]">The exact source task returned no run records.</CardContent>
              </Card>
            ) : visibleExecutions.length === 0 ? (
              <p className="py-8 text-center text-sm text-[var(--agent-platform-text-secondary)]">No source-local runs match the local filters.</p>
            ) : (
              <section className="space-y-3" aria-label="Source-local run records">
                {visibleExecutions.map((execution) => {
                  const detailPath = buildExecutionDetailPath(
                    execution.sourceLocalExecutionId,
                    execution.boardSlug,
                    execution.taskId,
                    profile,
                  );
                  return (
                    <Card key={execution.sourceLocalExecutionId} className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                      <CardContent className="grid gap-5 p-5 lg:grid-cols-[minmax(0,1fr)_auto]">
                        <div className="min-w-0 space-y-3">
                          <div className="flex flex-wrap items-start gap-2">
                            <h2 className="mr-auto break-words text-lg font-semibold">Run {execution.sourceLocalExecutionId}</h2>
                            <Badge tone="secondary">{execution.originalSourceStatus}</Badge>
                            {execution.originalSourceOutcome && <Badge tone="secondary">Outcome: {execution.originalSourceOutcome}</Badge>}
                          </div>
                          <div className="flex flex-wrap gap-x-5 gap-y-2 text-xs text-[var(--agent-platform-text-muted)]">
                            <span className="font-mono">Source-local ID: {execution.sourceLocalExecutionId}</span>
                            <span>Source profile: {execution.sourceProfile ?? "not supplied"}</span>
                            <span>Started: {formatExecutionTimestamp(execution.startedAt)}</span>
                            <span>Ended: {formatExecutionTimestamp(execution.endedAt)}</span>
                          </div>
                        </div>
                        {detailPath && (
                          <Link className="inline-flex items-center gap-2 self-end font-semibold text-[var(--agent-platform-action-primary)] underline-offset-4 hover:underline" to={detailPath}>
                            <Activity className="h-4 w-4" /> Inspect source record
                          </Link>
                        )}
                      </CardContent>
                    </Card>
                  );
                })}
              </section>
            )}
            <p className="inline-flex items-center gap-2 text-xs text-[var(--agent-platform-text-muted)]"><Clock3 className="h-4 w-4" /> Ordering is within this one task source only; no cross-source chronology is implied.</p>
          </>
        )}
      </main>
    </div>
  );
}

export function ExecutionInspectorPage({ loader }: { readonly loader?: ExecutionInspectorLoader } = {}) {
  const [searchParams] = useSearchParams();
  const boardSlug = searchParams.get("board") ?? "";
  const taskId = searchParams.get("task") ?? "";
  const { profile, refresh, ...state } = useExecutionInspector(
    { kind: "executions", boardSlug, taskId },
    loader,
  );
  return <ExecutionInspectorView state={state} profile={profile} refresh={refresh} />;
}
