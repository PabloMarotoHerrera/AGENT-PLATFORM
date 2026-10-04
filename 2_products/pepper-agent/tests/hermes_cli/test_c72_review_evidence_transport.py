"""Canonical transcript evidence reaches the unchanged review gate, read-only."""

from contextlib import closing
from copy import deepcopy
import hashlib
import json
import sqlite3

import pytest

from hermes_cli.agent_platform import execution_evidence as ev
from hermes_cli.agent_platform import manual_validation as mv
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.work_packet import validation_command_runner as runner
from tools import workpacket_validation_tool as vt
from tests.hermes_cli import test_c68_execution_evidence as c68
from tests.hermes_cli import test_c71_worker_witness as c71
from tests.hermes_cli.test_c68_execution_evidence import (
    flow as flow,
    evidence as evidence,
    observed as observed,
    projection_home as projection_home,
)

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


def complete(flow, evidence):
    source = json.loads(
        pr.governed_source_authority_record_path_for_run(
            evidence.projected, flow.run_id
        ).read_text()
    )
    with closing(ev.kb.connect(board=evidence.projected["kanban_board_slug"])) as conn:
        conn.execute(
            "UPDATE tasks SET status='done',current_run_id=NULL WHERE id=?",
            (evidence.projected["kanban_task_id"],),
        )
        conn.execute(
            "UPDATE task_runs SET status='done',outcome='completed',metadata=? WHERE id=?",
            (
                json.dumps({
                    "durable_source_authority_reference": pr._governed_source_authority_reference(
                        source
                    ),
                    "validation_results": [
                        {"validation_id": "V1", "status": "passed", "exit_code": 0}
                    ],
                }),
                flow.run_id,
            ),
        )
        conn.commit()
    completion = pr._kanban_completion_result_source(evidence.projected, read_only=True)
    assert completion["blocker_code"] is None, completion
    assert completion["durable_source_authority_SHA256"]
    return completion


@pytest.fixture
def ready(flow, evidence, observed, monkeypatch):
    c68.test_persisted_test_summary_without_execution(
        flow, evidence, observed, "passed"
    )
    c71.arguments(evidence, {})
    completion = complete(flow, evidence)
    contract = pr._acceptance_contract_for_review_projection(evidence.projected)
    # Machine-only fixture by default; mixed tests add their own persisted V2-V6.
    contract["work_packet_validation_steps"] = [
        step
        for step in contract["work_packet_validation_steps"]
        if step.get("kind") != "manual"
    ]

    def forbidden(*args, **kwargs):
        pytest.fail("gate evaluation must not execute validation or prepare review")

    monkeypatch.setattr(runner, "_launch_and_capture", forbidden)
    monkeypatch.setattr(pr, "prepare_current_ticket_review", forbidden)
    return completion, contract


def records(ready):
    return [
        r
        for r in vt.review_prepare_validation_result_records(ready[0])
        if r.get("review_prepare_validation_evidence_mode")
        == "canonical_worker_evidence"
    ]


def matches(ready):
    return pr._review_completion_validation_contract_satisfied(*ready)


def snapshot(home):
    return {
        str(p): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
        for p in home.rglob("*")
        if p.is_file()
    }


def test_passed_transport_matches_existing_predicate_read_only(flow, ready, evidence):
    before = snapshot(flow.home)
    original = deepcopy(ready)
    (result,) = records(ready)
    (requirement,) = vt.review_prepare_validation_requirements(ready[1])
    assert vt.review_prepare_validation_result_matches_requirement(
        result, requirement, acceptance_contract=ready[1]
    )
    assert matches(ready)
    assert result["success"] is True
    assert result["outcome"] == "TESTS_PASSED"
    provenance = result["provenance"]
    assert provenance["source_message_id"] == evidence.executed
    assert provenance["worker_session_id"] == "synthetic-c66-worker"
    assert (
        provenance["validation_result_SHA256"]
        == c68.call(flow)["validation"]["results"][0]["validation_result_SHA256"]
    )
    assert provenance["projection_SHA256"] == evidence.projected["projection_SHA256"]
    assert ready == original
    assert snapshot(flow.home) == before
    assert (
        pr._load_current_ticket_review_prepare_record_raw(
            projection_record=evidence.projected
        )
        is None
    )


def test_abbreviated_record_alone_is_not_evidence(ready, evidence):
    c71.edit(evidence, "DELETE FROM messages WHERE id=?", (evidence.executed,))
    assert records(ready) == []
    assert not matches(ready)


@pytest.mark.parametrize("mode", ["failed", "pretest"])
def test_real_failures_do_not_satisfy(flow, evidence, observed, ready, mode):
    if mode == "failed":
        c68.test_persisted_test_summary_without_execution(
            flow, evidence, observed, mode
        )
    else:
        c68.rewrite(
            evidence, lambda r: (r.clear(), r.update(deepcopy(evidence.result)))
        )
    (result,) = records(ready)
    assert result["success"] is False
    assert result["outcome"] == (
        "TESTS_FAILED" if mode == "failed" else "PRE_TEST_COMMAND_FAILURE"
    )
    assert not matches(ready)


@pytest.mark.parametrize(
    "field",
    [
        "command_authority_SHA256",
        "command_argv",
        "source_command",
        "working_directory",
        "package_relative_path",
        "execution_plan_SHA256",
        "work_packet_validation_step_SHA256",
    ],
)
def test_tampered_command_fails_closed(ready, evidence, field):
    c68.rewrite(evidence, lambda r: r["command"].__setitem__(field, "wrong"))
    assert not records(ready)
    assert not matches(ready)


@pytest.mark.parametrize(
    "field,value",
    [
        ("process_started", False),
        ("exit_code", 1),
        ("disposition", "failed"),
        ("success", False),
        ("failure_reason", "timeout"),
    ],
)
def test_inconsistent_or_unsuccessful_result_cannot_pass(ready, evidence, field, value):
    def change(r):
        for item in (r, r["subcommand_results"][0]):
            item[field] = value

    c68.rewrite(evidence, change)
    assert not matches(ready)


@pytest.mark.parametrize("mode", ["tampered", "truncated"])
def test_stream_integrity_remains_required(flow, ready, evidence, observed, mode):
    c68.test_stream_integrity_and_completeness(flow, evidence, observed, mode)
    assert not records(ready)
    assert not matches(ready)


@pytest.mark.parametrize(
    "field", ["validation_result_SHA256", "success", "command", "provenance"]
)
def test_transport_digest_covers_payload(ready, field):
    (result,) = records(ready)
    result[field] = "tampered"
    (requirement,) = vt.review_prepare_validation_requirements(ready[1])
    assert not vt.review_prepare_validation_result_matches_requirement(
        result, requirement, acceptance_contract=ready[1]
    )


def test_post_terminal_only_cannot_pass(ready, evidence):
    c71.edit(
        evidence,
        "UPDATE messages SET timestamp=? WHERE id=?",
        (evidence.run.ended_at + 3, evidence.executed),
    )
    assert not records(ready)
    assert not matches(ready)


def test_ambiguous_session_cannot_pass(flow, ready, evidence, observed):
    c68.test_ambiguous_sessions(flow, evidence, observed)
    assert not records(ready)
    assert not matches(ready)


@pytest.mark.parametrize(
    "field,value",
    [
        ("current_run_id", 999),
        ("workspace_path", "/wrong"),
        ("TicketSpec_SHA256", "wrong"),
        ("WorkPacket_ID", "wrong"),
        ("WorkPacket_SHA256", "wrong"),
    ],
)
def test_wrong_worker_binding_cannot_pass(flow, ready, evidence, field, value):
    c71.test_result_identity_required(flow, evidence, None, field, value)
    assert not records(ready)
    assert not matches(ready)


@pytest.mark.parametrize(
    "field",
    [
        "run_id",
        "kanban_task_id",
        "kanban_task_workspace_path",
        "durable_source_authority_SHA256",
    ],
)
def test_completion_identity_cannot_borrow_evidence(ready, field):
    ready[0][field] = "different"
    assert not records(ready)
    assert not matches(ready)


def test_wrong_projection_fails_closed(ready, evidence, flow):
    with closing(ev.kb.connect(board=evidence.projected["kanban_board_slug"])) as conn:
        metadata = dict(ready[0]["run_metadata"], projection_SHA256="wrong")
        conn.execute(
            "UPDATE task_runs SET metadata=? WHERE id=?",
            (json.dumps(metadata), flow.run_id),
        )
        conn.commit()
    completion = pr._kanban_completion_result_source(evidence.projected, read_only=True)
    assert not matches((completion, ready[1]))


def test_conflicting_in_run_results_are_not_selected(ready, evidence):
    with closing(sqlite3.connect(evidence.database)) as conn:
        conn.row_factory = sqlite3.Row
        invocation = dict(
            conn.execute(
                "SELECT * FROM messages WHERE role='assistant' ORDER BY id DESC LIMIT 1"
            ).fetchone()
        )
        result = dict(
            conn.execute(
                "SELECT * FROM messages WHERE id=?", (evidence.executed,)
            ).fetchone()
        )
        calls = json.loads(invocation["tool_calls"])
        calls[0]["id"] = "conflicting-call"
        invocation["tool_calls"] = json.dumps(calls)
        result["tool_call_id"] = "conflicting-call"
        result["content"] = json.dumps(evidence.result)
        for row in (invocation, result):
            row.pop("id")
            conn.execute(
                "INSERT INTO messages ("
                + ",".join(row)
                + ") VALUES ("
                + ",".join("?" for _ in row)
                + ")",
                tuple(row.values()),
            )
        conn.commit()
    assert not records(ready)
    assert not matches(ready)


def test_attempt_two_transport(flow, ready, evidence):
    old = str(evidence.workspace)
    c71.test_attempt_two_workspace_binds_result_and_session(flow, evidence, None)
    workspace = evidence.workspace.with_name(evidence.workspace.name + "-attempt-2")
    # Rematerialized attempt-local command discovery and result plan identities.
    with closing(sqlite3.connect(evidence.database)) as conn:
        for row_id in (evidence.listed, evidence.executed):
            raw = conn.execute(
                "SELECT content FROM messages WHERE id=?", (row_id,)
            ).fetchone()[0]
            payload = json.loads(raw.replace(old, str(workspace)))
            command = (
                payload["commands"][0]
                if row_id == evidence.listed
                else payload["command"]
            )
            child = json.loads(
                conn
                .execute(
                    "SELECT content FROM messages WHERE id=?", (evidence.executed,)
                )
                .fetchone()[0]
                .replace(old, str(workspace))
            )["subcommand_results"][0]
            plan_sha = vt._digest_payload(
                vt._WORKPACKET_VALIDATION_EXECUTION_PLAN_DIGEST_ALGORITHM,
                {
                    "command_id": command["command_id"],
                    "validation_id": command["validation_id"],
                    "source_command": command["source_command"],
                    "working_directory": command["working_directory"],
                    "expected_exit_codes": command["expected_exit_codes"],
                    "execution_plan": [child["subcommand"]],
                },
            )
            command["execution_plan_SHA256"] = plan_sha
            if row_id == evidence.executed:
                payload["execution_plan_SHA256"] = plan_sha
                payload["subcommand_results"][0]["command"] = deepcopy(command)
            conn.execute(
                "UPDATE messages SET content=? WHERE id=?",
                (json.dumps(payload), row_id),
            )
        conn.commit()
    completion = complete(flow, evidence)
    assert matches((completion, ready[1]))
    (result,) = records((completion, ready[1]))
    assert result["provenance"]["workspace"].endswith("-attempt-2")
    assert result["provenance"]["run_id"] == flow.run_id


@pytest.mark.parametrize("last_status", ["passed", "failed", "pending"])
def test_mixed_contract_preserves_human_evidence_and_review_boundary(
    flow, ready, last_status
):
    completion, original_contract = ready
    contract = deepcopy(original_contract)
    for number in range(2, 7):
        contract["work_packet_validation_steps"].append({
            "validation_id": f"V{number}",
            "kind": "manual",
            "required": True,
            "command": None,
            "command_execution_authorized": False,
            "description": f"Human check {number}",
        })
    for item in mv.required_items(contract):
        status = last_status if item["validation_id"] == "V6" else "passed"
        if status == "pending":
            continue
        identity = mv.binding(contract, completion, item)
        mv.persist(
            identity,
            status=status,
            human_attestation_text=mv.attestation_text(identity, status),
            evidence="Isolated human evidence fixture",
            actor="fixture-human",
        )
    before = snapshot(flow.home)
    assert matches((completion, contract)) is (last_status == "passed")
    assert snapshot(flow.home) == before


def test_legacy_valid_schema_is_preserved(ready):
    (result,) = records(ready)
    result.pop("review_prepare_validation_evidence_mode")
    result.pop("provenance")
    result.pop("validation_result_SHA256")
    legacy = {"validation_results": [result]}
    assert vt.review_prepare_validation_contract_satisfied(legacy, ready[1])


def test_supplied_canonical_transport_is_not_trusted(ready):
    (result,) = records(ready)
    forged = {"validation_results": [result]}
    assert not vt.review_prepare_validation_contract_satisfied(forged, ready[1])


@pytest.mark.parametrize(
    "mode", ["digest", "incomplete", "missing_worker", "source_reference"]
)
def test_incomplete_or_tampered_persisted_authority(ready, evidence, mode):
    if mode == "digest":
        c68.rewrite(evidence, lambda r: r.update(validation_result_SHA256="0" * 64))
    elif mode == "incomplete":
        c68.rewrite(evidence, lambda r: r["subcommand_results"][0].pop("success"))
    elif mode == "missing_worker":
        c71.edit(evidence, "DELETE FROM messages")
    else:
        with closing(
            ev.kb.connect(board=evidence.projected["kanban_board_slug"])
        ) as conn:
            metadata = deepcopy(ready[0]["run_metadata"])
            metadata["durable_source_authority_reference"]["authority_SHA256"] = "wrong"
            conn.execute(
                "UPDATE task_runs SET metadata=? WHERE id=?",
                (json.dumps(metadata), ready[0]["run_id"]),
            )
            conn.commit()
        ready = (
            pr._kanban_completion_result_source(evidence.projected, read_only=True),
            ready[1],
        )
    assert not records(ready)
    assert not matches(ready)
