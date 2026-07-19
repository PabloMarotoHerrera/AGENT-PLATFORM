from __future__ import annotations

import ast
import os
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.audit_normalization import (
    project_runtime_operation_audit,
)
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    RuntimeEventJournal,
)
from hermes_cli.agent_platform.runtime_adapter.lifecycle_control import (
    RuntimeLifecycleOperationConflictError,
    RuntimeLifecycleRequestIdentityError,
    RuntimeTerminationCoordinator,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    HermesProcessOwner,
    OwnedProcessGracefulStopResult,
    OwnedProcessSnapshot,
    OwnedProcessStillRunningError,
    ResolvedProcessLaunchPlan,
    UnknownRuntimeOwnershipError,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import get_runtime_profile
from hermes_cli.agent_platform.runtime_adapter.stream_capture import (
    BoundedStreamSnapshot,
)


UTC = timezone.utc
PROBE = Path(__file__).with_name("runtime_adapter_lifecycle_probe.py")
SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "lifecycle_control.py"
)
PROCESS_OWNER_SOURCE = SOURCE_PATH.with_name("process_owner.py")
WORKSPACE_ID = "workspace-001"


class DeterministicClock:
    def __init__(self) -> None:
        self._timestamp = datetime(2026, 1, 1, tzinfo=UTC)
        self._offset_ms = 0

    def utc_now(self) -> datetime:
        value = self._timestamp
        self._timestamp = self._timestamp + timedelta(milliseconds=10)
        return value

    def monotonic_offset_ms(self) -> int:
        value = self._offset_ms
        self._offset_ms += 10
        return value


def utc_now() -> datetime:
    return datetime.now(UTC)


def explicit_test_environment() -> tuple[tuple[str, str], ...]:
    values = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    for key in ("PATH", "SystemRoot", "WINDIR", "TEMP", "TMP"):
        if key in os.environ:
            values[key] = os.environ[key]
    return tuple(sorted(values.items()))


def runtime_handle(
    runtime_id: str = "rt.p146.lifecycle",
    *,
    state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.STARTING,
    workspace_id: str = WORKSPACE_ID,
) -> ra.RuntimeHandle:
    return ra.RuntimeHandle(
        schema_version=1,
        runtime_id=runtime_id,
        correlation_id=f"corr.p146.{runtime_id}",
        profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        workspace_id=workspace_id,
        lifecycle_state=state,
        created_at_utc=utc_now(),
    )


def timeout_policy() -> ra.RuntimeTimeoutPolicy:
    return get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID).timeout_policy


def launch_plan(tmp_path: Path, *arguments: str) -> ResolvedProcessLaunchPlan:
    return ResolvedProcessLaunchPlan(
        profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        workspace_id=WORKSPACE_ID,
        executable=sys.executable,
        arguments=(str(PROBE), *arguments),
        working_directory=str(tmp_path),
        environment_items=explicit_test_environment(),
        stdout_limit_bytes=4096,
        stderr_limit_bytes=4096,
    )


def cancel_request(handle: ra.RuntimeHandle) -> ra.RuntimeCancelRequest:
    return ra.RuntimeCancelRequest(
        schema_version=1,
        runtime_id=handle.runtime_id,
        correlation_id=handle.correlation_id,
        requested_by="tester.p146",
        reason_code="test.cancel",
    )


def stop_request(handle: ra.RuntimeHandle) -> ra.RuntimeStopRequest:
    return ra.RuntimeStopRequest(
        schema_version=1,
        runtime_id=handle.runtime_id,
        correlation_id=handle.correlation_id,
        requested_by="tester.p146",
        reason_code="test.stop",
    )


def event_journal(handle: ra.RuntimeHandle) -> RuntimeEventJournal:
    counter = iter(f"evt_p146_{index:03d}" for index in range(40))
    return RuntimeEventJournal(
        runtime_handle=handle, event_id_factory=lambda: next(counter)
    )


def cleanup_owner(owner: HermesProcessOwner, *runtime_ids: str) -> None:
    for runtime_id in runtime_ids:
        if runtime_id not in owner.owned_runtime_ids():
            continue
        try:
            snapshot = owner.snapshot(runtime_id)
            if (
                snapshot.process_reference.process_status
                is ra.RuntimeProcessStatus.RUNNING
            ):
                owner.terminate_owned_tree(runtime_id, timeout_ms=5000)
            owner.release(runtime_id)
        except Exception:
            pass


def snapshot(
    runtime_id: str,
    *,
    listener_pid: int | None = None,
    status: ra.RuntimeProcessStatus = ra.RuntimeProcessStatus.EXITED,
) -> OwnedProcessSnapshot:
    return OwnedProcessSnapshot(
        runtime_id=runtime_id,
        process_reference=ra.RuntimeProcessRef(
            launcher_pid=12345,
            listener_pid=listener_pid,
            descendant_pids=(),
            process_status=status,
            started_at_utc=utc_now(),
            exited_at_utc=utc_now()
            if status is not ra.RuntimeProcessStatus.RUNNING
            else None,
            exit_code=0 if status is not ra.RuntimeProcessStatus.RUNNING else None,
        ),
        stdout_snapshot=BoundedStreamSnapshot(
            stream=ra.RuntimeLogStream.STDOUT,
            total_bytes_read=0,
            bounded_bytes=0,
            discarded_bytes=0,
            truncated=False,
            drain_complete=True,
        ),
        stderr_snapshot=BoundedStreamSnapshot(
            stream=ra.RuntimeLogStream.STDERR,
            total_bytes_read=0,
            bounded_bytes=0,
            discarded_bytes=0,
            truncated=False,
            drain_complete=True,
        ),
        tree_captured_at_utc=utc_now(),
    )


def test_request_identity_and_public_request_authority_are_bounded() -> None:
    handle = runtime_handle(state=ra.RuntimeLifecycleState.CREATED)
    coordinator = RuntimeTerminationCoordinator(
        process_owner=HermesProcessOwner(),
        clock=DeterministicClock(),
    )

    wrong_runtime = ra.RuntimeCancelRequest(**{
        **cancel_request(handle).model_dump(),
        "runtime_id": "rt.other",
    })
    with pytest.raises(RuntimeLifecycleRequestIdentityError):
        coordinator.cancel(
            request=wrong_runtime,
            runtime_handle=handle,
            event_journal=event_journal(handle),
            timeout_policy=timeout_policy(),
        )

    wrong_correlation = ra.RuntimeStopRequest(**{
        **stop_request(handle).model_dump(),
        "correlation_id": "corr.other",
    })
    with pytest.raises(RuntimeLifecycleRequestIdentityError):
        coordinator.shutdown(
            request=wrong_correlation,
            runtime_handle=handle,
            event_journal=event_journal(handle),
            timeout_policy=timeout_policy(),
        )

    forbidden_fields = {"pid", "signal", "command", "argv", "environment", "path"}
    assert forbidden_fields.isdisjoint(ra.RuntimeCancelRequest.model_fields)
    assert forbidden_fields.isdisjoint(ra.RuntimeStopRequest.model_fields)


@pytest.mark.parametrize(
    "state",
    (ra.RuntimeLifecycleState.CREATED, ra.RuntimeLifecycleState.VALIDATING),
)
def test_pre_process_cancellation_needs_no_owner_and_emits_no_process_event(
    state: ra.RuntimeLifecycleState,
) -> None:
    handle = runtime_handle(state=state)
    journal = event_journal(handle)
    result = RuntimeTerminationCoordinator(
        process_owner=HermesProcessOwner(),
        clock=DeterministicClock(),
    ).cancel(
        request=cancel_request(handle),
        runtime_handle=handle,
        event_journal=journal,
        timeout_policy=timeout_policy(),
    )

    assert result.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.CANCELLED
    assert result.outcome is ra.RuntimeOperationOutcome.CANCELLED
    assert result.process_reference is None
    assert [event.event_type for event in result.events] == [
        ra.RuntimeEventType.CANCELLATION_REQUESTED
    ]


def test_graceful_shutdown_releases_owned_process_without_forced_fallback(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    handle = runtime_handle("rt.p146.graceful")
    try:
        owner.launch(
            handle,
            launch_plan(tmp_path, "--sleep-ms", "5000", "--graceful-exit-code", "0"),
        )
        result = RuntimeTerminationCoordinator(
            process_owner=owner,
            clock=DeterministicClock(),
        ).shutdown(
            request=stop_request(handle),
            runtime_handle=handle,
            event_journal=event_journal(handle),
            timeout_policy=timeout_policy(),
        )
    finally:
        cleanup_owner(owner, handle.runtime_id)

    assert result.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.STOPPED
    assert result.outcome is ra.RuntimeOperationOutcome.STOPPED
    assert handle.runtime_id not in owner.owned_runtime_ids()
    assert ra.RuntimeEventType.FORCED_TERMINATION_STARTED not in {
        event.event_type for event in result.events
    }
    assert [event.event_type for event in result.events] == [
        ra.RuntimeEventType.GRACEFUL_SHUTDOWN_STARTED,
        ra.RuntimeEventType.PROCESS_EXITED,
    ]
    audit = project_runtime_operation_audit(result)
    assert audit.outcome is ra.RuntimeOperationOutcome.STOPPED


def test_active_cancellation_preserves_cancelled_outcome_and_event_order(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    handle = runtime_handle("rt.p146.cancel")
    try:
        owner.launch(handle, launch_plan(tmp_path, "--sleep-ms", "5000"))
        result = RuntimeTerminationCoordinator(
            process_owner=owner,
            clock=DeterministicClock(),
        ).cancel(
            request=cancel_request(handle),
            runtime_handle=handle,
            event_journal=event_journal(handle),
            timeout_policy=timeout_policy(),
        )
    finally:
        cleanup_owner(owner, handle.runtime_id)

    assert result.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.CANCELLED
    assert result.outcome is ra.RuntimeOperationOutcome.CANCELLED
    event_types = [event.event_type for event in result.events]
    assert event_types[0] is ra.RuntimeEventType.CANCELLATION_REQUESTED
    assert event_types[1] is ra.RuntimeEventType.GRACEFUL_SHUTDOWN_STARTED
    assert event_types[-1] is ra.RuntimeEventType.PROCESS_EXITED
    assert result.log_references == ()


def test_forced_fallback_terminates_exact_owned_tree_after_graceful_timeout(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    handle = runtime_handle("rt.p146.forced")
    short_timeout = ra.RuntimeTimeoutPolicy(
        readiness_timeout_ms=1000,
        graceful_shutdown_timeout_ms=100,
        forced_termination_timeout_ms=5000,
        poll_interval_ms=50,
        max_stdout_bytes=4096,
        max_stderr_bytes=4096,
    )
    try:
        owner.launch(
            handle,
            launch_plan(
                tmp_path,
                "--sleep-ms",
                "10000",
                "--spawn-child",
                "--child-sleep-ms",
                "10000",
                "--ignore-graceful-stop",
            ),
        )
        result = RuntimeTerminationCoordinator(
            process_owner=owner,
            clock=DeterministicClock(),
        ).shutdown(
            request=stop_request(handle),
            runtime_handle=handle,
            event_journal=event_journal(handle),
            timeout_policy=short_timeout,
        )
    finally:
        cleanup_owner(owner, handle.runtime_id)

    assert result.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.STOPPED
    assert result.outcome is ra.RuntimeOperationOutcome.STOPPED
    assert ra.RuntimeEventType.FORCED_TERMINATION_STARTED in {
        event.event_type for event in result.events
    }
    assert result.process_reference is not None
    assert result.process_reference.descendant_pids == ()
    assert handle.runtime_id not in owner.owned_runtime_ids()


def test_terminal_idempotency_adds_no_events() -> None:
    coordinator = RuntimeTerminationCoordinator(
        process_owner=HermesProcessOwner(),
        clock=DeterministicClock(),
    )
    for state, outcome in (
        (ra.RuntimeLifecycleState.STOPPED, ra.RuntimeOperationOutcome.STOPPED),
        (ra.RuntimeLifecycleState.CANCELLED, ra.RuntimeOperationOutcome.CANCELLED),
        (ra.RuntimeLifecycleState.ROLLED_BACK, ra.RuntimeOperationOutcome.ROLLED_BACK),
    ):
        handle = runtime_handle(f"rt.p146.idempotent.{state.value}", state=state)
        journal = event_journal(handle)
        result = coordinator.cancel(
            request=cancel_request(handle),
            runtime_handle=handle,
            event_journal=journal,
            timeout_policy=timeout_policy(),
        )
        assert result.runtime_handle.lifecycle_state is state
        assert result.outcome is outcome
        assert result.events == ()


def test_listener_release_event_is_emitted_only_for_bound_listener(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    handle = runtime_handle("rt.p146.listener")
    try:
        launched = owner.launch(handle, launch_plan(tmp_path, "--sleep-ms", "5000"))
        assert launched.process_reference.launcher_pid is not None
        owner.bind_listener_pid(
            handle.runtime_id, launched.process_reference.launcher_pid
        )
        result = RuntimeTerminationCoordinator(
            process_owner=owner,
            clock=DeterministicClock(),
        ).shutdown(
            request=stop_request(handle),
            runtime_handle=handle,
            event_journal=event_journal(handle),
            timeout_policy=timeout_policy(),
        )
    finally:
        cleanup_owner(owner, handle.runtime_id)

    assert result.process_reference is not None
    assert (
        result.process_reference.listener_pid == launched.process_reference.launcher_pid
    )
    assert result.events[-1].event_type is ra.RuntimeEventType.LISTENER_RELEASED


def test_release_failure_returns_failed_result_with_stable_failure() -> None:
    class ReleaseFailureOwner:
        def __init__(self, runtime_id: str) -> None:
            self.runtime_id = runtime_id

        def request_graceful_stop(self, runtime_id: str, *, timeout_ms: int):
            snap = snapshot(runtime_id)
            return OwnedProcessGracefulStopResult(
                runtime_id=runtime_id,
                mechanism="already_exited",
                supported=True,
                exit_observed=True,
                timed_out=False,
                snapshot=snap,
            )

        def release(self, runtime_id: str) -> None:
            raise OwnedProcessStillRunningError(runtime_id=runtime_id)

        def owned_runtime_ids(self) -> tuple[str, ...]:
            return (self.runtime_id,)

    handle = runtime_handle("rt.p146.release.failure")
    result = RuntimeTerminationCoordinator(
        process_owner=ReleaseFailureOwner(handle.runtime_id),
        clock=DeterministicClock(),
    ).shutdown(
        request=stop_request(handle),
        runtime_handle=handle,
        event_journal=event_journal(handle),
        timeout_policy=timeout_policy(),
    )

    assert result.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.FAILED
    assert result.outcome is ra.RuntimeOperationOutcome.FAILED
    assert result.failure is not None
    assert result.failure.failure_code == "runtime_process_release_error"
    assert "still running" not in result.failure.sanitized_summary.lower()
    assert result.events[-1].event_type is ra.RuntimeEventType.RUNTIME_FAILED


def test_per_runtime_operation_lock_rejects_conflict_and_allows_other_runtime() -> None:
    entered = threading.Event()
    release = threading.Event()
    completed: list[RuntimeError | None] = []

    class BlockingOwner:
        def request_graceful_stop(self, runtime_id: str, *, timeout_ms: int):
            if runtime_id == "rt.p146.locked":
                entered.set()
                release.wait(timeout=5)
            snap = snapshot(runtime_id)
            return OwnedProcessGracefulStopResult(
                runtime_id=runtime_id,
                mechanism="already_exited",
                supported=True,
                exit_observed=True,
                timed_out=False,
                snapshot=snap,
            )

        def release(self, runtime_id: str) -> None:
            return None

        def owned_runtime_ids(self) -> tuple[str, ...]:
            return ()

    coordinator = RuntimeTerminationCoordinator(
        process_owner=BlockingOwner(),
        clock=DeterministicClock(),
    )
    locked = runtime_handle("rt.p146.locked")

    def run_locked() -> None:
        try:
            coordinator.shutdown(
                request=stop_request(locked),
                runtime_handle=locked,
                event_journal=event_journal(locked),
                timeout_policy=timeout_policy(),
            )
            completed.append(None)
        except RuntimeError as exc:
            completed.append(exc)

    thread = threading.Thread(target=run_locked)
    thread.start()
    assert entered.wait(timeout=5)
    with pytest.raises(RuntimeLifecycleOperationConflictError):
        coordinator.shutdown(
            request=stop_request(locked),
            runtime_handle=locked,
            event_journal=event_journal(locked),
            timeout_policy=timeout_policy(),
        )

    other = runtime_handle("rt.p146.other")
    other_result = coordinator.shutdown(
        request=stop_request(other),
        runtime_handle=other,
        event_journal=event_journal(other),
        timeout_policy=timeout_policy(),
    )
    assert other_result.outcome is ra.RuntimeOperationOutcome.STOPPED

    release.set()
    thread.join(timeout=5)
    assert completed == [None]


def test_lifecycle_control_source_safety_and_root_exports() -> None:
    forbidden_text = {
        "shell=True",
        "os.system",
        "os.popen",
        "PowerShell",
        "cmd.exe",
        "taskkill /IM",
        "Stop-Process",
        "Get-Process",
        "shutil.rmtree",
        "Path.home",
        "expanduser",
        "os.environ",
        "os.getenv",
        "requests",
        "httpx",
        "socket",
        "git reset",
        "git clean",
        "audit_log",
        "provider",
        "worker launch",
        "agent launch",
        "MCP execution",
    }
    for source_path in (SOURCE_PATH, PROCESS_OWNER_SOURCE):
        lowered = source_path.read_text(encoding="utf-8").lower()
        for forbidden in forbidden_text:
            assert forbidden.lower() not in lowered, (source_path, forbidden)

    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = {alias.name for alias in node.names}
            assert imported.isdisjoint({"subprocess", "socket", "requests", "httpx"})
        if isinstance(node, ast.ImportFrom):
            assert node.module not in {"subprocess", "socket", "requests", "httpx"}

    assert not hasattr(ra, "RuntimeTerminationCoordinator")
    assert "RuntimeTerminationCoordinator" not in ra.__all__
    assert not hasattr(ra, "RuntimeWorkspaceRollbackCoordinator")
