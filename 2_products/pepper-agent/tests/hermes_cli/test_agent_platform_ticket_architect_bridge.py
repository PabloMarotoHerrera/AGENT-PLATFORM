from __future__ import annotations

import json

import pytest

from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.ticket_factory import TicketLintDisposition
from hermes_cli.agent_platform.workflow.governed_state_machine import GovernedWorkflowState


def _workflow(**overrides):
    data = {
        "schema_version": 1,
        "source_system": "pepper-controlled-default-mode-cutover",
        "product_id": "pepper",
        "project_id": "PEPPER",
        "project_name": "Pepper",
        "macroproject_id": "P18.9",
        "macroproject_title": "Pepper Product Personalization",
        "current_ticket_id": None,
        "current_ticket_title": None,
        "current_gap_id": None,
        "current_gap_title": None,
        "next_ticket_id": "P18.9.0",
        "next_ticket_title": bridge.CANONICAL_TICKET_TITLE,
        "workflow_status": "planning_approved_or_intake_ready",
        "queue_state": "ready_to_generate_P18_9_0",
        "P18_9_ready": True,
        "P18_9_ticket_generated": False,
        "next_action": {
            "id": "GENERATE_P18_9_0",
            "label": "Generate governed P18.9.0 before execution.",
            "target_ticket_id": "P18.9.0",
            "target_ticket_title": bridge.CANONICAL_TICKET_TITLE,
        },
    }
    data.update(overrides)
    return data


@pytest.fixture
def bridge_home(tmp_path, monkeypatch):
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    return home


def _chat_tool_result(name: str, args: dict | None = None) -> dict:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    return json.loads(handle_function_call(name, args or {}))


def test_generate_p18_9_0_bridge_success_and_persists(bridge_home) -> None:
    result = bridge.generate_p18_9_0_ticket(workflow=_workflow())
    record = bridge.load_p18_9_0_generation_record()

    assert result["idempotent_replay"] is False
    assert result["ticket_id"] == "P18.9.0"
    assert result["ticket_title"] == bridge.CANONICAL_TICKET_TITLE
    assert result["workflow_status"] == "awaiting_ticket_approval"
    assert result["human_ticket_approval_required"] is True
    assert result["execution_ready"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert bridge.generation_record_path().exists()
    assert record is not None
    assert record["ticket_spec"]["title"] == bridge.CANONICAL_TICKET_TITLE
    assert record["lint_report"]["disposition"] == TicketLintDisposition.PASS.value
    assert record["WorkPacket_compilation_count"] == 1
    assert record["work_packet_compilation_result"]["work_packet"]["execution_ready"] is False
    assert record["workflow_transition_result"]["transition"]["transition_id"] == "GWT-002"
    assert (
        record["workflow_transition_result"]["resulting_snapshot"]["current_state"]
        == GovernedWorkflowState.AWAITING_TICKET_APPROVAL.value
    )


def test_generation_is_idempotent_without_recompiling(bridge_home, monkeypatch) -> None:
    calls = []
    original = bridge.compile_ticket_spec_to_work_packet

    def counting_compile(request):
        calls.append(request)
        return original(request)

    monkeypatch.setattr(bridge, "compile_ticket_spec_to_work_packet", counting_compile)

    first = bridge.generate_p18_9_0_ticket(workflow=_workflow())
    second = bridge.generate_p18_9_0_ticket(workflow=_workflow(workflow_status="awaiting_ticket_approval"))

    assert first["idempotent_replay"] is False
    assert second["idempotent_replay"] is True
    assert len(calls) == 1
    assert first["authority"] == second["authority"]


def test_stale_workflow_title_does_not_override_canonical_roadmap(bridge_home) -> None:
    workflow = _workflow(
        next_ticket_title="Product UX / IA Baseline",
        next_action={
            "id": "GENERATE_P18_9_0",
            "label": "Generate governed P18.9.0 Product UX / IA Baseline before execution.",
            "target_ticket_id": "P18.9.0",
            "target_ticket_title": "Product UX / IA Baseline",
        },
    )

    result = bridge.generate_p18_9_0_ticket(workflow=workflow)
    record = bridge.load_p18_9_0_generation_record()

    assert result["ticket_title"] == bridge.CANONICAL_TICKET_TITLE
    assert record is not None
    assert record["ticket_spec"]["title"] == bridge.CANONICAL_TICKET_TITLE
    serialized = json.dumps(record)
    assert "Product UX / IA Baseline" in serialized
    assert record["canonical_roadmap_authority"] == "human-approved-p18.9-roadmap"


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"requested_project_id": "P18"}, "requested project"),
        ({"requested_ticket_id": "P18.9.1"}, "requested ticket"),
        ({"requested_next_action_id": "APPROVE_P18_9_0"}, "requested next action"),
    ],
)
def test_wrong_requested_identity_rejects_without_record(bridge_home, kwargs, message) -> None:
    with pytest.raises(bridge.TicketArchitectBridgeInputError, match=message):
        bridge.generate_p18_9_0_ticket(workflow=_workflow(), **kwargs)

    assert bridge.load_p18_9_0_generation_record() is None


@pytest.mark.parametrize(
    "workflow",
    [
        _workflow(project_id="OTHER"),
        _workflow(macroproject_id="P18.8"),
        _workflow(current_ticket_id="P18.8"),
        _workflow(P18_9_ready=False),
        _workflow(next_action={"id": "APPROVE_P18_9_0", "target_ticket_id": "P18.9.0"}),
        _workflow(next_action={"id": "GENERATE_P18_9_0", "target_ticket_id": "P18.9.1"}),
    ],
)
def test_wrong_workflow_state_rejects_without_record(bridge_home, workflow) -> None:
    with pytest.raises(bridge.TicketArchitectBridgeError):
        bridge.generate_p18_9_0_ticket(workflow=workflow)

    assert bridge.load_p18_9_0_generation_record() is None


def test_compiler_failure_preserves_prior_workflow_state(bridge_home, monkeypatch) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    def fail_compile(_request):
        raise RuntimeError("compiler unavailable")

    monkeypatch.setattr(bridge, "compile_ticket_spec_to_work_packet", fail_compile)

    with pytest.raises(bridge.TicketArchitectBridgeGenerationError):
        bridge.generate_p18_9_0_ticket(workflow=_workflow())

    assert bridge.load_p18_9_0_generation_record() is None
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["current_ticket_id"] is None
    assert snapshot["workflow_status"] == "planning_approved_or_intake_ready"
    assert snapshot["P18_9_ticket_generated"] is False


def test_product_runtime_projects_generated_ticket_after_bridge(bridge_home, monkeypatch) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_execution_operational_summary",
        lambda: {
            "execution_state": "no_active_executions",
            "execution_count": 0,
            "active_execution_count": 0,
            "source_system": pr.CONTROLLED_EXECUTION_SOURCE_SYSTEM,
        },
    )

    generated = pr.generate_current_governed_ticket(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="GENERATE_P18_9_0",
    )
    snapshot = pr.build_workflow_control_snapshot()
    context = pr.build_lead_agent_operational_context()

    assert generated["idempotent_replay"] is False
    assert snapshot["current_ticket_id"] == "P18.9.0"
    assert snapshot["current_ticket_title"] == bridge.CANONICAL_TICKET_TITLE
    assert snapshot["workflow_status"] == "awaiting_ticket_approval"
    assert snapshot["approval_state"] == "pending_ticket_approval"
    assert snapshot["pending_approval_count"] == 1
    assert snapshot["pending_ticket_approval_count"] == 1
    assert snapshot["next_action"]["id"] == "APPROVE_P18_9_0"
    assert snapshot["P18_9_ticket_generated"] is True
    assert snapshot["worker_execution"] is False
    assert context["available"] is True
    assert context["current_ticket_id"] == "P18.9.0"
    assert context["approval_state"] == "pending_ticket_approval"
    assert context["pending_approval_count"] == 1
    assert context["approvals"]["items"][0]["id"] == "P18.9.0"


def test_generated_ticket_publishes_one_canonical_pending_approval(bridge_home) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    inbox = pr.build_approval_inbox_source()
    approvals = inbox["approvals"]

    assert inbox["source_system"] == pr.APPROVAL_SOURCE_SYSTEM
    assert [item["id"] for item in approvals] == ["P18.9.0"]
    assert approvals[0]["request_type"] == "ticket_approval"
    assert approvals[0]["status"] == "pending"
    assert approvals[0]["target"]["label"].startswith("P18.9.0")
    assert "payload" not in json.dumps(inbox).lower()


def test_generated_ticket_approval_detail_binds_ticket_and_work_packet_authority(bridge_home) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())
    record = bridge.load_p18_9_0_generation_record()
    assert record is not None

    detail = pr.build_approval_detail_source("P18.9.0")
    evidence = {item["id"]: item["label"] for item in detail["evidence"]}

    assert detail["approval"]["id"] == "P18.9.0"
    assert detail["approval"]["request_type"] == "ticket_approval"
    assert detail["approval"]["reason"].count("executes") == 1
    assert record["bridge_SHA256"] in evidence["P18.9.0:bridge"]
    assert record["ticket_spec_SHA256"] in evidence["P18.9.0:ticket_spec"]
    assert record["work_packet_id"] in evidence["P18.9.0:work_packet"]
    assert record["work_packet_SHA256"] in evidence["P18.9.0:work_packet"]
    assert detail["decisions"] == []


def test_p18_9_0_ticket_approve_persists_without_recompiling_or_executing(
    bridge_home,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())
    generated = bridge.load_p18_9_0_generation_record()
    assert generated is not None

    def fail_compile(_request):
        raise AssertionError("approval decision must not recompile WorkPacket")

    monkeypatch.setattr(bridge, "compile_ticket_spec_to_work_packet", fail_compile)

    result = pr.apply_approval_decision(
        "P18.9.0",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )
    decision = bridge.load_p18_9_0_approval_decision_record()
    snapshot = pr.build_workflow_control_snapshot()

    assert result["status"] == "approved"
    assert result["workflow_transition_id"] == "GWT-003"
    assert result["worker_execution"] is False
    assert decision is not None
    assert decision["decision"] == "approve"
    assert decision["ticket_publication_result"] is not None
    assert decision["workflow_transition_result"]["transition"]["transition_id"] == "GWT-003"
    assert decision["ticket_spec_SHA256"] == generated["ticket_spec_SHA256"]
    assert decision["work_packet_id"] == generated["work_packet_id"]
    assert decision["work_packet_SHA256"] == generated["work_packet_SHA256"]
    assert decision["WorkPacket_compilation_count"] == 1
    assert decision["WorkPacket_recompile_required"] is False
    assert decision["worker_execution"] is False
    assert decision["Kanban_dispatch"] is False
    assert decision["Git_mutation"] is False
    assert pr.build_approval_inbox_source()["approvals"] == []
    assert snapshot["workflow_status"] == "ticket_approved"
    assert snapshot["pending_approval_count"] == 0
    assert snapshot["pending_ticket_approval_count"] == 0
    assert snapshot["P18_9_ticket_approved"] is True


def test_p18_9_0_ticket_reject_persists_without_publication_or_execution(bridge_home) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    result = pr.apply_approval_decision(
        "P18.9.0",
        pr.ApprovalDecisionRequest(decision="reject", actor="human.p18.9"),
    )
    decision = bridge.load_p18_9_0_approval_decision_record()
    snapshot = pr.build_workflow_control_snapshot()

    assert result["status"] == "rejected"
    assert result["workflow_transition_id"] == "GWT-025"
    assert decision is not None
    assert decision["decision"] == "reject"
    assert decision["ticket_publication_result"] is None
    assert decision["workflow_transition_result"]["transition"]["transition_id"] == "GWT-025"
    assert decision["worker_execution"] is False
    assert decision["Kanban_dispatch"] is False
    assert decision["Git_mutation"] is False
    assert snapshot["workflow_status"] == "awaiting_correction"
    assert snapshot["pending_ticket_approval_count"] == 0
    assert snapshot["P18_9_ticket_approved"] is False


def test_p18_9_0_ticket_approval_second_decision_is_not_pending(bridge_home) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())
    pr.apply_approval_decision(
        "P18.9.0",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )

    replay = pr.apply_approval_decision(
        "P18.9.0",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )
    assert replay["status"] == "approved"
    assert replay["idempotent_replay"] is True
    assert replay["applied"] is False

    with pytest.raises(pr.ProductRuntimeConflict):
        pr.apply_approval_decision(
            "P18.9.0",
            pr.ApprovalDecisionRequest(decision="reject", actor="human.p18.9"),
        )


def test_chat_explicit_approve_current_ticket_uses_canonical_backend_without_execution(
    bridge_home,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    def fail_compile(_request):
        raise AssertionError("chat approval must not recompile WorkPacket")

    monkeypatch.setattr(bridge, "compile_ticket_spec_to_work_packet", fail_compile)

    result = _chat_tool_result(
        "decide_pending_approval",
        {
            "decision": "approve",
            "human_decision_text": "Apruebo P18.9.0",
            "approval_id": "P18.9.0",
            "project_id": "PEPPER",
            "ticket_id": "P18.9.0",
            "next_action_id": "APPROVE_P18_9_0",
        },
    )
    decision = bridge.load_p18_9_0_approval_decision_record()
    workflow = pr.build_workflow_control_snapshot()

    assert result["success"] is True
    assert result["source_tool"] == "decide_pending_approval"
    assert result["status"] == "approved"
    assert result["workflow_transition_id"] == "GWT-003"
    assert result["workflow_status"] == "ticket_approved"
    assert result["pending_approval_count"] == 0
    assert result["pending_ticket_approval_count"] == 0
    assert result["WorkPacket_recompile_required"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert decision is not None
    assert decision["decision"] == "approve"
    assert decision["WorkPacket_compilation_count"] == 1
    assert decision["worker_execution"] is False
    assert decision["Kanban_dispatch"] is False
    assert decision["Git_mutation"] is False
    assert pr.build_approval_inbox_source()["approvals"] == []
    assert workflow["workflow_status"] == "ticket_approved"
    assert workflow["next_action"]["id"] == "P18_9_0_APPROVED_NO_EXECUTION"
    assert workflow["worker_execution"] is False
    assert workflow["Kanban_dispatch"] is False
    assert workflow["Git_mutation"] is False


def test_chat_explicit_reject_current_ticket_uses_canonical_backend_without_execution(
    bridge_home,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    result = _chat_tool_result(
        "decide_pending_approval",
        {
            "decision": "reject",
            "human_decision_text": "Reject P18.9.0",
            "approval_id": "P18.9.0",
            "project_id": "PEPPER",
            "ticket_id": "P18.9.0",
            "next_action_id": "APPROVE_P18_9_0",
        },
    )
    decision = bridge.load_p18_9_0_approval_decision_record()
    workflow = pr.build_workflow_control_snapshot()

    assert result["success"] is True
    assert result["status"] == "rejected"
    assert result["workflow_transition_id"] == "GWT-025"
    assert result["workflow_status"] == "awaiting_correction"
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert decision is not None
    assert decision["decision"] == "reject"
    assert decision["ticket_publication_result"] is None
    assert workflow["workflow_status"] == "awaiting_correction"
    assert workflow["next_action"]["id"] == "REVISE_P18_9_0"
    assert workflow["worker_execution"] is False
    assert workflow["Kanban_dispatch"] is False
    assert workflow["Git_mutation"] is False


@pytest.mark.parametrize(
    "text",
    [
        "Que pasa si lo apruebo?",
        "Muestrame la aprobacion",
        "Esta listo?",
        "Creo que esta bien",
    ],
)
def test_chat_ambiguous_or_non_decision_language_does_not_approve(
    bridge_home,
    text,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    result = _chat_tool_result(
        "decide_pending_approval",
        {"decision": "approve", "human_decision_text": text},
    )

    assert result["success"] is False
    assert bridge.load_p18_9_0_approval_decision_record() is None
    assert [item["id"] for item in pr.build_approval_inbox_source()["approvals"]] == ["P18.9.0"]


def test_chat_approval_target_mismatch_is_rejected_before_decision(
    bridge_home,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    def malformed_inbox():
        return {
            "source_system": pr.APPROVAL_SOURCE_SYSTEM,
            "approvals": [
                {
                    "id": "P18.9.0",
                    "status": "pending",
                    "request_type": "ticket_approval",
                    "target": {"type": "runtime_action", "label": "P18.8 stale target"},
                }
            ],
        }

    def fail_apply(_approval_id, _request):
        raise AssertionError("target mismatch must not reach canonical apply")

    monkeypatch.setattr(pr, "build_approval_inbox_source", malformed_inbox)
    monkeypatch.setattr(pr, "apply_approval_decision", fail_apply)

    result = _chat_tool_result(
        "decide_pending_approval",
        {"decision": "approve", "human_decision_text": "Apruebo P18.9.0"},
    )

    assert result["success"] is False
    assert "target" in result["error"]
    assert bridge.load_p18_9_0_approval_decision_record() is None


def test_chat_duplicate_same_decision_is_idempotent_and_opposite_conflicts(
    bridge_home,
) -> None:
    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    first = _chat_tool_result(
        "decide_pending_approval",
        {"decision": "approve", "human_decision_text": "Apruebo P18.9.0"},
    )
    replay = _chat_tool_result(
        "decide_pending_approval",
        {"decision": "approve", "human_decision_text": "Apruebo P18.9.0"},
    )
    opposite = _chat_tool_result(
        "decide_pending_approval",
        {"decision": "reject", "human_decision_text": "Reject P18.9.0"},
    )
    decision = bridge.load_p18_9_0_approval_decision_record()

    assert first["status"] == "approved"
    assert first["idempotent_replay"] is False
    assert replay["status"] == "approved"
    assert replay["idempotent_replay"] is True
    assert replay["applied"] is False
    assert opposite["success"] is False
    assert "opposite" in opposite["error"]
    assert decision is not None
    assert decision["decision"] == "approve"
