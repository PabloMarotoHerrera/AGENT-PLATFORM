"""Non-executing ticket-generator role contracts for Pepper planning specs."""

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

from hermes_cli.agent_platform.ticket_factory.context_packs import ContextPack
from hermes_cli.agent_platform.ticket_factory.specs import (
    ProjectIdentifier as _ProjectIdentifier,
    ProjectSpec,
    TicketSpec,
    TicketType,
    _ticket_id_matches_project,
)

TICKET_GENERATOR_ROLE_SCHEMA_VERSION = 1
GENERATOR_INPUT_DIGEST_ALGORITHM = "agent-platform-ticket-generator-input-sha256-v1"
GENERATOR_ASSIGNMENT_DIGEST_ALGORITHM = (
    "agent-platform-ticket-generator-assignment-sha256-v1"
)
TICKET_PROPOSAL_DIGEST_ALGORITHM = "agent-platform-ticket-proposal-sha256-v1"


class TicketGeneratorRoleError(ValueError):
    """Base error for bounded ticket-generator role contract failures."""


class TicketGeneratorCompatibilityError(TicketGeneratorRoleError):
    """Raised when requested roles are incompatible with a ticket type."""


class TicketProposalValidationError(TicketGeneratorRoleError):
    """Raised when an independent proposal does not bind to its request."""


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
LongText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=8192),
    AfterValidator(_reject_nul),
]
ProjectIdentifier: TypeAlias = _ProjectIdentifier
TicketIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=4,
        max_length=64,
        pattern=r"^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$",
    ),
]
ContextSourceIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=5,
        max_length=96,
        pattern=r"^CTX-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    ),
]
AssignmentIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=12,
        max_length=128,
        pattern=(
            r"^GEN-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-"
            r"(?:ARCHITECTURE|IMPLEMENTATION|VALIDATION|INTEGRATION|"
            r"GOVERNANCE|DOCUMENTATION)$"
        ),
    ),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]


class TicketGeneratorRole(str, Enum):
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    VALIDATION = "validation"
    INTEGRATION = "integration"
    GOVERNANCE = "governance"
    DOCUMENTATION = "documentation"


class _TicketGeneratorModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


class GeneratorRoleProfile(_TicketGeneratorModel):
    role: TicketGeneratorRole
    title: ShortText
    objective: LongText
    focus_areas: tuple[ShortText, ...] = Field(min_length=1)
    required_checks: tuple[ShortText, ...] = Field(min_length=1)
    prohibited_claims: tuple[ShortText, ...] = Field(min_length=1)
    primary_ticket_types: tuple[TicketType, ...] = Field(min_length=1)
    supported_ticket_types: tuple[TicketType, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_profile(self) -> GeneratorRoleProfile:
        _reject_duplicate_values(self.focus_areas, "focus_areas")
        _reject_duplicate_values(self.required_checks, "required_checks")
        _reject_duplicate_values(self.prohibited_claims, "prohibited_claims")
        _reject_duplicate_values(self.primary_ticket_types, "primary_ticket_types")
        _reject_duplicate_values(self.supported_ticket_types, "supported_ticket_types")
        if not frozenset(self.primary_ticket_types).issubset(
            self.supported_ticket_types
        ):
            raise ValueError(
                "primary_ticket_types must be a subset of supported_ticket_types"
            )
        return self


class TicketGenerationRequest(_TicketGeneratorModel):
    project_spec: ProjectSpec
    ticket_spec: TicketSpec
    context_pack: ContextPack
    roles: tuple[TicketGeneratorRole, ...] = Field(min_length=1, max_length=6)

    @model_validator(mode="after")
    def _validate_request(self) -> TicketGenerationRequest:
        if self.project_spec.project_id != self.ticket_spec.project_id:
            raise ValueError(
                "project_spec and ticket_spec project identifiers must match"
            )
        if self.context_pack.project_id != self.ticket_spec.project_id:
            raise ValueError(
                "context_pack project_id must match ticket_spec project_id"
            )
        if self.context_pack.ticket_id != self.ticket_spec.ticket_id:
            raise ValueError("context_pack ticket_id must match ticket_spec ticket_id")
        _reject_duplicate_values(self.roles, "roles")
        _validate_role_compatibility(self.roles, self.ticket_spec.ticket_type)
        return self


class GeneratorAssignment(_TicketGeneratorModel):
    schema_version: Literal[1] = TICKET_GENERATOR_ROLE_SCHEMA_VERSION
    assignment_id: AssignmentIdentifier
    role: TicketGeneratorRole
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    ticket_type: TicketType
    input_SHA256: DigestText
    role_profile: GeneratorRoleProfile
    assignment_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_assignment(self) -> GeneratorAssignment:
        if not _ticket_id_matches_project(self.project_id, self.ticket_id):
            raise ValueError("ticket_id must use the project_id prefix")
        if self.assignment_id != _assignment_id(self.ticket_id, self.role):
            raise ValueError("assignment_id must match ticket_id and role")
        if self.role_profile != get_ticket_generator_role_profile(self.role):
            raise ValueError("role_profile must match canonical role profile")
        if self.ticket_type not in self.role_profile.supported_ticket_types:
            raise ValueError("role_profile must support ticket_type")
        if self.assignment_SHA256 != _assignment_digest(
            schema_version=self.schema_version,
            assignment_id=self.assignment_id,
            role=self.role,
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            ticket_type=self.ticket_type,
            input_SHA256=self.input_SHA256,
            role_profile=self.role_profile,
        ):
            raise ValueError("assignment_SHA256 must match assignment digest record")
        return self


class TicketProposal(_TicketGeneratorModel):
    schema_version: Literal[1] = TICKET_GENERATOR_ROLE_SCHEMA_VERSION
    assignment_id: AssignmentIdentifier
    assignment_SHA256: DigestText
    role: TicketGeneratorRole
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    proposed_ticket: TicketSpec
    rationale: LongText
    evidence_source_ids: tuple[ContextSourceIdentifier, ...] = Field(min_length=1)
    assumptions: tuple[ShortText, ...] = ()
    risks: tuple[ShortText, ...] = ()
    unresolved_questions: tuple[ShortText, ...] = ()
    proposal_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_proposal(self) -> TicketProposal:
        if not _ticket_id_matches_project(self.project_id, self.ticket_id):
            raise ValueError("ticket_id must use the project_id prefix")
        if self.proposed_ticket.project_id != self.project_id:
            raise ValueError(
                "proposed_ticket project_id must match proposal project_id"
            )
        if self.proposed_ticket.ticket_id != self.ticket_id:
            raise ValueError("proposed_ticket ticket_id must match proposal ticket_id")
        if (
            self.proposed_ticket.ticket_type
            not in get_ticket_generator_role_profile(self.role).supported_ticket_types
        ):
            raise ValueError("proposal role must support proposed ticket type")
        _reject_duplicate_values(self.evidence_source_ids, "evidence_source_ids")
        _reject_duplicate_values(self.assumptions, "assumptions")
        _reject_duplicate_values(self.risks, "risks")
        _reject_duplicate_values(self.unresolved_questions, "unresolved_questions")
        if self.proposal_SHA256 != _proposal_digest(
            schema_version=self.schema_version,
            assignment_id=self.assignment_id,
            assignment_SHA256=self.assignment_SHA256,
            role=self.role,
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            proposed_ticket=self.proposed_ticket,
            rationale=self.rationale,
            evidence_source_ids=self.evidence_source_ids,
            assumptions=self.assumptions,
            risks=self.risks,
            unresolved_questions=self.unresolved_questions,
        ):
            raise ValueError("proposal_SHA256 must match proposal digest record")
        return self


_CANONICAL_ROLE_ORDER = (
    TicketGeneratorRole.ARCHITECTURE,
    TicketGeneratorRole.IMPLEMENTATION,
    TicketGeneratorRole.VALIDATION,
    TicketGeneratorRole.INTEGRATION,
    TicketGeneratorRole.GOVERNANCE,
    TicketGeneratorRole.DOCUMENTATION,
)
_ROLE_RANK = {role: index for index, role in enumerate(_CANONICAL_ROLE_ORDER)}


_ROLE_PROFILES = (
    GeneratorRoleProfile(
        role=TicketGeneratorRole.ARCHITECTURE,
        title="Architecture ticket generator role",
        objective=(
            "Assess planning contracts, ownership and authority boundaries for an "
            "externally supplied ticket proposal."
        ),
        focus_areas=(
            "contract boundaries",
            "module ownership",
            "dependency direction",
            "authority separation",
            "deferred behavior",
            "rollback architecture",
        ),
        required_checks=(
            "Verify each proposed boundary is represented by explicit contract text.",
            "Verify deferred behavior is assigned to a later authorized ticket.",
            "Verify rollback posture is stated without execution claims.",
        ),
        prohibited_claims=(
            "implementation completed without evidence",
            "runtime readiness without runtime validation",
            "canonical approval authority",
        ),
        primary_ticket_types=(TicketType.ARCHITECTURE, TicketType.REFACTOR),
        supported_ticket_types=(
            TicketType.ARCHITECTURE,
            TicketType.DOCUMENTATION,
            TicketType.IMPLEMENTATION,
            TicketType.REFACTOR,
            TicketType.INTEGRATION,
        ),
    ),
    GeneratorRoleProfile(
        role=TicketGeneratorRole.IMPLEMENTATION,
        title="Implementation ticket generator role",
        objective=(
            "Assess code-scope, compatibility and failure-behavior evidence for an "
            "externally supplied ticket proposal."
        ),
        focus_areas=(
            "exact code scope",
            "public contracts",
            "failure behavior",
            "compatibility",
            "testability",
            "rollback",
        ),
        required_checks=(
            "Verify proposed code scope remains inside the TicketSpec boundary.",
            "Verify public contract and failure behavior are explicitly covered.",
            "Verify validation evidence is described without claiming unrun tests.",
        ),
        prohibited_claims=(
            "tests passed when not run",
            "production readiness",
            "scope outside the TicketSpec",
        ),
        primary_ticket_types=(TicketType.IMPLEMENTATION, TicketType.BUGFIX),
        supported_ticket_types=(
            TicketType.IMPLEMENTATION,
            TicketType.REFACTOR,
            TicketType.TEST,
            TicketType.BUGFIX,
            TicketType.INTEGRATION,
        ),
    ),
    GeneratorRoleProfile(
        role=TicketGeneratorRole.VALIDATION,
        title="Validation ticket generator role",
        objective=(
            "Assess acceptance, negative-case and regression evidence for an "
            "externally supplied ticket proposal."
        ),
        focus_areas=(
            "acceptance criteria",
            "negative cases",
            "boundary cases",
            "regression coverage",
            "deterministic evidence",
            "failure diagnostics",
        ),
        required_checks=(
            "Verify acceptance criteria map to validation evidence.",
            "Verify negative and boundary cases are considered where applicable.",
            "Verify diagnostics remain deterministic and bounded.",
        ),
        prohibited_claims=(
            "feature correctness without evidence",
            "coverage completeness without measurement",
            "human approval",
        ),
        primary_ticket_types=(TicketType.TEST,),
        supported_ticket_types=(
            TicketType.IMPLEMENTATION,
            TicketType.TEST,
            TicketType.BUGFIX,
            TicketType.INTEGRATION,
            TicketType.CLOSURE,
        ),
    ),
    GeneratorRoleProfile(
        role=TicketGeneratorRole.INTEGRATION,
        title="Integration ticket generator role",
        objective=(
            "Assess cross-module compatibility and sequencing evidence for an "
            "externally supplied ticket proposal."
        ),
        focus_areas=(
            "cross-module contracts",
            "compatibility boundaries",
            "integration sequencing",
            "failure isolation",
            "rollback",
            "end-to-end evidence",
        ),
        required_checks=(
            "Verify cross-module contracts identify both sides of the seam.",
            "Verify sequencing does not imply scheduler or parallel execution authority.",
            "Verify rollback and failure isolation are explicit.",
        ),
        prohibited_claims=(
            "upstream compatibility without validation",
            "downstream readiness without evidence",
            "automatic publication authority",
        ),
        primary_ticket_types=(TicketType.INTEGRATION,),
        supported_ticket_types=(
            TicketType.ARCHITECTURE,
            TicketType.IMPLEMENTATION,
            TicketType.TEST,
            TicketType.INTEGRATION,
            TicketType.CLOSURE,
        ),
    ),
    GeneratorRoleProfile(
        role=TicketGeneratorRole.GOVERNANCE,
        title="Governance ticket generator role",
        objective=(
            "Assess authority, scope and residual-constraint evidence for an "
            "externally supplied ticket proposal."
        ),
        focus_areas=(
            "authority",
            "scope compliance",
            "evidence sufficiency",
            "security boundaries",
            "approval boundaries",
            "residual constraints",
        ),
        required_checks=(
            "Verify the proposal cites authority without self-approval.",
            "Verify security and approval boundaries remain deferred where required.",
            "Verify residual constraints are explicit and bounded.",
        ),
        prohibited_claims=(
            "self-approval",
            "merge authorization",
            "production readiness without authority",
        ),
        primary_ticket_types=(TicketType.CLOSURE,),
        supported_ticket_types=(
            TicketType.ARCHITECTURE,
            TicketType.DOCUMENTATION,
            TicketType.TEST,
            TicketType.INTEGRATION,
            TicketType.CLOSURE,
        ),
    ),
    GeneratorRoleProfile(
        role=TicketGeneratorRole.DOCUMENTATION,
        title="Documentation ticket generator role",
        objective=(
            "Assess terminology, examples and operator handoff evidence for an "
            "externally supplied ticket proposal."
        ),
        focus_areas=(
            "terminology consistency",
            "public contract explanation",
            "examples",
            "limitations",
            "deferred behavior",
            "operator handoff",
        ),
        required_checks=(
            "Verify terminology matches the public contract names.",
            "Verify examples are synthetic and do not imply execution authority.",
            "Verify limitations and deferred behavior are explicitly documented.",
        ),
        prohibited_claims=(
            "undocumented implementation assumptions",
            "runtime behavior not present in code",
            "canonical policy authority",
        ),
        primary_ticket_types=(TicketType.DOCUMENTATION,),
        supported_ticket_types=(
            TicketType.ARCHITECTURE,
            TicketType.DOCUMENTATION,
            TicketType.INTEGRATION,
            TicketType.CLOSURE,
        ),
    ),
)
_ROLE_PROFILE_BY_ROLE = {profile.role: profile for profile in _ROLE_PROFILES}


def _coerce_role(role: TicketGeneratorRole) -> TicketGeneratorRole:
    return TicketGeneratorRole(role)


def get_ticket_generator_role_profile(
    role: TicketGeneratorRole,
) -> GeneratorRoleProfile:
    """Return the immutable canonical profile for one generator role."""

    return _ROLE_PROFILE_BY_ROLE[_coerce_role(role)]


def list_ticket_generator_role_profiles() -> tuple[GeneratorRoleProfile, ...]:
    """Return all canonical role profiles in canonical role order."""

    return _ROLE_PROFILES


def _validate_role_compatibility(
    roles: tuple[TicketGeneratorRole, ...], ticket_type: TicketType
) -> None:
    unsupported = tuple(
        role
        for role in roles
        if ticket_type
        not in get_ticket_generator_role_profile(role).supported_ticket_types
    )
    if unsupported:
        raise TicketGeneratorCompatibilityError(
            "role does not support ticket_type: "
            f"role={unsupported[0].value}; ticket_type={ticket_type.value}"
        )
    if not any(
        ticket_type in get_ticket_generator_role_profile(role).primary_ticket_types
        for role in roles
    ):
        raise TicketGeneratorCompatibilityError(
            "at least one requested role must be primary for ticket_type: "
            f"ticket_type={ticket_type.value}"
        )


def _generator_input_digest(request: TicketGenerationRequest) -> str:
    record = {
        "algorithm": GENERATOR_INPUT_DIGEST_ALGORITHM,
        "project_spec": request.project_spec.model_dump(mode="json"),
        "ticket_spec": request.ticket_spec.model_dump(mode="json"),
        "context_pack": request.context_pack.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _assignment_id(ticket_id: str, role: TicketGeneratorRole) -> str:
    return f"GEN-{ticket_id.replace('.', '-')}-{role.value.upper().replace('_', '-')}"


def _assignment_digest(
    *,
    schema_version: int,
    assignment_id: str,
    role: TicketGeneratorRole,
    project_id: str,
    ticket_id: str,
    ticket_type: TicketType,
    input_SHA256: str,
    role_profile: GeneratorRoleProfile,
) -> str:
    record = {
        "algorithm": GENERATOR_ASSIGNMENT_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "assignment_id": assignment_id,
        "role": role.value,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "ticket_type": ticket_type.value,
        "input_SHA256": input_SHA256,
        "role_profile": role_profile.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _make_assignment(
    request: TicketGenerationRequest, role: TicketGeneratorRole, input_SHA256: str
) -> GeneratorAssignment:
    profile = get_ticket_generator_role_profile(role)
    assignment_id = _assignment_id(request.ticket_spec.ticket_id, role)
    digest = _assignment_digest(
        schema_version=TICKET_GENERATOR_ROLE_SCHEMA_VERSION,
        assignment_id=assignment_id,
        role=role,
        project_id=request.ticket_spec.project_id,
        ticket_id=request.ticket_spec.ticket_id,
        ticket_type=request.ticket_spec.ticket_type,
        input_SHA256=input_SHA256,
        role_profile=profile,
    )
    return GeneratorAssignment(
        assignment_id=assignment_id,
        role=role,
        project_id=request.ticket_spec.project_id,
        ticket_id=request.ticket_spec.ticket_id,
        ticket_type=request.ticket_spec.ticket_type,
        input_SHA256=input_SHA256,
        role_profile=profile,
        assignment_SHA256=digest,
    )


def prepare_ticket_generator_assignments(
    request: TicketGenerationRequest,
) -> tuple[GeneratorAssignment, ...]:
    """Prepare deterministic in-memory role assignments without execution."""

    sorted_roles = tuple(sorted(request.roles, key=lambda role: _ROLE_RANK[role]))
    input_digest = _generator_input_digest(request)
    return tuple(_make_assignment(request, role, input_digest) for role in sorted_roles)


def _proposal_digest(
    *,
    schema_version: int,
    assignment_id: str,
    assignment_SHA256: str,
    role: TicketGeneratorRole,
    project_id: str,
    ticket_id: str,
    proposed_ticket: TicketSpec,
    rationale: str,
    evidence_source_ids: tuple[str, ...],
    assumptions: tuple[str, ...],
    risks: tuple[str, ...],
    unresolved_questions: tuple[str, ...],
) -> str:
    record = {
        "algorithm": TICKET_PROPOSAL_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "assignment_id": assignment_id,
        "assignment_SHA256": assignment_SHA256,
        "role": role.value,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "proposed_ticket": proposed_ticket.model_dump(mode="json"),
        "rationale": rationale,
        "evidence_source_ids": list(evidence_source_ids),
        "assumptions": list(assumptions),
        "risks": list(risks),
        "unresolved_questions": list(unresolved_questions),
    }
    return _sha256_text(_deterministic_json(record))


def build_ticket_proposal(
    *,
    assignment: GeneratorAssignment,
    proposed_ticket: TicketSpec,
    rationale: str,
    evidence_source_ids: tuple[str, ...],
    assumptions: tuple[str, ...] = (),
    risks: tuple[str, ...] = (),
    unresolved_questions: tuple[str, ...] = (),
) -> TicketProposal:
    """Package externally produced ticket content as one independent proposal."""

    if proposed_ticket.project_id != assignment.project_id:
        raise TicketProposalValidationError(
            f"proposed_ticket project_id must match assignment: project_id={assignment.project_id}"
        )
    if proposed_ticket.ticket_id != assignment.ticket_id:
        raise TicketProposalValidationError(
            f"proposed_ticket ticket_id must match assignment: ticket_id={assignment.ticket_id}"
        )
    if proposed_ticket.ticket_type != assignment.ticket_type:
        raise TicketProposalValidationError(
            "proposed_ticket ticket_type must match assignment: "
            f"ticket_type={assignment.ticket_type.value}"
        )
    if (
        proposed_ticket.ticket_type
        not in assignment.role_profile.supported_ticket_types
    ):
        raise TicketProposalValidationError(
            "assignment role must support proposed ticket type: "
            f"role={assignment.role.value}; ticket_type={proposed_ticket.ticket_type.value}"
        )
    proposal_SHA256 = _proposal_digest(
        schema_version=TICKET_GENERATOR_ROLE_SCHEMA_VERSION,
        assignment_id=assignment.assignment_id,
        assignment_SHA256=assignment.assignment_SHA256,
        role=assignment.role,
        project_id=assignment.project_id,
        ticket_id=assignment.ticket_id,
        proposed_ticket=proposed_ticket,
        rationale=rationale,
        evidence_source_ids=evidence_source_ids,
        assumptions=assumptions,
        risks=risks,
        unresolved_questions=unresolved_questions,
    )
    return TicketProposal(
        assignment_id=assignment.assignment_id,
        assignment_SHA256=assignment.assignment_SHA256,
        role=assignment.role,
        project_id=assignment.project_id,
        ticket_id=assignment.ticket_id,
        proposed_ticket=proposed_ticket,
        rationale=rationale,
        evidence_source_ids=evidence_source_ids,
        assumptions=assumptions,
        risks=risks,
        unresolved_questions=unresolved_questions,
        proposal_SHA256=proposal_SHA256,
    )


def validate_ticket_generator_proposal(
    request: TicketGenerationRequest,
    proposal: TicketProposal,
) -> TicketProposal:
    """Validate proposal binding without linting, approval or publication."""

    if proposal.role not in request.roles:
        raise TicketProposalValidationError(
            f"proposal role was not requested: role={proposal.role.value}"
        )
    assignments = prepare_ticket_generator_assignments(request)
    assignment_by_id = {
        assignment.assignment_id: assignment for assignment in assignments
    }
    assignment = assignment_by_id.get(proposal.assignment_id)
    if assignment is None:
        raise TicketProposalValidationError(
            f"assignment_id is not valid for request: assignment_id={proposal.assignment_id}"
        )
    if proposal.assignment_SHA256 != assignment.assignment_SHA256:
        raise TicketProposalValidationError(
            f"assignment_SHA256 does not match request assignment: assignment_id={proposal.assignment_id}"
        )
    if proposal.project_id != request.ticket_spec.project_id:
        raise TicketProposalValidationError(
            f"proposal project_id does not match request: project_id={request.ticket_spec.project_id}"
        )
    if proposal.ticket_id != request.ticket_spec.ticket_id:
        raise TicketProposalValidationError(
            f"proposal ticket_id does not match request: ticket_id={request.ticket_spec.ticket_id}"
        )
    if proposal.proposed_ticket.project_id != proposal.project_id:
        raise TicketProposalValidationError(
            "proposed_ticket project_id does not match proposal project_id: "
            f"project_id={proposal.project_id}"
        )
    if proposal.proposed_ticket.ticket_id != proposal.ticket_id:
        raise TicketProposalValidationError(
            "proposed_ticket ticket_id does not match proposal ticket_id: "
            f"ticket_id={proposal.ticket_id}"
        )
    if proposal.proposed_ticket.ticket_type != request.ticket_spec.ticket_type:
        raise TicketProposalValidationError(
            "proposed_ticket ticket_type does not match request: "
            f"ticket_type={request.ticket_spec.ticket_type.value}"
        )
    if (
        proposal.proposed_ticket.ticket_type
        not in get_ticket_generator_role_profile(proposal.role).supported_ticket_types
    ):
        raise TicketProposalValidationError(
            "proposal role does not support ticket_type: "
            f"role={proposal.role.value}; ticket_type={proposal.proposed_ticket.ticket_type.value}"
        )
    included_source_ids = frozenset(
        item.source_id for item in request.context_pack.items
    )
    missing_evidence = tuple(
        source_id
        for source_id in proposal.evidence_source_ids
        if source_id not in included_source_ids
    )
    if missing_evidence:
        raise TicketProposalValidationError(
            "proposal evidence source_id is not included in ContextPack: "
            f"source_id={missing_evidence[0]}"
        )
    expected_digest = _proposal_digest(
        schema_version=proposal.schema_version,
        assignment_id=proposal.assignment_id,
        assignment_SHA256=proposal.assignment_SHA256,
        role=proposal.role,
        project_id=proposal.project_id,
        ticket_id=proposal.ticket_id,
        proposed_ticket=proposal.proposed_ticket,
        rationale=proposal.rationale,
        evidence_source_ids=proposal.evidence_source_ids,
        assumptions=proposal.assumptions,
        risks=proposal.risks,
        unresolved_questions=proposal.unresolved_questions,
    )
    if proposal.proposal_SHA256 != expected_digest:
        raise TicketProposalValidationError(
            f"proposal_SHA256 does not match proposal digest: assignment_id={proposal.assignment_id}"
        )
    return proposal
