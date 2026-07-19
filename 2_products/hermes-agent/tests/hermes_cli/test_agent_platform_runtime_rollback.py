from __future__ import annotations

import ast
import json
import os
import sys
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
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    HermesProcessOwner,
    ResolvedProcessLaunchPlan,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import get_runtime_profile
from hermes_cli.agent_platform.runtime_adapter.rollback import (
    RuntimeRollbackDeletionError,
    RuntimeRollbackEntryTypeError,
    RuntimeRollbackIdentityError,
    RuntimeRollbackMarkerError,
    RuntimeRollbackProcessStillOwnedError,
    RuntimeRollbackStateError,
    RuntimeWorkspaceRollbackCoordinator,
)
from hermes_cli.agent_platform.runtime_adapter.workspace import (
    RuntimeWorkspaceAllocator,
    UnknownRuntimeWorkspaceError,
)


UTC = timezone.utc
PROBE = Path(__file__).with_name("runtime_adapter_lifecycle_probe.py")
SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "rollback.py"
)
WORKSPACE_SOURCE = SOURCE_PATH.with_name("workspace.py")


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


def id_factory(token: str):
    return lambda: "ws_" + token


def runtime_handle(
    runtime_id: str,
    workspace_id: str,
    *,
    state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.STOPPED,
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


def rollback_request(handle: ra.RuntimeHandle) -> ra.RuntimeRollbackRequest:
    return ra.RuntimeRollbackRequest(
        schema_version=1,
        runtime_id=handle.runtime_id,
        correlation_id=handle.correlation_id,
        requested_by="tester.p146",
        reason_code="test.rollback",
    )


def event_journal(handle: ra.RuntimeHandle) -> RuntimeEventJournal:
    counter = iter(f"evt_p146_rb_{index:03d}" for index in range(40))
    return RuntimeEventJournal(
        runtime_handle=handle, event_id_factory=lambda: next(counter)
    )


def make_allocation(tmp_path: Path, runtime_id: str, token: str = "a" * 32):
    base = tmp_path / "base"
    base.mkdir(exist_ok=True)
    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory(token),
    )
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    allocation = allocator.allocate(runtime_id=runtime_id, profile=profile)
    return allocator, profile, allocation


def coordinator(
    allocator: RuntimeWorkspaceAllocator,
    owner: HermesProcessOwner | None = None,
) -> RuntimeWorkspaceRollbackCoordinator:
    return RuntimeWorkspaceRollbackCoordinator(
        workspace_allocator=allocator,
        process_owner=owner or HermesProcessOwner(),
        clock=DeterministicClock(),
    )


def explicit_test_environment() -> tuple[tuple[str, str], ...]:
    values = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    for key in ("PATH", "SystemRoot", "WINDIR", "TEMP", "TMP"):
        if key in os.environ:
            values[key] = os.environ[key]
    return tuple(sorted(values.items()))


def cleanup_owner(owner: HermesProcessOwner, *runtime_ids: str) -> None:
    for runtime_id in runtime_ids:
        if runtime_id not in owner.owned_runtime_ids():
            continue
        try:
            owner.terminate_owned_tree(runtime_id, timeout_ms=5000)
            owner.release(runtime_id)
        except Exception:
            pass


def test_rollback_preconditions_reject_identity_state_process_and_unknown_allocation(
    tmp_path: Path,
) -> None:
    allocator, profile, allocation = make_allocation(tmp_path, "rt.p146.rb.pre")
    handle = runtime_handle(
        allocation.runtime_id, allocation.workspace_ref.workspace_id
    )

    wrong_request = ra.RuntimeRollbackRequest(**{
        **rollback_request(handle).model_dump(),
        "runtime_id": "rt.other",
    })
    with pytest.raises(RuntimeRollbackIdentityError):
        coordinator(allocator).rollback(
            request=wrong_request,
            runtime_handle=handle,
            profile=profile,
            allocation=allocation,
            event_journal=event_journal(handle),
        )

    wrong_handle = runtime_handle(
        allocation.runtime_id,
        allocation.workspace_ref.workspace_id,
        state=ra.RuntimeLifecycleState.READY,
    )
    with pytest.raises(RuntimeRollbackStateError):
        coordinator(allocator).rollback(
            request=rollback_request(wrong_handle),
            runtime_handle=wrong_handle,
            profile=profile,
            allocation=allocation,
            event_journal=event_journal(wrong_handle),
        )

    owner = HermesProcessOwner()
    process_handle = runtime_handle(
        allocation.runtime_id,
        allocation.workspace_ref.workspace_id,
        state=ra.RuntimeLifecycleState.STARTING,
    )
    try:
        owner.launch(
            process_handle,
            ResolvedProcessLaunchPlan(
                profile_id=profile.profile_ref.profile_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                executable=sys.executable,
                arguments=(str(PROBE), "--sleep-ms", "5000"),
                working_directory=str(tmp_path),
                environment_items=explicit_test_environment(),
                stdout_limit_bytes=4096,
                stderr_limit_bytes=4096,
            ),
        )
        with pytest.raises(RuntimeRollbackProcessStillOwnedError):
            coordinator(allocator, owner).rollback(
                request=rollback_request(handle),
                runtime_handle=handle,
                profile=profile,
                allocation=allocation,
                event_journal=event_journal(handle),
            )
    finally:
        cleanup_owner(owner, allocation.runtime_id)

    foreign_allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=tmp_path / "base",
        workspace_id_factory=id_factory("b" * 32),
    )
    with pytest.raises(RuntimeRollbackStateError):
        coordinator(foreign_allocator).rollback(
            request=rollback_request(handle),
            runtime_handle=handle,
            profile=profile,
            allocation=allocation,
            event_journal=event_journal(handle),
        )


@pytest.mark.parametrize(
    "marker_payload",
    (
        None,
        b"\xff",
        b"{",
        {"schema_version": 2},
        {
            "schema_version": 1,
            "runtime_id": "rt.other",
            "workspace_id": "ws_wrong",
            "workspace_policy_id": "runtime.workspace.test.lifecycle_probe.v1",
        },
        {
            "schema_version": 1,
            "runtime_id": "rt.p146.rb.marker",
            "workspace_id": "ws_wrong",
            "workspace_policy_id": "runtime.workspace.test.lifecycle_probe.v1",
        },
        {
            "schema_version": 1,
            "runtime_id": "rt.p146.rb.marker",
            "workspace_id": "ws_" + "c" * 32,
            "workspace_policy_id": "runtime.workspace.other.v1",
        },
        {
            "schema_version": 1,
            "runtime_id": "rt.p146.rb.marker",
            "workspace_id": "ws_" + "c" * 32,
            "workspace_policy_id": "runtime.workspace.test.lifecycle_probe.v1",
            "extra": True,
        },
    ),
)
def test_marker_validation_failures_return_rollback_failed_without_deleting(
    tmp_path: Path,
    marker_payload,
) -> None:
    allocator, profile, allocation = make_allocation(
        tmp_path,
        "rt.p146.rb.marker",
        "c" * 32,
    )
    marker = allocation.paths.ownership_marker
    if marker_payload is None:
        marker.unlink()
    elif isinstance(marker_payload, bytes):
        marker.write_bytes(marker_payload)
    else:
        marker.write_text(json.dumps(marker_payload), encoding="utf-8")
    handle = runtime_handle(
        allocation.runtime_id, allocation.workspace_ref.workspace_id
    )

    result = coordinator(allocator).rollback(
        request=rollback_request(handle),
        runtime_handle=handle,
        profile=profile,
        allocation=allocation,
        event_journal=event_journal(handle),
    )

    assert result.outcome is ra.RuntimeOperationOutcome.ROLLBACK_FAILED
    assert (
        result.runtime_handle.lifecycle_state
        is ra.RuntimeLifecycleState.ROLLBACK_FAILED
    )
    assert result.failure is not None
    assert result.failure.failure_code == "runtime_rollback_marker_error"
    assert allocation.paths.workspace_root.exists()


def test_oversized_and_symlink_marker_are_rejected_without_deleting(
    tmp_path: Path,
) -> None:
    allocator, profile, allocation = make_allocation(
        tmp_path, "rt.p146.rb.big", "d" * 32
    )
    allocation.paths.ownership_marker.write_bytes(b"x" * 4097)
    handle = runtime_handle(
        allocation.runtime_id, allocation.workspace_ref.workspace_id
    )
    result = coordinator(allocator).rollback(
        request=rollback_request(handle),
        runtime_handle=handle,
        profile=profile,
        allocation=allocation,
        event_journal=event_journal(handle),
    )
    assert result.failure is not None
    assert result.failure.failure_code == "runtime_rollback_marker_error"
    assert allocation.paths.workspace_root.exists()

    allocator2, profile2, allocation2 = make_allocation(
        tmp_path,
        "rt.p146.rb.symlink",
        "e" * 32,
    )
    target = allocation2.paths.workspace_root / "target-marker"
    target.write_text("{}", encoding="utf-8")
    allocation2.paths.ownership_marker.unlink()
    try:
        os.symlink(target, allocation2.paths.ownership_marker)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable")
    handle2 = runtime_handle(
        allocation2.runtime_id, allocation2.workspace_ref.workspace_id
    )
    result2 = coordinator(allocator2).rollback(
        request=rollback_request(handle2),
        runtime_handle=handle2,
        profile=profile2,
        allocation=allocation2,
        event_journal=event_journal(handle2),
    )
    assert result2.failure is not None
    assert result2.failure.failure_code == "runtime_rollback_marker_error"
    assert allocation2.paths.workspace_root.exists()


def test_safe_preflight_rejects_redirects_special_files_depth_and_entry_bounds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    allocator, profile, allocation = make_allocation(
        tmp_path, "rt.p146.rb.tree", "f" * 32
    )
    handle = runtime_handle(
        allocation.runtime_id, allocation.workspace_ref.workspace_id
    )
    symlink_target = allocation.paths.workdir / "target.txt"
    symlink_target.write_text("safe", encoding="utf-8")
    symlink_path = allocation.paths.workdir / "link.txt"
    try:
        os.symlink(symlink_target, symlink_path)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable")
    result = coordinator(allocator).rollback(
        request=rollback_request(handle),
        runtime_handle=handle,
        profile=profile,
        allocation=allocation,
        event_journal=event_journal(handle),
    )
    assert result.failure is not None
    assert result.failure.failure_code in {
        "runtime_rollback_entry_type_error",
        "runtime_rollback_containment_error",
    }
    assert allocation.paths.workspace_root.exists()

    allocator2, profile2, allocation2 = make_allocation(
        tmp_path,
        "rt.p146.rb.depth",
        "1" * 32,
    )
    deep = allocation2.paths.workdir
    for index in range(65):
        deep = deep / f"d{index}"
        deep.mkdir()
    handle2 = runtime_handle(
        allocation2.runtime_id, allocation2.workspace_ref.workspace_id
    )
    result2 = coordinator(allocator2).rollback(
        request=rollback_request(handle2),
        runtime_handle=handle2,
        profile=profile2,
        allocation=allocation2,
        event_journal=event_journal(handle2),
    )
    assert result2.failure is not None
    assert result2.failure.failure_code == "runtime_rollback_tree_limit_error"

    allocator3, profile3, allocation3 = make_allocation(
        tmp_path,
        "rt.p146.rb.count",
        "2" * 32,
    )
    (allocation3.paths.workdir / "one.txt").write_text("safe", encoding="utf-8")
    monkeypatch.setattr(
        "hermes_cli.agent_platform.runtime_adapter.rollback._MAX_TREE_ENTRIES",
        1,
    )
    handle3 = runtime_handle(
        allocation3.runtime_id, allocation3.workspace_ref.workspace_id
    )
    result3 = coordinator(allocator3).rollback(
        request=rollback_request(handle3),
        runtime_handle=handle3,
        profile=profile3,
        allocation=allocation3,
        event_journal=event_journal(handle3),
    )
    assert result3.failure is not None
    assert result3.failure.failure_code == "runtime_rollback_tree_limit_error"


def test_successful_rollback_removes_only_owned_workspace_and_releases_allocator(
    tmp_path: Path,
) -> None:
    allocator, profile, allocation = make_allocation(
        tmp_path, "rt.p146.rb.success", "3" * 32
    )
    sibling = allocation.paths.workspace_root.parent / ("ws_" + "4" * 32)
    sibling.mkdir()
    (allocation.paths.workdir / "artifact.txt").write_text("not read", encoding="utf-8")
    nested = allocation.paths.evidence / "nested"
    nested.mkdir()
    (nested / "evidence.bin").write_bytes(b"bytes")
    handle = runtime_handle(
        allocation.runtime_id, allocation.workspace_ref.workspace_id
    )

    result = coordinator(allocator).rollback(
        request=rollback_request(handle),
        runtime_handle=handle,
        profile=profile,
        allocation=allocation,
        event_journal=event_journal(handle),
    )

    assert result.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.ROLLED_BACK
    assert result.outcome is ra.RuntimeOperationOutcome.ROLLED_BACK
    assert result.workspace_reference is not None
    assert result.workspace_reference.status is ra.RuntimeWorkspaceStatus.CLEANED
    assert result.workspace_reference.managed_files_root_bound is False
    assert not allocation.paths.workspace_root.exists()
    assert sibling.is_dir()
    with pytest.raises(UnknownRuntimeWorkspaceError):
        allocator.get(allocation.runtime_id)
    assert [event.event_type for event in result.events] == [
        ra.RuntimeEventType.ROLLBACK_STARTED,
        ra.RuntimeEventType.WORKSPACE_CLEANUP_STARTED,
        ra.RuntimeEventType.WORKSPACE_CLEANUP_COMPLETED,
        ra.RuntimeEventType.ROLLBACK_COMPLETED,
    ]
    audit = project_runtime_operation_audit(result)
    assert audit.outcome is ra.RuntimeOperationOutcome.ROLLED_BACK


def test_deletion_failure_is_explicit_and_preserves_remaining_workspace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    allocator, profile, allocation = make_allocation(
        tmp_path, "rt.p146.rb.delete", "5" * 32
    )
    (allocation.paths.workdir / "artifact.txt").write_text("safe", encoding="utf-8")
    handle = runtime_handle(
        allocation.runtime_id, allocation.workspace_ref.workspace_id
    )

    def fail_delete(*_args, **_kwargs) -> None:
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="test_file_delete_failed",
        )

    monkeypatch.setattr(
        "hermes_cli.agent_platform.runtime_adapter.rollback._delete_regular_file",
        fail_delete,
    )
    result = coordinator(allocator).rollback(
        request=rollback_request(handle),
        runtime_handle=handle,
        profile=profile,
        allocation=allocation,
        event_journal=event_journal(handle),
    )

    assert result.outcome is ra.RuntimeOperationOutcome.ROLLBACK_FAILED
    assert (
        result.runtime_handle.lifecycle_state
        is ra.RuntimeLifecycleState.ROLLBACK_FAILED
    )
    assert result.failure is not None
    assert result.failure.failure_code == "runtime_rollback_deletion_error"
    assert allocation.paths.workspace_root.exists()
    assert str(allocation.paths.workspace_root) not in str(result.failure)


def test_rollback_source_safety_and_root_exports() -> None:
    forbidden_text = {
        "shell=True",
        "os.system",
        "os.popen",
        "PowerShell",
        "cmd.exe",
        "taskkill /IM",
        "shutil.rmtree",
        "glob(",
        "Path.home",
        "expanduser",
        "os.environ",
        "os.getenv",
        "requests",
        "httpx",
        "socket",
        "git reset",
        "git restore",
        "git checkout",
        "git clean",
        "audit_log",
        "provider",
        "worker launch",
        "agent launch",
        "MCP execution",
    }
    for source_path in (SOURCE_PATH, WORKSPACE_SOURCE):
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
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {"unlink", "rmdir", "remove"}

    assert not hasattr(ra, "RuntimeWorkspaceRollbackCoordinator")
    assert "RuntimeWorkspaceRollbackCoordinator" not in ra.__all__
