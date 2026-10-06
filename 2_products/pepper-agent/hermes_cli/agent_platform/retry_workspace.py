"""Retry workspace allocations and the explicitly authorized C85 historical read."""

import json
from pathlib import Path

POLICY = "pepper-fresh-retry-workspace-v1"
# Human C85-R1 exception: this historical execution only, never a future run.
LEGACY = ("PEPPER", "P18.9.12", "t_f501fd7f", 43)


def freshness(task):
    body = json.loads(task.body or "{}")
    reused = body.get("retry_attempt_number") is not None and body.get(
        "retry_attempt_number"
    ) != body.get("fresh_execution_attempt_number")
    return {
        "workspace_freshness": "historical_reused_workspace"
        if reused
        else "fresh_retry_workspace"
        if body.get("retry_workspace_allocation")
        else "task_workspace",
        "historical_workspace_reuse": reused,
    }


def historical(p, task, run, runs, workspace):
    from . import execution_evidence as ev, product_runtime as pr

    if (p["project_id"], p["ticket_id"], task.id, run.id) != LEGACY:
        raise ValueError(
            "workspace attempt mismatch is not an authorized historical retry"
        )
    body = json.loads(task.body or "{}")
    if (
        len(runs) != 6
        or runs[-1].id != run.id
        or runs[-2].id != 42
        or body.get("fresh_execution_attempt_number") != 5
        or body.get("retry_attempt_number") != 6
        or body.get("retry_identity_model") != "same_kanban_task_new_run"
        or body.get("retry_workspace_allocation") is not None
        or body.get("fresh_execution_workspace_path") != str(workspace)
        or task.current_run_id
        or task.worker_pid
        or task.claim_lock
        or any(pr._execution_is_active(pr._run_dict(r)) for r in runs)
    ):
        raise ValueError("historical retry workspace identity mismatch")
    recovery = pr.load_current_ticket_recovery_action_record(projection_record=p)
    retry = pr.load_current_ticket_retry_start_record(
        projection_record=p, recovery_record=recovery
    )
    if (
        not recovery
        or not retry
        or recovery["latest_failed_run_id"] != runs[-2].id
        or recovery["kanban_task_workspace_path"] != str(workspace)
        or body.get("retry_authority_SHA256") != recovery["recovery_action_SHA256"]
        or retry.get("start_status") != "authorized_pending_dispatch"
        or retry.get("kanban_run_id") is not None
        or retry.get("execution_started") is not False
        or retry.get("previous_attempt_count") != 5
        or retry.get("next_attempt_number") != 6
    ):
        raise ValueError("historical retry recovery/authorization chain mismatch")
    with ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"])) as conn:
        if conn.execute("SELECT COUNT(*) FROM tasks WHERE status='running'").fetchone()[
            0
        ]:
            raise ValueError("historical inspection requires no active execution")
        events = [
            dict(r)
            for r in conn.execute(
                "SELECT kind,payload FROM task_events WHERE task_id=? AND kind IN ('retry_prepared','claimed')",
                (task.id,),
            )
        ]
    prepared = any(
        e["kind"] == "retry_prepared"
        and json.loads(e["payload"] or "{}").get("recovery_action_SHA256")
        == recovery["recovery_action_SHA256"]
        and json.loads(e["payload"] or "{}").get("next_attempt_number") == 6
        for e in events
    )
    claimed = any(
        e["kind"] == "claimed"
        and json.loads(e["payload"] or "{}").get("run_id") == run.id
        for e in events
    )
    if not prepared or not claimed:
        raise ValueError("historical retry dispatch evidence missing")
    authority = ev.source(p, run)
    observed = ev.candidate(p, run, workspace, authority)
    if not observed.get("available") or not workspace.is_dir():
        raise ValueError("historical candidate/source identity unavailable")


def allocation_valid(value):
    from .execution_evidence import digest

    return (
        isinstance(value, dict)
        and value.get("policy_id") == POLICY
        and value.get("SHA256")
        == digest({k: v for k, v in value.items() if k != "SHA256"})
    )


def unblock_for_allocation(conn, task):
    """Keep readiness and workspace publication in the caller's single transaction."""
    from hermes_cli import kanban_db as kb

    if task.current_run_id or task.claim_lock or task.worker_pid:
        return False
    if conn.execute(
        "SELECT 1 FROM task_links l JOIN tasks p ON p.id=l.parent_id "
        "WHERE l.child_id=? AND p.status!='done' LIMIT 1",
        (task.id,),
    ).fetchone():
        return False
    changed = conn.execute(
        "UPDATE tasks SET status='ready', consecutive_failures=0, last_failure_error=NULL "
        "WHERE id=? AND status='blocked'",
        (task.id,),
    ).rowcount
    if changed:
        kb._append_event(conn, task.id, "unblocked")
    return changed == 1


def prepare(conn, task, p, recovery):
    from hermes_cli import kanban_db as kb
    from .execution_evidence import digest, safe_path

    task = kb.get_task(conn, task.id)
    if (
        task is None
        or task.workspace_kind != "scratch"
        or task.status != "ready"
        or task.current_run_id
        or task.claim_lock
        or task.worker_pid
    ):
        raise ValueError("retry workspace reservation requires an unclaimed ready task")
    runs = kb.list_runs(conn, task.id)
    attempt = len(runs) + 1
    if (
        not runs
        or runs[-1].id != recovery["latest_failed_run_id"]
        or attempt != recovery["next_attempt_number"]
    ):
        raise ValueError("retry workspace attempt authority mismatch")
    body = json.loads(task.body or "{}")
    existing = body.get("retry_workspace_allocation")
    if (
        allocation_valid(existing)
        and existing["recovery_action_SHA256"] == recovery["recovery_action_SHA256"]
    ):
        verify(conn, task, claimed=False)
        return body
    root = kb.workspaces_root(board=p["kanban_board_slug"])
    workspace = root / f"{task.id}-attempt-{attempt}"
    safe_path(workspace, root, missing=True)
    if str(workspace) == task.workspace_path:
        raise ValueError("retry workspace must differ from previous workspace")
    value = {
        "policy_id": POLICY,
        "task_id": task.id,
        "board": p["kanban_board_slug"],
        "projection_SHA256": p["projection_SHA256"],
        "recovery_action_SHA256": recovery["recovery_action_SHA256"],
        "previous_run_id": runs[-1].id,
        "previous_workspace": task.workspace_path,
        "attempt": attempt,
        "workspace": str(workspace),
    }
    value["SHA256"] = digest(value)
    # Exclusive reservation: an existing directory is never reused or cleared.
    workspace.mkdir(exist_ok=False)
    body.update(
        retry_workspace_allocation=value,
        fresh_execution_requested=True,
        fresh_execution_attempt_number=attempt,
        fresh_execution_workspace_path=str(workspace),
        fresh_execution_request_SHA256=value["SHA256"],
    )
    conn.execute(
        "UPDATE tasks SET workspace_path=? WHERE id=?", (str(workspace), task.id)
    )
    kb._append_event(conn, task.id, "retry_workspace_allocated", value)
    return body


def verify(conn, task, *, claimed=True):
    from hermes_cli import kanban_db as kb
    from .execution_evidence import safe_path

    body = json.loads(task.body or "{}")
    value = body.get("retry_workspace_allocation")
    if not allocation_valid(value):
        raise ValueError("retry workspace allocation identity mismatch")
    root = kb.workspaces_root(board=value["board"])
    safe_path(value["workspace"], root)
    runs = kb.list_runs(conn, task.id)
    if (
        not allocation_valid(value)
        or value["task_id"] != task.id
        or value["attempt"] != len(runs) + (0 if claimed else 1)
        or value["workspace"] != task.workspace_path
        or body.get("fresh_execution_workspace_path") != task.workspace_path
        or body.get("fresh_execution_attempt_number") != value["attempt"]
        or body.get("fresh_execution_request_SHA256") != value["SHA256"]
        or value["workspace"] == value["previous_workspace"]
        or Path(value["workspace"]) != root / f"{task.id}-attempt-{value['attempt']}"
        or body.get("retry_authority_SHA256") != value["recovery_action_SHA256"]
        or not Path(value["workspace"]).is_dir()
        or not any(
            json.loads(r[0]) == value
            for r in conn.execute(
                "SELECT payload FROM task_events WHERE task_id=? AND kind='retry_workspace_allocated'",
                (task.id,),
            )
        )
    ):
        raise ValueError("retry workspace allocation identity mismatch")
    return value


def preserves_previous(conn, task, record):
    """A new allocation cannot invalidate its predecessor's recovery record."""
    return any(
        allocation_valid(v := json.loads(row[0]))
        and v["task_id"] == task.id
        and v["previous_run_id"] == record["latest_failed_run_id"]
        and v["previous_workspace"] == record.get("kanban_task_workspace_path")
        and v["recovery_action_SHA256"] == record["recovery_action_SHA256"]
        for row in conn.execute(
            "SELECT payload FROM task_events WHERE task_id=? AND kind='retry_workspace_allocated'",
            (task.id,),
        )
    )
