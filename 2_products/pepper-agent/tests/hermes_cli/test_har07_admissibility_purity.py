"""Execute new imports and evaluations with imports/effects actively blocked."""

import os
from pathlib import Path
import subprocess
import sys

from tests.hermes_cli.test_har04_harness_purity import PROBE


def test_import_and_evaluation_are_effect_free(tmp_path):
    root = str(Path(__file__).resolve().parents[2])
    probe_home = tmp_path / "guarded"
    probe_home.mkdir()
    script = PROBE + r'''
allowed_project.update({"hermes_cli.agent_platform.admissibility_projection",
    "hermes_cli.agent_platform.pre_review_catalog", "hermes_cli.agent_platform.handler_correspondence"})
from tests.hermes_cli.test_har07_admissibility import fixture, admit, context
from hermes_cli.agent_platform.harness.admissibility import evaluate
from hermes_cli.agent_platform.admissibility_projection import translate
from hermes_cli.agent_platform.harness.contracts import DecisionOutcome
value, proof = fixture()
assert admit(value).decision.outcome == DecisionOutcome.ALLOW
assert evaluate(value).decision.outcome != DecisionOutcome.ALLOW
assert translate(admit(value), context(), binding=proof).invocable
print("HAR07_EVALUATION_PURE")
'''
    result = subprocess.run([sys.executable, "-I", "-B", "-c", script, root], cwd=probe_home,
        env={"HOME": str(probe_home), "HERMES_HOME": str(probe_home / "hermes"),
            "PATH": os.defpath, "LANG": "C.UTF-8", "TZ": "UTC"},
        capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "HAR07_EVALUATION_PURE" in result.stdout
    assert list(probe_home.iterdir()) == []
