"""P17 WorkPacket Execution MVP closure contract for Pepper.

This module is a pure deterministic reconciliation layer. It binds the
accepted P17.0 through P17.8 WorkPacket chain, records bounded closure
evidence, and emits a P18 handoff without inspecting the filesystem, invoking
Git or subprocesses, reading environment state, calling providers or models, or
claiming production readiness.
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

from hermes_cli.agent_platform.work_packet.non_critical_ticket_pilot import (
    NonCriticalTicketPilotResult,
    PilotDecision,
    PilotState,
    validate_non_critical_ticket_pilot_result,
)


WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION = 1
WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID = (
    "pepper-governed-work-packet-execution-mvp-closure-v1"
)

TICKET_ACCEPTANCE_DIGEST_ALGORITHM = "agent-platform-p17-ticket-acceptance-sha256-v1"
CAPABILITY_RECONCILIATION_DIGEST_ALGORITHM = (
    "agent-platform-p17-capability-reconciliation-sha256-v1"
)
AUTHORITY_BOUNDARY_DIGEST_ALGORITHM = "agent-platform-p17-authority-boundary-sha256-v1"
SECURITY_BOUNDARY_DIGEST_ALGORITHM = "agent-platform-p17-security-boundary-sha256-v1"
RESIDUAL_LIMITATION_DIGEST_ALGORITHM = (
    "agent-platform-p17-residual-limitation-sha256-v1"
)
P18_HANDOFF_DIGEST_ALGORITHM = "agent-platform-p17-p18-migration-handoff-sha256-v1"
CLOSURE_FINDING_DIGEST_ALGORITHM = "agent-platform-p17-closure-finding-sha256-v1"
CLOSURE_SUMMARY_DIGEST_ALGORITHM = "agent-platform-p17-closure-summary-sha256-v1"
CLOSURE_ID_DIGEST_ALGORITHM = (
    "agent-platform-p17-work-packet-execution-mvp-closure-id-sha256-v1"
)
CLOSURE_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-p17-work-packet-execution-mvp-closure-result-sha256-v1"
)

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_CLOSURE_ID_PATTERN = r"^P17C-[a-f0-9]{12}$"
_TICKET_ID_PATTERN = r"^P17\.(?:[0-8]|R)$"
_CAPABILITY_ID_PATTERN = r"^CAP-P17-[0-9]{3}$"
_LIMITATION_ID_PATTERN = r"^LIM-P17-[0-9]{3}$"
_FINDING_ID_PATTERN = r"^P17F-[0-9]{3}$"
_PROJECT_ID_PATTERN = r"^P(?:1[7-9]|2[0-1])(?:\.[0-9]+)?$"
_CONTROL_OR_ANSI_PATTERN = r"[\x00-\x1f\x7f\x1b]"
_PERSONAL_PATH_PATTERN = r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)"
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
_DIGEST_FIELD_NAMES = (
    "evidence_SHA256",
    "reconciliation_SHA256",
    "boundary_SHA256",
    "security_boundary_SHA256",
    "limitation_SHA256",
    "handoff_SHA256",
    "finding_SHA256",
    "summary_SHA256",
    "result_SHA256",
)


class P17ClosureError(ValueError):
    """Base error for P17 closure contract failures."""


class P17ClosureInputError(P17ClosureError):
    """Raised when closure inputs are structurally invalid."""


class P17ClosureIntegrityError(P17ClosureError):
    """Raised when deterministic closure digests are invalid."""


class P17ClosurePolicyError(P17ClosureError):
    """Raised when closure policy invariants are violated."""


class P17ClosureStateError(P17ClosureError):
    """Raised when prerequisite state prevents P17 closure."""


class P17ClosureValidationError(P17ClosureError):
    """Raised when a built P17 closure result fails validation."""


class P17ClosureState(str, Enum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    CLOSED = "closed"


class P17ClosureDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class P17ClosureFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class P17ClosureFindingCode(str, Enum):
    TICKET_ACCEPTED = "ticket_accepted"
    TICKET_MISSING = "ticket_missing"
    VERDICT_MISMATCH = "verdict_mismatch"
    CONTRACT_MISMATCH = "contract_mismatch"
    CHAIN_INCOMPLETE = "chain_incomplete"
    AUTHORITY_EXPANDED = "authority_expanded"
    SECURITY_BOUNDARY_MISMATCH = "security_boundary_mismatch"
    PILOT_NOT_ACCEPTED = "pilot_not_accepted"
    MVP_REQUIREMENT_UNSATISFIED = "mvp_requirement_unsatisfied"
    MANUAL_VALIDATION_PENDING = "manual_validation_pending"
    PRODUCTION_READINESS_NOT_CLAIMED = "production_readiness_not_claimed"
    CRITICAL_TICKET_SUPPORT_ABSENT = "critical_ticket_support_absent"
    PROVIDER_EXECUTION_ABSENT = "provider_execution_absent"
    MODEL_EXECUTION_ABSENT = "model_execution_absent"
    GIT_EXECUTION_ABSENT = "git_execution_absent"
    P18_REUSE_FIRST_REQUIRED = "p18_reuse_first_required"
    P18_READY = "p18_ready"
    P17_CLOSED = "p17_closed"
    P17_REJECTED = "p17_rejected"


class P17CapabilityStatus(str, Enum):
    SATISFIED = "satisfied"
    ABSENT_BY_DESIGN = "absent_by_design"
    DEFERRED = "deferred"


def _validate_bounded_text(value: str, label: str) -> str:
    if re.search(_CONTROL_OR_ANSI_PATTERN, value):
        raise ValueError(f"{label} contains control characters")
    lowered = value.lower()
    if any(marker in lowered for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} contains credential-shaped text")
    if any(marker in lowered for marker in _RAW_OUTPUT_MARKERS):
        raise ValueError(f"{label} contains raw-output marker")
    if re.search(_PERSONAL_PATH_PATTERN, value):
        raise ValueError(f"{label} contains personal absolute path")
    return value


DigestText: TypeAlias = Annotated[str, StringConstraints(pattern=_DIGEST_PATTERN)]
ClosureIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=17, max_length=17, pattern=_CLOSURE_ID_PATTERN)
]
TicketIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=5, max_length=5, pattern=_TICKET_ID_PATTERN)
]
CapabilityIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=11, max_length=11, pattern=_CAPABILITY_ID_PATTERN)
]
LimitationIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=11, max_length=11, pattern=_LIMITATION_ID_PATTERN)
]
FindingIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=8, max_length=8, pattern=_FINDING_ID_PATTERN)
]
ProjectIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=3, max_length=8, pattern=_PROJECT_ID_PATTERN)
]
TitleText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=160),
    AfterValidator(lambda value: _validate_bounded_text(value, "title")),
]
ContractText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
    AfterValidator(lambda value: _validate_bounded_text(value, "contract")),
]
SummaryText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(lambda value: _validate_bounded_text(value, "summary")),
]
InvariantText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=192),
    AfterValidator(lambda value: _validate_bounded_text(value, "invariant")),
]


class _ClosureModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class P17TicketAcceptance(_ClosureModel):
    ticket_id: TicketIdentifier
    ticket_title: TitleText
    ordinal: int = Field(ge=0, le=8, strict=True)
    accepted: StrictBool
    verdict: SummaryText
    primary_contract: ContractText
    prerequisite_ticket_ids: tuple[TicketIdentifier, ...] = Field(max_length=8)
    capability_summary: SummaryText
    authority_summary: SummaryText
    evidence_SHA256: DigestText

    @field_validator("prerequisite_ticket_ids", mode="after")
    @classmethod
    def _validate_prerequisites(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "ticket prerequisites")
        return value

    @model_validator(mode="after")
    def _validate_acceptance(self) -> P17TicketAcceptance:
        if self.evidence_SHA256 != _model_digest(
            TICKET_ACCEPTANCE_DIGEST_ALGORITHM, self
        ):
            raise ValueError("evidence_SHA256 must match ticket acceptance digest")
        return self


class P17CapabilityReconciliation(_ClosureModel):
    capability_id: CapabilityIdentifier
    capability_name: TitleText
    owner_ticket: TicketIdentifier
    status: P17CapabilityStatus
    satisfied: StrictBool
    intentionally_absent: StrictBool
    deferred_to_project: ProjectIdentifier | None = None
    authority_boundary: SummaryText
    evidence_source: SummaryText
    reconciliation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_reconciliation(self) -> P17CapabilityReconciliation:
        if self.status is P17CapabilityStatus.SATISFIED:
            if (
                not self.satisfied
                or self.intentionally_absent
                or self.deferred_to_project is not None
            ):
                raise ValueError("satisfied capability posture mismatch")
        elif self.status is P17CapabilityStatus.ABSENT_BY_DESIGN:
            if (
                self.satisfied
                or not self.intentionally_absent
                or self.deferred_to_project is not None
            ):
                raise ValueError("absent-by-design capability posture mismatch")
        else:
            if (
                self.satisfied
                or self.intentionally_absent
                or self.deferred_to_project is None
            ):
                raise ValueError("deferred capability posture mismatch")
        if self.reconciliation_SHA256 != _model_digest(
            CAPABILITY_RECONCILIATION_DIGEST_ALGORITHM, self
        ):
            raise ValueError("reconciliation_SHA256 must match capability digest")
        return self


class P17AuthorityBoundary(_ClosureModel):
    provider_dispatch_authorized: StrictBool
    model_inference_authorized: StrictBool
    network_authorized: StrictBool
    Docker_authorized: StrictBool
    Graphify_mutation_authorized: StrictBool
    automatic_retry_authorized: StrictBool
    automatic_fallback_authorized: StrictBool
    automatic_cleanup_authorized: StrictBool
    automatic_rollback_authorized: StrictBool
    automatic_staging_authorized: StrictBool
    automatic_commit_authorized: StrictBool
    automatic_push_authorized: StrictBool
    critical_ticket_execution_authorized: StrictBool
    production_execution_authorized: StrictBool
    multi_agent_execution_authorized: StrictBool
    parallel_execution_authorized: StrictBool
    human_Git_authority_required: StrictBool
    boundary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_boundary(self) -> P17AuthorityBoundary:
        if any((
            self.provider_dispatch_authorized,
            self.model_inference_authorized,
            self.network_authorized,
            self.Docker_authorized,
            self.Graphify_mutation_authorized,
            self.automatic_retry_authorized,
            self.automatic_fallback_authorized,
            self.automatic_cleanup_authorized,
            self.automatic_rollback_authorized,
            self.automatic_staging_authorized,
            self.automatic_commit_authorized,
            self.automatic_push_authorized,
            self.critical_ticket_execution_authorized,
            self.production_execution_authorized,
            self.multi_agent_execution_authorized,
            self.parallel_execution_authorized,
        )):
            raise ValueError(
                "P17 closure cannot authorize runtime or automatic authority"
            )
        if not self.human_Git_authority_required:
            raise ValueError("P17 closure requires human Git authority")
        if self.boundary_SHA256 != _model_digest(
            AUTHORITY_BOUNDARY_DIGEST_ALGORITHM, self
        ):
            raise ValueError("boundary_SHA256 must match authority boundary digest")
        return self


class P17SecurityBoundary(_ClosureModel):
    credential_contents_allowed: StrictBool
    raw_provider_responses_allowed: StrictBool
    raw_prompts_allowed: StrictBool
    reasoning_traces_allowed: StrictBool
    raw_stdout_allowed: StrictBool
    raw_stderr_allowed: StrictBool
    raw_diff_allowed: StrictBool
    source_snapshots_allowed: StrictBool
    environment_values_allowed: StrictBool
    personal_absolute_paths_allowed: StrictBool
    runtime_handles_allowed: StrictBool
    Git_handles_allowed: StrictBool
    digital_signature_claimed: StrictBool
    digest_is_signature: StrictBool
    security_boundary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_security(self) -> P17SecurityBoundary:
        if any((
            self.credential_contents_allowed,
            self.raw_provider_responses_allowed,
            self.raw_prompts_allowed,
            self.reasoning_traces_allowed,
            self.raw_stdout_allowed,
            self.raw_stderr_allowed,
            self.raw_diff_allowed,
            self.source_snapshots_allowed,
            self.environment_values_allowed,
            self.personal_absolute_paths_allowed,
            self.runtime_handles_allowed,
            self.Git_handles_allowed,
            self.digital_signature_claimed,
            self.digest_is_signature,
        )):
            raise ValueError("P17 closure cannot allow sensitive content or signatures")
        if self.security_boundary_SHA256 != _model_digest(
            SECURITY_BOUNDARY_DIGEST_ALGORITHM, self
        ):
            raise ValueError(
                "security_boundary_SHA256 must match security boundary digest"
            )
        return self


class P17ResidualLimitation(_ClosureModel):
    limitation_id: LimitationIdentifier
    title: TitleText
    description: SummaryText
    accepted: StrictBool
    blocking_for_P17_closure: StrictBool
    deferred_to_project: ProjectIdentifier | None = None
    limitation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_limitation(self) -> P17ResidualLimitation:
        if not self.accepted:
            raise ValueError("P17 residual limitations must be accepted")
        if self.blocking_for_P17_closure:
            raise ValueError("accepted P17 residual limitation cannot block closure")
        if self.limitation_SHA256 != _model_digest(
            RESIDUAL_LIMITATION_DIGEST_ALGORITHM, self
        ):
            raise ValueError("limitation_SHA256 must match limitation digest")
        return self


class P18MigrationHandoff(_ClosureModel):
    next_project: Literal["P18"] = "P18"
    first_ticket: Literal["P18.0"] = "P18.0"
    P17_closed: StrictBool
    WorkPacket_execution_MVP_available: StrictBool
    non_critical_pilot_accepted: StrictBool
    workflow_migration_authorized_to_begin: StrictBool
    Pepper_is_customized_Hermes: StrictBool
    reuse_existing_Hermes_capabilities_first: StrictBool
    modify_Hermes_when_product_requirements_require: StrictBool
    replace_Hermes_only_with_gap_evidence: StrictBool
    duplicate_existing_runtime_logic_prohibited: StrictBool
    Kanban_Swarm_reuse_assessment_required: StrictBool
    upstream_setup_is_Pepper_authority: StrictBool
    generic_dashboard_provider_state_is_P17_authority: StrictBool
    GBrain_memory_available: StrictBool
    Paperclip_control_plane_available: StrictBool
    production_default_mode_authorized: StrictBool
    handoff_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_handoff(self) -> P18MigrationHandoff:
        if not all((
            self.P17_closed,
            self.WorkPacket_execution_MVP_available,
            self.non_critical_pilot_accepted,
            self.workflow_migration_authorized_to_begin,
            self.Pepper_is_customized_Hermes,
            self.reuse_existing_Hermes_capabilities_first,
            self.modify_Hermes_when_product_requirements_require,
            self.replace_Hermes_only_with_gap_evidence,
            self.duplicate_existing_runtime_logic_prohibited,
            self.Kanban_Swarm_reuse_assessment_required,
        )):
            raise ValueError("P18 handoff affirmative posture mismatch")
        if any((
            self.upstream_setup_is_Pepper_authority,
            self.generic_dashboard_provider_state_is_P17_authority,
            self.GBrain_memory_available,
            self.Paperclip_control_plane_available,
            self.production_default_mode_authorized,
        )):
            raise ValueError("P18 handoff negative posture mismatch")
        if self.handoff_SHA256 != _model_digest(P18_HANDOFF_DIGEST_ALGORITHM, self):
            raise ValueError("handoff_SHA256 must match P18 handoff digest")
        return self


class P17ClosureFinding(_ClosureModel):
    finding_id: FindingIdentifier
    severity: P17ClosureFindingSeverity
    code: P17ClosureFindingCode
    ticket_id: TicketIdentifier | None = None
    capability_id: CapabilityIdentifier | None = None
    summary: SummaryText
    failed_invariant: InvariantText
    finding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_finding(self) -> P17ClosureFinding:
        if self.code in _BLOCKING_FINDING_CODES:
            if self.severity is not P17ClosureFindingSeverity.BLOCKING:
                raise ValueError(
                    "blocking closure finding code requires blocking severity"
                )
        elif self.code is P17ClosureFindingCode.MANUAL_VALIDATION_PENDING:
            if self.severity is not P17ClosureFindingSeverity.WARNING:
                raise ValueError("manual validation finding requires warning severity")
        elif self.severity is P17ClosureFindingSeverity.BLOCKING:
            raise ValueError("non-blocking closure finding code cannot be blocking")
        if self.finding_SHA256 != _model_digest(CLOSURE_FINDING_DIGEST_ALGORITHM, self):
            raise ValueError("finding_SHA256 must match closure finding digest")
        return self


class P17ClosureSummary(_ClosureModel):
    ticket_count: int = Field(ge=0, strict=True)
    accepted_ticket_count: int = Field(ge=0, strict=True)
    satisfied_capability_count: int = Field(ge=0, strict=True)
    absent_by_design_capability_count: int = Field(ge=0, strict=True)
    deferred_capability_count: int = Field(ge=0, strict=True)
    accepted_limitation_count: int = Field(ge=0, strict=True)
    blocking_limitation_count: int = Field(ge=0, strict=True)
    information_finding_count: int = Field(ge=0, strict=True)
    warning_finding_count: int = Field(ge=0, strict=True)
    blocking_finding_count: int = Field(ge=0, strict=True)
    non_critical_pilot_accepted: StrictBool
    WorkPacket_execution_MVP_requirement_satisfied: StrictBool
    P17_closure_requirement_satisfied: StrictBool
    P18_ready: StrictBool
    production_readiness_claimed: StrictBool
    provider_dispatch_count: int = Field(ge=0, strict=True)
    model_inference_count: int = Field(ge=0, strict=True)
    Git_commands_executed: int = Field(ge=0, strict=True)
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> P17ClosureSummary:
        if self.accepted_ticket_count > self.ticket_count:
            raise ValueError("accepted ticket count cannot exceed ticket count")
        if self.blocking_limitation_count:
            raise ValueError("P17 closure summary cannot contain blocking limitations")
        if self.production_readiness_claimed:
            raise ValueError("P17 closure summary cannot claim production readiness")
        if any((
            self.provider_dispatch_count,
            self.model_inference_count,
            self.Git_commands_executed,
        )):
            raise ValueError("P17 closure summary cannot record runtime authority")
        if self.summary_SHA256 != _model_digest(CLOSURE_SUMMARY_DIGEST_ALGORITHM, self):
            raise ValueError("summary_SHA256 must match closure summary digest")
        return self


class P17ClosureRequest(_ClosureModel):
    schema_version: Literal[1] = WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION
    policy_id: Literal["pepper-governed-work-packet-execution-mvp-closure-v1"] = (
        WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID
    )
    ticket_acceptances: tuple[P17TicketAcceptance, ...] = Field(
        min_length=9, max_length=9
    )
    capability_reconciliations: tuple[P17CapabilityReconciliation, ...] = Field(
        min_length=18, max_length=18
    )
    authority_boundary: P17AuthorityBoundary
    security_boundary: P17SecurityBoundary
    residual_limitations: tuple[P17ResidualLimitation, ...] = Field(
        min_length=13, max_length=13
    )
    non_critical_pilot_result: NonCriticalTicketPilotResult
    P18_handoff: P18MigrationHandoff


class P17ClosureResult(_ClosureModel):
    schema_version: Literal[1] = WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION
    policy_id: Literal["pepper-governed-work-packet-execution-mvp-closure-v1"] = (
        WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID
    )
    closure_id: ClosureIdentifier
    state: P17ClosureState
    decision: P17ClosureDecision
    ticket_acceptances: tuple[P17TicketAcceptance, ...] = Field(
        min_length=9, max_length=9
    )
    capability_reconciliations: tuple[P17CapabilityReconciliation, ...] = Field(
        min_length=18, max_length=18
    )
    authority_boundary: P17AuthorityBoundary
    security_boundary: P17SecurityBoundary
    residual_limitations: tuple[P17ResidualLimitation, ...] = Field(
        min_length=13, max_length=13
    )
    findings: tuple[P17ClosureFinding, ...] = Field(max_length=128)
    closure_summary: P17ClosureSummary
    P18_handoff: P18MigrationHandoff
    WorkPacket_execution_MVP_requirement_satisfied: StrictBool
    P17_closure_requirement_satisfied: StrictBool
    P18_ready: StrictBool
    production_readiness_claimed: StrictBool
    provider_dispatch_count: int = Field(ge=0, strict=True)
    model_inference_count: int = Field(ge=0, strict=True)
    Git_commands_executed: int = Field(ge=0, strict=True)
    result_SHA256: DigestText

    @field_validator("findings", mode="after")
    @classmethod
    def _validate_finding_collection_field(
        cls, value: tuple[P17ClosureFinding, ...]
    ) -> tuple[P17ClosureFinding, ...]:
        _validate_finding_collection(value, error_type=ValueError)
        return value

    @model_validator(mode="after")
    def _validate_result(self) -> P17ClosureResult:
        _validate_result_integrity(self, error_type=ValueError)
        return self


_BLOCKING_FINDING_CODES = frozenset((
    P17ClosureFindingCode.TICKET_MISSING,
    P17ClosureFindingCode.VERDICT_MISMATCH,
    P17ClosureFindingCode.CONTRACT_MISMATCH,
    P17ClosureFindingCode.CHAIN_INCOMPLETE,
    P17ClosureFindingCode.AUTHORITY_EXPANDED,
    P17ClosureFindingCode.SECURITY_BOUNDARY_MISMATCH,
    P17ClosureFindingCode.PILOT_NOT_ACCEPTED,
    P17ClosureFindingCode.MVP_REQUIREMENT_UNSATISFIED,
    P17ClosureFindingCode.P17_REJECTED,
))


_TICKET_SPECS = (
    (
        "P17.0",
        "TicketSpec to WorkPacket Compiler",
        0,
        "hermes_0_19_pepper_ticket_spec_to_work_packet_compiler_ready_with_compile_only_non_executing_authority",
        "WorkPacket compiler",
        (),
        "Deterministic TicketSpec to WorkPacket compilation is accepted.",
        "Compile-only contract with no runtime, provider, model, Git or workspace authority.",
    ),
    (
        "P17.1",
        "Workspace Allocator",
        1,
        "hermes_0_19_pepper_work_packet_workspace_allocator_ready_with_human_provisioned_exclusive_non_executing_authority",
        "Workspace allocation",
        ("P17.0",),
        "Human-provisioned exclusive workspace allocation is accepted.",
        "Bounded allocation contract without execution, provider, model or Git authority.",
    ),
    (
        "P17.2",
        "Tool Permission Profiles",
        2,
        "hermes_0_19_pepper_tool_permission_profiles_ready_with_deterministic_deny_first_non_executing_authority",
        "Tool permission profile",
        ("P17.1",),
        "Deny-first deterministic tool permission profiles are accepted.",
        "Permission profile contract grants no execution and defaults to denied authority.",
    ),
    (
        "P17.3",
        "Single-Agent Ticket Executor",
        3,
        "hermes_0_19_pepper_single_agent_work_packet_execution_ready_with_externally_driven_permission_gated_filesystem_only_authority",
        "Single-agent execution",
        ("P17.0", "P17.1", "P17.2"),
        "Externally driven single-agent WorkPacket execution evidence is accepted.",
        "Permission-gated filesystem-only contract with no provider, model or Git authority.",
    ),
    (
        "P17.4",
        "Validation Command Runner",
        4,
        "hermes_0_19_pepper_validation_command_runner_ready_with_exact_human_authorized_shell_free_bounded_subprocess_authority",
        "Validation command runner",
        ("P17.3",),
        "Exact human-authorized validation command execution evidence is accepted.",
        "Shell-free bounded validation subprocess authority only inside the accepted runner.",
    ),
    (
        "P17.5",
        "Result, Failure and Cancellation Envelopes",
        5,
        "hermes_0_19_pepper_result_failure_cancellation_envelopes_ready_with_deterministic_bounded_terminal_outcome_authority",
        "Outcome envelopes",
        ("P17.3", "P17.4"),
        "Deterministic terminal result, failure and cancellation envelopes are accepted.",
        "Terminal outcome projection only; no retry, fallback, cleanup, rollback or deployment authority.",
    ),
    (
        "P17.6",
        "Diff and Artifact Review",
        6,
        "hermes_0_19_pepper_diff_and_artifact_review_ready_with_deterministic_human_observed_non_mutating_candidate_and_artifact_authority",
        "Diff artifact review",
        ("P17.5",),
        "Deterministic human-observed diff and artifact review is accepted.",
        "Non-mutating review contract with no filesystem inspection by P17.R and no Git authority.",
    ),
    (
        "P17.7",
        "Human Git Handoff",
        7,
        "hermes_0_19_pepper_human_git_handoff_ready_with_exact_review_bound_non_executing_human_only_git_authority",
        "Human Git handoff",
        ("P17.6",),
        "Exact review-bound human-only Git handoff evidence is accepted.",
        "Non-executing handoff contract; Git remains human-only and outside automatic authority.",
    ),
    (
        "P17.8",
        "Non-Critical Ticket Pilot",
        8,
        "hermes_0_19_pepper_non_critical_ticket_pilot_ready_with_complete_governed_work_packet_chain_and_human_only_git_handoff_evidence",
        "Non-critical ticket pilot",
        ("P17.0", "P17.1", "P17.2", "P17.3", "P17.4", "P17.5", "P17.6", "P17.7"),
        "One non-critical pilot binds the complete governed WorkPacket chain.",
        "Evidence-only pilot with bounded human Git handoff and no automatic runtime authority.",
    ),
)

_CAPABILITY_SPECS = (
    (
        "CAP-P17-001",
        "TicketSpec compilation",
        "P17.0",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-002",
        "workspace allocation",
        "P17.1",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-003",
        "deny-first tool permissions",
        "P17.2",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-004",
        "single-agent WorkPacket execution",
        "P17.3",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-005",
        "exact validation command execution",
        "P17.4",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-006",
        "terminal outcome envelopes",
        "P17.5",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-007",
        "diff and artifact review",
        "P17.6",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    (
        "CAP-P17-008",
        "human-only Git handoff",
        "P17.7",
        P17CapabilityStatus.SATISFIED,
        None,
    ),
    ("CAP-P17-009", "non-critical pilot", "P17.8", P17CapabilityStatus.SATISFIED, None),
    (
        "CAP-P17-010",
        "provider-backed execution",
        "P17.8",
        P17CapabilityStatus.ABSENT_BY_DESIGN,
        None,
    ),
    (
        "CAP-P17-011",
        "model-backed execution",
        "P17.8",
        P17CapabilityStatus.ABSENT_BY_DESIGN,
        None,
    ),
    (
        "CAP-P17-012",
        "automatic Git execution",
        "P17.7",
        P17CapabilityStatus.ABSENT_BY_DESIGN,
        None,
    ),
    (
        "CAP-P17-013",
        "critical-ticket support",
        "P17.8",
        P17CapabilityStatus.ABSENT_BY_DESIGN,
        None,
    ),
    (
        "CAP-P17-014",
        "production readiness",
        "P17.8",
        P17CapabilityStatus.ABSENT_BY_DESIGN,
        None,
    ),
    ("CAP-P17-015", "workflow migration", "P17.R", P17CapabilityStatus.DEFERRED, "P18"),
    (
        "CAP-P17-016",
        "persistent shared agent memory",
        "P17.R",
        P17CapabilityStatus.DEFERRED,
        "P19",
    ),
    ("CAP-P17-017", "work control plane", "P17.R", P17CapabilityStatus.DEFERRED, "P20"),
    (
        "CAP-P17-018",
        "multi-agent automation",
        "P17.R",
        P17CapabilityStatus.DEFERRED,
        "P21",
    ),
)

_LIMITATION_SPECS = (
    (
        "LIM-P17-001",
        "Non-critical pilot only",
        "P17 closes over one accepted non-critical pilot only.",
        None,
    ),
    (
        "LIM-P17-002",
        "Critical tickets unsupported",
        "Critical-ticket execution remains outside P17 scope.",
        None,
    ),
    (
        "LIM-P17-003",
        "Provider dispatch absent from WorkPacket MVP",
        "Provider-backed execution is absent by design in P17.",
        None,
    ),
    (
        "LIM-P17-004",
        "Model inference absent from WorkPacket MVP",
        "Model-backed execution is absent by design in P17.",
        None,
    ),
    (
        "LIM-P17-005",
        "Git remains human-only",
        "Git staging, commit and push remain human-only.",
        None,
    ),
    (
        "LIM-P17-006",
        "Automatic retry absent",
        "Automatic retry remains deferred beyond P17.",
        "P18",
    ),
    (
        "LIM-P17-007",
        "Automatic fallback absent",
        "Automatic fallback remains deferred beyond P17.",
        "P18",
    ),
    (
        "LIM-P17-008",
        "Automatic cleanup and rollback absent",
        "Automatic cleanup and rollback remain deferred beyond P17.",
        "P18",
    ),
    (
        "LIM-P17-009",
        "Workflow migration incomplete",
        "Manual-to-Pepper workflow migration starts in P18.",
        "P18",
    ),
    (
        "LIM-P17-010",
        "Persistent shared agent memory absent",
        "G-Brain governed shared memory is deferred to P19.",
        "P19",
    ),
    (
        "LIM-P17-011",
        "Durable work control plane absent",
        "Paperclip durable work-control authority is deferred to P20.",
        "P20",
    ),
    (
        "LIM-P17-012",
        "Multi-agent automation absent",
        "Governed multi-agent automation is deferred to P21.",
        "P21",
    ),
    (
        "LIM-P17-013",
        "Production readiness not claimed",
        "P17 closure does not authorize production default operation.",
        None,
    ),
)


def build_canonical_p17_closure_request(
    *,
    non_critical_pilot_result: NonCriticalTicketPilotResult,
) -> P17ClosureRequest:
    """Build the canonical immutable P17 closure request from one P17.8 pilot."""

    validate_non_critical_ticket_pilot_result(non_critical_pilot_result)
    request = P17ClosureRequest(
        ticket_acceptances=_build_ticket_acceptances(),
        capability_reconciliations=_build_capability_reconciliations(),
        authority_boundary=_build_authority_boundary(),
        security_boundary=_build_security_boundary(),
        residual_limitations=_build_residual_limitations(),
        non_critical_pilot_result=non_critical_pilot_result,
        P18_handoff=_build_p18_handoff(),
    )
    validate_p17_closure_request(request)
    return request


def validate_p17_closure_request(request: P17ClosureRequest) -> None:
    """Validate a P17 closure request without repair, reordering or side effects."""

    validated = _validated_request(request)
    _validate_schema_policy(validated)
    _validate_ticket_acceptances(
        validated.ticket_acceptances, error_type=P17ClosurePolicyError
    )
    _validate_capabilities(
        validated.capability_reconciliations, error_type=P17ClosurePolicyError
    )
    _validate_authority(validated.authority_boundary, error_type=P17ClosurePolicyError)
    _validate_security(validated.security_boundary, error_type=P17ClosurePolicyError)
    _validate_limitations(
        validated.residual_limitations, error_type=P17ClosurePolicyError
    )
    _validate_pilot(validated.non_critical_pilot_result)
    _validate_p18_handoff(validated.P18_handoff, error_type=P17ClosurePolicyError)


def build_p17_work_packet_execution_mvp_closure(
    request: P17ClosureRequest,
) -> P17ClosureResult:
    """Build a deterministic P17 WorkPacket Execution MVP closure result."""

    validate_p17_closure_request(request)
    validated = _validated_request(request)
    findings = _derive_findings(validated)
    summary = _derive_summary(validated, findings)
    accepted = (
        summary.blocking_finding_count == 0
        and summary.P17_closure_requirement_satisfied
    )
    decision = P17ClosureDecision.ACCEPTED if accepted else P17ClosureDecision.REJECTED
    state = P17ClosureState.CLOSED if accepted else P17ClosureState.BLOCKED
    mvp_ready = accepted and summary.WorkPacket_execution_MVP_requirement_satisfied
    closure_ready = accepted and summary.P17_closure_requirement_satisfied
    p18_ready = accepted and summary.P18_ready
    result_data = _result_base_data(
        request=validated,
        findings=findings,
        summary=summary,
        decision=decision,
        state=state,
        mvp_ready=mvp_ready,
        closure_ready=closure_ready,
        p18_ready=p18_ready,
    )
    closure_id = _closure_id_from_record(result_data)
    result_record = {**result_data, "closure_id": closure_id}
    result = P17ClosureResult(
        **result_record,
        result_SHA256=_digest_from_record(
            CLOSURE_RESULT_DIGEST_ALGORITHM, result_record
        ),
    )
    validate_p17_closure_result(result)
    return result


def validate_p17_closure_result(result: P17ClosureResult) -> None:
    """Validate one immutable P17 closure result."""

    try:
        validated = P17ClosureResult.model_validate(result)
    except (AttributeError, ValueError) as exc:
        raise P17ClosureValidationError("invalid P17 closure result") from exc
    _validate_result_integrity(validated, error_type=P17ClosureValidationError)


def summarize_p17_closure(result: P17ClosureResult) -> P17ClosureSummary:
    """Return the exact immutable closure summary after validating the result."""

    validate_p17_closure_result(result)
    return result.closure_summary


def _build_ticket_acceptances() -> tuple[P17TicketAcceptance, ...]:
    return tuple(_ticket_acceptance_from_spec(spec) for spec in _TICKET_SPECS)


def _ticket_acceptance_from_spec(spec) -> P17TicketAcceptance:
    data = {
        "ticket_id": spec[0],
        "ticket_title": spec[1],
        "ordinal": spec[2],
        "accepted": True,
        "verdict": spec[3],
        "primary_contract": spec[4],
        "prerequisite_ticket_ids": spec[5],
        "capability_summary": spec[6],
        "authority_summary": spec[7],
    }
    return P17TicketAcceptance(
        **data,
        evidence_SHA256=_digest_from_record(TICKET_ACCEPTANCE_DIGEST_ALGORITHM, data),
    )


def _build_capability_reconciliations() -> tuple[P17CapabilityReconciliation, ...]:
    return tuple(_capability_from_spec(spec) for spec in _CAPABILITY_SPECS)


def _capability_from_spec(spec) -> P17CapabilityReconciliation:
    status = spec[3]
    satisfied = status is P17CapabilityStatus.SATISFIED
    intentionally_absent = status is P17CapabilityStatus.ABSENT_BY_DESIGN
    deferred_to_project = spec[4]
    data = {
        "capability_id": spec[0],
        "capability_name": spec[1],
        "owner_ticket": spec[2],
        "status": status,
        "satisfied": satisfied,
        "intentionally_absent": intentionally_absent,
        "deferred_to_project": deferred_to_project,
        "authority_boundary": _capability_authority_summary(
            status, deferred_to_project
        ),
        "evidence_source": _capability_evidence_source(
            spec[2], status, deferred_to_project
        ),
    }
    return P17CapabilityReconciliation(
        **data,
        reconciliation_SHA256=_digest_from_record(
            CAPABILITY_RECONCILIATION_DIGEST_ALGORITHM, data
        ),
    )


def _capability_authority_summary(
    status: P17CapabilityStatus, deferred_to_project: str | None
) -> str:
    if status is P17CapabilityStatus.SATISFIED:
        return "Capability is satisfied within the accepted P17 bounded WorkPacket authority."
    if status is P17CapabilityStatus.ABSENT_BY_DESIGN:
        return "Capability is intentionally absent from P17 and grants no runtime authority."
    return f"Capability is deferred to {deferred_to_project} and grants no P17 runtime authority."


def _capability_evidence_source(
    owner_ticket: str, status: P17CapabilityStatus, deferred_to_project: str | None
) -> str:
    if status is P17CapabilityStatus.DEFERRED:
        return f"P17.R records handoff to {deferred_to_project}; implementation is outside P17."
    return f"Accepted {owner_ticket} contract inventory and canonical P17.8 pilot evidence."


def _build_authority_boundary() -> P17AuthorityBoundary:
    data = {
        "provider_dispatch_authorized": False,
        "model_inference_authorized": False,
        "network_authorized": False,
        "Docker_authorized": False,
        "Graphify_mutation_authorized": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_cleanup_authorized": False,
        "automatic_rollback_authorized": False,
        "automatic_staging_authorized": False,
        "automatic_commit_authorized": False,
        "automatic_push_authorized": False,
        "critical_ticket_execution_authorized": False,
        "production_execution_authorized": False,
        "multi_agent_execution_authorized": False,
        "parallel_execution_authorized": False,
        "human_Git_authority_required": True,
    }
    return P17AuthorityBoundary(
        **data,
        boundary_SHA256=_digest_from_record(AUTHORITY_BOUNDARY_DIGEST_ALGORITHM, data),
    )


def _build_security_boundary() -> P17SecurityBoundary:
    data = {
        "credential_contents_allowed": False,
        "raw_provider_responses_allowed": False,
        "raw_prompts_allowed": False,
        "reasoning_traces_allowed": False,
        "raw_stdout_allowed": False,
        "raw_stderr_allowed": False,
        "raw_diff_allowed": False,
        "source_snapshots_allowed": False,
        "environment_values_allowed": False,
        "personal_absolute_paths_allowed": False,
        "runtime_handles_allowed": False,
        "Git_handles_allowed": False,
        "digital_signature_claimed": False,
        "digest_is_signature": False,
    }
    return P17SecurityBoundary(
        **data,
        security_boundary_SHA256=_digest_from_record(
            SECURITY_BOUNDARY_DIGEST_ALGORITHM, data
        ),
    )


def _build_residual_limitations() -> tuple[P17ResidualLimitation, ...]:
    return tuple(_limitation_from_spec(spec) for spec in _LIMITATION_SPECS)


def _limitation_from_spec(spec) -> P17ResidualLimitation:
    data = {
        "limitation_id": spec[0],
        "title": spec[1],
        "description": spec[2],
        "accepted": True,
        "blocking_for_P17_closure": False,
        "deferred_to_project": spec[3],
    }
    return P17ResidualLimitation(
        **data,
        limitation_SHA256=_digest_from_record(
            RESIDUAL_LIMITATION_DIGEST_ALGORITHM, data
        ),
    )


def _build_p18_handoff() -> P18MigrationHandoff:
    data = {
        "next_project": "P18",
        "first_ticket": "P18.0",
        "P17_closed": True,
        "WorkPacket_execution_MVP_available": True,
        "non_critical_pilot_accepted": True,
        "workflow_migration_authorized_to_begin": True,
        "Pepper_is_customized_Hermes": True,
        "reuse_existing_Hermes_capabilities_first": True,
        "modify_Hermes_when_product_requirements_require": True,
        "replace_Hermes_only_with_gap_evidence": True,
        "duplicate_existing_runtime_logic_prohibited": True,
        "Kanban_Swarm_reuse_assessment_required": True,
        "upstream_setup_is_Pepper_authority": False,
        "generic_dashboard_provider_state_is_P17_authority": False,
        "GBrain_memory_available": False,
        "Paperclip_control_plane_available": False,
        "production_default_mode_authorized": False,
    }
    return P18MigrationHandoff(
        **data,
        handoff_SHA256=_digest_from_record(P18_HANDOFF_DIGEST_ALGORITHM, data),
    )


def _validated_request(request: P17ClosureRequest) -> P17ClosureRequest:
    try:
        return P17ClosureRequest.model_validate(request)
    except (AttributeError, ValueError) as exc:
        raise P17ClosureInputError("invalid P17 closure request") from exc


def _validate_schema_policy(request: P17ClosureRequest) -> None:
    if request.schema_version != WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION:
        raise P17ClosureInputError("schema version mismatch")
    if request.policy_id != WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID:
        raise P17ClosureInputError("policy ID mismatch")


def _validate_ticket_acceptances(
    values: tuple[P17TicketAcceptance, ...], *, error_type
) -> None:
    if len(values) != 9:
        raise error_type("P17 ticket acceptance count must be exactly nine")
    expected_ids = tuple(spec[0] for spec in _TICKET_SPECS)
    expected_titles = tuple(spec[1] for spec in _TICKET_SPECS)
    expected_verdicts = tuple(spec[3] for spec in _TICKET_SPECS)
    expected_prerequisites = tuple(spec[5] for spec in _TICKET_SPECS)
    if tuple(value.ticket_id for value in values) != expected_ids:
        raise error_type("P17 ticket acceptance order mismatch")
    if tuple(value.ticket_title for value in values) != expected_titles:
        raise error_type("P17 ticket title mismatch")
    if tuple(value.ordinal for value in values) != tuple(range(9)):
        raise error_type("P17 ticket ordinal mismatch")
    if tuple(value.verdict for value in values) != expected_verdicts:
        raise error_type("P17 ticket verdict mismatch")
    if (
        tuple(value.prerequisite_ticket_ids for value in values)
        != expected_prerequisites
    ):
        raise error_type("P17 prerequisite relationship mismatch")
    for value in values:
        if not value.accepted:
            raise error_type(f"{value.ticket_id} must be accepted")
        if value.evidence_SHA256 != _model_digest(
            TICKET_ACCEPTANCE_DIGEST_ALGORITHM, value
        ):
            raise error_type(f"{value.ticket_id} acceptance digest mismatch")


def _validate_capabilities(
    values: tuple[P17CapabilityReconciliation, ...], *, error_type
) -> None:
    if len(values) != 18:
        raise error_type("P17 capability count must be exactly eighteen")
    expected_ids = tuple(spec[0] for spec in _CAPABILITY_SPECS)
    expected_names = tuple(spec[1] for spec in _CAPABILITY_SPECS)
    expected_owners = tuple(spec[2] for spec in _CAPABILITY_SPECS)
    expected_statuses = tuple(spec[3] for spec in _CAPABILITY_SPECS)
    expected_deferred = tuple(spec[4] for spec in _CAPABILITY_SPECS)
    if tuple(value.capability_id for value in values) != expected_ids:
        raise error_type("P17 capability order mismatch")
    if tuple(value.capability_name for value in values) != expected_names:
        raise error_type("P17 capability name mismatch")
    if tuple(value.owner_ticket for value in values) != expected_owners:
        raise error_type("P17 capability owner mismatch")
    if tuple(value.status for value in values) != expected_statuses:
        raise error_type("P17 capability status mismatch")
    if tuple(value.deferred_to_project for value in values) != expected_deferred:
        raise error_type("P17 deferred project mismatch")
    for value in values:
        if value.reconciliation_SHA256 != _model_digest(
            CAPABILITY_RECONCILIATION_DIGEST_ALGORITHM, value
        ):
            raise error_type(f"{value.capability_id} capability digest mismatch")


def _validate_authority(value: P17AuthorityBoundary, *, error_type) -> None:
    if any((
        value.provider_dispatch_authorized,
        value.model_inference_authorized,
        value.network_authorized,
        value.Docker_authorized,
        value.Graphify_mutation_authorized,
        value.automatic_retry_authorized,
        value.automatic_fallback_authorized,
        value.automatic_cleanup_authorized,
        value.automatic_rollback_authorized,
        value.automatic_staging_authorized,
        value.automatic_commit_authorized,
        value.automatic_push_authorized,
        value.critical_ticket_execution_authorized,
        value.production_execution_authorized,
        value.multi_agent_execution_authorized,
        value.parallel_execution_authorized,
    )):
        raise error_type("authority boundary mismatch")
    if not value.human_Git_authority_required:
        raise error_type("authority boundary mismatch")
    if value.boundary_SHA256 != _model_digest(
        AUTHORITY_BOUNDARY_DIGEST_ALGORITHM, value
    ):
        raise error_type("authority boundary digest mismatch")


def _validate_security(value: P17SecurityBoundary, *, error_type) -> None:
    if any((
        value.credential_contents_allowed,
        value.raw_provider_responses_allowed,
        value.raw_prompts_allowed,
        value.reasoning_traces_allowed,
        value.raw_stdout_allowed,
        value.raw_stderr_allowed,
        value.raw_diff_allowed,
        value.source_snapshots_allowed,
        value.environment_values_allowed,
        value.personal_absolute_paths_allowed,
        value.runtime_handles_allowed,
        value.Git_handles_allowed,
        value.digital_signature_claimed,
        value.digest_is_signature,
    )):
        raise error_type("security boundary mismatch")
    if value.security_boundary_SHA256 != _model_digest(
        SECURITY_BOUNDARY_DIGEST_ALGORITHM, value
    ):
        raise error_type("security boundary digest mismatch")


def _validate_limitations(
    values: tuple[P17ResidualLimitation, ...], *, error_type
) -> None:
    if len(values) != 13:
        raise error_type("P17 limitation count must be exactly thirteen")
    expected_ids = tuple(spec[0] for spec in _LIMITATION_SPECS)
    expected_titles = tuple(spec[1] for spec in _LIMITATION_SPECS)
    expected_deferred = tuple(spec[3] for spec in _LIMITATION_SPECS)
    if tuple(value.limitation_id for value in values) != expected_ids:
        raise error_type("P17 limitation order mismatch")
    if tuple(value.title for value in values) != expected_titles:
        raise error_type("P17 limitation title mismatch")
    if tuple(value.deferred_to_project for value in values) != expected_deferred:
        raise error_type("P17 limitation deferred project mismatch")
    for value in values:
        if not value.accepted or value.blocking_for_P17_closure:
            raise error_type(f"{value.limitation_id} limitation posture mismatch")
        if value.limitation_SHA256 != _model_digest(
            RESIDUAL_LIMITATION_DIGEST_ALGORITHM, value
        ):
            raise error_type(f"{value.limitation_id} limitation digest mismatch")


def _validate_pilot(result: NonCriticalTicketPilotResult) -> None:
    try:
        validate_non_critical_ticket_pilot_result(result)
    except ValueError as exc:
        raise P17ClosureStateError("invalid P17.8 pilot result") from exc
    if result.decision is not PilotDecision.ACCEPTED:
        raise P17ClosureStateError("P17.8 pilot must be accepted")
    if result.state is not PilotState.COMPLETED:
        raise P17ClosureStateError("P17.8 pilot must be completed")
    if not result.WorkPacket_execution_MVP_requirement_satisfied:
        raise P17ClosureStateError("P17.8 pilot must satisfy WorkPacket MVP")
    if not result.P17_closure_ready:
        raise P17ClosureStateError("P17.8 pilot must mark P17 closure ready")
    if result.production_readiness_claimed:
        raise P17ClosureStateError("P17.8 pilot cannot claim production readiness")
    if any((result.provider_dispatch_count, result.model_inference_count)):
        raise P17ClosureStateError(
            "P17.8 pilot cannot record provider or model authority"
        )
    if result.acceptance_summary.Git_commands_executed:
        raise P17ClosureStateError("P17.8 pilot cannot record Git execution")


def _validate_p18_handoff(value: P18MigrationHandoff, *, error_type) -> None:
    if not all((
        value.P17_closed,
        value.WorkPacket_execution_MVP_available,
        value.non_critical_pilot_accepted,
        value.workflow_migration_authorized_to_begin,
        value.Pepper_is_customized_Hermes,
        value.reuse_existing_Hermes_capabilities_first,
        value.modify_Hermes_when_product_requirements_require,
        value.replace_Hermes_only_with_gap_evidence,
        value.duplicate_existing_runtime_logic_prohibited,
        value.Kanban_Swarm_reuse_assessment_required,
    )):
        raise error_type("P18 handoff mismatch")
    if any((
        value.upstream_setup_is_Pepper_authority,
        value.generic_dashboard_provider_state_is_P17_authority,
        value.GBrain_memory_available,
        value.Paperclip_control_plane_available,
        value.production_default_mode_authorized,
    )):
        raise error_type("P18 handoff mismatch")
    if value.handoff_SHA256 != _model_digest(P18_HANDOFF_DIGEST_ALGORITHM, value):
        raise error_type("P18 handoff digest mismatch")


def _derive_findings(request: P17ClosureRequest) -> tuple[P17ClosureFinding, ...]:
    records = tuple(_finding_records(request))
    return tuple(
        _finding_from_record(index=index, record=record)
        for index, record in enumerate(
            sorted(records, key=_finding_record_sort_key), start=1
        )
    )


def _finding_records(request: P17ClosureRequest):
    for acceptance in request.ticket_acceptances:
        yield (
            P17ClosureFindingSeverity.INFO,
            P17ClosureFindingCode.TICKET_ACCEPTED,
            acceptance.ticket_id,
            None,
            f"{acceptance.ticket_id} accepted as part of the governed P17 chain.",
            "ticket accepted with exact verdict and digest",
        )
    for capability in request.capability_reconciliations:
        if capability.status is P17CapabilityStatus.ABSENT_BY_DESIGN:
            code = _absent_capability_code(capability.capability_id)
            yield (
                P17ClosureFindingSeverity.INFO,
                code,
                capability.owner_ticket,
                capability.capability_id,
                f"{capability.capability_name} remains absent by design in P17.",
                "absent capability grants no P17 authority",
            )
    manual_ids = request.non_critical_pilot_result.acceptance_summary.manual_validation_ids_pending
    if manual_ids:
        yield (
            P17ClosureFindingSeverity.WARNING,
            P17ClosureFindingCode.MANUAL_VALIDATION_PENDING,
            "P17.8",
            "CAP-P17-009",
            "P17.8 pilot retains bounded pending manual validation identifiers.",
            "manual validation pending remains warning not success",
        )
    yield (
        P17ClosureFindingSeverity.INFO,
        P17ClosureFindingCode.PRODUCTION_READINESS_NOT_CLAIMED,
        "P17.8",
        "CAP-P17-014",
        "P17 closure does not claim production readiness.",
        "production readiness remains false",
    )
    yield (
        P17ClosureFindingSeverity.INFO,
        P17ClosureFindingCode.P18_REUSE_FIRST_REQUIRED,
        None,
        "CAP-P17-015",
        "P18 must inspect and reuse or customize existing Pepper and Hermes capabilities first.",
        "duplicate runtime logic without gap evidence prohibited",
    )
    yield (
        P17ClosureFindingSeverity.INFO,
        P17ClosureFindingCode.P18_READY,
        None,
        "CAP-P17-015",
        "P18 may begin after P17.R is reviewed, committed and pushed.",
        "P17 closure handoff permits P18 start only after human Git handoff",
    )
    yield (
        P17ClosureFindingSeverity.INFO,
        P17ClosureFindingCode.P17_CLOSED,
        None,
        None,
        "P17 WorkPacket Execution MVP closure requirements are satisfied.",
        "P17.0 through P17.8 form one coherent accepted chain",
    )


def _absent_capability_code(capability_id: str) -> P17ClosureFindingCode:
    if capability_id == "CAP-P17-010":
        return P17ClosureFindingCode.PROVIDER_EXECUTION_ABSENT
    if capability_id == "CAP-P17-011":
        return P17ClosureFindingCode.MODEL_EXECUTION_ABSENT
    if capability_id == "CAP-P17-012":
        return P17ClosureFindingCode.GIT_EXECUTION_ABSENT
    if capability_id == "CAP-P17-013":
        return P17ClosureFindingCode.CRITICAL_TICKET_SUPPORT_ABSENT
    return P17ClosureFindingCode.PRODUCTION_READINESS_NOT_CLAIMED


def _finding_from_record(index: int, record) -> P17ClosureFinding:
    data = {
        "finding_id": f"P17F-{index:03d}",
        "severity": record[0],
        "code": record[1],
        "ticket_id": record[2],
        "capability_id": record[3],
        "summary": record[4],
        "failed_invariant": record[5],
    }
    return P17ClosureFinding(
        **data,
        finding_SHA256=_digest_from_record(CLOSURE_FINDING_DIGEST_ALGORITHM, data),
    )


def _derive_summary(
    request: P17ClosureRequest, findings: tuple[P17ClosureFinding, ...]
) -> P17ClosureSummary:
    info_count = sum(
        1 for finding in findings if finding.severity is P17ClosureFindingSeverity.INFO
    )
    warning_count = sum(
        1
        for finding in findings
        if finding.severity is P17ClosureFindingSeverity.WARNING
    )
    blocking_count = sum(
        1
        for finding in findings
        if finding.severity is P17ClosureFindingSeverity.BLOCKING
    )
    satisfied_count = sum(
        1
        for capability in request.capability_reconciliations
        if capability.status is P17CapabilityStatus.SATISFIED
    )
    absent_count = sum(
        1
        for capability in request.capability_reconciliations
        if capability.status is P17CapabilityStatus.ABSENT_BY_DESIGN
    )
    deferred_count = sum(
        1
        for capability in request.capability_reconciliations
        if capability.status is P17CapabilityStatus.DEFERRED
    )
    data = {
        "ticket_count": len(request.ticket_acceptances),
        "accepted_ticket_count": sum(
            1 for ticket in request.ticket_acceptances if ticket.accepted
        ),
        "satisfied_capability_count": satisfied_count,
        "absent_by_design_capability_count": absent_count,
        "deferred_capability_count": deferred_count,
        "accepted_limitation_count": sum(
            1 for item in request.residual_limitations if item.accepted
        ),
        "blocking_limitation_count": sum(
            1 for item in request.residual_limitations if item.blocking_for_P17_closure
        ),
        "information_finding_count": info_count,
        "warning_finding_count": warning_count,
        "blocking_finding_count": blocking_count,
        "non_critical_pilot_accepted": request.non_critical_pilot_result.decision
        is PilotDecision.ACCEPTED,
        "WorkPacket_execution_MVP_requirement_satisfied": request.non_critical_pilot_result.WorkPacket_execution_MVP_requirement_satisfied,
        "P17_closure_requirement_satisfied": request.non_critical_pilot_result.P17_closure_ready
        and blocking_count == 0,
        "P18_ready": request.P18_handoff.workflow_migration_authorized_to_begin
        and blocking_count == 0,
        "production_readiness_claimed": False,
        "provider_dispatch_count": request.non_critical_pilot_result.provider_dispatch_count,
        "model_inference_count": request.non_critical_pilot_result.model_inference_count,
        "Git_commands_executed": request.non_critical_pilot_result.acceptance_summary.Git_commands_executed,
    }
    return P17ClosureSummary(
        **data,
        summary_SHA256=_digest_from_record(CLOSURE_SUMMARY_DIGEST_ALGORITHM, data),
    )


def _result_base_data(
    *,
    request: P17ClosureRequest,
    findings: tuple[P17ClosureFinding, ...],
    summary: P17ClosureSummary,
    decision: P17ClosureDecision,
    state: P17ClosureState,
    mvp_ready: bool,
    closure_ready: bool,
    p18_ready: bool,
):
    return {
        "schema_version": WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION,
        "policy_id": WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID,
        "state": state,
        "decision": decision,
        "ticket_acceptances": request.ticket_acceptances,
        "capability_reconciliations": request.capability_reconciliations,
        "authority_boundary": request.authority_boundary,
        "security_boundary": request.security_boundary,
        "residual_limitations": request.residual_limitations,
        "findings": findings,
        "closure_summary": summary,
        "P18_handoff": request.P18_handoff,
        "WorkPacket_execution_MVP_requirement_satisfied": mvp_ready,
        "P17_closure_requirement_satisfied": closure_ready,
        "P18_ready": p18_ready,
        "production_readiness_claimed": False,
        "provider_dispatch_count": summary.provider_dispatch_count,
        "model_inference_count": summary.model_inference_count,
        "Git_commands_executed": summary.Git_commands_executed,
    }


def _validate_result_integrity(result: P17ClosureResult, error_type) -> None:
    _validate_ticket_acceptances(result.ticket_acceptances, error_type=error_type)
    _validate_capabilities(result.capability_reconciliations, error_type=error_type)
    _validate_authority(result.authority_boundary, error_type=error_type)
    _validate_security(result.security_boundary, error_type=error_type)
    _validate_limitations(result.residual_limitations, error_type=error_type)
    _validate_finding_collection(result.findings, error_type=error_type)
    _validate_p18_handoff(result.P18_handoff, error_type=error_type)
    if result.closure_id != _closure_id_from_result(result):
        raise error_type("closure ID mismatch")
    accepted = result.decision is P17ClosureDecision.ACCEPTED
    if accepted:
        if result.state is not P17ClosureState.CLOSED:
            raise error_type("accepted closure must be closed")
        if not result.WorkPacket_execution_MVP_requirement_satisfied:
            raise error_type("accepted closure must satisfy WorkPacket MVP")
        if not result.P17_closure_requirement_satisfied:
            raise error_type("accepted closure must satisfy P17 closure")
        if not result.P18_ready:
            raise error_type("accepted closure must mark P18 ready")
    else:
        if result.state is not P17ClosureState.BLOCKED:
            raise error_type("rejected closure must be blocked")
        if result.WorkPacket_execution_MVP_requirement_satisfied:
            raise error_type("rejected closure cannot satisfy WorkPacket MVP")
        if result.P17_closure_requirement_satisfied:
            raise error_type("rejected closure cannot satisfy P17 closure")
        if result.P18_ready:
            raise error_type("rejected closure cannot mark P18 ready")
    if result.production_readiness_claimed:
        raise error_type("production readiness must remain false")
    if any((
        result.provider_dispatch_count,
        result.model_inference_count,
        result.Git_commands_executed,
    )):
        raise error_type(
            "closure result cannot record provider, model or Git authority"
        )
    summary = result.closure_summary
    if summary.ticket_count != len(result.ticket_acceptances):
        raise error_type("summary ticket count mismatch")
    if summary.accepted_ticket_count != sum(
        1 for ticket in result.ticket_acceptances if ticket.accepted
    ):
        raise error_type("summary accepted ticket count mismatch")
    if summary.satisfied_capability_count != sum(
        1
        for capability in result.capability_reconciliations
        if capability.status is P17CapabilityStatus.SATISFIED
    ):
        raise error_type("summary satisfied capability count mismatch")
    if summary.absent_by_design_capability_count != sum(
        1
        for capability in result.capability_reconciliations
        if capability.status is P17CapabilityStatus.ABSENT_BY_DESIGN
    ):
        raise error_type("summary absent capability count mismatch")
    if summary.deferred_capability_count != sum(
        1
        for capability in result.capability_reconciliations
        if capability.status is P17CapabilityStatus.DEFERRED
    ):
        raise error_type("summary deferred capability count mismatch")
    if summary.accepted_limitation_count != sum(
        1 for limitation in result.residual_limitations if limitation.accepted
    ):
        raise error_type("summary accepted limitation count mismatch")
    if summary.blocking_limitation_count != sum(
        1
        for limitation in result.residual_limitations
        if limitation.blocking_for_P17_closure
    ):
        raise error_type("summary blocking limitation count mismatch")
    if summary.information_finding_count != sum(
        1
        for finding in result.findings
        if finding.severity is P17ClosureFindingSeverity.INFO
    ):
        raise error_type("summary information finding count mismatch")
    if summary.warning_finding_count != sum(
        1
        for finding in result.findings
        if finding.severity is P17ClosureFindingSeverity.WARNING
    ):
        raise error_type("summary warning finding count mismatch")
    if summary.blocking_finding_count != sum(
        1
        for finding in result.findings
        if finding.severity is P17ClosureFindingSeverity.BLOCKING
    ):
        raise error_type("summary blocking finding count mismatch")
    if result.result_SHA256 != _model_digest(CLOSURE_RESULT_DIGEST_ALGORITHM, result):
        raise error_type("result_SHA256 must match P17 closure result digest")


def _validate_finding_collection(
    values: tuple[P17ClosureFinding, ...], *, error_type
) -> None:
    expected_ids = tuple(f"P17F-{index:03d}" for index in range(1, len(values) + 1))
    if tuple(value.finding_id for value in values) != expected_ids:
        raise error_type("closure finding IDs must be contiguous")
    if tuple(values) != tuple(sorted(values, key=_finding_sort_key)):
        raise error_type("closure finding order mismatch")
    for value in values:
        if value.finding_SHA256 != _model_digest(
            CLOSURE_FINDING_DIGEST_ALGORITHM, value
        ):
            raise error_type("closure finding digest mismatch")


def _closure_id_from_record(record) -> str:
    identity_record = _closure_identity_record(record)
    digest = _digest_from_record(CLOSURE_ID_DIGEST_ALGORITHM, identity_record)
    return f"P17C-{digest[:12]}"


def _closure_id_from_result(result: P17ClosureResult) -> str:
    return _closure_id_from_record(
        result.model_dump(mode="python", exclude={"closure_id", "result_SHA256"})
    )


def _closure_identity_record(record):
    return {
        "schema_version": record["schema_version"],
        "policy_id": record["policy_id"],
        "ticket_acceptance_digests": tuple(
            _field(item, "evidence_SHA256") for item in record["ticket_acceptances"]
        ),
        "capability_reconciliation_digests": tuple(
            _field(item, "reconciliation_SHA256")
            for item in record["capability_reconciliations"]
        ),
        "authority_boundary_digest": _field(
            record["authority_boundary"], "boundary_SHA256"
        ),
        "security_boundary_digest": _field(
            record["security_boundary"], "security_boundary_SHA256"
        ),
        "limitation_digests": tuple(
            _field(item, "limitation_SHA256") for item in record["residual_limitations"]
        ),
        "finding_digests": tuple(
            _field(item, "finding_SHA256") for item in record["findings"]
        ),
        "closure_summary_digest": _field(record["closure_summary"], "summary_SHA256"),
        "P18_handoff_digest": _field(record["P18_handoff"], "handoff_SHA256"),
        "decision": record["decision"],
        "state": record["state"],
    }


def _field(value, name: str):
    if isinstance(value, dict):
        return value[name]
    return getattr(value, name)


def _model_digest(algorithm: str, model: BaseModel) -> str:
    field_name = _digest_field_name(model)
    return _digest_from_record(
        algorithm, model.model_dump(mode="python", exclude={field_name})
    )


def _digest_field_name(model: BaseModel) -> str:
    for field_name in _DIGEST_FIELD_NAMES:
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


def _reject_duplicate_values(values: tuple[str, ...], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {label}")


def _finding_record_sort_key(record) -> tuple[int, int, str, str]:
    severity, code, ticket_id, capability_id, _summary, _invariant = record
    return (
        tuple(P17ClosureFindingSeverity).index(severity),
        tuple(P17ClosureFindingCode).index(code),
        "" if ticket_id is None else ticket_id,
        "" if capability_id is None else capability_id,
    )


def _finding_sort_key(value: P17ClosureFinding) -> tuple[int, int, str, str]:
    return (
        tuple(P17ClosureFindingSeverity).index(value.severity),
        tuple(P17ClosureFindingCode).index(value.code),
        "" if value.ticket_id is None else value.ticket_id,
        "" if value.capability_id is None else value.capability_id,
    )


__all__ = (
    "WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION",
    "WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID",
    "P17ClosureState",
    "P17ClosureDecision",
    "P17ClosureFindingSeverity",
    "P17ClosureFindingCode",
    "P17CapabilityStatus",
    "P17TicketAcceptance",
    "P17CapabilityReconciliation",
    "P17AuthorityBoundary",
    "P17SecurityBoundary",
    "P17ResidualLimitation",
    "P18MigrationHandoff",
    "P17ClosureFinding",
    "P17ClosureSummary",
    "P17ClosureRequest",
    "P17ClosureResult",
    "P17ClosureError",
    "P17ClosureInputError",
    "P17ClosureIntegrityError",
    "P17ClosurePolicyError",
    "P17ClosureStateError",
    "P17ClosureValidationError",
    "build_canonical_p17_closure_request",
    "validate_p17_closure_request",
    "build_p17_work_packet_execution_mvp_closure",
    "validate_p17_closure_result",
    "summarize_p17_closure",
)
