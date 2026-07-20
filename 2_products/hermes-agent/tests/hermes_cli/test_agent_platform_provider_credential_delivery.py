from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials.delivery import (
    InvalidProviderCredentialLeaseError,
    ProviderCredentialLeaseCleanupError,
    assert_openai_codex_credential_lease_current,
    create_openai_codex_credential_lease,
    release_openai_codex_credential_lease,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionReport,
    promote_openai_codex_oauth_credential,
)


SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_credentials"
    / "delivery.py"
)


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


def write_store(
    root: Path, credential: OpenAICodexOAuthCredential | None = None
) -> None:
    promote_openai_codex_oauth_credential(
        root,
        credential or synthetic_credential(),
        protection_backend=FakeProtectionBackend(),
    )


def test_delivery_lease_has_pathless_public_ref_and_internal_projection(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source-store"
    lease_root = tmp_path / "lease-root"
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    write_store(source_root)

    projection = create_openai_codex_credential_lease(
        trusted_store_root=source_root,
        trusted_lease_root=lease_root,
        runtime_id="runtime.synthetic",
        correlation_id="corr.synthetic",
        lease_id="lease.synthetic",
        ttl_ms=60_000,
        now=now,
        protection_backend=FakeProtectionBackend(),
    )

    assert projection.environment_items == (
        ("HERMES_HOME", str(projection.projected_hermes_home)),
    )
    assert projection.lease_ref.maximum_active_leases == 1
    assert projection.lease_ref.maximum_lease_ttl_ms == 900_000
    assert projection.lease_ref.minimum_remaining_credential_lifetime_ms == 300_000
    assert projection.lease_ref.automatic_refresh is False
    assert projection.lease_ref.refresh_on_lease_acquisition is False
    assert projection.lease_ref.refresh_writeback is False
    public_text = repr(projection.lease_ref)
    assert "auth.json" not in public_text
    assert "hermes-home" not in public_text
    assert "synthetic-access-token" not in public_text
    marker_text = (
        lease_root
        / OPENAI_CODEX_CREDENTIAL_STORE_ID
        / "lease.synthetic"
        / ".agent-platform-provider-credential-lease.json"
    ).read_text(encoding="utf-8")
    assert "synthetic-access-token" not in marker_text
    assert "refresh_token" not in marker_text
    marker = json.loads(marker_text)
    assert marker["runtime_id"] == "runtime.synthetic"
    assert marker["correlation_id"] == "corr.synthetic"


def test_second_lease_and_excessive_ttl_are_rejected(tmp_path: Path) -> None:
    source_root = tmp_path / "source-store"
    lease_root = tmp_path / "lease-root"
    write_store(source_root)
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    create_openai_codex_credential_lease(
        trusted_store_root=source_root,
        trusted_lease_root=lease_root,
        runtime_id="runtime.one",
        correlation_id="corr.one",
        lease_id="lease.one",
        ttl_ms=60_000,
        now=now,
        protection_backend=FakeProtectionBackend(),
    )
    with pytest.raises(InvalidProviderCredentialLeaseError):
        create_openai_codex_credential_lease(
            trusted_store_root=source_root,
            trusted_lease_root=lease_root,
            runtime_id="runtime.two",
            correlation_id="corr.two",
            lease_id="lease.two",
            ttl_ms=60_000,
            now=now,
            protection_backend=FakeProtectionBackend(),
        )
    with pytest.raises(InvalidProviderCredentialLeaseError):
        create_openai_codex_credential_lease(
            trusted_store_root=source_root,
            trusted_lease_root=tmp_path / "other-lease-root",
            runtime_id="runtime.ttl",
            correlation_id="corr.ttl",
            ttl_ms=MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS + 1,
            now=now,
            protection_backend=FakeProtectionBackend(),
        )


def test_expired_and_near_expiry_credentials_are_rejected(tmp_path: Path) -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    expired_root = tmp_path / "expired-store"
    near_root = tmp_path / "near-store"
    expired_credential = OpenAICodexOAuthCredential(
        access_token="synthetic-access-token",
        refresh_token="synthetic-refresh-token",
        last_refresh_utc=now - timedelta(hours=1),
        expires_at_utc=now - timedelta(seconds=1),
    )
    write_store(expired_root, expired_credential)
    near_expiry_delta = timedelta(
        milliseconds=MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS
        + MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
        - 1
    )
    write_store(near_root, synthetic_credential(expires_delta=near_expiry_delta))

    with pytest.raises(InvalidProviderCredentialLeaseError):
        create_openai_codex_credential_lease(
            trusted_store_root=expired_root,
            trusted_lease_root=tmp_path / "expired-leases",
            runtime_id="runtime.expired",
            correlation_id="corr.expired",
            now=now,
            protection_backend=FakeProtectionBackend(),
        )
    with pytest.raises(InvalidProviderCredentialLeaseError):
        create_openai_codex_credential_lease(
            trusted_store_root=near_root,
            trusted_lease_root=tmp_path / "near-leases",
            runtime_id="runtime.near",
            correlation_id="corr.near",
            now=now,
            protection_backend=FakeProtectionBackend(),
        )


def test_release_rejects_runtime_correlation_and_provider_mismatch(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source-store"
    lease_root = tmp_path / "lease-root"
    write_store(source_root)
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    projection = create_openai_codex_credential_lease(
        trusted_store_root=source_root,
        trusted_lease_root=lease_root,
        runtime_id="runtime.expected",
        correlation_id="corr.expected",
        lease_id="lease.expected",
        ttl_ms=60_000,
        now=now,
        protection_backend=FakeProtectionBackend(),
    )
    with pytest.raises(ProviderCredentialLeaseCleanupError):
        release_openai_codex_credential_lease(
            trusted_lease_root=lease_root,
            lease_ref=projection.lease_ref,
            runtime_id="runtime.other",
            correlation_id="corr.expected",
        )
    with pytest.raises(ProviderCredentialLeaseCleanupError):
        release_openai_codex_credential_lease(
            trusted_lease_root=lease_root,
            lease_ref=projection.lease_ref,
            runtime_id="runtime.expected",
            correlation_id="corr.other",
        )
    with pytest.raises(InvalidProviderCredentialLeaseError):
        release_openai_codex_credential_lease(
            trusted_lease_root=lease_root,
            lease_ref=projection.lease_ref,
            runtime_id="runtime.expected",
            correlation_id="corr.expected",
            provider="not-openai-codex",
        )


def test_release_removes_exact_projection_preserves_sibling_and_zero_residue(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source-store"
    lease_root = tmp_path / "lease-root"
    write_store(source_root)
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    projection = create_openai_codex_credential_lease(
        trusted_store_root=source_root,
        trusted_lease_root=lease_root,
        runtime_id="runtime.release",
        correlation_id="corr.release",
        lease_id="lease.release",
        ttl_ms=60_000,
        now=now,
        protection_backend=FakeProtectionBackend(),
    )
    sibling = lease_root / OPENAI_CODEX_CREDENTIAL_STORE_ID / "sibling"
    sibling.mkdir(parents=True)
    (sibling / "keep.txt").write_text("keep", encoding="utf-8")

    result = release_openai_codex_credential_lease(
        trusted_lease_root=lease_root,
        lease_ref=projection.lease_ref,
        runtime_id="runtime.release",
        correlation_id="corr.release",
    )

    assert result.status == "released"
    assert not (
        lease_root / OPENAI_CODEX_CREDENTIAL_STORE_ID / "lease.release"
    ).exists()
    assert (sibling / "keep.txt").read_text(encoding="utf-8") == "keep"

    lease_root_without_sibling = tmp_path / "lease-root-zero"
    projection = create_openai_codex_credential_lease(
        trusted_store_root=source_root,
        trusted_lease_root=lease_root_without_sibling,
        runtime_id="runtime.zero",
        correlation_id="corr.zero",
        lease_id="lease.zero",
        ttl_ms=60_000,
        now=now,
        protection_backend=FakeProtectionBackend(),
    )
    result = release_openai_codex_credential_lease(
        trusted_lease_root=lease_root_without_sibling,
        lease_ref=projection.lease_ref,
        runtime_id="runtime.zero",
        correlation_id="corr.zero",
    )
    assert result.residue_item_count == 0
    assert list(lease_root_without_sibling.iterdir()) == []


def test_lease_current_check_and_source_no_refresh_or_erasure_claim() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    lease = assert_openai_codex_credential_lease_current(
        create_dummy_lease(now),
        now=now + timedelta(seconds=1),
    )
    assert lease.lease_id == "lease.current"
    with pytest.raises(InvalidProviderCredentialLeaseError):
        assert_openai_codex_credential_lease_current(
            create_dummy_lease(now),
            now=now + timedelta(minutes=15),
        )
    source = SOURCE_PATH.read_text(encoding="utf-8").lower()
    assert "secure erase" not in source
    assert "secure-erasure" not in source
    assert "refresh_codex" not in source
    assert "force_refresh" not in source


def create_dummy_lease(now: datetime):
    from hermes_cli.agent_platform.provider_credentials.contracts import (
        ProviderCredentialDeliveryLease,
    )

    return ProviderCredentialDeliveryLease(
        lease_id="lease.current",
        runtime_id="runtime.current",
        correlation_id="corr.current",
        created_at_utc=now,
        expires_at_utc=now + timedelta(minutes=15),
    )
