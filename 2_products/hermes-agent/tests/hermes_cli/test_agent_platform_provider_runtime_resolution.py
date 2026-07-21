from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.provider_credentials import (
    MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS,
    ProviderCredentialDeliveryLease,
    ProviderCredentialStatus,
)
from hermes_cli.agent_platform.provider_runtime import ProviderRuntimeResolutionRequest
from hermes_cli.agent_platform.provider_runtime.contracts import (
    ResolvedProviderRuntimeBinding,
)
from hermes_cli.agent_platform.provider_runtime.enums import ProviderRuntimeProfileState
from hermes_cli.agent_platform.provider_runtime.profiles import (
    UnknownProviderRuntimeProfileError,
)
from hermes_cli.agent_platform.provider_runtime.resolution import (
    ProviderRuntimeResolutionError,
    resolve_provider_runtime_profile,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)
PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"


def ready_credential_status(
    *,
    configured: bool = True,
    credential_count: int = 1,
    token_pair_present: bool = True,
    active_provider_matches: bool = True,
    durable_store_valid: bool = True,
    protection_valid: bool = True,
    expires_delta: timedelta = timedelta(minutes=20),
) -> ProviderCredentialStatus:
    return ProviderCredentialStatus(
        configured=configured,
        durable_store_present=True,
        durable_store_valid=durable_store_valid,
        protection_valid=protection_valid,
        provider_state_present=True,
        pool_state_present=True,
        token_pair_present=token_pair_present,
        credential_count=credential_count,
        active_provider_matches=active_provider_matches,
        last_refresh_utc=NOW - timedelta(minutes=1),
        expires_at_utc=NOW + expires_delta,
    )


def ready_lease(
    *,
    runtime_id: str = "runtime.ready",
    correlation_id: str = "corr.ready",
    created_at: datetime = NOW,
    expires_at: datetime = NOW + timedelta(minutes=15),
) -> ProviderCredentialDeliveryLease:
    return ProviderCredentialDeliveryLease(
        lease_id="lease.ready",
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        created_at_utc=created_at,
        expires_at_utc=expires_at,
    )


def ready_request(**overrides: object) -> ProviderRuntimeResolutionRequest:
    values: dict[str, object] = {
        "runtime_id": "runtime.ready",
        "correlation_id": "corr.ready",
        "requested_by": "p15.2.resolution-test",
        "evaluated_at_utc": NOW,
        "credential_status": ready_credential_status(),
        "credential_lease_ref": ready_lease(),
    }
    values.update(overrides)
    return ProviderRuntimeResolutionRequest(**values)


def test_worker_ready_resolution_returns_internal_binding_only() -> None:
    binding = resolve_provider_runtime_profile(ready_request())

    assert isinstance(binding, ResolvedProviderRuntimeBinding)
    assert (
        binding.resolved_state is ProviderRuntimeProfileState.READY_FOR_WORKER_PROFILE
    )
    assert binding.resolved_at_utc == NOW
    assert binding.profile.profile_id == PROFILE_ID
    assert binding.profile.provider.value == "openai-codex"
    assert binding.profile.authentication.value == "chatgpt_oauth"
    assert binding.profile.transport.value == "codex_responses"
    assert binding.profile.model_policy.model_id == "gpt-5.5"
    assert binding.profile.endpoint_policy.provider_endpoint == (
        "https://chatgpt.com/backend-api/codex"
    )
    assert binding.credential_store_ref.store_id == "openai-codex.primary"
    assert binding.credential_lease_ref.lease_id == "lease.ready"
    assert binding.profile.runtime_entitlement_verified is False
    assert binding.profile.runtime_transport_verified is False
    public_text = repr(binding).lower()
    assert "forbidden-sensitive-value" not in public_text
    assert "auth.json" not in public_text
    assert "lease-root" not in public_text


def test_unknown_profile_is_rejected() -> None:
    request = ready_request(profile_id="provider.unknown")
    with pytest.raises(UnknownProviderRuntimeProfileError):
        resolve_provider_runtime_profile(request)


@pytest.mark.parametrize(
    "forbidden_field",
    (
        "provider",
        "model",
        "endpoint",
        "generation_override",
        "timeout_override",
        "credential_path",
        "lease_path",
        "environment",
        "command",
        "argv",
    ),
)
def test_public_resolution_request_rejects_override_fields(
    forbidden_field: str,
) -> None:
    payload = ready_request().model_dump()
    payload[forbidden_field] = "forbidden"
    with pytest.raises(ValidationError):
        ProviderRuntimeResolutionRequest(**payload)


@pytest.mark.parametrize(
    ("resolution_request", "kwargs", "code"),
    [
        (
            ready_request(
                credential_status=ready_credential_status(
                    configured=False,
                    credential_count=0,
                    token_pair_present=False,
                )
            ),
            {},
            "credential_count_rejected",
        ),
        (
            ready_request(
                credential_status=ready_credential_status(token_pair_present=False)
            ),
            {},
            "access_token_presence_metadata_required",
        ),
        (
            ready_request(
                credential_status=ready_credential_status(
                    expires_delta=timedelta(seconds=-1)
                )
            ),
            {},
            "credential_expired",
        ),
        (ready_request(), {"lease_active": False}, "lease_inactive"),
        (
            ready_request(
                credential_lease_ref=ready_lease(
                    created_at=NOW - timedelta(minutes=15),
                    expires_at=NOW - timedelta(seconds=1),
                )
            ),
            {},
            "lease_expired",
        ),
        (
            ready_request(
                credential_status=ready_credential_status(
                    expires_delta=timedelta(
                        minutes=15,
                        milliseconds=MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS - 1,
                    )
                )
            ),
            {},
            "insufficient_remaining_lease_lifetime",
        ),
        (ready_request(runtime_id="runtime.other"), {}, "runtime_mismatch"),
        (
            ready_request(),
            {"credential_store_id": "openai-codex.other"},
            "store_mismatch",
        ),
        (
            ready_request(),
            {"credential_provider_id": "openai-api"},
            "provider_mismatch",
        ),
        (
            ready_request(
                credential_status=ready_credential_status(active_provider_matches=False)
            ),
            {},
            "provider_mismatch",
        ),
    ],
)
def test_worker_ready_resolution_rejects_invalid_metadata(
    resolution_request: ProviderRuntimeResolutionRequest,
    kwargs: dict[str, object],
    code: str,
) -> None:
    with pytest.raises(ProviderRuntimeResolutionError) as exc_info:
        resolve_provider_runtime_profile(resolution_request, **kwargs)
    assert exc_info.value.code == code
    message = str(exc_info.value).lower()
    assert "forbidden-sensitive-value" not in message
    assert "auth.json" not in message


def test_refresh_presence_requirement_is_public_policy_metadata() -> None:
    request = ready_request()
    binding = resolve_provider_runtime_profile(request)
    requirement = binding.profile.credential_requirement
    assert requirement.access_token_presence_metadata_required is True
    assert requirement.refresh_token_presence_metadata_required is True
    assert request.credential_status.token_pair_present is True
