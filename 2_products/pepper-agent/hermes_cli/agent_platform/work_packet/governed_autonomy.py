"""Governed task-local autonomy for Pepper WorkPacket workers.

01AH adds a capability-repair layer that can create and run task-local helper
tools inside an already-approved WorkPacket scope. It does not expose Hermes'
global dynamic tool registry, plugins, skills, MCP, arbitrary shell execution,
Git, Docker, Graphify, package installs, network access, provider calls, or
model calls.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.work_packet.compiler import (
    WorkPacketCompilationResult,
    WorkPacketGitAuthority,
    validate_work_packet,
)
from hermes_cli.agent_platform.work_packet.single_agent_execution import (
    SingleAgentExecutionResult,
    validate_single_agent_execution_result,
)
from hermes_cli.agent_platform.work_packet.tool_permissions import (
    ToolPermissionCheckRequest,
    ToolPermissionDecision,
    ToolPermissionDecisionEvidence,
    ToolPermissionOperation,
    ToolPermissionProfile,
    ToolPermissionProfileResult,
    evaluate_tool_permission,
    validate_tool_permission_profile,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocation,
    WorkspaceAllocationResult,
    validate_workspace_allocation,
)
from tools import governed_workpacket_file_guard as file_guard


GOVERNED_AUTONOMY_SCHEMA_VERSION = 1
GOVERNED_AUTONOMY_POLICY_ID = "pepper-governed-task-local-autonomy-v1"
GOVERNED_AUTONOMY_BOUNDARY_CLASSIFICATION = "CAPABILITY != AUTHORITY"
GOVERNED_AUTONOMY_ENVIRONMENT_POLICY_ID = (
    "pepper-minimal-task-local-autonomy-command-environment-v1"
)

ENVELOPE_DIGEST_ALGORITHM = "agent-platform-governed-autonomy-envelope-sha256-v1"
REUSE_ASSESSMENT_DIGEST_ALGORITHM = (
    "agent-platform-governed-autonomy-reuse-assessment-sha256-v1"
)
GAP_DIGEST_ALGORITHM = "agent-platform-governed-autonomy-gap-sha256-v1"
CONTRACT_DIGEST_ALGORITHM = "agent-platform-governed-autonomy-contract-sha256-v1"
CANDIDATE_DIGEST_ALGORITHM = "agent-platform-governed-autonomy-tool-candidate-sha256-v1"
MATERIALIZATION_DIGEST_ALGORITHM = (
    "agent-platform-governed-autonomy-tool-materialization-sha256-v1"
)
COMMAND_PROPOSAL_DIGEST_ALGORITHM = (
    "agent-platform-governed-autonomy-command-proposal-sha256-v1"
)
COMMAND_EVALUATION_DIGEST_ALGORITHM = (
    "agent-platform-governed-autonomy-command-evaluation-sha256-v1"
)
STREAM_DIGEST_ALGORITHM = "agent-platform-governed-autonomy-captured-stream-sha256-v1"
COMMAND_EXECUTION_DIGEST_ALGORITHM = (
    "agent-platform-governed-autonomy-command-execution-sha256-v1"
)
CONTINUATION_DIGEST_ALGORITHM = (
    "agent-platform-governed-autonomy-continuation-lineage-sha256-v1"
)

MAX_SOURCE_BYTES = 65_536
MAX_SOURCE_COMMAND_CHARACTERS = 4_096
MAX_ARGV_TOKENS = 64
MAX_STDOUT_BYTES = 262_144
MAX_STDERR_BYTES = 262_144
RETAINED_STDOUT_BYTES = 65_536
RETAINED_STDERR_BYTES = 65_536
OUTPUT_CHUNK_BYTES = 8_192
TERMINATION_GRACE_SECONDS = 2.0

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{0,127}$"
_TOOL_NAME_PATTERN = r"^[A-Za-z][A-Za-z0-9_]{2,63}$"
_DRIVE_PATH_PATTERN = re.compile(r"^[A-Za-z]:")
_CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
_ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_URL_PATTERN = re.compile(r"https?://|ssh://|git@", re.IGNORECASE)
_ENV_ASSIGNMENT_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_SECRET_PATTERNS = (
    re.compile(r"Authorization:\s*Bearer\s+\S+", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE),
    re.compile(r"access_token\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"refresh_token\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"password\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"client_secret\s*=\s*[^\s]+", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
        re.DOTALL,
    ),
)
_SECRET_COMMAND_MARKERS = (
    "authorization: bearer",
    "access_token=",
    "refresh_token=",
    "-----begin private key-----",
    "-----begin rsa private key-----",
    "password=",
    "client_secret=",
)
_FORBIDDEN_SHELL_MARKERS = ("||", "&&", "<<", ">>", "$(", "${")
_FORBIDDEN_SHELL_TOKENS = ("|", "&", ";", ">", "<", "`")
_FORBIDDEN_GIT_TOKENS = {"git", "gh"}
_FORBIDDEN_DOCKER_TOKENS = {"docker", "docker-compose", "podman"}
_FORBIDDEN_GRAPHIFY_TOKENS = {"graphify"}
_FORBIDDEN_PACKAGE_TOKENS = {
    "npm",
    "npx",
    "pnpm",
    "yarn",
    "corepack",
    "pip",
    "uv",
    "poetry",
    "pipenv",
}
_FORBIDDEN_NETWORK_TOKENS = {
    "curl",
    "wget",
    "ssh",
    "scp",
    "rsync",
    "ftp",
}
_PACKAGE_INSTALL_VERBS = {"install", "add", "update", "upgrade", "sync"}
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
_FIXED_ENVIRONMENT = (
    ("NO_COLOR", "1"),
    ("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1"),
    ("PYTHONDONTWRITEBYTECODE", "1"),
    ("PYTHONHASHSEED", "0"),
    ("PYTHONIOENCODING", "utf-8"),
    ("PYTHONNOUSERSITE", "1"),
    ("PYTHONUTF8", "1"),
)
_INHERITED_ENVIRONMENT_ALLOWLIST = (
    "LANG",
    "LC_ALL",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "WINDIR",
)


class GovernedAutonomyError(ValueError):
    """Base error for governed autonomy failures."""


class GovernedAutonomyInputError(GovernedAutonomyError):
    """Raised when supplied autonomy inputs are structurally invalid."""


class GovernedAutonomyIntegrityError(GovernedAutonomyError):
    """Raised when deterministic autonomy evidence fails integrity checks."""


class GovernedAutonomyPolicyError(GovernedAutonomyError):
    """Raised when an autonomy action would cross its authority boundary."""


class GovernedAutonomyExecutionError(GovernedAutonomyError):
    """Raised when a bounded task-local command cannot be controlled."""


class GovernedAutonomyStateError(GovernedAutonomyError):
    """Raised when an autonomy continuation cannot advance."""


class GovernedAutonomyReuseDisposition(str, Enum):
    HERMES_REUSED = "HERMES_REUSED"
    HERMES_ADAPTED = "HERMES_ADAPTED"
    PEPPER_NEW = "PEPPER_NEW"


class CapabilityGapKind(str, Enum):
    MISSING_TASK_LOCAL_TOOL = "missing_task_local_tool"
    COMMAND_SHAPE_UNSUPPORTED = "command_shape_unsupported"
    GIT_AUTHORITY_REQUIRED = "git_authority_required"
    CREDENTIAL_AUTHORITY_REQUIRED = "credential_authority_required"
    NETWORK_AUTHORITY_REQUIRED = "network_authority_required"
    PACKAGE_INSTALL_AUTHORITY_REQUIRED = "package_install_authority_required"
    DOCKER_AUTHORITY_REQUIRED = "docker_authority_required"
    GRAPHIFY_AUTHORITY_REQUIRED = "graphify_authority_required"
    NOT_REPAIRABLE = "not_repairable"


class CapabilityGapDisposition(str, Enum):
    REPAIRABLE_TASK_LOCAL = "repairable_task_local"
    HUMAN_AUTHORITY_REQUIRED = "human_authority_required"
    NOT_REPAIRABLE = "not_repairable"


class TaskLocalToolLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"


class TaskLocalToolMaterializationState(str, Enum):
    MATERIALIZED = "materialized"


class AutonomyCommandDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class AutonomyCommandDenialReason(str, Enum):
    NONE = "none"
    EMPTY_COMMAND = "empty_command"
    COMMAND_TOO_LONG = "command_too_long"
    SHELL_SYNTAX = "shell_syntax"
    SECRET_SHAPED_TEXT = "secret_shaped_text"
    UNSUPPORTED_EXECUTABLE = "unsupported_executable"
    CANDIDATE_ENTRYPOINT_MISMATCH = "candidate_entrypoint_mismatch"
    GIT_AUTHORITY_REQUIRED = "git_authority_required"
    CREDENTIAL_AUTHORITY_REQUIRED = "credential_authority_required"
    NETWORK_AUTHORITY_REQUIRED = "network_authority_required"
    PACKAGE_INSTALL_AUTHORITY_REQUIRED = "package_install_authority_required"
    DOCKER_AUTHORITY_REQUIRED = "docker_authority_required"
    GRAPHIFY_AUTHORITY_REQUIRED = "graphify_authority_required"
    TARGET_SCOPE_DENIED = "target_scope_denied"
    TARGET_NOT_FOUND = "target_not_found"
    RUNTIME_UNAVAILABLE = "runtime_unavailable"


class AutonomyCommandDisposition(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"


class AutonomyCommandFailureReason(str, Enum):
    NONE = "none"
    NONZERO_EXIT = "nonzero_exit"
    TIMEOUT = "timeout"
    OUTPUT_LIMIT = "output_limit"
    LAUNCH_ERROR = "launch_error"


class AutonomyCommandStreamKind(str, Enum):
    STDOUT = "stdout"
    STDERR = "stderr"


class AutonomyContinuationState(str, Enum):
    READY = "ready"
    CONTINUING = "continuing"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class AutonomyContinuationStopReason(str, Enum):
    NONE = "none"
    BUDGET_EXHAUSTED = "budget_exhausted"
    NO_PROGRESS = "no_progress"
    COMMAND_FAILED = "command_failed"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


def _validate_repository_relative_path(value: str) -> str:
    value = _reject_nul(value.strip())
    if not value:
        raise ValueError("repository path must not be empty")
    if value.startswith("/") or _DRIVE_PATH_PATTERN.match(value):
        raise ValueError("repository path must be relative")
    if "\\" in value:
        raise ValueError("repository path must use forward slashes")
    if _CONTROL_CHARACTER_PATTERN.search(value):
        raise ValueError("repository path must not contain control characters")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError("repository path must not contain traversal components")
    return value


def _validate_source_text(value: str) -> str:
    value = _reject_nul(value)
    if len(value.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise ValueError("tool candidate source exceeds byte limit")
    if _contains_secret_marker(value):
        raise ValueError("tool candidate source contains secret-shaped text")
    return value


def _validate_bounded_command_text(value: str) -> str:
    value = _reject_nul(value.strip())
    if len(value) > MAX_SOURCE_COMMAND_CHARACTERS:
        raise ValueError("source command exceeds maximum length")
    return value


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=2048),
    AfterValidator(_reject_nul),
]
LongBoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=1, max_length=MAX_SOURCE_BYTES),
    AfterValidator(_validate_source_text),
]
BoundedIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=1, max_length=128, pattern=_IDENTIFIER_PATTERN),
]
ToolName: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=3, max_length=64, pattern=_TOOL_NAME_PATTERN),
]
RepositoryRelativePath: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_repository_relative_path),
]
SourceCommandText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=1, max_length=MAX_SOURCE_COMMAND_CHARACTERS),
    AfterValidator(_validate_bounded_command_text),
]


class _GovernedAutonomyModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class GovernedAutonomyBudget(_GovernedAutonomyModel):
    max_repair_attempts: int = Field(default=3, ge=1, le=12, strict=True)
    max_tool_candidates: int = Field(default=3, ge=1, le=12, strict=True)
    max_command_evaluations: int = Field(default=6, ge=1, le=24, strict=True)
    max_continuations: int = Field(default=6, ge=1, le=24, strict=True)
    max_no_progress_iterations: int = Field(default=2, ge=1, le=6, strict=True)


class GovernedAutonomyReuseAssessment(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    component: BoundedIdentifier
    disposition: GovernedAutonomyReuseDisposition
    rationale: BoundedText
    assessment_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_assessment(self) -> GovernedAutonomyReuseAssessment:
        if self.assessment_SHA256 != _reuse_assessment_digest(self):
            raise ValueError("assessment_SHA256 must match reuse assessment digest")
        return self


class GovernedAutonomyEnvelope(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    policy_id: Literal["pepper-governed-task-local-autonomy-v1"] = (
        GOVERNED_AUTONOMY_POLICY_ID
    )
    autonomy_enabled: Literal[True] = True
    capability_authority_boundary: Literal["CAPABILITY != AUTHORITY"] = (
        GOVERNED_AUTONOMY_BOUNDARY_CLASSIFICATION
    )
    live_lineage_activation_authorized: Literal[False] = False
    work_packet_id: BoundedIdentifier
    work_packet_SHA256: DigestText
    source_ticket_SHA256: DigestText
    ticket_id: BoundedIdentifier
    publication_revision: int = Field(ge=1, strict=True)
    allocation_id: BoundedIdentifier
    allocation_SHA256: DigestText
    profile_id: BoundedIdentifier
    profile_SHA256: DigestText
    single_agent_result_SHA256: DigestText
    allocation: WorkspaceAllocation
    profile: ToolPermissionProfile
    workspace_root: BoundedText
    resolved_workspace_root: BoundedText
    allowed_paths: tuple[RepositoryRelativePath, ...] = Field(min_length=1)
    forbidden_paths: tuple[RepositoryRelativePath, ...] = ()
    denied_operations: tuple[ToolPermissionOperation, ...] = Field(min_length=1)
    git_authority: Literal[WorkPacketGitAuthority.HUMAN_ONLY] = (
        WorkPacketGitAuthority.HUMAN_ONLY
    )
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    budget: GovernedAutonomyBudget
    envelope_SHA256: DigestText

    @field_validator("denied_operations", mode="after")
    @classmethod
    def _validate_unique_denied_operations(
        cls, value: tuple[ToolPermissionOperation, ...]
    ) -> tuple[ToolPermissionOperation, ...]:
        if len(value) != len(frozenset(value)):
            raise ValueError("denied operations must be unique")
        return value

    @model_validator(mode="after")
    def _validate_envelope(self) -> GovernedAutonomyEnvelope:
        required_denials = {
            ToolPermissionOperation.EXECUTE_COMMAND,
            ToolPermissionOperation.VALIDATION_COMMAND,
            ToolPermissionOperation.GIT_READ_ONLY,
            ToolPermissionOperation.GIT_MUTATION,
            ToolPermissionOperation.NETWORK_ACCESS,
            ToolPermissionOperation.WORKSPACE_MUTATION,
            ToolPermissionOperation.PROVIDER_CALL,
            ToolPermissionOperation.MODEL_CALL,
            ToolPermissionOperation.AGENT_CONTROL,
            ToolPermissionOperation.WORKER_CONTROL,
        }
        if not required_denials.issubset(set(self.denied_operations)):
            raise ValueError("autonomy envelope requires non-filesystem operations denied")
        if self.allocation.allocation_id != self.allocation_id:
            raise ValueError("allocation object must match envelope allocation ID")
        if self.allocation.allocation_SHA256 != self.allocation_SHA256:
            raise ValueError("allocation object must match envelope allocation digest")
        if self.profile.profile_id != self.profile_id:
            raise ValueError("profile object must match envelope profile ID")
        if self.profile.profile_SHA256 != self.profile_SHA256:
            raise ValueError("profile object must match envelope profile digest")
        if self.profile.allocation_id != self.allocation_id:
            raise ValueError("profile object must bind envelope allocation")
        if self.envelope_SHA256 != _envelope_digest(self):
            raise ValueError("envelope_SHA256 must match autonomy envelope digest")
        return self


class CapabilityGapEvidence(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    gap_id: BoundedIdentifier
    envelope_SHA256: DigestText
    kind: CapabilityGapKind
    disposition: CapabilityGapDisposition
    observed_failure: BoundedText
    requested_capability: BoundedText
    requested_command: SourceCommandText | None = None
    requires_human_authority: StrictBool
    rationale: BoundedText
    gap_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_gap(self) -> CapabilityGapEvidence:
        if self.disposition is CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED:
            if self.requires_human_authority is not True:
                raise ValueError("authority-required gaps must require human authority")
        elif self.requires_human_authority:
            raise ValueError("repairable gaps must not require human authority")
        if self.gap_SHA256 != _gap_digest(self):
            raise ValueError("gap_SHA256 must match capability gap digest")
        return self


class TaskLocalCapabilityContract(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    contract_id: BoundedIdentifier
    envelope_SHA256: DigestText
    gap_id: BoundedIdentifier
    gap_SHA256: DigestText
    tool_name: ToolName
    language: TaskLocalToolLanguage
    implementation_path: RepositoryRelativePath
    allowed_paths: tuple[RepositoryRelativePath, ...] = Field(min_length=1)
    forbidden_paths: tuple[RepositoryRelativePath, ...] = ()
    permitted_operations: tuple[ToolPermissionOperation, ...] = Field(min_length=1)
    allow_package_install: Literal[False] = False
    allow_network_access: Literal[False] = False
    allow_git_access: Literal[False] = False
    allow_provider_or_model_calls: Literal[False] = False
    contract_SHA256: DigestText

    @field_validator("permitted_operations", mode="after")
    @classmethod
    def _validate_permitted_operations(
        cls, value: tuple[ToolPermissionOperation, ...]
    ) -> tuple[ToolPermissionOperation, ...]:
        if len(value) != len(frozenset(value)):
            raise ValueError("permitted operations must be unique")
        forbidden = {
            ToolPermissionOperation.EXECUTE_COMMAND,
            ToolPermissionOperation.VALIDATION_COMMAND,
            ToolPermissionOperation.GIT_READ_ONLY,
            ToolPermissionOperation.GIT_MUTATION,
            ToolPermissionOperation.NETWORK_ACCESS,
            ToolPermissionOperation.WORKSPACE_MUTATION,
            ToolPermissionOperation.PROVIDER_CALL,
            ToolPermissionOperation.MODEL_CALL,
            ToolPermissionOperation.AGENT_CONTROL,
            ToolPermissionOperation.WORKER_CONTROL,
        }
        if set(value) & forbidden:
            raise ValueError("contract cannot permit non-filesystem authority")
        return value

    @model_validator(mode="after")
    def _validate_contract(self) -> TaskLocalCapabilityContract:
        if self.contract_SHA256 != _contract_digest(self):
            raise ValueError("contract_SHA256 must match task-local contract digest")
        return self


class ToolCandidate(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    candidate_id: BoundedIdentifier
    contract_id: BoundedIdentifier
    contract_SHA256: DigestText
    language: TaskLocalToolLanguage
    implementation_path: RepositoryRelativePath
    entrypoint: BoundedText
    dependencies: tuple[BoundedIdentifier, ...] = ()
    source_text: LongBoundedText
    source_SHA256: DigestText
    candidate_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_candidate(self) -> ToolCandidate:
        if self.dependencies:
            raise ValueError("task-local candidates cannot request dependencies")
        if self.source_SHA256 != _sha256_text(self.source_text):
            raise ValueError("source_SHA256 must match source text")
        _validate_language_path(self.language, self.implementation_path)
        if self.candidate_SHA256 != _candidate_digest(self):
            raise ValueError("candidate_SHA256 must match tool candidate digest")
        return self


class TaskLocalToolMaterializationResult(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    state: Literal[TaskLocalToolMaterializationState.MATERIALIZED] = (
        TaskLocalToolMaterializationState.MATERIALIZED
    )
    candidate_id: BoundedIdentifier
    candidate_SHA256: DigestText
    implementation_path: RepositoryRelativePath
    source_SHA256: DigestText
    byte_count: int = Field(ge=1, le=MAX_SOURCE_BYTES, strict=True)
    directory_permission_decision_SHA256: DigestText | None = None
    file_permission_decision_SHA256: DigestText
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    materialization_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_materialization(self) -> TaskLocalToolMaterializationResult:
        if self.materialization_SHA256 != _materialization_digest(self):
            raise ValueError("materialization_SHA256 must match materialization digest")
        return self


class AutonomyCommandProposal(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    proposal_id: BoundedIdentifier
    contract_id: BoundedIdentifier
    contract_SHA256: DigestText
    candidate_id: BoundedIdentifier
    candidate_SHA256: DigestText
    source_command: SourceCommandText
    working_directory: BoundedText
    timeout_seconds: int = Field(ge=1, le=120, strict=True)
    expected_exit_codes: tuple[int, ...] = (0,)
    shell: Literal[False] = False
    stdin_disabled: Literal[True] = True
    proposal_SHA256: DigestText

    @field_validator("expected_exit_codes", mode="before")
    @classmethod
    def _normalize_exit_codes(cls, value: object) -> tuple[int, ...]:
        if value is None:
            return (0,)
        if isinstance(value, int) and not isinstance(value, bool):
            values = (value,)
        else:
            values = tuple(value)  # type: ignore[arg-type]
        if not values:
            raise ValueError("expected exit codes must not be empty")
        normalized: list[int] = []
        for item in values:
            if not isinstance(item, int) or isinstance(item, bool):
                raise ValueError("expected exit codes must be integers")
            if item < 0 or item > 255:
                raise ValueError("expected exit code out of range")
            normalized.append(item)
        return tuple(sorted(frozenset(normalized)))

    @model_validator(mode="after")
    def _validate_proposal(self) -> AutonomyCommandProposal:
        if self.proposal_SHA256 != _command_proposal_digest(self):
            raise ValueError("proposal_SHA256 must match command proposal digest")
        return self


class AutonomyCommandEvaluation(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    decision: AutonomyCommandDecision
    denial_reason: AutonomyCommandDenialReason = AutonomyCommandDenialReason.NONE
    proposal_id: BoundedIdentifier
    proposal_SHA256: DigestText
    candidate_id: BoundedIdentifier
    candidate_SHA256: DigestText
    source_command: SourceCommandText
    effective_argv: tuple[BoundedText, ...] = ()
    working_directory: BoundedText
    timeout_seconds: int = Field(ge=1, le=120, strict=True)
    expected_exit_codes: tuple[int, ...] = Field(min_length=1)
    shell: Literal[False] = False
    stdin_disabled: Literal[True] = True
    environment_policy_id: Literal[
        "pepper-minimal-task-local-autonomy-command-environment-v1"
    ] = GOVERNED_AUTONOMY_ENVIRONMENT_POLICY_ID
    path_permission_decision_SHA256s: tuple[DigestText, ...] = ()
    network_isolation_guaranteed: Literal[False] = False
    process_tree_isolation_guaranteed: Literal[False] = False
    evaluation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evaluation(self) -> AutonomyCommandEvaluation:
        if self.decision is AutonomyCommandDecision.ALLOW:
            if self.denial_reason is not AutonomyCommandDenialReason.NONE:
                raise ValueError("allowed command must not carry a denial reason")
            if not self.effective_argv:
                raise ValueError("allowed command requires effective argv")
        else:
            if self.denial_reason is AutonomyCommandDenialReason.NONE:
                raise ValueError("denied command requires a denial reason")
            if self.effective_argv:
                raise ValueError("denied command must not carry effective argv")
        if self.evaluation_SHA256 != _command_evaluation_digest(self):
            raise ValueError("evaluation_SHA256 must match command evaluation digest")
        return self


class AutonomyCommandCapturedStream(_GovernedAutonomyModel):
    stream: AutonomyCommandStreamKind
    retained_text: str | None
    raw_byte_count: int = Field(ge=0, strict=True)
    retained_byte_count: int = Field(ge=0, strict=True)
    raw_SHA256: DigestText
    truncated: StrictBool
    redaction_count: int = Field(ge=0, strict=True)
    decode_replacement_count: int = Field(ge=0, strict=True)
    stream_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_stream(self) -> AutonomyCommandCapturedStream:
        if self.raw_byte_count == 0:
            if self.retained_text is not None or self.retained_byte_count != 0:
                raise ValueError("empty stream must not retain text")
        elif self.retained_text is None:
            raise ValueError("nonempty stream must retain sanitized text")
        if self.stream_SHA256 != _captured_stream_digest(self):
            raise ValueError("stream_SHA256 must match captured stream digest")
        return self


class AutonomyCommandExecutionResult(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    disposition: AutonomyCommandDisposition
    failure_reason: AutonomyCommandFailureReason
    evaluation_SHA256: DigestText
    proposal_id: BoundedIdentifier
    candidate_id: BoundedIdentifier
    exit_code: int | None = Field(default=None, ge=0, le=255)
    timeout_seconds: int = Field(ge=1, le=120, strict=True)
    process_started: StrictBool
    terminate_requested: StrictBool
    kill_requested: StrictBool
    stdout: AutonomyCommandCapturedStream
    stderr: AutonomyCommandCapturedStream
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> AutonomyCommandExecutionResult:
        if self.disposition is AutonomyCommandDisposition.PASSED:
            if self.failure_reason is not AutonomyCommandFailureReason.NONE:
                raise ValueError("passed command must not carry failure reason")
            if not self.process_started or self.exit_code is None:
                raise ValueError("passed command requires process exit")
        elif self.disposition is AutonomyCommandDisposition.FAILED:
            if self.failure_reason not in {
                AutonomyCommandFailureReason.NONZERO_EXIT,
                AutonomyCommandFailureReason.LAUNCH_ERROR,
            }:
                raise ValueError("failed command reason is invalid")
        elif self.disposition is AutonomyCommandDisposition.TIMED_OUT:
            if (
                self.failure_reason is not AutonomyCommandFailureReason.TIMEOUT
                or not self.process_started
                or not self.terminate_requested
            ):
                raise ValueError("timeout command evidence is invalid")
        elif self.disposition is AutonomyCommandDisposition.OUTPUT_LIMIT_EXCEEDED:
            if (
                self.failure_reason is not AutonomyCommandFailureReason.OUTPUT_LIMIT
                or not self.process_started
                or not self.terminate_requested
            ):
                raise ValueError("output-limit command evidence is invalid")
        if self.result_SHA256 != _command_execution_digest(self):
            raise ValueError("result_SHA256 must match command execution digest")
        return self


class AutonomyContinuationLineage(_GovernedAutonomyModel):
    schema_version: Literal[1] = GOVERNED_AUTONOMY_SCHEMA_VERSION
    lineage_id: BoundedIdentifier
    envelope_SHA256: DigestText
    gap_SHA256: DigestText
    state: AutonomyContinuationState
    continuation_index: int = Field(ge=0, strict=True)
    repair_attempt_count: int = Field(ge=0, strict=True)
    tool_candidate_count: int = Field(ge=0, strict=True)
    command_evaluation_count: int = Field(ge=0, strict=True)
    successful_command_count: int = Field(ge=0, strict=True)
    no_progress_count: int = Field(ge=0, strict=True)
    progress_markers: tuple[BoundedIdentifier, ...] = ()
    budget: GovernedAutonomyBudget
    stop_reason: AutonomyContinuationStopReason = AutonomyContinuationStopReason.NONE
    previous_lineage_SHA256: DigestText | None = None
    lineage_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_lineage(self) -> AutonomyContinuationLineage:
        if self.state in {
            AutonomyContinuationState.READY,
            AutonomyContinuationState.CONTINUING,
            AutonomyContinuationState.COMPLETED,
        }:
            if self.stop_reason is not AutonomyContinuationStopReason.NONE:
                raise ValueError("non-blocked continuation must not carry stop reason")
        elif self.stop_reason is AutonomyContinuationStopReason.NONE:
            raise ValueError("blocked continuation requires stop reason")
        if self.lineage_SHA256 != _continuation_digest(self):
            raise ValueError("lineage_SHA256 must match continuation digest")
        return self


def build_governed_autonomy_reuse_matrix() -> tuple[GovernedAutonomyReuseAssessment, ...]:
    """Return the fixed 01AH reuse/customization/new-surface matrix."""

    records = (
        (
            "workpacket.file_guard",
            GovernedAutonomyReuseDisposition.HERMES_REUSED,
            "Reuses governed WorkPacket path confinement, including dependency-substrate protected paths.",
        ),
        (
            "workpacket.tool_permissions",
            GovernedAutonomyReuseDisposition.HERMES_REUSED,
            "Reuses deny-first filesystem grants and pure permission decisions for every materialized helper path.",
        ),
        (
            "workpacket.workspace_allocation",
            GovernedAutonomyReuseDisposition.HERMES_REUSED,
            "Reuses the existing allocated workspace binding and never allocates a replacement workspace.",
        ),
        (
            "workpacket.single_agent_result",
            GovernedAutonomyReuseDisposition.HERMES_REUSED,
            "Reuses completed single-agent execution evidence as the authority envelope prerequisite.",
        ),
        (
            "validation_command.subprocess_pattern",
            GovernedAutonomyReuseDisposition.HERMES_ADAPTED,
            "Adapts the shell-free bounded subprocess posture for task-local helper commands rather than exact human validation commands.",
        ),
        (
            "hermes.dynamic_tool_surfaces",
            GovernedAutonomyReuseDisposition.HERMES_ADAPTED,
            "Assesses global registry/plugin/skill/MCP/code-execution surfaces but keeps 01AH task-local and non-global.",
        ),
        (
            "pepper.autonomy_envelope",
            GovernedAutonomyReuseDisposition.PEPPER_NEW,
            "Adds Pepper-specific capability-gap, task-local contract, candidate, command, and continuation evidence.",
        ),
    )
    assessments: list[GovernedAutonomyReuseAssessment] = []
    for component, disposition, rationale in records:
        data = {
            "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
            "component": component,
            "disposition": disposition,
            "rationale": rationale,
        }
        assessments.append(
            GovernedAutonomyReuseAssessment(
                **data,
                assessment_SHA256=_digest(
                    REUSE_ASSESSMENT_DIGEST_ALGORITHM,
                    data,
                ),
            )
        )
    return tuple(assessments)


def build_governed_autonomy_envelope(
    *,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    profile_result: ToolPermissionProfileResult,
    single_agent_execution_result: SingleAgentExecutionResult,
    budget: GovernedAutonomyBudget | None = None,
) -> GovernedAutonomyEnvelope:
    """Bind one completed WorkPacket execution to 01AH autonomy authority."""

    try:
        compilation = WorkPacketCompilationResult.model_validate(
            compilation_result.model_dump(mode="json")
        )
        allocation_result = WorkspaceAllocationResult.model_validate(
            allocation_result.model_dump(mode="json")
        )
        profile_result = ToolPermissionProfileResult.model_validate(
            profile_result.model_dump(mode="json")
        )
        single_result = SingleAgentExecutionResult.model_validate(
            single_agent_execution_result.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise GovernedAutonomyInputError("autonomy envelope inputs are invalid") from exc
    except ValueError as exc:
        raise GovernedAutonomyInputError("autonomy envelope inputs are invalid") from exc

    _validate_authority_prerequisites(
        compilation_result=compilation,
        allocation_result=allocation_result,
        profile_result=profile_result,
        single_agent_execution_result=single_result,
    )
    packet = compilation.work_packet
    allocation = allocation_result.allocation
    profile = profile_result.profile
    effective_budget = budget or GovernedAutonomyBudget()
    data = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "policy_id": GOVERNED_AUTONOMY_POLICY_ID,
        "autonomy_enabled": True,
        "capability_authority_boundary": GOVERNED_AUTONOMY_BOUNDARY_CLASSIFICATION,
        "live_lineage_activation_authorized": False,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "source_ticket_SHA256": packet.source_ticket_SHA256,
        "ticket_id": packet.ticket_id,
        "publication_revision": packet.publication_revision,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "profile_id": profile.profile_id,
        "profile_SHA256": profile.profile_SHA256,
        "single_agent_result_SHA256": single_result.result_SHA256,
        "allocation": allocation,
        "profile": profile,
        "workspace_root": allocation.workspace_root,
        "resolved_workspace_root": allocation.resolved_workspace_root,
        "allowed_paths": allocation.scope_projection.allowed_paths,
        "forbidden_paths": allocation.scope_projection.forbidden_paths,
        "denied_operations": profile.denied_operations,
        "git_authority": WorkPacketGitAuthority.HUMAN_ONLY,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "budget": effective_budget,
    }
    return GovernedAutonomyEnvelope(
        **data,
        envelope_SHA256=_digest(ENVELOPE_DIGEST_ALGORITHM, data),
    )


def classify_capability_gap(
    *,
    envelope: GovernedAutonomyEnvelope,
    observed_failure: str,
    requested_capability: str,
    requested_command: str | None = None,
) -> CapabilityGapEvidence:
    """Classify whether a missing capability can be repaired task-locally."""

    validated_envelope = _validated_envelope(envelope)
    command = requested_command.strip() if requested_command else None
    text = " ".join(
        item
        for item in (observed_failure, requested_capability, command or "")
        if item
    )
    kind, disposition, requires_human, rationale = _classify_gap_text(
        text,
        command,
    )
    base = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "envelope_SHA256": validated_envelope.envelope_SHA256,
        "kind": kind,
        "disposition": disposition,
        "observed_failure": observed_failure,
        "requested_capability": requested_capability,
        "requested_command": command,
        "requires_human_authority": requires_human,
        "rationale": rationale,
    }
    gap_input_sha = _digest(GAP_DIGEST_ALGORITHM, base)
    data = {
        **base,
        "gap_id": _stable_id("GAP", validated_envelope.ticket_id, gap_input_sha),
    }
    return CapabilityGapEvidence(
        **data,
        gap_SHA256=_digest(GAP_DIGEST_ALGORITHM, data),
    )


def build_task_local_capability_contract(
    *,
    envelope: GovernedAutonomyEnvelope,
    gap: CapabilityGapEvidence,
    tool_name: str,
    language: TaskLocalToolLanguage,
    implementation_path: str,
    permitted_operations: tuple[ToolPermissionOperation, ...] | None = None,
) -> TaskLocalCapabilityContract:
    """Create a bounded task-local helper contract inside WorkPacket scope."""

    validated_envelope = _validated_envelope(envelope)
    validated_gap = CapabilityGapEvidence.model_validate(gap.model_dump(mode="json"))
    if validated_gap.envelope_SHA256 != validated_envelope.envelope_SHA256:
        raise GovernedAutonomyIntegrityError("gap envelope binding mismatch")
    if validated_gap.disposition is not CapabilityGapDisposition.REPAIRABLE_TASK_LOCAL:
        raise GovernedAutonomyPolicyError("gap is not task-local repairable")

    normalized_path = _validate_repository_relative_path(implementation_path)
    _ensure_write_path_allowed(validated_envelope, normalized_path)
    language = TaskLocalToolLanguage(language)
    _validate_language_path(language, normalized_path)
    operations = permitted_operations or (
        ToolPermissionOperation.LIST_DIRECTORY,
        ToolPermissionOperation.READ_FILE,
        ToolPermissionOperation.CREATE_FILE,
        ToolPermissionOperation.REPLACE_FILE,
        ToolPermissionOperation.CREATE_DIRECTORY,
    )
    base = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "envelope_SHA256": validated_envelope.envelope_SHA256,
        "gap_id": validated_gap.gap_id,
        "gap_SHA256": validated_gap.gap_SHA256,
        "tool_name": tool_name,
        "language": language,
        "implementation_path": normalized_path,
        "allowed_paths": validated_envelope.allowed_paths,
        "forbidden_paths": validated_envelope.forbidden_paths,
        "permitted_operations": operations,
        "allow_package_install": False,
        "allow_network_access": False,
        "allow_git_access": False,
        "allow_provider_or_model_calls": False,
    }
    contract_input_sha = _digest(CONTRACT_DIGEST_ALGORITHM, base)
    data = {
        **base,
        "contract_id": _stable_id("GAC", validated_envelope.ticket_id, contract_input_sha),
    }
    return TaskLocalCapabilityContract(
        **data,
        contract_SHA256=_digest(CONTRACT_DIGEST_ALGORITHM, data),
    )


def build_tool_candidate(
    *,
    contract: TaskLocalCapabilityContract,
    source_text: str,
    entrypoint: str | None = None,
    dependencies: tuple[str, ...] = (),
) -> ToolCandidate:
    """Build one reusable task-local helper candidate for a contract."""

    validated_contract = TaskLocalCapabilityContract.model_validate(
        contract.model_dump(mode="json")
    )
    source = _validate_source_text(source_text).strip()
    if not source:
        raise GovernedAutonomyInputError("tool candidate source must not be empty")
    source_sha = _sha256_text(source)
    dependency_tuple = tuple(str(item).strip() for item in dependencies)
    if any(not item for item in dependency_tuple):
        raise GovernedAutonomyInputError("dependencies must be nonempty identifiers")
    base = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "contract_id": validated_contract.contract_id,
        "contract_SHA256": validated_contract.contract_SHA256,
        "language": validated_contract.language,
        "implementation_path": validated_contract.implementation_path,
        "entrypoint": entrypoint or validated_contract.implementation_path,
        "dependencies": dependency_tuple,
        "source_text": source,
        "source_SHA256": source_sha,
    }
    candidate_input_sha = _digest(CANDIDATE_DIGEST_ALGORITHM, base)
    data = {
        **base,
        "candidate_id": _stable_id("GAT", validated_contract.contract_id, candidate_input_sha),
    }
    return ToolCandidate(
        **data,
        candidate_SHA256=_digest(CANDIDATE_DIGEST_ALGORITHM, data),
    )


def materialize_task_local_tool(
    *,
    envelope: GovernedAutonomyEnvelope,
    contract: TaskLocalCapabilityContract,
    candidate: ToolCandidate,
    replace_existing: bool = False,
) -> TaskLocalToolMaterializationResult:
    """Write a task-local helper file after WorkPacket permission evaluation."""

    validated_envelope = _validated_envelope(envelope)
    validated_contract = TaskLocalCapabilityContract.model_validate(
        contract.model_dump(mode="json")
    )
    validated_candidate = ToolCandidate.model_validate(candidate.model_dump(mode="json"))
    _validate_contract_candidate_binding(validated_contract, validated_candidate)
    _validate_envelope_contract_binding(validated_envelope, validated_contract)

    target = _workspace_path(validated_envelope, validated_candidate.implementation_path)
    parent = target.parent
    root = Path(validated_envelope.resolved_workspace_root)
    directory_decision_sha: str | None = None
    if not parent.exists():
        parent_rel = parent.relative_to(root).as_posix()
        _ensure_write_path_allowed(validated_envelope, parent_rel)
        directory_decision = _evaluate_permission_or_raise(
            validated_envelope,
            ToolPermissionOperation.CREATE_DIRECTORY,
            parent_rel,
        )
        directory_decision_sha = directory_decision.decision_SHA256
        parent.mkdir(parents=True, exist_ok=True)

    exists = target.exists()
    if exists and not replace_existing:
        raise GovernedAutonomyPolicyError("task-local tool already exists")
    operation = (
        ToolPermissionOperation.REPLACE_FILE
        if exists
        else ToolPermissionOperation.CREATE_FILE
    )
    file_decision = _evaluate_permission_or_raise(
        validated_envelope,
        operation,
        validated_candidate.implementation_path,
    )
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(validated_candidate.source_text)
    data = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "state": TaskLocalToolMaterializationState.MATERIALIZED,
        "candidate_id": validated_candidate.candidate_id,
        "candidate_SHA256": validated_candidate.candidate_SHA256,
        "implementation_path": validated_candidate.implementation_path,
        "source_SHA256": validated_candidate.source_SHA256,
        "byte_count": len(validated_candidate.source_text.encode("utf-8")),
        "directory_permission_decision_SHA256": directory_decision_sha,
        "file_permission_decision_SHA256": file_decision.decision_SHA256,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return TaskLocalToolMaterializationResult(
        **data,
        materialization_SHA256=_digest(MATERIALIZATION_DIGEST_ALGORITHM, data),
    )


def propose_autonomy_command(
    *,
    envelope: GovernedAutonomyEnvelope,
    contract: TaskLocalCapabilityContract,
    candidate: ToolCandidate,
    source_command: str,
    timeout_seconds: int = 30,
    expected_exit_codes: tuple[int, ...] = (0,),
) -> AutonomyCommandProposal:
    """Create a bounded command proposal for one task-local helper."""

    validated_envelope = _validated_envelope(envelope)
    validated_contract = TaskLocalCapabilityContract.model_validate(
        contract.model_dump(mode="json")
    )
    validated_candidate = ToolCandidate.model_validate(candidate.model_dump(mode="json"))
    _validate_envelope_contract_binding(validated_envelope, validated_contract)
    _validate_contract_candidate_binding(validated_contract, validated_candidate)
    base = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "contract_id": validated_contract.contract_id,
        "contract_SHA256": validated_contract.contract_SHA256,
        "candidate_id": validated_candidate.candidate_id,
        "candidate_SHA256": validated_candidate.candidate_SHA256,
        "source_command": source_command,
        "working_directory": validated_envelope.resolved_workspace_root,
        "timeout_seconds": timeout_seconds,
        "expected_exit_codes": expected_exit_codes,
        "shell": False,
        "stdin_disabled": True,
    }
    proposal_input_sha = _digest(COMMAND_PROPOSAL_DIGEST_ALGORITHM, base)
    data = {
        **base,
        "proposal_id": _stable_id("GAPCMD", validated_candidate.candidate_id, proposal_input_sha),
    }
    return AutonomyCommandProposal(
        **data,
        proposal_SHA256=_digest(COMMAND_PROPOSAL_DIGEST_ALGORITHM, data),
    )


def evaluate_autonomy_command(
    *,
    envelope: GovernedAutonomyEnvelope,
    contract: TaskLocalCapabilityContract,
    candidate: ToolCandidate,
    proposal: AutonomyCommandProposal,
) -> AutonomyCommandEvaluation:
    """Evaluate a task-local command proposal without executing it."""

    validated_envelope = _validated_envelope(envelope)
    validated_contract = TaskLocalCapabilityContract.model_validate(
        contract.model_dump(mode="json")
    )
    validated_candidate = ToolCandidate.model_validate(candidate.model_dump(mode="json"))
    validated_proposal = AutonomyCommandProposal.model_validate(
        proposal.model_dump(mode="json")
    )
    _validate_envelope_contract_binding(validated_envelope, validated_contract)
    _validate_contract_candidate_binding(validated_contract, validated_candidate)
    _validate_candidate_proposal_binding(validated_candidate, validated_proposal)
    reason, effective_argv, path_decisions = _evaluate_command_policy(
        envelope=validated_envelope,
        candidate=validated_candidate,
        proposal=validated_proposal,
    )
    decision = (
        AutonomyCommandDecision.ALLOW
        if reason is AutonomyCommandDenialReason.NONE
        else AutonomyCommandDecision.DENY
    )
    data = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "decision": decision,
        "denial_reason": reason,
        "proposal_id": validated_proposal.proposal_id,
        "proposal_SHA256": validated_proposal.proposal_SHA256,
        "candidate_id": validated_candidate.candidate_id,
        "candidate_SHA256": validated_candidate.candidate_SHA256,
        "source_command": validated_proposal.source_command,
        "effective_argv": effective_argv if decision is AutonomyCommandDecision.ALLOW else (),
        "working_directory": validated_proposal.working_directory,
        "timeout_seconds": validated_proposal.timeout_seconds,
        "expected_exit_codes": validated_proposal.expected_exit_codes,
        "shell": False,
        "stdin_disabled": True,
        "environment_policy_id": GOVERNED_AUTONOMY_ENVIRONMENT_POLICY_ID,
        "path_permission_decision_SHA256s": tuple(
            item.decision_SHA256 for item in path_decisions
        ),
        "network_isolation_guaranteed": False,
        "process_tree_isolation_guaranteed": False,
    }
    return AutonomyCommandEvaluation(
        **data,
        evaluation_SHA256=_digest(COMMAND_EVALUATION_DIGEST_ALGORITHM, data),
    )


def execute_autonomy_command(
    evaluation: AutonomyCommandEvaluation,
) -> AutonomyCommandExecutionResult:
    """Execute one previously allowed task-local helper command."""

    validated = AutonomyCommandEvaluation.model_validate(evaluation.model_dump(mode="json"))
    if validated.decision is not AutonomyCommandDecision.ALLOW:
        raise GovernedAutonomyPolicyError("cannot execute denied autonomy command")
    launch = _launch_and_capture(validated, _minimal_environment())
    stdout = _captured_stream(
        AutonomyCommandStreamKind.STDOUT,
        launch.stdout_raw,
        RETAINED_STDOUT_BYTES,
        raw_byte_count=launch.stdout_raw_byte_count,
        raw_SHA256=launch.stdout_raw_SHA256,
    )
    stderr = _captured_stream(
        AutonomyCommandStreamKind.STDERR,
        launch.stderr_raw,
        RETAINED_STDERR_BYTES,
        raw_byte_count=launch.stderr_raw_byte_count,
        raw_SHA256=launch.stderr_raw_SHA256,
    )
    disposition, failure_reason = _disposition_for_launch(validated, launch)
    data = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "disposition": disposition,
        "failure_reason": failure_reason,
        "evaluation_SHA256": validated.evaluation_SHA256,
        "proposal_id": validated.proposal_id,
        "candidate_id": validated.candidate_id,
        "exit_code": launch.exit_code,
        "timeout_seconds": validated.timeout_seconds,
        "process_started": launch.process_started,
        "terminate_requested": launch.terminate_requested,
        "kill_requested": launch.kill_requested,
        "stdout": stdout,
        "stderr": stderr,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return AutonomyCommandExecutionResult(
        **data,
        result_SHA256=_digest(COMMAND_EXECUTION_DIGEST_ALGORITHM, data),
    )


def start_governed_autonomy_continuation(
    *,
    envelope: GovernedAutonomyEnvelope,
    gap: CapabilityGapEvidence,
) -> AutonomyContinuationLineage:
    """Start immutable continuation lineage for one repairable gap."""

    validated_envelope = _validated_envelope(envelope)
    validated_gap = CapabilityGapEvidence.model_validate(gap.model_dump(mode="json"))
    if validated_gap.envelope_SHA256 != validated_envelope.envelope_SHA256:
        raise GovernedAutonomyIntegrityError("gap envelope binding mismatch")
    if validated_gap.disposition is not CapabilityGapDisposition.REPAIRABLE_TASK_LOCAL:
        raise GovernedAutonomyPolicyError("only repairable task-local gaps can continue")
    base = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "envelope_SHA256": validated_envelope.envelope_SHA256,
        "gap_SHA256": validated_gap.gap_SHA256,
        "state": AutonomyContinuationState.READY,
        "continuation_index": 0,
        "repair_attempt_count": 0,
        "tool_candidate_count": 0,
        "command_evaluation_count": 0,
        "successful_command_count": 0,
        "no_progress_count": 0,
        "progress_markers": (),
        "budget": validated_envelope.budget,
        "stop_reason": AutonomyContinuationStopReason.NONE,
        "previous_lineage_SHA256": None,
    }
    lineage_input_sha = _digest(CONTINUATION_DIGEST_ALGORITHM, base)
    data = {
        **base,
        "lineage_id": _stable_id("GAL", validated_gap.gap_id, lineage_input_sha),
    }
    return AutonomyContinuationLineage(
        **data,
        lineage_SHA256=_digest(CONTINUATION_DIGEST_ALGORITHM, data),
    )


def advance_governed_autonomy_continuation(
    *,
    envelope: GovernedAutonomyEnvelope,
    lineage: AutonomyContinuationLineage,
    candidate: ToolCandidate | None = None,
    command_evaluation: AutonomyCommandEvaluation | None = None,
    command_result: AutonomyCommandExecutionResult | None = None,
    progress_marker: str | None = None,
) -> AutonomyContinuationLineage:
    """Advance continuation lineage with budget and no-progress enforcement."""

    validated_envelope = _validated_envelope(envelope)
    validated_lineage = AutonomyContinuationLineage.model_validate(
        lineage.model_dump(mode="json")
    )
    if validated_lineage.envelope_SHA256 != validated_envelope.envelope_SHA256:
        raise GovernedAutonomyIntegrityError("lineage envelope binding mismatch")
    if validated_lineage.state in {
        AutonomyContinuationState.COMPLETED,
        AutonomyContinuationState.BLOCKED,
    }:
        raise GovernedAutonomyStateError("terminal continuation cannot advance")

    candidate_count = validated_lineage.tool_candidate_count
    repair_count = validated_lineage.repair_attempt_count
    evaluation_count = validated_lineage.command_evaluation_count
    success_count = validated_lineage.successful_command_count
    if candidate is not None:
        ToolCandidate.model_validate(candidate.model_dump(mode="json"))
        candidate_count += 1
        repair_count += 1
    if command_evaluation is not None:
        AutonomyCommandEvaluation.model_validate(command_evaluation.model_dump(mode="json"))
        evaluation_count += 1
    if command_result is not None:
        result = AutonomyCommandExecutionResult.model_validate(
            command_result.model_dump(mode="json")
        )
        if result.disposition is AutonomyCommandDisposition.PASSED:
            success_count += 1
        else:
            return _next_lineage(
                lineage=validated_lineage,
                state=AutonomyContinuationState.BLOCKED,
                stop_reason=AutonomyContinuationStopReason.COMMAND_FAILED,
                continuation_index=validated_lineage.continuation_index + 1,
                repair_attempt_count=repair_count,
                tool_candidate_count=candidate_count,
                command_evaluation_count=evaluation_count,
                successful_command_count=success_count,
                no_progress_count=validated_lineage.no_progress_count + 1,
                progress_markers=validated_lineage.progress_markers,
            )

    budget = validated_lineage.budget
    budget_exhausted = (
        repair_count > budget.max_repair_attempts
        or candidate_count > budget.max_tool_candidates
        or evaluation_count > budget.max_command_evaluations
        or validated_lineage.continuation_index + 1 > budget.max_continuations
    )
    if budget_exhausted:
        return _next_lineage(
            lineage=validated_lineage,
            state=AutonomyContinuationState.BLOCKED,
            stop_reason=AutonomyContinuationStopReason.BUDGET_EXHAUSTED,
            continuation_index=validated_lineage.continuation_index + 1,
            repair_attempt_count=repair_count,
            tool_candidate_count=candidate_count,
            command_evaluation_count=evaluation_count,
            successful_command_count=success_count,
            no_progress_count=validated_lineage.no_progress_count + 1,
            progress_markers=validated_lineage.progress_markers,
        )

    marker = _normalize_progress_marker(progress_marker)
    markers = validated_lineage.progress_markers
    if marker and marker not in markers:
        markers = (*markers, marker)
        no_progress_count = 0
    else:
        no_progress_count = validated_lineage.no_progress_count + 1
    if no_progress_count >= budget.max_no_progress_iterations:
        state = AutonomyContinuationState.BLOCKED
        stop_reason = AutonomyContinuationStopReason.NO_PROGRESS
    elif command_result is not None and success_count > validated_lineage.successful_command_count:
        state = AutonomyContinuationState.COMPLETED
        stop_reason = AutonomyContinuationStopReason.NONE
    else:
        state = AutonomyContinuationState.CONTINUING
        stop_reason = AutonomyContinuationStopReason.NONE
    return _next_lineage(
        lineage=validated_lineage,
        state=state,
        stop_reason=stop_reason,
        continuation_index=validated_lineage.continuation_index + 1,
        repair_attempt_count=repair_count,
        tool_candidate_count=candidate_count,
        command_evaluation_count=evaluation_count,
        successful_command_count=success_count,
        no_progress_count=no_progress_count,
        progress_markers=markers,
    )


def validate_governed_autonomy_envelope(envelope: GovernedAutonomyEnvelope) -> None:
    """Validate autonomy envelope integrity without repair or side effects."""

    try:
        GovernedAutonomyEnvelope.model_validate(envelope.model_dump(mode="json"))
    except Exception as exc:
        raise GovernedAutonomyIntegrityError("autonomy envelope invalid") from exc


def validate_governed_autonomy_continuation(
    lineage: AutonomyContinuationLineage,
) -> None:
    """Validate continuation lineage integrity without repair or side effects."""

    try:
        AutonomyContinuationLineage.model_validate(lineage.model_dump(mode="json"))
    except Exception as exc:
        raise GovernedAutonomyIntegrityError("autonomy continuation invalid") from exc


class _LaunchResult:
    def __init__(
        self,
        *,
        exit_code: int | None,
        stdout_raw: bytes,
        stderr_raw: bytes,
        stdout_raw_byte_count: int | None = None,
        stderr_raw_byte_count: int | None = None,
        stdout_raw_SHA256: str | None = None,
        stderr_raw_SHA256: str | None = None,
        process_started: bool,
        terminate_requested: bool,
        kill_requested: bool,
        timed_out: bool,
        output_limit_exceeded: bool,
        launch_failed: bool,
    ) -> None:
        self.exit_code = exit_code
        self.stdout_raw = stdout_raw
        self.stderr_raw = stderr_raw
        self.stdout_raw_byte_count = (
            len(stdout_raw) if stdout_raw_byte_count is None else stdout_raw_byte_count
        )
        self.stderr_raw_byte_count = (
            len(stderr_raw) if stderr_raw_byte_count is None else stderr_raw_byte_count
        )
        self.stdout_raw_SHA256 = (
            _sha256_bytes(stdout_raw)
            if stdout_raw_SHA256 is None
            else stdout_raw_SHA256
        )
        self.stderr_raw_SHA256 = (
            _sha256_bytes(stderr_raw)
            if stderr_raw_SHA256 is None
            else stderr_raw_SHA256
        )
        self.process_started = process_started
        self.terminate_requested = terminate_requested
        self.kill_requested = kill_requested
        self.timed_out = timed_out
        self.output_limit_exceeded = output_limit_exceeded
        self.launch_failed = launch_failed


class _StreamCapture:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.raw = bytearray()
        self.raw_byte_count = 0
        self.raw_SHA256 = hashlib.sha256()
        self.exceeded = False


def _launch_and_capture(
    evaluation: AutonomyCommandEvaluation,
    environment: dict[str, str],
) -> _LaunchResult:
    try:
        process = subprocess.Popen(
            tuple(evaluation.effective_argv),
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            bufsize=0,
            cwd=evaluation.working_directory,
            env=environment,
            close_fds=True,
        )
    except Exception:
        return _LaunchResult(
            exit_code=None,
            stdout_raw=b"",
            stderr_raw=b"",
            process_started=False,
            terminate_requested=False,
            kill_requested=False,
            timed_out=False,
            output_limit_exceeded=False,
            launch_failed=True,
        )
    stdout_capture = _StreamCapture(MAX_STDOUT_BYTES)
    stderr_capture = _StreamCapture(MAX_STDERR_BYTES)
    overflow = threading.Event()
    stdout_thread = threading.Thread(
        target=_read_stream,
        args=(process.stdout, stdout_capture, overflow),
    )
    stderr_thread = threading.Thread(
        target=_read_stream,
        args=(process.stderr, stderr_capture, overflow),
    )
    stdout_thread.start()
    stderr_thread.start()
    timed_out = False
    terminate_requested = False
    kill_requested = False
    deadline = time.monotonic() + evaluation.timeout_seconds
    while process.poll() is None:
        if overflow.is_set():
            terminate_requested = True
            _terminate_process(process)
            break
        if time.monotonic() >= deadline:
            timed_out = True
            terminate_requested = True
            _terminate_process(process)
            break
        time.sleep(0.01)
    if terminate_requested and process.poll() is None:
        grace_deadline = time.monotonic() + TERMINATION_GRACE_SECONDS
        while process.poll() is None and time.monotonic() < grace_deadline:
            time.sleep(0.01)
        if process.poll() is None:
            kill_requested = True
            process.kill()
    exit_code = process.wait()
    stdout_thread.join()
    stderr_thread.join()
    return _LaunchResult(
        exit_code=exit_code,
        stdout_raw=bytes(stdout_capture.raw),
        stderr_raw=bytes(stderr_capture.raw),
        stdout_raw_byte_count=stdout_capture.raw_byte_count,
        stderr_raw_byte_count=stderr_capture.raw_byte_count,
        stdout_raw_SHA256=stdout_capture.raw_SHA256.hexdigest(),
        stderr_raw_SHA256=stderr_capture.raw_SHA256.hexdigest(),
        process_started=True,
        terminate_requested=terminate_requested,
        kill_requested=kill_requested,
        timed_out=timed_out,
        output_limit_exceeded=stdout_capture.exceeded or stderr_capture.exceeded,
        launch_failed=False,
    )


def _read_stream(
    stream: object,
    capture: _StreamCapture,
    overflow: threading.Event,
) -> None:
    if stream is None:
        return
    while True:
        chunk = stream.read(OUTPUT_CHUNK_BYTES)  # type: ignore[attr-defined]
        if not chunk:
            return
        capture.raw_byte_count += len(chunk)
        capture.raw_SHA256.update(chunk)
        remaining = capture.limit - len(capture.raw)
        if remaining > 0:
            capture.raw.extend(chunk[:remaining])
        if len(chunk) > remaining:
            capture.exceeded = True
            overflow.set()


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    try:
        process.terminate()
    except Exception as exc:
        raise GovernedAutonomyExecutionError("process termination failed") from exc


def _disposition_for_launch(
    evaluation: AutonomyCommandEvaluation,
    launch: _LaunchResult,
) -> tuple[AutonomyCommandDisposition, AutonomyCommandFailureReason]:
    if launch.launch_failed:
        return (
            AutonomyCommandDisposition.FAILED,
            AutonomyCommandFailureReason.LAUNCH_ERROR,
        )
    if launch.timed_out:
        return (
            AutonomyCommandDisposition.TIMED_OUT,
            AutonomyCommandFailureReason.TIMEOUT,
        )
    if launch.output_limit_exceeded:
        return (
            AutonomyCommandDisposition.OUTPUT_LIMIT_EXCEEDED,
            AutonomyCommandFailureReason.OUTPUT_LIMIT,
        )
    if launch.exit_code in evaluation.expected_exit_codes:
        return (
            AutonomyCommandDisposition.PASSED,
            AutonomyCommandFailureReason.NONE,
        )
    return (
        AutonomyCommandDisposition.FAILED,
        AutonomyCommandFailureReason.NONZERO_EXIT,
    )


def _captured_stream(
    kind: AutonomyCommandStreamKind,
    raw: bytes,
    retained_limit: int,
    *,
    raw_byte_count: int,
    raw_SHA256: str,
) -> AutonomyCommandCapturedStream:
    if raw_byte_count == 0:
        data = {
            "stream": kind,
            "retained_text": None,
            "raw_byte_count": 0,
            "retained_byte_count": 0,
            "raw_SHA256": raw_SHA256,
            "truncated": False,
            "redaction_count": 0,
            "decode_replacement_count": 0,
        }
        return AutonomyCommandCapturedStream(
            **data,
            stream_SHA256=_digest(STREAM_DIGEST_ALGORITHM, data),
        )
    retained_raw = raw[:retained_limit]
    text = retained_raw.decode("utf-8", errors="replace")
    decode_replacements = text.count("\ufffd")
    text = _ANSI_ESCAPE_PATTERN.sub("", text)
    sanitized, redactions = _sanitize_output(text)
    sanitized = sanitized.strip()
    retained_bytes = sanitized.encode("utf-8")
    data = {
        "stream": kind,
        "retained_text": sanitized,
        "raw_byte_count": raw_byte_count,
        "retained_byte_count": len(retained_bytes),
        "raw_SHA256": raw_SHA256,
        "truncated": raw_byte_count > len(retained_raw),
        "redaction_count": redactions,
        "decode_replacement_count": decode_replacements,
    }
    return AutonomyCommandCapturedStream(
        **data,
        stream_SHA256=_digest(STREAM_DIGEST_ALGORITHM, data),
    )


def _sanitize_output(text: str) -> tuple[str, int]:
    redactions = 0
    sanitized = text
    for pattern in _SECRET_PATTERNS:
        sanitized, count = pattern.subn("[REDACTED]", sanitized)
        redactions += count
    return sanitized, redactions


def _validate_authority_prerequisites(
    *,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    profile_result: ToolPermissionProfileResult,
    single_agent_execution_result: SingleAgentExecutionResult,
) -> None:
    try:
        validate_work_packet(compilation_result.work_packet)
        validate_workspace_allocation(allocation_result.allocation)
        validate_tool_permission_profile(profile_result.profile)
        validate_single_agent_execution_result(single_agent_execution_result)
    except Exception as exc:
        raise GovernedAutonomyIntegrityError("autonomy prerequisite invalid") from exc
    packet = compilation_result.work_packet
    allocation = allocation_result.allocation
    profile = profile_result.profile
    single_result = single_agent_execution_result
    if allocation.work_packet_id != packet.work_packet_id:
        raise GovernedAutonomyIntegrityError("allocation WorkPacket binding mismatch")
    if allocation.work_packet_SHA256 != packet.work_packet_SHA256:
        raise GovernedAutonomyIntegrityError("allocation WorkPacket digest mismatch")
    if profile.work_packet_id != packet.work_packet_id:
        raise GovernedAutonomyIntegrityError("profile WorkPacket binding mismatch")
    if profile.work_packet_SHA256 != packet.work_packet_SHA256:
        raise GovernedAutonomyIntegrityError("profile WorkPacket digest mismatch")
    if profile.allocation_id != allocation.allocation_id:
        raise GovernedAutonomyIntegrityError("profile allocation binding mismatch")
    if profile.allocation_SHA256 != allocation.allocation_SHA256:
        raise GovernedAutonomyIntegrityError("profile allocation digest mismatch")
    session = single_result.session
    if session.work_packet_id != packet.work_packet_id:
        raise GovernedAutonomyIntegrityError("single-agent WorkPacket binding mismatch")
    if session.work_packet_SHA256 != packet.work_packet_SHA256:
        raise GovernedAutonomyIntegrityError("single-agent WorkPacket digest mismatch")
    if session.allocation_id != allocation.allocation_id:
        raise GovernedAutonomyIntegrityError("single-agent allocation binding mismatch")
    if session.allocation_SHA256 != allocation.allocation_SHA256:
        raise GovernedAutonomyIntegrityError("single-agent allocation digest mismatch")
    if session.profile_id != profile.profile_id:
        raise GovernedAutonomyIntegrityError("single-agent profile binding mismatch")
    if session.profile_SHA256 != profile.profile_SHA256:
        raise GovernedAutonomyIntegrityError("single-agent profile digest mismatch")
    if single_result.provider_dispatch_count != 0 or single_result.model_inference_count != 0:
        raise GovernedAutonomyPolicyError("autonomy prerequisite must be offline")
    if packet.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise GovernedAutonomyPolicyError("WorkPacket Git authority must remain human-only")
    if allocation.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise GovernedAutonomyPolicyError("workspace Git authority must remain human-only")
    if profile.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise GovernedAutonomyPolicyError("profile Git authority must remain human-only")


def _classify_gap_text(
    text: str,
    command: str | None,
) -> tuple[CapabilityGapKind, CapabilityGapDisposition, bool, str]:
    lowered = text.casefold()
    if _contains_secret_marker(text):
        return (
            CapabilityGapKind.CREDENTIAL_AUTHORITY_REQUIRED,
            CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED,
            True,
            "Credential-shaped capability requests require explicit human authority.",
        )
    if command:
        reason = _pre_parse_command_denial(command)
        if reason in {
            AutonomyCommandDenialReason.GIT_AUTHORITY_REQUIRED,
            AutonomyCommandDenialReason.NETWORK_AUTHORITY_REQUIRED,
            AutonomyCommandDenialReason.PACKAGE_INSTALL_AUTHORITY_REQUIRED,
            AutonomyCommandDenialReason.DOCKER_AUTHORITY_REQUIRED,
            AutonomyCommandDenialReason.GRAPHIFY_AUTHORITY_REQUIRED,
            AutonomyCommandDenialReason.CREDENTIAL_AUTHORITY_REQUIRED,
        }:
            return _gap_from_command_denial(reason)
    if _URL_PATTERN.search(text) or any(
        token in lowered for token in ("network", "http", "download", "fetch")
    ):
        return (
            CapabilityGapKind.NETWORK_AUTHORITY_REQUIRED,
            CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED,
            True,
            "Network access is authority, not task-local capability.",
        )
    if any(marker in lowered for marker in ("pip install", "npm install", "package install")):
        return (
            CapabilityGapKind.PACKAGE_INSTALL_AUTHORITY_REQUIRED,
            CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED,
            True,
            "Package installation is outside the WorkPacket authority envelope.",
        )
    if any(marker in lowered for marker in ("git ", "commit", "push", "checkout")):
        return (
            CapabilityGapKind.GIT_AUTHORITY_REQUIRED,
            CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED,
            True,
            "Git remains human-only for governed WorkPacket execution.",
        )
    if any(
        marker in lowered
        for marker in (
            "missing",
            "not found",
            "no helper",
            "need helper",
            "parser",
            "formatter",
            "assertion helper",
            "task-local",
            "local tool",
        )
    ):
        return (
            CapabilityGapKind.MISSING_TASK_LOCAL_TOOL,
            CapabilityGapDisposition.REPAIRABLE_TASK_LOCAL,
            False,
            "The gap can be repaired with a task-local helper inside existing WorkPacket scope.",
        )
    return (
        CapabilityGapKind.NOT_REPAIRABLE,
        CapabilityGapDisposition.NOT_REPAIRABLE,
        False,
        "The observed gap is not classified as a bounded task-local repair.",
    )


def _gap_from_command_denial(
    reason: AutonomyCommandDenialReason,
) -> tuple[CapabilityGapKind, CapabilityGapDisposition, bool, str]:
    mapping = {
        AutonomyCommandDenialReason.GIT_AUTHORITY_REQUIRED: (
            CapabilityGapKind.GIT_AUTHORITY_REQUIRED,
            "Git remains human-only for governed WorkPacket execution.",
        ),
        AutonomyCommandDenialReason.CREDENTIAL_AUTHORITY_REQUIRED: (
            CapabilityGapKind.CREDENTIAL_AUTHORITY_REQUIRED,
            "Credential material or credential acquisition requires explicit human authority.",
        ),
        AutonomyCommandDenialReason.NETWORK_AUTHORITY_REQUIRED: (
            CapabilityGapKind.NETWORK_AUTHORITY_REQUIRED,
            "Network access is authority, not task-local capability.",
        ),
        AutonomyCommandDenialReason.PACKAGE_INSTALL_AUTHORITY_REQUIRED: (
            CapabilityGapKind.PACKAGE_INSTALL_AUTHORITY_REQUIRED,
            "Package installation is outside the WorkPacket authority envelope.",
        ),
        AutonomyCommandDenialReason.DOCKER_AUTHORITY_REQUIRED: (
            CapabilityGapKind.DOCKER_AUTHORITY_REQUIRED,
            "Docker execution is outside the WorkPacket authority envelope.",
        ),
        AutonomyCommandDenialReason.GRAPHIFY_AUTHORITY_REQUIRED: (
            CapabilityGapKind.GRAPHIFY_AUTHORITY_REQUIRED,
            "Graphify mutation is outside the WorkPacket authority envelope.",
        ),
    }
    kind, rationale = mapping[reason]
    return (
        kind,
        CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED,
        True,
        rationale,
    )


def _evaluate_command_policy(
    *,
    envelope: GovernedAutonomyEnvelope,
    candidate: ToolCandidate,
    proposal: AutonomyCommandProposal,
) -> tuple[
    AutonomyCommandDenialReason,
    tuple[str, ...],
    tuple[ToolPermissionDecisionEvidence, ...],
]:
    pre_reason = _pre_parse_command_denial(proposal.source_command)
    if pre_reason is not AutonomyCommandDenialReason.NONE:
        return pre_reason, (), ()
    try:
        tokens = tuple(shlex.split(proposal.source_command, posix=True))
    except ValueError:
        return AutonomyCommandDenialReason.SHELL_SYNTAX, (), ()
    if not tokens:
        return AutonomyCommandDenialReason.EMPTY_COMMAND, (), ()
    if len(tokens) > MAX_ARGV_TOKENS:
        return AutonomyCommandDenialReason.COMMAND_TOO_LONG, (), ()
    if any(not token for token in tokens):
        return AutonomyCommandDenialReason.SHELL_SYNTAX, (), ()
    for token in tokens:
        if _ENV_ASSIGNMENT_PATTERN.match(token) or token in {"-", "-c"}:
            return AutonomyCommandDenialReason.SHELL_SYNTAX, (), ()
        if _is_absolute_or_traversal_path(token):
            return AutonomyCommandDenialReason.TARGET_SCOPE_DENIED, (), ()
    executable = tokens[0]
    reason, effective = _effective_candidate_argv(candidate, executable, tokens[1:])
    if reason is not AutonomyCommandDenialReason.NONE:
        return reason, (), ()
    path_decisions: list[ToolPermissionDecisionEvidence] = []
    candidate_decision = _evaluate_permission_or_deny(
        envelope,
        ToolPermissionOperation.READ_FILE,
        candidate.implementation_path,
    )
    if candidate_decision.decision is not ToolPermissionDecision.ALLOW:
        return AutonomyCommandDenialReason.TARGET_SCOPE_DENIED, (), (candidate_decision,)
    path_decisions.append(candidate_decision)
    for token in tokens[2:]:
        rel = _command_path_token(token)
        if rel is None:
            continue
        try:
            _validate_repository_relative_path(rel)
        except ValueError:
            return AutonomyCommandDenialReason.TARGET_SCOPE_DENIED, (), tuple(path_decisions)
        if _path_scope_denial(envelope, rel) is not None:
            return AutonomyCommandDenialReason.TARGET_SCOPE_DENIED, (), tuple(path_decisions)
        target = _workspace_path(envelope, rel)
        if not target.exists():
            return AutonomyCommandDenialReason.TARGET_NOT_FOUND, (), tuple(path_decisions)
        operation = (
            ToolPermissionOperation.LIST_DIRECTORY
            if target.is_dir()
            else ToolPermissionOperation.READ_FILE
        )
        decision = _evaluate_permission_or_deny(envelope, operation, rel)
        path_decisions.append(decision)
        if decision.decision is not ToolPermissionDecision.ALLOW:
            return AutonomyCommandDenialReason.TARGET_SCOPE_DENIED, (), tuple(path_decisions)
    return AutonomyCommandDenialReason.NONE, effective, tuple(path_decisions)


def _pre_parse_command_denial(command: str) -> AutonomyCommandDenialReason:
    if not command.strip():
        return AutonomyCommandDenialReason.EMPTY_COMMAND
    if len(command) > MAX_SOURCE_COMMAND_CHARACTERS:
        return AutonomyCommandDenialReason.COMMAND_TOO_LONG
    if "\x00" in command or "\n" in command or "\r" in command:
        return AutonomyCommandDenialReason.SHELL_SYNTAX
    for marker in _FORBIDDEN_SHELL_MARKERS:
        if marker in command:
            return AutonomyCommandDenialReason.SHELL_SYNTAX
    for token in _FORBIDDEN_SHELL_TOKENS:
        if token in command:
            return AutonomyCommandDenialReason.SHELL_SYNTAX
    if "\\" in command:
        return AutonomyCommandDenialReason.TARGET_SCOPE_DENIED
    if _contains_secret_marker(command):
        return AutonomyCommandDenialReason.CREDENTIAL_AUTHORITY_REQUIRED
    if _URL_PATTERN.search(command):
        return AutonomyCommandDenialReason.NETWORK_AUTHORITY_REQUIRED
    try:
        tokens = tuple(shlex.split(command, posix=True))
    except ValueError:
        return AutonomyCommandDenialReason.SHELL_SYNTAX
    lowered = tuple(token.casefold() for token in tokens)
    if not lowered:
        return AutonomyCommandDenialReason.EMPTY_COMMAND
    if set(lowered) & _FORBIDDEN_GIT_TOKENS:
        return AutonomyCommandDenialReason.GIT_AUTHORITY_REQUIRED
    if set(lowered) & _FORBIDDEN_DOCKER_TOKENS:
        return AutonomyCommandDenialReason.DOCKER_AUTHORITY_REQUIRED
    if set(lowered) & _FORBIDDEN_GRAPHIFY_TOKENS:
        return AutonomyCommandDenialReason.GRAPHIFY_AUTHORITY_REQUIRED
    if set(lowered) & _FORBIDDEN_NETWORK_TOKENS:
        return AutonomyCommandDenialReason.NETWORK_AUTHORITY_REQUIRED
    if _is_package_command(lowered):
        return AutonomyCommandDenialReason.PACKAGE_INSTALL_AUTHORITY_REQUIRED
    return AutonomyCommandDenialReason.NONE


def _is_package_command(tokens: tuple[str, ...]) -> bool:
    if not tokens:
        return False
    if tokens[0] in _FORBIDDEN_PACKAGE_TOKENS:
        return True
    if len(tokens) >= 3 and tokens[1] == "-m" and tokens[2] in {"pip", "ensurepip"}:
        return True
    return any(token in _PACKAGE_INSTALL_VERBS for token in tokens[:3]) and bool(
        set(tokens) & _FORBIDDEN_PACKAGE_TOKENS
    )


def _effective_candidate_argv(
    candidate: ToolCandidate,
    executable: str,
    args: tuple[str, ...],
) -> tuple[AutonomyCommandDenialReason, tuple[str, ...]]:
    if not args:
        return AutonomyCommandDenialReason.CANDIDATE_ENTRYPOINT_MISMATCH, ()
    if args[0] != candidate.implementation_path:
        return AutonomyCommandDenialReason.CANDIDATE_ENTRYPOINT_MISMATCH, ()
    if candidate.language is TaskLocalToolLanguage.PYTHON:
        allowed_executables = {
            "python",
            "python3",
            "py",
            Path(sys.executable).name,
            Path(sys.executable).resolve().as_posix(),
        }
        if executable not in allowed_executables:
            return AutonomyCommandDenialReason.UNSUPPORTED_EXECUTABLE, ()
        return (
            AutonomyCommandDenialReason.NONE,
            (Path(sys.executable).resolve().as_posix(), *args),
        )
    if candidate.language is TaskLocalToolLanguage.JAVASCRIPT:
        node = _resolve_node_executable()
        if node is None:
            return AutonomyCommandDenialReason.RUNTIME_UNAVAILABLE, ()
        if executable not in {"node", node.name, node.as_posix()}:
            return AutonomyCommandDenialReason.UNSUPPORTED_EXECUTABLE, ()
        return AutonomyCommandDenialReason.NONE, (node.as_posix(), *args)
    return AutonomyCommandDenialReason.RUNTIME_UNAVAILABLE, ()


def _command_path_token(token: str) -> str | None:
    raw = str(token or "").strip()
    if not raw or raw.startswith("-") or raw == "no:cacheprovider":
        return None
    raw = raw.split("::", 1)[0]
    if _URL_PATTERN.search(raw):
        return raw
    if "/" not in raw and not raw.endswith(
        (
            ".py",
            ".ts",
            ".tsx",
            ".js",
            ".jsx",
            ".mjs",
            ".cjs",
            ".json",
            ".txt",
            ".md",
            ".yaml",
            ".yml",
        )
    ):
        return None
    return raw


def _evaluate_permission_or_raise(
    envelope: GovernedAutonomyEnvelope,
    operation: ToolPermissionOperation,
    relative_path: str,
) -> ToolPermissionDecisionEvidence:
    decision = _evaluate_permission_or_deny(envelope, operation, relative_path)
    if decision.decision is not ToolPermissionDecision.ALLOW:
        raise GovernedAutonomyPolicyError(
            f"task-local path denied: {decision.reason.value}"
        )
    return decision


def _evaluate_permission_or_deny(
    envelope: GovernedAutonomyEnvelope,
    operation: ToolPermissionOperation,
    relative_path: str,
) -> ToolPermissionDecisionEvidence:
    if _path_scope_denial(envelope, relative_path) is not None:
        raise GovernedAutonomyPolicyError("task-local path violates protected scope")
    root = Path(envelope.resolved_workspace_root)
    resolved_target = root.joinpath(*relative_path.split("/")).resolve(strict=False)
    return evaluate_tool_permission(
        ToolPermissionCheckRequest(
            profile=envelope.profile,
            allocation=envelope.allocation,
            operation=operation,
            workspace_relative_path=relative_path,
            resolved_target_path=resolved_target.as_posix(),
            target_resolution_verified=True,
            request_reference=f"01AH-{operation.value}",
        )
    )


def _ensure_write_path_allowed(envelope: GovernedAutonomyEnvelope, relative_path: str) -> None:
    authority = file_guard.WorkPacketFileAuthority(
        ticket_id=envelope.ticket_id,
        work_packet_id=envelope.work_packet_id,
        work_packet_SHA256=envelope.work_packet_SHA256,
        ticket_spec_SHA256=envelope.source_ticket_SHA256,
        projection_SHA256=envelope.profile_SHA256,
        allowed_paths=envelope.allowed_paths,
        forbidden_paths=envelope.forbidden_paths,
        workspace_root=Path(envelope.workspace_root),
        resolved_workspace_root=Path(envelope.resolved_workspace_root),
    )
    denial = file_guard.evaluate_write_target(authority, relative_path)
    if denial is not None:
        raise GovernedAutonomyPolicyError(denial.format())


def _path_scope_denial(envelope: GovernedAutonomyEnvelope, relative_path: str) -> str | None:
    try:
        rel = _validate_repository_relative_path(relative_path)
    except ValueError:
        return "invalid_path"
    parts = tuple(part.casefold() for part in rel.split("/") if part)
    if any(part in _PROTECTED_COMPONENTS for part in parts):
        return "node_modules/**"
    if parts and parts[-1] in _PROTECTED_FILENAMES:
        return parts[-1]
    protected = _first_matching_pattern(rel, _PROTECTED_PATHS)
    if protected is not None:
        return protected
    forbidden = _first_matching_pattern(rel, envelope.forbidden_paths)
    if forbidden is not None:
        return forbidden
    allowed = _first_matching_pattern(rel, envelope.allowed_paths)
    if allowed is None:
        return "not_allowed"
    return None


def _workspace_path(envelope: GovernedAutonomyEnvelope, relative_path: str) -> Path:
    rel = _validate_repository_relative_path(relative_path)
    root = Path(envelope.resolved_workspace_root).resolve(strict=True)
    target = root.joinpath(*rel.split("/"))
    resolved_parent = target.parent.resolve(strict=False)
    if not _path_is_under(resolved_parent, root):
        raise GovernedAutonomyPolicyError("target parent escapes workspace")
    return target


def _path_is_under(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


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


def _is_absolute_or_traversal_path(token: str) -> bool:
    if token.startswith("/") or _DRIVE_PATH_PATTERN.match(token):
        return True
    return any(component in {"..", "."} for component in token.split("/"))


def _validate_language_path(language: TaskLocalToolLanguage, path: str) -> None:
    if language is TaskLocalToolLanguage.PYTHON and not path.endswith(".py"):
        raise ValueError("python task-local tools must use .py files")
    if language is TaskLocalToolLanguage.JAVASCRIPT and not path.endswith(
        (".js", ".mjs", ".cjs")
    ):
        raise ValueError("javascript task-local tools must use JS files")
    if language is TaskLocalToolLanguage.TYPESCRIPT and not path.endswith(
        (".ts", ".tsx")
    ):
        raise ValueError("typescript task-local tools must use TS files")


def _resolve_node_executable() -> Path | None:
    raw = shutil.which("node")
    if not raw:
        return None
    try:
        resolved = Path(raw).resolve(strict=True)
    except OSError:
        return None
    return resolved if resolved.is_file() else None


def _contains_secret_marker(value: str) -> bool:
    lowered = value.casefold()
    if any(marker in lowered for marker in _SECRET_COMMAND_MARKERS):
        return True
    return any(pattern.search(value) for pattern in _SECRET_PATTERNS)


def _minimal_environment() -> dict[str, str]:
    data: dict[str, str] = {}
    for key, value in _FIXED_ENVIRONMENT:
        data[key] = value
    for key in _INHERITED_ENVIRONMENT_ALLOWLIST:
        if key in os.environ:
            data[key] = os.environ[key]
    return {key: data[key] for key in sorted(data)}


def _next_lineage(
    *,
    lineage: AutonomyContinuationLineage,
    state: AutonomyContinuationState,
    stop_reason: AutonomyContinuationStopReason,
    continuation_index: int,
    repair_attempt_count: int,
    tool_candidate_count: int,
    command_evaluation_count: int,
    successful_command_count: int,
    no_progress_count: int,
    progress_markers: tuple[str, ...],
) -> AutonomyContinuationLineage:
    data = {
        "schema_version": GOVERNED_AUTONOMY_SCHEMA_VERSION,
        "lineage_id": lineage.lineage_id,
        "envelope_SHA256": lineage.envelope_SHA256,
        "gap_SHA256": lineage.gap_SHA256,
        "state": state,
        "continuation_index": continuation_index,
        "repair_attempt_count": repair_attempt_count,
        "tool_candidate_count": tool_candidate_count,
        "command_evaluation_count": command_evaluation_count,
        "successful_command_count": successful_command_count,
        "no_progress_count": no_progress_count,
        "progress_markers": progress_markers,
        "budget": lineage.budget,
        "stop_reason": stop_reason,
        "previous_lineage_SHA256": lineage.lineage_SHA256,
    }
    return AutonomyContinuationLineage(
        **data,
        lineage_SHA256=_digest(CONTINUATION_DIGEST_ALGORITHM, data),
    )


def _normalize_progress_marker(value: str | None) -> str | None:
    if value is None:
        return None
    marker = value.strip()
    if not marker:
        return None
    marker = re.sub(r"[^A-Za-z0-9._:@+-]", "-", marker)[:128].strip("-")
    if marker and not marker[0].isalnum():
        marker = f"P{marker}"[:128]
    return marker or None


def _validated_envelope(envelope: GovernedAutonomyEnvelope) -> GovernedAutonomyEnvelope:
    try:
        return GovernedAutonomyEnvelope.model_validate(
            envelope.model_dump(mode="json")
        )
    except Exception as exc:
        raise GovernedAutonomyIntegrityError("autonomy envelope invalid") from exc


def _validate_envelope_contract_binding(
    envelope: GovernedAutonomyEnvelope,
    contract: TaskLocalCapabilityContract,
) -> None:
    if contract.envelope_SHA256 != envelope.envelope_SHA256:
        raise GovernedAutonomyIntegrityError("contract envelope binding mismatch")
    if contract.allowed_paths != envelope.allowed_paths:
        raise GovernedAutonomyIntegrityError("contract allowed path scope mismatch")
    if contract.forbidden_paths != envelope.forbidden_paths:
        raise GovernedAutonomyIntegrityError("contract forbidden path scope mismatch")


def _validate_contract_candidate_binding(
    contract: TaskLocalCapabilityContract,
    candidate: ToolCandidate,
) -> None:
    if candidate.contract_id != contract.contract_id:
        raise GovernedAutonomyIntegrityError("candidate contract binding mismatch")
    if candidate.contract_SHA256 != contract.contract_SHA256:
        raise GovernedAutonomyIntegrityError("candidate contract digest mismatch")
    if candidate.language is not contract.language:
        raise GovernedAutonomyIntegrityError("candidate language mismatch")
    if candidate.implementation_path != contract.implementation_path:
        raise GovernedAutonomyIntegrityError("candidate implementation path mismatch")


def _validate_candidate_proposal_binding(
    candidate: ToolCandidate,
    proposal: AutonomyCommandProposal,
) -> None:
    if proposal.candidate_id != candidate.candidate_id:
        raise GovernedAutonomyIntegrityError("proposal candidate binding mismatch")
    if proposal.candidate_SHA256 != candidate.candidate_SHA256:
        raise GovernedAutonomyIntegrityError("proposal candidate digest mismatch")


def _stable_id(prefix: str, scope: str, digest_text: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", scope).strip("-").upper()
    token = token or "SCOPE"
    token_max = max(1, 128 - len(prefix) - 1 - 1 - 12)
    token = token[:token_max].strip("-") or "SCOPE"
    return f"{prefix}-{token}-{digest_text[:12]}"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _to_jsonable(value):
    if isinstance(value, BaseModel):
        return _to_jsonable(value.model_dump(mode="python"))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def _digest(algorithm: str, record: dict[str, object]) -> str:
    payload = {
        "algorithm": algorithm,
        "record": _to_jsonable(record),
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return _sha256_bytes(encoded)


def _model_digest(model: BaseModel, algorithm: str, digest_field: str) -> str:
    return _digest(
        algorithm,
        model.model_dump(mode="python", exclude={digest_field}),
    )


def _envelope_digest(model: GovernedAutonomyEnvelope) -> str:
    return _model_digest(model, ENVELOPE_DIGEST_ALGORITHM, "envelope_SHA256")


def _reuse_assessment_digest(model: GovernedAutonomyReuseAssessment) -> str:
    return _model_digest(
        model,
        REUSE_ASSESSMENT_DIGEST_ALGORITHM,
        "assessment_SHA256",
    )


def _gap_digest(model: CapabilityGapEvidence) -> str:
    return _model_digest(model, GAP_DIGEST_ALGORITHM, "gap_SHA256")


def _contract_digest(model: TaskLocalCapabilityContract) -> str:
    return _model_digest(model, CONTRACT_DIGEST_ALGORITHM, "contract_SHA256")


def _candidate_digest(model: ToolCandidate) -> str:
    return _model_digest(model, CANDIDATE_DIGEST_ALGORITHM, "candidate_SHA256")


def _materialization_digest(model: TaskLocalToolMaterializationResult) -> str:
    return _model_digest(
        model,
        MATERIALIZATION_DIGEST_ALGORITHM,
        "materialization_SHA256",
    )


def _command_proposal_digest(model: AutonomyCommandProposal) -> str:
    return _model_digest(model, COMMAND_PROPOSAL_DIGEST_ALGORITHM, "proposal_SHA256")


def _command_evaluation_digest(model: AutonomyCommandEvaluation) -> str:
    return _model_digest(
        model,
        COMMAND_EVALUATION_DIGEST_ALGORITHM,
        "evaluation_SHA256",
    )


def _captured_stream_digest(model: AutonomyCommandCapturedStream) -> str:
    return _model_digest(model, STREAM_DIGEST_ALGORITHM, "stream_SHA256")


def _command_execution_digest(model: AutonomyCommandExecutionResult) -> str:
    return _model_digest(model, COMMAND_EXECUTION_DIGEST_ALGORITHM, "result_SHA256")


def _continuation_digest(model: AutonomyContinuationLineage) -> str:
    return _model_digest(model, CONTINUATION_DIGEST_ALGORITHM, "lineage_SHA256")


__all__ = (
    "GOVERNED_AUTONOMY_SCHEMA_VERSION",
    "GOVERNED_AUTONOMY_POLICY_ID",
    "GOVERNED_AUTONOMY_BOUNDARY_CLASSIFICATION",
    "GovernedAutonomyReuseDisposition",
    "CapabilityGapKind",
    "CapabilityGapDisposition",
    "TaskLocalToolLanguage",
    "TaskLocalToolMaterializationState",
    "AutonomyCommandDecision",
    "AutonomyCommandDenialReason",
    "AutonomyCommandDisposition",
    "AutonomyCommandFailureReason",
    "AutonomyCommandStreamKind",
    "AutonomyContinuationState",
    "AutonomyContinuationStopReason",
    "GovernedAutonomyBudget",
    "GovernedAutonomyReuseAssessment",
    "GovernedAutonomyEnvelope",
    "CapabilityGapEvidence",
    "TaskLocalCapabilityContract",
    "ToolCandidate",
    "TaskLocalToolMaterializationResult",
    "AutonomyCommandProposal",
    "AutonomyCommandEvaluation",
    "AutonomyCommandCapturedStream",
    "AutonomyCommandExecutionResult",
    "AutonomyContinuationLineage",
    "GovernedAutonomyError",
    "GovernedAutonomyInputError",
    "GovernedAutonomyIntegrityError",
    "GovernedAutonomyPolicyError",
    "GovernedAutonomyExecutionError",
    "GovernedAutonomyStateError",
    "build_governed_autonomy_reuse_matrix",
    "build_governed_autonomy_envelope",
    "classify_capability_gap",
    "build_task_local_capability_contract",
    "build_tool_candidate",
    "materialize_task_local_tool",
    "propose_autonomy_command",
    "evaluate_autonomy_command",
    "execute_autonomy_command",
    "start_governed_autonomy_continuation",
    "advance_governed_autonomy_continuation",
    "validate_governed_autonomy_envelope",
    "validate_governed_autonomy_continuation",
)
