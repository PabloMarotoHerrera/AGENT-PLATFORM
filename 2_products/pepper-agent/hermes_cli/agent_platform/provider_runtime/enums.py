"""Enumerations for governed provider-runtime profile metadata."""

from __future__ import annotations

from enum import StrEnum


class ProviderRuntimeProvider(StrEnum):
    """AGENT PLATFORM provider identifiers accepted by P15.M8."""

    OPENAI_CODEX = "openai-codex"


class ProviderRuntimeAuthentication(StrEnum):
    """Authentication family selected for the governed runtime profile."""

    CHATGPT_OAUTH = "chatgpt_oauth"


class ProviderRuntimeTransport(StrEnum):
    """Hermes transport mode selected for the governed runtime profile."""

    CODEX_RESPONSES = "codex_responses"


class ProviderModelIdentifierKind(StrEnum):
    """Model identifier stability selected by the provider profile."""

    MUTABLE_BACKEND_SLUG = "mutable_backend_slug"


class ProviderRuntimeProfileState(StrEnum):
    """Lifecycle state values for provider-runtime profile metadata."""

    STRATEGY_READY = "strategy_ready"
    CREDENTIAL_READY = "credential_ready"
    READY_FOR_WORKER_PROFILE = "ready_for_worker_profile"
    RUNTIME_UNVERIFIED = "runtime_unverified"
    BLOCKED = "blocked"


class ProviderFeaturePolicy(StrEnum):
    """Feature posture values for the governed runtime profile."""

    DISABLED = "disabled"


class ProviderUsageEvidenceSource(StrEnum):
    """Classifications for usage and quota evidence fields."""

    PROVIDER_REPORTED_WHEN_AVAILABLE = "provider_reported_when_available"
    PROVIDER_REPORTED_OR_LOCALLY_SUMMED = "provider_reported_or_locally_summed"
    PROVIDER_REPORTED = "provider_reported"
    PROVIDER_REPORTED_WHEN_SAFE = "provider_reported_when_safe"
    LOCALLY_DERIVED = "locally_derived"
    ACCOUNT_SPECIFIC_WHEN_EXPOSED = "account_specific_when_exposed"
    UNAVAILABLE_BY_DEFAULT = "unavailable_by_default"


__all__ = [
    "ProviderFeaturePolicy",
    "ProviderModelIdentifierKind",
    "ProviderRuntimeAuthentication",
    "ProviderRuntimeProfileState",
    "ProviderRuntimeProvider",
    "ProviderRuntimeTransport",
    "ProviderUsageEvidenceSource",
]
