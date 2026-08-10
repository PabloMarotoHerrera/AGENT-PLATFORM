from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


def _workflow(**overrides):
    data = {
        "schema_version": 1,
        "source_system": "pepper-controlled-default-mode-cutover",
        "product_id": "pepper",
        "project_id": "PEPPER",
        "project_name": "Pepper",
        "macroproject_id": "P18",
        "macroproject_title": "Manual-to-Hermes Workflow Migration",
        "current_ticket_id": "P18.8",
        "current_ticket_title": "Controlled Default-Mode Cutover",
        "current_gap_id": "P18.8-GAP-005",
        "current_gap_title": "Lead Agent Live Governed Workflow Context Bridge",
        "mode": "controlled_default",
        "readiness": "blocked_pending_human_ui_smoke",
        "workflow_state": "P18.8-PEPPER-CHAT-WORKFLOW-CONTEXT-READY-FOR-HUMAN-SMOKE",
        "workflow_status": "blocked_pending_human_ui_smoke",
        "approval_state": "no_pending_approvals",
        "pending_approval_count": 0,
        "queue_state": "human_smoke_required",
        "execution_state": "no_active_executions",
        "active_execution_count": 0,
        "validation_state": "pending_human_cutover_smoke",
        "review_state": "pending_human_cutover_smoke",
        "recovery_state": "not_required",
        "git_handoff_state": "human_git_authority_preserved",
        "warning_count": 0,
        "closed_gaps": [{"id": "P18-8-GAP-001"}],
        "remaining_blockers": [{"id": "HUMAN_P18_8_CUTOVER_SMOKE_PASS"}],
        "default_mode_enabled": True,
        "manual_chat_control_required": False,
        "manual_opencode_ticket_copy_required": False,
        "manual_opencode_result_copy_required": False,
        "human_git_authority": "preserved_manual_git_add_commit_push_only",
        "ready_requires_human_smoke": True,
        "next_action": {
            "id": "HUMAN_P18_8_CUTOVER_SMOKE_PASS",
            "label": "Run real Pepper dashboard cutover smoke and record the pass token",
        },
        "evidence_timestamp": "2026-08-10T00:00:00Z",
        "evidence_version": 1,
        "observed_at": "2026-08-10T00:00:00Z",
    }
    data.update(overrides)
    return data


def _install_sources(monkeypatch, approvals=None, executions=None, workflow=None):
    from hermes_cli.agent_platform import product_runtime as pr

    approvals = [] if approvals is None else approvals
    executions = [] if executions is None else executions
    workflow = _workflow() if workflow is None else workflow
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: workflow)
    monkeypatch.setattr(
        pr,
        "build_approval_inbox_source",
        lambda: {
            "source_system": pr.APPROVAL_SOURCE_SYSTEM,
            "source_authority": "durable-hermes-staged-write-store",
            "approvals": list(approvals),
        },
    )
    monkeypatch.setattr(
        pr,
        "build_execution_collection_source",
        lambda: {
            "source_system": pr.CONTROLLED_EXECUTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "executions": list(executions),
        },
    )
    return pr


def _tool_result(name: str, args: dict | None = None) -> dict:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    return json.loads(handle_function_call(name, args or {}))


def test_lead_agent_context_uses_governed_project_not_cwd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_named_dir = tmp_path / "pepper-agent"
    repo_named_dir.mkdir()
    monkeypatch.chdir(repo_named_dir)
    pr = _install_sources(monkeypatch)

    context = pr.build_lead_agent_operational_context()

    assert context["project_id"] == "PEPPER"
    assert context["project_name"] == "Pepper"
    assert context["project_id"] != Path.cwd().name
    assert context["current_ticket_id"] == "P18.8"
    assert context["current_gap_id"] == "P18.8-GAP-005"


def test_lead_agent_context_contract_and_ui_workflow_consistency(monkeypatch) -> None:
    workflow = _workflow(pending_approval_count=2, active_execution_count=1)
    approvals = [{"id": "approval-1"}, {"id": "approval-2"}]
    executions = [{"id": 7, "status": "running", "ended_at": None}]
    pr = _install_sources(
        monkeypatch,
        approvals=approvals,
        executions=executions,
        workflow=workflow,
    )

    context = pr.build_lead_agent_operational_context()

    for key in (
        "product_id",
        "project_id",
        "project_name",
        "macroproject_id",
        "current_ticket_id",
        "current_ticket_title",
        "workflow_state",
        "workflow_status",
        "approval_state",
        "pending_approval_count",
        "queue_state",
        "execution_state",
        "active_execution_count",
        "validation_state",
        "review_state",
        "recovery_state",
        "git_handoff_state",
        "blocker_count",
        "warning_count",
        "next_action",
        "evidence_timestamp",
        "evidence_version",
    ):
        assert key in context

    assert context["workflow_control"]["project_id"] == context["project_id"]
    assert context["workflow_control"]["current_ticket_id"] == context["current_ticket_id"]
    assert context["workflow_control"]["workflow_state"] == context["workflow_state"]
    assert context["next_action"] == workflow["next_action"]
    assert context["pending_approval_count"] == 2
    assert context["active_execution_count"] == 1


def test_tools_refresh_approval_execution_and_workflow_state(monkeypatch) -> None:
    approvals = []
    executions = []
    workflow = _workflow(workflow_status="blocked_pending_human_ui_smoke")
    _install_sources(monkeypatch, approvals=approvals, executions=executions, workflow=workflow)

    assert _tool_result("get_pending_approvals")["pending_approval_count"] == 0
    approvals.append({"id": "approval-live", "status": "pending"})
    assert _tool_result("get_pending_approvals")["pending_approval_count"] == 1

    assert _tool_result("get_execution_status")["active_execution_count"] == 0
    executions.append({"id": 1, "status": "running", "ended_at": None})
    assert _tool_result("get_execution_status")["active_execution_count"] == 1

    assert _tool_result("get_workflow_control")["workflow_status"] == "blocked_pending_human_ui_smoke"
    workflow["workflow_status"] = "changed_live"
    assert _tool_result("get_workflow_control")["workflow_status"] == "changed_live"


def test_current_ticket_unavailable_reports_no_active_governed_ticket(monkeypatch) -> None:
    workflow = _workflow(current_ticket_id=None, current_ticket_title=None)
    _install_sources(monkeypatch, workflow=workflow)

    result = _tool_result("get_current_ticket")

    assert result["available"] is False
    assert result["message"] == "no active governed ticket"
    assert result["current_ticket_id"] is None
    assert result["next_action"]["id"] == "HUMAN_P18_8_CUTOVER_SMOKE_PASS"


def test_zero_approval_and_execution_states_are_grounded(monkeypatch) -> None:
    _install_sources(monkeypatch)

    approvals = _tool_result("get_pending_approvals")
    executions = _tool_result("get_execution_status")

    assert approvals["approval_state"] == "no_pending_approvals"
    assert approvals["pending_approval_count"] == 0
    assert approvals["message"] == "no pending approvals"
    assert executions["execution_state"] == "no_active_executions"
    assert executions["active_execution_count"] == 0
    assert executions["message"] == "no active executions"


def test_inspect_pending_approval_is_read_only_action(monkeypatch) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    _install_sources(monkeypatch, approvals=[{"id": "approval-1"}])
    monkeypatch.setattr(
        pr,
        "build_approval_detail_source",
        lambda approval_id: {
            "source_system": pr.APPROVAL_SOURCE_SYSTEM,
            "approval": {"id": approval_id, "status": "pending"},
            "evidence": [{"id": f"{approval_id}:summary"}],
            "decisions": [],
        },
    )

    result = _tool_result("inspect_pending_approval")

    assert result["approval"]["id"] == "approval-1"
    assert result["auto_approval"] is False
    assert result["decisions"] == []


def test_pepper_toolset_exposes_no_arbitrary_shell_or_file_authority(monkeypatch) -> None:
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_CHAT_MODE", "pepper-lead-agent")
    from hermes_cli.agent_platform.lead_agent import PEPPER_LEAD_AGENT_TOOLSETS
    from model_tools import get_tool_definitions

    definitions = get_tool_definitions(
        enabled_toolsets=PEPPER_LEAD_AGENT_TOOLSETS,
        quiet_mode=True,
    )
    names = {definition["function"]["name"] for definition in definitions}

    assert PEPPER_LEAD_AGENT_TOOLSETS == ["pepper_workflow"]
    assert names == {
        "get_current_project",
        "get_current_ticket",
        "get_workflow_control",
        "get_pending_approvals",
        "inspect_pending_approval",
        "get_execution_status",
        "get_review_status",
        "get_next_action",
    }
    assert not (names & {"terminal", "process", "read_file", "write_file", "patch", "search_files"})


def test_lead_agent_prompt_requires_tool_backed_state() -> None:
    from hermes_cli.agent_platform.lead_agent import pepper_lead_agent_system_prompt

    prompt = pepper_lead_agent_system_prompt()

    assert "call the relevant Pepper workflow tool" in prompt
    assert "Do not infer the active governed project from cwd" in prompt
    assert "Do not tell the user to inspect or copy dashboard state" in prompt


def test_context_has_no_gbrain_dependency(monkeypatch) -> None:
    pr = _install_sources(monkeypatch)
    before = {name for name in sys.modules if name.lower().startswith("gbrain")}

    context = pr.build_lead_agent_operational_context()

    after = {name for name in sys.modules if name.lower().startswith("gbrain")}
    assert context["GBrain_calls"] == 0
    assert after == before
