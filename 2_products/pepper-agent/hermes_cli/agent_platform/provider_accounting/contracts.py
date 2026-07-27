"""Immutable contracts for governed provider usage, cost and timeout accounting."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingLinkState,
    ProviderAccountingOutcome,
    ProviderCostSource,
    ProviderCostStatus,
    ProviderTimeoutDisposition,
    ProviderTimeoutStage,
    ProviderUsageCompleteness,
    ProviderUsageSource,
)


PROVIDER_ACCOUNTING_SCHEMA_VERSION = 1

OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID = (
    "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID = (
    "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
)
OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID = (
    "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
OPENAI_CODEX_PROVIDER_MODEL_ID = "gpt-5.5"
OPENAI_CODEX_BILLING_MODE = "subscription_included"

MAXIMUM_ACCOUNTING_TOKEN_COUNT = 2_147_483_647

BoundedAccountingIdentifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
BoundedProviderText = Annotated[str, StringConstraints(min_length=1, max_length=512)]


class _ProviderAccountingModel(BaseModel):
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


class ProviderAccountingPolicy(_ProviderAccountingModel):
    """Fixed accounting posture for the OpenAI Codex bounded worker route."""

    schema_version: Literal[1] = PROVIDER_ACCOUNTING_SCHEMA_VERSION
    policy_id: Literal[
        "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    worker_profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    model_id: Literal["gpt-5.5"] = OPENAI_CODEX_PROVIDER_MODEL_ID
    billing_mode: Literal["subscription_included"] = OPENAI_CODEX_BILLING_MODE
    maximum_provider_calls_per_record: Literal[1] = 1
    usage_record_id_required_on_worker_result: Literal[True] = True
    provider_usage_required_when_available: Literal[True] = True
    exact_marginal_request_cost_available: Literal[False] = False
    provider_billing_api_allowed: Literal[False] = False
    pricing_metadata_lookup_allowed: Literal[False] = False
    usage_api_allowed: Literal[False] = False
    raw_provider_response_allowed: Literal[False] = False
    provider_headers_allowed: Literal[False] = False
    credential_metadata_allowed: Literal[False] = False


class ProviderUsageCounters(_ProviderAccountingModel):
    """Canonical non-secret token buckets normalized from provider usage."""

    input_tokens: int = Field(default=0, ge=0, le=MAXIMUM_ACCOUNTING_TOKEN_COUNT)
    cache_read_input_tokens: int = Field(
        default=0,
        ge=0,
        le=MAXIMUM_ACCOUNTING_TOKEN_COUNT,
    )
    cache_write_input_tokens: int = Field(
        default=0,
        ge=0,
        le=MAXIMUM_ACCOUNTING_TOKEN_COUNT,
    )
    output_tokens: int = Field(default=0, ge=0, le=MAXIMUM_ACCOUNTING_TOKEN_COUNT)
    reasoning_output_tokens: int = Field(
        default=0,
        ge=0,
        le=MAXIMUM_ACCOUNTING_TOKEN_COUNT,
    )
    provider_total_tokens: int | None = Field(
        default=None,
        ge=0,
        le=MAXIMUM_ACCOUNTING_TOKEN_COUNT,
    )
    request_count: Literal[1] = 1

    @property
    def prompt_tokens(self) -> int:
        return (
            self.input_tokens
            + self.cache_read_input_tokens
            + self.cache_write_input_tokens
        )

    @property
    def canonical_total_tokens(self) -> int:
        return self.prompt_tokens + self.output_tokens

    @model_validator(mode="after")
    def provider_total_must_cover_canonical_tokens(self) -> "ProviderUsageCounters":
        if (
            self.provider_total_tokens is not None
            and self.provider_total_tokens < self.canonical_total_tokens
        ):
            raise ValueError("provider total tokens must cover canonical token buckets")
        return self


class ProviderUsageEvidence(_ProviderAccountingModel):
    """Provider usage evidence stripped to deterministic accounting fields."""

    schema_version: Literal[1] = PROVIDER_ACCOUNTING_SCHEMA_VERSION
    source: ProviderUsageSource
    completeness: ProviderUsageCompleteness
    counters: ProviderUsageCounters = Field(default_factory=ProviderUsageCounters)
    observed_at_utc: datetime
    provider_response_id: BoundedAccountingIdentifier | None = None
    returned_model_id: Literal["gpt-5.5"] | None = OPENAI_CODEX_PROVIDER_MODEL_ID
    finish_reason: BoundedProviderText | None = None
    raw_usage_payload_allowed: Literal[False] = False
    raw_provider_response_allowed: Literal[False] = False
    provider_headers_allowed: Literal[False] = False

    @field_validator("observed_at_utc", mode="after")
    @classmethod
    def observed_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @field_validator("finish_reason", mode="after")
    @classmethod
    def finish_reason_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return cls._reject_control_text(value)

    @model_validator(mode="after")
    def missing_usage_must_be_explicit(self) -> "ProviderUsageEvidence":
        if self.completeness is ProviderUsageCompleteness.MISSING:
            if self.source is not ProviderUsageSource.PROVIDER_OMITTED:
                raise ValueError("missing usage must use provider_omitted source")
            if self.counters.canonical_total_tokens != 0:
                raise ValueError("missing usage must not contain token counts")
        return self


class ProviderCostAccounting(_ProviderAccountingModel):
    """Subscription-included cost accounting without live billing lookup."""

    schema_version: Literal[1] = PROVIDER_ACCOUNTING_SCHEMA_VERSION
    billing_mode: Literal["subscription_included"] = OPENAI_CODEX_BILLING_MODE
    status: ProviderCostStatus = ProviderCostStatus.INCLUDED
    source: ProviderCostSource = ProviderCostSource.SUBSCRIPTION_INCLUDED
    currency: Literal["USD"] = "USD"
    amount_usd: Decimal | None = Decimal("0")
    exact_marginal_request_cost_available: Literal[False] = False
    estimated_pricing_lookup_performed: Literal[False] = False
    provider_billing_api_called: Literal[False] = False
    usage_api_called: Literal[False] = False
    notes: tuple[BoundedProviderText, ...] = (
        "subscription route records included marginal request cost as zero",
    )

    @model_validator(mode="after")
    def cost_status_must_match_amount_and_source(self) -> "ProviderCostAccounting":
        if self.status is ProviderCostStatus.INCLUDED:
            if self.amount_usd != Decimal("0"):
                raise ValueError("included cost records must have zero amount_usd")
            if self.source is not ProviderCostSource.SUBSCRIPTION_INCLUDED:
                raise ValueError("included cost records must use subscription source")
        if (
            self.status is ProviderCostStatus.UNAVAILABLE
            and self.amount_usd is not None
        ):
            raise ValueError("unavailable cost records must not carry an amount")
        return self


class ProviderTimeoutBudget(_ProviderAccountingModel):
    """Timeout limits copied into accounting evidence for deterministic review."""

    connection_timeout_ms: Literal[10000] = 10_000
    response_header_timeout_ms: Literal[30000] = 30_000
    complete_inference_timeout_ms: Literal[120000] = 120_000
    cancellation_deadline_ms: Literal[10000] = 10_000
    worker_shutdown_deadline_ms: Literal[15000] = 15_000
    caller_timeout_override_allowed: Literal[False] = False
    frontend_timeout_override_allowed: Literal[False] = False
    environment_timeout_override_allowed: Literal[False] = False


class ProviderTimeoutAccounting(_ProviderAccountingModel):
    """Local elapsed-time evidence for one bounded provider request."""

    schema_version: Literal[1] = PROVIDER_ACCOUNTING_SCHEMA_VERSION
    outcome: ProviderAccountingOutcome
    disposition: ProviderTimeoutDisposition
    budget: ProviderTimeoutBudget = Field(default_factory=ProviderTimeoutBudget)
    started_at_utc: datetime
    completed_at_utc: datetime
    elapsed_ms: int = Field(ge=0, le=600_000)
    timed_out: bool
    timeout_stage: ProviderTimeoutStage | None = None

    @field_validator("started_at_utc", "completed_at_utc", mode="after")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @model_validator(mode="after")
    def timeout_fields_must_match_outcome(self) -> "ProviderTimeoutAccounting":
        expected_elapsed = int(
            (self.completed_at_utc - self.started_at_utc).total_seconds() * 1000
        )
        if expected_elapsed < 0:
            raise ValueError("completed_at_utc must not precede started_at_utc")
        if self.elapsed_ms != expected_elapsed:
            raise ValueError("elapsed_ms must match started/completed timestamps")
        if self.outcome is ProviderAccountingOutcome.TIMED_OUT:
            if not self.timed_out:
                raise ValueError("timed_out must be true for timed_out outcome")
            if self.timeout_stage is None:
                raise ValueError("timed_out outcome requires timeout_stage")
            if self.disposition is not ProviderTimeoutDisposition.TIMED_OUT:
                raise ValueError("timed_out outcome requires timed_out disposition")
            return self
        if self.timed_out or self.timeout_stage is not None:
            raise ValueError(
                "non-timeout outcomes must not carry timeout stage evidence"
            )
        if self.disposition is not ProviderTimeoutDisposition.WITHIN_BUDGET:
            raise ValueError("non-timeout outcomes must be within_budget")
        return self


class ProviderAccountingRecord(_ProviderAccountingModel):
    """Single-request usage, cost and timeout accounting record."""

    schema_version: Literal[1] = PROVIDER_ACCOUNTING_SCHEMA_VERSION
    usage_record_id: BoundedAccountingIdentifier
    request_id: BoundedAccountingIdentifier
    runtime_id: BoundedAccountingIdentifier
    correlation_id: BoundedAccountingIdentifier
    created_at_utc: datetime
    policy: ProviderAccountingPolicy = Field(default_factory=ProviderAccountingPolicy)
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    worker_profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    model_id: Literal["gpt-5.5"] = OPENAI_CODEX_PROVIDER_MODEL_ID
    usage: ProviderUsageEvidence
    cost: ProviderCostAccounting = Field(default_factory=ProviderCostAccounting)
    timeout: ProviderTimeoutAccounting
    raw_request_allowed: Literal[False] = False
    raw_response_allowed: Literal[False] = False
    credential_metadata_allowed: Literal[False] = False

    @field_validator("created_at_utc", mode="after")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return cls._utc(value)

    @model_validator(mode="after")
    def profile_fields_must_match_policy(self) -> "ProviderAccountingRecord":
        if self.provider_runtime_profile_id != self.policy.provider_runtime_profile_id:
            raise ValueError("provider runtime profile must match accounting policy")
        if self.worker_profile_id != self.policy.worker_profile_id:
            raise ValueError("worker profile must match accounting policy")
        if self.model_id != self.policy.model_id:
            raise ValueError("model_id must match accounting policy")
        return self


class ProviderAccountingWorkerResultLink(_ProviderAccountingModel):
    """Validated link from a worker result usage_record_id to accounting evidence."""

    schema_version: Literal[1] = PROVIDER_ACCOUNTING_SCHEMA_VERSION
    usage_record_id: BoundedAccountingIdentifier
    request_id: BoundedAccountingIdentifier
    runtime_id: BoundedAccountingIdentifier
    correlation_id: BoundedAccountingIdentifier
    worker_result_state: Literal["completed", "failed", "cancelled"]
    link_state: ProviderAccountingLinkState = ProviderAccountingLinkState.MATCHED


__all__ = [
    "PROVIDER_ACCOUNTING_SCHEMA_VERSION",
    "OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID",
    "OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID",
    "OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID",
    "OPENAI_CODEX_PROVIDER_MODEL_ID",
    "OPENAI_CODEX_BILLING_MODE",
    "ProviderAccountingPolicy",
    "ProviderAccountingRecord",
    "ProviderAccountingWorkerResultLink",
    "ProviderCostAccounting",
    "ProviderTimeoutAccounting",
    "ProviderTimeoutBudget",
    "ProviderUsageCounters",
    "ProviderUsageEvidence",
]
