"""P18.0 governed workflow state-machine contracts for Pepper.

This module defines one normalized Pepper workflow lifecycle over the accepted
P17 WorkPacket contracts and existing Hermes/Pepper runtime mechanics. It is a
pure declarative layer: it does not inspect repositories, read databases, run
dispatchers, execute tools, call providers or models, mutate Git, invoke Docker,
invoke Graphify, retry work, roll back work, or claim production readiness.
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

from hermes_cli.agent_platform.work_packet.work_packet_execution_mvp_closure import (
    P17ClosureDecision,
    P17ClosureResult,
    P17ClosureState,
    validate_p17_closure_result,
)


GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION = 1
GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID = (
    "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
)

WORKFLOW_ID_DIGEST_ALGORITHM = "agent-platform-governed-workflow-id-sha256-v1"
WORKFLOW_IDENTITY_DIGEST_ALGORITHM = "agent-platform-workflow-identity-sha256-v1"
WORKFLOW_PROJECTION_DIGEST_ALGORITHM = (
    "agent-platform-hermes-workflow-projection-sha256-v1"
)
WORKFLOW_MAPPING_DIGEST_ALGORITHM = "agent-platform-workflow-runtime-mapping-sha256-v1"
WORKFLOW_TRANSITION_DIGEST_ALGORITHM = (
    "agent-platform-governed-workflow-transition-sha256-v1"
)
WORKFLOW_SNAPSHOT_DIGEST_ALGORITHM = (
    "agent-platform-governed-workflow-snapshot-sha256-v1"
)
WORKFLOW_P17_BINDING_DIGEST_ALGORITHM = "agent-platform-p17-workflow-binding-sha256-v1"
WORKFLOW_FINDING_DIGEST_ALGORITHM = (
    "agent-platform-workflow-state-machine-finding-sha256-v1"
)
WORKFLOW_REUSE_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-workflow-reuse-summary-sha256-v1"
)
WORKFLOW_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-governed-workflow-state-machine-result-sha256-v1"
)

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_WORKFLOW_ID_PATTERN = r"^GWF-[a-f0-9]{12}$"
_TRANSITION_ID_PATTERN = r"^GWT-(?:[0-9]{3}|REJECTED)$"
_FINDING_ID_PATTERN = r"^GSMF-[0-9]{3}$"
_PROJECT_ID_PATTERN = r"^P[0-9]+(?:\.[0-9]+|\.R)?$"
_TICKET_ID_PATTERN = r"^P[0-9]+(?:\.[0-9]+|\.R)?$"
_EVIDENCE_REF_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9_.:-]{1,95}$"
_BLOCKER_PATTERN = r"^[a-z][a-z0-9_:-]{2,80}$"
_CONTROL_OR_ANSI_PATTERN = r"[\x00-\x1f\x7f\x1b]"
_PERSONAL_PATH_PATTERN = r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)"
_RAW_RUNTIME_MARKERS = (
    "sqlite",
    "select ",
    "insert ",
    "update ",
    "delete ",
    "create table",
    "rowid",
    "raw stdout",
    "raw stderr",
    "traceback",
    "diff --git",
    "@@ ",
    "file content snapshot",
    "provider response",
    "model output",
    "reasoning trace",
    "runtime handle",
    "filesystem handle",
    "git handle",
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
)
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
_DIGEST_FIELD_NAMES = frozenset({
    "identity_SHA256",
    "projection_SHA256",
    "mapping_SHA256",
    "transition_SHA256",
    "workflow_SHA256",
    "binding_SHA256",
    "finding_SHA256",
    "summary_SHA256",
    "result_SHA256",
})


class GovernedWorkflowStateMachineError(ValueError):
    """Base error for P18.0 governed workflow state-machine failures."""


class GovernedWorkflowStateMachineInputError(GovernedWorkflowStateMachineError):
    """Raised when workflow inputs are structurally invalid."""


class GovernedWorkflowStateMachineIntegrityError(GovernedWorkflowStateMachineError):
    """Raised when deterministic workflow digests are invalid."""


class GovernedWorkflowStateMachinePolicyError(GovernedWorkflowStateMachineError):
    """Raised when workflow policy invariants are violated."""


class GovernedWorkflowStateMachineStateError(GovernedWorkflowStateMachineError):
    """Raised when a workflow transition is not valid for the current state."""


class GovernedWorkflowStateMachineValidationError(GovernedWorkflowStateMachineError):
    """Raised when a built workflow object fails validation."""


class GovernedWorkflowState(str, Enum):
    DRAFT = "draft"
    INTAKE_READY = "intake_ready"
    AWAITING_TICKET_APPROVAL = "awaiting_ticket_approval"
    TICKET_APPROVED = "ticket_approved"
    WORK_PACKET_READY = "work_packet_ready"
    QUEUED = "queued"
    BLOCKED = "blocked"
    ALLOCATING = "allocating"
    READY_TO_EXECUTE = "ready_to_execute"
    EXECUTING = "executing"
    VALIDATING = "validating"
    REVIEWING = "reviewing"
    AWAITING_CORRECTION = "awaiting_correction"
    AWAITING_HUMAN_APPROVAL = "awaiting_human_approval"
    AWAITING_HUMAN_GIT_HANDOFF = "awaiting_human_git_handoff"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INCIDENT = "incident"
    RETRY_PENDING = "retry_pending"
    ROLLBACK_REQUIRED = "rollback_required"


class WorkflowStateOwner(str, Enum):
    PEPPER_GOVERNANCE = "pepper_governance"
    PEPPER_RUNTIME = "pepper_runtime"
    HUMAN = "human"
    SHARED = "shared"


class WorkflowTransitionTrigger(str, Enum):
    PROJECT_INTAKE_COMPLETED = "project_intake_completed"
    TICKET_GENERATED = "ticket_generated"
    TICKET_APPROVED = "ticket_approved"
    WORK_PACKET_COMPILED = "work_packet_compiled"
    DEPENDENCIES_READY = "dependencies_ready"
    DEPENDENCIES_BLOCKED = "dependencies_blocked"
    WORKSPACE_ALLOCATED = "workspace_allocated"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETED = "execution_completed"
    EXECUTION_FAILED = "execution_failed"
    VALIDATION_STARTED = "validation_started"
    VALIDATION_COMPLETED = "validation_completed"
    VALIDATION_FAILED = "validation_failed"
    REVIEW_STARTED = "review_started"
    REVIEW_ACCEPTED = "review_accepted"
    REVIEW_REJECTED = "review_rejected"
    CORRECTION_REQUIRED = "correction_required"
    HUMAN_APPROVED = "human_approved"
    HUMAN_REJECTED = "human_rejected"
    GIT_HANDOFF_READY = "git_handoff_ready"
    HUMAN_GIT_COMPLETED = "human_git_completed"
    CANCEL_REQUESTED = "cancel_requested"
    INCIDENT_DETECTED = "incident_detected"
    RETRY_AUTHORIZED = "retry_authorized"
    ROLLBACK_AUTHORIZED = "rollback_authorized"


class WorkflowTransitionAuthority(str, Enum):
    SYSTEM = "system"
    HUMAN = "human"
    GOVERNED_RUNTIME = "governed_runtime"
    POLICY = "policy"


class HermesWorkflowRuntimeKind(str, Enum):
    KANBAN_SWARM = "kanban_swarm"
    RUNTIME_ADAPTER = "runtime_adapter"
    WORK_PACKET = "work_packet"
    GOVERNANCE_ONLY = "governance_only"


class WorkflowRuntimeMappingKind(str, Enum):
    EXACT = "exact"
    COMPOSITE = "composite"
    GOVERNANCE_ONLY = "governance_only"
    RUNTIME_ONLY = "runtime_only"


class WorkflowStateMachineFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class WorkflowStateMachineFindingCode(str, Enum):
    HERMES_CAPABILITY_REUSED = "hermes_capability_reused"
    HERMES_CAPABILITY_CUSTOMIZED = "hermes_capability_customized"
    HERMES_CAPABILITY_REPLACEMENT_REQUIRED = "hermes_capability_replacement_required"
    HERMES_CAPABILITY_GAP = "hermes_capability_gap"
    DUPLICATE_RUNTIME_LOGIC_DETECTED = "duplicate_runtime_logic_detected"
    STATE_MAPPING_COMPLETE = "state_mapping_complete"
    STATE_MAPPING_MISSING = "state_mapping_missing"
    AUTHORITY_MISMATCH = "authority_mismatch"
    P17_BINDING_VALID = "p17_binding_valid"
    P17_BINDING_INVALID = "p17_binding_invalid"
    HUMAN_BOUNDARY_PRESERVED = "human_boundary_preserved"
    RUNTIME_PROJECTION_NON_AUTHORITATIVE = "runtime_projection_non_authoritative"
    WORKFLOW_READY = "workflow_ready"


def _validate_bounded_text(value: str, label: str) -> str:
    if re.search(_CONTROL_OR_ANSI_PATTERN, value):
        raise ValueError(f"{label} contains control characters")
    lowered = value.lower()
    if any(marker in lowered for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} contains credential-shaped text")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-shaped text")
    if any(marker in lowered for marker in _RAW_RUNTIME_MARKERS):
        raise ValueError(f"{label} contains raw runtime content")
    if re.search(_PERSONAL_PATH_PATTERN, value):
        raise ValueError(f"{label} contains personal absolute path")
    return value


DigestText: TypeAlias = Annotated[str, StringConstraints(pattern=_DIGEST_PATTERN)]
WorkflowIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=16, max_length=16, pattern=_WORKFLOW_ID_PATTERN)
]
TransitionIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=7, max_length=12, pattern=_TRANSITION_ID_PATTERN)
]
FindingIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=8, max_length=8, pattern=_FINDING_ID_PATTERN)
]
ProjectIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=2, max_length=12, pattern=_PROJECT_ID_PATTERN)
]
TicketIdentifier: TypeAlias = Annotated[
    str, StringConstraints(min_length=4, max_length=12, pattern=_TICKET_ID_PATTERN)
]
EvidenceReference: TypeAlias = Annotated[
    str, StringConstraints(min_length=2, max_length=96, pattern=_EVIDENCE_REF_PATTERN)
]
BlockerCode: TypeAlias = Annotated[
    str, StringConstraints(min_length=3, max_length=80, pattern=_BLOCKER_PATTERN)
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=240),
    AfterValidator(lambda value: _validate_bounded_text(value, "text")),
]
RuntimeStateText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=80),
    AfterValidator(lambda value: _validate_bounded_text(value, "runtime state")),
]
OptionalRuntimeIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=80),
    AfterValidator(lambda value: _validate_bounded_text(value, "runtime identifier")),
]


class _WorkflowModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", use_enum_values=False)


def _digest_payload(value: object) -> object:
    if isinstance(value, BaseModel):
        return _digest_payload(
            value.model_dump(mode="python", exclude=_DIGEST_FIELD_NAMES, warnings=False)
        )
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_digest_payload(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _digest_payload(item) for key, item in value.items()}
    return value


def _digest(algorithm: str, payload: object) -> str:
    encoded = json.dumps(
        {"algorithm": algorithm, "payload": _digest_payload(payload)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _model_digest(algorithm: str, value: BaseModel) -> str:
    return _digest(algorithm, value)


def _make_model(
    model_type: type[_WorkflowModel],
    digest_field: str,
    algorithm: str,
    **data: object,
) -> _WorkflowModel:
    provisional = model_type.model_construct(**data, **{digest_field: "0" * 64})
    return model_type(**data, **{digest_field: _model_digest(algorithm, provisional)})


def _tuple(values: tuple[object, ...] | list[object]) -> tuple[object, ...]:
    return tuple(values)


class GovernedWorkflowStateDefinition(_WorkflowModel):
    state: GovernedWorkflowState
    owner: WorkflowStateOwner
    entry_condition: BoundedText
    exit_condition: BoundedText
    terminal: StrictBool
    human_authority_required: StrictBool
    operational_execution_allowed: StrictBool
    retry_allowed: StrictBool
    rollback_allowed: StrictBool
    inherited_runtime_mapping: BoundedText
    description: BoundedText

    @model_validator(mode="after")
    def _validate_state_definition(self) -> GovernedWorkflowStateDefinition:
        if self.owner is WorkflowStateOwner.HUMAN and not self.human_authority_required:
            raise ValueError("human-owned states require human authority")
        if self.terminal and (self.retry_allowed or self.rollback_allowed):
            raise ValueError(
                "terminal state cannot directly authorize retry or rollback"
            )
        if self.operational_execution_allowed and self.human_authority_required:
            raise ValueError("human authority state cannot allow operational execution")
        if self.state in _HUMAN_PENDING_STATES and not self.human_authority_required:
            raise ValueError("pending-human state must require human authority")
        return self


class GovernedWorkflowTransition(_WorkflowModel):
    transition_id: TransitionIdentifier
    from_state: GovernedWorkflowState
    to_state: GovernedWorkflowState
    trigger: WorkflowTransitionTrigger
    authority: WorkflowTransitionAuthority
    required_evidence: tuple[EvidenceReference, ...] = Field(max_length=12)
    forbidden_when: tuple[BlockerCode, ...] = Field(max_length=12)
    automatic: StrictBool
    transition_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_transition(self) -> GovernedWorkflowTransition:
        if self.transition_id == "GWT-REJECTED":
            if self.transition_SHA256 != _model_digest(
                WORKFLOW_TRANSITION_DIGEST_ALGORITHM, self
            ):
                raise ValueError("transition_SHA256 must match transition digest")
            return self
        if self.authority is WorkflowTransitionAuthority.HUMAN and self.automatic:
            raise ValueError("human-authorized transition cannot be automatic")
        if (
            self.trigger in _HUMAN_ONLY_TRIGGERS
            and self.authority is not WorkflowTransitionAuthority.HUMAN
        ):
            raise ValueError("human-only trigger must use human authority")
        if self.trigger in _NON_AUTOMATIC_TRIGGERS and self.automatic:
            raise ValueError(
                "retry, rollback and Git handoff transitions cannot be automatic"
            )
        if self.transition_SHA256 != _model_digest(
            WORKFLOW_TRANSITION_DIGEST_ALGORITHM, self
        ):
            raise ValueError("transition_SHA256 must match transition digest")
        return self


class GovernedWorkflowIdentity(_WorkflowModel):
    workflow_id: WorkflowIdentifier
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    ticket_revision: int = Field(ge=1, le=9999, strict=True)
    work_packet_id: OptionalRuntimeIdentifier
    work_packet_SHA256: DigestText
    workflow_policy_id: Literal[
        "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    ] = GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
    identity_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_identity(self) -> GovernedWorkflowIdentity:
        if self.workflow_id != _workflow_id_for(
            self.project_id,
            self.ticket_id,
            self.ticket_revision,
            self.work_packet_id,
            self.work_packet_SHA256,
        ):
            raise ValueError("workflow_id must be deterministic")
        if self.identity_SHA256 != _model_digest(
            WORKFLOW_IDENTITY_DIGEST_ALGORITHM, self
        ):
            raise ValueError("identity_SHA256 must match identity digest")
        return self


class HermesWorkflowProjection(_WorkflowModel):
    runtime_kind: HermesWorkflowRuntimeKind
    runtime_state: RuntimeStateText
    task_id: OptionalRuntimeIdentifier | None = None
    board_or_queue_id: OptionalRuntimeIdentifier | None = None
    worker_id_present: StrictBool
    workspace_binding_present: StrictBool
    dependency_blocked: StrictBool
    retry_state_present: StrictBool
    reclaim_state_present: StrictBool
    runtime_projection_is_authoritative_governance_state: Literal[False] = False
    projection_SHA256: DigestText

    @field_validator("task_id", "board_or_queue_id", mode="after")
    @classmethod
    def _validate_optional_runtime_identifier(cls, value: str | None) -> str | None:
        if value is not None:
            _validate_bounded_text(value, "runtime identifier")
        return value

    @model_validator(mode="after")
    def _validate_projection(self) -> HermesWorkflowProjection:
        if self.runtime_kind is HermesWorkflowRuntimeKind.KANBAN_SWARM:
            if self.runtime_state not in _RELEVANT_KANBAN_STATES:
                raise ValueError("unmapped Kanban runtime state")
            if self.board_or_queue_id is None:
                raise ValueError("Kanban projection requires board_or_queue_id")
        if self.runtime_kind is HermesWorkflowRuntimeKind.GOVERNANCE_ONLY:
            if self.task_id is not None or self.board_or_queue_id is not None:
                raise ValueError("governance-only projection cannot carry runtime IDs")
        if self.dependency_blocked and self.runtime_state not in {"blocked", "todo"}:
            raise ValueError(
                "dependency_blocked must map to blocked or parent-gated todo"
            )
        if self.projection_SHA256 != _model_digest(
            WORKFLOW_PROJECTION_DIGEST_ALGORITHM, self
        ):
            raise ValueError("projection_SHA256 must match projection digest")
        return self


class WorkflowRuntimeStateMapping(_WorkflowModel):
    governed_state: GovernedWorkflowState
    runtime_state: RuntimeStateText
    mapping_kind: WorkflowRuntimeMappingKind
    exact: StrictBool
    notes: BoundedText
    mapping_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_mapping(self) -> WorkflowRuntimeStateMapping:
        if self.mapping_kind is WorkflowRuntimeMappingKind.EXACT and not self.exact:
            raise ValueError("exact mapping kind requires exact=true")
        if self.mapping_kind is not WorkflowRuntimeMappingKind.EXACT and self.exact:
            raise ValueError("only exact mapping kind may set exact=true")
        if self.mapping_SHA256 != _model_digest(
            WORKFLOW_MAPPING_DIGEST_ALGORITHM, self
        ):
            raise ValueError("mapping_SHA256 must match mapping digest")
        return self


class P17WorkflowBinding(_WorkflowModel):
    P17_closure_id: OptionalRuntimeIdentifier
    P17_closure_SHA256: DigestText
    WorkPacket_execution_MVP_available: Literal[True]
    human_Git_authority_required: Literal[True]
    non_critical_scope: Literal[True]
    production_readiness_claimed: Literal[False]
    binding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_binding(self) -> P17WorkflowBinding:
        if self.binding_SHA256 != _model_digest(
            WORKFLOW_P17_BINDING_DIGEST_ALGORITHM, self
        ):
            raise ValueError("binding_SHA256 must match P17 workflow binding digest")
        return self


class GovernedWorkflowSnapshot(_WorkflowModel):
    schema_version: Literal[1] = GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    ] = GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
    identity: GovernedWorkflowIdentity
    current_state: GovernedWorkflowState
    state_owner: WorkflowStateOwner
    transition_index: int = Field(ge=0, le=10000, strict=True)
    completed_transition_ids: tuple[TransitionIdentifier, ...] = Field(max_length=10000)
    active_blocker_codes: tuple[BlockerCode, ...] = Field(max_length=64)
    pending_human_action: BoundedText | None
    P17_binding_SHA256: DigestText
    runtime_projection: HermesWorkflowProjection
    workflow_SHA256: DigestText

    @field_validator("completed_transition_ids", "active_blocker_codes", mode="after")
    @classmethod
    def _validate_unique_tuple(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("snapshot tuple fields must be unique")
        return value

    @model_validator(mode="after")
    def _validate_snapshot(self) -> GovernedWorkflowSnapshot:
        expected_owner = _state_definition_for(self.current_state).owner
        if self.state_owner is not expected_owner:
            raise ValueError("state_owner must match current_state owner")
        if self.transition_index != len(self.completed_transition_ids):
            raise ValueError("transition_index must match completed transition count")
        if self.current_state in _HUMAN_PENDING_STATES:
            if self.pending_human_action is None:
                raise ValueError("pending human state requires pending_human_action")
        elif self.pending_human_action is not None:
            raise ValueError(
                "non-human-pending state cannot carry pending_human_action"
            )
        if self.active_blocker_codes and self.current_state not in _BLOCKER_STATES:
            raise ValueError("active blockers require a blocker-capable state")
        if self.workflow_SHA256 != _model_digest(
            WORKFLOW_SNAPSHOT_DIGEST_ALGORITHM, self
        ):
            raise ValueError("workflow_SHA256 must match snapshot digest")
        return self


class GovernedWorkflowTransitionRequest(_WorkflowModel):
    schema_version: Literal[1] = GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    ] = GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
    current_snapshot: GovernedWorkflowSnapshot
    trigger: WorkflowTransitionTrigger
    authority: WorkflowTransitionAuthority
    evidence_refs: tuple[EvidenceReference, ...] = Field(max_length=32)
    runtime_projection: HermesWorkflowProjection

    @field_validator("evidence_refs", mode="after")
    @classmethod
    def _validate_evidence_refs(
        cls, value: tuple[EvidenceReference, ...]
    ) -> tuple[EvidenceReference, ...]:
        if len(value) != len(set(value)):
            raise ValueError("evidence_refs must be unique")
        return value


class GovernedWorkflowTransitionResult(_WorkflowModel):
    schema_version: Literal[1] = GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    ] = GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
    previous_snapshot_SHA256: DigestText
    transition: GovernedWorkflowTransition
    resulting_snapshot: GovernedWorkflowSnapshot
    accepted: StrictBool
    blocking_reasons: tuple[BlockerCode, ...] = Field(max_length=16)
    human_action_required: StrictBool
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_transition_result(self) -> GovernedWorkflowTransitionResult:
        if self.accepted and self.blocking_reasons:
            raise ValueError(
                "accepted transition result cannot include blocking reasons"
            )
        if not self.accepted and not self.blocking_reasons:
            raise ValueError("rejected transition result requires blocking reasons")
        if self.accepted and self.transition.transition_id == "GWT-REJECTED":
            raise ValueError(
                "accepted transition result cannot use rejected transition"
            )
        if self.result_SHA256 != _model_digest(WORKFLOW_RESULT_DIGEST_ALGORITHM, self):
            raise ValueError("result_SHA256 must match transition result digest")
        return self


class WorkflowStateMachineFinding(_WorkflowModel):
    finding_id: FindingIdentifier
    severity: WorkflowStateMachineFindingSeverity
    code: WorkflowStateMachineFindingCode
    capability: BoundedText | None
    summary: BoundedText
    finding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_finding(self) -> WorkflowStateMachineFinding:
        if self.code in _BLOCKING_FINDING_CODES:
            if self.severity is not WorkflowStateMachineFindingSeverity.BLOCKING:
                raise ValueError("blocking finding code requires blocking severity")
        elif self.severity is WorkflowStateMachineFindingSeverity.BLOCKING:
            raise ValueError("non-blocking finding code cannot use blocking severity")
        if self.finding_SHA256 != _model_digest(
            WORKFLOW_FINDING_DIGEST_ALGORITHM, self
        ):
            raise ValueError("finding_SHA256 must match finding digest")
        return self


class WorkflowReuseSummary(_WorkflowModel):
    capabilities_assessed: int = Field(ge=0, strict=True)
    capabilities_reused: int = Field(ge=0, strict=True)
    capabilities_customized: int = Field(ge=0, strict=True)
    capabilities_replaced: int = Field(ge=0, strict=True)
    capabilities_deferred: int = Field(ge=0, strict=True)
    duplicate_runtime_capabilities_created: int = Field(ge=0, strict=True)
    Kanban_Swarm_assessed: StrictBool
    planner_assessed: StrictBool
    dispatcher_assessed: StrictBool
    heartbeat_assessed: StrictBool
    retry_assessed: StrictBool
    reclaim_assessed: StrictBool
    workspace_lifecycle_assessed: StrictBool
    approval_surfaces_assessed: StrictBool
    dashboard_TUI_surfaces_assessed: StrictBool
    prior_Hermes_0_19_analysis_reused: StrictBool
    current_targeted_revalidation_performed: StrictBool
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> WorkflowReuseSummary:
        total = (
            self.capabilities_reused
            + self.capabilities_customized
            + self.capabilities_replaced
            + self.capabilities_deferred
        )
        if total != self.capabilities_assessed:
            raise ValueError(
                "reuse summary counts must derive from capability inventory"
            )
        required_flags = (
            self.Kanban_Swarm_assessed,
            self.planner_assessed,
            self.dispatcher_assessed,
            self.heartbeat_assessed,
            self.retry_assessed,
            self.reclaim_assessed,
            self.workspace_lifecycle_assessed,
            self.approval_surfaces_assessed,
            self.dashboard_TUI_surfaces_assessed,
            self.prior_Hermes_0_19_analysis_reused,
            self.current_targeted_revalidation_performed,
        )
        if not all(required_flags):
            raise ValueError(
                "all P18.0 reuse and revalidation surfaces must be assessed"
            )
        if self.summary_SHA256 != _model_digest(
            WORKFLOW_REUSE_SUMMARY_DIGEST_ALGORITHM, self
        ):
            raise ValueError("summary_SHA256 must match reuse summary digest")
        return self


class GovernedWorkflowStateMachineResult(_WorkflowModel):
    schema_version: Literal[1] = GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    ] = GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
    state_definitions: tuple[GovernedWorkflowStateDefinition, ...] = Field(
        min_length=21, max_length=21
    )
    transitions: tuple[GovernedWorkflowTransition, ...] = Field(
        min_length=20, max_length=64
    )
    runtime_mappings: tuple[WorkflowRuntimeStateMapping, ...] = Field(
        min_length=21, max_length=80
    )
    P17_binding: P17WorkflowBinding
    findings: tuple[WorkflowStateMachineFinding, ...] = Field(
        min_length=1, max_length=64
    )
    reuse_summary: WorkflowReuseSummary
    state_machine_ready: StrictBool
    P18_1_ready: StrictBool
    production_readiness_claimed: Literal[False]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> GovernedWorkflowStateMachineResult:
        state_values = tuple(item.state for item in self.state_definitions)
        if state_values != tuple(GovernedWorkflowState):
            raise ValueError(
                "state definitions must cover every canonical state in order"
            )
        transition_ids = tuple(item.transition_id for item in self.transitions)
        if len(transition_ids) != len(set(transition_ids)):
            raise ValueError("transitions must have unique IDs")
        mapping_keys = tuple(
            (item.runtime_state, item.governed_state) for item in self.runtime_mappings
        )
        if len(mapping_keys) != len(set(mapping_keys)):
            raise ValueError("runtime mappings must be unique")
        mapped_states = {item.governed_state for item in self.runtime_mappings}
        if set(GovernedWorkflowState) - mapped_states:
            raise ValueError("every governed state requires an explicit mapping")
        finding_numbers = tuple(
            int(item.finding_id.rsplit("-", 1)[1]) for item in self.findings
        )
        if finding_numbers != tuple(range(1, len(finding_numbers) + 1)):
            raise ValueError("finding IDs must be deterministic and contiguous")
        blocking_count = sum(
            item.severity is WorkflowStateMachineFindingSeverity.BLOCKING
            for item in self.findings
        )
        if blocking_count:
            if self.state_machine_ready or self.P18_1_ready:
                raise ValueError("blocking findings prevent readiness")
        if self.state_machine_ready and not self.P18_1_ready:
            raise ValueError("P18.1 readiness must follow state-machine readiness")
        if self.reuse_summary.duplicate_runtime_capabilities_created:
            raise ValueError("duplicate runtime capabilities are prohibited")
        if self.result_SHA256 != _model_digest(WORKFLOW_RESULT_DIGEST_ALGORITHM, self):
            raise ValueError("result_SHA256 must match state-machine result digest")
        return self


_HUMAN_PENDING_STATES = frozenset({
    GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
    GovernedWorkflowState.AWAITING_CORRECTION,
    GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
    GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
})
_BLOCKER_STATES = frozenset({
    GovernedWorkflowState.BLOCKED,
    GovernedWorkflowState.AWAITING_CORRECTION,
    GovernedWorkflowState.FAILED,
    GovernedWorkflowState.INCIDENT,
    GovernedWorkflowState.RETRY_PENDING,
    GovernedWorkflowState.ROLLBACK_REQUIRED,
})
_TERMINAL_STATES = frozenset({
    GovernedWorkflowState.COMPLETED,
    GovernedWorkflowState.CANCELLED,
})
_HUMAN_ONLY_TRIGGERS = frozenset({
    WorkflowTransitionTrigger.TICKET_APPROVED,
    WorkflowTransitionTrigger.HUMAN_APPROVED,
    WorkflowTransitionTrigger.HUMAN_REJECTED,
    WorkflowTransitionTrigger.HUMAN_GIT_COMPLETED,
    WorkflowTransitionTrigger.RETRY_AUTHORIZED,
    WorkflowTransitionTrigger.ROLLBACK_AUTHORIZED,
})
_NON_AUTOMATIC_TRIGGERS = frozenset({
    WorkflowTransitionTrigger.HUMAN_GIT_COMPLETED,
    WorkflowTransitionTrigger.RETRY_AUTHORIZED,
    WorkflowTransitionTrigger.ROLLBACK_AUTHORIZED,
})
_BLOCKING_FINDING_CODES = frozenset({
    WorkflowStateMachineFindingCode.DUPLICATE_RUNTIME_LOGIC_DETECTED,
    WorkflowStateMachineFindingCode.STATE_MAPPING_MISSING,
    WorkflowStateMachineFindingCode.AUTHORITY_MISMATCH,
    WorkflowStateMachineFindingCode.P17_BINDING_INVALID,
})
_RELEVANT_KANBAN_STATES = frozenset({
    "triage",
    "todo",
    "scheduled",
    "ready",
    "running",
    "blocked",
    "review",
    "done",
    "archived",
})


_STATE_DEFINITION_ROWS: tuple[
    tuple[
        GovernedWorkflowState,
        WorkflowStateOwner,
        str,
        str,
        bool,
        bool,
        bool,
        bool,
        bool,
        str,
        str,
    ],
    ...,
] = (
    (
        GovernedWorkflowState.DRAFT,
        WorkflowStateOwner.PEPPER_GOVERNANCE,
        "Project context exists but intake is not complete.",
        "Project intake evidence is accepted.",
        False,
        False,
        False,
        False,
        False,
        "Governance-only state before Kanban task creation.",
        "Initial governed workflow state for P18.1 intake.",
    ),
    (
        GovernedWorkflowState.INTAKE_READY,
        WorkflowStateOwner.PEPPER_GOVERNANCE,
        "Project intake evidence is complete.",
        "Ticket Factory emits a ticket candidate.",
        False,
        False,
        False,
        False,
        False,
        "Maps to Kanban triage when an operational task exists.",
        "Intake can proceed to ticket approval without executing runtime work.",
    ),
    (
        GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
        WorkflowStateOwner.HUMAN,
        "Ticket candidate is generated.",
        "Human approves the ticket.",
        False,
        True,
        False,
        False,
        False,
        "Governance-only state over Ticket Factory approval publishing.",
        "Human approval boundary before TicketSpec is accepted.",
    ),
    (
        GovernedWorkflowState.TICKET_APPROVED,
        WorkflowStateOwner.PEPPER_GOVERNANCE,
        "Human-approved ticket is available.",
        "WorkPacket compilation succeeds.",
        False,
        False,
        False,
        False,
        False,
        "Governance-only state over accepted TicketSpec contracts.",
        "Ticket is accepted as governance authority but not yet executable.",
    ),
    (
        GovernedWorkflowState.WORK_PACKET_READY,
        WorkflowStateOwner.PEPPER_GOVERNANCE,
        "P17 WorkPacket compilation evidence is accepted.",
        "Dependency policy allows queue entry.",
        False,
        False,
        False,
        False,
        False,
        "Governance-only state over P17.0 WorkPacketCompilationResult.",
        "WorkPacket is available for governed orchestration.",
    ),
    (
        GovernedWorkflowState.QUEUED,
        WorkflowStateOwner.SHARED,
        "Dependencies are ready or parent-gated by Kanban todo semantics.",
        "Runtime allocation begins, blocker appears, or cancellation is requested.",
        False,
        False,
        False,
        False,
        False,
        "Maps to Kanban todo or scheduled queue states.",
        "Workflow is queued without execution authority.",
    ),
    (
        GovernedWorkflowState.BLOCKED,
        WorkflowStateOwner.SHARED,
        "Dependency or human blocker is recorded.",
        "Blocker clears or human reroutes the workflow.",
        False,
        False,
        False,
        False,
        False,
        "Maps to Kanban blocked and dependency-gated todo semantics.",
        "Workflow cannot progress until explicit blocker evidence changes.",
    ),
    (
        GovernedWorkflowState.ALLOCATING,
        WorkflowStateOwner.PEPPER_RUNTIME,
        "Queue eligibility is established.",
        "P17.1 workspace allocation evidence is accepted.",
        False,
        False,
        False,
        False,
        False,
        "Composite mapping to runtime-adapter starting and waiting states.",
        "Runtime mechanics may prepare workspace binding but P18.0 does not allocate.",
    ),
    (
        GovernedWorkflowState.READY_TO_EXECUTE,
        WorkflowStateOwner.SHARED,
        "Workspace and permission evidence are present.",
        "Governed runtime starts execution.",
        False,
        False,
        False,
        False,
        False,
        "Maps to Kanban ready and runtime-adapter ready.",
        "Execution may be authorized by later P18 integration using P17 contracts.",
    ),
    (
        GovernedWorkflowState.EXECUTING,
        WorkflowStateOwner.PEPPER_RUNTIME,
        "Execution start evidence is accepted.",
        "Execution completes, fails, incident is detected, or cancellation is requested.",
        False,
        False,
        True,
        False,
        False,
        "Maps to Kanban running.",
        "Operational runtime may be active; P18.0 still executes nothing.",
    ),
    (
        GovernedWorkflowState.VALIDATING,
        WorkflowStateOwner.PEPPER_RUNTIME,
        "P17.3 execution result evidence is accepted.",
        "Validation completes or fails.",
        False,
        False,
        True,
        False,
        False,
        "Maps to P17.4 validation runner evidence and runtime validating state.",
        "Validation phase is represented without invoking commands in P18.0.",
    ),
    (
        GovernedWorkflowState.REVIEWING,
        WorkflowStateOwner.SHARED,
        "Validation result is accepted.",
        "Review accepts, rejects, or requests correction.",
        False,
        False,
        False,
        False,
        False,
        "Maps to Kanban review and P17.6 diff artifact review evidence.",
        "Human-observed review evidence is pending or being reconciled.",
    ),
    (
        GovernedWorkflowState.AWAITING_CORRECTION,
        WorkflowStateOwner.HUMAN,
        "Validation or review requires correction.",
        "Human supplies correction authority or reroutes.",
        False,
        True,
        False,
        False,
        False,
        "Governance-only correction loop before later P18 workflow integration.",
        "Correction is required before continued migration workflow progress.",
    ),
    (
        GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
        WorkflowStateOwner.HUMAN,
        "Review evidence is accepted.",
        "Human approves or rejects the reviewed workflow result.",
        False,
        True,
        False,
        False,
        False,
        "Governance-only approval boundary over existing approval surfaces.",
        "Explicit human approval remains required before Git handoff.",
    ),
    (
        GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
        WorkflowStateOwner.HUMAN,
        "Human approval has been granted.",
        "Human completes Git handoff outside automatic runtime authority.",
        False,
        True,
        False,
        False,
        False,
        "Maps to P17.7 human Git handoff evidence.",
        "Git authority remains human-only.",
    ),
    (
        GovernedWorkflowState.COMPLETED,
        WorkflowStateOwner.PEPPER_GOVERNANCE,
        "Human Git handoff is completed.",
        "No transition is allowed by P18.0.",
        True,
        False,
        False,
        False,
        False,
        "Maps to Kanban done.",
        "Workflow is closed for P18.0 governance purposes.",
    ),
    (
        GovernedWorkflowState.FAILED,
        WorkflowStateOwner.SHARED,
        "Execution or runtime evidence records failure.",
        "Human or policy authority may route to retry or rollback state in P18.6.",
        False,
        False,
        False,
        False,
        False,
        "Maps to runtime-adapter failed and Kanban failure run evidence.",
        "Failure is represented without automatic retry.",
    ),
    (
        GovernedWorkflowState.CANCELLED,
        WorkflowStateOwner.HUMAN,
        "Cancellation is requested and accepted.",
        "No transition is allowed by P18.0.",
        True,
        True,
        False,
        False,
        False,
        "Maps to runtime-adapter cancelled and archived task posture.",
        "Human cancellation terminates the governed workflow.",
    ),
    (
        GovernedWorkflowState.INCIDENT,
        WorkflowStateOwner.SHARED,
        "Incident evidence is detected.",
        "P18.6 incident policy determines next action.",
        False,
        False,
        False,
        False,
        False,
        "Governance-only state over future incident workflow.",
        "Incident handling is modeled but not implemented by P18.0.",
    ),
    (
        GovernedWorkflowState.RETRY_PENDING,
        WorkflowStateOwner.HUMAN,
        "Retry has been explicitly authorized.",
        "P18.6 retry policy requeues or escalates.",
        False,
        True,
        False,
        False,
        False,
        "Governance-only state over existing retry evidence.",
        "Retry is pending and not automatically executed by P18.0.",
    ),
    (
        GovernedWorkflowState.ROLLBACK_REQUIRED,
        WorkflowStateOwner.HUMAN,
        "Rollback has been explicitly authorized or required.",
        "P18.6 rollback workflow decides next action.",
        False,
        True,
        False,
        False,
        False,
        "Maps to runtime-adapter rollback pending.",
        "Rollback is represented but not executed by P18.0.",
    ),
)


_TRANSITION_ROWS: tuple[
    tuple[
        str,
        GovernedWorkflowState,
        GovernedWorkflowState,
        WorkflowTransitionTrigger,
        WorkflowTransitionAuthority,
        tuple[str, ...],
        tuple[str, ...],
        bool,
    ],
    ...,
] = (
    (
        "GWT-001",
        GovernedWorkflowState.DRAFT,
        GovernedWorkflowState.INTAKE_READY,
        WorkflowTransitionTrigger.PROJECT_INTAKE_COMPLETED,
        WorkflowTransitionAuthority.SYSTEM,
        ("project_intake_evidence",),
        (),
        True,
    ),
    (
        "GWT-002",
        GovernedWorkflowState.INTAKE_READY,
        GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
        WorkflowTransitionTrigger.TICKET_GENERATED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("ticket_factory_candidate",),
        (),
        True,
    ),
    (
        "GWT-003",
        GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
        GovernedWorkflowState.TICKET_APPROVED,
        WorkflowTransitionTrigger.TICKET_APPROVED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_ticket_approval",),
        (),
        False,
    ),
    (
        "GWT-004",
        GovernedWorkflowState.TICKET_APPROVED,
        GovernedWorkflowState.WORK_PACKET_READY,
        WorkflowTransitionTrigger.WORK_PACKET_COMPILED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("work_packet_compilation_result",),
        (),
        True,
    ),
    (
        "GWT-005",
        GovernedWorkflowState.WORK_PACKET_READY,
        GovernedWorkflowState.QUEUED,
        WorkflowTransitionTrigger.DEPENDENCIES_READY,
        WorkflowTransitionAuthority.POLICY,
        ("dependency_plan_ready",),
        (),
        True,
    ),
    (
        "GWT-006",
        GovernedWorkflowState.QUEUED,
        GovernedWorkflowState.BLOCKED,
        WorkflowTransitionTrigger.DEPENDENCIES_BLOCKED,
        WorkflowTransitionAuthority.POLICY,
        ("dependency_blocker",),
        (),
        True,
    ),
    (
        "GWT-007",
        GovernedWorkflowState.BLOCKED,
        GovernedWorkflowState.QUEUED,
        WorkflowTransitionTrigger.DEPENDENCIES_READY,
        WorkflowTransitionAuthority.POLICY,
        ("dependency_unblocked",),
        (),
        True,
    ),
    (
        "GWT-008",
        GovernedWorkflowState.QUEUED,
        GovernedWorkflowState.ALLOCATING,
        WorkflowTransitionTrigger.DEPENDENCIES_READY,
        WorkflowTransitionAuthority.POLICY,
        ("queue_eligible",),
        ("dependency_blocked",),
        True,
    ),
    (
        "GWT-009",
        GovernedWorkflowState.ALLOCATING,
        GovernedWorkflowState.READY_TO_EXECUTE,
        WorkflowTransitionTrigger.WORKSPACE_ALLOCATED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("workspace_allocation_result", "tool_permission_profile"),
        ("workspace_missing",),
        True,
    ),
    (
        "GWT-010",
        GovernedWorkflowState.READY_TO_EXECUTE,
        GovernedWorkflowState.EXECUTING,
        WorkflowTransitionTrigger.EXECUTION_STARTED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("single_agent_execution_authorization",),
        ("dependency_blocked", "workspace_missing", "worker_missing"),
        True,
    ),
    (
        "GWT-011",
        GovernedWorkflowState.EXECUTING,
        GovernedWorkflowState.VALIDATING,
        WorkflowTransitionTrigger.EXECUTION_COMPLETED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("single_agent_execution_result",),
        (),
        True,
    ),
    (
        "GWT-012",
        GovernedWorkflowState.EXECUTING,
        GovernedWorkflowState.FAILED,
        WorkflowTransitionTrigger.EXECUTION_FAILED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("outcome_envelope",),
        (),
        True,
    ),
    (
        "GWT-013",
        GovernedWorkflowState.VALIDATING,
        GovernedWorkflowState.REVIEWING,
        WorkflowTransitionTrigger.VALIDATION_COMPLETED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("validation_command_runner_result",),
        (),
        True,
    ),
    (
        "GWT-014",
        GovernedWorkflowState.VALIDATING,
        GovernedWorkflowState.AWAITING_CORRECTION,
        WorkflowTransitionTrigger.VALIDATION_FAILED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("validation_failure_evidence",),
        (),
        True,
    ),
    (
        "GWT-015",
        GovernedWorkflowState.REVIEWING,
        GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
        WorkflowTransitionTrigger.REVIEW_ACCEPTED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("diff_artifact_review_result",),
        (),
        True,
    ),
    (
        "GWT-016",
        GovernedWorkflowState.REVIEWING,
        GovernedWorkflowState.AWAITING_CORRECTION,
        WorkflowTransitionTrigger.REVIEW_REJECTED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("review_rejection_evidence",),
        (),
        True,
    ),
    (
        "GWT-017",
        GovernedWorkflowState.REVIEWING,
        GovernedWorkflowState.AWAITING_CORRECTION,
        WorkflowTransitionTrigger.CORRECTION_REQUIRED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_correction_request",),
        (),
        False,
    ),
    (
        "GWT-018",
        GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
        GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
        WorkflowTransitionTrigger.HUMAN_APPROVED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_result_approval",),
        (),
        False,
    ),
    (
        "GWT-019",
        GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
        GovernedWorkflowState.AWAITING_CORRECTION,
        WorkflowTransitionTrigger.HUMAN_REJECTED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_result_rejection",),
        (),
        False,
    ),
    (
        "GWT-020",
        GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
        GovernedWorkflowState.COMPLETED,
        WorkflowTransitionTrigger.HUMAN_GIT_COMPLETED,
        WorkflowTransitionAuthority.HUMAN,
        ("git_handoff_result",),
        (),
        False,
    ),
    (
        "GWT-021",
        GovernedWorkflowState.QUEUED,
        GovernedWorkflowState.CANCELLED,
        WorkflowTransitionTrigger.CANCEL_REQUESTED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_cancellation_request",),
        (),
        False,
    ),
    (
        "GWT-022",
        GovernedWorkflowState.EXECUTING,
        GovernedWorkflowState.INCIDENT,
        WorkflowTransitionTrigger.INCIDENT_DETECTED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("incident_evidence",),
        (),
        True,
    ),
    (
        "GWT-023",
        GovernedWorkflowState.FAILED,
        GovernedWorkflowState.RETRY_PENDING,
        WorkflowTransitionTrigger.RETRY_AUTHORIZED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_retry_authorization",),
        (),
        False,
    ),
    (
        "GWT-024",
        GovernedWorkflowState.FAILED,
        GovernedWorkflowState.ROLLBACK_REQUIRED,
        WorkflowTransitionTrigger.ROLLBACK_AUTHORIZED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_rollback_authorization",),
        (),
        False,
    ),
)


_MAPPING_ROWS: tuple[
    tuple[GovernedWorkflowState, str, WorkflowRuntimeMappingKind, bool, str], ...
] = (
    (
        GovernedWorkflowState.DRAFT,
        "pepper:draft",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "No inherited runtime task exists before intake.",
    ),
    (
        GovernedWorkflowState.INTAKE_READY,
        "kanban:triage",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Kanban triage can hold intake work, but approval remains Pepper governance.",
    ),
    (
        GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
        "pepper:ticket_approval",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "Ticket approval is a human governance boundary.",
    ),
    (
        GovernedWorkflowState.TICKET_APPROVED,
        "ticket_factory:approved_ticket",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "Accepted TicketSpec is governance authority.",
    ),
    (
        GovernedWorkflowState.WORK_PACKET_READY,
        "p17:work_packet_ready",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "P17 WorkPacketCompilationResult remains governance authority.",
    ),
    (
        GovernedWorkflowState.QUEUED,
        "kanban:todo",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Kanban todo includes parent-gated queue mechanics.",
    ),
    (
        GovernedWorkflowState.QUEUED,
        "kanban:scheduled",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Kanban scheduled is a queued operational state.",
    ),
    (
        GovernedWorkflowState.BLOCKED,
        "kanban:blocked",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Kanban blocked records human or capability blockers.",
    ),
    (
        GovernedWorkflowState.BLOCKED,
        "kanban:todo_dependency",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Dependency blockers may be routed through parent-gated todo.",
    ),
    (
        GovernedWorkflowState.ALLOCATING,
        "runtime_adapter:starting",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Runtime adapter starting/waiting states map to allocation readiness.",
    ),
    (
        GovernedWorkflowState.ALLOCATING,
        "runtime_adapter:waiting_for_readiness",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Readiness wait is operational allocation progress.",
    ),
    (
        GovernedWorkflowState.READY_TO_EXECUTE,
        "kanban:ready",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Kanban ready can be reused for executable queue readiness.",
    ),
    (
        GovernedWorkflowState.READY_TO_EXECUTE,
        "runtime_adapter:ready",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Runtime adapter ready is executable readiness.",
    ),
    (
        GovernedWorkflowState.EXECUTING,
        "kanban:running",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Kanban running carries worker ownership and heartbeat mechanics.",
    ),
    (
        GovernedWorkflowState.VALIDATING,
        "p17:validation_command_runner",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "P17 validation result evidence governs validation state.",
    ),
    (
        GovernedWorkflowState.REVIEWING,
        "kanban:review",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Kanban review can display review posture.",
    ),
    (
        GovernedWorkflowState.REVIEWING,
        "p17:diff_artifact_review",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "P17 review result remains governance authority.",
    ),
    (
        GovernedWorkflowState.AWAITING_CORRECTION,
        "pepper:awaiting_correction",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "Correction loop is deferred to P18 review integration.",
    ),
    (
        GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
        "pepper:human_approval",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "Human approval is not generic provider readiness.",
    ),
    (
        GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
        "p17:human_git_handoff",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "P17.7 handoff preserves human Git authority.",
    ),
    (
        GovernedWorkflowState.COMPLETED,
        "kanban:done",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Kanban done can represent completed operational work.",
    ),
    (
        GovernedWorkflowState.FAILED,
        "runtime_adapter:failed",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Runtime adapter failed maps to governed failure posture.",
    ),
    (
        GovernedWorkflowState.FAILED,
        "kanban:task_run_failed",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Kanban task_runs record failure attempts and retry evidence.",
    ),
    (
        GovernedWorkflowState.CANCELLED,
        "runtime_adapter:cancelled",
        WorkflowRuntimeMappingKind.EXACT,
        True,
        "Runtime adapter cancellation maps to governed cancellation.",
    ),
    (
        GovernedWorkflowState.CANCELLED,
        "kanban:archived",
        WorkflowRuntimeMappingKind.RUNTIME_ONLY,
        False,
        "Kanban archived is runtime-only and not automatic workflow completion.",
    ),
    (
        GovernedWorkflowState.INCIDENT,
        "pepper:incident",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "Incident policy is deferred to P18.6.",
    ),
    (
        GovernedWorkflowState.RETRY_PENDING,
        "pepper:retry_pending",
        WorkflowRuntimeMappingKind.GOVERNANCE_ONLY,
        False,
        "Retry authorization is represented but not executed.",
    ),
    (
        GovernedWorkflowState.ROLLBACK_REQUIRED,
        "runtime_adapter:rollback_pending",
        WorkflowRuntimeMappingKind.COMPOSITE,
        False,
        "Runtime rollback pending is represented without executing rollback.",
    ),
)

_CAPABILITY_DECISIONS: tuple[tuple[str, str], ...] = (
    ("Kanban Swarm", "customize"),
    ("Kanban task lifecycle", "reuse"),
    ("dispatcher", "reuse"),
    ("heartbeat", "reuse"),
    ("retry evidence", "customize"),
    ("reclaim", "reuse"),
    ("workspace lifecycle", "customize"),
    ("planner", "reuse"),
    ("approval surfaces", "customize"),
    ("dashboard and TUI surfaces", "customize"),
    ("runtime adapter state machine", "reuse"),
    ("provider failure policy", "reuse"),
    ("execution inspector", "defer"),
    ("P19 G-Brain memory", "defer"),
    ("P20 Paperclip control plane", "defer"),
)

_PENDING_HUMAN_ACTIONS: dict[GovernedWorkflowState, str] = {
    GovernedWorkflowState.AWAITING_TICKET_APPROVAL: "ticket_approval",
    GovernedWorkflowState.AWAITING_CORRECTION: "correction",
    GovernedWorkflowState.AWAITING_HUMAN_APPROVAL: "workflow_result_approval",
    GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF: "human_git_handoff",
}


def _state_definitions() -> tuple[GovernedWorkflowStateDefinition, ...]:
    return tuple(
        GovernedWorkflowStateDefinition(
            state=state,
            owner=owner,
            entry_condition=entry,
            exit_condition=exit_condition,
            terminal=terminal,
            human_authority_required=human,
            operational_execution_allowed=execution,
            retry_allowed=retry,
            rollback_allowed=rollback,
            inherited_runtime_mapping=mapping,
            description=description,
        )
        for (
            state,
            owner,
            entry,
            exit_condition,
            terminal,
            human,
            execution,
            retry,
            rollback,
            mapping,
            description,
        ) in _STATE_DEFINITION_ROWS
    )


def _state_definition_for(
    state: GovernedWorkflowState,
) -> GovernedWorkflowStateDefinition:
    return _STATE_DEFINITION_LOOKUP[state]


def _transition_from_row(row: tuple[object, ...]) -> GovernedWorkflowTransition:
    (
        transition_id,
        from_state,
        to_state,
        trigger,
        authority,
        evidence,
        forbidden,
        automatic,
    ) = row
    return _make_model(
        GovernedWorkflowTransition,
        "transition_SHA256",
        WORKFLOW_TRANSITION_DIGEST_ALGORITHM,
        transition_id=transition_id,
        from_state=from_state,
        to_state=to_state,
        trigger=trigger,
        authority=authority,
        required_evidence=tuple(evidence),
        forbidden_when=tuple(forbidden),
        automatic=automatic,
    )


def _transitions() -> tuple[GovernedWorkflowTransition, ...]:
    return tuple(_transition_from_row(row) for row in _TRANSITION_ROWS)


def _transition_lookup() -> dict[
    tuple[
        GovernedWorkflowState, WorkflowTransitionTrigger, WorkflowTransitionAuthority
    ],
    GovernedWorkflowTransition,
]:
    return {
        (transition.from_state, transition.trigger, transition.authority): transition
        for transition in _TRANSITIONS
    }


def _mapping_from_row(row: tuple[object, ...]) -> WorkflowRuntimeStateMapping:
    governed_state, runtime_state, mapping_kind, exact, notes = row
    return _make_model(
        WorkflowRuntimeStateMapping,
        "mapping_SHA256",
        WORKFLOW_MAPPING_DIGEST_ALGORITHM,
        governed_state=governed_state,
        runtime_state=runtime_state,
        mapping_kind=mapping_kind,
        exact=exact,
        notes=notes,
    )


_STATE_DEFINITIONS = _state_definitions()
_STATE_DEFINITION_LOOKUP = {item.state: item for item in _STATE_DEFINITIONS}
_TRANSITIONS = _transitions()
_TRANSITION_LOOKUP = _transition_lookup()


def _workflow_id_for(
    project_id: str,
    ticket_id: str,
    ticket_revision: int,
    work_packet_id: str,
    work_packet_SHA256: str,
) -> str:
    payload = {
        "project_id": project_id,
        "ticket_id": ticket_id,
        "ticket_revision": ticket_revision,
        "work_packet_id": work_packet_id,
        "work_packet_SHA256": work_packet_SHA256,
        "workflow_policy_id": GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    }
    return f"GWF-{_digest(WORKFLOW_ID_DIGEST_ALGORITHM, payload)[:12]}"


def build_governed_workflow_identity(
    *,
    project_id: str,
    ticket_id: str,
    ticket_revision: int,
    work_packet_id: str,
    work_packet_SHA256: str,
) -> GovernedWorkflowIdentity:
    workflow_id = _workflow_id_for(
        project_id,
        ticket_id,
        ticket_revision,
        work_packet_id,
        work_packet_SHA256,
    )
    return _make_model(
        GovernedWorkflowIdentity,
        "identity_SHA256",
        WORKFLOW_IDENTITY_DIGEST_ALGORITHM,
        workflow_id=workflow_id,
        project_id=project_id,
        ticket_id=ticket_id,
        ticket_revision=ticket_revision,
        work_packet_id=work_packet_id,
        work_packet_SHA256=work_packet_SHA256,
        workflow_policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    )


def build_hermes_workflow_projection(
    *,
    runtime_kind: HermesWorkflowRuntimeKind,
    runtime_state: str,
    task_id: str | None,
    board_or_queue_id: str | None,
    worker_id_present: bool,
    workspace_binding_present: bool,
    dependency_blocked: bool,
    retry_state_present: bool,
    reclaim_state_present: bool,
) -> HermesWorkflowProjection:
    return _make_model(
        HermesWorkflowProjection,
        "projection_SHA256",
        WORKFLOW_PROJECTION_DIGEST_ALGORITHM,
        runtime_kind=runtime_kind,
        runtime_state=runtime_state,
        task_id=task_id,
        board_or_queue_id=board_or_queue_id,
        worker_id_present=worker_id_present,
        workspace_binding_present=workspace_binding_present,
        dependency_blocked=dependency_blocked,
        retry_state_present=retry_state_present,
        reclaim_state_present=reclaim_state_present,
        runtime_projection_is_authoritative_governance_state=False,
    )


def build_p17_workflow_binding(closure_result: P17ClosureResult) -> P17WorkflowBinding:
    validate_p17_closure_result(closure_result)
    if closure_result.state is not P17ClosureState.CLOSED:
        raise GovernedWorkflowStateMachineStateError("P17 closure must be closed")
    if closure_result.decision is not P17ClosureDecision.ACCEPTED:
        raise GovernedWorkflowStateMachineStateError("P17 closure must be accepted")
    if not closure_result.WorkPacket_execution_MVP_requirement_satisfied:
        raise GovernedWorkflowStateMachinePolicyError(
            "P17 WorkPacket MVP must be available"
        )
    if not closure_result.authority_boundary.human_Git_authority_required:
        raise GovernedWorkflowStateMachinePolicyError(
            "P17 human Git authority is required"
        )
    if not closure_result.closure_summary.non_critical_pilot_accepted:
        raise GovernedWorkflowStateMachinePolicyError(
            "P17 non-critical pilot must be accepted"
        )
    if closure_result.production_readiness_claimed:
        raise GovernedWorkflowStateMachinePolicyError(
            "P18.0 cannot consume production readiness"
        )
    return _make_model(
        P17WorkflowBinding,
        "binding_SHA256",
        WORKFLOW_P17_BINDING_DIGEST_ALGORITHM,
        P17_closure_id=closure_result.closure_id,
        P17_closure_SHA256=closure_result.result_SHA256,
        WorkPacket_execution_MVP_available=True,
        human_Git_authority_required=True,
        non_critical_scope=True,
        production_readiness_claimed=False,
    )


def build_initial_governed_workflow_snapshot(
    *,
    identity: GovernedWorkflowIdentity,
    P17_binding: P17WorkflowBinding,
    runtime_projection: HermesWorkflowProjection,
    current_state: GovernedWorkflowState = GovernedWorkflowState.DRAFT,
) -> GovernedWorkflowSnapshot:
    state_definition = _state_definition_for(current_state)
    return _make_model(
        GovernedWorkflowSnapshot,
        "workflow_SHA256",
        WORKFLOW_SNAPSHOT_DIGEST_ALGORITHM,
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        identity=identity,
        current_state=current_state,
        state_owner=state_definition.owner,
        transition_index=0,
        completed_transition_ids=(),
        active_blocker_codes=(),
        pending_human_action=_pending_human_action(current_state),
        P17_binding_SHA256=P17_binding.binding_SHA256,
        runtime_projection=runtime_projection,
    )


def validate_hermes_workflow_projection(projection: HermesWorkflowProjection) -> None:
    try:
        HermesWorkflowProjection.model_validate(projection)
    except ValueError as exc:
        raise GovernedWorkflowStateMachineValidationError(str(exc)) from exc


def validate_governed_workflow_snapshot(snapshot: GovernedWorkflowSnapshot) -> None:
    try:
        GovernedWorkflowSnapshot.model_validate(snapshot)
    except ValueError as exc:
        raise GovernedWorkflowStateMachineValidationError(str(exc)) from exc


def build_workflow_runtime_state_mappings() -> tuple[WorkflowRuntimeStateMapping, ...]:
    mappings = tuple(_mapping_from_row(row) for row in _MAPPING_ROWS)
    _validate_mapping_inventory(mappings)
    return mappings


def validate_governed_workflow_transition_request(
    request: GovernedWorkflowTransitionRequest,
) -> None:
    try:
        GovernedWorkflowTransitionRequest.model_validate(request)
        validate_governed_workflow_snapshot(request.current_snapshot)
        validate_hermes_workflow_projection(request.runtime_projection)
    except ValueError as exc:
        raise GovernedWorkflowStateMachineValidationError(str(exc)) from exc

    transition = _resolve_transition(request)
    missing = _missing_required_evidence(request, transition)
    if missing:
        raise GovernedWorkflowStateMachinePolicyError(
            f"missing required evidence: {missing[0]}"
        )
    blocking = _forbidden_reasons(request, transition)
    if blocking:
        raise GovernedWorkflowStateMachinePolicyError(
            f"transition forbidden: {blocking[0]}"
        )


def build_governed_workflow_transition(
    request: GovernedWorkflowTransitionRequest,
) -> GovernedWorkflowTransitionResult:
    previous = request.current_snapshot
    try:
        validate_governed_workflow_transition_request(request)
        transition = _resolve_transition(request)
    except GovernedWorkflowStateMachineError as exc:
        blocking = (_safe_blocking_reason(str(exc)),)
        rejected_transition = _make_model(
            GovernedWorkflowTransition,
            "transition_SHA256",
            WORKFLOW_TRANSITION_DIGEST_ALGORITHM,
            transition_id="GWT-REJECTED",
            from_state=previous.current_state,
            to_state=previous.current_state,
            trigger=request.trigger,
            authority=request.authority,
            required_evidence=(),
            forbidden_when=blocking,
            automatic=False,
        )
        return _make_model(
            GovernedWorkflowTransitionResult,
            "result_SHA256",
            WORKFLOW_RESULT_DIGEST_ALGORITHM,
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            previous_snapshot_SHA256=previous.workflow_SHA256,
            transition=rejected_transition,
            resulting_snapshot=previous,
            accepted=False,
            blocking_reasons=blocking,
            human_action_required=previous.current_state in _HUMAN_PENDING_STATES,
        )

    resulting_snapshot = _resulting_snapshot(
        previous, transition, request.runtime_projection
    )
    return _make_model(
        GovernedWorkflowTransitionResult,
        "result_SHA256",
        WORKFLOW_RESULT_DIGEST_ALGORITHM,
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        previous_snapshot_SHA256=previous.workflow_SHA256,
        transition=transition,
        resulting_snapshot=resulting_snapshot,
        accepted=True,
        blocking_reasons=(),
        human_action_required=resulting_snapshot.current_state in _HUMAN_PENDING_STATES,
    )


def build_governed_workflow_state_machine_result(
    P17_binding: P17WorkflowBinding,
) -> GovernedWorkflowStateMachineResult:
    state_definitions = _STATE_DEFINITIONS
    runtime_mappings = build_workflow_runtime_state_mappings()
    findings = _build_findings()
    reuse_summary = _build_reuse_summary()
    result = _make_model(
        GovernedWorkflowStateMachineResult,
        "result_SHA256",
        WORKFLOW_RESULT_DIGEST_ALGORITHM,
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        state_definitions=state_definitions,
        transitions=_TRANSITIONS,
        runtime_mappings=runtime_mappings,
        P17_binding=P17_binding,
        findings=findings,
        reuse_summary=reuse_summary,
        state_machine_ready=True,
        P18_1_ready=True,
        production_readiness_claimed=False,
    )
    return result


def _resolve_transition(
    request: GovernedWorkflowTransitionRequest,
) -> GovernedWorkflowTransition:
    if request.current_snapshot.current_state in _TERMINAL_STATES:
        raise GovernedWorkflowStateMachineStateError("terminal state cannot transition")
    key = (request.current_snapshot.current_state, request.trigger, request.authority)
    try:
        return _TRANSITION_LOOKUP[key]
    except KeyError as exc:
        raise GovernedWorkflowStateMachineStateError(
            "transition is not allowed"
        ) from exc


def _missing_required_evidence(
    request: GovernedWorkflowTransitionRequest,
    transition: GovernedWorkflowTransition,
) -> tuple[str, ...]:
    provided = set(request.evidence_refs)
    return tuple(item for item in transition.required_evidence if item not in provided)


def _forbidden_reasons(
    request: GovernedWorkflowTransitionRequest,
    transition: GovernedWorkflowTransition,
) -> tuple[str, ...]:
    reasons: list[str] = []
    projection = request.runtime_projection
    for condition in transition.forbidden_when:
        if condition == "dependency_blocked" and projection.dependency_blocked:
            reasons.append(condition)
        elif (
            condition == "workspace_missing"
            and not projection.workspace_binding_present
        ):
            reasons.append(condition)
        elif condition == "worker_missing" and not projection.worker_id_present:
            reasons.append(condition)
    return tuple(reasons)


def _safe_blocking_reason(message: str) -> str:
    lowered = re.sub(r"[^a-z0-9_:-]+", "_", message.lower()).strip("_:")
    if not lowered:
        return "request_rejected"
    return lowered[:80]


def _pending_human_action(state: GovernedWorkflowState) -> str | None:
    return _PENDING_HUMAN_ACTIONS.get(state)


def _blockers_for_target(
    transition: GovernedWorkflowTransition,
) -> tuple[BlockerCode, ...]:
    if transition.to_state is GovernedWorkflowState.BLOCKED:
        return ("dependency_blocked",)
    if transition.to_state is GovernedWorkflowState.AWAITING_CORRECTION:
        return ("correction_required",)
    if transition.to_state is GovernedWorkflowState.FAILED:
        return ("execution_failed",)
    if transition.to_state is GovernedWorkflowState.INCIDENT:
        return ("incident_detected",)
    return ()


def _resulting_snapshot(
    previous: GovernedWorkflowSnapshot,
    transition: GovernedWorkflowTransition,
    runtime_projection: HermesWorkflowProjection,
) -> GovernedWorkflowSnapshot:
    state_definition = _state_definition_for(transition.to_state)
    completed = previous.completed_transition_ids + (transition.transition_id,)
    return _make_model(
        GovernedWorkflowSnapshot,
        "workflow_SHA256",
        WORKFLOW_SNAPSHOT_DIGEST_ALGORITHM,
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        identity=previous.identity,
        current_state=transition.to_state,
        state_owner=state_definition.owner,
        transition_index=previous.transition_index + 1,
        completed_transition_ids=completed,
        active_blocker_codes=_blockers_for_target(transition),
        pending_human_action=_pending_human_action(transition.to_state),
        P17_binding_SHA256=previous.P17_binding_SHA256,
        runtime_projection=runtime_projection,
    )


def _validate_mapping_inventory(
    mappings: tuple[WorkflowRuntimeStateMapping, ...],
) -> None:
    keys = tuple((item.runtime_state, item.governed_state) for item in mappings)
    if len(keys) != len(set(keys)):
        raise GovernedWorkflowStateMachinePolicyError("duplicate runtime mapping")
    missing = set(GovernedWorkflowState) - {item.governed_state for item in mappings}
    if missing:
        raise GovernedWorkflowStateMachinePolicyError("state mapping missing")
    relevant = {f"kanban:{state}" for state in _RELEVANT_KANBAN_STATES}
    mapped = {item.runtime_state for item in mappings}
    if relevant - mapped - {"kanban:todo_dependency"}:
        raise GovernedWorkflowStateMachinePolicyError("relevant Kanban state unmapped")


def _build_finding(
    finding_id: str,
    severity: WorkflowStateMachineFindingSeverity,
    code: WorkflowStateMachineFindingCode,
    capability: str | None,
    summary: str,
) -> WorkflowStateMachineFinding:
    return _make_model(
        WorkflowStateMachineFinding,
        "finding_SHA256",
        WORKFLOW_FINDING_DIGEST_ALGORITHM,
        finding_id=finding_id,
        severity=severity,
        code=code,
        capability=capability,
        summary=summary,
    )


def _build_findings() -> tuple[WorkflowStateMachineFinding, ...]:
    rows = (
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_CUSTOMIZED,
            "Kanban Swarm",
            "Kanban mechanics are reused with Pepper governed-state mapping.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "Kanban task lifecycle",
            "Existing task statuses, dependency gating and completion mechanics are retained.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "dispatcher",
            "Existing dispatcher loop is retained as operational mechanics.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "heartbeat",
            "Existing worker heartbeat and liveness posture are retained.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_CUSTOMIZED,
            "retry evidence",
            "Retry evidence is represented without automatic retry execution.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "reclaim",
            "Existing stale-claim reclaim mechanics are retained operationally.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_CUSTOMIZED,
            "workspace lifecycle",
            "P17 workspace allocation remains governance authority over runtime workspace mechanics.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "planner",
            "Existing Ticket Factory dependency planning is retained for sequencing evidence.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_CUSTOMIZED,
            "approval surfaces",
            "Approval surfaces are mapped to explicit human workflow states.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_CUSTOMIZED,
            "dashboard and TUI surfaces",
            "Current UI state is display evidence, not Pepper workflow authority.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "runtime adapter state machine",
            "Runtime adapter lifecycle states are mapped where relevant.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_REUSED,
            "provider failure policy",
            "Provider failure policy remains advisory and does not authorize P18.0 execution.",
        ),
        (
            WorkflowStateMachineFindingSeverity.WARNING,
            WorkflowStateMachineFindingCode.HERMES_CAPABILITY_GAP,
            "execution inspector",
            "Dedicated execution-inspector integration is deferred to later workflow migration.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.STATE_MAPPING_COMPLETE,
            "runtime mappings",
            "Every P18.0 governed state has an explicit runtime or governance mapping.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.P17_BINDING_VALID,
            "P17 closure",
            "P17 WorkPacket Execution MVP remains the governance authority.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.HUMAN_BOUNDARY_PRESERVED,
            "human authority",
            "Human approval and human Git handoff remain explicit boundaries.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.RUNTIME_PROJECTION_NON_AUTHORITATIVE,
            "runtime projection",
            "Hermes runtime projection is not authoritative governance state.",
        ),
        (
            WorkflowStateMachineFindingSeverity.INFO,
            WorkflowStateMachineFindingCode.WORKFLOW_READY,
            "P18.0",
            "Governed workflow state machine is ready for P18.1 intake integration.",
        ),
    )
    return tuple(
        _build_finding(f"GSMF-{index:03d}", severity, code, capability, summary)
        for index, (severity, code, capability, summary) in enumerate(rows, start=1)
    )


def _build_reuse_summary() -> WorkflowReuseSummary:
    decisions = tuple(decision for _capability, decision in _CAPABILITY_DECISIONS)
    return _make_model(
        WorkflowReuseSummary,
        "summary_SHA256",
        WORKFLOW_REUSE_SUMMARY_DIGEST_ALGORITHM,
        capabilities_assessed=len(decisions),
        capabilities_reused=decisions.count("reuse"),
        capabilities_customized=decisions.count("customize"),
        capabilities_replaced=decisions.count("replace"),
        capabilities_deferred=decisions.count("defer"),
        duplicate_runtime_capabilities_created=0,
        Kanban_Swarm_assessed=True,
        planner_assessed=True,
        dispatcher_assessed=True,
        heartbeat_assessed=True,
        retry_assessed=True,
        reclaim_assessed=True,
        workspace_lifecycle_assessed=True,
        approval_surfaces_assessed=True,
        dashboard_TUI_surfaces_assessed=True,
        prior_Hermes_0_19_analysis_reused=True,
        current_targeted_revalidation_performed=True,
    )


__all__ = (
    "GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION",
    "GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID",
    "GovernedWorkflowState",
    "WorkflowStateOwner",
    "WorkflowTransitionTrigger",
    "WorkflowTransitionAuthority",
    "HermesWorkflowRuntimeKind",
    "WorkflowRuntimeMappingKind",
    "WorkflowStateMachineFindingSeverity",
    "WorkflowStateMachineFindingCode",
    "GovernedWorkflowStateDefinition",
    "GovernedWorkflowTransition",
    "GovernedWorkflowIdentity",
    "GovernedWorkflowSnapshot",
    "HermesWorkflowProjection",
    "WorkflowRuntimeStateMapping",
    "GovernedWorkflowTransitionRequest",
    "GovernedWorkflowTransitionResult",
    "P17WorkflowBinding",
    "WorkflowStateMachineFinding",
    "WorkflowReuseSummary",
    "GovernedWorkflowStateMachineResult",
    "GovernedWorkflowStateMachineError",
    "GovernedWorkflowStateMachineInputError",
    "GovernedWorkflowStateMachineIntegrityError",
    "GovernedWorkflowStateMachinePolicyError",
    "GovernedWorkflowStateMachineStateError",
    "GovernedWorkflowStateMachineValidationError",
    "build_governed_workflow_identity",
    "build_hermes_workflow_projection",
    "build_p17_workflow_binding",
    "build_initial_governed_workflow_snapshot",
    "build_workflow_runtime_state_mappings",
    "validate_hermes_workflow_projection",
    "validate_governed_workflow_snapshot",
    "validate_governed_workflow_transition_request",
    "build_governed_workflow_transition",
    "build_governed_workflow_state_machine_result",
)
