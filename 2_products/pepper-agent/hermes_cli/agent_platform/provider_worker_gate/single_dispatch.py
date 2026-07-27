"""Single-dispatch OpenAI Codex Responses seam for the controlled gate."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import re
from typing import Any, Callable, Literal

from hermes_cli.agent_platform.provider_accounting import (
    ProviderAccountingOutcome,
    build_timeout_accounting,
    create_provider_accounting_record,
    normalize_codex_responses_usage,
    validate_worker_result_accounting_link,
)
from hermes_cli.agent_platform.provider_failure_policy import (
    ProviderFailureOrigin,
    ProviderFailureSignal,
    ProviderFailureStage,
    ProviderSDKExceptionKind,
    build_provider_failure_record,
    build_provider_retry_decision,
    validate_failure_accounting_link,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    MAXIMUM_OUTPUT_UTF8_BYTES,
    MAXIMUM_OUTPUT_TOKENS,
    BoundedProviderWorkerFailure,
    BoundedProviderWorkerRequest,
    BoundedProviderWorkerResult,
)
from hermes_cli.agent_platform.provider_worker.enums import (
    ProviderWorkerFailureStage,
    ProviderWorkerResultState,
)
from hermes_cli.agent_platform.provider_worker_gate.contracts import (
    GateCheckpoint,
    GateFailurePhase,
    GateLocalFailureCategory,
    OPENAI_CODEX_ENDPOINT,
    OPENAI_CODEX_MODEL_ID,
    OPENAI_CODEX_P15_7_EXPECTED_OUTPUT,
    OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION,
    OPENAI_CODEX_PROVIDER,
    OPENAI_CODEX_REASONING_EFFORT,
    OPENAI_CODEX_REASONING_SUMMARY,
    ProviderWorkerGateDispatchEvidence,
    ProviderWorkerGateDiagnostics,
    ProviderWorkerGateRequest,
    ProviderWorkerGateResult,
)


_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_FORBIDDEN_CODEX_BACKEND_CREATE_KEYS = frozenset({
    "max_output_tokens",
    "tools",
    "tool_choice",
    "parallel_tool_calls",
    "service_tier",
    "fallback_model",
    "timeout",
    "extra_headers",
    "extra_body",
})
_TERMINAL_EVENT_TYPES = frozenset({
    "response.completed",
    "response.failed",
    "response.incomplete",
})
_SAFE_EXCEPTION_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]{0,127}$")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime values must be timezone-aware")
    return value.astimezone(timezone.utc)


def _safe_text(value: object, *, maximum_length: int = 240) -> str | None:
    if value is None:
        return None
    text = "".join(
        character for character in str(value) if 32 <= ord(character) < 127
    ).strip()
    return text[:maximum_length] if text else None


def _field(value: Any, name: str, default: Any = None) -> Any:
    observed = getattr(value, name, None)
    if observed is None and isinstance(value, dict):
        observed = value.get(name, default)
    return observed if observed is not None else default


def _safe_identifier(value: object) -> str | None:
    text = str(value or "").strip()
    if _IDENTIFIER_RE.fullmatch(text):
        return text
    return None


def _append_checkpoint(
    checkpoints: list[GateCheckpoint],
    checkpoint: GateCheckpoint,
) -> None:
    if checkpoint not in checkpoints:
        checkpoints.append(checkpoint)


def _safe_exception_name(value: object) -> str | None:
    text = str(value or "").strip()
    if _SAFE_EXCEPTION_NAME_RE.fullmatch(text):
        return text[:128]
    return None


def _safe_exception_class(exc: Exception | None) -> str | None:
    if exc is None:
        return None
    return _safe_exception_name(exc.__class__.__name__)


def _safe_exception_module(exc: Exception | None) -> str | None:
    if exc is None:
        return None
    return _safe_exception_name(exc.__class__.__module__)


def _local_failure_category(exc: Exception) -> GateLocalFailureCategory:
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return "local_environment_import_failure"
    if isinstance(exc, FileNotFoundError):
        return "local_environment_missing_file"
    if isinstance(exc, PermissionError):
        return "local_environment_permission_failure"
    if isinstance(exc, ValueError):
        return "local_request_construction_or_contract_failure"
    return "local_internal_unknown"


def _observed_event_stream(
    event_stream: Any,
    checkpoints: list[GateCheckpoint],
) -> Any:
    _append_checkpoint(checkpoints, "stream_iteration_started")
    first_event_observed = False
    for event in event_stream:
        if not first_event_observed:
            _append_checkpoint(checkpoints, "first_event_observed")
            first_event_observed = True
        event_type = _field(event, "type", "")
        if isinstance(event_type, str) and event_type in _TERMINAL_EVENT_TYPES:
            _append_checkpoint(checkpoints, "terminal_event_observed")
        yield event


def build_usage_record_id(
    *,
    runtime_id: str,
    correlation_id: str,
    request_id: str,
) -> str:
    """Build a deterministic bounded usage-record identifier."""

    payload = "\0".join((runtime_id, correlation_id, request_id))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"usage-{digest}"


def build_provider_worker_gate_request(
    worker_request: BoundedProviderWorkerRequest,
    *,
    requested_at_utc: datetime | None = None,
    usage_record_id: str | None = None,
) -> ProviderWorkerGateRequest:
    """Compose a controlled-gate request from an already-bounded worker request."""

    return ProviderWorkerGateRequest(
        worker_request=worker_request,
        usage_record_id=usage_record_id
        or build_usage_record_id(
            runtime_id=worker_request.runtime_id,
            correlation_id=worker_request.correlation_id,
            request_id=worker_request.request_id,
        ),
        requested_at_utc=requested_at_utc or _utc_now(),
    )


def build_codex_responses_create_kwargs(
    gate_request: ProviderWorkerGateRequest,
) -> dict[str, Any]:
    """Return the source-native Codex Responses payload for one governed request."""

    from agent.transports.codex import ResponsesApiTransport

    transport = ResponsesApiTransport()
    create_kwargs = transport.build_kwargs(
        OPENAI_CODEX_MODEL_ID,
        [{"role": "user", "content": gate_request.worker_request.user_content}],
        tools=None,
        instructions=OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION,
        reasoning_config={"effort": OPENAI_CODEX_REASONING_EFFORT},
        is_codex_backend=True,
        provider=OPENAI_CODEX_PROVIDER,
        base_url=OPENAI_CODEX_ENDPOINT,
        max_tokens=MAXIMUM_OUTPUT_TOKENS,
    )
    create_kwargs["stream"] = True
    return assert_canonical_codex_backend_create_kwargs(create_kwargs)


def assert_canonical_codex_backend_create_kwargs(
    create_kwargs: dict[str, Any],
) -> dict[str, Any]:
    """Reject non-canonical Codex backend wire fields before dispatch."""

    forbidden = _FORBIDDEN_CODEX_BACKEND_CREATE_KEYS.intersection(create_kwargs)
    if forbidden:
        joined = ",".join(sorted(forbidden))
        raise ValueError(f"noncanonical_codex_backend_request_shape:{joined}")
    if create_kwargs.get("model") != OPENAI_CODEX_MODEL_ID:
        raise ValueError("noncanonical_codex_backend_request_shape:model")
    if create_kwargs.get("instructions") != OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION:
        raise ValueError("noncanonical_codex_backend_request_shape:instructions")
    if create_kwargs.get("store") is not False:
        raise ValueError("noncanonical_codex_backend_request_shape:store")
    if create_kwargs.get("stream") is not True:
        raise ValueError("noncanonical_codex_backend_request_shape:stream")
    if create_kwargs.get("reasoning") != {
        "effort": OPENAI_CODEX_REASONING_EFFORT,
        "summary": OPENAI_CODEX_REASONING_SUMMARY,
    }:
        raise ValueError("noncanonical_codex_backend_request_shape:reasoning")
    input_items = create_kwargs.get("input")
    if not isinstance(input_items, list) or not input_items:
        raise ValueError("noncanonical_codex_backend_request_shape:input")
    return create_kwargs


def run_openai_codex_single_dispatch(
    gate_request: ProviderWorkerGateRequest,
    *,
    client: Any,
    event_consumer: Callable[..., Any] | None = None,
    now: datetime | None = None,
    initial_checkpoints: tuple[GateCheckpoint, ...] = (),
) -> ProviderWorkerGateResult:
    """Issue at most one streamed Responses create call and return linked evidence."""

    from agent.codex_runtime import _consume_codex_event_stream

    consumer = event_consumer or _consume_codex_event_stream
    started_at = _utc(now or _utc_now())
    create_call_count = 0
    event_stream: Any = None
    stream_exists = False
    checkpoints = list(initial_checkpoints)
    _append_checkpoint(checkpoints, "request_validated")

    try:
        create_kwargs = build_codex_responses_create_kwargs(gate_request)
    except Exception as exc:
        completed_at = _utc(now or _utc_now())
        signal = _failure_signal_from_exception(
            exc,
            provider_dispatch_occurred=False,
            failure_phase="preflight",
        )
        return _build_failed_result(
            gate_request=gate_request,
            signal=signal,
            create_call_count=create_call_count,
            started_at_utc=started_at,
            completed_at_utc=completed_at,
            stream_exists=stream_exists,
            checkpoints=checkpoints,
            failure_phase="preflight",
            local_failure_category=_local_failure_category(exc),
            exception=exc,
        )

    try:
        _append_checkpoint(checkpoints, "dispatch_started")
        create_call_count = 1
        event_stream = client.responses.create(**create_kwargs)
    except Exception as exc:
        completed_at = _utc(now or _utc_now())
        signal = _failure_signal_from_exception(
            exc,
            provider_dispatch_occurred=True,
            failure_phase="dispatch",
        )
        return _build_failed_result(
            gate_request=gate_request,
            signal=signal,
            create_call_count=create_call_count,
            started_at_utc=started_at,
            completed_at_utc=completed_at,
            stream_exists=stream_exists,
            checkpoints=checkpoints,
            failure_phase="dispatch",
            local_failure_category="provider_failure_delegated_to_p15_6",
            exception=exc,
        )

    try:
        stream_exists = True
        _append_checkpoint(checkpoints, "event_stream_obtained")
        final = consumer(
            _observed_event_stream(event_stream, checkpoints),
            model=OPENAI_CODEX_MODEL_ID,
        )
        completed_at = _utc(now or _utc_now())
        try:
            return _build_result_from_final_response(
                gate_request=gate_request,
                final=final,
                create_call_count=create_call_count,
                started_at_utc=started_at,
                completed_at_utc=completed_at,
                checkpoints=checkpoints,
            )
        except Exception as exc:
            signal = ProviderFailureSignal(
                origin=ProviderFailureOrigin.ACCOUNTING_VALIDATION,
                stage=ProviderFailureStage.ACCOUNTING,
                provider_dispatch_occurred=True,
                provider_response_id_present=bool(
                    _safe_identifier(_field(final, "id"))
                ),
            )
            return _build_failed_result(
                gate_request=gate_request,
                signal=signal,
                create_call_count=create_call_count,
                started_at_utc=started_at,
                completed_at_utc=completed_at,
                stream_exists=stream_exists,
                checkpoints=checkpoints,
                failure_phase="accounting",
                local_failure_category="local_internal_unknown",
                exception=exc,
            )
    except Exception as exc:
        completed_at = _utc(now or _utc_now())
        signal = _failure_signal_from_exception(
            exc,
            provider_dispatch_occurred=True,
            failure_phase="stream",
        )
        return _build_failed_result(
            gate_request=gate_request,
            signal=signal,
            create_call_count=create_call_count,
            started_at_utc=started_at,
            completed_at_utc=completed_at,
            stream_exists=stream_exists,
            checkpoints=checkpoints,
            failure_phase="stream",
            local_failure_category="provider_failure_delegated_to_p15_6",
            exception=exc,
        )
    finally:
        close_fn = getattr(event_stream, "close", None)
        if callable(close_fn):
            try:
                close_fn()
            except Exception:
                pass


def _build_result_from_final_response(
    *,
    gate_request: ProviderWorkerGateRequest,
    final: Any,
    create_call_count: int,
    started_at_utc: datetime,
    completed_at_utc: datetime,
    checkpoints: list[GateCheckpoint],
) -> ProviderWorkerGateResult:
    status = str(_field(final, "status", "") or "")
    output_text = _field(final, "output_text", "")
    if (
        status != "completed"
        or not isinstance(output_text, str)
        or not output_text.strip()
    ):
        signal = ProviderFailureSignal(
            origin=ProviderFailureOrigin.TERMINAL_EVENT,
            stage=ProviderFailureStage.TERMINAL,
            terminal_status=status if status in {"incomplete", "failed"} else "failed",
            provider_dispatch_occurred=True,
            provider_response_id_present=bool(_safe_identifier(_field(final, "id"))),
        )
        return _build_failed_result(
            gate_request=gate_request,
            signal=signal,
            create_call_count=create_call_count,
            started_at_utc=started_at_utc,
            completed_at_utc=completed_at_utc,
            stream_exists=True,
            checkpoints=checkpoints,
            failure_phase="terminal",
            local_failure_category="provider_failure_delegated_to_p15_6",
        )
    if len(output_text.encode("utf-8")) > MAXIMUM_OUTPUT_UTF8_BYTES:
        signal = ProviderFailureSignal(
            origin=ProviderFailureOrigin.LOCAL_VALIDATION,
            stage=ProviderFailureStage.TERMINAL,
            provider_message="local output limit exceeded",
            provider_dispatch_occurred=True,
            provider_response_id_present=bool(_safe_identifier(_field(final, "id"))),
        )
        return _build_failed_result(
            gate_request=gate_request,
            signal=signal,
            create_call_count=create_call_count,
            started_at_utc=started_at_utc,
            completed_at_utc=completed_at_utc,
            stream_exists=True,
            checkpoints=checkpoints,
            failure_phase="terminal",
            local_failure_category="local_request_validation_failure",
        )
    if output_text != OPENAI_CODEX_P15_7_EXPECTED_OUTPUT:
        signal = ProviderFailureSignal(
            origin=ProviderFailureOrigin.LOCAL_VALIDATION,
            stage=ProviderFailureStage.TERMINAL,
            provider_message="exact output validation failed",
            provider_dispatch_occurred=True,
            provider_response_id_present=bool(_safe_identifier(_field(final, "id"))),
        )
        return _build_failed_result(
            gate_request=gate_request,
            signal=signal,
            create_call_count=create_call_count,
            started_at_utc=started_at_utc,
            completed_at_utc=completed_at_utc,
            stream_exists=True,
            checkpoints=checkpoints,
            failure_phase="terminal",
            local_failure_category="local_request_validation_failure",
        )

    provider_response_id = _safe_identifier(_field(final, "id"))
    _append_checkpoint(checkpoints, "accounting_started")
    usage = normalize_codex_responses_usage(
        _field(final, "usage"),
        observed_at_utc=completed_at_utc,
        provider_response_id=provider_response_id,
        finish_reason=status,
    )
    timeout = build_timeout_accounting(
        started_at_utc=started_at_utc,
        completed_at_utc=completed_at_utc,
        outcome=ProviderAccountingOutcome.COMPLETED,
    )
    record = create_provider_accounting_record(
        usage_record_id=gate_request.usage_record_id,
        request_id=gate_request.worker_request.request_id,
        runtime_id=gate_request.worker_request.runtime_id,
        correlation_id=gate_request.worker_request.correlation_id,
        created_at_utc=completed_at_utc,
        usage=usage,
        timeout=timeout,
    )
    worker_result = BoundedProviderWorkerResult(
        request_id=gate_request.worker_request.request_id,
        runtime_id=gate_request.worker_request.runtime_id,
        correlation_id=gate_request.worker_request.correlation_id,
        state=ProviderWorkerResultState.COMPLETED,
        completed_at_utc=completed_at_utc,
        output_text=output_text,
        usage_record_id=gate_request.usage_record_id,
    )
    accounting_link = validate_worker_result_accounting_link(
        record=record,
        worker_result=worker_result,
    )
    _append_checkpoint(checkpoints, "accounting_completed")
    _append_checkpoint(checkpoints, "worker_result_completed")
    return ProviderWorkerGateResult(
        worker_result=worker_result,
        dispatch_evidence=_dispatch_evidence(
            gate_request=gate_request,
            create_call_count=create_call_count,
            started_at_utc=started_at_utc,
            completed_at_utc=completed_at_utc,
            provider_response_id_present=provider_response_id is not None,
        ),
        accounting_record=record,
        accounting_link=accounting_link,
        diagnostics=_diagnostics(
            checkpoints=checkpoints,
            create_call_count=create_call_count,
        ),
    )


def _build_failed_result(
    *,
    gate_request: ProviderWorkerGateRequest,
    signal: ProviderFailureSignal,
    create_call_count: int,
    started_at_utc: datetime,
    completed_at_utc: datetime,
    stream_exists: bool,
    checkpoints: list[GateCheckpoint],
    failure_phase: GateFailurePhase,
    local_failure_category: GateLocalFailureCategory,
    exception: Exception | None = None,
    temporary_credential_lease_exists: bool = True,
    temporary_projected_hermes_home_present: bool = True,
) -> ProviderWorkerGateResult:
    usage_record_id = gate_request.usage_record_id if create_call_count == 1 else None
    failure_record = build_provider_failure_record(
        request_id=gate_request.worker_request.request_id,
        runtime_id=gate_request.worker_request.runtime_id,
        correlation_id=gate_request.worker_request.correlation_id,
        signal=signal,
        usage_record_id=usage_record_id,
    )
    retry_decision = build_provider_retry_decision(
        failure_record,
        temporary_credential_lease_exists=temporary_credential_lease_exists,
        provider_stream_exists=stream_exists,
        temporary_projected_hermes_home_present=temporary_projected_hermes_home_present,
    )
    accounting_record = None
    accounting_link = None
    failure_accounting_link = None
    if usage_record_id is not None:
        usage = normalize_codex_responses_usage(None, observed_at_utc=completed_at_utc)
        timeout = build_timeout_accounting(
            started_at_utc=started_at_utc,
            completed_at_utc=completed_at_utc,
            outcome=failure_record.accounting_outcome,
            timeout_stage=failure_record.accounting_timeout_stage,
        )
        accounting_record = create_provider_accounting_record(
            usage_record_id=usage_record_id,
            request_id=failure_record.request_id,
            runtime_id=failure_record.runtime_id,
            correlation_id=failure_record.correlation_id,
            created_at_utc=completed_at_utc,
            usage=usage,
            timeout=timeout,
        )
        failure_accounting_link = validate_failure_accounting_link(
            failure_record=failure_record,
            accounting_record=accounting_record,
        )

    worker_result = BoundedProviderWorkerResult(
        request_id=gate_request.worker_request.request_id,
        runtime_id=gate_request.worker_request.runtime_id,
        correlation_id=gate_request.worker_request.correlation_id,
        state=ProviderWorkerResultState.FAILED,
        completed_at_utc=completed_at_utc,
        usage_record_id=usage_record_id,
        failure=BoundedProviderWorkerFailure(
            failure_code=failure_record.category.value,
            stage=_worker_failure_stage(failure_record.stage),
            safe_message=failure_record.safe_summary,
        ),
    )
    if accounting_record is not None:
        accounting_link = validate_worker_result_accounting_link(
            record=accounting_record,
            worker_result=worker_result,
        )
    _append_checkpoint(checkpoints, "worker_result_completed")
    return ProviderWorkerGateResult(
        worker_result=worker_result,
        dispatch_evidence=_dispatch_evidence(
            gate_request=gate_request,
            create_call_count=create_call_count,
            started_at_utc=started_at_utc,
            completed_at_utc=completed_at_utc,
            provider_response_id_present=signal.provider_response_id_present,
        ),
        accounting_record=accounting_record,
        accounting_link=accounting_link,
        failure_record=failure_record,
        failure_retry_decision=retry_decision,
        failure_accounting_link=failure_accounting_link,
        diagnostics=_diagnostics(
            checkpoints=checkpoints,
            create_call_count=create_call_count,
            failure_phase=failure_phase,
            local_failure_category=local_failure_category,
            exception=exception,
        ),
    )


def _dispatch_evidence(
    *,
    gate_request: ProviderWorkerGateRequest,
    create_call_count: int,
    started_at_utc: datetime,
    completed_at_utc: datetime,
    provider_response_id_present: bool,
) -> ProviderWorkerGateDispatchEvidence:
    return ProviderWorkerGateDispatchEvidence(
        request_id=gate_request.worker_request.request_id,
        runtime_id=gate_request.worker_request.runtime_id,
        correlation_id=gate_request.worker_request.correlation_id,
        usage_record_id=gate_request.usage_record_id,
        responses_create_call_count=create_call_count,
        started_at_utc=started_at_utc,
        completed_at_utc=completed_at_utc,
        provider_response_id_present=provider_response_id_present,
    )


def _diagnostics(
    *,
    checkpoints: list[GateCheckpoint],
    create_call_count: int,
    failure_phase: GateFailurePhase | None = None,
    local_failure_category: GateLocalFailureCategory | None = None,
    exception: Exception | None = None,
) -> ProviderWorkerGateDiagnostics:
    return ProviderWorkerGateDiagnostics(
        checkpoints=tuple(checkpoints),
        provider_dispatches_for_attempt=create_call_count,
        failure_phase=failure_phase,
        local_failure_category=local_failure_category,
        safe_exception_class=_safe_exception_class(exception),
        safe_exception_module=_safe_exception_module(exception),
    )


def build_local_gate_failure_result(
    *,
    gate_request: ProviderWorkerGateRequest,
    started_at_utc: datetime,
    completed_at_utc: datetime,
    checkpoints: list[GateCheckpoint],
    failure_phase: GateFailurePhase,
    local_failure_category: GateLocalFailureCategory,
    exception: Exception,
    temporary_credential_lease_exists: bool,
    temporary_projected_hermes_home_present: bool,
) -> ProviderWorkerGateResult:
    signal = _failure_signal_from_exception(
        exception,
        provider_dispatch_occurred=False,
        failure_phase=failure_phase,
    )
    return _build_failed_result(
        gate_request=gate_request,
        signal=signal,
        create_call_count=0,
        started_at_utc=started_at_utc,
        completed_at_utc=completed_at_utc,
        stream_exists=False,
        checkpoints=checkpoints,
        failure_phase=failure_phase,
        local_failure_category=local_failure_category,
        exception=exception,
        temporary_credential_lease_exists=temporary_credential_lease_exists,
        temporary_projected_hermes_home_present=(
            temporary_projected_hermes_home_present
        ),
    )


def with_gate_cleanup_status(
    result: ProviderWorkerGateResult,
    *,
    cleanup_status: Literal["passed", "failed"],
    cleanup_exception: Exception | None = None,
) -> ProviderWorkerGateResult:
    checkpoints = list(result.diagnostics.checkpoints)
    _append_checkpoint(checkpoints, "cleanup_started")
    _append_checkpoint(checkpoints, "cleanup_completed")
    updates: dict[str, Any] = {
        "checkpoints": tuple(checkpoints),
        "cleanup_status": cleanup_status,
    }
    if cleanup_status == "failed":
        updates.update({
            "cleanup_failure_category": _local_failure_category(
                cleanup_exception or RuntimeError("cleanup_failed")
            ),
            "cleanup_safe_exception_class": _safe_exception_class(cleanup_exception),
            "cleanup_safe_exception_module": _safe_exception_module(cleanup_exception),
        })
    return result.model_copy(
        update={"diagnostics": result.diagnostics.model_copy(update=updates)},
    )


def _failure_signal_from_exception(
    exc: Exception,
    *,
    provider_dispatch_occurred: bool,
    failure_phase: GateFailurePhase,
) -> ProviderFailureSignal:
    stage = _provider_failure_stage_from_phase(failure_phase)
    if failure_phase in {"preflight", "client_construction"}:
        return ProviderFailureSignal(
            origin=ProviderFailureOrigin.LOCAL_VALIDATION,
            stage=stage,
            provider_dispatch_occurred=False,
        )
    status = _http_status(exc)
    if status is not None:
        return ProviderFailureSignal(
            origin=ProviderFailureOrigin.HTTP_RESPONSE,
            stage=stage,
            HTTP_status=status,
            provider_error_code=_safe_text(getattr(exc, "code", None)),
            provider_dispatch_occurred=provider_dispatch_occurred,
        )
    return ProviderFailureSignal(
        origin=ProviderFailureOrigin.SDK_EXCEPTION,
        stage=stage,
        SDK_exception_kind=ProviderSDKExceptionKind.GENERIC,
        provider_dispatch_occurred=provider_dispatch_occurred,
    )


def _provider_failure_stage_from_phase(
    failure_phase: GateFailurePhase,
) -> ProviderFailureStage:
    if failure_phase in {"preflight", "client_construction"}:
        return ProviderFailureStage.PREFLIGHT
    if failure_phase == "dispatch":
        return ProviderFailureStage.DISPATCH
    if failure_phase == "stream":
        return ProviderFailureStage.STREAM
    if failure_phase == "terminal":
        return ProviderFailureStage.TERMINAL
    if failure_phase == "accounting":
        return ProviderFailureStage.ACCOUNTING
    return ProviderFailureStage.SHUTDOWN


def _http_status(exc: Exception) -> int | None:
    for name in ("status_code", "status"):
        value = getattr(exc, name, None)
        if isinstance(value, int) and 100 <= value <= 599:
            return value
    response = getattr(exc, "response", None)
    value = getattr(response, "status_code", None)
    if isinstance(value, int) and 100 <= value <= 599:
        return value
    return None


def _sdk_exception_kind_and_stage(
    exc: Exception,
) -> tuple[ProviderSDKExceptionKind, ProviderFailureStage]:
    name = exc.__class__.__name__.lower()
    if "ssl" in name or "certificate" in name:
        return (
            ProviderSDKExceptionKind.SSL_VERIFICATION_ERROR,
            ProviderFailureStage.CONNECTION,
        )
    if "connect" in name:
        return ProviderSDKExceptionKind.CONNECT_ERROR, ProviderFailureStage.CONNECTION
    if "timeout" in name:
        return ProviderSDKExceptionKind.READ_TIMEOUT, ProviderFailureStage.STREAM
    if "protocol" in name:
        return (
            ProviderSDKExceptionKind.REMOTE_PROTOCOL_ERROR,
            ProviderFailureStage.STREAM,
        )
    if isinstance(exc, (TimeoutError,)):
        return ProviderSDKExceptionKind.READ_TIMEOUT, ProviderFailureStage.STREAM
    return ProviderSDKExceptionKind.GENERIC, ProviderFailureStage.STREAM


def _worker_failure_stage(
    stage: ProviderFailureStage,
) -> ProviderWorkerFailureStage:
    if stage is ProviderFailureStage.PREFLIGHT:
        return ProviderWorkerFailureStage.REQUEST_VALIDATION
    if stage is ProviderFailureStage.CREDENTIAL:
        return ProviderWorkerFailureStage.PROVIDER_BINDING
    if stage is ProviderFailureStage.CANCELLATION:
        return ProviderWorkerFailureStage.CANCELLATION
    if stage is ProviderFailureStage.SHUTDOWN:
        return ProviderWorkerFailureStage.SHUTDOWN
    return ProviderWorkerFailureStage.EXECUTION


__all__ = [
    "assert_canonical_codex_backend_create_kwargs",
    "build_codex_responses_create_kwargs",
    "build_provider_worker_gate_request",
    "build_usage_record_id",
    "run_openai_codex_single_dispatch",
]
