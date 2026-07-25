"""Internal secret-free client-token metadata derivation."""

from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from typing import Any

from pydantic import SecretStr

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS,
    ProviderClientTokenStatus,
)


_EARLIEST_REASONABLE_TOKEN_TIME = 1_577_836_800  # 2020-01-01T00:00:00Z
_LATEST_REASONABLE_TOKEN_TIME = 4_102_444_800  # 2100-01-01T00:00:00Z


class ProviderClientTokenMetadataError(ValueError):
    """Raised when token metadata cannot be safely derived without secrets."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"code={code}")


def derive_openai_codex_client_token_status(
    *,
    access_token: SecretStr,
    refresh_token: SecretStr,
    now: datetime | None = None,
    explicit_expires_at_utc: datetime | None = None,
    explicit_issued_at_utc: datetime | None = None,
) -> ProviderClientTokenStatus:
    """Return bounded, secret-free metadata for one Codex OAuth token pair."""

    access_value = _secret_value(access_token, "access_token_missing")
    _secret_value(refresh_token, "refresh_token_missing")
    observed = _utc(now or datetime.now(timezone.utc), "now_not_utc")
    if explicit_expires_at_utc is not None:
        expires_at = _utc(explicit_expires_at_utc, "explicit_expiry_not_utc")
        issued_at = (
            _utc(explicit_issued_at_utc, "explicit_issue_time_not_utc")
            if explicit_issued_at_utc is not None
            else None
        )
    else:
        issued_at, expires_at = _decode_jwt_time_metadata(access_value)
    remaining_ms = int((expires_at - observed).total_seconds() * 1000)
    if remaining_ms <= 0:
        raise ProviderClientTokenMetadataError("access_token_expired")
    return ProviderClientTokenStatus(
        access_token_present=True,
        refresh_token_present=True,
        expiry_known=True,
        issued_at_utc=issued_at,
        expires_at_utc=expires_at,
        remaining_lifetime_ms=remaining_ms,
        usable_for_bounded_lease=(
            remaining_ms >= MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
        ),
    )


def _secret_value(value: SecretStr, missing_code: str) -> str:
    if not isinstance(value, SecretStr):
        raise ProviderClientTokenMetadataError(missing_code)
    raw = value.get_secret_value()
    if not isinstance(raw, str) or not raw.strip():
        raise ProviderClientTokenMetadataError(missing_code)
    if len(raw) > 16_384 or any(ord(character) < 32 for character in raw):
        raise ProviderClientTokenMetadataError("token_malformed")
    return raw.strip()


def _utc(value: datetime, code: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProviderClientTokenMetadataError(code)
    return value.astimezone(timezone.utc)


def _decode_jwt_time_metadata(access_token: str) -> tuple[datetime | None, datetime]:
    parts = access_token.split(".")
    if len(parts) < 2 or not parts[1]:
        raise ProviderClientTokenMetadataError("access_token_expiry_unknown")
    try:
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded.encode("ascii")))
    except Exception:
        raise ProviderClientTokenMetadataError("access_token_malformed") from None
    if not isinstance(payload, dict):
        raise ProviderClientTokenMetadataError("access_token_malformed")
    exp = _reasonable_epoch_seconds(payload.get("exp"), "access_token_expiry_invalid")
    iat_value = payload.get("iat")
    iat = (
        _reasonable_epoch_seconds(iat_value, "access_token_issue_time_invalid")
        if iat_value is not None
        else None
    )
    if iat is not None and iat > exp:
        raise ProviderClientTokenMetadataError("access_token_issue_time_after_expiry")
    issued_at = datetime.fromtimestamp(iat, timezone.utc) if iat is not None else None
    expires_at = datetime.fromtimestamp(exp, timezone.utc)
    return issued_at, expires_at


def _reasonable_epoch_seconds(value: Any, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProviderClientTokenMetadataError(code)
    if not (_EARLIEST_REASONABLE_TOKEN_TIME <= value <= _LATEST_REASONABLE_TOKEN_TIME):
        raise ProviderClientTokenMetadataError(code)
    return value


__all__ = [
    "ProviderClientTokenMetadataError",
    "derive_openai_codex_client_token_status",
]
