#!/usr/bin/env python3
"""Deterministic, evidence-preserving Graphify refresh orchestration."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from collections import Counter
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable


PIPELINE_VERSION = "1.0.0"
SUPPORTED_GRAPHIFY_VERSION = "0.9.5"
DEFAULT_BATCH_SIZE = 500
DEFAULT_BATCH_TIMEOUT = 600
DEFAULT_PIPELINE_TIMEOUT = 2400

DERIVED_NODE_FIELDS = {
    "community",
    "community_name",
    "norm_label",
    "display_position",
    "extracted_at",
    "extraction_timestamp",
    "build_timestamp",
    "x",
    "y",
}
DERIVED_RELATIONSHIP_FIELDS = {
    "community",
    "display_position",
    "extracted_at",
    "extraction_timestamp",
    "build_timestamp",
    "x",
    "y",
}

BASELINE_PREFIXES = (
    "0_architecture/",
    "3_platform/_governed_skeleton/",
)
HERMES_PREFIX = "2_products/hermes-agent/"
REPRESENTATIVE_SELECTORS = {
    "hermes_cli_web_server": ("2_products/hermes-agent/hermes_cli/web_server.py",),
    "gateway_api_server": ("2_products/hermes-agent/gateway/platforms/api_server.py",),
    "kanban_plugin_api": (
        "2_products/hermes-agent/plugins/kanban/dashboard/plugin_api.py",
    ),
    "apps_shared": ("2_products/hermes-agent/apps/shared/",),
    "web_app": ("2_products/hermes-agent/web/src/App.tsx",),
    "runtime_overview": (
        "2_products/hermes-agent/web/src/agent-platform/runtime-overview/",
    ),
    "projects_tickets": (
        "2_products/hermes-agent/web/src/agent-platform/projects-tickets/",
    ),
    "approval_inbox": (
        "2_products/hermes-agent/web/src/agent-platform/approval-inbox/",
    ),
    "execution_inspector": (
        "2_products/hermes-agent/web/src/agent-platform/execution-inspector/",
    ),
    "tests": ("2_products/hermes-agent/tests/",),
}


class PipelineError(RuntimeError):
    """Raised when a governed pipeline invariant fails."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def hash_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def write_compact_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_path(path: str | Path) -> str:
    value = str(path).replace("\\", "/")
    return value[2:] if value.startswith("./") else value


def is_absolute_source(path: str) -> bool:
    return bool(path) and (
        Path(path).is_absolute()
        or PureWindowsPath(path).is_absolute()
        or path.startswith(("/", "\\"))
    )


def canonical_source_path(path: str | Path) -> str | None:
    raw = str(path)
    if not raw or is_absolute_source(raw):
        return None
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    if normalized.startswith("./") or any(part in {"", ".", ".."} for part in parts):
        return None
    return normalized


def ensure_graphify_version() -> str:
    version = importlib.metadata.version("graphifyy")
    if version != SUPPORTED_GRAPHIFY_VERSION:
        raise PipelineError(
            f"Graphify {SUPPORTED_GRAPHIFY_VERSION} is required; installed version is {version}"
        )
    return version


def run_git(
    repo_root: Path, *args: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    command = ["git", "-c", "core.longpaths=true", *args]
    return subprocess.run(
        command,
        cwd=repo_root,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git_head(repo_root: Path) -> str:
    result = run_git(repo_root, "rev-parse", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else "UNBORN"


def git_tracked_paths(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-c", "core.longpaths=true", "ls-files", "-z"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    return sorted(
        normalize_path(item.decode("utf-8", errors="surrogateescape"))
        for item in result.stdout.split(b"\0")
        if item
    )


def git_index_sha256(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "-c", "core.longpaths=true", "ls-files", "-s", "-z"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    return hashlib.sha256(result.stdout).hexdigest()


def direct_product_children(repo_root: Path) -> list[str]:
    root = repo_root / "2_products"
    if not root.exists():
        return []
    return sorted(item.name for item in root.iterdir() if item.is_dir())


def authorized_scope(path: str, scope: str) -> bool:
    if path == "README.md":
        return True
    if path.startswith("0_architecture/"):
        return path.lower().endswith(".md")
    if path.startswith("3_platform/_governed_skeleton/"):
        return path.lower().endswith(".py")
    return scope == "full" and path.startswith(HERMES_PREFIX)


def inclusion_reason(path: str) -> str:
    if path == "README.md":
        return "root_readme"
    if path.startswith("0_architecture/"):
        return "architecture_markdown"
    if path.startswith("3_platform/_governed_skeleton/"):
        return "governed_skeleton_python"
    if path.startswith(HERMES_PREFIX):
        return "hermes_product"
    raise PipelineError(f"No authorized inclusion reason for {path}")


def build_inventory(repo_root: Path, scope: str, batch_size: int) -> dict[str, Any]:
    ensure_graphify_version()
    from graphify.detect import (
        _is_ignored,
        _is_sensitive,
        _load_graphifyignore,
        classify_file,
    )
    from graphify.extract import _get_extractor

    root = repo_root.resolve()
    patterns = _load_graphifyignore(root)
    ignore_cache: dict[Path, bool] = {}
    accepted: list[dict[str, Any]] = []
    ignored: list[dict[str, str]] = []
    sensitive: list[dict[str, str]] = []
    unsupported: list[dict[str, str]] = []

    for relative in git_tracked_paths(root):
        absolute = root / relative
        if not absolute.is_file():
            ignored.append(
                {"path": relative, "reason": "tracked_path_missing_or_not_file"}
            )
            continue
        resolved = absolute.resolve()
        if absolute.is_symlink() or not resolved.is_relative_to(root):
            ignored.append(
                {
                    "path": relative,
                    "reason": "tracked_symlink_or_root_escape_denied",
                }
            )
            continue
        if not authorized_scope(relative, scope):
            ignored.append({"path": relative, "reason": "outside_authorized_scope"})
            continue
        if _is_ignored(absolute, root, patterns, _cache=ignore_cache):
            ignored.append({"path": relative, "reason": "installed_ignore_parser"})
            continue
        if _is_sensitive(absolute):
            sensitive.append({"path": relative, "reason": "installed_sensitive_filter"})
            continue
        file_type = classify_file(absolute)
        extractor = _get_extractor(absolute)
        if file_type is None or extractor is None:
            unsupported.append(
                {
                    "path": relative,
                    "reason": "no_installed_ast_extractor",
                    "detected_file_type": file_type.value
                    if file_type
                    else "unsupported",
                }
            )
            continue
        accepted.append(
            {
                "path": relative,
                "sha256": sha256_file(absolute),
                "bytes": absolute.stat().st_size,
                "detected_file_type": file_type.value,
                "extractor": f"{extractor.__module__}.{extractor.__name__}",
                "inclusion_reason": inclusion_reason(relative),
            }
        )

    accepted.sort(key=lambda item: item["path"])
    ignored.sort(key=lambda item: item["path"])
    sensitive.sort(key=lambda item: item["path"])
    unsupported.sort(key=lambda item: item["path"])

    batches: list[dict[str, Any]] = []
    for offset in range(0, len(accepted), batch_size):
        batch_number = offset // batch_size + 1
        batch_files = accepted[offset : offset + batch_size]
        batch_id = f"batch-{batch_number:04d}"
        for item in batch_files:
            item["batch_id"] = batch_id
        paths = [item["path"] for item in batch_files]
        batches.append(
            {
                "batch_id": batch_id,
                "paths": paths,
                "input_list_sha256": hash_value(paths),
                "file_count": len(paths),
            }
        )

    accepted_hash = hash_value(accepted)
    ignored_hash = hash_value(ignored)
    sensitive_hash = hash_value(sensitive)
    unsupported_hash = hash_value(unsupported)
    batch_hash = hash_value(batches)
    return {
        "schema_version": 1,
        "scope": scope,
        "git_commit": git_head(root),
        "git_index_sha256": git_index_sha256(root),
        "graphify_version": SUPPORTED_GRAPHIFY_VERSION,
        "pipeline_version": PIPELINE_VERSION,
        "batch_size": batch_size,
        "direct_product_children": direct_product_children(root),
        "accepted": accepted,
        "ignored": ignored,
        "sensitive": sensitive,
        "unsupported": unsupported,
        "batches": batches,
        "accepted_manifest_sha256": accepted_hash,
        "ignored_manifest_sha256": ignored_hash,
        "sensitive_manifest_sha256": sensitive_hash,
        "unsupported_manifest_sha256": unsupported_hash,
        "batch_definition_sha256": batch_hash,
        "counts": {
            "tracked": len(accepted) + len(ignored) + len(sensitive) + len(unsupported),
            "accepted": len(accepted),
            "ignored": len(ignored),
            "sensitive": len(sensitive),
            "unsupported": len(unsupported),
            "batches": len(batches),
        },
    }


def write_inventory(evidence_dir: Path, inventory: dict[str, Any]) -> None:
    write_json(evidence_dir / "authorized-input-manifest.json", inventory["accepted"])
    write_json(evidence_dir / "ignored-file-manifest.json", inventory["ignored"])
    write_json(evidence_dir / "sensitive-skip-manifest.json", inventory["sensitive"])
    write_json(
        evidence_dir / "unsupported-file-manifest.json", inventory["unsupported"]
    )
    write_json(evidence_dir / "batch-definitions.json", inventory["batches"])
    write_json(evidence_dir / "inventory-summary.json", inventory)


INVENTORY_BINDING_FIELDS = (
    "scope",
    "git_commit",
    "git_index_sha256",
    "graphify_version",
    "pipeline_version",
    "batch_size",
    "direct_product_children",
    "accepted",
    "ignored",
    "sensitive",
    "unsupported",
    "batches",
    "accepted_manifest_sha256",
    "ignored_manifest_sha256",
    "sensitive_manifest_sha256",
    "unsupported_manifest_sha256",
    "batch_definition_sha256",
    "counts",
)


def require_matching_inventory(
    declared: dict[str, Any], current: dict[str, Any], label: str
) -> None:
    changed = [
        field
        for field in INVENTORY_BINDING_FIELDS
        if declared.get(field) != current.get(field)
    ]
    if changed:
        raise PipelineError(
            f"{label} does not match the current repository inventory: {', '.join(changed)}"
        )


def validate_zero_node_sources(
    repo_root: Path, paths: list[str]
) -> list[dict[str, Any]]:
    ensure_graphify_version()
    from graphify.extract import _get_extractor, _safe_extract_with_xaml_root

    records = []
    for relative in paths:
        path = repo_root / relative
        if path.suffix.lower() != ".json":
            raise PipelineError(
                f"Accepted non-JSON source emitted no nodes and is not eligible: {relative}"
            )
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise PipelineError(
                f"Accepted zero-node JSON is not valid data-only JSON: {relative}: {error}"
            ) from error
        extractor = _get_extractor(path)
        if extractor is None:
            raise PipelineError(
                f"Accepted zero-node JSON has no maintained extractor: {relative}"
            )
        audit = _safe_extract_with_xaml_root(extractor, path, repo_root)
        relationships = audit.get("edges", audit.get("links", []))
        if audit.get("error"):
            raise PipelineError(
                f"Fresh zero-node JSON extraction failed: {relative}: {audit['error']}"
            )
        if audit.get("nodes") or relationships or audit.get("hyperedges"):
            raise PipelineError(
                f"Fresh extraction proves JSON is structural, not zero-node data: {relative}"
            )
        records.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
                "json_root_type": type(value).__name__,
                "fresh_extractor": f"{extractor.__module__}.{extractor.__name__}",
                "fresh_nodes": 0,
                "fresh_relationships": 0,
                "fresh_hyperedges": 0,
            }
        )
    return records


def validate_official_manifest(
    output_dir: Path, inventory: dict[str, Any]
) -> dict[str, Any]:
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.is_file():
        raise PipelineError("Official Graphify manifest.json is missing")
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise PipelineError("Official Graphify manifest.json must be an object")
    actual = set(manifest)
    noncanonical = sorted(
        path for path in actual if canonical_source_path(path) != path
    )
    if noncanonical:
        raise PipelineError(
            f"Official manifest contains noncanonical source paths: {noncanonical[:20]}"
        )
    expected = {item["path"] for item in inventory["accepted"]}
    if actual != expected:
        raise PipelineError(
            "Official manifest source coverage does not match the accepted inventory"
        )
    return {
        "source_count": len(actual),
        "source_path_sha256": hash_value(sorted(actual)),
    }


def directory_inventory(root: Path) -> dict[str, Any]:
    if not root.exists():
        return {
            "files": [],
            "file_count": 0,
            "total_bytes": 0,
            "sha256": hash_value([]),
        }
    records = []
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()), key=lambda p: p.as_posix()
    ):
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return {
        "files": records,
        "file_count": len(records),
        "total_bytes": sum(item["bytes"] for item in records),
        "sha256": hash_value(records),
    }


def selected_file_inventory(root: Path, names: Iterable[str]) -> dict[str, Any]:
    records = []
    for name in sorted(names):
        path = root / name
        if not path.is_file():
            raise PipelineError(f"Required snapshot file is missing: {name}")
        records.append(
            {"path": name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        )
    return {"files": records, "sha256": hash_value(records)}


def ensure_external(repo_root: Path, target: Path, label: str) -> Path:
    resolved = target.resolve()
    if resolved == repo_root.resolve() or resolved.is_relative_to(repo_root.resolve()):
        raise PipelineError(f"{label} must be outside the repository: {resolved}")
    return resolved


def ensure_disjoint_paths(*paths: Path) -> None:
    resolved = [path.resolve() for path in paths]
    for index, left in enumerate(resolved):
        for right in resolved[index + 1 :]:
            if (
                left == right
                or left.is_relative_to(right)
                or right.is_relative_to(left)
            ):
                raise PipelineError(
                    f"Pipeline paths must be disjoint: {left} and {right}"
                )


def sanitized_environment(graphify_out: Path, max_workers: int) -> dict[str, str]:
    env = os.environ.copy()
    for name in list(env):
        upper = name.upper()
        if any(
            marker in upper for marker in ("API_KEY", "TOKEN", "SECRET", "CREDENTIAL")
        ):
            env.pop(name, None)
    env.update(
        {
            "GRAPHIFY_OUT": str(graphify_out),
            "GRAPHIFY_MAX_WORKERS": str(max_workers),
            "GRAPHIFY_NO_TIPS": "1",
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
            "TZ": "UTC",
        }
    )
    return env


def terminate_process_tree(process: subprocess.Popen[Any]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            check=False,
        )
    else:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def run_owned_process(
    command: list[str],
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: int,
    stdout_path: Path,
    stderr_path: Path,
    progress_label: str,
) -> dict[str, Any]:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    started_wall = time.time()
    started_perf = time.perf_counter()
    peak_memory = 0
    max_cpu_seconds = 0.0
    next_progress = started_perf + 30
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    with (
        stdout_path.open("wb") as stdout_handle,
        stderr_path.open("wb") as stderr_handle,
    ):
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=creationflags,
        )
        timed_out = False
        try:
            import psutil

            monitored = psutil.Process(process.pid)
        except Exception:
            monitored = None
        while process.poll() is None:
            elapsed = time.perf_counter() - started_perf
            if elapsed >= timeout_seconds:
                timed_out = True
                terminate_process_tree(process)
                break
            if monitored is not None:
                try:
                    family = [monitored, *monitored.children(recursive=True)]
                    peak_memory = max(
                        peak_memory, sum(item.memory_info().rss for item in family)
                    )
                    max_cpu_seconds = max(
                        max_cpu_seconds,
                        sum(
                            item.cpu_times().user + item.cpu_times().system
                            for item in family
                        ),
                    )
                except Exception:
                    pass
            if time.perf_counter() >= next_progress:
                print(
                    f"[{progress_label}] elapsed={elapsed:.1f}s "
                    f"stdout_bytes={stdout_path.stat().st_size if stdout_path.exists() else 0} "
                    f"stderr_bytes={stderr_path.stat().st_size if stderr_path.exists() else 0}",
                    flush=True,
                )
                next_progress += 30
            time.sleep(0.25)
        return_code = process.wait()
    ended_perf = time.perf_counter()
    record = {
        "command": command,
        "started_at_epoch": started_wall,
        "ended_at_epoch": time.time(),
        "duration_seconds": ended_perf - started_perf,
        "timeout_seconds": timeout_seconds,
        "timed_out": timed_out,
        "exit_code": 124 if timed_out else return_code,
        "peak_memory_bytes": peak_memory or None,
        "cpu_seconds": max_cpu_seconds or None,
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_sha256": sha256_file(stderr_path),
    }
    if timed_out or return_code != 0:
        raise PipelineError(
            f"{progress_label} failed: exit={record['exit_code']} timeout={timed_out}; "
            f"see {stdout_path} and {stderr_path}"
        )
    return record


def worker_extract(args: argparse.Namespace) -> int:
    ensure_graphify_version()
    import graphify.extract as graphify_extract
    from graphify.extract import (
        _JS_CACHE_BYPASS_SUFFIXES,
        _get_extractor,
        _safe_extract_with_xaml_root,
    )
    from graphify.validate import validate_extraction

    repo_root = Path(args.repo_root).resolve()
    input_data = read_json(Path(args.input_list))
    entries = input_data["files"]
    paths: list[Path] = []
    for entry in entries:
        path = repo_root / entry["path"]
        if not path.is_file() or sha256_file(path) != entry["sha256"]:
            raise PipelineError(
                f"Input changed after manifest creation: {entry['path']}"
            )
        paths.append(path)

    cache_hits = 0
    cache_misses = sum(
        _get_extractor(path) is not None and path.suffix in _JS_CACHE_BYPASS_SUFFIXES
        for path in paths
    )
    original_load_cached = graphify_extract.load_cached

    def tracked_load_cached(
        path: Path, root: Path = Path("."), kind: str = "ast"
    ) -> Any:
        nonlocal cache_hits, cache_misses
        result = original_load_cached(path, root, kind)
        if result is None:
            cache_misses += 1
        else:
            cache_hits += 1
        return result

    started = time.perf_counter()
    graphify_extract.load_cached = tracked_load_cached
    try:
        result = graphify_extract.extract(
            paths, cache_root=repo_root, parallel=True, max_workers=args.max_workers
        )
    finally:
        graphify_extract.load_cached = original_load_cached
    print("official extraction complete; writing immutable raw evidence", flush=True)
    raw_path = Path(args.raw_output)
    write_compact_json(raw_path, result)
    print("raw extraction evidence written", flush=True)

    failures = []
    zero_node_files = []
    if not args.skip_zero_node_audit:
        represented: set[str] = set()
        for node in result.get("nodes", []):
            source = str(node.get("source_file", ""))
            if not source:
                continue
            if is_absolute_source(source):
                try:
                    represented.add(
                        Path(source).resolve().relative_to(repo_root).as_posix()
                    )
                except ValueError:
                    represented.add(normalize_path(source))
            else:
                represented.add(normalize_path(source))
        for entry, path in zip(entries, paths):
            if entry["path"] in represented:
                continue
            zero_node_files.append(entry["path"])
            extractor = _get_extractor(path)
            audit = (
                _safe_extract_with_xaml_root(extractor, path, repo_root)
                if extractor
                else {}
            )
            if audit.get("error"):
                failures.append({"path": entry["path"], "error": str(audit["error"])})
            elif (
                audit.get("nodes")
                or audit.get("edges", audit.get("links", []))
                or audit.get("hyperedges")
            ):
                failures.append(
                    {
                        "path": entry["path"],
                        "error": "fresh extractor emitted graph records after cached zero-node result",
                    }
                )

    validation_errors = [] if args.defer_validation else validate_extraction(result)
    summary = {
        "files": len(paths),
        "nodes": len(result.get("nodes", [])),
        "relationships": len(result.get("edges", result.get("links", []))),
        "hyperedges": len(result.get("hyperedges", [])),
        "duration_seconds": time.perf_counter() - started,
        "raw_sha256": None if args.defer_validation else sha256_file(raw_path),
        "parser_failures": failures,
        "zero_node_files": zero_node_files,
        "official_validation_errors": validation_errors,
        "official_validation_deferred_to_build": args.defer_validation,
        "cache_hits": cache_hits,
        "cache_misses": cache_misses,
    }
    write_json(Path(args.summary_output), summary)
    write_json(Path(args.failure_ledger), failures)
    print(canonical_json(summary), flush=True)
    return 0


def worker_build(args: argparse.Namespace) -> int:
    ensure_graphify_version()
    from graphify.build import build_from_json
    from graphify.detect import save_manifest
    from graphify.export import to_json
    from graphify.validate import validate_extraction

    repo_root = Path(args.repo_root).resolve()
    raw = read_json(Path(args.raw_input))
    official_errors = validate_extraction(raw)
    non_endpoint_errors = [
        error for error in official_errors if "does not match any node id" not in error
    ]
    if non_endpoint_errors:
        raise PipelineError(
            f"Official extraction validation failed: {non_endpoint_errors[:20]}"
        )
    graph = build_from_json(raw, root=repo_root)
    graph_path = Path(args.graph_output)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    if not to_json(
        graph,
        {},
        str(graph_path),
        force=True,
        built_at_commit=git_head(repo_root),
    ):
        raise PipelineError(
            "Official Graphify serialization refused the candidate graph"
        )

    inventory = read_json(Path(args.inventory))
    grouped: dict[str, list[str]] = {
        "code": [],
        "document": [],
        "paper": [],
        "image": [],
        "video": [],
    }
    for entry in inventory["accepted"]:
        grouped.setdefault(entry["detected_file_type"], []).append(
            str(repo_root / entry["path"])
        )
    save_manifest(grouped, kind="ast", root=repo_root)
    write_json(
        Path(args.summary_output),
        {
            "nodes": graph.number_of_nodes(),
            "relationships": graph.number_of_edges(),
            "official_validation_errors": official_errors,
            "graph_sha256": sha256_file(graph_path),
        },
    )
    return 0


def _normalized_record(record: dict[str, Any], stripped: set[str]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in stripped}


def normalized_graph(graph_data: dict[str, Any]) -> dict[str, Any]:
    nodes = [
        _normalized_record(dict(node), DERIVED_NODE_FIELDS)
        for node in graph_data.get("nodes", [])
    ]
    relationships = [
        _normalized_record(dict(edge), DERIVED_RELATIONSHIP_FIELDS)
        for edge in graph_data.get("links", graph_data.get("edges", []))
    ]
    nodes.sort(key=canonical_json)
    relationships.sort(key=canonical_json)
    hyperedges = [dict(item) for item in graph_data.get("hyperedges", [])]
    hyperedges.sort(key=canonical_json)
    return {
        "directed": bool(graph_data.get("directed", False)),
        "multigraph": bool(graph_data.get("multigraph", False)),
        "nodes": nodes,
        "relationships": relationships,
        "hyperedges": hyperedges,
    }


def graph_fingerprints(graph_data: dict[str, Any]) -> dict[str, Any]:
    normalized = normalized_graph(graph_data)
    ids = sorted(str(node.get("id", "")) for node in normalized["nodes"])
    relationship_set = sorted(
        {
            canonical_json(
                {
                    "source": edge.get("source"),
                    "target": edge.get("target"),
                    "relation": edge.get("relation"),
                    "source_file": edge.get("source_file", ""),
                }
            )
            for edge in normalized["relationships"]
        }
    )
    return {
        "node_id_set_sha256": hash_value(ids),
        "node_content_sha256": hash_value(normalized["nodes"]),
        "relationship_endpoint_type_set_sha256": hash_value(relationship_set),
        "relationship_content_sha256": hash_value(normalized["relationships"]),
        "normalized_complete_graph_sha256": hash_value(normalized),
        "nodes": len(normalized["nodes"]),
        "relationships": len(normalized["relationships"]),
        "hyperedges": len(normalized["hyperedges"]),
    }


def source_allowed(source: str, scope: str) -> bool:
    if not source:
        return True
    canonical = canonical_source_path(source)
    return canonical is not None and authorized_scope(canonical, scope)


def source_category(source: str, siblings: Iterable[str]) -> str | None:
    canonical = canonical_source_path(source)
    if canonical is None:
        return None
    normalized = canonical.lower()
    if not normalized:
        return None
    if normalized.startswith("4_external/"):
        return "external_source_paths"
    if normalized.startswith("9_artifacts/"):
        return "artifact_source_paths"
    if normalized.startswith("graphify-out/") or "/graphify-out/" in normalized:
        return "graphify_self_ingestion_paths"
    for sibling in siblings:
        if sibling != "hermes-agent" and normalized.startswith(
            f"2_products/{sibling.lower()}/"
        ):
            return "sibling_product_source_paths"
    components = set(normalized.split("/"))
    if components & {"node_modules", "site-packages", ".npm", ".pnpm-store", ".yarn"}:
        return "dependency_source_paths"
    if components & {".venv", "venv", "env", ".tox", ".nox"}:
        return "virtual_environment_source_paths"
    if components & {
        "dist",
        "build",
        "coverage",
        "htmlcov",
        "web_dist",
        "tui_dist",
        "outputs",
        "runs",
        "logs",
    }:
        return "generated_output_source_paths"
    if any(
        marker in normalized
        for marker in ("/.env", "/credentials/", "/secrets/", "/tokens/")
    ):
        return "sensitive_source_paths"
    if normalized.endswith((".db", ".sqlite", ".sqlite3")):
        return "sensitive_source_paths"
    return None


def analyze_graph(
    repo_root: Path, graph_path: Path, inventory: dict[str, Any]
) -> dict[str, Any]:
    ensure_graphify_version()
    from graphify.validate import validate_extraction

    graph_data = read_json(graph_path)
    nodes = graph_data.get("nodes", [])
    relationships = graph_data.get("links", graph_data.get("edges", []))
    node_ids = [node.get("id") for node in nodes]
    valid_ids = {node_id for node_id in node_ids if node_id not in (None, "")}
    duplicates = len(node_ids) - len(set(node_ids))
    missing_ids = sum(node_id in (None, "") for node_id in node_ids)
    dangling_sources = sum(
        edge.get("source") not in valid_ids for edge in relationships
    )
    dangling_targets = sum(
        edge.get("target") not in valid_ids for edge in relationships
    )
    relationship_keys = [canonical_json(edge) for edge in relationships]
    duplicate_relationships = len(relationship_keys) - len(set(relationship_keys))
    siblings = inventory.get("direct_product_children", [])
    hyperedges = graph_data.get("hyperedges", [])
    source_paths = [str(node.get("source_file", "")) for node in nodes]
    source_paths.extend(str(edge.get("source_file", "")) for edge in relationships)
    source_paths.extend(str(edge.get("source_file", "")) for edge in hyperedges)
    accepted_sources = {item["path"] for item in inventory["accepted"]}
    represented_node_sources = {
        canonical
        for node in nodes
        if (canonical := canonical_source_path(str(node.get("source_file", ""))))
    }
    represented_relationship_sources = {
        canonical
        for edge in relationships
        if (canonical := canonical_source_path(str(edge.get("source_file", ""))))
    }
    categories = Counter(
        filter(None, (source_category(path, siblings) for path in source_paths))
    )
    absolute_paths = sum(is_absolute_source(path) for path in source_paths)
    noncanonical_paths = sum(
        bool(path) and canonical_source_path(path) is None for path in source_paths
    )
    unresolved = sum(
        bool(path)
        and (canonical := canonical_source_path(path)) is not None
        and not (repo_root / canonical).exists()
        for path in source_paths
    )
    unauthorized = sum(
        bool(path) and not source_allowed(path, inventory["scope"])
        for path in source_paths
    )
    unmanifested = sum(
        bool(path)
        and (canonical := canonical_source_path(path)) is not None
        and canonical not in accepted_sources
        for path in source_paths
    )
    stubs = sum(not node.get("source_file") for node in nodes)
    self_loops = [
        edge for edge in relationships if edge.get("source") == edge.get("target")
    ]
    official_errors = validate_extraction(graph_data)

    representative: dict[str, Any] = {}
    for name, selectors in REPRESENTATIVE_SELECTORS.items():
        selected_sources = {
            path
            for path in {
                canonical_source_path(str(node.get("source_file", "")))
                for node in nodes
            }
            if path is not None
            if any(
                path == selector or path.startswith(selector) for selector in selectors
            )
        }
        selected_ids = {
            node.get("id")
            for node in nodes
            if canonical_source_path(str(node.get("source_file", "")))
            in selected_sources
        }
        incident = [
            edge
            for edge in relationships
            if edge.get("source") in selected_ids or edge.get("target") in selected_ids
        ]
        representative[name] = {
            "source_files": len(selected_sources),
            "nodes": len(selected_ids),
            "relationships": len(incident),
            "relation_types": sorted(
                {str(edge.get("relation", "")) for edge in incident}
            )[:12],
        }

    subtree_nodes: Counter[str] = Counter()
    for node in nodes:
        source = canonical_source_path(str(node.get("source_file", ""))) or ""
        if source.startswith(HERMES_PREFIX):
            remainder = source[len(HERMES_PREFIX) :]
            subtree_nodes[
                remainder.split("/", 1)[0] if "/" in remainder else "(root)"
            ] += 1

    parent: dict[Any, Any] = {node_id: node_id for node_id in valid_ids}
    size: dict[Any, int] = {node_id: 1 for node_id in valid_ids}

    def find(item: Any) -> Any:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: Any, right: Any) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return
        if size[left_root] < size[right_root]:
            left_root, right_root = right_root, left_root
        parent[right_root] = left_root
        size[left_root] += size[right_root]

    degree = Counter()
    for edge in relationships:
        source = edge.get("source")
        target = edge.get("target")
        if source in valid_ids and target in valid_ids:
            union(source, target)
            degree[source] += 1
            degree[target] += 1
    component_sizes = Counter(find(node_id) for node_id in valid_ids)
    largest_component = max(component_sizes.values(), default=0)

    integrity = {
        "duplicate_node_ids": duplicates,
        "missing_node_ids": missing_ids,
        "duplicate_relationship_records": duplicate_relationships,
        "dangling_relationship_sources": dangling_sources,
        "dangling_relationship_targets": dangling_targets,
        "invalid_nodes": sum(error.startswith("Node ") for error in official_errors),
        "invalid_relationships": sum(
            error.startswith("Edge ") for error in official_errors
        ),
        "absolute_source_paths": absolute_paths,
        "noncanonical_source_paths": noncanonical_paths,
        "unresolved_nonempty_source_paths": unresolved,
        "unauthorized_source_paths": unauthorized,
        "unmanifested_source_paths": unmanifested,
        "graphify_self_ingestion_paths": categories["graphify_self_ingestion_paths"],
        "artifact_source_paths": categories["artifact_source_paths"],
        "external_source_paths": categories["external_source_paths"],
        "sibling_product_source_paths": categories["sibling_product_source_paths"],
        "dependency_source_paths": categories["dependency_source_paths"],
        "virtual_environment_source_paths": categories[
            "virtual_environment_source_paths"
        ],
        "generated_output_source_paths": categories["generated_output_source_paths"],
        "sensitive_source_paths": categories["sensitive_source_paths"],
    }
    return {
        "fingerprints": graph_fingerprints(graph_data),
        "integrity": integrity,
        "integrity_passed": all(value == 0 for value in integrity.values()),
        "schema_valid_stubs": stubs,
        "self_loops": len(self_loops),
        "self_loops_by_relation": dict(
            Counter(str(edge.get("relation", "")) for edge in self_loops)
        ),
        "relationship_types": dict(
            Counter(str(edge.get("relation", "")) for edge in relationships)
        ),
        "representative": representative,
        "hermes_nodes_by_subtree": dict(sorted(subtree_nodes.items())),
        "connectivity": {
            "nodes": len(nodes),
            "relationships": len(relationships),
            "relationships_per_node": len(relationships) / len(nodes) if nodes else 0,
            "mean_undirected_degree": 2 * len(relationships) / len(nodes)
            if nodes
            else 0,
            "isolated_nodes": sum(degree[node_id] == 0 for node_id in valid_ids),
            "connected_components": len(component_sizes),
            "largest_component_nodes": largest_component,
            "largest_component_node_share_percent": 100 * largest_component / len(nodes)
            if nodes
            else 0,
        },
        "source_coverage": {
            "accepted_sources": len(accepted_sources),
            "represented_node_sources": len(represented_node_sources),
            "represented_relationship_sources": len(represented_relationship_sources),
            "accepted_sources_without_nodes": sorted(
                accepted_sources - represented_node_sources
            ),
            "accepted_sources_without_relationships": sorted(
                accepted_sources - represented_relationship_sources
            ),
        },
    }


def worker_validate(args: argparse.Namespace) -> int:
    inventory = read_json(Path(args.inventory))
    result = analyze_graph(Path(args.repo_root).resolve(), Path(args.graph), inventory)
    write_json(Path(args.output), result)
    if not result["integrity_passed"]:
        raise PipelineError(f"Structural integrity failed: {result['integrity']}")
    return 0


def extract_command(
    script: Path,
    repo_root: Path,
    output_dir: Path,
    evidence_dir: Path,
    input_entries: list[dict[str, Any]],
    label: str,
    timeout_seconds: int,
    max_workers: int,
    audit_zero_nodes: bool = True,
    defer_validation: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    batch_dir = evidence_dir / "batches" / label
    batch_dir.mkdir(parents=True, exist_ok=False)
    input_path = batch_dir / "input-list.json"
    raw_path = batch_dir / "raw-extraction.json"
    summary_path = batch_dir / "summary.json"
    failure_path = batch_dir / "parser-failures.json"
    write_json(
        input_path, {"files": input_entries, "sha256": hash_value(input_entries)}
    )
    command = [
        sys.executable,
        "-B",
        str(script),
        "_worker_extract",
        "--repo-root",
        str(repo_root),
        "--input-list",
        str(input_path),
        "--raw-output",
        str(raw_path),
        "--summary-output",
        str(summary_path),
        "--failure-ledger",
        str(failure_path),
        "--max-workers",
        str(max_workers),
    ]
    if not audit_zero_nodes:
        command.append("--skip-zero-node-audit")
    if defer_validation:
        command.append("--defer-validation")
    process = run_owned_process(
        command,
        repo_root,
        sanitized_environment(output_dir, max_workers),
        timeout_seconds,
        batch_dir / "stdout.log",
        batch_dir / "stderr.log",
        label,
    )
    process.update(
        {
            "batch_id": label,
            "input_list_sha256": hash_value(input_entries),
            "script_sha256": sha256_file(script),
            "script_version": PIPELINE_VERSION,
            "graphify_version": SUPPORTED_GRAPHIFY_VERSION,
            "raw_extraction_sha256": sha256_file(raw_path),
        }
    )
    summary = read_json(summary_path)
    summary["raw_sha256"] = process["raw_extraction_sha256"]
    write_json(summary_path, summary)
    write_json(batch_dir / "execution.json", process)
    return process, summary


def run_full(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    output_dir = ensure_external(repo_root, Path(args.output_dir), "candidate output")
    evidence_dir = ensure_external(
        repo_root, Path(args.evidence_dir), "evidence directory"
    )
    ensure_disjoint_paths(output_dir, evidence_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise PipelineError(f"Candidate output must start empty: {output_dir}")
    if evidence_dir.exists() and any(evidence_dir.iterdir()):
        raise PipelineError(f"Evidence directory must start empty: {evidence_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).resolve()
    started = time.perf_counter()
    deadline = started + args.pipeline_timeout

    inventory = build_inventory(repo_root, args.scope, args.batch_size)
    write_inventory(evidence_dir, inventory)
    inventory_path = evidence_dir / "inventory-summary.json"
    write_json(output_dir / "scale-manifest.json", inventory)

    cache_before = directory_inventory(output_dir / "cache")
    warm_source = None
    if args.cache_mode == "warm":
        if not args.warm_from:
            raise PipelineError("Warm mode requires --warm-from")
        warm_source = ensure_external(
            repo_root, Path(args.warm_from), "warm cache source"
        )
        ensure_disjoint_paths(output_dir, evidence_dir, warm_source)
        source_cache = warm_source / "cache"
        if not source_cache.is_dir():
            raise PipelineError(f"Warm cache source is missing: {source_cache}")
        shutil.copytree(source_cache, output_dir / "cache", dirs_exist_ok=True)
        cache_before = directory_inventory(output_dir / "cache")
    elif args.warm_from:
        raise PipelineError("Cold mode cannot use --warm-from")

    batch_processes = []
    batch_summaries = []
    accepted_by_path = {item["path"]: item for item in inventory["accepted"]}
    for batch in inventory["batches"]:
        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            raise PipelineError("Full candidate pipeline exceeded its total time bound")
        entries = [accepted_by_path[path] for path in batch["paths"]]
        process, summary = extract_command(
            script,
            repo_root,
            output_dir,
            evidence_dir,
            entries,
            batch["batch_id"],
            min(args.batch_timeout, max(1, int(remaining))),
            args.max_workers,
        )
        batch_processes.append(process)
        batch_summaries.append(summary)

    parser_failures = [
        failure for summary in batch_summaries for failure in summary["parser_failures"]
    ]
    if parser_failures:
        raise PipelineError(
            f"Official extraction reported {len(parser_failures)} parser failures"
        )
    zero_node_files = sorted(
        {path for summary in batch_summaries for path in summary["zero_node_files"]}
    )
    zero_node_evidence = validate_zero_node_sources(repo_root, zero_node_files)

    remaining = deadline - time.perf_counter()
    if remaining <= 0:
        raise PipelineError(
            "Full candidate pipeline exceeded its total time bound before global resolution"
        )
    resolve_process, resolve_summary = extract_command(
        script,
        repo_root,
        output_dir,
        evidence_dir,
        inventory["accepted"],
        "resolve-all",
        min(args.batch_timeout, max(1, int(remaining))),
        args.max_workers,
        audit_zero_nodes=False,
        defer_validation=True,
    )

    build_dir = evidence_dir / "build"
    build_dir.mkdir()
    raw_path = evidence_dir / "batches" / "resolve-all" / "raw-extraction.json"
    build_command = [
        sys.executable,
        "-B",
        str(script),
        "_worker_build",
        "--repo-root",
        str(repo_root),
        "--raw-input",
        str(raw_path),
        "--graph-output",
        str(output_dir / "graph.json"),
        "--inventory",
        str(inventory_path),
        "--summary-output",
        str(build_dir / "summary.json"),
    ]
    build_process = run_owned_process(
        build_command,
        repo_root,
        sanitized_environment(output_dir, args.max_workers),
        min(args.batch_timeout, max(1, int(deadline - time.perf_counter()))),
        build_dir / "stdout.log",
        build_dir / "stderr.log",
        "build",
    )
    write_json(build_dir / "execution.json", build_process)

    validate_dir = evidence_dir / "validation"
    validate_dir.mkdir()
    validate_command = [
        sys.executable,
        "-B",
        str(script),
        "_worker_validate",
        "--repo-root",
        str(repo_root),
        "--graph",
        str(output_dir / "graph.json"),
        "--inventory",
        str(inventory_path),
        "--output",
        str(validate_dir / "result.json"),
    ]
    validate_process = run_owned_process(
        validate_command,
        repo_root,
        sanitized_environment(output_dir, args.max_workers),
        min(args.batch_timeout, max(1, int(deadline - time.perf_counter()))),
        validate_dir / "stdout.log",
        validate_dir / "stderr.log",
        "validate",
    )
    write_json(validate_dir / "execution.json", validate_process)
    validation = read_json(validate_dir / "result.json")
    if (
        validation["source_coverage"]["accepted_sources_without_nodes"]
        != zero_node_files
    ):
        raise PipelineError(
            "Final graph source coverage does not match immutable batch zero-node ledgers"
        )
    official_manifest = validate_official_manifest(output_dir, inventory)
    cache_after = directory_inventory(output_dir / "cache")
    final_inventory = build_inventory(repo_root, args.scope, args.batch_size)
    stable_fields = (
        "git_commit",
        "git_index_sha256",
        "accepted_manifest_sha256",
        "ignored_manifest_sha256",
        "sensitive_manifest_sha256",
        "unsupported_manifest_sha256",
        "batch_definition_sha256",
    )
    changed_fields = [
        field for field in stable_fields if inventory[field] != final_inventory[field]
    ]
    if changed_fields:
        raise PipelineError(
            f"Repository inputs changed during extraction: {', '.join(changed_fields)}"
        )
    duration = time.perf_counter() - started
    if duration > args.pipeline_timeout:
        raise PipelineError("Full candidate pipeline exceeded its total time bound")

    total_files = inventory["counts"]["accepted"]
    result = {
        "schema_version": 1,
        "run_id": args.run_id,
        "scope": args.scope,
        "cache_mode": args.cache_mode,
        "cache_root": str(output_dir / "cache"),
        "warm_cache_source": str(warm_source / "cache") if warm_source else None,
        "cache_input": cache_before,
        "cache_output": cache_after,
        "git_commit": inventory["git_commit"],
        "graphify_version": SUPPORTED_GRAPHIFY_VERSION,
        "pipeline_version": PIPELINE_VERSION,
        "pipeline_script_sha256": sha256_file(script),
        "graphifyignore_sha256": sha256_file(repo_root / ".graphifyignore"),
        "inventory_hashes": {
            key: inventory[key]
            for key in (
                "accepted_manifest_sha256",
                "ignored_manifest_sha256",
                "sensitive_manifest_sha256",
                "unsupported_manifest_sha256",
                "batch_definition_sha256",
            )
        },
        "counts": inventory["counts"],
        "batch_processes": batch_processes,
        "batch_summaries": batch_summaries,
        "parser_failures": parser_failures,
        "zero_node_files": zero_node_files,
        "zero_node_evidence": zero_node_evidence,
        "official_manifest": official_manifest,
        "cache_metrics": {
            "priming_hits": sum(item["cache_hits"] for item in batch_summaries),
            "priming_misses": sum(item["cache_misses"] for item in batch_summaries),
            "resolve_hits": resolve_summary["cache_hits"],
            "resolve_misses": resolve_summary["cache_misses"],
        },
        "resolve_process": resolve_process,
        "resolve_summary": resolve_summary,
        "build_process": build_process,
        "validate_process": validate_process,
        "duration_seconds": duration,
        "files_per_second": total_files / duration if duration else 0,
        "largest_batch_duration_seconds": max(
            item["duration_seconds"] for item in batch_processes
        ),
        "largest_operation_duration_seconds": max(
            [item["duration_seconds"] for item in batch_processes]
            + [resolve_process["duration_seconds"]]
        ),
        "peak_memory_bytes": max(
            item.get("peak_memory_bytes") or 0
            for item in [
                *batch_processes,
                resolve_process,
                build_process,
                validate_process,
            ]
        ),
        "cpu_seconds": sum(
            item.get("cpu_seconds") or 0
            for item in [
                *batch_processes,
                resolve_process,
                build_process,
                validate_process,
            ]
        ),
        "graph_path": str(output_dir / "graph.json"),
        "graph_sha256": sha256_file(output_dir / "graph.json"),
        **validation,
    }
    write_json(evidence_dir / "run-result.json", result)
    print(
        canonical_json({"run_id": args.run_id, "fingerprints": result["fingerprints"]})
    )
    return 0


def worker_merge(args: argparse.Namespace) -> int:
    ensure_graphify_version()
    from graphify.build import build_merge
    from graphify.export import to_json

    repo_root = Path(args.repo_root).resolve()
    graph_path = Path(args.graph)
    extraction = read_json(Path(args.raw_input))
    changed = read_json(Path(args.changed))
    deleted = read_json(Path(args.deleted))
    represented = {
        normalize_path(str(node.get("source_file", "")))
        for node in extraction.get("nodes", [])
        if node.get("source_file")
    }
    changed_zero = [path for path in changed if path not in represented]
    prune = sorted(set(deleted + changed_zero))
    graph = build_merge(
        [extraction],
        graph_path=graph_path,
        prune_sources=prune or None,
        root=repo_root,
    )
    if not to_json(
        graph, {}, str(graph_path), force=True, built_at_commit=git_head(repo_root)
    ):
        raise PipelineError("Official serialization refused incremental graph")
    write_json(
        Path(args.output),
        {
            "changed": changed,
            "deleted": deleted,
            "changed_zero_node_sources": changed_zero,
            "pruned_sources": prune,
            "nodes": graph.number_of_nodes(),
            "relationships": graph.number_of_edges(),
            "graph_sha256": sha256_file(graph_path),
        },
    )
    return 0


def run_incremental(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    output_dir = ensure_external(repo_root, Path(args.output_dir), "candidate output")
    evidence_dir = ensure_external(
        repo_root, Path(args.evidence_dir), "evidence directory"
    )
    ensure_disjoint_paths(output_dir, evidence_dir)
    if evidence_dir.exists() and any(evidence_dir.iterdir()):
        raise PipelineError(f"Evidence directory must start empty: {evidence_dir}")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    graph_path = output_dir / "graph.json"
    prior_manifest_path = output_dir / "scale-manifest.json"
    if not graph_path.is_file() or not prior_manifest_path.is_file():
        raise PipelineError(
            "Incremental refresh requires graph.json and scale-manifest.json"
        )
    previous = read_json(prior_manifest_path)
    current = build_inventory(repo_root, previous["scope"], previous["batch_size"])
    write_inventory(evidence_dir, current)
    old_by_path = {item["path"]: item for item in previous["accepted"]}
    new_by_path = {item["path"]: item for item in current["accepted"]}
    changed = sorted(
        path
        for path, item in new_by_path.items()
        if path not in old_by_path or item["sha256"] != old_by_path[path]["sha256"]
    )
    deleted = sorted(set(old_by_path) - set(new_by_path))
    write_json(evidence_dir / "changed-sources.json", changed)
    write_json(evidence_dir / "deleted-sources.json", deleted)
    script = Path(__file__).resolve()
    if not changed and not deleted:
        validation = analyze_graph(repo_root, graph_path, current)
        if not validation["integrity_passed"]:
            raise PipelineError(
                f"No-change incremental graph failed integrity: {validation['integrity']}"
            )
        result = {
            "changed": [],
            "deleted": [],
            "extract_summary": {"files": 0, "nodes": 0, "relationships": 0},
            "merge": {"changed": [], "deleted": [], "pruned_sources": []},
            **validation,
        }
        write_json(evidence_dir / "incremental-result.json", result)
        print(canonical_json(result["merge"]))
        return 0
    if changed or deleted:
        _, extract_summary = extract_command(
            script,
            repo_root,
            output_dir,
            evidence_dir,
            current["accepted"],
            "incremental-resolve-all",
            args.batch_timeout,
            args.max_workers,
        )
        raw_path = (
            evidence_dir / "batches" / "incremental-resolve-all" / "raw-extraction.json"
        )
        if extract_summary["parser_failures"]:
            raise PipelineError(
                f"Incremental extraction reported {len(extract_summary['parser_failures'])} parser failures"
            )
    else:
        raw_path = evidence_dir / "empty-extraction.json"
        write_json(raw_path, {"nodes": [], "edges": [], "hyperedges": []})
        extract_summary = {"files": 0, "nodes": 0, "relationships": 0}

    merge_dir = evidence_dir / "merge"
    merge_dir.mkdir()
    rollback_dir = evidence_dir / "rollback"
    rollback_dir.mkdir()
    working_graph = output_dir / "cache" / f".incremental-{uuid.uuid4().hex}.graph.json"
    working_graph.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(graph_path, working_graph)
    rollback_files = (
        "graph.json",
        "scale-manifest.json",
        "manifest.json",
        "provenance.json",
        "GRAPH_REPORT.md",
        "graph.html",
        ".graphify_labels.json",
        ".graphify_labels.json.sig",
    )
    for name in rollback_files:
        source = output_dir / name
        if source.is_file():
            shutil.copy2(source, rollback_dir / name)
    command = [
        sys.executable,
        "-B",
        str(script),
        "_worker_merge",
        "--repo-root",
        str(repo_root),
        "--graph",
        str(working_graph),
        "--raw-input",
        str(raw_path),
        "--changed",
        str(evidence_dir / "changed-sources.json"),
        "--deleted",
        str(evidence_dir / "deleted-sources.json"),
        "--output",
        str(merge_dir / "result.json"),
    ]
    try:
        execution = run_owned_process(
            command,
            repo_root,
            sanitized_environment(output_dir, args.max_workers),
            args.batch_timeout,
            merge_dir / "stdout.log",
            merge_dir / "stderr.log",
            "incremental-merge",
        )
        write_json(merge_dir / "execution.json", execution)
        validation = analyze_graph(repo_root, working_graph, current)
        if not validation["integrity_passed"]:
            raise PipelineError(
                f"Incremental structural integrity failed: {validation['integrity']}"
            )
    except Exception:
        working_graph.unlink(missing_ok=True)
        raise
    merge_result = read_json(merge_dir / "result.json")
    final_inventory = build_inventory(
        repo_root, previous["scope"], previous["batch_size"]
    )
    stability_fields = (
        "git_commit",
        "git_index_sha256",
        "accepted_manifest_sha256",
        "ignored_manifest_sha256",
        "sensitive_manifest_sha256",
        "unsupported_manifest_sha256",
        "batch_definition_sha256",
    )
    if any(current[field] != final_inventory[field] for field in stability_fields):
        working_graph.unlink(missing_ok=True)
        raise PipelineError("Repository inputs changed during incremental extraction")
    try:
        os.replace(working_graph, graph_path)
        write_json(output_dir / "scale-manifest.json", current)
        for name in rollback_files[2:]:
            (output_dir / name).unlink(missing_ok=True)
    except Exception:
        for name in rollback_files:
            preserved = rollback_dir / name
            destination = output_dir / name
            if preserved.is_file():
                shutil.copy2(preserved, destination)
            else:
                destination.unlink(missing_ok=True)
        raise
    result = {
        "changed": changed,
        "deleted": deleted,
        "extract_summary": extract_summary,
        "merge": merge_result,
        "derived_outputs_invalidated": [
            name for name in rollback_files[2:] if (rollback_dir / name).is_file()
        ],
        **validation,
    }
    write_json(evidence_dir / "incremental-result.json", result)
    print(canonical_json(result["merge"]))
    return 0


def record_differences(
    left_graph: Path, right_graph: Path, limit: int = 100
) -> dict[str, Any]:
    left = normalized_graph(read_json(left_graph))
    right = normalized_graph(read_json(right_graph))
    result: dict[str, Any] = {}
    for key in ("nodes", "relationships", "hyperedges"):
        left_records = {canonical_json(item) for item in left[key]}
        right_records = {canonical_json(item) for item in right[key]}
        result[key] = {
            "left_only_count": len(left_records - right_records),
            "right_only_count": len(right_records - left_records),
            "left_only": sorted(left_records - right_records)[:limit],
            "right_only": sorted(right_records - left_records)[:limit],
        }
    result["graph_semantics"] = {
        "left": {key: left[key] for key in ("directed", "multigraph")},
        "right": {key: right[key] for key in ("directed", "multigraph")},
        "equal": all(left[key] == right[key] for key in ("directed", "multigraph")),
    }
    return result


DETERMINISM_KEYS = (
    "node_id_set_sha256",
    "node_content_sha256",
    "relationship_endpoint_type_set_sha256",
    "relationship_content_sha256",
    "normalized_complete_graph_sha256",
)

INVENTORY_HASH_KEYS = (
    "accepted_manifest_sha256",
    "ignored_manifest_sha256",
    "sensitive_manifest_sha256",
    "unsupported_manifest_sha256",
    "batch_definition_sha256",
)


def verify_run_results(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    expected_modes = {
        "cold_run_1": "cold",
        "cold_run_2": "cold",
        "warm_run_1": "warm",
        "warm_run_2": "warm",
    }
    by_id = {result.get("run_id"): result for result in results}
    if len(results) != 4 or set(by_id) != set(expected_modes):
        raise PipelineError(
            "Determinism requires unique cold_run_1, cold_run_2, warm_run_1 and warm_run_2 results"
        )
    graph_paths = [Path(result["graph_path"]).resolve() for result in results]
    if len(set(graph_paths)) != 4:
        raise PipelineError("Determinism requires four distinct candidate graph files")

    invariant_fields = (
        "git_commit",
        "graphify_version",
        "pipeline_version",
        "pipeline_script_sha256",
        "graphifyignore_sha256",
        "inventory_hashes",
        "counts",
    )
    for field in invariant_fields:
        if len({canonical_json(result[field]) for result in results}) != 1:
            raise PipelineError(f"Candidate runs disagree on {field}")

    for run_id, mode in expected_modes.items():
        result = by_id[run_id]
        if result.get("scope") != "full":
            raise PipelineError(f"{run_id} must use the full authorized scope")
        if result.get("cache_mode") != mode:
            raise PipelineError(f"{run_id} must use {mode} cache mode")
        if not result.get("integrity_passed") or result.get("parser_failures"):
            raise PipelineError(f"{run_id} did not pass integrity and parser gates")
        if result.get("source_coverage", {}).get(
            "accepted_sources_without_nodes"
        ) != result.get("zero_node_files"):
            raise PipelineError(
                f"{run_id} final source coverage does not match zero-node evidence"
            )
        zero_records = result.get("zero_node_evidence", [])
        if [item.get("path") for item in zero_records] != result.get(
            "zero_node_files"
        ) or any(Path(item["path"]).suffix.lower() != ".json" for item in zero_records):
            raise PipelineError(f"{run_id} has invalid zero-node eligibility evidence")
        if (
            result.get("duration_seconds", DEFAULT_PIPELINE_TIMEOUT + 1)
            > DEFAULT_PIPELINE_TIMEOUT
        ):
            raise PipelineError(f"{run_id} exceeded the full pipeline time bound")
        if (
            result.get("largest_batch_duration_seconds", DEFAULT_BATCH_TIMEOUT + 1)
            > DEFAULT_BATCH_TIMEOUT
        ):
            raise PipelineError(f"{run_id} exceeded the per-batch time bound")
        if (
            result.get("largest_operation_duration_seconds", DEFAULT_BATCH_TIMEOUT + 1)
            > DEFAULT_BATCH_TIMEOUT
        ):
            raise PipelineError(f"{run_id} exceeded the full-corpus resolve time bound")
        processes = [
            *result.get("batch_processes", []),
            result.get("resolve_process", {}),
            result.get("build_process", {}),
            result.get("validate_process", {}),
        ]
        if any(
            item.get("exit_code") != 0 or item.get("timed_out") for item in processes
        ):
            raise PipelineError(f"{run_id} contains a failed or timed-out process")
        graph_path = Path(result["graph_path"])
        if (
            not graph_path.is_file()
            or sha256_file(graph_path) != result["graph_sha256"]
        ):
            raise PipelineError(f"{run_id} graph artifact does not match its evidence")
        recomputed = graph_fingerprints(read_json(graph_path))
        if any(
            recomputed[key] != result["fingerprints"][key] for key in DETERMINISM_KEYS
        ):
            raise PipelineError(
                f"{run_id} declared fingerprints do not match graph.json"
            )
        scale_manifest_path = graph_path.parent / "scale-manifest.json"
        if not scale_manifest_path.is_file():
            raise PipelineError(f"{run_id} scale-manifest.json is missing")
        scale_manifest = read_json(scale_manifest_path)
        if (
            scale_manifest.get("scope") != "full"
            or scale_manifest.get("counts") != result.get("counts")
            or set(result.get("inventory_hashes", {})) != set(INVENTORY_HASH_KEYS)
            or any(
                scale_manifest.get(key) != result.get("inventory_hashes", {}).get(key)
                for key in INVENTORY_HASH_KEYS
            )
        ):
            raise PipelineError(f"{run_id} scale manifest does not match run evidence")
        if validate_official_manifest(graph_path.parent, scale_manifest) != result.get(
            "official_manifest"
        ):
            raise PipelineError(
                f"{run_id} official manifest is not bound to its inventory"
            )

    for warm_id, cold_id in (
        ("warm_run_1", "cold_run_1"),
        ("warm_run_2", "cold_run_2"),
    ):
        warm = by_id[warm_id]
        cold = by_id[cold_id]
        expected_source = Path(cold["graph_path"]).parent / "cache"
        if Path(warm["warm_cache_source"]).resolve() != expected_source.resolve():
            raise PipelineError(
                f"{warm_id} does not consume the immediately preceding cold cache"
            )
        if warm["cache_input"]["sha256"] != cold["cache_output"]["sha256"]:
            raise PipelineError(
                f"{warm_id} cache input hash does not match {cold_id} cache output"
            )
        if warm.get("cache_metrics", {}).get("priming_hits", 0) <= cold.get(
            "cache_metrics", {}
        ).get("priming_hits", 0):
            raise PipelineError(
                f"{warm_id} does not prove additional successful cache reads"
            )
        if warm.get("cache_metrics", {}).get("resolve_hits", 0) <= 0:
            raise PipelineError(f"{warm_id} has no successful full-corpus cache reads")
    if (
        len({canonical_json(result.get("zero_node_files", [])) for result in results})
        != 1
    ):
        raise PipelineError("Candidate runs disagree on accepted zero-node sources")
    if (
        len(
            {canonical_json(result.get("zero_node_evidence", [])) for result in results}
        )
        != 1
    ):
        raise PipelineError("Candidate runs disagree on zero-node JSON validation")
    return by_id


def compare_runs(args: argparse.Namespace) -> int:
    results = [read_json(Path(path)) for path in args.run_results]
    by_id = verify_run_results(results)
    ordered = [
        by_id[run_id]
        for run_id in ("cold_run_1", "cold_run_2", "warm_run_1", "warm_run_2")
    ]
    equality = {
        key: len({result["fingerprints"][key] for result in ordered}) == 1
        for key in DETERMINISM_KEYS
    }
    differences = []
    reference = ordered[0]
    for result in ordered[1:]:
        if any(
            reference["fingerprints"][key] != result["fingerprints"][key]
            for key in DETERMINISM_KEYS
        ):
            differences.append(
                {
                    "left": reference["run_id"],
                    "right": result["run_id"],
                    "records": record_differences(
                        Path(reference["graph_path"]), Path(result["graph_path"])
                    ),
                }
            )
    comparison = {
        "runs": [result["run_id"] for result in ordered],
        "run_result_sha256": {
            result["run_id"]: sha256_file(Path(path))
            for result, path in zip(results, args.run_results)
        },
        "hashes": {result["run_id"]: result["fingerprints"] for result in ordered},
        "equality": equality,
        "accepted": all(equality.values()),
        "record_level_differences": differences,
    }
    write_json(Path(args.output), comparison)
    print(canonical_json(comparison["equality"]))
    return 0 if comparison["accepted"] else 2


def baseline_subset_result(baseline_path: Path, candidate_path: Path) -> dict[str, Any]:
    baseline = normalized_graph(read_json(baseline_path))
    candidate = normalized_graph(read_json(candidate_path))
    if not baseline["nodes"]:
        raise PipelineError("Governed baseline graph must contain at least one node")
    result: dict[str, Any] = {}
    for key in ("nodes", "relationships", "hyperedges"):
        baseline_set = {canonical_json(item) for item in baseline[key]}
        candidate_set = {canonical_json(item) for item in candidate[key]}
        missing = sorted(baseline_set - candidate_set)
        result[key] = {
            "baseline": len(baseline_set),
            "missing": len(missing),
            "examples": missing[:100],
        }
    result["graph_semantics"] = {
        key: {
            "baseline": baseline[key],
            "candidate": candidate[key],
            "equal": baseline[key] == candidate[key],
        }
        for key in ("directed", "multigraph")
    }
    result["accepted"] = all(
        result[key]["missing"] == 0 for key in ("nodes", "relationships", "hyperedges")
    ) and all(item["equal"] for item in result["graph_semantics"].values())
    result["baseline_graph_sha256"] = sha256_file(baseline_path)
    result["baseline_normalized_sha256"] = graph_fingerprints(read_json(baseline_path))[
        "normalized_complete_graph_sha256"
    ]
    result["candidate_graph_sha256"] = sha256_file(candidate_path)
    result["candidate_normalized_sha256"] = graph_fingerprints(
        read_json(candidate_path)
    )["normalized_complete_graph_sha256"]
    return result


def verify_baseline_evidence(
    repo_root: Path,
    baseline_graph: Path,
    candidate_graph: Path,
    baseline_result_path: Path,
    candidate_result_path: Path,
) -> dict[str, Any]:
    baseline_result = read_json(baseline_result_path)
    candidate_result = read_json(candidate_result_path)
    if (
        baseline_result.get("run_id") != "baseline_run"
        or baseline_result.get("scope") != "baseline"
        or baseline_result.get("cache_mode") != "cold"
        or not baseline_result.get("integrity_passed")
        or baseline_result.get("parser_failures")
    ):
        raise PipelineError("Baseline run evidence did not pass its required gates")
    if (
        candidate_result.get("run_id") != "cold_run_1"
        or candidate_result.get("scope") != "full"
        or not candidate_result.get("integrity_passed")
    ):
        raise PipelineError("Baseline comparison candidate must be accepted cold_run_1")
    for result, graph, scope in (
        (baseline_result, baseline_graph, "baseline"),
        (candidate_result, candidate_graph, "full"),
    ):
        if Path(result.get("graph_path", "")).resolve() != graph.resolve():
            raise PipelineError(
                "Baseline comparison graph path does not match run evidence"
            )
        if (
            not graph.is_file()
            or result.get("graph_sha256") != sha256_file(graph)
            or any(
                result.get("fingerprints", {}).get(key)
                != graph_fingerprints(read_json(graph))[key]
                for key in DETERMINISM_KEYS
            )
        ):
            raise PipelineError("Baseline comparison graph does not match run evidence")
        manifest = read_json(graph.parent / "scale-manifest.json")
        if manifest.get("scope") != scope:
            raise PipelineError(
                "Baseline comparison scale manifest has the wrong scope"
            )
        if validate_official_manifest(graph.parent, manifest) != result.get(
            "official_manifest"
        ):
            raise PipelineError("Baseline comparison official manifest is not bound")
        current_inventory = build_inventory(
            repo_root, scope, int(manifest["batch_size"])
        )
        require_matching_inventory(
            manifest, current_inventory, f"{scope.title()} scale manifest"
        )
        analysis = analyze_graph(repo_root, graph, manifest)
        if (
            not analysis["integrity_passed"]
            or result.get("integrity") != analysis["integrity"]
            or result.get("source_coverage") != analysis["source_coverage"]
            or result.get("zero_node_files")
            != analysis["source_coverage"]["accepted_sources_without_nodes"]
            or result.get("zero_node_evidence")
            != validate_zero_node_sources(repo_root, result.get("zero_node_files", []))
        ):
            raise PipelineError(
                "Baseline comparison graph integrity and source coverage are not attested"
            )
    invariant_fields = (
        "git_commit",
        "graphify_version",
        "pipeline_version",
        "pipeline_script_sha256",
        "graphifyignore_sha256",
    )
    if any(
        baseline_result.get(field) != candidate_result.get(field)
        for field in invariant_fields
    ):
        raise PipelineError("Baseline and full candidate runs disagree on fixed inputs")
    baseline_manifest = read_json(baseline_graph.parent / "scale-manifest.json")
    candidate_manifest = read_json(candidate_graph.parent / "scale-manifest.json")
    baseline_inputs = {
        canonical_json({key: value for key, value in item.items() if key != "batch_id"})
        for item in baseline_manifest["accepted"]
    }
    candidate_inputs = {
        canonical_json({key: value for key, value in item.items() if key != "batch_id"})
        for item in candidate_manifest["accepted"]
    }
    if not baseline_inputs or not baseline_inputs.issubset(candidate_inputs):
        raise PipelineError(
            "Governed baseline inputs are not a nonempty subset of full scope"
        )
    result = baseline_subset_result(baseline_graph, candidate_graph)
    result.update(
        {
            "baseline_run_id": "baseline_run",
            "candidate_run_id": "cold_run_1",
            "baseline_run_result_sha256": sha256_file(baseline_result_path),
            "candidate_run_result_sha256": sha256_file(candidate_result_path),
            "baseline_accepted_manifest_sha256": baseline_manifest[
                "accepted_manifest_sha256"
            ],
            "candidate_accepted_manifest_sha256": candidate_manifest[
                "accepted_manifest_sha256"
            ],
        }
    )
    return result


def compare_baseline(args: argparse.Namespace) -> int:
    result = verify_baseline_evidence(
        Path(args.repo_root).resolve(),
        Path(args.baseline_graph),
        Path(args.candidate_graph),
        Path(args.baseline_run_result),
        Path(args.candidate_run_result),
    )
    write_json(Path(args.output), result)
    print(canonical_json(result))
    return 0 if result["accepted"] else 2


def fingerprint_output(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).resolve()
    graph = read_json(output_dir / "graph.json")
    manifest = (
        read_json(output_dir / "manifest.json")
        if (output_dir / "manifest.json").exists()
        else {}
    )
    labels = (
        read_json(output_dir / ".graphify_labels.json")
        if (output_dir / ".graphify_labels.json").exists()
        else {}
    )
    community_membership = sorted(
        (str(node.get("id", "")), node.get("community"))
        for node in graph.get("nodes", [])
    )
    direct_files = []
    for path in sorted(item for item in output_dir.iterdir() if item.is_file()):
        direct_files.append(
            {
                "path": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    result = {
        "direct_outputs": direct_files,
        "graph": graph_fingerprints(graph),
        "manifest_source_path_sha256": hash_value(
            sorted(normalize_path(path) for path in manifest)
        ),
        "labels_sha256": hash_value(labels),
        "community_membership_sha256": hash_value(community_membership),
        "tree": directory_inventory(output_dir),
    }
    write_json(Path(args.output), result)
    print(canonical_json(result["graph"]))
    return 0


def validate_derived_outputs(output_dir: Path) -> dict[str, Any]:
    ensure_graphify_version()
    from graphify.cluster import community_member_sigs

    graph = read_json(output_dir / "graph.json")
    labels = read_json(output_dir / ".graphify_labels.json")
    signatures = read_json(output_dir / ".graphify_labels.json.sig")
    communities: dict[int, list[str]] = {}
    node_community: dict[str, int] = {}
    for node in graph.get("nodes", []):
        community = node.get("community")
        if not isinstance(community, int):
            raise PipelineError(
                "Clustered graph contains a node without an integer community"
            )
        communities.setdefault(community, []).append(str(node["id"]))
        node_community[str(node["id"])] = community
        if node.get("community_name") != labels.get(str(community)):
            raise PipelineError(
                "Graph community_name does not match the official labels file"
            )
    expected_keys = {str(community) for community in communities}
    if set(labels) != expected_keys or not all(
        isinstance(value, str) and value for value in labels.values()
    ):
        raise PipelineError(
            "Official labels do not cover every graph community exactly"
        )
    expected_signatures = {
        str(key): value for key, value in community_member_sigs(communities).items()
    }
    if signatures != expected_signatures:
        raise PipelineError("Community membership signatures do not match graph.json")

    relationships = graph.get("links", graph.get("edges", []))
    cross_community_edges = sum(
        node_community.get(str(edge.get("source")))
        != node_community.get(str(edge.get("target")))
        for edge in relationships
    )
    aggregated_community_edges = len(
        {
            tuple(
                sorted(
                    (
                        node_community[str(edge.get("source"))],
                        node_community[str(edge.get("target"))],
                    )
                )
            )
            for edge in relationships
            if node_community.get(str(edge.get("source"))) is not None
            and node_community.get(str(edge.get("target"))) is not None
            and node_community[str(edge.get("source"))]
            != node_community[str(edge.get("target"))]
        }
    )
    community_count = len(communities)
    report = (output_dir / "GRAPH_REPORT.md").read_text(encoding="utf-8")
    report_summary = (
        f"- {len(graph.get('nodes', []))} nodes · {len(relationships)} edges · "
        f"{community_count} communities"
    )
    if report_summary not in report:
        raise PipelineError("GRAPH_REPORT.md summary does not match graph.json")
    html = (output_dir / "graph.html").read_text(encoding="utf-8")
    html_stats = re.search(
        r"(\d+) nodes &middot; (\d+) edges &middot; (\d+) communities", html
    )
    if not html_stats:
        raise PipelineError("Community HTML counts do not match graph.json")
    html_nodes, html_edges, html_communities = map(int, html_stats.groups())
    valid_aggregated = (
        html_nodes == community_count
        and html_edges == aggregated_community_edges
        and html_communities == community_count
    )
    valid_full = (
        html_nodes == len(graph.get("nodes", []))
        and html_edges == len(relationships)
        and html_communities == community_count
    )
    if not (valid_aggregated or valid_full):
        raise PipelineError("Community HTML counts do not match graph.json")
    title = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if not title or re.search(r"[A-Za-z]:[\\/]", title.group(1)):
        raise PipelineError(
            "Community HTML title is missing or contains an absolute path"
        )
    return {
        "communities": community_count,
        "community_html_nodes": html_nodes,
        "community_html_edges": html_edges,
        "cross_community_relationships": cross_community_edges,
        "aggregated_community_edges": aggregated_community_edges,
        "labels_sha256": hash_value(labels),
        "community_membership_sha256": hash_value(
            sorted(
                (node_id, community) for node_id, community in node_community.items()
            )
        ),
        "membership_signature_sha256": hash_value(signatures),
    }


def generate_provenance(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    output_dir = ensure_external(repo_root, Path(args.output_dir), "candidate output")
    run_results = [read_json(Path(path)) for path in args.run_results]
    by_id = verify_run_results(run_results)
    run_results = [
        by_id[run_id]
        for run_id in ("cold_run_1", "cold_run_2", "warm_run_1", "warm_run_2")
    ]
    comparison = read_json(Path(args.comparison))
    baseline = read_json(Path(args.baseline_comparison))
    run_paths_by_id = {
        read_json(Path(path))["run_id"]: Path(path) for path in args.run_results
    }
    current_run_hashes = {
        result["run_id"]: sha256_file(Path(path))
        for result, path in zip(
            [read_json(Path(path)) for path in args.run_results], args.run_results
        )
    }
    if (
        not comparison.get("accepted")
        or comparison.get("runs") != [result["run_id"] for result in run_results]
        or not all(comparison.get("equality", {}).get(key) for key in DETERMINISM_KEYS)
        or comparison.get("run_result_sha256") != current_run_hashes
        or comparison.get("hashes")
        != {result["run_id"]: result["fingerprints"] for result in run_results}
    ):
        raise PipelineError(
            "Cannot generate accepted provenance for nondeterministic runs"
        )
    recomputed_baseline = verify_baseline_evidence(
        repo_root,
        Path(args.baseline_graph),
        Path(by_id["cold_run_1"]["graph_path"]),
        Path(args.baseline_run_result),
        run_paths_by_id["cold_run_1"],
    )
    if not baseline.get("accepted") or baseline != recomputed_baseline:
        raise PipelineError(
            "Cannot generate accepted provenance for an unverified baseline comparison"
        )
    if not all(result.get("integrity_passed") for result in run_results):
        raise PipelineError(
            "Cannot generate accepted provenance for a structurally invalid run"
        )
    if run_results[0]["pipeline_script_sha256"] != sha256_file(
        Path(__file__).resolve()
    ):
        raise PipelineError("Run evidence was produced by a different pipeline script")
    if run_results[0]["graphifyignore_sha256"] != sha256_file(
        repo_root / ".graphifyignore"
    ):
        raise PipelineError("Run evidence was produced by a different ignore policy")
    if run_results[0]["git_commit"] != git_head(repo_root):
        raise PipelineError("Run evidence was produced from a different Git commit")
    scale_manifest = read_json(output_dir / "scale-manifest.json")
    current_full_inventory = build_inventory(
        repo_root, "full", int(scale_manifest["batch_size"])
    )
    require_matching_inventory(
        scale_manifest, current_full_inventory, "Candidate scale manifest"
    )
    validate_official_manifest(output_dir, current_full_inventory)
    baseline_scale_manifest = read_json(
        Path(args.baseline_graph).parent / "scale-manifest.json"
    )
    current_baseline_inventory = build_inventory(
        repo_root, "baseline", int(baseline_scale_manifest["batch_size"])
    )
    require_matching_inventory(
        baseline_scale_manifest,
        current_baseline_inventory,
        "Baseline scale manifest",
    )
    if (
        validate_zero_node_sources(repo_root, run_results[0]["zero_node_files"])
        != run_results[0]["zero_node_evidence"]
    ):
        raise PipelineError(
            "Zero-node JSON evidence no longer matches repository inputs"
        )
    commits = {result["git_commit"] for result in run_results}
    manifests = {
        result["inventory_hashes"]["accepted_manifest_sha256"] for result in run_results
    }
    if len(commits) != 1 or len(manifests) != 1:
        raise PipelineError(
            "Candidate runs did not use one commit and one authorized manifest"
        )

    graph_path = output_dir / "graph.json"
    if not graph_path.is_file():
        raise PipelineError("Candidate graph.json is missing")
    graph_data = read_json(graph_path)
    fingerprints = graph_fingerprints(graph_data)
    derived_validation = validate_derived_outputs(output_dir)
    finalization_path = Path(args.finalization_result)
    finalization = read_json(finalization_path)
    if (
        finalization.get("pipeline_script_sha256")
        != run_results[0]["pipeline_script_sha256"]
        or finalization.get("graphify_version") != SUPPORTED_GRAPHIFY_VERSION
        or finalization.get("source_graph_sha256")
        not in {result["graph_sha256"] for result in run_results}
        or finalization.get("initial_graph_sha256")
        != finalization.get("source_graph_sha256")
        or finalization.get("final_graph_sha256") != sha256_file(graph_path)
        or finalization.get("normalized_graph") != fingerprints
        or finalization.get("derived_validation") != derived_validation
        or finalization.get("cluster_execution", {}).get("exit_code") != 0
        or finalization.get("cluster_execution", {}).get("timed_out")
        or finalization.get("html_execution", {}).get("exit_code") != 0
        or finalization.get("html_execution", {}).get("timed_out")
    ):
        raise PipelineError(
            "Finalization evidence does not match official derived outputs"
        )
    for name, declared in finalization.get("output_hashes", {}).items():
        path = output_dir / name
        if not path.is_file() or declared != {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }:
            raise PipelineError(f"Finalization output hash mismatch: {name}")
    reference = run_results[0]["fingerprints"]
    for key in (
        "node_id_set_sha256",
        "node_content_sha256",
        "relationship_endpoint_type_set_sha256",
        "relationship_content_sha256",
        "normalized_complete_graph_sha256",
    ):
        if fingerprints[key] != reference[key]:
            raise PipelineError(
                f"Final candidate changed normalized graph content after acceptance: {key}"
            )

    direct_outputs = []
    for path in sorted(
        item
        for item in output_dir.iterdir()
        if item.is_file() and item.name != "provenance.json"
    ):
        direct_outputs.append(
            {
                "path": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    provenance = {
        "schema_version": 1,
        "ticket": "GRAPHIFY-SCALE-01",
        "status": "graphify_scalable_hermes_pipeline_ready_with_constraints",
        "git_commit": next(iter(commits)),
        "graphify": {
            "version": SUPPORTED_GRAPHIFY_VERSION,
            "executable": "graphify",
            "selected_path": "Path B",
            "supported_apis": [
                "graphify.detect._load_graphifyignore",
                "graphify.detect._is_ignored",
                "graphify.detect._is_sensitive",
                "graphify.detect.classify_file",
                "graphify.extract.extract",
                "graphify.ids.make_id",
                "graphify.ids.normalize_id",
                "graphify.build.build_from_json",
                "graphify.build.build_merge",
                "graphify.validate.validate_extraction",
                "graphify.export.to_json",
                "graphify.cluster.cluster",
            ],
        },
        "pipeline": {
            "version": PIPELINE_VERSION,
            "script": "10_scripts/graphify/refresh_hermes_graph.py",
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "graphifyignore_sha256": sha256_file(repo_root / ".graphifyignore"),
            "future_refresh_command": (
                "python -B 10_scripts/graphify/refresh_hermes_graph.py run "
                "--repo-root . --output-dir <external-output> --evidence-dir <external-evidence> "
                "--run-id <id> --scope full --cache-mode <cold|warm>"
            ),
        },
        "scope": {
            **run_results[0]["inventory_hashes"],
            "counts": run_results[0]["counts"],
        },
        "batching": {
            "strategy": "lexicographic cache priming followed by one full-corpus official extraction",
            "batch_definition_sha256": run_results[0]["inventory_hashes"][
                "batch_definition_sha256"
            ],
            "batch_count": run_results[0]["counts"]["batches"],
            "cross_batch_relationship_resolution": "full-corpus extract pass",
        },
        "cache_contract": {
            result["run_id"]: {
                "mode": result["cache_mode"],
                "input_sha256": result["cache_input"]["sha256"],
                "output_sha256": result["cache_output"]["sha256"],
                "input_files": result["cache_input"]["file_count"],
                "output_files": result["cache_output"]["file_count"],
                "metrics": result["cache_metrics"],
            }
            for result in run_results
        },
        "determinism": {
            "accepted": True,
            "comparison_sha256": sha256_file(Path(args.comparison)),
            "run_result_sha256": current_run_hashes,
            "equality": comparison["equality"],
            "runs": {
                result["run_id"]: {
                    "cache_mode": result["cache_mode"],
                    "fingerprints": result["fingerprints"],
                    "official_manifest": result["official_manifest"],
                }
                for result in run_results
            },
        },
        "baseline": baseline,
        "performance": {
            result["run_id"]: {
                "duration_seconds": result["duration_seconds"],
                "cpu_seconds": result["cpu_seconds"],
                "peak_memory_bytes": result["peak_memory_bytes"],
                "files_per_second": result["files_per_second"],
                "largest_batch_duration_seconds": result[
                    "largest_batch_duration_seconds"
                ],
                "largest_operation_duration_seconds": result[
                    "largest_operation_duration_seconds"
                ],
            }
            for result in run_results
        },
        "graph": {
            **fingerprints,
            "graph_sha256": sha256_file(graph_path),
            **derived_validation,
        },
        "validation": {result["run_id"]: result["integrity"] for result in run_results},
        "coverage": {
            "parser_failures": 0,
            "zero_node_files": run_results[0]["zero_node_files"],
            "zero_node_file_count": len(run_results[0]["zero_node_files"]),
            "zero_node_json_evidence": run_results[0]["zero_node_evidence"],
            "source_coverage": run_results[0]["source_coverage"],
        },
        "commands": {
            "extraction": "refresh_hermes_graph.py run",
            "clustering": "graphify cluster-only .",
            "html_export": "graphify export html",
        },
        "finalization": {
            "result_sha256": sha256_file(finalization_path),
            "cluster_duration_seconds": finalization["cluster_execution"][
                "duration_seconds"
            ],
            "html_duration_seconds": finalization["html_execution"]["duration_seconds"],
            "visualization_node_limit": finalization["visualization_node_limit"],
            "derived_validation": derived_validation,
        },
        "markdown_boundary": {
            "Hermes_code_AST_refresh": "completed",
            "Hermes_markdown_AST_refresh": "completed_or_supported_subset",
            "Hermes_markdown_semantic_LLM_refresh": "not_performed",
            "repository_markdown_semantic_LLM_refresh": "not_performed",
        },
        "direct_outputs": direct_outputs,
        "known_limitations": [
            "Graphify 0.9.5 is version-pinned because maintained Python APIs are not stability-versioned.",
            "Semantic provider or network-backed extraction is prohibited and was not performed.",
            "Community assignments and HTML layout are derived and excluded from structural determinism hashes.",
        ],
    }
    require_matching_inventory(
        scale_manifest,
        build_inventory(repo_root, "full", int(scale_manifest["batch_size"])),
        "Candidate scale manifest before provenance write",
    )
    require_matching_inventory(
        baseline_scale_manifest,
        build_inventory(
            repo_root, "baseline", int(baseline_scale_manifest["batch_size"])
        ),
        "Baseline scale manifest before provenance write",
    )
    serialized = canonical_json(provenance)
    if str(repo_root).lower() in serialized.lower():
        raise PipelineError("Provenance contains an absolute workspace path")
    write_json(output_dir / "provenance.json", provenance)
    print(sha256_file(output_dir / "provenance.json"))
    return 0


def sanitize_html_title(args: argparse.Namespace) -> int:
    html_path = Path(args.html).resolve()
    text = html_path.read_text(encoding="utf-8")
    match = re.search(r"<title>(.*?)</title>", text, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        raise PipelineError("Official HTML output has no title element")
    title = match.group(1)
    if is_absolute_source(title) or re.search(r"[A-Za-z]:[\\/]", title):
        replacement = f"<title>{args.title}</title>"
        text = text[: match.start()] + replacement + text[match.end() :]
        temporary = html_path.with_name(f".{html_path.name}.{uuid.uuid4().hex}.tmp")
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, html_path)
    final_match = re.search(
        r"<title>(.*?)</title>",
        html_path.read_text(encoding="utf-8"),
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not final_match or re.search(r"[A-Za-z]:[\\/]", final_match.group(1)):
        raise PipelineError("HTML title still contains an absolute Windows path")
    print(sha256_file(html_path))
    return 0


def finalize_candidate(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    source_output = ensure_external(
        repo_root, Path(args.source_output), "accepted run output"
    )
    output_dir = ensure_external(repo_root, Path(args.output_dir), "candidate output")
    evidence_dir = ensure_external(
        repo_root, Path(args.evidence_dir), "finalization evidence"
    )
    ensure_disjoint_paths(source_output, output_dir, evidence_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise PipelineError(f"Final candidate output must start empty: {output_dir}")
    if evidence_dir.exists() and any(evidence_dir.iterdir()):
        raise PipelineError(
            f"Finalization evidence directory must start empty: {evidence_dir}"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for name in ("graph.json", "manifest.json", "scale-manifest.json"):
        source = source_output / name
        if not source.is_file():
            raise PipelineError(f"Accepted run output is missing {name}")
        shutil.copy2(source, output_dir / name)
    graph_path = output_dir / "graph.json"
    initial_fingerprints = graph_fingerprints(read_json(graph_path))
    initial_graph_sha256 = sha256_file(graph_path)
    graphify_executable = shutil.which("graphify")
    if not graphify_executable:
        raise PipelineError("Installed graphify executable was not found on PATH")
    env = sanitized_environment(output_dir, min(os.cpu_count() or 4, 24))
    env["GRAPHIFY_VIZ_NODE_LIMIT"] = str(args.visualization_node_limit)
    deadline = time.perf_counter() + args.timeout

    cluster = run_owned_process(
        [graphify_executable, "cluster-only", "."],
        repo_root,
        env,
        max(1, int(deadline - time.perf_counter())),
        evidence_dir / "cluster-stdout.log",
        evidence_dir / "cluster-stderr.log",
        "cluster-only",
    )
    html = run_owned_process(
        [graphify_executable, "export", "html"],
        repo_root,
        env,
        max(1, int(deadline - time.perf_counter())),
        evidence_dir / "html-stdout.log",
        evidence_dir / "html-stderr.log",
        "html-export",
    )
    sanitize_html_title(
        type(
            "HtmlArgs",
            (),
            {"html": str(output_dir / "graph.html"), "title": args.title},
        )()
    )
    final_fingerprints = graph_fingerprints(read_json(graph_path))
    if any(
        initial_fingerprints[key] != final_fingerprints[key] for key in DETERMINISM_KEYS
    ):
        raise PipelineError(
            "Official clustering/export changed normalized graph semantics"
        )
    derived = validate_derived_outputs(output_dir)
    output_hashes = {
        path.name: {"sha256": sha256_file(path), "bytes": path.stat().st_size}
        for path in sorted(item for item in output_dir.iterdir() if item.is_file())
    }
    result = {
        "schema_version": 1,
        "graphify_version": SUPPORTED_GRAPHIFY_VERSION,
        "pipeline_version": PIPELINE_VERSION,
        "pipeline_script_sha256": sha256_file(Path(__file__).resolve()),
        "source_graph_sha256": sha256_file(source_output / "graph.json"),
        "initial_graph_sha256": initial_graph_sha256,
        "final_graph_sha256": sha256_file(graph_path),
        "normalized_graph": final_fingerprints,
        "cluster_execution": cluster,
        "html_execution": html,
        "visualization_node_limit": args.visualization_node_limit,
        "derived_validation": derived,
        "output_hashes": output_hashes,
    }
    write_json(evidence_dir / "finalization-result.json", result)
    print(canonical_json(derived))
    return 0


PROMOTED_FILES = frozenset(
    {
        ".graphify_labels.json",
        ".graphify_labels.json.sig",
        "GRAPH_REPORT.md",
        "graph.html",
        "graph.json",
        "manifest.json",
        "provenance.json",
        "scale-manifest.json",
    }
)


def promote_candidate(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    source = ensure_external(repo_root, Path(args.candidate_output), "candidate output")
    direct_files = {item.name for item in source.iterdir() if item.is_file()}
    direct_dirs = {item.name for item in source.iterdir() if item.is_dir()}
    if direct_files != PROMOTED_FILES or not direct_dirs.issubset({"cache"}):
        raise PipelineError(
            f"Candidate output tree is not canonical: files={sorted(direct_files)} dirs={sorted(direct_dirs)}"
        )
    snapshot = source.parent / f"validated-candidate-{uuid.uuid4().hex}"
    snapshot.mkdir()
    try:
        for name in sorted(PROMOTED_FILES):
            shutil.copy2(source / name, snapshot / name)
        staged_args = argparse.Namespace(
            **{
                name: getattr(args, name)
                for name in (
                    "repo_root",
                    "backup_output",
                    "run_results",
                    "comparison",
                    "baseline_comparison",
                    "baseline_graph",
                    "baseline_run_result",
                    "finalization_result",
                )
            },
            candidate_output=str(snapshot),
        )
        return _promote_staged_candidate(staged_args)
    finally:
        if snapshot.exists():
            shutil.rmtree(snapshot, ignore_errors=True)


def _promote_staged_candidate(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    current = repo_root / "graphify-out"
    candidate = ensure_external(
        repo_root, Path(args.candidate_output), "candidate output"
    )
    backup = ensure_external(repo_root, Path(args.backup_output), "promotion backup")
    if backup.exists():
        raise PipelineError(f"Promotion backup already exists: {backup}")
    if not current.is_dir():
        raise PipelineError("Current graphify-out directory is missing")
    backup.parent.mkdir(parents=True, exist_ok=True)
    if (
        len(
            {
                os.stat(current).st_dev,
                os.stat(candidate).st_dev,
                os.stat(backup.parent).st_dev,
            }
        )
        != 1
    ):
        raise PipelineError(
            "Atomic promotion requires current, candidate and backup on one filesystem"
        )

    required_files = set(PROMOTED_FILES)
    direct_files = {item.name for item in candidate.iterdir() if item.is_file()}
    direct_dirs = {item.name for item in candidate.iterdir() if item.is_dir()}
    if direct_files != required_files or not direct_dirs.issubset({"cache"}):
        raise PipelineError(
            f"Candidate output tree is not canonical: files={sorted(direct_files)} dirs={sorted(direct_dirs)}"
        )
    validated_snapshot = selected_file_inventory(candidate, required_files)
    html_text = (candidate / "graph.html").read_text(encoding="utf-8")
    title_match = re.search(
        r"<title>(.*?)</title>", html_text, re.DOTALL | re.IGNORECASE
    )
    if not title_match or re.search(r"[A-Za-z]:[\\/]", title_match.group(1)):
        raise PipelineError(
            "Candidate HTML title is missing or contains an absolute path"
        )
    provenance = read_json(candidate / "provenance.json")
    scale_manifest = read_json(candidate / "scale-manifest.json")
    current_inventory = build_inventory(
        repo_root,
        scale_manifest.get("scope", "full"),
        int(scale_manifest.get("batch_size", DEFAULT_BATCH_SIZE)),
    )
    require_matching_inventory(
        scale_manifest, current_inventory, "Candidate scale manifest"
    )
    official_manifest = validate_official_manifest(candidate, current_inventory)
    if (
        provenance.get("status")
        != "graphify_scalable_hermes_pipeline_ready_with_constraints"
    ):
        raise PipelineError("Candidate provenance does not carry the accepted verdict")
    if provenance.get("git_commit") != git_head(repo_root):
        raise PipelineError("Candidate provenance commit does not match HEAD")
    if provenance.get("pipeline", {}).get("script_sha256") != sha256_file(
        Path(__file__).resolve()
    ):
        raise PipelineError(
            "Candidate provenance script hash does not match this pipeline"
        )
    if provenance.get("pipeline", {}).get("graphifyignore_sha256") != sha256_file(
        repo_root / ".graphifyignore"
    ):
        raise PipelineError("Candidate provenance ignore-policy hash does not match")

    evidence_results = [read_json(Path(path)) for path in args.run_results]
    evidence_by_id = verify_run_results(evidence_results)
    ordered_ids = ("cold_run_1", "cold_run_2", "warm_run_1", "warm_run_2")
    evidence_paths = {
        read_json(Path(path))["run_id"]: Path(path) for path in args.run_results
    }
    comparison = read_json(Path(args.comparison))
    evidence_hashes = {
        run_id: sha256_file(evidence_paths[run_id]) for run_id in ordered_ids
    }
    expected_run_fingerprints = {
        run_id: evidence_by_id[run_id]["fingerprints"] for run_id in ordered_ids
    }
    if (
        not comparison.get("accepted")
        or comparison.get("runs") != list(ordered_ids)
        or not all(comparison.get("equality", {}).get(key) for key in DETERMINISM_KEYS)
        or comparison.get("run_result_sha256") != evidence_hashes
        or comparison.get("hashes") != expected_run_fingerprints
    ):
        raise PipelineError("Promotion determinism comparison is not valid")
    determinism = provenance.get("determinism", {})
    expected_determinism_runs = {
        run_id: {
            "cache_mode": evidence_by_id[run_id]["cache_mode"],
            "fingerprints": evidence_by_id[run_id]["fingerprints"],
            "official_manifest": evidence_by_id[run_id]["official_manifest"],
        }
        for run_id in ordered_ids
    }
    if (
        not determinism.get("accepted")
        or determinism.get("comparison_sha256") != sha256_file(Path(args.comparison))
        or determinism.get("run_result_sha256") != evidence_hashes
        or determinism.get("equality") != comparison.get("equality")
        or determinism.get("runs") != expected_determinism_runs
    ):
        raise PipelineError("Candidate provenance does not bind determinism evidence")

    baseline_comparison = read_json(Path(args.baseline_comparison))
    recomputed_baseline = verify_baseline_evidence(
        repo_root,
        Path(args.baseline_graph),
        Path(evidence_by_id["cold_run_1"]["graph_path"]),
        Path(args.baseline_run_result),
        evidence_paths["cold_run_1"],
    )
    baseline_scale_manifest = read_json(
        Path(args.baseline_graph).parent / "scale-manifest.json"
    )
    require_matching_inventory(
        baseline_scale_manifest,
        build_inventory(
            repo_root,
            "baseline",
            int(baseline_scale_manifest["batch_size"]),
        ),
        "Baseline scale manifest",
    )
    if (
        baseline_comparison != recomputed_baseline
        or not recomputed_baseline.get("accepted")
        or provenance.get("baseline") != recomputed_baseline
    ):
        raise PipelineError("Candidate provenance does not bind baseline evidence")
    for field in (
        "accepted_manifest_sha256",
        "ignored_manifest_sha256",
        "sensitive_manifest_sha256",
        "unsupported_manifest_sha256",
        "batch_definition_sha256",
    ):
        if provenance.get("scope", {}).get(field) != scale_manifest.get(field):
            raise PipelineError(f"Candidate provenance scope hash mismatch: {field}")
    graph_path = candidate / "graph.json"
    expected = sha256_file(graph_path)
    graph_fingerprint = graph_fingerprints(read_json(graph_path))
    if provenance.get("graph", {}).get("graph_sha256") != expected:
        raise PipelineError("Candidate provenance graph hash does not match graph.json")
    if any(
        provenance.get("graph", {}).get(key) != graph_fingerprint[key]
        for key in DETERMINISM_KEYS
    ):
        raise PipelineError(
            "Candidate provenance normalized graph hashes do not match graph.json"
        )
    validation = analyze_graph(repo_root, graph_path, scale_manifest)
    if not validation["integrity_passed"]:
        raise PipelineError(
            f"Candidate failed promotion integrity gate: {validation['integrity']}"
        )
    if (
        provenance.get("coverage", {}).get("source_coverage")
        != validation["source_coverage"]
        or provenance.get("coverage", {}).get("zero_node_files")
        != validation["source_coverage"]["accepted_sources_without_nodes"]
    ):
        raise PipelineError("Candidate source coverage is not attested by provenance")
    if provenance.get("coverage", {}).get(
        "zero_node_json_evidence"
    ) != validate_zero_node_sources(
        repo_root,
        validation["source_coverage"]["accepted_sources_without_nodes"],
    ):
        raise PipelineError("Candidate zero-node JSON eligibility is not attested")
    if official_manifest != evidence_by_id["cold_run_1"].get("official_manifest"):
        raise PipelineError("Candidate official manifest differs from accepted runs")
    derived_validation = validate_derived_outputs(candidate)
    if any(
        provenance.get("graph", {}).get(key) != value
        for key, value in derived_validation.items()
    ):
        raise PipelineError(
            "Candidate derived-output validation is not attested by provenance"
        )
    finalization_attestation = provenance.get("finalization", {})
    finalization_path = Path(args.finalization_result)
    finalization_result = read_json(finalization_path)
    if (
        finalization_attestation.get("derived_validation") != derived_validation
        or finalization_attestation.get("result_sha256")
        != sha256_file(finalization_path)
        or finalization_attestation.get("cluster_duration_seconds", 901) > 900
        or finalization_attestation.get("html_duration_seconds", 901) > 900
        or finalization_result.get("pipeline_script_sha256")
        != sha256_file(Path(__file__).resolve())
        or finalization_result.get("graphify_version") != SUPPORTED_GRAPHIFY_VERSION
        or finalization_result.get("source_graph_sha256")
        not in {result["graph_sha256"] for result in evidence_results}
        or finalization_result.get("initial_graph_sha256")
        != finalization_result.get("source_graph_sha256")
        or finalization_result.get("final_graph_sha256") != expected
        or finalization_result.get("normalized_graph") != graph_fingerprint
        or finalization_result.get("derived_validation") != derived_validation
        or finalization_result.get("cluster_execution", {}).get("exit_code") != 0
        or finalization_result.get("cluster_execution", {}).get("timed_out")
        or finalization_result.get("html_execution", {}).get("exit_code") != 0
        or finalization_result.get("html_execution", {}).get("timed_out")
    ):
        raise PipelineError(
            "Candidate official finalization is not attested by provenance"
        )
    for name, declared in finalization_result.get("output_hashes", {}).items():
        path = candidate / name
        if not path.is_file() or declared != {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }:
            raise PipelineError(f"Finalization output hash mismatch: {name}")
    declared_outputs = {
        item["path"]: item for item in provenance.get("direct_outputs", [])
    }
    for name in required_files - {"provenance.json"}:
        path = candidate / name
        declared = declared_outputs.get(name)
        if (
            not declared
            or declared["sha256"] != sha256_file(path)
            or declared["bytes"] != path.stat().st_size
        ):
            raise PipelineError(f"Candidate direct output is not attested: {name}")
    current_tree = directory_inventory(current)
    staging = candidate.parent / f"promotion-{uuid.uuid4().hex}"
    staging.mkdir()
    try:
        for name in sorted(required_files):
            shutil.copy2(candidate / name, staging / name)
        if (
            selected_file_inventory(candidate, required_files) != validated_snapshot
            or selected_file_inventory(staging, required_files) != validated_snapshot
        ):
            raise PipelineError("Candidate changed during promotion staging")
        expected_tree = directory_inventory(staging)
        require_matching_inventory(
            scale_manifest,
            build_inventory(
                repo_root,
                scale_manifest["scope"],
                int(scale_manifest["batch_size"]),
            ),
            "Candidate scale manifest before atomic replacement",
        )
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    moved_current = False
    try:
        os.replace(current, backup)
        moved_current = True
        if directory_inventory(backup)["sha256"] != current_tree["sha256"]:
            raise PipelineError("Promotion backup verification failed")
        os.replace(staging, current)
        if directory_inventory(current)["sha256"] != expected_tree["sha256"]:
            raise PipelineError("Promoted graph verification failed")
        promoted_validation = analyze_graph(
            repo_root,
            current / "graph.json",
            read_json(current / "scale-manifest.json"),
        )
        if (
            not promoted_validation["integrity_passed"]
            or sha256_file(current / "graph.json") != expected
        ):
            raise PipelineError("Promoted output failed final integrity verification")
        require_matching_inventory(
            read_json(current / "scale-manifest.json"),
            build_inventory(
                repo_root,
                scale_manifest["scope"],
                int(scale_manifest["batch_size"]),
            ),
            "Promoted scale manifest",
        )
    except Exception:
        rollback_error = None
        if moved_current:
            try:
                if current.exists():
                    shutil.rmtree(current)
                if backup.exists():
                    os.replace(backup, current)
                if directory_inventory(current)["sha256"] != current_tree["sha256"]:
                    raise PipelineError("Rollback tree hash mismatch")
            except Exception as error:
                rollback_error = error
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        if rollback_error is not None:
            raise PipelineError(
                f"Promotion and rollback both failed: {rollback_error}"
            ) from rollback_error
        raise
    print(expected)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--repo-root", required=True)
    inventory.add_argument("--scope", choices=("baseline", "full"), default="full")
    inventory.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    inventory.add_argument("--evidence-dir", required=True)

    run = subparsers.add_parser("run")
    run.add_argument("--repo-root", required=True)
    run.add_argument("--output-dir", required=True)
    run.add_argument("--evidence-dir", required=True)
    run.add_argument("--run-id", required=True)
    run.add_argument("--scope", choices=("baseline", "full"), default="full")
    run.add_argument("--cache-mode", choices=("cold", "warm"), required=True)
    run.add_argument("--warm-from")
    run.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    run.add_argument("--batch-timeout", type=int, default=DEFAULT_BATCH_TIMEOUT)
    run.add_argument("--pipeline-timeout", type=int, default=DEFAULT_PIPELINE_TIMEOUT)
    run.add_argument("--max-workers", type=int, default=min(os.cpu_count() or 4, 24))

    incremental = subparsers.add_parser("incremental")
    incremental.add_argument("--repo-root", required=True)
    incremental.add_argument("--output-dir", required=True)
    incremental.add_argument("--evidence-dir", required=True)
    incremental.add_argument("--batch-timeout", type=int, default=DEFAULT_BATCH_TIMEOUT)
    incremental.add_argument(
        "--max-workers", type=int, default=min(os.cpu_count() or 4, 24)
    )

    compare = subparsers.add_parser("compare")
    compare.add_argument("--run-results", nargs=4, required=True)
    compare.add_argument("--output", required=True)

    baseline = subparsers.add_parser("compare-baseline")
    baseline.add_argument("--repo-root", required=True)
    baseline.add_argument("--baseline-graph", required=True)
    baseline.add_argument("--candidate-graph", required=True)
    baseline.add_argument("--baseline-run-result", required=True)
    baseline.add_argument("--candidate-run-result", required=True)
    baseline.add_argument("--output", required=True)

    fingerprint = subparsers.add_parser("fingerprint")
    fingerprint.add_argument("--output-dir", required=True)
    fingerprint.add_argument("--output", required=True)

    provenance = subparsers.add_parser("provenance")
    provenance.add_argument("--repo-root", required=True)
    provenance.add_argument("--output-dir", required=True)
    provenance.add_argument("--run-results", nargs=4, required=True)
    provenance.add_argument("--comparison", required=True)
    provenance.add_argument("--baseline-comparison", required=True)
    provenance.add_argument("--baseline-graph", required=True)
    provenance.add_argument("--baseline-run-result", required=True)
    provenance.add_argument("--finalization-result", required=True)

    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--repo-root", required=True)
    finalize.add_argument("--source-output", required=True)
    finalize.add_argument("--output-dir", required=True)
    finalize.add_argument("--evidence-dir", required=True)
    finalize.add_argument("--timeout", type=int, default=900)
    finalize.add_argument("--visualization-node-limit", type=int, default=10000)
    finalize.add_argument("--title", default="graphify - AGENT PLATFORM")

    sanitize_html = subparsers.add_parser("sanitize-html")
    sanitize_html.add_argument("--html", required=True)
    sanitize_html.add_argument("--title", default="graphify - AGENT PLATFORM")

    promote = subparsers.add_parser("promote")
    promote.add_argument("--repo-root", required=True)
    promote.add_argument("--candidate-output", required=True)
    promote.add_argument("--backup-output", required=True)
    promote.add_argument("--run-results", nargs=4, required=True)
    promote.add_argument("--comparison", required=True)
    promote.add_argument("--baseline-comparison", required=True)
    promote.add_argument("--baseline-graph", required=True)
    promote.add_argument("--baseline-run-result", required=True)
    promote.add_argument("--finalization-result", required=True)

    worker = subparsers.add_parser("_worker_extract")
    worker.add_argument("--repo-root", required=True)
    worker.add_argument("--input-list", required=True)
    worker.add_argument("--raw-output", required=True)
    worker.add_argument("--summary-output", required=True)
    worker.add_argument("--failure-ledger", required=True)
    worker.add_argument("--max-workers", type=int, required=True)
    worker.add_argument("--skip-zero-node-audit", action="store_true")
    worker.add_argument("--defer-validation", action="store_true")

    build = subparsers.add_parser("_worker_build")
    build.add_argument("--repo-root", required=True)
    build.add_argument("--raw-input", required=True)
    build.add_argument("--graph-output", required=True)
    build.add_argument("--inventory", required=True)
    build.add_argument("--summary-output", required=True)

    validate = subparsers.add_parser("_worker_validate")
    validate.add_argument("--repo-root", required=True)
    validate.add_argument("--graph", required=True)
    validate.add_argument("--inventory", required=True)
    validate.add_argument("--output", required=True)

    merge = subparsers.add_parser("_worker_merge")
    merge.add_argument("--repo-root", required=True)
    merge.add_argument("--graph", required=True)
    merge.add_argument("--raw-input", required=True)
    merge.add_argument("--changed", required=True)
    merge.add_argument("--deleted", required=True)
    merge.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "inventory":
        evidence = ensure_external(
            Path(args.repo_root).resolve(),
            Path(args.evidence_dir),
            "evidence directory",
        )
        evidence.mkdir(parents=True, exist_ok=True)
        write_inventory(
            evidence, build_inventory(Path(args.repo_root), args.scope, args.batch_size)
        )
        return 0
    if args.command == "run":
        return run_full(args)
    if args.command == "incremental":
        return run_incremental(args)
    if args.command == "compare":
        return compare_runs(args)
    if args.command == "compare-baseline":
        return compare_baseline(args)
    if args.command == "fingerprint":
        return fingerprint_output(args)
    if args.command == "provenance":
        return generate_provenance(args)
    if args.command == "finalize":
        return finalize_candidate(args)
    if args.command == "sanitize-html":
        return sanitize_html_title(args)
    if args.command == "promote":
        return promote_candidate(args)
    if args.command == "_worker_extract":
        return worker_extract(args)
    if args.command == "_worker_build":
        return worker_build(args)
    if args.command == "_worker_validate":
        return worker_validate(args)
    if args.command == "_worker_merge":
        return worker_merge(args)
    raise PipelineError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PipelineError as error:
        print(f"graphify scalable refresh failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
