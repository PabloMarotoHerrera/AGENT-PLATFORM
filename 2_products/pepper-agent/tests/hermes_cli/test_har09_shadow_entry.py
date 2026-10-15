"""Real entry functions with disposable effect doubles, plus durable C91-C94 fixtures."""

import builtins
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from tools import pepper_workflow_tools as tools
from hermes_cli.agent_platform import (
    approved_artifact_inspection as artifact, command_validation as commands,
    material_revision_reconciliation as reconciliation, post_execution_material_revision as revision,
    post_accept_material_revision as post_accept, retry_material_revision as retry,
)
from hermes_cli.agent_platform import shadow_entry
from hermes_cli.agent_platform.shadow_entry import CaptureSpec, VerificationSession
from tests.hermes_cli.test_har09_shadow_adapters import case, expected_legacy, change

CASES = (
    "workflow-full", "workflow-blockers", "artifact-approved-error", "artifact-too-large",
    "artifact-approved", "artifact-scope", "artifact-no-id", "artifact-no-section",
    "artifact-pending-error", "artifact-pending", "review", "request-origin",
    "request-inspect-reconciliation", "request-reconcile", "request-inspect", "request-request",
    "request-error", "request-post-accept", "request-post-error", "request-retry", "request-retry-error",
    "revise-envelope", "revise-error", "revise-ok", "prepare-commands", "prepare-command-error",
    "prepare-unknown", "prepare-error", "prepare-ok", "manual-inspect", "manual-error",
    "attest-ok", "attest-error",
)


def setup_case(monkeypatch, name):
    calls = []
    context = defaultdict(lambda: None, next_action={"id": "SYNTHETIC", "target_ticket_id": "SYN-1"},
        current_ticket_id="SYN-1", blocker_count=0, workflow_status="synthetic", active_execution_count=0,
        workflow_control={})
    def good(*args, **kwargs):
        calls.append((deepcopy(args), deepcopy(kwargs)))
        return {"marker": "isolated-result"}
    def bad(*args, **kwargs):
        calls.append((deepcopy(args), deepcopy(kwargs)))
        exc = ValueError("isolated-owner-failure")
        if name == "revise-envelope":
            exc.failure_envelope = {"error_code": "SYNTHETIC_ENVELOPE"}
        raise exc
    failing = name.endswith("error") or name == "revise-envelope"
    pr = SimpleNamespace(build_lead_agent_operational_context=lambda: context,
        build_workflow_control_snapshot=lambda: context,
        build_approval_artifact_section_source=bad if failing else good,
        revise_current_ticket_for_material_contract_failure=bad if failing else good,
        prepare_current_ticket_review=bad if failing else good,
        inspect_current_ticket_manual_validation=bad if failing else good,
        attest_current_ticket_manual_validation=bad if failing else good)
    monkeypatch.setattr(tools, "_runtime", lambda: pr)
    monkeypatch.setattr(tools, "_context", lambda: context)
    monkeypatch.setattr(tools, "_validate_explicit_successor_revision_request", lambda *a, **k: "synthetic-consent")
    monkeypatch.setattr(tools, "_validate_explicit_review_prepare_request", lambda *a, **k: "synthetic-consent")
    monkeypatch.setattr(artifact, "inspect", bad if failing else good)
    if name == "artifact-too-large":
        def large(**kwargs):
            calls.append(((), kwargs))
            return {"body": "x" * 36000}
        monkeypatch.setattr(artifact, "inspect", large)
    for module, attrs in ((commands, ("inspect", "execute")), (revision, ("inspect", "request")),
            (reconciliation, ("inspect", "reconcile")), (post_accept, ("request",)), (retry, ("request",))):
        for attr in attrs:
            monkeypatch.setattr(module, attr, bad if failing else good)
    monkeypatch.setattr(commands, "public", lambda result: result)
    monkeypatch.setattr(revision, "public", lambda result: result)
    if name.startswith("workflow"):
        return tools._get_workflow_control, {"blockers_only": True} if name.endswith("blockers") else {}, calls
    if name.startswith("artifact"):
        args = {"authority_scope": "current_approved", "approval_id": "SYN-1", "section_id": "ticket_spec"}
        if "pending" in name: args["authority_scope"] = "pending"
        if name == "artifact-scope": args["authority_scope"] = "unknown"
        if name == "artifact-no-id": args = {"section_id": "ticket_spec"}
        if name == "artifact-no-section": args = {"approval_id": "SYN-1"}
        return tools._inspect_pending_approval_artifact_section, args, calls
    if name == "review": return tools._get_review_status, {}, calls
    if name.startswith("request"):
        operation = {"request-inspect-reconciliation": "inspect_reconciliation", "request-reconcile": "reconcile",
            "request-inspect": "inspect", "request-request": "request", "request-error": "request"}.get(name)
        args = {"origin": "post_execution", "operation": operation} if operation else {}
        if name == "request-origin": args = {"operation": "inspect"}
        if name.startswith("request-post"): args = {"origin": "post_accept"}
        return tools._request_current_ticket_material_revision, args, calls
    if name.startswith("revise"): return tools._revise_current_ticket_for_material_contract_failure, {}, calls
    if name.startswith("prepare"):
        args = {"operation": "inspect_commands"} if name in {"prepare-commands", "prepare-command-error"} else {}
        if name == "prepare-unknown": args = {"operation": "unknown"}
        return tools._prepare_current_ticket_review, args, calls
    if name.startswith("manual"): return tools._inspect_current_ticket_manual_validation, {}, calls
    return tools._attest_current_ticket_manual_validation, {"status": "passed"}, calls


def invoke_trace(function, args):
    lines = []
    def trace(frame, event, arg):
        if event == "return" and frame.f_code is function.__code__: lines.append(frame.f_lineno)
        return trace
    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        result = function(args)
    finally:
        sys.settrace(previous)
    assert len(lines) == 1
    return result, lines[0]


def test_all_33_final_returns_preserve_bytes_arguments_and_single_execution(monkeypatch):
    returns = set()
    for name in CASES:
        with monkeypatch.context() as patch:
            function, args, calls = setup_case(patch, name)
            original_args = deepcopy(args)
            captured = []
            patch.setattr(shadow_entry, "observe_completed", lambda session, entry, result: captured.append((entry, result)))
            patch.setattr(tools, "_HAR09_VERIFICATION", None)
            baseline, line = invoke_trace(function, args)
            call_trace = deepcopy(calls)
            assert len(calls) <= 1 and args == original_args and not captured
            calls.clear()
            patch.setattr(tools, "_HAR09_VERIFICATION", object())
            enabled, enabled_line = invoke_trace(function, args)
            assert enabled == baseline and enabled.encode() == baseline.encode()
            assert calls == call_trace and args == original_args
            assert len(captured) == 1 and captured[0] == (function.__name__[1:], enabled)
            assert captured[0][1] is enabled and line == enabled_line
            assert (function.__name__, line) not in returns, name
            returns.add((function.__name__, line))
            if name == "artifact-too-large":
                assert "exceeds bound" in enabled and "body" not in enabled
    assert len(returns) == 33


@pytest.mark.parametrize("name", CASES)
def test_disabled_does_not_import_or_call_shadow(monkeypatch, name):
    fn, args, _ = setup_case(monkeypatch, name)
    monkeypatch.setattr(tools, "_HAR09_VERIFICATION", None)
    def forbidden(*a, **k): raise AssertionError("disabled mode called shadow")
    monkeypatch.setattr(tools, "_har09_observe_completed", forbidden)
    original = builtins.__import__
    def guarded(name, *a, **k):
        if "shadow" in name: raise AssertionError("disabled mode imported shadow")
        return original(name, *a, **k)
    monkeypatch.setattr(builtins, "__import__", guarded)
    assert isinstance(fn(args), str)


@pytest.mark.parametrize("name", CASES)
def test_shadow_delivery_failure_never_becomes_a_legacy_tool_error(monkeypatch, name):
    fn, args, calls = setup_case(monkeypatch, name)
    monkeypatch.setattr(tools, "_HAR09_VERIFICATION", None)
    expected = fn(args)
    calls.clear()
    diagnostics = []
    monkeypatch.setattr(tools, "_HAR09_VERIFICATION", SimpleNamespace(fail=diagnostics.append))
    def fail(*args): raise RuntimeError("shadow-only-failure")
    monkeypatch.setattr(shadow_entry, "observe_completed", fail)
    assert fn(args) == expected
    assert len(calls) <= 1 and diagnostics == ["shadow_delivery_failed"]


def test_legacy_exception_identity_survives_without_shadow_delivery(monkeypatch):
    exc = RuntimeError("legacy-exception")
    def fail(): raise exc
    monkeypatch.setattr(tools, "_context", fail)
    monkeypatch.setattr(tools, "_HAR09_VERIFICATION", object())
    delivered = []
    monkeypatch.setattr(shadow_entry, "observe_completed", lambda *a: delivered.append(a))
    with pytest.raises(RuntimeError) as actual: tools._get_review_status({})
    assert actual.value is exc and not delivered


def test_fresh_tools_import_does_not_load_shadow_or_replace_registered_handlers(tmp_path):
    root = str(Path(__file__).resolve().parents[2])
    home = tmp_path / "fresh-import"; home.mkdir()
    script = r'''
import builtins,sys
sys.path.insert(0,sys.argv[1])
original=builtins.__import__
def guard(name,*args,**kwargs):
    if "shadow" in name: raise AssertionError("default import loaded shadow")
    return original(name,*args,**kwargs)
builtins.__import__=guard
from tools import pepper_workflow_tools as t
assert t._HAR09_VERIFICATION is None
for name in ("get_workflow_control","inspect_pending_approval_artifact_section","get_review_status",
 "request_current_ticket_material_revision","revise_current_ticket_for_material_contract_failure",
 "prepare_current_ticket_review","inspect_current_ticket_manual_validation","attest_current_ticket_manual_validation"):
    handler=getattr(t,"_"+name)
    assert t.registry.get_entry(name).handler is handler
    assert not hasattr(handler,"__wrapped__")
assert not any("shadow" in name for name in sys.modules)
print("DEFAULT_ENTRY_IMPORT_PRESERVED")
'''
    result = subprocess.run([sys.executable, "-I", "-B", "-c", script, root], cwd=home,
        env={"HOME": str(home), "HERMES_HOME": str(home / "hermes"), "PATH": os.defpath,
            "PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "DEFAULT_ENTRY_IMPORT_PRESERVED" in result.stdout


def session():
    s, metadata, proof = case("valid.O01")
    return VerificationSession(CaptureSpec("prepare_current_ticket_review", metadata, proof, expected_legacy(s, metadata)))


@pytest.mark.parametrize("payload,reason", [("not-json", "shadow_evaluation_failed"),
    ('{"id":1,"id":2}', "shadow_evaluation_failed"),
    ("[]", "shadow_evaluation_failed"), ("x" * 1_048_577, "result_type_or_size_bound"),
    ("é" * 600000, "result_size_bound")])
def test_bounded_parsing_diagnostics_are_separate(payload, reason):
    value = session()
    shadow_entry.observe_completed(value, value.spec.entry, payload)
    assert value.diagnostics == [reason] and not value.captures


def test_capture_count_and_entry_bounds_and_no_authority():
    value = session()
    shadow_entry.observe_completed(value, "wrong-entry", "{}")
    assert value.diagnostics == ["entry_mismatch"]
    for _ in range(257): shadow_entry.observe_completed(value, value.spec.entry, "{}")
    assert len(value.captures) == 256 and value.truncated
    assert all(c.comparison.observational and not c.comparison.grants_authority for c in value.captures)


# Existing durable fixture setup is reused verbatim, never live records.
from tests.hermes_cli.test_c92_post_execution_material_revision import (
    flow, projection_home, evidence, completed, terminal, contract, defective,
)
from tests.hermes_cli.test_c94_material_revision_reconciliation import stale


@pytest.mark.parametrize("domain", ["C91", "C92", "C93", "C94"])
def test_real_durable_legacy_inspection_once_with_shadow(defective, monkeypatch, domain, request, record_property):
    f = request.getfixturevalue("stale") if domain == "C94" else defective
    routes = {
        "C91": (tools._prepare_current_ticket_review, {"operation": "inspect_commands"}, commands, "inspect"),
        "C92": (tools._request_current_ticket_material_revision, {"origin": "post_execution", "operation": "inspect"}, revision, "inspect"),
        "C93": (tools._inspect_pending_approval_artifact_section,
            {"authority_scope": "current_approved", "approval_id": f.p["ticket_id"], "section_id": "ticket_spec", "max_chars": 20000}, artifact, "inspect"),
        "C94": (tools._request_current_ticket_material_revision,
            {"origin": "post_execution", "operation": "inspect_reconciliation"}, reconciliation, "inspect"),
    }
    fn, args, owner, symbol = routes[domain]
    before = {str(p.relative_to(f.home)): p.read_bytes() for p in f.home.rglob("*") if p.is_file()}
    original = getattr(owner, symbol)
    calls = []
    def count(*a, **k):
        calls.append(1)
        return original(*a, **k)
    monkeypatch.setattr(owner, symbol, count)
    operation = {"C91": "O01", "C92": "O04", "C93": "O03.ticket_spec", "C94": "O06"}[domain]
    s, metadata, proof = case("valid." + operation)
    ticket = f.p["ticket_id"]
    metadata = change(metadata, context=change(metadata.context, current_ticket_id=ticket,
        target_ticket_id=ticket, action=change(metadata.context.action, target_ticket_id=ticket)),
        scope=change(metadata.scope, resource_ids=(ticket,)), authorities=(), prerequisites=())
    # Deliberately incomplete trusted-owner metadata cannot establish parity.
    value = VerificationSession(CaptureSpec(fn.__name__[1:], metadata, proof, expected_legacy(s, metadata)))
    monkeypatch.setattr(tools, "_HAR09_VERIFICATION", value)
    output = fn(args)
    assert calls == [1] and not f.launched
    assert json.loads(output)["success"]
    assert len(value.captures) == 1
    assert value.captures[0].result.sha256 == hashlib.sha256(output.encode()).hexdigest()
    assert value.captures[0].comparison.provenance.value == "EXECUTED_ISOLATED_LEGACY"
    assert value.captures[0].comparison.category.value != "PARITY"
    assert value.captures[0].comparison.severity != "SAFETY_CRITICAL"
    if domain == "C92":
        assert "next_operation_action_not_compared" in value.captures[0].comparison.unobservable
    assert before == {str(p.relative_to(f.home)): p.read_bytes() for p in f.home.rglob("*") if p.is_file()}
    record_property("har09_empirical", json.dumps({"domain": domain, "function": fn.__name__,
        "owner": owner.__name__ + "." + symbol, "isolation_root": str(f.home), "owner_calls": len(calls),
        "durable_changes_during_observed_call": 0, "worker_launches": len(f.launched),
        "setup_writes": "existing fixture initializes durable approvals/runs in disposable storage",
        "cleanup_boundary": "pytest fixture tmp_path; no live or shared profile",
        "output": value.captures[0].result.model_dump(), "comparison": value.captures[0].comparison.model_dump()}))
