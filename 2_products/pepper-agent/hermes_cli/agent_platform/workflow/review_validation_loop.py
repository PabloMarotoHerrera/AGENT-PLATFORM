"""P18.5 governed review and validation loop for Pepper.

This module consumes an admitted P18.4 queue result and already-produced P17
execution outcome, validation, diff/artifact review and optional human Git
handoff evidence. It is a deterministic governance integration layer only: it
does not execute WorkPackets, run validation commands, inspect diffs, mutate
Git, retry, roll back, call providers/models, run Docker, run Graphify, write
G-Brain memory, operate Paperclip or persist runtime state.
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

from hermes_cli.agent_platform.work_packet import (
    AggregateReviewState,
    ArtifactReviewVerdict,
    DiffArtifactReviewResult,
    DiffReviewVerdict,
    GitHandoffDecision,
    GitHandoffResult,
    GitHandoffState,
    OutcomeEnvelope,
    OutcomeEnvelopeKind,
    OutcomeFailureCategory,
    OutcomeStage,
    OutcomeTerminalState,
    validate_diff_artifact_review_result,
    validate_human_git_handoff_result,
    validate_outcome_envelope,
)
from hermes_cli.agent_platform.workflow.dependency_execution_queue import (
    DependencyAwareQueueDecision,
    DependencyAwareQueueIntegrationResult,
    DependencyAwareQueueState,
    validate_dependency_aware_queue_integration_result,
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


REVIEW_VALIDATION_LOOP_SCHEMA_VERSION = 1
REVIEW_VALIDATION_LOOP_POLICY_ID = "pepper-review-validation-loop-v1"
REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION = "REVIEW_POST_EXECUTION_ONLY"

REVIEW_VALIDATION_REQUEST_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-loop-request-sha256-v1"
)
REVIEW_VALIDATION_CAPABILITY_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-capability-sha256-v1"
)
REVIEW_VALIDATION_OUTCOME_BINDING_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-outcome-binding-sha256-v1"
)
REVIEW_VALIDATION_FINDING_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-finding-sha256-v1"
)
REVIEW_VALIDATION_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-summary-sha256-v1"
)
REVIEW_VALIDATION_P18_6_HANDOFF_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-p18-6-handoff-sha256-v1"
)
REVIEW_VALIDATION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-review-validation-result-sha256-v1"
)
REVIEW_VALIDATION_ID_DIGEST_ALGORITHM = "agent-platform-review-validation-id-sha256-v1"

_CANONICAL_PROJECT_ID = "PEPPER"
_CANONICAL_MACROPROJECT_ID = "P18"
_CANONICAL_TICKET_ID = "P18.2"
_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_INTEGRATION_ID_PATTERN = r"^RVI-P18-[a-f0-9]{12}$"
_FINDING_ID_PATTERN = r"^RVIF-[0-9]{3}$"
_HANDOFF_ID_PATTERN = r"^RVH-P18-6-[a-f0-9]{12}$"
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
IntegrationIdentifier = Annotated[str, Field(pattern=_INTEGRATION_ID_PATTERN)]
FindingIdentifier = Annotated[str, Field(pattern=_FINDING_ID_PATTERN)]
P18_6HandoffIdentifier = Annotated[str, Field(pattern=_HANDOFF_ID_PATTERN)]
WorkPacketIdentifier = Annotated[str, Field(pattern=_WORK_PACKET_ID_PATTERN)]
BoundedText = Annotated[str, Field(min_length=1, max_length=1024)]


class ReviewValidationLoopError(ValueError):
    """Base error for P18.5 review-validation integration failures."""


class ReviewValidationLoopInputError(ReviewValidationLoopError):
    """Raised when review-loop inputs are malformed."""


class ReviewValidationLoopIntegrityError(ReviewValidationLoopError):
    """Raised when review-loop artifact bindings or digests mismatch."""


class ReviewValidationLoopPolicyError(ReviewValidationLoopError):
    """Raised when review-loop policy boundaries are violated."""


class ReviewValidationLoopStateError(ReviewValidationLoopError):
    """Raised when workflow or terminal evidence state is incompatible."""


class ReviewValidationLoopValidationError(ReviewValidationLoopError):
    """Raised when immutable review-loop evidence fails validation."""


class ReviewValidationRuntimeBoundary(str, Enum):
    REVIEW_CONSUMES_EXISTING_EXECUTION_OUTCOME = (
        "REVIEW_CONSUMES_EXISTING_EXECUTION_OUTCOME"
    )
    REVIEW_ORCHESTRATES_ACCEPTED_P17_EXECUTION_SEQUENCE = (
        "REVIEW_ORCHESTRATES_ACCEPTED_P17_EXECUTION_SEQUENCE"
    )
    REVIEW_POST_EXECUTION_ONLY = "REVIEW_POST_EXECUTION_ONLY"
    OTHER_WITH_EVIDENCE = "OTHER_WITH_EVIDENCE"


class ReviewValidationCapabilityDecision(str, Enum):
    RETAIN = "retain"
    CUSTOMIZE = "customize"
    REPLACE = "replace"
    DEFER = "defer"
    NOT_APPLICABLE = "not_applicable"


class ReviewValidationLoopDecision(str, Enum):
    ACCEPT = "accept"
    NEEDS_CORRECTION = "needs_correction"
    INCIDENT = "incident"
    CANCELLED = "cancelled"


class ReviewValidationLoopState(str, Enum):
    COMPLETED = "completed"
    CORRECTION_REQUIRED = "correction_required"
    INCIDENT = "incident"
    CANCELLED = "cancelled"


class ReviewValidationFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class ReviewValidationFindingCode(str, Enum):
    P18_4_CONTINUATION_VALID = "p18_4_continuation_valid"
    P17_OUTCOME_ENVELOPE_REUSED = "p17_outcome_envelope_reused"
    P17_VALIDATION_RUNNER_REUSED = "p17_validation_runner_reused"
    P17_DIFF_ARTIFACT_REVIEW_REUSED = "p17_diff_artifact_review_reused"
    P17_HUMAN_GIT_HANDOFF_REUSED = "p17_human_git_handoff_reused"
    WORKFLOW_TRANSITION_VALID = "workflow_transition_valid"
    REVIEW_DECISION_VALID = "review_decision_valid"
    P18_6_HANDOFF_VALID = "p18_6_handoff_valid"
    NO_RETRY_BOUNDARY_VALID = "no_retry_boundary_valid"
    NO_ROLLBACK_BOUNDARY_VALID = "no_rollback_boundary_valid"
    SECURITY_BOUNDARY_VALID = "security_boundary_valid"
    INTEGRATION_ACCEPTED = "integration_accepted"


class _ReviewValidationModel(BaseModel):
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
    model_type: type[_ReviewValidationModel],
    digest_field: str,
    algorithm: str,
    **data: object,
) -> _ReviewValidationModel:
    provisional = model_type.model_construct(**data, **{digest_field: "0" * 64})
    return model_type(
        **data,
        **{digest_field: _model_digest(algorithm, provisional, digest_field)},
    )


class ReviewValidationCapabilityReuseAssessment(_ReviewValidationModel):
    capability: BoundedText
    source_file: BoundedText
    symbol: BoundedText
    purpose: BoundedText
    current_authority: BoundedText
    suitable_for_P18_5: StrictBool
    decision: ReviewValidationCapabilityDecision
    customized: StrictBool
    duplicate_created: StrictBool
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
        return _validate_safe_text(value, "capability reuse assessment")

    @model_validator(mode="after")
    def _validate_assessment(self) -> ReviewValidationCapabilityReuseAssessment:
        if (
            self.decision is ReviewValidationCapabilityDecision.RETAIN
            and self.customized
        ):
            raise ValueError("retained capability cannot be customized")
        if self.duplicate_created:
            raise ValueError("P18.5 must not create duplicate P17 capability")
        if self.assessment_SHA256 != _model_digest(
            REVIEW_VALIDATION_CAPABILITY_DIGEST_ALGORITHM,
            self,
            "assessment_SHA256",
        ):
            raise ValueError("capability assessment digest mismatch")
        return self


class ReviewValidationExecutionOutcomeBinding(_ReviewValidationModel):
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    execution_outcome_state: Literal["result", "failure", "cancellation"]
    execution_outcome_SHA256: DigestText
    terminal_stage: OutcomeStage
    terminal_state: OutcomeTerminalState
    failure_category: OutcomeFailureCategory
    single_agent_result_SHA256: DigestText | None = None
    validation_result_SHA256: DigestText | None = None
    validation_session_SHA256: DigestText | None = None
    terminal_evidence_SHA256: DigestText
    execution_successful: StrictBool
    execution_cancelled: StrictBool
    binding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_binding(self) -> ReviewValidationExecutionOutcomeBinding:
        if self.execution_successful != (
            self.execution_outcome_state == OutcomeEnvelopeKind.RESULT.value
            or (
                self.execution_outcome_state == OutcomeEnvelopeKind.FAILURE.value
                and self.terminal_stage is OutcomeStage.VALIDATION_COMMAND_RUNNER
                and self.single_agent_result_SHA256 is not None
            )
        ):
            raise ValueError("execution_successful must derive from P17 terminal stage")
        if self.execution_cancelled != (
            self.execution_outcome_state == OutcomeEnvelopeKind.CANCELLATION.value
        ):
            raise ValueError("execution_cancelled must derive from outcome kind")
        if self.execution_outcome_state == OutcomeEnvelopeKind.RESULT.value:
            if self.validation_result_SHA256 is None:
                raise ValueError("successful outcome requires validation result digest")
        if self.binding_SHA256 != _model_digest(
            REVIEW_VALIDATION_OUTCOME_BINDING_DIGEST_ALGORITHM,
            self,
            "binding_SHA256",
        ):
            raise ValueError("execution outcome binding digest mismatch")
        return self


class ReviewValidationLoopRequest(_ReviewValidationModel):
    schema_version: Literal[1] = REVIEW_VALIDATION_LOOP_SCHEMA_VERSION
    policy_id: Literal["pepper-review-validation-loop-v1"] = (
        REVIEW_VALIDATION_LOOP_POLICY_ID
    )
    runtime_boundary_classification: Literal[
        ReviewValidationRuntimeBoundary.REVIEW_POST_EXECUTION_ONLY
    ] = ReviewValidationRuntimeBoundary.REVIEW_POST_EXECUTION_ONLY
    P18_4_result: DependencyAwareQueueIntegrationResult
    P18_4_result_SHA256: DigestText
    queue_result_SHA256: DigestText
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    TicketSpec_SHA256: DigestText
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    approval_decision_SHA256: DigestText
    dependency_plan_SHA256: DigestText
    expected_workflow_state: Literal[GovernedWorkflowState.QUEUED]
    outcome_envelope: OutcomeEnvelope
    execution_outcome_SHA256: DigestText
    diff_artifact_review_result: DiffArtifactReviewResult
    diff_artifact_review_SHA256: DigestText
    human_git_handoff_result: GitHandoffResult | None = None
    human_git_handoff_result_SHA256: DigestText | None = None
    prior_review_result_SHA256: DigestText | None = None
    prior_review_decision: ReviewValidationLoopDecision | None = None
    requested_retry: Literal[False] = False
    requested_rollback: Literal[False] = False
    requested_autonomous_correction: Literal[False] = False
    request_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_request(self) -> ReviewValidationLoopRequest:
        if self.request_SHA256 != _model_digest(
            REVIEW_VALIDATION_REQUEST_DIGEST_ALGORITHM,
            self,
            "request_SHA256",
        ):
            raise ValueError("review loop request digest mismatch")
        if (
            self.human_git_handoff_result is None
            and self.human_git_handoff_result_SHA256 is not None
        ):
            raise ValueError("handoff digest requires handoff result")
        if (
            self.human_git_handoff_result is not None
            and self.human_git_handoff_result_SHA256
            != self.human_git_handoff_result.result_SHA256
        ):
            raise ValueError("handoff digest mismatch")
        if (
            self.prior_review_result_SHA256 is None
            and self.prior_review_decision is not None
        ):
            raise ValueError("prior review decision requires prior digest")
        return self


class ReviewValidationFinding(_ReviewValidationModel):
    finding_id: FindingIdentifier
    severity: ReviewValidationFindingSeverity
    code: ReviewValidationFindingCode
    message: BoundedText
    evidence_SHA256: DigestText | None = None
    finding_SHA256: DigestText

    @field_validator("message", mode="after")
    @classmethod
    def _validate_message(cls, value: str) -> str:
        return _validate_safe_text(value, "review validation finding")

    @model_validator(mode="after")
    def _validate_finding(self) -> ReviewValidationFinding:
        if self.finding_SHA256 != _model_digest(
            REVIEW_VALIDATION_FINDING_DIGEST_ALGORITHM,
            self,
            "finding_SHA256",
        ):
            raise ValueError("review validation finding digest mismatch")
        return self


class ReviewValidationP18_6Handoff(_ReviewValidationModel):
    handoff_id: P18_6HandoffIdentifier
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    execution_outcome_classification: Literal["result", "failure", "cancellation"]
    validation_classification: BoundedText
    review_classification: BoundedText
    blocker_codes: tuple[BoundedText, ...] = Field(max_length=32)
    review_result_SHA256: DigestText
    workflow_state: GovernedWorkflowState
    retry_started: Literal[False] = False
    rollback_started: Literal[False] = False
    handoff_SHA256: DigestText

    @field_validator("validation_classification", "review_classification", mode="after")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.6 handoff")

    @field_validator("blocker_codes", mode="after")
    @classmethod
    def _validate_blockers(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("P18.6 blocker codes must be unique")
        for item in value:
            _validate_safe_text(item, "P18.6 blocker code")
        return value

    @model_validator(mode="after")
    def _validate_handoff(self) -> ReviewValidationP18_6Handoff:
        if self.retry_started or self.rollback_started:
            raise ValueError("P18.5 handoff must not start retry or rollback")
        if self.handoff_id != _p18_6_handoff_id(self):
            raise ValueError("P18.6 handoff ID mismatch")
        if self.handoff_SHA256 != _model_digest(
            REVIEW_VALIDATION_P18_6_HANDOFF_DIGEST_ALGORITHM,
            self,
            "handoff_SHA256",
        ):
            raise ValueError("P18.6 handoff digest mismatch")
        return self


class ReviewValidationSummary(_ReviewValidationModel):
    P18_4_continuation_valid: StrictBool
    project_identity_valid: StrictBool
    WorkPacket_binding_valid: StrictBool
    execution_outcome_binding_valid: StrictBool
    validation_integration_valid: StrictBool
    diff_artifact_review_valid: StrictBool
    review_decision_valid: StrictBool
    workflow_transition_valid: StrictBool
    human_Git_handoff_boundary_valid: StrictBool
    failure_handoff_valid: StrictBool
    cancellation_handling_valid: StrictBool
    replay_policy_valid: StrictBool
    no_retry_boundary_valid: StrictBool
    no_rollback_boundary_valid: StrictBool
    security_valid: StrictBool
    P18_6_handoff_valid: StrictBool
    information_finding_count: int = Field(ge=0, strict=True)
    warning_finding_count: int = Field(ge=0, strict=True)
    blocking_finding_count: int = Field(ge=0, strict=True)
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> ReviewValidationSummary:
        if self.warning_finding_count or self.blocking_finding_count:
            raise ValueError("P18.5 integration findings must not warn or block")
        expected = all((
            self.P18_4_continuation_valid,
            self.project_identity_valid,
            self.WorkPacket_binding_valid,
            self.execution_outcome_binding_valid,
            self.validation_integration_valid,
            self.diff_artifact_review_valid,
            self.review_decision_valid,
            self.workflow_transition_valid,
            self.human_Git_handoff_boundary_valid,
            self.failure_handoff_valid,
            self.cancellation_handling_valid,
            self.replay_policy_valid,
            self.no_retry_boundary_valid,
            self.no_rollback_boundary_valid,
            self.security_valid,
            self.P18_6_handoff_valid,
        ))
        if not expected:
            raise ValueError("P18.5 summary validity booleans must all be true")
        if self.summary_SHA256 != _model_digest(
            REVIEW_VALIDATION_SUMMARY_DIGEST_ALGORITHM,
            self,
            "summary_SHA256",
        ):
            raise ValueError("review validation summary digest mismatch")
        return self


class ReviewValidationLoopIntegrationResult(_ReviewValidationModel):
    schema_version: Literal[1] = REVIEW_VALIDATION_LOOP_SCHEMA_VERSION
    policy_id: Literal["pepper-review-validation-loop-v1"] = (
        REVIEW_VALIDATION_LOOP_POLICY_ID
    )
    integration_id: IntegrationIdentifier
    state: ReviewValidationLoopState
    decision: ReviewValidationLoopDecision
    request: ReviewValidationLoopRequest
    capability_reuse_assessments: tuple[
        ReviewValidationCapabilityReuseAssessment, ...
    ] = Field(min_length=12, max_length=16)
    execution_outcome_binding: ReviewValidationExecutionOutcomeBinding
    workflow_transition_results: tuple[GovernedWorkflowTransitionResult, ...] = Field(
        min_length=1,
        max_length=8,
    )
    resulting_workflow_snapshot: GovernedWorkflowSnapshot
    findings: tuple[ReviewValidationFinding, ...]
    summary: ReviewValidationSummary
    P18_6_handoff: ReviewValidationP18_6Handoff | None = None
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    execution_outcome_state: Literal["result", "failure", "cancellation"]
    execution_outcome_SHA256: DigestText
    validation_passed: StrictBool
    validation_result_SHA256: DigestText | None = None
    diff_artifact_review_passed: StrictBool
    diff_artifact_review_SHA256: DigestText
    review_accepted: StrictBool
    human_git_handoff_ready: StrictBool
    human_git_handoff_result_SHA256: DigestText | None = None
    P18_6_ready: StrictBool
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
    rollback_count: Literal[0]
    autonomous_correction_count: Literal[0]
    provider_dispatch_count: Literal[0]
    model_inference_count: Literal[0]
    Docker_commands_executed: Literal[0]
    Graphify_commands_executed: Literal[0]
    GBrain_calls: Literal[0]
    Paperclip_calls: Literal[0]
    Kanban_SQLite_canonical_authority: Literal[False]
    P17_validation_runner_reused: Literal[True]
    P17_outcome_envelopes_reused: Literal[True]
    P17_diff_artifact_review_reused: Literal[True]
    P17_human_Git_handoff_reused_or_deferred_with_evidence: Literal[True]
    duplicate_validation_runner_created: Literal[False]
    duplicate_outcome_envelope_created: Literal[False]
    duplicate_diff_review_engine_created: Literal[False]
    duplicate_artifact_review_engine_created: Literal[False]
    duplicate_Git_handoff_created: Literal[False]
    duplicate_WorkPacket_executor_created: Literal[False]
    duplicate_workflow_state_machine_created: Literal[False]
    duplicate_workspace_allocator_created: Literal[False]
    executor_calls_in_P18_5: Literal[0]
    workspace_allocation_calls_in_P18_5: Literal[0]
    validation_command_execution_count: Literal[0]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ReviewValidationLoopIntegrationResult:
        if self.result_SHA256 != _model_digest(
            REVIEW_VALIDATION_RESULT_DIGEST_ALGORITHM,
            self,
            "result_SHA256",
        ):
            raise ValueError("review validation result digest mismatch")
        if self.integration_id != _integration_id_from_record(
            self.model_dump(mode="json", exclude={"integration_id", "result_SHA256"})
        ):
            raise ValueError("integration ID mismatch")
        if (
            self.resulting_workflow_snapshot
            != self.workflow_transition_results[-1].resulting_snapshot
        ):
            raise ValueError("resulting workflow snapshot mismatch")
        if self.review_accepted != (
            self.decision is ReviewValidationLoopDecision.ACCEPT
        ):
            raise ValueError("review_accepted must derive from decision")
        if self.human_git_handoff_ready != self.review_accepted:
            raise ValueError("human Git handoff readiness derives from accept decision")
        if self.P18_6_ready != (
            self.decision is not ReviewValidationLoopDecision.ACCEPT
        ):
            raise ValueError("P18.6 readiness derives from non-accept decision")
        if self.P18_6_ready != (self.P18_6_handoff is not None):
            raise ValueError("P18.6 handoff presence mismatch")
        if (
            self.human_git_handoff_ready
            and self.human_git_handoff_result_SHA256 is None
        ):
            raise ValueError("accepted review requires human Git handoff digest")
        if self.decision is ReviewValidationLoopDecision.ACCEPT:
            if not self.validation_passed or not self.diff_artifact_review_passed:
                raise ValueError("accept requires validation and diff review pass")
        if (
            self.validation_result_SHA256
            != self.execution_outcome_binding.validation_result_SHA256
        ):
            raise ValueError("validation result digest mismatch")
        if (
            self.execution_outcome_SHA256
            != self.execution_outcome_binding.execution_outcome_SHA256
        ):
            raise ValueError("outcome digest mismatch")
        return self


def build_canonical_p18_review_validation_request(
    *,
    P18_4_result: DependencyAwareQueueIntegrationResult,
    outcome_envelope: OutcomeEnvelope,
    diff_artifact_review_result: DiffArtifactReviewResult,
    human_git_handoff_result: GitHandoffResult | None = None,
    prior_review_result_SHA256: str | None = None,
    prior_review_decision: ReviewValidationLoopDecision | None = None,
) -> ReviewValidationLoopRequest:
    _validate_p18_4_admit(P18_4_result)
    candidate = P18_4_result.queue_candidate
    selected = _selected_outcome(outcome_envelope)
    request = _make_model(
        ReviewValidationLoopRequest,
        "request_SHA256",
        REVIEW_VALIDATION_REQUEST_DIGEST_ALGORITHM,
        P18_4_result=P18_4_result,
        P18_4_result_SHA256=P18_4_result.result_SHA256,
        queue_result_SHA256=P18_4_result.queue_result_SHA256,
        project_id=candidate.project_id,
        macroproject_id=candidate.macroproject_id,
        ticket_id=candidate.ticket_id,
        TicketSpec_SHA256=candidate.TicketSpec_SHA256,
        WorkPacket_ID=candidate.WorkPacket_ID,
        WorkPacket_SHA256=candidate.WorkPacket_SHA256,
        approval_decision_SHA256=candidate.approval_decision_SHA256,
        dependency_plan_SHA256=candidate.dependency_plan_SHA256,
        expected_workflow_state=GovernedWorkflowState.QUEUED,
        outcome_envelope=outcome_envelope,
        execution_outcome_SHA256=outcome_envelope.envelope_SHA256,
        diff_artifact_review_result=diff_artifact_review_result,
        diff_artifact_review_SHA256=diff_artifact_review_result.result_SHA256,
        human_git_handoff_result=human_git_handoff_result,
        human_git_handoff_result_SHA256=human_git_handoff_result.result_SHA256
        if human_git_handoff_result is not None
        else None,
        prior_review_result_SHA256=prior_review_result_SHA256,
        prior_review_decision=prior_review_decision,
        requested_retry=False,
        requested_rollback=False,
        requested_autonomous_correction=False,
    )
    validate_review_validation_loop_request(request)
    if selected.work_packet_id != candidate.WorkPacket_ID:
        raise ReviewValidationLoopIntegrityError("outcome WorkPacket ID mismatch")
    return request


def validate_review_validation_loop_request(
    request: ReviewValidationLoopRequest,
) -> None:
    try:
        validated = ReviewValidationLoopRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ReviewValidationLoopValidationError("invalid P18.5 request") from exc
    _validate_replay_policy(validated)
    _validate_p18_4_admit(validated.P18_4_result)
    _validate_p18_4_request_bindings(validated)
    _validate_p17_evidence_bindings(validated)


def build_review_validation_loop_integration(
    request: ReviewValidationLoopRequest,
) -> ReviewValidationLoopIntegrationResult:
    validate_review_validation_loop_request(request)
    validated = ReviewValidationLoopRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    outcome_binding = _build_outcome_binding(validated)
    validation_passed = _validation_passed(outcome_binding)
    diff_review_passed = _diff_artifact_review_passed(
        validated.diff_artifact_review_result,
        outcome_binding,
    )
    decision = _derive_decision(
        outcome_binding=outcome_binding,
        validation_passed=validation_passed,
        diff_artifact_review_passed=diff_review_passed,
        human_git_handoff_result=validated.human_git_handoff_result,
    )
    workflow_results = _build_workflow_transitions(validated, decision, outcome_binding)
    if not all(result.accepted for result in workflow_results):
        raise ReviewValidationLoopStateError("P18.0 review transition rejected")
    p18_6_handoff = _build_p18_6_handoff(
        request=validated,
        decision=decision,
        outcome_binding=outcome_binding,
        resulting_workflow_state=workflow_results[-1].resulting_snapshot.current_state,
    )
    findings = _build_findings(
        decision=decision,
        outcome_binding=outcome_binding,
        validation_passed=validation_passed,
        diff_artifact_review_passed=diff_review_passed,
    )
    summary = _build_summary(findings, decision)
    accepted = decision is ReviewValidationLoopDecision.ACCEPT
    result_values = {
        "schema_version": REVIEW_VALIDATION_LOOP_SCHEMA_VERSION,
        "policy_id": REVIEW_VALIDATION_LOOP_POLICY_ID,
        "state": _state_for_decision(decision),
        "decision": decision,
        "request": validated,
        "capability_reuse_assessments": build_review_validation_reuse_matrix(),
        "execution_outcome_binding": outcome_binding,
        "workflow_transition_results": workflow_results,
        "resulting_workflow_snapshot": workflow_results[-1].resulting_snapshot,
        "findings": findings,
        "summary": summary,
        "P18_6_handoff": p18_6_handoff,
        "project_id": _CANONICAL_PROJECT_ID,
        "macroproject_id": _CANONICAL_MACROPROJECT_ID,
        "ticket_id": _CANONICAL_TICKET_ID,
        "WorkPacket_ID": validated.WorkPacket_ID,
        "WorkPacket_SHA256": validated.WorkPacket_SHA256,
        "execution_outcome_state": outcome_binding.execution_outcome_state,
        "execution_outcome_SHA256": outcome_binding.execution_outcome_SHA256,
        "validation_passed": validation_passed,
        "validation_result_SHA256": outcome_binding.validation_result_SHA256,
        "diff_artifact_review_passed": diff_review_passed,
        "diff_artifact_review_SHA256": validated.diff_artifact_review_SHA256,
        "review_accepted": accepted,
        "human_git_handoff_ready": accepted,
        "human_git_handoff_result_SHA256": validated.human_git_handoff_result_SHA256,
        "P18_6_ready": not accepted,
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
        "rollback_count": 0,
        "autonomous_correction_count": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "GBrain_calls": 0,
        "Paperclip_calls": 0,
        "Kanban_SQLite_canonical_authority": False,
        "P17_validation_runner_reused": True,
        "P17_outcome_envelopes_reused": True,
        "P17_diff_artifact_review_reused": True,
        "P17_human_Git_handoff_reused_or_deferred_with_evidence": True,
        "duplicate_validation_runner_created": False,
        "duplicate_outcome_envelope_created": False,
        "duplicate_diff_review_engine_created": False,
        "duplicate_artifact_review_engine_created": False,
        "duplicate_Git_handoff_created": False,
        "duplicate_WorkPacket_executor_created": False,
        "duplicate_workflow_state_machine_created": False,
        "duplicate_workspace_allocator_created": False,
        "executor_calls_in_P18_5": 0,
        "workspace_allocation_calls_in_P18_5": 0,
        "validation_command_execution_count": 0,
    }
    result = _make_model(
        ReviewValidationLoopIntegrationResult,
        "result_SHA256",
        REVIEW_VALIDATION_RESULT_DIGEST_ALGORITHM,
        integration_id=_integration_id_from_record(result_values),
        **result_values,
    )
    validate_review_validation_loop_integration_result(result)
    return result


def validate_review_validation_loop_integration_result(
    result: ReviewValidationLoopIntegrationResult,
) -> None:
    try:
        validated = ReviewValidationLoopIntegrationResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ReviewValidationLoopValidationError("invalid P18.5 result") from exc
    validate_review_validation_loop_request(validated.request)
    _validate_result_bindings(validated)


def summarize_review_validation_loop_integration(
    result: ReviewValidationLoopIntegrationResult,
) -> ReviewValidationSummary:
    validate_review_validation_loop_integration_result(result)
    return result.summary


def build_review_validation_reuse_matrix() -> tuple[
    ReviewValidationCapabilityReuseAssessment, ...
]:
    rows = (
        (
            "validation command runner",
            "hermes_cli/agent_platform/work_packet/validation_command_runner.py",
            "ValidationCommandRunnerResult",
            "Binds exact human-authorized validation command completion evidence.",
            "P17.4 may execute commands only through accepted runner authority; P18.5 consumes result evidence only.",
        ),
        (
            "validation command result",
            "hermes_cli/agent_platform/work_packet/validation_command_runner.py",
            "ValidationCommandExecutionResult",
            "Records bounded command disposition and stream digests.",
            "P17.4 owns validation command execution evidence.",
        ),
        (
            "terminal outcome envelopes",
            "hermes_cli/agent_platform/work_packet/outcome_envelopes.py",
            "OutcomeEnvelope",
            "Projects result, failure and cancellation evidence into one terminal envelope.",
            "P17.5 owns terminal outcome classification and retry-not-authorized posture.",
        ),
        (
            "result failure cancellation handling",
            "hermes_cli/agent_platform/work_packet/outcome_envelopes.py",
            "OutcomeEnvelopeKind",
            "Provides canonical result, failure and cancellation values.",
            "P17.5 owns terminal outcome enums; P18.5 does not create another terminal enum.",
        ),
        (
            "diff review",
            "hermes_cli/agent_platform/work_packet/diff_artifact_review.py",
            "DiffReviewVerdict",
            "Classifies observed path mutations against WorkPacket expectations.",
            "P17.6 owns diff review verdicts and blockers.",
        ),
        (
            "artifact review",
            "hermes_cli/agent_platform/work_packet/diff_artifact_review.py",
            "ArtifactReviewVerdict",
            "Classifies artifact observations without filesystem inspection.",
            "P17.6 owns artifact review verdicts and blockers.",
        ),
        (
            "review findings",
            "hermes_cli/agent_platform/work_packet/diff_artifact_review.py",
            "ReviewFinding",
            "Carries bounded info, warning and blocking review findings.",
            "P17.6 owns review finding codes and severity.",
        ),
        (
            "review decision",
            "hermes_cli/agent_platform/work_packet/diff_artifact_review.py",
            "AggregateReviewState",
            "Summarizes review completion or blockage.",
            "P17.6 state feeds P18.5 decision synthesis.",
        ),
        (
            "human Git handoff",
            "hermes_cli/agent_platform/work_packet/human_git_handoff.py",
            "GitHandoffResult",
            "Builds a human-only non-executing Git handoff package.",
            "P17.7 owns handoff rendering and Git authority boundary.",
        ),
        (
            "execution result binding",
            "hermes_cli/agent_platform/work_packet/single_agent_execution.py",
            "SingleAgentExecutionResult",
            "Binds completed single-agent WorkPacket execution evidence.",
            "P17.3 owns executor outcome evidence; P18.5 consumes only envelope digests.",
        ),
        (
            "workflow transitions",
            "hermes_cli/agent_platform/workflow/governed_state_machine.py",
            "GovernedWorkflowTransitionResult",
            "Records accepted governed state transitions.",
            "P18.0 owns the state machine; P18.5 adds no duplicate state machine.",
        ),
        (
            "cancellation semantics",
            "hermes_cli/agent_platform/work_packet/outcome_envelopes.py",
            "CancellationEnvelope",
            "Preserves cancellation as terminal evidence without false acceptance.",
            "P17.5 owns cancellation envelope semantics.",
        ),
    )
    return tuple(
        _make_model(
            ReviewValidationCapabilityReuseAssessment,
            "assessment_SHA256",
            REVIEW_VALIDATION_CAPABILITY_DIGEST_ALGORITHM,
            capability=capability,
            source_file=source_file,
            symbol=symbol,
            purpose=purpose,
            current_authority=current_authority,
            suitable_for_P18_5=True,
            decision=ReviewValidationCapabilityDecision.RETAIN,
            customized=False,
            duplicate_created=False,
            reason="Retained accepted P17/P18 contract; P18.5 only binds deterministic evidence.",
        )
        for capability, source_file, symbol, purpose, current_authority in rows
    )


def _validate_p18_4_admit(result: DependencyAwareQueueIntegrationResult) -> None:
    try:
        validate_dependency_aware_queue_integration_result(result)
    except ValueError as exc:
        raise ReviewValidationLoopValidationError("invalid P18.4 continuation") from exc
    if result.state is not DependencyAwareQueueState.COMPLETED:
        raise ReviewValidationLoopStateError("P18.4 result must be completed")
    if result.decision is not DependencyAwareQueueDecision.ADMIT:
        raise ReviewValidationLoopStateError("P18.5 rejects blocked P18.4 handoffs")
    if not result.approval_granted:
        raise ReviewValidationLoopPolicyError("P18.4 approval must be granted")
    if not result.dependencies_satisfied or not result.queue_eligible:
        raise ReviewValidationLoopPolicyError("P18.4 dependencies must be satisfied")
    if not result.queue_admitted or not result.P18_5_ready:
        raise ReviewValidationLoopPolicyError("P18.4 result must be P18.5-ready")
    if result.execution_started or result.WorkPacket_execution_started:
        raise ReviewValidationLoopPolicyError("P18.4 must not start execution")
    if (
        result.resulting_workflow_snapshot.current_state
        is not GovernedWorkflowState.QUEUED
    ):
        raise ReviewValidationLoopStateError("P18.4 admitted state must be queued")
    candidate = result.queue_candidate
    if (
        candidate.project_id != _CANONICAL_PROJECT_ID
        or candidate.macroproject_id != _CANONICAL_MACROPROJECT_ID
        or candidate.ticket_id != _CANONICAL_TICKET_ID
    ):
        raise ReviewValidationLoopIntegrityError("P18.4 identity mismatch")


def _validate_replay_policy(request: ReviewValidationLoopRequest) -> None:
    if request.prior_review_result_SHA256 is not None:
        raise ReviewValidationLoopStateError(
            "prior P18.5 review evidence blocks replay"
        )


def _validate_p18_4_request_bindings(request: ReviewValidationLoopRequest) -> None:
    result = request.P18_4_result
    candidate = result.queue_candidate
    expected = {
        "P18_4_result_SHA256": result.result_SHA256,
        "queue_result_SHA256": result.queue_result_SHA256,
        "TicketSpec_SHA256": candidate.TicketSpec_SHA256,
        "WorkPacket_ID": candidate.WorkPacket_ID,
        "WorkPacket_SHA256": candidate.WorkPacket_SHA256,
        "approval_decision_SHA256": candidate.approval_decision_SHA256,
        "dependency_plan_SHA256": candidate.dependency_plan_SHA256,
    }
    for field, value in expected.items():
        if getattr(request, field) != value:
            raise ReviewValidationLoopIntegrityError(f"{field} mismatch")
    if request.expected_workflow_state is not GovernedWorkflowState.QUEUED:
        raise ReviewValidationLoopStateError("expected workflow state must be queued")


def _validate_p17_evidence_bindings(request: ReviewValidationLoopRequest) -> None:
    try:
        validate_outcome_envelope(request.outcome_envelope)
        validate_diff_artifact_review_result(request.diff_artifact_review_result)
        if request.human_git_handoff_result is not None:
            validate_human_git_handoff_result(request.human_git_handoff_result)
    except ValueError as exc:
        raise ReviewValidationLoopValidationError(
            "invalid P17 review evidence"
        ) from exc
    selected = _selected_outcome(request.outcome_envelope)
    if request.execution_outcome_SHA256 != request.outcome_envelope.envelope_SHA256:
        raise ReviewValidationLoopIntegrityError("execution outcome digest mismatch")
    if (
        request.diff_artifact_review_SHA256
        != request.diff_artifact_review_result.result_SHA256
    ):
        raise ReviewValidationLoopIntegrityError("diff artifact review digest mismatch")
    if selected.work_packet_id != request.WorkPacket_ID:
        raise ReviewValidationLoopIntegrityError("outcome WorkPacket ID mismatch")
    if selected.work_packet_SHA256 != request.WorkPacket_SHA256:
        raise ReviewValidationLoopIntegrityError("outcome WorkPacket SHA mismatch")
    review = request.diff_artifact_review_result
    if review.work_packet_id != request.WorkPacket_ID:
        raise ReviewValidationLoopIntegrityError("review WorkPacket ID mismatch")
    if review.work_packet_SHA256 != request.WorkPacket_SHA256:
        raise ReviewValidationLoopIntegrityError("review WorkPacket SHA mismatch")
    if review.outcome_SHA256 != request.outcome_envelope.envelope_SHA256:
        raise ReviewValidationLoopIntegrityError("review outcome digest mismatch")
    if request.human_git_handoff_result is not None:
        handoff = request.human_git_handoff_result
        if handoff.work_packet_id != request.WorkPacket_ID:
            raise ReviewValidationLoopIntegrityError("handoff WorkPacket ID mismatch")
        if handoff.work_packet_SHA256 != request.WorkPacket_SHA256:
            raise ReviewValidationLoopIntegrityError("handoff WorkPacket SHA mismatch")
        if handoff.outcome_SHA256 != request.outcome_envelope.envelope_SHA256:
            raise ReviewValidationLoopIntegrityError("handoff outcome digest mismatch")
        if handoff.review_SHA256 != review.result_SHA256:
            raise ReviewValidationLoopIntegrityError("handoff review digest mismatch")
        if any((
            handoff.Git_commands_executed,
            handoff.staging_performed,
            handoff.commit_performed,
            handoff.push_performed,
            handoff.automatic_cleanup_authorized,
            handoff.automatic_rollback_authorized,
            handoff.automatic_staging_authorized,
            handoff.automatic_commit_authorized,
            handoff.automatic_push_authorized,
            handoff.provider_dispatch_count,
            handoff.model_inference_count,
        )):
            raise ReviewValidationLoopPolicyError("handoff must be non-executing")


def _selected_outcome(envelope: OutcomeEnvelope):
    selected = tuple(
        item
        for item in (
            envelope.result_envelope,
            envelope.failure_envelope,
            envelope.cancellation_envelope,
        )
        if item is not None
    )
    if len(selected) != 1:
        raise ReviewValidationLoopValidationError(
            "outcome envelope must select one kind"
        )
    return selected[0]


def _terminal_evidence(envelope: OutcomeEnvelope):
    return _selected_outcome(envelope).terminal_evidence


def _build_outcome_binding(
    request: ReviewValidationLoopRequest,
) -> ReviewValidationExecutionOutcomeBinding:
    selected = _selected_outcome(request.outcome_envelope)
    terminal = selected.terminal_evidence
    validation_result = terminal.validation_command_runner_result_SHA256
    validation_session = terminal.validation_command_runner_session_SHA256
    if validation_result is None:
        validation_result = validation_session
    return _make_model(
        ReviewValidationExecutionOutcomeBinding,
        "binding_SHA256",
        REVIEW_VALIDATION_OUTCOME_BINDING_DIGEST_ALGORITHM,
        project_id=_CANONICAL_PROJECT_ID,
        macroproject_id=_CANONICAL_MACROPROJECT_ID,
        ticket_id=_CANONICAL_TICKET_ID,
        WorkPacket_ID=request.WorkPacket_ID,
        WorkPacket_SHA256=request.WorkPacket_SHA256,
        execution_outcome_state=request.outcome_envelope.envelope_kind.value,
        execution_outcome_SHA256=request.outcome_envelope.envelope_SHA256,
        terminal_stage=terminal.terminal_stage,
        terminal_state=terminal.terminal_state,
        failure_category=terminal.failure_category,
        single_agent_result_SHA256=terminal.single_agent_result_SHA256,
        validation_result_SHA256=validation_result,
        validation_session_SHA256=validation_session,
        terminal_evidence_SHA256=terminal.terminal_evidence_SHA256,
        execution_successful=_execution_successful(request.outcome_envelope),
        execution_cancelled=request.outcome_envelope.envelope_kind
        is OutcomeEnvelopeKind.CANCELLATION,
    )


def _execution_successful(envelope: OutcomeEnvelope) -> bool:
    terminal = _terminal_evidence(envelope)
    if envelope.envelope_kind is OutcomeEnvelopeKind.RESULT:
        return True
    return (
        envelope.envelope_kind is OutcomeEnvelopeKind.FAILURE
        and terminal.terminal_stage is OutcomeStage.VALIDATION_COMMAND_RUNNER
        and terminal.single_agent_result_SHA256 is not None
    )


def _validation_passed(binding: ReviewValidationExecutionOutcomeBinding) -> bool:
    return (
        binding.execution_outcome_state == OutcomeEnvelopeKind.RESULT.value
        and binding.terminal_stage is OutcomeStage.VALIDATION_COMMAND_RUNNER
        and binding.terminal_state is OutcomeTerminalState.COMPLETED
        and binding.validation_result_SHA256 is not None
    )


def _diff_artifact_review_passed(
    review: DiffArtifactReviewResult,
    outcome_binding: ReviewValidationExecutionOutcomeBinding,
) -> bool:
    return (
        outcome_binding.execution_outcome_state == OutcomeEnvelopeKind.RESULT.value
        and review.state is AggregateReviewState.COMPLETED
        and review.diff_verdict is DiffReviewVerdict.ACCEPTED
        and review.artifact_verdict is ArtifactReviewVerdict.ACCEPTED
        and review.diff_artifact_review_requirement_satisfied
    )


def _derive_decision(
    *,
    outcome_binding: ReviewValidationExecutionOutcomeBinding,
    validation_passed: bool,
    diff_artifact_review_passed: bool,
    human_git_handoff_result: GitHandoffResult | None,
) -> ReviewValidationLoopDecision:
    if (
        outcome_binding.execution_outcome_state
        == OutcomeEnvelopeKind.CANCELLATION.value
    ):
        return ReviewValidationLoopDecision.CANCELLED
    if (
        outcome_binding.execution_outcome_state == OutcomeEnvelopeKind.FAILURE.value
        and outcome_binding.terminal_stage is OutcomeStage.SINGLE_AGENT_EXECUTION
    ):
        return ReviewValidationLoopDecision.INCIDENT
    if not validation_passed or not diff_artifact_review_passed:
        return ReviewValidationLoopDecision.NEEDS_CORRECTION
    if human_git_handoff_result is None:
        raise ReviewValidationLoopPolicyError("accepted review requires P17.7 handoff")
    if human_git_handoff_result.state is not GitHandoffState.COMPLETED:
        raise ReviewValidationLoopStateError("accepted handoff must be completed")
    if human_git_handoff_result.decision is not GitHandoffDecision.APPROVED:
        raise ReviewValidationLoopStateError("accepted handoff must be approved")
    if not human_git_handoff_result.human_git_handoff_requirement_satisfied:
        raise ReviewValidationLoopPolicyError(
            "human Git handoff requirement not satisfied"
        )
    return ReviewValidationLoopDecision.ACCEPT


def _build_workflow_transitions(
    request: ReviewValidationLoopRequest,
    decision: ReviewValidationLoopDecision,
    outcome_binding: ReviewValidationExecutionOutcomeBinding,
) -> tuple[GovernedWorkflowTransitionResult, ...]:
    snapshot = request.P18_4_result.resulting_workflow_snapshot
    transitions: list[GovernedWorkflowTransitionResult] = []

    def advance(
        trigger: WorkflowTransitionTrigger,
        authority: WorkflowTransitionAuthority,
        evidence_refs: tuple[str, ...],
        runtime_state: str,
        *,
        workspace: bool = True,
        worker: bool = True,
    ) -> None:
        nonlocal snapshot
        projection = build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.WORK_PACKET,
            runtime_state=runtime_state,
            task_id=request.WorkPacket_ID if worker else None,
            board_or_queue_id=None,
            worker_id_present=worker,
            workspace_binding_present=workspace,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
        transition_request = GovernedWorkflowTransitionRequest(
            current_snapshot=snapshot,
            trigger=trigger,
            authority=authority,
            evidence_refs=evidence_refs,
            runtime_projection=projection,
        )
        validate_governed_workflow_transition_request(transition_request)
        result = build_governed_workflow_transition(transition_request)
        transitions.append(result)
        snapshot = result.resulting_snapshot

    if decision is ReviewValidationLoopDecision.CANCELLED:
        advance(
            WorkflowTransitionTrigger.CANCEL_REQUESTED,
            WorkflowTransitionAuthority.HUMAN,
            ("human_cancellation_request",),
            "cancelled",
            workspace=False,
            worker=False,
        )
        return tuple(transitions)

    advance(
        WorkflowTransitionTrigger.DEPENDENCIES_READY,
        WorkflowTransitionAuthority.POLICY,
        ("queue_eligible",),
        "allocating",
        workspace=False,
        worker=False,
    )
    advance(
        WorkflowTransitionTrigger.WORKSPACE_ALLOCATED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("workspace_allocation_result", "tool_permission_profile"),
        "ready_to_execute",
        workspace=True,
        worker=False,
    )
    advance(
        WorkflowTransitionTrigger.EXECUTION_STARTED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("single_agent_execution_authorization",),
        "executing",
    )
    if decision is ReviewValidationLoopDecision.INCIDENT:
        advance(
            WorkflowTransitionTrigger.EXECUTION_FAILED,
            WorkflowTransitionAuthority.GOVERNED_RUNTIME,
            ("outcome_envelope",),
            "failed",
        )
        return tuple(transitions)
    advance(
        WorkflowTransitionTrigger.EXECUTION_COMPLETED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("single_agent_execution_result",),
        "validating",
    )
    if not _validation_passed(outcome_binding):
        advance(
            WorkflowTransitionTrigger.VALIDATION_FAILED,
            WorkflowTransitionAuthority.GOVERNED_RUNTIME,
            ("validation_failure_evidence",),
            "awaiting_correction",
        )
        return tuple(transitions)
    advance(
        WorkflowTransitionTrigger.VALIDATION_COMPLETED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("validation_command_runner_result",),
        "reviewing",
    )
    if decision is ReviewValidationLoopDecision.NEEDS_CORRECTION:
        advance(
            WorkflowTransitionTrigger.REVIEW_REJECTED,
            WorkflowTransitionAuthority.GOVERNED_RUNTIME,
            ("review_rejection_evidence",),
            "awaiting_correction",
        )
        return tuple(transitions)
    advance(
        WorkflowTransitionTrigger.REVIEW_ACCEPTED,
        WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        ("diff_artifact_review_result",),
        "awaiting_human_approval",
    )
    advance(
        WorkflowTransitionTrigger.HUMAN_APPROVED,
        WorkflowTransitionAuthority.HUMAN,
        ("human_result_approval",),
        "awaiting_human_git_handoff",
        worker=False,
    )
    return tuple(transitions)


def _build_p18_6_handoff(
    *,
    request: ReviewValidationLoopRequest,
    decision: ReviewValidationLoopDecision,
    outcome_binding: ReviewValidationExecutionOutcomeBinding,
    resulting_workflow_state: GovernedWorkflowState,
) -> ReviewValidationP18_6Handoff | None:
    if decision is ReviewValidationLoopDecision.ACCEPT:
        return None
    validation_classification = (
        "validation_passed"
        if _validation_passed(outcome_binding)
        else "validation_failed_or_unavailable"
    )
    review_classification = "review_not_accepted"
    blockers = _blocker_codes(decision, request, outcome_binding)
    data = {
        "project_id": _CANONICAL_PROJECT_ID,
        "macroproject_id": _CANONICAL_MACROPROJECT_ID,
        "ticket_id": _CANONICAL_TICKET_ID,
        "WorkPacket_ID": request.WorkPacket_ID,
        "WorkPacket_SHA256": request.WorkPacket_SHA256,
        "execution_outcome_classification": outcome_binding.execution_outcome_state,
        "validation_classification": validation_classification,
        "review_classification": review_classification,
        "blocker_codes": blockers,
        "review_result_SHA256": request.diff_artifact_review_SHA256,
        "workflow_state": resulting_workflow_state,
        "retry_started": False,
        "rollback_started": False,
    }
    return _make_model(
        ReviewValidationP18_6Handoff,
        "handoff_SHA256",
        REVIEW_VALIDATION_P18_6_HANDOFF_DIGEST_ALGORITHM,
        handoff_id=_p18_6_handoff_id_from_record(data),
        **data,
    )


def _blocker_codes(
    decision: ReviewValidationLoopDecision,
    request: ReviewValidationLoopRequest,
    outcome_binding: ReviewValidationExecutionOutcomeBinding,
) -> tuple[str, ...]:
    if decision is ReviewValidationLoopDecision.CANCELLED:
        return ("execution_cancelled",)
    if decision is ReviewValidationLoopDecision.INCIDENT:
        return (outcome_binding.failure_category.value,)
    blockers: list[str] = []
    if not _validation_passed(outcome_binding):
        blockers.append(outcome_binding.failure_category.value)
    review = request.diff_artifact_review_result
    if review.diff_verdict is not DiffReviewVerdict.ACCEPTED:
        blockers.append(f"diff_{review.diff_verdict.value}")
    if review.artifact_verdict is not ArtifactReviewVerdict.ACCEPTED:
        blockers.append(f"artifact_{review.artifact_verdict.value}")
    return tuple(sorted(frozenset(blockers or ["review_not_accepted"])))


def _build_findings(
    *,
    decision: ReviewValidationLoopDecision,
    outcome_binding: ReviewValidationExecutionOutcomeBinding,
    validation_passed: bool,
    diff_artifact_review_passed: bool,
) -> tuple[ReviewValidationFinding, ...]:
    records = (
        (
            ReviewValidationFindingCode.P18_4_CONTINUATION_VALID,
            "P18.4 admitted queue handoff is valid for P18.5.",
            None,
        ),
        (
            ReviewValidationFindingCode.P17_OUTCOME_ENVELOPE_REUSED,
            "P17.5 outcome envelope is reused without another outcome model.",
            outcome_binding.execution_outcome_SHA256,
        ),
        (
            ReviewValidationFindingCode.P17_VALIDATION_RUNNER_REUSED,
            "P17.4 validation evidence is consumed through P17.5 outcome binding.",
            outcome_binding.validation_result_SHA256,
        ),
        (
            ReviewValidationFindingCode.P17_DIFF_ARTIFACT_REVIEW_REUSED,
            "P17.6 diff and artifact review evidence is reused.",
            None,
        ),
        (
            ReviewValidationFindingCode.P17_HUMAN_GIT_HANDOFF_REUSED,
            "P17.7 human Git handoff is reused for accept or deferred for non-accept.",
            None,
        ),
        (
            ReviewValidationFindingCode.WORKFLOW_TRANSITION_VALID,
            "P18.0 governed workflow transition chain is valid.",
            None,
        ),
        (
            ReviewValidationFindingCode.REVIEW_DECISION_VALID,
            f"P18.5 review decision is {decision.value}.",
            None,
        ),
        (
            ReviewValidationFindingCode.P18_6_HANDOFF_VALID,
            "P18.6 handoff posture is deterministic for non-accept decisions.",
            None,
        ),
        (
            ReviewValidationFindingCode.NO_RETRY_BOUNDARY_VALID,
            "P18.5 starts no retry or automatic requeue.",
            None,
        ),
        (
            ReviewValidationFindingCode.NO_ROLLBACK_BOUNDARY_VALID,
            "P18.5 starts no rollback.",
            None,
        ),
        (
            ReviewValidationFindingCode.SECURITY_BOUNDARY_VALID,
            "P18.5 stores bounded deterministic evidence only.",
            None,
        ),
        (
            ReviewValidationFindingCode.INTEGRATION_ACCEPTED,
            f"validation_passed={validation_passed}; diff_artifact_review_passed={diff_artifact_review_passed}.",
            None,
        ),
    )
    return tuple(
        _make_model(
            ReviewValidationFinding,
            "finding_SHA256",
            REVIEW_VALIDATION_FINDING_DIGEST_ALGORITHM,
            finding_id=f"RVIF-{index:03d}",
            severity=ReviewValidationFindingSeverity.INFO,
            code=code,
            message=message,
            evidence_SHA256=evidence,
        )
        for index, (code, message, evidence) in enumerate(records, start=1)
    )


def _build_summary(
    findings: tuple[ReviewValidationFinding, ...],
    decision: ReviewValidationLoopDecision,
) -> ReviewValidationSummary:
    info = sum(
        1
        for finding in findings
        if finding.severity is ReviewValidationFindingSeverity.INFO
    )
    warnings = sum(
        1
        for finding in findings
        if finding.severity is ReviewValidationFindingSeverity.WARNING
    )
    blockers = sum(
        1
        for finding in findings
        if finding.severity is ReviewValidationFindingSeverity.BLOCKING
    )
    return _make_model(
        ReviewValidationSummary,
        "summary_SHA256",
        REVIEW_VALIDATION_SUMMARY_DIGEST_ALGORITHM,
        P18_4_continuation_valid=True,
        project_identity_valid=True,
        WorkPacket_binding_valid=True,
        execution_outcome_binding_valid=True,
        validation_integration_valid=True,
        diff_artifact_review_valid=True,
        review_decision_valid=True,
        workflow_transition_valid=True,
        human_Git_handoff_boundary_valid=True,
        failure_handoff_valid=True,
        cancellation_handling_valid=True,
        replay_policy_valid=True,
        no_retry_boundary_valid=True,
        no_rollback_boundary_valid=True,
        security_valid=True,
        P18_6_handoff_valid=True,
        information_finding_count=info,
        warning_finding_count=warnings,
        blocking_finding_count=blockers,
    )


def _state_for_decision(
    decision: ReviewValidationLoopDecision,
) -> ReviewValidationLoopState:
    if decision is ReviewValidationLoopDecision.ACCEPT:
        return ReviewValidationLoopState.COMPLETED
    if decision is ReviewValidationLoopDecision.NEEDS_CORRECTION:
        return ReviewValidationLoopState.CORRECTION_REQUIRED
    if decision is ReviewValidationLoopDecision.INCIDENT:
        return ReviewValidationLoopState.INCIDENT
    return ReviewValidationLoopState.CANCELLED


def _p18_6_handoff_id(value: ReviewValidationP18_6Handoff) -> str:
    return _p18_6_handoff_id_from_record(
        value.model_dump(mode="json", exclude={"handoff_id", "handoff_SHA256"})
    )


def _p18_6_handoff_id_from_record(record: object) -> str:
    digest = _digest_from_record(REVIEW_VALIDATION_ID_DIGEST_ALGORITHM, record)
    return f"RVH-P18-6-{digest[:12]}"


def _integration_id_from_record(record: object) -> str:
    digest = _digest_from_record(REVIEW_VALIDATION_ID_DIGEST_ALGORITHM, record)
    return f"RVI-P18-{digest[:12]}"


def _validate_result_bindings(result: ReviewValidationLoopIntegrationResult) -> None:
    request = result.request
    if (
        result.project_id != request.project_id
        or result.macroproject_id != request.macroproject_id
    ):
        raise ReviewValidationLoopIntegrityError("project identity mismatch")
    if result.ticket_id != request.ticket_id:
        raise ReviewValidationLoopIntegrityError("ticket identity mismatch")
    if result.WorkPacket_ID != request.WorkPacket_ID:
        raise ReviewValidationLoopIntegrityError("WorkPacket ID mismatch")
    if result.WorkPacket_SHA256 != request.WorkPacket_SHA256:
        raise ReviewValidationLoopIntegrityError("WorkPacket SHA mismatch")
    if result.diff_artifact_review_SHA256 != request.diff_artifact_review_SHA256:
        raise ReviewValidationLoopIntegrityError("diff review digest mismatch")
    if (
        result.human_git_handoff_result_SHA256
        != request.human_git_handoff_result_SHA256
    ):
        raise ReviewValidationLoopIntegrityError("handoff digest mismatch")
    if any((
        result.Git_commands_executed,
        result.staging_calls,
        result.commit_calls,
        result.push_calls,
        result.retry_execution_count,
        result.automatic_retry_count,
        result.automatic_requeue_count,
        result.rollback_count,
        result.autonomous_correction_count,
        result.provider_dispatch_count,
        result.model_inference_count,
        result.Docker_commands_executed,
        result.Graphify_commands_executed,
        result.GBrain_calls,
        result.Paperclip_calls,
        result.executor_calls_in_P18_5,
        result.workspace_allocation_calls_in_P18_5,
        result.validation_command_execution_count,
    )):
        raise ReviewValidationLoopPolicyError(
            "P18.5 result must not execute runtime actions"
        )


__all__ = (
    "REVIEW_VALIDATION_LOOP_SCHEMA_VERSION",
    "REVIEW_VALIDATION_LOOP_POLICY_ID",
    "REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION",
    "ReviewValidationRuntimeBoundary",
    "ReviewValidationCapabilityDecision",
    "ReviewValidationLoopDecision",
    "ReviewValidationLoopState",
    "ReviewValidationFindingSeverity",
    "ReviewValidationFindingCode",
    "ReviewValidationCapabilityReuseAssessment",
    "ReviewValidationExecutionOutcomeBinding",
    "ReviewValidationLoopRequest",
    "ReviewValidationFinding",
    "ReviewValidationSummary",
    "ReviewValidationP18_6Handoff",
    "ReviewValidationLoopIntegrationResult",
    "ReviewValidationLoopError",
    "ReviewValidationLoopInputError",
    "ReviewValidationLoopIntegrityError",
    "ReviewValidationLoopPolicyError",
    "ReviewValidationLoopStateError",
    "ReviewValidationLoopValidationError",
    "build_review_validation_reuse_matrix",
    "build_canonical_p18_review_validation_request",
    "validate_review_validation_loop_request",
    "build_review_validation_loop_integration",
    "validate_review_validation_loop_integration_result",
    "summarize_review_validation_loop_integration",
)
