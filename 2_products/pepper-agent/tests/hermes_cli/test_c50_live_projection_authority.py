"""Regression captured read-only from durable Pepper state at 7169c70.

The fixture preserves all 81 authority records byte-for-byte, including R0005's
projection, rejected/corrected generations, R0007 approval, and predecessor
completion evidence. It excludes credentials, sessions and the live database.
"""

import gzip
import hashlib
import json
from pathlib import Path

import pytest

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)


@pytest.fixture
def live_authority(tmp_path, monkeypatch):
    home = tmp_path / "hermes"
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.setenv("HERMES_KANBAN_HOME", str(home))
    fixture = Path(__file__).parents[1] / "fixtures/c50_live_authority.json.gz"
    records = json.loads(gzip.decompress(fixture.read_bytes()))
    manifest = json.loads(records.pop("manifest.json"))
    for name, data in records.items():
        assert hashlib.sha256(data.encode()).hexdigest() == manifest[name]
        path = home / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
    return home


def test_c50_live_shape_current_projection_is_not_the_old_revision(live_authority):
    authority = pr._current_approved_generation_authority_from_records()
    generation = authority["generation_record"]
    assert generation["ticket_id"] == "P18.9.5"
    assert generation["revision_sequence"] == 7
    # A valid superseded R0005 projection is historical, not an invalid R0007.
    assert (
        projection.load_kanban_projection_record(
            ticket_id=generation["ticket_id"],
            generation_record=generation,
            decision_record=authority["approval_decision_record"],
        )
        is None
    )


def test_c50_live_shape_snapshot_does_not_expose_bootstrap_as_current(live_authority):
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["current_ticket_id"] == "P18.9.5"
    assert snapshot["workflow_status"] == "ticket_approved"
    assert not snapshot.get("kanban_projection_authority")
    assert snapshot.get("P18_9_kanban_projection_present") is False


def test_c50_registered_prepare_preserves_boundaries_and_history(
    live_authority, monkeypatch
):
    from types import SimpleNamespace
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Execution, worker dispatch or subprocess/Git invocation during preparation"
        )

    import subprocess

    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(pr, "_dispatch_exact_current_kanban_task", forbidden)
    monkeypatch.setattr(pr, "start_current_ticket_execution", forbidden)
    worker_root = live_authority / "agent-platform/pepper-worker-start-action"
    worker_before = {p.name: p.read_bytes() for p in worker_root.iterdir()}
    profile_path = live_authority / "profiles/pepper-implementation-product"
    profile_path.mkdir(parents=True)
    (profile_path / "config.yaml").write_text(
        "model:\n  provider: openai-codex\n  default: gpt-5.5\n  api_mode: codex_responses\n"
        "platform_toolsets:\n  cli:\n    - pepper_repository\n    - file\n    - no_mcp\n"
    )
    profile = SimpleNamespace(
        name="pepper-implementation-product",
        description="Pepper frontend product implementation execution profile",
        is_default=False,
        path=profile_path,
    )
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])
    authority = pr._current_approved_generation_authority_from_records()
    generation = authority["generation_record"]
    ticket = generation["ticket_id"]
    old_path = projection.kanban_projection_record_path_for_ticket(ticket)
    old_bytes = old_path.read_bytes()
    bootstrap_path = projection.kanban_projection_record_path()
    bootstrap_bytes = bootstrap_path.read_bytes()
    original_project = projection.project_current_approved_workpacket_to_kanban
    original_resolve = projection.resolve_current_approved_workpacket_projection
    original_load_generation = projection.load_generation_record
    original_load_projection = projection.load_kanban_projection_record
    trace = [
        (
            "C",
            ticket,
            generation["ticket_spec_SHA256"],
            generation["work_packet_SHA256"],
        )
    ]
    active = False

    def row(label, value):
        return (
            label,
            value["ticket_id"],
            value["ticket_spec_SHA256"],
            value["work_packet_SHA256"],
        )

    def project(**kwargs):
        nonlocal active
        workflow = kwargs["workflow"]
        trace.append(
            row(
                "D",
                dict(
                    workflow["generated_ticket_authority"],
                    ticket_id=workflow["current_ticket_id"],
                ),
            )
        )
        active = True
        try:
            return original_project(**kwargs)
        finally:
            active = False

    def resolve(**kwargs):
        result = original_resolve(**kwargs)
        trace.append(row("E", result))
        return result

    def load_generation(**kwargs):
        result = original_load_generation(**kwargs)
        if active:
            trace.append(row("F", result))
        return result

    def load_projection(**kwargs):
        if active and kwargs.get("generation_record"):
            trace.append(row("G", kwargs["generation_record"]))
        return original_load_projection(**kwargs)

    monkeypatch.setattr(
        projection, "project_current_approved_workpacket_to_kanban", project
    )
    monkeypatch.setattr(
        projection, "resolve_current_approved_workpacket_projection", resolve
    )
    monkeypatch.setattr(projection, "load_generation_record", load_generation)
    monkeypatch.setattr(projection, "load_kanban_projection_record", load_projection)
    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_execution",
            {
                "human_request_text": "Prepare the current approved ticket execution.",
            },
        )
    )
    assert result["success"] is True, result
    assert result["idempotent_replay"] is False
    assert result["projection_status"] == "projected"
    current = projection.load_kanban_projection_record(ticket_id=ticket)
    for key in (
        "ticket_id",
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
    ):
        assert result[key] == current[key] == generation[key]
    assert set(item[0] for item in trace) == set("CDEFG")
    assert all(item[1:] == trace[0][1:] for item in trace), trace
    assert current["kanban_task_id"] != json.loads(old_bytes)["kanban_task_id"]
    for key in (
        "dispatch_performed",
        "worker_execution",
        "execution_started",
        "Kanban_dispatch",
        "Git_mutation",
    ):
        assert result[key] is False
    assert {p.name: p.read_bytes() for p in worker_root.iterdir()} == worker_before
    context = pr.build_lead_agent_operational_context()
    assert context["active_execution_count"] == 0
    assert bootstrap_path.read_bytes() == bootstrap_bytes
    bootstrap_authority = (
        bridge.load_historical_approved_predecessor_generation_authority(
            ticket_id="P18.9.0"
        )
    )
    assert (
        projection.load_kanban_projection_record(
            ticket_id="P18.9.0",
            generation_record=bootstrap_authority["generation_record"],
            decision_record=bootstrap_authority["approval_decision_record"],
            allow_terminal_completed_predecessor_historical=True,
        )["ticket_id"]
        == "P18.9.0"
    )
    history = [
        json.loads(line)
        for line in bridge.current_ticket_material_revision_history_path_for_ticket(
            ticket
        )
        .read_text()
        .splitlines()
    ]
    old_authority = history[0]
    archived = projection.load_kanban_projection_record(
        ticket_id=ticket,
        generation_record=old_authority["historical_current_generation_record"],
        decision_record=old_authority["historical_approved_decision_record"],
        allow_terminal_completed_predecessor_historical=True,
    )
    assert archived == json.loads(old_bytes)
    snapshot = pr.build_workflow_control_snapshot()
    assert (
        snapshot["kanban_projection_authority"]["work_packet_SHA256"]
        == generation["work_packet_SHA256"]
    )
    replay = json.loads(
        handle_function_call(
            "prepare_current_ticket_execution",
            {
                "human_request_text": "Prepare the current approved ticket execution.",
            },
        )
    )
    assert replay["success"] is True, replay
    assert replay["kanban_task_id"] == current["kanban_task_id"]


@pytest.mark.parametrize(
    "damage",
    [
        "projection_digest",
        "projection_identity",
        "history_digest",
        "broken_chain",
        "current_decision",
        "requested_ticket",
    ],
)
def test_c50_invalid_authority_still_fails_closed(live_authority, damage):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

    authority = pr._current_approved_generation_authority_from_records()
    generation = authority["generation_record"]
    ticket = generation["ticket_id"]
    path = projection.kanban_projection_record_path_for_ticket(ticket)
    if damage.startswith("projection_"):
        record = json.loads(path.read_text())
        record["ticket_spec_SHA256"] = "0" * 64
        if damage == "projection_identity":
            record["projection_SHA256"] = projection._projection_record_digest(record)
        path.write_text(json.dumps(record))
    elif damage in ("history_digest", "broken_chain"):
        path = bridge.current_ticket_material_revision_history_path_for_ticket(ticket)
        entries = [json.loads(line) for line in path.read_text().splitlines()]
        if damage == "history_digest":
            entries[0]["revision_SHA256"] = "0" * 64
        else:
            entries = entries[1:]
        path.write_text("\n".join(json.dumps(entry) for entry in entries) + "\n")
    elif damage == "requested_ticket":
        ticket = "P99.9"
        projection.kanban_projection_record_path_for_ticket(ticket).write_bytes(path.read_bytes())
    else:
        authority["approval_decision_record"]["approval_publication_SHA256"] = "0" * 64
    with pytest.raises((
        projection.WorkPacketKanbanProjectionConflict,
        bridge.TicketArchitectBridgeConflict,
    )):
        projection.load_kanban_projection_record(
            ticket_id=ticket,
            generation_record=generation,
            decision_record=authority["approval_decision_record"],
        )
