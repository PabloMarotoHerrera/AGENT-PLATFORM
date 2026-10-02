"""C65: human material-revision gate preserves recovered failed execution."""

import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest
from hermes_cli import kanban_db
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import retry_material_revision as revision
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import test_agent_platform_work_packet_compiler as compiler
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)
from tests.hermes_cli.test_c62_execution_profile_authority import profiles


@pytest.fixture
def flow(projection_home, monkeypatch, request):
    contract = generation._synthetic_implementation_contract("Revision")
    contract["validation_steps"] = [
        compiler.validation_step(command="npm test -- --runInBand").model_dump(
            mode="json"
        ),
        compiler.validation_step("V2", command=None).model_dump(mode="json"),
    ]
    if getattr(request, "param", None) == "executable":
        authority = compiler.command_authority(
            source_command="npm test -- --runInBand",
            command_argv=("npm", "test", "--", "--runInBand"),
        )
        contract["validation_steps"][0] = compiler.validation_step(
            command=authority.source_command, command_authority=authority
        ).model_dump(mode="json")
    target = generation._synthetic_implementation_target(
        "P99.4", "Synthetic Revision Surface", contract=contract
    )
    target = replace(
        target,
        macroproject_id="P999",
        macroproject_title="Synthetic Revision Macroproject",
    )
    workflow = {
        "project_id": target.project_id,
        "project_name": target.project_name,
        "macroproject_id": target.macroproject_id,
        "macroproject_title": target.macroproject_title,
        "current_ticket_id": None,
        "next_ticket_id": target.ticket_id,
        "next_ticket_title": target.ticket_title,
        "workflow_status": "completed",
        "P18_9_ready": True,
        "next_action": {
            "id": target.next_action_id,
            "target_ticket_id": target.ticket_id,
            "target_ticket_title": target.ticket_title,
        },
    }
    bridge.generate_current_ticket(workflow=workflow, target=target)
    record = bridge.load_generation_record(ticket_id=target.ticket_id)
    bridge.apply_ticket_approval_decision(
        ticket_id=target.ticket_id, decision="approve", actor="synthetic-human"
    )
    profiles(projection_home, monkeypatch)
    projected = projection.project_current_approved_workpacket_to_kanban(
        workflow=bridge.generated_record_to_workflow_overlay(record)
    )
    run_id = fixtures._force_projected_execution_failure(
        projected=projected, pr=pr, kanban_db=kanban_db, monkeypatch=monkeypatch
    )
    failed = pr.build_workflow_control_snapshot()
    assert failed["workflow_status"] == "execution_failed"
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        workspace = Path(task.workspace_path)
        workspace.mkdir(parents=True, exist_ok=True)
        candidate = workspace / "candidate.txt"
        candidate.write_text("preserved implementation candidate")
    finally:
        conn.close()
    recovered = pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text(
            target.ticket_id
        ),
        ticket_id=target.ticket_id,
    )
    args = {
        "human_authorization_text": revision.action_id(target.ticket_id),
        "ticket_id": target.ticket_id,
        "failed_run_id": run_id,
        "work_packet_SHA256": record["work_packet_SHA256"],
        "recovery_action_SHA256": recovered["recovery_action_SHA256"],
        "reason_code": revision.REASON,
    }
    return SimpleNamespace(
        home=projection_home,
        record=record,
        projection=projected,
        run_id=run_id,
        candidate=candidate,
        args=args,
    )


def immutable(flow):
    paths = [
        bridge.generation_record_path_for_ticket(flow.record["ticket_id"]),
        bridge.approval_decision_record_path_for_ticket(flow.record["ticket_id"]),
        pr.recovery_action_record_path_for_ticket(flow.record["ticket_id"]),
        flow.candidate,
    ]
    conn = kanban_db.connect(board=flow.projection["kanban_board_slug"])
    try:
        runs = [
            pr._run_dict(run)
            for run in kanban_db.list_runs(conn, flow.projection["kanban_task_id"])
        ]
    finally:
        conn.close()
    return [p.read_bytes() for p in paths], runs


def test_alternative_request_preserves_failed_run_candidate_and_budget(flow):
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "retry_pending"
    assert (
        workflow["alternative_actions"][0]["id"]
        == flow.args["human_authorization_text"]
    )
    before = immutable(flow)
    result = revision.request(**flow.args)
    assert result["retry_authority_status"] == "suspended_not_consumed"
    for field in (
        "retry_started",
        "new_run_started",
        "retry_budget_consumed",
        "execution_started",
        "Git_mutation",
    ):
        assert result[field] is False
    assert immutable(flow) == before
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "awaiting_material_revision"
    assert workflow["material_revision_required"] is True
    assert workflow["review_state"] == "material_revision_required"
    assert workflow["governed_workflow_state"] == "awaiting_material_revision"
    assert workflow["next_action"]["id"] == "REVISE_P99_4"
    assert (
        workflow["next_action"]["required_human_action"] == "ticket_material_revision"
    )
    assert revision.request(**flow.args)["idempotent_replay"] is True
    assert immutable(flow) == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("ticket_id", "P99.5"),
        ("failed_run_id", 999),
        ("work_packet_SHA256", "0" * 64),
        ("recovery_action_SHA256", "0" * 64),
        ("reason_code", "please change it"),
        ("human_authorization_text", "Retry P99.4"),
        ("human_authorization_text", "Inspect material revision P99.4"),
    ],
)
def test_invalid_request_has_no_side_effects(flow, field, value):
    before = immutable(flow)
    with pytest.raises((ValueError, pr.ProductRuntimeError)):
        revision.request(**{**flow.args, field: value})
    assert not revision.path_for(flow.record).exists()
    assert immutable(flow) == before


def test_suspended_retry_cannot_dispatch(flow):
    revision.request(**flow.args)
    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo el retry de P99.4.",
        ticket_id="P99.4",
        next_action_id="START_P99_4_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert result["blocker_code"] == "RETRY_SUSPENDED_FOR_MATERIAL_REVISION"
    assert result["execution_started"] is False


def test_canonical_revision_requires_fresh_approval_and_rejects_old_retry(flow):
    request = revision.request(**flow.args)
    recovery_bytes = pr.recovery_action_record_path_for_ticket("P99.4").read_bytes()
    authority = compiler.command_authority(
        source_command="npm test -- --runInBand",
        command_argv=("npm", "test", "--", "--runInBand"),
    )
    steps = [
        compiler.validation_step(
            command=authority.source_command, command_authority=authority
        ).model_dump(mode="json"),
        compiler.validation_step("V2", command=None).model_dump(mode="json"),
    ]
    result = pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "validation_steps": steps},
        ticket_id="P99.4",
        next_action_id="REVISE_P99_4",
    )
    assert result["revision_status"] == "awaiting_ticket_approval"
    revised = bridge.load_generation_record(ticket_id="P99.4")
    assert revised["work_packet_SHA256"] != flow.record["work_packet_SHA256"]
    assert revised["ticket_publication_result"]["publication"]["revision"] == 2
    assert (
        bridge.load_approval_decision_record(
            ticket_id="P99.4", generation_record=revised
        )
        is None
    )
    assert (
        revised["revision_authority"]["material_revision_request_SHA256"]
        == request["material_revision_request_SHA256"]
    )
    assert (
        pr.recovery_action_record_path_for_ticket("P99.4").read_bytes()
        == recovery_bytes
    )
    assert flow.candidate.read_text() == "preserved implementation candidate"
    try:
        blocked = pr.start_current_ticket_execution(
            human_authorization_text="Retry P99.4",
            ticket_id="P99.4",
            next_action_id="START_P99_4_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
            spawn_fn=lambda *a, **kw: pytest.fail("stale projection must not dispatch"),
        )
    except pr.ProductRuntimeError:
        pass
    else:
        assert blocked.get("execution_started") is False
    assert (
        pr.build_workflow_control_snapshot()["workflow_status"]
        == "awaiting_ticket_approval"
    )
    # A later human approval still cannot reuse the failed publication's task.
    bridge.apply_ticket_approval_decision(
        ticket_id="P99.4", decision="approve", actor="synthetic-human"
    )
    with pytest.raises(pr.ProductRuntimeError):
        pr._load_current_projection_record()
    fresh = projection.project_current_approved_workpacket_to_kanban(
        workflow=pr.build_workflow_control_snapshot()
    )
    assert fresh["work_packet_SHA256"] == revised["work_packet_SHA256"]
    fresh_record = projection.load_kanban_projection_record(ticket_id="P99.4")
    assert fresh_record["projection_SHA256"] != request["projection_SHA256"]
    assert fresh["kanban_task_id"] != flow.projection["kanban_task_id"]
    try:
        blocked = pr.start_current_ticket_execution(
            human_authorization_text="Autorizo el retry de P99.4.",
            ticket_id="P99.4",
            next_action_id="START_P99_4_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
            spawn_fn=lambda *a, **kw: pytest.fail(
                "old retry must not dispatch revised authority"
            ),
        )
    except pr.ProductRuntimeError:
        pass
    else:
        assert blocked.get("execution_started") is False
    assert flow.candidate.read_text() == "preserved implementation candidate"


@pytest.mark.parametrize("flow", ["executable"], indirect=True)
def test_executable_contract_cannot_request_material_revision(flow):
    before = immutable(flow)
    assert not pr.build_workflow_control_snapshot().get("alternative_actions")
    with pytest.raises(
        pr.ProductRuntimeConflict, match="material contract failure evidence"
    ):
        revision.request(**flow.args)
    assert not revision.path_for(flow.record).exists()
    assert immutable(flow) == before


def test_material_revision_consent_cannot_authorize_retry(flow):
    before = immutable(flow)
    result = pr.start_current_ticket_execution(
        human_authorization_text=flow.args["human_authorization_text"],
        ticket_id="P99.4",
        next_action_id="START_P99_4_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert result["execution_started"] is False
    assert not revision.path_for(flow.record).exists()
    assert immutable(flow) == before


def test_public_tool_exposes_choice_and_requests_gate(flow):
    from tools import pepper_workflow_tools as tool
    from toolsets import TOOLSETS

    assert (
        "request_current_ticket_material_revision"
        in TOOLSETS["pepper_workflow"]["tools"]
    )
    next_action = json.loads(tool._get_next_action({}))
    assert (
        next_action["alternative_actions"][0]["id"]
        == flow.args["human_authorization_text"]
    )
    control = json.loads(tool._get_workflow_control({}))
    assert control["alternative_actions"] == next_action["alternative_actions"]
    result = json.loads(tool._request_current_ticket_material_revision(flow.args))
    assert result["workflow_status"] == "awaiting_material_revision"
    assert result["next_action"]["id"] == "REVISE_P99_4"


def test_corrupt_request_never_restores_retry_authority(flow):
    revision.request(**flow.args)
    revision.path_for(flow.record).write_text("{}")
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["workflow_status"] == "material_revision_authority_blocked"
    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo el retry de P99.4.",
        ticket_id="P99.4",
        next_action_id="START_P99_4_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert result["blocker_code"] == "RETRY_SUSPENDED_FOR_MATERIAL_REVISION"


def test_old_workflow_snapshot_cannot_bypass_durable_gate(flow):
    old = pr.build_workflow_control_snapshot()
    revision.request(**flow.args)
    result = pr._start_current_ticket_retry_execution(
        request=pr.CurrentTicketExecutionStartRequest(
            human_authorization_text="Autorizo el retry de P99.4.",
            ticket_id="P99.4",
            next_action_id="START_P99_4_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        ),
        projection=flow.projection,
        workflow=old,
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert result["blocker_code"] == "RETRY_SUSPENDED_FOR_MATERIAL_REVISION"


def test_material_gate_does_not_replay_old_initial_start_authority(flow):
    revision.request(**flow.args)
    before = immutable(flow)
    result = pr.start_current_ticket_execution(
        human_authorization_text="I explicitly authorize execution of P99.4.",
        ticket_id="P99.4",
        next_action_id=pr.governed_ticket_lifecycle_action_ids("P99.4")[
            "execution_start"
        ],
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert result["execution_started"] is False
    assert result["blocker_code"] == "EXECUTION_SUSPENDED_FOR_MATERIAL_REVISION"
    assert immutable(flow) == before
