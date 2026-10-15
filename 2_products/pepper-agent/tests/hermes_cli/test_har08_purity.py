"""New-process guarded imports and execution of the pure verifier/model checker."""

import os
from pathlib import Path
import subprocess
import sys

import pytest

from tests.hermes_cli.test_har04_harness_purity import PROBE


@pytest.mark.parametrize("canary", [None, "runtime", "registry", "model_tools", "state", "provider", "write", "process", "network"])
def test_new_verifier_and_generator_have_no_runtime_effects(tmp_path, canary):
    home = tmp_path / "guarded"
    home.mkdir()
    script = PROBE + r'''
forbidden_roots.update({"model_tools", "hermes_state", "hermes_constants"})
allowed_project.update({"hermes_cli.agent_platform.pre_review_reference_model",
    "hermes_cli.agent_platform.admissibility_projection", "hermes_cli.agent_platform.pre_review_catalog",
    "hermes_cli.agent_platform.handler_correspondence"})
from tests.hermes_cli.test_har08_coverage import fixture
from hermes_cli.agent_platform.harness.coverage import verify_coverage
from hermes_cli.agent_platform.harness.reference_model import check_reference
from hermes_cli.agent_platform.pre_review_reference_model import build_synthetic_reference_model
model = fixture()
assert verify_coverage(model).complete
report = check_reference(build_synthetic_reference_model(model))
assert report.passed and report.content_identity()
print("HAR08_PURE")
'''
    canaries = {"runtime": "__import__('hermes_cli.agent_platform.product_runtime')",
        "registry": "__import__('tools.registry')", "model_tools": "__import__('model_tools')",
        "state": "__import__('hermes_state')", "provider": "__import__('openai')",
        "write": "open('forbidden', 'w')", "process": "audit('subprocess.Popen', ())", "network": "audit('socket.connect', ())"}
    if canary:
        script += "\n" + canaries[canary]
    root = str(Path(__file__).resolve().parents[2])
    result = subprocess.run([sys.executable, "-I", "-B", "-c", script, root], cwd=home,
        env={"HOME": str(home), "HERMES_HOME": str(home / "hermes"), "PATH": os.defpath, "LANG": "C.UTF-8", "TZ": "UTC"},
        text=True, capture_output=True, timeout=60)
    if canary:
        assert result.returncode != 0 and "RuntimeError:" in result.stderr
    else:
        assert result.returncode == 0, result.stderr
        assert "HAR08_PURE" in result.stdout
    assert list(home.iterdir()) == []
