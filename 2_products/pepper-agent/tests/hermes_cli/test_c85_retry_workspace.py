"""Fresh retry allocation uses real approved authority and isolated SQLite."""

import json
from pathlib import Path

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import execution_evidence as ev
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import retry_workspace as rw
from tests.hermes_cli.test_c55_stale_retry_authority import (
    recovered as recovered,
    projection_home as projection_home,
    _retry,
)
from tests.hermes_cli.test_c70_pre_review_candidate import (
    candidate as candidate,
    flow as flow,
    call,
    PATH,
)


@pytest.fixture
def legacy(flow, request, monkeypatch):
    """Persist the run43 shape with real validators; only policy target is synthetic."""
    from tests.hermes_cli.test_c55_stale_retry_authority import fixtures
    from hermes_cli.agent_platform import recovery_authority
    import shutil

    recovery_path = pr.recovery_action_record_path_for_ticket(flow.record["ticket_id"])
    recovery = json.loads(recovery_path.read_text())
    p, workspace, source = request.getfixturevalue("candidate")
    old = workspace
    workspace = old.with_name(old.name + "-attempt-5")
    old.rename(workspace)
    flow.candidate = workspace / "candidate.txt"
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        conn.execute("UPDATE task_runs SET id=43 WHERE id=?", (flow.run_id,))
        for run_id in range(38, 43):
            conn.execute(
                "INSERT INTO task_runs(id,task_id,profile,status,started_at,ended_at,outcome) VALUES(?,?,?,'blocked',1,2,'blocked')",
                (run_id, p["kanban_task_id"], p["assignee_profile"]),
            )
        body = json.loads(kb.get_task(conn, p["kanban_task_id"]).body)
        conn.execute(
            "UPDATE tasks SET workspace_path=? WHERE id=?",
            (str(workspace), p["kanban_task_id"]),
        )
        conn.commit()
    flow.run_id = 43
    recovery.update(
        latest_failed_run_id=42,
        latest_failed_run_status="blocked",
        latest_failed_run_outcome="blocked",
        latest_failed_run_ended_at=2,
        observed_attempt_count=5,
        next_attempt_number=6,
        max_attempts=6,
        kanban_task_workspace_path=str(workspace),
    )
    recovery.pop("recovery_cycle_id", None)
    recovery["terminal_run_SHA256"] = recovery_authority.terminal_identity(recovery)
    recovery["recovery_action_SHA256"] = pr._recovery_action_record_digest(recovery)
    recovery_path.write_text(json.dumps(recovery))
    retry = pr._build_retry_start_authorization_record(
        request=pr.CurrentTicketExecutionStartRequest(
            ticket_id=p["ticket_id"],
            human_authorization_text=f"I explicitly authorize the retry execution of {p['ticket_id']} after failed run 42.",
        ),
        projection=p,
        recovery_record=recovery,
        retry_source={},
        provider_readiness=fixtures._ready_executor_provider_payload(
            p["assignee_profile"]
        ),
    )
    pr.retry_start_record_path_for_ticket(p["ticket_id"]).write_text(json.dumps(retry))
    body.update(
        fresh_execution_attempt_number=5,
        fresh_execution_workspace_path=str(workspace),
        fresh_execution_request_SHA256="a" * 64,
        retry_attempt_number=6,
        retry_identity_model="same_kanban_task_new_run",
        retry_authority_SHA256=recovery["recovery_action_SHA256"],
    )
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        conn.execute(
            "UPDATE tasks SET body=? WHERE id=?",
            (json.dumps(body), p["kanban_task_id"]),
        )
        kb._append_event(
            conn,
            p["kanban_task_id"],
            "retry_prepared",
            {
                "recovery_action_SHA256": recovery["recovery_action_SHA256"],
                "next_attempt_number": 6,
            },
        )
        kb._append_event(conn, p["kanban_task_id"], "claimed", {"run_id": 43})
        conn.commit()
    new_path = pr.governed_source_authority_record_path_for_run(p, 43)
    shutil.copytree(Path(source["authority_path"]).parent, new_path.parent)
    source = json.loads(
        json
        .dumps(source)
        .replace(str(Path(source["authority_path"]).parent), str(new_path.parent))
        .replace(str(old), str(workspace))
    )
    source["run_id"] = 43
    source["materialization_manifest_SHA256"] = pr._digest_payload(
        pr.PEPPER_GOVERNED_SOURCE_MATERIALIZATION_MANIFEST_DIGEST_ALGORITHM,
        source["materialization_manifest"],
    )
    source["governed_source_authority_SHA256"] = (
        pr._governed_source_authority_record_digest(source)
    )
    new_path.write_text(json.dumps(source))
    (workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).write_text(
        json.dumps({
            **source["materialization_manifest"],
            "durable_source_authority_SHA256": source[
                "governed_source_authority_SHA256"
            ],
            "durable_source_authority_reference": pr._governed_source_authority_reference(
                source
            ),
        })
    )
    monkeypatch.setattr(
        rw, "LEGACY", (p["project_id"], p["ticket_id"], p["kanban_task_id"], 43)
    )
    return p, workspace, source


def test_historical_public_inspection(flow, legacy):
    result = call(flow)
    assert result["historical_workspace_reuse"] is True
    assert result["workspace_freshness"] == "historical_reused_workspace"
    assert result["changed_paths"][0]["path"] == PATH
    assert (
        call(
            flow,
            "content",
            candidate_binding_SHA256=result["candidate_binding_SHA256"],
            candidate_path=PATH,
        )["sections"][0]["candidate"]["text"]
        == "after\n"
    )


@pytest.mark.parametrize(
    "fault",
    ["retry", "task", "run", "source", "manifest", "active", "workspace", "later"],
)
def test_historical_fail_closed(flow, legacy, fault):
    p, workspace, source = legacy
    if fault == "retry":
        pr.retry_start_record_path_for_ticket(p["ticket_id"]).unlink()
    elif fault == "source":
        Path(source["authority_path"]).write_text("{}")
    elif fault == "manifest":
        path = workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
        record = json.loads(path.read_text())
        record["durable_source_authority_reference"]["run_id"] = 42
        path.write_text(json.dumps(record))
    elif fault == "run":
        flow.run_id = 42
    else:
        with kb.connect(board=p["kanban_board_slug"]) as conn:
            if fault == "active":
                conn.execute(
                    "UPDATE tasks SET current_run_id=43 WHERE id=?",
                    (p["kanban_task_id"],),
                )
            elif fault == "task":
                conn.execute("UPDATE task_runs SET task_id='other' WHERE id=43")
            elif fault == "later":
                conn.execute(
                    "INSERT INTO task_runs(id,task_id,profile,status,started_at,ended_at,outcome) VALUES(44,?,?,'blocked',3,4,'blocked')",
                    (p["kanban_task_id"], p["assignee_profile"]),
                )
            else:
                conn.execute(
                    "UPDATE tasks SET workspace_path=? WHERE id=?",
                    (
                        str(workspace.parent / "other" / workspace.name),
                        p["kanban_task_id"],
                    ),
                )
            conn.commit()
    with pytest.raises((ValueError, OSError, pr.ProductRuntimeError)):
        call(flow)


def test_fresh_retry_before_single_dispatch(recovered):
    p, _ = recovered
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        old = Path(kb.get_task(conn, p["kanban_task_id"]).workspace_path)
    old.mkdir(exist_ok=True, parents=True)
    marker = old / "historical.txt"
    marker.write_text("immutable failed candidate")
    before = marker.read_bytes()
    calls = []

    def spawn(task, workspace, **kwargs):
        calls.append(workspace)
        body = json.loads(task.body)
        assert Path(workspace).is_dir() and Path(workspace) != old
        assert (
            body["fresh_execution_workspace_path"] == workspace == task.workspace_path
        )
        assert body["fresh_execution_attempt_number"] == 2
        assert marker.read_bytes() == before
        return 4321

    result = _retry(spawn)
    assert result["execution_started"] is True, result
    assert len(calls) == 1
    replay = _retry(spawn)
    assert replay["idempotent_replay"] is True
    assert len(calls) == 1 and marker.read_bytes() == before
    assert pr.load_current_ticket_recovery_action_record() is not None


def test_existing_workspace_never_reused(recovered):
    p, _ = recovered
    workspace = (
        kb.workspaces_root(board=p["kanban_board_slug"])
        / f"{p['kanban_task_id']}-attempt-2"
    )
    workspace.mkdir(parents=True)
    (workspace / "sentinel").write_text("keep")
    result = _retry(lambda *a, **kw: pytest.fail("must not spawn"))
    assert result["blocker_code"] == "RETRY_WORKSPACE_ALLOCATION_FAILED"
    assert (workspace / "sentinel").read_text() == "keep"
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        assert len(kb.list_runs(conn, p["kanban_task_id"])) == 1


def test_partial_allocation_persistence_never_spawns(recovered, monkeypatch):
    p, _ = recovered
    real = kb._append_event

    def fail(conn, task, kind, *args, **kwargs):
        if kind == "retry_workspace_allocated":
            with ev.connection(
                kb.kanban_db_path(board=p["kanban_board_slug"])
            ) as observer:
                visible = kb.get_task(observer, p["kanban_task_id"])
                assert visible.status == "blocked"
                assert visible.workspace_path == old
            raise ValueError("synthetic persistence failure")
        return real(conn, task, kind, *args, **kwargs)

    monkeypatch.setattr(kb, "_append_event", fail)
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        old = kb.get_task(conn, p["kanban_task_id"]).workspace_path
    result = _retry(lambda *a, **kw: pytest.fail("must not spawn"))
    assert result["blocker_code"] == "RETRY_WORKSPACE_ALLOCATION_FAILED"
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        assert kb.get_task(conn, p["kanban_task_id"]).workspace_path == old
        assert len(kb.list_runs(conn, p["kanban_task_id"])) == 1


@pytest.mark.parametrize("size", [16_000_001, 22_398_108, 32_000_000])
def test_bounded_large_json(tmp_path, size):
    path = tmp_path / "authority.json"
    path.write_bytes(b"{}" + b" " * (size - 2))
    assert ev.read_json(path, tmp_path, maximum=32_000_000) == {}


@pytest.mark.parametrize("raw", [b"{" + b" " * 32_000_000, b"{}" + b" " * 32_000_000])
def test_oversized_json_rejected_before_parse(tmp_path, raw):
    path = tmp_path / "authority.json"
    path.write_bytes(raw)
    with pytest.raises(ValueError, match="exceeds inspection bound"):
        ev.read_json(path, tmp_path, maximum=32_000_000)


def test_arbitrary_legacy_identity_rejected():
    from types import SimpleNamespace

    with pytest.raises(ValueError, match="not an authorized historical"):
        rw.historical(
            {"project_id": "PEPPER", "ticket_id": "other"},
            SimpleNamespace(id="t_other"),
            SimpleNamespace(id=43),
            [],
            Path("/x"),
        )


def test_future_terminal_candidate_inspection(flow, monkeypatch):
    from tests.hermes_cli.test_c55_stale_retry_authority import fixtures
    from tests.hermes_cli.test_c68_execution_evidence import source_fixture

    p = pr._load_current_projection_record()
    monkeypatch.setattr(pr, "_pepper_governed_worker_env_overlay", lambda p: {})
    old = flow.candidate.read_bytes()
    monkeypatch.setattr(
        pr, "_executor_provider_readiness", fixtures._ready_executor_provider_payload
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda *a, **k: fixtures._ready_worker_credential_probe(),
    )
    monkeypatch.setattr(kb, "_pid_alive", lambda pid: pid == 4321)
    monkeypatch.setattr(
        pr, "_projection_requires_scratch_source_materialization", lambda p: True
    )
    sources = []

    def materialize(**kw):
        workspace = Path(kw["workspace"])
        file = workspace / PATH
        file.parent.mkdir(parents=True)
        file.write_text("before\n")
        record = source_fixture(p, kw["run_id"], workspace)
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
        manifest = {
            **record["materialization_manifest"],
            "durable_source_authority_SHA256": record[
                "governed_source_authority_SHA256"
            ],
            "durable_source_authority_reference": pr._governed_source_authority_reference(
                record
            ),
        }
        (workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).write_text(
            json.dumps(manifest)
        )
        sources.append(record)
        return manifest, pr._governed_source_authority_reference(record)

    monkeypatch.setattr(
        pr, "_prepare_governed_source_authority_for_dispatch", materialize
    )
    calls = []

    def spawn(task, workspace, **kw):
        assert len(sources) == 1 and sources[0]["run_id"] == task.current_run_id
        assert flow.candidate.read_bytes() == old
        (Path(workspace) / PATH).write_text("after\n")
        calls.append(workspace)
        return 4321

    result = pr.start_current_ticket_execution(
        ticket_id=p["ticket_id"],
        next_action_id=f"START_{p['ticket_id'].replace('.', '_')}_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        human_authorization_text=f"I explicitly authorize the retry execution of {p['ticket_id']}.",
        spawn_fn=spawn,
    )
    assert result["execution_started"], result
    flow.run_id = result["kanban_run_id"]
    fixtures._finish_projected_run_as_terminal(
        kb,
        p,
        flow.run_id,
        status="blocked",
        outcome="blocked",
        summary="review-required: governed validation passed; human code review needed",
    )
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        conn.execute(
            "UPDATE task_runs SET error=NULL, metadata=? WHERE id=?",
            (
                json.dumps({
                    "implementation_complete": True,
                    "validation_passed": True,
                    "review_required": True,
                    "terminal_outcome": "validated_review_required",
                }),
                flow.run_id,
            ),
        )
        conn.execute(
            "UPDATE tasks SET block_kind='needs_input' WHERE id=?",
            (p["kanban_task_id"],),
        )
        conn.commit()
    completion = pr._kanban_completion_result_source(p, read_only=True)
    assert not completion.get("blocker_code"), completion
    assert pr._review_prepare_human_git_handoff_required(completion), completion
    listing = call(flow)
    assert (
        listing["success"] and listing["workspace_freshness"] == "fresh_retry_workspace"
    )
    assert listing["historical_workspace_reuse"] is False
    assert len(calls) == 1 and flow.candidate.read_bytes() == old
    content = call(
        flow,
        "diff",
        candidate_binding_SHA256=listing["candidate_binding_SHA256"],
        candidate_path=PATH,
    )
    assert "-before\n+after\n" in content["sections"][0]["diff"]["text"]


@pytest.mark.parametrize(
    "field,value",
    [("snapshot_file_count", 100001), ("snapshot_total_bytes", 2000000001)],
)
def test_source_limits_still_enforced(flow, candidate, field, value):
    p, workspace, source = candidate
    source[field] = value
    Path(source["authority_path"]).write_text(json.dumps(source))
    with pytest.raises(ValueError, match="exceeds bounded inspection limits"):
        call(flow)


@pytest.mark.parametrize(
    "field",
    [
        "fresh_execution_attempt_number",
        "fresh_execution_workspace_path",
        "retry_authority_SHA256",
    ],
)
def test_stale_allocation_fails_before_worker(recovered, monkeypatch, field):
    p, _ = recovered
    dispatch = pr._dispatch_exact_current_kanban_task

    def drift(*args, **kwargs):
        with kb.connect(board=p["kanban_board_slug"]) as conn:
            task = kb.get_task(conn, p["kanban_task_id"])
            body = json.loads(task.body)
            body[field] = 1 if field.endswith("number") else "stale"
            conn.execute(
                "UPDATE tasks SET body=? WHERE id=?", (json.dumps(body), task.id)
            )
            conn.commit()
        return dispatch(*args, **kwargs)

    monkeypatch.setattr(pr, "_dispatch_exact_current_kanban_task", drift)
    result = _retry(lambda *a, **k: pytest.fail("stale allocation must not spawn"))
    assert result["blocker_code"] == "WORKSPACE_POLICY_GAP"
    assert result["worker_process_started"] is False


def test_current_sized_authority_fully_validates(flow, candidate):
    p, workspace, source = candidate
    source["bounded_fixture_padding"] = " " * 22_398_108
    source["governed_source_authority_SHA256"] = (
        pr._governed_source_authority_record_digest(source)
    )
    Path(source["authority_path"]).write_text(json.dumps(source))
    with ev.connection(kb.kanban_db_path(board=p["kanban_board_slug"])) as conn:
        run = kb.get_run(conn, flow.run_id)
    validated = ev.source(p, run)
    assert (
        validated["governed_source_authority_SHA256"]
        == source["governed_source_authority_SHA256"]
    )


def test_retry_real_source_reset_and_binding(recovered, monkeypatch):
    from tests.hermes_cli.test_c55_stale_retry_authority import fixtures

    p, _ = recovered
    events = []
    fixtures._install_c21_source_authority_derivation(monkeypatch, pr, events)
    monkeypatch.setattr(
        pr, "_projection_requires_scratch_source_materialization", lambda p: True
    )
    with kb.connect(board=p["kanban_board_slug"]) as conn:
        old = Path(kb.get_task(conn, p["kanban_task_id"]).workspace_path)
    old.mkdir(parents=True, exist_ok=True)
    (old / "unchanged.txt").write_text("historical")

    def spawn(task, workspace, **kwargs):
        assert Path(workspace) != old
        manifest = json.loads(
            (
                Path(workspace) / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
            ).read_text()
        )
        assert (
            manifest["durable_source_authority_reference"]["run_id"]
            == task.current_run_id
        )
        assert manifest["durable_source_authority_validated_before_worker_execution"]
        assert manifest["source_authority_materialized_before_worker_execution"]
        assert (old / "unchanged.txt").read_text() == "historical"
        events.append("spawn")
        return 4321

    result = _retry(spawn)
    assert result["execution_started"], result
    assert events == ["source_authority_derivation", "spawn"]
