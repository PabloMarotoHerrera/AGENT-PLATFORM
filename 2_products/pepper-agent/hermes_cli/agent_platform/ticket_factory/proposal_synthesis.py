"""Deterministic noncanonical synthesis review for independent proposals."""

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
    StrictBool,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory.dependency_planning import (
    TicketDependencyPlan,
)
from hermes_cli.agent_platform.ticket_factory.generator_roles import (
    GeneratorAssignment,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketProposal,
    TicketProposalValidationError,
    prepare_ticket_generator_assignments,
    validate_ticket_generator_proposal,
)
from hermes_cli.agent_platform.ticket_factory.specs import (
    ProjectIdentifier,
    TicketIdentifier,
    TicketSpec,
)
from hermes_cli.agent_platform.ticket_factory.ticket_policy import (
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    lint_ticket_collection,
)

MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION = 1
SYNTHESIS_INPUT_DIGEST_ALGORITHM = "agent-platform-ticket-synthesis-input-sha256-v1"
SYNTHESIZED_TICKET_CANDIDATE_DIGEST_ALGORITHM = (
    "agent-platform-synthesized-ticket-candidate-sha256-v1"
)
SYNTHESIS_REVIEW_DIGEST_ALGORITHM = "agent-platform-ticket-synthesis-review-sha256-v1"


class TicketSynthesisError(ValueError):
    """Base error for multi-generator synthesis review failures."""


class TicketSynthesisInputError(TicketSynthesisError):
    """Raised when assignments, proposal bindings or context are inconsistent."""


class TicketSynthesisValidationError(TicketSynthesisError):
    """Raised when proposal or lint-report digest evidence is invalid."""


class TicketSynthesisField(str, Enum):
    TITLE = "title"
    OBJECTIVE = "objective"
    CONTEXT = "context"
    AUTHORITY_REFERENCES = "authority_references"
    DEPENDENCIES = "dependencies"
    PARALLELIZATION_HINT = "parallelization_hint"
    SCOPE = "scope"
    CONSTRAINTS = "constraints"
    TASKS = "tasks"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"
    VALIDATION_STEPS = "validation_steps"
    RESPONSE_CONTRACT = "response_contract"
    RECOMMENDED_COMMIT_MESSAGE = "recommended_commit_message"


class ProposalAgreementLevel(str, Enum):
    UNANIMOUS = "unanimous"
    STRICT_MAJORITY = "strict_majority"
    SPLIT = "split"


class FieldResolutionKind(str, Enum):
    ADOPT_UNANIMOUS = "adopt_unanimous"
    ADOPT_STRICT_MAJORITY = "adopt_strict_majority"
    PRESERVE_SEED = "preserve_seed"


class ProposalConflictKind(str, Enum):
    LINT_BLOCKED_PROPOSAL = "lint_blocked_proposal"
    FIELD_DISSENT = "field_dissent"
    FIELD_SPLIT = "field_split"
    DEPENDENCY_PLAN_STALE = "dependency_plan_stale"
    SCOPE_PLAN_STALE = "scope_plan_stale"
    CANDIDATE_LINT_BLOCKED = "candidate_lint_blocked"
    INSUFFICIENT_ELIGIBLE_PROPOSALS = "insufficient_eligible_proposals"


class ProposalConflictSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    BLOCKING = "blocking"


class TicketSynthesisDisposition(str, Enum):
    REVIEW_READY = "review_ready"
    REVIEW_READY_WITH_DISSENT = "review_ready_with_dissent"
    HUMAN_RESOLUTION_REQUIRED = "human_resolution_required"
    BLOCKED = "blocked"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


ShortText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_reject_nul),
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
CandidateIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=8,
        max_length=70,
        pattern=r"^CAND-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+$",
    ),
]


class _SynthesisModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


class ReviewedTicketProposal(_SynthesisModel):
    proposal: TicketProposal
    lint_report: TicketLintReport

    @model_validator(mode="after")
    def _validate_reviewed_proposal(self) -> ReviewedTicketProposal:
        _validate_lint_report_binding(
            self.proposal, self.lint_report, error_type=ValueError
        )
        return self


class TicketSynthesisRequest(_SynthesisModel):
    generation_request: TicketGenerationRequest
    assignments: tuple[GeneratorAssignment, ...] = Field(min_length=2, max_length=6)
    reviewed_proposals: tuple[ReviewedTicketProposal, ...] = Field(
        min_length=2, max_length=6
    )
    dependency_plan: TicketDependencyPlan | None = None

    @model_validator(mode="after")
    def _validate_request(self) -> TicketSynthesisRequest:
        _validate_synthesis_request(
            self,
            input_error_type=ValueError,
            validation_error_type=ValueError,
        )
        return self


class ProposalVariantEvidence(_SynthesisModel):
    variant_SHA256: DigestText
    support_count: int = Field(ge=1, strict=True)
    supporting_proposal_SHA256s: tuple[DigestText, ...] = Field(min_length=1)
    supporting_roles: tuple[TicketGeneratorRole, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_variant(self) -> ProposalVariantEvidence:
        _reject_duplicate_values(
            self.supporting_proposal_SHA256s, "supporting_proposal_SHA256s"
        )
        _reject_duplicate_values(self.supporting_roles, "supporting_roles")
        if self.support_count != len(self.supporting_proposal_SHA256s):
            raise ValueError("support_count must equal supporting proposal count")
        if self.support_count != len(self.supporting_roles):
            raise ValueError("support_count must equal supporting role count")
        if (
            tuple(sorted(self.supporting_roles, key=_role_sort_key))
            != self.supporting_roles
        ):
            raise ValueError("supporting_roles must be in canonical role order")
        return self


class FieldSynthesisDecision(_SynthesisModel):
    field: TicketSynthesisField
    agreement_level: ProposalAgreementLevel
    resolution: FieldResolutionKind
    seed_value_SHA256: DigestText
    selected_value_SHA256: DigestText
    variants: tuple[ProposalVariantEvidence, ...] = Field(min_length=1)
    supporting_proposal_SHA256s: tuple[DigestText, ...]
    dissenting_proposal_SHA256s: tuple[DigestText, ...]

    @model_validator(mode="after")
    def _validate_decision(self) -> FieldSynthesisDecision:
        _reject_duplicate_values(
            self.supporting_proposal_SHA256s, "supporting_proposal_SHA256s"
        )
        _reject_duplicate_values(
            self.dissenting_proposal_SHA256s, "dissenting_proposal_SHA256s"
        )
        if tuple(sorted(self.variants, key=_variant_sort_key)) != self.variants:
            raise ValueError("variants must be in deterministic order")
        if self.agreement_level is ProposalAgreementLevel.UNANIMOUS:
            if self.resolution is not FieldResolutionKind.ADOPT_UNANIMOUS:
                raise ValueError("unanimous fields must adopt unanimous value")
            if self.dissenting_proposal_SHA256s:
                raise ValueError("unanimous fields must not have dissenting proposals")
        elif self.agreement_level is ProposalAgreementLevel.STRICT_MAJORITY:
            if self.resolution is not FieldResolutionKind.ADOPT_STRICT_MAJORITY:
                raise ValueError("strict-majority fields must adopt majority value")
            if not self.supporting_proposal_SHA256s:
                raise ValueError("strict-majority fields require supporting proposals")
            if not self.dissenting_proposal_SHA256s:
                raise ValueError("strict-majority fields require dissenting proposals")
        else:
            if self.resolution is not FieldResolutionKind.PRESERVE_SEED:
                raise ValueError("split fields must preserve seed value")
            if self.selected_value_SHA256 != self.seed_value_SHA256:
                raise ValueError("split selected value must equal seed value")
        return self


class ProposalConflict(_SynthesisModel):
    conflict_id: ConflictIdentifier
    kind: ProposalConflictKind
    severity: ProposalConflictSeverity
    field: TicketSynthesisField | None
    proposal_SHA256: DigestText | None
    related_proposal_SHA256s: tuple[DigestText, ...] = ()
    message: ShortText
    remediation: ShortText
    blocking: StrictBool

    @model_validator(mode="after")
    def _validate_conflict(self) -> ProposalConflict:
        _reject_duplicate_values(
            self.related_proposal_SHA256s, "related_proposal_SHA256s"
        )
        if (
            self.kind
            in {
                ProposalConflictKind.FIELD_DISSENT,
                ProposalConflictKind.FIELD_SPLIT,
            }
            and self.field is None
        ):
            raise ValueError("field conflicts require field")
        if (
            self.kind is ProposalConflictKind.LINT_BLOCKED_PROPOSAL
            and self.proposal_SHA256 is None
        ):
            raise ValueError("lint-blocked proposal conflicts require proposal_SHA256")
        if self.severity is ProposalConflictSeverity.BLOCKING and not self.blocking:
            raise ValueError("blocking severity requires blocking=true")
        if self.severity is not ProposalConflictSeverity.BLOCKING and self.blocking:
            raise ValueError("non-blocking severity requires blocking=false")
        return self


class SynthesizedTicketCandidate(_SynthesisModel):
    # SynthesizedTicketCandidate is review evidence, not approval or publication authority.
    schema_version: Literal[1] = MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION
    candidate_id: CandidateIdentifier
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    synthesized_ticket: TicketSpec
    source_proposal_SHA256s: tuple[DigestText, ...] = Field(min_length=1)
    excluded_proposal_SHA256s: tuple[DigestText, ...] = ()
    field_decisions: tuple[FieldSynthesisDecision, ...]
    unresolved_conflict_ids: tuple[ConflictIdentifier, ...]
    candidate_lint_report: TicketLintReport
    candidate_SHA256: DigestText

    @field_validator(
        "source_proposal_SHA256s", "excluded_proposal_SHA256s", mode="after"
    )
    @classmethod
    def _validate_unique_digest_tuple(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "proposal_SHA256s")
        return value

    @model_validator(mode="after")
    def _validate_candidate(self) -> SynthesizedTicketCandidate:
        if self.candidate_id != _candidate_id(self.ticket_id):
            raise ValueError("candidate_id must match ticket_id")
        if self.synthesized_ticket.project_id != self.project_id:
            raise ValueError("synthesized_ticket project_id must match candidate")
        if self.synthesized_ticket.ticket_id != self.ticket_id:
            raise ValueError("synthesized_ticket ticket_id must match candidate")
        if frozenset(self.source_proposal_SHA256s).intersection(
            self.excluded_proposal_SHA256s
        ):
            raise ValueError("source and excluded proposals must not overlap")
        _validate_complete_field_decisions(self.field_decisions)
        _reject_duplicate_values(
            self.unresolved_conflict_ids, "unresolved_conflict_ids"
        )
        _validate_candidate_lint_report(
            self.project_id,
            self.ticket_id,
            self.candidate_lint_report,
            error_type=ValueError,
        )
        expected_digest = _candidate_digest(
            schema_version=self.schema_version,
            candidate_id=self.candidate_id,
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            synthesized_ticket=self.synthesized_ticket,
            source_proposal_SHA256s=self.source_proposal_SHA256s,
            excluded_proposal_SHA256s=self.excluded_proposal_SHA256s,
            field_decisions=self.field_decisions,
            unresolved_conflict_ids=self.unresolved_conflict_ids,
            candidate_lint_report=self.candidate_lint_report,
        )
        if self.candidate_SHA256 != expected_digest:
            raise ValueError("candidate_SHA256 must match synthesized candidate digest")
        return self


class TicketSynthesisReview(_SynthesisModel):
    # TicketSynthesisReview is review evidence, not approval or publication authority.
    schema_version: Literal[1] = MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    synthesis_input_SHA256: DigestText
    proposal_SHA256s: tuple[DigestText, ...] = Field(min_length=1)
    eligible_proposal_SHA256s: tuple[DigestText, ...]
    excluded_proposal_SHA256s: tuple[DigestText, ...]
    field_decisions: tuple[FieldSynthesisDecision, ...]
    conflicts: tuple[ProposalConflict, ...]
    candidate: SynthesizedTicketCandidate | None
    disposition: TicketSynthesisDisposition
    review_SHA256: DigestText

    @field_validator(
        "proposal_SHA256s",
        "eligible_proposal_SHA256s",
        "excluded_proposal_SHA256s",
        mode="after",
    )
    @classmethod
    def _validate_unique_review_digest_tuple(
        cls, value: tuple[str, ...]
    ) -> tuple[str, ...]:
        _reject_duplicate_values(value, "proposal_SHA256s")
        return value

    @model_validator(mode="after")
    def _validate_review(self) -> TicketSynthesisReview:
        proposal_set = frozenset(self.proposal_SHA256s)
        eligible_set = frozenset(self.eligible_proposal_SHA256s)
        excluded_set = frozenset(self.excluded_proposal_SHA256s)
        if eligible_set.union(excluded_set) != proposal_set:
            raise ValueError("eligible and excluded proposals must partition proposals")
        if eligible_set.intersection(excluded_set):
            raise ValueError("eligible and excluded proposals must not overlap")
        if len(self.eligible_proposal_SHA256s) < 2:
            if self.candidate is not None:
                raise ValueError(
                    "candidate must be absent when eligibility is insufficient"
                )
            if self.field_decisions:
                raise ValueError("field decisions must be empty without a candidate")
        else:
            if self.candidate is None:
                raise ValueError("candidate must be present with sufficient proposals")
            _validate_complete_field_decisions(self.field_decisions)
        conflict_ids = tuple(conflict.conflict_id for conflict in self.conflicts)
        _reject_duplicate_values(conflict_ids, "conflict_ids")
        if tuple(sorted(self.conflicts, key=_conflict_sort_key)) != self.conflicts:
            raise ValueError("conflicts must be in deterministic order")
        expected_ids = tuple(
            _conflict_id(index) for index in range(1, len(self.conflicts) + 1)
        )
        if conflict_ids != expected_ids:
            raise ValueError("conflict identifiers must be sequential")
        if self.candidate is not None:
            if self.candidate.project_id != self.project_id:
                raise ValueError("candidate project_id must match review")
            if self.candidate.ticket_id != self.ticket_id:
                raise ValueError("candidate ticket_id must match review")
            if self.candidate.source_proposal_SHA256s != self.eligible_proposal_SHA256s:
                raise ValueError(
                    "candidate source proposals must match eligible proposals"
                )
            if (
                self.candidate.excluded_proposal_SHA256s
                != self.excluded_proposal_SHA256s
            ):
                raise ValueError("candidate excluded proposals must match review")
            if self.candidate.field_decisions != self.field_decisions:
                raise ValueError("candidate field decisions must match review")
            if self.candidate.unresolved_conflict_ids != conflict_ids:
                raise ValueError("candidate unresolved conflicts must match review")
        expected_disposition = _disposition_for_conflicts(
            self.conflicts, self.candidate, self.eligible_proposal_SHA256s
        )
        if self.disposition is not expected_disposition:
            raise ValueError("disposition must match conflicts and candidate")
        expected_digest = _review_digest(
            schema_version=self.schema_version,
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            synthesis_input_SHA256=self.synthesis_input_SHA256,
            proposal_SHA256s=self.proposal_SHA256s,
            eligible_proposal_SHA256s=self.eligible_proposal_SHA256s,
            excluded_proposal_SHA256s=self.excluded_proposal_SHA256s,
            field_decisions=self.field_decisions,
            conflicts=self.conflicts,
            candidate=self.candidate,
            disposition=self.disposition,
        )
        if self.review_SHA256 != expected_digest:
            raise ValueError("review_SHA256 must match synthesis review digest")
        return self


_SYNTHESIS_FIELDS = tuple(TicketSynthesisField)
_CANONICAL_ROLE_ORDER = (
    TicketGeneratorRole.ARCHITECTURE,
    TicketGeneratorRole.IMPLEMENTATION,
    TicketGeneratorRole.VALIDATION,
    TicketGeneratorRole.INTEGRATION,
    TicketGeneratorRole.GOVERNANCE,
    TicketGeneratorRole.DOCUMENTATION,
)
_ROLE_RANK = {role: index for index, role in enumerate(_CANONICAL_ROLE_ORDER)}
_AGREEMENT_RANK = {level: index for index, level in enumerate(ProposalAgreementLevel)}
_FIELD_RANK = {field: index for index, field in enumerate(TicketSynthesisField)}
_CONFLICT_KIND_RANK = {kind: index for index, kind in enumerate(ProposalConflictKind)}
_CONFLICT_SEVERITY_RANK = {
    ProposalConflictSeverity.BLOCKING: 0,
    ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED: 1,
    ProposalConflictSeverity.WARNING: 2,
    ProposalConflictSeverity.INFO: 3,
}


def build_ticket_synthesis_review(
    request: TicketSynthesisRequest,
) -> TicketSynthesisReview:
    """Build deterministic noncanonical synthesis review evidence in memory."""

    _validate_synthesis_request(
        request,
        input_error_type=TicketSynthesisInputError,
        validation_error_type=TicketSynthesisValidationError,
    )
    reviewed = _canonical_reviewed_proposals(request.reviewed_proposals)
    eligible = tuple(
        item
        for item in reviewed
        if item.lint_report.disposition
        in {TicketLintDisposition.PASS, TicketLintDisposition.PASS_WITH_WARNINGS}
    )
    excluded = tuple(
        item
        for item in reviewed
        if item.lint_report.disposition is TicketLintDisposition.BLOCKED
    )
    proposal_SHA256s = tuple(item.proposal.proposal_SHA256 for item in reviewed)
    eligible_SHA256s = tuple(item.proposal.proposal_SHA256 for item in eligible)
    excluded_SHA256s = tuple(item.proposal.proposal_SHA256 for item in excluded)
    conflicts = list(_lint_blocked_conflicts(excluded))
    field_decisions: tuple[FieldSynthesisDecision, ...] = ()
    candidate: SynthesizedTicketCandidate | None = None

    if len(eligible) < 2:
        conflicts.append(_insufficient_eligible_conflict(len(eligible)))
        conflicts = list(_assign_conflict_ids(tuple(conflicts)))
    else:
        field_decisions, field_conflicts, selected_values = _field_decisions(
            request.generation_request.ticket_spec, eligible
        )
        conflicts.extend(field_conflicts)
        synthesized_ticket = _synthesized_ticket(
            request.generation_request.ticket_spec, selected_values
        )
        conflicts.extend(
            _plan_staleness_conflicts(
                request.generation_request.ticket_spec,
                synthesized_ticket,
                request.dependency_plan,
            )
        )
        candidate_lint_report = lint_ticket_collection(
            TicketLintRequest(
                project_spec=request.generation_request.project_spec,
                tickets=(synthesized_ticket,),
                dependency_plan=None,
                collection_complete=False,
            )
        )
        if candidate_lint_report.disposition is TicketLintDisposition.BLOCKED:
            conflicts.append(_candidate_lint_blocked_conflict(candidate_lint_report))
        conflicts = list(_assign_conflict_ids(tuple(conflicts)))
        unresolved_conflict_ids = tuple(conflict.conflict_id for conflict in conflicts)
        candidate = _make_candidate(
            synthesized_ticket=synthesized_ticket,
            source_proposal_SHA256s=eligible_SHA256s,
            excluded_proposal_SHA256s=excluded_SHA256s,
            field_decisions=field_decisions,
            unresolved_conflict_ids=unresolved_conflict_ids,
            candidate_lint_report=candidate_lint_report,
        )
    synthesis_input_SHA256 = _synthesis_input_digest(request)
    disposition = _disposition_for_conflicts(
        tuple(conflicts), candidate, eligible_SHA256s
    )
    review_SHA256 = _review_digest(
        schema_version=MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION,
        project_id=request.generation_request.ticket_spec.project_id,
        ticket_id=request.generation_request.ticket_spec.ticket_id,
        synthesis_input_SHA256=synthesis_input_SHA256,
        proposal_SHA256s=proposal_SHA256s,
        eligible_proposal_SHA256s=eligible_SHA256s,
        excluded_proposal_SHA256s=excluded_SHA256s,
        field_decisions=field_decisions,
        conflicts=tuple(conflicts),
        candidate=candidate,
        disposition=disposition,
    )
    return TicketSynthesisReview(
        project_id=request.generation_request.ticket_spec.project_id,
        ticket_id=request.generation_request.ticket_spec.ticket_id,
        synthesis_input_SHA256=synthesis_input_SHA256,
        proposal_SHA256s=proposal_SHA256s,
        eligible_proposal_SHA256s=eligible_SHA256s,
        excluded_proposal_SHA256s=excluded_SHA256s,
        field_decisions=field_decisions,
        conflicts=tuple(conflicts),
        candidate=candidate,
        disposition=disposition,
        review_SHA256=review_SHA256,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _role_sort_key(role: TicketGeneratorRole) -> int:
    return _ROLE_RANK[role]


def _ticket_sort_key(
    ticket_id: str,
) -> tuple[int, tuple[tuple[tuple[int, int | str], ...], ...]]:
    parts = ticket_id.split(".")
    project_number = int(parts[0][1:]) if parts and parts[0].startswith("P") else 0
    segment_keys: list[tuple[tuple[int, int | str], ...]] = []
    for segment in parts[1:]:
        tokens: list[tuple[int, int | str]] = []
        index = 0
        while index < len(segment):
            start = index
            is_digit = segment[index].isdigit()
            while index < len(segment) and segment[index].isdigit() is is_digit:
                index += 1
            token = segment[start:index]
            tokens.append((0, int(token)) if is_digit else (1, token))
        segment_keys.append(tuple(tokens))
    return (project_number, tuple(segment_keys))


def _candidate_id(ticket_id: str) -> str:
    return f"CAND-{ticket_id.replace('.', '-')}"


def _conflict_id(index: int) -> str:
    return f"CONFLICT-{index:04d}"


def _field_value(ticket: TicketSpec, field: TicketSynthesisField) -> object:
    return ticket.model_dump(mode="json")[field.value]


def _field_value_digest(value: object) -> str:
    return _sha256_text(_deterministic_json(value))


def _proposal_sort_key(reviewed: ReviewedTicketProposal) -> tuple[object, ...]:
    return (
        _role_sort_key(reviewed.proposal.role),
        reviewed.proposal.assignment_id,
        reviewed.proposal.proposal_SHA256,
    )


def _assignment_sort_key(assignment: GeneratorAssignment) -> tuple[object, ...]:
    return (_role_sort_key(assignment.role), assignment.assignment_id)


def _canonical_reviewed_proposals(
    reviewed: tuple[ReviewedTicketProposal, ...],
) -> tuple[ReviewedTicketProposal, ...]:
    return tuple(sorted(reviewed, key=_proposal_sort_key))


def _canonical_assignments(
    assignments: tuple[GeneratorAssignment, ...],
) -> tuple[GeneratorAssignment, ...]:
    return tuple(sorted(assignments, key=_assignment_sort_key))


def _variant_sort_key(variant: ProposalVariantEvidence) -> tuple[object, ...]:
    return (-variant.support_count, variant.variant_SHA256)


def _decision_sort_key(decision: FieldSynthesisDecision) -> tuple[object, ...]:
    return (_FIELD_RANK[decision.field], _AGREEMENT_RANK[decision.agreement_level])


def _conflict_sort_key(conflict: ProposalConflict) -> tuple[object, ...]:
    return (
        _CONFLICT_SEVERITY_RANK[conflict.severity],
        _CONFLICT_KIND_RANK[conflict.kind],
        0 if conflict.field is None else 1,
        -1 if conflict.field is None else _FIELD_RANK[conflict.field],
        "" if conflict.proposal_SHA256 is None else conflict.proposal_SHA256,
        conflict.related_proposal_SHA256s,
        conflict.message,
    )


def _validate_lint_report_binding(
    proposal: TicketProposal,
    lint_report: TicketLintReport,
    *,
    error_type: type[Exception],
) -> None:
    try:
        TicketLintReport.model_validate(lint_report.model_dump(mode="json"))
    except ValueError as exc:
        raise error_type(
            "lint report digest evidence is invalid: "
            f"report_SHA256={lint_report.report_SHA256}"
        ) from exc
    if lint_report.project_id != proposal.project_id:
        raise error_type(
            "lint report project_id must match proposal: "
            f"project_id={proposal.project_id}"
        )
    if len(lint_report.ticket_ids) != 1:
        raise error_type("lint report must cover exactly one proposal ticket")
    if lint_report.ticket_ids[0] != proposal.ticket_id:
        raise error_type(
            f"lint report ticket_id must match proposal: ticket_id={proposal.ticket_id}"
        )


def _validate_synthesis_request(
    request: TicketSynthesisRequest,
    *,
    input_error_type: type[Exception],
    validation_error_type: type[Exception],
) -> None:
    expected_assignments = prepare_ticket_generator_assignments(
        request.generation_request
    )
    expected_by_id = {
        assignment.assignment_id: assignment for assignment in expected_assignments
    }
    assignment_ids = tuple(
        assignment.assignment_id for assignment in request.assignments
    )
    if len(assignment_ids) != len(frozenset(assignment_ids)):
        raise input_error_type("assignment IDs must be unique")
    assignment_roles = tuple(assignment.role for assignment in request.assignments)
    if len(assignment_roles) != len(frozenset(assignment_roles)):
        raise input_error_type("assignment roles must be unique")
    if frozenset(assignment_ids) != frozenset(expected_by_id):
        raise input_error_type("assignments must match generation request exactly")
    for assignment in request.assignments:
        if assignment != expected_by_id[assignment.assignment_id]:
            raise input_error_type(
                "assignment must match generation request digest: "
                f"assignment_id={assignment.assignment_id}"
            )
    proposal_ids = tuple(
        item.proposal.proposal_SHA256 for item in request.reviewed_proposals
    )
    if len(proposal_ids) != len(frozenset(proposal_ids)):
        raise input_error_type("proposal SHA-256 values must be unique")
    proposal_assignment_ids = tuple(
        item.proposal.assignment_id for item in request.reviewed_proposals
    )
    if frozenset(proposal_assignment_ids) != frozenset(assignment_ids):
        raise input_error_type("reviewed proposals must match assignments one-to-one")
    if len(proposal_assignment_ids) != len(frozenset(proposal_assignment_ids)):
        raise input_error_type("each assignment may have only one proposal")
    for item in request.reviewed_proposals:
        try:
            validate_ticket_generator_proposal(
                request.generation_request, item.proposal
            )
        except TicketProposalValidationError as exc:
            raise validation_error_type(
                "proposal validation failed: "
                f"assignment_id={item.proposal.assignment_id}"
            ) from exc
        _validate_lint_report_binding(
            item.proposal,
            item.lint_report,
            error_type=validation_error_type,
        )
    if request.dependency_plan is not None:
        seed = request.generation_request.ticket_spec
        if request.dependency_plan.project_id != seed.project_id:
            raise input_error_type(
                "dependency plan project_id must match request: "
                f"project_id={seed.project_id}"
            )
        if seed.ticket_id not in request.dependency_plan.ticket_ids:
            raise input_error_type(
                f"dependency plan must contain seed ticket: ticket_id={seed.ticket_id}"
            )


def _validate_candidate_lint_report(
    project_id: str,
    ticket_id: str,
    lint_report: TicketLintReport,
    *,
    error_type: type[Exception],
) -> None:
    try:
        TicketLintReport.model_validate(lint_report.model_dump(mode="json"))
    except ValueError as exc:
        raise error_type(
            "candidate lint report digest evidence is invalid: "
            f"report_SHA256={lint_report.report_SHA256}"
        ) from exc
    if lint_report.project_id != project_id:
        raise error_type("candidate lint report project_id must match candidate")
    if lint_report.ticket_ids != (ticket_id,):
        raise error_type(
            "candidate lint report must cover exactly the candidate ticket"
        )


def _validate_complete_field_decisions(
    decisions: tuple[FieldSynthesisDecision, ...],
) -> None:
    fields = tuple(decision.field for decision in decisions)
    if len(fields) != len(frozenset(fields)):
        raise ValueError("field decisions must not contain duplicate fields")
    if fields != _SYNTHESIS_FIELDS:
        raise ValueError("field decisions must cover all synthesis fields in order")


def _base_conflict(
    *,
    kind: ProposalConflictKind,
    severity: ProposalConflictSeverity,
    field: TicketSynthesisField | None,
    proposal_SHA256: str | None,
    related_proposal_SHA256s: tuple[str, ...] = (),
    message: str,
    remediation: str,
) -> ProposalConflict:
    return ProposalConflict(
        conflict_id="CONFLICT-0001",
        kind=kind,
        severity=severity,
        field=field,
        proposal_SHA256=proposal_SHA256,
        related_proposal_SHA256s=related_proposal_SHA256s,
        message=message,
        remediation=remediation,
        blocking=severity is ProposalConflictSeverity.BLOCKING,
    )


def _assign_conflict_ids(
    conflicts: tuple[ProposalConflict, ...],
) -> tuple[ProposalConflict, ...]:
    return tuple(
        conflict.model_copy(update={"conflict_id": _conflict_id(index)})
        for index, conflict in enumerate(
            sorted(conflicts, key=_conflict_sort_key), start=1
        )
    )


def _lint_blocked_conflicts(
    excluded: tuple[ReviewedTicketProposal, ...],
) -> tuple[ProposalConflict, ...]:
    return tuple(
        _base_conflict(
            kind=ProposalConflictKind.LINT_BLOCKED_PROPOSAL,
            severity=ProposalConflictSeverity.WARNING,
            field=None,
            proposal_SHA256=item.proposal.proposal_SHA256,
            message=(
                "Proposal is excluded from voting by lint report: "
                f"proposal_SHA256={item.proposal.proposal_SHA256}; "
                f"role={item.proposal.role.value}; "
                f"lint_report_SHA256={item.lint_report.report_SHA256}"
            ),
            remediation="Review lint diagnostics before considering this proposal.",
        )
        for item in excluded
    )


def _insufficient_eligible_conflict(eligible_count: int) -> ProposalConflict:
    return _base_conflict(
        kind=ProposalConflictKind.INSUFFICIENT_ELIGIBLE_PROPOSALS,
        severity=ProposalConflictSeverity.BLOCKING,
        field=None,
        proposal_SHA256=None,
        message=(
            "At least two lint-eligible proposals are required: "
            f"eligible_proposal_count={eligible_count}"
        ),
        remediation="Collect at least two non-blocked independent proposals.",
    )


def _candidate_lint_blocked_conflict(lint_report: TicketLintReport) -> ProposalConflict:
    return _base_conflict(
        kind=ProposalConflictKind.CANDIDATE_LINT_BLOCKED,
        severity=ProposalConflictSeverity.BLOCKING,
        field=None,
        proposal_SHA256=None,
        message=(
            "Synthesized candidate lint report is blocked: "
            f"lint_report_SHA256={lint_report.report_SHA256}"
        ),
        remediation="Resolve candidate lint errors before downstream review.",
    )


def _field_decisions(
    seed: TicketSpec, eligible: tuple[ReviewedTicketProposal, ...]
) -> tuple[
    tuple[FieldSynthesisDecision, ...],
    tuple[ProposalConflict, ...],
    dict[TicketSynthesisField, object],
]:
    decisions: list[FieldSynthesisDecision] = []
    conflicts: list[ProposalConflict] = []
    selected_values: dict[TicketSynthesisField, object] = {}
    eligible_count = len(eligible)
    for field in _SYNTHESIS_FIELDS:
        seed_value = _field_value(seed, field)
        seed_digest = _field_value_digest(seed_value)
        variants: dict[str, dict[str, object]] = {}
        for item in eligible:
            value = _field_value(item.proposal.proposed_ticket, field)
            digest = _field_value_digest(value)
            variant = variants.setdefault(
                digest,
                {"value": value, "items": []},
            )
            variant_items = variant["items"]
            if isinstance(variant_items, list):
                variant_items.append(item)
        variant_evidence = tuple(
            sorted(
                (
                    ProposalVariantEvidence(
                        variant_SHA256=digest,
                        support_count=len(data["items"]),
                        supporting_proposal_SHA256s=tuple(
                            item.proposal.proposal_SHA256 for item in data["items"]
                        ),
                        supporting_roles=tuple(
                            item.proposal.role for item in data["items"]
                        ),
                    )
                    for digest, data in variants.items()
                ),
                key=_variant_sort_key,
            )
        )
        selected_variant = variant_evidence[0]
        if len(variant_evidence) == 1:
            agreement = ProposalAgreementLevel.UNANIMOUS
            resolution = FieldResolutionKind.ADOPT_UNANIMOUS
            selected_digest = selected_variant.variant_SHA256
            supporting = selected_variant.supporting_proposal_SHA256s
            dissenting: tuple[str, ...] = ()
            selected_values[field] = variants[selected_digest]["value"]
        elif selected_variant.support_count > eligible_count / 2:
            agreement = ProposalAgreementLevel.STRICT_MAJORITY
            resolution = FieldResolutionKind.ADOPT_STRICT_MAJORITY
            selected_digest = selected_variant.variant_SHA256
            supporting = selected_variant.supporting_proposal_SHA256s
            supporting_set = frozenset(supporting)
            dissenting = tuple(
                item.proposal.proposal_SHA256
                for item in eligible
                if item.proposal.proposal_SHA256 not in supporting_set
            )
            selected_values[field] = variants[selected_digest]["value"]
            conflicts.append(
                _base_conflict(
                    kind=ProposalConflictKind.FIELD_DISSENT,
                    severity=ProposalConflictSeverity.WARNING,
                    field=field,
                    proposal_SHA256=supporting[0],
                    related_proposal_SHA256s=dissenting,
                    message=f"Field has strict-majority dissent: field={field.value}",
                    remediation="Preserve dissent for human review before downstream review.",
                )
            )
        else:
            agreement = ProposalAgreementLevel.SPLIT
            resolution = FieldResolutionKind.PRESERVE_SEED
            selected_digest = seed_digest
            supporting = ()
            dissenting = tuple(item.proposal.proposal_SHA256 for item in eligible)
            selected_values[field] = seed_value
            conflicts.append(
                _base_conflict(
                    kind=ProposalConflictKind.FIELD_SPLIT,
                    severity=ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED,
                    field=field,
                    proposal_SHA256=None,
                    related_proposal_SHA256s=dissenting,
                    message=f"Field has no strict majority: field={field.value}",
                    remediation="Resolve the split field manually before downstream review.",
                )
            )
        decisions.append(
            FieldSynthesisDecision(
                field=field,
                agreement_level=agreement,
                resolution=resolution,
                seed_value_SHA256=seed_digest,
                selected_value_SHA256=selected_digest,
                variants=variant_evidence,
                supporting_proposal_SHA256s=supporting,
                dissenting_proposal_SHA256s=dissenting,
            )
        )
    return (tuple(decisions), tuple(conflicts), selected_values)


def _synthesized_ticket(
    seed: TicketSpec, selected_values: dict[TicketSynthesisField, object]
) -> TicketSpec:
    data = seed.model_dump(mode="json")
    for field, value in selected_values.items():
        data[field.value] = value
    return TicketSpec.model_validate(data)


def _plan_staleness_conflicts(
    seed: TicketSpec,
    synthesized_ticket: TicketSpec,
    dependency_plan: TicketDependencyPlan | None,
) -> tuple[ProposalConflict, ...]:
    if dependency_plan is None:
        return ()
    conflicts: list[ProposalConflict] = []
    if seed.dependencies != synthesized_ticket.dependencies:
        conflicts.append(
            _base_conflict(
                kind=ProposalConflictKind.DEPENDENCY_PLAN_STALE,
                severity=ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED,
                field=TicketSynthesisField.DEPENDENCIES,
                proposal_SHA256=None,
                message=(
                    "The supplied dependency plan was built from earlier dependency "
                    "declarations and must be rebuilt before relying on its graph or waves."
                ),
                remediation="Rebuild dependency planning evidence outside P16.5.",
            )
        )
    if seed.scope != synthesized_ticket.scope:
        conflicts.append(
            _base_conflict(
                kind=ProposalConflictKind.SCOPE_PLAN_STALE,
                severity=ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED,
                field=TicketSynthesisField.SCOPE,
                proposal_SHA256=None,
                message=(
                    "The supplied scope-collision and wave evidence may no longer "
                    "describe the synthesized candidate."
                ),
                remediation="Rebuild scope and wave evidence outside P16.5.",
            )
        )
    return tuple(conflicts)


def _make_candidate(
    *,
    synthesized_ticket: TicketSpec,
    source_proposal_SHA256s: tuple[str, ...],
    excluded_proposal_SHA256s: tuple[str, ...],
    field_decisions: tuple[FieldSynthesisDecision, ...],
    unresolved_conflict_ids: tuple[str, ...],
    candidate_lint_report: TicketLintReport,
) -> SynthesizedTicketCandidate:
    candidate_id = _candidate_id(synthesized_ticket.ticket_id)
    candidate_SHA256 = _candidate_digest(
        schema_version=MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION,
        candidate_id=candidate_id,
        project_id=synthesized_ticket.project_id,
        ticket_id=synthesized_ticket.ticket_id,
        synthesized_ticket=synthesized_ticket,
        source_proposal_SHA256s=source_proposal_SHA256s,
        excluded_proposal_SHA256s=excluded_proposal_SHA256s,
        field_decisions=field_decisions,
        unresolved_conflict_ids=unresolved_conflict_ids,
        candidate_lint_report=candidate_lint_report,
    )
    return SynthesizedTicketCandidate(
        candidate_id=candidate_id,
        project_id=synthesized_ticket.project_id,
        ticket_id=synthesized_ticket.ticket_id,
        synthesized_ticket=synthesized_ticket,
        source_proposal_SHA256s=source_proposal_SHA256s,
        excluded_proposal_SHA256s=excluded_proposal_SHA256s,
        field_decisions=field_decisions,
        unresolved_conflict_ids=unresolved_conflict_ids,
        candidate_lint_report=candidate_lint_report,
        candidate_SHA256=candidate_SHA256,
    )


def _disposition_for_conflicts(
    conflicts: tuple[ProposalConflict, ...],
    candidate: SynthesizedTicketCandidate | None,
    eligible_proposal_SHA256s: tuple[str, ...],
) -> TicketSynthesisDisposition:
    if len(eligible_proposal_SHA256s) < 2 or candidate is None:
        return TicketSynthesisDisposition.BLOCKED
    if any(conflict.blocking for conflict in conflicts):
        return TicketSynthesisDisposition.BLOCKED
    if any(
        conflict.severity is ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED
        for conflict in conflicts
    ):
        return TicketSynthesisDisposition.HUMAN_RESOLUTION_REQUIRED
    if any(
        conflict.kind
        in {
            ProposalConflictKind.FIELD_DISSENT,
            ProposalConflictKind.LINT_BLOCKED_PROPOSAL,
        }
        for conflict in conflicts
    ):
        return TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT
    return TicketSynthesisDisposition.REVIEW_READY


def _synthesis_input_digest(request: TicketSynthesisRequest) -> str:
    record = {
        "algorithm": SYNTHESIS_INPUT_DIGEST_ALGORITHM,
        "generation_request": request.generation_request.model_dump(mode="json"),
        "assignments": [
            assignment.model_dump(mode="json")
            for assignment in _canonical_assignments(request.assignments)
        ],
        "reviewed_proposals": [
            reviewed.model_dump(mode="json")
            for reviewed in _canonical_reviewed_proposals(request.reviewed_proposals)
        ],
        "dependency_plan": (
            None
            if request.dependency_plan is None
            else request.dependency_plan.model_dump(mode="json")
        ),
    }
    return _sha256_text(_deterministic_json(record))


def _candidate_digest(
    *,
    schema_version: int,
    candidate_id: str,
    project_id: str,
    ticket_id: str,
    synthesized_ticket: TicketSpec,
    source_proposal_SHA256s: tuple[str, ...],
    excluded_proposal_SHA256s: tuple[str, ...],
    field_decisions: tuple[FieldSynthesisDecision, ...],
    unresolved_conflict_ids: tuple[str, ...],
    candidate_lint_report: TicketLintReport,
) -> str:
    record = {
        "algorithm": SYNTHESIZED_TICKET_CANDIDATE_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "candidate_id": candidate_id,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "synthesized_ticket": synthesized_ticket.model_dump(mode="json"),
        "source_proposal_SHA256s": list(source_proposal_SHA256s),
        "excluded_proposal_SHA256s": list(excluded_proposal_SHA256s),
        "field_decisions": [
            decision.model_dump(mode="json") for decision in field_decisions
        ],
        "unresolved_conflict_ids": list(unresolved_conflict_ids),
        "candidate_lint_report": candidate_lint_report.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _review_digest(
    *,
    schema_version: int,
    project_id: str,
    ticket_id: str,
    synthesis_input_SHA256: str,
    proposal_SHA256s: tuple[str, ...],
    eligible_proposal_SHA256s: tuple[str, ...],
    excluded_proposal_SHA256s: tuple[str, ...],
    field_decisions: tuple[FieldSynthesisDecision, ...],
    conflicts: tuple[ProposalConflict, ...],
    candidate: SynthesizedTicketCandidate | None,
    disposition: TicketSynthesisDisposition,
) -> str:
    record = {
        "algorithm": SYNTHESIS_REVIEW_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "synthesis_input_SHA256": synthesis_input_SHA256,
        "proposal_SHA256s": list(proposal_SHA256s),
        "eligible_proposal_SHA256s": list(eligible_proposal_SHA256s),
        "excluded_proposal_SHA256s": list(excluded_proposal_SHA256s),
        "field_decisions": [
            decision.model_dump(mode="json") for decision in field_decisions
        ],
        "conflicts": [conflict.model_dump(mode="json") for conflict in conflicts],
        "candidate": None if candidate is None else candidate.model_dump(mode="json"),
        "disposition": disposition.value,
    }
    return _sha256_text(_deterministic_json(record))
