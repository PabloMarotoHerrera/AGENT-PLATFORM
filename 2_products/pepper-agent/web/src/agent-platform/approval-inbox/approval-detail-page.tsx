import type { ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, FileCheck2, History, ShieldCheck, Target } from "lucide-react";
import { Badge } from "@nous-research/ui/ui/components/badge";
import { Card, CardContent } from "@nous-research/ui/ui/components/card";

import { buildApprovalInboxPath, type ApprovalInboxLoader } from "./approval-client";
import type { ApprovalSectionState } from "./contract";
import {
  ApprovalAuthorityNote,
  ApprovalBlockingState,
  ApprovalStaleNotice,
  ApprovalWorkspaceHeader,
  type ApprovalWorkspaceViewProps,
} from "./approval-inbox-page";
import { useApprovalInbox } from "./use-approval-inbox";

function formatApprovalTimestamp(value: number | null): string {
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
  readonly icon: typeof FileCheck2;
  readonly section: ApprovalSectionState<T>;
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

export function ApprovalDetailView({ state, profile, refresh }: ApprovalWorkspaceViewProps) {
  const approval = state.snapshot?.kind === "detail" ? state.snapshot.approval : null;
  const inboxPath = buildApprovalInboxPath(profile) ?? "/agent-platform/approvals";
  return (
    <div className="h-full overflow-y-auto bg-[var(--agent-platform-surface-canvas)] text-[var(--agent-platform-text-primary)]" style={{ fontFamily: "var(--agent-platform-font-body)" }}>
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <Link className="inline-flex w-fit items-center gap-2 text-sm text-[var(--agent-platform-text-secondary)] hover:text-[var(--agent-platform-text-primary)]" to={inboxPath}>
          <ArrowLeft className="h-4 w-4" /> Approval Inbox
        </Link>
        <ApprovalWorkspaceHeader
          eyebrow="AGENT PLATFORM / Approval presentation"
          title={approval?.title ?? "Approval presentation"}
          description={approval ? `Source-local approval ID ${approval.sourceLocalApprovalId}` : "Loading one exact provisional source identity."}
          state={state}
          profile={profile}
          refresh={refresh}
        >
          {approval && (
            <div className="flex flex-wrap gap-2">
              <Badge tone="warning">Provisional source</Badge>
              <Badge tone="secondary">Source status: {approval.originalSourceStatus}</Badge>
              <span className="break-all font-mono text-xs text-[var(--agent-platform-text-muted)]">Source-local ID: {approval.sourceLocalApprovalId}</span>
            </div>
          )}
        </ApprovalWorkspaceHeader>
        <ApprovalStaleNotice state={state} />
        <ApprovalBlockingState state={state} refresh={refresh} unavailableLabel="Selected approval presentation unavailable" />

        {approval && (
          <>
            <ApprovalAuthorityNote />
            <section className="grid gap-4 lg:grid-cols-[1.5fr_1fr]" aria-label="Approval source summary">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-4 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><FileCheck2 className="h-4 w-4" /> Safe summary</h2>
                  <p className="whitespace-pre-wrap break-words text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">{approval.summary}</p>
                </CardContent>
              </Card>
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5 text-sm">
                  <h2 className="font-semibold">Source request metadata</h2>
                  <dl className="grid grid-cols-[max-content_1fr] gap-x-4 gap-y-2 text-[var(--agent-platform-text-secondary)]">
                    <dt>Source system</dt><dd>Hermes staged write approvals</dd>
                    <dt>Request type</dt><dd>{approval.originalSourceType}</dd>
                    <dt>Requester</dt><dd>{approval.sourceRequesterLabel ?? "not supplied"} <span className="text-xs text-[var(--agent-platform-text-muted)]">(not governed Agent identity)</span></dd>
                    <dt>Requested</dt><dd>{formatApprovalTimestamp(approval.requestedAt)}</dd>
                    <dt>Expires</dt><dd>{formatApprovalTimestamp(approval.expiresAt)}</dd>
                    <dt>Source risk</dt><dd>{approval.sourceRiskLabel ?? "not supplied"} <span className="text-xs text-[var(--agent-platform-text-muted)]">(not platform risk assessment)</span></dd>
                  </dl>
                </CardContent>
              </Card>
            </section>
            <section className="grid gap-4 lg:grid-cols-2" aria-label="Approval source detail">
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><Target className="h-4 w-4" /> Safe target metadata</h2>
                  <p className="text-sm text-[var(--agent-platform-text-secondary)]">{approval.target.sourceTargetLabel}</p>
                  <Badge tone="secondary">{approval.target.sourceTargetType}</Badge>
                </CardContent>
              </Card>
              <Card className="border-[var(--agent-platform-border-default)] bg-[var(--agent-platform-surface-panel)]">
                <CardContent className="space-y-3 p-5">
                  <h2 className="inline-flex items-center gap-2 font-semibold"><ShieldCheck className="h-4 w-4" /> Safe reason</h2>
                  <p className="whitespace-pre-wrap break-words text-sm text-[var(--agent-platform-text-secondary)]">{approval.sourceReason ?? "No safe source reason supplied."}</p>
                </CardContent>
              </Card>
              <SectionCard title="Evidence summaries" icon={FileCheck2} section={approval.evidence} emptyLabel="No safe source evidence summaries.">
                {(item) => (
                  <div key={item.sourceLocalEvidenceId} className="space-y-1 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <p className="break-words text-[var(--agent-platform-text-secondary)]">{item.sourceEvidenceLabel}</p>
                    <code className="break-all text-xs text-[var(--agent-platform-text-muted)]">Source evidence ID: {item.sourceLocalEvidenceId}</code>
                  </div>
                )}
              </SectionCard>
              <SectionCard title="Source decision history" icon={History} section={approval.decisionHistory} emptyLabel="No source decision history.">
                {(item) => (
                  <div key={item.sourceLocalDecisionId} className="grid grid-cols-[1fr_auto] gap-2 border-b border-[var(--agent-platform-border-default)] pb-2 text-sm">
                    <span>{item.sourceActorLabel ?? "Source actor not supplied"}</span><Badge tone="secondary">{item.originalSourceStatus}</Badge>
                    <time className="col-span-2 text-xs text-[var(--agent-platform-text-muted)]">{formatApprovalTimestamp(item.decidedAt)}</time>
                  </div>
                )}
              </SectionCard>
            </section>
            <Card className="border-[var(--agent-platform-border-strong)] bg-[var(--agent-platform-surface-subtle)]">
              <CardContent className="space-y-3 p-5 text-sm leading-relaxed text-[var(--agent-platform-text-secondary)]">
                <h2 className="font-semibold text-[var(--agent-platform-text-primary)]">Authority limitations</h2>
                <p>No approval or rejection action is available in P15.C3A.</p>
                <p>This presentation is not a canonical ApprovalRequest. The source requester is not a governed Agent, the source target is not a WorkPacket, source risk is not an AGENT PLATFORM assessment, evidence is not a canonical EvidenceRef, and history is not a canonical audit log.</p>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
}

export function ApprovalDetailPage({ loader }: { readonly loader?: ApprovalInboxLoader } = {}) {
  const { approvalId = "" } = useParams();
  const { profile, refresh, ...state } = useApprovalInbox({ kind: "detail", approvalId }, loader);
  return <ApprovalDetailView state={state} profile={profile} refresh={refresh} />;
}
