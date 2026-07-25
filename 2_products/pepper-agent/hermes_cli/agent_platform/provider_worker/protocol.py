"""Deterministic in-memory protocol serialization for bounded worker envelopes."""

from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from hermes_cli.agent_platform.provider_worker.contracts import (
    MAXIMUM_REQUEST_UTF8_BYTES,
    MAXIMUM_RESULT_ENVELOPE_UTF8_BYTES,
    BoundedProviderWorkerRequest,
    BoundedProviderWorkerResult,
)


class ProviderWorkerProtocolError(ValueError):
    """Raised when a bounded worker protocol frame is invalid."""

    def __init__(self, code: str, payload_category: str, payload_size: int) -> None:
        self.code = code
        self.payload_category = payload_category
        self.payload_size = payload_size
        super().__init__(
            f"code={code} payload_category={payload_category} payload_size={payload_size}"
        )


def serialize_worker_request(request: BoundedProviderWorkerRequest) -> bytes:
    """Serialize one worker request to deterministic UTF-8 JSON bytes."""

    return _serialize(
        request,
        payload_category="worker_request",
        maximum_size=MAXIMUM_REQUEST_UTF8_BYTES,
    )


def deserialize_worker_request(payload: bytes) -> BoundedProviderWorkerRequest:
    """Deserialize one deterministic worker request JSON object."""

    data = _deserialize_json_object(
        payload,
        payload_category="worker_request",
        maximum_size=MAXIMUM_REQUEST_UTF8_BYTES,
    )
    try:
        return BoundedProviderWorkerRequest.model_validate(data)
    except ValidationError as exc:
        raise ProviderWorkerProtocolError(
            "request_validation_failed", "worker_request", len(payload)
        ) from exc


def serialize_worker_result(result: BoundedProviderWorkerResult) -> bytes:
    """Serialize one worker result to deterministic UTF-8 JSON bytes."""

    return _serialize(
        result,
        payload_category="worker_result",
        maximum_size=MAXIMUM_RESULT_ENVELOPE_UTF8_BYTES,
    )


def deserialize_worker_result(payload: bytes) -> BoundedProviderWorkerResult:
    """Deserialize one deterministic worker result JSON object."""

    data = _deserialize_json_object(
        payload,
        payload_category="worker_result",
        maximum_size=MAXIMUM_RESULT_ENVELOPE_UTF8_BYTES,
    )
    try:
        return BoundedProviderWorkerResult.model_validate(data)
    except ValidationError as exc:
        raise ProviderWorkerProtocolError(
            "result_validation_failed", "worker_result", len(payload)
        ) from exc


def _serialize(model: Any, *, payload_category: str, maximum_size: int) -> bytes:
    payload = json.dumps(
        model.model_dump(mode="json"),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    if len(payload) > maximum_size:
        raise ProviderWorkerProtocolError(
            "serialized_payload_oversized", payload_category, len(payload)
        )
    return payload


def _deserialize_json_object(
    payload: bytes,
    *,
    payload_category: str,
    maximum_size: int,
) -> dict[str, Any]:
    if len(payload) > maximum_size:
        raise ProviderWorkerProtocolError(
            "payload_oversized", payload_category, len(payload)
        )
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProviderWorkerProtocolError(
            "payload_not_utf8", payload_category, len(payload)
        ) from exc
    decoder = json.JSONDecoder(
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_json_constant,
    )
    try:
        data, end = decoder.raw_decode(text)
    except ValueError as exc:
        raise ProviderWorkerProtocolError(
            "payload_not_json_object", payload_category, len(payload)
        ) from exc
    if text[end:].strip():
        raise ProviderWorkerProtocolError(
            "multiple_json_values_rejected", payload_category, len(payload)
        )
    if not isinstance(data, dict):
        raise ProviderWorkerProtocolError(
            "payload_not_json_object", payload_category, len(payload)
        )
    return data


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object keys are rejected")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError("non-finite JSON values are rejected")


__all__ = [
    "ProviderWorkerProtocolError",
    "deserialize_worker_request",
    "deserialize_worker_result",
    "serialize_worker_request",
    "serialize_worker_result",
]
