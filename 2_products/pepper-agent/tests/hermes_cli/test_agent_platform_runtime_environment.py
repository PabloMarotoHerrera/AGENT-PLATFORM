from __future__ import annotations

import ast
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.environment import (
    DASHBOARD_ENVIRONMENT_POLICY_ID,
    TEST_ENVIRONMENT_POLICY_ID,
    ForbiddenRuntimeEnvironmentVariableError,
    InvalidRuntimeEnvironmentPathError,
    InvalidRuntimeEnvironmentVariableError,
    MissingRuntimeBootstrapVariableError,
    RuntimeEnvironmentPaths,
    RuntimeEnvironmentSanitizationReport,
    RuntimeEnvironmentTooLargeError,
    RuntimePlatformFamily,
    SanitizedRuntimeEnvironment,
    sanitize_runtime_environment,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    ResolvedProcessLaunchPlan,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    DASHBOARD_ENVIRONMENT_POLICY_ID as DASHBOARD_POLICY_ID_FROM_PROFILES,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    TEST_ENVIRONMENT_POLICY_ID as TEST_POLICY_ID_FROM_PROFILES,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    get_runtime_profile,
    list_runtime_profiles,
)


SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "environment.py"
)
PROFILE_SOURCE_PATH = SOURCE_PATH.with_name("profiles.py")


def windows_paths(
    *, files_root: str | None = r"D:\rt\files"
) -> RuntimeEnvironmentPaths:
    return RuntimeEnvironmentPaths(
        hermes_home=r"D:\rt\hermes-home",
        home=r"D:\rt\home",
        user_profile=r"D:\rt\user-profile",
        app_data=r"D:\rt\app-data",
        local_app_data=r"D:\rt\local-app-data",
        temp=r"D:\rt\temp",
        files_root=files_root,
    )


def posix_paths(*, files_root: str | None = "/rt/files") -> RuntimeEnvironmentPaths:
    return RuntimeEnvironmentPaths(
        hermes_home="/rt/hermes-home",
        home="/rt/home",
        user_profile="/rt/user-profile",
        app_data="/rt/app-data",
        local_app_data="/rt/local-app-data",
        temp="/rt/temp",
        files_root=files_root,
    )


def test_windows_managed_home_variables_override_source_and_bootstrap_is_narrow() -> (
    None
):
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    source = {
        "SystemRoot": r"C:\Windows",
        "HOME": r"C:\Users\real",
        "USERPROFILE": r"C:\Users\real",
        "HERMES_HOME": r"C:\Users\real\.hermes",
        "APPDATA": r"C:\Users\real\AppData\Roaming",
        "LOCALAPPDATA": r"C:\Users\real\AppData\Local",
        "TEMP": r"C:\Users\real\Temp",
        "TMP": r"C:\Users\real\Temp",
        "TMPDIR": r"C:\Users\real\Temp",
        "PATH": r"C:\untrusted",
    }

    sanitized = sanitize_runtime_environment(
        profile=profile,
        platform_family=RuntimePlatformFamily.WINDOWS,
        source_environment=source,
        paths=windows_paths(),
    )
    output = sanitized.as_mapping()

    assert output["HOME"] == r"D:\rt\home"
    assert output["USERPROFILE"] == r"D:\rt\user-profile"
    assert output["HERMES_HOME"] == r"D:\rt\hermes-home"
    assert output["APPDATA"] == r"D:\rt\app-data"
    assert output["LOCALAPPDATA"] == r"D:\rt\local-app-data"
    assert output["TEMP"] == r"D:\rt\temp"
    assert output["TMP"] == r"D:\rt\temp"
    assert output["TMPDIR"] == r"D:\rt\temp"
    assert output["HOMEDRIVE"] == "D:"
    assert output["HOMEPATH"] == r"\rt\user-profile"
    assert output["SystemRoot"] == r"C:\Windows"
    assert output["WINDIR"] == r"C:\Windows"
    assert "PATH" not in output
    assert sanitized.report.inherited_variable_names == ("SystemRoot", "WINDIR")
    assert sanitized.report.managed_home_bound is True

    with pytest.raises(MissingRuntimeBootstrapVariableError):
        sanitize_runtime_environment(
            profile=profile,
            platform_family=RuntimePlatformFamily.WINDOWS,
            source_environment={},
            paths=windows_paths(),
        )
    with pytest.raises(InvalidRuntimeEnvironmentVariableError):
        sanitize_runtime_environment(
            profile=profile,
            platform_family=RuntimePlatformFamily.WINDOWS,
            source_environment={
                "Path": "one",
                "PATH": "two",
                "SystemRoot": r"C:\Windows",
            },
            paths=windows_paths(),
        )


def test_posix_inherits_no_source_variables_by_default() -> None:
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    source = {
        "HOME": "/real/home",
        "PATH": "/usr/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "USER": "real-user",
        "LOGNAME": "real-user",
        "SHELL": "/bin/sh",
    }

    sanitized = sanitize_runtime_environment(
        profile=profile,
        platform_family=RuntimePlatformFamily.POSIX,
        source_environment=source,
        paths=posix_paths(files_root=None),
    )
    output = sanitized.as_mapping()

    assert output["HOME"] == "/rt/home"
    assert output["HERMES_HOME"] == "/rt/hermes-home"
    assert output["TEMP"] == "/rt/temp"
    assert output["TMP"] == "/rt/temp"
    assert output["TMPDIR"] == "/rt/temp"
    for key in source:
        if key not in {"HOME"}:
            assert key not in output
    assert "PATH" not in output
    assert sanitized.report.inherited_variable_names == ()
    assert sanitized.report.managed_home_bound is True


def test_explicit_path_policy_is_profile_scoped_and_deterministic() -> None:
    test_profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    dashboard_profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)

    with pytest.raises(ForbiddenRuntimeEnvironmentVariableError):
        sanitize_runtime_environment(
            profile=test_profile,
            platform_family=RuntimePlatformFamily.POSIX,
            source_environment={},
            paths=posix_paths(files_root=None),
            explicit_path_entries=("/rt/bin",),
        )

    no_path = sanitize_runtime_environment(
        profile=dashboard_profile,
        platform_family=RuntimePlatformFamily.POSIX,
        source_environment={},
        paths=posix_paths(),
    )
    assert "PATH" not in no_path.as_mapping()

    sanitized = sanitize_runtime_environment(
        profile=dashboard_profile,
        platform_family=RuntimePlatformFamily.POSIX,
        source_environment={},
        paths=posix_paths(),
        explicit_path_entries=("/rt/bin", "/rt/node/bin"),
    )
    assert sanitized.as_mapping()["PATH"] == "/rt/bin:/rt/node/bin"
    assert sanitized.report.explicit_path_entry_count == 2

    with pytest.raises(InvalidRuntimeEnvironmentPathError):
        sanitize_runtime_environment(
            profile=dashboard_profile,
            platform_family=RuntimePlatformFamily.POSIX,
            source_environment={},
            paths=posix_paths(),
            explicit_path_entries=("relative/bin",),
        )
    with pytest.raises(InvalidRuntimeEnvironmentVariableError):
        sanitize_runtime_environment(
            profile=dashboard_profile,
            platform_family=RuntimePlatformFamily.WINDOWS,
            source_environment={"SystemRoot": r"C:\Windows"},
            paths=windows_paths(),
            explicit_path_entries=(r"D:\Tools", r"d:\tools"),
        )


def test_secret_provider_proxy_and_injection_variables_are_excluded() -> None:
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    denied_value = "secret-value-must-not-appear"
    source = {
        "SystemRoot": r"C:\Windows",
        "OPENAI_API_KEY": denied_value,
        "AWS_SECRET_ACCESS_KEY": denied_value,
        "GIT_ASKPASS": denied_value,
        "SSH_AUTH_SOCK": denied_value,
        "MCP_SERVER_TOKEN": denied_value,
        "DATABASE_URL": denied_value,
        "NPM_TOKEN": denied_value,
        "HTTPS_PROXY": denied_value,
        "PYTHONPATH": denied_value,
        "NODE_OPTIONS": denied_value,
        "LD_PRELOAD": denied_value,
        "DYLD_INSERT_LIBRARIES": denied_value,
    }

    sanitized = sanitize_runtime_environment(
        profile=profile,
        platform_family=RuntimePlatformFamily.WINDOWS,
        source_environment=source,
        paths=windows_paths(),
    )
    output = sanitized.as_mapping()
    serialized_output = " ".join(f"{key}={value}" for key, value in output.items())

    assert denied_value not in serialized_output
    assert denied_value not in repr(sanitized)
    assert denied_value not in repr(sanitized.report)
    assert sanitized.report.provider_variables_present_in_output is False
    assert "OPENAI_API_KEY" in sanitized.report.excluded_sensitive_variable_names
    assert "HTTPS_PROXY" in sanitized.report.excluded_sensitive_variable_names
    assert sanitized.report.excluded_variable_count == len(source) - 1


def test_files_root_policy_is_profile_specific_and_lexical_only() -> None:
    test_profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    dashboard_profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)

    test_env = sanitize_runtime_environment(
        profile=test_profile,
        platform_family=RuntimePlatformFamily.POSIX,
        source_environment={},
        paths=posix_paths(files_root=None),
    )
    assert test_env.report.managed_files_root_required is False
    assert test_env.report.managed_files_root_supplied is False

    with pytest.raises(InvalidRuntimeEnvironmentPathError):
        sanitize_runtime_environment(
            profile=dashboard_profile,
            platform_family=RuntimePlatformFamily.POSIX,
            source_environment={},
            paths=posix_paths(files_root=None),
        )
    with pytest.raises(InvalidRuntimeEnvironmentPathError):
        sanitize_runtime_environment(
            profile=dashboard_profile,
            platform_family=RuntimePlatformFamily.WINDOWS,
            source_environment={"SystemRoot": r"C:\Windows"},
            paths=windows_paths(files_root=r"..\escape"),
        )


def test_environment_output_is_immutable_deterministic_and_copy_safe() -> None:
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    source = {"SystemRoot": r"C:\Windows", "OPENAI_API_KEY": "secret"}
    source_copy = dict(source)

    sanitized = sanitize_runtime_environment(
        profile=profile,
        platform_family=RuntimePlatformFamily.WINDOWS,
        source_environment=source,
        paths=windows_paths(),
        explicit_path_entries=(r"D:\runtime\bin",),
    )
    assert source == source_copy
    assert isinstance(sanitized.items, tuple)
    assert all(isinstance(item, tuple) for item in sanitized.items)
    assert sanitized.items == tuple(
        sorted(sanitized.items, key=lambda item: item[0].casefold())
    )

    first_mapping = sanitized.as_mapping()
    second_mapping = sanitized.as_mapping()
    assert first_mapping == second_mapping
    assert first_mapping is not second_mapping
    first_mapping["HOME"] = r"C:\mutated"
    assert sanitized.as_mapping()["HOME"] == r"D:\rt\home"

    with pytest.raises(FrozenInstanceError):
        sanitized.profile_id = "other"  # type: ignore[misc]
    assert r"D:\rt\home" not in repr(sanitized)
    assert r"D:\rt\home" not in repr(sanitized.report)


def test_environment_bounds_and_invalid_names_values_are_rejected() -> None:
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    with pytest.raises(RuntimeEnvironmentTooLargeError):
        sanitize_runtime_environment(
            profile=profile,
            platform_family=RuntimePlatformFamily.POSIX,
            source_environment={f"K{i}": "v" for i in range(4097)},
            paths=posix_paths(),
        )
    for bad_source in ({"": "v"}, {"A=B": "v"}, {"BAD\nNAME": "v"}):
        with pytest.raises(InvalidRuntimeEnvironmentVariableError):
            sanitize_runtime_environment(
                profile=profile,
                platform_family=RuntimePlatformFamily.POSIX,
                source_environment=bad_source,
                paths=posix_paths(),
            )
    with pytest.raises(InvalidRuntimeEnvironmentPathError):
        sanitize_runtime_environment(
            profile=profile,
            platform_family=RuntimePlatformFamily.POSIX,
            source_environment={},
            paths=posix_paths(files_root="/rt/bad\x00files"),
        )
    with pytest.raises(RuntimeEnvironmentTooLargeError):
        sanitize_runtime_environment(
            profile=profile,
            platform_family=RuntimePlatformFamily.POSIX,
            source_environment={},
            paths=posix_paths(),
            explicit_path_entries=tuple(f"/rt/bin{i}" for i in range(17)),
        )

    report = RuntimeEnvironmentSanitizationReport(
        profile_id="profile",
        environment_policy_id="policy",
        platform_family=RuntimePlatformFamily.WINDOWS,
        source_variable_count=0,
        output_variable_count=100,
        inherited_variable_names=(),
        managed_variable_names=(),
        fixed_variable_names=(),
        explicit_path_entry_count=0,
        excluded_variable_count=0,
        excluded_sensitive_variable_names=(),
        managed_home_bound=True,
        managed_files_root_required=False,
        managed_files_root_supplied=False,
        provider_variables_present_in_output=False,
    )
    with pytest.raises(RuntimeEnvironmentTooLargeError):
        SanitizedRuntimeEnvironment(
            profile_id="profile",
            environment_policy_id="policy",
            platform_family=RuntimePlatformFamily.WINDOWS,
            items=tuple((f"K{i:03d}", "v" * 300) for i in range(100)),
            report=report,
        )


def test_profile_environment_policy_ids_resolve_and_fit_launch_plan_shape(
    tmp_path: Path,
) -> None:
    policy_ids = {TEST_ENVIRONMENT_POLICY_ID, DASHBOARD_ENVIRONMENT_POLICY_ID}
    assert policy_ids == {
        TEST_POLICY_ID_FROM_PROFILES,
        DASHBOARD_POLICY_ID_FROM_PROFILES,
    }

    for profile in list_runtime_profiles():
        assert profile.profile_ref.environment_policy_id in policy_ids
        assert isinstance(profile.timeout_policy, ra.RuntimeTimeoutPolicy)
        assert isinstance(profile.default_workspace_binding, ra.RuntimeWorkspaceBinding)

    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    sanitized = sanitize_runtime_environment(
        profile=profile,
        platform_family=RuntimePlatformFamily.POSIX,
        source_environment={},
        paths=posix_paths(files_root=None),
    )
    plan = ResolvedProcessLaunchPlan(
        profile_id=profile.profile_ref.profile_id,
        workspace_id="workspace-001",
        executable=sys.executable,
        arguments=(),
        working_directory=str(tmp_path),
        environment_items=sanitized.items,
        stdout_limit_bytes=profile.timeout_policy.max_stdout_bytes,
        stderr_limit_bytes=profile.timeout_policy.max_stderr_bytes,
    )
    assert plan.environment_items == sanitized.items


def test_environment_source_guard_blocks_side_effects_and_parent_env_reads() -> None:
    for source_path in (SOURCE_PATH, PROFILE_SOURCE_PATH):
        text = source_path.read_text(encoding="utf-8")
        lowered = text.lower()
        forbidden_text = {
            "os.environ",
            "os.getenv",
            "os.putenv",
            "os.unsetenv",
            "dotenv",
            "subprocess",
            "create_subprocess",
            "multiprocessing",
            "threading",
            "signal",
            "socket",
            "requests",
            "httpx",
            "urllib.request",
            "shutil",
            "tempfile",
            ".mkdir",
            "makedirs",
            "unlink",
            "rmdir",
            "remove(",
            "rename(",
            "replace(",
            "chdir",
            "path.home",
            "expanduser",
            "getpass",
            "logger.",
            "logging.",
            "hermes_runtime_profile",
            "agent_platform_runtime_profile",
        }
        for forbidden in forbidden_text:
            assert forbidden not in lowered, (source_path, forbidden)

        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name for alias in node.names}
                assert imported.isdisjoint({"os", "subprocess", "threading", "signal"})
            if isinstance(node, ast.ImportFrom):
                assert node.module not in {"os", "subprocess", "threading", "signal"}


def test_root_export_remains_contract_only_for_environment_sanitizer() -> None:
    assert not hasattr(ra, "RuntimeEnvironmentPaths")
    assert not hasattr(ra, "sanitize_runtime_environment")
    assert "RuntimeEnvironmentPaths" not in ra.__all__
    assert "sanitize_runtime_environment" not in ra.__all__
