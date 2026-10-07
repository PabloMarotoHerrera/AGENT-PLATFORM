"""Historical recovery stays historical across real isolated review transitions."""

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr, review_readiness as readiness
from tests.hermes_cli.test_c88_review_readiness import (
    historical as historical, flow as flow, projection_home as projection_home, readers,
)
from tools import pepper_workflow_tools as tools
from tests.hermes_cli.test_c59_manual_validation_authority import _args

DECISION_OVERLAY = pr._current_ticket_review_decision_overlay


def compact():
    return json.loads(tools._get_workflow_control({"blockers_only": True}))


def assert_historical(output, f):
    inspection = output["blocker_inspection"]
    assert inspection["active_count"] == 0
    item, = inspection["historical_items"]
    assert item["source_run_id"] == f.old_run["id"]
    assert item["historical"] and not item["blocks_review"]


@pytest.fixture
def prepared(historical, monkeypatch):
    return prepare(historical, monkeypatch)


def prepare(f, monkeypatch):
    # The shared synthetic terminal fixture replaces the start overlay. Restore
    # real recovery production and decision projection around that terminal,
    # keeping the real persisted recovery, DB, prepare and decision authorities.
    terminal_overlay = pr._apply_current_projection_execution_lifecycle_overlay
    def lifecycle(overlay, projection):
        terminal_overlay(overlay, projection)
        _, blocker = pr._p18_9_0_recovery_overlay(projection, start_overlay=overlay)
        return blocker
    monkeypatch.setattr(pr, "_apply_current_projection_execution_lifecycle_overlay", lifecycle)
    monkeypatch.setattr(pr, "_current_ticket_review_decision_overlay", DECISION_OVERLAY)
    assert_historical(compact(), f)
    result = pr.prepare_current_ticket_review()
    assert result["review_preparation_recorded"]
    f.prepared_path = pr.review_prepare_record_path_for_ticket(f.ticket_id)
    f.prepared_bytes = f.prepared_path.read_bytes()
    return f


def test_real_prepare_transition_is_stable_and_all_readers_agree(prepared, projection_home, monkeypatch):
    f = prepared
    def files():
        return {str(p): p.read_bytes() for p in Path(projection_home).rglob("*") if p.is_file()}
    before = files()
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: pytest.fail("read inspection must not invoke Git or materialization commands"))
    first = compact()
    assert compact() == first
    for output in [first, *readers()]:
        assert_historical(output, f)
        assert output["next_action"]["id"] == pr._review_decision_request_action_id(f.ticket_id)
        assert output["review_decision_eligibility"]["available"]
        # Preparation has finished. Its pre-prepare action is no longer eligible.
        assert not output["review_preparation_eligibility"]["available"]
        assert output["review_preparation_eligibility"]["blocker_code"] != "WORKFLOW_BLOCKER_PRESENT"
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["review_state"] == "prepared_pending_human_acceptance"
    assert snapshot["blocker_count"] == 0
    assert not pr.review_decision_record_path_for_ticket(f.ticket_id).exists()
    assert f.prepared_path.read_bytes() == f.prepared_bytes
    assert f.recovery_path.read_bytes() == f.recovery_bytes
    assert files() == before


@pytest.mark.parametrize("decision", ["accept", "reject"])
def test_later_human_decision_does_not_reactivate_old_recovery(historical, monkeypatch, decision):
    f = historical
    # A nonempty candidate follows accept/reject without the separate no-op
    # successor-authority contract; manual evidence is rebound before prepare.
    f.completion["candidate_changes_reference"] = {
        "available": True, "files_changed": 1,
        "files": [{"path": "src/example.py", "change": "modified", "workspace_sha256": "b" * 64}],
    }
    f.completion["terminal_outcome_class"] = "validated_review_required"
    f.completion["kanban_completion_result_SHA256"] = pr._kanban_completion_result_digest(f.completion)
    pr.attest_current_ticket_manual_validation(**_args(f))
    prepare(f, monkeypatch)
    result = pr.submit_current_ticket_review_decision(decision=decision, feedback="Isolated human fixture decision.", reviewed_run_id=f.completion["run_id"])
    assert result["review_decision"] == decision
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["review_state"] == ("accepted" if decision == "accept" else "rejected")
    assert_historical(snapshot, f)
    assert f.prepared_path.read_bytes() == f.prepared_bytes
    assert f.recovery_path.read_bytes() == f.recovery_bytes


@pytest.mark.parametrize("mutation", [
    "current_recovery", "corrupt_head", "corrupt_history", "changed_failed_run",
    "workpacket", "prepared_run", "package_integrity", "candidate_change", "active_run",
])
def test_changed_durable_authority_fails_closed(prepared, mutation):
    f = prepared
    if mutation in {"current_recovery", "corrupt_head"}:
        record = json.loads(f.recovery_bytes)
        record["latest_failed_run_id"] = f.completion["run_id"]
        if mutation == "current_recovery":
            record["recovery_action_SHA256"] = pr._recovery_action_record_digest(record)
        f.recovery_path.write_text(json.dumps(record))
    elif mutation == "corrupt_history":
        pr.recovery_action_history_path_for_ticket(f.ticket_id).write_text("{}\n")
    elif mutation in {"changed_failed_run", "active_run"}:
        with kb.connect(board=f.projection_record["kanban_board_slug"]) as conn:
            if mutation == "changed_failed_run":
                conn.execute("UPDATE task_runs SET outcome='completed' WHERE id=?", (f.old_run["id"],))
            else:
                newer = f.completion["run_id"] + 1
                conn.execute("INSERT INTO task_runs (id,task_id,profile,status,started_at) VALUES (?,?,?,'running',?)", (
                    newer, f.projection_record["kanban_task_id"], "implementation_product", f.completion["run_ended_at"] + 1,
                ))
                conn.execute("UPDATE tasks SET current_run_id=?,status='running',worker_pid=? WHERE id=?", (
                    newer, os.getpid(), f.projection_record["kanban_task_id"],
                ))
            conn.commit()
    elif mutation in {"workpacket", "prepared_run", "package_integrity"}:
        record = json.loads(f.prepared_bytes)
        key = {"workpacket": "work_packet_SHA256", "prepared_run": "successful_run_id", "package_integrity": "review_package_SHA256"}[mutation]
        record[key] = f.old_run["id"] if mutation == "prepared_run" else "a" * 64
        record["review_prepare_action_SHA256"] = pr._review_prepare_record_digest(record)
        f.prepared_path.write_text(json.dumps(record))
    elif mutation == "candidate_change":
        f.completion["candidate_changes_reference"] = {"available": True, "candidate_SHA256": "a" * 64}
        f.completion["kanban_completion_result_SHA256"] = pr._kanban_completion_result_digest(f.completion)
    snapshot = pr.build_workflow_control_snapshot()
    readiness.apply(snapshot, [deepcopy(f.blocker), *snapshot["remaining_blockers"]])
    assert snapshot["blocker_inspection"]["historical_items"] == []
    assert snapshot["blocker_count"] > 0
    assert readiness.prepared_review_decision_blocker(snapshot, f.projection_record) is not None
    with pytest.raises(pr.ProductRuntimeError):
        pr.submit_current_ticket_review_decision(decision="reject", feedback="Must be blocked.", reviewed_run_id=f.completion["run_id"])
    assert not pr.review_decision_record_path_for_ticket(f.ticket_id).exists()


@pytest.mark.parametrize("change", [
    {"recovery_state": "recovery_required"},
    {"manual_validation": {"human_action_required": True}},
    {"pending_ticket_approval_count": 1},
    {"active_execution_count": 1},
    {"validation_contract_satisfied": False},
])
def test_current_prerequisites_block_prepared_decision(prepared, monkeypatch, change):
    f = prepared
    snapshot = pr.build_workflow_control_snapshot()
    snapshot.update(change)
    readiness.apply(snapshot, [deepcopy(f.blocker)])
    assert snapshot["blocker_count"] == 1
    assert not snapshot["review_decision_eligibility"]["available"]
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: deepcopy(snapshot))
    for output in readers():
        assert not output["review_decision_eligibility"]["available"]
        assert output["next_action"]["id"] != pr._review_decision_request_action_id(f.ticket_id)
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.submit_current_ticket_review_decision(decision="reject", feedback="Must be blocked.")
    assert not pr.review_decision_record_path_for_ticket(f.ticket_id).exists()


def test_independent_technical_blocker_survives_historical_classification(prepared, monkeypatch):
    f = prepared
    snapshot = pr.build_workflow_control_snapshot()
    readiness.apply(snapshot, [deepcopy(f.blocker), {"id": "TECHNICAL", "status": "blocked_current"}])
    assert snapshot["blocker_count"] == 1
    assert snapshot["blocker_inspection"]["historical_items"][0]["historical"]
    assert snapshot["blocker_inspection"]["items"][0]["blocker_id"] == "TECHNICAL"
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: deepcopy(snapshot))
    with pytest.raises(pr.ProductRuntimeConflict, match="WORKFLOW_BLOCKER_PRESENT"):
        pr.submit_current_ticket_review_decision(decision="reject", feedback="Must be blocked.")
    assert not pr.review_decision_record_path_for_ticket(f.ticket_id).exists()
