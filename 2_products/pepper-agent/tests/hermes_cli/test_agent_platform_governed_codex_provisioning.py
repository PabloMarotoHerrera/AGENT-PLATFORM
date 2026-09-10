from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform.auth_commands import agent_platform_command
from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_INTERNAL_LABEL,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.execution_profile_provisioning import (
    PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
)
from hermes_cli.agent_platform.provider_credentials.provisioning import (
    GovernedCodexProvisioningError,
    OPENAI_CODEX_PRIMARY_PROVISION_COMMAND,
    provision_openai_codex_primary,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionReport,
    default_openai_codex_credential_store_root,
    promote_openai_codex_oauth_credential,
)
from hermes_cli.subcommands.agent_platform import build_agent_platform_parser


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _absolute_preserving_symlink(path: Path) -> str:
    return os.path.abspath(os.fspath(path))


def _symlinked_python(tmp_path: Path) -> tuple[Path, Path]:
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    real_python = real_dir / "python3"
    real_python.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    real_python.chmod(0o755)
    venv_bin = tmp_path / "venv" / "bin"
    venv_bin.mkdir(parents=True)
    venv_python = venv_bin / "python"
    try:
        venv_python.symlink_to(real_python)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")
    return venv_python, real_python


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


def synthetic_access_token(
    *, issued_at: datetime = NOW, exp_delta: timedelta = timedelta(hours=1)
) -> str:
    payload = {
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + exp_delta).timestamp()),
    }
    body = (
        base64
        .urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        .decode("ascii")
        .rstrip("=")
    )
    return "header." + body + ".signature"


def synthetic_credential(
    *,
    issued_at: datetime = NOW,
    expires_delta: timedelta = timedelta(hours=1),
    refresh_token: str = "synthetic-refresh-token",
) -> OpenAICodexOAuthCredential:
    return OpenAICodexOAuthCredential(
        access_token=synthetic_access_token(
            issued_at=issued_at, exp_delta=expires_delta
        ),
        refresh_token=refresh_token,
        last_refresh_utc=issued_at,
        expires_at_utc=issued_at + expires_delta,
    )


def write_acquisition_payload(
    env: dict[str, str],
    *,
    issued_at: datetime = NOW,
    exp_delta: timedelta = timedelta(hours=1),
    refresh_token: str = "synthetic-refresh-token",
) -> str:
    access_token = synthetic_access_token(issued_at=issued_at, exp_delta=exp_delta)
    acquisition_home = Path(env["HERMES_HOME"])
    acquisition_home.mkdir(parents=True, exist_ok=True)
    (acquisition_home / "auth.json").write_text(
        json.dumps({
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
                        "refresh_token": refresh_token,
                        "base_url": OPENAI_CODEX_PROVIDER_ENDPOINT,
                        "last_refresh": issued_at.isoformat().replace("+00:00", "Z"),
                    }
                ]
            },
            "updated_at": issued_at.isoformat().replace("+00:00", "Z"),
        }),
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
    authoritative_python, real_python = _symlinked_python(tmp_path)

    def fake_executor(argv, env, cwd):
        calls.append((tuple(argv), dict(env), cwd))
        acquired["access_token"] = write_acquisition_payload(env)
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")

    status = provision_openai_codex_primary(
        product_root=product_root,
        acquisition_root=tmp_path / "acquisition",
        python_executable=authoritative_python,
        executor=fake_executor,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    governed_auth_file = default_openai_codex_credential_store_root() / "auth.json"
    payload = json.loads(governed_auth_file.read_text(encoding="utf-8"))
    entry = payload["credential_pool"]["openai-codex"][0]

    assert status.configured is True
    assert calls[0][0][0] == _absolute_preserving_symlink(authoritative_python)
    assert calls[0][0][0] != str(real_python.resolve(strict=False))
    assert calls[0][0][1:] == (
        "-m",
        "hermes_cli.main",
        "auth",
        "add",
        "openai-codex",
        "--type",
        "oauth",
    )
    assert calls[0][2] == product_root.resolve(strict=False)
    assert calls[0][1]["HERMES_HOME"] == str(
        (tmp_path / "acquisition").resolve(strict=False) / "home"
    )
    assert calls[0][1]["HOME"] == calls[0][1]["HERMES_HOME"]
    assert calls[0][1]["USERPROFILE"] == calls[0][1]["HERMES_HOME"]
    assert calls[0][1]["APPDATA"] == str(
        (tmp_path / "acquisition").resolve(strict=False) / "appdata"
    )
    assert calls[0][1]["LOCALAPPDATA"] == str(
        (tmp_path / "acquisition").resolve(strict=False) / "localappdata"
    )
    assert not (home / "auth.json").exists()
    assert governed_auth_file.is_file()
    assert payload["providers"] == {}
    assert payload["active_provider"] == "openai-codex"
    assert payload["suppressed_sources"] == {"openai-codex": ["device_code"]}
    assert entry["id"] == OPENAI_CODEX_CREDENTIAL_STORE_ID
    assert entry["label"] == OPENAI_CODEX_INTERNAL_LABEL
    assert entry["base_url"] == OPENAI_CODEX_PROVIDER_ENDPOINT
    assert entry["access_token"] == acquired["access_token"]


def test_governed_provisioning_rotates_expired_primary_store(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    governed_root = default_openai_codex_credential_store_root()
    promote_openai_codex_oauth_credential(
        governed_root,
        synthetic_credential(refresh_token="synthetic-refresh-token-old"),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )
    governed_auth_file = governed_root / "auth.json"
    original = governed_auth_file.read_text(encoding="utf-8")
    rotation_now = NOW + timedelta(hours=2)
    acquired: dict[str, str] = {}

    def fake_executor(_argv, env, _cwd):
        acquired["access_token"] = write_acquisition_payload(
            env,
            issued_at=rotation_now,
            refresh_token="synthetic-refresh-token-rotated",
        )
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")

    status = provision_openai_codex_primary(
        product_root=product_root,
        acquisition_root=tmp_path / "acquisition",
        python_executable=Path(sys.executable),
        executor=fake_executor,
        protection_backend=FakeProtectionBackend(),
        now=rotation_now,
    )
    payload = json.loads(governed_auth_file.read_text(encoding="utf-8"))
    entry = payload["credential_pool"]["openai-codex"][0]

    assert original != governed_auth_file.read_text(encoding="utf-8")
    assert status.configured is True
    assert status.durable_store_valid is True
    assert entry["access_token"] == acquired["access_token"]
    assert entry["refresh_token"] == "synthetic-refresh-token-rotated"


def test_governed_provisioning_failure_remains_fail_closed_without_promotion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    calls: list[tuple[tuple[str, ...], dict[str, str], Path]] = []
    authoritative_python = Path(sys.executable)

    def failing_executor(argv, env, cwd):
        calls.append((tuple(argv), dict(env), cwd))
        return SimpleNamespace(returncode=17, stdout=b"token=redacted", stderr=b"")

    with pytest.raises(GovernedCodexProvisioningError) as exc_info:
        provision_openai_codex_primary(
            product_root=product_root,
            acquisition_root=tmp_path / "acquisition",
            python_executable=authoritative_python,
            executor=failing_executor,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    governed_auth_file = default_openai_codex_credential_store_root() / "auth.json"
    assert exc_info.value.validation_category == "oauth_acquisition_failed"
    assert "token=redacted" not in str(exc_info.value)
    assert calls[0][0][0] == _absolute_preserving_symlink(authoritative_python)
    assert not governed_auth_file.exists()


def test_governed_provisioning_failure_preserves_existing_durable_store(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    governed_root = default_openai_codex_credential_store_root()
    promote_openai_codex_oauth_credential(
        governed_root,
        synthetic_credential(refresh_token="synthetic-refresh-token-old"),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )
    governed_auth_file = governed_root / "auth.json"
    original = governed_auth_file.read_text(encoding="utf-8")

    def failing_executor(_argv, _env, _cwd):
        return SimpleNamespace(returncode=17, stdout=b"", stderr=b"")

    with pytest.raises(GovernedCodexProvisioningError) as exc_info:
        provision_openai_codex_primary(
            product_root=product_root,
            acquisition_root=tmp_path / "acquisition",
            python_executable=Path(sys.executable),
            executor=failing_executor,
            protection_backend=FakeProtectionBackend(),
            now=NOW + timedelta(hours=2),
        )

    assert exc_info.value.validation_category == "oauth_acquisition_failed"
    assert governed_auth_file.read_text(encoding="utf-8") == original


def test_agent_platform_parser_accepts_only_governed_codex_profile() -> None:
    parser = argparse.ArgumentParser(prog="hermes")
    subparsers = parser.add_subparsers(dest="command")
    build_agent_platform_parser(subparsers, cmd_agent_platform=agent_platform_command)

    args = parser.parse_args(["agent-platform", "auth", "add", "openai-codex.primary"])

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

    args = parser.parse_args([
        "agent-platform",
        "profile",
        "status",
        "pepper-implementation-product",
    ])

    assert args.command == "agent-platform"
    assert args.agent_platform_action == "profile"
    assert args.agent_platform_profile_action == "status"
    assert args.profile == PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME
