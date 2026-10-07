"""Current review gates and historical recovery, using isolated durable fixtures."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr, review_readiness as readiness
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures
from tests.hermes_cli.test_c59_manual_validation_authority import terminal as terminal, _args
from tests.hermes_cli.test_c65_retry_material_revision import flow as flow, projection_home as projection_home
from tools import pepper_workflow_tools as tools


@pytest.fixture
def ready(terminal):
    fixtures._record_c19_zero_change_attestation(terminal)
    pr.attest_current_ticket_manual_validation(**_args(terminal))
    return terminal


def readers():
    return [json.loads(fn({})) for fn in (
        tools._get_workflow_control, tools._get_review_status,
        tools._get_execution_status, tools._get_next_action,
    )]


def test_validated_candidate_has_consistent_public_gates_and_prepares(ready):
    for output in readers():
        assert output["review_preparation_eligibility"]["available"] is True
        assert output["next_action"]["id"] == pr.governed_ticket_lifecycle_action_ids(ready.ticket_id)["review_prepare"]
        assert output["blocker_inspection"]["active_count"] == 0
    result = pr.prepare_current_ticket_review()
    assert result["review_preparation_recorded"] is True
    assert not pr.review_decision_record_path_for_ticket(ready.ticket_id).exists()


def test_pending_validation_blocks_without_autoattestation(terminal):
    fixtures._record_c19_zero_change_attestation(terminal)
    for output in readers():
        assert not output["review_preparation_eligibility"]["available"]
        assert output["manual_validation"]["items"][0]["status"] == "pending"
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]


@pytest.mark.parametrize("change", [
    {"active_execution_count": 1},
    {"recovery_state": "recovery_required"},
    {"pending_ticket_approval_count": 1},
    {"reviewable_result": False},
    {"validation_contract_satisfied": False},
    {"workflow_status": "blocked_manual_validation_failed"},
    {"manual_validation": {"human_action_required": True}},
])
def test_independent_prerequisites_remain_effective(ready, monkeypatch, change):
    snapshot = pr.build_workflow_control_snapshot()
    snapshot.update(change)
    readiness.apply(snapshot, snapshot["remaining_blockers"])
    assert not snapshot["review_preparation_eligibility"]["available"]
    assert snapshot["next_action"]["id"] != pr.governed_ticket_lifecycle_action_ids(ready.ticket_id)["review_prepare"]
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: deepcopy(snapshot))
    for output in readers():
        assert not output["review_preparation_eligibility"]["available"]
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]


def test_real_technical_blocker_is_visible_and_prevents_prepare(ready, monkeypatch):
    snapshot = pr.build_workflow_control_snapshot()
    blockers = [{"id": "CURRENT-TECHNICAL", "status": "blocked_dependency", "evidence": "Current dependency unavailable", "unrelated_payload": "must not escape"}]
    readiness.apply(snapshot, blockers)
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: deepcopy(snapshot))
    for output in readers():
        assert not output["review_preparation_eligibility"]["available"]
        item = output["blocker_inspection"]["items"][0]
        assert item["blocker_id"] == "CURRENT-TECHNICAL"
        assert item["blocks_review"]
        assert "unrelated_payload" not in item
    result = pr.prepare_current_ticket_review()
    assert result["blocker_code"] == "WORKFLOW_BLOCKER_PRESENT"
    assert not result["review_preparation_recorded"]


def test_candidate_identity_mismatch_still_prevents_prepare(ready):
    ready.completion["run_id"] += 1
    ready.completion["kanban_completion_result_SHA256"] = pr._kanban_completion_result_digest(ready.completion)
    for output in readers():
        assert not output["review_preparation_eligibility"]["available"]
    result = pr.prepare_current_ticket_review()
    assert not result["review_preparation_recorded"]


@pytest.fixture
def historical(flow, monkeypatch):
    """Preserve a real recovery/run, then install a later validated completion."""
    p = {**pr._load_current_projection_record(), "macroproject_title": "Synthetic Revision Macroproject"}
    generation_loader = bridge.load_generation_record
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        old = dict(conn.execute("SELECT * FROM task_runs WHERE id=?", (flow.run_id,)).fetchone())
    monkeypatch.setattr(fixtures, "_c9_projection_record", lambda ticket: p)
    f = fixtures._c18_v2_synthetic_noop_review_ready_fixture(
        monkeypatch, ticket_id=p["ticket_id"],
        completion_mutator=fixtures._c19_legacy_semantic_noop_mutator,
    )
    synthetic_loader = bridge.load_generation_record
    monkeypatch.setattr(bridge, "load_generation_record", lambda **kw: (
        generation_loader(**kw) if kw.get("ticket_id") == p["ticket_id"] else synthetic_loader(**kw)
    ))
    # The common fixture installs the later run. Put the untouched older row
    # back to model one task with successive attempts, not an invented recovery.
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        keys = list(old)
        conn.execute(f"INSERT INTO task_runs ({','.join(keys)}) VALUES ({','.join('?' for _ in keys)})", tuple(old.values()))
        f.completion["run_started_at"] = old["ended_at"] + 1
        f.completion["run_ended_at"] = old["ended_at"] + 5
        conn.execute("UPDATE task_runs SET started_at=?,ended_at=? WHERE id=?", (
            f.completion["run_started_at"], f.completion["run_ended_at"], f.completion["run_id"],
        ))
        conn.commit()
    f.completion["kanban_completion_result_SHA256"] = pr._kanban_completion_result_digest(f.completion)
    f.contract["validation_steps"] = []
    f.contract["work_packet_validation_steps"] = [{
        "validation_id": "V8", "kind": "manual", "required": True,
        "command": None, "command_execution_authorized": False,
        "description": "Confirm the revised candidate.", "expected_result": "Revision incorporated.",
    }]
    f.contract["criteria_revision_SHA256"] = pr._criteria_revision_digest(f.contract)
    f.contract["acceptance_contract_SHA256"] = pr._acceptance_contract_digest(f.contract)
    fixtures._record_c19_zero_change_attestation(f)
    pr.attest_current_ticket_manual_validation(**_args(f))
    f.old_run = old
    f.recovery_path = pr.recovery_action_record_path_for_ticket(f.ticket_id)
    f.recovery_bytes = f.recovery_path.read_bytes()
    f.blocker = {
        "id": f"{f.ticket_id.replace('.', '-')}-RECOVERY-AUTHORITY",
        "status": "blocked_by_invalid_recovery_authority",
        "evidence": "recovery terminal execution identity mismatch",
    }
    return f


def reconcile(f, extra=()):
    snapshot = pr.build_workflow_control_snapshot()
    blockers = [deepcopy(f.blocker), *deepcopy(extra)]
    readiness.apply(snapshot, blockers)
    return snapshot


def test_historical_recovery_cannot_create_circular_gate(historical, monkeypatch):
    f = historical
    record, _ = readiness._recovery_source(f.projection_record)
    assert readiness._superseded_workspace_check(pr.build_workflow_control_snapshot(), f.projection_record, record)
    snapshot = reconcile(f)
    assert snapshot["blocker_count"] == 0
    assert snapshot["review_preparation_eligibility"]["available"]
    item = snapshot["blocker_inspection"]["historical_items"][0]
    assert item["source_run_id"] == f.old_run["id"]
    assert item["integrity_valid"]
    assert not item["blocks_review"]
    assert f.recovery_path.read_bytes() == f.recovery_bytes
    # No review record was needed to clear the projected prerequisite.
    assert not pr.review_prepare_record_path_for_ticket(f.ticket_id).exists()
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: deepcopy(snapshot))
    assert pr.prepare_current_ticket_review()["review_preparation_recorded"]
    assert f.recovery_path.read_bytes() == f.recovery_bytes


@pytest.mark.parametrize("mutation", ["corrupt", "current_run", "wrong_workpacket", "changed_run", "pending_manual", "history_corrupt", "unknown_execution"])
def test_historical_exception_is_narrow_and_fail_closed(historical, mutation):
    f = historical
    if mutation == "corrupt":
        f.recovery_path.write_text("{}")
    elif mutation in {"current_run", "wrong_workpacket"}:
        record = json.loads(f.recovery_bytes)
        record["latest_failed_run_id" if mutation == "current_run" else "work_packet_SHA256"] = f.completion["run_id"] if mutation == "current_run" else "a" * 64
        record["recovery_action_SHA256"] = pr._recovery_action_record_digest(record)
        f.recovery_path.write_text(json.dumps(record))
    elif mutation == "changed_run":
        with kb.connect(board=f.projection_record["kanban_board_slug"]) as conn:
            conn.execute("UPDATE task_runs SET outcome='completed' WHERE id=?", (f.old_run["id"],))
            conn.commit()
    elif mutation == "history_corrupt":
        pr.recovery_action_history_path_for_ticket(f.ticket_id).write_text("{}\n")
    snapshot = pr.build_workflow_control_snapshot()
    if mutation == "pending_manual":
        snapshot["manual_validation"]["human_action_required"] = True
    if mutation == "unknown_execution":
        snapshot["active_execution_count"] = None
    readiness.apply(snapshot, [deepcopy(f.blocker)])
    assert snapshot["blocker_count"] == 1
    assert not snapshot["review_preparation_eligibility"]["available"]


def test_historical_exception_does_not_clear_independent_blocker(historical):
    snapshot = reconcile(historical, [{"id": "INDEPENDENT", "status": "blocked_technical"}])
    assert snapshot["blocker_count"] == 1
    assert snapshot["blocker_inspection"]["items"][0]["blocker_id"] == "INDEPENDENT"
    assert not snapshot["review_preparation_eligibility"]["available"]


def test_inspection_is_bounded_deterministic_and_nonmutating(ready, projection_home, monkeypatch):
    import subprocess
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: pytest.fail("inspection must not run Git or other commands"))
    snapshot = pr.build_workflow_control_snapshot()
    blockers = [{"id": f"B{i:03}", "status": "blocked", "evidence": "x" * 10000, "secret_payload": {"key": "not public"}} for i in range(40)]
    def files():
        return {str(p): p.read_bytes() for p in Path(projection_home).rglob("*") if p.is_file()}
    before = files()
    first, second = deepcopy(snapshot), deepcopy(snapshot)
    readiness.apply(first, deepcopy(blockers))
    readiness.apply(second, deepcopy(blockers))
    assert first == second
    inspection = first["blocker_inspection"]
    assert inspection["truncated"] and inspection["active_count"] == 40
    assert len(inspection["items"]) == readiness.MAX_BLOCKERS
    assert len(json.dumps(inspection)) < 16000
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: deepcopy(first))
    for output in readers():
        assert output["blocker_inspection"] == inspection
    compact = json.loads(tools._get_workflow_control({"blockers_only": True}))
    assert compact["blocker_inspection"] == inspection
    assert len(json.dumps(compact)) < 20000
    assert "workflow_control" not in compact
    assert files() == before
    assert not pr.review_prepare_record_path_for_ticket(ready.ticket_id).exists()
    assert not pr.review_decision_record_path_for_ticket(ready.ticket_id).exists()


def test_read_only_scope_never_initializes_or_writes_database(ready, tmp_path, monkeypatch):
    import sqlite3
    from hermes_cli.agent_platform import execution_evidence
    missing = tmp_path / "absent" / "kanban.db"
    with kb.scoped_read_only_connections(execution_evidence.connection):
        assert kb.init_db(missing) == missing
        assert not missing.parent.exists()
        with kb.connect(board=ready.projection_record["kanban_board_slug"]) as conn:
            with pytest.raises(sqlite3.OperationalError):
                conn.execute("UPDATE tasks SET status='blocked'")
        monkeypatch.setattr(kb, "detect_crashed_workers", lambda *a, **kw: pytest.fail("read-only inspection must not reconcile workers"))
        assert json.loads(tools._get_workflow_control({"blockers_only": True}))["read_only"]
    # Context cleanup restores normal isolated-fixture access.
    with kb.connect(board=ready.projection_record["kanban_board_slug"]) as conn:
        assert conn.execute("PRAGMA query_only").fetchone()[0] == 0
