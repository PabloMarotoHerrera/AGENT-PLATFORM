"""A successor selected late in a read must retain its own durable closure."""

import json
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as wk
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)
from tools import pepper_workflow_tools as tools


@pytest.fixture
def closed(projection_home, tmp_path, monkeypatch):
    fixture = fixtures._c14_review_authority_fixture(
        pr, tmp_path, monkeypatch, ticket_id="P99.7"
    )
    completion = fixtures._c14_persist_completion_record(pr, fixture)
    return SimpleNamespace(**fixture.__dict__, completion=completion)


def _late_successor(fixture, monkeypatch, history):
    ticket = fixture.ticket_id
    predecessor = fixtures._c14_predecessor_ticket_id(ticket)
    base = fixtures._c9_completed_overlay(pr, predecessor)
    monkeypatch.setattr(pr, "_p18_9_0_generation_overlay", lambda: (base, None))
    monkeypatch.setattr(
        pr,
        "_completed_predecessor_successor_lifecycle_overlay",
        lambda *a, **kw: (None, None),
    )
    monkeypatch.setattr(
        pr,
        "_load_current_projection_record",
        lambda: fixtures._c9_projection_record(predecessor),
    )
    monkeypatch.setattr(
        wk,
        "load_kanban_projection_record",
        lambda *, ticket_id, **kw: fixture.projection if ticket_id == ticket else None,
    )
    monkeypatch.setattr(
        pr,
        "resolve_canonical_next_ticket",
        lambda workflow=None: fixtures._c14_successor_authority(pr, predecessor),
    )
    overlay = {
        **fixtures._c9_projection_overlay(pr, ticket),
        **history,
        "current_ticket_id": ticket,
        "current_ticket_title": fixture.projection["ticket_title"],
        "next_ticket_id": None,
    }
    # The observed defect: only the last successor-precedence pass selects this ticket.
    monkeypatch.setattr(
        pr,
        "_pending_generated_successor_ticket_approval_overlay",
        lambda workflow, allow_current_ticket_projection=False: (overlay, None)
        if allow_current_ticket_projection
        else (None, None),
    )


@pytest.mark.parametrize(
    "history",
    ["execution", "retry", "review_prepared", "accepted_review", "handoff_prepared"],
)
def test_c57_late_selected_closed_ticket_dominates_history(
    closed, monkeypatch, history
):
    ticket = closed.ticket_id
    state = fixtures._c13_review_ready_workflow(pr, closed.projection)
    if history == "retry":
        state.update(
            workflow_state=f"{ticket}-RETRY-EXECUTION-COMPLETED",
            retry_state="retry_completed",
        )
    elif history in {"review_prepared", "accepted_review", "handoff_prepared"}:
        state.update(workflow_status=history, review_state=history)
    _late_successor(closed, monkeypatch, state)
    path = pr.human_git_handoff_completion_record_path_for_ticket(ticket)
    before = path.read_bytes()
    for _ in range(2):
        workflow = pr.build_workflow_control_snapshot()
        assert workflow["workflow_status"] == "completed"
        assert workflow["governed_workflow_state"] == "completed"
        assert workflow["ticket_closed"] is True
        assert workflow["handoff_completion_present"] is True
        assert workflow["current_ticket_id"] is None
        assert workflow["closed_predecessor_ticket_id"] == ticket
        assert workflow["next_action"] == closed.completion["next_action"]
        assert workflow["next_ticket_generated"] is False
        assert workflow["Git_mutation"] is False
        for reader in (
            tools._get_current_ticket,
            tools._get_workflow_control,
            tools._get_next_action,
            tools._get_review_status,
        ):
            result = json.loads(reader({}))
            assert result["next_action"]["id"] == closed.completion["next_action"]["id"]
            assert result.get("current_ticket_id") != ticket
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "mutation", ["digest", "ticket", "projection", "run", "candidate", "review"]
)
def test_c57_late_invalid_completion_cannot_close(closed, monkeypatch, mutation):
    record = dict(closed.completion)
    fields = {
        "ticket": "ticket_id",
        "projection": "projection_SHA256",
        "run": "reviewed_run_id",
        "candidate": "reviewed_candidate_SHA256",
        "review": "review_decision_SHA256",
    }
    if mutation == "digest":
        record["completion_record_SHA256"] = "f" * 64
    else:
        field = fields[mutation]
        record[field] = (
            999
            if mutation == "run"
            else ("P99.99" if mutation == "ticket" else "f" * 64)
        )
        fixtures._c14_reseal_completion_record(pr, record)
    path = pr.human_git_handoff_completion_record_path_for_ticket(closed.ticket_id)
    fixtures._write_json_authority_record(path, record)
    _late_successor(
        closed, monkeypatch, fixtures._c13_review_ready_workflow(pr, closed.projection)
    )
    before = path.read_bytes()
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["ticket_closed"] is False
    assert (
        workflow["workflow_status"]
        == "blocked_invalid_human_git_handoff_completion_authority"
    )
    assert path.read_bytes() == before


def test_c57_prepare_complete_then_rebuild_all_read_surfaces(
    projection_home, tmp_path, monkeypatch
):
    fixture = fixtures._c14_review_authority_fixture(
        pr, tmp_path, monkeypatch, ticket_id="P99.7"
    )
    ticket = fixture.ticket_id
    workflow = fixtures._c14_handoff_completion_workflow(pr, fixture.projection)
    workflow["next_action"]["id"] = pr._human_git_handoff_prepare_action_id(
        pr.resolve_current_ticket_lifecycle_binding(
            projection_record=fixture.projection
        )
    )
    context = pr._current_review_candidate_authority_context(
        projection=fixture.projection, review_prepare=fixture.review
    )
    snapshot = fixtures._p18_9_2_handoff_git_snapshot(
        status_entries=[],
        path_SHA256={p: e["source_SHA256"] for p, e in context["files"].items()},
    )
    with monkeypatch.context() as patch:
        patch.setattr(pr, "build_workflow_control_snapshot", lambda: workflow)
        patch.setattr(
            pr, "_human_git_handoff_completion_active_execution_blocker", lambda p: None
        )
        patch.setattr(
            pr,
            "_human_git_handoff_completion_successor_authority",
            lambda binding: fixtures._c14_successor_authority(pr, ticket),
        )
        prepared = pr.prepare_current_ticket_human_git_handoff(
            project_id="PEPPER",
            ticket_id=ticket,
            next_action_id=workflow["next_action"]["id"],
            git_snapshot_fn=lambda: snapshot,
        )
        assert prepared["handoff_preparation_recorded"] is True, prepared
        workflow["next_action"]["id"] = pr._human_git_handoff_completion_action_id(
            ticket
        )
        patch.setattr(
            pr,
            "_current_work_packet_scope_for_governed_autonomy",
            lambda projection: ((fixture.candidate_path,), (), "b" * 64),
        )
        final_sha = "a" * 40
        finished_snapshot = {
            **snapshot,
            "head_parent": snapshot["head"],
            "head": final_sha,
            "remote_head": final_sha,
        }
        result = pr.complete_current_ticket_human_git_handoff(
            reviewed_run_id=fixture.accepted_record["reviewed_run_id"],
            reviewed_candidate_SHA256=fixture.accepted_record[
                "reviewed_candidate_SHA256"
            ],
            review_decision_SHA256=fixture.accepted_record["review_decision_SHA256"],
            commits=(final_sha,),
            branch=snapshot["branch"],
            push_attestation="Human pushed the synthetic candidate.",
            approved_committed_paths=prepared["candidate_paths"],
            excluded_paths=prepared["tolerated_untracked_exclusions"],
            validation_evidence=("Synthetic candidate validation passed.",),
            project_id="PEPPER",
            ticket_id=ticket,
            next_action_id=workflow["next_action"]["id"],
            git_snapshot_fn=lambda: finished_snapshot,
        )
    assert result["handoff_completion_recorded"] is True, result
    assert result["ticket_closed"] is True
    assert result["governed_workflow_state"] == "completed"
    assert result["Git_commands_executed"] == 0
    assert result["Git_mutation"] is False
    _late_successor(
        fixture,
        monkeypatch,
        fixtures._c13_review_ready_workflow(pr, fixture.projection),
    )
    before = sorted(
        str(p.relative_to(projection_home))
        for p in (projection_home / "agent-platform").rglob("*")
    )
    for reader in (
        tools._get_current_ticket,
        tools._get_workflow_control,
        tools._get_next_action,
        tools._get_review_status,
    ):
        read = json.loads(reader({}))
        assert read["next_action"]["id"] == result["next_action"]["id"]
    assert (
        sorted(
            str(p.relative_to(projection_home))
            for p in (projection_home / "agent-platform").rglob("*")
        )
        == before
    )
    assert pr.build_workflow_control_snapshot()["next_ticket_generated"] is False
