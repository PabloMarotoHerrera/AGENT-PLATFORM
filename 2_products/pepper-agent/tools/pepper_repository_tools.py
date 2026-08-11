"""Pepper Lead Agent bounded read-only repository context tools."""

from __future__ import annotations

import json
import os
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Any

from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    RuntimePathContainmentError,
    assert_existing_path_contained,
    is_reparse_or_symlink,
    validate_safe_path_segment,
    validate_trusted_base_root,
)
from tools.binary_extensions import has_binary_extension
from tools.registry import registry, tool_error


TOOLSET = "pepper_repository"

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_ROOT_DEFINITIONS: dict[str, tuple[str, str]] = {
    "architecture": (
        "0_architecture",
        "Architecture, roadmap, governance, and project-planning context.",
    ),
    "pepper-agent": (
        "2_products/pepper-agent",
        "Pepper Agent product source, tests, docs, and governance registers.",
    ),
    "siamese-context": (
        "Contexto Módulos Siamese",
        "Read-only Siamese module/business context supplied for Pepper planning.",
    ),
}
_ROOT_ALIASES = {
    "architecture": "architecture",
    "0_architecture": "architecture",
    "pepper-agent": "pepper-agent",
    "pepper_agent": "pepper-agent",
    "product": "pepper-agent",
    "2_products/pepper-agent": "pepper-agent",
    "2_products\\pepper-agent": "pepper-agent",
    "siamese": "siamese-context",
    "siamese-context": "siamese-context",
    "siamese_context": "siamese-context",
    "contexto módulos siamese": "siamese-context",
    "contexto modulos siamese": "siamese-context",
}

_ROOT_ENUM = ["architecture", "pepper-agent", "siamese-context"]
_SEARCH_ROOT_ENUM = ["all", *_ROOT_ENUM]

_DEFAULT_TREE_LIMIT = 100
_MAX_TREE_LIMIT = 300
_DEFAULT_READ_LIMIT = 200
_MAX_READ_LIMIT = 400
_MAX_READ_CHARS = 60_000
_MAX_LINE_CHARS = 2_000
_DEFAULT_SEARCH_LIMIT = 50
_MAX_SEARCH_LIMIT = 100
_MAX_SEARCH_FILE_BYTES = 1_000_000
_MAX_QUERY_CHARS = 400
_MAX_GIT_STATUS_LINES = 200
_MAX_GIT_STATUS_ENTRIES = 80
_MAX_EXCERPT_CHARS = 240
_DEFAULT_AUTHORITY_CANDIDATES = 8
_MAX_AUTHORITY_CANDIDATES = 20
_MAX_AUTHORITY_SCAN_FILES = 600
_MAX_AUTHORITY_FILE_BYTES = 750_000
_AUTHORITY_RESOLUTION_MARGIN = 4
_AUTHORITY_RESOLUTION_MIN_SCORE = 14

_ALWAYS_SKIPPED_DIR_NAMES = frozenset({".git", "graphify-out"})
_DEFAULT_SKIPPED_DIR_NAMES = frozenset(
    {
        ".cache",
        ".mypy_cache",
        ".next",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".turbo",
        ".venv",
        "__pycache__",
        "build",
        "coverage",
        "dist",
        "env",
        "node_modules",
        "out",
        "target",
        "venv",
        "vendor",
    }
)
_SECRET_DIR_NAMES = frozenset({".aws", ".azure", ".gnupg", ".ssh"})
_SECRET_BASENAMES = frozenset(
    {
        ".env",
        ".git-credentials",
        ".netrc",
        "auth.json",
        "cookies.json",
        "cookie.json",
        "credentials.json",
        "credential.json",
        "oauth.json",
        "token.json",
        "tokens.json",
        "storage-state.json",
        "storage_state.json",
    }
)
_SAFE_ENV_EXAMPLE_BASENAMES = frozenset(
    {".env.dist", ".env.example", ".env.sample", ".env.template"}
)
_SECRET_NAME_MARKERS = frozenset(
    {
        "api-key",
        "api_key",
        "apikey",
        "auth-token",
        "auth_token",
        "client-secret",
        "client_secret",
        "cookie",
        "credential",
        "credentials",
        "oauth",
        "private-key",
        "private_key",
        "secret",
        "token",
    }
)
_SECRET_DATA_SUFFIXES = frozenset(
    {
        ".cfg",
        ".conf",
        ".ini",
        ".json",
        ".sqlite",
        ".sqlite3",
        ".toml",
        ".txt",
        ".yaml",
        ".yml",
    }
)
_PRIVATE_KEY_SUFFIXES = frozenset(
    {".key", ".kdbx", ".p12", ".pem", ".pfx", ".ppk"}
)
_READONLY_GIT_COMMANDS = frozenset(
    {
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "--abbrev-ref", "HEAD"),
        ("rev-parse", "HEAD"),
        ("status", "--short", "--branch", "--untracked-files=all"),
    }
)
_GIT_ENV_PASSTHROUGH_KEYS = (
    "COMSPEC",
    "HOME",
    "LANG",
    "LC_ALL",
    "PATH",
    "PATHEXT",
    "Path",
    "SystemRoot",
    "TEMP",
    "TMP",
    "USERPROFILE",
    "WINDIR",
)
_AUTHORITY_CANDIDATE_SUFFIXES = frozenset({".adoc", ".md", ".rst", ".txt"})
_AUTHORITY_COMMON_QUERY_TERMS = frozenset(
    {
        "about",
        "actual",
        "agent",
        "authority",
        "autoridad",
        "canonica",
        "canonico",
        "canonical",
        "current",
        "dime",
        "del",
        "document",
        "documento",
        "el",
        "for",
        "inspecciona",
        "la",
        "los",
        "now",
        "platform",
        "que",
        "repo",
        "repository",
        "source",
        "the",
        "what",
        "which",
    }
)
_CURRENT_INTENT_TERMS = frozenset({"actual", "current", "latest", "now", "active"})
_CANONICAL_INTENT_TERMS = frozenset({"canonica", "canonico", "canonical"})
_AUTHORITY_INTENT_TERMS = frozenset({"authority", "autoridad", "source of truth"})
_CANONICAL_MARKERS = (
    "canonical contract",
    "canonical docs",
    "canonical manual",
    "canonical marker evidence",
    "canonical path",
    "canonical source",
    "canonical work",
    "current canonical",
    "output canonical",
    "source of truth",
)
_AUTHORITY_MARKERS = (
    "authority model",
    "authority statement",
    "authority",
    "decides promotion",
    "governance decides",
    "source of truth",
)
_CURRENTNESS_MARKERS = (
    "accepted sequence after",
    "current canonical",
    "current roadmap",
    "current sequence",
    "current sequencing",
    "inserted project",
    "p18 r",
    "p18.9",
    "post migration",
    "roadmap update owner",
    "sequencing freeze",
    "updated by",
)
_HISTORICAL_DIRECTION_MARKERS = (
    "accepted direction decision",
    "direction only",
    "direction sequence",
    "does not authorize",
    "g 00",
    "g-00",
    "governance direction only",
    "historical",
    "not activation",
    "not implementation",
    "roadmap below is a direction sequence",
)
_NONCANONICAL_MARKERS = (
    "does not create authority",
    "no current canonical",
    "not authority",
    "not canonical",
    "supporting evidence only",
)
_SUPERSEDED_MARKERS = (
    "legacy only",
    "obsolete",
    "retired",
    "superseded",
    "superseded historical",
)
_ROADMAP_DOMAIN_MARKERS = (
    "phase",
    "roadmap",
    "sequencing",
    "work breakdown",
    "work packet",
    "work stream",
    "workstream",
)


class RepositoryAccessError(RuntimeError):
    """Bounded repository access failure safe to surface to the model."""

    def __init__(self, message: str, *, category: str) -> None:
        self.category = category
        super().__init__(message)


def _result(payload: dict[str, Any]) -> str:
    return json.dumps({"success": True, **payload}, ensure_ascii=False)


def _safe_error(exc: Exception) -> str:
    if isinstance(exc, RuntimePathContainmentError):
        return exc.validation_category
    return exc.__class__.__name__


def _int_arg(
    args: dict[str, Any],
    name: str,
    *,
    default: int,
    minimum: int,
    maximum: int,
) -> int:
    try:
        value = int(args.get(name, default))
    except (TypeError, ValueError):
        value = default
    return max(minimum, min(maximum, value))


def _repository_root() -> Path:
    try:
        return validate_trusted_base_root(Path(_REPOSITORY_ROOT))
    except RuntimePathContainmentError as exc:
        raise RepositoryAccessError(
            "AGENT PLATFORM repository root is unavailable",
            category=_safe_error(exc),
        ) from None


def _root_key(raw: Any, *, allow_all: bool = False) -> str:
    value = str(raw or ("all" if allow_all else "pepper-agent")).strip()
    normalized = value.replace("\\", "/").casefold()
    if allow_all and normalized == "all":
        return "all"
    key = _ROOT_ALIASES.get(normalized)
    if key is None:
        allowed = ", ".join(_SEARCH_ROOT_ENUM if allow_all else _ROOT_ENUM)
        raise RepositoryAccessError(
            f"root must be one of: {allowed}",
            category="unknown_root",
        )
    return key


def _allowed_root(repo_root: Path, key: str) -> Path:
    relative, _description = _ROOT_DEFINITIONS[key]
    candidate = repo_root.joinpath(*relative.split("/"))
    try:
        resolved = assert_existing_path_contained(
            candidate,
            containment_root=repo_root,
        )
    except RuntimePathContainmentError as exc:
        raise RepositoryAccessError(
            f"repository root {key!r} is unavailable",
            category=_safe_error(exc),
        ) from None
    if not resolved.is_dir():
        raise RepositoryAccessError(
            f"repository root {key!r} is not a directory",
            category="root_not_directory",
        )
    return resolved


def _available_roots(repo_root: Path) -> list[dict[str, Any]]:
    roots: list[dict[str, Any]] = []
    for key, (relative, description) in _ROOT_DEFINITIONS.items():
        record: dict[str, Any] = {
            "root": key,
            "path": relative,
            "description": description,
            "available": False,
        }
        try:
            resolved = _allowed_root(repo_root, key)
        except RepositoryAccessError as exc:
            record["unavailable_reason"] = exc.category
        else:
            record["available"] = True
            record["type"] = "directory" if resolved.is_dir() else "file"
        roots.append(record)
    return roots


def _relative_parts(raw_path: Any) -> list[str]:
    text = str(raw_path or "").strip().replace("\\", "/")
    if text in {"", "."}:
        return []
    if (
        text.startswith("/")
        or text.startswith("//")
        or (len(text) >= 2 and text[1] == ":")
    ):
        raise RepositoryAccessError(
            "absolute paths are not accepted; use a repository-relative path",
            category="absolute_path",
        )
    parts: list[str] = []
    for raw_segment in text.split("/"):
        if raw_segment in {"", "."}:
            continue
        try:
            parts.append(validate_safe_path_segment(raw_segment))
        except RuntimePathContainmentError as exc:
            raise RepositoryAccessError(
                "path contains an unsafe segment",
                category=_safe_error(exc),
            ) from None
    return parts


def _relative_path(path: Path, root: Path) -> str:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return ""
    text = rel.as_posix()
    return "" if text == "." else text


def _path_policy(
    relative_path: str,
    *,
    is_dir: bool = False,
) -> tuple[bool, str | None, str | None]:
    parts = [part.casefold() for part in relative_path.replace("\\", "/").split("/") if part]
    if not parts:
        return True, None, None
    if any(part in _ALWAYS_SKIPPED_DIR_NAMES for part in parts):
        return (
            False,
            "generated or repository-internal directory is not exposed",
            "generated_or_internal",
        )
    if any(part in _DEFAULT_SKIPPED_DIR_NAMES for part in parts):
        return False, "generated or vendor directory is skipped", "generated_or_vendor"
    if any(part in _SECRET_DIR_NAMES for part in parts):
        return False, "secret-bearing directory is not exposed", "secret_path"

    name = parts[-1]
    suffix = Path(name).suffix.casefold()
    if name in _SECRET_BASENAMES or (
        name.startswith(".env.") and name not in _SAFE_ENV_EXAMPLE_BASENAMES
    ):
        return False, "secret-bearing file is not exposed", "secret_path"
    if suffix in _PRIVATE_KEY_SUFFIXES:
        return False, "private key material is not exposed", "secret_path"
    if suffix in _SECRET_DATA_SUFFIXES and any(
        marker in name for marker in _SECRET_NAME_MARKERS
    ):
        return (
            False,
            "credential, token, OAuth, cookie, or API-key data is not exposed",
            "secret_path",
        )
    if is_dir and name in {
        "auth",
        "browser-auth-state",
        "browser_auth_state",
        "cookies",
        "credential-store",
        "credential_store",
        "credentials",
        "oauth-tokens",
        "oauth_tokens",
        "provider-store",
        "provider_store",
        "secrets",
        "token-store",
        "token_store",
        "tokens",
    }:
        return False, "secret-bearing directory is not exposed", "secret_path"
    return True, None, None


def _resolve_existing_target(
    repo_root: Path,
    root_key: str,
    raw_path: Any,
) -> tuple[Path, Path, str]:
    root = _allowed_root(repo_root, root_key)
    parts = _relative_parts(raw_path)
    candidate = root.joinpath(*parts) if parts else root
    try:
        target = assert_existing_path_contained(candidate, containment_root=root)
    except RuntimePathContainmentError as exc:
        raise RepositoryAccessError(
            "repository path is outside the allowed root or unavailable",
            category=_safe_error(exc),
        ) from None
    rel = _relative_path(target, root)
    allowed, reason, category = _path_policy(rel, is_dir=target.is_dir())
    if not allowed:
        raise RepositoryAccessError(
            reason or "repository path is not exposed",
            category=category or "blocked_path",
        )
    return root, target, rel


def _is_text_file(path: Path) -> bool:
    if has_binary_extension(path.name):
        return False
    try:
        with path.open("rb") as handle:
            sample = handle.read(4096)
    except OSError:
        return False
    return b"\x00" not in sample


def _entry_record(root: Path, entry: Path) -> dict[str, Any]:
    is_dir = entry.is_dir()
    record: dict[str, Any] = {
        "name": entry.name,
        "path": _relative_path(entry, root),
        "type": "directory" if is_dir else "file",
    }
    if not is_dir:
        try:
            record["size_bytes"] = entry.stat().st_size
        except OSError:
            record["size_bytes"] = None
        record["binary_extension"] = has_binary_extension(entry.name)
    return record


def _walk_search_files(root: Path, start: Path) -> tuple[list[Path], dict[str, int]]:
    files: list[Path] = []
    skipped = {
        "redirects": 0,
        "blocked_paths": 0,
        "binary_or_large_files": 0,
        "unreadable_files": 0,
    }
    if start.is_file():
        candidates = [start]
    else:
        candidates = []
        for current, dirnames, filenames in os.walk(start):
            current_path = Path(current)
            kept_dirs: list[str] = []
            for dirname in sorted(dirnames):
                directory = current_path / dirname
                rel = _relative_path(directory, root)
                try:
                    if is_reparse_or_symlink(directory):
                        skipped["redirects"] += 1
                        continue
                    allowed, _reason, _category = _path_policy(rel, is_dir=True)
                except (OSError, RuntimePathContainmentError):
                    skipped["unreadable_files"] += 1
                    continue
                if not allowed:
                    skipped["blocked_paths"] += 1
                    continue
                kept_dirs.append(dirname)
            dirnames[:] = kept_dirs
            for filename in sorted(filenames):
                candidates.append(current_path / filename)
    for candidate in candidates:
        rel = _relative_path(candidate, root)
        try:
            if is_reparse_or_symlink(candidate):
                skipped["redirects"] += 1
                continue
            allowed, _reason, _category = _path_policy(rel, is_dir=False)
            if not allowed:
                skipped["blocked_paths"] += 1
                continue
            if not candidate.is_file() or not _is_text_file(candidate):
                skipped["binary_or_large_files"] += 1
                continue
            if candidate.stat().st_size > _MAX_SEARCH_FILE_BYTES:
                skipped["binary_or_large_files"] += 1
                continue
        except (OSError, RuntimePathContainmentError):
            skipped["unreadable_files"] += 1
            continue
        files.append(candidate)
    return files, skipped


def _run_git_readonly(repo_root: Path, command: tuple[str, ...]) -> dict[str, Any]:
    if command not in _READONLY_GIT_COMMANDS:
        return {"ok": False, "error": "git_command_not_allowlisted"}
    env = {
        key: os.environ[key]
        for key in _GIT_ENV_PASSTHROUGH_KEYS
        if key in os.environ
    }
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        completed = subprocess.run(
            ["git", *command],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            shell=False,
            check=False,
            env=env,
        )
    except Exception as exc:  # noqa: BLE001 - secret-free bounded status only
        return {"ok": False, "error": exc.__class__.__name__}
    stdout = "\n".join(completed.stdout.splitlines()[:_MAX_GIT_STATUS_LINES])
    stderr = "\n".join(completed.stderr.splitlines()[:5])
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }


def _status_allowed_path(path_text: str) -> tuple[bool, str | None, str | None]:
    normalized = path_text.strip().strip('"').replace("\\", "/")
    if normalized.endswith("/"):
        normalized = normalized[:-1]
    for _key, (relative_root, _description) in _ROOT_DEFINITIONS.items():
        root_prefix = relative_root.replace("\\", "/")
        if normalized == root_prefix:
            return True, root_prefix, None
        prefix = f"{root_prefix}/"
        if normalized.startswith(prefix):
            inner = normalized[len(prefix) :]
            allowed, _reason, category = _path_policy(inner)
            return allowed, normalized, category
    return False, None, "outside_allowed_roots"


def _git_snapshot(repo_root: Path) -> dict[str, Any]:
    branch = _run_git_readonly(repo_root, ("rev-parse", "--abbrev-ref", "HEAD"))
    head = _run_git_readonly(repo_root, ("rev-parse", "HEAD"))
    status = _run_git_readonly(
        repo_root,
        ("status", "--short", "--branch", "--untracked-files=all"),
    )
    if not (branch.get("ok") or head.get("ok") or status.get("ok")):
        return {
            "available": False,
            "error": branch.get("error") or head.get("error") or status.get("error"),
        }

    entries: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    skipped = {"outside_allowed_roots": 0, "blocked_paths": 0}
    branch_status = None
    if status.get("ok"):
        for line in str(status.get("stdout") or "").splitlines()[
            :_MAX_GIT_STATUS_LINES
        ]:
            if not line:
                continue
            if line.startswith("##"):
                branch_status = line[2:].strip()
                continue
            code = line[:2]
            path_text = line[3:].strip() if len(line) > 3 else ""
            visible = True
            visible_path = path_text
            for candidate in path_text.split(" -> "):
                candidate_allowed, candidate_path, category = _status_allowed_path(candidate)
                if not candidate_allowed:
                    visible = False
                    if category == "outside_allowed_roots":
                        skipped["outside_allowed_roots"] += 1
                    else:
                        skipped["blocked_paths"] += 1
                    break
                visible_path = candidate_path or visible_path
            if not visible:
                continue
            status_key = code.strip() or code
            counts[status_key] = counts.get(status_key, 0) + 1
            if len(entries) < _MAX_GIT_STATUS_ENTRIES:
                entries.append({"status": code, "path": visible_path})
    return {
        "available": True,
        "read_only": True,
        "shell": False,
        "branch": str(branch.get("stdout") or "").strip() if branch.get("ok") else None,
        "head": str(head.get("stdout") or "").strip()[:40] if head.get("ok") else None,
        "status_branch": branch_status,
        "status_counts": counts,
        "status_entries": entries,
        "status_entry_limit": _MAX_GIT_STATUS_ENTRIES,
        "skipped_status_entries": skipped,
    }


def _normalize_authority_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = re.sub(r"[^a-zA-Z0-9_.-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.casefold()


def _authority_query_profile(query: str) -> dict[str, Any]:
    normalized = _normalize_authority_text(query)
    tokens = [token for token in normalized.split(" ") if token]
    terms = [
        token
        for token in tokens
        if len(token) >= 3 and token not in _AUTHORITY_COMMON_QUERY_TERMS
    ][:16]
    domains: set[str] = set()
    if any(marker in normalized for marker in _ROADMAP_DOMAIN_MARKERS):
        domains.add("roadmap")
    if any(token.startswith("provider") or token in {"auth", "oauth"} for token in tokens):
        domains.add("provider")
    if any(token.startswith("product") or token in {"pepper", "siamese"} for token in tokens):
        domains.add("product")
    if any(token.startswith("runtime") or token in {"execution", "workflow"} for token in tokens):
        domains.add("runtime")
    return {
        "normalized": normalized,
        "terms": terms,
        "domains": sorted(domains),
        "wants_current": any(term in normalized.split(" ") for term in _CURRENT_INTENT_TERMS),
        "wants_canonical": any(term in normalized.split(" ") for term in _CANONICAL_INTENT_TERMS),
        "wants_authority": any(term in normalized for term in _AUTHORITY_INTENT_TERMS),
    }


def _contains_any(normalized_text: str, markers: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for marker in markers:
        normalized_marker = _normalize_authority_text(marker)
        if normalized_marker and normalized_marker in normalized_text:
            found.append(marker)
    return found


def _extract_authority_header(text: str) -> dict[str, str | None]:
    header: dict[str, str | None] = {
        "title": None,
        "ticket": None,
        "status": None,
        "scope": None,
        "authority": None,
        "output": None,
    }
    for raw_line in text.splitlines()[:120]:
        line = raw_line.strip()
        if line.startswith("#") and header["title"] is None:
            header["title"] = line.lstrip("#").strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        field = _normalize_authority_text(cells[0]).replace(" ", "_")
        if field in header and cells[1] and cells[1] != "---":
            header[field] = cells[1]
    return header


def _authority_repository_path(root_key: str, relative_path: str) -> str:
    root_relative, _description = _ROOT_DEFINITIONS[root_key]
    return f"{root_relative}/{relative_path}" if relative_path else root_relative


def _authority_terms_present(
    profile: dict[str, Any],
    *,
    normalized_path: str,
    normalized_title: str,
    normalized_text: str,
) -> tuple[int, list[str], list[str]]:
    score = 0
    evidence: list[str] = []
    matched: list[str] = []
    for term in profile["terms"]:
        if term in normalized_path:
            score += 3
            matched.append(term)
            evidence.append(f"query term {term!r} appears in path")
        elif term in normalized_title:
            score += 2
            matched.append(term)
            evidence.append(f"query term {term!r} appears in title")
        elif term in normalized_text:
            score += 1
            matched.append(term)
    return score, evidence, sorted(set(matched))


def _score_authority_candidate(
    *,
    root_key: str,
    relative_path: str,
    text: str,
    profile: dict[str, Any],
) -> dict[str, Any] | None:
    header = _extract_authority_header(text)
    title = header.get("title") or Path(relative_path).name
    normalized_text = _normalize_authority_text(text)
    normalized_path = _normalize_authority_text(relative_path)
    normalized_title = _normalize_authority_text(title)
    score, evidence, matched_terms = _authority_terms_present(
        profile,
        normalized_path=normalized_path,
        normalized_title=normalized_title,
        normalized_text=normalized_text,
    )

    canonical_markers = _contains_any(normalized_text, _CANONICAL_MARKERS)
    authority_markers = _contains_any(normalized_text, _AUTHORITY_MARKERS)
    current_markers = _contains_any(normalized_text, _CURRENTNESS_MARKERS)
    historical_markers = _contains_any(normalized_text, _HISTORICAL_DIRECTION_MARKERS)
    noncanonical_markers = _contains_any(normalized_text, _NONCANONICAL_MARKERS)
    superseded_markers = _contains_any(normalized_text, _SUPERSEDED_MARKERS)

    specificity_score = 0
    domains = set(profile["domains"])
    basename = _normalize_authority_text(Path(relative_path).name)
    ticket = _normalize_authority_text(header.get("ticket") or "")
    if basename and basename in profile["normalized"]:
        specificity_score += 12
        evidence.append("candidate filename is explicitly named in the query")
    if ticket and ticket in profile["normalized"]:
        specificity_score += 8
        evidence.append("candidate ticket is explicitly named in the query")
    if "roadmap" in domains:
        if "roadmap" in normalized_path:
            specificity_score += 6
            evidence.append("roadmap appears in the candidate path")
        if "work_breakdown" in normalized_path or "work breakdown" in normalized_title:
            specificity_score += 4
            evidence.append("work-breakdown scope appears in path/title")
        if "roadmap generation" in normalized_title:
            specificity_score += 4
            evidence.append("title is a roadmap-generation contract")
        if "accepted sequence after" in normalized_text and "p18.9" in normalized_text:
            specificity_score += 5
            evidence.append("document contains current accepted sequence after P18.R")
    for domain in domains - {"roadmap"}:
        if domain in normalized_path:
            specificity_score += 5
            evidence.append(f"{domain} appears in the candidate path")
        elif domain in normalized_title:
            specificity_score += 4
            evidence.append(f"{domain} appears in the candidate title")
        elif domain in normalized_text:
            specificity_score += 1

    authority_score = 0
    if canonical_markers:
        authority_score += min(8, len(canonical_markers) * 3)
        evidence.append("explicit canonical marker found")
    if authority_markers:
        authority_score += min(6, len(authority_markers) * 2)
        evidence.append("explicit authority/scope marker found")
    if profile["wants_current"] and current_markers:
        authority_score += min(8, len(current_markers) * 2)
        evidence.append("currentness marker found")
    if "p18.9" in normalized_text and "p19" in normalized_text:
        authority_score += 4
        evidence.append("P18.9 and P19 sequencing evidence found")
    if "accepted" in _normalize_authority_text(header.get("status") or "") and (
        canonical_markers or authority_markers
    ):
        authority_score += 1
        evidence.append("accepted status is corroborated by authority markers")

    caution_score = 0
    cautions: list[str] = []
    if superseded_markers:
        caution_score -= 12
        cautions.append("superseded/legacy/retired marker found")
    if noncanonical_markers:
        caution_score -= min(10, len(noncanonical_markers) * 4)
        cautions.append("noncanonical/supporting-only marker found")
    if historical_markers:
        caution_score -= min(9, len(historical_markers) * 2)
        cautions.append("historical or directional-only marker found")
    if domains and not any(domain in normalized_path or domain in normalized_title for domain in domains):
        caution_score -= 2
        cautions.append("domain match is in body only, not path/title")
    if profile["wants_current"] and not current_markers:
        caution_score -= 2
        cautions.append("no explicit currentness marker found")
    if profile["wants_canonical"] and not canonical_markers:
        caution_score -= 2
        cautions.append("no explicit canonical marker found")

    total = score + specificity_score + authority_score + caution_score
    if total <= 0 and not (matched_terms or canonical_markers or authority_markers):
        return None

    if superseded_markers:
        classification = "superseded_or_legacy_authority"
    elif historical_markers and not current_markers:
        classification = "supporting_historical_directional_authority"
    elif historical_markers:
        classification = "supporting_historical_or_mixed_authority"
    elif noncanonical_markers:
        classification = "accepted_supporting_evidence_not_canonical"
    elif canonical_markers or authority_markers:
        classification = "candidate_current_authority"
    elif "accepted" in _normalize_authority_text(header.get("status") or ""):
        classification = "accepted_supporting_evidence_not_canonical"
    else:
        classification = "supporting_evidence"

    return {
        "root": root_key,
        "path": relative_path,
        "repository_path": _authority_repository_path(root_key, relative_path),
        "title": title,
        "ticket": header.get("ticket"),
        "status": header.get("status"),
        "scope": header.get("scope"),
        "authority": header.get("authority"),
        "output": header.get("output"),
        "score": total,
        "base_score": score,
        "specificity_score": specificity_score,
        "authority_score": authority_score,
        "caution_score": caution_score,
        "classification": classification,
        "matched_terms": matched_terms,
        "evidence": evidence[:10],
        "cautions": cautions,
        "canonical_markers": canonical_markers[:5],
        "authority_markers": authority_markers[:5],
        "currentness_markers": current_markers[:5],
        "historical_markers": historical_markers[:5],
        "noncanonical_markers": noncanonical_markers[:5],
    }


def _authority_scan_documents(
    repo_root: Path,
    root_key: str,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    keys = _ROOT_ENUM if root_key == "all" else [root_key]
    documents: list[dict[str, Any]] = []
    skipped = {
        "unavailable_roots": 0,
        "non_authority_suffix": 0,
        "too_large": 0,
        "scan_limit": 0,
        "unreadable_files": 0,
        "redirects": 0,
        "blocked_paths": 0,
        "binary_or_large_files": 0,
    }
    for key in keys:
        try:
            root = _allowed_root(repo_root, key)
        except RepositoryAccessError:
            skipped["unavailable_roots"] += 1
            continue
        files, walk_skipped = _walk_search_files(root, root)
        for name, count in walk_skipped.items():
            skipped[name] = skipped.get(name, 0) + count
        for path in sorted(files, key=lambda item: _relative_path(item, root)):
            if len(documents) >= _MAX_AUTHORITY_SCAN_FILES:
                skipped["scan_limit"] += 1
                continue
            if path.suffix.casefold() not in _AUTHORITY_CANDIDATE_SUFFIXES:
                skipped["non_authority_suffix"] += 1
                continue
            try:
                if path.stat().st_size > _MAX_AUTHORITY_FILE_BYTES:
                    skipped["too_large"] += 1
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                skipped["unreadable_files"] += 1
                continue
            documents.append(
                {
                    "root": key,
                    "path": _relative_path(path, root),
                    "repository_path": _authority_repository_path(key, _relative_path(path, root)),
                    "text": text,
                    "normalized_text": _normalize_authority_text(text),
                }
            )
    return documents, skipped


def _apply_cross_reference_evidence(
    candidates: list[dict[str, Any]],
    documents: list[dict[str, Any]],
) -> None:
    for candidate in candidates:
        basename = _normalize_authority_text(Path(candidate["path"]).name)
        if not basename:
            continue
        ref_count = 0
        current_ref_count = 0
        for document in documents:
            if document["repository_path"] == candidate["repository_path"]:
                continue
            text = str(document.get("normalized_text") or "")
            start = 0
            while True:
                index = text.find(basename, start)
                if index < 0:
                    break
                ref_count += 1
                window = text[max(0, index - 120) : index + len(basename) + 120]
                if _contains_any(window, _CURRENTNESS_MARKERS) or "roadmap source" in window:
                    current_ref_count += 1
                start = index + len(basename)
        if ref_count:
            reference_score = min(4, ref_count) + min(6, current_ref_count * 3)
            candidate["score"] += reference_score
            candidate["cross_reference_count"] = ref_count
            candidate["current_cross_reference_count"] = current_ref_count
            candidate["evidence"].append("referenced elsewhere in approved repository context")
            if current_ref_count:
                candidate["evidence"].append("referenced with currentness markers")
        else:
            candidate["cross_reference_count"] = 0
            candidate["current_cross_reference_count"] = 0


def _resolve_repository_authority_result(
    *,
    query: str,
    root_key: str,
    max_candidates: int,
) -> dict[str, Any]:
    repo_root = _repository_root()
    profile = _authority_query_profile(query)
    documents, skipped = _authority_scan_documents(repo_root, root_key)
    candidates: list[dict[str, Any]] = []
    for document in documents:
        scored = _score_authority_candidate(
            root_key=document["root"],
            relative_path=document["path"],
            text=document["text"],
            profile=profile,
        )
        if scored is not None:
            candidates.append(scored)

    _apply_cross_reference_evidence(candidates, documents)
    candidates.sort(key=lambda item: (-int(item["score"]), item["repository_path"]))
    candidates = candidates[:max_candidates]

    canonical = None
    resolution_state = "insufficient_evidence"
    uncertainty = "No candidate proved current canonical authority."
    if candidates:
        top = candidates[0]
        second_score = int(candidates[1]["score"]) if len(candidates) > 1 else None
        margin = int(top["score"]) - second_score if second_score is not None else None
        top_has_required_markers = bool(top["canonical_markers"] or top["authority_markers"])
        top_has_currentness = bool(
            top["currentness_markers"] or top["current_cross_reference_count"]
        )
        if int(top["score"]) < _AUTHORITY_RESOLUTION_MIN_SCORE or not top_has_required_markers:
            resolution_state = "insufficient_evidence"
            uncertainty = (
                "Top candidate lacks enough explicit authority evidence to claim "
                "current canonical status."
            )
        elif profile["wants_current"] and not top_has_currentness:
            resolution_state = "insufficient_currentness_evidence"
            uncertainty = (
                "Top candidate has authority markers but lacks currentness evidence."
            )
        elif margin is not None and margin < _AUTHORITY_RESOLUTION_MARGIN:
            resolution_state = "ambiguous"
            uncertainty = (
                "Multiple candidates have comparable authority evidence; canonicality "
                "cannot be proven from repository content alone."
            )
        else:
            canonical = dict(top)
            canonical["classification"] = "current_canonical_authority"
            candidates[0] = canonical
            resolution_state = "resolved"
            uncertainty = None

    return {
        "source_tool": "resolve_repository_authority",
        "query": query,
        "root": root_key,
        "resolution_state": resolution_state,
        "canonical": canonical,
        "candidates": candidates,
        "candidate_count": len(candidates),
        "candidate_limit": max_candidates,
        "profile": profile,
        "uncertainty": uncertainty,
        "skipped": skipped,
        "policy": {
            "accepted_alone_is_not_canonical": True,
            "prefer_specific_current_owner_over_broad_historical_direction": True,
            "historical_filename_identity_is_not_authority": True,
            "surviving_old_document_is_not_current_by_survival_alone": True,
            "ambiguity_returns_uncertainty": True,
        },
    }


def _get_repository_context(args: dict[str, Any], **_kwargs) -> str:
    try:
        repo_root = _repository_root()
    except RepositoryAccessError as exc:
        return tool_error(str(exc), category=exc.category)
    return _result(
        {
            "source_tool": "get_repository_context",
            "repository": "AGENT PLATFORM",
            "access_mode": "bounded_read_only",
            "allowed_roots": _available_roots(repo_root),
            "path_output": "repository_relative_only",
            "write_authority": False,
            "shell_authority": False,
            "worker_dispatch_authority": False,
            "git_mutation_authority": False,
            "git_read_only_inspection": _git_snapshot(repo_root),
            "secret_path_policy": {
                "denied": [
                    ".env files",
                    "auth.json",
                    "credential/token/OAuth/API-key/cookie data files",
                    "browser auth state",
                    "private key material",
                    "Git credentials",
                ]
            },
            "skipped_directory_policy": {
                "default_skipped": sorted(
                    _DEFAULT_SKIPPED_DIR_NAMES | _ALWAYS_SKIPPED_DIR_NAMES
                ),
            },
            "authority_resolution_policy": {
                "tool": "resolve_repository_authority",
                "accepted_alone_is_not_canonical": True,
                "compare_scope_authority_currentness_and_specificity": True,
                "prefer_specific_current_owner_over_broad_historical_direction": True,
                "historical_filename_identity_is_not_authority": True,
                "surviving_old_document_is_not_current_by_survival_alone": True,
                "ambiguity_returns_uncertainty": True,
            },
        }
    )


def _list_repository_tree(args: dict[str, Any], **_kwargs) -> str:
    try:
        repo_root = _repository_root()
        root_key = _root_key(args.get("root"))
        root, target, rel = _resolve_existing_target(
            repo_root,
            root_key,
            args.get("path"),
        )
    except RepositoryAccessError as exc:
        return tool_error(str(exc), category=exc.category)
    if not target.is_dir():
        return tool_error("repository path is not a directory", category="not_directory")
    limit = _int_arg(
        args,
        "max_entries",
        default=_DEFAULT_TREE_LIMIT,
        minimum=1,
        maximum=_MAX_TREE_LIMIT,
    )
    entries: list[dict[str, Any]] = []
    skipped = {"redirects": 0, "blocked_paths": 0, "unreadable_entries": 0}
    try:
        children = sorted(target.iterdir(), key=lambda item: item.name.casefold())
    except OSError as exc:
        return tool_error("repository path cannot be listed", category=exc.__class__.__name__)
    truncated = False
    for child in children:
        child_rel = _relative_path(child, root)
        try:
            if is_reparse_or_symlink(child):
                skipped["redirects"] += 1
                continue
            allowed, _reason, _category = _path_policy(child_rel, is_dir=child.is_dir())
            if not allowed:
                skipped["blocked_paths"] += 1
                continue
            if len(entries) >= limit:
                truncated = True
                continue
            entries.append(_entry_record(root, child))
        except (OSError, RuntimePathContainmentError):
            skipped["unreadable_entries"] += 1
    return _result(
        {
            "source_tool": "list_repository_tree",
            "root": root_key,
            "path": rel,
            "entries": entries,
            "entry_count": len(entries),
            "entry_limit": limit,
            "truncated": truncated,
            "skipped": skipped,
        }
    )


def _read_repository_file(args: dict[str, Any], **_kwargs) -> str:
    raw_path = args.get("path")
    if not str(raw_path or "").strip():
        return tool_error("path is required", category="missing_path")
    try:
        repo_root = _repository_root()
        root_key = _root_key(args.get("root"))
        root, target, rel = _resolve_existing_target(repo_root, root_key, raw_path)
    except RepositoryAccessError as exc:
        return tool_error(str(exc), category=exc.category)
    if not target.is_file():
        return tool_error("repository path is not a file", category="not_file")
    if not _is_text_file(target):
        return tool_error(
            "repository file is binary or unsupported for text reads",
            category="binary_file",
        )

    offset = _int_arg(args, "offset", default=1, minimum=1, maximum=1_000_000)
    limit = _int_arg(
        args,
        "limit",
        default=_DEFAULT_READ_LIMIT,
        minimum=1,
        maximum=_MAX_READ_LIMIT,
    )
    lines: list[dict[str, Any]] = []
    chars = 0
    truncated_by_chars = False
    last_line_seen = 0
    try:
        with target.open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, start=1):
                last_line_seen = line_number
                if line_number < offset:
                    continue
                if len(lines) >= limit:
                    break
                text = line.rstrip("\n\r")
                if len(text) > _MAX_LINE_CHARS:
                    text = f"{text[:_MAX_LINE_CHARS]}...[line truncated]"
                addition = len(text) + 16
                if chars + addition > _MAX_READ_CHARS:
                    truncated_by_chars = True
                    break
                lines.append({"line": line_number, "text": text})
                chars += addition
    except OSError as exc:
        return tool_error("repository file cannot be read", category=exc.__class__.__name__)

    next_offset = None
    if lines:
        if truncated_by_chars or len(lines) >= limit:
            next_offset = lines[-1]["line"] + 1
    elif last_line_seen >= offset:
        next_offset = offset
    content = "\n".join(f"{item['line']}: {item['text']}" for item in lines)
    return _result(
        {
            "source_tool": "read_repository_file",
            "root": root_key,
            "path": rel,
            "offset": offset,
            "line_count": len(lines),
            "line_limit": limit,
            "max_chars": _MAX_READ_CHARS,
            "truncated": bool(next_offset),
            "next_offset": next_offset,
            "content": content,
            "lines": lines,
        }
    )


def _search_repository(args: dict[str, Any], **_kwargs) -> str:
    query = str(args.get("query") or "")
    if not query.strip():
        return tool_error("query is required", category="missing_query")
    if len(query) > _MAX_QUERY_CHARS:
        return tool_error("query is too long", category="query_too_long")
    try:
        repo_root = _repository_root()
        root_key = _root_key(args.get("root", "all"), allow_all=True)
    except RepositoryAccessError as exc:
        return tool_error(str(exc), category=exc.category)
    raw_path = args.get("path")
    if root_key == "all" and str(raw_path or "").strip():
        return tool_error(
            "path can only be used with a specific root",
            category="path_requires_specific_root",
        )
    case_sensitive = bool(args.get("case_sensitive", False))
    needle = query if case_sensitive else query.casefold()
    max_matches = _int_arg(
        args,
        "max_matches",
        default=_DEFAULT_SEARCH_LIMIT,
        minimum=1,
        maximum=_MAX_SEARCH_LIMIT,
    )

    search_specs: list[tuple[str, Path, Path, str]] = []
    keys = _ROOT_ENUM if root_key == "all" else [root_key]
    for key in keys:
        try:
            root = _allowed_root(repo_root, key)
            if raw_path:
                _root, start, rel = _resolve_existing_target(
                    repo_root,
                    key,
                    raw_path,
                )
            else:
                start, rel = root, ""
        except RepositoryAccessError:
            continue
        search_specs.append((key, root, start, rel))

    matches: list[dict[str, Any]] = []
    skipped_total = {
        "redirects": 0,
        "blocked_paths": 0,
        "binary_or_large_files": 0,
        "unreadable_files": 0,
    }
    truncated = False
    for key, root, start, _rel in search_specs:
        files, skipped = _walk_search_files(root, start)
        for name, count in skipped.items():
            skipped_total[name] = skipped_total.get(name, 0) + count
        for path in files:
            if len(matches) >= max_matches:
                truncated = True
                break
            try:
                with path.open("r", encoding="utf-8", errors="replace") as handle:
                    for line_number, line in enumerate(handle, start=1):
                        haystack = line if case_sensitive else line.casefold()
                        if needle not in haystack:
                            continue
                        excerpt = line.strip()
                        if len(excerpt) > _MAX_EXCERPT_CHARS:
                            excerpt = (
                                f"{excerpt[:_MAX_EXCERPT_CHARS]}...[line truncated]"
                            )
                        matches.append(
                            {
                                "root": key,
                                "path": _relative_path(path, root),
                                "line": line_number,
                                "excerpt": excerpt,
                            }
                        )
                        if len(matches) >= max_matches:
                            truncated = True
                            break
            except OSError:
                skipped_total["unreadable_files"] += 1
            if truncated:
                break
        if truncated:
            break

    return _result(
        {
            "source_tool": "search_repository",
            "query": query,
            "root": root_key,
            "case_sensitive": case_sensitive,
            "matches": matches,
            "match_count": len(matches),
            "match_limit": max_matches,
            "truncated": truncated,
            "skipped": skipped_total,
        }
    )


def _resolve_repository_authority(args: dict[str, Any], **_kwargs) -> str:
    query = str(args.get("query") or "")
    if not query.strip():
        return tool_error("query is required", category="missing_query")
    if len(query) > _MAX_QUERY_CHARS:
        return tool_error("query is too long", category="query_too_long")
    try:
        root_key = _root_key(args.get("root", "all"), allow_all=True)
        result = _resolve_repository_authority_result(
            query=query,
            root_key=root_key,
            max_candidates=_int_arg(
                args,
                "max_candidates",
                default=_DEFAULT_AUTHORITY_CANDIDATES,
                minimum=1,
                maximum=_MAX_AUTHORITY_CANDIDATES,
            ),
        )
    except RepositoryAccessError as exc:
        return tool_error(str(exc), category=exc.category)
    return _result(result)


_EMPTY_SCHEMA = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}

_ROOT_PROPERTY = {
    "type": "string",
    "enum": _ROOT_ENUM,
    "description": "Allowed repository root to inspect.",
}

_PATH_PROPERTY = {
    "type": "string",
    "description": (
        "Path relative to the selected allowed root. Absolute paths and "
        "traversal are rejected."
    ),
}


registry.register(
    name="get_repository_context",
    toolset=TOOLSET,
    schema={
        "name": "get_repository_context",
        "description": (
            "Read Pepper's bounded AGENT PLATFORM repository context and "
            "read-only Git snapshot."
        ),
        "parameters": _EMPTY_SCHEMA,
    },
    handler=_get_repository_context,
    emoji="R",
    max_result_size_chars=32000,
)

registry.register(
    name="list_repository_tree",
    toolset=TOOLSET,
    schema={
        "name": "list_repository_tree",
        "description": (
            "List one approved repository directory without exposing secrets "
            "or generated/vendor trees."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "root": _ROOT_PROPERTY,
                "path": _PATH_PROPERTY,
                "max_entries": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": _MAX_TREE_LIMIT,
                    "description": "Maximum directory entries to return.",
                },
            },
            "additionalProperties": False,
        },
    },
    handler=_list_repository_tree,
    emoji="L",
    max_result_size_chars=32000,
)

registry.register(
    name="read_repository_file",
    toolset=TOOLSET,
    schema={
        "name": "read_repository_file",
        "description": (
            "Read a bounded text slice from one approved repository file; "
            "no writes or secret paths."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "root": _ROOT_PROPERTY,
                "path": {
                    **_PATH_PROPERTY,
                    "description": "Required path relative to the selected allowed root.",
                },
                "offset": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "1-indexed starting line.",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": _MAX_READ_LIMIT,
                    "description": "Maximum lines to return.",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    handler=_read_repository_file,
    emoji="F",
    max_result_size_chars=70000,
)

registry.register(
    name="search_repository",
    toolset=TOOLSET,
    schema={
        "name": "search_repository",
        "description": (
            "Literal text search across approved repository roots with secret "
            "and generated-path denial."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": _MAX_QUERY_CHARS,
                    "description": "Literal text query. Regular expressions are not evaluated.",
                },
                "root": {
                    "type": "string",
                    "enum": _SEARCH_ROOT_ENUM,
                    "description": "Approved root to search, or all approved roots.",
                },
                "path": _PATH_PROPERTY,
                "max_matches": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": _MAX_SEARCH_LIMIT,
                    "description": "Maximum line matches to return.",
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": "Whether the literal query match is case-sensitive.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    handler=_search_repository,
    emoji="S",
    max_result_size_chars=50000,
)

registry.register(
    name="resolve_repository_authority",
    toolset=TOOLSET,
    schema={
        "name": "resolve_repository_authority",
        "description": (
            "Resolve current canonical repository authority from multiple "
            "candidate governance documents; returns uncertainty when unproven."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": _MAX_QUERY_CHARS,
                    "description": (
                        "Authority question, for example current canonical "
                        "Agent Platform roadmap."
                    ),
                },
                "root": {
                    "type": "string",
                    "enum": _SEARCH_ROOT_ENUM,
                    "description": "Approved root to inspect, or all approved roots.",
                },
                "max_candidates": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": _MAX_AUTHORITY_CANDIDATES,
                    "description": "Maximum authority candidates to return.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    handler=_resolve_repository_authority,
    emoji="A",
    max_result_size_chars=60000,
)
