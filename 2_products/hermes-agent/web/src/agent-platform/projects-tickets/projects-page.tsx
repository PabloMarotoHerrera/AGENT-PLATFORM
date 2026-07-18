import { useDeferredValue, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { ExternalLink, FolderKanban, RefreshCw, Search } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Button } from "@nous-research/ui/ui/components/button";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";
import { Input } from "@nous-research/ui/ui/components/input";
import { Spinner } from "@nous-research/ui/ui/components/spinner";

import {
  KANBAN_STATUSES,
  type ProjectsWorkspaceDataState,
} from "./contract";
import {
  buildKanbanSourcePath,
  buildProjectPath,
} from "./kanban-client";
import { useProjectsWorkspace } from "./use-projects-workspace";

export interface WorkspaceViewProps {
  readonly state: ProjectsWorkspaceDataState;
  readonly profile: string;
  readonly refresh: () => void;
}

function formatSourceTime(value: number | null): string {
  return value === null ? "No successful refresh" : new Date(value).toLocaleTimeString();
}

export function SourceAuthorityNote() {
  return (
    <aside className="border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-subtle)] p-4 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
      <strong className="text-[var(--agent-platform-text-primary)]">Authority boundary.</strong>{" "}
      This workspace wraps Hermes Kanban as a provisional source. Paperclip remains the future
      canonical work-control authority; these presentations do not create canonical Projects,
      Tickets, WorkPackets, approvals, or governed executions.
    </aside>
  );
}

export function WorkspaceHeader({
  eyebrow,
  title,
  description,
  state,
  profile,
  refresh,
  children,
}: WorkspaceViewProps & {
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
          <h1 className="break-words text-3xl font-semibold tracking-tight sm:text-4xl" style={{ fontFamily: "var(--agent-platform-font-display)" }}>
            {title}
          </h1>
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
        <Badge tone="secondary">Source: Hermes Kanban</Badge>
        <Badge tone="warning">Authority: Provisional</Badge>
        <Badge tone={tone}>{state.phase}</Badge>
        <span className="font-mono text-[var(--agent-platform-text-muted)]">Profile: {profile}</span>
        <span className="font-mono text-[var(--agent-platform-text-muted)]">Last success: {formatSourceTime(state.lastSuccessAt)}</span>
      </div>
      {children}
    </header>
  );
}

export function WorkspaceBlockingState({
  state,
  refresh,
  unavailableLabel,
}: Pick<WorkspaceViewProps, "state" | "refresh"> & { readonly unavailableLabel: string }) {
  if (state.snapshot || !["loading", "error", "unavailable"].includes(state.phase)) return null;
  const loading = state.phase === "loading";
  const title = loading
    ? "Loading Hermes Kanban source"
    : state.phase === "error"
      ? "Hermes Kanban could not be reached"
      : unavailableLabel;
  return (
    <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-panel)]" aria-busy={loading}>
      <CardContent className="flex min-h-64 flex-col items-center justify-center gap-4 p-8 text-center">
        {loading ? <Spinner className="h-5 w-5" /> : <FolderKanban className="h-8 w-8 text-[var(--agent-platform-status-unavailable)]" />}
        <div className="max-w-lg space-y-2">
          <h2 className="text-xl font-semibold">{title}</h2>
          <p className="text-sm text-[var(--agent-platform-text-secondary)]">
            {loading
              ? "Waiting for a validated, source-qualified response."
              : "No alternate board, task, or process-current source will be used as a fallback."}
          </p>
        </div>
        {!loading && <Button outlined onClick={refresh}>Try again</Button>}
      </CardContent>
    </Card>
  );
}

export function WorkspaceStaleNotice({ state }: Pick<WorkspaceViewProps, "state">) {
  if (state.phase !== "stale" || !state.snapshot) return null;
  return (
    <div role="status" className="border border-[var(--agent-platform-status-warning)] bg-[var(--agent-platform-surface-subtle)] px-4 py-3 text-sm text-[var(--agent-platform-text-secondary)]">
      Refresh failed. Showing the last validated Hermes Kanban projection from {formatSourceTime(state.lastSuccessAt)}.
    </div>
  );
}

export function ProjectsView({ state, profile, refresh }: WorkspaceViewProps) {
  const [filter, setFilter] = useState("");
  const [status, setStatus] = useState("all");
  const deferredFilter = useDeferredValue(filter.trim().toLowerCase());
  const projects = state.snapshot?.kind === "projects" ? state.snapshot.projects : [];
  const visibleProjects = projects.filter((project) => {
    const matchesText = !deferredFilter || `${project.displayName} ${project.boardSlug} ${project.description ?? ""}`.toLowerCase().includes(deferredFilter);
    return matchesText && (status === "all" || (project.taskCounts[status] ?? 0) > 0);
  });

  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <WorkspaceHeader
          eyebrow="AGENT PLATFORM / Work source"
          title="Projects"
          description="Read-only project presentations projected from existing Hermes Kanban boards."
          state={state}
          profile={profile}
          refresh={refresh}
        />
        <WorkspaceStaleNotice state={state} />
        <WorkspaceBlockingState state={state} refresh={refresh} unavailableLabel="Projects source unavailable" />

        {state.snapshot?.kind === "projects" && (
          <>
            <SourceAuthorityNote />
            <section className="grid gap-3 sm:grid-cols-[minmax(0,1fr)_13rem]" aria-label="Project filters">
              <label className="relative block">
                <span className="sr-only">Filter projects</span>
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--agent-platform-text-muted)]" />
                <Input className="pl-9" value={filter} onChange={(event) => setFilter(event.target.value)} placeholder="Filter by name, slug, or description" />
              </label>
              <label className="flex items-center gap-2 border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)] px-3 focus-within:border-[var(--agent-platform-action-primary)] focus-within:ring-2 focus-within:ring-[var(--agent-platform-focus-ring)]">
                <span className="text-xs text-[var(--agent-platform-text-muted)]">Source state</span>
                <select className="min-w-0 flex-1 bg-transparent py-2 text-sm outline-none" value={status} onChange={(event) => setStatus(event.target.value)}>
                  <option value="all">All</option>
                  {KANBAN_STATUSES.map((value) => <option key={value} value={value}>{value}</option>)}
                </select>
              </label>
            </section>

            {projects.length === 0 ? (
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="py-12 text-center text-[var(--agent-platform-text-secondary)]">Hermes Kanban returned no boards.</CardContent>
              </Card>
            ) : visibleProjects.length === 0 ? (
              <p className="py-8 text-center text-sm text-[var(--agent-platform-text-secondary)]">No Projects match the local filters.</p>
            ) : (
              <section className="grid gap-4 md:grid-cols-2" aria-label="Projects">
                {visibleProjects.map((project) => {
                  const projectPath = buildProjectPath(project.boardSlug, profile) ?? "#";
                  const sourcePath = buildKanbanSourcePath(project.boardSlug, profile) ?? "#";
                  return (
                    <Card key={project.boardSlug} className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                      <CardContent className="flex h-full flex-col gap-5 p-5">
                        <div className="flex items-start justify-between gap-4">
                          <div className="min-w-0">
                            <h2 className="break-words text-xl font-semibold">{project.displayName}</h2>
                            <p className="mt-1 break-all font-mono text-xs text-[var(--agent-platform-text-muted)]">Board: {project.boardSlug}</p>
                          </div>
                          <Badge tone="warning">Provisional</Badge>
                        </div>
                        <p className="line-clamp-4 whitespace-pre-wrap text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                          {project.description || "No source description supplied."}
                        </p>
                        <div className="flex flex-wrap gap-2">
                          <Badge tone="secondary">{project.totalTaskCount} source tasks</Badge>
                          {KANBAN_STATUSES.filter((sourceStatus) => project.taskCounts[sourceStatus]).map((sourceStatus) => (
                            <span key={sourceStatus} className="font-mono text-xs text-[var(--agent-platform-text-muted)]">
                              {sourceStatus}: {project.taskCounts[sourceStatus]}
                            </span>
                          ))}
                        </div>
                        <div className="mt-auto flex flex-wrap items-center justify-between gap-3 border-t border-[var(--agent-platform-border-default)] pt-4">
                          <Link className="font-semibold text-[var(--agent-platform-action-primary)] underline-offset-4 hover:underline" to={projectPath}>View Project</Link>
                          <Link className="inline-flex items-center gap-1 text-xs text-[var(--agent-platform-text-muted)] hover:text-[var(--agent-platform-text-primary)]" to={sourcePath}>
                            Hermes Kanban <ExternalLink className="h-3 w-3" />
                          </Link>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </section>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export function ProjectsPage() {
  const { profile, refresh, ...state } = useProjectsWorkspace({ kind: "projects" });
  return <ProjectsView state={state} profile={profile} refresh={refresh} />;
}
