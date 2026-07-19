from __future__ import annotations

import stat
import sys
from pathlib import Path

import pytest

from hermes_cli.agent_platform.runtime_adapter import path_containment as pc
from hermes_cli.agent_platform.runtime_adapter.environment import RuntimePlatformFamily
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    InvalidRuntimePathSegmentError,
    InvalidTrustedBaseRootError,
    PathOutsideContainmentRootError,
    PathRedirectDetectedError,
    RuntimePathContainmentError,
    UnsafeRuntimePathError,
    UnsupportedPathInspectionError,
    assert_existing_path_contained,
    assert_path_chain_safe,
    is_reparse_or_symlink,
    join_contained_child,
    validate_safe_path_segment,
    validate_trusted_base_root,
)


SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "path_containment.py"
)


def test_trusted_base_root_accepts_only_existing_non_root_directory(
    tmp_path: Path,
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    file_root = tmp_path / "file.txt"
    file_root.write_text("x", encoding="utf-8")

    assert validate_trusted_base_root(base) == base.resolve()

    with pytest.raises(InvalidTrustedBaseRootError):
        validate_trusted_base_root(Path("relative-root"))
    with pytest.raises(InvalidTrustedBaseRootError):
        validate_trusted_base_root(tmp_path / "missing")
    with pytest.raises(InvalidTrustedBaseRootError):
        validate_trusted_base_root(file_root)
    with pytest.raises(InvalidTrustedBaseRootError):
        validate_trusted_base_root(Path(tmp_path.anchor))
    with pytest.raises((InvalidTrustedBaseRootError, UnsafeRuntimePathError)):
        validate_trusted_base_root(Path(r"\\server\share"))
    with pytest.raises((InvalidTrustedBaseRootError, UnsafeRuntimePathError)):
        validate_trusted_base_root(Path(r"\\?\C:\runtime"))
    with pytest.raises((InvalidTrustedBaseRootError, UnsafeRuntimePathError)):
        validate_trusted_base_root(Path(r"\\.\device"))


def test_trusted_base_root_rejects_symlink_and_reparse_point(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("host does not allow directory symlink creation")

    with pytest.raises(PathRedirectDetectedError):
        validate_trusted_base_root(link)

    def fake_is_redirect(path: Path) -> bool:
        return Path(path) == base

    monkeypatch.setattr(pc, "is_reparse_or_symlink", fake_is_redirect)
    with pytest.raises(PathRedirectDetectedError):
        validate_trusted_base_root(base)


@pytest.mark.parametrize(
    "segment",
    [
        "",
        ".",
        "..",
        "bad/name",
        r"bad\name",
        "bad:name",
        "bad\x00name",
        "bad\nname",
        " leading",
        "trailing ",
        "x" * 129,
    ],
)
def test_safe_path_segment_rejects_unsafe_values(segment: str) -> None:
    with pytest.raises(InvalidRuntimePathSegmentError):
        validate_safe_path_segment(segment)


@pytest.mark.parametrize(
    "segment",
    ["CON", "con", "CON.txt", "PRN", "AUX", "NUL", "CLOCK$", "COM1", "LPT9", "name."],
)
def test_safe_path_segment_rejects_windows_reserved_names(segment: str) -> None:
    with pytest.raises(InvalidRuntimePathSegmentError):
        validate_safe_path_segment(
            segment, platform_family=RuntimePlatformFamily.WINDOWS
        )


def test_safe_path_segment_accepts_normal_single_segment() -> None:
    assert validate_safe_path_segment("workspace-logs_01") == "workspace-logs_01"


def test_canonical_containment_accepts_root_and_children_rejects_escapes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "runtime-ws"
    root.mkdir()
    child = root / "child"
    child.mkdir()
    sibling = tmp_path / "runtime-ws-escape"
    sibling.mkdir()

    assert assert_existing_path_contained(root, containment_root=root) == root.resolve()
    assert (
        assert_existing_path_contained(child, containment_root=root) == child.resolve()
    )
    with pytest.raises(PathOutsideContainmentRootError):
        assert_existing_path_contained(sibling, containment_root=root)
    with pytest.raises(UnsafeRuntimePathError):
        assert_path_chain_safe(root / ".." / sibling.name, containment_root=root)
    with pytest.raises(PathOutsideContainmentRootError):
        assert_path_chain_safe(sibling / "future", containment_root=root)
    with pytest.raises(UnsafeRuntimePathError):
        assert_path_chain_safe(Path("relative"), containment_root=root)


def test_windows_case_insensitive_and_posix_case_sensitive_comparison(
    tmp_path: Path,
) -> None:
    root = tmp_path / "CaseRoot"
    root.mkdir()
    swapped = Path(str(root).swapcase())

    assert_existing_path_contained(
        swapped,
        containment_root=root,
        platform_family=RuntimePlatformFamily.WINDOWS,
    )
    with pytest.raises(PathOutsideContainmentRootError):
        assert_existing_path_contained(
            swapped,
            containment_root=root,
            platform_family=RuntimePlatformFamily.POSIX,
        )


def test_different_drive_or_anchor_is_rejected_for_nonexistent_candidate(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    root.mkdir()
    if sys.platform == "win32":
        drive = "Z:" if not str(root).casefold().startswith("z:") else "Y:"
        candidate = Path(drive + r"\outside\child")
    else:
        candidate = Path("/outside-runtime-root/child")

    with pytest.raises(RuntimePathContainmentError):
        assert_path_chain_safe(candidate, containment_root=root)


def test_symlink_redirect_rejected_even_when_target_is_inside_root(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    root.mkdir()
    target = root / "target"
    target.mkdir()
    link = root / "link"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("host does not allow directory symlink creation")

    with pytest.raises(PathRedirectDetectedError):
        assert_existing_path_contained(link, containment_root=root)
    with pytest.raises(PathRedirectDetectedError):
        assert_path_chain_safe(link / "future", containment_root=root)


def test_windows_reparse_detection_and_ambiguous_inspection_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class FakeStat:
        st_mode = stat.S_IFDIR
        st_file_attributes = 0x400

    monkeypatch.setattr(pc.os, "lstat", lambda _path: FakeStat())
    assert is_reparse_or_symlink(tmp_path) is True

    def raise_lstat(_path: Path):
        raise OSError("synthetic failure")

    monkeypatch.setattr(pc.os, "lstat", raise_lstat)
    with pytest.raises(UnsupportedPathInspectionError):
        is_reparse_or_symlink(tmp_path)


def test_nonexistent_children_validate_without_creation(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    ancestor = root / "ancestor"
    ancestor.mkdir()

    child = join_contained_child(root, "child", containment_root=root)
    nested = ancestor / "nested" / "leaf"
    assert child == root / "child"
    assert not child.exists()
    assert_path_chain_safe(nested, containment_root=root)
    assert not nested.exists()
    with pytest.raises(InvalidRuntimePathSegmentError):
        join_contained_child(root, "bad/name", containment_root=root)


def test_path_errors_are_bounded_and_do_not_expose_full_paths(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()

    with pytest.raises(PathOutsideContainmentRootError) as exc_info:
        assert_existing_path_contained(outside, containment_root=root)

    message = str(exc_info.value)
    assert "code=path_outside_containment_root" in message
    assert str(tmp_path) not in message


def test_path_containment_source_guard_blocks_unauthorized_runtime_behavior() -> None:
    text = SOURCE_PATH.read_text(encoding="utf-8")
    lowered = text.lower()
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
        "worker launch",
        "agent launch",
        "mcp execution",
    }
    for forbidden in forbidden_text:
        assert forbidden not in lowered, forbidden
