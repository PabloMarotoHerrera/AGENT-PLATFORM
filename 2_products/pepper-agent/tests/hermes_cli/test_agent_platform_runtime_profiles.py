from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter import profiles
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    DASHBOARD_ENVIRONMENT_POLICY_ID,
    DASHBOARD_FILES_ROOT_POLICY_ID,
    DASHBOARD_READINESS_POLICY_ID,
    DASHBOARD_SHUTDOWN_POLICY_ID,
    DASHBOARD_WORKSPACE_POLICY_ID,
    TEST_ENVIRONMENT_POLICY_ID,
    TEST_READINESS_POLICY_ID,
    TEST_SHUTDOWN_POLICY_ID,
    TEST_WORKSPACE_POLICY_ID,
    RuntimeArgumentSelector,
    RuntimeExecutableSelector,
    RuntimeExecutionScope,
    RuntimeProfileDefinition,
    UnknownRuntimeProfileError,
    get_runtime_profile,
    list_runtime_profile_ids,
    list_runtime_profiles,
)


SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "profiles.py"
)


def test_registry_contains_exact_two_profiles_in_deterministic_order() -> None:
    listed = list_runtime_profiles()

    assert isinstance(listed, tuple)
    assert list_runtime_profile_ids() == (
        ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID,
    )
    assert (
        tuple(profile.profile_ref.profile_id for profile in listed)
        == list_runtime_profile_ids()
    )
    assert len(listed) == 2
    assert get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID) is listed[0]
    assert get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID) is listed[1]

    with pytest.raises(UnknownRuntimeProfileError):
        get_runtime_profile("unknown.profile")


def test_registry_has_no_mutation_or_dynamic_loading_api() -> None:
    forbidden_public_names = {
        "register_runtime_profile",
        "add_runtime_profile",
        "delete_runtime_profile",
        "load_runtime_profiles",
        "discover_runtime_profiles",
        "reload_runtime_profiles",
    }

    assert forbidden_public_names.isdisjoint(dir(profiles))
    assert not hasattr(profiles, "AGENT_PLATFORM_RUNTIME_PROFILE")
    assert not hasattr(profiles, "HERMES_RUNTIME_PROFILE")


def test_profile_definitions_are_immutable_and_have_safe_repr() -> None:
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)

    assert isinstance(profile, RuntimeProfileDefinition)
    with pytest.raises(FrozenInstanceError):
        profile.execution_scope = RuntimeExecutionScope.P14_8_ONLY  # type: ignore[misc]

    representation = repr(profile)
    assert profile.profile_ref.profile_id in representation
    assert profile.profile_ref.environment_policy_id in representation
    assert "current_product_python" not in representation
    assert "lifecycle_probe.py" not in representation
    assert "dashboard" in repr(
        get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    )
    assert "--" not in representation
    assert ":\\" not in representation
    assert "/runtime" not in representation


def test_test_lifecycle_probe_profile_matches_contract() -> None:
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    ref = profile.profile_ref

    assert ref.profile_class is ra.RuntimeProfileClass.TEST_LIFECYCLE_PROBE
    assert (
        profile.executable_selector is RuntimeExecutableSelector.CURRENT_PRODUCT_PYTHON
    )
    assert profile.argument_selector is RuntimeArgumentSelector.LIFECYCLE_PROBE
    assert profile.execution_scope is RuntimeExecutionScope.INERT_TEST_ONLY
    assert ref.environment_policy_id == TEST_ENVIRONMENT_POLICY_ID
    assert ref.workspace_policy_id == TEST_WORKSPACE_POLICY_ID
    assert ref.readiness_policy_id == TEST_READINESS_POLICY_ID
    assert ref.shutdown_policy_id == TEST_SHUTDOWN_POLICY_ID
    assert ref.files_root_policy_id is None
    assert (
        profile.default_workspace_binding.workspace_policy_id
        == TEST_WORKSPACE_POLICY_ID
    )
    assert (
        profile.default_workspace_binding.retention_policy
        is ra.RuntimeRetentionPolicy.REMOVE_ON_TERMINAL
    )
    assert profile.default_workspace_binding.require_managed_files_root is False
    assert profile.timeout_policy.readiness_timeout_ms == 5000
    assert profile.timeout_policy.graceful_shutdown_timeout_ms == 2000
    assert profile.timeout_policy.forced_termination_timeout_ms == 5000
    assert profile.timeout_policy.poll_interval_ms == 100
    assert profile.timeout_policy.max_stdout_bytes == 65_536
    assert profile.timeout_policy.max_stderr_bytes == 65_536


def test_dashboard_provider_null_profile_matches_contract() -> None:
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    ref = profile.profile_ref

    assert ref.profile_class is ra.RuntimeProfileClass.PEPPER_DASHBOARD_PROVIDER_NULL
    assert (
        profile.executable_selector is RuntimeExecutableSelector.CURRENT_PRODUCT_PYTHON
    )
    assert (
        profile.argument_selector
        is RuntimeArgumentSelector.PEPPER_DASHBOARD_PROVIDER_NULL
    )
    assert profile.execution_scope is RuntimeExecutionScope.P14_8_ONLY
    assert ref.environment_policy_id == DASHBOARD_ENVIRONMENT_POLICY_ID
    assert ref.workspace_policy_id == DASHBOARD_WORKSPACE_POLICY_ID
    assert ref.readiness_policy_id == DASHBOARD_READINESS_POLICY_ID
    assert ref.shutdown_policy_id == DASHBOARD_SHUTDOWN_POLICY_ID
    assert ref.files_root_policy_id == DASHBOARD_FILES_ROOT_POLICY_ID
    assert (
        profile.default_workspace_binding.workspace_policy_id
        == DASHBOARD_WORKSPACE_POLICY_ID
    )
    assert (
        profile.default_workspace_binding.retention_policy
        is ra.RuntimeRetentionPolicy.REMOVE_ON_TERMINAL
    )
    assert profile.default_workspace_binding.require_managed_files_root is True
    assert profile.timeout_policy.readiness_timeout_ms == 30_000
    assert profile.timeout_policy.graceful_shutdown_timeout_ms == 5000
    assert profile.timeout_policy.forced_termination_timeout_ms == 10_000
    assert profile.timeout_policy.poll_interval_ms == 250
    assert profile.timeout_policy.max_stdout_bytes == 262_144
    assert profile.timeout_policy.max_stderr_bytes == 262_144


def test_profile_source_contains_no_executable_authority_or_dynamic_discovery() -> None:
    text = SOURCE_PATH.read_text(encoding="utf-8")
    forbidden_text = {
        "sys.executable",
        "subprocess",
        "shell=True",
        "cmd.exe",
        "powershell",
        "argparse",
        "os.environ",
        "os.getenv",
        "entry_points",
        "import_module",
        "glob",
        "dashboard --",
        "127.0.0.1",
        "localhost",
        "provider_api_key",
        "provider_credentials",
        "worker",
        "agent_profile",
        "tool_profile",
        "mcp_profile",
    }
    lowered = text.lower()
    for forbidden in forbidden_text:
        assert forbidden.lower() not in lowered, forbidden

    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = {alias.name for alias in node.names}
            assert imported.isdisjoint({"os", "sys", "subprocess", "importlib"})
        if isinstance(node, ast.ImportFrom):
            assert node.module not in {"os", "sys", "subprocess", "importlib"}


def test_root_export_remains_contract_only_for_profile_registry() -> None:
    assert not hasattr(ra, "RuntimeProfileDefinition")
    assert not hasattr(ra, "get_runtime_profile")
    assert "RuntimeProfileDefinition" not in ra.__all__
    assert "get_runtime_profile" not in ra.__all__
    assert ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION == 1
