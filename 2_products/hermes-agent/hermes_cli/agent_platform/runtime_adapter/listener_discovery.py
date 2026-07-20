"""Bounded listener discovery for governed runtime adapter processes."""

from __future__ import annotations

import ctypes
import ipaddress
import socket
import struct
import sys
import time
from collections.abc import Callable, Iterable
from ctypes import wintypes
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    HermesProcessOwner,
    RuntimeProcessOwnerError,
)


_LISTEN_STATE = 2
_TCP_TABLE_OWNER_PID_LISTENER = 3
_AF_INET = 2
_AF_INET6 = 23
_ERROR_INSUFFICIENT_BUFFER = 122
_MIN_TIMEOUT_MS = 100
_MAX_TIMEOUT_MS = 30_000
_MIN_POLL_INTERVAL_MS = 50
_MAX_POLL_INTERVAL_MS = 1_000
_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})
_LOOPBACK_ADDRESSES = frozenset({"127.0.0.1", "::1"})
_WILDCARD_ADDRESSES = frozenset({"0.0.0.0", "::"})


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[:160]


class RuntimeListenerDiscoveryError(RuntimeError):
    """Base class for bounded listener-discovery errors."""

    error_code = "runtime_listener_discovery_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        port: int | None = None,
        attempt_count: int | None = None,
        mechanism: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.port = port
        self.attempt_count = attempt_count
        self.mechanism = _safe_text(mechanism) if mechanism else None
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.port is not None:
            fragments.append(f"port={self.port}")
        if self.attempt_count is not None:
            fragments.append(f"attempt_count={self.attempt_count}")
        if self.mechanism is not None:
            fragments.append(f"mechanism={self.mechanism}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        super().__init__(" ".join(fragments))


class InvalidRuntimeListenerHostError(RuntimeListenerDiscoveryError):
    error_code = "invalid_runtime_listener_host"


class InvalidRuntimeListenerPortError(RuntimeListenerDiscoveryError):
    error_code = "invalid_runtime_listener_port"


class RuntimeListenerPortOccupiedError(RuntimeListenerDiscoveryError):
    error_code = "runtime_listener_port_occupied"


class RuntimeListenerDiscoveryTimeoutError(RuntimeListenerDiscoveryError):
    error_code = "runtime_listener_discovery_timeout"


class RuntimeListenerOwnershipError(RuntimeListenerDiscoveryError):
    error_code = "runtime_listener_ownership_error"


class RuntimeListenerAmbiguityError(RuntimeListenerDiscoveryError):
    error_code = "runtime_listener_ambiguity_error"


class RuntimeListenerInspectionUnsupportedError(RuntimeListenerDiscoveryError):
    error_code = "runtime_listener_inspection_unsupported"


@dataclass(frozen=True, slots=True)
class RuntimeTcpListenerEndpoint:
    """One bounded listening TCP endpoint."""

    local_address: str
    port: int
    owning_pid: int
    mechanism: str


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeListenerDiscoveryResult:
    """Secret-free owned-listener discovery result."""

    runtime_id: str
    host_class: str
    port: int
    listener_pid: int
    attempt_count: int
    discovered_at_utc: datetime
    mechanism: str

    def __post_init__(self) -> None:
        _validate_port(self.port)
        if self.listener_pid <= 0:
            raise ValueError("listener_pid must be positive")
        if self.attempt_count <= 0:
            raise ValueError("attempt_count must be positive")
        if (
            self.discovered_at_utc.tzinfo is None
            or self.discovered_at_utc.utcoffset() is None
        ):
            raise ValueError("discovered_at_utc must be timezone-aware")

    def __repr__(self) -> str:
        return (
            "RuntimeListenerDiscoveryResult("
            f"runtime_id={self.runtime_id!r}, host_class={self.host_class!r}, "
            f"port={self.port!r}, attempt_count={self.attempt_count!r}, "
            f"mechanism={self.mechanism!r})"
        )


class RuntimeListenerDiscovery:
    """Discover exact owned listener PIDs without shelling out."""

    def __init__(
        self,
        *,
        endpoint_provider: Callable[[], Iterable[RuntimeTcpListenerEndpoint]]
        | None = None,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] | None = None,
        sleeper: Callable[[float], None] | None = None,
    ) -> None:
        self._endpoint_provider = endpoint_provider or _system_tcp_listeners
        self._clock = clock or _utc_now
        self._monotonic = monotonic or time.monotonic
        self._sleep = sleeper or time.sleep

    def assert_port_free(self, *, host: str, port: int) -> None:
        host_class = _validate_host(host)
        _validate_port(port)
        listeners = tuple(self._matching_endpoints(host_class, port))
        if listeners:
            raise RuntimeListenerPortOccupiedError(
                port=port,
                attempt_count=1,
                mechanism=_mechanism_for(listeners),
            )

    def discover_owned_listener(
        self,
        *,
        process_owner: HermesProcessOwner,
        runtime_id: str,
        host: str,
        port: int,
        timeout_ms: int,
        poll_interval_ms: int,
    ) -> RuntimeListenerDiscoveryResult:
        host_class = _validate_host(host)
        _validate_port(port)
        _validate_bounds(timeout_ms, poll_interval_ms, runtime_id=runtime_id, port=port)

        deadline = self._monotonic() + (timeout_ms / 1000)
        attempt_count = 0
        last_mechanism = "unknown"
        while True:
            attempt_count += 1
            endpoints = tuple(self._matching_endpoints(host_class, port))
            if endpoints:
                return self._resolve_owned_endpoint(
                    endpoints=endpoints,
                    process_owner=process_owner,
                    runtime_id=runtime_id,
                    host_class=host_class,
                    port=port,
                    attempt_count=attempt_count,
                )
            if endpoints == ():
                last_mechanism = _provider_mechanism(self._endpoint_provider)
            remaining = deadline - self._monotonic()
            if remaining <= 0:
                raise RuntimeListenerDiscoveryTimeoutError(
                    runtime_id=runtime_id,
                    port=port,
                    attempt_count=attempt_count,
                    mechanism=last_mechanism,
                )
            self._sleep(min(remaining, poll_interval_ms / 1000))

    def _matching_endpoints(
        self, host_class: str, port: int
    ) -> tuple[RuntimeTcpListenerEndpoint, ...]:
        try:
            endpoints = tuple(self._endpoint_provider())
        except RuntimeListenerInspectionUnsupportedError:
            raise
        except Exception as exc:
            raise RuntimeListenerInspectionUnsupportedError(
                port=port,
                mechanism=exc.__class__.__name__,
            ) from None
        return tuple(
            endpoint
            for endpoint in endpoints
            if endpoint.port == port and _endpoint_matches_host(endpoint, host_class)
        )

    def _resolve_owned_endpoint(
        self,
        *,
        endpoints: tuple[RuntimeTcpListenerEndpoint, ...],
        process_owner: HermesProcessOwner,
        runtime_id: str,
        host_class: str,
        port: int,
        attempt_count: int,
    ) -> RuntimeListenerDiscoveryResult:
        if len({endpoint.owning_pid for endpoint in endpoints}) > 1:
            raise RuntimeListenerAmbiguityError(
                runtime_id=runtime_id,
                port=port,
                attempt_count=attempt_count,
                mechanism=_mechanism_for(endpoints),
            )
        try:
            snapshot = process_owner.snapshot(runtime_id)
        except RuntimeProcessOwnerError as exc:
            raise RuntimeListenerOwnershipError(
                runtime_id=runtime_id,
                port=port,
                attempt_count=attempt_count,
                mechanism=exc.error_code,
            ) from None
        owned_pids = {
            pid
            for pid in (
                snapshot.process_reference.launcher_pid,
                *snapshot.process_reference.descendant_pids,
            )
            if pid is not None
        }
        owned = tuple(
            endpoint for endpoint in endpoints if endpoint.owning_pid in owned_pids
        )
        if not owned:
            raise RuntimeListenerOwnershipError(
                runtime_id=runtime_id,
                port=port,
                attempt_count=attempt_count,
                mechanism=_mechanism_for(endpoints),
            )
        endpoint = owned[0]
        return RuntimeListenerDiscoveryResult(
            runtime_id=runtime_id,
            host_class=host_class,
            port=port,
            listener_pid=endpoint.owning_pid,
            attempt_count=attempt_count,
            discovered_at_utc=self._clock(),
            mechanism=endpoint.mechanism,
        )


def _validate_host(host: str) -> str:
    value = str(host or "").strip().lower()
    if value not in _LOOPBACK_HOSTS:
        raise InvalidRuntimeListenerHostError(validation_category="non_loopback_host")
    if value == "localhost":
        try:
            infos = socket.getaddrinfo("localhost", None, type=socket.SOCK_STREAM)
        except socket.gaierror:
            raise InvalidRuntimeListenerHostError(
                validation_category="localhost_resolution_failed"
            ) from None
        addresses = {info[4][0] for info in infos}
        if not addresses or not all(
            ipaddress.ip_address(addr).is_loopback for addr in addresses
        ):
            raise InvalidRuntimeListenerHostError(
                validation_category="localhost_not_loopback"
            )
        return "loopback_name"
    return "loopback_ipv6" if value == "::1" else "loopback_ipv4"


def _validate_port(port: int) -> None:
    if not isinstance(port, int) or not 1 <= port <= 65_535:
        raise InvalidRuntimeListenerPortError(
            port=port, validation_category="port_bounds"
        )


def _validate_bounds(
    timeout_ms: int,
    poll_interval_ms: int,
    *,
    runtime_id: str,
    port: int,
) -> None:
    if not _MIN_TIMEOUT_MS <= timeout_ms <= _MAX_TIMEOUT_MS:
        raise RuntimeListenerDiscoveryTimeoutError(
            runtime_id=runtime_id,
            port=port,
            validation_category="timeout_bounds",
        )
    if not _MIN_POLL_INTERVAL_MS <= poll_interval_ms <= _MAX_POLL_INTERVAL_MS:
        raise RuntimeListenerDiscoveryTimeoutError(
            runtime_id=runtime_id,
            port=port,
            validation_category="poll_interval_bounds",
        )
    if poll_interval_ms > timeout_ms:
        raise RuntimeListenerDiscoveryTimeoutError(
            runtime_id=runtime_id,
            port=port,
            validation_category="poll_interval_exceeds_timeout",
        )


def _endpoint_matches_host(
    endpoint: RuntimeTcpListenerEndpoint, host_class: str
) -> bool:
    address = endpoint.local_address.lower()
    if address in _WILDCARD_ADDRESSES:
        return True
    if host_class == "loopback_ipv4":
        return address == "127.0.0.1"
    if host_class == "loopback_ipv6":
        return address == "::1"
    return address in _LOOPBACK_ADDRESSES


def _provider_mechanism(provider: Callable[[], object]) -> str:
    return getattr(provider, "__name__", provider.__class__.__name__)


def _mechanism_for(endpoints: tuple[RuntimeTcpListenerEndpoint, ...]) -> str:
    mechanisms = tuple(sorted({endpoint.mechanism for endpoint in endpoints}))
    return mechanisms[0] if len(mechanisms) == 1 else "multiple"


def _system_tcp_listeners() -> tuple[RuntimeTcpListenerEndpoint, ...]:
    if sys.platform == "win32":
        return _windows_tcp_listeners()
    proc = Path("/proc")
    if proc.is_dir():
        return _proc_tcp_listeners(proc)
    raise RuntimeListenerInspectionUnsupportedError(mechanism="platform_unsupported")


class _MibTcpRowOwnerPid(ctypes.Structure):
    _fields_ = [
        ("dwState", wintypes.DWORD),
        ("dwLocalAddr", wintypes.DWORD),
        ("dwLocalPort", wintypes.DWORD),
        ("dwRemoteAddr", wintypes.DWORD),
        ("dwRemotePort", wintypes.DWORD),
        ("dwOwningPid", wintypes.DWORD),
    ]


class _MibTcp6RowOwnerPid(ctypes.Structure):
    _fields_ = [
        ("ucLocalAddr", ctypes.c_ubyte * 16),
        ("dwLocalScopeId", wintypes.DWORD),
        ("dwLocalPort", wintypes.DWORD),
        ("ucRemoteAddr", ctypes.c_ubyte * 16),
        ("dwRemoteScopeId", wintypes.DWORD),
        ("dwRemotePort", wintypes.DWORD),
        ("dwState", wintypes.DWORD),
        ("dwOwningPid", wintypes.DWORD),
    ]


def _windows_tcp_listeners() -> tuple[RuntimeTcpListenerEndpoint, ...]:
    if sys.platform != "win32":
        raise RuntimeListenerInspectionUnsupportedError(mechanism="windows_only")
    endpoints: list[RuntimeTcpListenerEndpoint] = []
    endpoints.extend(_windows_tcp4_listeners())
    endpoints.extend(_windows_tcp6_listeners())
    return tuple(endpoints)


def _windows_tcp4_listeners() -> tuple[RuntimeTcpListenerEndpoint, ...]:
    rows = _windows_table_rows(_AF_INET, _MibTcpRowOwnerPid)
    endpoints = []
    for row in rows:
        if int(row.dwState) != _LISTEN_STATE:
            continue
        endpoints.append(
            RuntimeTcpListenerEndpoint(
                local_address=socket.inet_ntoa(struct.pack("<L", int(row.dwLocalAddr))),
                port=_decode_windows_port(int(row.dwLocalPort)),
                owning_pid=int(row.dwOwningPid),
                mechanism="windows_get_extended_tcp_table",
            )
        )
    return tuple(endpoints)


def _windows_tcp6_listeners() -> tuple[RuntimeTcpListenerEndpoint, ...]:
    rows = _windows_table_rows(_AF_INET6, _MibTcp6RowOwnerPid)
    endpoints = []
    for row in rows:
        if int(row.dwState) != _LISTEN_STATE:
            continue
        endpoints.append(
            RuntimeTcpListenerEndpoint(
                local_address=socket.inet_ntop(socket.AF_INET6, bytes(row.ucLocalAddr)),
                port=_decode_windows_port(int(row.dwLocalPort)),
                owning_pid=int(row.dwOwningPid),
                mechanism="windows_get_extended_tcp_table",
            )
        )
    return tuple(endpoints)


def _windows_table_rows(address_family: int, row_type):
    iphlpapi = ctypes.WinDLL("iphlpapi")
    size = wintypes.ULONG(0)
    result = iphlpapi.GetExtendedTcpTable(
        None,
        ctypes.byref(size),
        False,
        address_family,
        _TCP_TABLE_OWNER_PID_LISTENER,
        0,
    )
    if result != _ERROR_INSUFFICIENT_BUFFER:
        return ()
    buffer = ctypes.create_string_buffer(size.value)
    result = iphlpapi.GetExtendedTcpTable(
        buffer,
        ctypes.byref(size),
        False,
        address_family,
        _TCP_TABLE_OWNER_PID_LISTENER,
        0,
    )
    if result != 0:
        raise RuntimeListenerInspectionUnsupportedError(
            mechanism="windows_get_extended_tcp_table"
        )
    count = ctypes.cast(buffer, ctypes.POINTER(wintypes.DWORD)).contents.value
    row_array = row_type * count
    offset = ctypes.sizeof(wintypes.DWORD)
    rows = row_array.from_address(ctypes.addressof(buffer) + offset)
    return tuple(row_type.from_buffer_copy(bytes(row)) for row in rows)


def _decode_windows_port(value: int) -> int:
    return socket.ntohs(value & 0xFFFF)


def _proc_tcp_listeners(proc_root: Path) -> tuple[RuntimeTcpListenerEndpoint, ...]:
    inode_to_pids = _proc_socket_inode_pids(proc_root)
    endpoints: list[RuntimeTcpListenerEndpoint] = []
    for path, family in (
        (proc_root / "net" / "tcp", socket.AF_INET),
        (proc_root / "net" / "tcp6", socket.AF_INET6),
    ):
        endpoints.extend(_parse_proc_table(path, family, inode_to_pids))
    return tuple(endpoints)


def _parse_proc_table(
    table_path: Path,
    family: int,
    inode_to_pids: dict[str, tuple[int, ...]],
) -> tuple[RuntimeTcpListenerEndpoint, ...]:
    try:
        lines = table_path.read_text(encoding="ascii").splitlines()[1:]
    except OSError:
        return ()
    endpoints: list[RuntimeTcpListenerEndpoint] = []
    for line in lines:
        fields = line.split()
        if len(fields) < 10 or fields[3] != "0A":
            continue
        address_hex, port_hex = fields[1].split(":", 1)
        inode = fields[9]
        pids = inode_to_pids.get(inode, ())
        if not pids:
            continue
        address = _decode_proc_address(address_hex, family)
        port = int(port_hex, 16)
        for pid in pids:
            endpoints.append(
                RuntimeTcpListenerEndpoint(
                    local_address=address,
                    port=port,
                    owning_pid=pid,
                    mechanism="proc_net_tcp_inode",
                )
            )
    return tuple(endpoints)


def _decode_proc_address(address_hex: str, family: int) -> str:
    raw = bytes.fromhex(address_hex)
    if family == socket.AF_INET:
        return socket.inet_ntop(family, raw[::-1])
    chunks = [raw[index : index + 4][::-1] for index in range(0, 16, 4)]
    return socket.inet_ntop(family, b"".join(chunks))


def _proc_socket_inode_pids(proc_root: Path) -> dict[str, tuple[int, ...]]:
    inode_to_pids: dict[str, set[int]] = {}
    for entry in proc_root.iterdir():
        if not entry.name.isdecimal():
            continue
        pid = int(entry.name)
        fd_dir = entry / "fd"
        try:
            fd_entries = tuple(fd_dir.iterdir())
        except OSError:
            continue
        for fd in fd_entries:
            try:
                target = fd.readlink()
            except OSError:
                continue
            text = str(target)
            if text.startswith("socket:[") and text.endswith("]"):
                inode = text[8:-1]
                inode_to_pids.setdefault(inode, set()).add(pid)
    return {inode: tuple(sorted(pids)) for inode, pids in inode_to_pids.items() if pids}
