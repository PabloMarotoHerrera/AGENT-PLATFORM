"""Exact public C93 parity and a single controlled read/evaluation path."""
import json
from copy import deepcopy
from tests.hermes_cli.har14_read_helpers import *


def test_mechanical_positive_exact_direct_and_tool(routed):
    from tools import pepper_workflow_tools as tools
    f = routed
    before = files(f)
    assert read(f, max_chars=20000) == f.default
    result = json.loads(tools._inspect_pending_approval_artifact_section({"authority_scope": "current_approved",
        "approval_id": f.p["ticket_id"], "section_id": "validation_steps", "max_chars": 20000}))
    assert result == {"success": True, "source_tool": "inspect_pending_approval_artifact_section", **f.default}
    assert files(f) == before and not f.launched
    q = f.owner.observations[-1]
    assert q.proof_level == "MECHANICAL_SYNTHETIC_ONLY"
    assert q.issuer_proof == "TRUSTED_ISSUER_PROOF_PENDING"
    assert not q.grants_authority and not q.authorizes_execution


def test_default_legacy_and_sibling_do_not_qualify(defective, monkeypatch):
    def forbidden(*a, **k):
        raise AssertionError("unexpected HAR qualification")
    monkeypatch.setattr(qualification.C93ReadQualificationOwner, "_prepare", forbidden)
    assert read(defective)["validated"]
    token = inspection._READ_ROUTE.set(object())
    try:
        result = inspection.inspect(ticket_id=defective.p["ticket_id"], section_id="ticket_spec", max_chars=20000)
        assert result["section_id"] == "ticket_spec"
    finally:
        inspection._READ_ROUTE.reset(token)


@pytest.mark.parametrize("params", [{}, {"max_chars": 1000}, {"max_chars": "1000"},
    {"max_chars": True}, {"max_chars": 1e4}, {"max_chars": 999999}, {"chunk_index": 0},
    {"chunk_index": None}, {"max_chars": None}])
def test_parameters_and_serialization_parity(routed, params):
    f = routed
    token = inspection._READ_ROUTE.set(None)
    try:
        expected = read(f, **params)
    finally:
        inspection._READ_ROUTE.reset(token)
    assert read(f, **params) == expected


@pytest.mark.parametrize("params", [{"chunk_index": True}, {"chunk_index": -1},
    {"chunk_index": "0"}, {"max_chars": "bad"}, {"expected_binding": {} }])
def test_error_type_text_and_short_circuit_parity(routed, params):
    f = routed
    token = inspection._READ_ROUTE.set(None)
    try:
        with pytest.raises(Exception) as legacy:
            read(f, **params)
    finally:
        inspection._READ_ROUTE.reset(token)
    with pytest.raises(type(legacy.value)) as candidate:
        read(f, **params)
    assert str(candidate.value) == str(legacy.value)
    assert not f.owner.observations


def test_one_capture_evaluation_and_final_sequence(routed, monkeypatch):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    from hermes_cli.agent_platform import product_runtime as pr
    trace = []
    for obj, name in [(bridge, "load_generation_record"), (bridge, "load_approval_decision_record"),
                      (pr, "_current_incomplete_generation_record_from_records")]:
        original = getattr(obj, name)
        def wrap(*a, _name=name, _original=original, **k):
            trace.append(_name)
            return _original(*a, **k)
        monkeypatch.setattr(obj, name, wrap)
    token = inspection._READ_ROUTE.set(None)
    try:
        expected = read(routed, max_chars=20000)
    finally:
        inspection._READ_ROUTE.reset(token)
    baseline_trace = tuple(trace)
    trace.clear()
    calls = []
    evaluator = qualification.evaluate
    def evaluate(*a, **k):
        calls.append((a, k))
        return evaluator(*a, **k)
    monkeypatch.setattr(qualification, "evaluate", evaluate)
    assert read(routed, max_chars=20000) == expected
    assert tuple(trace) == baseline_trace
    assert len(routed.captures) == len(calls) == len(routed.owner.observations) == 1
    value, kwargs = calls[0][0][0], calls[0][1]
    assert kwargs["qualification"].input == value.content_identity()
    assert all(p.observation.currentness.value == "UNVERIFIED" for p in value.prerequisites)
    assert set(p.requirement for p in value.prerequisites) == qualification.PREREQUISITES


def test_final_original_revalidation_drift(routed, monkeypatch):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    original = bridge.load_generation_record
    n = 0
    def changed(**kwargs):
        nonlocal n
        value = original(**kwargs)
        if not kwargs.get("allow_terminal_rejected_historical"):
            n += 1
            if n >= 2:
                value = deepcopy(value)
                value["bridge_SHA256"] = "changed"
        return value
    monkeypatch.setattr(bridge, "load_generation_record", changed)
    with pytest.raises(ValueError, match="changed during inspection"):
        read(routed)
    assert not routed.owner.observations and not routed.owner._active


def test_public_callers_cannot_supply_credentials(routed):
    for name in ("qualification", "qualified_evaluation", "issuer", "allow", "route"):
        with pytest.raises(TypeError, match="unexpected keyword"):
            read(routed, **{name: "ALLOW"})
    assert not routed.owner.observations


@pytest.mark.parametrize("change", ["missing_generation", "missing_approval", "rejected", "corrupt"])
def test_original_record_rejections_also_stop_selected_route(routed, change):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    generation_path = bridge.generation_record_path_for_ticket(routed.p["ticket_id"])
    approval_path = bridge.approval_decision_record_path_for_ticket(routed.p["ticket_id"])
    if change == "missing_generation":
        generation_path.unlink()
    elif change == "missing_approval":
        approval_path.unlink()
    elif change == "rejected":
        generation = json.loads(generation_path.read_text())
        approval_path.write_text(json.dumps(bridge._build_approval_decision_record(
            generation, decision="reject", actor="isolated-human", decided_at=None)))
    else:
        generation_path.write_text("not JSON")
    before = files(routed)
    with pytest.raises((ValueError, bridge.TicketArchitectBridgeConflict)):
        read(routed)
    assert files(routed) == before and not routed.owner.observations


def test_unicode_chunks_have_original_full_digest_and_single_use_per_page(routed):
    import hashlib
    full = routed.default["exact_body"]
    assert "漢字" in json.dumps(full, ensure_ascii=False)
    first = read(routed, max_chars=1000)
    pages = [first]
    for index in range(1, first["pagination"]["total_chunks"]):
        pages.append(read(routed, max_chars=1000, chunk_index=index, expected_binding=first["artifact_binding"]))
    text = "".join(page["exact_body"] for page in pages)
    assert json.loads(text) == full
    assert hashlib.sha256(text.encode()).hexdigest() == first["exact_body_serialized_SHA256"]
    ids = [q.invocation_binding.sha256 for q in routed.owner.observations]
    assert len(ids) == len(set(ids)) == len(pages)
