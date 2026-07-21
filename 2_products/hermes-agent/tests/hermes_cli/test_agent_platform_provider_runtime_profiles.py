from __future__ import annotations

from types import MappingProxyType

import pytest

from hermes_cli.agent_platform import provider_runtime as public_api
from hermes_cli.agent_platform.provider_runtime.enums import ProviderRuntimeProfileState
from hermes_cli.agent_platform.provider_runtime.profiles import (
    OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE,
    UnknownProviderRuntimeProfileError,
    _PROVIDER_RUNTIME_PROFILES,
    get_provider_runtime_profile,
    list_provider_runtime_profile_ids,
    list_provider_runtime_profiles,
)


PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"


def test_single_immutable_profile_is_registered() -> None:
    assert isinstance(_PROVIDER_RUNTIME_PROFILES, MappingProxyType)
    assert list_provider_runtime_profile_ids() == (PROFILE_ID,)
    profiles = list_provider_runtime_profiles()
    assert profiles == (OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE,)
    assert (
        get_provider_runtime_profile(PROFILE_ID)
        is OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE
    )
    assert public_api.list_provider_runtime_profile_ids() == (PROFILE_ID,)
    assert public_api.list_provider_runtime_profiles() == profiles
    assert public_api.get_provider_runtime_profile(PROFILE_ID) is profiles[0]

    profile = profiles[0]
    assert profile.profile_id == PROFILE_ID
    assert profile.state is ProviderRuntimeProfileState.RUNTIME_UNVERIFIED
    assert profile.provider.value == "openai-codex"
    assert profile.authentication.value == "chatgpt_oauth"
    assert profile.transport.value == "codex_responses"
    assert profile.model_policy.model_id == "gpt-5.5"
    assert profile.endpoint_policy.provider_endpoint == (
        "https://chatgpt.com/backend-api/codex"
    )


def test_registry_rejects_unknown_profiles_and_external_mutation() -> None:
    with pytest.raises(UnknownProviderRuntimeProfileError):
        get_provider_runtime_profile("openai-api.gpt-5.5")
    with pytest.raises(TypeError):
        _PROVIDER_RUNTIME_PROFILES["other"] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE  # type: ignore[index]


def test_profile_has_worker_requirement_but_no_runtime_verification_claims() -> None:
    profile = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE
    assert profile.worker_profile_required is True
    assert profile.runtime_entitlement_verified is False
    assert profile.runtime_transport_verified is False
    assert profile.generation_policy.streaming.value == "disabled"
    assert profile.generation_policy.tools.value == "disabled"
    assert profile.generation_policy.MCP.value == "disabled"
    assert profile.generation_policy.automatic_retry.value == "disabled"
    assert profile.generation_policy.automatic_fallback.value == "disabled"
