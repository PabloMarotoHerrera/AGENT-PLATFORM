"""C51 reuses C50's 81 durable records plus the two live C50 projection changes."""

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests.hermes_cli.test_c50_live_projection_authority import (
    live_authority as live_authority,
)
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)


@pytest.fixture
def current_revision(live_authority):
    delta = json.loads(
        (
            Path(__file__).parents[1] / "fixtures/c51_live_authority_delta.json"
        ).read_text()
    )
    for name, data in delta["records"].items():
        encoded = data.encode()
        assert hashlib.sha256(encoded).hexdigest() == delta["manifest"][name]
        path = live_authority / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encoded)
    generation = pr._current_approved_generation_authority_from_records()[
        "generation_record"
    ]
    current = projection.load_kanban_projection_record(
        ticket_id=generation["ticket_id"]
    )
    start_path = pr.execution_start_record_path_for_ticket(generation["ticket_id"])
    old_bytes = start_path.read_bytes()
    old_start = json.loads(old_bytes)
    historical = json.loads(
        projection._historical_projection_path(old_start).read_bytes()
    )
    assert projection._projection_is_superseded(historical, generation)
    assert (
        pr.validate_p18_9_0_execution_start_record(
            old_start, projection_record=historical
        )
        == old_start
    )
    return SimpleNamespace(
        home=live_authority,
        generation=generation,
        current=current,
        path=start_path,
        old_bytes=old_bytes,
        old=old_start,
        historical=historical,
    )


def test_c51_live_shape_start_does_not_block_on_proven_old_revision(current_revision):
    state = current_revision
    result = pr.start_current_ticket_execution(
        human_authorization_text=f"Start {state.generation['ticket_id']} execution now",
        spawn_fn=lambda *a, **k: pytest.fail("preparation regression must not spawn"),
    )
    assert result.get("blocker_code") != "EXECUTION_START_AUTHORITY_STALE", result


@pytest.fixture
def startable_revision(current_revision, monkeypatch):
    import os
    import subprocess
    import model_tools  # noqa: F401
    from hermes_cli import kanban_db
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
        _patch_synthetic_scratch_materialization,
        _ready_executor_provider_payload,
        _ready_worker_credential_probe,
    )

    state = current_revision
    decision = bridge.load_approval_decision_record(
        ticket_id=state.generation["ticket_id"]
    )
    # The durable capture excludes SQLite. Restore the completed bootstrap task
    # so its historical retry does not produce an artificial task_missing blocker.
    bootstrap = pr._bootstrap_projection_record_for_validation()
    with monkeypatch.context() as setup:
        setup.setattr(kanban_db, "_new_task_id", lambda: bootstrap["kanban_task_id"])
        with kanban_db.connect(board=bootstrap["kanban_board_slug"]) as conn:
            prior_task = kanban_db.create_task(conn, title="Completed predecessor")
            assert kanban_db.complete_task(
                conn, prior_task, result="Completed predecessor fixture"
            )
    with monkeypatch.context() as setup:
        setup.setattr(
            kanban_db, "_new_task_id", lambda: state.current["kanban_task_id"]
        )
        task_id, status = projection._project_task(
            state.generation,
            decision,
            state.current["dependency_admission"],
            state.current,
        )
    assert task_id == state.current["kanban_task_id"]
    assert status == "ready"
    calls = []
    preflights = []

    def provider(profile_name):
        preflights.append("provider")
        return _ready_executor_provider_payload(profile_name)

    def credentials(_projection, *, enabled=True):
        preflights.append("credentials")
        return _ready_worker_credential_probe()

    def spawn(task, workspace, **kwargs):
        assert (
            pr.load_historical_execution_start_record(
                projection_record=state.historical
            )
            == state.old
        )
        assert (
            pr.load_p18_9_0_execution_start_record(projection_record=state.current)[
                "kanban_task_id"
            ]
            == task.id
        )
        calls.append(task.id)
        assert task.id == state.current["kanban_task_id"]
        assert Path(workspace).is_relative_to(state.home)
        return os.getpid()

    def forbidden(*args, **kwargs):
        pytest.fail(
            "C51 isolated start must not invoke subprocesses/Git or real workers"
        )

    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(
        pr,
        "_run_source_authority_git",
        lambda *args: subprocess.CompletedProcess(
            args, 1, "", "isolated filesystem fixture"
        ),
    )
    monkeypatch.setattr(pr, "_executor_provider_readiness", provider)
    monkeypatch.setattr(
        pr, "_preflight_pepper_governed_worker_credentials", credentials
    )
    # No real profile credentials are captured or passed to the controlled spawn.
    monkeypatch.setattr(
        pr, "_pepper_governed_worker_env_overlay", lambda projection: {}
    )
    monkeypatch.setattr(kanban_db, "_default_spawn", spawn)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    state.calls = calls
    state.preflights = preflights
    return state


def _registered_start(state):
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    return json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "human_authorization_text": f"Start {state.generation['ticket_id']} execution now",
                "ticket_id": state.generation["ticket_id"],
            },
        )
    )


def test_c51_proven_supersession_read_is_nonmutating(current_revision):
    state = current_revision
    assert (
        pr.load_p18_9_0_execution_start_record(projection_record=state.current) is None
    )
    assert state.path.read_bytes() == state.old_bytes
    assert not pr.execution_start_history_path_for_ticket(
        state.generation["ticket_id"]
    ).exists()


def test_c51_archive_failure_prevents_replacement_and_dispatch(
    startable_revision, monkeypatch
):
    state = startable_revision

    def fail_archive(*args, **kwargs):
        raise OSError("isolated archive write failure")

    monkeypatch.setattr(pr, "_append_authority_history", fail_archive)
    result = _registered_start(state)
    assert result.get("success") is False, result
    assert not state.calls
    assert state.path.read_bytes() == state.old_bytes
    assert (
        pr.load_p18_9_0_execution_start_record(projection_record=state.historical)
        == state.old
    )


def test_c51_registered_start_preserves_history_and_current_idempotency(
    startable_revision,
):
    from hermes_cli import kanban_db

    state = startable_revision
    result = _registered_start(state)
    assert result["success"] is True, result
    assert result["execution_started"] is True, json.dumps(
        pr.build_workflow_control_snapshot().get("remaining_blockers")
    )
    assert result["dispatch_performed"] is True
    assert result["idempotent_replay"] is False
    assert state.calls == [state.current["kanban_task_id"]]
    assert state.preflights == ["provider", "credentials"]
    current_start = pr.load_p18_9_0_execution_start_record(
        projection_record=state.current
    )
    for key in (
        "ticket_id",
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
        "projection_SHA256",
        "kanban_task_id",
    ):
        assert current_start[key] == state.current[key]
        if key != "projection_SHA256":
            assert result[key] == current_start[key]
    assert result["Git_mutation"] is False
    history_path = pr.execution_start_history_path_for_ticket(
        state.generation["ticket_id"]
    )
    history_bytes = history_path.read_bytes()
    entries = [json.loads(line) for line in history_bytes.splitlines()]
    assert len(entries) == 1
    assert entries[0]["record"] == state.old
    assert entries[0]["record_text"].encode() == state.old_bytes
    assert (
        pr.load_historical_execution_start_record(projection_record=state.historical)
        == state.old
    )
    replay = _registered_start(state)
    assert replay["success"] is True, replay
    assert replay["idempotent_replay"] is True, replay
    assert replay["kanban_run_id"] == result["kanban_run_id"]
    assert state.calls == [state.current["kanban_task_id"]]
    assert history_path.read_bytes() == history_bytes
    with kanban_db.connect(board=state.current["kanban_board_slug"]) as conn:
        assert len(kanban_db.list_runs(conn, state.current["kanban_task_id"])) == 1


@pytest.mark.parametrize(
    "damage",
    [
        "bad_digest",
        "different_ticket",
        "broken_revision_chain",
        "unbound_historical_projection",
        "work_packet_id",
        "work_packet_SHA256",
        "projection_SHA256",
        "kanban_task_id",
        "corrupted_revision_history",
        "corrupted_execution_history",
    ],
)
def test_c51_unproven_mismatch_never_dispatches_or_replaces_authority(
    startable_revision, damage
):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

    state = startable_revision
    history_path = pr.execution_start_history_path_for_ticket(
        state.generation["ticket_id"]
    )
    if damage in ("broken_revision_chain", "corrupted_revision_history"):
        path = bridge.current_ticket_material_revision_history_path_for_ticket(
            state.generation["ticket_id"]
        )
        if damage == "broken_revision_chain":
            entries = path.read_text().splitlines()
            path.write_text(entries[-1] + "\n")
        else:
            path.write_text("{invalid json}\n")
    elif damage == "corrupted_execution_history":
        history_path.write_text("{invalid json}\n")
    else:
        record = dict(state.old)
        if damage == "bad_digest":
            record["start_authorization_SHA256"] = "0" * 64
        else:
            field = {
                "different_ticket": "ticket_id",
                "unbound_historical_projection": "approval_publication_SHA256",
            }.get(damage, damage)
            record[field] = "0" * 64 if "SHA256" in field else "unrelated-authority"
            record["start_authorization_SHA256"] = pr._execution_start_record_digest(
                record
            )
        state.path.write_text(json.dumps(record))
    slot_before = state.path.read_bytes()
    history_before = history_path.read_bytes() if history_path.exists() else None
    result = _registered_start(state)
    assert result.get("execution_started", False) is False, result
    assert result.get("dispatch_performed", False) is False, result
    assert (
        result.get("success") is False
        or result.get("blocker_code") == "EXECUTION_START_AUTHORITY_STALE"
    ), result
    assert not state.calls
    assert not state.preflights
    assert state.path.read_bytes() == slot_before
    assert (
        history_path.read_bytes() if history_path.exists() else None
    ) == history_before


@pytest.mark.parametrize("gate", ["workflow", "task", "provider", "credentials"])
def test_c51_supersession_does_not_bypass_current_start_preflight(
    startable_revision, monkeypatch, gate
):
    state = startable_revision
    if gate == "workflow":
        monkeypatch.setattr(
            pr,
            "_execution_start_workflow_blocker",
            lambda workflow: ("TEST_WORKFLOW_GAP", "isolated gate"),
        )
    elif gate == "task":
        monkeypatch.setattr(
            pr,
            "_kanban_start_preflight_blocker",
            lambda projection: ("TEST_TASK_GAP", "isolated gate"),
        )
    elif gate == "provider":
        monkeypatch.setattr(
            pr,
            "_executor_provider_readiness",
            lambda profile: {"ok": False, "blocker_code": "TEST_PROVIDER_GAP"},
        )
    else:
        monkeypatch.setattr(
            pr,
            "_preflight_pepper_governed_worker_credentials",
            lambda *a, **k: {"ok": False, "blocker_code": "TEST_CREDENTIAL_GAP"},
        )
    result = _registered_start(state)
    assert result["blocker_code"].startswith("TEST_"), result
    assert result["execution_started"] is False
    assert result["dispatch_performed"] is False
    assert not state.calls
    assert state.path.read_bytes() == state.old_bytes
    assert not pr.execution_start_history_path_for_ticket(
        state.generation["ticket_id"]
    ).exists()
