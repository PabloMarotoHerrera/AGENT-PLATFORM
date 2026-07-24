from __future__ import annotations

import ast
import io
import os
import subprocess
import sys
import time
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    DuplicateRuntimeOwnershipError,
    HermesProcessOwner,
    InvalidListenerOwnershipError,
    InvalidRuntimeHandleStateError,
    OwnedProcessDrainIncompleteError,
    OwnedProcessSnapshot,
    OwnedProcessStillRunningError,
    OwnedProcessTerminationError,
    ProcessLaunchError,
    ResolvedProcessLaunchPlan,
    RuntimeProcessOwnerError,
    UnknownRuntimeOwnershipError,
)
from hermes_cli.agent_platform.runtime_adapter.process_tree import (
    ProcessTreeBackend,
    ProcessTreeSnapshot,
    ProcessTreeTerminationResult,
)


PACKAGE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
)
PROBE = Path(__file__).with_name("runtime_adapter_lifecycle_probe.py")
PROFILE_ID = ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
WORKSPACE_ID = "workspace-001"
WAIT_TIMEOUT_SECONDS = 5.0
POLL_INTERVAL_SECONDS = 0.05


def utc_now():
    from datetime import datetime, timezone

    return datetime.now(timezone.utc)


def explicit_test_environment() -> tuple[tuple[str, str], ...]:
    values = {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    }
    for key in ("PATH", "SystemRoot", "WINDIR", "TEMP", "TMP"):
        if key in os.environ:
            values[key] = os.environ[key]
    return tuple(sorted(values.items()))


def runtime_handle(
    *,
    runtime_id: str = "rt_p142_001",
    profile_id: str = PROFILE_ID,
    workspace_id: str = WORKSPACE_ID,
    state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.STARTING,
) -> ra.RuntimeHandle:
    return ra.RuntimeHandle(
        schema_version=ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION,
        runtime_id=runtime_id,
        correlation_id=f"corr:p14.2:{runtime_id}",
        profile_id=profile_id,
        workspace_id=workspace_id,
        lifecycle_state=state,
        created_at_utc=utc_now(),
    )


def launch_plan(
    tmp_path: Path,
    *,
    profile_id: str = PROFILE_ID,
    workspace_id: str = WORKSPACE_ID,
    executable: str | None = None,
    arguments: tuple[str, ...] = (),
    environment_items: tuple[tuple[str, str], ...] | None = None,
    stdout_limit_bytes: int = 4096,
    stderr_limit_bytes: int = 4096,
) -> ResolvedProcessLaunchPlan:
    return ResolvedProcessLaunchPlan(
        profile_id=profile_id,
        workspace_id=workspace_id,
        executable=sys.executable if executable is None else executable,
        arguments=(str(PROBE), *arguments),
        working_directory=str(tmp_path),
        environment_items=environment_items or explicit_test_environment(),
        stdout_limit_bytes=stdout_limit_bytes,
        stderr_limit_bytes=stderr_limit_bytes,
    )


def wait_for_snapshot(
    owner: HermesProcessOwner,
    runtime_id: str,
    predicate,
    *,
    timeout_seconds: float = WAIT_TIMEOUT_SECONDS,
) -> OwnedProcessSnapshot:
    deadline = time.monotonic() + timeout_seconds
    last_snapshot = owner.snapshot(runtime_id)
    while time.monotonic() < deadline:
        last_snapshot = owner.snapshot(runtime_id)
        if predicate(last_snapshot):
            return last_snapshot
        time.sleep(POLL_INTERVAL_SECONDS)
    raise AssertionError(f"timed out waiting for runtime {runtime_id}: {last_snapshot}")


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
            wait_for_snapshot(
                owner,
                runtime_id,
                lambda snap: (
                    snap.process_reference.process_status
                    is not ra.RuntimeProcessStatus.RUNNING
                ),
            )
            owner.release(runtime_id)
        except (UnknownRuntimeOwnershipError, OwnedProcessDrainIncompleteError):
            pass


def test_launch_plan_validation_immutability_repr_and_bounds(tmp_path: Path) -> None:
    plan = launch_plan(
        tmp_path,
        arguments=("--sleep-ms", "10"),
        environment_items=(
            ("P14_EXPLICIT", "yes"),
            ("PYTHONUTF8", "1"),
        ),
    )

    with pytest.raises(FrozenInstanceError):
        plan.profile_id = "other"  # type: ignore[misc]

    representation = repr(plan)
    assert sys.executable not in representation
    assert str(tmp_path) not in representation
    assert "--sleep-ms" not in representation
    assert "yes" not in representation
    assert "argument_count=3" in representation
    assert "environment_count=2" in representation

    cases = [
        {"executable": ""},
        {"executable": "python"},
        {"arguments": ("x" * 4097,)},
        {"arguments": tuple("x" for _ in range(257))},
        {"arguments": ("x" * 129,) * 255},
        {"arguments": ("bad\x00arg",)},
        {"environment_items": (("PATH", "a"), ("Path", "b"))},
        {"environment_items": (("A=B", "value"),)},
        {"environment_items": (("BAD\x00KEY", "value"),)},
        {"environment_items": (("KEY", "v" * 16385),)},
        {"environment_items": tuple((f"K{i}", "v") for i in range(513))},
        {"stdout_limit_bytes": 1023},
        {"stderr_limit_bytes": 1_048_577},
    ]
    for overrides in cases:
        with pytest.raises(ValueError):
            launch_plan(tmp_path, **overrides)

    with pytest.raises(ValueError):
        ResolvedProcessLaunchPlan(
            profile_id=PROFILE_ID,
            workspace_id=WORKSPACE_ID,
            executable=sys.executable,
            arguments=(),
            working_directory="relative",
            environment_items=(),
            stdout_limit_bytes=1024,
            stderr_limit_bytes=1024,
        )


def test_launch_starts_inert_process_and_enforces_preconditions(tmp_path: Path) -> None:
    owner = HermesProcessOwner()
    runtime_id = "rt_p142_launch"
    try:
        snapshot = owner.launch(
            runtime_handle(runtime_id=runtime_id),
            launch_plan(tmp_path, arguments=("--sleep-ms", "4000")),
        )
        assert snapshot.process_reference.launcher_pid is not None
        assert snapshot.process_reference.launcher_pid > 0
        assert (
            snapshot.process_reference.process_status is ra.RuntimeProcessStatus.RUNNING
        )
        assert owner.owned_runtime_ids() == (runtime_id,)

        with pytest.raises(DuplicateRuntimeOwnershipError):
            owner.launch(
                runtime_handle(runtime_id=runtime_id),
                launch_plan(tmp_path, arguments=("--sleep-ms", "10")),
            )
    finally:
        cleanup_owner(owner, runtime_id)

    with pytest.raises(InvalidRuntimeHandleStateError):
        HermesProcessOwner().launch(
            runtime_handle(
                runtime_id="rt_p142_wrong_state",
                state=ra.RuntimeLifecycleState.CREATED,
            ),
            launch_plan(tmp_path, arguments=("--sleep-ms", "10")),
        )
    with pytest.raises(ProcessLaunchError):
        HermesProcessOwner().launch(
            runtime_handle(runtime_id="rt_p142_profile"),
            launch_plan(tmp_path, profile_id="other.profile"),
        )
    with pytest.raises(ProcessLaunchError):
        HermesProcessOwner().launch(
            runtime_handle(runtime_id="rt_p142_workspace"),
            launch_plan(tmp_path, workspace_id="workspace-other"),
        )


def test_launch_uses_shell_disabled_explicit_environment_and_process_group(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    class FakePopen:
        pid = 43210
        stdout = io.BytesIO(b"")
        stderr = io.BytesIO(b"")
        returncode = None

        def __init__(self, argv, **kwargs):
            captured["argv"] = argv
            captured["kwargs"] = kwargs

        def poll(self):
            return None

        def wait(self, timeout=None):
            self.returncode = 0
            return 0

    class FakeBackend(ProcessTreeBackend):
        def discover_descendants(self, root_pid: int) -> ProcessTreeSnapshot:
            return ProcessTreeSnapshot(root_pid, (), utc_now(), True)

    monkeypatch.setenv("P14_PARENT_ONLY", "must-not-merge")
    monkeypatch.setattr(
        "hermes_cli.agent_platform.runtime_adapter.process_owner.subprocess.Popen",
        FakePopen,
    )
    explicit_env = (("P14_CHILD_ONLY", "1"),)
    owner = HermesProcessOwner(process_tree_backend=FakeBackend())
    owner.launch(
        runtime_handle(runtime_id="rt_p142_fake"),
        launch_plan(
            tmp_path,
            arguments=("--sleep-ms", "10"),
            environment_items=explicit_env,
        ),
    )

    kwargs = captured["kwargs"]
    assert isinstance(kwargs, dict)
    assert captured["argv"] == [sys.executable, str(PROBE), "--sleep-ms", "10"]
    assert kwargs["shell"] is False
    assert kwargs["stdin"] is subprocess.DEVNULL
    assert kwargs["stdout"] is subprocess.PIPE
    assert kwargs["stderr"] is subprocess.PIPE
    assert kwargs["text"] is False
    assert kwargs["cwd"] == str(tmp_path)
    assert kwargs["env"] == {"P14_CHILD_ONLY": "1"}
    assert "P14_PARENT_ONLY" not in kwargs["env"]
    if sys.platform == "win32":
        assert kwargs["creationflags"] & subprocess.CREATE_NEW_PROCESS_GROUP
        assert "start_new_session" not in kwargs
    else:
        assert kwargs["start_new_session"] is True


def test_natural_exit_preserves_exit_code_reaps_and_releases(tmp_path: Path) -> None:
    owner = HermesProcessOwner()
    runtime_id = "rt_p142_exit"
    try:
        owner.launch(
            runtime_handle(runtime_id=runtime_id),
            launch_plan(tmp_path, arguments=("--sleep-ms", "50", "--exit-code", "7")),
        )
        snapshot = wait_for_snapshot(
            owner,
            runtime_id,
            lambda snap: (
                snap.process_reference.process_status is ra.RuntimeProcessStatus.EXITED
            ),
        )
        assert snapshot.process_reference.exit_code == 7
        assert snapshot.process_reference.exited_at_utc is not None
        assert snapshot.process_reference.exited_at_utc.utcoffset() is not None
        owner.release(runtime_id)
        with pytest.raises(UnknownRuntimeOwnershipError):
            owner.snapshot(runtime_id)
        with pytest.raises(UnknownRuntimeOwnershipError):
            owner.release(runtime_id)
    finally:
        cleanup_owner(owner, runtime_id)


def test_bounded_stdout_stderr_snapshots_never_expose_raw_output(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    small_id = "rt_p142_small_output"
    large_id = "rt_p142_large_output"
    try:
        owner.launch(
            runtime_handle(runtime_id=small_id),
            launch_plan(
                tmp_path,
                arguments=("--stdout-bytes", "128", "--stderr-bytes", "64"),
            ),
        )
        small = wait_for_snapshot(
            owner,
            small_id,
            lambda snap: (
                snap.stdout_snapshot.drain_complete
                and snap.stderr_snapshot.drain_complete
            ),
        )
        assert small.stdout_snapshot.total_bytes_read == 128
        assert small.stderr_snapshot.total_bytes_read == 64
        assert small.stdout_snapshot.bounded_bytes == 128
        assert small.stderr_snapshot.bounded_bytes == 64
        assert small.stdout_snapshot.discarded_bytes == 0
        assert small.stderr_snapshot.discarded_bytes == 0
        assert small.stdout_snapshot.truncated is False
        assert small.stderr_snapshot.truncated is False
        assert not hasattr(small.stdout_snapshot, "raw_bytes")
        assert not hasattr(small.stderr_snapshot, "raw_text")
        owner.release(small_id)

        owner.launch(
            runtime_handle(runtime_id=large_id),
            launch_plan(
                tmp_path,
                arguments=("--stdout-bytes", "4096", "--stderr-bytes", "3072"),
                stdout_limit_bytes=1024,
                stderr_limit_bytes=1024,
            ),
        )
        large = wait_for_snapshot(
            owner,
            large_id,
            lambda snap: (
                snap.stdout_snapshot.drain_complete
                and snap.stderr_snapshot.drain_complete
            ),
        )
        assert large.stdout_snapshot.total_bytes_read == 4096
        assert large.stdout_snapshot.bounded_bytes == 1024
        assert large.stdout_snapshot.discarded_bytes == 3072
        assert large.stdout_snapshot.truncated is True
        assert large.stderr_snapshot.total_bytes_read == 3072
        assert large.stderr_snapshot.bounded_bytes == 1024
        assert large.stderr_snapshot.discarded_bytes == 2048
        assert large.stderr_snapshot.truncated is True
        owner.release(large_id)
    finally:
        cleanup_owner(owner, small_id, large_id)


def test_process_tree_discovers_owned_child_without_unrelated_pids(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    runtime_id = "rt_p142_tree"
    try:
        owner.launch(
            runtime_handle(runtime_id=runtime_id),
            launch_plan(
                tmp_path,
                arguments=(
                    "--spawn-child",
                    "--sleep-ms",
                    "4000",
                    "--child-sleep-ms",
                    "4000",
                ),
            ),
        )
        snapshot = wait_for_snapshot(
            owner,
            runtime_id,
            lambda snap: bool(snap.process_reference.descendant_pids),
        )
        descendants = snapshot.process_reference.descendant_pids
        assert snapshot.process_reference.launcher_pid not in descendants
        assert tuple(sorted(descendants)) == descendants
        assert len(descendants) == len(set(descendants))
        assert os.getpid() not in descendants
    finally:
        cleanup_owner(owner, runtime_id)


def test_listener_binding_requires_launcher_or_current_descendant(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    runtime_id = "rt_p142_listener"
    try:
        launched = owner.launch(
            runtime_handle(runtime_id=runtime_id),
            launch_plan(
                tmp_path,
                arguments=(
                    "--spawn-child",
                    "--sleep-ms",
                    "4000",
                    "--child-sleep-ms",
                    "4000",
                ),
            ),
        )
        launcher_pid = launched.process_reference.launcher_pid
        assert launcher_pid is not None
        launcher_bound = owner.bind_listener_pid(runtime_id, launcher_pid)
        assert launcher_bound.process_reference.listener_pid == launcher_pid

        with pytest.raises(InvalidListenerOwnershipError):
            owner.bind_listener_pid(runtime_id, -1)
        with pytest.raises(InvalidListenerOwnershipError):
            owner.bind_listener_pid(runtime_id, os.getpid())
        with pytest.raises(UnknownRuntimeOwnershipError):
            owner.bind_listener_pid("missing-runtime", launcher_pid)

        child_snapshot = wait_for_snapshot(
            owner,
            runtime_id,
            lambda snap: bool(snap.process_reference.descendant_pids),
        )
        child_pid = child_snapshot.process_reference.descendant_pids[0]
        child_bound = owner.bind_listener_pid(runtime_id, child_pid)
        assert child_bound.process_reference.listener_pid == child_pid
        assert child_pid not in child_bound.process_reference.descendant_pids
    finally:
        cleanup_owner(owner, runtime_id)


def test_exact_tree_termination_targets_root_and_child_then_releases(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    backend = ProcessTreeBackend()
    runtime_id = "rt_p142_terminate"
    try:
        launched = owner.launch(
            runtime_handle(runtime_id=runtime_id),
            launch_plan(
                tmp_path,
                arguments=(
                    "--spawn-child",
                    "--sleep-ms",
                    "5000",
                    "--child-sleep-ms",
                    "5000",
                ),
            ),
        )
        root_pid = launched.process_reference.launcher_pid
        assert root_pid is not None
        child_snapshot = wait_for_snapshot(
            owner,
            runtime_id,
            lambda snap: bool(snap.process_reference.descendant_pids),
        )
        child_pids = child_snapshot.process_reference.descendant_pids
        terminated = owner.terminate_owned_tree(runtime_id, timeout_ms=5000)

        assert (
            terminated.process_reference.process_status
            is ra.RuntimeProcessStatus.TERMINATED
        )
        assert terminated.termination_result is not None
        assert terminated.termination_result.mechanism in {
            "windows_taskkill_exact_pid_tree",
            "posix_killpg_owned_group",
        }
        assert root_pid in terminated.termination_result.targeted_pids
        for child_pid in child_pids:
            assert child_pid in terminated.termination_result.targeted_pids
        assert terminated.termination_result.still_alive_pids == ()
        assert backend.pid_exists(root_pid) is False
        for child_pid in child_pids:
            assert backend.pid_exists(child_pid) is False
        owner.release(runtime_id)
    finally:
        cleanup_owner(owner, runtime_id)


def test_release_guards_running_processes_and_runtime_ids_are_sorted(
    tmp_path: Path,
) -> None:
    owner = HermesProcessOwner()
    first = "rt_p142_b"
    second = "rt_p142_a"
    try:
        owner.launch(
            runtime_handle(runtime_id=first),
            launch_plan(tmp_path, arguments=("--sleep-ms", "4000")),
        )
        owner.launch(
            runtime_handle(runtime_id=second),
            launch_plan(tmp_path, arguments=("--sleep-ms", "4000")),
        )
        ids = owner.owned_runtime_ids()
        assert ids == tuple(sorted(ids))
        assert isinstance(ids, tuple)
        with pytest.raises(OwnedProcessStillRunningError):
            owner.release(first)
    finally:
        cleanup_owner(owner, first, second)


def test_unknown_and_bounded_failure_paths(tmp_path: Path) -> None:
    owner = HermesProcessOwner()
    with pytest.raises(UnknownRuntimeOwnershipError):
        owner.snapshot("missing-runtime")
    with pytest.raises(UnknownRuntimeOwnershipError):
        owner.terminate_owned_tree("missing-runtime", timeout_ms=100)
    with pytest.raises(UnknownRuntimeOwnershipError):
        owner.release("missing-runtime")

    bad_executable = str(tmp_path / "missing-python-executable")
    with pytest.raises(ProcessLaunchError) as exc_info:
        HermesProcessOwner().launch(
            runtime_handle(runtime_id="rt_p142_bad_exec"),
            launch_plan(
                tmp_path,
                executable=bad_executable,
                arguments=("--sleep-ms", "10"),
            ),
        )
    message = str(exc_info.value)
    assert exc_info.value.error_code == "process_launch_error"
    assert "FileNotFoundError" in message
    assert bad_executable not in message
    assert "--sleep-ms" not in message
    assert "PATH" not in message


def test_termination_verification_failure_is_explicit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakePopen:
        pid = 54321
        stdout = io.BytesIO(b"")
        stderr = io.BytesIO(b"")
        returncode = None

        def __init__(self, _argv, **_kwargs):
            pass

        def poll(self):
            return None

        def wait(self, timeout=None):
            self.returncode = -9
            return -9

    class FailingBackend(ProcessTreeBackend):
        def discover_descendants(self, root_pid: int) -> ProcessTreeSnapshot:
            return ProcessTreeSnapshot(root_pid, (), utc_now(), True)

        def terminate_tree(
            self,
            root_pid: int,
            *,
            timeout_ms: int,
        ) -> ProcessTreeTerminationResult:
            return ProcessTreeTerminationResult(
                root_pid=root_pid,
                targeted_pids=(root_pid,),
                mechanism="test_failure_backend",
                attempted=True,
                terminated_pids=(),
                still_alive_pids=(root_pid,),
                timed_out=True,
                return_code=None,
                inspection_supported=True,
                completed_at_utc=utc_now(),
            )

        def pid_exists(self, pid: int) -> bool:
            return pid == 54321

    monkeypatch.setattr(
        "hermes_cli.agent_platform.runtime_adapter.process_owner.subprocess.Popen",
        FakePopen,
    )
    owner = HermesProcessOwner(process_tree_backend=FailingBackend())
    runtime_id = "rt_p142_term_failure"
    owner.launch(
        runtime_handle(runtime_id=runtime_id),
        launch_plan(tmp_path, arguments=("--sleep-ms", "10")),
    )

    with pytest.raises(OwnedProcessTerminationError) as exc_info:
        owner.terminate_owned_tree(runtime_id, timeout_ms=100)
    assert exc_info.value.error_code == "owned_process_termination_error"
    assert exc_info.value.fields["mechanism"] == "test_failure_backend"
    assert exc_info.value.fields["still_alive_count"] == 1


def test_source_guard_blocks_shell_process_name_cleanup_globals_and_live_runtime() -> (
    None
):
    source_paths = [
        PACKAGE_ROOT / "process_owner.py",
        PACKAGE_ROOT / "process_tree.py",
        PACKAGE_ROOT / "stream_capture.py",
        PROBE,
    ]
    forbidden_text = {
        "shell=True",
        "os.system",
        "os.popen",
        "taskkill /IM",
        "/IM",
        "Stop-Process",
        "Get-Process",
        "wmic process delete",
        "os.environ.copy",
        "atexit",
        "hermes dashboard",
        "hermes gateway",
        "RuntimeEvent(",
        "RuntimeReadinessRef(",
        "transition_runtime_state(",
        "logger.",
        "logging.",
    }

    for source_path in source_paths:
        text = source_path.read_text(encoding="utf-8")
        lowered = text.lower()
        for forbidden in forbidden_text:
            assert forbidden.lower() not in lowered, (source_path, forbidden)

        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in {"eval", "exec"}, source_path
                elif isinstance(node.func, ast.Attribute):
                    assert not (
                        isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "os"
                        and node.func.attr in {"system", "popen"}
                    ), source_path
                for keyword in node.keywords:
                    assert not (
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ), source_path

        for node in tree.body:
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                assert "record" not in node.target.id.lower(), source_path
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assert "registry" not in target.id.lower(), source_path

    process_tree_text = (PACKAGE_ROOT / "process_tree.py").read_text(encoding="utf-8")
    assert '["taskkill", "/PID", str(root_pid), "/T", "/F"]' in process_tree_text


def test_public_contract_root_remains_contract_only() -> None:
    assert not hasattr(ra, "ResolvedProcessLaunchPlan")
    assert not hasattr(ra, "HermesProcessOwner")
    assert "ResolvedProcessLaunchPlan" not in ra.__all__
    assert "HermesProcessOwner" not in ra.__all__

    forbidden_request_fields = {
        "command",
        "argv",
        "executable",
        "executable_path",
        "shell",
        "environment",
        "env",
        "cwd",
        "working_directory",
        "output_path",
        "signal",
        "kill_command",
    }
    public_models = [
        ra.RuntimeLaunchRequest,
        ra.RuntimeStopRequest,
        ra.RuntimeCancelRequest,
        ra.RuntimeRollbackRequest,
        ra.RuntimeProfileRef,
        ra.RuntimeWorkspaceBinding,
    ]
    for model in public_models:
        forbidden = forbidden_request_fields & set(model.model_fields)
        if forbidden == {"environment_policy_id"}:
            forbidden = set()
        assert not forbidden, (model.__name__, forbidden)

    assert ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION == 1
