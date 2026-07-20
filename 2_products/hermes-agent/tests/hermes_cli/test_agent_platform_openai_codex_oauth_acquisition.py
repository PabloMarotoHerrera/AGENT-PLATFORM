from __future__ import annotations

from pathlib import Path
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


def write_fake_product_python(product_root: Path) -> Path:
    python_path = product_root / ".venv" / "Scripts" / "python.exe"
    python_path.parent.mkdir(parents=True)
    python_path.write_text("", encoding="utf-8")
    return python_path


def test_oauth_plan_uses_product_local_python_and_fixed_no_label_argv(
    tmp_path: Path,
) -> None:
    product_root = tmp_path / "hermes-agent"
    product_python = write_fake_product_python(product_root)
    store_root = tmp_path / "governed-store"
    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_store_root=store_root,
    )

    assert plan.command_argv == (
        str(product_python.resolve(strict=False)),
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
    assert dict(plan.environment_items) == {
        "HERMES_HOME": str(store_root.resolve(strict=False)),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    }


def test_locked_hermes_cli_supports_exact_auth_add_openai_codex_argv() -> None:
    parser_source = AUTH_PARSER_PATH.read_text(encoding="utf-8")
    command_source = AUTH_COMMANDS_PATH.read_text(encoding="utf-8")

    assert (
        'auth_subparsers.add_parser("add", help="Add a pooled credential")'
        in parser_source
    )
    assert 'auth_add.add_argument(\n        "provider"' in parser_source
    assert 'choices=["oauth", "api-key", "api_key"]' in parser_source
    assert (
        'auth_add.add_argument("--label", help="Optional display label")'
        in parser_source
    )
    assert 'if provider == "openai-codex":' in command_source
    assert "creds = auth_mod._codex_device_code_login()" in command_source
    assert (
        "--portal-url"
        not in command_source[
            command_source.index(
                'if provider == "openai-codex":'
            ) : command_source.index('if provider == "xai-oauth":')
        ]
    )


def test_oauth_acquisition_default_is_dry_run_and_fake_executor_is_explicit(
    tmp_path: Path,
) -> None:
    product_root = tmp_path / "hermes-agent"
    write_fake_product_python(product_root)
    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root,
        trusted_store_root=tmp_path / "store",
    )
    dry_run = run_openai_codex_oauth_acquisition(plan)
    calls: list[tuple[tuple[str, ...], dict[str, str]]] = []

    def fake_executor(argv, env):
        calls.append((tuple(argv), dict(env)))
        return SimpleNamespace(returncode=0, stdout=b"synthetic", stderr=b"")

    executed = run_openai_codex_oauth_acquisition(plan, executor=fake_executor)

    assert dry_run.execution_attempted is False
    assert dry_run.completed is False
    assert executed.execution_attempted is True
    assert executed.completed is True
    assert calls == [(plan.command_argv, dict(plan.environment_items))]


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
