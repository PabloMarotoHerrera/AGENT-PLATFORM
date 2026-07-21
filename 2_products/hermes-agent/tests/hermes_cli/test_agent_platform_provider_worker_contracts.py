from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_worker as pw


SOURCE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_worker"
)

EXPECTED_EXPORTS = [
    "PROVIDER_WORKER_PROFILE_SCHEMA_VERSION",
    "ProviderWorkerProfileState",
    "ProviderWorkerInputKind",
    "ProviderWorkerOutputKind",
    "ProviderWorkerFeaturePolicy",
    "ProviderWorkerRequestState",
    "ProviderWorkerResultState",
    "ProviderWorkerFailureStage",
    "ProviderWorkerOversizedRequestPolicy",
    "ProviderWorkerExecutionPolicy",
    "ProviderWorkerRequestPolicy",
    "ProviderWorkerResultPolicy",
    "ProviderWorkerTimeoutPolicy",
    "BoundedProviderWorkerProfile",
    "BoundedProviderWorkerRequest",
    "BoundedProviderWorkerResult",
    "BoundedProviderWorkerFailure",
    "ProviderWorkerResolutionRequest",
    "get_provider_worker_profile",
    "list_provider_worker_profiles",
    "list_provider_worker_profile_ids",
]

FORBIDDEN_ROOT_EXPORTS = {
    "ResolvedProviderWorkerBinding",
    "resolve_provider_worker_profile",
    "serialize_worker_request",
    "deserialize_worker_request",
    "serialize_worker_result",
    "deserialize_worker_result",
    "ProviderWorkerError",
    "UnknownProviderWorkerProfileError",
}

WORKER_PROFILE_ID = "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
PROVIDER_PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_request(
    content: str = "synthetic worker request",
) -> pw.BoundedProviderWorkerRequest:
    return pw.BoundedProviderWorkerRequest(
        request_id="request.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        requested_by="p15.3.contract-test",
        submitted_at_utc=NOW,
        user_content=content,
    )


def make_failure() -> pw.BoundedProviderWorkerFailure:
    return pw.BoundedProviderWorkerFailure(
        failure_code="profile_validation_failed",
        stage=pw.ProviderWorkerFailureStage.PROFILE_VALIDATION,
        safe_message="bounded synthetic failure",
    )


def test_root_exports_exact_authorized_public_api_without_internal_aliases() -> None:
    assert pw.__all__ == EXPECTED_EXPORTS
    assert set(pw.__all__) == set(EXPECTED_EXPORTS)
    for name in FORBIDDEN_ROOT_EXPORTS:
        assert name not in pw.__all__
        assert not hasattr(pw, name)
    for name in pw.__all__:
        assert hasattr(pw, name)


def test_schema_version_and_enum_vocabulary_are_exact() -> None:
    assert pw.PROVIDER_WORKER_PROFILE_SCHEMA_VERSION == 1
    assert [member.value for member in pw.ProviderWorkerProfileState] == [
        "profile_ready_runtime_unverified",
        "ready_for_inference_gate",
        "blocked",
    ]
    assert [member.value for member in pw.ProviderWorkerInputKind] == ["text"]
    assert [member.value for member in pw.ProviderWorkerOutputKind] == ["text"]
    assert [member.value for member in pw.ProviderWorkerFeaturePolicy] == ["disabled"]
    assert [member.value for member in pw.ProviderWorkerRequestState] == [
        "accepted",
        "rejected",
    ]
    assert [member.value for member in pw.ProviderWorkerResultState] == [
        "completed",
        "failed",
        "cancelled",
    ]
    assert [member.value for member in pw.ProviderWorkerFailureStage] == [
        "profile_validation",
        "provider_binding",
        "request_validation",
        "execution",
        "cancellation",
        "shutdown",
    ]
    assert [member.value for member in pw.ProviderWorkerOversizedRequestPolicy] == [
        "fail_before_provider_call"
    ]


def test_worker_profile_and_policy_values_are_fixed() -> None:
    profile = pw.BoundedProviderWorkerProfile()
    execution = profile.execution_policy
    request = profile.request_policy
    result = profile.result_policy
    timeout = profile.timeout_policy

    assert profile.profile_id == WORKER_PROFILE_ID
    assert (
        profile.state is pw.ProviderWorkerProfileState.PROFILE_READY_RUNTIME_UNVERIFIED
    )
    assert profile.provider_runtime_profile_id == PROVIDER_PROFILE_ID
    assert profile.credential_store_id == "openai-codex.primary"
    assert profile.worker_process_required is True
    assert profile.inference_gate_required is True
    assert profile.controlled_lifecycle_gate_required is True
    assert profile.runtime_entitlement_verified is False
    assert profile.runtime_transport_verified is False
    assert profile.worker_runtime_verified is False
    assert profile.system_instruction_policy_id == (
        "worker.system.openai-codex.p15-pilot.v1"
    )
    assert profile.system_instruction_source == "tracked_internal_template"
    assert profile.caller_system_instruction_allowed is False
    assert profile.frontend_system_instruction_allowed is False
    assert profile.provider_supplied_system_instruction_allowed is False

    assert execution.maximum_concurrent_workers == 1
    assert execution.maximum_concurrent_requests_per_worker == 1
    assert execution.maximum_requests_per_worker_lifetime == 1
    assert execution.request_queue_capacity == 0
    assert execution.provider_calls_per_request_maximum == 1
    assert execution.model_list_calls_per_request_maximum == 0
    assert execution.credential_refresh_calls_per_request_maximum == 0
    for field_name in (
        "process_reuse",
        "persistent_memory",
        "conversation_history",
        "background_tasks",
        "subworkers",
        "subagents",
        "tools",
        "hosted_tools",
        "MCP",
        "streaming",
        "automatic_retry",
        "automatic_fallback",
    ):
        assert getattr(execution, field_name) is pw.ProviderWorkerFeaturePolicy.DISABLED

    assert request.input_kind is pw.ProviderWorkerInputKind.TEXT
    assert request.provider_runtime_profile_id == PROVIDER_PROFILE_ID
    assert request.maximum_prompt_tokens == 32_768
    assert request.reserved_system_instruction_tokens == 8_192
    assert request.maximum_user_content_tokens == 24_576
    assert request.maximum_request_utf8_bytes == 131_072
    assert request.maximum_user_content_utf8_bytes == 98_304
    assert (
        request.reserved_system_instruction_tokens + request.maximum_user_content_tokens
        <= request.maximum_prompt_tokens
    )
    assert request.caller_system_instructions_allowed is False
    assert request.caller_provider_allowed is False
    assert request.caller_model_allowed is False
    assert request.caller_endpoint_allowed is False
    assert request.caller_generation_parameters_allowed is False
    assert request.caller_timeout_parameters_allowed is False
    assert request.caller_tools_allowed is False
    assert request.caller_metadata_passthrough_allowed is False
    assert (
        request.oversized_request_policy
        is pw.ProviderWorkerOversizedRequestPolicy.FAIL_BEFORE_PROVIDER_CALL
    )

    assert result.output_kind is pw.ProviderWorkerOutputKind.TEXT
    assert result.maximum_output_tokens == 4_096
    assert result.maximum_output_utf8_bytes == 32_768
    assert result.maximum_result_envelope_utf8_bytes == 65_536
    assert result.raw_provider_response_allowed is False
    assert result.reasoning_trace_allowed is False
    assert result.tool_calls_allowed is False
    assert result.stream_chunks_allowed is False
    assert result.provider_headers_allowed is False
    assert result.credential_metadata_allowed is False
    assert result.automatic_file_write_allowed is False
    assert result.persistent_output_allowed is False

    assert timeout.startup_timeout_ms == 30_000
    assert timeout.connection_timeout_ms == 10_000
    assert timeout.response_header_timeout_ms == 30_000
    assert timeout.complete_inference_timeout_ms == 120_000
    assert timeout.cancellation_deadline_ms == 10_000
    assert timeout.worker_shutdown_deadline_ms == 15_000
    assert timeout.maximum_worker_lifetime_ms == 180_000
    assert timeout.caller_timeout_override_allowed is False
    assert timeout.frontend_timeout_override_allowed is False
    assert timeout.environment_timeout_override_allowed is False


@pytest.mark.parametrize(
    "model_cls",
    (
        pw.ProviderWorkerExecutionPolicy,
        pw.ProviderWorkerRequestPolicy,
        pw.ProviderWorkerResultPolicy,
        pw.ProviderWorkerTimeoutPolicy,
        pw.BoundedProviderWorkerProfile,
    ),
)
def test_public_profile_contracts_are_immutable_and_reject_extra_fields(
    model_cls: type,
) -> None:
    instance = model_cls()
    with pytest.raises(ValidationError):
        model_cls(**(instance.model_dump(mode="python") | {"unexpected": "field"}))
    with pytest.raises(ValidationError):
        model_cls(schema_version=2)
    with pytest.raises(ValidationError):
        instance.profile_id = "mutated"  # type: ignore[attr-defined]


def test_request_contract_rejects_overrides_and_hides_content_from_repr() -> None:
    request = make_request("forbidden-sensitive-request-body")
    assert request.schema_version == 1
    assert request.profile_id == WORKER_PROFILE_ID
    assert request.provider_runtime_profile_id == PROVIDER_PROFILE_ID
    assert request.input_kind is pw.ProviderWorkerInputKind.TEXT
    assert request.submitted_at_utc.tzinfo is timezone.utc
    assert "forbidden-sensitive-request-body" not in repr(request)

    for forbidden_field in (
        "system_instructions",
        "provider",
        "model",
        "endpoint",
        "generation_parameters",
        "timeout_values",
        "tools",
        "MCP",
        "streaming",
        "retry",
        "fallback",
        "conversation_history",
        "file_path",
        "environment",
        "command",
        "argv",
    ):
        payload = request.model_dump(mode="python")
        payload[forbidden_field] = "forbidden"
        with pytest.raises(ValidationError):
            pw.BoundedProviderWorkerRequest(**payload)


def test_request_validation_enforces_utc_safe_ids_and_utf8_byte_bounds() -> None:
    with pytest.raises(ValidationError):
        pw.BoundedProviderWorkerRequest(
            request_id="bad space",
            runtime_id="runtime.contract",
            correlation_id="corr.contract",
            requested_by="p15.3.contract-test",
            submitted_at_utc=NOW,
            user_content="synthetic",
        )
    with pytest.raises(ValidationError):
        pw.BoundedProviderWorkerRequest(
            request_id="request.contract",
            runtime_id="runtime.contract",
            correlation_id="corr.contract",
            requested_by="p15.3.contract-test",
            submitted_at_utc=datetime(2026, 1, 1),
            user_content="synthetic",
        )
    with pytest.raises(ValidationError):
        make_request("")
    with pytest.raises(ValidationError):
        make_request("\x00")
    with pytest.raises(ValidationError):
        make_request("x" * 98_305)


def test_result_and_failure_contracts_are_bounded_and_hide_output_repr() -> None:
    completed = pw.BoundedProviderWorkerResult(
        request_id="request.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        state=pw.ProviderWorkerResultState.COMPLETED,
        completed_at_utc=NOW,
        output_text="forbidden-sensitive-result-body",
    )
    failed = pw.BoundedProviderWorkerResult(
        request_id="request.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        state=pw.ProviderWorkerResultState.FAILED,
        completed_at_utc=NOW,
        failure=make_failure(),
    )
    cancelled = pw.BoundedProviderWorkerResult(
        request_id="request.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        state=pw.ProviderWorkerResultState.CANCELLED,
        completed_at_utc=NOW,
        failure=pw.BoundedProviderWorkerFailure(
            failure_code="cancelled",
            stage=pw.ProviderWorkerFailureStage.CANCELLATION,
            safe_message="bounded synthetic cancellation",
        ),
    )

    assert completed.output_kind is pw.ProviderWorkerOutputKind.TEXT
    assert completed.usage_record_id is None
    assert completed.failure is None
    assert "forbidden-sensitive-result-body" not in repr(completed)
    assert failed.output_text is None
    assert failed.failure is not None
    assert failed.failure.retryable is False
    assert cancelled.output_text is None

    with pytest.raises(ValidationError):
        pw.BoundedProviderWorkerResult(
            request_id="request.contract",
            runtime_id="runtime.contract",
            correlation_id="corr.contract",
            state=pw.ProviderWorkerResultState.COMPLETED,
            completed_at_utc=NOW,
            failure=make_failure(),
        )
    with pytest.raises(ValidationError):
        pw.BoundedProviderWorkerResult(
            request_id="request.contract",
            runtime_id="runtime.contract",
            correlation_id="corr.contract",
            state=pw.ProviderWorkerResultState.FAILED,
            completed_at_utc=NOW,
            output_text="synthetic",
        )
    with pytest.raises(ValidationError):
        pw.BoundedProviderWorkerResult(
            request_id="request.contract",
            runtime_id="runtime.contract",
            correlation_id="corr.contract",
            state=pw.ProviderWorkerResultState.COMPLETED,
            completed_at_utc=NOW,
            output_text="x" * 32_769,
        )


def test_public_models_contain_no_secret_path_process_or_account_authority() -> None:
    unsafe_field_fragments = (
        "auth_json",
        "credential_path",
        "lease_path",
        "command",
        "argv",
        "workspace",
        "pid",
        "account",
        "email",
        "quota",
    )
    public_models = (
        pw.ProviderWorkerExecutionPolicy,
        pw.ProviderWorkerRequestPolicy,
        pw.ProviderWorkerResultPolicy,
        pw.ProviderWorkerTimeoutPolicy,
        pw.BoundedProviderWorkerProfile,
        pw.BoundedProviderWorkerRequest,
        pw.BoundedProviderWorkerResult,
        pw.BoundedProviderWorkerFailure,
        pw.ProviderWorkerResolutionRequest,
    )
    for model in public_models:
        for field_name in model.model_fields:
            assert not any(
                fragment in field_name for fragment in unsafe_field_fragments
            )


def test_provider_worker_source_has_no_operational_authority() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in sorted(SOURCE_ROOT.glob("*.py"))
    )
    for forbidden in (
        "subprocess",
        "socket.",
        "import requests",
        "requests.get",
        "requests.post",
        "httpx",
        "urllib.request",
        "openai.",
        "models.list",
        "responses.create",
        "chat.completions",
        "oauth call",
        "auth" + ".json",
        "os.environ",
        "os.getenv",
        "path.home",
        "expanduser",
        "shell=true",
        "os.system",
        "os.popen",
        "sqlite",
    ):
        assert forbidden not in source
