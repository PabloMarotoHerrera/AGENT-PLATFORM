"""Successive recovery authorities retain exact predecessor evidence."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import recovery_authority as authority
from hermes_cli.agent_platform import retry_material_revision as revision
from hermes_cli.agent_platform import validation_contract_failure as defect
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)
from tests.hermes_cli import test_agent_platform_work_packet_compiler as compiler
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c66_invalid_validation_command_revision import (
    persist_evidence,
)


def recover():
    return pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text(
            "P99.4"
        ),
        ticket_id="P99.4",
    )


def current():
    return projection.load_kanban_projection_record(ticket_id="P99.4")


def read():
    return pr.load_current_ticket_recovery_action_record(projection_record=current())


def advance(flow, monkeypatch, *, executable=False):
    revision.request(**flow.args)
    command = (
        compiler.command_authority(
            source_command="npm test -- --runInBand",
            command_argv=("npm", "test", "--", "--runInBand"),
        )
        if executable
        else None
    )
    steps = [
        compiler.validation_step(
            command="npm test -- --runInBand", command_authority=command
        ).model_dump(mode="json"),
        compiler.validation_step("V2", command=None).model_dump(mode="json"),
    ]
    steps[1]["description"] = "Inspect revision " + flow.record["work_packet_SHA256"]
    revised = pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "validation_steps": steps},
        ticket_id="P99.4",
        next_action_id="REVISE_P99_4",
    )
    assert revised["revision_status"] == "awaiting_ticket_approval"
    record = bridge.load_generation_record(ticket_id="P99.4")
    bridge.apply_ticket_approval_decision(
        ticket_id="P99.4", decision="approve", actor="isolated-human"
    )
    projected = projection.project_current_approved_workpacket_to_kanban(
        workflow=pr.build_workflow_control_snapshot()
    )
    run_id = fixtures._force_projected_execution_failure(
        projected=projected, pr=pr, kanban_db=kb, monkeypatch=monkeypatch
    )
    failed = pr.build_workflow_control_snapshot()
    assert failed["workflow_status"] == "execution_failed"
    conn = kb.connect(board=projected["kanban_board_slug"])
    try:
        workspace = Path(kb.get_task(conn, projected["kanban_task_id"]).workspace_path)
    finally:
        conn.close()
    workspace.mkdir(parents=True, exist_ok=True)
    candidate = workspace / "candidate.txt"
    candidate.write_text("next isolated candidate")
    return SimpleNamespace(
        home=flow.home,
        record=record,
        projection=projected,
        run_id=run_id,
        candidate=candidate,
        args={
            **flow.args,
            "failed_run_id": run_id,
            "work_packet_SHA256": record["work_packet_SHA256"],
        },
    )


def test_three_material_revision_recovery_cycles(flow, monkeypatch):
    saved = []
    for generation in range(3):
        record = read()
        raw = pr.recovery_action_record_path_for_ticket("P99.4").read_bytes()
        saved.append((record, raw))
        assert record["latest_failed_run_id"] == flow.run_id
        assert record["work_packet_SHA256"] == flow.record["work_packet_SHA256"]
        assert recover()["idempotent_replay"] is True
        assert pr.recovery_action_record_path_for_ticket("P99.4").read_bytes() == raw
        assert (
            pr.build_workflow_control_snapshot()["workflow_status"] == "retry_pending"
        )
        if generation == 2:
            break
        flow = advance(flow, monkeypatch)
        assert read() is None
        with pytest.raises(pr.ProductRuntimeConflict):
            pr.validate_p18_9_0_recovery_action_record(
                record, projection_record=current()
            )
        result = recover()
        assert result["recovery_action_SHA256"] != record["recovery_action_SHA256"]
        for key in ("second_run_started", "execution_started", "dispatch_performed"):
            assert result[key] is False
        flow.args["recovery_action_SHA256"] = result["recovery_action_SHA256"]
        entries = authority.history(current())
        assert len(entries) == generation + 1
        for old, old_raw in saved:
            entry = next(
                x
                for x in entries
                if x["record"]["recovery_action_SHA256"]
                == old["recovery_action_SHA256"]
            )
            assert entry["record"] == old
            assert entry["record_text"].encode() == old_raw
    assert len({r["recovery_action_SHA256"] for r, _ in saved}) == 3


def test_c66_alternative_after_second_recovery_only(flow, monkeypatch):
    path = pr.recovery_action_record_path_for_ticket("P99.4")
    old = path.read_bytes()
    second = advance(flow, monkeypatch, executable=True)
    persist_evidence(second, monkeypatch, refresh_recovery=False)
    assert path.read_bytes() == old
    assert read() is None
    assert not pr.build_workflow_control_snapshot().get("alternative_actions")
    result = recover()
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["workflow_status"] == "retry_pending"
    alternative = snapshot["alternative_actions"][0]
    assert alternative["reason_code"] == defect.REASON
    assert (
        alternative["request_binding"]["recovery_action_SHA256"]
        == result["recovery_action_SHA256"]
    )
    assert not revision.path_for(second.record).exists()
    requested = revision.request(**{
        **second.args,
        "reason_code": defect.REASON,
        "recovery_action_SHA256": result["recovery_action_SHA256"],
    })
    assert requested["retry_authority_status"] == "suspended_not_consumed"
    assert authority.history(current())[0]["record_text"].encode() == old


@pytest.mark.parametrize(
    "key,value",
    [
        ("ticket_spec_SHA256", "0" * 64),
        ("work_packet_id", "wrong"),
        ("work_packet_SHA256", "0" * 64),
        ("projection_SHA256", "0" * 64),
        ("kanban_task_id", "wrong"),
        ("latest_failed_run_id", 99999),
        ("terminal_run_SHA256", "0" * 64),
        ("kanban_task_workspace_path", "/wrong"),
    ],
)
def test_current_tampering_rejected_even_with_recomputed_digest(flow, key, value):
    record = read()
    record[key] = value
    record["recovery_action_SHA256"] = pr._recovery_action_record_digest(record)
    pr.recovery_action_record_path_for_ticket("P99.4").write_text(json.dumps(record))
    with pytest.raises(pr.ProductRuntimeConflict):
        read()


def test_ambiguous_same_execution_rejected(flow):
    record = read()
    record["created_at"] = "different-authority"
    record["recovery_action_SHA256"] = pr._recovery_action_record_digest(record)
    pr._append_authority_history(
        pr.recovery_action_history_path_for_ticket("P99.4"), record, reason="ambiguous"
    )
    with pytest.raises(pr.ProductRuntimeConflict, match="ambiguous"):
        read()


def test_legacy_recovery_keeps_original_sha_and_bytes(flow, monkeypatch):
    record = read()
    record.pop("terminal_run_SHA256")
    record["recovery_action_SHA256"] = pr._recovery_action_record_digest(record)
    path = pr.recovery_action_record_path_for_ticket("P99.4")
    path.write_text(json.dumps(record, indent=4) + "\n")
    flow.args["recovery_action_SHA256"] = record["recovery_action_SHA256"]
    old = path.read_bytes()
    second = advance(flow, monkeypatch)
    assert read() is None
    recover()
    assert authority.history(current())[0]["record_text"].encode() == old
    assert second.run_id != record["latest_failed_run_id"]


@pytest.mark.parametrize("raw", [False, True])
def test_tampered_consulted_history_rejected(flow, monkeypatch, raw):
    advance(flow, monkeypatch)
    recover()
    path = pr.recovery_action_history_path_for_ticket("P99.4")
    entry = json.loads(path.read_text())
    if raw:
        entry["record_text"] += " "
    else:
        entry["record"]["latest_failed_run_id"] = 99999
    path.write_text(json.dumps(entry) + "\n")
    with pytest.raises(pr.ProductRuntimeConflict):
        read()


def test_replay_cannot_replace_same_execution(flow):
    record = read()
    path = pr.recovery_action_record_path_for_ticket("P99.4")
    before = path.read_bytes()
    record["created_at"] = "different"
    record["recovery_action_SHA256"] = pr._recovery_action_record_digest(record)
    with pytest.raises(pr.ProductRuntimeConflict, match="same failed execution"):
        pr._persist_recovery_action_record(record)
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "text",
    [
        "Inspect P99.4",
        "I authorize recovery of P99.5.",
        "I authorize recovery of P99.4 run 99999.",
    ],
)
def test_missing_or_stale_human_authorization(flow, text):
    before = pr.recovery_action_record_path_for_ticket("P99.4").read_bytes()
    with pytest.raises(pr.ProductRuntimeError):
        pr.recover_current_ticket_execution(
            human_authorization_text=text, ticket_id="P99.4"
        )
    assert pr.recovery_action_record_path_for_ticket("P99.4").read_bytes() == before


@pytest.mark.parametrize("state", ["running", "nonterminal"])
def test_active_or_nonterminal_new_run_cannot_recover(flow, monkeypatch, state):
    second = advance(flow, monkeypatch)
    path = pr.recovery_action_record_path_for_ticket("P99.4")
    before = path.read_bytes()
    conn = kb.connect(board=second.projection["kanban_board_slug"])
    try:
        if state == "running":
            conn.execute(
                "UPDATE tasks SET status='running',worker_pid=? WHERE id=?",
                (12345, second.projection["kanban_task_id"]),
            )
            monkeypatch.setattr(kb, "_pid_alive", lambda pid: True)
        else:
            conn.execute(
                "UPDATE task_runs SET ended_at=NULL WHERE id=?", (second.run_id,)
            )
        conn.commit()
    finally:
        conn.close()
    result = recover()
    assert result.get("recovery_authorization_recorded") is not True
    assert result["execution_started"] is False
    assert path.read_bytes() == before


def test_new_failure_same_projection_needs_new_recovery(flow, monkeypatch):
    old = read()
    conn = kb.connect(board=flow.projection["kanban_board_slug"])
    try:
        assert kb.unblock_task(conn, flow.projection["kanban_task_id"])
    finally:
        conn.close()
    run_id = fixtures._force_projected_execution_failure(
        projected=flow.projection, pr=pr, kanban_db=kb, monkeypatch=monkeypatch
    )
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["workflow_status"] == "execution_failed"
    assert not snapshot.get("alternative_actions")
    with pytest.raises(pr.ProductRuntimeError):
        pr.recover_current_ticket_execution(
            human_authorization_text=f"I authorize recovery of P99.4 run {old['latest_failed_run_id']}.",
            ticket_id="P99.4",
        )
    result = recover()
    assert result["latest_failed_run_id"] == run_id
    assert result["recovery_action_SHA256"] != old["recovery_action_SHA256"]
    assert result["observed_attempt_count"] == 2
    assert result["next_attempt_number"] == 3
    assert result["second_run_started"] is False
    assert authority.history(current())[0]["record"] == old
