"""C70 reads real isolated approved authority, SQLite, source and candidate files."""

import hashlib
import json
from pathlib import Path

import pytest

from hermes_cli.agent_platform import execution_evidence as ev
from hermes_cli.agent_platform import pre_review_candidate as pc
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    UnsafeRuntimePathError,
)
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c68_execution_evidence import source_fixture
from tools import pepper_workflow_tools as tools

PATH = "2_products/pepper-agent/web/src/agent-platform/shell/example.ts"


@pytest.fixture
def candidate(flow, monkeypatch):
    p = pr._load_current_projection_record()
    workspace = flow.candidate.parent
    file = workspace / PATH
    file.parent.mkdir(parents=True)
    file.write_text("before\n")
    record = source_fixture(p, flow.run_id, workspace)
    scope = flow.record["work_packet_compilation_result"]["work_packet"][
        "repository_scope"
    ]
    record["materialization_manifest"].update(
        writable_allowed_paths=scope["allowed_paths"],
        forbidden_paths=scope["forbidden_paths"],
    )
    record["materialization_manifest_SHA256"] = pr._digest_payload(
        pr.PEPPER_GOVERNED_SOURCE_MATERIALIZATION_MANIFEST_DIGEST_ALGORITHM,
        record["materialization_manifest"],
    )
    record["governed_source_authority_SHA256"] = (
        pr._governed_source_authority_record_digest(record)
    )
    Path(record["authority_path"]).write_text(json.dumps(record))
    (workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).write_text(
        json.dumps({
            **record["materialization_manifest"],
            "durable_source_authority_SHA256": record[
                "governed_source_authority_SHA256"
            ],
            "durable_source_authority_reference": pr._governed_source_authority_reference(
                record
            ),
        })
    )
    file.write_text("after\n")
    conn = ev.kb.connect(board=p["kanban_board_slug"])
    metadata = {
        "implementation_complete": True,
        "validation_passed": True,
        "review_required": True,
        "terminal_outcome": "validated_review_required",
    }
    conn.execute(
        "UPDATE task_runs SET status='blocked', outcome='blocked', error=NULL, metadata=?, summary=? WHERE id=?",
        (
            json.dumps(metadata),
            "review-required: governed validation passed; human code review needed",
            flow.run_id,
        ),
    )
    conn.execute(
        "UPDATE tasks SET status='blocked', block_kind='needs_input', current_run_id=NULL, worker_pid=NULL, claim_lock=NULL WHERE id=?",
        (p["kanban_task_id"],),
    )
    conn.commit()
    conn.close()
    pr.recovery_action_record_path_for_ticket(p["ticket_id"]).unlink()
    for name in (
        "build_workflow_control_snapshot",
        "prepare_current_ticket_review",
        "_reconcile_kanban_board_lifecycle",
    ):
        monkeypatch.setattr(
            pr,
            name,
            lambda *a, **kw: pytest.fail(
                "inspection attempted mutation/reconciliation"
            ),
        )
    return p, workspace, record


def call(flow, operation="list", **kw):
    return pr.inspect_current_ticket_review_candidate(
        operation="pre_review_" + operation,
        ticket_id=flow.record["ticket_id"],
        reviewed_run_id=flow.run_id,
        **kw,
    )


def fingerprint(root):
    return {
        str(p): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
        for p in root.rglob("*")
        if p.is_file()
    }


def test_real_pre_review_list_content_diff_and_no_writes(flow, candidate):
    before = fingerprint(flow.home)
    listing = call(flow)
    assert listing["changed_paths"] == [
        {
            "path": PATH,
            "change": "modified",
            "source_SHA256": hashlib.sha256(b"before\n").hexdigest(),
            "candidate_SHA256": hashlib.sha256(b"after\n").hexdigest(),
        }
    ]
    guard = listing["candidate_binding_SHA256"]
    for op in ("metadata", "content", "diff", "aggregate_diff"):
        r = call(
            flow,
            op,
            candidate_binding_SHA256=guard,
            **({"candidate_path": PATH} if op != "aggregate_diff" else {}),
        )
        assert r["review_preparation_recorded"] is False
        assert r["manual_validation_recorded"] is False
        assert r["workflow_mutation"] is False
        assert set(r["manual_validation_statuses"].values()) == {"pending"}
        if op == "content":
            assert r["sections"][0]["candidate"]["text"] == "after\n"
            assert r["sections"][0]["source"]["text"] == "before\n"
        if op == "diff":
            assert "-before\n+after\n" in r["sections"][0]["diff"]["text"]
        if op == "aggregate_diff":
            assert r["aggregate_diff"]["complete"]
    assert fingerprint(flow.home) == before


@pytest.mark.parametrize(
    "path",
    [
        "/etc/passwd",
        "../example.ts",
        "a/../b",
        "a\\b",
        "C:/x",
        "a//b",
        "candidate.txt",
        "2_products/pepper-agent/web/src/.env",
        "2_products/pepper-agent/web/src/absent.ts",
    ],
)
def test_arbitrary_paths_denied(flow, candidate, path):
    guard = call(flow)["candidate_binding_SHA256"]
    with pytest.raises(ValueError):
        call(flow, "diff", candidate_binding_SHA256=guard, candidate_path=path)


@pytest.mark.parametrize(
    "what",
    [
        "candidate",
        "source",
        "missing_source",
        "workspace",
        "symlink",
        "active",
        "nonterminal",
        "wrong_projection",
        "wrong_workpacket",
    ],
)
def test_integrity_and_terminal_guards(flow, candidate, what):
    p, workspace, source = candidate
    guard = call(flow)["candidate_binding_SHA256"]
    if what == "candidate":
        (workspace / PATH).write_text("changed again")
    elif what == "source":
        (Path(source["snapshot_root"]) / PATH).write_text("bad source")
    elif what == "missing_source":
        Path(source["authority_path"]).unlink()
    elif what == "symlink":
        (workspace / PATH).unlink()
        (workspace / PATH).symlink_to(flow.candidate)
    else:
        conn = ev.kb.connect(board=p["kanban_board_slug"])
        if what == "workspace":
            conn.execute(
                "UPDATE tasks SET workspace_path=? WHERE id=?",
                (str(workspace.parent / "historical"), p["kanban_task_id"]),
            )
        elif what == "active":
            conn.execute(
                "UPDATE tasks SET current_run_id=? WHERE id=?",
                (flow.run_id, p["kanban_task_id"]),
            )
        elif what == "nonterminal":
            conn.execute(
                "UPDATE task_runs SET ended_at=NULL WHERE id=?", (flow.run_id,)
            )
        else:
            key = (
                "projection_SHA256"
                if what == "wrong_projection"
                else "work_packet_SHA256"
            )
            conn.execute(
                "UPDATE task_runs SET metadata=? WHERE id=?",
                (json.dumps({key: "wrong"}), flow.run_id),
            )
        conn.commit()
        conn.close()
    with pytest.raises((
        ValueError,
        OSError,
        pr.ProductRuntimeConflict,
        UnsafeRuntimePathError,
    )):
        call(flow, "diff", candidate_binding_SHA256=guard, candidate_path=PATH)


def test_tool_guards_and_binding_required(flow, candidate):
    base = {
        "operation": "pre_review_list",
        "ticket_id": flow.record["ticket_id"],
        "reviewed_run_id": flow.run_id,
    }
    for args in (
        {**base, "ticket_id": "wrong"},
        {**base, "reviewed_run_id": flow.run_id - 1},
        {**base, "historical_binding": {}},
        {**base, "operation": " pre_review_list ", "historical_binding": {}},
        {**base, "path": PATH},
        {**base, "review_package_SHA256": "wrong"},
        {**base, "operation": "pre_review_diff", "candidate_path": PATH},
    ):
        result = json.loads(tools._inspect_current_ticket_review_candidate(args))
        assert result["success"] is False
    assert json.loads(tools._inspect_current_ticket_review_candidate(base))["success"]


def test_explicit_bounds_and_binary(flow, candidate):
    guard = call(flow)["candidate_binding_SHA256"]
    r = call(flow, "aggregate_diff", candidate_binding_SHA256=guard, max_bytes=10)
    assert r["aggregate_diff"]["truncated"]
    assert not r["aggregate_diff"]["complete"]
    assert r["aggregate_diff"]["retained_byte_count"] <= 10
    assert r["omitted_paths"] == [PATH]
    (candidate[1] / PATH).write_bytes(b"binary\0data")
    guard = call(flow)["candidate_binding_SHA256"]
    r = call(flow, "aggregate_diff", candidate_binding_SHA256=guard)
    assert not r["aggregate_diff"]["complete"]
    assert r["omitted_paths"] == [PATH]


def test_race_during_read_is_rejected(flow, candidate, monkeypatch):
    guard = call(flow)["candidate_binding_SHA256"]
    real = pc.read_bytes

    def race(root, path, expected):
        data = real(root, path, expected)
        if root == candidate[1]:
            (root / path).write_text("raced")
        return data

    monkeypatch.setattr(pc, "read_bytes", race)
    with pytest.raises(ValueError, match="changed"):
        call(flow, "content", candidate_binding_SHA256=guard, candidate_path=PATH)


def test_changed_path_pagination(flow, candidate):
    for n in range(27):
        (candidate[1] / PATH).with_name(f"added-{n:02}.ts").write_text(f"file {n}\n")
    first = call(flow)
    assert first["changed_path_count"] == 28
    assert len(first["changed_paths"]) == 25
    second = call(
        flow,
        candidate_binding_SHA256=first["candidate_binding_SHA256"],
        evidence_offset=25,
    )
    assert len(second["changed_paths"]) == 3
    assert second["next_offset"] is None
    r = call(
        flow,
        "aggregate_diff",
        candidate_binding_SHA256=first["candidate_binding_SHA256"],
    )
    assert not r["aggregate_diff"]["complete"]
    assert r["next_offset"] == 25


@pytest.mark.parametrize("decision", ["passed", "failed"])
def test_manual_boundary_ends_without_inspection_authority(flow, candidate, decision):
    from hermes_cli.agent_platform import manual_validation as mv

    *_, items = pc.context(flow.record["ticket_id"], flow.run_id, None)
    for item in items:
        mv.persist(
            item["binding"],
            status=decision,
            human_attestation_text=item["required_attestation_text"][decision],
            evidence="isolated human fixture decision",
            actor="fixture",
        )
    with pytest.raises(ValueError, match="pending manual"):
        call(flow)


def test_old_mode_still_requires_package_and_pre_review_has_no_package(flow, candidate):
    r = pr.inspect_current_ticket_review_candidate(operation="aggregate_diff")
    assert r["blocker_code"] == "CURRENT_REVIEW_PACKAGE_MISSING"
    call(flow)
    r = pr.inspect_current_ticket_review_candidate(operation="aggregate_diff")
    assert r["blocker_code"] == "CURRENT_REVIEW_PACKAGE_MISSING"


@pytest.mark.parametrize("change", ["added", "deleted"])
def test_add_delete_diff(flow, candidate, change):
    file = candidate[1] / PATH
    if change == "deleted":
        file.unlink()
    else:
        file = file.with_name("added.ts")
        file.write_text("new\n")
    r = call(flow)
    path = file.relative_to(candidate[1]).as_posix()
    d = call(
        flow,
        "diff",
        candidate_binding_SHA256=r["candidate_binding_SHA256"],
        candidate_path=path,
    )
    assert d["sections"][0]["change"] == change
    assert d["sections"][0]["diff"]["complete"]


def test_missing_candidate_and_wrong_source_root(flow, candidate):
    manifest = candidate[1] / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    value = json.loads(manifest.read_text())
    value["source_root"] = str(flow.home)
    manifest.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="source root"):
        call(flow)


def test_prepared_package_cannot_be_shadowed(flow, candidate, monkeypatch):
    monkeypatch.setattr(
        pr,
        "_load_current_ticket_review_prepare_record_raw",
        lambda **kw: {"review_package_SHA256": "existing"},
    )
    with pytest.raises(ValueError, match="prepared review exists"):
        call(flow)


def test_review_prepare_revalidates_source_and_reobserves_candidate(flow, candidate):
    p, workspace, source = candidate
    listing = call(flow)
    (workspace / PATH).write_text("new candidate after inspection\n")
    completion = pr._kanban_completion_result_source(p, read_only=True)
    entry = next(
        x
        for x in completion["candidate_changes_reference"]["files"]
        if x["path"] == PATH
    )
    assert entry["workspace_SHA256"] != listing["changed_paths"][0]["candidate_SHA256"]
    (Path(source["snapshot_root"]) / PATH).write_text(
        "source corruption after inspection"
    )
    with pytest.raises(pr.ProductRuntimeConflict, match="snapshot"):
        pr._review_prepare_validation_context(p, completion)


@pytest.mark.parametrize(
    "mode", ["equal", "missing", "source_authority", "excluded_scope", "oversized"]
)
def test_unavailable_and_text_bounds(flow, candidate, mode):
    _, workspace, source = candidate
    if mode == "equal":
        (workspace / PATH).write_text("before\n")
    elif mode == "missing":
        workspace.rename(workspace.with_name(workspace.name + "-unavailable"))
    elif mode == "source_authority":
        record = json.loads(Path(source["authority_path"]).read_text())
        record["work_packet_SHA256"] = "wrong"
        Path(source["authority_path"]).write_text(json.dumps(record))
    elif mode == "excluded_scope":
        path = workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
        record = json.loads(path.read_text())
        record["product_diff_excluded_roots"] = ["2_products"]
        path.write_text(json.dumps(record))
    else:
        (workspace / PATH).write_text("x" * (pc.MAX_FILE_BYTES + 1))
        listing = call(flow)
        result = call(
            flow,
            "aggregate_diff",
            candidate_binding_SHA256=listing["candidate_binding_SHA256"],
        )
        assert result["omitted_paths"] == [PATH]
        assert result["aggregate_diff"]["complete"] is False
        return
    with pytest.raises((
        ValueError,
        OSError,
        pr.ProductRuntimeConflict,
        UnsafeRuntimePathError,
    )):
        call(flow)
