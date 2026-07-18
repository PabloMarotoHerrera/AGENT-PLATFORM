import type { ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  CalendarClock,
  FileText,
  GitBranch,
  MessageSquareText,
  Paperclip,
  ScrollText,
  Stethoscope,
} from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";

import type { WorkspaceSection as WorkspaceSectionModel } from "./contract";
import {
  buildProjectPath,
  buildTicketPath,
} from "./kanban-client";
import {
  SourceAuthorityNote,
  WorkspaceBlockingState,
  WorkspaceHeader,
  WorkspaceStaleNotice,
  type WorkspaceViewProps,
} from "./projects-page";
import { useProjectsWorkspace } from "./use-projects-workspace";

function formatTimestamp(value: number | null): string {
  return value === null ? "not supplied" : new Date(value * 1000).toLocaleString();
}

function SectionCard<T>({
  title,
  icon: Icon,
  section,
  emptyLabel,
  children,
}: {
  readonly title: string;
  readonly icon: typeof FileText;
  readonly section: WorkspaceSectionModel<T>;
  readonly emptyLabel: string;
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
          <p className="text-sm text-[var(--agent-platform-text-secondary)]">This optional source section cannot be projected safely.</p>
        ) : section.items.length === 0 ? (
          <p className="text-sm text-[var(--agent-platform-text-secondary)]">{emptyLabel}</p>
        ) : (
          <div className="space-y-3">{section.items.map(children)}</div>
        )}
      </CardContent>
    </Card>
  );
}

export function TicketDetailView({ state, profile, refresh }: WorkspaceViewProps) {
  const ticket = state.snapshot?.kind === "ticket" ? state.snapshot.ticket : null;
  const projectPath = ticket ? buildProjectPath(ticket.boardSlug, profile) : null;

  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        {projectPath && (
          <Link className="inline-flex w-fit items-center gap-2 text-sm text-[var(--agent-platform-text-secondary)] hover:text-[var(--agent-platform-text-primary)]" to={projectPath}>
            <ArrowLeft className="h-4 w-4" /> Project {ticket?.boardSlug}
          </Link>
        )}
        <WorkspaceHeader
          eyebrow="AGENT PLATFORM / Ticket presentation"
          title={ticket?.title ?? "Ticket"}
          description={ticket ? `Hermes task ${ticket.taskId} from board ${ticket.boardSlug}` : "Loading one exact board-qualified Hermes task identity."}
          state={state}
          profile={profile}
          refresh={refresh}
        >
          {ticket && (
            <div className="flex flex-wrap gap-2">
              <Badge tone="warning">Provisional source</Badge>
              <Badge tone="secondary">Hermes status: {ticket.originalSourceStatus}</Badge>
              <span className="break-all font-mono text-xs text-[var(--agent-platform-text-muted)]">Board: {ticket.boardSlug} / Task: {ticket.taskId}</span>
            </div>
          )}
        </WorkspaceHeader>
        <WorkspaceStaleNotice state={state} />
        <WorkspaceBlockingState state={state} refresh={refresh} unavailableLabel="Selected board-qualified Ticket unavailable" />

        {ticket && (
          <>
            <SourceAuthorityNote />

            <section className="grid gap-4 lg:grid-cols-[1.5fr_1fr]" aria-label="Ticket source content">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-4 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><FileText className="h-4 w-4" /> Description</h2>
                  <p className="whitespace-pre-wrap break-words text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                    {ticket.body || "No source description supplied."}
                  </p>
                </CardContent>
              </Card>
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5 text-sm">
                  <h2 className="font-semibold">Source metadata</h2>
                  <dl className="grid grid-cols-[max-content_1fr] gap-x-4 gap-y-2 text-[var(--agent-platform-text-secondary)]">
                    <dt>Hermes priority</dt><dd className="font-mono">{ticket.sourcePriority}</dd>
                    <dt>Profile assignee</dt><dd>{ticket.profileAssigneeLabel ?? "none"} <span className="text-xs text-[var(--agent-platform-text-muted)]">(not Agent authority)</span></dd>
                    <dt>Tenant label</dt><dd>{ticket.tenantLabel ?? "none"} <span className="text-xs text-[var(--agent-platform-text-muted)]">(not access control)</span></dd>
                    <dt>Created</dt><dd>{formatTimestamp(ticket.createdAt)}</dd>
                    <dt>Started</dt><dd>{formatTimestamp(ticket.startedAt)}</dd>
                    <dt>Completed</dt><dd>{formatTimestamp(ticket.completedAt)}</dd>
                  </dl>
                </CardContent>
              </Card>
            </section>

            <section className="grid gap-4 lg:grid-cols-2" aria-label="Ticket source details">
              <SectionCard title="Parent and dependencies" icon={GitBranch} section={ticket.dependencies} emptyLabel="No parent or child source links.">
                {(dependency) => (
                  <Link
                    key={`${dependency.relation}:${dependency.taskId}`}
                    className="flex items-center justify-between gap-3 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm hover:text-[var(--agent-platform-action-primary)]"
                    to={buildTicketPath(dependency.boardSlug, dependency.taskId, profile) ?? "#"}
                  >
                    <span className="capitalize">{dependency.relation}</span>
                    <code className="break-all">{dependency.taskId}</code>
                  </Link>
                )}
              </SectionCard>

              <SectionCard title="Comments" icon={MessageSquareText} section={ticket.comments} emptyLabel="No source comments.">
                {(comment) => (
                  <article key={String(comment.sourceCommentId)} className="space-y-2 border-b border-[var(--agent-platform-border-default)] pb-3">
                    <div className="flex flex-wrap justify-between gap-2 text-xs text-[var(--agent-platform-text-muted)]">
                      <span>{comment.authorLabel}</span><time>{formatTimestamp(comment.createdAt)}</time>
                    </div>
                    <p className="whitespace-pre-wrap break-words text-sm text-[var(--agent-platform-text-secondary)]">{comment.body}</p>
                  </article>
                )}
              </SectionCard>

              <SectionCard title="Attachment metadata" icon={Paperclip} section={ticket.attachments} emptyLabel="No source attachment metadata.">
                {(attachment) => (
                  <div key={String(attachment.sourceAttachmentId)} className="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <span className="break-all">{attachment.displayFilename}</span>
                    <span className="font-mono text-xs text-[var(--agent-platform-text-muted)]">
                      {attachment.mediaType ?? "type unavailable"} / {attachment.sizeBytes === null ? "size unavailable" : `${attachment.sizeBytes} bytes`}
                    </span>
                  </div>
                )}
              </SectionCard>

              <SectionCard title="Events" icon={CalendarClock} section={ticket.events} emptyLabel="No source events.">
                {(event) => (
                  <div key={String(event.sourceEventId)} className="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <span>{event.label}</span><time className="text-xs text-[var(--agent-platform-text-muted)]">{formatTimestamp(event.createdAt)}</time>
                  </div>
                )}
              </SectionCard>

              <SectionCard title="Hermes run summaries" icon={ScrollText} section={ticket.runs} emptyLabel="No Hermes run summaries.">
                {(run) => (
                  <div key={String(run.sourceRunId)} className="grid grid-cols-[1fr_auto] gap-3 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <span>{run.sourceLabel} {String(run.sourceRunId)}</span>
                    <Badge tone="secondary">{run.sourceStatus}</Badge>
                    <span className="col-span-2 text-xs text-[var(--agent-platform-text-muted)]">{formatTimestamp(run.startedAt)} to {formatTimestamp(run.endedAt)}</span>
                  </div>
                )}
              </SectionCard>

              <SectionCard title="Diagnostics" icon={Stethoscope} section={ticket.diagnostics} emptyLabel="No safe source diagnostics.">
                {(diagnostic) => (
                  <div key={diagnostic.sourceKind} className="space-y-2 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <div className="flex items-center justify-between gap-3">
                      <code>{diagnostic.sourceKind}</code>
                      <Badge tone={diagnostic.severity === "warning" ? "warning" : "destructive"}>{diagnostic.severity}</Badge>
                    </div>
                    <p className="text-[var(--agent-platform-text-secondary)]">{diagnostic.message}</p>
                  </div>
                )}
              </SectionCard>
            </section>

            <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-subtle)]">
              <CardContent className="space-y-3 p-5 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                <h2 className="font-semibold text-[var(--agent-platform-text-primary)]">Authority limitations</h2>
                <p>Hermes Kanban Task is not a WorkPacket. Review and blocked are source states, not ApprovalRequests. Comments are discussion or evidence candidates only. Attachments are metadata only.</p>
                <p>Hermes runs are source-labelled summaries and are not governed execution records. Detailed execution evidence belongs to a later governed surface.</p>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
}

export function TicketDetailPage() {
  const { boardSlug = "", taskId = "" } = useParams();
  const { profile, refresh, ...state } = useProjectsWorkspace({ kind: "ticket", boardSlug, taskId });
  return <TicketDetailView state={state} profile={profile} refresh={refresh} />;
}
