"""Independent legacy final-read/approval oracles also used in disposable mutants."""
from copy import deepcopy
from tests.hermes_cli.har14_read_helpers import *


def test_valid_digest_does_not_substitute_approval(routed):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    import json
    path = bridge.approval_decision_record_path_for_ticket(routed.p["ticket_id"])
    record = json.loads(path.read_text())
    record["status"] = "rejected"
    record["approval_publication_SHA256"] = bridge._approval_decision_record_digest(record)
    path.write_text(json.dumps(record))  # isolated adversarial fixture preparation
    before = files(routed)
    # Selection may reject first, before the direct approval loader. Preserve
    # that original ordering; a valid checksum never makes the body available.
    with pytest.raises((ValueError, bridge.TicketArchitectBridgeConflict)):
        read(routed)
    assert files(routed) == before
    assert not routed.owner.observations


def test_original_stale_approval_cannot_follow_new_generation(routed, monkeypatch):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    original = bridge.load_approval_decision_record
    evaluator = qualification.evaluate
    def after_admission(*a, **k):
        result = evaluator(*a, **k)
        def changed(**kwargs):
            record = deepcopy(original(**kwargs))
            record["approval_publication_SHA256"] = "changed"
            return record
        monkeypatch.setattr(bridge, "load_approval_decision_record", changed)
        return result
    monkeypatch.setattr(qualification, "evaluate", after_admission)
    with pytest.raises(ValueError, match="changed during inspection"):
        read(routed)
    assert not routed.owner.observations
