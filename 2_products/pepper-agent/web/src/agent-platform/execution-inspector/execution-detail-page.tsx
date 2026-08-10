import type { ReactNode } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { ArrowLeft, Clock3, FileCheck2, FileText, FileWarning, History, Package, ShieldCheck, TriangleAlert } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";

import { buildExecutionsPath, type ExecutionInspectorLoader } from "./execution-client";
import type { ExecutionEvidenceSection } from "./contract";
import {
  ExecutionAuthorityNote,
  ExecutionBlockingState,
  ExecutionInspectorHeader,
  ExecutionStaleNotice,
  type ExecutionInspectorViewProps,
} from "./execution-inspector-page";
import { useExecutionInspector } from "./use-execution-inspector";

function formatExecutionTimestamp(value: number | null): string {
  return value === null ? "not supplied" : new Date(value * 1000).toLocaleString();
}

function EvidenceCard<T>({
  title,
  icon: Icon,
  section,
  emptyLabel,
  unavailableLabel,
  children,
}: {
  readonly title: string;
  readonly icon: typeof FileText;
  readonly section: ExecutionEvidenceSection<T>;
  readonly emptyLabel: string;
  readonly unavailableLabel: string;
  readonly children: (item: T) => ReactNode;
}) {
  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="space-y-4 p-5">
        <div className="flex items-center justify-between gap-3">
          <h2 className="inline-flex items-center gap-2 font-semibold"><Icon className="h-4 w-4" /> {title}</h2>
          <Badge tone={section.phase === "unavailable" ? "warning" : "secondary"}>{section.phase}</Badge>
        </div>
        {section.phase === "unavailable" ? (
          <p className="text-sm text-[var(--agent-platform-text-secondary)]">{unavailableLabel}</p>
        ) : section.items.length === 0 ? (
          <p className="text-sm text-[var(--agent-platform-text-secondary)]">{emptyLabel}</p>
        ) : (
          <div className="space-y-3">{section.items.map(children)}</div>
        )}
      </CardContent>
    </Card>
  );
}

export function ExecutionDetailView({
  state,
  profile,
  refresh,
  requestedBoardSlug = "",
  requestedTaskId = "",
}: ExecutionInspectorViewProps & {
  readonly requestedBoardSlug?: string;
  readonly requestedTaskId?: string;
}) {
  const execution = state.snapshot?.kind === "detail" ? state.snapshot.execution : null;
  const collectionPath = buildExecutionsPath(
    profile,
    execution?.boardSlug ?? requestedBoardSlug,
    execution?.taskId ?? requestedTaskId,
  ) ?? buildExecutionsPath(profile);
  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <Link className="inline-flex w-fit items-center gap-2 text-sm text-[var(--agent-platform-text-secondary)] hover:text-[var(--agent-platform-text-primary)]" to={collectionPath ?? "/agent-platform/executions"}>
          <ArrowLeft className="h-4 w-4" /> Execution Inspector
        </Link>
        <ExecutionInspectorHeader
          eyebrow="AGENT PLATFORM / Source-local run"
          title={execution ? `Run ${execution.sourceLocalExecutionId}` : "Execution source record"}
          description={execution
            ? `Exact Hermes Kanban run ${execution.sourceLocalExecutionId} for task ${execution.taskId}.`
            : "Loading one exact board, task, and source-run identity."}
          state={state}
          profile={profile}
          refresh={refresh}
        >
          {execution && (
            <div className="flex flex-wrap gap-2">
              <Badge tone="success">Controlled source</Badge>
              <Badge tone="secondary">Source status: {execution.originalSourceStatus}</Badge>
              <span className="break-all font-mono text-xs text-[var(--agent-platform-text-muted)]">Board / task / run: {execution.boardSlug} / {execution.taskId} / {execution.sourceLocalExecutionId}</span>
            </div>
          )}
        </ExecutionInspectorHeader>
        <ExecutionStaleNotice state={state} />
        <ExecutionBlockingState state={state} refresh={refresh} unavailableLabel="Selected source-local run unavailable" />

        {execution && (
          <>
            <ExecutionAuthorityNote />
            <section className="grid gap-4 lg:grid-cols-2" aria-label="Execution source facts">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-4 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><Clock3 className="h-4 w-4" /> Source timing and state</h2>
                  <dl className="grid grid-cols-[max-content_1fr] gap-x-4 gap-y-2 text-sm text-[var(--agent-platform-text-secondary)]">
                    <dt>Status</dt><dd>{execution.originalSourceStatus}</dd>
                    <dt>Outcome</dt><dd>{execution.originalSourceOutcome ?? "not supplied"}</dd>
                    <dt>Workflow</dt><dd>{execution.workflowState ?? "not supplied"}</dd>
                    <dt>Next action</dt><dd>{execution.nextAction ?? "inspect_detail"}</dd>
                    <dt>Started</dt><dd>{formatExecutionTimestamp(execution.startedAt)}</dd>
                    <dt>Ended</dt><dd>{formatExecutionTimestamp(execution.endedAt)}</dd>
                    <dt>Source profile</dt><dd>{execution.sourceProfile ?? "not supplied"}</dd>
                  </dl>
                </CardContent>
              </Card>
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-4 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><FileWarning className="h-4 w-4" /> Retention and redaction</h2>
                  <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">{execution.source.retentionLimitation}</p>
                  <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">Executable content is excluded. Result and failure presence is shown without raw narrative detail; metadata, event payloads, logs, claims, PIDs, paths and process inspection are not displayed.</p>
                  <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">Git handoff: {execution.gitHandoffState ?? "human_git_authority_preserved"}. WorkPacket: {execution.workPacketId ?? "not supplied"}.</p>
                </CardContent>
              </Card>
            </section>
            <section className="grid gap-4 lg:grid-cols-2" aria-label="Execution classification and validation">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><ShieldCheck className="h-4 w-4" /> Safe action category</h2>
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">{execution.safeActionCategory}</p>
                  <Badge tone="secondary">Executable content {execution.executableContent}</Badge>
                </CardContent>
              </Card>
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><FileCheck2 className="h-4 w-4" /> Validation summaries</h2>
                  <ul className="space-y-2 text-sm text-[var(--agent-platform-text-secondary)]">
                    {execution.validationSummaries.map((summary) => <li key={summary}>{summary}</li>)}
                  </ul>
                </CardContent>
              </Card>
            </section>
            <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
              <CardContent className="space-y-4 p-5">
                <div className="flex items-center justify-between gap-3">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><History className="h-4 w-4" /> Explicitly linked source events</h2>
                  <Badge tone={execution.linkedEvents.phase === "unavailable" ? "warning" : "secondary"}>{execution.linkedEvents.phase}</Badge>
                </div>
                {execution.linkedEvents.phase === "unavailable" ? (
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">The linked event section could not be projected safely.</p>
                ) : execution.linkedEvents.items.length === 0 ? (
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">No retained events explicitly reference this source run.</p>
                ) : (
                  <ol className="space-y-3">
                    {execution.linkedEvents.items.map((event) => (
                      <li key={event.sourceLocalEventId} className="grid gap-2 border-b border-[var(--agent-platform-border-default)] pb-3 text-sm sm:grid-cols-[1fr_auto]">
                        <span className="break-words">{event.sourceEventKind}</span>
                        <time className="text-xs text-[var(--agent-platform-text-muted)]">{formatExecutionTimestamp(event.occurredAt)}</time>
                        <code className="text-xs text-[var(--agent-platform-text-muted)] sm:col-span-2">Source event ID: {event.sourceLocalEventId}</code>
                      </li>
                    ))}
                  </ol>
                )}
                <p className="text-xs text-[var(--agent-platform-text-muted)]">Display timeline ordering is source-local presentation, not authoritative causality.</p>
              </CardContent>
            </Card>
            <section className="grid gap-4 lg:grid-cols-2" aria-label="Bounded execution evidence">
              <EvidenceCard title="Result summary" icon={FileText} section={execution.resultSummary} emptyLabel="No safe source result summary." unavailableLabel="The source result summary could not be projected safely.">
                {(item) => <p key={item.sourceLocalExecutionId} className="whitespace-pre-wrap break-words text-sm text-[var(--agent-platform-text-secondary)]">{item.safeText}</p>}
              </EvidenceCard>
              <EvidenceCard title="Failure summary" icon={TriangleAlert} section={execution.failureSummary} emptyLabel="No source failure summary." unavailableLabel="The source failure summary could not be projected safely.">
                {(item) => <p key={item.sourceLocalExecutionId} className="text-sm text-[var(--agent-platform-text-secondary)]">{item.safeText}</p>}
              </EvidenceCard>
              <EvidenceCard title="Artifact-reference metadata" icon={Package} section={execution.artifactReferences} emptyLabel="No task-level artifact references." unavailableLabel="Artifact-reference metadata could not be projected safely.">
                {(item) => (
                  <div key={item.sourceLocalArtifactId} className="space-y-1 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <p className="break-words">{item.displayFilename}</p>
                    <p className="text-xs text-[var(--agent-platform-text-muted)]">Source artifact ID {item.sourceLocalArtifactId} / {item.mediaType ?? "media type not supplied"} / {item.sizeBytes ?? "size not supplied"} bytes</p>
                    <p className="text-xs text-[var(--agent-platform-text-muted)]">Task-level metadata; not attributed to this run.</p>
                  </div>
                )}
              </EvidenceCard>
              <EvidenceCard title="Diagnostics" icon={FileWarning} section={execution.diagnostics} emptyLabel="No diagnostics explicitly reference this source run." unavailableLabel="Diagnostics could not be projected safely.">
                {(item) => (
                  <div key={item.sourceLocalDiagnosticId} className="space-y-2 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <div className="flex items-center justify-between gap-3"><span>{item.safeMessage}</span><Badge tone={item.severity === "warning" ? "warning" : "destructive"}>{item.severity}</Badge></div>
                    <p className="text-xs text-[var(--agent-platform-text-muted)]">Source diagnostic {item.sourceLocalDiagnosticId}; count {item.count}</p>
                  </div>
                )}
              </EvidenceCard>
            </section>
            <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-subtle)]">
              <CardContent className="space-y-3 p-5 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                <h2 className="font-semibold text-[var(--agent-platform-text-primary)]">Inspector limitations</h2>
                <p>Stop, retry, rollback, assignment, and Git actions are not automated here. Worker handoff preparation is explicit and bounded to the accepted P15/P17 substrate.</p>
                <p>Task status is not substituted for run status, missing events are not evidence of inactivity, and this source-local run is not a durable audit timeline.</p>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
}

export function ExecutionDetailPage({ loader }: { readonly loader?: ExecutionInspectorLoader } = {}) {
  const { executionId = "" } = useParams();
  const [searchParams] = useSearchParams();
  const boardSlug = searchParams.get("board") ?? "";
  const taskId = searchParams.get("task") ?? "";
  const { profile, refresh, ...state } = useExecutionInspector(
    { kind: "detail", boardSlug, taskId, executionId },
    loader,
  );
  return (
    <ExecutionDetailView
      state={state}
      profile={profile}
      refresh={refresh}
      requestedBoardSlug={boardSlug}
      requestedTaskId={taskId}
    />
  );
}
