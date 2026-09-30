import { ExternalLink, Link as LinkIcon, ShieldCheck } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";

export type AutomationIntegrationsKind = "automation" | "integrations";

interface AutomationIntegrationsPageProps {
  readonly kind: AutomationIntegrationsKind;
}

interface ConsolidatedLink {
  readonly description: string;
  readonly href: string;
  readonly label: string;
}

const AUTOMATION_LINKS: readonly ConsolidatedLink[] = Object.freeze([
  Object.freeze({
    label: "Cron",
    href: "/cron",
    description: "Scheduled local automation jobs exposed by the existing Hermes Cron surface.",
  }),
  Object.freeze({
    label: "Webhooks",
    href: "/webhooks",
    description: "Existing webhook receivers and delivery settings without new execution authority.",
  }),
]);

const INTEGRATION_LINKS: readonly ConsolidatedLink[] = Object.freeze([
  Object.freeze({
    label: "Plugins",
    href: "/plugins",
    description: "Installed plugin manifests and plugin-provided UI surfaces remain managed by the existing Plugins route.",
  }),
  Object.freeze({
    label: "MCP",
    href: "/mcp",
    description: "Model Context Protocol configuration continues to live behind the existing MCP route.",
  }),
  Object.freeze({
    label: "Pairing",
    href: "/pairing",
    description: "Gateway pairing remains controlled by the existing pairing flow.",
  }),
  Object.freeze({
    label: "Channels",
    href: "/channels",
    description: "Gateway channel wiring remains controlled by the existing Channels route.",
  }),
]);

const PAGE_COPY: Record<AutomationIntegrationsKind, {
  readonly title: string;
  readonly summary: string;
  readonly links: readonly ConsolidatedLink[];
}> = Object.freeze({
  automation: Object.freeze({
    title: "Automation",
    summary: "Read-through entry point for existing scheduled jobs and webhook automation surfaces.",
    links: AUTOMATION_LINKS,
  }),
  integrations: Object.freeze({
    title: "Integrations",
    summary: "Read-through entry point for existing extension, MCP, pairing, channel, and plugin surfaces.",
    links: INTEGRATION_LINKS,
  }),
});

function OpenLink({ item }: { readonly item: ConsolidatedLink }) {
  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="flex h-full flex-col gap-4 p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-[var(--agent-platform-text-primary)]">{item.label}</h2>
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

export function AutomationIntegrationsView({ kind }: AutomationIntegrationsPageProps) {
  const page = PAGE_COPY[kind];

  return (
    <div
      className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]"
      style={{ fontFamily: "var(--agent-platform-font-body)" }}
    >
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8" aria-labelledby={`${kind}-title`}>
        <header className="flex flex-col gap-5 border-b border-[var(--agent-platform-border-default)] pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div className="space-y-2">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--agent-platform-text-muted)]">
              Pepper / {page.title}
            </p>
            <h1
              id={`${kind}-title`}
              className="text-3xl font-semibold tracking-tight sm:text-4xl"
              style={{ fontFamily: "var(--agent-platform-font-display)" }}
            >
              {page.title}
            </h1>
            <p className="max-w-2xl text-sm leading-relaxed text-[var(--agent-platform-text-secondary)] sm:text-base">
              {page.summary}
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
              This page does not add worker, Kanban, provider, model, Docker, Graphify, Git, credential, or execution authority. It only links to already-existing Hermes surfaces.
            </p>
          </CardContent>
        </Card>

        <section className="grid gap-4 md:grid-cols-2" aria-label={`${page.title} read-through links`}>
          {page.links.map((item) => <OpenLink key={item.href} item={item} />)}
        </section>
      </div>
    </div>
  );
}

export function AutomationPage() {
  return <AutomationIntegrationsView kind="automation" />;
}

export function IntegrationsPage() {
  return <AutomationIntegrationsView kind="integrations" />;
}
