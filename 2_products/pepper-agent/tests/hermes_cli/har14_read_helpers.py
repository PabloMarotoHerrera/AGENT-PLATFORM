"""MECHANICAL_SYNTHETIC_ONLY: original isolated C93 records, no human provenance."""
from pathlib import Path
import json
import pytest

from tests.hermes_cli.test_c93_approved_artifact_inspection import (
    flow, projection_home, evidence, completed, terminal, contract, defective,
)
from hermes_cli.agent_platform import approved_artifact_inspection as inspection
from hermes_cli.agent_platform import approved_artifact_read_qualification as qualification
from hermes_cli.agent_platform.approved_artifact_routing import _mechanical_read_route


@pytest.fixture(autouse=True)
def unicode_contract(contract, monkeypatch):
    from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
    original = generation._synthetic_implementation_target
    def target(*args, **kwargs):
        kwargs["contract"]["validation_steps"][0]["description"] += " — aprobación: 漢字 😀"
        return original(*args, **kwargs)
    monkeypatch.setattr(generation, "_synthetic_implementation_target", target)


def read(f, **kwargs):
    return inspection.inspect(ticket_id=f.p["ticket_id"], section_id="validation_steps", **kwargs)


def files(f):
    return {str(p.relative_to(f.home)): p.read_bytes() for p in f.home.rglob("*") if p.is_file()}


@pytest.fixture
def routed(defective, monkeypatch):
    f = defective
    f.default = read(f, max_chars=20000)
    root = Path(qualification.__file__).resolve().parents[4]
    with _mechanical_read_route(isolated_repository=root, isolated_home=f.home) as owner:
        f.owner = owner
        f.captures = []
        prepare = owner._prepare
        def capture(value):
            f.captures.append(json.loads(json.dumps(value)))
            return prepare(value)
        monkeypatch.setattr(owner, "_prepare", capture)
        yield f


__all__ = ["flow", "projection_home", "evidence", "completed", "terminal", "contract", "defective",
           "unicode_contract", "routed", "read", "files", "inspection", "qualification", "pytest"]
