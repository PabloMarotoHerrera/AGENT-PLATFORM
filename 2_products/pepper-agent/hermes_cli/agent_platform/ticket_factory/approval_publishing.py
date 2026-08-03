"""Explicit human-gated approval and logical canonical publication evidence."""

from __future__ import annotations

from enum import Enum
import hashlib
import json
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory.dependency_planning import (
    TicketDependencyPlan,
    TicketPlanningRequest,
    WaveDisposition,
    build_ticket_dependency_plan,
)
from hermes_cli.agent_platform.ticket_factory.proposal_synthesis import (
    ProposalConflict,
    ProposalConflictSeverity,
    SynthesizedTicketCandidate,
    TicketSynthesisReview,
)
from hermes_cli.agent_platform.ticket_factory.specs import (
    ProjectIdentifier,
    ProjectSpec,
    TicketIdentifier,
    TicketSpec,
)
from hermes_cli.agent_platform.ticket_factory.ticket_policy import (
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    lint_ticket_collection,
)

HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION = 1
APPROVAL_INPUT_DIGEST_ALGORITHM = "agent-platform-ticket-approval-input-sha256-v1"
APPROVAL_RECORD_DIGEST_ALGORITHM = "agent-platform-ticket-approval-record-sha256-v1"
CANONICAL_TICKET_DIGEST_ALGORITHM = "agent-platform-canonical-ticket-sha256-v1"
PUBLISHED_TICKET_ARTIFACT_DIGEST_ALGORITHM = (
    "agent-platform-published-ticket-artifact-sha256-v1"
)
TICKET_SUPERSESSION_DIGEST_ALGORITHM = "agent-platform-ticket-supersession-sha256-v1"
PUBLICATION_INPUT_DIGEST_ALGORITHM = "agent-platform-ticket-publication-input-sha256-v1"
PUBLICATION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-ticket-publication-result-sha256-v1"
)


class TicketApprovalPublishingError(ValueError):
    """Base error for human approval and publication failures."""


class TicketApprovalInputError(TicketApprovalPublishingError):
    """Raised when approval input identities or decision shapes are inconsistent."""


class TicketApprovalValidationError(TicketApprovalPublishingError):
    """Raised when supplied review, lint or planning evidence is invalid."""


class TicketPublicationAuthorizationError(TicketApprovalPublishingError):
    """Raised when a record does not authorize logical publication."""


class HumanApprovalDecision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"


class ConflictResolutionAction(str, Enum):
    ACKNOWLEDGE = "acknowledge"
    ACCEPT_CANDIDATE = "accept_candidate"
    RESOLVE_WITH_MANUAL_REPLACEMENT = "resolve_with_manual_replacement"
    REJECT = "reject"


class TicketApprovalState(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_REQUIRED = "revision_required"


class CanonicalTicketSource(str, Enum):
    SYNTHESIZED_CANDIDATE = "synthesized_candidate"
    MANUAL_REPLACEMENT = "manual_replacement"


class TicketPublicationState(str, Enum):
    PUBLISHED = "published"
    SUPERSEDED = "superseded"


class TicketPublicationFormat(str, Enum):
    CANONICAL_JSON_V1 = "canonical_json_v1"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
CanonicalTicketJSON: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=1, max_length=65536),
    AfterValidator(_reject_nul),
]
HumanIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=3,
        max_length=96,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$",
    ),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]
ConflictIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=13, max_length=20, pattern=r"^CONFLICT-[0-9]{4,10}$"),
]
PublicationIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=13,
        max_length=80,
        pattern=r"^PUB-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-[0-9]{4}$",
    ),
]


class _ApprovalPublishingModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


class HumanApprovalEvidence(_ApprovalPublishingModel):
    reviewer_id: HumanIdentifier
    decision_reference: BoundedText
    rationale: BoundedText
    policy_warning_acknowledgement: BoundedText | None = None
    planning_warning_acknowledgement: BoundedText | None = None


class HumanConflictResolution(_ApprovalPublishingModel):
    conflict_id: ConflictIdentifier
    action: ConflictResolutionAction
    rationale: BoundedText
    evidence_reference: BoundedText | None = None


class ManualTicketReplacement(_ApprovalPublishingModel):
    replacement_ticket: TicketSpec
    rationale: BoundedText
    evidence_references: tuple[BoundedText, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_replacement(self) -> ManualTicketReplacement:
        _reject_duplicate_values(self.evidence_references, "evidence_references")
        return self


class FreshDependencyPlanningEvidence(_ApprovalPublishingModel):
    planning_request: TicketPlanningRequest
    dependency_plan: TicketDependencyPlan
    evidence_reference: BoundedText
    rationale: BoundedText

    @model_validator(mode="after")
    def _validate_planning_evidence(self) -> FreshDependencyPlanningEvidence:
        _validate_planning_evidence_recomputes(self, error_type=ValueError)
        return self


class TicketApprovalRequest(_ApprovalPublishingModel):
    project_spec: ProjectSpec
    seed_ticket: TicketSpec
    synthesis_review: TicketSynthesisReview
    decision: HumanApprovalDecision
    conflict_resolutions: tuple[HumanConflictResolution, ...] = ()
    approval_evidence: HumanApprovalEvidence
    manual_replacement: ManualTicketReplacement | None = None
    fresh_planning_evidence: FreshDependencyPlanningEvidence | None = None


class TicketApprovalRecord(_ApprovalPublishingModel):
    # TicketApprovalRecord is explicit human decision evidence, not execution authority.
    schema_version: Literal[1] = HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    synthesis_review_SHA256: DigestText
    decision: HumanApprovalDecision
    state: TicketApprovalState
    canonical_source: CanonicalTicketSource | None
    approved_ticket: TicketSpec | None
    approval_evidence: HumanApprovalEvidence
    conflict_resolutions: tuple[HumanConflictResolution, ...]
    approved_ticket_lint_report: TicketLintReport | None
    fresh_planning_evidence: FreshDependencyPlanningEvidence | None
    approval_input_SHA256: DigestText
    approval_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_record(self) -> TicketApprovalRecord:
        _validate_approval_record_state(self, error_type=ValueError)
        expected = _approval_record_digest(
            schema_version=self.schema_version,
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            synthesis_review_SHA256=self.synthesis_review_SHA256,
            decision=self.decision,
            state=self.state,
            canonical_source=self.canonical_source,
            approved_ticket=self.approved_ticket,
            approval_evidence=self.approval_evidence,
            conflict_resolutions=self.conflict_resolutions,
            approved_ticket_lint_report=self.approved_ticket_lint_report,
            fresh_planning_evidence=self.fresh_planning_evidence,
            approval_input_SHA256=self.approval_input_SHA256,
        )
        if self.approval_SHA256 != expected:
            raise ValueError("approval_SHA256 must match approval record digest")
        return self


class TicketPublicationEvidence(_ApprovalPublishingModel):
    publisher_id: HumanIdentifier
    publication_reference: BoundedText
    rationale: BoundedText


class TicketPublicationRequest(_ApprovalPublishingModel):
    approval_record: TicketApprovalRecord
    publication_evidence: TicketPublicationEvidence
    prior_publication: PublishedTicketArtifact | None = None
    supersession_rationale: BoundedText | None = None


class PublishedTicketArtifact(_ApprovalPublishingModel):
    # PublishedTicketArtifact is logical canonical publication evidence only.
    schema_version: Literal[1] = HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION
    publication_id: PublicationIdentifier
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    revision: int = Field(ge=1, strict=True)
    state: Literal[TicketPublicationState.PUBLISHED] = TicketPublicationState.PUBLISHED
    format: Literal[TicketPublicationFormat.CANONICAL_JSON_V1] = (
        TicketPublicationFormat.CANONICAL_JSON_V1
    )
    canonical_ticket: TicketSpec
    canonical_ticket_JSON: CanonicalTicketJSON
    canonical_ticket_SHA256: DigestText
    approval_SHA256: DigestText
    supersedes_publication_id: PublicationIdentifier | None
    artifact_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_artifact(self) -> PublishedTicketArtifact:
        if self.publication_id != _publication_id(self.ticket_id, self.revision):
            raise ValueError("publication_id must match ticket_id and revision")
        if self.canonical_ticket.project_id != self.project_id:
            raise ValueError("canonical_ticket project_id must match artifact")
        if self.canonical_ticket.ticket_id != self.ticket_id:
            raise ValueError("canonical_ticket ticket_id must match artifact")
        if self.canonical_ticket_JSON != _canonical_ticket_json(self.canonical_ticket):
            raise ValueError("canonical_ticket_JSON must match canonical ticket")
        if self.canonical_ticket_SHA256 != _canonical_ticket_digest(
            self.canonical_ticket_JSON
        ):
            raise ValueError("canonical_ticket_SHA256 must match canonical JSON")
        expected = _artifact_digest(
            schema_version=self.schema_version,
            publication_id=self.publication_id,
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            revision=self.revision,
            state=self.state,
            format=self.format,
            canonical_ticket=self.canonical_ticket,
            canonical_ticket_JSON=self.canonical_ticket_JSON,
            canonical_ticket_SHA256=self.canonical_ticket_SHA256,
            approval_SHA256=self.approval_SHA256,
            supersedes_publication_id=self.supersedes_publication_id,
        )
        if self.artifact_SHA256 != expected:
            raise ValueError("artifact_SHA256 must match published artifact digest")
        return self


class TicketSupersessionRecord(_ApprovalPublishingModel):
    superseded_publication_id: PublicationIdentifier
    replacement_publication_id: PublicationIdentifier
    state: Literal[TicketPublicationState.SUPERSEDED] = (
        TicketPublicationState.SUPERSEDED
    )
    rationale: BoundedText
    evidence_reference: BoundedText
    supersession_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_supersession(self) -> TicketSupersessionRecord:
        if self.superseded_publication_id == self.replacement_publication_id:
            raise ValueError("supersession publication IDs must differ")
        expected = _supersession_digest(
            superseded_publication_id=self.superseded_publication_id,
            replacement_publication_id=self.replacement_publication_id,
            state=self.state,
            rationale=self.rationale,
            evidence_reference=self.evidence_reference,
        )
        if self.supersession_SHA256 != expected:
            raise ValueError("supersession_SHA256 must match supersession digest")
        return self


class TicketPublicationResult(_ApprovalPublishingModel):
    schema_version: Literal[1] = HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION
    publication: PublishedTicketArtifact
    supersession: TicketSupersessionRecord | None
    publication_input_SHA256: DigestText
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> TicketPublicationResult:
        if self.publication.revision == 1:
            if self.supersession is not None:
                raise ValueError("first publication must not include supersession")
            if self.publication.supersedes_publication_id is not None:
                raise ValueError(
                    "first publication must not supersede another artifact"
                )
        else:
            if self.supersession is None:
                raise ValueError("revision greater than one requires supersession")
            if (
                self.publication.supersedes_publication_id
                != self.supersession.superseded_publication_id
            ):
                raise ValueError("publication lineage must match supersession")
            if (
                self.supersession.replacement_publication_id
                != self.publication.publication_id
            ):
                raise ValueError("supersession replacement must match publication")
        expected = _publication_result_digest(
            schema_version=self.schema_version,
            publication=self.publication,
            supersession=self.supersession,
            publication_input_SHA256=self.publication_input_SHA256,
        )
        if self.result_SHA256 != expected:
            raise ValueError("result_SHA256 must match publication result digest")
        return self


def build_ticket_approval_record(
    request: TicketApprovalRequest,
) -> TicketApprovalRecord:
    """Build immutable explicit human approval or nonapproval evidence in memory."""

    _validate_approval_request_identity(request)
    review = _validated_synthesis_review(request.synthesis_review)
    resolutions = _canonical_conflict_resolutions(request.conflict_resolutions)
    selected_ticket: TicketSpec | None = None
    canonical_source: CanonicalTicketSource | None = None
    lint_report: TicketLintReport | None = None
    planning_evidence: FreshDependencyPlanningEvidence | None = None

    if request.decision is HumanApprovalDecision.APPROVE:
        _validate_approval_conflict_resolutions(
            review.conflicts,
            resolutions,
            manual_replacement_present=request.manual_replacement is not None,
        )
        selected_ticket, canonical_source = _selected_ticket_for_approval(
            request, review
        )
        lint_report = _fresh_selected_ticket_lint(request.project_spec, selected_ticket)
        _validate_fresh_lint_for_approval(lint_report, request.approval_evidence)
        planning_evidence = _validated_required_planning_evidence(
            request,
            selected_ticket,
        )
        state = TicketApprovalState.APPROVED
    elif request.decision is HumanApprovalDecision.REJECT:
        _reject_nonapproval_extras(request)
        _validate_nonapproval_conflict_resolutions(resolutions)
        state = TicketApprovalState.REJECTED
    else:
        _reject_nonapproval_extras(request)
        _validate_nonapproval_conflict_resolutions(resolutions)
        state = TicketApprovalState.REVISION_REQUIRED

    approval_input_SHA256 = _approval_input_digest(request, resolutions)
    approval_SHA256 = _approval_record_digest(
        schema_version=HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION,
        project_id=request.seed_ticket.project_id,
        ticket_id=request.seed_ticket.ticket_id,
        synthesis_review_SHA256=review.review_SHA256,
        decision=request.decision,
        state=state,
        canonical_source=canonical_source,
        approved_ticket=selected_ticket,
        approval_evidence=request.approval_evidence,
        conflict_resolutions=resolutions,
        approved_ticket_lint_report=lint_report,
        fresh_planning_evidence=planning_evidence,
        approval_input_SHA256=approval_input_SHA256,
    )
    return TicketApprovalRecord(
        project_id=request.seed_ticket.project_id,
        ticket_id=request.seed_ticket.ticket_id,
        synthesis_review_SHA256=review.review_SHA256,
        decision=request.decision,
        state=state,
        canonical_source=canonical_source,
        approved_ticket=selected_ticket,
        approval_evidence=request.approval_evidence,
        conflict_resolutions=resolutions,
        approved_ticket_lint_report=lint_report,
        fresh_planning_evidence=planning_evidence,
        approval_input_SHA256=approval_input_SHA256,
        approval_SHA256=approval_SHA256,
    )


def publish_canonical_ticket(
    request: TicketPublicationRequest,
) -> TicketPublicationResult:
    """Build in-memory logical canonical publication evidence for an approved record."""

    approval = _validated_approval_record_for_publication(request.approval_record)
    assert approval.approved_ticket is not None
    prior = _validated_prior_publication(request)
    revision = 1 if prior is None else prior.revision + 1
    supersedes_publication_id = None if prior is None else prior.publication_id
    publication_id = _publication_id(approval.ticket_id, revision)
    canonical_json = _canonical_ticket_json(approval.approved_ticket)
    canonical_sha = _canonical_ticket_digest(canonical_json)
    artifact_SHA256 = _artifact_digest(
        schema_version=HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION,
        publication_id=publication_id,
        project_id=approval.project_id,
        ticket_id=approval.ticket_id,
        revision=revision,
        state=TicketPublicationState.PUBLISHED,
        format=TicketPublicationFormat.CANONICAL_JSON_V1,
        canonical_ticket=approval.approved_ticket,
        canonical_ticket_JSON=canonical_json,
        canonical_ticket_SHA256=canonical_sha,
        approval_SHA256=approval.approval_SHA256,
        supersedes_publication_id=supersedes_publication_id,
    )
    publication = PublishedTicketArtifact(
        publication_id=publication_id,
        project_id=approval.project_id,
        ticket_id=approval.ticket_id,
        revision=revision,
        canonical_ticket=approval.approved_ticket,
        canonical_ticket_JSON=canonical_json,
        canonical_ticket_SHA256=canonical_sha,
        approval_SHA256=approval.approval_SHA256,
        supersedes_publication_id=supersedes_publication_id,
        artifact_SHA256=artifact_SHA256,
    )
    supersession = None
    if prior is not None:
        assert request.supersession_rationale is not None
        supersession_sha = _supersession_digest(
            superseded_publication_id=prior.publication_id,
            replacement_publication_id=publication.publication_id,
            state=TicketPublicationState.SUPERSEDED,
            rationale=request.supersession_rationale,
            evidence_reference=request.publication_evidence.publication_reference,
        )
        supersession = TicketSupersessionRecord(
            superseded_publication_id=prior.publication_id,
            replacement_publication_id=publication.publication_id,
            rationale=request.supersession_rationale,
            evidence_reference=request.publication_evidence.publication_reference,
            supersession_SHA256=supersession_sha,
        )
    publication_input_SHA256 = _publication_input_digest(request)
    result_SHA256 = _publication_result_digest(
        schema_version=HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION,
        publication=publication,
        supersession=supersession,
        publication_input_SHA256=publication_input_SHA256,
    )
    return TicketPublicationResult(
        publication=publication,
        supersession=supersession,
        publication_input_SHA256=publication_input_SHA256,
        result_SHA256=result_SHA256,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


def _resolution_sort_key(resolution: HumanConflictResolution) -> tuple[int, str]:
    return (int(resolution.conflict_id.rsplit("-", 1)[1]), resolution.action.value)


def _canonical_conflict_resolutions(
    resolutions: tuple[HumanConflictResolution, ...],
) -> tuple[HumanConflictResolution, ...]:
    conflict_ids = tuple(resolution.conflict_id for resolution in resolutions)
    if len(conflict_ids) != len(frozenset(conflict_ids)):
        raise TicketApprovalInputError("conflict resolution IDs must be unique")
    return tuple(sorted(resolutions, key=_resolution_sort_key))


def _validated_synthesis_review(review: TicketSynthesisReview) -> TicketSynthesisReview:
    try:
        return TicketSynthesisReview.model_validate(review.model_dump(mode="json"))
    except ValueError as exc:
        raise TicketApprovalValidationError(
            f"synthesis review digest evidence is invalid: ticket_id={review.ticket_id}"
        ) from exc


def _validated_candidate(
    candidate: SynthesizedTicketCandidate,
) -> SynthesizedTicketCandidate:
    try:
        return SynthesizedTicketCandidate.model_validate(
            candidate.model_dump(mode="json")
        )
    except ValueError as exc:
        raise TicketApprovalValidationError(
            f"synthesis candidate digest evidence is invalid: ticket_id={candidate.ticket_id}"
        ) from exc


def _validate_approval_request_identity(request: TicketApprovalRequest) -> None:
    if request.project_spec.project_id != request.seed_ticket.project_id:
        raise TicketApprovalInputError(
            f"project and seed ticket identifiers must match: project_id={request.project_spec.project_id}"
        )
    if request.synthesis_review.project_id != request.seed_ticket.project_id:
        raise TicketApprovalInputError(
            f"synthesis review project_id must match seed: project_id={request.seed_ticket.project_id}"
        )
    if request.synthesis_review.ticket_id != request.seed_ticket.ticket_id:
        raise TicketApprovalInputError(
            f"synthesis review ticket_id must match seed: ticket_id={request.seed_ticket.ticket_id}"
        )
    review = _validated_synthesis_review(request.synthesis_review)
    if review.candidate is not None:
        candidate = _validated_candidate(review.candidate)
        if candidate.project_id != request.seed_ticket.project_id:
            raise TicketApprovalInputError("candidate project_id must match seed")
        if candidate.ticket_id != request.seed_ticket.ticket_id:
            raise TicketApprovalInputError("candidate ticket_id must match seed")
        if (
            candidate.synthesized_ticket.ticket_type
            is not request.seed_ticket.ticket_type
        ):
            raise TicketApprovalInputError("candidate ticket_type must match seed")
    if request.manual_replacement is not None:
        _validate_manual_replacement_identity(
            request.manual_replacement,
            request.seed_ticket,
            error_type=TicketApprovalInputError,
        )


def _validate_manual_replacement_identity(
    replacement: ManualTicketReplacement,
    seed: TicketSpec,
    *,
    error_type: type[Exception],
) -> None:
    ticket = replacement.replacement_ticket
    if ticket.schema_version != seed.schema_version:
        raise error_type("manual replacement schema_version must match seed")
    if ticket.project_id != seed.project_id:
        raise error_type("manual replacement project_id must match seed")
    if ticket.ticket_id != seed.ticket_id:
        raise error_type("manual replacement ticket_id must match seed")
    if ticket.ticket_type is not seed.ticket_type:
        raise error_type("manual replacement ticket_type must match seed")


def _validate_approval_conflict_resolutions(
    conflicts: tuple[ProposalConflict, ...],
    resolutions: tuple[HumanConflictResolution, ...],
    *,
    manual_replacement_present: bool,
) -> None:
    conflict_ids = tuple(conflict.conflict_id for conflict in conflicts)
    resolution_ids = tuple(resolution.conflict_id for resolution in resolutions)
    if frozenset(resolution_ids) != frozenset(conflict_ids):
        raise TicketApprovalInputError(
            "approval requires exactly one resolution per conflict"
        )
    by_id = {conflict.conflict_id: conflict for conflict in conflicts}
    for resolution in resolutions:
        _validate_resolution_compatibility(
            by_id[resolution.conflict_id],
            resolution,
            manual_replacement_present=manual_replacement_present,
        )


def _validate_resolution_compatibility(
    conflict: ProposalConflict,
    resolution: HumanConflictResolution,
    *,
    manual_replacement_present: bool,
) -> None:
    action = resolution.action
    if action is ConflictResolutionAction.REJECT:
        raise TicketApprovalInputError("approve decision cannot use reject resolution")
    if action is ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT:
        if not manual_replacement_present:
            raise TicketApprovalInputError(
                "manual replacement action requires replacement"
            )
        return
    if (
        manual_replacement_present
        and action is ConflictResolutionAction.ACCEPT_CANDIDATE
    ):
        raise TicketApprovalInputError(
            "manual replacement cannot accept candidate conflict"
        )
    if conflict.severity is ProposalConflictSeverity.BLOCKING:
        raise TicketApprovalValidationError(
            f"blocking conflict requires manual replacement: conflict_id={conflict.conflict_id}"
        )
    if conflict.severity is ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED:
        if action is ConflictResolutionAction.ACKNOWLEDGE:
            raise TicketApprovalInputError(
                f"human-review conflict cannot be acknowledged: conflict_id={conflict.conflict_id}"
            )
        return
    if action in {
        ConflictResolutionAction.ACKNOWLEDGE,
        ConflictResolutionAction.ACCEPT_CANDIDATE,
    }:
        return
    raise TicketApprovalInputError(
        f"unsupported conflict action: conflict_id={conflict.conflict_id}"
    )


def _validate_nonapproval_conflict_resolutions(
    resolutions: tuple[HumanConflictResolution, ...],
) -> None:
    for resolution in resolutions:
        if resolution.action not in {
            ConflictResolutionAction.ACKNOWLEDGE,
            ConflictResolutionAction.REJECT,
        }:
            raise TicketApprovalInputError(
                "nonapproval records allow only acknowledge or reject"
            )


def _reject_nonapproval_extras(request: TicketApprovalRequest) -> None:
    if request.manual_replacement is not None:
        raise TicketApprovalInputError(
            "nonapproval decision must not include manual replacement"
        )
    if request.fresh_planning_evidence is not None:
        raise TicketApprovalInputError(
            "nonapproval decision must not include planning evidence"
        )


def _selected_ticket_for_approval(
    request: TicketApprovalRequest,
    review: TicketSynthesisReview,
) -> tuple[TicketSpec, CanonicalTicketSource]:
    if request.manual_replacement is not None:
        return (
            request.manual_replacement.replacement_ticket,
            CanonicalTicketSource.MANUAL_REPLACEMENT,
        )
    if review.candidate is None:
        raise TicketApprovalInputError(
            "approval requires candidate or manual replacement"
        )
    candidate = _validated_candidate(review.candidate)
    return (candidate.synthesized_ticket, CanonicalTicketSource.SYNTHESIZED_CANDIDATE)


def _fresh_selected_ticket_lint(
    project_spec: ProjectSpec,
    selected_ticket: TicketSpec,
) -> TicketLintReport:
    return lint_ticket_collection(
        TicketLintRequest(
            project_spec=project_spec,
            tickets=(selected_ticket,),
            dependency_plan=None,
            collection_complete=False,
        )
    )


def _validate_fresh_lint_for_approval(
    lint_report: TicketLintReport,
    evidence: HumanApprovalEvidence,
) -> None:
    try:
        TicketLintReport.model_validate(lint_report.model_dump(mode="json"))
    except ValueError as exc:
        raise TicketApprovalValidationError(
            "fresh lint report digest evidence is invalid"
        ) from exc
    if lint_report.disposition is TicketLintDisposition.BLOCKED:
        raise TicketApprovalValidationError(
            f"fresh lint blocked approved ticket: report_SHA256={lint_report.report_SHA256}"
        )
    if (
        lint_report.disposition is TicketLintDisposition.PASS_WITH_WARNINGS
        and evidence.policy_warning_acknowledgement is None
    ):
        raise TicketApprovalValidationError(
            "policy warning acknowledgement is required"
        )


def _validated_required_planning_evidence(
    request: TicketApprovalRequest,
    selected_ticket: TicketSpec,
) -> FreshDependencyPlanningEvidence | None:
    changed = (
        selected_ticket.dependencies != request.seed_ticket.dependencies
        or selected_ticket.scope != request.seed_ticket.scope
    )
    evidence = request.fresh_planning_evidence
    if evidence is None:
        if changed:
            raise TicketApprovalValidationError("fresh planning evidence is required")
        return None
    _validate_planning_evidence_for_selected_ticket(
        evidence,
        request.project_spec,
        selected_ticket,
        request.approval_evidence,
    )
    return evidence


def _validate_planning_evidence_recomputes(
    evidence: FreshDependencyPlanningEvidence,
    *,
    error_type: type[Exception],
) -> None:
    try:
        TicketDependencyPlan.model_validate(
            evidence.dependency_plan.model_dump(mode="json")
        )
    except ValueError as exc:
        raise error_type("dependency plan digest evidence is invalid") from exc
    recomputed = build_ticket_dependency_plan(evidence.planning_request)
    if recomputed != evidence.dependency_plan:
        raise error_type("dependency plan must equal recomputed planning evidence")


def _validate_planning_evidence_for_selected_ticket(
    evidence: FreshDependencyPlanningEvidence,
    project_spec: ProjectSpec,
    selected_ticket: TicketSpec,
    approval_evidence: HumanApprovalEvidence,
) -> None:
    _validate_planning_evidence_recomputes(
        evidence, error_type=TicketApprovalValidationError
    )
    if evidence.planning_request.project_spec.project_id != project_spec.project_id:
        raise TicketApprovalInputError(
            "planning request project_id must match approval"
        )
    if evidence.dependency_plan.project_id != project_spec.project_id:
        raise TicketApprovalInputError("dependency plan project_id must match approval")
    planning_ticket_by_id = {
        ticket.ticket_id: ticket for ticket in evidence.planning_request.tickets
    }
    if selected_ticket.ticket_id not in planning_ticket_by_id:
        raise TicketApprovalValidationError(
            "selected ticket must be in planning request"
        )
    if planning_ticket_by_id[selected_ticket.ticket_id] != selected_ticket:
        raise TicketApprovalValidationError(
            "selected ticket content must match planning request"
        )
    if selected_ticket.ticket_id in evidence.dependency_plan.blocked_ticket_ids:
        raise TicketApprovalValidationError(
            "selected ticket is blocked by planning evidence"
        )
    if frozenset(evidence.dependency_plan.ticket_ids) != frozenset(
        planning_ticket_by_id
    ):
        raise TicketApprovalValidationError(
            "dependency plan ticket set must match planning request"
        )
    if _planning_warning_requires_acknowledgement(evidence, selected_ticket.ticket_id):
        if approval_evidence.planning_warning_acknowledgement is None:
            raise TicketApprovalValidationError(
                "planning warning acknowledgement is required"
            )


def _planning_warning_requires_acknowledgement(
    evidence: FreshDependencyPlanningEvidence,
    selected_ticket_id: str,
) -> bool:
    if evidence.dependency_plan.unresolved_soft_external_dependency_ids:
        return True
    return any(
        wave.disposition is WaveDisposition.SCOPE_REVIEW_REQUIRED
        and selected_ticket_id in wave.ticket_ids
        for wave in evidence.dependency_plan.waves
    )


def _validate_approval_record_state(
    record: TicketApprovalRecord,
    *,
    error_type: type[Exception],
) -> None:
    if record.state is TicketApprovalState.APPROVED:
        if record.decision is not HumanApprovalDecision.APPROVE:
            raise error_type("approved state requires approve decision")
        if record.approved_ticket is None:
            raise error_type("approved state requires approved_ticket")
        if record.canonical_source is None:
            raise error_type("approved state requires canonical_source")
        if record.approved_ticket_lint_report is None:
            raise error_type("approved state requires approved_ticket_lint_report")
        return
    if record.state is TicketApprovalState.REJECTED:
        expected_decision = HumanApprovalDecision.REJECT
    else:
        expected_decision = HumanApprovalDecision.REQUEST_REVISION
    if record.decision is not expected_decision:
        raise error_type("nonapproval state must match decision")
    if record.approved_ticket is not None:
        raise error_type("nonapproval state must not include approved_ticket")
    if record.canonical_source is not None:
        raise error_type("nonapproval state must not include canonical_source")
    if record.approved_ticket_lint_report is not None:
        raise error_type("nonapproval state must not include lint report")
    if record.fresh_planning_evidence is not None:
        raise error_type("nonapproval state must not include planning evidence")


def _approval_input_digest(
    request: TicketApprovalRequest,
    resolutions: tuple[HumanConflictResolution, ...],
) -> str:
    record = {
        "algorithm": APPROVAL_INPUT_DIGEST_ALGORITHM,
        "project_spec": request.project_spec.model_dump(mode="json"),
        "seed_ticket": request.seed_ticket.model_dump(mode="json"),
        "synthesis_review": request.synthesis_review.model_dump(mode="json"),
        "decision": request.decision.value,
        "conflict_resolutions": [
            resolution.model_dump(mode="json") for resolution in resolutions
        ],
        "approval_evidence": request.approval_evidence.model_dump(mode="json"),
        "manual_replacement": None
        if request.manual_replacement is None
        else request.manual_replacement.model_dump(mode="json"),
        "fresh_planning_evidence": None
        if request.fresh_planning_evidence is None
        else request.fresh_planning_evidence.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _approval_record_digest(
    *,
    schema_version: int,
    project_id: str,
    ticket_id: str,
    synthesis_review_SHA256: str,
    decision: HumanApprovalDecision,
    state: TicketApprovalState,
    canonical_source: CanonicalTicketSource | None,
    approved_ticket: TicketSpec | None,
    approval_evidence: HumanApprovalEvidence,
    conflict_resolutions: tuple[HumanConflictResolution, ...],
    approved_ticket_lint_report: TicketLintReport | None,
    fresh_planning_evidence: FreshDependencyPlanningEvidence | None,
    approval_input_SHA256: str,
) -> str:
    record = {
        "algorithm": APPROVAL_RECORD_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "synthesis_review_SHA256": synthesis_review_SHA256,
        "decision": decision.value,
        "state": state.value,
        "canonical_source": None
        if canonical_source is None
        else canonical_source.value,
        "approved_ticket": None
        if approved_ticket is None
        else approved_ticket.model_dump(mode="json"),
        "approval_evidence": approval_evidence.model_dump(mode="json"),
        "conflict_resolutions": [
            resolution.model_dump(mode="json") for resolution in conflict_resolutions
        ],
        "approved_ticket_lint_report": None
        if approved_ticket_lint_report is None
        else approved_ticket_lint_report.model_dump(mode="json"),
        "fresh_planning_evidence": None
        if fresh_planning_evidence is None
        else fresh_planning_evidence.model_dump(mode="json"),
        "approval_input_SHA256": approval_input_SHA256,
    }
    return _sha256_text(_deterministic_json(record))


def _canonical_ticket_json(ticket: TicketSpec) -> str:
    return _deterministic_json(ticket.model_dump(mode="json"))


def _canonical_ticket_digest(canonical_ticket_JSON: str) -> str:
    return _sha256_text(canonical_ticket_JSON)


def _publication_id(ticket_id: str, revision: int) -> str:
    return f"PUB-{ticket_id.replace('.', '-')}-{revision:04d}"


def _artifact_digest(
    *,
    schema_version: int,
    publication_id: str,
    project_id: str,
    ticket_id: str,
    revision: int,
    state: TicketPublicationState,
    format: TicketPublicationFormat,
    canonical_ticket: TicketSpec,
    canonical_ticket_JSON: str,
    canonical_ticket_SHA256: str,
    approval_SHA256: str,
    supersedes_publication_id: str | None,
) -> str:
    record = {
        "algorithm": PUBLISHED_TICKET_ARTIFACT_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "publication_id": publication_id,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "revision": revision,
        "state": state.value,
        "format": format.value,
        "canonical_ticket": canonical_ticket.model_dump(mode="json"),
        "canonical_ticket_JSON": canonical_ticket_JSON,
        "canonical_ticket_SHA256": canonical_ticket_SHA256,
        "approval_SHA256": approval_SHA256,
        "supersedes_publication_id": supersedes_publication_id,
    }
    return _sha256_text(_deterministic_json(record))


def _supersession_digest(
    *,
    superseded_publication_id: str,
    replacement_publication_id: str,
    state: TicketPublicationState,
    rationale: str,
    evidence_reference: str,
) -> str:
    record = {
        "algorithm": TICKET_SUPERSESSION_DIGEST_ALGORITHM,
        "superseded_publication_id": superseded_publication_id,
        "replacement_publication_id": replacement_publication_id,
        "state": state.value,
        "rationale": rationale,
        "evidence_reference": evidence_reference,
    }
    return _sha256_text(_deterministic_json(record))


def _publication_input_digest(request: TicketPublicationRequest) -> str:
    record = {
        "algorithm": PUBLICATION_INPUT_DIGEST_ALGORITHM,
        "approval_record": request.approval_record.model_dump(mode="json"),
        "publication_evidence": request.publication_evidence.model_dump(mode="json"),
        "prior_publication": None
        if request.prior_publication is None
        else request.prior_publication.model_dump(mode="json"),
        "supersession_rationale": request.supersession_rationale,
    }
    return _sha256_text(_deterministic_json(record))


def _publication_result_digest(
    *,
    schema_version: int,
    publication: PublishedTicketArtifact,
    supersession: TicketSupersessionRecord | None,
    publication_input_SHA256: str,
) -> str:
    record = {
        "algorithm": PUBLICATION_RESULT_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "publication": publication.model_dump(mode="json"),
        "supersession": None
        if supersession is None
        else supersession.model_dump(mode="json"),
        "publication_input_SHA256": publication_input_SHA256,
    }
    return _sha256_text(_deterministic_json(record))


def _validated_approval_record_for_publication(
    approval: TicketApprovalRecord,
) -> TicketApprovalRecord:
    try:
        validated = TicketApprovalRecord.model_validate(
            approval.model_dump(mode="json")
        )
    except ValueError as exc:
        raise TicketPublicationAuthorizationError(
            "approval record digest is invalid"
        ) from exc
    if validated.state is not TicketApprovalState.APPROVED:
        raise TicketPublicationAuthorizationError(
            "only approved records can be published"
        )
    if (
        validated.approved_ticket is None
        or validated.approved_ticket_lint_report is None
    ):
        raise TicketPublicationAuthorizationError(
            "approved record lacks publication evidence"
        )
    return validated


def _validated_prior_publication(
    request: TicketPublicationRequest,
) -> PublishedTicketArtifact | None:
    prior = request.prior_publication
    if prior is None:
        if request.supersession_rationale is not None:
            raise TicketPublicationAuthorizationError(
                "supersession rationale requires prior publication"
            )
        return None
    try:
        validated = PublishedTicketArtifact.model_validate(
            prior.model_dump(mode="json")
        )
    except ValueError as exc:
        raise TicketPublicationAuthorizationError(
            "prior publication digest is invalid"
        ) from exc
    approval = request.approval_record
    if validated.project_id != approval.project_id:
        raise TicketPublicationAuthorizationError("prior publication project mismatch")
    if validated.ticket_id != approval.ticket_id:
        raise TicketPublicationAuthorizationError("prior publication ticket mismatch")
    if request.supersession_rationale is None:
        raise TicketPublicationAuthorizationError(
            "prior publication requires supersession rationale"
        )
    return validated
