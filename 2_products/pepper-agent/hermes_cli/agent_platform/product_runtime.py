"""Pepper product runtime adapters for controlled default mode.

This module is intentionally a thin projection layer. It reuses Hermes staged
write approvals and Kanban run evidence, and it exposes bounded product shapes
for the dashboard without creating a second approval engine, executor, review
engine, or Git authority path.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import difflib
import hashlib
import json
import os
import re
import shutil
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
PEPPER_SCRATCH_SOURCE_MATERIALIZATION_POLICY_ID = (
    "pepper-governed-workpacket-scratch-source-materialization-v1"
)
PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST = (
    ".hermes-agent-platform/workpacket-source-materialization.json"
)
PEPPER_SCRATCH_DEPENDENCY_SUBSTRATE_POLICY_ID = (
    "pepper-governed-workpacket-scratch-dependency-substrate-v1"
)
IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP = (
    "IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP"
)
DEPENDENCY_SOURCE_NOT_FOUND = "DEPENDENCY_SOURCE_NOT_FOUND"
DEPENDENCY_MATERIALIZATION_FAILED = "DEPENDENCY_MATERIALIZATION_FAILED"
DEPENDENCY_PROVENANCE_MISMATCH = "DEPENDENCY_PROVENANCE_MISMATCH"
VALIDATION_RUNTIME_UNAVAILABLE = "VALIDATION_RUNTIME_UNAVAILABLE"
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
PEPPER_GOVERNED_AUTONOMY_ACTION_SOURCE_SYSTEM = "pepper-governed-autonomy-action"
PEPPER_GOVERNED_AUTONOMY_ACTION_SCHEMA_VERSION = 1
PEPPER_GOVERNED_AUTONOMY_ACTION_POLICY_ID = (
    "pepper-governed-autonomy-runtime-01ai-v1"
)
PEPPER_GOVERNED_AUTONOMY_ACTION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-governed-autonomy-action-sha256-v1"
)
PEPPER_GOVERNED_AUTONOMY_A2A_POLICY_ID = (
    "pepper-governed-autonomy-same-authority-a2a-v1"
)
PEPPER_GOVERNED_AUTONOMY_READY_MARKER = (
    "PEPPER-GOVERNED-AUTONOMY-EXECUTION-PLANE-AND-A2A-CLOSURE-READY"
)
PEPPER_LEGACY_GOVERNED_AUTONOMY_READY_MARKER = (
    "PEPPER-GOVERNED-AUTONOMY-RUNTIME-AND-A2A-INTEGRATION-READY"
)
PEPPER_GOVERNED_AUTONOMY_LIVE_CONTINUATION_MARKER = (
    "READY_FOR_LIVE_P18_9_1_AUTONOMOUS_CONTINUATION"
)
PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON = (
    "governed_autonomy_internal_continuation"
)
PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON = (
    "human_requested_fresh_execution_after_runtime_substrate_correction"
)
PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM = (
    "pepper-governed-autonomy-runtime"
)
PEPPER_GOVERNED_AUTONOMY_RUNTIME_SCHEMA_VERSION = 1
PEPPER_GOVERNED_AUTONOMY_RUNTIME_POLICY_ID = (
    "pepper-governed-autonomy-operational-continuation-01ai-v1"
)
PEPPER_GOVERNED_AUTONOMY_RUNTIME_DIGEST_ALGORITHM = (
    "agent-platform-pepper-governed-autonomy-runtime-sha256-v1"
)
PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_DIGEST_ALGORITHM = (
    "agent-platform-pepper-governed-autonomy-fresh-execution-request-sha256-v1"
)
PEPPER_GOVERNED_AUTONOMY_AUTHORITY_DIGEST_ALGORITHM = (
    "agent-platform-pepper-governed-autonomy-backend-derived-live-authority-sha256-v1"
)

_GOVERNED_TICKET_START_STORE_DIR = Path("agent-platform") / "pepper-worker-start-action"
_GOVERNED_TICKET_RECOVERY_STORE_DIR = Path("agent-platform") / "pepper-recovery-action"
_GOVERNED_TICKET_REVIEW_PREPARE_STORE_DIR = Path("agent-platform") / "pepper-review-prepare-action"
_GOVERNED_TICKET_REVIEW_ACCEPTANCE_STORE_DIR = (
    Path("agent-platform") / "pepper-review-human-acceptance-action"
)
_GOVERNED_TICKET_AUTONOMY_STORE_DIR = (
    Path("agent-platform") / "pepper-governed-autonomy-action"
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
    "governed_autonomy_activation": (
        _GOVERNED_TICKET_AUTONOMY_STORE_DIR,
        "governed-autonomy-activation.json",
    ),
    "governed_autonomy_activation_history": (
        _GOVERNED_TICKET_AUTONOMY_STORE_DIR,
        "governed-autonomy-activation.history.jsonl",
    ),
    "governed_autonomy_runtime_state": (
        _GOVERNED_TICKET_AUTONOMY_STORE_DIR,
        "governed-autonomy-runtime.json",
    ),
    "governed_autonomy_runtime_history": (
        _GOVERNED_TICKET_AUTONOMY_STORE_DIR,
        "governed-autonomy-runtime.history.jsonl",
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
_SAFE_GOVERNED_AUTONOMY_REF_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{0,127}$")
_SAFE_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_GOVERNED_AUTONOMY_RUNTIME_DECISIONS = frozenset({
    "DIRECT",
    "TASK_LOCAL_SELF_EXTENSION",
    "A2A_DELEGATION",
    "STOP_FOR_HUMAN",
})
_GOVERNED_AUTONOMY_STABLE_AUTHORITY_FIELDS = (
    "authority_kind",
    "authority_lifecycle",
    "01AH_envelope_lifecycle_classification",
    "policy_id",
    "ticket_id",
    "source_ticket_SHA256",
    "work_packet_id",
    "work_packet_SHA256",
    "single_agent_result_SHA256",
    "allocation_SHA256",
    "profile_SHA256",
    "projection_SHA256",
    "approval_publication_SHA256",
    "dependency_plan_SHA256",
    "allowed_paths_SHA256",
    "forbidden_paths_SHA256",
    "validation_steps_SHA256",
    "kanban_board_slug",
    "kanban_task_id",
    "assignee_profile",
    "selected_profile",
    "execution_profile_role",
    "workspace_kind",
    "live_lineage_activation_authorized",
    "provider_dispatch_count",
    "model_inference_count",
    "budget",
)
_GOVERNED_AUTONOMY_MUTABLE_AUTHORITY_FIELDS = (
    "envelope_SHA256",
    "workspace_path_SHA256",
    "source_run_id",
    "source_run_status",
    "source_run_outcome",
    "source_run_profile",
    "source_run_snapshot_SHA256",
    "source_run_count",
    "active_execution_count",
)
_GOVERNED_AUTONOMY_A2A_ALLOWED_OPERATIONS = frozenset({
    "list_directory",
    "read_file",
    "create_file",
    "replace_file",
    "delete_file",
    "create_directory",
    "delete_directory",
})
_GOVERNED_AUTONOMY_A2A_PRIVILEGED_OPERATIONS = frozenset({
    "execute_command",
    "validation_command",
    "git_read_only",
    "git_mutation",
    "network_access",
    "workspace_mutation",
    "provider_call",
    "model_call",
    "agent_control",
    "worker_control",
    "docker",
    "docker_command",
    "graphify",
    "graphify_command",
    "dependency_install",
    "package_install",
    "git_add",
    "git_commit",
    "git_push",
    "git_reset",
    "git_clean",
    "git_stash",
    "git_checkout",
    "git_worktree",
})


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


@dataclass(frozen=True)
class _BackendDerivedGovernedAutonomyAuthority:
    authority_kind: str
    policy_id: str
    envelope_SHA256: str
    ticket_id: str
    source_ticket_SHA256: str
    work_packet_id: str
    work_packet_SHA256: str
    live_lineage_activation_authorized: bool
    provider_dispatch_count: int
    model_inference_count: int
    allowed_paths: tuple[str, ...]
    forbidden_paths: tuple[str, ...]


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


class CurrentTicketGovernedAutonomyActivationRequest(BaseModel):
    """Request body for dispatch-free 01AH autonomy activation status."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    human_request_text: str = Field(min_length=1, max_length=1024)
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

    @field_validator("human_request_text")
    @classmethod
    def request_text_must_be_text(cls, value: str) -> str:
        if _CONTROL_CHARS.search(value):
            raise ValueError("human_request_text contains control characters")
        return value


class CurrentTicketGovernedAutonomyContinuationRequest(BaseModel):
    """Request body for consuming active server-derived 01AH authority."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    runtime_goal: str = Field(min_length=1, max_length=1024)
    observed_failure: str | None = Field(default=None, max_length=1024)
    requested_capability: str | None = Field(default=None, max_length=1024)
    strategy: Literal[
        "AUTO",
        "DIRECT",
        "TASK_LOCAL_SELF_EXTENSION",
        "A2A_DELEGATION",
        "STOP_FOR_HUMAN",
    ] = "AUTO"
    task_local_tool_name: str | None = Field(default=None, max_length=64)
    task_local_language: Literal["python", "javascript", "typescript"] = "python"
    task_local_implementation_path: str | None = Field(default=None, max_length=512)
    task_local_source_text: str | None = Field(default=None, max_length=65536)
    task_local_command: str | None = Field(default=None, max_length=4096)
    delegate_goal: str | None = Field(default=None, max_length=1024)
    delegate_paths: tuple[str, ...] = ()
    delegate_requested_operations: tuple[str, ...] = ()
    delegate_result: dict[str, Any] | None = None
    fresh_execution_request_text: str | None = Field(default=None, max_length=1024)
    project_id: str | None = Field(default=None, max_length=128)
    ticket_id: str | None = Field(default=None, max_length=128)

    @field_validator(
        "runtime_goal",
        "observed_failure",
        "requested_capability",
        "delegate_goal",
        "fresh_execution_request_text",
    )
    @classmethod
    def bounded_text_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if _CONTROL_CHARS.search(value):
            raise ValueError("runtime text contains control characters")
        return value

    @field_validator("project_id", "ticket_id")
    @classmethod
    def optional_guards_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not _SAFE_ID.fullmatch(value):
            raise ValueError("invalid guarded identifier")
        return value

    @field_validator("task_local_tool_name")
    @classmethod
    def optional_tool_name_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,63}", value):
            raise ValueError("invalid task-local tool name")
        return value

    @field_validator("task_local_implementation_path")
    @classmethod
    def optional_runtime_path_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        _normalize_runtime_relative_path(value)
        return value

    @field_validator("task_local_source_text", "task_local_command")
    @classmethod
    def optional_runtime_payload_must_be_safe(cls, value: str | None) -> str | None:
        if value in {None, ""}:
            return None
        if "\x00" in value or _CONTROL_CHARS.search(value.replace("\n", "")):
            raise ValueError("runtime payload contains control characters")
        return value

    @field_validator("delegate_paths")
    @classmethod
    def delegate_paths_must_be_safe(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(_normalize_runtime_relative_path(item) for item in value)

    @field_validator("delegate_requested_operations")
    @classmethod
    def delegate_operations_must_be_safe(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        safe: list[str] = []
        for item in value:
            candidate = str(item or "").strip().lower().replace("-", "_")
            if not candidate or not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", candidate):
                raise ValueError("invalid delegate operation")
            safe.append(candidate)
        return tuple(safe)

    @field_validator("delegate_result")
    @classmethod
    def delegate_result_must_be_object(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ValueError("delegate_result must be an object")
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


def _normalize_runtime_relative_path(value: object) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if not text or text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        raise ProductRuntimeConflict("runtime path must be repository-relative")
    if _CONTROL_CHARS.search(text):
        raise ProductRuntimeConflict("runtime path contains control characters")
    parts = [part for part in text.split("/") if part]
    if not parts or any(part in {".", ".."} for part in parts):
        raise ProductRuntimeConflict("runtime path contains traversal components")
    return "/".join(parts)


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


def governed_autonomy_continuation_action_id(ticket_id: str) -> str:
    token = governed_ticket_lifecycle_action_token(ticket_id)
    return f"CONTINUE_{token}_GOVERNED_AUTONOMY"


def governed_ticket_recovery_authorization_text(ticket_id: str) -> str:
    """Return the canonical explicit recovery authorization phrase for a ticket."""

    return f"Autorizo explícitamente la recuperación de la ejecución fallida de {ticket_id}."


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
                                            next_retry_start_overlay, next_retry_start_blocker = (
                                                _p18_9_0_retry_start_overlay(next_projection)
                                            )
                                            if next_retry_start_overlay is not None:
                                                overlay.update(next_retry_start_overlay)
                                            if next_retry_start_blocker is not None:
                                                return overlay, next_retry_start_blocker
                                            if next_retry_start_overlay is None:
                                                next_recovery_overlay, next_recovery_blocker = (
                                                    _p18_9_0_recovery_overlay(
                                                        next_projection,
                                                        start_overlay=next_start_overlay,
                                                    )
                                                )
                                                if next_recovery_overlay is not None:
                                                    overlay.update(next_recovery_overlay)
                                                if next_recovery_blocker is not None:
                                                    return overlay, next_recovery_blocker
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
                                        next_retry_start_overlay, next_retry_start_blocker = (
                                            _p18_9_0_retry_start_overlay(next_projection)
                                        )
                                        if next_retry_start_overlay is not None:
                                            overlay.update(next_retry_start_overlay)
                                        if next_retry_start_blocker is not None:
                                            return overlay, next_retry_start_blocker
                                        if next_retry_start_overlay is None:
                                            next_recovery_overlay, next_recovery_blocker = (
                                                _p18_9_0_recovery_overlay(
                                                    next_projection,
                                                    start_overlay=next_start_overlay,
                                                )
                                            )
                                            if next_recovery_overlay is not None:
                                                overlay.update(next_recovery_overlay)
                                            if next_recovery_blocker is not None:
                                                return overlay, next_recovery_blocker
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

    return recovery_action_record_path_for_ticket(PEPPER_BOOTSTRAP_NEXT_TICKET_ID)


def p18_9_0_recovery_action_history_path() -> Path:
    """Return the append-only P18.9.0 recovery authority history path."""

    return recovery_action_history_path_for_ticket(PEPPER_BOOTSTRAP_NEXT_TICKET_ID)


def p18_9_0_retry_start_record_path() -> Path:
    """Return the profile-scoped P18.9.0 retry-start authority path."""

    return retry_start_record_path_for_ticket(PEPPER_BOOTSTRAP_NEXT_TICKET_ID)


def p18_9_0_retry_start_history_path() -> Path:
    """Return the append-only P18.9.0 retry-start authority history path."""

    return retry_start_history_path_for_ticket(PEPPER_BOOTSTRAP_NEXT_TICKET_ID)


def recovery_action_record_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped recovery authority path for one ticket."""

    return governed_ticket_lifecycle_authority_path(
        "recovery_action",
        ticket_id=ticket_id,
    )


def recovery_action_history_path_for_ticket(ticket_id: str) -> Path:
    """Return the append-only recovery authority history path for one ticket."""

    return governed_ticket_lifecycle_authority_path(
        "recovery_action_history",
        ticket_id=ticket_id,
    )


def retry_start_record_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped retry-start authority path for one ticket."""

    return governed_ticket_lifecycle_authority_path(
        "retry_start",
        ticket_id=ticket_id,
    )


def retry_start_history_path_for_ticket(ticket_id: str) -> Path:
    """Return the append-only retry-start authority history path for one ticket."""

    return governed_ticket_lifecycle_authority_path(
        "retry_start_history",
        ticket_id=ticket_id,
    )


def governed_autonomy_activation_record_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped governed-autonomy activation path."""

    return governed_ticket_lifecycle_authority_path(
        "governed_autonomy_activation",
        ticket_id=ticket_id,
    )


def governed_autonomy_activation_history_path_for_ticket(ticket_id: str) -> Path:
    """Return the append-only governed-autonomy activation history path."""

    return governed_ticket_lifecycle_authority_path(
        "governed_autonomy_activation_history",
        ticket_id=ticket_id,
    )


def governed_autonomy_runtime_state_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped governed-autonomy runtime state path."""

    return governed_ticket_lifecycle_authority_path(
        "governed_autonomy_runtime_state",
        ticket_id=ticket_id,
    )


def governed_autonomy_runtime_history_path_for_ticket(ticket_id: str) -> Path:
    """Return the append-only governed-autonomy runtime history path."""

    return governed_ticket_lifecycle_authority_path(
        "governed_autonomy_runtime_history",
        ticket_id=ticket_id,
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


def _bootstrap_projection_record_for_validation() -> dict[str, Any]:
    from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
        load_p18_9_0_kanban_projection_record,
    )

    projection = load_p18_9_0_kanban_projection_record()
    if projection is None:
        projection = _load_current_projection_record()
    return projection


def _recovery_action_record_path_for_projection(
    projection_record: dict[str, Any] | None = None,
) -> Path:
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    return recovery_action_record_path_for_ticket(str(projection["ticket_id"]))


def _retry_start_record_path_for_projection(
    projection_record: dict[str, Any] | None = None,
) -> Path:
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    return retry_start_record_path_for_ticket(str(projection["ticket_id"]))


def _load_recovery_action_record_from_path(
    path: Path,
    *,
    projection_record: dict[str, Any],
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "execution recovery action record is unreadable"
        ) from exc
    return validate_p18_9_0_recovery_action_record(
        record,
        projection_record=projection_record,
    )


def load_current_ticket_recovery_action_record(
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the current ticket recovery record, if present."""

    projection = projection_record if projection_record is not None else _load_current_projection_record()
    return _load_recovery_action_record_from_path(
        recovery_action_record_path_for_ticket(str(projection["ticket_id"])),
        projection_record=projection,
    )


def load_p18_9_0_recovery_action_record(
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the bounded P18.9.0 recovery record, if present."""

    path = p18_9_0_recovery_action_record_path()
    if not path.exists():
        return None
    projection = (
        projection_record
        if projection_record is not None
        else _bootstrap_projection_record_for_validation()
    )
    return _load_recovery_action_record_from_path(
        path,
        projection_record=projection,
    )


def _load_retry_start_record_from_path(
    path: Path,
    *,
    projection_record: dict[str, Any],
    recovery_record: dict[str, Any] | None = None,
    allow_historical_mismatch: bool = False,
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "execution retry-start authorization record is unreadable"
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
        recovery = recovery_record
        if recovery is None:
            recovery = load_current_ticket_recovery_action_record(
                projection_record=projection_record,
            )
        if recovery is None:
            raise
        same_recovery_authority = (
            record.get("recovery_action_SHA256") == recovery.get("recovery_action_SHA256")
        )
        same_recovery_cycle = (
            _retry_start_record_cycle_id(record, recovery, projection_record)
            == _recovery_record_cycle_id(recovery, projection_record)
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
            projection_record=projection_record,
            recovery_record=historical_recovery,
        )
        return record


def load_current_ticket_retry_start_record(
    *,
    projection_record: dict[str, Any] | None = None,
    recovery_record: dict[str, Any] | None = None,
    allow_historical_mismatch: bool = False,
) -> dict[str, Any] | None:
    """Load and validate the current ticket retry-start record, if present."""

    projection = projection_record if projection_record is not None else _load_current_projection_record()
    return _load_retry_start_record_from_path(
        retry_start_record_path_for_ticket(str(projection["ticket_id"])),
        projection_record=projection,
        recovery_record=recovery_record,
        allow_historical_mismatch=allow_historical_mismatch,
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
    projection = (
        projection_record
        if projection_record is not None
        else _bootstrap_projection_record_for_validation()
    )
    return _load_retry_start_record_from_path(
        path,
        projection_record=projection,
        recovery_record=recovery_record,
        allow_historical_mismatch=allow_historical_mismatch,
    )


def load_current_ticket_governed_autonomy_activation_record(
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate current-ticket 01AH activation status, if present."""

    projection = projection_record if projection_record is not None else _load_current_projection_record()
    path = governed_autonomy_activation_record_path_for_ticket(str(projection["ticket_id"]))
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "governed-autonomy activation record is unreadable"
        ) from exc
    return validate_governed_autonomy_activation_record(
        record,
        projection_record=projection,
    )


def load_current_ticket_governed_autonomy_runtime_state(
    *,
    projection_record: dict[str, Any] | None = None,
    activation_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate current-ticket 01AI operational autonomy state."""

    projection = projection_record if projection_record is not None else _load_current_projection_record()
    activation = activation_record
    if activation is None:
        activation = load_current_ticket_governed_autonomy_activation_record(
            projection_record=projection,
        )
    if activation is None:
        return None
    path = governed_autonomy_runtime_state_path_for_ticket(str(projection["ticket_id"]))
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductRuntimeConflict(
            "governed-autonomy runtime state is unreadable"
        ) from exc
    return validate_governed_autonomy_runtime_state_record(
        record,
        projection_record=projection,
        activation_record=activation,
    )


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


def _governed_ticket_recovery_cycle_id(
    *,
    projection: dict[str, Any],
    latest_failed_run_id: Any,
    observed_attempt_count: Any,
    failure_category: Any = None,
    failure_summary: Any = None,
) -> str:
    ticket_id = str(projection.get("ticket_id") or PEPPER_NEXT_TICKET_ID)
    payload = {
        "project_id": PEPPER_GOVERNED_PROJECT_ID,
        "ticket_id": ticket_id,
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
    algorithm = (
        "pepper-p18-9-0-recovery-cycle-v1"
        if ticket_id == PEPPER_BOOTSTRAP_NEXT_TICKET_ID
        else "pepper-current-ticket-recovery-cycle-v1"
    )
    return hashlib.sha256(f"{algorithm}\n{data}".encode("utf-8")).hexdigest()


def _p18_9_0_recovery_cycle_id(
    *,
    projection: dict[str, Any],
    latest_failed_run_id: Any,
    observed_attempt_count: Any,
    failure_category: Any = None,
    failure_summary: Any = None,
) -> str:
    return _governed_ticket_recovery_cycle_id(
        projection=projection,
        latest_failed_run_id=latest_failed_run_id,
        observed_attempt_count=observed_attempt_count,
        failure_category=failure_category,
        failure_summary=failure_summary,
    )


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


def _governed_autonomy_activation_cycle(record: dict[str, Any]) -> str:
    payload = {
        "project_id": record.get("project_id"),
        "ticket_id": record.get("ticket_id"),
        "projection_SHA256": record.get("projection_SHA256"),
        "work_packet_id": record.get("work_packet_id"),
        "work_packet_SHA256": record.get("work_packet_SHA256"),
        "governed_autonomy_envelope_SHA256": record.get(
            "governed_autonomy_envelope_SHA256"
        ),
        "backend_derived_live_authority_SHA256": record.get(
            "backend_derived_live_authority_SHA256"
        ),
        "capability_gap_SHA256": record.get("capability_gap_SHA256"),
        "continuation_lineage_SHA256": record.get("continuation_lineage_SHA256"),
        "human_request_text": record.get("human_request_text"),
        "authorizer_id": record.get("authorizer_id"),
    }
    return _digest_payload("pepper-governed-autonomy-activation-cycle-v1", payload)


def _governed_autonomy_reference_digest(reference: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in reference.items()
        if key != "envelope_SHA256"
    }
    return _digest_payload(PEPPER_GOVERNED_AUTONOMY_AUTHORITY_DIGEST_ALGORITHM, payload)


def _digest_optional_text(value: object, *, algorithm: str) -> str | None:
    text = str(value or "")
    if not text:
        return None
    return _digest_payload(algorithm, {"text": text})


def _current_work_packet_scope_for_governed_autonomy(
    projection: dict[str, Any],
) -> tuple[tuple[str, ...], tuple[str, ...], str]:
    from hermes_cli.agent_platform.work_packet import WorkPacketCompilationResult
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        load_generation_record,
    )

    generation = load_generation_record(ticket_id=str(projection["ticket_id"]))
    if generation is None:
        raise ProductRuntimeConflict("governed-autonomy authority requires generated WorkPacket")
    try:
        compilation = WorkPacketCompilationResult.model_validate(
            generation["work_packet_compilation_result"]
        )
    except Exception as exc:
        raise ProductRuntimeConflict(
            "governed-autonomy authority WorkPacket compilation is invalid"
        ) from exc
    packet = compilation.work_packet.model_dump(mode="json")
    scope = packet.get("repository_scope") if isinstance(packet, dict) else None
    if not isinstance(scope, dict):
        raise ProductRuntimeConflict("governed-autonomy authority scope is unavailable")
    allowed_paths = tuple(str(item) for item in scope.get("allowed_paths") or ())
    forbidden_paths = tuple(str(item) for item in scope.get("forbidden_paths") or ())
    if not allowed_paths:
        raise ProductRuntimeConflict("governed-autonomy authority has no allowed paths")
    validation_steps_sha = _digest_payload(
        "pepper-governed-autonomy-workpacket-validation-steps-sha256-v1",
        {"validation_steps": packet.get("validation_steps") or []},
    )
    return allowed_paths, forbidden_paths, validation_steps_sha


def _derive_current_governed_autonomy_authority_reference(
    projection: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli.agent_platform.work_packet import (
        GOVERNED_AUTONOMY_POLICY_ID,
        GovernedAutonomyBudget,
    )

    _validate_execution_start_authority(projection)
    allowed_paths, forbidden_paths, validation_steps_sha = (
        _current_work_packet_scope_for_governed_autonomy(projection)
    )
    task_visibility, runs = _governed_autonomy_kanban_visibility(projection)
    if task_visibility is None:
        raise ProductRuntimeConflict("governed-autonomy authority requires projected Kanban task")
    if task_visibility.get("workspace_kind") != "scratch":
        raise ProductRuntimeConflict("governed-autonomy authority requires scratch workspace")
    active_runs = [run for run in runs if _execution_is_active(run)]
    if active_runs or task_visibility.get("current_run_id") is not None:
        raise ProductRuntimeConflict("governed-autonomy authority requires no active execution")
    if not runs:
        raise ProductRuntimeConflict("governed-autonomy authority requires blocked source run evidence")
    latest = runs[-1]
    source_status = str(latest.get("status") or "").strip().lower()
    source_outcome = str(latest.get("outcome") or "").strip().lower()
    if (
        source_status not in _GOVERNED_TICKET_FAILURE_OUTCOMES
        and source_outcome not in _GOVERNED_TICKET_FAILURE_OUTCOMES
    ):
        raise ProductRuntimeConflict(
            "governed-autonomy authority requires failed or blocked source run evidence"
        )
    source_status = source_status or "none"
    source_outcome = source_outcome or "none"
    source_profile = _safe_text(latest.get("profile"), limit=128) or "unknown"
    source_run_snapshot = {
        "source_run_id": latest.get("id"),
        "source_run_status": source_status,
        "source_run_outcome": source_outcome,
        "source_run_profile": source_profile,
        "source_run_ended_at": latest.get("ended_at"),
        "failure_category": _safe_text(latest.get("failure_category"), limit=128),
        "failure_summary_SHA256": _digest_optional_text(
            latest.get("failure_summary") or latest.get("summary") or latest.get("error"),
            algorithm="pepper-governed-autonomy-source-run-failure-summary-sha256-v1",
        ),
    }
    workspace_path_sha = _digest_optional_text(
        task_visibility.get("workspace_path"),
        algorithm="pepper-governed-autonomy-scratch-workspace-path-sha256-v1",
    )
    reference = {
        "authority_kind": "backend_derived_live_authority",
        "authority_lifecycle": "pre_continuation_blocked_run",
        "01AH_envelope_lifecycle_classification": "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE",
        "policy_id": GOVERNED_AUTONOMY_POLICY_ID,
        "envelope_SHA256": "0" * 64,
        "ticket_id": projection["ticket_id"],
        "source_ticket_SHA256": projection["ticket_spec_SHA256"],
        "work_packet_id": projection["work_packet_id"],
        "work_packet_SHA256": projection["work_packet_SHA256"],
        "single_agent_result_SHA256": None,
        "allocation_SHA256": None,
        "profile_SHA256": None,
        "projection_SHA256": projection["projection_SHA256"],
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "allowed_paths_SHA256": _digest_payload(
            "pepper-governed-autonomy-allowed-paths-sha256-v1",
            {"allowed_paths": allowed_paths},
        ),
        "forbidden_paths_SHA256": _digest_payload(
            "pepper-governed-autonomy-forbidden-paths-sha256-v1",
            {"forbidden_paths": forbidden_paths},
        ),
        "validation_steps_SHA256": validation_steps_sha,
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "execution_profile_role": projection["execution_profile_role"],
        "workspace_kind": task_visibility.get("workspace_kind"),
        "workspace_path_SHA256": workspace_path_sha,
        "source_run_id": latest.get("id"),
        "source_run_status": source_status,
        "source_run_outcome": source_outcome,
        "source_run_profile": source_profile,
        "source_run_snapshot_SHA256": _digest_payload(
            "pepper-governed-autonomy-source-run-snapshot-sha256-v1",
            source_run_snapshot,
        ),
        "source_run_count": len(runs),
        "active_execution_count": 0,
        "live_lineage_activation_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "budget": GovernedAutonomyBudget().model_dump(mode="json"),
    }
    reference["envelope_SHA256"] = _governed_autonomy_reference_digest(reference)
    return reference


def _derive_current_governed_autonomy_stable_authority_reference(
    projection: dict[str, Any],
) -> dict[str, Any]:
    from hermes_cli.agent_platform.work_packet import (
        GOVERNED_AUTONOMY_POLICY_ID,
        GovernedAutonomyBudget,
    )

    _validate_execution_start_authority(projection)
    allowed_paths, forbidden_paths, validation_steps_sha = (
        _current_work_packet_scope_for_governed_autonomy(projection)
    )
    return {
        "authority_kind": "backend_derived_live_authority",
        "authority_lifecycle": "pre_continuation_blocked_run",
        "01AH_envelope_lifecycle_classification": "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE",
        "policy_id": GOVERNED_AUTONOMY_POLICY_ID,
        "ticket_id": projection["ticket_id"],
        "source_ticket_SHA256": projection["ticket_spec_SHA256"],
        "work_packet_id": projection["work_packet_id"],
        "work_packet_SHA256": projection["work_packet_SHA256"],
        "single_agent_result_SHA256": None,
        "allocation_SHA256": None,
        "profile_SHA256": None,
        "projection_SHA256": projection["projection_SHA256"],
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "allowed_paths_SHA256": _digest_payload(
            "pepper-governed-autonomy-allowed-paths-sha256-v1",
            {"allowed_paths": allowed_paths},
        ),
        "forbidden_paths_SHA256": _digest_payload(
            "pepper-governed-autonomy-forbidden-paths-sha256-v1",
            {"forbidden_paths": forbidden_paths},
        ),
        "validation_steps_SHA256": validation_steps_sha,
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "execution_profile_role": projection["execution_profile_role"],
        "workspace_kind": projection["workspace_kind"],
        "live_lineage_activation_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "budget": GovernedAutonomyBudget().model_dump(mode="json"),
    }


def _governed_autonomy_stable_authority_reference(
    reference: dict[str, Any],
) -> dict[str, Any]:
    return {
        field: reference.get(field)
        for field in _GOVERNED_AUTONOMY_STABLE_AUTHORITY_FIELDS
    }


def _governed_autonomy_stable_authority_digest(
    reference: dict[str, Any],
) -> str:
    return _digest_payload(
        "pepper-governed-autonomy-stable-authority-sha256-v1",
        _governed_autonomy_stable_authority_reference(reference),
    )


def _governed_autonomy_stable_authority_comparison(
    *,
    projection: dict[str, Any],
    activation_reference: dict[str, Any],
) -> dict[str, Any]:
    current_reference = _derive_current_governed_autonomy_stable_authority_reference(
        projection,
    )
    activation_stable = _governed_autonomy_stable_authority_reference(
        activation_reference,
    )
    mismatches = [
        field
        for field in _GOVERNED_AUTONOMY_STABLE_AUTHORITY_FIELDS
        if activation_stable.get(field) != current_reference.get(field)
    ]
    mismatch_details = [
        _governed_autonomy_authority_field_comparison(
            field=field,
            expected=activation_stable.get(field),
            observed=current_reference.get(field),
            classification="STABLE_AUTHORITY",
        )
        for field in mismatches
    ]
    return {
        "same_authority": not mismatches,
        "mismatches": mismatches,
        "mismatch_details": mismatch_details,
        "activation_stable_authority_SHA256": _governed_autonomy_stable_authority_digest(
            activation_reference,
        ),
        "current_stable_authority_SHA256": _governed_autonomy_stable_authority_digest(
            current_reference,
        ),
        "mutable_authority_fields_ignored": list(
            _GOVERNED_AUTONOMY_MUTABLE_AUTHORITY_FIELDS,
        ),
        "activation_authority_SHA256": activation_reference.get("envelope_SHA256"),
        "activation_source_run_id": activation_reference.get("source_run_id"),
    }


def _governed_autonomy_authority_view_from_reference(
    reference: dict[str, Any],
    *,
    projection: dict[str, Any],
) -> _BackendDerivedGovernedAutonomyAuthority:
    allowed_paths, forbidden_paths, _validation_steps_sha = (
        _current_work_packet_scope_for_governed_autonomy(projection)
    )
    return _BackendDerivedGovernedAutonomyAuthority(
        authority_kind=str(reference["authority_kind"]),
        policy_id=str(reference["policy_id"]),
        envelope_SHA256=str(reference["envelope_SHA256"]),
        ticket_id=str(reference["ticket_id"]),
        source_ticket_SHA256=str(reference["source_ticket_SHA256"]),
        work_packet_id=str(reference["work_packet_id"]),
        work_packet_SHA256=str(reference["work_packet_SHA256"]),
        live_lineage_activation_authorized=False,
        provider_dispatch_count=0,
        model_inference_count=0,
        allowed_paths=allowed_paths,
        forbidden_paths=forbidden_paths,
    )


def _governed_autonomy_owned_direct_run_id(
    previous: dict[str, Any] | None,
) -> int | None:
    if not isinstance(previous, dict):
        return None
    if previous.get("runtime_decision") != "DIRECT":
        return None
    if previous.get("governed_autonomy_continuation_reason") != (
        PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON
    ):
        return None
    if not previous.get("kanban_run_created") or not previous.get("execution_started"):
        return None
    return _int_or_none(previous.get("kanban_run_id"))


def _governed_autonomy_authority_field_comparison(
    *,
    field: str,
    expected: Any,
    observed: Any,
    classification: str,
    matches: bool | None = None,
) -> dict[str, Any]:
    return {
        "field": field,
        "expected": expected,
        "observed": observed,
        "classification": classification,
        "matches": expected == observed if matches is None else matches,
    }


def _governed_autonomy_task_governance_events(
    projection: dict[str, Any],
) -> list[dict[str, Any]]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(projection["kanban_board_slug"]))
    task_id = str(projection["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
        rows = conn.execute(
            "SELECT id, kind, payload, created_at, run_id FROM task_events "
            "WHERE task_id = ? ORDER BY id ASC",
            (task_id,),
        ).fetchall()
    finally:
        conn.close()
    events: list[dict[str, Any]] = []
    for row in rows:
        kind = str(row["kind"] or "")
        if kind not in {"governed_autonomy_continuation_prepared", "claimed"}:
            continue
        try:
            payload = json.loads(row["payload"]) if row["payload"] else None
        except json.JSONDecodeError:
            payload = None
        if not isinstance(payload, dict):
            payload = {}
        events.append({
            "id": int(row["id"]),
            "kind": kind,
            "payload": {
                key: payload.get(key)
                for key in (
                    "source",
                    "reason",
                    "activation_action_SHA256",
                    "backend_derived_live_authority_SHA256",
                    "source_run_id",
                    "run_id",
                )
                if key in payload
            },
            "created_at": row["created_at"],
            "run_id": row["run_id"],
        })
    return events


def _governed_autonomy_event_owned_run_probe(
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    run: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    activation_reference = _validated_governed_autonomy_envelope_reference(
        activation.get("governed_autonomy_envelope_reference")
    )
    run_id = _int_or_none(run.get("id"))
    expected_task_id = str(projection["kanban_task_id"])
    expected_profiles = {
        str(projection["assignee_profile"]),
        str(projection["selected_profile"]),
    }
    comparisons = [
        _governed_autonomy_authority_field_comparison(
            field="kanban_task_id",
            expected=expected_task_id,
            observed=run.get("task_id"),
            classification="STABLE_AUTHORITY",
        ),
        _governed_autonomy_authority_field_comparison(
            field="executor_profile",
            expected=sorted(expected_profiles),
            observed=run.get("profile"),
            classification="STABLE_AUTHORITY",
            matches=str(run.get("profile")) in expected_profiles,
        ),
    ]
    claim_event = None
    if run_id is not None:
        for event in events:
            if event["kind"] != "claimed":
                continue
            payload_run_id = _int_or_none(event.get("payload", {}).get("run_id"))
            event_run_id = _int_or_none(event.get("run_id"))
            if run_id in {payload_run_id, event_run_id}:
                claim_event = event
                break
    comparisons.append(
        _governed_autonomy_authority_field_comparison(
            field="claimed_run_event",
            expected=run_id,
            observed=claim_event.get("id") if claim_event else None,
            classification="RUNTIME_RECORD_STATE",
            matches=claim_event is not None,
        )
    )
    previous_claim_event_id = 0
    preparation_event = None
    if claim_event is not None:
        claim_event_id = int(claim_event["id"])
        previous_claim_event_id = max(
            (
                int(event["id"])
                for event in events
                if event["kind"] == "claimed" and int(event["id"]) < claim_event_id
            ),
            default=0,
        )
        prepared_events = [
            event
            for event in events
            if event["kind"] == "governed_autonomy_continuation_prepared"
            and previous_claim_event_id < int(event["id"]) < claim_event_id
        ]
        preparation_event = prepared_events[-1] if prepared_events else None
    comparisons.append(
        _governed_autonomy_authority_field_comparison(
            field="governed_preparation_event",
            expected="event_between_previous_claim_and_this_claim",
            observed=preparation_event.get("id") if preparation_event else None,
            classification="RUNTIME_RECORD_STATE",
            matches=preparation_event is not None,
        )
    )
    payload = preparation_event.get("payload", {}) if preparation_event else {}
    expected_source_run_id = _int_or_none(activation_reference.get("source_run_id"))
    comparisons.extend([
        _governed_autonomy_authority_field_comparison(
            field="governed_autonomy_event_source",
            expected=PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM,
            observed=payload.get("source"),
            classification="RUNTIME_RECORD_STATE",
        ),
        _governed_autonomy_authority_field_comparison(
            field="governed_autonomy_continuation_reason",
            expected=PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON,
            observed=payload.get("reason"),
            classification="RUNTIME_RECORD_STATE",
        ),
        _governed_autonomy_authority_field_comparison(
            field="activation_action_SHA256",
            expected=activation.get("activation_action_SHA256"),
            observed=payload.get("activation_action_SHA256"),
            classification="STABLE_AUTHORITY",
        ),
        _governed_autonomy_authority_field_comparison(
            field="authority_SHA256",
            expected=activation_reference.get("envelope_SHA256"),
            observed=payload.get("backend_derived_live_authority_SHA256"),
            classification="STABLE_AUTHORITY",
        ),
        _governed_autonomy_authority_field_comparison(
            field="historical_source_run_id",
            expected=expected_source_run_id,
            observed=_int_or_none(payload.get("source_run_id")),
            classification="HISTORICAL_PROVENANCE",
        ),
    ])
    mismatches = [comparison for comparison in comparisons if not comparison["matches"]]
    return {
        "owned": not mismatches,
        "run_id": run_id,
        "proof_kind": "kanban_preparation_event_and_claim_event",
        "claim_event_id": claim_event.get("id") if claim_event else None,
        "previous_claim_event_id": previous_claim_event_id or None,
        "preparation_event_id": preparation_event.get("id") if preparation_event else None,
        "comparisons": comparisons,
        "mismatches": mismatches,
    }


def _governed_autonomy_runtime_record_owned_run_probe(
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    run: dict[str, Any] | None,
) -> dict[str, Any] | None:
    run_id = _governed_autonomy_owned_direct_run_id(previous)
    if run_id is None or previous is None:
        return None
    activation_reference = _validated_governed_autonomy_envelope_reference(
        activation.get("governed_autonomy_envelope_reference")
    )
    expected_profiles = {
        str(projection["assignee_profile"]),
        str(projection["selected_profile"]),
    }
    comparisons = [
        _governed_autonomy_authority_field_comparison(
            field="kanban_run_id",
            expected=run_id,
            observed=_int_or_none(run.get("id")) if isinstance(run, dict) else None,
            classification="RUNTIME_RECORD_STATE",
        ),
        _governed_autonomy_authority_field_comparison(
            field="kanban_task_id",
            expected=projection["kanban_task_id"],
            observed=run.get("task_id") if isinstance(run, dict) else None,
            classification="STABLE_AUTHORITY",
        ),
        _governed_autonomy_authority_field_comparison(
            field="executor_profile",
            expected=sorted(expected_profiles),
            observed=run.get("profile") if isinstance(run, dict) else None,
            classification="STABLE_AUTHORITY",
            matches=(
                isinstance(run, dict)
                and str(run.get("profile")) in expected_profiles
            ),
        ),
        _governed_autonomy_authority_field_comparison(
            field="governed_autonomy_continuation_reason",
            expected=PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON,
            observed=previous.get("governed_autonomy_continuation_reason"),
            classification="RUNTIME_RECORD_STATE",
        ),
        _governed_autonomy_authority_field_comparison(
            field="activation_action_SHA256",
            expected=activation.get("activation_action_SHA256"),
            observed=previous.get("activation_action_SHA256"),
            classification="STABLE_AUTHORITY",
        ),
        _governed_autonomy_authority_field_comparison(
            field="authority_SHA256",
            expected=activation_reference.get("envelope_SHA256"),
            observed=previous.get("governed_autonomy_envelope_SHA256"),
            classification="STABLE_AUTHORITY",
        ),
        _governed_autonomy_authority_field_comparison(
            field="historical_source_run_id",
            expected=_int_or_none(activation_reference.get("source_run_id")),
            observed=_int_or_none(previous.get("source_run_id")),
            classification="HISTORICAL_PROVENANCE",
        ),
    ]
    mismatches = [comparison for comparison in comparisons if not comparison["matches"]]
    return {
        "owned": not mismatches,
        "run_id": run_id,
        "proof_kind": "validated_runtime_record",
        "comparisons": comparisons,
        "mismatches": mismatches,
    }


def _governed_autonomy_owned_lineage_state(
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    task_visibility: dict[str, Any] | None,
    runs: list[dict[str, Any]],
) -> dict[str, Any]:
    owned_proofs_by_run_id: dict[int, dict[str, Any]] = {}
    previous_run_id = _governed_autonomy_owned_direct_run_id(previous)
    if previous_run_id is not None:
        previous_run = next(
            (run for run in runs if _int_or_none(run.get("id")) == previous_run_id),
            None,
        )
        previous_probe = _governed_autonomy_runtime_record_owned_run_probe(
            projection=projection,
            activation=activation,
            previous=previous,
            run=previous_run,
        )
        if previous_probe is not None and previous_probe["owned"]:
            owned_proofs_by_run_id[previous_run_id] = previous_probe
    event_probes: list[dict[str, Any]] = []
    events = _governed_autonomy_task_governance_events(projection)
    for run in runs:
        probe = _governed_autonomy_event_owned_run_probe(
            projection=projection,
            activation=activation,
            run=run,
            events=events,
        )
        event_probes.append(probe)
        run_id = _int_or_none(run.get("id"))
        if run_id is not None and probe["owned"]:
            owned_proofs_by_run_id[run_id] = probe
    owned_run_ids = sorted(owned_proofs_by_run_id)
    latest_run = runs[-1] if runs else None
    latest_run_id = (
        _int_or_none(latest_run.get("id"))
        if isinstance(latest_run, dict)
        else None
    )
    latest_probe = next(
        (probe for probe in event_probes if probe.get("run_id") == latest_run_id),
        None,
    )
    task_current_run_id = (
        _int_or_none(task_visibility.get("current_run_id"))
        if isinstance(task_visibility, dict)
        else None
    )
    owned_active_run_ids = [
        run_id
        for run_id in owned_run_ids
        for run in runs
        if _int_or_none(run.get("id")) == run_id and _execution_is_active(run)
    ]
    return {
        "owned_governed_run_id": owned_run_ids[-1] if owned_run_ids else None,
        "owned_governed_run_ids": owned_run_ids,
        "owned_active_run_ids": owned_active_run_ids,
        "previous_runtime_owned_run_id": previous_run_id,
        "latest_run_id": latest_run_id,
        "task_current_run_id": task_current_run_id,
        "latest_run_ownership_probe": latest_probe,
        "ownership_proofs": list(owned_proofs_by_run_id.values()),
    }


def _governed_autonomy_lineage_mismatch(
    *,
    activation_reference: dict[str, Any],
    task_visibility: dict[str, Any] | None,
    runs: list[dict[str, Any]],
    owned_lineage_state: dict[str, Any],
) -> dict[str, Any] | None:
    active_runs = [run for run in runs if _execution_is_active(run)]
    owned_run_ids = {
        int(run_id)
        for run_id in owned_lineage_state.get("owned_governed_run_ids", [])
        if _int_or_none(run_id) is not None
    }
    owned_run_id = _int_or_none(owned_lineage_state.get("owned_governed_run_id"))
    activation_source_run_id = _int_or_none(activation_reference.get("source_run_id"))
    latest_run = runs[-1] if runs else None
    latest_run_id = (
        _int_or_none(latest_run.get("id"))
        if isinstance(latest_run, dict)
        else None
    )
    task_current_run_id = (
        _int_or_none(task_visibility.get("current_run_id"))
        if isinstance(task_visibility, dict)
        else None
    )
    base = {
        "activation_source_run_id": activation_source_run_id,
        "owned_governed_run_id": owned_run_id,
        "owned_governed_run_ids": sorted(owned_run_ids),
        "current_source_run_id": latest_run_id,
        "current_active_run_ids": [run.get("id") for run in active_runs],
        "task_current_run_id": task_current_run_id,
        "latest_run_ownership_probe": owned_lineage_state.get(
            "latest_run_ownership_probe"
        ),
    }
    if active_runs:
        active_run_ids = {_int_or_none(run.get("id")) for run in active_runs}
        if active_run_ids and active_run_ids.issubset(owned_run_ids):
            return None
        return {
            **base,
            "reason": "unowned_active_execution_present",
            "blocker_detail": (
                "an active Kanban run is not owned by this governed-autonomy runtime"
            ),
        }
    if task_current_run_id is not None and task_current_run_id not in owned_run_ids:
        return {
            **base,
            "reason": "unowned_task_current_run_present",
            "blocker_detail": "projected Kanban task has an unowned current run",
        }
    if (
        latest_run_id is not None
        and activation_source_run_id is not None
        and latest_run_id > activation_source_run_id
        and latest_run_id not in owned_run_ids
    ):
        return {
            **base,
            "reason": "newer_unowned_source_run",
            "current_source_run_status": (
                latest_run.get("status") if isinstance(latest_run, dict) else None
            ),
            "current_source_run_outcome": (
                latest_run.get("outcome") if isinstance(latest_run, dict) else None
            ),
            "blocker_detail": (
                "latest Kanban run is newer than the activation source and is not "
                "owned by this governed-autonomy runtime"
            ),
        }
    return None


def _resolve_effective_current_governed_autonomy_authority(
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None = None,
) -> dict[str, Any]:
    activation_reference = _validated_governed_autonomy_envelope_reference(
        activation.get("governed_autonomy_envelope_reference")
    )
    stable_comparison = _governed_autonomy_stable_authority_comparison(
        projection=projection,
        activation_reference=activation_reference,
    )
    task_visibility, runs = _governed_autonomy_kanban_visibility(projection)
    owned_lineage_state = _governed_autonomy_owned_lineage_state(
        projection=projection,
        activation=activation,
        previous=previous,
        task_visibility=task_visibility,
        runs=runs,
    )
    lineage_mismatch = _governed_autonomy_lineage_mismatch(
        activation_reference=activation_reference,
        task_visibility=task_visibility,
        runs=runs,
        owned_lineage_state=owned_lineage_state,
    )
    diagnostics = {
        "blocker_code": "CONTINUATION_AUTHORITY_MISMATCH",
        "reason": None,
        "activation_authority_SHA256": activation_reference.get("envelope_SHA256"),
        "activation_source_run_id": activation_reference.get("source_run_id"),
        "activation_source_run_status": activation_reference.get("source_run_status"),
        "activation_stable_authority_SHA256": stable_comparison[
            "activation_stable_authority_SHA256"
        ],
        "current_stable_authority_SHA256": stable_comparison[
            "current_stable_authority_SHA256"
        ],
        "stable_authority_mismatches": stable_comparison["mismatches"],
        "stable_authority_mismatch_details": stable_comparison.get(
            "mismatch_details",
            [],
        ),
        "mutable_authority_fields_ignored": stable_comparison[
            "mutable_authority_fields_ignored"
        ],
        "owned_lineage_state": owned_lineage_state,
    }
    if not stable_comparison["same_authority"]:
        diagnostics["reason"] = "stable_authority_fields_changed"
    elif lineage_mismatch is not None:
        diagnostics.update(lineage_mismatch)
    return {
        "activation": activation,
        "activation_reference": activation_reference,
        "activation_origin": _governed_autonomy_activation_effective_projection(activation),
        "stable_authority": stable_comparison,
        "current_execution_state": {
            "task": task_visibility,
            "runs": runs,
            "active_execution_count": len(
                [run for run in runs if _execution_is_active(run)]
            ),
            "latest_run_id": owned_lineage_state.get("latest_run_id"),
            "task_current_run_id": owned_lineage_state.get("task_current_run_id"),
        },
        "owned_lineage_state": owned_lineage_state,
        "authority_revalidated": (
            stable_comparison["same_authority"] and lineage_mismatch is None
        ),
        "continuation_eligible": (
            stable_comparison["same_authority"] and lineage_mismatch is None
        ),
        "diagnostics": diagnostics,
    }


def _require_current_governed_autonomy_authority_match(
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None = None,
    effective_authority: dict[str, Any] | None = None,
) -> _BackendDerivedGovernedAutonomyAuthority:
    if effective_authority is None:
        effective_authority = _resolve_effective_current_governed_autonomy_authority(
            projection=projection,
            activation=activation,
            previous=previous,
        )
    activation_reference = effective_authority["activation_reference"]
    if not effective_authority["authority_revalidated"]:
        stable_comparison = effective_authority["stable_authority"]
        diagnostics = dict(effective_authority["diagnostics"])
        current_reference = None
        try:
            current_reference = _derive_current_governed_autonomy_authority_reference(
                projection,
            )
        except Exception:
            current_reference = None
        diagnostics.update({
            "current_authority_SHA256": (
                current_reference.get("envelope_SHA256")
                if isinstance(current_reference, dict)
                else None
            ),
            "activation_source_run_id": activation_reference.get("source_run_id"),
            "current_source_run_id": (
                current_reference.get("source_run_id")
                if isinstance(current_reference, dict)
                else effective_authority["current_execution_state"].get("latest_run_id")
            ),
            "activation_source_run_status": activation_reference.get("source_run_status"),
            "current_source_run_status": (
                current_reference.get("source_run_status")
                if isinstance(current_reference, dict)
                else None
            ),
        })
        raise ProductRuntimeAuthorityMismatch(
            "CONTINUATION_AUTHORITY_MISMATCH",
            diagnostics=diagnostics,
        )
    return _governed_autonomy_authority_view_from_reference(
        activation_reference,
        projection=projection,
    )


def _validated_governed_autonomy_budget_reference(value: object) -> dict[str, int]:
    from hermes_cli.agent_platform.work_packet import GovernedAutonomyBudget

    try:
        budget = GovernedAutonomyBudget.model_validate(value)
    except Exception as exc:
        raise ProductRuntimeConflict("governed-autonomy budget reference is invalid") from exc
    return budget.model_dump(mode="json")


def _validated_governed_autonomy_envelope_reference(value: object) -> dict[str, Any]:
    from hermes_cli.agent_platform.work_packet import GOVERNED_AUTONOMY_POLICY_ID

    required_keys = {
        "authority_kind",
        "authority_lifecycle",
        "01AH_envelope_lifecycle_classification",
        "policy_id",
        "envelope_SHA256",
        "ticket_id",
        "source_ticket_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
        "single_agent_result_SHA256",
        "allocation_SHA256",
        "profile_SHA256",
        "projection_SHA256",
        "approval_publication_SHA256",
        "dependency_plan_SHA256",
        "allowed_paths_SHA256",
        "forbidden_paths_SHA256",
        "validation_steps_SHA256",
        "kanban_board_slug",
        "kanban_task_id",
        "assignee_profile",
        "selected_profile",
        "execution_profile_role",
        "workspace_kind",
        "workspace_path_SHA256",
        "source_run_id",
        "source_run_status",
        "source_run_outcome",
        "source_run_profile",
        "source_run_snapshot_SHA256",
        "source_run_count",
        "active_execution_count",
        "live_lineage_activation_authorized",
        "provider_dispatch_count",
        "model_inference_count",
        "budget",
    }
    if not isinstance(value, dict):
        raise ProductRuntimeConflict("governed-autonomy envelope reference must be an object")
    keys = set(value)
    if keys != required_keys:
        raise ProductRuntimeConflict("governed-autonomy envelope reference field mismatch")
    if value["authority_kind"] != "backend_derived_live_authority":
        raise ProductRuntimeConflict("governed-autonomy authority kind mismatch")
    if value["authority_lifecycle"] != "pre_continuation_blocked_run":
        raise ProductRuntimeConflict("governed-autonomy authority lifecycle mismatch")
    if value["01AH_envelope_lifecycle_classification"] != "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE":
        raise ProductRuntimeConflict("governed-autonomy 01AH lifecycle classification mismatch")
    if value["envelope_SHA256"] != _governed_autonomy_reference_digest(value):
        raise ProductRuntimeConflict("governed-autonomy authority reference digest mismatch")
    digest_fields = {
        "envelope_SHA256",
        "source_ticket_SHA256",
        "work_packet_SHA256",
        "projection_SHA256",
        "approval_publication_SHA256",
        "dependency_plan_SHA256",
        "allowed_paths_SHA256",
        "forbidden_paths_SHA256",
        "validation_steps_SHA256",
        "source_run_snapshot_SHA256",
    }
    nullable_digest_fields = {
        "single_agent_result_SHA256",
        "allocation_SHA256",
        "profile_SHA256",
        "workspace_path_SHA256",
    }
    identifier_fields = {
        "ticket_id",
        "work_packet_id",
        "kanban_board_slug",
        "kanban_task_id",
        "assignee_profile",
        "selected_profile",
        "execution_profile_role",
        "workspace_kind",
        "source_run_status",
        "source_run_outcome",
        "source_run_profile",
    }
    if value["policy_id"] != GOVERNED_AUTONOMY_POLICY_ID:
        raise ProductRuntimeConflict("governed-autonomy envelope policy mismatch")
    for field in digest_fields:
        if not isinstance(value[field], str) or not _SAFE_SHA256.fullmatch(value[field]):
            raise ProductRuntimeConflict(
                f"governed-autonomy envelope reference {field} is invalid"
            )
    for field in nullable_digest_fields:
        if value[field] is not None and (
            not isinstance(value[field], str) or not _SAFE_SHA256.fullmatch(value[field])
        ):
            raise ProductRuntimeConflict(
                f"governed-autonomy envelope reference {field} is invalid"
            )
    for field in identifier_fields:
        if (
            not isinstance(value[field], str)
            or not _SAFE_GOVERNED_AUTONOMY_REF_ID.fullmatch(value[field])
        ):
            raise ProductRuntimeConflict(
                f"governed-autonomy envelope reference {field} is invalid"
            )
    if value["live_lineage_activation_authorized"] is not False:
        raise ProductRuntimeConflict(
            "governed-autonomy envelope reference live lineage authority mismatch"
        )
    if value["provider_dispatch_count"] != 0 or value["model_inference_count"] != 0:
        raise ProductRuntimeConflict(
            "governed-autonomy envelope reference dispatch count mismatch"
        )
    for field in ("source_run_id", "source_run_count", "active_execution_count"):
        if not isinstance(value[field], int) or isinstance(value[field], bool) or value[field] < 0:
            raise ProductRuntimeConflict(
                f"governed-autonomy envelope reference {field} is invalid"
            )
    if value["single_agent_result_SHA256"] is not None:
        raise ProductRuntimeConflict(
            "backend-derived governed-autonomy authority must not claim completed single-agent evidence"
        )
    if value["allocation_SHA256"] is not None or value["profile_SHA256"] is not None:
        raise ProductRuntimeConflict(
            "backend-derived governed-autonomy authority must not claim P17 envelope allocation/profile digests"
        )
    _validated_governed_autonomy_budget_reference(value["budget"])
    return dict(value)


def _validated_governed_autonomy_gap_reference(value: object) -> dict[str, Any]:
    from hermes_cli.agent_platform.work_packet import (
        CapabilityGapDisposition,
        CapabilityGapKind,
    )

    required_keys = {
        "gap_id",
        "gap_SHA256",
        "envelope_SHA256",
        "kind",
        "disposition",
        "requires_human_authority",
    }
    if not isinstance(value, dict):
        raise ProductRuntimeConflict("governed-autonomy capability gap reference must be an object")
    keys = set(value)
    if keys != required_keys:
        raise ProductRuntimeConflict("governed-autonomy capability gap reference field mismatch")
    if (
        not isinstance(value["gap_id"], str)
        or not _SAFE_GOVERNED_AUTONOMY_REF_ID.fullmatch(value["gap_id"])
    ):
        raise ProductRuntimeConflict("governed-autonomy capability gap reference ID is invalid")
    for field in ("gap_SHA256", "envelope_SHA256"):
        if not isinstance(value[field], str) or not _SAFE_SHA256.fullmatch(value[field]):
            raise ProductRuntimeConflict(
                f"governed-autonomy capability gap reference {field} is invalid"
            )
    if value["kind"] not in {item.value for item in CapabilityGapKind}:
        raise ProductRuntimeConflict("governed-autonomy capability gap reference kind is invalid")
    if value["disposition"] not in {item.value for item in CapabilityGapDisposition}:
        raise ProductRuntimeConflict(
            "governed-autonomy capability gap reference disposition is invalid"
        )
    if not isinstance(value["requires_human_authority"], bool):
        raise ProductRuntimeConflict(
            "governed-autonomy capability gap reference authority flag is invalid"
        )
    if value["disposition"] == CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED.value:
        if value["requires_human_authority"] is not True:
            raise ProductRuntimeConflict(
                "governed-autonomy capability gap reference authority mismatch"
            )
    elif value["requires_human_authority"] is not False:
        raise ProductRuntimeConflict(
            "governed-autonomy capability gap reference authority mismatch"
        )
    return dict(value)


def _validated_governed_autonomy_lineage_reference(value: object) -> dict[str, Any]:
    from hermes_cli.agent_platform.work_packet import AutonomyContinuationState

    required_keys = {
        "lineage_id",
        "lineage_SHA256",
        "envelope_SHA256",
        "gap_SHA256",
        "state",
        "continuation_index",
    }
    if not isinstance(value, dict):
        raise ProductRuntimeConflict(
            "governed-autonomy continuation lineage reference must be an object"
        )
    keys = set(value)
    if keys != required_keys:
        raise ProductRuntimeConflict(
            "governed-autonomy continuation lineage reference field mismatch"
        )
    if (
        not isinstance(value["lineage_id"], str)
        or not _SAFE_GOVERNED_AUTONOMY_REF_ID.fullmatch(value["lineage_id"])
    ):
        raise ProductRuntimeConflict(
            "governed-autonomy continuation lineage reference ID is invalid"
        )
    for field in ("lineage_SHA256", "envelope_SHA256", "gap_SHA256"):
        if not isinstance(value[field], str) or not _SAFE_SHA256.fullmatch(value[field]):
            raise ProductRuntimeConflict(
                f"governed-autonomy continuation lineage reference {field} is invalid"
            )
    if value["state"] not in {item.value for item in AutonomyContinuationState}:
        raise ProductRuntimeConflict(
            "governed-autonomy continuation lineage reference state is invalid"
        )
    if not isinstance(value["continuation_index"], int) or value["continuation_index"] < 0:
        raise ProductRuntimeConflict(
            "governed-autonomy continuation lineage reference index is invalid"
        )
    return dict(value)


def _governed_autonomy_same_authority_subset(
    projection: dict[str, Any],
    envelope: Any,
) -> dict[str, Any]:
    def field(name: str) -> Any:
        if isinstance(envelope, dict):
            return envelope.get(name)
        return getattr(envelope, name)

    comparisons = {
        "ticket_id": {
            "projection": projection.get("ticket_id"),
            "envelope": field("ticket_id"),
            "matches": projection.get("ticket_id") == field("ticket_id"),
        },
        "ticket_spec_SHA256": {
            "projection": projection.get("ticket_spec_SHA256"),
            "envelope_source_ticket_SHA256": field("source_ticket_SHA256"),
            "matches": projection.get("ticket_spec_SHA256") == field("source_ticket_SHA256"),
        },
        "work_packet_id": {
            "projection": projection.get("work_packet_id"),
            "envelope": field("work_packet_id"),
            "matches": projection.get("work_packet_id") == field("work_packet_id"),
        },
        "work_packet_SHA256": {
            "projection": projection.get("work_packet_SHA256"),
            "envelope": field("work_packet_SHA256"),
            "matches": projection.get("work_packet_SHA256") == field("work_packet_SHA256"),
        },
        "live_lineage_activation_authorized": {
            "projection": False,
            "envelope": field("live_lineage_activation_authorized"),
            "matches": field("live_lineage_activation_authorized") is False,
        },
        "provider_dispatch_count": {
            "projection": 0,
            "envelope": field("provider_dispatch_count"),
            "matches": field("provider_dispatch_count") == 0,
        },
        "model_inference_count": {
            "projection": 0,
            "envelope": field("model_inference_count"),
            "matches": field("model_inference_count") == 0,
        },
    }
    mismatches = [key for key, item in comparisons.items() if not item["matches"]]
    return {
        "policy_id": PEPPER_GOVERNED_AUTONOMY_A2A_POLICY_ID,
        "same_authority": not mismatches,
        "mismatches": mismatches,
        "comparisons": comparisons,
    }


def _governed_autonomy_activation_has_legacy_runtime_limit(record: dict[str, Any]) -> bool:
    return (
        record.get("live_lineage_activation_authorized") is False
        and record.get("live_lineage_activation_status") == "blocked_requires_separate_authority"
        and record.get("live_lineage_activation_blocker_code") == "LIVE_LINEAGE_ACTIVATION_AUTHORITY_GAP"
        and record.get("same_authority_delegation_status") == "blocked_metadata_only"
        and record.get("same_authority_delegation_authorized") is False
        and record.get("same_authority_delegation_blocker_code")
        == "A2A_RUNTIME_UNAVAILABLE_WITHOUT_TASK_LOCAL_AUTHORITY"
        and record.get("opencode_runtime_dispatcher_found") is False
        and record.get("delegate_task_runtime_kind") == "local_subagent_not_opencode_a2a"
    )


def _raise_governed_autonomy_continuation_authority_mismatch(
    *,
    record: dict[str, Any],
    current_reference: dict[str, Any] | None,
    reason: str,
    detail: Any | None = None,
) -> None:
    activation_reference = record.get("governed_autonomy_envelope_reference")
    if not isinstance(activation_reference, dict):
        activation_reference = {}
    diagnostics = {
        "blocker_code": "CONTINUATION_AUTHORITY_MISMATCH",
        "reason": reason,
        "detail": detail,
        "activation_action_SHA256": record.get("activation_action_SHA256"),
        "activation_authority_SHA256": activation_reference.get("envelope_SHA256"),
        "current_authority_SHA256": (
            current_reference.get("envelope_SHA256")
            if isinstance(current_reference, dict)
            else None
        ),
        "activation_ticket_id": record.get("ticket_id"),
        "current_ticket_id": (
            current_reference.get("ticket_id")
            if isinstance(current_reference, dict)
            else None
        ),
        "activation_work_packet_id": record.get("work_packet_id"),
        "current_work_packet_id": (
            current_reference.get("work_packet_id")
            if isinstance(current_reference, dict)
            else None
        ),
        "activation_work_packet_SHA256": record.get("work_packet_SHA256"),
        "current_work_packet_SHA256": (
            current_reference.get("work_packet_SHA256")
            if isinstance(current_reference, dict)
            else None
        ),
        "activation_projection_SHA256": record.get("projection_SHA256"),
        "current_projection_SHA256": (
            current_reference.get("projection_SHA256")
            if isinstance(current_reference, dict)
            else None
        ),
    }
    raise ProductRuntimeAuthorityMismatch(
        "CONTINUATION_AUTHORITY_MISMATCH",
        diagnostics=diagnostics,
    )


def _validate_governed_autonomy_legacy_activation_compatibility(
    *,
    record: dict[str, Any],
    projection: dict[str, Any],
    expected: dict[str, Any],
    envelope_reference: dict[str, Any],
    same_authority: dict[str, Any],
    gap: dict[str, Any] | None,
    lineage: dict[str, Any] | None,
) -> None:
    if not _governed_autonomy_activation_has_legacy_runtime_limit(record):
        raise ProductRuntimeConflict("governed-autonomy activation record is not legacy-compatible")
    try:
        request = CurrentTicketGovernedAutonomyActivationRequest(
            human_request_text=str(record.get("human_request_text") or ""),
            authorizer_id=str(record.get("authorizer_id") or ""),
            project_id=str(record.get("project_id") or "") or None,
            ticket_id=str(record.get("ticket_id") or "") or None,
            next_action_id=str(record.get("current_next_action_id") or "") or None,
        )
        _validate_governed_autonomy_activation_request_text(
            request.human_request_text,
            ticket_id=str(projection["ticket_id"]),
        )
    except Exception as exc:
        raise ProductRuntimeConflict(
            "legacy governed-autonomy activation human authorization is invalid"
        ) from exc

    compatibility_expected = dict(expected)
    compatibility_expected.update({
        "same_authority_delegation_status": "blocked_metadata_only",
        "same_authority_delegation_authorized": False,
        "same_authority_delegation_blocker_code": "A2A_RUNTIME_UNAVAILABLE_WITHOUT_TASK_LOCAL_AUTHORITY",
        "same_authority_delegation_blocker_detail": (
            "No canonical OpenCode/A2A dispatcher is available; task-local delegation requires "
            "a separate 01AH-scoped authority that still cannot activate live lineage."
        ),
        "opencode_runtime_dispatcher_found": False,
        "delegate_task_runtime_kind": "local_subagent_not_opencode_a2a",
        "live_lineage_activation_authorized": False,
        "live_lineage_activation_status": "blocked_requires_separate_authority",
        "live_lineage_activation_blocker_code": "LIVE_LINEAGE_ACTIVATION_AUTHORITY_GAP",
        "live_lineage_activation_blocker_detail": (
            f"{projection['ticket_id']} live lineage activation, retry execution, and run creation "
            "require separate human/runtime authority."
        ),
        "human_smoke_marker": PEPPER_LEGACY_GOVERNED_AUTONOMY_READY_MARKER,
    })
    for key, value in compatibility_expected.items():
        if record.get(key) != value:
            _raise_governed_autonomy_continuation_authority_mismatch(
                record=record,
                current_reference=None,
                reason="legacy_activation_field_mismatch",
                detail={"field": key},
            )
    if record.get("requested_action") != "record_governed_autonomy_activation_status":
        raise ProductRuntimeConflict("legacy governed-autonomy activation action is invalid")
    if record.get("same_authority_subset") != same_authority:
        _raise_governed_autonomy_continuation_authority_mismatch(
            record=record,
            current_reference=None,
            reason="legacy_activation_same_authority_subset_mismatch",
        )
    expected_gap_sha = gap["gap_SHA256"] if gap is not None else None
    if record.get("capability_gap_SHA256") != expected_gap_sha or record.get("capability_gap_reference") != gap:
        _raise_governed_autonomy_continuation_authority_mismatch(
            record=record,
            current_reference=None,
            reason="legacy_activation_capability_gap_mismatch",
        )
    expected_lineage_sha = lineage["lineage_SHA256"] if lineage is not None else None
    if (
        record.get("continuation_lineage_SHA256") != expected_lineage_sha
        or record.get("continuation_lineage_reference") != lineage
    ):
        _raise_governed_autonomy_continuation_authority_mismatch(
            record=record,
            current_reference=None,
            reason="legacy_activation_continuation_lineage_mismatch",
        )
    try:
        stable_comparison = _governed_autonomy_stable_authority_comparison(
            projection=projection,
            activation_reference=envelope_reference,
        )
    except Exception as exc:
        _raise_governed_autonomy_continuation_authority_mismatch(
            record=record,
            current_reference=None,
            reason="current_backend_stable_authority_unavailable",
            detail=_safe_text(exc, limit=300),
        )
    if not stable_comparison["same_authority"]:
        _raise_governed_autonomy_continuation_authority_mismatch(
            record=record,
            current_reference={
                "ticket_id": projection.get("ticket_id"),
                "work_packet_id": projection.get("work_packet_id"),
                "work_packet_SHA256": projection.get("work_packet_SHA256"),
                "projection_SHA256": projection.get("projection_SHA256"),
                "envelope_SHA256": stable_comparison.get(
                    "current_stable_authority_SHA256"
                ),
            },
            reason="current_backend_stable_authority_changed",
            detail=stable_comparison,
        )


def _governed_autonomy_activation_effective_projection(record: dict[str, Any]) -> dict[str, Any]:
    if _governed_autonomy_activation_has_legacy_runtime_limit(record):
        return {
            "governed_autonomy_activation_origin": "legacy_compatible_human_activation",
            "legacy_activation_compatibility_applied": True,
            "historical_activation_record_preserved": True,
            "historical_runtime_limitation_classification": "LEGACY_ACTIVATION_RUNTIME_CAPABILITY_LIMITATION",
            "effective_live_lineage_activation_authorized": True,
            "additional_human_activation_required": False,
            "authority_revalidated": True,
            "same_authority_delegation_status": "canonical_hermes_delegate_task_available_with_parent_agent",
            "same_authority_delegation_authorized": True,
            "same_authority_delegation_blocker_code": None,
            "same_authority_delegation_blocker_detail": (
                "Canonical Hermes delegate_task can run a bounded same-authority child when "
                "the tool invocation provides parent_agent context; otherwise continuation stops."
            ),
            "opencode_runtime_dispatcher_found": True,
            "delegate_task_runtime_kind": "canonical_hermes_delegate_task",
            "live_lineage_activation_authorized": True,
            "live_lineage_activation_status": "active_authority_ready_for_continuation",
            "live_lineage_activation_blocker_code": None,
            "live_lineage_activation_blocker_detail": (
                "Legacy human activation is preserved; current backend-derived authority has "
                "been revalidated without expanding scope."
            ),
            "historical_live_lineage_activation_authorized": record.get("live_lineage_activation_authorized"),
            "historical_live_lineage_activation_status": record.get("live_lineage_activation_status"),
            "historical_live_lineage_activation_blocker_code": record.get(
                "live_lineage_activation_blocker_code"
            ),
        }
    return {
        "governed_autonomy_activation_origin": "current_human_activation",
        "legacy_activation_compatibility_applied": False,
        "historical_activation_record_preserved": False,
        "historical_runtime_limitation_classification": None,
        "effective_live_lineage_activation_authorized": bool(
            record.get("live_lineage_activation_authorized")
        ),
        "additional_human_activation_required": False,
        "authority_revalidated": True,
        "same_authority_delegation_status": record.get("same_authority_delegation_status"),
        "same_authority_delegation_authorized": record.get("same_authority_delegation_authorized"),
        "same_authority_delegation_blocker_code": record.get("same_authority_delegation_blocker_code"),
        "same_authority_delegation_blocker_detail": record.get("same_authority_delegation_blocker_detail"),
        "opencode_runtime_dispatcher_found": record.get("opencode_runtime_dispatcher_found"),
        "delegate_task_runtime_kind": record.get("delegate_task_runtime_kind"),
        "live_lineage_activation_authorized": record.get("live_lineage_activation_authorized"),
        "live_lineage_activation_status": record.get("live_lineage_activation_status"),
        "live_lineage_activation_blocker_code": record.get("live_lineage_activation_blocker_code"),
        "live_lineage_activation_blocker_detail": record.get("live_lineage_activation_blocker_detail"),
        "historical_live_lineage_activation_authorized": record.get("live_lineage_activation_authorized"),
        "historical_live_lineage_activation_status": record.get("live_lineage_activation_status"),
        "historical_live_lineage_activation_blocker_code": record.get(
            "live_lineage_activation_blocker_code"
        ),
    }


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
    binding, identity = _current_ticket_identity_fields(projection)
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
    authorization_diagnostics = execution_recovery_authorization_text_diagnostics(
        str(record.get("human_authorization_text") or ""),
        current_ticket_id=binding.ticket_id,
        requested_ticket_id=record.get("ticket_id"),
        current_next_action_id=binding.execution_recovery_next_action_id,
        requested_next_action_id=binding.execution_recovery_next_action_id,
    )
    if authorization_diagnostics is not None:
        raise ProductRuntimeConflict(
            "recovery action human authorization text mismatch: "
            f"{authorization_diagnostics['blocker_detail']}"
        )
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
        recovery = load_current_ticket_recovery_action_record(projection_record=projection)
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


def validate_governed_autonomy_activation_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate persisted dispatch-free 01AH activation status."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("governed-autonomy activation record must be an object")
    if record.get("activation_action_SHA256") != _governed_autonomy_activation_record_digest(record):
        raise ProductRuntimeConflict("governed-autonomy activation record digest mismatch")
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    _binding, identity = _current_ticket_identity_fields(projection)
    try:
        envelope_reference = _validated_governed_autonomy_envelope_reference(
            record.get("governed_autonomy_envelope_reference")
        )
    except Exception as exc:
        if _governed_autonomy_activation_has_legacy_runtime_limit(record):
            _raise_governed_autonomy_continuation_authority_mismatch(
                record=record,
                current_reference=None,
                reason="legacy_activation_envelope_reference_invalid",
                detail=_safe_text(exc, limit=300),
            )
        raise
    budget_reference = _validated_governed_autonomy_budget_reference(
        record.get("governed_autonomy_budget")
    )
    if envelope_reference.get("budget") != budget_reference:
        raise ProductRuntimeConflict("governed-autonomy authority budget mismatch")
    same_authority = _governed_autonomy_same_authority_subset(
        projection,
        envelope_reference,
    )
    if not same_authority["same_authority"]:
        if _governed_autonomy_activation_has_legacy_runtime_limit(record):
            _raise_governed_autonomy_continuation_authority_mismatch(
                record=record,
                current_reference=None,
                reason="legacy_activation_same_authority_subset_mismatch",
                detail=same_authority,
            )
        raise ProductRuntimeAuthorityMismatch(
            "governed-autonomy envelope authority mismatch",
            diagnostics=same_authority,
        )
    if record.get("governed_autonomy_envelope") is not None:
        raise ProductRuntimeConflict("governed-autonomy activation record must store envelope reference only")
    if record.get("capability_gap") is not None:
        raise ProductRuntimeConflict("governed-autonomy activation record must store gap reference only")
    if record.get("continuation_lineage") is not None:
        raise ProductRuntimeConflict("governed-autonomy activation record must store lineage reference only")
    if record.get("backend_derived_live_authority_reference") != envelope_reference:
        if _governed_autonomy_activation_has_legacy_runtime_limit(record):
            _raise_governed_autonomy_continuation_authority_mismatch(
                record=record,
                current_reference=None,
                reason="legacy_activation_backend_authority_reference_mismatch",
            )
        raise ProductRuntimeConflict("governed-autonomy backend authority reference mismatch")
    gap_payload = record.get("capability_gap_reference")
    gap = _validated_governed_autonomy_gap_reference(gap_payload) if gap_payload is not None else None
    if gap is not None and gap["envelope_SHA256"] != envelope_reference["envelope_SHA256"]:
        raise ProductRuntimeConflict("governed-autonomy gap envelope digest mismatch")
    lineage_payload = record.get("continuation_lineage_reference")
    lineage = (
        _validated_governed_autonomy_lineage_reference(lineage_payload)
        if lineage_payload is not None
        else None
    )
    if lineage is not None:
        if lineage["envelope_SHA256"] != envelope_reference["envelope_SHA256"]:
            raise ProductRuntimeConflict("governed-autonomy lineage envelope digest mismatch")
        if gap is not None and lineage["gap_SHA256"] != gap["gap_SHA256"]:
            raise ProductRuntimeConflict("governed-autonomy lineage gap digest mismatch")
    expected = {
        "schema_version": PEPPER_GOVERNED_AUTONOMY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_ACTION_POLICY_ID,
        "source_system": PEPPER_GOVERNED_AUTONOMY_ACTION_SOURCE_SYSTEM,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "governed_autonomy_policy_id": envelope_reference["policy_id"],
        "governed_autonomy_envelope_SHA256": envelope_reference["envelope_SHA256"],
        "governed_autonomy_budget": budget_reference,
        "backend_derived_live_authority_SHA256": envelope_reference["envelope_SHA256"],
        "authority_derivation_source": "server_side_current_ticket_projection_and_kanban_run",
        "01AH_envelope_lifecycle_classification": "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE",
        "governed_autonomy_activation_recorded": True,
        "governed_autonomy_status": "activation_recorded_live_lineage_blocked",
        "live_lineage_activation_authorized": True,
        "live_lineage_activation_status": "active_authority_ready_for_continuation",
        "live_lineage_activation_blocker_code": None,
        "same_authority_subset_validated": True,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "lineage_dispatch_performed": False,
        "A2A_dispatch_performed": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": PEPPER_GOVERNED_AUTONOMY_READY_MARKER,
    }
    expected_gap_sha = gap["gap_SHA256"] if gap is not None else None
    expected_lineage_sha = lineage["lineage_SHA256"] if lineage is not None else None
    mismatched_fields = [key for key, value in expected.items() if record.get(key) != value]
    legacy_candidate = bool(mismatched_fields) and _governed_autonomy_activation_has_legacy_runtime_limit(record)
    if legacy_candidate:
        _validate_governed_autonomy_legacy_activation_compatibility(
            record=record,
            projection=projection,
            expected=expected,
            envelope_reference=envelope_reference,
            same_authority=same_authority,
            gap=gap,
            lineage=lineage,
        )
        return record
    if mismatched_fields:
        raise ProductRuntimeConflict(
            f"governed-autonomy activation record {mismatched_fields[0]} mismatch"
        )
    if record.get("same_authority_subset") != same_authority:
        raise ProductRuntimeConflict("governed-autonomy same-authority subset mismatch")
    if record.get("governed_autonomy_envelope_reference") != envelope_reference:
        raise ProductRuntimeConflict("governed-autonomy envelope reference mismatch")
    if record.get("capability_gap_SHA256") != expected_gap_sha:
        raise ProductRuntimeConflict("governed-autonomy capability gap digest mismatch")
    if record.get("capability_gap_reference") != gap:
        raise ProductRuntimeConflict("governed-autonomy capability gap reference mismatch")
    if record.get("continuation_lineage_SHA256") != expected_lineage_sha:
        raise ProductRuntimeConflict("governed-autonomy continuation digest mismatch")
    if record.get("continuation_lineage_reference") != lineage:
        raise ProductRuntimeConflict("governed-autonomy continuation reference mismatch")
    return record


def validate_governed_autonomy_runtime_state_record(
    record: dict[str, Any],
    *,
    projection_record: dict[str, Any] | None = None,
    activation_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate persisted 01AI operational continuation state."""

    if not isinstance(record, dict):
        raise ProductRuntimeConflict("governed-autonomy runtime state must be an object")
    if record.get("runtime_state_SHA256") != _governed_autonomy_runtime_record_digest(record):
        raise ProductRuntimeConflict("governed-autonomy runtime state digest mismatch")
    for forbidden_key in (
        "governed_autonomy_envelope",
        "task_local_source_text",
        "delegate_result",
        "raw_reasoning",
        "chain_of_thought",
        "hidden_reasoning",
    ):
        if forbidden_key in record:
            raise ProductRuntimeConflict(
                f"governed-autonomy runtime state must not persist {forbidden_key}"
            )
    projection = projection_record if projection_record is not None else _load_current_projection_record()
    _validate_execution_start_authority(projection)
    activation = activation_record
    if activation is None:
        activation = load_current_ticket_governed_autonomy_activation_record(
            projection_record=projection,
        )
    if activation is None:
        raise ProductRuntimeConflict("governed-autonomy runtime state requires active authority")
    _binding, identity = _current_ticket_identity_fields(projection)
    envelope_reference = _validated_governed_autonomy_envelope_reference(
        record.get("governed_autonomy_envelope_reference")
    )
    if envelope_reference != activation.get("governed_autonomy_envelope_reference"):
        raise ProductRuntimeConflict("governed-autonomy runtime envelope reference mismatch")
    budget_reference = _validated_governed_autonomy_budget_reference(
        record.get("governed_autonomy_budget")
    )
    if budget_reference != activation.get("governed_autonomy_budget"):
        raise ProductRuntimeConflict("governed-autonomy runtime budget reference mismatch")
    expected = {
        "schema_version": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_RUNTIME_POLICY_ID,
        "source_system": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM,
        **identity,
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "activation_action_SHA256": activation["activation_action_SHA256"],
        "governed_autonomy_policy_id": activation["governed_autonomy_policy_id"],
        "governed_autonomy_envelope_SHA256": activation["governed_autonomy_envelope_SHA256"],
        "same_authority_subset_validated": True,
        "legacy_human_recovery_retry_micro_gates_required": False,
        "legacy_run_mutation_performed": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ProductRuntimeConflict(f"governed-autonomy runtime state {key} mismatch")
    if record.get("human_smoke_marker") not in {
        PEPPER_GOVERNED_AUTONOMY_READY_MARKER,
        PEPPER_LEGACY_GOVERNED_AUTONOMY_READY_MARKER,
    }:
        raise ProductRuntimeConflict("governed-autonomy runtime state human_smoke_marker mismatch")
    if record.get("runtime_decision") not in _GOVERNED_AUTONOMY_RUNTIME_DECISIONS:
        raise ProductRuntimeConflict("governed-autonomy runtime decision is invalid")
    for key in (
        "process_continuation_count",
        "self_repair_count",
        "task_local_tool_candidate_count",
        "command_evaluation_count",
        "A2A_delegation_count",
        "validation_failure_count",
        "no_progress_count",
    ):
        value = record.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ProductRuntimeConflict(f"governed-autonomy runtime {key} is invalid")
    for key in ("budget_exhausted", "authority_revalidated"):
        if not isinstance(record.get(key), bool):
            raise ProductRuntimeConflict(f"governed-autonomy runtime {key} is invalid")
    if "fresh_execution_requested" in record:
        if not isinstance(record.get("fresh_execution_requested"), bool):
            raise ProductRuntimeConflict("governed-autonomy fresh execution flag is invalid")
        if record.get("fresh_execution_requested"):
            fresh_request_sha = record.get("fresh_execution_request_SHA256")
            fresh_request_reference = record.get("fresh_execution_request_reference")
            if not isinstance(fresh_request_sha, str) or not _SAFE_SHA256.fullmatch(
                fresh_request_sha
            ):
                raise ProductRuntimeConflict(
                    "governed-autonomy fresh execution request digest is invalid"
                )
            if not isinstance(fresh_request_reference, dict):
                raise ProductRuntimeConflict(
                    "governed-autonomy fresh execution request reference is invalid"
                )
            if fresh_request_reference.get("fresh_execution_request_SHA256") != fresh_request_sha:
                raise ProductRuntimeConflict(
                    "governed-autonomy fresh execution request reference mismatch"
                )
            if record.get("execution_attempt_reason") != (
                PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON
            ):
                raise ProductRuntimeConflict(
                    "governed-autonomy fresh execution reason mismatch"
                )
            if _int_or_none(record.get("prior_terminal_run_id")) is None:
                raise ProductRuntimeConflict(
                    "governed-autonomy fresh execution prior terminal run is invalid"
                )
    latest_fingerprint = record.get("latest_no_progress_fingerprint_SHA256")
    if latest_fingerprint is not None and (
        not isinstance(latest_fingerprint, str) or not _SAFE_SHA256.fullmatch(latest_fingerprint)
    ):
        raise ProductRuntimeConflict("governed-autonomy runtime no-progress fingerprint invalid")
    progress_markers = record.get("progress_marker_SHA256s")
    if not isinstance(progress_markers, list) or any(
        not isinstance(item, str) or not _SAFE_SHA256.fullmatch(item)
        for item in progress_markers
    ):
        raise ProductRuntimeConflict("governed-autonomy runtime progress markers invalid")
    if not isinstance(record.get("budget_remaining"), dict):
        raise ProductRuntimeConflict("governed-autonomy runtime budget remaining is invalid")
    if not isinstance(record.get("latest_decision_evidence"), dict):
        raise ProductRuntimeConflict("governed-autonomy runtime decision evidence is invalid")
    current_side_effects = record.get("current_invocation_side_effects")
    if not isinstance(current_side_effects, dict):
        raise ProductRuntimeConflict("governed-autonomy runtime side effects are invalid")
    direct_dispatch_authorized = (
        record.get("runtime_decision") == "DIRECT"
        and record.get("governed_autonomy_continuation_reason")
        == PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON
    )
    for key in (
        "dispatch_performed",
        "Kanban_dispatch",
        "execution_started",
        "worker_execution",
        "worker_process_started",
        "lineage_dispatch_performed",
    ):
        value = record.get(key, False)
        if not isinstance(value, bool):
            raise ProductRuntimeConflict(f"governed-autonomy runtime {key} is invalid")
        if current_side_effects.get(key, False) is not value:
            raise ProductRuntimeConflict(f"governed-autonomy runtime side effect {key} mismatch")
        if value and not direct_dispatch_authorized:
            raise ProductRuntimeConflict(
                f"governed-autonomy runtime forbidden side effect {key} mismatch"
            )
    kanban_run_created = record.get("kanban_run_created", False)
    if not isinstance(kanban_run_created, bool):
        raise ProductRuntimeConflict("governed-autonomy runtime kanban_run_created is invalid")
    if kanban_run_created and not direct_dispatch_authorized:
        raise ProductRuntimeConflict("governed-autonomy runtime forbidden run creation mismatch")
    if kanban_run_created and _int_or_none(record.get("kanban_run_id")) is None:
        raise ProductRuntimeConflict("governed-autonomy runtime Kanban run id is invalid")
    forbidden_side_effects = {
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    for key, value in forbidden_side_effects.items():
        if current_side_effects.get(key) != value:
            raise ProductRuntimeConflict(
                f"governed-autonomy runtime forbidden side effect {key} mismatch"
            )
    a2a_dispatch_performed = current_side_effects.get(
        "A2A_dispatch_performed",
        bool(record.get("A2A_dispatch_performed")),
    )
    if record.get("runtime_decision") == "A2A_DELEGATION":
        if a2a_dispatch_performed is not True:
            raise ProductRuntimeConflict("governed-autonomy A2A runtime side effect mismatch")
    elif a2a_dispatch_performed is not False:
        raise ProductRuntimeConflict("governed-autonomy A2A side effect mismatch")
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
    projection = _load_current_projection_record()
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    _validate_execution_recovery_request_guards(request, projection_record=projection)
    _validate_execution_recovery_authorization_text(
        request.human_authorization_text,
        current_ticket_id=binding.ticket_id,
        requested_ticket_id=request.ticket_id,
        requested_next_action_id=request.next_action_id,
    )
    _validate_execution_start_authority(projection)
    existing = load_current_ticket_recovery_action_record(projection_record=projection)
    if existing is not None and _recovery_record_matches_current_failure(projection, existing):
        if existing.get("human_authorization_text") != request.human_authorization_text:
            raise ProductRuntimeConflict(
                f"{binding.ticket_id} recovery was already recorded with different authorization text"
            )
        return _recovery_action_operational_result(existing, idempotent_replay=True)
    if existing is not None:
        _archive_existing_authority_record(
            recovery_action_record_path_for_ticket(binding.ticket_id),
            recovery_action_history_path_for_ticket(binding.ticket_id),
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
            blocker_detail=f"{binding.ticket_id} retry budget is exhausted",
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


def get_current_ticket_governed_autonomy_status(
    *,
    project_id: str | None = None,
    ticket_id: str | None = None,
) -> dict[str, Any]:
    """Return current-ticket 01AH activation status without side effects."""

    try:
        projection = _load_current_projection_record()
    except ProductRuntimeError as exc:
        return _governed_autonomy_status_without_record(
            project_id=project_id or PEPPER_GOVERNED_PROJECT_ID,
            ticket_id=ticket_id,
            blocker_code="GOVERNED_AUTONOMY_PROJECTION_GAP",
            blocker_detail=str(exc) or "current Kanban projection is unavailable",
        )
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    if project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(
            f"governed autonomy status is bounded to project {binding.project_id}"
        )
    if ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(
            f"governed autonomy status is bounded to ticket {binding.ticket_id}"
        )
    record = load_current_ticket_governed_autonomy_activation_record(
        projection_record=projection,
    )
    if record is None:
        return _governed_autonomy_status_without_record(
            project_id=binding.project_id,
            ticket_id=binding.ticket_id,
            ticket_title=binding.ticket_title,
            projection=projection,
        )
    result = _governed_autonomy_activation_operational_result(
        record,
        idempotent_replay=True,
    )
    runtime_state = load_current_ticket_governed_autonomy_runtime_state(
        projection_record=projection,
        activation_record=record,
    )
    effective_authority = _resolve_effective_current_governed_autonomy_authority(
        projection=projection,
        activation=record,
        previous=runtime_state,
    )
    result["authority_revalidated"] = bool(
        effective_authority["authority_revalidated"]
    )
    result["continuation_eligible"] = bool(
        effective_authority["continuation_eligible"]
    )
    result["effective_authority_diagnostics"] = effective_authority["diagnostics"]
    if runtime_state is None:
        result.update({
            "governed_autonomy_runtime_status": "active_authority_ready_for_continuation",
            "runtime_decision": None,
            "runtime_state_SHA256": None,
            "process_continuation_count": 0,
            "self_repair_count": 0,
            "A2A_delegation_count": 0,
            "validation_failure_count": 0,
            "no_progress_count": 0,
            "budget_limits": record.get("governed_autonomy_budget"),
            "budget_remaining": record.get("governed_autonomy_budget"),
            "budget_exhausted": False,
            "next_autonomous_action": "call continue_current_ticket_governed_autonomy with active server-derived authority",
            "next_human_action": None,
            "governed_autonomy_runtime": None,
        })
        return result
    terminal_reconciliation = _governed_autonomy_runtime_terminal_reconciliation(
        runtime_state,
        effective_authority=effective_authority,
    )
    runtime_summary = _governed_autonomy_runtime_summary(
        runtime_state,
        terminal_reconciliation=terminal_reconciliation,
        effective_authority=effective_authority,
    )
    result.update({
        "governed_autonomy_runtime_status": runtime_state["governed_autonomy_runtime_status"],
        "runtime_decision": runtime_state["runtime_decision"],
        "runtime_state_SHA256": runtime_state["runtime_state_SHA256"],
        "process_continuation_count": _effective_governed_autonomy_process_continuation_count(
            runtime_state
        ),
        "recorded_process_continuation_count": runtime_state["process_continuation_count"],
        "self_repair_count": runtime_state["self_repair_count"],
        "task_local_tool_candidate_count": runtime_state["task_local_tool_candidate_count"],
        "command_evaluation_count": runtime_state["command_evaluation_count"],
        "A2A_delegation_count": runtime_state["A2A_delegation_count"],
        "validation_failure_count": runtime_state["validation_failure_count"],
        "no_progress_count": runtime_state["no_progress_count"],
        "budget_limits": runtime_state["budget_limits"],
        "budget_remaining": runtime_state["budget_remaining"],
        "budget_exhausted": runtime_state["budget_exhausted"],
        "blocker_code": runtime_state.get("blocker_code"),
        "blocker_detail": runtime_state.get("blocker_detail"),
        "fresh_execution_requested": bool(runtime_state.get("fresh_execution_requested")),
        "fresh_execution_request_SHA256": runtime_state.get(
            "fresh_execution_request_SHA256"
        ),
        "fresh_execution_request_reference": runtime_state.get(
            "fresh_execution_request_reference"
        ),
        "execution_attempt_reason": runtime_state.get("execution_attempt_reason"),
        "prior_terminal_run_id": runtime_state.get("prior_terminal_run_id"),
        "next_autonomous_action": runtime_state.get("next_autonomous_action"),
        "next_human_action": runtime_state.get("next_human_action"),
        "latest_runtime_side_effects": runtime_state["current_invocation_side_effects"],
        "kanban_run_created": bool(runtime_state.get("kanban_run_created")),
        "kanban_run_id": runtime_state.get("kanban_run_id"),
        "workspace_path": runtime_state.get("workspace_path"),
        "dispatch_performed": bool(runtime_state.get("dispatch_performed")),
        "execution_started": bool(runtime_state.get("execution_started")),
        "worker_execution": bool(runtime_state.get("worker_execution")),
        "worker_process_started": bool(runtime_state.get("worker_process_started")),
        "Kanban_dispatch": bool(runtime_state.get("Kanban_dispatch")),
        "lineage_dispatch_performed": bool(runtime_state.get("lineage_dispatch_performed")),
        "live_autonomous_continuation_marker": runtime_state.get(
            "live_autonomous_continuation_marker"
        ),
        "governed_autonomy_runtime": runtime_summary,
    })
    return _governed_autonomy_apply_terminal_reconciliation(
        result,
        terminal_reconciliation,
    )


def activate_current_ticket_governed_autonomy(
    *,
    human_request_text: str,
    authorizer_id: str = "pepper-chat-human",
    project_id: str | None = None,
    ticket_id: str | None = None,
    next_action_id: str | None = None,
) -> dict[str, Any]:
    """Persist dispatch-free 01AH activation status for the current ticket."""

    request = CurrentTicketGovernedAutonomyActivationRequest(
        human_request_text=human_request_text,
        authorizer_id=authorizer_id,
        project_id=project_id,
        ticket_id=ticket_id,
        next_action_id=next_action_id,
    )
    projection = _load_current_projection_record()
    _validate_execution_start_authority(projection)
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    workflow = build_workflow_control_snapshot()
    _validate_governed_autonomy_activation_request_guards(
        request,
        projection_record=projection,
        workflow=workflow,
    )
    _validate_governed_autonomy_activation_request_text(
        request.human_request_text,
        ticket_id=binding.ticket_id,
    )

    existing = load_current_ticket_governed_autonomy_activation_record(
        projection_record=projection,
    )
    if existing is not None:
        if (
            existing.get("human_request_text") == request.human_request_text
            and existing.get("authorizer_id") == request.authorizer_id
        ):
            return _governed_autonomy_activation_operational_result(
                existing,
                idempotent_replay=True,
            )
    record = _build_governed_autonomy_activation_record(
        request=request,
        projection=projection,
        workflow=workflow,
    )
    if existing is not None:
        existing_cycle = _governed_autonomy_activation_cycle(existing)
        new_cycle = _governed_autonomy_activation_cycle(record)
        if existing_cycle == new_cycle:
            return _governed_autonomy_activation_operational_result(
                existing,
                idempotent_replay=True,
            )
        _archive_existing_authority_record(
            governed_autonomy_activation_record_path_for_ticket(binding.ticket_id),
            governed_autonomy_activation_history_path_for_ticket(binding.ticket_id),
            reason="replaced_by_current_governed_autonomy_activation",
        )
    _persist_governed_autonomy_activation_record(record)
    return _governed_autonomy_activation_operational_result(
        record,
        idempotent_replay=False,
    )


def continue_current_ticket_governed_autonomy(
    *,
    runtime_goal: str,
    observed_failure: str | None = None,
    requested_capability: str | None = None,
    strategy: Literal[
        "AUTO",
        "DIRECT",
        "TASK_LOCAL_SELF_EXTENSION",
        "A2A_DELEGATION",
        "STOP_FOR_HUMAN",
    ] = "AUTO",
    task_local_tool_name: str | None = None,
    task_local_language: Literal["python", "javascript", "typescript"] = "python",
    task_local_implementation_path: str | None = None,
    task_local_source_text: str | None = None,
    task_local_command: str | None = None,
    delegate_goal: str | None = None,
    delegate_paths: tuple[str, ...] = (),
    delegate_requested_operations: tuple[str, ...] = (),
    delegate_runner: Any | None = None,
    delegate_result: dict[str, Any] | None = None,
    delegate_parent_agent: Any | None = None,
    fresh_execution_request_text: str | None = None,
    spawn_fn: Any = None,
    project_id: str | None = None,
    ticket_id: str | None = None,
) -> dict[str, Any]:
    """Consume already-active server-derived governed-autonomy authority."""

    request = CurrentTicketGovernedAutonomyContinuationRequest(
        runtime_goal=runtime_goal,
        observed_failure=observed_failure,
        requested_capability=requested_capability,
        strategy=strategy,
        task_local_tool_name=task_local_tool_name,
        task_local_language=task_local_language,
        task_local_implementation_path=task_local_implementation_path,
        task_local_source_text=task_local_source_text,
        task_local_command=task_local_command,
        delegate_goal=delegate_goal,
        delegate_paths=tuple(delegate_paths or ()),
        delegate_requested_operations=tuple(delegate_requested_operations or ()),
        delegate_result=delegate_result,
        fresh_execution_request_text=fresh_execution_request_text,
        project_id=project_id,
        ticket_id=ticket_id,
    )
    projection = _load_current_projection_record()
    _validate_execution_start_authority(projection)
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(
            f"governed autonomy continuation is bounded to project {binding.project_id}"
        )
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(
            f"governed autonomy continuation is bounded to ticket {binding.ticket_id}"
        )
    activation = load_current_ticket_governed_autonomy_activation_record(
        projection_record=projection,
    )
    if activation is None:
        raise ProductRuntimeConflict("governed autonomy continuation requires active server-derived authority")
    previous = load_current_ticket_governed_autonomy_runtime_state(
        projection_record=projection,
        activation_record=activation,
    )
    effective_authority = _resolve_effective_current_governed_autonomy_authority(
        projection=projection,
        activation=activation,
        previous=previous,
    )
    authority = _require_current_governed_autonomy_authority_match(
        projection=projection,
        activation=activation,
        previous=previous,
        effective_authority=effective_authority,
    )
    if _governed_autonomy_active_execution_replay(previous, projection):
        result = _governed_autonomy_runtime_operational_result(
            previous,
            activation_record=activation,
            idempotent_replay=True,
            effective_authority=effective_authority,
        )
        result["non_consuming_observation"] = True
        result["observation_status"] = "governed_autonomy_execution_already_active"
        return result
    decision = _select_governed_autonomy_runtime_decision(request)
    terminal_reconciliation = _governed_autonomy_runtime_terminal_reconciliation(
        previous,
        effective_authority=effective_authority,
    )
    fresh_execution_request = _governed_autonomy_fresh_execution_request_reference(
        request,
        projection=projection,
        activation=activation,
        terminal_reconciliation=terminal_reconciliation,
    )
    fresh_execution_request_pending_replay = (
        decision == "DIRECT"
        and _governed_autonomy_fresh_execution_request_pending_replay(
            previous,
            fresh_execution_request,
        )
    )
    if terminal_reconciliation is not None and decision == "DIRECT":
        if _governed_autonomy_fresh_execution_request_already_consumed(
            previous,
            fresh_execution_request,
        ):
            result = _governed_autonomy_runtime_operational_result(
                previous,
                activation_record=activation,
                idempotent_replay=True,
                effective_authority=effective_authority,
            )
            result["fresh_execution_requested"] = True
            result["fresh_execution_duplicate_suppressed"] = True
            result["fresh_execution_request_SHA256"] = fresh_execution_request[
                "fresh_execution_request_SHA256"
            ]
            result["non_consuming_observation"] = True
            result["observation_status"] = "governed_autonomy_fresh_execution_request_replayed"
            return result
        if fresh_execution_request is None:
            result = _governed_autonomy_runtime_operational_result(
                previous,
                activation_record=activation,
                idempotent_replay=True,
                effective_authority=effective_authority,
            )
            result["non_consuming_observation"] = True
            result["observation_status"] = "governed_autonomy_execution_terminal_reconciled"
            return result

    if fresh_execution_request is not None and terminal_reconciliation is None:
        record = _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="FRESH_EXECUTION_TERMINAL_SOURCE_REQUIRED",
            blocker_detail="fresh same-authority execution requires an owned terminal run source",
            validation_failed=True,
            provider_readiness={"ok": True},
            extra_evidence={
                "fresh_execution_request_reference": fresh_execution_request,
            },
        )
        _persist_governed_autonomy_runtime_state(record)
        return _governed_autonomy_runtime_operational_result(
            record,
            activation_record=activation,
            idempotent_replay=False,
            effective_authority=effective_authority,
        )

    if fresh_execution_request is not None and decision != "DIRECT":
        record = _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="FRESH_EXECUTION_REQUIRES_DIRECT_STRATEGY",
            blocker_detail="fresh same-authority execution requires DIRECT strategy",
            validation_failed=True,
            provider_readiness={"ok": True},
            extra_evidence={
                "fresh_execution_request_reference": fresh_execution_request,
            },
        )
        _persist_governed_autonomy_runtime_state(record)
        return _governed_autonomy_runtime_operational_result(
            record,
            activation_record=activation,
            idempotent_replay=False,
            effective_authority=effective_authority,
        )
    provider_readiness = _executor_provider_readiness(str(projection["assignee_profile"]))
    if provider_readiness.get("ok") is not True:
        record = _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code=provider_readiness.get("blocker_code") or "EXECUTOR_PROVIDER_RESOLUTION_GAP",
            blocker_detail=provider_readiness.get("blocker_detail") or "executor provider unavailable",
            validation_failed=True,
            provider_readiness=provider_readiness,
        )
        _persist_governed_autonomy_runtime_state(record)
        return _governed_autonomy_runtime_operational_result(
            record,
            activation_record=activation,
            idempotent_replay=False,
        )
    if decision == "DIRECT":
        worker_credential_probe = _preflight_pepper_governed_worker_credentials(
            projection,
            enabled=spawn_fn is None,
        )
        if not worker_credential_probe.get("ok"):
            record = _build_governed_autonomy_runtime_stop_record(
                request=request,
                projection=projection,
                activation=activation,
                previous=previous,
                runtime_decision="STOP_FOR_HUMAN",
                blocker_code=worker_credential_probe.get("blocker_code")
                or "WORKER_CREDENTIAL_AUTHORITY_MISMATCH",
                blocker_detail=worker_credential_probe.get("blocker_detail")
                or "governed worker credential probe failed",
                validation_failed=True,
                provider_readiness={
                    **provider_readiness,
                    "worker_credential_probe": worker_credential_probe,
                },
            )
            _persist_governed_autonomy_runtime_state(record)
            return _governed_autonomy_runtime_operational_result(
                record,
                activation_record=activation,
                idempotent_replay=False,
            )
        provider_readiness = dict(provider_readiness)
        provider_readiness["worker_credential_probe"] = worker_credential_probe
    budget_blocker = _governed_autonomy_runtime_budget_blocker(
        activation,
        previous,
        requested_decision=decision,
        request=request,
        fresh_execution_request_pending_replay=fresh_execution_request_pending_replay,
    )
    if budget_blocker is not None:
        record = _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code=budget_blocker[0],
            blocker_detail=budget_blocker[1],
            validation_failed=False,
            provider_readiness=provider_readiness,
        )
        _persist_governed_autonomy_runtime_state(record)
        return _governed_autonomy_runtime_operational_result(
            record,
            activation_record=activation,
            idempotent_replay=False,
        )

    if decision == "TASK_LOCAL_SELF_EXTENSION":
        record = _build_governed_autonomy_self_extension_runtime_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            envelope=authority,
            provider_readiness=provider_readiness,
        )
    elif decision == "A2A_DELEGATION":
        record = _build_governed_autonomy_a2a_runtime_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            envelope=authority,
            provider_readiness=provider_readiness,
            delegate_runner=delegate_runner,
            delegate_parent_agent=delegate_parent_agent,
        )
    elif decision == "STOP_FOR_HUMAN":
        record = _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="GOVERNED_AUTONOMY_STOP_REQUESTED",
            blocker_detail="runtime request selected STOP_FOR_HUMAN",
            validation_failed=False,
            provider_readiness=provider_readiness,
        )
    else:
        record = _build_governed_autonomy_direct_runtime_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            provider_readiness=provider_readiness,
            envelope=authority,
            terminal_reconciliation=terminal_reconciliation,
            spawn_fn=spawn_fn,
        )
    _persist_governed_autonomy_runtime_state(record)
    return _governed_autonomy_runtime_operational_result(
        record,
        activation_record=activation,
        idempotent_replay=False,
    )


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
    recovery_record = load_current_ticket_recovery_action_record(projection_record=projection)
    if recovery_record is None:
        return _blocked_current_execution_retry_start_result(
            projection,
            request=request,
            blocker_code="RECOVERY_AUTHORITY_GAP",
            blocker_detail=(
                f"{binding.ticket_id} retry start requires a persisted "
                "retry-pending recovery authority"
            ),
        )
    existing = load_current_ticket_retry_start_record(
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
                retry_start_record_path_for_ticket(binding.ticket_id),
                retry_start_history_path_for_ticket(binding.ticket_id),
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


def execution_recovery_authorization_text_diagnostics(
    value: str,
    *,
    current_ticket_id: str,
    requested_ticket_id: str | None = None,
    current_next_action_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any] | None:
    raw = str(value or "").strip()
    expected_ticket_id = str(current_ticket_id or "").strip()
    expected_next_action_id = (
        governed_ticket_lifecycle_action_ids(expected_ticket_id)["execution_recovery"]
        if expected_ticket_id
        else None
    )
    normalized = _normalize_authorization_intent_text(raw)
    observed_kind = _observed_execution_authorization_kind(normalized)
    base = {
        "current_ticket_id": expected_ticket_id or None,
        "requested_ticket_id": requested_ticket_id,
        "current_next_action_id": current_next_action_id,
        "requested_next_action_id": requested_next_action_id,
        "expected_next_action_id": expected_next_action_id,
        "authorization_kind": observed_kind,
        "expected_authorization_kind": "execution_recovery_authorization",
    }

    def blocked(code: str, detail: str) -> dict[str, Any]:
        return {
            **base,
            "blocker_code": code,
            "blocker_detail": detail,
        }

    if not expected_ticket_id:
        return blocked(
            "EXECUTION_RECOVERY_AUTHORITY_GAP",
            "current ticket is unavailable for execution recovery authorization",
        )
    if requested_next_action_id not in {None, expected_next_action_id}:
        return blocked(
            "EXECUTION_RECOVERY_ACTION_MISMATCH",
            f"execution recovery authorization requires {expected_next_action_id}",
        )
    if not raw:
        return blocked(
            "EXECUTION_RECOVERY_HUMAN_AUTHORIZATION_TEXT_GAP",
            "human_authorization_text is required",
        )
    if "?" in raw or "¿" in raw:
        return blocked(
            "EXECUTION_RECOVERY_HUMAN_AUTHORIZATION_TEXT_GAP",
            "execution recovery authorization text must not be a question",
        )
    if _authorization_text_is_ambiguous(normalized):
        return blocked(
            "EXECUTION_RECOVERY_HUMAN_AUTHORIZATION_TEXT_GAP",
            "execution recovery authorization text is ambiguous",
        )

    mentioned_ticket_ids = _mentioned_authorization_ticket_ids(normalized)
    base["mentioned_ticket_ids"] = sorted(mentioned_ticket_ids)
    if not mentioned_ticket_ids:
        return blocked(
            "EXECUTION_RECOVERY_HUMAN_AUTHORIZATION_TEXT_GAP",
            "execution recovery authorization text must name the current ticket",
        )
    if expected_ticket_id.upper() not in mentioned_ticket_ids:
        return blocked(
            "EXECUTION_RECOVERY_AUTHORIZATION_TICKET_MISMATCH",
            "execution recovery authorization targets a different ticket",
        )
    if not _authorization_text_has_recovery_intent(normalized):
        return blocked(
            "EXECUTION_AUTHORIZATION_KIND_MISMATCH",
            "explicit execution recovery authorization text is required",
        )
    if _authorization_text_has_retry_intent(normalized):
        return blocked(
            "EXECUTION_AUTHORIZATION_KIND_MISMATCH",
            "execution recovery authorization must not be retry-start authorization",
        )
    return None


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
    *,
    projection_record: dict[str, Any] | None = None,
) -> None:
    binding = resolve_current_ticket_lifecycle_binding(
        projection_record=projection_record,
    )
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(f"execution recovery is bounded to project {binding.project_id}")
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(f"execution recovery is bounded to ticket {binding.ticket_id}")
    if request.next_action_id not in {None, binding.execution_recovery_next_action_id}:
        raise ProductRuntimeConflict(
            f"execution recovery requires {binding.execution_recovery_next_action_id}"
        )


def _validate_execution_recovery_authorization_text(
    value: str,
    *,
    current_ticket_id: str,
    requested_ticket_id: str | None = None,
    current_next_action_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> None:
    diagnostics = execution_recovery_authorization_text_diagnostics(
        value,
        current_ticket_id=current_ticket_id,
        requested_ticket_id=requested_ticket_id,
        current_next_action_id=current_next_action_id,
        requested_next_action_id=requested_next_action_id,
    )
    if diagnostics is not None:
        raise ProductRuntimeDecisionFailed(str(diagnostics["blocker_detail"]))


def _validate_governed_autonomy_activation_request_guards(
    request: CurrentTicketGovernedAutonomyActivationRequest,
    *,
    projection_record: dict[str, Any],
    workflow: dict[str, Any],
) -> None:
    binding = resolve_current_ticket_lifecycle_binding(
        projection_record=projection_record,
    )
    if request.project_id not in {None, binding.project_id}:
        raise ProductRuntimeConflict(
            f"governed autonomy activation is bounded to project {binding.project_id}"
        )
    if request.ticket_id not in {None, binding.ticket_id}:
        raise ProductRuntimeConflict(
            f"governed autonomy activation is bounded to ticket {binding.ticket_id}"
        )
    current_next_action = workflow.get("next_action")
    current_next_action_id = (
        current_next_action.get("id")
        if isinstance(current_next_action, dict)
        else None
    )
    if request.next_action_id not in {
        None,
        current_next_action_id,
        binding.execution_recovery_next_action_id,
        governed_autonomy_continuation_action_id(binding.ticket_id),
    }:
        raise ProductRuntimeConflict(
            f"governed autonomy activation is bounded to active action {current_next_action_id}"
        )


def _governed_autonomy_text_has_activation_intent(normalized: str) -> bool:
    return bool(
        re.search(r"\b(01ah|autonomy|autonomia|autonomous|activation|activate|record|status|a2a)\b", normalized)
        or "governed autonomy" in normalized
        or "autonomia gobernada" in normalized
    )


def _governed_autonomy_text_has_denial_intent(normalized: str) -> bool:
    return bool(
        re.search(
            r"\b(?:do not authorize|don'?t authorize|not authorized|not authorize|"
            r"deny|denied|reject|rejected|revoke|revoked|"
            r"no autorizo|no autorizar|no autorizado|rechazo|rechazar|"
            r"revoco|revocar|deniego|denegar)\b",
            normalized,
        )
    )


def _validate_governed_autonomy_activation_request_text(
    value: str,
    *,
    ticket_id: str,
) -> None:
    raw = str(value or "").strip()
    normalized = _normalize_authorization_intent_text(raw)
    if not raw:
        raise ProductRuntimeDecisionFailed("governed autonomy activation text is required")
    if "?" in raw or "¿" in raw:
        raise ProductRuntimeDecisionFailed("governed autonomy activation text must not be a question")
    if _authorization_text_is_ambiguous(normalized):
        raise ProductRuntimeDecisionFailed("governed autonomy activation text is ambiguous")
    if _governed_autonomy_text_has_denial_intent(normalized):
        raise ProductRuntimeDecisionFailed("governed autonomy activation text must not deny autonomy")
    mentioned_ticket_ids = _mentioned_authorization_ticket_ids(normalized)
    if ticket_id.upper() not in mentioned_ticket_ids:
        raise ProductRuntimeDecisionFailed(
            "governed autonomy activation text must name the current ticket"
        )
    if not _governed_autonomy_text_has_activation_intent(normalized):
        raise ProductRuntimeDecisionFailed(
            "governed autonomy activation text must explicitly request autonomy status recording"
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

    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
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
                    f"treated as canonical {binding.ticket_id} WorkPacket authority"
                ),
                "synthetic_work_packet_id": synthetic_work_packet_id,
            }
        if task_body.get("WorkPacket_ID") != projection["work_packet_id"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": (
                    "projected Kanban task WorkPacket ID does not match "
                    f"{binding.ticket_id} authority"
                ),
                "observed_work_packet_id": task_body.get("WorkPacket_ID"),
                "canonical_work_packet_id": projection["work_packet_id"],
            }
        if task_body.get("WorkPacket_SHA256") != projection["work_packet_SHA256"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": (
                    "projected Kanban task WorkPacket SHA256 does not match "
                    f"{binding.ticket_id} authority"
                ),
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
                "blocker_detail": f"latest {binding.ticket_id} run has not ended",
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
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
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
            "blocker_detail": f"{binding.ticket_id} retry budget is exhausted",
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

    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
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
                    f"treated as canonical {binding.ticket_id} WorkPacket authority"
                ),
                "synthetic_work_packet_id": synthetic_work_packet_id,
            }
        if task_body.get("WorkPacket_ID") != projection["work_packet_id"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": (
                    "projected Kanban task WorkPacket ID does not match "
                    f"{binding.ticket_id} authority"
                ),
                "observed_work_packet_id": task_body.get("WorkPacket_ID"),
                "canonical_work_packet_id": projection["work_packet_id"],
            }
        if task_body.get("WorkPacket_SHA256") != projection["work_packet_SHA256"]:
            return {
                "blocker_code": "WORKPACKET_AUTHORITY_DRIFT_GAP",
                "blocker_detail": (
                    "projected Kanban task WorkPacket SHA256 does not match "
                    f"{binding.ticket_id} authority"
                ),
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
                "blocker_detail": f"latest {binding.ticket_id} run has not ended",
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
    current_cycle_id = _governed_ticket_recovery_cycle_id(
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

    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
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
            return (
                "WORKSPACE_POLICY_GAP",
                f"{binding.ticket_id} start only authorizes scratch workspace dispatch",
            )
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


_SCRATCH_SOURCE_SKIP_DIR_NAMES = frozenset({
    ".git",
    ".opencode",
    ".agents",
    ".cache",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".turbo",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "graphify-out",
    "node_modules",
    "out",
    "target",
    "venv",
    ".venv",
})
_SCRATCH_SOURCE_SKIP_FILE_SUFFIXES = frozenset({".pyc", ".pyo"})
_SCRATCH_SOURCE_COMMON_PACKAGE_FILES = (
    "package.json",
    "tsconfig.json",
    "tsconfig.app.json",
    "tsconfig.node.json",
    "vite.config.ts",
    "vitest.config.ts",
    "eslint.config.js",
    "index.html",
)
_SCRATCH_SOURCE_PACKAGE_CLOSURES = (
    {
        "package_rel": "2_products/pepper-agent/web",
        "source_dirs": ("src", "public"),
        "support_files": _SCRATCH_SOURCE_COMMON_PACKAGE_FILES,
    },
    {
        "package_rel": "2_products/pepper-agent/apps/desktop",
        "source_dirs": ("src", "electron", "public"),
        "support_files": _SCRATCH_SOURCE_COMMON_PACKAGE_FILES,
    },
    {
        "package_rel": "2_products/pepper-agent/ui-tui",
        "source_dirs": ("src",),
        "support_files": _SCRATCH_SOURCE_COMMON_PACKAGE_FILES,
    },
)
_SCRATCH_DEPENDENCY_EXCLUDED_DIR_NAMES = frozenset({
    ".cache",
    ".vite",
    ".turbo",
    "__pycache__",
})
_SCRATCH_DEPENDENCY_PROTECTED_DIR_NAMES = frozenset({
    ".agents",
    ".git",
    ".opencode",
    "4_external",
    "graphify-out",
})
_FRONTEND_DEPENDENCY_SENTINEL_ENTRIES = (
    "vitest/vitest.mjs",
    "vite/package.json",
    "react/package.json",
    "react-dom/package.json",
    "@vitejs/plugin-react/package.json",
)
_PACKAGE_DEPENDENCY_SECTIONS = (
    "dependencies",
    "devDependencies",
    "optionalDependencies",
    "peerDependencies",
)
_LOCAL_FILE_DEPENDENCY_PREFIX = "file:"


class ProductRuntimeDependencyGap(ProductRuntimeConflict):
    def __init__(self, dependency_code: str, detail: str) -> None:
        self.dependency_code = dependency_code
        self.external_code = IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP
        super().__init__(detail)


def _agent_platform_repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _materialize_pepper_governed_scratch_source(
    projection: dict[str, Any],
    workspace: Path | str,
    *,
    env_overlay: dict[str, str] | None = None,
    source_root: Path | str | None = None,
) -> dict[str, Any]:
    """Materialize a governed scratch source tree before worker spawn."""

    if projection.get("workspace_kind") != "scratch":
        raise ProductRuntimeConflict("governed source materialization requires scratch workspace")
    workspace_path = Path(workspace).expanduser()
    if not workspace_path.is_absolute():
        raise ProductRuntimeConflict("governed scratch workspace path is not absolute")
    workspace_path.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    overlay = env_overlay or _pepper_governed_worker_env_overlay(projection)
    env.update({str(key): str(value) for key, value in overlay.items()})
    env["HERMES_KANBAN_WORKSPACE"] = str(workspace_path)
    env["TERMINAL_CWD"] = str(workspace_path)
    from tools import governed_workpacket_file_guard as file_guard

    authority = file_guard.resolve_governed_workpacket_file_authority(env)
    materialization = _materialize_workpacket_scratch_source_tree(
        authority,
        source_root=source_root,
    )
    from tools import workpacket_validation_tool as validation_tool

    try:
        (
            _validation_authority,
            work_packet,
        ) = validation_tool.resolve_governed_workpacket_validation_authority(env)
    except Exception as exc:
        raise ProductRuntimeDependencyGap(
            VALIDATION_RUNTIME_UNAVAILABLE,
            "governed validation authority is unavailable for dependency substrate readiness",
        ) from exc
    dependency_materialization = _materialize_workpacket_dependency_substrate(
        authority,
        work_packet,
        source_root=source_root,
    )
    materialization.update(dependency_materialization)
    _write_materialization_manifest(
        Path(materialization["manifest_path"]),
        materialization,
        workspace_root=authority.resolved_workspace_root,
    )
    return materialization


def _projection_requires_scratch_source_materialization(projection: dict[str, Any]) -> bool:
    fields: list[Any] = [
        projection.get("execution_profile_role"),
        projection.get("selected_role"),
        projection.get("assignee_profile"),
        projection.get("selected_profile"),
    ]
    requirements = projection.get("ticket_execution_requirements")
    if isinstance(requirements, dict):
        fields.append(requirements.get("role"))
        fields.extend(requirements.get("semantic_capabilities") or ())
    return any("implementation" in str(value or "").casefold() for value in fields)


def _materialize_workpacket_dependency_substrate(
    authority: Any,
    work_packet: Any,
    *,
    source_root: Path | str | None = None,
) -> dict[str, Any]:
    """Copy preinstalled validation dependencies into scratch when required."""

    from tools import workpacket_validation_tool as validation_tool

    source = (
        Path(source_root).expanduser()
        if source_root is not None
        else _agent_platform_repository_root()
    )
    try:
        resolved_source = source.resolve(strict=True)
    except OSError as exc:
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_SOURCE_NOT_FOUND,
            "canonical source root is unavailable for dependency substrate discovery",
        ) from exc
    workspace = Path(authority.resolved_workspace_root).resolve(strict=True)
    specs = validation_tool.build_governed_validation_command_specs(authority, work_packet)
    frontend_specs = tuple(spec for spec in specs if str(spec.source).startswith("package:"))
    if not frontend_specs:
        return _empty_dependency_materialization_record(authority)

    substrates: list[dict[str, Any]] = []
    copied_destinations: set[str] = set()
    local_package_sources: list[dict[str, Any]] = []
    copied_local_package_source_roots: set[str] = set()
    local_package_source_copied_file_count = 0
    for spec in frontend_specs:
        package_dir = Path(spec.working_directory)
        try:
            package_rel = package_dir.relative_to(workspace).as_posix()
        except ValueError as exc:
            raise ProductRuntimeDependencyGap(
                VALIDATION_RUNTIME_UNAVAILABLE,
                "validation package cwd is outside scratch workspace",
            ) from exc
        dependency_entries = _package_dependency_entries(resolved_source, package_rel)
        required_package_names = frozenset(
            str(entry["name"]) for entry in dependency_entries
        )
        local_source_records, copied_count = _materialize_local_file_package_sources(
            resolved_source,
            workspace,
            package_rel,
            dependency_entries,
            copied_package_roots=copied_local_package_source_roots,
        )
        local_package_sources.extend(local_source_records)
        local_package_source_copied_file_count += copied_count
        candidates = _dependency_root_candidates(
            package_rel,
            source_root=resolved_source,
            workspace_root=workspace,
        )
        if not any(
            (source_root_path / "vitest/vitest.mjs").is_file()
            for source_root_path, _dest in candidates
        ):
            raise ProductRuntimeDependencyGap(
                DEPENDENCY_SOURCE_NOT_FOUND,
                "vitest dependency source root is unavailable for scratch validation",
            )
        for source_root_path, destination_root in candidates:
            if not source_root_path.is_dir():
                continue
            has_runtime_sentinel = any(
                (source_root_path / entry).exists()
                for entry in _FRONTEND_DEPENDENCY_SENTINEL_ENTRIES
            )
            has_declared_package = _dependency_root_contains_declared_package(
                source_root_path,
                required_package_names,
            )
            if not has_runtime_sentinel and not has_declared_package:
                continue
            destination_key = destination_root.resolve(strict=False).as_posix().casefold()
            if destination_key in copied_destinations:
                continue
            copied_destinations.add(destination_key)
            substrates.append(
                _copy_dependency_substrate_root(
                    source_root_path,
                    destination_root,
                    source_root=resolved_source,
                    workspace_root=workspace,
                    package_rel=package_rel,
                    authority=authority,
                    required_package_names=required_package_names,
                )
            )
        resolved_vitest = validation_tool._resolve_node_module_entry(  # noqa: SLF001
            workspace,
            workspace / package_rel,
            "vitest/vitest.mjs",
        )
        if resolved_vitest is None:
            raise ProductRuntimeDependencyGap(
                DEPENDENCY_PROVENANCE_MISMATCH,
                "scratch dependency substrate does not expose vitest at the authorized package cwd",
            )

    total_files = sum(int(item["copied_file_count"]) for item in substrates)
    total_dirs = sum(int(item["copied_directory_count"]) for item in substrates)
    total_bytes = sum(int(item["copied_bytes"]) for item in substrates)
    return {
        "dependency_substrate_materialized": bool(substrates),
        "dependency_substrate_policy_id": PEPPER_SCRATCH_DEPENDENCY_SUBSTRATE_POLICY_ID,
        "dependency_substrate_kind": "physical_node_modules_snapshot",
        "dependency_substrates": substrates,
        "dependency_substrate_copied_file_count": total_files,
        "dependency_substrate_copied_directory_count": total_dirs,
        "dependency_substrate_copied_bytes": total_bytes,
        "dependency_substrate_excluded_directories": sorted(
            _SCRATCH_DEPENDENCY_EXCLUDED_DIR_NAMES
        ),
        "product_diff_excluded_roots": sorted(
            item["scratch_dependency_root_relative"] for item in substrates
        ),
        "local_package_sources_materialized": bool(local_package_sources),
        "local_package_source_materializations": sorted(
            local_package_sources,
            key=lambda item: (
                str(item["local_package_source_relative"]),
                str(item["package_name"]),
            ),
        ),
        "local_package_source_copied_file_count": local_package_source_copied_file_count,
        "dependency_install_performed": False,
        "canonical_package_lock_materialized": False,
    }


def _empty_dependency_materialization_record(authority: Any) -> dict[str, Any]:
    _ = authority
    return {
        "dependency_substrate_materialized": False,
        "dependency_substrate_policy_id": PEPPER_SCRATCH_DEPENDENCY_SUBSTRATE_POLICY_ID,
        "dependency_substrate_kind": "not_required",
        "dependency_substrates": [],
        "dependency_substrate_copied_file_count": 0,
        "dependency_substrate_copied_directory_count": 0,
        "dependency_substrate_copied_bytes": 0,
        "dependency_substrate_excluded_directories": sorted(
            _SCRATCH_DEPENDENCY_EXCLUDED_DIR_NAMES
        ),
        "product_diff_excluded_roots": [],
        "local_package_sources_materialized": False,
        "local_package_source_materializations": [],
        "local_package_source_copied_file_count": 0,
        "dependency_install_performed": False,
        "canonical_package_lock_materialized": False,
    }


def _dependency_root_candidates(
    package_rel: str,
    *,
    source_root: Path,
    workspace_root: Path,
) -> tuple[tuple[Path, Path], ...]:
    rels = []
    for rel in (
        f"{package_rel}/node_modules",
        "2_products/pepper-agent/node_modules",
        "node_modules",
    ):
        normalized = _normalize_dependency_root_relative_path(rel)
        if normalized not in rels:
            rels.append(normalized)
    return tuple((source_root / rel, workspace_root / rel) for rel in rels)


def _package_dependency_entries(
    source_root: Path,
    package_rel: str,
) -> tuple[dict[str, str], ...]:
    package_json = source_root / package_rel / "package.json"
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    if not isinstance(data, dict):
        return ()
    entries: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for section in _PACKAGE_DEPENDENCY_SECTIONS:
        dependencies = data.get(section)
        if not isinstance(dependencies, dict):
            continue
        for raw_name, raw_specifier in dependencies.items():
            name = _normalize_package_dependency_name(raw_name)
            if name is None:
                continue
            key = (section, name)
            if key in seen:
                continue
            seen.add(key)
            entries.append({
                "name": name,
                "specifier": str(raw_specifier or ""),
                "section": section,
            })
    return tuple(entries)


def _normalize_package_dependency_name(value: object) -> str | None:
    text = str(value or "").strip().replace("\\", "/")
    if not text or any(ord(character) < 32 or ord(character) == 127 for character in text):
        return None
    parts = text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return None
    if text.startswith("@"):
        return text if len(parts) == 2 else None
    return text if len(parts) == 1 else None


def _dependency_root_contains_declared_package(
    dependency_root: Path,
    package_names: frozenset[str],
) -> bool:
    return any(
        (dependency_root / package_name).exists()
        or (dependency_root / package_name).is_symlink()
        for package_name in package_names
    )


def _materialize_local_file_package_sources(
    source_root: Path,
    workspace_root: Path,
    package_rel: str,
    dependency_entries: tuple[dict[str, str], ...],
    *,
    copied_package_roots: set[str],
) -> tuple[list[dict[str, Any]], int]:
    records: list[dict[str, Any]] = []
    copied_files: set[str] = set()
    package_source = source_root / package_rel
    for entry in dependency_entries:
        target = _local_file_dependency_target(
            source_root,
            package_source,
            str(entry["specifier"]),
        )
        if target is None:
            continue
        target_rel = target.relative_to(source_root).as_posix()
        if target_rel in copied_package_roots:
            continue
        copied_package_roots.add(target_rel)
        before = len(copied_files)
        _copy_materialized_directory(
            target,
            workspace_root / target_rel,
            source_root=source_root,
            workspace_root=workspace_root,
            copied_files=copied_files,
            clean=True,
        )
        copied_count = len(copied_files) - before
        records.append({
            "package_name": entry["name"],
            "dependency_section": entry["section"],
            "source_package_relative": package_rel,
            "local_package_source_relative": target_rel,
            "scratch_local_package_source": str(workspace_root / target_rel),
            "copied_file_count": copied_count,
            "dependency_install_performed": False,
        })
    return records, len(copied_files)


def _local_file_dependency_target(
    source_root: Path,
    package_source: Path,
    specifier: str,
) -> Path | None:
    text = str(specifier or "").strip()
    if not text.casefold().startswith(_LOCAL_FILE_DEPENDENCY_PREFIX):
        return None
    raw_target = text[len(_LOCAL_FILE_DEPENDENCY_PREFIX) :].strip()
    if not raw_target:
        return None
    target_path = Path(raw_target)
    if not target_path.is_absolute():
        target_path = package_source / target_path
    try:
        target = target_path.resolve(strict=True)
        target.relative_to(source_root)
    except (OSError, RuntimeError, ValueError):
        return None
    if not target.is_dir() or not (target / "package.json").is_file():
        return None
    return target


def _dependency_module_name_from_relative_path(relative_path: str) -> str | None:
    parts = tuple(part for part in relative_path.replace("\\", "/").split("/") if part)
    if not parts:
        return None
    if parts[0].startswith("@"):
        return "/".join(parts[:2]) if len(parts) >= 2 else None
    return parts[0]


def _normalize_dependency_root_relative_path(value: str) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if not text or text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        raise ProductRuntimeConflict("dependency substrate path must be repository-relative")
    if any(ord(character) < 32 or ord(character) == 127 for character in text):
        raise ProductRuntimeConflict("dependency substrate path contains control characters")
    parts = text.split("/")
    lowered = tuple(part.casefold() for part in parts)
    if any(part in {"", ".", ".."} for part in parts):
        raise ProductRuntimeConflict("dependency substrate path contains traversal")
    if lowered[-1] != "node_modules":
        raise ProductRuntimeConflict("dependency substrate path must target node_modules")
    if any(part in _SCRATCH_DEPENDENCY_PROTECTED_DIR_NAMES for part in lowered[:-1]):
        raise ProductRuntimeConflict("dependency substrate path targets a protected root")
    return text


def _copy_dependency_substrate_root(
    source_dependency_root: Path,
    scratch_dependency_root: Path,
    *,
    source_root: Path,
    workspace_root: Path,
    package_rel: str,
    authority: Any,
    required_package_names: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    from hermes_cli.agent_platform.runtime_adapter.path_containment import is_reparse_or_symlink

    started = time.perf_counter()
    if is_reparse_or_symlink(source_dependency_root):
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_SOURCE_NOT_FOUND,
            "dependency source root is a symlink or reparse point",
        )
    try:
        source_dependency_root.resolve(strict=True).relative_to(source_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_SOURCE_NOT_FOUND,
            "dependency source root escapes canonical source root",
        ) from exc
    if not source_dependency_root.is_dir():
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_SOURCE_NOT_FOUND,
            "dependency source root is not a directory",
        )
    _remove_materialized_destination(scratch_dependency_root, workspace_root=workspace_root)
    _ensure_materialized_directory(scratch_dependency_root, workspace_root=workspace_root)

    copied_files = 0
    copied_dirs = 1
    copied_bytes = 0
    excluded_dirs: set[str] = set()
    excluded_reparse_dirs: list[dict[str, str]] = []
    materialized_reparse_dirs: list[dict[str, str]] = []
    try:
        for root, dirnames, filenames in os.walk(source_dependency_root):
            root_path = Path(root)
            rel_root = root_path.relative_to(source_dependency_root).as_posix()
            kept_dirnames: list[str] = []
            for dirname in dirnames:
                child = root_path / dirname
                child_rel = child.relative_to(source_dependency_root).as_posix()
                if dirname in _SCRATCH_DEPENDENCY_EXCLUDED_DIR_NAMES:
                    excluded_dirs.add(child_rel)
                    continue
                if is_reparse_or_symlink(child):
                    try:
                        target = child.resolve(strict=True)
                        target.relative_to(source_root)
                    except (OSError, RuntimeError, ValueError) as exc:
                        raise ProductRuntimeDependencyGap(
                            DEPENDENCY_MATERIALIZATION_FAILED,
                            "dependency source contains an unsafe reparse point",
                        ) from exc
                    try:
                        target.relative_to(source_dependency_root)
                    except ValueError:
                        package_name = _dependency_module_name_from_relative_path(child_rel)
                        if package_name in required_package_names:
                            (
                                reparse_files,
                                reparse_dirs,
                                reparse_bytes,
                            ) = _copy_dependency_reparse_directory_as_physical_snapshot(
                                target,
                                scratch_dependency_root / child_rel,
                                source_root=source_root,
                                workspace_root=workspace_root,
                            )
                            copied_files += reparse_files
                            copied_dirs += reparse_dirs
                            copied_bytes += reparse_bytes
                            materialized_reparse_dirs.append({
                                "relative_path": child_rel,
                                "resolved_target": str(target),
                                "reason": "required_workspace_package_reparse_point_materialized_as_physical_copy",
                            })
                        else:
                            excluded_dirs.add(child_rel)
                            excluded_reparse_dirs.append({
                                "relative_path": child_rel,
                                "resolved_target": str(target),
                                "reason": "workspace_package_reparse_point_excluded",
                            })
                        continue
                    raise ProductRuntimeDependencyGap(
                        DEPENDENCY_MATERIALIZATION_FAILED,
                        "dependency source contains a reparse point inside node_modules",
                    )
                kept_dirnames.append(dirname)
            dirnames[:] = kept_dirnames
            dest_root = (
                scratch_dependency_root
                if rel_root == "."
                else scratch_dependency_root / rel_root
            )
            _ensure_materialized_directory(dest_root, workspace_root=workspace_root)
            copied_dirs += len(kept_dirnames)
            for filename in filenames:
                source_file = root_path / filename
                if is_reparse_or_symlink(source_file):
                    raise ProductRuntimeDependencyGap(
                        DEPENDENCY_MATERIALIZATION_FAILED,
                        "dependency source contains a symlinked file",
                    )
                dest_file = dest_root / filename
                _assert_materialized_destination(dest_file, workspace_root=workspace_root)
                size = source_file.stat().st_size
                shutil.copy2(source_file, dest_file)
                copied_files += 1
                copied_bytes += size
    except ProductRuntimeDependencyGap:
        raise
    except Exception as exc:
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_MATERIALIZATION_FAILED,
            "dependency substrate physical copy failed",
        ) from exc

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    source_rel = source_dependency_root.relative_to(source_root).as_posix()
    scratch_rel = scratch_dependency_root.relative_to(workspace_root).as_posix()
    package_json = source_root / package_rel / "package.json"
    canonical_lock = source_root / "2_products/pepper-agent/package-lock.json"
    return {
        "schema_version": 1,
        "policy_id": PEPPER_SCRATCH_DEPENDENCY_SUBSTRATE_POLICY_ID,
        "dependency_substrate_kind": "physical_node_modules_snapshot",
        "created_at": _utc_now_iso(),
        "ticket_id": authority.ticket_id,
        "work_packet_id": authority.work_packet_id,
        "work_packet_SHA256": authority.work_packet_SHA256,
        "projection_SHA256": authority.projection_SHA256,
        "package_relative_path": package_rel,
        "canonical_dependency_root": str(source_dependency_root),
        "canonical_dependency_root_relative": source_rel,
        "scratch_dependency_root": str(scratch_dependency_root),
        "scratch_dependency_root_relative": scratch_rel,
        "source_package_json_SHA256": _sha256_file_or_none(package_json),
        "canonical_package_lock_SHA256": _sha256_file_or_none(canonical_lock),
        "dependency_sentinel_SHA256": _dependency_sentinel_hashes(source_dependency_root),
        "scratch_dependency_sentinel_SHA256": _dependency_sentinel_hashes(scratch_dependency_root),
        "copied_file_count": copied_files,
        "copied_directory_count": copied_dirs,
        "copied_bytes": copied_bytes,
        "elapsed_ms": elapsed_ms,
        "excluded_directories": sorted(excluded_dirs),
        "excluded_reparse_directories": sorted(
            excluded_reparse_dirs,
            key=lambda item: item["relative_path"],
        ),
        "materialized_reparse_directories": sorted(
            materialized_reparse_dirs,
            key=lambda item: item["relative_path"],
        ),
        "dependency_install_performed": False,
        "canonical_package_lock_materialized": False,
    }


def _copy_dependency_reparse_directory_as_physical_snapshot(
    source_dir: Path,
    destination_dir: Path,
    *,
    source_root: Path,
    workspace_root: Path,
) -> tuple[int, int, int]:
    from hermes_cli.agent_platform.runtime_adapter.path_containment import is_reparse_or_symlink

    try:
        source = source_dir.resolve(strict=True)
        source.relative_to(source_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_MATERIALIZATION_FAILED,
            "workspace dependency reparse target escapes canonical source root",
        ) from exc
    if not source.is_dir():
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_MATERIALIZATION_FAILED,
            "workspace dependency reparse target is not a directory",
        )

    _remove_materialized_destination(destination_dir, workspace_root=workspace_root)
    _ensure_materialized_directory(destination_dir, workspace_root=workspace_root)

    copied_files = 0
    copied_dirs = 1
    copied_bytes = 0
    try:
        for root, dirnames, filenames in os.walk(source):
            root_path = Path(root)
            rel_snapshot = root_path.relative_to(source).as_posix()
            kept_dirnames: list[str] = []
            for dirname in dirnames:
                child = root_path / dirname
                child_rel = child.relative_to(source_root).as_posix()
                if dirname in _SCRATCH_DEPENDENCY_EXCLUDED_DIR_NAMES:
                    continue
                if _should_skip_materialized_relative_path(child_rel, is_dir=True):
                    continue
                if is_reparse_or_symlink(child):
                    raise ProductRuntimeDependencyGap(
                        DEPENDENCY_MATERIALIZATION_FAILED,
                        "workspace dependency source contains a reparse point",
                    )
                kept_dirnames.append(dirname)
            dirnames[:] = kept_dirnames
            dest_root = destination_dir if rel_snapshot == "." else destination_dir / rel_snapshot
            _ensure_materialized_directory(dest_root, workspace_root=workspace_root)
            copied_dirs += len(kept_dirnames)
            for filename in filenames:
                source_file = root_path / filename
                source_rel = source_file.relative_to(source_root).as_posix()
                if _should_skip_materialized_relative_path(source_rel, is_dir=False):
                    continue
                if is_reparse_or_symlink(source_file):
                    raise ProductRuntimeDependencyGap(
                        DEPENDENCY_MATERIALIZATION_FAILED,
                        "workspace dependency source contains a symlinked file",
                    )
                dest_file = dest_root / filename
                _assert_materialized_destination(dest_file, workspace_root=workspace_root)
                size = source_file.stat().st_size
                shutil.copy2(source_file, dest_file)
                copied_files += 1
                copied_bytes += size
    except ProductRuntimeDependencyGap:
        raise
    except Exception as exc:
        raise ProductRuntimeDependencyGap(
            DEPENDENCY_MATERIALIZATION_FAILED,
            "workspace dependency physical copy failed",
        ) from exc
    return copied_files, copied_dirs, copied_bytes


def _sha256_file_or_none(path: Path) -> str | None:
    try:
        if not path.is_file():
            return None
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def _dependency_sentinel_hashes(dependency_root: Path) -> dict[str, str | None]:
    return {
        entry: _sha256_file_or_none(dependency_root / entry)
        for entry in _FRONTEND_DEPENDENCY_SENTINEL_ENTRIES
    }


def _materialize_workpacket_scratch_source_tree(
    authority: Any,
    *,
    source_root: Path | str | None = None,
) -> dict[str, Any]:
    """Copy bounded readable source into scratch while preserving write scope."""

    source = Path(source_root).expanduser() if source_root is not None else _agent_platform_repository_root()
    try:
        resolved_source = source.resolve(strict=True)
    except OSError as exc:
        raise ProductRuntimeConflict("canonical source root is unavailable") from exc
    if not resolved_source.is_dir():
        raise ProductRuntimeConflict("canonical source root is not a directory")
    workspace = Path(authority.resolved_workspace_root).resolve(strict=True)
    if not workspace.is_dir():
        raise ProductRuntimeConflict("scratch workspace root is not a directory")
    try:
        workspace.relative_to(resolved_source)
    except ValueError:
        pass
    else:
        raise ProductRuntimeConflict("scratch workspace must not be inside canonical source root")

    copied_files: set[str] = set()
    materialized_roots: set[str] = set()
    readable_roots: set[str] = set()
    cleaned_roots: set[str] = set()
    package_closures: set[str] = set()
    missing_paths: set[str] = set()

    for package in _selected_scratch_source_package_closures(authority.allowed_paths):
        package_rel = str(package["package_rel"])
        package_source = resolved_source / package_rel
        if not package_source.is_dir():
            missing_paths.add(package_rel)
            continue
        package_closures.add(package_rel)
        for dirname in tuple(package["source_dirs"]):
            rel = _normalize_materialization_relative_path(f"{package_rel}/{dirname}")
            src = resolved_source / rel
            if not src.is_dir():
                continue
            _copy_materialized_directory(
                src,
                workspace / rel,
                source_root=resolved_source,
                workspace_root=workspace,
                copied_files=copied_files,
                clean=True,
            )
            materialized_roots.add(rel)
            readable_roots.add(rel)
            cleaned_roots.add(rel)
        for filename in tuple(package["support_files"]):
            rel = _normalize_materialization_relative_path(f"{package_rel}/{filename}")
            src = resolved_source / rel
            if not src.is_file():
                continue
            _copy_materialized_file(
                src,
                workspace / rel,
                source_root=resolved_source,
                workspace_root=workspace,
                copied_files=copied_files,
            )
            materialized_roots.add(rel)
            readable_roots.add(package_rel)

    for pattern in authority.allowed_paths:
        _materialize_allowed_source_pattern(
            str(pattern),
            source_root=resolved_source,
            workspace_root=workspace,
            copied_files=copied_files,
            materialized_roots=materialized_roots,
            readable_roots=readable_roots,
            cleaned_roots=cleaned_roots,
            missing_paths=missing_paths,
        )

    manifest_path = workspace / PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    record = {
        "policy_id": PEPPER_SCRATCH_SOURCE_MATERIALIZATION_POLICY_ID,
        "created_at": _utc_now_iso(),
        "ticket_id": authority.ticket_id,
        "work_packet_id": authority.work_packet_id,
        "work_packet_SHA256": authority.work_packet_SHA256,
        "ticket_spec_SHA256": authority.ticket_spec_SHA256,
        "projection_SHA256": authority.projection_SHA256,
        "source_materialized": True,
        "source_root": str(resolved_source),
        "workspace_root": str(workspace),
        "manifest_path": str(manifest_path),
        "readable_source_roots": sorted(readable_roots),
        "writable_allowed_paths": list(authority.allowed_paths),
        "forbidden_paths": list(authority.forbidden_paths),
        "package_source_closures": sorted(package_closures),
        "materialized_roots": sorted(materialized_roots),
        "missing_source_paths": sorted(missing_paths),
        "copied_file_count": len(copied_files),
        "dependency_install_performed": False,
        "canonical_package_lock_materialized": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
    }
    _write_materialization_manifest(manifest_path, record, workspace_root=workspace)
    return record


def _selected_scratch_source_package_closures(
    allowed_paths: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    selected: list[dict[str, Any]] = []
    for package in _SCRATCH_SOURCE_PACKAGE_CLOSURES:
        package_rel = str(package["package_rel"])
        prefix = f"{package_rel}/"
        if any(str(path).strip() == package_rel or str(path).strip().startswith(prefix) for path in allowed_paths):
            selected.append(package)
    return tuple(selected)


def _materialize_allowed_source_pattern(
    pattern: str,
    *,
    source_root: Path,
    workspace_root: Path,
    copied_files: set[str],
    materialized_roots: set[str],
    readable_roots: set[str],
    cleaned_roots: set[str],
    missing_paths: set[str],
) -> None:
    rel_pattern = _normalize_materialization_relative_path(pattern)
    if rel_pattern.endswith("/**"):
        rel_dir = rel_pattern[:-3]
        src = source_root / rel_dir
        dest = workspace_root / rel_dir
        clean = not _relative_path_under_any_root(rel_dir, cleaned_roots)
        if src.is_dir():
            _copy_materialized_directory(
                src,
                dest,
                source_root=source_root,
                workspace_root=workspace_root,
                copied_files=copied_files,
                clean=clean,
            )
            materialized_roots.add(rel_dir)
            readable_roots.add(rel_dir)
            if clean:
                cleaned_roots.add(rel_dir)
        else:
            if clean:
                _remove_materialized_destination(dest, workspace_root=workspace_root)
            _ensure_materialized_directory(dest, workspace_root=workspace_root)
            materialized_roots.add(rel_dir)
            missing_paths.add(rel_dir)
        return

    if _contains_glob_pattern(rel_pattern):
        matches = sorted(source_root.glob(rel_pattern))
        if not matches:
            missing_paths.add(rel_pattern)
            return
        for src in matches:
            rel = src.relative_to(source_root).as_posix()
            if _should_skip_materialized_relative_path(rel, is_dir=src.is_dir()):
                continue
            dest = workspace_root / rel
            if src.is_dir():
                _copy_materialized_directory(
                    src,
                    dest,
                    source_root=source_root,
                    workspace_root=workspace_root,
                    copied_files=copied_files,
                    clean=not _relative_path_under_any_root(rel, cleaned_roots),
                )
                materialized_roots.add(rel)
                readable_roots.add(rel)
            elif src.is_file():
                _copy_materialized_file(
                    src,
                    dest,
                    source_root=source_root,
                    workspace_root=workspace_root,
                    copied_files=copied_files,
                )
                materialized_roots.add(rel)
                readable_roots.add(str(Path(rel).parent).replace("\\", "/"))
        return

    src = source_root / rel_pattern
    dest = workspace_root / rel_pattern
    if src.is_dir():
        clean = not _relative_path_under_any_root(rel_pattern, cleaned_roots)
        _copy_materialized_directory(
            src,
            dest,
            source_root=source_root,
            workspace_root=workspace_root,
            copied_files=copied_files,
            clean=clean,
        )
        materialized_roots.add(rel_pattern)
        readable_roots.add(rel_pattern)
        if clean:
            cleaned_roots.add(rel_pattern)
    elif src.is_file():
        _copy_materialized_file(
            src,
            dest,
            source_root=source_root,
            workspace_root=workspace_root,
            copied_files=copied_files,
        )
        materialized_roots.add(rel_pattern)
        readable_roots.add(str(Path(rel_pattern).parent).replace("\\", "/"))
    else:
        _remove_materialized_destination(dest, workspace_root=workspace_root)
        _ensure_materialized_directory(dest.parent, workspace_root=workspace_root)
        missing_paths.add(rel_pattern)


def _normalize_materialization_relative_path(value: str) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if not text or text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        raise ProductRuntimeConflict("source materialization path must be repository-relative")
    if any(ord(character) < 32 or ord(character) == 127 for character in text):
        raise ProductRuntimeConflict("source materialization path contains control characters")
    parts = text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ProductRuntimeConflict("source materialization path contains traversal")
    if _should_skip_materialized_relative_path(text, is_dir=text.endswith("/**")):
        raise ProductRuntimeConflict("source materialization path targets a protected root")
    return text


def _contains_glob_pattern(value: str) -> bool:
    return any(marker in value for marker in ("*", "?", "["))


def _relative_path_under_any_root(relative_path: str, roots: set[str]) -> bool:
    rel = relative_path.strip("/")
    return any(rel == root or rel.startswith(f"{root.rstrip('/')}/") for root in roots)


def _should_skip_materialized_relative_path(relative_path: str, *, is_dir: bool) -> bool:
    rel = relative_path.replace("\\", "/").strip("/")
    parts = tuple(part.casefold() for part in rel.split("/") if part)
    if any(part in _SCRATCH_SOURCE_SKIP_DIR_NAMES for part in parts):
        return True
    if parts and parts[-1] == "package-lock.json":
        return True
    if rel == "AGENTS.md" or rel.startswith("4_external/sources/"):
        return True
    if rel == "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json":
        return True
    return (not is_dir) and Path(rel).suffix in _SCRATCH_SOURCE_SKIP_FILE_SUFFIXES


def _copy_materialized_directory(
    source_dir: Path,
    destination_dir: Path,
    *,
    source_root: Path,
    workspace_root: Path,
    copied_files: set[str],
    clean: bool,
) -> None:
    _assert_materialized_source(source_dir, source_root=source_root, expect_dir=True)
    if clean:
        _remove_materialized_destination(destination_dir, workspace_root=workspace_root)
    _ensure_materialized_directory(destination_dir, workspace_root=workspace_root)
    for root, dirnames, filenames in os.walk(source_dir):
        root_path = Path(root)
        rel_root = root_path.relative_to(source_root).as_posix()
        kept_dirnames: list[str] = []
        for dirname in dirnames:
            child = root_path / dirname
            child_rel = child.relative_to(source_root).as_posix()
            if _should_skip_materialized_relative_path(child_rel, is_dir=True):
                continue
            if child.is_symlink():
                raise ProductRuntimeConflict("source materialization refuses symlinked directories")
            kept_dirnames.append(dirname)
        dirnames[:] = kept_dirnames
        _ensure_materialized_directory(
            workspace_root / rel_root,
            workspace_root=workspace_root,
        )
        for filename in filenames:
            child = root_path / filename
            child_rel = child.relative_to(source_root).as_posix()
            if _should_skip_materialized_relative_path(child_rel, is_dir=False):
                continue
            _copy_materialized_file(
                child,
                workspace_root / child_rel,
                source_root=source_root,
                workspace_root=workspace_root,
                copied_files=copied_files,
            )


def _copy_materialized_file(
    source_file: Path,
    destination_file: Path,
    *,
    source_root: Path,
    workspace_root: Path,
    copied_files: set[str],
) -> None:
    _assert_materialized_source(source_file, source_root=source_root, expect_dir=False)
    _ensure_materialized_directory(destination_file.parent, workspace_root=workspace_root)
    _assert_materialized_destination(destination_file, workspace_root=workspace_root)
    if destination_file.is_symlink():
        raise ProductRuntimeConflict("source materialization refuses symlinked scratch paths")
    if destination_file.exists() and destination_file.is_dir():
        _remove_materialized_destination(destination_file, workspace_root=workspace_root)
    shutil.copy2(source_file, destination_file)
    copied_files.add(destination_file.relative_to(workspace_root).as_posix())


def _assert_materialized_source(
    path: Path,
    *,
    source_root: Path,
    expect_dir: bool,
) -> None:
    if path.is_symlink():
        raise ProductRuntimeConflict("source materialization refuses symlinked source paths")
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(source_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ProductRuntimeConflict("source materialization path escapes canonical source root") from exc
    if expect_dir and not resolved.is_dir():
        raise ProductRuntimeConflict("source materialization expected a directory")
    if not expect_dir and not resolved.is_file():
        raise ProductRuntimeConflict("source materialization expected a file")


def _assert_materialized_destination(path: Path, *, workspace_root: Path) -> None:
    if path == workspace_root:
        raise ProductRuntimeConflict("source materialization refuses workspace root mutation")
    try:
        path.resolve(strict=False).relative_to(workspace_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ProductRuntimeConflict("source materialization destination escapes scratch workspace") from exc


def _ensure_materialized_directory(path: Path, *, workspace_root: Path) -> None:
    if path == workspace_root:
        if not path.is_dir():
            raise ProductRuntimeConflict("scratch workspace root is not a directory")
        return
    _assert_materialized_destination(path, workspace_root=workspace_root)
    if path.exists() and not path.is_dir():
        _remove_materialized_destination(path, workspace_root=workspace_root)
    path.mkdir(parents=True, exist_ok=True)


def _remove_materialized_destination(path: Path, *, workspace_root: Path) -> None:
    _assert_materialized_destination(path, workspace_root=workspace_root)
    if not path.exists() and not path.is_symlink():
        return
    try:
        path.resolve(strict=True).relative_to(workspace_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ProductRuntimeConflict("source materialization destination escapes scratch workspace") from exc
    if path.is_symlink():
        raise ProductRuntimeConflict("source materialization refuses symlinked scratch paths")
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _write_materialization_manifest(
    manifest_path: Path,
    record: dict[str, Any],
    *,
    workspace_root: Path,
) -> None:
    _ensure_materialized_directory(manifest_path.parent, workspace_root=workspace_root)
    _assert_materialized_destination(manifest_path, workspace_root=workspace_root)
    manifest_path.write_text(
        json.dumps(record, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


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
        source_materialization = None
        if _projection_requires_scratch_source_materialization(projection):
            try:
                source_materialization = _materialize_pepper_governed_scratch_source(
                    projection,
                    workspace,
                    env_overlay=env_overlay,
                )
            except ProductRuntimeDependencyGap as exc:
                detail = f"{exc.dependency_code}: {_safe_text(str(exc), limit=240)}"
                kanban_db._record_spawn_failure(
                    conn,
                    claimed.id,
                    f"dependency substrate: {detail}",
                    failure_limit=1,
                )
                task = kanban_db.get_task(conn, task_id)
                runs = kanban_db.list_runs(conn, task_id) if task is not None else []
                return _dispatch_blocked_result(
                    exc.external_code,
                    detail,
                    task=task,
                    runs=runs,
                    dispatch_performed=True,
                )
            except Exception as exc:
                kanban_db._record_spawn_failure(
                    conn,
                    claimed.id,
                    f"source materialization: {_safe_text(exc, limit=300)}",
                    failure_limit=1,
                )
                task = kanban_db.get_task(conn, task_id)
                runs = kanban_db.list_runs(conn, task_id) if task is not None else []
                return _dispatch_blocked_result(
                    "WORKSPACE_SOURCE_MATERIALIZATION_FAILED",
                    str(exc) or "scratch source materialization failed",
                    task=task,
                    runs=runs,
                    dispatch_performed=True,
                )
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
            "source_materialized": source_materialization is not None,
            "source_materialization": source_materialization,
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
            f"Authorize {binding.ticket_id} retry-pending governance after failed run "
            f"{retry_source.get('latest_run_id')} without starting attempt "
            f"{retry_source.get('next_attempt_number')} or mutating Kanban."
        ),
        authorized_at=observed_at,
    )
    observed_attempt_count = int(retry_source["observed_attempt_count"])
    max_attempts = int(retry_source["max_attempts"])
    next_attempt_number = int(retry_source["next_attempt_number"])
    recovery_cycle_id = _governed_ticket_recovery_cycle_id(
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


def _build_governed_autonomy_activation_record(
    *,
    request: CurrentTicketGovernedAutonomyActivationRequest,
    projection: dict[str, Any],
    workflow: dict[str, Any],
) -> dict[str, Any]:
    authority_reference = _derive_current_governed_autonomy_authority_reference(projection)
    budget_reference = _validated_governed_autonomy_budget_reference(
        authority_reference["budget"]
    )
    authority_view = _governed_autonomy_authority_view_from_reference(
        authority_reference,
        projection=projection,
    )
    same_authority = _governed_autonomy_same_authority_subset(projection, authority_view)
    if not same_authority["same_authority"]:
        raise ProductRuntimeAuthorityMismatch(
            "governed-autonomy backend authority mismatch",
            diagnostics=same_authority,
        )
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    current_next_action = workflow.get("next_action")
    record = {
        "schema_version": PEPPER_GOVERNED_AUTONOMY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_ACTION_POLICY_ID,
        "source_system": PEPPER_GOVERNED_AUTONOMY_ACTION_SOURCE_SYSTEM,
        "created_at": _utc_now_iso(),
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "authorizer_id": request.authorizer_id,
        "human_request_text": request.human_request_text,
        "requested_action": "record_governed_autonomy_activation_status",
        "current_workflow_status": workflow.get("workflow_status"),
        "current_recovery_state": workflow.get("recovery_state"),
        "current_next_action_id": (
            current_next_action.get("id") if isinstance(current_next_action, dict) else None
        ),
        "governed_autonomy_policy_id": authority_reference["policy_id"],
        "governed_autonomy_envelope_SHA256": authority_reference["envelope_SHA256"],
        "governed_autonomy_budget": budget_reference,
        "governed_autonomy_envelope_reference": authority_reference,
        "backend_derived_live_authority_SHA256": authority_reference["envelope_SHA256"],
        "backend_derived_live_authority_reference": authority_reference,
        "authority_derivation_source": "server_side_current_ticket_projection_and_kanban_run",
        "01AH_envelope_lifecycle_classification": authority_reference[
            "01AH_envelope_lifecycle_classification"
        ],
        "governed_autonomy_activation_recorded": True,
        "governed_autonomy_status": "activation_recorded_live_lineage_blocked",
        "capability_gap_SHA256": None,
        "capability_gap_reference": None,
        "continuation_lineage_SHA256": None,
        "continuation_lineage_reference": None,
        "same_authority_subset_validated": True,
        "same_authority_subset": same_authority,
        "same_authority_delegation_policy_id": PEPPER_GOVERNED_AUTONOMY_A2A_POLICY_ID,
        "same_authority_delegation_status": "canonical_hermes_delegate_task_available_with_parent_agent",
        "same_authority_delegation_authorized": True,
        "same_authority_delegation_blocker_code": None,
        "same_authority_delegation_blocker_detail": (
            "Canonical Hermes delegate_task can run a bounded same-authority child when "
            "the tool invocation provides parent_agent context; otherwise continuation stops."
        ),
        "opencode_runtime_dispatcher_found": True,
        "delegate_task_runtime_kind": "canonical_hermes_delegate_task",
        "live_lineage_activation_authorized": True,
        "live_lineage_activation_status": "active_authority_ready_for_continuation",
        "live_lineage_activation_blocker_code": None,
        "live_lineage_activation_blocker_detail": (
            f"{binding.ticket_id} same-authority continuation may create exactly one new "
            "Kanban run through the canonical projected-task worker lifecycle while the "
            "backend-derived authority and active_execution_count=0 still match."
        ),
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "lineage_dispatch_performed": False,
        "A2A_dispatch_performed": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": PEPPER_GOVERNED_AUTONOMY_READY_MARKER,
    }
    record["activation_action_SHA256"] = _governed_autonomy_activation_record_digest(record)
    return record


def _select_governed_autonomy_runtime_decision(
    request: CurrentTicketGovernedAutonomyContinuationRequest,
) -> str:
    if request.strategy != "AUTO":
        return request.strategy
    if request.delegate_goal or request.delegate_paths or request.delegate_requested_operations:
        return "A2A_DELEGATION"
    if (
        request.task_local_tool_name
        or request.task_local_implementation_path
        or request.task_local_source_text
        or request.task_local_command
    ):
        return "TASK_LOCAL_SELF_EXTENSION"
    return "DIRECT"


def _governed_autonomy_runtime_budget_limits(
    activation: dict[str, Any],
) -> dict[str, int]:
    return _validated_governed_autonomy_budget_reference(
        activation.get("governed_autonomy_budget")
    )


def _runtime_counter(previous: dict[str, Any] | None, key: str) -> int:
    if previous is None:
        return 0
    return int(previous.get(key) or 0)


def _governed_autonomy_runtime_record_consumed_process(
    record: dict[str, Any] | None,
) -> bool:
    if not isinstance(record, dict):
        return False
    side_effects = record.get("current_invocation_side_effects")
    if not isinstance(side_effects, dict):
        side_effects = {}
    if any(
        side_effects.get(key) is True
        for key in (
            "dispatch_performed",
            "Kanban_dispatch",
            "execution_started",
            "worker_execution",
            "worker_process_started",
            "A2A_dispatch_performed",
        )
    ):
        return True
    if record.get("kanban_run_created") or record.get("lineage_dispatch_performed"):
        return True
    if (
        record.get("human_smoke_marker") == PEPPER_GOVERNED_AUTONOMY_READY_MARKER
        and _runtime_counter(record, "process_continuation_count") > 0
    ):
        return True
    return str(record.get("runtime_decision") or "") == "TASK_LOCAL_SELF_EXTENSION" and str(
        record.get("governed_autonomy_runtime_status") or ""
    ).startswith("task_local_self_extension")


def _effective_governed_autonomy_process_continuation_count(
    previous: dict[str, Any] | None,
) -> int:
    if previous is None:
        return 0
    if _governed_autonomy_runtime_record_consumed_process(previous):
        return _runtime_counter(previous, "process_continuation_count")
    return 0


def _governed_autonomy_runtime_budget_blocker(
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    *,
    requested_decision: str,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    fresh_execution_request_pending_replay: bool = False,
) -> tuple[str, str] | None:
    limits = _governed_autonomy_runtime_budget_limits(activation)
    if requested_decision != "STOP_FOR_HUMAN" and (
        _effective_governed_autonomy_process_continuation_count(previous) + 1
        > limits["max_continuations"]
    ):
        return "GOVERNED_AUTONOMY_PROCESS_CONTINUATION_BUDGET_EXHAUSTED", (
            "process continuation budget is exhausted"
        )
    if requested_decision == "TASK_LOCAL_SELF_EXTENSION":
        if _runtime_counter(previous, "self_repair_count") + 1 > limits["max_repair_attempts"]:
            return "GOVERNED_AUTONOMY_SELF_REPAIR_BUDGET_EXHAUSTED", (
                "task-local self-repair budget is exhausted"
            )
        if (
            _runtime_counter(previous, "task_local_tool_candidate_count") + 1
            > limits["max_tool_candidates"]
        ):
            return "GOVERNED_AUTONOMY_TOOL_CANDIDATE_BUDGET_EXHAUSTED", (
                "task-local helper candidate budget is exhausted"
            )
        if request.task_local_command and (
            _runtime_counter(previous, "command_evaluation_count") + 1
            > limits["max_command_evaluations"]
        ):
            return "GOVERNED_AUTONOMY_COMMAND_EVALUATION_BUDGET_EXHAUSTED", (
                "task-local command evaluation budget is exhausted"
            )
    if requested_decision == "A2A_DELEGATION":
        if _runtime_counter(previous, "A2A_delegation_count") + 1 > limits["max_tool_candidates"]:
            return "GOVERNED_AUTONOMY_A2A_DELEGATION_BUDGET_EXHAUSTED", (
                "A2A delegation budget is exhausted"
            )
    if (
        not fresh_execution_request_pending_replay
        and _runtime_counter(previous, "validation_failure_count")
        >= limits["max_no_progress_iterations"]
    ):
        return "GOVERNED_AUTONOMY_VALIDATION_FAILURE_BUDGET_EXHAUSTED", (
            "validation failure budget is exhausted"
        )
    return None


def _governed_autonomy_runtime_counts(
    previous: dict[str, Any] | None,
    *,
    process_continuation_increment: int = 1,
    self_repair_increment: int = 0,
    tool_candidate_increment: int = 0,
    command_evaluation_increment: int = 0,
    delegation_increment: int = 0,
    validation_failure_increment: int = 0,
) -> dict[str, int]:
    return {
        "process_continuation_count": (
            _effective_governed_autonomy_process_continuation_count(previous)
            + process_continuation_increment
        ),
        "self_repair_count": _runtime_counter(previous, "self_repair_count") + self_repair_increment,
        "task_local_tool_candidate_count": (
            _runtime_counter(previous, "task_local_tool_candidate_count") + tool_candidate_increment
        ),
        "command_evaluation_count": (
            _runtime_counter(previous, "command_evaluation_count") + command_evaluation_increment
        ),
        "A2A_delegation_count": _runtime_counter(previous, "A2A_delegation_count") + delegation_increment,
        "validation_failure_count": (
            _runtime_counter(previous, "validation_failure_count") + validation_failure_increment
        ),
    }


def _governed_autonomy_runtime_budget_remaining(
    limits: dict[str, int],
    counts: dict[str, int],
    *,
    no_progress_count: int,
) -> dict[str, int]:
    return {
        "process_continuations": max(
            0,
            limits["max_continuations"] - counts["process_continuation_count"],
        ),
        "self_repairs": max(0, limits["max_repair_attempts"] - counts["self_repair_count"]),
        "task_local_tool_candidates": max(
            0,
            limits["max_tool_candidates"] - counts["task_local_tool_candidate_count"],
        ),
        "command_evaluations": max(
            0,
            limits["max_command_evaluations"] - counts["command_evaluation_count"],
        ),
        "A2A_delegations": max(
            0,
            limits["max_tool_candidates"] - counts["A2A_delegation_count"],
        ),
        "validation_failures": max(
            0,
            limits["max_no_progress_iterations"] - counts["validation_failure_count"],
        ),
        "no_progress_iterations": max(
            0,
            limits["max_no_progress_iterations"] - no_progress_count,
        ),
    }


def _governed_autonomy_runtime_budget_exhausted(
    limits: dict[str, int],
    counts: dict[str, int],
    *,
    no_progress_count: int,
) -> bool:
    return (
        counts["process_continuation_count"] >= limits["max_continuations"]
        or counts["self_repair_count"] >= limits["max_repair_attempts"]
        or counts["task_local_tool_candidate_count"] >= limits["max_tool_candidates"]
        or counts["command_evaluation_count"] >= limits["max_command_evaluations"]
        or counts["A2A_delegation_count"] >= limits["max_tool_candidates"]
        or counts["validation_failure_count"] >= limits["max_no_progress_iterations"]
        or no_progress_count >= limits["max_no_progress_iterations"]
    )


def _governed_autonomy_runtime_fingerprint(
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    *,
    runtime_decision: str,
) -> str:
    return _digest_payload(
        "pepper-governed-autonomy-runtime-no-progress-fingerprint-v1",
        {
            "runtime_decision": runtime_decision,
            "runtime_goal": request.runtime_goal,
            "observed_failure": request.observed_failure,
            "requested_capability": request.requested_capability,
            "task_local_tool_name": request.task_local_tool_name,
            "task_local_implementation_path": request.task_local_implementation_path,
            "task_local_source_SHA256": (
                hashlib.sha256(request.task_local_source_text.encode("utf-8")).hexdigest()
                if request.task_local_source_text
                else None
            ),
            "task_local_command": request.task_local_command,
            "delegate_goal": request.delegate_goal,
            "delegate_paths": list(request.delegate_paths),
            "delegate_requested_operations": list(request.delegate_requested_operations),
            "fresh_execution_request_text_SHA256": (
                hashlib.sha256(request.fresh_execution_request_text.encode("utf-8")).hexdigest()
                if request.fresh_execution_request_text
                else None
            ),
        },
    )


def _governed_autonomy_runtime_no_progress(
    previous: dict[str, Any] | None,
    *,
    fingerprint_sha256: str,
    progress_marker_sha256: str | None,
) -> tuple[int, list[str]]:
    previous_markers = list(previous.get("progress_marker_SHA256s") or []) if previous else []
    if progress_marker_sha256 and progress_marker_sha256 not in previous_markers:
        return 0, [*previous_markers, progress_marker_sha256]
    if previous and previous.get("latest_no_progress_fingerprint_SHA256") == fingerprint_sha256:
        return int(previous.get("no_progress_count") or 0) + 1, previous_markers
    return 0, previous_markers


def _governed_autonomy_runtime_source_run(
    projection: dict[str, Any],
) -> dict[str, Any]:
    _task_visibility, runs = _governed_autonomy_kanban_visibility({
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
    })
    latest = runs[-1] if runs else None
    return {
        "source_run_id": latest.get("id") if isinstance(latest, dict) else None,
        "source_run_status": latest.get("status") if isinstance(latest, dict) else None,
        "source_run_outcome": latest.get("outcome") if isinstance(latest, dict) else None,
        "historical_source_run_immutable": True,
    }


def _governed_autonomy_activation_source_run(
    activation: dict[str, Any],
) -> dict[str, Any]:
    reference = activation.get("governed_autonomy_envelope_reference")
    if not isinstance(reference, dict):
        return {
            "source_run_id": None,
            "source_run_status": None,
            "source_run_outcome": None,
            "historical_source_run_immutable": True,
        }
    return {
        "source_run_id": reference.get("source_run_id"),
        "source_run_status": reference.get("source_run_status"),
        "source_run_outcome": reference.get("source_run_outcome"),
        "historical_source_run_immutable": True,
    }


def _governed_autonomy_active_execution_replay(
    previous: dict[str, Any] | None,
    projection: dict[str, Any],
) -> bool:
    if previous is None or previous.get("runtime_decision") != "DIRECT":
        return False
    if not previous.get("kanban_run_created") or not previous.get("execution_started"):
        return False
    run_id = _int_or_none(previous.get("kanban_run_id"))
    if run_id is None:
        return False
    task_visibility, runs = _governed_autonomy_kanban_visibility(projection)
    if isinstance(task_visibility, dict):
        if (
            _int_or_none(task_visibility.get("current_run_id")) == run_id
            and str(task_visibility.get("status") or "").strip().lower() == "running"
        ):
            return True
    for run in runs:
        if _int_or_none(run.get("id")) == run_id:
            return _execution_is_active(run)
    return False


def _governed_autonomy_materialization_manifest(
    workspace_path: object,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if not workspace_path:
        return None, None
    manifest_path = Path(str(workspace_path)) / PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, {
            "available": False,
            "manifest_path": str(manifest_path),
        }
    if not isinstance(manifest, dict):
        return None, {
            "available": False,
            "manifest_path": str(manifest_path),
        }
    reference = {
        "available": True,
        "manifest_path": _safe_text(
            manifest.get("manifest_path") or manifest_path,
            limit=500,
        ),
    }
    for key in (
        "policy_id",
        "source_materialized",
        "copied_file_count",
        "dependency_substrate_materialized",
        "dependency_substrate_kind",
        "dependency_substrate_copied_file_count",
        "dependency_substrate_copied_directory_count",
        "dependency_install_performed",
        "canonical_package_lock_materialized",
        "missing_source_paths",
        "product_diff_excluded_roots",
    ):
        if key in manifest:
            reference[key] = manifest.get(key)
    canonical_lock_sha = manifest.get("canonical_package_lock_SHA256")
    if not canonical_lock_sha:
        substrates = manifest.get("dependency_substrates")
        if isinstance(substrates, list):
            for substrate in substrates:
                if isinstance(substrate, dict) and substrate.get(
                    "canonical_package_lock_SHA256"
                ):
                    canonical_lock_sha = substrate.get("canonical_package_lock_SHA256")
                    break
    reference["canonical_package_lock_SHA256"] = canonical_lock_sha
    return manifest, reference


def _governed_autonomy_candidate_files_for_pattern(
    root: Path,
    pattern: object,
) -> set[str]:
    try:
        rel_pattern = _normalize_materialization_relative_path(str(pattern or ""))
    except ProductRuntimeConflict:
        return set()
    matches: set[str] = set()
    try:
        if rel_pattern.endswith("/**"):
            base = root / rel_pattern[:-3]
            if base.is_file():
                return {base.relative_to(root).as_posix()}
            if base.is_dir():
                for path in base.rglob("*"):
                    if path.is_file():
                        matches.add(path.relative_to(root).as_posix())
            return matches
        if _contains_glob_pattern(rel_pattern):
            for path in root.glob(rel_pattern):
                if path.is_file():
                    matches.add(path.relative_to(root).as_posix())
            return matches
        path = root / rel_pattern
        if path.is_file():
            return {rel_pattern}
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    matches.add(child.relative_to(root).as_posix())
    except (OSError, RuntimeError, ValueError):
        return matches
    return matches


def _governed_autonomy_candidate_diff_excluded(
    relative_path: str,
    *,
    excluded_roots: tuple[str, ...],
) -> bool:
    rel = str(relative_path or "").replace("\\", "/").strip("/")
    if not rel:
        return True
    try:
        if _should_skip_materialized_relative_path(rel, is_dir=False):
            return True
    except ProductRuntimeConflict:
        return True
    for root in excluded_roots:
        normalized = str(root or "").replace("\\", "/").strip("/")
        if normalized and (rel == normalized or rel.startswith(f"{normalized}/")):
            return True
    return False


def _governed_autonomy_line_delta(
    source_path: Path | None,
    workspace_path: Path | None,
) -> dict[str, Any]:
    try:
        source_lines = (
            source_path.read_text(encoding="utf-8").splitlines()
            if source_path
            else []
        )
        workspace_lines = (
            workspace_path.read_text(encoding="utf-8").splitlines()
            if workspace_path
            else []
        )
    except (OSError, UnicodeDecodeError):
        return {"line_delta_available": False}
    insertions = 0
    deletions = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        a=source_lines,
        b=workspace_lines,
    ).get_opcodes():
        if tag in {"replace", "delete"}:
            deletions += i2 - i1
        if tag in {"replace", "insert"}:
            insertions += j2 - j1
    return {
        "line_delta_available": True,
        "insertions": insertions,
        "deletions": deletions,
    }


def _governed_autonomy_candidate_changes_reference(
    manifest: dict[str, Any] | None,
    *,
    max_files: int = 80,
) -> dict[str, Any] | None:
    if not isinstance(manifest, dict):
        return None
    source_root_value = manifest.get("source_root")
    workspace_root_value = manifest.get("workspace_root")
    if not source_root_value or not workspace_root_value:
        return {"available": False, "reason": "source_or_workspace_root_unavailable"}
    try:
        source_root = Path(str(source_root_value)).resolve(strict=True)
        workspace_root = Path(str(workspace_root_value)).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return {"available": False, "reason": "source_or_workspace_root_unavailable"}
    allowed_paths = tuple(manifest.get("writable_allowed_paths") or ())
    excluded_roots = tuple(
        str(item) for item in manifest.get("product_diff_excluded_roots") or ()
    )
    source_files: set[str] = set()
    workspace_files: set[str] = set()
    for pattern in allowed_paths:
        source_files.update(
            _governed_autonomy_candidate_files_for_pattern(source_root, pattern)
        )
        workspace_files.update(
            _governed_autonomy_candidate_files_for_pattern(workspace_root, pattern)
        )
    changes: list[dict[str, Any]] = []
    totals = {
        "modified": 0,
        "created": 0,
        "deleted": 0,
        "insertions": 0,
        "deletions": 0,
    }
    for rel in sorted(source_files | workspace_files):
        if _governed_autonomy_candidate_diff_excluded(rel, excluded_roots=excluded_roots):
            continue
        source_path = source_root / rel if rel in source_files else None
        workspace_path = workspace_root / rel if rel in workspace_files else None
        source_sha = _sha256_file_or_none(source_path) if source_path is not None else None
        workspace_sha = _sha256_file_or_none(workspace_path) if workspace_path is not None else None
        if source_sha == workspace_sha:
            continue
        if source_path is not None and workspace_path is not None:
            change = "modified"
        elif workspace_path is not None:
            change = "created"
        else:
            change = "deleted"
        line_delta = _governed_autonomy_line_delta(source_path, workspace_path)
        insertions = int(line_delta.get("insertions") or 0)
        deletions = int(line_delta.get("deletions") or 0)
        totals[change] += 1
        totals["insertions"] += insertions
        totals["deletions"] += deletions
        if len(changes) < max_files:
            changes.append({
                "path": rel,
                "change": change,
                "source_SHA256": source_sha,
                "workspace_SHA256": workspace_sha,
                **line_delta,
            })
    return {
        "available": True,
        "files_changed": totals["modified"] + totals["created"] + totals["deleted"],
        "modified_file_count": totals["modified"],
        "created_file_count": totals["created"],
        "deleted_file_count": totals["deleted"],
        "line_insertions": totals["insertions"],
        "line_deletions": totals["deletions"],
        "truncated": (
            totals["modified"] + totals["created"] + totals["deleted"] > max_files
        ),
        "files": changes,
    }


def _governed_autonomy_validation_infrastructure_failure(
    run: dict[str, Any],
) -> bool:
    text = " ".join(
        str(run.get(key) or "")
        for key in (
            "status",
            "outcome",
            "failure_category",
            "failure_summary",
            "summary",
            "error",
        )
    ).casefold()
    validation_hint = "workpacket_validation" in text or "validation" in text
    infrastructure_hint = any(
        marker in text
        for marker in (
            "typeerror",
            "unexpected keyword argument",
            "tool execution failed",
            "validation_runtime_unavailable",
            "workpacket_validation_authority_unavailable",
        )
    )
    return validation_hint and infrastructure_hint


def _governed_autonomy_runtime_terminal_reconciliation(
    record: dict[str, Any] | None,
    *,
    effective_authority: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if record is None:
        return None
    owned_run_id = None
    if effective_authority is not None:
        owned_lineage_state = effective_authority.get("owned_lineage_state") or {}
        owned_run_id = _int_or_none(owned_lineage_state.get("owned_governed_run_id"))
        execution_state = effective_authority.get("current_execution_state") or {}
        task_visibility = execution_state.get("task")
        runs = execution_state.get("runs")
        if not isinstance(runs, list):
            task_visibility, runs = _governed_autonomy_kanban_visibility(record)
    else:
        owned_run_id = _governed_autonomy_owned_direct_run_id(record)
        task_visibility, runs = _governed_autonomy_kanban_visibility(record)
    if owned_run_id is None:
        return None
    owned_run = next(
        (run for run in runs if _int_or_none(run.get("id")) == owned_run_id),
        None,
    )
    if owned_run is None or _execution_is_active(owned_run):
        return None
    status = str(owned_run.get("status") or "").strip().lower()
    outcome = str(owned_run.get("outcome") or "").strip().lower()
    if (
        status not in _TERMINAL_EXECUTION_STATUSES
        and outcome not in _TERMINAL_EXECUTION_STATUSES
        and owned_run.get("ended_at") is None
    ):
        return None
    action_ids = governed_ticket_lifecycle_action_ids(str(record["ticket_id"]))
    completed = status in {"completed", "done"} or outcome == "completed"
    detail = (
        owned_run.get("error")
        or owned_run.get("failure_summary")
        or owned_run.get("summary")
        or f"Kanban run {owned_run_id} ended with status {status or outcome or 'unknown'}"
    )
    manifest, materialization_reference = _governed_autonomy_materialization_manifest(
        record.get("workspace_path") or (task_visibility or {}).get("workspace_path"),
    )
    candidate_changes = _governed_autonomy_candidate_changes_reference(manifest)
    validation_infra_failure = _governed_autonomy_validation_infrastructure_failure(
        owned_run,
    )
    if completed:
        runtime_status = "direct_execution_terminal_completed"
        blocker_code = None
        next_action = {
            "id": action_ids["review_prepare"],
            "target_ticket_id": record["ticket_id"],
            "required_human_action": "review_validation_preparation",
        }
        next_autonomous_action = "prepare governed review validation from terminal completion evidence"
        next_human_action = None
    elif validation_infra_failure:
        runtime_status = "direct_execution_terminal_blocked_validation_repairable"
        blocker_code = "GOVERNED_AUTONOMY_VALIDATION_INFRASTRUCTURE_REPAIRABLE"
        next_action = {
            "id": governed_autonomy_continuation_action_id(str(record["ticket_id"])),
            "target_ticket_id": record["ticket_id"],
            "authority": "backend_derived_governed_autonomy_continuation",
            "recommended_strategy": "DIRECT",
        }
        next_autonomous_action = (
            "replay terminal run evidence non-consumingly, then run governed workpacket validation "
            "after validation tool infrastructure is repaired"
        )
        next_human_action = None
    else:
        runtime_status = "direct_execution_terminal_blocked"
        blocker_code = "GOVERNED_AUTONOMY_TERMINAL_RUN_BLOCKED"
        next_action = None
        next_autonomous_action = None
        next_human_action = "human review or recovery authority required for terminal governed run"
    return {
        "terminal_run_reconciled": True,
        "governed_autonomy_runtime_status": runtime_status,
        "terminal_run_id": owned_run_id,
        "terminal_run_status": status or None,
        "terminal_run_outcome": outcome or None,
        "terminal_run_ended_at": owned_run.get("ended_at"),
        "terminal_run_failure_category": owned_run.get("failure_category"),
        "terminal_run_failure_summary": owned_run.get("failure_summary"),
        "validation_infrastructure_failure": validation_infra_failure,
        "validation_observation_reference": {
            "tool_name": "workpacket_validation",
            "infrastructure_failure": validation_infra_failure,
            "error_excerpt": _safe_text(detail, limit=500),
        },
        "source_materialization_reference": materialization_reference,
        "candidate_changes_reference": candidate_changes,
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(detail, limit=500) if blocker_code else None,
        "next_autonomous_action": next_autonomous_action,
        "next_human_action": next_human_action,
        "next_action": next_action,
    }


def _governed_autonomy_fresh_execution_request_reference(
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    terminal_reconciliation: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not request.fresh_execution_request_text:
        return None
    identity = {
        "project_id": projection["project_id"],
        "ticket_id": projection["ticket_id"],
        "ticket_spec_SHA256": projection["ticket_spec_SHA256"],
        "work_packet_id": projection["work_packet_id"],
        "work_packet_SHA256": projection["work_packet_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "activation_action_SHA256": activation["activation_action_SHA256"],
        "human_request_text": request.fresh_execution_request_text,
    }
    text_sha256 = hashlib.sha256(
        request.fresh_execution_request_text.encode("utf-8")
    ).hexdigest()
    reference = {
        "fresh_execution_requested": True,
        "transition_classification": "FRESH_EXECUTION_TRANSITION_REPRESENTED",
        "execution_attempt_reason": PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON,
        "fresh_execution_request_SHA256": _digest_payload(
            PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_DIGEST_ALGORITHM,
            identity,
        ),
        "human_request_text_SHA256": text_sha256,
        "human_request_text_excerpt": _safe_text(
            request.fresh_execution_request_text,
            limit=300,
        ),
        "same_ticket": True,
        "same_work_packet_authority": True,
        "same_kanban_task": True,
        "same_authority_envelope": True,
        "new_scratch_required": True,
    }
    if terminal_reconciliation is not None:
        reference.update({
            "prior_terminal_run_id": terminal_reconciliation.get("terminal_run_id"),
            "prior_terminal_run_status": terminal_reconciliation.get(
                "terminal_run_status"
            ),
            "prior_terminal_run_outcome": terminal_reconciliation.get(
                "terminal_run_outcome"
            ),
            "prior_terminal_run_ended_at": terminal_reconciliation.get(
                "terminal_run_ended_at"
            ),
            "prior_terminal_run_preserved": True,
        })
    return reference


def _governed_autonomy_fresh_execution_request_already_consumed(
    previous: dict[str, Any] | None,
    fresh_execution_request: dict[str, Any] | None,
) -> bool:
    if previous is None or fresh_execution_request is None:
        return False
    if not bool(previous.get("fresh_execution_requested")):
        return False
    if previous.get("fresh_execution_request_SHA256") != fresh_execution_request.get(
        "fresh_execution_request_SHA256"
    ):
        return False
    return bool(
        previous.get("kanban_run_created")
        or previous.get("lineage_dispatch_performed")
        or previous.get("execution_started")
    )


def _governed_autonomy_fresh_execution_request_pending_replay(
    previous: dict[str, Any] | None,
    fresh_execution_request: dict[str, Any] | None,
) -> bool:
    if previous is None or fresh_execution_request is None:
        return False
    if not bool(previous.get("fresh_execution_requested")):
        return False
    if previous.get("fresh_execution_request_SHA256") != fresh_execution_request.get(
        "fresh_execution_request_SHA256"
    ):
        return False
    return not _governed_autonomy_fresh_execution_request_already_consumed(
        previous,
        fresh_execution_request,
    )


def _governed_autonomy_apply_terminal_reconciliation(
    payload: dict[str, Any],
    terminal_reconciliation: dict[str, Any] | None,
) -> dict[str, Any]:
    if terminal_reconciliation is None:
        return payload
    payload.update({
        "governed_autonomy_runtime_status": terminal_reconciliation[
            "governed_autonomy_runtime_status"
        ],
        "terminal_run_reconciled": True,
        "terminal_run_id": terminal_reconciliation["terminal_run_id"],
        "terminal_run_status": terminal_reconciliation["terminal_run_status"],
        "terminal_run_outcome": terminal_reconciliation["terminal_run_outcome"],
        "terminal_run_ended_at": terminal_reconciliation["terminal_run_ended_at"],
        "terminal_run_failure_category": terminal_reconciliation[
            "terminal_run_failure_category"
        ],
        "terminal_run_failure_summary": terminal_reconciliation[
            "terminal_run_failure_summary"
        ],
        "validation_infrastructure_failure": terminal_reconciliation[
            "validation_infrastructure_failure"
        ],
        "validation_observation_reference": terminal_reconciliation[
            "validation_observation_reference"
        ],
        "source_materialization_reference": terminal_reconciliation[
            "source_materialization_reference"
        ],
        "candidate_changes_reference": terminal_reconciliation[
            "candidate_changes_reference"
        ],
        "blocker_code": terminal_reconciliation["blocker_code"],
        "blocker_detail": terminal_reconciliation["blocker_detail"],
        "next_autonomous_action": terminal_reconciliation["next_autonomous_action"],
        "next_human_action": terminal_reconciliation["next_human_action"],
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
    })
    if terminal_reconciliation.get("next_action") is not None:
        payload["next_action"] = terminal_reconciliation["next_action"]
    return payload


def _governed_autonomy_provider_readiness_reference(
    provider_readiness: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ok": provider_readiness.get("ok") is True,
        "provider": provider_readiness.get("provider"),
        "model": provider_readiness.get("model"),
        "api_mode": provider_readiness.get("api_mode"),
        "credential_profile_id": provider_readiness.get("credential_profile_id"),
        "credential_policy_revision": provider_readiness.get("credential_policy_revision"),
        "provider_runtime_profile_id": provider_readiness.get("provider_runtime_profile_id"),
        "worker_profile_id": provider_readiness.get("worker_profile_id"),
        "blocker_code": provider_readiness.get("blocker_code"),
        "blocker_detail": _safe_text(provider_readiness.get("blocker_detail"), limit=300)
        if provider_readiness.get("blocker_detail")
        else None,
        "legacy_auth_json_used": bool(provider_readiness.get("legacy_auth_json_used")),
        "API_key_fallback_used": bool(provider_readiness.get("API_key_fallback_used")),
        "credential_pool_fallback_used": bool(provider_readiness.get("credential_pool_fallback_used")),
    }


def _governed_autonomy_runtime_base_record(
    *,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    runtime_decision: str,
    runtime_status: str,
    latest_decision_evidence: dict[str, Any],
    provider_readiness: dict[str, Any],
    process_continuation_increment: int = 1,
    self_repair_increment: int = 0,
    tool_candidate_increment: int = 0,
    command_evaluation_increment: int = 0,
    delegation_increment: int = 0,
    validation_failure_increment: int = 0,
    progress_marker_sha256: str | None = None,
    blocker_code: str | None = None,
    blocker_detail: str | None = None,
    next_autonomous_action: str | None = None,
    next_human_action: str | None = None,
    fresh_execution_request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    limits = _governed_autonomy_runtime_budget_limits(activation)
    counts = _governed_autonomy_runtime_counts(
        previous,
        process_continuation_increment=process_continuation_increment,
        self_repair_increment=self_repair_increment,
        tool_candidate_increment=tool_candidate_increment,
        command_evaluation_increment=command_evaluation_increment,
        delegation_increment=delegation_increment,
        validation_failure_increment=validation_failure_increment,
    )
    fingerprint = _governed_autonomy_runtime_fingerprint(
        request,
        runtime_decision=runtime_decision,
    )
    no_progress_count, progress_markers = _governed_autonomy_runtime_no_progress(
        previous,
        fingerprint_sha256=fingerprint,
        progress_marker_sha256=progress_marker_sha256,
    )
    remaining = _governed_autonomy_runtime_budget_remaining(
        limits,
        counts,
        no_progress_count=no_progress_count,
    )
    budget_exhausted = _governed_autonomy_runtime_budget_exhausted(
        limits,
        counts,
        no_progress_count=no_progress_count,
    )
    if budget_exhausted and next_human_action is None:
        next_human_action = "budget exhausted; human authority required before more autonomy"
    record = {
        "schema_version": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_RUNTIME_POLICY_ID,
        "source_system": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM,
        "created_at": _utc_now_iso(),
        **_current_ticket_projection_identity_fields(projection),
        "approval_publication_SHA256": projection["approval_publication_SHA256"],
        "dependency_plan_SHA256": projection["dependency_plan_SHA256"],
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "assignee_profile": projection["assignee_profile"],
        "selected_profile": projection["selected_profile"],
        "activation_action_SHA256": activation["activation_action_SHA256"],
        "previous_runtime_state_SHA256": previous.get("runtime_state_SHA256") if previous else None,
        "governed_autonomy_policy_id": activation["governed_autonomy_policy_id"],
        "governed_autonomy_envelope_SHA256": activation["governed_autonomy_envelope_SHA256"],
        "governed_autonomy_envelope_reference": activation["governed_autonomy_envelope_reference"],
        "governed_autonomy_budget": activation["governed_autonomy_budget"],
        "authority_revalidated": True,
        "same_authority_subset_validated": True,
        "runtime_goal_SHA256": _digest_payload(
            "pepper-governed-autonomy-runtime-goal-sha256-v1",
            {"runtime_goal": request.runtime_goal},
        ),
        "runtime_goal_excerpt": _safe_text(request.runtime_goal, limit=300),
        "runtime_decision": runtime_decision,
        "governed_autonomy_runtime_status": runtime_status,
        "latest_decision_evidence": latest_decision_evidence,
        "fresh_execution_requested": fresh_execution_request is not None,
        "fresh_execution_request_SHA256": (
            fresh_execution_request.get("fresh_execution_request_SHA256")
            if fresh_execution_request is not None
            else None
        ),
        "fresh_execution_request_reference": fresh_execution_request,
        "execution_attempt_reason": (
            PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON
            if fresh_execution_request is not None
            else None
        ),
        "prior_terminal_run_id": (
            fresh_execution_request.get("prior_terminal_run_id")
            if fresh_execution_request is not None
            else None
        ),
        "provider_readiness_reference": _governed_autonomy_provider_readiness_reference(
            provider_readiness
        ),
        "process_continuation_count": counts["process_continuation_count"],
        "self_repair_count": counts["self_repair_count"],
        "task_local_tool_candidate_count": counts["task_local_tool_candidate_count"],
        "command_evaluation_count": counts["command_evaluation_count"],
        "A2A_delegation_count": counts["A2A_delegation_count"],
        "validation_failure_count": counts["validation_failure_count"],
        "latest_no_progress_fingerprint_SHA256": fingerprint,
        "no_progress_count": no_progress_count,
        "progress_marker_SHA256s": progress_markers,
        "budget_limits": limits,
        "budget_remaining": remaining,
        "budget_exhausted": budget_exhausted,
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=500) if blocker_detail else None,
        "next_autonomous_action": next_autonomous_action,
        "next_human_action": next_human_action,
        **_governed_autonomy_activation_source_run(activation),
        "legacy_human_recovery_retry_micro_gates_required": False,
        "legacy_run_mutation_performed": False,
        "kanban_run_created": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "lineage_dispatch_performed": False,
        "A2A_dispatch_performed": runtime_decision == "A2A_DELEGATION",
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "current_invocation_side_effects": {
            "dispatch_performed": False,
            "Kanban_dispatch": False,
            "execution_started": False,
            "worker_execution": False,
            "worker_process_started": False,
            "lineage_dispatch_performed": False,
            "A2A_dispatch_performed": runtime_decision == "A2A_DELEGATION",
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        },
        "human_smoke_marker": PEPPER_GOVERNED_AUTONOMY_READY_MARKER,
    }
    record["runtime_state_SHA256"] = _governed_autonomy_runtime_record_digest(record)
    return record


def _prepare_current_ticket_governed_autonomy_task_for_dispatch(
    *,
    projection: dict[str, Any],
    activation: dict[str, Any],
    envelope: Any,
    fresh_execution_request: dict[str, Any] | None = None,
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
        task_unblocked = False
        task_triage_specified = False
        if task.status == "triage" and fresh_execution_request is not None:
            if task.claim_lock or task.worker_pid or task.current_run_id is not None:
                return {
                    "task_prepare_status": "blocked",
                    "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
                    "blocker_detail": "projected Kanban task has unresolved current lifecycle state",
                }
            if not kanban_db.specify_triage_task(
                conn,
                task_id,
                assignee=str(projection["assignee_profile"]),
                author=PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM,
            ):
                return {
                    "task_prepare_status": "blocked",
                    "blocker_code": "KANBAN_TRIAGE_SPECIFICATION_FAILED",
                    "blocker_detail": "projected Kanban triage task could not be specified for fresh governed autonomy",
                }
            task_triage_specified = True
            task = kanban_db.get_task(conn, task_id)
            if task is None:
                return {
                    "task_prepare_status": "blocked",
                    "blocker_code": "KANBAN_TASK_GAP",
                    "blocker_detail": "projected Kanban task is missing after triage specification",
                }
        if task.status not in {"blocked", "ready"}:
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "KANBAN_GOVERNED_AUTONOMY_SOURCE_GAP",
                "blocker_detail": f"projected Kanban task status is {task.status}",
            }
        if task.status == "blocked":
            if not kanban_db.unblock_task(conn, task_id):
                return {
                    "task_prepare_status": "blocked",
                    "blocker_code": "KANBAN_UNBLOCK_FAILED",
                    "blocker_detail": "projected Kanban task could not be unblocked for governed autonomy",
                }
            task_unblocked = True
        task = kanban_db.get_task(conn, task_id)
        if task is None or task.status != "ready":
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "KANBAN_TASK_NOT_READY",
                "blocker_detail": "projected Kanban task did not become ready for governed autonomy",
            }
        if task.claim_lock or task.worker_pid or task.current_run_id is not None:
            return {
                "task_prepare_status": "blocked",
                "blocker_code": "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED",
                "blocker_detail": "projected Kanban task has unresolved current lifecycle state",
            }
        try:
            body = json.loads(task.body or "{}")
        except json.JSONDecodeError:
            body = {}
        if not isinstance(body, dict):
            body = {}
        source_reference = activation.get("governed_autonomy_envelope_reference")
        source_run_id = source_reference.get("source_run_id") if isinstance(source_reference, dict) else None
        body.update({
            "task_skills": [],
            "governed_autonomy_continuation_authorized": True,
            "governed_autonomy_continuation_reason": (
                PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON
            ),
            "governed_autonomy_activation_action_SHA256": activation["activation_action_SHA256"],
            "governed_autonomy_authority_SHA256": envelope.envelope_SHA256,
            "governed_autonomy_source_run_id": source_run_id,
        })
        if fresh_execution_request is not None:
            next_attempt_number = len(kanban_db.list_runs(conn, task_id)) + 1
            fresh_workspace_path = (
                kanban_db.workspaces_root(board=board)
                / f"{task_id}-attempt-{next_attempt_number}"
            )
            body.update({
                "fresh_execution_requested": True,
                "fresh_execution_request_SHA256": fresh_execution_request[
                    "fresh_execution_request_SHA256"
                ],
                "execution_attempt_reason": PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON,
                "prior_terminal_run_id": fresh_execution_request.get("prior_terminal_run_id"),
                "fresh_execution_attempt_number": next_attempt_number,
                "fresh_execution_workspace_path": str(fresh_workspace_path),
            })
        else:
            fresh_workspace_path = None
        conn.execute(
            "UPDATE tasks SET skills = ?, body = ?, claim_lock = NULL, "
            "claim_expires = NULL, worker_pid = NULL, workspace_path = ? "
            "WHERE id = ? AND status = 'ready'",
            (
                json.dumps([]),
                json.dumps(body, sort_keys=True),
                str(fresh_workspace_path) if fresh_workspace_path is not None else task.workspace_path,
                task_id,
            ),
        )
        kanban_db._append_event(
            conn,
            task_id,
            "governed_autonomy_continuation_prepared",
            {
                "source": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM,
                "reason": PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON,
                "activation_action_SHA256": activation["activation_action_SHA256"],
                "backend_derived_live_authority_SHA256": envelope.envelope_SHA256,
                "source_run_id": source_run_id,
                "future_task_skills": [],
                "task_triage_specified": task_triage_specified,
                "fresh_execution_request_reference": fresh_execution_request,
                "fresh_execution_workspace_path": str(fresh_workspace_path)
                if fresh_workspace_path is not None
                else None,
            },
        )
        conn.commit()
        task = kanban_db.get_task(conn, task_id)
        return {
            "task_prepare_status": "prepared",
            "blocker_code": None,
            "blocker_detail": None,
            "task_unblocked": task_unblocked,
            "task_triage_specified": task_triage_specified,
            "task_skills_corrected": True,
            "governed_autonomy_continuation_reason": (
                PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON
            ),
            "dispatcher_primitive": (
                "kanban_db.specify_triage_task+kanban_db.claim_task+resolve_workspace+_default_spawn"
                if task_triage_specified
                else "kanban_db.unblock_task+kanban_db.claim_task+resolve_workspace+_default_spawn"
            ),
            "kanban_task_status_after_prepare": task.status if task is not None else None,
            "kanban_task_skills_after_prepare": list(task.skills or []) if task is not None else None,
            "source_run_id": source_run_id,
            "fresh_execution_request_reference": fresh_execution_request,
            "fresh_execution_workspace_path": str(fresh_workspace_path)
            if fresh_workspace_path is not None
            else None,
        }
    finally:
        conn.close()


def _governed_autonomy_dispatch_result_reference(
    dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    source_materialization = dispatch_result.get("source_materialization")
    materialization_reference = None
    if isinstance(source_materialization, dict):
        materialization_reference = {
            key: source_materialization.get(key)
            for key in (
                "policy_id",
                "source_materialized",
                "dependency_substrate_materialized",
                "dependency_substrate_kind",
                "dependency_install_performed",
                "canonical_package_lock_materialized",
                "manifest_path",
            )
            if key in source_materialization
        }
    return {
        "start_status": dispatch_result.get("start_status"),
        "blocker_code": dispatch_result.get("blocker_code"),
        "blocker_detail": _safe_text(dispatch_result.get("blocker_detail"), limit=300)
        if dispatch_result.get("blocker_detail")
        else None,
        "dispatch_performed": bool(dispatch_result.get("dispatch_performed")),
        "execution_started": bool(dispatch_result.get("execution_started")),
        "worker_execution": bool(dispatch_result.get("worker_execution")),
        "worker_process_started": bool(dispatch_result.get("worker_process_started")),
        "Kanban_dispatch": bool(dispatch_result.get("Kanban_dispatch")),
        "kanban_run_id": dispatch_result.get("kanban_run_id"),
        "kanban_task_status": dispatch_result.get("kanban_task_status"),
        "workspace_path": dispatch_result.get("workspace_path"),
        "workspace_created": bool(dispatch_result.get("workspace_created")),
        "source_materialized": bool(dispatch_result.get("source_materialized")),
        "source_materialization_reference": materialization_reference,
    }


def _with_governed_autonomy_dispatch_result(
    record: dict[str, Any],
    *,
    dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(record)
    for key in (
        "blocker_code",
        "blocker_detail",
        "dispatch_performed",
        "execution_started",
        "worker_execution",
        "worker_process_started",
        "Kanban_dispatch",
        "kanban_run_id",
        "workspace_path",
        "workspace_created",
    ):
        if key in dispatch_result:
            updated[key] = dispatch_result.get(key)
    updated["worker_pid_recorded"] = bool(dispatch_result.get("worker_pid_recorded"))
    updated["kanban_task_status"] = dispatch_result.get("kanban_task_status")
    updated["kanban_run_created"] = bool(dispatch_result.get("kanban_run_id")) and bool(
        dispatch_result.get("dispatch_performed")
    )
    updated["lineage_dispatch_performed"] = bool(dispatch_result.get("dispatch_performed"))
    updated["governed_autonomy_continuation_reason"] = (
        PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON
    )
    updated["dispatcher_primitive"] = "kanban_db.unblock_task+kanban_db.claim_task+resolve_workspace+_default_spawn"
    if bool(dispatch_result.get("execution_started")):
        updated["live_autonomous_continuation_marker"] = (
            PEPPER_GOVERNED_AUTONOMY_LIVE_CONTINUATION_MARKER
        )
    side_effects = dict(updated.get("current_invocation_side_effects") or {})
    side_effects.update({
        "dispatch_performed": bool(dispatch_result.get("dispatch_performed")),
        "Kanban_dispatch": bool(dispatch_result.get("Kanban_dispatch")),
        "execution_started": bool(dispatch_result.get("execution_started")),
        "worker_execution": bool(dispatch_result.get("worker_execution")),
        "worker_process_started": bool(dispatch_result.get("worker_process_started")),
        "lineage_dispatch_performed": bool(dispatch_result.get("dispatch_performed")),
        "A2A_dispatch_performed": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    })
    updated["current_invocation_side_effects"] = side_effects
    updated.pop("runtime_state_SHA256", None)
    updated["runtime_state_SHA256"] = _governed_autonomy_runtime_record_digest(updated)
    return updated


def _build_governed_autonomy_direct_runtime_record(
    *,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    provider_readiness: dict[str, Any],
    envelope: Any,
    terminal_reconciliation: dict[str, Any] | None = None,
    spawn_fn: Any = None,
) -> dict[str, Any]:
    fresh_execution_request = _governed_autonomy_fresh_execution_request_reference(
        request,
        projection=projection,
        activation=activation,
        terminal_reconciliation=terminal_reconciliation,
    )
    prep_result = _prepare_current_ticket_governed_autonomy_task_for_dispatch(
        projection=projection,
        activation=activation,
        envelope=envelope,
        fresh_execution_request=fresh_execution_request,
    )
    if prep_result.get("blocker_code"):
        return _governed_autonomy_runtime_base_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="DIRECT",
            runtime_status="blocked_stop_for_human",
            latest_decision_evidence={
                "decision": "DIRECT",
                "direct_execution_request_reference": prep_result,
                "blocker_code": prep_result.get("blocker_code"),
                "blocker_detail": prep_result.get("blocker_detail"),
                "fresh_execution_request_reference": fresh_execution_request,
            },
            provider_readiness=provider_readiness,
            process_continuation_increment=0,
            validation_failure_increment=0 if fresh_execution_request is not None else 1,
            blocker_code=str(prep_result.get("blocker_code") or "GOVERNED_AUTONOMY_PREP_FAILED"),
            blocker_detail=str(prep_result.get("blocker_detail") or "governed autonomy task preparation failed"),
            next_human_action="human authority required to resolve governed autonomy dispatch preparation",
            fresh_execution_request=None,
        )

    dispatch_result = _dispatch_exact_current_kanban_task(
        projection,
        spawn_fn=spawn_fn,
    )
    dispatch_consumed = bool(dispatch_result.get("dispatch_performed"))
    execution_started = bool(dispatch_result.get("execution_started"))
    fresh_execution_request_consumed = bool(
        fresh_execution_request is not None
        and (
            dispatch_consumed
            or execution_started
            or dispatch_result.get("kanban_run_id") is not None
        )
    )
    progress_marker = (
        _digest_payload(
            "pepper-governed-autonomy-direct-dispatch-progress-sha256-v1",
            {
                "kanban_run_id": dispatch_result.get("kanban_run_id"),
                "start_status": dispatch_result.get("start_status"),
                "execution_started": execution_started,
            },
        )
        if dispatch_consumed
        else None
    )
    record = _governed_autonomy_runtime_base_record(
        request=request,
        projection=projection,
        activation=activation,
        previous=previous,
        runtime_decision="DIRECT",
        runtime_status="direct_execution_continuation_started" if execution_started else "blocked_stop_for_human",
        latest_decision_evidence={
            "decision": "DIRECT",
            "rationale": "active authority revalidated; same-authority Kanban dispatch uses the canonical worker lifecycle",
            "direct_execution_request_reference": prep_result,
            "fresh_execution_request_reference": fresh_execution_request,
            "direct_execution_result_reference": _governed_autonomy_dispatch_result_reference(
                dispatch_result
            ),
        },
        provider_readiness=provider_readiness,
        process_continuation_increment=1 if dispatch_consumed else 0,
        validation_failure_increment=0 if execution_started else 1,
        progress_marker_sha256=progress_marker,
        blocker_code=None if execution_started else str(
            dispatch_result.get("blocker_code") or "GOVERNED_AUTONOMY_DISPATCH_FAILED"
        ),
        blocker_detail=None if execution_started else str(
            dispatch_result.get("blocker_detail") or "governed autonomy direct dispatch failed"
        ),
        next_autonomous_action=(
            "monitor the governed Kanban run and continue only after it reaches a terminal state"
            if execution_started
            else None
        ),
        next_human_action=None if execution_started else "human authority required to resolve dispatch blocker",
        fresh_execution_request=(
            fresh_execution_request if fresh_execution_request_consumed else None
        ),
    )
    return _with_governed_autonomy_dispatch_result(record, dispatch_result=dispatch_result)


def _build_governed_autonomy_runtime_stop_record(
    *,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    runtime_decision: str,
    blocker_code: str,
    blocker_detail: object,
    validation_failed: bool,
    provider_readiness: dict[str, Any],
    extra_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _governed_autonomy_runtime_base_record(
        request=request,
        projection=projection,
        activation=activation,
        previous=previous,
        runtime_decision=runtime_decision,
        runtime_status="blocked_stop_for_human",
        latest_decision_evidence={
            "decision": runtime_decision,
            "blocker_code": blocker_code,
            "blocker_detail": _safe_text(blocker_detail, limit=500),
            **(extra_evidence or {}),
        },
        provider_readiness=provider_readiness,
        process_continuation_increment=0,
        validation_failure_increment=1 if validation_failed else 0,
        blocker_code=blocker_code,
        blocker_detail=str(blocker_detail or ""),
        next_human_action="human authority or corrected same-authority runtime input required",
    )


def _capability_gap_reference_from_model(gap: Any) -> dict[str, Any]:
    payload = gap.model_dump(mode="json")
    return {
        "gap_id": payload["gap_id"],
        "gap_SHA256": payload["gap_SHA256"],
        "envelope_SHA256": payload["envelope_SHA256"],
        "kind": payload["kind"],
        "disposition": payload["disposition"],
        "requires_human_authority": payload["requires_human_authority"],
    }


def _continuation_lineage_reference_from_model(lineage: Any) -> dict[str, Any]:
    payload = lineage.model_dump(mode="json")
    return {
        "lineage_id": payload["lineage_id"],
        "lineage_SHA256": payload["lineage_SHA256"],
        "envelope_SHA256": payload["envelope_SHA256"],
        "gap_SHA256": payload["gap_SHA256"],
        "state": payload["state"],
        "continuation_index": payload["continuation_index"],
        "repair_attempt_count": payload["repair_attempt_count"],
        "tool_candidate_count": payload["tool_candidate_count"],
        "command_evaluation_count": payload["command_evaluation_count"],
        "successful_command_count": payload["successful_command_count"],
        "no_progress_count": payload["no_progress_count"],
        "stop_reason": payload["stop_reason"],
    }


def _command_result_reference_from_model(result: Any) -> dict[str, Any]:
    payload = result.model_dump(mode="json")
    stdout = payload.get("stdout") if isinstance(payload.get("stdout"), dict) else {}
    stderr = payload.get("stderr") if isinstance(payload.get("stderr"), dict) else {}
    return {
        "result_SHA256": payload["result_SHA256"],
        "disposition": payload["disposition"],
        "failure_reason": payload["failure_reason"],
        "exit_code": payload.get("exit_code"),
        "process_started": payload["process_started"],
        "stdout_SHA256": stdout.get("raw_SHA256"),
        "stderr_SHA256": stderr.get("raw_SHA256"),
        "stdout_excerpt": _safe_text(stdout.get("retained_text"), limit=300)
        if stdout.get("retained_text")
        else None,
        "stderr_excerpt": _safe_text(stderr.get("retained_text"), limit=300)
        if stderr.get("retained_text")
        else None,
    }


def _build_governed_autonomy_self_extension_runtime_record(
    *,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    envelope: Any,
    provider_readiness: dict[str, Any],
) -> dict[str, Any]:
    if getattr(envelope, "authority_kind", None) == "backend_derived_live_authority":
        return _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="TASK_LOCAL_SELF_EXTENSION_01AH_ENVELOPE_GAP",
            blocker_detail=(
                "task-local self-extension requires real 01AH envelope evidence; "
                "backend-derived live authority deliberately does not synthesize completed "
                "single-agent execution evidence"
            ),
            validation_failed=True,
            provider_readiness=provider_readiness,
            extra_evidence={
                "authority_kind": envelope.authority_kind,
                "01AH_envelope_lifecycle_classification": "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE",
            },
        )
    if not (
        request.task_local_tool_name
        and request.task_local_implementation_path
        and request.task_local_source_text
    ):
        return _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="TASK_LOCAL_SELF_EXTENSION_INPUT_GAP",
            blocker_detail="task-local tool name, implementation path, and source text are required",
            validation_failed=True,
            provider_readiness=provider_readiness,
        )
    try:
        from hermes_cli.agent_platform.work_packet import (
            CapabilityGapDisposition,
            TaskLocalToolLanguage,
            advance_governed_autonomy_continuation,
            build_task_local_capability_contract,
            build_tool_candidate,
            classify_capability_gap,
            evaluate_autonomy_command,
            execute_autonomy_command,
            materialize_task_local_tool,
            propose_autonomy_command,
            start_governed_autonomy_continuation,
        )

        gap = classify_capability_gap(
            envelope=envelope,
            observed_failure=request.observed_failure or request.runtime_goal,
            requested_capability=request.requested_capability or request.task_local_tool_name,
            requested_command=request.task_local_command,
        )
        if gap.disposition is not CapabilityGapDisposition.REPAIRABLE_TASK_LOCAL:
            return _build_governed_autonomy_runtime_stop_record(
                request=request,
                projection=projection,
                activation=activation,
                previous=previous,
                runtime_decision="STOP_FOR_HUMAN",
                blocker_code="TASK_LOCAL_SELF_EXTENSION_NOT_REPAIRABLE",
                blocker_detail=f"capability gap disposition is {gap.disposition.value}",
                validation_failed=True,
                provider_readiness=provider_readiness,
                extra_evidence={"capability_gap_reference": _capability_gap_reference_from_model(gap)},
            )
        lineage = start_governed_autonomy_continuation(envelope=envelope, gap=gap)
        contract = build_task_local_capability_contract(
            envelope=envelope,
            gap=gap,
            tool_name=request.task_local_tool_name,
            language=TaskLocalToolLanguage(request.task_local_language),
            implementation_path=request.task_local_implementation_path,
        )
        candidate = build_tool_candidate(
            contract=contract,
            source_text=request.task_local_source_text,
        )
        materialization = materialize_task_local_tool(
            envelope=envelope,
            contract=contract,
            candidate=candidate,
            replace_existing=True,
        )
        proposal = None
        evaluation = None
        command_result = None
        progress_marker = materialization.materialization_SHA256
        command_evaluation_increment = 0
        if request.task_local_command:
            proposal = propose_autonomy_command(
                envelope=envelope,
                contract=contract,
                candidate=candidate,
                source_command=request.task_local_command,
            )
            evaluation = evaluate_autonomy_command(
                envelope=envelope,
                contract=contract,
                candidate=candidate,
                proposal=proposal,
            )
            command_evaluation_increment = 1
            if evaluation.decision.value != "allow":
                advanced_lineage = advance_governed_autonomy_continuation(
                    envelope=envelope,
                    lineage=lineage,
                    candidate=candidate,
                    command_evaluation=evaluation,
                )
                return _governed_autonomy_runtime_base_record(
                    request=request,
                    projection=projection,
                    activation=activation,
                    previous=previous,
                    runtime_decision="TASK_LOCAL_SELF_EXTENSION",
                    runtime_status="blocked_stop_for_human",
                    latest_decision_evidence={
                        "decision": "TASK_LOCAL_SELF_EXTENSION",
                        "blocker_code": "TASK_LOCAL_COMMAND_DENIED",
                        "capability_gap_reference": _capability_gap_reference_from_model(gap),
                        "continuation_lineage_reference": _continuation_lineage_reference_from_model(
                            advanced_lineage
                        ),
                        "task_local_contract_reference": {
                            "contract_id": contract.contract_id,
                            "contract_SHA256": contract.contract_SHA256,
                            "tool_name": contract.tool_name,
                            "implementation_path": contract.implementation_path,
                        },
                        "tool_candidate_reference": {
                            "candidate_id": candidate.candidate_id,
                            "candidate_SHA256": candidate.candidate_SHA256,
                            "source_SHA256": candidate.source_SHA256,
                            "implementation_path": candidate.implementation_path,
                        },
                        "materialization_reference": materialization.model_dump(mode="json"),
                        "command_evaluation_reference": evaluation.model_dump(mode="json"),
                    },
                    provider_readiness=provider_readiness,
                    self_repair_increment=1,
                    tool_candidate_increment=1,
                    command_evaluation_increment=command_evaluation_increment,
                    validation_failure_increment=1,
                    progress_marker_sha256=progress_marker,
                    blocker_code="TASK_LOCAL_COMMAND_DENIED",
                    blocker_detail=f"command denied: {evaluation.denial_reason.value}",
                    next_human_action="human authority required for denied command shape",
                )
            command_result = execute_autonomy_command(evaluation)
            progress_marker = command_result.result_SHA256
            advanced_lineage = advance_governed_autonomy_continuation(
                envelope=envelope,
                lineage=lineage,
                candidate=candidate,
                command_evaluation=evaluation,
                command_result=command_result,
                progress_marker=command_result.result_SHA256,
            )
        else:
            advanced_lineage = advance_governed_autonomy_continuation(
                envelope=envelope,
                lineage=lineage,
                candidate=candidate,
                progress_marker=materialization.materialization_SHA256,
            )
    except Exception as exc:
        return _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="TASK_LOCAL_SELF_EXTENSION_POLICY_DENIED",
            blocker_detail=str(exc) or exc.__class__.__name__,
            validation_failed=True,
            provider_readiness=provider_readiness,
        )

    evidence = {
        "decision": "TASK_LOCAL_SELF_EXTENSION",
        "capability_gap_reference": _capability_gap_reference_from_model(gap),
        "continuation_lineage_reference": _continuation_lineage_reference_from_model(advanced_lineage),
        "task_local_contract_reference": {
            "contract_id": contract.contract_id,
            "contract_SHA256": contract.contract_SHA256,
            "tool_name": contract.tool_name,
            "language": contract.language.value,
            "implementation_path": contract.implementation_path,
            "permitted_operations": [operation.value for operation in contract.permitted_operations],
        },
        "tool_candidate_reference": {
            "candidate_id": candidate.candidate_id,
            "candidate_SHA256": candidate.candidate_SHA256,
            "source_SHA256": candidate.source_SHA256,
            "implementation_path": candidate.implementation_path,
            "entrypoint": candidate.entrypoint,
        },
        "materialization_reference": materialization.model_dump(mode="json"),
    }
    if proposal is not None:
        evidence["command_proposal_reference"] = {
            "proposal_id": proposal.proposal_id,
            "proposal_SHA256": proposal.proposal_SHA256,
            "source_command": proposal.source_command,
            "working_directory": proposal.working_directory,
            "timeout_seconds": proposal.timeout_seconds,
        }
    if evaluation is not None:
        evidence["command_evaluation_reference"] = evaluation.model_dump(mode="json")
    if command_result is not None:
        evidence["command_result_reference"] = _command_result_reference_from_model(command_result)
    blocked = advanced_lineage.state.value == "blocked"
    return _governed_autonomy_runtime_base_record(
        request=request,
        projection=projection,
        activation=activation,
        previous=previous,
        runtime_decision="TASK_LOCAL_SELF_EXTENSION",
        runtime_status=(
            "blocked_stop_for_human"
            if blocked
            else "task_local_self_extension_completed"
            if command_result is not None and command_result.disposition.value == "passed"
            else "task_local_self_extension_materialized"
        ),
        latest_decision_evidence=evidence,
        provider_readiness=provider_readiness,
        self_repair_increment=1,
        tool_candidate_increment=1,
        command_evaluation_increment=command_evaluation_increment,
        validation_failure_increment=1 if blocked else 0,
        progress_marker_sha256=progress_marker,
        blocker_code="TASK_LOCAL_COMMAND_FAILED" if blocked else None,
        blocker_detail=advanced_lineage.stop_reason.value if blocked else None,
        next_autonomous_action=None if blocked else "continue under active authority with materialized helper evidence",
        next_human_action="human review required for blocked task-local continuation" if blocked else None,
    )


def _runtime_path_matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        base = pattern[:-3]
        return path == base or path.startswith(f"{base}/")
    return path == pattern


def _runtime_path_allowed_by_envelope(envelope: Any, relative_path: str) -> bool:
    path = _normalize_runtime_relative_path(relative_path)
    if any(_runtime_path_matches_pattern(path, pattern) for pattern in envelope.forbidden_paths):
        return False
    return any(_runtime_path_matches_pattern(path, pattern) for pattern in envelope.allowed_paths)


def _governed_autonomy_a2a_default_delegate_paths(envelope: Any) -> tuple[str, ...]:
    paths: list[str] = []
    for pattern in tuple(getattr(envelope, "allowed_paths", ()) or ()):
        candidate = str(pattern or "").strip().replace("\\", "/")
        if candidate.endswith("/**"):
            candidate = candidate[:-3]
        if not candidate:
            continue
        normalized = _normalize_runtime_relative_path(candidate)
        if _runtime_path_allowed_by_envelope(envelope, normalized) and normalized not in paths:
            paths.append(normalized)
    return tuple(paths)


def _governed_autonomy_a2a_default_operations(
    request: CurrentTicketGovernedAutonomyContinuationRequest,
) -> tuple[str, ...]:
    goal = " ".join(
        str(item or "")
        for item in (
            request.delegate_goal,
            request.runtime_goal,
            request.requested_capability,
        )
    ).casefold()
    operations = ["list_directory", "read_file"]
    if re.search(r"\b(write|modify|replace|create|update|patch|fix|implement)\b", goal):
        operations.extend(["create_file", "replace_file", "create_directory"])
    return tuple(dict.fromkeys(operations))


def _governed_autonomy_a2a_child_authority_scope(
    *,
    envelope: Any,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
) -> tuple[tuple[str, ...], tuple[str, ...], dict[str, Any]]:
    paths = tuple(request.delegate_paths) or _governed_autonomy_a2a_default_delegate_paths(envelope)
    operations = tuple(request.delegate_requested_operations) or _governed_autonomy_a2a_default_operations(
        request
    )
    return paths, operations, {
        "child_authority_source": "backend_derived_parent_authority",
        "delegate_paths_source": "caller_narrowed_subset" if request.delegate_paths else "backend_allowed_paths",
        "delegate_requested_operations_source": (
            "caller_narrowed_subset"
            if request.delegate_requested_operations
            else "backend_goal_classification"
        ),
    }


def _validate_governed_autonomy_a2a_child_authority(
    *,
    envelope: Any,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
) -> tuple[bool, str | None, str | None, dict[str, Any]]:
    if not request.delegate_goal:
        return False, "A2A_DELEGATE_GOAL_REQUIRED", "delegate_goal is required", {}
    delegate_paths, delegate_operations, derivation = _governed_autonomy_a2a_child_authority_scope(
        envelope=envelope,
        request=request,
    )
    if not delegate_paths:
        return False, "A2A_DELEGATE_PATHS_REQUIRED", "backend-derived delegate paths are unavailable", derivation
    invalid_operations = [
        operation
        for operation in delegate_operations
        if operation in _GOVERNED_AUTONOMY_A2A_PRIVILEGED_OPERATIONS
        or operation not in _GOVERNED_AUTONOMY_A2A_ALLOWED_OPERATIONS
    ]
    if invalid_operations:
        return (
            False,
            "A2A_CHILD_AUTHORITY_OPERATION_DENIED",
            f"A2A child requested denied operations: {', '.join(invalid_operations)}",
            {"invalid_operations": invalid_operations},
        )
    denied_paths = [
        path for path in delegate_paths if not _runtime_path_allowed_by_envelope(envelope, path)
    ]
    if denied_paths:
        return (
            False,
            "A2A_CHILD_AUTHORITY_PATH_OUT_OF_SCOPE",
            f"A2A child paths exceed parent envelope: {', '.join(denied_paths)}",
            {"denied_paths": denied_paths},
        )
    return (
        True,
        None,
        None,
        {
            **derivation,
            "delegate_paths": list(delegate_paths),
            "delegate_requested_operations": list(delegate_operations),
            "parent_allowed_paths": list(envelope.allowed_paths),
            "parent_forbidden_paths": list(envelope.forbidden_paths),
            "provider_authority": "canonical_delegate_task_inherits_parent_agent_only",
            "network_access": False,
            "git_mutation": False,
            "docker": False,
            "dependency_install": False,
            "concurrency": "single_child",
        },
    )


class _GovernedAutonomyA2AParentAgentProxy:
    """Parent-agent view that lets delegate_task inherit credentials, not tools."""

    def __init__(self, parent_agent: Any) -> None:
        self._parent_agent = parent_agent
        self.enabled_toolsets: list[str] = []
        self.valid_tool_names: list[str] = []
        inherited_disabled = getattr(parent_agent, "disabled_toolsets", None)
        self.disabled_toolsets = list(inherited_disabled or [])
        self._memory_manager = None

    def __getattr__(self, name: str) -> Any:
        return getattr(self._parent_agent, name)


def _governed_autonomy_a2a_delegate_context_text(
    *,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    projection: dict[str, Any],
    activation: dict[str, Any],
    envelope: Any,
    authority_evidence: dict[str, Any],
) -> str:
    context = {
        "parent_policy_id": PEPPER_GOVERNED_AUTONOMY_RUNTIME_POLICY_ID,
        "a2a_policy_id": PEPPER_GOVERNED_AUTONOMY_A2A_POLICY_ID,
        "parent_authority_SHA256": envelope.envelope_SHA256,
        "activation_action_SHA256": activation["activation_action_SHA256"],
        "ticket_id": projection["ticket_id"],
        "work_packet_id": projection["work_packet_id"],
        "work_packet_SHA256": projection["work_packet_SHA256"],
        "delegate_authority": {
            "paths": list(authority_evidence.get("delegate_paths") or []),
            "requested_operations": list(
                authority_evidence.get("delegate_requested_operations") or []
            ),
            "parent_allowed_paths": authority_evidence.get("parent_allowed_paths", []),
            "parent_forbidden_paths": authority_evidence.get("parent_forbidden_paths", []),
            "child_authority_source": authority_evidence.get("child_authority_source"),
            "delegate_paths_source": authority_evidence.get("delegate_paths_source"),
            "delegate_requested_operations_source": authority_evidence.get(
                "delegate_requested_operations_source"
            ),
        },
        "hard_denials": {
            "git_mutation": False,
            "network_access": False,
            "provider_or_model_authority_expansion": False,
            "docker": False,
            "graphify": False,
            "dependency_install": False,
            "worker_control": False,
        },
        "operational_constraints": [
            "Use only the delegated path references and compact context supplied here.",
            "Do not ask for human microapproval; stop and report a blocker if authority is insufficient.",
            "Do not claim file, Git, Docker, Graphify, network, or provider-side effects unless verified in this context.",
        ],
    }
    return _safe_text(json.dumps(context, ensure_ascii=False, sort_keys=True), limit=6000)


def _opencode_provider_profile_reference(profile: Any) -> dict[str, Any]:
    base_url = getattr(profile, "base_url", "") or ""
    return {
        "provider_name": _safe_text(getattr(profile, "name", "opencode-zen"), limit=80),
        "aliases": [_safe_text(alias, limit=80) for alias in tuple(getattr(profile, "aliases", ()) or ())],
        "api_mode": _safe_text(getattr(profile, "api_mode", ""), limit=80),
        "auth_type": _safe_text(getattr(profile, "auth_type", ""), limit=80),
        "base_url_SHA256": _digest_payload(
            "pepper-governed-autonomy-opencode-provider-base-url-sha256-v1",
            {"base_url": base_url},
        ),
        "env_vars": [_safe_text(name, limit=80) for name in tuple(getattr(profile, "env_vars", ()) or ())],
    }


def _resolve_canonical_governed_autonomy_a2a_runtime(
    *,
    delegate_parent_agent: Any | None,
) -> tuple[Any | None, dict[str, Any], str | None, str | None]:
    evidence: dict[str, Any] = {
        "canonical_runtime_classification": "NO_CANONICAL_A2A_RUNTIME",
        "delegate_identity": {
            "tool_name": "delegate_task",
            "toolset": "delegation",
            "runtime_function": "tools.delegate_tool.delegate_task",
        },
        "invocation_contract": {
            "goal": "string",
            "context": "string",
            "tasks": "optional batch list",
            "role": "leaf|orchestrator",
            "background": "bool",
            "parent_agent": "required for child AIAgent construction",
            "return_type": "json string",
        },
        "sync_semantics": "called with background=False for 01AI bounded continuation",
        "async_semantics": "background=True is backed by tools.async_delegation outside this 01AI path",
        "opencode_provider_route": "opencode-zen",
        "opencode_delegate_registration_status": "provider_profile_only_not_delegate_tool",
    }
    try:
        from tools import delegate_tool
        from tools.registry import registry
    except Exception as exc:
        evidence["delegate_task_import_error"] = _safe_text(exc, limit=300)
        return None, evidence, "A2A_DELEGATE_TASK_IMPORT_FAILED", str(exc) or exc.__class__.__name__

    entry = registry.get_entry("delegate_task")
    if entry is None:
        evidence["delegate_task_registered"] = False
        return None, evidence, "A2A_DELEGATE_TASK_NOT_REGISTERED", "delegate_task is not registered"
    evidence.update({
        "delegate_task_registered": True,
        "delegate_task_toolset": entry.toolset,
        "delegate_task_schema_name": (entry.schema or {}).get("name"),
        "delegate_task_schema_parameters": sorted(
            ((entry.schema or {}).get("parameters") or {}).get("properties", {}).keys()
        ),
    })
    if entry.toolset != "delegation" or (entry.schema or {}).get("name") != "delegate_task":
        return None, evidence, "A2A_DELEGATE_TASK_REGISTRATION_MISMATCH", (
            "delegate_task registration does not match the canonical delegation toolset/schema"
        )
    delegate_task = getattr(delegate_tool, "delegate_task", None)
    if not callable(delegate_task):
        return None, evidence, "A2A_DELEGATE_TASK_NOT_CALLABLE", "tools.delegate_tool.delegate_task is not callable"

    try:
        from providers import get_provider_profile

        profile = get_provider_profile("opencode-zen")
    except Exception as exc:
        evidence["opencode_provider_profile_error"] = _safe_text(exc, limit=300)
        return None, evidence, "OPENCODE_PROVIDER_PROFILE_LOOKUP_FAILED", str(exc) or exc.__class__.__name__
    if profile is None:
        evidence["opencode_provider_profile_found"] = False
        evidence["canonical_runtime_classification"] = "HERMES_A2A_PARTIAL"
        return None, evidence, "OPENCODE_PROVIDER_PROFILE_UNAVAILABLE", (
            "opencode-zen provider profile is not registered/discoverable"
        )
    evidence["opencode_provider_profile_found"] = True
    evidence["opencode_provider_profile_reference"] = _opencode_provider_profile_reference(profile)

    if delegate_parent_agent is None:
        evidence["canonical_runtime_classification"] = "HERMES_CANONICAL_A2A_FOUND"
        return None, evidence, "A2A_PARENT_AGENT_CONTEXT_UNAVAILABLE", (
            "canonical Hermes delegate_task requires parent_agent context for child runtime construction"
        )

    evidence["canonical_runtime_classification"] = "HERMES_CANONICAL_A2A_FOUND"
    return delegate_task, evidence, None, None


def _delegate_result_summary_fields(value: object) -> dict[str, Any]:
    parsed = None
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = None
    payload = parsed if isinstance(parsed, dict) else value
    fields: dict[str, Any] = {
        "result_shape": "json_string" if parsed is not None else type(value).__name__,
    }
    status: object | None = None
    summary: object | None = None
    result_count: int | None = None
    api_call_count = 0
    if isinstance(payload, dict):
        status = payload.get("status") or payload.get("state") or payload.get("success")
        summary = payload.get("summary") or payload.get("final_response") or payload.get("result")
        results = payload.get("results")
        if isinstance(results, list):
            result_count = len(results)
            statuses: list[str] = []
            summaries: list[str] = []
            for item in results[:5]:
                if not isinstance(item, dict):
                    continue
                item_status = item.get("status") or item.get("state")
                if item_status is not None:
                    statuses.append(_safe_text(item_status, limit=80))
                item_summary = item.get("summary") or item.get("final_response") or item.get("result")
                if item_summary is not None:
                    summaries.append(_safe_text(item_summary, limit=300))
                try:
                    api_call_count += int(item.get("api_calls") or 0)
                except (TypeError, ValueError):
                    pass
            if status is None:
                status = "completed" if statuses and all(s == "completed" for s in statuses) else (statuses[0] if statuses else None)
            if summary is None and summaries:
                summary = "\n".join(summaries)
            fields["result_statuses"] = statuses
        elif payload.get("api_calls") is not None:
            try:
                api_call_count = int(payload.get("api_calls") or 0)
            except (TypeError, ValueError):
                api_call_count = 0
        if payload.get("total_duration_seconds") is not None:
            try:
                fields["total_duration_seconds"] = round(float(payload.get("total_duration_seconds") or 0), 3)
            except (TypeError, ValueError):
                pass
    if result_count is not None:
        fields["result_count"] = result_count
    fields["api_call_count"] = api_call_count
    result_text = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    fields["status"] = _safe_text(status, limit=80) if status is not None else "completed"
    fields["summary_excerpt"] = _safe_text(summary if summary is not None else result_text, limit=500)
    return fields


def _delegate_result_reference(value: object) -> dict[str, Any]:
    result_sha = _digest_payload(
        "pepper-governed-autonomy-a2a-delegate-result-sha256-v1",
        {"delegate_result": value},
    )
    return {
        "delegate_result_SHA256": result_sha,
        **_delegate_result_summary_fields(value),
    }


def _build_governed_autonomy_a2a_runtime_record(
    *,
    request: CurrentTicketGovernedAutonomyContinuationRequest,
    projection: dict[str, Any],
    activation: dict[str, Any],
    previous: dict[str, Any] | None,
    envelope: Any,
    provider_readiness: dict[str, Any],
    delegate_runner: Any | None,
    delegate_parent_agent: Any | None,
) -> dict[str, Any]:
    ok, blocker_code, blocker_detail, authority_evidence = _validate_governed_autonomy_a2a_child_authority(
        envelope=envelope,
        request=request,
    )
    if not ok:
        return _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code=blocker_code or "A2A_CHILD_AUTHORITY_DENIED",
            blocker_detail=blocker_detail or "A2A child authority is outside parent envelope",
            validation_failed=True,
            provider_readiness=provider_readiness,
            extra_evidence=authority_evidence,
        )
    delegate_request_reference = {
        "policy_id": PEPPER_GOVERNED_AUTONOMY_A2A_POLICY_ID,
        "runtime_kind": "hermes_delegate_task",
        "opencode_provider_route": "opencode-zen",
        "role": "leaf",
        "background": False,
        "delegate_goal_SHA256": _digest_payload(
            "pepper-governed-autonomy-a2a-delegate-goal-sha256-v1",
            {"delegate_goal": request.delegate_goal},
        ),
        "delegate_goal_excerpt": _safe_text(request.delegate_goal, limit=300),
        **authority_evidence,
    }
    if delegate_runner is None and request.delegate_result is None:
        canonical_runner, runtime_evidence, runtime_blocker_code, runtime_blocker_detail = (
            _resolve_canonical_governed_autonomy_a2a_runtime(
                delegate_parent_agent=delegate_parent_agent,
            )
        )
        delegate_request_reference.update(runtime_evidence)
        delegate_request_reference["runner_source"] = "canonical_hermes_delegate_task"
        if runtime_blocker_code is not None or canonical_runner is None:
            return _build_governed_autonomy_runtime_stop_record(
                request=request,
                projection=projection,
                activation=activation,
                previous=previous,
                runtime_decision="STOP_FOR_HUMAN",
                blocker_code=runtime_blocker_code or "A2A_DELEGATE_TASK_UNAVAILABLE",
                blocker_detail=runtime_blocker_detail or "canonical Hermes delegate_task is unavailable",
                validation_failed=False,
                provider_readiness=provider_readiness,
                extra_evidence={"a2a_delegation_request_reference": delegate_request_reference},
            )
    else:
        canonical_runner = None
        delegate_request_reference["runner_source"] = (
            "injected_delegate_runner" if delegate_runner is not None else "precomputed_delegate_result"
        )
    try:
        if delegate_runner is not None:
            delegate_output = delegate_runner(
                goal=request.delegate_goal,
                context={
                    "parent_policy_id": PEPPER_GOVERNED_AUTONOMY_RUNTIME_POLICY_ID,
                    "parent_authority_SHA256": envelope.envelope_SHA256,
                    "activation_action_SHA256": activation["activation_action_SHA256"],
                    "ticket_id": projection["ticket_id"],
                    "work_packet_id": projection["work_packet_id"],
                    "work_packet_SHA256": projection["work_packet_SHA256"],
                    "delegate_paths": list(authority_evidence.get("delegate_paths") or []),
                    "delegate_requested_operations": list(
                        authority_evidence.get("delegate_requested_operations") or []
                    ),
                    "child_authority_source": authority_evidence.get("child_authority_source"),
                    "git_mutation": False,
                    "provider_dispatch_count": 0,
                    "model_inference_count": 0,
                },
                role="leaf",
                background=False,
                max_iterations=1,
                parent_agent="pepper-governed-autonomy-runtime",
            )
        elif canonical_runner is not None:
            delegate_output = canonical_runner(
                goal=request.delegate_goal,
                context=_governed_autonomy_a2a_delegate_context_text(
                    request=request,
                    projection=projection,
                    activation=activation,
                    envelope=envelope,
                    authority_evidence=authority_evidence,
                ),
                role="leaf",
                background=False,
                max_iterations=1,
                parent_agent=_GovernedAutonomyA2AParentAgentProxy(delegate_parent_agent),
            )
        else:
            delegate_output = request.delegate_result
    except Exception as exc:
        return _build_governed_autonomy_runtime_stop_record(
            request=request,
            projection=projection,
            activation=activation,
            previous=previous,
            runtime_decision="STOP_FOR_HUMAN",
            blocker_code="A2A_DELEGATE_RUNNER_FAILED",
            blocker_detail=str(exc) or exc.__class__.__name__,
            validation_failed=False,
            provider_readiness=provider_readiness,
            extra_evidence={"a2a_delegation_request_reference": delegate_request_reference},
        )
    result_reference = _delegate_result_reference(delegate_output)
    return _governed_autonomy_runtime_base_record(
        request=request,
        projection=projection,
        activation=activation,
        previous=previous,
        runtime_decision="A2A_DELEGATION",
        runtime_status="a2a_delegation_completed",
        latest_decision_evidence={
            "decision": "A2A_DELEGATION",
            "a2a_delegation_request_reference": delegate_request_reference,
            "a2a_delegation_result_reference": result_reference,
        },
        provider_readiness=provider_readiness,
        delegation_increment=1,
        progress_marker_sha256=result_reference["delegate_result_SHA256"],
        next_autonomous_action="continue under active authority using bounded delegate result evidence",
    )


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


def _governed_autonomy_kanban_visibility(record: dict[str, Any]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    from hermes_cli import kanban_db

    board = _normalize_board(str(record["kanban_board_slug"]))
    task_id = str(record["kanban_task_id"])
    conn = kanban_db.connect(board=board)
    try:
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
    return task_visibility, [_run_dict(run) for run in runs]


def _governed_autonomy_status_without_record(
    *,
    project_id: str,
    ticket_id: str | None,
    ticket_title: str | None = None,
    projection: dict[str, Any] | None = None,
    blocker_code: str = "GOVERNED_AUTONOMY_AUTHORITY_REQUIRED",
    blocker_detail: str = "01AH governed autonomy authority has not been activated for the current ticket.",
) -> dict[str, Any]:
    identity = _current_ticket_projection_identity_fields(projection) if projection is not None else {}
    task_visibility: dict[str, Any] | None = None
    runs: list[dict[str, Any]] = []
    if projection is not None:
        task_visibility, runs = _governed_autonomy_kanban_visibility({
            "kanban_board_slug": projection["kanban_board_slug"],
            "kanban_task_id": projection["kanban_task_id"],
        })
    return {
        "source_system": PEPPER_GOVERNED_AUTONOMY_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_GOVERNED_AUTONOMY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_ACTION_POLICY_ID,
        "idempotent_replay": False,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "ticket_title": ticket_title,
        **identity,
        "governed_autonomy_activation_recorded": False,
        "governed_autonomy_status": "not_activated",
        "governed_autonomy_envelope_SHA256": None,
        "capability_gap_SHA256": None,
        "continuation_lineage_SHA256": None,
        "same_authority_subset_validated": False,
        "live_lineage_activation_authorized": False,
        "live_lineage_activation_status": "blocked_requires_governed_autonomy_activation",
        "blocker_code": blocker_code,
        "blocker_detail": _safe_text(blocker_detail, limit=300),
        "same_authority_delegation_status": "blocked_no_activation_record",
        "same_authority_delegation_authorized": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "lineage_dispatch_performed": False,
        "A2A_dispatch_performed": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "task": task_visibility,
        "runs": runs,
    }


def _governed_autonomy_activation_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool,
) -> dict[str, Any]:
    task_visibility, runs = _governed_autonomy_kanban_visibility(record)
    effective = _governed_autonomy_activation_effective_projection(record)
    current_side_effects = {
        "dispatch_performed": False,
        "Kanban_dispatch": False,
        "execution_started": False,
        "worker_process_started": False,
        "lineage_dispatch_performed": False,
        "A2A_dispatch_performed": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    }
    return {
        "source_system": PEPPER_GOVERNED_AUTONOMY_ACTION_SOURCE_SYSTEM,
        "schema_version": PEPPER_GOVERNED_AUTONOMY_ACTION_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_ACTION_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "activation_action_SHA256": record["activation_action_SHA256"],
        "governed_autonomy_activation_recorded": True,
        "governed_autonomy_activation_origin": effective[
            "governed_autonomy_activation_origin"
        ],
        "legacy_activation_compatibility_applied": effective[
            "legacy_activation_compatibility_applied"
        ],
        "historical_activation_record_preserved": effective[
            "historical_activation_record_preserved"
        ],
        "historical_runtime_limitation_classification": effective[
            "historical_runtime_limitation_classification"
        ],
        "effective_live_lineage_activation_authorized": effective[
            "effective_live_lineage_activation_authorized"
        ],
        "additional_human_activation_required": effective[
            "additional_human_activation_required"
        ],
        "authority_revalidated": effective["authority_revalidated"],
        "governed_autonomy_status": record["governed_autonomy_status"],
        "governed_autonomy_policy_id": record["governed_autonomy_policy_id"],
        "governed_autonomy_envelope_SHA256": record["governed_autonomy_envelope_SHA256"],
        "backend_derived_live_authority_SHA256": record[
            "backend_derived_live_authority_SHA256"
        ],
        "authority_derivation_source": record["authority_derivation_source"],
        "01AH_envelope_lifecycle_classification": record[
            "01AH_envelope_lifecycle_classification"
        ],
        "capability_gap_SHA256": record.get("capability_gap_SHA256"),
        "continuation_lineage_SHA256": record.get("continuation_lineage_SHA256"),
        "same_authority_subset_validated": record["same_authority_subset_validated"],
        "same_authority_subset": record["same_authority_subset"],
        "same_authority_delegation_policy_id": record["same_authority_delegation_policy_id"],
        "same_authority_delegation_status": effective["same_authority_delegation_status"],
        "same_authority_delegation_authorized": effective[
            "same_authority_delegation_authorized"
        ],
        "same_authority_delegation_blocker_code": effective[
            "same_authority_delegation_blocker_code"
        ],
        "same_authority_delegation_blocker_detail": effective[
            "same_authority_delegation_blocker_detail"
        ],
        "opencode_runtime_dispatcher_found": effective["opencode_runtime_dispatcher_found"],
        "delegate_task_runtime_kind": effective["delegate_task_runtime_kind"],
        "live_lineage_activation_authorized": effective["live_lineage_activation_authorized"],
        "live_lineage_activation_status": effective["live_lineage_activation_status"],
        "live_lineage_activation_blocker_code": effective[
            "live_lineage_activation_blocker_code"
        ],
        "live_lineage_activation_blocker_detail": effective[
            "live_lineage_activation_blocker_detail"
        ],
        "historical_live_lineage_activation_authorized": effective[
            "historical_live_lineage_activation_authorized"
        ],
        "historical_live_lineage_activation_status": effective[
            "historical_live_lineage_activation_status"
        ],
        "historical_live_lineage_activation_blocker_code": effective[
            "historical_live_lineage_activation_blocker_code"
        ],
        "current_invocation_side_effects": current_side_effects,
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_run_count": len(runs),
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "task": task_visibility,
        "runs": runs,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "lineage_dispatch_performed": False,
        "A2A_dispatch_performed": False,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "human_smoke_marker": record["human_smoke_marker"],
    }


def _governed_autonomy_runtime_summary(
    record: dict[str, Any],
    *,
    terminal_reconciliation: dict[str, Any] | None = None,
    effective_authority: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if terminal_reconciliation is None:
        terminal_reconciliation = _governed_autonomy_runtime_terminal_reconciliation(
            record,
            effective_authority=effective_authority,
        )
    summary = {
        "source_system": record["source_system"],
        "policy_id": record["policy_id"],
        "runtime_state_SHA256": record["runtime_state_SHA256"],
        "activation_action_SHA256": record["activation_action_SHA256"],
        "governed_autonomy_envelope_SHA256": record["governed_autonomy_envelope_SHA256"],
        "governed_autonomy_runtime_status": record["governed_autonomy_runtime_status"],
        "runtime_decision": record["runtime_decision"],
        "runtime_goal_SHA256": record["runtime_goal_SHA256"],
        "previous_runtime_state_SHA256": record.get("previous_runtime_state_SHA256"),
        "runtime_goal_excerpt": record["runtime_goal_excerpt"],
        "latest_decision_evidence": record["latest_decision_evidence"],
        "fresh_execution_requested": bool(record.get("fresh_execution_requested")),
        "fresh_execution_request_SHA256": record.get("fresh_execution_request_SHA256"),
        "fresh_execution_request_reference": record.get("fresh_execution_request_reference"),
        "execution_attempt_reason": record.get("execution_attempt_reason"),
        "prior_terminal_run_id": record.get("prior_terminal_run_id"),
        "process_continuation_count": _effective_governed_autonomy_process_continuation_count(record),
        "recorded_process_continuation_count": record["process_continuation_count"],
        "self_repair_count": record["self_repair_count"],
        "task_local_tool_candidate_count": record["task_local_tool_candidate_count"],
        "command_evaluation_count": record["command_evaluation_count"],
        "A2A_delegation_count": record["A2A_delegation_count"],
        "validation_failure_count": record["validation_failure_count"],
        "no_progress_count": record["no_progress_count"],
        "latest_no_progress_fingerprint_SHA256": record["latest_no_progress_fingerprint_SHA256"],
        "progress_marker_SHA256s": record["progress_marker_SHA256s"],
        "budget_limits": record["budget_limits"],
        "budget_remaining": record["budget_remaining"],
        "budget_exhausted": record["budget_exhausted"],
        "blocker_code": record.get("blocker_code"),
        "blocker_detail": record.get("blocker_detail"),
        "next_autonomous_action": record.get("next_autonomous_action"),
        "next_human_action": record.get("next_human_action"),
        "source_run_id": record.get("source_run_id"),
        "source_run_status": record.get("source_run_status"),
        "source_run_outcome": record.get("source_run_outcome"),
        "historical_source_run_immutable": record.get("historical_source_run_immutable"),
        "legacy_human_recovery_retry_micro_gates_required": record[
            "legacy_human_recovery_retry_micro_gates_required"
        ],
        "legacy_run_mutation_performed": record["legacy_run_mutation_performed"],
        "kanban_run_created": bool(record.get("kanban_run_created")),
        "kanban_run_id": record.get("kanban_run_id"),
        "workspace_path": record.get("workspace_path"),
        "dispatch_performed": bool(record.get("dispatch_performed")),
        "execution_started": bool(record.get("execution_started")),
        "worker_execution": bool(record.get("worker_execution")),
        "worker_process_started": bool(record.get("worker_process_started")),
        "Kanban_dispatch": bool(record.get("Kanban_dispatch")),
        "lineage_dispatch_performed": bool(record.get("lineage_dispatch_performed")),
        "current_invocation_side_effects": record["current_invocation_side_effects"],
        "provider_dispatch_count": record["provider_dispatch_count"],
        "model_inference_count": record["model_inference_count"],
        "Git_mutation": record["Git_mutation"],
        "auto_retry": record["auto_retry"],
        "auto_rollback": record["auto_rollback"],
    }
    return _governed_autonomy_apply_terminal_reconciliation(
        summary,
        terminal_reconciliation,
    )


def _governed_autonomy_runtime_operational_result(
    record: dict[str, Any],
    *,
    activation_record: dict[str, Any],
    idempotent_replay: bool,
    effective_authority: dict[str, Any] | None = None,
) -> dict[str, Any]:
    task_visibility, runs = _governed_autonomy_kanban_visibility(record)
    terminal_reconciliation = _governed_autonomy_runtime_terminal_reconciliation(
        record,
        effective_authority=effective_authority,
    )
    result = {
        "source_system": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SOURCE_SYSTEM,
        "schema_version": PEPPER_GOVERNED_AUTONOMY_RUNTIME_SCHEMA_VERSION,
        "policy_id": PEPPER_GOVERNED_AUTONOMY_RUNTIME_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "activation_action_SHA256": activation_record["activation_action_SHA256"],
        "runtime_state_SHA256": record["runtime_state_SHA256"],
        "previous_runtime_state_SHA256": record.get("previous_runtime_state_SHA256"),
        "governed_autonomy_activation_recorded": True,
        "governed_autonomy_envelope_SHA256": record["governed_autonomy_envelope_SHA256"],
        "governed_autonomy_status": activation_record["governed_autonomy_status"],
        "governed_autonomy_runtime_status": record["governed_autonomy_runtime_status"],
        "runtime_decision": record["runtime_decision"],
        "authority_revalidated": record["authority_revalidated"],
        "same_authority_subset_validated": record["same_authority_subset_validated"],
        "latest_decision_evidence": record["latest_decision_evidence"],
        "fresh_execution_requested": bool(record.get("fresh_execution_requested")),
        "fresh_execution_request_SHA256": record.get("fresh_execution_request_SHA256"),
        "fresh_execution_request_reference": record.get("fresh_execution_request_reference"),
        "execution_attempt_reason": record.get("execution_attempt_reason"),
        "prior_terminal_run_id": record.get("prior_terminal_run_id"),
        "process_continuation_count": _effective_governed_autonomy_process_continuation_count(record),
        "recorded_process_continuation_count": record["process_continuation_count"],
        "self_repair_count": record["self_repair_count"],
        "task_local_tool_candidate_count": record["task_local_tool_candidate_count"],
        "command_evaluation_count": record["command_evaluation_count"],
        "A2A_delegation_count": record["A2A_delegation_count"],
        "validation_failure_count": record["validation_failure_count"],
        "no_progress_count": record["no_progress_count"],
        "budget_limits": record["budget_limits"],
        "budget_remaining": record["budget_remaining"],
        "budget_exhausted": record["budget_exhausted"],
        "blocker_code": record.get("blocker_code"),
        "blocker_detail": record.get("blocker_detail"),
        "next_autonomous_action": record.get("next_autonomous_action"),
        "next_human_action": record.get("next_human_action"),
        "source_run_id": record.get("source_run_id"),
        "historical_source_run_immutable": record.get("historical_source_run_immutable"),
        "legacy_human_recovery_retry_micro_gates_required": record[
            "legacy_human_recovery_retry_micro_gates_required"
        ],
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_run_count": len(runs),
        "kanban_run_created": bool(record.get("kanban_run_created")),
        "kanban_run_id": record.get("kanban_run_id"),
        "workspace_path": record.get("workspace_path"),
        "task": task_visibility,
        "runs": runs,
        "dispatch_performed": bool(record.get("dispatch_performed")),
        "execution_started": bool(record.get("execution_started")),
        "worker_execution": bool(record.get("worker_execution")),
        "worker_process_started": bool(record.get("worker_process_started")),
        "Kanban_dispatch": bool(record.get("Kanban_dispatch")),
        "lineage_dispatch_performed": bool(record.get("lineage_dispatch_performed")),
        "A2A_dispatch_performed": bool(record.get("A2A_dispatch_performed")),
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "current_invocation_side_effects": record["current_invocation_side_effects"],
        "governed_autonomy_runtime": _governed_autonomy_runtime_summary(
            record,
            terminal_reconciliation=terminal_reconciliation,
            effective_authority=effective_authority,
        ),
        "live_autonomous_continuation_marker": record.get("live_autonomous_continuation_marker"),
        "human_smoke_marker": record["human_smoke_marker"],
    }
    return _governed_autonomy_apply_terminal_reconciliation(
        result,
        terminal_reconciliation,
    )


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
    ticket_id = str(record["ticket_id"])
    path = recovery_action_record_path_for_ticket(ticket_id)
    _archive_existing_authority_record(
        path,
        recovery_action_history_path_for_ticket(ticket_id),
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


def _governed_autonomy_activation_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "activation_action_SHA256"
    }
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(
        f"{PEPPER_GOVERNED_AUTONOMY_ACTION_DIGEST_ALGORITHM}\n{data}".encode("utf-8")
    ).hexdigest()


def _governed_autonomy_runtime_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "runtime_state_SHA256"
    }
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(
        f"{PEPPER_GOVERNED_AUTONOMY_RUNTIME_DIGEST_ALGORITHM}\n{data}".encode("utf-8")
    ).hexdigest()


def _persist_retry_start_record(record: dict[str, Any]) -> None:
    validate_p18_9_0_retry_start_record(record)
    ticket_id = str(record["ticket_id"])
    path = retry_start_record_path_for_ticket(ticket_id)
    _archive_existing_authority_record(
        path,
        retry_start_history_path_for_ticket(ticket_id),
        reason="replaced_by_current_recovery_cycle",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _persist_governed_autonomy_activation_record(record: dict[str, Any]) -> None:
    validate_governed_autonomy_activation_record(record)
    ticket_id = str(record["ticket_id"])
    path = governed_autonomy_activation_record_path_for_ticket(ticket_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _persist_governed_autonomy_runtime_state(record: dict[str, Any]) -> None:
    validate_governed_autonomy_runtime_state_record(record)
    ticket_id = str(record["ticket_id"])
    path = governed_autonomy_runtime_state_path_for_ticket(ticket_id)
    _archive_existing_authority_record(
        path,
        governed_autonomy_runtime_history_path_for_ticket(ticket_id),
        reason="replaced_by_next_governed_autonomy_continuation",
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
        record = load_current_ticket_recovery_action_record(projection_record=projection)
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": f"{binding.ticket_hyphen_token}-RECOVERY-AUTHORITY",
            "status": "blocked_by_invalid_recovery_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    if not _recovery_record_matches_current_failure(projection, record):
        return None, None
    if start_overlay.get("workflow_status") != "execution_failed":
        return None, {
            "id": f"{binding.ticket_hyphen_token}-RECOVERY-AUTHORITY",
            "status": "blocked_by_recovery_state_mismatch",
            "evidence": f"{binding.ticket_id} recovery authority exists but execution is not failed",
        }
    return {
        "readiness": "execution_failed_retry_pending",
        "workflow_state": f"{binding.ticket_id}-RETRY-PENDING-NOT-DISPATCHED",
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
                "a separate governed retry-start authorization is required before a new run."
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
        recovery = load_current_ticket_recovery_action_record(projection_record=projection)
        if recovery is None:
            return None, None
        record = load_current_ticket_retry_start_record(
            projection_record=projection,
            recovery_record=recovery,
            allow_historical_mismatch=True,
        )
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": f"{binding.ticket_hyphen_token}-RETRY-START-AUTHORITY",
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
            "workflow_state": f"{binding.ticket_id}-RETRY-PENDING-NOT-DISPATCHED",
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
            "next_action_id": binding.execution_recovery_next_action_id,
            "outcome": "state_unavailable",
        }
        task = None
        runs = []
    authority["kanban_run_id"] = getattr(task, "current_run_id", None) or record.get("kanban_run_id")
    if terminal_state is not None and terminal_state["start_status"] != "completed":
        blocker = {
            "id": f"{binding.ticket_hyphen_token}-RETRY-WORKER-LIFECYCLE",
            "status": "blocked_by_worker_lifecycle_failure",
            "evidence": terminal_state["blocker_detail"],
            "outcome": terminal_state.get("outcome"),
            "failure_category": terminal_state.get("failure_category"),
            "failure_summary": terminal_state.get("failure_summary"),
        }
        return {
            "readiness": "retry_execution_failed_recovery_required",
            "workflow_state": f"{binding.ticket_id}-RETRY-EXECUTION-FAILED-RECOVERY-REQUIRED",
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
                "id": binding.execution_recovery_next_action_id,
                "label": (
                    f"{binding.ticket_id} retry execution failed; governed recovery "
                    "authorization is required before another action."
                ),
                "target_ticket_id": binding.ticket_id,
                "target_ticket_title": binding.ticket_title,
            },
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }, blocker
    if terminal_state is not None and terminal_state["start_status"] == "completed":
        return {
            "readiness": "retry_execution_completed",
            "workflow_state": f"{binding.ticket_id}-RETRY-EXECUTION-COMPLETED",
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
                "id": binding.review_prepare_next_action_id,
                "label": f"{binding.ticket_id} retry execution completed; prepare review validation.",
                "target_ticket_id": binding.ticket_id,
                "target_ticket_title": binding.ticket_title,
            },
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }, None
    return {
        "readiness": "retry_execution_started",
        "workflow_state": f"{binding.ticket_id}-EXECUTING",
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
            "id": binding.monitor_execution_next_action_id,
            "label": (
                f"{binding.ticket_id} retry execution has started; monitor the Kanban run "
                "and await worker completion."
            ),
            "target_ticket_id": binding.ticket_id,
            "target_ticket_title": binding.ticket_title,
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


def _current_ticket_governed_autonomy_overlay(
    projection: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    binding = resolve_current_ticket_lifecycle_binding(projection_record=projection)
    try:
        record = load_current_ticket_governed_autonomy_activation_record(
            projection_record=projection,
        )
    except Exception as exc:  # pragma: no cover - defensive live-state guard
        return None, {
            "id": f"{binding.ticket_hyphen_token}-GOVERNED-AUTONOMY-AUTHORITY",
            "status": "blocked_by_invalid_governed_autonomy_authority",
            "evidence": _safe_text(exc, limit=300),
        }
    if record is None:
        return None, None
    result = _governed_autonomy_activation_operational_result(
        record,
        idempotent_replay=True,
    )
    runtime_state = load_current_ticket_governed_autonomy_runtime_state(
        projection_record=projection,
        activation_record=record,
    )
    effective_authority = _resolve_effective_current_governed_autonomy_authority(
        projection=projection,
        activation=record,
        previous=runtime_state,
    )
    terminal_reconciliation = (
        _governed_autonomy_runtime_terminal_reconciliation(
            runtime_state,
            effective_authority=effective_authority,
        )
        if runtime_state is not None
        else None
    )
    runtime_summary = (
        _governed_autonomy_runtime_summary(
            runtime_state,
            terminal_reconciliation=terminal_reconciliation,
            effective_authority=effective_authority,
        )
        if runtime_state is not None
        else None
    )
    active_governed_run = _governed_autonomy_active_execution_replay(
        runtime_state,
        projection,
    )
    continue_next_action = {
        "id": governed_autonomy_continuation_action_id(binding.ticket_id),
        "label": (
            f"{binding.ticket_id} governed autonomy is active; continue under the "
            "same backend-derived authority through the canonical runtime."
        ),
        "target_ticket_id": binding.ticket_id,
        "target_ticket_title": binding.ticket_title,
        "authority": "backend_derived_governed_autonomy_continuation",
    }
    expose_continue_action = (
        not active_governed_run
        and effective_authority["continuation_eligible"]
        and (
            runtime_state is None
            or (
                runtime_state.get("governed_autonomy_runtime_status")
                in {
                    "direct_continuation_recorded",
                    "a2a_delegation_completed",
                    "task_local_self_extension_completed",
                    "task_local_self_extension_materialized",
                }
                and runtime_state.get("budget_exhausted") is not True
                and runtime_state.get("blocker_code") in {None, ""}
            )
            or (
                runtime_state is not None
                and not _governed_autonomy_runtime_record_consumed_process(runtime_state)
                and runtime_state.get("budget_exhausted") is not True
                and runtime_state.get("blocker_code") in {None, ""}
            )
            or (
                terminal_reconciliation is not None
                and terminal_reconciliation.get("validation_infrastructure_failure") is True
            )
        )
    )
    summary = {
        "source_system": result["source_system"],
        "policy_id": result["policy_id"],
        "activation_action_SHA256": result["activation_action_SHA256"],
        "governed_autonomy_activation_origin": result[
            "governed_autonomy_activation_origin"
        ],
        "legacy_activation_compatibility_applied": result[
            "legacy_activation_compatibility_applied"
        ],
        "historical_activation_record_preserved": result[
            "historical_activation_record_preserved"
        ],
        "historical_runtime_limitation_classification": result[
            "historical_runtime_limitation_classification"
        ],
        "effective_live_lineage_activation_authorized": result[
            "effective_live_lineage_activation_authorized"
        ],
        "additional_human_activation_required": result[
            "additional_human_activation_required"
        ],
        "authority_revalidated": result["authority_revalidated"],
        "effective_authority_revalidated": effective_authority[
            "authority_revalidated"
        ],
        "continuation_eligible": effective_authority["continuation_eligible"],
        "effective_authority_diagnostics": effective_authority["diagnostics"],
        "governed_autonomy_status": result["governed_autonomy_status"],
        "governed_autonomy_policy_id": result["governed_autonomy_policy_id"],
        "governed_autonomy_envelope_SHA256": result["governed_autonomy_envelope_SHA256"],
        "backend_derived_live_authority_SHA256": result[
            "backend_derived_live_authority_SHA256"
        ],
        "authority_derivation_source": result["authority_derivation_source"],
        "01AH_envelope_lifecycle_classification": result[
            "01AH_envelope_lifecycle_classification"
        ],
        "capability_gap_SHA256": result.get("capability_gap_SHA256"),
        "continuation_lineage_SHA256": result.get("continuation_lineage_SHA256"),
        "same_authority_subset_validated": result["same_authority_subset_validated"],
        "same_authority_delegation_policy_id": result["same_authority_delegation_policy_id"],
        "same_authority_delegation_status": result["same_authority_delegation_status"],
        "same_authority_delegation_authorized": result["same_authority_delegation_authorized"],
        "same_authority_delegation_blocker_code": result[
            "same_authority_delegation_blocker_code"
        ],
        "live_lineage_activation_authorized": result["live_lineage_activation_authorized"],
        "live_lineage_activation_status": result["live_lineage_activation_status"],
        "live_lineage_activation_blocker_code": result["live_lineage_activation_blocker_code"],
        "historical_live_lineage_activation_authorized": result[
            "historical_live_lineage_activation_authorized"
        ],
        "historical_live_lineage_activation_status": result[
            "historical_live_lineage_activation_status"
        ],
        "historical_live_lineage_activation_blocker_code": result[
            "historical_live_lineage_activation_blocker_code"
        ],
        "governed_autonomy_runtime_status": (
            runtime_state["governed_autonomy_runtime_status"]
            if runtime_state is not None
            else "active_authority_ready_for_continuation"
        ),
        "runtime_decision": runtime_state["runtime_decision"] if runtime_state is not None else None,
        "runtime_state_SHA256": runtime_state["runtime_state_SHA256"] if runtime_state is not None else None,
        "process_continuation_count": (
            _effective_governed_autonomy_process_continuation_count(runtime_state)
            if runtime_state is not None
            else 0
        ),
        "recorded_process_continuation_count": (
            runtime_state["process_continuation_count"] if runtime_state is not None else 0
        ),
        "self_repair_count": runtime_state["self_repair_count"] if runtime_state is not None else 0,
        "A2A_delegation_count": (
            runtime_state["A2A_delegation_count"] if runtime_state is not None else 0
        ),
        "validation_failure_count": (
            runtime_state["validation_failure_count"] if runtime_state is not None else 0
        ),
        "budget_exhausted": runtime_state["budget_exhausted"] if runtime_state is not None else False,
        "fresh_execution_requested": bool(runtime_state.get("fresh_execution_requested"))
        if runtime_state is not None
        else False,
        "fresh_execution_request_SHA256": (
            runtime_state.get("fresh_execution_request_SHA256")
            if runtime_state is not None
            else None
        ),
        "fresh_execution_request_reference": (
            runtime_state.get("fresh_execution_request_reference")
            if runtime_state is not None
            else None
        ),
        "execution_attempt_reason": (
            runtime_state.get("execution_attempt_reason")
            if runtime_state is not None
            else None
        ),
        "prior_terminal_run_id": (
            runtime_state.get("prior_terminal_run_id")
            if runtime_state is not None
            else None
        ),
        "next_autonomous_action": (
            runtime_state.get("next_autonomous_action")
            if runtime_state is not None
            else "call continue_current_ticket_governed_autonomy with the active server-derived authority"
        ),
        "next_human_action": runtime_state.get("next_human_action") if runtime_state is not None else None,
        "dispatch_performed": bool(runtime_state.get("dispatch_performed"))
        if runtime_state is not None
        else False,
        "execution_started": bool(runtime_state.get("execution_started"))
        if runtime_state is not None
        else False,
        "worker_execution": bool(runtime_state.get("worker_execution"))
        if runtime_state is not None
        else False,
        "Kanban_dispatch": bool(runtime_state.get("Kanban_dispatch"))
        if runtime_state is not None
        else False,
        "lineage_dispatch_performed": bool(runtime_state.get("lineage_dispatch_performed"))
        if runtime_state is not None
        else False,
        "A2A_dispatch_performed": (
            bool(runtime_state.get("A2A_dispatch_performed")) if runtime_state is not None else False
        ),
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
        "kanban_run_count": result["kanban_run_count"],
        "kanban_run_created": bool(runtime_state.get("kanban_run_created"))
        if runtime_state is not None
        else False,
        "kanban_run_id": runtime_state.get("kanban_run_id") if runtime_state is not None else None,
        "workspace_path": runtime_state.get("workspace_path") if runtime_state is not None else None,
        "live_autonomous_continuation_marker": (
            runtime_state.get("live_autonomous_continuation_marker")
            if runtime_state is not None
            else None
        ),
        "human_smoke_marker": result["human_smoke_marker"],
        "runtime": runtime_summary,
    }
    _governed_autonomy_apply_terminal_reconciliation(
        summary,
        terminal_reconciliation,
    )
    overlay = {
        "governed_autonomy_activation_recorded": True,
        "governed_autonomy_status": result["governed_autonomy_status"],
        "governed_autonomy_activation_origin": result[
            "governed_autonomy_activation_origin"
        ],
        "legacy_activation_compatibility_applied": result[
            "legacy_activation_compatibility_applied"
        ],
        "historical_activation_record_preserved": result[
            "historical_activation_record_preserved"
        ],
        "effective_live_lineage_activation_authorized": result[
            "effective_live_lineage_activation_authorized"
        ],
        "governed_autonomy_envelope_SHA256": result["governed_autonomy_envelope_SHA256"],
        "backend_derived_live_authority_SHA256": result[
            "backend_derived_live_authority_SHA256"
        ],
        "governed_autonomy_live_lineage_activation_authorized": result[
            "live_lineage_activation_authorized"
        ],
        "governed_autonomy_live_lineage_activation_status": result[
            "live_lineage_activation_status"
        ],
        "governed_autonomy_same_authority_delegation_status": result[
            "same_authority_delegation_status"
        ],
        "governed_autonomy_runtime_status": summary["governed_autonomy_runtime_status"],
        "governed_autonomy_effective_authority_revalidated": bool(
            summary.get("effective_authority_revalidated")
        ),
        "governed_autonomy_continuation_eligible": bool(
            summary.get("continuation_eligible")
        ),
        "governed_autonomy_runtime_decision": summary["runtime_decision"],
        "governed_autonomy_runtime_state_SHA256": summary["runtime_state_SHA256"],
        "A2A_dispatch_performed": summary["A2A_dispatch_performed"],
        "lineage_dispatch_performed": summary["lineage_dispatch_performed"],
        "governed_autonomy_terminal_run_reconciled": bool(
            summary.get("terminal_run_reconciled")
        ),
        "governed_autonomy_validation_infrastructure_failure": bool(
            summary.get("validation_infrastructure_failure")
        ),
        "governed_autonomy": summary,
    }
    if (
        terminal_reconciliation is not None
        and terminal_reconciliation.get("next_action") is not None
    ):
        terminal_next_action = dict(terminal_reconciliation["next_action"])
        if terminal_next_action.get("id") == governed_autonomy_continuation_action_id(
            binding.ticket_id,
        ):
            terminal_next_action.setdefault(
                "label",
                (
                    f"{binding.ticket_id} governed-autonomy run reached terminal validation "
                    "infrastructure failure; continue under the same authority without creating a new run."
                ),
            )
            overlay.update({
                "readiness": "governed_autonomy_execution_terminal_reconciled",
                "workflow_state": f"{binding.ticket_id}-GOVERNED-AUTONOMY-TERMINAL-VALIDATION-REPAIRABLE",
                "workflow_status": "governed_autonomy_validation_repairable",
                "queue_state": "governed_autonomy_kanban_execution_terminal",
                "execution_state": "no_active_executions",
                "active_execution_count": 0,
                "validation_state": "governed_autonomy_validation_infrastructure_repairable",
                "review_state": "candidate_available_pending_governed_validation",
                "recovery_state": "not_required_same_authority_reconciliation_available",
                "next_action": terminal_next_action,
            })
        else:
            terminal_next_action.setdefault(
                "label",
                f"{binding.ticket_id} governed-autonomy execution completed; prepare review validation.",
            )
            overlay.update({
                "readiness": "governed_autonomy_execution_completed",
                "workflow_state": f"{binding.ticket_id}-GOVERNED-AUTONOMY-EXECUTION-COMPLETED",
                "workflow_status": "execution_completed",
                "queue_state": "governed_autonomy_kanban_execution_terminal",
                "execution_state": "no_active_executions",
                "active_execution_count": 0,
                "validation_state": "execution_completed_pending_validation",
                "review_state": "ready_for_review_validation",
                "recovery_state": "not_required",
                "next_action": terminal_next_action,
            })
    elif terminal_reconciliation is not None:
        overlay.update({
            "readiness": "governed_autonomy_execution_terminal_reconciled",
            "workflow_state": f"{binding.ticket_id}-GOVERNED-AUTONOMY-TERMINAL-VALIDATION-BLOCKED",
            "workflow_status": "governed_autonomy_validation_blocked",
            "queue_state": "governed_autonomy_kanban_execution_terminal",
            "execution_state": "no_active_executions",
            "active_execution_count": 0,
            "validation_state": "governed_autonomy_validation_blocked",
            "review_state": "candidate_available_validation_blocked",
            "recovery_state": "terminal_governed_run_review_required",
            "next_action": {
                "id": governed_autonomy_continuation_action_id(binding.ticket_id),
                "label": (
                    f"{binding.ticket_id} governed-autonomy run reached terminal validation blockage "
                    "after worker execution; inspect evidence or provide an explicit fresh-execution request."
                ),
                "target_ticket_id": binding.ticket_id,
                "target_ticket_title": binding.ticket_title,
                "authority": "backend_derived_governed_autonomy_continuation",
                "required_human_action": "terminal_governed_run_review_or_fresh_execution_request",
            },
        })
    elif expose_continue_action:
        overlay["next_action"] = continue_next_action
    elif not effective_authority["continuation_eligible"]:
        overlay.update({
            "readiness": "blocked_governed_autonomy_authority_mismatch",
            "workflow_state": f"{binding.ticket_id}-GOVERNED-AUTONOMY-AUTHORITY-MISMATCH",
            "workflow_status": "blocked_governed_autonomy_authority_mismatch",
            "queue_state": "blocked_governed_autonomy_authority_mismatch",
            "execution_state": "no_authorized_governed_continuation",
            "recovery_state": "requires_authority_review",
            "blocker_code": "CONTINUATION_AUTHORITY_MISMATCH",
            "blocker_detail": effective_authority["diagnostics"].get("reason"),
        })
    return overlay, None


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
    current_ticket_id = str(snapshot.get("current_ticket_id") or "").strip()
    if current_ticket_id:
        try:
            projection = _load_current_projection_record()
            if projection.get("ticket_id") == current_ticket_id:
                autonomy_overlay, autonomy_blocker = _current_ticket_governed_autonomy_overlay(
                    projection,
                )
                if autonomy_overlay is not None:
                    snapshot.update(autonomy_overlay)
                if autonomy_blocker is not None:
                    remaining_blockers.append(autonomy_blocker)
        except Exception as exc:  # pragma: no cover - defensive live-state guard
            remaining_blockers.append({
                "id": f"{current_ticket_id}-GOVERNED-AUTONOMY-AUTHORITY",
                "status": "blocked_by_unreadable_governed_autonomy_projection",
                "evidence": _safe_text(exc, limit=300),
            })
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
        "governed_autonomy_status": workflow.get("governed_autonomy_status"),
        "governed_autonomy": workflow.get("governed_autonomy"),
        "governed_autonomy_live_lineage_activation_status": workflow.get(
            "governed_autonomy_live_lineage_activation_status"
        ),
        "governed_autonomy_same_authority_delegation_status": workflow.get(
            "governed_autonomy_same_authority_delegation_status"
        ),
        "governed_autonomy_runtime_status": workflow.get("governed_autonomy_runtime_status"),
        "governed_autonomy_runtime_decision": workflow.get("governed_autonomy_runtime_decision"),
        "governed_autonomy_runtime_state_SHA256": workflow.get(
            "governed_autonomy_runtime_state_SHA256"
        ),
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
