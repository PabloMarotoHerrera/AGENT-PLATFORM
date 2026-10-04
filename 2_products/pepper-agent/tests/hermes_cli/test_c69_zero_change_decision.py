"""C69 uses isolated homes; dispatch substitutes only the worker process boundary."""

import json
import shutil
from pathlib import Path

import pytest
from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import execution_evidence as ev
from hermes_cli.agent_platform import zero_change_decision as decision
from hermes_cli.agent_platform import terminal_candidate_evidence as retained
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c66_invalid_validation_command_revision import (
    evidence as evidence,
)
from tests.hermes_cli.test_c68_execution_evidence import source_fixture
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tools import pepper_workflow_tools as tools

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


@pytest.fixture
def completed(flow, evidence):
    p = evidence.projected
    candidate = evidence.workspace / "2_products/pepper-agent/web/src/example.ts"
    candidate.parent.mkdir(parents=True)
    candidate.write_text("governed implementation")
    source_fixture(p, flow.run_id, evidence.workspace)
    pr.recovery_action_record_path_for_ticket(p["ticket_id"]).unlink()
    conn = kb.connect(board=p["kanban_board_slug"])
    try:
        conn.execute(
            "UPDATE tasks SET status='done',current_run_id=NULL,worker_pid=NULL,claim_lock=NULL WHERE id=?",
            (p["kanban_task_id"],),
        )
        conn.execute(
            "UPDATE task_runs SET status='done',outcome='completed',metadata=?,error=NULL WHERE id=?",
            (json.dumps(fixtures._c19_legacy_semantic_noop_metadata()), flow.run_id),
        )
        conn.commit()
    finally:
        conn.close()
    flow.p = p
    flow.workspace = evidence.workspace
    flow.reject = dict(
        human_authorization_text=decision.action(p["ticket_id"], flow.run_id),
        run_id=flow.run_id,
        **{
            k: p[k]
            for k in (
                "ticket_id",
                "project_id",
                "ticket_spec_SHA256",
                "work_packet_SHA256",
                "projection_SHA256",
            )
        },
    )
    return flow


def runs(f):
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        return [pr._run_dict(r) for r in kb.list_runs(conn, f.p["kanban_task_id"])]
    finally:
        conn.close()


def test_reject_choices_state_and_idempotence(completed):
    f = completed
    w = pr.build_workflow_control_snapshot()
    assert (
        w["workflow_status"] == "execution_completed_pending_zero_change_attestation"
    ), w
    assert w["next_action"]["id"].startswith("ATTEST_")
    assert w["alternative_actions"][0]["id"] == f.reject["human_authorization_text"]
    before = runs(f)
    result = decision.request(**f.reject)
    assert result["human_decision"] == "zero_change_rejected"
    assert result["execution_started"] is False
    assert result["retry_budget_consumed"] is False
    assert runs(f) == before
    assert decision.request(**f.reject)["idempotent_replay"] is True
    w = pr.build_workflow_control_snapshot()
    assert w["governed_workflow_state"] == decision.STATE
    assert (
        w["next_action"]["required_human_authorization_text"]
        != f.reject["human_authorization_text"]
    )
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.attest_current_ticket_zero_change_for_review_prepare(
            human_attestation_text=pr.governed_ticket_zero_change_attestation_text(
                f.p["ticket_id"]
            ),
            project_id=f.p["project_id"],
            ticket_id=f.p["ticket_id"],
            next_action_id=pr.governed_ticket_lifecycle_action_ids(f.p["ticket_id"])[
                "zero_change_attestation"
            ],
        )
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.prepare_current_ticket_review(ticket_id=f.p["ticket_id"])


@pytest.mark.parametrize(
    "field,value",
    [
        ("human_authorization_text", ""),
        ("human_authorization_text", "ATTEST P99.4 ZERO CHANGE FOR REVIEW PREPARE"),
        ("ticket_id", "P99.5"),
        ("run_id", 999),
        ("ticket_spec_SHA256", "0" * 64),
        ("work_packet_SHA256", "0" * 64),
        ("projection_SHA256", "0" * 64),
    ],
)
def test_rejection_guards(completed, field, value):
    with pytest.raises((ValueError, pr.ProductRuntimeConflict)):
        decision.request(**{**completed.reject, field: value})
    assert not decision.path_for(completed.p, completed.run_id).exists()


def test_positive_excludes_negative(completed):
    f = completed
    pr.attest_current_ticket_zero_change_for_review_prepare(
        human_attestation_text=pr.governed_ticket_zero_change_attestation_text(
            f.p["ticket_id"]
        ),
        project_id=f.p["project_id"],
        ticket_id=f.p["ticket_id"],
        next_action_id=pr.governed_ticket_lifecycle_action_ids(f.p["ticket_id"])[
            "zero_change_attestation"
        ],
    )
    with pytest.raises(pr.ProductRuntimeConflict):
        decision.request(**f.reject)


@pytest.mark.parametrize("changed", [False, True])
def test_durable_evidence_before_real_cleanup_and_after_removal(completed, changed):
    f = completed
    if changed:
        (f.workspace / "2_products/pepper-agent/web/src/example.ts").write_text(
            "changed"
        )
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        kb._cleanup_workspace(conn, f.p["kanban_task_id"])
    finally:
        conn.close()
    if changed:
        assert f.workspace.exists()  # Content remains available for ordinary review.
        shutil.rmtree(f.workspace)  # Simulate later removal of this isolated fixture.
    assert not f.workspace.exists()
    result = ev.inspect(
        ticket_id=f.p["ticket_id"], run_id=f.run_id, section="candidate"
    )["candidate"]
    assert result["zero_change_status"] == ("CONTRADICTED" if changed else "PROVEN"), (
        result
    )
    assert result["candidate_exists"] is False
    assert result["terminal_evidence_SHA256"]


def test_capture_gap_preserves_workspace(completed):
    f = completed
    (f.workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).unlink()
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        kb._cleanup_workspace(conn, f.p["kanban_task_id"])
    finally:
        conn.close()
    assert f.workspace.exists()


def test_legacy_absence_never_proven(completed):
    f = completed
    shutil.rmtree(f.workspace)
    result = ev.inspect(
        ticket_id=f.p["ticket_id"], run_id=f.run_id, section="candidate"
    )["candidate"]
    assert result["zero_change_status"] == "UNAVAILABLE"
    assert decision.request(**f.reject)["human_decision"] == "zero_change_rejected"


def test_fresh_corrective_dispatch(completed, monkeypatch):
    f = completed
    before = runs(f)
    rejected = decision.request(**f.reject)
    args = dict(
        ticket_id=f.p["ticket_id"],
        run_id=f.run_id,
        decision_SHA256=rejected["decision_SHA256"],
        human_authorization_text=decision.action(
            f.p["ticket_id"], f.run_id, corrective=True
        ),
    )
    with pytest.raises(pr.ProductRuntimeConflict):
        decision.start(**{
            **args,
            "human_authorization_text": f.reject["human_authorization_text"],
        })
    monkeypatch.setattr(
        pr, "_executor_provider_readiness", fixtures._ready_executor_provider_payload
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda *a, **kw: fixtures._ready_worker_credential_probe(),
    )
    monkeypatch.setattr(pr, "_pepper_governed_worker_env_overlay", lambda p: {})
    # Fixture source substitution only: no Git subprocess, actual claim/rearm and spawn boundary execute.
    monkeypatch.setattr(
        pr,
        "_prepare_governed_source_authority_for_dispatch",
        lambda **kw: ({"source_materialized": True}, {}),
    )
    monkeypatch.setattr(kb, "_pid_alive", lambda pid: pid == 4321)
    seen = []
    result = decision.start(
        **args,
        spawn_fn=lambda task, workspace, board=None: (
            seen.append((task, workspace)) or 4321
        ),
    )
    assert result["execution_started"] is True, json.dumps(result, indent=2)
    assert len(seen) == 1
    after = runs(f)
    assert after[:-1] == before
    assert len(after) == len(before) + 1
    assert str(seen[0][1]) != str(f.workspace)
    body = json.loads(seen[0][0].body)
    assert body["WorkPacket_SHA256"] == f.p["work_packet_SHA256"]
    assert body["corrective_implementation_intent"].startswith("Implement the original")
    assert decision.start(
        **args, spawn_fn=lambda *a, **k: pytest.fail("duplicate dispatch")
    )["idempotent_replay"]


def test_tool_rejects_arbitrary_arguments(completed):
    args = {"operation": "reject", **completed.reject, "path": "/tmp/arbitrary"}
    assert (
        json.loads(tools._decide_current_ticket_zero_change(args))["success"] is False
    )


@pytest.mark.parametrize("status,outcome", [("running", None), ("failed", "failed")])
def test_noncompleted_run_rejected(completed, status, outcome):
    f = completed
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        conn.execute(
            "UPDATE task_runs SET status=?,outcome=? WHERE id=?",
            (status, outcome, f.run_id),
        )
        conn.commit()
    finally:
        conn.close()
    with pytest.raises(pr.ProductRuntimeConflict):
        decision.request(**f.reject)


def test_conflicting_replay_and_tampered_decision(completed):
    f = completed
    decision.request(**f.reject)
    with pytest.raises(pr.ProductRuntimeConflict):
        decision.request(**f.reject, reviewer_id="different-human")
    path = decision.path_for(f.p, f.run_id)
    data = json.loads(path.read_text())
    data["run_id"] = 999
    path.write_text(json.dumps(data))
    with pytest.raises(pr.ProductRuntimeConflict):
        decision.request(**f.reject)
    w = pr.build_workflow_control_snapshot()
    assert any(
        b["id"] == "ZERO-CHANGE-DECISION-AUTHORITY" for b in w["remaining_blockers"]
    )


def test_retained_manifest_tampering_fails_closed(completed):
    f = completed
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        assert retained.before_cleanup(conn, f.p["kanban_task_id"])
        run = kb.get_run(conn, f.run_id)
    finally:
        conn.close()
    path = retained.path_for(f.p, run)
    data = json.loads(path.read_text())
    data["candidate"]["files"][0]["candidate_SHA256"] = "0" * 64
    data["evidence_SHA256"] = ev.digest({
        k: v for k, v in data.items() if k != "evidence_SHA256"
    })
    path.write_text(json.dumps(data))
    shutil.rmtree(f.workspace)
    result = ev.inspect(
        ticket_id=f.p["ticket_id"], run_id=f.run_id, section="candidate"
    )["candidate"]
    assert result["available"] is False


def test_old_start_consent_does_not_authorize_correction(completed):
    f = completed
    decision.request(**f.reject)
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.start_current_ticket_execution(
            human_authorization_text="Start P99.4 execution now",
            ticket_id=f.p["ticket_id"],
        )


def test_refusal_does_not_require_available_source_evidence(completed):
    f = completed
    path = pr.governed_source_authority_record_path_for_run(f.p, f.run_id)
    path.unlink()
    result = decision.request(**f.reject)
    assert result["source_authority_identity"]["available"] is False
    assert result["human_decision"] == "zero_change_rejected"


def test_positive_negative_cross_process_lock_boundary(completed):
    f = completed
    path = decision.path_for(f.p, f.run_id, "lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("held by another process")
    with pytest.raises(pr.ProductRuntimeConflict, match="in progress"):
        decision.request(**f.reject)
    with pytest.raises(pr.ProductRuntimeConflict, match="in progress"):
        pr.attest_current_ticket_zero_change_for_review_prepare(
            human_attestation_text=pr.governed_ticket_zero_change_attestation_text(
                f.p["ticket_id"]
            ),
            project_id=f.p["project_id"],
            ticket_id=f.p["ticket_id"],
            next_action_id=pr.governed_ticket_lifecycle_action_ids(f.p["ticket_id"])[
                "zero_change_attestation"
            ],
        )
    assert path.read_text() == "held by another process"


def test_tool_cannot_override_spawn_boundary(completed):
    result = json.loads(
        tools._decide_current_ticket_zero_change({
            "operation": "start_corrective",
            "ticket_id": completed.p["ticket_id"],
            "run_id": completed.run_id,
            "human_authorization_text": "anything",
            "decision_SHA256": "0" * 64,
            "spawn_fn": "arbitrary",
        })
    )
    assert result["success"] is False
    assert "unsupported" in str(result)


def test_failed_durable_flush_retains_only_equality_proof(completed, monkeypatch):
    f = completed
    monkeypatch.setattr(
        retained,
        "sync_record",
        lambda p: (_ for _ in ()).throw(OSError("flush failed")),
    )
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        kb._cleanup_workspace(conn, f.p["kanban_task_id"])
    finally:
        conn.close()
    assert f.workspace.exists()


def test_decision_never_targets_older_terminal_run(completed):
    f = completed
    conn = kb.connect(board=f.p["kanban_board_slug"])
    try:
        conn.execute(
            "INSERT INTO task_runs(task_id,profile,status,outcome,started_at,ended_at) VALUES(?,?,'done','completed',1,2)",
            (f.p["kanban_task_id"], f.p["assignee_profile"]),
        )
        conn.commit()
    finally:
        conn.close()
    with pytest.raises((ValueError, pr.ProductRuntimeConflict), match="current"):
        decision.request(**f.reject)


def test_refusal_does_not_require_source_snapshot_files(completed):
    f = completed
    path = pr.governed_source_authority_record_path_for_run(f.p, f.run_id)
    source = json.loads(path.read_text())
    shutil.rmtree(source["snapshot_root"])
    result = decision.request(**f.reject)
    assert (
        result["source_authority_identity"]["authority_SHA256"]
        == source["governed_source_authority_SHA256"]
    )
    assert pr.build_workflow_control_snapshot()["workflow_status"] == decision.STATE
