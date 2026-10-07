"""Retrieve an already persisted human script; never prepare or execute it."""

import hashlib
import json
import re

MAX_RECORD_BYTES = 8 * 1024 * 1024
MAX_SCRIPT_BYTES = 256 * 1024
GUARDS = (
    "ticket_id", "reviewed_run_id", "handoff_prepare_identity_SHA256",
    "handoff_prepare_record_SHA256", "P17_7_handoff_package_SHA256",
    "materialization_plan_SHA256", "rendered_powershell_SHA256",
)


def inspect(**guards):
    """Return exact persisted UTF-8 text plus both canonical and raw digests.

    C12's rendered_powershell_SHA256 hashes an algorithm-prefixed canonical
    JSON envelope, not the raw .ps1 bytes. Neither digest is supplied as proof
    by the caller: authority is independently validated before comparison.
    """
    from hermes_cli import kanban_db
    from . import execution_evidence, post_accept_material_revision as revision
    from . import product_runtime as pr

    if set(guards) != set(GUARDS):
        raise ValueError("handoff_script requires exactly the seven handoff authority guards")
    if not isinstance(guards["ticket_id"], str) or not guards["ticket_id"]:
        raise ValueError("exact ticket guard is required")
    if type(guards["reviewed_run_id"]) is not int or guards["reviewed_run_id"] < 1:
        raise ValueError("exact integer reviewed run guard is required")
    for key in GUARDS[2:]:
        if not isinstance(guards[key], str) or not re.fullmatch(r"[0-9a-f]{64}", guards[key]):
            raise ValueError(f"invalid {key} guard")

    with kanban_db.scoped_read_only_connections(execution_evidence.connection):
        projection = pr._load_current_projection_record()
        if guards["ticket_id"] != projection["ticket_id"]:
            raise ValueError("handoff ticket guard differs from current authority")
        revision.assert_handoff_current(projection)
        path = pr.human_git_handoff_prepare_record_path_for_ticket(projection["ticket_id"])
        with path.open("rb") as stream:
            raw = stream.read(MAX_RECORD_BYTES + 1)
        if len(raw) > MAX_RECORD_BYTES:
            raise ValueError("persisted handoff exceeds inspection bound")
        record = json.loads(raw.decode("utf-8"))
        if not isinstance(record, dict):
            raise ValueError("persisted handoff must be an object")
        body = record.get("rendered_handoff_powershell")
        if not isinstance(body, str) or not body or "\x00" in body:
            raise ValueError("persisted rendering is missing or malformed")
        script_bytes = body.encode("utf-8")
        if len(script_bytes) > MAX_SCRIPT_BYTES:
            raise ValueError("persisted rendering exceeds complete-script inspection bound")
        if body.startswith("\ufeff") or "\r" in body or not body.endswith("\n"):
            raise ValueError("persisted rendering violates UTF-8/no-BOM/LF/terminal-newline contract")
        if revision.supersedes_lifecycle_record(projection, record, "handoff"):
            raise ValueError("handoff has been superseded by material revision")
        pr.validate_current_ticket_human_git_handoff_prepare_record(record, projection_record=projection)
        for key, expected in guards.items():
            if record.get(key) != expected:
                raise ValueError(f"handoff {key} guard mismatch")
        canonical_sha = pr._c12_rendered_handoff_digest(body)
        if canonical_sha != record["rendered_powershell_SHA256"]:
            raise ValueError("persisted rendering digest mismatch")
        package = record["P17_7_human_git_handoff_result"]["package"]
        for key, package_key in (("branch", "branch_name"), ("expected_parent_commit", "expected_parent_commit"), ("commit_message", "commit_message")):
            if record[key] != package[package_key]:
                raise ValueError(f"persisted handoff {key} differs from canonical P17.7 package")
        if len(record["candidate_paths"]) > 256:
            raise ValueError("accepted path set exceeds inspection bound")
        # Detect a concurrent replacement of the source; never mix two heads.
        with path.open("rb") as stream:
            if stream.read(MAX_RECORD_BYTES + 1) != raw:
                raise ValueError("handoff authority changed during inspection; read again")

    return {
        "success": True, "source_tool": "inspect_current_ticket_review_candidate",
        "operation": "handoff_script", "inspection_status": "available",
        "persistence_classification": "PATH_A", "read_only": True,
        **{key: record[key] for key in GUARDS},
        "rendered_handoff_powershell": body,
        "script_encoding": "UTF-8", "script_bom": False,
        "line_endings": "LF", "terminal_newline": True,
        "byte_count": len(script_bytes), "character_count": len(body),
        "script_bytes_SHA256": hashlib.sha256(script_bytes).hexdigest(),
        "recomputed_rendered_powershell_SHA256": canonical_sha,
        "rendered_digest_contract": {
            "algorithm": pr.PEPPER_HUMAN_GIT_HANDOFF_C12_RENDERED_DIGEST_ALGORITHM,
            "preimage": 'UTF-8(algorithm + "\\n" + json.dumps({"rendered_handoff_powershell": body}, sort_keys=True, separators=(",", ":"), ensure_ascii=True))',
            "raw_script_bytes_digest": False,
        },
        "expected_branch": record["branch"],
        "expected_parent_commit": record["expected_parent_commit"],
        "expected_commit_message": record["commit_message"],
        "candidate_paths": record["candidate_paths"], "candidate_count": len(record["candidate_paths"]),
        "post_execution_next_action": {key: str(value)[:300] for key, value in record["next_action"].items()
                                       if key in {"id", "label", "target_ticket_id", "required_human_action"}},
        "source_record_path": str(path), "source_record_bytes_SHA256": hashlib.sha256(raw).hexdigest(),
        "workflow_mutation": False, "handoff_regenerated": False,
        "materialization_performed": False, "Git_commands_executed": 0,
        "execution_preflight_performed": False,
    }
