"""Immutable contracts for the governed Hermes runtime adapter."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, ClassVar, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeCleanupStatus,
    RuntimeEventType,
    RuntimeFailureStage,
    RuntimeLifecycleState,
    RuntimeLogStream,
    RuntimeOperationOutcome,
    RuntimeProcessStatus,
    RuntimeProfileClass,
    RuntimeReadinessState,
    RuntimeRetentionPolicy,
    RuntimeRetryability,
    RuntimeSeverity,
    RuntimeWorkspaceStatus,
)


RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION = 1
TEST_LIFECYCLE_PROBE_PROFILE_ID = "test.lifecycle_probe"
PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID = "pepper.dashboard.provider_null"

StableIdentifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
BoundedMessage = Annotated[str, StringConstraints(min_length=1, max_length=512)]


class _RuntimeAdapterModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
    )

    @staticmethod
    def _utc(value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _no_control_characters(value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("text fields must not contain control characters")
        return value


class RuntimeTimeoutPolicy(_RuntimeAdapterModel):
    readiness_timeout_ms: int = Field(ge=1, le=300_000)
    graceful_shutdown_timeout_ms: int = Field(ge=1, le=60_000)
    forced_termination_timeout_ms: int = Field(ge=1, le=60_000)
    poll_interval_ms: int = Field(ge=50, le=5_000)
    max_stdout_bytes: int = Field(ge=1_024, le=1_048_576)
    max_stderr_bytes: int = Field(ge=1_024, le=1_048_576)

    @model_validator(mode="after")
    def poll_interval_must_be_below_readiness_timeout(self) -> "RuntimeTimeoutPolicy":
        if self.poll_interval_ms >= self.readiness_timeout_ms:
            raise ValueError("poll_interval_ms must be below readiness_timeout_ms")
        return self


class RuntimeProfileRef(_RuntimeAdapterModel):
    profile_id: StableIdentifier
    profile_class: RuntimeProfileClass
    environment_policy_id: StableIdentifier
    workspace_policy_id: StableIdentifier
    readiness_policy_id: StableIdentifier
    shutdown_policy_id: StableIdentifier
    files_root_policy_id: StableIdentifier | None

    @model_validator(mode="after")
    def dashboard_profile_requires_files_root_policy(self) -> "RuntimeProfileRef":
        if (
            self.profile_class is RuntimeProfileClass.PEPPER_DASHBOARD_PROVIDER_NULL
            and self.files_root_policy_id is None
        ):
            raise ValueError("dashboard profiles require files_root_policy_id")
        return self


class RuntimeWorkspaceBinding(_RuntimeAdapterModel):
    workspace_policy_id: StableIdentifier
    retention_policy: RuntimeRetentionPolicy
    require_managed_files_root: bool


class RuntimeWorkspaceRef(_RuntimeAdapterModel):
    workspace_id: StableIdentifier
    workspace_policy_id: StableIdentifier
    status: RuntimeWorkspaceStatus
    managed_files_root_bound: bool


class RuntimeEvidenceRef(_RuntimeAdapterModel):
    evidence_id: StableIdentifier
    evidence_kind: StableIdentifier


class RuntimeLaunchRequest(_RuntimeAdapterModel):
    schema_version: Literal[1]
    runtime_profile_id: StableIdentifier
    workspace_binding: RuntimeWorkspaceBinding
    correlation_id: StableIdentifier
    requested_by: StableIdentifier
    timeout_policy: RuntimeTimeoutPolicy
    evidence_context: tuple[RuntimeEvidenceRef, ...] = Field(max_length=32)


class RuntimeStopRequest(_RuntimeAdapterModel):
    schema_version: Literal[1]
    runtime_id: StableIdentifier
    correlation_id: StableIdentifier
    requested_by: StableIdentifier
    reason_code: StableIdentifier


class RuntimeCancelRequest(_RuntimeAdapterModel):
    schema_version: Literal[1]
    runtime_id: StableIdentifier
    correlation_id: StableIdentifier
    requested_by: StableIdentifier
    reason_code: StableIdentifier


class RuntimeRollbackRequest(_RuntimeAdapterModel):
    schema_version: Literal[1]
    runtime_id: StableIdentifier
    correlation_id: StableIdentifier
    requested_by: StableIdentifier
    reason_code: StableIdentifier


class RuntimeHandle(_RuntimeAdapterModel):
    schema_version: Literal[1]
    runtime_id: StableIdentifier
    correlation_id: StableIdentifier
    profile_id: StableIdentifier
    workspace_id: StableIdentifier
    lifecycle_state: RuntimeLifecycleState
    created_at_utc: datetime

    @field_validator("created_at_utc", mode="after")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)  # type: ignore[return-value]


class RuntimeProcessRef(_RuntimeAdapterModel):
    launcher_pid: PositiveInt | None
    listener_pid: PositiveInt | None
    descendant_pids: tuple[PositiveInt, ...]
    process_status: RuntimeProcessStatus
    started_at_utc: datetime | None
    exited_at_utc: datetime | None
    exit_code: int | None

    @field_validator("started_at_utc", "exited_at_utc", mode="after")
    @classmethod
    def process_datetimes_must_be_utc(cls, value: datetime | None) -> datetime | None:
        return cls._utc(value)

    @model_validator(mode="after")
    def process_evidence_must_be_consistent(self) -> "RuntimeProcessRef":
        if len(self.descendant_pids) != len(set(self.descendant_pids)):
            raise ValueError("descendant_pids must be unique")
        if self.launcher_pid is not None and self.launcher_pid in self.descendant_pids:
            raise ValueError("launcher_pid must not repeat in descendant_pids")
        if (
            self.listener_pid is not None
            and self.listener_pid != self.launcher_pid
            and self.listener_pid in self.descendant_pids
        ):
            raise ValueError("listener_pid must not repeat in descendant_pids")
        if (
            self.process_status is RuntimeProcessStatus.RUNNING
            and self.exited_at_utc is not None
        ):
            raise ValueError("running process status forbids exited_at_utc")
        if self.exited_at_utc is not None and self.process_status in {
            RuntimeProcessStatus.NOT_STARTED,
            RuntimeProcessStatus.STARTING,
            RuntimeProcessStatus.RUNNING,
        }:
            raise ValueError("exited_at_utc requires a non-running process status")
        if self.exit_code is not None and self.exited_at_utc is None:
            raise ValueError("exit_code requires exited_at_utc")
        return self


class RuntimeReadinessRef(_RuntimeAdapterModel):
    probe_id: StableIdentifier
    state: RuntimeReadinessState
    attempt_count: int = Field(ge=0)
    deadline_at_utc: datetime
    observed_at_utc: datetime | None
    listener_port: int | None = Field(default=None, ge=1, le=65_535)

    @field_validator("deadline_at_utc", "observed_at_utc", mode="after")
    @classmethod
    def readiness_datetimes_must_be_utc(cls, value: datetime | None) -> datetime | None:
        return cls._utc(value)

    @model_validator(mode="after")
    def readiness_evidence_must_be_consistent(self) -> "RuntimeReadinessRef":
        if self.state is RuntimeReadinessState.READY and self.observed_at_utc is None:
            raise ValueError("ready state requires observed_at_utc")
        if self.state is RuntimeReadinessState.NOT_STARTED and self.attempt_count != 0:
            raise ValueError("not_started state requires attempt_count == 0")
        if (
            self.observed_at_utc is not None
            and self.observed_at_utc > self.deadline_at_utc
            and self.state is not RuntimeReadinessState.TIMED_OUT
        ):
            raise ValueError("observed_at_utc must not exceed deadline_at_utc")
        return self


class RuntimeLogRef(_RuntimeAdapterModel):
    stream: RuntimeLogStream
    evidence_ref: RuntimeEvidenceRef
    captured_bytes: int = Field(ge=0)
    truncated: bool


class RuntimeEvent(_RuntimeAdapterModel):
    schema_version: Literal[1]
    event_id: StableIdentifier
    runtime_id: StableIdentifier
    correlation_id: StableIdentifier
    sequence: int = Field(ge=0)
    event_type: RuntimeEventType
    lifecycle_state: RuntimeLifecycleState
    profile_id: StableIdentifier
    timestamp_utc: datetime
    monotonic_offset_ms: int = Field(ge=0)
    stage: RuntimeFailureStage
    severity: RuntimeSeverity
    message_code: StableIdentifier
    sanitized_message: BoundedMessage
    process_reference: RuntimeEvidenceRef | None
    workspace_reference: RuntimeEvidenceRef | None
    readiness_reference: RuntimeEvidenceRef | None
    failure_reference: RuntimeEvidenceRef | None

    @field_validator("timestamp_utc", mode="after")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)  # type: ignore[return-value]

    @field_validator("sanitized_message")
    @classmethod
    def event_message_must_be_bounded(cls, value: str) -> str:
        return cls._no_control_characters(value)


class RuntimeFailure(_RuntimeAdapterModel):
    schema_version: Literal[1]
    failure_id: StableIdentifier
    runtime_id: StableIdentifier
    profile_id: StableIdentifier
    stage: RuntimeFailureStage
    failure_code: StableIdentifier
    sanitized_summary: BoundedMessage
    retryability: RuntimeRetryability
    cleanup_status: RuntimeCleanupStatus
    process_status: RuntimeProcessStatus
    workspace_status: RuntimeWorkspaceStatus
    evidence_refs: tuple[RuntimeEvidenceRef, ...] = Field(max_length=32)

    @field_validator("sanitized_summary")
    @classmethod
    def failure_summary_must_be_bounded(cls, value: str) -> str:
        return cls._no_control_characters(value)

    @model_validator(mode="after")
    def evidence_refs_must_be_unique(self) -> "RuntimeFailure":
        evidence_ids = [ref.evidence_id for ref in self.evidence_refs]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence_refs must have unique evidence IDs")
        return self


class RuntimeOperationResult(_RuntimeAdapterModel):
    _SUCCESSFUL_OUTCOMES: ClassVar[frozenset[RuntimeOperationOutcome]] = frozenset({
        RuntimeOperationOutcome.ACCEPTED,
        RuntimeOperationOutcome.READY,
        RuntimeOperationOutcome.STOPPED,
        RuntimeOperationOutcome.CANCELLED,
        RuntimeOperationOutcome.ROLLED_BACK,
    })
    _OUTCOME_STATES: ClassVar[
        dict[RuntimeOperationOutcome, frozenset[RuntimeLifecycleState]]
    ] = {
        RuntimeOperationOutcome.ACCEPTED: frozenset({
            RuntimeLifecycleState.CREATED,
            RuntimeLifecycleState.VALIDATING,
            RuntimeLifecycleState.STARTING,
            RuntimeLifecycleState.WAITING_FOR_READINESS,
            RuntimeLifecycleState.CANCELLATION_REQUESTED,
            RuntimeLifecycleState.STOPPING,
            RuntimeLifecycleState.ROLLBACK_PENDING,
        }),
        RuntimeOperationOutcome.READY: frozenset({RuntimeLifecycleState.READY}),
        RuntimeOperationOutcome.STOPPED: frozenset({RuntimeLifecycleState.STOPPED}),
        RuntimeOperationOutcome.CANCELLED: frozenset({RuntimeLifecycleState.CANCELLED}),
        RuntimeOperationOutcome.FAILED: frozenset({RuntimeLifecycleState.FAILED}),
        RuntimeOperationOutcome.ROLLED_BACK: frozenset({
            RuntimeLifecycleState.ROLLED_BACK
        }),
        RuntimeOperationOutcome.ROLLBACK_FAILED: frozenset({
            RuntimeLifecycleState.ROLLBACK_FAILED,
        }),
    }

    schema_version: Literal[1]
    runtime_handle: RuntimeHandle
    outcome: RuntimeOperationOutcome
    process_reference: RuntimeProcessRef | None
    workspace_reference: RuntimeWorkspaceRef | None
    readiness_reference: RuntimeReadinessRef | None
    log_references: tuple[RuntimeLogRef, ...] = Field(max_length=2)
    failure: RuntimeFailure | None
    events: tuple[RuntimeEvent, ...] = Field(max_length=256)

    @model_validator(mode="after")
    def result_envelope_must_be_consistent(self) -> "RuntimeOperationResult":
        streams = [ref.stream for ref in self.log_references]
        if len(streams) != len(set(streams)):
            raise ValueError("log_references may contain only one reference per stream")
        event_ids = [event.event_id for event in self.events]
        if len(event_ids) != len(set(event_ids)):
            raise ValueError("events must have unique event IDs")
        sequences = [event.sequence for event in self.events]
        if any(left >= right for left, right in zip(sequences, sequences[1:])):
            raise ValueError("events must be strictly ordered by sequence")
        for event in self.events:
            if event.runtime_id != self.runtime_handle.runtime_id:
                raise ValueError("event runtime_id must match runtime handle")
            if event.correlation_id != self.runtime_handle.correlation_id:
                raise ValueError("event correlation_id must match runtime handle")
            if event.profile_id != self.runtime_handle.profile_id:
                raise ValueError("event profile_id must match runtime handle")
        if self.failure is not None:
            if self.failure.runtime_id != self.runtime_handle.runtime_id:
                raise ValueError("failure runtime_id must match runtime handle")
            if self.failure.profile_id != self.runtime_handle.profile_id:
                raise ValueError("failure profile_id must match runtime handle")
        if self.outcome in self._SUCCESSFUL_OUTCOMES and self.failure is not None:
            raise ValueError("successful outcomes forbid failure")
        if (
            self.outcome
            in {
                RuntimeOperationOutcome.FAILED,
                RuntimeOperationOutcome.ROLLBACK_FAILED,
            }
            and self.failure is None
        ):
            raise ValueError("failed outcomes require failure")
        allowed_states = self._OUTCOME_STATES[self.outcome]
        if self.runtime_handle.lifecycle_state not in allowed_states:
            raise ValueError(
                "outcome is incompatible with runtime_handle lifecycle_state"
            )
        return self
