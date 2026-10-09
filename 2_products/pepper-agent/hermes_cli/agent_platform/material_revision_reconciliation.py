"""Append-only human reconciliation of source-only material-request drift."""

import json

from . import command_validation as cv
from . import post_execution_material_revision as rev
from .post_accept_material_revision import serialized, revision_action

POLICY = "pepper-material-revision-authority-reconciliation-v1"
ACTION = "RECONCILE_MATERIAL_REVISION_AUTHORITY"
SOURCE = "canonical_validation_source"
MAX_LINKS = 8


def digest(record):
    return cv.digest({"policy_id": POLICY, "record": {
        k: v for k, v in record.items() if k != "reconciliation_SHA256"}})


def consent(binding):
    return f"{ACTION} BINDING {cv.digest(binding)}"


def path_for(generation, previous_sha):
    from .workflow.ticket_architect_bridge import _safe_digest
    return rev.path_for(generation).parent / "reconciliations" / (_safe_digest(previous_sha) + ".json")


def source_only(old, current):
    from .command_validation_context import POLICY as SOURCE_POLICY
    if {k: v for k, v in old.items() if k != SOURCE} != {k: v for k, v in current.items() if k != SOURCE}:
        raise ValueError("immutable material revision authority changed")
    a, b = old.get(SOURCE), current.get(SOURCE)
    keys = {"policy_id", "source_root", "source_files_SHA256", "source_file_count", "source_bytes"}
    if (not isinstance(a, dict) or not isinstance(b, dict) or set(a) != keys or set(b) != keys
            or a["policy_id"] != SOURCE_POLICY or b["policy_id"] != SOURCE_POLICY
            or a["source_root"] != b["source_root"] or a["source_files_SHA256"] == b["source_files_SHA256"]):
        raise ValueError("only canonical source fingerprint drift is reconcilable")


def effective(record):
    previous = record["previous_request"]
    binding = record["reconciliation_binding"]["current_request_binding"]
    result = {**previous, **binding, "request_binding": binding,
              "human_authorization_text": record["human_authorization_text"],
              "authorizer_id": record["authorizer_id"], "created_at": record["created_at"],
              "reconciliation_authority": record}
    result["material_revision_request_SHA256"] = rev.digest(result)
    return result


def validate(record, generation, depth=0):
    from .workflow import ticket_architect_bridge as bridge
    if depth >= MAX_LINKS or record.get("reconciliation_SHA256") != digest(record):
        raise ValueError("invalid or overlong material reconciliation authority")
    previous = rev.validate_record(record["previous_request"], generation, _depth=depth + 1)
    binding = record["reconciliation_binding"]
    source_only(previous["request_binding"], binding["current_request_binding"])
    expected = {"policy_id": POLICY, "reason": "canonical_source_fingerprint_drift",
                "human_authorization_text": consent(binding), "successor_generated": False,
                "execution_started": False, "Git_mutation": False}
    if (any(record.get(k) != v for k, v in expected.items())
            or binding["old_material_revision_request_SHA256"] != previous["material_revision_request_SHA256"]
            or binding["old_request_binding"] != previous["request_binding"]
            or bridge._reviewer_id_from_actor(record["authorizer_id"]) != record["authorizer_id"]
            or not record.get("created_at")):
        raise ValueError("material reconciliation binding or consent mismatch")
    artifact = binding["approved_artifact_binding"]
    current = binding["current_request_binding"]
    if (any(artifact.get(k) != current.get(k) for k in (
            "project_id", "ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256"))
            or artifact.get("revision") != f"R{current['revision']:04d}"
            or any(artifact.get(k) != generation[k] for k in (
                "project_id", "ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256", "bridge_SHA256") if k in generation)):
        raise ValueError("reconciliation approved artifact mismatch")
    return record


def resolve(generation, original):
    """Follow immutable links; corrupt links never fall back to old consent."""
    from .execution_evidence import read_json, kb
    current = original
    for depth in range(MAX_LINKS + 1):
        path = path_for(generation, current["material_revision_request_SHA256"])
        if not path.exists():
            return current
        if depth == MAX_LINKS:
            raise ValueError("material reconciliation chain exceeds bound")
        record = validate(read_json(path, kb.kanban_home(), maximum=rev.MAX_BYTES), generation)
        if record["previous_request"] != current:
            raise ValueError("conflicting material reconciliation predecessor")
        current = effective(record)
    raise ValueError("invalid reconciliation chain")


def context(projection):
    from . import approved_artifact_inspection as artifacts
    generation, current, history = rev.context(projection)
    previous = rev.load(generation)
    if previous is None:
        raise ValueError("valid prior post-execution request required")
    rev.validate_record(previous, generation)
    artifact = artifacts.inspect(ticket_id=current["ticket_id"], section_id="validation_steps")
    if previous["historical_authority"] != history:
        raise ValueError("historical completion, zero-change or validation authority changed")
    if previous["request_binding"] == current and "reconciliation_authority" in previous:
        record = previous["reconciliation_authority"]
        if (record["reconciliation_binding"]["approved_artifact_binding"] != artifact["artifact_binding"]
                or record["reconciliation_binding"]["validation_steps_SHA256"] != artifact["exact_body_serialized_SHA256"]):
            raise ValueError("reconciled artifact authority changed")
        return generation, previous, record["reconciliation_binding"], history, record
    source_only(previous["request_binding"], current)
    binding = {"old_material_revision_request_SHA256": previous["material_revision_request_SHA256"],
               "old_request_binding": previous["request_binding"], "current_request_binding": current,
               "approved_artifact_binding": artifact["artifact_binding"],
               "validation_steps_SHA256": artifact["exact_body_serialized_SHA256"]}
    return generation, previous, binding, history, None


def inspect(projection=None):
    from . import product_runtime as pr
    try:
        projection = projection or pr._load_current_projection_record()
        _, previous, binding, _, record = context(projection)
        result = {"read_only": True, "reconciliation_available": record is None,
                "blocker_classification": "canonical_source_fingerprint_drift" if record is None else None,
                "immutable_authority_identity_match": True, "reconciliation_binding": binding,
                "reconciliation_SHA256": record["reconciliation_SHA256"] if record else None,
                "material_revision_request_SHA256": previous["material_revision_request_SHA256"],
                "next_action": {"id": ACTION, "required_human_action": "authority_reconciliation",
                                "tool": "request_current_ticket_material_revision", "origin": "post_execution",
                                "operation": "reconcile",
                                "human_authorization_text": consent(binding)},
                "expected_next_action": revision_action(binding["current_request_binding"]["ticket_id"]),
                "expected_workflow_status": "awaiting_material_revision",
                "successor_generated": False, "execution_started": False, "Git_mutation": False}
        if len(json.dumps(result)) > 14000:
            raise ValueError("material reconciliation inspection exceeds bound")
        return result
    except (ValueError, OSError, KeyError, TypeError):
        return {"read_only": True, "reconciliation_available": False,
                "immutable_authority_identity_match": False,
                "blocker_classification": "material_revision_reconciliation_unqualified"}


@serialized
def reconcile(*, binding, human_authorization_text, next_action_id, authorizer_id="pepper-chat-human"):
    from . import product_runtime as pr
    from .workflow import ticket_architect_bridge as bridge
    from .zero_change_decision import persist
    with bridge._STORE_LOCK:
        projection = pr._load_current_projection_record()
        generation, previous, current, history, existing = context(projection)
        actor = bridge._reviewer_id_from_actor(authorizer_id)
        if binding != current or human_authorization_text != consent(current) or next_action_id != ACTION:
            raise ValueError("exact current reconciliation binding and explicit consent required")
        if existing:
            if existing["authorizer_id"] != actor:
                raise ValueError("conflicting reconciliation authorizer")
            return {"success": True, "idempotent_replay": True,
                    "reconciliation_SHA256": existing["reconciliation_SHA256"],
                    "material_revision_request_SHA256": previous["material_revision_request_SHA256"],
                    "next_action": revision_action(current["current_request_binding"]["ticket_id"]),
                    "successor_generated": False, "execution_started": False, "Git_mutation": False}
        workflow = pr.build_workflow_control_snapshot()
        if (workflow.get("workflow_status") != "material_revision_authority_blocked"
                or workflow.get("active_execution_count") != 0 or workflow.get("pending_ticket_approval_count") != 0
                or any(b["id"] != "POST-EXECUTION-MATERIAL-REVISION-AUTHORITY" for b in workflow.get("remaining_blockers", []))):
            raise ValueError("source reconciliation is not the current boundary")
        record = {"policy_id": POLICY, "reason": "canonical_source_fingerprint_drift",
                  "previous_request": previous, "reconciliation_binding": current,
                  "human_authorization_text": human_authorization_text, "authorizer_id": actor,
                  "created_at": pr._utc_now_iso(), "successor_generated": False,
                  "execution_started": False, "Git_mutation": False}
        record["reconciliation_SHA256"] = digest(record)
        validate(record, generation)
        result = effective(record)
        if len(json.dumps(result).encode()) > rev.MAX_BYTES:
            raise ValueError("material reconciliation exceeds size bound")
        if (pr._load_current_projection_record() != projection
                or context(projection) != (generation, previous, current, history, None)):
            raise ValueError("material reconciliation authority changed before persistence")
        persist(path_for(generation, previous["material_revision_request_SHA256"]), record)
        return {"success": True, "idempotent_replay": False, "reconciliation_SHA256": record["reconciliation_SHA256"],
                "material_revision_request_SHA256": result["material_revision_request_SHA256"],
                "next_action": revision_action(current["current_request_binding"]["ticket_id"]),
                "successor_generated": False, "execution_started": False, "Git_mutation": False}
