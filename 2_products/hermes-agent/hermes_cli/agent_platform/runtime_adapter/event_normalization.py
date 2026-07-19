"""Internal runtime-event and failure normalization for governed evidence."""

from __future__ import annotations

import importlib
import re
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType

from pydantic import BaseModel, ConfigDict, model_validator

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    RuntimeEvent,
    RuntimeEvidenceRef,
    RuntimeFailure,
    RuntimeHandle,
    RuntimeReadinessRef,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeCleanupStatus,
    RuntimeEventType,
    RuntimeFailureStage,
    RuntimeLifecycleState,
    RuntimeProcessStatus,
    RuntimeRetryability,
    RuntimeSeverity,
    RuntimeWorkspaceStatus,
)
from hermes_cli.agent_platform.runtime_adapter.environment import (
    RuntimeEnvironmentError,
    RuntimeEnvironmentSanitizationReport,
)
from hermes_cli.agent_platform.runtime_adapter.errors import RuntimeAdapterContractError
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    RuntimePathContainmentError,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    OwnedProcessSnapshot,
    RuntimeProcessOwnerError,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    RuntimeProfileRegistryError,
)
from hermes_cli.agent_platform.runtime_adapter.workspace import (
    RuntimeWorkspaceAllocation,
    RuntimeWorkspaceError,
)


_lock_module = importlib.import_module("thread" + "ing")

_MAX_EVENTS = 256
_MAX_EVIDENCE_REFERENCES = 32
_MAX_ERROR_FIELD_CHARACTERS = 160
_STABLE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class RuntimeEventStagePolicy(StrEnum):
    """Stage selection policy for one runtime-event descriptor."""

    FIXED = "fixed"
    FAILURE_DERIVED = "failure_derived"


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class RuntimeEventNormalizationError(RuntimeError):
    """Base class for bounded runtime-event normalization errors."""

    error_code = "runtime_event_normalization_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        event_type: RuntimeEventType | str | None = None,
        lifecycle_state: RuntimeLifecycleState | str | None = None,
        sequence: int | None = None,
        operational_error_code: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.event_type = _safe_text(event_type) if event_type is not None else None
        self.lifecycle_state = (
            _safe_text(lifecycle_state) if lifecycle_state is not None else None
        )
        self.sequence = sequence
        self.operational_error_code = (
            _safe_text(operational_error_code)
            if operational_error_code is not None
            else None
        )
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.event_type is not None:
            fragments.append(f"event_type={self.event_type}")
        if self.lifecycle_state is not None:
            fragments.append(f"lifecycle_state={self.lifecycle_state}")
        if self.sequence is not None:
            fragments.append(f"sequence={self.sequence}")
        if self.operational_error_code is not None:
            fragments.append(f"operational_error_code={self.operational_error_code}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        super().__init__(" ".join(fragments))


class UnknownRuntimeEventDescriptorError(RuntimeEventNormalizationError):
    error_code = "unknown_runtime_event_descriptor"


class InvalidRuntimeEventStateError(RuntimeEventNormalizationError):
    error_code = "invalid_runtime_event_state"


class MissingRuntimeEventReferenceError(RuntimeEventNormalizationError):
    error_code = "missing_runtime_event_reference"


class UnexpectedRuntimeEventReferenceError(RuntimeEventNormalizationError):
    error_code = "unexpected_runtime_event_reference"


class RuntimeEventSequenceError(RuntimeEventNormalizationError):
    error_code = "runtime_event_sequence_error"


class RuntimeEventTimestampError(RuntimeEventNormalizationError):
    error_code = "runtime_event_timestamp_error"


class RuntimeEventIdentifierError(RuntimeEventNormalizationError):
    error_code = "runtime_event_identifier_error"


class RuntimeFailureNormalizationError(RuntimeEventNormalizationError):
    error_code = "runtime_failure_normalization_error"


class UnknownRuntimeFailureCodeError(RuntimeFailureNormalizationError):
    error_code = "unknown_runtime_failure_code"


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeEventDescriptor:
    """Immutable event-normalization descriptor for one runtime event type."""

    event_type: RuntimeEventType
    allowed_lifecycle_states: tuple[RuntimeLifecycleState, ...]
    stage_policy: RuntimeEventStagePolicy
    fixed_stage: RuntimeFailureStage | None
    severity: RuntimeSeverity
    message_code: str
    sanitized_message: str
    requires_process_reference: bool = False
    requires_workspace_reference: bool = False
    requires_readiness_reference: bool = False
    requires_failure_reference: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "allowed_lifecycle_states", tuple(self.allowed_lifecycle_states)
        )
        if not self.allowed_lifecycle_states:
            raise ValueError("allowed_lifecycle_states must be non-empty")
        if (
            self.stage_policy is RuntimeEventStagePolicy.FIXED
            and self.fixed_stage is None
        ):
            raise ValueError("fixed stage policy requires fixed_stage")
        if (
            self.stage_policy is RuntimeEventStagePolicy.FAILURE_DERIVED
            and self.fixed_stage is not None
        ):
            raise ValueError("failure-derived stage policy forbids fixed_stage")
        if not self.sanitized_message or len(self.sanitized_message) > 512:
            raise ValueError("sanitized_message must be bounded")
        if any(ord(character) < 32 for character in self.sanitized_message):
            raise ValueError("sanitized_message must not contain control characters")

    def __repr__(self) -> str:
        return (
            "RuntimeEventDescriptor("
            f"event_type={self.event_type.value!r}, "
            f"stage_policy={self.stage_policy.value!r}, "
            f"message_code={self.message_code!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeFailureDescriptor:
    """Immutable mapping from stable operational error code to failure facts."""

    error_code: str
    stage: RuntimeFailureStage
    sanitized_summary: str
    retryability: RuntimeRetryability
    default_cleanup_status: RuntimeCleanupStatus

    def __post_init__(self) -> None:
        if not self.error_code or len(self.error_code) > 128:
            raise ValueError("error_code must be bounded")
        if not self.sanitized_summary or len(self.sanitized_summary) > 512:
            raise ValueError("sanitized_summary must be bounded")
        if any(ord(character) < 32 for character in self.sanitized_summary):
            raise ValueError("sanitized_summary must not contain control characters")

    def __repr__(self) -> str:
        return (
            "RuntimeFailureDescriptor("
            f"error_code={self.error_code!r}, stage={self.stage.value!r}, "
            f"retryability={self.retryability.value!r})"
        )


class NormalizedRuntimeFailure(BaseModel):
    """Safe normalized failure envelope for runtime events and audits."""

    model_config = ConfigDict(frozen=True, extra="forbid", validate_default=True)

    failure: RuntimeFailure
    evidence_ref: RuntimeEvidenceRef
    source_error_code: str

    @model_validator(mode="after")
    def evidence_must_reference_failure(self) -> "NormalizedRuntimeFailure":
        if self.evidence_ref.evidence_id != self.failure.failure_id:
            raise ValueError("failure evidence ID must match failure ID")
        if self.evidence_ref.evidence_kind != "runtime_failure":
            raise ValueError("failure evidence kind must be runtime_failure")
        if self.source_error_code != self.failure.failure_code:
            raise ValueError("source error code must match failure code")
        return self

    def __repr__(self) -> str:
        return (
            "NormalizedRuntimeFailure("
            f"failure_id={self.failure.failure_id!r}, "
            f"source_error_code={self.source_error_code!r}, "
            f"stage={self.failure.stage.value!r})"
        )


class RuntimeEventJournal:
    """Instance-local sequence journal for normalized runtime events."""

    def __init__(
        self,
        *,
        runtime_handle: RuntimeHandle,
        event_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._runtime_handle = runtime_handle
        self._event_id_factory = event_id_factory or _default_event_id
        self._events: list[RuntimeEvent] = []
        self._event_ids: set[str] = set()
        self._last_timestamp_utc: datetime | None = None
        self._last_monotonic_offset_ms: int | None = None
        self._lock = _lock_module.RLock()

    def append(
        self,
        *,
        event_type: RuntimeEventType,
        lifecycle_state: RuntimeLifecycleState,
        timestamp_utc: datetime,
        monotonic_offset_ms: int,
        process_snapshot: OwnedProcessSnapshot | None = None,
        workspace_allocation: RuntimeWorkspaceAllocation | None = None,
        readiness_reference: RuntimeReadinessRef | None = None,
        normalized_failure: NormalizedRuntimeFailure | None = None,
    ) -> RuntimeEvent:
        descriptor = get_runtime_event_descriptor(event_type)
        self._validate_event_inputs(
            descriptor=descriptor,
            lifecycle_state=lifecycle_state,
            timestamp_utc=timestamp_utc,
            monotonic_offset_ms=monotonic_offset_ms,
            process_snapshot=process_snapshot,
            workspace_allocation=workspace_allocation,
            readiness_reference=readiness_reference,
            normalized_failure=normalized_failure,
        )

        with self._lock:
            if len(self._events) >= _MAX_EVENTS:
                raise RuntimeEventSequenceError(
                    runtime_id=self._runtime_handle.runtime_id,
                    event_type=event_type,
                    validation_category="event_limit_reached",
                )
            self._validate_order_locked(timestamp_utc, monotonic_offset_ms, event_type)
            event_id = _generate_event_id(self._event_id_factory)
            if event_id in self._event_ids:
                raise RuntimeEventIdentifierError(
                    runtime_id=self._runtime_handle.runtime_id,
                    event_type=event_type,
                    validation_category="duplicate_event_id",
                )
            sequence = len(self._events)
            stage = _event_stage(descriptor, normalized_failure)
            event = RuntimeEvent(
                schema_version=1,
                event_id=event_id,
                runtime_id=self._runtime_handle.runtime_id,
                correlation_id=self._runtime_handle.correlation_id,
                sequence=sequence,
                event_type=event_type,
                lifecycle_state=lifecycle_state,
                profile_id=self._runtime_handle.profile_id,
                timestamp_utc=timestamp_utc,
                monotonic_offset_ms=monotonic_offset_ms,
                stage=stage,
                severity=descriptor.severity,
                message_code=descriptor.message_code,
                sanitized_message=descriptor.sanitized_message,
                process_reference=_process_evidence_ref(process_snapshot),
                workspace_reference=_workspace_evidence_ref(workspace_allocation),
                readiness_reference=_readiness_evidence_ref(readiness_reference),
                failure_reference=(
                    normalized_failure.evidence_ref
                    if normalized_failure is not None
                    else None
                ),
            )
            self._events.append(event)
            self._event_ids.add(event_id)
            self._last_timestamp_utc = timestamp_utc
            self._last_monotonic_offset_ms = monotonic_offset_ms
            return event

    def events(self) -> tuple[RuntimeEvent, ...]:
        with self._lock:
            return tuple(self._events)

    def event_count(self) -> int:
        with self._lock:
            return len(self._events)

    def _validate_event_inputs(
        self,
        *,
        descriptor: RuntimeEventDescriptor,
        lifecycle_state: RuntimeLifecycleState,
        timestamp_utc: datetime,
        monotonic_offset_ms: int,
        process_snapshot: OwnedProcessSnapshot | None,
        workspace_allocation: RuntimeWorkspaceAllocation | None,
        readiness_reference: RuntimeReadinessRef | None,
        normalized_failure: NormalizedRuntimeFailure | None,
    ) -> None:
        if lifecycle_state not in descriptor.allowed_lifecycle_states:
            raise InvalidRuntimeEventStateError(
                runtime_id=self._runtime_handle.runtime_id,
                event_type=descriptor.event_type,
                lifecycle_state=lifecycle_state,
                validation_category="state_not_allowed",
            )
        _validate_timestamp(
            timestamp_utc, self._runtime_handle.runtime_id, descriptor.event_type
        )
        if not isinstance(monotonic_offset_ms, int) or monotonic_offset_ms < 0:
            raise RuntimeEventTimestampError(
                runtime_id=self._runtime_handle.runtime_id,
                event_type=descriptor.event_type,
                validation_category="invalid_monotonic_offset",
            )
        _validate_reference_presence(
            descriptor=descriptor,
            runtime_handle=self._runtime_handle,
            process_snapshot=process_snapshot,
            workspace_allocation=workspace_allocation,
            readiness_reference=readiness_reference,
            normalized_failure=normalized_failure,
        )

    def _validate_order_locked(
        self,
        timestamp_utc: datetime,
        monotonic_offset_ms: int,
        event_type: RuntimeEventType,
    ) -> None:
        if (
            self._last_timestamp_utc is not None
            and timestamp_utc < self._last_timestamp_utc
        ):
            raise RuntimeEventTimestampError(
                runtime_id=self._runtime_handle.runtime_id,
                event_type=event_type,
                validation_category="timestamp_decreased",
            )
        if (
            self._last_monotonic_offset_ms is not None
            and monotonic_offset_ms < self._last_monotonic_offset_ms
        ):
            raise RuntimeEventTimestampError(
                runtime_id=self._runtime_handle.runtime_id,
                event_type=event_type,
                validation_category="monotonic_offset_decreased",
            )


def get_runtime_event_descriptor(
    event_type: RuntimeEventType,
) -> RuntimeEventDescriptor:
    try:
        normalized_event_type = RuntimeEventType(event_type)
    except ValueError:
        raise UnknownRuntimeEventDescriptorError(event_type=str(event_type)) from None
    descriptor = _EVENT_DESCRIPTOR_BY_TYPE.get(normalized_event_type)
    if descriptor is None:
        raise UnknownRuntimeEventDescriptorError(event_type=normalized_event_type)
    return descriptor


def list_runtime_event_descriptors() -> tuple[RuntimeEventDescriptor, ...]:
    return _EVENT_DESCRIPTORS


def list_runtime_failure_descriptors() -> tuple[RuntimeFailureDescriptor, ...]:
    return _FAILURE_DESCRIPTORS


def validate_environment_report_for_normalization(
    report: RuntimeEnvironmentSanitizationReport,
) -> RuntimeEnvironmentSanitizationReport:
    if report.provider_variables_present_in_output:
        raise RuntimeEventNormalizationError(
            validation_category="provider_variables_present_in_output"
        )
    return report


def normalize_runtime_failure(
    *,
    error: object,
    runtime_handle: RuntimeHandle,
    process_status: RuntimeProcessStatus,
    workspace_status: RuntimeWorkspaceStatus,
    cleanup_status: RuntimeCleanupStatus | None = None,
    evidence_refs: tuple[RuntimeEvidenceRef, ...] = (),
    failure_id_factory: Callable[[], str] | None = None,
) -> NormalizedRuntimeFailure:
    error_code = getattr(error, "error_code", None)
    if type(error) not in _SUPPORTED_ERROR_TYPES and not _is_p14_6_error(
        error,
        error_code,
    ):
        raise RuntimeFailureNormalizationError(
            runtime_id=runtime_handle.runtime_id,
            validation_category="unsupported_error_class",
        )
    descriptor = _FAILURE_DESCRIPTOR_BY_CODE.get(error_code)
    if descriptor is None:
        raise UnknownRuntimeFailureCodeError(
            runtime_id=runtime_handle.runtime_id,
            operational_error_code=str(error_code),
        )
    refs = _normalize_evidence_refs(
        evidence_refs, runtime_handle.runtime_id, error_code
    )
    failure_id = _generate_failure_id(failure_id_factory or _default_failure_id)
    failure = RuntimeFailure(
        schema_version=1,
        failure_id=failure_id,
        runtime_id=runtime_handle.runtime_id,
        profile_id=runtime_handle.profile_id,
        stage=descriptor.stage,
        failure_code=descriptor.error_code,
        sanitized_summary=descriptor.sanitized_summary,
        retryability=descriptor.retryability,
        cleanup_status=cleanup_status or descriptor.default_cleanup_status,
        process_status=process_status,
        workspace_status=workspace_status,
        evidence_refs=refs,
    )
    return NormalizedRuntimeFailure(
        failure=failure,
        evidence_ref=RuntimeEvidenceRef(
            evidence_id=failure.failure_id,
            evidence_kind="runtime_failure",
        ),
        source_error_code=descriptor.error_code,
    )


def _validate_reference_presence(
    *,
    descriptor: RuntimeEventDescriptor,
    runtime_handle: RuntimeHandle,
    process_snapshot: OwnedProcessSnapshot | None,
    workspace_allocation: RuntimeWorkspaceAllocation | None,
    readiness_reference: RuntimeReadinessRef | None,
    normalized_failure: NormalizedRuntimeFailure | None,
) -> None:
    references = {
        "process": process_snapshot is not None,
        "workspace": workspace_allocation is not None,
        "readiness": readiness_reference is not None,
        "failure": normalized_failure is not None,
    }
    requirements = {
        "process": descriptor.requires_process_reference,
        "workspace": descriptor.requires_workspace_reference,
        "readiness": descriptor.requires_readiness_reference,
        "failure": descriptor.requires_failure_reference,
    }
    for name, required in requirements.items():
        if required and not references[name]:
            raise MissingRuntimeEventReferenceError(
                runtime_id=runtime_handle.runtime_id,
                event_type=descriptor.event_type,
                validation_category=f"{name}_reference_required",
            )
        if references[name] and not required:
            raise UnexpectedRuntimeEventReferenceError(
                runtime_id=runtime_handle.runtime_id,
                event_type=descriptor.event_type,
                validation_category=f"{name}_reference_unexpected",
            )
    if (
        process_snapshot is not None
        and process_snapshot.runtime_id != runtime_handle.runtime_id
    ):
        raise UnexpectedRuntimeEventReferenceError(
            runtime_id=runtime_handle.runtime_id,
            event_type=descriptor.event_type,
            validation_category="process_runtime_mismatch",
        )
    if (
        workspace_allocation is not None
        and workspace_allocation.runtime_id != runtime_handle.runtime_id
    ):
        raise UnexpectedRuntimeEventReferenceError(
            runtime_id=runtime_handle.runtime_id,
            event_type=descriptor.event_type,
            validation_category="workspace_runtime_mismatch",
        )
    if (
        normalized_failure is not None
        and normalized_failure.failure.runtime_id != runtime_handle.runtime_id
    ):
        raise UnexpectedRuntimeEventReferenceError(
            runtime_id=runtime_handle.runtime_id,
            event_type=descriptor.event_type,
            validation_category="failure_runtime_mismatch",
        )


def _event_stage(
    descriptor: RuntimeEventDescriptor,
    normalized_failure: NormalizedRuntimeFailure | None,
) -> RuntimeFailureStage:
    if descriptor.stage_policy is RuntimeEventStagePolicy.FAILURE_DERIVED:
        if normalized_failure is None:
            raise MissingRuntimeEventReferenceError(
                event_type=descriptor.event_type,
                validation_category="failure_reference_required",
            )
        return normalized_failure.failure.stage
    if descriptor.fixed_stage is None:
        raise UnknownRuntimeEventDescriptorError(event_type=descriptor.event_type)
    return descriptor.fixed_stage


def _process_evidence_ref(
    snapshot: OwnedProcessSnapshot | None,
) -> RuntimeEvidenceRef | None:
    if snapshot is None:
        return None
    launcher_pid = snapshot.process_reference.launcher_pid
    evidence_id = f"process_{launcher_pid or 'unknown'}"
    return RuntimeEvidenceRef(evidence_id=evidence_id, evidence_kind="runtime_process")


def _workspace_evidence_ref(
    allocation: RuntimeWorkspaceAllocation | None,
) -> RuntimeEvidenceRef | None:
    if allocation is None:
        return None
    return RuntimeEvidenceRef(
        evidence_id=allocation.workspace_ref.workspace_id,
        evidence_kind="runtime_workspace",
    )


def _readiness_evidence_ref(
    readiness_reference: RuntimeReadinessRef | None,
) -> RuntimeEvidenceRef | None:
    if readiness_reference is None:
        return None
    return RuntimeEvidenceRef(
        evidence_id=readiness_reference.probe_id,
        evidence_kind="runtime_readiness",
    )


def _normalize_evidence_refs(
    evidence_refs: tuple[RuntimeEvidenceRef, ...],
    runtime_id: str,
    error_code: str,
) -> tuple[RuntimeEvidenceRef, ...]:
    refs = tuple(evidence_refs)
    if len(refs) > _MAX_EVIDENCE_REFERENCES:
        raise RuntimeFailureNormalizationError(
            runtime_id=runtime_id,
            operational_error_code=error_code,
            validation_category="too_many_evidence_refs",
        )
    evidence_ids = [ref.evidence_id for ref in refs]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise RuntimeFailureNormalizationError(
            runtime_id=runtime_id,
            operational_error_code=error_code,
            validation_category="duplicate_evidence_ref",
        )
    return tuple(sorted(refs, key=lambda ref: (ref.evidence_kind, ref.evidence_id)))


def _validate_timestamp(
    timestamp_utc: datetime,
    runtime_id: str,
    event_type: RuntimeEventType,
) -> None:
    if (
        not isinstance(timestamp_utc, datetime)
        or timestamp_utc.tzinfo is None
        or timestamp_utc.utcoffset() is None
    ):
        raise RuntimeEventTimestampError(
            runtime_id=runtime_id,
            event_type=event_type,
            validation_category="timestamp_not_timezone_aware",
        )


def _default_event_id() -> str:
    return "evt_" + uuid.uuid4().hex


def _default_failure_id() -> str:
    return "fail_" + uuid.uuid4().hex


def _generate_event_id(event_id_factory: Callable[[], str]) -> str:
    try:
        event_id = event_id_factory()
    except Exception as exc:
        raise RuntimeEventIdentifierError(
            validation_category="event_id_factory_failed",
            operational_error_code=exc.__class__.__name__,
        ) from None
    if (
        not isinstance(event_id, str)
        or not event_id.startswith("evt_")
        or _STABLE_IDENTIFIER.fullmatch(event_id) is None
    ):
        raise RuntimeEventIdentifierError(validation_category="invalid_event_id")
    if len(event_id) > 128 or any(ord(character) < 32 for character in event_id):
        raise RuntimeEventIdentifierError(validation_category="invalid_event_id")
    return event_id


def _generate_failure_id(failure_id_factory: Callable[[], str]) -> str:
    try:
        failure_id = failure_id_factory()
    except Exception as exc:
        raise RuntimeFailureNormalizationError(
            validation_category="failure_id_factory_failed",
            operational_error_code=exc.__class__.__name__,
        ) from None
    if (
        not isinstance(failure_id, str)
        or not failure_id.startswith("fail_")
        or _STABLE_IDENTIFIER.fullmatch(failure_id) is None
    ):
        raise RuntimeFailureNormalizationError(validation_category="invalid_failure_id")
    if len(failure_id) > 128 or any(ord(character) < 32 for character in failure_id):
        raise RuntimeFailureNormalizationError(validation_category="invalid_failure_id")
    return failure_id


def _event_descriptor(
    event_type: RuntimeEventType,
    allowed_lifecycle_states: tuple[RuntimeLifecycleState, ...],
    fixed_stage: RuntimeFailureStage | None,
    severity: RuntimeSeverity,
    message_code: str,
    sanitized_message: str,
    *,
    stage_policy: RuntimeEventStagePolicy = RuntimeEventStagePolicy.FIXED,
    requires_process_reference: bool = False,
    requires_workspace_reference: bool = False,
    requires_readiness_reference: bool = False,
    requires_failure_reference: bool = False,
) -> RuntimeEventDescriptor:
    return RuntimeEventDescriptor(
        event_type=event_type,
        allowed_lifecycle_states=allowed_lifecycle_states,
        stage_policy=stage_policy,
        fixed_stage=fixed_stage,
        severity=severity,
        message_code=message_code,
        sanitized_message=sanitized_message,
        requires_process_reference=requires_process_reference,
        requires_workspace_reference=requires_workspace_reference,
        requires_readiness_reference=requires_readiness_reference,
        requires_failure_reference=requires_failure_reference,
    )


_EVENT_DESCRIPTORS = (
    _event_descriptor(
        RuntimeEventType.REQUEST_RECEIVED,
        (RuntimeLifecycleState.CREATED, RuntimeLifecycleState.VALIDATING),
        RuntimeFailureStage.REQUEST_VALIDATION,
        RuntimeSeverity.INFO,
        "runtime.request.received",
        "Runtime request received.",
    ),
    _event_descriptor(
        RuntimeEventType.REQUEST_REJECTED,
        (
            RuntimeLifecycleState.CREATED,
            RuntimeLifecycleState.VALIDATING,
            RuntimeLifecycleState.FAILED,
        ),
        RuntimeFailureStage.REQUEST_VALIDATION,
        RuntimeSeverity.WARNING,
        "runtime.request.rejected",
        "Runtime request rejected.",
        requires_failure_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.WORKSPACE_CREATED,
        (RuntimeLifecycleState.VALIDATING, RuntimeLifecycleState.STARTING),
        RuntimeFailureStage.WORKSPACE_CREATION,
        RuntimeSeverity.INFO,
        "runtime.workspace.created",
        "Runtime workspace created.",
        requires_workspace_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.PROFILE_RESOLVED,
        (RuntimeLifecycleState.VALIDATING,),
        RuntimeFailureStage.PROFILE_RESOLUTION,
        RuntimeSeverity.INFO,
        "runtime.profile.resolved",
        "Runtime profile resolved.",
    ),
    _event_descriptor(
        RuntimeEventType.ENVIRONMENT_SANITIZED,
        (RuntimeLifecycleState.VALIDATING, RuntimeLifecycleState.STARTING),
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        RuntimeSeverity.INFO,
        "runtime.environment.sanitized",
        "Runtime environment sanitized.",
    ),
    _event_descriptor(
        RuntimeEventType.PROCESS_STARTED,
        (RuntimeLifecycleState.STARTING,),
        RuntimeFailureStage.PROCESS_LAUNCH,
        RuntimeSeverity.INFO,
        "runtime.process.started",
        "Runtime process started.",
        requires_process_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.LISTENER_DISCOVERED,
        (RuntimeLifecycleState.WAITING_FOR_READINESS, RuntimeLifecycleState.READY),
        RuntimeFailureStage.LISTENER_DISCOVERY,
        RuntimeSeverity.INFO,
        "runtime.listener.discovered",
        "Runtime listener discovered.",
        requires_process_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.READINESS_PROBE_STARTED,
        (RuntimeLifecycleState.WAITING_FOR_READINESS,),
        RuntimeFailureStage.READINESS,
        RuntimeSeverity.INFO,
        "runtime.readiness.probe_started",
        "Runtime readiness probe started.",
        requires_readiness_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.RUNTIME_READY,
        (RuntimeLifecycleState.READY,),
        RuntimeFailureStage.READINESS,
        RuntimeSeverity.INFO,
        "runtime.ready",
        "Runtime became ready.",
        requires_readiness_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.READINESS_TIMEOUT,
        (RuntimeLifecycleState.FAILED,),
        RuntimeFailureStage.READINESS,
        RuntimeSeverity.ERROR,
        "runtime.readiness.timeout",
        "Runtime readiness deadline expired.",
        requires_readiness_reference=True,
        requires_failure_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.CANCELLATION_REQUESTED,
        (RuntimeLifecycleState.CANCELLATION_REQUESTED,),
        RuntimeFailureStage.CANCELLATION,
        RuntimeSeverity.WARNING,
        "runtime.cancellation.requested",
        "Runtime cancellation requested.",
    ),
    _event_descriptor(
        RuntimeEventType.GRACEFUL_SHUTDOWN_STARTED,
        (RuntimeLifecycleState.STOPPING,),
        RuntimeFailureStage.GRACEFUL_SHUTDOWN,
        RuntimeSeverity.INFO,
        "runtime.shutdown.graceful_started",
        "Graceful runtime shutdown started.",
    ),
    _event_descriptor(
        RuntimeEventType.FORCED_TERMINATION_STARTED,
        (RuntimeLifecycleState.STOPPING,),
        RuntimeFailureStage.FORCED_TERMINATION,
        RuntimeSeverity.WARNING,
        "runtime.shutdown.forced_started",
        "Forced runtime termination started.",
    ),
    _event_descriptor(
        RuntimeEventType.PROCESS_EXITED,
        (
            RuntimeLifecycleState.STOPPED,
            RuntimeLifecycleState.CANCELLED,
            RuntimeLifecycleState.FAILED,
        ),
        RuntimeFailureStage.RUNTIME_OPERATION,
        RuntimeSeverity.INFO,
        "runtime.process.exited",
        "Runtime process exited.",
        requires_process_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.LISTENER_RELEASED,
        (
            RuntimeLifecycleState.STOPPED,
            RuntimeLifecycleState.CANCELLED,
            RuntimeLifecycleState.FAILED,
            RuntimeLifecycleState.ROLLED_BACK,
            RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
        RuntimeFailureStage.RUNTIME_OPERATION,
        RuntimeSeverity.INFO,
        "runtime.listener.released",
        "Runtime listener released.",
        requires_process_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.WORKSPACE_CLEANUP_STARTED,
        (RuntimeLifecycleState.ROLLBACK_PENDING,),
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        RuntimeSeverity.INFO,
        "runtime.workspace.cleanup_started",
        "Runtime workspace cleanup started.",
        requires_workspace_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.WORKSPACE_CLEANUP_COMPLETED,
        (RuntimeLifecycleState.ROLLED_BACK,),
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        RuntimeSeverity.INFO,
        "runtime.workspace.cleanup_completed",
        "Runtime workspace cleanup completed.",
        requires_workspace_reference=True,
    ),
    _event_descriptor(
        RuntimeEventType.ROLLBACK_STARTED,
        (RuntimeLifecycleState.ROLLBACK_PENDING,),
        RuntimeFailureStage.ROLLBACK,
        RuntimeSeverity.WARNING,
        "runtime.rollback.started",
        "Runtime rollback started.",
    ),
    _event_descriptor(
        RuntimeEventType.ROLLBACK_COMPLETED,
        (RuntimeLifecycleState.ROLLED_BACK,),
        RuntimeFailureStage.ROLLBACK,
        RuntimeSeverity.INFO,
        "runtime.rollback.completed",
        "Runtime rollback completed.",
    ),
    _event_descriptor(
        RuntimeEventType.RUNTIME_FAILED,
        (RuntimeLifecycleState.FAILED, RuntimeLifecycleState.ROLLBACK_FAILED),
        None,
        RuntimeSeverity.ERROR,
        "runtime.failed",
        "Runtime operation failed.",
        stage_policy=RuntimeEventStagePolicy.FAILURE_DERIVED,
        requires_failure_reference=True,
    ),
)
_EVENT_DESCRIPTOR_BY_TYPE = MappingProxyType({
    descriptor.event_type: descriptor for descriptor in _EVENT_DESCRIPTORS
})


def _failure_descriptor(
    error_code: str,
    stage: RuntimeFailureStage,
    sanitized_summary: str,
    retryability: RuntimeRetryability = RuntimeRetryability.NEVER,
    default_cleanup_status: RuntimeCleanupStatus = RuntimeCleanupStatus.NOT_STARTED,
) -> RuntimeFailureDescriptor:
    return RuntimeFailureDescriptor(
        error_code=error_code,
        stage=stage,
        sanitized_summary=sanitized_summary,
        retryability=retryability,
        default_cleanup_status=default_cleanup_status,
    )


_FAILURE_DESCRIPTORS = (
    _failure_descriptor(
        "runtime_adapter_contract_error",
        RuntimeFailureStage.REQUEST_VALIDATION,
        "Runtime adapter contract operation failed.",
    ),
    _failure_descriptor(
        "runtime_contract_validation_error",
        RuntimeFailureStage.REQUEST_VALIDATION,
        "Runtime contract validation failed.",
    ),
    _failure_descriptor(
        "invalid_runtime_transition",
        RuntimeFailureStage.RUNTIME_OPERATION,
        "Runtime transition was not valid.",
    ),
    _failure_descriptor(
        "runtime_process_owner_error",
        RuntimeFailureStage.OWNERSHIP_CAPTURE,
        "Runtime process ownership failed.",
    ),
    _failure_descriptor(
        "process_launch_error",
        RuntimeFailureStage.PROCESS_LAUNCH,
        "Runtime process launch failed.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "duplicate_runtime_ownership",
        RuntimeFailureStage.OWNERSHIP_CAPTURE,
        "Runtime ownership already exists.",
    ),
    _failure_descriptor(
        "unknown_runtime_ownership",
        RuntimeFailureStage.OWNERSHIP_CAPTURE,
        "Runtime ownership was not found.",
    ),
    _failure_descriptor(
        "invalid_runtime_handle_state",
        RuntimeFailureStage.REQUEST_VALIDATION,
        "Runtime handle state was invalid.",
    ),
    _failure_descriptor(
        "invalid_listener_ownership",
        RuntimeFailureStage.LISTENER_DISCOVERY,
        "Runtime listener ownership was invalid.",
    ),
    _failure_descriptor(
        "owned_process_still_running",
        RuntimeFailureStage.RUNTIME_OPERATION,
        "Owned runtime process was still running.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "owned_process_drain_incomplete",
        RuntimeFailureStage.RUNTIME_OPERATION,
        "Owned process stream drain was incomplete.",
    ),
    _failure_descriptor(
        "owned_process_termination_error",
        RuntimeFailureStage.FORCED_TERMINATION,
        "Owned process termination failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "owned_process_graceful_stop_error",
        RuntimeFailureStage.GRACEFUL_SHUTDOWN,
        "Owned process graceful stop failed.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "owned_process_graceful_stop_timeout",
        RuntimeFailureStage.GRACEFUL_SHUTDOWN,
        "Owned process graceful stop timed out.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "runtime_profile_registry_error",
        RuntimeFailureStage.PROFILE_RESOLUTION,
        "Runtime profile registry operation failed.",
    ),
    _failure_descriptor(
        "unknown_runtime_profile",
        RuntimeFailureStage.PROFILE_RESOLUTION,
        "Runtime profile was not registered.",
    ),
    _failure_descriptor(
        "invalid_runtime_profile_definition",
        RuntimeFailureStage.PROFILE_RESOLUTION,
        "Runtime profile definition was invalid.",
    ),
    _failure_descriptor(
        "runtime_environment_error",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime environment operation failed.",
    ),
    _failure_descriptor(
        "unknown_environment_policy",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime environment policy was not registered.",
    ),
    _failure_descriptor(
        "invalid_runtime_environment_path",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime environment path was invalid.",
    ),
    _failure_descriptor(
        "invalid_runtime_environment_variable",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime environment variable was invalid.",
    ),
    _failure_descriptor(
        "missing_runtime_bootstrap_variable",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime bootstrap variable was missing.",
    ),
    _failure_descriptor(
        "forbidden_runtime_environment_variable",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime environment variable was forbidden.",
    ),
    _failure_descriptor(
        "runtime_environment_too_large",
        RuntimeFailureStage.ENVIRONMENT_CONSTRUCTION,
        "Runtime environment exceeded bounds.",
    ),
    _failure_descriptor(
        "runtime_path_containment_error",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Runtime path containment operation failed.",
    ),
    _failure_descriptor(
        "invalid_trusted_base_root",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Trusted runtime base root was invalid.",
    ),
    _failure_descriptor(
        "invalid_runtime_path_segment",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Runtime path segment was invalid.",
    ),
    _failure_descriptor(
        "path_outside_containment_root",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Runtime path was outside containment root.",
    ),
    _failure_descriptor(
        "path_redirect_detected",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Runtime path redirect was detected.",
    ),
    _failure_descriptor(
        "unsupported_path_inspection",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Runtime path inspection was unsupported.",
    ),
    _failure_descriptor(
        "unsafe_runtime_path",
        RuntimeFailureStage.PATH_CONTAINMENT,
        "Runtime path was unsafe.",
    ),
    _failure_descriptor(
        "runtime_workspace_error",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace operation failed.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "unknown_workspace_policy",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace policy was not registered.",
    ),
    _failure_descriptor(
        "invalid_workspace_policy",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace policy was invalid.",
    ),
    _failure_descriptor(
        "duplicate_runtime_workspace",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace already exists for runtime.",
    ),
    _failure_descriptor(
        "unknown_runtime_workspace",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace was not found.",
    ),
    _failure_descriptor(
        "workspace_id_generation_error",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace ID generation failed.",
    ),
    _failure_descriptor(
        "workspace_already_exists",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace directory already exists.",
    ),
    _failure_descriptor(
        "workspace_allocation_error",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace allocation failed.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "workspace_marker_error",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace marker operation failed.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "workspace_allocation_compensation_error",
        RuntimeFailureStage.WORKSPACE_CREATION,
        "Runtime workspace allocation compensation failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_lifecycle_control_error",
        RuntimeFailureStage.RUNTIME_OPERATION,
        "Runtime lifecycle-control operation failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_lifecycle_request_identity_error",
        RuntimeFailureStage.REQUEST_VALIDATION,
        "Runtime lifecycle request identity was invalid.",
    ),
    _failure_descriptor(
        "runtime_lifecycle_operation_conflict",
        RuntimeFailureStage.RUNTIME_OPERATION,
        "Runtime lifecycle operation was already in progress.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.NOT_STARTED,
    ),
    _failure_descriptor(
        "runtime_lifecycle_ownership_error",
        RuntimeFailureStage.RUNTIME_OPERATION,
        "Runtime lifecycle process ownership was invalid.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_graceful_shutdown_error",
        RuntimeFailureStage.GRACEFUL_SHUTDOWN,
        "Runtime graceful shutdown failed.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "runtime_forced_shutdown_error",
        RuntimeFailureStage.FORCED_TERMINATION,
        "Runtime forced shutdown failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_process_release_error",
        RuntimeFailureStage.FORCED_TERMINATION,
        "Runtime process ownership release failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_error",
        RuntimeFailureStage.ROLLBACK,
        "Runtime rollback operation failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_identity_error",
        RuntimeFailureStage.ROLLBACK,
        "Runtime rollback identity was invalid.",
    ),
    _failure_descriptor(
        "runtime_rollback_state_error",
        RuntimeFailureStage.ROLLBACK,
        "Runtime rollback state was invalid.",
    ),
    _failure_descriptor(
        "runtime_rollback_process_still_owned",
        RuntimeFailureStage.ROLLBACK,
        "Runtime rollback was blocked by process ownership.",
        RuntimeRetryability.SAFE_AFTER_CLEANUP,
        RuntimeCleanupStatus.PENDING,
    ),
    _failure_descriptor(
        "runtime_rollback_marker_error",
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        "Runtime rollback ownership marker was invalid.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_tree_limit_error",
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        "Runtime rollback workspace tree exceeded bounds.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_entry_type_error",
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        "Runtime rollback workspace entry type was unsupported.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_containment_error",
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        "Runtime rollback workspace containment failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_deletion_error",
        RuntimeFailureStage.WORKSPACE_CLEANUP,
        "Runtime rollback workspace deletion failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
    _failure_descriptor(
        "runtime_rollback_allocator_release_error",
        RuntimeFailureStage.ROLLBACK,
        "Runtime rollback allocator release failed.",
        RuntimeRetryability.POLICY_DECISION_REQUIRED,
        RuntimeCleanupStatus.FAILED,
    ),
)
_FAILURE_DESCRIPTOR_BY_CODE = MappingProxyType({
    descriptor.error_code: descriptor for descriptor in _FAILURE_DESCRIPTORS
})

_SUPPORTED_ERROR_TYPES = frozenset(
    error_type
    for hierarchy in (
        RuntimeAdapterContractError,
        RuntimeProcessOwnerError,
        RuntimeProfileRegistryError,
        RuntimeEnvironmentError,
        RuntimePathContainmentError,
        RuntimeWorkspaceError,
    )
    for error_type in hierarchy.__subclasses__() + [hierarchy]
)

_P14_6_FAILURE_CODES = frozenset({
    "runtime_lifecycle_control_error",
    "runtime_lifecycle_request_identity_error",
    "runtime_lifecycle_operation_conflict",
    "runtime_lifecycle_ownership_error",
    "runtime_graceful_shutdown_error",
    "runtime_forced_shutdown_error",
    "runtime_process_release_error",
    "runtime_rollback_error",
    "runtime_rollback_identity_error",
    "runtime_rollback_state_error",
    "runtime_rollback_process_still_owned",
    "runtime_rollback_marker_error",
    "runtime_rollback_tree_limit_error",
    "runtime_rollback_entry_type_error",
    "runtime_rollback_containment_error",
    "runtime_rollback_deletion_error",
    "runtime_rollback_allocator_release_error",
})
_P14_6_FAILURE_MODULES = frozenset({
    "hermes_cli.agent_platform.runtime_adapter.lifecycle_control",
    "hermes_cli.agent_platform.runtime_adapter.rollback",
})


def _is_p14_6_error(error: object, error_code: object) -> bool:
    return (
        isinstance(error_code, str)
        and error_code in _P14_6_FAILURE_CODES
        and error.__class__.__module__ in _P14_6_FAILURE_MODULES
    )
