"""Discovery of run-bound recovery preserves the separate retry boundary."""
import json

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import recovery_authority as recovery
from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import projection_home as projection_home
from tests.hermes_cli.test_c81_manual_resolution_projection import public_action


@pytest.fixture
def failed(projection_home, monkeypatch):
    fixtures._install_execution_profile(monkeypatch, projection_home)
    fixtures._approve_current_ticket()
    p = fixtures._project_via_runtime()
    run_id = fixtures._force_projected_execution_failure(
        projected=p, pr=pr, kanban_db=kb, monkeypatch=monkeypatch,
    )
    pr.build_workflow_control_snapshot()  # reconcile the synthetic crashed worker
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        conn.execute("UPDATE task_runs SET status='blocked', outcome='blocked', error='validation-infrastructure-failed' WHERE id=?", (run_id,))
        conn.commit()
    return p, run_id


@pytest.mark.parametrize("field", ["tool", "run_id", "required_human_action", "required_human_authorization_text", "recovery_binding", "recovery_binding_SHA256"])
def test_public_recovery_authority(failed, field):
    p, run_id = failed
    workflow, action = public_action()
    assert action[field]
    assert action["run_id"] == run_id
    assert action["recovery_binding"]["kanban_task_id"] == p["kanban_task_id"]
    assert action["tool"] == "recover_current_ticket_execution"
    assert workflow["recovery_state"] == "recovery_required"


def test_recovery_only_then_separate_retry_and_idempotency(failed, monkeypatch):
    p, run_id = failed
    monkeypatch.setattr(kb, "_default_spawn", lambda *a, **kw: pytest.fail("unexpected worker"))
    _, action = public_action()
    result = pr.recover_current_ticket_execution(
        human_authorization_text=action["required_human_authorization_text"],
        ticket_id=p["ticket_id"], next_action_id=action["id"],
    )
    assert result["recovery_authorization_recorded"]
    assert not result["dispatch_performed"]
    workflow, retry = public_action()
    assert workflow["workflow_status"] == "retry_pending"
    assert retry["tool"] == "start_current_ticket_execution"
    assert retry["run_id"] == run_id
    assert retry["recovery_action_SHA256"] == result["recovery_action_SHA256"]
    assert retry["required_human_authorization_text"] != action["required_human_authorization_text"]
    assert pr.execution_human_authorization_text_diagnostics(
        retry["required_human_authorization_text"], current_ticket_id=p["ticket_id"],
        current_next_action_id=retry["id"],
    ) is None
    denied = pr.start_current_ticket_execution(
        human_authorization_text=action["required_human_authorization_text"],
        spawn_fn=lambda *a, **kw: pytest.fail("unexpected worker"),
    )
    assert not denied["execution_started"]
    assert denied["blocker_code"]
    assert pr.recover_current_ticket_execution(human_authorization_text=action["required_human_authorization_text"])["idempotent_replay"]
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        assert len(kb.list_runs(conn, p["kanban_task_id"])) == 1


def test_wrong_run_consent_is_rejected(failed):
    _, run_id = failed
    _, action = public_action()
    with pytest.raises(pr.ProductRuntimeError):
        pr.recover_current_ticket_execution(human_authorization_text=action["required_human_authorization_text"].replace(f"run {run_id}.", f"run {run_id+1}."))


def test_generic_start_cannot_bypass_recovery(failed):
    p, _ = failed
    result = pr.start_current_ticket_execution(
        human_authorization_text=f"I explicitly authorize execution start for {p['ticket_id']}.",
        spawn_fn=lambda *a, **kw: pytest.fail("unexpected worker"),
    )
    assert not result["execution_started"]


def test_unrelated_retry_metadata_is_not_recovery_authority(failed):
    workflow, action = public_action()
    workflow["retry_start_authority"] = {"kanban_task_id": "unrelated", "kanban_run_id": 3}
    recovery.apply_workflow(workflow, [])
    assert workflow["next_action"] == action
    assert "retry_start_authority" not in workflow


@pytest.mark.parametrize("body", [{"WorkPacket_ID": "wrong"}, []])
def test_tampered_task_binding_blocks_action(failed, body):
    p, _ = failed
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        conn.execute("UPDATE tasks SET body=? WHERE id=?", (json.dumps(body), p["kanban_task_id"]))
        conn.commit()
    workflow, action = public_action()
    assert action["id"] != pr.governed_ticket_lifecycle_action_ids(p["ticket_id"])["execution_recovery"]
    assert "tool" not in action


def test_unavailable_terminal_identity_fails_closed(failed, monkeypatch):
    def invalid(_record):
        raise pr.ProductRuntimeConflict("invalid terminal digest")
    monkeypatch.setattr(recovery, "terminal_identity", invalid)
    workflow, action = public_action()
    assert workflow["recovery_state"] == "blocked_invalid_recovery_authority"
    assert action["id"] == "RESOLVE_RECOVERY_AUTHORITY_BLOCKER"


@pytest.mark.parametrize("field", ["terminal_run_SHA256", "recovery_action_SHA256"])
def test_tampered_recovery_record_does_not_advertise_retry(failed, field):
    p, _ = failed
    _, action = public_action()
    pr.recover_current_ticket_execution(**action["arguments"])
    path = pr.recovery_action_record_path_for_ticket(p["ticket_id"])
    record = json.loads(path.read_text())
    record[field] = "0" * 64
    path.write_text(json.dumps(record))
    workflow, action = public_action()
    assert action["id"] == "RESOLVE_RECOVERY_AUTHORITY_BLOCKER"
    assert not workflow["runtime_execution_authorized"]
