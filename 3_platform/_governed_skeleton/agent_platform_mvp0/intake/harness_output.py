"""HarnessOutput intake metadata records for MVP-0.

HarnessOutputPackage is not trusted by default.
claims are not verified facts.
manual review required.
no auto-review.
no harness execution.
no validation execution.
no Git mutation.

This module accepts only caller-supplied metadata and user-pasted text. It does
not read files, inspect paths, execute commands, call harnesses, call providers,
call tools, call agents, run validation, persist records, or mutate Git.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class HarnessOutputIntakeStatus(Enum):
    """Metadata-only intake status for manually pasted harness output."""

    accepted_for_manual_review = "accepted_for_manual_review"
    blocked = "blocked"
    deferred = "deferred"
    rejected_for_scope = "rejected_for_scope"


class HarnessOutputTrustStatus(Enum):
    """External harness output is untrusted by default."""

    untrusted_by_default = "untrusted_by_default"
    claim_record_only = "claim_record_only"
    requires_manual_review = "requires_manual_review"
    requires_reviewer_verdict = "requires_reviewer_verdict"
    rejected = "rejected"


@dataclass(frozen=True)
class IntakeBlocker:
    """A metadata blocker that prevents automatic acceptance or integration."""

    blocker_id: str
    reason: str
    source_ref: str = "manual_intake"
    severity: str = "blocking"


@dataclass(frozen=True)
class IntakeLimitation:
    """A metadata limitation propagated into the intake decision."""

    limitation_id: str
    description: str
    impact: str = "requires_manual_review"


@dataclass(frozen=True)
class ManualReviewRequirement:
    """Manual review required before any downstream use."""

    requirement_id: str = "manual_review_required"
    required_actor: str = "human_or_manual_reviewer"
    reason: str = "manual review required"
    status: str = "required"


@dataclass(frozen=True)
class HarnessOutputSource:
    """Path-free, content-free source classification for pasted output."""

    source_id: str
    harness_name: str
    source_classification: str = "external_harness_output_claim"
    operator_classification: str = "user_operated"
    trust_status: HarnessOutputTrustStatus = HarnessOutputTrustStatus.untrusted_by_default
    sensitivity: str = "unknown_user_supplied_text"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class HarnessOutputClaim:
    """A supplied claim; claims are not verified facts."""

    claim_id: str
    claim_text: str
    claim_source: str = "user_pasted_output"
    claim_status: str = "claim_record_only"
    trust_status: HarnessOutputTrustStatus = HarnessOutputTrustStatus.claim_record_only
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class HarnessCommandClaim:
    """A claimed command record; command claims are not command execution."""

    claim_id: str
    command_text: str
    claimed_result: str = "claimed_not_verified"
    execution_status: str = "not_executed_by_AGENT_PLATFORM"
    trust_status: HarnessOutputTrustStatus = HarnessOutputTrustStatus.claim_record_only
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class HarnessValidationClaim:
    """A claimed validation/test record; no validation execution occurs."""

    claim_id: str
    validation_name: str
    claimed_result: str = "claimed_not_verified"
    validation_status: str = "not_executed_by_AGENT_PLATFORM"
    trust_status: HarnessOutputTrustStatus = HarnessOutputTrustStatus.claim_record_only
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class HarnessFileChangeClaim:
    """A claimed file-change record; no filesystem verification occurs."""

    claim_id: str
    path_claim: str
    change_summary: str
    claimed_status: str = "claimed_not_verified"
    filesystem_verification_status: str = "not_verified_no_filesystem_inspection"
    trust_status: HarnessOutputTrustStatus = HarnessOutputTrustStatus.claim_record_only
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class HarnessOutputIntakeRequest:
    """Manual pasted output intake request.

    The request carries only supplied metadata and pasted text. It is not a
    harness call, adapter call, provider call, tool call, or validation call.
    """

    request_id: str
    source: HarnessOutputSource
    pasted_output_text: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    claims: Sequence[HarnessOutputClaim] = field(default_factory=tuple)
    command_claims: Sequence[HarnessCommandClaim] = field(default_factory=tuple)
    validation_claims: Sequence[HarnessValidationClaim] = field(default_factory=tuple)
    file_change_claims: Sequence[HarnessFileChangeClaim] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    retention_refs: Sequence[str] = field(default_factory=tuple)
    rollback_refs: Sequence[str] = field(default_factory=tuple)
    incident_refs: Sequence[str] = field(default_factory=tuple)
    publication_blockers: Sequence[str] = field(default_factory=tuple)
    source_tracking_blockers: Sequence[str] = field(default_factory=tuple)
    generated_output_blockers: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[IntakeBlocker] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)
    suspected_sensitive_material: bool = False


@dataclass(frozen=True)
class HarnessOutputPackage:
    """Structured HarnessOutputPackage candidate for manual review only."""

    package_id: str
    request_id: str
    source: HarnessOutputSource
    pasted_output_text: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    claims: Sequence[HarnessOutputClaim] = field(default_factory=tuple)
    command_claims: Sequence[HarnessCommandClaim] = field(default_factory=tuple)
    validation_claims: Sequence[HarnessValidationClaim] = field(default_factory=tuple)
    file_change_claims: Sequence[HarnessFileChangeClaim] = field(default_factory=tuple)
    trust_status: HarnessOutputTrustStatus = HarnessOutputTrustStatus.untrusted_by_default
    manual_review_requirement: ManualReviewRequirement = field(default_factory=ManualReviewRequirement)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    retention_refs: Sequence[str] = field(default_factory=tuple)
    rollback_refs: Sequence[str] = field(default_factory=tuple)
    incident_refs: Sequence[str] = field(default_factory=tuple)
    publication_blockers: Sequence[str] = field(default_factory=tuple)
    source_tracking_blockers: Sequence[str] = field(default_factory=tuple)
    generated_output_blockers: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[IntakeBlocker] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class HarnessOutputIntakeDecision:
    """Decision wrapper for metadata-only intake construction."""

    decision_id: str
    request_id: str
    status: HarnessOutputIntakeStatus
    trust_status: HarnessOutputTrustStatus
    package: HarnessOutputPackage
    manual_review_requirement: ManualReviewRequirement
    blockers: Sequence[IntakeBlocker] = field(default_factory=tuple)
    limitations: Sequence[IntakeLimitation] = field(default_factory=tuple)
    decision_notes: Sequence[str] = field(default_factory=tuple)


def build_harness_output_package(
    request: HarnessOutputIntakeRequest,
) -> HarnessOutputIntakeDecision:
    """Build a HarnessOutputPackage from supplied metadata and pasted text only.

    This function records claims without verification. It does not execute
    commands, run tests, run validation, inspect claimed files, or mutate Git.
    """

    default_limitations = (
        IntakeLimitation(
            limitation_id="claims_are_not_verified_facts",
            description="claims are not verified facts",
        ),
        IntakeLimitation(
            limitation_id="command_claims_are_not_execution",
            description="command claims are not command execution",
        ),
        IntakeLimitation(
            limitation_id="validation_claims_are_not_validation_execution",
            description="validation/test claims are not validation execution",
        ),
        IntakeLimitation(
            limitation_id="file_claims_are_not_filesystem_verification",
            description="file-change claims are not filesystem verification",
        ),
    )
    blockers = tuple(request.blockers)

    if not request.pasted_output_text:
        blockers = blockers + (
            IntakeBlocker(
                blocker_id="missing_manual_pasted_output",
                reason="manual pasted output is required for intake",
            ),
        )

    if request.suspected_sensitive_material:
        blockers = blockers + (
            IntakeBlocker(
                blocker_id="suspected_sensitive_material",
                reason="suspected secret or credential material requires safe metadata reporting only",
            ),
        )

    limitations = default_limitations + tuple(request.limitations)
    manual_review = ManualReviewRequirement()
    status = (
        HarnessOutputIntakeStatus.blocked
        if blockers
        else HarnessOutputIntakeStatus.accepted_for_manual_review
    )
    package = HarnessOutputPackage(
        package_id=f"{request.request_id}:harness_output_package",
        request_id=request.request_id,
        source=request.source,
        pasted_output_text=request.pasted_output_text,
        metadata=request.metadata,
        claims=tuple(request.claims),
        command_claims=tuple(request.command_claims),
        validation_claims=tuple(request.validation_claims),
        file_change_claims=tuple(request.file_change_claims),
        trust_status=HarnessOutputTrustStatus.untrusted_by_default,
        manual_review_requirement=manual_review,
        evidence_refs=tuple(request.evidence_refs),
        validation_refs=tuple(request.validation_refs),
        security_refs=tuple(request.security_refs),
        retention_refs=tuple(request.retention_refs),
        rollback_refs=tuple(request.rollback_refs),
        incident_refs=tuple(request.incident_refs),
        publication_blockers=tuple(request.publication_blockers),
        source_tracking_blockers=tuple(request.source_tracking_blockers),
        generated_output_blockers=tuple(request.generated_output_blockers),
        blockers=blockers,
        limitations=limitations,
    )
    return HarnessOutputIntakeDecision(
        decision_id=f"{request.request_id}:intake_decision",
        request_id=request.request_id,
        status=status,
        trust_status=HarnessOutputTrustStatus.untrusted_by_default,
        package=package,
        manual_review_requirement=manual_review,
        blockers=blockers,
        limitations=limitations,
        decision_notes=(
            "HarnessOutputPackage is not trusted by default",
            "claims are not verified facts",
            "manual review required",
            "no harness execution",
            "no validation execution",
            "no Git mutation",
        ),
    )
