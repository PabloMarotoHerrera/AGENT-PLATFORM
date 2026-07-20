from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.adapter import GovernedRuntimeAdapter
from hermes_cli.agent_platform.runtime_adapter.listener_discovery import (
    RuntimeListenerDiscoveryResult,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    OwnedProcessGracefulStopResult,
    OwnedProcessSnapshot,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import get_runtime_profile
from hermes_cli.agent_platform.runtime_adapter.readiness import (
    READINESS_CHECK_IDS,
    RuntimeDashboardReadyFileResult,
    RuntimeReadinessCheckResult,
    RuntimeReadinessProbeResult,
)
from hermes_cli.agent_platform.runtime_adapter.stream_capture import (
    BoundedStreamSnapshot,
)


UTC = timezone.utc


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
    return datetime(2026, 1, 1, tzinfo=UTC)


def snapshot(
    runtime_id: str,
    *,
    listener_pid: int | None = None,
    status: ra.RuntimeProcessStatus = ra.RuntimeProcessStatus.RUNNING,
) -> OwnedProcessSnapshot:
    return OwnedProcessSnapshot(
        runtime_id=runtime_id,
        process_reference=ra.RuntimeProcessRef(
            launcher_pid=4321,
            listener_pid=listener_pid,
            descendant_pids=(8765,),
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


class FakeProcessOwner:
    def __init__(self) -> None:
        self.launch_plan = None
        self.runtime_id = ""
        self.listener_pid: int | None = None
        self.released = False

    def launch(self, runtime_handle, launch_plan):
        self.runtime_id = runtime_handle.runtime_id
        self.launch_plan = launch_plan
        return snapshot(runtime_handle.runtime_id)

    def snapshot(self, runtime_id: str):
        return snapshot(runtime_id, listener_pid=self.listener_pid)

    def bind_listener_pid(self, runtime_id: str, listener_pid: int):
        self.listener_pid = listener_pid
        return snapshot(runtime_id, listener_pid=listener_pid)

    def request_graceful_stop(self, runtime_id: str, *, timeout_ms: int):
        stopped = snapshot(
            runtime_id,
            listener_pid=self.listener_pid,
            status=ra.RuntimeProcessStatus.EXITED,
        )
        return OwnedProcessGracefulStopResult(
            runtime_id=runtime_id,
            mechanism="already_exited",
            supported=True,
            exit_observed=True,
            timed_out=False,
            snapshot=stopped,
        )

    def terminate_owned_tree(self, runtime_id: str, *, timeout_ms: int):
        return snapshot(
            runtime_id,
            listener_pid=self.listener_pid,
            status=ra.RuntimeProcessStatus.EXITED,
        )

    def release(self, runtime_id: str) -> None:
        self.released = True

    def owned_runtime_ids(self):
        return () if self.released else (self.runtime_id,) if self.runtime_id else ()


class FakeReadyFileWaiter:
    def __init__(self, port: int = 65432) -> None:
        self.port = port

    def wait_for_port(self, **kwargs):
        return RuntimeDashboardReadyFileResult(
            runtime_id=kwargs["runtime_id"],
            port=self.port,
            attempt_count=1,
            observed_at_utc=utc_now(),
        )


class FakeListenerDiscovery:
    def __init__(self) -> None:
        self.checked_ports: list[int] = []

    def assert_port_free(self, *, host: str, port: int) -> None:
        assert host == "127.0.0.1"
        self.checked_ports.append(port)

    def discover_owned_listener(self, **kwargs):
        return RuntimeListenerDiscoveryResult(
            runtime_id=kwargs["runtime_id"],
            host_class="loopback_ipv4",
            port=kwargs["port"],
            listener_pid=4321,
            attempt_count=1,
            discovered_at_utc=utc_now(),
            mechanism="fixture",
        )


class FakeReadinessProbe:
    def waiting_reference(self, *, runtime_id: str, port: int, timeout_ms: int):
        return ra.RuntimeReadinessRef(
            probe_id="probe.p148.adapter",
            state=ra.RuntimeReadinessState.WAITING,
            attempt_count=0,
            deadline_at_utc=utc_now() + timedelta(milliseconds=timeout_ms),
            observed_at_utc=None,
            listener_port=port,
        )

    def wait_for_dashboard(self, **kwargs):
        assert kwargs["host"] == "127.0.0.1"
        assert kwargs["session_token"] == "session-token"
        assert Path(kwargs["files_root"]).name == "files-root"
        ref = ra.RuntimeReadinessRef(
            probe_id="probe.p148.adapter",
            state=ra.RuntimeReadinessState.READY,
            attempt_count=1,
            deadline_at_utc=utc_now() + timedelta(milliseconds=kwargs["timeout_ms"]),
            observed_at_utc=utc_now(),
            listener_port=kwargs["port"],
        )
        return RuntimeReadinessProbeResult(
            readiness_ref=ref,
            checks=readiness_checks(),
            status_keys=(
                "active_agents",
                "active_sessions",
                "auth_providers",
                "gateway_running",
                "version",
            ),
            product_id="agent-platform-hermes",
            root_status=200,
            root_asset_refs_present=True,
            root_vite_dev_marker_present=False,
            root_vite_error_overlay_marker_present=False,
            root_redirect_outside_origin=False,
            status_http_status=200,
            gateway_running=False,
            active_agent_count=0,
            active_session_count=0,
            provider_count=0,
            unauthenticated_config_status=401,
            authenticated_config_status=200,
            product_feature_state="experimental",
            extension_module_count=9,
            extension_module_order_valid=True,
            plugin_manifest_status=200,
            plugin_manifest_valid=True,
            plugin_route_conflict_count=0,
            files_root_locked=True,
            managed_files_root_matches=True,
            files_root_status=200,
            outside_files_root_status=403,
            outside_root_rejected=True,
        )


def readiness_checks() -> tuple[RuntimeReadinessCheckResult, ...]:
    evidence = {
        "dashboard.root": {"root_asset_refs_present": True},
        "dashboard.status": {
            "gateway_running": False,
            "active_agent_count": 0,
            "active_session_count": 0,
            "provider_count": 0,
        },
        "dashboard.product_config_unauthenticated": {},
        "dashboard.product_config_authenticated": {
            "product_feature_state": "experimental",
            "extension_module_count": 9,
            "extension_module_order_valid": True,
        },
        "dashboard.plugin_manifest": {
            "plugin_manifest_valid": True,
            "plugin_route_conflict_count": 0,
        },
        "dashboard.files_root": {"managed_files_root_matches": True},
        "dashboard.files_outside_root": {"outside_files_root_denied": True},
    }
    statuses = {
        "dashboard.root": 200,
        "dashboard.status": 200,
        "dashboard.product_config_unauthenticated": 401,
        "dashboard.product_config_authenticated": 200,
        "dashboard.plugin_manifest": 200,
        "dashboard.files_root": 200,
        "dashboard.files_outside_root": 403,
    }
    return tuple(
        RuntimeReadinessCheckResult(
            check_id=check_id,
            status_code=statuses[check_id],
            passed=True,
            evidence=evidence[check_id],
        )
        for check_id in READINESS_CHECK_IDS
    )


def launch_request() -> ra.RuntimeLaunchRequest:
    profile = get_runtime_profile(ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID)
    return ra.RuntimeLaunchRequest(
        schema_version=1,
        runtime_profile_id=profile.profile_ref.profile_id,
        workspace_binding=profile.default_workspace_binding,
        correlation_id="corr.p148.adapter",
        requested_by="tester.p148",
        timeout_policy=profile.timeout_policy,
        evidence_context=(),
    )


def source_environment() -> dict[str, str]:
    env = {"PATH": os.environ.get("PATH", "")}
    for key in ("SystemRoot", "WINDIR"):
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def test_adapter_composes_dashboard_launch_shutdown_and_rollback(
    tmp_path: Path,
) -> None:
    process_owner = FakeProcessOwner()
    listener_discovery = FakeListenerDiscovery()
    adapter = GovernedRuntimeAdapter(
        runtime_base_root=tmp_path,
        source_environment=source_environment(),
        python_executable=sys.executable,
        process_owner=process_owner,
        listener_discovery=listener_discovery,
        ready_file_waiter=FakeReadyFileWaiter(9130),
        readiness_probe=FakeReadinessProbe(),
        dashboard_port=9130,
        runtime_id_factory=lambda: "rt.p148.adapter",
        workspace_id_factory=lambda: "ws_0123456789abcdef",
        session_token_factory=lambda: "session-token",
        clock=DeterministicClock(),
    )

    launch = adapter.launch(launch_request())

    assert launch.outcome is ra.RuntimeOperationOutcome.READY
    assert launch.runtime_handle.lifecycle_state is ra.RuntimeLifecycleState.READY
    assert launch.workspace_reference is not None
    assert launch.readiness_reference is not None
    assert process_owner.launch_plan is not None
    assert process_owner.launch_plan.arguments == (
        "-m",
        "hermes_cli.main",
        "dashboard",
        "--host",
        "127.0.0.1",
        "--port",
        "9130",
        "--no-open",
        "--skip-build",
    )
    assert listener_discovery.checked_ports == [9130]
    assert (
        dict(process_owner.launch_plan.environment_items)[
            "HERMES_DASHBOARD_SESSION_TOKEN"
        ]
        == "session-token"
    )
    assert [event.event_type for event in launch.events] == [
        ra.RuntimeEventType.REQUEST_RECEIVED,
        ra.RuntimeEventType.PROFILE_RESOLVED,
        ra.RuntimeEventType.WORKSPACE_CREATED,
        ra.RuntimeEventType.ENVIRONMENT_SANITIZED,
        ra.RuntimeEventType.PROCESS_STARTED,
        ra.RuntimeEventType.LISTENER_DISCOVERED,
        ra.RuntimeEventType.READINESS_PROBE_STARTED,
        ra.RuntimeEventType.RUNTIME_READY,
    ]
    summary = adapter.readiness_summary(
        launch.runtime_handle.runtime_id,
        launch.runtime_handle.correlation_id,
    )
    assert summary["check_count"] == 7
    assert tuple(summary["check_ids"]) == READINESS_CHECK_IDS
    assert summary["gateway_running"] is False
    assert summary["active_agent_count"] == 0
    assert summary["active_session_count"] == 0
    assert summary["provider_count"] == 0
    assert summary["plugin_manifest_valid"] is True
    assert summary["outside_files_root_denied"] is True

    stop = adapter.shutdown(
        ra.RuntimeStopRequest(
            schema_version=1,
            runtime_id=launch.runtime_handle.runtime_id,
            correlation_id=launch.runtime_handle.correlation_id,
            requested_by="tester.p148",
            reason_code="test.stop",
        )
    )
    assert stop.outcome is ra.RuntimeOperationOutcome.STOPPED
    assert process_owner.released is True

    rollback = adapter.rollback(
        ra.RuntimeRollbackRequest(
            schema_version=1,
            runtime_id=launch.runtime_handle.runtime_id,
            correlation_id=launch.runtime_handle.correlation_id,
            requested_by="tester.p148",
            reason_code="test.rollback",
        )
    )
    assert rollback.outcome is ra.RuntimeOperationOutcome.ROLLED_BACK
    assert adapter.active_runtime_ids() == ()
    assert not tmp_path.joinpath("ws_0123456789abcdef").exists()
