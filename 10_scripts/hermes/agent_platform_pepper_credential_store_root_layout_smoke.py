#!/usr/bin/env python3
"""Synthetic Pepper credential-store root-layout smoke."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
VERDICT = "pepper_credential_store_root_layout_smoke_passed"
CONFLICT_CATEGORY = "ambiguous_canonical_and_legacy_credential_store_roots"


class RootLayoutSmokeError(RuntimeError):
    """Raised when the synthetic root-layout smoke cannot prove readiness."""


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _product_root() -> Path:
    return _repository_root() / "2_products" / "pepper-agent"


def _load_store_module():
    product_root = _product_root()
    if not (product_root / "hermes_cli" / "agent_platform").is_dir():
        raise RootLayoutSmokeError("Pepper AGENT PLATFORM package was not found")
    product_path = str(product_root)
    if product_path not in sys.path:
        sys.path.insert(0, product_path)
    from hermes_cli.agent_platform.provider_credentials import store

    return store


def _relative_parts(root: Path, hermes_home: Path) -> tuple[str, ...]:
    return root.relative_to(hermes_home).parts


def _remove_empty_upward(path: Path, stop: Path) -> None:
    current = path
    while current != stop and current.exists():
        current.rmdir()
        current = current.parent


def _build_status() -> dict[str, Any]:
    store = _load_store_module()
    temp_removed = False
    with tempfile.TemporaryDirectory(
        prefix="agent-platform-p15c2-root-layout-"
    ) as directory:
        temp_root = Path(directory)
        hermes_home = temp_root / "hermes-home"
        canonical_root = store._canonical_openai_codex_credential_store_root(
            hermes_home
        )
        legacy_root = store._legacy_duplicated_openai_codex_credential_store_root(
            hermes_home
        )
        canonical_parts = _relative_parts(canonical_root, hermes_home)
        legacy_parts = _relative_parts(legacy_root, hermes_home)

        selected_absent = store.default_openai_codex_credential_store_root(hermes_home)
        created_by_resolver = canonical_root.exists() or legacy_root.exists()
        canonical_root.mkdir(parents=True)
        selected_canonical = store.default_openai_codex_credential_store_root(
            hermes_home
        )
        _remove_empty_upward(canonical_root, hermes_home)
        legacy_root.mkdir(parents=True)
        selected_legacy = store.default_openai_codex_credential_store_root(hermes_home)
        canonical_root.mkdir(parents=True)
        failure_category = ""
        fail_closed = False
        try:
            store.default_openai_codex_credential_store_root(hermes_home)
        except store.InvalidProviderCredentialStoreRootError as exc:
            failure_category = exc.validation_category
            fail_closed = failure_category == CONFLICT_CATEGORY
    temp_removed = not temp_root.exists()

    canonical_duplicate_segments = max(canonical_parts.count("agent-platform") - 1, 0)
    canonical_duplicate_segments += max(
        canonical_parts.count("provider-credentials") - 1, 0
    )
    result = {
        "schema_version": SCHEMA_VERSION,
        "verdict": VERDICT,
        "canonical_layout": {
            "exact_segments": canonical_parts
            == (
                "agent-platform",
                "provider-credentials",
                "openai-codex.primary",
            ),
            "duplicate_segments": canonical_duplicate_segments,
            "selected_when_absent": selected_absent == canonical_root,
            "selected_when_present": selected_canonical == canonical_root,
        },
        "legacy_layout": {
            "exact_segments": legacy_parts
            == (
                "agent-platform",
                "provider-credentials",
                "agent-platform",
                "provider-credentials",
                "openai-codex.primary",
            ),
            "selected_when_canonical_absent": selected_legacy == legacy_root,
            "created_by_resolver": created_by_resolver,
        },
        "ambiguous_layout": {
            "fail_closed": fail_closed,
            "failure_category": failure_category,
        },
        "temporary_root_removed": temp_removed,
        "runtime_residue": 0 if temp_removed else 1,
        "real_credential_reads": 0,
        "real_credential_writes": 0,
        "credential_copies": 0,
        "credential_moves": 0,
        "credential_deletes": 0,
        "OAuth_attempts": 0,
        "provider_calls": 0,
    }
    if not _result_passed(result):
        raise RootLayoutSmokeError("root layout smoke failed")
    return result


def _result_passed(result: dict[str, Any]) -> bool:
    return (
        result["canonical_layout"]["exact_segments"] is True
        and result["canonical_layout"]["duplicate_segments"] == 0
        and result["canonical_layout"]["selected_when_absent"] is True
        and result["canonical_layout"]["selected_when_present"] is True
        and result["legacy_layout"]["exact_segments"] is True
        and result["legacy_layout"]["selected_when_canonical_absent"] is True
        and result["legacy_layout"]["created_by_resolver"] is False
        and result["ambiguous_layout"]["fail_closed"] is True
        and result["temporary_root_removed"] is True
        and result["runtime_residue"] == 0
        and result["real_credential_reads"] == 0
        and result["real_credential_writes"] == 0
        and result["credential_copies"] == 0
        and result["credential_moves"] == 0
        and result["credential_deletes"] == 0
        and result["OAuth_attempts"] == 0
        and result["provider_calls"] == 0
    )


def _text_result(result: dict[str, Any]) -> str:
    return "\n".join(
        (
            f"verdict={result['verdict']}",
            f"canonical_exact_segments={result['canonical_layout']['exact_segments']}",
            f"canonical_duplicate_segments={result['canonical_layout']['duplicate_segments']}",
            f"legacy_selected={result['legacy_layout']['selected_when_canonical_absent']}",
            f"ambiguous_fail_closed={result['ambiguous_layout']['fail_closed']}",
            f"temporary_root_removed={result['temporary_root_removed']}",
            f"runtime_residue={result['runtime_residue']}",
        )
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        help="Output format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parsed = parser.parse_args(argv)
    try:
        result = _build_status()
    except Exception as exc:
        error = {
            "schema_version": SCHEMA_VERSION,
            "status": "failed",
            "error": type(exc).__name__,
        }
        print(
            json.dumps(error, sort_keys=True)
            if parsed.format == "json"
            else "status=failed"
        )
        return 1
    if parsed.format == "json":
        print(json.dumps(result, sort_keys=True))
    else:
        print(_text_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
