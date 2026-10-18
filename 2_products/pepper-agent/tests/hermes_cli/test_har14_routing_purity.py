"""Read-phase effects are forbidden; fixture setup is explicitly separate."""
import sys
import socket
import subprocess
from tests.hermes_cli.har14_read_helpers import *


def test_fresh_import_pure(tmp_path):
    import os
    code = '''import sys, os
sys.dont_write_bytecode = True
def audit(event, args):
    if event == "open" and isinstance(args[2], int) and args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC):
        raise AssertionError((event, args))
    if event.startswith(("socket.", "subprocess.", "sqlite3.connect")) or event in ("os.system", "os.mkdir", "os.rename", "os.remove"):
        raise AssertionError((event, args))
sys.addaudithook(audit)
from hermes_cli.agent_platform import approved_artifact_read_qualification, approved_artifact_routing, approved_artifact_inspection
assert approved_artifact_inspection._READ_ROUTE.get() is None
assert "hermes_cli.agent_platform.product_runtime" not in sys.modules
assert "tools.registry" not in sys.modules
print("PURE_IMPORT_DEFAULT_OFF")
'''
    env = {**os.environ, "HOME": str(tmp_path), "HERMES_HOME": str(tmp_path / ".hermes"),
           "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "PURE_IMPORT_DEFAULT_OFF"


def test_read_phase_zero_effects(routed, monkeypatch):
    from pathlib import Path
    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import zero_change_decision
    from tools.registry import registry
    f = routed
    before = files(f)
    def forbidden(*a, **k):
        raise AssertionError("unexpected read-phase effect")
    for obj, name in [(socket, "socket"), (subprocess, "Popen"), (registry, "dispatch"),
                      (zero_change_decision, "persist"), (kanban_db, "init_db"),
                      (Path, "write_text"), (Path, "write_bytes"), (Path, "mkdir"),
                      (Path, "rename"), (Path, "replace"), (Path, "unlink")]:
        monkeypatch.setattr(obj, name, forbidden)
    open_original = Path.open
    def read_only(path, mode="r", *a, **k):
        if any(x in mode for x in "wax+"):
            forbidden()
        return open_original(path, mode, *a, **k)
    monkeypatch.setattr(Path, "open", read_only)
    assert read(f, max_chars=20000) == f.default
    assert files(f) == before and not f.launched


def test_no_legacy_fallback_on_admission_deny(routed, monkeypatch):
    evaluator = qualification.evaluate
    def denied(*a, **k):
        from hermes_cli.agent_platform.harness.contracts import DecisionOutcome
        result = evaluator(*a, **k)
        return result.model_copy(update={"decision": result.decision.model_copy(update={"outcome": DecisionOutcome.DENY})})
    monkeypatch.setattr(qualification, "evaluate", denied)
    with pytest.raises(ValueError, match="HAR admission rejected"):
        read(routed)
    assert not routed.owner.observations


def test_observation_never_human_approval_or_journal_permission(routed):
    read(routed)
    q = routed.owner.observations[0]
    assert q.raw_bytes_provenance == "NOT_CAPTURED"
    assert q.currentness_model == "SEQUENTIAL_OBSERVED_NOT_ATOMIC_AT_DELIVERY"
    assert q.source_closure == "BROAD_REQUIRED_NOT_OPERATIONALLY_QUALIFIED"
    assert q.read_principal.actor_id != q.original_reviewer
    assert q.scope.workflow_id == "c93-approved-artifact-read"
    assert q.original_decision == "approve"
    assert not q.grants_authority and not q.authorizes_execution
