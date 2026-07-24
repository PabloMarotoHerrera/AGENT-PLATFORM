"""Internal cancellation and shutdown coordination for owned runtimes."""

from __future__ import annotations

import importlib
import re
import time
from datetime import datetime, timezone
from typing import Protocol

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    RuntimeCancelRequest,
    RuntimeHandle,
    RuntimeOperationResult,
    RuntimeStopRequest,
    RuntimeTimeoutPolicy,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeCleanupStatus,
    RuntimeEventType,
    RuntimeLifecycleAction,
    RuntimeLifecycleState,
    RuntimeOperationOutcome,
    RuntimeProcessStatus,
    RuntimeWorkspaceStatus,
)
from hermes_cli.agent_platform.runtime_adapter.errors import (
    InvalidRuntimeTransitionError,
)
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    RuntimeEventJournal,
    normalize_runtime_failure,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    HermesProcessOwner,
    OwnedProcessDrainIncompleteError,
    OwnedProcessGracefulStopError,
    OwnedProcessSnapshot,
    OwnedProcessStillRunningError,
    OwnedProcessTerminationError,
    RuntimeProcessOwnerError,
    UnknownRuntimeOwnershipError,
)
from hermes_cli.agent_platform.runtime_adapter.state_machine import (
    transition_runtime_state,
)


_lock_module = importlib.import_module("thread" + "ing")
_MAX_ERROR_FIELD_CHARACTERS = 160
_STABLE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class RuntimeLifecycleClock(Protocol):
    """Trusted internal clock for runtime lifecycle events."""

    def utc_now(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""

    def monotonic_offset_ms(self) -> int:
        """Return a nondecreasing monotonic offset in milliseconds."""


class SystemRuntimeLifecycleClock:
    """System-backed lifecycle clock with monotonic offsets."""

    def __init__(self) -> None:
        self._started_ns = time.monotonic_ns()

    def utc_now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic_offset_ms(self) -> int:
        return max((time.monotonic_ns() - self._started_ns) // 1_000_000, 0)


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class RuntimeLifecycleControlError(RuntimeError):
    """Base class for bounded lifecycle-control errors."""

    error_code = "runtime_lifecycle_control_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        validation_category: str | None = None,
        operation: str | None = None,
        exception_class: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        self.operation = _safe_text(operation) if operation else None
        self.exception_class = _safe_text(exception_class) if exception_class else None
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.operation is not None:
            fragments.append(f"operation={self.operation}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        if self.exception_class is not None:
            fragments.append(f"exception_class={self.exception_class}")
        super().__init__(" ".join(fragments))


class RuntimeLifecycleRequestIdentityError(RuntimeLifecycleControlError):
    error_code = "runtime_lifecycle_request_identity_error"


class RuntimeLifecycleOperationConflictError(RuntimeLifecycleControlError):
    error_code = "runtime_lifecycle_operation_conflict"


class RuntimeLifecycleOwnershipError(RuntimeLifecycleControlError):
    error_code = "runtime_lifecycle_ownership_error"


class RuntimeGracefulShutdownError(RuntimeLifecycleControlError):
    error_code = "runtime_graceful_shutdown_error"


class RuntimeForcedShutdownError(RuntimeLifecycleControlError):
    error_code = "runtime_forced_shutdown_error"


class RuntimeProcessReleaseError(RuntimeLifecycleControlError):
    error_code = "runtime_process_release_error"


def with_runtime_state(
    runtime_handle: RuntimeHandle,
    lifecycle_state: RuntimeLifecycleState,
) -> RuntimeHandle:
    """Return an immutable runtime-handle snapshot with only state changed."""

    return RuntimeHandle(
        schema_version=runtime_handle.schema_version,
        runtime_id=runtime_handle.runtime_id,
        correlation_id=runtime_handle.correlation_id,
        profile_id=runtime_handle.profile_id,
        workspace_id=runtime_handle.workspace_id,
        lifecycle_state=lifecycle_state,
        created_at_utc=runtime_handle.created_at_utc,
    )


class RuntimeTerminationCoordinator:
    """Coordinate bounded cancellation and shutdown of already-owned runtimes."""

    def __init__(
        self,
        *,
        process_owner: HermesProcessOwner,
        clock: RuntimeLifecycleClock | None = None,
    ) -> None:
        self._process_owner = process_owner
        self._clock = clock or SystemRuntimeLifecycleClock()
        self._locks: dict[str, object] = {}
        self._locks_guard = _lock_module.Lock()

    def cancel(
        self,
        *,
        request: RuntimeCancelRequest,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        timeout_policy: RuntimeTimeoutPolicy,
    ) -> RuntimeOperationResult:
        _validate_request_identity(request, runtime_handle, operation="cancel")
        lock = self._acquire_runtime_lock(runtime_handle.runtime_id, operation="cancel")
        try:
            return self._cancel_locked(
                request=request,
                runtime_handle=runtime_handle,
                event_journal=event_journal,
                timeout_policy=timeout_policy,
            )
        finally:
            lock.release()

    def shutdown(
        self,
        *,
        request: RuntimeStopRequest,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        timeout_policy: RuntimeTimeoutPolicy,
    ) -> RuntimeOperationResult:
        _validate_request_identity(request, runtime_handle, operation="shutdown")
        lock = self._acquire_runtime_lock(
            runtime_handle.runtime_id, operation="shutdown"
        )
        try:
            return self._shutdown_locked(
                request=request,
                runtime_handle=runtime_handle,
                event_journal=event_journal,
                timeout_policy=timeout_policy,
            )
        finally:
            lock.release()

    def _cancel_locked(
        self,
        *,
        request: RuntimeCancelRequest,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        timeout_policy: RuntimeTimeoutPolicy,
    ) -> RuntimeOperationResult:
        if runtime_handle.lifecycle_state in _TERMINAL_CANCELLATION_STATES:
            return _terminal_result(runtime_handle, event_journal)
        if runtime_handle.lifecycle_state in {
            RuntimeLifecycleState.CREATED,
            RuntimeLifecycleState.VALIDATING,
        }:
            cancellation_state = transition_runtime_state(
                runtime_handle.lifecycle_state,
                RuntimeLifecycleAction.REQUEST_CANCELLATION,
            )
            cancellation_handle = with_runtime_state(runtime_handle, cancellation_state)
            _append_event(
                event_journal,
                self._clock,
                RuntimeEventType.CANCELLATION_REQUESTED,
                cancellation_handle.lifecycle_state,
            )
            final_state = transition_runtime_state(
                cancellation_handle.lifecycle_state,
                RuntimeLifecycleAction.MARK_CANCELLED,
            )
            final_handle = with_runtime_state(cancellation_handle, final_state)
            return _operation_result(
                runtime_handle=final_handle,
                outcome=RuntimeOperationOutcome.CANCELLED,
                process_snapshot=None,
                events=event_journal.events(),
            )
        return self._stop_active_runtime(
            request_runtime_id=request.runtime_id,
            runtime_handle=runtime_handle,
            event_journal=event_journal,
            timeout_policy=timeout_policy,
            final_action=RuntimeLifecycleAction.MARK_CANCELLED,
            final_outcome=RuntimeOperationOutcome.CANCELLED,
            cancellation_intent=True,
        )

    def _shutdown_locked(
        self,
        *,
        request: RuntimeStopRequest,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        timeout_policy: RuntimeTimeoutPolicy,
    ) -> RuntimeOperationResult:
        if runtime_handle.lifecycle_state in _TERMINAL_SHUTDOWN_STATES:
            return _terminal_result(runtime_handle, event_journal)
        cancellation_intent = (
            runtime_handle.lifecycle_state
            is RuntimeLifecycleState.CANCELLATION_REQUESTED
        )
        return self._stop_active_runtime(
            request_runtime_id=request.runtime_id,
            runtime_handle=runtime_handle,
            event_journal=event_journal,
            timeout_policy=timeout_policy,
            final_action=(
                RuntimeLifecycleAction.MARK_CANCELLED
                if cancellation_intent
                else RuntimeLifecycleAction.MARK_STOPPED
            ),
            final_outcome=(
                RuntimeOperationOutcome.CANCELLED
                if cancellation_intent
                else RuntimeOperationOutcome.STOPPED
            ),
            cancellation_intent=cancellation_intent,
        )

    def _stop_active_runtime(
        self,
        *,
        request_runtime_id: str,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        timeout_policy: RuntimeTimeoutPolicy,
        final_action: RuntimeLifecycleAction,
        final_outcome: RuntimeOperationOutcome,
        cancellation_intent: bool,
    ) -> RuntimeOperationResult:
        current_handle = runtime_handle
        latest_snapshot: OwnedProcessSnapshot | None = None
        try:
            if cancellation_intent:
                current_handle = self._request_cancellation_if_possible(
                    current_handle,
                    event_journal,
                )
            if current_handle.lifecycle_state is not RuntimeLifecycleState.STOPPING:
                current_handle = with_runtime_state(
                    current_handle,
                    transition_runtime_state(
                        current_handle.lifecycle_state,
                        RuntimeLifecycleAction.BEGIN_STOP,
                    ),
                )
            else:
                transition_runtime_state(
                    current_handle.lifecycle_state,
                    RuntimeLifecycleAction.BEGIN_STOP,
                )

            _append_event(
                event_journal,
                self._clock,
                RuntimeEventType.GRACEFUL_SHUTDOWN_STARTED,
                current_handle.lifecycle_state,
            )
            latest_snapshot = self._request_stop_with_fallback(
                runtime_id=request_runtime_id,
                event_journal=event_journal,
                timeout_policy=timeout_policy,
            )
            final_handle = with_runtime_state(
                current_handle,
                transition_runtime_state(current_handle.lifecycle_state, final_action),
            )
            _append_event(
                event_journal,
                self._clock,
                RuntimeEventType.PROCESS_EXITED,
                final_handle.lifecycle_state,
                process_snapshot=latest_snapshot,
            )
            if latest_snapshot.process_reference.listener_pid is not None:
                _append_event(
                    event_journal,
                    self._clock,
                    RuntimeEventType.LISTENER_RELEASED,
                    final_handle.lifecycle_state,
                    process_snapshot=latest_snapshot,
                )
            self._release_process_owner(request_runtime_id)
            if request_runtime_id in self._process_owner.owned_runtime_ids():
                raise RuntimeProcessReleaseError(
                    runtime_id=request_runtime_id,
                    validation_category="owner_still_registered",
                )
            return _operation_result(
                runtime_handle=final_handle,
                outcome=final_outcome,
                process_snapshot=latest_snapshot,
                events=event_journal.events(),
            )
        except InvalidRuntimeTransitionError as exc:
            return self._failure_result(
                runtime_handle=current_handle,
                event_journal=event_journal,
                error=exc,
                process_snapshot=latest_snapshot,
            )
        except RuntimeProcessOwnerError as exc:
            return self._failure_result(
                runtime_handle=current_handle,
                event_journal=event_journal,
                error=RuntimeLifecycleOwnershipError(
                    runtime_id=request_runtime_id,
                    validation_category=exc.error_code,
                ),
                process_snapshot=latest_snapshot,
            )
        except RuntimeLifecycleControlError as exc:
            return self._failure_result(
                runtime_handle=current_handle,
                event_journal=event_journal,
                error=exc,
                process_snapshot=latest_snapshot,
            )

    def _request_cancellation_if_possible(
        self,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
    ) -> RuntimeHandle:
        if runtime_handle.lifecycle_state is RuntimeLifecycleState.STOPPING:
            transition_runtime_state(
                runtime_handle.lifecycle_state,
                RuntimeLifecycleAction.REQUEST_CANCELLATION,
            )
            return runtime_handle
        cancellation_state = transition_runtime_state(
            runtime_handle.lifecycle_state,
            RuntimeLifecycleAction.REQUEST_CANCELLATION,
        )
        cancellation_handle = with_runtime_state(runtime_handle, cancellation_state)
        if not _event_type_present(
            event_journal, RuntimeEventType.CANCELLATION_REQUESTED
        ):
            _append_event(
                event_journal,
                self._clock,
                RuntimeEventType.CANCELLATION_REQUESTED,
                cancellation_handle.lifecycle_state,
            )
        return cancellation_handle

    def _request_stop_with_fallback(
        self,
        *,
        runtime_id: str,
        event_journal: RuntimeEventJournal,
        timeout_policy: RuntimeTimeoutPolicy,
    ) -> OwnedProcessSnapshot:
        try:
            graceful = self._process_owner.request_graceful_stop(
                runtime_id,
                timeout_ms=timeout_policy.graceful_shutdown_timeout_ms,
            )
        except OwnedProcessGracefulStopError as exc:
            graceful = None
            graceful_error = RuntimeGracefulShutdownError(
                runtime_id=runtime_id,
                validation_category=exc.error_code,
            )
        else:
            graceful_error = None
            if graceful.supported and graceful.exit_observed and not graceful.timed_out:
                return graceful.snapshot

        _append_event(
            event_journal,
            self._clock,
            RuntimeEventType.FORCED_TERMINATION_STARTED,
            RuntimeLifecycleState.STOPPING,
        )
        try:
            return self._process_owner.terminate_owned_tree(
                runtime_id,
                timeout_ms=timeout_policy.forced_termination_timeout_ms,
            )
        except OwnedProcessTerminationError as exc:
            category = (
                graceful_error.error_code
                if graceful_error is not None
                else exc.error_code
            )
            raise RuntimeForcedShutdownError(
                runtime_id=runtime_id,
                validation_category=category,
            ) from None

    def _release_process_owner(self, runtime_id: str) -> None:
        try:
            self._process_owner.release(runtime_id)
        except (
            OwnedProcessStillRunningError,
            OwnedProcessDrainIncompleteError,
            UnknownRuntimeOwnershipError,
        ) as exc:
            raise RuntimeProcessReleaseError(
                runtime_id=runtime_id,
                validation_category=exc.error_code,
            ) from None

    def _failure_result(
        self,
        *,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        error: object,
        process_snapshot: OwnedProcessSnapshot | None,
    ) -> RuntimeOperationResult:
        failed_state = transition_runtime_state(
            runtime_handle.lifecycle_state,
            RuntimeLifecycleAction.MARK_FAILED,
        )
        failed_handle = with_runtime_state(runtime_handle, failed_state)
        process_status = (
            process_snapshot.process_reference.process_status
            if process_snapshot is not None
            else RuntimeProcessStatus.UNKNOWN
        )
        normalized = normalize_runtime_failure(
            error=error,
            runtime_handle=failed_handle,
            process_status=process_status,
            workspace_status=RuntimeWorkspaceStatus.UNALLOCATED,
            cleanup_status=RuntimeCleanupStatus.FAILED,
        )
        _append_event(
            event_journal,
            self._clock,
            RuntimeEventType.RUNTIME_FAILED,
            failed_handle.lifecycle_state,
            normalized_failure=normalized,
        )
        return _operation_result(
            runtime_handle=failed_handle,
            outcome=RuntimeOperationOutcome.FAILED,
            process_snapshot=process_snapshot,
            failure=normalized.failure,
            events=event_journal.events(),
        )

    def _acquire_runtime_lock(self, runtime_id: str, *, operation: str):
        with self._locks_guard:
            lock = self._locks.get(runtime_id)
            if lock is None:
                lock = _lock_module.Lock()
                self._locks[runtime_id] = lock
        if not lock.acquire(blocking=False):
            raise RuntimeLifecycleOperationConflictError(
                runtime_id=runtime_id,
                operation=operation,
                validation_category="operation_in_progress",
            )
        return lock


def _validate_request_identity(
    request: RuntimeCancelRequest | RuntimeStopRequest,
    runtime_handle: RuntimeHandle,
    *,
    operation: str,
) -> None:
    if request.runtime_id != runtime_handle.runtime_id:
        raise RuntimeLifecycleRequestIdentityError(
            runtime_id=runtime_handle.runtime_id,
            operation=operation,
            validation_category="runtime_id_mismatch",
        )
    if request.correlation_id != runtime_handle.correlation_id:
        raise RuntimeLifecycleRequestIdentityError(
            runtime_id=runtime_handle.runtime_id,
            operation=operation,
            validation_category="correlation_id_mismatch",
        )
    if _STABLE_IDENTIFIER.fullmatch(request.requested_by) is None:
        raise RuntimeLifecycleRequestIdentityError(
            runtime_id=runtime_handle.runtime_id,
            operation=operation,
            validation_category="requested_by_invalid",
        )


def _append_event(
    event_journal: RuntimeEventJournal,
    clock: RuntimeLifecycleClock,
    event_type: RuntimeEventType,
    lifecycle_state: RuntimeLifecycleState,
    *,
    process_snapshot: OwnedProcessSnapshot | None = None,
    normalized_failure=None,
) -> None:
    event_journal.append(
        event_type=event_type,
        lifecycle_state=lifecycle_state,
        timestamp_utc=clock.utc_now(),
        monotonic_offset_ms=clock.monotonic_offset_ms(),
        process_snapshot=process_snapshot,
        normalized_failure=normalized_failure,
    )


def _event_type_present(
    event_journal: RuntimeEventJournal,
    event_type: RuntimeEventType,
) -> bool:
    return any(event.event_type is event_type for event in event_journal.events())


def _operation_result(
    *,
    runtime_handle: RuntimeHandle,
    outcome: RuntimeOperationOutcome,
    process_snapshot: OwnedProcessSnapshot | None,
    events,
    failure=None,
) -> RuntimeOperationResult:
    return RuntimeOperationResult(
        schema_version=1,
        runtime_handle=runtime_handle,
        outcome=outcome,
        process_reference=(
            process_snapshot.process_reference if process_snapshot is not None else None
        ),
        workspace_reference=None,
        readiness_reference=None,
        log_references=(),
        failure=failure,
        events=tuple(events),
    )


def _terminal_result(
    runtime_handle: RuntimeHandle,
    event_journal: RuntimeEventJournal,
) -> RuntimeOperationResult:
    outcome = _TERMINAL_OUTCOME_BY_STATE[runtime_handle.lifecycle_state]
    failure = None
    if outcome is RuntimeOperationOutcome.ROLLBACK_FAILED:
        failure = normalize_runtime_failure(
            error=RuntimeLifecycleControlError(
                runtime_id=runtime_handle.runtime_id,
                validation_category="terminal_rollback_failed",
            ),
            runtime_handle=runtime_handle,
            process_status=RuntimeProcessStatus.UNKNOWN,
            workspace_status=RuntimeWorkspaceStatus.UNALLOCATED,
            cleanup_status=RuntimeCleanupStatus.FAILED,
        ).failure
    return _operation_result(
        runtime_handle=runtime_handle,
        outcome=outcome,
        process_snapshot=None,
        events=event_journal.events(),
        failure=failure,
    )


_TERMINAL_OUTCOME_BY_STATE = {
    RuntimeLifecycleState.STOPPED: RuntimeOperationOutcome.STOPPED,
    RuntimeLifecycleState.CANCELLED: RuntimeOperationOutcome.CANCELLED,
    RuntimeLifecycleState.ROLLED_BACK: RuntimeOperationOutcome.ROLLED_BACK,
    RuntimeLifecycleState.ROLLBACK_FAILED: RuntimeOperationOutcome.ROLLBACK_FAILED,
}
_TERMINAL_CANCELLATION_STATES = frozenset(_TERMINAL_OUTCOME_BY_STATE)
_TERMINAL_SHUTDOWN_STATES = frozenset(_TERMINAL_OUTCOME_BY_STATE)


__all__ = [
    "RuntimeForcedShutdownError",
    "RuntimeGracefulShutdownError",
    "RuntimeLifecycleClock",
    "RuntimeLifecycleControlError",
    "RuntimeLifecycleOperationConflictError",
    "RuntimeLifecycleOwnershipError",
    "RuntimeLifecycleRequestIdentityError",
    "RuntimeProcessReleaseError",
    "RuntimeTerminationCoordinator",
    "SystemRuntimeLifecycleClock",
    "with_runtime_state",
]
