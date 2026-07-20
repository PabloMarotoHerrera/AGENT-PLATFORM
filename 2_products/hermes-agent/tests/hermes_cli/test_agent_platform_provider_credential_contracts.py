from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_credentials as pc


SOURCE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_credentials"
)


def test_contract_constants_and_enums_are_fixed_to_p15_openai_codex() -> None:
    assert pc.PROVIDER_CREDENTIAL_SCHEMA_VERSION == 1
    assert pc.OPENAI_CODEX_CREDENTIAL_STORE_ID == "openai-codex.primary"
    assert pc.OPENAI_CODEX_HERMES_PROVIDER_ID == "openai-codex"
    assert pc.OPENAI_CODEX_PROVIDER_ENDPOINT == "https://chatgpt.com/backend-api/codex"
    assert pc.MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES == 1
    assert pc.MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS == 900_000
    assert pc.MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS == 300_000
    assert (
        pc.PROVIDER_CREDENTIAL_REMOTE_REVOCATION_STATUS == "not_supported_or_unverified"
    )
    assert [member.value for member in pc.ProviderCredentialProvider] == [
        "openai_codex"
    ]
    assert [member.value for member in pc.ProviderCredentialAuthKind] == [
        "chatgpt_oauth_device"
    ]
    ref = pc.ProviderCredentialRef()
    assert ref.store_id == "openai-codex.primary"
    assert ref.provider is pc.ProviderCredentialProvider.OPENAI_CODEX
    assert ref.auth_kind is pc.ProviderCredentialAuthKind.CHATGPT_OAUTH_DEVICE


def test_secret_bearing_contract_is_frozen_strict_utc_and_redacted() -> None:
    now = datetime.now(timezone.utc)
    credential = pc.OpenAICodexOAuthCredential(
        access_token="synthetic-access-token",
        refresh_token="synthetic-refresh-token",
        last_refresh_utc=now,
        expires_at_utc=now + timedelta(hours=1),
    )

    assert credential.last_refresh_utc.tzinfo is timezone.utc
    assert "synthetic-access-token" not in repr(credential)
    assert "**********" in repr(credential)
    with pytest.raises(ValidationError):
        pc.OpenAICodexOAuthCredential(
            access_token="synthetic-access-token",
            refresh_token="synthetic-refresh-token",
            last_refresh_utc=datetime(2026, 1, 1),
            expires_at_utc=now + timedelta(hours=1),
        )
    with pytest.raises(ValidationError):
        pc.OpenAICodexOAuthCredential(
            access_token="synthetic-access-token",
            refresh_token="synthetic-refresh-token",
            last_refresh_utc=now,
            expires_at_utc=now + timedelta(hours=1),
            base_url="https://api.openai.com/v1",
        )
    with pytest.raises(ValidationError):
        pc.OpenAICodexOAuthCredential(
            access_token="synthetic\naccess-token",
            refresh_token="synthetic-refresh-token",
            last_refresh_utc=now,
            expires_at_utc=now + timedelta(hours=1),
        )
    with pytest.raises(ValidationError):
        pc.OpenAICodexOAuthCredential(
            access_token="synthetic-access-token",
            refresh_token="synthetic-refresh-token",
            last_refresh_utc=now,
            expires_at_utc=now,
        )


def test_public_contract_models_contain_no_filesystem_path_authority() -> None:
    forbidden_fragments = (
        "path",
        "root",
        "hermes_home",
        "lease_root",
        "auth_file",
        "store_root",
        "environment_items",
    )
    public_models = (
        pc.ProviderCredentialRef,
        pc.OpenAICodexOAuthCredential,
        pc.ProviderCredentialStatus,
        pc.ProviderCredentialDeliveryLease,
        pc.ProviderCredentialLeaseCleanup,
        pc.ProviderCredentialLocalClearResult,
        pc.ProviderCredentialAcquisitionPlan,
        pc.ProviderCredentialAcquisitionResult,
    )
    for model in public_models:
        field_names = set(model.model_fields)
        for field_name in field_names:
            assert not any(fragment in field_name for fragment in forbidden_fragments)

    now = datetime.now(timezone.utc)
    lease = pc.ProviderCredentialDeliveryLease(
        lease_id="lease.synthetic",
        runtime_id="runtime.synthetic",
        correlation_id="corr.synthetic",
        created_at_utc=now,
        expires_at_utc=now + timedelta(milliseconds=900_000),
    )
    plan = pc.ProviderCredentialAcquisitionPlan(
        command_argv_suffix=(
            "-m",
            "hermes_cli.main",
            "auth",
            "add",
            "openai-codex",
            "--type",
            "oauth",
        ),
        environment_keys=("HERMES_HOME", "PYTHONIOENCODING", "PYTHONUTF8"),
    )
    combined = f"{lease!r}\n{plan!r}"
    assert "synthetic-access-token" not in combined
    assert "auth.json" not in combined
    assert "hermes-home" not in combined
    with pytest.raises(ValidationError):
        pc.ProviderCredentialDeliveryLease(
            lease_id="lease.synthetic",
            runtime_id="runtime.synthetic",
            correlation_id="corr.synthetic",
            created_at_utc=now,
            expires_at_utc=now + timedelta(milliseconds=900_001),
        )


def test_package_root_exports_contracts_only() -> None:
    assert "promote_openai_codex_oauth_credential" not in pc.__all__
    assert "create_openai_codex_credential_lease" not in pc.__all__
    assert "build_openai_codex_oauth_acquisition_plan" not in pc.__all__
    root_text = (SOURCE_ROOT / "__init__.py").read_text(encoding="utf-8")
    assert ".store" not in root_text
    assert ".delivery" not in root_text
    assert ".oauth_acquisition" not in root_text
