"""Pure provider failure classification and retry-policy helpers."""

from __future__ import annotations

import hashlib

from hermes_cli.agent_platform.provider_accounting.contracts import (
    ProviderAccountingRecord,
)
from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingOutcome,
    ProviderTimeoutStage,
)
from hermes_cli.agent_platform.provider_failure_policy.contracts import (
    ProviderFailureAccountingLink,
    ProviderFailureAccountingProjection,
    ProviderFailureClassification,
    ProviderFailureRecord,
    ProviderFailureSignal,
    ProviderRetryDecision,
)
from hermes_cli.agent_platform.provider_failure_policy.enums import (
    ProviderFailureAccountingLinkState,
    ProviderFailureCategory,
    ProviderFailureOrigin,
    ProviderFailureStage,
    ProviderRecoveryAction,
    ProviderRetryDelaySource,
    ProviderRetryDisposition,
    ProviderSDKExceptionKind,
)


_CREDENTIAL_EXPIRED_PATTERNS = (
    "token_expired",
    "access_token_expired",
    "expired credential",
    "credential expired",
    "access token expired",
)
_AUTHENTICATION_PATTERNS = (
    "invalid authentication",
    "invalid access token",
    "missing bearer credential",
)
_AUTHORIZATION_PATTERNS = ("forbidden", "access denied")
_ENTITLEMENT_PATTERNS = (
    "model not included in plan",
    "model not available for account",
    "plan does not include model",
    "account not entitled",
    "subscription does not permit model",
)
_QUOTA_PATTERNS = (
    "insufficient_quota",
    "usage allocation exhausted",
    "account quota exhausted",
    "credit or subscription capacity exhausted",
)
_RATE_LIMIT_PATTERNS = (
    "rate_limit",
    "rate limit",
    "too many requests",
    "retry after",
    "throttled",
)
_OVERLOAD_PATTERNS = ("overloaded", "at capacity", "temporarily overloaded")
_CONTEXT_PATTERNS = (
    "context length",
    "context window",
    "too many tokens",
    "prompt too long",
    "maximum context",
)
_MODEL_PATTERNS = ("model_not_found", "unknown model", "unsupported model")
_CONTENT_POLICY_PATTERNS = (
    "content policy",
    "safety policy",
    "request blocked by policy",
)


_TIMEOUT_CATEGORY_BY_STAGE = {
    ProviderTimeoutStage.CONNECTION: ProviderFailureCategory.CONNECTION_TIMEOUT,
    ProviderTimeoutStage.RESPONSE_HEADER: (
        ProviderFailureCategory.RESPONSE_HEADER_TIMEOUT
    ),
    ProviderTimeoutStage.COMPLETE_INFERENCE: (
        ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT
    ),
    ProviderTimeoutStage.CANCELLATION: ProviderFailureCategory.CANCELLATION_TIMEOUT,
    ProviderTimeoutStage.WORKER_SHUTDOWN: (
        ProviderFailureCategory.WORKER_SHUTDOWN_TIMEOUT
    ),
}
_FAILURE_STAGE_BY_TIMEOUT_STAGE = {
    ProviderTimeoutStage.CONNECTION: ProviderFailureStage.CONNECTION,
    ProviderTimeoutStage.RESPONSE_HEADER: ProviderFailureStage.RESPONSE_HEADER,
    ProviderTimeoutStage.COMPLETE_INFERENCE: ProviderFailureStage.STREAM,
    ProviderTimeoutStage.CANCELLATION: ProviderFailureStage.CANCELLATION,
    ProviderTimeoutStage.WORKER_SHUTDOWN: ProviderFailureStage.SHUTDOWN,
}
_TIMEOUT_STAGE_BY_CATEGORY = {
    category: stage for stage, category in _TIMEOUT_CATEGORY_BY_STAGE.items()
}


_OUTCOME_BY_CATEGORY = {
    ProviderFailureCategory.CANCELLED_BY_OWNER: ProviderAccountingOutcome.CANCELLED,
    ProviderFailureCategory.CONNECTION_TIMEOUT: ProviderAccountingOutcome.TIMED_OUT,
    ProviderFailureCategory.RESPONSE_HEADER_TIMEOUT: ProviderAccountingOutcome.TIMED_OUT,
    ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT: (
        ProviderAccountingOutcome.TIMED_OUT
    ),
    ProviderFailureCategory.CANCELLATION_TIMEOUT: ProviderAccountingOutcome.TIMED_OUT,
    ProviderFailureCategory.WORKER_SHUTDOWN_TIMEOUT: ProviderAccountingOutcome.TIMED_OUT,
}


_RECOVERY_BY_CATEGORY = {
    ProviderFailureCategory.AUTHENTICATION: ProviderRecoveryAction.REAUTHENTICATE,
    ProviderFailureCategory.CREDENTIAL_EXPIRED: ProviderRecoveryAction.REAUTHENTICATE,
    ProviderFailureCategory.AUTHORIZATION: ProviderRecoveryAction.REVIEW_AUTHORIZATION,
    ProviderFailureCategory.ENTITLEMENT: ProviderRecoveryAction.REVIEW_ENTITLEMENT,
    ProviderFailureCategory.QUOTA: ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
    ProviderFailureCategory.RATE_LIMIT: ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET,
    ProviderFailureCategory.PROVIDER_OVERLOADED: (
        ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET
    ),
    ProviderFailureCategory.PROVIDER_SERVER_ERROR: (
        ProviderRecoveryAction.WAIT_FOR_EXTERNAL_RESET
    ),
    ProviderFailureCategory.TLS_VERIFICATION: ProviderRecoveryAction.CORRECT_CONFIGURATION,
    ProviderFailureCategory.TRANSPORT_PROTOCOL: ProviderRecoveryAction.CORRECT_TRANSPORT,
    ProviderFailureCategory.REQUEST_INVALID: ProviderRecoveryAction.CORRECT_CONFIGURATION,
    ProviderFailureCategory.REQUEST_TOO_LARGE: ProviderRecoveryAction.REDUCE_REQUEST,
    ProviderFailureCategory.CONTEXT_OVERFLOW: ProviderRecoveryAction.REDUCE_REQUEST,
    ProviderFailureCategory.MODEL_UNAVAILABLE: ProviderRecoveryAction.REVIEW_ENTITLEMENT,
    ProviderFailureCategory.CONTENT_POLICY: (
        ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE
    ),
    ProviderFailureCategory.CANCELLED_BY_OWNER: ProviderRecoveryAction.CANCEL_AND_CLEANUP,
    ProviderFailureCategory.ACCOUNTING_INVALID: (
        ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE
    ),
}


_DISPOSITION_BY_CATEGORY = {
    ProviderFailureCategory.AUTHENTICATION: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION
    ),
    ProviderFailureCategory.CREDENTIAL_EXPIRED: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION
    ),
    ProviderFailureCategory.AUTHORIZATION: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION
    ),
    ProviderFailureCategory.ENTITLEMENT: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION
    ),
    ProviderFailureCategory.QUOTA: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION
    ),
    ProviderFailureCategory.RATE_LIMIT: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION
    ),
    ProviderFailureCategory.PROVIDER_OVERLOADED: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION
    ),
    ProviderFailureCategory.PROVIDER_SERVER_ERROR: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION
    ),
    ProviderFailureCategory.TLS_VERIFICATION: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE
    ),
    ProviderFailureCategory.TRANSPORT_PROTOCOL: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE
    ),
    ProviderFailureCategory.REQUEST_INVALID: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE
    ),
    ProviderFailureCategory.REQUEST_TOO_LARGE: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE
    ),
    ProviderFailureCategory.CONTEXT_OVERFLOW: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE
    ),
    ProviderFailureCategory.MODEL_UNAVAILABLE: (
        ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE
    ),
    ProviderFailureCategory.CONTENT_POLICY: ProviderRetryDisposition.NEVER,
    ProviderFailureCategory.CANCELLED_BY_OWNER: ProviderRetryDisposition.NEVER,
    ProviderFailureCategory.ACCOUNTING_INVALID: ProviderRetryDisposition.NEVER,
}


_SAFE_SUMMARY_BY_CATEGORY = {
    ProviderFailureCategory.AUTHENTICATION: "Provider authentication failed.",
    ProviderFailureCategory.CREDENTIAL_EXPIRED: (
        "The governed provider credential is expired."
    ),
    ProviderFailureCategory.AUTHORIZATION: "Provider authorization failed.",
    ProviderFailureCategory.ENTITLEMENT: (
        "The configured model is not currently available to this account."
    ),
    ProviderFailureCategory.QUOTA: "Provider usage capacity is unavailable.",
    ProviderFailureCategory.RATE_LIMIT: "The provider rate limit was reached.",
    ProviderFailureCategory.PROVIDER_OVERLOADED: (
        "The provider is temporarily overloaded."
    ),
    ProviderFailureCategory.PROVIDER_SERVER_ERROR: "The provider returned a server error.",
    ProviderFailureCategory.CONNECTION_FAILURE: "The provider connection failed.",
    ProviderFailureCategory.CONNECTION_TIMEOUT: "The provider connection timed out.",
    ProviderFailureCategory.RESPONSE_HEADER_TIMEOUT: (
        "The provider response-header wait timed out."
    ),
    ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT: (
        "The governed provider inference timed out."
    ),
    ProviderFailureCategory.CANCELLATION_TIMEOUT: "Provider cancellation timed out.",
    ProviderFailureCategory.WORKER_SHUTDOWN_TIMEOUT: "Worker shutdown timed out.",
    ProviderFailureCategory.TLS_VERIFICATION: "Provider TLS verification failed.",
    ProviderFailureCategory.TRANSPORT_PROTOCOL: (
        "The provider request did not satisfy the required transport protocol."
    ),
    ProviderFailureCategory.REQUEST_INVALID: "The governed provider request is invalid.",
    ProviderFailureCategory.REQUEST_TOO_LARGE: "The governed request is too large.",
    ProviderFailureCategory.CONTEXT_OVERFLOW: (
        "The request exceeds the governed context boundary."
    ),
    ProviderFailureCategory.MODEL_UNAVAILABLE: "The configured model is unavailable.",
    ProviderFailureCategory.CONTENT_POLICY: (
        "The provider rejected the request under its content policy."
    ),
    ProviderFailureCategory.PROVIDER_INCOMPLETE: (
        "The provider returned an incomplete terminal state."
    ),
    ProviderFailureCategory.PROVIDER_FAILED: "The provider returned a failed terminal state.",
    ProviderFailureCategory.STREAM_TRUNCATED: "The provider stream ended early.",
    ProviderFailureCategory.CANCELLED_BY_OWNER: "The request was cancelled by its owner.",
    ProviderFailureCategory.ACCOUNTING_INVALID: "Failure/accounting linkage is invalid.",
    ProviderFailureCategory.UNKNOWN: (
        "The provider request failed for an unclassified reason."
    ),
}


def _text(signal: ProviderFailureSignal) -> str:
    return " ".join(
        value.lower()
        for value in (signal.provider_error_code, signal.provider_message)
        if value
    )


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def _category_from_read_timeout(
    stage: ProviderFailureStage,
) -> ProviderFailureCategory:
    if stage is ProviderFailureStage.CONNECTION:
        return ProviderFailureCategory.CONNECTION_TIMEOUT
    if stage is ProviderFailureStage.RESPONSE_HEADER:
        return ProviderFailureCategory.RESPONSE_HEADER_TIMEOUT
    if stage is ProviderFailureStage.CANCELLATION:
        return ProviderFailureCategory.CANCELLATION_TIMEOUT
    if stage is ProviderFailureStage.SHUTDOWN:
        return ProviderFailureCategory.WORKER_SHUTDOWN_TIMEOUT
    return ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT


def _category_from_status_and_text(
    signal: ProviderFailureSignal,
    text: str,
) -> ProviderFailureCategory | None:
    status = signal.HTTP_status
    if status == 402 or _contains_any(text, _QUOTA_PATTERNS):
        return ProviderFailureCategory.QUOTA
    if _contains_any(text, _ENTITLEMENT_PATTERNS):
        return ProviderFailureCategory.ENTITLEMENT
    if _contains_any(text, _CONTENT_POLICY_PATTERNS):
        return ProviderFailureCategory.CONTENT_POLICY
    if _contains_any(text, _CONTEXT_PATTERNS):
        return ProviderFailureCategory.CONTEXT_OVERFLOW
    if status == 413:
        return ProviderFailureCategory.REQUEST_TOO_LARGE
    if status == 404 or _contains_any(text, _MODEL_PATTERNS):
        return ProviderFailureCategory.MODEL_UNAVAILABLE
    if status == 400 and "stream must be set to true" in text:
        return ProviderFailureCategory.TRANSPORT_PROTOCOL
    if status == 401 or _contains_any(text, _AUTHENTICATION_PATTERNS):
        return ProviderFailureCategory.AUTHENTICATION
    if status == 403 or _contains_any(text, _AUTHORIZATION_PATTERNS):
        return ProviderFailureCategory.AUTHORIZATION
    if status == 429 or _contains_any(text, _RATE_LIMIT_PATTERNS):
        return ProviderFailureCategory.RATE_LIMIT
    if status in {503, 529} or _contains_any(text, _OVERLOAD_PATTERNS):
        return ProviderFailureCategory.PROVIDER_OVERLOADED
    if status in {500, 502, 504}:
        return ProviderFailureCategory.PROVIDER_SERVER_ERROR
    if status == 400:
        return ProviderFailureCategory.REQUEST_INVALID
    return None


def _stage_for_category(
    category: ProviderFailureCategory,
    signal_stage: ProviderFailureStage,
) -> ProviderFailureStage:
    if category in _TIMEOUT_STAGE_BY_CATEGORY:
        return _FAILURE_STAGE_BY_TIMEOUT_STAGE[_TIMEOUT_STAGE_BY_CATEGORY[category]]
    if category is ProviderFailureCategory.CONNECTION_FAILURE:
        return ProviderFailureStage.CONNECTION
    if category is ProviderFailureCategory.TLS_VERIFICATION:
        return ProviderFailureStage.CONNECTION
    if category is ProviderFailureCategory.TRANSPORT_PROTOCOL:
        return ProviderFailureStage.DISPATCH
    if category in {
        ProviderFailureCategory.PROVIDER_INCOMPLETE,
        ProviderFailureCategory.PROVIDER_FAILED,
    }:
        return ProviderFailureStage.TERMINAL
    if category is ProviderFailureCategory.STREAM_TRUNCATED:
        return ProviderFailureStage.STREAM
    if category is ProviderFailureCategory.CANCELLED_BY_OWNER:
        return ProviderFailureStage.CANCELLATION
    if category is ProviderFailureCategory.ACCOUNTING_INVALID:
        return ProviderFailureStage.ACCOUNTING
    return signal_stage


def _recovery_for_category(
    category: ProviderFailureCategory,
) -> ProviderRecoveryAction:
    return _RECOVERY_BY_CATEGORY.get(
        category,
        ProviderRecoveryAction.PRESERVE_EVIDENCE_AND_ESCALATE,
    )


def _disposition_for_category(
    category: ProviderFailureCategory,
) -> ProviderRetryDisposition:
    return _DISPOSITION_BY_CATEGORY.get(
        category,
        ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
    )


def _accounting_outcome_for_category(
    category: ProviderFailureCategory,
) -> ProviderAccountingOutcome:
    return _OUTCOME_BY_CATEGORY.get(category, ProviderAccountingOutcome.FAILED)


def build_failure_record_id(
    *,
    runtime_id: str,
    correlation_id: str,
    request_id: str,
    category: ProviderFailureCategory,
) -> str:
    """Build a deterministic bounded failure-record identifier."""

    payload = "\0".join((runtime_id, correlation_id, request_id, category.value))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"failure-{digest}"


def classify_openai_codex_failure(
    signal: ProviderFailureSignal,
) -> ProviderFailureClassification:
    """Classify one synthetic OpenAI Codex failure signal deterministically."""

    text = _text(signal)
    category = ProviderFailureCategory.UNKNOWN

    if (
        signal.origin is ProviderFailureOrigin.OWNER_CANCELLATION
        or signal.SDK_exception_kind is ProviderSDKExceptionKind.CANCELLED
    ):
        category = ProviderFailureCategory.CANCELLED_BY_OWNER
    elif (
        signal.origin is ProviderFailureOrigin.ACCOUNTING_VALIDATION
        or signal.stage is ProviderFailureStage.ACCOUNTING
    ):
        category = ProviderFailureCategory.ACCOUNTING_INVALID
    elif signal.timeout_stage is not None:
        category = _TIMEOUT_CATEGORY_BY_STAGE[signal.timeout_stage]
    elif signal.SDK_exception_kind is ProviderSDKExceptionKind.SSL_VERIFICATION_ERROR:
        category = ProviderFailureCategory.TLS_VERIFICATION
    elif _contains_any(text, _CREDENTIAL_EXPIRED_PATTERNS):
        category = ProviderFailureCategory.CREDENTIAL_EXPIRED
    else:
        category = _category_from_status_and_text(signal, text) or category
        if category is ProviderFailureCategory.UNKNOWN:
            if signal.SDK_exception_kind is ProviderSDKExceptionKind.CONNECT_ERROR:
                category = ProviderFailureCategory.CONNECTION_FAILURE
            elif signal.SDK_exception_kind is ProviderSDKExceptionKind.READ_TIMEOUT:
                category = _category_from_read_timeout(signal.stage)
            elif (
                signal.SDK_exception_kind
                is ProviderSDKExceptionKind.REMOTE_PROTOCOL_ERROR
            ):
                category = ProviderFailureCategory.TRANSPORT_PROTOCOL
            elif signal.terminal_status == "incomplete":
                category = ProviderFailureCategory.PROVIDER_INCOMPLETE
            elif signal.terminal_status == "failed":
                category = ProviderFailureCategory.PROVIDER_FAILED
            elif (
                signal.origin is ProviderFailureOrigin.SSE_ERROR
                and signal.stage is ProviderFailureStage.STREAM
                and "stream ended without terminal event" in text
            ):
                category = ProviderFailureCategory.STREAM_TRUNCATED

    stage = _stage_for_category(category, signal.stage)
    timeout_stage = _TIMEOUT_STAGE_BY_CATEGORY.get(category)
    outcome = _accounting_outcome_for_category(category)
    return ProviderFailureClassification(
        category=category,
        stage=stage,
        origin=signal.origin,
        recovery_action=_recovery_for_category(category),
        retry_disposition=_disposition_for_category(category),
        accounting_outcome=outcome,
        accounting_timeout_stage=timeout_stage,
        provider_dispatch_occurred=signal.provider_dispatch_occurred,
        provider_dispatch_count=1 if signal.provider_dispatch_occurred else 0,
    )


def resolve_safe_failure_summary(category: ProviderFailureCategory) -> str:
    """Return the catalogued safe summary for a failure category."""

    return _SAFE_SUMMARY_BY_CATEGORY[category]


def build_provider_failure_record(
    *,
    request_id: str,
    runtime_id: str,
    correlation_id: str,
    signal: ProviderFailureSignal,
    usage_record_id: str | None = None,
) -> ProviderFailureRecord:
    """Build one durable secret-free failure record from a synthetic signal."""

    classification = classify_openai_codex_failure(signal)
    failure_record_id = build_failure_record_id(
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        request_id=request_id,
        category=classification.category,
    )
    return ProviderFailureRecord(
        failure_record_id=failure_record_id,
        request_id=request_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        category=classification.category,
        stage=classification.stage,
        origin=classification.origin,
        provider_dispatch_occurred=classification.provider_dispatch_occurred,
        provider_dispatch_count=classification.provider_dispatch_count,
        accounting_outcome=classification.accounting_outcome,
        accounting_timeout_stage=classification.accounting_timeout_stage,
        usage_record_id=usage_record_id,
        HTTP_status=signal.HTTP_status,
        provider_response_id_present=signal.provider_response_id_present,
        provider_error_code_present=signal.provider_error_code is not None,
        provider_message_present=signal.provider_message is not None,
        retry_after_ms=signal.retry_after_ms,
        retry_delay_source=signal.retry_delay_source,
        safe_summary=resolve_safe_failure_summary(classification.category),
    )


def build_provider_retry_decision(
    failure_record: ProviderFailureRecord,
    *,
    temporary_credential_lease_exists: bool = True,
    provider_stream_exists: bool | None = None,
    temporary_projected_hermes_home_present: bool = True,
) -> ProviderRetryDecision:
    """Build a bounded advisory retry and cleanup decision."""

    disposition = _disposition_for_category(failure_record.category)
    recovery = _recovery_for_category(failure_record.category)
    new_request_required = disposition is not ProviderRetryDisposition.NEVER
    human_authorization_required = disposition in {
        ProviderRetryDisposition.NEW_REQUEST_AFTER_HUMAN_ACTION,
        ProviderRetryDisposition.NEW_REQUEST_AFTER_REQUEST_CHANGE,
        ProviderRetryDisposition.NEW_REQUEST_AFTER_CONFIGURATION_CHANGE,
        ProviderRetryDisposition.OPERATOR_REVIEW_REQUIRED,
    }
    return ProviderRetryDecision(
        failure_record_id=failure_record.failure_record_id,
        category=failure_record.category,
        disposition=disposition,
        recovery_action=recovery,
        new_request_required=new_request_required,
        new_worker_lifecycle_required=new_request_required,
        new_usage_record_required=new_request_required,
        new_credential_lease_required=new_request_required,
        human_authorization_required=human_authorization_required,
        retry_after_ms=failure_record.retry_after_ms,
        release_temporary_credential_lease=temporary_credential_lease_exists,
        close_provider_stream=provider_stream_exists
        if provider_stream_exists is not None
        else failure_record.provider_dispatch_occurred,
        remove_temporary_projected_hermes_home=(
            temporary_projected_hermes_home_present
        ),
    )


def project_failure_to_accounting(
    failure_record: ProviderFailureRecord,
) -> ProviderFailureAccountingProjection:
    """Project failure metadata to P15.5 accounting without mutation."""

    return ProviderFailureAccountingProjection(
        failure_record_id=failure_record.failure_record_id,
        category=failure_record.category,
        accounting_outcome=failure_record.accounting_outcome,
        accounting_timeout_stage=failure_record.accounting_timeout_stage,
        provider_dispatch_count=failure_record.provider_dispatch_count,
        usage_record_id=failure_record.usage_record_id,
    )


def validate_failure_accounting_link(
    *,
    failure_record: ProviderFailureRecord,
    accounting_record: ProviderAccountingRecord | None,
) -> ProviderFailureAccountingLink:
    """Validate failure/accounting identity, outcome and call-count linkage."""

    if accounting_record is None:
        if failure_record.provider_dispatch_occurred:
            return ProviderFailureAccountingLink(
                failure_record_id=failure_record.failure_record_id,
                link_state=ProviderFailureAccountingLinkState.MISSING,
                usage_record_id_matched=False,
                request_id_matched=False,
                runtime_id_matched=False,
                correlation_id_matched=False,
                accounting_outcome_matched=False,
                timeout_stage_matched=False,
                provider_dispatch_count_matched=False,
                mismatch_reason="accounting record missing after provider dispatch",
            )
        return ProviderFailureAccountingLink(
            failure_record_id=failure_record.failure_record_id,
            link_state=ProviderFailureAccountingLinkState.MATCHED_WITHOUT_ACCOUNTING,
            usage_record_id_matched=True,
            request_id_matched=True,
            runtime_id_matched=True,
            correlation_id_matched=True,
            accounting_outcome_matched=True,
            timeout_stage_matched=True,
            provider_dispatch_count_matched=True,
        )

    usage_record_id_matched = (
        failure_record.usage_record_id == accounting_record.usage_record_id
    )
    request_id_matched = failure_record.request_id == accounting_record.request_id
    runtime_id_matched = failure_record.runtime_id == accounting_record.runtime_id
    correlation_id_matched = (
        failure_record.correlation_id == accounting_record.correlation_id
    )
    accounting_outcome_matched = (
        failure_record.accounting_outcome == accounting_record.timeout.outcome
    )
    timeout_stage_matched = (
        failure_record.accounting_timeout_stage
        == accounting_record.timeout.timeout_stage
    )
    provider_dispatch_count_matched = (
        failure_record.provider_dispatch_count
        == accounting_record.usage.counters.request_count
    )
    matched = all((
        usage_record_id_matched,
        request_id_matched,
        runtime_id_matched,
        correlation_id_matched,
        accounting_outcome_matched,
        timeout_stage_matched,
        provider_dispatch_count_matched,
    ))
    return ProviderFailureAccountingLink(
        failure_record_id=failure_record.failure_record_id,
        link_state=ProviderFailureAccountingLinkState.MATCHED
        if matched
        else ProviderFailureAccountingLinkState.MISMATCHED,
        usage_record_id_matched=usage_record_id_matched,
        request_id_matched=request_id_matched,
        runtime_id_matched=runtime_id_matched,
        correlation_id_matched=correlation_id_matched,
        accounting_outcome_matched=accounting_outcome_matched,
        timeout_stage_matched=timeout_stage_matched,
        provider_dispatch_count_matched=provider_dispatch_count_matched,
        mismatch_reason=None if matched else "failure/accounting link mismatch",
    )


__all__ = [
    "build_failure_record_id",
    "build_provider_failure_record",
    "build_provider_retry_decision",
    "classify_openai_codex_failure",
    "project_failure_to_accounting",
    "resolve_safe_failure_summary",
    "validate_failure_accounting_link",
]
