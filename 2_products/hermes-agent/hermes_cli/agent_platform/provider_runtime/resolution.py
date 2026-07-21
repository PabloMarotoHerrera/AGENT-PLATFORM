"""Internal safe resolver for P15.2 provider-runtime profile metadata."""

from __future__ import annotations

from datetime import timedelta

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
)
from hermes_cli.agent_platform.provider_runtime.contracts import (
    ProviderRuntimeResolutionRequest,
    ResolvedProviderRuntimeBinding,
)
from hermes_cli.agent_platform.provider_runtime.enums import ProviderRuntimeProfileState
from hermes_cli.agent_platform.provider_runtime.profiles import (
    get_provider_runtime_profile,
)


_OPENAI_CODEX_HERMES_PROVIDER_ID = "openai-codex"


class ProviderRuntimeResolutionError(ValueError):
    """Raised when supplied metadata violates the P15.2 profile."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


def resolve_provider_runtime_profile(
    request: ProviderRuntimeResolutionRequest,
    *,
    lease_active: bool = True,
    credential_store_id: str = OPENAI_CODEX_CREDENTIAL_STORE_ID,
    credential_provider_id: str = _OPENAI_CODEX_HERMES_PROVIDER_ID,
) -> ResolvedProviderRuntimeBinding:
    """Resolve a worker-ready binding from secret-free credential metadata.

    This internal resolver does not read credentials, paths, environment
    variables, auth stores, model lists, providers, workers, agents or tools.
    """

    profile = get_provider_runtime_profile(request.profile_id)
    requirement = profile.credential_requirement
    status = request.credential_status
    lease = request.credential_lease_ref
    now = request.evaluated_at_utc

    if credential_provider_id != _OPENAI_CODEX_HERMES_PROVIDER_ID:
        raise ProviderRuntimeResolutionError(
            "provider_mismatch",
            "credential metadata provider does not match the profile",
        )
    if credential_store_id != requirement.credential_store_id:
        raise ProviderRuntimeResolutionError(
            "store_mismatch",
            "credential metadata store does not match the profile",
        )
    if status.credential_ref != requirement.credential_ref:
        raise ProviderRuntimeResolutionError(
            "store_mismatch",
            "credential status reference does not match the profile",
        )
    if lease.credential_ref != requirement.credential_ref:
        raise ProviderRuntimeResolutionError(
            "store_mismatch",
            "credential lease reference does not match the profile",
        )
    if status.credential_count != requirement.credential_count:
        raise ProviderRuntimeResolutionError(
            "credential_count_rejected",
            "provider-runtime readiness requires exactly one credential",
        )
    if not status.configured:
        raise ProviderRuntimeResolutionError(
            "credential_not_configured",
            "provider-runtime readiness requires configured credential metadata",
        )
    if not status.durable_store_valid or not status.protection_valid:
        raise ProviderRuntimeResolutionError(
            "credential_store_not_valid",
            "provider-runtime readiness requires valid credential-store metadata",
        )
    if not status.active_provider_matches:
        raise ProviderRuntimeResolutionError(
            "provider_mismatch",
            "active credential provider does not match the profile",
        )
    if not status.token_pair_present:
        raise ProviderRuntimeResolutionError(
            "access_token_presence_metadata_required",
            "provider-runtime readiness requires token-pair presence metadata",
        )
    if status.expires_at_utc is None:
        raise ProviderRuntimeResolutionError(
            "credential_expiry_metadata_required",
            "provider-runtime readiness requires credential-expiry metadata",
        )
    if status.expires_at_utc <= now:
        raise ProviderRuntimeResolutionError(
            "credential_expired",
            "provider-runtime readiness rejects expired credential metadata",
        )
    if requirement.active_lease_required and not lease_active:
        raise ProviderRuntimeResolutionError(
            "lease_inactive",
            "provider-runtime readiness requires active lease metadata",
        )
    if lease.expires_at_utc <= now:
        raise ProviderRuntimeResolutionError(
            "lease_expired",
            "provider-runtime readiness rejects expired lease metadata",
        )
    required_credential_expiry = lease.expires_at_utc + timedelta(
        milliseconds=MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
    )
    if status.expires_at_utc < required_credential_expiry:
        raise ProviderRuntimeResolutionError(
            "insufficient_remaining_lease_lifetime",
            "credential metadata does not cover the lease plus remaining-lifetime bound",
        )
    if lease.runtime_id != request.runtime_id:
        raise ProviderRuntimeResolutionError(
            "runtime_mismatch",
            "credential lease runtime does not match the requested runtime",
        )
    if lease.correlation_id != request.correlation_id:
        raise ProviderRuntimeResolutionError(
            "correlation_mismatch",
            "credential lease correlation does not match the requested runtime",
        )

    return ResolvedProviderRuntimeBinding(
        profile=profile,
        credential_store_ref=requirement.credential_ref,
        credential_lease_ref=lease,
        resolved_state=ProviderRuntimeProfileState.READY_FOR_WORKER_PROFILE,
        resolved_at_utc=now,
    )


__all__ = [
    "ProviderRuntimeResolutionError",
    "resolve_provider_runtime_profile",
]
