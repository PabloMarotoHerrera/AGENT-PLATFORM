"""Fresh-process import/effect guards, exercising actual passive evaluation."""

import os
from pathlib import Path
import subprocess
import sys

import pytest

from tests.hermes_cli.test_har04_harness_purity import PROBE


@pytest.mark.parametrize("canary", [None, "runtime", "registry", "model_tools", "provider", "write", "process", "network"])
def test_passive_shadow_runs_without_imports_or_effects(tmp_path, canary):
    home = tmp_path / "guarded"; home.mkdir()
    script = PROBE + r'''
allowed_project.update({"hermes_cli.agent_platform.shadow_adapters", "hermes_cli.agent_platform.shadow_entry",
 "hermes_cli.agent_platform.admissibility_projection", "hermes_cli.agent_platform.pre_review_catalog",
 "hermes_cli.agent_platform.pre_review_reference_model", "hermes_cli.agent_platform.handler_correspondence"})
forbidden_roots.update({"model_tools", "hermes_state", "hermes_constants"})
from tests.hermes_cli.test_har09_shadow_adapters import case, expected_legacy
from hermes_cli.agent_platform.shadow_adapters import observe
from hermes_cli.agent_platform.harness.shadow import compare
from hermes_cli.agent_platform.shadow_entry import CaptureSpec, VerificationSession, observe_completed
s, metadata, proof = case()
legacy = expected_legacy(s, metadata)
result = compare(legacy, observe(metadata, proof))
assert not result.grants_authority and result.observational
session = VerificationSession(CaptureSpec("synthetic", metadata, proof, legacy))
observe_completed(session, "synthetic", "{}")
assert len(session.captures) == 1
print("HAR09_PURE")
'''
    canaries = {"runtime": "__import__('hermes_cli.agent_platform.product_runtime')",
        "registry": "__import__('tools.registry')", "model_tools": "__import__('model_tools')",
        "provider": "__import__('openai')", "write": "open('forbidden', 'w')",
        "process": "audit('subprocess.Popen', ())", "network": "audit('socket.connect', ())"}
    if canary: script += "\n" + canaries[canary]
    root = str(Path(__file__).resolve().parents[2])
    result = subprocess.run([sys.executable, "-I", "-B", "-c", script, root], cwd=home,
        env={"HOME": str(home), "HERMES_HOME": str(home / "hermes"), "PATH": os.defpath, "LANG": "C.UTF-8", "TZ": "UTC"},
        capture_output=True, text=True, timeout=60)
    if canary:
        assert result.returncode != 0 and "RuntimeError:" in result.stderr
    else:
        assert result.returncode == 0, result.stderr
        assert "HAR09_PURE" in result.stdout
    assert list(home.iterdir()) == []
