"""Pepper governed worker credential binding and runtime resolution.

This module carries only Agent Platform worker credential authority. It passes
secret-free binding metadata to Kanban children and resolves the actual Codex
OAuth material in-process from the governed store.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    ProviderCredentialDeliveryLease,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
    OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
    ProviderWorkerResolutionRequest,
)


PEPPER_GOVERNED_WORKER_ENV = "HERMES_AGENT_PLATFORM_GOVERNED_WORKER"
PEPPER_GOVERNED_WORKER_MODE = "pepper-kanban-worker"
PEPPER_GOVERNED_WORKER_SOURCE = "pepper-governed-openai-codex-oauth"
PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE = "worker_credential_authority_mismatch"
PEPPER_GOVERNED_WORKER_BLOCKER_CODE = "WORKER_CREDENTIAL_AUTHORITY_MISMATCH"
PEPPER_GOVERNED_WORKER_READY_MARKER = (
    "PEPPER-WORKER-GOVERNED-CREDENTIAL-PROPAGATION-READY-FOR-HUMAN-SMOKE"
)

_PROJECT_ID = "PEPPER"
_TICKET_ID = "P18.9.0"
_EXECUTOR_PROFILE = "pepper-architecture-product"
_PROVIDER = "openai-codex"
_MODEL = "gpt-5.5"
_API_MODE = "codex_responses"
_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_UNSAFE_IDENTIFIER_CHARS = re.compile(r"[^A-Za-z0-9._:-]+")
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


class PepperGovernedWorkerCredentialError(RuntimeError):
    """Secret-free governed worker credential resolution failure."""

    error_code = PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE

    def __init__(self, validation_category: str, detail: object | None = None) -> None:
        self.validation_category = _safe_text(validation_category, limit=120)
        self.detail = _safe_text(detail, limit=200) if detail is not None else None
        message = (
            f"{PEPPER_GOVERNED_WORKER_BLOCKER_CODE}: governed "
            f"{OPENAI_CODEX_CREDENTIAL_STORE_ID} credential unavailable "
            f"(validation_category={self.validation_category})"
        )
        if self.detail:
            message += f" detail={self.detail}"
        super().__init__(message)


def pepper_governed_worker_env(
    *,
    project_id: str = _PROJECT_ID,
    ticket_id: str = _TICKET_ID,
    task_id: str,
    executor_profile: str = _EXECUTOR_PROFILE,
) -> dict[str, str]:
    """Return the non-secret environment overlay for a Pepper Kanban worker."""

    normalized_profile = str(executor_profile or "").strip().lower()
    if project_id != _PROJECT_ID:
        raise PepperGovernedWorkerCredentialError("project_id_mismatch")
    if ticket_id != _TICKET_ID:
        raise PepperGovernedWorkerCredentialError("ticket_id_mismatch")
    if normalized_profile != _EXECUTOR_PROFILE:
        raise PepperGovernedWorkerCredentialError("executor_profile_mismatch")
    task_fragment = _identifier_fragment(task_id, field_name="task_id")
    runtime_id = _bounded_identifier("runtime.pepper-kanban-worker", ticket_id)
    correlation_id = _bounded_identifier("correlation.pepper-kanban-worker", ticket_id, task_fragment)
    lease_id = _bounded_identifier("lease.pepper-kanban-worker", ticket_id, task_fragment)
    return {
        PEPPER_GOVERNED_WORKER_ENV: PEPPER_GOVERNED_WORKER_MODE,
        "HERMES_AGENT_PLATFORM_GOVERNED_PROJECT_ID": _PROJECT_ID,
        "HERMES_AGENT_PLATFORM_GOVERNED_TICKET_ID": _TICKET_ID,
        "HERMES_AGENT_PLATFORM_EXECUTOR_PROFILE": _EXECUTOR_PROFILE,
        "HERMES_AGENT_PLATFORM_PROVIDER": _PROVIDER,
        "HERMES_AGENT_PLATFORM_MODEL": _MODEL,
        "HERMES_AGENT_PLATFORM_API_MODE": _API_MODE,
        "HERMES_AGENT_PLATFORM_CREDENTIAL_STORE_ID": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_PROFILE_ID": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        "HERMES_AGENT_PLATFORM_WORKER_PROFILE_ID": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
        "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_ID": runtime_id,
        "HERMES_AGENT_PLATFORM_PROVIDER_CORRELATION_ID": correlation_id,
        "HERMES_AGENT_PLATFORM_PROVIDER_LEASE_ID": lease_id,
    }


def pepper_governed_worker_enabled(env: Mapping[str, str] | None = None) -> bool:
    """Return True only for the Agent Platform Pepper Kanban worker binding."""

    raw = str((env or os.environ).get(PEPPER_GOVERNED_WORKER_ENV, "") or "")
    return raw.strip().lower().replace("_", "-") == PEPPER_GOVERNED_WORKER_MODE


def resolve_pepper_governed_worker_runtime(
    *,
    env: Mapping[str, str] | None = None,
    protection_backend: Any = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Resolve worker runtime credentials from the governed store only."""

    return _resolve_pepper_governed_worker_runtime(
        env=env,
        protection_backend=protection_backend,
        now=now,
        include_secret=True,
    )


def probe_pepper_governed_worker_credentials(
    *,
    env: Mapping[str, str] | None = None,
    protection_backend: Any = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Probe the child-equivalent governed worker resolver without returning secrets."""

    return _resolve_pepper_governed_worker_runtime(
        env=env,
        protection_backend=protection_backend,
        now=now,
        include_secret=False,
    )


def _resolve_pepper_governed_worker_runtime(
    *,
    env: Mapping[str, str] | None,
    protection_backend: Any,
    now: datetime | None,
    include_secret: bool,
) -> dict[str, Any]:
    binding_env = env or os.environ
    binding = _validate_worker_binding(binding_env)
    observed = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)

    from hermes_cli.agent_platform.provider_credentials.store import (
        default_openai_codex_credential_store_root,
        load_openai_codex_oauth_credential,
        read_openai_codex_credential_status,
    )
    from hermes_cli.agent_platform.provider_runtime.contracts import (
        ProviderRuntimeResolutionRequest,
    )
    from hermes_cli.agent_platform.provider_worker.resolution import (
        resolve_provider_worker_profile,
    )

    store_root = default_openai_codex_credential_store_root(
        hermes_home=_canonical_hermes_root(binding_env)
    )
    try:
        status = read_openai_codex_credential_status(
            store_root,
            protection_backend=protection_backend,
            now=observed,
        )
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(
            _exception_category(exc, "credential_status_unavailable")
        ) from exc
    if not bool(getattr(status, "configured", False)):
        raise PepperGovernedWorkerCredentialError("governed_credential_absent")

    lease = ProviderCredentialDeliveryLease(
        lease_id=binding["lease_id"],
        runtime_id=binding["runtime_id"],
        correlation_id=binding["correlation_id"],
        created_at_utc=observed,
        expires_at_utc=observed
        + timedelta(milliseconds=MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS),
    )
    provider_request = ProviderRuntimeResolutionRequest(
        profile_id=binding["provider_runtime_profile_id"],
        runtime_id=binding["runtime_id"],
        correlation_id=binding["correlation_id"],
        requested_by="pepper-kanban-worker",
        evaluated_at_utc=observed,
        credential_status=status,
        credential_lease_ref=lease,
    )
    try:
        resolve_provider_worker_profile(
            ProviderWorkerResolutionRequest(
                worker_profile_id=binding["worker_profile_id"],
                provider_resolution_request=provider_request,
                evaluated_at_utc=observed,
            )
        )
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(
            _exception_category(exc, "provider_worker_resolution_failed")
        ) from exc

    try:
        credential = load_openai_codex_oauth_credential(
            store_root,
            protection_backend=protection_backend,
            now=observed,
        )
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(
            _exception_category(exc, "credential_load_failed")
        ) from exc

    runtime = {
        "provider": _PROVIDER,
        "model": _MODEL,
        "base_url": OPENAI_CODEX_PROVIDER_ENDPOINT,
        "api_mode": _API_MODE,
        "source": PEPPER_GOVERNED_WORKER_SOURCE,
        "credential_profile_id": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "credential_resolution_source": "canonical_governed_home",
        "provider_runtime_profile_id": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        "worker_profile_id": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
        "runtime_id": binding["runtime_id"],
        "correlation_id": binding["correlation_id"],
        "lease_id": binding["lease_id"],
        "last_refresh": credential.last_refresh_utc.isoformat().replace("+00:00", "Z"),
        "legacy_auth_json_used": False,
        "API_key_fallback_used": False,
        "credential_pool_fallback_used": False,
        "legacy_refresh_fallback": False,
        "credential_refresh_calls_per_request_maximum": 0,
        "human_smoke_marker": PEPPER_GOVERNED_WORKER_READY_MARKER,
    }
    if include_secret:
        runtime["api_key"] = credential.access_token.get_secret_value()
    return runtime


def _validate_worker_binding(env: Mapping[str, str]) -> dict[str, str]:
    if not pepper_governed_worker_enabled(env):
        raise PepperGovernedWorkerCredentialError("worker_binding_absent")
    expected = {
        "HERMES_AGENT_PLATFORM_GOVERNED_PROJECT_ID": _PROJECT_ID,
        "HERMES_AGENT_PLATFORM_GOVERNED_TICKET_ID": _TICKET_ID,
        "HERMES_AGENT_PLATFORM_EXECUTOR_PROFILE": _EXECUTOR_PROFILE,
        "HERMES_AGENT_PLATFORM_PROVIDER": _PROVIDER,
        "HERMES_AGENT_PLATFORM_MODEL": _MODEL,
        "HERMES_AGENT_PLATFORM_API_MODE": _API_MODE,
        "HERMES_AGENT_PLATFORM_CREDENTIAL_STORE_ID": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_PROFILE_ID": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        "HERMES_AGENT_PLATFORM_WORKER_PROFILE_ID": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
    }
    for key, expected_value in expected.items():
        actual = str(env.get(key, "") or "").strip()
        if actual != expected_value:
            raise PepperGovernedWorkerCredentialError(f"{key.lower()}_mismatch")
    hermes_profile = str(env.get("HERMES_PROFILE", "") or "").strip().lower()
    if hermes_profile and hermes_profile != _EXECUTOR_PROFILE:
        raise PepperGovernedWorkerCredentialError("hermes_profile_mismatch")
    runtime_id = _require_identifier(env, "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_ID")
    correlation_id = _require_identifier(
        env,
        "HERMES_AGENT_PLATFORM_PROVIDER_CORRELATION_ID",
    )
    lease_id = _require_identifier(env, "HERMES_AGENT_PLATFORM_PROVIDER_LEASE_ID")
    return {
        "runtime_id": runtime_id,
        "correlation_id": correlation_id,
        "lease_id": lease_id,
        "provider_runtime_profile_id": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        "worker_profile_id": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
    }


def _canonical_hermes_root(env: Mapping[str, str]) -> Path:
    hermes_home = str(env.get("HERMES_HOME", "") or "").strip()
    if hermes_home:
        path = Path(hermes_home)
        if path.parent.name == "profiles":
            return path.parent.parent
        return path
    from hermes_constants import get_default_hermes_root

    return get_default_hermes_root()


def _require_identifier(env: Mapping[str, str], key: str) -> str:
    value = str(env.get(key, "") or "").strip()
    if not _SAFE_IDENTIFIER.fullmatch(value):
        raise PepperGovernedWorkerCredentialError(f"{key.lower()}_invalid")
    return value


def _identifier_fragment(value: object, *, field_name: str) -> str:
    raw = _safe_text(value, limit=128)
    fragment = _UNSAFE_IDENTIFIER_CHARS.sub("-", raw).strip(".-_:")
    if not fragment or not re.match(r"^[A-Za-z0-9]", fragment):
        raise PepperGovernedWorkerCredentialError(f"{field_name}_invalid")
    return fragment[:64]


def _bounded_identifier(prefix: str, *parts: object) -> str:
    fragments = [_identifier_fragment(part, field_name="identifier") for part in parts]
    value = ".".join([prefix, *fragments])[:128]
    if not _SAFE_IDENTIFIER.fullmatch(value):
        raise PepperGovernedWorkerCredentialError("identifier_invalid")
    return value


def _safe_text(value: object, *, limit: int) -> str:
    text = str(value or "").replace("\r", "\n")
    text = _CONTROL_CHARS.sub("", text).strip()
    return text[:limit] or "not supplied"


def _exception_category(exc: BaseException, fallback: str) -> str:
    for attr in ("validation_category", "code", "error_code"):
        value = getattr(exc, attr, None)
        if value:
            return _safe_text(value, limit=120)
    return fallback


__all__ = [
    "PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE",
    "PEPPER_GOVERNED_WORKER_BLOCKER_CODE",
    "PEPPER_GOVERNED_WORKER_ENV",
    "PEPPER_GOVERNED_WORKER_MODE",
    "PEPPER_GOVERNED_WORKER_READY_MARKER",
    "PEPPER_GOVERNED_WORKER_SOURCE",
    "PepperGovernedWorkerCredentialError",
    "pepper_governed_worker_enabled",
    "pepper_governed_worker_env",
    "probe_pepper_governed_worker_credentials",
    "resolve_pepper_governed_worker_runtime",
]
