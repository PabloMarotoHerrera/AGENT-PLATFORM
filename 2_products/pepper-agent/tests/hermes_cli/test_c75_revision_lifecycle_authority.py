"""Current execution is independent of authenticated predecessor review history."""

import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import post_accept_material_revision as revision
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)
from tests.hermes_cli.test_c73_post_accept_material_revision import (
    accepted as accepted,
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)


@pytest.fixture
def successor(accepted):
    f = accepted
    paths = [
        pr.review_decision_record_path_for_ticket(f.ticket_id),
        pr.review_prepare_record_path_for_ticket(f.ticket_id),
        pr.human_git_handoff_prepare_record_path_for_ticket(f.ticket_id),
    ]
    saved = {p: p.read_bytes() for p in paths}
    revision.request(**f.args)
    result = pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text=f"I explicitly authorize revision of {f.ticket_id}.",
        ticket_id=f.ticket_id,
        next_action_id=bridge.revise_action_id(f.ticket_id),
        revision_contract={
            "ticket_id": f.ticket_id,
            "objective": "Implement the next complete visual revision from fresh canonical source.",
        },
    )
    assert result["revision_status"] == "awaiting_ticket_approval"
    bridge.apply_ticket_approval_decision(
        ticket_id=f.ticket_id, decision="approve", actor="isolated-human"
    )
    projected = projection.project_current_approved_workpacket_to_kanban(
        workflow=pr.build_workflow_control_snapshot()
    )
    p = projection.load_kanban_projection_record(ticket_id=f.ticket_id)
    return SimpleNamespace(prior=f, p=p, projected=projected, saved=saved)


@pytest.mark.parametrize("accepted", [4], indirect=True)
def test_current_revision_does_not_require_predecessor_review(successor):
    f = successor
    state = pr.build_workflow_control_snapshot()
    assert not state["remaining_blockers"], json.dumps(
        state["remaining_blockers"], indent=2
    )
    assert state["workflow_status"] == "queued"
    assert f.p["ticket_spec_SHA256"] != f.prior.projection["ticket_spec_SHA256"]
    assert all(p.read_bytes() == raw for p, raw in f.saved.items())
    for reader in (
        pr.load_current_ticket_review_decision_record,
        pr.load_current_ticket_review_prepare_record,
        pr.load_current_ticket_human_git_handoff_prepare_record,
    ):
        assert reader(projection_record=f.p) is None
    history = revision.inspect_history(
        ticket_id=f.p["ticket_id"],
        work_packet_SHA256=f.prior.projection["work_packet_SHA256"],
    )
    assert history["historical"] and not history["current_handoff_executable"]
    assert (
        history["transition"]["historical_authority"]["review_decision"][
            "ticket_spec_SHA256"
        ]
        == f.prior.projection["ticket_spec_SHA256"]
    )
    # Fresh reads and idempotent reprojection must not revive predecessor authority.
    projection.project_current_approved_workpacket_to_kanban(
        workflow=pr.build_workflow_control_snapshot()
    )
    assert (
        pr._load_current_projection_record()["projection_SHA256"]
        == f.p["projection_SHA256"]
    )
    assert not pr.build_workflow_control_snapshot()["remaining_blockers"]
    code = """
import json,sys
from hermes_cli.agent_platform import product_runtime as pr
p=json.load(open(sys.argv[1]))
assert pr.load_current_ticket_review_decision_record(projection_record=p) is None
assert pr.load_current_ticket_review_prepare_record(projection_record=p) is None
assert pr.load_current_ticket_human_git_handoff_prepare_record(projection_record=p) is None
print('historical selection reconstructed from durable authority')
"""
    env = {**os.environ, "HERMES_HOME": str(f.prior.flow.home)}
    restarted = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(projection.kanban_projection_record_path_for_ticket(f.p["ticket_id"])),
        ],
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert restarted.returncode == 0, restarted.stderr


def start(f, **kwargs):
    return pr.start_current_ticket_execution(
        human_authorization_text=kwargs.pop(
            "text", f"Start {f.p['ticket_id']} execution now"
        ),
        ticket_id=f.p["ticket_id"],
        **kwargs,
    )


def forbidden(*args, **kwargs):
    pytest.fail("No real worker or external process may run")


@pytest.mark.parametrize("accepted", [4], indirect=True)
def test_explicit_start_binds_fresh_current_revision(successor, monkeypatch):
    f = successor
    calls = []
    fixtures._patch_synthetic_scratch_materialization(monkeypatch, pr)
    original = pr._materialize_pepper_governed_scratch_source

    def materialize(p, workspace, **kwargs):
        assert p["work_packet_SHA256"] == f.p["work_packet_SHA256"]
        assert Path(workspace) != Path(
            f.prior.current_completion["kanban_task_workspace_path"]
        )
        calls.append(("materialize", p["work_packet_SHA256"]))
        return original(p, workspace, **kwargs)

    monkeypatch.setattr(pr, "_materialize_pepper_governed_scratch_source", materialize)
    monkeypatch.setattr(
        pr, "_executor_provider_readiness", fixtures._ready_executor_provider_payload
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda *a, **k: fixtures._ready_worker_credential_probe(),
    )
    monkeypatch.setattr(pr, "_pepper_governed_worker_env_overlay", lambda p: {})
    monkeypatch.setattr(
        pr,
        "_run_source_authority_git",
        lambda *a: subprocess.CompletedProcess(a, 1, "", "isolated source"),
    )
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(kb, "_pid_alive", lambda pid: pid == os.getpid())

    def spawn(task, workspace, **kwargs):
        assert task.id == f.p["kanban_task_id"] != f.prior.projection["kanban_task_id"]
        assert Path(workspace).is_relative_to(f.prior.flow.home)
        calls.append(("spawn", task.id))
        return os.getpid()

    result = start(f, spawn_fn=spawn)
    assert result["start_status"] == "started", json.dumps(result, indent=2)
    authority = pr.load_p18_9_0_execution_start_record(projection_record=f.p)
    assert authority["ticket_spec_SHA256"] == f.p["ticket_spec_SHA256"]
    assert authority["work_packet_SHA256"] == f.p["work_packet_SHA256"]
    assert authority["projection_SHA256"] == f.p["projection_SHA256"]
    assert calls == [
        ("materialize", f.p["work_packet_SHA256"]),
        ("spawn", f.p["kanban_task_id"]),
    ]
    assert all(p.read_bytes() == raw for p, raw in f.saved.items())
    source = result["durable_source_authority_reference"]
    assert source["work_packet_SHA256"] == f.p["work_packet_SHA256"]
    assert source["projection_SHA256"] == f.p["projection_SHA256"]
    assert result["durable_source_authority_validated_before_worker_execution"]
    assert (
        "synthetic = true"
        in (
            Path(result["workspace_path"]) / "2_products/pepper-agent/web/src/App.tsx"
        ).read_text()
    )
    (f.prior.flow.home / "c75-isolated-proof.json").write_text(
        json.dumps(
            {
                "prior_projection": f.prior.projection,
                "current_projection": f.p,
                "execution_start": result,
                "execution_authority": authority,
                "historical_review": json.loads(next(iter(f.saved.values()))),
                "historical_files_unchanged": True,
                "real_worker_started": False,
                "materialization_seam": "fresh deterministic fixture source; real durable source binding/validation",
            },
            indent=2,
        )
    )


def test_no_human_authorization(successor):
    result = start(successor, text="Do not start execution", spawn_fn=forbidden)
    assert result["start_status"] == "blocked"
    assert result["execution_started"] is False


@pytest.mark.parametrize(
    "field",
    ["projection_SHA256", "ticket_spec_SHA256", "work_packet_SHA256", "kanban_task_id"],
)
def test_wrong_current_projection_blocks(successor, monkeypatch, field):
    bad = deepcopy(successor.p)
    bad[field] = "0" * 64
    monkeypatch.setattr(pr, "_load_current_projection_record", lambda: bad)
    try:
        result = start(successor, spawn_fn=forbidden)
    except (
        pr.ProductRuntimeError,
        bridge.TicketArchitectBridgeError,
        projection.WorkPacketKanbanProjectionError,
    ):
        return
    assert result["start_status"] == "blocked"


@pytest.mark.parametrize(
    "kind",
    [
        "missing_approval",
        "tampered_approval",
        "current_autonomy",
        "execution_authority",
        "missing_transition",
        "corrupt_transition",
        "historical_review",
        "historical_package",
        "historical_handoff",
        "wrong_revision",
    ],
)
def test_required_authority_corruption_blocks(successor, kind):
    f = successor
    if kind in {"missing_approval", "tampered_approval"}:
        path = bridge.approval_decision_record_path_for_ticket(f.p["ticket_id"])
    elif kind == "current_autonomy":
        path = pr.governed_autonomy_activation_record_path_for_ticket(f.p["ticket_id"])
    elif kind == "execution_authority":
        path = pr.execution_start_record_path_for_ticket(f.p["ticket_id"])
    elif kind in {"missing_transition", "corrupt_transition"}:
        path = revision.path_for(f.prior.generation)
    elif kind == "wrong_revision":
        path = bridge.generation_record_path_for_ticket(f.p["ticket_id"])
    else:
        path = list(f.saved)[
            ["historical_review", "historical_package", "historical_handoff"].index(
                kind
            )
        ]
    if kind.startswith("missing_"):
        path.unlink()
    else:
        data = json.loads(path.read_text()) if path.exists() else dict(f.p)
        if kind == "wrong_revision":
            data["ticket_publication_result"]["publication"]["revision"] += 1
        else:
            data["ticket_spec_SHA256"] = "0" * 64
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
    try:
        result = start(f, spawn_fn=forbidden)
    except (
        pr.ProductRuntimeError,
        bridge.TicketArchitectBridgeError,
        projection.WorkPacketKanbanProjectionError,
        ValueError,
    ):
        return
    assert result["start_status"] == "blocked", result


def test_stale_task_and_projection_cannot_start(successor, monkeypatch):
    path = projection.kanban_projection_record_path_for_ticket(successor.p["ticket_id"])
    path.write_text(json.dumps(successor.prior.projection))
    try:
        result = start(successor, spawn_fn=forbidden)
    except (
        pr.ProductRuntimeError,
        bridge.TicketArchitectBridgeError,
        projection.WorkPacketKanbanProjectionError,
    ):
        return
    assert result["start_status"] == "blocked"


def test_concurrent_identity_change_blocks(successor, monkeypatch):
    original = pr.build_workflow_control_snapshot

    def changed():
        path = projection.kanban_projection_record_path_for_ticket(
            successor.p["ticket_id"]
        )
        data = json.loads(path.read_text())
        data["projection_SHA256"] = "0" * 64
        path.write_text(json.dumps(data))
        return original()

    monkeypatch.setattr(pr, "build_workflow_control_snapshot", changed)
    try:
        result = start(successor, spawn_fn=forbidden)
    except (
        pr.ProductRuntimeError,
        bridge.TicketArchitectBridgeError,
        projection.WorkPacketKanbanProjectionError,
    ):
        return
    assert result["start_status"] == "blocked"


def test_active_conflicting_execution_blocks(successor, monkeypatch):
    p = successor.p
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        task = kb.claim_task(conn, p["kanban_task_id"], claimer="isolated-conflict")
        assert task is not None
        kb._set_worker_pid(conn, task.id, os.getpid())
    monkeypatch.setattr(kb, "_pid_alive", lambda _: True)
    result = start(successor, spawn_fn=forbidden)
    assert result["start_status"] == "blocked"
