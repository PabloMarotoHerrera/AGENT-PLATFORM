"""Worker evidence uses persisted isolated sessions; inspection never executes V1."""

import hashlib
import json
import sqlite3
from contextlib import closing

import pytest

from hermes_cli.agent_platform import execution_evidence as ev
from tests.hermes_cli import test_c68_execution_evidence as c68
from tests.hermes_cli.test_c68_execution_evidence import (
    flow as flow,
    evidence as evidence,
    observed as observed,
    projection_home as projection_home,
)

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


def edit(evidence, sql, params=()):
    with closing(sqlite3.connect(evidence.database)) as conn:
        conn.execute(sql, params)
        conn.commit()


def arguments(evidence, value):
    with closing(sqlite3.connect(evidence.database)) as conn:
        row = conn.execute(
            "SELECT id,tool_calls FROM messages WHERE role='assistant' ORDER BY id LIMIT 1"
        ).fetchone()
        calls = json.loads(row[1])
        calls[0]["function"]["arguments"] = json.dumps(value)
        conn.execute(
            "UPDATE messages SET tool_calls=? WHERE id=?", (json.dumps(calls), row[0])
        )
        conn.commit()


@pytest.fixture
def local(evidence, observed):
    arguments(evidence, {})


@pytest.mark.parametrize("explicit", [True, False])
def test_accepted_forms_without_any_writes(flow, evidence, observed, explicit):
    if not explicit:
        arguments(evidence, {})

    def snapshot():
        return {
            str(p): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in flow.home.rglob("*")
            if p.is_file()
        }

    before = snapshot()
    result = c68.call(flow)
    assert result["worker"]["available"]
    assert result["worker"]["task_witness_message_id"] == evidence.show
    assert result["validation"]["results"][0]["outcome"] == "PRE_TEST_COMMAND_FAILURE"
    assert snapshot() == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", "wrong"),
        ("current_run_id", 999),
        ("current_run_id", None),
        ("current_run_id", True),
        ("workspace_path", "/wrong"),
        ("TicketSpec_SHA256", "wrong"),
        ("WorkPacket_ID", "wrong"),
        ("WorkPacket_SHA256", "wrong"),
        ("body", None),
    ],
)
def test_result_identity_required(flow, evidence, local, field, value):
    def change(payload):
        if field in {"TicketSpec_SHA256", "WorkPacket_ID", "WorkPacket_SHA256"}:
            body = json.loads(payload["task"]["body"])
            body[field] = value
            payload["task"]["body"] = json.dumps(body)
        else:
            payload["task"][field] = value

    c68.rewrite(evidence, change, message_id=evidence.show)
    assert c68.call(flow)["worker"]["available"] is False


@pytest.mark.parametrize(
    "value",
    [
        {"task_id": "wrong"},
        {"task_id": None},
        {"board": "other"},
        {"path": "/etc/passwd"},
        [],
        None,
    ],
)
def test_arbitrary_arguments_rejected(flow, evidence, observed, value):
    arguments(evidence, value)
    assert c68.call(flow)["worker"]["available"] is False


@pytest.mark.parametrize(
    "mode", ["missing_task", "wrong_tool", "wrong_call", "late", "reversed"]
)
def test_pairing_and_terminal_window(flow, evidence, local, mode):
    if mode == "missing_task":
        c68.rewrite(evidence, lambda x: x.pop("task"), message_id=evidence.show)
    elif mode == "wrong_tool":
        edit(
            evidence,
            "UPDATE messages SET tool_name='different' WHERE id=?",
            (evidence.show,),
        )
    elif mode == "wrong_call":
        edit(
            evidence,
            "UPDATE messages SET tool_call_id='unpaired' WHERE id=?",
            (evidence.show,),
        )
    elif mode == "late":
        edit(
            evidence,
            "UPDATE messages SET timestamp=? WHERE id=?",
            (evidence.run.ended_at + 2, evidence.show),
        )
    else:
        edit(
            evidence,
            "UPDATE messages SET timestamp=? WHERE id=?",
            (evidence.run.started_at + 1, evidence.show),
        )
    assert c68.call(flow)["worker"]["available"] is False


@pytest.mark.parametrize(
    "field,value", [("cwd", "/wrong"), ("profile_name", "wrong"), ("started_at", 1)]
)
def test_session_guards(flow, evidence, observed, local, field, value):
    c68.test_wrong_session_binding(flow, evidence, observed, field, value)


def test_ambiguity_remains_closed(flow, evidence, observed, local):
    c68.test_ambiguous_sessions(flow, evidence, observed)


@pytest.mark.parametrize("mode", ["passed", "failed"])
def test_persisted_v1_outcomes(flow, evidence, observed, local, mode):
    c68.test_persisted_test_summary_without_execution(flow, evidence, observed, mode)


@pytest.mark.parametrize("mode", ["tampered", "truncated"])
def test_streams_remain_validated(flow, evidence, observed, local, mode):
    c68.test_stream_integrity_and_completeness(flow, evidence, observed, mode)


@pytest.mark.parametrize(
    "field",
    [
        "command_authority_SHA256",
        "command_argv",
        "working_directory",
        "execution_plan_SHA256",
    ],
)
def test_v1_authority_is_not_weakened(flow, evidence, observed, local, field):
    c68.test_validation_wrong_authority_rejected(flow, evidence, observed, field)


def test_post_terminal_calls_do_not_replace_in_run_result(flow, evidence, local):
    original = c68.call(flow)["validation"]["results"][0]
    with closing(sqlite3.connect(evidence.database)) as conn:
        conn.row_factory = sqlite3.Row
        result = dict(
            conn.execute(
                "SELECT * FROM messages WHERE id=?", (evidence.executed,)
            ).fetchone()
        )
        invocation = dict(
            conn.execute(
                "SELECT * FROM messages WHERE role='assistant' ORDER BY id DESC LIMIT 1"
            ).fetchone()
        )
        calls = json.loads(invocation["tool_calls"])
        calls[0]["id"] = "late-call"
        invocation.update(
            tool_calls=json.dumps(calls), timestamp=evidence.run.ended_at + 3
        )
        result.update(tool_call_id="late-call", timestamp=evidence.run.ended_at + 4)
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
    current = c68.call(flow)["validation"]
    assert current["results"][0] == original
    assert current["excluded_post_terminal_count"] == 1
    # Removing the in-run result cannot promote the later result to authority.
    edit(evidence, "DELETE FROM messages WHERE id=?", (evidence.executed,))
    assert c68.call(flow)["validation"]["available"] is False


def test_direct_session_id_guard(flow, evidence, local):
    conn = ev.kb.connect(board=evidence.projected["kanban_board_slug"])
    metadata = dict(evidence.run.metadata or {})
    metadata["worker_session_id"] = "wrong"
    conn.execute(
        "UPDATE task_runs SET metadata=? WHERE id=?",
        (json.dumps(metadata), flow.run_id),
    )
    conn.commit()
    conn.close()
    assert c68.call(flow)["worker"]["available"] is False


@pytest.mark.parametrize("role", ["assistant", "tool"])
def test_duplicate_pair_identity_is_ambiguous(flow, evidence, local, role):
    with closing(sqlite3.connect(evidence.database)) as conn:
        conn.row_factory = sqlite3.Row
        row = dict(
            conn.execute(
                "SELECT * FROM messages WHERE role=? ORDER BY id LIMIT 1", (role,)
            ).fetchone()
        )
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
    assert c68.call(flow)["worker"]["available"] is False


def test_attempt_two_workspace_binds_result_and_session(flow, evidence, local):
    # Keep the existing terminal row and add a preceding attempt in this isolated
    # history. Inspection binds the terminal row, not a guessed workspace suffix.
    p = evidence.projected
    conn = ev.kb.connect(board=p["kanban_board_slug"])
    conn.execute("UPDATE task_runs SET id=? WHERE id=?", (flow.run_id + 1, flow.run_id))
    conn.execute(
        "INSERT INTO task_runs (id,task_id,profile,status,started_at,ended_at,outcome) VALUES (?,?,?,'done',?,?,'completed')",
        (
            flow.run_id,
            p["kanban_task_id"],
            evidence.run.profile,
            evidence.run.started_at - 10,
            evidence.run.started_at - 1,
        ),
    )
    flow.run_id += 1
    workspace = evidence.workspace.with_name(evidence.workspace.name + "-attempt-2")
    evidence.workspace.rename(workspace)
    task = ev.kb.get_task(conn, p["kanban_task_id"])
    body = json.loads(task.body)
    body.update(
        fresh_execution_attempt_number=2,
        fresh_execution_workspace_path=str(workspace),
        fresh_execution_request_SHA256="fixture",
    )
    conn.execute(
        "UPDATE tasks SET workspace_path=?,body=? WHERE id=?",
        (str(workspace), json.dumps(body), task.id),
    )
    conn.commit()
    conn.close()
    edit(evidence, "UPDATE sessions SET cwd=?", (str(workspace),))

    def update(result):
        result["task"].update(current_run_id=flow.run_id, workspace_path=str(workspace))

    c68.rewrite(evidence, update, message_id=evidence.show)
    c68.source_fixture(p, flow.run_id, workspace)
    result = c68.call(flow, section="worker")
    assert result["worker"]["available"]
    assert result["workspace"] == str(workspace)
