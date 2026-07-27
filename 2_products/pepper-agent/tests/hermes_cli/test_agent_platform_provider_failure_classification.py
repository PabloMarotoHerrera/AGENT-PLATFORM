from __future__ import annotations

import pytest

from hermes_cli.agent_platform import provider_failure_policy as fp
from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingOutcome,
    ProviderTimeoutStage,
)


def signal(**overrides: object) -> fp.ProviderFailureSignal:
    values = {
        "origin": fp.ProviderFailureOrigin.HTTP_RESPONSE,
        "stage": fp.ProviderFailureStage.DISPATCH,
        "provider_dispatch_occurred": True,
        "provider_response_id_present": True,
    }
    values.update(overrides)
    return fp.ProviderFailureSignal(**values)


def classify(**overrides: object) -> fp.ProviderFailureRecord:
    synthetic_signal = signal(**overrides)
    return fp.build_provider_failure_record(
        request_id="request.classification",
        runtime_id="runtime.classification",
        correlation_id="corr.classification",
        signal=synthetic_signal,
        usage_record_id="usage.classification"
        if synthetic_signal.provider_dispatch_occurred
        else None,
    )


@pytest.mark.parametrize(
    (
        "name",
        "overrides",
        "category",
        "stage",
        "recovery",
        "disposition",
        "outcome",
        "timeout_stage",
    ),
    [
        (
            "401 authentication",
            {"HTTP_status": 401, "provider_message": "invalid authentication"},
            fp.ProviderFailureCategory.AUTHENTICATION,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REAUTHENTICATE,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "401 credential expired",
            {"HTTP_status": 401, "provider_error_code": "token_expired"},
            fp.ProviderFailureCategory.CREDENTIAL_EXPIRED,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REAUTHENTICATE,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "403 authorization",
            {"HTTP_status": 403, "provider_message": "access denied"},
            fp.ProviderFailureCategory.AUTHORIZATION,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REVIEW_AUTHORIZATION,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "403 entitlement",
            {"HTTP_status": 403, "provider_message": "model not included in plan"},
            fp.ProviderFailureCategory.ENTITLEMENT,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REVIEW_ENTITLEMENT,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "402 quota",
            {"HTTP_status": 402, "provider_error_code": "insufficient_quota"},
            fp.ProviderFailureCategory.QUOTA,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "429 quota-specific",
            {"HTTP_status": 429, "provider_error_code": "insufficient_quota"},
            fp.ProviderFailureCategory.QUOTA,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "429 rate limit",
            {"HTTP_status": 429, "provider_message": "too many requests retry after"},
            fp.ProviderFailureCategory.RATE_LIMIT,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "503 overload",
            {"HTTP_status": 503, "provider_message": "temporarily overloaded"},
            fp.ProviderFailureCategory.PROVIDER_OVERLOADED,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "529 overload",
            {"HTTP_status": 529, "provider_message": "at capacity"},
            fp.ProviderFailureCategory.PROVIDER_OVERLOADED,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "500 server error",
            {"HTTP_status": 500},
            fp.ProviderFailureCategory.PROVIDER_SERVER_ERROR,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "502 server error",
            {"HTTP_status": 502},
            fp.ProviderFailureCategory.PROVIDER_SERVER_ERROR,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "connect error",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.CONNECTION,
                "SDK_exception_kind": fp.ProviderSDKExceptionKind.CONNECT_ERROR,
            },
            fp.ProviderFailureCategory.CONNECTION_FAILURE,
            fp.ProviderFailureStage.CONNECTION,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "connection timeout",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.CONNECTION,
                "timeout_stage": ProviderTimeoutStage.CONNECTION,
            },
            fp.ProviderFailureCategory.CONNECTION_TIMEOUT,
            fp.ProviderFailureStage.CONNECTION,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.TIMED_OUT,
            ProviderTimeoutStage.CONNECTION,
        ),
        (
            "response-header timeout",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.RESPONSE_HEADER,
                "timeout_stage": ProviderTimeoutStage.RESPONSE_HEADER,
            },
            fp.ProviderFailureCategory.RESPONSE_HEADER_TIMEOUT,
            fp.ProviderFailureStage.RESPONSE_HEADER,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.TIMED_OUT,
            ProviderTimeoutStage.RESPONSE_HEADER,
        ),
        (
            "complete-inference timeout",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.STREAM,
                "timeout_stage": ProviderTimeoutStage.COMPLETE_INFERENCE,
            },
            fp.ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT,
            fp.ProviderFailureStage.STREAM,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.TIMED_OUT,
            ProviderTimeoutStage.COMPLETE_INFERENCE,
        ),
        (
            "cancellation timeout",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.CANCELLATION,
                "timeout_stage": ProviderTimeoutStage.CANCELLATION,
            },
            fp.ProviderFailureCategory.CANCELLATION_TIMEOUT,
            fp.ProviderFailureStage.CANCELLATION,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.TIMED_OUT,
            ProviderTimeoutStage.CANCELLATION,
        ),
        (
            "shutdown timeout",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.SHUTDOWN,
                "timeout_stage": ProviderTimeoutStage.WORKER_SHUTDOWN,
            },
            fp.ProviderFailureCategory.WORKER_SHUTDOWN_TIMEOUT,
            fp.ProviderFailureStage.SHUTDOWN,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.TIMED_OUT,
            ProviderTimeoutStage.WORKER_SHUTDOWN,
        ),
        (
            "TLS verification",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.CONNECTION,
                "SDK_exception_kind": fp.ProviderSDKExceptionKind.SSL_VERIFICATION_ERROR,
            },
            fp.ProviderFailureCategory.TLS_VERIFICATION,
            fp.ProviderFailureStage.CONNECTION,
            fp.ProviderRecoveryAction.CORRECT_CONFIGURATION,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "HTTP 400 stream protocol failure",
            {"HTTP_status": 400, "provider_message": "Stream must be set to true"},
            fp.ProviderFailureCategory.TRANSPORT_PROTOCOL,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.CORRECT_TRANSPORT,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "HTTP 400 invalid request",
            {"HTTP_status": 400, "provider_message": "invalid request"},
            fp.ProviderFailureCategory.REQUEST_INVALID,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.CORRECT_CONFIGURATION,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "HTTP 413 request too large",
            {"HTTP_status": 413},
            fp.ProviderFailureCategory.REQUEST_TOO_LARGE,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REDUCE_REQUEST,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "context overflow",
            {"HTTP_status": 400, "provider_message": "maximum context window"},
            fp.ProviderFailureCategory.CONTEXT_OVERFLOW,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REDUCE_REQUEST,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "HTTP 404 model unavailable",
            {"HTTP_status": 404, "provider_message": "unknown model"},
            fp.ProviderFailureCategory.MODEL_UNAVAILABLE,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.REVIEW_ENTITLEMENT,
            fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "content policy block",
            {"HTTP_status": 400, "provider_message": "request blocked by policy"},
            fp.ProviderFailureCategory.CONTENT_POLICY,
            fp.ProviderFailureStage.DISPATCH,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.NEVER,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "response.incomplete",
            {
                "origin": fp.ProviderFailureOrigin.TERMINAL_EVENT,
                "stage": fp.ProviderFailureStage.TERMINAL,
                "terminal_status": "incomplete",
            },
            fp.ProviderFailureCategory.PROVIDER_INCOMPLETE,
            fp.ProviderFailureStage.TERMINAL,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "response.failed",
            {
                "origin": fp.ProviderFailureOrigin.TERMINAL_EVENT,
                "stage": fp.ProviderFailureStage.TERMINAL,
                "terminal_status": "failed",
            },
            fp.ProviderFailureCategory.PROVIDER_FAILED,
            fp.ProviderFailureStage.TERMINAL,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "stream truncation",
            {
                "origin": fp.ProviderFailureOrigin.SSE_ERROR,
                "stage": fp.ProviderFailureStage.STREAM,
                "provider_message": "stream ended without terminal event",
            },
            fp.ProviderFailureCategory.STREAM_TRUNCATED,
            fp.ProviderFailureStage.STREAM,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "owner cancellation",
            {
                "origin": fp.ProviderFailureOrigin.OWNER_CANCELLATION,
                "stage": fp.ProviderFailureStage.CANCELLATION,
            },
            fp.ProviderFailureCategory.CANCELLED_BY_OWNER,
            fp.ProviderFailureStage.CANCELLATION,
            fp.ProviderRecoveryAction.CANCEL_AND_CLEANUP,
            fp.ProviderRetryDisposition.NEVER,
            ProviderAccountingOutcome.CANCELLED,
            None,
        ),
        (
            "accounting mismatch",
            {
                "origin": fp.ProviderFailureOrigin.ACCOUNTING_VALIDATION,
                "stage": fp.ProviderFailureStage.ACCOUNTING,
                "provider_message": "mismatched request identity",
            },
            fp.ProviderFailureCategory.ACCOUNTING_INVALID,
            fp.ProviderFailureStage.ACCOUNTING,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.NEVER,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
        (
            "unknown failure",
            {
                "origin": fp.ProviderFailureOrigin.SDK_EXCEPTION,
                "stage": fp.ProviderFailureStage.STREAM,
                "SDK_exception_kind": fp.ProviderSDKExceptionKind.GENERIC,
            },
            fp.ProviderFailureCategory.UNKNOWN,
            fp.ProviderFailureStage.STREAM,
            fp.ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
            fp.ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
            ProviderAccountingOutcome.FAILED,
            None,
        ),
    ],
)
def test_required_failure_classification_matrix(
    name: str,
    overrides: dict[str, object],
    category: fp.ProviderFailureCategory,
    stage: fp.ProviderFailureStage,
    recovery: fp.ProviderRecoveryAction,
    disposition: fp.ProviderRetryDisposition,
    outcome: ProviderAccountingOutcome,
    timeout_stage: ProviderTimeoutStage | None,
) -> None:
    record = classify(**overrides)
    decision = fp.build_provider_retry_decision(record)

    assert name
    assert record.category is category
    assert record.stage is stage
    assert record.accounting_outcome is outcome
    assert record.accounting_timeout_stage is timeout_stage
    assert record.provider_dispatch_count == 1
    assert decision.recovery_action is recovery
    assert decision.disposition is disposition
    assert decision.automatic_retry_allowed is False
    assert decision.automatic_retry_attempts == 0
    assert record.provider_error_code_retained is False
    assert record.provider_message_retained is False
    assert record.raw_provider_response_retained is False
    assert record.provider_headers_retained is False


def test_classification_precedence_keeps_specific_structured_failures() -> None:
    expired = classify(
        HTTP_status=401,
        provider_error_code="token_expired",
        provider_message="invalid authentication",
    )
    owner_cancelled = classify(
        origin=fp.ProviderFailureOrigin.OWNER_CANCELLATION,
        stage=fp.ProviderFailureStage.CANCELLATION,
        HTTP_status=500,
    )
    timeout = classify(
        HTTP_status=500,
        timeout_stage=ProviderTimeoutStage.COMPLETE_INFERENCE,
    )
    quota = classify(
        HTTP_status=429,
        provider_error_code="insufficient_quota",
        provider_message="rate_limit",
    )

    assert expired.category is fp.ProviderFailureCategory.CREDENTIAL_EXPIRED
    assert owner_cancelled.category is fp.ProviderFailureCategory.CANCELLED_BY_OWNER
    assert timeout.category is fp.ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT
    assert quota.category is fp.ProviderFailureCategory.QUOTA


def test_safe_summaries_never_include_raw_provider_text() -> None:
    raw_message = "synthetic account detail and rejected prompt excerpt"
    record = classify(HTTP_status=429, provider_message=raw_message)

    assert record.safe_summary == "The provider rate limit was reached."
    assert raw_message not in record.safe_summary
    assert record.provider_message_present is True
    assert record.provider_message_retained is False
