"""Internal path-containment primitives for governed runtime workspaces."""

from __future__ import annotations

import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath

from hermes_cli.agent_platform.runtime_adapter.environment import RuntimePlatformFamily


_MAX_SEGMENT_CHARACTERS = 128
_MAX_ERROR_FIELD_CHARACTERS = 120
_WINDOWS_REPARSE_ATTRIBUTE = 0x400
_WINDOWS_RESERVED_BASENAMES = frozenset({
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "CLOCK$",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
})


def _default_platform_family() -> RuntimePlatformFamily:
    if sys.platform == "win32":
        return RuntimePlatformFamily.WINDOWS
    return RuntimePlatformFamily.POSIX


def _coerce_platform_family(
    platform_family: RuntimePlatformFamily | str | None,
) -> RuntimePlatformFamily:
    if platform_family is None:
        return _default_platform_family()
    if isinstance(platform_family, RuntimePlatformFamily):
        return platform_family
    return RuntimePlatformFamily(platform_family)


def _safe_text(value: object) -> str:
    text = str(value)
    return "".join(character for character in text if 32 <= ord(character) < 127)[
        :_MAX_ERROR_FIELD_CHARACTERS
    ]


def _safe_basename(path: object) -> str | None:
    try:
        name = Path(path).name
    except TypeError:
        return None
    if not name:
        return None
    return _safe_text(name)


def _has_nul_or_control(value: str) -> bool:
    return any(ord(character) < 32 for character in value)


def _is_windows_unc_or_device_text(value: str) -> bool:
    normalized = "\\".join(value.split("/"))
    lowered = normalized.casefold()
    return normalized.startswith("\\\\") or lowered.startswith(("\\\\?\\", "\\\\.\\"))


class RuntimePathContainmentError(RuntimeError):
    """Base class for bounded runtime path-containment errors."""

    error_code = "runtime_path_containment_error"

    def __init__(
        self,
        *,
        validation_category: str,
        path_role: str | None = None,
        platform_family: RuntimePlatformFamily | str | None = None,
        basename: object | None = None,
        os_error_type: str | None = None,
    ) -> None:
        self.validation_category = validation_category
        self.path_role = path_role
        self.platform_family = (
            _coerce_platform_family(platform_family)
            if platform_family is not None
            else None
        )
        self.basename = _safe_text(basename) if basename is not None else None
        self.os_error_type = _safe_text(os_error_type) if os_error_type else None
        fragments = [f"code={self.error_code}"]
        fragments.append(f"validation_category={validation_category}")
        if path_role is not None:
            fragments.append(f"path_role={_safe_text(path_role)}")
        if self.platform_family is not None:
            fragments.append(f"platform_family={self.platform_family.value}")
        if self.basename is not None:
            fragments.append(f"basename={self.basename}")
        if self.os_error_type is not None:
            fragments.append(f"os_error_type={self.os_error_type}")
        super().__init__(" ".join(fragments))


class InvalidTrustedBaseRootError(RuntimePathContainmentError):
    error_code = "invalid_trusted_base_root"


class InvalidRuntimePathSegmentError(RuntimePathContainmentError):
    error_code = "invalid_runtime_path_segment"


class PathOutsideContainmentRootError(RuntimePathContainmentError):
    error_code = "path_outside_containment_root"


class PathRedirectDetectedError(RuntimePathContainmentError):
    error_code = "path_redirect_detected"


class UnsupportedPathInspectionError(RuntimePathContainmentError):
    error_code = "unsupported_path_inspection"


class UnsafeRuntimePathError(RuntimePathContainmentError):
    error_code = "unsafe_runtime_path"


@dataclass(frozen=True, slots=True)
class _PathMetadata:
    is_redirect: bool
    inspection_supported: bool


def validate_trusted_base_root(base_root: Path) -> Path:
    """Return a canonical trusted base root or fail closed."""

    platform_family = _default_platform_family()
    root = Path(base_root)
    _validate_path_text(
        root, path_role="trusted_base_root", platform_family=platform_family
    )
    if _is_windows_forbidden_root_text(str(root)):
        raise InvalidTrustedBaseRootError(
            validation_category="unsupported_windows_root",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    if not root.is_absolute():
        raise InvalidTrustedBaseRootError(
            validation_category="not_absolute",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    if not root.exists():
        raise InvalidTrustedBaseRootError(
            validation_category="missing",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    if is_reparse_or_symlink(root):
        raise PathRedirectDetectedError(
            validation_category="trusted_base_redirect",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    if not root.is_dir():
        raise InvalidTrustedBaseRootError(
            validation_category="not_directory",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    try:
        resolved = root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise InvalidTrustedBaseRootError(
            validation_category="resolve_failed",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
            os_error_type=exc.__class__.__name__,
        ) from None
    if _is_filesystem_root(resolved):
        raise InvalidTrustedBaseRootError(
            validation_category="filesystem_root",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    if platform_family is RuntimePlatformFamily.WINDOWS and _is_windows_drive_root(
        resolved
    ):
        raise InvalidTrustedBaseRootError(
            validation_category="drive_root",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    if is_reparse_or_symlink(resolved):
        raise PathRedirectDetectedError(
            validation_category="trusted_base_redirect",
            path_role="trusted_base_root",
            platform_family=platform_family,
            basename=_safe_basename(root),
        )
    return resolved


def validate_safe_path_segment(
    segment: str,
    *,
    platform_family: RuntimePlatformFamily | str | None = None,
) -> str:
    """Validate one allocator-owned filesystem path segment."""

    family = _coerce_platform_family(platform_family)
    if not isinstance(segment, str) or not segment:
        raise InvalidRuntimePathSegmentError(
            validation_category="empty_segment",
            path_role="path_segment",
            platform_family=family,
        )
    if len(segment) > _MAX_SEGMENT_CHARACTERS:
        raise InvalidRuntimePathSegmentError(
            validation_category="segment_too_long",
            path_role="path_segment",
            platform_family=family,
            basename=segment,
        )
    if segment != segment.strip():
        raise InvalidRuntimePathSegmentError(
            validation_category="leading_or_trailing_whitespace",
            path_role="path_segment",
            platform_family=family,
            basename=segment,
        )
    if segment in {".", ".."}:
        raise InvalidRuntimePathSegmentError(
            validation_category="dot_segment",
            path_role="path_segment",
            platform_family=family,
            basename=segment,
        )
    if _has_nul_or_control(segment):
        raise InvalidRuntimePathSegmentError(
            validation_category="control_character",
            path_role="path_segment",
            platform_family=family,
            basename=segment,
        )
    if any(character in segment for character in ("/", "\\", ":")):
        raise InvalidRuntimePathSegmentError(
            validation_category="separator_or_colon",
            path_role="path_segment",
            platform_family=family,
            basename=segment,
        )
    if family is RuntimePlatformFamily.WINDOWS:
        if segment.endswith((" ", ".")):
            raise InvalidRuntimePathSegmentError(
                validation_category="windows_trailing_space_or_dot",
                path_role="path_segment",
                platform_family=family,
                basename=segment,
            )
        basename = segment.split(".", 1)[0].casefold().upper()
        if basename in _WINDOWS_RESERVED_BASENAMES:
            raise InvalidRuntimePathSegmentError(
                validation_category="windows_reserved_name",
                path_role="path_segment",
                platform_family=family,
                basename=segment,
            )
    return segment


def join_contained_child(
    parent: Path,
    segment: str,
    *,
    containment_root: Path,
    platform_family: RuntimePlatformFamily | str | None = None,
) -> Path:
    """Join one validated segment below an existing contained parent."""

    family = _coerce_platform_family(platform_family)
    safe_segment = validate_safe_path_segment(segment, platform_family=family)
    canonical_parent = assert_existing_path_contained(
        Path(parent), containment_root=containment_root, platform_family=family
    )
    candidate = canonical_parent / safe_segment
    _assert_lexical_containment(candidate, containment_root, platform_family=family)
    if candidate.exists():
        return assert_existing_path_contained(
            candidate, containment_root=containment_root, platform_family=family
        )
    assert_path_chain_safe(
        candidate, containment_root=containment_root, platform_family=family
    )
    return candidate


def assert_existing_path_contained(
    candidate: Path,
    *,
    containment_root: Path,
    platform_family: RuntimePlatformFamily | str | None = None,
) -> Path:
    """Return canonical candidate when it exists below the containment root."""

    family = _coerce_platform_family(platform_family)
    root = _canonical_existing_path(
        Path(containment_root),
        path_role="containment_root",
        platform_family=family,
        require_directory=True,
    )
    path = Path(candidate)
    _validate_path_text(path, path_role="candidate", platform_family=family)
    if not path.is_absolute():
        raise UnsafeRuntimePathError(
            validation_category="candidate_not_absolute",
            path_role="candidate",
            platform_family=family,
            basename=_safe_basename(path),
        )
    if not path.exists():
        raise UnsafeRuntimePathError(
            validation_category="candidate_missing",
            path_role="candidate",
            platform_family=family,
            basename=_safe_basename(path),
        )
    _assert_chain_has_no_redirects(path, containment_root=root, platform_family=family)
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise UnsafeRuntimePathError(
            validation_category="candidate_resolve_failed",
            path_role="candidate",
            platform_family=family,
            basename=_safe_basename(path),
            os_error_type=exc.__class__.__name__,
        ) from None
    _assert_canonical_containment(resolved, root, platform_family=family)
    if is_reparse_or_symlink(resolved):
        raise PathRedirectDetectedError(
            validation_category="candidate_redirect",
            path_role="candidate",
            platform_family=family,
            basename=_safe_basename(path),
        )
    return resolved


def assert_path_chain_safe(
    candidate: Path,
    *,
    containment_root: Path,
    platform_family: RuntimePlatformFamily | str | None = None,
) -> None:
    """Validate an existing path or a safe nonexistent descendant chain."""

    family = _coerce_platform_family(platform_family)
    root = _canonical_existing_path(
        Path(containment_root),
        path_role="containment_root",
        platform_family=family,
        require_directory=True,
    )
    path = Path(candidate)
    _validate_path_text(path, path_role="candidate", platform_family=family)
    if not path.is_absolute():
        raise UnsafeRuntimePathError(
            validation_category="candidate_not_absolute",
            path_role="candidate",
            platform_family=family,
            basename=_safe_basename(path),
        )
    _assert_anchor_compatible(path, root, platform_family=family)
    if path.exists():
        assert_existing_path_contained(
            path, containment_root=root, platform_family=family
        )
        return

    missing_segments: list[str] = []
    current = path
    while not current.exists():
        missing_segments.append(current.name)
        parent = current.parent
        if parent == current:
            raise UnsafeRuntimePathError(
                validation_category="no_existing_ancestor",
                path_role="candidate",
                platform_family=family,
                basename=_safe_basename(path),
            )
        current = parent
    ancestor = assert_existing_path_contained(
        current, containment_root=root, platform_family=family
    )
    probe = ancestor
    for segment in reversed(missing_segments):
        safe_segment = validate_safe_path_segment(segment, platform_family=family)
        probe = probe / safe_segment
        _assert_lexical_containment(probe, root, platform_family=family)


def is_reparse_or_symlink(path: Path) -> bool:
    """Return true for symlinks, junctions, mount reparse points or unknown redirects."""

    metadata = _path_metadata(Path(path))
    return metadata.is_redirect


def validate_managed_files_root_candidate(
    candidate: Path,
    *,
    containment_root: Path,
    platform_family: RuntimePlatformFamily | str | None = None,
) -> Path:
    """Validate an existing managed Files-root directory candidate."""

    family = _coerce_platform_family(platform_family)
    resolved = assert_existing_path_contained(
        Path(candidate), containment_root=containment_root, platform_family=family
    )
    if not resolved.is_dir():
        raise UnsafeRuntimePathError(
            validation_category="managed_files_root_not_directory",
            path_role="managed_files_root",
            platform_family=family,
            basename=_safe_basename(resolved),
        )
    return resolved


def _path_metadata(path: Path) -> _PathMetadata:
    try:
        item_stat = os.lstat(path)
    except OSError as exc:
        raise UnsupportedPathInspectionError(
            validation_category="lstat_failed",
            path_role="path",
            platform_family=_default_platform_family(),
            basename=_safe_basename(path),
            os_error_type=exc.__class__.__name__,
        ) from None
    is_redirect = stat.S_ISLNK(item_stat.st_mode)
    attributes = getattr(item_stat, "st_file_attributes", None)
    if attributes is not None and attributes & _WINDOWS_REPARSE_ATTRIBUTE:
        is_redirect = True
    return _PathMetadata(is_redirect=is_redirect, inspection_supported=True)


def _validate_path_text(
    path: Path,
    *,
    path_role: str,
    platform_family: RuntimePlatformFamily,
) -> None:
    text = str(path)
    if not text or _has_nul_or_control(text):
        raise UnsafeRuntimePathError(
            validation_category="path_text_invalid",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    if ".." in path.parts:
        raise UnsafeRuntimePathError(
            validation_category="parent_segment",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    if _is_windows_forbidden_root_text(text):
        raise UnsafeRuntimePathError(
            validation_category="unsupported_windows_path",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )


def _is_windows_forbidden_root_text(value: str) -> bool:
    return _is_windows_unc_or_device_text(value)


def _is_filesystem_root(path: Path) -> bool:
    return path.parent == path


def _is_windows_drive_root(path: Path) -> bool:
    pure = PureWindowsPath(str(path))
    return bool(pure.drive) and str(pure) == pure.anchor


def _canonical_existing_path(
    path: Path,
    *,
    path_role: str,
    platform_family: RuntimePlatformFamily,
    require_directory: bool,
) -> Path:
    _validate_path_text(path, path_role=path_role, platform_family=platform_family)
    if not path.is_absolute():
        raise UnsafeRuntimePathError(
            validation_category=f"{path_role}_not_absolute",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    if not path.exists():
        raise UnsafeRuntimePathError(
            validation_category=f"{path_role}_missing",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    if is_reparse_or_symlink(path):
        raise PathRedirectDetectedError(
            validation_category=f"{path_role}_redirect",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    if require_directory and not path.is_dir():
        raise UnsafeRuntimePathError(
            validation_category=f"{path_role}_not_directory",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise UnsafeRuntimePathError(
            validation_category=f"{path_role}_resolve_failed",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
            os_error_type=exc.__class__.__name__,
        ) from None
    if is_reparse_or_symlink(resolved):
        raise PathRedirectDetectedError(
            validation_category=f"{path_role}_redirect",
            path_role=path_role,
            platform_family=platform_family,
            basename=_safe_basename(path),
        )
    return resolved


def _assert_chain_has_no_redirects(
    candidate: Path,
    *,
    containment_root: Path,
    platform_family: RuntimePlatformFamily,
) -> None:
    root = containment_root
    path = Path(candidate)
    if path.exists():
        parts_to_check = _contained_existing_chain(
            path, root, platform_family=platform_family
        )
    else:
        parts_to_check = _contained_existing_chain(
            _nearest_existing_ancestor(path), root, platform_family=platform_family
        )
    for part in parts_to_check:
        if is_reparse_or_symlink(part):
            raise PathRedirectDetectedError(
                validation_category="redirect_in_path_chain",
                path_role="candidate",
                platform_family=platform_family,
                basename=_safe_basename(part),
            )


def _nearest_existing_ancestor(candidate: Path) -> Path:
    current = Path(candidate)
    while not current.exists():
        parent = current.parent
        if parent == current:
            return current
        current = parent
    return current


def _contained_existing_chain(
    existing: Path,
    root: Path,
    *,
    platform_family: RuntimePlatformFamily,
) -> tuple[Path, ...]:
    absolute_existing = Path(existing)
    if not absolute_existing.is_absolute():
        raise UnsafeRuntimePathError(
            validation_category="candidate_not_absolute",
            path_role="candidate",
            platform_family=platform_family,
            basename=_safe_basename(existing),
        )
    _assert_canonical_containment(
        absolute_existing, root, platform_family=platform_family
    )
    if _path_key(absolute_existing, platform_family) == _path_key(
        root, platform_family
    ):
        return (root,)
    relative = Path(*absolute_existing.parts[len(root.parts) :])
    chain = [root]
    probe = root
    for part in relative.parts:
        probe = probe / part
        if probe.exists():
            chain.append(probe)
    return tuple(chain)


def _assert_lexical_containment(
    candidate: Path,
    containment_root: Path,
    *,
    platform_family: RuntimePlatformFamily,
) -> None:
    candidate_path = Path(candidate)
    root_path = Path(containment_root)
    if not candidate_path.is_absolute() or not root_path.is_absolute():
        raise UnsafeRuntimePathError(
            validation_category="lexical_path_not_absolute",
            path_role="candidate",
            platform_family=platform_family,
            basename=_safe_basename(candidate_path),
        )
    _assert_canonical_containment(
        candidate_path, root_path, platform_family=platform_family
    )


def _assert_canonical_containment(
    candidate: Path,
    containment_root: Path,
    *,
    platform_family: RuntimePlatformFamily,
) -> None:
    candidate_key = _path_key(candidate, platform_family)
    root_key = _path_key(containment_root, platform_family)
    if len(candidate_key) < len(root_key):
        raise PathOutsideContainmentRootError(
            validation_category="candidate_not_descendant",
            path_role="candidate",
            platform_family=platform_family,
            basename=_safe_basename(candidate),
        )
    if candidate_key[: len(root_key)] != root_key:
        raise PathOutsideContainmentRootError(
            validation_category="candidate_not_descendant",
            path_role="candidate",
            platform_family=platform_family,
            basename=_safe_basename(candidate),
        )


def _assert_anchor_compatible(
    candidate: Path,
    containment_root: Path,
    *,
    platform_family: RuntimePlatformFamily,
) -> None:
    candidate_parts = _path_key(candidate, platform_family)
    root_parts = _path_key(containment_root, platform_family)
    if not candidate_parts or not root_parts or candidate_parts[0] != root_parts[0]:
        raise PathOutsideContainmentRootError(
            validation_category="anchor_mismatch",
            path_role="candidate",
            platform_family=platform_family,
            basename=_safe_basename(candidate),
        )


def _path_key(path: Path, platform_family: RuntimePlatformFamily) -> tuple[str, ...]:
    parts = Path(path).parts
    if platform_family is RuntimePlatformFamily.WINDOWS:
        return tuple(part.casefold() for part in parts)
    return tuple(parts)
