from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from hermes_cli.agent_platform import provider_accounting as pa
from hermes_cli.agent_platform import provider_failure_policy as fp
from hermes_cli.agent_platform import provider_worker as pw
from hermes_cli.agent_platform import provider_worker_gate as gate
from hermes_cli.agent_platform.provider_worker_gate import (
    single_dispatch as gate_dispatch,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    MAXIMUM_OUTPUT_UTF8_BYTES,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


class ClosingEventStream(list):
    def __init__(self, events: list[dict[str, Any]]):
        super().__init__(events)
        self.closed = False

    def close(self) -> None:
        self.closed = True


class RecordingResponses:
    def __init__(
        self,
        events: list[dict[str, Any]] | None = None,
        exc: Exception | None = None,
    ) -> None:
        self.events = events or []
        self.exc = exc
        self.create_calls: list[dict[str, Any]] = []
        self.last_stream: ClosingEventStream | None = None

    def create(self, **kwargs: Any) -> ClosingEventStream:
        self.create_calls.append(kwargs)
        if self.exc is not None:
            raise self.exc
        self.last_stream = ClosingEventStream(self.events)
        return self.last_stream


class RecordingClient:
    def __init__(self, responses: RecordingResponses) -> None:
        self.responses = responses


class RaisingEventStream:
    def __init__(self) -> None:
        self.closed = False

    def __iter__(self):
        yield {"type": "response.output_text.delta", "delta": "PEPPER"}
        raise RuntimeError("synthetic stream failure")

    def close(self) -> None:
        self.closed = True


class RaisingStreamResponses:
    def __init__(self) -> None:
        self.create_calls: list[dict[str, Any]] = []
        self.last_stream: RaisingEventStream | None = None

    def create(self, **kwargs: Any) -> RaisingEventStream:
        self.create_calls.append(kwargs)
        self.last_stream = RaisingEventStream()
        return self.last_stream


class HTTPFailure(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class ConnectFailure(Exception):
    pass


def make_worker_request() -> pw.BoundedProviderWorkerRequest:
    return pw.BoundedProviderWorkerRequest(
        request_id="request.single",
        runtime_id="runtime.single",
        correlation_id="corr.single",
        requested_by="p15.7.single-test",
        submitted_at_utc=NOW,
        user_content="Reply with exactly: PEPPER_P15_7_OK",
    )


def make_gate_request() -> gate.ProviderWorkerGateRequest:
    return gate.build_provider_worker_gate_request(
        make_worker_request(),
        requested_at_utc=NOW,
        usage_record_id="usage.single",
    )


def test_single_dispatch_success_calls_responses_create_once_and_links_accounting() -> (
    None
):
    events = [
        {"type": "response.output_text.delta", "delta": "PEPPER_P15_7_OK"},
        {
            "type": "response.completed",
            "response": {
                "id": "resp.single",
                "status": "completed",
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 2,
                    "total_tokens": 12,
                },
            },
        },
    ]
    responses = RecordingResponses(events)
    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    create_kwargs = responses.create_calls[0]
    assert create_kwargs == {
        "model": "gpt-5.5",
        "instructions": gate.OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION,
        "input": [{"role": "user", "content": "Reply with exactly: PEPPER_P15_7_OK"}],
        "store": False,
        "reasoning": {"effort": "medium", "summary": "auto"},
        "include": ["reasoning.encrypted_content"],
        "prompt_cache_key": "pck_70158de7be5d5037d4450889",
        "stream": True,
    }
    assert "max_output_tokens" not in create_kwargs
    assert "tools" not in create_kwargs
    assert "tool_choice" not in create_kwargs
    assert "parallel_tool_calls" not in create_kwargs
    assert "service_tier" not in create_kwargs
    assert responses.last_stream is not None
    assert responses.last_stream.closed is True
    assert result.worker_result.state is pw.ProviderWorkerResultState.COMPLETED
    assert result.worker_result.output_text == "PEPPER_P15_7_OK"
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.dispatch_evidence.SDK_max_retries == 0
    assert result.dispatch_evidence.worker_retry_attempts == 0
    assert result.dispatch_evidence.worker_fallback_attempts == 0
    assert result.accounting_record is not None
    assert result.accounting_record.usage.counters.canonical_total_tokens == 12
    assert (
        result.accounting_record.timeout.outcome
        is pa.ProviderAccountingOutcome.COMPLETED
    )
    assert result.accounting_link is not None
    assert result.accounting_link.link_state is pa.ProviderAccountingLinkState.MATCHED
    assert result.failure_record is None


def test_single_dispatch_provider_failure_does_not_retry_or_fallback() -> None:
    responses = RecordingResponses(
        exc=HTTPFailure(429, "rate_limit", "too many requests")
    )
    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert result.worker_result.state is pw.ProviderWorkerResultState.FAILED
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.failure_record is not None
    assert result.failure_record.category is fp.ProviderFailureCategory.RATE_LIMIT
    assert result.failure_record.provider_dispatch_count == 1
    assert result.failure_retry_decision is not None
    assert result.failure_retry_decision.automatic_retry_allowed is False
    assert result.failure_retry_decision.automatic_retry_attempts == 0
    assert result.failure_retry_decision.same_worker_retry_allowed is False
    assert result.failure_retry_decision.model_fallback_allowed is False
    assert result.failure_retry_decision.endpoint_fallback_allowed is False
    assert result.accounting_record is not None
    assert (
        result.accounting_record.timeout.outcome is pa.ProviderAccountingOutcome.FAILED
    )
    assert result.failure_accounting_link is not None
    assert result.failure_accounting_link.link_state is (
        fp.ProviderFailureAccountingLinkState.MATCHED
    )


@pytest.mark.parametrize(
    "exc",
    [
        HTTPFailure(400, "invalid_request_error", "bad request"),
        ConnectFailure("connect failed"),
        TimeoutError("timed out"),
    ],
)
def test_single_dispatch_never_retries_after_request_or_transport_failure(
    exc: Exception,
) -> None:
    responses = RecordingResponses(exc=exc)

    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert result.worker_result.state is pw.ProviderWorkerResultState.FAILED
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.failure_retry_decision is not None
    assert result.failure_retry_decision.automatic_retry_attempts == 0
    assert result.failure_retry_decision.model_fallback_allowed is False
    assert result.failure_retry_decision.endpoint_fallback_allowed is False


def test_single_dispatch_pre_create_failure_is_preflight_zero_dispatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_before_create(
        _gate_request: gate.ProviderWorkerGateRequest,
    ) -> dict[str, Any]:
        raise ValueError("synthetic request construction failure")

    responses = RecordingResponses()
    monkeypatch.setattr(
        gate_dispatch,
        "build_codex_responses_create_kwargs",
        raise_before_create,
    )

    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 0
    assert result.dispatch_evidence.responses_create_call_count == 0
    assert result.diagnostics.provider_dispatches_for_attempt == 0
    assert result.diagnostics.failure_phase == "preflight"
    assert (
        result.diagnostics.local_failure_category
        == "local_request_construction_or_contract_failure"
    )
    assert result.diagnostics.safe_exception_class == "ValueError"
    assert result.failure_record is not None
    assert result.failure_record.stage is fp.ProviderFailureStage.PREFLIGHT
    assert result.failure_record.provider_dispatch_count == 0
    assert "dispatch_started" not in result.diagnostics.checkpoints


def test_single_dispatch_responses_create_exception_is_dispatch_count_one() -> None:
    responses = RecordingResponses(exc=TimeoutError("synthetic create failure"))

    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.diagnostics.provider_dispatches_for_attempt == 1
    assert result.diagnostics.failure_phase == "dispatch"
    assert result.diagnostics.safe_exception_class == "TimeoutError"
    assert result.failure_record is not None
    assert result.failure_record.stage is fp.ProviderFailureStage.DISPATCH
    assert result.failure_record.provider_dispatch_count == 1


def test_single_dispatch_stream_iterator_exception_is_stream_count_one() -> None:
    responses = RaisingStreamResponses()

    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert responses.last_stream is not None
    assert responses.last_stream.closed is True
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.diagnostics.provider_dispatches_for_attempt == 1
    assert result.diagnostics.failure_phase == "stream"
    assert result.failure_record is not None
    assert result.failure_record.stage is fp.ProviderFailureStage.STREAM
    assert result.failure_record.provider_dispatch_count == 1
    assert "event_stream_obtained" in result.diagnostics.checkpoints
    assert "stream_iteration_started" in result.diagnostics.checkpoints
    assert "first_event_observed" in result.diagnostics.checkpoints


def test_single_dispatch_accounting_failure_preserves_dispatch_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_normalize = gate_dispatch.normalize_codex_responses_usage

    def fail_only_success_usage(usage: Any, **kwargs: Any):
        if usage is not None:
            raise ValueError("synthetic accounting failure")
        return original_normalize(usage, **kwargs)

    responses = RecordingResponses([
        {"type": "response.output_text.delta", "delta": "PEPPER_P15_7_OK"},
        {
            "type": "response.completed",
            "response": {
                "id": "resp.accounting",
                "status": "completed",
                "usage": {"input_tokens": 10, "output_tokens": 2},
            },
        },
    ])
    monkeypatch.setattr(
        gate_dispatch,
        "normalize_codex_responses_usage",
        fail_only_success_usage,
    )

    result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(responses),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.diagnostics.provider_dispatches_for_attempt == 1
    assert result.diagnostics.failure_phase == "accounting"
    assert result.diagnostics.safe_exception_class == "ValueError"
    assert result.failure_record is not None
    assert (
        result.failure_record.category is fp.ProviderFailureCategory.ACCOUNTING_INVALID
    )
    assert result.failure_record.stage is fp.ProviderFailureStage.ACCOUNTING
    assert result.failure_record.provider_dispatch_count == 1
    assert "accounting_started" in result.diagnostics.checkpoints


def test_single_dispatch_rejects_previous_max_output_tokens_wire_shape() -> None:
    corrected = gate.build_codex_responses_create_kwargs(make_gate_request())
    previous_shape = dict(corrected)
    previous_shape["max_output_tokens"] = 64

    with pytest.raises(ValueError, match="max_output_tokens"):
        gate.assert_canonical_codex_backend_create_kwargs(previous_shape)

    accepted = gate.assert_canonical_codex_backend_create_kwargs(corrected)
    assert accepted is corrected
    assert accepted["store"] is False
    assert accepted["stream"] is True
    assert accepted["prompt_cache_key"].startswith("pck_")
    assert "max_output_tokens" not in accepted


def test_single_dispatch_matches_source_native_codex_backend_builder() -> None:
    from agent.transports.codex import ResponsesApiTransport

    source_native = ResponsesApiTransport().build_kwargs(
        "gpt-5.5",
        [{"role": "user", "content": "Reply with exactly: PEPPER_P15_7_OK"}],
        tools=None,
        instructions=gate.OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION,
        reasoning_config={"effort": "medium"},
        is_codex_backend=True,
        provider="openai-codex",
        base_url="https://chatgpt.com/backend-api/codex",
        max_tokens=64,
    )
    corrected = gate.build_codex_responses_create_kwargs(make_gate_request())

    assert corrected == {**source_native, "stream": True}
    assert "max_output_tokens" not in source_native


def test_single_dispatch_enforces_local_output_limit_and_exact_result() -> None:
    oversized = gate.OPENAI_CODEX_P15_7_EXPECTED_OUTPUT + (
        "x" * MAXIMUM_OUTPUT_UTF8_BYTES
    )
    oversized_responses = RecordingResponses([
        {"type": "response.output_text.delta", "delta": oversized},
        {
            "type": "response.completed",
            "response": {"id": "resp.oversized", "status": "completed"},
        },
    ])
    oversized_result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(oversized_responses),
        now=NOW,
    )
    assert len(oversized_responses.create_calls) == 1
    assert oversized_result.worker_result.state is pw.ProviderWorkerResultState.FAILED
    assert oversized_result.worker_result.output_text is None

    mismatch_responses = RecordingResponses([
        {"type": "response.output_text.delta", "delta": "PEPPER_P15_7_NOT_OK"},
        {
            "type": "response.completed",
            "response": {"id": "resp.mismatch", "status": "completed"},
        },
    ])
    mismatch_result = gate.run_openai_codex_single_dispatch(
        make_gate_request(),
        client=RecordingClient(mismatch_responses),
        now=NOW,
    )
    assert len(mismatch_responses.create_calls) == 1
    assert mismatch_result.worker_result.state is pw.ProviderWorkerResultState.FAILED
    assert mismatch_result.worker_result.output_text is None


def test_single_dispatch_source_uses_only_allowed_event_consumer() -> None:
    source = Path(gate.run_openai_codex_single_dispatch.__code__.co_filename).read_text(
        encoding="utf-8"
    )
    assert "client.responses.create" in source
    assert '["stream"] = True' in source
    assert "_consume_codex_event_stream" in source
    assert "run_codex_stream(" not in source
    assert "run_codex_create_stream_fallback" not in source
    assert "responses.stream" not in source
