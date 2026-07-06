"""Manual review checklist metadata records for MVP-0.

HarnessOutputPackage is not trusted by default.
claims are not verified facts.
manual review required.
no auto-review.
no harness execution.
no validation execution.
no Git mutation.

This module renders checklist decisions as data only. It does not approve,
auto-review, execute commands, run validation, inspect files, persist records,
or mutate Git.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class ReviewChecklistItemStatus(Enum):
    """Manual checklist item status; no item is auto-reviewed."""

    not_reviewed = "not_reviewed"
    pass_claimed = "pass_claimed"
    fail_claimed = "fail_claimed"
    needs_manual_review = "needs_manual_review"
    blocked = "blocked"
    out_of_scope = "out_of_scope"


class DriftMarkerSeverity(Enum):
    """Metadata-only drift marker severity."""

    informational = "informational"
    minor = "minor"
    major = "major"
    blocking = "blocking"


@dataclass(frozen=True)
class ReviewChecklistItem:
    """A manual reviewer checklist prompt."""

    item_id: str
    prompt: str
    status: ReviewChecklistItemStatus = ReviewChecklistItemStatus.needs_manual_review
    required_actor: str = "human_or_manual_reviewer"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class ReviewChecklist:
    """Assisted manual review checklist; no auto-review."""

    checklist_id: str
    title: str = "HarnessOutput Intake / Review Checklist"
    items: Sequence[ReviewChecklistItem] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    retention_refs: Sequence[str] = field(default_factory=tuple)
    rollback_refs: Sequence[str] = field(default_factory=tuple)
    incident_refs: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ReviewFinding:
    """A supplied manual review finding candidate."""

    finding_id: str
    summary: str
    finding_status: str = "manual_review_required"
    severity: DriftMarkerSeverity = DriftMarkerSeverity.informational
    drift_candidate: bool = False
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class ReviewVerdictDraft:
    """Draft metadata only; not final approval."""

    verdict_id: str
    verdict_status: str = "manual_review_required"
    summary: str = "ReviewVerdictDraft is not final approval"
    required_actor: str = "human_or_manual_reviewer"
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class DriftMarker:
    """Metadata-only drift marker; not an integration decision."""

    drift_id: str
    source_area: str
    observed_issue: str
    expected_canonical_posture: str
    severity: DriftMarkerSeverity = DriftMarkerSeverity.informational
    status: str = "pending_P8.R_reconciliation"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class ReviewChecklistDecision:
    """Checklist rendering result as inert data."""

    decision_id: str
    package_id: str
    checklist: ReviewChecklist
    item_results: Sequence[ReviewChecklistItem] = field(default_factory=tuple)
    findings: Sequence[ReviewFinding] = field(default_factory=tuple)
    drift_markers: Sequence[DriftMarker] = field(default_factory=tuple)
    verdict_draft: ReviewVerdictDraft = field(
        default_factory=lambda: ReviewVerdictDraft(verdict_id="manual_review_required")
    )
    decision_status: str = "manual review required"
    decision_notes: Sequence[str] = field(default_factory=tuple)


def build_review_checklist(
    package: HarnessOutputPackage,
    checklist: ReviewChecklist,
) -> ReviewChecklistDecision:
    """Render a manual review checklist decision as data only.

    This function does not auto-review, approve, validate, inspect files, execute
    commands, execute harnesses, or mutate Git.
    """

    package_id = package.package_id
    findings = ()
    drift_markers = mark_drift(package, findings)
    return ReviewChecklistDecision(
        decision_id=f"{package_id}:review_checklist_decision",
        package_id=package_id,
        checklist=checklist,
        item_results=tuple(checklist.items),
        findings=findings,
        drift_markers=drift_markers,
        verdict_draft=ReviewVerdictDraft(
            verdict_id=f"{package_id}:review_verdict_draft",
            limitations=(
                "ReviewVerdictDraft is not final approval",
                "manual review required",
            ),
        ),
        decision_status="manual review required",
        decision_notes=(
            "ReviewChecklist is not auto-review",
            "manual review required",
            "no auto-review",
            "no validation execution",
            "no Git mutation",
        ),
    )


def mark_drift(
    package: HarnessOutputPackage,
    findings: Sequence[ReviewFinding],
) -> tuple[DriftMarker, ...]:
    """Create DriftMarker metadata from explicitly supplied findings only."""

    markers: list[DriftMarker] = []
    for finding in findings:
        if finding.drift_candidate:
            markers.append(
                DriftMarker(
                    drift_id=f"{package.package_id}:{finding.finding_id}:drift",
                    source_area="manual_review_finding",
                    observed_issue=finding.summary,
                    expected_canonical_posture="manual review required; no auto-review",
                    severity=finding.severity,
                    evidence_refs=tuple(finding.evidence_refs),
                    limitations=tuple(finding.limitations),
                )
            )
    return tuple(markers)
