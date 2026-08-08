"""Bounded dashboard readiness probes for governed runtime launches."""

from __future__ import annotations

import ipaddress
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any

from hermes_cli.agent_platform.product_config import load_product_configuration
from hermes_cli.agent_platform.runtime_adapter.contracts import RuntimeReadinessRef
from hermes_cli.agent_platform.runtime_adapter.enums import RuntimeReadinessState


_MAX_ERROR_FIELD_CHARACTERS = 160
_MAX_BODY_BYTES = 65_536
_MAX_READY_FILE_BYTES = 4096
_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})
_MIN_TIMEOUT_MS = 100
_MAX_TIMEOUT_MS = 60_000
_MIN_POLL_INTERVAL_MS = 50
_MAX_POLL_INTERVAL_MS = 5_000
READINESS_CHECK_IDS = (
    "dashboard.root",
    "dashboard.status",
    "dashboard.product_config_unauthenticated",
    "dashboard.product_config_authenticated",
    "dashboard.plugin_manifest",
    "dashboard.files_root",
    "dashboard.files_outside_root",
)
_PRODUCT_CONFIGURATION = load_product_configuration()
_PRODUCT_EXTENSION_IDS: tuple[str, ...] = _PRODUCT_CONFIGURATION.extension_modules
_PRODUCT_UI_FEATURE_STATE = _PRODUCT_CONFIGURATION.feature_flags[
    "agent_platform.product_ui"
]
_ROOT_REQUIRED_ASSET_MARKER = "/assets/"
_ROOT_FORBIDDEN_VITE_MARKERS = (
    "/@vite/client",
    "__vite",
    "vite-error-overlay",
    "react-refresh",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class RuntimeReadinessProbeError(RuntimeError):
    """Base class for bounded dashboard-readiness probe errors."""

    error_code = "runtime_readiness_probe_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        probe_id: str | None = None,
        endpoint_kind: str | None = None,
        status_code: int | None = None,
        attempt_count: int | None = None,
        validation_category: str | None = None,
        exception_class: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.probe_id = _safe_text(probe_id) if probe_id is not None else None
        self.endpoint_kind = _safe_text(endpoint_kind) if endpoint_kind else None
        self.status_code = status_code
        self.attempt_count = attempt_count
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        self.exception_class = _safe_text(exception_class) if exception_class else None
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.probe_id is not None:
            fragments.append(f"probe_id={self.probe_id}")
        if self.endpoint_kind is not None:
            fragments.append(f"endpoint_kind={self.endpoint_kind}")
        if self.status_code is not None:
            fragments.append(f"status_code={self.status_code}")
        if self.attempt_count is not None:
            fragments.append(f"attempt_count={self.attempt_count}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        if self.exception_class is not None:
            fragments.append(f"exception_class={self.exception_class}")
        super().__init__(" ".join(fragments))


class InvalidRuntimeReadinessEndpointError(RuntimeReadinessProbeError):
    error_code = "invalid_runtime_readiness_endpoint"


class RuntimeDashboardReadyFileError(RuntimeReadinessProbeError):
    error_code = "runtime_dashboard_ready_file_error"


class RuntimeDashboardReadyFileTimeoutError(RuntimeReadinessProbeError):
    error_code = "runtime_dashboard_ready_file_timeout"


class RuntimeReadinessHttpError(RuntimeReadinessProbeError):
    error_code = "runtime_readiness_http_error"


class RuntimeReadinessPayloadError(RuntimeReadinessProbeError):
    error_code = "runtime_readiness_payload_error"


class RuntimeReadinessProductConfigurationError(RuntimeReadinessProbeError):
    error_code = "runtime_readiness_product_configuration_error"


class RuntimeReadinessFilesRootError(RuntimeReadinessProbeError):
    error_code = "runtime_readiness_files_root_error"


class RuntimeReadinessTimeoutError(RuntimeReadinessProbeError):
    error_code = "runtime_readiness_timeout"

    readiness_ref: RuntimeReadinessRef

    def __init__(
        self,
        *,
        readiness_ref: RuntimeReadinessRef,
        runtime_id: str,
        probe_id: str,
        attempt_count: int,
        validation_category: str | None = None,
    ) -> None:
        self.readiness_ref = readiness_ref
        super().__init__(
            runtime_id=runtime_id,
            probe_id=probe_id,
            attempt_count=attempt_count,
            validation_category=validation_category,
        )


@dataclass(frozen=True, slots=True)
class RuntimeHttpProbeResponse:
    """One bounded HTTP response used by the readiness probe."""

    status_code: int
    payload: object | None
    text: str | None = None
    final_url: str | None = None
    headers: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))


@dataclass(frozen=True, slots=True)
class RuntimeReadinessCheckResult:
    """Bounded result for one immutable readiness check."""

    check_id: str
    status_code: int | None
    passed: bool
    evidence: Mapping[str, bool | int | str]

    def __post_init__(self) -> None:
        if self.check_id not in READINESS_CHECK_IDS:
            raise ValueError("unknown readiness check_id")
        if self.status_code is not None and not 100 <= self.status_code <= 599:
            raise ValueError("status_code must be an HTTP status")
        if not self.passed:
            raise ValueError("only passed readiness checks are retained")
        clean: dict[str, bool | int | str] = {}
        for key, value in self.evidence.items():
            if key.startswith("_"):
                raise ValueError("readiness evidence keys must be public")
            if not isinstance(value, bool | int | str):
                raise ValueError("readiness evidence must be bounded scalars")
            clean[key] = value
        object.__setattr__(self, "evidence", MappingProxyType(clean))


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeDashboardReadyFileResult:
    """Port announcement read from ``HERMES_DESKTOP_READY_FILE``."""

    runtime_id: str
    port: int
    attempt_count: int
    observed_at_utc: datetime

    def __post_init__(self) -> None:
        _validate_port(self.port)
        if self.attempt_count <= 0:
            raise ValueError("attempt_count must be positive")
        if (
            self.observed_at_utc.tzinfo is None
            or self.observed_at_utc.utcoffset() is None
        ):
            raise ValueError("observed_at_utc must be timezone-aware")

    def __repr__(self) -> str:
        return (
            "RuntimeDashboardReadyFileResult("
            f"runtime_id={self.runtime_id!r}, port={self.port!r}, "
            f"attempt_count={self.attempt_count!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeReadinessProbeResult:
    """Secret-free dashboard readiness evidence."""

    readiness_ref: RuntimeReadinessRef
    checks: tuple[RuntimeReadinessCheckResult, ...]
    status_keys: tuple[str, ...]
    product_id: str
    root_status: int
    root_asset_refs_present: bool
    root_vite_dev_marker_present: bool
    root_vite_error_overlay_marker_present: bool
    root_redirect_outside_origin: bool
    status_http_status: int
    gateway_running: bool
    active_agent_count: int
    active_session_count: int
    provider_count: int
    unauthenticated_config_status: int
    authenticated_config_status: int
    product_feature_state: str
    extension_module_count: int
    extension_module_order_valid: bool
    plugin_manifest_status: int
    plugin_manifest_valid: bool
    plugin_route_conflict_count: int
    files_root_locked: bool
    managed_files_root_matches: bool
    files_root_status: int
    outside_files_root_status: int
    outside_root_rejected: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "status_keys", tuple(sorted(self.status_keys)))
        check_ids = tuple(check.check_id for check in self.checks)
        if check_ids != READINESS_CHECK_IDS:
            raise ValueError("readiness checks must match the immutable registry")
        if self.readiness_ref.state is not RuntimeReadinessState.READY:
            raise ValueError("readiness_ref must be ready")
        if not self.product_id:
            raise ValueError("product_id must be non-empty")
        if self.root_status != 200:
            raise ValueError("dashboard root must return 200")
        if (
            not self.root_asset_refs_present
            or self.root_vite_dev_marker_present
            or self.root_vite_error_overlay_marker_present
            or self.root_redirect_outside_origin
        ):
            raise ValueError("dashboard root evidence is not production safe")
        if self.status_http_status != 200:
            raise ValueError("dashboard status must return 200")
        if self.gateway_running:
            raise ValueError("gateway_running must be false")
        if self.active_agent_count != 0 or self.active_session_count != 0:
            raise ValueError("runtime activity counts must be zero")
        if self.provider_count != 0:
            raise ValueError("provider count must be zero")
        if self.unauthenticated_config_status != 401:
            raise ValueError("unauthenticated product configuration must be denied")
        if self.authenticated_config_status != 200:
            raise ValueError("authenticated product configuration must return 200")
        if self.product_feature_state != str(_PRODUCT_UI_FEATURE_STATE):
            raise ValueError(
                "product UI feature state must match product configuration"
            )
        if self.extension_module_count != len(_PRODUCT_EXTENSION_IDS):
            raise ValueError("extension module count must match the product registry")
        if not self.extension_module_order_valid:
            raise ValueError("extension module order must be exact")
        if self.plugin_manifest_status != 200 or not self.plugin_manifest_valid:
            raise ValueError("plugin manifest must be valid")
        if self.plugin_route_conflict_count != 0:
            raise ValueError("plugin route conflicts must be zero")
        if not self.files_root_locked:
            raise ValueError("files_root_locked must be true")
        if self.files_root_status != 200 or not self.managed_files_root_matches:
            raise ValueError("files root must be managed and locked")
        if self.outside_files_root_status != 403:
            raise ValueError("outside files root probe must return 403")
        if not self.outside_root_rejected:
            raise ValueError("outside_root_rejected must be true")

    @property
    def check_count(self) -> int:
        return len(self.checks)

    @property
    def check_ids(self) -> tuple[str, ...]:
        return tuple(check.check_id for check in self.checks)

    def as_summary(self) -> dict[str, object]:
        """Return a path-, token- and body-free summary for gate persistence."""

        return {
            "check_count": self.check_count,
            "check_ids": list(self.check_ids),
            "checks": [
                {
                    "check_id": check.check_id,
                    "status_code": check.status_code,
                    "passed": check.passed,
                    "evidence": dict(check.evidence),
                }
                for check in self.checks
            ],
            "root_status": self.root_status,
            "root_asset_refs_present": self.root_asset_refs_present,
            "root_vite_dev_marker_present": self.root_vite_dev_marker_present,
            "root_vite_error_overlay_marker_present": self.root_vite_error_overlay_marker_present,
            "root_redirect_outside_origin": self.root_redirect_outside_origin,
            "status_http_status": self.status_http_status,
            "gateway_running": self.gateway_running,
            "active_agent_count": self.active_agent_count,
            "active_session_count": self.active_session_count,
            "provider_count": self.provider_count,
            "unauthenticated_config_status": self.unauthenticated_config_status,
            "authenticated_config_status": self.authenticated_config_status,
            "product_feature_state": self.product_feature_state,
            "extension_module_count": self.extension_module_count,
            "extension_module_order_valid": self.extension_module_order_valid,
            "plugin_manifest_status": self.plugin_manifest_status,
            "plugin_manifest_valid": self.plugin_manifest_valid,
            "plugin_route_conflict_count": self.plugin_route_conflict_count,
            "files_root_status": self.files_root_status,
            "managed_files_root_matches": self.managed_files_root_matches,
            "outside_files_root_status": self.outside_files_root_status,
            "outside_files_root_denied": self.outside_root_rejected,
        }

    def __repr__(self) -> str:
        return (
            "RuntimeReadinessProbeResult("
            f"probe_id={self.readiness_ref.probe_id!r}, "
            f"state={self.readiness_ref.state.value!r}, "
            f"attempt_count={self.readiness_ref.attempt_count!r}, "
            f"listener_port={self.readiness_ref.listener_port!r})"
        )


class RuntimeDashboardReadyFileWaiter:
    """Poll the dashboard ready-file sentinel with a hard deadline."""

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] | None = None,
        sleeper: Callable[[float], None] | None = None,
    ) -> None:
        self._clock = clock or _utc_now
        self._monotonic = monotonic or time.monotonic
        self._sleep = sleeper or time.sleep

    def wait_for_port(
        self,
        *,
        runtime_id: str,
        ready_file: Path,
        timeout_ms: int,
        poll_interval_ms: int,
        process_exited: Callable[[], bool] | None = None,
    ) -> RuntimeDashboardReadyFileResult:
        _validate_bounds(timeout_ms, poll_interval_ms, runtime_id=runtime_id)
        path = Path(ready_file)
        deadline = self._monotonic() + (timeout_ms / 1000)
        attempt_count = 0
        while True:
            attempt_count += 1
            if path.exists():
                return RuntimeDashboardReadyFileResult(
                    runtime_id=runtime_id,
                    port=_read_ready_file_port(
                        path, runtime_id=runtime_id, attempt_count=attempt_count
                    ),
                    attempt_count=attempt_count,
                    observed_at_utc=self._clock(),
                )
            if process_exited is not None and process_exited():
                raise RuntimeDashboardReadyFileError(
                    runtime_id=runtime_id,
                    attempt_count=attempt_count,
                    validation_category="process_exited_before_ready",
                )
            remaining = deadline - self._monotonic()
            if remaining <= 0:
                raise RuntimeDashboardReadyFileTimeoutError(
                    runtime_id=runtime_id,
                    attempt_count=attempt_count,
                    validation_category="ready_file_missing",
                )
            self._sleep(min(remaining, poll_interval_ms / 1000))


class RuntimeDashboardReadinessProbe:
    """Probe dashboard HTTP readiness through fixed local endpoints."""

    def __init__(
        self,
        *,
        transport: Callable[[str, Mapping[str, str], float], RuntimeHttpProbeResponse]
        | None = None,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] | None = None,
        sleeper: Callable[[float], None] | None = None,
    ) -> None:
        self._transport = transport or _default_transport
        self._clock = clock or _utc_now
        self._monotonic = monotonic or time.monotonic
        self._sleep = sleeper or time.sleep

    def wait_for_dashboard(
        self,
        *,
        runtime_id: str,
        host: str,
        port: int,
        session_token: str,
        files_root: Path,
        timeout_ms: int,
        poll_interval_ms: int,
    ) -> RuntimeReadinessProbeResult:
        _validate_host(host)
        _validate_port(port)
        _validate_session_token(session_token, runtime_id)
        _validate_bounds(timeout_ms, poll_interval_ms, runtime_id=runtime_id)
        files_root = Path(files_root)
        probe_id = _probe_id(runtime_id)
        started_at_utc = self._clock()
        deadline_at_utc = started_at_utc + timedelta(milliseconds=timeout_ms)
        deadline = self._monotonic() + (timeout_ms / 1000)
        attempt_count = 0
        last_error_code: str | None = None
        while True:
            attempt_count += 1
            try:
                return self._probe_once(
                    runtime_id=runtime_id,
                    probe_id=probe_id,
                    host=host,
                    port=port,
                    session_token=session_token,
                    files_root=files_root,
                    attempt_count=attempt_count,
                    deadline_at_utc=deadline_at_utc,
                )
            except RuntimeReadinessProbeError as exc:
                last_error_code = exc.error_code
                if _permanent_readiness_error(exc):
                    raise
            remaining = deadline - self._monotonic()
            if remaining <= 0:
                observed = self._clock()
                ref = RuntimeReadinessRef(
                    probe_id=probe_id,
                    state=RuntimeReadinessState.TIMED_OUT,
                    attempt_count=attempt_count,
                    deadline_at_utc=deadline_at_utc,
                    observed_at_utc=observed,
                    listener_port=port,
                )
                raise RuntimeReadinessTimeoutError(
                    runtime_id=runtime_id,
                    probe_id=probe_id,
                    attempt_count=attempt_count,
                    readiness_ref=ref,
                    validation_category=last_error_code or "deadline_expired",
                )
            self._sleep(min(remaining, poll_interval_ms / 1000))

    def waiting_reference(
        self,
        *,
        runtime_id: str,
        port: int,
        timeout_ms: int,
    ) -> RuntimeReadinessRef:
        _validate_port(port)
        if timeout_ms <= 0:
            raise InvalidRuntimeReadinessEndpointError(
                runtime_id=runtime_id,
                validation_category="timeout_not_positive",
            )
        return RuntimeReadinessRef(
            probe_id=_probe_id(runtime_id),
            state=RuntimeReadinessState.WAITING,
            attempt_count=0,
            deadline_at_utc=self._clock() + timedelta(milliseconds=timeout_ms),
            observed_at_utc=None,
            listener_port=port,
        )

    def _probe_once(
        self,
        *,
        runtime_id: str,
        probe_id: str,
        host: str,
        port: int,
        session_token: str,
        files_root: Path,
        attempt_count: int,
        deadline_at_utc: datetime,
    ) -> RuntimeReadinessProbeResult:
        base_url = _base_url(host, port)
        headers = MappingProxyType({"X-Hermes-Session-Token": session_token})
        root = self._fetch_status_and_payload(
            f"{base_url}/",
            headers=MappingProxyType({}),
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.root",
            attempt_count=attempt_count,
        )
        root_evidence = _validate_root_response(
            root,
            base_url=base_url,
            runtime_id=runtime_id,
            probe_id=probe_id,
            attempt_count=attempt_count,
        )
        status_response = self._fetch_status_and_payload(
            f"{base_url}/api/status",
            headers=MappingProxyType({}),
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
        )
        if status_response.status_code != 200:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind="dashboard.status",
                status_code=status_response.status_code,
                attempt_count=attempt_count,
            )
        status = _response_dict(
            status_response,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
        )
        status_evidence = _validate_status_payload(
            status,
            runtime_id,
            probe_id,
            attempt_count,
        )
        unauthenticated_config_status = self._fetch_status(
            f"{base_url}/api/agent-platform/product-configuration",
            headers=MappingProxyType({}),
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_unauthenticated",
            attempt_count=attempt_count,
        )
        if unauthenticated_config_status != 401:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind="dashboard.product_config_unauthenticated",
                status_code=unauthenticated_config_status,
                attempt_count=attempt_count,
            )
        product_response = self._fetch_status_and_payload(
            f"{base_url}/api/agent-platform/product-configuration",
            headers=headers,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
        )
        if product_response.status_code != 200:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind="dashboard.product_config_authenticated",
                status_code=product_response.status_code,
                attempt_count=attempt_count,
            )
        product = _response_dict(
            product_response,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
        )
        product_evidence = _validate_product_configuration(
            product,
            runtime_id,
            probe_id,
            attempt_count,
        )
        plugin_response = self._fetch_status_and_payload(
            f"{base_url}/api/dashboard/plugins",
            headers=MappingProxyType({}),
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.plugin_manifest",
            attempt_count=attempt_count,
        )
        if plugin_response.status_code != 200:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind="dashboard.plugin_manifest",
                status_code=plugin_response.status_code,
                attempt_count=attempt_count,
            )
        plugin_evidence = _validate_plugin_manifest(
            plugin_response.payload,
            runtime_id=runtime_id,
            probe_id=probe_id,
            attempt_count=attempt_count,
        )
        files_response = self._fetch_status_and_payload(
            _url_with_path(base_url, "/api/files", str(files_root)),
            headers=headers,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.files_root",
            attempt_count=attempt_count,
        )
        if files_response.status_code != 200:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind="dashboard.files_root",
                status_code=files_response.status_code,
                attempt_count=attempt_count,
            )
        files_payload = _response_dict(
            files_response,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.files_root",
            attempt_count=attempt_count,
        )
        files_evidence = _validate_files_root_payload(
            files_payload,
            files_root,
            runtime_id,
            probe_id,
            attempt_count,
        )
        outside_status = self._fetch_status(
            _url_with_path(base_url, "/api/files", str(files_root.parent)),
            headers=headers,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.files_outside_root",
            attempt_count=attempt_count,
        )
        if outside_status != 403:
            raise RuntimeReadinessFilesRootError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind="dashboard.files_outside_root",
                status_code=outside_status,
                attempt_count=attempt_count,
                validation_category="outside_root_not_rejected",
            )
        observed = self._clock()
        readiness_ref = RuntimeReadinessRef(
            probe_id=probe_id,
            state=RuntimeReadinessState.READY,
            attempt_count=attempt_count,
            deadline_at_utc=deadline_at_utc,
            observed_at_utc=min(observed, deadline_at_utc),
            listener_port=port,
        )
        checks = (
            _check_result("dashboard.root", root.status_code, **root_evidence),
            _check_result(
                "dashboard.status",
                status_response.status_code,
                **status_evidence,
            ),
            _check_result(
                "dashboard.product_config_unauthenticated",
                unauthenticated_config_status,
            ),
            _check_result(
                "dashboard.product_config_authenticated",
                product_response.status_code,
                **product_evidence,
            ),
            _check_result(
                "dashboard.plugin_manifest",
                plugin_response.status_code,
                **plugin_evidence,
            ),
            _check_result(
                "dashboard.files_root",
                files_response.status_code,
                **files_evidence,
            ),
            _check_result(
                "dashboard.files_outside_root",
                outside_status,
                outside_files_root_denied=True,
            ),
        )
        return RuntimeReadinessProbeResult(
            readiness_ref=readiness_ref,
            checks=checks,
            status_keys=tuple(status),
            product_id=str(product_evidence["product_id"]),
            root_status=root.status_code,
            root_asset_refs_present=bool(root_evidence["root_asset_refs_present"]),
            root_vite_dev_marker_present=bool(
                root_evidence["root_vite_dev_marker_present"]
            ),
            root_vite_error_overlay_marker_present=bool(
                root_evidence["root_vite_error_overlay_marker_present"]
            ),
            root_redirect_outside_origin=bool(
                root_evidence["root_redirect_outside_origin"]
            ),
            status_http_status=status_response.status_code,
            gateway_running=bool(status_evidence["gateway_running"]),
            active_agent_count=int(status_evidence["active_agent_count"]),
            active_session_count=int(status_evidence["active_session_count"]),
            provider_count=int(status_evidence["provider_count"]),
            unauthenticated_config_status=unauthenticated_config_status,
            authenticated_config_status=product_response.status_code,
            product_feature_state=str(product_evidence["product_feature_state"]),
            extension_module_count=int(product_evidence["extension_module_count"]),
            extension_module_order_valid=bool(
                product_evidence["extension_module_order_valid"]
            ),
            plugin_manifest_status=plugin_response.status_code,
            plugin_manifest_valid=bool(plugin_evidence["plugin_manifest_valid"]),
            plugin_route_conflict_count=int(
                plugin_evidence["plugin_route_conflict_count"]
            ),
            files_root_locked=True,
            managed_files_root_matches=bool(
                files_evidence["managed_files_root_matches"]
            ),
            files_root_status=files_response.status_code,
            outside_files_root_status=outside_status,
            outside_root_rejected=True,
        )

    def _fetch_json(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        runtime_id: str,
        probe_id: str,
        endpoint_kind: str,
        attempt_count: int,
    ) -> dict[str, Any]:
        response = self._fetch_status_and_payload(
            url,
            headers=headers,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=endpoint_kind,
            attempt_count=attempt_count,
        )
        if response.status_code != 200:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=endpoint_kind,
                status_code=response.status_code,
                attempt_count=attempt_count,
            )
        if not isinstance(response.payload, dict):
            raise RuntimeReadinessPayloadError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=endpoint_kind,
                attempt_count=attempt_count,
                validation_category="json_object_required",
            )
        return response.payload

    def _fetch_status(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        runtime_id: str,
        probe_id: str,
        endpoint_kind: str,
        attempt_count: int,
    ) -> int:
        return self._fetch_status_and_payload(
            url,
            headers=headers,
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=endpoint_kind,
            attempt_count=attempt_count,
        ).status_code

    def _fetch_status_and_payload(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        runtime_id: str,
        probe_id: str,
        endpoint_kind: str,
        attempt_count: int,
    ) -> RuntimeHttpProbeResponse:
        try:
            return self._transport(url, headers, 2.0)
        except RuntimeReadinessProbeError:
            raise
        except Exception as exc:
            raise RuntimeReadinessHttpError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=endpoint_kind,
                attempt_count=attempt_count,
                exception_class=exc.__class__.__name__,
            ) from None


def _default_transport(
    url: str, headers: Mapping[str, str], timeout_seconds: float
) -> RuntimeHttpProbeResponse:
    request = urllib.request.Request(url, headers=dict(headers), method="GET")
    opener = urllib.request.build_opener(_NoRedirectHandler)
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            status_code = int(response.status)
            data = response.read(_MAX_BODY_BYTES + 1)
            final_url = response.geturl()
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        status_code = int(exc.code)
        data = exc.read(_MAX_BODY_BYTES + 1)
        final_url = exc.geturl()
        response_headers = dict(exc.headers.items())
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        raise OSError(reason.__class__.__name__) from None
    if len(data) > _MAX_BODY_BYTES:
        raise ValueError("response body exceeded readiness bound")
    text = data.decode("utf-8", errors="replace") if data else ""
    payload: object | None = None
    if text:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None
    return RuntimeHttpProbeResponse(
        status_code=status_code,
        payload=payload,
        text=text,
        final_url=final_url,
        headers=response_headers,
    )


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _read_ready_file_port(path: Path, *, runtime_id: str, attempt_count: int) -> int:
    try:
        if path.stat().st_size > _MAX_READY_FILE_BYTES:
            raise RuntimeDashboardReadyFileError(
                runtime_id=runtime_id,
                attempt_count=attempt_count,
                validation_category="ready_file_too_large",
            )
        payload = json.loads(path.read_text(encoding="utf-8"))
    except RuntimeReadinessProbeError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeDashboardReadyFileError(
            runtime_id=runtime_id,
            attempt_count=attempt_count,
            validation_category="ready_file_unreadable",
            exception_class=exc.__class__.__name__,
        ) from None
    if not isinstance(payload, dict):
        raise RuntimeDashboardReadyFileError(
            runtime_id=runtime_id,
            attempt_count=attempt_count,
            validation_category="ready_file_payload_not_object",
        )
    port = payload.get("port")
    if not isinstance(port, int):
        raise RuntimeDashboardReadyFileError(
            runtime_id=runtime_id,
            attempt_count=attempt_count,
            validation_category="ready_file_port_invalid",
        )
    _validate_port(port)
    return port


def _validate_host(host: str) -> None:
    value = str(host or "").strip().lower()
    if value not in _LOOPBACK_HOSTS:
        raise InvalidRuntimeReadinessEndpointError(
            validation_category="non_loopback_host"
        )
    if value == "localhost":
        try:
            infos = socket.getaddrinfo("localhost", None, type=socket.SOCK_STREAM)
        except socket.gaierror:
            raise InvalidRuntimeReadinessEndpointError(
                validation_category="localhost_resolution_failed"
            ) from None
        addresses = {info[4][0] for info in infos}
        if not addresses or not all(
            ipaddress.ip_address(addr).is_loopback for addr in addresses
        ):
            raise InvalidRuntimeReadinessEndpointError(
                validation_category="localhost_not_loopback"
            )


def _validate_port(port: int) -> None:
    if not isinstance(port, int) or not 1 <= port <= 65_535:
        raise InvalidRuntimeReadinessEndpointError(
            validation_category="port_bounds",
        )


def _validate_session_token(session_token: str, runtime_id: str) -> None:
    if (
        not isinstance(session_token, str)
        or not session_token
        or len(session_token) > 512
        or any(ord(character) < 32 for character in session_token)
    ):
        raise InvalidRuntimeReadinessEndpointError(
            runtime_id=runtime_id,
            validation_category="session_token_invalid",
        )


def _validate_bounds(
    timeout_ms: int, poll_interval_ms: int, *, runtime_id: str
) -> None:
    if not _MIN_TIMEOUT_MS <= timeout_ms <= _MAX_TIMEOUT_MS:
        raise InvalidRuntimeReadinessEndpointError(
            runtime_id=runtime_id,
            validation_category="timeout_bounds",
        )
    if not _MIN_POLL_INTERVAL_MS <= poll_interval_ms <= _MAX_POLL_INTERVAL_MS:
        raise InvalidRuntimeReadinessEndpointError(
            runtime_id=runtime_id,
            validation_category="poll_interval_bounds",
        )
    if poll_interval_ms > timeout_ms:
        raise InvalidRuntimeReadinessEndpointError(
            runtime_id=runtime_id,
            validation_category="poll_interval_exceeds_timeout",
        )


def _response_dict(
    response: RuntimeHttpProbeResponse,
    *,
    runtime_id: str,
    probe_id: str,
    endpoint_kind: str,
    attempt_count: int,
) -> dict[str, Any]:
    if not isinstance(response.payload, dict):
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=endpoint_kind,
            attempt_count=attempt_count,
            validation_category="json_object_required",
        )
    return response.payload


def _validate_root_response(
    response: RuntimeHttpProbeResponse,
    *,
    base_url: str,
    runtime_id: str,
    probe_id: str,
    attempt_count: int,
) -> dict[str, bool]:
    check_id = "dashboard.root"
    if response.status_code != 200:
        raise RuntimeReadinessHttpError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            status_code=response.status_code,
            attempt_count=attempt_count,
        )
    text = response.text or ""
    lower = text.lower()
    asset_refs_present = _ROOT_REQUIRED_ASSET_MARKER in text and (
        'src="/assets/' in text or 'href="/assets/' in text
    )
    vite_dev_marker_present = any(
        marker in lower for marker in _ROOT_FORBIDDEN_VITE_MARKERS[:2]
    )
    vite_error_overlay_marker_present = any(
        marker in lower for marker in _ROOT_FORBIDDEN_VITE_MARKERS[2:]
    )
    redirect_outside_origin = _redirect_outside_origin(
        base_url,
        response.final_url,
        response.headers,
    )
    if not asset_refs_present:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            attempt_count=attempt_count,
            validation_category="production_asset_refs_missing",
        )
    if vite_dev_marker_present:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            attempt_count=attempt_count,
            validation_category="vite_dev_marker_present",
        )
    if vite_error_overlay_marker_present:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            attempt_count=attempt_count,
            validation_category="vite_error_overlay_marker_present",
        )
    if redirect_outside_origin:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            attempt_count=attempt_count,
            validation_category="redirect_outside_origin",
        )
    return {
        "root_asset_refs_present": asset_refs_present,
        "root_vite_dev_marker_present": vite_dev_marker_present,
        "root_vite_error_overlay_marker_present": vite_error_overlay_marker_present,
        "root_redirect_outside_origin": redirect_outside_origin,
    }


def _validate_status_payload(
    payload: Mapping[str, Any], runtime_id: str, probe_id: str, attempt_count: int
) -> dict[str, bool | int]:
    if not {
        "version",
        "gateway_running",
        "active_agents",
        "active_sessions",
        "auth_providers",
    }.issubset(payload):
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
            validation_category="status_shape_invalid",
        )
    gateway_running = payload.get("gateway_running")
    active_agents = payload.get("active_agents")
    active_sessions = payload.get("active_sessions")
    auth_providers = payload.get("auth_providers")
    if gateway_running is not False:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
            validation_category="gateway_running_not_false",
        )
    if not isinstance(active_agents, int) or active_agents != 0:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
            validation_category="agent_activity_not_null",
        )
    if not isinstance(active_sessions, int) or active_sessions != 0:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
            validation_category="session_activity_not_null",
        )
    if not isinstance(auth_providers, list) or auth_providers:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.status",
            attempt_count=attempt_count,
            validation_category="provider_activity_not_null",
        )
    return {
        "gateway_running": False,
        "active_agent_count": active_agents,
        "active_session_count": active_sessions,
        "provider_count": len(auth_providers),
    }


def _validate_product_configuration(
    payload: Mapping[str, Any], runtime_id: str, probe_id: str, attempt_count: int
) -> dict[str, bool | int | str]:
    product_id = payload.get("product_id")
    feature_flags = payload.get("feature_flags")
    modules = payload.get("extension_modules")
    if product_id != "pepper":
        raise RuntimeReadinessProductConfigurationError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
            validation_category="product_id_mismatch",
        )
    if not isinstance(feature_flags, dict) or feature_flags.get(
        "agent_platform.product_ui"
    ) != str(_PRODUCT_UI_FEATURE_STATE):
        raise RuntimeReadinessProductConfigurationError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
            validation_category="product_ui_state_mismatch",
        )
    if not isinstance(modules, list) or len(modules) != len(_PRODUCT_EXTENSION_IDS):
        raise RuntimeReadinessProductConfigurationError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
            validation_category="extension_module_count_mismatch",
        )
    extension_module_order_valid = tuple(modules) == _PRODUCT_EXTENSION_IDS
    if not extension_module_order_valid:
        raise RuntimeReadinessProductConfigurationError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
            validation_category="extension_module_order_mismatch",
        )
    serialized = json.dumps(payload, ensure_ascii=True, sort_keys=True).lower()
    if any(term in serialized for term in ("api_key", "credential", "provider")):
        raise RuntimeReadinessProductConfigurationError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.product_config_authenticated",
            attempt_count=attempt_count,
            validation_category="credential_like_term_present",
        )
    return {
        "product_id": product_id,
        "product_feature_state": str(_PRODUCT_UI_FEATURE_STATE),
        "extension_module_count": len(modules),
        "extension_module_order_valid": extension_module_order_valid,
    }


def _validate_plugin_manifest(
    payload: object,
    *,
    runtime_id: str,
    probe_id: str,
    attempt_count: int,
) -> dict[str, bool | int]:
    check_id = "dashboard.plugin_manifest"
    if not isinstance(payload, list):
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            attempt_count=attempt_count,
            validation_category="plugin_manifest_list_required",
        )
    for plugin in payload:
        if not isinstance(plugin, dict):
            raise RuntimeReadinessPayloadError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=check_id,
                attempt_count=attempt_count,
                validation_category="plugin_manifest_entry_invalid",
            )
        if not isinstance(plugin.get("name"), str) or not plugin.get("name"):
            raise RuntimeReadinessPayloadError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=check_id,
                attempt_count=attempt_count,
                validation_category="plugin_name_invalid",
            )
        if not isinstance(plugin.get("tab"), dict):
            raise RuntimeReadinessPayloadError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=check_id,
                attempt_count=attempt_count,
                validation_category="plugin_tab_invalid",
            )
        if not isinstance(plugin.get("slots", []), list):
            raise RuntimeReadinessPayloadError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=check_id,
                attempt_count=attempt_count,
                validation_category="plugin_slots_invalid",
            )
        if not isinstance(plugin.get("has_api", False), bool):
            raise RuntimeReadinessPayloadError(
                runtime_id=runtime_id,
                probe_id=probe_id,
                endpoint_kind=check_id,
                attempt_count=attempt_count,
                validation_category="plugin_has_api_invalid",
            )
    conflict_count = _plugin_route_conflict_count(payload)
    if conflict_count:
        raise RuntimeReadinessPayloadError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind=check_id,
            attempt_count=attempt_count,
            validation_category="plugin_product_route_conflict",
        )
    return {
        "plugin_manifest_valid": True,
        "plugin_route_conflict_count": conflict_count,
    }


def _validate_files_root_payload(
    payload: Mapping[str, Any],
    files_root: Path,
    runtime_id: str,
    probe_id: str,
    attempt_count: int,
) -> dict[str, bool]:
    locked_root = payload.get("locked_root")
    root = payload.get("root")
    can_change = payload.get("can_change_path")
    expected = str(files_root.resolve(strict=True))
    if locked_root != expected or root != expected or can_change is not False:
        raise RuntimeReadinessFilesRootError(
            runtime_id=runtime_id,
            probe_id=probe_id,
            endpoint_kind="dashboard.files_root",
            attempt_count=attempt_count,
            validation_category="files_root_not_locked",
        )
    return {
        "managed_files_root_matches": True,
        "default_path_equals_managed_root": True,
        "locked_root_equals_managed_root": True,
        "can_change_path": False,
    }


def _check_result(
    check_id: str,
    status_code: int | None,
    **evidence: bool | int | str,
) -> RuntimeReadinessCheckResult:
    return RuntimeReadinessCheckResult(
        check_id=check_id,
        status_code=status_code,
        passed=True,
        evidence=evidence,
    )


def _plugin_route_conflict_count(payload: list[object]) -> int:
    count = 0
    for plugin in payload:
        if not isinstance(plugin, Mapping):
            continue
        tab = plugin.get("tab")
        if not isinstance(tab, Mapping):
            continue
        for key in ("path", "override"):
            value = tab.get(key)
            if isinstance(value, str) and _conflicts_product_route(value):
                count += 1
    return count


def _conflicts_product_route(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized == "/agent-platform" or normalized.startswith("/agent-platform/")


def _redirect_outside_origin(
    base_url: str,
    final_url: str | None,
    headers: Mapping[str, str],
) -> bool:
    expected = _origin(base_url)
    observed = _origin(final_url or base_url)
    if observed != expected:
        return True
    location = next(
        (value for key, value in headers.items() if key.lower() == "location"),
        None,
    )
    if not location:
        return False
    resolved = urllib.parse.urljoin(base_url, location)
    return _origin(resolved) != expected


def _origin(url: str) -> tuple[str, str, int | None]:
    parsed = urllib.parse.urlsplit(url)
    return (parsed.scheme.lower(), (parsed.hostname or "").lower(), parsed.port)


def _permanent_readiness_error(error: RuntimeReadinessProbeError) -> bool:
    if isinstance(
        error,
        (
            RuntimeReadinessPayloadError,
            RuntimeReadinessProductConfigurationError,
            RuntimeReadinessFilesRootError,
        ),
    ):
        return True
    return isinstance(error, RuntimeReadinessHttpError) and error.status_code in {
        401,
        403,
    }


def _probe_id(runtime_id: str) -> str:
    token = "".join(
        character if character.isalnum() else "." for character in str(runtime_id)
    )
    return f"probe.{token}"[:128]


def _base_url(host: str, port: int) -> str:
    host_text = str(host).strip().lower()
    if ":" in host_text and not host_text.startswith("["):
        host_text = f"[{host_text}]"
    return f"http://{host_text}:{port}"


def _url_with_path(base_url: str, route: str, path_value: str) -> str:
    return f"{base_url}{route}?{urllib.parse.urlencode({'path': path_value})}"


__all__ = [
    "InvalidRuntimeReadinessEndpointError",
    "READINESS_CHECK_IDS",
    "RuntimeDashboardReadinessProbe",
    "RuntimeDashboardReadyFileError",
    "RuntimeDashboardReadyFileResult",
    "RuntimeDashboardReadyFileTimeoutError",
    "RuntimeDashboardReadyFileWaiter",
    "RuntimeHttpProbeResponse",
    "RuntimeReadinessCheckResult",
    "RuntimeReadinessFilesRootError",
    "RuntimeReadinessHttpError",
    "RuntimeReadinessPayloadError",
    "RuntimeReadinessProbeError",
    "RuntimeReadinessProbeResult",
    "RuntimeReadinessProductConfigurationError",
    "RuntimeReadinessTimeoutError",
]
