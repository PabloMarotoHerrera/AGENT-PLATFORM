import {
  BookOpenCheck,
  Boxes,
  CircleOff,
  Languages,
  Palette,
  RefreshCw,
  Settings2,
  ShieldCheck,
  Type,
} from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Button } from "@nous-research/ui/ui/components/button";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";
import { Spinner } from "@nous-research/ui/ui/components/spinner";

import type {
  SafeFeatureState,
  SafePreferenceDescriptor,
} from "./contract";
import {
  useSafeSettings,
  type SafeSettingsState,
} from "./use-safe-settings";

interface SafeSettingsViewProps {
  readonly state: SafeSettingsState;
  readonly refresh: () => void;
}

const FEATURE_TONES: Record<SafeFeatureState["state"], "success" | "secondary" | "warning"> = {
  enabled: "success",
  disabled: "secondary",
  unavailable: "secondary",
  experimental: "warning",
};

function timeLabel(value: number | null): string {
  return value === null ? "Never" : new Date(value).toLocaleTimeString();
}

function phaseBadge(phase: SafeSettingsState["phase"]) {
  if (phase === "ready") return <Badge tone="success">Ready</Badge>;
  if (phase === "stale") return <Badge tone="warning">Stale</Badge>;
  if (phase === "error") return <Badge tone="destructive">Error</Badge>;
  if (phase === "not_configured") return <Badge tone="secondary">Not configured</Badge>;
  if (phase === "unavailable") return <Badge tone="secondary">Unavailable</Badge>;
  return <Badge tone="secondary">Loading</Badge>;
}

function Definition({ label, value }: { readonly label: string; readonly value: string | number }) {
  return (
    <div className="min-w-0 border-l-2 border-[var(--agent-platform-border-default)] pl-3">
      <dt className="text-[0.68rem] font-semibold uppercase tracking-[0.14em] text-[var(--agent-platform-text-muted)]">
        {label}
      </dt>
      <dd className="mt-1 break-words font-mono text-sm text-[var(--agent-platform-text-primary)]">
        {value}
      </dd>
    </div>
  );
}

function IdentityCard({
  eyebrow,
  title,
  values,
}: {
  readonly eyebrow: string;
  readonly title: string;
  readonly values: readonly { readonly label: string; readonly value: string }[];
}) {
  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="space-y-5 p-5 sm:p-6">
        <div>
          <p className="font-mono text-[0.68rem] uppercase tracking-[0.18em] text-[var(--agent-platform-text-muted)]">
            {eyebrow}
          </p>
          <h2 className="mt-2 text-xl font-semibold">{title}</h2>
        </div>
        <dl className="grid gap-4 sm:grid-cols-2">
          {values.map((value) => <Definition key={value.label} {...value} />)}
        </dl>
      </CardContent>
    </Card>
  );
}

function PreferenceCard({
  preference,
}: {
  readonly preference: SafePreferenceDescriptor;
}) {
  const icon = preference.id === "theme"
    ? Palette
    : preference.id === "font"
      ? Type
      : preference.id === "language"
        ? Languages
        : Settings2;
  const Icon = icon;
  return (
    <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
      <CardContent className="flex h-full flex-col gap-5 p-5 sm:p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <span className="mt-0.5 border border-[var(--agent-platform-border-default)] p-2 text-[var(--agent-platform-text-secondary)]">
              <Icon className="h-4 w-4" aria-hidden="true" />
            </span>
            <div>
              <h3 className="font-semibold">{preference.label}</h3>
              <p className="mt-1 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                {preference.description}
              </p>
            </div>
          </div>
          <Badge tone={preference.writeAvailable ? "success" : "secondary"}>
            {preference.classification === "unavailable" ? "Unavailable" : "Read only"}
          </Badge>
        </div>

        <div className="border-y border-[var(--agent-platform-border-default)] py-4">
          <p className="text-xs text-[var(--agent-platform-text-muted)]">Current trusted value</p>
          <p className="mt-1 font-mono text-sm">{preference.currentValueLabel}</p>
        </div>

        {preference.allowedValues.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[var(--agent-platform-text-secondary)]">
              Trusted catalog
            </p>
            <div className="flex flex-wrap gap-2">
              {preference.allowedValues.slice(0, 8).map((value) => (
                <Badge key={value.id} tone={value.id === preference.currentValueId ? "success" : "secondary"}>
                  {value.label}
                </Badge>
              ))}
              {preference.allowedValues.length > 8 && (
                <Badge tone="secondary">+{preference.allowedValues.length - 8} more</Badge>
              )}
            </div>
          </div>
        )}

        <dl className="grid gap-3 text-sm sm:grid-cols-3">
          <Definition label="Target" value={preference.targetScope} />
          <Definition label="Persistence" value={preference.persistenceAuthority} />
          <Definition label="Impact" value={preference.impact} />
        </dl>

        <div className="mt-auto space-y-2 text-xs text-[var(--agent-platform-text-muted)]">
          <p>Selected profile: <span className="text-[var(--agent-platform-text-secondary)]">{preference.selectedProfileContext}</span></p>
          <p>Last source write surfaced here: {timeLabel(preference.lastSuccessfulWriteAt)}</p>
          <p>This Pepper reconciliation candidate does not write display preferences.</p>
        </div>
      </CardContent>
    </Card>
  );
}

export function SafeSettingsView({ state, refresh }: SafeSettingsViewProps) {
  const snapshot = state.snapshot;

  return (
    <div
      className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]"
      style={{ fontFamily: "var(--agent-platform-font-body)" }}
    >
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-7 px-4 py-6 sm:px-6 sm:py-8 lg:px-8" aria-labelledby="safe-settings-title">
        <header className="grid gap-5 border-b border-[var(--agent-platform-border-default)] pb-6 lg:grid-cols-[1fr_auto] lg:items-end">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--agent-platform-text-muted)]">
              AGENT PLATFORM / Presentation boundary
            </p>
            <h1 id="safe-settings-title" className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl" style={{ fontFamily: "var(--agent-platform-font-display)" }}>
              Safe Settings
            </h1>
            <p className="mt-3 max-w-3xl text-sm leading-relaxed text-[var(--agent-platform-text-secondary)] sm:text-base">
              A strict projection of product identity, read-only feature posture, and proven display preferences. No raw configuration fallback exists.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
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

        <dl className="grid gap-3 border border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-subtle)] p-4 text-sm sm:grid-cols-3" aria-label="Safe source context">
          <Definition label="Selected profile context" value={snapshot?.selectedProfileContext ?? "Loading"} />
          <Definition label="Safe source" value={snapshot?.sourceLabel ?? "Awaiting validated source"} />
          <Definition label="Last successful refresh" value={timeLabel(state.lastSuccessAt)} />
        </dl>

        {state.phase === "loading" && snapshot === null && (
          <Card aria-busy="true" className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
            <CardContent className="flex min-h-64 items-center justify-center gap-3 p-8 text-[var(--agent-platform-text-secondary)]">
              <Spinner className="h-5 w-5" /> Loading the safe projection…
            </CardContent>
          </Card>
        )}

        {snapshot === null && state.phase !== "loading" && (
          <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-panel)]">
            <CardContent className="flex min-h-64 flex-col items-center justify-center gap-4 p-8 text-center">
              <CircleOff className="h-8 w-8 text-[var(--agent-platform-status-unavailable)]" aria-hidden="true" />
              <div className="max-w-lg">
                <h2 className="text-xl font-semibold">Safe settings source unavailable</h2>
                <p className="mt-2 text-sm text-[var(--agent-platform-text-secondary)]">
                  No raw Config, Keys, provider, plugin, MCP, or lifecycle surface is used as a fallback.
                </p>
              </div>
              <Button outlined onClick={refresh}>Try safe refresh</Button>
            </CardContent>
          </Card>
        )}

        {snapshot && (
          <>
            {state.phase === "stale" && (
              <div role="status" className="border border-[var(--agent-platform-status-warning)] bg-[var(--agent-platform-surface-subtle)] px-4 py-3 text-sm">
                Refresh failed. Showing the last validated safe projection.
              </div>
            )}

            <section className="grid gap-4 lg:grid-cols-2" aria-label="Product and upstream identity">
              <IdentityCard
                eyebrow="Product identity / read only"
                title={snapshot.product.displayName}
                values={[
                  { label: "Product ID", value: snapshot.product.id },
                  { label: "Product version", value: snapshot.product.version },
                ]}
              />
              <IdentityCard
                eyebrow="Upstream identity / read only"
                title={snapshot.upstream.displayName}
                values={[
                  { label: "Upstream version", value: snapshot.upstream.version },
                  { label: "Immutable commit", value: snapshot.upstream.commit.slice(0, 12) },
                ]}
              />
            </section>

            <section className="space-y-4" aria-labelledby="feature-states-title">
              <div className="flex items-center gap-3">
                <ShieldCheck className="h-5 w-5 text-[var(--agent-platform-status-success)]" aria-hidden="true" />
                <div>
                  <h2 id="feature-states-title" className="text-xl font-semibold">Feature states</h2>
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">Feature state authority is tracked product configuration and is read-only here.</p>
                </div>
              </div>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {snapshot.features.map((feature) => (
                  <Card key={feature.id} className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                    <CardContent className="space-y-3 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <code className="break-all text-xs">{feature.id}</code>
                        <Badge tone={FEATURE_TONES[feature.state]}>{feature.state}</Badge>
                      </div>
                      <p className="text-xs text-[var(--agent-platform-text-muted)]">{feature.sourceAuthority} · Read only</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </section>

            <section className="space-y-4" aria-labelledby="extension-posture-title">
              <div className="flex items-center gap-3">
                <Boxes className="h-5 w-5 text-[var(--agent-platform-text-secondary)]" aria-hidden="true" />
                <div>
                  <h2 id="extension-posture-title" className="text-xl font-semibold">Extension activation posture</h2>
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">
                    Feature and module activation is read-only in P15.C3A. A later governed activation task owns any tracked activation decision.
                  </p>
                </div>
              </div>
              <dl className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
                <Definition label="Compiled" value={snapshot.extensionPosture.compiledDescriptorCount} />
                <Definition label="Selected modules" value={snapshot.extensionPosture.selectedModuleCount} />
                <Definition label="Resolved" value={snapshot.extensionPosture.resolvedDescriptorCount} />
                <Definition label="Routes" value={snapshot.extensionPosture.registeredRouteCount} />
                <Definition label="Navigation" value={snapshot.extensionPosture.registeredNavigationCount} />
              </dl>
            </section>

            <section className="space-y-4" aria-labelledby="display-preferences-title">
              <div className="flex items-center gap-3">
                <BookOpenCheck className="h-5 w-5 text-[var(--agent-platform-text-secondary)]" aria-hidden="true" />
                <div>
                  <h2 id="display-preferences-title" className="text-xl font-semibold">Display preferences</h2>
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">Each displayed value is an exact member of an existing source-owned catalog, shown read-only in Pepper.</p>
                </div>
              </div>
              <div className="grid gap-4 lg:grid-cols-2">
                {snapshot.preferences.map((preference) => (
                  <PreferenceCard
                    key={preference.id}
                    preference={preference}
                  />
                ))}
              </div>
            </section>

            <section className="border border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-elevated)] p-5 sm:p-6" aria-labelledby="excluded-settings-title">
              <div className="flex items-start gap-3">
                <ShieldCheck className="mt-0.5 h-5 w-5 text-[var(--agent-platform-status-success)]" aria-hidden="true" />
                <div>
                  <h2 id="excluded-settings-title" className="text-xl font-semibold">Excluded settings boundary</h2>
                  <p className="mt-2 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                    No secrets are exposed. API keys, tokens, OAuth, providers, models, custom themes or CSS, URLs, paths, raw YAML, plugins, MCP, hooks, memory providers, gateway controls, workers, and agents are excluded. No raw configuration fallback exists.
                  </p>
                </div>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
}

export function SafeSettingsPage() {
  const { refresh, ...state } = useSafeSettings();
  return (
    <SafeSettingsView
      state={state}
      refresh={refresh}
    />
  );
}
