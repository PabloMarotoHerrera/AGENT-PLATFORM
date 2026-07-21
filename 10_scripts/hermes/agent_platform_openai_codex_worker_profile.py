#!/usr/bin/env python3
"""Bounded worker-profile status gate for Hermes OpenAI Codex OAuth."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
GATE_ID = "P15.3"
VERDICT = "hermes_openai_codex_bounded_worker_profile_ready_with_constraints"

PREREQUISITE_EXIT_CODE = 20
REGISTRY_EXIT_CODE = 21
CONTRACT_EXIT_CODE = 22
PROVIDER_PROFILE_MISMATCH_EXIT_CODE = 23
PROTOCOL_POLICY_EXIT_CODE = 24
UNEXPECTED_EXIT_CODE = 29

WORKER_PROFILE_ID = "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
PROVIDER_RUNTIME_PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
CREDENTIAL_STORE_ID = "openai-codex.primary"


class WorkerProfileGateError(RuntimeError):
    """Raised when the P15.3 bounded worker profile cannot be proven."""

    exit_code = UNEXPECTED_EXIT_CODE


class WorkerProfileRegistryError(WorkerProfileGateError):
    exit_code = REGISTRY_EXIT_CODE


class WorkerProfileContractError(WorkerProfileGateError):
    exit_code = CONTRACT_EXIT_CODE


class WorkerProviderProfileMismatchError(WorkerProfileGateError):
    exit_code = PROVIDER_PROFILE_MISMATCH_EXIT_CODE


class WorkerProtocolPolicyError(WorkerProfileGateError):
    exit_code = PROTOCOL_POLICY_EXIT_CODE


@dataclass(frozen=True, slots=True)
class WorkerProfileGateConfig:
    """Trusted internal composition input; not exposed as a CLI argument."""

    product_root: Path


@dataclass(frozen=True, slots=True)
class WorkerProfileModules:
    """Product modules used by the read-only status gate."""

    provider_worker: Any


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _product_root() -> Path:
    return _repository_root() / "2_products" / "hermes-agent"


def _load_product_modules(product_root: Path) -> WorkerProfileModules:
    if not (product_root / "hermes_cli" / "agent_platform").is_dir():
        raise WorkerProfileGateError("Hermes AGENT PLATFORM package was not found")
    product_path = str(product_root)
    if product_path not in sys.path:
        sys.path.insert(0, product_path)

    from hermes_cli.agent_platform import provider_worker

    return WorkerProfileModules(provider_worker=provider_worker)


def _default_config() -> WorkerProfileGateConfig:
    return WorkerProfileGateConfig(product_root=_product_root())


def _safe_error(error: BaseException, *paths: Path) -> str:
    text = f"{type(error).__name__}: {error}"
    for path in paths:
        raw = str(path)
        text = text.replace(raw, "<path>")
        text = text.replace(raw.replace("\\", "/"), "<path>")
    for marker in ("token", "secret", "password", "api_key", "authorization"):
        text = text.replace(marker.upper(), marker)
    return text[:500]


def run_status(
    config: WorkerProfileGateConfig | None = None,
    *,
    module_loader: Callable[[Path], WorkerProfileModules] | None = None,
) -> dict[str, Any]:
    """Return the bounded P15.3 worker profile summary."""

    resolved_config = config or _default_config()
    modules = (
        module_loader(resolved_config.product_root)
        if module_loader is not None
        else _load_product_modules(resolved_config.product_root)
    )
    provider_worker = modules.provider_worker
    profile_ids = provider_worker.list_provider_worker_profile_ids()
    profiles = provider_worker.list_provider_worker_profiles()
    if profile_ids != (WORKER_PROFILE_ID,) or len(profiles) != 1:
        raise WorkerProfileRegistryError("worker profile registry is not singular")
    profile = provider_worker.get_provider_worker_profile(WORKER_PROFILE_ID)
    if profile.schema_version != SCHEMA_VERSION:
        raise WorkerProfileContractError("worker profile schema version mismatch")
    if profile.provider_runtime_profile_id != PROVIDER_RUNTIME_PROFILE_ID:
        raise WorkerProviderProfileMismatchError("provider-runtime profile mismatch")
    if profile.credential_store_id != CREDENTIAL_STORE_ID:
        raise WorkerProfileContractError("credential store mismatch")

    execution = profile.execution_policy
    request = profile.request_policy
    result = profile.result_policy
    if request.provider_runtime_profile_id != profile.provider_runtime_profile_id:
        raise WorkerProviderProfileMismatchError(
            "request policy provider profile mismatch"
        )
    if result.output_kind.value != "text":
        raise WorkerProtocolPolicyError("worker result output kind mismatch")

    return {
        "verdict": VERDICT,
        "schema_version": SCHEMA_VERSION,
        "worker_profile_id": profile.profile_id,
        "worker_profile_state": profile.state.value,
        "provider_runtime_profile_id": profile.provider_runtime_profile_id,
        "credential_store_id": profile.credential_store_id,
        "maximum_concurrent_workers": execution.maximum_concurrent_workers,
        "maximum_concurrent_requests": (
            execution.maximum_concurrent_requests_per_worker
        ),
        "maximum_requests_per_worker_lifetime": (
            execution.maximum_requests_per_worker_lifetime
        ),
        "request_queue_capacity": execution.request_queue_capacity,
        "provider_calls_per_request_maximum": (
            execution.provider_calls_per_request_maximum
        ),
        "model_list_calls_per_request_maximum": (
            execution.model_list_calls_per_request_maximum
        ),
        "credential_refresh_calls_per_request_maximum": (
            execution.credential_refresh_calls_per_request_maximum
        ),
        "input_kind": request.input_kind.value,
        "output_kind": result.output_kind.value,
        "streaming_enabled": execution.streaming.value != "disabled",
        "tools_enabled": execution.tools.value != "disabled",
        "hosted_tools_enabled": execution.hosted_tools.value != "disabled",
        "MCP_enabled": execution.MCP.value != "disabled",
        "automatic_retry_enabled": execution.automatic_retry.value != "disabled",
        "automatic_fallback_enabled": execution.automatic_fallback.value != "disabled",
        "persistent_memory_enabled": execution.persistent_memory.value != "disabled",
        "process_reuse_enabled": execution.process_reuse.value != "disabled",
        "inference_gate_required": profile.inference_gate_required,
        "controlled_lifecycle_gate_required": profile.controlled_lifecycle_gate_required,
        "runtime_entitlement_verified": profile.runtime_entitlement_verified,
        "runtime_transport_verified": profile.runtime_transport_verified,
        "worker_runtime_verified": profile.worker_runtime_verified,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("status", help="Inspect the fixed bounded worker profile")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parser.parse_args(argv)
    try:
        result = run_status()
    except WorkerProfileGateError as exc:
        result = {
            "schema_version": SCHEMA_VERSION,
            "gate_id": GATE_ID,
            "status": "failed",
            "error": _safe_error(exc, _repository_root(), _product_root()),
        }
        print(json.dumps(result, sort_keys=True))
        return exc.exit_code
    except Exception as exc:
        result = {
            "schema_version": SCHEMA_VERSION,
            "gate_id": GATE_ID,
            "status": "failed",
            "error": _safe_error(exc, _repository_root(), _product_root()),
        }
        print(json.dumps(result, sort_keys=True))
        return UNEXPECTED_EXIT_CODE
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
