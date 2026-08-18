from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import json
from pathlib import Path
import sys

from tools import governed_workpacket_file_guard as file_guard
from tools import workpacket_validation_tool as tool


@dataclass(frozen=True)
class _Ticket:
    ticket_type: str = "implementation"


@dataclass(frozen=True)
class _Step:
    validation_id: str
    description: str
    expected_result: str
    command: str | None = None


@dataclass(frozen=True)
class _WorkPacket:
    validation_steps: tuple[_Step, ...]
    source_ticket: _Ticket = _Ticket()
    ticket_id: str = "P18.9.1"


class _FakeProcess:
    def __init__(self, stdout: bytes = b"ok\n", stderr: bytes = b"", code: int = 0):
        self.stdout = BytesIO(stdout)
        self.stderr = BytesIO(stderr)
        self.code = code
        self.terminated = False
        self.killed = False

    def poll(self):
        return self.code

    def wait(self):
        return self.code

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True


def _authority(
    workspace: Path,
    *,
    allowed_paths: tuple[str, ...],
    forbidden_paths: tuple[str, ...] = (),
) -> file_guard.WorkPacketFileAuthority:
    return file_guard.WorkPacketFileAuthority(
        ticket_id="P18.9.1",
        work_packet_id="WP-P18-9-1-R0001-123456789abc",
        work_packet_SHA256="a" * 64,
        ticket_spec_SHA256="b" * 64,
        projection_SHA256="c" * 64,
        allowed_paths=allowed_paths,
        forbidden_paths=forbidden_paths,
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(strict=True),
    )


def _workpacket_with_steps(*steps: _Step) -> _WorkPacket:
    return _WorkPacket(validation_steps=tuple(steps))


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_non_governed_tool_fails_closed(monkeypatch) -> None:
    monkeypatch.delenv(file_guard.GOVERNED_WORKER_ENV, raising=False)

    result = json.loads(tool.workpacket_validation_tool(action="list"))

    assert result["error_code"] == tool.WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE


def test_registry_dispatch_accepts_session_metadata(monkeypatch) -> None:
    authority = _authority(
        Path(__file__).resolve().parent,
        allowed_paths=("tests/**",),
    )
    work_packet = _workpacket_with_steps()
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )

    result = json.loads(
        tool.registry.dispatch(
            "workpacket_validation",
            {"action": "list"},
            task_id="t_d5b19f78",
            session_id="session-1",
            user_task="P18.9.1",
        )
    )

    assert result["success"] is True
    assert result["command_count"] == 0


def test_python_command_run_uses_shell_false_and_minimal_env(tmp_path, monkeypatch) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    authority = _authority(workspace, allowed_paths=("tests/**",))
    work_packet = _workpacket_with_steps(
        _Step(
            "V1",
            "Run focused Python tests.",
            "The focused pytest command passes.",
            command="python -m pytest tests/example_test.py",
        )
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )

    from hermes_cli.agent_platform.work_packet import validation_command_runner as vcr

    calls = []

    def fake_popen(*args, **kwargs):
        calls.append((args, kwargs))
        return _FakeProcess()

    monkeypatch.setattr(vcr.subprocess, "Popen", fake_popen)

    result = json.loads(tool.workpacket_validation_tool(action="run", command_id="GVCMD-001"))

    assert result["success"] is True
    assert result["disposition"] == "passed"
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0][:3] == (Path(sys.executable).resolve().as_posix(), "-m", "pytest")
    assert args[0][-2:] == ("-p", "no:cacheprovider")
    assert kwargs["shell"] is False
    assert kwargs["stdin"] is vcr.subprocess.DEVNULL
    assert kwargs["cwd"] == workspace.resolve().as_posix()
    assert kwargs["env"]["CI"] == "1"
    assert "PATH" not in kwargs["env"]


def test_python_command_outside_workpacket_scope_is_not_authorized(tmp_path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    authority = _authority(workspace, allowed_paths=("src/**",))
    work_packet = _workpacket_with_steps(
        _Step(
            "V1",
            "Run focused Python tests.",
            "The focused pytest command passes.",
            command="python -m pytest tests/outside_test.py",
        )
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert specs == ()


def test_unlisted_command_id_is_denied(tmp_path, monkeypatch) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    authority = _authority(workspace, allowed_paths=("tests/**",))
    work_packet = _workpacket_with_steps(
        _Step("V1", "Run focused Python tests.", "The focused pytest command passes.", command="python -m unittest --help")
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )

    result = json.loads(tool.workpacket_validation_tool(action="run", command_id="GVCMD-999"))

    assert result["error_code"] == tool.WORKPACKET_VALIDATION_COMMAND_DENIED


def test_p18_9_1_frontend_package_command_uses_allowed_route_navigation_tests(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"test": "vitest run"}}))
    node = tmp_path / "node"
    vitest = tmp_path / "vitest.mjs"
    _write(node, "")
    _write(vitest, "")
    allowed_test_files = (
        "2_products/pepper-agent/web/src/agent-platform/extensions.test.ts",
        "2_products/pepper-agent/web/src/agent-platform/shell/navigation-group-order.test.tsx",
        "2_products/pepper-agent/web/src/agent-platform/runtime-overview/route-compatibility.test.tsx",
        "2_products/pepper-agent/web/src/agent-platform/projects-tickets/contextual-detail-routes.test.tsx",
        "2_products/pepper-agent/web/src/agent-platform/approval-inbox/protected-namespace.test.tsx",
        "2_products/pepper-agent/web/src/agent-platform/execution-inspector/plugin-collision.test.tsx",
    )
    for rel in allowed_test_files:
        _write(workspace / rel, "test('synthetic', () => {})\n")
    _write(
        workspace / "2_products/pepper-agent/web/src/agent-platform/design-system/design-system.test.ts",
        "test('p18.9.12', () => {})\n",
    )
    _write(
        workspace / "2_products/pepper-agent/web/src/agent-platform/product-config.test.ts",
        "test('outside p18.9.1 paths', () => {})\n",
    )
    authority = _authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/web/src/agent-platform/extensions.test.ts",
            "2_products/pepper-agent/web/src/agent-platform/shell/**",
            "2_products/pepper-agent/web/src/agent-platform/runtime-overview/**",
            "2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",
            "2_products/pepper-agent/web/src/agent-platform/approval-inbox/**",
            "2_products/pepper-agent/web/src/agent-platform/execution-inspector/**",
        ),
    )
    work_packet = _workpacket_with_steps(
        _Step(
            "V1",
            "Human review confirms generated TicketSpec and WorkPacket.",
            "The reviewer can identify implementation objective and boundaries.",
        ),
        _Step(
            "V2",
            "Focused frontend tests validate route compatibility and navigation grouping.",
            "Test results show plugin collision blocking, protected namespace, contextual detail routes, and P18.9.12 boundary preservation.",
        ),
    )
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, _entry: vitest,
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert len(specs) == 1
    spec = specs[0]
    assert spec.command_id == "GVCMD-001"
    assert spec.validation_id == "V2"
    assert spec.effective_argv[:3] == (node.as_posix(), vitest.as_posix(), "run")
    command_text = " ".join(spec.effective_argv[3:])
    for rel in allowed_test_files:
        assert Path(rel).relative_to("2_products/pepper-agent/web").as_posix() in command_text
    assert "design-system" not in command_text
    assert "product-config.test.ts" not in command_text


def test_frontend_package_script_must_be_safe_vitest_run(tmp_path) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"test": "vitest run && git status"}}))
    _write(
        workspace / "2_products/pepper-agent/web/src/agent-platform/extensions.test.ts",
        "test('synthetic', () => {})\n",
    )
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/extensions.test.ts",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V2", "Focused frontend tests.", "The focused frontend tests pass.")
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert specs == ()


def test_pepper_validation_toolset_is_not_a_core_terminal_surface() -> None:
    from toolsets import _HERMES_CORE_TOOLS, resolve_toolset

    assert resolve_toolset("pepper_validation") == ["workpacket_validation"]
    assert "workpacket_validation" not in _HERMES_CORE_TOOLS
    assert "terminal" not in resolve_toolset("pepper_validation")
    assert "process" not in resolve_toolset("pepper_validation")


def test_model_tools_auto_adds_validation_toolset_only_for_governed_workers(
    monkeypatch,
) -> None:
    import model_tools

    captured: list[set[str]] = []

    def fake_get_definitions(tool_names, quiet=False):
        _ = quiet
        captured.append(set(tool_names))
        return []

    monkeypatch.setattr(model_tools.registry, "get_definitions", fake_get_definitions)
    monkeypatch.delenv(file_guard.GOVERNED_WORKER_ENV, raising=False)

    model_tools._compute_tool_definitions(
        enabled_toolsets=["pepper_repository", "file"],
        quiet_mode=True,
        skip_tool_search_assembly=True,
    )

    assert "workpacket_validation" not in captured[-1]

    monkeypatch.setenv(file_guard.GOVERNED_WORKER_ENV, file_guard.GOVERNED_WORKER_MODE)
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_WORKPACKET_ID", "WP-P18-9-1-R0001-123456789abc")
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_WORKPACKET_SHA256", "a" * 64)

    model_tools._compute_tool_definitions(
        enabled_toolsets=["pepper_repository", "file"],
        quiet_mode=True,
        skip_tool_search_assembly=True,
    )

    assert "workpacket_validation" in captured[-1]
    assert "terminal" not in captured[-1]
    assert "process" not in captured[-1]
