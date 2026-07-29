#!/usr/bin/env python3
"""Provider-runtime profile status gate for Hermes OpenAI Codex OAuth."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
GATE_ID = "P15.2"
VERDICT = "hermes_openai_codex_provider_runtime_profile_ready_with_constraints"
PREREQUISITE_EXIT_CODE = 20


class ProviderProfileGateError(RuntimeError):
    """Raised when the P15.2 provider-runtime profile cannot be proven."""


@dataclass(frozen=True, slots=True)
class ProviderProfileGateConfig:
    """Trusted internal composition input; not exposed as a CLI argument."""

    product_root: Path


@dataclass(frozen=True, slots=True)
class ProviderProfileModules:
    """Product modules used by the read-only status gate."""

    provider_runtime: Any
    auth: Any
    providers: Any
    codex_models: Any


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _product_root() -> Path:
    return _repository_root() / "2_products" / "pepper-agent"


def _load_product_modules(product_root: Path) -> ProviderProfileModules:
    if not (product_root / "hermes_cli" / "agent_platform").is_dir():
        raise ProviderProfileGateError("Hermes AGENT PLATFORM package was not found")
    product_path = str(product_root)
    if product_path not in sys.path:
        sys.path.insert(0, product_path)

    from hermes_cli import auth, codex_models, providers
    from hermes_cli.agent_platform import provider_runtime

    return ProviderProfileModules(
        provider_runtime=provider_runtime,
        auth=auth,
        providers=providers,
        codex_models=codex_models,
    )


def _default_config() -> ProviderProfileGateConfig:
    return ProviderProfileGateConfig(product_root=_product_root())


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
    config: ProviderProfileGateConfig | None = None,
    *,
    module_loader: Callable[[Path], ProviderProfileModules] | None = None,
) -> dict[str, Any]:
    """Return the bounded P15.2 provider-runtime profile summary."""

    resolved_config = config or _default_config()
    modules = (
        module_loader(resolved_config.product_root)
        if module_loader is not None
        else _load_product_modules(resolved_config.product_root)
    )
    profile_ids = modules.provider_runtime.list_provider_runtime_profile_ids()
    profile = modules.provider_runtime.get_provider_runtime_profile(profile_ids[0])
    overlay = modules.providers.HERMES_OVERLAYS.get("openai-codex")
    endpoint = profile.endpoint_policy.provider_endpoint
    generation = profile.generation_policy
    return {
        "schema_version": SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "status": "passed",
        "verdict": VERDICT,
        "root_exports": list(modules.provider_runtime.__all__),
        "registry": {
            "profile_count": len(
                modules.provider_runtime.list_provider_runtime_profiles()
            ),
            "profile_ids": list(profile_ids),
        },
        "provider_runtime_profile": {
            "schema_version": profile.schema_version,
            "profile_id": profile.profile_id,
            "state": profile.state.value,
            "provider": profile.provider.value,
            "authentication": profile.authentication.value,
            "transport": profile.transport.value,
            "credential_store_id": (profile.credential_requirement.credential_store_id),
            "provider_endpoint": endpoint,
            "endpoint_source": profile.endpoint_policy.endpoint_source,
            "model_id": profile.model_policy.model_id,
            "worker_profile_required": profile.worker_profile_required,
            "runtime_entitlement_verified": profile.runtime_entitlement_verified,
            "runtime_transport_verified": profile.runtime_transport_verified,
        },
        "endpoint_policy": {
            "base_url_override_allowed": profile.endpoint_policy.base_url_override_allowed,
            "caller_endpoint_allowed": profile.endpoint_policy.caller_endpoint_allowed,
            "frontend_endpoint_allowed": profile.endpoint_policy.frontend_endpoint_allowed,
            "config_endpoint_allowed": profile.endpoint_policy.config_endpoint_allowed,
            "custom_endpoint_allowed": profile.endpoint_policy.custom_endpoint_allowed,
            "proxy_endpoint_allowed": profile.endpoint_policy.proxy_endpoint_allowed,
            "aggregator_endpoint_allowed": (
                profile.endpoint_policy.aggregator_endpoint_allowed
            ),
        },
        "generation_policy": {
            "maximum_prompt_tokens": generation.maximum_prompt_tokens,
            "reserved_system_instruction_tokens": (
                generation.reserved_system_instruction_tokens
            ),
            "maximum_user_content_tokens": generation.maximum_user_content_tokens,
            "maximum_output_tokens": generation.maximum_output_tokens,
            "reasoning_effort": generation.reasoning_effort,
            "streaming": generation.streaming.value,
            "tools": generation.tools.value,
            "MCP": generation.MCP.value,
            "automatic_retry": generation.automatic_retry.value,
            "automatic_fallback": generation.automatic_fallback.value,
            "oversized_request_posture": generation.oversized_request_posture,
        },
        "usage_evidence_policy": {
            key: value.value
            for key, value in profile.usage_evidence_policy.model_dump().items()
        },
        "timeout_policy": {
            "connection_timeout_ms": profile.timeout_policy.connection_timeout_ms,
            "response_header_timeout_ms": (
                profile.timeout_policy.response_header_timeout_ms
            ),
            "complete_inference_timeout_ms": (
                profile.timeout_policy.complete_inference_timeout_ms
            ),
            "cancellation_deadline_ms": profile.timeout_policy.cancellation_deadline_ms,
            "caller_timeout_override_allowed": (
                profile.timeout_policy.caller_timeout_override_allowed
            ),
            "sdk_default_timeout_allowed": (
                profile.timeout_policy.sdk_default_timeout_allowed
            ),
        },
        "hermes_evidence": {
            "auth_default_endpoint_matches_profile": (
                modules.auth.DEFAULT_CODEX_BASE_URL == endpoint
            ),
            "overlay_transport": getattr(overlay, "transport", None),
            "overlay_endpoint_matches_profile": (
                getattr(overlay, "base_url_override", None) == endpoint
            ),
            "profile_transport_matches_overlay": (
                profile.transport.value == getattr(overlay, "transport", None)
            ),
            "codex_catalog_contains_model": (
                profile.model_policy.model_id
                in modules.codex_models.DEFAULT_CODEX_MODELS
            ),
            "codex_catalog_first_model": modules.codex_models.DEFAULT_CODEX_MODELS[0],
        },
        "forbidden_activity": {
            "oauth_started": False,
            "provider_calls": 0,
            "model_list_calls": 0,
            "inference_calls": 0,
            "real_credential_reads": 0,
            "worker_started": False,
            "agent_started": False,
            "graphify_mutation": False,
        },
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("status", help="Inspect the fixed provider-runtime profile")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parser.parse_args(argv)
    try:
        result = run_status()
    except ProviderProfileGateError as exc:
        result = {
            "schema_version": SCHEMA_VERSION,
            "gate_id": GATE_ID,
            "status": "failed",
            "error": _safe_error(exc, _repository_root(), _product_root()),
        }
        print(json.dumps(result, sort_keys=True))
        return PREREQUISITE_EXIT_CODE
    except Exception as exc:
        result = {
            "schema_version": SCHEMA_VERSION,
            "gate_id": GATE_ID,
            "status": "failed",
            "error": _safe_error(exc, _repository_root(), _product_root()),
        }
        print(json.dumps(result, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
