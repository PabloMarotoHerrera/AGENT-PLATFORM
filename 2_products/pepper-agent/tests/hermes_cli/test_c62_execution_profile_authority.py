"""C62: pre-projection profile reads follow immutable current ticket authority."""
import json
from tests.hermes_cli.test_c58_pending_approval_authority import scenario as generic_scenario

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as wk
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import projection_home as projection_home


def profiles(home, monkeypatch):
    roster = [fixtures._profile_stub(home), fixtures._profile_stub(
        home, name="pepper-implementation-product", description="Pepper product implementation execution profile",
        cli_toolsets=("pepper_repository", "file", "no_mcp"),
    )]
    monkeypatch.setattr(wk, "list_profiles", lambda: roster)
    return roster


def approved(home, monkeypatch, ticket="P18.9.8"):
    from hermes_cli import kanban_db
    kanban_db.init_db()
    profiles(home, monkeypatch)
    if ticket == "P18.9.0":
        workflow = generation._workflow()
    else:
        predecessor = ticket.rsplit('.', 1)[0] + '.' + str(int(ticket.rsplit('.', 1)[1]) - 1)
        workflow = generation._workflow(
            closed_predecessor_ticket_id=predecessor, next_ticket_id=ticket,
            workflow_status="completed", next_action={
                "id": bridge.canonical_generation_action_id(ticket), "target_ticket_id": ticket,
            },
        )
    bridge.generate_current_ticket(workflow=workflow)
    record = bridge.load_generation_record(ticket_id=ticket)
    before = bridge.generation_record_path_for_ticket(ticket).read_bytes()
    bridge.apply_ticket_approval_decision(ticket_id=ticket, decision="approve", actor="synthetic-human")
    assert bridge.generation_record_path_for_ticket(ticket).read_bytes() == before
    assert not wk.kanban_projection_record_path_for_ticket(ticket).exists()
    return record


def inventory(home):
    return {str(p.relative_to(home)): p.read_bytes() for p in home.rglob('*') if p.is_file()}


def stale_base(monkeypatch):
    # The live path starts with historical architecture projection fields.
    old = {"current_ticket_id": "P18.9.0", "workflow_status": "completed",
           "selected_profile": "pepper-architecture-product", "assignee_profile": "pepper-architecture-product",
           "selected_role": "architecture_product", "execution_profile_role": "architecture_product",
           "required_write_toolsets": [], "profile_toolsets": ["pepper_repository"],
           "ticket_execution_requirements": {"ticket_id": "P18.9.0", "ticket_type": "architecture"}}
    monkeypatch.setattr(pr, "_p18_9_0_generation_overlay", lambda: (old, None))


@pytest.mark.parametrize("ticket", ["P18.9.8", "P18.9.9", "P18.9.10"])
def test_approved_implementation_uses_current_profile_without_projection(projection_home, monkeypatch, ticket):
    record = approved(projection_home, monkeypatch, ticket)
    stale_base(monkeypatch)
    before = inventory(projection_home)
    for _ in range(2):
        workflow = pr.build_workflow_control_snapshot()
        assert workflow["current_ticket_id"] == ticket
        assert workflow["workflow_status"] == "ticket_approved"
        assert workflow["selected_profile"] == "pepper-implementation-product"
        assert workflow["assignee_profile"] == "pepper-implementation-product"
        assert workflow["selected_role"] == workflow["execution_profile_role"] == "implementation_product"
        assert workflow["required_profile_toolsets"] == ["pepper_repository", "file"]
        assert workflow["required_write_toolsets"] == ["file"]
        assert workflow["required_capabilities"] == ["codebase-inspection", "codebase-edit"]
        assert workflow["ticket_execution_requirements"]["ticket_id"] == ticket
        assert workflow["ticket_execution_requirements"]["ticket_type"] == record["ticket_spec"]["ticket_type"]
        assert workflow["queue_state"] == "ticket_approved_not_queued"
        assert workflow.get("execution_started", False) is False
        assert workflow["active_execution_count"] == 0
        assert workflow["Kanban_dispatch"] is False
    assert inventory(projection_home) == before
    assert not wk.kanban_projection_record_path_for_ticket(ticket).exists()


def test_architecture_retains_architecture_profile(projection_home, monkeypatch):
    approved(projection_home, monkeypatch, "P18.9.0")
    before = inventory(projection_home)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["selected_profile"] == "pepper-architecture-product"
    assert workflow["selected_role"] == "architecture_product"
    assert workflow["required_write_toolsets"] == []
    assert inventory(projection_home) == before


def test_generic_approved_implementation(generic_scenario, monkeypatch):
    from tests.hermes_cli.test_c58_pending_approval_authority import _generate
    record = _generate(generic_scenario)
    profiles(generic_scenario.home, monkeypatch)
    bridge.apply_ticket_approval_decision(ticket_id=record["ticket_id"], decision="approve", actor="synthetic-human")
    before = inventory(generic_scenario.home)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == record["ticket_id"]
    assert workflow["selected_profile"] == "pepper-implementation-product"
    assert workflow["ticket_execution_requirements"]["ticket_type"] == "implementation"
    assert inventory(generic_scenario.home) == before


def test_real_historical_projection_does_not_supply_successor_profile(projection_home, monkeypatch):
    old = approved(projection_home, monkeypatch, "P18.9.0")
    wk.project_current_approved_workpacket_to_kanban(workflow=bridge.generated_record_to_workflow_overlay(old))
    old_path = wk.kanban_projection_record_path_for_ticket("P18.9.0")
    old_bytes = old_path.read_bytes()
    approved(projection_home, monkeypatch, "P18.9.8")
    before = inventory(projection_home)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.8"
    assert workflow["selected_profile"] == "pepper-implementation-product"
    assert not wk.kanban_projection_record_path_for_ticket("P18.9.8").exists()
    assert old_path.read_bytes() == old_bytes
    assert inventory(projection_home) == before


def test_persisted_projection_profile_is_not_reclassified(projection_home, monkeypatch):
    record = approved(projection_home, monkeypatch, "P18.9.8")
    initial = bridge.generated_record_to_workflow_overlay(record)
    wk.project_current_approved_workpacket_to_kanban(workflow=initial)
    projection = wk.load_kanban_projection_record(ticket_id="P18.9.8")
    monkeypatch.setattr(wk, "resolve_execution_profile_for_ticket", lambda *a, **k: pytest.fail("persisted projection must not be reclassified"))
    before = inventory(projection_home)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["selected_profile"] == projection["selected_profile"]
    assert workflow["selected_role"] == projection["selected_role"]
    # Also protect an approved-state read that already has persisted projection authority.
    blockers = []
    pr._apply_approved_ticket_execution_profile_authority(initial, blockers)
    assert not blockers
    assert initial["selected_profile"] == projection["selected_profile"]
    assert inventory(projection_home) == before


@pytest.mark.parametrize("mutation", ["ticket", "ticket_spec", "ticket_type", "approval", "no_profiles", "missing_write", "ambiguous"])
def test_invalid_current_profile_authority_fails_closed(projection_home, monkeypatch, mutation):
    record = approved(projection_home, monkeypatch)
    snapshot = bridge.generated_record_to_workflow_overlay(record)
    snapshot.update(selected_profile="pepper-architecture-product", assignee_profile="pepper-architecture-product",
                    selected_role="architecture_product", execution_profile_role="architecture_product")
    if mutation == "ticket":
        snapshot["current_ticket_id"] = "P999.999"
    elif mutation in {"ticket_spec", "ticket_type"}:
        if mutation == "ticket_spec":
            record["ticket_spec_SHA256"] = "f" * 64
        else:
            record["ticket_spec"]["ticket_type"] = "unknown-role"
        record["bridge_SHA256"] = bridge._record_digest(record)
        bridge.generation_record_path_for_ticket("P18.9.8").write_text(json.dumps(record), encoding="utf-8")
    elif mutation == "approval":
        path = bridge.approval_decision_record_path_for_ticket("P18.9.8")
        decision = json.loads(path.read_text(encoding="utf-8"))
        decision["decision_record_SHA256"] = "f" * 64
        path.write_text(json.dumps(decision), encoding="utf-8")
    elif mutation == "no_profiles":
        monkeypatch.setattr(wk, "list_profiles", lambda: [])
    elif mutation == "missing_write":
        roster = [fixtures._profile_stub(projection_home, name="pepper-implementation-product",
                  description="Pepper product implementation execution profile", cli_toolsets=("pepper_repository", "no_mcp"))]
        monkeypatch.setattr(wk, "list_profiles", lambda: roster)
    else:
        roster = profiles(projection_home, monkeypatch)
        roster.append(fixtures._profile_stub(projection_home, name="pepper-other-implementation",
                      description="Pepper product implementation execution profile", cli_toolsets=("pepper_repository", "file", "no_mcp")))
    before = inventory(projection_home)
    blockers = []
    pr._apply_approved_ticket_execution_profile_authority(snapshot, blockers)
    assert blockers
    assert snapshot["profile_assignment_gap"] is True
    for key in ("selected_profile", "assignee_profile", "selected_role", "execution_profile_role"):
        assert not snapshot.get(key)
    assert inventory(projection_home) == before
    assert not wk.kanban_projection_record_path_for_ticket("P18.9.8").exists()
