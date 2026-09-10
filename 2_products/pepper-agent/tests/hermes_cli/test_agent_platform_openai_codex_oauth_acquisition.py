from __future__ import annotations

import os
from pathlib import Path
import sys
from types import SimpleNamespace

from hermes_cli.agent_platform.provider_credentials.oauth_acquisition import (
    build_openai_codex_oauth_acquisition_plan,
    run_openai_codex_oauth_acquisition,
)


PRODUCT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    PRODUCT_ROOT
    / "hermes_cli"
    / "agent_platform"
    / "provider_credentials"
    / "oauth_acquisition.py"
)
AUTH_PARSER_PATH = PRODUCT_ROOT / "hermes_cli" / "subcommands" / "auth.py"
AUTH_COMMANDS_PATH = PRODUCT_ROOT / "hermes_cli" / "auth_commands.py"


def test_oauth_plan_uses_fixed_python_command_and_isolated_environment(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("HERMES_PYTHON", raising=False)
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    acquisition_root = tmp_path / "acquisition"
    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_acquisition_root=acquisition_root,
    )

    assert plan.command_argv[0] == str(Path(sys.executable).resolve(strict=False))
    assert plan.command_argv[0] != "python"
    assert Path(plan.command_argv[0]).is_absolute()
    assert plan.command_argv[1:] == (
        "-m",
        "hermes_cli.main",
        "auth",
        "add",
        "openai-codex",
        "--type",
        "oauth",
    )
    assert plan.public_plan.command_argv_suffix == plan.command_argv[1:]
    assert "--label" not in plan.command_argv
    env = dict(plan.environment_items)
    assert env["HERMES_HOME"] == str(acquisition_root.resolve(strict=False) / "home")
    assert env["HOME"] == env["HERMES_HOME"]
    assert env["USERPROFILE"] == env["HERMES_HOME"]
    assert env["APPDATA"] == str(acquisition_root.resolve(strict=False) / "appdata")
    assert env["LOCALAPPDATA"] == str(
        acquisition_root.resolve(strict=False) / "localappdata"
    )
    assert env["PYTHONIOENCODING"] == "utf-8"
    assert env["PYTHONUTF8"] == "1"
    assert plan.working_directory == product_root.resolve(strict=False)


def test_oauth_plan_uses_controlled_authoritative_python_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("HERMES_PYTHON", raising=False)
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    authoritative_python = Path(sys.executable).resolve(strict=False)

    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_acquisition_root=tmp_path / "acquisition",
        python_executable=authoritative_python,
    )

    assert plan.command_argv[0] == str(authoritative_python)


def test_oauth_plan_uses_valid_hermes_python_before_sys_executable(
    tmp_path: Path,
    monkeypatch,
) -> None:
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    authoritative_python = Path(sys.executable).resolve(strict=False)
    monkeypatch.setenv("HERMES_PYTHON", str(authoritative_python))

    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_acquisition_root=tmp_path / "acquisition",
    )

    assert plan.command_argv[0] == str(authoritative_python)


def test_oauth_plan_ignores_ambient_path_python_when_selecting_child_interpreter(
    tmp_path: Path,
    monkeypatch,
) -> None:
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    fake_bin = tmp_path / "fake-bin"
    fake_bin.mkdir()
    fake_python = fake_bin / "python"
    fake_python.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
    fake_python.chmod(0o755)
    monkeypatch.setenv("PATH", str(fake_bin) + os.pathsep + os.environ.get("PATH", ""))
    monkeypatch.setenv("HERMES_PYTHON", "python")

    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_acquisition_root=tmp_path / "acquisition",
    )

    assert plan.command_argv[0] == str(Path(sys.executable).resolve(strict=False))
    assert plan.command_argv[0] != str(fake_python)
    assert plan.command_argv[0] != "python"


def test_locked_hermes_cli_supports_exact_auth_add_openai_codex_argv() -> None:
    parser_source = AUTH_PARSER_PATH.read_text(encoding="utf-8")
    command_source = AUTH_COMMANDS_PATH.read_text(encoding="utf-8")

    assert (
        'auth_subparsers.add_parser("add", help="Add a pooled credential")'
        in parser_source
    )
    assert 'auth_add.add_argument(\n        "provider"' in parser_source
    assert 'choices=["oauth", "api-key", "api_key"]' in parser_source
    assert 'if provider == "openai-codex":' in command_source
    assert "creds = auth_mod._codex_device_code_login()" in command_source
    codex_block = command_source[
        command_source.index('if provider == "openai-codex":') : command_source.index(
            'if provider == "xai-oauth":'
        )
    ]
    assert "--portal-url" not in codex_block


def test_oauth_acquisition_default_is_dry_run_and_fake_executor_is_explicit(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("HERMES_PYTHON", raising=False)
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_acquisition_root=tmp_path / "acquisition",
    )
    dry_run = run_openai_codex_oauth_acquisition(plan)
    calls: list[tuple[tuple[str, ...], dict[str, str], Path]] = []

    def fake_executor(argv, env, cwd):
        calls.append((tuple(argv), dict(env), cwd))
        return SimpleNamespace(returncode=0, stdout=b"synthetic", stderr=b"")

    executed = run_openai_codex_oauth_acquisition(plan, executor=fake_executor)

    assert dry_run.execution_attempted is False
    assert dry_run.completed is False
    assert executed.execution_attempted is True
    assert executed.completed is True
    assert calls == [
        (plan.command_argv, dict(plan.environment_items), plan.working_directory)
    ]


def test_oauth_acquisition_result_and_plan_repr_do_not_leak_executor_output(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("HERMES_PYTHON", raising=False)
    product_root = tmp_path / "pepper-agent"
    product_root.mkdir()
    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_acquisition_root=tmp_path / "acquisition",
    )
    secret = "synthetic-refresh-token"

    def fake_executor(_argv, _env, _cwd):
        return SimpleNamespace(
            returncode=1,
            stdout=f"access_token={secret}".encode("utf-8"),
            stderr=f"refresh_token={secret}".encode("utf-8"),
        )

    result = run_openai_codex_oauth_acquisition(plan, executor=fake_executor)

    assert result.completed is False
    assert result.stdout_bytes > 0
    assert result.stderr_bytes > 0
    assert secret not in repr(plan)
    assert secret not in str(result)
    assert secret not in repr(result)


def test_oauth_acquisition_source_has_no_provider_call_or_shell_authority() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "subprocess",
        "shell=True",
        "webbrowser",
        "httpx",
        "_codex_device_code_login",
        "resolve_codex_runtime_credentials",
        "OPENAI_API_KEY",
        ".codex",
        "--label",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source
