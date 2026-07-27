"""Immutable contracts for the P15.7 single-worker controlled gate."""

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

from hermes_cli.agent_platform.provider_accounting.contracts import (
    ProviderAccountingRecord,
    ProviderAccountingWorkerResultLink,
)
from hermes_cli.agent_platform.provider_failure_policy.contracts import (
    ProviderFailureAccountingLink,
    ProviderFailureRecord,
    ProviderRetryDecision,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    BoundedProviderWorkerRequest,
    BoundedProviderWorkerResult,
)
from hermes_cli.agent_platform.provider_worker.enums import ProviderWorkerResultState


PROVIDER_WORKER_GATE_SCHEMA_VERSION = 1

OPENAI_CODEX_PROVIDER_WORKER_GATE_ID = (
    "gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1"
)
OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID = (
    "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
)
OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID = (
    "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID = (
    "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
OPENAI_CODEX_PROVIDER_FAILURE_POLICY_ID = (
    "failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
OPENAI_CODEX_CREDENTIAL_STORE_ID = "openai-codex.primary"
OPENAI_CODEX_PROVIDER = "openai-codex"
OPENAI_CODEX_AUTHENTICATION = "chatgpt_oauth"
OPENAI_CODEX_ENDPOINT = "https://chatgpt.com/backend-api/codex"
OPENAI_CODEX_MODEL_ID = "gpt-5.5"
OPENAI_CODEX_TRANSPORT = "codex_responses"
OPENAI_CODEX_SINGLE_DISPATCH_EVENT_CONSUMER = (
    "agent.codex_runtime._consume_codex_event_stream"
)
OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION = (
    "Return only the exact literal requested by the user. Do not call tools. "
    "Do not include commentary, markdown, punctuation or additional text."
)
OPENAI_CODEX_P15_7_EXPECTED_OUTPUT = "PEPPER_P15_7_OK"
OPENAI_CODEX_REASONING_EFFORT = "medium"
OPENAI_CODEX_REASONING_SUMMARY = "auto"

GOVERNED_CREDENTIAL_LEASE_TTL_MS = 300_000
GOVERNED_CREDENTIAL_MINIMUM_REMAINING_LIFETIME_MS = 300_000
MAXIMUM_RESPONSES_CREATE_CALLS = 1
SDK_MAX_RETRIES = 0
WORKER_RETRY_ATTEMPTS = 0
WORKER_FALLBACK_ATTEMPTS = 0

GateIdentifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
GateSafeText = Annotated[str, StringConstraints(min_length=1, max_length=128)]
GateCheckpoint = Literal[
    "request_validated",
    "client_construction_started",
    "client_constructed",
    "dispatch_started",
    "event_stream_obtained",
    "stream_iteration_started",
    "first_event_observed",
    "terminal_event_observed",
    "accounting_started",
    "accounting_completed",
    "worker_result_completed",
    "cleanup_started",
    "cleanup_completed",
]
GateFailurePhase = Literal[
    "preflight",
    "client_construction",
    "dispatch",
    "stream",
    "terminal",
    "accounting",
    "cleanup_local_only",
]
GateLocalFailureCategory = Literal[
    "local_environment_missing_dependency",
    "local_environment_import_failure",
    "local_environment_missing_file",
    "local_environment_permission_failure",
    "local_request_construction_or_contract_failure",
    "local_request_validation_failure",
    "local_client_construction_failure",
    "provider_failure_delegated_to_p15_6",
    "local_internal_unknown",
]
GateCleanupStatus = Literal["not_started", "passed", "failed"]


class _ProviderWorkerGateModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
        protected_namespaces=(),
    )

    @staticmethod
    def _utc(value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _reject_control_text(value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("text fields must not contain control characters")
        return value


class ProviderWorkerGatePolicy(_ProviderWorkerGateModel):
    """Fixed policy for one worker, one request and one provider dispatch."""

    schema_version: Literal[1] = PROVIDER_WORKER_GATE_SCHEMA_VERSION
    gate_id: Literal["gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1"] = (
        OPENAI_CODEX_PROVIDER_WORKER_GATE_ID
    )
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
    ] = OPENAI_CODEX_PROVIDER_FAILURE_POLICY_ID
    credential_store_id: Literal["openai-codex.primary"] = (
        OPENAI_CODEX_CREDENTIAL_STORE_ID
    )
    provider: Literal["openai-codex"] = OPENAI_CODEX_PROVIDER
    authentication: Literal["chatgpt_oauth"] = OPENAI_CODEX_AUTHENTICATION
    endpoint: Literal["https://chatgpt.com/backend-api/codex"] = OPENAI_CODEX_ENDPOINT
    model_id: Literal["gpt-5.5"] = OPENAI_CODEX_MODEL_ID
    transport: Literal["codex_responses"] = OPENAI_CODEX_TRANSPORT
    maximum_concurrent_workers: Literal[1] = 1
    maximum_concurrent_requests_per_worker: Literal[1] = 1
    maximum_requests_per_worker_lifetime: Literal[1] = 1
    maximum_provider_dispatches_per_request: Literal[1] = 1
    responses_create_call_maximum: Literal[1] = MAXIMUM_RESPONSES_CREATE_CALLS
    SDK_max_retries: Literal[0] = SDK_MAX_RETRIES
    worker_retry_attempts: Literal[0] = WORKER_RETRY_ATTEMPTS
    worker_fallback_attempts: Literal[0] = WORKER_FALLBACK_ATTEMPTS
    credential_refresh_calls_per_request: Literal[0] = 0
    model_list_calls_per_request: Literal[0] = 0
    wire_max_output_tokens_allowed: Literal[False] = False
    credential_lease_ttl_ms: Literal[300000] = GOVERNED_CREDENTIAL_LEASE_TTL_MS
    minimum_remaining_credential_lifetime_ms: Literal[300000] = (
        GOVERNED_CREDENTIAL_MINIMUM_REMAINING_LIFETIME_MS
    )
    temporary_credential_projection_required: Literal[True] = True
    stdin_stdout_worker_protocol_required: Literal[True] = True
    stream_requested: Literal[True] = True
    event_consumer: Literal["agent.codex_runtime._consume_codex_event_stream"] = (
        OPENAI_CODEX_SINGLE_DISPATCH_EVENT_CONSUMER
    )
    local_expected_output: Literal["PEPPER_P15_7_OK"] = (
        OPENAI_CODEX_P15_7_EXPECTED_OUTPUT
    )
    local_exact_output_validation_required: Literal[True] = True
    caller_system_instruction_allowed: Literal[False] = False
    caller_provider_allowed: Literal[False] = False
    caller_model_allowed: Literal[False] = False
    caller_endpoint_allowed: Literal[False] = False
    caller_generation_parameters_allowed: Literal[False] = False
    caller_timeout_parameters_allowed: Literal[False] = False
    tools_allowed: Literal[False] = False
    hosted_tools_allowed: Literal[False] = False
    MCP_allowed: Literal[False] = False
    automatic_retry_allowed: Literal[False] = False
    automatic_fallback_allowed: Literal[False] = False
    credential_rotation_allowed: Literal[False] = False
    raw_provider_response_retained: Literal[False] = False
    provider_headers_retained: Literal[False] = False
    credential_metadata_retained: Literal[False] = False


class ProviderWorkerGateRequest(_ProviderWorkerGateModel):
    """Single governed worker request plus fixed dispatch metadata."""

    schema_version: Literal[1] = PROVIDER_WORKER_GATE_SCHEMA_VERSION
    gate_id: Literal["gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1"] = (
        OPENAI_CODEX_PROVIDER_WORKER_GATE_ID
    )
    policy: ProviderWorkerGatePolicy = Field(default_factory=ProviderWorkerGatePolicy)
    worker_request: BoundedProviderWorkerRequest
    usage_record_id: GateIdentifier
    requested_at_utc: datetime
    system_instruction: Literal[
        "Return only the exact literal requested by the user. Do not call tools. Do not include commentary, markdown, punctuation or additional text."
    ] = OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION
    stream_requested: Literal[True] = True

    @field_validator("requested_at_utc", mode="after")
    @classmethod
    def requested_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @model_validator(mode="after")
    def request_must_match_fixed_policy(self) -> "ProviderWorkerGateRequest":
        if self.worker_request.profile_id != self.policy.worker_profile_id:
            raise ValueError("worker request profile must match gate policy")
        if (
            self.worker_request.provider_runtime_profile_id
            != self.policy.provider_runtime_profile_id
        ):
            raise ValueError("worker request provider profile must match gate policy")
        return self


class ProviderWorkerGateDispatchEvidence(_ProviderWorkerGateModel):
    """Secret-free evidence for the single provider dispatch attempt."""

    schema_version: Literal[1] = PROVIDER_WORKER_GATE_SCHEMA_VERSION
    gate_id: Literal["gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1"] = (
        OPENAI_CODEX_PROVIDER_WORKER_GATE_ID
    )
    request_id: GateIdentifier
    runtime_id: GateIdentifier
    correlation_id: GateIdentifier
    usage_record_id: GateIdentifier
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
    ] = OPENAI_CODEX_PROVIDER_FAILURE_POLICY_ID
    provider: Literal["openai-codex"] = OPENAI_CODEX_PROVIDER
    authentication: Literal["chatgpt_oauth"] = OPENAI_CODEX_AUTHENTICATION
    endpoint: Literal["https://chatgpt.com/backend-api/codex"] = OPENAI_CODEX_ENDPOINT
    model_id: Literal["gpt-5.5"] = OPENAI_CODEX_MODEL_ID
    transport: Literal["codex_responses"] = OPENAI_CODEX_TRANSPORT
    responses_create_call_count: Literal[0, 1]
    stream_requested: Literal[True] = True
    SDK_max_retries: Literal[0] = SDK_MAX_RETRIES
    worker_retry_attempts: Literal[0] = WORKER_RETRY_ATTEMPTS
    worker_fallback_attempts: Literal[0] = WORKER_FALLBACK_ATTEMPTS
    credential_refresh_calls: Literal[0] = 0
    model_list_calls: Literal[0] = 0
    event_consumer: Literal["agent.codex_runtime._consume_codex_event_stream"] = (
        OPENAI_CODEX_SINGLE_DISPATCH_EVENT_CONSUMER
    )
    started_at_utc: datetime
    completed_at_utc: datetime
    provider_response_id_present: bool = False
    provider_response_id_retained_on_failure: Literal[False] = False
    raw_provider_response_retained: Literal[False] = False
    provider_headers_retained: Literal[False] = False
    credential_metadata_retained: Literal[False] = False

    @field_validator("started_at_utc", "completed_at_utc", mode="after")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @model_validator(mode="after")
    def completed_must_not_precede_started(
        self,
    ) -> "ProviderWorkerGateDispatchEvidence":
        if self.completed_at_utc < self.started_at_utc:
            raise ValueError("completed_at_utc must not precede started_at_utc")
        return self


class ProviderWorkerGateDiagnostics(_ProviderWorkerGateModel):
    """Bounded P15.7-local diagnostics with no raw provider or host detail."""

    checkpoints: tuple[GateCheckpoint, ...] = Field(
        default_factory=tuple, max_length=16
    )
    provider_dispatches_for_attempt: Literal[0, 1] = 0
    failure_phase: GateFailurePhase | None = None
    local_failure_category: GateLocalFailureCategory | None = None
    safe_exception_class: GateSafeText | None = Field(default=None, repr=False)
    safe_exception_module: GateSafeText | None = Field(default=None, repr=False)
    cleanup_status: GateCleanupStatus = "not_started"
    cleanup_failure_category: GateLocalFailureCategory | None = None
    cleanup_safe_exception_class: GateSafeText | None = Field(default=None, repr=False)
    cleanup_safe_exception_module: GateSafeText | None = Field(default=None, repr=False)
    raw_exception_retained: Literal[False] = False
    traceback_retained: Literal[False] = False
    request_body_retained: Literal[False] = False
    response_body_retained: Literal[False] = False
    provider_text_retained: Literal[False] = False
    provider_headers_retained: Literal[False] = False
    provider_response_id_retained: Literal[False] = False
    credential_metadata_retained: Literal[False] = False

    @field_validator(
        "safe_exception_class",
        "safe_exception_module",
        "cleanup_safe_exception_class",
        "cleanup_safe_exception_module",
        mode="after",
    )
    @classmethod
    def diagnostic_text_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return cls._reject_control_text(value)

    @model_validator(mode="after")
    def phase_must_match_dispatch_counter(self) -> "ProviderWorkerGateDiagnostics":
        if self.failure_phase in {"preflight", "client_construction"}:
            if self.provider_dispatches_for_attempt != 0:
                raise ValueError(
                    "pre-dispatch diagnostics must have dispatch count zero"
                )
        if self.failure_phase in {"dispatch", "stream", "terminal", "accounting"}:
            if self.provider_dispatches_for_attempt != 1:
                raise ValueError(
                    "post-dispatch diagnostics must have dispatch count one"
                )
        if self.cleanup_status == "failed" and self.cleanup_failure_category is None:
            raise ValueError("failed cleanup diagnostics require a cleanup category")
        return self


class ProviderWorkerGateResult(_ProviderWorkerGateModel):
    """Controlled-gate result linking worker, accounting and failure evidence."""

    schema_version: Literal[1] = PROVIDER_WORKER_GATE_SCHEMA_VERSION
    gate_id: Literal["gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1"] = (
        OPENAI_CODEX_PROVIDER_WORKER_GATE_ID
    )
    worker_result: BoundedProviderWorkerResult
    dispatch_evidence: ProviderWorkerGateDispatchEvidence
    accounting_record: ProviderAccountingRecord | None = None
    accounting_link: ProviderAccountingWorkerResultLink | None = None
    failure_record: ProviderFailureRecord | None = None
    failure_retry_decision: ProviderRetryDecision | None = None
    failure_accounting_link: ProviderFailureAccountingLink | None = None
    diagnostics: ProviderWorkerGateDiagnostics = Field(
        default_factory=ProviderWorkerGateDiagnostics,
    )
    credential_lease_release_required: Literal[True] = True
    raw_provider_response_retained: Literal[False] = False
    provider_headers_retained: Literal[False] = False
    credential_metadata_retained: Literal[False] = False

    @model_validator(mode="after")
    def result_must_have_required_links(self) -> "ProviderWorkerGateResult":
        if (
            self.diagnostics.provider_dispatches_for_attempt
            != self.dispatch_evidence.responses_create_call_count
        ):
            raise ValueError("diagnostic dispatch count must match dispatch evidence")
        completed = self.worker_result.state is ProviderWorkerResultState.COMPLETED
        if completed:
            if (
                self.failure_record is not None
                or self.failure_retry_decision is not None
            ):
                raise ValueError(
                    "completed gate result must not carry failure evidence"
                )
            if self.accounting_record is None or self.accounting_link is None:
                raise ValueError("completed gate result requires accounting linkage")
            return self
        if self.failure_record is None or self.failure_retry_decision is None:
            raise ValueError("failed gate result requires failure and retry evidence")
        if (
            self.failure_record.provider_dispatch_count
            != self.dispatch_evidence.responses_create_call_count
        ):
            raise ValueError("failure dispatch count must match dispatch evidence")
        if self.dispatch_evidence.responses_create_call_count == 1:
            if (
                self.accounting_record is None
                or self.accounting_link is None
                or self.failure_accounting_link is None
            ):
                raise ValueError(
                    "post-dispatch failed gate result requires accounting linkage"
                )
        return self


__all__ = [
    "GOVERNED_CREDENTIAL_LEASE_TTL_MS",
    "GOVERNED_CREDENTIAL_MINIMUM_REMAINING_LIFETIME_MS",
    "MAXIMUM_RESPONSES_CREATE_CALLS",
    "OPENAI_CODEX_AUTHENTICATION",
    "OPENAI_CODEX_CREDENTIAL_STORE_ID",
    "OPENAI_CODEX_ENDPOINT",
    "OPENAI_CODEX_MODEL_ID",
    "OPENAI_CODEX_P15_7_EXPECTED_OUTPUT",
    "OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION",
    "OPENAI_CODEX_PROVIDER",
    "OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID",
    "OPENAI_CODEX_PROVIDER_FAILURE_POLICY_ID",
    "OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID",
    "OPENAI_CODEX_PROVIDER_WORKER_GATE_ID",
    "OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID",
    "OPENAI_CODEX_REASONING_EFFORT",
    "OPENAI_CODEX_REASONING_SUMMARY",
    "OPENAI_CODEX_SINGLE_DISPATCH_EVENT_CONSUMER",
    "OPENAI_CODEX_TRANSPORT",
    "PROVIDER_WORKER_GATE_SCHEMA_VERSION",
    "SDK_MAX_RETRIES",
    "WORKER_FALLBACK_ATTEMPTS",
    "WORKER_RETRY_ATTEMPTS",
    "ProviderWorkerGateDispatchEvidence",
    "ProviderWorkerGateDiagnostics",
    "ProviderWorkerGatePolicy",
    "ProviderWorkerGateRequest",
    "ProviderWorkerGateResult",
]
