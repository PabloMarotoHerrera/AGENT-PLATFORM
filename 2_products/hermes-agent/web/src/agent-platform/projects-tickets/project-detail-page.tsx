import { useDeferredValue, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, GitBranch, Search } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";
import { Input } from "@nous-research/ui/ui/components/input";

import {
  KANBAN_STATUSES,
  type KanbanSourceStatus,
} from "./contract";
import {
  buildProjectsPath,
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

const STATUS_SEMANTICS: Readonly<Partial<Record<KanbanSourceStatus, string>>> = Object.freeze({
  ready: "May be dispatcher-eligible in Hermes; it is not executable here.",
  running: "Hermes source state only; it is not governed WorkPacket execution.",
  review: "Hermes source state only; it is not an ApprovalRequest.",
  scheduled: "Waiting source state; no wake timestamp is inferred.",
  blocked: "Hermes source state; it is not a pending approval.",
});

function statusTone(status: KanbanSourceStatus): "success" | "warning" | "destructive" | "secondary" {
  if (status === "done") return "success";
  if (status === "blocked" || status === "review") return "warning";
  if (status === "running") return "destructive";
  return "secondary";
}

export function ProjectDetailView({ state, profile, refresh }: WorkspaceViewProps) {
  const [filter, setFilter] = useState("");
  const deferredFilter = useDeferredValue(filter.trim().toLowerCase());
  const project = state.snapshot?.kind === "project" ? state.snapshot.project : null;
  const visibleTickets = project?.tickets.filter((ticket) =>
    !deferredFilter || `${ticket.title} ${ticket.taskId} ${ticket.originalSourceStatus}`.toLowerCase().includes(deferredFilter)) ?? [];
  const projectsPath = buildProjectsPath(profile) ?? "/agent-platform/projects";

  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <main className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <Link className="inline-flex w-fit items-center gap-2 text-sm text-[var(--agent-platform-text-secondary)] hover:text-[var(--agent-platform-text-primary)]" to={projectsPath}>
          <ArrowLeft className="h-4 w-4" /> Projects
        </Link>
        <WorkspaceHeader
          eyebrow="AGENT PLATFORM / Project presentation"
          title={project?.displayName ?? "Project"}
          description={project ? `Hermes Kanban board ${project.boardSlug}` : "Loading one exact Hermes Kanban board identity."}
          state={state}
          profile={profile}
          refresh={refresh}
        >
          {project && <p className="break-all font-mono text-xs text-[var(--agent-platform-text-muted)]">Source board slug: {project.boardSlug}</p>}
        </WorkspaceHeader>
        <WorkspaceStaleNotice state={state} />
        <WorkspaceBlockingState state={state} refresh={refresh} unavailableLabel="Selected Hermes board unavailable" />

        {project && (
          <>
            <SourceAuthorityNote />
            <section className="grid gap-3 lg:grid-cols-[minmax(0,1fr)_2fr]" aria-label="Source status semantics">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5">
                  <p className="text-xs uppercase tracking-[0.16em] text-[var(--agent-platform-text-muted)]">Board source</p>
                  <p className="break-all font-mono text-sm">{project.boardSlug}</p>
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">{project.totalTaskCount} available source tasks</p>
                </CardContent>
              </Card>
              <div className="grid gap-2 sm:grid-cols-2">
                {Object.entries(STATUS_SEMANTICS).map(([status, description]) => (
                  <div key={status} className="border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-subtle)] p-3 text-xs leading-relaxed text-[var(--agent-platform-text-secondary)]">
                    <strong className="font-mono text-[var(--agent-platform-text-primary)]">{status}</strong>: {description}
                  </div>
                ))}
              </div>
            </section>

            <label className="relative block">
              <span className="sr-only">Filter tickets</span>
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--agent-platform-text-muted)]" />
              <Input className="pl-9" value={filter} onChange={(event) => setFilter(event.target.value)} placeholder="Filter by title, task ID, or source status" />
            </label>

            {project.tickets.length === 0 ? (
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="py-12 text-center text-[var(--agent-platform-text-secondary)]">This Hermes board contains no source tasks.</CardContent>
              </Card>
            ) : visibleTickets.length === 0 ? (
              <p className="py-8 text-center text-sm text-[var(--agent-platform-text-secondary)]">No Tickets match the local filter.</p>
            ) : (
              <section className="space-y-6" aria-label="Board-qualified tickets">
                {KANBAN_STATUSES.map((status) => {
                  const tickets = visibleTickets.filter((ticket) => ticket.visualStatus === status);
                  if (!tickets.length) return null;
                  return (
                    <div key={status} className="space-y-3">
                      <div className="flex items-center gap-3">
                        <h2 className="font-mono text-sm uppercase tracking-[0.16em]">Hermes status: {status}</h2>
                        <Badge tone="secondary">{tickets.length}</Badge>
                      </div>
                      <div className="grid gap-3 lg:grid-cols-2">
                        {tickets.map((ticket) => (
                          <Card key={`${ticket.boardSlug}:${ticket.taskId}`} className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                            <CardContent className="flex h-full flex-col gap-4 p-5">
                              <div className="flex items-start justify-between gap-3">
                                <div className="min-w-0">
                                  <h3 className="break-words font-semibold">{ticket.title}</h3>
                                  <p className="mt-1 break-all font-mono text-xs text-[var(--agent-platform-text-muted)]">Task: {ticket.taskId}</p>
                                </div>
                                <Badge tone={statusTone(ticket.visualStatus)}>{ticket.originalSourceStatus}</Badge>
                              </div>
                              <div className="flex flex-wrap gap-x-4 gap-y-2 text-xs text-[var(--agent-platform-text-secondary)]">
                                <span>Hermes priority: {ticket.sourcePriority}</span>
                                <span>Profile assignee: {ticket.profileAssigneeLabel ?? "none"}</span>
                                <span>Tenant label: {ticket.tenantLabel ?? "none"}</span>
                              </div>
                              {(ticket.parentCount > 0 || ticket.childCount > 0) && (
                                <p className="inline-flex items-center gap-2 text-xs text-[var(--agent-platform-text-muted)]">
                                  <GitBranch className="h-4 w-4" /> {ticket.parentCount} parent / {ticket.childCount} child source links
                                </p>
                              )}
                              {STATUS_SEMANTICS[ticket.visualStatus] && (
                                <p className="text-xs leading-relaxed text-[var(--agent-platform-text-muted)]">{STATUS_SEMANTICS[ticket.visualStatus]}</p>
                              )}
                              <Link className="mt-auto w-fit font-semibold text-[var(--agent-platform-action-primary)] underline-offset-4 hover:underline" to={buildTicketPath(ticket.boardSlug, ticket.taskId, profile) ?? "#"}>
                                View Ticket
                              </Link>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export function ProjectDetailPage() {
  const { boardSlug = "" } = useParams();
  const { profile, refresh, ...state } = useProjectsWorkspace({ kind: "project", boardSlug });
  return <ProjectDetailView state={state} profile={profile} refresh={refresh} />;
}
