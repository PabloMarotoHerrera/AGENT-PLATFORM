"""P18.6 retry, incident and rollback workflow for Pepper.

This module consumes P18.5 non-accept review handoff evidence and records a
bounded recovery decision. It is a governance projection only: it does not
execute retries, requeue Kanban tasks, reclaim claims, restore workspaces,
mutate Git, run validation commands, call providers/models, run Docker, run
Graphify, write G-Brain memory, operate Paperclip or persist runtime state.
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

from hermes_cli.agent_platform.workflow.governed_state_machine import (
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
from hermes_cli.agent_platform.workflow.review_validation_loop import (
    ReviewValidationLoopDecision,
    ReviewValidationLoopIntegrationResult,
    ReviewValidationP18_6Handoff,
    validate_review_validation_loop_integration_result,
)


RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION = 1
RETRY_INCIDENT_ROLLBACK_POLICY_ID = "pepper-retry-incident-rollback-workflow-v1"
RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION = "RECOVERY_DECISION_ONLY"

RETRY_INCIDENT_ROLLBACK_REQUEST_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-request-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-authorization-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_CAPABILITY_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-capability-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_ATTEMPT_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-attempt-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_INCIDENT_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-incident-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_ROLLBACK_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-rollback-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_FINDING_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-finding-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-summary-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-result-sha256-v1"
)
RETRY_INCIDENT_ROLLBACK_ID_DIGEST_ALGORITHM = (
    "agent-platform-retry-incident-rollback-id-sha256-v1"
)

_CANONICAL_PROJECT_ID = "PEPPER"
_CANONICAL_MACROPROJECT_ID = "P18"
_CANONICAL_TICKET_ID = "P18.2"
_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_AUTHORIZATION_ID_PATTERN = r"^RIR-AUTH-[a-f0-9]{12}$"
_RECOVERY_ID_PATTERN = r"^RIR-P18-6-[a-f0-9]{12}$"
_PLAN_ID_PATTERN = r"^RIR-(?:RETRY|ROLLBACK)-[a-f0-9]{12}$"
_INCIDENT_ID_PATTERN = r"^RIR-INC-[a-f0-9]{12}$"
_FINDING_ID_PATTERN = r"^RIRF-[0-9]{3}$"
_WORK_PACKET_ID_PATTERN = r"^WP-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$"
_CONTROL_OR_ANSI_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x1b]")
_PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)")
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
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
    "raw diff",
    "diff --git",
    "source snapshot",
    "raw conversation",
    "chatgpt transcript",
    "opencode transcript",
    "runtime handle",
    "git handle",
)

DigestText = Annotated[str, Field(pattern=_DIGEST_PATTERN)]
AuthorizationIdentifier = Annotated[str, Field(pattern=_AUTHORIZATION_ID_PATTERN)]
RecoveryIdentifier = Annotated[str, Field(pattern=_RECOVERY_ID_PATTERN)]
PlanIdentifier = Annotated[str, Field(pattern=_PLAN_ID_PATTERN)]
IncidentIdentifier = Annotated[str, Field(pattern=_INCIDENT_ID_PATTERN)]
FindingIdentifier = Annotated[str, Field(pattern=_FINDING_ID_PATTERN)]
WorkPacketIdentifier = Annotated[str, Field(pattern=_WORK_PACKET_ID_PATTERN)]
BoundedText = Annotated[str, Field(min_length=1, max_length=1024)]


class RetryIncidentRollbackError(ValueError):
    """Base error for P18.6 retry/incident/rollback integration failures."""


class RetryIncidentRollbackInputError(RetryIncidentRollbackError):
    """Raised when P18.6 caller input is malformed."""


class RetryIncidentRollbackIntegrityError(RetryIncidentRollbackError):
    """Raised when P18.6 artifact bindings or digests mismatch."""


class RetryIncidentRollbackPolicyError(RetryIncidentRollbackError):
    """Raised when P18.6 recovery policy boundaries are violated."""


class RetryIncidentRollbackStateError(RetryIncidentRollbackError):
    """Raised when P18.6 source workflow state cannot accept recovery routing."""


class RetryIncidentRollbackValidationError(RetryIncidentRollbackError):
    """Raised when immutable P18.6 evidence fails validation."""


class RetryIncidentRollbackBoundary(str, Enum):
    RECOVERY_DECISION_ONLY = "RECOVERY_DECISION_ONLY"
    OTHER_WITH_EVIDENCE = "OTHER_WITH_EVIDENCE"


class RetryIncidentRollbackCapabilityDecision(str, Enum):
    RETAIN = "retain"
    CUSTOMIZE = "customize"
    DEFER = "defer"
    NOT_APPLICABLE = "not_applicable"


class RetryIncidentRollbackRequestedAction(str, Enum):
    NONE = "none"
    AUTHORIZE_RETRY = "authorize_retry"
    AUTHORIZE_ROLLBACK = "authorize_rollback"


class RetryIncidentRollbackDecision(str, Enum):
    AWAIT_HUMAN_CORRECTION = "await_human_correction"
    RECORD_INCIDENT = "record_incident"
    RETRY_PENDING = "retry_pending"
    ROLLBACK_REQUIRED = "rollback_required"
    CANCELLED = "cancelled"


class RetryIncidentRollbackState(str, Enum):
    CORRECTION_REQUIRED = "correction_required"
    INCIDENT_RECORDED = "incident_recorded"
    RETRY_PENDING = "retry_pending"
    ROLLBACK_REQUIRED = "rollback_required"
    CANCELLED = "cancelled"


class RetryIncidentRollbackFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class RetryIncidentRollbackFindingCode(str, Enum):
    P18_5_HANDOFF_VALID = "p18_5_handoff_valid"
    RECOVERY_DECISION_VALID = "recovery_decision_valid"
    RETRY_ATTEMPT_TRACKING_VALID = "retry_attempt_tracking_valid"
    INCIDENT_RECORD_VALID = "incident_record_valid"
    ROLLBACK_GOVERNANCE_VALID = "rollback_governance_valid"
    WORKFLOW_TRANSITION_VALID = "workflow_transition_valid"
    KANBAN_MUTATION_DEFERRED = "kanban_mutation_deferred"
    WORKSPACE_RESTORATION_DEFERRED = "workspace_restoration_deferred"
    HUMAN_AUTHORITY_PRESERVED = "human_authority_preserved"
    NO_AUTONOMOUS_RETRY_VALID = "no_autonomous_retry_valid"
    NO_AUTONOMOUS_ROLLBACK_VALID = "no_autonomous_rollback_valid"
    SECURITY_BOUNDARY_VALID = "security_boundary_valid"


class _RetryIncidentRollbackModel(BaseModel):
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
        raise ValueError(f"{label} contains credential-shaped text")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-shaped text")
    if any(marker in lowered for marker in _RAW_CONTEXT_MARKERS):
        raise ValueError(f"{label} contains raw context")
    if _PERSONAL_PATH_PATTERN.search(value):
        raise ValueError(f"{label} contains personal absolute path")
    return value


def _digest_payload(value: object) -> object:
    if isinstance(value, BaseModel):
        return _digest_payload(value.model_dump(mode="python", warnings=False))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_digest_payload(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _digest_payload(item) for key, item in value.items()}
    return value


def _digest_from_record(algorithm: str, record: object) -> str:
    encoded = json.dumps(
        {"algorithm": algorithm, "payload": _digest_payload(record)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _model_digest(algorithm: str, value: BaseModel, digest_field: str) -> str:
    return _digest_from_record(
        algorithm,
        value.model_dump(mode="python", exclude={digest_field}, warnings=False),
    )


def _make_model(
    model_type: type[_RetryIncidentRollbackModel],
    digest_field: str,
    algorithm: str,
    **data: object,
) -> _RetryIncidentRollbackModel:
    provisional = model_type.model_construct(**data, **{digest_field: "0" * 64})
    return model_type(
        **data,
        **{digest_field: _model_digest(algorithm, provisional, digest_field)},
    )


class RetryIncidentRollbackHumanAuthorization(_RetryIncidentRollbackModel):
    authorization_id: AuthorizationIdentifier
    action: Literal[
        RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
        RetryIncidentRollbackRequestedAction.AUTHORIZE_ROLLBACK,
    ]
    authorizer_id: BoundedText
    authorization_reference: BoundedText
    rationale: BoundedText
    authorized_at: BoundedText
    authorization_SHA256: DigestText

    @field_validator(
        "authorizer_id",
        "authorization_reference",
        "rationale",
        "authorized_at",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.6 human authorization")

    @model_validator(mode="after")
    def _validate_authorization(self) -> RetryIncidentRollbackHumanAuthorization:
        if self.authorization_id != _authorization_id(self):
            raise ValueError("P18.6 authorization ID mismatch")
        if self.authorization_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_AUTHORIZATION_DIGEST_ALGORITHM,
            self,
            "authorization_SHA256",
        ):
            raise ValueError("P18.6 authorization digest mismatch")
        return self


class RetryIncidentRollbackCapabilityReuseAssessment(_RetryIncidentRollbackModel):
    capability: BoundedText
    source_file: BoundedText
    symbol: BoundedText
    purpose: BoundedText
    current_authority: BoundedText
    suitable_for_P18_6: StrictBool
    decision: RetryIncidentRollbackCapabilityDecision
    customized: StrictBool
    duplicate_created: StrictBool
    invoked_by_P18_6: StrictBool
    reason: BoundedText
    assessment_SHA256: DigestText

    @field_validator(
        "capability",
        "source_file",
        "symbol",
        "purpose",
        "current_authority",
        "reason",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.6 capability reuse assessment")

    @model_validator(mode="after")
    def _validate_assessment(self) -> RetryIncidentRollbackCapabilityReuseAssessment:
        if self.duplicate_created:
            raise ValueError("P18.6 must not create duplicate recovery runtime")
        if self.decision is RetryIncidentRollbackCapabilityDecision.RETAIN:
            if self.customized:
                raise ValueError("retained capability cannot be customized")
        elif self.decision is RetryIncidentRollbackCapabilityDecision.DEFER:
            if self.invoked_by_P18_6:
                raise ValueError("deferred capability cannot be invoked by P18.6")
        if self.assessment_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_CAPABILITY_DIGEST_ALGORITHM,
            self,
            "assessment_SHA256",
        ):
            raise ValueError("P18.6 capability assessment digest mismatch")
        return self


class RetryIncidentRollbackRequest(_RetryIncidentRollbackModel):
    schema_version: Literal[1] = RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION
    policy_id: Literal["pepper-retry-incident-rollback-workflow-v1"] = (
        RETRY_INCIDENT_ROLLBACK_POLICY_ID
    )
    runtime_boundary_classification: Literal[
        RetryIncidentRollbackBoundary.RECOVERY_DECISION_ONLY
    ] = RetryIncidentRollbackBoundary.RECOVERY_DECISION_ONLY
    P18_5_result: ReviewValidationLoopIntegrationResult
    P18_5_result_SHA256: DigestText
    P18_6_handoff: ReviewValidationP18_6Handoff
    P18_6_handoff_SHA256: DigestText
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    expected_workflow_state: GovernedWorkflowState
    requested_action: RetryIncidentRollbackRequestedAction = (
        RetryIncidentRollbackRequestedAction.NONE
    )
    human_authorization: RetryIncidentRollbackHumanAuthorization | None = None
    observed_attempt_count: int = Field(default=1, ge=1, le=100, strict=True)
    max_attempts: int = Field(default=2, ge=1, le=100, strict=True)
    prior_recovery_result_SHA256: DigestText | None = None
    request_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_request(self) -> RetryIncidentRollbackRequest:
        if self.request_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_REQUEST_DIGEST_ALGORITHM,
            self,
            "request_SHA256",
        ):
            raise ValueError("P18.6 request digest mismatch")
        if self.human_authorization is None:
            if self.requested_action is not RetryIncidentRollbackRequestedAction.NONE:
                raise ValueError("human authorization is required for recovery action")
        elif self.human_authorization.action is not self.requested_action:
            raise ValueError("human authorization action mismatch")
        return self


class RetryAttemptPlan(_RetryIncidentRollbackModel):
    attempt_plan_id: PlanIdentifier
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    observed_attempt_count: int = Field(ge=1, le=100, strict=True)
    max_attempts: int = Field(ge=1, le=100, strict=True)
    retry_budget_exhausted: StrictBool
    retry_requested_by_human: StrictBool
    retry_authorized_for_governed_state: StrictBool
    next_attempt_number: int | None = Field(default=None, ge=2, le=101)
    retry_execution_started: Literal[False] = False
    automatic_retry_authorized: Literal[False] = False
    automatic_requeue_authorized: Literal[False] = False
    Kanban_requeue_authorized: Literal[False] = False
    attempt_plan_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_plan(self) -> RetryAttemptPlan:
        exhausted = self.observed_attempt_count >= self.max_attempts
        if self.retry_budget_exhausted != exhausted:
            raise ValueError("retry budget flag must derive from attempt counts")
        expected_next = (
            self.observed_attempt_count + 1
            if self.retry_authorized_for_governed_state and not exhausted
            else None
        )
        if self.next_attempt_number != expected_next:
            raise ValueError("next attempt number must derive from retry authorization")
        if (
            self.retry_authorized_for_governed_state
            and not self.retry_requested_by_human
        ):
            raise ValueError("governed retry requires human request")
        if self.attempt_plan_id != _plan_id("RETRY", self):
            raise ValueError("retry attempt plan ID mismatch")
        if self.attempt_plan_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_ATTEMPT_DIGEST_ALGORITHM,
            self,
            "attempt_plan_SHA256",
        ):
            raise ValueError("retry attempt plan digest mismatch")
        return self


class RetryIncidentRecord(_RetryIncidentRollbackModel):
    incident_id: IncidentIdentifier
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    source_review_decision: Literal[ReviewValidationLoopDecision.INCIDENT]
    source_workflow_state: Literal[GovernedWorkflowState.FAILED]
    execution_outcome_SHA256: DigestText
    failure_category: BoundedText
    blocker_codes: tuple[BoundedText, ...] = Field(min_length=1, max_length=32)
    incident_open: Literal[True] = True
    human_triage_required: Literal[True] = True
    automatic_retry_authorized: Literal[False] = False
    automatic_rollback_authorized: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    incident_SHA256: DigestText

    @field_validator("failure_category", mode="after")
    @classmethod
    def _validate_failure_category(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.6 incident record")

    @field_validator("blocker_codes", mode="after")
    @classmethod
    def _validate_blockers(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("incident blocker codes must be unique")
        for item in value:
            _validate_safe_text(item, "P18.6 incident blocker code")
        return value

    @model_validator(mode="after")
    def _validate_record(self) -> RetryIncidentRecord:
        if self.incident_id != _incident_id(self):
            raise ValueError("incident ID mismatch")
        if self.incident_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_INCIDENT_DIGEST_ALGORITHM,
            self,
            "incident_SHA256",
        ):
            raise ValueError("incident digest mismatch")
        return self


class RollbackGovernancePlan(_RetryIncidentRollbackModel):
    rollback_plan_id: PlanIdentifier
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    rollback_requested_by_human: StrictBool
    rollback_required_for_governed_state: StrictBool
    rollback_target: BoundedText
    human_git_handoff_required: StrictBool
    rollback_execution_started: Literal[False] = False
    automatic_rollback_authorized: Literal[False] = False
    Git_rollback_authorized: Literal[False] = False
    workspace_restore_authorized: Literal[False] = False
    rollback_plan_SHA256: DigestText

    @field_validator("rollback_target", mode="after")
    @classmethod
    def _validate_target(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.6 rollback plan")

    @model_validator(mode="after")
    def _validate_plan(self) -> RollbackGovernancePlan:
        if (
            self.rollback_required_for_governed_state
            and not self.rollback_requested_by_human
        ):
            raise ValueError("governed rollback requires human request")
        if self.human_git_handoff_required != self.rollback_required_for_governed_state:
            raise ValueError("human Git rollback handoff derives from rollback state")
        if self.rollback_plan_id != _plan_id("ROLLBACK", self):
            raise ValueError("rollback plan ID mismatch")
        if self.rollback_plan_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_ROLLBACK_DIGEST_ALGORITHM,
            self,
            "rollback_plan_SHA256",
        ):
            raise ValueError("rollback plan digest mismatch")
        return self


class RetryIncidentRollbackFinding(_RetryIncidentRollbackModel):
    finding_id: FindingIdentifier
    severity: RetryIncidentRollbackFindingSeverity
    code: RetryIncidentRollbackFindingCode
    message: BoundedText
    evidence_SHA256: DigestText | None = None
    finding_SHA256: DigestText

    @field_validator("message", mode="after")
    @classmethod
    def _validate_message(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.6 finding")

    @model_validator(mode="after")
    def _validate_finding(self) -> RetryIncidentRollbackFinding:
        if self.finding_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_FINDING_DIGEST_ALGORITHM,
            self,
            "finding_SHA256",
        ):
            raise ValueError("P18.6 finding digest mismatch")
        return self


class RetryIncidentRollbackSummary(_RetryIncidentRollbackModel):
    P18_5_handoff_valid: StrictBool
    source_non_accept_valid: StrictBool
    recovery_decision_valid: StrictBool
    retry_attempt_tracking_valid: StrictBool
    incident_classification_valid: StrictBool
    rollback_governance_valid: StrictBool
    workflow_transition_valid: StrictBool
    Kanban_runtime_mutation_deferred: StrictBool
    task_requeue_reclaim_deferred: StrictBool
    workspace_restoration_deferred: StrictBool
    human_Git_handoff_boundary_valid: StrictBool
    no_autonomous_retry_valid: StrictBool
    no_autonomous_rollback_valid: StrictBool
    no_runtime_mutation_valid: StrictBool
    security_valid: StrictBool
    information_finding_count: int = Field(ge=0, strict=True)
    warning_finding_count: int = Field(ge=0, strict=True)
    blocking_finding_count: int = Field(ge=0, strict=True)
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> RetryIncidentRollbackSummary:
        if self.warning_finding_count or self.blocking_finding_count:
            raise ValueError("P18.6 findings must not warn or block")
        required = all((
            self.P18_5_handoff_valid,
            self.source_non_accept_valid,
            self.recovery_decision_valid,
            self.retry_attempt_tracking_valid,
            self.incident_classification_valid,
            self.rollback_governance_valid,
            self.workflow_transition_valid,
            self.Kanban_runtime_mutation_deferred,
            self.task_requeue_reclaim_deferred,
            self.workspace_restoration_deferred,
            self.human_Git_handoff_boundary_valid,
            self.no_autonomous_retry_valid,
            self.no_autonomous_rollback_valid,
            self.no_runtime_mutation_valid,
            self.security_valid,
        ))
        if not required:
            raise ValueError("P18.6 summary validity booleans must all be true")
        if self.summary_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_SUMMARY_DIGEST_ALGORITHM,
            self,
            "summary_SHA256",
        ):
            raise ValueError("P18.6 summary digest mismatch")
        return self


class RetryIncidentRollbackResult(_RetryIncidentRollbackModel):
    schema_version: Literal[1] = RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION
    policy_id: Literal["pepper-retry-incident-rollback-workflow-v1"] = (
        RETRY_INCIDENT_ROLLBACK_POLICY_ID
    )
    recovery_id: RecoveryIdentifier
    state: RetryIncidentRollbackState
    decision: RetryIncidentRollbackDecision
    request: RetryIncidentRollbackRequest
    capability_reuse_assessments: tuple[
        RetryIncidentRollbackCapabilityReuseAssessment, ...
    ] = Field(min_length=10, max_length=16)
    retry_attempt_plan: RetryAttemptPlan
    incident_record: RetryIncidentRecord | None = None
    rollback_plan: RollbackGovernancePlan
    workflow_transition_results: tuple[GovernedWorkflowTransitionResult, ...] = Field(
        max_length=1
    )
    resulting_workflow_snapshot: GovernedWorkflowSnapshot
    findings: tuple[RetryIncidentRollbackFinding, ...]
    summary: RetryIncidentRollbackSummary
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    P18_5_result_SHA256: DigestText
    P18_6_handoff_SHA256: DigestText
    source_review_decision: ReviewValidationLoopDecision
    source_workflow_state: GovernedWorkflowState
    requested_action: RetryIncidentRollbackRequestedAction
    human_authorization_SHA256: DigestText | None = None
    retry_authorized_by_human: StrictBool
    rollback_authorized_by_human: StrictBool
    retry_budget_exhausted: StrictBool
    Git_commands_executed: Literal[0]
    Git_staging_performed: Literal[False]
    Git_commit_performed: Literal[False]
    Git_push_performed: Literal[False]
    staging_calls: Literal[0]
    commit_calls: Literal[0]
    push_calls: Literal[0]
    retry_execution_count: Literal[0]
    automatic_retry_count: Literal[0]
    automatic_requeue_count: Literal[0]
    Kanban_requeue_calls: Literal[0]
    Kanban_reclaim_calls: Literal[0]
    Kanban_reassign_calls: Literal[0]
    rollback_execution_count: Literal[0]
    workspace_allocation_calls_in_P18_6: Literal[0]
    workspace_cleanup_calls_in_P18_6: Literal[0]
    workspace_restore_calls_in_P18_6: Literal[0]
    provider_dispatch_count: Literal[0]
    model_inference_count: Literal[0]
    Docker_commands_executed: Literal[0]
    Graphify_commands_executed: Literal[0]
    GBrain_calls: Literal[0]
    Paperclip_calls: Literal[0]
    Kanban_SQLite_canonical_authority: Literal[False]
    duplicate_retry_controller_created: Literal[False]
    duplicate_requeue_controller_created: Literal[False]
    duplicate_incident_store_created: Literal[False]
    duplicate_rollback_controller_created: Literal[False]
    duplicate_workspace_restorer_created: Literal[False]
    duplicate_Git_handoff_created: Literal[False]
    duplicate_workflow_state_machine_created: Literal[False]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> RetryIncidentRollbackResult:
        if self.result_SHA256 != _model_digest(
            RETRY_INCIDENT_ROLLBACK_RESULT_DIGEST_ALGORITHM,
            self,
            "result_SHA256",
        ):
            raise ValueError("P18.6 result digest mismatch")
        if self.recovery_id != _recovery_id(self):
            raise ValueError("P18.6 recovery ID mismatch")
        if self.workflow_transition_results:
            if self.resulting_workflow_snapshot != (
                self.workflow_transition_results[-1].resulting_snapshot
            ):
                raise ValueError("resulting workflow snapshot mismatch")
        elif (
            self.resulting_workflow_snapshot
            != self.request.P18_5_result.resulting_workflow_snapshot
        ):
            raise ValueError("unchanged workflow snapshot must derive from P18.5")
        if self.retry_authorized_by_human != (
            self.requested_action
            is RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY
        ):
            raise ValueError("retry authorization flag mismatch")
        if self.rollback_authorized_by_human != (
            self.requested_action
            is RetryIncidentRollbackRequestedAction.AUTHORIZE_ROLLBACK
        ):
            raise ValueError("rollback authorization flag mismatch")
        if (
            self.retry_budget_exhausted
            != self.retry_attempt_plan.retry_budget_exhausted
        ):
            raise ValueError("retry budget exhaustion mismatch")
        if self.rollback_plan.rollback_required_for_governed_state != (
            self.decision is RetryIncidentRollbackDecision.ROLLBACK_REQUIRED
        ):
            raise ValueError("rollback decision mismatch")
        if self.source_review_decision is ReviewValidationLoopDecision.INCIDENT:
            if self.incident_record is None:
                raise ValueError("incident source requires incident record")
        elif self.incident_record is not None:
            raise ValueError("non-incident source cannot carry incident record")
        if self.human_authorization_SHA256 != (
            self.request.human_authorization.authorization_SHA256
            if self.request.human_authorization is not None
            else None
        ):
            raise ValueError("human authorization digest mismatch")
        if any((
            self.Git_commands_executed,
            self.staging_calls,
            self.commit_calls,
            self.push_calls,
            self.retry_execution_count,
            self.automatic_retry_count,
            self.automatic_requeue_count,
            self.Kanban_requeue_calls,
            self.Kanban_reclaim_calls,
            self.Kanban_reassign_calls,
            self.rollback_execution_count,
            self.workspace_allocation_calls_in_P18_6,
            self.workspace_cleanup_calls_in_P18_6,
            self.workspace_restore_calls_in_P18_6,
            self.provider_dispatch_count,
            self.model_inference_count,
            self.Docker_commands_executed,
            self.Graphify_commands_executed,
            self.GBrain_calls,
            self.Paperclip_calls,
        )):
            raise ValueError("P18.6 result must not execute runtime actions")
        return self


def build_retry_incident_rollback_human_authorization(
    *,
    action: RetryIncidentRollbackRequestedAction,
    authorizer_id: str,
    authorization_reference: str,
    rationale: str,
    authorized_at: str,
) -> RetryIncidentRollbackHumanAuthorization:
    if action is RetryIncidentRollbackRequestedAction.NONE:
        raise RetryIncidentRollbackInputError("authorization action cannot be none")
    data = {
        "action": action,
        "authorizer_id": authorizer_id,
        "authorization_reference": authorization_reference,
        "rationale": rationale,
        "authorized_at": authorized_at,
    }
    return _make_model(
        RetryIncidentRollbackHumanAuthorization,
        "authorization_SHA256",
        RETRY_INCIDENT_ROLLBACK_AUTHORIZATION_DIGEST_ALGORITHM,
        authorization_id=_authorization_id_from_record(data),
        **data,
    )


def build_canonical_p18_retry_incident_rollback_request(
    *,
    P18_5_result: ReviewValidationLoopIntegrationResult,
    requested_action: RetryIncidentRollbackRequestedAction = (
        RetryIncidentRollbackRequestedAction.NONE
    ),
    human_authorization: RetryIncidentRollbackHumanAuthorization | None = None,
    observed_attempt_count: int = 1,
    max_attempts: int = 2,
    prior_recovery_result_SHA256: str | None = None,
) -> RetryIncidentRollbackRequest:
    _validate_p18_5_non_accept(P18_5_result)
    handoff = P18_5_result.P18_6_handoff
    if handoff is None:
        raise RetryIncidentRollbackStateError("P18.5 result has no P18.6 handoff")
    request = _make_model(
        RetryIncidentRollbackRequest,
        "request_SHA256",
        RETRY_INCIDENT_ROLLBACK_REQUEST_DIGEST_ALGORITHM,
        P18_5_result=P18_5_result,
        P18_5_result_SHA256=P18_5_result.result_SHA256,
        P18_6_handoff=handoff,
        P18_6_handoff_SHA256=handoff.handoff_SHA256,
        project_id=_CANONICAL_PROJECT_ID,
        macroproject_id=_CANONICAL_MACROPROJECT_ID,
        ticket_id=_CANONICAL_TICKET_ID,
        WorkPacket_ID=P18_5_result.WorkPacket_ID,
        WorkPacket_SHA256=P18_5_result.WorkPacket_SHA256,
        expected_workflow_state=P18_5_result.resulting_workflow_snapshot.current_state,
        requested_action=requested_action,
        human_authorization=human_authorization,
        observed_attempt_count=observed_attempt_count,
        max_attempts=max_attempts,
        prior_recovery_result_SHA256=prior_recovery_result_SHA256,
    )
    validate_retry_incident_rollback_request(request)
    return request


def validate_retry_incident_rollback_request(
    request: RetryIncidentRollbackRequest,
) -> None:
    try:
        validated = RetryIncidentRollbackRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise RetryIncidentRollbackValidationError("invalid P18.6 request") from exc
    _validate_p18_5_non_accept(validated.P18_5_result)
    _validate_request_bindings(validated)
    _validate_replay_policy(validated)
    _validate_requested_action(validated)


def build_retry_incident_rollback_workflow(
    request: RetryIncidentRollbackRequest,
) -> RetryIncidentRollbackResult:
    validate_retry_incident_rollback_request(request)
    validated = RetryIncidentRollbackRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    retry_plan = _build_retry_attempt_plan(validated)
    rollback_plan = _build_rollback_plan(validated)
    incident_record = _build_incident_record(validated)
    decision = _derive_decision(validated, retry_plan, rollback_plan)
    workflow_results = _build_workflow_transitions(validated, decision)
    if not all(result.accepted for result in workflow_results):
        raise RetryIncidentRollbackStateError("P18.0 recovery transition rejected")
    resulting_snapshot = (
        workflow_results[-1].resulting_snapshot
        if workflow_results
        else validated.P18_5_result.resulting_workflow_snapshot
    )
    findings = _build_findings(
        request=validated,
        decision=decision,
        retry_plan=retry_plan,
        rollback_plan=rollback_plan,
    )
    summary = _build_summary(findings)
    result_values = {
        "schema_version": RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION,
        "policy_id": RETRY_INCIDENT_ROLLBACK_POLICY_ID,
        "state": _state_for_decision(decision),
        "decision": decision,
        "request": validated,
        "capability_reuse_assessments": build_retry_incident_rollback_reuse_matrix(),
        "retry_attempt_plan": retry_plan,
        "incident_record": incident_record,
        "rollback_plan": rollback_plan,
        "workflow_transition_results": workflow_results,
        "resulting_workflow_snapshot": resulting_snapshot,
        "findings": findings,
        "summary": summary,
        "project_id": _CANONICAL_PROJECT_ID,
        "macroproject_id": _CANONICAL_MACROPROJECT_ID,
        "ticket_id": _CANONICAL_TICKET_ID,
        "WorkPacket_ID": validated.WorkPacket_ID,
        "WorkPacket_SHA256": validated.WorkPacket_SHA256,
        "P18_5_result_SHA256": validated.P18_5_result_SHA256,
        "P18_6_handoff_SHA256": validated.P18_6_handoff_SHA256,
        "source_review_decision": validated.P18_5_result.decision,
        "source_workflow_state": validated.P18_5_result.resulting_workflow_snapshot.current_state,
        "requested_action": validated.requested_action,
        "human_authorization_SHA256": validated.human_authorization.authorization_SHA256
        if validated.human_authorization is not None
        else None,
        "retry_authorized_by_human": validated.requested_action
        is RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
        "rollback_authorized_by_human": validated.requested_action
        is RetryIncidentRollbackRequestedAction.AUTHORIZE_ROLLBACK,
        "retry_budget_exhausted": retry_plan.retry_budget_exhausted,
        "Git_commands_executed": 0,
        "Git_staging_performed": False,
        "Git_commit_performed": False,
        "Git_push_performed": False,
        "staging_calls": 0,
        "commit_calls": 0,
        "push_calls": 0,
        "retry_execution_count": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "rollback_execution_count": 0,
        "workspace_allocation_calls_in_P18_6": 0,
        "workspace_cleanup_calls_in_P18_6": 0,
        "workspace_restore_calls_in_P18_6": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "GBrain_calls": 0,
        "Paperclip_calls": 0,
        "Kanban_SQLite_canonical_authority": False,
        "duplicate_retry_controller_created": False,
        "duplicate_requeue_controller_created": False,
        "duplicate_incident_store_created": False,
        "duplicate_rollback_controller_created": False,
        "duplicate_workspace_restorer_created": False,
        "duplicate_Git_handoff_created": False,
        "duplicate_workflow_state_machine_created": False,
    }
    result = _make_model(
        RetryIncidentRollbackResult,
        "result_SHA256",
        RETRY_INCIDENT_ROLLBACK_RESULT_DIGEST_ALGORITHM,
        recovery_id=_recovery_id_from_record(result_values),
        **result_values,
    )
    validate_retry_incident_rollback_result(result)
    return result


def validate_retry_incident_rollback_result(
    result: RetryIncidentRollbackResult,
) -> None:
    try:
        validated = RetryIncidentRollbackResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise RetryIncidentRollbackValidationError("invalid P18.6 result") from exc
    validate_retry_incident_rollback_request(validated.request)
    _validate_result_bindings(validated)


def summarize_retry_incident_rollback_workflow(
    result: RetryIncidentRollbackResult,
) -> RetryIncidentRollbackSummary:
    validate_retry_incident_rollback_result(result)
    return result.summary


def build_retry_incident_rollback_reuse_matrix() -> tuple[
    RetryIncidentRollbackCapabilityReuseAssessment, ...
]:
    rows = (
        (
            "P18.5 non-accept handoff",
            "hermes_cli/agent_platform/workflow/review_validation_loop.py",
            "ReviewValidationP18_6Handoff",
            "Binds terminal review blocker evidence for P18.6 recovery routing.",
            "P18.5 owns review, validation and non-accept handoff classification.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            True,
        ),
        (
            "P18.5 integration result",
            "hermes_cli/agent_platform/workflow/review_validation_loop.py",
            "ReviewValidationLoopIntegrationResult",
            "Provides source decision, workflow state and P17 digest bindings.",
            "P18.5 remains the source of accepted, correction, incident and cancellation decisions.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            True,
        ),
        (
            "terminal outcome envelopes",
            "hermes_cli/agent_platform/work_packet/outcome_envelopes.py",
            "OutcomeEnvelope",
            "Carries result, failure and cancellation evidence plus retry-not-authorized posture.",
            "P17.5 owns terminal outcome and retry posture evidence.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            False,
        ),
        (
            "single-agent execution evidence",
            "hermes_cli/agent_platform/work_packet/single_agent_execution.py",
            "SingleAgentExecutionResult",
            "Identifies execution-failure incidents without re-running actions.",
            "P17.3 owns WorkPacket action execution evidence and current-action rollback only.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            False,
        ),
        (
            "workspace allocation evidence",
            "hermes_cli/agent_platform/work_packet/workspace_allocator.py",
            "WorkspaceAllocationResult",
            "Provides prior workspace binding evidence without new allocation or restoration.",
            "P17.1 owns workspace allocation validation; P18.6 creates no restorer.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            False,
        ),
        (
            "human Git handoff",
            "hermes_cli/agent_platform/work_packet/human_git_handoff.py",
            "GitHandoffResult",
            "Preserves human-only Git authority for accepted handoffs and manual rollback review.",
            "P17.7 owns non-executing human Git handoff evidence.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            False,
        ),
        (
            "governed recovery transitions",
            "hermes_cli/agent_platform/workflow/governed_state_machine.py",
            "GovernedWorkflowTransitionResult",
            "Projects human-authorized retry or rollback state transitions without executing them.",
            "P18.0 owns FAILED to RETRY_PENDING and FAILED to ROLLBACK_REQUIRED transitions.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            True,
        ),
        (
            "Kanban retry counters",
            "hermes_cli/kanban_db.py",
            "consecutive_failures",
            "Existing runtime tracks repeated task failures and bounded failure limits.",
            "Kanban runtime mutation remains outside P18.6 governance decisions.",
            RetryIncidentRollbackCapabilityDecision.CUSTOMIZE,
            True,
            False,
        ),
        (
            "Kanban requeue and reclaim",
            "hermes_cli/kanban_db.py",
            "reclaim_task",
            "Runtime can reclaim or reassign tasks, but those paths mutate board state.",
            "P18.6 classifies these as human/runtime operations and does not invoke them.",
            RetryIncidentRollbackCapabilityDecision.DEFER,
            False,
            False,
        ),
        (
            "Kanban dashboard recovery endpoints",
            "plugins/kanban/dashboard/plugin_api.py",
            "reclaim_task_endpoint",
            "Dashboard exposes human/operator recovery affordances over Kanban tasks.",
            "P18.6 does not route through dashboard endpoints or mutate task claims.",
            RetryIncidentRollbackCapabilityDecision.DEFER,
            False,
            False,
        ),
        (
            "failure diagnostics",
            "hermes_cli/kanban_diagnostics.py",
            "build_repeated_failure_diagnostic",
            "Provides repeated-failure guidance based on configured failure limits.",
            "P18.6 records bounded attempt counts without reading live diagnostic state.",
            RetryIncidentRollbackCapabilityDecision.CUSTOMIZE,
            True,
            False,
        ),
        (
            "bounded stop nudge attempts",
            "agent/kanban_stop.py",
            "build_kanban_stop_nudge",
            "Shows existing bounded retry-like nudging is local to worker protocol completion.",
            "P18.6 uses the bound as evidence only and does not continue a conversation.",
            RetryIncidentRollbackCapabilityDecision.RETAIN,
            False,
            False,
        ),
    )
    return tuple(
        _make_model(
            RetryIncidentRollbackCapabilityReuseAssessment,
            "assessment_SHA256",
            RETRY_INCIDENT_ROLLBACK_CAPABILITY_DIGEST_ALGORITHM,
            capability=capability,
            source_file=source_file,
            symbol=symbol,
            purpose=purpose,
            current_authority=current_authority,
            suitable_for_P18_6=True,
            decision=decision,
            customized=customized,
            duplicate_created=False,
            invoked_by_P18_6=invoked,
            reason="Reuse-first recovery governance; P18.6 records decisions without runtime mutation.",
        )
        for (
            capability,
            source_file,
            symbol,
            purpose,
            current_authority,
            decision,
            customized,
            invoked,
        ) in rows
    )


def _validate_p18_5_non_accept(result: ReviewValidationLoopIntegrationResult) -> None:
    try:
        validate_review_validation_loop_integration_result(result)
    except ValueError as exc:
        raise RetryIncidentRollbackValidationError("invalid P18.5 result") from exc
    if result.decision is ReviewValidationLoopDecision.ACCEPT:
        raise RetryIncidentRollbackStateError(
            "P18.6 accepts only non-accept P18.5 results"
        )
    if not result.P18_6_ready or result.P18_6_handoff is None:
        raise RetryIncidentRollbackPolicyError("P18.5 result is not P18.6-ready")
    handoff = result.P18_6_handoff
    if handoff.retry_started or handoff.rollback_started:
        raise RetryIncidentRollbackPolicyError("P18.5 handoff must not start recovery")


def _validate_request_bindings(request: RetryIncidentRollbackRequest) -> None:
    result = request.P18_5_result
    handoff = result.P18_6_handoff
    if handoff is None:
        raise RetryIncidentRollbackIntegrityError("P18.6 handoff missing")
    expected = {
        "P18_5_result_SHA256": result.result_SHA256,
        "P18_6_handoff_SHA256": handoff.handoff_SHA256,
        "WorkPacket_ID": result.WorkPacket_ID,
        "WorkPacket_SHA256": result.WorkPacket_SHA256,
    }
    for field, value in expected.items():
        if getattr(request, field) != value:
            raise RetryIncidentRollbackIntegrityError(f"{field} mismatch")
    if request.P18_6_handoff != handoff:
        raise RetryIncidentRollbackIntegrityError("P18.6 handoff object mismatch")
    if (
        request.expected_workflow_state
        is not result.resulting_workflow_snapshot.current_state
    ):
        raise RetryIncidentRollbackStateError("expected workflow state mismatch")
    if request.expected_workflow_state is not handoff.workflow_state:
        raise RetryIncidentRollbackStateError("handoff workflow state mismatch")
    if (
        request.project_id != _CANONICAL_PROJECT_ID
        or request.macroproject_id != _CANONICAL_MACROPROJECT_ID
        or request.ticket_id != _CANONICAL_TICKET_ID
    ):
        raise RetryIncidentRollbackIntegrityError("project identity mismatch")


def _validate_replay_policy(request: RetryIncidentRollbackRequest) -> None:
    if request.prior_recovery_result_SHA256 is not None:
        raise RetryIncidentRollbackStateError(
            "prior P18.6 recovery evidence blocks replay"
        )


def _validate_requested_action(request: RetryIncidentRollbackRequest) -> None:
    action = request.requested_action
    if action is RetryIncidentRollbackRequestedAction.NONE:
        return
    if request.P18_5_result.decision is not ReviewValidationLoopDecision.INCIDENT:
        raise RetryIncidentRollbackPolicyError(
            "human retry or rollback authorization requires incident source"
        )
    if (
        request.P18_5_result.resulting_workflow_snapshot.current_state
        is not GovernedWorkflowState.FAILED
    ):
        raise RetryIncidentRollbackStateError(
            "retry or rollback requires failed workflow state"
        )


def _build_retry_attempt_plan(
    request: RetryIncidentRollbackRequest,
) -> RetryAttemptPlan:
    requested = (
        request.requested_action is RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY
    )
    exhausted = request.observed_attempt_count >= request.max_attempts
    authorized = requested and not exhausted
    data = {
        "WorkPacket_ID": request.WorkPacket_ID,
        "WorkPacket_SHA256": request.WorkPacket_SHA256,
        "observed_attempt_count": request.observed_attempt_count,
        "max_attempts": request.max_attempts,
        "retry_budget_exhausted": exhausted,
        "retry_requested_by_human": requested,
        "retry_authorized_for_governed_state": authorized,
        "next_attempt_number": request.observed_attempt_count + 1
        if authorized
        else None,
        "retry_execution_started": False,
        "automatic_retry_authorized": False,
        "automatic_requeue_authorized": False,
        "Kanban_requeue_authorized": False,
    }
    return _make_model(
        RetryAttemptPlan,
        "attempt_plan_SHA256",
        RETRY_INCIDENT_ROLLBACK_ATTEMPT_DIGEST_ALGORITHM,
        attempt_plan_id=_plan_id_from_record("RETRY", data),
        **data,
    )


def _build_rollback_plan(
    request: RetryIncidentRollbackRequest,
) -> RollbackGovernancePlan:
    requested = (
        request.requested_action
        is RetryIncidentRollbackRequestedAction.AUTHORIZE_ROLLBACK
    )
    data = {
        "WorkPacket_ID": request.WorkPacket_ID,
        "WorkPacket_SHA256": request.WorkPacket_SHA256,
        "rollback_requested_by_human": requested,
        "rollback_required_for_governed_state": requested,
        "rollback_target": "manual_human_rollback_review" if requested else "none",
        "human_git_handoff_required": requested,
        "rollback_execution_started": False,
        "automatic_rollback_authorized": False,
        "Git_rollback_authorized": False,
        "workspace_restore_authorized": False,
    }
    return _make_model(
        RollbackGovernancePlan,
        "rollback_plan_SHA256",
        RETRY_INCIDENT_ROLLBACK_ROLLBACK_DIGEST_ALGORITHM,
        rollback_plan_id=_plan_id_from_record("ROLLBACK", data),
        **data,
    )


def _build_incident_record(
    request: RetryIncidentRollbackRequest,
) -> RetryIncidentRecord | None:
    result = request.P18_5_result
    if result.decision is not ReviewValidationLoopDecision.INCIDENT:
        return None
    handoff = request.P18_6_handoff
    data = {
        "WorkPacket_ID": request.WorkPacket_ID,
        "WorkPacket_SHA256": request.WorkPacket_SHA256,
        "source_review_decision": result.decision,
        "source_workflow_state": result.resulting_workflow_snapshot.current_state,
        "execution_outcome_SHA256": result.execution_outcome_SHA256,
        "failure_category": result.execution_outcome_binding.failure_category.value,
        "blocker_codes": handoff.blocker_codes,
        "incident_open": True,
        "human_triage_required": True,
        "automatic_retry_authorized": False,
        "automatic_rollback_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return _make_model(
        RetryIncidentRecord,
        "incident_SHA256",
        RETRY_INCIDENT_ROLLBACK_INCIDENT_DIGEST_ALGORITHM,
        incident_id=_incident_id_from_record(data),
        **data,
    )


def _derive_decision(
    request: RetryIncidentRollbackRequest,
    retry_plan: RetryAttemptPlan,
    rollback_plan: RollbackGovernancePlan,
) -> RetryIncidentRollbackDecision:
    source_decision = request.P18_5_result.decision
    if source_decision is ReviewValidationLoopDecision.CANCELLED:
        return RetryIncidentRollbackDecision.CANCELLED
    if source_decision is ReviewValidationLoopDecision.NEEDS_CORRECTION:
        return RetryIncidentRollbackDecision.AWAIT_HUMAN_CORRECTION
    if rollback_plan.rollback_required_for_governed_state:
        return RetryIncidentRollbackDecision.ROLLBACK_REQUIRED
    if retry_plan.retry_authorized_for_governed_state:
        return RetryIncidentRollbackDecision.RETRY_PENDING
    return RetryIncidentRollbackDecision.RECORD_INCIDENT


def _build_workflow_transitions(
    request: RetryIncidentRollbackRequest,
    decision: RetryIncidentRollbackDecision,
) -> tuple[GovernedWorkflowTransitionResult, ...]:
    if decision not in {
        RetryIncidentRollbackDecision.RETRY_PENDING,
        RetryIncidentRollbackDecision.ROLLBACK_REQUIRED,
    }:
        return ()
    snapshot = request.P18_5_result.resulting_workflow_snapshot
    if decision is RetryIncidentRollbackDecision.RETRY_PENDING:
        trigger = WorkflowTransitionTrigger.RETRY_AUTHORIZED
        evidence_refs = ("human_retry_authorization",)
        runtime_state = "retry_pending"
        retry_state_present = True
    else:
        trigger = WorkflowTransitionTrigger.ROLLBACK_AUTHORIZED
        evidence_refs = ("human_rollback_authorization",)
        runtime_state = "rollback_required"
        retry_state_present = False
    projection = build_hermes_workflow_projection(
        runtime_kind=HermesWorkflowRuntimeKind.WORK_PACKET,
        runtime_state=runtime_state,
        task_id=request.WorkPacket_ID,
        board_or_queue_id=None,
        worker_id_present=False,
        workspace_binding_present=True,
        dependency_blocked=False,
        retry_state_present=retry_state_present,
        reclaim_state_present=False,
    )
    transition_request = GovernedWorkflowTransitionRequest(
        current_snapshot=snapshot,
        trigger=trigger,
        authority=WorkflowTransitionAuthority.HUMAN,
        evidence_refs=evidence_refs,
        runtime_projection=projection,
    )
    validate_governed_workflow_transition_request(transition_request)
    return (build_governed_workflow_transition(transition_request),)


def _build_findings(
    *,
    request: RetryIncidentRollbackRequest,
    decision: RetryIncidentRollbackDecision,
    retry_plan: RetryAttemptPlan,
    rollback_plan: RollbackGovernancePlan,
) -> tuple[RetryIncidentRollbackFinding, ...]:
    records = (
        (
            RetryIncidentRollbackFindingCode.P18_5_HANDOFF_VALID,
            "P18.5 non-accept handoff is valid for P18.6.",
            request.P18_6_handoff_SHA256,
        ),
        (
            RetryIncidentRollbackFindingCode.RECOVERY_DECISION_VALID,
            f"P18.6 recovery decision is {decision.value}.",
            None,
        ),
        (
            RetryIncidentRollbackFindingCode.RETRY_ATTEMPT_TRACKING_VALID,
            f"Observed attempts {retry_plan.observed_attempt_count} within max attempts {retry_plan.max_attempts}.",
            retry_plan.attempt_plan_SHA256,
        ),
        (
            RetryIncidentRollbackFindingCode.INCIDENT_RECORD_VALID,
            "Incident evidence is recorded only for execution-failure sources.",
            request.P18_5_result.execution_outcome_SHA256,
        ),
        (
            RetryIncidentRollbackFindingCode.ROLLBACK_GOVERNANCE_VALID,
            "Rollback is represented as human governance and not execution.",
            rollback_plan.rollback_plan_SHA256,
        ),
        (
            RetryIncidentRollbackFindingCode.WORKFLOW_TRANSITION_VALID,
            "P18.0 recovery transition is reused only when human-authorized and valid.",
            None,
        ),
        (
            RetryIncidentRollbackFindingCode.KANBAN_MUTATION_DEFERRED,
            "Kanban requeue, reclaim and reassign mutation paths are deferred.",
            None,
        ),
        (
            RetryIncidentRollbackFindingCode.WORKSPACE_RESTORATION_DEFERRED,
            "Workspace cleanup and restoration are not performed by P18.6.",
            None,
        ),
        (
            RetryIncidentRollbackFindingCode.HUMAN_AUTHORITY_PRESERVED,
            "Retry and rollback authorization remain human-only governance actions.",
            request.human_authorization.authorization_SHA256
            if request.human_authorization is not None
            else None,
        ),
        (
            RetryIncidentRollbackFindingCode.NO_AUTONOMOUS_RETRY_VALID,
            "P18.6 starts no retry and authorizes no automatic requeue.",
            None,
        ),
        (
            RetryIncidentRollbackFindingCode.NO_AUTONOMOUS_ROLLBACK_VALID,
            "P18.6 starts no rollback and authorizes no Git or workspace restore.",
            None,
        ),
        (
            RetryIncidentRollbackFindingCode.SECURITY_BOUNDARY_VALID,
            "P18.6 stores bounded deterministic evidence only.",
            None,
        ),
    )
    return tuple(
        _make_model(
            RetryIncidentRollbackFinding,
            "finding_SHA256",
            RETRY_INCIDENT_ROLLBACK_FINDING_DIGEST_ALGORITHM,
            finding_id=f"RIRF-{index:03d}",
            severity=RetryIncidentRollbackFindingSeverity.INFO,
            code=code,
            message=message,
            evidence_SHA256=evidence,
        )
        for index, (code, message, evidence) in enumerate(records, start=1)
    )


def _build_summary(
    findings: tuple[RetryIncidentRollbackFinding, ...],
) -> RetryIncidentRollbackSummary:
    info = sum(
        1
        for finding in findings
        if finding.severity is RetryIncidentRollbackFindingSeverity.INFO
    )
    warnings = sum(
        1
        for finding in findings
        if finding.severity is RetryIncidentRollbackFindingSeverity.WARNING
    )
    blockers = sum(
        1
        for finding in findings
        if finding.severity is RetryIncidentRollbackFindingSeverity.BLOCKING
    )
    return _make_model(
        RetryIncidentRollbackSummary,
        "summary_SHA256",
        RETRY_INCIDENT_ROLLBACK_SUMMARY_DIGEST_ALGORITHM,
        P18_5_handoff_valid=True,
        source_non_accept_valid=True,
        recovery_decision_valid=True,
        retry_attempt_tracking_valid=True,
        incident_classification_valid=True,
        rollback_governance_valid=True,
        workflow_transition_valid=True,
        Kanban_runtime_mutation_deferred=True,
        task_requeue_reclaim_deferred=True,
        workspace_restoration_deferred=True,
        human_Git_handoff_boundary_valid=True,
        no_autonomous_retry_valid=True,
        no_autonomous_rollback_valid=True,
        no_runtime_mutation_valid=True,
        security_valid=True,
        information_finding_count=info,
        warning_finding_count=warnings,
        blocking_finding_count=blockers,
    )


def _state_for_decision(
    decision: RetryIncidentRollbackDecision,
) -> RetryIncidentRollbackState:
    if decision is RetryIncidentRollbackDecision.AWAIT_HUMAN_CORRECTION:
        return RetryIncidentRollbackState.CORRECTION_REQUIRED
    if decision is RetryIncidentRollbackDecision.RETRY_PENDING:
        return RetryIncidentRollbackState.RETRY_PENDING
    if decision is RetryIncidentRollbackDecision.ROLLBACK_REQUIRED:
        return RetryIncidentRollbackState.ROLLBACK_REQUIRED
    if decision is RetryIncidentRollbackDecision.CANCELLED:
        return RetryIncidentRollbackState.CANCELLED
    return RetryIncidentRollbackState.INCIDENT_RECORDED


def _authorization_id(value: RetryIncidentRollbackHumanAuthorization) -> str:
    return _authorization_id_from_record(
        value.model_dump(
            mode="json", exclude={"authorization_id", "authorization_SHA256"}
        )
    )


def _authorization_id_from_record(record: object) -> str:
    digest = _digest_from_record(RETRY_INCIDENT_ROLLBACK_ID_DIGEST_ALGORITHM, record)
    return f"RIR-AUTH-{digest[:12]}"


def _plan_id(kind: str, value: BaseModel) -> str:
    digest_field = "attempt_plan_SHA256" if kind == "RETRY" else "rollback_plan_SHA256"
    id_field = "attempt_plan_id" if kind == "RETRY" else "rollback_plan_id"
    return _plan_id_from_record(
        kind,
        value.model_dump(mode="json", exclude={id_field, digest_field}),
    )


def _plan_id_from_record(kind: str, record: object) -> str:
    digest = _digest_from_record(RETRY_INCIDENT_ROLLBACK_ID_DIGEST_ALGORITHM, record)
    return f"RIR-{kind}-{digest[:12]}"


def _incident_id(value: RetryIncidentRecord) -> str:
    return _incident_id_from_record(
        value.model_dump(mode="json", exclude={"incident_id", "incident_SHA256"})
    )


def _incident_id_from_record(record: object) -> str:
    digest = _digest_from_record(RETRY_INCIDENT_ROLLBACK_ID_DIGEST_ALGORITHM, record)
    return f"RIR-INC-{digest[:12]}"


def _recovery_id(value: RetryIncidentRollbackResult) -> str:
    return _recovery_id_from_record(
        value.model_dump(mode="json", exclude={"recovery_id", "result_SHA256"})
    )


def _recovery_id_from_record(record: object) -> str:
    digest = _digest_from_record(RETRY_INCIDENT_ROLLBACK_ID_DIGEST_ALGORITHM, record)
    return f"RIR-P18-6-{digest[:12]}"


def _validate_result_bindings(result: RetryIncidentRollbackResult) -> None:
    request = result.request
    if (
        result.project_id != request.project_id
        or result.macroproject_id != request.macroproject_id
    ):
        raise RetryIncidentRollbackIntegrityError("project identity mismatch")
    if result.ticket_id != request.ticket_id:
        raise RetryIncidentRollbackIntegrityError("ticket identity mismatch")
    if result.WorkPacket_ID != request.WorkPacket_ID:
        raise RetryIncidentRollbackIntegrityError("WorkPacket ID mismatch")
    if result.WorkPacket_SHA256 != request.WorkPacket_SHA256:
        raise RetryIncidentRollbackIntegrityError("WorkPacket SHA mismatch")
    if result.P18_5_result_SHA256 != request.P18_5_result_SHA256:
        raise RetryIncidentRollbackIntegrityError("P18.5 digest mismatch")
    if result.P18_6_handoff_SHA256 != request.P18_6_handoff_SHA256:
        raise RetryIncidentRollbackIntegrityError("P18.6 handoff digest mismatch")
    if result.source_review_decision is not request.P18_5_result.decision:
        raise RetryIncidentRollbackIntegrityError("source review decision mismatch")
    if (
        result.source_workflow_state
        is not request.P18_5_result.resulting_workflow_snapshot.current_state
    ):
        raise RetryIncidentRollbackStateError("source workflow state mismatch")


__all__ = (
    "RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION",
    "RETRY_INCIDENT_ROLLBACK_POLICY_ID",
    "RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION",
    "RetryIncidentRollbackBoundary",
    "RetryIncidentRollbackCapabilityDecision",
    "RetryIncidentRollbackRequestedAction",
    "RetryIncidentRollbackDecision",
    "RetryIncidentRollbackState",
    "RetryIncidentRollbackFindingSeverity",
    "RetryIncidentRollbackFindingCode",
    "RetryIncidentRollbackHumanAuthorization",
    "RetryIncidentRollbackCapabilityReuseAssessment",
    "RetryIncidentRollbackRequest",
    "RetryAttemptPlan",
    "RetryIncidentRecord",
    "RollbackGovernancePlan",
    "RetryIncidentRollbackFinding",
    "RetryIncidentRollbackSummary",
    "RetryIncidentRollbackResult",
    "RetryIncidentRollbackError",
    "RetryIncidentRollbackInputError",
    "RetryIncidentRollbackIntegrityError",
    "RetryIncidentRollbackPolicyError",
    "RetryIncidentRollbackStateError",
    "RetryIncidentRollbackValidationError",
    "build_retry_incident_rollback_human_authorization",
    "build_retry_incident_rollback_reuse_matrix",
    "build_canonical_p18_retry_incident_rollback_request",
    "validate_retry_incident_rollback_request",
    "build_retry_incident_rollback_workflow",
    "validate_retry_incident_rollback_result",
    "summarize_retry_incident_rollback_workflow",
)
