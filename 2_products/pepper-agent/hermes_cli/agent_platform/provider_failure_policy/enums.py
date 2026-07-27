"""Enumerations for governed provider failure and retry policy metadata."""

from __future__ import annotations

from enum import StrEnum


class ProviderFailureCategory(StrEnum):
    """Failure taxonomy for the governed OpenAI Codex route."""

    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    CREDENTIAL_EXPIRED = "credential_expired"
    ENTITLEMENT = "entitlement"
    QUOTA = "quota"
    RATE_LIMIT = "rate_limit"
    PROVIDER_OVERLOADED = "provider_overloaded"
    PROVIDER_SERVER_ERROR = "provider_server_error"
    CONNECTION_FAILURE = "connection_failure"
    CONNECTION_TIMEOUT = "connection_timeout"
    RESPONSE_HEADER_TIMEOUT = "response_header_timeout"
    COMPLETE_INFERENCE_TIMEOUT = "complete_inference_timeout"
    CANCELLATION_TIMEOUT = "cancellation_timeout"
    WORKER_SHUTDOWN_TIMEOUT = "worker_shutdown_timeout"
    TLS_VERIFICATION = "tls_verification"
    TRANSPORT_PROTOCOL = "transport_protocol"
    REQUEST_INVALID = "request_invalid"
    REQUEST_TOO_LARGE = "request_too_large"
    CONTEXT_OVERFLOW = "context_overflow"
    MODEL_UNAVAILABLE = "model_unavailable"
    CONTENT_POLICY = "content_policy"
    PROVIDER_INCOMPLETE = "provider_incomplete"
    PROVIDER_FAILED = "provider_failed"
    STREAM_TRUNCATED = "stream_truncated"
    CANCELLED_BY_OWNER = "cancelled_by_owner"
    ACCOUNTING_INVALID = "accounting_invalid"
    UNKNOWN = "unknown"


class ProviderFailureStage(StrEnum):
    """Lifecycle stage at which the failure was observed."""

    PREFLIGHT = "preflight"
    CREDENTIAL = "credential"
    DISPATCH = "dispatch"
    CONNECTION = "connection"
    RESPONSE_HEADER = "response_header"
    STREAM = "stream"
    TERMINAL = "terminal"
    CANCELLATION = "cancellation"
    SHUTDOWN = "shutdown"
    ACCOUNTING = "accounting"


class ProviderFailureOrigin(StrEnum):
    """Where synthetic failure evidence arrived from."""

    LOCAL_VALIDATION = "local_validation"
    SDK_EXCEPTION = "SDK_exception"
    HTTP_RESPONSE = "HTTP_response"
    SSE_ERROR = "SSE_error"
    TERMINAL_EVENT = "terminal_event"
    OWNER_CANCELLATION = "owner_cancellation"
    ACCOUNTING_VALIDATION = "accounting_validation"


class ProviderRetryDisposition(StrEnum):
    """Retry disposition kept separate from failure category."""

    NEVER = "never"
    NEW_REQUEST_AFTER_HUMAN_ACTION = "new_request_after_human_action"
    NEW_REQUEST_AFTER_EXTERNAL_CONDITION = "new_request_after_external_condition"
    NEW_REQUEST_AFTER_REQUEST_CHANGE = "new_request_after_request_change"
    NEW_REQUEST_AFTER_CONFIGURATION_CHANGE = "new_request_after_configuration_change"
    OPERATOR_REVIEW_REQUIRED = "operator_review_required"


class ProviderRecoveryAction(StrEnum):
    """Advisory recovery metadata; no action is executed by P15.6."""

    ABORT = "abort"
    REAUTHENTICATE = "reauthenticate"
    REVIEW_AUTHORIZATION = "review_authorization"
    REVIEW_ENTITLEMENT = "review_entitlement"
    WAIT_FOR_EXTERNAL_RESET = "wait_for_external_reset"
    REDUCE_REQUEST = "reduce_request"
    CORRECT_TRANSPORT = "correct_transport"
    CORRECT_CONFIGURATION = "correct_configuration"
    PRESERVE_EVIDENCE_AND_ESCALATE = "preserve_evidence_and_escalate"
    CANCEL_AND_CLEANUP = "cancel_and_cleanup"


class ProviderRetryDelaySource(StrEnum):
    """Source of caller-normalized advisory retry-delay metadata."""

    NONE = "none"
    PROVIDER_RETRY_AFTER = "provider_retry_after"
    POLICY_ADVISORY = "policy_advisory"


class ProviderSDKExceptionKind(StrEnum):
    """Bounded SDK exception vocabulary supplied by a future adapter."""

    NONE = "none"
    CONNECT_ERROR = "connect_error"
    READ_TIMEOUT = "read_timeout"
    REMOTE_PROTOCOL_ERROR = "remote_protocol_error"
    SSL_VERIFICATION_ERROR = "SSL_verification_error"
    CANCELLED = "cancelled"
    GENERIC = "generic"


class ProviderFailureAccountingLinkState(StrEnum):
    """Failure-policy-local accounting link validation states."""

    MATCHED = "matched"
    MATCHED_WITHOUT_ACCOUNTING = "matched_without_accounting"
    MISSING = "missing"
    MISMATCHED = "mismatched"


__all__ = [
    "ProviderFailureAccountingLinkState",
    "ProviderFailureCategory",
    "ProviderFailureOrigin",
    "ProviderFailureStage",
    "ProviderRecoveryAction",
    "ProviderRetryDelaySource",
    "ProviderRetryDisposition",
    "ProviderSDKExceptionKind",
]
