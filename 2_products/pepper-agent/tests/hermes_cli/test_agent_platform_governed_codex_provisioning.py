from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform.auth_commands import agent_platform_command
from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_INTERNAL_LABEL,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
)
from hermes_cli.agent_platform.execution_profile_provisioning import (
    PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
)
from hermes_cli.agent_platform.provider_credentials.provisioning import (
    OPENAI_CODEX_PRIMARY_PROVISION_COMMAND,
    provision_openai_codex_primary,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionReport,
    default_openai_codex_credential_store_root,
)
from hermes_cli.subcommands.agent_platform import build_agent_platform_parser


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


class FakeProtectionBackend:
    def prepare_directory(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return StoreProtectionReport("store_directory", "test", True)

    def prepare_file(self, path: Path):
        return StoreProtectionReport("auth_file", "test", True)

    def validate_directory(self, path: Path):
        if not path.is_dir():
            raise AssertionError("missing directory")
        return StoreProtectionReport("store_directory", "test", True)

    def validate_file(self, path: Path):
        if not path.is_file():
            raise AssertionError("missing file")
        return StoreProtectionReport("auth_file", "test", True)


def synthetic_access_token() -> str:
    payload = {
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + timedelta(hours=1)).timestamp()),
    }
    body = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return "header." + body + ".signature"


def write_acquisition_payload(env: dict[str, str]) -> str:
    access_token = synthetic_access_token()
    acquisition_home = Path(env["HERMES_HOME"])
    acquisition_home.mkdir(parents=True, exist_ok=True)
    (acquisition_home / "auth.json").write_text(
        json.dumps(
            {
                "version": 1,
                "active_provider": "openai-codex",
                "providers": {},
                "credential_pool": {
                    "openai-codex": [
                        {
                            "id": "source",
                            "label": "source-derived",
                            "auth_type": "oauth",
                            "priority": 0,
                            "source": "manual:device_code",
                            "access_token": access_token,
                            "refresh_token": "synthetic-refresh-token",
                            "base_url": OPENAI_CODEX_PROVIDER_ENDPOINT,
                            "last_refresh": NOW.isoformat().replace("+00:00", "Z"),
                        }
                    ]
                },
                "updated_at": NOW.isoformat().replace("+00:00", "Z"),
            }
        ),
        encoding="utf-8",
    )
    return access_token


def test_governed_provisioning_promotes_isolated_acquisition_to_primary_store(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    calls: list[tuple[tuple[str, ...], dict[str, str], Path]] = []
    acquired: dict[str, str] = {}

    def fake_executor(argv, env, cwd):
        calls.append((tuple(argv), dict(env), cwd))
        acquired["access_token"] = write_acquisition_payload(env)
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")

    status = provision_openai_codex_primary(
        product_root=product_root,
        acquisition_root=tmp_path / "acquisition",
        executor=fake_executor,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    governed_auth_file = default_openai_codex_credential_store_root() / "auth.json"
    payload = json.loads(governed_auth_file.read_text(encoding="utf-8"))
    entry = payload["credential_pool"]["openai-codex"][0]

    assert status.configured is True
    assert calls[0][0] == (
        "python",
        "-m",
        "hermes_cli.main",
        "auth",
        "add",
        "openai-codex",
        "--type",
        "oauth",
    )
    assert calls[0][2] == product_root.resolve(strict=False)
    assert not (home / "auth.json").exists()
    assert governed_auth_file.is_file()
    assert payload["providers"] == {}
    assert payload["active_provider"] == "openai-codex"
    assert payload["suppressed_sources"] == {"openai-codex": ["device_code"]}
    assert entry["id"] == OPENAI_CODEX_CREDENTIAL_STORE_ID
    assert entry["label"] == OPENAI_CODEX_INTERNAL_LABEL
    assert entry["base_url"] == OPENAI_CODEX_PROVIDER_ENDPOINT
    assert entry["access_token"] == acquired["access_token"]


def test_agent_platform_parser_accepts_only_governed_codex_profile() -> None:
    parser = argparse.ArgumentParser(prog="hermes")
    subparsers = parser.add_subparsers(dest="command")
    build_agent_platform_parser(subparsers, cmd_agent_platform=agent_platform_command)

    args = parser.parse_args(
        ["agent-platform", "auth", "add", "openai-codex.primary"]
    )

    assert args.command == "agent-platform"
    assert args.agent_platform_action == "auth"
    assert args.agent_platform_auth_action == "add"
    assert args.profile == "openai-codex.primary"
    assert OPENAI_CODEX_PRIMARY_PROVISION_COMMAND == (
        "hermes agent-platform auth add openai-codex.primary"
    )


def test_agent_platform_parser_accepts_governed_implementation_profile() -> None:
    parser = argparse.ArgumentParser(prog="hermes")
    subparsers = parser.add_subparsers(dest="command")
    build_agent_platform_parser(subparsers, cmd_agent_platform=agent_platform_command)

    args = parser.parse_args(
        [
            "agent-platform",
            "profile",
            "status",
            "pepper-implementation-product",
        ]
    )

    assert args.command == "agent-platform"
    assert args.agent_platform_action == "profile"
    assert args.agent_platform_profile_action == "status"
    assert args.profile == PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME
