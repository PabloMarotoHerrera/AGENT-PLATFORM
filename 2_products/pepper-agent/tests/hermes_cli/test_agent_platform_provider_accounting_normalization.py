from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_accounting as pa


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_codex_responses_usage_normalization_subtracts_cache_and_preserves_reasoning() -> (
    None
):
    usage = SimpleNamespace(
        input_tokens=1200,
        output_tokens=200,
        input_tokens_details=SimpleNamespace(
            cached_tokens=300,
            cache_creation_tokens=50,
        ),
        output_tokens_details=SimpleNamespace(reasoning_tokens=25),
    )

    evidence = pa.normalize_codex_responses_usage(
        usage,
        observed_at_utc=NOW,
        provider_response_id="resp.normalization",
        finish_reason="completed",
    )

    assert evidence.source is pa.ProviderUsageSource.CODEX_RESPONSES_PROVIDER_REPORTED
    assert evidence.completeness is pa.ProviderUsageCompleteness.COMPLETE
    assert evidence.provider_response_id == "resp.normalization"
    assert evidence.returned_model_id == "gpt-5.5"
    assert evidence.finish_reason == "completed"
    assert evidence.counters.input_tokens == 850
    assert evidence.counters.cache_read_input_tokens == 300
    assert evidence.counters.cache_write_input_tokens == 50
    assert evidence.counters.output_tokens == 200
    assert evidence.counters.reasoning_output_tokens == 25
    assert evidence.counters.provider_total_tokens == 1400
    assert evidence.counters.prompt_tokens == 1200
    assert evidence.counters.canonical_total_tokens == 1400


def test_codex_app_server_usage_normalization_maps_camel_case_payload() -> None:
    evidence = pa.normalize_codex_app_server_usage(
        {
            "inputTokens": "100",
            "cachedInputTokens": 20.9,
            "outputTokens": 30,
            "reasoningOutputTokens": 5,
            "totalTokens": 150,
        },
        observed_at_utc=NOW,
    )

    assert evidence.source is pa.ProviderUsageSource.CODEX_APP_SERVER_PROVIDER_REPORTED
    assert evidence.counters.input_tokens == 100
    assert evidence.counters.cache_read_input_tokens == 20
    assert evidence.counters.cache_write_input_tokens == 0
    assert evidence.counters.output_tokens == 30
    assert evidence.counters.reasoning_output_tokens == 5
    assert evidence.counters.provider_total_tokens == 150
    assert evidence.counters.canonical_total_tokens == 150


def test_missing_or_invalid_usage_is_secret_free_and_non_negative() -> None:
    missing = pa.normalize_codex_responses_usage(None, observed_at_utc=NOW)
    assert missing.source is pa.ProviderUsageSource.PROVIDER_OMITTED
    assert missing.completeness is pa.ProviderUsageCompleteness.MISSING
    assert missing.returned_model_id is None
    assert missing.counters.canonical_total_tokens == 0

    clamped = pa.normalize_codex_responses_usage(
        {
            "input_tokens": -10,
            "output_tokens": True,
            "input_tokens_details": {"cached_tokens": "bad"},
            "output_tokens_details": {"reasoning_tokens": "7"},
        },
        observed_at_utc=NOW,
    )
    assert clamped.counters.input_tokens == 0
    assert clamped.counters.output_tokens == 0
    assert clamped.counters.cache_read_input_tokens == 0
    assert clamped.counters.reasoning_output_tokens == 7


def test_subscription_cost_accounting_uses_no_pricing_lookup_or_billing_api() -> None:
    cost = pa.build_subscription_included_cost()

    assert cost.billing_mode == "subscription_included"
    assert cost.status is pa.ProviderCostStatus.INCLUDED
    assert cost.source is pa.ProviderCostSource.SUBSCRIPTION_INCLUDED
    assert cost.amount_usd == 0
    assert cost.exact_marginal_request_cost_available is False
    assert cost.estimated_pricing_lookup_performed is False
    assert cost.provider_billing_api_called is False
    assert cost.usage_api_called is False


def test_normalization_rejects_naive_timestamps_and_unsafe_text() -> None:
    with pytest.raises(pa.ProviderAccountingError) as timestamp_error:
        pa.normalize_codex_responses_usage({}, observed_at_utc=datetime(2026, 1, 1))
    assert timestamp_error.value.code == "timestamp_not_utc"

    with pytest.raises(ValidationError):
        pa.normalize_codex_responses_usage(
            {"input_tokens": 1, "output_tokens": 1},
            observed_at_utc=NOW,
            finish_reason="line\nbreak",
        )
