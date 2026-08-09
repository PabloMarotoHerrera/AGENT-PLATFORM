"""P18.4 dependency-aware queue admission integration for Pepper.

This module validates a P18.3 human-approved handoff, reuses the accepted P16
dependency plan already bound by P18.2, and emits deterministic queue admission
evidence. It does not enqueue a live Kanban task, claim workers, allocate
workspaces, execute commands, call providers/models, mutate Git, invoke Docker,
invoke Graphify, write G-Brain memory, operate Paperclip or start execution.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import re
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory import (
    HumanApprovalDecision,
    TicketDependencyPlan,
    WaveDisposition,
)
from hermes_cli.agent_platform.workflow.approval_workflow import (
    APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID,
    APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION,
    ApprovalWorkflowIntegrationResult,
    ApprovalWorkflowResultDecision,
    ApprovalWorkflowState,
    validate_approval_workflow_integration_result,
)
from hermes_cli.agent_platform.workflow.governed_state_machine import (
    GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
    GovernedWorkflowSnapshot,
    GovernedWorkflowState,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowRuntimeKind,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_governed_workflow_transition,
    build_hermes_workflow_projection,
    validate_governed_workflow_transition_request,
)


DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION = 1
DEPENDENCY_AWARE_QUEUE_POLICY_ID = "pepper-dependency-aware-execution-queue-v1"

QUEUE_REQUEST_DIGEST_ALGORITHM = "agent-platform-dependency-queue-request-sha256-v1"
QUEUE_CANDIDATE_DIGEST_ALGORITHM = "agent-platform-dependency-queue-candidate-sha256-v1"
QUEUE_SATISFACTION_DIGEST_ALGORITHM = (
    "agent-platform-dependency-satisfaction-evidence-sha256-v1"
)
QUEUE_BLOCKER_DIGEST_ALGORITHM = "agent-platform-dependency-queue-blocker-sha256-v1"
QUEUE_ADMISSION_BOUNDARY_DIGEST_ALGORITHM = (
    "agent-platform-dependency-queue-admission-boundary-sha256-v1"
)
QUEUE_HANDOFF_DIGEST_ALGORITHM = (
    "agent-platform-dependency-queue-p18-5-handoff-sha256-v1"
)
QUEUE_FINDING_DIGEST_ALGORITHM = "agent-platform-dependency-queue-finding-sha256-v1"
QUEUE_SUMMARY_DIGEST_ALGORITHM = "agent-platform-dependency-queue-summary-sha256-v1"
QUEUE_RESULT_CORE_DIGEST_ALGORITHM = (
    "agent-platform-dependency-queue-core-result-sha256-v1"
)
QUEUE_RESULT_DIGEST_ALGORITHM = "agent-platform-dependency-queue-result-sha256-v1"
QUEUE_INTEGRATION_ID_DIGEST_ALGORITHM = "agent-platform-dependency-queue-id-sha256-v1"

_CANONICAL_PROJECT_ID = "PEPPER"
_CANONICAL_MACROPROJECT_ID = "P18"
_CANONICAL_TICKET_ID = "P18.2"
_CANONICAL_PREREQUISITE_TICKET_ID = "P18.1"
_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_INTEGRATION_ID_PATTERN = r"^DQI-P18-[a-f0-9]{12}$"
_FINDING_ID_PATTERN = r"^DQIF-[0-9]{3}$"
_WORK_PACKET_ID_PATTERN = r"^WP-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$"
_TICKET_ID_PATTERN = r"^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$"
_CONTROL_OR_ANSI_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x1b]")
_PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)")
_SHELL_COMMAND_PATTERN = re.compile(
    r"(?:\bgit\s+(?:add|commit|push|checkout|switch|merge|rebase|reset|stash|tag|worktree)\b)"
    r"|(?:\bdocker\s+(?:build|run|compose|pull|push)\b)"
    r"|(?:\bgraphify\s+(?:update|extract|export|cluster|recluster|query|path|explain)\b)"
    r"|(?:\b(?:subprocess|shell|powershell|cmd\.exe|bash)\b)"
    r"|(?:\b(?:execute_work_packet|run_queue|dispatch_work_packet|launch_worker)\b)",
    re.IGNORECASE,
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
_RAW_CONTEXT_MARKERS = (
    "raw prompt",
    "system prompt",
    "reasoning trace",
    "provider response",
    "model output",
    "raw stdout",
    "raw stderr",
    "raw conversation",
    "chatgpt transcript",
    "opencode transcript",
    "diff --git",
    "runtime handle",
    "git handle",
)
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")

DigestText = Annotated[str, Field(pattern=_DIGEST_PATTERN)]
IntegrationIdentifier = Annotated[str, Field(pattern=_INTEGRATION_ID_PATTERN)]
FindingIdentifier = Annotated[str, Field(pattern=_FINDING_ID_PATTERN)]
WorkPacketIdentifier = Annotated[str, Field(pattern=_WORK_PACKET_ID_PATTERN)]
TicketIdentifier = Annotated[str, Field(pattern=_TICKET_ID_PATTERN)]
BoundedText = Annotated[str, Field(min_length=1, max_length=1024)]


class DependencyAwareQueueIntegrationError(ValueError):
    """Base error for P18.4 dependency-aware queue integration failures."""


class DependencyAwareQueueInputError(DependencyAwareQueueIntegrationError):
    """Raised when caller-supplied queue inputs are malformed."""


class DependencyAwareQueueIntegrityError(DependencyAwareQueueIntegrationError):
    """Raised when queue evidence digests or artifact bindings mismatch."""


class DependencyAwareQueuePolicyError(DependencyAwareQueueIntegrationError):
    """Raised when queue policy boundaries are violated."""


class DependencyAwareQueueStateError(DependencyAwareQueueIntegrationError):
    """Raised when workflow or approval state is not queue-admissible."""


class DependencyAwareQueueValidationError(DependencyAwareQueueIntegrationError):
    """Raised when immutable P18.4 queue evidence fails validation."""


class QueueCapabilityDecision(str, Enum):
    RETAIN = "retain"
    CUSTOMIZE = "customize"
    REPLACE = "replace"
    DEFER = "defer"
    NOT_APPLICABLE = "not_applicable"


class DependencySatisfactionState(str, Enum):
    SATISFIED = "satisfied"
    UNSATISFIED = "unsatisfied"
    UNKNOWN = "unknown"
    MALFORMED = "malformed"
    STALE = "stale"


class DependencyAwareQueueDecision(str, Enum):
    ADMIT = "admit"
    BLOCKED = "blocked"


class DependencyAwareQueueState(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"


class DependencyAwareQueueFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class DependencyAwareQueueFindingCode(str, Enum):
    P18_3_CONTINUATION_VALID = "p18_3_continuation_valid"
    APPROVAL_BINDING_VALID = "approval_binding_valid"
    DEPENDENCY_PLANNER_REUSED = "dependency_planner_reused"
    DEPENDENCY_EVIDENCE_VALID = "dependency_evidence_valid"
    QUEUE_CANDIDATE_VALID = "queue_candidate_valid"
    QUEUE_DECISION_VALID = "queue_decision_valid"
    WORKFLOW_TRANSITION_VALID = "workflow_transition_valid"
    DISPATCHER_BOUNDARY_PRESERVED = "dispatcher_boundary_preserved"
    EXECUTION_AUTHORITY_PROHIBITED = "execution_authority_prohibited"
    P18_5_HANDOFF_READY = "p18_5_handoff_ready"
    DUPLICATE_RUNTIME_AVOIDED = "duplicate_runtime_avoided"
    INTEGRATION_ACCEPTED = "integration_accepted"


class _DependencyQueueModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        protected_namespaces=(),
        validate_default=True,
        str_strip_whitespace=True,
    )


def _validate_safe_text(value: str, label: str) -> str:
    if _CONTROL_OR_ANSI_PATTERN.search(value):
        raise ValueError(f"{label} contains control characters")
    lowered = value.lower()
    if any(marker in lowered for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} contains credential-like content")
    if any(marker in lowered for marker in _RAW_CONTEXT_MARKERS):
        raise ValueError(f"{label} contains raw context")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-like content")
    if _PERSONAL_PATH_PATTERN.search(value):
        raise ValueError(f"{label} contains a personal absolute path")
    if _SHELL_COMMAND_PATTERN.search(value):
        raise ValueError(f"{label} contains execution-shaped content")
    return value


def _normalize_for_digest(value: object) -> object:
    if isinstance(value, BaseModel):
        return _normalize_for_digest(value.model_dump(mode="json", warnings=False))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_normalize_for_digest(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize_for_digest(item) for key, item in value.items()}
    return value


def _digest_from_record(algorithm: str, record: object) -> str:
    payload = {"algorithm": algorithm, "record": _normalize_for_digest(record)}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _model_digest(algorithm: str, value: BaseModel, digest_field: str) -> str:
    return _digest_from_record(
        algorithm,
        value.model_dump(mode="json", exclude={digest_field}, warnings=False),
    )


def _make_model(
    model_type: type[_DependencyQueueModel],
    digest_field: str,
    algorithm: str,
    **values: object,
) -> _DependencyQueueModel:
    data = dict(values)
    data[digest_field] = "0" * 64
    provisional = model_type.model_construct(**data)
    data[digest_field] = _model_digest(algorithm, provisional, digest_field)
    return model_type(**data)


class QueueRuntimeCapabilityAssessment(_DependencyQueueModel):
    capability: BoundedText
    file: BoundedText
    symbol: BoundedText
    purpose: BoundedText
    accepted_authority: BoundedText
    suitable_for_P18_4: StrictBool
    decision: QueueCapabilityDecision
    customization_needed: BoundedText
    duplicate_created: Literal[False]

    @field_validator(
        "capability",
        "file",
        "symbol",
        "purpose",
        "accepted_authority",
        "customization_needed",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "queue capability assessment")


class DependencySatisfactionEvidence(_DependencyQueueModel):
    dependency_ticket_id: TicketIdentifier
    required_relationship: BoundedText
    satisfaction_state: DependencySatisfactionState
    evidence_reference: BoundedText
    evidence_SHA256: DigestText | None = None
    satisfaction_SHA256: DigestText

    @field_validator("required_relationship", "evidence_reference", mode="after")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "dependency satisfaction evidence")

    @model_validator(mode="after")
    def _validate_satisfaction(self) -> DependencySatisfactionEvidence:
        if (
            self.satisfaction_state is DependencySatisfactionState.SATISFIED
            and self.evidence_SHA256 is None
        ):
            raise ValueError("satisfied dependencies require evidence_SHA256")
        if self.satisfaction_SHA256 != _model_digest(
            QUEUE_SATISFACTION_DIGEST_ALGORITHM,
            self,
            "satisfaction_SHA256",
        ):
            raise ValueError("satisfaction_SHA256 must match evidence digest")
        return self


class DependencyAwareQueueRequest(_DependencyQueueModel):
    schema_version: Literal[1] = DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION
    policy_id: Literal["pepper-dependency-aware-execution-queue-v1"] = (
        DEPENDENCY_AWARE_QUEUE_POLICY_ID
    )
    approval_result: ApprovalWorkflowIntegrationResult
    P18_3_result_SHA256: DigestText
    approval_result_SHA256: DigestText
    approval_decision_SHA256: DigestText
    TicketSpec_SHA256: DigestText
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    dependency_plan: TicketDependencyPlan
    dependency_plan_SHA256: DigestText
    workflow_snapshot: GovernedWorkflowSnapshot
    expected_current_state: Literal[GovernedWorkflowState.TICKET_APPROVED]
    dependency_satisfaction_evidence: tuple[DependencySatisfactionEvidence, ...] = (
        Field(default=(), max_length=64)
    )
    prior_queue_result_SHA256: DigestText | None = None
    prior_queue_decision: DependencyAwareQueueDecision | None = None
    requested_worker_dispatch: Literal[False] = False
    requested_command_execution: Literal[False] = False
    requested_provider_dispatch: Literal[False] = False
    requested_model_inference: Literal[False] = False
    queue_request_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_request_digest(self) -> DependencyAwareQueueRequest:
        if self.queue_request_SHA256 != _model_digest(
            QUEUE_REQUEST_DIGEST_ALGORITHM,
            self,
            "queue_request_SHA256",
        ):
            raise ValueError("queue_request_SHA256 must match request digest")
        return self


class DependencyAwareQueueCandidate(_DependencyQueueModel):
    schema_version: Literal[1] = DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION
    policy_id: Literal["pepper-dependency-aware-execution-queue-v1"] = (
        DEPENDENCY_AWARE_QUEUE_POLICY_ID
    )
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    P18_3_result_SHA256: DigestText
    approval_result_SHA256: DigestText
    approval_decision_SHA256: DigestText
    TicketSpec_SHA256: DigestText
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    dependency_plan_SHA256: DigestText
    workflow_snapshot_SHA256: DigestText
    queue_candidate: Literal[True]
    queue_candidate_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_candidate_digest(self) -> DependencyAwareQueueCandidate:
        if self.queue_candidate_SHA256 != _model_digest(
            QUEUE_CANDIDATE_DIGEST_ALGORITHM,
            self,
            "queue_candidate_SHA256",
        ):
            raise ValueError("queue_candidate_SHA256 must match queue candidate digest")
        return self


class DependencyQueueBlocker(_DependencyQueueModel):
    dependency_ticket_id: TicketIdentifier
    required_relationship: BoundedText
    satisfaction_state: DependencySatisfactionState
    evidence_reference: BoundedText
    evidence_SHA256: DigestText | None
    blocker_SHA256: DigestText

    @field_validator("required_relationship", "evidence_reference", mode="after")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "dependency queue blocker")

    @model_validator(mode="after")
    def _validate_blocker_digest(self) -> DependencyQueueBlocker:
        if self.satisfaction_state is DependencySatisfactionState.SATISFIED:
            raise ValueError("satisfied dependencies cannot be queue blockers")
        if self.blocker_SHA256 != _model_digest(
            QUEUE_BLOCKER_DIGEST_ALGORITHM,
            self,
            "blocker_SHA256",
        ):
            raise ValueError("blocker_SHA256 must match dependency blocker digest")
        return self


class QueueAdmissionBoundary(_DependencyQueueModel):
    queue_persistence_mechanism: Literal["result_envelope_only"]
    provisional_runtime_authority: Literal["kanban_projection_deferred"]
    canonical_long_term_authority: Literal["p20_paperclip_deferred"]
    Kanban_SQLite_canonical: Literal[False]
    Paperclip_calls: Literal[0]
    GBrain_calls: Literal[0]
    existing_queue_projection_calls: Literal[0]
    does_not_dispatch: Literal[True]
    does_not_execute: Literal[True]
    duplicate_dependency_planner_created: Literal[False]
    duplicate_execution_queue_created: Literal[False]
    duplicate_scheduler_created: Literal[False]
    duplicate_dispatcher_created: Literal[False]
    duplicate_Kanban_backend_created: Literal[False]
    duplicate_WorkPacket_executor_created: Literal[False]
    duplicate_workflow_state_machine_created: Literal[False]
    boundary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_boundary_digest(self) -> QueueAdmissionBoundary:
        if self.boundary_SHA256 != _model_digest(
            QUEUE_ADMISSION_BOUNDARY_DIGEST_ALGORITHM,
            self,
            "boundary_SHA256",
        ):
            raise ValueError("boundary_SHA256 must match queue boundary digest")
        return self


class DependencyAwareQueueFinding(_DependencyQueueModel):
    finding_id: FindingIdentifier
    severity: DependencyAwareQueueFindingSeverity
    code: DependencyAwareQueueFindingCode
    subject_id: BoundedText
    summary: BoundedText
    failed_invariant: BoundedText | None = None
    finding_SHA256: DigestText

    @field_validator("subject_id", "summary", "failed_invariant", mode="after")
    @classmethod
    def _validate_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_safe_text(value, "queue finding")

    @model_validator(mode="after")
    def _validate_finding_digest(self) -> DependencyAwareQueueFinding:
        if self.severity is DependencyAwareQueueFindingSeverity.BLOCKING:
            if self.failed_invariant is None:
                raise ValueError("blocking findings require failed_invariant")
        elif self.failed_invariant is not None:
            raise ValueError("non-blocking findings must not include failed_invariant")
        if self.finding_SHA256 != _model_digest(
            QUEUE_FINDING_DIGEST_ALGORITHM,
            self,
            "finding_SHA256",
        ):
            raise ValueError("finding_SHA256 must match queue finding digest")
        return self


class DependencyAwareQueueP18_5Handoff(_DependencyQueueModel):
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    TicketSpec_SHA256: DigestText
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    approval_decision_SHA256: DigestText
    queue_decision: DependencyAwareQueueDecision
    queue_result_SHA256: DigestText
    dependency_plan_SHA256: DigestText
    resulting_workflow_state: GovernedWorkflowState
    execution_started: Literal[False]
    P18_5_ready: StrictBool
    handoff_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_handoff_digest(self) -> DependencyAwareQueueP18_5Handoff:
        expected_ready = self.queue_decision is DependencyAwareQueueDecision.ADMIT
        if self.P18_5_ready != expected_ready:
            raise ValueError("P18_5_ready must derive from queue decision")
        if self.handoff_SHA256 != _model_digest(
            QUEUE_HANDOFF_DIGEST_ALGORITHM,
            self,
            "handoff_SHA256",
        ):
            raise ValueError("handoff_SHA256 must match P18.5 handoff digest")
        return self


class DependencyAwareQueueSummary(_DependencyQueueModel):
    P18_3_continuation_valid: StrictBool
    project_identity_valid: StrictBool
    approval_binding_valid: StrictBool
    dependency_plan_valid: StrictBool
    dependency_planner_reused: StrictBool
    dependency_plan_recomputed_unnecessarily: Literal[False]
    dependency_evidence_valid: StrictBool
    queue_candidate_valid: StrictBool
    queue_decision_valid: StrictBool
    queue_admission_valid: StrictBool
    dependency_blocking_valid: StrictBool
    workflow_transition_valid: StrictBool
    dispatcher_boundary_valid: StrictBool
    execution_prohibition_valid: StrictBool
    replay_policy_valid: StrictBool
    P18_5_handoff_valid: StrictBool
    information_finding_count: int = Field(ge=0, le=128, strict=True)
    warning_finding_count: int = Field(ge=0, le=128, strict=True)
    blocking_finding_count: int = Field(ge=0, le=128, strict=True)
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary_digest(self) -> DependencyAwareQueueSummary:
        if self.summary_SHA256 != _model_digest(
            QUEUE_SUMMARY_DIGEST_ALGORITHM,
            self,
            "summary_SHA256",
        ):
            raise ValueError("summary_SHA256 must match queue summary digest")
        if self.warning_finding_count or self.blocking_finding_count:
            raise ValueError(
                "P18.4 canonical queue evidence must have no warnings or blockers"
            )
        return self


class DependencyAwareQueueIntegrationResult(_DependencyQueueModel):
    schema_version: Literal[1] = DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION
    policy_id: Literal["pepper-dependency-aware-execution-queue-v1"] = (
        DEPENDENCY_AWARE_QUEUE_POLICY_ID
    )
    integration_id: IntegrationIdentifier
    state: DependencyAwareQueueState
    decision: DependencyAwareQueueDecision
    request: DependencyAwareQueueRequest
    queue_candidate: DependencyAwareQueueCandidate
    runtime_capability_assessments: tuple[QueueRuntimeCapabilityAssessment, ...]
    dependency_satisfaction_evidence: tuple[DependencySatisfactionEvidence, ...]
    dependency_blockers: tuple[DependencyQueueBlocker, ...]
    queue_admission_boundary: QueueAdmissionBoundary
    workflow_transition_results: tuple[GovernedWorkflowTransitionResult, ...] = Field(
        min_length=2, max_length=2
    )
    resulting_workflow_snapshot: GovernedWorkflowSnapshot
    findings: tuple[DependencyAwareQueueFinding, ...]
    summary: DependencyAwareQueueSummary
    handoff: DependencyAwareQueueP18_5Handoff
    queue_result_SHA256: DigestText
    approval_granted: Literal[True]
    dependencies_satisfied: StrictBool
    queue_eligible: StrictBool
    queue_admitted: StrictBool
    dispatch_eligible: Literal[False]
    ticket_execution_authorized: Literal[False]
    WorkPacket_execution_authorized: Literal[False]
    execution_started: Literal[False]
    WorkPacket_execution_started: Literal[False]
    worker_dispatch_count: Literal[0]
    command_execution_count: Literal[0]
    provider_dispatch_count: Literal[0]
    model_inference_count: Literal[0]
    Git_commands_executed: Literal[0]
    Docker_commands_executed: Literal[0]
    Graphify_commands_executed: Literal[0]
    claim_count: Literal[0]
    heartbeat_count: Literal[0]
    reclaim_count: Literal[0]
    workspace_allocation_count: Literal[0]
    validation_command_execution_count: Literal[0]
    retry_execution_count: Literal[0]
    automatic_requeue_count: Literal[0]
    rollback_count: Literal[0]
    staging_calls: Literal[0]
    commit_calls: Literal[0]
    push_calls: Literal[0]
    GBrain_calls: Literal[0]
    Paperclip_calls: Literal[0]
    P17_execution_substrate_reused: Literal[True]
    P17_execution_invoked: Literal[False]
    dispatcher_calls_in_P18_4: Literal[0]
    queue_order_deterministic: Literal[True]
    arbitrary_random_ordering: Literal[False]
    cycle_detection_reused: Literal[True]
    duplicate_cycle_detector_created: Literal[False]
    P18_5_ready: StrictBool
    production_readiness_claimed: Literal[False]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> DependencyAwareQueueIntegrationResult:
        if self.queue_result_SHA256 != _queue_result_core_digest_from_result(self):
            raise ValueError("queue_result_SHA256 must match queue core result digest")
        if self.result_SHA256 != _model_digest(
            QUEUE_RESULT_DIGEST_ALGORITHM,
            self,
            "result_SHA256",
        ):
            raise ValueError("result_SHA256 must match queue integration digest")
        if self.integration_id != _integration_id_from_record(
            self.model_dump(mode="json", exclude={"integration_id", "result_SHA256"})
        ):
            raise ValueError("integration_id must match deterministic queue identity")
        expected_admitted = self.decision is DependencyAwareQueueDecision.ADMIT
        if self.queue_admitted != expected_admitted:
            raise ValueError("queue_admitted must derive from decision")
        if self.queue_eligible != self.dependencies_satisfied:
            raise ValueError(
                "queue eligibility must derive from dependency satisfaction"
            )
        if self.P18_5_ready != expected_admitted:
            raise ValueError("P18_5_ready must derive from queue decision")
        if self.handoff.queue_result_SHA256 != self.queue_result_SHA256:
            raise ValueError("handoff must bind queue result digest")
        if self.handoff.P18_5_ready != self.P18_5_ready:
            raise ValueError("handoff readiness must match result")
        if (
            self.resulting_workflow_snapshot.current_state
            is not self.handoff.resulting_workflow_state
        ):
            raise ValueError("handoff state must match resulting workflow state")
        return self


def build_dependency_satisfaction_evidence(
    *,
    dependency_ticket_id: str,
    required_relationship: str,
    satisfaction_state: DependencySatisfactionState,
    evidence_reference: str,
    evidence_SHA256: str | None = None,
) -> DependencySatisfactionEvidence:
    return _make_model(
        DependencySatisfactionEvidence,
        "satisfaction_SHA256",
        QUEUE_SATISFACTION_DIGEST_ALGORITHM,
        dependency_ticket_id=dependency_ticket_id,
        required_relationship=required_relationship,
        satisfaction_state=satisfaction_state,
        evidence_reference=evidence_reference,
        evidence_SHA256=evidence_SHA256,
    )


def build_canonical_p18_dependency_queue_request(
    *,
    approval_result: ApprovalWorkflowIntegrationResult,
    dependency_satisfaction_evidence: tuple[DependencySatisfactionEvidence, ...] = (),
    prior_queue_result_SHA256: str | None = None,
    prior_queue_decision: DependencyAwareQueueDecision | None = None,
) -> DependencyAwareQueueRequest:
    _validate_approved_handoff(approval_result)
    p18_2_result = approval_result.request.P18_2_result
    packet = p18_2_result.work_packet_compilation_result.work_packet
    request = _make_model(
        DependencyAwareQueueRequest,
        "queue_request_SHA256",
        QUEUE_REQUEST_DIGEST_ALGORITHM,
        approval_result=approval_result,
        P18_3_result_SHA256=approval_result.result_SHA256,
        approval_result_SHA256=approval_result.approval_result_SHA256,
        approval_decision_SHA256=approval_result.handoff.approval_decision_SHA256,
        TicketSpec_SHA256=packet.source_ticket_SHA256,
        WorkPacket_ID=packet.work_packet_id,
        WorkPacket_SHA256=packet.work_packet_SHA256,
        dependency_plan=p18_2_result.dependency_plan,
        dependency_plan_SHA256=p18_2_result.dependency_plan.plan_SHA256,
        workflow_snapshot=approval_result.resulting_workflow_snapshot,
        expected_current_state=GovernedWorkflowState.TICKET_APPROVED,
        dependency_satisfaction_evidence=dependency_satisfaction_evidence,
        prior_queue_result_SHA256=prior_queue_result_SHA256,
        prior_queue_decision=prior_queue_decision,
        requested_worker_dispatch=False,
        requested_command_execution=False,
        requested_provider_dispatch=False,
        requested_model_inference=False,
    )
    validate_dependency_aware_queue_request(request)
    return request


def validate_dependency_aware_queue_request(
    request: DependencyAwareQueueRequest,
) -> None:
    try:
        validated = DependencyAwareQueueRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise DependencyAwareQueueValidationError(
            "invalid dependency-aware queue request"
        ) from exc
    _validate_approved_handoff(validated.approval_result)
    _validate_request_bindings(validated)
    _validate_replay_policy(validated)
    _validate_dependency_satisfaction_evidence(validated)


def build_dependency_aware_queue_integration(
    request: DependencyAwareQueueRequest,
) -> DependencyAwareQueueIntegrationResult:
    validate_dependency_aware_queue_request(request)
    validated = DependencyAwareQueueRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    candidate = _build_queue_candidate(validated)
    blockers = _dependency_blockers(validated)
    dependencies_satisfied = not blockers and _plan_ready_for_ticket(
        validated.dependency_plan,
        _CANONICAL_TICKET_ID,
    )
    decision = (
        DependencyAwareQueueDecision.ADMIT
        if dependencies_satisfied
        else DependencyAwareQueueDecision.BLOCKED
    )
    work_packet_ready_transition = _build_work_packet_ready_transition(validated)
    final_transition = _build_queue_decision_transition(
        work_packet_ready_transition.resulting_snapshot,
        decision,
    )
    if not work_packet_ready_transition.accepted or not final_transition.accepted:
        raise DependencyAwareQueueStateError("P18.0 queue transition rejected")
    boundary = _build_queue_boundary()
    capability_assessments = _runtime_capability_assessments()
    findings = _derive_findings(
        decision=decision,
        candidate=candidate,
        dependency_plan=validated.dependency_plan,
        blockers=blockers,
        final_transition=final_transition,
    )
    summary = _derive_summary(
        findings=findings,
        decision=decision,
        dependencies_satisfied=dependencies_satisfied,
        final_transition=final_transition,
        blockers=blockers,
    )
    workflow_transition_results = (work_packet_ready_transition, final_transition)
    queue_result_SHA256 = _queue_result_core_digest(
        candidate=candidate,
        decision=decision,
        dependency_satisfaction_evidence=validated.dependency_satisfaction_evidence,
        dependency_blockers=blockers,
        boundary=boundary,
        workflow_transition_results=workflow_transition_results,
        summary=summary,
    )
    handoff = _build_p18_5_handoff(
        candidate=candidate,
        decision=decision,
        queue_result_SHA256=queue_result_SHA256,
        resulting_workflow_state=final_transition.resulting_snapshot.current_state,
    )
    queue_admitted = decision is DependencyAwareQueueDecision.ADMIT
    result_values = {
        "schema_version": DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION,
        "policy_id": DEPENDENCY_AWARE_QUEUE_POLICY_ID,
        "state": DependencyAwareQueueState.COMPLETED
        if queue_admitted
        else DependencyAwareQueueState.BLOCKED,
        "decision": decision,
        "request": validated,
        "queue_candidate": candidate,
        "runtime_capability_assessments": capability_assessments,
        "dependency_satisfaction_evidence": validated.dependency_satisfaction_evidence,
        "dependency_blockers": blockers,
        "queue_admission_boundary": boundary,
        "workflow_transition_results": workflow_transition_results,
        "resulting_workflow_snapshot": final_transition.resulting_snapshot,
        "findings": findings,
        "summary": summary,
        "handoff": handoff,
        "queue_result_SHA256": queue_result_SHA256,
        "approval_granted": True,
        "dependencies_satisfied": dependencies_satisfied,
        "queue_eligible": dependencies_satisfied,
        "queue_admitted": queue_admitted,
        "dispatch_eligible": False,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "execution_started": False,
        "WorkPacket_execution_started": False,
        "worker_dispatch_count": 0,
        "command_execution_count": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "claim_count": 0,
        "heartbeat_count": 0,
        "reclaim_count": 0,
        "workspace_allocation_count": 0,
        "validation_command_execution_count": 0,
        "retry_execution_count": 0,
        "automatic_requeue_count": 0,
        "rollback_count": 0,
        "staging_calls": 0,
        "commit_calls": 0,
        "push_calls": 0,
        "GBrain_calls": 0,
        "Paperclip_calls": 0,
        "P17_execution_substrate_reused": True,
        "P17_execution_invoked": False,
        "dispatcher_calls_in_P18_4": 0,
        "queue_order_deterministic": True,
        "arbitrary_random_ordering": False,
        "cycle_detection_reused": True,
        "duplicate_cycle_detector_created": False,
        "P18_5_ready": queue_admitted,
        "production_readiness_claimed": False,
    }
    result = _make_model(
        DependencyAwareQueueIntegrationResult,
        "result_SHA256",
        QUEUE_RESULT_DIGEST_ALGORITHM,
        integration_id=_integration_id_from_record(result_values),
        **result_values,
    )
    validate_dependency_aware_queue_integration_result(result)
    return result


def validate_dependency_aware_queue_integration_result(
    result: DependencyAwareQueueIntegrationResult,
) -> None:
    try:
        validated = DependencyAwareQueueIntegrationResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise DependencyAwareQueueValidationError(
            "invalid dependency-aware queue integration result"
        ) from exc
    validate_dependency_aware_queue_request(validated.request)
    _validate_result_bindings(validated)


def summarize_dependency_aware_queue_integration(
    result: DependencyAwareQueueIntegrationResult,
) -> DependencyAwareQueueSummary:
    validate_dependency_aware_queue_integration_result(result)
    return result.summary


def _validate_approved_handoff(result: ApprovalWorkflowIntegrationResult) -> None:
    try:
        validate_approval_workflow_integration_result(result)
    except ValueError as exc:
        raise DependencyAwareQueueValidationError("invalid P18.3 continuation") from exc
    handoff = result.handoff
    if result.state is not ApprovalWorkflowState.COMPLETED:
        raise DependencyAwareQueueStateError("P18.3 continuation must be completed")
    if result.decision is not ApprovalWorkflowResultDecision.APPROVED:
        raise DependencyAwareQueueStateError(
            "P18.4 accepts approved P18.3 handoffs only"
        )
    if result.authority.value != "human":
        raise DependencyAwareQueuePolicyError("approval authority must be human")
    if not result.approval_granted or not handoff.approval_granted:
        raise DependencyAwareQueuePolicyError("approval_granted must be true")
    if result.decision_input.decision is not HumanApprovalDecision.APPROVE:
        raise DependencyAwareQueuePolicyError("handoff decision must be approve")
    if not result.human_ticket_approval_present:
        raise DependencyAwareQueuePolicyError("human ticket approval must be present")
    if result.resulting_workflow_state is not GovernedWorkflowState.TICKET_APPROVED:
        raise DependencyAwareQueueStateError(
            "P18.3 workflow state must be ticket_approved"
        )
    if (
        result.resulting_workflow_snapshot.current_state
        is not GovernedWorkflowState.TICKET_APPROVED
    ):
        raise DependencyAwareQueueStateError("P18.3 snapshot must be ticket_approved")
    if handoff.workflow_state is not GovernedWorkflowState.TICKET_APPROVED:
        raise DependencyAwareQueueStateError("P18.4 handoff must bind ticket_approved")
    if not result.P18_4_ready or not handoff.P18_4_ready:
        raise DependencyAwareQueuePolicyError("P18.3 handoff must be P18.4-ready")
    if handoff.execution_started is not False:
        raise DependencyAwareQueuePolicyError("P18.3 handoff must not start execution")
    if any((
        result.ticket_execution_authorized,
        result.WorkPacket_execution_authorized,
        result.ticket_execution_started,
        result.WorkPacket_execution_started,
    )):
        raise DependencyAwareQueuePolicyError(
            "P18.3 result must not authorize execution"
        )


def _validate_request_bindings(request: DependencyAwareQueueRequest) -> None:
    result = request.approval_result
    handoff = result.handoff
    p18_2_result = result.request.P18_2_result
    packet = p18_2_result.work_packet_compilation_result.work_packet
    if request.P18_3_result_SHA256 != result.result_SHA256:
        raise DependencyAwareQueueIntegrityError("P18.3 result digest mismatch")
    if request.approval_result_SHA256 != result.approval_result_SHA256:
        raise DependencyAwareQueueIntegrityError("approval result digest mismatch")
    if request.approval_decision_SHA256 != handoff.approval_decision_SHA256:
        raise DependencyAwareQueueIntegrityError("approval decision digest mismatch")
    if request.TicketSpec_SHA256 != handoff.TicketSpec_SHA256:
        raise DependencyAwareQueueIntegrityError("handoff TicketSpec digest mismatch")
    if request.TicketSpec_SHA256 != packet.source_ticket_SHA256:
        raise DependencyAwareQueueIntegrityError(
            "WorkPacket source TicketSpec digest mismatch"
        )
    if request.WorkPacket_ID != handoff.WorkPacket_ID:
        raise DependencyAwareQueueIntegrityError("handoff WorkPacket ID mismatch")
    if request.WorkPacket_ID != packet.work_packet_id:
        raise DependencyAwareQueueIntegrityError("compiled WorkPacket ID mismatch")
    if request.WorkPacket_SHA256 != handoff.WorkPacket_SHA256:
        raise DependencyAwareQueueIntegrityError("handoff WorkPacket digest mismatch")
    if request.WorkPacket_SHA256 != packet.work_packet_SHA256:
        raise DependencyAwareQueueIntegrityError("compiled WorkPacket digest mismatch")
    if request.dependency_plan != p18_2_result.dependency_plan:
        raise DependencyAwareQueueIntegrityError("dependency plan object mismatch")
    if request.dependency_plan_SHA256 != p18_2_result.dependency_plan.plan_SHA256:
        raise DependencyAwareQueueIntegrityError("dependency plan digest mismatch")
    if (
        request.dependency_plan_SHA256
        != p18_2_result.work_packet_continuation.dependency_plan_SHA256
    ):
        raise DependencyAwareQueueIntegrityError(
            "WorkPacket continuation plan mismatch"
        )
    if (
        p18_2_result.work_packet_compilation_result.dependency_plan
        != request.dependency_plan
    ):
        raise DependencyAwareQueueIntegrityError("WorkPacket compilation plan mismatch")
    fresh = result.ticket_approval_record.fresh_planning_evidence
    if fresh is None:
        raise DependencyAwareQueueIntegrityError(
            "approved ticket lacks fresh planning evidence"
        )
    if fresh.dependency_plan != request.dependency_plan:
        raise DependencyAwareQueueIntegrityError("approval planning evidence mismatch")
    if request.workflow_snapshot != result.resulting_workflow_snapshot:
        raise DependencyAwareQueueIntegrityError("workflow snapshot mismatch")
    if request.workflow_snapshot.current_state is not request.expected_current_state:
        raise DependencyAwareQueueStateError("workflow snapshot state mismatch")
    if result.artifact_binding.project_id != _CANONICAL_PROJECT_ID:
        raise DependencyAwareQueueIntegrityError("project identity mismatch")
    if result.artifact_binding.macroproject_id != _CANONICAL_MACROPROJECT_ID:
        raise DependencyAwareQueueIntegrityError("macroproject identity mismatch")
    if result.artifact_binding.ticket_id != _CANONICAL_TICKET_ID:
        raise DependencyAwareQueueIntegrityError("ticket identity mismatch")


def _validate_replay_policy(request: DependencyAwareQueueRequest) -> None:
    prior_values = (request.prior_queue_result_SHA256, request.prior_queue_decision)
    if all(value is None for value in prior_values):
        return
    if any(value is None for value in prior_values):
        raise DependencyAwareQueuePolicyError(
            "prior queue replay evidence is incomplete"
        )
    raise DependencyAwareQueuePolicyError("queue admission replay is rejected")


def _validate_dependency_satisfaction_evidence(
    request: DependencyAwareQueueRequest,
) -> None:
    allowed_dependency_ids = _allowed_dependency_ids(request.dependency_plan)
    seen: set[str] = set()
    for evidence in request.dependency_satisfaction_evidence:
        if evidence.dependency_ticket_id in seen:
            raise DependencyAwareQueuePolicyError(
                "dependency evidence must not duplicate tickets"
            )
        seen.add(evidence.dependency_ticket_id)
        if evidence.dependency_ticket_id not in allowed_dependency_ids:
            raise DependencyAwareQueuePolicyError("unknown dependency evidence")
        if evidence.satisfaction_state is DependencySatisfactionState.MALFORMED:
            raise DependencyAwareQueuePolicyError("malformed dependency evidence")
        if evidence.satisfaction_state is DependencySatisfactionState.STALE:
            raise DependencyAwareQueuePolicyError("stale dependency evidence")


def _allowed_dependency_ids(plan: TicketDependencyPlan) -> frozenset[str]:
    ids = {_CANONICAL_PREREQUISITE_TICKET_ID}
    ids.update(edge.prerequisite_ticket_id for edge in plan.edges)
    ids.update(blocker.blocked_by_ticket_id for blocker in plan.blockers)
    ids.update(plan.unresolved_soft_external_dependency_ids)
    return frozenset(ids)


def _build_queue_candidate(
    request: DependencyAwareQueueRequest,
) -> DependencyAwareQueueCandidate:
    result = request.approval_result
    return _make_model(
        DependencyAwareQueueCandidate,
        "queue_candidate_SHA256",
        QUEUE_CANDIDATE_DIGEST_ALGORITHM,
        project_id=_CANONICAL_PROJECT_ID,
        macroproject_id=_CANONICAL_MACROPROJECT_ID,
        ticket_id=_CANONICAL_TICKET_ID,
        P18_3_result_SHA256=request.P18_3_result_SHA256,
        approval_result_SHA256=request.approval_result_SHA256,
        approval_decision_SHA256=request.approval_decision_SHA256,
        TicketSpec_SHA256=request.TicketSpec_SHA256,
        WorkPacket_ID=request.WorkPacket_ID,
        WorkPacket_SHA256=request.WorkPacket_SHA256,
        dependency_plan_SHA256=request.dependency_plan_SHA256,
        workflow_snapshot_SHA256=result.resulting_workflow_snapshot.workflow_SHA256,
        queue_candidate=True,
    )


def _plan_ready_for_ticket(plan: TicketDependencyPlan, ticket_id: str) -> bool:
    if ticket_id in plan.blocked_ticket_ids:
        return False
    return any(
        ticket_id in wave.ticket_ids
        and wave.disposition is WaveDisposition.DEPENDENCY_READY
        for wave in plan.waves
    )


def _dependency_blockers(
    request: DependencyAwareQueueRequest,
) -> tuple[DependencyQueueBlocker, ...]:
    blockers: list[DependencyQueueBlocker] = []
    for blocker in request.dependency_plan.blockers:
        blockers.append(
            _make_model(
                DependencyQueueBlocker,
                "blocker_SHA256",
                QUEUE_BLOCKER_DIGEST_ALGORITHM,
                dependency_ticket_id=blocker.blocked_by_ticket_id,
                required_relationship=blocker.kind.value,
                satisfaction_state=DependencySatisfactionState.UNSATISFIED,
                evidence_reference=blocker.rationale,
                evidence_SHA256=request.dependency_plan.plan_SHA256,
            )
        )
    for evidence in request.dependency_satisfaction_evidence:
        if evidence.satisfaction_state is not DependencySatisfactionState.SATISFIED:
            blockers.append(
                _make_model(
                    DependencyQueueBlocker,
                    "blocker_SHA256",
                    QUEUE_BLOCKER_DIGEST_ALGORITHM,
                    dependency_ticket_id=evidence.dependency_ticket_id,
                    required_relationship=evidence.required_relationship,
                    satisfaction_state=evidence.satisfaction_state,
                    evidence_reference=evidence.evidence_reference,
                    evidence_SHA256=evidence.evidence_SHA256,
                )
            )
    return tuple(blockers)


def _build_work_packet_ready_transition(
    request: DependencyAwareQueueRequest,
) -> GovernedWorkflowTransitionResult:
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=request.workflow_snapshot,
        trigger=WorkflowTransitionTrigger.WORK_PACKET_COMPILED,
        authority=WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        evidence_refs=("work_packet_compilation_result",),
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.WORK_PACKET,
            runtime_state="p17:work_packet_ready",
            task_id=None,
            board_or_queue_id=None,
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        ),
    )
    validate_governed_workflow_transition_request(transition_request)
    return build_governed_workflow_transition(transition_request)


def _build_queue_decision_transition(
    snapshot: GovernedWorkflowSnapshot,
    decision: DependencyAwareQueueDecision,
) -> GovernedWorkflowTransitionResult:
    admitted = decision is DependencyAwareQueueDecision.ADMIT
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=snapshot,
        trigger=WorkflowTransitionTrigger.DEPENDENCIES_READY
        if admitted
        else WorkflowTransitionTrigger.DEPENDENCIES_BLOCKED,
        authority=WorkflowTransitionAuthority.POLICY,
        evidence_refs=("dependency_plan_ready",)
        if admitted
        else ("dependency_blocker",),
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="todo" if admitted else "blocked",
            task_id=None,
            board_or_queue_id="P18-queue-contract",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=not admitted,
            retry_state_present=False,
            reclaim_state_present=False,
        ),
    )
    validate_governed_workflow_transition_request(transition_request)
    return build_governed_workflow_transition(transition_request)


def _build_queue_boundary() -> QueueAdmissionBoundary:
    return _make_model(
        QueueAdmissionBoundary,
        "boundary_SHA256",
        QUEUE_ADMISSION_BOUNDARY_DIGEST_ALGORITHM,
        queue_persistence_mechanism="result_envelope_only",
        provisional_runtime_authority="kanban_projection_deferred",
        canonical_long_term_authority="p20_paperclip_deferred",
        Kanban_SQLite_canonical=False,
        Paperclip_calls=0,
        GBrain_calls=0,
        existing_queue_projection_calls=0,
        does_not_dispatch=True,
        does_not_execute=True,
        duplicate_dependency_planner_created=False,
        duplicate_execution_queue_created=False,
        duplicate_scheduler_created=False,
        duplicate_dispatcher_created=False,
        duplicate_Kanban_backend_created=False,
        duplicate_WorkPacket_executor_created=False,
        duplicate_workflow_state_machine_created=False,
    )


def _runtime_capability_assessments() -> tuple[QueueRuntimeCapabilityAssessment, ...]:
    rows = (
        (
            "Ticket Factory dependency planner",
            "hermes_cli/agent_platform/ticket_factory/dependency_planning.py",
            "build_ticket_dependency_plan",
            "Deterministic dependency DAG and wave planning evidence.",
            "P16.3 accepted dependency planning contract.",
            True,
            QueueCapabilityDecision.RETAIN,
            "Consume the accepted P18.2 plan without recomputing a different plan.",
        ),
        (
            "Kanban task state",
            "hermes_cli/kanban_db.py",
            "recompute_ready",
            "Parent-gated ready state projection for runtime tasks.",
            "Existing provisional Kanban task lifecycle.",
            True,
            QueueCapabilityDecision.CUSTOMIZE,
            "Use as deferred projection only; do not mutate live task rows in P18.4.",
        ),
        (
            "Kanban dispatcher",
            "hermes_cli/kanban_db.py",
            "dispatch_once",
            "Consumes ready tasks and spawns assigned workers.",
            "Existing operational dispatcher mechanics.",
            False,
            QueueCapabilityDecision.DEFER,
            "Retain for later controlled runtime coupling; P18.4 calls it zero times.",
        ),
        (
            "Kanban heartbeat and reclaim",
            "hermes_cli/kanban_db.py",
            "heartbeat_claim/release_stale_claims",
            "Worker claim liveness and stale-claim recovery.",
            "Existing provisional runtime lifecycle mechanics.",
            False,
            QueueCapabilityDecision.DEFER,
            "No claim exists in P18.4, so heartbeat and reclaim remain unused.",
        ),
        (
            "P17 WorkPacket substrate",
            "hermes_cli/agent_platform/work_packet/__init__.py",
            "WorkPacketCompilationResult",
            "Compiled WorkPacket identity and downstream execution policy references.",
            "P17 accepted WorkPacket execution substrate.",
            True,
            QueueCapabilityDecision.RETAIN,
            "Bind identity and policy only; do not invoke execution machinery.",
        ),
        (
            "P18 governed workflow",
            "hermes_cli/agent_platform/workflow/governed_state_machine.py",
            "build_governed_workflow_transition",
            "Canonical non-executing workflow state transitions.",
            "P18.0 accepted workflow state machine.",
            True,
            QueueCapabilityDecision.CUSTOMIZE,
            "Reuse existing queue path and add only blocked-from-ready transition.",
        ),
    )
    return tuple(
        QueueRuntimeCapabilityAssessment(
            capability=capability,
            file=file,
            symbol=symbol,
            purpose=purpose,
            accepted_authority=authority,
            suitable_for_P18_4=suitable,
            decision=decision,
            customization_needed=customization,
            duplicate_created=False,
        )
        for (
            capability,
            file,
            symbol,
            purpose,
            authority,
            suitable,
            decision,
            customization,
        ) in rows
    )


def _build_finding(
    finding_id: str,
    code: DependencyAwareQueueFindingCode,
    subject_id: str,
    summary: str,
) -> DependencyAwareQueueFinding:
    return _make_model(
        DependencyAwareQueueFinding,
        "finding_SHA256",
        QUEUE_FINDING_DIGEST_ALGORITHM,
        finding_id=finding_id,
        severity=DependencyAwareQueueFindingSeverity.INFO,
        code=code,
        subject_id=subject_id,
        summary=summary,
        failed_invariant=None,
    )


def _derive_findings(
    *,
    decision: DependencyAwareQueueDecision,
    candidate: DependencyAwareQueueCandidate,
    dependency_plan: TicketDependencyPlan,
    blockers: tuple[DependencyQueueBlocker, ...],
    final_transition: GovernedWorkflowTransitionResult,
) -> tuple[DependencyAwareQueueFinding, ...]:
    decision_summary = (
        "All accepted dependency evidence is satisfied and queue admission is recorded."
        if decision is DependencyAwareQueueDecision.ADMIT
        else "Dependency blocker evidence is preserved without queue admission."
    )
    blocking_summary = (
        "No dependency blockers remain for the approved WorkPacket."
        if not blockers
        else "Dependency blockers prevent queue admission without changing approval evidence."
    )
    rows = (
        (
            DependencyAwareQueueFindingCode.P18_3_CONTINUATION_VALID,
            candidate.P18_3_result_SHA256,
            "Approved P18.3 handoff is complete, human-approved and execution-free.",
        ),
        (
            DependencyAwareQueueFindingCode.APPROVAL_BINDING_VALID,
            candidate.approval_decision_SHA256,
            "Approval decision, TicketSpec and WorkPacket digests remain bound.",
        ),
        (
            DependencyAwareQueueFindingCode.DEPENDENCY_PLANNER_REUSED,
            dependency_plan.plan_SHA256,
            "P16.3 dependency planning evidence is reused without semantic recomputation.",
        ),
        (
            DependencyAwareQueueFindingCode.DEPENDENCY_EVIDENCE_VALID,
            candidate.dependency_plan_SHA256,
            blocking_summary,
        ),
        (
            DependencyAwareQueueFindingCode.QUEUE_CANDIDATE_VALID,
            candidate.queue_candidate_SHA256,
            "The queue candidate binds the approved P18.2 artifact identity.",
        ),
        (
            DependencyAwareQueueFindingCode.QUEUE_DECISION_VALID,
            decision.value,
            decision_summary,
        ),
        (
            DependencyAwareQueueFindingCode.WORKFLOW_TRANSITION_VALID,
            final_transition.transition.transition_id,
            "P18.0 owns the queue or dependency-blocked workflow transition.",
        ),
        (
            DependencyAwareQueueFindingCode.DISPATCHER_BOUNDARY_PRESERVED,
            "dispatch_once",
            "Existing dispatcher is inspected and deferred; P18.4 calls it zero times.",
        ),
        (
            DependencyAwareQueueFindingCode.EXECUTION_AUTHORITY_PROHIBITED,
            candidate.WorkPacket_ID,
            "Queue evidence starts no worker, workspace, command, provider or model activity.",
        ),
        (
            DependencyAwareQueueFindingCode.P18_5_HANDOFF_READY,
            candidate.ticket_id,
            "P18.5 handoff readiness is true only for admitted queue candidates.",
        ),
        (
            DependencyAwareQueueFindingCode.DUPLICATE_RUNTIME_AVOIDED,
            "kanban-and-p17",
            "No duplicate planner, queue, dispatcher, store, executor or workflow engine is created.",
        ),
        (
            DependencyAwareQueueFindingCode.INTEGRATION_ACCEPTED,
            candidate.ticket_id,
            "P18.4 dependency-aware queue integration is accepted with zero runtime execution.",
        ),
    )
    return tuple(
        _build_finding(f"DQIF-{index:03d}", code, subject_id, summary)
        for index, (code, subject_id, summary) in enumerate(rows, start=1)
    )


def _derive_summary(
    *,
    findings: tuple[DependencyAwareQueueFinding, ...],
    decision: DependencyAwareQueueDecision,
    dependencies_satisfied: bool,
    final_transition: GovernedWorkflowTransitionResult,
    blockers: tuple[DependencyQueueBlocker, ...],
) -> DependencyAwareQueueSummary:
    information = sum(
        item.severity is DependencyAwareQueueFindingSeverity.INFO for item in findings
    )
    warnings = sum(
        item.severity is DependencyAwareQueueFindingSeverity.WARNING
        for item in findings
    )
    blocking = sum(
        item.severity is DependencyAwareQueueFindingSeverity.BLOCKING
        for item in findings
    )
    transition_valid = final_transition.accepted and (
        (
            decision is DependencyAwareQueueDecision.ADMIT
            and final_transition.transition.transition_id == "GWT-005"
            and final_transition.resulting_snapshot.current_state
            is GovernedWorkflowState.QUEUED
        )
        or (
            decision is DependencyAwareQueueDecision.BLOCKED
            and final_transition.transition.transition_id == "GWT-026"
            and final_transition.resulting_snapshot.current_state
            is GovernedWorkflowState.BLOCKED
        )
    )
    return _make_model(
        DependencyAwareQueueSummary,
        "summary_SHA256",
        QUEUE_SUMMARY_DIGEST_ALGORITHM,
        P18_3_continuation_valid=True,
        project_identity_valid=True,
        approval_binding_valid=True,
        dependency_plan_valid=True,
        dependency_planner_reused=True,
        dependency_plan_recomputed_unnecessarily=False,
        dependency_evidence_valid=True,
        queue_candidate_valid=True,
        queue_decision_valid=True,
        queue_admission_valid=decision is DependencyAwareQueueDecision.ADMIT,
        dependency_blocking_valid=(bool(blockers) != dependencies_satisfied),
        workflow_transition_valid=transition_valid,
        dispatcher_boundary_valid=True,
        execution_prohibition_valid=True,
        replay_policy_valid=True,
        P18_5_handoff_valid=decision is DependencyAwareQueueDecision.ADMIT,
        information_finding_count=information,
        warning_finding_count=warnings,
        blocking_finding_count=blocking,
    )


def _build_p18_5_handoff(
    *,
    candidate: DependencyAwareQueueCandidate,
    decision: DependencyAwareQueueDecision,
    queue_result_SHA256: str,
    resulting_workflow_state: GovernedWorkflowState,
) -> DependencyAwareQueueP18_5Handoff:
    return _make_model(
        DependencyAwareQueueP18_5Handoff,
        "handoff_SHA256",
        QUEUE_HANDOFF_DIGEST_ALGORITHM,
        project_id=candidate.project_id,
        macroproject_id=candidate.macroproject_id,
        ticket_id=candidate.ticket_id,
        TicketSpec_SHA256=candidate.TicketSpec_SHA256,
        WorkPacket_ID=candidate.WorkPacket_ID,
        WorkPacket_SHA256=candidate.WorkPacket_SHA256,
        approval_decision_SHA256=candidate.approval_decision_SHA256,
        queue_decision=decision,
        queue_result_SHA256=queue_result_SHA256,
        dependency_plan_SHA256=candidate.dependency_plan_SHA256,
        resulting_workflow_state=resulting_workflow_state,
        execution_started=False,
        P18_5_ready=decision is DependencyAwareQueueDecision.ADMIT,
    )


def _queue_result_core_digest(
    *,
    candidate: DependencyAwareQueueCandidate,
    decision: DependencyAwareQueueDecision,
    dependency_satisfaction_evidence: tuple[DependencySatisfactionEvidence, ...],
    dependency_blockers: tuple[DependencyQueueBlocker, ...],
    boundary: QueueAdmissionBoundary,
    workflow_transition_results: tuple[GovernedWorkflowTransitionResult, ...],
    summary: DependencyAwareQueueSummary,
) -> str:
    return _digest_from_record(
        QUEUE_RESULT_CORE_DIGEST_ALGORITHM,
        {
            "candidate": candidate,
            "decision": decision,
            "dependency_satisfaction_evidence": dependency_satisfaction_evidence,
            "dependency_blockers": dependency_blockers,
            "boundary": boundary,
            "workflow_transition_results": workflow_transition_results,
            "summary": summary,
        },
    )


def _queue_result_core_digest_from_result(
    result: DependencyAwareQueueIntegrationResult,
) -> str:
    return _queue_result_core_digest(
        candidate=result.queue_candidate,
        decision=result.decision,
        dependency_satisfaction_evidence=result.dependency_satisfaction_evidence,
        dependency_blockers=result.dependency_blockers,
        boundary=result.queue_admission_boundary,
        workflow_transition_results=result.workflow_transition_results,
        summary=result.summary,
    )


def _integration_id_from_record(record: object) -> str:
    digest = _digest_from_record(QUEUE_INTEGRATION_ID_DIGEST_ALGORITHM, record)
    return f"DQI-P18-{digest[:12]}"


def _validate_result_bindings(result: DependencyAwareQueueIntegrationResult) -> None:
    request = result.request
    if result.queue_candidate.P18_3_result_SHA256 != request.P18_3_result_SHA256:
        raise DependencyAwareQueueIntegrityError("candidate P18.3 digest mismatch")
    if result.queue_candidate.dependency_plan_SHA256 != request.dependency_plan_SHA256:
        raise DependencyAwareQueueIntegrityError("candidate dependency plan mismatch")
    if (
        result.resulting_workflow_snapshot
        != result.workflow_transition_results[-1].resulting_snapshot
    ):
        raise DependencyAwareQueueIntegrityError("resulting workflow snapshot mismatch")
    if result.handoff.queue_decision is not result.decision:
        raise DependencyAwareQueueIntegrityError("handoff decision mismatch")
    if any((
        result.dispatch_eligible,
        result.ticket_execution_authorized,
        result.WorkPacket_execution_authorized,
        result.execution_started,
        result.WorkPacket_execution_started,
        result.production_readiness_claimed,
    )):
        raise DependencyAwareQueuePolicyError(
            "queue result must not authorize execution"
        )


__all__ = (
    "DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION",
    "DEPENDENCY_AWARE_QUEUE_POLICY_ID",
    "QueueCapabilityDecision",
    "DependencySatisfactionState",
    "DependencyAwareQueueDecision",
    "DependencyAwareQueueState",
    "DependencyAwareQueueFindingSeverity",
    "DependencyAwareQueueFindingCode",
    "QueueRuntimeCapabilityAssessment",
    "DependencySatisfactionEvidence",
    "DependencyAwareQueueRequest",
    "DependencyAwareQueueCandidate",
    "DependencyQueueBlocker",
    "QueueAdmissionBoundary",
    "DependencyAwareQueueFinding",
    "DependencyAwareQueueSummary",
    "DependencyAwareQueueP18_5Handoff",
    "DependencyAwareQueueIntegrationResult",
    "DependencyAwareQueueIntegrationError",
    "DependencyAwareQueueInputError",
    "DependencyAwareQueueIntegrityError",
    "DependencyAwareQueuePolicyError",
    "DependencyAwareQueueStateError",
    "DependencyAwareQueueValidationError",
    "build_dependency_satisfaction_evidence",
    "build_canonical_p18_dependency_queue_request",
    "validate_dependency_aware_queue_request",
    "build_dependency_aware_queue_integration",
    "validate_dependency_aware_queue_integration_result",
    "summarize_dependency_aware_queue_integration",
)
