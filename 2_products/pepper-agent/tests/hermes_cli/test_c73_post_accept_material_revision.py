"""Post-accept supersession is a separate, immutable human decision."""

from contextlib import closing
from copy import deepcopy
import json
from pathlib import Path

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import post_accept_material_revision as rev
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c67_successive_recovery_cycles import advance, recover


@pytest.fixture
def accepted(flow, monkeypatch, tmp_path, request):
    real_projection = pr._load_current_projection_record
    real_binding_projection = pr._current_projection_record_for_binding
    if getattr(request, "param", 1) == 4:
        for _ in range(3):
            flow = advance(flow, monkeypatch)
            flow.args["recovery_action_SHA256"] = recover()["recovery_action_SHA256"]
    p = pr._load_current_projection_record()
    for name in (
        "_c13_review_ready_workflow",
        "_c13_prepared_review_workflow",
        "_c14_handoff_completion_workflow",
    ):
        original = getattr(fixtures, name)

        def workflow(runtime, projection, *args, _fn=original, **kwargs):
            return _fn(
                runtime,
                {**projection, "macroproject_title": "Synthetic Revision Macroproject"},
                *args,
                **kwargs,
            )

        monkeypatch.setattr(fixtures, name, workflow)
    monkeypatch.setattr(fixtures, "_c13_projection_record", lambda *args: p)
    original_source = fixtures._c13_review_round_completion

    def source(runtime, projection, path, **kwargs):
        kwargs["run_id"] = flow.run_id
        result = original_source(runtime, projection, path, **kwargs)
        c = result.completion
        with closing(kb.connect(board=p["kanban_board_slug"])) as conn:
            conn.execute(
                "UPDATE tasks SET status='blocked',current_run_id=NULL,worker_pid=NULL,claim_lock=NULL,workspace_path=? WHERE id=?",
                (c["kanban_task_workspace_path"], p["kanban_task_id"]),
            )
            conn.execute(
                "UPDATE task_runs SET status=?,outcome=?,started_at=?,ended_at=?,metadata=NULL,error=NULL WHERE id=?",
                (
                    c["run_status"],
                    c["run_outcome"],
                    c["run_started_at"],
                    c["run_ended_at"],
                    flow.run_id,
                ),
            )
            conn.commit()
        return result

    monkeypatch.setattr(fixtures, "_c13_review_round_completion", source)
    real_prepare = pr.prepare_current_ticket_review

    def prepare(**kwargs):
        result = real_prepare(**kwargs)
        assert (
            result.get("review_prepare_status") == "prepared_pending_human_acceptance"
        ), json.dumps(result, indent=2)
        return result

    monkeypatch.setattr(pr, "prepare_current_ticket_review", prepare)
    fixture = fixtures._c14_review_authority_fixture(
        pr, tmp_path, monkeypatch, ticket_id=p["ticket_id"], round_count=1
    )
    monkeypatch.setattr(pr, "_load_current_projection_record", real_projection)
    monkeypatch.setattr(
        pr, "_current_projection_record_for_binding", real_binding_projection
    )
    with closing(kb.connect(board=p["kanban_board_slug"])) as conn:
        conn.execute(
            "UPDATE tasks SET status='blocked',current_run_id=NULL,worker_pid=NULL,workspace_path=? WHERE id=?",
            (
                fixture.current_completion["kanban_task_workspace_path"],
                p["kanban_task_id"],
            ),
        )
        conn.commit()
    # Recovery is historical and cannot compete with the accepted publication.
    pr.recovery_action_record_path_for_ticket(p["ticket_id"]).unlink()
    context = pr._current_review_candidate_authority_context(
        projection=p, review_prepare=fixture.review
    )
    snapshot = fixtures._p18_9_2_handoff_git_snapshot(
        status_entries=[],
        path_SHA256={
            path: entry["source_SHA256"] for path, entry in context["files"].items()
        },
    )
    monkeypatch.setattr(
        pr, "_current_handoff_execution_git_snapshot", lambda **kw: deepcopy(snapshot)
    )
    workflow = fixtures._c14_handoff_completion_workflow(pr, p)
    workflow["next_action"]["id"] = pr._human_git_handoff_prepare_action_id(
        pr.resolve_current_ticket_lifecycle_binding(projection_record=p)
    )
    with monkeypatch.context() as patch:
        patch.setattr(pr, "build_workflow_control_snapshot", lambda: workflow)
        result = pr.prepare_current_ticket_human_git_handoff(
            ticket_id=p["ticket_id"], git_snapshot_fn=lambda: snapshot
        )
    assert result["handoff_preparation_recorded"], result
    fixture.flow, fixture.snapshot = flow, snapshot
    fixture.generation = bridge.load_generation_record(ticket_id=p["ticket_id"])
    fixture.binding = rev.context(p)[1]
    fixture.args = dict(
        human_authorization_text=rev.action_id(p["ticket_id"]),
        next_action_id=rev.action_id(p["ticket_id"]),
        binding=fixture.binding,
    )
    return fixture


def test_request_and_replay(accepted):
    f = accepted
    current = pr.build_workflow_control_snapshot()
    assert any(
        a["id"] == rev.action_id(f.ticket_id)
        for a in current.get("alternative_actions", [])
    ), current
    lead = pr.build_lead_agent_operational_context()
    assert any(
        a["id"] == rev.action_id(f.ticket_id) for a in lead["alternative_actions"]
    )
    before = {
        str(path): path.read_bytes()
        for path in (
            pr.review_decision_record_path_for_ticket(f.ticket_id),
            pr.review_prepare_record_path_for_ticket(f.ticket_id),
            pr.human_git_handoff_prepare_record_path_for_ticket(f.ticket_id),
        )
    }
    result = rev.request(**f.args)
    assert result["handoff_state"] == "superseded_by_material_revision"
    assert not result["successor_generated"]
    assert rev.request(**f.args)["idempotent_replay"]
    assert all(Path(path).read_bytes() == raw for path, raw in before.items())
    workflow = fixtures._c14_handoff_completion_workflow(pr, f.projection)
    rev.apply_workflow(workflow, [])
    assert workflow["next_action"]["id"] == "REVISE_P99_4"
    assert workflow["review_state"] == "accepted_historical"
    rebuilt = pr.build_workflow_control_snapshot()
    assert rebuilt["next_action"]["id"] == "REVISE_P99_4"
    assert rebuilt["review_state"] == "accepted_historical"


@pytest.mark.parametrize("dirty", [False, True])
def test_alternative_is_independent_of_unrelated_dirty_state(accepted, dirty):
    f = accepted
    if dirty:
        f.snapshot["status_entries"] = ["?? unrelated/c64.py"]
    workflow = fixtures._c14_handoff_completion_workflow(pr, f.projection)
    rev.apply_workflow(workflow, [])
    assert workflow["alternative_actions"][0]["id"] == rev.action_id(f.ticket_id)
    if dirty:
        handoff = pr.load_current_ticket_human_git_handoff_prepare_record(
            projection_record=f.projection
        )
        assert (
            pr._human_git_handoff_prepare_execution_context_status(
                handoff, git_snapshot=f.snapshot
            )["blocker_code"]
            == "HUMAN_GIT_HANDOFF_UNEXPECTED_DIRTY_STATE"
        )
    rev.request(**f.args)
    rev.apply_workflow(workflow, [])
    assert workflow["next_action"]["id"] == "REVISE_P99_4"


@pytest.mark.parametrize(
    "field",
    [
        "project_id",
        "ticket_id",
        "work_packet_SHA256",
        "ticket_spec_SHA256",
        "projection_SHA256",
        "publication_revision",
        "reviewed_run_id",
        "review_decision_SHA256",
        "review_decision_identity_SHA256",
        "review_package_SHA256",
        "P17_7_handoff_package_SHA256",
        "handoff_prepare_record_SHA256",
        "handoff_prepare_identity_SHA256",
    ],
)
def test_exact_request_guards(accepted, field):
    args = deepcopy(accepted.args)
    args["binding"][field] = "wrong"
    with pytest.raises(ValueError):
        rev.request(**args)
    assert not rev.path_for(accepted.generation).exists()


@pytest.mark.parametrize(
    "text", ["", "continue", "PREPARE_P99_4_HUMAN_GIT_HANDOFF", "REVISE_P99_4"]
)
def test_authorization_is_a_separate_decision(accepted, text):
    with pytest.raises(ValueError):
        rev.request(**{**accepted.args, "human_authorization_text": text})
    assert not rev.path_for(accepted.generation).exists()


@pytest.mark.parametrize(
    "mode",
    [
        "completion",
        "active",
        "claim",
        "materialized",
        "staged",
        "missing_source",
        "source_drift",
        "successor",
        "conflict",
    ],
)
def test_prohibited_states(accepted, mode):
    f = accepted
    if mode == "completion":
        path = pr.human_git_handoff_completion_record_path_for_ticket(f.ticket_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")
    elif mode in {"active", "claim"}:
        with closing(kb.connect(board=f.projection["kanban_board_slug"])) as conn:
            if mode == "active":
                conn.execute(
                    "UPDATE tasks SET current_run_id=? WHERE id=?",
                    (f.flow.run_id, f.projection["kanban_task_id"]),
                )
            else:
                conn.execute(
                    "UPDATE tasks SET claim_lock='unresolved' WHERE id=?",
                    (f.projection["kanban_task_id"],),
                )
            conn.commit()
    elif mode in {"materialized", "missing_source", "source_drift"}:
        handoff = pr.load_current_ticket_human_git_handoff_prepare_record(
            projection_record=f.projection
        )
        _source, candidate = pr._handoff_record_candidate_sha_maps(handoff)
        f.snapshot["path_SHA256"] = (
            candidate
            if mode == "materialized"
            else {}
            if mode == "missing_source"
            else {p: "f" * 64 for p in candidate}
        )
    elif mode == "staged":
        f.snapshot["status_entries"] = ["M  " + f.candidate_path]
    elif mode == "successor":
        bridge.generation_record_path_for_ticket("P99.5").write_text(
            json.dumps({"ticket_id": "P99.5", "predecessor_ticket_id": f.ticket_id})
        )
    else:
        from hermes_cli.agent_platform import retry_material_revision

        path = retry_material_revision.path_for(f.generation)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")
    with pytest.raises(ValueError):
        rev.request(**f.args)
    assert not rev.path_for(f.generation).exists()


@pytest.mark.parametrize("decision", [None, "reject", "changes_requested"])
def test_nonaccepted_review_cannot_reopen(accepted, decision):
    f = accepted
    path = pr.review_decision_record_path_for_ticket(f.ticket_id)
    if decision is None:
        path.unlink()
    else:
        record = json.loads(path.read_text())
        record["review_decision"] = decision
        path.write_text(json.dumps(record))
    with pytest.raises(ValueError):
        rev.request(**f.args)
    assert not rev.path_for(f.generation).exists()


def test_conflicting_replay_and_corruption_fail_closed(accepted):
    f = accepted
    rev.request(**f.args)
    with pytest.raises(ValueError):
        rev.request(**f.args, authorizer_id="different-human")
    path = rev.path_for(f.generation)
    raw = json.loads(path.read_text())
    raw["review_decision_SHA256"] = "wrong"
    path.write_text(json.dumps(raw))
    workflow = fixtures._c14_handoff_completion_workflow(pr, f.projection)
    blockers = []
    rev.apply_workflow(workflow, blockers)
    assert workflow["workflow_status"] == "material_revision_authority_blocked"
    with pytest.raises(ValueError, match="superseded"):
        pr.prepare_current_ticket_human_git_handoff(ticket_id=f.ticket_id)


def test_old_handoff_entrypoints_are_closed(accepted):
    f = accepted
    rev.request(**f.args)
    with pytest.raises(ValueError, match="superseded"):
        pr.prepare_current_ticket_human_git_handoff(ticket_id=f.ticket_id)
    with pytest.raises(ValueError, match="superseded"):
        pr.complete_current_ticket_human_git_handoff(
            ticket_id=f.ticket_id,
            reviewed_run_id=f.flow.run_id,
            reviewed_candidate_SHA256=f.accepted_record["reviewed_candidate_SHA256"],
            review_decision_SHA256=f.accepted_record["review_decision_SHA256"],
            commits=["a" * 40],
            branch="synthetic-handoff",
            push_attestation="Human completed push.",
            validation_evidence=["Isolated persisted validation passed."],
            approved_committed_paths=[f.candidate_path],
        )


def test_restart_history_and_no_candidate_writes(accepted):
    f = accepted
    paths = [
        p
        for source in f.round_sources
        for p in Path(source.completion["kanban_task_workspace_path"]).rglob("*")
        if p.is_file()
    ]
    before = {p: p.read_bytes() for p in paths}
    result = rev.request(**f.args)
    import importlib

    importlib.reload(rev)
    workflow = fixtures._c14_handoff_completion_workflow(pr, f.projection)
    rev.apply_workflow(workflow, [])
    assert workflow["next_action"]["id"] == "REVISE_P99_4"
    history = rev.inspect_history(
        ticket_id=f.ticket_id, work_packet_SHA256=f.generation["work_packet_SHA256"]
    )
    assert (
        history["transition"]["material_revision_request_SHA256"]
        == result["material_revision_request_SHA256"]
    )
    assert (
        history["transition"]["historical_authority"]["review_decision"]
        == f.accepted_record
    )
    assert all(p.read_bytes() == data for p, data in before.items())


@pytest.mark.parametrize("accepted", [4], indirect=True)
def test_separate_generation_produces_revision_five(accepted, monkeypatch, tmp_path):
    f = accepted
    assert f.generation["ticket_publication_result"]["publication"]["revision"] == 4
    record = rev.request(**f.args)
    workflow = fixtures._c14_handoff_completion_workflow(pr, f.projection)
    rev.apply_workflow(workflow, [])
    with monkeypatch.context() as patch:
        patch.setattr(pr, "build_workflow_control_snapshot", lambda: workflow)
        result = pr.revise_current_ticket_for_material_contract_failure(
            human_authorization_text="I explicitly authorize revision of P99.4.",
            revision_contract={
                "ticket_id": f.ticket_id,
                "objective": "Implement the newly specified visual hierarchy using current canonical source.",
            },
            ticket_id=f.ticket_id,
            next_action_id="REVISE_P99_4",
        )
    assert result["revision_status"] == "awaiting_ticket_approval"
    revised = bridge.load_generation_record(ticket_id=f.ticket_id)
    assert revised["ticket_publication_result"]["publication"]["revision"] == 5
    assert revised["ticket_id"] == f.ticket_id
    assert revised["work_packet_SHA256"] != f.generation["work_packet_SHA256"]
    assert revised["ticket_spec_SHA256"] != f.generation["ticket_spec_SHA256"]
    assert (
        revised["revision_authority"]["material_revision_request_SHA256"]
        == record["material_revision_request_SHA256"]
    )
    assert (
        bridge.load_approval_decision_record(
            ticket_id=f.ticket_id, generation_record=revised
        )
        is None
    )
    assert result["active_execution_count"] == 0
    assert (
        pr.build_workflow_control_snapshot()["workflow_status"]
        == "awaiting_ticket_approval"
    )
    history = rev.inspect_history(
        ticket_id=f.ticket_id, work_packet_SHA256=f.generation["work_packet_SHA256"]
    )
    assert (
        history["transition"]["historical_authority"]["review_decision"]
        == f.accepted_record
    )
    candidate = rev.inspect_history(
        ticket_id=f.ticket_id,
        work_packet_SHA256=f.generation["work_packet_SHA256"],
        evidence_section="content",
        candidate_path=f.candidate_path,
    )
    assert candidate["historical"] and candidate["read_only"]
    assert candidate["inspection_status"] == "content_available"
    # A separate human approval permits a fresh projection, never a worker.
    from hermes_cli.agent_platform.workflow import (
        work_packet_kanban_projection as projection,
    )
    from tools import governed_workpacket_file_guard as guard

    bridge.apply_ticket_approval_decision(
        ticket_id=f.ticket_id, decision="approve", actor="isolated-human"
    )
    projection.project_current_approved_workpacket_to_kanban(
        workflow=pr.build_workflow_control_snapshot()
    )
    current = pr._load_current_projection_record()
    assert current["projection_SHA256"] != f.projection["projection_SHA256"]
    assert current["work_packet_SHA256"] == revised["work_packet_SHA256"]
    assert pr.build_workflow_control_snapshot()["active_execution_count"] == 0
    canonical = tmp_path / "canonical-r5"
    relative = "2_products/pepper-agent/web/src/agent-platform/shell/c73.ts"
    source = canonical / relative
    source.parent.mkdir(parents=True)
    source.write_text("current canonical R5 source")
    old_scratch = Path(f.current_completion["kanban_task_workspace_path"]) / relative
    old_scratch.parent.mkdir(parents=True, exist_ok=True)
    old_scratch.write_text("obsolete R4 scratch bytes")
    fixtures._write_web_read_only_validation_support_file(canonical)
    scratch = tmp_path / "fresh-r5-scratch"
    scratch.mkdir()
    env = {
        guard.WORKPACKET_ID_ENV: current["work_packet_id"],
        guard.WORKPACKET_SHA256_ENV: current["work_packet_SHA256"],
        guard.TICKET_SPEC_SHA256_ENV: current["ticket_spec_SHA256"],
        guard.KANBAN_PROJECTION_SHA256_ENV: current["projection_SHA256"],
        guard.GENERATION_RECORD_PATH_ENV: str(
            bridge.generation_record_path_for_ticket(f.ticket_id)
        ),
        guard.APPROVAL_DECISION_RECORD_PATH_ENV: str(
            bridge.approval_decision_record_path_for_ticket(f.ticket_id)
        ),
        guard.KANBAN_PROJECTION_RECORD_PATH_ENV: str(
            projection.kanban_projection_record_path_for_ticket(f.ticket_id)
        ),
        "HERMES_KANBAN_WORKSPACE": str(scratch),
        "TERMINAL_CWD": str(scratch),
    }
    authority = guard.resolve_governed_workpacket_file_authority(env)
    with monkeypatch.context() as patch:
        patch.setattr(pr, "_agent_platform_repository_root", lambda: canonical)
        materialized = pr._materialize_workpacket_scratch_source_tree(authority)
    assert materialized["work_packet_SHA256"] == revised["work_packet_SHA256"]
    assert (
        (scratch / relative).read_text()
        == source.read_text()
        == "current canonical R5 source"
    )
    assert old_scratch.read_text() == "obsolete R4 scratch bytes"
    assert Path(f.current_completion["kanban_task_workspace_path"]) != scratch
    assert pr.build_workflow_control_snapshot()["active_execution_count"] == 0


@pytest.mark.parametrize("change", ["projection", "completion", "execution", "review"])
def test_revalidates_before_persisting(accepted, monkeypatch, change):
    f = accepted
    original = rev.context
    count = 0

    def context(*args, **kwargs):
        nonlocal count
        count += 1
        if count == 2:
            if change == "completion":
                path = pr.human_git_handoff_completion_record_path_for_ticket(
                    f.ticket_id
                )
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}")
            elif change == "execution":
                with closing(
                    kb.connect(board=f.projection["kanban_board_slug"])
                ) as conn:
                    conn.execute(
                        "UPDATE tasks SET current_run_id=? WHERE id=?",
                        (f.flow.run_id, f.projection["kanban_task_id"]),
                    )
                    conn.commit()
            elif change == "review":
                pr.review_decision_record_path_for_ticket(f.ticket_id).unlink()
            else:
                changed = deepcopy(args[0])
                changed["work_packet_SHA256"] = "f" * 64
                args = (changed,)
        return original(*args, **kwargs)

    monkeypatch.setattr(rev, "context", context)
    with pytest.raises(ValueError):
        rev.request(**f.args)
    assert not rev.path_for(f.generation).exists()


def test_tool_boundary_and_historical_diagnosis(accepted):
    from tools import pepper_workflow_tools as tools

    f = accepted
    f.snapshot["status_entries"] = ["?? unrelated/c64.py"]
    args = {
        "origin": "post_accept",
        "human_authorization_text": f.args["human_authorization_text"],
        "request_binding": f.binding,
        "next_action_id": f.args["next_action_id"],
    }
    assert not json.loads(
        tools._request_current_ticket_material_revision({
            **args,
            "user_task": "continue",
        })
    )["success"]
    result = json.loads(tools._request_current_ticket_material_revision(args))
    assert result["success"]
    history = json.loads(
        tools._inspect_current_ticket_review_candidate({
            "operation": "post_accept_history",
            "ticket_id": f.ticket_id,
            "work_packet_SHA256": f.generation["work_packet_SHA256"],
            "evidence_section": "handoff_diagnosis",
        })
    )
    assert (
        json.loads(history["evidence_text"])["blocker_code"]
        == "HUMAN_GIT_HANDOFF_UNEXPECTED_DIRTY_STATE"
    )
    f.snapshot["head"] = "d" * 40
    assert rev.request(**f.args)["idempotent_replay"]


def test_supersession_precedence_when_old_review_becomes_invalid(accepted):
    f = accepted
    rev.request(**f.args)
    pr.review_decision_record_path_for_ticket(f.ticket_id).unlink()
    workflow = fixtures._c14_handoff_completion_workflow(pr, f.projection)
    workflow["workflow_status"] = "blocked"
    rev.apply_workflow(workflow, [])
    assert workflow["workflow_status"] == "material_revision_authority_blocked"
    assert workflow["next_action"]["id"] == "RECONCILE_MATERIAL_REVISION_AUTHORITY"


def test_simultaneous_exact_requests_are_one_decision(accepted):
    from concurrent.futures import ThreadPoolExecutor

    f = accepted
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: rev.request(**f.args), range(2)))
    assert {r["idempotent_replay"] for r in results} == {False, True}
    assert len({r["material_revision_request_SHA256"] for r in results}) == 1
    assert len(list(rev.path_for(f.generation).parent.glob("*.json"))) == 1


def test_history_rejects_nested_tampering_even_when_outer_digest_is_resealed(accepted):
    f = accepted
    rev.request(**f.args)
    path = rev.path_for(f.generation)
    raw = json.loads(path.read_text())
    raw["historical_authority"]["handoff"]["candidate_paths"] = ["elsewhere.py"]
    raw["material_revision_request_SHA256"] = rev.digest(raw)
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match="historical authority digest"):
        rev.inspect_history(
            ticket_id=f.ticket_id, work_packet_SHA256=f.generation["work_packet_SHA256"]
        )
