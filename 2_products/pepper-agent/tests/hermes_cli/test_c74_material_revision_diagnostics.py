"""Rich post-accept revisions retain strict lint and expose bounded preflight issues."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import post_accept_material_revision as revision
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tests.hermes_cli.test_c73_post_accept_material_revision import (
    accepted as accepted,
    flow as flow,
    projection_home as projection_home,
)


def rich(ticket_id):
    text = (
        Path(__file__).parent / "fixtures/c74-rich-visual-revision.json"
    ).read_text()
    return json.loads(text.replace("P99.4", ticket_id))


def corrected(ticket_id):
    contract = rich(ticket_id)
    contract["scope"]["allowed_paths"] = ["2_products/pepper-agent/web/src/**"]
    contract["scope"]["forbidden_paths"] += [
        ".git/**",
        ".agents/**",
        "AGENTS.md",
        "graphify-out/**",
        "9_artifacts/**",
        "2_products/pepper-agent/hermes_cli/**",
        "2_products/pepper-agent/tools/**",
        "2_products/pepper-agent/tests/**",
        "2_products/pepper-agent/.env*",
    ]
    contract["scope"]["forbidden_actions"].append(
        "Do not mutate git worktree state; Git remains exclusively human."
    )
    contract["constraints"].append(
        "Provide rollback/restoration evidence for the bounded visual changes: identify prior canonical files and reversible visual deltas for human rollback, without executing Git or materializing historical R0004 scratch."
    )
    contract["response_contract"]["required_sections"] += [
        "Decisions made",
        "Tests/commands run",
    ]
    contract["validation_steps"][0]["command_authority"]["package_relative_path"] = (
        "2_products/pepper-agent/web"
    )
    return contract


def generate(f, contract):
    return pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text=f"I explicitly authorize revision of {f.ticket_id}.",
        revision_contract=contract,
        ticket_id=f.ticket_id,
        next_action_id=bridge.revise_action_id(f.ticket_id),
    )


def files(home):
    return {
        str(p.relative_to(home)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in home.rglob("*")
        if p.is_file()
    }


@pytest.fixture
def requested(accepted):
    revision.request(**accepted.args)
    assert (
        pr.build_workflow_control_snapshot()["workflow_status"]
        == "awaiting_material_revision"
    )
    return accepted


def failure(f, contract):
    before = files(f.flow.home)
    with pytest.raises(bridge.TicketArchitectBridgeError) as error:
        generate(f, contract)
    envelope = error.value.failure_envelope
    assert envelope is not None
    assert files(f.flow.home) == before
    for flag in (
        "publication_occurred",
        "generation_record_changed",
        "approval_occurred",
        "projection_occurred",
        "task_created",
        "execution_started",
        "Git_mutation",
        "auto_retry",
    ):
        assert envelope[flag] is False
    assert pr.build_workflow_control_snapshot()["next_action"][
        "id"
    ] == bridge.revise_action_id(f.ticket_id)
    return envelope


@pytest.mark.parametrize("accepted", [4], indirect=True)
def test_real_rich_contract_fails_actionably_then_generates_exactly_revision_five(
    requested,
):
    f = requested
    before = bridge.load_generation_record(ticket_id=f.ticket_id)
    assert before["ticket_publication_result"]["publication"]["revision"] == 4
    first = failure(f, rich(f.ticket_id))
    second = failure(f, rich(f.ticket_id))
    assert first["issues"] == second["issues"]
    assert first["revision_attempt"] == second["revision_attempt"] == 5
    assert first["source_stage"] == "ticketspec_lint"
    assert first["lint_passed"] is False and first["lint_evaluated"] is True
    assert first["lint_issue_count"] == 4
    assert len(first["generated_pre_lint_ticket_spec_SHA256"]) == 64
    assert {i["issue_code"] for i in first["issues"]} == {
        "required_forbidden_action_missing",
        "rollback_constraint_required",
        "required_response_section_missing",
    }
    assert all(i["expected_constraint"] for i in first["issues"])
    original_review = pr.review_decision_record_path_for_ticket(
        f.ticket_id
    ).read_bytes()
    original_handoff = pr.human_git_handoff_prepare_record_path_for_ticket(
        f.ticket_id
    ).read_bytes()
    contract = corrected(f.ticket_id)
    result = generate(f, contract)
    record = bridge.load_generation_record(ticket_id=f.ticket_id)
    spec = record["ticket_spec"]
    packet = record["work_packet_compilation_result"]["work_packet"]
    assert result["revision_status"] == "awaiting_ticket_approval"
    assert result["active_execution_count"] == 0
    assert record["ticket_publication_result"]["publication"]["revision"] == 5
    assert record["revision_authority"]["revision_reason"] == revision.REASON
    assert record["ticket_id"] == f.ticket_id
    assert record["ticket_spec_SHA256"] != before["ticket_spec_SHA256"]
    assert record["work_packet_SHA256"] != before["work_packet_SHA256"]
    assert record["work_packet_id"] != before["work_packet_id"]
    assert spec["dependencies"] == []
    assert spec["objective"] == contract["objective"]
    assert set(contract["tasks"]).issubset(spec["tasks"])
    assert set(contract["acceptance_criteria"]).issubset(spec["acceptance_criteria"])
    assert spec["scope"]["allowed_paths"] == ["2_products/pepper-agent/web/src/**"]
    assert packet["repository_scope"]["allowed_paths"] == spec["scope"]["allowed_paths"]
    for original in contract["validation_steps"]:
        generated = next(
            v
            for v in spec["validation_steps"]
            if v["validation_id"] == original["validation_id"]
        )
        assert generated["description"] == original["description"]
        assert generated["expected_result"] == original["expected_result"]
        assert generated["command"] == original["command"]
    assert spec["validation_steps"][0]["command_authority"]["command_argv"] == [
        "npm",
        "test",
    ]
    assert (
        spec["validation_steps"][0]["command_authority"]["package_relative_path"]
        == "2_products/pepper-agent/web"
    )
    assert record["lint_report"]["disposition"] == "pass"
    assert packet["validation_steps"][0]["command_execution_authorized"] is True
    assert packet["validation_steps"][0]["command_authority"]["command_argv"] == [
        "npm",
        "test",
    ]
    assert all(
        v["command"] is None and v["command_execution_authorized"] is False
        for v in packet["validation_steps"][1:]
    )
    assert (
        packet["repository_scope"]["forbidden_paths"]
        == spec["scope"]["forbidden_paths"]
    )
    assert (
        bridge.load_approval_decision_record(
            ticket_id=f.ticket_id, generation_record=record
        )
        is None
    )
    assert (
        pr.review_decision_record_path_for_ticket(f.ticket_id).read_bytes()
        == original_review
    )
    assert (
        pr.human_git_handoff_prepare_record_path_for_ticket(f.ticket_id).read_bytes()
        == original_handoff
    )
    history = record["revision_authority"]["material_revision_request_record"]
    assert (
        history["historical_authority"]["review_decision"]["review_decision"]
        == "accept"
    )
    assert history["handoff_state"] == "superseded_by_material_revision"
    assert (
        pr.build_workflow_control_snapshot()["workflow_status"]
        == "awaiting_ticket_approval"
    )


@pytest.mark.parametrize(
    "mode,field",
    [
        ("self", "dependencies.0.ticket_id"),
        ("unsupported", "unsupported_rich_field"),
        ("absolute", "scope.allowed_paths.0"),
        ("traversal", "scope.allowed_paths.0"),
        ("empty_acceptance", "acceptance_criteria"),
        ("validation", "validation_steps.0"),
        ("bad_command", "validation_steps.0.command_authority"),
        ("long", "objective"),
        ("count", "acceptance_criteria"),
    ],
)
def test_contract_errors_name_exact_field_without_mutation(requested, mode, field):
    c = corrected(requested.ticket_id)
    if mode == "self":
        c["dependencies"] = [
            {
                "ticket_id": requested.ticket_id,
                "kind": "hard_prerequisite",
                "scope": "internal_project",
                "rationale": "Invalid self dependency",
            }
        ]
    elif mode == "unsupported":
        c["unsupported_rich_field"] = "must never be silently ignored"
    elif mode in {"absolute", "traversal"}:
        c["scope"]["allowed_paths"] = [
            "/home/private" if mode == "absolute" else "../outside"
        ]
    elif mode == "empty_acceptance":
        c["acceptance_criteria"] = []
    elif mode == "validation":
        c["validation_steps"][0]["command"] = None
    elif mode == "bad_command":
        c["validation_steps"][0]["command_authority"]["command_argv"] = [
            "npm",
            "test",
            "--",
            "different",
        ]
    elif mode == "long":
        c["objective"] = "x" * 8193
    else:
        c["acceptance_criteria"] = [f"Criterion {i}" for i in range(33)]
    envelope = failure(requested, c)
    assert envelope["source_stage"] == "revision_contract_validation"
    assert any(i["field_path"].startswith(field) for i in envelope["issues"])


def test_conflicting_scope_still_fails_unchanged_lint(requested):
    c = corrected(requested.ticket_id)
    c["scope"]["forbidden_paths"].append(c["scope"]["allowed_paths"][0])
    result = failure(requested, c)
    assert any(i["issue_code"] == "scope_exact_contradiction" for i in result["issues"])


def test_tool_preserves_structured_diagnostics_and_does_not_retry(requested):
    from tools import pepper_workflow_tools as tools

    before = files(requested.flow.home)
    result = json.loads(
        tools._revise_current_ticket_for_material_contract_failure({
            "human_authorization_text": f"I explicitly authorize revision of {requested.ticket_id}.",
            "ticket_id": requested.ticket_id,
            "next_action_id": bridge.revise_action_id(requested.ticket_id),
            "revision_contract": rich(requested.ticket_id),
        })
    )
    assert result["success"] is False
    assert result["lint_issue_count"] == 4
    assert result["auto_retry"] is False
    assert files(requested.flow.home) == before


def test_invalid_post_accept_provenance_remains_blocked(requested):
    path = revision.path_for(requested.generation)
    record = json.loads(path.read_text())
    record["review_decision_SHA256"] = "f" * 64
    path.write_text(json.dumps(record))
    before = files(requested.flow.home)
    with pytest.raises(ValueError):
        generate(requested, corrected(requested.ticket_id))
    assert files(requested.flow.home) == before


def test_schema_diagnostics_are_bounded_and_do_not_expose_rejected_values(requested):
    contract = corrected(requested.ticket_id)
    secret = "sk-proj-" + "a" * 70
    for i in range(45):
        contract[f"unexpected_{i}"] = secret
    result = failure(requested, contract)
    assert result["issue_count"] == 45
    assert len(result["issues"]) == 32
    assert result["issues_omitted_count"] == 13
    assert secret not in json.dumps(result)


def test_many_lint_issues_report_total_and_explicit_omission(requested):
    c = corrected(requested.ticket_id)
    paths = [f"2_products/pepper-agent/web/src/visual-{i}.ts" for i in range(25)]
    c["scope"]["allowed_paths"] = paths
    c["scope"]["forbidden_paths"] += paths
    result = failure(requested, c)
    assert result["lint_issue_count"] == 25
    assert len(result["issues"]) == 20
    assert result["issues_omitted_count"] == 5
    assert result["issues_truncated"] is True


def test_ticket_model_limits_are_not_truncated_or_bypassed(requested):
    c = corrected(requested.ticket_id)
    c["response_contract"]["required_sections"].append("x" * 513)
    result = failure(requested, c)
    assert result["source_stage"] == "ticketspec_build"
    assert any(
        i["field_path"].startswith("required_sections") and "512" in i["message"]
        for i in result["issues"]
    )


def test_unresolved_dependency_remains_blocked(requested):
    c = corrected(requested.ticket_id)
    c["dependencies"] = [
        {
            "ticket_id": "P99.999",
            "kind": "hard_prerequisite",
            "scope": "internal_project",
            "rationale": "Unresolved dependency",
        }
    ]
    result = failure(requested, c)
    assert result["lint_passed"] is False


def test_compile_failure_stays_before_persistence(requested, monkeypatch):
    def fail_compile(*args, **kwargs):
        raise ValueError("isolated compiler rejection")

    monkeypatch.setattr(bridge, "compile_ticket_spec_to_work_packet", fail_compile)
    result = failure(requested, corrected(requested.ticket_id))
    assert result["source_stage"] == "workpacket_compile"
    assert result["lint_passed"] is True and result["lint_evaluated"] is True


@pytest.mark.parametrize(
    "path",
    [
        "2_products/pepper-agent/hermes_cli/agent_platform/product_runtime.py",
        "2_products/pepper-agent/tests/hermes_cli/test_c64_validation_authority_boundary.py",
        ".git/config",
        "9_artifacts/result.json",
        "../.pepper-hermes/state.db",
    ],
)
def test_corrected_visual_scope_denies_unrelated_writes(tmp_path, path):
    from tools import governed_workpacket_file_guard as guard

    c = corrected("P99.22")
    authority = guard.WorkPacketFileAuthority(
        ticket_id="P99.22",
        work_packet_id="isolated",
        work_packet_SHA256="a" * 64,
        ticket_spec_SHA256="b" * 64,
        projection_SHA256="c" * 64,
        allowed_paths=tuple(c["scope"]["allowed_paths"]),
        forbidden_paths=tuple(c["scope"]["forbidden_paths"]),
        workspace_root=tmp_path,
        resolved_workspace_root=tmp_path,
    )
    assert guard.evaluate_write_target(authority, path) is not None
    for allowed in [
        "2_products/pepper-agent/web/src/index.css",
        "2_products/pepper-agent/web/src/components/Sidebar.tsx",
        "2_products/pepper-agent/web/src/agent-platform/shell/brand-lockup.tsx",
    ]:
        assert guard.evaluate_write_target(authority, allowed) is None
