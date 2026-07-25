from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.provider_credentials import (
    ProviderClientTokenStatus,
    ProviderCredentialDeliveryLease,
    ProviderCredentialStatus,
)
from hermes_cli.agent_platform.provider_runtime import ProviderRuntimeResolutionRequest
from hermes_cli.agent_platform.provider_runtime.enums import (
    ProviderRuntimeAuthentication,
    ProviderRuntimeProvider,
    ProviderRuntimeTransport,
)
from hermes_cli.agent_platform.provider_runtime.resolution import (
    resolve_provider_runtime_profile,
)
from hermes_cli.agent_platform.provider_worker import (
    ProviderWorkerExecutionPolicy,
    ProviderWorkerFeaturePolicy,
    ProviderWorkerProfileState,
    ProviderWorkerResolutionRequest,
    get_provider_worker_profile,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    ResolvedProviderWorkerBinding,
)
from hermes_cli.agent_platform.provider_worker.profiles import (
    UnknownProviderWorkerProfileError,
)
from hermes_cli.agent_platform.provider_worker import resolution as worker_resolution
from hermes_cli.agent_platform.provider_worker.resolution import (
    ProviderWorkerConcurrencyPolicyError,
    ProviderWorkerCredentialRequirementError,
    ProviderWorkerFeaturePolicyError,
    ProviderWorkerProviderProfileMismatchError,
    ProviderWorkerQueuePolicyError,
    ProviderWorkerRequestBudgetError,
    ProviderWorkerResultBudgetError,
    ProviderWorkerTimeoutPolicyError,
    resolve_provider_worker_profile,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)
WORKER_PROFILE_ID = "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
PROVIDER_PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"


def ready_credential_status(
    *, expires_delta: timedelta = timedelta(minutes=20)
) -> ProviderCredentialStatus:
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
        last_refresh_utc=NOW - timedelta(minutes=1),
        expires_at_utc=NOW + expires_delta,
        client_token_status=ProviderClientTokenStatus(
            access_token_present=True,
            refresh_token_present=True,
            expiry_known=True,
            issued_at_utc=NOW - timedelta(minutes=1),
            expires_at_utc=NOW + expires_delta,
            remaining_lifetime_ms=int(expires_delta.total_seconds() * 1000),
            usable_for_bounded_lease=True,
        ),
    )


def ready_lease() -> ProviderCredentialDeliveryLease:
    return ProviderCredentialDeliveryLease(
        lease_id="lease.worker",
        runtime_id="runtime.worker",
        correlation_id="corr.worker",
        created_at_utc=NOW,
        expires_at_utc=NOW + timedelta(minutes=15),
    )


def provider_request(**overrides: object) -> ProviderRuntimeResolutionRequest:
    values: dict[str, object] = {
        "runtime_id": "runtime.worker",
        "correlation_id": "corr.worker",
        "requested_by": "p15.m8.resolution-test",
        "evaluated_at_utc": NOW,
        "credential_status": ready_credential_status(),
        "credential_lease_ref": ready_lease(),
    }
    values.update(overrides)
    return ProviderRuntimeResolutionRequest(**values)


def worker_request(**overrides: object) -> ProviderWorkerResolutionRequest:
    values: dict[str, object] = {
        "provider_resolution_request": provider_request(),
        "evaluated_at_utc": NOW,
    }
    values.update(overrides)
    return ProviderWorkerResolutionRequest(**values)


def test_valid_synthetic_provider_binding_is_ready_for_inference_gate() -> None:
    binding = resolve_provider_worker_profile(worker_request())

    assert isinstance(binding, ResolvedProviderWorkerBinding)
    assert binding.worker_profile.profile_id == WORKER_PROFILE_ID
    assert binding.provider_binding.profile.profile_id == PROVIDER_PROFILE_ID
    assert binding.resolved_state is ProviderWorkerProfileState.READY_FOR_INFERENCE_GATE
    assert binding.resolved_at_utc == NOW
    assert (
        binding.provider_binding.credential_store_ref.store_id == "openai-codex.primary"
    )
    assert binding.worker_profile.runtime_entitlement_verified is False
    assert binding.worker_profile.runtime_transport_verified is False
    assert binding.worker_profile.worker_runtime_verified is False
    assert "auth" + ".json" not in repr(binding).lower()


def test_unknown_worker_profile_is_rejected() -> None:
    with pytest.raises(UnknownProviderWorkerProfileError):
        resolve_provider_worker_profile(
            worker_request(worker_profile_id="worker.unknown")
        )


def test_wrong_provider_profile_is_rejected_before_provider_resolution() -> None:
    request = worker_request(
        provider_resolution_request=provider_request(profile_id="provider.other")
    )
    with pytest.raises(ProviderWorkerProviderProfileMismatchError) as exc_info:
        resolve_provider_worker_profile(request)
    assert exc_info.value.validation_category == "provider_runtime_profile_id"


def test_resolution_request_rejects_prompt_path_and_worker_runtime_overrides() -> None:
    request = worker_request()
    for forbidden_field in (
        "prompt",
        "provider",
        "model",
        "endpoint",
        "worker_command",
        "worker_argv",
        "workspace",
        "environment",
        "credential_path",
        "lease_path",
    ):
        payload = request.model_dump(mode="python")
        payload[forbidden_field] = "forbidden"
        with pytest.raises(ValidationError):
            ProviderWorkerResolutionRequest(**payload)


@pytest.mark.parametrize(
    ("profile_update", "expected_error"),
    [
        (
            {"credential_store_id": "openai-codex.other"},
            ProviderWorkerCredentialRequirementError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"maximum_concurrent_workers": 2}
                )
            },
            ProviderWorkerConcurrencyPolicyError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"maximum_concurrent_requests_per_worker": 2}
                )
            },
            ProviderWorkerConcurrencyPolicyError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"maximum_requests_per_worker_lifetime": 2}
                )
            },
            ProviderWorkerConcurrencyPolicyError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"request_queue_capacity": 1}
                )
            },
            ProviderWorkerQueuePolicyError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"provider_calls_per_request_maximum": 2}
                )
            },
            ProviderWorkerConcurrencyPolicyError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"model_list_calls_per_request_maximum": 1}
                )
            },
            ProviderWorkerFeaturePolicyError,
        ),
        (
            {
                "execution_policy": ProviderWorkerExecutionPolicy().model_copy(
                    update={"credential_refresh_calls_per_request_maximum": 1}
                )
            },
            ProviderWorkerFeaturePolicyError,
        ),
    ],
)
def test_worker_policy_drift_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    profile_update: dict[str, object],
    expected_error: type[Exception],
) -> None:
    profile = get_provider_worker_profile(WORKER_PROFILE_ID).model_copy(
        update=profile_update
    )
    monkeypatch.setattr(
        worker_resolution, "get_provider_worker_profile", lambda _id: profile
    )

    with pytest.raises(expected_error):
        resolve_provider_worker_profile(worker_request())


@pytest.mark.parametrize(
    "field_name",
    (
        "tools",
        "hosted_tools",
        "MCP",
        "streaming",
        "automatic_retry",
        "automatic_fallback",
        "persistent_memory",
        "process_reuse",
    ),
)
def test_enabled_worker_features_are_rejected(
    monkeypatch: pytest.MonkeyPatch, field_name: str
) -> None:
    execution = ProviderWorkerExecutionPolicy().model_copy(
        update={field_name: "enabled"}
    )
    profile = get_provider_worker_profile(WORKER_PROFILE_ID).model_copy(
        update={"execution_policy": execution}
    )
    monkeypatch.setattr(
        worker_resolution, "get_provider_worker_profile", lambda _id: profile
    )

    with pytest.raises(ProviderWorkerFeaturePolicyError):
        resolve_provider_worker_profile(worker_request())


@pytest.mark.parametrize(
    ("request_update", "expected_error"),
    [
        ({"maximum_prompt_tokens": 32_769}, ProviderWorkerRequestBudgetError),
        (
            {"reserved_system_instruction_tokens": 8_193},
            ProviderWorkerRequestBudgetError,
        ),
        ({"maximum_user_content_tokens": 24_577}, ProviderWorkerRequestBudgetError),
    ],
)
def test_token_budget_drift_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    request_update: dict[str, object],
    expected_error: type[Exception],
) -> None:
    base = get_provider_worker_profile(WORKER_PROFILE_ID)
    request_policy = base.request_policy.model_copy(update=request_update)
    profile = base.model_copy(update={"request_policy": request_policy})
    monkeypatch.setattr(
        worker_resolution, "get_provider_worker_profile", lambda _id: profile
    )

    with pytest.raises(expected_error):
        resolve_provider_worker_profile(worker_request())


def test_output_budget_drift_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    base = get_provider_worker_profile(WORKER_PROFILE_ID)
    result_policy = base.result_policy.model_copy(
        update={"maximum_output_tokens": 4_097}
    )
    profile = base.model_copy(update={"result_policy": result_policy})
    monkeypatch.setattr(
        worker_resolution, "get_provider_worker_profile", lambda _id: profile
    )

    with pytest.raises(ProviderWorkerResultBudgetError):
        resolve_provider_worker_profile(worker_request())


def test_timeout_increase_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    base = get_provider_worker_profile(WORKER_PROFILE_ID)
    timeout_policy = base.timeout_policy.model_copy(
        update={"connection_timeout_ms": 10_001}
    )
    profile = base.model_copy(update={"timeout_policy": timeout_policy})
    monkeypatch.setattr(
        worker_resolution, "get_provider_worker_profile", lambda _id: profile
    )

    with pytest.raises(ProviderWorkerTimeoutPolicyError):
        resolve_provider_worker_profile(worker_request())


@pytest.mark.parametrize(
    ("provider_profile_update", "expected_error"),
    [
        (
            {"provider": ProviderRuntimeProvider.OPENAI_CODEX.value},
            ProviderWorkerProviderProfileMismatchError,
        ),
        (
            {"authentication": ProviderRuntimeAuthentication.CHATGPT_OAUTH.value},
            ProviderWorkerProviderProfileMismatchError,
        ),
        (
            {"transport": ProviderRuntimeTransport.CODEX_RESPONSES.value},
            ProviderWorkerProviderProfileMismatchError,
        ),
    ],
)
def test_wrong_provider_authentication_or_transport_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    provider_profile_update: dict[str, object],
    expected_error: type[Exception],
) -> None:
    runtime_binding = resolve_provider_runtime_profile(provider_request())
    provider_profile = runtime_binding.profile.model_copy(
        update=provider_profile_update
    )
    bad_binding = runtime_binding.model_copy(update={"profile": provider_profile})
    monkeypatch.setattr(
        worker_resolution,
        "resolve_provider_runtime_profile",
        lambda _request: bad_binding,
    )

    with pytest.raises(expected_error):
        resolve_provider_worker_profile(worker_request())


def test_wrong_model_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime_binding = resolve_provider_runtime_profile(provider_request())
    model_policy = runtime_binding.profile.model_policy.model_copy(
        update={"model_id": "gpt-5.4"}
    )
    provider_profile = runtime_binding.profile.model_copy(
        update={"model_policy": model_policy}
    )
    bad_binding = runtime_binding.model_copy(update={"profile": provider_profile})
    monkeypatch.setattr(
        worker_resolution,
        "resolve_provider_runtime_profile",
        lambda _request: bad_binding,
    )

    with pytest.raises(ProviderWorkerProviderProfileMismatchError):
        resolve_provider_worker_profile(worker_request())


def test_resolution_source_has_no_credential_path_process_or_provider_call_authority() -> (
    None
):
    source = Path(worker_resolution.__file__).read_text(encoding="utf-8").lower()
    for forbidden in (
        "subprocess",
        "import requests",
        "requests.",
        "httpx",
        "urllib.request",
        "openai.",
        "models.list",
        "responses.create",
        "chat.completions",
        "auth" + ".json",
        "os.environ",
        "os.getenv",
        "path.home",
        "expanduser",
        "shell=true",
        "os.system",
        "os.popen",
    ):
        assert forbidden not in source


def test_synthetic_resolution_requires_no_real_token_or_path() -> None:
    binding = resolve_provider_worker_profile(worker_request())
    field_text = "\n".join(
        field
        for model in (type(binding.worker_profile), type(binding))
        for field in model.model_fields
    )
    assert "token" not in field_text
    assert "path" not in field_text
    assert "command" not in field_text
    assert "argv" not in field_text
