"""Explicit isolated-verification delivery. Never installed by production config.

Only a trusted disposable test process may inject VerificationSession into the
private tools slot. This is not a sandbox against hostile Python in that process.
No imports of tools/runtime, no callbacks or legacy callables, no persistence.
"""

import json
from dataclasses import dataclass, field

from .harness.contracts import ContentRef
from .harness.shadow import LegacyObservation, Comparison, Provenance, compare
from .harness.validation import sha256_bytes
from .handler_correspondence import BindingEvidence
from .shadow_adapters import SnapshotMetadata, observe

MAX_RESULT_BYTES = 1_048_576
MAX_CAPTURES = 256


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_legacy_json_key")
        result[key] = value
    return result


@dataclass(frozen=True)
class CaptureSpec:
    entry: str
    metadata: SnapshotMetadata
    binding: BindingEvidence | None
    legacy: LegacyObservation


@dataclass(frozen=True)
class CapturedResult:
    entry: str
    result: ContentRef
    comparison: Comparison | None
    diagnostic: str | None


@dataclass
class VerificationSession:
    spec: CaptureSpec
    captures: list[CapturedResult] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    truncated: bool = False

    def fail(self, reason: str) -> None:
        if len(self.diagnostics) < MAX_CAPTURES:
            self.diagnostics.append(reason[:128])
        else:
            self.truncated = True


def observe_completed(session: VerificationSession, entry: str, result: str) -> None:
    if not isinstance(session, VerificationSession):
        raise TypeError("explicit_verification_session_required")
    try:
        if len(session.captures) >= MAX_CAPTURES:
            session.truncated = True
            session.fail("capture_bound")
            return
        if type(result) is not str or len(result) > MAX_RESULT_BYTES:
            session.fail("result_type_or_size_bound")
            return
        raw = result.encode("utf-8")
        if len(raw) > MAX_RESULT_BYTES:
            session.fail("result_size_bound")
            return
        output = ContentRef(content_id="legacy-result", sha256=sha256_bytes(raw))
        spec = session.spec
        if spec.entry != entry:
            session.fail("entry_mismatch")
            return
        # The fixture supplies pre-operation metadata. The result is independently
        # captured and bound, never used to invent prior consent or guard success.
        payload = json.loads(result, object_pairs_hook=_pairs)
        if not isinstance(payload, dict):
            raise ValueError("legacy_object_required")
        legacy = LegacyObservation.model_validate(spec.legacy)
        updates = {"source": output, "provenance": Provenance.EMPIRICAL, "authority_qualification": "UNOBSERVED",
            "unobservable": tuple(sorted(set(legacy.unobservable + (
                "legacy_full_guard_qualification", "live_source_currentness"))))}
        view_updates = {}
        if "next_action" in payload:
            from .harness.shadow import PublicAction
            raw_action = payload["next_action"]
            action = None
            if raw_action is not None:
                if not isinstance(raw_action, dict):
                    raise ValueError("legacy_action_object_required")
                fields = {k: v for k, v in raw_action.items() if k in PublicAction.model_fields and k != "schema_version"}
                if "id" in fields and "label" in fields:
                    action = PublicAction.model_validate(fields)
                else:
                    updates["unobservable"] += ("legacy_action_incomplete",)
                if set(raw_action) - set(fields):
                    updates["unobservable"] += ("legacy_action_extension_fields",)
            if legacy.view.mapping == "UNMAPPED":
                # An inspector can advertise a DIFFERENT next operation (e.g.
                # O04 returns an O05 request offer). Never rebind that offer to
                # the operation just observed or call the public actions equal.
                updates["unobservable"] += ("next_operation_action_not_compared",)
            else:
                view_updates["action"] = action
                if action and action.target_ticket_id:
                    view_updates["target_ticket_id"] = action.target_ticket_id
        for key in ("current_ticket_id", "next_ticket_id"):
            if key in payload:
                view_updates[key] = payload[key]
        if "active_execution_count" in payload and type(payload["active_execution_count"]) is int:
            view_updates["active_execution"] = payload["active_execution_count"] > 0
        if view_updates:
            updates["view"] = legacy.view.model_copy(update=view_updates)
        if payload.get("success") is False or "error" in payload:
            updates["valid"] = False
        legacy = LegacyObservation.model_validate(legacy.model_copy(update=updates))
        observation = observe(spec.metadata, spec.binding)
        comparison = compare(legacy, observation)
        session.captures.append(CapturedResult(entry, output, comparison, None))
    except Exception:
        session.fail("shadow_evaluation_failed")
