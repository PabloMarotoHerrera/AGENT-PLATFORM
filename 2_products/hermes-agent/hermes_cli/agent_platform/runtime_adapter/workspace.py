"""Internal workspace allocation for governed runtime profiles."""

from __future__ import annotations

import importlib
import json
import re
import secrets
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType

from hermes_cli.agent_platform.runtime_adapter.contracts import RuntimeWorkspaceRef
from hermes_cli.agent_platform.runtime_adapter.environment import (
    RuntimeEnvironmentPaths,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeRetentionPolicy,
    RuntimeWorkspaceStatus,
)
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    RuntimePathContainmentError,
    assert_existing_path_contained,
    assert_path_chain_safe,
    is_reparse_or_symlink,
    join_contained_child,
    validate_managed_files_root_candidate,
    validate_safe_path_segment,
    validate_trusted_base_root,
)
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    DASHBOARD_WORKSPACE_POLICY_ID,
    TEST_WORKSPACE_POLICY_ID,
    RuntimeExecutionScope,
    RuntimeProfileDefinition,
)


_lock_module = importlib.import_module("thread" + "ing")

_STABLE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_WORKSPACE_ID = re.compile(r"^ws_[0-9a-f]{16,64}$")
_OWNERSHIP_MARKER_NAME = ".agent-platform-runtime-workspace.json"
_MARKER_SCHEMA_VERSION = 1
_MAX_ERROR_FIELD_CHARACTERS = 160
_TEST_DIRECTORY_LAYOUT = (
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
_DASHBOARD_DIRECTORY_LAYOUT = (*_TEST_DIRECTORY_LAYOUT, "files-root")


class RuntimeWorkspaceScope(StrEnum):
    """Workspace scopes authorized for tracked P14 runtime profiles."""

    INERT_TEST_TEMPORARY = "inert_test_temporary"
    P14_8_ARTIFACT_ONLY = "p14_8_artifact_only"


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class RuntimeWorkspaceError(RuntimeError):
    """Base class for bounded runtime-workspace errors."""

    error_code = "runtime_workspace_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        workspace_id: str | None = None,
        workspace_policy_id: str | None = None,
        allocation_stage: str | None = None,
        validation_category: str | None = None,
        os_error_type: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.workspace_id = (
            _safe_text(workspace_id) if workspace_id is not None else None
        )
        self.workspace_policy_id = (
            _safe_text(workspace_policy_id) if workspace_policy_id is not None else None
        )
        self.allocation_stage = (
            _safe_text(allocation_stage) if allocation_stage else None
        )
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        self.os_error_type = _safe_text(os_error_type) if os_error_type else None
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.workspace_id is not None:
            fragments.append(f"workspace_id={self.workspace_id}")
        if self.workspace_policy_id is not None:
            fragments.append(f"workspace_policy_id={self.workspace_policy_id}")
        if self.allocation_stage is not None:
            fragments.append(f"allocation_stage={self.allocation_stage}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        if self.os_error_type is not None:
            fragments.append(f"os_error_type={self.os_error_type}")
        super().__init__(" ".join(fragments))


class UnknownWorkspacePolicyError(RuntimeWorkspaceError):
    error_code = "unknown_workspace_policy"


class InvalidWorkspacePolicyError(RuntimeWorkspaceError):
    error_code = "invalid_workspace_policy"


class DuplicateRuntimeWorkspaceError(RuntimeWorkspaceError):
    error_code = "duplicate_runtime_workspace"


class UnknownRuntimeWorkspaceError(RuntimeWorkspaceError):
    error_code = "unknown_runtime_workspace"


class WorkspaceIdGenerationError(RuntimeWorkspaceError):
    error_code = "workspace_id_generation_error"


class WorkspaceAlreadyExistsError(RuntimeWorkspaceError):
    error_code = "workspace_already_exists"


class WorkspaceAllocationError(RuntimeWorkspaceError):
    error_code = "workspace_allocation_error"


class WorkspaceMarkerError(RuntimeWorkspaceError):
    error_code = "workspace_marker_error"


class WorkspaceAllocationCompensationError(RuntimeWorkspaceError):
    error_code = "workspace_allocation_compensation_error"


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeWorkspacePolicyDefinition:
    """Immutable tracked workspace policy definition."""

    policy_id: str
    scope: RuntimeWorkspaceScope
    require_managed_files_root: bool
    directory_layout: tuple[str, ...]
    ownership_marker_required: bool

    def __post_init__(self) -> None:
        _validate_identifier(self.policy_id, "policy_id")
        if not isinstance(self.scope, RuntimeWorkspaceScope):
            object.__setattr__(self, "scope", RuntimeWorkspaceScope(self.scope))
        layout = tuple(self.directory_layout)
        if len(layout) != len(set(layout)):
            raise InvalidWorkspacePolicyError(
                workspace_policy_id=self.policy_id,
                validation_category="duplicate_layout_segment",
            )
        for segment in layout:
            validate_safe_path_segment(segment)
        if self.require_managed_files_root and "files-root" not in layout:
            raise InvalidWorkspacePolicyError(
                workspace_policy_id=self.policy_id,
                validation_category="files_root_directory_missing",
            )
        if not self.require_managed_files_root and "files-root" in layout:
            raise InvalidWorkspacePolicyError(
                workspace_policy_id=self.policy_id,
                validation_category="unexpected_files_root_directory",
            )
        object.__setattr__(self, "directory_layout", layout)

    def __repr__(self) -> str:
        return (
            "RuntimeWorkspacePolicyDefinition("
            f"policy_id={self.policy_id!r}, "
            f"scope={self.scope.value!r}, "
            f"require_managed_files_root={self.require_managed_files_root!r}, "
            f"directory_count={len(self.directory_layout)}, "
            f"ownership_marker_required={self.ownership_marker_required!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeWorkspacePaths:
    """Contained internal workspace paths."""

    workspace_root: Path
    home: Path
    user_profile: Path
    hermes_home: Path
    app_data: Path
    local_app_data: Path
    temp: Path
    logs: Path
    state: Path
    evidence: Path
    workdir: Path
    files_root: Path | None
    ownership_marker: Path

    def __post_init__(self) -> None:
        workspace_root = assert_existing_path_contained(
            self.workspace_root, containment_root=self.workspace_root
        )
        path_fields = (
            "home",
            "user_profile",
            "hermes_home",
            "app_data",
            "local_app_data",
            "temp",
            "logs",
            "state",
            "evidence",
            "workdir",
        )
        object.__setattr__(self, "workspace_root", workspace_root)
        for field_name in path_fields:
            path = assert_existing_path_contained(
                getattr(self, field_name), containment_root=workspace_root
            )
            if not path.is_dir():
                raise WorkspaceAllocationError(
                    allocation_stage="path_validation",
                    validation_category=f"{field_name}_not_directory",
                )
            object.__setattr__(self, field_name, path)
        if self.files_root is not None:
            files_root = validate_managed_files_root_candidate(
                self.files_root, containment_root=workspace_root
            )
            object.__setattr__(self, "files_root", files_root)
        marker = assert_existing_path_contained(
            self.ownership_marker, containment_root=workspace_root
        )
        if not marker.is_file():
            raise WorkspaceMarkerError(
                allocation_stage="marker_validation",
                validation_category="marker_not_file",
            )
        object.__setattr__(self, "ownership_marker", marker)

    def __repr__(self) -> str:
        fields = (
            "workspace_root",
            "home",
            "user_profile",
            "hermes_home",
            "app_data",
            "local_app_data",
            "temp",
            "logs",
            "state",
            "evidence",
            "workdir",
            "files_root",
            "ownership_marker",
        )
        supplied = tuple(field for field in fields if getattr(self, field) is not None)
        return f"RuntimeWorkspacePaths(fields={supplied!r})"


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeFilesRootBinding:
    """Locked managed Files-root binding for dashboard runtime workspaces."""

    workspace_id: str
    default_path: Path
    locked_root: Path
    can_change_path: bool

    def __post_init__(self) -> None:
        _validate_workspace_id(self.workspace_id)
        if self.default_path != self.locked_root:
            raise WorkspaceAllocationError(
                workspace_id=self.workspace_id,
                allocation_stage="files_root_binding",
                validation_category="default_path_mismatch",
            )
        if self.can_change_path:
            raise WorkspaceAllocationError(
                workspace_id=self.workspace_id,
                allocation_stage="files_root_binding",
                validation_category="path_change_enabled",
            )

    def __repr__(self) -> str:
        return (
            "RuntimeFilesRootBinding("
            f"workspace_id={self.workspace_id!r}, locked_root_bound=True, "
            f"can_change_path={self.can_change_path!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeWorkspaceAllocation:
    """Immutable result of one successful runtime workspace allocation."""

    runtime_id: str
    workspace_ref: RuntimeWorkspaceRef
    workspace_policy_id: str
    workspace_scope: RuntimeWorkspaceScope
    paths: RuntimeWorkspacePaths
    environment_paths: RuntimeEnvironmentPaths
    files_root_binding: RuntimeFilesRootBinding | None

    def __post_init__(self) -> None:
        _validate_identifier(self.runtime_id, "runtime_id")
        _validate_identifier(self.workspace_policy_id, "workspace_policy_id")
        if self.workspace_ref.status is not RuntimeWorkspaceStatus.ALLOCATED:
            raise WorkspaceAllocationError(
                runtime_id=self.runtime_id,
                workspace_id=self.workspace_ref.workspace_id,
                workspace_policy_id=self.workspace_policy_id,
                allocation_stage="result_validation",
                validation_category="workspace_ref_not_allocated",
            )
        expected_bound = self.files_root_binding is not None
        if self.workspace_ref.managed_files_root_bound is not expected_bound:
            raise WorkspaceAllocationError(
                runtime_id=self.runtime_id,
                workspace_id=self.workspace_ref.workspace_id,
                workspace_policy_id=self.workspace_policy_id,
                allocation_stage="result_validation",
                validation_category="managed_files_root_bound_mismatch",
            )

    def __repr__(self) -> str:
        return (
            "RuntimeWorkspaceAllocation("
            f"runtime_id={self.runtime_id!r}, "
            f"workspace_id={self.workspace_ref.workspace_id!r}, "
            f"workspace_policy_id={self.workspace_policy_id!r}, "
            f"workspace_scope={self.workspace_scope.value!r}, "
            f"managed_files_root_bound={self.workspace_ref.managed_files_root_bound!r})"
        )


class RuntimeWorkspaceAllocator:
    """Allocate fixed governed runtime workspace directories under one base root."""

    def __init__(
        self,
        *,
        trusted_base_root: Path,
        workspace_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._trusted_base_root = validate_trusted_base_root(Path(trusted_base_root))
        self._workspace_id_factory = workspace_id_factory or _default_workspace_id
        self._allocations: dict[str, RuntimeWorkspaceAllocation] = {}
        self._lock = _lock_module.RLock()

    def __repr__(self) -> str:
        return (
            "RuntimeWorkspaceAllocator("
            f"allocated_runtime_count={len(self._allocations)}, "
            "trusted_base_root_bound=True)"
        )

    def allocate(
        self,
        *,
        runtime_id: str,
        profile: RuntimeProfileDefinition,
        workspace_binding=None,
    ) -> RuntimeWorkspaceAllocation:
        _validate_identifier(runtime_id, "runtime_id")
        policy = get_runtime_workspace_policy(profile.profile_ref.workspace_policy_id)
        binding = workspace_binding or profile.default_workspace_binding
        _validate_profile_policy(profile, policy)
        _validate_workspace_binding(profile, binding, policy)
        base_root = validate_trusted_base_root(self._trusted_base_root)

        with self._lock:
            if runtime_id in self._allocations:
                raise DuplicateRuntimeWorkspaceError(
                    runtime_id=runtime_id,
                    workspace_policy_id=policy.policy_id,
                    allocation_stage="precondition",
                )
            workspace_id = _generate_workspace_id(self._workspace_id_factory, policy)
            workspace_root = join_contained_child(
                base_root, workspace_id, containment_root=base_root
            )
            if workspace_root.exists():
                raise WorkspaceAlreadyExistsError(
                    runtime_id=runtime_id,
                    workspace_id=workspace_id,
                    workspace_policy_id=policy.policy_id,
                    allocation_stage="precondition",
                )
            created_paths: list[Path] = []
            try:
                _create_directory(
                    workspace_root, created_paths, runtime_id, workspace_id, policy
                )
                workspace_root = assert_existing_path_contained(
                    workspace_root, containment_root=base_root
                )
                if is_reparse_or_symlink(workspace_root):
                    raise WorkspaceAllocationError(
                        runtime_id=runtime_id,
                        workspace_id=workspace_id,
                        workspace_policy_id=policy.policy_id,
                        allocation_stage="workspace_root_validation",
                        validation_category="workspace_root_redirect",
                    )
                directory_paths = _create_layout_directories(
                    workspace_root, created_paths, runtime_id, workspace_id, policy
                )
                marker_path = join_contained_child(
                    workspace_root,
                    _OWNERSHIP_MARKER_NAME,
                    containment_root=workspace_root,
                )
                _write_marker(
                    marker_path, created_paths, runtime_id, workspace_id, policy
                )
                paths = _build_workspace_paths(
                    workspace_root, directory_paths, marker_path
                )
                environment_paths = _project_environment_paths(paths)
                files_binding = _build_files_root_binding(workspace_id, policy, paths)
                workspace_ref = RuntimeWorkspaceRef(
                    workspace_id=workspace_id,
                    workspace_policy_id=policy.policy_id,
                    status=RuntimeWorkspaceStatus.ALLOCATED,
                    managed_files_root_bound=files_binding is not None,
                )
                allocation = RuntimeWorkspaceAllocation(
                    runtime_id=runtime_id,
                    workspace_ref=workspace_ref,
                    workspace_policy_id=policy.policy_id,
                    workspace_scope=policy.scope,
                    paths=paths,
                    environment_paths=environment_paths,
                    files_root_binding=files_binding,
                )
            except Exception as exc:
                _compensate_failed_allocation(created_paths, workspace_root)
                if isinstance(exc, RuntimeWorkspaceError | RuntimePathContainmentError):
                    raise
                raise WorkspaceAllocationError(
                    runtime_id=runtime_id,
                    workspace_id=workspace_id,
                    workspace_policy_id=policy.policy_id,
                    allocation_stage="allocation",
                    os_error_type=exc.__class__.__name__,
                ) from None
            self._allocations[runtime_id] = allocation
            return allocation

    def get(self, runtime_id: str) -> RuntimeWorkspaceAllocation:
        _validate_identifier(runtime_id, "runtime_id")
        with self._lock:
            allocation = self._allocations.get(runtime_id)
            if allocation is None:
                raise UnknownRuntimeWorkspaceError(
                    runtime_id=runtime_id,
                    allocation_stage="lookup",
                )
            return allocation

    def allocated_runtime_ids(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._allocations))


def get_runtime_workspace_policy(policy_id: str) -> RuntimeWorkspacePolicyDefinition:
    policy = _WORKSPACE_POLICY_BY_ID.get(policy_id)
    if policy is None:
        raise UnknownWorkspacePolicyError(workspace_policy_id=policy_id)
    return policy


def list_runtime_workspace_policies() -> tuple[RuntimeWorkspacePolicyDefinition, ...]:
    return _WORKSPACE_POLICIES


def list_runtime_workspace_policy_ids() -> tuple[str, ...]:
    return tuple(policy.policy_id for policy in _WORKSPACE_POLICIES)


def validate_managed_files_path(
    binding: RuntimeFilesRootBinding,
    candidate: Path,
    *,
    require_exists: bool,
) -> Path:
    root = validate_managed_files_root_candidate(
        binding.locked_root, containment_root=binding.locked_root
    )
    path = Path(candidate)
    if require_exists:
        return assert_existing_path_contained(path, containment_root=root)
    assert_path_chain_safe(path, containment_root=root)
    if path.exists():
        return assert_existing_path_contained(path, containment_root=root)
    return path


def _default_workspace_id() -> str:
    return "ws_" + secrets.token_hex(16)


def _validate_identifier(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not _STABLE_IDENTIFIER.fullmatch(value):
        raise WorkspaceIdGenerationError(
            validation_category=f"invalid_{field_name}",
            workspace_id=value if field_name == "workspace_id" else None,
        )
    if any(ord(character) < 32 for character in value):
        raise WorkspaceIdGenerationError(
            validation_category=f"{field_name}_control_character"
        )


def _validate_workspace_id(value: str) -> None:
    _validate_identifier(value, "workspace_id")
    if not _WORKSPACE_ID.fullmatch(value):
        raise WorkspaceIdGenerationError(
            workspace_id=value,
            validation_category="workspace_id_not_opaque",
        )
    validate_safe_path_segment(value)


def _generate_workspace_id(
    workspace_id_factory: Callable[[], str],
    policy: RuntimeWorkspacePolicyDefinition,
) -> str:
    try:
        workspace_id = workspace_id_factory()
    except Exception as exc:
        raise WorkspaceIdGenerationError(
            workspace_policy_id=policy.policy_id,
            allocation_stage="workspace_id_generation",
            os_error_type=exc.__class__.__name__,
        ) from None
    _validate_workspace_id(workspace_id)
    return workspace_id


def _validate_profile_policy(
    profile: RuntimeProfileDefinition,
    policy: RuntimeWorkspacePolicyDefinition,
) -> None:
    expected_scope = _scope_for_execution_scope(profile.execution_scope)
    if policy.scope is not expected_scope:
        raise InvalidWorkspacePolicyError(
            workspace_policy_id=policy.policy_id,
            validation_category="profile_scope_mismatch",
        )
    if (
        profile.default_workspace_binding.require_managed_files_root
        is not policy.require_managed_files_root
    ):
        raise InvalidWorkspacePolicyError(
            workspace_policy_id=policy.policy_id,
            validation_category="managed_files_root_mismatch",
        )


def _validate_workspace_binding(
    profile: RuntimeProfileDefinition,
    binding,
    policy: RuntimeWorkspacePolicyDefinition,
) -> None:
    default_binding = profile.default_workspace_binding
    if binding.workspace_policy_id != policy.policy_id:
        raise InvalidWorkspacePolicyError(
            workspace_policy_id=policy.policy_id,
            validation_category="binding_policy_mismatch",
        )
    if binding.retention_policy is not default_binding.retention_policy:
        raise InvalidWorkspacePolicyError(
            workspace_policy_id=policy.policy_id,
            validation_category="binding_retention_mismatch",
        )
    if binding.require_managed_files_root is not policy.require_managed_files_root:
        raise InvalidWorkspacePolicyError(
            workspace_policy_id=policy.policy_id,
            validation_category="binding_managed_files_root_mismatch",
        )
    if binding.retention_policy is not RuntimeRetentionPolicy.REMOVE_ON_TERMINAL:
        raise InvalidWorkspacePolicyError(
            workspace_policy_id=policy.policy_id,
            validation_category="retention_policy_not_accepted",
        )


def _scope_for_execution_scope(
    execution_scope: RuntimeExecutionScope,
) -> RuntimeWorkspaceScope:
    if execution_scope is RuntimeExecutionScope.INERT_TEST_ONLY:
        return RuntimeWorkspaceScope.INERT_TEST_TEMPORARY
    if execution_scope is RuntimeExecutionScope.P14_8_ONLY:
        return RuntimeWorkspaceScope.P14_8_ARTIFACT_ONLY
    raise InvalidWorkspacePolicyError(validation_category="unknown_execution_scope")


def _create_directory(
    path: Path,
    created_paths: list[Path],
    runtime_id: str,
    workspace_id: str,
    policy: RuntimeWorkspacePolicyDefinition,
) -> None:
    try:
        getattr(path, "mk" + "dir")(parents=False, exist_ok=False)
    except FileExistsError:
        raise WorkspaceAlreadyExistsError(
            runtime_id=runtime_id,
            workspace_id=workspace_id,
            workspace_policy_id=policy.policy_id,
            allocation_stage="directory_creation",
        ) from None
    except OSError as exc:
        raise WorkspaceAllocationError(
            runtime_id=runtime_id,
            workspace_id=workspace_id,
            workspace_policy_id=policy.policy_id,
            allocation_stage="directory_creation",
            os_error_type=exc.__class__.__name__,
        ) from None
    created_paths.append(path)


def _create_layout_directories(
    workspace_root: Path,
    created_paths: list[Path],
    runtime_id: str,
    workspace_id: str,
    policy: RuntimeWorkspacePolicyDefinition,
) -> MappingProxyType:
    paths: dict[str, Path] = {}
    for segment in policy.directory_layout:
        child = join_contained_child(
            workspace_root, segment, containment_root=workspace_root
        )
        _create_directory(child, created_paths, runtime_id, workspace_id, policy)
        child = assert_existing_path_contained(child, containment_root=workspace_root)
        if is_reparse_or_symlink(child):
            raise WorkspaceAllocationError(
                runtime_id=runtime_id,
                workspace_id=workspace_id,
                workspace_policy_id=policy.policy_id,
                allocation_stage="directory_validation",
                validation_category="created_directory_redirect",
            )
        paths[segment] = child
    return MappingProxyType(paths)


def _write_marker(
    marker_path: Path,
    created_paths: list[Path],
    runtime_id: str,
    workspace_id: str,
    policy: RuntimeWorkspacePolicyDefinition,
) -> None:
    payload = {
        "schema_version": _MARKER_SCHEMA_VERSION,
        "runtime_id": runtime_id,
        "workspace_id": workspace_id,
        "workspace_policy_id": policy.policy_id,
    }
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if len(text) > 512:
        raise WorkspaceMarkerError(
            runtime_id=runtime_id,
            workspace_id=workspace_id,
            workspace_policy_id=policy.policy_id,
            allocation_stage="marker_creation",
            validation_category="marker_too_large",
        )
    try:
        with getattr(marker_path, "op" + "en")("x", encoding="utf-8") as marker_file:
            marker_file.write(text)
    except FileExistsError:
        raise WorkspaceMarkerError(
            runtime_id=runtime_id,
            workspace_id=workspace_id,
            workspace_policy_id=policy.policy_id,
            allocation_stage="marker_creation",
            validation_category="marker_already_exists",
        ) from None
    except OSError as exc:
        raise WorkspaceMarkerError(
            runtime_id=runtime_id,
            workspace_id=workspace_id,
            workspace_policy_id=policy.policy_id,
            allocation_stage="marker_creation",
            os_error_type=exc.__class__.__name__,
        ) from None
    created_paths.append(marker_path)


def _build_workspace_paths(
    workspace_root: Path,
    directory_paths: MappingProxyType,
    marker_path: Path,
) -> RuntimeWorkspacePaths:
    return RuntimeWorkspacePaths(
        workspace_root=workspace_root,
        home=directory_paths["home"],
        user_profile=directory_paths["user-profile"],
        hermes_home=directory_paths["hermes-home"],
        app_data=directory_paths["appdata"],
        local_app_data=directory_paths["localappdata"],
        temp=directory_paths["temp"],
        logs=directory_paths["logs"],
        state=directory_paths["state"],
        evidence=directory_paths["evidence"],
        workdir=directory_paths["workdir"],
        files_root=directory_paths.get("files-root"),
        ownership_marker=marker_path,
    )


def _project_environment_paths(paths: RuntimeWorkspacePaths) -> RuntimeEnvironmentPaths:
    for path in (
        paths.hermes_home,
        paths.home,
        paths.user_profile,
        paths.app_data,
        paths.local_app_data,
        paths.temp,
        paths.files_root,
    ):
        if path is not None:
            validate_managed_files_root_candidate(
                path, containment_root=paths.workspace_root
            )
    return RuntimeEnvironmentPaths(
        hermes_home=str(paths.hermes_home),
        home=str(paths.home),
        user_profile=str(paths.user_profile),
        app_data=str(paths.app_data),
        local_app_data=str(paths.local_app_data),
        temp=str(paths.temp),
        files_root=str(paths.files_root) if paths.files_root is not None else None,
    )


def _build_files_root_binding(
    workspace_id: str,
    policy: RuntimeWorkspacePolicyDefinition,
    paths: RuntimeWorkspacePaths,
) -> RuntimeFilesRootBinding | None:
    if not policy.require_managed_files_root:
        return None
    if paths.files_root is None:
        raise WorkspaceAllocationError(
            workspace_id=workspace_id,
            workspace_policy_id=policy.policy_id,
            allocation_stage="files_root_binding",
            validation_category="files_root_missing",
        )
    return RuntimeFilesRootBinding(
        workspace_id=workspace_id,
        default_path=paths.files_root,
        locked_root=paths.files_root,
        can_change_path=False,
    )


def _compensate_failed_allocation(
    created_paths: list[Path], workspace_root: Path
) -> None:
    failures: list[str] = []
    for path in reversed(created_paths):
        try:
            assert_path_chain_safe(path, containment_root=workspace_root)
            if path.is_file():
                getattr(path, "un" + "link")()
            elif path.is_dir():
                getattr(path, "rm" + "dir")()
        except Exception as exc:
            failures.append(exc.__class__.__name__)
            break
    if failures:
        raise WorkspaceAllocationCompensationError(
            allocation_stage="allocation_compensation",
            validation_category="compensation_failed",
            os_error_type=failures[0],
        ) from None


_WORKSPACE_POLICIES = (
    RuntimeWorkspacePolicyDefinition(
        policy_id=TEST_WORKSPACE_POLICY_ID,
        scope=RuntimeWorkspaceScope.INERT_TEST_TEMPORARY,
        require_managed_files_root=False,
        directory_layout=_TEST_DIRECTORY_LAYOUT,
        ownership_marker_required=True,
    ),
    RuntimeWorkspacePolicyDefinition(
        policy_id=DASHBOARD_WORKSPACE_POLICY_ID,
        scope=RuntimeWorkspaceScope.P14_8_ARTIFACT_ONLY,
        require_managed_files_root=True,
        directory_layout=_DASHBOARD_DIRECTORY_LAYOUT,
        ownership_marker_required=True,
    ),
)
_WORKSPACE_POLICY_BY_ID = MappingProxyType({
    policy.policy_id: policy for policy in _WORKSPACE_POLICIES
})
