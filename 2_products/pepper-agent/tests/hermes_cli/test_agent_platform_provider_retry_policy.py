from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_accounting as pa
from hermes_cli.agent_platform import provider_failure_policy as fp
from hermes_cli.agent_platform.provider_accounting.enums import (
    ProviderAccountingOutcome,
    ProviderTimeoutStage,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)
SOURCE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_failure_policy"
)


TIMEOUT_STAGE_BY_CATEGORY = {
    fp.ProviderFailureCategory.CONNECTION_TIMEOUT: ProviderTimeoutStage.CONNECTION,
    fp.ProviderFailureCategory.RESPONSE_HEADER_TIMEOUT: (
        ProviderTimeoutStage.RESPONSE_HEADER
    ),
    fp.ProviderFailureCategory.COMPLETE_INFERENCE_TIMEOUT: (
        ProviderTimeoutStage.COMPLETE_INFERENCE
    ),
    fp.ProviderFailureCategory.CANCELLATION_TIMEOUT: ProviderTimeoutStage.CANCELLATION,
    fp.ProviderFailureCategory.WORKER_SHUTDOWN_TIMEOUT: (
        ProviderTimeoutStage.WORKER_SHUTDOWN
    ),
}


def outcome_for(category: fp.ProviderFailureCategory) -> ProviderAccountingOutcome:
    if category is fp.ProviderFailureCategory.CANCELLED_BY_OWNER:
        return ProviderAccountingOutcome.CANCELLED
    if category in TIMEOUT_STAGE_BY_CATEGORY:
        return ProviderAccountingOutcome.TIMED_OUT
    return ProviderAccountingOutcome.FAILED


def record_for(
    category: fp.ProviderFailureCategory,
    *,
    request_id: str = "request.retry",
    runtime_id: str = "runtime.retry",
    correlation_id: str = "corr.retry",
    usage_record_id: str | None = "usage.retry",
    provider_dispatch_occurred: bool = True,
    retry_after_ms: int | None = None,
) -> fp.ProviderFailureRecord:
    return fp.ProviderFailureRecord(
        failure_record_id=fp.build_failure_record_id(
            runtime_id=runtime_id,
            correlation_id=correlation_id,
            request_id=request_id,
            category=category,
        ),
        request_id=request_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        category=category,
        stage=fp.ProviderFailureStage.CONNECTION
        if category is fp.ProviderFailureCategory.CONNECTION_TIMEOUT
        else fp.ProviderFailureStage.DISPATCH,
        origin=fp.ProviderFailureOrigin.HTTP_RESPONSE,
        provider_dispatch_occurred=provider_dispatch_occurred,
        provider_dispatch_count=1 if provider_dispatch_occurred else 0,
        accounting_outcome=outcome_for(category),
        accounting_timeout_stage=TIMEOUT_STAGE_BY_CATEGORY.get(category),
        usage_record_id=usage_record_id if provider_dispatch_occurred else None,
        retry_after_ms=retry_after_ms,
        retry_delay_source=fp.ProviderRetryDelaySource.PROVIDER_RETRY_AFTER
        if retry_after_ms is not None
        else fp.ProviderRetryDelaySource.NONE,
        safe_summary=fp.resolve_safe_failure_summary(category),
    )


def accounting_record(
    *,
    outcome: ProviderAccountingOutcome = ProviderAccountingOutcome.FAILED,
    timeout_stage: ProviderTimeoutStage | None = None,
    request_id: str = "request.retry",
    runtime_id: str = "runtime.retry",
    correlation_id: str = "corr.retry",
    usage_record_id: str = "usage.retry",
) -> pa.ProviderAccountingRecord:
    usage = pa.normalize_codex_responses_usage(
        {"input_tokens": 1, "output_tokens": 1},
        observed_at_utc=NOW,
    )
    timeout = pa.build_timeout_accounting(
        started_at_utc=NOW,
        completed_at_utc=NOW + timedelta(milliseconds=1),
        outcome=outcome,
        timeout_stage=timeout_stage,
    )
    return pa.create_provider_accounting_record(
        usage_record_id=usage_record_id,
        request_id=request_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        created_at_utc=NOW,
        usage=usage,
        timeout=timeout,
    )


def test_retry_decision_never_allows_automatic_retry_for_any_category() -> None:
    for category in fp.ProviderFailureCategory:
        record = record_for(category)
        decision = fp.build_provider_retry_decision(record)

        assert decision.automatic_retry_allowed is False
        assert decision.automatic_retry_attempts == 0
        assert decision.same_request_retry_allowed is False
        assert decision.same_worker_retry_allowed is False
        assert decision.same_request_id_reuse_allowed is False
        assert decision.same_usage_record_id_reuse_allowed is False
        assert decision.credential_rotation_allowed is False
        assert decision.automatic_refresh_allowed is False
        assert decision.model_fallback_allowed is False
        assert decision.endpoint_fallback_allowed is False


def test_manual_resubmission_requires_new_identities_and_worker_lifecycle() -> None:
    record = record_for(fp.ProviderFailureCategory.RATE_LIMIT)
    decision = fp.build_provider_retry_decision(record)

    assert decision.disposition is (
        fp.ProviderRetryDisposition.NEW_REQUEST_AFTER_EXTERNAL_CONDITION
    )
    assert decision.new_request_required is True
    assert decision.new_worker_lifecycle_required is True
    assert decision.new_usage_record_required is True
    assert decision.new_credential_lease_required is True
    assert decision.same_request_retry_allowed is False
    assert decision.same_worker_retry_allowed is False


def test_never_disposition_does_not_authorize_resubmission() -> None:
    decision = fp.build_provider_retry_decision(
        record_for(fp.ProviderFailureCategory.CONTENT_POLICY)
    )

    assert decision.disposition is fp.ProviderRetryDisposition.NEVER
    assert decision.new_request_required is False
    assert decision.new_worker_lifecycle_required is False
    assert decision.new_usage_record_required is False
    assert decision.new_credential_lease_required is False


def test_retry_after_metadata_is_advisory_only_and_range_checked() -> None:
    signal = fp.ProviderFailureSignal(
        origin=fp.ProviderFailureOrigin.HTTP_RESPONSE,
        stage=fp.ProviderFailureStage.DISPATCH,
        HTTP_status=429,
        provider_message="too many requests",
        provider_dispatch_occurred=True,
        provider_response_id_present=True,
        retry_after_ms=1000,
        retry_delay_source=fp.ProviderRetryDelaySource.PROVIDER_RETRY_AFTER,
    )
    record = fp.build_provider_failure_record(
        request_id="request.retry_after",
        runtime_id="runtime.retry_after",
        correlation_id="corr.retry_after",
        signal=signal,
        usage_record_id="usage.retry_after",
    )
    decision = fp.build_provider_retry_decision(record)

    assert record.retry_after_ms == 1000
    assert record.retry_delay_source is fp.ProviderRetryDelaySource.PROVIDER_RETRY_AFTER
    assert decision.retry_after_ms == 1000
    assert decision.delay_is_advisory_only is True
    assert decision.automatic_retry_allowed is False

    with pytest.raises(ValidationError):
        fp.ProviderFailureSignal(
            origin=fp.ProviderFailureOrigin.HTTP_RESPONSE,
            stage=fp.ProviderFailureStage.DISPATCH,
            HTTP_status=429,
            provider_dispatch_occurred=True,
            retry_after_ms=fp.MAXIMUM_RETRY_AFTER_MS + 1,
            retry_delay_source=fp.ProviderRetryDelaySource.PROVIDER_RETRY_AFTER,
        )
    with pytest.raises(ValidationError):
        fp.ProviderFailureSignal(
            origin=fp.ProviderFailureOrigin.HTTP_RESPONSE,
            stage=fp.ProviderFailureStage.DISPATCH,
            HTTP_status=429,
            provider_dispatch_occurred=True,
            retry_after_ms=1000,
        )


def test_no_sleep_or_backoff_execution_authority() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in sorted(SOURCE_ROOT.glob("*.py"))
    )
    for forbidden in ("sleep(", "asyncio.sleep", "time.sleep", "backoff"):
        assert forbidden not in source


def test_cleanup_flags_project_without_execution() -> None:
    decision = fp.build_provider_retry_decision(
        record_for(fp.ProviderFailureCategory.PROVIDER_SERVER_ERROR),
        temporary_credential_lease_exists=True,
        provider_stream_exists=True,
        temporary_projected_hermes_home_present=True,
    )

    assert decision.release_temporary_credential_lease is True
    assert decision.close_provider_stream is True
    assert decision.stop_owned_worker is True
    assert decision.remove_temporary_projected_hermes_home is True
    assert decision.preserve_durable_credential is True
    assert decision.preserve_secret_free_accounting is True
    assert decision.preserve_secret_free_failure_record is True
    assert decision.preserve_partial_output is False
    assert decision.preserve_raw_provider_response is False
    assert decision.preserve_headers is False


def test_failure_to_accounting_outcome_mapping_for_all_categories() -> None:
    for category in fp.ProviderFailureCategory:
        record = record_for(category)
        projection = fp.project_failure_to_accounting(record)

        assert projection.accounting_outcome is outcome_for(category)
        assert projection.accounting_timeout_stage is TIMEOUT_STAGE_BY_CATEGORY.get(
            category
        )
        assert projection.provider_dispatch_count == 1


def test_failure_accounting_link_matches_all_required_dimensions() -> None:
    failure = record_for(fp.ProviderFailureCategory.RATE_LIMIT)
    accounting = accounting_record()

    link = fp.validate_failure_accounting_link(
        failure_record=failure,
        accounting_record=accounting,
    )

    assert link.link_state is fp.ProviderFailureAccountingLinkState.MATCHED
    assert link.usage_record_id_matched is True
    assert link.request_id_matched is True
    assert link.runtime_id_matched is True
    assert link.correlation_id_matched is True
    assert link.accounting_outcome_matched is True
    assert link.timeout_stage_matched is True
    assert link.provider_dispatch_count_matched is True


def test_failure_accounting_link_reports_missing_accounting_after_dispatch() -> None:
    link = fp.validate_failure_accounting_link(
        failure_record=record_for(fp.ProviderFailureCategory.RATE_LIMIT),
        accounting_record=None,
    )

    assert link.link_state is fp.ProviderFailureAccountingLinkState.MISSING
    assert link.provider_dispatch_count_matched is False


def test_pre_dispatch_failure_without_accounting_is_matched_without_accounting() -> (
    None
):
    failure = record_for(
        fp.ProviderFailureCategory.REQUEST_INVALID,
        provider_dispatch_occurred=False,
        usage_record_id=None,
    )
    link = fp.validate_failure_accounting_link(
        failure_record=failure,
        accounting_record=None,
    )

    assert link.link_state is (
        fp.ProviderFailureAccountingLinkState.MATCHED_WITHOUT_ACCOUNTING
    )
    assert link.provider_dispatch_count_matched is True


def test_failure_accounting_link_reports_identity_outcome_and_timeout_mismatches() -> (
    None
):
    failure = record_for(
        fp.ProviderFailureCategory.CONNECTION_TIMEOUT,
        usage_record_id="usage.retry",
    )
    accounting = accounting_record(
        outcome=ProviderAccountingOutcome.FAILED,
        request_id="request.other",
        usage_record_id="usage.other",
    )

    link = fp.validate_failure_accounting_link(
        failure_record=failure,
        accounting_record=accounting,
    )

    assert link.link_state is fp.ProviderFailureAccountingLinkState.MISMATCHED
    assert link.usage_record_id_matched is False
    assert link.request_id_matched is False
    assert link.accounting_outcome_matched is False
    assert link.timeout_stage_matched is False


def test_accounting_integrity_failures_never_trigger_provider_retry() -> None:
    record = record_for(fp.ProviderFailureCategory.ACCOUNTING_INVALID)
    decision = fp.build_provider_retry_decision(record)

    assert record.accounting_outcome is ProviderAccountingOutcome.FAILED
    assert decision.disposition is fp.ProviderRetryDisposition.NEVER
    assert decision.automatic_retry_allowed is False
    assert decision.new_request_required is False
