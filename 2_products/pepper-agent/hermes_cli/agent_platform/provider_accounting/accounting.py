"""Pure helpers for governed provider usage, cost and timeout accounting."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
import math
from typing import Any

from hermes_cli.agent_platform.provider_accounting.contracts import (
    OPENAI_CODEX_PROVIDER_MODEL_ID,
    ProviderAccountingRecord,
    ProviderAccountingWorkerResultLink,
    ProviderCostAccounting,
    ProviderTimeoutAccounting,
    ProviderTimeoutBudget,
    ProviderUsageCounters,
    ProviderUsageEvidence,
)
from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingOutcome,
    ProviderCostSource,
    ProviderCostStatus,
    ProviderTimeoutDisposition,
    ProviderTimeoutStage,
    ProviderUsageCompleteness,
    ProviderUsageSource,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    BoundedProviderWorkerResult,
)


class ProviderAccountingError(ValueError):
    """Bounded error that never includes raw request or response bodies."""

    def __init__(
        self,
        *,
        code: str,
        usage_record_id: str | None = None,
        request_id: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.code = code
        self.usage_record_id = usage_record_id
        self.request_id = request_id
        self.validation_category = validation_category
        fragments = [f"code={code}"]
        if usage_record_id is not None:
            fragments.append(f"usage_record_id={usage_record_id}")
        if request_id is not None:
            fragments.append(f"request_id={request_id}")
        if validation_category is not None:
            fragments.append(f"validation_category={validation_category}")
        super().__init__(" ".join(fragments))


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProviderAccountingError(
            code="timestamp_not_utc",
            validation_category="timestamp",
        )
    return value.astimezone(timezone.utc)


def _field(value: Any, name: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _coerce_usage_int(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        return 0
    if isinstance(value, int):
        return max(value, 0)
    if isinstance(value, float):
        if not math.isfinite(value):
            return 0
        return max(int(value), 0)
    if isinstance(value, Decimal):
        return max(int(value), 0)
    if isinstance(value, str):
        try:
            return max(int(value.strip()), 0)
        except ValueError:
            return 0
    return 0


def _missing_usage(observed_at_utc: datetime) -> ProviderUsageEvidence:
    return ProviderUsageEvidence(
        source=ProviderUsageSource.PROVIDER_OMITTED,
        completeness=ProviderUsageCompleteness.MISSING,
        counters=ProviderUsageCounters(),
        observed_at_utc=_utc(observed_at_utc),
        returned_model_id=None,
    )


def normalize_codex_responses_usage(
    response_usage: Any,
    *,
    observed_at_utc: datetime,
    provider_response_id: str | None = None,
    finish_reason: str | None = None,
) -> ProviderUsageEvidence:
    """Normalize a synthetic Codex Responses usage shape into accounting buckets."""

    observed_at_utc = _utc(observed_at_utc)
    if not response_usage:
        return _missing_usage(observed_at_utc)

    input_total = _coerce_usage_int(_field(response_usage, "input_tokens"))
    output_tokens = _coerce_usage_int(_field(response_usage, "output_tokens"))
    input_details = _field(response_usage, "input_tokens_details")
    output_details = _field(response_usage, "output_tokens_details")
    cache_read_tokens = _coerce_usage_int(_field(input_details, "cached_tokens"))
    cache_write_tokens = _coerce_usage_int(
        _field(input_details, "cache_creation_tokens")
    )
    reasoning_tokens = _coerce_usage_int(_field(output_details, "reasoning_tokens"))
    provider_total = _coerce_usage_int(
        _field(response_usage, "total_tokens", input_total + output_tokens)
    )

    return ProviderUsageEvidence(
        source=ProviderUsageSource.CODEX_RESPONSES_PROVIDER_REPORTED,
        completeness=ProviderUsageCompleteness.COMPLETE,
        counters=ProviderUsageCounters(
            input_tokens=max(0, input_total - cache_read_tokens - cache_write_tokens),
            cache_read_input_tokens=cache_read_tokens,
            cache_write_input_tokens=cache_write_tokens,
            output_tokens=output_tokens,
            reasoning_output_tokens=reasoning_tokens,
            provider_total_tokens=provider_total,
        ),
        observed_at_utc=observed_at_utc,
        provider_response_id=provider_response_id,
        returned_model_id=OPENAI_CODEX_PROVIDER_MODEL_ID,
        finish_reason=finish_reason,
    )


def normalize_codex_app_server_usage(
    token_usage: Any,
    *,
    observed_at_utc: datetime,
) -> ProviderUsageEvidence:
    """Normalize a synthetic Codex app-server tokenUsage/updated payload."""

    observed_at_utc = _utc(observed_at_utc)
    if not token_usage:
        return _missing_usage(observed_at_utc)

    input_tokens = _coerce_usage_int(_field(token_usage, "inputTokens"))
    cache_read_tokens = _coerce_usage_int(_field(token_usage, "cachedInputTokens"))
    output_tokens = _coerce_usage_int(_field(token_usage, "outputTokens"))
    reasoning_tokens = _coerce_usage_int(_field(token_usage, "reasoningOutputTokens"))
    reported_total = _coerce_usage_int(_field(token_usage, "totalTokens"))

    return ProviderUsageEvidence(
        source=ProviderUsageSource.CODEX_APP_SERVER_PROVIDER_REPORTED,
        completeness=ProviderUsageCompleteness.COMPLETE,
        counters=ProviderUsageCounters(
            input_tokens=input_tokens,
            cache_read_input_tokens=cache_read_tokens,
            cache_write_input_tokens=0,
            output_tokens=output_tokens,
            reasoning_output_tokens=reasoning_tokens,
            provider_total_tokens=reported_total or None,
        ),
        observed_at_utc=observed_at_utc,
        returned_model_id=OPENAI_CODEX_PROVIDER_MODEL_ID,
    )


def build_subscription_included_cost() -> ProviderCostAccounting:
    """Return the fixed subscription-included cost record without live lookup."""

    return ProviderCostAccounting(
        status=ProviderCostStatus.INCLUDED,
        source=ProviderCostSource.SUBSCRIPTION_INCLUDED,
        amount_usd=Decimal("0"),
    )


def build_timeout_accounting(
    *,
    started_at_utc: datetime,
    completed_at_utc: datetime,
    outcome: ProviderAccountingOutcome,
    timeout_stage: ProviderTimeoutStage | None = None,
    budget: ProviderTimeoutBudget | None = None,
) -> ProviderTimeoutAccounting:
    """Build deterministic local timeout accounting from injected timestamps."""

    started_at_utc = _utc(started_at_utc)
    completed_at_utc = _utc(completed_at_utc)
    elapsed_ms = int((completed_at_utc - started_at_utc).total_seconds() * 1000)
    if elapsed_ms < 0:
        raise ProviderAccountingError(
            code="negative_elapsed_time",
            validation_category="timeout",
        )
    timed_out = outcome is ProviderAccountingOutcome.TIMED_OUT
    return ProviderTimeoutAccounting(
        outcome=outcome,
        disposition=ProviderTimeoutDisposition.TIMED_OUT
        if timed_out
        else ProviderTimeoutDisposition.WITHIN_BUDGET,
        budget=budget or ProviderTimeoutBudget(),
        started_at_utc=started_at_utc,
        completed_at_utc=completed_at_utc,
        elapsed_ms=elapsed_ms,
        timed_out=timed_out,
        timeout_stage=timeout_stage,
    )


def create_provider_accounting_record(
    *,
    usage_record_id: str,
    request_id: str,
    runtime_id: str,
    correlation_id: str,
    created_at_utc: datetime,
    usage: ProviderUsageEvidence,
    timeout: ProviderTimeoutAccounting,
    cost: ProviderCostAccounting | None = None,
) -> ProviderAccountingRecord:
    """Create one immutable single-request accounting record."""

    return ProviderAccountingRecord(
        usage_record_id=usage_record_id,
        request_id=request_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        created_at_utc=_utc(created_at_utc),
        usage=usage,
        cost=cost or build_subscription_included_cost(),
        timeout=timeout,
    )


def validate_worker_result_accounting_link(
    *,
    record: ProviderAccountingRecord,
    worker_result: BoundedProviderWorkerResult,
) -> ProviderAccountingWorkerResultLink:
    """Validate that a worker result references exactly this usage record."""

    expected = {
        "usage_record_id": record.usage_record_id,
        "request_id": record.request_id,
        "runtime_id": record.runtime_id,
        "correlation_id": record.correlation_id,
    }
    observed = {
        "usage_record_id": worker_result.usage_record_id,
        "request_id": worker_result.request_id,
        "runtime_id": worker_result.runtime_id,
        "correlation_id": worker_result.correlation_id,
    }
    for field_name, expected_value in expected.items():
        if observed[field_name] != expected_value:
            raise ProviderAccountingError(
                code="worker_result_accounting_mismatch",
                usage_record_id=record.usage_record_id,
                request_id=record.request_id,
                validation_category=field_name,
            )
    return ProviderAccountingWorkerResultLink(
        usage_record_id=record.usage_record_id,
        request_id=record.request_id,
        runtime_id=record.runtime_id,
        correlation_id=record.correlation_id,
        worker_result_state=worker_result.state.value,
    )


__all__ = [
    "ProviderAccountingError",
    "build_subscription_included_cost",
    "build_timeout_accounting",
    "create_provider_accounting_record",
    "normalize_codex_app_server_usage",
    "normalize_codex_responses_usage",
    "validate_worker_result_accounting_link",
]
