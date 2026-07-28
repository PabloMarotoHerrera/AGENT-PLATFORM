import { useDeferredValue, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { Clock3, FileCheck2, RefreshCw, Search, ShieldAlert } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Button } from "@nous-research/ui/ui/components/button";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";
import { Input } from "@nous-research/ui/ui/components/input";
import { Spinner } from "@nous-research/ui/ui/components/spinner";

import type { ApprovalInboxLoader } from "./approval-client";
import { buildApprovalDetailPath } from "./approval-client";
import type { ApprovalInboxDataState, ApprovalVisualStatus } from "./contract";
import { useApprovalInbox } from "./use-approval-inbox";

export interface ApprovalWorkspaceViewProps {
  readonly state: ApprovalInboxDataState;
  readonly profile: string;
  readonly refresh: () => void;
}

function formatSourceTime(value: number | null): string {
  return value === null ? "No successful refresh" : new Date(value).toLocaleTimeString();
}

function formatApprovalTimestamp(value: number | null): string {
  return value === null ? "not supplied" : new Date(value * 1000).toLocaleString();
}

function statusTone(status: ApprovalVisualStatus): "success" | "warning" | "destructive" | "secondary" {
  if (status === "approved") return "success";
  if (status === "pending" || status === "expired") return "warning";
  if (status === "rejected") return "destructive";
  return "secondary";
}

export function ApprovalAuthorityNote() {
  return (
    <aside className="border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-subtle)] p-4 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
      <strong className="text-[var(--agent-platform-text-primary)]">Authority boundary.</strong>{" "}
      These are provisional source approval presentations. No governed AGENT PLATFORM approval authority is active.
      Source pending is not governed pending approval, and source decisions are not governed decisions.
    </aside>
  );
}

export function ApprovalWorkspaceHeader({
  eyebrow,
  title,
  description,
  state,
  profile,
  refresh,
  children,
}: ApprovalWorkspaceViewProps & {
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
        <Badge tone="secondary">Source: Hermes staged write approvals</Badge>
        <Badge tone="warning">Provisional source</Badge>
        <Badge tone={tone}>{state.phase}</Badge>
        <span className="font-mono text-[var(--agent-platform-text-muted)]">Profile: {profile}</span>
        <span className="font-mono text-[var(--agent-platform-text-muted)]">Last success: {formatSourceTime(state.lastSuccessAt)}</span>
      </div>
      {children}
    </header>
  );
}

export function ApprovalBlockingState({
  state,
  refresh,
  unavailableLabel,
}: Pick<ApprovalWorkspaceViewProps, "state" | "refresh"> & { readonly unavailableLabel: string }) {
  if (state.snapshot || !["loading", "error", "unavailable"].includes(state.phase)) return null;
  const loading = state.phase === "loading";
  const title = loading
    ? "Loading approval source"
    : state.phase === "error"
      ? "Approval source could not be reached"
      : unavailableLabel;
  return (
    <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-panel)]" aria-busy={loading}>
      <CardContent className="flex min-h-64 flex-col items-center justify-center gap-4 p-8 text-center">
        {loading ? <Spinner className="h-5 w-5" /> : <ShieldAlert className="h-8 w-8 text-[var(--agent-platform-status-unavailable)]" />}
        <div className="max-w-2xl space-y-2">
          <h2 className="text-xl font-semibold">{title}</h2>
          <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
            {loading
              ? "Waiting for an exact source-qualified response."
              : "Hermes has no safe authenticated dashboard list/detail read for its durable staged-write source. Kanban, Chat, logs, providers, workers, OAuth and transient prompts are not used as fallbacks."}
          </p>
        </div>
        {!loading && <Button outlined onClick={refresh}>Try again</Button>}
      </CardContent>
    </Card>
  );
}

export function ApprovalStaleNotice({ state }: Pick<ApprovalWorkspaceViewProps, "state">) {
  if (state.phase !== "stale" || !state.snapshot) return null;
  return (
    <div role="status" className="border border-[var(--agent-platform-status-warning)] bg-[var(--agent-platform-surface-subtle)] px-4 py-3 text-sm text-[var(--agent-platform-text-secondary)]">
      Refresh failed. Showing only the last validated provisional source projection from {formatSourceTime(state.lastSuccessAt)}.
    </div>
  );
}

export function ApprovalInboxView({ state, profile, refresh }: ApprovalWorkspaceViewProps) {
  const [filter, setFilter] = useState("");
  const [status, setStatus] = useState("all");
  const [requestType, setRequestType] = useState("all");
  const deferredFilter = useDeferredValue(filter.trim().toLowerCase());
  const approvals = state.snapshot?.kind === "inbox" ? state.snapshot.approvals : [];
  const pendingCount = approvals.filter((approval) => approval.visualStatus === "pending").length;
  const historicalCount = approvals.length - pendingCount;
  const requestTypes = [...new Set(approvals.map((approval) => approval.originalSourceType))].sort();
  const visibleApprovals = approvals.filter((approval) => {
    const matchesText = !deferredFilter || `${approval.title} ${approval.summary} ${approval.sourceLocalApprovalId} ${approval.target.sourceTargetLabel}`.toLowerCase().includes(deferredFilter);
    return matchesText && (status === "all" || approval.visualStatus === status) &&
      (requestType === "all" || approval.originalSourceType === requestType);
  });

  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <ApprovalWorkspaceHeader
          eyebrow="AGENT PLATFORM / Decision source"
          title="Approval Inbox"
          description="Read-only presentations of explicit Hermes source requests when a safe source read is available."
          state={state}
          profile={profile}
          refresh={refresh}
        />
        <ApprovalStaleNotice state={state} />
        <ApprovalBlockingState state={state} refresh={refresh} unavailableLabel="Approval source unavailable" />

        {state.snapshot?.kind === "inbox" && (
          <>
            <ApprovalAuthorityNote />
            <section className="grid gap-3 sm:grid-cols-2" aria-label="Source approval counts">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="flex items-center justify-between p-5"><span>Pending in source</span><Badge tone="warning">{pendingCount}</Badge></CardContent>
              </Card>
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="flex items-center justify-between p-5"><span>Historical source states</span><Badge tone="secondary">{historicalCount}</Badge></CardContent>
              </Card>
            </section>
            <section className="grid gap-3 lg:grid-cols-[minmax(0,1fr)_12rem_14rem]" aria-label="Approval filters">
              <label className="relative block">
                <span className="sr-only">Filter approval presentations</span>
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--agent-platform-text-muted)]" />
                <Input className="pl-9" value={filter} onChange={(event) => setFilter(event.target.value)} placeholder="Filter by title, source ID, target, or summary" />
              </label>
              <label className="flex items-center gap-2 border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)] px-3 focus-within:border-[var(--agent-platform-action-primary)] focus-within:ring-2 focus-within:ring-[var(--agent-platform-focus-ring)]">
                <span className="sr-only">Source status</span>
                <select className="w-full bg-transparent py-2 text-sm outline-none" value={status} onChange={(event) => setStatus(event.target.value)}>
                  <option value="all">All source states</option>
                  {(["pending", "approved", "rejected", "expired", "cancelled", "other"] as const).map((value) => <option key={value} value={value}>{value}</option>)}
                </select>
              </label>
              <label className="flex items-center gap-2 border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)] px-3 focus-within:border-[var(--agent-platform-action-primary)] focus-within:ring-2 focus-within:ring-[var(--agent-platform-focus-ring)]">
                <span className="sr-only">Source request type</span>
                <select className="w-full bg-transparent py-2 text-sm outline-none" value={requestType} onChange={(event) => setRequestType(event.target.value)}>
                  <option value="all">All request types</option>
                  {requestTypes.map((value) => <option key={value} value={value}>{value}</option>)}
                </select>
              </label>
            </section>

            {approvals.length === 0 ? (
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="py-12 text-center text-[var(--agent-platform-text-secondary)]">The safe source returned no approval presentations.</CardContent>
              </Card>
            ) : visibleApprovals.length === 0 ? (
              <p className="py-8 text-center text-sm text-[var(--agent-platform-text-secondary)]">No approval presentations match the local filters.</p>
            ) : (
              <section className="space-y-3" aria-label="Approval presentations">
                {visibleApprovals.map((approval) => (
                  <Card key={approval.sourceLocalApprovalId} className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                    <CardContent className="grid gap-5 p-5 lg:grid-cols-[minmax(0,1fr)_auto]">
                      <div className="min-w-0 space-y-3">
                        <div className="flex flex-wrap items-start gap-2">
                          <h2 className="mr-auto break-words text-lg font-semibold">{approval.title}</h2>
                          <Badge tone={statusTone(approval.visualStatus)}>{approval.originalSourceStatus}</Badge>
                          <Badge tone="secondary">{approval.originalSourceType}</Badge>
                        </div>
                        <p className="line-clamp-3 whitespace-pre-wrap break-words text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">{approval.summary}</p>
                        <div className="flex flex-wrap gap-x-5 gap-y-2 text-xs text-[var(--agent-platform-text-muted)]">
                          <span className="font-mono">Source ID: {approval.sourceLocalApprovalId}</span>
                          <span>Target: {approval.target.sourceTargetLabel}</span>
                          <span>Requested: {formatApprovalTimestamp(approval.requestedAt)}</span>
                          <span>Expires: {formatApprovalTimestamp(approval.expiresAt)}</span>
                        </div>
                      </div>
                      <Link className="inline-flex items-center gap-2 self-end font-semibold text-[var(--agent-platform-action-primary)] underline-offset-4 hover:underline" to={buildApprovalDetailPath(approval.sourceLocalApprovalId, profile) ?? "#"}>
                        <FileCheck2 className="h-4 w-4" /> View presentation
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </section>
            )}
            <p className="inline-flex items-center gap-2 text-xs text-[var(--agent-platform-text-muted)]"><Clock3 className="h-4 w-4" /> Source timestamps are displayed without inferring governed decision state.</p>
          </>
        )}
      </div>
    </div>
  );
}

export function ApprovalInboxPage({ loader }: { readonly loader?: ApprovalInboxLoader } = {}) {
  const { profile, refresh, ...state } = useApprovalInbox({ kind: "inbox" }, loader);
  return <ApprovalInboxView state={state} profile={profile} refresh={refresh} />;
}
