"""Internal non-authoritative audit projection for runtime adapter evidence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    RuntimeEvent,
    RuntimeEvidenceRef,
    RuntimeFailure,
    RuntimeOperationResult,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeCleanupStatus,
    RuntimeEventType,
    RuntimeFailureStage,
    RuntimeLifecycleState,
    RuntimeOperationOutcome,
    RuntimeProcessStatus,
    RuntimeRetryability,
    RuntimeSeverity,
    RuntimeWorkspaceStatus,
)


RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION = 1

_MAX_EVENT_EVIDENCE_REFERENCES = 4
_MAX_LOG_EVIDENCE_REFERENCES = 2
_MAX_ERROR_FIELD_CHARACTERS = 160
_STABLE_IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class RuntimeAuditNormalizationError(RuntimeError):
    """Base class for bounded audit-projection normalization errors."""

    error_code = "runtime_audit_normalization_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        event_id: str | None = None,
        failure_id: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.event_id = _safe_text(event_id) if event_id is not None else None
        self.failure_id = _safe_text(failure_id) if failure_id is not None else None
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.event_id is not None:
            fragments.append(f"event_id={self.event_id}")
        if self.failure_id is not None:
            fragments.append(f"failure_id={self.failure_id}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        super().__init__(" ".join(fragments))


class RuntimeAuditEventOrderError(RuntimeAuditNormalizationError):
    error_code = "runtime_audit_event_order_error"


class RuntimeAuditEvidenceReferenceError(RuntimeAuditNormalizationError):
    error_code = "runtime_audit_evidence_reference_error"


class _RuntimeAuditModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", validate_default=True)

    @staticmethod
    def _utc(value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _no_control_characters(value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("text fields must not contain control characters")
        return value


class RuntimeAuditEventProjection(_RuntimeAuditModel):
    """Safe event facts projected for audit consumers."""

    schema_version: Literal[1]
    event_id: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    sequence: int = Field(ge=0)
    event_type: RuntimeEventType
    lifecycle_state: RuntimeLifecycleState
    timestamp_utc: datetime
    monotonic_offset_ms: int = Field(ge=0)
    stage: RuntimeFailureStage
    severity: RuntimeSeverity
    message_code: str = Field(min_length=1, max_length=128)
    sanitized_message: str = Field(min_length=1, max_length=512)
    evidence_refs: tuple[RuntimeEvidenceRef, ...] = Field(
        max_length=_MAX_EVENT_EVIDENCE_REFERENCES
    )

    @field_validator("timestamp_utc", mode="after")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @field_validator("message_code", "sanitized_message")
    @classmethod
    def text_must_be_bounded(cls, value: str) -> str:
        return cls._no_control_characters(value)

    @model_validator(mode="after")
    def evidence_refs_must_be_sorted_and_unique(self) -> "RuntimeAuditEventProjection":
        _assert_sorted_unique_evidence_refs(self.evidence_refs)
        return self


class RuntimeAuditFailureProjection(_RuntimeAuditModel):
    """Safe failure facts projected for audit consumers."""

    schema_version: Literal[1]
    failure_id: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    stage: RuntimeFailureStage
    failure_code: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    sanitized_summary: str = Field(min_length=1, max_length=512)
    retryability: RuntimeRetryability
    cleanup_status: RuntimeCleanupStatus
    process_status: RuntimeProcessStatus
    workspace_status: RuntimeWorkspaceStatus
    evidence_refs: tuple[RuntimeEvidenceRef, ...] = Field(max_length=32)

    @field_validator("sanitized_summary")
    @classmethod
    def summary_must_be_bounded(cls, value: str) -> str:
        return cls._no_control_characters(value)

    @model_validator(mode="after")
    def evidence_refs_must_be_sorted_and_unique(
        self,
    ) -> "RuntimeAuditFailureProjection":
        _assert_sorted_unique_evidence_refs(self.evidence_refs)
        return self


class RuntimeAuditProjection(_RuntimeAuditModel):
    """Non-authoritative immutable runtime audit projection."""

    schema_version: Literal[1]
    projection_kind: Literal["runtime_audit_projection"]
    authority: Literal["non_authoritative"]
    runtime_id: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    correlation_id: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    profile_id: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    workspace_id: str = Field(pattern=_STABLE_IDENTIFIER_PATTERN)
    lifecycle_state: RuntimeLifecycleState
    outcome: RuntimeOperationOutcome
    created_at_utc: datetime
    event_count: int = Field(ge=0, le=256)
    events: tuple[RuntimeAuditEventProjection, ...] = Field(max_length=256)
    failure: RuntimeAuditFailureProjection | None
    log_evidence_refs: tuple[RuntimeEvidenceRef, ...] = Field(
        max_length=_MAX_LOG_EVIDENCE_REFERENCES
    )
    process_evidence_present: bool
    workspace_evidence_present: bool
    readiness_evidence_present: bool

    @field_validator("created_at_utc", mode="after")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @model_validator(mode="after")
    def projection_must_be_consistent(self) -> "RuntimeAuditProjection":
        if self.event_count != len(self.events):
            raise ValueError("event_count must match events length")
        sequences = [event.sequence for event in self.events]
        if any(left >= right for left, right in zip(sequences, sequences[1:])):
            raise ValueError("events must be strictly ordered by sequence")
        _assert_sorted_unique_evidence_refs(self.log_evidence_refs)
        return self


def project_runtime_operation_audit(
    result: RuntimeOperationResult,
) -> RuntimeAuditProjection:
    """Project one operation result into a safe, non-persistent audit DTO."""

    _validate_event_order(result)
    _validate_failure_references(result)
    events = tuple(_project_event(event) for event in result.events)
    failure = _project_failure(result.failure)
    log_evidence_refs = _normalize_evidence_refs(
        tuple(ref.evidence_ref for ref in result.log_references),
        runtime_id=result.runtime_handle.runtime_id,
        event_id=None,
        validation_category="duplicate_log_evidence_ref",
    )
    return RuntimeAuditProjection(
        schema_version=RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION,
        projection_kind="runtime_audit_projection",
        authority="non_authoritative",
        runtime_id=result.runtime_handle.runtime_id,
        correlation_id=result.runtime_handle.correlation_id,
        profile_id=result.runtime_handle.profile_id,
        workspace_id=result.runtime_handle.workspace_id,
        lifecycle_state=result.runtime_handle.lifecycle_state,
        outcome=result.outcome,
        created_at_utc=result.runtime_handle.created_at_utc,
        event_count=len(events),
        events=events,
        failure=failure,
        log_evidence_refs=log_evidence_refs,
        process_evidence_present=result.process_reference is not None,
        workspace_evidence_present=result.workspace_reference is not None,
        readiness_evidence_present=result.readiness_reference is not None,
    )


def _project_event(event: RuntimeEvent) -> RuntimeAuditEventProjection:
    return RuntimeAuditEventProjection(
        schema_version=RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION,
        event_id=event.event_id,
        sequence=event.sequence,
        event_type=event.event_type,
        lifecycle_state=event.lifecycle_state,
        timestamp_utc=event.timestamp_utc,
        monotonic_offset_ms=event.monotonic_offset_ms,
        stage=event.stage,
        severity=event.severity,
        message_code=event.message_code,
        sanitized_message=event.sanitized_message,
        evidence_refs=_event_evidence_refs(event),
    )


def _project_failure(
    failure: RuntimeFailure | None,
) -> RuntimeAuditFailureProjection | None:
    if failure is None:
        return None
    return RuntimeAuditFailureProjection(
        schema_version=RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION,
        failure_id=failure.failure_id,
        stage=failure.stage,
        failure_code=failure.failure_code,
        sanitized_summary=failure.sanitized_summary,
        retryability=failure.retryability,
        cleanup_status=failure.cleanup_status,
        process_status=failure.process_status,
        workspace_status=failure.workspace_status,
        evidence_refs=_normalize_evidence_refs(
            failure.evidence_refs,
            runtime_id=failure.runtime_id,
            event_id=None,
            validation_category="duplicate_failure_evidence_ref",
        ),
    )


def _event_evidence_refs(event: RuntimeEvent) -> tuple[RuntimeEvidenceRef, ...]:
    return _normalize_evidence_refs(
        tuple(
            ref
            for ref in (
                event.process_reference,
                event.workspace_reference,
                event.readiness_reference,
                event.failure_reference,
            )
            if ref is not None
        ),
        runtime_id=event.runtime_id,
        event_id=event.event_id,
        validation_category="duplicate_event_evidence_ref",
    )


def _validate_event_order(result: RuntimeOperationResult) -> None:
    previous_timestamp: datetime | None = None
    previous_offset: int | None = None
    previous_sequence: int | None = None
    for event in result.events:
        if previous_sequence is not None and event.sequence <= previous_sequence:
            raise RuntimeAuditEventOrderError(
                runtime_id=result.runtime_handle.runtime_id,
                event_id=event.event_id,
                validation_category="sequence_not_increasing",
            )
        if previous_timestamp is not None and event.timestamp_utc < previous_timestamp:
            raise RuntimeAuditEventOrderError(
                runtime_id=result.runtime_handle.runtime_id,
                event_id=event.event_id,
                validation_category="timestamp_decreased",
            )
        if previous_offset is not None and event.monotonic_offset_ms < previous_offset:
            raise RuntimeAuditEventOrderError(
                runtime_id=result.runtime_handle.runtime_id,
                event_id=event.event_id,
                validation_category="monotonic_offset_decreased",
            )
        previous_sequence = event.sequence
        previous_timestamp = event.timestamp_utc
        previous_offset = event.monotonic_offset_ms


def _validate_failure_references(result: RuntimeOperationResult) -> None:
    failure_ref = (
        RuntimeEvidenceRef(
            evidence_id=result.failure.failure_id,
            evidence_kind="runtime_failure",
        )
        if result.failure is not None
        else None
    )
    events_with_failure_refs = tuple(
        event for event in result.events if event.failure_reference is not None
    )
    for event in events_with_failure_refs:
        if failure_ref is None or event.failure_reference != failure_ref:
            raise RuntimeAuditEvidenceReferenceError(
                runtime_id=result.runtime_handle.runtime_id,
                event_id=event.event_id,
                validation_category="failure_reference_mismatch",
            )
    if result.failure is not None and not events_with_failure_refs:
        raise RuntimeAuditEvidenceReferenceError(
            runtime_id=result.runtime_handle.runtime_id,
            failure_id=result.failure.failure_id,
            validation_category="failure_event_reference_missing",
        )


def _normalize_evidence_refs(
    refs: tuple[RuntimeEvidenceRef, ...],
    *,
    runtime_id: str,
    event_id: str | None,
    validation_category: str,
) -> tuple[RuntimeEvidenceRef, ...]:
    evidence_ids = [ref.evidence_id for ref in refs]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise RuntimeAuditEvidenceReferenceError(
            runtime_id=runtime_id,
            event_id=event_id,
            validation_category=validation_category,
        )
    return tuple(sorted(refs, key=lambda ref: (ref.evidence_kind, ref.evidence_id)))


def _assert_sorted_unique_evidence_refs(refs: tuple[RuntimeEvidenceRef, ...]) -> None:
    normalized = tuple(
        sorted(refs, key=lambda ref: (ref.evidence_kind, ref.evidence_id))
    )
    if refs != normalized:
        raise ValueError("evidence_refs must be sorted")
    evidence_ids = [ref.evidence_id for ref in refs]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("evidence_refs must have unique evidence IDs")


__all__ = [
    "RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION",
    "RuntimeAuditEventOrderError",
    "RuntimeAuditEventProjection",
    "RuntimeAuditEvidenceReferenceError",
    "RuntimeAuditFailureProjection",
    "RuntimeAuditNormalizationError",
    "RuntimeAuditProjection",
    "project_runtime_operation_audit",
]
