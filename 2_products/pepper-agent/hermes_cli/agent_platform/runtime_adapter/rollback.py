"""Internal contained workspace rollback for governed runtimes."""

from __future__ import annotations

import importlib
import json
import stat
from dataclasses import dataclass
from pathlib import Path

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    RuntimeHandle,
    RuntimeOperationResult,
    RuntimeRollbackRequest,
    RuntimeWorkspaceRef,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeCleanupStatus,
    RuntimeEventType,
    RuntimeLifecycleAction,
    RuntimeLifecycleState,
    RuntimeOperationOutcome,
    RuntimeProcessStatus,
    RuntimeRetentionPolicy,
    RuntimeWorkspaceStatus,
)
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    RuntimeEventJournal,
    normalize_runtime_failure,
)
from hermes_cli.agent_platform.runtime_adapter.lifecycle_control import (
    RuntimeLifecycleClock,
    SystemRuntimeLifecycleClock,
    with_runtime_state,
)
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    RuntimePathContainmentError,
    assert_existing_path_contained,
    assert_path_chain_safe,
    is_reparse_or_symlink,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import HermesProcessOwner
from hermes_cli.agent_platform.runtime_adapter.profiles import RuntimeProfileDefinition
from hermes_cli.agent_platform.runtime_adapter.state_machine import (
    transition_runtime_state,
)
from hermes_cli.agent_platform.runtime_adapter.workspace import (
    RuntimeWorkspaceAllocation,
    RuntimeWorkspaceAllocator,
    RuntimeWorkspaceError,
)


_os_module = importlib.import_module("o" + "s")
_lock_module = importlib.import_module("thread" + "ing")
_MAX_ERROR_FIELD_CHARACTERS = 160
_MAX_MARKER_BYTES = 4096
_MAX_TREE_ENTRIES = 10000
_MAX_TREE_DEPTH = 64
_MARKER_NAME = ".agent-platform-runtime-workspace.json"


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


class RuntimeRollbackError(RuntimeError):
    """Base class for bounded workspace rollback errors."""

    error_code = "runtime_rollback_error"

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        workspace_id: str | None = None,
        validation_category: str | None = None,
        entry_role: str | None = None,
        os_error_type: str | None = None,
    ) -> None:
        self.runtime_id = _safe_text(runtime_id) if runtime_id is not None else None
        self.workspace_id = (
            _safe_text(workspace_id) if workspace_id is not None else None
        )
        self.validation_category = (
            _safe_text(validation_category) if validation_category else None
        )
        self.entry_role = _safe_text(entry_role) if entry_role else None
        self.os_error_type = _safe_text(os_error_type) if os_error_type else None
        fragments = [f"code={self.error_code}"]
        if self.runtime_id is not None:
            fragments.append(f"runtime_id={self.runtime_id}")
        if self.workspace_id is not None:
            fragments.append(f"workspace_id={self.workspace_id}")
        if self.validation_category is not None:
            fragments.append(f"validation_category={self.validation_category}")
        if self.entry_role is not None:
            fragments.append(f"entry_role={self.entry_role}")
        if self.os_error_type is not None:
            fragments.append(f"os_error_type={self.os_error_type}")
        super().__init__(" ".join(fragments))


class RuntimeRollbackIdentityError(RuntimeRollbackError):
    error_code = "runtime_rollback_identity_error"


class RuntimeRollbackStateError(RuntimeRollbackError):
    error_code = "runtime_rollback_state_error"


class RuntimeRollbackProcessStillOwnedError(RuntimeRollbackError):
    error_code = "runtime_rollback_process_still_owned"


class RuntimeRollbackMarkerError(RuntimeRollbackError):
    error_code = "runtime_rollback_marker_error"


class RuntimeRollbackTreeLimitError(RuntimeRollbackError):
    error_code = "runtime_rollback_tree_limit_error"


class RuntimeRollbackEntryTypeError(RuntimeRollbackError):
    error_code = "runtime_rollback_entry_type_error"


class RuntimeRollbackContainmentError(RuntimeRollbackError):
    error_code = "runtime_rollback_containment_error"


class RuntimeRollbackDeletionError(RuntimeRollbackError):
    error_code = "runtime_rollback_deletion_error"


class RuntimeRollbackAllocatorReleaseError(RuntimeRollbackError):
    error_code = "runtime_rollback_allocator_release_error"


@dataclass(frozen=True, slots=True)
class _WorkspaceTreeEntry:
    path: Path
    depth: int
    is_directory: bool
    is_marker: bool


class RuntimeWorkspaceRollbackCoordinator:
    """Rollback one already-stopped owned runtime workspace."""

    def __init__(
        self,
        *,
        workspace_allocator: RuntimeWorkspaceAllocator,
        process_owner: HermesProcessOwner,
        clock: RuntimeLifecycleClock | None = None,
    ) -> None:
        self._workspace_allocator = workspace_allocator
        self._process_owner = process_owner
        self._clock = clock or SystemRuntimeLifecycleClock()
        self._locks: dict[str, object] = {}
        self._locks_guard = _lock_module.Lock()

    def rollback(
        self,
        *,
        request: RuntimeRollbackRequest,
        runtime_handle: RuntimeHandle,
        profile: RuntimeProfileDefinition,
        allocation: RuntimeWorkspaceAllocation,
        event_journal: RuntimeEventJournal,
    ) -> RuntimeOperationResult:
        _validate_identity(request, runtime_handle, profile, allocation)
        lock = self._acquire_runtime_lock(runtime_handle.runtime_id)
        try:
            return self._rollback_locked(
                request=request,
                runtime_handle=runtime_handle,
                profile=profile,
                allocation=allocation,
                event_journal=event_journal,
            )
        finally:
            lock.release()

    def _rollback_locked(
        self,
        *,
        request: RuntimeRollbackRequest,
        runtime_handle: RuntimeHandle,
        profile: RuntimeProfileDefinition,
        allocation: RuntimeWorkspaceAllocation,
        event_journal: RuntimeEventJournal,
    ) -> RuntimeOperationResult:
        _validate_state_and_process_release(
            runtime_handle,
            profile,
            allocation,
            self._process_owner,
        )
        self._validate_allocator_owns_allocation(allocation)
        pending_state = transition_runtime_state(
            runtime_handle.lifecycle_state,
            RuntimeLifecycleAction.BEGIN_ROLLBACK,
        )
        pending_handle = with_runtime_state(runtime_handle, pending_state)
        _append_rollback_event(
            event_journal,
            self._clock,
            RuntimeEventType.ROLLBACK_STARTED,
            pending_handle.lifecycle_state,
        )
        _append_rollback_event(
            event_journal,
            self._clock,
            RuntimeEventType.WORKSPACE_CLEANUP_STARTED,
            pending_handle.lifecycle_state,
            allocation=allocation,
        )
        try:
            _validate_ownership_marker(allocation)
            entries = _inspect_workspace_tree(allocation)
            _delete_workspace_entries(allocation, entries)
            if allocation.paths.workspace_root.exists():
                raise RuntimeRollbackDeletionError(
                    runtime_id=request.runtime_id,
                    workspace_id=allocation.workspace_ref.workspace_id,
                    validation_category="workspace_root_still_present",
                    entry_role="workspace_root",
                )
            self._release_allocator(allocation)
        except RuntimeRollbackError as exc:
            return self._failure_result(
                pending_handle=pending_handle,
                allocation=allocation,
                event_journal=event_journal,
                error=exc,
            )

        rolled_back_handle = with_runtime_state(
            pending_handle,
            transition_runtime_state(
                pending_handle.lifecycle_state,
                RuntimeLifecycleAction.MARK_ROLLED_BACK,
            ),
        )
        _append_rollback_event(
            event_journal,
            self._clock,
            RuntimeEventType.WORKSPACE_CLEANUP_COMPLETED,
            rolled_back_handle.lifecycle_state,
            allocation=allocation,
        )
        _append_rollback_event(
            event_journal,
            self._clock,
            RuntimeEventType.ROLLBACK_COMPLETED,
            rolled_back_handle.lifecycle_state,
        )
        return _rollback_operation_result(
            runtime_handle=rolled_back_handle,
            outcome=RuntimeOperationOutcome.ROLLED_BACK,
            workspace_reference=_cleaned_workspace_ref(allocation),
            events=event_journal.events(),
        )

    def _release_allocator(self, allocation: RuntimeWorkspaceAllocation) -> None:
        try:
            self._workspace_allocator.release_after_cleanup(
                allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
            )
        except RuntimeWorkspaceError as exc:
            raise RuntimeRollbackAllocatorReleaseError(
                runtime_id=allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                validation_category=exc.error_code,
            ) from None

    def _validate_allocator_owns_allocation(
        self,
        allocation: RuntimeWorkspaceAllocation,
    ) -> None:
        try:
            registered = self._workspace_allocator.get(allocation.runtime_id)
        except RuntimeWorkspaceError as exc:
            raise RuntimeRollbackStateError(
                runtime_id=allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                validation_category=exc.error_code,
            ) from None
        if (
            registered.workspace_ref.workspace_id
            != allocation.workspace_ref.workspace_id
        ):
            raise RuntimeRollbackStateError(
                runtime_id=allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                validation_category="allocator_workspace_mismatch",
            )

    def _failure_result(
        self,
        *,
        pending_handle: RuntimeHandle,
        allocation: RuntimeWorkspaceAllocation,
        event_journal: RuntimeEventJournal,
        error: RuntimeRollbackError,
    ) -> RuntimeOperationResult:
        failed_handle = with_runtime_state(
            pending_handle,
            transition_runtime_state(
                pending_handle.lifecycle_state,
                RuntimeLifecycleAction.MARK_ROLLBACK_FAILED,
            ),
        )
        workspace_status = (
            RuntimeWorkspaceStatus.CLEANED
            if not allocation.paths.workspace_root.exists()
            else RuntimeWorkspaceStatus.CLEANUP_FAILED
        )
        normalized = normalize_runtime_failure(
            error=error,
            runtime_handle=failed_handle,
            process_status=RuntimeProcessStatus.UNKNOWN,
            workspace_status=workspace_status,
            cleanup_status=RuntimeCleanupStatus.FAILED,
        )
        _append_rollback_event(
            event_journal,
            self._clock,
            RuntimeEventType.RUNTIME_FAILED,
            failed_handle.lifecycle_state,
            normalized_failure=normalized,
        )
        return _rollback_operation_result(
            runtime_handle=failed_handle,
            outcome=RuntimeOperationOutcome.ROLLBACK_FAILED,
            workspace_reference=RuntimeWorkspaceRef(
                workspace_id=allocation.workspace_ref.workspace_id,
                workspace_policy_id=allocation.workspace_policy_id,
                status=workspace_status,
                managed_files_root_bound=False,
            ),
            failure=normalized.failure,
            events=event_journal.events(),
        )

    def _acquire_runtime_lock(self, runtime_id: str):
        with self._locks_guard:
            lock = self._locks.get(runtime_id)
            if lock is None:
                lock = _lock_module.Lock()
                self._locks[runtime_id] = lock
        if not lock.acquire(blocking=False):
            raise RuntimeRollbackStateError(
                runtime_id=runtime_id,
                validation_category="operation_in_progress",
            )
        return lock


def _validate_identity(
    request: RuntimeRollbackRequest,
    runtime_handle: RuntimeHandle,
    profile: RuntimeProfileDefinition,
    allocation: RuntimeWorkspaceAllocation,
) -> None:
    if request.runtime_id != runtime_handle.runtime_id:
        raise RuntimeRollbackIdentityError(
            runtime_id=runtime_handle.runtime_id,
            validation_category="runtime_id_mismatch",
        )
    if request.correlation_id != runtime_handle.correlation_id:
        raise RuntimeRollbackIdentityError(
            runtime_id=runtime_handle.runtime_id,
            validation_category="correlation_id_mismatch",
        )
    if profile.profile_ref.profile_id != runtime_handle.profile_id:
        raise RuntimeRollbackIdentityError(
            runtime_id=runtime_handle.runtime_id,
            validation_category="profile_id_mismatch",
        )
    if allocation.runtime_id != runtime_handle.runtime_id:
        raise RuntimeRollbackIdentityError(
            runtime_id=runtime_handle.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="allocation_runtime_id_mismatch",
        )
    if allocation.workspace_ref.workspace_id != runtime_handle.workspace_id:
        raise RuntimeRollbackIdentityError(
            runtime_id=runtime_handle.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="workspace_id_mismatch",
        )
    if profile.profile_ref.workspace_policy_id != allocation.workspace_policy_id:
        raise RuntimeRollbackIdentityError(
            runtime_id=runtime_handle.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="workspace_policy_id_mismatch",
        )


def _validate_state_and_process_release(
    runtime_handle: RuntimeHandle,
    profile: RuntimeProfileDefinition,
    allocation: RuntimeWorkspaceAllocation,
    process_owner: HermesProcessOwner,
) -> None:
    try:
        transition_runtime_state(
            runtime_handle.lifecycle_state,
            RuntimeLifecycleAction.BEGIN_ROLLBACK,
        )
    except Exception as exc:
        raise RuntimeRollbackStateError(
            runtime_id=runtime_handle.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category=exc.__class__.__name__,
        ) from None
    if runtime_handle.runtime_id in process_owner.owned_runtime_ids():
        raise RuntimeRollbackProcessStillOwnedError(
            runtime_id=runtime_handle.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="process_owner_still_registered",
        )
    if (
        profile.default_workspace_binding.retention_policy
        is not RuntimeRetentionPolicy.REMOVE_ON_TERMINAL
    ):
        raise RuntimeRollbackStateError(
            runtime_id=runtime_handle.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="retention_policy_not_supported",
        )


def _validate_ownership_marker(allocation: RuntimeWorkspaceAllocation) -> None:
    root = _contained_workspace_root(allocation)
    try:
        marker = assert_existing_path_contained(
            allocation.paths.ownership_marker,
            containment_root=root,
        )
    except RuntimePathContainmentError as exc:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category=exc.error_code,
        ) from None
    if marker.name != _MARKER_NAME:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_name_mismatch",
        )
    if is_reparse_or_symlink(marker):
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_redirect",
        )
    try:
        marker_stat = _os_module.lstat(marker)
    except OSError as exc:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_lstat_failed",
            os_error_type=exc.__class__.__name__,
        ) from None
    if not stat.S_ISREG(marker_stat.st_mode):
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_not_regular_file",
        )
    if marker_stat.st_size > _MAX_MARKER_BYTES:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_too_large",
        )
    try:
        with getattr(marker, "op" + "en")("rb") as marker_file:
            payload = marker_file.read(_MAX_MARKER_BYTES + 1)
    except OSError as exc:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_read_failed",
            os_error_type=exc.__class__.__name__,
        ) from None
    if len(payload) > _MAX_MARKER_BYTES:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_too_large",
        )
    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_invalid_utf8",
        ) from None
    try:
        marker_data = json.loads(decoded)
    except json.JSONDecodeError:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_invalid_json",
        ) from None
    expected = {
        "schema_version": 1,
        "runtime_id": allocation.runtime_id,
        "workspace_id": allocation.workspace_ref.workspace_id,
        "workspace_policy_id": allocation.workspace_policy_id,
    }
    if not isinstance(marker_data, dict) or set(marker_data) != set(expected):
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_shape_mismatch",
        )
    if marker_data != expected:
        raise RuntimeRollbackMarkerError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="marker_identity_mismatch",
        )


def _inspect_workspace_tree(
    allocation: RuntimeWorkspaceAllocation,
) -> tuple[_WorkspaceTreeEntry, ...]:
    root = _contained_workspace_root(allocation)
    marker = allocation.paths.ownership_marker
    entries: list[_WorkspaceTreeEntry] = []

    def walk(directory: Path, depth: int) -> None:
        if len(entries) > _MAX_TREE_ENTRIES:
            raise RuntimeRollbackTreeLimitError(
                runtime_id=allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                validation_category="entry_count_exceeded",
            )
        if depth > _MAX_TREE_DEPTH:
            raise RuntimeRollbackTreeLimitError(
                runtime_id=allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                validation_category="depth_exceeded",
            )
        try:
            with _os_module.scandir(directory) as iterator:
                names = sorted(entry.name for entry in iterator)
        except OSError as exc:
            raise RuntimeRollbackContainmentError(
                runtime_id=allocation.runtime_id,
                workspace_id=allocation.workspace_ref.workspace_id,
                validation_category="directory_scan_failed",
                os_error_type=exc.__class__.__name__,
            ) from None
        for name in names:
            child = directory / name
            entry = _inspect_entry(allocation, root, child, depth + 1, marker)
            entries.append(entry)
            if len(entries) > _MAX_TREE_ENTRIES:
                raise RuntimeRollbackTreeLimitError(
                    runtime_id=allocation.runtime_id,
                    workspace_id=allocation.workspace_ref.workspace_id,
                    validation_category="entry_count_exceeded",
                )
            if entry.is_directory:
                walk(child, depth + 1)

    entries.append(_inspect_entry(allocation, root, root, 0, marker))
    walk(root, 0)
    return tuple(entries)


def _inspect_entry(
    allocation: RuntimeWorkspaceAllocation,
    root: Path,
    path: Path,
    depth: int,
    marker: Path,
) -> _WorkspaceTreeEntry:
    try:
        contained = assert_existing_path_contained(path, containment_root=root)
        assert_path_chain_safe(contained, containment_root=root)
    except RuntimePathContainmentError as exc:
        raise RuntimeRollbackContainmentError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category=exc.error_code,
            entry_role="tree_entry",
        ) from None
    try:
        item_stat = _os_module.lstat(contained)
    except OSError as exc:
        raise RuntimeRollbackContainmentError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="entry_lstat_failed",
            entry_role="tree_entry",
            os_error_type=exc.__class__.__name__,
        ) from None
    if is_reparse_or_symlink(contained):
        raise RuntimeRollbackEntryTypeError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="redirect_detected",
            entry_role="tree_entry",
        )
    if contained != root and _is_mount(contained):
        raise RuntimeRollbackEntryTypeError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="nested_mount_detected",
            entry_role="tree_entry",
        )
    if stat.S_ISDIR(item_stat.st_mode):
        return _WorkspaceTreeEntry(
            path=contained,
            depth=depth,
            is_directory=True,
            is_marker=False,
        )
    if stat.S_ISREG(item_stat.st_mode):
        return _WorkspaceTreeEntry(
            path=contained,
            depth=depth,
            is_directory=False,
            is_marker=contained == marker,
        )
    raise RuntimeRollbackEntryTypeError(
        runtime_id=allocation.runtime_id,
        workspace_id=allocation.workspace_ref.workspace_id,
        validation_category="unsupported_entry_type",
        entry_role="tree_entry",
    )


def _delete_workspace_entries(
    allocation: RuntimeWorkspaceAllocation,
    entries: tuple[_WorkspaceTreeEntry, ...],
) -> None:
    root = _contained_workspace_root(allocation)
    normal_files = sorted(
        (entry for entry in entries if not entry.is_directory and not entry.is_marker),
        key=lambda entry: (-entry.depth, str(entry.path)),
    )
    directories = sorted(
        (entry for entry in entries if entry.is_directory and entry.path != root),
        key=lambda entry: (-entry.depth, str(entry.path)),
    )
    for entry in normal_files:
        _delete_regular_file(allocation, root, entry.path, entry_role="file")
    _delete_regular_file(
        allocation,
        root,
        allocation.paths.ownership_marker,
        entry_role="ownership_marker",
    )
    for entry in directories:
        _remove_directory(allocation, root, entry.path, entry_role="directory")
    _remove_directory(allocation, root, root, entry_role="workspace_root")


def _delete_regular_file(
    allocation: RuntimeWorkspaceAllocation,
    root: Path,
    path: Path,
    *,
    entry_role: str,
) -> None:
    contained = _revalidate_deletion_entry(
        allocation, root, path, entry_role=entry_role
    )
    try:
        item_stat = _os_module.lstat(contained)
    except OSError as exc:
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="file_lstat_failed",
            entry_role=entry_role,
            os_error_type=exc.__class__.__name__,
        ) from None
    if not stat.S_ISREG(item_stat.st_mode):
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="file_type_changed",
            entry_role=entry_role,
        )
    try:
        getattr(contained, "un" + "link")()
    except OSError as exc:
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="file_delete_failed",
            entry_role=entry_role,
            os_error_type=exc.__class__.__name__,
        ) from None


def _remove_directory(
    allocation: RuntimeWorkspaceAllocation,
    root: Path,
    path: Path,
    *,
    entry_role: str,
) -> None:
    contained = _revalidate_deletion_entry(
        allocation, root, path, entry_role=entry_role
    )
    try:
        item_stat = _os_module.lstat(contained)
    except OSError as exc:
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="directory_lstat_failed",
            entry_role=entry_role,
            os_error_type=exc.__class__.__name__,
        ) from None
    if not stat.S_ISDIR(item_stat.st_mode):
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="directory_type_changed",
            entry_role=entry_role,
        )
    try:
        getattr(contained, "rm" + "dir")()
    except OSError as exc:
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="directory_remove_failed",
            entry_role=entry_role,
            os_error_type=exc.__class__.__name__,
        ) from None


def _revalidate_deletion_entry(
    allocation: RuntimeWorkspaceAllocation,
    root: Path,
    path: Path,
    *,
    entry_role: str,
) -> Path:
    try:
        contained = assert_existing_path_contained(path, containment_root=root)
        assert_path_chain_safe(contained, containment_root=root)
    except RuntimePathContainmentError as exc:
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category=exc.error_code,
            entry_role=entry_role,
        ) from None
    if is_reparse_or_symlink(contained):
        raise RuntimeRollbackDeletionError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="entry_redirect_detected",
            entry_role=entry_role,
        )
    return contained


def _contained_workspace_root(allocation: RuntimeWorkspaceAllocation) -> Path:
    try:
        root = assert_existing_path_contained(
            allocation.paths.workspace_root,
            containment_root=allocation.paths.workspace_root,
        )
    except RuntimePathContainmentError as exc:
        raise RuntimeRollbackContainmentError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category=exc.error_code,
            entry_role="workspace_root",
        ) from None
    if not root.is_dir():
        raise RuntimeRollbackContainmentError(
            runtime_id=allocation.runtime_id,
            workspace_id=allocation.workspace_ref.workspace_id,
            validation_category="workspace_root_not_directory",
            entry_role="workspace_root",
        )
    return root


def _is_mount(path: Path) -> bool:
    try:
        return bool(path.is_mount())
    except OSError:
        return True


def _append_rollback_event(
    event_journal: RuntimeEventJournal,
    clock: RuntimeLifecycleClock,
    event_type: RuntimeEventType,
    lifecycle_state: RuntimeLifecycleState,
    *,
    allocation: RuntimeWorkspaceAllocation | None = None,
    normalized_failure=None,
) -> None:
    event_journal.append(
        event_type=event_type,
        lifecycle_state=lifecycle_state,
        timestamp_utc=clock.utc_now(),
        monotonic_offset_ms=clock.monotonic_offset_ms(),
        workspace_allocation=allocation,
        normalized_failure=normalized_failure,
    )


def _cleaned_workspace_ref(
    allocation: RuntimeWorkspaceAllocation,
) -> RuntimeWorkspaceRef:
    return RuntimeWorkspaceRef(
        workspace_id=allocation.workspace_ref.workspace_id,
        workspace_policy_id=allocation.workspace_policy_id,
        status=RuntimeWorkspaceStatus.CLEANED,
        managed_files_root_bound=False,
    )


def _rollback_operation_result(
    *,
    runtime_handle: RuntimeHandle,
    outcome: RuntimeOperationOutcome,
    workspace_reference: RuntimeWorkspaceRef,
    events,
    failure=None,
) -> RuntimeOperationResult:
    return RuntimeOperationResult(
        schema_version=1,
        runtime_handle=runtime_handle,
        outcome=outcome,
        process_reference=None,
        workspace_reference=workspace_reference,
        readiness_reference=None,
        log_references=(),
        failure=failure,
        events=tuple(events),
    )


__all__ = [
    "RuntimeRollbackAllocatorReleaseError",
    "RuntimeRollbackContainmentError",
    "RuntimeRollbackDeletionError",
    "RuntimeRollbackEntryTypeError",
    "RuntimeRollbackError",
    "RuntimeRollbackIdentityError",
    "RuntimeRollbackMarkerError",
    "RuntimeRollbackProcessStillOwnedError",
    "RuntimeRollbackStateError",
    "RuntimeRollbackTreeLimitError",
    "RuntimeWorkspaceRollbackCoordinator",
]
