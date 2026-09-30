"""C61: traverse persisted closure chains to the existing successor approval."""

import json
from dataclasses import asdict, replace
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as wk
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)
from tools import pepper_workflow_tools as tools


@pytest.fixture
def chain(projection_home, tmp_path, monkeypatch):
    original_projection = fixtures._c13_projection_record

    def projection(runtime, ticket_id):
        return {**original_projection(runtime, ticket_id), "macroproject_id": "P18.9"}

    monkeypatch.setattr(fixtures, "_c13_projection_record", projection)
    original_authority = fixtures._c14_successor_authority

    def authority(runtime, predecessor):
        result = original_authority(runtime, predecessor)
        result["next_action_id"] = bridge.canonical_generation_action_id(
            result["ticket_id"]
        )
        return result

    monkeypatch.setattr(fixtures, "_c14_successor_authority", authority)
    closed = {}
    for ticket in ("P18.9.7", "P18.9.8", "P18.9.9"):
        f = fixtures._c14_review_authority_fixture(
            pr, tmp_path, monkeypatch, ticket_id=ticket
        )
        fixtures._c14_persist_completion_record(pr, f)
        closed[ticket] = f
    targets = tuple(
        replace(
            generation._synthetic_implementation_target(
                f"P18.9.{i}",
                fixtures._c9_ticket_title(f"P18.9.{i}"),
                contract=generation._synthetic_implementation_contract("Approval"),
                dependencies=(f"P18.9.{i - 1}",),
            ),
            macroproject_id="P18.9",
            next_action_id=bridge.canonical_generation_action_id(f"P18.9.{i}"),
        )
        for i in range(7, 14)
    )
    items = tuple(
        {
            **asdict(t),
            "authority_type": t.canonical_roadmap_authority,
            "authority_path": t.roadmap_authority_path,
            "authority_section": t.roadmap_authority_section,
        }
        for t in targets
    )
    monkeypatch.setattr(bridge, "resolve_roadmap_ticket_authorities", lambda: items)
    monkeypatch.setattr(
        pr,
        "resolve_canonical_next_ticket",
        lambda workflow=None: asdict(bridge.resolve_canonical_next_ticket(workflow)),
    )
    base = fixtures._c13_review_ready_workflow(pr, closed["P18.9.7"].projection)
    monkeypatch.setattr(pr, "_p18_9_0_generation_overlay", lambda: (base, None))
    monkeypatch.setattr(
        pr,
        "_completed_predecessor_successor_lifecycle_overlay",
        lambda *a, **k: (None, None),
    )
    monkeypatch.setattr(
        pr, "_load_current_projection_record", lambda: closed["P18.9.7"].projection
    )
    monkeypatch.setattr(
        wk,
        "load_kanban_projection_record",
        lambda *, ticket_id, **k: (
            closed[ticket_id].projection if ticket_id in closed else None
        ),
    )
    real_overlay = pr._pending_generated_successor_ticket_approval_overlay

    def overlay(workflow, *, allow_current_ticket_projection=False):
        predecessor = workflow.get("closed_predecessor_ticket_id")
        ticket = {"P18.9.7": "P18.9.8", "P18.9.8": "P18.9.9"}.get(predecessor)
        if ticket and not workflow.get("current_ticket_id"):
            return {
                **fixtures._c13_review_ready_workflow(pr, closed[ticket].projection),
                "current_ticket_id": ticket,
                "next_ticket_id": None,
            }, None
        return real_overlay(
            workflow, allow_current_ticket_projection=allow_current_ticket_projection
        )

    monkeypatch.setattr(
        pr, "_pending_generated_successor_ticket_approval_overlay", overlay
    )
    return SimpleNamespace(
        home=projection_home, closed=closed, target=targets[3], items=items
    )


def generate(chain):
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == chain.target.next_action_id
    result = bridge.generate_current_ticket(workflow=workflow, target=chain.target)
    assert result["generation_status"] == "awaiting_ticket_approval"
    return bridge.load_generation_record(ticket_id=chain.target.ticket_id)


def inventory(chain):
    return {
        str(p.relative_to(chain.home)): p.read_bytes()
        for p in (chain.home / "agent-platform").rglob("*")
        if p.is_file()
    }


def test_completed_predecessor_only(chain):
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["closed_predecessor_ticket_id"] == "P18.9.9"
    assert (
        workflow["next_action"]["id"]
        == "GENERATE_P18_9_10_REQUIRES_SEPARATE_HUMAN_ACTION"
    )
    assert not bridge.generation_record_path_for_ticket("P18.9.10").exists()


def test_existing_pending_successor_surfaces_and_approval(chain):
    record = generate(chain)
    before = inventory(chain)
    for _ in range(2):
        workflow = pr.build_workflow_control_snapshot()
        assert workflow["workflow_status"] == "awaiting_ticket_approval", workflow
        assert workflow["current_ticket_id"] == "P18.9.10"
        assert workflow["governed_workflow_state"] == "awaiting_ticket_approval"
        assert workflow["workflow_state"] == "P18.9.10-AWAITING-TICKET-APPROVAL"
        assert workflow["ticket_closed"] is False
        assert workflow["handoff_completion_present"] is False
        for flag in (
            "execution_started",
            "ticket_execution_authorized",
            "WorkPacket_execution_authorized",
            "runtime_execution_authorized",
            "worker_execution",
            "Kanban_dispatch",
            "Git_mutation",
        ):
            assert workflow[flag] is False
        assert workflow["next_action"]["id"] == "APPROVE_P18_9_10"
        assert workflow["pending_ticket_approval_count"] == 1
        for reader in (
            tools._get_current_ticket,
            tools._get_workflow_control,
            tools._get_next_action,
        ):
            value = json.loads(reader({}))
            assert value["success"] is True
            assert value["current_ticket_id"] == "P18.9.10"
            assert value["next_action"]["id"] == "APPROVE_P18_9_10"
        pending = json.loads(tools._get_pending_approvals({}))
        assert pending["pending_approval_count"] == 1
        inspection = json.loads(
            tools._inspect_pending_approval({"approval_id": "P18.9.10"})
        )
        assert inspection["success"] is True
        binding = inspection["artifact_inspection"]["approval_binding"]
        assert binding["TicketSpec_SHA256"] == record["ticket_spec_SHA256"]
        assert binding["WorkPacket_SHA256"] == record["work_packet_SHA256"]
        assert binding["publication_revision"] == 1
    assert inventory(chain) == before
    result = json.loads(
        tools._decide_pending_approval({
            "approval_id": "P18.9.10",
            "ticket_id": "P18.9.10",
            "decision": "approve",
            "next_action_id": "APPROVE_P18_9_10",
            "human_decision_text": "I approve P18.9.10",
            "ticket_spec_sha256": record["ticket_spec_SHA256"],
            "work_packet_sha256": record["work_packet_SHA256"],
        })
    )
    assert result["success"] is True, result
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    after = inventory(chain)
    changed = [
        key for key in before.keys() | after.keys() if before.get(key) != after.get(key)
    ]
    assert len(changed) == 1
    assert changed[0].endswith("P18.9.10.approval-decision.json")


@pytest.mark.parametrize(
    "mutation",
    [
        "publication_id",
        "publication_sha",
        "ticket_spec",
        "work_packet",
        "approval_ticket",
        "approval_revision",
        "transition",
        "unreadable",
    ],
)
def test_malformed_successor_fails_closed(chain, mutation):
    record = generate(chain)
    path = bridge.generation_record_path_for_ticket("P18.9.10")
    if mutation == "publication_id":
        pr._ticket_approval_publication_body(record)["publication_id"] = (
            "PUB-P18-9-11-0001"
        )
    elif mutation == "publication_sha":
        pr._ticket_approval_publication_body(record)["artifact_SHA256"] = "f" * 64
    elif mutation == "ticket_spec":
        record["ticket_spec_SHA256"] = "f" * 64
    elif mutation == "work_packet":
        record["work_packet_SHA256"] = "f" * 64
    elif mutation == "approval_ticket":
        record["ticket_approval_record"]["ticket_id"] = "P18.9.11"
    elif mutation == "approval_revision":
        record["ticket_approval_record"]["publication_revision"] = 2
    elif mutation == "transition":
        record["workflow_transition_result"] = {"unreadable_transition": True}
    record["bridge_SHA256"] = bridge._record_digest(record)
    path.write_text(
        "{" if mutation == "unreadable" else json.dumps(record), encoding="utf-8"
    )
    before = inventory(chain)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] != "P18.9.10"
    assert workflow["next_action"]["id"] != "APPROVE_P18_9_10"
    assert workflow["remaining_blockers"]
    assert inventory(chain) == before


def test_duplicate_pending_successor_fails_closed(chain, monkeypatch):
    record = generate(chain)
    monkeypatch.setattr(
        pr, "_pending_ticket_approval_records", lambda: [record, record]
    )
    before = inventory(chain)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] != "APPROVE_P18_9_10"
    assert any("ambiguous" in item["status"] for item in workflow["remaining_blockers"])
    assert inventory(chain) == before


def test_numeric_order_and_identifiers(projection_home):
    tickets = [f"P18.9.{i}" for i in range(8, 14)]
    assert sorted(reversed(tickets), key=pr._governed_ticket_sequence_key) == tickets
    assert sorted(tickets) != tickets  # lexical order would put .10 before .8
    roadmap = bridge.resolve_roadmap_ticket_authorities()
    assert [
        item["ticket_id"] for item in roadmap if item["ticket_id"] in tickets
    ] == tickets
    for ticket in tickets:
        assert bridge._safe_ticket_id(ticket) == ticket
        token = ticket.replace(".", "_")
        assert bridge.approval_action_id(ticket) == f"APPROVE_{token}"
        assert (
            bridge.canonical_generation_action_id(ticket)
            == f"GENERATE_{token}_REQUIRES_SEPARATE_HUMAN_ACTION"
        )
        assert pr.governed_ticket_lifecycle_action_token(ticket) == token
        assert pr.governed_ticket_lifecycle_hyphen_token(ticket) == ticket.replace(
            ".", "-"
        )


@pytest.mark.parametrize("predecessor", ["P18.9.9", "P18.9.10", "P18.9.11", "P18.9.12"])
def test_future_two_digit_successor_projection(projection_home, predecessor):
    expected = f"P18.9.{int(predecessor.rsplit('.', 1)[1]) + 1}"
    authority = bridge.resolve_canonical_next_ticket({
        "closed_predecessor_ticket_id": predecessor,
        "workflow_status": "completed",
        "current_ticket_id": None,
    })
    assert authority.ticket_id == expected
    assert authority.next_action_id == bridge.canonical_generation_action_id(expected)
    assert (
        authority.generation_target().approval_next_action_id
        == bridge.approval_action_id(expected)
    )


def test_actual_active_execution_preempts_pending_successor(
    projection_home, monkeypatch
):
    from tests.hermes_cli.test_c60_terminal_revision_selection import revised

    f = revised(projection_home, monkeypatch, active=True)
    workflow = {
        "project_id": "PEPPER",
        "macroproject_id": "P18.9",
        "closed_predecessor_ticket_id": "P18.9.9",
        "current_ticket_id": None,
        "next_ticket_id": "P18.9.10",
        "workflow_status": "completed",
        "P18_9_ready": True,
        "next_action": {
            "id": bridge.canonical_generation_action_id("P18.9.10"),
            "target_ticket_id": "P18.9.10",
        },
    }
    result = bridge.generate_current_ticket(workflow=workflow)
    assert result["generation_status"] == "awaiting_ticket_approval"
    before = bridge.generation_record_path_for_ticket("P18.9.10").read_bytes()
    current = pr.build_workflow_control_snapshot()
    assert current["current_ticket_id"] == f.ticket_id
    assert current["workflow_status"] == "executing"
    assert current["active_execution_count"] == 1
    assert (
        current["next_action"]["id"]
        == pr.governed_ticket_lifecycle_action_ids(f.ticket_id)["monitor_execution"]
    )
    assert bridge.generation_record_path_for_ticket("P18.9.10").read_bytes() == before
    assert bridge.load_approval_decision_record(ticket_id="P18.9.10") is None


def test_live_successor_review_boundary_stops_closure_traversal(chain):
    generate(chain)
    pr.human_git_handoff_completion_record_path_for_ticket("P18.9.9").unlink()
    before = inventory(chain)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.9"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_9_REVIEW"
    assert inventory(chain) == before
    assert bridge.load_approval_decision_record(ticket_id="P18.9.10") is None


def test_cyclic_successor_projection_fails_closed(chain, monkeypatch):
    original = pr._pending_generated_successor_ticket_approval_overlay

    def cyclic(workflow, **kwargs):
        if workflow.get("closed_predecessor_ticket_id") == "P18.9.9":
            return fixtures._c13_review_ready_workflow(
                pr, chain.closed["P18.9.8"].projection
            ), None
        return original(workflow, **kwargs)

    monkeypatch.setattr(
        pr, "_pending_generated_successor_ticket_approval_overlay", cyclic
    )
    before = inventory(chain)
    with pytest.raises(pr.ProductRuntimeConflict, match="traversal contains a cycle"):
        pr.build_workflow_control_snapshot()
    assert inventory(chain) == before
