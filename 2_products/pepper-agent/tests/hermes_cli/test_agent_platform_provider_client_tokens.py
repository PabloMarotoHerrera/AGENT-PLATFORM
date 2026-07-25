from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import SecretStr

from hermes_cli.agent_platform.provider_credentials.client_tokens import (
    ProviderClientTokenMetadataError,
    derive_openai_codex_client_token_status,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def jwt_token(*, exp_delta: timedelta = timedelta(hours=1), iat: bool = True) -> str:
    header = {"alg": "none", "typ": "JWT"}
    payload = {"exp": int((NOW + exp_delta).timestamp())}
    if iat:
        payload["iat"] = int(NOW.timestamp())
    return ".".join((_segment(header), _segment(payload), "signature"))


def _segment(payload: dict[str, object]) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def test_client_token_metadata_decodes_only_time_claims_and_is_secret_free() -> None:
    token = jwt_token()
    status = derive_openai_codex_client_token_status(
        access_token=SecretStr(token),
        refresh_token=SecretStr("synthetic-refresh-token"),
        now=NOW,
    )

    assert status.access_token_present is True
    assert status.refresh_token_present is True
    assert status.expiry_known is True
    assert status.issued_at_utc == NOW
    assert status.expires_at_utc == NOW + timedelta(hours=1)
    assert status.remaining_lifetime_ms == 3_600_000
    assert status.usable_for_bounded_lease is True
    assert status.remote_validity == "unverified"
    public_text = repr(status) + status.model_dump_json()
    assert token not in public_text
    assert "synthetic-refresh-token" not in public_text


def test_explicit_trusted_expiry_metadata_is_preferred() -> None:
    status = derive_openai_codex_client_token_status(
        access_token=SecretStr("opaque-access-token"),
        refresh_token=SecretStr("synthetic-refresh-token"),
        now=NOW,
        explicit_issued_at_utc=NOW - timedelta(minutes=1),
        explicit_expires_at_utc=NOW + timedelta(minutes=10),
    )

    assert status.issued_at_utc == NOW - timedelta(minutes=1)
    assert status.expires_at_utc == NOW + timedelta(minutes=10)
    assert status.remaining_lifetime_ms == 600_000
    assert status.usable_for_bounded_lease is True


@pytest.mark.parametrize(
    ("access_token", "refresh_token", "code"),
    [
        (
            "opaque-access-token",
            "synthetic-refresh-token",
            "access_token_expiry_unknown",
        ),
        (
            jwt_token(exp_delta=timedelta(seconds=-1), iat=False),
            "synthetic-refresh-token",
            "access_token_expired",
        ),
        (
            jwt_token(exp_delta=timedelta(seconds=299)),
            "synthetic-refresh-token",
            "client_token_not_lease_usable",
        ),
        (jwt_token(), "", "refresh_token_missing"),
    ],
)
def test_malformed_missing_expired_and_near_expiry_tokens_are_bounded(
    access_token: str,
    refresh_token: str,
    code: str,
) -> None:
    if code == "client_token_not_lease_usable":
        status = derive_openai_codex_client_token_status(
            access_token=SecretStr(access_token),
            refresh_token=SecretStr(refresh_token),
            now=NOW,
        )
        assert status.usable_for_bounded_lease is False
        assert status.remaining_lifetime_ms is not None
        assert status.remaining_lifetime_ms < 300_000
        return

    with pytest.raises(ProviderClientTokenMetadataError) as exc_info:
        derive_openai_codex_client_token_status(
            access_token=SecretStr(access_token),
            refresh_token=SecretStr(refresh_token),
            now=NOW,
        )
    assert exc_info.value.code == code
    assert access_token not in str(exc_info.value)
    if refresh_token:
        assert refresh_token not in str(exc_info.value)


def test_jwt_claims_are_not_returned_or_persisted() -> None:
    token = ".".join((
        _segment({"alg": "none"}),
        _segment({
            "iat": int(NOW.timestamp()),
            "exp": int((NOW + timedelta(hours=1)).timestamp()),
            "ignored": "not-returned",
        }),
        "signature",
    ))
    status = derive_openai_codex_client_token_status(
        access_token=SecretStr(token),
        refresh_token=SecretStr("synthetic-refresh-token"),
        now=NOW,
    )

    assert "ignored" not in status.model_dump_json()
    assert "not-returned" not in status.model_dump_json()
