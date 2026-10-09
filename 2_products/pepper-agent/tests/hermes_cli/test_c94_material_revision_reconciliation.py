"""Human reconciliation against real isolated C92/C93 durable authority."""

from copy import deepcopy
import json

import pytest

from hermes_cli.agent_platform import material_revision_reconciliation as rc
from hermes_cli.agent_platform import post_execution_material_revision as rev
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import approved_artifact_inspection as artifact
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tools import pepper_workflow_tools as tools
from tests.hermes_cli.test_c92_post_execution_material_revision import (
    flow, projection_home, evidence, completed, terminal, contract, defective, request,
)


def files(f):
    return {str(p.relative_to(f.home)): p.read_bytes() for p in f.home.rglob("*") if p.is_file()}


@pytest.fixture
def stale(defective):
    f = defective
    request()
    f.original = rev.load(f.record)
    f.original_bytes = rev.path_for(f.record).read_bytes()
    f.changed = f.workspace / "2_products/pepper-agent/docs/source-change.md"
    f.changed.parent.mkdir(parents=True, exist_ok=True)
    f.changed.write_text("isolated source change")
    return f


def arguments():
    i = rc.inspect()
    assert i["reconciliation_available"], i
    return {"binding": i["reconciliation_binding"],
            "human_authorization_text": i["next_action"]["human_authorization_text"],
            "next_action_id": rc.ACTION}


def test_inspection_exposes_exact_source_only_authority_without_writes(stale):
    f = stale
    before = files(f)
    i = rc.inspect()
    assert i["reconciliation_available"], i
    assert i["immutable_authority_identity_match"]
    assert i["reconciliation_binding"]["old_material_revision_request_SHA256"] == f.original["material_revision_request_SHA256"]
    assert i["reconciliation_binding"]["old_request_binding"][rc.SOURCE] != i["reconciliation_binding"]["current_request_binding"][rc.SOURCE]
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "material_revision_authority_blocked"
    assert workflow["required_human_action"] == "authority_reconciliation"
    assert workflow["next_action"]["id"] == rc.ACTION
    assert workflow["next_action"]["human_authorization_text"] == rc.consent(i["reconciliation_binding"])
    assert not workflow["command_validation_available"]
    assert files(f) == before


@pytest.mark.parametrize("text", [None, "yes", "continue", "I explicitly authorize revision of P99.4."])
def test_exact_distinct_human_consent_required(stale, text):
    args = arguments()
    before = files(stale)
    with pytest.raises(ValueError):
        rc.reconcile(**{**args, "human_authorization_text": text})
    assert files(stale) == before


@pytest.mark.parametrize("key", ["ticket_spec_SHA256", "work_packet_SHA256", "work_packet_id", "revision",
                                 "run_id", "completion_SHA256", "validation_contract_SHA256", "projection_SHA256"])
def test_wrong_immutable_binding_denied(stale, key):
    args = arguments()
    args["binding"]["current_request_binding"][key] = "wrong"
    before = files(stale)
    with pytest.raises(ValueError):
        rc.reconcile(**args)
    assert files(stale) == before


def test_wrong_prior_sha_or_conflicting_actor_denied(stale):
    args = arguments()
    wrong = deepcopy(args)
    wrong["binding"]["old_material_revision_request_SHA256"] = "0" * 64
    with pytest.raises(ValueError):
        rc.reconcile(**wrong)
    rc.reconcile(**args)
    with pytest.raises(ValueError, match="authorizer"):
        rc.reconcile(**args, authorizer_id="different-human")


@pytest.mark.parametrize("drift", ["run_id", "validation_contract_SHA256", "defects", "history", "root"])
def test_actual_non_source_drift_is_not_reconcilable(stale, monkeypatch, drift):
    original = rev.context

    def changed(projection):
        generation, current, history = deepcopy(original(projection))
        if drift == "history":
            history["zero_change_authority"] = {}
        elif drift == "root":
            current[rc.SOURCE]["source_root"] = "/different"
        else:
            current[drift] = "unexpected"
        return generation, current, history

    monkeypatch.setattr(rev, "context", changed)
    before = files(stale)
    assert not rc.inspect()["reconciliation_available"]
    assert files(stale) == before


@pytest.mark.parametrize("flow", [2], indirect=True)
def test_reconciliation_only_restores_revise_preserves_history_and_c93(stale):
    f = stale
    args = arguments()
    old_artifact = artifact.inspect(ticket_id="P99.4", section_id="validation_steps", max_chars=20000)
    before = files(f)
    result = rc.reconcile(**args)
    after = files(f)
    added = set(after) - set(before)
    assert len(added) == 1 and "reconciliations/" in next(iter(added))
    assert all(after[p] == data for p, data in before.items())
    assert rev.path_for(f.record).read_bytes() == f.original_bytes
    assert not result["successor_generated"] and not result["execution_started"] and not result["Git_mutation"]
    current = rev.load(f.record)
    assert current["reconciliation_authority"]["previous_request"] == f.original
    assert current["material_revision_request_SHA256"] != f.original["material_revision_request_SHA256"]
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "awaiting_material_revision"
    assert workflow["review_state"] == "material_revision_required"
    assert workflow["next_action"]["id"] == "REVISE_P99_4"
    assert workflow["pending_ticket_approval_count"] == 0
    assert not workflow["command_validation_available"] and not workflow["reviewable_result"]
    assert bridge._publication_from_generation_record(bridge.load_generation_record(ticket_id="P99.4")).revision == 2
    assert artifact.inspect(ticket_id="P99.4", section_id="validation_steps", max_chars=20000) == old_artifact
    assert rc.reconcile(**args)["idempotent_replay"]
    assert files(f) == after
    assert rc.inspect()["reconciliation_SHA256"] == result["reconciliation_SHA256"]
    with pytest.raises((ValueError, pr.ProductRuntimeConflict)):
        pr.revise_current_ticket_for_material_contract_failure(
            ticket_id="P99.4", next_action_id="REVISE_P99_4", human_authorization_text=args["human_authorization_text"],
            revision_contract={"ticket_id": "P99.4", "objective": "Not authorized by reconciliation."})
    assert files(f) == after
    assert not f.launched


def test_tampered_reconciliation_blocks_without_fallback(stale):
    args = arguments()
    rc.reconcile(**args)
    path = rc.path_for(stale.record, stale.original["material_revision_request_SHA256"])
    data = json.loads(path.read_text())
    data["human_authorization_text"] = "yes"
    path.write_text(json.dumps(data))
    assert not rc.inspect()["reconciliation_available"]
    assert pr.build_workflow_control_snapshot()["workflow_status"] == "material_revision_authority_blocked"
    assert rev.path_for(stale.record).read_bytes() == stale.original_bytes


def test_no_drift_no_reconciliation_and_public_operation_is_strict(defective):
    request()
    assert not rc.inspect()["reconciliation_available"]
    before = files(defective)
    for args in ({"origin": "post_execution", "operation": "inspect_reconciliation", "command": "bad"},
                 {"origin": "retry_pending", "operation": "reconcile"},
                 {"origin": "post_execution", "operation": "reconcile", "human_authorization_text": "yes"}):
        assert json.loads(tools._request_current_ticket_material_revision(args))["success"] is False
    assert files(defective) == before


def test_public_inspect_reconcile_and_further_source_drift(stale):
    args = {"origin": "post_execution", "operation": "inspect_reconciliation"}
    inspected = json.loads(tools._request_current_ticket_material_revision(args))
    assert inspected["reconciliation_available"]
    result = json.loads(tools._request_current_ticket_material_revision({
        "origin": "post_execution", "operation": "reconcile",
        "reconciliation_binding": inspected["reconciliation_binding"],
        "human_authorization_text": inspected["next_action"]["human_authorization_text"], "next_action_id": rc.ACTION}))
    assert result["success"], result
    stale.changed.write_text("another independent source change")
    assert pr.build_workflow_control_snapshot()["workflow_status"] == "material_revision_authority_blocked"
    second = rc.reconcile(**arguments())
    assert second["reconciliation_SHA256"] != result["reconciliation_SHA256"]
    assert pr.build_workflow_control_snapshot()["workflow_status"] == "awaiting_material_revision"


@pytest.mark.parametrize("boundary", ["review_prepare_record_path_for_ticket", "review_decision_record_path_for_ticket",
                                     "human_git_handoff_completion_record_path_for_ticket"])
def test_superseding_review_or_handoff_prevents_reconciliation(stale, boundary):
    path = getattr(pr, boundary)("P99.4")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}")
    before = files(stale)
    assert not rc.inspect()["reconciliation_available"]
    assert files(stale) == before


def test_existing_executor_accepts_only_separate_fixture_consent(stale):
    f = stale
    assert bridge._publication_from_generation_record(f.record).revision == 1
    rc.reconcile(**arguments())
    effective = rev.load(f.record)
    # Historical bridge validation supplies only these predecessor identity fields.
    rev.validate_record(effective, {k: f.record[k] for k in (
        "ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256")})
    result = pr.revise_current_ticket_for_material_contract_failure(
        ticket_id="P99.4", next_action_id="REVISE_P99_4",
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "objective": "Isolated separately authorized revision executor compatibility."})
    assert result["revision_status"] == "awaiting_ticket_approval"
    new = bridge.load_generation_record(ticket_id="P99.4")
    assert bridge._publication_from_generation_record(new).revision == 2
    assert new["revision_authority"]["material_revision_request_record"] == effective
    assert rev.path_for(f.record).read_bytes() == f.original_bytes
    assert not f.launched


def test_active_execution_prevents_reconciliation(stale):
    from hermes_cli import kanban_db as kb
    conn = kb.connect(board=stale.p["kanban_board_slug"])
    try:
        conn.execute("UPDATE tasks SET current_run_id=? WHERE id=?", (stale.run_id, stale.p["kanban_task_id"]))
        conn.commit()
    finally:
        conn.close()
    before = files(stale)
    assert not rc.inspect()["reconciliation_available"]
    assert files(stale) == before
