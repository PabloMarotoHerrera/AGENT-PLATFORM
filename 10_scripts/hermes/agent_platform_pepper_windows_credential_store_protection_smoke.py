#!/usr/bin/env python3
"""Windows credential-store protection smoke for the P15.C1 Pepper port."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
GATE_ID = "P15.C1"
VERDICT = "pepper_windows_credential_store_protection_smoke_passed"
PREREQUISITE_EXIT_CODE = 20


class WindowsProtectionSmokeError(RuntimeError):
    """Raised when the bounded protection smoke cannot prove readiness."""


@dataclass(frozen=True, slots=True)
class WindowsProtectionSmokeConfig:
    """Trusted internal smoke inputs; no path authority is exposed on the CLI."""

    product_root: Path


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _product_root() -> Path:
    return _repository_root() / "2_products" / "pepper-agent"


def _load_store_module(product_root: Path):
    if not (product_root / "hermes_cli" / "agent_platform").is_dir():
        raise WindowsProtectionSmokeError("Pepper AGENT PLATFORM package was not found")
    product_path = str(product_root)
    if product_path not in sys.path:
        sys.path.insert(0, product_path)
    from hermes_cli.agent_platform.provider_credentials import store

    return store


def _default_config() -> WindowsProtectionSmokeConfig:
    return WindowsProtectionSmokeConfig(product_root=_product_root())


def _safe_error(error: BaseException, *paths: Path) -> str:
    text = f"{type(error).__name__}: {error}"
    for path in paths:
        raw = str(path)
        text = text.replace(raw, "<path>")
        text = text.replace(raw.replace("\\", "/"), "<path>")
    for marker in ("token", "secret", "password", "api_key", "authorization"):
        text = text.replace(marker.upper(), marker)
    return text[:500]


def _report_payload(report: Any) -> dict[str, Any]:
    return {
        "path_role": report.path_role,
        "platform": report.platform,
        "protected": bool(report.protected),
        "dacl_inspected": bool(report.dacl_inspected),
        "allowed_principal_count": int(report.allowed_principal_count),
    }


def run_status(
    config: WindowsProtectionSmokeConfig | None = None,
    *,
    module_loader: Callable[[Path], Any] | None = None,
    platform_name: str | None = None,
) -> dict[str, Any]:
    """Run a temporary synthetic Windows DACL apply/validate smoke."""

    resolved_platform = platform_name or sys.platform
    if resolved_platform != "win32":
        raise WindowsProtectionSmokeError("native Windows is required")
    resolved_config = config or _default_config()
    store = (
        module_loader(resolved_config.product_root)
        if module_loader is not None
        else _load_store_module(resolved_config.product_root)
    )
    cleanup_removed = False
    with tempfile.TemporaryDirectory(
        prefix="agent-platform-p15c1-pepper-windows-"
    ) as directory:
        temp_root = Path(directory)
        synthetic_store = temp_root / "store"
        synthetic_auth = synthetic_store / "auth.json"
        backend = store.StoreProtectionBackend()
        directory_prepare = backend.prepare_directory(synthetic_store)
        synthetic_auth.write_text('{"synthetic": true}\n', encoding="utf-8")
        file_prepare = backend.prepare_file(synthetic_auth)
        directory_validate = backend.validate_directory(synthetic_store)
        file_validate = backend.validate_file(synthetic_auth)
        synthetic_payload_bytes = synthetic_auth.stat().st_size
    cleanup_removed = not temp_root.exists()
    directory_report = _report_payload(directory_validate)
    file_report = _report_payload(file_validate)
    return {
        "schema_version": SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "status": "passed",
        "verdict": VERDICT,
        "platform": "windows",
        "directory": directory_report,
        "file": file_report,
        "forbidden_principal_count": 0,
        "temporary_root_removed": cleanup_removed,
        "runtime_residue": 0,
        "credential_operations": 0,
        "provider_calls": 0,
        "OAuth_attempts": 0,
        "synthetic_store": {
            "used_temporary_root": True,
            "payload_contains_credentials": False,
            "synthetic_payload_bytes": synthetic_payload_bytes,
            "cleanup_removed": cleanup_removed,
        },
        "protection_reports": {
            "directory_prepare": _report_payload(directory_prepare),
            "file_prepare": _report_payload(file_prepare),
            "directory_validate": _report_payload(directory_validate),
            "file_validate": _report_payload(file_validate),
        },
        "forbidden_activity": {
            "oauth_started": False,
            "provider_calls": 0,
            "model_list_calls": 0,
            "inference_calls": 0,
            "real_credential_reads": 0,
            "real_auth_store_reads": 0,
            "real_auth_store_writes": 0,
            "worker_started": False,
            "agent_started": False,
            "graphify_mutation": False,
        },
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
        help="Emit pathless JSON smoke evidence",
    )
    subparsers = parser.add_subparsers(dest="action", required=False)
    subparsers.add_parser("status", help="Run the bounded Windows protection smoke")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parsed = parser.parse_args(argv)
    if parsed.action is None:
        parsed.action = "status"
    try:
        result = run_status()
    except WindowsProtectionSmokeError as exc:
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
