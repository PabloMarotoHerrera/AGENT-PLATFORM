"""Current manual failure authority survives re-queueing a terminal candidate."""

import json

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import manual_validation_resolution as resolution
from tests.hermes_cli import test_c76_manual_validation_resolution as c76
from tests.hermes_cli.test_c76_manual_validation_resolution import (
    completed as completed,
    evidence as evidence,
    failed as failed,
    flow as flow,
    full_contract as full_contract,
    projection_home as projection_home,
)
from tools import pepper_workflow_tools as tools

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


def public_action():
    workflow = pr.build_workflow_control_snapshot()
    action = workflow["next_action"]
    control = json.loads(tools._get_workflow_control({}))
    assert control["next_action"] == control["workflow_control"]["next_action"] == action
    assert json.loads(tools._get_next_action({}))["next_action"] == action
    return workflow, action


def assert_discovery(action, binding):
    assert action["tool"] == "resolve_current_ticket_manual_validation_failure"
    assert action["resolution_binding"] == binding
    assert action["choices"] == [
        {
            "decision": decision,
            "required_human_authorization_text": resolution.consent(binding, decision),
        }
        for decision in (resolution.IMPLEMENTATION, resolution.MATERIAL)
    ]


def test_first_failure_public_authority(failed):
    workflow, action = public_action()
    assert_discovery(action, failed.binding)
    assert workflow["human_action_required"] is True
    assert not workflow["remaining_blockers"]


@pytest.fixture
def fresh_v2_failure(failed, monkeypatch, evidence, terminal_status):
    """Use C76's real dispatch/evidence lifecycle, stopping at the fresh failure.

    Only worker spawning and command execution are synthetic, as in C76.
    Re-queue the terminal task before attestation to model the observed live
    triage state without changing its run, workspace, metadata or evidence.
    """
    original_attest = c76.attest

    class FreshFailureRecorded(Exception):
        pass

    def fail_v2(validation_id, status):
        assert validation_id == "V2"
        with kb.connect(board=failed.p["kanban_board_slug"]) as conn:
            conn.execute(
                "UPDATE tasks SET status=? WHERE id=?",
                (terminal_status, failed.p["kanban_task_id"]),
            )
            conn.commit()
        original_attest("V2", "failed")
        raise FreshFailureRecorded

    monkeypatch.setattr(c76, "attest", fail_v2)
    with pytest.raises(FreshFailureRecorded):
        c76.test_fresh_dispatch(failed, monkeypatch, evidence, False)
    monkeypatch.setattr(c76, "attest", original_attest)
    return failed


@pytest.mark.parametrize("terminal_status", ["blocked", "triage", "ready"])
@pytest.mark.parametrize("decision", [resolution.IMPLEMENTATION, resolution.MATERIAL])
def test_successive_round_precedence(fresh_v2_failure, decision):
    f = fresh_v2_failure
    historical = resolution.load(f.p, f.run_id)
    assert historical["validation_id"] == "V4"
    assert historical["human_decision"] == resolution.IMPLEMENTATION
    history_bytes = resolution.path_for(f.p, f.run_id).read_bytes()
    assert resolution.current(f.p) is None
    manual = pr.inspect_current_ticket_manual_validation()
    item = next(i for i in manual["items"] if i["validation_id"] == "V2")
    workflow, action = public_action()
    assert not workflow["remaining_blockers"], workflow["remaining_blockers"]
    assert workflow["workflow_status"] == "blocked_manual_validation_failed"
    assert workflow["review_state"] == "blocked_pending_contract_validation"
    binding = action["resolution_binding"]
    assert_discovery(action, binding)
    assert binding["run_id"] == manual["run_id"] != f.run_id
    assert binding["validation_id"] == "V2"
    assert binding["binding_SHA256"] == item["binding_SHA256"]
    assert binding["evidence_SHA256"] == item["evidence_SHA256"]
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]
    with pytest.raises(pr.ProductRuntimeConflict):
        c76.attest("V3", "passed")
    record = resolution.resolve(
        binding=binding,
        decision=decision,
        human_authorization_text=resolution.consent(binding, decision),
        corrective_guidance="Correct the current candidate or its contract explicitly.",
    )["resolution"]
    workflow, action = public_action()
    assert action == resolution.next_action(record)
    assert workflow["workflow_status"] == (
        resolution.STATE
        if decision == resolution.IMPLEMENTATION
        else "awaiting_material_revision"
    )
    assert resolution.path_for(f.p, f.run_id).read_bytes() == history_bytes
    assert resolution.load(f.p, f.run_id) == historical


def test_tampered_resolution_has_no_generic_fallback(failed):
    record = resolution.resolve(**failed.args)["resolution"]
    record["decision_SHA256"] = "0" * 64
    resolution.path_for(failed.p, failed.run_id).write_text(json.dumps(record))
    workflow, action = public_action()
    assert (
        workflow["remaining_blockers"][-1]["status"]
        == "blocked_by_invalid_manual_resolution"
    )
    assert action is None
    assert not workflow["reviewable_result"]


@pytest.mark.parametrize("status", ["executing", "awaiting_material_revision"])
def test_discovery_does_not_replace_other_authority(failed, status):
    action = {"id": "existing_authority"}
    snapshot = {"workflow_status": status, "next_action": action}
    blockers = []
    resolution.apply_workflow(snapshot, blockers)
    assert snapshot["next_action"] == action
    assert not blockers
