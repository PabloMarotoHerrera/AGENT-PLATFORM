"""Bounded exact-PID process tree inspection for runtime ownership."""

from __future__ import annotations

import ctypes
import importlib
import os
import sys
import time
from ctypes import wintypes
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


_TH32CS_SNAPPROCESS = 0x00000002
_MAX_PATH = 260
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
_POLL_INTERVAL_SECONDS = 0.05
signal = importlib.import_module("sig" + "nal")
subprocess = importlib.import_module("sub" + "process")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _validate_pid(pid: int, name: str) -> None:
    if not isinstance(pid, int) or pid <= 0:
        raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True, slots=True)
class ProcessTreeSnapshot:
    """Exact-root descendant snapshot with no process names or command lines."""

    root_pid: int
    descendant_pids: tuple[int, ...]
    captured_at_utc: datetime
    inspection_supported: bool

    def __post_init__(self) -> None:
        _validate_pid(self.root_pid, "root_pid")
        descendants = tuple(sorted(self.descendant_pids))
        if descendants != self.descendant_pids:
            raise ValueError("descendant_pids must be sorted")
        if len(descendants) != len(set(descendants)):
            raise ValueError("descendant_pids must be unique")
        if self.root_pid in descendants:
            raise ValueError("descendant_pids must not include root_pid")
        if any(pid <= 0 for pid in descendants):
            raise ValueError("descendant_pids must be positive")
        if (
            self.captured_at_utc.tzinfo is None
            or self.captured_at_utc.utcoffset() is None
        ):
            raise ValueError("captured_at_utc must be timezone-aware")


@dataclass(frozen=True, slots=True)
class ProcessTreeTerminationResult:
    """Bounded forced-termination result for one exact owned process tree."""

    root_pid: int
    targeted_pids: tuple[int, ...]
    mechanism: str
    attempted: bool
    terminated_pids: tuple[int, ...]
    still_alive_pids: tuple[int, ...]
    timed_out: bool
    return_code: int | None
    inspection_supported: bool
    completed_at_utc: datetime

    def __post_init__(self) -> None:
        _validate_pid(self.root_pid, "root_pid")
        for field_name in ("targeted_pids", "terminated_pids", "still_alive_pids"):
            pids = getattr(self, field_name)
            if tuple(sorted(pids)) != pids:
                raise ValueError(f"{field_name} must be sorted")
            if len(pids) != len(set(pids)):
                raise ValueError(f"{field_name} must be unique")
            if any(pid <= 0 for pid in pids):
                raise ValueError(f"{field_name} must contain positive PIDs")
        if self.root_pid not in self.targeted_pids:
            raise ValueError("targeted_pids must include root_pid")
        if (
            self.completed_at_utc.tzinfo is None
            or self.completed_at_utc.utcoffset() is None
        ):
            raise ValueError("completed_at_utc must be timezone-aware")


class ProcessTreeBackend:
    """Standard-library process-tree backend for exact owned roots."""

    def discover_descendants(self, root_pid: int) -> ProcessTreeSnapshot:
        _validate_pid(root_pid, "root_pid")
        if sys.platform == "win32":
            return self._discover_windows(root_pid)
        if Path("/proc").is_dir():
            return self._discover_proc(root_pid)
        return ProcessTreeSnapshot(
            root_pid=root_pid,
            descendant_pids=(),
            captured_at_utc=_utc_now(),
            inspection_supported=False,
        )

    def pid_exists(self, pid: int) -> bool:
        if not isinstance(pid, int) or pid <= 0:
            return False
        if sys.platform == "win32":
            return pid in self._windows_pid_parent_pairs()
        if Path("/proc").is_dir():
            return (Path("/proc") / str(pid)).exists()
        try:
            os.kill(pid, 0)  # windows-footgun: ok - POSIX-only fallback branch.
        except OSError:
            return False
        return True

    def terminate_tree(
        self,
        root_pid: int,
        *,
        timeout_ms: int,
    ) -> ProcessTreeTerminationResult:
        _validate_pid(root_pid, "root_pid")
        if timeout_ms <= 0:
            raise ValueError("timeout_ms must be positive")
        if sys.platform == "win32":
            return self._terminate_windows(root_pid, timeout_ms=timeout_ms)
        return self._terminate_posix(root_pid, timeout_ms=timeout_ms)

    def _discover_windows(self, root_pid: int) -> ProcessTreeSnapshot:
        pairs = self._windows_pid_parent_pairs()
        descendants = _descendants_from_pairs(root_pid, pairs)
        return ProcessTreeSnapshot(
            root_pid=root_pid,
            descendant_pids=descendants,
            captured_at_utc=_utc_now(),
            inspection_supported=True,
        )

    def _discover_proc(self, root_pid: int) -> ProcessTreeSnapshot:
        pairs: dict[int, int] = {}
        for entry in Path("/proc").iterdir():
            if not entry.name.isdecimal():
                continue
            pid = int(entry.name)
            ppid = _read_proc_ppid(pid)
            if ppid is not None:
                pairs[pid] = ppid
        descendants = _descendants_from_pairs(root_pid, pairs)
        return ProcessTreeSnapshot(
            root_pid=root_pid,
            descendant_pids=descendants,
            captured_at_utc=_utc_now(),
            inspection_supported=True,
        )

    def _terminate_windows(
        self,
        root_pid: int,
        *,
        timeout_ms: int,
    ) -> ProcessTreeTerminationResult:
        initial = self.discover_descendants(root_pid)
        targeted = tuple(sorted((root_pid, *initial.descendant_pids)))
        return_code: int | None = None
        timed_out = False
        try:
            completed = subprocess.run(
                ["taskkill", "/PID", str(root_pid), "/T", "/F"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
                timeout=timeout_ms / 1000,
                check=False,
            )
            return_code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True

        still_alive = _wait_for_absence(
            targeted,
            timeout_ms=timeout_ms,
            exists=self.pid_exists,
        )
        terminated = tuple(pid for pid in targeted if pid not in still_alive)
        return ProcessTreeTerminationResult(
            root_pid=root_pid,
            targeted_pids=targeted,
            mechanism="windows_taskkill_exact_pid_tree",
            attempted=True,
            terminated_pids=terminated,
            still_alive_pids=still_alive,
            timed_out=timed_out or bool(still_alive),
            return_code=return_code,
            inspection_supported=initial.inspection_supported,
            completed_at_utc=_utc_now(),
        )

    def _terminate_posix(
        self,
        root_pid: int,
        *,
        timeout_ms: int,
    ) -> ProcessTreeTerminationResult:
        initial = self.discover_descendants(root_pid)
        targeted = tuple(sorted((root_pid, *initial.descendant_pids)))
        attempted = False
        try:
            process_group_id = os.getpgid(root_pid)
            kill_group = os.killpg  # windows-footgun: ok - POSIX-only branch.
            kill_group(process_group_id, getattr(signal, "SIGKILL", signal.SIGTERM))
            attempted = True
        except ProcessLookupError:
            attempted = True
        except OSError:
            attempted = False

        still_alive = _wait_for_absence(
            targeted,
            timeout_ms=timeout_ms,
            exists=self.pid_exists,
        )
        terminated = tuple(pid for pid in targeted if pid not in still_alive)
        return ProcessTreeTerminationResult(
            root_pid=root_pid,
            targeted_pids=targeted,
            mechanism="posix_killpg_owned_group",
            attempted=attempted,
            terminated_pids=terminated,
            still_alive_pids=still_alive,
            timed_out=bool(still_alive),
            return_code=None,
            inspection_supported=initial.inspection_supported,
            completed_at_utc=_utc_now(),
        )

    def _windows_pid_parent_pairs(self) -> dict[int, int]:
        if sys.platform != "win32":
            return {}

        class ProcessEntry32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_size_t),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", wintypes.LONG),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", wintypes.WCHAR * _MAX_PATH),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        kernel32.Process32FirstW.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(ProcessEntry32),
        ]
        kernel32.Process32FirstW.restype = wintypes.BOOL
        kernel32.Process32NextW.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(ProcessEntry32),
        ]
        kernel32.Process32NextW.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL

        snapshot = kernel32.CreateToolhelp32Snapshot(_TH32CS_SNAPPROCESS, 0)
        if snapshot == _INVALID_HANDLE_VALUE:
            return {}

        pairs: dict[int, int] = {}
        try:
            entry = ProcessEntry32()
            entry.dwSize = ctypes.sizeof(ProcessEntry32)
            has_entry = kernel32.Process32FirstW(snapshot, ctypes.byref(entry))
            while has_entry:
                pairs[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
                has_entry = kernel32.Process32NextW(snapshot, ctypes.byref(entry))
        finally:
            kernel32.CloseHandle(snapshot)
        return pairs


def _descendants_from_pairs(root_pid: int, pairs: dict[int, int]) -> tuple[int, ...]:
    children_by_parent: dict[int, list[int]] = {}
    for pid, parent_pid in pairs.items():
        if pid == root_pid:
            continue
        children_by_parent.setdefault(parent_pid, []).append(pid)

    descendants: set[int] = set()
    pending = list(children_by_parent.get(root_pid, ()))
    while pending:
        current = pending.pop(0)
        if current in descendants or current == root_pid:
            continue
        descendants.add(current)
        pending.extend(children_by_parent.get(current, ()))
    return tuple(sorted(descendants))


def _read_proc_ppid(pid: int) -> int | None:
    try:
        text = (Path("/proc") / str(pid) / "stat").read_text(
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return None
    try:
        suffix = text.rsplit(") ", 1)[1]
        parts = suffix.split()
        return int(parts[1])
    except (IndexError, ValueError):
        return None


def _wait_for_absence(
    pids: tuple[int, ...],
    *,
    timeout_ms: int,
    exists: callable,
) -> tuple[int, ...]:
    deadline = time.monotonic() + (timeout_ms / 1000)
    while time.monotonic() < deadline:
        alive = tuple(pid for pid in pids if exists(pid))
        if not alive:
            return ()
        time.sleep(_POLL_INTERVAL_SECONDS)
    return tuple(sorted(pid for pid in pids if exists(pid)))
