import { BookOpen, Database, ExternalLink, FolderOpen, Link as LinkIcon, ShieldCheck } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";

interface ConsolidatedResourceLink {
  readonly description: string;
  readonly href: string;
  readonly label: string;
  readonly icon: typeof FolderOpen;
}

const RESOURCE_LINKS: readonly ConsolidatedResourceLink[] = Object.freeze([
  Object.freeze({
    label: "Files",
    href: "/files",
    description: "Workspace file browsing remains handled by the existing Hermes Files surface.",
    icon: FolderOpen,
  }),
  Object.freeze({
    label: "Models",
    href: "/models",
    description: "Configured model/provider resource visibility remains read through the existing Models surface.",
    icon: Database,
  }),
  Object.freeze({
    label: "Documentation",
    href: "/docs",
    description: "Operator documentation continues to live behind the existing Documentation route.",
    icon: BookOpen,
  }),
]);

function OpenResourceLink({ item }: { readonly item: ConsolidatedResourceLink }) {
  const Icon = item.icon;

  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="flex h-full flex-col gap-4 p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Icon className="h-5 w-5 text-[var(--agent-platform-text-muted)]" aria-hidden="true" />
              <h2 className="text-lg font-semibold text-[var(--agent-platform-text-primary)]">{item.label}</h2>
            </div>
            <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">{item.description}</p>
          </div>
          <LinkIcon className="mt-1 h-5 w-5 flex-none text-[var(--agent-platform-text-muted)]" aria-hidden="true" />
        </div>
        <div className="mt-auto">
          <a
            className="inline-flex items-center gap-2 rounded-md border border-[var(--agent-platform-border-strong)] px-3 py-2 text-sm font-medium text-[var(--agent-platform-text-primary)] hover:bg-[var(--agent-platform-surface-elevated)]"
            href={item.href}
          >
            <ExternalLink className="h-4 w-4" aria-hidden="true" />
            Open {item.label}
          </a>
        </div>
      </CardContent>
    </Card>
  );
}

export function ResourcesPage() {
  return (
    <div
      className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]"
      style={{ fontFamily: "var(--agent-platform-font-body)" }}
    >
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8" aria-labelledby="resources-title">
        <header className="flex flex-col gap-5 border-b border-[var(--agent-platform-border-default)] pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div className="space-y-2">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--agent-platform-text-muted)]">
              Pepper / Resources
            </p>
            <h1
              id="resources-title"
              className="text-3xl font-semibold tracking-tight sm:text-4xl"
              style={{ fontFamily: "var(--agent-platform-font-display)" }}
            >
              Resources
            </h1>
            <p className="max-w-2xl text-sm leading-relaxed text-[var(--agent-platform-text-secondary)] sm:text-base">
              Read-through entry point for existing file, model, and documentation resource surfaces.
            </p>
          </div>
          <Badge tone="secondary">Navigation-only</Badge>
        </header>

        <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-elevated)]">
          <CardContent className="flex flex-col gap-3 p-5 sm:p-6">
            <div className="flex items-center gap-2 text-[var(--agent-platform-text-secondary)]">
              <ShieldCheck className="h-4 w-4" aria-hidden="true" />
              <span className="font-mono text-xs uppercase tracking-[0.16em]">Authority boundary</span>
            </div>
            <p className="text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
              This page does not add provider, model, filesystem, credential, worker, Kanban, Docker, Graphify, Git, or execution authority. It only links to already-existing Hermes resource surfaces.
            </p>
          </CardContent>
        </Card>

        <section className="grid gap-4 md:grid-cols-3" aria-label="Resources read-through links">
          {RESOURCE_LINKS.map((item) => <OpenResourceLink key={item.href} item={item} />)}
        </section>
      </div>
    </div>
  );
}
