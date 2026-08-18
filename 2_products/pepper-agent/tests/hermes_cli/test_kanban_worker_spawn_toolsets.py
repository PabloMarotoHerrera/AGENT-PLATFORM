from __future__ import annotations

import json
import logging.handlers
import subprocess
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

import pytest


def _make_task(kb, *, assignee: str, task_id: str = "t_spawn_tools"):
    return kb.Task(
        id=task_id,
        title="spawn tools",
        body=None,
        assignee=assignee,
        status="running",
        priority=0,
        created_by="test",
        created_at=1,
        started_at=None,
        completed_at=None,
        workspace_kind="dir",
        workspace_path=None,
        claim_lock="lock",
        claim_expires=None,
        tenant=None,
        current_run_id=7,
    )


def _tool_call(name: str, call_id: str):
    return SimpleNamespace(
        id=f"fc_{call_id}",
        call_id=call_id,
        type="function_call",
        name=name,
        arguments=json.dumps({"action": "list"}),
    )


def _codex_tool_call_response(name: str, call_id: str):
    return SimpleNamespace(
        output=[_tool_call(name, call_id)],
        usage=SimpleNamespace(input_tokens=12, output_tokens=4, total_tokens=16),
        status="completed",
        model="gpt-5.5",
    )


def _codex_message_response(text: str):
    return SimpleNamespace(
        output=[
            SimpleNamespace(
                type="message",
                content=[SimpleNamespace(type="output_text", text=text)],
            )
        ],
        usage=SimpleNamespace(input_tokens=5, output_tokens=3, total_tokens=8),
        status="completed",
        model="gpt-5.5",
    )


@pytest.fixture(autouse=True)
def _stub_windows_log_handler_dependency(monkeypatch):
    if sys.platform != "win32":
        return
    try:
        __import__("concurrent_log_handler")
    except ModuleNotFoundError:
        module = ModuleType("concurrent_log_handler")
        module.ConcurrentRotatingFileHandler = logging.handlers.RotatingFileHandler
        monkeypatch.setitem(sys.modules, "concurrent_log_handler", module)


def test_default_spawn_pins_assignee_profile_cli_toolsets(monkeypatch, tmp_path):
    """Manual profile assignment should keep that profile's CLI tools.

    Regression guard for dispatcher-spawned workers that boot with
    HERMES_KANBAN_TASK: the worker must not collapse to only kanban lifecycle
    tools when the assigned profile's top-level ``toolsets`` is the default
    composite. The spawned CLI gets an explicit --toolsets pin resolved from
    platform_toolsets.cli; model_tools appends task-scoped kanban tools later.
    """
    root = tmp_path / ".hermes"
    profile = root / "profiles" / "elias"
    profile.mkdir(parents=True)
    profile.joinpath("config.yaml").write_text(
        """
platform_toolsets:
  cli:
    - clarify
    - code_execution
    - delegation
    - file
    - memory
    - session_search
    - skills
    - terminal
    - web
toolsets:
  - hermes-cli
agent:
  disabled_toolsets: []
""".lstrip(),
        encoding="utf-8",
    )
    root.joinpath("config.yaml").write_text("toolsets:\n  - kanban\n", encoding="utf-8")
    monkeypatch.setenv("HERMES_HOME", str(root))

    from hermes_cli import kanban_db as kb

    monkeypatch.setattr(kb, "_resolve_hermes_argv", lambda: ["hermes"])

    captured = {}

    class FakeProc:
        pid = 4242

    def fake_popen(cmd, *args, **kwargs):
        captured["cmd"] = list(cmd)
        captured["env"] = dict(kwargs.get("env") or {})
        captured["cwd"] = kwargs.get("cwd")
        return FakeProc()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    pid = kb._default_spawn(_make_task(kb, assignee="elias"), str(workspace))

    assert pid == 4242
    assert captured["env"]["HERMES_HOME"] == str(profile)
    assert captured["env"]["HERMES_KANBAN_TASK"] == "t_spawn_tools"
    assert "--toolsets" in captured["cmd"]
    pinned = captured["cmd"][captured["cmd"].index("--toolsets") + 1].split(",")
    for required in ("terminal", "web", "file", "skills", "code_execution", "delegation"):
        assert required in pinned


def test_default_spawn_never_boots_the_tui(monkeypatch, tmp_path):
    """Workers are headless: an inherited HERMES_TUI=1 (or a TUI-default
    config) must not send the quiet chat run into the Ink TUI, whose no-TTY
    bail-out exits 0 without doing the task — every attempt then ends in
    "protocol violation". The spawn pins --cli (highest-precedence interface
    flag) and strips HERMES_TUI from the child env."""
    root = tmp_path / ".hermes"
    (root / "profiles" / "elias").mkdir(parents=True)
    root.joinpath("config.yaml").write_text("display:\n  interface: tui\n", encoding="utf-8")
    monkeypatch.setenv("HERMES_HOME", str(root))
    monkeypatch.setenv("HERMES_TUI", "1")

    from hermes_cli import kanban_db as kb

    monkeypatch.setattr(kb, "_resolve_hermes_argv", lambda: ["hermes"])

    captured = {}

    class FakeProc:
        pid = 4243

    def fake_popen(cmd, *args, **kwargs):
        captured["cmd"] = list(cmd)
        captured["env"] = dict(kwargs.get("env") or {})
        return FakeProc()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    kb._default_spawn(_make_task(kb, assignee="elias"), str(workspace))

    assert "--cli" in captured["cmd"]
    assert "HERMES_TUI" not in captured["env"]


def test_default_spawn_model_override_survives_real_cli_parse(monkeypatch, tmp_path):
    """The dispatcher's pre-``chat`` model flag must reach ``args.model``.

    This is an integration contract between Kanban's worker argv builder and
    the real CLI parser. A parser default once erased the explicit override,
    silently sending the worker to its profile default or fallback instead.
    """
    root = tmp_path / ".hermes"
    (root / "profiles" / "elias").mkdir(parents=True)
    root.joinpath("config.yaml").write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv("HERMES_HOME", str(root))

    from hermes_cli import kanban_db as kb
    from hermes_cli._parser import build_top_level_parser

    monkeypatch.setattr(kb, "_resolve_hermes_argv", lambda: ["hermes"])
    captured = {}

    class FakeProc:
        pid = 4244

    def fake_popen(cmd, *args, **kwargs):
        captured["cmd"] = list(cmd)
        return FakeProc()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    task = _make_task(kb, assignee="elias")
    task.model_override = "gpt-5.6-sol"
    kb._default_spawn(task, str(workspace))

    parser, _subparsers, _chat_parser = build_top_level_parser()
    # Profile selection is attached by the outer CLI bootstrap rather than
    # build_top_level_parser(); remove that already-validated prefix and parse
    # the worker flags/subcommand through the real shared parser.
    assert captured["cmd"][1:3] == ["-p", "elias"]
    args = parser.parse_args(captured["cmd"][3:])

    assert args.command == "chat"
    assert args.model == "gpt-5.6-sol"
    assert args.query == "work kanban task t_spawn_tools"


def test_resolve_worker_cli_toolsets_uses_profile_home_not_parent_config(monkeypatch, tmp_path):
    root = tmp_path / ".hermes"
    profile = root / "profiles" / "elias"
    profile.mkdir(parents=True)
    root.joinpath("config.yaml").write_text("platform_toolsets:\n  cli:\n    - kanban\n", encoding="utf-8")
    profile.joinpath("config.yaml").write_text(
        """
platform_toolsets:
  cli:
    - terminal
    - web
toolsets:
  - hermes-cli
""".lstrip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("HERMES_HOME", str(root))

    from hermes_cli import kanban_db as kb

    resolved = kb._resolve_worker_cli_toolsets(str(profile))

    assert resolved is not None
    assert "terminal" in resolved
    assert "web" in resolved
    assert "kanban" in resolved  # recovered worker lifecycle surface
    assert resolved != ["kanban"]


def test_pepper_implementation_worker_entry_reaches_native_loop_after_validation_failure(
    monkeypatch,
    tmp_path,
):
    root = tmp_path / ".hermes"
    profile_name = "pepper-implementation-product"
    profile = root / "profiles" / profile_name
    profile.mkdir(parents=True)
    profile.joinpath("config.yaml").write_text(
        """
platform_toolsets:
  cli:
    - pepper_repository
    - file
    - no_mcp
model:
  provider: openai-codex
  default: gpt-5.5
  api_mode: codex_responses
toolsets:
  - pepper_repository
  - file
  - no_mcp
agent:
  disabled_toolsets: []
""".lstrip(),
        encoding="utf-8",
    )
    root.joinpath("config.yaml").write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv("HERMES_HOME", str(root))

    from hermes_cli import kanban_db as kb
    from hermes_cli.agent_platform import product_runtime as pr

    task_id = "t_d5b19f78"
    work_packet_id = "WP-P18-9-1-R0001-123456789abc"
    projection = {
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
        "work_packet_id": work_packet_id,
        "work_packet_SHA256": "a" * 64,
        "ticket_spec_SHA256": "b" * 64,
        "kanban_task_id": task_id,
        "assignee_profile": profile_name,
        "projection_SHA256": "c" * 64,
        "authority": {"projection_SHA256": "c" * 64},
        "profile_assignment_policy_id": "pepper.execution-profiles.v1",
        "profile_assignment_policy_revision": "test",
    }
    env_overlay = pr._pepper_governed_worker_env_overlay(projection)

    monkeypatch.setattr(kb, "_resolve_hermes_argv", lambda: ["hermes"])
    captured = {}

    class FakeProc:
        pid = 4245

    def fake_popen(cmd, *args, **kwargs):
        captured["cmd"] = list(cmd)
        captured["env"] = dict(kwargs.get("env") or {})
        captured["cwd"] = kwargs.get("cwd")
        return FakeProc()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    pid = kb._default_spawn(
        _make_task(kb, assignee=profile_name, task_id=task_id),
        str(workspace),
        env_overlay=env_overlay,
    )

    assert pid == 4245
    assert captured["cwd"] == str(workspace)
    assert captured["cmd"][:4] == ["hermes", "-p", profile_name, "--cli"]
    assert captured["cmd"][-3:] == ["chat", "-q", f"work kanban task {task_id}"]
    assert "--toolsets" in captured["cmd"]
    pinned = captured["cmd"][captured["cmd"].index("--toolsets") + 1].split(",")
    assert "pepper_repository" in pinned
    assert "file" in pinned
    assert "terminal" not in pinned
    assert "process" not in pinned

    worker_env = captured["env"]
    assert worker_env["HERMES_HOME"] == str(profile)
    assert worker_env["HERMES_PROFILE"] == profile_name
    assert worker_env["HERMES_KANBAN_TASK"] == task_id
    assert worker_env["HERMES_KANBAN_WORKSPACE"] == str(workspace)
    assert worker_env["TERMINAL_CWD"] == str(workspace)
    assert worker_env["HERMES_AGENT_PLATFORM_GOVERNED_WORKER"] == "pepper-kanban-worker"
    assert worker_env["HERMES_AGENT_PLATFORM_EXECUTOR_PROFILE"] == profile_name
    assert worker_env["HERMES_AGENT_PLATFORM_WORKPACKET_ID"] == work_packet_id
    assert worker_env["HERMES_AGENT_PLATFORM_WORKER_PROFILE_ID"] == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    overlay_text = json.dumps(env_overlay, sort_keys=True).lower()
    assert "api_key" not in overlay_text
    assert "access_token" not in overlay_text
    assert "refresh_token" not in overlay_text

    for key in (
        "HERMES_HOME",
        "HERMES_PROFILE",
        "HERMES_KANBAN_TASK",
        "HERMES_KANBAN_WORKSPACE",
        "HERMES_KANBAN_DB",
        "HERMES_KANBAN_WORKSPACES_ROOT",
        "HERMES_KANBAN_BOARD",
        "TERMINAL_CWD",
        *env_overlay.keys(),
    ):
        monkeypatch.setenv(key, worker_env[key])
    monkeypatch.chdir(workspace)

    import model_tools
    import run_agent
    from tools.registry import invalidate_check_fn_cache

    model_tools._clear_tool_defs_cache()
    invalidate_check_fn_cache()

    api_requests = []
    captured_result = {}

    def fake_ensure_runtime_credentials(self):
        self.provider = worker_env["HERMES_AGENT_PLATFORM_PROVIDER"]
        self.model = worker_env["HERMES_AGENT_PLATFORM_MODEL"]
        self.api_mode = worker_env["HERMES_AGENT_PLATFORM_API_MODE"]
        self.api_key = "offline-codex-token"
        self.base_url = "https://chatgpt.com/backend-api/codex"
        self.acp_command = None
        self.acp_args = []
        self._credential_pool = None
        return True

    def fake_interruptible_api_call(self, api_kwargs):
        api_requests.append(api_kwargs)
        if len(api_requests) == 1:
            return _codex_tool_call_response("workpacket_validation", "validation1")
        return _codex_message_response("Validation failure returned to the native loop.")

    original_agent_run = run_agent.AIAgent.run_conversation

    def capture_agent_run(self, *args, **kwargs):
        captured_result["agent_run_conversation_called"] = True
        result = original_agent_run(self, *args, **kwargs)
        captured_result["result"] = result
        return result

    import agent.conversation_loop as conversation_loop

    original_loop_run = conversation_loop.run_conversation

    def capture_native_loop(agent, *args, **kwargs):
        captured_result["native_loop_called"] = True
        return original_loop_run(agent, *args, **kwargs)

    import cli as cli_mod

    monkeypatch.setattr(cli_mod.atexit, "register", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cli_mod, "_finalize_single_query", lambda _cli: None)
    monkeypatch.setattr(cli_mod.HermesCLI, "_claim_active_session", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(cli_mod.HermesCLI, "_show_security_advisories", lambda _self: None)
    monkeypatch.setattr(cli_mod.HermesCLI, "_print_exit_summary", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cli_mod.HermesCLI, "_ensure_runtime_credentials", fake_ensure_runtime_credentials)
    monkeypatch.setattr("hermes_cli.mcp_startup.wait_for_mcp_discovery", lambda: None)
    monkeypatch.setattr(run_agent.AIAgent, "_interruptible_api_call", fake_interruptible_api_call)
    monkeypatch.setattr(run_agent.AIAgent, "run_conversation", capture_agent_run)
    monkeypatch.setattr(conversation_loop, "run_conversation", capture_native_loop)
    monkeypatch.setattr(run_agent, "OpenAI", MagicMock(return_value=MagicMock()))

    try:
        cli_mod.main(
            query=f"work kanban task {task_id}",
            toolsets=",".join(pinned),
            quiet=False,
            worktree=False,
        )
    finally:
        model_tools._clear_tool_defs_cache()
        invalidate_check_fn_cache()

    assert captured_result["agent_run_conversation_called"] is True
    assert captured_result["native_loop_called"] is True
    result = captured_result["result"]
    assert result["completed"] is True
    assert result["failed"] is False
    assert result["api_calls"] >= 2
    assert result["final_response"] == "Validation failure returned to the native loop."

    first_request_tools = api_requests[0]["tools"]
    assert any(tool.get("name") == "workpacket_validation" for tool in first_request_tools)
    second_request_input = api_requests[1]["input"]
    assert any(
        item.get("type") == "function_call_output"
        and item.get("call_id") == "validation1"
        and "WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE" in item.get("output", "")
        for item in second_request_input
    )
    assert any(
        message.get("role") == "tool"
        and message.get("tool_call_id") == "validation1"
        and "WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE" in message.get("content", "")
        for message in result["messages"]
    )
