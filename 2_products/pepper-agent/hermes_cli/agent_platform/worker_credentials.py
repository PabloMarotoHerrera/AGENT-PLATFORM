"""Pepper governed worker credential binding and runtime resolution.

This module carries only Agent Platform worker credential authority. It passes
secret-free binding metadata to Kanban children and resolves credential material
from the governed provider store. Ticket/profile selection comes from runtime
projection authority, not from prompt text or historical vertical-slice names.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
from typing import Any

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_HERMES_PROVIDER_ID,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    PROVIDER_CREDENTIAL_SCHEMA_VERSION,
    ProviderCredentialDeliveryLease,
)
from hermes_cli.agent_platform.provider_runtime.contracts import (
    PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION,
    ProviderRuntimeResolutionRequest,
)
from hermes_cli.agent_platform.provider_runtime.profiles import (
    list_provider_runtime_profiles,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    PROVIDER_WORKER_PROFILE_SCHEMA_VERSION,
    ProviderWorkerResolutionRequest,
)
from hermes_cli.agent_platform.provider_worker.profiles import (
    list_provider_worker_profiles,
)


PEPPER_GOVERNED_WORKER_ENV = "HERMES_AGENT_PLATFORM_GOVERNED_WORKER"
PEPPER_GOVERNED_WORKER_MODE = "pepper-kanban-worker"
PEPPER_GOVERNED_WORKER_SOURCE = "pepper-governed-openai-codex-oauth"
PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE = "worker_credential_authority_mismatch"
PEPPER_GOVERNED_WORKER_BLOCKER_CODE = "WORKER_CREDENTIAL_AUTHORITY_MISMATCH"
PEPPER_GOVERNED_EXECUTOR_PROFILE_BLOCKER_CODE = (
    "GOVERNED_EXECUTOR_PROFILE_AUTHORITY_UNAVAILABLE"
)
PEPPER_GOVERNED_WORKER_READY_MARKER = (
    "PEPPER-WORKER-GOVERNED-CREDENTIAL-PROPAGATION-READY-FOR-HUMAN-SMOKE"
)
PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION = (
    f"provider-runtime-v{PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION}."
    f"provider-worker-v{PROVIDER_WORKER_PROFILE_SCHEMA_VERSION}."
    f"provider-credential-v{PROVIDER_CREDENTIAL_SCHEMA_VERSION}"
)

_PROJECT_ID = "PEPPER"
_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SAFE_CONTEXT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
_UNSAFE_IDENTIFIER_CHARS = re.compile(r"[^A-Za-z0-9._:-]+")
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class GovernedWorkerCredentialBinding:
    project_id: str
    ticket_id: str
    work_packet_id: str
    work_packet_SHA256: str
    ticket_spec_SHA256: str
    kanban_task_id: str
    executor_profile: str
    provider: str
    model: str
    api_mode: str
    credential_profile_id: str
    provider_runtime_profile_id: str
    worker_profile_id: str
    credential_policy_revision: str
    runtime_id: str
    correlation_id: str
    lease_id: str
    base_url: str
    profile_assignment_policy_id: str = ""
    profile_assignment_policy_revision: str = ""
    projection_SHA256: str = ""
    executor_config_source: str = "executor_profile_config_yaml"
    profile_path: str = ""

    def to_env(self) -> dict[str, str]:
        env = {
            PEPPER_GOVERNED_WORKER_ENV: PEPPER_GOVERNED_WORKER_MODE,
            "HERMES_AGENT_PLATFORM_GOVERNED_PROJECT_ID": self.project_id,
            "HERMES_AGENT_PLATFORM_GOVERNED_TICKET_ID": self.ticket_id,
            "HERMES_AGENT_PLATFORM_EXECUTOR_PROFILE": self.executor_profile,
            "HERMES_AGENT_PLATFORM_PROVIDER": self.provider,
            "HERMES_AGENT_PLATFORM_MODEL": self.model,
            "HERMES_AGENT_PLATFORM_API_MODE": self.api_mode,
            "HERMES_AGENT_PLATFORM_CREDENTIAL_STORE_ID": self.credential_profile_id,
            "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_PROFILE_ID": self.provider_runtime_profile_id,
            "HERMES_AGENT_PLATFORM_WORKER_PROFILE_ID": self.worker_profile_id,
            "HERMES_AGENT_PLATFORM_CREDENTIAL_POLICY_REVISION": self.credential_policy_revision,
            "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_ID": self.runtime_id,
            "HERMES_AGENT_PLATFORM_PROVIDER_CORRELATION_ID": self.correlation_id,
            "HERMES_AGENT_PLATFORM_PROVIDER_LEASE_ID": self.lease_id,
            "HERMES_AGENT_PLATFORM_WORKPACKET_ID": self.work_packet_id,
            "HERMES_AGENT_PLATFORM_WORKPACKET_SHA256": self.work_packet_SHA256,
            "HERMES_AGENT_PLATFORM_TICKET_SPEC_SHA256": self.ticket_spec_SHA256,
        }
        if self.projection_SHA256:
            env["HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_SHA256"] = self.projection_SHA256
        if self.profile_assignment_policy_id:
            env["HERMES_AGENT_PLATFORM_PROFILE_ASSIGNMENT_POLICY_ID"] = (
                self.profile_assignment_policy_id
            )
        if self.profile_assignment_policy_revision:
            env["HERMES_AGENT_PLATFORM_PROFILE_ASSIGNMENT_POLICY_REVISION"] = (
                self.profile_assignment_policy_revision
            )
        return env


class PepperGovernedWorkerCredentialError(RuntimeError):
    """Secret-free governed worker credential resolution failure."""

    error_code = PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE

    def __init__(self, validation_category: str, detail: object | None = None) -> None:
        self.validation_category = _safe_text(validation_category, limit=120)
        self.detail = _safe_text(detail, limit=200) if detail is not None else None
        message = (
            f"{PEPPER_GOVERNED_WORKER_BLOCKER_CODE}: governed worker "
            f"credential unavailable (validation_category={self.validation_category})"
        )
        if self.detail:
            message += f" detail={self.detail}"
        super().__init__(message)


def pepper_governed_worker_env(
    *,
    binding: GovernedWorkerCredentialBinding | None = None,
    project_id: str | None = None,
    ticket_id: str | None = None,
    work_packet_id: str | None = None,
    work_packet_SHA256: str | None = None,
    ticket_spec_SHA256: str | None = None,
    task_id: str | None = None,
    executor_profile: str | None = None,
    projection_SHA256: str | None = None,
    profile_assignment_policy_id: str | None = None,
    profile_assignment_policy_revision: str | None = None,
) -> dict[str, str]:
    """Return the non-secret environment overlay for a Pepper Kanban worker."""

    resolved = binding or build_pepper_governed_worker_credential_binding(
        project_id=_required_arg(project_id, "project_id"),
        ticket_id=_required_arg(ticket_id, "ticket_id"),
        work_packet_id=_required_arg(work_packet_id, "work_packet_id"),
        work_packet_SHA256=_required_arg(work_packet_SHA256, "work_packet_SHA256"),
        ticket_spec_SHA256=_required_arg(ticket_spec_SHA256, "ticket_spec_SHA256"),
        kanban_task_id=_required_arg(task_id, "task_id"),
        executor_profile=_required_arg(executor_profile, "executor_profile"),
        projection_SHA256=projection_SHA256 or "",
        profile_assignment_policy_id=profile_assignment_policy_id or "",
        profile_assignment_policy_revision=profile_assignment_policy_revision or "",
    )
    return resolved.to_env()


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


def build_pepper_governed_worker_credential_binding(
    *,
    project_id: str,
    ticket_id: str,
    work_packet_id: str,
    work_packet_SHA256: str,
    ticket_spec_SHA256: str,
    kanban_task_id: str,
    executor_profile: str,
    projection_SHA256: str = "",
    profile_assignment_policy_id: str = "",
    profile_assignment_policy_revision: str = "",
) -> GovernedWorkerCredentialBinding:
    """Build a secret-free binding from selected-profile and projection authority."""

    _require_project(project_id)
    ticket = _require_context_id(ticket_id, "ticket_id")
    packet = _require_context_id(work_packet_id, "work_packet_id")
    task = _require_context_id(kanban_task_id, "kanban_task_id")
    _require_digest(work_packet_SHA256, "work_packet_SHA256")
    _require_digest(ticket_spec_SHA256, "ticket_spec_SHA256")
    if projection_SHA256:
        _require_digest(projection_SHA256, "projection_SHA256")
    profile_runtime = resolve_pepper_governed_executor_profile_runtime(executor_profile)
    runtime_id = _bounded_identifier("runtime.pepper-kanban-worker", ticket, task, packet)
    correlation_id = _bounded_identifier("correlation.pepper-kanban-worker", ticket, task)
    lease_id = _bounded_identifier("lease.pepper-kanban-worker", ticket, task)
    return GovernedWorkerCredentialBinding(
        project_id=_PROJECT_ID,
        ticket_id=ticket,
        work_packet_id=packet,
        work_packet_SHA256=work_packet_SHA256.lower(),
        ticket_spec_SHA256=ticket_spec_SHA256.lower(),
        kanban_task_id=task,
        executor_profile=profile_runtime["executor_profile"],
        provider=profile_runtime["provider"],
        model=profile_runtime["model"],
        api_mode=profile_runtime["api_mode"],
        credential_profile_id=profile_runtime["credential_profile_id"],
        provider_runtime_profile_id=profile_runtime["provider_runtime_profile_id"],
        worker_profile_id=profile_runtime["worker_profile_id"],
        credential_policy_revision=PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        lease_id=lease_id,
        base_url=profile_runtime["base_url"],
        profile_assignment_policy_id=_safe_optional_identifier(
            profile_assignment_policy_id,
            "profile_assignment_policy_id",
        ),
        profile_assignment_policy_revision=_safe_optional_identifier(
            profile_assignment_policy_revision,
            "profile_assignment_policy_revision",
        ),
        projection_SHA256=projection_SHA256.lower() if projection_SHA256 else "",
        executor_config_source=profile_runtime["executor_config_source"],
        profile_path=profile_runtime.get("profile_path", ""),
    )


def resolve_pepper_governed_executor_profile_runtime(
    profile_name: str,
    *,
    profile_dir: Path | None = None,
    require_assignable_roster_profile: bool = True,
) -> dict[str, Any]:
    """Resolve selected executor profile config into governed provider policy."""

    if profile_dir is None:
        profile_info = _selected_profile_authority(profile_name)
        profile_dir = Path(str(profile_info["profile_path"]))
        executor_profile = str(profile_info["executor_profile"])
        classification = profile_info.get("classification")
    else:
        executor_profile = _canonical_profile_name(profile_name)
        classification = None
        if require_assignable_roster_profile:
            profile_info = _selected_profile_authority(executor_profile)
            profile_dir = Path(str(profile_info["profile_path"]))
            executor_profile = str(profile_info["executor_profile"])
            classification = profile_info.get("classification")
    launch_config = _executor_profile_launch_config(profile_dir)
    provider_policy = _provider_policy_for_launch_config(launch_config)
    return {
        "ok": True,
        "executor_profile": executor_profile,
        "profile_path": str(profile_dir),
        "classification": classification,
        **provider_policy,
        "executor_config_source": launch_config["executor_config_source"],
        "credential_policy_revision": PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION,
    }


def probe_pepper_governed_executor_profile_readiness(
    profile_name: str,
    *,
    env: Mapping[str, str] | None = None,
    protection_backend: Any = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return bounded non-secret readiness for a selected executor profile."""

    observed = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    try:
        profile_runtime = resolve_pepper_governed_executor_profile_runtime(profile_name)
        status = _read_governed_credential_status(
            provider=profile_runtime["provider"],
            credential_profile_id=profile_runtime["credential_profile_id"],
            hermes_root=_canonical_hermes_root(env or os.environ),
            protection_backend=protection_backend,
            now=observed,
        )
        if not bool(getattr(status, "configured", False)):
            return _profile_readiness_blocked(
                profile_runtime,
                status=status,
                blocker_detail=(
                    "executor profile lacks governed "
                    f"{profile_runtime['credential_profile_id']} credentials"
                ),
                validation_category="governed_credential_absent",
            )
        _resolve_provider_worker_with_status(
            provider_runtime_profile_id=profile_runtime["provider_runtime_profile_id"],
            worker_profile_id=profile_runtime["worker_profile_id"],
            runtime_id="runtime.pepper-worker-start-readiness",
            correlation_id=_bounded_identifier(
                "correlation.pepper-worker-start",
                profile_runtime["executor_profile"],
            ),
            lease_id="lease.pepper-worker-start-readiness",
            requested_by="pepper-worker-start-action",
            status=status,
            observed=observed,
        )
    except PepperGovernedWorkerCredentialError as exc:
        return {
            "ok": False,
            "blocker_code": _blocker_code_for_category(exc.validation_category),
            "blocker_detail": f"executor credential binding failed: {exc.validation_category}",
            "validation_category": exc.validation_category,
            "legacy_auth_json_used": False,
            "API_key_fallback_used": False,
            "credential_pool_fallback_used": False,
            "governed_refresh_path": "provider_worker_resolution_no_refresh",
            "legacy_refresh_fallback": False,
        }
    except Exception as exc:
        category = _exception_category(exc, "provider_worker_resolution_failed")
        return {
            "ok": False,
            "blocker_code": "EXECUTOR_PROVIDER_RESOLUTION_GAP",
            "blocker_detail": f"executor provider-worker resolution failed: {category}",
            "validation_category": category,
            "legacy_auth_json_used": False,
            "API_key_fallback_used": False,
            "credential_pool_fallback_used": False,
            "governed_refresh_path": "provider_worker_resolution_no_refresh",
            "legacy_refresh_fallback": False,
        }
    return {
        "ok": True,
        **_runtime_public_fields(profile_runtime),
        "credential_resolution_source": "canonical_governed_home",
        "durable_store_valid": bool(getattr(status, "durable_store_valid", False)),
        "token_pair_present": bool(getattr(status, "token_pair_present", False)),
        "legacy_auth_json_used": False,
        "API_key_fallback_used": False,
        "credential_pool_fallback_used": False,
        "governed_refresh_path": "provider_worker_resolution_no_refresh",
        "legacy_refresh_fallback": False,
        "credential_refresh_calls_per_request_maximum": 0,
    }


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
    status = _read_governed_credential_status(
        provider=binding.provider,
        credential_profile_id=binding.credential_profile_id,
        hermes_root=_canonical_hermes_root(binding_env),
        protection_backend=protection_backend,
        now=observed,
    )
    if not bool(getattr(status, "configured", False)):
        raise PepperGovernedWorkerCredentialError("governed_credential_absent")
    _resolve_provider_worker_with_status(
        provider_runtime_profile_id=binding.provider_runtime_profile_id,
        worker_profile_id=binding.worker_profile_id,
        runtime_id=binding.runtime_id,
        correlation_id=binding.correlation_id,
        lease_id=binding.lease_id,
        requested_by="pepper-kanban-worker",
        status=status,
        observed=observed,
    )
    credential = _load_governed_credential(
        provider=binding.provider,
        credential_profile_id=binding.credential_profile_id,
        hermes_root=_canonical_hermes_root(binding_env),
        protection_backend=protection_backend,
        now=observed,
    )
    runtime = {
        "provider": binding.provider,
        "model": binding.model,
        "base_url": binding.base_url,
        "api_mode": binding.api_mode,
        "source": PEPPER_GOVERNED_WORKER_SOURCE,
        "ticket_id": binding.ticket_id,
        "work_packet_id": binding.work_packet_id,
        "work_packet_SHA256": binding.work_packet_SHA256,
        "executor_profile": binding.executor_profile,
        "credential_profile_id": binding.credential_profile_id,
        "credential_policy_revision": binding.credential_policy_revision,
        "credential_resolution_source": "canonical_governed_home",
        "provider_runtime_profile_id": binding.provider_runtime_profile_id,
        "worker_profile_id": binding.worker_profile_id,
        "runtime_id": binding.runtime_id,
        "correlation_id": binding.correlation_id,
        "lease_id": binding.lease_id,
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


def _validate_worker_binding(env: Mapping[str, str]) -> GovernedWorkerCredentialBinding:
    if not pepper_governed_worker_enabled(env):
        raise PepperGovernedWorkerCredentialError("worker_binding_absent")
    project_id = _require_env(env, "HERMES_AGENT_PLATFORM_GOVERNED_PROJECT_ID")
    _require_project(project_id)
    ticket_id = _require_context_id(
        _require_env(env, "HERMES_AGENT_PLATFORM_GOVERNED_TICKET_ID"),
        "ticket_id",
    )
    work_packet_id = _require_context_id(
        _require_env(env, "HERMES_AGENT_PLATFORM_WORKPACKET_ID"),
        "work_packet_id",
    )
    work_packet_sha = _require_digest(
        _require_env(env, "HERMES_AGENT_PLATFORM_WORKPACKET_SHA256"),
        "work_packet_SHA256",
    )
    ticket_spec_sha = _require_digest(
        _require_env(env, "HERMES_AGENT_PLATFORM_TICKET_SPEC_SHA256"),
        "ticket_spec_SHA256",
    )
    projection_sha = _require_digest(
        _require_env(env, "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_SHA256"),
        "projection_SHA256",
    )
    executor_profile = _canonical_profile_name(
        _require_env(env, "HERMES_AGENT_PLATFORM_EXECUTOR_PROFILE")
    )
    hermes_profile = str(env.get("HERMES_PROFILE", "") or "").strip().lower()
    if hermes_profile and hermes_profile != executor_profile.lower():
        raise PepperGovernedWorkerCredentialError("hermes_profile_mismatch")
    profile_dir = _selected_profile_dir_from_env(env)
    _validate_persisted_worker_authority(
        env,
        ticket_id=ticket_id,
        work_packet_id=work_packet_id,
        work_packet_SHA256=work_packet_sha,
        ticket_spec_SHA256=ticket_spec_sha,
        projection_SHA256=projection_sha,
        executor_profile=executor_profile,
    )
    actual_runtime = resolve_pepper_governed_executor_profile_runtime(
        executor_profile,
        profile_dir=profile_dir,
        require_assignable_roster_profile=False,
    )
    expected = {
        "HERMES_AGENT_PLATFORM_PROVIDER": actual_runtime["provider"],
        "HERMES_AGENT_PLATFORM_MODEL": actual_runtime["model"],
        "HERMES_AGENT_PLATFORM_API_MODE": actual_runtime["api_mode"],
        "HERMES_AGENT_PLATFORM_CREDENTIAL_STORE_ID": actual_runtime["credential_profile_id"],
        "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_PROFILE_ID": actual_runtime[
            "provider_runtime_profile_id"
        ],
        "HERMES_AGENT_PLATFORM_WORKER_PROFILE_ID": actual_runtime["worker_profile_id"],
        "HERMES_AGENT_PLATFORM_CREDENTIAL_POLICY_REVISION": (
            PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION
        ),
    }
    for key, expected_value in expected.items():
        actual = str(env.get(key, "") or "").strip()
        if actual != expected_value:
            raise PepperGovernedWorkerCredentialError(f"{key.lower()}_mismatch")
    return GovernedWorkerCredentialBinding(
        project_id=_PROJECT_ID,
        ticket_id=ticket_id,
        work_packet_id=work_packet_id,
        work_packet_SHA256=work_packet_sha,
        ticket_spec_SHA256=ticket_spec_sha,
        kanban_task_id=str(env.get("HERMES_KANBAN_TASK") or "not-supplied"),
        executor_profile=executor_profile,
        provider=actual_runtime["provider"],
        model=actual_runtime["model"],
        api_mode=actual_runtime["api_mode"],
        credential_profile_id=actual_runtime["credential_profile_id"],
        provider_runtime_profile_id=actual_runtime["provider_runtime_profile_id"],
        worker_profile_id=actual_runtime["worker_profile_id"],
        credential_policy_revision=PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION,
        runtime_id=_require_identifier(env, "HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_ID"),
        correlation_id=_require_identifier(
            env,
            "HERMES_AGENT_PLATFORM_PROVIDER_CORRELATION_ID",
        ),
        lease_id=_require_identifier(env, "HERMES_AGENT_PLATFORM_PROVIDER_LEASE_ID"),
        base_url=actual_runtime["base_url"],
        profile_assignment_policy_id=_safe_optional_identifier(
            str(env.get("HERMES_AGENT_PLATFORM_PROFILE_ASSIGNMENT_POLICY_ID") or ""),
            "profile_assignment_policy_id",
        ),
        profile_assignment_policy_revision=_safe_optional_identifier(
            str(env.get("HERMES_AGENT_PLATFORM_PROFILE_ASSIGNMENT_POLICY_REVISION") or ""),
            "profile_assignment_policy_revision",
        ),
        projection_SHA256=projection_sha,
        executor_config_source=actual_runtime["executor_config_source"],
        profile_path=str(profile_dir),
    )


def _validate_persisted_worker_authority(
    env: Mapping[str, str],
    *,
    ticket_id: str,
    work_packet_id: str,
    work_packet_SHA256: str,
    ticket_spec_SHA256: str,
    projection_SHA256: str,
    executor_profile: str,
) -> None:
    generation_record = _read_authority_record(
        _require_env(env, "HERMES_AGENT_PLATFORM_GENERATION_RECORD_PATH"),
        "generation_record",
    )
    projection_record = _read_authority_record(
        _require_env(env, "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_RECORD_PATH"),
        "kanban_projection_record",
    )
    _read_authority_record(
        _require_env(env, "HERMES_AGENT_PLATFORM_APPROVAL_DECISION_RECORD_PATH"),
        "approval_decision_record",
    )
    expected = {
        "ticket_id": ticket_id,
        "work_packet_id": work_packet_id,
        "work_packet_SHA256": work_packet_SHA256,
        "ticket_spec_SHA256": ticket_spec_SHA256,
    }
    for key, expected_value in expected.items():
        if generation_record.get(key) != expected_value:
            raise PepperGovernedWorkerCredentialError(f"generation_record_{key}_mismatch")
        if projection_record.get(key) != expected_value:
            raise PepperGovernedWorkerCredentialError(f"projection_record_{key}_mismatch")
    if projection_record.get("projection_SHA256") != projection_SHA256:
        raise PepperGovernedWorkerCredentialError("projection_record_projection_sha256_mismatch")
    if str(projection_record.get("assignee_profile") or "").strip().lower() != executor_profile.lower():
        raise PepperGovernedWorkerCredentialError("projection_record_executor_profile_mismatch")


def _read_authority_record(path_text: str, role: str) -> dict[str, Any]:
    path = Path(path_text).expanduser()
    if not path.is_absolute() or not path.is_file():
        raise PepperGovernedWorkerCredentialError(f"{role}_unavailable")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(f"{role}_unreadable") from exc
    if not isinstance(data, dict):
        raise PepperGovernedWorkerCredentialError(f"{role}_invalid")
    return data


def _selected_profile_authority(profile_name: str) -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        classify_pepper_execution_profile,
    )
    from hermes_cli.profiles import list_profiles, normalize_profile_name

    canonical = normalize_profile_name(profile_name)
    try:
        profiles = list_profiles()
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(
            "selected_profile_roster_unavailable",
            exc,
        ) from exc
    for profile in profiles:
        try:
            candidate = normalize_profile_name(str(getattr(profile, "name", "")))
        except Exception:
            continue
        if candidate != canonical:
            continue
        classification = classify_pepper_execution_profile(profile)
        if classification.get("worker_assignable") is not True:
            raise PepperGovernedWorkerCredentialError(
                "selected_profile_not_worker_assignable",
                classification.get("rejection_reasons"),
            )
        path = getattr(profile, "path", None)
        if not path:
            raise PepperGovernedWorkerCredentialError("selected_profile_path_unavailable")
        return {
            "executor_profile": canonical,
            "profile_path": str(path),
            "classification": classification,
        }
    raise PepperGovernedWorkerCredentialError("selected_profile_missing", canonical)


def _executor_profile_launch_config(profile_dir: Path) -> dict[str, Any]:
    if not profile_dir.is_dir():
        raise PepperGovernedWorkerCredentialError(
            "selected_profile_path_unavailable",
            profile_dir,
        )
    config = _read_executor_profile_config(profile_dir)
    model_cfg = config.get("model") if isinstance(config, dict) else None
    provider = ""
    model = ""
    api_mode = ""
    if isinstance(model_cfg, dict):
        provider = str(model_cfg.get("provider") or "").strip().lower()
        model = str(model_cfg.get("default") or model_cfg.get("model") or "").strip()
        api_mode = str(model_cfg.get("api_mode") or "").strip().lower()
    elif isinstance(model_cfg, str):
        model = model_cfg.strip()
    if not provider or not model:
        raise PepperGovernedWorkerCredentialError(
            "provider_runtime_profile_unavailable",
            "executor profile must define model.provider and model.default",
        )
    return {
        "provider": provider,
        "model": model,
        "api_mode": api_mode,
        "executor_config_source": "executor_profile_config_yaml",
    }


def _read_executor_profile_config(profile_dir: Path) -> dict[str, Any]:
    config_path = profile_dir / "config.yaml"
    if not config_path.is_file():
        return {}
    try:
        import yaml

        with config_path.open("r", encoding="utf-8") as stream:
            loaded = yaml.safe_load(stream) or {}
        return loaded if isinstance(loaded, dict) else {}
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError("selected_profile_config_unreadable") from exc


def _provider_policy_for_launch_config(launch_config: dict[str, Any]) -> dict[str, str]:
    provider = str(launch_config["provider"])
    model = str(launch_config["model"])
    api_mode = str(launch_config.get("api_mode") or "")
    candidates = []
    for runtime_profile in list_provider_runtime_profiles():
        runtime_provider = str(getattr(runtime_profile.provider, "value", runtime_profile.provider))
        runtime_transport = str(getattr(runtime_profile.transport, "value", runtime_profile.transport))
        runtime_model = str(runtime_profile.model_policy.model_id)
        if runtime_provider != provider or runtime_model != model:
            continue
        if api_mode and runtime_transport != api_mode:
            continue
        candidates.append(runtime_profile)
    if not candidates:
        raise PepperGovernedWorkerCredentialError(
            "provider_runtime_profile_unavailable",
            f"provider={provider} model={model} api_mode={api_mode or 'default'}",
        )
    if len(candidates) > 1:
        raise PepperGovernedWorkerCredentialError("provider_runtime_profile_ambiguous")
    runtime_profile = candidates[0]
    credential_profile_id = str(runtime_profile.credential_requirement.credential_store_id)
    worker_candidates = [
        worker_profile
        for worker_profile in list_provider_worker_profiles()
        if str(worker_profile.provider_runtime_profile_id) == str(runtime_profile.profile_id)
        and str(worker_profile.credential_store_id) == credential_profile_id
    ]
    if not worker_candidates:
        raise PepperGovernedWorkerCredentialError("provider_worker_profile_unavailable")
    if len(worker_candidates) > 1:
        raise PepperGovernedWorkerCredentialError("provider_worker_profile_ambiguous")
    worker_profile = worker_candidates[0]
    return {
        "provider": provider,
        "model": model,
        "api_mode": str(getattr(runtime_profile.transport, "value", runtime_profile.transport)),
        "credential_profile_id": credential_profile_id,
        "provider_runtime_profile_id": str(runtime_profile.profile_id),
        "worker_profile_id": str(worker_profile.profile_id),
        "base_url": str(runtime_profile.endpoint_policy.provider_endpoint),
    }


def _read_governed_credential_status(
    *,
    provider: str,
    credential_profile_id: str,
    hermes_root: Path,
    protection_backend: Any,
    now: datetime,
) -> Any:
    if provider != OPENAI_CODEX_HERMES_PROVIDER_ID or credential_profile_id != OPENAI_CODEX_CREDENTIAL_STORE_ID:
        raise PepperGovernedWorkerCredentialError("credential_profile_provider_mismatch")
    from hermes_cli.agent_platform.provider_credentials.store import (
        default_openai_codex_credential_store_root,
        read_openai_codex_credential_status,
    )

    store_root = default_openai_codex_credential_store_root(hermes_home=hermes_root)
    try:
        kwargs = {"now": now}
        if protection_backend is not None:
            kwargs["protection_backend"] = protection_backend
        return read_openai_codex_credential_status(
            store_root,
            **kwargs,
        )
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(
            _exception_category(exc, "credential_status_unavailable")
        ) from exc


def _load_governed_credential(
    *,
    provider: str,
    credential_profile_id: str,
    hermes_root: Path,
    protection_backend: Any,
    now: datetime,
) -> Any:
    if provider != OPENAI_CODEX_HERMES_PROVIDER_ID or credential_profile_id != OPENAI_CODEX_CREDENTIAL_STORE_ID:
        raise PepperGovernedWorkerCredentialError("credential_profile_provider_mismatch")
    from hermes_cli.agent_platform.provider_credentials.store import (
        default_openai_codex_credential_store_root,
        load_openai_codex_oauth_credential,
    )

    store_root = default_openai_codex_credential_store_root(hermes_home=hermes_root)
    try:
        kwargs = {"now": now}
        if protection_backend is not None:
            kwargs["protection_backend"] = protection_backend
        return load_openai_codex_oauth_credential(
            store_root,
            **kwargs,
        )
    except Exception as exc:
        raise PepperGovernedWorkerCredentialError(
            _exception_category(exc, "credential_load_failed")
        ) from exc


def _resolve_provider_worker_with_status(
    *,
    provider_runtime_profile_id: str,
    worker_profile_id: str,
    runtime_id: str,
    correlation_id: str,
    lease_id: str,
    requested_by: str,
    status: Any,
    observed: datetime,
) -> None:
    from hermes_cli.agent_platform.provider_worker.resolution import (
        resolve_provider_worker_profile,
    )

    lease = ProviderCredentialDeliveryLease(
        lease_id=lease_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        created_at_utc=observed,
        expires_at_utc=observed
        + timedelta(milliseconds=MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS),
    )
    provider_request = ProviderRuntimeResolutionRequest(
        profile_id=provider_runtime_profile_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        requested_by=requested_by,
        evaluated_at_utc=observed,
        credential_status=status,
        credential_lease_ref=lease,
    )
    resolve_provider_worker_profile(
        ProviderWorkerResolutionRequest(
            worker_profile_id=worker_profile_id,
            provider_resolution_request=provider_request,
            evaluated_at_utc=observed,
        )
    )


def _profile_readiness_blocked(
    profile_runtime: dict[str, Any],
    *,
    status: Any,
    blocker_detail: str,
    validation_category: str,
) -> dict[str, Any]:
    return {
        "ok": False,
        **_runtime_public_fields(profile_runtime),
        "blocker_code": "EXECUTOR_PROVIDER_RESOLUTION_GAP",
        "blocker_detail": blocker_detail,
        "validation_category": validation_category,
        "credential_resolution_source": "canonical_governed_home",
        "durable_store_valid": bool(getattr(status, "durable_store_valid", False)),
        "token_pair_present": bool(getattr(status, "token_pair_present", False)),
        "legacy_auth_json_used": False,
        "API_key_fallback_used": False,
        "credential_pool_fallback_used": False,
        "governed_refresh_path": "provider_worker_resolution_no_refresh",
        "legacy_refresh_fallback": False,
    }


def _runtime_public_fields(profile_runtime: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": profile_runtime["provider"],
        "model": profile_runtime["model"],
        "api_mode": profile_runtime["api_mode"],
        "credential_profile_id": profile_runtime["credential_profile_id"],
        "credential_policy_revision": profile_runtime["credential_policy_revision"],
        "provider_runtime_profile_id": profile_runtime["provider_runtime_profile_id"],
        "worker_profile_id": profile_runtime["worker_profile_id"],
        "source": PEPPER_GOVERNED_WORKER_SOURCE,
        "executor_profile": profile_runtime["executor_profile"],
        "executor_config_source": profile_runtime["executor_config_source"],
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


def _selected_profile_dir_from_env(env: Mapping[str, str]) -> Path:
    hermes_home = str(env.get("HERMES_HOME", "") or "").strip()
    if not hermes_home:
        raise PepperGovernedWorkerCredentialError("selected_profile_path_unavailable")
    path = Path(hermes_home)
    if not path.is_dir():
        raise PepperGovernedWorkerCredentialError("selected_profile_path_unavailable", path)
    return path


def _required_arg(value: str | None, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise PepperGovernedWorkerCredentialError(f"{field_name}_missing")
    return str(value)


def _require_env(env: Mapping[str, str], key: str) -> str:
    value = str(env.get(key, "") or "").strip()
    if not value:
        raise PepperGovernedWorkerCredentialError(f"{key.lower()}_missing")
    return value


def _require_project(project_id: str) -> str:
    if str(project_id or "").strip() != _PROJECT_ID:
        raise PepperGovernedWorkerCredentialError("project_id_mismatch")
    return _PROJECT_ID


def _require_context_id(value: str, field_name: str) -> str:
    text = str(value or "").strip()
    if not _SAFE_CONTEXT_ID.fullmatch(text):
        raise PepperGovernedWorkerCredentialError(f"{field_name}_invalid")
    return text


def _require_digest(value: str, field_name: str) -> str:
    text = str(value or "").strip().lower()
    if not _DIGEST_RE.fullmatch(text):
        raise PepperGovernedWorkerCredentialError(f"{field_name}_invalid")
    return text


def _safe_optional_identifier(value: str, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if not _SAFE_CONTEXT_ID.fullmatch(text):
        raise PepperGovernedWorkerCredentialError(f"{field_name}_invalid")
    return text


def _require_identifier(env: Mapping[str, str], key: str) -> str:
    value = str(env.get(key, "") or "").strip()
    if not _SAFE_IDENTIFIER.fullmatch(value):
        raise PepperGovernedWorkerCredentialError(f"{key.lower()}_invalid")
    return value


def _canonical_profile_name(profile_name: object) -> str:
    text = str(profile_name or "").strip().lower()
    if not text:
        raise PepperGovernedWorkerCredentialError("selected_profile_missing")
    return text


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


def _blocker_code_for_category(category: str) -> str:
    if category in {
        "selected_profile_missing",
        "selected_profile_path_unavailable",
        "selected_profile_roster_unavailable",
    }:
        return PEPPER_GOVERNED_EXECUTOR_PROFILE_BLOCKER_CODE
    if category == "selected_profile_not_worker_assignable":
        return "PROFILE_ASSIGNMENT_GAP"
    return "EXECUTOR_PROVIDER_RESOLUTION_GAP"


__all__ = [
    "PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION",
    "PEPPER_GOVERNED_EXECUTOR_PROFILE_BLOCKER_CODE",
    "PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE",
    "PEPPER_GOVERNED_WORKER_BLOCKER_CODE",
    "PEPPER_GOVERNED_WORKER_ENV",
    "PEPPER_GOVERNED_WORKER_MODE",
    "PEPPER_GOVERNED_WORKER_READY_MARKER",
    "PEPPER_GOVERNED_WORKER_SOURCE",
    "GovernedWorkerCredentialBinding",
    "PepperGovernedWorkerCredentialError",
    "build_pepper_governed_worker_credential_binding",
    "pepper_governed_worker_enabled",
    "pepper_governed_worker_env",
    "probe_pepper_governed_executor_profile_readiness",
    "probe_pepper_governed_worker_credentials",
    "resolve_pepper_governed_executor_profile_runtime",
    "resolve_pepper_governed_worker_runtime",
]
