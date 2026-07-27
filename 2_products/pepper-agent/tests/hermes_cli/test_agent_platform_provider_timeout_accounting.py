from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_accounting as pa
from hermes_cli.agent_platform import provider_worker as pw


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_usage() -> pa.ProviderUsageEvidence:
    return pa.normalize_codex_responses_usage(
        {"input_tokens": 10, "output_tokens": 5},
        observed_at_utc=NOW,
        provider_response_id="resp.timeout",
    )


def make_record(
    *,
    usage_record_id: str = "usage.timeout",
    request_id: str = "request.timeout",
    timeout: pa.ProviderTimeoutAccounting | None = None,
) -> pa.ProviderAccountingRecord:
    return pa.create_provider_accounting_record(
        usage_record_id=usage_record_id,
        request_id=request_id,
        runtime_id="runtime.timeout",
        correlation_id="corr.timeout",
        created_at_utc=NOW,
        usage=make_usage(),
        timeout=timeout
        or pa.build_timeout_accounting(
            started_at_utc=NOW,
            completed_at_utc=NOW + timedelta(milliseconds=100),
            outcome=pa.ProviderAccountingOutcome.COMPLETED,
        ),
    )


def test_timeout_accounting_records_success_and_timeout_deterministically() -> None:
    completed = pa.build_timeout_accounting(
        started_at_utc=NOW,
        completed_at_utc=NOW + timedelta(milliseconds=999),
        outcome=pa.ProviderAccountingOutcome.COMPLETED,
    )
    timed_out = pa.build_timeout_accounting(
        started_at_utc=NOW,
        completed_at_utc=NOW + timedelta(milliseconds=120001),
        outcome=pa.ProviderAccountingOutcome.TIMED_OUT,
        timeout_stage=pa.ProviderTimeoutStage.COMPLETE_INFERENCE,
    )

    assert completed.elapsed_ms == 999
    assert completed.disposition is pa.ProviderTimeoutDisposition.WITHIN_BUDGET
    assert completed.timed_out is False
    assert completed.timeout_stage is None
    assert timed_out.elapsed_ms == 120001
    assert timed_out.disposition is pa.ProviderTimeoutDisposition.TIMED_OUT
    assert timed_out.timed_out is True
    assert timed_out.timeout_stage is pa.ProviderTimeoutStage.COMPLETE_INFERENCE
    assert timed_out.budget.complete_inference_timeout_ms == 120_000


def test_timeout_accounting_rejects_inconsistent_or_unsafe_time_evidence() -> None:
    with pytest.raises(pa.ProviderAccountingError) as timestamp_error:
        pa.build_timeout_accounting(
            started_at_utc=datetime(2026, 1, 1),
            completed_at_utc=NOW,
            outcome=pa.ProviderAccountingOutcome.COMPLETED,
        )
    assert timestamp_error.value.code == "timestamp_not_utc"

    with pytest.raises(pa.ProviderAccountingError) as elapsed_error:
        pa.build_timeout_accounting(
            started_at_utc=NOW,
            completed_at_utc=NOW - timedelta(milliseconds=1),
            outcome=pa.ProviderAccountingOutcome.COMPLETED,
        )
    assert elapsed_error.value.code == "negative_elapsed_time"

    with pytest.raises(ValidationError):
        pa.ProviderTimeoutAccounting(
            outcome=pa.ProviderAccountingOutcome.TIMED_OUT,
            disposition=pa.ProviderTimeoutDisposition.TIMED_OUT,
            started_at_utc=NOW,
            completed_at_utc=NOW,
            elapsed_ms=0,
            timed_out=True,
        )
    with pytest.raises(ValidationError):
        pa.ProviderTimeoutAccounting(
            outcome=pa.ProviderAccountingOutcome.COMPLETED,
            disposition=pa.ProviderTimeoutDisposition.WITHIN_BUDGET,
            started_at_utc=NOW,
            completed_at_utc=NOW + timedelta(milliseconds=5),
            elapsed_ms=6,
            timed_out=False,
        )


def test_accounting_record_links_to_worker_result_usage_record_id() -> None:
    record = make_record()
    result = pw.BoundedProviderWorkerResult(
        request_id="request.timeout",
        runtime_id="runtime.timeout",
        correlation_id="corr.timeout",
        state=pw.ProviderWorkerResultState.COMPLETED,
        completed_at_utc=NOW + timedelta(milliseconds=100),
        output_text="synthetic bounded result",
        usage_record_id="usage.timeout",
    )

    link = pa.validate_worker_result_accounting_link(
        record=record,
        worker_result=result,
    )

    assert link.usage_record_id == "usage.timeout"
    assert link.request_id == "request.timeout"
    assert link.worker_result_state == "completed"
    assert link.link_state is pa.ProviderAccountingLinkState.MATCHED


def test_worker_result_accounting_link_rejects_mismatches_without_raw_output() -> None:
    record = make_record()
    result = pw.BoundedProviderWorkerResult(
        request_id="request.timeout",
        runtime_id="runtime.timeout",
        correlation_id="corr.timeout",
        state=pw.ProviderWorkerResultState.COMPLETED,
        completed_at_utc=NOW + timedelta(milliseconds=100),
        output_text="forbidden-sensitive-result-body",
        usage_record_id="usage.other",
    )

    with pytest.raises(pa.ProviderAccountingError) as mismatch:
        pa.validate_worker_result_accounting_link(record=record, worker_result=result)

    assert mismatch.value.code == "worker_result_accounting_mismatch"
    assert mismatch.value.validation_category == "usage_record_id"
    assert "forbidden-sensitive-result-body" not in str(mismatch.value)


def test_timed_out_records_preserve_usage_and_subscription_cost_posture() -> None:
    timeout = pa.build_timeout_accounting(
        started_at_utc=NOW,
        completed_at_utc=NOW + timedelta(milliseconds=120001),
        outcome=pa.ProviderAccountingOutcome.TIMED_OUT,
        timeout_stage=pa.ProviderTimeoutStage.COMPLETE_INFERENCE,
    )
    record = make_record(usage_record_id="usage.timedout", timeout=timeout)

    assert record.timeout.outcome is pa.ProviderAccountingOutcome.TIMED_OUT
    assert record.timeout.timed_out is True
    assert record.usage.counters.canonical_total_tokens == 15
    assert record.cost.status is pa.ProviderCostStatus.INCLUDED
    assert record.cost.provider_billing_api_called is False
