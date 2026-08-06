"""Deterministic bounded terminal outcome envelopes for WorkPacket execution.

P17.5 projects already-terminal P17.3/P17.4 evidence into immutable result,
failure or cancellation envelopes. It has no execution, retry, fallback,
resubmission, filesystem, environment, network, Git, Docker or Graphify authority.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    model_validator,
)

from hermes_cli.agent_platform.work_packet.single_agent_execution import (
    SingleAgentActionDisposition,
    SingleAgentExecutionResult,
    SingleAgentExecutionSession,
    SingleAgentExecutionState,
    validate_single_agent_execution_result,
    validate_single_agent_execution_session,
)
from hermes_cli.agent_platform.work_packet.validation_command_runner import (
    ValidationCommandFailureReason,
    ValidationCommandRunnerResult,
    ValidationCommandRunnerSession,
    ValidationCommandRunnerState,
    validate_validation_command_runner_result,
    validate_validation_command_runner_session,
)

OUTCOME_ENVELOPE_SCHEMA_VERSION = 1
OUTCOME_ENVELOPE_POLICY_ID = (
    "pepper-deterministic-bounded-terminal-outcome-envelopes-v1"
)

DIAGNOSTIC_DIGEST_ALGORITHM = "agent-platform-outcome-diagnostic-projection-sha256-v1"
TERMINAL_EVIDENCE_DIGEST_ALGORITHM = (
    "agent-platform-outcome-terminal-evidence-sha256-v1"
)
RESULT_ENVELOPE_DIGEST_ALGORITHM = "agent-platform-result-envelope-sha256-v1"
FAILURE_ENVELOPE_DIGEST_ALGORITHM = "agent-platform-failure-envelope-sha256-v1"
CANCELLATION_ENVELOPE_DIGEST_ALGORITHM = (
    "agent-platform-cancellation-envelope-sha256-v1"
)
OUTCOME_ENVELOPE_DIGEST_ALGORITHM = "agent-platform-outcome-envelope-sha256-v1"
REQUEST_DIGEST_ALGORITHM = "agent-platform-outcome-envelope-request-sha256-v1"

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"

__all__ = (
    "OUTCOME_ENVELOPE_SCHEMA_VERSION",
    "OUTCOME_ENVELOPE_POLICY_ID",
    "OutcomeEnvelopeKind",
    "OutcomeStage",
    "OutcomeTerminalState",
    "OutcomeFailureCategory",
    "OutcomeRetryPosture",
    "OutcomeCancellationPoint",
    "OutcomeDiagnosticProjection",
    "OutcomeTerminalEvidence",
    "ResultEnvelope",
    "FailureEnvelope",
    "CancellationEnvelope",
    "OutcomeEnvelopeRequest",
    "OutcomeEnvelope",
    "OutcomeEnvelopeError",
    "OutcomeEnvelopeInputError",
    "OutcomeEnvelopeIntegrityError",
    "OutcomeEnvelopePolicyError",
    "OutcomeEnvelopeStateError",
    "OutcomeEnvelopeValidationError",
    "build_result_envelope",
    "build_failure_envelope",
    "build_cancellation_envelope",
    "build_outcome_envelope",
    "validate_outcome_envelope_request",
    "validate_outcome_envelope",
)


class OutcomeEnvelopeError(ValueError):
    """Base error for P17.5 outcome envelope failures."""


class OutcomeEnvelopeInputError(OutcomeEnvelopeError):
    """Raised when envelope inputs are structurally invalid."""


class OutcomeEnvelopeIntegrityError(OutcomeEnvelopeError):
    """Raised when deterministic envelope evidence fails integrity checks."""


class OutcomeEnvelopePolicyError(OutcomeEnvelopeError):
    """Raised when the P17.5 policy boundary is violated."""


class OutcomeEnvelopeStateError(OutcomeEnvelopeError):
    """Raised when terminal prerequisite state is missing or ambiguous."""


class OutcomeEnvelopeValidationError(OutcomeEnvelopeError):
    """Raised when a supplied envelope cannot be validated."""


class OutcomeEnvelopeKind(str, Enum):
    RESULT = "result"
    FAILURE = "failure"
    CANCELLATION = "cancellation"


class OutcomeStage(str, Enum):
    SINGLE_AGENT_EXECUTION = "single_agent_execution"
    VALIDATION_COMMAND_RUNNER = "validation_command_runner"


class OutcomeTerminalState(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class OutcomeFailureCategory(str, Enum):
    NONE = "none"
    SINGLE_AGENT_BLOCKED = "single_agent_blocked"
    SINGLE_AGENT_ACTION_DENIED = "single_agent_action_denied"
    VALIDATION_COMMAND_NONZERO_EXIT = "validation_command_nonzero_exit"
    VALIDATION_COMMAND_TIMEOUT = "validation_command_timeout"
    VALIDATION_COMMAND_OUTPUT_LIMIT = "validation_command_output_limit"
    VALIDATION_COMMAND_LAUNCH_ERROR = "validation_command_launch_error"


class OutcomeRetryPosture(str, Enum):
    NOT_AUTHORIZED = "not_authorized"


class OutcomeCancellationPoint(str, Enum):
    NONE = "none"
    SINGLE_AGENT_BEFORE_ACTION = "single_agent_before_action"
    VALIDATION_COMMAND_PRELAUNCH = "validation_command_prelaunch"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
BoundedIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
    AfterValidator(_reject_nul),
]
RepositoryRelativePathText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_reject_nul),
]


class _OutcomeModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class OutcomeDiagnosticProjection(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    diagnostic_id: BoundedIdentifier
    envelope_kind: OutcomeEnvelopeKind
    terminal_stage: OutcomeStage
    terminal_state: OutcomeTerminalState
    failure_category: OutcomeFailureCategory = OutcomeFailureCategory.NONE
    retry_posture: OutcomeRetryPosture = OutcomeRetryPosture.NOT_AUTHORIZED
    cancellation_point: OutcomeCancellationPoint = OutcomeCancellationPoint.NONE
    process_started: StrictBool
    result_envelopes_ready: Literal[True] = True
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    automatic_retry_authorized: Literal[False] = False
    automatic_fallback_authorized: Literal[False] = False
    automatic_resubmission_authorized: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    diagnostic_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_diagnostic(self) -> OutcomeDiagnosticProjection:
        if self.envelope_kind is OutcomeEnvelopeKind.RESULT:
            if self.terminal_state is not OutcomeTerminalState.COMPLETED:
                raise ValueError("result diagnostic requires completed state")
            if self.failure_category is not OutcomeFailureCategory.NONE:
                raise ValueError("result diagnostic must not carry failure")
            if self.cancellation_point is not OutcomeCancellationPoint.NONE:
                raise ValueError("result diagnostic must not carry cancellation")
        elif self.envelope_kind is OutcomeEnvelopeKind.FAILURE:
            if self.terminal_state is not OutcomeTerminalState.BLOCKED:
                raise ValueError("failure diagnostic requires blocked state")
            if self.failure_category is OutcomeFailureCategory.NONE:
                raise ValueError("failure diagnostic requires category")
            if self.cancellation_point is not OutcomeCancellationPoint.NONE:
                raise ValueError("failure diagnostic must not carry cancellation")
        else:
            if self.terminal_state is not OutcomeTerminalState.CANCELLED:
                raise ValueError("cancellation diagnostic requires cancelled state")
            if self.failure_category is not OutcomeFailureCategory.NONE:
                raise ValueError("cancellation diagnostic must not carry failure")
            if self.cancellation_point is OutcomeCancellationPoint.NONE:
                raise ValueError("cancellation diagnostic requires point")
            if self.process_started:
                raise ValueError("P17.5 cancellation evidence is prelaunch")
        if self.diagnostic_id != _diagnostic_id(
            kind=self.envelope_kind,
            stage=self.terminal_stage,
            state=self.terminal_state,
            failure_category=self.failure_category,
            cancellation_point=self.cancellation_point,
        ):
            raise ValueError("diagnostic_id mismatch")
        if self.diagnostic_SHA256 != _diagnostic_digest(self):
            raise ValueError("diagnostic digest mismatch")
        return self


class OutcomeTerminalEvidence(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    envelope_kind: OutcomeEnvelopeKind
    terminal_stage: OutcomeStage
    terminal_state: OutcomeTerminalState
    terminal_disposition: BoundedText
    failure_category: OutcomeFailureCategory = OutcomeFailureCategory.NONE
    cancellation_point: OutcomeCancellationPoint = OutcomeCancellationPoint.NONE
    single_agent_session_SHA256: DigestText | None = None
    single_agent_result_SHA256: DigestText | None = None
    validation_command_runner_session_SHA256: DigestText | None = None
    validation_command_runner_result_SHA256: DigestText | None = None
    terminal_action_id: BoundedIdentifier | None = None
    terminal_task_step_id: BoundedIdentifier | None = None
    terminal_command_id: BoundedIdentifier | None = None
    terminal_validation_id: BoundedIdentifier | None = None
    process_started: StrictBool
    terminal_evidence_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_terminal_evidence(self) -> OutcomeTerminalEvidence:
        if self.envelope_kind is OutcomeEnvelopeKind.RESULT:
            if self.terminal_stage is not OutcomeStage.VALIDATION_COMMAND_RUNNER:
                raise ValueError("result evidence requires validation stage")
            if self.terminal_state is not OutcomeTerminalState.COMPLETED:
                raise ValueError("result evidence requires completed state")
            if self.failure_category is not OutcomeFailureCategory.NONE:
                raise ValueError("result evidence must not carry failure")
            if self.cancellation_point is not OutcomeCancellationPoint.NONE:
                raise ValueError("result evidence must not carry cancellation")
            if (
                self.single_agent_result_SHA256 is None
                or self.validation_command_runner_result_SHA256 is None
                or self.validation_command_runner_session_SHA256 is None
            ):
                raise ValueError("result evidence requires result digests")
        elif self.envelope_kind is OutcomeEnvelopeKind.FAILURE:
            if self.terminal_state is not OutcomeTerminalState.BLOCKED:
                raise ValueError("failure evidence requires blocked state")
            if self.failure_category is OutcomeFailureCategory.NONE:
                raise ValueError("failure evidence requires category")
            if self.cancellation_point is not OutcomeCancellationPoint.NONE:
                raise ValueError("failure evidence must not carry cancellation")
            if self.validation_command_runner_result_SHA256 is not None:
                raise ValueError(
                    "failure evidence must not carry completed runner result"
                )
        else:
            if self.terminal_state is not OutcomeTerminalState.CANCELLED:
                raise ValueError("cancellation evidence requires cancelled state")
            if self.failure_category is not OutcomeFailureCategory.NONE:
                raise ValueError("cancellation evidence must not carry failure")
            if self.cancellation_point is OutcomeCancellationPoint.NONE:
                raise ValueError("cancellation evidence requires point")
            if self.process_started:
                raise ValueError("cancellation evidence must be prelaunch")
            if self.validation_command_runner_result_SHA256 is not None:
                raise ValueError("cancellation evidence must not carry runner result")
        if self.terminal_stage is OutcomeStage.SINGLE_AGENT_EXECUTION:
            if self.single_agent_session_SHA256 is None:
                raise ValueError("single-agent evidence requires session digest")
            if (
                self.validation_command_runner_session_SHA256 is not None
                or self.validation_command_runner_result_SHA256 is not None
            ):
                raise ValueError("single-agent evidence must not carry runner digests")
        elif self.validation_command_runner_session_SHA256 is None:
            raise ValueError("validation evidence requires runner session digest")
        if self.terminal_evidence_SHA256 != _terminal_evidence_digest(self):
            raise ValueError("terminal evidence digest mismatch")
        return self


class ResultEnvelope(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    envelope_id: BoundedIdentifier
    envelope_kind: Literal[OutcomeEnvelopeKind.RESULT] = OutcomeEnvelopeKind.RESULT
    work_packet_id: BoundedText
    work_packet_SHA256: DigestText
    allocation_id: BoundedText
    allocation_SHA256: DigestText
    profile_id: BoundedText
    profile_SHA256: DigestText
    diagnostic_projection: OutcomeDiagnosticProjection
    terminal_evidence: OutcomeTerminalEvidence
    completed_task_step_ids: tuple[BoundedIdentifier, ...]
    touched_paths: tuple[RepositoryRelativePathText, ...]
    read_paths: tuple[RepositoryRelativePathText, ...]
    created_paths: tuple[RepositoryRelativePathText, ...]
    replaced_paths: tuple[RepositoryRelativePathText, ...]
    deleted_paths: tuple[RepositoryRelativePathText, ...]
    passed_validation_ids: tuple[BoundedIdentifier, ...]
    manual_validation_ids_pending: tuple[BoundedIdentifier, ...]
    single_agent_result_SHA256: DigestText
    validation_command_runner_result_SHA256: DigestText
    result_envelopes_ready: Literal[True] = True
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    automatic_retry_authorized: Literal[False] = False
    automatic_fallback_authorized: Literal[False] = False
    automatic_resubmission_authorized: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    envelope_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result_envelope(self) -> ResultEnvelope:
        if self.diagnostic_projection.envelope_kind is not OutcomeEnvelopeKind.RESULT:
            raise ValueError("result envelope requires result diagnostic")
        if self.terminal_evidence.envelope_kind is not OutcomeEnvelopeKind.RESULT:
            raise ValueError("result envelope requires result terminal evidence")
        if (
            self.terminal_evidence.single_agent_result_SHA256
            != self.single_agent_result_SHA256
        ):
            raise ValueError("single-agent result digest mismatch")
        if (
            self.terminal_evidence.validation_command_runner_result_SHA256
            != self.validation_command_runner_result_SHA256
        ):
            raise ValueError("validation runner result digest mismatch")
        _validate_sorted_unique_paths(self.touched_paths)
        _validate_sorted_unique_paths(self.read_paths)
        _validate_sorted_unique_paths(self.created_paths)
        _validate_sorted_unique_paths(self.replaced_paths)
        _validate_sorted_unique_paths(self.deleted_paths)
        _validate_common_posture(self)
        _validate_envelope_id(self.envelope_id, self.envelope_kind, self.work_packet_id)
        if self.envelope_SHA256 != _result_envelope_digest(self):
            raise ValueError("result envelope digest mismatch")
        return self


class FailureEnvelope(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    envelope_id: BoundedIdentifier
    envelope_kind: Literal[OutcomeEnvelopeKind.FAILURE] = OutcomeEnvelopeKind.FAILURE
    work_packet_id: BoundedText
    work_packet_SHA256: DigestText
    allocation_id: BoundedText
    allocation_SHA256: DigestText
    profile_id: BoundedText
    profile_SHA256: DigestText
    diagnostic_projection: OutcomeDiagnosticProjection
    terminal_evidence: OutcomeTerminalEvidence
    failure_category: OutcomeFailureCategory
    single_agent_session_SHA256: DigestText | None = None
    single_agent_result_SHA256: DigestText | None = None
    validation_command_runner_session_SHA256: DigestText | None = None
    failed_action_id: BoundedIdentifier | None = None
    failed_task_step_id: BoundedIdentifier | None = None
    failed_command_id: BoundedIdentifier | None = None
    failed_validation_id: BoundedIdentifier | None = None
    result_envelopes_ready: Literal[True] = True
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    automatic_retry_authorized: Literal[False] = False
    automatic_fallback_authorized: Literal[False] = False
    automatic_resubmission_authorized: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    envelope_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_failure_envelope(self) -> FailureEnvelope:
        if self.diagnostic_projection.envelope_kind is not OutcomeEnvelopeKind.FAILURE:
            raise ValueError("failure envelope requires failure diagnostic")
        if self.terminal_evidence.envelope_kind is not OutcomeEnvelopeKind.FAILURE:
            raise ValueError("failure envelope requires failure terminal evidence")
        if self.failure_category is OutcomeFailureCategory.NONE:
            raise ValueError("failure envelope requires category")
        if self.terminal_evidence.failure_category is not self.failure_category:
            raise ValueError("failure category mismatch")
        if self.diagnostic_projection.failure_category is not self.failure_category:
            raise ValueError("diagnostic failure category mismatch")
        if self.terminal_evidence.terminal_stage is OutcomeStage.SINGLE_AGENT_EXECUTION:
            if self.single_agent_session_SHA256 is None:
                raise ValueError("single-agent failure requires session digest")
            if (
                self.terminal_evidence.single_agent_session_SHA256
                != self.single_agent_session_SHA256
            ):
                raise ValueError("single-agent failure digest mismatch")
        else:
            if self.validation_command_runner_session_SHA256 is None:
                raise ValueError("validation failure requires session digest")
            if (
                self.terminal_evidence.validation_command_runner_session_SHA256
                != self.validation_command_runner_session_SHA256
            ):
                raise ValueError("validation failure digest mismatch")
        _validate_common_posture(self)
        _validate_envelope_id(self.envelope_id, self.envelope_kind, self.work_packet_id)
        if self.envelope_SHA256 != _failure_envelope_digest(self):
            raise ValueError("failure envelope digest mismatch")
        return self


class CancellationEnvelope(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    envelope_id: BoundedIdentifier
    envelope_kind: Literal[OutcomeEnvelopeKind.CANCELLATION] = (
        OutcomeEnvelopeKind.CANCELLATION
    )
    work_packet_id: BoundedText
    work_packet_SHA256: DigestText
    allocation_id: BoundedText
    allocation_SHA256: DigestText
    profile_id: BoundedText
    profile_SHA256: DigestText
    diagnostic_projection: OutcomeDiagnosticProjection
    terminal_evidence: OutcomeTerminalEvidence
    cancellation_point: OutcomeCancellationPoint
    cancellation_reference: BoundedText | None = None
    single_agent_session_SHA256: DigestText | None = None
    single_agent_result_SHA256: DigestText | None = None
    validation_command_runner_session_SHA256: DigestText | None = None
    cancelled_action_id: BoundedIdentifier | None = None
    cancelled_task_step_id: BoundedIdentifier | None = None
    cancelled_command_id: BoundedIdentifier | None = None
    cancelled_validation_id: BoundedIdentifier | None = None
    process_started: Literal[False] = False
    result_envelopes_ready: Literal[True] = True
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    automatic_retry_authorized: Literal[False] = False
    automatic_fallback_authorized: Literal[False] = False
    automatic_resubmission_authorized: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    envelope_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_cancellation_envelope(self) -> CancellationEnvelope:
        if (
            self.diagnostic_projection.envelope_kind
            is not OutcomeEnvelopeKind.CANCELLATION
        ):
            raise ValueError("cancellation envelope requires cancellation diagnostic")
        if self.terminal_evidence.envelope_kind is not OutcomeEnvelopeKind.CANCELLATION:
            raise ValueError(
                "cancellation envelope requires cancellation terminal evidence"
            )
        if self.cancellation_point is OutcomeCancellationPoint.NONE:
            raise ValueError("cancellation envelope requires point")
        if self.terminal_evidence.cancellation_point is not self.cancellation_point:
            raise ValueError("cancellation point mismatch")
        if self.diagnostic_projection.cancellation_point is not self.cancellation_point:
            raise ValueError("diagnostic cancellation point mismatch")
        if self.terminal_evidence.process_started or self.process_started:
            raise ValueError("cancellation must be prelaunch")
        if self.terminal_evidence.terminal_stage is OutcomeStage.SINGLE_AGENT_EXECUTION:
            if self.single_agent_session_SHA256 is None:
                raise ValueError("single-agent cancellation requires session digest")
            if (
                self.terminal_evidence.single_agent_session_SHA256
                != self.single_agent_session_SHA256
            ):
                raise ValueError("single-agent cancellation digest mismatch")
        else:
            if self.validation_command_runner_session_SHA256 is None:
                raise ValueError("validation cancellation requires session digest")
            if (
                self.terminal_evidence.validation_command_runner_session_SHA256
                != self.validation_command_runner_session_SHA256
            ):
                raise ValueError("validation cancellation digest mismatch")
        _validate_common_posture(self)
        _validate_envelope_id(self.envelope_id, self.envelope_kind, self.work_packet_id)
        if self.envelope_SHA256 != _cancellation_envelope_digest(self):
            raise ValueError("cancellation envelope digest mismatch")
        return self


class OutcomeEnvelopeRequest(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    single_agent_execution_result: SingleAgentExecutionResult | None = None
    single_agent_execution_session: SingleAgentExecutionSession | None = None
    validation_command_runner_result: ValidationCommandRunnerResult | None = None
    validation_command_runner_session: ValidationCommandRunnerSession | None = None
    cancellation_reference: BoundedText | None = None
    request_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_request(self) -> OutcomeEnvelopeRequest:
        if (
            self.single_agent_execution_result is None
            and self.single_agent_execution_session is None
            and self.validation_command_runner_result is None
            and self.validation_command_runner_session is None
        ):
            raise ValueError("request requires terminal evidence")
        if (
            self.validation_command_runner_result is not None
            and self.validation_command_runner_session is not None
        ):
            raise ValueError("request has ambiguous validation evidence")
        if (
            self.single_agent_execution_session is not None
            and self.validation_command_runner_session is not None
        ):
            raise ValueError("request has ambiguous terminal sessions")
        if (
            self.single_agent_execution_session is not None
            and self.validation_command_runner_result is not None
        ):
            raise ValueError(
                "request cannot mix single-agent terminal session and result"
            )
        if self.request_SHA256 != _request_digest(self):
            raise ValueError("request digest mismatch")
        return self


class OutcomeEnvelope(_OutcomeModel):
    schema_version: Literal[1] = OUTCOME_ENVELOPE_SCHEMA_VERSION
    policy_id: Literal["pepper-deterministic-bounded-terminal-outcome-envelopes-v1"] = (
        OUTCOME_ENVELOPE_POLICY_ID
    )
    envelope_id: BoundedIdentifier
    envelope_kind: OutcomeEnvelopeKind
    result_envelope: ResultEnvelope | None = None
    failure_envelope: FailureEnvelope | None = None
    cancellation_envelope: CancellationEnvelope | None = None
    result_envelopes_ready: Literal[True] = True
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    automatic_retry_authorized: Literal[False] = False
    automatic_fallback_authorized: Literal[False] = False
    automatic_resubmission_authorized: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    envelope_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_outcome_envelope(self) -> OutcomeEnvelope:
        selected = tuple(
            item
            for item in (
                self.result_envelope,
                self.failure_envelope,
                self.cancellation_envelope,
            )
            if item is not None
        )
        if len(selected) != 1:
            raise ValueError("exactly one envelope selection is required")
        if selected[0].envelope_kind is not self.envelope_kind:
            raise ValueError("selected envelope kind mismatch")
        if self.envelope_id != _wrapper_id(selected[0].envelope_id):
            raise ValueError("outcome envelope id mismatch")
        _validate_common_posture(self)
        if self.envelope_SHA256 != _outcome_envelope_digest(self):
            raise ValueError("outcome envelope digest mismatch")
        return self


def build_result_envelope(
    *,
    single_agent_execution_result: SingleAgentExecutionResult,
    validation_command_runner_result: ValidationCommandRunnerResult,
) -> ResultEnvelope:
    """Project completed P17.3 and P17.4 evidence into a result envelope."""

    single_result = _validated_single_agent_result(single_agent_execution_result)
    runner_result = _validated_runner_result(validation_command_runner_result)
    _validate_result_binding(single_result, runner_result)
    session = runner_result.session
    terminal = _terminal_evidence_for_result(single_result, runner_result)
    diagnostic = _diagnostic_projection(
        kind=OutcomeEnvelopeKind.RESULT,
        stage=OutcomeStage.VALIDATION_COMMAND_RUNNER,
        state=OutcomeTerminalState.COMPLETED,
        failure_category=OutcomeFailureCategory.NONE,
        cancellation_point=OutcomeCancellationPoint.NONE,
        process_started=True,
    )
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_id": _envelope_id(
            OutcomeEnvelopeKind.RESULT,
            session.work_packet_id,
            terminal.terminal_evidence_SHA256,
        ),
        "envelope_kind": OutcomeEnvelopeKind.RESULT,
        "work_packet_id": session.work_packet_id,
        "work_packet_SHA256": session.work_packet_SHA256,
        "allocation_id": session.allocation_id,
        "allocation_SHA256": session.allocation_SHA256,
        "profile_id": session.profile_id,
        "profile_SHA256": session.profile_SHA256,
        "diagnostic_projection": diagnostic,
        "terminal_evidence": terminal,
        "completed_task_step_ids": single_result.completed_task_step_ids,
        "touched_paths": single_result.touched_paths,
        "read_paths": single_result.read_paths,
        "created_paths": single_result.created_paths,
        "replaced_paths": single_result.replaced_paths,
        "deleted_paths": single_result.deleted_paths,
        "passed_validation_ids": runner_result.passed_validation_ids,
        "manual_validation_ids_pending": runner_result.manual_validation_ids_pending,
        "single_agent_result_SHA256": single_result.result_SHA256,
        "validation_command_runner_result_SHA256": runner_result.result_SHA256,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return ResultEnvelope(
        **data,
        envelope_SHA256=_result_envelope_digest_from_record(data),
    )


def build_failure_envelope(
    *,
    single_agent_execution_session: SingleAgentExecutionSession | None = None,
    validation_command_runner_session: ValidationCommandRunnerSession | None = None,
    single_agent_execution_result: SingleAgentExecutionResult | None = None,
) -> FailureEnvelope:
    """Project one blocked P17.3 or P17.4 terminal session into failure."""

    if single_agent_execution_session is not None:
        if validation_command_runner_session is not None:
            raise OutcomeEnvelopeStateError("failure source is ambiguous")
        return _single_agent_failure_envelope(single_agent_execution_session)
    if validation_command_runner_session is None:
        raise OutcomeEnvelopeStateError("failure source is required")
    return _validation_failure_envelope(
        validation_command_runner_session=validation_command_runner_session,
        single_agent_execution_result=single_agent_execution_result,
    )


def build_cancellation_envelope(
    *,
    single_agent_execution_session: SingleAgentExecutionSession | None = None,
    validation_command_runner_session: ValidationCommandRunnerSession | None = None,
    single_agent_execution_result: SingleAgentExecutionResult | None = None,
    cancellation_reference: str | None = None,
) -> CancellationEnvelope:
    """Project one cancelled P17.3 or P17.4 terminal session into cancellation."""

    if single_agent_execution_session is not None:
        if validation_command_runner_session is not None:
            raise OutcomeEnvelopeStateError("cancellation source is ambiguous")
        return _single_agent_cancellation_envelope(
            single_agent_execution_session=single_agent_execution_session,
            cancellation_reference=cancellation_reference,
        )
    if validation_command_runner_session is None:
        raise OutcomeEnvelopeStateError("cancellation source is required")
    return _validation_cancellation_envelope(
        validation_command_runner_session=validation_command_runner_session,
        single_agent_execution_result=single_agent_execution_result,
        cancellation_reference=cancellation_reference,
    )


def build_outcome_envelope(request: OutcomeEnvelopeRequest) -> OutcomeEnvelope:
    """Select exactly one terminal outcome envelope from supplied evidence."""

    validated = _validated_request(request)
    if validated.validation_command_runner_result is not None:
        if validated.single_agent_execution_result is None:
            raise OutcomeEnvelopeStateError("result requires single-agent result")
        return _wrap_envelope(
            build_result_envelope(
                single_agent_execution_result=validated.single_agent_execution_result,
                validation_command_runner_result=validated.validation_command_runner_result,
            )
        )
    if validated.validation_command_runner_session is not None:
        session = validated.validation_command_runner_session
        if session.state is ValidationCommandRunnerState.BLOCKED:
            return _wrap_envelope(
                build_failure_envelope(
                    validation_command_runner_session=session,
                    single_agent_execution_result=validated.single_agent_execution_result,
                )
            )
        if session.state is ValidationCommandRunnerState.CANCELLED:
            return _wrap_envelope(
                build_cancellation_envelope(
                    validation_command_runner_session=session,
                    single_agent_execution_result=validated.single_agent_execution_result,
                    cancellation_reference=validated.cancellation_reference,
                )
            )
        raise OutcomeEnvelopeStateError("validation runner session is not terminal")
    if validated.single_agent_execution_session is not None:
        session = validated.single_agent_execution_session
        if session.state is SingleAgentExecutionState.BLOCKED:
            return _wrap_envelope(
                build_failure_envelope(single_agent_execution_session=session)
            )
        if session.state is SingleAgentExecutionState.CANCELLED:
            return _wrap_envelope(
                build_cancellation_envelope(
                    single_agent_execution_session=session,
                    cancellation_reference=validated.cancellation_reference,
                )
            )
        raise OutcomeEnvelopeStateError("single-agent session is not terminal")
    raise OutcomeEnvelopeStateError("terminal outcome evidence is incomplete")


def validate_outcome_envelope_request(request: OutcomeEnvelopeRequest) -> None:
    try:
        _validated_request(request)
    except OutcomeEnvelopeError:
        raise
    except Exception as exc:
        raise OutcomeEnvelopeValidationError(
            "outcome envelope request invalid"
        ) from exc


def validate_outcome_envelope(envelope: OutcomeEnvelope) -> None:
    try:
        OutcomeEnvelope.model_validate(envelope.model_dump(mode="json"))
    except Exception as exc:
        raise OutcomeEnvelopeValidationError("outcome envelope invalid") from exc


def _outcome_request(
    *,
    single_agent_execution_result: SingleAgentExecutionResult | None = None,
    single_agent_execution_session: SingleAgentExecutionSession | None = None,
    validation_command_runner_result: ValidationCommandRunnerResult | None = None,
    validation_command_runner_session: ValidationCommandRunnerSession | None = None,
    cancellation_reference: str | None = None,
) -> OutcomeEnvelopeRequest:
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "single_agent_execution_result": single_agent_execution_result,
        "single_agent_execution_session": single_agent_execution_session,
        "validation_command_runner_result": validation_command_runner_result,
        "validation_command_runner_session": validation_command_runner_session,
        "cancellation_reference": cancellation_reference,
    }
    return OutcomeEnvelopeRequest(
        **data,
        request_SHA256=_request_digest_from_record(data),
    )


def _validated_request(request: OutcomeEnvelopeRequest) -> OutcomeEnvelopeRequest:
    try:
        return OutcomeEnvelopeRequest.model_validate(request.model_dump(mode="json"))
    except Exception as exc:
        raise OutcomeEnvelopeInputError("outcome envelope request invalid") from exc


def _validated_single_agent_result(
    result: SingleAgentExecutionResult,
) -> SingleAgentExecutionResult:
    try:
        validated = SingleAgentExecutionResult.model_validate(
            result.model_dump(mode="json")
        )
        validate_single_agent_execution_result(validated)
    except Exception as exc:
        raise OutcomeEnvelopeInputError("single-agent result invalid") from exc
    return validated


def _validated_single_agent_session(
    session: SingleAgentExecutionSession,
) -> SingleAgentExecutionSession:
    try:
        validated = SingleAgentExecutionSession.model_validate(
            session.model_dump(mode="json")
        )
        validate_single_agent_execution_session(validated)
    except Exception as exc:
        raise OutcomeEnvelopeInputError("single-agent session invalid") from exc
    return validated


def _validated_runner_result(
    result: ValidationCommandRunnerResult,
) -> ValidationCommandRunnerResult:
    try:
        validated = ValidationCommandRunnerResult.model_validate(
            result.model_dump(mode="json")
        )
        validate_validation_command_runner_result(validated)
    except Exception as exc:
        raise OutcomeEnvelopeInputError("validation result invalid") from exc
    return validated


def _validated_runner_session(
    session: ValidationCommandRunnerSession,
) -> ValidationCommandRunnerSession:
    try:
        validated = ValidationCommandRunnerSession.model_validate(
            session.model_dump(mode="json")
        )
        validate_validation_command_runner_session(validated)
    except Exception as exc:
        raise OutcomeEnvelopeInputError("validation session invalid") from exc
    return validated


def _validate_result_binding(
    single_result: SingleAgentExecutionResult,
    runner_result: ValidationCommandRunnerResult,
) -> None:
    session = runner_result.session
    if session.single_agent_result_SHA256 != single_result.result_SHA256:
        raise OutcomeEnvelopeInputError("single-agent result digest mismatch")
    if session.work_packet_id != single_result.session.work_packet_id:
        raise OutcomeEnvelopeInputError("WorkPacket identity mismatch")
    if session.work_packet_SHA256 != single_result.session.work_packet_SHA256:
        raise OutcomeEnvelopeInputError("WorkPacket digest mismatch")
    if session.allocation_id != single_result.session.allocation_id:
        raise OutcomeEnvelopeInputError("allocation identity mismatch")
    if session.allocation_SHA256 != single_result.session.allocation_SHA256:
        raise OutcomeEnvelopeInputError("allocation digest mismatch")
    if session.profile_id != single_result.session.profile_id:
        raise OutcomeEnvelopeInputError("profile identity mismatch")
    if session.profile_SHA256 != single_result.session.profile_SHA256:
        raise OutcomeEnvelopeInputError("profile digest mismatch")


def _validate_optional_single_result_binding(
    single_result: SingleAgentExecutionResult | None,
    session: ValidationCommandRunnerSession,
) -> str:
    if single_result is None:
        return session.single_agent_result_SHA256
    validated = _validated_single_agent_result(single_result)
    if session.single_agent_result_SHA256 != validated.result_SHA256:
        raise OutcomeEnvelopeInputError("single-agent result digest mismatch")
    if session.work_packet_id != validated.session.work_packet_id:
        raise OutcomeEnvelopeInputError("WorkPacket identity mismatch")
    if session.work_packet_SHA256 != validated.session.work_packet_SHA256:
        raise OutcomeEnvelopeInputError("WorkPacket digest mismatch")
    if session.allocation_id != validated.session.allocation_id:
        raise OutcomeEnvelopeInputError("allocation identity mismatch")
    if session.allocation_SHA256 != validated.session.allocation_SHA256:
        raise OutcomeEnvelopeInputError("allocation digest mismatch")
    if session.profile_id != validated.session.profile_id:
        raise OutcomeEnvelopeInputError("profile identity mismatch")
    if session.profile_SHA256 != validated.session.profile_SHA256:
        raise OutcomeEnvelopeInputError("profile digest mismatch")
    return validated.result_SHA256


def _single_agent_failure_envelope(
    single_agent_execution_session: SingleAgentExecutionSession,
) -> FailureEnvelope:
    session = _validated_single_agent_session(single_agent_execution_session)
    if session.state is not SingleAgentExecutionState.BLOCKED:
        raise OutcomeEnvelopeStateError("single-agent session is not blocked")
    if not session.action_evidence:
        raise OutcomeEnvelopeStateError("single-agent failure lacks evidence")
    evidence = session.action_evidence[-1]
    category = _single_agent_failure_category(evidence.disposition)
    terminal = _terminal_evidence_for_single_agent_failure(session, category)
    diagnostic = _diagnostic_projection(
        kind=OutcomeEnvelopeKind.FAILURE,
        stage=OutcomeStage.SINGLE_AGENT_EXECUTION,
        state=OutcomeTerminalState.BLOCKED,
        failure_category=category,
        cancellation_point=OutcomeCancellationPoint.NONE,
        process_started=False,
    )
    data = _base_failure_record(
        session=session,
        diagnostic_projection=diagnostic,
        terminal_evidence=terminal,
        failure_category=category,
        single_agent_session_SHA256=session.session_SHA256,
        single_agent_result_SHA256=None,
        validation_command_runner_session_SHA256=None,
        failed_action_id=evidence.action_id,
        failed_task_step_id=evidence.task_step_id,
        failed_command_id=None,
        failed_validation_id=None,
    )
    return FailureEnvelope(
        **data,
        envelope_SHA256=_failure_envelope_digest_from_record(data),
    )


def _validation_failure_envelope(
    *,
    validation_command_runner_session: ValidationCommandRunnerSession,
    single_agent_execution_result: SingleAgentExecutionResult | None,
) -> FailureEnvelope:
    session = _validated_runner_session(validation_command_runner_session)
    if session.state is not ValidationCommandRunnerState.BLOCKED:
        raise OutcomeEnvelopeStateError("validation session is not blocked")
    if not session.command_evidence:
        raise OutcomeEnvelopeStateError("validation failure lacks evidence")
    single_result_sha = _validate_optional_single_result_binding(
        single_agent_execution_result,
        session,
    )
    evidence = session.command_evidence[-1]
    category = _validation_failure_category(evidence.failure_reason)
    terminal = _terminal_evidence_for_validation_failure(session, category)
    diagnostic = _diagnostic_projection(
        kind=OutcomeEnvelopeKind.FAILURE,
        stage=OutcomeStage.VALIDATION_COMMAND_RUNNER,
        state=OutcomeTerminalState.BLOCKED,
        failure_category=category,
        cancellation_point=OutcomeCancellationPoint.NONE,
        process_started=evidence.process_started,
    )
    data = _base_failure_record(
        session=session,
        diagnostic_projection=diagnostic,
        terminal_evidence=terminal,
        failure_category=category,
        single_agent_session_SHA256=None,
        single_agent_result_SHA256=single_result_sha,
        validation_command_runner_session_SHA256=session.session_SHA256,
        failed_action_id=None,
        failed_task_step_id=None,
        failed_command_id=evidence.command_id,
        failed_validation_id=evidence.validation_id,
    )
    return FailureEnvelope(
        **data,
        envelope_SHA256=_failure_envelope_digest_from_record(data),
    )


def _single_agent_cancellation_envelope(
    *,
    single_agent_execution_session: SingleAgentExecutionSession,
    cancellation_reference: str | None,
) -> CancellationEnvelope:
    session = _validated_single_agent_session(single_agent_execution_session)
    if session.state is not SingleAgentExecutionState.CANCELLED:
        raise OutcomeEnvelopeStateError("single-agent session is not cancelled")
    if not session.action_evidence:
        raise OutcomeEnvelopeStateError("single-agent cancellation lacks evidence")
    evidence = session.action_evidence[-1]
    cancellation_point = OutcomeCancellationPoint.SINGLE_AGENT_BEFORE_ACTION
    terminal = _terminal_evidence_for_single_agent_cancellation(
        session, cancellation_point
    )
    diagnostic = _diagnostic_projection(
        kind=OutcomeEnvelopeKind.CANCELLATION,
        stage=OutcomeStage.SINGLE_AGENT_EXECUTION,
        state=OutcomeTerminalState.CANCELLED,
        failure_category=OutcomeFailureCategory.NONE,
        cancellation_point=cancellation_point,
        process_started=False,
    )
    data = _base_cancellation_record(
        session=session,
        diagnostic_projection=diagnostic,
        terminal_evidence=terminal,
        cancellation_point=cancellation_point,
        cancellation_reference=cancellation_reference,
        single_agent_session_SHA256=session.session_SHA256,
        single_agent_result_SHA256=None,
        validation_command_runner_session_SHA256=None,
        cancelled_action_id=evidence.action_id,
        cancelled_task_step_id=evidence.task_step_id,
        cancelled_command_id=None,
        cancelled_validation_id=None,
    )
    return CancellationEnvelope(
        **data,
        envelope_SHA256=_cancellation_envelope_digest_from_record(data),
    )


def _validation_cancellation_envelope(
    *,
    validation_command_runner_session: ValidationCommandRunnerSession,
    single_agent_execution_result: SingleAgentExecutionResult | None,
    cancellation_reference: str | None,
) -> CancellationEnvelope:
    session = _validated_runner_session(validation_command_runner_session)
    if session.state is not ValidationCommandRunnerState.CANCELLED:
        raise OutcomeEnvelopeStateError("validation session is not cancelled")
    if not session.command_evidence:
        raise OutcomeEnvelopeStateError("validation cancellation lacks evidence")
    single_result_sha = _validate_optional_single_result_binding(
        single_agent_execution_result,
        session,
    )
    evidence = session.command_evidence[-1]
    cancellation_point = OutcomeCancellationPoint.VALIDATION_COMMAND_PRELAUNCH
    terminal = _terminal_evidence_for_validation_cancellation(
        session, cancellation_point
    )
    diagnostic = _diagnostic_projection(
        kind=OutcomeEnvelopeKind.CANCELLATION,
        stage=OutcomeStage.VALIDATION_COMMAND_RUNNER,
        state=OutcomeTerminalState.CANCELLED,
        failure_category=OutcomeFailureCategory.NONE,
        cancellation_point=cancellation_point,
        process_started=False,
    )
    data = _base_cancellation_record(
        session=session,
        diagnostic_projection=diagnostic,
        terminal_evidence=terminal,
        cancellation_point=cancellation_point,
        cancellation_reference=cancellation_reference,
        single_agent_session_SHA256=None,
        single_agent_result_SHA256=single_result_sha,
        validation_command_runner_session_SHA256=session.session_SHA256,
        cancelled_action_id=None,
        cancelled_task_step_id=None,
        cancelled_command_id=evidence.command_id,
        cancelled_validation_id=evidence.validation_id,
    )
    return CancellationEnvelope(
        **data,
        envelope_SHA256=_cancellation_envelope_digest_from_record(data),
    )


def _base_failure_record(
    *,
    session: SingleAgentExecutionSession | ValidationCommandRunnerSession,
    diagnostic_projection: OutcomeDiagnosticProjection,
    terminal_evidence: OutcomeTerminalEvidence,
    failure_category: OutcomeFailureCategory,
    single_agent_session_SHA256: str | None,
    single_agent_result_SHA256: str | None,
    validation_command_runner_session_SHA256: str | None,
    failed_action_id: str | None,
    failed_task_step_id: str | None,
    failed_command_id: str | None,
    failed_validation_id: str | None,
) -> dict[str, object]:
    return {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_id": _envelope_id(
            OutcomeEnvelopeKind.FAILURE,
            session.work_packet_id,
            terminal_evidence.terminal_evidence_SHA256,
        ),
        "envelope_kind": OutcomeEnvelopeKind.FAILURE,
        "work_packet_id": session.work_packet_id,
        "work_packet_SHA256": session.work_packet_SHA256,
        "allocation_id": session.allocation_id,
        "allocation_SHA256": session.allocation_SHA256,
        "profile_id": session.profile_id,
        "profile_SHA256": session.profile_SHA256,
        "diagnostic_projection": diagnostic_projection,
        "terminal_evidence": terminal_evidence,
        "failure_category": failure_category,
        "single_agent_session_SHA256": single_agent_session_SHA256,
        "single_agent_result_SHA256": single_agent_result_SHA256,
        "validation_command_runner_session_SHA256": validation_command_runner_session_SHA256,
        "failed_action_id": failed_action_id,
        "failed_task_step_id": failed_task_step_id,
        "failed_command_id": failed_command_id,
        "failed_validation_id": failed_validation_id,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }


def _base_cancellation_record(
    *,
    session: SingleAgentExecutionSession | ValidationCommandRunnerSession,
    diagnostic_projection: OutcomeDiagnosticProjection,
    terminal_evidence: OutcomeTerminalEvidence,
    cancellation_point: OutcomeCancellationPoint,
    cancellation_reference: str | None,
    single_agent_session_SHA256: str | None,
    single_agent_result_SHA256: str | None,
    validation_command_runner_session_SHA256: str | None,
    cancelled_action_id: str | None,
    cancelled_task_step_id: str | None,
    cancelled_command_id: str | None,
    cancelled_validation_id: str | None,
) -> dict[str, object]:
    return {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_id": _envelope_id(
            OutcomeEnvelopeKind.CANCELLATION,
            session.work_packet_id,
            terminal_evidence.terminal_evidence_SHA256,
        ),
        "envelope_kind": OutcomeEnvelopeKind.CANCELLATION,
        "work_packet_id": session.work_packet_id,
        "work_packet_SHA256": session.work_packet_SHA256,
        "allocation_id": session.allocation_id,
        "allocation_SHA256": session.allocation_SHA256,
        "profile_id": session.profile_id,
        "profile_SHA256": session.profile_SHA256,
        "diagnostic_projection": diagnostic_projection,
        "terminal_evidence": terminal_evidence,
        "cancellation_point": cancellation_point,
        "cancellation_reference": cancellation_reference,
        "single_agent_session_SHA256": single_agent_session_SHA256,
        "single_agent_result_SHA256": single_agent_result_SHA256,
        "validation_command_runner_session_SHA256": validation_command_runner_session_SHA256,
        "cancelled_action_id": cancelled_action_id,
        "cancelled_task_step_id": cancelled_task_step_id,
        "cancelled_command_id": cancelled_command_id,
        "cancelled_validation_id": cancelled_validation_id,
        "process_started": False,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }


def _terminal_evidence_for_result(
    single_result: SingleAgentExecutionResult,
    runner_result: ValidationCommandRunnerResult,
) -> OutcomeTerminalEvidence:
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_kind": OutcomeEnvelopeKind.RESULT,
        "terminal_stage": OutcomeStage.VALIDATION_COMMAND_RUNNER,
        "terminal_state": OutcomeTerminalState.COMPLETED,
        "terminal_disposition": OutcomeEnvelopeKind.RESULT.value,
        "failure_category": OutcomeFailureCategory.NONE,
        "cancellation_point": OutcomeCancellationPoint.NONE,
        "single_agent_session_SHA256": single_result.session.session_SHA256,
        "single_agent_result_SHA256": single_result.result_SHA256,
        "validation_command_runner_session_SHA256": runner_result.session.session_SHA256,
        "validation_command_runner_result_SHA256": runner_result.result_SHA256,
        "terminal_action_id": None,
        "terminal_task_step_id": None,
        "terminal_command_id": runner_result.session.completed_command_ids[-1],
        "terminal_validation_id": runner_result.passed_validation_ids[-1],
        "process_started": True,
    }
    return OutcomeTerminalEvidence(
        **data,
        terminal_evidence_SHA256=_terminal_evidence_digest_from_record(data),
    )


def _terminal_evidence_for_single_agent_failure(
    session: SingleAgentExecutionSession,
    category: OutcomeFailureCategory,
) -> OutcomeTerminalEvidence:
    evidence = session.action_evidence[-1]
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_kind": OutcomeEnvelopeKind.FAILURE,
        "terminal_stage": OutcomeStage.SINGLE_AGENT_EXECUTION,
        "terminal_state": OutcomeTerminalState.BLOCKED,
        "terminal_disposition": evidence.disposition.value,
        "failure_category": category,
        "cancellation_point": OutcomeCancellationPoint.NONE,
        "single_agent_session_SHA256": session.session_SHA256,
        "single_agent_result_SHA256": None,
        "validation_command_runner_session_SHA256": None,
        "validation_command_runner_result_SHA256": None,
        "terminal_action_id": evidence.action_id,
        "terminal_task_step_id": evidence.task_step_id,
        "terminal_command_id": None,
        "terminal_validation_id": None,
        "process_started": False,
    }
    return OutcomeTerminalEvidence(
        **data,
        terminal_evidence_SHA256=_terminal_evidence_digest_from_record(data),
    )


def _terminal_evidence_for_validation_failure(
    session: ValidationCommandRunnerSession,
    category: OutcomeFailureCategory,
) -> OutcomeTerminalEvidence:
    evidence = session.command_evidence[-1]
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_kind": OutcomeEnvelopeKind.FAILURE,
        "terminal_stage": OutcomeStage.VALIDATION_COMMAND_RUNNER,
        "terminal_state": OutcomeTerminalState.BLOCKED,
        "terminal_disposition": evidence.disposition.value,
        "failure_category": category,
        "cancellation_point": OutcomeCancellationPoint.NONE,
        "single_agent_session_SHA256": None,
        "single_agent_result_SHA256": session.single_agent_result_SHA256,
        "validation_command_runner_session_SHA256": session.session_SHA256,
        "validation_command_runner_result_SHA256": None,
        "terminal_action_id": None,
        "terminal_task_step_id": None,
        "terminal_command_id": evidence.command_id,
        "terminal_validation_id": evidence.validation_id,
        "process_started": evidence.process_started,
    }
    return OutcomeTerminalEvidence(
        **data,
        terminal_evidence_SHA256=_terminal_evidence_digest_from_record(data),
    )


def _terminal_evidence_for_single_agent_cancellation(
    session: SingleAgentExecutionSession,
    cancellation_point: OutcomeCancellationPoint,
) -> OutcomeTerminalEvidence:
    evidence = session.action_evidence[-1]
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_kind": OutcomeEnvelopeKind.CANCELLATION,
        "terminal_stage": OutcomeStage.SINGLE_AGENT_EXECUTION,
        "terminal_state": OutcomeTerminalState.CANCELLED,
        "terminal_disposition": evidence.disposition.value,
        "failure_category": OutcomeFailureCategory.NONE,
        "cancellation_point": cancellation_point,
        "single_agent_session_SHA256": session.session_SHA256,
        "single_agent_result_SHA256": None,
        "validation_command_runner_session_SHA256": None,
        "validation_command_runner_result_SHA256": None,
        "terminal_action_id": evidence.action_id,
        "terminal_task_step_id": evidence.task_step_id,
        "terminal_command_id": None,
        "terminal_validation_id": None,
        "process_started": False,
    }
    return OutcomeTerminalEvidence(
        **data,
        terminal_evidence_SHA256=_terminal_evidence_digest_from_record(data),
    )


def _terminal_evidence_for_validation_cancellation(
    session: ValidationCommandRunnerSession,
    cancellation_point: OutcomeCancellationPoint,
) -> OutcomeTerminalEvidence:
    evidence = session.command_evidence[-1]
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_kind": OutcomeEnvelopeKind.CANCELLATION,
        "terminal_stage": OutcomeStage.VALIDATION_COMMAND_RUNNER,
        "terminal_state": OutcomeTerminalState.CANCELLED,
        "terminal_disposition": evidence.disposition.value,
        "failure_category": OutcomeFailureCategory.NONE,
        "cancellation_point": cancellation_point,
        "single_agent_session_SHA256": None,
        "single_agent_result_SHA256": session.single_agent_result_SHA256,
        "validation_command_runner_session_SHA256": session.session_SHA256,
        "validation_command_runner_result_SHA256": None,
        "terminal_action_id": None,
        "terminal_task_step_id": None,
        "terminal_command_id": evidence.command_id,
        "terminal_validation_id": evidence.validation_id,
        "process_started": False,
    }
    return OutcomeTerminalEvidence(
        **data,
        terminal_evidence_SHA256=_terminal_evidence_digest_from_record(data),
    )


def _diagnostic_projection(
    *,
    kind: OutcomeEnvelopeKind,
    stage: OutcomeStage,
    state: OutcomeTerminalState,
    failure_category: OutcomeFailureCategory,
    cancellation_point: OutcomeCancellationPoint,
    process_started: bool,
) -> OutcomeDiagnosticProjection:
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "diagnostic_id": _diagnostic_id(
            kind=kind,
            stage=stage,
            state=state,
            failure_category=failure_category,
            cancellation_point=cancellation_point,
        ),
        "envelope_kind": kind,
        "terminal_stage": stage,
        "terminal_state": state,
        "failure_category": failure_category,
        "retry_posture": OutcomeRetryPosture.NOT_AUTHORIZED,
        "cancellation_point": cancellation_point,
        "process_started": process_started,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return OutcomeDiagnosticProjection(
        **data,
        diagnostic_SHA256=_diagnostic_digest_from_record(data),
    )


def _single_agent_failure_category(
    disposition: SingleAgentActionDisposition,
) -> OutcomeFailureCategory:
    if disposition is SingleAgentActionDisposition.DENIED:
        return OutcomeFailureCategory.SINGLE_AGENT_ACTION_DENIED
    return OutcomeFailureCategory.SINGLE_AGENT_BLOCKED


def _validation_failure_category(
    reason: ValidationCommandFailureReason,
) -> OutcomeFailureCategory:
    if reason is ValidationCommandFailureReason.NONZERO_EXIT:
        return OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT
    if reason is ValidationCommandFailureReason.TIMEOUT:
        return OutcomeFailureCategory.VALIDATION_COMMAND_TIMEOUT
    if reason is ValidationCommandFailureReason.OUTPUT_LIMIT:
        return OutcomeFailureCategory.VALIDATION_COMMAND_OUTPUT_LIMIT
    if reason is ValidationCommandFailureReason.LAUNCH_ERROR:
        return OutcomeFailureCategory.VALIDATION_COMMAND_LAUNCH_ERROR
    raise OutcomeEnvelopeStateError("validation failure reason is not failed")


def _wrap_envelope(
    envelope: ResultEnvelope | FailureEnvelope | CancellationEnvelope,
) -> OutcomeEnvelope:
    data = {
        "schema_version": OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_id": _wrapper_id(envelope.envelope_id),
        "envelope_kind": envelope.envelope_kind,
        "result_envelope": envelope
        if envelope.envelope_kind is OutcomeEnvelopeKind.RESULT
        else None,
        "failure_envelope": envelope
        if envelope.envelope_kind is OutcomeEnvelopeKind.FAILURE
        else None,
        "cancellation_envelope": envelope
        if envelope.envelope_kind is OutcomeEnvelopeKind.CANCELLATION
        else None,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return OutcomeEnvelope(
        **data,
        envelope_SHA256=_outcome_envelope_digest_from_record(data),
    )


def _selected_envelope(
    envelope: OutcomeEnvelope,
) -> ResultEnvelope | FailureEnvelope | CancellationEnvelope:
    if envelope.result_envelope is not None:
        return envelope.result_envelope
    if envelope.failure_envelope is not None:
        return envelope.failure_envelope
    if envelope.cancellation_envelope is not None:
        return envelope.cancellation_envelope
    raise OutcomeEnvelopeStateError("outcome envelope is empty")


def _validate_common_posture(envelope: object) -> None:
    for field in (
        "result_envelopes_ready",
        "diff_artifact_review_ready",
        "human_git_handoff_ready",
        "automatic_retry_authorized",
        "automatic_fallback_authorized",
        "automatic_resubmission_authorized",
        "provider_dispatch_count",
        "model_inference_count",
    ):
        getattr(envelope, field)


def _validate_sorted_unique_paths(paths: tuple[str, ...]) -> None:
    if tuple(sorted(frozenset(paths))) != paths:
        raise ValueError("path collections must be unique and sorted")


def _validate_envelope_id(
    envelope_id: str,
    kind: OutcomeEnvelopeKind,
    work_packet_id: str,
) -> None:
    prefix = f"OE-{kind.value.upper()}-"
    if not envelope_id.startswith(prefix):
        raise ValueError("envelope id prefix mismatch")
    if len(envelope_id.rsplit("-", 1)[-1]) != 16:
        raise ValueError("envelope id digest suffix mismatch")
    if not work_packet_id:
        raise ValueError("work packet id is required")


def _diagnostic_id(
    *,
    kind: OutcomeEnvelopeKind,
    stage: OutcomeStage,
    state: OutcomeTerminalState,
    failure_category: OutcomeFailureCategory,
    cancellation_point: OutcomeCancellationPoint,
) -> str:
    digest = _sha256_text(
        ":".join((
            kind.value,
            stage.value,
            state.value,
            failure_category.value,
            cancellation_point.value,
        ))
    )[:16]
    return f"OD-{kind.value.upper()}-{digest}"


def _envelope_id(
    kind: OutcomeEnvelopeKind,
    work_packet_id: str,
    terminal_evidence_sha: str,
) -> str:
    digest = _sha256_text(f"{kind.value}:{work_packet_id}:{terminal_evidence_sha}")[:16]
    return f"OE-{kind.value.upper()}-{digest}"


def _wrapper_id(envelope_id: str) -> str:
    return f"OE-WRAPPER-{_sha256_text(envelope_id)[:16]}"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _dump_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_dump_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _dump_value(item) for key, item in value.items()}
    return value


def _normalized_record(record: dict[str, object]) -> dict[str, object]:
    return {key: _dump_value(value) for key, value in record.items()}


def _digest(algorithm: str, record: dict[str, object]) -> str:
    return _sha256_text(
        _deterministic_json({"algorithm": algorithm, **_normalized_record(record)})
    )


def _diagnostic_digest(diagnostic: OutcomeDiagnosticProjection) -> str:
    return _diagnostic_digest_from_record(
        diagnostic.model_dump(mode="json", exclude={"diagnostic_SHA256"})
    )


def _diagnostic_digest_from_record(record: dict[str, object]) -> str:
    return _digest(DIAGNOSTIC_DIGEST_ALGORITHM, record)


def _terminal_evidence_digest(evidence: OutcomeTerminalEvidence) -> str:
    return _terminal_evidence_digest_from_record(
        evidence.model_dump(mode="json", exclude={"terminal_evidence_SHA256"})
    )


def _terminal_evidence_digest_from_record(record: dict[str, object]) -> str:
    return _digest(TERMINAL_EVIDENCE_DIGEST_ALGORITHM, record)


def _result_envelope_digest(envelope: ResultEnvelope) -> str:
    return _result_envelope_digest_from_record(
        envelope.model_dump(mode="json", exclude={"envelope_SHA256"})
    )


def _result_envelope_digest_from_record(record: dict[str, object]) -> str:
    return _digest(RESULT_ENVELOPE_DIGEST_ALGORITHM, record)


def _failure_envelope_digest(envelope: FailureEnvelope) -> str:
    return _failure_envelope_digest_from_record(
        envelope.model_dump(mode="json", exclude={"envelope_SHA256"})
    )


def _failure_envelope_digest_from_record(record: dict[str, object]) -> str:
    return _digest(FAILURE_ENVELOPE_DIGEST_ALGORITHM, record)


def _cancellation_envelope_digest(envelope: CancellationEnvelope) -> str:
    return _cancellation_envelope_digest_from_record(
        envelope.model_dump(mode="json", exclude={"envelope_SHA256"})
    )


def _cancellation_envelope_digest_from_record(record: dict[str, object]) -> str:
    return _digest(CANCELLATION_ENVELOPE_DIGEST_ALGORITHM, record)


def _request_digest(request: OutcomeEnvelopeRequest) -> str:
    return _request_digest_from_record(
        request.model_dump(mode="json", exclude={"request_SHA256"})
    )


def _request_digest_from_record(record: dict[str, object]) -> str:
    return _digest(REQUEST_DIGEST_ALGORITHM, record)


def _outcome_envelope_digest(envelope: OutcomeEnvelope) -> str:
    return _outcome_envelope_digest_from_record(
        envelope.model_dump(mode="json", exclude={"envelope_SHA256"})
    )


def _outcome_envelope_digest_from_record(record: dict[str, object]) -> str:
    return _digest(OUTCOME_ENVELOPE_DIGEST_ALGORITHM, record)
