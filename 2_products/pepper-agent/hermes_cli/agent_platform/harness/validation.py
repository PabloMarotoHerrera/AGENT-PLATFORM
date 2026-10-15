"""Pure bounded JSON transport and byte integrity checks; no reference resolution."""

import hashlib
import hmac
import json
from typing import TypeVar

from .contracts import ContentRef, EvidenceReference, _Contract

_Model = TypeVar("_Model", bound=_Contract)
MAX_JSON_BYTES = 1_048_576


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def parse_contract(model: type[_Model], data: str | bytes) -> _Model:
    """Caller selects the trusted type; serialized data cannot select Python code."""
    if not isinstance(model, type) or not issubclass(model, _Contract) or model is _Contract:
        raise TypeError("expected a harness contract type")
    if not isinstance(data, (str, bytes)):
        raise TypeError("expected JSON text or bytes")
    raw = data.encode("utf-8") if isinstance(data, str) else data
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError("contract exceeds transport bound")
    # Reject duplicate keys before model parsing; nesting is finite in every model.
    try:
        json.loads(raw, object_pairs_hook=_unique_object)
    except RecursionError as exc:
        raise ValueError("excessive JSON nesting") from exc
    return model.model_validate_json(raw)


def canonical_json(contract: _Contract) -> str:
    """UTF-8 JSON, sorted keys, compact separators; ordered sequences retain order.

    Revalidate even instances: unsafe model_construct/model_copy bypass validation
    and must not be treated as a transport boundary.
    """
    if not isinstance(contract, _Contract):
        raise TypeError("expected a harness contract")
    validated = parse_contract(type(contract), contract.model_dump_json())
    return json.dumps(validated.model_dump(mode="json"), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_bytes(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise TypeError("expected bytes, not a file or locator")
    return hashlib.sha256(data).hexdigest()


def verify_content_digest(data: bytes, reference: ContentRef | EvidenceReference) -> bool:
    """Compare supplied bytes only. A matching digest is not consent or a signature."""
    if not isinstance(reference, (ContentRef, EvidenceReference)):
        raise TypeError("expected content or evidence reference")
    validated = parse_contract(type(reference), canonical_json(reference))
    return hmac.compare_digest(sha256_bytes(data), validated.sha256)
