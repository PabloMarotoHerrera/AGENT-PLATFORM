"""Governed non-critical Ticket pilot evidence binding for Agent Platform P17.8.

This module is a pure, deterministic contract layer. It binds already-created
P17.0 through P17.7 evidence for one human-selected, non-critical pilot ticket.
It does not inspect the workspace, invoke subprocesses, run Git, call providers
or models, persist evidence, retry stages, clean up workspaces, or claim
production readiness.
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
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.work_packet.compiler import (
    WorkPacket,
    WorkPacketAuthorityBoundary,
    WorkPacketCompilationDisposition,
    WorkPacketCompilationResult,
    validate_work_packet,
)
from hermes_cli.agent_platform.work_packet.diff_artifact_review import (
    AggregateReviewState,
    DiffArtifactReviewResult,
    ReviewFindingSeverity,
    ReviewObservedPathStatus,
    validate_diff_artifact_review_result,
)
from hermes_cli.agent_platform.work_packet.human_git_handoff import (
    GitHandoffAuthority,
    GitHandoffDecision,
    GitHandoffPathStatus,
    GitHandoffResult,
    GitHandoffState,
    validate_human_git_handoff_result,
)
from hermes_cli.agent_platform.work_packet.outcome_envelopes import (
    OutcomeEnvelope,
    OutcomeEnvelopeKind,
    validate_outcome_envelope,
)
from hermes_cli.agent_platform.work_packet.single_agent_execution import (
    SingleAgentExecutionResult,
    SingleAgentExecutionState,
    validate_single_agent_execution_result,
)
from hermes_cli.agent_platform.work_packet.tool_permissions import (
    ToolPermissionOperation,
    ToolPermissionProfileResult,
    validate_tool_permission_profile,
)
from hermes_cli.agent_platform.work_packet.validation_command_runner import (
    ValidationCommandDisposition,
    ValidationCommandRunnerResult,
    ValidationCommandRunnerState,
    validate_validation_command_runner_result,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocationResult,
    WorkspaceKind,
    WorkspaceLifecycleState,
    validate_workspace_allocation,
)

NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION = 1
NON_CRITICAL_TICKET_PILOT_POLICY_ID = (
    "pepper-complete-governed-non-critical-ticket-pilot-v1"
)
NON_CRITICAL_TICKET_PILOT_EXPORT_COUNT = 27

POLICY_DIGEST_ALGORITHM = (
    "agent-platform-non-critical-pilot-eligibility-policy-sha256-v1"
)
SELECTION_DIGEST_ALGORITHM = (
    "agent-platform-non-critical-pilot-ticket-selection-sha256-v1"
)
STAGE_EVIDENCE_DIGEST_ALGORITHM = (
    "agent-platform-non-critical-pilot-stage-evidence-sha256-v1"
)
FINDING_DIGEST_ALGORITHM = "agent-platform-non-critical-pilot-finding-sha256-v1"
ACCEPTANCE_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-non-critical-pilot-acceptance-summary-sha256-v1"
)
PILOT_ID_DIGEST_ALGORITHM = "agent-platform-non-critical-ticket-pilot-id-sha256-v1"
RESULT_DIGEST_ALGORITHM = "agent-platform-non-critical-ticket-pilot-result-sha256-v1"

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_SELECTION_ID_PATTERN = r"^PSEL-[A-Z0-9]+(?:-[A-Z0-9]+)*-R[0-9]{4}-[a-f0-9]{12}$"
_PILOT_ID_PATTERN = r"^NCP-[A-Z0-9]+(?:-[A-Z0-9]+)*-R[0-9]{4}-[a-f0-9]{12}$"
_STAGE_EVIDENCE_ID_PATTERN = r"^PSEV-[0-9]{3}$"
_FINDING_ID_PATTERN = r"^PFND-[0-9]{3}$"
_CONTROL_OR_ANSI_PATTERN = r"[\x00-\x1f\x7f\x1b]"
_PERSONAL_PATH_PATTERN = r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)"
_RELATIVE_PATH_PATTERN = r"^[A-Za-z0-9._@+\-/]+$"
_VALIDATION_ID_PATTERN = r"^[A-Za-z0-9._:@+\-]+$"
_SHELL_MARKERS = ("&&", "||", ";", "|", "`", "$(", "<", ">")
_GIT_COMMAND_MARKERS = (
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
    "git worktree",
    "git tag",
)
_CREDENTIAL_MARKERS = (
    "access_token",
    "refresh_token",
    "authorization:",
    "bearer ",
    "client_secret",
    "api_key",
    "apikey",
    "private key",
    "password=",
    "token=",
    "secret=",
    "sk-",
)
_RAW_OUTPUT_MARKERS = (
    "raw stdout",
    "raw stderr",
    "traceback",
    "diff --git",
    "@@ ",
    "file content snapshot",
    "reasoning trace",
    "model output",
    "provider response",
)
_DEPENDENCY_PATHS = (
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "setup.py",
    "setup.cfg",
    "package.json",
    "pnpm-workspace.yaml",
    "uv.toml",
)
_LOCKFILE_NAMES = (
    "package-lock.json",
    "uv.lock",
    "poetry.lock",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pipfile.lock",
)
_CREDENTIAL_PATH_MARKERS = (
    ".env",
    "auth.json",
    "credential",
    "credentials",
    "secret",
    "secrets",
    "private_key",
    "id_rsa",
    "id_ed25519",
    "token",
)
_DENY_FIRST_REQUIRED_OPERATIONS = frozenset((
    ToolPermissionOperation.EXECUTE_COMMAND,
    ToolPermissionOperation.VALIDATION_COMMAND,
    ToolPermissionOperation.GIT_READ_ONLY,
    ToolPermissionOperation.GIT_MUTATION,
    ToolPermissionOperation.NETWORK_ACCESS,
    ToolPermissionOperation.PROVIDER_CALL,
    ToolPermissionOperation.MODEL_CALL,
    ToolPermissionOperation.AGENT_CONTROL,
    ToolPermissionOperation.WORKER_CONTROL,
))


class NonCriticalTicketPilotError(ValueError):
    """Base error for P17.8 non-critical pilot contract failures."""


class NonCriticalTicketPilotInputError(NonCriticalTicketPilotError):
    """Raised when supplied pilot inputs are structurally invalid."""


class NonCriticalTicketPilotIntegrityError(NonCriticalTicketPilotError):
    """Raised when deterministic digest evidence is invalid."""


class NonCriticalTicketPilotPolicyError(NonCriticalTicketPilotError):
    """Raised when pilot policy invariants are violated."""


class NonCriticalTicketPilotStateError(NonCriticalTicketPilotError):
    """Raised when prerequisite stage state is invalid or ambiguous."""


class NonCriticalTicketPilotValidationError(NonCriticalTicketPilotError):
    """Raised when a built pilot result fails validation."""


class PilotState(str, Enum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class PilotDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class PilotRiskClass(str, Enum):
    NON_CRITICAL = "non_critical"


class PilotStage(str, Enum):
    WORK_PACKET_COMPILATION = "work_packet_compilation"
    WORKSPACE_ALLOCATION = "workspace_allocation"
    TOOL_PERMISSION_PROFILE = "tool_permission_profile"
    SINGLE_AGENT_EXECUTION = "single_agent_execution"
    VALIDATION_COMMAND_RUNNER = "validation_command_runner"
    OUTCOME_ENVELOPE = "outcome_envelope"
    DIFF_ARTIFACT_REVIEW = "diff_artifact_review"
    HUMAN_GIT_HANDOFF = "human_git_handoff"


class PilotFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class PilotFindingCode(str, Enum):
    TICKET_ELIGIBLE = "ticket_eligible"
    TICKET_CRITICAL = "ticket_critical"
    TICKET_SECURITY_SENSITIVE = "ticket_security_sensitive"
    TICKET_EXTERNAL_ACCESS_REQUIRED = "ticket_external_access_required"
    TICKET_DEPENDENCY_MUTATION_REQUIRED = "ticket_dependency_mutation_required"
    TICKET_GIT_MUTATION_REQUIRED = "ticket_git_mutation_required"
    STAGE_EVIDENCE_COMPLETE = "stage_evidence_complete"
    STAGE_EVIDENCE_MISSING = "stage_evidence_missing"
    STAGE_BINDING_MISMATCH = "stage_binding_mismatch"
    STAGE_NOT_COMPLETED = "stage_not_completed"
    PROVIDER_AUTHORITY_PRESENT = "provider_authority_present"
    MODEL_AUTHORITY_PRESENT = "model_authority_present"
    AUTOMATIC_AUTHORITY_PRESENT = "automatic_authority_present"
    GIT_EXECUTION_PRESENT = "git_execution_present"
    MANUAL_VALIDATION_PENDING = "manual_validation_pending"
    PILOT_ACCEPTED = "pilot_accepted"
    PILOT_REJECTED = "pilot_rejected"


def _validate_public_text(value: str, label: str) -> str:
    if re.search(_CONTROL_OR_ANSI_PATTERN, value):
        raise ValueError(f"{label} must not contain control characters")
    lower = value.casefold()
    if re.search(_PERSONAL_PATH_PATTERN, value):
        raise ValueError(f"{label} must not contain personal absolute paths")
    if any(marker in lower for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} must not contain credential material")
    if any(marker in lower for marker in _RAW_OUTPUT_MARKERS):
        raise ValueError(f"{label} must not contain raw output")
    if any(marker in lower for marker in _GIT_COMMAND_MARKERS):
        raise ValueError(f"{label} must not contain Git commands")
    if any(marker in value for marker in _SHELL_MARKERS):
        raise ValueError(f"{label} must not contain shell syntax")
    return value


def _validate_relative_path(value: str) -> str:
    _validate_public_text(value, "relative path")
    if not re.match(_RELATIVE_PATH_PATTERN, value):
        raise ValueError("relative path contains unsupported characters")
    if value.startswith("/") or value.startswith("./") or value.endswith("/"):
        raise ValueError("relative path must be normalized and relative")
    if "\\" in value or "//" in value:
        raise ValueError("relative path must use normalized forward slashes")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError("relative path must not contain traversal")
    if re.match(r"^[A-Za-z]:", value):
        raise ValueError("relative path must not contain a drive prefix")
    return value


def _validate_validation_identifier(value: str) -> str:
    _validate_public_text(value, "validation ID")
    if not re.match(_VALIDATION_ID_PATTERN, value):
        raise ValueError("validation ID contains unsupported characters")
    return value


def _reject_duplicate_values(values: tuple[str, ...], label: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{label} must be unique")


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
SelectionIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=24, max_length=128, pattern=_SELECTION_ID_PATTERN),
]
PilotIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=24, max_length=128, pattern=_PILOT_ID_PATTERN),
]
StageEvidenceIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=8, pattern=_STAGE_EVIDENCE_ID_PATTERN),
]
FindingIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=8, pattern=_FINDING_ID_PATTERN),
]
TicketIdentifierText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=64),
    AfterValidator(lambda value: _validate_public_text(value, "ticket ID")),
]
TitleText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=160),
    AfterValidator(lambda value: _validate_public_text(value, "ticket title")),
]
SummaryText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(lambda value: _validate_public_text(value, "summary")),
]
InvariantText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=192),
    AfterValidator(lambda value: _validate_public_text(value, "invariant")),
]
SourceIdentifierText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=160),
    AfterValidator(lambda value: _validate_public_text(value, "source ID")),
]
RelativePathText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_relative_path),
]
ValidationIdentifierText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=64),
    AfterValidator(_validate_validation_identifier),
]


class _PilotModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class PilotEligibilityPolicy(_PilotModel):
    schema_version: Literal[1] = NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION
    policy_id: Literal["pepper-complete-governed-non-critical-ticket-pilot-v1"] = (
        NON_CRITICAL_TICKET_PILOT_POLICY_ID
    )
    risk_class: Literal[PilotRiskClass.NON_CRITICAL] = PilotRiskClass.NON_CRITICAL
    maximum_files_changed: Literal[10] = 10
    maximum_created_files: Literal[5] = 5
    maximum_modified_files: Literal[10] = 10
    maximum_deleted_files: Literal[0] = 0
    allows_deleted_files: Literal[False] = False
    allows_untracked_files: Literal[True] = True
    allows_dependency_changes: Literal[False] = False
    allows_lockfile_changes: Literal[False] = False
    allows_credentials: Literal[False] = False
    allows_network: Literal[False] = False
    allows_provider_dispatch: Literal[False] = False
    allows_model_inference: Literal[False] = False
    allows_Docker: Literal[False] = False
    allows_Graphify: Literal[False] = False
    allows_Git_mutation: Literal[False] = False
    allows_branch_mutation: Literal[False] = False
    allows_database_migration: Literal[False] = False
    allows_production_deployment: Literal[False] = False
    allows_destructive_actions: Literal[False] = False
    requires_exact_validation_commands: Literal[True] = True
    requires_completed_diff_review: Literal[True] = True
    requires_completed_human_git_handoff: Literal[True] = True
    policy_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_policy(self) -> PilotEligibilityPolicy:
        if self.policy_SHA256 != _model_digest(POLICY_DIGEST_ALGORITHM, self):
            raise ValueError("policy_SHA256 must match policy digest")
        return self


class PilotTicketSelection(_PilotModel):
    selection_id: SelectionIdentifier
    ticket_id: TicketIdentifierText
    ticket_title: TitleText
    ticket_revision: int = Field(ge=1, le=9999, strict=True)
    risk_class: Literal[PilotRiskClass.NON_CRITICAL] = PilotRiskClass.NON_CRITICAL
    rationale: SummaryText
    selected_by_human: Literal[True] = True
    synthetic: Literal[False] = False
    expected_candidate_paths: tuple[RelativePathText, ...] = Field(min_length=1)
    expected_validation_ids: tuple[ValidationIdentifierText, ...] = Field(min_length=1)
    criticality_acknowledgement: SummaryText
    selection_SHA256: DigestText

    @field_validator(
        "expected_candidate_paths", "expected_validation_ids", mode="after"
    )
    @classmethod
    def _validate_unique_tuple(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "selection tuple")
        return value

    @model_validator(mode="after")
    def _validate_selection(self) -> PilotTicketSelection:
        if self.selection_id != _selection_id(self):
            raise ValueError("selection_id must match selection digest")
        if self.selection_SHA256 != _model_digest(SELECTION_DIGEST_ALGORITHM, self):
            raise ValueError("selection_SHA256 must match selection digest")
        return self


class PilotStageEvidence(_PilotModel):
    evidence_id: StageEvidenceIdentifier
    stage: PilotStage
    requirement_satisfied: StrictBool
    source_id: SourceIdentifierText
    source_SHA256: DigestText
    ticket_id: TicketIdentifierText
    work_packet_SHA256: DigestText
    allocation_SHA256: DigestText
    profile_SHA256: DigestText
    provider_dispatch_count: int = Field(ge=0, strict=True)
    model_inference_count: int = Field(ge=0, strict=True)
    automatic_authority_present: StrictBool
    Git_execution_count: int = Field(ge=0, strict=True)
    summary: SummaryText
    evidence_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evidence(self) -> PilotStageEvidence:
        if self.evidence_id != _stage_evidence_id(self.stage):
            raise ValueError("evidence_id must match pilot stage order")
        if self.evidence_SHA256 != _model_digest(STAGE_EVIDENCE_DIGEST_ALGORITHM, self):
            raise ValueError("evidence_SHA256 must match stage evidence digest")
        return self


class PilotFinding(_PilotModel):
    finding_id: FindingIdentifier
    severity: PilotFindingSeverity
    code: PilotFindingCode
    stage: PilotStage | None
    source_id: SourceIdentifierText
    summary: SummaryText
    failed_invariant: InvariantText
    finding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_finding(self) -> PilotFinding:
        if (
            self.code in _BLOCKING_CODES
            and self.severity is not PilotFindingSeverity.BLOCKING
        ):
            raise ValueError("blocking finding code requires blocking severity")
        if (
            self.code in _INFO_ONLY_CODES
            and self.severity is not PilotFindingSeverity.INFO
        ):
            raise ValueError("accepted finding code requires info severity")
        if self.code is PilotFindingCode.MANUAL_VALIDATION_PENDING:
            if self.severity is not PilotFindingSeverity.WARNING:
                raise ValueError("manual validation pending requires warning severity")
        if self.finding_SHA256 != _model_digest(FINDING_DIGEST_ALGORITHM, self):
            raise ValueError("finding_SHA256 must match finding digest")
        return self


class PilotAcceptanceSummary(_PilotModel):
    eligible: StrictBool
    stage_count: int = Field(ge=0, strict=True)
    completed_stage_count: int = Field(ge=0, strict=True)
    blocking_finding_count: int = Field(ge=0, strict=True)
    warning_finding_count: int = Field(ge=0, strict=True)
    information_finding_count: int = Field(ge=0, strict=True)
    manual_validation_ids_pending: tuple[ValidationIdentifierText, ...] = ()
    Git_commands_executed: int = Field(ge=0, strict=True)
    provider_dispatch_count: int = Field(ge=0, strict=True)
    model_inference_count: int = Field(ge=0, strict=True)
    automatic_retry_authorized: Literal[False] = False
    automatic_fallback_authorized: Literal[False] = False
    automatic_cleanup_authorized: Literal[False] = False
    automatic_rollback_authorized: Literal[False] = False
    automatic_staging_authorized: Literal[False] = False
    automatic_commit_authorized: Literal[False] = False
    automatic_push_authorized: Literal[False] = False
    summary_SHA256: DigestText

    @field_validator("manual_validation_ids_pending", mode="after")
    @classmethod
    def _validate_manual_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "manual validation IDs")
        return value

    @model_validator(mode="after")
    def _validate_summary(self) -> PilotAcceptanceSummary:
        if self.completed_stage_count > self.stage_count:
            raise ValueError("completed stage count cannot exceed stage count")
        if self.summary_SHA256 != _model_digest(
            ACCEPTANCE_SUMMARY_DIGEST_ALGORITHM, self
        ):
            raise ValueError("summary_SHA256 must match acceptance summary digest")
        return self


class NonCriticalTicketPilotRequest(_PilotModel):
    schema_version: Literal[1] = NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION
    policy_id: Literal["pepper-complete-governed-non-critical-ticket-pilot-v1"] = (
        NON_CRITICAL_TICKET_PILOT_POLICY_ID
    )
    selection: PilotTicketSelection
    eligibility_policy: PilotEligibilityPolicy
    compilation_result: WorkPacketCompilationResult
    allocation_result: WorkspaceAllocationResult
    profile_result: ToolPermissionProfileResult
    single_agent_execution_result: SingleAgentExecutionResult
    validation_command_runner_result: ValidationCommandRunnerResult
    outcome_envelope: OutcomeEnvelope
    diff_artifact_review_result: DiffArtifactReviewResult
    human_git_handoff_result: GitHandoffResult


class NonCriticalTicketPilotResult(_PilotModel):
    schema_version: Literal[1] = NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION
    policy_id: Literal["pepper-complete-governed-non-critical-ticket-pilot-v1"] = (
        NON_CRITICAL_TICKET_PILOT_POLICY_ID
    )
    pilot_id: PilotIdentifier
    state: PilotState
    decision: PilotDecision
    risk_class: PilotRiskClass
    ticket_id: TicketIdentifierText
    ticket_revision: int = Field(ge=1, le=9999, strict=True)
    selection_SHA256: DigestText
    eligibility_policy_SHA256: DigestText
    work_packet_id: SourceIdentifierText
    work_packet_SHA256: DigestText
    allocation_id: SourceIdentifierText
    allocation_SHA256: DigestText
    profile_id: SourceIdentifierText
    profile_SHA256: DigestText
    execution_result_SHA256: DigestText
    validation_result_SHA256: DigestText
    outcome_SHA256: DigestText
    review_SHA256: DigestText
    handoff_SHA256: DigestText
    stage_evidence: tuple[PilotStageEvidence, ...] = Field(min_length=8, max_length=8)
    findings: tuple[PilotFinding, ...] = Field(max_length=128)
    acceptance_summary: PilotAcceptanceSummary
    WorkPacket_execution_MVP_requirement_satisfied: StrictBool
    P17_closure_ready: StrictBool
    production_readiness_claimed: Literal[False] = False
    provider_dispatch_count: int = Field(ge=0, strict=True)
    model_inference_count: int = Field(ge=0, strict=True)
    result_SHA256: DigestText

    @field_validator("stage_evidence", mode="after")
    @classmethod
    def _validate_stage_evidence_tuple(
        cls, value: tuple[PilotStageEvidence, ...]
    ) -> tuple[PilotStageEvidence, ...]:
        _validate_stage_evidence_collection(value, error_type=ValueError)
        return value

    @field_validator("findings", mode="after")
    @classmethod
    def _validate_findings_tuple(
        cls, value: tuple[PilotFinding, ...]
    ) -> tuple[PilotFinding, ...]:
        _validate_finding_collection(value, error_type=ValueError)
        return value

    @model_validator(mode="after")
    def _validate_result(self) -> NonCriticalTicketPilotResult:
        _validate_result_integrity(self, error_type=ValueError)
        return self


_BLOCKING_CODES = frozenset((
    PilotFindingCode.TICKET_CRITICAL,
    PilotFindingCode.TICKET_SECURITY_SENSITIVE,
    PilotFindingCode.TICKET_EXTERNAL_ACCESS_REQUIRED,
    PilotFindingCode.TICKET_DEPENDENCY_MUTATION_REQUIRED,
    PilotFindingCode.TICKET_GIT_MUTATION_REQUIRED,
    PilotFindingCode.STAGE_EVIDENCE_MISSING,
    PilotFindingCode.STAGE_BINDING_MISMATCH,
    PilotFindingCode.STAGE_NOT_COMPLETED,
    PilotFindingCode.PROVIDER_AUTHORITY_PRESENT,
    PilotFindingCode.MODEL_AUTHORITY_PRESENT,
    PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
    PilotFindingCode.GIT_EXECUTION_PRESENT,
    PilotFindingCode.PILOT_REJECTED,
))
_INFO_ONLY_CODES = frozenset((
    PilotFindingCode.TICKET_ELIGIBLE,
    PilotFindingCode.STAGE_EVIDENCE_COMPLETE,
    PilotFindingCode.PILOT_ACCEPTED,
))


def build_pilot_eligibility_policy() -> PilotEligibilityPolicy:
    """Build the canonical immutable non-critical pilot eligibility policy."""

    data = {
        "schema_version": NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION,
        "policy_id": NON_CRITICAL_TICKET_PILOT_POLICY_ID,
        "risk_class": PilotRiskClass.NON_CRITICAL,
        "maximum_files_changed": 10,
        "maximum_created_files": 5,
        "maximum_modified_files": 10,
        "maximum_deleted_files": 0,
        "allows_deleted_files": False,
        "allows_untracked_files": True,
        "allows_dependency_changes": False,
        "allows_lockfile_changes": False,
        "allows_credentials": False,
        "allows_network": False,
        "allows_provider_dispatch": False,
        "allows_model_inference": False,
        "allows_Docker": False,
        "allows_Graphify": False,
        "allows_Git_mutation": False,
        "allows_branch_mutation": False,
        "allows_database_migration": False,
        "allows_production_deployment": False,
        "allows_destructive_actions": False,
        "requires_exact_validation_commands": True,
        "requires_completed_diff_review": True,
        "requires_completed_human_git_handoff": True,
    }
    return PilotEligibilityPolicy(
        **data,
        policy_SHA256=_digest_from_record(POLICY_DIGEST_ALGORITHM, data),
    )


def validate_non_critical_ticket_pilot_request(
    request: NonCriticalTicketPilotRequest,
) -> None:
    """Validate one P17.8 pilot request without repair or side effects."""

    validated = _validated_request(request)
    _validate_schema_policy(validated)
    _validate_policy(validated.eligibility_policy)
    _validate_selection_digest(validated.selection)
    _validate_prerequisite_digests(validated, strict_state=True)
    _validate_cross_contract_bindings(validated)
    _validate_selected_ticket_identity(validated)
    candidate_paths = _derive_candidate_paths(validated)
    if candidate_paths != validated.selection.expected_candidate_paths:
        raise NonCriticalTicketPilotPolicyError("candidate path selection mismatch")
    validation_ids = _derive_validation_ids(validated)
    if validation_ids != validated.selection.expected_validation_ids:
        raise NonCriticalTicketPilotPolicyError("validation ID selection mismatch")


def build_non_critical_ticket_pilot(
    request: NonCriticalTicketPilotRequest,
) -> NonCriticalTicketPilotResult:
    """Build a deterministic accepted or rejected non-critical pilot result."""

    validated = _validated_request(request)
    _validate_schema_policy(validated)
    _validate_policy(validated.eligibility_policy)
    _validate_selection_digest(validated.selection)
    _validate_prerequisite_digests(validated, strict_state=False)
    _validate_cross_contract_bindings(validated)
    _validate_selected_ticket_identity(validated)
    candidate_paths = _derive_candidate_paths(validated, require_review_match=False)
    validation_ids = _derive_validation_ids(validated)
    selection_paths_match = (
        candidate_paths == validated.selection.expected_candidate_paths
    )
    selection_validation_match = (
        validation_ids == validated.selection.expected_validation_ids
    )
    if not selection_paths_match:
        raise NonCriticalTicketPilotPolicyError("candidate path selection mismatch")
    if not selection_validation_match:
        raise NonCriticalTicketPilotPolicyError("validation ID selection mismatch")

    stage_evidence = _derive_stage_evidence(validated)
    findings = _derive_findings(validated, stage_evidence)
    acceptance_summary = _derive_acceptance_summary(validated, stage_evidence, findings)
    accepted = _is_accepted(stage_evidence, findings, acceptance_summary)
    decision = PilotDecision.ACCEPTED if accepted else PilotDecision.REJECTED
    state = PilotState.COMPLETED if accepted else PilotState.BLOCKED
    mvp_ready = accepted
    closure_ready = accepted
    result_data = _result_base_data(
        request=validated,
        stage_evidence=stage_evidence,
        findings=findings,
        acceptance_summary=acceptance_summary,
        decision=decision,
        state=state,
        mvp_ready=mvp_ready,
        closure_ready=closure_ready,
    )
    pilot_id = _pilot_id_from_record(result_data)
    result_record = {**result_data, "pilot_id": pilot_id}
    result = NonCriticalTicketPilotResult(
        **result_record,
        result_SHA256=_digest_from_record(RESULT_DIGEST_ALGORITHM, result_record),
    )
    validate_non_critical_ticket_pilot_result(result)
    return result


def validate_non_critical_ticket_pilot_result(
    result: NonCriticalTicketPilotResult,
) -> None:
    """Validate one immutable P17.8 pilot result."""

    try:
        validated = NonCriticalTicketPilotResult.model_validate(
            result.model_dump(mode="json")
        )
    except (AttributeError, ValueError) as exc:
        raise NonCriticalTicketPilotValidationError("invalid pilot result") from exc
    _validate_result_integrity(
        validated,
        error_type=NonCriticalTicketPilotValidationError,
    )


def summarize_non_critical_ticket_pilot(
    result: NonCriticalTicketPilotResult,
) -> PilotAcceptanceSummary:
    """Return the exact immutable acceptance summary after result validation."""

    validate_non_critical_ticket_pilot_result(result)
    return result.acceptance_summary


def _validated_request(
    request: NonCriticalTicketPilotRequest,
) -> NonCriticalTicketPilotRequest:
    try:
        return NonCriticalTicketPilotRequest.model_validate(request)
    except (AttributeError, ValueError) as exc:
        raise NonCriticalTicketPilotInputError("invalid pilot request") from exc


def _validate_schema_policy(request: NonCriticalTicketPilotRequest) -> None:
    if request.schema_version != NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION:
        raise NonCriticalTicketPilotInputError("schema version mismatch")
    if request.policy_id != NON_CRITICAL_TICKET_PILOT_POLICY_ID:
        raise NonCriticalTicketPilotInputError("policy ID mismatch")


def _validate_policy(policy: PilotEligibilityPolicy) -> None:
    try:
        PilotEligibilityPolicy.model_validate(policy.model_dump(mode="json"))
    except (AttributeError, ValueError) as exc:
        raise NonCriticalTicketPilotIntegrityError(
            "invalid eligibility policy"
        ) from exc


def _validate_selection_digest(selection: PilotTicketSelection) -> None:
    if not _selection_digest_matches(selection):
        raise NonCriticalTicketPilotIntegrityError("selection digest mismatch")


def _validate_prerequisite_digests(
    request: NonCriticalTicketPilotRequest,
    *,
    strict_state: bool,
) -> None:
    _validate_work_packet_digest(request.compilation_result.work_packet)
    _call_validator(
        lambda: validate_workspace_allocation(request.allocation_result.allocation),
        "workspace allocation",
    )
    _call_validator(
        lambda: validate_tool_permission_profile(request.profile_result.profile),
        "tool permission profile",
    )
    _call_validator(
        lambda: validate_single_agent_execution_result(
            request.single_agent_execution_result
        ),
        "single-agent execution result",
    )
    _call_validator(
        lambda: validate_validation_command_runner_result(
            request.validation_command_runner_result
        ),
        "validation command runner result",
    )
    _validate_outcome_for_request(request.outcome_envelope, strict_state)
    _validate_review_for_request(request.diff_artifact_review_result, strict_state)
    _validate_handoff_for_request(request.human_git_handoff_result, strict_state)


def _validate_work_packet_digest(work_packet: WorkPacket) -> None:
    try:
        validate_work_packet(work_packet)
    except ValueError as exc:
        raise NonCriticalTicketPilotIntegrityError("invalid WorkPacket") from exc


def _validate_review_for_request(
    result: DiffArtifactReviewResult,
    strict_state: bool,
) -> None:
    try:
        validate_diff_artifact_review_result(result)
    except ValueError as exc:
        if strict_state:
            raise NonCriticalTicketPilotStateError(
                "invalid diff artifact review result"
            ) from exc


def _validate_outcome_for_request(outcome: OutcomeEnvelope, strict_state: bool) -> None:
    try:
        validate_outcome_envelope(outcome)
    except ValueError as exc:
        if strict_state:
            raise NonCriticalTicketPilotStateError("invalid outcome envelope") from exc


def _validate_handoff_for_request(result: GitHandoffResult, strict_state: bool) -> None:
    try:
        validate_human_git_handoff_result(result)
    except ValueError as exc:
        if strict_state:
            raise NonCriticalTicketPilotStateError(
                "invalid human Git handoff result"
            ) from exc


def _call_validator(callback, label: str) -> None:
    try:
        callback()
    except ValueError as exc:
        raise NonCriticalTicketPilotIntegrityError(f"invalid {label}") from exc


def _validate_cross_contract_bindings(request: NonCriticalTicketPilotRequest) -> None:
    packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    execution = request.single_agent_execution_result
    validation = request.validation_command_runner_result
    outcome = _selected_outcome(request.outcome_envelope)
    review = request.diff_artifact_review_result
    handoff = request.human_git_handoff_result
    _require_binding(
        allocation.work_packet_id, packet.work_packet_id, "allocation WorkPacket"
    )
    _require_binding(
        allocation.work_packet_SHA256,
        packet.work_packet_SHA256,
        "allocation WorkPacket digest",
    )
    _require_binding(
        profile.work_packet_id, packet.work_packet_id, "profile WorkPacket"
    )
    _require_binding(
        profile.work_packet_SHA256,
        packet.work_packet_SHA256,
        "profile WorkPacket digest",
    )
    _require_binding(
        profile.allocation_id, allocation.allocation_id, "profile allocation"
    )
    _require_binding(
        profile.allocation_SHA256,
        allocation.allocation_SHA256,
        "profile allocation digest",
    )
    for label, source in (
        ("execution", execution.session),
        ("validation", validation.session),
        ("outcome", outcome),
        ("review", review),
        ("handoff", handoff),
    ):
        _require_binding(
            source.work_packet_id, packet.work_packet_id, f"{label} WorkPacket"
        )
        _require_binding(
            source.work_packet_SHA256,
            packet.work_packet_SHA256,
            f"{label} WorkPacket digest",
        )
        _require_binding(
            source.allocation_id, allocation.allocation_id, f"{label} allocation"
        )
        _require_binding(
            source.allocation_SHA256,
            allocation.allocation_SHA256,
            f"{label} allocation digest",
        )
        _require_binding(source.profile_id, profile.profile_id, f"{label} profile")
        _require_binding(
            source.profile_SHA256, profile.profile_SHA256, f"{label} profile digest"
        )
    _require_binding(
        validation.session.single_agent_result_SHA256,
        execution.result_SHA256,
        "validation execution digest",
    )
    if outcome.single_agent_result_SHA256 is not None:
        _require_binding(
            outcome.single_agent_result_SHA256,
            execution.result_SHA256,
            "outcome execution digest",
        )
    if outcome.validation_command_runner_result_SHA256 is not None:
        _require_binding(
            outcome.validation_command_runner_result_SHA256,
            validation.result_SHA256,
            "outcome validation digest",
        )
    _require_binding(
        review.outcome_SHA256,
        request.outcome_envelope.envelope_SHA256,
        "review outcome",
    )
    _require_binding(
        handoff.outcome_SHA256,
        request.outcome_envelope.envelope_SHA256,
        "handoff outcome",
    )
    _require_binding(handoff.review_id, review.review_id, "handoff review")
    _require_binding(
        handoff.review_SHA256, review.result_SHA256, "handoff review digest"
    )


def _require_binding(left: str, right: str, label: str) -> None:
    if left != right:
        raise NonCriticalTicketPilotIntegrityError(f"{label} binding mismatch")


def _validate_selected_ticket_identity(request: NonCriticalTicketPilotRequest) -> None:
    packet = request.compilation_result.work_packet
    selection = request.selection
    if selection.ticket_id != packet.ticket_id:
        raise NonCriticalTicketPilotPolicyError("selected ticket ID mismatch")
    if selection.ticket_revision != packet.publication_revision:
        raise NonCriticalTicketPilotPolicyError("selected ticket revision mismatch")
    source_title = getattr(packet.source_ticket, "title", None)
    if source_title is not None and selection.ticket_title != source_title:
        raise NonCriticalTicketPilotPolicyError("selected ticket title mismatch")


def _derive_candidate_paths(
    request: NonCriticalTicketPilotRequest,
    *,
    require_review_match: bool = True,
) -> tuple[str, ...]:
    from_review = tuple(
        path.relative_path
        for path in request.diff_artifact_review_result.observed_paths
    )
    from_handoff = tuple(
        candidate.relative_path
        for candidate in request.human_git_handoff_result.package.candidates
    )
    if require_review_match and from_review != from_handoff:
        raise NonCriticalTicketPilotPolicyError("review to handoff candidate mismatch")
    return from_handoff


def _derive_validation_ids(request: NonCriticalTicketPilotRequest) -> tuple[str, ...]:
    validation = request.validation_command_runner_result
    ids = tuple(validation.passed_validation_ids) + tuple(
        validation.manual_validation_ids_pending
    )
    _reject_duplicate_values(ids, "validation IDs")
    return ids


def _derive_stage_evidence(
    request: NonCriticalTicketPilotRequest,
) -> tuple[PilotStageEvidence, ...]:
    packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    sources = (
        _stage_source(
            PilotStage.WORK_PACKET_COMPILATION,
            packet.work_packet_id,
            request.compilation_result.result_SHA256,
            _compilation_stage_satisfied(request.compilation_result),
            0,
            0,
            False,
            0,
            "P17.0 WorkPacket compilation evidence is complete and non-executing.",
        ),
        _stage_source(
            PilotStage.WORKSPACE_ALLOCATION,
            allocation.allocation_id,
            request.allocation_result.result_SHA256,
            _allocation_stage_satisfied(request.allocation_result),
            0,
            0,
            False,
            0,
            "P17.1 human-provisioned exclusive linked workspace is allocated.",
        ),
        _stage_source(
            PilotStage.TOOL_PERMISSION_PROFILE,
            profile.profile_id,
            request.profile_result.result_SHA256,
            _profile_stage_satisfied(request.profile_result),
            0,
            0,
            False,
            0,
            "P17.2 deny-first tool permission profile is ready.",
        ),
        _stage_source(
            PilotStage.SINGLE_AGENT_EXECUTION,
            request.single_agent_execution_result.session.session_id,
            request.single_agent_execution_result.result_SHA256,
            _single_agent_stage_satisfied(request.single_agent_execution_result),
            request.single_agent_execution_result.provider_dispatch_count,
            request.single_agent_execution_result.model_inference_count,
            False,
            0,
            "P17.3 single-agent execution completed without provider or model calls.",
        ),
        _stage_source(
            PilotStage.VALIDATION_COMMAND_RUNNER,
            request.validation_command_runner_result.session.session_id,
            request.validation_command_runner_result.result_SHA256,
            _validation_stage_satisfied(request.validation_command_runner_result),
            request.validation_command_runner_result.provider_dispatch_count,
            request.validation_command_runner_result.model_inference_count,
            False,
            0,
            "P17.4 exact validation-command runner completed accepted commands.",
        ),
        _stage_source(
            PilotStage.OUTCOME_ENVELOPE,
            request.outcome_envelope.envelope_id,
            request.outcome_envelope.envelope_SHA256,
            _outcome_stage_satisfied(request.outcome_envelope),
            request.outcome_envelope.provider_dispatch_count,
            request.outcome_envelope.model_inference_count,
            _outcome_automatic_authority_present(request.outcome_envelope),
            0,
            "P17.5 terminal result outcome is present and does not pre-authorize review or handoff.",
        ),
        _stage_source(
            PilotStage.DIFF_ARTIFACT_REVIEW,
            request.diff_artifact_review_result.review_id,
            request.diff_artifact_review_result.result_SHA256,
            _review_stage_satisfied(request.diff_artifact_review_result),
            request.diff_artifact_review_result.provider_dispatch_count,
            request.diff_artifact_review_result.model_inference_count,
            _review_automatic_authority_present(request.diff_artifact_review_result),
            0,
            "P17.6 diff and artifact review completed without automatic cleanup, rollback or staging.",
        ),
        _stage_source(
            PilotStage.HUMAN_GIT_HANDOFF,
            request.human_git_handoff_result.handoff_id,
            request.human_git_handoff_result.result_SHA256,
            _handoff_stage_satisfied(request.human_git_handoff_result),
            request.human_git_handoff_result.provider_dispatch_count,
            request.human_git_handoff_result.model_inference_count,
            _handoff_automatic_authority_present(request.human_git_handoff_result),
            request.human_git_handoff_result.Git_commands_executed,
            "P17.7 human-only Git handoff completed with Git commands unexecuted.",
        ),
    )
    return tuple(
        _build_stage_evidence(
            source,
            ticket_id=packet.ticket_id,
            work_packet_SHA256=packet.work_packet_SHA256,
            allocation_SHA256=allocation.allocation_SHA256,
            profile_SHA256=profile.profile_SHA256,
        )
        for source in sources
    )


def _stage_source(
    stage: PilotStage,
    source_id: str,
    source_SHA256: str,
    requirement_satisfied: bool,
    provider_dispatch_count: int,
    model_inference_count: int,
    automatic_authority_present: bool,
    Git_execution_count: int,
    summary: str,
) -> tuple[PilotStage, str, str, bool, int, int, bool, int, str]:
    return (
        stage,
        source_id,
        source_SHA256,
        requirement_satisfied,
        provider_dispatch_count,
        model_inference_count,
        automatic_authority_present,
        Git_execution_count,
        summary,
    )


def _build_stage_evidence(
    source: tuple[PilotStage, str, str, bool, int, int, bool, int, str],
    *,
    ticket_id: str,
    work_packet_SHA256: str,
    allocation_SHA256: str,
    profile_SHA256: str,
) -> PilotStageEvidence:
    (
        stage,
        source_id,
        source_SHA256,
        requirement_satisfied,
        provider_dispatch_count,
        model_inference_count,
        automatic_authority_present,
        Git_execution_count,
        summary,
    ) = source
    data = {
        "evidence_id": _stage_evidence_id(stage),
        "stage": stage,
        "requirement_satisfied": requirement_satisfied,
        "source_id": source_id,
        "source_SHA256": source_SHA256,
        "ticket_id": ticket_id,
        "work_packet_SHA256": work_packet_SHA256,
        "allocation_SHA256": allocation_SHA256,
        "profile_SHA256": profile_SHA256,
        "provider_dispatch_count": provider_dispatch_count,
        "model_inference_count": model_inference_count,
        "automatic_authority_present": automatic_authority_present,
        "Git_execution_count": Git_execution_count,
        "summary": summary,
    }
    return PilotStageEvidence(
        **data,
        evidence_SHA256=_digest_from_record(STAGE_EVIDENCE_DIGEST_ALGORITHM, data),
    )


def _derive_findings(
    request: NonCriticalTicketPilotRequest,
    stage_evidence: tuple[PilotStageEvidence, ...],
) -> tuple[PilotFinding, ...]:
    records: list[
        tuple[PilotFindingSeverity, PilotFindingCode, PilotStage | None, str, str, str]
    ] = []
    records.extend(_eligibility_finding_records(request))
    for evidence in stage_evidence:
        if evidence.requirement_satisfied:
            records.append((
                PilotFindingSeverity.INFO,
                PilotFindingCode.STAGE_EVIDENCE_COMPLETE,
                evidence.stage,
                evidence.source_id,
                "Stage evidence is complete for the bound WorkPacket chain.",
                "stage requirement satisfied",
            ))
        else:
            records.append((
                PilotFindingSeverity.BLOCKING,
                PilotFindingCode.STAGE_NOT_COMPLETED,
                evidence.stage,
                evidence.source_id,
                "Stage evidence is incomplete or not accepted.",
                "stage requirement not satisfied",
            ))
        if evidence.provider_dispatch_count:
            records.append((
                PilotFindingSeverity.BLOCKING,
                PilotFindingCode.PROVIDER_AUTHORITY_PRESENT,
                evidence.stage,
                evidence.source_id,
                "Provider dispatch authority or count is present.",
                "provider dispatch count must be zero",
            ))
        if evidence.model_inference_count:
            records.append((
                PilotFindingSeverity.BLOCKING,
                PilotFindingCode.MODEL_AUTHORITY_PRESENT,
                evidence.stage,
                evidence.source_id,
                "Model inference authority or count is present.",
                "model inference count must be zero",
            ))
        if evidence.automatic_authority_present:
            records.append((
                PilotFindingSeverity.BLOCKING,
                PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
                evidence.stage,
                evidence.source_id,
                "Automatic authority is present on a prerequisite stage.",
                "automatic authority must be false",
            ))
        if evidence.Git_execution_count:
            records.append((
                PilotFindingSeverity.BLOCKING,
                PilotFindingCode.GIT_EXECUTION_PRESENT,
                evidence.stage,
                evidence.source_id,
                "Git execution evidence is present in the handoff chain.",
                "Git execution count must be zero",
            ))
    manual_ids = _manual_validation_ids(request)
    if manual_ids:
        records.append((
            PilotFindingSeverity.WARNING,
            PilotFindingCode.MANUAL_VALIDATION_PENDING,
            PilotStage.VALIDATION_COMMAND_RUNNER,
            request.validation_command_runner_result.session.session_id,
            "Manual validation IDs remain pending and are preserved.",
            "manual validation pending IDs must not be dropped",
        ))
    has_blocking = any(item[0] is PilotFindingSeverity.BLOCKING for item in records)
    if has_blocking:
        records.append((
            PilotFindingSeverity.BLOCKING,
            PilotFindingCode.PILOT_REJECTED,
            None,
            request.selection.selection_id,
            "Pilot is rejected because blocking findings are present.",
            "accepted pilot requires zero blocking findings",
        ))
    else:
        records.append((
            PilotFindingSeverity.INFO,
            PilotFindingCode.PILOT_ACCEPTED,
            None,
            request.selection.selection_id,
            "Pilot is accepted for one bounded non-critical ticket.",
            "all acceptance criteria satisfied",
        ))
    return _build_findings(records)


def _eligibility_finding_records(
    request: NonCriticalTicketPilotRequest,
) -> tuple[
    tuple[PilotFindingSeverity, PilotFindingCode, PilotStage | None, str, str, str], ...
]:
    records: list[
        tuple[PilotFindingSeverity, PilotFindingCode, PilotStage | None, str, str, str]
    ] = []
    selection = request.selection
    handoff = request.human_git_handoff_result
    candidate_paths = tuple(
        candidate.relative_path for candidate in handoff.package.candidates
    )
    added_count = sum(
        1
        for candidate in handoff.package.candidates
        if candidate.status is GitHandoffPathStatus.ADDED
    )
    modified_count = sum(
        1
        for candidate in handoff.package.candidates
        if candidate.status is GitHandoffPathStatus.MODIFIED
    )
    deleted_count = sum(
        1
        for candidate in handoff.package.candidates
        if candidate.status is GitHandoffPathStatus.DELETED
    )
    policy = request.eligibility_policy
    if selection.risk_class is not PilotRiskClass.NON_CRITICAL:
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_CRITICAL,
                selection.selection_id,
                "Ticket risk is outside the non-critical pilot policy.",
                "risk class must be non_critical",
            )
        )
    if len(candidate_paths) > policy.maximum_files_changed:
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_SECURITY_SENSITIVE,
                selection.selection_id,
                "Ticket changes more files than the non-critical pilot limit.",
                "changed file count must be at most ten",
            )
        )
    if added_count > policy.maximum_created_files:
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_SECURITY_SENSITIVE,
                selection.selection_id,
                "Ticket creates more files than the non-critical pilot limit.",
                "created file count must be at most five",
            )
        )
    if modified_count > policy.maximum_modified_files:
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_SECURITY_SENSITIVE,
                selection.selection_id,
                "Ticket modifies more files than the non-critical pilot limit.",
                "modified file count must be at most ten",
            )
        )
    if deleted_count > policy.maximum_deleted_files:
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_SECURITY_SENSITIVE,
                selection.selection_id,
                "Ticket includes deleted-file evidence, which the pilot excludes.",
                "deleted file count must be zero",
            )
        )
    if any(_is_dependency_path(path) for path in candidate_paths):
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_DEPENDENCY_MUTATION_REQUIRED,
                selection.selection_id,
                "Ticket candidate paths include dependency configuration.",
                "dependency changes must be absent",
            )
        )
    if any(_is_lockfile_path(path) for path in candidate_paths):
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_DEPENDENCY_MUTATION_REQUIRED,
                selection.selection_id,
                "Ticket candidate paths include a lockfile.",
                "lockfile changes must be absent",
            )
        )
    if any(_is_credential_path(path) for path in candidate_paths):
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_SECURITY_SENSITIVE,
                selection.selection_id,
                "Ticket candidate paths include credential-sensitive material.",
                "credentials must be absent",
            )
        )
    if _work_packet_requires_external_access(request.compilation_result.work_packet):
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_EXTERNAL_ACCESS_REQUIRED,
                selection.selection_id,
                "WorkPacket scope requires external access or networked authority.",
                "external access must be absent",
            )
        )
    if _work_packet_requires_git_mutation(request.compilation_result.work_packet):
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.TICKET_GIT_MUTATION_REQUIRED,
                selection.selection_id,
                "WorkPacket scope requires Git mutation or branch authority.",
                "Git mutation must be absent",
            )
        )
    if not _has_exact_validation_commands(request):
        records.append(
            _blocking_ticket_record(
                PilotFindingCode.STAGE_EVIDENCE_MISSING,
                request.validation_command_runner_result.session.session_id,
                "Exact validation command evidence is missing.",
                "completed validation command evidence required",
            )
        )
    if (
        tuple(
            path.relative_path
            for path in request.diff_artifact_review_result.observed_paths
        )
        != candidate_paths
    ):
        records.append((
            PilotFindingSeverity.BLOCKING,
            PilotFindingCode.STAGE_BINDING_MISMATCH,
            PilotStage.HUMAN_GIT_HANDOFF,
            handoff.handoff_id,
            "Human Git handoff candidates differ from diff review paths.",
            "reviewed paths must match handoff candidates",
        ))
    if not records:
        records.append((
            PilotFindingSeverity.INFO,
            PilotFindingCode.TICKET_ELIGIBLE,
            None,
            selection.selection_id,
            "Ticket is eligible for the non-critical governed pilot.",
            "non-critical eligibility satisfied",
        ))
    return tuple(records)


def _blocking_ticket_record(
    code: PilotFindingCode,
    source_id: str,
    summary: str,
    failed_invariant: str,
) -> tuple[PilotFindingSeverity, PilotFindingCode, PilotStage | None, str, str, str]:
    return (
        PilotFindingSeverity.BLOCKING,
        code,
        None,
        source_id,
        summary,
        failed_invariant,
    )


def _build_findings(
    records: list[
        tuple[PilotFindingSeverity, PilotFindingCode, PilotStage | None, str, str, str]
    ],
) -> tuple[PilotFinding, ...]:
    sorted_records = tuple(sorted(records, key=_finding_record_sort_key))
    if len(sorted_records) > 128:
        raise NonCriticalTicketPilotPolicyError("too many pilot findings")
    findings: list[PilotFinding] = []
    for index, record in enumerate(sorted_records, start=1):
        severity, code, stage, source_id, summary, failed_invariant = record
        data = {
            "finding_id": f"PFND-{index:03d}",
            "severity": severity,
            "code": code,
            "stage": stage,
            "source_id": source_id,
            "summary": summary,
            "failed_invariant": failed_invariant,
        }
        findings.append(
            PilotFinding(
                **data,
                finding_SHA256=_digest_from_record(FINDING_DIGEST_ALGORITHM, data),
            )
        )
    return tuple(findings)


def _derive_acceptance_summary(
    request: NonCriticalTicketPilotRequest,
    stage_evidence: tuple[PilotStageEvidence, ...],
    findings: tuple[PilotFinding, ...],
) -> PilotAcceptanceSummary:
    blocking = sum(
        1 for finding in findings if finding.severity is PilotFindingSeverity.BLOCKING
    )
    warning = sum(
        1 for finding in findings if finding.severity is PilotFindingSeverity.WARNING
    )
    info = sum(
        1 for finding in findings if finding.severity is PilotFindingSeverity.INFO
    )
    provider_count = sum(
        evidence.provider_dispatch_count for evidence in stage_evidence
    )
    model_count = sum(evidence.model_inference_count for evidence in stage_evidence)
    git_count = sum(evidence.Git_execution_count for evidence in stage_evidence)
    data = {
        "eligible": blocking == 0,
        "stage_count": len(stage_evidence),
        "completed_stage_count": sum(
            1 for evidence in stage_evidence if evidence.requirement_satisfied
        ),
        "blocking_finding_count": blocking,
        "warning_finding_count": warning,
        "information_finding_count": info,
        "manual_validation_ids_pending": _manual_validation_ids(request),
        "Git_commands_executed": git_count,
        "provider_dispatch_count": provider_count,
        "model_inference_count": model_count,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_cleanup_authorized": False,
        "automatic_rollback_authorized": False,
        "automatic_staging_authorized": False,
        "automatic_commit_authorized": False,
        "automatic_push_authorized": False,
    }
    return PilotAcceptanceSummary(
        **data,
        summary_SHA256=_digest_from_record(ACCEPTANCE_SUMMARY_DIGEST_ALGORITHM, data),
    )


def _is_accepted(
    stage_evidence: tuple[PilotStageEvidence, ...],
    findings: tuple[PilotFinding, ...],
    summary: PilotAcceptanceSummary,
) -> bool:
    return (
        summary.eligible
        and len(stage_evidence) == 8
        and all(evidence.requirement_satisfied for evidence in stage_evidence)
        and summary.blocking_finding_count == 0
        and summary.Git_commands_executed == 0
        and summary.provider_dispatch_count == 0
        and summary.model_inference_count == 0
        and not any(
            finding.severity is PilotFindingSeverity.BLOCKING for finding in findings
        )
    )


def _result_base_data(
    *,
    request: NonCriticalTicketPilotRequest,
    stage_evidence: tuple[PilotStageEvidence, ...],
    findings: tuple[PilotFinding, ...],
    acceptance_summary: PilotAcceptanceSummary,
    decision: PilotDecision,
    state: PilotState,
    mvp_ready: bool,
    closure_ready: bool,
) -> dict[str, object]:
    packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    return {
        "schema_version": NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION,
        "policy_id": NON_CRITICAL_TICKET_PILOT_POLICY_ID,
        "state": state,
        "decision": decision,
        "risk_class": PilotRiskClass.NON_CRITICAL,
        "ticket_id": packet.ticket_id,
        "ticket_revision": packet.publication_revision,
        "selection_SHA256": request.selection.selection_SHA256,
        "eligibility_policy_SHA256": request.eligibility_policy.policy_SHA256,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "profile_id": profile.profile_id,
        "profile_SHA256": profile.profile_SHA256,
        "execution_result_SHA256": request.single_agent_execution_result.result_SHA256,
        "validation_result_SHA256": request.validation_command_runner_result.result_SHA256,
        "outcome_SHA256": request.outcome_envelope.envelope_SHA256,
        "review_SHA256": request.diff_artifact_review_result.result_SHA256,
        "handoff_SHA256": request.human_git_handoff_result.result_SHA256,
        "stage_evidence": stage_evidence,
        "findings": findings,
        "acceptance_summary": acceptance_summary,
        "WorkPacket_execution_MVP_requirement_satisfied": mvp_ready,
        "P17_closure_ready": closure_ready,
        "production_readiness_claimed": False,
        "provider_dispatch_count": acceptance_summary.provider_dispatch_count,
        "model_inference_count": acceptance_summary.model_inference_count,
    }


def _validate_result_integrity(
    result: NonCriticalTicketPilotResult, error_type
) -> None:
    _validate_stage_evidence_collection(result.stage_evidence, error_type=error_type)
    _validate_finding_collection(result.findings, error_type=error_type)
    if result.pilot_id != _pilot_id_from_result(result):
        raise error_type("pilot ID mismatch")
    accepted = result.decision is PilotDecision.ACCEPTED
    if accepted:
        if result.state is not PilotState.COMPLETED:
            raise error_type("accepted pilot must be completed")
        if not result.WorkPacket_execution_MVP_requirement_satisfied:
            raise error_type("accepted pilot must satisfy WorkPacket MVP")
        if not result.P17_closure_ready:
            raise error_type("accepted pilot must mark P17 closure ready")
    else:
        if result.state is not PilotState.BLOCKED:
            raise error_type("rejected pilot must be blocked")
        if result.WorkPacket_execution_MVP_requirement_satisfied:
            raise error_type("rejected pilot cannot satisfy WorkPacket MVP")
        if result.P17_closure_ready:
            raise error_type("rejected pilot cannot mark P17 closure ready")
    if result.production_readiness_claimed is not False:
        raise error_type("production readiness must remain false")
    blocking = sum(
        1
        for finding in result.findings
        if finding.severity is PilotFindingSeverity.BLOCKING
    )
    warning = sum(
        1
        for finding in result.findings
        if finding.severity is PilotFindingSeverity.WARNING
    )
    info = sum(
        1
        for finding in result.findings
        if finding.severity is PilotFindingSeverity.INFO
    )
    if result.acceptance_summary.blocking_finding_count != blocking:
        raise error_type("blocking finding count mismatch")
    if result.acceptance_summary.warning_finding_count != warning:
        raise error_type("warning finding count mismatch")
    if result.acceptance_summary.information_finding_count != info:
        raise error_type("information finding count mismatch")
    if result.acceptance_summary.stage_count != len(result.stage_evidence):
        raise error_type("stage count mismatch")
    if result.acceptance_summary.completed_stage_count != sum(
        1 for evidence in result.stage_evidence if evidence.requirement_satisfied
    ):
        raise error_type("completed stage count mismatch")
    if (
        result.provider_dispatch_count
        != result.acceptance_summary.provider_dispatch_count
    ):
        raise error_type("provider dispatch count mismatch")
    if result.model_inference_count != result.acceptance_summary.model_inference_count:
        raise error_type("model inference count mismatch")
    if accepted != (blocking == 0 and result.acceptance_summary.eligible):
        raise error_type("decision derivation mismatch")
    if result.result_SHA256 != _model_digest(RESULT_DIGEST_ALGORITHM, result):
        raise error_type("result_SHA256 must match pilot result digest")


def _validate_stage_evidence_collection(
    values: tuple[PilotStageEvidence, ...], *, error_type
) -> None:
    if len(values) != 8:
        raise error_type("stage evidence count must be exactly eight")
    if tuple(value.stage for value in values) != tuple(PilotStage):
        raise error_type("stage evidence order mismatch")
    expected_ids = tuple(f"PSEV-{index:03d}" for index in range(1, 9))
    if tuple(value.evidence_id for value in values) != expected_ids:
        raise error_type("stage evidence IDs must be contiguous")
    for value in values:
        if value.evidence_SHA256 != _model_digest(
            STAGE_EVIDENCE_DIGEST_ALGORITHM, value
        ):
            raise error_type("stage evidence digest mismatch")


def _validate_finding_collection(
    values: tuple[PilotFinding, ...], *, error_type
) -> None:
    if len(values) > 128:
        raise error_type("too many pilot findings")
    expected_ids = tuple(f"PFND-{index:03d}" for index in range(1, len(values) + 1))
    if tuple(value.finding_id for value in values) != expected_ids:
        raise error_type("finding IDs must be contiguous")
    sort_key = tuple(_finding_sort_key(value) for value in values)
    if sort_key != tuple(sorted(sort_key)):
        raise error_type("finding order mismatch")
    for value in values:
        if value.finding_SHA256 != _model_digest(FINDING_DIGEST_ALGORITHM, value):
            raise error_type("finding digest mismatch")


def _compilation_stage_satisfied(result: WorkPacketCompilationResult) -> bool:
    packet = result.work_packet
    return (
        result.disposition is WorkPacketCompilationDisposition.COMPILED
        and packet.authority_boundary is WorkPacketAuthorityBoundary.COMPILE_ONLY
        and packet.execution_ready is False
        and all(
            step.command_execution_authorized is False
            for step in packet.validation_steps
        )
    )


def _allocation_stage_satisfied(result: WorkspaceAllocationResult) -> bool:
    allocation = result.allocation
    return (
        allocation.lifecycle_state is WorkspaceLifecycleState.ALLOCATED
        and allocation.workspace_kind is WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE
        and allocation.exclusive is True
        and allocation.workspace_requirement_satisfied is True
        and allocation.inspection_evidence.linked_worktree is True
        and allocation.git_authority.value == "human_only"
    )


def _profile_stage_satisfied(result: ToolPermissionProfileResult) -> bool:
    profile = result.profile
    denied = frozenset(profile.denied_operations)
    return (
        profile.tool_permissions_ready is True
        and profile.execution_ready is False
        and _DENY_FIRST_REQUIRED_OPERATIONS.issubset(denied)
    )


def _single_agent_stage_satisfied(result: SingleAgentExecutionResult) -> bool:
    return (
        result.state is SingleAgentExecutionState.COMPLETED
        and result.single_agent_execution_requirement_satisfied is True
        and result.provider_dispatch_count == 0
        and result.model_inference_count == 0
    )


def _validation_stage_satisfied(result: ValidationCommandRunnerResult) -> bool:
    return (
        result.state is ValidationCommandRunnerState.COMPLETED
        and result.validation_command_runner_requirement_satisfied is True
        and result.provider_dispatch_count == 0
        and result.model_inference_count == 0
        and all(
            evidence.disposition is ValidationCommandDisposition.PASSED
            for evidence in result.session.command_evidence
        )
    )


def _outcome_stage_satisfied(outcome: OutcomeEnvelope) -> bool:
    return (
        outcome.envelope_kind is OutcomeEnvelopeKind.RESULT
        and outcome.result_envelopes_ready is True
        and outcome.diff_artifact_review_ready is False
        and outcome.human_git_handoff_ready is False
        and outcome.provider_dispatch_count == 0
        and outcome.model_inference_count == 0
        and not _outcome_automatic_authority_present(outcome)
    )


def _review_stage_satisfied(result: DiffArtifactReviewResult) -> bool:
    return (
        result.state is AggregateReviewState.COMPLETED
        and result.diff_artifact_review_requirement_satisfied is True
        and not any(
            finding.severity is ReviewFindingSeverity.BLOCKING
            for finding in result.findings
        )
        and not _review_automatic_authority_present(result)
        and result.provider_dispatch_count == 0
        and result.model_inference_count == 0
    )


def _handoff_stage_satisfied(result: GitHandoffResult) -> bool:
    return (
        result.state is GitHandoffState.COMPLETED
        and result.decision is GitHandoffDecision.APPROVED
        and result.authority is GitHandoffAuthority.HUMAN_ONLY
        and result.human_git_handoff_requirement_satisfied is True
        and result.Git_commands_executed == 0
        and result.staging_performed is False
        and result.commit_performed is False
        and result.push_performed is False
        and not _handoff_automatic_authority_present(result)
        and result.provider_dispatch_count == 0
        and result.model_inference_count == 0
    )


def _selected_outcome(outcome: OutcomeEnvelope):
    if outcome.result_envelope is not None:
        return outcome.result_envelope
    if outcome.failure_envelope is not None:
        return outcome.failure_envelope
    if outcome.cancellation_envelope is not None:
        return outcome.cancellation_envelope
    raise NonCriticalTicketPilotStateError("outcome envelope is empty")


def _outcome_automatic_authority_present(outcome: OutcomeEnvelope) -> bool:
    return bool(
        outcome.automatic_retry_authorized
        or outcome.automatic_fallback_authorized
        or outcome.automatic_resubmission_authorized
    )


def _review_automatic_authority_present(result: DiffArtifactReviewResult) -> bool:
    return bool(
        result.automatic_cleanup_authorized
        or result.automatic_rollback_authorized
        or result.automatic_staging_authorized
    )


def _handoff_automatic_authority_present(result: GitHandoffResult) -> bool:
    return bool(
        result.automatic_cleanup_authorized
        or result.automatic_rollback_authorized
        or result.automatic_staging_authorized
        or result.automatic_commit_authorized
        or result.automatic_push_authorized
        or result.staging_performed
        or result.commit_performed
        or result.push_performed
    )


def _manual_validation_ids(request: NonCriticalTicketPilotRequest) -> tuple[str, ...]:
    runner_ids = tuple(
        request.validation_command_runner_result.manual_validation_ids_pending
    )
    outcome = _selected_outcome(request.outcome_envelope)
    review_ids = tuple(
        request.diff_artifact_review_result.manual_validation_ids_pending
    )
    handoff_ids = tuple(request.human_git_handoff_result.manual_validation_ids_pending)
    if tuple(outcome.manual_validation_ids_pending) != runner_ids:
        raise NonCriticalTicketPilotIntegrityError(
            "outcome manual validation IDs mismatch"
        )
    if review_ids != runner_ids:
        raise NonCriticalTicketPilotIntegrityError(
            "review manual validation IDs mismatch"
        )
    if handoff_ids != runner_ids:
        raise NonCriticalTicketPilotIntegrityError(
            "handoff manual validation IDs mismatch"
        )
    return runner_ids


def _has_exact_validation_commands(request: NonCriticalTicketPilotRequest) -> bool:
    command_ids = tuple(
        step.validation_id
        for step in request.compilation_result.work_packet.validation_steps
        if step.command is not None
    )
    passed_ids = tuple(request.validation_command_runner_result.passed_validation_ids)
    return bool(command_ids) and command_ids == passed_ids


def _work_packet_requires_external_access(packet: WorkPacket) -> bool:
    text = _work_packet_action_text(packet)
    return any(
        marker in text
        for marker in (
            "network",
            "http://",
            "https://",
            "provider",
            "model",
            "docker",
            "graphify",
            "database migration",
            "production deploy",
            "external service",
            "credential",
            "secret",
        )
    )


def _work_packet_requires_git_mutation(packet: WorkPacket) -> bool:
    text = _work_packet_action_text(packet)
    return any(marker in text for marker in _GIT_COMMAND_MARKERS) or any(
        marker in text for marker in ("branch", "merge", "rebase", "reset")
    )


def _work_packet_action_text(packet: WorkPacket) -> str:
    return " ".join(
        tuple(packet.repository_scope.allowed_actions)
        + tuple(packet.repository_scope.allowed_paths)
    ).casefold()


def _is_dependency_path(path: str) -> bool:
    lower = path.casefold().rsplit("/", 1)[-1]
    return lower in _DEPENDENCY_PATHS


def _is_lockfile_path(path: str) -> bool:
    lower = path.casefold().rsplit("/", 1)[-1]
    return lower in _LOCKFILE_NAMES


def _is_credential_path(path: str) -> bool:
    lower = path.casefold()
    return any(marker in lower for marker in _CREDENTIAL_PATH_MARKERS)


def _stage_evidence_id(stage: PilotStage) -> str:
    return f"PSEV-{tuple(PilotStage).index(stage) + 1:03d}"


def _normalize_ticket_id(ticket_id: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", ticket_id.strip().upper()).strip("-")
    if not normalized:
        raise ValueError("ticket ID cannot normalize to empty")
    return normalized


def _selection_id(selection: PilotTicketSelection) -> str:
    digest = _model_digest(
        SELECTION_DIGEST_ALGORITHM, selection, exclude=("selection_id",)
    )
    return (
        f"PSEL-{_normalize_ticket_id(selection.ticket_id)}-"
        f"R{selection.ticket_revision:04d}-{digest[:12]}"
    )


def _selection_digest_matches(selection: PilotTicketSelection) -> bool:
    expected_sha = _model_digest(SELECTION_DIGEST_ALGORITHM, selection)
    expected_id = _selection_id(selection)
    return (
        selection.selection_SHA256 == expected_sha
        and selection.selection_id == expected_id
    )


def _pilot_id_from_record(record: dict[str, object]) -> str:
    ticket_id = str(record["ticket_id"])
    revision = int(record["ticket_revision"])
    digest = _digest_from_record(PILOT_ID_DIGEST_ALGORITHM, record)[:12]
    return f"NCP-{_normalize_ticket_id(ticket_id)}-R{revision:04d}-{digest}"


def _pilot_id_from_result(result: NonCriticalTicketPilotResult) -> str:
    data = result.model_dump(
        mode="python",
        exclude={"pilot_id", "result_SHA256"},
    )
    return _pilot_id_from_record(data)


def _model_digest(
    algorithm: str,
    model: BaseModel,
    *,
    exclude: tuple[str, ...] = (),
) -> str:
    field_name = _digest_field_name(model)
    excluded = frozenset(exclude + (field_name,))
    return _digest_from_record(
        algorithm,
        model.model_dump(mode="python", exclude=excluded),
    )


def _digest_field_name(model: BaseModel) -> str:
    for field_name in (
        "result_SHA256",
        "policy_SHA256",
        "selection_SHA256",
        "evidence_SHA256",
        "finding_SHA256",
        "summary_SHA256",
    ):
        if field_name in model.model_fields:
            return field_name
    for field_name in model.model_fields:
        if field_name.endswith("_SHA256"):
            return field_name
    return ""


def _digest_from_record(algorithm: str, record) -> str:
    payload = {
        "algorithm": algorithm,
        "record": _canonical_jsonable(record),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _canonical_jsonable(value):
    if isinstance(value, BaseModel):
        return _canonical_jsonable(value.model_dump(mode="python"))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_canonical_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_canonical_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): _canonical_jsonable(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    return value


def _finding_record_sort_key(
    value: tuple[
        PilotFindingSeverity, PilotFindingCode, PilotStage | None, str, str, str
    ],
) -> tuple[int, int, str, str]:
    severity, code, stage, source_id, _summary, _invariant = value
    return (
        tuple(PilotFindingSeverity).index(severity),
        -1 if stage is None else tuple(PilotStage).index(stage),
        code.value,
        source_id,
    )


def _finding_sort_key(value: PilotFinding) -> tuple[int, int, str, str]:
    return (
        tuple(PilotFindingSeverity).index(value.severity),
        -1 if value.stage is None else tuple(PilotStage).index(value.stage),
        value.code.value,
        value.source_id,
    )


__all__ = (
    "NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION",
    "NON_CRITICAL_TICKET_PILOT_POLICY_ID",
    "NON_CRITICAL_TICKET_PILOT_EXPORT_COUNT",
    "PilotState",
    "PilotDecision",
    "PilotRiskClass",
    "PilotStage",
    "PilotFindingSeverity",
    "PilotFindingCode",
    "PilotEligibilityPolicy",
    "PilotTicketSelection",
    "PilotStageEvidence",
    "PilotFinding",
    "PilotAcceptanceSummary",
    "NonCriticalTicketPilotRequest",
    "NonCriticalTicketPilotResult",
    "NonCriticalTicketPilotError",
    "NonCriticalTicketPilotInputError",
    "NonCriticalTicketPilotIntegrityError",
    "NonCriticalTicketPilotPolicyError",
    "NonCriticalTicketPilotStateError",
    "NonCriticalTicketPilotValidationError",
    "build_pilot_eligibility_policy",
    "validate_non_critical_ticket_pilot_request",
    "build_non_critical_ticket_pilot",
    "validate_non_critical_ticket_pilot_result",
    "summarize_non_critical_ticket_pilot",
)
