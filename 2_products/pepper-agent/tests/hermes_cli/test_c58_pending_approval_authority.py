"""Persisted successor approval must be resolved after late predecessor closure."""

import json
from dataclasses import asdict, replace
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)
from tests.hermes_cli.test_c57_post_closure_authority import _late_successor
from tools import pepper_workflow_tools as tools


@pytest.fixture
def scenario(projection_home, tmp_path, monkeypatch):
    original_projection = fixtures._c13_projection_record

    def projection(runtime, ticket_id):
        record = original_projection(runtime, ticket_id)
        record["macroproject_id"] = "P18.9"
        return record

    monkeypatch.setattr(fixtures, "_c13_projection_record", projection)
    original_authority = fixtures._c14_successor_authority

    def canonical_authority(runtime, predecessor):
        authority = original_authority(runtime, predecessor)
        authority["next_action_id"] = bridge.canonical_generation_action_id(
            authority["ticket_id"]
        )
        return authority

    monkeypatch.setattr(fixtures, "_c14_successor_authority", canonical_authority)
    fixture = fixtures._c14_review_authority_fixture(
        pr, tmp_path, monkeypatch, ticket_id="P999.7"
    )
    completion = fixtures._c14_persist_completion_record(pr, fixture)
    real_overlay = pr._pending_generated_successor_ticket_approval_overlay
    _late_successor(
        fixture,
        monkeypatch,
        fixtures._c13_review_ready_workflow(pr, fixture.projection),
    )
    late_overlay = pr._pending_generated_successor_ticket_approval_overlay
    target = generation._synthetic_implementation_target(
        "P999.8",
        fixtures._c9_ticket_title("P999.8"),
        contract=generation._synthetic_implementation_contract("Approval"),
        dependencies=("P999.7",),
    )
    target = replace(
        target, macroproject_id="P18.9", next_action_id=completion["next_action"]["id"]
    )
    authority = asdict(target)
    monkeypatch.setattr(
        bridge,
        "resolve_roadmap_ticket_authorities",
        lambda: (
            {
                **authority,
                "authority_type": target.canonical_roadmap_authority,
                "authority_path": target.roadmap_authority_path,
                "authority_section": target.roadmap_authority_section,
            },
        ),
    )
    monkeypatch.setattr(
        pr,
        "resolve_canonical_next_ticket",
        lambda workflow=None: authority
        if (workflow or {}).get("closed_predecessor_ticket_id") == "P999.7"
        else fixtures._c14_successor_authority(pr, "P999.6"),
    )

    def overlay(workflow, *, allow_current_ticket_projection=False):
        if workflow.get("closed_predecessor_ticket_id") == "P999.7":
            return real_overlay(
                workflow,
                allow_current_ticket_projection=allow_current_ticket_projection,
            )
        return late_overlay(
            workflow, allow_current_ticket_projection=allow_current_ticket_projection
        )

    monkeypatch.setattr(
        pr, "_pending_generated_successor_ticket_approval_overlay", overlay
    )
    return SimpleNamespace(home=projection_home, target=target, completion=completion)


def _generate(scenario):
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == scenario.target.next_action_id
    assert workflow["pending_ticket_approval_count"] == 0
    result = bridge.generate_current_ticket(workflow=workflow, target=scenario.target)
    assert result["generation_status"] == "awaiting_ticket_approval"
    record = bridge.load_generation_record(ticket_id=scenario.target.ticket_id)
    assert record["WorkPacket_compilation_count"] == 1
    assert pr._ticket_approval_work_packet_body(record)["execution_ready"] is False
    return record


def _inventory():
    root = bridge.generation_record_path_for_ticket("P999.8").parent.parent
    return {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    }


def test_c58_pre_generation_retains_durable_closure(scenario):
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"] == scenario.completion["next_action"]
    assert workflow["pending_ticket_approval_count"] == 0
    assert workflow["closed_predecessor_ticket_id"] == "P999.7"
    assert not bridge.generation_record_path_for_ticket("P999.8").exists()


def test_c58_persisted_pending_approval_surfaces_and_explicit_decision(scenario):
    record = _generate(scenario)
    before = _inventory()
    context = pr.build_lead_agent_operational_context()
    assert context["pending_approval_count"] == 1
    assert (context["pending_ticket_approval_count"], context["next_action"]["id"]) == (
        1,
        scenario.target.approval_next_action_id,
    )
    for reader in (
        tools._get_current_ticket,
        tools._get_workflow_control,
        tools._get_next_action,
    ):
        result = json.loads(reader({}))
        assert result["success"] is True
        assert result["next_action"]["id"] == scenario.target.approval_next_action_id
        assert result["current_ticket_id"] == scenario.target.ticket_id
    workflow = context["workflow_control"]
    assert workflow["closed_predecessor_ticket_id"] == "P999.7"
    assert workflow["queue_state"] == "awaiting_human_successor_ticket_approval"
    assert workflow["approval_state"] == "pending_ticket_approval"
    for flag in (
        "ticket_execution_authorized",
        "WorkPacket_execution_authorized",
        "runtime_execution_authorized",
        "worker_execution",
        "Kanban_dispatch",
        "Git_mutation",
    ):
        assert workflow[flag] is False
    pending = json.loads(tools._get_pending_approvals({}))
    assert pending["pending_approval_count"] == 1
    inspected = json.loads(tools._inspect_pending_approval({"approval_id": "P999.8"}))
    assert inspected["success"] is True
    binding = inspected["artifact_inspection"]["approval_binding"]
    publication = pr._ticket_approval_publication_body(record)
    assert binding["TicketSpec_SHA256"] == record["ticket_spec_SHA256"]
    assert binding["WorkPacket_SHA256"] == record["work_packet_SHA256"]
    assert binding["publication_id"] == publication["publication_id"]
    assert binding["publication_revision"] == publication["revision"]
    assert binding["publication_artifact_SHA256"] == publication["artifact_SHA256"]
    assert inspected["decisions"] == []
    assert inspected["auto_approval"] is False
    assert _inventory() == before
    result = json.loads(
        tools._decide_pending_approval({
            "approval_id": "P999.8",
            "ticket_id": "P999.8",
            "decision": "approve",
            "next_action_id": scenario.target.approval_next_action_id,
            "human_decision_text": "I approve P999.8",
            "ticket_spec_sha256": record["ticket_spec_SHA256"],
            "work_packet_sha256": record["work_packet_SHA256"],
        })
    )
    assert result["success"] is True, result
    assert result["pending_ticket_approval_count"] == 0
    assert (
        result["next_action"]["id"]
        == scenario.target.approved_no_execution_next_action_id
    )
    assert bridge.load_approval_decision_record(ticket_id="P999.8") is not None
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    after = _inventory()
    changed = {
        key for key in before.keys() | after.keys() if before.get(key) != after.get(key)
    }
    assert len(changed) == 1
    assert next(iter(changed)).endswith("P999.8.approval-decision.json")


@pytest.mark.parametrize(
    "mutation",
    ["ticket", "revision", "ticket_spec", "work_packet", "publication", "superseded"],
)
def test_c58_mismatched_pending_binding_never_wins(scenario, monkeypatch, mutation):
    record = _generate(scenario)
    pending = json.loads(json.dumps(record))
    if mutation == "ticket":
        pending["ticket_id"] = "P999.9"
    elif mutation == "revision":
        pr._ticket_approval_publication_body(pending)["revision"] += 1
    elif mutation == "ticket_spec":
        pending["ticket_spec_SHA256"] = "f" * 64
    elif mutation == "work_packet":
        pending["work_packet_SHA256"] = "f" * 64
    elif mutation == "publication":
        pr._ticket_approval_publication_body(pending)["artifact_SHA256"] = "f" * 64
    else:
        pr._ticket_approval_publication_body(pending)["supersedes_publication_id"] = (
            "PUB-P999-8-0000"
        )
    monkeypatch.setattr(pr, "_pending_ticket_approval_records", lambda: [pending])
    before = _inventory()
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == scenario.target.next_action_id
    assert workflow["pending_ticket_approval_count"] == 0
    assert any(
        "pending_successor_approval_authority" in item["status"]
        for item in workflow["remaining_blockers"]
    )
    assert _inventory() == before


@pytest.mark.parametrize("decision", ["approve", "reject"])
def test_c58_decided_publication_supersedes_pending(scenario, decision):
    _generate(scenario)
    bridge.apply_ticket_approval_decision(
        ticket_id="P999.8", decision=decision, actor="synthetic-human"
    )
    before = _inventory()
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["pending_ticket_approval_count"] == 0
    assert not pr._pending_ticket_approval_records()
    expected = (
        scenario.target.approved_no_execution_next_action_id
        if decision == "approve"
        else scenario.target.revise_next_action_id
    )
    assert workflow["next_action"]["id"] == expected
    assert _inventory() == before


def test_c58_missing_generation_does_not_promote_orphan_pending(scenario, monkeypatch):
    record = _generate(scenario)
    bridge.generation_record_path_for_ticket("P999.8").unlink()
    monkeypatch.setattr(pr, "_pending_ticket_approval_records", lambda: [record])
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == scenario.target.next_action_id
    assert workflow["pending_ticket_approval_count"] == 0


def test_c58_noncurrent_successor_cannot_gain_approval_authority(scenario, monkeypatch):
    _generate(scenario)
    monkeypatch.setattr(
        pr,
        "resolve_canonical_next_ticket",
        lambda workflow=None: fixtures._c14_successor_authority(pr, "P999.8"),
    )
    before = _inventory()
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] != scenario.target.approval_next_action_id
    assert workflow["pending_ticket_approval_count"] == 0
    assert _inventory() == before


def test_c58_unrelated_request_type_does_not_become_ticket_approval(scenario):
    from tools import write_approval as wa

    wa.stage_write(
        wa.MEMORY,
        {"action": "add", "target": "user", "content": "synthetic memory"},
        summary="Unrelated pending request",
        origin="foreground",
    )
    context = pr.build_lead_agent_operational_context()
    assert context["pending_approval_count"] == 1
    assert context["pending_ticket_approval_count"] == 0
    assert context["next_action"]["id"] == scenario.target.next_action_id
    result = json.loads(
        tools._decide_pending_approval({
            "approval_id": "P999.8",
            "decision": "approve",
            "human_decision_text": "I approve P999.8",
        })
    )
    assert result["success"] is False
    assert not bridge.approval_decision_record_path_for_ticket("P999.8").exists()


@pytest.mark.parametrize(
    "field",
    [
        "ticket_spec_sha256",
        "work_packet_sha256",
        "next_action_id",
        "human_decision_text",
    ],
)
def test_c58_explicit_decision_guards_remain_strict(scenario, field):
    record = _generate(scenario)
    args = {
        "approval_id": "P999.8",
        "decision": "approve",
        "next_action_id": scenario.target.approval_next_action_id,
        "human_decision_text": "I approve P999.8",
        "ticket_spec_sha256": record["ticket_spec_SHA256"],
        "work_packet_sha256": record["work_packet_SHA256"],
    }
    args[field] = "f" * 64 if field.endswith("sha256") else ""
    if field == "next_action_id":
        args[field] = scenario.target.next_action_id
    before = _inventory()
    result = json.loads(tools._decide_pending_approval(args))
    assert result["success"] is False, result
    assert _inventory() == before
    assert not bridge.approval_decision_record_path_for_ticket("P999.8").exists()


@pytest.mark.parametrize(
    "field,value", [("request_type", "memory"), ("status", "approved")]
)
def test_c58_approval_guard_rejects_nonpending_or_wrong_type(scenario, field, value):
    _generate(scenario)
    context = pr.build_lead_agent_operational_context()
    pending = dict(context["approvals"]["items"][0])
    pending[field] = value
    with pytest.raises(ValueError, match="not pending|not a ticket approval"):
        tools._validate_pending_current_ticket_approval(
            context=context, approval=pending
        )
    assert not bridge.approval_decision_record_path_for_ticket("P999.8").exists()


def test_c58_exact_current_pending_guard_accepts_without_deciding(scenario):
    _generate(scenario)
    context = pr.build_lead_agent_operational_context()
    before = _inventory()
    tools._validate_pending_current_ticket_approval(
        context=context, approval=context["approvals"]["items"][0]
    )
    assert _inventory() == before
    assert not bridge.approval_decision_record_path_for_ticket("P999.8").exists()


def test_c58_invalid_persisted_generation_fails_closed(scenario):
    record = _generate(scenario)
    record["ticket_spec_SHA256"] = "f" * 64
    record["bridge_SHA256"] = bridge._record_digest(record)
    path = bridge.generation_record_path_for_ticket("P999.8")
    path.write_text(json.dumps(record), encoding="utf-8")
    before = _inventory()
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == scenario.target.next_action_id
    assert workflow["pending_ticket_approval_count"] == 0
    assert _inventory() == before
