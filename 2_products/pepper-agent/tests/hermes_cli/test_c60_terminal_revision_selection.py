"""C60: real revision lifecycle with isolated Kanban, evidence and candidate files."""

import json
from pathlib import Path

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import terminal_review_selection as selection
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)

projection_home = fixtures.projection_home


def attest_manual_items():
    inspection = pr.inspect_current_ticket_manual_validation()
    for item in inspection.get("items", []):
        if item["status"] != "passed":
            pr.attest_current_ticket_manual_validation(
                ticket_id=inspection["ticket_id"],
                work_packet_id=inspection["work_packet_id"],
                work_packet_sha256=inspection["work_packet_SHA256"],
                run_id=inspection["run_id"],
                validation_id=item["validation_id"],
                validation_contract_sha256=inspection["validation_contract_SHA256"],
                binding_sha256=item["binding_SHA256"],
                next_action_id=inspection["next_action_id"],
                status="passed",
                human_attestation_text=item["required_attestation_text"]["passed"],
                evidence="Synthetic human confirms the bounded predecessor review criteria.",
            )


def align_source(workspace):
    manifest = json.loads(
        (workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).read_text()
    )
    for relative in manifest.get("materialized_roots", []):
        source = Path(manifest["source_root"]) / relative
        candidate = workspace / relative
        if candidate.is_file() and not source.exists():
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes(candidate.read_bytes())


def revised(projection_home, monkeypatch, *, active=False):
    original_prepare = pr.prepare_current_ticket_review

    def prepare_with_human_evidence(**kwargs):
        attest_manual_items()
        return original_prepare(**kwargs)

    finish = fixtures._finish_projected_run_as_review_required_terminal

    def finish_with_structured_evidence(*args, **kwargs):
        kwargs["metadata"] = {
            "implementation_complete": True,
            "validation_passed": True,
            "terminal_outcome": "validated_review_required",
            "Git_mutation": False,
        }
        kb, projection, _run_id = args
        with kb.connect(board=projection["kanban_board_slug"]) as conn:
            workspace = Path(
                kb.get_task(conn, projection["kanban_task_id"]).workspace_path
            )
        align_source(workspace)
        return finish(*args, **kwargs)

    with monkeypatch.context() as setup:
        setup.setattr(
            fixtures,
            "_mark_projected_task_done_preserving_review_run_fixture",
            lambda *a, **k: None,
        )
        setup.setattr(
            fixtures,
            "_finish_projected_run_as_review_required_terminal",
            finish_with_structured_evidence,
        )
        setup.setattr(pr, "prepare_current_ticket_review", prepare_with_human_evidence)
        f = fixtures._terminal_done_review_revision_pending_fixture(
            projection_home,
            monkeypatch,
            ticket_id="P18.9.2",
            first_pid=8300,
        )
    fixtures._patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(f.kanban_db, "_pid_alive", lambda pid: int(pid) == 8301)
    started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Apply the bounded human review feedback.",
        strategy="DIRECT",
        resume_pending_fresh_execution_request_SHA256=f.revision_request[
            "fresh_execution_request_SHA256"
        ],
        spawn_fn=lambda *a, **k: 8301,
        project_id="PEPPER",
        ticket_id=f.ticket_id,
    )
    assert started["kanban_run_id"] == f.prior_run_id + 1
    f.run_id = started["kanban_run_id"]
    f.workspace = Path(started["workspace_path"])
    fixtures._write_p18_9_2_terminal_candidate_fixture(pr, projection_home, f.workspace)
    path = (
        f.workspace
        / "2_products/pepper-agent/web/src/agent-platform/runtime-overview/contract.ts"
    )
    path.write_text(path.read_text() + "// bounded human correction\n")
    align_source(f.workspace)
    if not active:
        fixtures._finish_projected_run_as_review_required_terminal(
            f.kanban_db,
            f.projected,
            f.run_id,
            summary="review-required: bounded revision passes governed validation; human code review required.",
            metadata={
                "implementation_complete": True,
                "validation_passed": True,
                "terminal_outcome": "validated_review_required",
                "Git_mutation": False,
            },
        )
    f.package_path = pr.review_prepare_record_path_for_ticket(f.ticket_id)
    f.decision_path = pr.review_decision_record_path_for_ticket(f.ticket_id)
    f.package_bytes = f.package_path.read_bytes()
    f.decision_bytes = f.decision_path.read_bytes()
    return f


def choose(f, request=None, **kwargs):
    return pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Use terminal revision for governed review; do not start a fresh execution.",
        strategy="DIRECT",
        terminal_review_selection=request
        or selection._context(f.authority)["selection"],
        project_id="PEPPER",
        ticket_id=f.ticket_id,
        spawn_fn=lambda *a, **k: pytest.fail("selection must not dispatch"),
        **kwargs,
    )


def test_terminal_revision_selection_full_lifecycle(projection_home, monkeypatch):
    f = revised(projection_home, monkeypatch)
    before = pr.build_workflow_control_snapshot()
    assert before["next_action"]["id"] == "CONTINUE_P18_9_2_GOVERNED_AUTONOMY"
    request = selection._context(f.authority)["selection"]
    result = choose(f, request)
    assert result["continuation_status"] == "terminal_revision_promoted_for_review"
    assert result["idempotent_replay"] is False
    assert result["reviewed_run_id"] == f.run_id
    assert result["next_action"]["id"] == "ATTEST_P18_9_2_MANUAL_VALIDATION", result
    for key in (
        "dispatch_performed",
        "execution_started",
        "worker_process_started",
        "Git_mutation",
        "kanban_run_created",
        "review_decision_recorded",
    ):
        assert result[key] is False
    assert f.package_path.read_bytes() == f.package_bytes
    assert f.decision_path.read_bytes() == f.decision_bytes
    inspected = pr.inspect_current_ticket_review_candidate(
        reviewed_run_id=f.run_id, operation="aggregate_diff"
    )
    assert inspected["inspection_status"] == "aggregate_diff_available", inspected
    assert inspected["reviewed_candidate_SHA256"] == request["candidate_SHA256"]
    assert inspected["review_prepared"] is False
    stale = pr.inspect_current_ticket_review_candidate(reviewed_run_id=f.prior_run_id)
    assert stale["blocker_code"] == "REVIEW_RUN_GUARD_MISMATCH"
    assert choose(f, request)["idempotent_replay"] is True
    attest_manual_items()
    assert (
        pr.build_workflow_control_snapshot()["next_action"]["id"]
        == "PREPARE_P18_9_2_REVIEW"
    )
    prepared = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id=f.ticket_id,
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance", (
        prepared
    )
    assert prepared["successful_run_id"] == f.run_id
    assert prepared["review_package_SHA256"] != f.review["review_package_SHA256"]
    promoted = selection.load(f.authority)
    assert promoted["predecessor_package"] == json.loads(f.package_bytes)
    assert promoted["predecessor_decision"] == json.loads(f.decision_bytes)
    assert (
        f.review["review_package_SHA256"]
        in pr.review_prepare_history_path_for_ticket(f.ticket_id).read_text()
    )
    assert (
        json.loads(f.decision_bytes)["review_decision_SHA256"]
        in pr.review_decision_history_path_for_ticket(f.ticket_id).read_text()
    )
    prepared_bytes = f.package_path.read_bytes()
    assert (
        pr.inspect_current_ticket_review_candidate(reviewed_run_id=f.run_id)[
            "inspection_status"
        ]
        == "available"
    )
    assert choose(f, request)["idempotent_replay"] is True
    assert f.package_path.read_bytes() == prepared_bytes
    conn = f.kanban_db.connect(board=f.projected["kanban_board_slug"])
    try:
        assert (
            f.kanban_db.list_runs(conn, f.projected["kanban_task_id"])[-1].id
            == f.run_id
        )
    finally:
        conn.close()


@pytest.mark.parametrize(
    "key,value",
    [
        ("work_packet_SHA256", "a" * 64),
        ("review_revision_request_SHA256", "b" * 64),
        ("predecessor_reviewed_run_id", 999),
        ("terminal_run_id", 999),
        ("candidate_SHA256", "c" * 64),
        ("choice", "fresh_execution_request"),
        ("terminal_run_id", True),
    ],
)
def test_selection_guard_mismatch(projection_home, monkeypatch, key, value):
    f = revised(projection_home, monkeypatch)
    request = selection._context(f.authority)["selection"]
    request[key] = value
    with pytest.raises(pr.ProductRuntimeConflict):
        choose(f, request)
    assert not selection._path(f.authority, f.run_id).exists()
    assert f.package_path.read_bytes() == f.package_bytes
    assert f.decision_path.read_bytes() == f.decision_bytes


def test_selection_active_run_rejected(projection_home, monkeypatch):
    f = revised(projection_home, monkeypatch, active=True)
    with pytest.raises(pr.ProductRuntimeConflict):
        choose(f, {"choice": "terminal_governed_run_review"})
    assert not selection._path(f.authority, f.run_id).exists()


def test_selection_and_fresh_execution_are_exclusive(projection_home, monkeypatch):
    f = revised(projection_home, monkeypatch)
    with pytest.raises(pr.ProductRuntimeConflict, match="cannot request fresh"):
        choose(f, fresh_execution_request_text="Start a fresh execution")
    assert not selection._path(f.authority, f.run_id).exists()


def test_selection_drift_and_tamper_fail_closed(projection_home, monkeypatch):
    f = revised(projection_home, monkeypatch)
    choose(f)
    path = selection._path(f.authority, f.run_id)
    record = json.loads(path.read_text())
    record["selection"]["candidate_SHA256"] = "a" * 64
    path.write_text(json.dumps(record))
    with pytest.raises(pr.ProductRuntimeConflict, match="digest mismatch"):
        selection.load(f.authority)


def test_selection_option_is_reachable_without_promotion(projection_home, monkeypatch):
    f = revised(projection_home, monkeypatch)
    workflow = pr.build_workflow_control_snapshot()
    option = workflow["next_action"]["terminal_review_selection"]
    assert option["terminal_run_id"] == f.run_id
    assert option["predecessor_reviewed_run_id"] == f.prior_run_id
    assert not selection._path(f.authority, f.run_id).exists()


@pytest.mark.parametrize("damage", ["candidate", "completion", "decision", "runtime"])
def test_selected_authority_drift_is_rejected(projection_home, monkeypatch, damage):
    f = revised(projection_home, monkeypatch)
    request = selection._context(f.authority)["selection"]
    choose(f, request)
    if damage == "candidate":
        path = (
            f.workspace
            / "2_products/pepper-agent/web/src/agent-platform/runtime-overview/contract.ts"
        )
        path.write_text(path.read_text() + "// unselected drift\n")
    elif damage == "completion":
        with f.kanban_db.connect(board=f.projected["kanban_board_slug"]) as conn:
            conn.execute(
                "UPDATE task_runs SET summary=? WHERE id=?",
                ("Changed terminal evidence", f.run_id),
            )
            conn.commit()
    elif damage == "decision":
        path = selection._path(f.authority, f.run_id)
        record = json.loads(path.read_text())
        record["predecessor_decision"]["review_decision"] = "accept"
        record["selection_SHA256"] = pr._digest_payload(
            selection.POLICY,
            {k: v for k, v in record.items() if k != "selection_SHA256"},
        )
        path.write_text(json.dumps(record))
    else:
        path = pr.governed_autonomy_runtime_state_path_for_ticket(f.ticket_id)
        record = json.loads(path.read_text())
        record["prior_terminal_run_id"] = 999
        record["runtime_state_SHA256"] = pr._governed_autonomy_runtime_record_digest(
            record
        )
        path.write_text(json.dumps(record))
    with pytest.raises(pr.ProductRuntimeConflict):
        choose(f, request)


def test_explicit_fresh_execution_remains_a_distinct_branch(
    projection_home, monkeypatch
):
    f = revised(projection_home, monkeypatch)
    assert not selection._path(f.authority, f.run_id).exists()
    monkeypatch.setattr(f.kanban_db, "_pid_alive", lambda pid: int(pid) == 8302)
    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Human explicitly requests a fresh same-authority execution.",
        strategy="DIRECT",
        fresh_execution_request_text="Start a fresh same-authority execution instead of selecting terminal revision for review.",
        project_id="PEPPER",
        ticket_id=f.ticket_id,
        spawn_fn=lambda *a, **k: 8302,
    )
    assert result["fresh_execution_requested"] is True, result
    assert result["kanban_run_id"] == f.run_id + 1, result
    assert result["execution_started"] is True
    assert result["Git_mutation"] is False

    assert not selection._path(f.authority, f.run_id).exists()


def test_public_continuation_tool_selects_exact_candidate(projection_home, monkeypatch):
    from tools import pepper_workflow_tools

    f = revised(projection_home, monkeypatch)
    option = pr.build_workflow_control_snapshot()["next_action"][
        "terminal_review_selection"
    ]
    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda *a, **k: pytest.fail("selection must not probe providers"),
    )
    result = json.loads(
        pepper_workflow_tools._continue_current_ticket_governed_autonomy({
            "runtime_goal": "Human selects the terminal revision for review.",
            "strategy": "DIRECT",
            "project_id": "PEPPER",
            "ticket_id": f.ticket_id,
            "terminal_review_selection": option,
        })
    )
    assert result["success"] is True, result
    assert result["reviewed_run_id"] == f.run_id
    assert result["execution_started"] is False
    assert result["Git_mutation"] is False


@pytest.mark.parametrize("request_kind", ["text", "resume", "override"])
def test_terminal_review_selection_consumes_same_terminal_fresh_execution_choice(
    projection_home, monkeypatch, request_kind,
):
    f = revised(projection_home, monkeypatch)
    chosen = choose(f)
    monkeypatch.setattr(
        pr, "_executor_provider_readiness",
        lambda *a, **k: pytest.fail("consumed choice must not probe providers"),
    )
    selection_path = selection._path(f.authority, f.run_id)
    paths = [selection_path, f.package_path, f.decision_path,
             pr.governed_autonomy_runtime_state_path_for_ticket(f.ticket_id)]
    before = {path: path.read_bytes() for path in paths}
    with f.kanban_db.connect(board=f.projected["kanban_board_slug"]) as conn:
        runs_before = [run.id for run in f.kanban_db.list_runs(conn, f.projected["kanban_task_id"])]
    request = {
        "text": {"fresh_execution_request_text": "Start a fresh same-authority execution."},
        "resume": {"resume_pending_fresh_execution_request_SHA256": f.revision_request["fresh_execution_request_SHA256"]},
        "override": {"fresh_execution_request_override": f.revision_request},
    }[request_kind]
    with pytest.raises(pr.ProductRuntimeConflict, match="TERMINAL_REVIEW_SELECTION_CHOICE_CONSUMED"):
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Attempt to reuse the consumed terminal branch.", strategy="DIRECT",
            project_id="PEPPER", ticket_id=f.ticket_id,
            spawn_fn=lambda *a, **k: pytest.fail("consumed choice must not spawn"), **request,
        )
    assert {path: path.read_bytes() for path in paths} == before
    with f.kanban_db.connect(board=f.projected["kanban_board_slug"]) as conn:
        assert [run.id for run in f.kanban_db.list_runs(conn, f.projected["kanban_task_id"])] == runs_before
    assert pr.inspect_current_ticket_review_candidate(reviewed_run_id=f.run_id)["inspection_status"] == "available"
    replay = choose(f)
    assert replay["idempotent_replay"] is True
    assert replay["selection_SHA256"] == chosen["selection_SHA256"]
    assert replay["Git_mutation"] is False


@pytest.mark.parametrize("request_kind", ["resume", "override"])
def test_new_review_revision_creates_later_execution_authority(projection_home, monkeypatch, request_kind):
    f = revised(projection_home, monkeypatch)
    choose(f)
    selection_path = selection._path(f.authority, f.run_id)
    selected_bytes = selection_path.read_bytes()
    attest_manual_items()
    prepared = pr.prepare_current_ticket_review(
        project_id="PEPPER", ticket_id=f.ticket_id, next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert prepared["successful_run_id"] == f.run_id
    changed = pr.submit_current_ticket_review_decision(
        decision="changes_requested", feedback="Human requests another bounded correction of this reviewed candidate.",
        reviewed_run_id=f.run_id, project_id="PEPPER", ticket_id=f.ticket_id,
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *a, **k: pytest.fail("review decision only records pending authority"),
    )
    request = changed["review_revision_request_reference"]
    assert request["fresh_execution_request_SHA256"] != f.revision_request["fresh_execution_request_SHA256"]
    assert request["prior_terminal_run_id"] == f.run_id
    # Even after a new decision, the old boundary and arbitrary fresh text stay consumed.
    for stale in [
        {"resume_pending_fresh_execution_request_SHA256": f.revision_request["fresh_execution_request_SHA256"]},
        {"fresh_execution_request_override": f.revision_request},
        {"fresh_execution_request_text": "Start another arbitrary fresh execution."},
    ]:
        with pytest.raises(pr.ProductRuntimeConflict, match="TERMINAL_REVIEW_SELECTION_CHOICE_CONSUMED"):
            pr.continue_current_ticket_governed_autonomy(
                runtime_goal="Attempt stale authority after a new review decision.", strategy="DIRECT",
                project_id="PEPPER", ticket_id=f.ticket_id,
                spawn_fn=lambda *a, **k: pytest.fail("stale authority must not spawn"), **stale,
            )
    valid_request = (
        {"resume_pending_fresh_execution_request_SHA256": request["fresh_execution_request_SHA256"]}
        if request_kind == "resume" else {"fresh_execution_request_override": request}
    )
    # Pending runtime alone cannot substitute for the persisted human decision.
    decision_bytes = f.decision_path.read_bytes()
    f.decision_path.unlink()
    try:
        with pytest.raises(pr.ProductRuntimeConflict, match="TERMINAL_REVIEW_SELECTION_CHOICE_CONSUMED"):
            pr.continue_current_ticket_governed_autonomy(
                runtime_goal="Attempt pending authority without its decision.", strategy="DIRECT",
                project_id="PEPPER", ticket_id=f.ticket_id,
                spawn_fn=lambda *a, **k: pytest.fail("missing decision must not spawn"), **valid_request,
            )
    finally:
        f.decision_path.write_bytes(decision_bytes)
    monkeypatch.setattr(f.kanban_db, "_pid_alive", lambda pid: int(pid) == 8302)
    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue the newly recorded human revision.", strategy="DIRECT",
        project_id="PEPPER", ticket_id=f.ticket_id, spawn_fn=lambda *a, **k: 8302, **valid_request,
    )
    assert result["execution_started"] is True, result
    assert result["kanban_run_id"] == f.run_id + 1
    assert result["Git_mutation"] is False
    assert selection_path.read_bytes() == selected_bytes
