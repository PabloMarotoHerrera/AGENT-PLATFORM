"""Pepper product runtime adapters for controlled default mode.

This module is intentionally a thin projection layer. It reuses Hermes staged
write approvals and Kanban run evidence, and it exposes bounded product shapes
for the dashboard without creating a second approval engine, executor, review
engine, or Git authority path.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
import re
import time
import unicodedata
from pathlib import Path
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
PEPPER_BOOTSTRAP_NEXT_TICKET_ID = "P18.9.0"
PEPPER_BOOTSTRAP_NEXT_TICKET_TITLE = "Product Inventory, IA Decision, and Acceptance Contract"
PEPPER_NEXT_TICKET_ID = PEPPER_BOOTSTRAP_NEXT_TICKET_ID
PEPPER_NEXT_TICKET_TITLE = PEPPER_BOOTSTRAP_NEXT_TICKET_TITLE
PEPPER_WORKFLOW_CONTEXT_SOURCE_SYSTEM = "pepper-lead-agent-governed-context"
PEPPER_CURRENT_EXECUTION_RECOVERY_NEXT_ACTION_ID = "RECOVER_P18_9_0_EXECUTION"
PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT = (
    "Autorizo explícitamente la recuperación de la ejecución fallida de P18.9.0."
)
PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM = "pepper-worker-start-action"
PEPPER_WORKER_START_ACTION_SCHEMA_VERSION = 1
PEPPER_WORKER_START_ACTION_POLICY_ID = "pepper-worker-start-action-v1"
PEPPER_WORKER_START_AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-worker-start-authorization-sha256-v1"
)
PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM = "pepper-recovery-action"
PEPPER_RECOVERY_ACTION_SCHEMA_VERSION = 1
PEPPER_RECOVERY_ACTION_POLICY_ID = "pepper-p18-9-0-recovery-action-v1"
PEPPER_RECOVERY_ACTION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-recovery-action-sha256-v1"
)
PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM = "pepper-retry-start-action"
PEPPER_RETRY_START_ACTION_SCHEMA_VERSION = 1
PEPPER_RETRY_START_ACTION_POLICY_ID = "pepper-p18-9-0-retry-start-action-v1"
PEPPER_RETRY_START_ACTION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-retry-start-action-sha256-v1"
)
PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM = "pepper-review-prepare-action"
PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION = 1
PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID = "pepper-p18-9-0-review-prepare-action-v1"
PEPPER_REVIEW_PREPARE_ACTION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-review-prepare-action-sha256-v1"
)
PEPPER_REVIEW_PREPARE_PACKAGE_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-review-package-sha256-v1"
)
PEPPER_ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-acceptance-contract-sha256-v1"
)
PEPPER_KANBAN_COMPLETION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-kanban-completion-result-sha256-v1"
)
PEPPER_CURRENT_REVIEW_PREPARE_NEXT_ACTION_ID = "PREPARE_P18_9_0_REVIEW"
PEPPER_CURRENT_REVIEW_ACCEPTANCE_NEXT_ACTION_ID = (
    "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"
)
PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM = (
    "pepper-review-human-acceptance-action"
)
PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION = 1
PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID = (
    "pepper-p18-9-0-review-human-acceptance-action-v1"
)
PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-review-human-acceptance-action-sha256-v1"
)
PEPPER_REVIEW_HUMAN_ACCEPTANCE_TEXT_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-review-human-acceptance-text-sha256-v1"
)
PEPPER_REVIEW_HUMAN_ACCEPTANCE_READY_MARKER = (
    "PEPPER-REVIEW-HUMAN-ACCEPTANCE-READY-FOR-HUMAN-SMOKE"
)
PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT = (
    "Acepto explícitamente la review de P18.9.0 y el resultado preparado para aceptación humana."
)
PEPPER_GOVERNED_EXECUTOR_PROVIDER = "openai-codex"
PEPPER_GOVERNED_EXECUTOR_MODEL = "gpt-5.5"
PEPPER_GOVERNED_EXECUTOR_API_MODE = "codex_responses"

_GOVERNED_TICKET_START_STORE_DIR = Path("agent-platform") / "pepper-worker-start-action"
_GOVERNED_TICKET_RECOVERY_STORE_DIR = Path("agent-platform") / "pepper-recovery-action"
_GOVERNED_TICKET_REVIEW_PREPARE_STORE_DIR = Path("agent-platform") / "pepper-review-prepare-action"
_GOVERNED_TICKET_REVIEW_ACCEPTANCE_STORE_DIR = (
    Path("agent-platform") / "pepper-review-human-acceptance-action"
)
_GOVERNED_TICKET_AUTHORITY_PATH_SPECS = {
    "execution_start": (
        _GOVERNED_TICKET_START_STORE_DIR,
        "execution-start.json",
    ),
    "retry_start": (
        _GOVERNED_TICKET_START_STORE_DIR,
        "retry-start.json",
    ),
    "retry_start_history": (
        _GOVERNED_TICKET_START_STORE_DIR,
        "retry-start.history.jsonl",
    ),
    "recovery_action": (
        _GOVERNED_TICKET_RECOVERY_STORE_DIR,
        "recovery-action.json",
    ),
    "recovery_action_history": (
        _GOVERNED_TICKET_RECOVERY_STORE_DIR,
        "recovery-action.history.jsonl",
    ),
    "review_prepare": (
        _GOVERNED_TICKET_REVIEW_PREPARE_STORE_DIR,
        "review-prepare.json",
    ),
    "review_prepare_history": (
        _GOVERNED_TICKET_REVIEW_PREPARE_STORE_DIR,
        "review-prepare.history.jsonl",
    ),
    "review_acceptance": (
        _GOVERNED_TICKET_REVIEW_ACCEPTANCE_STORE_DIR,
        "review-acceptance.json",
    ),
    "review_acceptance_history": (
        _GOVERNED_TICKET_REVIEW_ACCEPTANCE_STORE_DIR,
        "review-acceptance.history.jsonl",
    ),
}

_ACTIVE_EXECUTION_STATUSES = frozenset({"running"})
_TERMINAL_EXECUTION_STATUSES = frozenset({
    "blocked",
    "cancelled",
    "completed",
    "crashed",
    "done",
    "failed",
    "gave_up",
    "rate_limited",
    "reclaimed",
    "spawn_failed",
    "timed_out",
})
_GOVERNED_TICKET_FAILURE_OUTCOMES = frozenset({
    "blocked",
    "crashed",
    "failed",
    "gave_up",
    "rate_limited",
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


class ProductRuntimeAuthorityMismatch(ProductRuntimeConflict):
    """Raised when a persisted authority no longer matches current identity."""

    def __init__(self, message: str, *, diagnostics: dict[str, Any]) -> None:
        self.diagnostics = diagnostics
        super().__init__(message)


class ProductRuntimeDecisionFailed(ProductRuntimeError):
    """Raised when an approval decision cannot be applied safely."""


@dataclass(frozen=True)
class GovernedTicketLifecycleBinding:
    """Current governed ticket identity, actions, and runtime authority."""

    product_id: str
    project_id: str
    macroproject_id: str
    macroproject_title: str
    ticket_id: str
    ticket_title: str
    ticket_action_token: str
    ticket_hyphen_token: str
    ticket_spec_sha256: str | None
    work_packet_id: str | None
    work_packet_sha256: str | None
    work_packet_compilation_count: int | None
    executor_provider: str
    executor_model: str
    executor_api_mode: str
    generate_next_action_id: str
    approve_next_action_id: str
    approved_no_execution_next_action_id: str
    execution_start_next_action_id: str
    execution_recovery_next_action_id: str
    retry_start_next_action_id: str
    review_prepare_next_action_id: str
    review_acceptance_next_action_id: str
    monitor_execution_next_action_id: str
    revise_next_action_id: str


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


class CurrentTicketExecutionStartRequest(BaseModel):
    """Request body for the bounded P18.9.0 worker start action."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    human_authorization_text: str = Field(min_length=1, max_length=1024)
    authorizer_id: str = Field(default="pepper-chat-human", min_length=1, max_length=128)
    project_id: str | None = Field(default=None, max_length=128)
    ticket_id: str | None = Field(default=None, max_length=128)
    next_action_id: str | None = Field(default=None, max_length=128)

    @field_validator("authorizer_id")
    @classmethod
    def authorizer_must_be_safe(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("authorizer_id contains control characters")
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid authorizer_id")
        return value

    @field_validator("project_id", "ticket_id", "next_action_id")
    @classmethod
    def optional_guards_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid guarded identifier")
        return value

    @field_validator("human_authorization_text")
    @classmethod
    def authorization_text_must_be_text(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("human_authorization_text contains control characters")
        return value


class CurrentTicketExecutionRecoveryRequest(BaseModel):
    """Request body for the bounded P18.9.0 failed-execution recovery action."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    human_authorization_text: str = Field(min_length=1, max_length=1024)
    authorizer_id: str = Field(default="pepper-chat-human", min_length=1, max_length=128)
    project_id: str | None = Field(default=None, max_length=128)
    ticket_id: str | None = Field(default=None, max_length=128)
    next_action_id: str | None = Field(default=None, max_length=128)

    @field_validator("authorizer_id")
    @classmethod
    def authorizer_must_be_safe(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("authorizer_id contains control characters")
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid authorizer_id")
        return value

    @field_validator("project_id", "ticket_id", "next_action_id")
    @classmethod
    def optional_guards_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid guarded identifier")
        return value

    @field_validator("human_authorization_text")
    @classmethod
    def authorization_text_must_be_text(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("human_authorization_text contains control characters")
        return value


class CurrentTicketReviewPrepareRequest(BaseModel):
    """Request body for bounded P18.9.0 post-execution review preparation."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    project_id: str | None = Field(default=None, max_length=128)
    ticket_id: str | None = Field(default=None, max_length=128)
    next_action_id: str | None = Field(default=None, max_length=128)

    @field_validator("project_id", "ticket_id", "next_action_id")
    @classmethod
    def optional_guards_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid guarded identifier")
        return value


class CurrentTicketReviewAcceptanceRequest(BaseModel):
    """Request body for bounded P18.9.0 human review acceptance."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    human_acceptance_text: str = Field(min_length=1, max_length=1024)
    acceptor_id: str = Field(default="pepper-chat-human", min_length=1, max_length=128)
    project_id: str | None = Field(default=None, max_length=128)
    ticket_id: str | None = Field(default=None, max_length=128)
    next_action_id: str | None = Field(default=None, max_length=128)

    @field_validator("acceptor_id")
    @classmethod
    def acceptor_must_be_safe(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("acceptor_id contains control characters")
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid acceptor_id")
        return value

    @field_validator("project_id", "ticket_id", "next_action_id")
    @classmethod
    def optional_guards_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid guarded identifier")
        return value

    @field_validator("human_acceptance_text")
    @classmethod
    def acceptance_text_must_be_text(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("human_acceptance_text contains control characters")
        return unicodedata.normalize("NFC", value)


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


def governed_ticket_lifecycle_action_token(ticket_id: str) -> str:
    """Return the reusable action-token form for a governed ticket id."""

    token = re.sub(r"[^A-Za-z0-9]+", "_", str(ticket_id or "").strip()).strip("_")
    if not token:
        raise ProductRuntimeConflict("governed ticket id is unavailable")
    return token.upper()


def governed_ticket_lifecycle_hyphen_token(ticket_id: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", str(ticket_id or "").strip()).strip("-")
    if not token:
        raise ProductRuntimeConflict("governed ticket id is unavailable")
    return token.upper()


def governed_ticket_lifecycle_action_ids(ticket_id: str) -> dict[str, str]:
    token = governed_ticket_lifecycle_action_token(ticket_id)
    return {
        "generate": f"GENERATE_{token}",
        "approve": f"APPROVE_{token}",
        "approved_no_execution": f"{token}_APPROVED_NO_EXECUTION",
        "execution_start": f"START_{token}_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        "execution_recovery": f"RECOVER_{token}_EXECUTION",
        "retry_start": f"START_{token}_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        "review_prepare": f"PREPARE_{token}_REVIEW",
        "review_acceptance": f"AWAIT_HUMAN_{token}_REVIEW_ACCEPTANCE",
        "monitor_execution": f"MONITOR_{token}_EXECUTION",
        "revise": f"REVISE_{token}",
    }


def _int_or_none(value: object) -> int | None:
    try:
        return int(value) if value not in {None, ""} else None
    except (TypeError, ValueError):
        return None


def _current_generation_record_for_binding() -> dict[str, Any] | None:
    try:
        from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
            load_p18_9_0_generation_record,
        )

        return load_p18_9_0_generation_record()
    except Exception:
        return None


def _current_projected_ticket_id_from_records() -> str | None:
    try:
        from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
            kanban_projection_record_path,
            load_kanban_projection_record,
        )
    except Exception:
        return None

    root = kanban_projection_record_path().parent
    if not root.exists():
        return None
    candidates: list[Path] = []
    try:
        candidates = sorted(
            root.glob("*.json"),
            key=lambda path: (
                _governed_ticket_sequence_key(
                    PEPPER_BOOTSTRAP_NEXT_TICKET_ID
                    if path.name == kanban_projection_record_path().name
                    else path.stem
                ),
                path.stat().st_mtime,
            ),
            reverse=True,
        )
    except OSError:
        return None
    canonical_name = kanban_projection_record_path().name
    for path in candidates:
        ticket_id = PEPPER_BOOTSTRAP_NEXT_TICKET_ID if path.name == canonical_name else path.stem
        try:
            projection = load_kanban_projection_record(ticket_id=ticket_id)
        except Exception:
            continue
        if projection is not None:
            return str(projection.get("ticket_id") or ticket_id)
    return None


def _governed_ticket_sequence_key(ticket_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", str(ticket_id or "")))


def _current_projection_record_for_binding() -> dict[str, Any] | None:
    try:
        from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
            load_kanban_projection_record,
            load_p18_9_0_kanban_projection_record,
        )

        ticket_id = _current_projected_ticket_id_from_records()
        if ticket_id:
            projection = load_kanban_projection_record(ticket_id=ticket_id)
            if projection is not None:
                return projection
        return load_p18_9_0_kanban_projection_record()
    except Exception:
        return None


def resolve_current_ticket_lifecycle_binding(
    *,
    generation_record: dict[str, Any] | None = None,
    projection_record: dict[str, Any] | None = None,
) -> GovernedTicketLifecycleBinding:
    """Resolve current governed ticket lifecycle values from live authority."""

    generation = generation_record
    projection = projection_record
    if projection is None:
        projection = _current_projection_record_for_binding()
    if generation is None:
        generation = _current_generation_record_for_binding()
    if projection_record is not None and isinstance(projection, dict):
        authority = projection
    elif generation_record is not None and isinstance(generation, dict):
        authority = generation
    else:
        authority = projection if isinstance(projection, dict) else generation
    authority = authority if isinstance(authority, dict) else {}

    ticket_id = _safe_text(authority.get("ticket_id") or PEPPER_NEXT_TICKET_ID, limit=128)
    ticket_title = _safe_text(
        authority.get("ticket_title") or PEPPER_NEXT_TICKET_TITLE,
        limit=300,
    )
    action_ids = governed_ticket_lifecycle_action_ids(ticket_id)
    return GovernedTicketLifecycleBinding(
        product_id=PEPPER_GOVERNED_PRODUCT_ID,
        project_id=_safe_text(authority.get("project_id") or PEPPER_GOVERNED_PROJECT_ID, limit=128),
        macroproject_id=_safe_text(
            authority.get("macroproject_id") or PEPPER_GOVERNED_MACROPROJECT_ID,
            limit=128,
        ),
        macroproject_title=_safe_text(
            authority.get("macroproject_title") or PEPPER_GOVERNED_MACROPROJECT_TITLE,
            limit=300,
        ),
        ticket_id=ticket_id,
        ticket_title=ticket_title,
        ticket_action_token=governed_ticket_lifecycle_action_token(ticket_id),
        ticket_hyphen_token=governed_ticket_lifecycle_hyphen_token(ticket_id),
        ticket_spec_sha256=authority.get("ticket_spec_SHA256"),
        work_packet_id=authority.get("work_packet_id"),
        work_packet_sha256=authority.get("work_packet_SHA256"),
        work_packet_compilation_count=_int_or_none(
            authority.get("WorkPacket_compilation_count")
        ),
        executor_provider=PEPPER_GOVERNED_EXECUTOR_PROVIDER,
        executor_model=PEPPER_GOVERNED_EXECUTOR_MODEL,
        executor_api_mode=PEPPER_GOVERNED_EXECUTOR_API_MODE,
        generate_next_action_id=action_ids["generate"],
        approve_next_action_id=action_ids["approve"],
        approved_no_execution_next_action_id=action_ids["approved_no_execution"],
        execution_start_next_action_id=action_ids["execution_start"],
        execution_recovery_next_action_id=action_ids["execution_recovery"],
        retry_start_next_action_id=action_ids["retry_start"],
        review_prepare_next_action_id=action_ids["review_prepare"],
        review_acceptance_next_action_id=action_ids["review_acceptance"],
        monitor_execution_next_action_id=action_ids["monitor_execution"],
        revise_next_action_id=action_ids["revise"],
    )


def governed_ticket_lifecycle_authority_path(
    kind: str,
    *,
    binding: GovernedTicketLifecycleBinding | None = None,
    ticket_id: str | None = None,
) -> Path:
    from hermes_constants import get_hermes_home

    if kind not in _GOVERNED_TICKET_AUTHORITY_PATH_SPECS:
        raise ProductRuntimeConflict("unknown governed ticket authority path kind")
    if binding is None and ticket_id is None:
        binding = resolve_current_ticket_lifecycle_binding()
    scoped_ticket_id = _safe_text(
        ticket_id or (binding.ticket_id if binding is not None else PEPPER_NEXT_TICKET_ID),
        limit=128,
    )
    store_dir, suffix = _GOVERNED_TICKET_AUTHORITY_PATH_SPECS[kind]
    return get_hermes_home() / store_dir / f"{scoped_ticket_id}.{suffix}"


def execution_start_record_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped execution-start authority path for one ticket."""

    return governed_ticket_lifecycle_authority_path(
        "execution_start",
        ticket_id=ticket_id,
    )


def _execution_start_record_path_for_projection(
    projection_record: dict[str, Any] | None = None,
) -> Path:
    if projection_record is not None:
        return execution_start_record_path_for_ticket(str(projection_record["ticket_id"]))
    projection = _load_current_projection_record()
    return execution_start_record_path_for_ticket(str(projection["ticket_id"]))


def _current_ticket_identity_fields(
    projection: dict[str, Any],
) -> tuple[GovernedTicketLifecycleBinding, dict[str, Any]]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    expected = {
        "project_id": binding.project_id,
        "macroproject_id": binding.macroproject_id,
        "ticket_id": binding.ticket_id,
        "ticket_title": binding.ticket_title,
        "ticket_spec_SHA256": binding.ticket_spec_sha256,
        "work_packet_id": binding.work_packet_id,
        "work_packet_SHA256": binding.work_packet_sha256,
        "WorkPacket_compilation_count": binding.work_packet_compilation_count,
    }
    return binding, expected


def _current_ticket_projection_identity_fields(projection: dict[str, Any]) -> dict[str, Any]:
    _binding, identity = _current_ticket_identity_fields(projection)
    return identity


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


def _p18_9_0_generation_overlay() -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    try:
        from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
            generated_record_to_workflow_overlay,
            load_generation_record,
            load_p18_9_0_generation_record,
        )

        record = load_p18_9_0_generation_record()
        if record is None:
            return None, None
        overlay = generated_record_to_workflow_overlay(record)
        projection = _projection_record_for_generated_ticket(record)
        if projection is not None:
            overlay.update(_projection_overlay_for_record(projection))
            start_overlay, start_blocker = _current_ticket_execution_start_overlay(projection)
            if start_overlay is not None:
                overlay.update(start_overlay)
                retry_start_overlay, retry_start_blocker = _p18_9_0_retry_start_overlay(
                    projection,
                )
                if retry_start_overlay is not None:
                    overlay.update(retry_start_overlay)
                    if overlay.get("workflow_status") == "execution_completed":
                        review_overlay, review_blocker = _p18_9_0_review_prepare_overlay(
                            projection,
                            completed_overlay=overlay,
                        )
                        if review_overlay is not None:
                            overlay.update(review_overlay)
                            next_ticket_id = overlay.get("next_ticket_id")
                            if next_ticket_id:
                                next_record = load_generation_record(ticket_id=str(next_ticket_id))
                                if next_record is not None:
                                    overlay.update(generated_record_to_workflow_overlay(next_record))
                                    next_projection = _projection_record_for_generated_ticket(next_record)
                                    if next_projection is not None:
                                        overlay.update(_projection_overlay_for_record(next_projection))
                                        next_start_overlay, next_start_blocker = (
                                            _current_ticket_execution_start_overlay(
                                                next_projection,
                                            )
                                        )
                                        if next_start_overlay is not None:
                                            overlay.update(next_start_overlay)
                                        if next_start_blocker is not None:
                                            return overlay, next_start_blocker
                        if review_blocker is not None:
                            return overlay, review_blocker
                    return overlay, retry_start_blocker
                if retry_start_blocker is not None:
                    return overlay, retry_start_blocker
                recovery_overlay, recovery_blocker = _p18_9_0_recovery_overlay(
                    projection,
                    start_overlay=start_overlay,
                )
                if recovery_overlay is not None:
                    overlay.update(recovery_overlay)
                if recovery_blocker is not None:
                    return overlay, recovery_blocker
                if recovery_overlay is not None:
                    return overlay, None
                if overlay.get("workflow_status") == "execution_completed":
                    review_overlay, review_blocker = _p18_9_0_review_prepare_overlay(
                        projection,
                        completed_overlay=overlay,
                    )
                    if review_overlay is not None:
                        overlay.update(review_overlay)
                        next_ticket_id = overlay.get("next_ticket_id")
                        if next_ticket_id:
                            next_record = load_generation_record(ticket_id=str(next_ticket_id))
                            if next_record is not None:
                                overlay.update(generated_record_to_workflow_overlay(next_record))
                                next_projection = _projection_record_for_generated_ticket(next_record)
                                if next_projection is not None:
                                    overlay.update(_projection_overlay_for_record(next_projection))
                                    next_start_overlay, next_start_blocker = (
                                        _current_ticket_execution_start_overlay(
                                            next_projection,
                                        )
                                    )
                                    if next_start_overlay is not None:
                                        overlay.update(next_start_overlay)
                                    if next_start_blocker is not None:
                                        return overlay, next_start_blocker
                    if review_blocker is not None:
                        return overlay, review_blocker
            if start_blocker is not None:
                return overlay, start_blocker
        return overlay, None
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": "P18-9-0-GENERATION-AUTHORITY",
            "status": "blocked_by_invalid_generated_ticket_authority",
            "evidence": _safe_text(exc, limit=300),
        }


def _projection_record_for_generated_ticket(record: dict[str, Any]) -> dict[str, Any] | None:
    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        load_kanban_projection_record,
    )

    return load_kanban_projection_record(
        ticket_id=str(record["ticket_id"]),
        generation_record=record,
    )


def _projection_overlay_for_record(record: dict[str, Any]) -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        kanban_projection_to_workflow_overlay,
    )

    return kanban_projection_to_workflow_overlay(record)


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


_TICKET_APPROVAL_KIND = "ticket_approval"
_P18_9_0_TICKET_APPROVAL_KIND = _TICKET_APPROVAL_KIND


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


def _timestamp_from_source(value: Any) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, float(value))
    if isinstance(value, str):
        try:
            return max(0.0, datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())
        except ValueError:
            return 0.0
    return 0.0


def _p18_9_0_pending_ticket_approval_record() -> dict[str, Any] | None:
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        load_approval_decision_record,
        load_p18_9_0_generation_record,
    )

    record = load_p18_9_0_generation_record()
    if record is None:
        return None
    decision = load_approval_decision_record(
        ticket_id=str(record["ticket_id"]),
        generation_record=record,
    )
    return None if decision is not None else record


def _current_pending_ticket_approval_record() -> dict[str, Any] | None:
    p18_9_0_pending = _p18_9_0_pending_ticket_approval_record()
    if p18_9_0_pending is not None:
        return p18_9_0_pending
    try:
        from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
            CANONICAL_TICKET_ID,
            generation_record_path_for_ticket,
            load_approval_decision_record,
            load_generation_record,
        )

        store_dir = generation_record_path_for_ticket(CANONICAL_TICKET_ID).parent
        records: list[dict[str, Any]] = []
        for path in sorted(store_dir.glob("*.json")):
            if path.name.endswith(".approval-decision.json") or path.stem == CANONICAL_TICKET_ID:
                continue
            try:
                record = load_generation_record(ticket_id=path.stem)
            except Exception:
                continue
            if record is None or record.get("human_ticket_approval_present") is True:
                continue
            if load_approval_decision_record(
                ticket_id=str(record["ticket_id"]),
                generation_record=record,
            ) is None:
                records.append(record)
    except Exception:
        return None
    if not records:
        return None
    if len(records) > 1:
        raise ProductRuntimeConflict("pending ticket approval authority is ambiguous")
    return records[0]


def _ticket_approval_summary(record: dict[str, Any]) -> dict[str, Any]:
    ticket_id = _safe_id(record.get("ticket_id"))
    ticket_title = _safe_text(record.get("ticket_title"), limit=300)
    return {
        "id": ticket_id,
        "semantics": "explicit_approval_request",
        "title": f"Review governed ticket approval: {ticket_id}",
        "summary": (
            f"Generated {ticket_id} {ticket_title!r} is awaiting "
            "explicit human ticket approval. The existing TicketSpec, WorkPacket ID, "
            "WorkPacket digest and compile count are preserved."
        ),
        "status": "pending",
        "request_type": "ticket_approval",
        "requested_at": _timestamp_from_source(record.get("created_at")),
        "expires_at": None,
        "requester": "pepper-ticket-architect-bridge",
        "risk_label": "medium",
        "target": {
            "type": "runtime_action",
            "label": f"{ticket_id} {ticket_title}",
        },
        "reason": (
            "Approve records a human ticket approval through the governed P18 approval "
            "transition; reject records the human rejection. Neither path executes a "
            "worker, dispatches Kanban, recompiles the WorkPacket, mutates Git, invokes "
            "Docker, or invokes Graphify."
        ),
    }


def _p18_9_0_ticket_approval_summary(record: dict[str, Any]) -> dict[str, Any]:
    return _ticket_approval_summary(record)


def _ticket_approval_evidence(record: dict[str, Any]) -> list[dict[str, str]]:
    approval_id = _safe_id(record.get("ticket_id"))
    return [
        {
            "id": f"{approval_id}:bridge",
            "label": f"bridge authority SHA256: {record['bridge_SHA256']}",
        },
        {
            "id": f"{approval_id}:ticket_spec",
            "label": f"TicketSpec SHA256: {record['ticket_spec_SHA256']}",
        },
        {
            "id": f"{approval_id}:work_packet",
            "label": (
                f"WorkPacket {record['work_packet_id']} SHA256: "
                f"{record['work_packet_SHA256']}"
            ),
        },
        {
            "id": f"{approval_id}:workflow",
            "label": "workflow transition GWT-002 stops at awaiting_ticket_approval",
        },
    ]


def build_approval_inbox_source() -> dict[str, Any]:
    """Return the bounded live approval inbox source for the active profile."""

    from tools import write_approval as wa

    approvals: list[dict[str, Any]] = []
    ticket_approval = _current_pending_ticket_approval_record()
    if ticket_approval is not None:
        approvals.append(_ticket_approval_summary(ticket_approval))
    for subsystem in _subsystems():
        for record in wa.list_pending(subsystem):
            approvals.append(_approval_summary(record))
    return {
        "source_system": APPROVAL_SOURCE_SYSTEM,
        "source_authority": "durable-hermes-staged-write-store+pepper-ticket-architect-bridge",
        "canonical_approval_authority": "pepper-controlled-human-decision-v1",
        "approvals": approvals,
    }


def _find_pending(approval_id: str) -> tuple[str, dict[str, Any]]:
    from tools import write_approval as wa

    approval_id = _safe_id(approval_id)
    matches: list[tuple[str, dict[str, Any]]] = []
    ticket_approval = _current_pending_ticket_approval_record()
    if ticket_approval is not None and approval_id == _safe_id(ticket_approval.get("ticket_id")):
        matches.append((_TICKET_APPROVAL_KIND, ticket_approval))
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
    if subsystem == _TICKET_APPROVAL_KIND:
        summary = _ticket_approval_summary(record)
        return {
            "source_system": APPROVAL_SOURCE_SYSTEM,
            "source_authority": "pepper-ticket-architect-bridge-authority",
            "canonical_approval_authority": "pepper-controlled-human-decision-v1",
            "approval": summary,
            "evidence": _ticket_approval_evidence(record),
            "decisions": [],
        }

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


def _resolved_ticket_approval_decision(
    approval_id: str,
    request: ApprovalDecisionRequest,
) -> dict[str, Any] | None:
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        TicketArchitectBridgeConflict,
        TicketArchitectBridgeInputError,
        load_approval_decision_record,
        load_generation_record,
    )

    ticket_id = _safe_id(approval_id)
    if not ticket_id:
        return None
    try:
        generation = load_generation_record(ticket_id=ticket_id)
        if generation is None:
            return None
        decision = load_approval_decision_record(
            ticket_id=ticket_id,
            generation_record=generation,
        )
    except TicketArchitectBridgeInputError:
        return None
    except TicketArchitectBridgeConflict as exc:
        raise ProductRuntimeConflict(str(exc) or "ticket approval authority conflict") from exc
    if decision is None:
        return None
    if decision.get("decision") != request.decision:
        raise ProductRuntimeConflict("approval is already decided with the opposite decision")
    return {
        "source_system": APPROVAL_SOURCE_SYSTEM,
        "id": approval_id,
        "decision": request.decision,
        "status": decision["status"],
        "actor": decision["actor"],
        "decided_at": decision["decided_at"],
        "applied": False,
        "idempotent_replay": True,
        "ticket_id": decision["ticket_id"],
        "workflow_transition_id": decision["workflow_transition_result"]["transition"]["transition_id"],
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "WorkPacket_compilation_count": 1,
        "WorkPacket_recompile_required": False,
    }


def apply_approval_decision(
    approval_id: str,
    request: ApprovalDecisionRequest,
) -> dict[str, Any]:
    """Apply a human approval decision through the existing write gate."""

    from tools import write_approval as wa

    approval_id = _safe_id(approval_id)
    resolved_ticket_decision = _resolved_ticket_approval_decision(
        approval_id,
        request,
    )
    if resolved_ticket_decision is not None:
        return resolved_ticket_decision

    subsystem, record = _find_pending(approval_id)
    if subsystem == _TICKET_APPROVAL_KIND:
        from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
            TicketArchitectBridgeConflict,
            apply_ticket_approval_decision,
        )

        ticket_id = _safe_id(record.get("ticket_id"))
        if approval_id != ticket_id:
            raise ProductRuntimeConflict("approval id does not match pending ticket authority")
        try:
            result = apply_ticket_approval_decision(
                ticket_id=ticket_id,
                decision=request.decision,
                actor=request.actor,
                decided_at=time.time(),
            )
        except TicketArchitectBridgeConflict as exc:
            raise ProductRuntimeConflict(str(exc) or "ticket approval authority conflict") from exc
        except Exception as exc:  # pragma: no cover - defensive authority guard
            raise ProductRuntimeDecisionFailed("ticket approval decision failed") from exc
        return {
            "source_system": APPROVAL_SOURCE_SYSTEM,
            "id": approval_id,
            "decision": request.decision,
            "status": result["status"],
            "actor": request.actor,
            "decided_at": result["decided_at"],
            "applied": True,
            "ticket_id": result["ticket_id"],
            "workflow_transition_id": result["workflow_transition_id"],
            "ticket_execution_authorized": False,
            "WorkPacket_execution_authorized": False,
            "runtime_execution_authorized": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "WorkPacket_compilation_count": 1,
            "WorkPacket_recompile_required": False,
        }

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


def _bounded_optional_text(value: object, *, limit: int) -> str | None:
    text = str(value or "").strip()
    return _safe_text(text, limit=limit) if text else None


def _run_failure_fields(run: Any) -> dict[str, Any]:
    status = str(getattr(run, "status", "") or "").strip().lower()
    outcome = str(getattr(run, "outcome", "") or "").strip().lower()
    if status not in _GOVERNED_TICKET_FAILURE_OUTCOMES and outcome not in _GOVERNED_TICKET_FAILURE_OUTCOMES:
        return {"failure_category": None, "failure_summary": None}

    metadata = getattr(run, "metadata", None)
    category = None
    summary = None
    if isinstance(metadata, dict):
        category = metadata.get("failure_category")
        summary = metadata.get("failure_summary")
    if not category:
        category = outcome or status or "failed"
    if not summary:
        summary = getattr(run, "error", None) or getattr(run, "summary", None)
    return {
        "failure_category": _bounded_optional_text(category, limit=128),
        "failure_summary": _bounded_optional_text(summary, limit=300),
    }


def _run_dict(run: Any) -> dict[str, Any]:
    failure_fields = _run_failure_fields(run)
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
        **failure_fields,
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


def _p18_9_0_projected_task_id_for_board(board_slug: str) -> str | None:
    try:
        from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
            load_p18_9_0_kanban_projection_record,
        )

        record = load_p18_9_0_kanban_projection_record()
    except Exception:
        return None
    if not isinstance(record, dict):
        return None
    try:
        projected_board = _normalize_board(str(record.get("kanban_board_slug") or ""))
    except Exception:
        return None
    if projected_board != board_slug:
        return None
    task_id = str(record.get("kanban_task_id") or "").strip()
    return task_id if _SAFE_TASK.fullmatch(task_id) else None


def _is_p18_9_0_projected_task(board_slug: str, task_id: str) -> bool:
    return _p18_9_0_projected_task_id_for_board(board_slug) == task_id


def build_task_execution_source(board_slug: str, task_id: str) -> dict[str, Any]:
    """Return the existing task-nested execution evidence through product API."""

    from hermes_cli import kanban_db

    board = _normalize_board(board_slug)
    if not _SAFE_TASK.fullmatch(task_id):
        raise ProductRuntimeNotFound("invalid task id")
    kanban_db.init_db(board=board)
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(
            conn,
            task_id=task_id if _is_p18_9_0_projected_task(board, task_id) else None,
        )
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
            _reconcile_kanban_board_lifecycle(
                conn,
                task_id=_p18_9_0_projected_task_id_for_board(board),
            )
            tasks = kanban_db.list_tasks(conn, include_archived=False)
            for task in tasks:
                for run in kanban_db.list_runs(conn, task.id):
                    control = _execution_control_fields(board, task.id, task.status)
                    failure_fields = _run_failure_fields(run)
                    records.append({
                        "id": int(run.id),
                        "board_slug": board,
                        "task_id": task.id,
                        "task_title": "Source task title withheld by the execution projection",
                        "profile": run.profile,
                        "status": run.status,
                        "outcome": run.outcome,
                        **failure_fields,
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


def _reconcile_kanban_board_lifecycle(
    conn: Any,
    *,
    task_id: str | None = None,
) -> None:
    """Best-effort Kanban lifecycle reconciliation before Pepper reads state."""

    try:
        from hermes_cli import kanban_db

        kanban_db.detect_crashed_workers(conn)
        if task_id:
            kanban_db.reconcile_orphaned_active_run(
                conn,
                task_id,
                failure_limit=1,
                force_trip=True,
                failure_category="worker_bootstrap_failure",
            )
    except Exception:
        return


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


def generate_current_governed_ticket(
    *,
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
) -> dict[str, Any]:
    """Generate the current governed Pepper ticket from the active next action."""

    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        generate_current_ticket,
    )

    workflow = build_workflow_control_snapshot()
    return generate_current_ticket(
        workflow=workflow,
        requested_project_id=project_id,
        requested_ticket_id=ticket_id,
        requested_next_action_id=next_action_id,
    )


def reconcile_invalid_current_generation_authority(
    *,
    project_id: str | None = None,
    ticket_id: str | None = None,
) -> dict[str, Any]:
    """Reconcile invalid unaccepted future-ticket authority without generation."""

    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        reconcile_invalid_future_ticket_authority,
        resolve_canonical_next_ticket as bridge_resolve_canonical_next_ticket,
    )

    workflow = build_workflow_control_snapshot()
    authority = bridge_resolve_canonical_next_ticket(workflow)
    if project_id not in {None, authority.project_id}:
        raise ProductRuntimeConflict(f"current generation authority is bounded to {authority.project_id}")
    if ticket_id not in {None, authority.ticket_id}:
        raise ProductRuntimeConflict(
            f"current generation authority is bounded to {authority.ticket_id}"
        )
    return reconcile_invalid_future_ticket_authority(
        ticket_id=authority.ticket_id,
        workflow=workflow,
    )


def project_current_approved_workpacket_to_kanban(
    *,
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
) -> dict[str, Any]:
    """Project the current approved Pepper WorkPacket to Kanban without dispatch."""

    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        project_current_approved_workpacket_to_kanban as project_workpacket,
    )

    return project_workpacket(
        workflow=build_workflow_control_snapshot(),
        requested_project_id=project_id,
        requested_ticket_id=ticket_id,
        requested_next_action_id=next_action_id,
    )


def p18_9_0_execution_start_record_path() -> Path:
    """Return the profile-scoped P18.9.0 execution-start authority path."""

    return execution_start_record_path_for_ticket(PEPPER_BOOTSTRAP_NEXT_TICKET_ID)


def p18_9_0_recovery_action_record_path() -> Path:
    """Return the profile-scoped P18.9.0 recovery authority path."""

    return governed_ticket_lifecycle_authority_path(
        "recovery_action",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_recovery_action_history_path() -> Path:
    """Return the append-only P18.9.0 recovery authority history path."""

    return governed_ticket_lifecycle_authority_path(
        "recovery_action_history",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_retry_start_record_path() -> Path:
    """Return the profile-scoped P18.9.0 retry-start authority path."""

    return governed_ticket_lifecycle_authority_path(
        "retry_start",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_retry_start_history_path() -> Path:
    """Return the append-only P18.9.0 retry-start authority history path."""

    return governed_ticket_lifecycle_authority_path(
        "retry_start_history",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_review_prepare_record_path() -> Path:
    """Return the profile-scoped P18.9.0 review-preparation authority path."""

    return governed_ticket_lifecycle_authority_path(
        "review_prepare",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_review_prepare_history_path() -> Path:
    """Return the append-only P18.9.0 review-preparation authority history path."""

    return governed_ticket_lifecycle_authority_path(
        "review_prepare_history",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_review_acceptance_record_path() -> Path:
    """Return the profile-scoped P18.9.0 review-acceptance authority path."""

    return governed_ticket_lifecycle_authority_path(
        "review_acceptance",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def p18_9_0_review_acceptance_history_path() -> Path:
    """Return the append-only P18.9.0 review-acceptance authority history path."""

    return governed_ticket_lifecycle_authority_path(
        "review_acceptance_history",
        ticket_id=PEPPER_NEXT_TICKET_ID,
    )


def load_p18_9_0_execution_start_record(
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the bounded P18.9.0 worker-start record, if present."""

    path = _execution_start_record_path_for_projection(projection_record)
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "execution-start authorization record is unreadable"
        ) from exc
    return validate_p18_9_0_execution_start_record(
        record,
        projection_record=projection_record,
    )


def load_p18_9_0_recovery_action_record(
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the bounded P18.9.0 recovery record, if present."""

    path = p18_9_0_recovery_action_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "P18.9.0 recovery action record is unreadable"
        ) from exc
    return validate_p18_9_0_recovery_action_record(
        record,
        projection_record=projection_record,
    )


def load_p18_9_0_retry_start_record(
    *,
    projection_record: dict[str, Any] | None = None,
    recovery_record: dict[str, Any] | None = None,
    allow_historical_mismatch: bool = False,
) -> dict[str, Any] | None:
    """Load and validate the bounded P18.9.0 retry-start record, if present."""

    path = p18_9_0_retry_start_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "P18.9.0 retry-start authorization record is unreadable"
        ) from exc
    try:
        return validate_p18_9_0_retry_start_record(
            record,
            projection_record=projection_record,
            recovery_record=recovery_record,
        )
    except ProductRuntimeConflict:
        if not allow_historical_mismatch:
            raise
        if record.get("retry_start_authorization_SHA256") != _retry_start_record_digest(record):
            raise
        projection = projection_record if projection_record is not None else _load_current_projection_record()
        _validate_execution_start_authority(projection)
        recovery = recovery_record
        if recovery is None:
            recovery = load_p18_9_0_recovery_action_record(projection_record=projection)
        if recovery is None:
            raise
        same_recovery_authority = (
            record.get("recovery_action_SHA256") == recovery.get("recovery_action_SHA256")
        )
        same_recovery_cycle = (
            _retry_start_record_cycle_id(record, recovery, projection)
            == _recovery_record_cycle_id(recovery, projection)
        )
        if same_recovery_authority and same_recovery_cycle:
            raise
        historical_recovery = dict(recovery)
        historical_recovery["recovery_action_SHA256"] = record.get("recovery_action_SHA256")
        historical_recovery["observed_attempt_count"] = record.get("previous_attempt_count")
        historical_recovery["next_attempt_number"] = record.get("next_attempt_number")
        historical_recovery["max_attempts"] = record.get("max_attempts")
        historical_recovery["latest_failed_run_id"] = record.get("latest_failed_run_id")
        validate_p18_9_0_retry_start_record(
            record,
            projection_record=projection,
            recovery_record=historical_recovery,
        )
        return record


def load_p18_9_0_review_prepare_record(
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the bounded P18.9.0 review-preparation record."""

    path = p18_9_0_review_prepare_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "P18.9.0 review-preparation record is unreadable"
        ) from exc
    return validate_p18_9_0_review_prepare_record(
        record,
        projection_record=projection_record,
    )


def load_p18_9_0_review_acceptance_record(
    *,
    projection_record: dict[str, Any] | None = None,
    review_prepare_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the bounded P18.9.0 review-acceptance record."""

    path = p18_9_0_review_acceptance_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "P18.9.0 review-acceptance record is unreadable"
        ) from exc
    return validate_p18_9_0_review_acceptance_record(
        record,
        projection_record=projection_record,
        review_prepare_record=review_prepare_record,
    )


def _p18_9_0_recovery_cycle_id(
    *,
    projection: dict[str, Any],
    latest_failed_run_id: Any,
    observed_attempt_count: Any,
    failure_category: Any = None,
    failure_summary: Any = None,
) -> str:
    payload = {
        "project_id": PEPPER_GOVERNED_PROJECT_ID,
        "ticket_id": PEPPER_NEXT_TICKET_ID,
        "work_packet_id": projection.get("work_packet_id"),
        "work_packet_SHA256": projection.get("work_packet_SHA256"),
        "projection_SHA256": projection.get("projection_SHA256"),
        "kanban_board_slug": projection.get("kanban_board_slug"),
        "kanban_task_id": projection.get("kanban_task_id"),
        "latest_failed_run_id": int(latest_failed_run_id or 0),
        "observed_attempt_count": int(observed_attempt_count or 0),
        "failure_category": _safe_text(failure_category, limit=120),
        "failure_summary": _safe_text(failure_summary, limit=300),
    }
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(f"pepper-p18-9-0-recovery-cycle-v1\n{data}".encode("utf-8")).hexdigest()


def _recovery_record_cycle_id(record: dict[str, Any], projection: dict[str, Any]) -> str:
    return str(record.get("recovery_cycle_id") or _p18_9_0_recovery_cycle_id(
        projection=projection,
        latest_failed_run_id=record.get("latest_failed_run_id"),
        observed_attempt_count=record.get("observed_attempt_count"),
        failure_category=record.get("failure_category"),
        failure_summary=record.get("failure_summary"),
    ))


def _retry_start_record_cycle_id(
    record: dict[str, Any],
    recovery_record: dict[str, Any],
    projection: dict[str, Any],
) -> str:
    if record.get("recovery_cycle_id"):
        return str(record["recovery_cycle_id"])
    return _p18_9_0_recovery_cycle_id(
        projection=projection,
        latest_failed_run_id=record.get("latest_failed_run_id"),
        observed_attempt_count=record.get("previous_attempt_count"),
        failure_category=record.get("failure_category"),
        failure_summary=record.get("failure_summary"),
    )


def _append_authority_history(path: Path, record: dict[str, Any], *, reason: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "archived_at": _utc_now_iso(),
        "archive_reason": reason,
        "record": record,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def _archive_existing_authority_record(
    current_path: Path,
    history_path: Path,
    *,
    reason: str,
) -> None:
    if not current_path.exists():
        return
    try:
        record = json.loads(current_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        record = {"unreadable_record_path": str(current_path)}
    _append_authority_history(history_path, record, reason=reason)


def validate_p18_9_0_execution_start_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the persisted worker-start authority without dispatching."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("execution-start record must be an object")
    if record.get("start_authorization_SHA256") != _execution_start_record_digest(record):
        raise ProductRuntimeConflict("execution-start record digest mismatch")
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    _binding, identity = _current_ticket_identity_fields(projection)
    expected = {
        "schema_version": PEPPER_WORKER_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_WORKER_START_ACTION_POLICY_ID,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "execution_authorized": True,
        "synthetic": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    authority_identity_fields = {
        "ticket_id",
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
        "projection_SHA256",
        "kanban_task_id",
        "assignee_profile",
        "selected_profile",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            if key in authority_identity_fields:
                raise ProductRuntimeAuthorityMismatch(
                    f"execution-start record {key} mismatch",
                    diagnostics=_execution_start_authority_mismatch_diagnostics(
                        record,
                        projection,
                        mismatched_field=key,
                    ),
                )
            raise ProductRuntimeConflict(f"execution-start record {key} mismatch")
    return record


def validate_p18_9_0_recovery_action_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the persisted recovery authority without requeueing or dispatch."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("recovery action record must be an object")
    if record.get("recovery_action_SHA256") != _recovery_action_record_digest(record):
        raise ProductRuntimeConflict("recovery action record digest mismatch")
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    _binding, identity = _current_ticket_identity_fields(projection)
    expected = {
        "schema_version": PEPPER_RECOVERY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RECOVERY_ACTION_POLICY_ID,
        "source_system": PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "requested_action": "authorize_retry",
        "recovery_status": "retry_pending",
        "retry_identity_model": "same_kanban_task_new_run",
        "future_retry_prepared": True,
        "future_task_skills": [],
        "future_retry_capability_surface": "pepper_repository",
        "unresolved_Hermes_task_skills": [],
        "retry_budget_exhausted": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "retry_execution_count": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ProductRuntimeConflict(f"recovery action record {key} mismatch")
    if int(record.get("observed_attempt_count") or 0) < 1:
        raise ProductRuntimeConflict("recovery action observed_attempt_count mismatch")
    expected_max_attempts = max(
        int(projection.get("task_max_retries") or 0) + 1,
        int(record.get("observed_attempt_count") or 0) + 1,
    )
    if int(record.get("max_attempts") or 0) != expected_max_attempts:
        raise ProductRuntimeConflict("recovery action max_attempts mismatch")
    if int(record.get("next_attempt_number") or 0) != int(record["observed_attempt_count"]) + 1:
        raise ProductRuntimeConflict("recovery action next_attempt_number mismatch")
    if record.get("human_authorization_text") != PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT:
        raise ProductRuntimeConflict("recovery action human authorization text mismatch")
    try:
        from hermes_cli.agent_platform.workflow.retry_incident_rollback import (
            RetryIncidentRollbackHumanAuthorization,
            RetryIncidentRollbackRequestedAction,
        )

        authorization_payload = dict(record.get("human_authorization") or {})
        if authorization_payload.get("action") == "authorize_retry":
            authorization_payload["action"] = RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY
        authorization = RetryIncidentRollbackHumanAuthorization.model_validate(
            authorization_payload
        )
    except Exception as exc:
        raise ProductRuntimeConflict("recovery action human authorization is invalid") from exc
    if authorization.authorization_SHA256 != record.get("human_authorization_SHA256"):
        raise ProductRuntimeConflict("recovery action human authorization digest mismatch")
    return record


def validate_p18_9_0_retry_start_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
    recovery_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the persisted retry-start authority without dispatching."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("retry-start record must be an object")
    if record.get("retry_start_authorization_SHA256") != _retry_start_record_digest(record):
        raise ProductRuntimeConflict("retry-start record digest mismatch")
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    recovery = recovery_record
    if recovery is None:
        recovery = load_p18_9_0_recovery_action_record(projection_record=projection)
    if recovery is None:
        raise ProductRuntimeConflict("retry-start record requires recovery authority")
    binding, identity = _current_ticket_identity_fields(projection)
    expected = {
        "schema_version": PEPPER_RETRY_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RETRY_START_ACTION_POLICY_ID,
        "source_system": PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "recovery_action_SHA256": recovery["recovery_action_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "requested_action": "start_retry",
        "recovery_status_at_authorization": "retry_pending",
        "retry_identity_model": "same_kanban_task_new_run",
        "future_task_skills": [],
        "future_retry_capability_surface": "pepper_repository",
        "unresolved_Hermes_task_skills": [],
        "retry_start_authorized": True,
        "synthetic": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ProductRuntimeConflict(f"retry-start record {key} mismatch")
    authorization_diagnostics = execution_human_authorization_text_diagnostics(
        str(record.get("human_authorization_text") or ""),
        current_ticket_id=binding.ticket_id,
        requested_ticket_id=record.get("ticket_id"),
        current_next_action_id=binding.retry_start_next_action_id,
        requested_next_action_id=binding.retry_start_next_action_id,
        expected_authorization_kind="execution_retry_authorization",
    )
    if authorization_diagnostics is not None:
        raise ProductRuntimeConflict(
            "retry-start record human authorization text mismatch: "
            f"{authorization_diagnostics['blocker_detail']}"
        )
    if int(record.get("previous_attempt_count") or 0) != int(recovery["observed_attempt_count"]):
        raise ProductRuntimeConflict("retry-start record previous_attempt_count mismatch")
    if int(record.get("next_attempt_number") or 0) != int(recovery["next_attempt_number"]):
        raise ProductRuntimeConflict("retry-start record next_attempt_number mismatch")
    if int(record.get("max_attempts") or 0) != int(recovery["max_attempts"]):
        raise ProductRuntimeConflict("retry-start record max_attempts mismatch")
    if record.get("latest_failed_run_id") != recovery.get("latest_failed_run_id"):
        raise ProductRuntimeConflict("retry-start record latest_failed_run_id mismatch")
    return record


def validate_p18_9_0_review_prepare_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate persisted P18.9.0 review-preparation authority."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("review-preparation record must be an object")
    if record.get("review_prepare_action_SHA256") != _review_prepare_record_digest(record):
        raise ProductRuntimeConflict("review-preparation record digest mismatch")
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    completion = _kanban_completion_result_source(projection)
    if completion.get("blocker_code"):
        raise ProductRuntimeConflict(str(completion["blocker_code"]))
    contract = _review_prepare_acceptance_contract_for_validation(
        record,
        projection=projection,
        completion=completion,
    )
    binding, identity = _current_ticket_identity_fields(projection)
    expected = {
        "schema_version": PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID,
        "source_system": PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "successful_run_id": completion["run_id"],
        "successful_run_status": "done",
        "successful_run_outcome": "completed",
        "acceptance_contract_SHA256": contract["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": contract["criteria_revision_SHA256"],
        "kanban_completion_result_SHA256": completion["kanban_completion_result_SHA256"],
        "review_package_SHA256": _review_prepare_package_digest(
            projection=projection,
            completion=completion,
            acceptance_contract=contract,
        ),
        "review_prepare_status": "prepared_pending_human_acceptance",
        "validation_state": "review_prepared_pending_human_acceptance",
        "review_state": "prepared_pending_human_acceptance",
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
        "git_handoff_required": False,
        "git_handoff_state": "not_required_for_ticket_result",
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ProductRuntimeConflict(f"review-preparation record {key} mismatch")
    if record.get("acceptance_contract") != contract:
        raise ProductRuntimeConflict("review-preparation acceptance contract mismatch")
    if record.get("kanban_completion_result") != completion:
        raise ProductRuntimeConflict("review-preparation completion result mismatch")
    invariants = record.get("pre_review_invariants")
    if not isinstance(invariants, dict):
        raise ProductRuntimeConflict("review-preparation pre-review invariants missing")
    invariant_expected = {
        "project": binding.project_id,
        "ticket": binding.ticket_id,
        "next_action": binding.review_prepare_next_action_id,
        "run_id": completion["run_id"],
        "run_status": "done",
        "run_outcome": "completed",
        "active_execution_count": 0,
        "recovery_state": "not_required",
        "validation_state": "execution_completed_pending_validation",
        "review_state": "ready_for_review_validation",
        "blocker_count": 0,
    }
    for key, value in invariant_expected.items():
        if invariants.get(key) != value:
            raise ProductRuntimeConflict(f"review-preparation invariant {key} mismatch")
    return record


def validate_p18_9_0_review_acceptance_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
    review_prepare_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate persisted P18.9.0 human review-acceptance authority."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("review-acceptance record must be an object")
    if record.get("review_acceptance_action_SHA256") != _review_acceptance_record_digest(record):
        raise ProductRuntimeConflict("review-acceptance record digest mismatch")
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    review_prepare = review_prepare_record
    if review_prepare is None:
        review_prepare = load_p18_9_0_review_prepare_record(projection_record=projection)
    if review_prepare is None:
        raise ProductRuntimeConflict("review-acceptance record requires review-preparation authority")
    validate_p18_9_0_review_prepare_record(review_prepare, projection_record=projection)
    next_ticket = _p18_9_next_ticket_authority()
    binding, identity = _current_ticket_identity_fields(projection)
    expected = {
        "schema_version": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID,
        "source_system": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "successful_run_id": review_prepare["successful_run_id"],
        "successful_run_status": "done",
        "successful_run_outcome": "completed",
        "review_prepare_action_SHA256": review_prepare["review_prepare_action_SHA256"],
        "review_package_SHA256": review_prepare["review_package_SHA256"],
        "acceptance_contract_SHA256": review_prepare["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": review_prepare["criteria_revision_SHA256"],
        "kanban_completion_result_SHA256": review_prepare["kanban_completion_result_SHA256"],
        "human_acceptance_text": PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        "human_acceptance_text_SHA256": _review_acceptance_text_digest(
            PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT
        ),
        "review_acceptance_status": "accepted",
        "validation_state": "review_accepted",
        "review_state": "accepted",
        "workflow_state": "P18.9.0-COMPLETED",
        "workflow_status": "completed",
        "governed_workflow_state": "completed",
        "human_acceptance_required": True,
        "human_acceptance_recorded": True,
        "pending_human_acceptance_required": False,
        "ticket_closed": True,
        "P18_9_0_closed": True,
        "P18_9_0_completed": True,
        "git_handoff_required": False,
        "git_handoff_state": "not_required_for_ticket_result",
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ProductRuntimeConflict(f"review-acceptance record {key} mismatch")
    acceptor = str(record.get("acceptor_id") or "")
    if not _SAFE_ID.fullmatch(acceptor):
        raise ProductRuntimeConflict("review-acceptance record acceptor_id mismatch")
    if record.get("review_prepare_authority") != _review_prepare_authority_projection(review_prepare):
        raise ProductRuntimeConflict("review-acceptance review-preparation authority mismatch")
    if not _review_acceptance_next_ticket_snapshot_matches(record, next_ticket):
        raise ProductRuntimeConflict("review-acceptance next ticket authority mismatch")
    invariants = record.get("pre_acceptance_invariants")
    if not isinstance(invariants, dict):
        raise ProductRuntimeConflict("review-acceptance pre-acceptance invariants missing")
    invariant_expected = {
        "project": binding.project_id,
        "ticket": binding.ticket_id,
        "next_action": binding.review_acceptance_next_action_id,
        "review_prepare_action_SHA256": review_prepare["review_prepare_action_SHA256"],
        "review_package_SHA256": review_prepare["review_package_SHA256"],
        "active_execution_count": 0,
        "recovery_state": "not_required",
        "validation_state": "review_prepared_pending_human_acceptance",
        "review_state": "prepared_pending_human_acceptance",
        "git_handoff_state": "not_required_for_ticket_result",
        "blocker_count": 0,
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
    }
    for key, value in invariant_expected.items():
        if invariants.get(key) != value:
            raise ProductRuntimeConflict(f"review-acceptance invariant {key} mismatch")
    return record


def _review_acceptance_next_ticket_snapshot_matches(
    record: dict[str, Any],
    current_next_ticket: dict[str, Any],
) -> bool:
    snapshot = record.get("next_ticket_authority")
    if not isinstance(snapshot, dict):
        return False
    action = record.get("next_action")
    if not isinstance(action, dict):
        return False
    if _review_acceptance_next_ticket_fields_match(
        record,
        action=action,
        expected=current_next_ticket,
    ):
        return True
    legacy_next_ticket = {
        "ticket_id": "P18.9.1",
        "ticket_title": "Pepper Design System",
        "authority_path": "2_products/pepper-agent/docs/agent-platform/workflow_migration_closure.md",
        "authority_section": "Advisory decomposition only, not implementation tickets",
        "authority_type": "current_repository_roadmap_authority",
        "auto_generated": False,
        "execution_authorized": False,
        "next_action_id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
    }
    return _review_acceptance_next_ticket_fields_match(
        record,
        action=action,
        expected=legacy_next_ticket,
    )


def _review_acceptance_next_ticket_fields_match(
    record: dict[str, Any],
    *,
    action: dict[str, Any],
    expected: dict[str, Any],
) -> bool:
    snapshot = record.get("next_ticket_authority")
    if not isinstance(snapshot, dict):
        return False
    required_snapshot = {
        "ticket_id": expected.get("ticket_id"),
        "ticket_title": expected.get("ticket_title"),
        "authority_path": expected.get("authority_path"),
        "authority_section": expected.get("authority_section"),
        "authority_type": expected.get("authority_type"),
        "auto_generated": expected.get("auto_generated"),
        "execution_authorized": expected.get("execution_authorized"),
        "next_action_id": expected.get("next_action_id"),
    }
    for key, value in required_snapshot.items():
        if snapshot.get(key) != value:
            return False
    if record.get("next_ticket_id") != expected.get("ticket_id"):
        return False
    if record.get("next_ticket_title") != expected.get("ticket_title"):
        return False
    if record.get("next_ticket_authority_path") != expected.get("authority_path"):
        return False
    if action.get("id") != expected.get("next_action_id"):
        return False
    if action.get("target_ticket_id") != expected.get("ticket_id"):
        return False
    if action.get("target_ticket_title") != expected.get("ticket_title"):
        return False
    if action.get("required_human_action") != "separate_next_ticket_generation":
        return False
    return True


def prepare_current_ticket_review(
    *,
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
) -> dict[str, Any]:
    """Prepare governed P18.9.0 review validation without accepting it."""

    request = CurrentTicketReviewPrepareRequest(
        project_id=project_id,
        ticket_id=ticket_id,
        next_action_id=next_action_id,
    )
    _validate_review_prepare_request_guards(request)
    projection = _load_current_projection_record()
    _validate_execution_start_authority(projection)

    existing = None
    try:
        existing = load_p18_9_0_review_prepare_record(projection_record=projection)
    except ProductRuntimeConflict:
        path = p18_9_0_review_prepare_record_path()
        _archive_existing_authority_record(
            path,
            p18_9_0_review_prepare_history_path(),
            reason="superseded_or_invalid_review_prepare_authority",
        )
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    if existing is not None:
        acceptance = load_p18_9_0_review_acceptance_record(
            projection_record=projection,
            review_prepare_record=existing,
        )
        if acceptance is not None:
            return _review_acceptance_operational_result(
                acceptance,
                idempotent_replay=True,
            )
        return _review_prepare_operational_result(existing, idempotent_replay=True)

    workflow = build_workflow_control_snapshot()
    workflow_blocker = _review_prepare_workflow_blocker(workflow)
    if workflow_blocker is not None:
        code, detail = workflow_blocker
        return _blocked_current_review_prepare_result(
            projection,
            request=request,
            blocker_code=code,
            blocker_detail=detail,
        )

    completion = _kanban_completion_result_source(projection)
    if completion.get("blocker_code"):
        return _blocked_current_review_prepare_result(
            projection,
            request=request,
            blocker_code=str(completion["blocker_code"]),
            blocker_detail=str(completion.get("blocker_detail") or "completion result detail is unavailable"),
            completion_source=completion,
        )
    acceptance_contract = _p18_9_0_acceptance_contract()
    record = _build_review_prepare_record(
        request=request,
        projection=projection,
        workflow=workflow,
        completion=completion,
        acceptance_contract=acceptance_contract,
    )
    _persist_review_prepare_record(record)
    return _review_prepare_operational_result(record, idempotent_replay=False)


def accept_current_ticket_review(
    *,
    human_acceptance_text: str,
    acceptor_id: str = "pepper-chat-human",
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
) -> dict[str, Any]:
    """Accept and close only the prepared P18.9.0 review package."""

    request = CurrentTicketReviewAcceptanceRequest(
        human_acceptance_text=human_acceptance_text,
        acceptor_id=acceptor_id,
        project_id=project_id,
        ticket_id=ticket_id,
        next_action_id=next_action_id,
    )
    _validate_review_acceptance_request_guards(request)
    projection = _load_current_projection_record()
    _validate_execution_start_authority(projection)
    review_prepare = load_p18_9_0_review_prepare_record(projection_record=projection)
    if review_prepare is None:
        return _blocked_current_review_acceptance_result(
            projection,
            request=request,
            blocker_code="REVIEW_PREPARE_AUTHORITY_GAP",
            blocker_detail="P18.9.0 review preparation authority is missing",
        )

    existing = None
    try:
        existing = load_p18_9_0_review_acceptance_record(
            projection_record=projection,
            review_prepare_record=review_prepare,
        )
    except ProductRuntimeConflict:
        path = p18_9_0_review_acceptance_record_path()
        _archive_existing_authority_record(
            path,
            p18_9_0_review_acceptance_history_path(),
            reason="superseded_or_invalid_review_acceptance_authority",
        )
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    if existing is not None:
        return _review_acceptance_operational_result(existing, idempotent_replay=True)

    workflow = build_workflow_control_snapshot()
    workflow_blocker = _review_acceptance_workflow_blocker(workflow)
    if workflow_blocker is not None:
        code, detail = workflow_blocker
        return _blocked_current_review_acceptance_result(
            projection,
            request=request,
            blocker_code=code,
            blocker_detail=detail,
            review_prepare_record=review_prepare,
        )

    record = _build_review_acceptance_record(
        request=request,
        projection=projection,
        workflow=workflow,
        review_prepare=review_prepare,
        next_ticket=_p18_9_next_ticket_authority(),
    )
    _persist_review_acceptance_record(record)
    return _review_acceptance_operational_result(record, idempotent_replay=False)


def start_current_ticket_execution(
    *,
    human_authorization_text: str,
    authorizer_id: str = "pepper-chat-human",
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
    spawn_fn: Any = None,
) -> dict[str, Any]:
    """Authorize and start only the current P18.9.0 Kanban worker or retry."""

    request = CurrentTicketExecutionStartRequest(
        human_authorization_text=human_authorization_text,
        authorizer_id=authorizer_id,
        project_id=project_id,
        ticket_id=ticket_id,
        next_action_id=next_action_id,
    )
    projection = _load_current_projection_record()
    _validate_execution_start_request_guards(request, projection_record=projection)
    _validate_execution_start_authority(projection)
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    workflow = build_workflow_control_snapshot()
    workflow_next_action = workflow.get("next_action")
    workflow_next_action_id = (
        workflow_next_action.get("id") if isinstance(workflow_next_action, dict) else None
    )

    if (
        request.next_action_id == binding.retry_start_next_action_id
        or (
            request.next_action_id is None
            and workflow_next_action_id == binding.retry_start_next_action_id
        )
    ):
        return _start_current_ticket_retry_execution(
            request=request,
            projection=projection,
            workflow=workflow,
            spawn_fn=spawn_fn,
        )

    authorization_diagnostics = execution_human_authorization_text_diagnostics(
        request.human_authorization_text,
        current_ticket_id=binding.ticket_id,
        requested_ticket_id=request.ticket_id,
        current_next_action_id=workflow_next_action_id,
        requested_next_action_id=request.next_action_id,
        expected_authorization_kind="execution_start_authorization",
    )
    if authorization_diagnostics is not None:
        return _blocked_current_execution_start_result(
            projection,
            request=request,
            blocker_code=str(authorization_diagnostics["blocker_code"]),
            blocker_detail=str(authorization_diagnostics["blocker_detail"]),
            authorization_diagnostics=authorization_diagnostics,
        )

    try:
        existing = load_p18_9_0_execution_start_record(projection_record=projection)
    except ProductRuntimeAuthorityMismatch as exc:
        return _blocked_current_execution_start_result(
            projection,
            request=request,
            blocker_code="EXECUTION_START_AUTHORITY_STALE",
            blocker_detail=str(exc),
            authorization_mismatch=exc.diagnostics,
        )
    if existing is not None and bool(existing.get("execution_started")):
        return _execution_start_operational_result(existing, idempotent_replay=True)

    workflow_blocker = _execution_start_workflow_blocker(workflow)
    if workflow_blocker is not None:
        code, detail = workflow_blocker
        return _blocked_current_execution_start_result(
            projection,
            request=request,
            blocker_code=code,
            blocker_detail=detail,
        )

    task_blocker = _kanban_start_preflight_blocker(projection)
    if task_blocker is not None:
        code, detail = task_blocker
        return _blocked_current_execution_start_result(
            projection,
            request=request,
            blocker_code=code,
            blocker_detail=detail,
        )

    provider_readiness = _executor_provider_readiness(projection["assignee_profile"])
    if not provider_readiness.get("ok"):
        return _blocked_current_execution_start_result(
            projection,
            request=request,
            blocker_code=str(
                provider_readiness.get("blocker_code") or "EXECUTOR_PROVIDER_RESOLUTION_GAP"
            ),
            blocker_detail=str(provider_readiness.get("blocker_detail") or "executor provider unavailable"),
            provider_readiness=provider_readiness,
        )

    worker_credential_probe = _preflight_pepper_governed_worker_credentials(
        projection,
        enabled=spawn_fn is None,
    )
    if not worker_credential_probe.get("ok"):
        return _blocked_current_execution_start_result(
            projection,
            request=request,
            blocker_code=str(
                worker_credential_probe.get("blocker_code")
                or "WORKER_CREDENTIAL_AUTHORITY_MISMATCH"
            ),
            blocker_detail=str(
                worker_credential_probe.get("blocker_detail")
                or "governed worker credential probe failed"
            ),
            provider_readiness=provider_readiness,
        )
    provider_readiness = dict(provider_readiness)
    provider_readiness["worker_credential_probe"] = worker_credential_probe

    authorization_record = _build_execution_start_authorization_record(
        request=request,
        projection=projection,
        provider_readiness=provider_readiness,
    )
    _persist_execution_start_record(authorization_record)
    dispatch_result = _dispatch_exact_current_kanban_task(
        projection,
        spawn_fn=spawn_fn,
    )
    final_record = _finalize_execution_start_record(
        authorization_record,
        dispatch_result=dispatch_result,
    )
    _persist_execution_start_record(final_record)
    return _execution_start_operational_result(final_record, idempotent_replay=False)


def recover_current_ticket_execution(
    *,
    human_authorization_text: str,
    authorizer_id: str = "pepper-chat-human",
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
) -> dict[str, Any]:
    """Record human recovery authorization for failed P18.9.0 without retrying."""

    request = CurrentTicketExecutionRecoveryRequest(
        human_authorization_text=human_authorization_text,
        authorizer_id=authorizer_id,
        project_id=project_id,
        ticket_id=ticket_id,
        next_action_id=next_action_id,
    )
    _validate_execution_recovery_request_guards(request)
    _validate_execution_recovery_authorization_text(request.human_authorization_text)
    projection = _load_current_projection_record()
    _validate_execution_start_authority(projection)
    existing = load_p18_9_0_recovery_action_record(projection_record=projection)
    if existing is not None and _recovery_record_matches_current_failure(projection, existing):
        if existing.get("human_authorization_text") != request.human_authorization_text:
            raise ProductRuntimeConflict(
                "P18.9.0 recovery was already recorded with different authorization text"
            )
        return _recovery_action_operational_result(existing, idempotent_replay=True)
    if existing is not None:
        _archive_existing_authority_record(
            p18_9_0_recovery_action_record_path(),
            p18_9_0_recovery_action_history_path(),
            reason="superseded_recovery_cycle",
        )
    workflow = build_workflow_control_snapshot()
    workflow_blocker = _execution_recovery_workflow_blocker(workflow)
    if workflow_blocker is not None:
        code, detail = workflow_blocker
        return _blocked_current_execution_recovery_result(
            projection,
            request=request,
            blocker_code=code,
            blocker_detail=detail,
        )

    retry_source = _kanban_recovery_source_state(projection)
    if retry_source.get("blocker_code"):
        return _blocked_current_execution_recovery_result(
            projection,
            request=request,
            blocker_code=str(retry_source["blocker_code"]),
            blocker_detail=str(retry_source.get("blocker_detail") or "retry source is unavailable"),
            retry_source=retry_source,
        )
    if int(retry_source["observed_attempt_count"]) >= int(retry_source["max_attempts"]):
        return _blocked_current_execution_recovery_result(
            projection,
            request=request,
            blocker_code="RETRY_BUDGET_EXHAUSTED",
            blocker_detail="P18.9.0 retry budget is exhausted",
            retry_source=retry_source,
        )

    record = _build_recovery_action_record(
        request=request,
        projection=projection,
        workflow=workflow,
        retry_source=retry_source,
    )
    _persist_recovery_action_record(record)
    return _recovery_action_operational_result(record, idempotent_replay=False)


def _start_current_ticket_retry_execution(
    *,
    request: CurrentTicketExecutionStartRequest,
    projection: dict[str, Any],
    workflow: dict[str, Any],
    spawn_fn: Any = None,
) -> dict[str, Any]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    workflow_next_action = workflow.get("next_action")
    workflow_next_action_id = (
        workflow_next_action.get("id") if isinstance(workflow_next_action, dict) else None
    )
    authorization_diagnostics = execution_human_authorization_text_diagnostics(
        request.human_authorization_text,
        current_ticket_id=binding.ticket_id,
        requested_ticket_id=request.ticket_id,
        current_next_action_id=workflow_next_action_id,
        requested_next_action_id=request.next_action_id,
        expected_authorization_kind="execution_retry_authorization",
    )
    if authorization_diagnostics is not None:
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code=str(authorization_diagnostics["blocker_code"]),
            blocker_detail=str(authorization_diagnostics["blocker_detail"]),
            authorization_diagnostics=authorization_diagnostics,
        )
    recovery_record = load_p18_9_0_recovery_action_record(projection_record=projection)
    if recovery_record is None:
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code="RECOVERY_AUTHORITY_GAP",
            blocker_detail="P18.9.0 retry start requires a persisted retry-pending recovery authority",
        )
    existing = load_p18_9_0_retry_start_record(
        projection_record=projection,
        recovery_record=recovery_record,
        allow_historical_mismatch=True,
    )
    if existing is not None:
        same_recovery_authority = (
            existing.get("recovery_action_SHA256") == recovery_record.get("recovery_action_SHA256")
        )
        existing_cycle_id = _retry_start_record_cycle_id(existing, recovery_record, projection)
        current_cycle_id = _recovery_record_cycle_id(recovery_record, projection)
        if (not same_recovery_authority) or existing_cycle_id != current_cycle_id:
            _archive_existing_authority_record(
                p18_9_0_retry_start_record_path(),
                p18_9_0_retry_start_history_path(),
                reason="superseded_recovery_cycle",
            )
            existing = None
    if existing is not None and bool(existing.get("execution_started")):
        return _retry_start_operational_result(existing, idempotent_replay=True)

    retry_source = _kanban_retry_start_source_state(projection, recovery_record)
    if retry_source.get("blocker_code"):
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code=str(retry_source["blocker_code"]),
            blocker_detail=str(retry_source.get("blocker_detail") or "retry source is unavailable"),
            recovery_record=recovery_record,
            retry_source=retry_source,
        )

    workflow_blocker = _execution_retry_start_workflow_blocker(workflow)
    if workflow_blocker is not None:
        code, detail = workflow_blocker
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code=code,
            blocker_detail=detail,
            recovery_record=recovery_record,
        )

    provider_readiness = _executor_provider_readiness(projection["assignee_profile"])
    if not provider_readiness.get("ok"):
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code=str(
                provider_readiness.get("blocker_code") or "EXECUTOR_PROVIDER_RESOLUTION_GAP"
            ),
            blocker_detail=str(provider_readiness.get("blocker_detail") or "executor provider unavailable"),
            recovery_record=recovery_record,
            retry_source=retry_source,
            provider_readiness=provider_readiness,
        )

    worker_credential_probe = _preflight_pepper_governed_worker_credentials(
        projection,
        enabled=spawn_fn is None,
    )
    if not worker_credential_probe.get("ok"):
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code=str(
                worker_credential_probe.get("blocker_code")
                or "WORKER_CREDENTIAL_AUTHORITY_MISMATCH"
            ),
            blocker_detail=str(
                worker_credential_probe.get("blocker_detail")
                or "governed worker credential probe failed"
            ),
            recovery_record=recovery_record,
            retry_source=retry_source,
            provider_readiness=provider_readiness,
        )
    provider_readiness = dict(provider_readiness)
    provider_readiness["worker_credential_probe"] = worker_credential_probe

    authorization_record = _build_retry_start_authorization_record(
        request=request,
        projection=projection,
        recovery_record=recovery_record,
        retry_source=retry_source,
        provider_readiness=provider_readiness,
    )
    _persist_retry_start_record(authorization_record)
    prep_result = _prepare_p18_9_0_retry_task_for_dispatch(
        projection=projection,
        recovery_record=recovery_record,
        retry_source=retry_source,
    )
    if prep_result.get("blocker_code"):
        final_record = _finalize_retry_start_record(
            authorization_record,
            prep_result=prep_result,
            dispatch_result=_dispatch_blocked_result(
                str(prep_result["blocker_code"]),
                str(prep_result.get("blocker_detail") or "retry task preparation failed"),
            ),
        )
        _persist_retry_start_record(final_record)
        return _retry_start_operational_result(final_record, idempotent_replay=False)

    dispatch_result = _dispatch_exact_current_kanban_task(
        projection,
        spawn_fn=spawn_fn,
    )
    final_record = _finalize_retry_start_record(
        authorization_record,
        prep_result=prep_result,
        dispatch_result=dispatch_result,
    )
    _persist_retry_start_record(final_record)
    return _retry_start_operational_result(final_record, idempotent_replay=False)


def _load_current_projection_record() -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        load_kanban_projection_record,
        load_p18_9_0_kanban_projection_record,
    )

    ticket_id = _current_projected_ticket_id_from_records()
    if ticket_id:
        projection = load_kanban_projection_record(ticket_id=ticket_id)
        if projection is not None:
            return projection
    projection = load_p18_9_0_kanban_projection_record()
    if projection is None:
        raise ProductRuntimeNotFound("current Kanban projection not found")
    return projection


def _validate_execution_start_request_guards(
    request: CurrentTicketExecutionStartRequest,
    *,
    projection_record: dict[str, Any] | None = None,
) -> None:
    binding = resolve_current_ticket_lifecycle_binding(
        projection_record=projection_record,
    )
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(f"execution start is bounded to project {binding.project_id}")
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(f"execution start is bounded to ticket {binding.ticket_id}")
    if request.next_action_id not in {
        None,
        binding.execution_start_next_action_id,
        binding.retry_start_next_action_id,
    }:
        raise ProductRuntimeConflict(
            "execution start requires "
            f"{binding.execution_start_next_action_id} or {binding.retry_start_next_action_id}"
        )


def execution_authorization_kind_for_action_id(
    next_action_id: str | None,
    *,
    ticket_id: str,
) -> str | None:
    action_ids = governed_ticket_lifecycle_action_ids(ticket_id)
    if next_action_id == action_ids["execution_start"]:
        return "execution_start_authorization"
    if next_action_id == action_ids["retry_start"]:
        return "execution_retry_authorization"
    return None


def expected_execution_authorization_kind(
    *,
    ticket_id: str,
    requested_next_action_id: str | None = None,
    current_next_action_id: str | None = None,
) -> str:
    return (
        execution_authorization_kind_for_action_id(
            requested_next_action_id,
            ticket_id=ticket_id,
        )
        or execution_authorization_kind_for_action_id(
            current_next_action_id,
            ticket_id=ticket_id,
        )
        or "execution_start_authorization"
    )


def execution_human_authorization_text_diagnostics(
    value: str,
    *,
    current_ticket_id: str,
    requested_ticket_id: str | None = None,
    current_next_action_id: str | None = None,
    requested_next_action_id: str | None = None,
    expected_authorization_kind: str | None = None,
) -> dict[str, Any] | None:
    expected_kind = expected_authorization_kind or expected_execution_authorization_kind(
        ticket_id=current_ticket_id,
        requested_next_action_id=requested_next_action_id,
        current_next_action_id=current_next_action_id,
    )
    raw = str(value or "").strip()
    normalized = _normalize_authorization_intent_text(raw)
    observed_kind = _observed_execution_authorization_kind(normalized)
    expected_next_action_id = (
        governed_ticket_lifecycle_action_ids(current_ticket_id)["retry_start"]
        if expected_kind == "execution_retry_authorization"
        else governed_ticket_lifecycle_action_ids(current_ticket_id)["execution_start"]
    )
    base = {
        "current_ticket_id": current_ticket_id,
        "requested_ticket_id": requested_ticket_id,
        "current_next_action_id": current_next_action_id,
        "requested_next_action_id": requested_next_action_id,
        "expected_next_action_id": expected_next_action_id,
        "authorization_kind": observed_kind,
        "expected_authorization_kind": expected_kind,
    }

    def blocked(code: str, detail: str) -> dict[str, Any]:
        return {
            **base,
            "blocker_code": code,
            "blocker_detail": detail,
        }

    if not raw:
        return blocked(
            "EXECUTION_HUMAN_AUTHORIZATION_TEXT_GAP",
            "human_authorization_text is required",
        )
    if "?" in raw or "¿" in raw:
        return blocked(
            "EXECUTION_HUMAN_AUTHORIZATION_TEXT_GAP",
            "execution authorization text must not be a question",
        )
    if _authorization_text_is_ambiguous(normalized):
        return blocked(
            "EXECUTION_HUMAN_AUTHORIZATION_TEXT_GAP",
            "execution authorization text is ambiguous",
        )
    if _authorization_text_has_recovery_intent(normalized):
        return blocked(
            "EXECUTION_AUTHORIZATION_KIND_MISMATCH",
            "execution authorization must not be recovery authorization",
        )

    mentioned_ticket_ids = _mentioned_authorization_ticket_ids(normalized)
    base["mentioned_ticket_ids"] = sorted(mentioned_ticket_ids)
    if not mentioned_ticket_ids:
        return blocked(
            "EXECUTION_HUMAN_AUTHORIZATION_TEXT_GAP",
            "execution authorization text must name the current ticket",
        )
    if current_ticket_id.upper() not in mentioned_ticket_ids:
        return blocked(
            "EXECUTION_AUTHORIZATION_TICKET_MISMATCH",
            "execution authorization targets a different ticket",
        )

    retry_intent = _authorization_text_has_retry_intent(normalized)
    start_intent = _authorization_text_has_start_intent(normalized)
    if expected_kind == "execution_start_authorization":
        if retry_intent:
            return blocked(
                "EXECUTION_AUTHORIZATION_KIND_MISMATCH",
                "initial execution start authorization must not be retry authorization",
            )
        if not start_intent:
            return blocked(
                "EXECUTION_HUMAN_AUTHORIZATION_TEXT_GAP",
                "explicit execution start authorization text is required",
            )
        return None

    if expected_kind == "execution_retry_authorization":
        if not retry_intent:
            return blocked(
                "EXECUTION_AUTHORIZATION_KIND_MISMATCH",
                "explicit execution retry authorization text is required",
            )
        return None

    return blocked(
        "EXECUTION_AUTHORIZATION_KIND_MISMATCH",
        f"unsupported execution authorization kind {expected_kind}",
    )


def _normalize_authorization_intent_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").strip())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.lower()


def _mentioned_authorization_ticket_ids(normalized: str) -> set[str]:
    return {match.group(0).upper() for match in re.finditer(r"\bP\d+(?:\.\d+)+\b", normalized, re.I)}


def _authorization_text_is_ambiguous(normalized: str) -> bool:
    return any(
        phrase in normalized
        for phrase in (
            "creo que",
            "pienso que",
            "tal vez",
            "parece que",
            "quizas",
            "quiza",
            "maybe",
            "probably",
            "looks like",
            "what if",
            "que pasa si",
            "si lo ejecuto",
            "if i start",
        )
    )


def _authorization_text_has_recovery_intent(normalized: str) -> bool:
    return bool(
        "recuperacion" in normalized
        or "recuperar" in normalized
        or re.search(r"\brecovery\b", normalized)
    )


def _authorization_text_has_retry_intent(normalized: str) -> bool:
    return bool(
        re.search(r"\b(retry|retries|retried|reintenta|reintentar|reintento)\b", normalized)
        or "segundo intento" in normalized
        or "volver a ejecutar" in normalized
    )


def _authorization_text_has_start_intent(normalized: str) -> bool:
    return bool(
        re.search(
            r"\b(start|execute|execution|dispatch|run|authorize|authorized|authorization|"
            r"inicia|iniciar|inicio|ejecuta|ejecutar|ejecucion|despacha|despachar|"
            r"lanza|lanzar|arranca|arrancar|autoriza|autorizo|autorizar|autorizado|"
            r"autorizacion)\b",
            normalized,
        )
    )


def _observed_execution_authorization_kind(normalized: str) -> str:
    if _authorization_text_has_recovery_intent(normalized):
        return "execution_recovery_authorization"
    if _authorization_text_has_retry_intent(normalized):
        return "execution_retry_authorization"
    if _authorization_text_has_start_intent(normalized):
        return "execution_start_authorization"
    return "unknown"


def _validate_execution_start_authority(projection: dict[str, Any]) -> None:
    validate_governed_ticket_lifecycle_projection_authority(projection)


def validate_governed_ticket_lifecycle_projection_authority(
    projection: dict[str, Any],
    *,
    binding: GovernedTicketLifecycleBinding | None = None,
) -> GovernedTicketLifecycleBinding:
    """Validate projection authority for the current governed ticket lifecycle."""

    binding = binding or resolve_current_ticket_lifecycle_binding(
        projection_record=projection,
    )
    if projection.get("project_id") != binding.project_id:
        raise ProductRuntimeConflict(f"{binding.ticket_id} projection project authority mismatch")
    if projection.get("macroproject_id") != binding.macroproject_id:
        raise ProductRuntimeConflict(f"{binding.ticket_id} projection macroproject authority mismatch")
    if projection.get("ticket_id") != binding.ticket_id:
        raise ProductRuntimeConflict(f"{binding.ticket_id} projection ticket authority mismatch")
    if projection.get("ticket_spec_SHA256") != binding.ticket_spec_sha256:
        raise ProductRuntimeConflict(f"{binding.ticket_id} TicketSpec SHA256 mismatch")
    if projection.get("work_packet_id") != binding.work_packet_id:
        raise ProductRuntimeConflict(f"{binding.ticket_id} WorkPacket ID mismatch")
    if projection.get("work_packet_SHA256") != binding.work_packet_sha256:
        raise ProductRuntimeConflict(f"{binding.ticket_id} WorkPacket SHA256 mismatch")
    if projection.get("WorkPacket_compilation_count") != binding.work_packet_compilation_count:
        raise ProductRuntimeConflict(f"{binding.ticket_id} WorkPacket compile count mismatch")
    if projection.get("approval_status") != "approved" or projection.get("approval_decision") != "approve":
        raise ProductRuntimeConflict(f"{binding.ticket_id} ticket approval authority is not approved")
    admission = projection.get("dependency_admission")
    if not isinstance(admission, dict) or admission.get("decision") != "admit":
        raise ProductRuntimeConflict(f"{binding.ticket_id} dependency admission is not admitted")
    if admission.get("dependency_blockers"):
        raise ProductRuntimeConflict(f"{binding.ticket_id} dependency blockers are present")
    if projection.get("workspace_kind") != "scratch":
        raise ProductRuntimeConflict(f"{binding.ticket_id} projection is not a scratch workspace")
    if projection.get("concurrent_workers_for_ticket") != 1:
        raise ProductRuntimeConflict(f"{binding.ticket_id} worker concurrency authority mismatch")
    if projection.get("task_max_retries") != 1:
        raise ProductRuntimeConflict(f"{binding.ticket_id} retry authority mismatch")
    next_action = projection.get("next_action")
    if not isinstance(next_action, dict) or next_action.get("id") != binding.execution_start_next_action_id:
        raise ProductRuntimeConflict(f"{binding.ticket_id} projection is not awaiting start authorization")
    return binding


def _validate_execution_recovery_request_guards(
    request: CurrentTicketExecutionRecoveryRequest,
) -> None:
    binding = resolve_current_ticket_lifecycle_binding()
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(f"execution recovery is bounded to project {binding.project_id}")
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(f"execution recovery is bounded to ticket {binding.ticket_id}")
    if request.next_action_id not in {None, binding.execution_recovery_next_action_id}:
        raise ProductRuntimeConflict(
            f"execution recovery requires {binding.execution_recovery_next_action_id}"
        )


def _validate_execution_recovery_authorization_text(value: str) -> None:
    if value.strip() != PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT:
        raise ProductRuntimeDecisionFailed(
            "exact explicit P18.9.0 recovery authorization text is required"
        )


def _execution_start_workflow_blocker(
    workflow: dict[str, Any],
) -> tuple[str, str] | None:
    binding = resolve_current_ticket_lifecycle_binding()
    if workflow.get("project_id") != binding.project_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current project is not {binding.project_id}"
    if workflow.get("macroproject_id") != binding.macroproject_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current macroproject is not {binding.macroproject_id}"
    if workflow.get("current_ticket_id") != binding.ticket_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current ticket is not {binding.ticket_id}"
    if workflow.get("workflow_status") != "queued":
        return "WORKFLOW_START_ACTION_GAP", "workflow status is not queued"
    if workflow.get("queue_state") != "kanban_projection_ready_not_dispatched":
        return "WORKFLOW_START_ACTION_GAP", "queue state is not ready for start authorization"
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        return "WORKFLOW_START_ACTION_GAP", "next action is unavailable"
    if next_action.get("id") != binding.execution_start_next_action_id:
        return "WORKFLOW_START_ACTION_GAP", "next action is not execution start authorization"
    if next_action.get("target_ticket_id") != binding.ticket_id:
        return "WORKFLOW_START_ACTION_GAP", f"next action does not target {binding.ticket_id}"
    if int(workflow.get("pending_ticket_approval_count") or 0) != 0:
        return "APPROVAL_STATE_GAP", "pending ticket approvals remain"
    if int(workflow.get("active_execution_count") or 0) != 0:
        return "EXECUTION_ALREADY_ACTIVE", "an execution is already active"
    blockers = workflow.get("remaining_blockers") or []
    if blockers:
        return "WORKFLOW_BLOCKER_PRESENT", "workflow blockers are present"
    return None


def _execution_recovery_workflow_blocker(
    workflow: dict[str, Any],
) -> tuple[str, str] | None:
    binding = resolve_current_ticket_lifecycle_binding()
    if workflow.get("project_id") != binding.project_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current project is not {binding.project_id}"
    if workflow.get("macroproject_id") != binding.macroproject_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current macroproject is not {binding.macroproject_id}"
    if workflow.get("current_ticket_id") != binding.ticket_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current ticket is not {binding.ticket_id}"
    if workflow.get("workflow_status") != "execution_failed":
        return "WORKFLOW_RECOVERY_ACTION_GAP", "workflow status is not execution_failed"
    if workflow.get("recovery_state") != "recovery_required":
        return "WORKFLOW_RECOVERY_ACTION_GAP", "recovery state is not recovery_required"
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        return "WORKFLOW_RECOVERY_ACTION_GAP", "next action is unavailable"
    if next_action.get("id") != binding.execution_recovery_next_action_id:
        return "WORKFLOW_RECOVERY_ACTION_GAP", "next action is not recovery authorization"
    if next_action.get("target_ticket_id") != binding.ticket_id:
        return "WORKFLOW_RECOVERY_ACTION_GAP", f"next action does not target {binding.ticket_id}"
    if int(workflow.get("pending_ticket_approval_count") or 0) != 0:
        return "APPROVAL_STATE_GAP", "pending ticket approvals remain"
    if int(workflow.get("active_execution_count") or 0) != 0:
        return "EXECUTION_ALREADY_ACTIVE", "an execution is already active"
    if workflow.get("execution_state") == "active_executions":
        return "EXECUTION_ALREADY_ACTIVE", "execution state is active"
    return None


def _execution_retry_start_workflow_blocker(
    workflow: dict[str, Any],
) -> tuple[str, str] | None:
    binding = resolve_current_ticket_lifecycle_binding()
    if workflow.get("project_id") != binding.project_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current project is not {binding.project_id}"
    if workflow.get("macroproject_id") != binding.macroproject_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current macroproject is not {binding.macroproject_id}"
    if workflow.get("current_ticket_id") != binding.ticket_id:
        return "WORKFLOW_AUTHORITY_GAP", f"current ticket is not {binding.ticket_id}"
    if workflow.get("workflow_status") != "retry_pending":
        return "WORKFLOW_RETRY_START_ACTION_GAP", "workflow status is not retry_pending"
    if workflow.get("recovery_state") != "retry_pending":
        return "WORKFLOW_RETRY_START_ACTION_GAP", "recovery state is not retry_pending"
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        return "WORKFLOW_RETRY_START_ACTION_GAP", "next action is unavailable"
    if next_action.get("id") != binding.retry_start_next_action_id:
        return "WORKFLOW_RETRY_START_ACTION_GAP", "next action is not retry-start authorization"
    if next_action.get("target_ticket_id") != binding.ticket_id:
        return "WORKFLOW_RETRY_START_ACTION_GAP", f"next action does not target {binding.ticket_id}"
    if int(workflow.get("pending_ticket_approval_count") or 0) != 0:
        return "APPROVAL_STATE_GAP", "pending ticket approvals remain"
    if int(workflow.get("active_execution_count") or 0) != 0:
        return "EXECUTION_ALREADY_ACTIVE", "an execution is already active"
    if workflow.get("execution_state") == "active_executions":
        return "EXECUTION_ALREADY_ACTIVE", "execution state is active"
    blockers = workflow.get("remaining_blockers") or []
    if blockers:
        return "WORKFLOW_BLOCKER_PRESENT", "workflow blockers are present"
    return None


def _kanban_recovery_source_state(projection: dict[str, Any]) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            return {
                "blocker_code": "KANBAN_TASK_GAP",
                "blocker_detail": "projected Kanban task is missing",
            }
        try:
            task_body = json.loads(task.body or "{}")
        except json.JSONDecodeError:
            task_body = {}
        synthetic_work_packet_id = f"WP-{board.upper()}-{task_id.upper()}"
        if task_body.get("WorkPacket_ID") == synthetic_work_packet_id:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": (
                    "synthetic Kanban execution-detail WorkPacket identity cannot be "
                    "treated as canonical P18.9.0 WorkPacket authority"
                ),
                "synthetic_work_packet_id": synthetic_work_packet_id,
            }
        if task_body.get("WorkPacket_ID") != projection["work_packet_id"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": "projected Kanban task WorkPacket ID does not match P18.9.0 authority",
                "observed_work_packet_id": task_body.get("WorkPacket_ID"),
                "canonical_work_packet_id": projection["work_packet_id"],
            }
        if task_body.get("WorkPacket_SHA256") != projection["work_packet_SHA256"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": "projected Kanban task WorkPacket SHA256 does not match P18.9.0 authority",
            }
        runs = kanban_db.list_runs(conn, task_id)
        active_runs = [run for run in runs if _execution_is_active(_run_dict(run))]
        if active_runs or task.current_run_id is not None:
            return {
                "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                "blocker_detail": "projected Kanban task still has active execution state",
            }
        worker_pid = getattr(task, "worker_pid", None)
        if worker_pid and kanban_db._pid_alive(int(worker_pid)):
            return {
                "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                "blocker_detail": "projected Kanban task still has a live worker process",
                "worker_pid": int(worker_pid),
            }
        if not runs:
            return {
                "blocker_code": "KANBAN_RUN_GAP",
                "blocker_detail": "projected Kanban task has no failed run evidence",
            }
        latest_run = runs[-1]
        latest_status = str(getattr(latest_run, "status", "") or "").strip().lower()
        latest_outcome = str(getattr(latest_run, "outcome", "") or "").strip().lower()
        if getattr(latest_run, "ended_at", None) is None:
            return {
                "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                "blocker_detail": "latest P18.9.0 run has not ended",
            }
        if task.status != "blocked" or (
            latest_outcome or latest_status
        ) not in _GOVERNED_TICKET_FAILURE_OUTCOMES:
            return {
                "blocker_code": "KANBAN_RECOVERY_SOURCE_GAP",
                "blocker_detail": "projected Kanban task is not blocked on failed run evidence",
                "kanban_task_status": task.status,
                "latest_run_status": latest_status,
                "latest_run_outcome": latest_outcome,
            }
        failure_fields = _run_failure_fields(latest_run)
        observed_attempt_count = len(runs)
        max_attempts = max(
            int(projection.get("task_max_retries") or 0) + 1,
            observed_attempt_count + 1,
        )
        return {
            "blocker_code": None,
            "blocker_detail": None,
            "kanban_board_slug": board,
            "kanban_task_id": task.id,
            "kanban_task_status": task.status,
            "kanban_task_assignee": task.assignee,
            "kanban_task_current_run_id": task.current_run_id,
            "kanban_task_workspace_kind": task.workspace_kind,
            "kanban_task_workspace_path": task.workspace_path,
            "kanban_task_claim_lock": task.claim_lock,
            "kanban_task_worker_pid": worker_pid,
            "observed_task_skills": list(task.skills or []),
            "observed_attempt_count": observed_attempt_count,
            "max_attempts": max_attempts,
            "next_attempt_number": observed_attempt_count + 1,
            "latest_run_id": latest_run.id,
            "latest_run_status": latest_status,
            "latest_run_outcome": latest_outcome,
            "latest_run_ended_at": getattr(latest_run, "ended_at", None),
            "failure_category": failure_fields.get("failure_category") or latest_outcome or latest_status,
            "failure_summary": failure_fields.get("failure_summary") or getattr(latest_run, "error", None),
            "synthetic_work_packet_id": synthetic_work_packet_id,
            "canonical_work_packet_id": projection["work_packet_id"],
            "Kanban_SQLite_canonical_authority": False,
        }
    finally:
        conn.close()


def _kanban_retry_start_source_state(
    projection: dict[str, Any],
    recovery_record: dict[str, Any],
) -> dict[str, Any]:
    retry_source = _kanban_recovered_retry_source_state(projection, recovery_record)
    if retry_source.get("blocker_code"):
        return retry_source
    if recovery_record.get("recovery_status") != "retry_pending":
        return {
            **retry_source,
            "blocker_code": "RECOVERY_AUTHORITY_GAP",
            "blocker_detail": "recovery authority is not retry_pending",
        }
    if recovery_record.get("retry_identity_model") != "same_kanban_task_new_run":
        return {
            **retry_source,
            "blocker_code": "RECOVERY_AUTHORITY_GAP",
            "blocker_detail": "recovery authority does not preserve same-task new-run identity",
        }
    if recovery_record.get("future_task_skills") != []:
        return {
            **retry_source,
            "blocker_code": "TASK_SKILL_EXECUTOR_CAPABILITY_MISMATCH",
            "blocker_detail": "recovery authority future task skills are not empty",
        }
    if recovery_record.get("unresolved_Hermes_task_skills") != []:
        return {
            **retry_source,
            "blocker_code": "TASK_SKILL_EXECUTOR_CAPABILITY_MISMATCH",
            "blocker_detail": "recovery authority still has unresolved Hermes task skills",
        }
    if recovery_record.get("future_retry_capability_surface") != "pepper_repository":
        return {
            **retry_source,
            "blocker_code": "TASK_SKILL_EXECUTOR_CAPABILITY_MISMATCH",
            "blocker_detail": "recovery authority does not bind retry to pepper_repository",
        }
    profile_toolsets = list(projection.get("profile_toolsets") or [])
    if "pepper_repository" not in profile_toolsets:
        return {
            **retry_source,
            "blocker_code": "PROFILE_ASSIGNMENT_GAP",
            "blocker_detail": "executor profile toolsets do not include pepper_repository",
        }
    if int(retry_source["observed_attempt_count"]) != int(recovery_record["observed_attempt_count"]):
        return {
            **retry_source,
            "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
            "blocker_detail": "observed attempt count no longer matches recovery authority",
        }
    if int(retry_source["next_attempt_number"]) != int(recovery_record["next_attempt_number"]):
        return {
            **retry_source,
            "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
            "blocker_detail": "next attempt number no longer matches recovery authority",
        }
    if int(retry_source["observed_attempt_count"]) >= int(retry_source["max_attempts"]):
        return {
            **retry_source,
            "blocker_code": "RETRY_BUDGET_EXHAUSTED",
            "blocker_detail": "P18.9.0 retry budget is exhausted",
        }
    if retry_source.get("latest_run_id") != recovery_record.get("latest_failed_run_id"):
        return {
            **retry_source,
            "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
            "blocker_detail": "latest failed run no longer matches recovery authority",
        }
    return retry_source


def _kanban_recovered_retry_source_state(
    projection: dict[str, Any],
    recovery_record: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            return {
                "blocker_code": "KANBAN_TASK_GAP",
                "blocker_detail": "projected Kanban task is missing",
            }
        try:
            task_body = json.loads(task.body or "{}")
        except json.JSONDecodeError:
            task_body = {}
        if not isinstance(task_body, dict):
            task_body = {}
        synthetic_work_packet_id = f"WP-{board.upper()}-{task_id.upper()}"
        if task_body.get("WorkPacket_ID") == synthetic_work_packet_id:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": (
                    "synthetic Kanban execution-detail WorkPacket identity cannot be "
                    "treated as canonical P18.9.0 WorkPacket authority"
                ),
                "synthetic_work_packet_id": synthetic_work_packet_id,
            }
        if task_body.get("WorkPacket_ID") != projection["work_packet_id"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": "projected Kanban task WorkPacket ID does not match P18.9.0 authority",
                "observed_work_packet_id": task_body.get("WorkPacket_ID"),
                "canonical_work_packet_id": projection["work_packet_id"],
            }
        if task_body.get("WorkPacket_SHA256") != projection["work_packet_SHA256"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": "projected Kanban task WorkPacket SHA256 does not match P18.9.0 authority",
            }
        runs = kanban_db.list_runs(conn, task_id)
        active_runs = [run for run in runs if _execution_is_active(_run_dict(run))]
        if active_runs or task.current_run_id is not None:
            return {
                "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                "blocker_detail": "projected Kanban task still has active execution state",
            }
        if task.claim_lock:
            return {
                "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
                "blocker_detail": "projected Kanban task has an unresolved current claim",
                "kanban_task_claim_lock": task.claim_lock,
            }
        worker_pid = getattr(task, "worker_pid", None)
        if worker_pid:
            if kanban_db._pid_alive(int(worker_pid)):
                return {
                    "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                    "blocker_detail": "projected Kanban task still has a live worker process",
                    "worker_pid": int(worker_pid),
                }
            return {
                "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
                "blocker_detail": f"projected Kanban task has unreconciled stale worker pid {int(worker_pid)}",
                "worker_pid": int(worker_pid),
            }
        if not runs:
            return {
                "blocker_code": "KANBAN_RUN_GAP",
                "blocker_detail": "projected Kanban task has no failed run evidence",
            }
        latest_run = runs[-1]
        latest_status = str(getattr(latest_run, "status", "") or "").strip().lower()
        latest_outcome = str(getattr(latest_run, "outcome", "") or "").strip().lower()
        if getattr(latest_run, "ended_at", None) is None:
            return {
                "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                "blocker_detail": "latest P18.9.0 run has not ended",
            }
        if latest_run.id != recovery_record.get("latest_failed_run_id"):
            return {
                "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
                "blocker_detail": "latest failed run no longer matches recovery authority",
                "latest_run_id": latest_run.id,
                "recovered_latest_failed_run_id": recovery_record.get("latest_failed_run_id"),
            }
        if (latest_outcome or latest_status) not in _GOVERNED_TICKET_FAILURE_OUTCOMES:
            return {
                "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
                "blocker_detail": "recovered latest run is no longer failed run evidence",
                "latest_run_status": latest_status,
                "latest_run_outcome": latest_outcome,
            }
        if task.status not in {"blocked", "ready"}:
            return {
                "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
                "blocker_detail": f"projected Kanban task status is {task.status}",
                "kanban_task_status": task.status,
            }
        failure_fields = _run_failure_fields(latest_run)
        observed_attempt_count = len(runs)
        max_attempts = max(
            int(projection.get("task_max_retries") or 0) + 1,
            observed_attempt_count + 1,
        )
        return {
            "blocker_code": None,
            "blocker_detail": None,
            "kanban_board_slug": board,
            "kanban_task_id": task.id,
            "kanban_task_status": task.status,
            "kanban_task_assignee": task.assignee,
            "kanban_task_current_run_id": task.current_run_id,
            "kanban_task_workspace_kind": task.workspace_kind,
            "kanban_task_workspace_path": task.workspace_path,
            "kanban_task_claim_lock": task.claim_lock,
            "kanban_task_worker_pid": worker_pid,
            "observed_task_skills": list(recovery_record.get("observed_task_skills") or []),
            "current_task_skills": list(task.skills or []),
            "historical_lifecycle_blocker_consumed": True,
            "observed_attempt_count": observed_attempt_count,
            "max_attempts": max_attempts,
            "next_attempt_number": observed_attempt_count + 1,
            "latest_run_id": latest_run.id,
            "latest_run_status": latest_status,
            "latest_run_outcome": latest_outcome,
            "latest_run_ended_at": getattr(latest_run, "ended_at", None),
            "failure_category": failure_fields.get("failure_category") or latest_outcome or latest_status,
            "failure_summary": failure_fields.get("failure_summary") or getattr(latest_run, "error", None),
            "synthetic_work_packet_id": synthetic_work_packet_id,
            "canonical_work_packet_id": projection["work_packet_id"],
            "Kanban_SQLite_canonical_authority": False,
        }
    finally:
        conn.close()


def _recovery_record_matches_current_failure(
    projection: dict[str, Any],
    recovery_record: dict[str, Any],
) -> bool:
    try:
        retry_source = _kanban_recovered_retry_source_state(projection, recovery_record)
    except Exception:
        return False
    if retry_source.get("blocker_code"):
        return False
    current_cycle_id = _p18_9_0_recovery_cycle_id(
        projection=projection,
        latest_failed_run_id=retry_source.get("latest_run_id"),
        observed_attempt_count=retry_source.get("observed_attempt_count"),
        failure_category=retry_source.get("failure_category"),
        failure_summary=retry_source.get("failure_summary"),
    )
    return _recovery_record_cycle_id(recovery_record, projection) == current_cycle_id


def _prepare_p18_9_0_retry_task_for_dispatch(
    *,
    projection: dict[str, Any],
    recovery_record: dict[str, Any],
    retry_source: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "KANBAN_TASK_GAP",
                "blocker_detail": "projected Kanban task is missing",
            }
        if task.status not in {"blocked", "ready"}:
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "KANBAN_RETRY_SOURCE_GAP",
                "blocker_detail": f"projected Kanban task status is {task.status}",
            }
        task_unblocked = False
        if task.status == "blocked":
            if not kanban_db.unblock_task(conn, task_id):
                return {
                    "task_prepare_status": "blocked",
                    "blocker_code": "KANBAN_UNBLOCK_FAILED",
                    "blocker_detail": "projected Kanban task could not be unblocked for retry",
                }
            task_unblocked = True
        task = kanban_db.get_task(conn, task_id)
        if task is None or task.status != "ready":
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "KANBAN_TASK_NOT_READY",
                "blocker_detail": "projected Kanban task did not become ready for retry",
            }
        if task.claim_lock or task.worker_pid or task.current_run_id is not None:
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
                "blocker_detail": "projected Kanban task has unresolved current lifecycle state",
            }
        body = {}
        try:
            body = json.loads(task.body or "{}")
        except json.JSONDecodeError:
            body = {}
        if isinstance(body, dict):
            body["task_skills"] = []
            body["retry_start_authorized"] = True
            body["retry_identity_model"] = recovery_record["retry_identity_model"]
            body["retry_attempt_number"] = recovery_record["next_attempt_number"]
            body["retry_authority_SHA256"] = recovery_record["recovery_action_SHA256"]
        else:
            body = {}
        conn.execute(
            "UPDATE tasks SET skills = ?, body = ?, claim_lock = NULL, "
            "claim_expires = NULL, worker_pid = NULL WHERE id = ? AND status = 'ready'",
            (json.dumps([]), json.dumps(body, sort_keys=True), task_id),
        )
        kanban_db._append_event(
            conn,
            task_id,
            "retry_prepared",
            {
                "source": PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM,
                "recovery_action_SHA256": recovery_record["recovery_action_SHA256"],
                "previous_attempt_count": retry_source["observed_attempt_count"],
                "next_attempt_number": recovery_record["next_attempt_number"],
                "future_task_skills": [],
            },
        )
        conn.commit()
        task = kanban_db.get_task(conn, task_id)
        return {
            "task_prepare_status": "prepared",
            "blocker_code": None,
            "blocker_detail": None,
            "task_unblocked": task_unblocked,
            "task_skills_corrected": True,
            "kanban_task_status_after_prepare": task.status if task is not None else None,
            "kanban_task_skills_after_prepare": list(task.skills or []) if task is not None else None,
        }
    finally:
        conn.close()


def _kanban_start_preflight_blocker(
    projection: dict[str, Any],
) -> tuple[str, str] | None:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            return "KANBAN_TASK_GAP", "projected Kanban task is missing"
        if task.assignee != projection["assignee_profile"]:
            return "KANBAN_TASK_GAP", "projected Kanban task assignee mismatch"
        if task.status != "ready":
            return "KANBAN_TASK_NOT_READY", f"projected Kanban task status is {task.status}"
        if task.claim_lock:
            return "KANBAN_TASK_NOT_READY", "projected Kanban task is already claimed"
        if task.worker_pid and kanban_db._pid_alive(int(task.worker_pid)):
            return "KANBAN_TASK_NOT_READY", "projected Kanban task still has a live worker process"
        if task.workspace_kind != "scratch":
            return "WORKSPACE_POLICY_GAP", "P18.9.0 start only authorizes scratch workspace dispatch"
        if task.max_retries != 1:
            return "KANBAN_TASK_GAP", "projected Kanban task retry policy mismatch"
        if task.skills:
            requested = ", ".join(str(item) for item in task.skills)
            return (
                "TASK_SKILL_EXECUTOR_CAPABILITY_MISMATCH",
                "projected Kanban task carries Hermes task skill(s) "
                f"{requested}; Pepper codebase inspection resolves through "
                "the bounded pepper_repository profile toolset",
            )
        running_for_profile = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'running' AND assignee = ?",
            (task.assignee,),
        ).fetchone()[0]
        if int(running_for_profile or 0) > 0:
            return "EXECUTOR_CONCURRENCY_CAP", "executor profile already has a running task"
        running_total = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'running'",
        ).fetchone()[0]
        if int(running_total or 0) > 0:
            return "EXECUTION_CONCURRENCY_CAP", "another Kanban execution is already running"
        guard = kanban_db.check_respawn_guard(conn, task_id)
        if guard is not None:
            return "KANBAN_RESPAWN_GUARD", guard
        return None
    finally:
        conn.close()


def _executor_provider_readiness(profile_name: str) -> dict[str, Any]:
    try:
        from hermes_cli.agent_platform.worker_credentials import (
            probe_pepper_governed_executor_profile_readiness,
        )

        return probe_pepper_governed_executor_profile_readiness(profile_name)
    except Exception as exc:
        category = getattr(exc, "validation_category", exc.__class__.__name__)
        return {
            "ok": False,
            "blocker_code": "EXECUTOR_PROVIDER_RESOLUTION_GAP",
            "blocker_detail": f"executor provider resolution failed: {_safe_text(category, limit=200)}",
            "validation_category": _safe_text(category, limit=200),
            "legacy_auth_json_used": False,
            "API_key_fallback_used": False,
            "credential_pool_fallback_used": False,
            "governed_refresh_path": "provider_worker_resolution_no_refresh",
            "legacy_refresh_fallback": False,
        }


def _pepper_governed_worker_env_overlay(projection: dict[str, Any]) -> dict[str, str]:
    from hermes_cli.agent_platform.worker_credentials import (
        build_pepper_governed_worker_credential_binding,
        pepper_governed_worker_env,
    )
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        approval_decision_record_path_for_ticket,
        generation_record_path_for_ticket,
    )
    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        kanban_projection_record_path_for_ticket,
    )

    ticket_id = _safe_text(projection.get("ticket_id") or PEPPER_NEXT_TICKET_ID, limit=128)
    authority = projection.get("authority") if isinstance(projection.get("authority"), dict) else {}
    projection_sha256 = str(projection.get("projection_SHA256") or authority.get("projection_SHA256") or "")
    if not projection_sha256:
        raise ProductRuntimeConflict("Kanban projection digest is unavailable for worker env overlay")
    binding = build_pepper_governed_worker_credential_binding(
        project_id=str(projection.get("project_id") or PEPPER_GOVERNED_PROJECT_ID),
        ticket_id=ticket_id,
        work_packet_id=str(projection["work_packet_id"]),
        work_packet_SHA256=str(projection["work_packet_SHA256"]),
        ticket_spec_SHA256=str(projection["ticket_spec_SHA256"]),
        kanban_task_id=str(projection["kanban_task_id"]),
        executor_profile=str(projection["assignee_profile"]),
        projection_SHA256=projection_sha256,
        profile_assignment_policy_id=str(projection.get("profile_assignment_policy_id") or ""),
        profile_assignment_policy_revision=str(projection.get("profile_assignment_policy_revision") or ""),
    )
    overlay = pepper_governed_worker_env(binding=binding)
    overlay.update({
        "HERMES_AGENT_PLATFORM_WORKPACKET_ID": str(projection["work_packet_id"]),
        "HERMES_AGENT_PLATFORM_WORKPACKET_SHA256": str(projection["work_packet_SHA256"]),
        "HERMES_AGENT_PLATFORM_TICKET_SPEC_SHA256": str(projection["ticket_spec_SHA256"]),
        "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_SHA256": projection_sha256,
        "HERMES_AGENT_PLATFORM_GENERATION_RECORD_PATH": str(
            generation_record_path_for_ticket(ticket_id)
        ),
        "HERMES_AGENT_PLATFORM_APPROVAL_DECISION_RECORD_PATH": str(
            approval_decision_record_path_for_ticket(ticket_id)
        ),
        "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_RECORD_PATH": str(
            kanban_projection_record_path_for_ticket(ticket_id)
        ),
    })
    return overlay


def _pepper_governed_worker_probe_env(projection: dict[str, Any]) -> dict[str, str]:
    from hermes_cli.profiles import normalize_profile_name, resolve_profile_env

    profile_arg = normalize_profile_name(str(projection["assignee_profile"]))
    env = dict(os.environ)
    try:
        env["HERMES_HOME"] = resolve_profile_env(profile_arg)
    except FileNotFoundError:
        pass
    env["HERMES_PROFILE"] = profile_arg
    env.update(_pepper_governed_worker_env_overlay(projection))
    return env


def _preflight_pepper_governed_worker_credentials(
    projection: dict[str, Any],
    *,
    enabled: bool = True,
) -> dict[str, Any]:
    if not enabled:
        return {
            "ok": True,
            "probe_status": "skipped_test_spawn_override",
            "credential_resolution_source": "not_applicable",
        }
    try:
        from hermes_cli.agent_platform.worker_credentials import (
            probe_pepper_governed_worker_credentials,
        )

        env = _pepper_governed_worker_probe_env(projection)
        probe = probe_pepper_governed_worker_credentials(env=env)
        return {
            "ok": True,
            "probe_status": "passed",
            "provider": probe.get("provider"),
            "model": probe.get("model"),
            "api_mode": probe.get("api_mode"),
            "credential_profile_id": probe.get("credential_profile_id"),
            "credential_policy_revision": probe.get("credential_policy_revision"),
            "credential_resolution_source": probe.get("credential_resolution_source"),
            "provider_runtime_profile_id": probe.get("provider_runtime_profile_id"),
            "worker_profile_id": probe.get("worker_profile_id"),
            "executor_profile": probe.get("executor_profile"),
            "work_packet_id": probe.get("work_packet_id"),
            "work_packet_SHA256": probe.get("work_packet_SHA256"),
            "runtime_id": probe.get("runtime_id"),
            "correlation_id": probe.get("correlation_id"),
            "lease_id": probe.get("lease_id"),
            "legacy_auth_json_used": False,
            "API_key_fallback_used": False,
            "credential_pool_fallback_used": False,
            "legacy_refresh_fallback": False,
            "credential_refresh_calls_per_request_maximum": 0,
            "human_smoke_marker": probe.get("human_smoke_marker"),
        }
    except Exception as exc:
        category = getattr(exc, "validation_category", exc.__class__.__name__)
        return {
            "ok": False,
            "probe_status": "failed",
            "blocker_code": "WORKER_CREDENTIAL_AUTHORITY_MISMATCH",
            "blocker_detail": (
                "governed Pepper worker credential probe failed: "
                f"{_safe_text(category, limit=200)}"
            ),
            "validation_category": _safe_text(category, limit=200),
            "legacy_auth_json_used": False,
            "API_key_fallback_used": False,
            "credential_pool_fallback_used": False,
            "legacy_refresh_fallback": False,
        }


def _dispatch_exact_current_kanban_task(
    projection: dict[str, Any],
    *,
    spawn_fn: Any = None,
) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    claimed = None
    try:
        blocker = _kanban_start_preflight_blocker(projection)
        if blocker is not None:
            code, detail = blocker
            task = kanban_db.get_task(conn, task_id)
            runs = kanban_db.list_runs(conn, task_id) if task is not None else []
            return _dispatch_blocked_result(
                code,
                detail,
                task=task,
                runs=runs,
            )
        claimed = kanban_db.claim_task(
            conn,
            task_id,
            claimer=f"{kanban_db._claimer_id()}:pepper-worker-start-action",
        )
        if claimed is None:
            task = kanban_db.get_task(conn, task_id)
            runs = kanban_db.list_runs(conn, task_id) if task is not None else []
            return _dispatch_blocked_result(
                "KANBAN_CLAIM_FAILED",
                "projected Kanban task could not be claimed",
                task=task,
                runs=runs,
            )
        try:
            workspace = kanban_db.resolve_workspace(claimed, board=board)
            kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
            kanban_db._maybe_emit_scratch_tip(conn, claimed.id, claimed.workspace_kind)
        except Exception as exc:
            kanban_db._record_spawn_failure(
                conn,
                claimed.id,
                f"workspace: {_safe_text(exc, limit=300)}",
                failure_limit=1,
            )
            task = kanban_db.get_task(conn, task_id)
            runs = kanban_db.list_runs(conn, task_id) if task is not None else []
            return _dispatch_blocked_result(
                "WORKSPACE_POLICY_GAP",
                str(exc) or "workspace resolution failed",
                task=task,
                runs=runs,
                dispatch_performed=True,
            )
        env_overlay = _pepper_governed_worker_env_overlay(projection)
        spawn = spawn_fn if spawn_fn is not None else kanban_db._default_spawn
        try:
            import inspect

            try:
                signature = inspect.signature(spawn)
                kwargs: dict[str, Any] = {}
                accepts_kwargs = any(
                    param.kind is inspect.Parameter.VAR_KEYWORD
                    for param in signature.parameters.values()
                )
                if "board" in signature.parameters or accepts_kwargs:
                    kwargs["board"] = board
                if "env_overlay" in signature.parameters or accepts_kwargs:
                    kwargs["env_overlay"] = env_overlay
                pid = spawn(claimed, str(workspace), **kwargs)
            except (TypeError, ValueError):
                pid = spawn(claimed, str(workspace))
            if pid:
                kanban_db._set_worker_pid(conn, claimed.id, int(pid))
        except Exception as exc:
            kanban_db._record_spawn_failure(
                conn,
                claimed.id,
                _safe_text(exc, limit=300),
                failure_limit=1,
            )
            task = kanban_db.get_task(conn, task_id)
            runs = kanban_db.list_runs(conn, task_id) if task is not None else []
            return _dispatch_blocked_result(
                "KANBAN_WORKER_SPAWN_FAILED",
                str(exc) or "worker spawn failed",
                task=task,
                runs=runs,
                dispatch_performed=True,
            )
        task = kanban_db.get_task(conn, task_id)
        runs = kanban_db.list_runs(conn, task_id)
        return {
            "start_status": "started",
            "blocker_code": None,
            "blocker_detail": None,
            "dispatch_performed": True,
            "execution_started": True,
            "worker_execution": bool(pid),
            "worker_process_started": bool(pid),
            "worker_pid_recorded": bool(pid),
            "Kanban_dispatch": True,
            "kanban_task_status": task.status if task is not None else "running",
            "kanban_run_id": task.current_run_id if task is not None else None,
            "workspace_path": task.workspace_path if task is not None else str(workspace),
            "workspace_created": True,
            "runs": [_run_dict(run) for run in runs],
        }
    finally:
        conn.close()


def _dispatch_blocked_result(
    blocker_code: str,
    blocker_detail: str,
    *,
    task: Any = None,
    runs: list[Any] | None = None,
    dispatch_performed: bool = False,
) -> dict[str, Any]:
    return {
        "start_status": "blocked",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        "dispatch_performed": dispatch_performed,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "worker_pid_recorded": False,
        "Kanban_dispatch": dispatch_performed,
        "kanban_task_status": getattr(task, "status", None),
        "kanban_run_id": getattr(task, "current_run_id", None),
        "workspace_path": getattr(task, "workspace_path", None),
        "workspace_created": False,
        "runs": [_run_dict(run) for run in (runs or [])],
    }


def _build_execution_start_authorization_record(
    *,
    request: CurrentTicketExecutionStartRequest,
    projection: dict[str, Any],
    provider_readiness: dict[str, Any],
) -> dict[str, Any]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    record = {
        "schema_version": PEPPER_WORKER_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_WORKER_START_ACTION_POLICY_ID,
        "source_system": PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM,
        "created_at": _utc_now_iso(),
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "execution_profile_role": projection["execution_profile_role"],
        "selected_role": projection["selected_role"],
        "profile_assignment_policy_id": projection["profile_assignment_policy_id"],
        "authorizer_id": request.authorizer_id,
        "authorization_reference": f"human_authorized_start:{binding.ticket_id}",
        "human_authorization_text": request.human_authorization_text,
        "execution_authorized": True,
        "synthetic": False,
        "ticket_execution_authorized": True,
        "WorkPacket_execution_authorized": True,
        "runtime_execution_authorized": True,
        "provider": provider_readiness["provider"],
        "model": provider_readiness["model"],
        "api_mode": provider_readiness["api_mode"],
        "credential_profile_id": provider_readiness["credential_profile_id"],
        "credential_policy_revision": provider_readiness.get("credential_policy_revision"),
        "provider_runtime_profile_id": provider_readiness["provider_runtime_profile_id"],
        "worker_profile_id": provider_readiness["worker_profile_id"],
        "executor_config_source": provider_readiness["executor_config_source"],
        "workspace_kind": "scratch",
        "workspace_path": None,
        "workspace_created": False,
        "dispatcher_primitive": "kanban_db.claim_task+resolve_workspace+_default_spawn",
        "max_spawn": 1,
        "max_in_progress_per_profile": 1,
        "start_status": "authorized_pending_dispatch",
        "blocker_code": None,
        "blocker_detail": None,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "worker_pid_recorded": False,
        "Kanban_dispatch": False,
        "kanban_task_status": "ready",
        "kanban_run_id": None,
        "command_execution_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    record["start_authorization_SHA256"] = _execution_start_record_digest(record)
    return record


def _build_recovery_action_record(
    *,
    request: CurrentTicketExecutionRecoveryRequest,
    projection: dict[str, Any],
    workflow: dict[str, Any],
    retry_source: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.retry_incident_rollback import (
        RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION,
        RETRY_INCIDENT_ROLLBACK_POLICY_ID,
        RetryIncidentRollbackRequestedAction,
        build_retry_incident_rollback_human_authorization,
    )

    observed_at = _utc_now_iso()
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    authorization = build_retry_incident_rollback_human_authorization(
        action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
        authorizer_id=request.authorizer_id,
        authorization_reference=request.human_authorization_text,
        rationale=(
            f"Authorize {binding.ticket_id} retry-pending governance after failed run 1 "
            "without starting run 2 or mutating Kanban."
        ),
        authorized_at=observed_at,
    )
    observed_attempt_count = int(retry_source["observed_attempt_count"])
    max_attempts = int(retry_source["max_attempts"])
    next_attempt_number = int(retry_source["next_attempt_number"])
    recovery_cycle_id = _p18_9_0_recovery_cycle_id(
        projection=projection,
        latest_failed_run_id=retry_source.get("latest_run_id"),
        observed_attempt_count=observed_attempt_count,
        failure_category=retry_source.get("failure_category"),
        failure_summary=retry_source.get("failure_summary"),
    )
    record = {
        "schema_version": PEPPER_RECOVERY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RECOVERY_ACTION_POLICY_ID,
        "source_system": PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
        "P18_6_policy_id": RETRY_INCIDENT_ROLLBACK_POLICY_ID,
        "runtime_boundary_classification": RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION,
        "created_at": observed_at,
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "execution_start_authority_SHA256": workflow.get("execution_start_authority", {}).get(
            "start_authorization_SHA256"
        ),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "authorizer_id": request.authorizer_id,
        "human_authorization_text": request.human_authorization_text,
        "human_authorization": authorization.model_dump(mode="json"),
        "human_authorization_SHA256": authorization.authorization_SHA256,
        "recovery_cycle_id": recovery_cycle_id,
        "requested_action": "authorize_retry",
        "recovery_status": "retry_pending",
        "governed_workflow_transition_id": "GWT-023",
        "governed_workflow_transition": "FAILED->RETRY_PENDING",
        "retry_identity_model": "same_kanban_task_new_run",
        "future_retry_prepared": True,
        "future_retry_requires_separate_start_authorization": True,
        "future_retry_next_action_id": binding.retry_start_next_action_id,
        "future_task_skills": [],
        "future_retry_capability_surface": "pepper_repository",
        "semantic_capabilities": list(projection.get("semantic_capabilities") or []),
        "capability_resolution": list(projection.get("capability_resolution") or []),
        "unresolved_Hermes_task_skills": [],
        "observed_task_skills": list(retry_source.get("observed_task_skills") or []),
        "observed_attempt_count": observed_attempt_count,
        "max_attempts": max_attempts,
        "next_attempt_number": next_attempt_number,
        "retry_budget_exhausted": False,
        "latest_failed_run_id": retry_source["latest_run_id"],
        "latest_failed_run_status": retry_source["latest_run_status"],
        "latest_failed_run_outcome": retry_source["latest_run_outcome"],
        "latest_failed_run_ended_at": retry_source.get("latest_run_ended_at"),
        "failure_category": workflow.get("failure_category") or retry_source.get("failure_category"),
        "failure_summary": workflow.get("failure_summary") or retry_source.get("failure_summary"),
        "kanban_task_status_at_recovery": retry_source["kanban_task_status"],
        "kanban_task_workspace_kind": retry_source["kanban_task_workspace_kind"],
        "kanban_task_workspace_path": retry_source.get("kanban_task_workspace_path"),
        "canonical_work_packet_id": projection["work_packet_id"],
        "synthetic_kanban_work_packet_id": retry_source.get("synthetic_work_packet_id"),
        "Kanban_SQLite_canonical_authority": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "retry_execution_count": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": "PEPPER-RECOVERY-ACTION-READY-FOR-HUMAN-SMOKE",
    }
    record["recovery_action_SHA256"] = _recovery_action_record_digest(record)
    return record


def _build_retry_start_authorization_record(
    *,
    request: CurrentTicketExecutionStartRequest,
    projection: dict[str, Any],
    recovery_record: dict[str, Any],
    retry_source: dict[str, Any],
    provider_readiness: dict[str, Any],
) -> dict[str, Any]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    record = {
        "schema_version": PEPPER_RETRY_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RETRY_START_ACTION_POLICY_ID,
        "source_system": PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM,
        "created_at": _utc_now_iso(),
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "execution_start_authority_SHA256": recovery_record.get("execution_start_authority_SHA256"),
        "recovery_action_SHA256": recovery_record["recovery_action_SHA256"],
        "recovery_cycle_id": _recovery_record_cycle_id(recovery_record, projection),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "execution_profile_role": projection["execution_profile_role"],
        "selected_role": projection["selected_role"],
        "profile_assignment_policy_id": projection["profile_assignment_policy_id"],
        "profile_toolsets": list(projection.get("profile_toolsets") or []),
        "authorizer_id": request.authorizer_id,
        "authorization_reference": f"human_authorized_retry_start:{binding.ticket_id}",
        "human_authorization_text": request.human_authorization_text,
        "requested_action": "start_retry",
        "recovery_status_at_authorization": "retry_pending",
        "retry_start_authorized": True,
        "execution_authorized": True,
        "synthetic": False,
        "ticket_execution_authorized": True,
        "WorkPacket_execution_authorized": True,
        "runtime_execution_authorized": True,
        "retry_identity_model": "same_kanban_task_new_run",
        "previous_attempt_count": int(recovery_record["observed_attempt_count"]),
        "next_attempt_number": int(recovery_record["next_attempt_number"]),
        "max_attempts": int(recovery_record["max_attempts"]),
        "latest_failed_run_id": recovery_record["latest_failed_run_id"],
        "latest_failed_run_status": recovery_record["latest_failed_run_status"],
        "latest_failed_run_outcome": recovery_record["latest_failed_run_outcome"],
        "failure_category": recovery_record.get("failure_category") or retry_source.get("failure_category"),
        "failure_summary": recovery_record.get("failure_summary") or retry_source.get("failure_summary"),
        "future_task_skills": [],
        "future_retry_capability_surface": "pepper_repository",
        "unresolved_Hermes_task_skills": [],
        "observed_task_skills": list(retry_source.get("observed_task_skills") or []),
        "provider": provider_readiness["provider"],
        "model": provider_readiness["model"],
        "api_mode": provider_readiness["api_mode"],
        "credential_profile_id": provider_readiness["credential_profile_id"],
        "credential_policy_revision": provider_readiness.get("credential_policy_revision"),
        "provider_runtime_profile_id": provider_readiness["provider_runtime_profile_id"],
        "worker_profile_id": provider_readiness["worker_profile_id"],
        "executor_config_source": provider_readiness["executor_config_source"],
        "workspace_kind": "scratch",
        "workspace_path": None,
        "workspace_created": False,
        "dispatcher_primitive": "kanban_db.unblock_task+kanban_db.claim_task+resolve_workspace+_default_spawn",
        "max_spawn": 1,
        "max_in_progress_per_profile": 1,
        "task_prepare_status": "pending",
        "task_unblocked": False,
        "task_skills_corrected": False,
        "start_status": "authorized_pending_dispatch",
        "blocker_code": None,
        "blocker_detail": None,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "worker_pid_recorded": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "retry_execution_count": 0,
        "second_run_started": False,
        "kanban_task_status": "blocked",
        "kanban_run_id": None,
        "command_execution_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": "PEPPER-RETRY-START-ACTION-READY-FOR-HUMAN-SMOKE",
    }
    record["retry_start_authorization_SHA256"] = _retry_start_record_digest(record)
    return record


def _finalize_execution_start_record(
    record: dict[str, Any],
    *,
    dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(record)
    for key in (
        "start_status",
        "blocker_code",
        "blocker_detail",
        "dispatch_performed",
        "execution_started",
        "worker_execution",
        "worker_process_started",
        "worker_pid_recorded",
        "Kanban_dispatch",
        "kanban_task_status",
        "kanban_run_id",
        "workspace_path",
        "workspace_created",
    ):
        updated[key] = dispatch_result.get(key)
    updated["updated_at"] = _utc_now_iso()
    updated.pop("start_authorization_SHA256", None)
    updated["start_authorization_SHA256"] = _execution_start_record_digest(updated)
    return updated


def _finalize_retry_start_record(
    record: dict[str, Any],
    *,
    prep_result: dict[str, Any],
    dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(record)
    for key in (
        "task_prepare_status",
        "task_unblocked",
        "task_skills_corrected",
    ):
        if key in prep_result:
            updated[key] = prep_result.get(key)
    for key in (
        "start_status",
        "blocker_code",
        "blocker_detail",
        "dispatch_performed",
        "execution_started",
        "worker_execution",
        "worker_process_started",
        "worker_pid_recorded",
        "Kanban_dispatch",
        "kanban_task_status",
        "kanban_run_id",
        "workspace_path",
        "workspace_created",
    ):
        updated[key] = dispatch_result.get(key)
    runs = dispatch_result.get("runs") if isinstance(dispatch_result.get("runs"), list) else []
    updated["retry_execution_started"] = bool(dispatch_result.get("execution_started"))
    updated["retry_execution_count"] = 1 if bool(dispatch_result.get("dispatch_performed")) else 0
    updated["second_run_started"] = len(runs) >= int(updated["next_attempt_number"])
    updated["updated_at"] = _utc_now_iso()
    updated.pop("retry_start_authorization_SHA256", None)
    updated["retry_start_authorization_SHA256"] = _retry_start_record_digest(updated)
    return updated


def _blocked_current_execution_start_result(
    projection: dict[str, Any],
    *,
    request: CurrentTicketExecutionStartRequest,
    blocker_code: str,
    blocker_detail: str,
    provider_readiness: dict[str, Any] | None = None,
    authorization_mismatch: dict[str, Any] | None = None,
    authorization_diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_system": PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_WORKER_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_WORKER_START_ACTION_POLICY_ID,
        "start_status": "blocked",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        **_current_ticket_projection_identity_fields(projection),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "human_authorization_present": True,
        "human_authorization_text": request.human_authorization_text,
        "execution_authorization_recorded": False,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "provider_readiness": provider_readiness,
        "authorization_mismatch": authorization_mismatch,
        "authorization_diagnostics": authorization_diagnostics,
    }


def _blocked_current_execution_recovery_result(
    projection: dict[str, Any],
    *,
    request: CurrentTicketExecutionRecoveryRequest,
    blocker_code: str,
    blocker_detail: str,
    retry_source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_system": PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_RECOVERY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RECOVERY_ACTION_POLICY_ID,
        "recovery_status": "blocked",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        **_current_ticket_projection_identity_fields(projection),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "human_authorization_present": True,
        "human_authorization_text": request.human_authorization_text,
        "recovery_authorization_recorded": False,
        "future_retry_prepared": False,
        "retry_identity_model": "same_kanban_task_new_run",
        "future_task_skills": [],
        "future_retry_capability_surface": "pepper_repository",
        "unresolved_Hermes_task_skills": [],
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "retry_execution_count": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "retry_source": retry_source,
    }


def _blocked_current_execution_retry_start_result(
    projection: dict[str, Any],
    *,
    request: CurrentTicketExecutionStartRequest,
    blocker_code: str,
    blocker_detail: str,
    recovery_record: dict[str, Any] | None = None,
    retry_source: dict[str, Any] | None = None,
    provider_readiness: dict[str, Any] | None = None,
    authorization_diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_system": PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_RETRY_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RETRY_START_ACTION_POLICY_ID,
        "start_status": "blocked",
        "retry_start_status": "blocked",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        **_current_ticket_projection_identity_fields(projection),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "human_authorization_present": True,
        "human_authorization_text": request.human_authorization_text,
        "retry_start_authorization_recorded": False,
        "recovery_action_SHA256": (
            recovery_record.get("recovery_action_SHA256") if recovery_record else None
        ),
        "recovery_status": (
            recovery_record.get("recovery_status") if recovery_record else None
        ),
        "retry_identity_model": "same_kanban_task_new_run",
        "future_task_skills": [],
        "future_retry_capability_surface": "pepper_repository",
        "unresolved_Hermes_task_skills": [],
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "retry_execution_count": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "retry_source": retry_source,
        "provider_readiness": provider_readiness,
        "authorization_diagnostics": authorization_diagnostics,
    }


def _recovery_action_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool,
) -> dict[str, Any]:
    from hermes_cli import kanban_db

    action_ids = governed_ticket_lifecycle_action_ids(str(record["ticket_id"]))
    board = _normalize_board(str(record["kanban_board_slug"]))
    task_id = str(record["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        runs = kanban_db.list_runs(conn, task_id) if task is not None else []
    finally:
        conn.close()
    task_visibility = None
    if task is not None:
        task_visibility = {
            "id": task.id,
            "status": task.status,
            "assignee": task.assignee,
            "workspace_kind": task.workspace_kind,
            "workspace_path": task.workspace_path,
            "current_run_id": task.current_run_id,
            "skills": list(task.skills or []),
        }
    current_side_effects = {
        "dispatch_performed": False,
        "Kanban_dispatch": False,
        "execution_started": False,
        "worker_process_started": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    return {
        "source_system": PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_RECOVERY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RECOVERY_ACTION_POLICY_ID,
        "P18_6_policy_id": record["P18_6_policy_id"],
        "runtime_boundary_classification": record["runtime_boundary_classification"],
        "idempotent_replay": idempotent_replay,
        "recovery_status": record["recovery_status"],
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "recovery_action_SHA256": record["recovery_action_SHA256"],
        "recovery_cycle_id": record.get("recovery_cycle_id"),
        "human_authorization_SHA256": record["human_authorization_SHA256"],
        "human_authorization_id": record["human_authorization"]["authorization_id"],
        "human_authorization_text": record["human_authorization_text"],
        "recovery_authorization_recorded": True,
        "current_invocation_side_effects": current_side_effects,
        "requested_action": record["requested_action"],
        "governed_workflow_transition_id": record["governed_workflow_transition_id"],
        "governed_workflow_transition": record["governed_workflow_transition"],
        "future_retry_prepared": record["future_retry_prepared"],
        "future_retry_requires_separate_start_authorization": record[
            "future_retry_requires_separate_start_authorization"
        ],
        "retry_identity_model": record["retry_identity_model"],
        "future_task_skills": record["future_task_skills"],
        "future_retry_capability_surface": record["future_retry_capability_surface"],
        "semantic_capabilities": record["semantic_capabilities"],
        "capability_resolution": record["capability_resolution"],
        "unresolved_Hermes_task_skills": record["unresolved_Hermes_task_skills"],
        "observed_task_skills": record["observed_task_skills"],
        "observed_attempt_count": record["observed_attempt_count"],
        "max_attempts": record["max_attempts"],
        "next_attempt_number": record["next_attempt_number"],
        "retry_budget_exhausted": record["retry_budget_exhausted"],
        "latest_failed_run_id": record["latest_failed_run_id"],
        "failure_category": record.get("failure_category"),
        "failure_summary": record.get("failure_summary"),
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_status": task.status if task is not None else record.get("kanban_task_status_at_recovery"),
        "kanban_run_count": len(runs),
        "second_run_started": len(runs) >= int(record["next_attempt_number"]),
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "task": task_visibility,
        "runs": [_run_dict(run) for run in runs],
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "retry_execution_count": 0,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": record["human_smoke_marker"],
        "next_action": {
            "id": action_ids["retry_start"],
            "target_ticket_id": record["ticket_id"],
            "required_human_action": "retry_start_authorization",
        },
    }


def _retry_start_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool,
) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(record["kanban_board_slug"]))
    task_id = str(record["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        runs = kanban_db.list_runs(conn, task_id) if task is not None else []
    finally:
        conn.close()
    task_visibility = None
    terminal_state = (
        _p18_9_0_terminal_execution_state(task, runs, ticket_id=str(record["ticket_id"]))
        if bool(record.get("execution_started"))
        else None
    )
    if task is not None:
        task_visibility = {
            "id": task.id,
            "status": task.status,
            "assignee": task.assignee,
            "workspace_kind": task.workspace_kind,
            "workspace_path": task.workspace_path,
            "current_run_id": task.current_run_id,
            "skills": list(task.skills or []),
        }
    action_ids = governed_ticket_lifecycle_action_ids(str(record["ticket_id"]))
    start_status = record["start_status"]
    blocker_code = record.get("blocker_code")
    blocker_detail = record.get("blocker_detail")
    execution_started = bool(record.get("execution_started"))
    worker_execution = bool(record.get("worker_execution"))
    worker_process_started = bool(record.get("worker_process_started"))
    worker_pid_recorded = bool(record.get("worker_pid_recorded"))
    retry_execution_started = bool(record.get("retry_execution_started"))
    next_action_id = (
        action_ids["monitor_execution"]
        if record.get("execution_started")
        else action_ids["retry_start"]
    )
    if terminal_state is not None:
        start_status = terminal_state["start_status"]
        blocker_code = terminal_state["blocker_code"]
        blocker_detail = terminal_state["blocker_detail"]
        execution_started = False
        worker_execution = False
        worker_process_started = False
        worker_pid_recorded = False
        retry_execution_started = False
        next_action_id = terminal_state["next_action_id"]
    historical_action_result = {
        "start_status": start_status,
        "blocker_code": blocker_code,
        "blocker_detail": blocker_detail,
        "dispatch_performed": bool(record.get("dispatch_performed")),
        "Kanban_dispatch": bool(record.get("Kanban_dispatch")),
        "execution_started": bool(record.get("execution_started")),
        "worker_process_started": bool(record.get("worker_process_started")),
        "kanban_run_id": record.get("kanban_run_id"),
        "recovery_cycle_id": record.get("recovery_cycle_id"),
    }
    current_invocation_side_effects = {
        "dispatch_performed": False if idempotent_replay else bool(record.get("dispatch_performed")),
        "Kanban_dispatch": False if idempotent_replay else bool(record.get("Kanban_dispatch")),
        "execution_started": False if idempotent_replay else execution_started,
        "worker_process_started": False if idempotent_replay else worker_process_started,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    return {
        "source_system": PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_RETRY_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_RETRY_START_ACTION_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "start_status": start_status,
        "retry_start_status": start_status,
        "blocker_code": blocker_code,
        "blocker_detail": blocker_detail,
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "retry_start_authorization_SHA256": record["retry_start_authorization_SHA256"],
        "recovery_action_SHA256": record["recovery_action_SHA256"],
        "recovery_cycle_id": record.get("recovery_cycle_id"),
        "retry_start_authorization_recorded": True,
        "historical_action_result": historical_action_result if idempotent_replay else None,
        "current_invocation_side_effects": current_invocation_side_effects,
        "ticket_execution_authorized": record["ticket_execution_authorized"],
        "WorkPacket_execution_authorized": record["WorkPacket_execution_authorized"],
        "runtime_execution_authorized": record["runtime_execution_authorized"],
        "retry_identity_model": record["retry_identity_model"],
        "previous_attempt_count": record["previous_attempt_count"],
        "next_attempt_number": record["next_attempt_number"],
        "max_attempts": record["max_attempts"],
        "latest_failed_run_id": record["latest_failed_run_id"],
        "failure_category": record.get("failure_category"),
        "failure_summary": record.get("failure_summary"),
        "future_task_skills": record["future_task_skills"],
        "future_retry_capability_surface": record["future_retry_capability_surface"],
        "unresolved_Hermes_task_skills": record["unresolved_Hermes_task_skills"],
        "observed_task_skills": record["observed_task_skills"],
        "provider": record["provider"],
        "model": record["model"],
        "api_mode": record["api_mode"],
        "credential_profile_id": record["credential_profile_id"],
        "credential_policy_revision": record.get("credential_policy_revision"),
        "provider_runtime_profile_id": record["provider_runtime_profile_id"],
        "worker_profile_id": record["worker_profile_id"],
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_status": task.status if task is not None else record.get("kanban_task_status"),
        "kanban_run_id": task.current_run_id if task is not None else record.get("kanban_run_id"),
        "kanban_run_count": len(runs),
        "second_run_started": len(runs) >= int(record["next_attempt_number"]),
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "workspace_kind": record["workspace_kind"],
        "workspace_path": (task.workspace_path if task is not None else record.get("workspace_path")),
        "workspace_created": bool(record.get("workspace_created")),
        "task_prepare_status": record["task_prepare_status"],
        "task_unblocked": bool(record.get("task_unblocked")),
        "task_skills_corrected": bool(record.get("task_skills_corrected")),
        "dispatch_performed": current_invocation_side_effects["dispatch_performed"],
        "execution_started": current_invocation_side_effects["execution_started"],
        "worker_execution": False if idempotent_replay else worker_execution,
        "worker_process_started": current_invocation_side_effects["worker_process_started"],
        "worker_pid_recorded": False if idempotent_replay else worker_pid_recorded,
        "Kanban_dispatch": current_invocation_side_effects["Kanban_dispatch"],
        "retry_execution_started": False if idempotent_replay else retry_execution_started,
        "retry_execution_count": int(record.get("retry_execution_count") or 0),
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "task": task_visibility,
        "runs": [_run_dict(run) for run in runs],
        "human_smoke_marker": record["human_smoke_marker"],
        "next_action": {
            "id": next_action_id,
            "target_ticket_id": record["ticket_id"],
        },
    }


def _execution_start_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool,
) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(record["kanban_board_slug"]))
    task_id = str(record["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        runs = kanban_db.list_runs(conn, task_id) if task is not None else []
    finally:
        conn.close()
    task_visibility = None
    terminal_state = (
        _p18_9_0_terminal_execution_state(task, runs, ticket_id=str(record["ticket_id"]))
        if bool(record.get("execution_started"))
        else None
    )
    if task is not None:
        task_visibility = {
            "id": task.id,
            "status": task.status,
            "assignee": task.assignee,
            "workspace_kind": task.workspace_kind,
            "workspace_path": task.workspace_path,
            "current_run_id": task.current_run_id,
        }
    action_ids = governed_ticket_lifecycle_action_ids(str(record["ticket_id"]))
    start_status = record["start_status"]
    blocker_code = record.get("blocker_code")
    blocker_detail = record.get("blocker_detail")
    execution_started = bool(record.get("execution_started"))
    worker_execution = bool(record.get("worker_execution"))
    worker_process_started = bool(record.get("worker_process_started"))
    worker_pid_recorded = bool(record.get("worker_pid_recorded"))
    next_action_id = (
        action_ids["monitor_execution"]
        if record.get("execution_started")
        else action_ids["execution_start"]
    )
    if terminal_state is not None:
        start_status = terminal_state["start_status"]
        blocker_code = terminal_state["blocker_code"]
        blocker_detail = terminal_state["blocker_detail"]
        execution_started = False
        worker_execution = False
        worker_process_started = False
        worker_pid_recorded = False
        next_action_id = terminal_state["next_action_id"]
    return {
        "source_system": PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_WORKER_START_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_WORKER_START_ACTION_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "start_status": start_status,
        "blocker_code": blocker_code,
        "blocker_detail": blocker_detail,
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "start_authorization_SHA256": record["start_authorization_SHA256"],
        "execution_authorization_recorded": True,
        "ticket_execution_authorized": record["ticket_execution_authorized"],
        "WorkPacket_execution_authorized": record["WorkPacket_execution_authorized"],
        "runtime_execution_authorized": record["runtime_execution_authorized"],
        "provider": record["provider"],
        "model": record["model"],
        "api_mode": record["api_mode"],
        "credential_profile_id": record["credential_profile_id"],
        "credential_policy_revision": record.get("credential_policy_revision"),
        "provider_runtime_profile_id": record["provider_runtime_profile_id"],
        "worker_profile_id": record["worker_profile_id"],
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_status": task.status if task is not None else record.get("kanban_task_status"),
        "kanban_run_id": task.current_run_id if task is not None else record.get("kanban_run_id"),
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "workspace_kind": record["workspace_kind"],
        "workspace_path": (task.workspace_path if task is not None else record.get("workspace_path")),
        "workspace_created": bool(record.get("workspace_created")),
        "dispatch_performed": bool(record.get("dispatch_performed")),
        "execution_started": execution_started,
        "worker_execution": worker_execution,
        "worker_process_started": worker_process_started,
        "worker_pid_recorded": worker_pid_recorded,
        "Kanban_dispatch": bool(record.get("Kanban_dispatch")),
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "task": task_visibility,
        "runs": [_run_dict(run) for run in runs],
        "next_action": {
            "id": next_action_id,
            "target_ticket_id": record["ticket_id"],
        },
    }


def _p18_9_0_terminal_execution_state(
    task: Any,
    runs: list[Any],
    *,
    ticket_id: str = PEPPER_BOOTSTRAP_NEXT_TICKET_ID,
) -> dict[str, Any] | None:
    action_ids = governed_ticket_lifecycle_action_ids(ticket_id)
    if task is None:
        return {
            "start_status": "failed",
            "blocker_code": "KANBAN_TASK_GAP",
            "blocker_detail": "projected Kanban task is missing after execution start",
            "next_action_id": action_ids["execution_recovery"],
            "outcome": "task_missing",
            "failure_category": "task_missing",
            "failure_summary": "projected Kanban task is missing after execution start",
        }
    task_status = str(getattr(task, "status", "") or "").strip().lower()
    latest_run = runs[-1] if runs else None
    run_status = str(getattr(latest_run, "status", "") or "").strip().lower()
    outcome = str(getattr(latest_run, "outcome", "") or "").strip().lower()
    if task_status == "running" and getattr(task, "current_run_id", None):
        return None
    if task_status == "done" or outcome == "completed":
        return {
            "start_status": "completed",
            "blocker_code": None,
            "blocker_detail": None,
            "next_action_id": action_ids["review_prepare"],
            "outcome": "completed",
        }
    failure_outcome = outcome or run_status
    if task_status == "blocked" or failure_outcome in _GOVERNED_TICKET_FAILURE_OUTCOMES:
        detail = (
            getattr(latest_run, "error", None)
            or getattr(task, "last_failure_error", None)
            or f"Kanban task status is {task_status or 'unknown'}"
        )
        failure_fields = (
            _run_failure_fields(latest_run)
            if latest_run is not None
            else {"failure_category": failure_outcome or task_status, "failure_summary": detail}
        )
        return {
            "start_status": "failed",
            "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
            "blocker_detail": _safe_text(detail, limit=300),
            "next_action_id": action_ids["execution_recovery"],
            "outcome": failure_outcome or task_status,
            "failure_category": (
                failure_fields.get("failure_category")
                or failure_outcome
                or task_status
                or "failed"
            ),
            "failure_summary": (
                failure_fields.get("failure_summary")
                or _safe_text(detail, limit=300)
            ),
        }
    if latest_run is not None and getattr(latest_run, "ended_at", None) is not None:
        failure_fields = _run_failure_fields(latest_run)
        return {
            "start_status": "failed",
            "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
            "blocker_detail": f"Kanban run ended with status {run_status or 'unknown'}",
            "next_action_id": action_ids["execution_recovery"],
            "outcome": failure_outcome or "ended_without_outcome",
            "failure_category": (
                failure_fields.get("failure_category")
                or failure_outcome
                or run_status
                or "ended_without_outcome"
            ),
            "failure_summary": (
                failure_fields.get("failure_summary")
                or f"Kanban run ended with status {run_status or 'unknown'}"
            ),
        }
    return None


def _execution_start_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "start_authorization_SHA256"
    }
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(
        f"{PEPPER_WORKER_START_AUTHORIZATION_DIGEST_ALGORITHM}\n{data}".encode("utf-8")
    ).hexdigest()


def _execution_start_authority_mismatch_diagnostics(
    record: dict[str, Any],
    projection: dict[str, Any],
    *,
    mismatched_field: str,
) -> dict[str, Any]:
    return {
        "mismatched_field": mismatched_field,
        "current_ticket_id": projection.get("ticket_id"),
        "authorization_ticket_id": record.get("ticket_id"),
        "expected_ticket_spec_SHA256": projection.get("ticket_spec_SHA256"),
        "authorization_ticket_spec_SHA256": record.get("ticket_spec_SHA256"),
        "expected_work_packet_id": projection.get("work_packet_id"),
        "authorization_work_packet_id": record.get("work_packet_id"),
        "expected_work_packet_SHA256": projection.get("work_packet_SHA256"),
        "authorization_work_packet_SHA256": record.get("work_packet_SHA256"),
        "expected_projection_SHA256": projection.get("projection_SHA256"),
        "authorization_projection_SHA256": record.get("projection_SHA256"),
        "expected_kanban_task_id": projection.get("kanban_task_id"),
        "authorization_kanban_task_id": record.get("kanban_task_id"),
        "expected_executor_profile": projection.get("assignee_profile"),
        "authorization_executor_profile": record.get("assignee_profile"),
    }


def _persist_execution_start_record(record: dict[str, Any]) -> None:
    validate_p18_9_0_execution_start_record(record)
    path = execution_start_record_path_for_ticket(str(record["ticket_id"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _recovery_action_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "recovery_action_SHA256"
    }
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(
        f"{PEPPER_RECOVERY_ACTION_DIGEST_ALGORITHM}\n{data}".encode("utf-8")
    ).hexdigest()


def _persist_recovery_action_record(record: dict[str, Any]) -> None:
    validate_p18_9_0_recovery_action_record(record)
    path = p18_9_0_recovery_action_record_path()
    _archive_existing_authority_record(
        path,
        p18_9_0_recovery_action_history_path(),
        reason="replaced_by_current_recovery_cycle",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _retry_start_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "retry_start_authorization_SHA256"
    }
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(
        f"{PEPPER_RETRY_START_ACTION_DIGEST_ALGORITHM}\n{data}".encode("utf-8")
    ).hexdigest()


def _persist_retry_start_record(record: dict[str, Any]) -> None:
    validate_p18_9_0_retry_start_record(record)
    path = p18_9_0_retry_start_record_path()
    _archive_existing_authority_record(
        path,
        p18_9_0_retry_start_history_path(),
        reason="replaced_by_current_recovery_cycle",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _digest_payload(algorithm: str, payload: dict[str, Any]) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(f"{algorithm}\n{data}".encode("utf-8")).hexdigest()


def _review_prepare_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "review_prepare_action_SHA256"
    }
    return _digest_payload(PEPPER_REVIEW_PREPARE_ACTION_DIGEST_ALGORITHM, payload)


def _review_acceptance_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "review_acceptance_action_SHA256"
    }
    return _digest_payload(PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_DIGEST_ALGORITHM, payload)


def _review_acceptance_text_digest(value: str) -> str:
    payload = {"human_acceptance_text": unicodedata.normalize("NFC", str(value))}
    return _digest_payload(PEPPER_REVIEW_HUMAN_ACCEPTANCE_TEXT_DIGEST_ALGORITHM, payload)


def _kanban_completion_result_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "kanban_completion_result_SHA256"
    }
    return _digest_payload(PEPPER_KANBAN_COMPLETION_RESULT_DIGEST_ALGORITHM, payload)


def _criteria_revision_digest(contract: dict[str, Any]) -> str:
    payload = {
        "ticket_spec_SHA256": contract["ticket_spec_SHA256"],
        "work_packet_SHA256": contract["work_packet_SHA256"],
        "acceptance_criteria": contract["acceptance_criteria"],
        "validation_steps": contract["validation_steps"],
        "response_contract": contract["response_contract"],
    }
    return _digest_payload(
        f"{PEPPER_ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM}:criteria-revision-v1",
        payload,
    )


def _acceptance_contract_digest(contract: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in contract.items()
        if key != "acceptance_contract_SHA256"
    }
    return _digest_payload(PEPPER_ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM, payload)


def _review_prepare_package_digest(
    *,
    projection: dict[str, Any],
    completion: dict[str, Any],
    acceptance_contract: dict[str, Any],
) -> str:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    payload = {
        "project_id": binding.project_id,
        "ticket_id": binding.ticket_id,
        "ticket_spec_SHA256": projection["ticket_spec_SHA256"],
        "work_packet_id": projection["work_packet_id"],
        "work_packet_SHA256": projection["work_packet_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "successful_run_id": completion["run_id"],
        "kanban_completion_result_SHA256": completion[
            "kanban_completion_result_SHA256"
        ],
        "criteria_revision_SHA256": acceptance_contract["criteria_revision_SHA256"],
        "acceptance_contract_SHA256": acceptance_contract[
            "acceptance_contract_SHA256"
        ],
    }
    return _digest_payload(PEPPER_REVIEW_PREPARE_PACKAGE_DIGEST_ALGORITHM, payload)


def _review_prepare_acceptance_contract_for_validation(
    record: dict[str, Any],
    *,
    projection: dict[str, Any],
    completion: dict[str, Any],
) -> dict[str, Any]:
    current_contract = _p18_9_0_acceptance_contract()
    current_package_sha = _review_prepare_package_digest(
        projection=projection,
        completion=completion,
        acceptance_contract=current_contract,
    )
    if _review_prepare_contract_fields_match(
        record,
        contract=current_contract,
        review_package_sha=current_package_sha,
    ):
        return current_contract

    historical_contract = record.get("acceptance_contract")
    historical_package_sha = None
    if isinstance(historical_contract, dict):
        try:
            historical_package_sha = _review_prepare_package_digest(
                projection=projection,
                completion=completion,
                acceptance_contract=historical_contract,
            )
        except (KeyError, TypeError, ValueError):
            historical_package_sha = None
        if (
            historical_package_sha is not None
            and _review_prepare_contract_fields_match(
                record,
                contract=historical_contract,
                review_package_sha=historical_package_sha,
            )
            and _terminal_review_acceptance_preserves_prepare_record(record)
        ):
            return historical_contract

    diagnostics = _review_prepare_hash_mismatch_diagnostics(
        record,
        current_contract=current_contract,
        current_package_sha=current_package_sha,
        historical_contract=historical_contract,
        historical_package_sha=historical_package_sha,
    )
    raise ProductRuntimeConflict(
        "review-preparation record acceptance_contract_SHA256 mismatch; "
        f"persisted={diagnostics['persisted_acceptance_contract_SHA256']} "
        f"expected_historical={diagnostics['expected_historical_acceptance_contract_SHA256']} "
        f"current={diagnostics['current_acceptance_contract_SHA256']} "
        f"historical_revision={diagnostics['historical_contract_revision']}"
    )


def _review_prepare_contract_fields_match(
    record: dict[str, Any],
    *,
    contract: dict[str, Any],
    review_package_sha: str,
) -> bool:
    try:
        if contract.get("criteria_revision_SHA256") != _criteria_revision_digest(contract):
            return False
        if contract.get("acceptance_contract_SHA256") != _acceptance_contract_digest(contract):
            return False
    except (KeyError, TypeError, ValueError):
        return False
    if record.get("criteria_revision_SHA256") != contract.get("criteria_revision_SHA256"):
        return False
    if record.get("acceptance_contract_SHA256") != contract.get("acceptance_contract_SHA256"):
        return False
    if record.get("review_package_SHA256") != review_package_sha:
        return False
    if record.get("acceptance_contract") != contract:
        return False
    return True


def _terminal_review_acceptance_preserves_prepare_record(
    review_prepare: dict[str, Any],
) -> bool:
    path = p18_9_0_review_acceptance_record_path()
    if not path.exists():
        return False
    try:
        acceptance = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(acceptance, dict):
        return False
    if acceptance.get("review_acceptance_action_SHA256") != _review_acceptance_record_digest(acceptance):
        return False
    expected = {
        "ticket_id": review_prepare.get("ticket_id"),
        "ticket_spec_SHA256": review_prepare.get("ticket_spec_SHA256"),
        "work_packet_id": review_prepare.get("work_packet_id"),
        "work_packet_SHA256": review_prepare.get("work_packet_SHA256"),
        "projection_SHA256": review_prepare.get("projection_SHA256"),
        "kanban_task_id": review_prepare.get("kanban_task_id"),
        "review_prepare_action_SHA256": review_prepare.get("review_prepare_action_SHA256"),
        "review_package_SHA256": review_prepare.get("review_package_SHA256"),
        "acceptance_contract_SHA256": review_prepare.get("acceptance_contract_SHA256"),
        "criteria_revision_SHA256": review_prepare.get("criteria_revision_SHA256"),
        "kanban_completion_result_SHA256": review_prepare.get("kanban_completion_result_SHA256"),
        "successful_run_id": review_prepare.get("successful_run_id"),
    }
    for key, value in expected.items():
        if acceptance.get(key) != value:
            return False
    return (
        acceptance.get("review_acceptance_status") == "accepted"
        and acceptance.get("review_validation_state") == "completed"
        and acceptance.get("validation_state") == "review_accepted"
        and acceptance.get("review_state") == "accepted"
        and acceptance.get("workflow_status") == "completed"
        and acceptance.get("ticket_closed") is True
        and acceptance.get("P18_9_0_closed") is True
        and acceptance.get("P18_9_0_completed") is True
        and acceptance.get("review_prepare_authority")
        == _review_prepare_authority_projection(review_prepare)
    )


def _review_prepare_hash_mismatch_diagnostics(
    record: dict[str, Any],
    *,
    current_contract: dict[str, Any],
    current_package_sha: str,
    historical_contract: Any,
    historical_package_sha: str | None,
) -> dict[str, Any]:
    historical_contract_dict = historical_contract if isinstance(historical_contract, dict) else {}
    expected_historical_sha = None
    expected_historical_criteria_sha = None
    if historical_contract_dict:
        try:
            expected_historical_sha = _acceptance_contract_digest(historical_contract_dict)
            expected_historical_criteria_sha = _criteria_revision_digest(historical_contract_dict)
        except (KeyError, TypeError, ValueError):
            expected_historical_sha = None
            expected_historical_criteria_sha = None
    return {
        "persisted_acceptance_contract_SHA256": record.get("acceptance_contract_SHA256"),
        "persisted_criteria_revision_SHA256": record.get("criteria_revision_SHA256"),
        "persisted_review_package_SHA256": record.get("review_package_SHA256"),
        "expected_historical_acceptance_contract_SHA256": expected_historical_sha,
        "expected_historical_criteria_revision_SHA256": expected_historical_criteria_sha,
        "expected_historical_review_package_SHA256": historical_package_sha,
        "current_acceptance_contract_SHA256": current_contract.get("acceptance_contract_SHA256"),
        "current_criteria_revision_SHA256": current_contract.get("criteria_revision_SHA256"),
        "current_review_package_SHA256": current_package_sha,
        "historical_contract_revision": historical_contract_dict.get("schema_version"),
        "historical_contract_source": historical_contract_dict.get("acceptance_contract_source"),
        "current_contract_source": current_contract.get("acceptance_contract_source"),
    }


def _validate_review_acceptance_request_guards(
    request: CurrentTicketReviewAcceptanceRequest,
) -> None:
    binding = resolve_current_ticket_lifecycle_binding()
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(f"review acceptance is bounded to project {binding.project_id}")
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(f"review acceptance is bounded to ticket {binding.ticket_id}")
    if request.next_action_id not in {None, binding.review_acceptance_next_action_id}:
        raise ProductRuntimeConflict(
            f"review acceptance requires {binding.review_acceptance_next_action_id}"
        )
    if request.human_acceptance_text != PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT:
        raise ProductRuntimeConflict(
            "exact explicit P18.9.0 review acceptance text is required"
        )


def _review_acceptance_workflow_blocker(
    workflow: dict[str, Any],
) -> tuple[str, str] | None:
    binding = resolve_current_ticket_lifecycle_binding()
    if workflow.get("project_id") != binding.project_id:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", f"current project is not {binding.project_id}"
    if workflow.get("macroproject_id") != binding.macroproject_id:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", f"current macroproject is not {binding.macroproject_id}"
    if workflow.get("current_ticket_id") != binding.ticket_id:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", f"current ticket is not {binding.ticket_id}"
    if workflow.get("workflow_status") != "review_prepared_pending_human_acceptance":
        return (
            "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP",
            "workflow status is not review_prepared_pending_human_acceptance",
        )
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "next action is unavailable"
    if next_action.get("id") != binding.review_acceptance_next_action_id:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "next action is not review acceptance"
    if next_action.get("target_ticket_id") != binding.ticket_id:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", f"next action does not target {binding.ticket_id}"
    if int(workflow.get("active_execution_count") or 0) != 0:
        return "EXECUTION_ALREADY_ACTIVE", "an execution is already active"
    if workflow.get("execution_state") == "active_executions":
        return "EXECUTION_ALREADY_ACTIVE", "execution state is active"
    if workflow.get("recovery_state") != "not_required":
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "recovery state is not not_required"
    if workflow.get("validation_state") != "review_prepared_pending_human_acceptance":
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "validation state is not pending acceptance"
    if workflow.get("review_state") != "prepared_pending_human_acceptance":
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "review state is not pending acceptance"
    if workflow.get("git_handoff_state") != "not_required_for_ticket_result":
        return "GIT_HANDOFF_STATE_GAP", "git handoff state is not not_required_for_ticket_result"
    if workflow.get("remaining_blockers"):
        return "WORKFLOW_BLOCKER_PRESENT", "workflow blockers are present"
    if workflow.get("human_acceptance_required") is not True:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "human acceptance is not required"
    if workflow.get("human_acceptance_recorded") is not False:
        return "PEPPER_REVIEW_ACCEPTANCE_ACTION_GAP", "human acceptance is already recorded"
    return None


def _review_prepare_authority_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy_id": record["policy_id"],
        "P18_5_policy_id": record["P18_5_policy_id"],
        "runtime_boundary_classification": record["runtime_boundary_classification"],
        "review_prepare_action_SHA256": record["review_prepare_action_SHA256"],
        "review_package_SHA256": record["review_package_SHA256"],
        "acceptance_contract_SHA256": record["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": record["criteria_revision_SHA256"],
        "kanban_completion_result_SHA256": record["kanban_completion_result_SHA256"],
        "successful_run_id": record["successful_run_id"],
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
    }


def _p18_9_next_ticket_authority() -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        resolve_canonical_next_ticket,
    )

    authority = resolve_canonical_next_ticket({
        "project_id": PEPPER_GOVERNED_PROJECT_ID,
        "project_name": PEPPER_GOVERNED_PROJECT_NAME,
        "macroproject_id": PEPPER_GOVERNED_MACROPROJECT_ID,
        "macroproject_title": PEPPER_GOVERNED_MACROPROJECT_TITLE,
        "closed_predecessor_ticket_id": PEPPER_BOOTSTRAP_NEXT_TICKET_ID,
    })
    return {
        "ticket_id": authority.ticket_id,
        "ticket_title": _safe_text(authority.ticket_title, limit=200),
        "authority_path": authority.roadmap_authority_path,
        "authority_section": authority.roadmap_authority_section,
        "authority_type": "current_repository_roadmap_authority",
        "auto_generated": False,
        "execution_authorized": False,
        "next_action_id": authority.next_action_id,
        "dependency_ticket_ids": list(authority.dependency_ticket_ids),
    }


def resolve_canonical_next_ticket(workflow: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resolve Pepper's canonical next governed ticket for runtime surfaces."""

    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        resolve_canonical_next_ticket as bridge_resolve_canonical_next_ticket,
    )

    source = workflow if workflow is not None else build_workflow_control_snapshot()
    return bridge_resolve_canonical_next_ticket(source).asdict()


def _current_next_ticket_generation_target(workflow: dict[str, Any]) -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        resolve_generation_target_from_workflow,
    )

    target = resolve_generation_target_from_workflow(workflow)
    return {
        "project_id": target.project_id,
        "macroproject_id": target.macroproject_id,
        "macroproject_title": target.macroproject_title,
        "ticket_id": target.ticket_id,
        "ticket_title": target.ticket_title,
        "next_action_id": target.next_action_id,
        "roadmap_authority_path": target.roadmap_authority_path,
        "roadmap_authority_section": target.roadmap_authority_section,
        "canonical_roadmap_authority": target.canonical_roadmap_authority,
        "dependency_ticket_ids": list(target.dependency_ticket_ids),
    }


def _validate_review_prepare_request_guards(
    request: CurrentTicketReviewPrepareRequest,
) -> None:
    binding = resolve_current_ticket_lifecycle_binding()
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(f"review preparation is bounded to project {binding.project_id}")
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(f"review preparation is bounded to ticket {binding.ticket_id}")
    if request.next_action_id not in {None, binding.review_prepare_next_action_id}:
        raise ProductRuntimeConflict(
            f"review preparation requires {binding.review_prepare_next_action_id}"
        )


def _review_prepare_workflow_blocker(
    workflow: dict[str, Any],
) -> tuple[str, str] | None:
    binding = resolve_current_ticket_lifecycle_binding()
    if workflow.get("project_id") != binding.project_id:
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", f"current project is not {binding.project_id}"
    if workflow.get("macroproject_id") != binding.macroproject_id:
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", f"current macroproject is not {binding.macroproject_id}"
    if workflow.get("current_ticket_id") != binding.ticket_id:
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", f"current ticket is not {binding.ticket_id}"
    if workflow.get("workflow_status") != "execution_completed":
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", "workflow status is not execution_completed"
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", "next action is unavailable"
    if next_action.get("id") != binding.review_prepare_next_action_id:
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", "next action is not review preparation"
    if next_action.get("target_ticket_id") != binding.ticket_id:
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", f"next action does not target {binding.ticket_id}"
    if int(workflow.get("active_execution_count") or 0) != 0:
        return "EXECUTION_ALREADY_ACTIVE", "an execution is already active"
    if workflow.get("execution_state") == "active_executions":
        return "EXECUTION_ALREADY_ACTIVE", "execution state is active"
    if workflow.get("recovery_state") != "not_required":
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", "recovery state is not not_required"
    if workflow.get("validation_state") != "execution_completed_pending_validation":
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", "validation state is not pending validation"
    if workflow.get("review_state") != "ready_for_review_validation":
        return "PEPPER_REVIEW_PREPARE_ACTION_GAP", "review state is not ready for validation"
    if workflow.get("remaining_blockers"):
        return "WORKFLOW_BLOCKER_PRESENT", "workflow blockers are present"
    return None


def _p18_9_0_acceptance_contract() -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        load_p18_9_0_generation_record,
    )

    generation = load_p18_9_0_generation_record()
    if generation is None:
        raise ProductRuntimeNotFound("P18.9.0 generated TicketSpec authority not found")
    ticket_spec = generation.get("ticket_spec")
    compilation = generation.get("work_packet_compilation_result")
    if not isinstance(ticket_spec, dict) or not isinstance(compilation, dict):
        raise ProductRuntimeConflict("P18.9.0 acceptance contract source is unavailable")
    work_packet = compilation.get("work_packet")
    if not isinstance(work_packet, dict):
        raise ProductRuntimeConflict("P18.9.0 WorkPacket contract source is unavailable")
    binding = resolve_current_ticket_lifecycle_binding(generation_record=generation)
    contract = {
        "schema_version": PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
        "project_id": binding.project_id,
        "ticket_id": binding.ticket_id,
        "ticket_title": binding.ticket_title,
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "acceptance_criteria": list(ticket_spec.get("acceptance_criteria") or []),
        "validation_steps": list(ticket_spec.get("validation_steps") or []),
        "response_contract": dict(ticket_spec.get("response_contract") or {}),
        "work_packet_validation_steps": list(work_packet.get("validation_steps") or []),
        "completion_verdict": dict(ticket_spec.get("response_contract") or {}).get(
            "completion_verdict"
        ),
        "required_response_sections": list(
            dict(ticket_spec.get("response_contract") or {}).get("required_sections") or []
        ),
        "acceptance_contract_source": f"pepper-ticket-architect-bridge:{binding.ticket_id}",
    }
    contract["criteria_revision_SHA256"] = _criteria_revision_digest(contract)
    contract["acceptance_contract_SHA256"] = _acceptance_contract_digest(contract)
    return contract


def _metadata_list(metadata: Any, *keys: str) -> list[str]:
    if not isinstance(metadata, dict):
        return []
    for key in keys:
        value = metadata.get(key)
        if isinstance(value, (list, tuple)):
            return [_safe_text(item, limit=300) for item in value if str(item or "").strip()]
    return []


def _metadata_bool(metadata: Any, *keys: str) -> bool | None:
    if not isinstance(metadata, dict):
        return None
    for key in keys:
        if key in metadata:
            return bool(metadata.get(key))
    return None


def _kanban_completion_result_source(projection: dict[str, Any]) -> dict[str, Any]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            return {
                "blocker_code": "KANBAN_TASK_GAP",
                "blocker_detail": "projected Kanban task is missing",
            }
        try:
            task_body = json.loads(task.body or "{}")
        except json.JSONDecodeError:
            task_body = {}
        if not isinstance(task_body, dict):
            task_body = {}
        if task_body.get("WorkPacket_ID") != projection["work_packet_id"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": "projected Kanban task WorkPacket ID does not match P18.9.0 authority",
            }
        if task_body.get("WorkPacket_SHA256") != projection["work_packet_SHA256"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": "projected Kanban task WorkPacket SHA256 does not match P18.9.0 authority",
            }
        runs = kanban_db.list_runs(conn, task_id)
        active_runs = [run for run in runs if _execution_is_active(_run_dict(run))]
        if active_runs or task.current_run_id is not None:
            return {
                "blocker_code": "EXECUTION_ALREADY_ACTIVE",
                "blocker_detail": "projected Kanban task still has active execution state",
            }
        if not runs:
            return {
                "blocker_code": "KANBAN_RUN_GAP",
                "blocker_detail": "projected Kanban task has no run evidence",
            }
        latest_run = runs[-1]
        run_status = str(getattr(latest_run, "status", "") or "").strip().lower()
        run_outcome = str(getattr(latest_run, "outcome", "") or "").strip().lower()
        if task.status != "done" or run_status != "done" or run_outcome != "completed":
            return {
                "blocker_code": "KANBAN_COMPLETION_RESULT_GAP",
                "blocker_detail": "latest projected Kanban run is not completed",
                "kanban_task_status": task.status,
                "latest_run_status": run_status,
                "latest_run_outcome": run_outcome,
            }
        if getattr(latest_run, "ended_at", None) is None:
            return {
                "blocker_code": "KANBAN_COMPLETION_RESULT_GAP",
                "blocker_detail": "latest projected Kanban run has not ended",
            }
        summary = getattr(latest_run, "summary", None)
        metadata = getattr(latest_run, "metadata", None)
        task_result = getattr(task, "result", None)
        if not (str(summary or "").strip() or str(task_result or "").strip() or metadata):
            return {
                "blocker_code": "KANBAN_COMPLETION_RESULT_DETAIL_GAP",
                "blocker_detail": "completed P18.9.0 run lacks structural result, summary, or metadata detail",
                "run_id": int(latest_run.id),
            }
        modified_files = _metadata_list(
            metadata,
            "files_modified",
            "modified_files",
            "changed_files",
        )
        git_mutation = _metadata_bool(metadata, "Git_mutation", "git_mutation")
        if modified_files or git_mutation is True:
            return {
                "blocker_code": "GIT_HANDOFF_STATE_GAP",
                "blocker_detail": "completed P18.9.0 result reports file or Git mutation",
                "files_modified": modified_files,
                "git_mutation": git_mutation,
            }
        detail_sources = []
        if str(summary or "").strip():
            detail_sources.append("task_runs.summary")
        if str(task_result or "").strip():
            detail_sources.append("tasks.result")
        if isinstance(metadata, dict) and metadata:
            detail_sources.append("task_runs.metadata")
        source = {
            "blocker_code": None,
            "blocker_detail": None,
            "kanban_board_slug": board,
            "kanban_task_id": task.id,
            "kanban_task_status": task.status,
            "kanban_task_assignee": task.assignee,
            "kanban_task_workspace_kind": task.workspace_kind,
            "kanban_task_workspace_path": task.workspace_path,
            "kanban_task_current_run_id": task.current_run_id,
            "run_id": int(latest_run.id),
            "run_status": run_status,
            "run_outcome": run_outcome,
            "run_profile": latest_run.profile,
            "run_started_at": latest_run.started_at,
            "run_ended_at": latest_run.ended_at,
            "run_summary": summary,
            "run_metadata": metadata if isinstance(metadata, dict) else None,
            "task_result": task_result,
            "completion_detail_sources": detail_sources,
            "reported_files_modified": modified_files,
            "reported_git_mutation": bool(git_mutation) if git_mutation is not None else False,
            "task_run_count": len(runs),
            "Kanban_SQLite_canonical_authority": False,
            "logs_parsed_for_completion_authority": False,
        }
        source["kanban_completion_result_SHA256"] = _kanban_completion_result_digest(source)
        return source
    finally:
        conn.close()


def _build_review_prepare_record(
    *,
    request: CurrentTicketReviewPrepareRequest,
    projection: dict[str, Any],
    workflow: dict[str, Any],
    completion: dict[str, Any],
    acceptance_contract: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.review_validation_loop import (
        REVIEW_VALIDATION_LOOP_POLICY_ID,
        REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION,
        ReviewValidationLoopDecision,
        ReviewValidationLoopState,
        ReviewValidationRuntimeBoundary,
    )

    package_sha = _review_prepare_package_digest(
        projection=projection,
        completion=completion,
        acceptance_contract=acceptance_contract,
    )
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    pre_review_invariants = {
        "project": binding.project_id,
        "ticket": binding.ticket_id,
        "next_action": binding.review_prepare_next_action_id,
        "run_id": completion["run_id"],
        "run_status": "done",
        "run_outcome": "completed",
        "active_execution_count": 0,
        "recovery_state": "not_required",
        "validation_state": "execution_completed_pending_validation",
        "review_state": "ready_for_review_validation",
        "blocker_count": 0,
    }
    record = {
        "schema_version": PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID,
        "source_system": PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM,
        "P18_5_policy_id": REVIEW_VALIDATION_LOOP_POLICY_ID,
        "runtime_boundary_classification": REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION,
        "runtime_boundary": ReviewValidationRuntimeBoundary.REVIEW_POST_EXECUTION_ONLY.value,
        "created_at": _utc_now_iso(),
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "execution_start_authority_SHA256": workflow.get("execution_start_authority", {}).get(
            "start_authorization_SHA256"
        ),
        "retry_start_authority_SHA256": workflow.get("retry_start_authority", {}).get(
            "retry_start_authorization_SHA256"
        ),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "successful_run_id": completion["run_id"],
        "successful_run_status": "done",
        "successful_run_outcome": "completed",
        "kanban_completion_result": completion,
        "kanban_completion_result_SHA256": completion["kanban_completion_result_SHA256"],
        "acceptance_contract": acceptance_contract,
        "acceptance_contract_SHA256": acceptance_contract["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": acceptance_contract["criteria_revision_SHA256"],
        "review_package_SHA256": package_sha,
        "pre_review_invariants": pre_review_invariants,
        "review_prepare_status": "prepared_pending_human_acceptance",
        "validation_state": "review_prepared_pending_human_acceptance",
        "review_state": "prepared_pending_human_acceptance",
        "review_validation_vocabulary": {
            "decisions": [item.value for item in ReviewValidationLoopDecision],
            "states": [item.value for item in ReviewValidationLoopState],
        },
        "P18_5_request_model_reused": False,
        "P18_5_review_vocabulary_reused": True,
        "P18_9_0_ticket_specific_contract_bound": True,
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
        "human_acceptance_next_action_id": binding.review_acceptance_next_action_id,
        "git_handoff_required": False,
        "git_handoff_state": "not_required_for_ticket_result",
        "git_handoff_decision_basis": "P18.9.0 completion source reports no file or Git mutation metadata",
        "requested_project_id": request.project_id,
        "requested_ticket_id": request.ticket_id,
        "requested_next_action_id": request.next_action_id,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "next_action": {
            "id": binding.review_acceptance_next_action_id,
            "target_ticket_id": binding.ticket_id,
            "target_ticket_title": binding.ticket_title,
            "required_human_action": "p18_9_0_review_acceptance",
        },
        "human_smoke_marker": "PEPPER-REVIEW-PREPARE-ACTION-READY-FOR-HUMAN-SMOKE",
    }
    record["review_prepare_action_SHA256"] = _review_prepare_record_digest(record)
    return record


def _build_review_acceptance_record(
    *,
    request: CurrentTicketReviewAcceptanceRequest,
    projection: dict[str, Any],
    workflow: dict[str, Any],
    review_prepare: dict[str, Any],
    next_ticket: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.governed_state_machine import (
        GovernedWorkflowState,
        WorkflowTransitionTrigger,
    )
    from hermes_cli.agent_platform.workflow.review_validation_loop import (
        REVIEW_VALIDATION_LOOP_POLICY_ID,
        REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION,
        ReviewValidationLoopDecision,
        ReviewValidationLoopState,
    )

    observed_at = _utc_now_iso()
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    acceptance_text = unicodedata.normalize("NFC", request.human_acceptance_text)
    acceptance_text_sha = _review_acceptance_text_digest(acceptance_text)
    pre_acceptance_invariants = {
        "project": binding.project_id,
        "ticket": binding.ticket_id,
        "next_action": binding.review_acceptance_next_action_id,
        "review_prepare_action_SHA256": review_prepare["review_prepare_action_SHA256"],
        "review_package_SHA256": review_prepare["review_package_SHA256"],
        "active_execution_count": int(workflow.get("active_execution_count") or 0),
        "recovery_state": workflow.get("recovery_state"),
        "validation_state": workflow.get("validation_state"),
        "review_state": workflow.get("review_state"),
        "git_handoff_state": workflow.get("git_handoff_state"),
        "blocker_count": len(workflow.get("remaining_blockers") or []),
        "human_acceptance_required": workflow.get("human_acceptance_required"),
        "human_acceptance_recorded": workflow.get("human_acceptance_recorded"),
    }
    record = {
        "schema_version": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID,
        "source_system": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM,
        "P18_5_policy_id": REVIEW_VALIDATION_LOOP_POLICY_ID,
        "runtime_boundary_classification": REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION,
        "created_at": observed_at,
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "successful_run_id": review_prepare["successful_run_id"],
        "successful_run_status": "done",
        "successful_run_outcome": "completed",
        "review_prepare_action_SHA256": review_prepare["review_prepare_action_SHA256"],
        "review_package_SHA256": review_prepare["review_package_SHA256"],
        "acceptance_contract_SHA256": review_prepare["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": review_prepare["criteria_revision_SHA256"],
        "kanban_completion_result_SHA256": review_prepare["kanban_completion_result_SHA256"],
        "review_prepare_authority": _review_prepare_authority_projection(review_prepare),
        "pre_acceptance_invariants": pre_acceptance_invariants,
        "acceptor_id": request.acceptor_id,
        "human_acceptance_text": acceptance_text,
        "human_acceptance_text_SHA256": acceptance_text_sha,
        "human_acceptance": {
            "acceptor_id": request.acceptor_id,
            "accepted_at": observed_at,
            "acceptance_reference": f"human_acceptance:{binding.ticket_id}.review",
            "human_acceptance_text_SHA256": acceptance_text_sha,
        },
        "review_acceptance_status": "accepted",
        "review_validation_decision": ReviewValidationLoopDecision.ACCEPT.value,
        "review_validation_state": ReviewValidationLoopState.COMPLETED.value,
        "validation_state": "review_accepted",
        "review_state": "accepted",
        "workflow_state": "P18.9.0-COMPLETED",
        "workflow_status": "completed",
        "governed_workflow_state": GovernedWorkflowState.COMPLETED.value,
        "governed_workflow_transition_triggers": [
            WorkflowTransitionTrigger.HUMAN_APPROVED.value,
        ],
        "human_git_handoff_transition_required": False,
        "human_acceptance_required": True,
        "human_acceptance_recorded": True,
        "pending_human_acceptance_required": False,
        "ticket_closed": True,
        "P18_9_0_closed": True,
        "P18_9_0_completed": True,
        "P18_9_0_acceptance_contract_satisfied": True,
        "git_handoff_required": False,
        "git_handoff_state": "not_required_for_ticket_result",
        "git_handoff_decision_basis": review_prepare["git_handoff_decision_basis"],
        "next_ticket_authority": next_ticket,
        "next_ticket_id": next_ticket["ticket_id"],
        "next_ticket_title": next_ticket["ticket_title"],
        "next_ticket_authority_path": next_ticket["authority_path"],
        "requested_project_id": request.project_id,
        "requested_ticket_id": request.ticket_id,
        "requested_next_action_id": request.next_action_id,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "next_action": {
            "id": next_ticket["next_action_id"],
            "label": (
                f"P18.9.0 is accepted and closed; {next_ticket['ticket_id']} "
                f"{next_ticket['ticket_title']} may be generated only by a separate governed action."
            ),
            "target_ticket_id": next_ticket["ticket_id"],
            "target_ticket_title": next_ticket["ticket_title"],
            "required_human_action": "separate_next_ticket_generation",
        },
        "human_smoke_marker": PEPPER_REVIEW_HUMAN_ACCEPTANCE_READY_MARKER,
    }
    record["review_acceptance_action_SHA256"] = _review_acceptance_record_digest(record)
    return record


def _persist_review_prepare_record(record: dict[str, Any]) -> None:
    validate_p18_9_0_review_prepare_record(record)
    path = p18_9_0_review_prepare_record_path()
    _archive_existing_authority_record(
        path,
        p18_9_0_review_prepare_history_path(),
        reason="replaced_by_current_review_prepare_package",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _persist_review_acceptance_record(record: dict[str, Any]) -> None:
    validate_p18_9_0_review_acceptance_record(record)
    path = p18_9_0_review_acceptance_record_path()
    _archive_existing_authority_record(
        path,
        p18_9_0_review_acceptance_history_path(),
        reason="replaced_by_current_review_acceptance",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _review_prepare_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool,
) -> dict[str, Any]:
    current_invocation_side_effects = {
        "dispatch_performed": False,
        "Kanban_dispatch": False,
        "execution_started": False,
        "worker_process_started": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    return {
        "source_system": PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID,
        "P18_5_policy_id": record["P18_5_policy_id"],
        "runtime_boundary_classification": record["runtime_boundary_classification"],
        "idempotent_replay": idempotent_replay,
        "review_prepare_status": record["review_prepare_status"],
        "review_preparation_recorded": True,
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "review_prepare_action_SHA256": record["review_prepare_action_SHA256"],
        "review_package_SHA256": record["review_package_SHA256"],
        "acceptance_contract_SHA256": record["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": record["criteria_revision_SHA256"],
        "kanban_completion_result_SHA256": record["kanban_completion_result_SHA256"],
        "successful_run_id": record["successful_run_id"],
        "successful_run_status": record["successful_run_status"],
        "successful_run_outcome": record["successful_run_outcome"],
        "validation_state": record["validation_state"],
        "review_state": record["review_state"],
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
        "git_handoff_required": False,
        "git_handoff_state": record["git_handoff_state"],
        "current_invocation_side_effects": current_invocation_side_effects,
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "acceptance_contract": record["acceptance_contract"],
        "kanban_completion_result": record["kanban_completion_result"],
        "review_validation_vocabulary": record["review_validation_vocabulary"],
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": record["human_smoke_marker"],
        "next_action": record["next_action"],
    }


def _review_acceptance_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool,
) -> dict[str, Any]:
    current_invocation_side_effects = {
        "dispatch_performed": False,
        "Kanban_dispatch": False,
        "execution_started": False,
        "worker_process_started": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    return {
        "source_system": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID,
        "P18_5_policy_id": record["P18_5_policy_id"],
        "runtime_boundary_classification": record["runtime_boundary_classification"],
        "idempotent_replay": idempotent_replay,
        "review_acceptance_status": record["review_acceptance_status"],
        "review_acceptance_recorded": True,
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "review_acceptance_action_SHA256": record["review_acceptance_action_SHA256"],
        "human_acceptance_text_SHA256": record["human_acceptance_text_SHA256"],
        "human_acceptance_text": record["human_acceptance_text"],
        "review_prepare_action_SHA256": record["review_prepare_action_SHA256"],
        "review_package_SHA256": record["review_package_SHA256"],
        "acceptance_contract_SHA256": record["acceptance_contract_SHA256"],
        "criteria_revision_SHA256": record["criteria_revision_SHA256"],
        "kanban_completion_result_SHA256": record["kanban_completion_result_SHA256"],
        "successful_run_id": record["successful_run_id"],
        "validation_state": record["validation_state"],
        "review_state": record["review_state"],
        "workflow_state": record["workflow_state"],
        "workflow_status": record["workflow_status"],
        "governed_workflow_state": record["governed_workflow_state"],
        "human_acceptance_required": True,
        "human_acceptance_recorded": True,
        "ticket_closed": True,
        "P18_9_0_closed": True,
        "P18_9_0_completed": True,
        "git_handoff_required": False,
        "git_handoff_state": record["git_handoff_state"],
        "next_ticket_authority": record["next_ticket_authority"],
        "next_ticket_id": record["next_ticket_id"],
        "next_ticket_title": record["next_ticket_title"],
        "current_invocation_side_effects": current_invocation_side_effects,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": record["human_smoke_marker"],
        "next_action": record["next_action"],
    }


def _blocked_current_review_prepare_result(
    projection: dict[str, Any],
    *,
    request: CurrentTicketReviewPrepareRequest,
    blocker_code: str,
    blocker_detail: str,
    completion_source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_system": PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID,
        "review_prepare_status": "blocked",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        **_current_ticket_projection_identity_fields(projection),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "requested_project_id": request.project_id,
        "requested_ticket_id": request.ticket_id,
        "requested_next_action_id": request.next_action_id,
        "review_preparation_recorded": False,
        "human_acceptance_required": False,
        "human_acceptance_recorded": False,
        "completion_source": completion_source,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }


def _blocked_current_review_acceptance_result(
    projection: dict[str, Any],
    *,
    request: CurrentTicketReviewAcceptanceRequest,
    blocker_code: str,
    blocker_detail: str,
    review_prepare_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_system": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID,
        "review_acceptance_status": "blocked",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        **_current_ticket_projection_identity_fields(projection),
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "requested_project_id": request.project_id,
        "requested_ticket_id": request.ticket_id,
        "requested_next_action_id": request.next_action_id,
        "human_acceptance_present": True,
        "human_acceptance_text_SHA256": _review_acceptance_text_digest(
            request.human_acceptance_text
        ),
        "review_acceptance_recorded": False,
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
        "review_prepare_action_SHA256": (
            review_prepare_record.get("review_prepare_action_SHA256")
            if review_prepare_record else None
        ),
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "retry_execution_started": False,
        "automatic_retry_count": 0,
        "automatic_requeue_count": 0,
        "Kanban_requeue_calls": 0,
        "Kanban_reclaim_calls": 0,
        "Kanban_reassign_calls": 0,
        "new_kanban_task_created": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }


def _p18_9_0_review_prepare_overlay(
    projection: dict[str, Any],
    *,
    completed_overlay: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    try:
        record = load_p18_9_0_review_prepare_record(projection_record=projection)
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": "P18-9-0-REVIEW-PREPARE-AUTHORITY",
            "status": "blocked_by_invalid_review_prepare_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    if completed_overlay.get("workflow_status") != "execution_completed":
        return None, {
            "id": "P18-9-0-REVIEW-PREPARE-AUTHORITY",
            "status": "blocked_by_review_prepare_state_mismatch",
            "evidence": "P18.9.0 review preparation exists but execution is not completed",
        }
    acceptance_overlay, acceptance_blocker = _p18_9_0_review_acceptance_overlay(
        projection,
        review_prepare_record=record,
    )
    if acceptance_overlay is not None:
        return acceptance_overlay, None
    if acceptance_blocker is not None:
        return None, acceptance_blocker
    return {
        "readiness": "review_prepared_pending_human_acceptance",
        "workflow_state": "P18.9.0-REVIEW-PREPARED-PENDING-HUMAN-ACCEPTANCE",
        "workflow_status": "review_prepared_pending_human_acceptance",
        "queue_state": completed_overlay.get("queue_state", "kanban_execution_terminal"),
        "execution_state": "no_active_executions",
        "validation_state": "review_prepared_pending_human_acceptance",
        "review_state": "prepared_pending_human_acceptance",
        "recovery_state": "not_required",
        "git_handoff_state": "not_required_for_ticket_result",
        "review_prepare_authority": {
            "policy_id": record["policy_id"],
            "P18_5_policy_id": record["P18_5_policy_id"],
            "runtime_boundary_classification": record["runtime_boundary_classification"],
            "review_prepare_action_SHA256": record["review_prepare_action_SHA256"],
            "review_package_SHA256": record["review_package_SHA256"],
            "acceptance_contract_SHA256": record["acceptance_contract_SHA256"],
            "criteria_revision_SHA256": record["criteria_revision_SHA256"],
            "kanban_completion_result_SHA256": record["kanban_completion_result_SHA256"],
            "successful_run_id": record["successful_run_id"],
            "human_acceptance_required": True,
            "human_acceptance_recorded": False,
        },
        "P18_9_0_review_prepare_present": True,
        "human_acceptance_required": True,
        "human_acceptance_recorded": False,
        "git_handoff_required": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "next_action": {
            "id": binding.review_acceptance_next_action_id,
            "label": (
                f"{binding.ticket_id} review package is prepared; await explicit human "
                "review acceptance before closure."
            ),
            "target_ticket_id": binding.ticket_id,
            "target_ticket_title": binding.ticket_title,
            "required_human_action": "p18_9_0_review_acceptance",
        },
    }, None


def _p18_9_0_review_acceptance_overlay(
    projection: dict[str, Any],
    *,
    review_prepare_record: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    try:
        record = load_p18_9_0_review_acceptance_record(
            projection_record=projection,
            review_prepare_record=review_prepare_record,
        )
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": "P18-9-0-REVIEW-ACCEPTANCE-AUTHORITY",
            "status": "blocked_by_invalid_review_acceptance_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    next_ticket = _p18_9_next_ticket_authority()
    return {
        "current_ticket_id": None,
        "current_ticket_title": None,
        "next_ticket_id": next_ticket["ticket_id"],
        "next_ticket_title": next_ticket["ticket_title"],
        "readiness": "p18_9_0_completed_next_ticket_ready",
        "workflow_state": record["workflow_state"],
        "workflow_status": record["workflow_status"],
        "queue_state": "p18_9_0_closed_next_ticket_ready",
        "execution_state": "no_active_executions",
        "validation_state": record["validation_state"],
        "review_state": record["review_state"],
        "recovery_state": "not_required",
        "git_handoff_state": record["git_handoff_state"],
        "review_prepare_authority": record["review_prepare_authority"],
        "review_acceptance_authority": {
            "policy_id": record["policy_id"],
            "P18_5_policy_id": record["P18_5_policy_id"],
            "runtime_boundary_classification": record["runtime_boundary_classification"],
            "review_acceptance_action_SHA256": record["review_acceptance_action_SHA256"],
            "human_acceptance_text_SHA256": record["human_acceptance_text_SHA256"],
            "review_prepare_action_SHA256": record["review_prepare_action_SHA256"],
            "review_package_SHA256": record["review_package_SHA256"],
            "acceptance_contract_SHA256": record["acceptance_contract_SHA256"],
            "criteria_revision_SHA256": record["criteria_revision_SHA256"],
            "kanban_completion_result_SHA256": record["kanban_completion_result_SHA256"],
            "successful_run_id": record["successful_run_id"],
            "ticket_closed": True,
        },
        "P18_9_0_review_prepare_present": True,
        "P18_9_0_review_acceptance_present": True,
        "P18_9_0_closed": True,
        "P18_9_0_completed": True,
        "next_ticket_ready": True,
        "next_ticket_generated": False,
        "human_acceptance_required": False,
        "human_acceptance_recorded": True,
        "pending_human_acceptance_required": False,
        "git_handoff_required": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "next_action": {
            "id": next_ticket["next_action_id"],
            "label": (
                f"P18.9.0 is accepted and closed; {next_ticket['ticket_id']} "
                f"{next_ticket['ticket_title']} may be generated only by a separate governed action."
            ),
            "target_ticket_id": next_ticket["ticket_id"],
            "target_ticket_title": next_ticket["ticket_title"],
            "required_human_action": "separate_next_ticket_generation",
        },
    }, None


def _current_ticket_execution_start_overlay(
    projection: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    try:
        record = load_p18_9_0_execution_start_record(projection_record=projection)
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": f"{binding.ticket_hyphen_token}-EXECUTION-START-AUTHORITY",
            "status": "blocked_by_invalid_execution_start_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    dispatched_failure = (
        record.get("start_status") == "blocked"
        and bool(record.get("dispatch_performed"))
    )
    if not bool(record.get("execution_started")) and not dispatched_failure:
        return None, None
    try:
        task, runs = _p18_9_0_live_kanban_execution(projection)
        terminal_state = _p18_9_0_terminal_execution_state(
            task,
            runs,
            ticket_id=binding.ticket_id,
        )
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        terminal_state = {
            "start_status": "failed",
            "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
            "blocker_detail": f"Kanban execution state unavailable: {_safe_text(exc, limit=200)}",
            "next_action_id": binding.execution_recovery_next_action_id,
            "outcome": "state_unavailable",
        }
        task = None
        runs = []
    if terminal_state is not None and terminal_state["start_status"] != "completed":
        blocker = {
            "id": f"{binding.ticket_hyphen_token}-WORKER-LIFECYCLE",
            "status": "blocked_by_worker_lifecycle_failure",
            "evidence": terminal_state["blocker_detail"],
            "outcome": terminal_state.get("outcome"),
            "failure_category": terminal_state.get("failure_category"),
            "failure_summary": terminal_state.get("failure_summary"),
        }
        return {
            "readiness": "execution_failed_recovery_required",
            "workflow_state": f"{binding.ticket_id}-EXECUTION-FAILED-RECOVERY-REQUIRED",
            "workflow_status": "execution_failed",
            "queue_state": "kanban_execution_terminal",
            "execution_state": "no_active_executions",
            "validation_state": "execution_failed_before_validation",
            "review_state": "not_started_execution_failed",
            "recovery_state": "recovery_required",
            "ticket_execution_authorized": True,
            "WorkPacket_execution_authorized": True,
            "runtime_execution_authorized": True,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": True,
            "failure_category": terminal_state.get("failure_category"),
            "failure_summary": terminal_state.get("failure_summary"),
            "execution_start_authority": {
                "policy_id": record["policy_id"],
                "start_authorization_SHA256": record["start_authorization_SHA256"],
                "kanban_board_slug": record["kanban_board_slug"],
                "kanban_task_id": record["kanban_task_id"],
                "kanban_run_id": getattr(task, "current_run_id", None) or record.get("kanban_run_id"),
            },
            "worker_lifecycle": {
                "start_status": terminal_state["start_status"],
                "blocker_code": terminal_state["blocker_code"],
                "blocker_detail": terminal_state["blocker_detail"],
                "kanban_task_status": getattr(task, "status", None),
                "latest_run_outcome": terminal_state.get("outcome"),
                "failure_category": terminal_state.get("failure_category"),
                "failure_summary": terminal_state.get("failure_summary"),
                "runs": [_run_dict(run) for run in runs],
            },
            "next_action": {
                "id": binding.execution_recovery_next_action_id,
                "label": (
                    f"{binding.ticket_id} worker start failed; governed recovery "
                    "authorization is required before retry."
                ),
                "target_ticket_id": binding.ticket_id,
                "target_ticket_title": binding.ticket_title,
            },
            "Git_mutation": False,
        }, blocker
    if terminal_state is not None and terminal_state["start_status"] == "completed":
        return {
            "readiness": "execution_completed",
            "workflow_state": f"{binding.ticket_id}-EXECUTION-COMPLETED",
            "workflow_status": "execution_completed",
            "queue_state": "kanban_execution_terminal",
            "execution_state": "no_active_executions",
            "validation_state": "execution_completed_pending_validation",
            "review_state": "ready_for_review_validation",
            "recovery_state": "not_required",
            "ticket_execution_authorized": True,
            "WorkPacket_execution_authorized": True,
            "runtime_execution_authorized": True,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": True,
            "execution_start_authority": {
                "policy_id": record["policy_id"],
                "start_authorization_SHA256": record["start_authorization_SHA256"],
                "kanban_board_slug": record["kanban_board_slug"],
                "kanban_task_id": record["kanban_task_id"],
                "kanban_run_id": record.get("kanban_run_id"),
            },
            "next_action": {
                "id": binding.review_prepare_next_action_id,
                "label": f"{binding.ticket_id} execution completed; prepare review validation.",
                "target_ticket_id": binding.ticket_id,
                "target_ticket_title": binding.ticket_title,
            },
            "Git_mutation": False,
        }, None
    return {
        "readiness": "execution_started",
        "workflow_state": f"{binding.ticket_id}-EXECUTING",
        "workflow_status": "executing",
        "queue_state": "kanban_dispatched",
        "execution_state": "active_executions",
        "validation_state": "execution_in_progress",
        "review_state": "not_started_execution_in_progress",
        "recovery_state": "not_required",
        "ticket_execution_authorized": True,
        "WorkPacket_execution_authorized": True,
        "runtime_execution_authorized": True,
        "execution_started": True,
        "worker_execution": True,
        "Kanban_dispatch": True,
        "execution_start_authority": {
            "policy_id": record["policy_id"],
            "start_authorization_SHA256": record["start_authorization_SHA256"],
            "kanban_board_slug": record["kanban_board_slug"],
            "kanban_task_id": record["kanban_task_id"],
            "kanban_run_id": record.get("kanban_run_id"),
        },
        "next_action": {
            "id": binding.monitor_execution_next_action_id,
            "label": (
                f"{binding.ticket_id} execution has started; monitor the Kanban run "
                "and await worker completion."
            ),
            "target_ticket_id": binding.ticket_id,
            "target_ticket_title": binding.ticket_title,
        },
        "Git_mutation": False,
    }, None


def _p18_9_0_execution_start_overlay(
    projection: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    return _current_ticket_execution_start_overlay(projection)


def _p18_9_0_recovery_overlay(
    projection: dict[str, Any],
    *,
    start_overlay: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    try:
        record = load_p18_9_0_recovery_action_record(projection_record=projection)
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": "P18-9-0-RECOVERY-AUTHORITY",
            "status": "blocked_by_invalid_recovery_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    if not _recovery_record_matches_current_failure(projection, record):
        return None, None
    if start_overlay.get("workflow_status") != "execution_failed":
        return None, {
            "id": "P18-9-0-RECOVERY-AUTHORITY",
            "status": "blocked_by_recovery_state_mismatch",
            "evidence": "P18.9.0 recovery authority exists but execution is not failed",
        }
    return {
        "readiness": "execution_failed_retry_pending",
        "workflow_state": "P18.9.0-RETRY-PENDING-NOT-DISPATCHED",
        "workflow_status": "retry_pending",
        "queue_state": "kanban_retry_prepared_not_dispatched",
        "execution_state": "no_active_executions",
        "validation_state": "execution_failed_retry_pending",
        "review_state": "not_started_execution_failed",
        "recovery_state": "retry_pending",
        "retry_state": "retry_pending",
        "ticket_execution_authorized": True,
        "WorkPacket_execution_authorized": True,
        "runtime_execution_authorized": True,
        "execution_started": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "recovery_authority": {
            "policy_id": record["policy_id"],
            "P18_6_policy_id": record["P18_6_policy_id"],
            "runtime_boundary_classification": record["runtime_boundary_classification"],
            "recovery_action_SHA256": record["recovery_action_SHA256"],
            "human_authorization_SHA256": record["human_authorization_SHA256"],
            "retry_identity_model": record["retry_identity_model"],
            "next_attempt_number": record["next_attempt_number"],
            "future_task_skills": record["future_task_skills"],
            "future_retry_capability_surface": record["future_retry_capability_surface"],
            "unresolved_Hermes_task_skills": record["unresolved_Hermes_task_skills"],
            "Kanban_requeue_calls": record["Kanban_requeue_calls"],
            "Kanban_reclaim_calls": record["Kanban_reclaim_calls"],
            "retry_execution_count": record["retry_execution_count"],
        },
        "failure_category": record.get("failure_category") or start_overlay.get("failure_category"),
        "failure_summary": record.get("failure_summary") or start_overlay.get("failure_summary"),
        "worker_lifecycle": {
            "status": "historical_failure_recovered",
            "current_lifecycle_blocker": None,
            "historical_lifecycle_blocker_consumed": True,
            "latest_failed_run_id": record.get("latest_failed_run_id"),
            "failure_category": record.get("failure_category") or start_overlay.get("failure_category"),
            "failure_summary": record.get("failure_summary") or start_overlay.get("failure_summary"),
        },
        "next_action": {
            "id": binding.retry_start_next_action_id,
            "label": (
                f"{binding.ticket_id} recovery authorization is recorded and retry is pending; "
                "a separate governed retry-start authorization is required before run 2."
            ),
            "target_ticket_id": binding.ticket_id,
            "target_ticket_title": binding.ticket_title,
            "required_human_action": "retry_start_authorization",
        },
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }, None


def _p18_9_0_retry_start_overlay(
    projection: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    try:
        recovery = load_p18_9_0_recovery_action_record(projection_record=projection)
        if recovery is None:
            return None, None
        record = load_p18_9_0_retry_start_record(
            projection_record=projection,
            recovery_record=recovery,
            allow_historical_mismatch=True,
        )
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": "P18-9-0-RETRY-START-AUTHORITY",
            "status": "blocked_by_invalid_retry_start_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    if record.get("recovery_action_SHA256") != recovery.get("recovery_action_SHA256"):
        return None, None
    if _retry_start_record_cycle_id(record, recovery, projection) != _recovery_record_cycle_id(recovery, projection):
        return None, None
    authority = {
        "policy_id": record["policy_id"],
        "retry_start_authorization_SHA256": record["retry_start_authorization_SHA256"],
        "recovery_action_SHA256": record["recovery_action_SHA256"],
        "retry_identity_model": record["retry_identity_model"],
        "previous_attempt_count": record["previous_attempt_count"],
        "next_attempt_number": record["next_attempt_number"],
        "future_task_skills": record["future_task_skills"],
        "future_retry_capability_surface": record["future_retry_capability_surface"],
        "unresolved_Hermes_task_skills": record["unresolved_Hermes_task_skills"],
        "retry_execution_count": record["retry_execution_count"],
        "Kanban_requeue_calls": record["Kanban_requeue_calls"],
        "Kanban_reclaim_calls": record["Kanban_reclaim_calls"],
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_run_id": record.get("kanban_run_id"),
    }
    if not bool(record.get("execution_started")):
        return {
            "readiness": "execution_failed_retry_pending",
            "workflow_state": "P18.9.0-RETRY-PENDING-NOT-DISPATCHED",
            "workflow_status": "retry_pending",
            "queue_state": "kanban_retry_prepared_not_dispatched",
            "execution_state": "no_active_executions",
            "validation_state": "execution_failed_retry_pending",
            "review_state": "not_started_execution_failed",
            "recovery_state": "retry_pending",
            "retry_state": "retry_pending",
            "ticket_execution_authorized": True,
            "WorkPacket_execution_authorized": True,
            "runtime_execution_authorized": True,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "retry_execution_started": False,
            "retry_execution_count": int(record.get("retry_execution_count") or 0),
            "retry_start_authority": authority,
            "failure_category": record.get("failure_category"),
            "failure_summary": record.get("failure_summary"),
            "worker_lifecycle": {
                "status": "historical_failure_recovered",
                "current_lifecycle_blocker": None,
                "historical_lifecycle_blocker_consumed": True,
                "latest_failed_run_id": record.get("latest_failed_run_id"),
                "failure_category": record.get("failure_category"),
                "failure_summary": record.get("failure_summary"),
            },
            "retry_start_blocker": {
                "blocker_code": record.get("blocker_code"),
                "blocker_detail": record.get("blocker_detail"),
                "task_prepare_status": record.get("task_prepare_status"),
                "dispatch_performed": bool(record.get("dispatch_performed")),
                "worker_process_started": False,
                "historical_lifecycle_blocker_consumed": True,
            },
            "next_action": {
                "id": binding.retry_start_next_action_id,
                "label": (
                    f"{binding.ticket_id} retry is still pending; resolve the recorded retry-start "
                    "blocker and submit separate governed retry-start authorization."
                ),
                "target_ticket_id": binding.ticket_id,
                "target_ticket_title": binding.ticket_title,
                "required_human_action": "retry_start_authorization",
            },
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }, None
    try:
        task, runs = _p18_9_0_live_kanban_execution(projection)
        terminal_state = _p18_9_0_terminal_execution_state(task, runs)
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        terminal_state = {
            "start_status": "failed",
            "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
            "blocker_detail": f"Kanban retry execution state unavailable: {_safe_text(exc, limit=200)}",
            "next_action_id": "RECOVER_P18_9_0_EXECUTION",
            "outcome": "state_unavailable",
        }
        task = None
        runs = []
    authority["kanban_run_id"] = getattr(task, "current_run_id", None) or record.get("kanban_run_id")
    if terminal_state is not None and terminal_state["start_status"] != "completed":
        blocker = {
            "id": "P18-9-0-RETRY-WORKER-LIFECYCLE",
            "status": "blocked_by_worker_lifecycle_failure",
            "evidence": terminal_state["blocker_detail"],
            "outcome": terminal_state.get("outcome"),
            "failure_category": terminal_state.get("failure_category"),
            "failure_summary": terminal_state.get("failure_summary"),
        }
        return {
            "readiness": "retry_execution_failed_recovery_required",
            "workflow_state": "P18.9.0-RETRY-EXECUTION-FAILED-RECOVERY-REQUIRED",
            "workflow_status": "execution_failed",
            "queue_state": "kanban_retry_execution_terminal",
            "execution_state": "no_active_executions",
            "validation_state": "retry_execution_failed_before_validation",
            "review_state": "not_started_execution_failed",
            "recovery_state": "recovery_required",
            "retry_state": "retry_failed",
            "ticket_execution_authorized": True,
            "WorkPacket_execution_authorized": True,
            "runtime_execution_authorized": True,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": True,
            "retry_execution_started": False,
            "retry_execution_count": record["retry_execution_count"],
            "retry_start_authority": authority,
            "failure_category": terminal_state.get("failure_category"),
            "failure_summary": terminal_state.get("failure_summary"),
            "worker_lifecycle": {
                "start_status": terminal_state["start_status"],
                "blocker_code": terminal_state["blocker_code"],
                "blocker_detail": terminal_state["blocker_detail"],
                "kanban_task_status": getattr(task, "status", None),
                "latest_run_outcome": terminal_state.get("outcome"),
                "failure_category": terminal_state.get("failure_category"),
                "failure_summary": terminal_state.get("failure_summary"),
                "runs": [_run_dict(run) for run in runs],
            },
            "next_action": {
                "id": "RECOVER_P18_9_0_EXECUTION",
                "label": "P18.9.0 retry execution failed; governed recovery authorization is required before another action.",
                "target_ticket_id": PEPPER_NEXT_TICKET_ID,
                "target_ticket_title": PEPPER_NEXT_TICKET_TITLE,
            },
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }, blocker
    if terminal_state is not None and terminal_state["start_status"] == "completed":
        return {
            "readiness": "retry_execution_completed",
            "workflow_state": "P18.9.0-RETRY-EXECUTION-COMPLETED",
            "workflow_status": "execution_completed",
            "queue_state": "kanban_retry_execution_terminal",
            "execution_state": "no_active_executions",
            "validation_state": "execution_completed_pending_validation",
            "review_state": "ready_for_review_validation",
            "recovery_state": "not_required",
            "retry_state": "retry_completed",
            "ticket_execution_authorized": True,
            "WorkPacket_execution_authorized": True,
            "runtime_execution_authorized": True,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": True,
            "retry_execution_started": False,
            "retry_execution_count": record["retry_execution_count"],
            "retry_start_authority": authority,
            "next_action": {
                "id": "PREPARE_P18_9_0_REVIEW",
                "label": "P18.9.0 retry execution completed; prepare review validation.",
                "target_ticket_id": PEPPER_NEXT_TICKET_ID,
                "target_ticket_title": PEPPER_NEXT_TICKET_TITLE,
            },
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }, None
    return {
        "readiness": "retry_execution_started",
        "workflow_state": "P18.9.0-EXECUTING",
        "workflow_status": "executing",
        "queue_state": "kanban_dispatched",
        "execution_state": "active_executions",
        "validation_state": "execution_in_progress",
        "review_state": "not_started_execution_in_progress",
        "recovery_state": "not_required",
        "retry_state": "retry_executing",
        "ticket_execution_authorized": True,
        "WorkPacket_execution_authorized": True,
        "runtime_execution_authorized": True,
        "execution_started": True,
        "worker_execution": True,
        "Kanban_dispatch": True,
        "retry_execution_started": True,
        "retry_execution_count": record["retry_execution_count"],
        "retry_start_authority": authority,
        "next_action": {
            "id": "MONITOR_P18_9_0_EXECUTION",
            "label": "P18.9.0 retry execution has started; monitor the Kanban run and await worker completion.",
            "target_ticket_id": PEPPER_NEXT_TICKET_ID,
            "target_ticket_title": PEPPER_NEXT_TICKET_TITLE,
        },
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }, None


def _p18_9_0_live_kanban_execution(
    projection: dict[str, Any],
) -> tuple[Any, list[Any]]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        _reconcile_kanban_board_lifecycle(conn, task_id=task_id)
        task = kanban_db.get_task(conn, task_id)
        runs = kanban_db.list_runs(conn, task_id) if task is not None else []
        return task, runs
    finally:
        conn.close()


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
    generation_overlay, generation_blocker = _p18_9_0_generation_overlay()
    if generation_blocker is not None:
        remaining_blockers.append(generation_blocker)
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
    canonical_next = resolve_canonical_next_ticket({
        "project_id": PEPPER_GOVERNED_PROJECT_ID,
        "project_name": PEPPER_GOVERNED_PROJECT_NAME,
        "macroproject_id": PEPPER_GOVERNED_MACROPROJECT_ID,
        "macroproject_title": PEPPER_GOVERNED_MACROPROJECT_TITLE,
    })
    next_action = {
        "id": canonical_next["next_action_id"],
        "label": (
            f"Generate governed {canonical_next['ticket_id']} "
            f"{canonical_next['ticket_title']} before execution."
        ),
        "target_ticket_id": canonical_next["ticket_id"],
        "target_ticket_title": canonical_next["ticket_title"],
        "required_human_action": "ticket_generation",
    }
    observed_at = _utc_now_iso()
    snapshot = {
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
        "next_ticket_id": canonical_next["ticket_id"],
        "next_ticket_title": canonical_next["ticket_title"],
        "canonical_next_ticket_authority": canonical_next,
        "mode": "controlled_default",
        "readiness": "planning_approved_or_intake_ready",
        "workflow_state": "P18.9-PEPPER-PRODUCT-PERSONALIZATION-INTAKE-READY",
        "workflow_status": "planning_approved_or_intake_ready",
        "approval_state": approval_summary["approval_state"],
        "pending_approval_count": approval_summary["pending_approval_count"],
        "queue_state": f"ready_to_generate_{canonical_next['ticket_id'].replace('.', '_')}",
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
    if generation_overlay is not None:
        snapshot.update(generation_overlay)
        if snapshot.get("P18_9_0_closed") is True:
            snapshot["ready_verdict"] = (
                "p18_9_0_completed_by_human_review_acceptance_with_next_ticket_ready"
            )
        else:
            snapshot["ready_verdict"] = (
                "p18_9_0_generated_awaiting_human_ticket_approval_with_preserved_execution_boundary"
            )
    elif generation_blocker is not None:
        snapshot["readiness"] = "blocked_invalid_generated_ticket_authority"
        snapshot["workflow_status"] = "blocked_invalid_generated_ticket_authority"
        snapshot["queue_state"] = "blocked_invalid_generated_ticket_authority"
        snapshot["ready_verdict"] = "p18_9_0_generation_authority_invalid"
    if (
        generation_blocker is None
        and snapshot.get("current_ticket_id") in {None, ""}
        and snapshot.get("next_ticket_ready") is not False
    ):
        canonical_next = resolve_canonical_next_ticket(snapshot)
        snapshot["next_ticket_id"] = canonical_next["ticket_id"]
        snapshot["next_ticket_title"] = canonical_next["ticket_title"]
        snapshot["next_action"] = {
            "id": canonical_next["next_action_id"],
            "label": (
                f"Generate governed {canonical_next['ticket_id']} "
                f"{canonical_next['ticket_title']}."
            ),
            "target_ticket_id": canonical_next["ticket_id"],
            "target_ticket_title": canonical_next["ticket_title"],
            "required_human_action": "ticket_generation",
        }
        if snapshot.get("P18_9_0_closed") is not True:
            snapshot["queue_state"] = f"ready_to_generate_{canonical_next['ticket_id'].replace('.', '_')}"
        snapshot["canonical_next_ticket_authority"] = canonical_next
    else:
        snapshot["canonical_next_ticket_authority"] = None
    snapshot["blocker_count"] = len(remaining_blockers)
    snapshot["next_action_label"] = _next_action_label(snapshot.get("next_action"))
    return snapshot


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
        "next_ticket_id": _workflow_value(workflow, "next_ticket_id"),
        "next_ticket_title": _workflow_value(workflow, "next_ticket_title"),
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
    workflow_status = _workflow_value(workflow, "workflow_status", workflow.get("readiness"))
    approval_state = _approval_state(pending_approval_count)
    if workflow_status == "awaiting_ticket_approval":
        approval_state = _workflow_value(workflow, "approval_state", "pending_ticket_approval")
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
        "workflow_status": workflow_status,
        "approval_state": approval_state,
        "pending_approval_count": pending_approval_count,
        "pending_ticket_approval_count": int(workflow.get("pending_ticket_approval_count") or 0),
        "queue_state": _workflow_value(workflow, "queue_state", "unavailable"),
        "execution_state": _execution_state(active_execution_count),
        "execution_count": execution_count,
        "active_execution_count": active_execution_count,
        "validation_state": _workflow_value(workflow, "validation_state", "unavailable"),
        "review_state": _workflow_value(workflow, "review_state", "unavailable"),
        "recovery_state": _workflow_value(workflow, "recovery_state", "unavailable"),
        "failure_category": workflow.get("failure_category"),
        "failure_summary": workflow.get("failure_summary"),
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
