"""Real isolated approved/terminal authority; no live home or process execution."""

from copy import deepcopy
import json
from types import SimpleNamespace
import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import post_execution_material_revision as rev
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tests.hermes_cli.test_c65_retry_material_revision import flow as seed_flow, projection_home as projection_home
from tests.hermes_cli.test_c66_invalid_validation_command_revision import evidence as evidence
from tests.hermes_cli.test_c69_zero_change_decision import completed as completed, runs
from tests.hermes_cli.test_c91_validation_lifecycle import terminal as terminal
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import test_agent_platform_work_packet_compiler as compiler
from tools import pepper_workflow_tools as tools

MISSING = ["test_agent_platform_provider_single_worker_controlled_gate.py", "test_agent_platform_provider_failure_retry_policy.py"]
ACTUAL = ["test_agent_platform_provider_worker_controlled_gate.py", "test_agent_platform_provider_retry_policy.py"]
KEPT = ["test_agent_platform_work_packet_single_agent_execution.py", "test_agent_platform_work_packet_outcome_envelopes.py"]
COMMAND = "scripts/run_tests.sh " + " ".join("tests/hermes_cli/" + n for n in MISSING + KEPT)


@pytest.fixture
def flow(projection_home, monkeypatch, request):
    f = seed_flow.__wrapped__(projection_home, monkeypatch, SimpleNamespace(param="executable"))
    if getattr(request, "param", 1) == 1:
        return f
    from hermes_cli.agent_platform import retry_material_revision
    from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as projection
    from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures
    from hermes_cli import kanban_db as kb
    from pathlib import Path
    retry_material_revision.request(**f.args)
    pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "objective": "Verify the same bounded validation contract on the second revision."},
        ticket_id="P99.4", next_action_id="REVISE_P99_4")
    f.record = bridge.load_generation_record(ticket_id="P99.4")
    bridge.apply_ticket_approval_decision(ticket_id="P99.4", decision="approve", actor="isolated-human")
    f.projection = projection.project_current_approved_workpacket_to_kanban(workflow=pr.build_workflow_control_snapshot())
    f.run_id = fixtures._force_projected_execution_failure(projected=f.projection, pr=pr, kanban_db=kb, monkeypatch=monkeypatch)
    conn = kb.connect(board=f.projection["kanban_board_slug"])
    try:
        workspace = Path(kb.get_task(conn, f.projection["kanban_task_id"]).workspace_path)
    finally:
        conn.close()
    workspace.mkdir(parents=True, exist_ok=True)
    f.candidate = workspace / "candidate.txt"
    f.candidate.write_text("isolated revision two candidate")
    pr.recover_current_ticket_execution(human_authorization_text=pr.governed_ticket_recovery_authorization_text("P99.4"), ticket_id="P99.4")
    return f


@pytest.fixture(autouse=True)
def contract(monkeypatch):
    original = generation._synthetic_implementation_target
    def target(*args, **kwargs):
        c = kwargs["contract"]
        c["allowed_paths"].append("2_products/pepper-agent/tests/hermes_cli/**")
        c["validation_steps"][1] = compiler.validation_step("V2", command=COMMAND).model_dump(mode="json")
        c["validation_steps"].extend(compiler.validation_step(f"V{i}", command=None).model_dump(mode="json") for i in range(3, 13))
        return original(*args, **kwargs)
    monkeypatch.setattr(generation, "_synthetic_implementation_target", target)


@pytest.fixture
def defective(terminal, monkeypatch):
    f = terminal
    product = f.workspace / "2_products/pepper-agent"
    for name in ["scripts/run_tests.sh", "scripts/run_tests_parallel.py", *["tests/hermes_cli/" + n for n in ACTUAL + KEPT]]:
        p = product / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# isolated input\n")
    monkeypatch.setattr(pr, "_agent_platform_repository_root", lambda: f.workspace)
    monkeypatch.setattr(pr, "_completion_durable_source_authority_reference", lambda *a, **k: None)
    monkeypatch.setattr(pr, "_governed_autonomy_materialization_manifest", lambda *a, **k: (None, None))
    return f


def request():
    inspection = rev.inspect()
    return rev.request(binding=inspection["request_binding"], human_authorization_text=rev.consent(inspection["request_binding"]), next_action_id=rev.action_id(inspection["request_binding"]["ticket_id"]))


def test_request_is_separate_durable_and_read_only_inspection(defective):
    f = defective
    before = {p: p.read_bytes() for p in f.home.rglob('*') if p.is_file()}
    inspected = json.loads(tools._request_current_ticket_material_revision({"origin": "post_execution", "operation": "inspect"}))
    assert inspected["requestable"], inspected
    assert {p: p.read_bytes() for p in f.home.rglob('*') if p.is_file()} == before
    old = bridge.load_generation_record(ticket_id=f.p["ticket_id"])
    old_runs = runs(f)
    manual = pr.inspect_current_ticket_manual_validation()
    result = request()
    assert result["successor_generated"] is False
    assert bridge.load_generation_record(ticket_id=f.p["ticket_id"]) == old
    assert runs(f) == old_runs
    assert pr.inspect_current_ticket_manual_validation() == manual
    assert all(p.read_bytes() == raw for p, raw in before.items())
    assert set(p for p in f.home.rglob('*') if p.is_file()) - set(before) == {rev.path_for(old)}
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "awaiting_material_revision", workflow
    assert workflow["review_state"] == "material_revision_required"
    assert workflow["next_action"]["id"] == "REVISE_P99_4"
    assert workflow["next_action"]["required_human_action"] == "ticket_material_revision"
    assert not workflow["review_preparation_eligibility"]["available"]
    assert request()["idempotent_replay"]
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]
    assert not f.launched


@pytest.mark.parametrize("key", ["project_id", "ticket_id", "revision", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256", "run_id", "completion_SHA256", "validation_contract_SHA256", "defect_category", "defects"])
def test_wrong_binding_denied(defective, key):
    i = rev.inspect(); binding = {**i["request_binding"], key: "wrong"}
    with pytest.raises(ValueError):
        rev.request(binding=binding, human_authorization_text=i["next_action"]["human_authorization_text"], next_action_id=i["next_action"]["id"])
    assert not rev.path_for(defective.p).exists()


@pytest.mark.parametrize("text", ["", "yes", "REVISE_P99_4"])
def test_exact_human_consent_required(defective, text):
    i = rev.inspect()
    with pytest.raises(ValueError):
        rev.request(binding=i["request_binding"], human_authorization_text=text, next_action_id=i["next_action"]["id"])
    assert not rev.path_for(defective.p).exists()


def test_no_missing_references_no_gate(defective):
    for n in MISSING:
        (defective.workspace / "2_products/pepper-agent/tests/hermes_cli" / n).write_text("present")
    assert not rev.inspect()["requestable"]
    w = pr.build_workflow_control_snapshot()
    assert not any(a.get("origin") == "post_execution" for a in w.get("alternative_actions", []))


def test_tampered_request_fails_closed(defective):
    record = request();path = rev.path_for(defective.p)
    record["request_binding"]["run_id"] += 1
    path.write_text(json.dumps(record))
    assert pr.build_workflow_control_snapshot()["workflow_status"] == "material_revision_authority_blocked"


def test_public_request_needs_separate_revision_consent(defective):
    action = rev.inspect()["next_action"]
    args = {"origin": "post_execution", "operation": "request", "request_binding": action["request_binding"],
            "next_action_id": action["id"], "human_authorization_text": action["human_authorization_text"]}
    assert json.loads(tools._request_current_ticket_material_revision({**args, "command": "arbitrary"}))["success"] is False
    result = json.loads(tools._request_current_ticket_material_revision(args))
    assert result["success"], result
    before = bridge.load_generation_record(ticket_id=defective.p["ticket_id"])
    with pytest.raises(ValueError):
        pr.revise_current_ticket_for_material_contract_failure(
            human_authorization_text="", revision_contract={"ticket_id": "P99.4", "objective": "Not authorized"},
            ticket_id="P99.4", next_action_id="REVISE_P99_4")
    assert bridge.load_generation_record(ticket_id=defective.p["ticket_id"]) == before
    assert not defective.launched


def test_source_drift_after_request_blocks_revision(defective):
    request()
    (defective.workspace / "2_products/pepper-agent/tests/hermes_cli" / ACTUAL[0]).write_text("changed")
    assert pr.build_workflow_control_snapshot()["workflow_status"] == "material_revision_authority_blocked"


def test_inspect_operation_cannot_request_legacy_retry(flow):
    from hermes_cli.agent_platform import retry_material_revision
    path = retry_material_revision.path_for(flow.record)
    assert not path.exists()
    result = json.loads(tools._request_current_ticket_material_revision({
        "origin": "retry_pending", "operation": "inspect", **flow.args,
    }))
    assert result["success"] is False
    assert not path.exists()


@pytest.mark.parametrize("flow", [2], indirect=True)
def test_existing_executor_narrow_revision_preserves_history(defective):
    f = defective
    old = bridge.load_generation_record(ticket_id=f.p["ticket_id"])
    publication = bridge._publication_from_generation_record(old)
    assert publication.revision == 2
    record = request()
    steps = deepcopy(record["historical_authority"]["validation_contract"]["validation_steps"])
    old_steps = deepcopy(steps)
    for a, b in zip(MISSING, ACTUAL):
        steps[1]["command"] = steps[1]["command"].replace(a, b)
    old_runs = runs(f)
    zero = pr.zero_change_attestation_record_path_for_ticket(f.p["ticket_id"]).read_bytes()
    result = pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": f.p["ticket_id"], "validation_steps": steps},
        ticket_id=f.p["ticket_id"], next_action_id="REVISE_P99_4")
    assert result["revision_status"] == "awaiting_ticket_approval", result
    new = bridge.load_generation_record(ticket_id=f.p["ticket_id"])
    assert bridge._publication_from_generation_record(new).revision == publication.revision + 1
    assert bridge.load_approval_decision_record(ticket_id=f.p["ticket_id"], generation_record=new) is None
    assert new["revision_authority"]["material_revision_request_record"] == rev.load(old)
    assert new["revision_authority"]["previous_ticket_spec_SHA256"] == old["ticket_spec_SHA256"]
    assert new["revision_authority"]["previous_work_packet_SHA256"] == old["work_packet_SHA256"]
    assert runs(f) == old_runs
    assert pr.zero_change_attestation_record_path_for_ticket(f.p["ticket_id"]).read_bytes() == zero
    assert new["ticket_spec"]["title"] == old["ticket_spec"]["title"]
    assert new["ticket_spec"]["scope"] == old["ticket_spec"]["scope"]
    assert all(c in new["ticket_spec"]["constraints"] for c in old["ticket_spec"]["constraints"])
    assert new["ticket_spec"]["validation_steps"][0] == old["ticket_spec"]["validation_steps"][0]
    assert new["ticket_spec"]["validation_steps"][2:len(old_steps)] == old["ticket_spec"]["validation_steps"][2:]
    new_contract = new["revision_authority"]["revision_contract"]
    assert new_contract["validation_steps"][0] == old_steps[0]
    assert new_contract["validation_steps"][2:] == old_steps[2:]
    assert all(n in new_contract["validation_steps"][1]["command"] for n in ACTUAL + KEPT)
    assert not f.launched
