"""Read-compatible recovery history: immutable records, one ticket-level head."""

import hashlib
import json
import sqlite3
from pathlib import Path


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
