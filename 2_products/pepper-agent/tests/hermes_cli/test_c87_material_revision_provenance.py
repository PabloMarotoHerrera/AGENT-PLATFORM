"""Real persisted revision envelopes, isolated from the live governed home."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from hermes_cli.agent_platform import material_revision_provenance as provenance
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import retry_material_revision
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow, projection_home as projection_home,
)
from tests.hermes_cli.test_c67_successive_recovery_cycles import advance
from tests.hermes_cli.test_c73_post_accept_material_revision import accepted as accepted


def revise(flow):
    retry_material_revision.request(**flow.args)
    return pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "validation_steps": flow.record["ticket_spec"]["validation_steps"]},
        ticket_id="P99.4", next_action_id="REVISE_P99_4",
    )


@pytest.fixture
def revised(flow):
    revise(flow)
    return bridge.load_generation_record(ticket_id="P99.4")


def inspect(**kwargs):
    return provenance.inspect(ticket_id="P99.4", revision=2, **kwargs)


def write(record):
    # Deliberate disk corruption bypasses production persistence validation.
    bridge.generation_record_path_for_ticket("P99.4").write_text(json.dumps(record))


def snapshot(home):
    return {str(p): p.read_bytes() for p in Path(home).rglob("*") if p.is_file()}


def test_persisted_authority_and_publication_lineage(revised):
    got = inspect(expected_authority_sha256=revised["revision_authority_SHA256"])
    assert got["status"] == "PROVEN"
    assert got["classification"] == "PATH_A_EXISTING_PROVENANCE"
    assert (got["source_revision"], got["target_revision"]) == (1, 2)
    assert got["authorization_text"] == "I explicitly authorize revision of P99.4."
    assert got["authorization_text_sha256"] == hashlib.sha256(got["authorization_text"].encode()).hexdigest()
    assert got["publication_id"] == revised["ticket_publication_result"]["publication"]["publication_id"]
    assert got["ticket_spec_sha256"] == revised["ticket_spec_SHA256"]
    assert got["work_packet_sha256"] == revised["work_packet_SHA256"]
    assert got["record_integrity_sha256"] == revised["bridge_SHA256"]
    assert len(got["source_records"]) == 2


def test_expected_contract_is_never_proof(flow):
    # A real generation with a human validation contract has no revision event.
    got = provenance.inspect(ticket_id="P99.4", revision=1, expected_authority_sha256="a" * 64)
    assert got["status"] == "MISSING"
    assert "authorization_text" not in got


def test_missing_generation(projection_home):
    assert inspect(expected_authority_sha256="a" * 64)["status"] == "MISSING"


def test_contract_retaining_exact_expected_values_cannot_replace_lost_authority(revised):
    expected = revised["revision_authority_SHA256"]
    assert expected in json.dumps(revised["ticket_spec"]["validation_steps"])
    revised.pop("revision_authority")
    revised.pop("revision_authority_SHA256")
    revised["bridge_SHA256"] = bridge._record_digest(revised)
    write(revised)
    bridge.current_ticket_material_revision_history_path_for_ticket("P99.4").unlink()
    got = inspect(expected_authority_sha256=expected)
    assert got["status"] == "MISSING"
    assert "authorization_text" not in got


def test_authority_mismatch(revised):
    assert inspect(expected_authority_sha256="a" * 64)["status"] == "AUTHORITY_MISMATCH"


@pytest.mark.parametrize("field", ["text", "authority_hash", "publication", "spec", "work_packet", "sequence", "timestamp"])
def test_corruption_fails_closed(revised, field):
    record = deepcopy(revised)
    if field == "text":
        record["revision_authority"]["human_authorization_text"] += " changed"
    elif field == "authority_hash":
        record["revision_authority_SHA256"] = "a" * 64
    elif field == "publication":
        record["ticket_publication_result"]["publication"]["canonical_ticket"]["title"] += " altered"
    elif field == "spec":
        record["ticket_spec_SHA256"] = "a" * 64
    elif field == "work_packet":
        record["work_packet_id"] += "X"
    elif field == "sequence":
        record["revision_sequence"] += 1
    else:
        record["created_at"] = "not a timestamp"
    record["bridge_SHA256"] = bridge._record_digest(record)
    write(record)
    # Remove the duplicate source so detection must validate the envelope itself.
    bridge.current_ticket_material_revision_history_path_for_ticket("P99.4").unlink()
    assert inspect()["status"] == "INCONSISTENT"


def test_public_surface_readonly_deterministic_and_no_attestation(revised, projection_home):
    from tools import pepper_workflow_tools as tools
    before = snapshot(projection_home)
    args = {"ticket_id": "P99.4", "revision": 2, "provenance_only": True}
    first = json.loads(tools._inspect_current_ticket_manual_validation(args))
    second = json.loads(tools._inspect_current_ticket_manual_validation(args))
    assert first == second
    evidence = first["manual_validation"]["material_revision_provenance"]
    assert evidence["status"] == "PROVEN"
    assert evidence["human_attestation_required"]
    assert not evidence["validation_attested"]
    assert not evidence["auto_validation"]
    assert snapshot(projection_home) == before
    assert len(json.dumps(first)) < 6000


def test_duplicate_history_is_unambiguous(revised):
    path = bridge.current_ticket_material_revision_history_path_for_ticket("P99.4")
    raw = path.read_text()
    expected = inspect()
    path.write_text(raw + raw)
    assert inspect() == expected


def test_competing_revision_is_rejected(revised):
    record = deepcopy(revised)
    record["created_at"] = "2026-10-07T00:00:00Z"
    record["bridge_SHA256"] = bridge._record_digest(record)
    write(record)
    assert inspect()["status"] == "INCONSISTENT"


@pytest.mark.parametrize("ticket,revision", [("P99.5", 2), ("P99.4", 99)])
def test_unrelated_identity_cannot_supply_proof(revised, ticket, revision):
    assert provenance.inspect(ticket_id=ticket, revision=revision)["status"] == "MISSING"


def test_history_tampering(revised):
    path = bridge.current_ticket_material_revision_history_path_for_ticket("P99.4")
    entry = json.loads(path.read_text())
    entry["human_authorization_text"] += " tampered"
    # Even a rehashed history must match its accepted authority.
    entry["revision_SHA256"] = bridge._revision_history_record_digest(entry)
    path.write_text(json.dumps(entry) + "\n")
    assert inspect()["status"] == "INCONSISTENT"


def test_history_append_failure_retains_atomic_provenance(flow, monkeypatch):
    def fail(*args):
        raise OSError("isolated append failure")
    monkeypatch.setattr(bridge, "_append_current_ticket_material_revision_history_entry", fail)
    with pytest.raises(OSError, match="isolated append failure"):
        revise(flow)
    got = inspect()
    assert got["status"] == "PROVEN"
    assert got["transition_timestamp"]
    assert got["source_revision"] == 1
    assert len(got["source_records"]) == 1


def test_failed_atomic_replace_keeps_previous_generation(flow, monkeypatch):
    path = bridge.generation_record_path_for_ticket("P99.4")
    before = path.read_bytes()
    original = Path.replace
    def fail(self, target):
        if Path(target) == path:
            raise OSError("isolated replace failure")
        return original(self, target)
    monkeypatch.setattr(Path, "replace", fail)
    with pytest.raises(OSError, match="isolated replace failure"):
        revise(flow)
    assert path.read_bytes() == before
    assert inspect()["status"] == "MISSING"


def test_corrupt_envelope_cannot_cross_atomic_boundary(revised):
    path = bridge.generation_record_path_for_ticket("P99.4")
    before = path.read_bytes()
    revised["revision_authority"]["human_authorization_text"] += " forged"
    with pytest.raises(ValueError):
        bridge._write_json_atomic(path, revised)
    assert path.read_bytes() == before


def test_past_revision_inspectable_after_successor(flow, monkeypatch):
    newer = advance(flow, monkeypatch)
    got = inspect()
    assert got["status"] == "PROVEN"
    # Advance once more through a separately authorized recovery/revision cycle.
    from tests.hermes_cli.test_c67_successive_recovery_cycles import recover
    newer.args["recovery_action_SHA256"] = recover()["recovery_action_SHA256"]
    advance(newer, monkeypatch)
    past = inspect()
    assert past["status"] == "PROVEN"
    assert past["record_integrity_sha256"] == got["record_integrity_sha256"]


@pytest.mark.parametrize("revision", [0, -1, True, "2"])
def test_invalid_revision_is_bounded(projection_home, revision):
    assert provenance.inspect(ticket_id="P99.4", revision=revision)["status"] == "INCONSISTENT"


def test_history_bound_fails_closed(revised, monkeypatch):
    monkeypatch.setattr(provenance, "MAX_BYTES", 32)
    assert inspect()["status"] == "INCONSISTENT"


@pytest.mark.parametrize("raw", ["[]", "null", "{bad json"])
def test_malformed_history_fails_closed(revised, raw):
    bridge.current_ticket_material_revision_history_path_for_ticket("P99.4").write_text(raw)
    assert inspect()["status"] == "INCONSISTENT"


def test_proof_for_other_workpacket_cannot_satisfy_current_validation(revised, flow, monkeypatch):
    # Current validation still binds the previous WorkPacket. A separately
    # inspected new revision must not be presented as proof for that candidate.
    monkeypatch.setattr(pr, "_load_current_projection_record", lambda: flow.projection)
    monkeypatch.setattr(pr, "_current_manual_validation_context", lambda p: {"items": []})
    got = pr.inspect_current_ticket_manual_validation()["material_revision_provenance"]
    assert got["status"] == "AUTHORITY_MISMATCH"
    assert got["classification"] == "MATERIAL_REVISION_VALIDATION_BINDING_MISMATCH"
    assert inspect()["status"] == "PROVEN"


@pytest.mark.parametrize("accepted", [4], indirect=True)
def test_post_accept_r4_to_r5_uses_same_general_provenance_contract(accepted):
    from hermes_cli.agent_platform import post_accept_material_revision as rev
    rev.request(**accepted.args)
    pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        revision_contract={"ticket_id": "P99.4", "validation_steps": accepted.generation["ticket_spec"]["validation_steps"]},
        ticket_id="P99.4", next_action_id="REVISE_P99_4",
    )
    got = provenance.inspect(ticket_id="P99.4", revision=5)
    assert got["status"] == "PROVEN"
    assert (got["source_revision"], got["target_revision"]) == (4, 5)
    assert got["revision_reason"] == "post_accept_pre_git_material_revision"
    assert got["source_publication_id"] == "PUB-P99-4-0004"
    assert got["publication_id"] == "PUB-P99-4-0005"
    assert not got["validation_attested"]
