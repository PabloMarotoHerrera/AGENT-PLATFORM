"""Pepper product runtime adapters for controlled default mode.

This module is intentionally a thin projection layer. It reuses Hermes staged
write approvals and Kanban run evidence, and it exposes bounded product shapes
for the dashboard without creating a second approval engine, executor, review
engine, or Git authority path.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import re
import time
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


APPROVAL_SOURCE_SYSTEM = "hermes-write-approval"
CONTROLLED_EXECUTION_SOURCE_SYSTEM = "pepper-controlled-execution"
CONTROLLED_CUTOVER_SCHEMA_VERSION = 1
P18_7_COMMIT = "661f1362a7d019c1629e73ad04e4a70e966e394c"
P18_7_RESULT_SHA256 = (
    "c71eaf7711ad59855be33eca067c7cfe4bf0bbfa2d4f898d4190a1ed82cac263"
)
P18_7_MIGRATION_GAP_DIGEST = (
    "18f484479ca97179ba5996cf673296df5bdc6816e782ca37cf78e6c141cecd68"
)
PEPPER_GOVERNED_PRODUCT_ID = "pepper"
PEPPER_GOVERNED_PROJECT_ID = "PEPPER"
PEPPER_GOVERNED_PROJECT_NAME = "Pepper"
PEPPER_COMPLETED_MACROPROJECT_ID = "P18"
PEPPER_COMPLETED_MACROPROJECT_TITLE = "Manual-to-Hermes Workflow Migration"
PEPPER_GOVERNED_MACROPROJECT_ID = "P18.9"
PEPPER_GOVERNED_MACROPROJECT_TITLE = "Pepper Product Personalization"
PEPPER_CURRENT_TICKET_ID = None
PEPPER_CURRENT_TICKET_TITLE = None
PEPPER_CURRENT_GAP_ID = None
PEPPER_CURRENT_GAP_TITLE = None
PEPPER_NEXT_TICKET_ID = "P18.9.0"
PEPPER_NEXT_TICKET_TITLE = "Product UX / IA Baseline"
PEPPER_WORKFLOW_CONTEXT_SOURCE_SYSTEM = "pepper-lead-agent-governed-context"

_ACTIVE_EXECUTION_STATUSES = frozenset({"running"})
_TERMINAL_EXECUTION_STATUSES = frozenset({
    "blocked",
    "cancelled",
    "completed",
    "crashed",
    "done",
    "failed",
    "reclaimed",
    "spawn_failed",
    "timed_out",
})

_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SAFE_BOARD = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_SAFE_TASK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SAFE_PROFILE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class ProductRuntimeError(ValueError):
    """Base error for product runtime projection failures."""


class ProductRuntimeNotFound(ProductRuntimeError):
    """Raised when a requested source-local object does not exist."""


class ProductRuntimeConflict(ProductRuntimeError):
    """Raised when a source-local identifier is ambiguous."""


class ProductRuntimeDecisionFailed(ProductRuntimeError):
    """Raised when an approval decision cannot be applied safely."""


class ApprovalDecisionRequest(BaseModel):
    """Dashboard request body for a human approval decision."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    decision: Literal["approve", "reject"]
    actor: str = Field(default="pepper-dashboard-human", min_length=1, max_length=128)

    @field_validator("actor")
    @classmethod
    def actor_must_be_safe(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("actor contains control characters")
        return value


class ControlledExecutionStartRequest(BaseModel):
    """Dashboard request body for a controlled execution preparation."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    board_slug: str = Field(min_length=1, max_length=64)
    task_id: str = Field(min_length=1, max_length=128)
    profile: str | None = Field(default=None, max_length=128)
    dispatch: Literal[False] = False

    @field_validator("board_slug")
    @classmethod
    def board_slug_must_be_safe(cls, value: str) -> str:
        candidate = value.strip().lower()
        if not _SAFE_BOARD.fullmatch(candidate):
            raise ValueError("invalid board slug")
        return candidate

    @field_validator("task_id")
    @classmethod
    def task_id_must_be_safe(cls, value: str) -> str:
        if not _SAFE_TASK.fullmatch(value):
            raise ValueError("invalid task id")
        return value

    @field_validator("profile")
    @classmethod
    def profile_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not _SAFE_PROFILE.fullmatch(value):
            raise ValueError("invalid profile")
        return value


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_text(value: object, *, limit: int = 4000) -> str:
    text = str(value or "").replace("\r", "\n")
    text = _CONTROL_CHARS.sub("", text).strip()
    return text[:limit] or "not supplied"


def _safe_id(value: object) -> str:
    text = str(value or "").strip()
    if not _SAFE_ID.fullmatch(text):
        raise ProductRuntimeNotFound("invalid source-local identifier")
    return text


def _next_action_label(next_action: Any) -> str:
    if isinstance(next_action, dict):
        return _safe_text(next_action.get("label"), limit=300)
    return _safe_text(next_action, limit=300)


def _approval_count(source: dict[str, Any]) -> int:
    approvals = source.get("approvals") if isinstance(source, dict) else []
    return len(approvals) if isinstance(approvals, list) else 0


def _approval_state(count: int) -> str:
    return "pending_approvals" if count > 0 else "no_pending_approvals"


def _execution_is_active(record: dict[str, Any]) -> bool:
    status = str(record.get("status") or "").strip().lower()
    if status in _ACTIVE_EXECUTION_STATUSES:
        return True
    if status in _TERMINAL_EXECUTION_STATUSES:
        return False
    return record.get("ended_at") is None and bool(status)


def _execution_counts(source: dict[str, Any]) -> tuple[int, int]:
    executions = source.get("executions") if isinstance(source, dict) else []
    if not isinstance(executions, list):
        return 0, 0
    active = sum(
        1 for record in executions
        if isinstance(record, dict) and _execution_is_active(record)
    )
    return len(executions), active


def _execution_state(active_count: int) -> str:
    return "active_executions" if active_count > 0 else "no_active_executions"


def _approval_operational_summary() -> dict[str, Any]:
    try:
        source = build_approval_inbox_source()
    except Exception as exc:  # pragma: no cover - defensive live-source guard
        return {
            "approval_state": "unavailable",
            "pending_approval_count": None,
            "source_system": APPROVAL_SOURCE_SYSTEM,
            "error": _safe_text(exc, limit=300),
        }
    count = _approval_count(source)
    return {
        "approval_state": _approval_state(count),
        "pending_approval_count": count,
        "source_system": source.get("source_system", APPROVAL_SOURCE_SYSTEM),
    }


def _execution_operational_summary() -> dict[str, Any]:
    try:
        source = build_execution_collection_source()
    except Exception as exc:  # pragma: no cover - defensive live-source guard
        return {
            "execution_state": "unavailable",
            "execution_count": None,
            "active_execution_count": None,
            "source_system": CONTROLLED_EXECUTION_SOURCE_SYSTEM,
            "error": _safe_text(exc, limit=300),
        }
    total, active = _execution_counts(source)
    return {
        "execution_state": _execution_state(active),
        "execution_count": total,
        "active_execution_count": active,
        "source_system": source.get("source_system", CONTROLLED_EXECUTION_SOURCE_SYSTEM),
    }


def _subsystems() -> tuple[str, ...]:
    from tools import write_approval as wa

    return (wa.MEMORY, wa.SKILLS)


def _approval_title(record: dict[str, Any]) -> str:
    subsystem = _safe_text(record.get("subsystem"), limit=32)
    action = _safe_text(record.get("action"), limit=64)
    return f"Review staged {subsystem} write: {action}"


def _approval_target(record: dict[str, Any]) -> dict[str, str]:
    subsystem = record.get("subsystem")
    if subsystem == "skills":
        return {"type": "filesystem_action", "label": "Skill file write"}
    if subsystem == "memory":
        return {"type": "configuration_action", "label": "Memory store write"}
    return {"type": "other_source_action", "label": "Staged source write"}


def _approval_summary(record: dict[str, Any]) -> dict[str, Any]:
    approval_id = _safe_id(record.get("id"))
    subsystem = _safe_text(record.get("subsystem"), limit=32)
    action = _safe_text(record.get("action"), limit=64)
    summary = _safe_text(record.get("summary"), limit=4000)
    created_at = record.get("created_at")
    requested_at = float(created_at) if isinstance(created_at, (int, float)) else 0.0
    return {
        "id": approval_id,
        "semantics": "explicit_approval_request",
        "title": _approval_title(record),
        "summary": summary,
        "status": "pending",
        "request_type": f"{subsystem}_write",
        "requested_at": requested_at,
        "expires_at": None,
        "requester": _safe_text(record.get("origin"), limit=128),
        "risk_label": "medium" if subsystem == "skills" else "low",
        "target": _approval_target(record),
        "reason": (
            "A durable Hermes staged-write record requires an explicit human "
            f"decision before applying action {action!r}."
        ),
    }


def build_approval_inbox_source() -> dict[str, Any]:
    """Return the bounded live approval inbox source for the active profile."""

    from tools import write_approval as wa

    approvals: list[dict[str, Any]] = []
    for subsystem in _subsystems():
        for record in wa.list_pending(subsystem):
            approvals.append(_approval_summary(record))
    return {
        "source_system": APPROVAL_SOURCE_SYSTEM,
        "source_authority": "durable-hermes-staged-write-store",
        "canonical_approval_authority": "pepper-controlled-human-decision-v1",
        "approvals": approvals,
    }


def _find_pending(approval_id: str) -> tuple[str, dict[str, Any]]:
    from tools import write_approval as wa

    approval_id = _safe_id(approval_id)
    matches: list[tuple[str, dict[str, Any]]] = []
    for subsystem in _subsystems():
        record = wa.get_pending(subsystem, approval_id)
        if record:
            matches.append((subsystem, record))
    if not matches:
        raise ProductRuntimeNotFound("approval not found")
    if len(matches) > 1:
        raise ProductRuntimeConflict("approval id is ambiguous across subsystems")
    return matches[0]


def build_approval_detail_source(approval_id: str) -> dict[str, Any]:
    """Return one bounded approval detail source by source-local id."""

    subsystem, record = _find_pending(approval_id)
    summary = _approval_summary(record)
    evidence = [
        {
            "id": f"{summary['id']}:summary",
            "label": f"{subsystem} staged write summary retained in durable pending store",
        },
        {
            "id": f"{summary['id']}:origin",
            "label": f"source origin: {_safe_text(record.get('origin'), limit=128)}",
        },
    ]
    return {
        "source_system": APPROVAL_SOURCE_SYSTEM,
        "source_authority": "durable-hermes-staged-write-store",
        "canonical_approval_authority": "pepper-controlled-human-decision-v1",
        "approval": summary,
        "evidence": evidence,
        "decisions": [],
    }


def apply_approval_decision(
    approval_id: str,
    request: ApprovalDecisionRequest,
) -> dict[str, Any]:
    """Apply a human approval decision through the existing write gate."""

    from tools import write_approval as wa

    subsystem, record = _find_pending(approval_id)
    if request.decision == "reject":
        if not wa.discard_pending(subsystem, approval_id):
            raise ProductRuntimeNotFound("approval not found")
        return {
            "source_system": APPROVAL_SOURCE_SYSTEM,
            "id": approval_id,
            "decision": "reject",
            "status": "rejected",
            "actor": request.actor,
            "decided_at": time.time(),
            "applied": True,
        }

    payload = record.get("payload", {})
    try:
        if subsystem == wa.MEMORY:
            from tools.memory_tool import apply_memory_pending, load_on_disk_store

            result = apply_memory_pending(payload, load_on_disk_store())
        else:
            from tools.skill_manager_tool import apply_skill_pending

            result = json.loads(apply_skill_pending(payload))
    except Exception as exc:  # pragma: no cover - defensive source adapter guard
        raise ProductRuntimeDecisionFailed("approval application failed") from exc

    if not bool(result.get("success")):
        raise ProductRuntimeDecisionFailed(_safe_text(result.get("error"), limit=300))
    wa.discard_pending(subsystem, approval_id)
    return {
        "source_system": APPROVAL_SOURCE_SYSTEM,
        "id": approval_id,
        "decision": "approve",
        "status": "approved",
        "actor": request.actor,
        "decided_at": time.time(),
        "applied": True,
    }


def _run_dict(run: Any) -> dict[str, Any]:
    return {
        "id": int(run.id),
        "task_id": run.task_id,
        "profile": run.profile,
        "step_key": run.step_key,
        "status": run.status,
        "claim_lock": None,
        "claim_expires": None,
        "worker_pid": None,
        "max_runtime_seconds": run.max_runtime_seconds,
        "last_heartbeat_at": run.last_heartbeat_at,
        "started_at": run.started_at,
        "ended_at": run.ended_at,
        "outcome": run.outcome,
        "summary": run.summary,
        "metadata": None,
        "error": run.error,
    }


def _task_dict(task: Any) -> dict[str, Any]:
    data = asdict(task)
    for field in (
        "workspace_path",
        "claim_lock",
        "worker_pid",
        "last_failure_error",
        "model_override",
        "result",
    ):
        data.pop(field, None)
    return data


def _event_dict(event: Any) -> dict[str, Any]:
    return {
        "id": event.id,
        "task_id": event.task_id,
        "kind": event.kind,
        "payload": None,
        "created_at": event.created_at,
        "run_id": event.run_id,
    }


def _attachment_dict(attachment: Any) -> dict[str, Any]:
    return {
        "id": attachment.id,
        "task_id": attachment.task_id,
        "filename": attachment.filename,
        "content_type": attachment.content_type,
        "size": attachment.size,
        "uploaded_by": attachment.uploaded_by,
        "stored_path": None,
        "created_at": attachment.created_at,
    }


def _normalize_board(board_slug: str | None) -> str:
    from hermes_cli import kanban_db

    try:
        board = kanban_db._normalize_board_slug(board_slug or kanban_db.DEFAULT_BOARD)
    except ValueError as exc:
        raise ProductRuntimeNotFound("invalid board") from exc
    if not board:
        raise ProductRuntimeNotFound("invalid board")
    if board != kanban_db.DEFAULT_BOARD and not kanban_db.board_exists(board):
        raise ProductRuntimeNotFound("board not found")
    return board


def build_task_execution_source(board_slug: str, task_id: str) -> dict[str, Any]:
    """Return the existing task-nested execution evidence through product API."""

    from hermes_cli import kanban_db

    board = _normalize_board(board_slug)
    if not _SAFE_TASK.fullmatch(task_id):
        raise ProductRuntimeNotFound("invalid task id")
    kanban_db.init_db(board=board)
    conn = kanban_db.connect(board=board)
    try:
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            raise ProductRuntimeNotFound("task not found")
        links = {"parents": [], "children": []}
        return {
            "task": _task_dict(task),
            "comments": [],
            "events": [_event_dict(event) for event in kanban_db.list_events(conn, task_id)],
            "attachments": [
                _attachment_dict(attachment)
                for attachment in kanban_db.list_attachments(conn, task_id)
            ],
            "links": links,
            "child_results": [],
            "runs": [_run_dict(run) for run in kanban_db.list_runs(conn, task_id)],
            "control": _execution_control_fields(board, task_id, task.status),
        }
    finally:
        conn.close()


def _execution_control_fields(board_slug: str, task_id: str, status: str) -> dict[str, Any]:
    next_action = "review_execution"
    if status in {"todo", "ready", "scheduled"}:
        next_action = "start_controlled_execution"
    elif status == "review":
        next_action = "perform_review_validation"
    elif status == "done":
        next_action = "prepare_human_git_handoff"
    return {
        "workflow_state": status,
        "work_packet_id": f"WP-{board_slug.upper()}-{task_id.upper()}",
        "validation_state": "visible_in_execution_detail",
        "review_state": "visible_in_execution_detail",
        "git_handoff_state": "human_git_authority_preserved",
        "next_action": next_action,
    }


def build_execution_collection_source(
    *,
    max_records: int = 500,
) -> dict[str, Any]:
    """Return a bounded universal execution collection over Kanban run facts."""

    from hermes_cli import kanban_db

    records: list[dict[str, Any]] = []
    for board_meta in kanban_db.list_boards(include_archived=False):
        board = _normalize_board(str(board_meta.get("slug") or kanban_db.DEFAULT_BOARD))
        kanban_db.init_db(board=board)
        conn = kanban_db.connect(board=board)
        try:
            tasks = kanban_db.list_tasks(conn, include_archived=False)
            for task in tasks:
                for run in kanban_db.list_runs(conn, task.id):
                    control = _execution_control_fields(board, task.id, task.status)
                    records.append({
                        "id": int(run.id),
                        "board_slug": board,
                        "task_id": task.id,
                        "task_title": "Source task title withheld by the execution projection",
                        "profile": run.profile,
                        "status": run.status,
                        "outcome": run.outcome,
                        "started_at": run.started_at,
                        "ended_at": run.ended_at,
                        **control,
                    })
        finally:
            conn.close()
    records.sort(key=lambda item: (item["started_at"], item["id"]), reverse=True)
    return {
        "source_system": CONTROLLED_EXECUTION_SOURCE_SYSTEM,
        "schema_version": CONTROLLED_CUTOVER_SCHEMA_VERSION,
        "collection_scope": "universal",
        "observed_at": int(time.time() * 1000),
        "executions": records[:max_records],
        "manual_opencode_copy_required": False,
        "human_git_authority": "preserved",
    }


def ensure_execution_exists(board_slug: str, task_id: str, execution_id: str) -> dict[str, Any]:
    source = build_task_execution_source(board_slug, task_id)
    requested = int(execution_id) if str(execution_id).isdigit() else -1
    if not any(int(run.get("id", -1)) == requested for run in source.get("runs", [])):
        raise ProductRuntimeNotFound("execution not found")
    return source


def prepare_controlled_execution(
    request: ControlledExecutionStartRequest,
) -> dict[str, Any]:
    """Prepare a controlled worker handoff without dispatching a provider call."""

    source = build_task_execution_source(request.board_slug, request.task_id)
    task = source["task"]
    prompt = "\n".join((
        f"Board: {request.board_slug}",
        f"Task: {request.task_id}",
        f"Title: {_safe_text(task.get('title'), limit=300)}",
        "Produce a bounded implementation result for Pepper controlled default mode.",
    ))
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    request_id = f"p18-8-{digest[:24]}"
    return {
        "source_system": CONTROLLED_EXECUTION_SOURCE_SYSTEM,
        "schema_version": CONTROLLED_CUTOVER_SCHEMA_VERSION,
        "state": "prepared",
        "dispatch_performed": False,
        "request_id": request_id,
        "runtime_id": "pepper-controlled-default-mode",
        "correlation_id": f"{request.board_slug}:{request.task_id}",
        "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
        "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
        "request_user_content_sha256": digest,
        "accepted_substrate": [
            "build_provider_worker_gate_request",
            "run_controlled_worker_request",
            "run_openai_codex_single_dispatch",
            "prepare_single_agent_execution",
            "execute_single_agent_tool_action",
            "complete_single_agent_execution",
        ],
        "manual_opencode_ticket_copy_required": False,
        "manual_opencode_result_copy_required": False,
        "human_git_authority": "preserved",
        "next_action": "dispatch requires an explicit governed worker operation outside tests",
    }


def build_workflow_control_snapshot() -> dict[str, Any]:
    """Return the controlled cutover dashboard projection."""

    approval_summary = _approval_operational_summary()
    execution_summary = _execution_operational_summary()
    closed_gaps = [
        {
            "id": "P18-8-GAP-001",
            "status": "closed_by_live_product_approval_api",
            "evidence": "/api/agent-platform/approvals list detail and decision routes",
        },
        {
            "id": "P18-8-GAP-002",
            "status": "closed_by_live_product_execution_api",
            "evidence": "/api/agent-platform/executions collection detail and start preparation routes",
        },
        {
            "id": "P18-8-GAP-003",
            "status": "closed_by_workflow_control_projection",
            "evidence": "/api/agent-platform/workflow-control next action and default-mode posture",
        },
        {
            "id": "P18-8-GAP-004",
            "status": "closed_by_p15_p17_worker_handoff_projection",
            "evidence": "controlled worker request preparation removes normal OpenCode copy transfer",
        },
        {
            "id": "P18-8-GAP-005",
            "status": "closed_by_human_pepper_chat_workflow_context_smoke",
            "evidence": "HUMAN_P18_8_CUTOVER_SMOKE_PASS",
        },
    ]
    remaining_blockers: list[dict[str, Any]] = []
    historical_evidence = [
        {
            "id": "P18.8",
            "title": "Controlled Default-Mode Cutover",
            "state": "completed",
            "evidence": "HUMAN_P18_8_CUTOVER_SMOKE_PASS",
        },
        {
            "id": "P18.R",
            "title": "Workflow Migration Closure",
            "state": "closed",
            "decision": "accepted",
            "evidence": "docs/agent-platform/workflow_migration_closure.md",
        },
    ]
    next_action = {
        "id": "GENERATE_P18_9_0",
        "label": "Generate governed P18.9.0 Product UX / IA Baseline before execution.",
        "target_ticket_id": PEPPER_NEXT_TICKET_ID,
        "target_ticket_title": PEPPER_NEXT_TICKET_TITLE,
    }
    observed_at = _utc_now_iso()
    return {
        "schema_version": CONTROLLED_CUTOVER_SCHEMA_VERSION,
        "source_system": "pepper-controlled-default-mode-cutover",
        "product_id": PEPPER_GOVERNED_PRODUCT_ID,
        "project_id": PEPPER_GOVERNED_PROJECT_ID,
        "project_name": PEPPER_GOVERNED_PROJECT_NAME,
        "macroproject_id": PEPPER_GOVERNED_MACROPROJECT_ID,
        "macroproject_title": PEPPER_GOVERNED_MACROPROJECT_TITLE,
        "completed_macroproject_id": PEPPER_COMPLETED_MACROPROJECT_ID,
        "completed_macroproject_title": PEPPER_COMPLETED_MACROPROJECT_TITLE,
        "completed_macroproject_state": "closed",
        "completed_macroproject_decision": "accepted",
        "current_ticket_id": PEPPER_CURRENT_TICKET_ID,
        "current_ticket_title": PEPPER_CURRENT_TICKET_TITLE,
        "current_gap_id": PEPPER_CURRENT_GAP_ID,
        "current_gap_title": PEPPER_CURRENT_GAP_TITLE,
        "next_ticket_id": PEPPER_NEXT_TICKET_ID,
        "next_ticket_title": PEPPER_NEXT_TICKET_TITLE,
        "mode": "controlled_default",
        "readiness": "planning_approved_or_intake_ready",
        "workflow_state": "P18.9-PEPPER-PRODUCT-PERSONALIZATION-INTAKE-READY",
        "workflow_status": "planning_approved_or_intake_ready",
        "approval_state": approval_summary["approval_state"],
        "pending_approval_count": approval_summary["pending_approval_count"],
        "queue_state": "ready_to_generate_P18_9_0",
        "execution_state": execution_summary["execution_state"],
        "active_execution_count": execution_summary["active_execution_count"],
        "validation_state": "not_started_no_ticket_generated",
        "review_state": "not_started_no_ticket_generated",
        "recovery_state": "not_required",
        "git_handoff_state": "human_git_authority_preserved",
        "blocker_count": len(remaining_blockers),
        "warning_count": 0,
        "ready_verdict": (
            "p18_closed_and_p18_9_personalization_intake_ready_with_no_active_ticket_"
            "and_preserved_human_git_authority"
        ),
        "p18_7_commit": P18_7_COMMIT,
        "p18_7_result_sha256": P18_7_RESULT_SHA256,
        "p18_7_migration_gap_digest": P18_7_MIGRATION_GAP_DIGEST,
        "normal_control_surface": "pepper-dashboard-agent-platform",
        "manual_chat_control_required": False,
        "manual_opencode_ticket_copy_required": False,
        "manual_opencode_result_copy_required": False,
        "human_git_authority": "preserved_manual_git_add_commit_push_only",
        "automatic_git_add": False,
        "automatic_git_commit": False,
        "automatic_git_push": False,
        "closed_gaps": closed_gaps,
        "historical_evidence": historical_evidence,
        "remaining_blockers": remaining_blockers,
        "default_mode_enabled": True,
        "ready_requires_human_smoke": False,
        "human_cutover_smoke": "HUMAN_P18_8_CUTOVER_SMOKE_PASS",
        "workflow_migration_complete": True,
        "P18_closed": True,
        "P18_state": "closed",
        "P18_decision": "accepted",
        "P18_R_closed": True,
        "P18_R_state": "closed",
        "P18_R_decision": "accepted",
        "P18_R_pending": False,
        "P18_9_ready": True,
        "P18_9_ticket_generated": False,
        "next_action": next_action,
        "next_action_label": _next_action_label(next_action),
        "evidence_timestamp": observed_at,
        "evidence_version": CONTROLLED_CUTOVER_SCHEMA_VERSION,
        "observed_at": observed_at,
    }


def _workflow_value(workflow: dict[str, Any], key: str, fallback: Any = None) -> Any:
    value = workflow.get(key) if isinstance(workflow, dict) else None
    return fallback if value in {None, ""} else value


def _workflow_ticket(workflow: dict[str, Any]) -> dict[str, Any]:
    ticket_id = _workflow_value(workflow, "current_ticket_id")
    ticket_title = _workflow_value(workflow, "current_ticket_title")
    return {
        "available": bool(ticket_id),
        "current_ticket_id": ticket_id,
        "current_ticket_title": ticket_title,
        "current_gap_id": _workflow_value(workflow, "current_gap_id"),
        "current_gap_title": _workflow_value(workflow, "current_gap_title"),
        "message": "active governed ticket" if ticket_id else "no active governed ticket",
        "next_action": workflow.get("next_action"),
    }


def build_lead_agent_operational_context() -> dict[str, Any]:
    """Return Pepper's bounded live operational context for Lead Agent tools.

    This is a projection over the same live state sources the dashboard uses:
    workflow-control, staged-write approvals, controlled execution records, and
    Kanban board/task facts. It is intentionally read-only and creates no new
    workflow, approval, execution, queue, review, recovery, Git, or memory store.
    """

    workflow = build_workflow_control_snapshot()
    approvals_source = build_approval_inbox_source()
    executions_source = build_execution_collection_source()
    pending_approval_count = _approval_count(approvals_source)
    execution_count, active_execution_count = _execution_counts(executions_source)
    ticket = _workflow_ticket(workflow)
    next_action = workflow.get("next_action")
    evidence_timestamp = _safe_text(
        workflow.get("evidence_timestamp") or workflow.get("observed_at") or _utc_now_iso(),
        limit=64,
    )

    return {
        "schema_version": CONTROLLED_CUTOVER_SCHEMA_VERSION,
        "source_system": PEPPER_WORKFLOW_CONTEXT_SOURCE_SYSTEM,
        "source_authority": "product_runtime_live_projection",
        "product_id": _workflow_value(workflow, "product_id", PEPPER_GOVERNED_PRODUCT_ID),
        "project_id": _workflow_value(workflow, "project_id", PEPPER_GOVERNED_PROJECT_ID),
        "project_name": _workflow_value(workflow, "project_name", PEPPER_GOVERNED_PROJECT_NAME),
        "macroproject_id": _workflow_value(
            workflow, "macroproject_id", PEPPER_GOVERNED_MACROPROJECT_ID
        ),
        "macroproject_title": _workflow_value(
            workflow, "macroproject_title", PEPPER_GOVERNED_MACROPROJECT_TITLE
        ),
        **ticket,
        "workflow_state": _workflow_value(workflow, "workflow_state", workflow.get("mode")),
        "workflow_status": _workflow_value(workflow, "workflow_status", workflow.get("readiness")),
        "approval_state": _approval_state(pending_approval_count),
        "pending_approval_count": pending_approval_count,
        "queue_state": _workflow_value(workflow, "queue_state", "unavailable"),
        "execution_state": _execution_state(active_execution_count),
        "execution_count": execution_count,
        "active_execution_count": active_execution_count,
        "validation_state": _workflow_value(workflow, "validation_state", "unavailable"),
        "review_state": _workflow_value(workflow, "review_state", "unavailable"),
        "recovery_state": _workflow_value(workflow, "recovery_state", "unavailable"),
        "git_handoff_state": _workflow_value(workflow, "git_handoff_state", "unavailable"),
        "blocker_count": len(workflow.get("remaining_blockers") or []),
        "warning_count": int(workflow.get("warning_count") or 0),
        "next_action": next_action,
        "next_action_label": _next_action_label(next_action),
        "evidence_timestamp": evidence_timestamp,
        "evidence_version": CONTROLLED_CUTOVER_SCHEMA_VERSION,
        "workflow_control": workflow,
        "approvals": {
            "source_system": approvals_source.get("source_system", APPROVAL_SOURCE_SYSTEM),
            "pending_approval_count": pending_approval_count,
            "items": approvals_source.get("approvals", []),
        },
        "executions": {
            "source_system": executions_source.get(
                "source_system", CONTROLLED_EXECUTION_SOURCE_SYSTEM
            ),
            "execution_count": execution_count,
            "active_execution_count": active_execution_count,
            "items": executions_source.get("executions", []),
        },
        "duplicate_workflow_context_store_created": False,
        "duplicate_next_action_engine_created": False,
        "duplicate_approval_state_created": False,
        "duplicate_execution_state_created": False,
        "GBrain_calls": 0,
        "auto_approval": False,
        "auto_execution": False,
        "auto_retry": False,
        "auto_rollback": False,
        "Git_mutation": False,
        "external_dashboard_state_copy_required": False,
        "external_ChatGPT_required": False,
    }
