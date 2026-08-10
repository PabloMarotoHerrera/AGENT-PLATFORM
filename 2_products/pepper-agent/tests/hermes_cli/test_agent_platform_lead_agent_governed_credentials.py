from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform.lead_agent import (
    PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE,
    PEPPER_LEAD_AGENT_MODEL,
    PEPPER_LEAD_AGENT_PROVIDER,
    PEPPER_LEAD_AGENT_SOURCE,
    PepperLeadAgentProviderUnavailable,
    resolve_pepper_lead_agent_runtime,
)
from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials.provisioning import (
    read_openai_codex_primary_status,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionReport,
    default_openai_codex_credential_store_root,
    promote_openai_codex_oauth_credential,
)


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


def synthetic_access_token(*, exp_delta: timedelta = timedelta(hours=1)) -> str:
    payload = {
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + exp_delta).timestamp()),
    }
    body = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return "header." + body + ".signature"


def write_governed_store(root: Path) -> str:
    access_token = synthetic_access_token()
    promote_openai_codex_oauth_credential(
        root,
        OpenAICodexOAuthCredential(
            access_token=access_token,
            refresh_token="synthetic-refresh-token",
            last_refresh_utc=NOW,
            expires_at_utc=NOW + timedelta(hours=1),
        ),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )
    return access_token


def test_pepper_runtime_resolves_governed_primary_without_legacy_auth(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    root = default_openai_codex_credential_store_root()
    access_token = write_governed_store(root)

    runtime = resolve_pepper_lead_agent_runtime(
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert runtime["provider"] == PEPPER_LEAD_AGENT_PROVIDER
    assert runtime["model"] == PEPPER_LEAD_AGENT_MODEL
    assert runtime["base_url"] == OPENAI_CODEX_PROVIDER_ENDPOINT
    assert runtime["api_key"] == access_token
    assert runtime["api_mode"] == "codex_responses"
    assert runtime["source"] == PEPPER_LEAD_AGENT_SOURCE
    assert runtime["credential_profile_id"] == PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE
    assert runtime["provider_runtime_profile_id"] == (
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert runtime["worker_profile_id"] == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert not (home / "auth.json").exists()
    assert "credential_pool" not in runtime


def test_status_cli_helper_and_pepper_runtime_share_governed_store(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    access_token = write_governed_store(default_openai_codex_credential_store_root())

    status = read_openai_codex_primary_status(
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )
    runtime = resolve_pepper_lead_agent_runtime(
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert status.configured is True
    assert status.durable_store_valid is True
    assert status.token_pair_present is True
    assert status.credential_ref.store_id == PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE
    assert runtime["credential_profile_id"] == status.credential_ref.store_id
    assert runtime["api_key"] == access_token
    assert not (home / "auth.json").exists()


def test_pepper_runtime_ignores_legacy_auth_json_when_governed_store_absent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    home.mkdir(parents=True)
    (home / "auth.json").write_text(
        json.dumps(
            {
                "version": 1,
                "active_provider": "openai-codex",
                "providers": {},
                "credential_pool": {
                    "openai-codex": [
                        {
                            "id": "legacy",
                            "label": "legacy",
                            "auth_type": "oauth",
                            "priority": 0,
                            "source": "manual:device_code",
                            "access_token": synthetic_access_token(),
                            "refresh_token": "legacy-refresh-token",
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

    with pytest.raises(PepperLeadAgentProviderUnavailable) as exc_info:
        resolve_pepper_lead_agent_runtime(now=NOW)

    assert exc_info.value.validation_category == "governed_credential_absent"
    assert not default_openai_codex_credential_store_root().exists()


def test_pepper_runtime_ignores_openai_api_key_when_governed_store_absent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes-home"))
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-openai-api-key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "synthetic-openrouter-api-key")

    with pytest.raises(PepperLeadAgentProviderUnavailable) as exc_info:
        resolve_pepper_lead_agent_runtime(now=NOW)

    assert exc_info.value.validation_category == "governed_credential_absent"
