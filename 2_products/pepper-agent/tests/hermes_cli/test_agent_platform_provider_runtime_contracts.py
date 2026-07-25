from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_runtime as pr
from hermes_cli.agent_platform.provider_credentials import (
    ProviderClientTokenStatus,
    ProviderCredentialDeliveryLease,
    ProviderCredentialStatus,
)


SOURCE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_runtime"
)

EXPECTED_EXPORTS = [
    "PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION",
    "ProviderRuntimeProvider",
    "ProviderRuntimeAuthentication",
    "ProviderRuntimeTransport",
    "ProviderModelIdentifierKind",
    "ProviderRuntimeProfileState",
    "ProviderFeaturePolicy",
    "ProviderUsageEvidenceSource",
    "ProviderEndpointPolicy",
    "ProviderModelPolicy",
    "ProviderCredentialRequirement",
    "ProviderGenerationPolicy",
    "ProviderTimeoutPolicy",
    "ProviderUsageEvidencePolicy",
    "ProviderRuntimeProfile",
    "ProviderRuntimeResolutionRequest",
    "get_provider_runtime_profile",
    "list_provider_runtime_profiles",
    "list_provider_runtime_profile_ids",
]


def ready_client_token_status(now: datetime) -> ProviderClientTokenStatus:
    return ProviderClientTokenStatus(
        access_token_present=True,
        refresh_token_present=True,
        expiry_known=True,
        issued_at_utc=now - timedelta(minutes=1),
        expires_at_utc=now + timedelta(minutes=20),
        remaining_lifetime_ms=1_200_000,
        usable_for_bounded_lease=True,
    )


def ready_credential_status(now: datetime) -> ProviderCredentialStatus:
    return ProviderCredentialStatus(
        configured=True,
        durable_store_present=True,
        durable_store_valid=True,
        protection_valid=True,
        provider_state_present=False,
        pool_state_present=True,
        token_pair_present=True,
        credential_count=1,
        active_provider_matches=True,
        last_refresh_utc=now - timedelta(minutes=1),
        expires_at_utc=now + timedelta(minutes=20),
        client_token_status=ready_client_token_status(now),
    )


def ready_lease(now: datetime) -> ProviderCredentialDeliveryLease:
    return ProviderCredentialDeliveryLease(
        lease_id="lease.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        created_at_utc=now,
        expires_at_utc=now + timedelta(minutes=15),
    )


def test_root_exports_exact_authorized_public_api_without_legacy_aliases() -> None:
    assert pr.__all__ == EXPECTED_EXPORTS
    for name in EXPECTED_EXPORTS:
        assert hasattr(pr, name)
    for forbidden in (
        "ResolvedProviderRuntimeBinding",
        "resolve_provider_runtime_profile",
    ):
        assert forbidden not in pr.__all__
        assert not hasattr(pr, forbidden)


def test_enum_vocabulary_and_values_are_exact() -> None:
    assert pr.PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION == 1
    assert [member.value for member in pr.ProviderRuntimeProvider] == ["openai-codex"]
    assert [member.value for member in pr.ProviderRuntimeAuthentication] == [
        "chatgpt_oauth"
    ]
    assert [member.value for member in pr.ProviderRuntimeTransport] == [
        "codex_responses"
    ]
    assert [member.value for member in pr.ProviderModelIdentifierKind] == [
        "mutable_backend_slug"
    ]
    assert [member.value for member in pr.ProviderFeaturePolicy] == ["disabled"]


def test_public_profile_uses_exact_accepted_policy_vocabulary() -> None:
    profile = pr.list_provider_runtime_profiles()[0]

    assert profile.profile_id == "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    assert profile.state is pr.ProviderRuntimeProfileState.RUNTIME_UNVERIFIED
    assert profile.provider is pr.ProviderRuntimeProvider.OPENAI_CODEX
    assert profile.authentication is pr.ProviderRuntimeAuthentication.CHATGPT_OAUTH
    assert profile.transport is pr.ProviderRuntimeTransport.CODEX_RESPONSES
    assert profile.worker_profile_required is True
    assert profile.runtime_entitlement_verified is False
    assert profile.provider_reachability_verified is False
    assert profile.runtime_transport_verified is False
    assert profile.inference_success_verified is False
    assert (
        profile.endpoint_policy.provider_endpoint
        == "https://chatgpt.com/backend-api/codex"
    )
    assert profile.endpoint_policy.base_url_override_allowed is False
    assert profile.model_policy.model_id == "gpt-5.5"
    assert (
        profile.model_policy.identifier_kind
        is pr.ProviderModelIdentifierKind.MUTABLE_BACKEND_SLUG
    )
    requirement = profile.credential_requirement
    assert requirement.credential_store_id == "openai-codex.primary"
    assert requirement.credential_count == 1
    assert requirement.active_lease_required is True
    assert requirement.client_token_metadata_required is True


def test_generation_policy_and_usage_evidence_policy_are_explicit_and_distinct() -> (
    None
):
    profile = pr.list_provider_runtime_profiles()[0]
    generation = profile.generation_policy
    usage = profile.usage_evidence_policy

    assert generation.maximum_prompt_tokens == 32_768
    assert generation.reserved_system_instruction_tokens == 8_192
    assert generation.maximum_user_content_tokens == 24_576
    assert generation.maximum_output_tokens == 4_096
    assert generation.reasoning_effort == "medium"
    assert generation.streaming is pr.ProviderFeaturePolicy.DISABLED
    assert generation.tools is pr.ProviderFeaturePolicy.DISABLED
    assert generation.hosted_tools is pr.ProviderFeaturePolicy.DISABLED
    assert generation.MCP is pr.ProviderFeaturePolicy.DISABLED
    assert generation.automatic_retry is pr.ProviderFeaturePolicy.DISABLED
    assert generation.automatic_fallback is pr.ProviderFeaturePolicy.DISABLED
    assert generation.oversized_request_posture == "fail_before_provider_call"
    assert (
        usage.input_tokens
        is pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    assert (
        usage.total_tokens
        is pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_OR_LOCALLY_SUMMED
    )
    assert (
        usage.exact_marginal_request_cost
        is pr.ProviderUsageEvidenceSource.UNAVAILABLE_BY_DEFAULT
    )


def test_resolution_request_public_shape_is_safe_and_rejects_overrides() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    request = pr.ProviderRuntimeResolutionRequest(
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        requested_by="p15.m8.contract-test",
        evaluated_at_utc=now,
        credential_status=ready_credential_status(now),
        credential_lease_ref=ready_lease(now),
    )

    assert set(pr.ProviderRuntimeResolutionRequest.model_fields) == {
        "schema_version",
        "profile_id",
        "runtime_id",
        "correlation_id",
        "requested_by",
        "evaluated_at_utc",
        "credential_status",
        "credential_lease_ref",
    }
    assert request.profile_id == "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    for forbidden_field in (
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
    ):
        payload = request.model_dump()
        payload[forbidden_field] = "forbidden"
        with pytest.raises(ValidationError):
            pr.ProviderRuntimeResolutionRequest(**payload)


def test_provider_runtime_source_has_no_execution_or_credential_authority() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in sorted(SOURCE_ROOT.glob("*.py"))
    )
    for forbidden in (
        "httpx",
        "requests",
        "openai.",
        "subprocess",
        "popen",
        "webbrowser",
        "socket.",
        "os.environ",
        "getenv",
        "get_secret",
        "load_pool",
        "auth.json",
        "~/.codex",
        "openai_api_key",
        "hermes_codex_base_url",
        "openai_base_url",
    ):
        assert forbidden not in source
