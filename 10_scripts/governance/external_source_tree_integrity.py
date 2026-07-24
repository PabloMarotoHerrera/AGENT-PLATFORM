#!/usr/bin/env python3
"""Canonical integrity utility for ignored external source trees."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


GIT_SOURCE_ALGORITHM = "agent-platform-git-source-tree-sha256-v2"
MATERIALIZED_SOURCE_ALGORITHM = "agent-platform-materialized-source-tree-sha256-v1"
RECORD_FORMAT = "path-utf8-nul-byte-count-nul-content-sha256-lf"
REGULAR_GIT_MODES = frozenset({"100644", "100755"})
SYMLINK_GIT_MODE = "120000"
SUBMODULE_GIT_MODE = "160000"
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1\n"
MANIFEST_COLUMNS = (
    "source_repository",
    "source_tag",
    "source_commit",
    "entry_type",
    "relative_path",
    "git_mode",
    "git_object_id",
    "git_bytes",
    "git_sha256",
    "materialized_bytes",
    "materialized_sha256",
    "verification_status",
)


class IntegrityError(RuntimeError):
    """Raised when canonical integrity cannot be computed safely."""


@dataclass(frozen=True, slots=True)
class FileRecord:
    """One regular file selected for canonical aggregate hashing."""

    path_bytes: bytes
    data: bytes
    git_mode: str | None = None
    git_object_id: str | None = None

    @property
    def path(self) -> str:
        return self.path_bytes.decode("utf-8")

    @property
    def byte_count(self) -> int:
        return len(self.data)

    @property
    def content_sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


@dataclass(frozen=True, slots=True)
class GitTreeEntry:
    mode: str
    object_type: str
    object_id: str
    path_bytes: bytes

    @property
    def path(self) -> str:
        return self.path_bytes.decode("utf-8")


@dataclass(frozen=True, slots=True)
class SourceScan:
    algorithm: str
    records: tuple[FileRecord, ...]
    directories: int
    zero_byte_files: int
    symlinks: int = 0
    reparse_points: int = 0
    submodules: int = 0
    special_entries: int = 0
    nested_git_directories: int = 0
    nested_git_files: int = 0
    lfs_pointers: int = 0

    @property
    def files(self) -> int:
        return len(self.records)

    @property
    def bytes(self) -> int:
        return sum(record.byte_count for record in self.records)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(record_stream(self.records)).hexdigest()

    def as_result(self) -> dict[str, object]:
        return {
            "algorithm": self.algorithm,
            "record_format": RECORD_FORMAT,
            "files": self.files,
            "directories": self.directories,
            "bytes": self.bytes,
            "zero_byte_files": self.zero_byte_files,
            "symlinks": self.symlinks,
            "reparse_points": self.reparse_points,
            "submodules": self.submodules,
            "special_entries": self.special_entries,
            "nested_git_directories": self.nested_git_directories,
            "nested_git_files": self.nested_git_files,
            "lfs_pointers": self.lfs_pointers,
            "sha256": self.sha256,
        }


def _run_git(git_repo: Path, args: Sequence[str], *, stdin: bytes | None = None) -> bytes:
    command = ["git", "-C", str(git_repo), *args]
    try:
        return subprocess.check_output(command, input=stdin, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace").strip()
        detail = f": {stderr}" if stderr else ""
        raise IntegrityError(f"git command failed: {' '.join(command)}{detail}") from exc


def resolve_commit(git_repo: Path, commitish: str) -> str:
    return _run_git(git_repo, ["rev-parse", f"{commitish}^{{commit}}"]).decode("ascii").strip()


def _validate_relative_path_bytes(path_bytes: bytes) -> None:
    try:
        path = path_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntegrityError("source path is not valid UTF-8") from exc
    if not path:
        raise IntegrityError("empty source path")
    if "\x00" in path or "\t" in path or "\r" in path or "\n" in path:
        raise IntegrityError(f"source path is not TSV-safe: {path!r}")
    if path.startswith("/") or "\\" in path or "//" in path:
        raise IntegrityError(f"unsafe source path: {path!r}")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise IntegrityError(f"unsafe source path: {path!r}")


def _path_has_git_component(path_bytes: bytes) -> bool:
    return ".git" in path_bytes.decode("utf-8").split("/")


def record_stream(records: Iterable[FileRecord]) -> bytes:
    """Return the exact canonical record stream for external source files."""

    chunks: list[bytes] = []
    for record in sorted(records, key=lambda item: item.path_bytes):
        _validate_relative_path_bytes(record.path_bytes)
        chunks.extend(
            (
                record.path_bytes,
                b"\0",
                str(record.byte_count).encode("ascii"),
                b"\0",
                record.content_sha256.encode("ascii"),
                b"\n",
            )
        )
    return b"".join(chunks)


def _parse_ls_tree(raw: bytes) -> list[GitTreeEntry]:
    entries: list[GitTreeEntry] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            meta, path_bytes = item.split(b"\t", 1)
            mode, object_type, object_id = meta.decode("ascii").split(" ")
        except ValueError as exc:
            raise IntegrityError("unexpected git ls-tree output") from exc
        _validate_relative_path_bytes(path_bytes)
        entries.append(GitTreeEntry(mode, object_type, object_id, path_bytes))
    return entries


def _read_git_blobs(git_repo: Path, object_ids: Sequence[str]) -> dict[str, bytes]:
    unique_ids = list(dict.fromkeys(object_ids))
    if not unique_ids:
        return {}
    batch_input = ("\n".join(unique_ids) + "\n").encode("ascii")
    output = _run_git(git_repo, ["cat-file", "--batch"], stdin=batch_input)
    stream = io.BytesIO(output)
    blobs: dict[str, bytes] = {}
    for object_id in unique_ids:
        header = stream.readline().decode("ascii", errors="replace").strip().split()
        if len(header) != 3 or header[0] != object_id or header[1] != "blob":
            raise IntegrityError(f"unexpected git cat-file header for {object_id}")
        try:
            size = int(header[2])
        except ValueError as exc:
            raise IntegrityError(f"invalid git cat-file size for {object_id}") from exc
        data = stream.read(size)
        if len(data) != size:
            raise IntegrityError(f"short git cat-file payload for {object_id}")
        if stream.read(1) != b"\n":
            raise IntegrityError(f"missing git cat-file terminator for {object_id}")
        blobs[object_id] = data
    return blobs


def _is_lfs_pointer(data: bytes) -> bool:
    return data.startswith(LFS_POINTER_PREFIX) and b"\noid sha256:" in data and b"\nsize " in data


def git_source_scan(git_repo: Path, commitish: str) -> SourceScan:
    commit = resolve_commit(git_repo, commitish)
    raw = _run_git(git_repo, ["ls-tree", "-r", "-t", "-z", "--full-tree", commit])
    entries = _parse_ls_tree(raw)
    directories = 0
    symlinks = 0
    submodules = 0
    special_entries = 0
    nested_git_directories = 0
    nested_git_files = 0
    regular_entries: list[GitTreeEntry] = []
    seen_paths: set[bytes] = set()

    for entry in entries:
        if entry.path_bytes in seen_paths:
            raise IntegrityError(f"duplicate source path: {entry.path}")
        seen_paths.add(entry.path_bytes)
        has_git_component = _path_has_git_component(entry.path_bytes)
        if entry.object_type == "tree":
            directories += 1
            if has_git_component:
                nested_git_directories += 1
        elif entry.object_type == "blob" and entry.mode in REGULAR_GIT_MODES:
            regular_entries.append(entry)
            if has_git_component:
                nested_git_files += 1
        elif entry.object_type == "blob" and entry.mode == SYMLINK_GIT_MODE:
            symlinks += 1
            if has_git_component:
                nested_git_files += 1
        elif entry.object_type == "commit" or entry.mode == SUBMODULE_GIT_MODE:
            submodules += 1
        else:
            special_entries += 1

    blob_map = _read_git_blobs(git_repo, [entry.object_id for entry in regular_entries])
    records = tuple(
        FileRecord(entry.path_bytes, blob_map[entry.object_id], entry.mode, entry.object_id)
        for entry in regular_entries
    )
    return SourceScan(
        algorithm=GIT_SOURCE_ALGORITHM,
        records=records,
        directories=directories,
        zero_byte_files=sum(1 for record in records if record.byte_count == 0),
        symlinks=symlinks,
        submodules=submodules,
        special_entries=special_entries,
        nested_git_directories=nested_git_directories,
        nested_git_files=nested_git_files,
        lfs_pointers=sum(1 for record in records if _is_lfs_pointer(record.data)),
    )


def _validate_name(name: str) -> None:
    if not name or name in {".", ".."}:
        raise IntegrityError(f"unsafe filesystem name: {name!r}")
    if "/" in name or "\\" in name or "\x00" in name or "\t" in name or "\r" in name or "\n" in name:
        raise IntegrityError(f"filesystem name is not portable: {name!r}")
    try:
        name.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise IntegrityError(f"filesystem name is not valid UTF-8: {name!r}") from exc


def _has_reparse_point(entry: os.DirEntry[str]) -> bool:
    try:
        attributes = getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0)
    except OSError as exc:
        raise IntegrityError(f"cannot stat source entry: {entry.path}") from exc
    return bool(attributes & FILE_ATTRIBUTE_REPARSE_POINT)


def materialized_source_scan(source_root: Path) -> SourceScan:
    root = source_root.resolve()
    if not root.is_dir():
        raise IntegrityError(f"materialized source root is not a directory: {source_root}")

    directories = 0
    symlinks = 0
    reparse_points = 0
    special_entries = 0
    nested_git_directories = 0
    nested_git_files = 0
    records: list[FileRecord] = []
    seen_paths: set[bytes] = set()

    def visit(directory: Path, parts: tuple[str, ...]) -> None:
        nonlocal directories, symlinks, reparse_points, special_entries
        nonlocal nested_git_directories, nested_git_files
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name.encode("utf-8"))
        except OSError as exc:
            raise IntegrityError(f"cannot scan source directory: {directory}") from exc
        for entry in entries:
            _validate_name(entry.name)
            child_parts = (*parts, entry.name)
            path_text = "/".join(child_parts)
            path_bytes = path_text.encode("utf-8")
            _validate_relative_path_bytes(path_bytes)
            if _has_reparse_point(entry):
                reparse_points += 1
                continue
            if entry.is_symlink():
                symlinks += 1
                continue
            if entry.is_dir(follow_symlinks=False):
                directories += 1
                if entry.name == ".git":
                    nested_git_directories += 1
                    continue
                visit(Path(entry.path), child_parts)
            elif entry.is_file(follow_symlinks=False):
                if path_bytes in seen_paths:
                    raise IntegrityError(f"duplicate materialized path: {path_text}")
                seen_paths.add(path_bytes)
                if entry.name == ".git":
                    nested_git_files += 1
                try:
                    data = Path(entry.path).read_bytes()
                except OSError as exc:
                    raise IntegrityError(f"cannot read source file: {entry.path}") from exc
                records.append(FileRecord(path_bytes, data))
            else:
                special_entries += 1

    visit(root, ())
    record_tuple = tuple(records)
    return SourceScan(
        algorithm=MATERIALIZED_SOURCE_ALGORITHM,
        records=record_tuple,
        directories=directories,
        zero_byte_files=sum(1 for record in record_tuple if record.byte_count == 0),
        symlinks=symlinks,
        reparse_points=reparse_points,
        special_entries=special_entries,
        nested_git_directories=nested_git_directories,
        nested_git_files=nested_git_files,
        lfs_pointers=sum(1 for record in record_tuple if _is_lfs_pointer(record.data)),
    )


def _records_by_path(scan: SourceScan) -> dict[bytes, FileRecord]:
    records: dict[bytes, FileRecord] = {}
    for record in scan.records:
        if record.path_bytes in records:
            raise IntegrityError(f"duplicate record path: {record.path}")
        records[record.path_bytes] = record
    return records


def compare_scans(git_scan: SourceScan, materialized_scan: SourceScan) -> dict[str, object]:
    git_records = _records_by_path(git_scan)
    materialized_records = _records_by_path(materialized_scan)
    git_paths = set(git_records)
    materialized_paths = set(materialized_records)
    missing = sorted(git_paths - materialized_paths)
    extra = sorted(materialized_paths - git_paths)
    different = sorted(
        path
        for path in git_paths & materialized_paths
        if git_records[path].byte_count != materialized_records[path].byte_count
        or git_records[path].content_sha256 != materialized_records[path].content_sha256
    )
    directory_count_match = git_scan.directories == materialized_scan.directories
    special_counts_clear = (
        git_scan.symlinks == 0
        and git_scan.submodules == 0
        and git_scan.special_entries == 0
        and materialized_scan.symlinks == 0
        and materialized_scan.reparse_points == 0
        and materialized_scan.special_entries == 0
    )
    nested_git_clear = (
        git_scan.nested_git_directories == 0
        and git_scan.nested_git_files == 0
        and materialized_scan.nested_git_directories == 0
        and materialized_scan.nested_git_files == 0
    )
    lfs_pointers_clear = git_scan.lfs_pointers == 0 and materialized_scan.lfs_pointers == 0
    matched = (
        not missing
        and not extra
        and not different
        and directory_count_match
        and special_counts_clear
        and nested_git_clear
        and lfs_pointers_clear
    )
    return {
        "status": "match" if matched else "mismatch",
        "sha256_match": git_scan.sha256 == materialized_scan.sha256,
        "files_match": git_scan.files == materialized_scan.files,
        "bytes_match": git_scan.bytes == materialized_scan.bytes,
        "directories_match": directory_count_match,
        "zero_byte_files_match": git_scan.zero_byte_files == materialized_scan.zero_byte_files,
        "special_counts_clear": special_counts_clear,
        "nested_git_clear": nested_git_clear,
        "lfs_pointers_clear": lfs_pointers_clear,
        "missing_materialized_count": len(missing),
        "extra_materialized_count": len(extra),
        "different_file_count": len(different),
        "missing_materialized": [path.decode("utf-8") for path in missing[:50]],
        "extra_materialized": [path.decode("utf-8") for path in extra[:50]],
        "different_files": [path.decode("utf-8") for path in different[:50]],
    }


def manifest_rows(
    git_scan: SourceScan,
    materialized_scan: SourceScan,
    *,
    repository: str,
    tag: str,
    commit: str,
) -> list[dict[str, str]]:
    git_records = _records_by_path(git_scan)
    materialized_records = _records_by_path(materialized_scan)
    rows: list[dict[str, str]] = []
    for path in sorted(set(git_records) | set(materialized_records)):
        git_record = git_records.get(path)
        materialized_record = materialized_records.get(path)
        if git_record and materialized_record:
            if (
                git_record.byte_count == materialized_record.byte_count
                and git_record.content_sha256 == materialized_record.content_sha256
            ):
                status = "exact_match"
            else:
                status = "content_mismatch"
        elif git_record:
            status = "missing_materialized"
        else:
            status = "extra_materialized"
        rows.append(
            {
                "source_repository": repository,
                "source_tag": tag,
                "source_commit": commit,
                "entry_type": "regular_file",
                "relative_path": path.decode("utf-8"),
                "git_mode": git_record.git_mode if git_record and git_record.git_mode else "not_applicable",
                "git_object_id": git_record.git_object_id if git_record and git_record.git_object_id else "not_applicable",
                "git_bytes": str(git_record.byte_count) if git_record else "not_applicable",
                "git_sha256": git_record.content_sha256 if git_record else "not_applicable",
                "materialized_bytes": str(materialized_record.byte_count) if materialized_record else "not_applicable",
                "materialized_sha256": materialized_record.content_sha256 if materialized_record else "not_applicable",
                "verification_status": status,
            }
        )
    return rows


def write_manifest(path: Path, rows: Sequence[dict[str, str]]) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    data = path.read_bytes()
    return {
        "path": path.as_posix(),
        "rows": len(rows),
        "columns": len(MANIFEST_COLUMNS),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def compute(
    *,
    git_repo: Path | None,
    commitish: str | None,
    source_root: Path | None,
    mode: str,
    repository: str = "",
    tag: str = "",
    manifest_output: Path | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {}
    git_scan: SourceScan | None = None
    materialized_scan: SourceScan | None = None
    resolved_commit = "not_applicable"
    if mode in {"all", "git", "compare", "manifest"}:
        if git_repo is None or commitish is None:
            raise IntegrityError("--git-repo and --commit are required for this mode")
        resolved_commit = resolve_commit(git_repo, commitish)
        git_scan = git_source_scan(git_repo, resolved_commit)
        result["git"] = git_scan.as_result()
        result["commit"] = resolved_commit
    if mode in {"all", "materialized", "compare", "manifest"}:
        if source_root is None:
            raise IntegrityError("--source-root is required for this mode")
        materialized_scan = materialized_source_scan(source_root)
        result["materialized"] = materialized_scan.as_result()
    if mode in {"all", "compare", "manifest"}:
        if git_scan is None or materialized_scan is None:
            raise IntegrityError("git and materialized scans are required for comparison")
        result["comparison"] = compare_scans(git_scan, materialized_scan)
    if mode in {"all", "manifest"} and manifest_output is not None:
        if git_scan is None or materialized_scan is None:
            raise IntegrityError("git and materialized scans are required for manifest output")
        rows = manifest_rows(git_scan, materialized_scan, repository=repository, tag=tag, commit=resolved_commit)
        result["manifest"] = write_manifest(manifest_output, rows)
    if repository:
        result["repository"] = repository
    if tag:
        result["tag"] = tag
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--git-repo", type=Path)
    parser.add_argument("--commit")
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--repository", default="")
    parser.add_argument("--tag", default="")
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--mode", choices=("all", "git", "materialized", "compare", "manifest"), default="all")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def _print_text(result: dict[str, object]) -> None:
    for key in ("git", "materialized"):
        scan = result.get(key)
        if isinstance(scan, dict):
            print(
                f"{key}: files={scan['files']} dirs={scan['directories']} "
                f"bytes={scan['bytes']} sha256={scan['sha256']}"
            )
    comparison = result.get("comparison")
    if isinstance(comparison, dict):
        print(f"comparison: status={comparison['status']} sha256_match={comparison['sha256_match']}")
    manifest = result.get("manifest")
    if isinstance(manifest, dict):
        print(
            f"manifest: rows={manifest['rows']} columns={manifest['columns']} "
            f"bytes={manifest['bytes']} sha256={manifest['sha256']}"
        )


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = compute(
            git_repo=args.git_repo.resolve() if args.git_repo else None,
            commitish=args.commit,
            source_root=args.source_root.resolve() if args.source_root else None,
            mode=args.mode,
            repository=args.repository,
            tag=args.tag,
            manifest_output=args.manifest_output,
        )
    except IntegrityError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    if args.format == "json":
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        _print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
