"""Compile approved TicketSpecs into compile-only WorkPacket candidates.

The compiler is deterministic and fully in-memory. It validates already-approved
and logically published P16 ticket evidence, then produces an immutable
execution-input candidate for later P17 stages. It does not allocate workspaces,
grant tools, run commands, mutate Git or execute tickets.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import re
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

from hermes_cli.agent_platform.ticket_factory import (
    HumanApprovalDecision,
    ProjectSpec,
    PublishedTicketArtifact,
    TicketApprovalRecord,
    TicketApprovalState,
    TicketDependencyPlan,
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    TicketPlanningRequest,
    TicketPublicationResult,
    TicketPublicationState,
    TicketResponseContractSpec,
    TicketSpec,
    WaveDisposition,
    build_ticket_dependency_plan,
    lint_ticket_collection,
)
from hermes_cli.agent_platform.ticket_factory.specs import (
    ProjectIdentifier,
    RepositoryScopeSpec,
    TicketIdentifier,
)

WORK_PACKET_SCHEMA_VERSION = 1
WORK_PACKET_COMPILER_SCHEMA_VERSION = 1
WORK_PACKET_COMPILER_POLICY_ID = "pepper-work-packet-compiler-policy-v1"

AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-work-packet-compilation-authorization-sha256-v1"
)
REPOSITORY_SCOPE_DIGEST_ALGORITHM = (
    "agent-platform-work-packet-repository-scope-sha256-v1"
)
TASK_STEP_DIGEST_ALGORITHM = "agent-platform-work-packet-task-step-sha256-v1"
VALIDATION_STEP_DIGEST_ALGORITHM = (
    "agent-platform-work-packet-validation-step-sha256-v1"
)
PROJECT_SPEC_DIGEST_ALGORITHM = "agent-platform-work-packet-project-spec-sha256-v1"
SOURCE_TICKET_DIGEST_ALGORITHM = "agent-platform-work-packet-source-ticket-sha256-v1"
COMPILATION_INPUT_DIGEST_ALGORITHM = (
    "agent-platform-work-packet-compilation-input-sha256-v1"
)
COMPILATION_EVIDENCE_DIGEST_ALGORITHM = (
    "agent-platform-work-packet-compilation-evidence-sha256-v1"
)
WORK_PACKET_DIGEST_ALGORITHM = "agent-platform-work-packet-sha256-v1"
COMPILATION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-work-packet-compilation-result-sha256-v1"
)

_WORK_PACKET_ID_PATTERN = r"^WP-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"
_HUMAN_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$"
_PUBLICATION_ID_PATTERN = r"^PUB-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-[0-9]{4}$"
_PATH_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_WHITESPACE_PATTERN = re.compile(r"\s+")

_PILOT_ONLY_TICKET_IDS = frozenset(("P16.SP0", "P16.SP1"))
_ROOT_WILDCARD_PATTERNS = frozenset(("*", "**", ".", "./**"))
_PROTECTED_ROOT_PATTERNS = (
    ".git/**",
    ".opencode/**",
    "AGENTS.md",
    "graphify-out/**",
    "4_external/sources/**",
    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
)
_FORBIDDEN_GIT_ACTION_MARKERS = (
    "git add",
    "git commit",
    "git push",
    "git merge",
    "git rebase",
    "git reset",
    "git clean",
    "git stash",
    "git switch",
    "git checkout",
    "git branch",
    "git tag",
    "git worktree",
    "force push",
)


class WorkPacketCompilerError(ValueError):
    """Base error for compile-only WorkPacket compiler failures."""


class WorkPacketCompilerInputError(WorkPacketCompilerError):
    """Raised when supplied ticket, approval or publication inputs conflict."""


class WorkPacketCompilerAuthorizationError(WorkPacketCompilerError):
    """Raised when explicit compilation authorization is absent or invalid."""


class WorkPacketCompilerIntegrityError(WorkPacketCompilerError):
    """Raised when deterministic digest or nested integrity checks fail."""


class WorkPacketExecutionMode(str, Enum):
    SINGLE_AGENT = "single_agent"


class WorkPacketValidationKind(str, Enum):
    COMMAND = "command"
    MANUAL = "manual"


class WorkPacketDownstreamCapability(str, Enum):
    WORKSPACE_ALLOCATION = "workspace_allocation"
    TOOL_PERMISSION_PROFILE = "tool_permission_profile"
    SINGLE_AGENT_EXECUTION = "single_agent_execution"
    VALIDATION_COMMAND_RUNNER = "validation_command_runner"
    RESULT_FAILURE_CANCELLATION_ENVELOPES = "result_failure_cancellation_envelopes"
    DIFF_ARTIFACT_REVIEW = "diff_artifact_review"
    HUMAN_GIT_HANDOFF = "human_git_handoff"


class WorkPacketGitAuthority(str, Enum):
    HUMAN_ONLY = "human_only"


class WorkPacketAuthorityBoundary(str, Enum):
    COMPILE_ONLY = "compile_only"


class WorkPacketCompilationDisposition(str, Enum):
    COMPILED = "compiled"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


def _validate_repository_path_pattern(value: str) -> str:
    if "\x00" in value:
        raise ValueError("repository path pattern must not contain NUL characters")
    if value in _ROOT_WILDCARD_PATTERNS:
        raise ValueError("repository path pattern is too broad")
    if value.startswith("/"):
        raise ValueError("repository path pattern must be relative")
    if _PATH_DRIVE_PATTERN.match(value):
        raise ValueError("repository path pattern must not be a Windows drive path")
    if "\\" in value:
        raise ValueError("repository path pattern must use forward slashes")
    if any(component == ".." for component in value.split("/")):
        raise ValueError("repository path pattern must not contain parent traversal")
    return value


def _validate_allowed_repository_path_pattern(value: str) -> str:
    value = _validate_repository_path_pattern(value)
    if any(_path_covers(value, protected) for protected in _PROTECTED_ROOT_PATTERNS):
        raise ValueError("repository path pattern covers protected root")
    return value


WorkPacketIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=24, max_length=96, pattern=_WORK_PACKET_ID_PATTERN),
]
HumanCompilationAuthorizerIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=3, max_length=96, pattern=_HUMAN_ID_PATTERN),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]
StepIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=8, max_length=16, pattern=r"^TASK-[0-9]{3,10}$"),
]
PublicationIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=13, max_length=80, pattern=_PUBLICATION_ID_PATTERN),
]
RepositoryPathPattern: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_repository_path_pattern),
]
AllowedRepositoryPathPattern: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_allowed_repository_path_pattern),
]


class _WorkPacketModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


class WorkPacketCompilationAuthorization(_WorkPacketModel):
    schema_version: Literal[1] = WORK_PACKET_COMPILER_SCHEMA_VERSION
    compilation_authorized: Literal[True] = True
    synthetic: Literal[False] = False
    authorizer_id: HumanCompilationAuthorizerIdentifier
    authorization_reference: BoundedText
    rationale: BoundedText
    risk_acknowledgement: BoundedText | None = None
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    publication_id: PublicationIdentifier
    publication_revision: int = Field(ge=1, strict=True)
    approval_SHA256: DigestText
    canonical_ticket_SHA256: DigestText
    publication_artifact_SHA256: DigestText
    execution_mode: Literal[WorkPacketExecutionMode.SINGLE_AGENT] = (
        WorkPacketExecutionMode.SINGLE_AGENT
    )
    git_authority: Literal[WorkPacketGitAuthority.HUMAN_ONLY] = (
        WorkPacketGitAuthority.HUMAN_ONLY
    )
    authorization_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_authorization(self) -> WorkPacketCompilationAuthorization:
        if _is_shadow_identifier(self.authorizer_id):
            raise ValueError(_SHADOW_REJECTION_MESSAGE)
        if self.ticket_id in _PILOT_ONLY_TICKET_IDS:
            raise ValueError(_SHADOW_REJECTION_MESSAGE)
        if self.authorization_SHA256 != _authorization_digest(self):
            raise ValueError("authorization_SHA256 must match authorization digest")
        return self


class WorkPacketRepositoryScope(_WorkPacketModel):
    allowed_paths: tuple[AllowedRepositoryPathPattern, ...] = Field(min_length=1)
    forbidden_paths: tuple[RepositoryPathPattern, ...] = ()
    allowed_actions: tuple[BoundedText, ...] = Field(min_length=1)
    forbidden_actions: tuple[BoundedText, ...] = ()
    scope_SHA256: DigestText

    @field_validator(
        "allowed_paths",
        "forbidden_paths",
        "allowed_actions",
        "forbidden_actions",
        mode="after",
    )
    @classmethod
    def _validate_unique_tuple(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "repository scope tuple")
        return value

    @model_validator(mode="after")
    def _validate_scope(self) -> WorkPacketRepositoryScope:
        for action in self.allowed_actions:
            if _is_forbidden_git_action(action):
                raise ValueError("allowed action authorizes Git mutation")
        if self.scope_SHA256 != _repository_scope_digest(self):
            raise ValueError("scope_SHA256 must match repository scope digest")
        return self


class WorkPacketTaskStep(_WorkPacketModel):
    step_id: StepIdentifier
    ordinal: int = Field(ge=1, strict=True)
    instruction: BoundedText
    source_task_index: int = Field(ge=0, strict=True)
    step_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_step(self) -> WorkPacketTaskStep:
        if self.step_id != _task_step_id(self.ordinal):
            raise ValueError("step_id must match ordinal")
        if self.source_task_index != self.ordinal - 1:
            raise ValueError("source_task_index must match ordinal")
        if self.step_SHA256 != _task_step_digest(self):
            raise ValueError("step_SHA256 must match task step digest")
        return self


class WorkPacketValidationStep(_WorkPacketModel):
    validation_id: BoundedText
    ordinal: int = Field(ge=1, strict=True)
    kind: WorkPacketValidationKind
    description: BoundedText
    command: BoundedText | None
    expected_result: BoundedText
    required: StrictBool
    command_execution_authorized: Literal[False] = False
    step_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_step(self) -> WorkPacketValidationStep:
        expected_kind = (
            WorkPacketValidationKind.MANUAL
            if self.command is None
            else WorkPacketValidationKind.COMMAND
        )
        if self.kind is not expected_kind:
            raise ValueError("validation kind must match command presence")
        if self.step_SHA256 != _validation_step_digest(self):
            raise ValueError("step_SHA256 must match validation step digest")
        return self


class WorkPacketDownstreamRequirement(_WorkPacketModel):
    capability: WorkPacketDownstreamCapability
    owner_ticket: TicketIdentifier
    required: Literal[True] = True
    satisfied_by_compiler: Literal[False] = False
    rationale: BoundedText


class WorkPacketCompilationRequest(_WorkPacketModel):
    schema_version: Literal[1] = WORK_PACKET_COMPILER_SCHEMA_VERSION
    compiler_policy_id: Literal["pepper-work-packet-compiler-policy-v1"] = (
        WORK_PACKET_COMPILER_POLICY_ID
    )
    project_spec: ProjectSpec
    approval_record: TicketApprovalRecord
    publication_result: TicketPublicationResult
    compilation_authorization: WorkPacketCompilationAuthorization

    @model_validator(mode="after")
    def _validate_request(self) -> WorkPacketCompilationRequest:
        _validate_request_bindings(self, error_type=ValueError)
        return self


class WorkPacketCompilationEvidence(_WorkPacketModel):
    compiler_policy_id: Literal["pepper-work-packet-compiler-policy-v1"] = (
        WORK_PACKET_COMPILER_POLICY_ID
    )
    project_spec_SHA256: DigestText
    source_ticket_SHA256: DigestText
    approval_SHA256: DigestText
    publication_result_SHA256: DigestText
    publication_artifact_SHA256: DigestText
    compilation_authorization_SHA256: DigestText
    fresh_lint_report_SHA256: DigestText
    dependency_plan_SHA256: DigestText
    compilation_input_SHA256: DigestText
    evidence_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evidence(self) -> WorkPacketCompilationEvidence:
        if self.evidence_SHA256 != _evidence_digest(self):
            raise ValueError("evidence_SHA256 must match compilation evidence digest")
        return self


class WorkPacket(_WorkPacketModel):
    schema_version: Literal[1] = WORK_PACKET_SCHEMA_VERSION
    work_packet_id: WorkPacketIdentifier
    compiler_policy_id: Literal["pepper-work-packet-compiler-policy-v1"] = (
        WORK_PACKET_COMPILER_POLICY_ID
    )
    authority_boundary: Literal[WorkPacketAuthorityBoundary.COMPILE_ONLY] = (
        WorkPacketAuthorityBoundary.COMPILE_ONLY
    )
    execution_ready: Literal[False] = False
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    publication_id: PublicationIdentifier
    publication_revision: int = Field(ge=1, strict=True)
    execution_mode: Literal[WorkPacketExecutionMode.SINGLE_AGENT] = (
        WorkPacketExecutionMode.SINGLE_AGENT
    )
    git_authority: Literal[WorkPacketGitAuthority.HUMAN_ONLY] = (
        WorkPacketGitAuthority.HUMAN_ONLY
    )
    project_spec: ProjectSpec
    source_ticket: TicketSpec
    repository_scope: WorkPacketRepositoryScope
    tasks: tuple[WorkPacketTaskStep, ...] = Field(min_length=1)
    validation_steps: tuple[WorkPacketValidationStep, ...] = Field(min_length=1)
    response_contract: TicketResponseContractSpec
    downstream_requirements: tuple[WorkPacketDownstreamRequirement, ...]
    source_ticket_SHA256: DigestText
    approval_SHA256: DigestText
    publication_artifact_SHA256: DigestText
    compilation_authorization_SHA256: DigestText
    compilation_input_SHA256: DigestText
    work_packet_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_packet(self) -> WorkPacket:
        _validate_work_packet_integrity(self, error_type=ValueError)
        return self


class WorkPacketCompilationResult(_WorkPacketModel):
    schema_version: Literal[1] = WORK_PACKET_COMPILER_SCHEMA_VERSION
    disposition: Literal[WorkPacketCompilationDisposition.COMPILED] = (
        WorkPacketCompilationDisposition.COMPILED
    )
    work_packet: WorkPacket
    evidence: WorkPacketCompilationEvidence
    fresh_lint_report: TicketLintReport
    dependency_plan: TicketDependencyPlan
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> WorkPacketCompilationResult:
        _validate_result_integrity(self, error_type=ValueError)
        return self


_SHADOW_REJECTION_MESSAGE = (
    "shadow-only approval evidence cannot authorize WorkPacket compilation"
)


def build_work_packet_compilation_authorization(
    *,
    authorizer_id: str,
    authorization_reference: str,
    rationale: str,
    approval_record: TicketApprovalRecord,
    publication_result: TicketPublicationResult,
    risk_acknowledgement: str | None = None,
) -> WorkPacketCompilationAuthorization:
    """Build explicit human authorization for compile-only WorkPacket creation."""

    approval, publication = _validated_approval_publication_for_compile(
        approval_record,
        publication_result,
    )
    if _is_shadow_identifier(authorizer_id):
        raise WorkPacketCompilerAuthorizationError(_SHADOW_REJECTION_MESSAGE)
    data = {
        "schema_version": WORK_PACKET_COMPILER_SCHEMA_VERSION,
        "compilation_authorized": True,
        "synthetic": False,
        "authorizer_id": authorizer_id,
        "authorization_reference": authorization_reference,
        "rationale": rationale,
        "risk_acknowledgement": risk_acknowledgement,
        "project_id": approval.project_id,
        "ticket_id": approval.ticket_id,
        "publication_id": publication.publication.publication_id,
        "publication_revision": publication.publication.revision,
        "approval_SHA256": approval.approval_SHA256,
        "canonical_ticket_SHA256": publication.publication.canonical_ticket_SHA256,
        "publication_artifact_SHA256": publication.publication.artifact_SHA256,
        "execution_mode": WorkPacketExecutionMode.SINGLE_AGENT,
        "git_authority": WorkPacketGitAuthority.HUMAN_ONLY,
    }
    authorization_sha = _authorization_digest_from_record(data)
    try:
        return WorkPacketCompilationAuthorization(
            **data,
            authorization_SHA256=authorization_sha,
        )
    except ValueError as exc:
        raise WorkPacketCompilerAuthorizationError(
            "compilation authorization invalid"
        ) from exc


def validate_work_packet(work_packet: WorkPacket) -> None:
    """Validate a compile-only WorkPacket without repair or side effects."""

    try:
        packet = WorkPacket.model_validate(work_packet.model_dump(mode="json"))
    except ValueError as exc:
        raise WorkPacketCompilerIntegrityError(
            "WorkPacket nested integrity is invalid"
        ) from exc
    _validate_work_packet_integrity(packet, error_type=WorkPacketCompilerIntegrityError)


def compile_ticket_spec_to_work_packet(
    request: WorkPacketCompilationRequest,
) -> WorkPacketCompilationResult:
    """Compile an approved and logically published TicketSpec into a WorkPacket."""

    try:
        validated_request = WorkPacketCompilationRequest.model_validate(
            request.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise WorkPacketCompilerInputError(
            "request must be a WorkPacketCompilationRequest"
        ) from exc
    except ValueError as exc:
        raise WorkPacketCompilerInputError(
            "request schema or binding is invalid"
        ) from exc

    _validate_request_for_compile(validated_request)
    approval = validated_request.approval_record
    publication = validated_request.publication_result
    published_ticket = publication.publication.canonical_ticket

    repository_scope = _compile_repository_scope(published_ticket.scope)
    planning_evidence = approval.fresh_planning_evidence
    if planning_evidence is None:
        raise WorkPacketCompilerInputError("fresh planning evidence is required")
    dependency_plan = _recompute_dependency_plan(planning_evidence.planning_request)
    if dependency_plan != planning_evidence.dependency_plan:
        raise WorkPacketCompilerIntegrityError(
            "dependency plan must equal approved planning evidence"
        )
    _validate_dependency_eligibility(dependency_plan, published_ticket.ticket_id)

    fresh_lint_report = _fresh_lint_report(
        validated_request.project_spec,
        published_ticket,
        dependency_plan,
    )
    _validate_fresh_lint_gate(
        fresh_lint_report,
        validated_request.compilation_authorization,
    )

    tasks = _compile_task_steps(published_ticket.tasks)
    validation_steps = _compile_validation_steps(published_ticket.validation_steps)
    downstream_requirements = _canonical_downstream_requirements()
    project_spec_sha = _project_spec_digest(validated_request.project_spec)
    source_ticket_sha = _source_ticket_digest(published_ticket)
    compilation_input_sha = _compilation_input_digest(
        project_spec_SHA256=project_spec_sha,
        source_ticket_SHA256=source_ticket_sha,
        approval_SHA256=approval.approval_SHA256,
        publication_result_SHA256=publication.result_SHA256,
        publication_artifact_SHA256=publication.publication.artifact_SHA256,
        compilation_authorization_SHA256=(
            validated_request.compilation_authorization.authorization_SHA256
        ),
        fresh_lint_report_SHA256=fresh_lint_report.report_SHA256,
        dependency_plan_SHA256=dependency_plan.plan_SHA256,
        repository_scope=repository_scope,
        tasks=tasks,
        validation_steps=validation_steps,
        downstream_requirements=downstream_requirements,
    )
    work_packet_id = _work_packet_id(
        ticket_id=published_ticket.ticket_id,
        revision=publication.publication.revision,
        compilation_input_SHA256=compilation_input_sha,
    )
    packet_data = {
        "schema_version": WORK_PACKET_SCHEMA_VERSION,
        "work_packet_id": work_packet_id,
        "compiler_policy_id": WORK_PACKET_COMPILER_POLICY_ID,
        "authority_boundary": WorkPacketAuthorityBoundary.COMPILE_ONLY,
        "execution_ready": False,
        "project_id": published_ticket.project_id,
        "ticket_id": published_ticket.ticket_id,
        "publication_id": publication.publication.publication_id,
        "publication_revision": publication.publication.revision,
        "execution_mode": WorkPacketExecutionMode.SINGLE_AGENT,
        "git_authority": WorkPacketGitAuthority.HUMAN_ONLY,
        "project_spec": validated_request.project_spec,
        "source_ticket": published_ticket,
        "repository_scope": repository_scope,
        "tasks": tasks,
        "validation_steps": validation_steps,
        "response_contract": published_ticket.response_contract,
        "downstream_requirements": downstream_requirements,
        "source_ticket_SHA256": source_ticket_sha,
        "approval_SHA256": approval.approval_SHA256,
        "publication_artifact_SHA256": publication.publication.artifact_SHA256,
        "compilation_authorization_SHA256": (
            validated_request.compilation_authorization.authorization_SHA256
        ),
        "compilation_input_SHA256": compilation_input_sha,
    }
    packet = WorkPacket(
        **packet_data,
        work_packet_SHA256=_work_packet_digest_from_record(packet_data),
    )
    validate_work_packet(packet)
    evidence_data = {
        "project_spec_SHA256": project_spec_sha,
        "source_ticket_SHA256": source_ticket_sha,
        "approval_SHA256": approval.approval_SHA256,
        "publication_result_SHA256": publication.result_SHA256,
        "publication_artifact_SHA256": publication.publication.artifact_SHA256,
        "compilation_authorization_SHA256": (
            validated_request.compilation_authorization.authorization_SHA256
        ),
        "fresh_lint_report_SHA256": fresh_lint_report.report_SHA256,
        "dependency_plan_SHA256": dependency_plan.plan_SHA256,
        "compilation_input_SHA256": compilation_input_sha,
    }
    evidence = WorkPacketCompilationEvidence(
        **evidence_data,
        evidence_SHA256=_evidence_digest_from_record(evidence_data),
    )
    result_data = {
        "schema_version": WORK_PACKET_COMPILER_SCHEMA_VERSION,
        "disposition": WorkPacketCompilationDisposition.COMPILED,
        "work_packet": packet,
        "evidence": evidence,
        "fresh_lint_report": fresh_lint_report,
        "dependency_plan": dependency_plan,
    }
    try:
        return WorkPacketCompilationResult(
            **result_data,
            result_SHA256=_result_digest_from_record(result_data),
        )
    except ValueError as exc:
        raise WorkPacketCompilerIntegrityError(
            "compilation result digest is invalid"
        ) from exc


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _record(value: BaseModel) -> dict[str, object]:
    return value.model_dump(mode="json")


def _dump_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, tuple | list):
        return [_dump_value(item) for item in value]
    return value


def _digest(algorithm: str, record: dict[str, object]) -> str:
    return _sha256_text(_deterministic_json({"algorithm": algorithm, **record}))


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


def _normalize_text(value: str) -> str:
    return _WHITESPACE_PATTERN.sub(" ", value.strip()).casefold()


def _is_shadow_identifier(value: str) -> bool:
    return value.upper().startswith("SHADOW-") or value.casefold().startswith("shadow-")


def _path_base(value: str) -> str:
    return value[:-3] if value.endswith("/**") else value


def _path_covers(candidate: str, protected: str) -> bool:
    candidate_base = _path_base(candidate)
    protected_base = _path_base(protected)
    if candidate_base == protected_base:
        return True
    return protected_base.startswith(f"{candidate_base}/") and candidate.endswith("/**")


def _is_forbidden_git_action(action: str) -> bool:
    normalized = _normalize_text(action.replace("-", " "))
    return any(marker in normalized for marker in _FORBIDDEN_GIT_ACTION_MARKERS)


def _authorization_digest(authorization: WorkPacketCompilationAuthorization) -> str:
    return _authorization_digest_from_record(
        authorization.model_dump(mode="json", exclude={"authorization_SHA256"})
    )


def _authorization_digest_from_record(record: dict[str, object]) -> str:
    return _digest(AUTHORIZATION_DIGEST_ALGORITHM, record)


def _repository_scope_digest(scope: WorkPacketRepositoryScope) -> str:
    return _repository_scope_digest_from_record(
        scope.model_dump(mode="json", exclude={"scope_SHA256"})
    )


def _repository_scope_digest_from_record(record: dict[str, object]) -> str:
    return _digest(REPOSITORY_SCOPE_DIGEST_ALGORITHM, record)


def _task_step_digest(step: WorkPacketTaskStep) -> str:
    return _task_step_digest_from_record(
        step.model_dump(mode="json", exclude={"step_SHA256"})
    )


def _task_step_digest_from_record(record: dict[str, object]) -> str:
    return _digest(TASK_STEP_DIGEST_ALGORITHM, record)


def _validation_step_digest(step: WorkPacketValidationStep) -> str:
    return _validation_step_digest_from_record(
        step.model_dump(mode="json", exclude={"step_SHA256"})
    )


def _validation_step_digest_from_record(record: dict[str, object]) -> str:
    return _digest(VALIDATION_STEP_DIGEST_ALGORITHM, record)


def _project_spec_digest(project_spec: ProjectSpec) -> str:
    return _digest(
        PROJECT_SPEC_DIGEST_ALGORITHM, {"project_spec": _record(project_spec)}
    )


def _source_ticket_digest(ticket: TicketSpec) -> str:
    return _digest(SOURCE_TICKET_DIGEST_ALGORITHM, {"source_ticket": _record(ticket)})


def _compilation_input_digest(
    *,
    project_spec_SHA256: str,
    source_ticket_SHA256: str,
    approval_SHA256: str,
    publication_result_SHA256: str,
    publication_artifact_SHA256: str,
    compilation_authorization_SHA256: str,
    fresh_lint_report_SHA256: str,
    dependency_plan_SHA256: str,
    repository_scope: WorkPacketRepositoryScope,
    tasks: tuple[WorkPacketTaskStep, ...],
    validation_steps: tuple[WorkPacketValidationStep, ...],
    downstream_requirements: tuple[WorkPacketDownstreamRequirement, ...],
) -> str:
    return _digest(
        COMPILATION_INPUT_DIGEST_ALGORITHM,
        {
            "compiler_policy_id": WORK_PACKET_COMPILER_POLICY_ID,
            "project_spec_SHA256": project_spec_SHA256,
            "source_ticket_SHA256": source_ticket_SHA256,
            "approval_SHA256": approval_SHA256,
            "publication_result_SHA256": publication_result_SHA256,
            "publication_artifact_SHA256": publication_artifact_SHA256,
            "compilation_authorization_SHA256": compilation_authorization_SHA256,
            "fresh_lint_report_SHA256": fresh_lint_report_SHA256,
            "dependency_plan_SHA256": dependency_plan_SHA256,
            "repository_scope": _record(repository_scope),
            "tasks": [_record(step) for step in tasks],
            "validation_steps": [_record(step) for step in validation_steps],
            "downstream_requirements": [
                _record(requirement) for requirement in downstream_requirements
            ],
        },
    )


def _evidence_digest(evidence: WorkPacketCompilationEvidence) -> str:
    return _evidence_digest_from_record(
        evidence.model_dump(mode="json", exclude={"evidence_SHA256"})
    )


def _evidence_digest_from_record(record: dict[str, object]) -> str:
    return _digest(
        COMPILATION_EVIDENCE_DIGEST_ALGORITHM,
        {"compiler_policy_id": WORK_PACKET_COMPILER_POLICY_ID, **record},
    )


def _work_packet_digest(packet: WorkPacket) -> str:
    return _work_packet_digest_from_record(
        packet.model_dump(mode="json", exclude={"work_packet_SHA256"})
    )


def _work_packet_digest_from_record(record: dict[str, object]) -> str:
    prepared = {key: _dump_value(value) for key, value in record.items()}
    return _digest(WORK_PACKET_DIGEST_ALGORITHM, prepared)


def _result_digest(result: WorkPacketCompilationResult) -> str:
    return _result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _result_digest_from_record(record: dict[str, object]) -> str:
    prepared = {key: _dump_value(value) for key, value in record.items()}
    return _digest(COMPILATION_RESULT_DIGEST_ALGORITHM, prepared)


def _task_step_id(ordinal: int) -> str:
    return f"TASK-{ordinal:03d}"


def _work_packet_id(
    *, ticket_id: str, revision: int, compilation_input_SHA256: str
) -> str:
    normalized_ticket = ticket_id.replace(".", "-")
    return f"WP-{normalized_ticket}-R{revision:04d}-{compilation_input_SHA256[:12]}"


def _validated_approval_publication_for_compile(
    approval_record: TicketApprovalRecord,
    publication_result: TicketPublicationResult,
) -> tuple[TicketApprovalRecord, TicketPublicationResult]:
    try:
        approval = TicketApprovalRecord.model_validate(
            approval_record.model_dump(mode="json")
        )
        publication = TicketPublicationResult.model_validate(
            publication_result.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkPacketCompilerIntegrityError(
            "approval or publication digest evidence is invalid"
        ) from exc
    if _is_shadow_identifier(approval.approval_evidence.reviewer_id):
        raise WorkPacketCompilerAuthorizationError(_SHADOW_REJECTION_MESSAGE)
    if approval.ticket_id in _PILOT_ONLY_TICKET_IDS:
        raise WorkPacketCompilerAuthorizationError(_SHADOW_REJECTION_MESSAGE)
    if approval.state is not TicketApprovalState.APPROVED:
        raise WorkPacketCompilerAuthorizationError("approval state must be approved")
    if approval.decision is not HumanApprovalDecision.APPROVE:
        raise WorkPacketCompilerAuthorizationError("approval decision must be approve")
    if approval.approved_ticket is None:
        raise WorkPacketCompilerAuthorizationError("approved ticket is required")
    if publication.publication.state is not TicketPublicationState.PUBLISHED:
        raise WorkPacketCompilerAuthorizationError(
            "publication state must be published"
        )
    if publication.publication.project_id != approval.project_id:
        raise WorkPacketCompilerInputError("publication project_id must match approval")
    if publication.publication.ticket_id != approval.ticket_id:
        raise WorkPacketCompilerInputError("publication ticket_id must match approval")
    if publication.publication.approval_SHA256 != approval.approval_SHA256:
        raise WorkPacketCompilerIntegrityError("publication approval digest must match")
    if publication.publication.canonical_ticket != approval.approved_ticket:
        raise WorkPacketCompilerIntegrityError(
            "published ticket must match approved ticket"
        )
    return (approval, publication)


def _validate_request_bindings(
    request: WorkPacketCompilationRequest, *, error_type: type[Exception]
) -> None:
    approval = request.approval_record
    publication = request.publication_result.publication
    authorization = request.compilation_authorization
    if approval.project_id != request.project_spec.project_id:
        raise error_type("approval project_id must match project")
    if approval.approved_ticket is None:
        raise error_type("approved ticket is required")
    if approval.approved_ticket.project_id != request.project_spec.project_id:
        raise error_type("approved ticket project_id must match project")
    if publication.project_id != request.project_spec.project_id:
        raise error_type("publication project_id must match project")
    if approval.ticket_id != publication.ticket_id:
        raise error_type("approval and publication ticket_id must match")
    if approval.approved_ticket != publication.canonical_ticket:
        raise error_type("approved ticket must match published canonical ticket")
    if authorization.project_id != request.project_spec.project_id:
        raise error_type("authorization project_id must match project")
    if authorization.ticket_id != approval.ticket_id:
        raise error_type("authorization ticket_id must match approval")
    if authorization.publication_id != publication.publication_id:
        raise error_type("authorization publication_id must match publication")
    if authorization.publication_revision != publication.revision:
        raise error_type("authorization publication revision must match publication")
    if authorization.approval_SHA256 != approval.approval_SHA256:
        raise error_type("authorization approval digest must match approval")
    if authorization.canonical_ticket_SHA256 != publication.canonical_ticket_SHA256:
        raise error_type("authorization ticket digest must match publication")
    if authorization.publication_artifact_SHA256 != publication.artifact_SHA256:
        raise error_type("authorization artifact digest must match publication")


def _validate_request_for_compile(request: WorkPacketCompilationRequest) -> None:
    _validated_approval_publication_for_compile(
        request.approval_record,
        request.publication_result,
    )
    try:
        WorkPacketCompilationAuthorization.model_validate(
            request.compilation_authorization.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkPacketCompilerAuthorizationError(
            "compilation authorization digest is invalid"
        ) from exc
    _validate_request_bindings(
        request,
        error_type=WorkPacketCompilerInputError,
    )


def _compile_repository_scope(
    source_scope: RepositoryScopeSpec,
) -> WorkPacketRepositoryScope:
    data = {
        "allowed_paths": source_scope.allowed_paths,
        "forbidden_paths": source_scope.forbidden_paths,
        "allowed_actions": source_scope.allowed_actions,
        "forbidden_actions": source_scope.forbidden_actions,
    }
    try:
        return WorkPacketRepositoryScope(
            **data,
            scope_SHA256=_repository_scope_digest_from_record(data),
        )
    except ValueError as exc:
        raise WorkPacketCompilerInputError("repository scope is unsafe") from exc


def _compile_task_steps(tasks: tuple[str, ...]) -> tuple[WorkPacketTaskStep, ...]:
    compiled: list[WorkPacketTaskStep] = []
    for index, instruction in enumerate(tasks, start=1):
        data = {
            "step_id": _task_step_id(index),
            "ordinal": index,
            "instruction": instruction,
            "source_task_index": index - 1,
        }
        compiled.append(
            WorkPacketTaskStep(
                **data,
                step_SHA256=_task_step_digest_from_record(data),
            )
        )
    return tuple(compiled)


def _compile_validation_steps(
    validation_steps: tuple[object, ...],
) -> tuple[WorkPacketValidationStep, ...]:
    compiled: list[WorkPacketValidationStep] = []
    for index, step in enumerate(validation_steps, start=1):
        command = step.command
        data = {
            "validation_id": step.validation_id,
            "ordinal": index,
            "kind": WorkPacketValidationKind.MANUAL
            if command is None
            else WorkPacketValidationKind.COMMAND,
            "description": step.description,
            "command": command,
            "expected_result": step.expected_result,
            "required": step.required,
            "command_execution_authorized": False,
        }
        compiled.append(
            WorkPacketValidationStep(
                **data,
                step_SHA256=_validation_step_digest_from_record(data),
            )
        )
    return tuple(compiled)


def _canonical_downstream_requirements() -> tuple[WorkPacketDownstreamRequirement, ...]:
    rows = (
        (
            WorkPacketDownstreamCapability.WORKSPACE_ALLOCATION,
            "P17.1",
            "Workspace allocation is deferred to P17.1.",
        ),
        (
            WorkPacketDownstreamCapability.TOOL_PERMISSION_PROFILE,
            "P17.2",
            "Tool permission profiles are deferred to P17.2.",
        ),
        (
            WorkPacketDownstreamCapability.SINGLE_AGENT_EXECUTION,
            "P17.3",
            "Single-agent runtime execution is deferred to P17.3.",
        ),
        (
            WorkPacketDownstreamCapability.VALIDATION_COMMAND_RUNNER,
            "P17.4",
            "Validation command execution is deferred to P17.4.",
        ),
        (
            WorkPacketDownstreamCapability.RESULT_FAILURE_CANCELLATION_ENVELOPES,
            "P17.5",
            "Result, failure and cancellation envelopes are deferred to P17.5.",
        ),
        (
            WorkPacketDownstreamCapability.DIFF_ARTIFACT_REVIEW,
            "P17.6",
            "Diff and artifact review are deferred to P17.6.",
        ),
        (
            WorkPacketDownstreamCapability.HUMAN_GIT_HANDOFF,
            "P17.7",
            "Human Git handoff is deferred to P17.7.",
        ),
    )
    return tuple(
        WorkPacketDownstreamRequirement(
            capability=capability,
            owner_ticket=owner,
            rationale=rationale,
        )
        for capability, owner, rationale in rows
    )


def _recompute_dependency_plan(request: TicketPlanningRequest) -> TicketDependencyPlan:
    try:
        return build_ticket_dependency_plan(request)
    except ValueError as exc:
        raise WorkPacketCompilerInputError(
            "dependency planning request is invalid"
        ) from exc


def _validate_dependency_eligibility(
    plan: TicketDependencyPlan, ticket_id: str
) -> None:
    if ticket_id not in plan.ticket_ids:
        raise WorkPacketCompilerInputError(
            "target ticket must be present in dependency plan"
        )
    if ticket_id in plan.blocked_ticket_ids:
        raise WorkPacketCompilerInputError("target ticket is blocked")
    if ticket_id not in plan.topological_order:
        raise WorkPacketCompilerIntegrityError("target ticket missing from topology")
    target_wave = next(
        (wave for wave in plan.waves if ticket_id in wave.ticket_ids), None
    )
    if target_wave is None:
        raise WorkPacketCompilerInputError("target ticket missing from dependency wave")
    if target_wave.disposition is not WaveDisposition.DEPENDENCY_READY:
        raise WorkPacketCompilerInputError("target dependency wave is not ready")


def _fresh_lint_report(
    project_spec: ProjectSpec,
    published_ticket: TicketSpec,
    dependency_plan: TicketDependencyPlan,
) -> TicketLintReport:
    try:
        return lint_ticket_collection(
            TicketLintRequest(
                project_spec=project_spec,
                tickets=(published_ticket,),
                dependency_plan=dependency_plan,
                collection_complete=False,
            )
        )
    except ValueError as exc:
        raise WorkPacketCompilerInputError("fresh lint request is invalid") from exc


def _validate_fresh_lint_gate(
    report: TicketLintReport,
    authorization: WorkPacketCompilationAuthorization,
) -> None:
    if report.disposition not in (
        TicketLintDisposition.PASS,
        TicketLintDisposition.PASS_WITH_WARNINGS,
    ):
        raise WorkPacketCompilerInputError("fresh lint disposition blocks compilation")
    if (
        report.disposition is TicketLintDisposition.PASS_WITH_WARNINGS
        and authorization.risk_acknowledgement is None
    ):
        raise WorkPacketCompilerAuthorizationError(
            "risk acknowledgement is required for warning lint disposition"
        )


def _validate_sequence(
    values: tuple[WorkPacketTaskStep, ...] | tuple[WorkPacketValidationStep, ...],
    *,
    field_name: str,
    error_type: type[Exception],
) -> None:
    for index, value in enumerate(values, start=1):
        if value.ordinal != index:
            raise error_type(f"{field_name} ordinals must be contiguous")


def _validate_work_packet_integrity(
    packet: WorkPacket,
    *,
    error_type: type[Exception],
) -> None:
    if packet.project_id != packet.project_spec.project_id:
        raise error_type("project ID must match project spec")
    if packet.project_id != packet.source_ticket.project_id:
        raise error_type("project ID must match source ticket")
    if packet.ticket_id != packet.source_ticket.ticket_id:
        raise error_type("ticket ID must match source ticket")
    if packet.source_ticket_SHA256 != _source_ticket_digest(packet.source_ticket):
        raise error_type("source_ticket_SHA256 mismatch")
    if packet.repository_scope.scope_SHA256 != _repository_scope_digest(
        packet.repository_scope
    ):
        raise error_type("repository scope digest mismatch")
    _validate_sequence(packet.tasks, field_name="task", error_type=error_type)
    for step in packet.tasks:
        if step.step_id != _task_step_id(step.ordinal):
            raise error_type("task step ID mismatch")
        if step.source_task_index != step.ordinal - 1:
            raise error_type("task source index mismatch")
        if step.step_SHA256 != _task_step_digest(step):
            raise error_type("task step digest mismatch")
    _validate_sequence(
        packet.validation_steps,
        field_name="validation",
        error_type=error_type,
    )
    for step in packet.validation_steps:
        if step.command_execution_authorized is not False:
            raise error_type("validation command execution must be false")
        if step.step_SHA256 != _validation_step_digest(step):
            raise error_type("validation step digest mismatch")
    if packet.downstream_requirements != _canonical_downstream_requirements():
        raise error_type("downstream requirements mismatch")
    if packet.work_packet_id != _work_packet_id(
        ticket_id=packet.ticket_id,
        revision=packet.publication_revision,
        compilation_input_SHA256=packet.compilation_input_SHA256,
    ):
        raise error_type("WorkPacket ID mismatch")
    if packet.work_packet_SHA256 != _work_packet_digest(packet):
        raise error_type("work_packet_SHA256 mismatch")


def _validate_result_integrity(
    result: WorkPacketCompilationResult,
    *,
    error_type: type[Exception],
) -> None:
    packet = result.work_packet
    evidence = result.evidence
    if packet.execution_ready is not False:
        raise error_type("compiled WorkPacket must not be execution-ready")
    if evidence.source_ticket_SHA256 != packet.source_ticket_SHA256:
        raise error_type("evidence source ticket digest mismatch")
    if evidence.approval_SHA256 != packet.approval_SHA256:
        raise error_type("evidence approval digest mismatch")
    if evidence.publication_artifact_SHA256 != packet.publication_artifact_SHA256:
        raise error_type("evidence artifact digest mismatch")
    if (
        evidence.compilation_authorization_SHA256
        != packet.compilation_authorization_SHA256
    ):
        raise error_type("evidence authorization digest mismatch")
    if evidence.fresh_lint_report_SHA256 != result.fresh_lint_report.report_SHA256:
        raise error_type("fresh lint report digest mismatch")
    if evidence.dependency_plan_SHA256 != result.dependency_plan.plan_SHA256:
        raise error_type("dependency plan digest mismatch")
    if evidence.compilation_input_SHA256 != packet.compilation_input_SHA256:
        raise error_type("compilation input digest mismatch")
    if evidence.evidence_SHA256 != _evidence_digest(evidence):
        raise error_type("evidence digest mismatch")
    if result.result_SHA256 != _result_digest(result):
        raise error_type("result_SHA256 mismatch")
