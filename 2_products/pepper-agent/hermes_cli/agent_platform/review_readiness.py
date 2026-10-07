"""Read-only review gate projection; historical recovery is not a prerequisite.

Recovery/retry mutation and validation retain their existing semantics. Only a
proven older recovery's obsolete *current workspace* comparison is superseded
here, after independently validating the current terminal candidate.
"""

import hashlib
import json
import sqlite3

MAX_BLOCKERS = 8
MAX_SOURCE_BYTES = 2 * 1024 * 1024


def _text(value, limit=300):
    return str(value)[:limit] if value is not None else None


def _recovery_source(projection):
    from . import product_runtime as pr

    path = pr.recovery_action_record_path_for_ticket(projection["ticket_id"])
    with path.open("rb") as handle:
        raw = handle.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise ValueError("recovery source exceeds inspection bound")
    record = json.loads(raw)
    if not isinstance(record, dict):
        raise ValueError("recovery source must be an object")
    from .workflow import ticket_architect_bridge as bridge
    revision = None
    generation = bridge.load_generation_record(ticket_id=projection["ticket_id"])
    if generation and generation["work_packet_SHA256"] == record.get("work_packet_SHA256"):
        revision = bridge._publication_from_generation_record(generation).revision
    return record, {
        "source": "pepper-recovery-action",
        "source_record_id": _text(record.get("recovery_action_SHA256"), 64),
        "source_run_id": record.get("latest_failed_run_id") if type(record.get("latest_failed_run_id")) is int else None,
        "source_ticket_id": _text(record.get("ticket_id"), 128),
        "source_revision": revision,
        "source_path": str(path),
        "source_bytes_sha256": hashlib.sha256(raw).hexdigest(),
        "created_at": _text(record.get("created_at"), 64),
        "updated_at": _text(record.get("updated_at"), 64),
        "active_condition": "Recovery authority is required for the current failed execution.",
        "clearing_condition": "A later independently validated current terminal candidate supersedes this failed run; review preparation is not required.",
        "derived": True,
        "integrity_valid": record.get("recovery_action_SHA256") == pr._recovery_action_record_digest(record),
    }


def _superseded_workspace_check(snapshot, projection, record):
    from hermes_cli import kanban_db as kb
    from . import product_runtime as pr, recovery_authority

    manual = snapshot.get("manual_validation") or {}
    if not (
        snapshot.get("workflow_status") == "execution_completed"
        and snapshot.get("review_state") == "ready_for_review_validation"
        and snapshot.get("recovery_state") == "not_required"
        and snapshot.get("validation_contract_satisfied") is True
        and snapshot.get("reviewable_result") is True
        and manual.get("human_action_required") is False
        and snapshot.get("active_execution_count") == 0
        and snapshot.get("pending_ticket_approval_count") == 0
    ):
        return False
    # Do not repair corrupt history or weaken the recovery loader. Its history
    # must still validate; the head is checked against its own failed run below.
    history_path = pr.recovery_action_history_path_for_ticket(projection["ticket_id"])
    if history_path.exists() and history_path.stat().st_size > MAX_SOURCE_BYTES:
        return False
    recovery_authority.history(projection)
    pr.validate_p18_9_0_recovery_action_record(record, projection_record=projection)
    completion = pr._current_review_round_completion_source(projection)
    contract = pr._acceptance_contract_for_review_projection(projection)
    if completion.get("blocker_code") or not pr._review_completion_validation_contract_satisfied(completion, contract):
        return False
    if pr._completion_current_terminal_run_authority_blocker(
        projection, completion, unavailable_code="CURRENT_RUN_UNAVAILABLE",
        mismatch_code="CURRENT_RUN_MISMATCH",
    ):
        return False
    current_id = completion.get("run_id")
    failed_id = record["latest_failed_run_id"]
    if type(current_id) is not int or type(failed_id) is not int or failed_id >= current_id:
        return False
    if any(manual.get(key) != projection.get(key) for key in ("ticket_id", "work_packet_id", "work_packet_SHA256")) or manual.get("run_id") != current_id:
        return False
    path = kb.kanban_db_path(board=projection["kanban_board_slug"])
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        task = kb.get_task(conn, projection["kanban_task_id"])
        runs = kb.list_runs(conn, projection["kanban_task_id"])
        failed = kb.get_run(conn, failed_id)
    if task is None or failed is None or not runs:
        return False
    if task.current_run_id or any(pr._execution_is_active(pr._run_dict(run)) for run in runs) or max(run.id for run in runs) != current_id:
        return False
    if failed.task_id != task.id or failed.ended_at is None or failed.profile != record["assignee_profile"]:
        return False
    if (failed.outcome or failed.status) not in pr._GOVERNED_TICKET_FAILURE_OUTCOMES:
        return False
    if any(record.get(key) != value for key, value in {
        "latest_failed_run_status": failed.status,
        "latest_failed_run_outcome": failed.outcome,
        "latest_failed_run_ended_at": failed.ended_at,
        "observed_attempt_count": sum(run.id <= failed_id for run in runs),
    }.items()):
        return False
    digest = hashlib.sha256(json.dumps(pr._run_dict(failed), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if record.get("terminal_run_SHA256", digest) != digest:
        return False
    return task.workspace_path != record.get("kanban_task_workspace_path")


def _public(blocker):
    # Allowlist, not a dump of arbitrary producer payloads.
    result = {key: _text(blocker.get(key), 300 if key in {
        "source_path", "active_condition", "clearing_condition",
    } else 128) for key in (
        "code", "category", "status", "source", "source_record_id",
        "source_ticket_id", "source_path", "source_bytes_sha256", "created_at",
        "updated_at", "active_condition", "clearing_condition",
    )}
    result.update(
        blocker_id=_text(blocker.get("id"), 128),
        reason=_text(blocker.get("evidence")),
        code=result["code"] or _text(blocker.get("status"), 128),
        category=result["category"] or "workflow_authority",
        source=result["source"] or "product_runtime.remaining_blockers",
        source_run_id=blocker.get("source_run_id") if type(blocker.get("source_run_id")) is int else None,
        source_revision=blocker.get("source_revision") if type(blocker.get("source_revision")) is int else None,
        blocks_review=blocker.get("blocks_review") is not False,
        historical=blocker.get("historical") is True,
        derived=True,
        integrity_valid=blocker.get("integrity_valid") if type(blocker.get("integrity_valid")) is bool else None,
    )
    return result


def apply(snapshot, blockers):
    from . import product_runtime as pr

    ticket = snapshot.get("current_ticket_id")
    historical = []
    recovery_id = f"{str(ticket).replace('.', '-')}-RECOVERY-AUTHORITY"
    for blocker in list(blockers):
        if blocker.get("id") != recovery_id:
            continue
        try:
            projection = pr._load_current_projection_record()
            if projection["ticket_id"] != ticket:
                continue
            record, source = _recovery_source(projection)
            blocker.update(source, code="RECOVERY_AUTHORITY_INVALID", category="execution_recovery")
            if (
                blocker.get("status") == "blocked_by_invalid_recovery_authority"
                and blocker.get("evidence") == "recovery terminal execution identity mismatch"
                and _superseded_workspace_check(snapshot, projection, record)
            ):
                historical.append({**blocker, "blocks_review": False, "historical": True,
                                   "status": "superseded_by_validated_terminal_run"})
                blockers.remove(blocker)
        except (pr.ProductRuntimeError, OSError, ValueError, KeyError, TypeError, sqlite3.Error):
            # Unreadable/corrupt/current recovery authority remains blocking.
            pass
    snapshot["remaining_blockers"] = blockers
    snapshot["blocker_count"] = len(blockers)
    ordered = sorted(blockers, key=lambda b: (str(b.get("id")), str(b.get("status"))))
    snapshot["blocker_inspection"] = {
        "read_only": True, "active_count": len(blockers),
        "items": [_public(b) for b in ordered[:MAX_BLOCKERS]],
        "truncated": len(blockers) > MAX_BLOCKERS,
        "historical_items": [_public(b) for b in historical[:MAX_BLOCKERS]],
    }
    try:
        blocked = pr._review_prepare_workflow_blocker(snapshot) if ticket else ("NO_CURRENT_TICKET", "No current ticket.")
    except (pr.ProductRuntimeError, ValueError, KeyError, TypeError):
        blocked = ("REVIEW_AUTHORITY_UNAVAILABLE", "Current review authority is unavailable.")
    snapshot["review_preparation_eligibility"] = {
        "available": blocked is None, "scope": "workflow_gate",
        "blocker_code": blocked[0] if blocked else None,
        "blocker_detail": blocked[1] if blocked else None,
        "ticket_id": ticket,
        "run_id": (snapshot.get("manual_validation") or {}).get("run_id"),
        "read_only": True, "review_preparation_recorded": False,
    }
    action = snapshot.get("next_action") or {}
    if ticket and blocked and action.get("id") == pr.governed_ticket_lifecycle_action_ids(ticket)["review_prepare"]:
        snapshot.update(readiness="review_prerequisite_blocked", review_state="blocked_review_prerequisite", next_action={
            "id": f"RESOLVE_{str(ticket).replace('.', '_')}_REVIEW_BLOCKER",
            "target_ticket_id": ticket, "label": "Resolve the current review prerequisite.",
            "blocker_code": blocked[0], "required_human_action": "resolve_review_prerequisite",
        })
