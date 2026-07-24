from __future__ import annotations

import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.readiness import (
    READINESS_CHECK_IDS,
    RuntimeDashboardReadinessProbe,
    RuntimeDashboardReadyFileError,
    RuntimeDashboardReadyFileWaiter,
    RuntimeHttpProbeResponse,
    RuntimeReadinessFilesRootError,
    RuntimeReadinessPayloadError,
)


UTC = timezone.utc
PRODUCT_EXTENSION_IDS: tuple[str, ...] = ()


def utc_now() -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC)


def product_payload() -> dict[str, object]:
    return {
        "schema_version": 1,
        "product_id": "pepper",
        "feature_flags": {"agent_platform.product_ui": "disabled"},
        "extension_modules": list(PRODUCT_EXTENSION_IDS),
    }


def status_payload() -> dict[str, object]:
    return {
        "version": "x",
        "gateway_running": False,
        "active_agents": 0,
        "active_sessions": 0,
        "auth_providers": [],
    }


def root_response() -> RuntimeHttpProbeResponse:
    return RuntimeHttpProbeResponse(
        200,
        None,
        text='<html><script type="module" src="/assets/index.js"></script></html>',
        final_url="http://127.0.0.1:8765/",
        headers={},
    )


def plugin_payload() -> list[dict[str, object]]:
    return [
        {
            "name": "kanban",
            "label": "Kanban",
            "tab": {"path": "/kanban", "position": "end"},
            "slots": [],
            "has_api": False,
        }
    ]


def test_ready_file_waiter_accepts_only_bounded_integer_port(tmp_path: Path) -> None:
    ready_file = tmp_path / "ready.json"
    ready_file.write_text(json.dumps({"port": 54321}), encoding="utf-8")
    waiter = RuntimeDashboardReadyFileWaiter(clock=utc_now)

    result = waiter.wait_for_port(
        runtime_id="rt.p148.ready_file",
        ready_file=ready_file,
        timeout_ms=100,
        poll_interval_ms=50,
    )

    assert result.port == 54321
    assert result.attempt_count == 1

    ready_file.write_text(json.dumps({"port": "54321"}), encoding="utf-8")
    with pytest.raises(RuntimeDashboardReadyFileError):
        waiter.wait_for_port(
            runtime_id="rt.p148.ready_file",
            ready_file=ready_file,
            timeout_ms=100,
            poll_interval_ms=50,
        )


def test_readiness_probe_validates_status_product_and_locked_files_root(
    tmp_path: Path,
) -> None:
    files_root = tmp_path / "files-root"
    files_root.mkdir()
    calls: list[tuple[str, dict[str, str]]] = []

    def transport(
        url: str, headers, _timeout_seconds: float
    ) -> RuntimeHttpProbeResponse:
        calls.append((url, dict(headers)))
        parsed = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/":
            return root_response()
        if parsed.path == "/api/status":
            return RuntimeHttpProbeResponse(200, status_payload())
        if parsed.path == "/api/agent-platform/product-configuration":
            if "X-Hermes-Session-Token" not in headers:
                return RuntimeHttpProbeResponse(401, {"detail": "auth required"})
            return RuntimeHttpProbeResponse(200, product_payload())
        if parsed.path == "/api/dashboard/plugins":
            return RuntimeHttpProbeResponse(200, plugin_payload())
        if parsed.path == "/api/files":
            requested = query.get("path", [""])[0]
            expected = str(files_root.resolve(strict=True))
            if requested == expected:
                return RuntimeHttpProbeResponse(
                    200,
                    {
                        "root": expected,
                        "locked_root": expected,
                        "can_change_path": False,
                    },
                )
            return RuntimeHttpProbeResponse(403, {"detail": "outside root"})
        return RuntimeHttpProbeResponse(404, {})

    probe = RuntimeDashboardReadinessProbe(transport=transport, clock=utc_now)

    result = probe.wait_for_dashboard(
        runtime_id="rt.p148.readiness",
        host="127.0.0.1",
        port=8765,
        session_token="session-token",
        files_root=files_root,
        timeout_ms=100,
        poll_interval_ms=50,
    )

    assert result.readiness_ref.state is ra.RuntimeReadinessState.READY
    assert result.check_count == 7
    assert result.check_ids == READINESS_CHECK_IDS
    assert result.product_id == "pepper"
    assert result.gateway_running is False
    assert result.active_agent_count == 0
    assert result.active_session_count == 0
    assert result.provider_count == 0
    assert result.unauthenticated_config_status == 401
    assert result.authenticated_config_status == 200
    assert result.product_feature_state == "disabled"
    assert result.extension_module_count == 0
    assert result.extension_module_order_valid is True
    assert result.plugin_manifest_valid is True
    assert result.plugin_route_conflict_count == 0
    assert result.managed_files_root_matches is True
    assert result.outside_root_rejected is True
    assert result.status_keys == tuple(sorted(status_payload()))
    assert calls[0][1] == {}
    assert [urllib.parse.urlsplit(url).path for url, _headers in calls] == [
        "/",
        "/api/status",
        "/api/agent-platform/product-configuration",
        "/api/agent-platform/product-configuration",
        "/api/dashboard/plugins",
        "/api/files",
        "/api/files",
    ]
    assert [headers for _url, headers in calls] == [
        {},
        {},
        {},
        {"X-Hermes-Session-Token": "session-token"},
        {},
        {"X-Hermes-Session-Token": "session-token"},
        {"X-Hermes-Session-Token": "session-token"},
    ]
    summary = result.as_summary()
    assert summary["check_count"] == 7
    assert summary["outside_files_root_denied"] is True
    assert "session-token" not in json.dumps(summary)
    assert str(files_root) not in json.dumps(summary)


def test_readiness_probe_fails_when_files_root_can_escape(tmp_path: Path) -> None:
    files_root = tmp_path / "files-root"
    files_root.mkdir()

    def transport(
        url: str, _headers, _timeout_seconds: float
    ) -> RuntimeHttpProbeResponse:
        path = urllib.parse.urlsplit(url).path
        if path == "/":
            return root_response()
        if path == "/api/status":
            return RuntimeHttpProbeResponse(200, status_payload())
        if path == "/api/agent-platform/product-configuration":
            if "X-Hermes-Session-Token" not in _headers:
                return RuntimeHttpProbeResponse(401, {"detail": "auth required"})
            return RuntimeHttpProbeResponse(200, product_payload())
        if path == "/api/dashboard/plugins":
            return RuntimeHttpProbeResponse(200, plugin_payload())
        return RuntimeHttpProbeResponse(200, {"root": "wrong", "locked_root": "wrong"})

    probe = RuntimeDashboardReadinessProbe(transport=transport, clock=utc_now)

    with pytest.raises(RuntimeReadinessFilesRootError):
        probe.wait_for_dashboard(
            runtime_id="rt.p148.files_escape",
            host="127.0.0.1",
            port=8765,
            session_token="session-token",
            files_root=files_root,
            timeout_ms=100,
            poll_interval_ms=50,
        )


def test_readiness_probe_fails_when_status_cannot_prove_zero_activity(
    tmp_path: Path,
) -> None:
    files_root = tmp_path / "files-root"
    files_root.mkdir()

    def transport(
        url: str, _headers, _timeout_seconds: float
    ) -> RuntimeHttpProbeResponse:
        path = urllib.parse.urlsplit(url).path
        if path == "/":
            return root_response()
        if path == "/api/status":
            payload = status_payload()
            payload["gateway_running"] = True
            return RuntimeHttpProbeResponse(200, payload)
        return RuntimeHttpProbeResponse(404, {})

    probe = RuntimeDashboardReadinessProbe(transport=transport, clock=utc_now)

    with pytest.raises(RuntimeReadinessPayloadError) as exc_info:
        probe.wait_for_dashboard(
            runtime_id="rt.p148.status_busy",
            host="127.0.0.1",
            port=8765,
            session_token="session-token",
            files_root=files_root,
            timeout_ms=100,
            poll_interval_ms=50,
        )
    assert exc_info.value.endpoint_kind == "dashboard.status"
    assert exc_info.value.validation_category == "gateway_running_not_false"


def test_readiness_probe_fails_on_plugin_agent_platform_route_conflict(
    tmp_path: Path,
) -> None:
    files_root = tmp_path / "files-root"
    files_root.mkdir()

    def transport(
        url: str, headers, _timeout_seconds: float
    ) -> RuntimeHttpProbeResponse:
        parsed = urllib.parse.urlsplit(url)
        if parsed.path == "/":
            return root_response()
        if parsed.path == "/api/status":
            return RuntimeHttpProbeResponse(200, status_payload())
        if parsed.path == "/api/agent-platform/product-configuration":
            if "X-Hermes-Session-Token" not in headers:
                return RuntimeHttpProbeResponse(401, {"detail": "auth required"})
            return RuntimeHttpProbeResponse(200, product_payload())
        if parsed.path == "/api/dashboard/plugins":
            payload = plugin_payload()
            payload[0]["tab"] = {"path": "/agent-platform/override"}
            return RuntimeHttpProbeResponse(200, payload)
        return RuntimeHttpProbeResponse(404, {})

    probe = RuntimeDashboardReadinessProbe(transport=transport, clock=utc_now)

    with pytest.raises(RuntimeReadinessPayloadError) as exc_info:
        probe.wait_for_dashboard(
            runtime_id="rt.p148.plugin_conflict",
            host="127.0.0.1",
            port=8765,
            session_token="session-token",
            files_root=files_root,
            timeout_ms=100,
            poll_interval_ms=50,
        )
    assert exc_info.value.endpoint_kind == "dashboard.plugin_manifest"
    assert exc_info.value.validation_category == "plugin_product_route_conflict"
