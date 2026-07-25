from __future__ import annotations

from hermes_cli.agent_platform import provider_worker as pw
from hermes_cli.agent_platform.provider_worker.profiles import (
    UnknownProviderWorkerProfileError,
)


WORKER_PROFILE_ID = "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
PROVIDER_PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"


def test_single_immutable_worker_profile_registry_is_deterministic() -> None:
    ids = pw.list_provider_worker_profile_ids()
    profiles = pw.list_provider_worker_profiles()

    assert ids == (WORKER_PROFILE_ID,)
    assert len(profiles) == 1
    assert profiles == (pw.get_provider_worker_profile(WORKER_PROFILE_ID),)
    assert profiles[0] is pw.get_provider_worker_profile(WORKER_PROFILE_ID)
    assert isinstance(profiles, tuple)
    assert isinstance(ids, tuple)


def test_unknown_worker_profile_fails_closed() -> None:
    try:
        pw.get_provider_worker_profile("worker.unknown")
    except UnknownProviderWorkerProfileError as exc:
        assert exc.error_code == "unknown_provider_worker_profile"
        assert exc.worker_profile_id == "worker.unknown"
        assert "worker.unknown" in str(exc)
    else:
        raise AssertionError("unknown worker profile was accepted")


def test_registered_profile_binds_provider_runtime_and_credential_store() -> None:
    profile = pw.get_provider_worker_profile(WORKER_PROFILE_ID)

    assert profile.schema_version == 1
    assert profile.profile_id == WORKER_PROFILE_ID
    assert profile.provider_runtime_profile_id == PROVIDER_PROFILE_ID
    assert profile.credential_store_id == "openai-codex.primary"
    assert (
        profile.state is pw.ProviderWorkerProfileState.PROFILE_READY_RUNTIME_UNVERIFIED
    )
    assert profile.inference_gate_required is True
    assert profile.controlled_lifecycle_gate_required is True
    assert profile.runtime_entitlement_verified is False
    assert profile.runtime_transport_verified is False
    assert profile.worker_runtime_verified is False


def test_registered_profile_preserves_single_request_zero_queue_policy() -> None:
    execution = pw.get_provider_worker_profile(WORKER_PROFILE_ID).execution_policy

    assert execution.maximum_concurrent_workers == 1
    assert execution.maximum_concurrent_requests_per_worker == 1
    assert execution.maximum_requests_per_worker_lifetime == 1
    assert execution.request_queue_capacity == 0
    assert execution.provider_calls_per_request_maximum == 1
    assert execution.model_list_calls_per_request_maximum == 0
    assert execution.credential_refresh_calls_per_request_maximum == 0


def test_registered_profile_disables_worker_features() -> None:
    execution = pw.get_provider_worker_profile(WORKER_PROFILE_ID).execution_policy

    assert execution.tools is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.hosted_tools is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.MCP is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.streaming is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.automatic_retry is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.automatic_fallback is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.persistent_memory is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.process_reuse is pw.ProviderWorkerFeaturePolicy.DISABLED
    assert execution.conversation_history is pw.ProviderWorkerFeaturePolicy.DISABLED


def test_registry_source_has_no_dynamic_discovery_or_selection() -> None:
    import inspect

    from hermes_cli.agent_platform.provider_worker import profiles

    source = inspect.getsource(profiles).lower()
    for forbidden in (
        "importlib",
        "pkgutil",
        "entry_points",
        "os.environ",
        "getenv",
        "plugin",
        "frontend",
        "load",
    ):
        assert forbidden not in source
