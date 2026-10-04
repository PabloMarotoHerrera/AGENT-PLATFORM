"""C68 evidence inspection uses persisted fixtures and never executes a command."""

import hashlib
import json
from pathlib import Path
import shutil
import sqlite3

import pytest
from hermes_cli.agent_platform import execution_evidence as inspect
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.work_packet.validation_command_runner import (
    ValidationCommandCapturedStream,
)
from tools import pepper_workflow_tools as tools
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c66_invalid_validation_command_revision import (
    evidence as evidence,
    rewrite,
    stream,
)
from tests.hermes_cli.test_c67_successive_recovery_cycles import advance

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


def source_fixture(p, run_id, workspace):
    path = pr.governed_source_authority_record_path_for_run(p, run_id)
    root = path.parent / "src"
    root.mkdir(parents=True)
    shutil.copytree(workspace, root, dirs_exist_ok=True)
    snapshot = pr._build_governed_source_snapshot_manifest(root)
    manifest_path = path.parent / "manifest.json"
    manifest_path.write_text(json.dumps(snapshot))
    materialization = {
        "policy_id": pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_POLICY_ID,
        **{
            k: p[k]
            for k in [
                "ticket_id",
                "work_packet_id",
                "work_packet_SHA256",
                "ticket_spec_SHA256",
                "projection_SHA256",
            ]
        },
        "source_materialized": True,
        "workspace_root": str(workspace),
        "manifest_path": str(
            workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
        ),
        "source_root": str(root),
        "writable_allowed_paths": ["2_products/pepper-agent/web/src/**"],
        "forbidden_paths": ["**/.env"],
        "product_diff_excluded_roots": [],
    }
    record = {
        "policy_id": pr.PEPPER_GOVERNED_SOURCE_AUTHORITY_POLICY_ID,
        **{
            k: p[k]
            for k in [
                "project_id",
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
                "projection_SHA256",
                "kanban_board_slug",
                "kanban_task_id",
            ]
        },
        "run_id": run_id,
        "authority_path": str(path),
        "source_authority_kind": "git_clean_head_tree",
        "git_source_authority": {
            "clean_source_validated": True,
            "git_HEAD": "fixture-head",
            "git_tree_SHA256": "fixture-tree",
        },
        "materialization_manifest": materialization,
        "materialization_manifest_SHA256": pr._digest_payload(
            pr.PEPPER_GOVERNED_SOURCE_MATERIALIZATION_MANIFEST_DIGEST_ALGORITHM,
            materialization,
        ),
        "snapshot_root": str(root),
        "snapshot_manifest_path": str(manifest_path),
        "snapshot_manifest_SHA256": hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest(),
        "snapshot_manifest": snapshot,
        "snapshot_SHA256": snapshot["snapshot_SHA256"],
        "snapshot_file_count": snapshot["file_count"],
        "snapshot_total_bytes": snapshot["total_bytes"],
    }
    record["governed_source_authority_SHA256"] = (
        pr._governed_source_authority_record_digest(record)
    )
    path.write_text(json.dumps(record))
    materialization = {
        **materialization,
        "durable_source_authority_SHA256": record["governed_source_authority_SHA256"],
        "durable_source_authority_reference": pr._governed_source_authority_reference(
            record
        ),
    }
    mp = workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    mp.parent.mkdir(exist_ok=True)
    mp.write_text(json.dumps(materialization))
    return record


@pytest.fixture
def observed(flow, evidence, monkeypatch):
    f = evidence.workspace / "2_products/pepper-agent/web/src/example.ts"
    f.parent.mkdir(parents=True)
    f.write_text("unchanged governed content")
    record = source_fixture(evidence.projected, flow.run_id, evidence.workspace)
    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda *a, **kw: pytest.fail("inspection must not build/reconcile workflow"),
    )
    return record


def call(flow, **kwargs):
    return inspect.inspect(
        ticket_id=flow.record["ticket_id"], run_id=flow.run_id, **kwargs
    )


def test_genuine_zero_candidate_and_pretest_evidence(flow, evidence, observed):
    r = call(flow)
    assert r["candidate"]["zero_change_status"] == "PROVEN"
    assert r["candidate"]["candidate_file_count"] == 1
    assert r["candidate"]["changed_path_count"] == 0
    assert r["candidate"]["source_candidate_equal"] is True
    assert r["worker"]["available"] is True
    assert r["validation"]["results"][0]["outcome"] == "PRE_TEST_COMMAND_FAILURE"
    assert r["human_attestation_performed"] is False


@pytest.mark.parametrize("change", ["modified", "added", "deleted"])
def test_candidate_changes_exact_hashes(flow, evidence, observed, change):
    p = evidence.workspace / "2_products/pepper-agent/web/src/example.ts"
    if change == "modified":
        p.write_text("modified")
    elif change == "deleted":
        p.unlink()
    else:
        (p.parent / "added.ts").write_text("added")
    r = call(flow, section="candidate")["candidate"]
    assert r["zero_change_status"] == "CONTRADICTED"
    assert r["changed_path_count"] == 1
    assert r["changed_paths"][0]["change"] == change
    assert r["source_candidate_equal"] is False


@pytest.mark.parametrize("which", ["workspace", "source"])
def test_missing_candidate_or_source_is_unavailable(flow, evidence, observed, which):
    if which == "workspace":
        shutil.rmtree(evidence.workspace)
    else:
        Path(observed["snapshot_manifest_path"]).unlink()
    r = call(flow)["candidate"]
    assert r["zero_change_status"] == "UNAVAILABLE"
    assert r["available"] is False


@pytest.mark.parametrize("mode", ["passed", "failed"])
def test_persisted_test_summary_without_execution(flow, evidence, observed, mode):
    def change(r):
        success = mode == "passed"
        child = r["subcommand_results"][0]
        for item in (r, child):
            item.update(
                success=success,
                disposition=mode,
                failure_reason="none" if success else "nonzero_exit",
                exit_code=0 if success else 1,
            )
        r["all_subcommands_passed"] = success
        child["stdout"] = stream(
            "RUN v4.1.9 /fixture\n Test Files  "
            + ("2 passed (2)" if success else "1 failed | 1 passed (2)")
            + "\n Tests  "
            + ("4 passed (4)" if success else "1 failed | 2 passed | 1 skipped (4)"),
            "stdout",
        )
        child["stderr"] = stream("", "stderr")

    rewrite(evidence, change)
    r = call(flow, section="validation")["validation"]
    assert r["available"] is True
    r = r["results"][0]
    assert r["outcome"] == ("TESTS_PASSED" if mode == "passed" else "TESTS_FAILED")
    assert r["test_evidence"]["tests_total"] == 4
    assert r["test_evidence"]["tests_executed"] is True
    assert r["authority_match"] is True


@pytest.mark.parametrize(
    "field",
    [
        "command_authority_SHA256",
        "command_argv",
        "working_directory",
        "execution_plan_SHA256",
    ],
)
def test_validation_wrong_authority_rejected(flow, evidence, observed, field):
    rewrite(evidence, lambda r: r["command"].__setitem__(field, "wrong"))
    assert call(flow)["validation"]["available"] is False


@pytest.mark.parametrize("mode", ["tampered", "truncated"])
def test_stream_integrity_and_completeness(flow, evidence, observed, mode):
    def change(r):
        child = r["subcommand_results"][0]
        if mode == "tampered":
            child["stderr"]["stream_SHA256"] = "0" * 64
        else:
            child["stderr"] = (
                __import__(
                    "hermes_cli.agent_platform.work_packet.validation_command_runner",
                    fromlist=["_captured_stream"],
                )
                ._captured_stream("stderr", b"x" * 10000, 10)
                .model_dump(mode="json")
            )

    rewrite(evidence, change)
    r = call(flow)["validation"]
    if mode == "tampered":
        assert r["available"] is False
    else:
        assert r["results"][0]["outcome"] == "UNDETERMINED"


@pytest.mark.parametrize(
    "field,value", [("cwd", "/wrong"), ("profile_name", "wrong"), ("started_at", 1)]
)
def test_wrong_session_binding(flow, evidence, observed, field, value):
    c = sqlite3.connect(evidence.database)
    c.execute(f"UPDATE sessions SET {field}=?", (value,))
    c.commit()
    c.close()
    assert call(flow)["worker"]["available"] is False


def test_ambiguous_sessions(flow, evidence, observed):
    c = sqlite3.connect(evidence.database)
    c.row_factory = sqlite3.Row
    session = dict(c.execute("SELECT * FROM sessions").fetchone())
    sid = session["id"]
    session["id"] = "another"
    c.execute(
        "INSERT INTO sessions ("
        + ",".join(session)
        + ") VALUES ("
        + ",".join("?" for _ in session)
        + ")",
        tuple(session.values()),
    )
    for row in c.execute(
        "SELECT * FROM messages WHERE session_id=?", (sid,)
    ).fetchall():
        row = dict(row)
        row.pop("id")
        row["session_id"] = "another"
        c.execute(
            "INSERT INTO messages ("
            + ",".join(row)
            + ") VALUES ("
            + ",".join("?" for _ in row)
            + ")",
            tuple(row.values()),
        )
    c.commit()
    c.close()
    assert call(flow)["worker"]["available"] is False


def test_candidate_symlink_escape(flow, evidence, observed, tmp_path):
    outside = tmp_path / "private"
    outside.write_text("private")
    (evidence.workspace / "2_products/pepper-agent/web/src/escape.ts").symlink_to(
        outside
    )
    assert call(flow)["candidate"]["available"] is False


def test_public_tool_rejects_arbitrary_paths(flow, evidence, observed):
    r = json.loads(
        tools._inspect_current_ticket_review_candidate({
            "operation": "execution_evidence",
            "ticket_id": "P99.4",
            "reviewed_run_id": flow.run_id,
            "candidate_path": "/etc/passwd",
        })
    )
    assert r["success"] is False
    r = json.loads(
        tools._inspect_current_ticket_review_candidate({
            "operation": "execution_evidence",
            "ticket_id": "P99.4",
            "reviewed_run_id": flow.run_id,
            "evidence_section": "candidate",
        })
    )
    assert r["candidate"]["zero_change_status"] == "PROVEN"


def test_no_state_mutation(flow, evidence, observed):
    def state():
        return {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in flow.home.rglob("*")
            if p.is_file() and not p.name.endswith("-shm")
        }

    before = state()
    call(flow)
    assert state() == before


@pytest.mark.parametrize(
    "text",
    [
        "RUN v4.1.9\nTest Files 1 passed (2)\nTests 2 passed (2)",
        "RUN v4.1.9\nTest Files 1 passed (1)\nTests 2 passed (2)\nTests 2 passed (2)",
        "nonstandard output",
    ],
)
def test_parser_does_not_guess_counts(flow, text):
    assert (
        inspect.vitest_summary(
            ValidationCommandCapturedStream.model_validate(stream(text, "stdout")),
            ValidationCommandCapturedStream.model_validate(stream("", "stderr")),
        )["available"]
        is False
    )


def test_validated_historical_candidate_and_collision(flow, evidence, monkeypatch):
    f = evidence.workspace / "2_products/pepper-agent/web/src/example.ts"
    f.parent.mkdir(parents=True)
    f.write_text("historical")
    source_fixture(evidence.projected, flow.run_id, evidence.workspace)
    second = advance(flow, monkeypatch)
    f2 = second.candidate.parent / "2_products/pepper-agent/web/src/example.ts"
    f2.parent.mkdir(parents=True)
    f2.write_text("current")
    p = pr._load_current_projection_record()
    source_fixture(p, second.run_id, second.candidate.parent)
    binding = {
        "ticket_id": "P99.4",
        "work_packet_SHA256": flow.record["work_packet_SHA256"],
        "projection_SHA256": evidence.projected["projection_SHA256"],
        "task_id": evidence.projected["kanban_task_id"],
        "run_id": flow.run_id,
        "workspace": str(evidence.workspace),
    }
    r = call(second, section="historical_candidate", historical=binding)[
        "historical_candidate"
    ]
    assert r["available"] is True
    assert r["changed_path_count"] == 1
    assert (
        r["changed_paths"][0]["source_SHA256"] == hashlib.sha256(b"current").hexdigest()
    )
    for key, value in [
        ("workspace", "/etc"),
        ("projection_SHA256", "0" * 64),
        ("run_id", second.run_id),
    ]:
        with pytest.raises(ValueError):
            call(
                second,
                section="historical_candidate",
                historical={**binding, key: value},
            )


def test_sqlite_wal_committed_snapshot_has_no_file_side_effects(flow, tmp_path):
    from hermes_cli.agent_platform import evidence_sqlite

    path = tmp_path / "evidence.db"
    writer = sqlite3.connect(path)
    writer.execute("PRAGMA journal_mode=WAL")
    writer.execute("CREATE TABLE evidence(value)")
    writer.commit()
    writer.execute("INSERT INTO evidence VALUES (1)")
    writer.commit()
    writer.execute("INSERT INTO evidence VALUES (2)")
    before = {p.name: p.read_bytes() for p in tmp_path.glob("evidence.db*")}
    reader = evidence_sqlite.connect(path)
    assert [r[0] for r in reader.execute("SELECT value FROM evidence")] == [1]
    with pytest.raises(sqlite3.OperationalError):
        reader.execute("INSERT INTO evidence VALUES (3)")
    reader.close()
    assert {p.name: p.read_bytes() for p in tmp_path.glob("evidence.db*")} == before
    writer.rollback()
    writer.close()


@pytest.mark.parametrize("corruption", ["checksum", "partial"])
def test_sqlite_corrupt_wal_unavailable(flow, tmp_path, corruption):
    from hermes_cli.agent_platform import evidence_sqlite

    path = tmp_path / "evidence.db"
    writer = sqlite3.connect(path)
    writer.execute("PRAGMA journal_mode=WAL")
    writer.execute("CREATE TABLE evidence(value)")
    writer.commit()
    wal = Path(str(path) + "-wal")
    raw = bytearray(wal.read_bytes())
    if corruption == "checksum":
        raw[-1] ^= 1
    else:
        raw = raw[:-1]
    wal.write_bytes(raw)
    with pytest.raises(ValueError):
        evidence_sqlite.connect(path)
    writer.close()


@pytest.mark.parametrize(
    "key", ["TicketSpec_SHA256", "WorkPacket_SHA256", "current_run_id"]
)
def test_wrong_worker_witness_rejected(flow, evidence, observed, key):
    def change(r):
        if key == "current_run_id":
            r["task"][key] = 99999
        else:
            body = json.loads(r["task"]["body"])
            body[key] = "0" * 64
            r["task"]["body"] = json.dumps(body)

    rewrite(evidence, change, message_id=evidence.show)
    assert call(flow)["worker"]["available"] is False


def test_unresolved_write_attempt_is_not_hidden(flow, evidence, observed):
    c = sqlite3.connect(evidence.database)
    c.execute(
        "INSERT INTO messages (session_id,role,tool_calls,timestamp,active) VALUES (?,?,?,?,1)",
        (
            "synthetic-c66-worker",
            "assistant",
            json.dumps([
                {
                    "id": "unresolved",
                    "type": "function",
                    "function": {
                        "name": "write_file",
                        "arguments": json.dumps({
                            "path": "2_products/pepper-agent/web/src/example.ts"
                        }),
                    },
                }
            ]),
            evidence.run.started_at + 100,
        ),
    )
    c.commit()
    c.close()
    r = call(flow)["worker"]
    assert r["mutation_call_count"] == 1
    assert r["unresolved_calls"][0]["result_available"] is False


@pytest.mark.parametrize(
    "key", ["ticket_spec_SHA256", "work_packet_SHA256", "projection_SHA256"]
)
def test_terminal_metadata_contradiction_rejected(flow, evidence, observed, key):
    from hermes_cli import kanban_db as kb

    conn = kb.connect(board=evidence.projected["kanban_board_slug"])
    try:
        run = kb.get_run(conn, flow.run_id)
        metadata = dict(run.metadata or {})
        metadata[key] = "0" * 64
        conn.execute(
            "UPDATE task_runs SET metadata=? WHERE id=?",
            (json.dumps(metadata), flow.run_id),
        )
        conn.commit()
    finally:
        conn.close()
    with pytest.raises(ValueError, match="terminal run immutable"):
        call(flow)
