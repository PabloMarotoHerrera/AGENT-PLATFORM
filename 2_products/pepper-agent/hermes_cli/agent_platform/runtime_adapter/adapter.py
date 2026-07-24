"""Internal P14.8 dashboard runtime adapter composition."""

from __future__ import annotations

import secrets
import sys
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID,
    RuntimeCancelRequest,
    RuntimeEvidenceRef,
    RuntimeHandle,
    RuntimeLaunchRequest,
    RuntimeLogRef,
    RuntimeOperationResult,
    RuntimeRollbackRequest,
    RuntimeStopRequest,
)
from hermes_cli.agent_platform.runtime_adapter.environment import (
    RuntimePlatformFamily,
    SanitizedRuntimeEnvironment,
    sanitize_runtime_environment,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeCleanupStatus,
    RuntimeEventType,
    RuntimeLifecycleAction,
    RuntimeLifecycleState,
    RuntimeLogStream,
    RuntimeOperationOutcome,
    RuntimeProcessStatus,
    RuntimeWorkspaceStatus,
)
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    NormalizedRuntimeFailure,
    RuntimeEventJournal,
    normalize_runtime_failure,
)
from hermes_cli.agent_platform.runtime_adapter.lifecycle_control import (
    RuntimeLifecycleClock,
    RuntimeTerminationCoordinator,
    SystemRuntimeLifecycleClock,
    with_runtime_state,
)
from hermes_cli.agent_platform.runtime_adapter.listener_discovery import (
    RuntimeListenerDiscovery,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    HermesProcessOwner,
    OwnedProcessDrainIncompleteError,
    OwnedProcessSnapshot,
    OwnedProcessStillRunningError,
    OwnedProcessTerminationError,
    ResolvedProcessLaunchPlan,
    RuntimeProcessOwnerError,
    UnknownRuntimeOwnershipError,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    RuntimeArgumentSelector,
    RuntimeExecutionScope,
    RuntimeProfileDefinition,
    RuntimeExecutableSelector,
    get_runtime_profile,
)
from hermes_cli.agent_platform.runtime_adapter.readiness import (
    RuntimeDashboardReadinessProbe,
    RuntimeDashboardReadyFileWaiter,
    RuntimeReadinessProbeResult,
    RuntimeReadinessTimeoutError,
)
from hermes_cli.agent_platform.runtime_adapter.rollback import (
    RuntimeWorkspaceRollbackCoordinator,
)
from hermes_cli.agent_platform.runtime_adapter.state_machine import (
    transition_runtime_state,
)
from hermes_cli.agent_platform.runtime_adapter.workspace import (
    RuntimeWorkspaceAllocation,
    RuntimeWorkspaceAllocator,
)


_MAX_ERROR_FIELD_CHARACTERS = 160
_DASHBOARD_HOST = "127.0.0.1"
_DASHBOARD_ARGUMENT_PREFIX = (
    "-m",
    "hermes_cli.main",
    "dashboard",
    "--host",
    _DASHBOARD_HOST,
    "--port",
)
_DASHBOARD_ARGUMENT_SUFFIX = (
    "--no-open",
    "--skip-build",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class GovernedRuntimeAdapterError(RuntimeError):
    """Base class for bounded P14.8 adapter-composition errors."""

    error_code = "runtime_adapter_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        profile_id: str | None = None,
        operation: str | None = None,
        validation_category: str | None = None,
        exception_class: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.profile_id = _safe_text(profile_id) if profile_id is not None else None
        self.operation = _safe_text(operation) if operation else None
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        self.exception_class = _safe_text(exception_class) if exception_class else None
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.profile_id is not None:
            fragments.append(f"profile_id={self.profile_id}")
        if self.operation is not None:
            fragments.append(f"operation={self.operation}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        if self.exception_class is not None:
            fragments.append(f"exception_class={self.exception_class}")
        super().__init__(" ".join(fragments))


class RuntimeAdapterProfileError(GovernedRuntimeAdapterError):
    error_code = "runtime_adapter_profile_error"


class RuntimeAdapterLaunchError(GovernedRuntimeAdapterError):
    error_code = "runtime_adapter_launch_error"


class RuntimeAdapterCleanupError(GovernedRuntimeAdapterError):
    error_code = "runtime_adapter_cleanup_error"


class RuntimeAdapterOperationConflictError(GovernedRuntimeAdapterError):
    error_code = "runtime_adapter_operation_conflict"


@dataclass(slots=True)
class _RuntimeRecord:
    runtime_id: str
    profile: RuntimeProfileDefinition
    allocator: RuntimeWorkspaceAllocator
    allocation: RuntimeWorkspaceAllocation
    handle: RuntimeHandle
    journal: RuntimeEventJournal
    session_token: str
    ready_file: Path
    readiness_ref: object | None = None
    readiness_result: RuntimeReadinessProbeResult | None = None
    latest_snapshot: OwnedProcessSnapshot | None = None
    sanitized_environment: SanitizedRuntimeEnvironment | None = None


class GovernedRuntimeAdapter:
    """Compose the single authorized P14.8 dashboard runtime lifecycle."""

    def __init__(
        self,
        *,
        runtime_base_root: Path,
        source_environment: Mapping[str, str],
        python_executable: str | None = None,
        process_owner: HermesProcessOwner | None = None,
        listener_discovery: RuntimeListenerDiscovery | None = None,
        ready_file_waiter: RuntimeDashboardReadyFileWaiter | None = None,
        readiness_probe: RuntimeDashboardReadinessProbe | None = None,
        dashboard_port: int = 0,
        runtime_id_factory: Callable[[], str] | None = None,
        workspace_id_factory: Callable[[], str] | None = None,
        session_token_factory: Callable[[], str] | None = None,
        clock: RuntimeLifecycleClock | None = None,
    ) -> None:
        self._runtime_base_root = Path(runtime_base_root)
        self._source_environment = MappingProxyType(dict(source_environment))
        self._python_executable = str(
            Path(python_executable or sys.executable).resolve(strict=False)
        )
        self._process_owner = process_owner or HermesProcessOwner()
        self._listener_discovery = listener_discovery or RuntimeListenerDiscovery()
        self._ready_file_waiter = ready_file_waiter or RuntimeDashboardReadyFileWaiter()
        self._readiness_probe = readiness_probe or RuntimeDashboardReadinessProbe()
        self._dashboard_port = _validate_dashboard_port(dashboard_port)
        self._runtime_id_factory = runtime_id_factory or _default_runtime_id
        self._workspace_id_factory = workspace_id_factory
        self._session_token_factory = session_token_factory or _default_session_token
        self._clock = clock or SystemRuntimeLifecycleClock()
        self._records: dict[str, _RuntimeRecord] = {}
        self._launch_lock = __import__("thread" + "ing").Lock()

    def launch(self, request: RuntimeLaunchRequest) -> RuntimeOperationResult:
        """Launch the tracked dashboard profile and wait for governed readiness."""

        if not self._launch_lock.acquire(blocking=False):
            raise RuntimeAdapterOperationConflictError(
                operation="launch",
                validation_category="operation_in_progress",
            )
        runtime_id = _generate_runtime_id(self._runtime_id_factory)
        handle = _runtime_handle(
            runtime_id=runtime_id,
            correlation_id=request.correlation_id,
            profile_id=request.runtime_profile_id,
            workspace_id="workspace.unallocated",
            state=RuntimeLifecycleState.CREATED,
        )
        journal = _event_journal(handle)
        _append_event(
            journal,
            self._clock,
            RuntimeEventType.REQUEST_RECEIVED,
            handle.lifecycle_state,
        )
        record: _RuntimeRecord | None = None
        try:
            profile = _resolve_dashboard_profile(request)
            validating = with_runtime_state(
                handle,
                transition_runtime_state(
                    handle.lifecycle_state,
                    RuntimeLifecycleAction.VALIDATE,
                ),
            )
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.PROFILE_RESOLVED,
                validating.lifecycle_state,
            )
            allocator = RuntimeWorkspaceAllocator(
                trusted_base_root=self._runtime_base_root,
                workspace_id_factory=self._workspace_id_factory,
            )
            allocation = allocator.allocate(
                runtime_id=runtime_id,
                profile=profile,
                workspace_binding=request.workspace_binding,
            )
            validating = _replace_workspace(
                validating, allocation.workspace_ref.workspace_id
            )
            journal = _event_journal_from_existing(validating, journal)
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.WORKSPACE_CREATED,
                validating.lifecycle_state,
                workspace_allocation=allocation,
            )
            sanitized = sanitize_runtime_environment(
                profile=profile,
                platform_family=_platform_family(),
                source_environment=self._source_environment,
                paths=allocation.environment_paths,
                explicit_path_entries=_python_path_entries(self._python_executable),
            )
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.ENVIRONMENT_SANITIZED,
                validating.lifecycle_state,
            )
            starting = with_runtime_state(
                validating,
                transition_runtime_state(
                    validating.lifecycle_state,
                    RuntimeLifecycleAction.START,
                ),
            )
            ready_file = allocation.paths.evidence / "dashboard-ready.json"
            session_token = self._session_token_factory()
            record = _RuntimeRecord(
                runtime_id=runtime_id,
                profile=profile,
                allocator=allocator,
                allocation=allocation,
                handle=starting,
                journal=journal,
                session_token=session_token,
                ready_file=ready_file,
                sanitized_environment=sanitized,
            )
            if self._dashboard_port:
                self._listener_discovery.assert_port_free(
                    host=_DASHBOARD_HOST,
                    port=self._dashboard_port,
                )
            snapshot = self._process_owner.launch(
                starting,
                _dashboard_launch_plan(
                    profile=profile,
                    allocation=allocation,
                    sanitized=sanitized,
                    python_executable=self._python_executable,
                    dashboard_port=self._dashboard_port,
                    ready_file=ready_file,
                    session_token=session_token,
                    timeout_policy=request.timeout_policy,
                ),
            )
            record.latest_snapshot = snapshot
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.PROCESS_STARTED,
                starting.lifecycle_state,
                process_snapshot=snapshot,
            )
            waiting = with_runtime_state(
                starting,
                transition_runtime_state(
                    starting.lifecycle_state,
                    RuntimeLifecycleAction.WAIT_FOR_READINESS,
                ),
            )
            record.handle = waiting
            ready_file_result = self._ready_file_waiter.wait_for_port(
                runtime_id=runtime_id,
                ready_file=ready_file,
                timeout_ms=request.timeout_policy.readiness_timeout_ms,
                poll_interval_ms=request.timeout_policy.poll_interval_ms,
                process_exited=lambda: _process_exited(self._process_owner, runtime_id),
            )
            if self._dashboard_port and ready_file_result.port != self._dashboard_port:
                raise RuntimeAdapterLaunchError(
                    runtime_id=runtime_id,
                    operation="readiness",
                    validation_category="dashboard_port_mismatch",
                )
            listener = self._listener_discovery.discover_owned_listener(
                process_owner=self._process_owner,
                runtime_id=runtime_id,
                host=_DASHBOARD_HOST,
                port=ready_file_result.port,
                timeout_ms=request.timeout_policy.readiness_timeout_ms,
                poll_interval_ms=request.timeout_policy.poll_interval_ms,
            )
            snapshot = self._process_owner.bind_listener_pid(
                runtime_id, listener.listener_pid
            )
            record.latest_snapshot = snapshot
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.LISTENER_DISCOVERED,
                waiting.lifecycle_state,
                process_snapshot=snapshot,
            )
            waiting_ref = self._readiness_probe.waiting_reference(
                runtime_id=runtime_id,
                port=listener.port,
                timeout_ms=request.timeout_policy.readiness_timeout_ms,
            )
            record.readiness_ref = waiting_ref
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.READINESS_PROBE_STARTED,
                waiting.lifecycle_state,
                readiness_reference=waiting_ref,
            )
            readiness = self._readiness_probe.wait_for_dashboard(
                runtime_id=runtime_id,
                host=_DASHBOARD_HOST,
                port=listener.port,
                session_token=session_token,
                files_root=_require_files_root(allocation),
                timeout_ms=request.timeout_policy.readiness_timeout_ms,
                poll_interval_ms=request.timeout_policy.poll_interval_ms,
            )
            ready = with_runtime_state(
                waiting,
                transition_runtime_state(
                    waiting.lifecycle_state,
                    RuntimeLifecycleAction.MARK_READY,
                ),
            )
            record.handle = ready
            record.readiness_ref = readiness.readiness_ref
            record.readiness_result = readiness
            _append_event(
                journal,
                self._clock,
                RuntimeEventType.RUNTIME_READY,
                ready.lifecycle_state,
                readiness_reference=readiness.readiness_ref,
            )
            self._records[runtime_id] = record
            return _operation_result(
                runtime_handle=ready,
                outcome=RuntimeOperationOutcome.READY,
                process_snapshot=snapshot,
                allocation=allocation,
                readiness_ref=readiness.readiness_ref,
                events=journal.events(),
            )
        except Exception as exc:
            if record is not None:
                self._records[runtime_id] = record
            return self._launch_failure_result(
                error=_coerce_launch_error(exc, runtime_id, request.runtime_profile_id),
                runtime_handle=record.handle if record is not None else handle,
                event_journal=record.journal if record is not None else journal,
                allocation=record.allocation if record is not None else None,
                process_snapshot=record.latest_snapshot if record is not None else None,
                readiness_ref=(record.readiness_ref if record is not None else None),
            )
        finally:
            self._launch_lock.release()

    def shutdown(self, request: RuntimeStopRequest) -> RuntimeOperationResult:
        record = self._record_for(request.runtime_id, request.correlation_id)
        result = RuntimeTerminationCoordinator(
            process_owner=self._process_owner,
            clock=self._clock,
        ).shutdown(
            request=request,
            runtime_handle=record.handle,
            event_journal=record.journal,
            timeout_policy=record.profile.timeout_policy,
        )
        record.handle = result.runtime_handle
        if result.process_reference is not None:
            record.latest_snapshot = self._safe_snapshot(record.runtime_id)
        return _copy_result_with_context(result, record)

    def cancel(self, request: RuntimeCancelRequest) -> RuntimeOperationResult:
        record = self._record_for(request.runtime_id, request.correlation_id)
        result = RuntimeTerminationCoordinator(
            process_owner=self._process_owner,
            clock=self._clock,
        ).cancel(
            request=request,
            runtime_handle=record.handle,
            event_journal=record.journal,
            timeout_policy=record.profile.timeout_policy,
        )
        record.handle = result.runtime_handle
        if result.process_reference is not None:
            record.latest_snapshot = self._safe_snapshot(record.runtime_id)
        return _copy_result_with_context(result, record)

    def rollback(self, request: RuntimeRollbackRequest) -> RuntimeOperationResult:
        record = self._record_for(request.runtime_id, request.correlation_id)
        result = RuntimeWorkspaceRollbackCoordinator(
            workspace_allocator=record.allocator,
            process_owner=self._process_owner,
            clock=self._clock,
        ).rollback(
            request=request,
            runtime_handle=record.handle,
            profile=record.profile,
            allocation=record.allocation,
            event_journal=record.journal,
        )
        record.handle = result.runtime_handle
        if result.outcome is RuntimeOperationOutcome.ROLLED_BACK:
            self._records.pop(record.runtime_id, None)
        return result

    def active_runtime_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._records))

    def readiness_summary(
        self, runtime_id: str, correlation_id: str
    ) -> dict[str, object]:
        record = self._record_for(runtime_id, correlation_id)
        if record.readiness_result is None:
            raise RuntimeAdapterLaunchError(
                runtime_id=runtime_id,
                operation="readiness",
                validation_category="readiness_result_missing",
            )
        return record.readiness_result.as_summary()

    def _record_for(self, runtime_id: str, correlation_id: str) -> _RuntimeRecord:
        record = self._records.get(runtime_id)
        if record is None:
            raise RuntimeAdapterProfileError(
                runtime_id=runtime_id,
                operation="lookup",
                validation_category="unknown_runtime",
            )
        if record.handle.correlation_id != correlation_id:
            raise RuntimeAdapterProfileError(
                runtime_id=runtime_id,
                operation="lookup",
                validation_category="correlation_id_mismatch",
            )
        return record

    def _safe_snapshot(self, runtime_id: str) -> OwnedProcessSnapshot | None:
        try:
            return self._process_owner.snapshot(runtime_id)
        except RuntimeProcessOwnerError:
            return None

    def _launch_failure_result(
        self,
        *,
        error: object,
        runtime_handle: RuntimeHandle,
        event_journal: RuntimeEventJournal,
        allocation: RuntimeWorkspaceAllocation | None,
        process_snapshot: OwnedProcessSnapshot | None,
        readiness_ref: object | None,
    ) -> RuntimeOperationResult:
        process_snapshot = self._cleanup_after_failed_launch(
            runtime_handle.runtime_id, process_snapshot
        )
        failed_handle = with_runtime_state(
            runtime_handle,
            transition_runtime_state(
                runtime_handle.lifecycle_state,
                RuntimeLifecycleAction.MARK_FAILED,
            ),
        )
        process_status = (
            process_snapshot.process_reference.process_status
            if process_snapshot is not None
            else RuntimeProcessStatus.UNKNOWN
        )
        workspace_status = (
            RuntimeWorkspaceStatus.ALLOCATED
            if allocation is not None and allocation.paths.workspace_root.exists()
            else RuntimeWorkspaceStatus.UNALLOCATED
        )
        normalized = normalize_runtime_failure(
            error=error,
            runtime_handle=failed_handle,
            process_status=process_status,
            workspace_status=workspace_status,
            cleanup_status=(
                RuntimeCleanupStatus.PENDING
                if workspace_status is RuntimeWorkspaceStatus.ALLOCATED
                else RuntimeCleanupStatus.NOT_STARTED
            ),
        )
        event_type = RuntimeEventType.RUNTIME_FAILED
        if isinstance(error, RuntimeReadinessTimeoutError):
            event_type = RuntimeEventType.READINESS_TIMEOUT
            readiness_ref = error.readiness_ref
        _append_event(
            event_journal,
            self._clock,
            event_type,
            failed_handle.lifecycle_state,
            readiness_reference=(
                readiness_ref
                if event_type is RuntimeEventType.READINESS_TIMEOUT
                else None
            ),
            normalized_failure=normalized,
        )
        if failed_handle.runtime_id in self._records:
            self._records[failed_handle.runtime_id].handle = failed_handle
            self._records[failed_handle.runtime_id].latest_snapshot = process_snapshot
        return _operation_result(
            runtime_handle=failed_handle,
            outcome=RuntimeOperationOutcome.FAILED,
            process_snapshot=process_snapshot,
            allocation=allocation,
            readiness_ref=readiness_ref,
            failure=normalized,
            events=event_journal.events(),
        )

    def _cleanup_after_failed_launch(
        self,
        runtime_id: str,
        fallback_snapshot: OwnedProcessSnapshot | None,
    ) -> OwnedProcessSnapshot | None:
        if runtime_id not in self._process_owner.owned_runtime_ids():
            return fallback_snapshot
        snapshot = fallback_snapshot
        try:
            snapshot = self._process_owner.terminate_owned_tree(
                runtime_id,
                timeout_ms=5000,
            )
        except OwnedProcessTerminationError:
            snapshot = self._safe_snapshot(runtime_id) or snapshot
        try:
            self._process_owner.release(runtime_id)
        except (
            OwnedProcessStillRunningError,
            OwnedProcessDrainIncompleteError,
            UnknownRuntimeOwnershipError,
        ):
            return snapshot
        return snapshot


def _resolve_dashboard_profile(
    request: RuntimeLaunchRequest,
) -> RuntimeProfileDefinition:
    if request.runtime_profile_id != PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID:
        raise RuntimeAdapterProfileError(
            profile_id=request.runtime_profile_id,
            operation="launch",
            validation_category="dashboard_profile_required",
        )
    profile = get_runtime_profile(request.runtime_profile_id)
    if profile.execution_scope is not RuntimeExecutionScope.P14_8_ONLY:
        raise RuntimeAdapterProfileError(
            profile_id=profile.profile_ref.profile_id,
            operation="launch",
            validation_category="execution_scope_not_p14_8",
        )
    if (
        profile.executable_selector
        is not RuntimeExecutableSelector.CURRENT_PRODUCT_PYTHON
    ):
        raise RuntimeAdapterProfileError(
            profile_id=profile.profile_ref.profile_id,
            operation="launch",
            validation_category="executable_selector_unsupported",
        )
    if (
        profile.argument_selector
        is not RuntimeArgumentSelector.PEPPER_DASHBOARD_PROVIDER_NULL
    ):
        raise RuntimeAdapterProfileError(
            profile_id=profile.profile_ref.profile_id,
            operation="launch",
            validation_category="argument_selector_unsupported",
        )
    if request.workspace_binding != profile.default_workspace_binding:
        raise RuntimeAdapterProfileError(
            profile_id=profile.profile_ref.profile_id,
            operation="launch",
            validation_category="workspace_binding_mismatch",
        )
    if request.timeout_policy != profile.timeout_policy:
        raise RuntimeAdapterProfileError(
            profile_id=profile.profile_ref.profile_id,
            operation="launch",
            validation_category="timeout_policy_mismatch",
        )
    return profile


def _dashboard_launch_plan(
    *,
    profile: RuntimeProfileDefinition,
    allocation: RuntimeWorkspaceAllocation,
    sanitized: SanitizedRuntimeEnvironment,
    python_executable: str,
    dashboard_port: int,
    ready_file: Path,
    session_token: str,
    timeout_policy,
) -> ResolvedProcessLaunchPlan:
    files_root = _require_files_root(allocation)
    environment_items = _with_dashboard_environment(
        sanitized.items,
        {
            "HERMES_DASHBOARD_FILES_ROOT": str(files_root),
            "HERMES_DASHBOARD_SESSION_TOKEN": session_token,
            "HERMES_DESKTOP_READY_FILE": str(ready_file),
        },
    )
    return ResolvedProcessLaunchPlan(
        profile_id=profile.profile_ref.profile_id,
        workspace_id=allocation.workspace_ref.workspace_id,
        executable=python_executable,
        arguments=_dashboard_arguments(dashboard_port),
        working_directory=str(allocation.paths.workdir),
        environment_items=environment_items,
        stdout_limit_bytes=timeout_policy.max_stdout_bytes,
        stderr_limit_bytes=timeout_policy.max_stderr_bytes,
    )


def _dashboard_arguments(port: int) -> tuple[str, ...]:
    return (
        _DASHBOARD_ARGUMENT_PREFIX
        + (str(_validate_dashboard_port(port)),)
        + _DASHBOARD_ARGUMENT_SUFFIX
    )


def _validate_dashboard_port(port: int) -> int:
    if not isinstance(port, int) or not 0 <= port <= 65_535:
        raise RuntimeAdapterLaunchError(
            operation="launch",
            validation_category="dashboard_port_bounds",
        )
    return port


def _with_dashboard_environment(
    sanitized_items: tuple[tuple[str, str], ...], internal_items: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    merged = dict(sanitized_items)
    for key, value in internal_items.items():
        if not isinstance(value, str) or not value:
            raise RuntimeAdapterLaunchError(
                operation="environment",
                validation_category=f"{key.lower()}_invalid",
            )
        merged[key] = value
    return tuple(sorted(merged.items(), key=lambda item: item[0].casefold()))


def _require_files_root(allocation: RuntimeWorkspaceAllocation) -> Path:
    if allocation.files_root_binding is None:
        raise RuntimeAdapterLaunchError(
            runtime_id=allocation.runtime_id,
            operation="launch",
            validation_category="files_root_binding_missing",
        )
    return allocation.files_root_binding.locked_root


def _runtime_handle(
    *,
    runtime_id: str,
    correlation_id: str,
    profile_id: str,
    workspace_id: str,
    state: RuntimeLifecycleState,
) -> RuntimeHandle:
    return RuntimeHandle(
        schema_version=1,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        profile_id=profile_id,
        workspace_id=workspace_id,
        lifecycle_state=state,
        created_at_utc=_utc_now(),
    )


def _replace_workspace(handle: RuntimeHandle, workspace_id: str) -> RuntimeHandle:
    return RuntimeHandle(
        schema_version=handle.schema_version,
        runtime_id=handle.runtime_id,
        correlation_id=handle.correlation_id,
        profile_id=handle.profile_id,
        workspace_id=workspace_id,
        lifecycle_state=handle.lifecycle_state,
        created_at_utc=handle.created_at_utc,
    )


def _event_journal(handle: RuntimeHandle) -> RuntimeEventJournal:
    counter = iter(
        f"evt_{_stable_token(handle.runtime_id)}_{index:03d}" for index in range(256)
    )
    return RuntimeEventJournal(
        runtime_handle=handle, event_id_factory=lambda: next(counter)
    )


def _event_journal_from_existing(
    handle: RuntimeHandle, previous: RuntimeEventJournal
) -> RuntimeEventJournal:
    first_index = previous.event_count()
    counter = iter(
        f"evt_{_stable_token(handle.runtime_id)}_{index:03d}"
        for index in range(first_index, 256)
    )
    journal = RuntimeEventJournal(
        runtime_handle=handle,
        event_id_factory=lambda: next(counter),
    )
    for event in previous.events():
        journal._events.append(event)
        journal._event_ids.add(event.event_id)
        journal._last_timestamp_utc = event.timestamp_utc
        journal._last_monotonic_offset_ms = event.monotonic_offset_ms
    return journal


def _append_event(
    journal: RuntimeEventJournal,
    clock: RuntimeLifecycleClock,
    event_type: RuntimeEventType,
    lifecycle_state: RuntimeLifecycleState,
    *,
    process_snapshot: OwnedProcessSnapshot | None = None,
    workspace_allocation: RuntimeWorkspaceAllocation | None = None,
    readiness_reference: object | None = None,
    normalized_failure: NormalizedRuntimeFailure | None = None,
) -> None:
    journal.append(
        event_type=event_type,
        lifecycle_state=lifecycle_state,
        timestamp_utc=clock.utc_now(),
        monotonic_offset_ms=clock.monotonic_offset_ms(),
        process_snapshot=process_snapshot,
        workspace_allocation=workspace_allocation,
        readiness_reference=readiness_reference,
        normalized_failure=normalized_failure,
    )


def _operation_result(
    *,
    runtime_handle: RuntimeHandle,
    outcome: RuntimeOperationOutcome,
    process_snapshot: OwnedProcessSnapshot | None,
    allocation: RuntimeWorkspaceAllocation | None,
    readiness_ref: object | None,
    events,
    failure: NormalizedRuntimeFailure | None = None,
) -> RuntimeOperationResult:
    return RuntimeOperationResult(
        schema_version=1,
        runtime_handle=runtime_handle,
        outcome=outcome,
        process_reference=(
            process_snapshot.process_reference if process_snapshot is not None else None
        ),
        workspace_reference=allocation.workspace_ref
        if allocation is not None
        else None,
        readiness_reference=readiness_ref,
        log_references=_log_refs(process_snapshot),
        failure=failure.failure if failure is not None else None,
        events=tuple(events),
    )


def _copy_result_with_context(
    result: RuntimeOperationResult, record: _RuntimeRecord
) -> RuntimeOperationResult:
    return RuntimeOperationResult(
        schema_version=result.schema_version,
        runtime_handle=result.runtime_handle,
        outcome=result.outcome,
        process_reference=result.process_reference,
        workspace_reference=record.allocation.workspace_ref,
        readiness_reference=record.readiness_ref,
        log_references=result.log_references,
        failure=result.failure,
        events=result.events,
    )


def _log_refs(snapshot: OwnedProcessSnapshot | None) -> tuple[RuntimeLogRef, ...]:
    if snapshot is None:
        return ()
    runtime_token = _stable_token(snapshot.runtime_id)
    return (
        RuntimeLogRef(
            stream=RuntimeLogStream.STDOUT,
            evidence_ref=RuntimeEvidenceRef(
                evidence_id=f"log.{runtime_token}.stdout",
                evidence_kind="runtime_log",
            ),
            captured_bytes=snapshot.stdout_snapshot.bounded_bytes,
            truncated=snapshot.stdout_snapshot.truncated,
        ),
        RuntimeLogRef(
            stream=RuntimeLogStream.STDERR,
            evidence_ref=RuntimeEvidenceRef(
                evidence_id=f"log.{runtime_token}.stderr",
                evidence_kind="runtime_log",
            ),
            captured_bytes=snapshot.stderr_snapshot.bounded_bytes,
            truncated=snapshot.stderr_snapshot.truncated,
        ),
    )


def _coerce_launch_error(
    error: BaseException, runtime_id: str, profile_id: str
) -> BaseException:
    if hasattr(error, "error_code"):
        return error
    return RuntimeAdapterLaunchError(
        runtime_id=runtime_id,
        profile_id=profile_id,
        operation="launch",
        exception_class=error.__class__.__name__,
    )


def _cleanup_error(error: BaseException, runtime_id: str) -> RuntimeAdapterCleanupError:
    return RuntimeAdapterCleanupError(
        runtime_id=runtime_id,
        operation="cleanup",
        exception_class=error.__class__.__name__,
    )


def _process_exited(process_owner: HermesProcessOwner, runtime_id: str) -> bool:
    try:
        snapshot = process_owner.snapshot(runtime_id)
    except RuntimeProcessOwnerError:
        return True
    return snapshot.process_reference.process_status is not RuntimeProcessStatus.RUNNING


def _platform_family() -> RuntimePlatformFamily:
    if sys.platform == "win32":
        return RuntimePlatformFamily.WINDOWS
    return RuntimePlatformFamily.POSIX


def _python_path_entries(python_executable: str) -> tuple[str, ...]:
    executable = Path(python_executable).resolve(strict=False)
    parent = executable.parent
    if not parent.is_absolute():
        return ()
    return (str(parent),)


def _generate_runtime_id(factory: Callable[[], str]) -> str:
    try:
        runtime_id = factory()
    except Exception as exc:
        raise RuntimeAdapterLaunchError(
            operation="runtime_id_generation",
            exception_class=exc.__class__.__name__,
        ) from None
    _runtime_handle(
        runtime_id=runtime_id,
        correlation_id="corr.validation",
        profile_id=PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID,
        workspace_id="workspace.validation",
        state=RuntimeLifecycleState.CREATED,
    )
    return runtime_id


def _default_runtime_id() -> str:
    return "rt.p148." + uuid.uuid4().hex


def _default_session_token() -> str:
    return secrets.token_urlsafe(32)


def _stable_token(value: str) -> str:
    token = "".join(character if character.isalnum() else "." for character in value)
    return token[:80]


__all__ = [
    "GovernedRuntimeAdapter",
    "GovernedRuntimeAdapterError",
    "RuntimeAdapterCleanupError",
    "RuntimeAdapterLaunchError",
    "RuntimeAdapterOperationConflictError",
    "RuntimeAdapterProfileError",
]
