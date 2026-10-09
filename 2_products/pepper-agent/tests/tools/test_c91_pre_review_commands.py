"""Bounded legacy command syntax, source contexts, and launch substrate."""

import json
from types import SimpleNamespace
import pytest

from tools import pre_review_validation_commands as compat, workpacket_validation_tool as vt
from tools.governed_workpacket_file_guard import WorkPacketFileAuthority
from hermes_cli.agent_platform import command_validation_context as context
from hermes_cli.agent_platform.work_packet import validation_command_runner as runner


@pytest.fixture
def source(tmp_path, monkeypatch):
    root = tmp_path / "source"
    product = root / compat.PRODUCT
    for name, text in {
        "scripts/run_tests.sh": "#!/bin/bash\nexit 0\n",
        "scripts/run_tests_parallel.py": "# isolated canonical helper\n",
        "tests/hermes_cli/test_smoke.py": "def test_smoke(): assert True\n",
        "web/package.json": json.dumps({"scripts": {"test": "vitest run", "typecheck": "tsc -p . --noEmit", "build": "tsc -b && vite build"}}),
        "web/src/agent-platform/smoke.test.ts": "// source\n",
        "node_modules/vitest/vitest.mjs": "// CLI\n",
        "node_modules/typescript/lib/tsc.js": "// CLI\n",
        "node_modules/vite/bin/vite.js": "// CLI\n",
    }.items():
        path = product / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    node = tmp_path / "node"
    node.write_text("isolated node executable")
    monkeypatch.setattr(vt, "_resolve_node_executable", lambda: node)
    authority = WorkPacketFileAuthority(ticket_id="P99.1", ticket_spec_SHA256="a" * 64,
        work_packet_id="WP-P99", work_packet_SHA256="b" * 64, projection_SHA256="c" * 64,
        allowed_paths=(compat.PRODUCT + "/tests/hermes_cli/**", compat.PRODUCT + "/web/src/**"),
        forbidden_paths=(".git/**",), workspace_root=root, resolved_workspace_root=root)
    return SimpleNamespace(root=root, product=product, authority=authority)


def specs(source, *commands):
    packet = SimpleNamespace(validation_steps=[SimpleNamespace(validation_id=f"T{i}", command=cmd,
        required=True, step_SHA256=str(i) * 64, command_authority=None) for i, cmd in enumerate(commands, 1)])
    return compat.extend_specs(source.authority, packet, ())


def test_wrapper_and_npm_plans_preserve_exact_source_and_scope(source):
    commands = ("scripts/run_tests.sh tests/hermes_cli/test_smoke.py", "npm test -- --run web/src/agent-platform", "npm run typecheck && npm run build")
    result = specs(source, *commands)
    assert [s.source_command for s in result] == list(commands)
    assert len(result) == 3
    assert result[0].effective_argv[-1] == "tests/hermes_cli/test_smoke.py"
    assert result[0].working_directory == str(source.product)
    assert result[1].working_directory == str(source.product / "web")
    assert result[1].effective_argv[-1] == "src/agent-platform"
    assert len(result[2].execution_plan) == 3
    assert all(s.command_authority_SHA256 and s.execution_plan_SHA256 for s in result)
    assert all(s.work_packet_SHA256 == source.authority.work_packet_SHA256 for s in result)


@pytest.mark.parametrize("command", [
    "bash -c echo", "scripts/run_tests.sh -p arbitrary", "scripts/run_tests.sh ../escape.py",
    "scripts/run_tests.sh tests/other.py", "scripts/run_tests.sh tests/hermes_cli/test_smoke.py;touch /tmp/bad",
    "npm install", "npm test || curl bad", "npm run typecheck && npm run build && npm test",
    "npm test -- ../../outside.test.ts", "npm exec arbitrary", "git status", "docker ps", "graphify update .",
])
def test_arbitrary_or_unbounded_commands_have_no_spec(source, command):
    assert specs(source, command) == ()


def test_wrapper_drift_denies_before_process(source, monkeypatch):
    spec = specs(source, "scripts/run_tests.sh tests/hermes_cli/test_smoke.py")[0]
    (source.product / "scripts/run_tests.sh").write_text("changed")
    monkeypatch.setattr(runner, "_launch_and_capture", lambda *a, **k: pytest.fail("must not launch"))
    result = json.loads(vt._run_command(source.authority, spec))
    assert not result["process_started"]
    assert result["error_code"] == vt.WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT


def test_missing_approved_test_does_not_silently_narrow_suite(source, monkeypatch):
    spec = specs(source, "scripts/run_tests.sh tests/hermes_cli/test_missing.py tests/hermes_cli/test_smoke.py")[0]
    monkeypatch.setattr(runner, "_launch_and_capture", lambda *a, **k: pytest.fail("must not run partial suite"))
    result = json.loads(vt._run_command(source.authority, spec))
    assert result["success"] is False and result["process_started"] is False
    assert "test_missing.py" in result["error_detail"]


def test_wrapper_uses_substrate_and_bound_interpreter(source, monkeypatch):
    spec = specs(source, "scripts/run_tests.sh tests/hermes_cli/test_smoke.py")[0]
    launched = []
    def launch(command, env):
        launched.append((command, env))
        return runner._LaunchResult(exit_code=0, stdout_raw=b"1 passed", stderr_raw=b"", process_started=True,
            terminate_requested=False, kill_requested=False, timed_out=False, output_limit_exceeded=False, launch_failed=False)
    monkeypatch.setattr(runner, "_launch_and_capture", launch)
    result = json.loads(vt._run_command(source.authority, spec))
    assert result["success"] and len(launched) == 1
    assert launched[0][0].effective_argv == spec.effective_argv
    assert launched[0][1]["HERMES_PYTHON"]


def test_fingerprint_ignores_outputs_but_detects_source_and_lock_drift(source):
    before = context.fingerprint(source.root)
    (source.product / "test_durations.json").write_text("generated timing")
    (source.product / "web/dist").mkdir()
    (source.product / "web/dist/generated.js").write_text("build output")
    assert context.fingerprint(source.root) == before
    (source.product / "package-lock.json").write_text('{"lockfileVersion": 3}')
    assert context.fingerprint(source.root) != before


def test_ambiguous_package_context_is_denied(source):
    from dataclasses import replace
    other = source.product / "ui-tui"
    other.mkdir()
    (other / "package.json").write_text('{"scripts":{"typecheck":"tsc -p . --noEmit"}}')
    source.authority = replace(source.authority, allowed_paths=(*source.authority.allowed_paths, compat.PRODUCT + "/ui-tui/src/**"))
    assert specs(source, "npm run typecheck") == ()
