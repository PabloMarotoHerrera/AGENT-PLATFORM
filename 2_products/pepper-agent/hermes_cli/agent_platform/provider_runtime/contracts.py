"""Immutable contracts for governed provider-runtime profile metadata."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES,
    MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    ProviderCredentialDeliveryLease,
    ProviderCredentialRef,
    ProviderCredentialStatus,
)
from hermes_cli.agent_platform.provider_runtime.enums import (
    ProviderFeaturePolicy,
    ProviderModelIdentifierKind,
    ProviderRuntimeAuthentication,
    ProviderRuntimeProfileState,
    ProviderRuntimeProvider,
    ProviderRuntimeTransport,
    ProviderUsageEvidenceSource,
)


PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION = 1

_OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID = (
    "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
)
_OPENAI_CODEX_PROVIDER_ENDPOINT_SOURCE = "DEFAULT_CODEX_BASE_URL"
_OPENAI_CODEX_PROVIDER_RUNTIME_MODEL_ID = "gpt-5.5"
_OPENAI_CODEX_PROVIDER_RUNTIME_REASONING_EFFORT = "medium"
_OPENAI_CODEX_MAXIMUM_PROMPT_TOKENS = 32_768
_OPENAI_CODEX_RESERVED_SYSTEM_INSTRUCTION_TOKENS = 8_192
_OPENAI_CODEX_MAXIMUM_USER_CONTENT_TOKENS = 24_576
_OPENAI_CODEX_MAXIMUM_OUTPUT_TOKENS = 4_096
_OPENAI_CODEX_CONNECTION_TIMEOUT_MS = 10_000
_OPENAI_CODEX_RESPONSE_HEADER_TIMEOUT_MS = 30_000
_OPENAI_CODEX_COMPLETE_INFERENCE_TIMEOUT_MS = 120_000
_OPENAI_CODEX_CANCELLATION_DEADLINE_MS = 10_000

BoundedRuntimeText = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=256,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:/ -]{0,255}$",
    ),
]


class _ProviderRuntimeModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
    )

    @staticmethod
    def _utc(value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(timezone.utc)


class ProviderEndpointPolicy(_ProviderRuntimeModel):
    """Endpoint binding and override denial for the governed profile."""

    provider_endpoint: Literal["https://chatgpt.com/backend-api/codex"] = (
        OPENAI_CODEX_PROVIDER_ENDPOINT
    )
    endpoint_source: Literal["DEFAULT_CODEX_BASE_URL"] = (
        _OPENAI_CODEX_PROVIDER_ENDPOINT_SOURCE
    )
    base_url_override_allowed: Literal[False] = False
    caller_endpoint_allowed: Literal[False] = False
    frontend_endpoint_allowed: Literal[False] = False
    config_endpoint_allowed: Literal[False] = False
    custom_endpoint_allowed: Literal[False] = False
    proxy_endpoint_allowed: Literal[False] = False
    aggregator_endpoint_allowed: Literal[False] = False


class ProviderModelPolicy(_ProviderRuntimeModel):
    """Selected model identity and replacement posture for P15.M8."""

    model_id: Literal["gpt-5.5"] = _OPENAI_CODEX_PROVIDER_RUNTIME_MODEL_ID
    identifier_kind: ProviderModelIdentifierKind = (
        ProviderModelIdentifierKind.MUTABLE_BACKEND_SLUG
    )
    immutable_snapshot: Literal[False] = False
    dynamic_replacement_allowed: Literal[False] = False
    live_model_list_replacement_allowed: Literal[False] = False
    fallback_model_id: None = None


class ProviderCredentialRequirement(_ProviderRuntimeModel):
    """Secret-free credential and lease metadata required by the profile."""

    credential_ref: ProviderCredentialRef = Field(default_factory=ProviderCredentialRef)
    credential_store_id: Literal["openai-codex.primary"] = (
        OPENAI_CODEX_CREDENTIAL_STORE_ID
    )
    credential_count: Literal[1] = 1
    active_lease_required: Literal[True] = True
    access_token_presence_metadata_required: Literal[True] = True
    refresh_token_presence_metadata_required: Literal[True] = True
    client_token_metadata_required: Literal[True] = True
    maximum_active_leases: Literal[1] = MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES
    maximum_lease_ttl_ms: Literal[900000] = MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS
    minimum_remaining_credential_lifetime_ms: Literal[300000] = (
        MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
    )
    automatic_refresh: Literal[False] = False
    refresh_on_lease_acquisition: Literal[False] = False
    refresh_writeback: Literal[False] = False
    profile_reads_credentials: Literal[False] = False


class ProviderGenerationPolicy(_ProviderRuntimeModel):
    """Generation controls and disabled feature posture for the profile."""

    maximum_prompt_tokens: Literal[32768] = _OPENAI_CODEX_MAXIMUM_PROMPT_TOKENS
    reserved_system_instruction_tokens: Literal[8192] = (
        _OPENAI_CODEX_RESERVED_SYSTEM_INSTRUCTION_TOKENS
    )
    maximum_user_content_tokens: Literal[24576] = (
        _OPENAI_CODEX_MAXIMUM_USER_CONTENT_TOKENS
    )
    maximum_output_tokens: Literal[4096] = _OPENAI_CODEX_MAXIMUM_OUTPUT_TOKENS
    reasoning_effort: Literal["medium"] = (
        _OPENAI_CODEX_PROVIDER_RUNTIME_REASONING_EFFORT
    )
    streaming: ProviderFeaturePolicy = ProviderFeaturePolicy.DISABLED
    tools: ProviderFeaturePolicy = ProviderFeaturePolicy.DISABLED
    hosted_tools: ProviderFeaturePolicy = ProviderFeaturePolicy.DISABLED
    MCP: ProviderFeaturePolicy = ProviderFeaturePolicy.DISABLED
    automatic_retry: ProviderFeaturePolicy = ProviderFeaturePolicy.DISABLED
    automatic_fallback: ProviderFeaturePolicy = ProviderFeaturePolicy.DISABLED
    oversized_request_posture: Literal["fail_before_provider_call"] = (
        "fail_before_provider_call"
    )


class ProviderTimeoutPolicy(_ProviderRuntimeModel):
    """Maximum provider-runtime timeout values owned by P15.M8."""

    connection_timeout_ms: Literal[10000] = _OPENAI_CODEX_CONNECTION_TIMEOUT_MS
    response_header_timeout_ms: Literal[30000] = (
        _OPENAI_CODEX_RESPONSE_HEADER_TIMEOUT_MS
    )
    complete_inference_timeout_ms: Literal[120000] = (
        _OPENAI_CODEX_COMPLETE_INFERENCE_TIMEOUT_MS
    )
    cancellation_deadline_ms: Literal[10000] = _OPENAI_CODEX_CANCELLATION_DEADLINE_MS
    caller_timeout_override_allowed: Literal[False] = False
    sdk_default_timeout_allowed: Literal[False] = False


class ProviderUsageEvidencePolicy(_ProviderRuntimeModel):
    """Usage and quota evidence classification for later runtime work."""

    input_tokens: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    cached_input_tokens: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    output_tokens: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    total_tokens: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED_OR_LOCALLY_SUMMED
    )
    returned_model_id: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED
    )
    finish_reason: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    provider_request_id: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_SAFE
    )
    elapsed_time_ms: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.LOCALLY_DERIVED
    )
    subscription_quota_signal: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.ACCOUNT_SPECIFIC_WHEN_EXPOSED
    )
    credit_consumption_signal: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.ACCOUNT_SPECIFIC_WHEN_EXPOSED
    )
    exact_marginal_request_cost: ProviderUsageEvidenceSource = (
        ProviderUsageEvidenceSource.UNAVAILABLE_BY_DEFAULT
    )


class ProviderRuntimeProfile(_ProviderRuntimeModel):
    """Public immutable P15.M8 OpenAI Codex provider-runtime profile."""

    schema_version: Literal[1] = PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION
    profile_id: Literal["provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"] = (
        _OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    )
    state: ProviderRuntimeProfileState = ProviderRuntimeProfileState.RUNTIME_UNVERIFIED
    provider: ProviderRuntimeProvider = ProviderRuntimeProvider.OPENAI_CODEX
    authentication: ProviderRuntimeAuthentication = (
        ProviderRuntimeAuthentication.CHATGPT_OAUTH
    )
    transport: ProviderRuntimeTransport = ProviderRuntimeTransport.CODEX_RESPONSES
    endpoint_policy: ProviderEndpointPolicy = Field(
        default_factory=ProviderEndpointPolicy
    )
    model_policy: ProviderModelPolicy = Field(default_factory=ProviderModelPolicy)
    credential_requirement: ProviderCredentialRequirement = Field(
        default_factory=ProviderCredentialRequirement
    )
    generation_policy: ProviderGenerationPolicy = Field(
        default_factory=ProviderGenerationPolicy
    )
    timeout_policy: ProviderTimeoutPolicy = Field(default_factory=ProviderTimeoutPolicy)
    usage_evidence_policy: ProviderUsageEvidencePolicy = Field(
        default_factory=ProviderUsageEvidencePolicy
    )
    worker_profile_required: Literal[True] = True
    runtime_entitlement_verified: Literal[False] = False
    provider_reachability_verified: Literal[False] = False
    runtime_transport_verified: Literal[False] = False
    inference_success_verified: Literal[False] = False


class ProviderRuntimeResolutionRequest(_ProviderRuntimeModel):
    """Public safe request for internal provider-runtime metadata resolution."""

    schema_version: Literal[1] = PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION
    profile_id: BoundedRuntimeText = _OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    runtime_id: BoundedRuntimeText
    correlation_id: BoundedRuntimeText
    requested_by: BoundedRuntimeText
    evaluated_at_utc: datetime
    credential_status: ProviderCredentialStatus
    credential_lease_ref: ProviderCredentialDeliveryLease

    @field_validator("evaluated_at_utc", mode="after")
    @classmethod
    def evaluated_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)


class ResolvedProviderRuntimeBinding(_ProviderRuntimeModel):
    """Internal resolved binding passed to later worker-profile composition."""

    profile: ProviderRuntimeProfile
    credential_store_ref: ProviderCredentialRef = Field(
        default_factory=ProviderCredentialRef
    )
    credential_lease_ref: ProviderCredentialDeliveryLease
    resolved_state: Literal[ProviderRuntimeProfileState.READY_FOR_WORKER_PROFILE] = (
        ProviderRuntimeProfileState.READY_FOR_WORKER_PROFILE
    )
    resolved_at_utc: datetime

    @field_validator("resolved_at_utc", mode="after")
    @classmethod
    def resolved_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)


__all__ = [
    "PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION",
    "ProviderCredentialRequirement",
    "ProviderEndpointPolicy",
    "ProviderGenerationPolicy",
    "ProviderModelPolicy",
    "ProviderRuntimeProfile",
    "ProviderRuntimeResolutionRequest",
    "ProviderTimeoutPolicy",
    "ProviderUsageEvidencePolicy",
]
