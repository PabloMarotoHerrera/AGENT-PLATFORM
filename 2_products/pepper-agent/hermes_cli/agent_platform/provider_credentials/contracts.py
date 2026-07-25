"""Immutable contracts for governed provider credential boundaries."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    StringConstraints,
    field_validator,
    model_validator,
)


PROVIDER_CREDENTIAL_SCHEMA_VERSION = 1
OPENAI_CODEX_CREDENTIAL_STORE_ID = "openai-codex.primary"
OPENAI_CODEX_HERMES_PROVIDER_ID = "openai-codex"
OPENAI_CODEX_PROVIDER_ENDPOINT = "https://chatgpt.com/backend-api/codex"
OPENAI_CODEX_INTERNAL_LABEL = "AGENT PLATFORM OpenAI Codex OAuth"
MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES = 1
MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS = 900_000
MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS = 300_000
PROVIDER_CREDENTIAL_REMOTE_REVOCATION_STATUS = "not_supported_or_unverified"
PROVIDER_CLIENT_TOKEN_REMOTE_VALIDITY = "unverified"

StableCredentialIdentifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
BoundedCredentialText = Annotated[str, StringConstraints(min_length=1, max_length=512)]


class ProviderCredentialProvider(StrEnum):
    """AGENT PLATFORM provider identifiers accepted by this boundary."""

    OPENAI_CODEX = "openai_codex"


class ProviderCredentialAuthKind(StrEnum):
    """Credential-acquisition mechanisms accepted by this boundary."""

    CHATGPT_OAUTH_DEVICE = "chatgpt_oauth_device"


class _ProviderCredentialModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
    )

    @staticmethod
    def _utc(value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _no_control_characters(value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("text fields must not contain control characters")
        return value

    @staticmethod
    def _validate_secret(value: SecretStr) -> SecretStr:
        raw = value.get_secret_value()
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("credential tokens must be non-empty")
        if len(raw) > 16_384:
            raise ValueError("credential tokens exceed the boundary size limit")
        if any(ord(character) < 32 for character in raw):
            raise ValueError("credential tokens must not contain control characters")
        return value


class ProviderCredentialRef(_ProviderCredentialModel):
    """Stable pathless reference to the one governed credential store."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    store_id: Literal["openai-codex.primary"] = OPENAI_CODEX_CREDENTIAL_STORE_ID
    provider: ProviderCredentialProvider = ProviderCredentialProvider.OPENAI_CODEX
    auth_kind: ProviderCredentialAuthKind = (
        ProviderCredentialAuthKind.CHATGPT_OAUTH_DEVICE
    )
    hermes_provider_id: Literal["openai-codex"] = OPENAI_CODEX_HERMES_PROVIDER_ID


class ProviderClientTokenStatus(_ProviderCredentialModel):
    """Secret-free metadata derived from the OpenAI Codex client token pair."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    credential_store_id: Literal["openai-codex.primary"] = (
        OPENAI_CODEX_CREDENTIAL_STORE_ID
    )
    access_token_present: bool
    refresh_token_present: bool
    expiry_known: bool
    issued_at_utc: datetime | None = None
    expires_at_utc: datetime | None = None
    remaining_lifetime_ms: int | None = Field(default=None, ge=0, le=31_536_000_000)
    usable_for_bounded_lease: bool
    remote_validity: Literal["unverified"] = PROVIDER_CLIENT_TOKEN_REMOTE_VALIDITY

    @field_validator("issued_at_utc", "expires_at_utc", mode="after")
    @classmethod
    def token_datetimes_must_be_utc(cls, value: datetime | None) -> datetime | None:
        return cls._utc(value)

    @model_validator(mode="after")
    def usable_status_requires_complete_secret_free_metadata(
        self,
    ) -> "ProviderClientTokenStatus":
        if self.expiry_known != (self.expires_at_utc is not None):
            raise ValueError("expiry_known must match expires_at_utc presence")
        if self.usable_for_bounded_lease:
            if not self.access_token_present or not self.refresh_token_present:
                raise ValueError("bounded lease usability requires token-pair presence")
            if self.remaining_lifetime_ms is None:
                raise ValueError("bounded lease usability requires remaining lifetime")
            if (
                self.remaining_lifetime_ms
                < MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
            ):
                raise ValueError("bounded lease usability requires minimum lifetime")
        return self


class OpenAICodexOAuthCredential(_ProviderCredentialModel):
    """Secret-bearing OpenAI Codex ChatGPT OAuth material."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    access_token: SecretStr
    refresh_token: SecretStr
    base_url: Literal["https://chatgpt.com/backend-api/codex"] = (
        OPENAI_CODEX_PROVIDER_ENDPOINT
    )
    last_refresh_utc: datetime
    expires_at_utc: datetime

    @field_validator("access_token", "refresh_token", mode="after")
    @classmethod
    def tokens_must_be_bounded(cls, value: SecretStr) -> SecretStr:
        return cls._validate_secret(value)

    @field_validator("last_refresh_utc", "expires_at_utc", mode="after")
    @classmethod
    def datetimes_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)  # type: ignore[return-value]

    @model_validator(mode="after")
    def expiry_must_follow_refresh(self) -> "OpenAICodexOAuthCredential":
        if self.expires_at_utc <= self.last_refresh_utc:
            raise ValueError("expires_at_utc must be after last_refresh_utc")
        return self


class ProviderCredentialStatus(_ProviderCredentialModel):
    """Secret-free status projection for the governed credential store."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    configured: bool
    durable_store_present: bool
    durable_store_valid: bool
    protection_valid: bool
    provider_state_present: bool
    pool_state_present: bool
    token_pair_present: bool
    credential_count: int = Field(ge=0, le=1)
    active_provider_matches: bool
    last_refresh_utc: datetime | None = None
    expires_at_utc: datetime | None = None
    client_token_status: ProviderClientTokenStatus | None = None
    remote_revocation: Literal["not_supported_or_unverified"] = (
        PROVIDER_CREDENTIAL_REMOTE_REVOCATION_STATUS
    )

    @field_validator("last_refresh_utc", "expires_at_utc", mode="after")
    @classmethod
    def status_datetimes_must_be_utc(cls, value: datetime | None) -> datetime | None:
        return cls._utc(value)

    @model_validator(mode="after")
    def configured_requires_exactly_one_credential(self) -> "ProviderCredentialStatus":
        if self.configured and self.credential_count != 1:
            raise ValueError("configured status requires exactly one credential")
        if self.client_token_status is not None:
            if (
                self.client_token_status.credential_store_id
                != self.credential_ref.store_id
            ):
                raise ValueError("client-token metadata store mismatch")
        return self


class ProviderCredentialDeliveryLease(_ProviderCredentialModel):
    """Pathless public lease reference for a temporary credential projection."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    lease_id: StableCredentialIdentifier
    runtime_id: StableCredentialIdentifier
    correlation_id: StableCredentialIdentifier
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    created_at_utc: datetime
    expires_at_utc: datetime
    maximum_active_leases: Literal[1] = MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES
    maximum_lease_ttl_ms: Literal[900000] = MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS
    minimum_remaining_credential_lifetime_ms: Literal[300000] = (
        MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
    )
    automatic_refresh: Literal[False] = False
    refresh_on_lease_acquisition: Literal[False] = False
    refresh_writeback: Literal[False] = False

    @field_validator("created_at_utc", "expires_at_utc", mode="after")
    @classmethod
    def lease_datetimes_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)  # type: ignore[return-value]

    @model_validator(mode="after")
    def lease_ttl_must_be_bounded(self) -> "ProviderCredentialDeliveryLease":
        if self.expires_at_utc <= self.created_at_utc:
            raise ValueError("expires_at_utc must be after created_at_utc")
        ttl_ms = int((self.expires_at_utc - self.created_at_utc).total_seconds() * 1000)
        if ttl_ms > MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS:
            raise ValueError("lease TTL exceeds maximum_lease_ttl_ms")
        return self


class ProviderCredentialLeaseCleanup(_ProviderCredentialModel):
    """Secret-free release result for a temporary credential lease."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    lease_id: StableCredentialIdentifier
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    status: Literal["released", "not_found"]
    removed_item_count: int = Field(ge=0, le=512)
    residue_item_count: int = Field(ge=0, le=512)


class ProviderCredentialLocalClearResult(_ProviderCredentialModel):
    """Secret-free result for local store deletion, not remote revocation."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    local_store_present_after: bool
    remote_revocation: Literal["not_supported_or_unverified"] = (
        PROVIDER_CREDENTIAL_REMOTE_REVOCATION_STATUS
    )


class ProviderCredentialAcquisitionPlan(_ProviderCredentialModel):
    """Fixed OAuth-acquisition command plan without filesystem paths."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    command_argv_suffix: tuple[BoundedCredentialText, ...] = Field(
        min_length=7, max_length=7
    )
    environment_keys: tuple[BoundedCredentialText, ...] = Field(
        min_length=7, max_length=7
    )
    working_directory_role: Literal["Pepper_product_root"] = "Pepper_product_root"
    execution_disabled_by_default: Literal[True] = True

    @model_validator(mode="after")
    def command_must_be_fixed(self) -> "ProviderCredentialAcquisitionPlan":
        if self.command_argv_suffix != (
            "-m",
            "hermes_cli.main",
            "auth",
            "add",
            "openai-codex",
            "--type",
            "oauth",
        ):
            raise ValueError("acquisition command must be fixed to Hermes Codex OAuth")
        if self.environment_keys != (
            "HERMES_HOME",
            "HOME",
            "USERPROFILE",
            "APPDATA",
            "LOCALAPPDATA",
            "PYTHONIOENCODING",
            "PYTHONUTF8",
        ):
            raise ValueError("acquisition environment keys are fixed")
        return self


class ProviderCredentialAcquisitionResult(_ProviderCredentialModel):
    """Secret-free result from a dry-run or explicitly injected acquisition."""

    schema_version: Literal[1] = PROVIDER_CREDENTIAL_SCHEMA_VERSION
    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    execution_attempted: bool
    completed: bool
    exit_code: int | None = Field(default=None, ge=0, le=255)
    stdout_bytes: int = Field(default=0, ge=0, le=1_048_576)
    stderr_bytes: int = Field(default=0, ge=0, le=1_048_576)
    message: BoundedCredentialText

    @field_validator("message", mode="after")
    @classmethod
    def message_must_be_printable(cls, value: str) -> str:
        return cls._no_control_characters(value)
