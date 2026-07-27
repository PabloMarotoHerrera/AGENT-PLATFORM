"""Immutable contracts for governed provider failure and retry policy."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.provider_accounting.contracts import (
    OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID,
    OPENAI_CODEX_PROVIDER_MODEL_ID,
    OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
    OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
)
from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingOutcome,
    ProviderTimeoutStage,
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


PROVIDER_FAILURE_POLICY_SCHEMA_VERSION = 1
PROVIDER_FAILURE_POLICY_ID = (
    "failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
PROVIDER_FAILURE_PROVIDER = "openai-codex"
PROVIDER_FAILURE_AUTHENTICATION = "chatgpt_oauth"
PROVIDER_FAILURE_ENDPOINT = "https://chatgpt.com/backend-api/codex"
PROVIDER_FAILURE_TRANSPORT = "codex_responses"
MAXIMUM_RETRY_AFTER_MS = 86_400_000

BoundedFailureIdentifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
BoundedFailureText = Annotated[str, StringConstraints(min_length=1, max_length=512)]
BoundedProviderSignalText = Annotated[
    str,
    StringConstraints(min_length=1, max_length=256),
]


class _ProviderFailureModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
        protected_namespaces=(),
    )

    @staticmethod
    def _reject_control_text(value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("text fields must not contain control characters")
        return value


class ProviderFailurePolicy(_ProviderFailureModel):
    """Fixed failure and retry posture for the governed route."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    policy_id: Literal[
        "failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = PROVIDER_FAILURE_POLICY_ID
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    worker_profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    accounting_policy_id: Literal[
        "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID
    provider: Literal["openai-codex"] = PROVIDER_FAILURE_PROVIDER
    authentication: Literal["chatgpt_oauth"] = PROVIDER_FAILURE_AUTHENTICATION
    endpoint: Literal["https://chatgpt.com/backend-api/codex"] = (
        PROVIDER_FAILURE_ENDPOINT
    )
    model: Literal["gpt-5.5"] = OPENAI_CODEX_PROVIDER_MODEL_ID
    transport: Literal["codex_responses"] = PROVIDER_FAILURE_TRANSPORT
    automatic_retry_allowed: Literal[False] = False
    maximum_automatic_retries: Literal[0] = 0
    maximum_provider_dispatches_per_request: Literal[1] = 1
    same_worker_retry_allowed: Literal[False] = False
    same_request_retry_allowed: Literal[False] = False
    credential_rotation_allowed: Literal[False] = False
    automatic_fallback_allowed: Literal[False] = False
    model_fallback_allowed: Literal[False] = False
    endpoint_fallback_allowed: Literal[False] = False
    automatic_refresh_allowed: Literal[False] = False


class ProviderFailureSignal(_ProviderFailureModel):
    """Transient synthetic classifier input; not persisted or exported."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    origin: ProviderFailureOrigin
    stage: ProviderFailureStage
    HTTP_status: int | None = Field(default=None, ge=100, le=599)
    provider_error_code: BoundedProviderSignalText | None = Field(
        default=None,
        repr=False,
    )
    provider_message: BoundedProviderSignalText | None = Field(
        default=None,
        repr=False,
    )
    SDK_exception_kind: ProviderSDKExceptionKind = ProviderSDKExceptionKind.NONE
    terminal_status: Literal["incomplete", "failed"] | None = None
    timeout_stage: ProviderTimeoutStage | None = None
    provider_dispatch_occurred: bool
    provider_response_id_present: bool = False
    retry_after_ms: int | None = Field(default=None, ge=0, le=MAXIMUM_RETRY_AFTER_MS)
    retry_delay_source: ProviderRetryDelaySource = ProviderRetryDelaySource.NONE

    @field_validator("provider_error_code", "provider_message", mode="after")
    @classmethod
    def signal_text_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return cls._reject_control_text(value)

    @model_validator(mode="after")
    def retry_delay_source_must_match_delay(self) -> "ProviderFailureSignal":
        if self.retry_after_ms is None:
            if self.retry_delay_source is not ProviderRetryDelaySource.NONE:
                raise ValueError("retry delay source requires normalized delay")
            return self
        if self.retry_delay_source is ProviderRetryDelaySource.NONE:
            raise ValueError("normalized retry delay requires a non-none source")
        return self


class ProviderFailureClassification(_ProviderFailureModel):
    """Deterministic intermediate classification result."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    category: ProviderFailureCategory
    stage: ProviderFailureStage
    origin: ProviderFailureOrigin
    recovery_action: ProviderRecoveryAction
    retry_disposition: ProviderRetryDisposition
    accounting_outcome: ProviderAccountingOutcome
    accounting_timeout_stage: ProviderTimeoutStage | None = None
    provider_dispatch_occurred: bool
    provider_dispatch_count: Literal[0, 1]


class ProviderFailureRecord(_ProviderFailureModel):
    """Durable secret-free failure evidence for one governed request."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    failure_record_id: BoundedFailureIdentifier
    request_id: BoundedFailureIdentifier
    runtime_id: BoundedFailureIdentifier
    correlation_id: BoundedFailureIdentifier
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    worker_profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    accounting_policy_id: Literal[
        "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID
    failure_policy_id: Literal[
        "failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = PROVIDER_FAILURE_POLICY_ID
    provider: Literal["openai-codex"] = PROVIDER_FAILURE_PROVIDER
    authentication: Literal["chatgpt_oauth"] = PROVIDER_FAILURE_AUTHENTICATION
    endpoint: Literal["https://chatgpt.com/backend-api/codex"] = (
        PROVIDER_FAILURE_ENDPOINT
    )
    model: Literal["gpt-5.5"] = OPENAI_CODEX_PROVIDER_MODEL_ID
    transport: Literal["codex_responses"] = PROVIDER_FAILURE_TRANSPORT
    category: ProviderFailureCategory
    stage: ProviderFailureStage
    origin: ProviderFailureOrigin
    provider_dispatch_occurred: bool
    provider_dispatch_count: Literal[0, 1]
    accounting_outcome: ProviderAccountingOutcome
    accounting_timeout_stage: ProviderTimeoutStage | None = None
    usage_record_id: BoundedFailureIdentifier | None = None
    HTTP_status: int | None = Field(default=None, ge=100, le=599)
    provider_response_id_present: bool = False
    provider_response_id_retained: Literal[False] = False
    provider_error_code_present: bool = False
    provider_error_code_retained: Literal[False] = False
    provider_message_present: bool = False
    provider_message_retained: Literal[False] = False
    retry_after_ms: int | None = Field(default=None, ge=0, le=MAXIMUM_RETRY_AFTER_MS)
    retry_delay_source: ProviderRetryDelaySource = ProviderRetryDelaySource.NONE
    safe_summary: BoundedFailureText
    raw_exception_retained: Literal[False] = False
    raw_provider_response_retained: Literal[False] = False
    provider_headers_retained: Literal[False] = False
    request_content_retained: Literal[False] = False
    response_content_retained: Literal[False] = False
    reasoning_trace_retained: Literal[False] = False
    credential_metadata_retained: Literal[False] = False

    @field_validator("safe_summary", mode="after")
    @classmethod
    def safe_summary_must_be_safe(cls, value: str) -> str:
        return cls._reject_control_text(value)

    @model_validator(mode="after")
    def failure_record_invariants(self) -> "ProviderFailureRecord":
        if not self.provider_dispatch_occurred:
            if self.provider_dispatch_count != 0:
                raise ValueError("pre-dispatch failures must have dispatch count zero")
            if self.usage_record_id is not None:
                raise ValueError("pre-dispatch failures must not carry usage_record_id")
        else:
            if self.provider_dispatch_count != 1:
                raise ValueError("dispatched failures must have dispatch count one")
            if self.usage_record_id is None:
                raise ValueError("dispatched failures require usage_record_id")
        if self.accounting_outcome is ProviderAccountingOutcome.COMPLETED:
            raise ValueError("failure records cannot project completed accounting")
        if self.accounting_outcome is ProviderAccountingOutcome.TIMED_OUT:
            if self.accounting_timeout_stage is None:
                raise ValueError("timed-out failures require timeout stage")
        elif self.accounting_timeout_stage is not None:
            raise ValueError("non-timeout failures must not carry timeout stage")
        if self.retry_after_ms is None:
            if self.retry_delay_source is not ProviderRetryDelaySource.NONE:
                raise ValueError("retry delay source requires normalized delay")
        elif self.retry_delay_source is ProviderRetryDelaySource.NONE:
            raise ValueError("normalized retry delay requires a non-none source")
        return self


class ProviderRetryDecision(_ProviderFailureModel):
    """Secret-free retry and cleanup projection for a failure record."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    failure_record_id: BoundedFailureIdentifier
    category: ProviderFailureCategory
    disposition: ProviderRetryDisposition
    recovery_action: ProviderRecoveryAction
    automatic_retry_allowed: Literal[False] = False
    automatic_retry_attempts: Literal[0] = 0
    same_request_retry_allowed: Literal[False] = False
    same_worker_retry_allowed: Literal[False] = False
    same_request_id_reuse_allowed: Literal[False] = False
    same_usage_record_id_reuse_allowed: Literal[False] = False
    credential_rotation_allowed: Literal[False] = False
    automatic_refresh_allowed: Literal[False] = False
    model_fallback_allowed: Literal[False] = False
    endpoint_fallback_allowed: Literal[False] = False
    new_request_required: bool
    new_worker_lifecycle_required: bool
    new_usage_record_required: bool
    new_credential_lease_required: bool
    human_authorization_required: bool
    retry_after_ms: int | None = Field(default=None, ge=0, le=MAXIMUM_RETRY_AFTER_MS)
    delay_is_advisory_only: Literal[True] = True
    release_temporary_credential_lease: bool
    close_provider_stream: bool
    stop_owned_worker: Literal[True] = True
    remove_temporary_projected_hermes_home: bool
    preserve_durable_credential: Literal[True] = True
    preserve_secret_free_accounting: Literal[True] = True
    preserve_secret_free_failure_record: Literal[True] = True
    preserve_partial_output: Literal[False] = False
    preserve_raw_provider_response: Literal[False] = False
    preserve_headers: Literal[False] = False

    @model_validator(mode="after")
    def retry_decision_must_preserve_boundaries(self) -> "ProviderRetryDecision":
        if self.disposition is ProviderRetryDisposition.NEVER:
            return self
        for field_name in (
            "new_request_required",
            "new_worker_lifecycle_required",
            "new_usage_record_required",
            "new_credential_lease_required",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be true for later resubmission")
        return self


class ProviderFailureAccountingProjection(_ProviderFailureModel):
    """Safe projection metadata for later P15.5 accounting integration."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    failure_record_id: BoundedFailureIdentifier
    category: ProviderFailureCategory
    accounting_outcome: ProviderAccountingOutcome
    accounting_timeout_stage: ProviderTimeoutStage | None = None
    provider_dispatch_count: Literal[0, 1]
    usage_record_id: BoundedFailureIdentifier | None = None


class ProviderFailureAccountingLink(_ProviderFailureModel):
    """Failure-to-accounting link validation result."""

    schema_version: Literal[1] = PROVIDER_FAILURE_POLICY_SCHEMA_VERSION
    failure_record_id: BoundedFailureIdentifier
    link_state: ProviderFailureAccountingLinkState
    usage_record_id_matched: bool
    request_id_matched: bool
    runtime_id_matched: bool
    correlation_id_matched: bool
    accounting_outcome_matched: bool
    timeout_stage_matched: bool
    provider_dispatch_count_matched: bool
    mismatch_reason: BoundedFailureText | None = None


__all__ = [
    "PROVIDER_FAILURE_POLICY_SCHEMA_VERSION",
    "PROVIDER_FAILURE_POLICY_ID",
    "PROVIDER_FAILURE_PROVIDER",
    "PROVIDER_FAILURE_AUTHENTICATION",
    "PROVIDER_FAILURE_ENDPOINT",
    "PROVIDER_FAILURE_TRANSPORT",
    "MAXIMUM_RETRY_AFTER_MS",
    "ProviderFailureAccountingLink",
    "ProviderFailureAccountingProjection",
    "ProviderFailureClassification",
    "ProviderFailurePolicy",
    "ProviderFailureRecord",
    "ProviderFailureSignal",
    "ProviderRetryDecision",
]
