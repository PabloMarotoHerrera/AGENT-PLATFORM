"""Inspect real isolated durable approvals, never a reconstructed contract."""

from copy import deepcopy
import hashlib
import json

import pytest

from hermes_cli.agent_platform import approved_artifact_inspection as inspection
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tools import pepper_workflow_tools as tools
from tests.hermes_cli.test_c92_post_execution_material_revision import (
    flow, projection_home, evidence, completed, terminal, contract, defective,
    request, MISSING, ACTUAL,
)


def read(f, **kwargs):
    return inspection.inspect(ticket_id=f.p["ticket_id"], section_id="validation_steps", **kwargs)


def files(f):
    return {str(p.relative_to(f.home)): p.read_bytes() for p in f.home.rglob("*") if p.is_file()}


def test_exact_approved_body_and_steps_zero_mutation(defective):
    f = defective
    before = files(f)
    result = read(f, max_chars=20000)
    decision = bridge.load_approval_decision_record(ticket_id=f.p["ticket_id"])
    body = decision["ticket_publication_result"]["publication"]["canonical_ticket"]
    assert result["exact_body"] == body["validation_steps"]
    assert [v["validation_id"] for v in result["exact_body"]] == [f"V{i}" for i in range(1, 13)]
    assert any(v.get("command") is None for v in result["exact_body"])
    full = inspection.inspect(ticket_id=f.p["ticket_id"], section_id="ticket_spec", max_chars=20000)
    assert full["exact_body"] == body
    assert read(f, expected_binding=result["artifact_binding"], max_chars=20000) == result
    assert files(f) == before
    assert not f.launched


@pytest.mark.parametrize("key", ["project_id", "ticket_id", "revision", "ticket_spec_SHA256", "work_packet_id",
                                 "work_packet_SHA256", "bridge_SHA256", "publication_id", "publication_artifact_SHA256",
                                 "approval_publication_SHA256", "approval_publication_id", "approval_SHA256"])
def test_wrong_binding_fails_closed(defective, key):
    binding = read(defective)["artifact_binding"]
    binding[key] = "wrong"
    before = files(defective)
    with pytest.raises(ValueError, match="binding mismatch"):
        read(defective, expected_binding=binding)
    assert files(defective) == before


def test_bounded_chunks_reassemble_exact_array(defective):
    f = defective
    first = read(f, max_chars=1000)
    assert first["pagination"]["chunked"]
    chunks = [read(f, max_chars=1000, chunk_index=i, expected_binding=first["artifact_binding"])
              for i in range(first["pagination"]["total_chunks"])]
    assert all(len(r["exact_body"]) <= 1000 for r in chunks)
    text = "".join(r["exact_body"] for r in chunks)
    assert json.loads(text) == f.record["ticket_spec"]["validation_steps"]
    assert hashlib.sha256(text.encode()).hexdigest() == first["exact_body_serialized_SHA256"]
    with pytest.raises(ValueError):
        read(f, chunk_index=-1)


@pytest.mark.parametrize("change", ["generation", "approval", "rejected", "pending"])
def test_corrupt_rejected_or_pending_authority_is_not_returned(defective, change):
    f = defective
    if change == "generation":
        path = bridge.generation_record_path_for_ticket(f.p["ticket_id"])
        record = json.loads(path.read_text())
        record["ticket_spec"]["validation_steps"][0]["description"] = "corrupt"
    else:
        path = bridge.approval_decision_record_path_for_ticket(f.p["ticket_id"])
        record = json.loads(path.read_text())
        if change == "pending":
            path.unlink()  # isolated fixture only: pending generation has no approval
            record = None
        elif change == "rejected":
            record = bridge._build_approval_decision_record(
                f.record, decision="reject", actor="isolated-human", decided_at=None)
        else:
            record["ticket_publication_result"]["publication"]["canonical_ticket"]["validation_steps"] = []
    if record is not None:
        path.write_text(json.dumps(record))
    before = files(f)
    with pytest.raises((ValueError, bridge.TicketArchitectBridgeConflict)):
        read(f)
    assert files(f) == before


def test_tool_is_bounded_path_safe_and_has_no_side_effect_authority(defective):
    f = defective
    args = {"authority_scope": "current_approved", "approval_id": f.p["ticket_id"],
            "section_id": "validation_steps", "max_chars": 1000}
    before = files(f)
    result = json.loads(tools._inspect_pending_approval_artifact_section(args))
    assert result["read_only"] and result["validated"]
    assert not any(result[k] for k in ["command_execution_authorized", "revision_authorized", "auto_approval", "Git_mutation"])
    for invalid in ({"path": str(f.home)}, {"approval_id": "../../secrets"}, {"section_id": "bridge_record"},
                    {"authority_scope": "unknown"}, {"command": "echo unauthorized"}):
        denied = json.loads(tools._inspect_pending_approval_artifact_section({**args, **invalid}))
        assert denied["success"] is False
        assert "exact_body" not in denied
    assert files(f) == before


@pytest.mark.parametrize("flow", [2], indirect=True)
def test_request_and_revise_unchanged_and_narrow_copy_validates(defective):
    f = defective
    request()
    workflow = pr.build_workflow_control_snapshot()
    before = files(f)
    result = read(f, max_chars=20000)
    assert result["artifact_binding"]["revision"] == "R0002"
    steps = deepcopy(result["exact_body"])
    for old, new in zip(MISSING, ACTUAL):
        steps[1]["command"] = steps[1]["command"].replace(old, new)
    original = result["exact_body"]
    assert [(i, k) for i, (a, b) in enumerate(zip(original, steps)) for k in a if a[k] != b[k]] == [(1, "command")]
    validated = bridge.validate_ticket_spec_material_revision_contract(
        {"ticket_id": f.p["ticket_id"], "validation_steps": steps}, target=bridge._target_from_record(f.record))
    assert [s.model_dump(mode="json") for s in validated.validation_steps] == steps
    after = pr.build_workflow_control_snapshot()
    for key in ("observed_at", "evidence_timestamp"):
        workflow.pop(key, None)
        after.pop(key, None)
    assert after == workflow
    assert workflow["next_action"]["id"] == "REVISE_P99_4"
    assert files(f) == before
    assert not f.launched


def test_real_pending_successor_cannot_substitute_old_approved_artifact(defective):
    f = defective
    binding = read(f)["artifact_binding"]
    request()
    pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "objective": "Isolated pending successor for artifact selection test."},
        ticket_id="P99.4", next_action_id="REVISE_P99_4")
    before = files(f)
    with pytest.raises(ValueError, match="approved decision"):
        read(f, expected_binding=binding)
    assert files(f) == before


def test_concurrent_authority_change_fails_closed(defective, monkeypatch):
    original = bridge.load_generation_record
    count = 0

    def changing(**kwargs):
        nonlocal count
        record = original(**kwargs)
        if kwargs.get("ticket_id") == defective.p["ticket_id"] and not kwargs.get("allow_terminal_rejected_historical"):
            count += 1
            if count >= 2:
                record = deepcopy(record)
                record["bridge_SHA256"] = "changed"
        return record

    monkeypatch.setattr(bridge, "load_generation_record", changing)
    with pytest.raises(ValueError, match="changed during inspection"):
        read(defective)


def test_public_response_cannot_be_silently_truncated(monkeypatch):
    monkeypatch.setattr(inspection, "inspect", lambda **kwargs: {"exact_body": "\\" * 20000})
    result = json.loads(tools._inspect_pending_approval_artifact_section({
        "authority_scope": "current_approved", "approval_id": "P99.4", "section_id": "validation_steps"}))
    assert result["success"] is False
    assert "exact_body" not in result
    assert "smaller max_chars" in result["error"]
