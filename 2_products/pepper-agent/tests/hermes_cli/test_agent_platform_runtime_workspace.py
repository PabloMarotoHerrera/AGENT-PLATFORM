from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.environment import (
    RuntimePlatformFamily,
    sanitize_runtime_environment,
)
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    PathOutsideContainmentRootError,
    PathRedirectDetectedError,
    assert_existing_path_contained,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    ResolvedProcessLaunchPlan,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    DASHBOARD_WORKSPACE_POLICY_ID,
    TEST_WORKSPACE_POLICY_ID,
    RuntimeExecutionScope,
    get_runtime_profile,
    list_runtime_profiles,
)
from hermes_cli.agent_platform.runtime_adapter import workspace as ws
from hermes_cli.agent_platform.runtime_adapter.workspace import (
    DuplicateRuntimeWorkspaceError,
    RuntimeFilesRootBinding,
    RuntimeWorkspaceAllocator,
    RuntimeWorkspaceScope,
    UnknownRuntimeWorkspaceError,
    UnknownWorkspacePolicyError,
    WorkspaceAllocationCompensationError,
    WorkspaceAllocationError,
    WorkspaceAlreadyExistsError,
    WorkspaceIdGenerationError,
    WorkspaceMarkerError,
    get_runtime_workspace_policy,
    list_runtime_workspace_policies,
    list_runtime_workspace_policy_ids,
    validate_managed_files_path,
)


SOURCE_PATHS = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "workspace.py",
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "path_containment.py",
)
MARKER_NAME = ".agent-platform-runtime-workspace.json"


def id_factory(token: str):
    return lambda: "ws_" + token


def sequence_factory(*tokens: str):
    values = iter("ws_" + token for token in tokens)
    return lambda: next(values)


def platform_family() -> RuntimePlatformFamily:
    if sys.platform == "win32":
        return RuntimePlatformFamily.WINDOWS
    return RuntimePlatformFamily.POSIX


def synthetic_source() -> dict[str, str]:
    if platform_family() is RuntimePlatformFamily.WINDOWS:
        return {"SystemRoot": r"C:\Windows", "OPENAI_API_KEY": "secret"}
    return {"OPENAI_API_KEY": "secret"}


def make_allocator(tmp_path: Path, token: str = "a" * 32) -> RuntimeWorkspaceAllocator:
    base = tmp_path / "base"
    base.mkdir()
    return RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory(token),
    )


def test_workspace_policy_registry_contains_exact_two_immutable_policies() -> None:
    policies = list_runtime_workspace_policies()
    assert list_runtime_workspace_policy_ids() == (
        TEST_WORKSPACE_POLICY_ID,
        DASHBOARD_WORKSPACE_POLICY_ID,
    )
    assert len(policies) == 2
    assert get_runtime_workspace_policy(TEST_WORKSPACE_POLICY_ID) is policies[0]
    assert get_runtime_workspace_policy(DASHBOARD_WORKSPACE_POLICY_ID) is policies[1]
    assert policies[0].scope is RuntimeWorkspaceScope.INERT_TEST_TEMPORARY
    assert policies[1].scope is RuntimeWorkspaceScope.P14_8_ARTIFACT_ONLY
    assert policies[0].directory_layout == (
        "home",
        "user-profile",
        "hermes-home",
        "appdata",
        "localappdata",
        "temp",
        "logs",
        "state",
        "evidence",
        "workdir",
    )
    assert policies[1].directory_layout == (*policies[0].directory_layout, "files-root")
    assert policies[0].require_managed_files_root is False
    assert policies[1].require_managed_files_root is True
    assert policies[0].ownership_marker_required is True
    assert policies[1].ownership_marker_required is True
    with pytest.raises(UnknownWorkspacePolicyError):
        get_runtime_workspace_policy("runtime.workspace.unknown.v1")
    assert not hasattr(ws, "register_runtime_workspace_policy")
    assert not hasattr(ws, "load_runtime_workspace_policies")


def test_profile_workspace_policy_ids_resolve_and_scopes_match() -> None:
    for profile in list_runtime_profiles():
        policy = get_runtime_workspace_policy(profile.profile_ref.workspace_policy_id)
        if profile.execution_scope is RuntimeExecutionScope.INERT_TEST_ONLY:
            assert policy.scope is RuntimeWorkspaceScope.INERT_TEST_TEMPORARY
        elif profile.execution_scope is RuntimeExecutionScope.P14_8_ONLY:
            assert policy.scope is RuntimeWorkspaceScope.P14_8_ARTIFACT_ONLY
        assert (
            profile.default_workspace_binding.require_managed_files_root
            is policy.require_managed_files_root
        )


def test_test_workspace_allocation_creates_exact_layout_without_files_root(
    tmp_path: Path,
) -> None:
    allocator = make_allocator(tmp_path, "1" * 32)
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.test.001", profile=profile)

    assert allocation.workspace_ref.workspace_id == "ws_" + "1" * 32
    assert allocation.workspace_ref.status is ra.RuntimeWorkspaceStatus.ALLOCATED
    assert allocation.workspace_ref.managed_files_root_bound is False
    assert allocation.files_root_binding is None
    assert allocation.paths.files_root is None
    assert not (allocation.paths.workspace_root / "files-root").exists()
    for segment in get_runtime_workspace_policy(
        TEST_WORKSPACE_POLICY_ID
    ).directory_layout:
        assert (allocation.paths.workspace_root / segment).is_dir()
    assert allocation.paths.ownership_marker.name == MARKER_NAME
    assert allocator.get("runtime.test.001") is allocation
    assert allocator.allocated_runtime_ids() == ("runtime.test.001",)


def test_dashboard_workspace_allocation_creates_locked_files_root(
    tmp_path: Path,
) -> None:
    allocator = make_allocator(tmp_path, "2" * 32)
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.dashboard.001", profile=profile)
    binding = allocation.files_root_binding

    assert allocation.workspace_ref.status is ra.RuntimeWorkspaceStatus.ALLOCATED
    assert allocation.workspace_ref.managed_files_root_bound is True
    assert isinstance(binding, RuntimeFilesRootBinding)
    assert allocation.paths.files_root is not None
    assert allocation.paths.files_root.is_dir()
    assert binding.default_path == binding.locked_root
    assert binding.can_change_path is False
    assert binding.locked_root == allocation.paths.files_root
    for segment in get_runtime_workspace_policy(
        DASHBOARD_WORKSPACE_POLICY_ID
    ).directory_layout:
        assert (allocation.paths.workspace_root / segment).is_dir()


def test_marker_is_deterministic_bounded_and_contains_no_paths(tmp_path: Path) -> None:
    allocator = make_allocator(tmp_path, "3" * 32)
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.marker.001", profile=profile)
    marker_text = allocation.paths.ownership_marker.read_text(encoding="utf-8")
    marker = json.loads(marker_text)

    assert allocation.paths.ownership_marker.name == MARKER_NAME
    assert marker_text.endswith("\n")
    assert (
        marker_text == json.dumps(marker, sort_keys=True, separators=(",", ":")) + "\n"
    )
    assert marker == {
        "schema_version": 1,
        "runtime_id": "runtime.marker.001",
        "workspace_id": allocation.workspace_ref.workspace_id,
        "workspace_policy_id": DASHBOARD_WORKSPACE_POLICY_ID,
    }
    forbidden_fragments = {
        str(allocation.paths.workspace_root),
        "HERMES_HOME",
        "PATH",
        "OPENAI",
        "provider_api_key",
        "provider_credentials",
        "command",
        "arguments",
    }
    for fragment in forbidden_fragments:
        assert fragment not in marker_text


def test_duplicate_collision_invalid_id_and_unknown_lookup_fail_closed(
    tmp_path: Path,
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory("4" * 32),
    )
    allocator.allocate(runtime_id="runtime.duplicate.001", profile=profile)
    with pytest.raises(DuplicateRuntimeWorkspaceError):
        allocator.allocate(runtime_id="runtime.duplicate.001", profile=profile)
    with pytest.raises(WorkspaceAlreadyExistsError):
        allocator.allocate(runtime_id="runtime.duplicate.002", profile=profile)
    with pytest.raises(UnknownRuntimeWorkspaceError):
        allocator.get("runtime.unknown.001")

    invalid_allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=lambda: "invalid/path",
    )
    with pytest.raises(WorkspaceIdGenerationError):
        invalid_allocator.allocate(runtime_id="runtime.invalid.001", profile=profile)

    existing_id = "ws_" + "5" * 32
    (base / existing_id).mkdir()
    existing_allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=lambda: existing_id,
    )
    with pytest.raises(WorkspaceAlreadyExistsError):
        existing_allocator.allocate(runtime_id="runtime.existing.001", profile=profile)


def test_allocated_runtime_ids_are_sorted_and_registries_instance_local(
    tmp_path: Path,
) -> None:
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    base_one = tmp_path / "base-one"
    base_two = tmp_path / "base-two"
    base_one.mkdir()
    base_two.mkdir()
    allocator_one = RuntimeWorkspaceAllocator(
        trusted_base_root=base_one,
        workspace_id_factory=sequence_factory("b" * 32, "a" * 32),
    )
    allocator_two = RuntimeWorkspaceAllocator(
        trusted_base_root=base_two,
        workspace_id_factory=id_factory("b" * 32),
    )

    allocator_one.allocate(runtime_id="runtime.z", profile=profile)
    allocator_one.allocate(runtime_id="runtime.a", profile=profile)
    allocator_two.allocate(runtime_id="runtime.z", profile=profile)

    assert allocator_one.allocated_runtime_ids() == ("runtime.a", "runtime.z")
    assert allocator_two.allocated_runtime_ids() == ("runtime.z",)


def test_workspace_paths_are_contained_and_symlink_workspace_root_rejected(
    tmp_path: Path,
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    target = tmp_path / "target"
    target.mkdir()
    workspace_id = "ws_" + "6" * 32
    link = base / workspace_id
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("host does not allow directory symlink creation")

    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=lambda: workspace_id,
    )
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    with pytest.raises(PathRedirectDetectedError):
        allocator.allocate(runtime_id="runtime.symlink.001", profile=profile)


def test_managed_files_path_validation_accepts_contained_and_rejects_outside(
    tmp_path: Path,
) -> None:
    allocator = make_allocator(tmp_path, "7" * 32)
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.files.001", profile=profile)
    binding = allocation.files_root_binding
    assert binding is not None
    root = binding.locked_root
    child = root / "child"
    child.mkdir()
    future = root / "nested" / "future"
    outside = allocation.paths.workspace_root / "files-root-escape"
    outside.mkdir()

    assert validate_managed_files_path(binding, root, require_exists=True) == root
    assert (
        validate_managed_files_path(binding, child, require_exists=True)
        == child.resolve()
    )
    assert validate_managed_files_path(binding, future, require_exists=False) == future
    with pytest.raises(PathOutsideContainmentRootError):
        validate_managed_files_path(binding, outside, require_exists=True)
    with pytest.raises(PathOutsideContainmentRootError):
        validate_managed_files_path(binding, outside / "future", require_exists=False)
    with pytest.raises(WorkspaceAllocationError):
        RuntimeFilesRootBinding(
            workspace_id=binding.workspace_id,
            default_path=root,
            locked_root=child,
            can_change_path=False,
        )
    with pytest.raises(WorkspaceAllocationError):
        RuntimeFilesRootBinding(
            workspace_id=binding.workspace_id,
            default_path=root,
            locked_root=root,
            can_change_path=True,
        )


def test_allocation_compensates_directory_creation_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    unrelated = base / "unrelated.txt"
    unrelated.write_text("keep", encoding="utf-8")
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    original_create = ws._create_directory

    def fail_on_logs(path, created_paths, runtime_id, workspace_id, policy):
        if path.name == "logs":
            raise WorkspaceAllocationError(allocation_stage="directory_creation")
        original_create(path, created_paths, runtime_id, workspace_id, policy)

    monkeypatch.setattr(ws, "_create_directory", fail_on_logs)
    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory("8" * 32),
    )
    with pytest.raises(WorkspaceAllocationError):
        allocator.allocate(runtime_id="runtime.faildir.001", profile=profile)
    assert not (base / ("ws_" + "8" * 32)).exists()
    assert unrelated.read_text(encoding="utf-8") == "keep"


def test_allocation_compensates_marker_creation_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)

    def fail_marker(*_args, **_kwargs):
        raise WorkspaceMarkerError(allocation_stage="marker_creation")

    monkeypatch.setattr(ws, "_write_marker", fail_marker)
    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory("9" * 32),
    )
    with pytest.raises(WorkspaceMarkerError):
        allocator.allocate(runtime_id="runtime.failmarker.001", profile=profile)
    assert not (base / ("ws_" + "9" * 32)).exists()


def test_compensation_failure_is_explicit_and_does_not_recurse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    original_create = ws._create_directory
    workspace_root = base / ("ws_" + "a" * 32)

    def create_unexpected_file_then_fail(
        path, created_paths, runtime_id, workspace_id, policy
    ):
        original_create(path, created_paths, runtime_id, workspace_id, policy)
        if path.name == "home":
            (workspace_root / "unexpected.txt").write_text("preserve", encoding="utf-8")
            raise WorkspaceAllocationError(allocation_stage="directory_creation")

    monkeypatch.setattr(ws, "_create_directory", create_unexpected_file_then_fail)
    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory("a" * 32),
    )
    with pytest.raises(WorkspaceAllocationCompensationError):
        allocator.allocate(runtime_id="runtime.compensation.001", profile=profile)
    assert (workspace_root / "unexpected.txt").read_text(encoding="utf-8") == "preserve"


def test_environment_projection_sanitizer_and_launch_plan_compatibility(
    tmp_path: Path,
) -> None:
    allocator = make_allocator(tmp_path, "c" * 32)
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.compat.001", profile=profile)
    env_paths = allocation.environment_paths

    assert env_paths.hermes_home == str(allocation.paths.hermes_home)
    assert env_paths.home == str(allocation.paths.home)
    assert env_paths.user_profile == str(allocation.paths.user_profile)
    assert env_paths.app_data == str(allocation.paths.app_data)
    assert env_paths.local_app_data == str(allocation.paths.local_app_data)
    assert env_paths.temp == str(allocation.paths.temp)
    assert env_paths.files_root == str(allocation.paths.files_root)

    sanitized = sanitize_runtime_environment(
        profile=profile,
        platform_family=platform_family(),
        source_environment=synthetic_source(),
        paths=env_paths,
    )
    assert "OPENAI_API_KEY" not in sanitized.as_mapping()
    plan = ResolvedProcessLaunchPlan(
        profile_id=profile.profile_ref.profile_id,
        workspace_id=allocation.workspace_ref.workspace_id,
        executable=sys.executable,
        arguments=(),
        working_directory=str(allocation.paths.workdir),
        environment_items=sanitized.items,
        stdout_limit_bytes=profile.timeout_policy.max_stdout_bytes,
        stderr_limit_bytes=profile.timeout_policy.max_stderr_bytes,
    )
    assert plan.working_directory == str(allocation.paths.workdir)


def test_workspace_safety_boundaries_and_root_exports(tmp_path: Path) -> None:
    allocator = make_allocator(tmp_path, "d" * 32)
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.safe.001", profile=profile)

    for representation in (repr(allocator), repr(allocation), repr(allocation.paths)):
        assert str(tmp_path) not in representation
    assert allocation.files_root_binding is not None
    assert str(tmp_path) not in repr(allocation.files_root_binding)
    for forbidden_method in (
        "delete",
        "cleanup",
        "rollback",
        "release_and_remove",
        "purge",
        "clean_all",
    ):
        assert not hasattr(allocator, forbidden_method)
    assert not hasattr(ra, "RuntimeWorkspaceAllocator")
    assert not hasattr(ra, "RuntimeFilesRootBinding")
    assert "RuntimeWorkspaceAllocator" not in ra.__all__
    assert "RuntimeFilesRootBinding" not in ra.__all__


def test_workspace_source_guard_blocks_unauthorized_runtime_behavior() -> None:
    forbidden_text = {
        "subprocess",
        "os.system",
        "os.popen",
        "shell=true",
        "requests",
        "httpx",
        "urllib.request",
        "socket",
        "path.home",
        "expanduser",
        "os.environ",
        "os.getenv",
        "getpass",
        "shutil.rmtree",
        "git clean",
        "taskkill",
        "provider_api_key",
        "provider_credentials",
        "worker launch",
        "agent launch",
        "mcp execution",
    }
    for source_path in SOURCE_PATHS:
        text = source_path.read_text(encoding="utf-8")
        lowered = text.lower()
        for forbidden in forbidden_text:
            assert forbidden not in lowered, (source_path, forbidden)
        assert "caller_workspace_path" not in lowered
        assert "public_workspace_path" not in lowered


def test_generated_paths_are_beneath_workspace_and_base(tmp_path: Path) -> None:
    base = tmp_path / "base"
    base.mkdir()
    allocator = RuntimeWorkspaceAllocator(
        trusted_base_root=base,
        workspace_id_factory=id_factory("e" * 32),
    )
    profile = get_runtime_profile(ra.PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID)
    allocation = allocator.allocate(runtime_id="runtime.contained.001", profile=profile)

    assert_existing_path_contained(
        allocation.paths.workspace_root, containment_root=base
    )
    for path in (
        allocation.paths.home,
        allocation.paths.user_profile,
        allocation.paths.hermes_home,
        allocation.paths.app_data,
        allocation.paths.local_app_data,
        allocation.paths.temp,
        allocation.paths.logs,
        allocation.paths.state,
        allocation.paths.evidence,
        allocation.paths.workdir,
        allocation.paths.files_root,
        allocation.paths.ownership_marker,
    ):
        assert path is not None
        assert_existing_path_contained(
            path, containment_root=allocation.paths.workspace_root
        )
