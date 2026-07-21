from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_worker as pw
from hermes_cli.agent_platform.provider_worker import protocol
from hermes_cli.agent_platform.provider_worker.protocol import (
    ProviderWorkerProtocolError,
    deserialize_worker_request,
    deserialize_worker_result,
    serialize_worker_request,
    serialize_worker_result,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)
WORKER_PROFILE_ID = "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
PROVIDER_PROFILE_ID = "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"


def make_request(
    content: str = "synthetic bounded request",
) -> pw.BoundedProviderWorkerRequest:
    return pw.BoundedProviderWorkerRequest(
        request_id="request.protocol",
        runtime_id="runtime.protocol",
        correlation_id="corr.protocol",
        requested_by="p15.3.protocol-test",
        submitted_at_utc=NOW,
        user_content=content,
    )


def make_failure() -> pw.BoundedProviderWorkerFailure:
    return pw.BoundedProviderWorkerFailure(
        failure_code="request_validation_failed",
        stage=pw.ProviderWorkerFailureStage.REQUEST_VALIDATION,
        safe_message="bounded synthetic request failure",
    )


def make_result(
    output_text: str = "synthetic bounded result",
) -> pw.BoundedProviderWorkerResult:
    return pw.BoundedProviderWorkerResult(
        request_id="request.protocol",
        runtime_id="runtime.protocol",
        correlation_id="corr.protocol",
        state=pw.ProviderWorkerResultState.COMPLETED,
        completed_at_utc=NOW,
        output_text=output_text,
    )


def test_request_serialization_is_deterministic_and_round_trips() -> None:
    request = make_request("hidden request body")
    first = serialize_worker_request(request)
    second = serialize_worker_request(request)

    assert first == second
    assert first.decode("utf-8").startswith('{"correlation_id"')
    assert deserialize_worker_request(first) == request
    assert "hidden request body" not in repr(request)


def test_result_serialization_is_deterministic_and_round_trips() -> None:
    result = make_result("hidden result body")
    first = serialize_worker_result(result)
    second = serialize_worker_result(result)

    assert first == second
    assert first.decode("utf-8").startswith('{"completed_at_utc"')
    assert deserialize_worker_result(first) == result
    assert "hidden result body" not in repr(result)


def test_failure_result_round_trips_with_bounded_failure_only() -> None:
    result = pw.BoundedProviderWorkerResult(
        request_id="request.protocol",
        runtime_id="runtime.protocol",
        correlation_id="corr.protocol",
        state=pw.ProviderWorkerResultState.FAILED,
        completed_at_utc=NOW,
        failure=make_failure(),
    )
    payload = serialize_worker_result(result)
    restored = deserialize_worker_result(payload)

    assert restored == result
    assert restored.output_text is None
    assert restored.failure is not None
    assert restored.failure.retryable is False
    assert len(restored.failure.safe_message.encode("utf-8")) <= 512


def test_protocol_requires_utf8_and_rejects_oversized_payload_before_parse() -> None:
    with pytest.raises(ProviderWorkerProtocolError) as utf8_error:
        deserialize_worker_request(b"\xff")
    assert utf8_error.value.code == "payload_not_utf8"

    oversized = b'{"x":"' + (b"a" * 131_073) + b'"}'
    with pytest.raises(ProviderWorkerProtocolError) as size_error:
        deserialize_worker_request(oversized)
    assert size_error.value.code == "payload_oversized"


def test_protocol_rejects_unknown_fields_and_multiple_json_values() -> None:
    request_payload = json.loads(serialize_worker_request(make_request()))
    request_payload["endpoint"] = "forbidden"
    with pytest.raises(ProviderWorkerProtocolError) as unknown_error:
        deserialize_worker_request(json.dumps(request_payload).encode("utf-8"))
    assert unknown_error.value.code == "request_validation_failed"

    with pytest.raises(ProviderWorkerProtocolError) as multiple_error:
        deserialize_worker_request(serialize_worker_request(make_request()) + b"{}")
    assert multiple_error.value.code == "multiple_json_values_rejected"


def test_protocol_rejects_duplicate_keys_nan_and_infinity() -> None:
    duplicate = b'{"schema_version":1,"schema_version":1}'
    with pytest.raises(ProviderWorkerProtocolError) as duplicate_error:
        deserialize_worker_request(duplicate)
    assert duplicate_error.value.code == "payload_not_json_object"

    common = (
        b'{"correlation_id":"corr.protocol","input_kind":"text",'
        b'"profile_id":"'
        + WORKER_PROFILE_ID.encode("utf-8")
        + b'","provider_runtime_profile_id":"'
        + PROVIDER_PROFILE_ID.encode("utf-8")
        + b'","request_id":"request.protocol","requested_by":"p15.3.protocol-test",'
        b'"runtime_id":"runtime.protocol","schema_version":1,'
        b'"submitted_at_utc":"2026-01-01T00:00:00Z","user_content":'
    )
    with pytest.raises(ProviderWorkerProtocolError):
        deserialize_worker_request(common + b"NaN}")
    with pytest.raises(ProviderWorkerProtocolError):
        deserialize_worker_request(common + b"Infinity}")


def test_protocol_rejects_empty_binary_and_oversized_result_content() -> None:
    with pytest.raises(ValidationError):
        make_request("")
    with pytest.raises(ValidationError):
        make_request("\x00")
    with pytest.raises(ValidationError):
        make_result("\x00")

    oversized_result = make_result("x" * 32_768)
    oversized_payload = serialize_worker_result(oversized_result) + (b" " * 65_536)
    with pytest.raises(ProviderWorkerProtocolError):
        deserialize_worker_result(oversized_payload)


def test_protocol_helpers_do_not_write_files_or_log_content() -> None:
    source = Path(protocol.__file__).read_text(encoding="utf-8").lower()
    for forbidden in (
        "logging",
        "logger",
        "print(",
        ".write_text",
        ".write_bytes",
        "open(",
        "path(",
        "request payload",
        "result payload",
        "user_content=",
        "output_text=",
    ):
        assert forbidden not in source
