from __future__ import annotations

from datetime import datetime, timezone

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.listener_discovery import (
    RuntimeListenerAmbiguityError,
    RuntimeListenerDiscovery,
    RuntimeListenerPortOccupiedError,
    RuntimeTcpListenerEndpoint,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import OwnedProcessSnapshot
from hermes_cli.agent_platform.runtime_adapter.stream_capture import (
    BoundedStreamSnapshot,
)


UTC = timezone.utc


def utc_now() -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC)


def snapshot(runtime_id: str, *, launcher_pid: int = 1111) -> OwnedProcessSnapshot:
    return OwnedProcessSnapshot(
        runtime_id=runtime_id,
        process_reference=ra.RuntimeProcessRef(
            launcher_pid=launcher_pid,
            listener_pid=None,
            descendant_pids=(2222,),
            process_status=ra.RuntimeProcessStatus.RUNNING,
            started_at_utc=utc_now(),
            exited_at_utc=None,
            exit_code=None,
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


class FakeProcessOwner:
    def snapshot(self, runtime_id: str) -> OwnedProcessSnapshot:
        return snapshot(runtime_id)


def endpoint(
    port: int, pid: int, address: str = "127.0.0.1"
) -> RuntimeTcpListenerEndpoint:
    return RuntimeTcpListenerEndpoint(
        local_address=address,
        port=port,
        owning_pid=pid,
        mechanism="fixture",
    )


def test_discovers_exact_owned_loopback_listener_without_shelling_out() -> None:
    discovery = RuntimeListenerDiscovery(
        endpoint_provider=lambda: (endpoint(8765, 2222),),
        monotonic=lambda: 0.0,
        sleeper=lambda _seconds: None,
        clock=utc_now,
    )

    result = discovery.discover_owned_listener(
        process_owner=FakeProcessOwner(),
        runtime_id="rt.p148.listener",
        host="127.0.0.1",
        port=8765,
        timeout_ms=100,
        poll_interval_ms=50,
    )

    assert result.listener_pid == 2222
    assert result.host_class == "loopback_ipv4"
    assert result.mechanism == "fixture"


def test_same_owned_pid_with_multiple_matching_rows_is_not_ambiguous() -> None:
    discovery = RuntimeListenerDiscovery(
        endpoint_provider=lambda: (
            endpoint(8765, 2222),
            endpoint(8765, 2222, address="0.0.0.0"),
        ),
        monotonic=lambda: 0.0,
        sleeper=lambda _seconds: None,
        clock=utc_now,
    )

    result = discovery.discover_owned_listener(
        process_owner=FakeProcessOwner(),
        runtime_id="rt.p148.listener.duplicate_rows",
        host="127.0.0.1",
        port=8765,
        timeout_ms=100,
        poll_interval_ms=50,
    )

    assert result.listener_pid == 2222


def test_rejects_occupied_and_ambiguous_listener_ports() -> None:
    occupied = RuntimeListenerDiscovery(
        endpoint_provider=lambda: (endpoint(8765, 9999),)
    )

    with pytest.raises(RuntimeListenerPortOccupiedError):
        occupied.assert_port_free(host="127.0.0.1", port=8765)

    ambiguous = RuntimeListenerDiscovery(
        endpoint_provider=lambda: (endpoint(8765, 2222), endpoint(8765, 3333))
    )
    with pytest.raises(RuntimeListenerAmbiguityError):
        ambiguous.discover_owned_listener(
            process_owner=FakeProcessOwner(),
            runtime_id="rt.p148.ambiguous",
            host="localhost",
            port=8765,
            timeout_ms=100,
            poll_interval_ms=50,
        )
