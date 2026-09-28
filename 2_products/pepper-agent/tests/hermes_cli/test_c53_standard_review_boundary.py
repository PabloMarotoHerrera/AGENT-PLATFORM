"""C53: preserve explicit review evidence through the real block persistence path."""

import json
import pytest
from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from tools import kanban_tools
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)


@pytest.fixture
def terminal_case(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("HERMES_KANBAN_HOME", str(tmp_path / "home"))
    monkeypatch.delenv("HERMES_KANBAN_TASK", raising=False)
    monkeypatch.setattr(kb, "_new_task_id", lambda: "t_synthetic")
    candidate = fixtures._write_synthetic_terminal_candidate_manifest(
        pr, tmp_path, label="c53"
    )
    with kb.connect(board="default") as conn:
        tid = kb.create_task(
            conn,
            title="Synthetic governed frontend candidate",
            assignee="pepper-implementation-product",
            workspace_kind="scratch",
        )
        kb.recompute_ready(conn)
        task = kb.claim_task(conn, tid, claimer="isolated-c53")
        assert task is not None
        kb.set_workspace_path(conn, tid, str(candidate["workspace"]))
        run_id = task.current_run_id
    projection = fixtures._synthetic_projection("P99.1")
    manifest = json.loads(candidate["manifest_path"].read_text())
    manifest.update({
        k: projection[k]
        for k in (
            "ticket_id",
            "ticket_spec_SHA256",
            "work_packet_id",
            "work_packet_SHA256",
            "projection_SHA256",
        )
    })
    candidate["manifest_path"].write_text(json.dumps(manifest))
    metadata = {
        "review_required": True,
        "implementation_complete": True,
        "validation_passed": True,
        "human_boundary": "human_code_review",
        "Git_mutation": False,
    }
    metadata.update({
        k: projection[k]
        for k in (
            "ticket_id",
            "ticket_spec_SHA256",
            "work_packet_id",
            "work_packet_SHA256",
            "projection_SHA256",
        )
    })
    metadata.update(kanban_task_id=tid, run_id=run_id)
    monkeypatch.setattr(
        pr,
        "load_p18_9_0_execution_start_record",
        lambda projection_record=None: fixtures._synthetic_execution_start_record(
            "P99.1", run_id=run_id
        ),
    )

    def live(_projection):
        with kb.connect(board="default") as conn:
            return kb.get_task(conn, tid), kb.list_runs(conn, tid)

    monkeypatch.setattr(pr, "_p18_9_0_live_kanban_execution", live)
    return candidate, projection, metadata, tid, run_id, live


def test_c53_block_preserves_structured_review_evidence(terminal_case):
    candidate, projection, metadata, tid, run_id, live = terminal_case
    result = json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "board": "default",
            "kind": "needs_input",
            "reason": "Candidate awaits a human decision.",
            "metadata": metadata,
        })
    )
    assert result.get("error") is None, result
    task, runs = live(projection)
    assert task.status == "blocked"
    assert runs[-1].id == run_id

    overlay, blocker = pr._current_ticket_execution_start_overlay(projection)
    assert overlay["workflow_status"] == "execution_completed", (
        overlay["workflow_status"],
        overlay["next_action"]["id"],
    )
    assert runs[-1].metadata == metadata
    assert blocker is None
    assert overlay["workflow_status"] == "execution_completed"
    assert overlay["validation_state"] == "execution_completed_pending_validation"
    assert overlay["review_state"] == "ready_for_review_validation"
    assert overlay["recovery_state"] == "not_required"
    assert overlay["terminal_outcome_class"] == "validated_review_required"
    assert overlay["candidate_changes_available"] is True
    assert overlay["validated_candidate_review_required"] is True
    assert overlay["next_action"]["id"] == "PREPARE_P99_1_REVIEW"


@pytest.mark.parametrize(
    "damage",
    [
        "no_candidate",
        "validation_failed",
        "infrastructure_failed",
        "run_error",
        "active_run",
        "worker_pid",
        "malformed_manifest",
        "out_of_scope",
        "wording_only",
        "git_mutation",
        "wrong_ticket",
        "wrong_workpacket",
        "wrong_projection",
        "wrong_task",
        "wrong_run",
    ],
)
def test_c53_invalid_review_boundary_fails_closed(terminal_case, damage):
    candidate, projection, metadata, tid, run_id, live = terminal_case
    if damage == "validation_failed":
        metadata["validation_passed"] = False
    elif damage == "infrastructure_failed":
        metadata["validation_infrastructure_failure"] = True
    elif damage == "git_mutation":
        metadata["Git_mutation"] = True
    elif damage.startswith("wrong_"):
        key = {
            "wrong_ticket": "ticket_id",
            "wrong_workpacket": "work_packet_SHA256",
            "wrong_projection": "projection_SHA256",
            "wrong_task": "kanban_task_id",
            "wrong_run": "run_id",
        }[damage]
        metadata[key] = (
            999 if key == "run_id" else "e" * 64 if "SHA256" in key else "unrelated"
        )
    elif damage == "wording_only":
        metadata = {}
    if damage == "no_candidate":
        (candidate["workspace"] / candidate["writable_rel"]).write_bytes(
            (candidate["source_root"] / candidate["writable_rel"]).read_bytes()
        )
    elif damage == "malformed_manifest":
        candidate["manifest_path"].write_text("{invalid}")
    elif damage == "out_of_scope":
        manifest = json.loads(candidate["manifest_path"].read_text())
        manifest["writable_allowed_paths"] = ["other/**"]
        candidate["manifest_path"].write_text(json.dumps(manifest))
    result = json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": "needs_input",
            "reason": "review required",
            "metadata": metadata,
        })
    )
    assert result.get("error") is None, result
    with kb.connect(board="default") as conn:
        if damage == "run_error":
            conn.execute(
                "UPDATE task_runs SET error=? WHERE id=?", ("execution failed", run_id)
            )
        elif damage == "active_run":
            conn.execute("UPDATE tasks SET current_run_id=? WHERE id=?", (run_id, tid))
        elif damage == "worker_pid":
            conn.execute("UPDATE tasks SET worker_pid=? WHERE id=?", (123, tid))
        conn.commit()
    task, runs = live(projection)
    assert pr._terminal_run_review_boundary_evidence(task, runs[-1]) is None
    overlay, blocker = pr._current_ticket_execution_start_overlay(projection)
    assert overlay.get("terminal_outcome_class") != "validated_review_required"
    assert overlay["next_action"]["id"] != "PREPARE_P99_1_REVIEW"


@pytest.mark.parametrize("metadata", [None, {}, {"validation_passed": False}])
def test_c53_ordinary_failure_remains_recovery(terminal_case, metadata):
    _, projection, _, tid, _, _ = terminal_case
    json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": "capability",
            "reason": "Execution failed",
            "metadata": metadata,
        })
    )
    overlay, blocker = pr._current_ticket_execution_start_overlay(projection)
    assert overlay["workflow_status"] == "execution_failed"
    assert overlay["next_action"]["id"] == "RECOVER_P99_1_EXECUTION"


@pytest.mark.parametrize(
    "kind", ["needs_input", "capability", "transient", "dependency", None]
)
def test_c53_all_block_routes_preserve_metadata(terminal_case, kind):
    _, projection, _, tid, _, live = terminal_case
    metadata = {"terminal_outcome": "blocked"}
    result = json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": kind,
            "reason": "External decision needed",
            "metadata": metadata,
        })
    )
    assert result.get("error") is None, result
    assert live(projection)[1][-1].metadata == metadata


def test_c53_symlink_candidate_outside_scratch_is_not_reviewable(
    terminal_case, tmp_path
):
    candidate, projection, metadata, tid, _, live = terminal_case
    outside = tmp_path / "outside.ts"
    outside.write_text("out of scope candidate")
    path = candidate["workspace"] / candidate["writable_rel"]
    path.unlink()
    path.symlink_to(outside)
    result = json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": "needs_input",
            "reason": "Candidate awaits review",
            "metadata": metadata,
        })
    )
    assert result.get("error") is None
    task, runs = live(projection)
    assert pr._terminal_run_review_boundary_evidence(task, runs[-1]) is None


@pytest.mark.parametrize(
    "value", [[], "review required", {"validation_passed": float("nan")}]
)
def test_c53_invalid_metadata_does_not_close_active_run(terminal_case, value):
    _, projection, _, tid, run_id, live = terminal_case
    result = json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": "needs_input",
            "reason": "Human boundary",
            "metadata": value,
        })
    )
    assert "error" in result
    task, runs = live(projection)
    assert task.current_run_id == run_id
    assert runs[-1].ended_at is None


def test_c53_manifest_identity_must_match_current_projection(terminal_case):
    candidate, projection, metadata, tid, _, _ = terminal_case
    manifest = json.loads(candidate["manifest_path"].read_text())
    manifest["ticket_spec_SHA256"] = "e" * 64
    candidate["manifest_path"].write_text(json.dumps(manifest))
    metadata["ticket_spec_SHA256"] = manifest["ticket_spec_SHA256"]
    json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": "needs_input",
            "reason": "Human boundary",
            "metadata": metadata,
        })
    )
    overlay, _ = pr._current_ticket_execution_start_overlay(projection)
    assert overlay["workflow_status"] == "execution_failed"


def test_c53_unrestored_out_of_scope_change_blocks_review(terminal_case):
    candidate, projection, metadata, tid, _, live = terminal_case
    manifest = json.loads(candidate["manifest_path"].read_text())
    manifest["materialized_roots"] = [
        candidate["writable_rel"],
        candidate["support_rel"],
    ]
    candidate["manifest_path"].write_text(json.dumps(manifest))
    (candidate["workspace"] / candidate["support_rel"]).write_text(
        "unrestored out-of-scope change"
    )
    json.loads(
        kanban_tools._handle_block({
            "task_id": tid,
            "kind": "needs_input",
            "reason": "Human boundary",
            "metadata": metadata,
        })
    )
    task, runs = live(projection)
    assert pr._terminal_run_review_boundary_evidence(task, runs[-1]) is None


def _bounded_validation_results(count=3):
    return [
        {"validation_id": f"V{i + 1}", "status": "passed", "exit_code": 0,
         "command_SHA256": "a" * 64}
        for i in range(count)
    ]


def _metadata_db_snapshot(conn, tid):
    return (
        tuple(conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()),
        [tuple(row) for row in conn.execute(
            "SELECT * FROM task_runs WHERE task_id=? ORDER BY id", (tid,)
        )],
        [tuple(row) for row in conn.execute(
            "SELECT * FROM task_events WHERE task_id=? ORDER BY id", (tid,)
        )],
    )


@pytest.mark.parametrize("entrypoint", ["tool", "db"])
@pytest.mark.parametrize("value, error", [
    ({"unknown": "evidence"}, "unknown field"),
    ({"validation_results": _bounded_validation_results(16)}, "UTF-8 byte limit"),
    ({"validation_results": [{"status": {"nested": {}}}]}, "container depth"),
    ({"ticket_id": "x" * 129}, "string length"),
    ({"validation_results": _bounded_validation_results(17)}, "collection entry"),
    ({str(i): True for i in range(21)}, "collection entry"),
    ({"validation_passed": float("nan")}, "unsupported JSON value"),
    ({"validation_passed": float("inf")}, "unsupported JSON value"),
    ({"validation_passed": float("-inf")}, "unsupported JSON value"),
    ([], "invalid type"),
    ("review required", "invalid type"),
    ({"validation_results": [{"validation_id": "V1", "status": "passed",
                              "stdout": "secret log"}]}, "unknown field"),
    ({"validation_results": [{"status": "passed"}]}, "missing required"),
    ({"validation_results": ["passed"]}, "invalid type"),
    ({"validation_results": [{"validation_id": "V1", "status": "unknown"}]},
     "unsupported value"),
    ({"validation_results": [{"validation_id": "V1", "status": "passed",
                              "exit_code": True}]}, "invalid type"),
    ({"validation_results": [{"validation_id": "V1", "status": "passed",
                              "exit_code": 2147483648}]}, "outside bounds"),
    ({"review_required": 1}, "invalid type"),
    ({"run_id": True}, "invalid type"),
    ({"run_id": 0}, "outside bounds"),
    ({"run_id": 9223372036854775808}, "outside bounds"),
    ({"ticket_spec_SHA256": "not-a-digest"}, "string length"),
    ({"projection_SHA256": "z" * 64}, "identity format"),
    ({"ticket_id": "raw\ntranscript"}, "identity format"),
    ({"terminal_outcome": "arbitrary source code"}, "unsupported value"),
    ({"validation_results": ()}, "unsupported JSON value"),
    ({"ticket_id": b"binary"}, "unsupported JSON value"),
    ({"review_required": None}, "unsupported JSON value"),
    ({1: True}, "invalid object key"),
])
def test_c53_1_invalid_metadata_is_atomic(terminal_case, entrypoint, value, error):
    _, _, _, tid, run_id, _ = terminal_case
    with kb.connect(board="default") as conn:
        before = _metadata_db_snapshot(conn, tid)
        if entrypoint == "tool":
            result = json.loads(kanban_tools._handle_block({
                "task_id": tid, "kind": "needs_input", "reason": "Human boundary",
                "metadata": value,
            }))
            assert "error" in result
        else:
            with pytest.raises(ValueError, match=error):
                kb.block_task(conn, tid, reason="Human boundary", metadata=value)
        assert _metadata_db_snapshot(conn, tid) == before
        assert kb.get_task(conn, tid).current_run_id == run_id
        assert kb.latest_run(conn, tid).ended_at is None


@pytest.mark.parametrize("entrypoint", ["tool", "db"])
def test_c53_1_valid_results_preserve_review_boundary(terminal_case, entrypoint):
    _, projection, metadata, tid, _, live = terminal_case
    metadata["validation_results"] = _bounded_validation_results()
    if entrypoint == "tool":
        result = json.loads(kanban_tools._handle_block({
            "task_id": tid, "kind": "needs_input", "reason": "Human boundary",
            "metadata": metadata,
        }))
        assert "error" not in result
    else:
        with kb.connect(board="default") as conn:
            assert kb.block_task(conn, tid, reason="Human boundary",
                                 kind="needs_input", metadata=metadata)
    task, runs = live(projection)
    assert task.current_run_id is None
    assert runs[-1].ended_at is not None
    assert runs[-1].metadata == metadata
    overlay, blocker = pr._current_ticket_execution_start_overlay(projection)
    assert blocker is None
    assert overlay["workflow_status"] == "execution_completed"
    assert overlay["validation_state"] == "execution_completed_pending_validation"
    assert overlay["review_state"] == "ready_for_review_validation"
    assert overlay["recovery_state"] == "not_required"
    assert overlay["terminal_outcome_class"] == "validated_review_required"
    assert overlay["next_action"]["id"] == "PREPARE_P99_1_REVIEW"


def test_c53_1_redaction_cannot_make_unknown_metadata_valid(terminal_case, monkeypatch):
    _, _, _, tid, _, _ = terminal_case
    # Even a redactor that strips the entire metadata cannot bypass validation.
    monkeypatch.setattr(kanban_tools, "redact_sensitive_text", lambda *a, **k: "{}")
    with kb.connect(board="default") as conn:
        before = _metadata_db_snapshot(conn, tid)
        result = json.loads(kanban_tools._handle_block({
            "task_id": tid, "reason": "Human boundary", "kind": "needs_input",
            "metadata": {"api_key": "sk-" + "x" * 48},
        }))
        assert "error" in result
        assert "sk-" not in json.dumps(result)
        assert _metadata_db_snapshot(conn, tid) == before
        assert kb.latest_run(conn, tid).ended_at is None


@pytest.mark.parametrize("kind", ["needs_input", "dependency", "transient"])
def test_c53_1_metadata_and_transition_rollback_together(terminal_case, monkeypatch, kind):
    _, _, metadata, tid, _, _ = terminal_case
    original = kb._end_run

    def fail_after_run_update(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError("synthetic transaction failure")

    monkeypatch.setattr(kb, "_end_run", fail_after_run_update)
    with kb.connect(board="default") as conn:
        if kind == "transient":
            conn.execute("UPDATE tasks SET block_kind=?, block_recurrences=? WHERE id=?",
                         (kind, kb.BLOCK_RECURRENCE_LIMIT, tid))
            conn.commit()
        before = _metadata_db_snapshot(conn, tid)
        with pytest.raises(RuntimeError, match="synthetic transaction failure"):
            kb.block_task(conn, tid, kind=kind, reason="Human boundary",
                          metadata=metadata)
        assert _metadata_db_snapshot(conn, tid) == before
        assert kb.latest_run(conn, tid).ended_at is None


def test_c53_1_omitted_metadata_remains_compatible(terminal_case):
    _, projection, _, tid, _, live = terminal_case
    result = json.loads(kanban_tools._handle_block({
        "task_id": tid, "kind": "needs_input", "reason": "Human boundary",
    }))
    assert "error" not in result
    task, runs = live(projection)
    assert task.status == "blocked"
    assert task.current_run_id is None
    assert runs[-1].ended_at is not None
    assert runs[-1].metadata is None


def test_c53_1_public_schema_and_validator_agree(terminal_case):
    import jsonschema

    _, _, metadata, _, _, _ = terminal_case
    schema = kanban_tools.KANBAN_BLOCK_SCHEMA["parameters"]["properties"]["metadata"]
    metadata["validation_results"] = _bounded_validation_results()
    jsonschema.validate(metadata, schema)
    assert kb.validate_block_terminal_metadata(metadata) == metadata
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"stdout": "not evidence"}, schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"validation_results": [{"validation_id": "V1",
                                                     "status": "passed",
                                                     "stdout": "not evidence"}]}, schema)


@pytest.mark.parametrize("entrypoint", ["tool", "db"])
def test_c53_1_rejected_ready_task_has_no_synthetic_run(terminal_case, monkeypatch, entrypoint):
    monkeypatch.setattr(kb, "_new_task_id", lambda: "t_ready")
    with kb.connect(board="default") as conn:
        tid = kb.create_task(conn, title="Ready task", workspace_kind="scratch")
        kb.recompute_ready(conn)
        assert kb.get_task(conn, tid).status == "ready"
        before = _metadata_db_snapshot(conn, tid)
        if entrypoint == "tool":
            result = json.loads(kanban_tools._handle_block({
                "task_id": tid, "kind": "needs_input", "reason": "Human boundary",
                "metadata": {"unknown": True},
            }))
            assert "error" in result
        else:
            with pytest.raises(ValueError, match="unknown field"):
                kb.block_task(conn, tid, reason="Human boundary", metadata={"unknown": True})
        assert _metadata_db_snapshot(conn, tid) == before
        assert kb.get_task(conn, tid).current_run_id is None
        assert kb.list_runs(conn, tid) == []


@pytest.mark.parametrize("kind, status", [
    ("needs_input", "blocked"), ("dependency", "todo"), ("transient", "triage"),
])
def test_c53_1_ready_synthetic_run_preserves_valid_metadata(terminal_case, monkeypatch, kind, status):
    monkeypatch.setattr(kb, "_new_task_id", lambda: "t_ready")
    metadata = {"terminal_outcome": "blocked", "validation_results": _bounded_validation_results()}
    with kb.connect(board="default") as conn:
        tid = kb.create_task(conn, title="Ready task", workspace_kind="scratch")
        kb.recompute_ready(conn)
        if kind == "transient":
            conn.execute("UPDATE tasks SET block_kind=?, block_recurrences=? WHERE id=?",
                         (kind, kb.BLOCK_RECURRENCE_LIMIT, tid))
            conn.commit()
        assert kb.block_task(conn, tid, reason="Human boundary", kind=kind, metadata=metadata)
        assert kb.get_task(conn, tid).status == status
        runs = kb.list_runs(conn, tid)
        assert len(runs) == 1
        assert runs[0].ended_at is not None
        assert runs[0].metadata == metadata
