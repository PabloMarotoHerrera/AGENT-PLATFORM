"""Immutable contracts for bounded provider-worker profile metadata."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
)
from hermes_cli.agent_platform.provider_runtime.contracts import (
    ProviderRuntimeResolutionRequest,
    ResolvedProviderRuntimeBinding,
)
from hermes_cli.agent_platform.provider_worker.enums import (
    ProviderWorkerFailureStage,
    ProviderWorkerFeaturePolicy,
    ProviderWorkerInputKind,
    ProviderWorkerOutputKind,
    ProviderWorkerOversizedRequestPolicy,
    ProviderWorkerProfileState,
    ProviderWorkerResultState,
)


PROVIDER_WORKER_PROFILE_SCHEMA_VERSION = 1

OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID = (
    "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID = (
    "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
)

_EXECUTION_POLICY_ID = "worker.execution.openai-codex.single-request.v1"
_REQUEST_POLICY_ID = "worker.request.openai-codex.pilot.v1"
_RESULT_POLICY_ID = "worker.result.openai-codex.single-text.v1"
_TIMEOUT_POLICY_ID = "worker.timeout.openai-codex.single-request.v1"
_SYSTEM_INSTRUCTION_POLICY_ID = "worker.system.openai-codex.p15-pilot.v1"
_SYSTEM_INSTRUCTION_SOURCE = "tracked_internal_template"

MAXIMUM_PROMPT_TOKENS = 32_768
RESERVED_SYSTEM_INSTRUCTION_TOKENS = 8_192
MAXIMUM_USER_CONTENT_TOKENS = 24_576
MAXIMUM_OUTPUT_TOKENS = 4_096
MAXIMUM_REQUEST_UTF8_BYTES = 131_072
MAXIMUM_USER_CONTENT_UTF8_BYTES = 98_304
MAXIMUM_OUTPUT_UTF8_BYTES = 32_768
MAXIMUM_RESULT_ENVELOPE_UTF8_BYTES = 65_536
CONNECTION_TIMEOUT_MS = 10_000
RESPONSE_HEADER_TIMEOUT_MS = 30_000
COMPLETE_INFERENCE_TIMEOUT_MS = 120_000
CANCELLATION_DEADLINE_MS = 10_000
WORKER_SHUTDOWN_DEADLINE_MS = 15_000

BoundedWorkerIdentifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
BoundedWorkerText = Annotated[str, StringConstraints(min_length=1, max_length=512)]


class _ProviderWorkerModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
    )

    @staticmethod
    def _utc(value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _reject_binary_text(value: str) -> str:
        if "\x00" in value:
            raise ValueError("text fields must not contain binary control data")
        return value

    @staticmethod
    def _utf8_size(value: str) -> int:
        return len(value.encode("utf-8"))


class ProviderWorkerExecutionPolicy(_ProviderWorkerModel):
    """Single-request execution posture for the bounded worker profile."""

    policy_id: Literal["worker.execution.openai-codex.single-request.v1"] = (
        _EXECUTION_POLICY_ID
    )
    maximum_concurrent_workers: Literal[1] = 1
    maximum_concurrent_requests_per_worker: Literal[1] = 1
    maximum_requests_per_worker_lifetime: Literal[1] = 1
    request_queue_capacity: Literal[0] = 0
    provider_calls_per_request_maximum: Literal[1] = 1
    model_list_calls_per_request_maximum: Literal[0] = 0
    credential_refresh_calls_per_request_maximum: Literal[0] = 0
    process_reuse: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    persistent_memory: ProviderWorkerFeaturePolicy = (
        ProviderWorkerFeaturePolicy.DISABLED
    )
    conversation_history: ProviderWorkerFeaturePolicy = (
        ProviderWorkerFeaturePolicy.DISABLED
    )
    background_tasks: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    subworkers: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    subagents: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    tools: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    hosted_tools: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    MCP: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    streaming: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    automatic_retry: ProviderWorkerFeaturePolicy = ProviderWorkerFeaturePolicy.DISABLED
    automatic_fallback: ProviderWorkerFeaturePolicy = (
        ProviderWorkerFeaturePolicy.DISABLED
    )


class ProviderWorkerRequestPolicy(_ProviderWorkerModel):
    """Request authority and bounded text-input policy."""

    policy_id: Literal["worker.request.openai-codex.pilot.v1"] = _REQUEST_POLICY_ID
    input_kind: ProviderWorkerInputKind = ProviderWorkerInputKind.TEXT
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    maximum_prompt_tokens: Literal[32768] = MAXIMUM_PROMPT_TOKENS
    reserved_system_instruction_tokens: Literal[8192] = (
        RESERVED_SYSTEM_INSTRUCTION_TOKENS
    )
    maximum_user_content_tokens: Literal[24576] = MAXIMUM_USER_CONTENT_TOKENS
    maximum_request_utf8_bytes: Literal[131072] = MAXIMUM_REQUEST_UTF8_BYTES
    maximum_user_content_utf8_bytes: Literal[98304] = MAXIMUM_USER_CONTENT_UTF8_BYTES
    caller_system_instructions_allowed: Literal[False] = False
    caller_provider_allowed: Literal[False] = False
    caller_model_allowed: Literal[False] = False
    caller_endpoint_allowed: Literal[False] = False
    caller_generation_parameters_allowed: Literal[False] = False
    caller_timeout_parameters_allowed: Literal[False] = False
    caller_tools_allowed: Literal[False] = False
    caller_metadata_passthrough_allowed: Literal[False] = False
    oversized_request_policy: ProviderWorkerOversizedRequestPolicy = (
        ProviderWorkerOversizedRequestPolicy.FAIL_BEFORE_PROVIDER_CALL
    )

    @model_validator(mode="after")
    def token_budget_must_fit_prompt(self) -> "ProviderWorkerRequestPolicy":
        if (
            self.reserved_system_instruction_tokens + self.maximum_user_content_tokens
            > self.maximum_prompt_tokens
        ):
            raise ValueError(
                "worker request token budget exceeds maximum prompt tokens"
            )
        return self


class ProviderWorkerResultPolicy(_ProviderWorkerModel):
    """Bounded single-text result envelope policy."""

    policy_id: Literal["worker.result.openai-codex.single-text.v1"] = _RESULT_POLICY_ID
    output_kind: ProviderWorkerOutputKind = ProviderWorkerOutputKind.TEXT
    maximum_output_tokens: Literal[4096] = MAXIMUM_OUTPUT_TOKENS
    maximum_output_utf8_bytes: Literal[32768] = MAXIMUM_OUTPUT_UTF8_BYTES
    maximum_result_envelope_utf8_bytes: Literal[65536] = (
        MAXIMUM_RESULT_ENVELOPE_UTF8_BYTES
    )
    raw_provider_response_allowed: Literal[False] = False
    reasoning_trace_allowed: Literal[False] = False
    tool_calls_allowed: Literal[False] = False
    stream_chunks_allowed: Literal[False] = False
    provider_headers_allowed: Literal[False] = False
    credential_metadata_allowed: Literal[False] = False
    automatic_file_write_allowed: Literal[False] = False
    persistent_output_allowed: Literal[False] = False


class ProviderWorkerTimeoutPolicy(_ProviderWorkerModel):
    """Worker and provider timeout limits for the bounded profile."""

    policy_id: Literal["worker.timeout.openai-codex.single-request.v1"] = (
        _TIMEOUT_POLICY_ID
    )
    startup_timeout_ms: Literal[30000] = 30_000
    connection_timeout_ms: Literal[10000] = CONNECTION_TIMEOUT_MS
    response_header_timeout_ms: Literal[30000] = RESPONSE_HEADER_TIMEOUT_MS
    complete_inference_timeout_ms: Literal[120000] = COMPLETE_INFERENCE_TIMEOUT_MS
    cancellation_deadline_ms: Literal[10000] = CANCELLATION_DEADLINE_MS
    worker_shutdown_deadline_ms: Literal[15000] = WORKER_SHUTDOWN_DEADLINE_MS
    maximum_worker_lifetime_ms: Literal[180000] = 180_000
    caller_timeout_override_allowed: Literal[False] = False
    frontend_timeout_override_allowed: Literal[False] = False
    environment_timeout_override_allowed: Literal[False] = False


class BoundedProviderWorkerProfile(_ProviderWorkerModel):
    """Public immutable P15.M8 OpenAI Codex bounded worker profile."""

    schema_version: Literal[1] = PROVIDER_WORKER_PROFILE_SCHEMA_VERSION
    profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    state: ProviderWorkerProfileState = (
        ProviderWorkerProfileState.PROFILE_READY_RUNTIME_UNVERIFIED
    )
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    credential_store_id: Literal["openai-codex.primary"] = (
        OPENAI_CODEX_CREDENTIAL_STORE_ID
    )
    execution_policy: ProviderWorkerExecutionPolicy = Field(
        default_factory=ProviderWorkerExecutionPolicy
    )
    request_policy: ProviderWorkerRequestPolicy = Field(
        default_factory=ProviderWorkerRequestPolicy
    )
    result_policy: ProviderWorkerResultPolicy = Field(
        default_factory=ProviderWorkerResultPolicy
    )
    timeout_policy: ProviderWorkerTimeoutPolicy = Field(
        default_factory=ProviderWorkerTimeoutPolicy
    )
    system_instruction_policy_id: Literal["worker.system.openai-codex.p15-pilot.v1"] = (
        _SYSTEM_INSTRUCTION_POLICY_ID
    )
    system_instruction_source: Literal["tracked_internal_template"] = (
        _SYSTEM_INSTRUCTION_SOURCE
    )
    caller_system_instruction_allowed: Literal[False] = False
    frontend_system_instruction_allowed: Literal[False] = False
    provider_supplied_system_instruction_allowed: Literal[False] = False
    worker_process_required: Literal[True] = True
    inference_gate_required: Literal[True] = True
    controlled_lifecycle_gate_required: Literal[True] = True
    runtime_entitlement_verified: Literal[False] = False
    runtime_transport_verified: Literal[False] = False
    worker_runtime_verified: Literal[False] = False


class BoundedProviderWorkerRequest(_ProviderWorkerModel):
    """Text-only single-request protocol envelope."""

    schema_version: Literal[1] = PROVIDER_WORKER_PROFILE_SCHEMA_VERSION
    request_id: BoundedWorkerIdentifier
    profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    runtime_id: BoundedWorkerIdentifier
    correlation_id: BoundedWorkerIdentifier
    requested_by: BoundedWorkerIdentifier
    submitted_at_utc: datetime
    input_kind: ProviderWorkerInputKind = ProviderWorkerInputKind.TEXT
    user_content: str = Field(min_length=1, repr=False)

    @field_validator("submitted_at_utc", mode="after")
    @classmethod
    def submitted_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @field_validator("user_content", mode="after")
    @classmethod
    def user_content_must_be_bounded_text(cls, value: str) -> str:
        value = cls._reject_binary_text(value)
        if cls._utf8_size(value) > MAXIMUM_USER_CONTENT_UTF8_BYTES:
            raise ValueError("worker request user content exceeds UTF-8 byte limit")
        return value


class BoundedProviderWorkerFailure(_ProviderWorkerModel):
    """Bounded failure envelope for worker request/result protocol."""

    schema_version: Literal[1] = PROVIDER_WORKER_PROFILE_SCHEMA_VERSION
    failure_code: BoundedWorkerIdentifier
    stage: ProviderWorkerFailureStage
    retryable: Literal[False] = False
    safe_message: BoundedWorkerText

    @field_validator("safe_message", mode="after")
    @classmethod
    def safe_message_must_be_printable(cls, value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError(
                "safe failure messages must not contain control characters"
            )
        return value


class BoundedProviderWorkerResult(_ProviderWorkerModel):
    """Text-only single-result protocol envelope."""

    schema_version: Literal[1] = PROVIDER_WORKER_PROFILE_SCHEMA_VERSION
    request_id: BoundedWorkerIdentifier
    profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    runtime_id: BoundedWorkerIdentifier
    correlation_id: BoundedWorkerIdentifier
    state: ProviderWorkerResultState
    completed_at_utc: datetime
    output_kind: ProviderWorkerOutputKind = ProviderWorkerOutputKind.TEXT
    output_text: str | None = Field(default=None, repr=False)
    usage_record_id: BoundedWorkerIdentifier | None = None
    failure: BoundedProviderWorkerFailure | None = None

    @field_validator("completed_at_utc", mode="after")
    @classmethod
    def completed_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @field_validator("output_text", mode="after")
    @classmethod
    def output_text_must_be_bounded(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = cls._reject_binary_text(value)
        if not value.strip():
            raise ValueError("completed worker results require output text")
        if cls._utf8_size(value) > MAXIMUM_OUTPUT_UTF8_BYTES:
            raise ValueError("worker result output exceeds UTF-8 byte limit")
        return value

    @model_validator(mode="after")
    def result_state_must_match_payload(self) -> "BoundedProviderWorkerResult":
        if self.state is ProviderWorkerResultState.COMPLETED:
            if self.output_text is None or self.failure is not None:
                raise ValueError("completed worker result requires output text only")
            return self
        if self.output_text is not None or self.failure is None:
            raise ValueError("non-completed worker result requires failure only")
        if (
            self.state is ProviderWorkerResultState.CANCELLED
            and self.failure.stage is not ProviderWorkerFailureStage.CANCELLATION
        ):
            raise ValueError(
                "cancelled worker result requires cancellation failure stage"
            )
        return self


class ProviderWorkerResolutionRequest(_ProviderWorkerModel):
    """Safe request for internal worker-profile compatibility resolution."""

    schema_version: Literal[1] = PROVIDER_WORKER_PROFILE_SCHEMA_VERSION
    worker_profile_id: BoundedWorkerIdentifier = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    provider_resolution_request: ProviderRuntimeResolutionRequest
    evaluated_at_utc: datetime

    @field_validator("evaluated_at_utc", mode="after")
    @classmethod
    def evaluated_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)


class ResolvedProviderWorkerBinding(_ProviderWorkerModel):
    """Internal resolved worker binding for the future inference gate."""

    worker_profile: BoundedProviderWorkerProfile
    provider_binding: ResolvedProviderRuntimeBinding
    resolved_state: Literal[ProviderWorkerProfileState.READY_FOR_INFERENCE_GATE] = (
        ProviderWorkerProfileState.READY_FOR_INFERENCE_GATE
    )
    resolved_at_utc: datetime

    @field_validator("resolved_at_utc", mode="after")
    @classmethod
    def resolved_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)


__all__ = [
    "PROVIDER_WORKER_PROFILE_SCHEMA_VERSION",
    "ProviderWorkerExecutionPolicy",
    "ProviderWorkerRequestPolicy",
    "ProviderWorkerResultPolicy",
    "ProviderWorkerTimeoutPolicy",
    "BoundedProviderWorkerProfile",
    "BoundedProviderWorkerRequest",
    "BoundedProviderWorkerResult",
    "BoundedProviderWorkerFailure",
    "ProviderWorkerResolutionRequest",
]
