"""Read-compatible recovery history: immutable records, one ticket-level head."""

import hashlib
import json
import sqlite3
from pathlib import Path


def apply_workflow(snapshot, blockers):
    """Publish current recovery authority after all historical overlays."""
    from hermes_cli import kanban_db as kb
    from hermes_cli.agent_platform import product_runtime as pr

    action = snapshot.get("next_action") or {}
    ticket = snapshot.get("current_ticket_id")
    if not ticket:
        return
    actions = pr.governed_ticket_lifecycle_action_ids(ticket)
    if action.get("id") not in {actions["execution_recovery"], actions["retry_start"]}:
        return
    retry = action["id"] == actions["retry_start"]
    try:
        projection = pr._load_current_projection_record()
        if projection["ticket_id"] != ticket:
            raise pr.ProductRuntimeConflict("recovery projection targets a different ticket")
        pr._validate_execution_start_authority(projection)
        path = kb.kanban_db_path(board=projection["kanban_board_slug"])
        with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as conn:
            conn.row_factory = sqlite3.Row
            task = kb.get_task(conn, projection["kanban_task_id"])
            runs = kb.list_runs(conn, projection["kanban_task_id"])
        allowed_states = {"blocked", "ready"} if retry else {"blocked"}
        if task is None or not runs or task.status not in allowed_states or task.current_run_id is not None:
            raise pr.ProductRuntimeConflict("recovery requires a terminal blocked task")
        if any(pr._execution_is_active(pr._run_dict(item)) for item in runs) or int(snapshot.get("active_execution_count") or 0):
            raise pr.ProductRuntimeConflict("recovery cannot authorize an active execution")
        body = json.loads(task.body or "{}")
        if not isinstance(body, dict) or body.get("WorkPacket_ID") != projection["work_packet_id"] or body.get("WorkPacket_SHA256") != projection["work_packet_SHA256"]:
            raise pr.ProductRuntimeConflict("recovery task WorkPacket binding mismatch")
        run = runs[-1]
        binding = {
            **pr._current_ticket_projection_identity_fields(projection),
            "projection_SHA256": projection["projection_SHA256"],
            "kanban_board_slug": projection["kanban_board_slug"],
            "kanban_task_id": task.id,
            "assignee_profile": projection["assignee_profile"],
            "kanban_task_workspace_path": task.workspace_path,
            "latest_failed_run_id": run.id,
            "latest_failed_run_status": run.status,
            "latest_failed_run_outcome": run.outcome,
            "latest_failed_run_ended_at": run.ended_at,
            "observed_attempt_count": len(runs),
        }
        binding["terminal_run_SHA256"] = terminal_identity(binding)
        record = pr.load_current_ticket_recovery_action_record(projection_record=projection)
        if retry:
            if record is None or record["latest_failed_run_id"] != run.id:
                raise pr.ProductRuntimeConflict("retry requires this failed run's recovery decision")
            binding["recovery_action_SHA256"] = record["recovery_action_SHA256"]
            text = f"I explicitly authorize the retry execution of {ticket} after failed run {run.id}."
            tool = "start_current_ticket_execution"
        else:
            text = (
                f"I explicitly authorize the governed recovery action {action['id']} "
                f"for ticket {ticket}, run {run.id}. Recovery only. "
                "Do not start a retry or a new execution as part of this action."
            )
            pr._validate_execution_recovery_authorization_text(
                text, current_ticket_id=ticket, current_run_id=run.id,
            )
            tool = "recover_current_ticket_execution"
        digest = hashlib.sha256(json.dumps(binding, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        snapshot["next_action"] = {
            **action,
            "tool": tool,
            "run_id": run.id,
            "required_human_action": "retry_start_authorization" if retry else "execution_recovery_authorization",
            "required_human_authorization_text": text,
            "required_human_authorization_text_SHA256": hashlib.sha256(text.encode()).hexdigest(),
            "recovery_binding": binding,
            "recovery_binding_SHA256": digest,
            "recovery_action_SHA256": binding.get("recovery_action_SHA256"),
            "failed_run": pr._run_dict(run),
            "arguments": {
                "project_id": projection["project_id"],
                "ticket_id": ticket,
                "next_action_id": action["id"],
                "human_authorization_text": text,
            },
            "separate_retry_start_authorization_required": True,
            "dispatch_performed": False,
        }
        snapshot["human_action_required"] = True
        historical = snapshot.get("retry_start_authority") or {}
        if historical and historical.get("kanban_task_id") != task.id:
            snapshot.pop("retry_start_authority", None)
    except (pr.ProductRuntimeError, OSError, sqlite3.Error, ValueError, KeyError, TypeError) as exc:
        blocker = {"id": "RECOVERY-AUTHORITY-INVALID", "status": "blocked_by_invalid_recovery_authority", "evidence": str(exc)}
        blockers.append(blocker)
        snapshot.update({
            "recovery_state": "blocked_invalid_recovery_authority",
            "runtime_execution_authorized": False,
            "next_action": {
                "id": "RESOLVE_RECOVERY_AUTHORITY_BLOCKER",
                "target_ticket_id": ticket,
                "label": "Resolve invalid current execution-recovery authority.",
                "blocker": blocker,
            },
        })


def _projection(record, current):
    from hermes_cli.agent_platform import product_runtime as pr
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    from hermes_cli.agent_platform.workflow import (
        work_packet_kanban_projection as kanban,
    )

    if record.get("projection_SHA256") == current.get("projection_SHA256"):
        return current
    try:
        generation = bridge.load_generation_record(ticket_id=current["ticket_id"])
        historical = json.loads(
            kanban._historical_projection_path(record).read_text(encoding="utf-8")
        )
        if (
            record.get("ticket_id") != current["ticket_id"]
            or generation is None
            or not kanban._projection_is_superseded(historical, generation)
        ):
            raise ValueError("unproven historical recovery lineage")
        kanban.validate_kanban_projection_record(
            current, ticket_id=current["ticket_id"], generation_record=generation
        )
        return historical
    except (
        OSError,
        ValueError,
        bridge.TicketArchitectBridgeError,
        kanban.WorkPacketKanbanProjectionError,
    ) as exc:
        raise pr.ProductRuntimeConflict(
            "recovery historical projection is invalid"
        ) from exc


def terminal_identity(record):
    """Bind a record to its own persisted terminal run without reconciliation."""
    from hermes_cli import kanban_db as kb
    from hermes_cli.agent_platform import product_runtime as pr

    path = kb.kanban_db_path(board=record["kanban_board_slug"])
    try:
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            run = kb.get_run(conn, int(record["latest_failed_run_id"]))
            task = kb.get_task(conn, record["kanban_task_id"])
            runs = kb.list_runs(conn, record["kanban_task_id"])
        finally:
            conn.close()
        if (
            run is None
            or task is None
            or run.task_id != task.id
            or run.ended_at is None
            or (run.outcome or run.status) not in pr._GOVERNED_TICKET_FAILURE_OUTCOMES
            or run.profile != record["assignee_profile"]
            or task.workspace_path != record.get("kanban_task_workspace_path")
            or sum(item.id <= run.id for item in runs)
            != record["observed_attempt_count"]
            or any(
                record.get(key) != value
                for key, value in {
                    "latest_failed_run_status": run.status,
                    "latest_failed_run_outcome": run.outcome,
                    "latest_failed_run_ended_at": run.ended_at,
                }.items()
            )
        ):
            raise ValueError("terminal run binding mismatch")
        payload = pr._run_dict(run)
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
    except (sqlite3.Error, OSError, ValueError, KeyError, TypeError) as exc:
        raise pr.ProductRuntimeConflict(
            "recovery terminal execution identity mismatch"
        ) from exc


def _validate(record, current):
    from hermes_cli.agent_platform import product_runtime as pr

    if not isinstance(record, dict):
        raise pr.ProductRuntimeConflict("recovery history record must be an object")
    projection = _projection(record, current)
    pr.validate_p18_9_0_recovery_action_record(record, projection_record=projection)
    digest = terminal_identity(record)
    if record.get("terminal_run_SHA256", digest) != digest:
        raise pr.ProductRuntimeConflict("recovery terminal run digest mismatch")
    return projection


def history(current):
    """Validate every consulted historical authority, including preserved raw bytes."""
    from hermes_cli.agent_platform import product_runtime as pr

    path = pr.recovery_action_history_path_for_ticket(current["ticket_id"])
    if not path.exists():
        return []
    try:
        entries = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for entry in entries:
            record = entry["record"]
            if "record_text" in entry:
                raw = entry["record_text"].encode("utf-8")
                if (
                    hashlib.sha256(raw).hexdigest() != entry.get("record_bytes_SHA256")
                    or json.loads(raw) != record
                ):
                    raise ValueError("historical recovery bytes mismatch")
            _validate(record, current)
        return entries
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise pr.ProductRuntimeConflict("recovery history is invalid") from exc


def resolve(path: Path, current):
    """Do not treat a proven predecessor's record as this projection's authority."""
    from hermes_cli.agent_platform import product_runtime as pr

    entries = history(current)
    try:
        record = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        own_projection = _validate(record, current) if record is not None else None
        cycles = {}
        for candidate in [entry["record"] for entry in entries] + (
            [record] if record else []
        ):
            identity = tuple(
                candidate.get(key)
                for key in (
                    "project_id",
                    "macroproject_id",
                    "ticket_id",
                    "ticket_spec_SHA256",
                    "work_packet_id",
                    "work_packet_SHA256",
                    "projection_SHA256",
                    "kanban_task_id",
                    "latest_failed_run_id",
                )
            )
            digest = candidate["recovery_action_SHA256"]
            if identity in cycles and cycles[identity] != digest:
                raise pr.ProductRuntimeConflict(
                    "ambiguous recovery authority for failed execution"
                )
            cycles[identity] = digest
    except pr.ProductRuntimeConflict:
        raise
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise pr.ProductRuntimeConflict(
            "execution recovery action record is unreadable"
        ) from exc
    if own_projection is not current:
        return None
    return record


def archive_for_replacement(record, current):
    """Archive exact legacy/current bytes before replacement, without duplicate replay."""
    from hermes_cli.agent_platform import product_runtime as pr

    path = pr.recovery_action_record_path_for_ticket(record["ticket_id"])
    resolve(path, current)
    if not path.exists():
        return
    raw = path.read_bytes().decode("utf-8")
    previous = json.loads(raw)
    if previous["recovery_action_SHA256"] == record["recovery_action_SHA256"]:
        return
    fields = (
        "ticket_spec_SHA256",
        "work_packet_SHA256",
        "projection_SHA256",
        "kanban_task_id",
        "latest_failed_run_id",
    )
    if all(previous.get(key) == record.get(key) for key in fields):
        raise pr.ProductRuntimeConflict(
            "recovery authority cannot replace the same failed execution"
        )
    entries = history(current)
    if not any(
        entry["record"]["recovery_action_SHA256"] == previous["recovery_action_SHA256"]
        and entry.get("record_text") == raw
        for entry in entries
    ):
        pr._append_authority_history(
            pr.recovery_action_history_path_for_ticket(record["ticket_id"]),
            previous,
            reason="replaced_by_current_recovery_cycle",
            record_text=raw,
        )
