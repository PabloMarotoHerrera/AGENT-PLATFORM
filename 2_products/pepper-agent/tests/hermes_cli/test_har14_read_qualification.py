"""Invocation ownership is not authentication against hostile Python."""
import json
from copy import deepcopy
from dataclasses import replace
from tests.hermes_cli.har14_read_helpers import *


def test_strict_frozen_contract_and_versions(routed):
    from pydantic import ValidationError
    read(routed)
    q = routed.owner.observations[0]
    with pytest.raises(ValidationError):
        q.ticket_id = "other"
    for change in ({"schema_version": 2}, {"effect": "WRITE_ARTIFACT"},
                   {"capability": "O03.ticket_spec@1"}, {"trusted": True}):
        with pytest.raises(ValidationError):
            qualification.C93ReadQualification.model_validate({**q.model_dump(), **change})
    clone = qualification.C93ReadQualification.model_validate_json(q.model_dump_json())
    with pytest.raises(ValueError, match="foreign or consumed"):
        routed.owner._finish(clone, routed.captures[0])


@pytest.mark.parametrize("field", ["section", "ticket", "current", "approval"])
def test_capture_guard_ownership(routed, field):
    read(routed)
    capture = deepcopy(routed.captures[0])
    if field == "section":
        capture["request"]["section_id"] = "ticket_spec"
        message = "selected section mismatch"
    elif field == "ticket":
        capture["request"]["ticket_id"] = "wrong"
        message = "ticket binding mismatch"
    elif field == "current":
        capture["current"]["bridge_SHA256"] = "stale"
        message = "currentness unavailable"
    else:
        capture["decision"]["decision"] = "reject"
        message = "original approval required"
    with pytest.raises(ValueError, match=message):
        routed.owner._prepare(capture)


@pytest.mark.parametrize("change", ["seal", "foreign", "replay", "input", "request", "resource", "source"])
def test_finish_rejects_forgery_replay_and_drift(routed, monkeypatch, change):
    read(routed)
    capture = deepcopy(routed.captures[0])
    invocation = routed.owner._prepare(capture)
    try:
        if change == "seal":
            invocation.seal = object()
            message = "forged issuer"
        elif change == "foreign":
            invocation = replace(invocation)
            message = "foreign or consumed"
        elif change == "replay":
            routed.owner._finish(invocation, capture)
            message = "foreign or consumed"
        elif change == "input":
            invocation.input = invocation.input.model_copy(update={"authority_version": "changed"})
            message = "admission input changed"
        elif change == "request":
            capture["request"]["max_chars"] = 1001
            message = "parameters changed"
        elif change == "resource":
            monkeypatch.setenv("HERMES_HOME", str(routed.home / "other"))
            message = "resource context changed"
        else:
            monkeypatch.setattr(routed.owner, "_source", lambda: ((), routed.owner._implementation))
            message = "implementation source drift"
        with pytest.raises(ValueError, match=message):
            routed.owner._finish(invocation, capture)
    finally:
        for active in tuple(routed.owner._active.values()):
            routed.owner._discard(active)


def test_wrong_actual_policy_and_handler_proof(routed, monkeypatch):
    read(routed)
    original = qualification.operation_policy
    def changed(*a):
        return original(*a).model_copy(update={"prerequisites": ()})
    monkeypatch.setattr(qualification, "operation_policy", changed)
    with pytest.raises(ValueError, match="policy requirements mismatch"):
        read(routed)


def test_thread_task_and_process_context_is_not_reusable(routed, monkeypatch):
    monkeypatch.setattr(qualification, "_execution_context", lambda: (0, 0, None))
    with pytest.raises(ValueError, match="foreign thread task or process"):
        read(routed)
