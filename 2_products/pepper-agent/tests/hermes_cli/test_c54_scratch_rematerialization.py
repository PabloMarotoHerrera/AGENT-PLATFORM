"""Exact-source dispatch must not inherit prior scratch attempt contents."""

import json
from pathlib import Path

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)


@pytest.fixture
def scratch_case(projection_home, monkeypatch):
    _, _, projection = fixtures._c21_dispatch_fixture(projection_home, monkeypatch)
    fixtures._install_c21_source_authority_derivation(monkeypatch, pr, [])
    return projection


def _dispatch(projection, spawn=None):
    return pr._dispatch_exact_current_kanban_task(
        projection, spawn_fn=spawn or (lambda *a, **kw: 4321),
    )


def _terminal_then_ready(projection):
    with kb.connect(board=projection["kanban_board_slug"]) as conn:
        tid = projection["kanban_task_id"]
        assert kb.block_task(conn, tid, kind="needs_input", reason="Candidate needs review",
                             metadata={"review_required": True})
        previous = tuple(conn.execute("SELECT * FROM task_runs WHERE task_id=?", (tid,)).fetchone())
        assert kb.unblock_task(conn, tid)
        kb.recompute_ready(conn)
    return previous


@pytest.mark.parametrize("stale", ["candidate.ts", "nested/cache/old.json", None])
def test_c54_two_attempts_rematerialize_exactly(scratch_case, stale):
    projection = scratch_case
    first = _dispatch(projection)
    assert first["start_status"] == "started", first
    workspace = Path(first["workspace_path"])
    authority_path = Path(first["governed_source_authority_path"])
    previous_authority = authority_path.read_bytes()
    first_authority = json.loads(previous_authority)
    source_rel = first_authority["snapshot_manifest"]["files"][0]["relative_path"]
    (workspace / source_rel).write_text("prior candidate changes")
    if stale:
        path = workspace / stale
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("stale prior attempt")
    manifest_path = workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    previous_manifest = json.loads(manifest_path.read_text())
    previous_manifest["stale_attempt_marker"] = True
    manifest_path.write_text(json.dumps(previous_manifest))
    previous_run = _terminal_then_ready(projection)
    spawns = []

    def spawn(task, path, **kwargs):
        spawns.append(task.current_run_id)
        assert Path(path) == workspace
        manifest = json.loads(manifest_path.read_text())
        assert "stale_attempt_marker" not in manifest
        assert manifest["rematerialized_from_terminal_run_id"] == task.current_run_id
        authority = json.loads(Path(manifest["governed_source_authority_path"]).read_text())
        assert authority["Git_mutation"] is False
        expected = {item["relative_path"] for item in authority["snapshot_manifest"]["files"]}
        observed = {p.relative_to(workspace).as_posix() for p in workspace.rglob("*") if p.is_file()}
        assert observed == expected | {pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST}
        assert pr._verify_rematerialized_source_authority_workspace(
            source_authority=authority, workspace_root=workspace,
        )["verified"]
        return 4322

    second = _dispatch(projection, spawn)
    assert second["start_status"] == "started", second
    assert second["source_authority_materialization_verification"]["verified"]
    assert second["kanban_run_id"] != first["kanban_run_id"]
    assert spawns == [second["kanban_run_id"]]
    assert authority_path.read_bytes() == previous_authority
    assert pr._build_governed_source_snapshot_manifest(Path(first_authority["snapshot_root"]))["snapshot_SHA256"] == first_authority["snapshot_SHA256"]
    with kb.connect(board=projection["kanban_board_slug"]) as conn:
        assert tuple(conn.execute("SELECT * FROM task_runs WHERE id=?", (first["kanban_run_id"],)).fetchone()) == previous_run
        assert len(kb.list_runs(conn, projection["kanban_task_id"])) == 2


@pytest.fixture
def pending_retry(scratch_case):
    projection = scratch_case
    first = _dispatch(projection)
    assert first["start_status"] == "started", first
    workspace = Path(first["workspace_path"])
    stale = workspace / "old/nested/candidate.txt"
    stale.parent.mkdir(parents=True)
    stale.write_text("prior attempt evidence")
    _terminal_then_ready(projection)
    return projection, first, workspace, stale


def _assert_blocked_without_spawn(projection, code="WORKSPACE_SOURCE_MATERIALIZATION_FAILED"):
    calls = []
    result = _dispatch(projection, lambda *a, **k: calls.append(True))
    assert result["start_status"] == "blocked", result
    assert result["blocker_code"] == code
    assert result["execution_started"] is False
    assert result.get("source_materialized") is not True
    assert result["worker_process_started"] is False
    assert not calls
    return result


@pytest.mark.parametrize("damage", [
    "outside", "scratch_root", "other_task", "other_board", "root_symlink", "parent_symlink",
    "nested_symlink", "file_symlink", "dangling_symlink", "reparse", "mount",
    "dir", "worktree", "unsafe_rmtree", "protected_store", "source_checkout",
])
def test_c54_unsafe_targets_preserve_contents(pending_retry, monkeypatch, tmp_path, damage):
    import shutil
    from hermes_cli.agent_platform.runtime_adapter import path_containment as pc

    projection, _, workspace, stale = pending_retry
    outside = tmp_path / "outside"
    outside.mkdir()
    external_evidence = outside / "evidence.txt"
    external_evidence.write_text("must survive")
    target = workspace
    kind = "scratch"
    if damage in {"outside", "dir", "worktree"}:
        target = outside
        if damage != "outside":
            kind = damage
        if damage == "worktree":
            # Exercise the cleanup boundary without using Git to allocate a worktree.
            monkeypatch.setattr(kb, "resolve_workspace", lambda *a, **k: outside)
    elif damage == "scratch_root":
        target = workspace.parent
    elif damage in {"other_task", "other_board"}:
        target = workspace.parent / "t_other" if damage == "other_task" else workspace.parents[1] / "boards" / "other" / "workspaces" / projection["kanban_task_id"]
        target.mkdir(parents=True)
        (target / "evidence.txt").write_text("another task")
    elif damage == "root_symlink":
        moved = workspace.with_name(workspace.name + "_saved")
        workspace.rename(moved)
        workspace.symlink_to(outside, target_is_directory=True)
        stale = moved / stale.relative_to(workspace)
    elif damage == "parent_symlink":
        moved = workspace.parent.with_name("saved-workspaces")
        workspace.parent.rename(moved)
        workspace.parent.symlink_to(moved, target_is_directory=True)
    elif damage in {"nested_symlink", "file_symlink", "dangling_symlink"}:
        destination = outside if damage == "nested_symlink" else external_evidence
        if damage == "dangling_symlink":
            destination = outside / "missing"
        (workspace / "redirect").symlink_to(destination, target_is_directory=damage == "nested_symlink")
    elif damage == "reparse":
        original = pc.is_reparse_or_symlink
        monkeypatch.setattr(pc, "is_reparse_or_symlink", lambda p: Path(p) == workspace or original(p))
    elif damage == "mount":
        original = Path.is_mount
        monkeypatch.setattr(Path, "is_mount", lambda p: p == stale.parent or original(p))
    elif damage == "unsafe_rmtree":
        monkeypatch.setattr(shutil.rmtree, "avoids_symlink_attacks", False)
    elif damage in {"protected_store", "source_checkout"}:
        root = workspace.parents[2] / "agent-platform" / "unsafe-root" if damage == "protected_store" else outside
        target = root / projection["kanban_task_id"]
        target.mkdir(parents=True)
        (target / "evidence.txt").write_text("protected")
        monkeypatch.setenv("HERMES_KANBAN_WORKSPACES_ROOT", str(root))
        if damage == "source_checkout":
            original = pr._load_governed_source_authority_from_reference
            def bound_source(*a, **k):
                authority = original(*a, **k)
                authority["git_source_authority"]["source_root"] = str(outside)
                return authority
            monkeypatch.setattr(pr, "_load_governed_source_authority_from_reference", bound_source)
    with kb.connect(board=projection["kanban_board_slug"]) as conn:
        conn.execute("UPDATE tasks SET workspace_path=?, workspace_kind=? WHERE id=?",
                     (str(target), kind, projection["kanban_task_id"]))
        conn.commit()
    _assert_blocked_without_spawn(
        projection, "WORKSPACE_POLICY_GAP" if damage in {"dir", "worktree"} else "WORKSPACE_SOURCE_MATERIALIZATION_FAILED",
    )
    assert stale.read_text() == "prior attempt evidence"
    assert external_evidence.read_text() == "must survive"
    if damage in {"other_task", "other_board", "protected_store", "source_checkout"}:
        assert (target / "evidence.txt").read_text() in {"another task", "protected"}


@pytest.mark.parametrize("damage", ["record", "snapshot", "manifest"])
def test_c54_invalid_authority_never_cleans(pending_retry, monkeypatch, damage):
    projection, _, workspace, stale = pending_retry
    before = (workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).read_bytes()
    original = pr._persist_governed_source_authority
    def persist(**kwargs):
        ref = original(**kwargs)
        path = Path(ref["authority_path"])
        record = json.loads(path.read_text())
        if damage == "record":
            record["run_id"] = -1
            path.write_text(json.dumps(record))
        elif damage == "snapshot":
            item = record["snapshot_manifest"]["files"][0]
            (Path(record["snapshot_root"]) / item["relative_path"]).write_text("tampered")
        else:
            Path(record["snapshot_manifest_path"]).write_text("{}")
        return ref
    monkeypatch.setattr(pr, "_persist_governed_source_authority", persist)
    result = _assert_blocked_without_spawn(projection)
    assert "digest mismatch" in result["blocker_detail"]
    assert stale.read_text() == "prior attempt evidence"
    assert (workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).read_bytes() == before


@pytest.mark.parametrize("damage", [
    "task_pid", "run_pid", "claim", "expired", "run_ended", "other_open_run", "other_task", "child", "new_run",
])
def test_c54_concurrent_ownership_prevents_reset(pending_retry, monkeypatch, damage):
    projection, _, _, stale = pending_retry
    original = pr._load_governed_source_authority_from_reference
    before = []
    def change_owner(*a, **kw):
        authority = original(*a, **kw)
        with kb.connect(board=projection["kanban_board_slug"]) as conn:
            tid = projection["kanban_task_id"]
            task = kb.get_task(conn, tid)
            if damage == "task_pid":
                conn.execute("UPDATE tasks SET worker_pid=123 WHERE id=?", (tid,))
            elif damage == "run_pid":
                conn.execute("UPDATE task_runs SET worker_pid=123 WHERE id=?", (task.current_run_id,))
            elif damage == "claim":
                conn.execute("UPDATE tasks SET claim_lock='another-dispatcher' WHERE id=?", (tid,))
            elif damage == "expired":
                conn.execute("UPDATE tasks SET claim_expires=1 WHERE id=?", (tid,))
            elif damage == "run_ended":
                conn.execute("UPDATE task_runs SET ended_at=1 WHERE id=?", (task.current_run_id,))
            elif damage == "new_run":
                conn.execute("UPDATE task_runs SET ended_at=1 WHERE id=?", (task.current_run_id,))
                other_run = conn.execute("INSERT INTO task_runs(task_id,status,started_at,claim_lock) VALUES (?,'running',1,'new-owner')", (tid,)).lastrowid
                conn.execute("UPDATE tasks SET current_run_id=?, claim_lock='new-owner' WHERE id=?", (other_run, tid))
            elif damage == "other_open_run":
                conn.execute("INSERT INTO task_runs(task_id,status,started_at) VALUES (?,'running',1)", (tid,))
            conn.commit()
            if damage in {"other_task", "child"}:
                other = kb.create_task(conn, title="Other task", workspace_kind="scratch")
                if damage == "other_task":
                    kb.recompute_ready(conn)
                    assert kb.claim_task(conn, other)
                    kb.set_workspace_path(conn, other, task.workspace_path)
                else:
                    kb.link_tasks(conn, tid, other)
            before.append((tuple(conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()),
                           [tuple(r) for r in conn.execute("SELECT * FROM task_runs WHERE task_id=? ORDER BY id", (tid,))]))
        return authority
    monkeypatch.setattr(pr, "_load_governed_source_authority_from_reference", change_owner)
    _assert_blocked_without_spawn(projection)
    assert stale.read_text() == "prior attempt evidence"
    with kb.connect(board=projection["kanban_board_slug"]) as conn:
        tid = projection["kanban_task_id"]
        after = (tuple(conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()),
                 [tuple(r) for r in conn.execute("SELECT * FROM task_runs WHERE task_id=? ORDER BY id", (tid,))])
        assert after == before[-1]


@pytest.mark.parametrize("failure", ["reset", "copy", "unexpected_after_copy"])
def test_c54_failure_never_spawns_or_claims_materialization(pending_retry, monkeypatch, failure):
    projection, first, workspace, _ = pending_retry
    old_authority = Path(first["governed_source_authority_path"]).read_bytes()
    if failure == "reset":
        def fail(*a, **kw):
            raise OSError("synthetic reset failure")
        monkeypatch.setattr(pr, "_remove_materialized_destination", fail)
    else:
        original = pr._copy_governed_source_authority_snapshot_files
        def copy(**kwargs):
            original(**kwargs)
            if failure == "copy":
                raise OSError("synthetic copy failure")
            (kwargs["workspace_root"] / "unexpected.txt").write_text("injected extra")
        monkeypatch.setattr(pr, "_copy_governed_source_authority_snapshot_files", copy)
    result = _assert_blocked_without_spawn(projection)
    if failure == "unexpected_after_copy":
        assert "contains unexpected files" in result["blocker_detail"]
        manifest = json.loads((workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).read_text())
        assert manifest["source_materialized"] is False
    assert Path(first["governed_source_authority_path"]).read_bytes() == old_authority



def test_c54_reset_and_copy_hold_exclusive_database_lock(pending_retry, monkeypatch):
    import sqlite3

    projection, _, _, stale = pending_retry
    original = pr._copy_governed_source_authority_snapshot_files
    checked = []
    def copy(**kwargs):
        contender = sqlite3.connect(str(kb.kanban_db_path(board=projection["kanban_board_slug"])), timeout=0)
        try:
            with pytest.raises(sqlite3.OperationalError, match="locked"):
                contender.execute("UPDATE tasks SET claim_lock='racing-owner' WHERE id=?", (projection["kanban_task_id"],))
            checked.append(True)
        finally:
            contender.close()
        original(**kwargs)
    monkeypatch.setattr(pr, "_copy_governed_source_authority_snapshot_files", copy)
    result = _dispatch(projection)
    assert result["start_status"] == "started", result
    assert checked == [True]
    assert not stale.exists()


@pytest.mark.parametrize("kind", ["dir", "worktree"])
def test_c54_workspace_kind_drift_after_claim_is_not_cleaned(pending_retry, monkeypatch, kind):
    projection, _, _, stale = pending_retry
    original = pr._load_governed_source_authority_from_reference
    def drift(*a, **kw):
        authority = original(*a, **kw)
        with kb.connect(board=projection["kanban_board_slug"]) as conn:
            conn.execute("UPDATE tasks SET workspace_kind=? WHERE id=?", (kind, projection["kanban_task_id"]))
            conn.commit()
        return authority
    monkeypatch.setattr(pr, "_load_governed_source_authority_from_reference", drift)
    result = _assert_blocked_without_spawn(projection)
    assert "requires a managed scratch workspace" in result["blocker_detail"]
    assert stale.read_text() == "prior attempt evidence"



def test_c54_wrong_board_connection_never_cleans(pending_retry, monkeypatch):
    projection, _, _, stale = pending_retry
    original = pr._prepare_governed_source_authority_for_dispatch
    def prepare(**kwargs):
        # The destructive boundary must validate the actual connection, not
        # merely trust a caller's board string or same-numbered task/run.
        with kb.connect(board="other-board") as other:
            kwargs["conn"] = other
            return original(**kwargs)
    monkeypatch.setattr(pr, "_prepare_governed_source_authority_for_dispatch", prepare)
    result = _assert_blocked_without_spawn(projection)
    assert "board database mismatch" in result["blocker_detail"]
    assert stale.read_text() == "prior attempt evidence"


@pytest.mark.parametrize("binding", ["valid", "missing_event", "wrong_digest", "wrong_source", "wrong_attempt"])
def test_c54_attempt_scoped_path_requires_durable_preparation(pending_retry, binding):
    projection, first, original_workspace, old_stale = pending_retry
    tid = projection["kanban_task_id"]
    reference = {"fresh_execution_request_SHA256": "f" * 64,
                 "prior_terminal_run_id": first["kanban_run_id"]}
    with kb.connect(board=projection["kanban_board_slug"]) as conn:
        task = kb.get_task(conn, tid)
        body, fresh_path = pr._governed_autonomy_dispatch_task_body(
            raw_body=task.body, projection=projection,
            activation_action_sha256="a" * 64, authority_sha256="b" * 64,
            source_run_id=first["kanban_run_id"], fresh_execution_request=reference,
            run_count=1, board=projection["kanban_board_slug"], kanban_db=kb,
        )
        workspace = Path(fresh_path)
        workspace.mkdir()
        stale = workspace / "prior-generated.txt"
        stale.write_text("old fresh-attempt output")
        if binding == "wrong_attempt":
            body["fresh_execution_attempt_number"] = 1
        payload = pr._governed_autonomy_continuation_prepared_event_payload(
            activation_action_sha256="a" * 64, authority_sha256="b" * 64,
            source_run_id=first["kanban_run_id"], task_triage_specified=False,
            terminal_done_task_rearmed=False, fresh_execution_request=dict(reference),
            fresh_workspace_path=fresh_path,
        )
        if binding == "wrong_digest":
            payload["fresh_execution_request_reference"]["fresh_execution_request_SHA256"] = "e" * 64
        elif binding == "wrong_source":
            payload["source"] = "untrusted"
        conn.execute("UPDATE tasks SET body=?, workspace_path=? WHERE id=?", (json.dumps(body), fresh_path, tid))
        if binding != "missing_event":
            kb._append_event(conn, tid, "governed_autonomy_continuation_prepared", payload)
        conn.commit()
    if binding == "valid":
        result = _dispatch(projection)
        assert result["start_status"] == "started", result
        assert result["workspace_path"] == fresh_path
        assert result["source_authority_materialization_verification"]["verified"]
        assert not stale.exists()
    else:
        _assert_blocked_without_spawn(projection)
        assert stale.read_text() == "old fresh-attempt output"
    # The previously terminal task workspace is not this reset's target.
    assert old_stale.read_text() == "prior attempt evidence"
    assert original_workspace.exists()
