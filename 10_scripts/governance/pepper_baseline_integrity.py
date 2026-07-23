#!/usr/bin/env python3
"""Canonical Git-blob integrity utility for Pepper baseline governance."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ALGORITHM = "agent-platform-git-tree-sha256-v2"
BASELINE_RECORD = "AGENT_PLATFORM_UPSTREAM_BASELINE.json"
IMPORT_MANIFEST = "AGENT_PLATFORM_IMPORT_MANIFEST.tsv"
PAYLOAD_CLASSIFICATIONS = frozenset(
    {
        "included_byte_exact",
        "included_canonical_text_lf",
        "transformed_by_canonical_compliance_rule",
    }
)


class IntegrityError(RuntimeError):
    """Raised when canonical integrity cannot be computed safely."""


@dataclass(frozen=True, slots=True)
class BlobRecord:
    """One committed Git blob selected for aggregate hashing."""

    path_bytes: bytes
    blob_bytes: bytes

    @property
    def byte_count(self) -> int:
        return len(self.blob_bytes)

    @property
    def content_sha256(self) -> str:
        return hashlib.sha256(self.blob_bytes).hexdigest()


def _run_git(repo_root: Path, args: Sequence[str], *, stdin: bytes | None = None) -> bytes:
    command = ["git", "-C", str(repo_root), *args]
    try:
        return subprocess.check_output(command, input=stdin, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace").strip()
        detail = f": {stderr}" if stderr else ""
        raise IntegrityError(f"git command failed: {' '.join(command)}{detail}") from exc


def git_head(repo_root: Path) -> str:
    return _run_git(repo_root, ["rev-parse", "HEAD"]).decode("ascii").strip()


def _normalize_product_root(product_root: str) -> str:
    root = product_root.replace("\\", "/").strip("/")
    if not root or root.startswith("../") or "/../" in f"/{root}/":
        raise IntegrityError(f"unsafe product root: {product_root!r}")
    return root


def _validate_git_path_bytes(path_bytes: bytes) -> None:
    try:
        text = path_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntegrityError("Git path is not valid UTF-8") from exc
    if "\x00" in text or text.startswith("/") or "//" in text:
        raise IntegrityError(f"unsafe Git path: {text!r}")
    parts = text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise IntegrityError(f"unsafe Git path: {text!r}")


def _parse_ls_tree(raw: bytes) -> list[tuple[bytes, str]]:
    entries: list[tuple[bytes, str]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            meta, path_bytes = item.split(b"\t", 1)
            _mode, object_type, object_id = meta.decode("ascii").split(" ")
        except ValueError as exc:
            raise IntegrityError("unexpected git ls-tree output") from exc
        if object_type != "blob":
            continue
        _validate_git_path_bytes(path_bytes)
        entries.append((path_bytes, object_id))
    return entries


def _strip_product_prefix(path_bytes: bytes, product_root: str) -> bytes:
    prefix = product_root.encode("utf-8") + b"/"
    if not path_bytes.startswith(prefix):
        escaped = path_bytes.decode("utf-8", errors="replace")
        raise IntegrityError(f"Git path escapes product root: {escaped}")
    relative = path_bytes[len(prefix) :]
    _validate_git_path_bytes(relative)
    return relative


def _read_blob_bytes(repo_root: Path, object_ids: Sequence[str]) -> dict[str, bytes]:
    if not object_ids:
        return {}
    batch_input = ("\n".join(object_ids) + "\n").encode("ascii")
    output = _run_git(repo_root, ["cat-file", "--batch"], stdin=batch_input)
    stream = io.BytesIO(output)
    blobs: dict[str, bytes] = {}
    for object_id in object_ids:
        header = stream.readline().decode("ascii", errors="replace").strip().split()
        if len(header) != 3 or header[0] != object_id or header[1] != "blob":
            raise IntegrityError(f"unexpected git cat-file header for {object_id}")
        size = int(header[2])
        data = stream.read(size)
        if len(data) != size:
            raise IntegrityError(f"short git cat-file payload for {object_id}")
        if stream.read(1) != b"\n":
            raise IntegrityError(f"missing git cat-file terminator for {object_id}")
        blobs[object_id] = data
    return blobs


def _tree_blobs(repo_root: Path, product_root: str) -> dict[bytes, bytes]:
    raw = _run_git(repo_root, ["ls-tree", "-r", "-z", "HEAD", "--", product_root])
    entries = _parse_ls_tree(raw)
    blob_map = _read_blob_bytes(repo_root, [object_id for _path, object_id in entries])
    tree: dict[bytes, bytes] = {}
    for repo_path, object_id in entries:
        relative = _strip_product_prefix(repo_path, product_root)
        if relative in tree:
            raise IntegrityError(f"duplicate product-relative path: {relative.decode('utf-8')}")
        tree[relative] = blob_map[object_id]
    return tree


def record_stream(records: Iterable[BlobRecord]) -> bytes:
    """Return the exact canonical v2 record stream."""

    chunks: list[bytes] = []
    for record in sorted(records, key=lambda item: item.path_bytes):
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


def digest_records(records: Iterable[BlobRecord]) -> dict[str, object]:
    selected = list(records)
    stream = record_stream(selected)
    return {
        "algorithm": ALGORITHM,
        "files": len(selected),
        "bytes": sum(record.byte_count for record in selected),
        "sha256": hashlib.sha256(stream).hexdigest(),
    }


def candidate_digest(
    repo_root: Path,
    product_root: str,
    *,
    exclude: Iterable[str] = (BASELINE_RECORD,),
) -> dict[str, object]:
    root = _normalize_product_root(product_root)
    excluded = {path.replace("\\", "/").encode("utf-8") for path in exclude}
    tree = _tree_blobs(repo_root, root)
    records = [
        BlobRecord(path, data)
        for path, data in tree.items()
        if path not in excluded
    ]
    result = digest_records(records)
    result.update(
        {
            "mode": "candidate",
            "product_root": root,
            "excluded_paths": sorted(path.decode("utf-8") for path in excluded),
        }
    )
    return result


def payload_digest(
    repo_root: Path,
    product_root: str,
    *,
    manifest_path: str = IMPORT_MANIFEST,
) -> dict[str, object]:
    root = _normalize_product_root(product_root)
    tree = _tree_blobs(repo_root, root)
    manifest_key = manifest_path.replace("\\", "/").encode("utf-8")
    try:
        manifest_bytes = tree[manifest_key]
    except KeyError as exc:
        raise IntegrityError(f"missing import manifest: {manifest_path}") from exc
    try:
        manifest_text = manifest_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntegrityError("import manifest is not valid UTF-8") from exc
    reader = csv.DictReader(manifest_text.splitlines(), delimiter="\t")
    required = {"destination_path", "classification"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise IntegrityError("import manifest lacks required columns")
    seen: set[bytes] = set()
    records: list[BlobRecord] = []
    for line_number, row in enumerate(reader, start=2):
        if row["classification"] not in PAYLOAD_CLASSIFICATIONS:
            continue
        destination = row["destination_path"].replace("\\", "/")
        if not destination or destination == "not_applicable":
            raise IntegrityError(f"invalid payload destination on line {line_number}")
        path_bytes = destination.encode("utf-8")
        _validate_git_path_bytes(path_bytes)
        if path_bytes in seen:
            raise IntegrityError(f"duplicate payload destination: {destination}")
        seen.add(path_bytes)
        try:
            blob = tree[path_bytes]
        except KeyError as exc:
            raise IntegrityError(f"payload destination missing: {destination}") from exc
        records.append(BlobRecord(path_bytes, blob))
    result = digest_records(records)
    result.update(
        {
            "mode": "payload",
            "product_root": root,
            "manifest_path": manifest_path,
            "included_classifications": sorted(PAYLOAD_CLASSIFICATIONS),
        }
    )
    return result


def baseline_record_digest(repo_root: Path, product_root: str) -> dict[str, object]:
    root = _normalize_product_root(product_root)
    tree = _tree_blobs(repo_root, root)
    path_bytes = BASELINE_RECORD.encode("utf-8")
    try:
        data = tree[path_bytes]
    except KeyError as exc:
        raise IntegrityError(f"baseline record missing: {BASELINE_RECORD}") from exc
    return {
        "algorithm": "sha256-git-blob-v1",
        "mode": "baseline_record",
        "product_root": root,
        "path": BASELINE_RECORD,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def compute_all(repo_root: Path, product_root: str) -> dict[str, object]:
    return {
        "head": git_head(repo_root),
        "candidate": candidate_digest(repo_root, product_root),
        "payload": payload_digest(repo_root, product_root),
        "baseline_record": baseline_record_digest(repo_root, product_root),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--product-root", default="2_products/pepper-agent")
    parser.add_argument(
        "--mode",
        choices=("all", "candidate", "payload", "baseline-record"),
        default="all",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        if args.mode == "all":
            result = compute_all(repo_root, args.product_root)
        elif args.mode == "candidate":
            result = candidate_digest(repo_root, args.product_root)
        elif args.mode == "payload":
            result = payload_digest(repo_root, args.product_root)
        else:
            result = baseline_record_digest(repo_root, args.product_root)
    except IntegrityError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    if args.format == "json":
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    if args.mode == "all":
        print(f"head: {result['head']}")
        for key in ("candidate", "payload", "baseline_record"):
            value = result[key]
            print(
                f"{key}: files={value.get('files', 'not_applicable')} "
                f"bytes={value['bytes']} sha256={value['sha256']}"
            )
    else:
        print(
            f"{args.mode}: files={result.get('files', 'not_applicable')} "
            f"bytes={result['bytes']} sha256={result['sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
