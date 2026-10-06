"""Offline npm closure verification for retained governed dependency snapshots.

This module never installs dependencies or redirects candidate source lookup.
The receipt lives in node_modules, inside the existing durable snapshot boundary.
"""

import hashlib
import json
from pathlib import Path
import subprocess


class SubstrateError(ValueError):
    """Validation infrastructure is unavailable; no candidate verdict exists."""


def _read(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("not an object")
        return value
    except (OSError, ValueError) as exc:
        raise SubstrateError(f"invalid dependency definition: {path}") from exc


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inside(path, root):
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError, RuntimeError) as exc:
        raise SubstrateError(f"dependency escapes authorized substrate: {path}") from exc


def node_version(node):
    if node is None:
        raise SubstrateError("Node executable unavailable")
    try:
        return subprocess.check_output(
            [str(node), "--version"], text=True, timeout=10,
            stderr=subprocess.PIPE, env=_runtime_environment(),
        ).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise SubstrateError("Node version unavailable") from exc


def _runtime_environment():
    from .validation_command_runner import _minimal_environment

    return _minimal_environment()


def npm_runtime(node, engines):
    """Use the installed npm's own semver implementation, without running npm."""
    npm = Path(node).resolve().parent.parent / "lib/node_modules/npm"
    script = (
        "const fs=require('fs');const p=process.argv[1];"
        "const semver=require(p+'/node_modules/semver');"
        "const ranges=JSON.parse(process.argv[2]);"
        "if(!ranges.every(r=>semver.satisfies(process.version,r)))process.exit(2);"
        "console.log(JSON.parse(fs.readFileSync(p+'/package.json','utf8')).version);"
    )
    if not npm.is_dir():
        npm = Path(node).resolve().parent / "node_modules/npm"  # Windows distribution
    try:
        return subprocess.check_output(
            [str(node), "-e", script, str(npm), json.dumps(engines)],
            text=True, stderr=subprocess.PIPE, timeout=10, env=_runtime_environment(),
        ).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise SubstrateError("npm runtime unavailable or Node incompatible with locked engines") from exc


def _dependencies(package, *, development=False):
    result = dict(package.get("dependencies", {}))
    if development:
        result.update(package.get("devDependencies", {}))
    optional = set(package.get("optionalDependencies", {}))
    result.update(package.get("optionalDependencies", {}))
    result.update(package.get("peerDependencies", {}))
    optional.update(
        name for name, meta in package.get("peerDependenciesMeta", {}).items()
        if meta.get("optional")
    )
    return [(name, name in optional) for name in sorted(result)]


def _resolve(packages, origin, name):
    if not name or ".." in name.split("/") or name.startswith(("/", "\\")):
        raise SubstrateError("invalid dependency name")
    current = Path(origin)
    while True:
        rel = (current / "node_modules" / name).as_posix()
        if rel in packages:
            return rel
        if current == Path("."):
            break
        current = current.parent
    return None


def inspect(source, package_rel, node):
    """Check every installed package reachable from the npm workspace lock."""
    package = source / package_rel
    definition = _read(package / "package.json")
    _inside(package / "package.json", source)
    if not _dependencies(definition, development=True):
        return None  # CLI-only packages retain the existing CLI readiness check.
    root = package
    while not (root / "package-lock.json").is_file():
        if root == source or root == root.parent:
            raise SubstrateError("npm lockfile required for declared dependencies")
        root = root.parent
    _inside(root, source)
    _inside(root / "package.json", source)
    _inside(root / "package-lock.json", source)
    root_definition = _read(root / "package.json")
    manager = root_definition.get("packageManager", "npm")
    if manager != "npm" and not str(manager).startswith("npm@"):
        raise SubstrateError("dependency package manager is not npm")
    lock = _read(root / "package-lock.json")
    if lock.get("lockfileVersion") not in (2, 3):
        raise SubstrateError("unsupported npm lockfile")
    packages = lock.get("packages", {})
    if not isinstance(packages, dict) or any(
        not isinstance(value, dict) or Path(key).is_absolute()
        or ".." in key.split("/") or "\\" in key or ":" in key
        for key, value in packages.items()
    ):
        raise SubstrateError("invalid lockfile package paths")
    if any(
        value.get("link") and value.get("resolved") not in packages
        for value in packages.values()
    ):
        raise SubstrateError("linked package absent from lock authority")
    origin = package.relative_to(root).as_posix()
    origin = "" if origin == "." else origin
    for key, actual in (("", root_definition), (origin, definition)):
        locked = packages.get(key)
        if not isinstance(locked, dict):
            raise SubstrateError(f"package definition absent from lock: {key}")
        for field in ("dependencies", "devDependencies", "optionalDependencies"):
            if actual.get(field, {}) != locked.get(field, {}):
                raise SubstrateError(f"package/lock mismatch: {key} {field}")
    pending = [(origin, name, optional) for name, optional in _dependencies(definition, development=True)]
    visited = {}
    engines = [p["engines"]["node"] for p in (definition, root_definition) if p.get("engines", {}).get("node")]
    while pending:
        parent, name, optional = pending.pop()
        rel = _resolve(packages, parent, name)
        if rel is None:
            if optional:
                continue
            raise SubstrateError(f"dependency missing from lock: {name}")
        if rel in visited:
            continue
        entry = packages[rel]
        manifest = root / rel / "package.json"
        if not manifest.is_file() and optional:
            continue
        if not manifest.is_file():
            raise SubstrateError(f"installed dependency missing: {rel}")
        _inside(manifest, source)
        lookup = root / parent
        while True:
            resolved = lookup / "node_modules" / name / "package.json"
            if resolved.exists():
                if resolved.resolve() != manifest.resolve():
                    raise SubstrateError(f"installed dependency shadows locked resolution: {name}")
                break
            if lookup == root:
                break
            lookup = lookup.parent
        installed = _read(manifest)
        target = entry.get("resolved") if entry.get("link") else rel
        locked = packages.get(target, {}) if entry.get("link") else entry
        if installed.get("version") != locked.get("version"):
            raise SubstrateError(f"installed dependency version differs from lock: {rel}")
        visited[rel] = _digest(manifest)
        if locked.get("engines", {}).get("node"):
            engines.append(locked["engines"]["node"])
        pending.extend((str(target), child, opt) for child, opt in _dependencies(locked))
    version = node_version(node)
    npm_version = npm_runtime(node, sorted(set(engines)))
    if manager != "npm" and manager != f"npm@{npm_version}":
        raise SubstrateError("installed npm version differs from packageManager")
    return {
        "schema_version": 1,
        "package_relative_path": package_rel,
        "root_relative_path": root.relative_to(source).as_posix(),
        "package_manager": manager,
        "node_version": version,
        "npm_version": npm_version,
        "definitions": {
            f.relative_to(source).as_posix(): _digest(f)
            for f in (package / "package.json", root / "package.json", root / "package-lock.json")
        },
        "packages": visited,
    }


def receipt_path(workspace, package_rel):
    return workspace / package_rel / "node_modules/.pepper-validation-substrate.json"


def verify(workspace, package_rel, node):
    """Recheck retained identity immediately before a governed command."""
    definition = _read(workspace / package_rel / "package.json")
    if not _dependencies(definition, development=True) and not receipt_path(workspace, package_rel).exists():
        return
    _inside(receipt_path(workspace, package_rel), workspace)
    receipt = _read(receipt_path(workspace, package_rel))
    actual = inspect(workspace, package_rel, node)
    if receipt != actual:
        raise SubstrateError("retained npm dependency identity changed")
