"""Current retry authority must follow the latest failure, not dispatch intent."""
import json

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)
from tools import pepper_workflow_tools as tools


def _recover():
    return pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER", ticket_id="P18.9.0", next_action_id="RECOVER_P18_9_0_EXECUTION",
    )


def _retry(spawn=None):
    return pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER", ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=spawn or (lambda *a, **kw: 4321),
    )


@pytest.fixture
def recovered(projection_home, monkeypatch):
    fixtures._install_execution_profile(monkeypatch, projection_home)
    fixtures._approve_current_ticket()
    projected = fixtures._project_via_runtime()
    fixtures._force_projected_execution_failure(
        projected=projected, pr=pr, kanban_db=kb, monkeypatch=monkeypatch,
    )
    recovery = _recover()
    assert recovery["recovery_status"] == "retry_pending"
    monkeypatch.setattr(pr, "_executor_provider_readiness", fixtures._ready_executor_provider_payload)
    monkeypatch.setattr(pr, "_preflight_pepper_governed_worker_credentials",
                        lambda *a, **kw: fixtures._ready_worker_credential_probe())
    monkeypatch.setattr(kb, "_pid_alive", lambda pid: int(pid) == 4321)
    return pr._load_current_projection_record(), recovery


def _state(projection):
    conn = kb.connect(board=projection["kanban_board_slug"])
    try:
        return [tuple(row) for row in conn.execute(
            "SELECT * FROM task_runs WHERE task_id=? ORDER BY id", (projection["kanban_task_id"],)
        )]
    finally:
        conn.close()


def _assert_surfaces(projection, status, action, recovery, retry):
    paths = [pr.recovery_action_record_path_for_ticket("P18.9.0"),
             pr.retry_start_record_path_for_ticket("P18.9.0")]
    before = {p: p.read_bytes() for p in paths if p.exists()}
    runs = _state(projection)
    for result in (json.loads(tools._get_workflow_control({})),
                   json.loads(tools._get_next_action({}))):
        assert result["workflow_status"] == status, result
        assert result["next_action"]["id"] == action
        assert result["recovery_state"] == recovery
        assert result["Git_mutation"] is False
    assert _state(projection) == runs
    assert {p: p.read_bytes() for p in before} == before
    workflow = pr.build_workflow_control_snapshot()
    assert pr.build_lead_agent_operational_context()["auto_retry"] is False
    assert workflow["retry_state"] == retry
    return workflow


@pytest.mark.parametrize("blocked", [False, True])
def test_c55_no_new_run_preserves_current_pending(recovered, monkeypatch, blocked):
    projection, _ = recovered
    if blocked:
        monkeypatch.setattr(pr, "_dispatch_exact_current_kanban_task", lambda *a, **kw: {
            "start_status": "blocked", "blocker_code": "SYNTHETIC_PRECLAIM_BLOCKER",
            "blocker_detail": "No claim was made", "dispatch_performed": False,
            "execution_started": False, "worker_process_started": False,
        })
        result = _retry(lambda *a, **kw: pytest.fail("preclaim block must not spawn"))
        assert result["execution_started"] is False
        assert pr.load_current_ticket_retry_start_record() is not None
    _assert_surfaces(projection, "retry_pending", "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
                     "retry_pending", "retry_pending")
    assert len(_state(projection)) == 1


def _fail_dispatch(monkeypatch):
    def fail(**kwargs):
        raise pr.ProductRuntimeConflict("synthetic exact source verification failure")
    monkeypatch.setattr(pr, "_projection_requires_scratch_source_materialization", lambda p: True)
    monkeypatch.setattr(pr, "_prepare_governed_source_authority_for_dispatch", fail)


@pytest.mark.parametrize("before_worker", [False, True])
def test_c55_new_failed_run_requires_new_recovery(recovered, monkeypatch, before_worker):
    projection, recovery = recovered
    if before_worker:
        _fail_dispatch(monkeypatch)
        result = _retry(lambda *a, **kw: pytest.fail("failed materialization must not spawn"))
        assert result["execution_started"] is False
        assert result["blocker_code"] == "WORKSPACE_SOURCE_MATERIALIZATION_FAILED"
    else:
        result = _retry()
        assert result["execution_started"] is True
        fixtures._finish_projected_run_as_terminal(kb, projection, result["kanban_run_id"],
            status="gave_up", outcome="gave_up", summary="synthetic worker failure")
    runs = _state(projection)
    assert len(runs) == 2
    old_recovery = pr.load_current_ticket_recovery_action_record()
    old_retry = pr.load_current_ticket_retry_start_record(allow_historical_mismatch=True)
    assert old_recovery["recovery_action_SHA256"] == recovery["recovery_action_SHA256"]
    assert old_retry["execution_started"] is (not before_worker)
    workflow = _assert_surfaces(projection, "execution_failed", "RECOVER_P18_9_0_EXECUTION",
                               "recovery_required", "retry_failed")
    assert workflow["validation_state"] == "retry_execution_failed_before_validation"
    assert workflow["review_state"] == "not_started_execution_failed"
    assert workflow["active_execution_count"] == 0
    assert workflow["worker_lifecycle"]["runs"][-1]["id"] != recovery["latest_failed_run_id"]
    denied = _retry(lambda *a, **kw: pytest.fail("stale recovery must not dispatch"))
    source = pr._kanban_retry_start_source_state(projection, old_recovery)
    assert source["blocker_code"] == "KANBAN_RETRY_SOURCE_GAP"
    assert source["blocker_detail"] == "latest failed run no longer matches recovery authority"
    if before_worker:
        assert denied["blocker_code"] == "KANBAN_RETRY_SOURCE_GAP"
        assert denied["blocker_detail"] == source["blocker_detail"]
    else:
        assert denied["blocker_code"] == "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED"
    assert denied["dispatch_performed"] is False
    assert _state(projection) == runs
    assert pr.load_current_ticket_recovery_action_record() == old_recovery
    assert pr.load_current_ticket_retry_start_record(allow_historical_mismatch=True) == old_retry


def test_c55_new_recovery_requires_separate_retry(recovered, monkeypatch):
    projection, old_recovery = recovered
    with monkeypatch.context() as patch:
        _fail_dispatch(patch)
        failed = _retry(lambda *a, **kw: pytest.fail("must not spawn"))
    assert failed["execution_started"] is False
    old_retry = pr.load_current_ticket_retry_start_record()
    runs = _state(projection)
    new = _recover()
    assert new["recovery_status"] == "retry_pending", new
    assert new["recovery_cycle_id"] != old_recovery["recovery_cycle_id"]
    assert new["latest_failed_run_id"] != old_recovery["latest_failed_run_id"]
    assert new["observed_attempt_count"] == 2
    assert new["execution_started"] is False
    assert new["dispatch_performed"] is False
    assert _state(projection) == runs
    assert pr.load_current_ticket_retry_start_record(allow_historical_mismatch=True) == old_retry
    assert old_recovery["recovery_action_SHA256"] in pr.p18_9_0_recovery_action_history_path().read_text()
    _assert_surfaces(projection, "retry_pending", "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
                     "retry_pending", "retry_pending")
    assert pr._kanban_retry_start_source_state(projection, pr.load_current_ticket_recovery_action_record())["blocker_code"] is None
    started = _retry()
    assert started["retry_start_status"] == "started", started
    assert started["recovery_cycle_id"] == new["recovery_cycle_id"]
    assert len(_state(projection)) == 3
    assert old_retry["retry_start_authorization_SHA256"] in pr.p18_9_0_retry_start_history_path().read_text()


@pytest.mark.parametrize("completed", [False, True])
def test_c55_new_run_projects_runtime_state(recovered, completed):
    projection, _ = recovered
    result = _retry()
    assert result["execution_started"] is True
    if completed:
        conn = kb.connect(board=projection["kanban_board_slug"])
        try:
            assert kb.complete_task(conn, projection["kanban_task_id"], summary="synthetic success")
        finally:
            conn.close()
    _assert_surfaces(projection, "execution_completed_pending_zero_change_attestation" if completed else "executing",
                     "ATTEST_P18_9_0_ZERO_CHANGE_FOR_REVIEW_PREPARE" if completed else "MONITOR_P18_9_0_EXECUTION",
                     "not_required", "retry_completed" if completed else "retry_executing")

@pytest.mark.parametrize("completed", [False, True])
def test_c55_pending_record_cannot_hide_new_active_or_successful_run(recovered, monkeypatch, completed):
    projection, _ = recovered
    with monkeypatch.context() as patch:
        patch.setattr(pr, "_dispatch_exact_current_kanban_task", lambda *a, **kw: {
            "start_status": "blocked", "blocker_code": "SYNTHETIC_PRECLAIM_BLOCKER",
            "blocker_detail": "No claim was made", "dispatch_performed": False,
            "execution_started": False, "worker_process_started": False,
        })
        assert _retry()["execution_started"] is False
    conn = kb.connect(board=projection["kanban_board_slug"])
    try:
        task = kb.claim_task(conn, projection["kanban_task_id"], claimer="synthetic-later-dispatch")
        assert task is not None
        kb._set_worker_pid(conn, task.id, 4321)
        if completed:
            assert kb.complete_task(conn, task.id, summary="synthetic success")
    finally:
        conn.close()
    workflow = _assert_surfaces(
        projection, "execution_completed_pending_zero_change_attestation" if completed else "executing",
        "ATTEST_P18_9_0_ZERO_CHANGE_FOR_REVIEW_PREPARE" if completed else "MONITOR_P18_9_0_EXECUTION",
        "not_required", "retry_completed" if completed else "retry_executing",
    )
    assert workflow["active_execution_count"] == (0 if completed else 1)
