from __future__ import annotations

import json

import pytest

from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.ticket_factory import TicketLintDisposition
from hermes_cli.agent_platform.workflow.governed_state_machine import GovernedWorkflowState


P18_9_1_IMPLEMENTATION_TITLE = "Pepper Shell, Routing, and Compact Navigation"


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


def _next_ticket_workflow(**overrides):
    data = _workflow(
        current_ticket_id=None,
        current_ticket_title=None,
        next_ticket_id="P18.9.1",
        next_ticket_title="Pepper Design System",
        workflow_state="P18.9.0-COMPLETED",
        workflow_status="completed",
        queue_state="p18_9_0_closed_next_ticket_ready",
        validation_state="review_accepted",
        review_state="accepted",
        P18_9_ticket_generated=True,
        P18_9_0_closed=True,
        next_ticket_ready=True,
        next_ticket_generated=False,
        next_action={
            "id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
            "label": "Generate governed P18.9.1 Pepper Design System.",
            "target_ticket_id": "P18.9.1",
            "target_ticket_title": "Pepper Design System",
            "required_human_action": "ticket_generation",
        },
    )
    data.update(overrides)
    return data


def _synthetic_roadmap_items() -> tuple[dict[str, object], ...]:
    return (
        {
            "ticket_id": "TEST.1",
            "ticket_title": "Synthetic Predecessor",
            "authority_path": "synthetic-roadmap.md",
            "authority_section": "Synthetic roadmap",
            "authority_type": "synthetic_test_roadmap",
            "next_action_id": "GENERATE_TEST_1_REQUIRES_SEPARATE_HUMAN_ACTION",
            "dependency_ticket_ids": (),
        },
        {
            "ticket_id": "TEST.2",
            "ticket_title": "Synthetic Successor",
            "authority_path": "synthetic-roadmap.md",
            "authority_section": "Synthetic roadmap",
            "authority_type": "synthetic_test_roadmap",
            "next_action_id": "GENERATE_TEST_2_REQUIRES_SEPARATE_HUMAN_ACTION",
            "dependency_ticket_ids": ("TEST.1",),
        },
        {
            "ticket_id": "TEST.3",
            "ticket_title": "Synthetic Future",
            "authority_path": "synthetic-roadmap.md",
            "authority_section": "Synthetic roadmap",
            "authority_type": "synthetic_test_roadmap",
            "next_action_id": "GENERATE_TEST_3_REQUIRES_SEPARATE_HUMAN_ACTION",
            "dependency_ticket_ids": ("TEST.2",),
        },
    )


@pytest.fixture
def bridge_home(tmp_path, monkeypatch):
    home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(home))
    return home


def _chat_tool_result(name: str, args: dict | None = None) -> dict:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    return json.loads(handle_function_call(name, args or {}))


def _write_generation_record(record: dict) -> None:
    bridge.generation_record_path_for_ticket(record["ticket_id"]).write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _make_stale_future_generation_record() -> dict:
    bridge.generate_current_ticket(workflow=_next_ticket_workflow())
    record = bridge.load_generation_record(ticket_id="P18.9.1")
    assert record is not None
    record["roadmap_authority_path"] = "2_products/pepper-agent/docs/agent-platform/stale_roadmap.md"
    record["bridge_SHA256"] = bridge._record_digest(record)
    _write_generation_record(record)
    return record


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
    assert "Product UX / IA Baseline" not in serialized
    assert record["canonical_roadmap_authority"] == "human-approved-p18.9-roadmap"


def test_historical_p18_9_0_record_without_top_level_roadmap_path_remains_valid(bridge_home) -> None:
    bridge.generate_p18_9_0_ticket(workflow=_workflow())
    record = bridge.load_p18_9_0_generation_record()
    assert record is not None

    record.pop("roadmap_authority_path", None)
    record.pop("roadmap_authority_section", None)
    record["bridge_SHA256"] = bridge._record_digest(record)
    _write_generation_record(record)

    validated = bridge.load_p18_9_0_generation_record()

    assert validated is not None
    assert validated["ticket_id"] == "P18.9.0"
    assert validated["canonical_roadmap_authority"] == bridge.CANONICAL_ROADMAP_AUTHORITY


def test_generic_generation_resolves_canonical_next_ticket_from_roadmap(bridge_home) -> None:
    workflow = _next_ticket_workflow()
    authority = bridge.resolve_canonical_next_ticket(workflow)
    result = bridge.generate_current_ticket(workflow=workflow)
    record = bridge.load_generation_record(ticket_id="P18.9.1")

    assert result["idempotent_replay"] is False
    assert result["ticket_id"] == "P18.9.1"
    assert result["ticket_title"] == P18_9_1_IMPLEMENTATION_TITLE
    assert result["roadmap_authority_path"] == bridge.CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH
    assert result["roadmap_authority_section"] == "P18.9 Implementation Roadmap Authority"
    assert result["roadmap_dependency_ticket_ids"] == ["P18.9.0"]
    assert result["workflow_status"] == "awaiting_ticket_approval"
    assert result["next_action"]["id"] == "APPROVE_P18_9_1"
    assert result["human_ticket_approval_required"] is True
    assert result["execution_ready"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert bridge.generation_record_path_for_ticket("P18.9.1").exists()
    assert record is not None
    assert record["predecessor_ticket_id"] == "P18.9.0"
    assert record["canonical_next_ticket_authority"] == authority.asdict()
    assert record["canonical_roadmap_authority"] == bridge.CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY
    assert record["roadmap_dependency_ticket_ids"] == ["P18.9.0"]
    assert record["canonical_next_ticket_authority"]["dependency_ticket_ids"] == ["P18.9.0"]
    assert record["ticket_spec"]["ticket_id"] == "P18.9.1"
    assert record["ticket_spec"]["title"] == P18_9_1_IMPLEMENTATION_TITLE
    assert record["ticket_spec"]["dependencies"] == []
    assert record["dependency_plan"]["ticket_ids"] == ["P18.9.1"]
    assert record["dependency_plan"]["edges"] == []
    assert record["lint_report"]["disposition"] == TicketLintDisposition.PASS.value
    assert record["work_packet_compilation_result"]["work_packet"]["execution_ready"] is False
    assert record["WorkPacket_compilation_count"] == 1
    assert record["workflow_transition_result"]["transition"]["transition_id"] == "GWT-002"


def test_future_generation_rejects_stale_roadmap_authority_record(bridge_home) -> None:
    bridge.generate_current_ticket(workflow=_next_ticket_workflow())
    record = bridge.load_generation_record(ticket_id="P18.9.1")
    assert record is not None

    record["roadmap_authority_path"] = "2_products/pepper-agent/docs/agent-platform/stale_roadmap.md"
    record["bridge_SHA256"] = bridge._record_digest(record)
    bridge.generation_record_path_for_ticket("P18.9.1").write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(bridge.TicketArchitectBridgeConflict, match="roadmap_authority_path"):
        bridge.load_generation_record(ticket_id="P18.9.1")
    with pytest.raises(bridge.TicketArchitectBridgeConflict, match="roadmap_authority_path"):
        bridge.generate_current_ticket(workflow=_next_ticket_workflow())

    record["roadmap_authority_path"] = bridge.CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH
    record["canonical_next_ticket_authority"]["roadmap_authority_path"] = (
        "2_products/pepper-agent/docs/agent-platform/stale_roadmap.md"
    )
    record["bridge_SHA256"] = bridge._record_digest(record)
    bridge.generation_record_path_for_ticket("P18.9.1").write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(bridge.TicketArchitectBridgeConflict, match="canonical_next_ticket_authority"):
        bridge.load_generation_record(ticket_id="P18.9.1")


def test_future_generation_rejects_stale_source_next_action_record(bridge_home) -> None:
    bridge.generate_current_ticket(workflow=_next_ticket_workflow())
    record = bridge.load_generation_record(ticket_id="P18.9.1")
    assert record is not None

    record["source_next_action_id"] = "GENERATE_P18_9_1_STALE_ACTION"
    record["idempotency_key"] = "PEPPER:P18.9:P18.9.1:GENERATE_P18_9_1_STALE_ACTION"
    record["bridge_SHA256"] = bridge._record_digest(record)
    bridge.generation_record_path_for_ticket("P18.9.1").write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(bridge.TicketArchitectBridgeConflict, match="source_next_action_id"):
        bridge.load_generation_record(ticket_id="P18.9.1")


def test_stale_future_authority_can_be_reconciled_without_generation(bridge_home, monkeypatch) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    stale = _make_stale_future_generation_record()
    before = bridge.inspect_invalid_future_ticket_authority(ticket_id="P18.9.1")

    assert before["classification"] == "unaccepted_partial_failed_future_ticket_authority"
    assert before["reconcilable"] is True
    assert before["actual_roadmap_authority_path"].endswith("stale_roadmap.md")
    assert before["expected_roadmap_authority_path"] == bridge.CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH
    assert before["ticket_spec_SHA256"] == stale["ticket_spec_SHA256"]
    assert before["work_packet_id"] == stale["work_packet_id"]
    assert before["generation_completed_structurally"] is True

    result = bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.1")
    real_snapshot = pr.build_workflow_control_snapshot
    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (
            {
                "current_ticket_id": None,
                "current_ticket_title": None,
                "next_ticket_id": "P18.9.1",
                "next_ticket_title": "Pepper Design System",
                "workflow_state": "P18.9.0-COMPLETED",
                "workflow_status": "completed",
                "validation_state": "review_accepted",
                "review_state": "accepted",
                "review_acceptance_authority": {"ticket_closed": True},
                "P18_9_0_closed": True,
                "P18_9_0_completed": True,
                "next_ticket_ready": True,
                "next_ticket_generated": False,
                "next_action": {
                    "id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
                    "target_ticket_id": "P18.9.1",
                    "target_ticket_title": "Pepper Design System",
                },
            },
            None,
        ),
    )
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", real_snapshot)
    workflow_tool = _chat_tool_result("get_workflow_control")
    next_action_tool = _chat_tool_result("get_next_action")

    assert result["reconciled"] is True
    assert result["ticket_generated"] is False
    assert result["fresh_generation_required"] is True
    assert bridge.load_generation_record(ticket_id="P18.9.1") is None
    assert not bridge.generation_record_path_for_ticket("P18.9.1").exists()
    quarantine = bridge.quarantined_generation_record_path(
        ticket_id="P18.9.1",
        bridge_sha256=stale["bridge_SHA256"],
    )
    assert quarantine.exists()
    retained = json.loads(quarantine.read_text(encoding="utf-8"))
    assert retained["bridge_SHA256"] == stale["bridge_SHA256"]
    history_lines = bridge.reconciliation_history_path_for_ticket("P18.9.1").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(history_lines) == 1
    history = json.loads(history_lines[0])
    assert history["bridge_SHA256"] == stale["bridge_SHA256"]
    assert history["actual_roadmap_authority_path"].endswith("stale_roadmap.md")
    assert workflow_tool["next_ticket_id"] == "P18.9.1"
    assert workflow_tool["next_ticket_title"] == P18_9_1_IMPLEMENTATION_TITLE
    assert workflow_tool["current_ticket_id"] is None
    assert next_action_tool["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert next_action_tool["next_ticket_id"] == "P18.9.1"


def test_runtime_and_chat_tool_reconcile_stale_current_generation_authority(
    bridge_home,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    stale = _make_stale_future_generation_record()
    real_snapshot = pr.build_workflow_control_snapshot
    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (
            {
                "current_ticket_id": None,
                "current_ticket_title": None,
                "next_ticket_id": "P18.9.1",
                "next_ticket_title": "Pepper Design System",
                "workflow_state": "P18.9.0-COMPLETED",
                "workflow_status": "completed",
                "validation_state": "review_accepted",
                "review_state": "accepted",
                "review_acceptance_authority": {"ticket_closed": True},
                "P18_9_0_closed": True,
                "P18_9_0_completed": True,
                "next_ticket_ready": True,
                "next_ticket_generated": False,
                "next_action": {
                    "id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
                    "target_ticket_id": "P18.9.1",
                    "target_ticket_title": "Pepper Design System",
                },
            },
            None,
        ),
    )
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", real_snapshot)

    result = _chat_tool_result(
        "reconcile_invalid_current_generation_authority",
        {
            "human_request_text": "Reconcile stale generated authority for P18.9.1.",
            "project_id": "PEPPER",
            "ticket_id": "P18.9.1",
        },
    )

    assert result["success"] is True
    assert result["source_tool"] == "reconcile_invalid_current_generation_authority"
    assert result["reconciled"] is True
    assert result["bridge_SHA256"] == stale["bridge_SHA256"]
    assert result["ticket_generated"] is False
    assert result["current_ticket_id"] is None
    assert result["next_ticket_id"] == "P18.9.1"
    assert result["next_ticket_title"] == P18_9_1_IMPLEMENTATION_TITLE
    assert result["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert bridge.load_generation_record(ticket_id="P18.9.1") is None


def test_stale_future_authority_reconciliation_is_idempotent(bridge_home) -> None:
    stale = _make_stale_future_generation_record()
    first = bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.1")
    second = bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.1")
    history_lines = bridge.reconciliation_history_path_for_ticket("P18.9.1").read_text(
        encoding="utf-8"
    ).splitlines()

    assert first["reconciled"] is True
    assert second["classification"] == "no_future_ticket_generation_authority"
    assert second["idempotent_replay"] is False
    assert len(history_lines) == 1
    assert bridge.quarantined_generation_record_path(
        ticket_id="P18.9.1",
        bridge_sha256=stale["bridge_SHA256"],
    ).exists()


@pytest.mark.parametrize(
    "mutation, message",
    [
        (lambda record: record.__setitem__("human_ticket_approval_present", True), "approval"),
        (lambda record: record.__setitem__("Kanban_dispatch", True), "Kanban_dispatch"),
        (lambda record: record.__setitem__("worker_execution", True), "worker_execution"),
    ],
)
def test_stale_future_authority_with_later_boundary_cannot_reconcile(
    bridge_home,
    mutation,
    message,
) -> None:
    record = _make_stale_future_generation_record()
    mutation(record)
    record["bridge_SHA256"] = bridge._record_digest(record)
    _write_generation_record(record)

    with pytest.raises(bridge.TicketArchitectBridgeConflict, match=message):
        bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.1")

    assert bridge.generation_record_path_for_ticket("P18.9.1").exists()
    assert not bridge.reconciliation_history_path_for_ticket("P18.9.1").exists()


def test_stale_future_authority_with_downstream_projection_cannot_reconcile(bridge_home) -> None:
    _make_stale_future_generation_record()
    projection_path = bridge_home / "agent-platform" / "pepper-future-projection" / "P18.9.1.projection.json"
    projection_path.parent.mkdir(parents=True)
    projection_path.write_text(
        json.dumps({"ticket_id": "P18.9.1", "Kanban_dispatch": False}),
        encoding="utf-8",
    )

    with pytest.raises(bridge.TicketArchitectBridgeConflict, match="downstream authority"):
        bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.1")

    assert bridge.generation_record_path_for_ticket("P18.9.1").exists()


def test_valid_future_authority_and_historical_p18_9_0_are_not_reconciled(bridge_home) -> None:
    bridge.generate_current_ticket(workflow=_next_ticket_workflow())
    valid = bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.1")

    assert valid["classification"] == "valid_current_generated_authority"
    assert valid["reconciled"] is False
    assert bridge.load_generation_record(ticket_id="P18.9.1") is not None
    assert not bridge.reconciliation_history_path_for_ticket("P18.9.1").exists()

    bridge.generate_p18_9_0_ticket(workflow=_workflow())
    with pytest.raises(bridge.TicketArchitectBridgeInputError, match="historical"):
        bridge.reconcile_invalid_future_ticket_authority(ticket_id="P18.9.0")
    assert bridge.load_p18_9_0_generation_record() is not None


def test_closed_p18_9_0_resolves_p18_9_1_across_runtime_and_generation(
    bridge_home,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (
            {
                "current_ticket_id": None,
                "current_ticket_title": None,
                "next_ticket_id": "P18.9.1",
                "next_ticket_title": "Pepper Design System",
                "readiness": "p18_9_0_completed_next_ticket_ready",
                "workflow_state": "P18.9.0-COMPLETED",
                "workflow_status": "completed",
                "queue_state": "p18_9_0_closed_next_ticket_ready",
                "validation_state": "review_accepted",
                "review_state": "accepted",
                "recovery_state": "not_required",
                "git_handoff_state": "not_required_for_ticket_result",
                "review_acceptance_authority": {"ticket_closed": True},
                "P18_9_0_closed": True,
                "P18_9_0_completed": True,
                "next_ticket_ready": True,
                "next_ticket_generated": False,
                "human_acceptance_recorded": True,
                "next_action": {
                    "id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
                    "target_ticket_id": "P18.9.1",
                    "target_ticket_title": "Pepper Design System",
                },
            },
            None,
        ),
    )

    workflow = pr.build_workflow_control_snapshot()
    runtime_authority = pr.resolve_canonical_next_ticket(workflow)
    bridge_authority = bridge.resolve_canonical_next_ticket(workflow)
    workflow_tool = _chat_tool_result("get_workflow_control")
    next_action_tool = _chat_tool_result("get_next_action")
    generated = pr.generate_current_governed_ticket(
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
    )

    assert workflow["next_ticket_id"] == "P18.9.1"
    assert workflow["next_ticket_title"] == P18_9_1_IMPLEMENTATION_TITLE
    assert workflow["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert workflow_tool["workflow_control"]["next_ticket_id"] == workflow["next_ticket_id"]
    assert workflow_tool["workflow_control"]["next_ticket_title"] == workflow["next_ticket_title"]
    assert workflow_tool["next_ticket_id"] == workflow["next_ticket_id"]
    assert workflow_tool["next_ticket_title"] == workflow["next_ticket_title"]
    assert workflow_tool["next_action"]["id"] == workflow["next_action"]["id"]
    assert next_action_tool["next_ticket_id"] == workflow["next_ticket_id"]
    assert next_action_tool["next_ticket_title"] == workflow["next_ticket_title"]
    assert next_action_tool["next_action"]["id"] == workflow["next_action"]["id"]
    assert next_action_tool["next_action"]["target_ticket_id"] == workflow["next_ticket_id"]
    assert next_action_tool["next_action"]["target_ticket_title"] == workflow["next_ticket_title"]
    assert runtime_authority["ticket_id"] == workflow["next_ticket_id"]
    assert runtime_authority["ticket_title"] == workflow["next_ticket_title"]
    assert runtime_authority["next_action_id"] == workflow["next_action"]["id"]
    assert bridge_authority.ticket_id == workflow["next_ticket_id"]
    assert bridge_authority.ticket_title == workflow["next_ticket_title"]
    assert bridge_authority.next_action_id == workflow["next_action"]["id"]
    assert generated["ticket_id"] == workflow["next_ticket_id"]
    assert generated["ticket_title"] == workflow["next_ticket_title"]
    assert generated["next_action"]["id"] == "APPROVE_P18_9_1"
    assert generated["human_ticket_approval_present"] is False
    assert generated["worker_execution"] is False
    assert generated["Kanban_dispatch"] is False
    assert generated["Git_mutation"] is False


def test_stale_bootstrap_p18_9_0_cannot_override_closed_workflow_state(bridge_home) -> None:
    stale = _next_ticket_workflow(
        next_ticket_id="P18.9.0",
        next_ticket_title=bridge.CANONICAL_TICKET_TITLE,
        next_action={
            "id": "GENERATE_P18_9_0",
            "target_ticket_id": "P18.9.0",
            "target_ticket_title": bridge.CANONICAL_TICKET_TITLE,
        },
    )

    authority = bridge.resolve_canonical_next_ticket(stale)
    accepted = bridge.generate_current_ticket(
        workflow=stale,
        requested_ticket_id="P18.9.1",
        requested_next_action_id="GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
    )

    assert authority.ticket_id == "P18.9.1"
    assert authority.ticket_title == P18_9_1_IMPLEMENTATION_TITLE
    assert authority.next_action_id == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert authority.predecessor_ticket_id == "P18.9.0"
    assert accepted["ticket_id"] == "P18.9.1"
    assert bridge.load_generation_record(ticket_id="P18.9.0") is None


def test_generic_generation_rejects_wrong_requested_ticket_and_wrong_next_action(bridge_home) -> None:
    with pytest.raises(bridge.TicketArchitectBridgeInputError, match="requested ticket"):
        bridge.generate_current_ticket(
            workflow=_next_ticket_workflow(),
            requested_ticket_id="P18.9.2",
        )

    with pytest.raises(bridge.TicketArchitectBridgeInputError, match="requested next action"):
        bridge.generate_current_ticket(
            workflow=_next_ticket_workflow(),
            requested_next_action_id="GENERATE_P18_9_2",
        )

    assert bridge.load_generation_record(ticket_id="P18.9.1") is None


def test_p18_9_2_request_fails_while_p18_9_1_is_canonical(bridge_home) -> None:
    with pytest.raises(bridge.TicketArchitectBridgeInputError, match="canonical next ticket P18.9.1"):
        bridge.generate_current_ticket(
            workflow=_next_ticket_workflow(),
            requested_ticket_id="P18.9.2",
        )

    assert bridge.load_generation_record(ticket_id="P18.9.1") is None
    assert bridge.load_generation_record(ticket_id="P18.9.2") is None


def test_bootstrap_no_history_resolves_first_roadmap_ticket(bridge_home) -> None:
    authority = bridge.resolve_canonical_next_ticket(_workflow())
    result = bridge.generate_current_ticket(
        workflow=_workflow(),
        requested_ticket_id="P18.9.0",
        requested_next_action_id="GENERATE_P18_9_0",
    )

    assert authority.ticket_id == "P18.9.0"
    assert authority.ticket_title == bridge.CANONICAL_TICKET_TITLE
    assert authority.next_action_id == "GENERATE_P18_9_0"
    assert authority.authority_source == "workflow_control_next_ticket"
    assert result["ticket_id"] == "P18.9.0"


def test_synthetic_successor_fixture_proves_generic_next_ticket_authority() -> None:
    workflow = {
        "project_id": "PEPPER",
        "project_name": "Pepper",
        "macroproject_id": "PTEST",
        "macroproject_title": "Synthetic Macroproject",
        "current_ticket_id": None,
        "next_ticket_id": "TEST.1",
        "workflow_status": "completed",
        "closed_predecessor_ticket_id": "TEST.1",
        "next_action": {
            "id": "GENERATE_TEST_1_REQUIRES_SEPARATE_HUMAN_ACTION",
            "target_ticket_id": "TEST.1",
        },
    }

    authority = bridge.resolve_canonical_next_ticket(
        workflow,
        roadmap_items=_synthetic_roadmap_items(),
    )

    assert authority.ticket_id == "TEST.2"
    assert authority.ticket_title == "Synthetic Successor"
    assert authority.next_action_id == "GENERATE_TEST_2_REQUIRES_SEPARATE_HUMAN_ACTION"
    bridge._validate_requested_identity(
        requested_project_id="PEPPER",
        requested_ticket_id="TEST.2",
        requested_next_action_id="GENERATE_TEST_2_REQUIRES_SEPARATE_HUMAN_ACTION",
        target=authority.generation_target(),
    )
    with pytest.raises(bridge.TicketArchitectBridgeInputError, match="canonical next ticket TEST.2"):
        bridge._validate_requested_identity(
            requested_project_id="PEPPER",
            requested_ticket_id="TEST.3",
            requested_next_action_id="GENERATE_TEST_3_REQUIRES_SEPARATE_HUMAN_ACTION",
            target=authority.generation_target(),
        )


@pytest.mark.parametrize(
    "workflow, message",
    [
        (_workflow(next_ticket_id=None, current_ticket_id="P18.9.0"), "no next governed ticket"),
        (_next_ticket_workflow(current_ticket_id="P18.9.1"), "requires no active ticket"),
        (_next_ticket_workflow(next_action={"id": "APPROVE_P18_9_1", "target_ticket_id": "P18.9.1"}), "generation action"),
        (_next_ticket_workflow(next_action={"id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION", "target_ticket_id": "P18.9.2"}), "target"),
    ],
)
def test_generic_generation_rejects_ineligible_workflow(bridge_home, workflow, message) -> None:
    with pytest.raises(bridge.TicketArchitectBridgeError, match=message):
        bridge.generate_current_ticket(workflow=workflow)

    assert bridge.load_generation_record(ticket_id="P18.9.1") is None


def test_generic_generation_is_idempotent_without_recompiling(bridge_home, monkeypatch) -> None:
    calls = []
    original = bridge.compile_ticket_spec_to_work_packet

    def counting_compile(request):
        calls.append(request)
        return original(request)

    monkeypatch.setattr(bridge, "compile_ticket_spec_to_work_packet", counting_compile)

    first = bridge.generate_current_ticket(workflow=_next_ticket_workflow())
    second = bridge.generate_current_ticket(workflow=_next_ticket_workflow())

    assert first["idempotent_replay"] is False
    assert second["idempotent_replay"] is True
    assert first["authority"] == second["authority"]
    assert len(calls) == 1


def test_product_runtime_projects_generic_generation_to_pending_approval(bridge_home, monkeypatch) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (None, None),
    )
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: _next_ticket_workflow())

    generated = pr.generate_current_governed_ticket(
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
    )
    overlay = bridge.generated_record_to_workflow_overlay(
        bridge.load_generation_record(ticket_id="P18.9.1")
    )
    inbox = pr.build_approval_inbox_source()

    assert generated["ticket_id"] == "P18.9.1"
    assert overlay["current_ticket_id"] == "P18.9.1"
    assert overlay["workflow_status"] == "awaiting_ticket_approval"
    assert overlay["approval_state"] == "pending_ticket_approval"
    assert overlay["next_action"]["id"] == "APPROVE_P18_9_1"
    assert overlay["WorkPacket_execution_authorized"] is False
    assert overlay["worker_execution"] is False
    assert overlay["Kanban_dispatch"] is False
    assert overlay["Git_mutation"] is False
    assert [item["id"] for item in inbox["approvals"]] == ["P18.9.1"]
    assert inbox["approvals"][0]["request_type"] == "ticket_approval"


def test_chat_tool_requires_explicit_generation_request_and_routes_generic_ticket(
    bridge_home,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: _next_ticket_workflow())

    ambiguous = _chat_tool_result(
        "generate_current_ticket",
        {"human_request_text": "P18.9.1 parece correcto.", "ticket_id": "P18.9.1"},
    )
    accepted = _chat_tool_result(
        "generate_current_ticket",
        {
            "human_request_text": "Genera el siguiente ticket gobernado P18.9.1.",
            "ticket_id": "P18.9.1",
            "next_action_id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
        },
    )

    assert "success" not in ambiguous
    assert "ambiguous" in ambiguous["error"]
    assert accepted["success"] is True
    assert accepted["ticket_id"] == "P18.9.1"
    assert accepted["human_request_text"] == "Genera el siguiente ticket gobernado P18.9.1."
    assert accepted["worker_execution"] is False
    assert accepted["Kanban_dispatch"] is False
    assert accepted["Git_mutation"] is False


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
