from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_INTERNAL_LABEL,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials import store
from hermes_cli.agent_platform.provider_credentials.store import (
    ExistingProviderCredentialStoreError,
    InvalidProviderCredentialStoreError,
    ProviderCredentialStoreProtectionError,
    clear_local_openai_codex_credential,
    promote_openai_codex_oauth_credential,
    read_openai_codex_credential_status,
    validate_windows_dacl_principals,
)


SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_credentials"
    / "store.py"
)


class FakeProtectionBackend:
    def __init__(self, *, fail_stage_file: bool = False) -> None:
        self.fail_stage_file = fail_stage_file
        self.calls: list[tuple[str, str]] = []

    def prepare_directory(self, path: Path):
        self.calls.append(("prepare_directory", path.name))
        path.mkdir(parents=True, exist_ok=True)
        return store.StoreProtectionReport("store_directory", "test", True)

    def prepare_file(self, path: Path):
        self.calls.append(("prepare_file", path.name))
        if self.fail_stage_file and ".agent-platform-store-stage." in str(path.parent):
            raise ProviderCredentialStoreProtectionError(
                validation_category="synthetic_stage_failure"
            )
        return store.StoreProtectionReport("auth_file", "test", True)

    def validate_directory(self, path: Path):
        self.calls.append(("validate_directory", path.name))
        if not path.is_dir():
            raise ProviderCredentialStoreProtectionError(
                validation_category="missing_directory"
            )
        return store.StoreProtectionReport("store_directory", "test", True)

    def validate_file(self, path: Path):
        self.calls.append(("validate_file", path.name))
        if not path.is_file():
            raise ProviderCredentialStoreProtectionError(
                validation_category="missing_file"
            )
        return store.StoreProtectionReport("auth_file", "test", True)


def synthetic_credential(
    *, expires_delta: timedelta = timedelta(hours=1)
) -> OpenAICodexOAuthCredential:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return OpenAICodexOAuthCredential(
        access_token="synthetic-access-token",
        refresh_token="synthetic-refresh-token",
        last_refresh_utc=now,
        expires_at_utc=now + expires_delta,
    )


def test_status_for_missing_store_is_secret_free_and_read_only(tmp_path: Path) -> None:
    trusted_root = tmp_path / "dedicated-store"
    status = read_openai_codex_credential_status(
        trusted_root,
        protection_backend=FakeProtectionBackend(),
    )

    assert status.configured is False
    assert status.durable_store_present is False
    assert status.credential_count == 0
    assert not (trusted_root / "auth.json").exists()
    assert "synthetic" not in repr(status)


def test_promote_creates_exact_single_credential_store_and_clear_is_local_only(
    tmp_path: Path,
) -> None:
    trusted_root = tmp_path / "dedicated-store"
    fake = FakeProtectionBackend()
    status = promote_openai_codex_oauth_credential(
        trusted_root,
        synthetic_credential(),
        protection_backend=fake,
    )
    payload = json.loads((trusted_root / "auth.json").read_text(encoding="utf-8"))

    assert status.configured is True
    assert status.credential_count == 1
    assert status.protection_valid is True
    assert set(payload["providers"]) == {"openai-codex"}
    assert set(payload["credential_pool"]) == {"openai-codex"}
    assert payload["active_provider"] == "openai-codex"
    provider_state = payload["providers"]["openai-codex"]
    assert provider_state["auth_mode"] == "chatgpt"
    assert provider_state["label"] == OPENAI_CODEX_INTERNAL_LABEL
    assert provider_state["base_url"] == OPENAI_CODEX_PROVIDER_ENDPOINT
    assert provider_state["credential_store_id"] == OPENAI_CODEX_CREDENTIAL_STORE_ID
    pool_entries = payload["credential_pool"]["openai-codex"]
    assert len(pool_entries) == 1
    assert pool_entries[0]["id"] == OPENAI_CODEX_CREDENTIAL_STORE_ID
    assert pool_entries[0]["source"] == "manual:device_code"
    assert pool_entries[0]["priority"] == 0
    assert any(call[0] == "prepare_file" for call in fake.calls)

    clear_result = clear_local_openai_codex_credential(
        trusted_root,
        protection_backend=fake,
    )
    assert clear_result.local_store_present_after is False
    assert clear_result.remote_revocation == "not_supported_or_unverified"
    assert not (trusted_root / "auth.json").exists()


def test_existing_durable_store_is_rejected_without_overwrite(tmp_path: Path) -> None:
    trusted_root = tmp_path / "dedicated-store"
    trusted_root.mkdir()
    auth_file = trusted_root / "auth.json"
    original = '{"preexisting": true}\n'
    auth_file.write_text(original, encoding="utf-8")

    with pytest.raises(ExistingProviderCredentialStoreError):
        promote_openai_codex_oauth_credential(
            trusted_root,
            synthetic_credential(),
            protection_backend=FakeProtectionBackend(),
        )

    assert auth_file.read_text(encoding="utf-8") == original


def test_unrelated_provider_and_multiple_codex_credentials_are_rejected(
    tmp_path: Path,
) -> None:
    fake = FakeProtectionBackend()
    unrelated_root = tmp_path / "unrelated"
    promote_openai_codex_oauth_credential(
        unrelated_root,
        synthetic_credential(),
        protection_backend=fake,
    )
    payload = json.loads((unrelated_root / "auth.json").read_text(encoding="utf-8"))
    unrelated_access_token = "synthetic-unrelated-token"
    payload["providers"]["anthropic"] = {
        "tokens": {"access_token": unrelated_access_token}
    }
    (unrelated_root / "auth.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidProviderCredentialStoreError):
        read_openai_codex_credential_status(unrelated_root, protection_backend=fake)

    multiple_root = tmp_path / "multiple"
    promote_openai_codex_oauth_credential(
        multiple_root,
        synthetic_credential(),
        protection_backend=fake,
    )
    payload = json.loads((multiple_root / "auth.json").read_text(encoding="utf-8"))
    payload["credential_pool"]["openai-codex"].append({
        **payload["credential_pool"]["openai-codex"][0],
        "id": "second",
    })
    (multiple_root / "auth.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidProviderCredentialStoreError):
        read_openai_codex_credential_status(multiple_root, protection_backend=fake)


def test_failed_staging_validation_leaves_no_store_or_stage_residue(
    tmp_path: Path,
) -> None:
    trusted_root = tmp_path / "dedicated-store"

    with pytest.raises(ProviderCredentialStoreProtectionError):
        promote_openai_codex_oauth_credential(
            trusted_root,
            synthetic_credential(),
            protection_backend=FakeProtectionBackend(fail_stage_file=True),
        )

    assert not (trusted_root / "auth.json").exists()
    assert not list(trusted_root.glob(".agent-platform-store-stage.*"))


def test_windows_dacl_policy_rejects_broad_or_unknown_principals() -> None:
    current = "S-1-5-21-1000"
    report = validate_windows_dacl_principals(
        {current, "S-1-5-18"}, current_user_sid=current
    )
    assert report.protected is True
    for forbidden in ("S-1-1-0", "S-1-5-11", "S-1-5-32-545"):
        with pytest.raises(ProviderCredentialStoreProtectionError):
            validate_windows_dacl_principals(
                {current, forbidden}, current_user_sid=current
            )
    with pytest.raises(ProviderCredentialStoreProtectionError):
        validate_windows_dacl_principals(
            {current, "S-1-5-21-unknown"}, current_user_sid=current
        )
    with pytest.raises(ProviderCredentialStoreProtectionError):
        validate_windows_dacl_principals({"S-1-5-18"}, current_user_sid=current)


def test_store_source_has_no_real_credential_or_merge_authority() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "Path.home",
        "os.getenv",
        ".codex",
        "webbrowser",
        "subprocess",
        "_codex_device_code_login",
        "resolve_codex_runtime_credentials",
        "read_credential_pool",
        "write_credential_pool",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source
    assert "durable_store_exists" in source
    assert "credential_count_not_one" in source
    assert "windows_forbidden_principal" in source
