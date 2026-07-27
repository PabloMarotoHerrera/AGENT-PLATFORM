from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_failure_policy as fp
from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingOutcome,
    ProviderTimeoutStage,
)


SOURCE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_failure_policy"
)

EXPECTED_EXPORTS = [
    "PROVIDER_FAILURE_POLICY_SCHEMA_VERSION",
    "PROVIDER_FAILURE_POLICY_ID",
    "PROVIDER_FAILURE_PROVIDER",
    "PROVIDER_FAILURE_AUTHENTICATION",
    "PROVIDER_FAILURE_ENDPOINT",
    "PROVIDER_FAILURE_TRANSPORT",
    "MAXIMUM_RETRY_AFTER_MS",
    "ProviderFailureCategory",
    "ProviderFailureStage",
    "ProviderFailureOrigin",
    "ProviderRetryDisposition",
    "ProviderRecoveryAction",
    "ProviderRetryDelaySource",
    "ProviderSDKExceptionKind",
    "ProviderFailureAccountingLinkState",
    "ProviderFailurePolicy",
    "ProviderFailureSignal",
    "ProviderFailureClassification",
    "ProviderFailureRecord",
    "ProviderRetryDecision",
    "ProviderFailureAccountingProjection",
    "ProviderFailureAccountingLink",
    "build_failure_record_id",
    "classify_openai_codex_failure",
    "build_provider_failure_record",
    "build_provider_retry_decision",
    "project_failure_to_accounting",
    "validate_failure_accounting_link",
    "resolve_safe_failure_summary",
]


def synthetic_signal(**overrides: object) -> fp.ProviderFailureSignal:
    values = {
        "origin": fp.ProviderFailureOrigin.HTTP_RESPONSE,
        "stage": fp.ProviderFailureStage.DISPATCH,
        "HTTP_status": 500,
        "provider_dispatch_occurred": True,
        "provider_response_id_present": True,
    }
    values.update(overrides)
    return fp.ProviderFailureSignal(**values)


def synthetic_record(**overrides: object) -> fp.ProviderFailureRecord:
    values = {
        "request_id": "request.contract",
        "runtime_id": "runtime.contract",
        "correlation_id": "corr.contract",
        "signal": synthetic_signal(),
        "usage_record_id": "usage.contract",
    }
    values.update(overrides)
    return fp.build_provider_failure_record(**values)


def test_root_exports_exact_authorized_public_api_without_internal_helpers() -> None:
    assert fp.__all__ == EXPECTED_EXPORTS
    for name in EXPECTED_EXPORTS:
        assert hasattr(fp, name)
    for forbidden in (
        "_category_from_status_and_text",
        "_CREDENTIAL_EXPIRED_PATTERNS",
        "sleep_then_retry",
        "rotate_credential",
        "fallback_model",
        "runtime_client",
    ):
        assert forbidden not in fp.__all__
        assert not hasattr(fp, forbidden)


def test_schema_policy_identity_and_disabled_execution_posture() -> None:
    policy = fp.ProviderFailurePolicy()

    assert fp.PROVIDER_FAILURE_POLICY_SCHEMA_VERSION == 1
    assert policy.policy_id == (
        "failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert policy.provider_runtime_profile_id == (
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert policy.worker_profile_id == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert policy.accounting_policy_id == (
        "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert policy.provider == "openai-codex"
    assert policy.authentication == "chatgpt_oauth"
    assert policy.endpoint == "https://chatgpt.com/backend-api/codex"
    assert policy.model == "gpt-5.5"
    assert policy.transport == "codex_responses"
    assert policy.automatic_retry_allowed is False
    assert policy.maximum_automatic_retries == 0
    assert policy.maximum_provider_dispatches_per_request == 1
    assert policy.same_worker_retry_allowed is False
    assert policy.same_request_retry_allowed is False
    assert policy.credential_rotation_allowed is False
    assert policy.automatic_fallback_allowed is False
    assert policy.model_fallback_allowed is False
    assert policy.endpoint_fallback_allowed is False
    assert policy.automatic_refresh_allowed is False


def test_exact_enum_vocabularies() -> None:
    assert [item.value for item in fp.ProviderFailureCategory] == [
        "authentication",
        "authorization",
        "credential_expired",
        "entitlement",
        "quota",
        "rate_limit",
        "provider_overloaded",
        "provider_server_error",
        "connection_failure",
        "connection_timeout",
        "response_header_timeout",
        "complete_inference_timeout",
        "cancellation_timeout",
        "worker_shutdown_timeout",
        "tls_verification",
        "transport_protocol",
        "request_invalid",
        "request_too_large",
        "context_overflow",
        "model_unavailable",
        "content_policy",
        "provider_incomplete",
        "provider_failed",
        "stream_truncated",
        "cancelled_by_owner",
        "accounting_invalid",
        "unknown",
    ]
    assert [item.value for item in fp.ProviderFailureStage] == [
        "preflight",
        "credential",
        "dispatch",
        "connection",
        "response_header",
        "stream",
        "terminal",
        "cancellation",
        "shutdown",
        "accounting",
    ]
    assert [item.value for item in fp.ProviderFailureOrigin] == [
        "local_validation",
        "SDK_exception",
        "HTTP_response",
        "SSE_error",
        "terminal_event",
        "owner_cancellation",
        "accounting_validation",
    ]
    assert [item.value for item in fp.ProviderRetryDisposition] == [
        "never",
        "new_request_after_human_action",
        "new_request_after_external_condition",
        "new_request_after_request_change",
        "new_request_after_configuration_change",
        "operator_review_required",
    ]
    assert [item.value for item in fp.ProviderRecoveryAction] == [
        "abort",
        "reauthenticate",
        "review_authorization",
        "review_entitlement",
        "wait_for_external_reset",
        "reduce_request",
        "correct_transport",
        "correct_configuration",
        "preserve_evidence_and_escalate",
        "cancel_and_cleanup",
    ]
    assert [item.value for item in fp.ProviderRetryDelaySource] == [
        "none",
        "provider_retry_after",
        "policy_advisory",
    ]
    assert [item.value for item in fp.ProviderSDKExceptionKind] == [
        "none",
        "connect_error",
        "read_timeout",
        "remote_protocol_error",
        "SSL_verification_error",
        "cancelled",
        "generic",
    ]
    assert [item.value for item in fp.ProviderFailureAccountingLinkState] == [
        "matched",
        "matched_without_accounting",
        "missing",
        "mismatched",
    ]


@pytest.mark.parametrize(
    "instance",
    (
        fp.ProviderFailurePolicy(),
        synthetic_signal(),
        synthetic_record(),
        fp.build_provider_retry_decision(synthetic_record()),
        fp.project_failure_to_accounting(synthetic_record()),
    ),
)
def test_public_contracts_are_immutable_and_reject_extra_fields(
    instance: object,
) -> None:
    model_cls = type(instance)
    with pytest.raises(ValidationError):
        model_cls(**(instance.model_dump(mode="python") | {"unexpected": "field"}))
    with pytest.raises(ValidationError):
        instance.schema_version = 2


def test_bounded_identifiers_safe_repr_and_secret_retention_flags() -> None:
    signal = synthetic_signal(
        provider_error_code="token_expired",
        provider_message="synthetic raw provider text",
    )
    assert "synthetic raw provider text" not in repr(signal)
    assert "token_expired" not in repr(signal)

    record = fp.build_provider_failure_record(
        request_id="request.safe",
        runtime_id="runtime.safe",
        correlation_id="corr.safe",
        signal=signal,
        usage_record_id="usage.safe",
    )
    assert record.category is fp.ProviderFailureCategory.CREDENTIAL_EXPIRED
    assert record.provider_error_code_present is True
    assert record.provider_error_code_retained is False
    assert record.provider_message_present is True
    assert record.provider_message_retained is False
    assert record.provider_response_id_present is True
    assert record.provider_response_id_retained is False
    assert record.raw_exception_retained is False
    assert record.raw_provider_response_retained is False
    assert record.provider_headers_retained is False
    assert record.request_content_retained is False
    assert record.response_content_retained is False
    assert record.reasoning_trace_retained is False
    assert record.credential_metadata_retained is False
    assert "synthetic raw provider text" not in record.safe_summary

    with pytest.raises(ValidationError):
        synthetic_signal(provider_message="line\nbreak")
    with pytest.raises(ValidationError):
        synthetic_signal(HTTP_status=99)
    with pytest.raises(AttributeError):
        fp.build_provider_failure_record_id  # type: ignore[attr-defined]


def test_deterministic_failure_record_id_uses_only_stable_identity() -> None:
    first = fp.build_failure_record_id(
        runtime_id="runtime.identity",
        correlation_id="corr.identity",
        request_id="request.identity",
        category=fp.ProviderFailureCategory.RATE_LIMIT,
    )
    second = fp.build_failure_record_id(
        runtime_id="runtime.identity",
        correlation_id="corr.identity",
        request_id="request.identity",
        category=fp.ProviderFailureCategory.RATE_LIMIT,
    )
    different = fp.build_failure_record_id(
        runtime_id="runtime.identity",
        correlation_id="corr.identity",
        request_id="request.identity",
        category=fp.ProviderFailureCategory.QUOTA,
    )

    assert first == second
    assert first != different
    assert first.startswith("failure-")
    assert len(first.removeprefix("failure-")) == 24
    assert first.removeprefix("failure-").islower()


def test_failure_record_dispatch_and_accounting_invariants() -> None:
    with pytest.raises(ValidationError):
        fp.ProviderFailureRecord(
            failure_record_id="failure.invalid",
            request_id="request.invalid",
            runtime_id="runtime.invalid",
            correlation_id="corr.invalid",
            category=fp.ProviderFailureCategory.AUTHENTICATION,
            stage=fp.ProviderFailureStage.DISPATCH,
            origin=fp.ProviderFailureOrigin.HTTP_RESPONSE,
            provider_dispatch_occurred=False,
            provider_dispatch_count=1,
            accounting_outcome=ProviderAccountingOutcome.FAILED,
            safe_summary="Provider authentication failed.",
        )
    with pytest.raises(ValidationError):
        fp.ProviderFailureRecord(
            failure_record_id="failure.invalid2",
            request_id="request.invalid2",
            runtime_id="runtime.invalid2",
            correlation_id="corr.invalid2",
            category=fp.ProviderFailureCategory.AUTHENTICATION,
            stage=fp.ProviderFailureStage.DISPATCH,
            origin=fp.ProviderFailureOrigin.HTTP_RESPONSE,
            provider_dispatch_occurred=True,
            provider_dispatch_count=1,
            accounting_outcome=ProviderAccountingOutcome.FAILED,
            safe_summary="Provider authentication failed.",
        )
    with pytest.raises(ValidationError):
        fp.ProviderFailureRecord(
            failure_record_id="failure.invalid3",
            request_id="request.invalid3",
            runtime_id="runtime.invalid3",
            correlation_id="corr.invalid3",
            category=fp.ProviderFailureCategory.CONNECTION_TIMEOUT,
            stage=fp.ProviderFailureStage.CONNECTION,
            origin=fp.ProviderFailureOrigin.SDK_EXCEPTION,
            provider_dispatch_occurred=True,
            provider_dispatch_count=1,
            accounting_outcome=ProviderAccountingOutcome.COMPLETED,
            accounting_timeout_stage=ProviderTimeoutStage.CONNECTION,
            usage_record_id="usage.invalid3",
            safe_summary="The provider connection timed out.",
        )


def test_failure_policy_source_has_no_operational_authority() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in sorted(SOURCE_ROOT.glob("*.py"))
    )
    for forbidden in (
        "subprocess",
        "socket",
        "import requests",
        "from requests",
        "requests.",
        "httpx",
        "urllib.request",
        "import openai",
        "from openai",
        "responses.create",
        "chat.completions",
        "models.list",
        "auth.json",
        "os.environ",
        "os.getenv",
        "path.home",
        "expanduser",
        "sqlite",
        "session_db",
        "write_text",
        "write_bytes",
        "open(",
        "asyncio.sleep",
        "time.sleep",
        "shell=true",
        "os.system",
        "os.popen",
    ):
        assert forbidden not in source
