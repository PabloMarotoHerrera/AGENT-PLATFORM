"""Externally driven single-agent WorkPacket filesystem execution.

P17.3 binds one explicit action plan to one WorkPacket, one human-provisioned
workspace allocation and one deny-first tool permission profile. The controller
does not plan, prompt, call providers, run commands or mutate Git. It executes
one scoped filesystem operation at a time after physical target resolution and
P17.2 permission evaluation.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
from pathlib import Path
import re
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
    WorkPacket,
    WorkPacketCompilationResult,
    WorkPacketDownstreamCapability,
    WorkPacketGitAuthority,
    validate_work_packet,
)
from hermes_cli.agent_platform.work_packet.tool_permissions import (
    ToolPermissionCheckRequest,
    ToolPermissionDecision,
    ToolPermissionDecisionEvidence,
    ToolPermissionOperation,
    ToolPermissionProfile,
    ToolPermissionProfileResult,
    evaluate_tool_permission,
    validate_tool_permission_decision,
    validate_tool_permission_profile,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocation,
    WorkspaceAllocationResult,
    inspect_human_provisioned_workspace,
    validate_workspace_allocation,
)

SINGLE_AGENT_EXECUTION_SCHEMA_VERSION = 1
SINGLE_AGENT_EXECUTION_POLICY_ID = (
    "pepper-externally-driven-single-agent-filesystem-execution-v1"
)

OPENAI_CODEX_PROVIDER = "openai-codex"
OPENAI_CODEX_MODEL_ID = "gpt-5.5"
OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID = (
    "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
)
OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID = (
    "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)

EXTERNALLY_SUPPLIED_PLAN_SOURCE = "externally_supplied_single_agent_plan"
MAX_ACTIONS = 64
MAX_TEXT_BYTES = 262144
MAX_DIRECTORY_ENTRIES = 512

RUNTIME_BINDING_DIGEST_ALGORITHM = (
    "agent-platform-single-agent-runtime-binding-sha256-v1"
)
ACTION_DIGEST_ALGORITHM = "agent-platform-single-agent-tool-action-sha256-v1"
PLAN_DIGEST_ALGORITHM = "agent-platform-single-agent-execution-plan-sha256-v1"
AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-single-agent-execution-authorization-sha256-v1"
)
TARGET_RESOLUTION_DIGEST_ALGORITHM = (
    "agent-platform-single-agent-target-resolution-sha256-v1"
)
OBSERVATION_DIGEST_ALGORITHM = "agent-platform-single-agent-tool-observation-sha256-v1"
ACTION_EVIDENCE_DIGEST_ALGORITHM = (
    "agent-platform-single-agent-action-evidence-sha256-v1"
)
SESSION_DIGEST_ALGORITHM = "agent-platform-single-agent-execution-session-sha256-v1"
ACTION_RESULT_DIGEST_ALGORITHM = "agent-platform-single-agent-action-result-sha256-v1"
EXECUTION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-single-agent-execution-result-sha256-v1"
)

_CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
_DRIVE_RELATIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$"
_ACTION_ID_PATTERN = r"^ACTION-[0-9]{3}$"
_SESSION_ID_PATTERN = r"^SAE-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"
_BINDING_ID_PATTERN = r"^SAB-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"

_GRANTABLE_OPERATIONS = (
    ToolPermissionOperation.LIST_DIRECTORY,
    ToolPermissionOperation.READ_FILE,
    ToolPermissionOperation.CREATE_FILE,
    ToolPermissionOperation.REPLACE_FILE,
    ToolPermissionOperation.DELETE_FILE,
    ToolPermissionOperation.CREATE_DIRECTORY,
    ToolPermissionOperation.DELETE_DIRECTORY,
)
_MUTATING_OPERATIONS = (
    ToolPermissionOperation.CREATE_FILE,
    ToolPermissionOperation.REPLACE_FILE,
    ToolPermissionOperation.DELETE_FILE,
    ToolPermissionOperation.CREATE_DIRECTORY,
    ToolPermissionOperation.DELETE_DIRECTORY,
)
_PROTECTED_PATHS = (
    ".git",
    ".git/**",
    ".opencode",
    ".opencode/**",
    ".agents",
    ".agents/**",
    "AGENTS.md",
    "graphify-out",
    "graphify-out/**",
    "4_external/sources",
    "4_external/sources/**",
    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
)


class SingleAgentExecutionError(ValueError):
    """Base error for P17.3 single-agent execution failures."""


class SingleAgentExecutionInputError(SingleAgentExecutionError):
    """Raised when execution inputs or bindings are structurally invalid."""


class SingleAgentExecutionAuthorizationError(SingleAgentExecutionError):
    """Raised when explicit human execution authorization is invalid."""


class SingleAgentExecutionIntegrityError(SingleAgentExecutionError):
    """Raised when deterministic execution evidence is invalid."""


class SingleAgentTargetResolutionError(SingleAgentExecutionError):
    """Raised when a target cannot be resolved safely under the workspace."""


class SingleAgentToolExecutionError(SingleAgentExecutionError):
    """Raised when a bounded filesystem adapter action fails."""


class SingleAgentExecutionStateError(SingleAgentExecutionError):
    """Raised when a session transition is not allowed."""


class SingleAgentExecutionState(str, Enum):
    PREPARED = "prepared"
    ACTIVE = "active"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class SingleAgentActionDisposition(str, Enum):
    EXECUTED = "executed"
    DENIED = "denied"
    CANCELLED = "cancelled"


class SingleAgentToolObservationKind(str, Enum):
    NONE = "none"
    TEXT = "text"
    DIRECTORY_ENTRIES = "directory_entries"


class SingleAgentTargetKind(str, Enum):
    ABSENT = "absent"
    FILE = "file"
    DIRECTORY = "directory"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


def _validate_identifier(value: str) -> str:
    if _is_shadow_identifier(value):
        raise ValueError("shadow identifier is not authorized")
    lowered = value.casefold()
    for marker in ("token", "secret", "password", "credential", "bearer"):
        if marker in lowered:
            raise ValueError("identifier must not contain credential markers")
    return value


def _validate_repository_relative_path(value: str) -> str:
    if not value or "\x00" in value or "\\" in value:
        raise ValueError("target path must be repository-relative")
    if value.startswith("/") or _DRIVE_RELATIVE_PATTERN.match(value):
        raise ValueError("target path must not be absolute")
    if _CONTROL_CHARACTER_PATTERN.search(value):
        raise ValueError("target path must not contain control characters")
    if any(component in {"", ".", ".."} for component in value.split("/")):
        raise ValueError("target path must not contain traversal components")
    if _path_matches_any(value, _PROTECTED_PATHS):
        raise ValueError("target path must not target protected roots")
    return value


def _validate_content_size(value: str) -> str:
    if len(value.encode("utf-8")) > MAX_TEXT_BYTES:
        raise ValueError("content exceeds maximum UTF-8 byte length")
    return value


def _validate_grantable_operation(
    operation: ToolPermissionOperation,
) -> ToolPermissionOperation:
    if operation not in _GRANTABLE_OPERATIONS:
        raise ValueError("operation is not a P17.3 filesystem operation")
    return operation


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
BoundedIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=3, max_length=96, pattern=_IDENTIFIER_PATTERN),
    AfterValidator(_validate_identifier),
]
ActionIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=10, max_length=10, pattern=_ACTION_ID_PATTERN),
]
RuntimeBindingIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=28, max_length=96, pattern=_BINDING_ID_PATTERN),
]
ExecutionSessionIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=28, max_length=96, pattern=_SESSION_ID_PATTERN),
]
RepositoryRelativePath: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_repository_relative_path),
]
BoundedContent: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=0, max_length=262144),
    AfterValidator(_reject_nul),
    AfterValidator(_validate_content_size),
]
AbsolutePathText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=1024),
    AfterValidator(_reject_nul),
]


class _SingleAgentExecutionModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class SingleAgentRuntimeBinding(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    binding_id: RuntimeBindingIdentifier
    agent_id: BoundedIdentifier
    worker_id: BoundedIdentifier
    provider: Literal["openai-codex"] = OPENAI_CODEX_PROVIDER
    model_id: Literal["gpt-5.5"] = OPENAI_CODEX_MODEL_ID
    provider_runtime_profile_id: Literal[
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    ] = OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID
    worker_profile_id: Literal[
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    ] = OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID
    externally_driven: Literal[True] = True
    maximum_concurrent_agents: Literal[1] = 1
    maximum_concurrent_workers: Literal[1] = 1
    provider_dispatch_authorized: Literal[False] = False
    model_inference_authorized: Literal[False] = False
    binding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_binding(self) -> SingleAgentRuntimeBinding:
        if self.agent_id == self.worker_id:
            raise ValueError("agent and worker identifiers must be distinct")
        if self.binding_id != _runtime_binding_id_from_binding(self):
            raise ValueError("binding_id must match runtime binding digest")
        if self.binding_SHA256 != _runtime_binding_digest(self):
            raise ValueError("binding_SHA256 must match runtime binding digest")
        return self


class SingleAgentExecutionAuthorization(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    execution_authorized: Literal[True] = True
    synthetic: Literal[False] = False
    authorizer_id: BoundedIdentifier
    authorization_reference: BoundedText
    rationale: BoundedText
    risk_acknowledgement: BoundedText | None = None
    work_packet_id: str
    work_packet_SHA256: DigestText
    allocation_id: str
    allocation_SHA256: DigestText
    profile_id: str
    profile_SHA256: DigestText
    runtime_binding_SHA256: DigestText
    plan_SHA256: DigestText
    authorization_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_authorization(self) -> SingleAgentExecutionAuthorization:
        if self.authorization_SHA256 != _execution_authorization_digest(self):
            raise ValueError("authorization_SHA256 must match authorization digest")
        return self


class SingleAgentToolAction(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    action_id: ActionIdentifier
    task_step_id: str
    operation: ToolPermissionOperation
    workspace_relative_path: RepositoryRelativePath
    content: BoundedContent | None = None
    expected_preexisting_SHA256: DigestText | None = None
    rationale: BoundedText
    action_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_action(self) -> SingleAgentToolAction:
        _validate_grantable_operation(self.operation)
        if self.operation in {
            ToolPermissionOperation.LIST_DIRECTORY,
            ToolPermissionOperation.READ_FILE,
            ToolPermissionOperation.DELETE_FILE,
            ToolPermissionOperation.CREATE_DIRECTORY,
            ToolPermissionOperation.DELETE_DIRECTORY,
        }:
            if self.content is not None:
                raise ValueError("operation must not include content")
        if self.operation in {
            ToolPermissionOperation.CREATE_FILE,
            ToolPermissionOperation.REPLACE_FILE,
        }:
            if self.content is None:
                raise ValueError("operation requires content")
        if self.operation in {
            ToolPermissionOperation.REPLACE_FILE,
            ToolPermissionOperation.DELETE_FILE,
        }:
            if self.expected_preexisting_SHA256 is None:
                raise ValueError("operation requires expected preexisting digest")
        if self.operation in {
            ToolPermissionOperation.LIST_DIRECTORY,
            ToolPermissionOperation.CREATE_FILE,
            ToolPermissionOperation.CREATE_DIRECTORY,
            ToolPermissionOperation.DELETE_DIRECTORY,
        }:
            if self.expected_preexisting_SHA256 is not None:
                raise ValueError(
                    "operation must not include expected preexisting digest"
                )
        if self.action_SHA256 != _action_digest(self):
            raise ValueError("action_SHA256 must match action digest")
        return self


class SingleAgentExecutionPlan(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    action_source: Literal["externally_supplied_single_agent_plan"] = (
        EXTERNALLY_SUPPLIED_PLAN_SOURCE
    )
    actions: tuple[SingleAgentToolAction, ...] = Field(min_length=1, max_length=64)
    plan_SHA256: DigestText

    @field_validator("actions", mode="after")
    @classmethod
    def _validate_actions(
        cls, value: tuple[SingleAgentToolAction, ...]
    ) -> tuple[SingleAgentToolAction, ...]:
        expected_ids = tuple(
            f"ACTION-{index:03d}" for index in range(1, len(value) + 1)
        )
        action_ids = tuple(action.action_id for action in value)
        if action_ids != expected_ids:
            raise ValueError("action IDs must be contiguous from ACTION-001")
        if len(action_ids) != len(frozenset(action_ids)):
            raise ValueError("action IDs must be unique")
        return value

    @model_validator(mode="after")
    def _validate_plan(self) -> SingleAgentExecutionPlan:
        if self.plan_SHA256 != _plan_digest(self):
            raise ValueError("plan_SHA256 must match plan digest")
        return self


class SingleAgentExecutionRequest(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-externally-driven-single-agent-filesystem-execution-v1"
    ] = SINGLE_AGENT_EXECUTION_POLICY_ID
    compilation_result: WorkPacketCompilationResult
    allocation_result: WorkspaceAllocationResult
    profile_result: ToolPermissionProfileResult
    runtime_binding: SingleAgentRuntimeBinding
    plan: SingleAgentExecutionPlan
    execution_authorization: SingleAgentExecutionAuthorization
    require_initial_clean_workspace: StrictBool = True

    @model_validator(mode="after")
    def _validate_request(self) -> SingleAgentExecutionRequest:
        _validate_execution_request_bindings(self, error_type=ValueError)
        return self


class SingleAgentTargetResolutionEvidence(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    action_id: ActionIdentifier
    workspace_relative_path: RepositoryRelativePath
    candidate_target_path: AbsolutePathText
    resolved_target_path: AbsolutePathText
    target_kind_before: SingleAgentTargetKind
    target_exists_before: StrictBool
    parent_exists: StrictBool
    under_workspace: Literal[True] = True
    symlink_safe: Literal[True] = True
    preexisting_SHA256: DigestText | None = None
    resolution_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_resolution(self) -> SingleAgentTargetResolutionEvidence:
        if self.resolution_SHA256 != _target_resolution_digest(self):
            raise ValueError("resolution_SHA256 must match target resolution digest")
        return self


class SingleAgentToolObservation(_SingleAgentExecutionModel):
    kind: SingleAgentToolObservationKind
    text: BoundedContent | None = None
    directory_entries: tuple[BoundedText, ...] = ()
    byte_count: int = Field(ge=0, le=MAX_TEXT_BYTES, strict=True)
    content_SHA256: DigestText | None = None
    observation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_observation(self) -> SingleAgentToolObservation:
        if self.kind is SingleAgentToolObservationKind.NONE:
            if self.text is not None or self.directory_entries or self.byte_count != 0:
                raise ValueError("none observation must not carry tool output")
            if self.content_SHA256 is not None:
                raise ValueError("none observation must not carry content digest")
        elif self.kind is SingleAgentToolObservationKind.TEXT:
            if self.text is None or self.directory_entries:
                raise ValueError("text observation requires only text")
            data = self.text.encode("utf-8")
            if self.byte_count != len(data):
                raise ValueError("byte_count must match UTF-8 text bytes")
            if self.content_SHA256 != _sha256_bytes(data):
                raise ValueError("content_SHA256 must match text")
        else:
            if self.text is not None or not self.directory_entries:
                raise ValueError("directory observation requires entries only")
            if self.byte_count != 0 or self.content_SHA256 is not None:
                raise ValueError("directory observation must not carry content digest")
            if tuple(sorted(self.directory_entries)) != self.directory_entries:
                raise ValueError("directory entries must be sorted")
        if self.observation_SHA256 != _observation_digest(self):
            raise ValueError("observation_SHA256 must match observation digest")
        return self


class SingleAgentActionEvidence(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    action_id: ActionIdentifier
    task_step_id: str
    operation: ToolPermissionOperation
    disposition: SingleAgentActionDisposition
    permission_decision: ToolPermissionDecision | None
    target_resolution: SingleAgentTargetResolutionEvidence | None
    target_kind_after: SingleAgentTargetKind | None
    target_exists_after: StrictBool
    postexisting_SHA256: DigestText | None = None
    tool_executed: StrictBool
    filesystem_mutated: StrictBool
    rollback_performed: StrictBool
    observation_SHA256: DigestText | None = None
    evidence_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evidence(self) -> SingleAgentActionEvidence:
        if self.disposition is SingleAgentActionDisposition.EXECUTED:
            if self.permission_decision is not ToolPermissionDecision.ALLOW:
                raise ValueError("executed action requires allow decision")
            if self.target_resolution is None or not self.tool_executed:
                raise ValueError("executed action requires target and tool execution")
        elif self.disposition is SingleAgentActionDisposition.DENIED:
            if self.permission_decision is not ToolPermissionDecision.DENY:
                raise ValueError("denied action requires deny decision")
            if self.tool_executed or self.filesystem_mutated:
                raise ValueError("denied action must not execute or mutate")
        else:
            if (
                self.permission_decision is not None
                or self.target_resolution is not None
            ):
                raise ValueError("cancelled action must not resolve or evaluate")
            if self.tool_executed or self.filesystem_mutated:
                raise ValueError("cancelled action must not execute or mutate")
        if self.evidence_SHA256 != _action_evidence_digest(self):
            raise ValueError("evidence_SHA256 must match action evidence digest")
        return self


class SingleAgentExecutionSession(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    session_id: ExecutionSessionIdentifier
    policy_id: Literal[
        "pepper-externally-driven-single-agent-filesystem-execution-v1"
    ] = SINGLE_AGENT_EXECUTION_POLICY_ID
    state: SingleAgentExecutionState
    work_packet_id: str
    work_packet_SHA256: DigestText
    allocation_id: str
    allocation_SHA256: DigestText
    profile_id: str
    profile_SHA256: DigestText
    runtime_binding_SHA256: DigestText
    plan_SHA256: DigestText
    workspace_root: AbsolutePathText
    resolved_workspace_root: AbsolutePathText
    next_action_index: int = Field(ge=0, strict=True)
    completed_action_ids: tuple[ActionIdentifier, ...] = ()
    completed_task_step_ids: tuple[str, ...] = ()
    action_evidence: tuple[SingleAgentActionEvidence, ...] = ()
    execution_active: StrictBool
    single_agent_execution_requirement_satisfied: StrictBool
    validation_command_runner_ready: Literal[False] = False
    result_envelopes_ready: Literal[False] = False
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    session_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_session(self) -> SingleAgentExecutionSession:
        if self.completed_action_ids != tuple(
            evidence.action_id
            for evidence in self.action_evidence
            if evidence.disposition is SingleAgentActionDisposition.EXECUTED
        ):
            raise ValueError("completed action IDs must match executed evidence")
        if self.next_action_index < len(self.completed_action_ids):
            raise ValueError("next action index must not precede completed actions")
        if self.state in {
            SingleAgentExecutionState.PREPARED,
            SingleAgentExecutionState.ACTIVE,
        }:
            if not self.execution_active:
                raise ValueError("prepared or active session must be execution-active")
            if self.single_agent_execution_requirement_satisfied:
                raise ValueError(
                    "active session must not satisfy execution requirement"
                )
        elif self.state is SingleAgentExecutionState.COMPLETED:
            if self.execution_active:
                raise ValueError("completed session must not be execution-active")
            if not self.single_agent_execution_requirement_satisfied:
                raise ValueError("completed session must satisfy execution requirement")
        else:
            if (
                self.execution_active
                or self.single_agent_execution_requirement_satisfied
            ):
                raise ValueError("blocked or cancelled session must be inactive")
        if self.session_SHA256 != _session_digest(self):
            raise ValueError("session_SHA256 must match session digest")
        return self


class SingleAgentActionExecutionRequest(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    execution_request: SingleAgentExecutionRequest
    session: SingleAgentExecutionSession
    cancellation_requested: StrictBool = False
    cancellation_reference: BoundedText | None = None

    @model_validator(mode="after")
    def _validate_request(self) -> SingleAgentActionExecutionRequest:
        if self.cancellation_requested and self.cancellation_reference is None:
            raise ValueError("cancellation reference is required")
        if not self.cancellation_requested and self.cancellation_reference is not None:
            raise ValueError("cancellation reference requires cancellation request")
        _validate_session_request_binding(
            session=self.session,
            request=self.execution_request,
            error_type=ValueError,
        )
        return self


class SingleAgentActionExecutionResult(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    disposition: SingleAgentActionDisposition
    action: SingleAgentToolAction
    updated_session: SingleAgentExecutionSession
    observation: SingleAgentToolObservation
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> SingleAgentActionExecutionResult:
        if self.result_SHA256 != _action_result_digest(self):
            raise ValueError("result_SHA256 must match action result digest")
        return self


class SingleAgentExecutionResult(_SingleAgentExecutionModel):
    schema_version: Literal[1] = SINGLE_AGENT_EXECUTION_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-externally-driven-single-agent-filesystem-execution-v1"
    ] = SINGLE_AGENT_EXECUTION_POLICY_ID
    state: Literal[SingleAgentExecutionState.COMPLETED] = (
        SingleAgentExecutionState.COMPLETED
    )
    session: SingleAgentExecutionSession
    completed_action_count: int = Field(ge=1, strict=True)
    completed_task_step_ids: tuple[str, ...]
    touched_paths: tuple[RepositoryRelativePath, ...]
    read_paths: tuple[RepositoryRelativePath, ...]
    created_paths: tuple[RepositoryRelativePath, ...]
    replaced_paths: tuple[RepositoryRelativePath, ...]
    deleted_paths: tuple[RepositoryRelativePath, ...]
    single_agent_execution_requirement_satisfied: Literal[True] = True
    validation_command_runner_ready: Literal[False] = False
    result_envelopes_ready: Literal[False] = False
    diff_artifact_review_ready: Literal[False] = False
    human_git_handoff_ready: Literal[False] = False
    provider_dispatch_count: Literal[0] = 0
    model_inference_count: Literal[0] = 0
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> SingleAgentExecutionResult:
        if self.session.state is not SingleAgentExecutionState.COMPLETED:
            raise ValueError("execution result requires completed session")
        if self.completed_action_count != len(self.session.completed_action_ids):
            raise ValueError("completed action count must match session")
        if self.completed_task_step_ids != self.session.completed_task_step_ids:
            raise ValueError("completed task IDs must match session")
        for paths in (
            self.touched_paths,
            self.read_paths,
            self.created_paths,
            self.replaced_paths,
            self.deleted_paths,
        ):
            if tuple(sorted(frozenset(paths))) != paths:
                raise ValueError("path collections must be unique and sorted")
        if self.result_SHA256 != _execution_result_digest(self):
            raise ValueError("result_SHA256 must match execution result digest")
        return self


def build_single_agent_runtime_binding(
    *,
    agent_id: str,
    worker_id: str,
    work_packet: WorkPacket,
) -> SingleAgentRuntimeBinding:
    """Bind one explicit agent and worker to fixed provider/model identities."""

    packet = _validated_work_packet(work_packet)
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "agent_id": agent_id,
        "worker_id": worker_id,
        "provider": OPENAI_CODEX_PROVIDER,
        "model_id": OPENAI_CODEX_MODEL_ID,
        "provider_runtime_profile_id": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        "worker_profile_id": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
        "externally_driven": True,
        "maximum_concurrent_agents": 1,
        "maximum_concurrent_workers": 1,
        "provider_dispatch_authorized": False,
        "model_inference_authorized": False,
    }
    input_digest = _digest(RUNTIME_BINDING_DIGEST_ALGORITHM, data)
    binding_id = _binding_id(
        ticket_id=packet.ticket_id,
        publication_revision=packet.publication_revision,
        digest_text=input_digest,
    )
    try:
        return SingleAgentRuntimeBinding(
            **data,
            binding_id=binding_id,
            binding_SHA256=_runtime_binding_digest_from_record({
                "binding_id": binding_id,
                **data,
            }),
        )
    except ValueError as exc:
        raise SingleAgentExecutionInputError("runtime binding is invalid") from exc


def build_single_agent_execution_authorization(
    *,
    authorizer_id: str,
    authorization_reference: str,
    rationale: str,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    profile_result: ToolPermissionProfileResult,
    runtime_binding: SingleAgentRuntimeBinding,
    plan: SingleAgentExecutionPlan,
    risk_acknowledgement: str | None = None,
) -> SingleAgentExecutionAuthorization:
    """Build explicit human authorization for exactly one execution plan."""

    packet, allocation, profile = _validated_prerequisites(
        compilation_result=compilation_result,
        allocation_result=allocation_result,
        profile_result=profile_result,
    )
    binding = _validated_runtime_binding(runtime_binding)
    execution_plan = _validated_plan(plan)
    _validate_plan_against_work_packet(
        plan=execution_plan,
        packet=packet,
        error_type=SingleAgentExecutionAuthorizationError,
    )
    if any(
        action.operation in _MUTATING_OPERATIONS for action in execution_plan.actions
    ):
        if risk_acknowledgement is None:
            raise SingleAgentExecutionAuthorizationError(
                "mutating execution plan requires risk acknowledgement"
            )
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "execution_authorized": True,
        "synthetic": False,
        "authorizer_id": authorizer_id,
        "authorization_reference": authorization_reference,
        "rationale": rationale,
        "risk_acknowledgement": risk_acknowledgement,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "profile_id": profile.profile_id,
        "profile_SHA256": profile.profile_SHA256,
        "runtime_binding_SHA256": binding.binding_SHA256,
        "plan_SHA256": execution_plan.plan_SHA256,
    }
    try:
        return SingleAgentExecutionAuthorization(
            **data,
            authorization_SHA256=_execution_authorization_digest_from_record(data),
        )
    except ValueError as exc:
        raise SingleAgentExecutionAuthorizationError(
            "execution authorization is invalid"
        ) from exc


def prepare_single_agent_execution(
    request: SingleAgentExecutionRequest,
) -> SingleAgentExecutionSession:
    """Validate all bindings and prepare an immutable execution session."""

    validated = _validated_execution_request(request)
    packet = validated.compilation_result.work_packet
    allocation = validated.allocation_result.allocation
    profile = validated.profile_result.profile
    validate_work_packet(packet)
    validate_workspace_allocation(allocation)
    validate_tool_permission_profile(profile)
    _validate_execution_request_bindings(
        validated,
        error_type=SingleAgentExecutionInputError,
    )
    inspection = inspect_human_provisioned_workspace(
        workspace_root=allocation.workspace_root,
        repository_identity=allocation.repository_identity,
        require_clean_worktree=validated.require_initial_clean_workspace,
        require_linked_worktree=True,
    )
    _validate_workspace_reinspection(
        inspection=inspection,
        allocation=allocation,
        require_clean=True,
        error_type=SingleAgentExecutionInputError,
    )
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "policy_id": SINGLE_AGENT_EXECUTION_POLICY_ID,
        "state": SingleAgentExecutionState.PREPARED,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "profile_id": profile.profile_id,
        "profile_SHA256": profile.profile_SHA256,
        "runtime_binding_SHA256": validated.runtime_binding.binding_SHA256,
        "plan_SHA256": validated.plan.plan_SHA256,
        "workspace_root": allocation.workspace_root,
        "resolved_workspace_root": allocation.resolved_workspace_root,
        "next_action_index": 0,
        "completed_action_ids": (),
        "completed_task_step_ids": (),
        "action_evidence": (),
        "execution_active": True,
        "single_agent_execution_requirement_satisfied": False,
        "validation_command_runner_ready": False,
        "result_envelopes_ready": False,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
    }
    session_id = _session_id(
        ticket_id=packet.ticket_id,
        publication_revision=packet.publication_revision,
        digest_text=_session_digest_from_record(data),
    )
    return SingleAgentExecutionSession(
        **data,
        session_id=session_id,
        session_SHA256=_session_digest_from_record({"session_id": session_id, **data}),
    )


def execute_single_agent_tool_action(
    request: SingleAgentActionExecutionRequest,
) -> SingleAgentActionExecutionResult:
    """Execute exactly one externally supplied, permission-gated action."""

    try:
        validated = SingleAgentActionExecutionRequest.model_validate(
            request.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise SingleAgentExecutionInputError(
            "action execution request is invalid"
        ) from exc
    except ValueError as exc:
        raise SingleAgentExecutionInputError(
            "action execution request is invalid"
        ) from exc
    execution_request = validated.execution_request
    session = validated.session
    _validate_session_can_execute(session)
    if session.next_action_index >= len(execution_request.plan.actions):
        raise SingleAgentExecutionStateError("session has no next action")
    action = execution_request.plan.actions[session.next_action_index]
    if validated.cancellation_requested:
        return _cancel_action(
            execution_request=execution_request, session=session, action=action
        )

    allocation = execution_request.allocation_result.allocation
    profile = execution_request.profile_result.profile
    inspection = inspect_human_provisioned_workspace(
        workspace_root=allocation.workspace_root,
        repository_identity=allocation.repository_identity,
        require_clean_worktree=False,
        require_linked_worktree=True,
    )
    _validate_workspace_reinspection(
        inspection=inspection,
        allocation=allocation,
        require_clean=False,
        error_type=SingleAgentExecutionStateError,
    )
    resolution = _resolve_target(action=action, allocation=allocation)
    permission_request = ToolPermissionCheckRequest(
        profile=profile,
        allocation=allocation,
        operation=action.operation,
        workspace_relative_path=action.workspace_relative_path,
        resolved_target_path=resolution.resolved_target_path,
        target_resolution_verified=True,
        request_reference=action.action_id,
    )
    decision = evaluate_tool_permission(permission_request)
    validate_tool_permission_decision(decision)
    if decision.decision is ToolPermissionDecision.DENY:
        evidence = _build_action_evidence(
            action=action,
            disposition=SingleAgentActionDisposition.DENIED,
            permission_decision=decision,
            target_resolution=resolution,
            observation=_none_observation(),
            tool_executed=False,
            filesystem_mutated=False,
            rollback_performed=False,
        )
        blocked = _advance_session(
            request=execution_request,
            session=session,
            action=action,
            evidence=evidence,
            state=SingleAgentExecutionState.BLOCKED,
            execution_active=False,
        )
        return _action_result(
            disposition=SingleAgentActionDisposition.DENIED,
            action=action,
            updated_session=blocked,
            observation=_none_observation(),
        )

    _recheck_resolution(action=action, allocation=allocation, expected=resolution)
    observation, mutated, rollback_performed = _execute_filesystem_operation(
        action=action,
        resolution=resolution,
    )
    evidence = _build_action_evidence(
        action=action,
        disposition=SingleAgentActionDisposition.EXECUTED,
        permission_decision=decision,
        target_resolution=resolution,
        observation=observation,
        tool_executed=True,
        filesystem_mutated=mutated,
        rollback_performed=rollback_performed,
    )
    updated = _advance_session(
        request=execution_request,
        session=session,
        action=action,
        evidence=evidence,
        state=SingleAgentExecutionState.ACTIVE,
        execution_active=True,
    )
    return _action_result(
        disposition=SingleAgentActionDisposition.EXECUTED,
        action=action,
        updated_session=updated,
        observation=observation,
    )


def complete_single_agent_execution(
    session: SingleAgentExecutionSession,
) -> SingleAgentExecutionResult:
    """Complete a fully executed single-agent session."""

    try:
        validated = SingleAgentExecutionSession.model_validate(
            session.model_dump(mode="json")
        )
    except ValueError as exc:
        raise SingleAgentExecutionIntegrityError(
            "session integrity is invalid"
        ) from exc
    if validated.state not in {
        SingleAgentExecutionState.PREPARED,
        SingleAgentExecutionState.ACTIVE,
    }:
        raise SingleAgentExecutionStateError("session cannot be completed")
    if not validated.execution_active:
        raise SingleAgentExecutionStateError("session must be active before completion")
    if not validated.action_evidence:
        raise SingleAgentExecutionStateError("session has no completed actions")
    if any(
        evidence.disposition is not SingleAgentActionDisposition.EXECUTED
        for evidence in validated.action_evidence
    ):
        raise SingleAgentExecutionStateError("session contains nonexecuted action")
    if validated.next_action_index != len(validated.completed_action_ids):
        raise SingleAgentExecutionStateError("session action progression is incomplete")
    completed_task_ids = _completed_task_ids_from_evidence(validated.action_evidence)
    if completed_task_ids != validated.completed_task_step_ids:
        raise SingleAgentExecutionStateError("session task progression is incomplete")
    completed_session = _copy_session(
        validated,
        state=SingleAgentExecutionState.COMPLETED,
        execution_active=False,
        single_agent_execution_requirement_satisfied=True,
    )
    paths = _result_paths(completed_session.action_evidence)
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "policy_id": SINGLE_AGENT_EXECUTION_POLICY_ID,
        "state": SingleAgentExecutionState.COMPLETED,
        "session": completed_session,
        "completed_action_count": len(completed_session.completed_action_ids),
        "completed_task_step_ids": completed_session.completed_task_step_ids,
        "touched_paths": paths["touched"],
        "read_paths": paths["read"],
        "created_paths": paths["created"],
        "replaced_paths": paths["replaced"],
        "deleted_paths": paths["deleted"],
        "single_agent_execution_requirement_satisfied": True,
        "validation_command_runner_ready": False,
        "result_envelopes_ready": False,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return SingleAgentExecutionResult(
        **data,
        result_SHA256=_execution_result_digest_from_record(data),
    )


def validate_single_agent_execution_session(
    session: SingleAgentExecutionSession,
) -> None:
    """Validate immutable session evidence without repair."""

    try:
        SingleAgentExecutionSession.model_validate(session.model_dump(mode="json"))
    except ValueError as exc:
        raise SingleAgentExecutionIntegrityError(
            "session integrity is invalid"
        ) from exc


def validate_single_agent_execution_result(
    result: SingleAgentExecutionResult,
) -> None:
    """Validate immutable completion evidence without repair."""

    try:
        SingleAgentExecutionResult.model_validate(result.model_dump(mode="json"))
    except ValueError as exc:
        raise SingleAgentExecutionIntegrityError(
            "execution result integrity is invalid"
        ) from exc


def _validated_work_packet(work_packet: WorkPacket) -> WorkPacket:
    try:
        packet = WorkPacket.model_validate(work_packet.model_dump(mode="json"))
    except AttributeError as exc:
        raise SingleAgentExecutionInputError("WorkPacket is invalid") from exc
    except ValueError as exc:
        raise SingleAgentExecutionInputError("WorkPacket is invalid") from exc
    validate_work_packet(packet)
    return packet


def _validated_runtime_binding(
    binding: SingleAgentRuntimeBinding,
) -> SingleAgentRuntimeBinding:
    try:
        return SingleAgentRuntimeBinding.model_validate(binding.model_dump(mode="json"))
    except AttributeError as exc:
        raise SingleAgentExecutionInputError("runtime binding is invalid") from exc
    except ValueError as exc:
        raise SingleAgentExecutionInputError("runtime binding is invalid") from exc


def _validated_plan(plan: SingleAgentExecutionPlan) -> SingleAgentExecutionPlan:
    try:
        return SingleAgentExecutionPlan.model_validate(plan.model_dump(mode="json"))
    except AttributeError as exc:
        raise SingleAgentExecutionInputError("execution plan is invalid") from exc
    except ValueError as exc:
        raise SingleAgentExecutionInputError("execution plan is invalid") from exc


def _validated_execution_request(
    request: SingleAgentExecutionRequest,
) -> SingleAgentExecutionRequest:
    try:
        return SingleAgentExecutionRequest.model_validate(
            request.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise SingleAgentExecutionInputError("execution request is invalid") from exc
    except ValueError as exc:
        raise SingleAgentExecutionInputError("execution request is invalid") from exc


def _validated_prerequisites(
    *,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    profile_result: ToolPermissionProfileResult,
) -> tuple[WorkPacket, WorkspaceAllocation, ToolPermissionProfile]:
    try:
        result = WorkPacketCompilationResult.model_validate(
            compilation_result.model_dump(mode="json")
        )
        allocation_result = WorkspaceAllocationResult.model_validate(
            allocation_result.model_dump(mode="json")
        )
        profile_result = ToolPermissionProfileResult.model_validate(
            profile_result.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise SingleAgentExecutionInputError("prerequisite result is invalid") from exc
    except ValueError as exc:
        raise SingleAgentExecutionIntegrityError(
            "prerequisite integrity is invalid"
        ) from exc
    packet = result.work_packet
    allocation = allocation_result.allocation
    profile = profile_result.profile
    validate_work_packet(packet)
    validate_workspace_allocation(allocation)
    validate_tool_permission_profile(profile)
    _validate_work_packet_allocation_profile_binding(
        packet=packet,
        allocation=allocation,
        profile=profile,
        error_type=SingleAgentExecutionInputError,
    )
    return packet, allocation, profile


def _validate_execution_request_bindings(
    request: SingleAgentExecutionRequest,
    *,
    error_type: type[Exception],
) -> None:
    packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    _validate_work_packet_allocation_profile_binding(
        packet=packet,
        allocation=allocation,
        profile=profile,
        error_type=error_type,
    )
    if request.require_initial_clean_workspace is not True:
        raise error_type("initial workspace cleanliness is required")
    if request.runtime_binding.provider_dispatch_authorized is not False:
        raise error_type("provider dispatch must remain unauthorized")
    if request.runtime_binding.model_inference_authorized is not False:
        raise error_type("model inference must remain unauthorized")
    _validate_plan_against_work_packet(
        plan=request.plan,
        packet=packet,
        error_type=error_type,
    )
    authorization = request.execution_authorization
    if authorization.work_packet_id != packet.work_packet_id:
        raise error_type("authorization WorkPacket binding mismatch")
    if authorization.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("authorization WorkPacket digest mismatch")
    if authorization.allocation_id != allocation.allocation_id:
        raise error_type("authorization allocation binding mismatch")
    if authorization.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("authorization allocation digest mismatch")
    if authorization.profile_id != profile.profile_id:
        raise error_type("authorization profile binding mismatch")
    if authorization.profile_SHA256 != profile.profile_SHA256:
        raise error_type("authorization profile digest mismatch")
    if authorization.runtime_binding_SHA256 != request.runtime_binding.binding_SHA256:
        raise error_type("authorization runtime binding mismatch")
    if authorization.plan_SHA256 != request.plan.plan_SHA256:
        raise error_type("authorization plan mismatch")


def _validate_work_packet_allocation_profile_binding(
    *,
    packet: WorkPacket,
    allocation: WorkspaceAllocation,
    profile: ToolPermissionProfile,
    error_type: type[Exception],
) -> None:
    if packet.execution_ready is not False:
        raise error_type("WorkPacket must remain compile-only")
    if not any(
        requirement.capability is WorkPacketDownstreamCapability.SINGLE_AGENT_EXECUTION
        for requirement in packet.downstream_requirements
    ):
        raise error_type("WorkPacket lacks single-agent downstream requirement")
    if allocation.work_packet_id != packet.work_packet_id:
        raise error_type("allocation WorkPacket binding mismatch")
    if allocation.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("allocation WorkPacket digest mismatch")
    if allocation.workspace_requirement_satisfied is not True:
        raise error_type("workspace requirement must be satisfied")
    if allocation.execution_ready is not False:
        raise error_type("workspace allocation must not be execution-ready")
    if allocation.exclusive is not True:
        raise error_type("workspace allocation must be exclusive")
    if allocation.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("workspace Git authority must be human-only")
    if profile.work_packet_id != packet.work_packet_id:
        raise error_type("profile WorkPacket binding mismatch")
    if profile.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("profile WorkPacket digest mismatch")
    if profile.allocation_id != allocation.allocation_id:
        raise error_type("profile allocation binding mismatch")
    if profile.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("profile allocation digest mismatch")
    if (
        profile.tool_permissions_ready is not True
        or profile.execution_ready is not False
    ):
        raise error_type("profile must be deny-first and non-executing")


def _validate_plan_against_work_packet(
    *,
    plan: SingleAgentExecutionPlan,
    packet: WorkPacket,
    error_type: type[Exception],
) -> None:
    task_order = {task.step_id: index for index, task in enumerate(packet.tasks)}
    seen_tasks: set[str] = set()
    previous_index = -1
    for action in plan.actions:
        if action.task_step_id not in task_order:
            raise error_type("plan references unknown task step")
        current_index = task_order[action.task_step_id]
        if current_index < previous_index:
            raise error_type("plan returns to an earlier task step")
        previous_index = current_index
        seen_tasks.add(action.task_step_id)
    if seen_tasks != set(task_order):
        raise error_type("plan must cover every WorkPacket task step")


def _validate_session_request_binding(
    *,
    session: SingleAgentExecutionSession,
    request: SingleAgentExecutionRequest,
    error_type: type[Exception],
) -> None:
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    packet = request.compilation_result.work_packet
    pairs = (
        (session.work_packet_id, packet.work_packet_id, "WorkPacket"),
        (session.work_packet_SHA256, packet.work_packet_SHA256, "WorkPacket digest"),
        (session.allocation_id, allocation.allocation_id, "allocation"),
        (session.allocation_SHA256, allocation.allocation_SHA256, "allocation digest"),
        (session.profile_id, profile.profile_id, "profile"),
        (session.profile_SHA256, profile.profile_SHA256, "profile digest"),
        (
            session.runtime_binding_SHA256,
            request.runtime_binding.binding_SHA256,
            "runtime binding",
        ),
        (session.plan_SHA256, request.plan.plan_SHA256, "plan"),
    )
    for left, right, label in pairs:
        if left != right:
            raise error_type(f"session {label} binding mismatch")


def _validate_session_can_execute(session: SingleAgentExecutionSession) -> None:
    validate_single_agent_execution_session(session)
    if session.state in {
        SingleAgentExecutionState.BLOCKED,
        SingleAgentExecutionState.CANCELLED,
        SingleAgentExecutionState.COMPLETED,
    }:
        raise SingleAgentExecutionStateError("session cannot execute another action")
    if not session.execution_active:
        raise SingleAgentExecutionStateError("session is not execution-active")


def _validate_workspace_reinspection(
    *,
    inspection,
    allocation: WorkspaceAllocation,
    require_clean: bool,
    error_type: type[Exception],
) -> None:
    if inspection.workspace_root != allocation.workspace_root:
        raise error_type("workspace root mismatch")
    if inspection.resolved_workspace_root != allocation.resolved_workspace_root:
        raise error_type("resolved workspace root mismatch")
    if inspection.git_top_level != allocation.resolved_workspace_root:
        raise error_type("workspace top level mismatch")
    if inspection.source_commit != allocation.repository_identity.source_commit:
        raise error_type("workspace HEAD mismatch")
    if inspection.workspace_branch != allocation.repository_identity.workspace_branch:
        raise error_type("workspace branch mismatch")
    if (
        inspection.linked_worktree is not True
        or inspection.inside_work_tree is not True
    ):
        raise error_type("workspace must remain a linked worktree")
    if require_clean and inspection.clean is not True:
        raise error_type("workspace must be clean")


def _resolve_target(
    *, action: SingleAgentToolAction, allocation: WorkspaceAllocation
) -> SingleAgentTargetResolutionEvidence:
    relative = _validate_repository_relative_path(action.workspace_relative_path)
    root = Path(allocation.resolved_workspace_root)
    try:
        root_resolved = root.resolve(strict=True)
    except OSError as exc:
        raise SingleAgentTargetResolutionError(
            "workspace root cannot be resolved"
        ) from exc
    if root.is_symlink() or not root_resolved.is_dir():
        raise SingleAgentTargetResolutionError("workspace root is unsafe")
    target = root.joinpath(*relative.split("/"))
    if target == root:
        raise SingleAgentTargetResolutionError("workspace root target is not allowed")
    _reject_symlink_components(root_resolved, target)
    parent = target.parent
    parent_exists = parent.exists()
    nearest_parent = parent
    while not nearest_parent.exists() and nearest_parent != root_resolved:
        nearest_parent = nearest_parent.parent
    try:
        resolved_parent = nearest_parent.resolve(strict=True)
    except OSError as exc:
        raise SingleAgentTargetResolutionError(
            "target parent cannot be resolved"
        ) from exc
    if not _path_is_under(resolved_parent, root_resolved):
        raise SingleAgentTargetResolutionError("target parent escapes workspace")
    if target.exists():
        if target.is_symlink():
            raise SingleAgentTargetResolutionError("target symlink is not allowed")
        try:
            resolved_target = target.resolve(strict=True)
        except OSError as exc:
            raise SingleAgentTargetResolutionError("target cannot be resolved") from exc
    else:
        resolved_target = resolved_parent.joinpath(
            *target.relative_to(nearest_parent).parts
        )
    if not _path_is_under(resolved_target, root_resolved):
        raise SingleAgentTargetResolutionError("target escapes workspace")
    kind = _target_kind(target)
    preexisting_sha = (
        _file_sha256_if_utf8(target) if kind is SingleAgentTargetKind.FILE else None
    )
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "action_id": action.action_id,
        "workspace_relative_path": relative,
        "candidate_target_path": _path_text(target),
        "resolved_target_path": _path_text(resolved_target),
        "target_kind_before": kind,
        "target_exists_before": target.exists(),
        "parent_exists": parent_exists,
        "under_workspace": True,
        "symlink_safe": True,
        "preexisting_SHA256": preexisting_sha,
    }
    return SingleAgentTargetResolutionEvidence(
        **data,
        resolution_SHA256=_target_resolution_digest_from_record(data),
    )


def _recheck_resolution(
    *,
    action: SingleAgentToolAction,
    allocation: WorkspaceAllocation,
    expected: SingleAgentTargetResolutionEvidence,
) -> None:
    current = _resolve_target(action=action, allocation=allocation)
    if current.resolved_target_path != expected.resolved_target_path:
        raise SingleAgentTargetResolutionError("target resolution changed")


def _reject_symlink_components(root: Path, target: Path) -> None:
    current = root
    for part in target.relative_to(root).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise SingleAgentTargetResolutionError("symlink component is not allowed")


def _execute_filesystem_operation(
    *,
    action: SingleAgentToolAction,
    resolution: SingleAgentTargetResolutionEvidence,
) -> tuple[SingleAgentToolObservation, bool, bool]:
    target = Path(resolution.resolved_target_path)
    operation = action.operation
    if operation is ToolPermissionOperation.LIST_DIRECTORY:
        return _list_directory(target), False, False
    if operation is ToolPermissionOperation.READ_FILE:
        return _read_file(target), False, False
    if operation is ToolPermissionOperation.CREATE_FILE:
        return _create_file(action=action, target=target), True, False
    if operation is ToolPermissionOperation.REPLACE_FILE:
        return _replace_file(action=action, target=target), True, False
    if operation is ToolPermissionOperation.DELETE_FILE:
        return _delete_file(action=action, target=target), True, False
    if operation is ToolPermissionOperation.CREATE_DIRECTORY:
        return _create_directory(target=target, action_id=action.action_id), True, False
    if operation is ToolPermissionOperation.DELETE_DIRECTORY:
        return _delete_directory(target=target, action_id=action.action_id), True, False
    raise SingleAgentToolExecutionError("unsupported filesystem operation")


def _list_directory(target: Path) -> SingleAgentToolObservation:
    if not target.exists() or not target.is_dir() or target.is_symlink():
        raise SingleAgentToolExecutionError("list_directory requires directory target")
    entries = sorted(path.name for path in target.iterdir())
    if len(entries) > MAX_DIRECTORY_ENTRIES:
        raise SingleAgentToolExecutionError("directory entry bound exceeded")
    return _directory_observation(tuple(entries))


def _read_file(target: Path) -> SingleAgentToolObservation:
    text = _read_utf8_regular_file(target)
    return _text_observation(text)


def _create_file(
    *, action: SingleAgentToolAction, target: Path
) -> SingleAgentToolObservation:
    if action.content is None:
        raise SingleAgentToolExecutionError("create_file content missing")
    if target.exists():
        raise SingleAgentToolExecutionError("create_file target exists")
    _require_parent_directory(target)
    try:
        with target.open("x", encoding="utf-8", newline="") as handle:
            handle.write(action.content)
        _after_filesystem_mutation_hook(action.action_id)
    except Exception as exc:
        _rollback_created_file(target)
        raise SingleAgentToolExecutionError(
            "create_file post-mutation failure"
        ) from exc
    return _none_observation()


def _replace_file(
    *, action: SingleAgentToolAction, target: Path
) -> SingleAgentToolObservation:
    if action.content is None or action.expected_preexisting_SHA256 is None:
        raise SingleAgentToolExecutionError("replace_file precondition missing")
    original = _read_utf8_regular_file_bytes(target)
    if _sha256_bytes(original) != action.expected_preexisting_SHA256:
        raise SingleAgentToolExecutionError("replace_file digest precondition failed")
    try:
        target.write_text(action.content, encoding="utf-8", newline="")
        _after_filesystem_mutation_hook(action.action_id)
    except Exception as exc:
        _rollback_replaced_file(target, original)
        raise SingleAgentToolExecutionError(
            "replace_file post-mutation failure"
        ) from exc
    return _none_observation()


def _delete_file(
    *, action: SingleAgentToolAction, target: Path
) -> SingleAgentToolObservation:
    if action.expected_preexisting_SHA256 is None:
        raise SingleAgentToolExecutionError("delete_file precondition missing")
    original = _read_utf8_regular_file_bytes(target)
    if _sha256_bytes(original) != action.expected_preexisting_SHA256:
        raise SingleAgentToolExecutionError("delete_file digest precondition failed")
    try:
        target.unlink()
        _after_filesystem_mutation_hook(action.action_id)
    except Exception as exc:
        _rollback_deleted_file(target, original)
        raise SingleAgentToolExecutionError(
            "delete_file post-mutation failure"
        ) from exc
    return _none_observation()


def _create_directory(*, target: Path, action_id: str) -> SingleAgentToolObservation:
    if target.exists():
        raise SingleAgentToolExecutionError("create_directory target exists")
    _require_parent_directory(target)
    try:
        target.mkdir()
        _after_filesystem_mutation_hook(action_id)
    except Exception as exc:
        _rollback_created_directory(target)
        raise SingleAgentToolExecutionError(
            "create_directory post-mutation failure"
        ) from exc
    return _none_observation()


def _delete_directory(*, target: Path, action_id: str) -> SingleAgentToolObservation:
    if not target.exists() or not target.is_dir() or target.is_symlink():
        raise SingleAgentToolExecutionError(
            "delete_directory requires directory target"
        )
    if any(target.iterdir()):
        raise SingleAgentToolExecutionError("delete_directory requires empty directory")
    try:
        target.rmdir()
        _after_filesystem_mutation_hook(action_id)
    except Exception as exc:
        _rollback_deleted_directory(target)
        raise SingleAgentToolExecutionError(
            "delete_directory post-mutation failure"
        ) from exc
    return _none_observation()


def _require_parent_directory(target: Path) -> None:
    parent = target.parent
    if not parent.exists() or not parent.is_dir() or parent.is_symlink():
        raise SingleAgentToolExecutionError("parent directory precondition failed")


def _read_utf8_regular_file(target: Path) -> str:
    return _read_utf8_regular_file_bytes(target).decode("utf-8")


def _read_utf8_regular_file_bytes(target: Path) -> bytes:
    if not target.exists() or not target.is_file() or target.is_symlink():
        raise SingleAgentToolExecutionError("file operation requires regular file")
    data = target.read_bytes()
    if len(data) > MAX_TEXT_BYTES:
        raise SingleAgentToolExecutionError("file byte bound exceeded")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SingleAgentToolExecutionError("file must be UTF-8") from exc
    return data


def _rollback_created_file(target: Path) -> None:
    try:
        if target.exists() and target.is_file() and not target.is_symlink():
            target.unlink()
    except OSError as exc:
        raise SingleAgentToolExecutionError("P17.3-ROLLBACK-FAILED") from exc


def _rollback_replaced_file(target: Path, original: bytes) -> None:
    try:
        target.write_bytes(original)
    except OSError as exc:
        raise SingleAgentToolExecutionError("P17.3-ROLLBACK-FAILED") from exc


def _rollback_deleted_file(target: Path, original: bytes) -> None:
    try:
        target.write_bytes(original)
    except OSError as exc:
        raise SingleAgentToolExecutionError("P17.3-ROLLBACK-FAILED") from exc


def _rollback_created_directory(target: Path) -> None:
    try:
        if target.exists() and target.is_dir() and not any(target.iterdir()):
            target.rmdir()
    except OSError as exc:
        raise SingleAgentToolExecutionError("P17.3-ROLLBACK-FAILED") from exc


def _rollback_deleted_directory(target: Path) -> None:
    try:
        target.mkdir()
    except OSError as exc:
        raise SingleAgentToolExecutionError("P17.3-ROLLBACK-FAILED") from exc


def _after_filesystem_mutation_hook(action_id: str) -> None:
    _ = action_id


def _build_action_evidence(
    *,
    action: SingleAgentToolAction,
    disposition: SingleAgentActionDisposition,
    permission_decision: ToolPermissionDecisionEvidence | None,
    target_resolution: SingleAgentTargetResolutionEvidence | None,
    observation: SingleAgentToolObservation,
    tool_executed: bool,
    filesystem_mutated: bool,
    rollback_performed: bool,
) -> SingleAgentActionEvidence:
    target = Path(target_resolution.resolved_target_path) if target_resolution else None
    kind_after = _target_kind(target) if target is not None else None
    post_sha = (
        _file_sha256_if_utf8(target)
        if target is not None and kind_after is SingleAgentTargetKind.FILE
        else None
    )
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "action_id": action.action_id,
        "task_step_id": action.task_step_id,
        "operation": action.operation,
        "disposition": disposition,
        "permission_decision": permission_decision.decision
        if permission_decision is not None
        else None,
        "target_resolution": target_resolution,
        "target_kind_after": kind_after,
        "target_exists_after": target.exists() if target is not None else False,
        "postexisting_SHA256": post_sha,
        "tool_executed": tool_executed,
        "filesystem_mutated": filesystem_mutated,
        "rollback_performed": rollback_performed,
        "observation_SHA256": observation.observation_SHA256,
    }
    return SingleAgentActionEvidence(
        **data,
        evidence_SHA256=_action_evidence_digest_from_record(data),
    )


def _advance_session(
    *,
    request: SingleAgentExecutionRequest,
    session: SingleAgentExecutionSession,
    action: SingleAgentToolAction,
    evidence: SingleAgentActionEvidence,
    state: SingleAgentExecutionState,
    execution_active: bool,
) -> SingleAgentExecutionSession:
    action_evidence = (*session.action_evidence, evidence)
    completed_actions = session.completed_action_ids
    completed_tasks = session.completed_task_step_ids
    next_index = session.next_action_index
    if evidence.disposition is SingleAgentActionDisposition.EXECUTED:
        completed_actions = (*completed_actions, action.action_id)
        next_index = session.next_action_index + 1
        completed_tasks = _completed_task_progression(
            request=request,
            evidence=action_evidence,
            completed_task_ids=completed_tasks,
        )
    data = session.model_dump(mode="python", exclude={"session_SHA256"})
    data.update({
        "state": state,
        "next_action_index": next_index,
        "completed_action_ids": completed_actions,
        "completed_task_step_ids": completed_tasks,
        "action_evidence": action_evidence,
        "execution_active": execution_active,
        "single_agent_execution_requirement_satisfied": False,
    })
    return SingleAgentExecutionSession(
        **data,
        session_SHA256=_session_digest_from_record(data),
    )


def _copy_session(
    session: SingleAgentExecutionSession,
    **updates: object,
) -> SingleAgentExecutionSession:
    data = session.model_dump(mode="python", exclude={"session_SHA256"})
    data.update(updates)
    return SingleAgentExecutionSession(
        **data,
        session_SHA256=_session_digest_from_record(data),
    )


def _completed_task_progression(
    *,
    request: SingleAgentExecutionRequest,
    evidence: tuple[SingleAgentActionEvidence, ...],
    completed_task_ids: tuple[str, ...],
) -> tuple[str, ...]:
    executed_by_task = {
        item.task_step_id
        for item in evidence
        if item.disposition is SingleAgentActionDisposition.EXECUTED
    }
    completed = list(completed_task_ids)
    for task in request.compilation_result.work_packet.tasks:
        if task.step_id in completed:
            continue
        planned = tuple(
            action
            for action in request.plan.actions
            if action.task_step_id == task.step_id
        )
        if planned and all(
            action.task_step_id in executed_by_task for action in planned
        ):
            if all(
                any(
                    item.action_id == action.action_id
                    and item.disposition is SingleAgentActionDisposition.EXECUTED
                    for item in evidence
                )
                for action in planned
            ):
                completed.append(task.step_id)
        else:
            break
    return tuple(completed)


def _completed_task_ids_from_evidence(
    evidence: tuple[SingleAgentActionEvidence, ...],
) -> tuple[str, ...]:
    task_ids: list[str] = []
    for item in evidence:
        if item.disposition is SingleAgentActionDisposition.EXECUTED:
            if item.task_step_id not in task_ids:
                task_ids.append(item.task_step_id)
    return tuple(task_ids)


def _cancel_action(
    *,
    execution_request: SingleAgentExecutionRequest,
    session: SingleAgentExecutionSession,
    action: SingleAgentToolAction,
) -> SingleAgentActionExecutionResult:
    observation = _none_observation()
    evidence = _build_action_evidence(
        action=action,
        disposition=SingleAgentActionDisposition.CANCELLED,
        permission_decision=None,
        target_resolution=None,
        observation=observation,
        tool_executed=False,
        filesystem_mutated=False,
        rollback_performed=False,
    )
    cancelled = _advance_session(
        request=execution_request,
        session=session,
        action=action,
        evidence=evidence,
        state=SingleAgentExecutionState.CANCELLED,
        execution_active=False,
    )
    return _action_result(
        disposition=SingleAgentActionDisposition.CANCELLED,
        action=action,
        updated_session=cancelled,
        observation=observation,
    )


def _action_result(
    *,
    disposition: SingleAgentActionDisposition,
    action: SingleAgentToolAction,
    updated_session: SingleAgentExecutionSession,
    observation: SingleAgentToolObservation,
) -> SingleAgentActionExecutionResult:
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "disposition": disposition,
        "action": action,
        "updated_session": updated_session,
        "observation": observation,
    }
    return SingleAgentActionExecutionResult(
        **data,
        result_SHA256=_action_result_digest_from_record(data),
    )


def _none_observation() -> SingleAgentToolObservation:
    data = {
        "kind": SingleAgentToolObservationKind.NONE,
        "text": None,
        "directory_entries": (),
        "byte_count": 0,
        "content_SHA256": None,
    }
    return SingleAgentToolObservation(
        **data,
        observation_SHA256=_observation_digest_from_record(data),
    )


def _text_observation(text: str) -> SingleAgentToolObservation:
    data_bytes = text.encode("utf-8")
    data = {
        "kind": SingleAgentToolObservationKind.TEXT,
        "text": text,
        "directory_entries": (),
        "byte_count": len(data_bytes),
        "content_SHA256": _sha256_bytes(data_bytes),
    }
    return SingleAgentToolObservation(
        **data,
        observation_SHA256=_observation_digest_from_record(data),
    )


def _directory_observation(entries: tuple[str, ...]) -> SingleAgentToolObservation:
    data = {
        "kind": SingleAgentToolObservationKind.DIRECTORY_ENTRIES,
        "text": None,
        "directory_entries": entries,
        "byte_count": 0,
        "content_SHA256": None,
    }
    return SingleAgentToolObservation(
        **data,
        observation_SHA256=_observation_digest_from_record(data),
    )


def _result_paths(
    evidence: tuple[SingleAgentActionEvidence, ...],
) -> dict[str, tuple[str, ...]]:
    touched: list[str] = []
    read: list[str] = []
    created: list[str] = []
    replaced: list[str] = []
    deleted: list[str] = []
    for item in evidence:
        if item.disposition is not SingleAgentActionDisposition.EXECUTED:
            continue
        if item.target_resolution is None:
            continue
        path = item.target_resolution.workspace_relative_path
        touched.append(path)
        if item.operation in {
            ToolPermissionOperation.READ_FILE,
            ToolPermissionOperation.LIST_DIRECTORY,
        }:
            read.append(path)
        elif item.operation in {
            ToolPermissionOperation.CREATE_FILE,
            ToolPermissionOperation.CREATE_DIRECTORY,
        }:
            created.append(path)
        elif item.operation is ToolPermissionOperation.REPLACE_FILE:
            replaced.append(path)
        elif item.operation in {
            ToolPermissionOperation.DELETE_FILE,
            ToolPermissionOperation.DELETE_DIRECTORY,
        }:
            deleted.append(path)
    return {
        "touched": _sorted_unique(touched),
        "read": _sorted_unique(read),
        "created": _sorted_unique(created),
        "replaced": _sorted_unique(replaced),
        "deleted": _sorted_unique(deleted),
    }


def _target_kind(path: Path | None) -> SingleAgentTargetKind:
    if path is None or not path.exists():
        return SingleAgentTargetKind.ABSENT
    if path.is_dir():
        return SingleAgentTargetKind.DIRECTORY
    if path.is_file():
        return SingleAgentTargetKind.FILE
    raise SingleAgentTargetResolutionError("unsupported filesystem target kind")


def _file_sha256_if_utf8(path: Path) -> str | None:
    if not path.exists() or not path.is_file() or path.is_symlink():
        return None
    data = path.read_bytes()
    if len(data) > MAX_TEXT_BYTES:
        return None
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return _sha256_bytes(data)


def _path_is_under(target: Path, root: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def _path_text(path: Path) -> str:
    return path.as_posix().rstrip("/")


def _path_matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(_path_matches(path, pattern) for pattern in patterns)


def _path_matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        base = pattern[:-3]
        return path == base or path.startswith(f"{base}/")
    return path == pattern


def _sorted_unique(values: list[str]) -> tuple[str, ...]:
    return tuple(sorted(frozenset(values)))


def _binding_id(*, ticket_id: str, publication_revision: int, digest_text: str) -> str:
    return f"SAB-{ticket_id.replace('.', '-')}-R{publication_revision:04d}-{digest_text[:12]}"


def _session_id(*, ticket_id: str, publication_revision: int, digest_text: str) -> str:
    return f"SAE-{ticket_id.replace('.', '-')}-R{publication_revision:04d}-{digest_text[:12]}"


def _runtime_binding_id_from_binding(binding: SingleAgentRuntimeBinding) -> str:
    prefix = binding.binding_id.rsplit("-", 1)[0]
    input_record = binding.model_dump(
        mode="json", exclude={"binding_id", "binding_SHA256"}
    )
    return f"{prefix}-{_digest(RUNTIME_BINDING_DIGEST_ALGORITHM, input_record)[:12]}"


def _is_shadow_identifier(value: str) -> bool:
    return value.upper().startswith("SHADOW-") or value.casefold().startswith("shadow-")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _dump_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_dump_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _dump_value(item) for key, item in value.items()}
    return value


def _normalized_record(record: dict[str, object]) -> dict[str, object]:
    return {key: _dump_value(value) for key, value in record.items()}


def _digest(algorithm: str, record: dict[str, object]) -> str:
    return _sha256_text(
        _deterministic_json({"algorithm": algorithm, **_normalized_record(record)})
    )


def _runtime_binding_digest(binding: SingleAgentRuntimeBinding) -> str:
    return _runtime_binding_digest_from_record(
        binding.model_dump(mode="json", exclude={"binding_SHA256"})
    )


def _runtime_binding_digest_from_record(record: dict[str, object]) -> str:
    return _digest(RUNTIME_BINDING_DIGEST_ALGORITHM, record)


def _action_digest(action: SingleAgentToolAction) -> str:
    return _action_digest_from_record(
        action.model_dump(mode="json", exclude={"action_SHA256"})
    )


def _action_digest_from_record(record: dict[str, object]) -> str:
    return _digest(ACTION_DIGEST_ALGORITHM, record)


def _plan_digest(plan: SingleAgentExecutionPlan) -> str:
    return _plan_digest_from_record(
        plan.model_dump(mode="json", exclude={"plan_SHA256"})
    )


def _plan_digest_from_record(record: dict[str, object]) -> str:
    return _digest(PLAN_DIGEST_ALGORITHM, record)


def _execution_authorization_digest(
    authorization: SingleAgentExecutionAuthorization,
) -> str:
    return _execution_authorization_digest_from_record(
        authorization.model_dump(mode="json", exclude={"authorization_SHA256"})
    )


def _execution_authorization_digest_from_record(record: dict[str, object]) -> str:
    return _digest(AUTHORIZATION_DIGEST_ALGORITHM, record)


def _target_resolution_digest(evidence: SingleAgentTargetResolutionEvidence) -> str:
    return _target_resolution_digest_from_record(
        evidence.model_dump(mode="json", exclude={"resolution_SHA256"})
    )


def _target_resolution_digest_from_record(record: dict[str, object]) -> str:
    return _digest(TARGET_RESOLUTION_DIGEST_ALGORITHM, record)


def _observation_digest(observation: SingleAgentToolObservation) -> str:
    return _observation_digest_from_record(
        observation.model_dump(mode="json", exclude={"observation_SHA256"})
    )


def _observation_digest_from_record(record: dict[str, object]) -> str:
    return _digest(OBSERVATION_DIGEST_ALGORITHM, record)


def _action_evidence_digest(evidence: SingleAgentActionEvidence) -> str:
    return _action_evidence_digest_from_record(
        evidence.model_dump(mode="json", exclude={"evidence_SHA256"})
    )


def _action_evidence_digest_from_record(record: dict[str, object]) -> str:
    return _digest(ACTION_EVIDENCE_DIGEST_ALGORITHM, record)


def _session_digest(session: SingleAgentExecutionSession) -> str:
    return _session_digest_from_record(
        session.model_dump(mode="json", exclude={"session_SHA256"})
    )


def _session_digest_from_record(record: dict[str, object]) -> str:
    return _digest(SESSION_DIGEST_ALGORITHM, record)


def _action_result_digest(result: SingleAgentActionExecutionResult) -> str:
    return _action_result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _action_result_digest_from_record(record: dict[str, object]) -> str:
    return _digest(ACTION_RESULT_DIGEST_ALGORITHM, record)


def _execution_result_digest(result: SingleAgentExecutionResult) -> str:
    return _execution_result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _execution_result_digest_from_record(record: dict[str, object]) -> str:
    return _digest(EXECUTION_RESULT_DIGEST_ALGORITHM, record)
