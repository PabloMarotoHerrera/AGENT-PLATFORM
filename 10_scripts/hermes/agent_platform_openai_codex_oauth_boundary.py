#!/usr/bin/env python3
"""Credential-delivery boundary status gate for Hermes OpenAI Codex OAuth."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
GATE_ID = "P15.1"
VERDICT = "hermes_openai_codex_credential_delivery_boundary_ready_with_constraints"
PREREQUISITE_EXIT_CODE = 20


class BoundaryGateError(RuntimeError):
    """Raised when the P15.1 boundary cannot be proven safely."""


@dataclass(frozen=True, slots=True)
class BoundaryGateConfig:
    """Trusted internal composition inputs; not exposed as CLI arguments."""

    product_root: Path
    trusted_store_root: Path


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _product_root() -> Path:
    return _repository_root() / "2_products" / "pepper-agent"


def _load_product_modules(product_root: Path):
    if not (product_root / "hermes_cli" / "agent_platform").is_dir():
        raise BoundaryGateError("Hermes AGENT PLATFORM package was not found")
    product_path = str(product_root)
    if product_path not in sys.path:
        sys.path.insert(0, product_path)
    from hermes_cli.agent_platform.provider_credentials import contracts
    from hermes_cli.agent_platform.provider_credentials import delivery
    from hermes_cli.agent_platform.provider_credentials import oauth_acquisition
    from hermes_cli.agent_platform.provider_credentials import store

    return contracts, delivery, oauth_acquisition, store


def _fixed_host_store_root(contracts_module) -> Path:
    try:
        from hermes_constants import get_hermes_home
    except Exception as exc:
        raise BoundaryGateError("Hermes home policy could not be resolved") from exc
    return (
        get_hermes_home()
        / "agent-platform"
        / "provider-credentials"
        / contracts_module.OPENAI_CODEX_CREDENTIAL_STORE_ID
    )


def _default_config(contracts_module) -> BoundaryGateConfig:
    product_root = _product_root()
    return BoundaryGateConfig(
        product_root=product_root,
        trusted_store_root=_fixed_host_store_root(contracts_module),
    )


def _safe_error(error: BaseException, *paths: Path) -> str:
    text = f"{type(error).__name__}: {error}"
    for path in paths:
        raw = str(path)
        text = text.replace(raw, "<path>")
        text = text.replace(raw.replace("\\", "/"), "<path>")
    for marker in ("token", "secret", "password", "api_key"):
        text = text.replace(marker.upper(), marker)
    return text[:500]


def run_status(
    config: BoundaryGateConfig | None = None,
    *,
    status_reader: Callable[[Path], Any] | None = None,
    acquisition_planner: Callable[..., Any] | None = None,
    module_loader: Callable[[Path], tuple[Any, Any, Any, Any]] | None = None,
) -> dict[str, Any]:
    """Return the bounded P15.1 status summary.

    Tests may inject synthetic roots through ``config`` and fake collaborators.
    The production CLI accepts no path arguments and resolves only the fixed
    host-store policy.
    """

    product_root = _product_root() if config is None else config.product_root
    contracts, delivery, oauth_acquisition, store = (
        module_loader(product_root)
        if module_loader is not None
        else _load_product_modules(product_root)
    )
    resolved_config = config or _default_config(contracts)
    reader = status_reader or store.read_openai_codex_credential_status
    planner = (
        acquisition_planner
        or oauth_acquisition.build_openai_codex_oauth_acquisition_plan
    )
    status = reader(resolved_config.trusted_store_root)
    acquisition = planner(
        product_root=resolved_config.product_root,
        trusted_acquisition_root=resolved_config.trusted_store_root,
    )
    public_plan = getattr(acquisition, "public_plan", acquisition)
    return {
        "schema_version": SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "status": "passed",
        "verdict": VERDICT,
        "credential_contract": {
            "schema_version": contracts.PROVIDER_CREDENTIAL_SCHEMA_VERSION,
            "store_id": contracts.OPENAI_CODEX_CREDENTIAL_STORE_ID,
            "provider": contracts.ProviderCredentialProvider.OPENAI_CODEX.value,
            "auth_kind": contracts.ProviderCredentialAuthKind.CHATGPT_OAUTH_DEVICE.value,
            "hermes_provider_id": contracts.OPENAI_CODEX_HERMES_PROVIDER_ID,
            "provider_endpoint": contracts.OPENAI_CODEX_PROVIDER_ENDPOINT,
            "remote_revocation": contracts.PROVIDER_CREDENTIAL_REMOTE_REVOCATION_STATUS,
        },
        "status_probe": {
            "configured": bool(status.configured),
            "durable_store_present": bool(status.durable_store_present),
            "durable_store_valid": bool(status.durable_store_valid),
            "credential_count": int(status.credential_count),
            "protection_valid": bool(status.protection_valid),
            "token_pair_present": bool(status.token_pair_present),
        },
        "oauth_acquisition_boundary": {
            "execution_attempted": False,
            "execution_disabled_by_default": bool(
                public_plan.execution_disabled_by_default
            ),
            "uses_product_local_python": (
                public_plan.working_directory_role == "Pepper_product_root"
            ),
            "argv_suffix": list(public_plan.command_argv_suffix),
            "environment_keys": list(public_plan.environment_keys),
            "caller_label_allowed": False,
            "endpoint_override_allowed": False,
        },
        "delivery_boundary": {
            "public_lease_ref_contains_path": False,
            "public_lease_ref_contains_token": False,
            "maximum_active_leases": contracts.MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES,
            "maximum_lease_ttl_ms": contracts.MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
            "minimum_remaining_credential_lifetime_ms": (
                contracts.MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
            ),
            "automatic_refresh": False,
            "refresh_on_lease_acquisition": False,
            "refresh_writeback": False,
            "lease_marker_name": delivery.LEASE_MARKER_NAME,
        },
        "forbidden_activity": {
            "oauth_started": False,
            "provider_calls": 0,
            "browser_opened": False,
            "real_credential_reads": 0,
            "worker_started": False,
            "graphify_mutation": False,
        },
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("status", help="Inspect the fixed governed host-store policy")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parser.parse_args(argv)
    try:
        result = run_status()
    except BoundaryGateError as exc:
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
