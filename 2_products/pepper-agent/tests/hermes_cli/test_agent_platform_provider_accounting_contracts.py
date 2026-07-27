from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_accounting as pa


SOURCE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_accounting"
)

EXPECTED_EXPORTS = [
    "PROVIDER_ACCOUNTING_SCHEMA_VERSION",
    "OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID",
    "OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID",
    "OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID",
    "OPENAI_CODEX_PROVIDER_MODEL_ID",
    "OPENAI_CODEX_BILLING_MODE",
    "ProviderUsageSource",
    "ProviderUsageCompleteness",
    "ProviderCostStatus",
    "ProviderCostSource",
    "ProviderTimeoutStage",
    "ProviderAccountingOutcome",
    "ProviderTimeoutDisposition",
    "ProviderAccountingLinkState",
    "ProviderAccountingPolicy",
    "ProviderUsageCounters",
    "ProviderUsageEvidence",
    "ProviderCostAccounting",
    "ProviderTimeoutBudget",
    "ProviderTimeoutAccounting",
    "ProviderAccountingRecord",
    "ProviderAccountingWorkerResultLink",
    "ProviderAccountingError",
    "normalize_codex_responses_usage",
    "normalize_codex_app_server_usage",
    "build_subscription_included_cost",
    "build_timeout_accounting",
    "create_provider_accounting_record",
    "validate_worker_result_accounting_link",
]
NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def usage_evidence() -> pa.ProviderUsageEvidence:
    return pa.ProviderUsageEvidence(
        source=pa.ProviderUsageSource.CODEX_RESPONSES_PROVIDER_REPORTED,
        completeness=pa.ProviderUsageCompleteness.COMPLETE,
        counters=pa.ProviderUsageCounters(
            input_tokens=10,
            cache_read_input_tokens=2,
            output_tokens=3,
            provider_total_tokens=15,
        ),
        observed_at_utc=NOW,
        provider_response_id="resp.contract",
        finish_reason="completed",
    )


def timeout_evidence() -> pa.ProviderTimeoutAccounting:
    return pa.build_timeout_accounting(
        started_at_utc=NOW,
        completed_at_utc=NOW + timedelta(milliseconds=250),
        outcome=pa.ProviderAccountingOutcome.COMPLETED,
    )


def test_root_exports_exact_authorized_public_api_without_internal_aliases() -> None:
    assert pa.__all__ == EXPECTED_EXPORTS
    for name in EXPECTED_EXPORTS:
        assert hasattr(pa, name)
    for forbidden in (
        "_coerce_usage_int",
        "BoundedProviderWorkerResult",
        "estimate_usage_cost",
        "fetch_account_usage",
    ):
        assert forbidden not in pa.__all__
        assert not hasattr(pa, forbidden)


def test_schema_enum_and_policy_values_are_exact() -> None:
    assert pa.PROVIDER_ACCOUNTING_SCHEMA_VERSION == 1
    assert pa.OPENAI_CODEX_PROVIDER_ACCOUNTING_POLICY_ID == (
        "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert [member.value for member in pa.ProviderUsageSource] == [
        "codex_responses_provider_reported",
        "codex_app_server_provider_reported",
        "provider_omitted",
    ]
    assert [member.value for member in pa.ProviderCostStatus] == [
        "included",
        "unavailable",
    ]
    assert [member.value for member in pa.ProviderTimeoutStage] == [
        "connection",
        "response_header",
        "complete_inference",
        "cancellation",
        "worker_shutdown",
    ]

    policy = pa.ProviderAccountingPolicy()
    assert policy.provider_runtime_profile_id == (
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert policy.worker_profile_id == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert policy.model_id == "gpt-5.5"
    assert policy.billing_mode == "subscription_included"
    assert policy.maximum_provider_calls_per_record == 1
    assert policy.provider_billing_api_allowed is False
    assert policy.pricing_metadata_lookup_allowed is False
    assert policy.usage_api_allowed is False
    assert policy.raw_provider_response_allowed is False


@pytest.mark.parametrize(
    "model_cls",
    (
        pa.ProviderAccountingPolicy,
        pa.ProviderUsageCounters,
        pa.ProviderCostAccounting,
        pa.ProviderTimeoutBudget,
    ),
)
def test_public_contracts_are_immutable_and_reject_extra_fields(
    model_cls: type,
) -> None:
    instance = model_cls()
    with pytest.raises(ValidationError):
        model_cls(**(instance.model_dump(mode="python") | {"unexpected": "field"}))
    with pytest.raises(ValidationError):
        model_cls(schema_version=2)


def test_usage_cost_timeout_and_record_contract_invariants() -> None:
    usage = usage_evidence()
    cost = pa.build_subscription_included_cost()
    timeout = timeout_evidence()
    record = pa.create_provider_accounting_record(
        usage_record_id="usage.contract",
        request_id="request.contract",
        runtime_id="runtime.contract",
        correlation_id="corr.contract",
        created_at_utc=NOW,
        usage=usage,
        cost=cost,
        timeout=timeout,
    )

    assert usage.counters.prompt_tokens == 12
    assert usage.counters.canonical_total_tokens == 15
    assert cost.amount_usd == 0
    assert cost.status is pa.ProviderCostStatus.INCLUDED
    assert cost.exact_marginal_request_cost_available is False
    assert timeout.elapsed_ms == 250
    assert timeout.timed_out is False
    assert record.policy.usage_record_id_required_on_worker_result is True
    assert record.raw_request_allowed is False
    assert record.raw_response_allowed is False


def test_contracts_reject_unsafe_or_inconsistent_evidence() -> None:
    with pytest.raises(ValidationError):
        pa.ProviderUsageCounters(input_tokens=-1)
    with pytest.raises(ValidationError):
        pa.ProviderUsageCounters(input_tokens=10, provider_total_tokens=9)
    with pytest.raises(ValidationError):
        pa.ProviderUsageEvidence(
            source=pa.ProviderUsageSource.CODEX_RESPONSES_PROVIDER_REPORTED,
            completeness=pa.ProviderUsageCompleteness.MISSING,
            observed_at_utc=NOW,
        )
    with pytest.raises(ValidationError):
        pa.ProviderUsageEvidence(
            source=pa.ProviderUsageSource.PROVIDER_OMITTED,
            completeness=pa.ProviderUsageCompleteness.MISSING,
            observed_at_utc=datetime(2026, 1, 1),
        )
    with pytest.raises(ValidationError):
        pa.ProviderCostAccounting(amount_usd=1)
    with pytest.raises(ValidationError):
        pa.ProviderTimeoutAccounting(
            outcome=pa.ProviderAccountingOutcome.COMPLETED,
            disposition=pa.ProviderTimeoutDisposition.TIMED_OUT,
            started_at_utc=NOW,
            completed_at_utc=NOW,
            elapsed_ms=0,
            timed_out=True,
            timeout_stage=pa.ProviderTimeoutStage.COMPLETE_INFERENCE,
        )


def test_provider_accounting_source_has_no_operational_authority() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in sorted(SOURCE_ROOT.glob("*.py"))
    )
    for forbidden in (
        "httpx",
        "requests",
        "openai.",
        "subprocess",
        "socket.",
        "os.environ",
        "getenv",
        "auth.json",
        "usage_pricing",
        "account_usage",
        "fetch_model_metadata",
        "fetch_endpoint_model_metadata",
        "responses.create",
        "models.list",
        ".write_text",
        ".write_bytes",
        "open(",
        "sqlite",
    ):
        assert forbidden not in source
