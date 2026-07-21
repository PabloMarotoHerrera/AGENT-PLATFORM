from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_runtime as pr
from hermes_cli.agent_platform.provider_credentials import (
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

FORBIDDEN_ROOT_EXPORTS = {
    "ResolvedProviderRuntimeBinding",
    "resolve_provider_runtime_profile",
    "ProviderRuntimeResolution",
    "ProviderRuntimeAuthKind",
    "ProviderRuntimeBillingRoute",
    "ProviderRuntimeCredentialPolicy",
    "ProviderRuntimeExecutionPolicy",
    "ProviderRuntimeIdentity",
    "ProviderRuntimeOverrideSource",
    "ProviderRuntimeRequestPolicy",
}


def ready_credential_status(now: datetime) -> ProviderCredentialStatus:
    return ProviderCredentialStatus(
        configured=True,
        durable_store_present=True,
        durable_store_valid=True,
        protection_valid=True,
        provider_state_present=True,
        pool_state_present=True,
        token_pair_present=True,
        credential_count=1,
        active_provider_matches=True,
        last_refresh_utc=now,
        expires_at_utc=now,
    )


def ready_lease(now: datetime) -> ProviderCredentialDeliveryLease:
    return ProviderCredentialDeliveryLease(
        lease_id="lease.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        created_at_utc=now,
        expires_at_utc=now + timedelta(seconds=1),
    )


def test_root_exports_exact_authorized_public_api_without_legacy_aliases() -> None:
    assert pr.__all__ == EXPECTED_EXPORTS
    assert set(pr.__all__) == set(EXPECTED_EXPORTS)
    for name in FORBIDDEN_ROOT_EXPORTS:
        assert name not in pr.__all__
        assert not hasattr(pr, name)
    for name in pr.__all__:
        assert hasattr(pr, name)


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
    assert [member.value for member in pr.ProviderRuntimeProfileState] == [
        "strategy_ready",
        "credential_ready",
        "ready_for_worker_profile",
        "runtime_unverified",
        "blocked",
    ]
    assert [member.value for member in pr.ProviderFeaturePolicy] == ["disabled"]
    assert [member.value for member in pr.ProviderUsageEvidenceSource] == [
        "provider_reported_when_available",
        "provider_reported_or_locally_summed",
        "provider_reported",
        "provider_reported_when_safe",
        "locally_derived",
        "account_specific_when_exposed",
        "unavailable_by_default",
    ]


def test_public_profile_uses_exact_accepted_policy_vocabulary() -> None:
    profile = pr.list_provider_runtime_profiles()[0]

    assert pr.ProviderRuntimeProfile.model_fields.keys() == {
        "schema_version",
        "profile_id",
        "state",
        "provider",
        "authentication",
        "transport",
        "endpoint_policy",
        "model_policy",
        "credential_requirement",
        "generation_policy",
        "timeout_policy",
        "usage_evidence_policy",
        "worker_profile_required",
        "runtime_entitlement_verified",
        "runtime_transport_verified",
    }
    assert profile.profile_id == "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    assert profile.state is pr.ProviderRuntimeProfileState.RUNTIME_UNVERIFIED
    assert profile.provider is pr.ProviderRuntimeProvider.OPENAI_CODEX
    assert profile.authentication is pr.ProviderRuntimeAuthentication.CHATGPT_OAUTH
    assert profile.transport is pr.ProviderRuntimeTransport.CODEX_RESPONSES
    assert profile.worker_profile_required is True
    assert profile.runtime_entitlement_verified is False
    assert profile.runtime_transport_verified is False
    assert profile.endpoint_policy.provider_endpoint == (
        "https://chatgpt.com/backend-api/codex"
    )
    assert profile.model_policy.model_id == "gpt-5.5"
    assert profile.model_policy.identifier_kind is (
        pr.ProviderModelIdentifierKind.MUTABLE_BACKEND_SLUG
    )
    assert profile.credential_requirement.credential_store_id == "openai-codex.primary"
    assert profile.credential_requirement.credential_count == 1
    assert profile.credential_requirement.active_lease_required is True
    assert (
        profile.credential_requirement.access_token_presence_metadata_required is True
    )
    assert (
        profile.credential_requirement.refresh_token_presence_metadata_required is True
    )


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
    assert generation.MCP is pr.ProviderFeaturePolicy.DISABLED
    assert generation.automatic_retry is pr.ProviderFeaturePolicy.DISABLED
    assert generation.automatic_fallback is pr.ProviderFeaturePolicy.DISABLED
    assert generation.oversized_request_posture == "fail_before_provider_call"

    assert usage.input_tokens is (
        pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    assert usage.cached_input_tokens is (
        pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    assert usage.output_tokens is (
        pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    assert usage.total_tokens is (
        pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_OR_LOCALLY_SUMMED
    )
    assert usage.returned_model_id is pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED
    assert usage.finish_reason is (
        pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_AVAILABLE
    )
    assert usage.provider_request_id is (
        pr.ProviderUsageEvidenceSource.PROVIDER_REPORTED_WHEN_SAFE
    )
    assert usage.elapsed_time_ms is pr.ProviderUsageEvidenceSource.LOCALLY_DERIVED
    assert usage.subscription_quota_signal is (
        pr.ProviderUsageEvidenceSource.ACCOUNT_SPECIFIC_WHEN_EXPOSED
    )
    assert usage.credit_consumption_signal is (
        pr.ProviderUsageEvidenceSource.ACCOUNT_SPECIFIC_WHEN_EXPOSED
    )
    assert usage.exact_marginal_request_cost is (
        pr.ProviderUsageEvidenceSource.UNAVAILABLE_BY_DEFAULT
    )


def test_resolution_request_public_shape_is_safe_and_rejects_overrides() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    request = pr.ProviderRuntimeResolutionRequest(
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        requested_by="p15.2.contract-test",
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
    assert request.evaluated_at_utc.tzinfo is timezone.utc
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


def test_public_contract_models_contain_no_path_token_or_runtime_authority() -> None:
    forbidden_field_fragments = (
        "path",
        "root",
        "home",
        "auth_file",
        "environment",
        "command",
        "argv",
    )
    public_models = (
        pr.ProviderEndpointPolicy,
        pr.ProviderModelPolicy,
        pr.ProviderCredentialRequirement,
        pr.ProviderGenerationPolicy,
        pr.ProviderTimeoutPolicy,
        pr.ProviderUsageEvidencePolicy,
        pr.ProviderRuntimeProfile,
        pr.ProviderRuntimeResolutionRequest,
    )
    for model in public_models:
        for field_name in model.model_fields:
            assert not any(
                fragment in field_name for fragment in forbidden_field_fragments
            )


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
