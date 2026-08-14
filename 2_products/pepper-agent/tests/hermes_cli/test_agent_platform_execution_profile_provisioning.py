from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest
import yaml

from hermes_cli.agent_platform.auth_commands import agent_platform_command
from hermes_cli.agent_platform.execution_profile_provisioning import (
    CANONICAL_PROFILE_CONTRACT_MISMATCH,
    HUMAN_PROFILE_SELECTION_REQUIRED,
    PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
    PROFILE_ALREADY_PRESENT,
    PROFILE_PROVISIONED,
    PepperExecutionProfileProvisioningError,
    READY_FOR_HUMAN_PROVISIONING,
    READY_FOR_P18_9_1_PROJECTION,
    canonical_pepper_implementation_profile_contract,
    inspect_pepper_implementation_profile_provisioning,
    provision_pepper_implementation_profile,
    validate_pepper_implementation_profile_contract,
)
from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as projection
from hermes_cli.subcommands.agent_platform import build_agent_platform_parser


@pytest.fixture()
def profile_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    home = tmp_path / ".hermes"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))
    return home


def _write_profile(
    home: Path,
    name: str,
    *,
    description: str = "Pepper product implementation execution profile",
    cli_toolsets: list[str] | None = None,
    model: dict | None = None,
) -> Path:
    profile_dir = home / "profiles" / name
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "profile.yaml").write_text(
        yaml.safe_dump(
            {"description": description, "description_auto": False},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    config = {
        "model": model
        or {
            "provider": "openai-codex",
            "default": "gpt-5.5",
            "api_mode": "codex_responses",
        },
    }
    if cli_toolsets is not None:
        config["platform_toolsets"] = {"cli": cli_toolsets}
    (profile_dir / "config.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False),
        encoding="utf-8",
    )
    return profile_dir


def test_canonical_contract_is_bounded_and_secret_free() -> None:
    contract = canonical_pepper_implementation_profile_contract()
    serialized = json.dumps(contract, sort_keys=True)

    assert contract["profile_name"] == "pepper-implementation-product"
    assert contract["role"] == "implementation_product"
    assert contract["stored_toolsets"] == ["pepper_repository", "file"]
    assert contract["stored_sentinels"] == ["no_mcp"]
    assert contract["config_toolsets"] == ["pepper_repository", "file", "no_mcp"]
    assert contract["effective_worker_toolsets"] == [
        "kanban",
        "pepper_repository",
        "file",
        "pepper_validation",
    ]
    assert contract["runtime_injected_toolsets"] == ["pepper_validation"]
    assert contract["provider"] == "openai-codex"
    assert contract["model"] == "gpt-5.5"
    assert contract["api_mode"] == "codex_responses"
    assert contract["credential_profile_id"] == "openai-codex.primary"
    assert contract["legacy_auth_json_used"] is False
    assert contract["API_key_fallback_used"] is False
    assert "OPENAI_API_KEY" not in serialized
    assert "access_token" not in serialized
    assert "refresh_token" not in serialized
    for forbidden in ("terminal", "process", "git", "docker", "graphify"):
        assert forbidden in contract["forbidden_toolsets"]
        assert forbidden not in contract["config_toolsets"]


def test_status_candidate_count_zero_ready_for_human_provisioning(profile_env: Path) -> None:
    inspection = inspect_pepper_implementation_profile_provisioning()

    assert inspection["status"] == READY_FOR_HUMAN_PROVISIONING
    assert inspection["canonical_profile_exists"] is False
    assert inspection["canonical_profile"] == PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME
    assert inspection["candidate_count"] == 0
    assert inspection["candidate_profiles"] == []
    assert inspection["projection_performed"] is False
    assert inspection["dispatch_performed"] is False
    assert inspection["worker_execution"] is False
    assert inspection["Git_mutation"] is False
    assert inspection["Docker_invocation"] is False
    assert inspection["Graphify_invocation"] is False


def test_provisioner_creates_canonical_profile_with_bounded_surface(profile_env: Path) -> None:
    result = provision_pepper_implementation_profile()
    profile_dir = profile_env / "profiles" / PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME
    config = yaml.safe_load((profile_dir / "config.yaml").read_text(encoding="utf-8"))
    validation = validate_pepper_implementation_profile_contract(profile_dir)
    classification = projection.classify_pepper_execution_profile({
        "name": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        "path": profile_dir,
        "description": "Pepper product implementation execution profile",
        "is_default": False,
    })

    assert result["provisioning_status"] == PROFILE_PROVISIONED
    assert result["created"] is True
    assert result["status"] == READY_FOR_P18_9_1_PROJECTION
    assert result["candidate_count"] == 1
    assert config["model"] == {
        "provider": "openai-codex",
        "default": "gpt-5.5",
        "api_mode": "codex_responses",
    }
    assert config["platform_toolsets"]["cli"] == [
        "pepper_repository",
        "file",
        "no_mcp",
    ]
    assert "pepper_validation" not in config["platform_toolsets"]["cli"]
    assert "kanban" not in config["platform_toolsets"]["cli"]
    assert validation["ok"] is True
    assert validation["provider_runtime"] == {
        "provider": "openai-codex",
        "model": "gpt-5.5",
        "api_mode": "codex_responses",
        "credential_profile_id": "openai-codex.primary",
        "credential_policy_revision": "provider-runtime-v1.provider-worker-v1.provider-credential-v1",
        "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
        "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
        "executor_config_source": "executor_profile_config_yaml",
    }
    assert validation["legacy_auth_json_used"] is False
    assert validation["API_key_fallback_used"] is False
    assert classification["role"] == "implementation_product"
    assert classification["worker_assignable"] is True
    assert classification["cli_toolsets"] == ["pepper_repository", "file"]
    assert classification["rejection_reasons"] == []


def test_provisioner_is_idempotent_when_profile_matches(profile_env: Path) -> None:
    first = provision_pepper_implementation_profile()
    second = provision_pepper_implementation_profile()

    assert first["provisioning_status"] == PROFILE_PROVISIONED
    assert second["provisioning_status"] == PROFILE_ALREADY_PRESENT
    assert second["created"] is False
    assert second["candidate_count"] == 1


def test_provisioner_rejects_divergent_same_name_profile(profile_env: Path) -> None:
    profile_dir = _write_profile(
        profile_env,
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        cli_toolsets=["pepper_repository", "terminal", "no_mcp"],
    )

    inspection = inspect_pepper_implementation_profile_provisioning()
    with pytest.raises(PepperExecutionProfileProvisioningError) as exc_info:
        provision_pepper_implementation_profile()

    assert inspection["status"] == CANONICAL_PROFILE_CONTRACT_MISMATCH
    assert "config_cli_toolsets_mismatch" in inspection[
        "canonical_profile_validation"
    ]["rejection_reasons"]
    assert "unbounded_toolsets:terminal" in inspection[
        "canonical_profile_validation"
    ]["rejection_reasons"]
    assert exc_info.value.validation_category == "canonical_profile_contract_mismatch"
    assert yaml.safe_load((profile_dir / "config.yaml").read_text(encoding="utf-8"))[
        "platform_toolsets"
    ]["cli"] == ["pepper_repository", "terminal", "no_mcp"]


def test_architecture_profile_is_not_implementation_candidate(profile_env: Path) -> None:
    _write_profile(
        profile_env,
        "pepper-architecture-product",
        description="Pepper product architecture execution profile",
        cli_toolsets=["pepper_repository", "no_mcp"],
    )

    inspection = inspect_pepper_implementation_profile_provisioning()

    assert inspection["status"] == READY_FOR_HUMAN_PROVISIONING
    assert inspection["candidate_count"] == 0
    architecture = next(
        item
        for item in inspection["available_profiles"]
        if item["canonical_name"] == "pepper-architecture-product"
    )
    assert architecture["role"] == "architecture_product"
    assert architecture["worker_assignable"] is True


def test_candidate_count_one_ready_for_projection_without_projection(profile_env: Path) -> None:
    _write_profile(
        profile_env,
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        cli_toolsets=["pepper_repository", "file", "no_mcp"],
    )

    inspection = inspect_pepper_implementation_profile_provisioning()

    assert inspection["status"] == READY_FOR_P18_9_1_PROJECTION
    assert inspection["candidate_count"] == 1
    assert inspection["candidate_profiles"] == [PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME]
    assert inspection["projection_performed"] is False
    assert inspection["dispatch_performed"] is False
    assert inspection["worker_execution"] is False


def test_multiple_implementation_candidates_require_human_selection(profile_env: Path) -> None:
    _write_profile(
        profile_env,
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        cli_toolsets=["pepper_repository", "file", "no_mcp"],
    )
    _write_profile(
        profile_env,
        "pepper-routing-implementation",
        description="Pepper routing product implementation execution profile",
        cli_toolsets=["pepper_repository", "file", "no_mcp"],
    )

    inspection = inspect_pepper_implementation_profile_provisioning()

    assert inspection["status"] == HUMAN_PROFILE_SELECTION_REQUIRED
    assert inspection["candidate_count"] == 2
    assert inspection["candidate_profiles"] == [
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        "pepper-routing-implementation",
    ]


def test_profile_status_command_is_read_only(profile_env: Path, capsys) -> None:
    args = argparse.Namespace(
        agent_platform_action="profile",
        agent_platform_profile_action="status",
        profile=PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
    )

    assert agent_platform_command(args) == 0
    output = capsys.readouterr().out

    assert "Status: READY_FOR_HUMAN_PROVISIONING" in output
    assert "Candidate count: 0" in output
    assert not (profile_env / "profiles" / PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME).exists()


def test_agent_platform_parser_accepts_profile_provision_command() -> None:
    parser = argparse.ArgumentParser(prog="hermes")
    subparsers = parser.add_subparsers(dest="command")
    build_agent_platform_parser(subparsers, cmd_agent_platform=agent_platform_command)

    args = parser.parse_args([
        "agent-platform",
        "profile",
        "provision",
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
    ])

    assert args.command == "agent-platform"
    assert args.agent_platform_action == "profile"
    assert args.agent_platform_profile_action == "provision"
    assert args.profile == PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME
