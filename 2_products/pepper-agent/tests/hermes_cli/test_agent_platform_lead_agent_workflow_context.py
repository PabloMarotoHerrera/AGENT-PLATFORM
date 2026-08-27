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
        "macroproject_id": "P18.9",
        "macroproject_title": "Pepper Product Personalization",
        "completed_macroproject_id": "P18",
        "completed_macroproject_state": "closed",
        "current_ticket_id": None,
        "current_ticket_title": None,
        "current_gap_id": None,
        "current_gap_title": None,
        "next_ticket_id": "P18.9.0",
        "next_ticket_title": "Product Inventory, IA Decision, and Acceptance Contract",
        "mode": "controlled_default",
        "readiness": "planning_approved_or_intake_ready",
        "workflow_state": "P18.9-PEPPER-PRODUCT-PERSONALIZATION-INTAKE-READY",
        "workflow_status": "planning_approved_or_intake_ready",
        "approval_state": "no_pending_approvals",
        "pending_approval_count": 0,
        "queue_state": "ready_to_generate_P18_9_0",
        "execution_state": "no_active_executions",
        "active_execution_count": 0,
        "validation_state": "not_started_no_ticket_generated",
        "review_state": "not_started_no_ticket_generated",
        "recovery_state": "not_required",
        "git_handoff_state": "human_git_authority_preserved",
        "warning_count": 0,
        "closed_gaps": [{"id": "P18-8-GAP-001"}],
        "historical_evidence": [{"id": "P18.R", "state": "closed", "decision": "accepted"}],
        "remaining_blockers": [],
        "default_mode_enabled": True,
        "manual_chat_control_required": False,
        "manual_opencode_ticket_copy_required": False,
        "manual_opencode_result_copy_required": False,
        "human_git_authority": "preserved_manual_git_add_commit_push_only",
        "ready_requires_human_smoke": False,
        "workflow_migration_complete": True,
        "P18_closed": True,
        "P18_R_closed": True,
        "P18_R_pending": False,
        "P18_9_ready": True,
        "P18_9_ticket_generated": False,
        "next_action": {
            "id": "GENERATE_P18_9_0",
            "label": (
                "Generate governed P18.9.0 Product Inventory, IA Decision, and "
                "Acceptance Contract before execution."
            ),
            "target_ticket_id": "P18.9.0",
            "target_ticket_title": "Product Inventory, IA Decision, and Acceptance Contract",
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
    assert context["macroproject_id"] == "P18.9"
    assert context["macroproject_title"] == "Pepper Product Personalization"
    assert context["available"] is False
    assert context["message"] == "no active governed ticket"
    assert context["current_ticket_id"] is None
    assert context["current_gap_id"] is None


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
    assert result["next_action"]["id"] == "GENERATE_P18_9_0"


def test_workflow_projection_closes_p18r_and_prepares_p18_9_without_ticket(monkeypatch) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_approval_operational_summary",
        lambda: {
            "approval_state": "no_pending_approvals",
            "pending_approval_count": 0,
            "source_system": pr.APPROVAL_SOURCE_SYSTEM,
        },
    )
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

    snapshot = pr.build_workflow_control_snapshot()
    serialized = json.dumps(snapshot, ensure_ascii=False)

    assert snapshot["completed_macroproject_id"] == "P18"
    assert snapshot["completed_macroproject_state"] == "closed"
    assert snapshot["P18_closed"] is True
    assert snapshot["P18_R_closed"] is True
    assert snapshot["P18_R_pending"] is False
    assert snapshot["workflow_migration_complete"] is True
    assert snapshot["macroproject_id"] == "P18.9"
    assert snapshot["macroproject_title"] == "Pepper Product Personalization"
    assert snapshot["readiness"] == "planning_approved_or_intake_ready"
    assert snapshot["current_ticket_id"] is None
    assert snapshot["current_gap_id"] is None
    assert snapshot["P18_9_ready"] is True
    assert snapshot["P18_9_ticket_generated"] is False
    assert snapshot["next_ticket_id"] == "P18.9.0"
    assert snapshot["next_action"]["id"] == "GENERATE_P18_9_0"
    assert {item["id"] for item in snapshot["historical_evidence"]} == {"P18.8", "P18.R"}
    assert "HUMAN_P18_8_CUTOVER_SMOKE_PASS" in serialized
    assert "P18_R_READY_FOR_HUMAN_AUTHORIZATION" not in serialized
    assert "ready_for_P18_R" not in serialized


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
    assert "artifact_inspection" not in result


def test_pepper_toolset_exposes_no_arbitrary_shell_or_file_authority(monkeypatch) -> None:
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_CHAT_MODE", "pepper-lead-agent")
    from hermes_cli.agent_platform.lead_agent import PEPPER_LEAD_AGENT_TOOLSETS
    from model_tools import get_tool_definitions

    definitions = get_tool_definitions(
        enabled_toolsets=PEPPER_LEAD_AGENT_TOOLSETS,
        quiet_mode=True,
    )
    names = {definition["function"]["name"] for definition in definitions}

    assert PEPPER_LEAD_AGENT_TOOLSETS == ["pepper_workflow", "pepper_repository"]
    assert {
        "get_current_project",
        "get_current_ticket",
        "get_workflow_control",
        "get_pending_approvals",
        "inspect_pending_approval",
        "inspect_pending_approval_artifact_section",
        "decide_pending_approval",
        "get_execution_status",
        "get_review_status",
        "get_next_action",
        "reconcile_invalid_current_generation_authority",
        "revise_generated_successor_ticket",
        "generate_current_ticket",
        "prepare_current_ticket_execution",
        "start_current_ticket_execution",
        "recover_current_ticket_execution",
        "get_governed_autonomy_status",
        "activate_current_ticket_governed_autonomy",
        "continue_current_ticket_governed_autonomy",
        "prepare_current_ticket_review",
        "accept_current_ticket_review",
        "submit_current_ticket_review_decision",
        "complete_current_ticket_human_git_handoff",
    }.issubset(names)
    assert {
        "get_repository_context",
        "list_repository_tree",
        "read_repository_file",
        "search_repository",
        "resolve_repository_authority",
    }.issubset(names)
    by_name = {definition["function"]["name"]: definition["function"] for definition in definitions}
    revision_params = by_name["revise_generated_successor_ticket"]["parameters"]
    activation_params = by_name["activate_current_ticket_governed_autonomy"]["parameters"]
    continuation_params = by_name["continue_current_ticket_governed_autonomy"]["parameters"]
    review_prepare_tool = by_name["prepare_current_ticket_review"]
    review_accept_tool = by_name["accept_current_ticket_review"]
    review_prepare_params = review_prepare_tool["parameters"]
    review_accept_params = review_accept_tool["parameters"]
    review_decision_params = by_name["submit_current_ticket_review_decision"]["parameters"]
    handoff_completion_params = by_name["complete_current_ticket_human_git_handoff"]["parameters"]
    assert revision_params["required"] == ["human_authorization_text"]
    assert "ticket_id" in revision_params["properties"]
    assert "next_action_id" in revision_params["properties"]
    assert "shell_command" not in revision_params["properties"]
    assert "workspace_path" not in revision_params["properties"]
    assert activation_params["required"] == ["human_request_text"]
    assert "governed_autonomy_envelope" not in activation_params["properties"]
    assert "capability_gap" not in activation_params["properties"]
    assert "continuation_lineage" not in activation_params["properties"]
    assert continuation_params["required"] == ["runtime_goal"]
    assert "governed_autonomy_envelope" not in continuation_params["properties"]
    assert "delegate_paths" not in continuation_params["properties"]
    assert "delegate_requested_operations" not in continuation_params["properties"]
    assert "fresh_execution_request_text" in continuation_params["properties"]
    assert "resume_pending_fresh_execution_request_SHA256" in continuation_params[
        "properties"
    ]
    assert "current Pepper ticket" in review_prepare_tool["description"]
    assert "PREPARE_<current-ticket>_REVIEW" in json.dumps(review_prepare_params)
    assert "P18.9.0" not in review_prepare_tool["description"]
    assert "P18.9.0" not in json.dumps(review_prepare_params)
    assert "current Pepper ticket" in review_accept_tool["description"]
    assert "AWAIT_HUMAN_<current-ticket>_REVIEW_ACCEPTANCE" in json.dumps(
        review_accept_params
    )
    assert "P18.9.0" not in review_accept_tool["description"]
    assert "P18.9.0" not in json.dumps(review_accept_params)
    assert review_decision_params["required"] == ["decision", "feedback"]
    assert review_decision_params["properties"]["decision"]["enum"] == [
        "accept",
        "changes_requested",
        "reject",
    ]
    assert handoff_completion_params["required"] == [
        "reviewed_run_id",
        "reviewed_candidate_SHA256",
        "review_decision_SHA256",
        "commits",
        "branch",
        "push_attestation",
        "approved_committed_paths",
        "validation_evidence",
    ]
    handoff_properties = handoff_completion_params["properties"]
    assert "commits" in handoff_properties
    assert "approved_committed_paths" in handoff_properties
    assert "excluded_paths" in handoff_properties
    assert "human_attested_evidence" in handoff_properties
    assert "git_command" not in handoff_properties
    assert "shell_command" not in handoff_properties
    assert "workspace_path" not in handoff_properties
    assert not (names & {"terminal", "process", "read_file", "write_file", "patch", "search_files"})


def test_continue_governed_autonomy_tool_forwards_pending_fresh_request_sha(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools as pepper_tools

    captured: dict[str, object] = {}

    class RuntimeStub:
        def continue_current_ticket_governed_autonomy(self, **kwargs):
            captured.update(kwargs)
            return {"dispatch_performed": False, "execution_started": False}

        def build_lead_agent_operational_context(self):
            return {}

    monkeypatch.setattr(pepper_tools, "_runtime", lambda: RuntimeStub())
    pending_sha = "a" * 64

    result = json.loads(pepper_tools._continue_current_ticket_governed_autonomy({
        "runtime_goal": "Resume pending governed autonomy request by identity.",
        "strategy": "DIRECT",
        "resume_pending_fresh_execution_request_SHA256": pending_sha,
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
    }))

    assert result["success"] is True
    assert captured["resume_pending_fresh_execution_request_SHA256"] == pending_sha


def test_complete_human_git_handoff_tool_forwards_evidence_only_lists(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools as pepper_tools

    captured: dict[str, object] = {}

    class RuntimeStub:
        def complete_current_ticket_human_git_handoff(self, **kwargs):
            captured.update(kwargs)
            return {
                "handoff_completion_recorded": True,
                "dispatch_performed": False,
                "execution_started": False,
                "Git_mutation": False,
            }

        def build_lead_agent_operational_context(self):
            return {"workflow_status": "completed", "git_handoff_state": "completed"}

    monkeypatch.setattr(pepper_tools, "_runtime", lambda: RuntimeStub())

    result = json.loads(pepper_tools._complete_current_ticket_human_git_handoff({
        "reviewed_run_id": 11,
        "reviewed_candidate_SHA256": "a" * 64,
        "review_decision_SHA256": "b" * 64,
        "commits": ["dc77d92", "467f3b412ddd51a237fc76ff5f297e0347308755"],
        "branch": "p18-manual-to-hermes-workflow-migration",
        "push_attestation": "Human pushed origin branch.",
        "approved_committed_paths": [
            "web/src/agent-platform/shell/navigation.ts",
            "web/src/agent-platform/shell/shell.test.tsx",
        ],
        "excluded_paths": ["package-lock.json"],
        "validation_evidence": ["Human validation passed."],
        "human_attested_evidence": ["Second commit path set attested."],
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
        "next_action_id": "PREPARE_P18_9_1_HUMAN_GIT_HANDOFF",
    }))

    assert result["success"] is True
    assert captured["commits"] == ["dc77d92", "467f3b412ddd51a237fc76ff5f297e0347308755"]
    assert captured["approved_committed_paths"] == [
        "web/src/agent-platform/shell/navigation.ts",
        "web/src/agent-platform/shell/shell.test.tsx",
    ]
    assert captured["excluded_paths"] == ["package-lock.json"]
    assert captured["validation_evidence"] == ["Human validation passed."]
    assert captured["human_attested_evidence"] == ["Second commit path set attested."]
    assert "spawn_fn" not in captured
    assert "shell_command" not in captured


def test_lead_agent_prompt_requires_tool_backed_state() -> None:
    from hermes_cli.agent_platform.lead_agent import pepper_lead_agent_system_prompt

    prompt = pepper_lead_agent_system_prompt()

    assert "call the relevant Pepper workflow tool" in prompt
    assert "generate_current_ticket" in prompt
    assert "current canonical next governed ticket" in prompt
    assert "P18.9.0 TicketSpec/WorkPacket bridge" not in prompt
    assert "revise_generated_successor_ticket" in prompt
    assert "REVISE_<current-ticket>" in prompt
    assert "rejected generated successor" in prompt
    assert "preserve rejected history" in prompt
    assert "decide_pending_approval" in prompt
    assert "APPROVE_<current-ticket>" in prompt
    assert "current pending governed ticket approval" in prompt
    assert "<current-ticket-token>_APPROVED_NO_EXECUTION" in prompt
    assert "current approved governed WorkPacket" in prompt
    assert "start_current_ticket_execution" in prompt
    assert "recover_current_ticket_execution" in prompt
    assert "RECOVER_<current-ticket>_EXECUTION" in prompt
    assert "failed execution for that same current ticket" in prompt
    assert "Autorizo explícitamente la recuperación de la ejecución fallida de P18.9.0." not in prompt
    assert "get_governed_autonomy_status" in prompt
    assert "activate_current_ticket_governed_autonomy" in prompt
    assert "continue_current_ticket_governed_autonomy" in prompt
    assert "01AH governed autonomy" in prompt
    assert "status-only" in prompt
    assert "server-derived authority" in prompt
    assert "Do not ask for or supply GovernedAutonomyEnvelope JSON" in prompt
    assert "without a GovernedAutonomyEnvelope, delegate paths, or delegate operations" in prompt
    assert "DIRECT may start exactly one same-authority Kanban run" in prompt
    assert "fresh_execution_request_text" in prompt
    assert "runtime substrate changed" in prompt
    assert "resume_pending_fresh_execution_request_SHA256" in prompt
    assert "do not paraphrase the original request" in prompt
    assert "replaying the same fresh request must not create another run" in prompt
    assert "submit_current_ticket_review_decision" in prompt
    assert "accept, changes_requested, and reject" in prompt
    assert "Do not route human review accept, changes_requested, or reject decisions" in prompt
    assert "complete_current_ticket_human_git_handoff" in prompt
    assert "PREPARE_<current-ticket>_HUMAN_GIT_HANDOFF" in prompt
    assert "never execute Git yourself" in prompt
    assert "evidence-only human Git handoff completion" in prompt
    assert "backend-derived child scope/operations" in prompt
    assert "prepare_current_ticket_review" in prompt
    assert "accept_current_ticket_review" in prompt
    assert "PREPARE_<current-ticket>_REVIEW" in prompt
    assert "AWAIT_HUMAN_<current-ticket>_REVIEW_ACCEPTANCE" in prompt
    assert "exact backend-required acceptance phrase" in prompt
    assert "PREPARE_P18_9_0_REVIEW" not in prompt
    assert "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE" not in prompt
    assert "Acepto explícitamente la review de P18.9.0" not in prompt
    assert "KANBAN_COMPLETION_RESULT_DETAIL_GAP" in prompt
    assert "START_<current-ticket>_RETRY_REQUIRES_HUMAN_AUTHORIZATION" in prompt
    assert "explicitly authorizes retrying that same current ticket" in prompt
    assert "Autorizo explícitamente el retry de P18.9.0." not in prompt
    assert "questions, hypotheticals, readiness checks, ambiguous language, or non-current ticket IDs" in prompt
    assert "get_repository_context" in prompt
    assert "resolve_repository_authority" in prompt
    assert "Do not infer the active governed project from cwd" in prompt
    assert "Do not tell the user to inspect or copy dashboard state" in prompt


def test_context_has_no_gbrain_dependency(monkeypatch) -> None:
    pr = _install_sources(monkeypatch)
    before = {name for name in sys.modules if name.lower().startswith("gbrain")}

    context = pr.build_lead_agent_operational_context()

    after = {name for name in sys.modules if name.lower().startswith("gbrain")}
    assert context["GBrain_calls"] == 0
    assert after == before
