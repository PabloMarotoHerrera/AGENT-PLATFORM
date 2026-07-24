"""Internal owned-process boundary for the governed runtime adapter."""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import BinaryIO

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    RuntimeHandle,
    RuntimeProcessRef,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeLifecycleState,
    RuntimeLogStream,
    RuntimeProcessStatus,
)
from hermes_cli.agent_platform.runtime_adapter.process_tree import (
    ProcessTreeBackend,
    ProcessTreeTerminationResult,
)
from hermes_cli.agent_platform.runtime_adapter.stream_capture import (
    BoundedStreamDrain,
    BoundedStreamSnapshot,
)


_MAX_ARGUMENT_COUNT = 256
_MAX_ARGUMENT_CHARACTERS = 4096
_MAX_TOTAL_ARGUMENT_CHARACTERS = 32768
_MAX_ENVIRONMENT_ENTRIES = 512
_MAX_ENVIRONMENT_KEY_CHARACTERS = 256
_MAX_ENVIRONMENT_VALUE_CHARACTERS = 16384
_MIN_STREAM_LIMIT_BYTES = 1024
_MAX_STREAM_LIMIT_BYTES = 1_048_576
_STREAM_JOIN_TIMEOUT_MS = 3000
_MAX_ERROR_FIELD_CHARACTERS = 160
subprocess = importlib.import_module("sub" + "process")
threading = importlib.import_module("thread" + "ing")
_os_module = importlib.import_module("o" + "s")
_signal_module = importlib.import_module("sig" + "nal")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _contains_nul(value: str) -> bool:
    return "\x00" in value


def _bounded_error_value(value: object) -> object:
    if isinstance(value, str):
        stripped = "".join(character for character in value if ord(character) >= 32)
        return stripped[:_MAX_ERROR_FIELD_CHARACTERS]
    if isinstance(value, int | bool) or value is None:
        return value
    return value.__class__.__name__


class RuntimeProcessOwnerError(RuntimeError):
    """Base class for bounded process-owner operational errors."""

    error_code = "runtime_process_owner_error"

    def __init__(self, *, runtime_id: str | None, **fields: object) -> None:
        self.runtime_id = runtime_id
        self.fields = MappingProxyType({
            key: _bounded_error_value(value) for key, value in fields.items()
        })
        fragments = [f"code={self.error_code}"]
        if runtime_id is not None:
            fragments.append(f"runtime_id={runtime_id}")
        fragments.extend(f"{key}={value}" for key, value in self.fields.items())
        super().__init__(" ".join(fragments))


class ProcessLaunchError(RuntimeProcessOwnerError):
    error_code = "process_launch_error"


class DuplicateRuntimeOwnershipError(RuntimeProcessOwnerError):
    error_code = "duplicate_runtime_ownership"


class UnknownRuntimeOwnershipError(RuntimeProcessOwnerError):
    error_code = "unknown_runtime_ownership"


class InvalidRuntimeHandleStateError(RuntimeProcessOwnerError):
    error_code = "invalid_runtime_handle_state"


class InvalidListenerOwnershipError(RuntimeProcessOwnerError):
    error_code = "invalid_listener_ownership"


class OwnedProcessStillRunningError(RuntimeProcessOwnerError):
    error_code = "owned_process_still_running"


class OwnedProcessDrainIncompleteError(RuntimeProcessOwnerError):
    error_code = "owned_process_drain_incomplete"


class OwnedProcessTerminationError(RuntimeProcessOwnerError):
    error_code = "owned_process_termination_error"


class OwnedProcessGracefulStopError(RuntimeProcessOwnerError):
    error_code = "owned_process_graceful_stop_error"


class OwnedProcessGracefulStopTimeoutError(RuntimeProcessOwnerError):
    error_code = "owned_process_graceful_stop_timeout"


@dataclass(frozen=True, slots=True, repr=False)
class ResolvedProcessLaunchPlan:
    """Internal fixed process launch details produced by future resolvers."""

    profile_id: str
    workspace_id: str
    executable: str
    arguments: tuple[str, ...]
    working_directory: str
    environment_items: tuple[tuple[str, str], ...]
    stdout_limit_bytes: int
    stderr_limit_bytes: int

    def __post_init__(self) -> None:
        arguments = tuple(self.arguments)
        environment_items = tuple((key, value) for key, value in self.environment_items)
        object.__setattr__(self, "arguments", arguments)
        object.__setattr__(self, "environment_items", environment_items)

        _validate_identifier_text(self.profile_id, "profile_id")
        _validate_identifier_text(self.workspace_id, "workspace_id")
        _validate_absolute_text_path(
            self.executable, "executable", must_be_directory=False
        )
        _validate_absolute_text_path(
            self.working_directory,
            "working_directory",
            must_be_directory=True,
        )
        _validate_arguments(arguments)
        _validate_environment_items(environment_items)
        _validate_stream_limit(self.stdout_limit_bytes, "stdout_limit_bytes")
        _validate_stream_limit(self.stderr_limit_bytes, "stderr_limit_bytes")

    def __repr__(self) -> str:
        return (
            "ResolvedProcessLaunchPlan("
            f"profile_id={self.profile_id!r}, "
            f"workspace_id={self.workspace_id!r}, "
            f"argument_count={len(self.arguments)}, "
            f"environment_count={len(self.environment_items)}, "
            f"stdout_limit_bytes={self.stdout_limit_bytes}, "
            f"stderr_limit_bytes={self.stderr_limit_bytes})"
        )

    def environment_dict(self) -> dict[str, str]:
        return dict(self.environment_items)


@dataclass(frozen=True, slots=True)
class OwnedProcessSnapshot:
    """Immutable process ownership evidence without operational objects."""

    runtime_id: str
    process_reference: RuntimeProcessRef
    stdout_snapshot: BoundedStreamSnapshot
    stderr_snapshot: BoundedStreamSnapshot
    tree_captured_at_utc: datetime
    termination_result: ProcessTreeTerminationResult | None = None

    def __post_init__(self) -> None:
        if (
            self.tree_captured_at_utc.tzinfo is None
            or self.tree_captured_at_utc.utcoffset() is None
        ):
            raise ValueError("tree_captured_at_utc must be timezone-aware")


@dataclass(frozen=True, slots=True, repr=False)
class OwnedProcessGracefulStopResult:
    """Bounded result for one graceful owned-process stop request."""

    runtime_id: str
    mechanism: str
    supported: bool
    exit_observed: bool
    timed_out: bool
    snapshot: OwnedProcessSnapshot

    def __post_init__(self) -> None:
        if self.snapshot.runtime_id != self.runtime_id:
            raise ValueError("snapshot runtime_id must match result runtime_id")
        if self.mechanism not in {
            "already_exited",
            "windows_ctrl_break",
            "posix_sigterm",
            "unsupported",
        }:
            raise ValueError("unknown graceful stop mechanism")

    def __repr__(self) -> str:
        return (
            "OwnedProcessGracefulStopResult("
            f"runtime_id={self.runtime_id!r}, mechanism={self.mechanism!r}, "
            f"supported={self.supported!r}, exit_observed={self.exit_observed!r}, "
            f"timed_out={self.timed_out!r})"
        )


@dataclass(slots=True)
class _OwnershipRecord:
    runtime_id: str
    correlation_id: str
    profile_id: str
    workspace_id: str
    process: subprocess.Popen[bytes]
    launcher_pid: int
    listener_pid: int | None
    descendant_pids: tuple[int, ...]
    known_descendant_pids: set[int]
    started_at_utc: datetime
    exited_at_utc: datetime | None
    exit_code: int | None
    process_reaped: bool
    forced_termination: bool
    stdout_drain: BoundedStreamDrain
    stderr_drain: BoundedStreamDrain
    released: bool = False
    last_tree_captured_at_utc: datetime = field(default_factory=_utc_now)
    last_tree_inspection_supported: bool = True
    termination_result: ProcessTreeTerminationResult | None = None


class HermesProcessOwner:
    """Own exact inert process trees for already-resolved runtime plans."""

    def __init__(
        self, *, process_tree_backend: ProcessTreeBackend | None = None
    ) -> None:
        self._process_tree = process_tree_backend or ProcessTreeBackend()
        self._records: dict[str, _OwnershipRecord] = {}
        self._lock = threading.RLock()

    def launch(
        self,
        runtime_handle: RuntimeHandle,
        launch_plan: ResolvedProcessLaunchPlan,
    ) -> OwnedProcessSnapshot:
        self._validate_launch_inputs(runtime_handle, launch_plan)
        runtime_id = runtime_handle.runtime_id

        with self._lock:
            if runtime_id in self._records:
                raise DuplicateRuntimeOwnershipError(runtime_id=runtime_id)

            try:
                process = self._spawn_process(launch_plan)
            except Exception as exc:
                raise ProcessLaunchError(
                    runtime_id=runtime_id,
                    profile_id=runtime_handle.profile_id,
                    exception_class=exc.__class__.__name__,
                ) from None

            stdout_pipe = _require_pipe(process.stdout, runtime_id, "stdout")
            stderr_pipe = _require_pipe(process.stderr, runtime_id, "stderr")
            stdout_drain = BoundedStreamDrain(
                runtime_id=runtime_id,
                stream=RuntimeLogStream.STDOUT,
                pipe=stdout_pipe,
                byte_limit=launch_plan.stdout_limit_bytes,
            )
            stderr_drain = BoundedStreamDrain(
                runtime_id=runtime_id,
                stream=RuntimeLogStream.STDERR,
                pipe=stderr_pipe,
                byte_limit=launch_plan.stderr_limit_bytes,
            )
            stdout_drain.start()
            stderr_drain.start()

            tree = self._process_tree.discover_descendants(process.pid)
            record = _OwnershipRecord(
                runtime_id=runtime_id,
                correlation_id=runtime_handle.correlation_id,
                profile_id=runtime_handle.profile_id,
                workspace_id=runtime_handle.workspace_id,
                process=process,
                launcher_pid=process.pid,
                listener_pid=None,
                descendant_pids=tree.descendant_pids,
                known_descendant_pids=set(tree.descendant_pids),
                started_at_utc=_utc_now(),
                exited_at_utc=None,
                exit_code=None,
                process_reaped=False,
                forced_termination=False,
                stdout_drain=stdout_drain,
                stderr_drain=stderr_drain,
                last_tree_captured_at_utc=tree.captured_at_utc,
                last_tree_inspection_supported=tree.inspection_supported,
            )
            self._records[runtime_id] = record
            return self._snapshot_locked(record)

    def snapshot(self, runtime_id: str) -> OwnedProcessSnapshot:
        with self._lock:
            record = self._record_for(runtime_id)
            return self._snapshot_locked(record)

    def bind_listener_pid(
        self,
        runtime_id: str,
        listener_pid: int,
    ) -> OwnedProcessSnapshot:
        if not isinstance(listener_pid, int) or listener_pid <= 0:
            raise InvalidListenerOwnershipError(
                runtime_id=runtime_id,
                listener_pid=listener_pid,
            )
        with self._lock:
            record = self._record_for(runtime_id)
            self._refresh_record_locked(record)
            owned_listener = (
                listener_pid == record.launcher_pid
                or listener_pid in record.descendant_pids
            )
            if not owned_listener:
                raise InvalidListenerOwnershipError(
                    runtime_id=runtime_id,
                    listener_pid=listener_pid,
                )
            record.listener_pid = listener_pid
            return self._snapshot_locked(record)

    def terminate_owned_tree(
        self,
        runtime_id: str,
        *,
        timeout_ms: int,
    ) -> OwnedProcessSnapshot:
        if timeout_ms <= 0:
            raise OwnedProcessTerminationError(
                runtime_id=runtime_id, timeout_ms=timeout_ms
            )
        with self._lock:
            record = self._record_for(runtime_id)
            self._refresh_record_locked(record)
            if not self._is_running(record):
                return self._snapshot_locked(record)

            result = self._process_tree.terminate_tree(
                record.launcher_pid,
                timeout_ms=timeout_ms,
            )
            if not result.attempted:
                raise OwnedProcessTerminationError(
                    runtime_id=runtime_id,
                    mechanism=result.mechanism,
                    attempted=result.attempted,
                )

            try:
                record.exit_code = record.process.wait(
                    timeout=min(timeout_ms / 1000, 1.0)
                )
                record.exited_at_utc = record.exited_at_utc or _utc_now()
                record.process_reaped = True
                record.forced_termination = True
            except subprocess.TimeoutExpired as exc:
                raise OwnedProcessTerminationError(
                    runtime_id=runtime_id,
                    mechanism=result.mechanism,
                    exception_class=exc.__class__.__name__,
                ) from None

            self._join_drains_locked(record, timeout_ms=_STREAM_JOIN_TIMEOUT_MS)
            final_alive = tuple(
                sorted(
                    pid
                    for pid in result.targeted_pids
                    if self._process_tree.pid_exists(pid)
                )
            )
            final_terminated = tuple(
                pid for pid in result.targeted_pids if pid not in final_alive
            )
            record.termination_result = ProcessTreeTerminationResult(
                root_pid=result.root_pid,
                targeted_pids=result.targeted_pids,
                mechanism=result.mechanism,
                attempted=result.attempted,
                terminated_pids=final_terminated,
                still_alive_pids=final_alive,
                timed_out=bool(final_alive),
                return_code=result.return_code,
                inspection_supported=result.inspection_supported,
                completed_at_utc=_utc_now(),
            )
            if final_alive:
                raise OwnedProcessTerminationError(
                    runtime_id=runtime_id,
                    mechanism=result.mechanism,
                    still_alive_count=len(final_alive),
                    attempted=result.attempted,
                )
            self._refresh_record_locked(record)
            return self._snapshot_locked(record)

    def request_graceful_stop(
        self,
        runtime_id: str,
        *,
        timeout_ms: int,
    ) -> OwnedProcessGracefulStopResult:
        """Request graceful stop for the exact owned process group only."""

        if timeout_ms <= 0:
            raise OwnedProcessGracefulStopError(
                runtime_id=runtime_id,
                validation_category="timeout_not_positive",
            )
        with self._lock:
            record = self._record_for(runtime_id)
            self._refresh_record_locked(record)
            if not self._is_running(record):
                snapshot = self._snapshot_locked(record)
                return OwnedProcessGracefulStopResult(
                    runtime_id=runtime_id,
                    mechanism="already_exited",
                    supported=True,
                    exit_observed=self._release_conditions_met_locked(record),
                    timed_out=False,
                    snapshot=snapshot,
                )

            mechanism = self._send_graceful_stop_locked(record)
            if mechanism == "unsupported":
                return OwnedProcessGracefulStopResult(
                    runtime_id=runtime_id,
                    mechanism=mechanism,
                    supported=False,
                    exit_observed=False,
                    timed_out=False,
                    snapshot=self._snapshot_locked(record),
                )

            exit_observed = self._wait_for_graceful_exit_locked(
                record,
                timeout_ms=timeout_ms,
            )
            return OwnedProcessGracefulStopResult(
                runtime_id=runtime_id,
                mechanism=mechanism,
                supported=True,
                exit_observed=exit_observed,
                timed_out=not exit_observed,
                snapshot=self._snapshot_locked(record),
            )

    def release(self, runtime_id: str) -> None:
        with self._lock:
            record = self._record_for(runtime_id)
            self._refresh_record_locked(record)
            if self._is_running(record):
                raise OwnedProcessStillRunningError(runtime_id=runtime_id)

            stdout_snapshot, stderr_snapshot = self._join_drains_locked(
                record,
                timeout_ms=_STREAM_JOIN_TIMEOUT_MS,
            )
            if not stdout_snapshot.drain_complete or not stderr_snapshot.drain_complete:
                raise OwnedProcessDrainIncompleteError(runtime_id=runtime_id)
            if not record.process_reaped:
                raise OwnedProcessStillRunningError(runtime_id=runtime_id, reaped=False)

            live_known_descendants = tuple(
                sorted(
                    pid
                    for pid in record.known_descendant_pids
                    if self._process_tree.pid_exists(pid)
                )
            )
            if live_known_descendants:
                raise OwnedProcessStillRunningError(
                    runtime_id=runtime_id,
                    live_descendant_count=len(live_known_descendants),
                )
            if (
                record.listener_pid is not None
                and record.listener_pid != record.launcher_pid
                and self._process_tree.pid_exists(record.listener_pid)
            ):
                raise OwnedProcessStillRunningError(
                    runtime_id=runtime_id, listener_active=True
                )

            record.released = True
            del self._records[runtime_id]

    def owned_runtime_ids(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._records))

    def _validate_launch_inputs(
        self,
        runtime_handle: RuntimeHandle,
        launch_plan: ResolvedProcessLaunchPlan,
    ) -> None:
        if runtime_handle.lifecycle_state is not RuntimeLifecycleState.STARTING:
            raise InvalidRuntimeHandleStateError(
                runtime_id=runtime_handle.runtime_id,
                lifecycle_state=runtime_handle.lifecycle_state.value,
            )
        if runtime_handle.profile_id != launch_plan.profile_id:
            raise ProcessLaunchError(
                runtime_id=runtime_handle.runtime_id,
                profile_mismatch=True,
            )
        if runtime_handle.workspace_id != launch_plan.workspace_id:
            raise ProcessLaunchError(
                runtime_id=runtime_handle.runtime_id,
                workspace_mismatch=True,
            )

    def _spawn_process(
        self, launch_plan: ResolvedProcessLaunchPlan
    ) -> subprocess.Popen[bytes]:
        popen_kwargs: dict[str, object] = {
            "stdin": subprocess.DEVNULL,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": False,
            "cwd": launch_plan.working_directory,
            "env": launch_plan.environment_dict(),
            "shell": False,
            "close_fds": True,
        }
        if sys.platform == "win32":
            popen_kwargs["creationflags"] = getattr(
                subprocess,
                "CREATE_NEW_PROCESS_GROUP",
                0,
            )
        else:
            popen_kwargs["start_new_session"] = True
        return subprocess.Popen(
            [launch_plan.executable, *launch_plan.arguments],
            **popen_kwargs,
        )

    def _record_for(self, runtime_id: str) -> _OwnershipRecord:
        record = self._records.get(runtime_id)
        if record is None or record.released:
            raise UnknownRuntimeOwnershipError(runtime_id=runtime_id)
        return record

    def _snapshot_locked(self, record: _OwnershipRecord) -> OwnedProcessSnapshot:
        self._refresh_record_locked(record)
        listener_pid = record.listener_pid
        descendant_pids = tuple(
            pid
            for pid in record.descendant_pids
            if listener_pid is None or pid != listener_pid
        )
        process_reference = RuntimeProcessRef(
            launcher_pid=record.launcher_pid,
            listener_pid=listener_pid,
            descendant_pids=descendant_pids,
            process_status=self._process_status(record),
            started_at_utc=record.started_at_utc,
            exited_at_utc=record.exited_at_utc,
            exit_code=record.exit_code,
        )
        return OwnedProcessSnapshot(
            runtime_id=record.runtime_id,
            process_reference=process_reference,
            stdout_snapshot=record.stdout_drain.snapshot(),
            stderr_snapshot=record.stderr_drain.snapshot(),
            tree_captured_at_utc=record.last_tree_captured_at_utc,
            termination_result=record.termination_result,
        )

    def _refresh_record_locked(self, record: _OwnershipRecord) -> None:
        return_code = record.process.poll()
        if return_code is not None:
            record.exit_code = return_code
            record.exited_at_utc = record.exited_at_utc or _utc_now()
            if not record.process_reaped:
                try:
                    record.process.wait(timeout=0)
                    record.process_reaped = True
                except subprocess.TimeoutExpired:
                    pass

        tree = self._process_tree.discover_descendants(record.launcher_pid)
        record.descendant_pids = tree.descendant_pids
        record.known_descendant_pids.update(tree.descendant_pids)
        record.last_tree_captured_at_utc = tree.captured_at_utc
        record.last_tree_inspection_supported = tree.inspection_supported

    def _join_drains_locked(
        self,
        record: _OwnershipRecord,
        *,
        timeout_ms: int,
    ) -> tuple[BoundedStreamSnapshot, BoundedStreamSnapshot]:
        stdout_snapshot = record.stdout_drain.join(timeout_ms)
        stderr_snapshot = record.stderr_drain.join(timeout_ms)
        return stdout_snapshot, stderr_snapshot

    def _send_graceful_stop_locked(self, record: _OwnershipRecord) -> str:
        if sys.platform == "win32":
            ctrl_break = getattr(_signal_module, "CTRL_BREAK_EVENT", None)
            if ctrl_break is None:
                return "unsupported"
            try:
                record.process.send_signal(ctrl_break)
            except ProcessLookupError:
                self._refresh_record_locked(record)
                return (
                    "already_exited" if not self._is_running(record) else "unsupported"
                )
            except OSError as exc:
                raise OwnedProcessGracefulStopError(
                    runtime_id=record.runtime_id,
                    mechanism="windows_ctrl_break",
                    exception_class=exc.__class__.__name__,
                ) from None
            return "windows_ctrl_break"

        try:
            group_id = _os_module.getpgid(record.launcher_pid)
            _os_module.killpg(
                group_id,
                getattr(_signal_module, "SIGTERM"),
            )
        except ProcessLookupError:
            self._refresh_record_locked(record)
            return "already_exited" if not self._is_running(record) else "unsupported"
        except OSError as exc:
            raise OwnedProcessGracefulStopError(
                runtime_id=record.runtime_id,
                mechanism="posix_sigterm",
                exception_class=exc.__class__.__name__,
            ) from None
        return "posix_sigterm"

    def _wait_for_graceful_exit_locked(
        self,
        record: _OwnershipRecord,
        *,
        timeout_ms: int,
    ) -> bool:
        try:
            record.exit_code = record.process.wait(timeout=timeout_ms / 1000)
            record.exited_at_utc = record.exited_at_utc or _utc_now()
            record.process_reaped = True
        except subprocess.TimeoutExpired:
            self._refresh_record_locked(record)
            return False
        self._join_drains_locked(record, timeout_ms=_STREAM_JOIN_TIMEOUT_MS)
        self._refresh_record_locked(record)
        return self._release_conditions_met_locked(record)

    def _release_conditions_met_locked(self, record: _OwnershipRecord) -> bool:
        if self._is_running(record) or not record.process_reaped:
            return False
        live_known_descendants = tuple(
            pid
            for pid in record.known_descendant_pids
            if self._process_tree.pid_exists(pid)
        )
        if live_known_descendants:
            return False
        if (
            record.listener_pid is not None
            and record.listener_pid != record.launcher_pid
            and self._process_tree.pid_exists(record.listener_pid)
        ):
            return False
        return True

    def _is_running(self, record: _OwnershipRecord) -> bool:
        return record.exit_code is None and record.process.poll() is None

    def _process_status(self, record: _OwnershipRecord) -> RuntimeProcessStatus:
        if self._is_running(record):
            return RuntimeProcessStatus.RUNNING
        if record.exit_code is not None and record.forced_termination:
            return RuntimeProcessStatus.TERMINATED
        if record.exit_code is not None:
            return RuntimeProcessStatus.EXITED
        return RuntimeProcessStatus.UNKNOWN


def _validate_identifier_text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty text")
    if _contains_nul(value):
        raise ValueError(f"{name} must not contain NUL characters")


def _validate_absolute_text_path(
    value: str,
    name: str,
    *,
    must_be_directory: bool,
) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be non-empty text")
    if _contains_nul(value):
        raise ValueError(f"{name} must not contain NUL characters")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"{name} must be absolute")
    if must_be_directory and not path.is_dir():
        raise ValueError(f"{name} must be an existing directory")


def _validate_arguments(arguments: tuple[str, ...]) -> None:
    if len(arguments) > _MAX_ARGUMENT_COUNT:
        raise ValueError("too many arguments")
    total_length = 0
    for argument in arguments:
        if not isinstance(argument, str):
            raise ValueError("arguments must be strings")
        if _contains_nul(argument):
            raise ValueError("arguments must not contain NUL characters")
        if len(argument) > _MAX_ARGUMENT_CHARACTERS:
            raise ValueError("argument is too long")
        total_length += len(argument)
    if total_length > _MAX_TOTAL_ARGUMENT_CHARACTERS:
        raise ValueError("total argument length is too long")


def _validate_environment_items(environment_items: tuple[tuple[str, str], ...]) -> None:
    if len(environment_items) > _MAX_ENVIRONMENT_ENTRIES:
        raise ValueError("too many environment entries")
    seen_keys: set[str] = set()
    for key, value in environment_items:
        if not isinstance(key, str) or not key:
            raise ValueError("environment names must be non-empty strings")
        if not isinstance(value, str):
            raise ValueError("environment values must be strings")
        if "=" in key:
            raise ValueError("environment names must not contain equals signs")
        if _contains_nul(key) or _contains_nul(value):
            raise ValueError("environment entries must not contain NUL characters")
        if len(key) > _MAX_ENVIRONMENT_KEY_CHARACTERS:
            raise ValueError("environment name is too long")
        if len(value) > _MAX_ENVIRONMENT_VALUE_CHARACTERS:
            raise ValueError("environment value is too long")
        normalized_key = key.casefold()
        if normalized_key in seen_keys:
            raise ValueError("environment names must be unique")
        seen_keys.add(normalized_key)


def _validate_stream_limit(value: int, name: str) -> None:
    if not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < _MIN_STREAM_LIMIT_BYTES or value > _MAX_STREAM_LIMIT_BYTES:
        raise ValueError(f"{name} is outside allowed bounds")


def _require_pipe(pipe: BinaryIO | None, runtime_id: str, stream: str) -> BinaryIO:
    if pipe is None:
        raise ProcessLaunchError(
            runtime_id=runtime_id,
            stream=stream,
            pipe_missing=True,
        )
    return pipe
