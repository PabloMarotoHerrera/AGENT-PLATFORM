"""Real correction dispatch and transactional failure boundaries in isolated homes."""

import json
import os
import sqlite3
from pathlib import Path

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import manual_validation_resolution as mr
from tests.hermes_cli import test_c76_manual_validation_resolution as c76
from tests.hermes_cli.test_c81_manual_resolution_projection import (
    completed as completed,
    evidence as evidence,
    failed as failed,
    flow as flow,
    full_contract as full_contract,
    projection_home as projection_home,
    fresh_v2_failure as fresh_v2_failure,
    public_action,
)

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


def files(root):
    return {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    }


@pytest.fixture
def correction(fresh_v2_failure):
    f = fresh_v2_failure
    binding, _ = mr.context(f.p)
    f.current_run = binding["run_id"]
    record = mr.resolve(
        binding=binding,
        decision=mr.IMPLEMENTATION,
        human_authorization_text=mr.consent(binding, mr.IMPLEMENTATION),
        corrective_guidance="Apply the correction from current canonical source.",
    )["resolution"]
    f.start_args = dict(
        ticket_id=f.p["ticket_id"],
        run_id=f.current_run,
        decision_SHA256=record["decision_SHA256"],
        human_authorization_text=mr.start_consent(record),
    )
    f.before_runs = c76.runs(f)
    with kb.connect(board=f.p["kanban_board_slug"]) as conn:
        f.before_task = kb.get_task(conn, f.p["kanban_task_id"])
    f.workspace_before = Path(f.before_task.workspace_path)
    f.old_workspaces = {p: files(p) for p in (f.workspace, f.workspace_before)}
    f.history = {
        mr.path_for(f.p, r): mr.path_for(f.p, r).read_bytes()
        for r in (f.run_id, f.current_run)
    }
    f.source_store = f.home / "agent-platform/source-authority"
    f.source_before = files(f.source_store)
    f.spawned = []
    f.spawn = lambda task, workspace, **kw: (
        f.spawned.append((task, workspace)) or os.getpid()
    )
    return f


def preserved(f):
    assert all(files(p) == before for p, before in f.old_workspaces.items())
    assert all(p.read_bytes() == before for p, before in f.history.items())
    assert c76.runs(f)[: len(f.before_runs)] == f.before_runs


@pytest.mark.parametrize("terminal_status", ["blocked", "triage", "ready"])
def test_requeued_terminal_correction(correction):
    f = correction
    result = mr.start(**f.start_args, spawn_fn=f.spawn)
    assert result["execution_started"], result
    assert len(f.spawned) == 1 and len(c76.runs(f)) == len(f.before_runs) + 1
    assert mr.current(f.p) is None
    assert pr.build_workflow_control_snapshot()["execution_state"] == "active_executions"
    assert result["kanban_run_id"] > f.current_run
    workspace = Path(result["workspace_path"])
    assert workspace not in f.old_workspaces
    assert workspace.name.endswith(f"-attempt-{len(f.before_runs) + 1}")
    source = json.loads(
        Path(result["durable_source_authority_reference"]["authority_path"]).read_text()
    )
    assert source["run_id"] == result["kanban_run_id"]
    assert source["projection_SHA256"] == f.p["projection_SHA256"]
    assert result["durable_source_authority_validated_before_worker_execution"]
    assert (
        "synthetic = true"
        in (workspace / "2_products/pepper-agent/web/src/App.tsx").read_text()
    )
    assert mr.start(**f.start_args, spawn_fn=f.spawn)["idempotent_replay"]
    assert len(f.spawned) == 1
    preserved(f)


@pytest.mark.parametrize("terminal_status", ["triage"])
@pytest.mark.parametrize(
    "boundary", ["provider", "insert_run", "source", "spawn", "spawn_typeerror"]
)
def test_failure_boundaries(correction, monkeypatch, boundary):
    f = correction
    auth_path = mr.path_for(f.p, f.current_run, "start")
    with monkeypatch.context() as patch:
        if boundary == "provider":
            patch.setattr(pr, "_executor_provider_readiness", lambda p: {"ok": False})
        elif boundary == "insert_run":
            with kb.connect(board=f.p["kanban_board_slug"]) as conn:
                conn.execute(
                    "CREATE TRIGGER c82_insert BEFORE INSERT ON task_runs BEGIN SELECT RAISE(ABORT, 'c82 insert failure'); END"
                )
                conn.commit()
        elif boundary == "source":

            def source_failure(**kw):
                raise RuntimeError("c82 source failure")

            patch.setattr(
                pr, "_prepare_governed_source_authority_for_dispatch", source_failure
            )
        spawn = f.spawn
        if boundary.startswith("spawn"):

            def spawn(task, workspace, **kw):
                f.spawned.append((task, workspace))
                raise (TypeError if boundary == "spawn_typeerror" else RuntimeError)(
                    "c82 spawn failure"
                )

        if boundary in ("provider", "insert_run"):
            with pytest.raises((pr.ProductRuntimeConflict, sqlite3.IntegrityError)):
                mr.start(**f.start_args, spawn_fn=spawn)
        else:
            result = mr.start(**f.start_args, spawn_fn=spawn)
            assert not result["execution_started"]
    current_runs = c76.runs(f)
    assert auth_path.exists() == (boundary != "provider")
    with kb.connect(board=f.p["kanban_board_slug"]) as conn:
        task = kb.get_task(conn, f.p["kanban_task_id"])
        assert not task.current_run_id and not task.worker_pid and not task.claim_lock
        if boundary == "insert_run":
            conn.execute("DROP TRIGGER c82_insert")
            conn.commit()
    workflow, action = public_action()
    assert not workflow.get("active_execution_count")
    assert (
        action["id"]
        != pr.resolve_current_ticket_lifecycle_binding(
            projection_record=f.p
        ).execution_start_next_action_id
    )
    if boundary in ("provider", "insert_run"):
        assert current_runs == f.before_runs and not f.spawned
        assert files(f.source_store) == f.source_before
        assert task.status == f.before_task.status
        assert task.workspace_path == f.before_task.workspace_path
        assert workflow["workflow_status"] == mr.STATE
        assert not (
            kb.workspaces_root(board=f.p["kanban_board_slug"])
            / f"{task.id}-attempt-{len(f.before_runs) + 1}"
        ).exists()
        retry = mr.start(**f.start_args, spawn_fn=f.spawn)
        assert retry["execution_started"] and len(f.spawned) == 1
    else:
        assert len(current_runs) == len(f.before_runs) + 1
        assert task.status == "blocked"
        assert Path(task.workspace_path) not in f.old_workspaces
        assert len(f.spawned) == int(boundary.startswith("spawn"))
        assert mr.start(**f.start_args, spawn_fn=f.spawn)["idempotent_replay"]
        assert c76.runs(f) == current_runs
        assert len(f.spawned) == int(boundary.startswith("spawn"))
    preserved(f)


@pytest.mark.parametrize("terminal_status", ["triage"])
def test_workspace_collision_fails_before_run(correction):
    f = correction
    destination = (
        kb.workspaces_root(board=f.p["kanban_board_slug"])
        / f"{f.p['kanban_task_id']}-attempt-{len(f.before_runs) + 1}"
    )
    destination.mkdir()
    (destination / "immutable.txt").write_text("Do not reuse this existing directory.")
    before = files(destination)
    result = mr.start(**f.start_args, spawn_fn=f.spawn)
    assert result["blocker_code"] == "FRESH_EXECUTION_WORKSPACE_CONFLICT"
    assert not f.spawned and c76.runs(f) == f.before_runs
    assert files(destination) == before
    assert public_action()[1]["retry_same_authority"]
    preserved(f)


@pytest.mark.parametrize("terminal_status", ["triage"])
@pytest.mark.parametrize("invalid_status", ["done", "running", "todo", "archived"])
def test_inconsistent_terminal_task_fails_closed(correction, invalid_status):
    f = correction
    with kb.connect(board=f.p["kanban_board_slug"]) as conn:
        conn.execute(
            "UPDATE tasks SET status=? WHERE id=?",
            (invalid_status, f.p["kanban_task_id"]),
        )
        conn.commit()
    with pytest.raises((pr.ProductRuntimeError, ValueError)):
        mr.start(**f.start_args, spawn_fn=f.spawn)
    assert c76.runs(f) == f.before_runs and not f.spawned
    preserved(f)


def test_completed_done_candidate_is_supported(failed, monkeypatch, evidence):
    # A genuinely completed done/done/completed tuple remains legal; changing
    # only a blocked terminal candidate's task status to done is not completion.
    c76.test_fresh_dispatch(failed, monkeypatch, evidence, False)


@pytest.mark.parametrize("terminal_status", ["triage"])
def test_failed_rearm_retains_same_start_authority(correction, monkeypatch):
    f = correction
    # SQLite itself ignores this UPDATE: execute the real rearm path, no fake blocker.
    with kb.connect(board=f.p["kanban_board_slug"]) as conn:
        conn.execute(
            "CREATE TRIGGER c82_rearm BEFORE UPDATE OF status ON tasks WHEN NEW.status='ready' BEGIN SELECT RAISE(IGNORE); END"
        )
        conn.commit()
    result = mr.start(**f.start_args, spawn_fn=f.spawn)
    assert result["blocker_code"] == "KANBAN_TERMINAL_REARM_FAILED"
    assert result["execution_authorization_recorded"]
    assert not result["dispatch_performed"] and not f.spawned
    assert c76.runs(f) == f.before_runs
    assert files(f.source_store) == f.source_before
    assert not (
        kb.workspaces_root(board=f.p["kanban_board_slug"])
        / f"{f.p['kanban_task_id']}-attempt-{len(f.before_runs)+1}"
    ).exists()
    assert mr.correction.read(mr.path_for(f.p, f.current_run, "result")) is None
    auth_path = mr.path_for(f.p, f.current_run, "start")
    auth_bytes = auth_path.read_bytes()
    again = mr.start(**f.start_args, spawn_fn=f.spawn)
    assert again["blocker_code"] == "KANBAN_TERMINAL_REARM_FAILED"
    assert auth_path.read_bytes() == auth_bytes
    assert c76.runs(f) == f.before_runs and not f.spawned
    workflow, action = public_action()
    assert workflow["workflow_status"] == mr.STATE
    assert (
        action["required_human_authorization_text"]
        == f.start_args["human_authorization_text"]
    )
    assert action["retry_same_authority"] is True
    assert (
        action["corrective_start_authority_SHA256"]
        == json.loads(auth_bytes)["decision_SHA256"]
    )
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.start_current_ticket_execution(
            human_authorization_text=f"Start {f.p['ticket_id']} execution now",
            ticket_id=f.p["ticket_id"],
            spawn_fn=f.spawn,
        )
    with monkeypatch.context() as patch:
        patch.setattr(
            pr, "build_workflow_control_snapshot", lambda: {"workflow_status": "queued"}
        )
        with pytest.raises(pr.ProductRuntimeConflict, match="run-bound"):
            pr.start_current_ticket_execution(
                human_authorization_text=f"Start {f.p['ticket_id']} execution now",
                ticket_id=f.p["ticket_id"],
                spawn_fn=f.spawn,
            )
    damaged = json.loads(auth_bytes)
    damaged["resolution_SHA256"] = "0" * 64
    damaged["decision_SHA256"] = mr.ev.digest({
        k: v for k, v in damaged.items() if k != "decision_SHA256"
    })
    auth_path.write_text(json.dumps(damaged))
    workflow, action = public_action()
    assert action is None and workflow["remaining_blockers"]
    with pytest.raises(pr.ProductRuntimeConflict):
        mr.start(**f.start_args, spawn_fn=f.spawn)
    auth_path.write_bytes(auth_bytes)
    with kb.connect(board=f.p["kanban_board_slug"]) as conn:
        conn.execute("DROP TRIGGER c82_rearm")
        conn.commit()
    result = mr.start(**f.start_args, spawn_fn=f.spawn)
    assert result["execution_started"] and len(f.spawned) == 1
    assert auth_path.read_bytes() == auth_bytes
    assert mr.start(**f.start_args, spawn_fn=f.spawn)["idempotent_replay"]
    assert len(c76.runs(f)) == len(f.before_runs) + 1 and len(f.spawned) == 1
    preserved(f)


@pytest.mark.parametrize("terminal_status", ["triage"])
def test_workspace_created_after_claim_is_not_reused(correction, monkeypatch):
    f = correction
    original = pr._claim_terminal_done_review_revision_task
    occupied = []

    def claim(*args, **kwargs):
        task, info = original(*args, **kwargs)
        assert task is not None
        path = Path(task.workspace_path)
        path.mkdir()
        (path / "existing.txt").write_text("Other owner; never materialize here.")
        occupied.append((path, files(path)))
        return task, info

    monkeypatch.setattr(pr, "_claim_terminal_done_review_revision_task", claim)
    result = mr.start(**f.start_args, spawn_fn=f.spawn)
    assert result["blocker_code"] == "WORKSPACE_POLICY_GAP"
    assert not f.spawned and len(c76.runs(f)) == len(f.before_runs) + 1
    assert files(occupied[0][0]) == occupied[0][1]
    assert mr.start(**f.start_args, spawn_fn=f.spawn)["idempotent_replay"]
    assert len(occupied) == 1 and not f.spawned
    preserved(f)
