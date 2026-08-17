"""Pepper governed WorkPacket write confinement for file tools.

The model-facing ``file`` tools stay generic. This module only activates when
the process is explicitly running as a Pepper governed Kanban worker and then
maps WorkPacket repository-relative scope onto the active worker workspace.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping


GOVERNED_WORKER_ENV = "HERMES_AGENT_PLATFORM_GOVERNED_WORKER"
GOVERNED_WORKER_MODE = "pepper-kanban-worker"

WORKPACKET_ID_ENV = "HERMES_AGENT_PLATFORM_WORKPACKET_ID"
WORKPACKET_SHA256_ENV = "HERMES_AGENT_PLATFORM_WORKPACKET_SHA256"
TICKET_SPEC_SHA256_ENV = "HERMES_AGENT_PLATFORM_TICKET_SPEC_SHA256"
KANBAN_PROJECTION_SHA256_ENV = "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_SHA256"
GENERATION_RECORD_PATH_ENV = "HERMES_AGENT_PLATFORM_GENERATION_RECORD_PATH"
APPROVAL_DECISION_RECORD_PATH_ENV = "HERMES_AGENT_PLATFORM_APPROVAL_DECISION_RECORD_PATH"
KANBAN_PROJECTION_RECORD_PATH_ENV = "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_RECORD_PATH"

WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE = "WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE"
WORKPACKET_WRITE_PATH_DENIED = "WORKPACKET_WRITE_PATH_DENIED"
WORKPACKET_FORBIDDEN_PATH = "WORKPACKET_FORBIDDEN_PATH"
WORKSPACE_PATH_ESCAPE = "WORKSPACE_PATH_ESCAPE"
WORKPACKET_PATCH_ATOMICITY_DENIED = "WORKPACKET_PATCH_ATOMICITY_DENIED"

_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")
_PROTECTED_PATHS = (
    ".git/**",
    ".opencode/**",
    ".agents/**",
    "AGENTS.md",
    "graphify-out/**",
    "4_external/sources/**",
    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
)
_PROTECTED_COMPONENTS = frozenset({"node_modules"})
_PROTECTED_FILENAMES = frozenset({"package-lock.json"})


@dataclass(frozen=True)
class WorkPacketFileAuthority:
    ticket_id: str
    work_packet_id: str
    work_packet_SHA256: str
    ticket_spec_SHA256: str
    projection_SHA256: str
    allowed_paths: tuple[str, ...]
    forbidden_paths: tuple[str, ...]
    workspace_root: Path
    resolved_workspace_root: Path
    generation_record_path: Path | None = None
    approval_decision_record_path: Path | None = None
    kanban_projection_record_path: Path | None = None


@dataclass(frozen=True)
class WorkPacketWriteDenial:
    code: str
    path: str
    detail: str
    matched_pattern: str | None = None

    def format(self) -> str:
        message = f"{self.code}: {self.detail}"
        if self.path:
            message += f" path={self.path!r}"
        if self.matched_pattern:
            message += f" matched_pattern={self.matched_pattern!r}"
        return message


class WorkPacketAuthorityUnavailable(ValueError):
    pass


def governed_worker_enabled(env: Mapping[str, str] | None = None) -> bool:
    raw = str((env or os.environ).get(GOVERNED_WORKER_ENV, "") or "")
    return raw.strip().lower().replace("_", "-") == GOVERNED_WORKER_MODE


def governed_write_denial(
    path: str,
    *,
    resolved_path: str | Path | None = None,
    env: Mapping[str, str] | None = None,
) -> str | None:
    """Return a denial string for one write target, or ``None`` when allowed.

    Non-governed Hermes sessions preserve existing behavior and return ``None``.
    Governed workers fail closed if the WorkPacket authority cannot be resolved.
    """

    runtime_env = env or os.environ
    if not governed_worker_enabled(runtime_env):
        return None
    try:
        authority = resolve_governed_workpacket_file_authority(runtime_env)
    except WorkPacketAuthorityUnavailable as exc:
        return f"{WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE}: {exc}"
    denial = evaluate_write_target(
        authority,
        path,
        resolved_path=resolved_path,
    )
    return denial.format() if denial else None


def governed_patch_denial(
    paths: list[str] | tuple[str, ...],
    *,
    resolved_paths: Mapping[str, str | Path | None] | None = None,
    env: Mapping[str, str] | None = None,
) -> str | None:
    """Return a patch-level denial before any backend mutation occurs."""

    runtime_env = env or os.environ
    if not governed_worker_enabled(runtime_env):
        return None
    try:
        authority = resolve_governed_workpacket_file_authority(runtime_env)
    except WorkPacketAuthorityUnavailable as exc:
        return f"{WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE}: {exc}"
    resolved_paths = resolved_paths or {}
    for path in paths:
        denial = evaluate_write_target(
            authority,
            path,
            resolved_path=resolved_paths.get(path),
        )
        if denial:
            return (
                f"{WORKPACKET_PATCH_ATOMICITY_DENIED}: patch contains an "
                f"unauthorized mutation target; {denial.format()}. "
                "No files were modified."
            )
    return None


def resolve_governed_workpacket_file_authority(
    env: Mapping[str, str] | None = None,
) -> WorkPacketFileAuthority:
    runtime_env = env or os.environ
    required = (
        WORKPACKET_ID_ENV,
        WORKPACKET_SHA256_ENV,
        TICKET_SPEC_SHA256_ENV,
        KANBAN_PROJECTION_SHA256_ENV,
        GENERATION_RECORD_PATH_ENV,
        APPROVAL_DECISION_RECORD_PATH_ENV,
        KANBAN_PROJECTION_RECORD_PATH_ENV,
    )
    values = {key: str(runtime_env.get(key, "") or "").strip() for key in required}
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise WorkPacketAuthorityUnavailable("missing governed WorkPacket context: " + ",".join(missing))
    for key in (WORKPACKET_SHA256_ENV, TICKET_SPEC_SHA256_ENV, KANBAN_PROJECTION_SHA256_ENV):
        if not _DIGEST_RE.fullmatch(values[key].lower()):
            raise WorkPacketAuthorityUnavailable(f"{key} is invalid")

    workspace_root = _workspace_root(runtime_env)
    generation_path = _authority_record_path(values[GENERATION_RECORD_PATH_ENV], GENERATION_RECORD_PATH_ENV)
    approval_path = _authority_record_path(
        values[APPROVAL_DECISION_RECORD_PATH_ENV],
        APPROVAL_DECISION_RECORD_PATH_ENV,
    )
    projection_path = _authority_record_path(
        values[KANBAN_PROJECTION_RECORD_PATH_ENV],
        KANBAN_PROJECTION_RECORD_PATH_ENV,
    )

    try:
        generation_record = _read_json_record(generation_path)
        approval_record = _read_json_record(approval_path)
        projection_record = _read_json_record(projection_path)
        from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
            validate_approval_decision_record,
            validate_generation_record,
        )
        from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
            validate_kanban_projection_record,
        )

        generation = validate_generation_record(generation_record)
        ticket_id = str(generation.get("ticket_id") or "").strip()
        if not ticket_id:
            raise WorkPacketAuthorityUnavailable("generated ticket is unavailable")
        decision = validate_approval_decision_record(
            approval_record,
            ticket_id=ticket_id,
            generation_record=generation,
        )
        projection = validate_kanban_projection_record(
            projection_record,
            ticket_id=ticket_id,
            generation_record=generation,
            decision_record=decision,
        )
    except WorkPacketAuthorityUnavailable:
        raise
    except Exception as exc:
        raise WorkPacketAuthorityUnavailable("persisted WorkPacket authority is invalid") from exc

    if projection.get("ticket_id") != ticket_id:
        raise WorkPacketAuthorityUnavailable("projection ticket mismatch")
    if generation.get("work_packet_id") != values[WORKPACKET_ID_ENV]:
        raise WorkPacketAuthorityUnavailable("WorkPacket ID mismatch")
    if generation.get("work_packet_SHA256") != values[WORKPACKET_SHA256_ENV].lower():
        raise WorkPacketAuthorityUnavailable("WorkPacket digest mismatch")
    if projection.get("work_packet_id") != values[WORKPACKET_ID_ENV]:
        raise WorkPacketAuthorityUnavailable("projection WorkPacket ID mismatch")
    if projection.get("work_packet_SHA256") != values[WORKPACKET_SHA256_ENV].lower():
        raise WorkPacketAuthorityUnavailable("projection WorkPacket digest mismatch")
    if projection.get("ticket_spec_SHA256") != values[TICKET_SPEC_SHA256_ENV].lower():
        raise WorkPacketAuthorityUnavailable("projection TicketSpec digest mismatch")
    if projection.get("projection_SHA256") != values[KANBAN_PROJECTION_SHA256_ENV].lower():
        raise WorkPacketAuthorityUnavailable("projection digest mismatch")

    scope = _repository_scope_from_generation(generation)
    allowed = tuple(str(item).strip() for item in scope.get("allowed_paths") or () if str(item).strip())
    forbidden = tuple(str(item).strip() for item in scope.get("forbidden_paths") or () if str(item).strip())
    if not allowed:
        raise WorkPacketAuthorityUnavailable("WorkPacket allowed paths are unavailable")
    return WorkPacketFileAuthority(
        ticket_id=ticket_id,
        work_packet_id=values[WORKPACKET_ID_ENV],
        work_packet_SHA256=values[WORKPACKET_SHA256_ENV].lower(),
        ticket_spec_SHA256=values[TICKET_SPEC_SHA256_ENV].lower(),
        projection_SHA256=values[KANBAN_PROJECTION_SHA256_ENV].lower(),
        allowed_paths=allowed,
        forbidden_paths=forbidden,
        workspace_root=workspace_root,
        resolved_workspace_root=workspace_root.resolve(strict=True),
        generation_record_path=generation_path,
        approval_decision_record_path=approval_path,
        kanban_projection_record_path=projection_path,
    )


def evaluate_write_target(
    authority: WorkPacketFileAuthority,
    path: str,
    *,
    resolved_path: str | Path | None = None,
) -> WorkPacketWriteDenial | None:
    raw = str(path or "")
    if not raw.strip() or _CONTROL_RE.search(raw):
        return WorkPacketWriteDenial(
            WORKPACKET_WRITE_PATH_DENIED,
            raw,
            "mutation target path is invalid",
        )
    if _has_parent_traversal(raw):
        return WorkPacketWriteDenial(
            WORKSPACE_PATH_ESCAPE,
            raw,
            "mutation target contains parent traversal",
        )
    try:
        target = Path(resolved_path) if resolved_path is not None else Path(raw)
        if not target.is_absolute():
            target = authority.workspace_root / target
        resolved_target = target.resolve(strict=False)
        relative = resolved_target.relative_to(authority.resolved_workspace_root)
    except (OSError, RuntimeError, ValueError) as exc:
        return WorkPacketWriteDenial(
            WORKSPACE_PATH_ESCAPE,
            raw,
            f"mutation target escapes the governed worker workspace ({exc})",
        )
    relative_text = relative.as_posix()
    if not relative_text or relative_text == "." or _has_parent_traversal(relative_text):
        return WorkPacketWriteDenial(
            WORKPACKET_WRITE_PATH_DENIED,
            raw,
            "mutation target is not a repository-relative file path",
        )
    protected_component = _first_protected_component(relative_text)
    if protected_component is not None:
        return WorkPacketWriteDenial(
            WORKPACKET_FORBIDDEN_PATH,
            raw,
            "mutation target is forbidden by governed dependency substrate policy",
            matched_pattern=protected_component,
        )
    forbidden = _first_matching_pattern(relative_text, (*_PROTECTED_PATHS, *authority.forbidden_paths))
    if forbidden is not None:
        return WorkPacketWriteDenial(
            WORKPACKET_FORBIDDEN_PATH,
            raw,
            "mutation target is forbidden by WorkPacket scope",
            matched_pattern=forbidden,
        )
    allowed = _first_matching_pattern(relative_text, authority.allowed_paths)
    if allowed is None:
        return WorkPacketWriteDenial(
            WORKPACKET_WRITE_PATH_DENIED,
            raw,
            "mutation target is not included in WorkPacket allowed paths",
        )
    return None


def _workspace_root(env: Mapping[str, str]) -> Path:
    raw = str(env.get("HERMES_KANBAN_WORKSPACE") or env.get("TERMINAL_CWD") or "").strip()
    if not raw:
        raise WorkPacketAuthorityUnavailable("governed worker workspace is unavailable")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise WorkPacketAuthorityUnavailable("governed worker workspace is not absolute")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise WorkPacketAuthorityUnavailable("governed worker workspace cannot be resolved") from exc
    if not resolved.is_dir():
        raise WorkPacketAuthorityUnavailable("governed worker workspace is not a directory")
    return path


def _authority_record_path(value: str, key: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise WorkPacketAuthorityUnavailable(f"{key} is not absolute")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise WorkPacketAuthorityUnavailable(f"{key} cannot be resolved") from exc
    if not resolved.is_file():
        raise WorkPacketAuthorityUnavailable(f"{key} is not a file")
    return path


def _read_json_record(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("authority record must be an object")
    return data


def _repository_scope_from_generation(generation: dict[str, Any]) -> dict[str, Any]:
    compilation = generation.get("work_packet_compilation_result")
    if not isinstance(compilation, dict):
        raise WorkPacketAuthorityUnavailable("WorkPacket compilation result is unavailable")
    packet = compilation.get("work_packet")
    if not isinstance(packet, dict):
        raise WorkPacketAuthorityUnavailable("WorkPacket record is unavailable")
    scope = packet.get("repository_scope")
    if not isinstance(scope, dict):
        raise WorkPacketAuthorityUnavailable("WorkPacket repository scope is unavailable")
    return scope


def _has_parent_traversal(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(part == ".." for part in normalized.split("/"))


def _first_protected_component(path: str) -> str | None:
    parts = tuple(part.casefold() for part in path.replace("\\", "/").split("/") if part)
    if any(part in _PROTECTED_COMPONENTS for part in parts):
        return "node_modules/**"
    if parts and parts[-1] in _PROTECTED_FILENAMES:
        return parts[-1]
    return None


def _first_matching_pattern(path: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        if _matches_pattern(path, pattern):
            return pattern
    return None


def _matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        base = pattern[:-3]
        return path == base or path.startswith(f"{base}/")
    return path == pattern


__all__ = [
    "APPROVAL_DECISION_RECORD_PATH_ENV",
    "GENERATION_RECORD_PATH_ENV",
    "GOVERNED_WORKER_ENV",
    "GOVERNED_WORKER_MODE",
    "KANBAN_PROJECTION_RECORD_PATH_ENV",
    "KANBAN_PROJECTION_SHA256_ENV",
    "TICKET_SPEC_SHA256_ENV",
    "WORKPACKET_FORBIDDEN_PATH",
    "WORKPACKET_ID_ENV",
    "WORKPACKET_PATCH_ATOMICITY_DENIED",
    "WORKPACKET_SHA256_ENV",
    "WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE",
    "WORKPACKET_WRITE_PATH_DENIED",
    "WORKSPACE_PATH_ESCAPE",
    "WorkPacketFileAuthority",
    "WorkPacketWriteDenial",
    "evaluate_write_target",
    "governed_patch_denial",
    "governed_worker_enabled",
    "governed_write_denial",
    "resolve_governed_workpacket_file_authority",
]
