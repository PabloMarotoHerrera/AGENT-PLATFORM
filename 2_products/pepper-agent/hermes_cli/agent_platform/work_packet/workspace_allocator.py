"""Human-provisioned workspace allocation contracts for Agent Platform P17.1.

The allocator validates an already-provisioned linked Git worktree and binds it
to one compile-only WorkPacket. It never creates worktrees, mutates Git, grants
tools, assigns agents, runs commands or persists allocation state.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
from pathlib import Path
import re
import subprocess
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
    WorkPacketAuthorityBoundary,
    WorkPacketCompilationDisposition,
    WorkPacketCompilationResult,
    WorkPacketDownstreamCapability,
    WorkPacketGitAuthority,
    validate_work_packet,
)

WORKSPACE_ALLOCATION_SCHEMA_VERSION = 1
WORKSPACE_ALLOCATION_POLICY_ID = "pepper-human-provisioned-workspace-allocation-v1"

REPOSITORY_IDENTITY_DIGEST_ALGORITHM = (
    "agent-platform-workspace-repository-identity-sha256-v1"
)
ALLOCATION_AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-workspace-allocation-authorization-sha256-v1"
)
INSPECTION_EVIDENCE_DIGEST_ALGORITHM = (
    "agent-platform-workspace-inspection-evidence-sha256-v1"
)
SCOPE_PROJECTION_DIGEST_ALGORITHM = (
    "agent-platform-workspace-scope-projection-sha256-v1"
)
RESERVATION_DIGEST_ALGORITHM = "agent-platform-workspace-reservation-sha256-v1"
REGISTRY_DIGEST_ALGORITHM = "agent-platform-workspace-allocation-registry-sha256-v1"
ALLOCATION_INPUT_DIGEST_ALGORITHM = (
    "agent-platform-workspace-allocation-input-sha256-v1"
)
ALLOCATION_DIGEST_ALGORITHM = "agent-platform-workspace-allocation-sha256-v1"
ALLOCATION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-workspace-allocation-result-sha256-v1"
)
CLEANUP_ASSESSMENT_DIGEST_ALGORITHM = (
    "agent-platform-workspace-cleanup-assessment-sha256-v1"
)

_READ_ONLY_GIT_TIMEOUT_SECONDS = 5
_WORKSPACE_ALLOCATION_ID_PATTERN = (
    r"^WS-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"
)
_REPOSITORY_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$"
_HUMAN_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$"
_DRIVE_ABSOLUTE_PATTERN = re.compile(r"^[A-Za-z]:/")
_DRIVE_ROOT_PATTERN = re.compile(r"^[A-Za-z]:/$")
_GIT_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
_CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
_BRANCH_FORBIDDEN_MARKERS = ("\\", "..", "@{", "~", "^", ":", "?", "*", "[")
_PROTECTED_WORKSPACE_COMPONENTS = frozenset((".git", ".opencode", "graphify-out"))
_PROTECTED_BASELINE_SUFFIX = (
    "2_products/pepper-agent/agent_platform_upstream_baseline.json"
)


class WorkspaceAllocatorError(ValueError):
    """Base error for P17.1 workspace allocator failures."""


class WorkspaceAllocatorInputError(WorkspaceAllocatorError):
    """Raised when allocator inputs or bindings are structurally invalid."""


class WorkspaceAllocatorAuthorizationError(WorkspaceAllocatorError):
    """Raised when human allocation authorization is absent or invalid."""


class WorkspaceAllocatorInspectionError(WorkspaceAllocatorError):
    """Raised when read-only workspace inspection rejects the workspace."""


class WorkspaceAllocatorCollisionError(WorkspaceAllocatorError):
    """Raised when a caller-supplied registry contains an active collision."""


class WorkspaceAllocatorIntegrityError(WorkspaceAllocatorError):
    """Raised when deterministic allocator digest evidence is invalid."""


class WorkspaceKind(str, Enum):
    HUMAN_PROVISIONED_GIT_WORKTREE = "human_provisioned_git_worktree"


class WorkspaceLifecycleState(str, Enum):
    ALLOCATED = "allocated"


class WorkspaceIsolationLevel(str, Enum):
    DEDICATED = "dedicated"


class WorkspaceAllocationDisposition(str, Enum):
    ALLOCATED = "allocated"


class WorkspaceCleanupEligibility(str, Enum):
    NOT_ELIGIBLE = "not_eligible"
    ELIGIBLE = "eligible"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


def _validate_branch_identifier(value: str) -> str:
    if not value or value.startswith("-"):
        raise ValueError("workspace branch must be a named branch")
    if any(character.isspace() for character in value):
        raise ValueError("workspace branch must not contain whitespace")
    if _CONTROL_CHARACTER_PATTERN.search(value):
        raise ValueError("workspace branch must not contain control characters")
    if any(marker in value for marker in _BRANCH_FORBIDDEN_MARKERS):
        raise ValueError("workspace branch contains forbidden ref syntax")
    return value


def _workspace_root_is_filesystem_root(value: str) -> bool:
    return value == "/" or bool(_DRIVE_ROOT_PATTERN.match(value))


def _workspace_path_parts(value: str) -> tuple[str, ...]:
    if _DRIVE_ABSOLUTE_PATTERN.match(value):
        value = value[3:]
    else:
        value = value[1:]
    return tuple(part for part in value.split("/") if part)


def _validate_absolute_workspace_path(value: str) -> str:
    if "\x00" in value:
        raise ValueError("workspace root must not contain NUL characters")
    if "\\" in value:
        raise ValueError("workspace root must use forward slashes")
    if not (value.startswith("/") or _DRIVE_ABSOLUTE_PATTERN.match(value)):
        raise ValueError("workspace root must be absolute")
    if value.endswith("/") and not _workspace_root_is_filesystem_root(value):
        raise ValueError("workspace root must not have a trailing separator")
    parts = _workspace_path_parts(value)
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("workspace root must not contain traversal components")
    lowered_parts = tuple(part.casefold() for part in parts)
    if any(part in _PROTECTED_WORKSPACE_COMPONENTS for part in lowered_parts):
        raise ValueError("workspace root targets a protected path")
    for index in range(len(lowered_parts) - 1):
        if (
            lowered_parts[index] == "4_external"
            and lowered_parts[index + 1] == "sources"
        ):
            raise ValueError("workspace root targets a protected path")
    if value.casefold().endswith(_PROTECTED_BASELINE_SUFFIX):
        raise ValueError("workspace root targets a protected path")
    return value


WorkspaceAllocationIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=24, max_length=96, pattern=_WORKSPACE_ALLOCATION_ID_PATTERN
    ),
]
WorkspaceRepositoryIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=3, max_length=96, pattern=_REPOSITORY_ID_PATTERN),
]
WorkspaceBranchIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
    AfterValidator(_validate_branch_identifier),
]
HumanWorkspaceAuthorizerIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=3, max_length=96, pattern=_HUMAN_ID_PATTERN),
]
AbsoluteWorkspacePath: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=512),
    AfterValidator(_validate_absolute_workspace_path),
]
GitCommitIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=40, max_length=40, pattern=_GIT_COMMIT_PATTERN),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]


class _WorkspaceAllocatorModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


class WorkspaceRepositoryIdentity(_WorkspaceAllocatorModel):
    repository_id: WorkspaceRepositoryIdentifier
    source_commit: GitCommitIdentifier
    workspace_branch: WorkspaceBranchIdentifier
    identity_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_identity(self) -> WorkspaceRepositoryIdentity:
        if self.identity_SHA256 != _repository_identity_digest(self):
            raise ValueError("identity_SHA256 must match repository identity digest")
        return self


class WorkspaceAllocationAuthorization(_WorkspaceAllocatorModel):
    schema_version: Literal[1] = WORKSPACE_ALLOCATION_SCHEMA_VERSION
    allocation_authorized: Literal[True] = True
    synthetic: Literal[False] = False
    authorizer_id: HumanWorkspaceAuthorizerIdentifier
    authorization_reference: BoundedText
    rationale: BoundedText
    risk_acknowledgement: BoundedText | None = None
    work_packet_id: str
    work_packet_SHA256: DigestText
    repository_identity_SHA256: DigestText
    workspace_root: AbsoluteWorkspacePath
    workspace_kind: Literal[WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE] = (
        WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE
    )
    git_authority: Literal[WorkPacketGitAuthority.HUMAN_ONLY] = (
        WorkPacketGitAuthority.HUMAN_ONLY
    )
    authorization_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_authorization(self) -> WorkspaceAllocationAuthorization:
        if _is_shadow_identifier(self.authorizer_id):
            raise ValueError(
                "shadow-only authorizer cannot authorize workspace allocation"
            )
        if self.authorization_SHA256 != _allocation_authorization_digest(self):
            raise ValueError("authorization_SHA256 must match authorization digest")
        return self


class WorkspaceInspectionEvidence(_WorkspaceAllocatorModel):
    workspace_root: AbsoluteWorkspacePath
    resolved_workspace_root: AbsoluteWorkspacePath
    git_top_level: AbsoluteWorkspacePath
    source_commit: GitCommitIdentifier
    workspace_branch: WorkspaceBranchIdentifier
    inside_work_tree: Literal[True] = True
    linked_worktree: Literal[True] = True
    clean: StrictBool
    status_entry_count: int = Field(ge=0, strict=True)
    inspection_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evidence(self) -> WorkspaceInspectionEvidence:
        if self.git_top_level != self.resolved_workspace_root:
            raise ValueError("git top level must equal resolved workspace root")
        expected_clean = self.status_entry_count == 0
        if self.clean != expected_clean:
            raise ValueError("clean must match whether status_entry_count is zero")
        if self.inspection_SHA256 != _inspection_evidence_digest(self):
            raise ValueError("inspection_SHA256 must match inspection evidence digest")
        return self


class WorkspaceScopeProjection(_WorkspaceAllocatorModel):
    allowed_paths: tuple[BoundedText, ...] = Field(min_length=1)
    forbidden_paths: tuple[BoundedText, ...] = ()
    allowed_actions: tuple[BoundedText, ...] = Field(min_length=1)
    forbidden_actions: tuple[BoundedText, ...] = ()
    scope_enforcement_ready: Literal[False] = False
    projection_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_projection(self) -> WorkspaceScopeProjection:
        if self.projection_SHA256 != _scope_projection_digest(self):
            raise ValueError("projection_SHA256 must match scope projection digest")
        return self


class WorkspaceReservation(_WorkspaceAllocatorModel):
    allocation_id: WorkspaceAllocationIdentifier
    work_packet_id: str
    work_packet_SHA256: DigestText
    workspace_root: AbsoluteWorkspacePath
    resolved_workspace_root: AbsoluteWorkspacePath
    source_commit: GitCommitIdentifier
    workspace_branch: WorkspaceBranchIdentifier
    lifecycle_state: Literal[WorkspaceLifecycleState.ALLOCATED] = (
        WorkspaceLifecycleState.ALLOCATED
    )
    allocation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_reservation(self) -> WorkspaceReservation:
        if self.allocation_SHA256 != _reservation_digest(self):
            raise ValueError("allocation_SHA256 must match reservation digest")
        return self


class WorkspaceAllocationRegistry(_WorkspaceAllocatorModel):
    schema_version: Literal[1] = WORKSPACE_ALLOCATION_SCHEMA_VERSION
    policy_id: Literal["pepper-human-provisioned-workspace-allocation-v1"] = (
        WORKSPACE_ALLOCATION_POLICY_ID
    )
    revision: int = Field(ge=0, strict=True)
    reservations: tuple[WorkspaceReservation, ...] = ()
    registry_SHA256: DigestText

    @field_validator("reservations", mode="after")
    @classmethod
    def _validate_reservation_order(
        cls, value: tuple[WorkspaceReservation, ...]
    ) -> tuple[WorkspaceReservation, ...]:
        if tuple(sorted(value, key=lambda item: item.allocation_id)) != value:
            raise ValueError("reservations must be ordered by allocation_id")
        return value

    @model_validator(mode="after")
    def _validate_registry(self) -> WorkspaceAllocationRegistry:
        _validate_registry_uniqueness(self, error_type=ValueError)
        if self.registry_SHA256 != _registry_digest(self):
            raise ValueError("registry_SHA256 must match registry digest")
        return self


class WorkspaceAllocationRequest(_WorkspaceAllocatorModel):
    schema_version: Literal[1] = WORKSPACE_ALLOCATION_SCHEMA_VERSION
    policy_id: Literal["pepper-human-provisioned-workspace-allocation-v1"] = (
        WORKSPACE_ALLOCATION_POLICY_ID
    )
    compilation_result: WorkPacketCompilationResult
    repository_identity: WorkspaceRepositoryIdentity
    allocation_authorization: WorkspaceAllocationAuthorization
    registry: WorkspaceAllocationRegistry
    require_clean_worktree: Literal[True] = True
    require_linked_worktree: Literal[True] = True

    @model_validator(mode="after")
    def _validate_request(self) -> WorkspaceAllocationRequest:
        _validate_request_bindings(self, error_type=ValueError)
        return self


class WorkspaceAllocation(_WorkspaceAllocatorModel):
    schema_version: Literal[1] = WORKSPACE_ALLOCATION_SCHEMA_VERSION
    allocation_id: WorkspaceAllocationIdentifier
    policy_id: Literal["pepper-human-provisioned-workspace-allocation-v1"] = (
        WORKSPACE_ALLOCATION_POLICY_ID
    )
    disposition: Literal[WorkspaceAllocationDisposition.ALLOCATED] = (
        WorkspaceAllocationDisposition.ALLOCATED
    )
    lifecycle_state: Literal[WorkspaceLifecycleState.ALLOCATED] = (
        WorkspaceLifecycleState.ALLOCATED
    )
    isolation_level: Literal[WorkspaceIsolationLevel.DEDICATED] = (
        WorkspaceIsolationLevel.DEDICATED
    )
    exclusive: Literal[True] = True
    workspace_requirement_satisfied: Literal[True] = True
    execution_ready: Literal[False] = False
    work_packet_id: str
    work_packet_SHA256: DigestText
    workspace_kind: Literal[WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE] = (
        WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE
    )
    git_authority: Literal[WorkPacketGitAuthority.HUMAN_ONLY] = (
        WorkPacketGitAuthority.HUMAN_ONLY
    )
    workspace_root: AbsoluteWorkspacePath
    resolved_workspace_root: AbsoluteWorkspacePath
    repository_identity: WorkspaceRepositoryIdentity
    inspection_evidence: WorkspaceInspectionEvidence
    scope_projection: WorkspaceScopeProjection
    cleanup_eligibility: Literal[WorkspaceCleanupEligibility.NOT_ELIGIBLE] = (
        WorkspaceCleanupEligibility.NOT_ELIGIBLE
    )
    tool_permissions_ready: Literal[False] = False
    allocation_input_SHA256: DigestText
    allocation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_allocation(self) -> WorkspaceAllocation:
        _validate_allocation_integrity(self, error_type=ValueError)
        return self


class WorkspaceAllocationResult(_WorkspaceAllocatorModel):
    schema_version: Literal[1] = WORKSPACE_ALLOCATION_SCHEMA_VERSION
    disposition: Literal[WorkspaceAllocationDisposition.ALLOCATED] = (
        WorkspaceAllocationDisposition.ALLOCATED
    )
    allocation: WorkspaceAllocation
    updated_registry: WorkspaceAllocationRegistry
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> WorkspaceAllocationResult:
        _validate_result_integrity(self, error_type=ValueError)
        return self


class WorkspaceCleanupAssessment(_WorkspaceAllocatorModel):
    allocation_id: WorkspaceAllocationIdentifier
    execution_active: StrictBool
    unreviewed_changes_present: StrictBool
    artifacts_preserved: StrictBool
    human_git_handoff_complete: StrictBool
    eligibility: WorkspaceCleanupEligibility
    rationale: BoundedText
    assessment_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_assessment(self) -> WorkspaceCleanupAssessment:
        expected = _cleanup_eligibility(
            execution_active=self.execution_active,
            unreviewed_changes_present=self.unreviewed_changes_present,
            artifacts_preserved=self.artifacts_preserved,
            human_git_handoff_complete=self.human_git_handoff_complete,
        )
        if self.eligibility is not expected:
            raise ValueError("eligibility must match cleanup preconditions")
        if self.assessment_SHA256 != _cleanup_assessment_digest(self):
            raise ValueError("assessment_SHA256 must match cleanup assessment digest")
        return self


def build_workspace_repository_identity(
    *,
    repository_id: str,
    source_commit: str,
    workspace_branch: str,
) -> WorkspaceRepositoryIdentity:
    """Build deterministic repository identity for a human-provisioned worktree."""

    data = {
        "repository_id": repository_id,
        "source_commit": source_commit,
        "workspace_branch": workspace_branch,
    }
    try:
        return WorkspaceRepositoryIdentity(
            **data,
            identity_SHA256=_repository_identity_digest_from_record(data),
        )
    except ValueError as exc:
        raise WorkspaceAllocatorInputError("repository identity is invalid") from exc


def build_workspace_allocation_authorization(
    *,
    authorizer_id: str,
    authorization_reference: str,
    rationale: str,
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
    workspace_root: str,
    risk_acknowledgement: str | None = None,
) -> WorkspaceAllocationAuthorization:
    """Build explicit human authorization to reserve one existing workspace."""

    result = _validated_compilation_result(compilation_result)
    identity = _validated_repository_identity(repository_identity)
    _validate_compilation_result_for_allocation(result)
    if _is_shadow_identifier(authorizer_id):
        raise WorkspaceAllocatorAuthorizationError(
            "shadow-only authorizer cannot authorize workspace allocation"
        )
    packet = result.work_packet
    data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "allocation_authorized": True,
        "synthetic": False,
        "authorizer_id": authorizer_id,
        "authorization_reference": authorization_reference,
        "rationale": rationale,
        "risk_acknowledgement": risk_acknowledgement,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "repository_identity_SHA256": identity.identity_SHA256,
        "workspace_root": workspace_root,
        "workspace_kind": WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE,
        "git_authority": WorkPacketGitAuthority.HUMAN_ONLY,
    }
    try:
        return WorkspaceAllocationAuthorization(
            **data,
            authorization_SHA256=_allocation_authorization_digest_from_record(data),
        )
    except ValueError as exc:
        raise WorkspaceAllocatorAuthorizationError(
            "workspace allocation authorization is invalid"
        ) from exc


def get_empty_workspace_allocation_registry() -> WorkspaceAllocationRegistry:
    """Return the deterministic empty in-memory allocation registry."""

    data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "policy_id": WORKSPACE_ALLOCATION_POLICY_ID,
        "revision": 0,
        "reservations": (),
    }
    return WorkspaceAllocationRegistry(
        **data,
        registry_SHA256=_registry_digest_from_record(data),
    )


def validate_workspace_allocation_registry(
    registry: WorkspaceAllocationRegistry,
) -> None:
    """Validate an immutable caller-supplied allocation registry."""

    try:
        validated = WorkspaceAllocationRegistry.model_validate(
            registry.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkspaceAllocatorIntegrityError(
            "workspace allocation registry integrity is invalid"
        ) from exc
    _validate_registry_uniqueness(
        validated,
        error_type=WorkspaceAllocatorCollisionError,
    )
    if validated.registry_SHA256 != _registry_digest(validated):
        raise WorkspaceAllocatorIntegrityError("registry_SHA256 mismatch")


def inspect_human_provisioned_workspace(
    *,
    workspace_root: str,
    repository_identity: WorkspaceRepositoryIdentity,
    require_clean_worktree: bool = True,
    require_linked_worktree: bool = True,
) -> WorkspaceInspectionEvidence:
    """Inspect a supplied workspace using only fixed read-only Git commands."""

    try:
        normalized_root = _validate_absolute_workspace_path(workspace_root.strip())
    except ValueError as exc:
        raise WorkspaceAllocatorInspectionError("workspace root is invalid") from exc
    identity = _validated_repository_identity(repository_identity)
    metadata = _workspace_path_metadata(normalized_root)
    if not metadata.exists:
        raise WorkspaceAllocatorInspectionError("workspace root must exist")
    if not metadata.is_dir:
        raise WorkspaceAllocatorInspectionError("workspace root must be a directory")
    if metadata.is_symlink:
        raise WorkspaceAllocatorInspectionError("workspace root must not be a symlink")
    if metadata.resolved_workspace_root != normalized_root:
        raise WorkspaceAllocatorInspectionError("workspace root must be canonical")

    inside = _run_git_command(normalized_root, ("rev-parse", "--is-inside-work-tree"))
    if inside != "true":
        raise WorkspaceAllocatorInspectionError(
            "workspace root must be inside a work tree"
        )
    git_top_level = _normalize_git_path(
        _run_git_command(normalized_root, ("rev-parse", "--show-toplevel"))
    )
    if git_top_level != metadata.resolved_workspace_root:
        raise WorkspaceAllocatorInspectionError("workspace top level mismatch")
    source_commit = _run_git_command(normalized_root, ("rev-parse", "HEAD"))
    if source_commit != identity.source_commit:
        raise WorkspaceAllocatorInspectionError("workspace source commit mismatch")
    workspace_branch = _run_git_command(normalized_root, ("branch", "--show-current"))
    if not workspace_branch:
        raise WorkspaceAllocatorInspectionError(
            "workspace branch must be a named branch"
        )
    if workspace_branch != identity.workspace_branch:
        raise WorkspaceAllocatorInspectionError("workspace branch mismatch")
    git_dir = _normalize_git_path(
        _run_git_command(normalized_root, ("rev-parse", "--git-dir"))
    )
    git_common_dir = _normalize_git_path(
        _run_git_command(normalized_root, ("rev-parse", "--git-common-dir"))
    )
    linked_worktree = git_dir.casefold() != git_common_dir.casefold()
    if require_linked_worktree and not linked_worktree:
        raise WorkspaceAllocatorInspectionError(
            "workspace must be a human-provisioned linked Git worktree"
        )
    status_output = _run_git_command(
        normalized_root, ("status", "--porcelain=v1", "-uall")
    )
    status_entry_count = _status_entry_count(status_output)
    clean = status_entry_count == 0
    if require_clean_worktree and not clean:
        raise WorkspaceAllocatorInspectionError("workspace worktree must be clean")
    data = {
        "workspace_root": normalized_root,
        "resolved_workspace_root": metadata.resolved_workspace_root,
        "git_top_level": git_top_level,
        "source_commit": source_commit,
        "workspace_branch": workspace_branch,
        "inside_work_tree": True,
        "linked_worktree": linked_worktree,
        "clean": clean,
        "status_entry_count": status_entry_count,
    }
    try:
        return WorkspaceInspectionEvidence(
            **data,
            inspection_SHA256=_inspection_evidence_digest_from_record(data),
        )
    except ValueError as exc:
        raise WorkspaceAllocatorInspectionError(
            "workspace inspection evidence is invalid"
        ) from exc


def allocate_workspace(
    request: WorkspaceAllocationRequest,
) -> WorkspaceAllocationResult:
    """Reserve one clean human-provisioned linked worktree for one WorkPacket."""

    try:
        validated_request = WorkspaceAllocationRequest.model_validate(
            request.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise WorkspaceAllocatorInputError(
            "request must be a WorkspaceAllocationRequest"
        ) from exc
    except ValueError as exc:
        raise WorkspaceAllocatorInputError(
            "workspace allocation request is invalid"
        ) from exc

    result = validated_request.compilation_result
    packet = result.work_packet
    validate_work_packet(packet)
    _validate_compilation_result_for_allocation(result)
    _validated_repository_identity(validated_request.repository_identity)
    _validate_authorization_for_request(validated_request)
    validate_workspace_allocation_registry(validated_request.registry)
    _reject_registry_collisions(
        validated_request.registry,
        work_packet_id=packet.work_packet_id,
        workspace_root=validated_request.allocation_authorization.workspace_root,
        resolved_workspace_root=None,
        workspace_branch=validated_request.repository_identity.workspace_branch,
    )
    inspection = inspect_human_provisioned_workspace(
        workspace_root=validated_request.allocation_authorization.workspace_root,
        repository_identity=validated_request.repository_identity,
        require_clean_worktree=validated_request.require_clean_worktree,
        require_linked_worktree=validated_request.require_linked_worktree,
    )
    _reject_registry_collisions(
        validated_request.registry,
        work_packet_id=packet.work_packet_id,
        workspace_root=inspection.workspace_root,
        resolved_workspace_root=inspection.resolved_workspace_root,
        workspace_branch=inspection.workspace_branch,
    )
    scope_projection = _project_scope(packet)
    allocation_input_sha = _allocation_input_digest(
        compilation_result=result,
        repository_identity=validated_request.repository_identity,
        allocation_authorization=validated_request.allocation_authorization,
        registry=validated_request.registry,
        inspection_evidence=inspection,
        scope_projection=scope_projection,
    )
    allocation_id = _allocation_id(
        ticket_id=packet.ticket_id,
        publication_revision=packet.publication_revision,
        allocation_input_SHA256=allocation_input_sha,
    )
    allocation_data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "allocation_id": allocation_id,
        "policy_id": WORKSPACE_ALLOCATION_POLICY_ID,
        "disposition": WorkspaceAllocationDisposition.ALLOCATED,
        "lifecycle_state": WorkspaceLifecycleState.ALLOCATED,
        "isolation_level": WorkspaceIsolationLevel.DEDICATED,
        "exclusive": True,
        "workspace_requirement_satisfied": True,
        "execution_ready": False,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "workspace_kind": WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE,
        "git_authority": WorkPacketGitAuthority.HUMAN_ONLY,
        "workspace_root": inspection.workspace_root,
        "resolved_workspace_root": inspection.resolved_workspace_root,
        "repository_identity": validated_request.repository_identity,
        "inspection_evidence": inspection,
        "scope_projection": scope_projection,
        "cleanup_eligibility": WorkspaceCleanupEligibility.NOT_ELIGIBLE,
        "tool_permissions_ready": False,
        "allocation_input_SHA256": allocation_input_sha,
    }
    allocation = WorkspaceAllocation(
        **allocation_data,
        allocation_SHA256=_allocation_digest_from_record(allocation_data),
    )
    validate_workspace_allocation(allocation)
    reservation_data = {
        "allocation_id": allocation.allocation_id,
        "work_packet_id": allocation.work_packet_id,
        "work_packet_SHA256": allocation.work_packet_SHA256,
        "workspace_root": allocation.workspace_root,
        "resolved_workspace_root": allocation.resolved_workspace_root,
        "source_commit": allocation.repository_identity.source_commit,
        "workspace_branch": allocation.repository_identity.workspace_branch,
        "lifecycle_state": WorkspaceLifecycleState.ALLOCATED,
    }
    reservation = WorkspaceReservation(
        **reservation_data,
        allocation_SHA256=_reservation_digest_from_record(reservation_data),
    )
    updated_reservations = tuple(
        sorted(
            (*validated_request.registry.reservations, reservation),
            key=lambda item: item.allocation_id,
        )
    )
    registry_data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "policy_id": WORKSPACE_ALLOCATION_POLICY_ID,
        "revision": validated_request.registry.revision + 1,
        "reservations": updated_reservations,
    }
    updated_registry = WorkspaceAllocationRegistry(
        **registry_data,
        registry_SHA256=_registry_digest_from_record(registry_data),
    )
    validate_workspace_allocation_registry(updated_registry)
    result_data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "disposition": WorkspaceAllocationDisposition.ALLOCATED,
        "allocation": allocation,
        "updated_registry": updated_registry,
    }
    try:
        return WorkspaceAllocationResult(
            **result_data,
            result_SHA256=_allocation_result_digest_from_record(result_data),
        )
    except ValueError as exc:
        raise WorkspaceAllocatorIntegrityError(
            "workspace allocation result digest is invalid"
        ) from exc


def validate_workspace_allocation(allocation: WorkspaceAllocation) -> None:
    """Validate a workspace allocation without repair or side effects."""

    try:
        validated = WorkspaceAllocation.model_validate(
            allocation.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkspaceAllocatorIntegrityError(
            "workspace allocation integrity is invalid"
        ) from exc
    _validate_allocation_integrity(
        validated,
        error_type=WorkspaceAllocatorIntegrityError,
    )


def assess_workspace_cleanup_eligibility(
    *,
    allocation: WorkspaceAllocation,
    execution_active: bool,
    unreviewed_changes_present: bool,
    artifacts_preserved: bool,
    human_git_handoff_complete: bool,
) -> WorkspaceCleanupAssessment:
    """Assess cleanup eligibility without deleting files or mutating state."""

    validate_workspace_allocation(allocation)
    eligibility = _cleanup_eligibility(
        execution_active=execution_active,
        unreviewed_changes_present=unreviewed_changes_present,
        artifacts_preserved=artifacts_preserved,
        human_git_handoff_complete=human_git_handoff_complete,
    )
    rationale = (
        "Workspace cleanup is eligible for human-controlled removal."
        if eligibility is WorkspaceCleanupEligibility.ELIGIBLE
        else "Workspace cleanup is not eligible until execution, review, artifact and handoff gates are closed."
    )
    data = {
        "allocation_id": allocation.allocation_id,
        "execution_active": execution_active,
        "unreviewed_changes_present": unreviewed_changes_present,
        "artifacts_preserved": artifacts_preserved,
        "human_git_handoff_complete": human_git_handoff_complete,
        "eligibility": eligibility,
        "rationale": rationale,
    }
    try:
        return WorkspaceCleanupAssessment(
            **data,
            assessment_SHA256=_cleanup_assessment_digest_from_record(data),
        )
    except ValueError as exc:
        raise WorkspaceAllocatorInputError(
            "cleanup assessment inputs are invalid"
        ) from exc


class _WorkspacePathMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    exists: bool
    is_dir: bool
    is_symlink: bool
    resolved_workspace_root: str


def _workspace_path_metadata(workspace_root: str) -> _WorkspacePathMetadata:
    path = Path(workspace_root)
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise WorkspaceAllocatorInspectionError(
            "workspace root cannot be resolved"
        ) from exc
    return _WorkspacePathMetadata(
        exists=path.exists(),
        is_dir=path.is_dir(),
        is_symlink=path.is_symlink(),
        resolved_workspace_root=_public_path(resolved),
    )


def _run_git_command(workspace_root: str, args: tuple[str, ...]) -> str:
    allowed = {
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "HEAD"),
        ("branch", "--show-current"),
        ("rev-parse", "--is-inside-work-tree"),
        ("rev-parse", "--git-dir"),
        ("rev-parse", "--git-common-dir"),
        ("status", "--porcelain=v1", "-uall"),
    }
    if args not in allowed:
        raise WorkspaceAllocatorInspectionError("Git inspection command is not allowed")
    command = ["git", "--no-optional-locks", "-C", workspace_root, *args]
    try:
        completed = subprocess.run(
            command,
            shell=False,
            timeout=_READ_ONLY_GIT_TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise WorkspaceAllocatorInspectionError(
            "Git inspection command failed"
        ) from exc
    if completed.returncode != 0:
        operation = " ".join(args)
        raise WorkspaceAllocatorInspectionError(
            f"Git read-only inspection failed: {operation}"
        )
    return completed.stdout.strip()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _dump_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, tuple | list):
        return [_dump_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    return value


def _digest(algorithm: str, record: dict[str, object]) -> str:
    prepared = {key: _dump_value(value) for key, value in record.items()}
    return _sha256_text(_deterministic_json({"algorithm": algorithm, **prepared}))


def _repository_identity_digest(identity: WorkspaceRepositoryIdentity) -> str:
    return _repository_identity_digest_from_record(
        identity.model_dump(mode="json", exclude={"identity_SHA256"})
    )


def _repository_identity_digest_from_record(record: dict[str, object]) -> str:
    return _digest(REPOSITORY_IDENTITY_DIGEST_ALGORITHM, record)


def _allocation_authorization_digest(
    authorization: WorkspaceAllocationAuthorization,
) -> str:
    return _allocation_authorization_digest_from_record(
        authorization.model_dump(mode="json", exclude={"authorization_SHA256"})
    )


def _allocation_authorization_digest_from_record(record: dict[str, object]) -> str:
    return _digest(ALLOCATION_AUTHORIZATION_DIGEST_ALGORITHM, record)


def _inspection_evidence_digest(evidence: WorkspaceInspectionEvidence) -> str:
    return _inspection_evidence_digest_from_record(
        evidence.model_dump(mode="json", exclude={"inspection_SHA256"})
    )


def _inspection_evidence_digest_from_record(record: dict[str, object]) -> str:
    return _digest(INSPECTION_EVIDENCE_DIGEST_ALGORITHM, record)


def _scope_projection_digest(projection: WorkspaceScopeProjection) -> str:
    return _scope_projection_digest_from_record(
        projection.model_dump(mode="json", exclude={"projection_SHA256"})
    )


def _scope_projection_digest_from_record(record: dict[str, object]) -> str:
    return _digest(SCOPE_PROJECTION_DIGEST_ALGORITHM, record)


def _reservation_digest(reservation: WorkspaceReservation) -> str:
    return _reservation_digest_from_record(
        reservation.model_dump(mode="json", exclude={"allocation_SHA256"})
    )


def _reservation_digest_from_record(record: dict[str, object]) -> str:
    return _digest(RESERVATION_DIGEST_ALGORITHM, record)


def _registry_digest(registry: WorkspaceAllocationRegistry) -> str:
    return _registry_digest_from_record(
        registry.model_dump(mode="json", exclude={"registry_SHA256"})
    )


def _registry_digest_from_record(record: dict[str, object]) -> str:
    return _digest(REGISTRY_DIGEST_ALGORITHM, record)


def _allocation_digest(allocation: WorkspaceAllocation) -> str:
    return _allocation_digest_from_record(
        allocation.model_dump(mode="json", exclude={"allocation_SHA256"})
    )


def _allocation_digest_from_record(record: dict[str, object]) -> str:
    return _digest(ALLOCATION_DIGEST_ALGORITHM, record)


def _allocation_result_digest(result: WorkspaceAllocationResult) -> str:
    return _allocation_result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _allocation_result_digest_from_record(record: dict[str, object]) -> str:
    return _digest(ALLOCATION_RESULT_DIGEST_ALGORITHM, record)


def _cleanup_assessment_digest(assessment: WorkspaceCleanupAssessment) -> str:
    return _cleanup_assessment_digest_from_record(
        assessment.model_dump(mode="json", exclude={"assessment_SHA256"})
    )


def _cleanup_assessment_digest_from_record(record: dict[str, object]) -> str:
    return _digest(CLEANUP_ASSESSMENT_DIGEST_ALGORITHM, record)


def _allocation_input_digest(
    *,
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
    allocation_authorization: WorkspaceAllocationAuthorization,
    registry: WorkspaceAllocationRegistry,
    inspection_evidence: WorkspaceInspectionEvidence,
    scope_projection: WorkspaceScopeProjection,
) -> str:
    return _digest(
        ALLOCATION_INPUT_DIGEST_ALGORITHM,
        {
            "policy_id": WORKSPACE_ALLOCATION_POLICY_ID,
            "work_packet_id": compilation_result.work_packet.work_packet_id,
            "work_packet_SHA256": compilation_result.work_packet.work_packet_SHA256,
            "compilation_result_SHA256": compilation_result.result_SHA256,
            "repository_identity_SHA256": repository_identity.identity_SHA256,
            "allocation_authorization_SHA256": (
                allocation_authorization.authorization_SHA256
            ),
            "registry_SHA256": registry.registry_SHA256,
            "inspection_SHA256": inspection_evidence.inspection_SHA256,
            "scope_projection_SHA256": scope_projection.projection_SHA256,
        },
    )


def _allocation_id(
    *, ticket_id: str, publication_revision: int, allocation_input_SHA256: str
) -> str:
    normalized_ticket = ticket_id.replace(".", "-")
    return f"WS-{normalized_ticket}-R{publication_revision:04d}-{allocation_input_SHA256[:12]}"


def _public_path(path: Path) -> str:
    return path.as_posix()


def _normalize_git_path(value: str) -> str:
    return value.replace("\\", "/").rstrip("/") if value not in {"/"} else value


def _status_entry_count(status_output: str) -> int:
    if not status_output:
        return 0
    return len(tuple(line for line in status_output.splitlines() if line.strip()))


def _is_shadow_identifier(value: str) -> bool:
    return value.upper().startswith("SHADOW-") or value.casefold().startswith("shadow-")


def _validated_repository_identity(
    repository_identity: WorkspaceRepositoryIdentity,
) -> WorkspaceRepositoryIdentity:
    try:
        return WorkspaceRepositoryIdentity.model_validate(
            repository_identity.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkspaceAllocatorIntegrityError(
            "repository identity digest is invalid"
        ) from exc


def _validated_compilation_result(
    compilation_result: WorkPacketCompilationResult,
) -> WorkPacketCompilationResult:
    try:
        return WorkPacketCompilationResult.model_validate(
            compilation_result.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkspaceAllocatorIntegrityError(
            "WorkPacket compilation result is invalid"
        ) from exc


def _validate_compilation_result_for_allocation(
    compilation_result: WorkPacketCompilationResult,
) -> None:
    if compilation_result.disposition is not WorkPacketCompilationDisposition.COMPILED:
        raise WorkspaceAllocatorInputError(
            "WorkPacket compilation result must be compiled"
        )
    packet = compilation_result.work_packet
    validate_work_packet(packet)
    if packet.authority_boundary is not WorkPacketAuthorityBoundary.COMPILE_ONLY:
        raise WorkspaceAllocatorInputError("WorkPacket authority must be compile-only")
    if packet.execution_ready is not False:
        raise WorkspaceAllocatorInputError("WorkPacket must not be execution-ready")
    if packet.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise WorkspaceAllocatorInputError(
            "WorkPacket Git authority must be human-only"
        )
    requirement = next(
        (
            item
            for item in packet.downstream_requirements
            if item.capability is WorkPacketDownstreamCapability.WORKSPACE_ALLOCATION
        ),
        None,
    )
    if requirement is None:
        raise WorkspaceAllocatorInputError(
            "workspace-allocation requirement is missing"
        )
    if requirement.satisfied_by_compiler is not False:
        raise WorkspaceAllocatorInputError(
            "workspace-allocation requirement must remain unsatisfied"
        )


def _validate_request_bindings(
    request: WorkspaceAllocationRequest, *, error_type: type[Exception]
) -> None:
    packet = request.compilation_result.work_packet
    authorization = request.allocation_authorization
    if authorization.work_packet_id != packet.work_packet_id:
        raise error_type("authorization WorkPacket ID must match request")
    if authorization.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("authorization WorkPacket digest must match request")
    if (
        authorization.repository_identity_SHA256
        != request.repository_identity.identity_SHA256
    ):
        raise error_type("authorization repository identity must match request")
    if authorization.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("authorization Git authority must be human-only")


def _validate_authorization_for_request(request: WorkspaceAllocationRequest) -> None:
    try:
        authorization = WorkspaceAllocationAuthorization.model_validate(
            request.allocation_authorization.model_dump(mode="json")
        )
    except ValueError as exc:
        raise WorkspaceAllocatorAuthorizationError(
            "workspace allocation authorization digest is invalid"
        ) from exc
    if authorization != request.allocation_authorization:
        raise WorkspaceAllocatorAuthorizationError(
            "authorization validation changed input"
        )
    _validate_request_bindings(
        request,
        error_type=WorkspaceAllocatorAuthorizationError,
    )


def _project_scope(packet: WorkPacket) -> WorkspaceScopeProjection:
    scope = packet.repository_scope
    data = {
        "allowed_paths": scope.allowed_paths,
        "forbidden_paths": scope.forbidden_paths,
        "allowed_actions": scope.allowed_actions,
        "forbidden_actions": scope.forbidden_actions,
        "scope_enforcement_ready": False,
    }
    return WorkspaceScopeProjection(
        **data,
        projection_SHA256=_scope_projection_digest_from_record(data),
    )


def _validate_allocation_integrity(
    allocation: WorkspaceAllocation,
    *,
    error_type: type[Exception],
) -> None:
    if allocation.policy_id != WORKSPACE_ALLOCATION_POLICY_ID:
        raise error_type("allocation policy ID mismatch")
    if allocation.disposition is not WorkspaceAllocationDisposition.ALLOCATED:
        raise error_type("allocation disposition mismatch")
    if allocation.lifecycle_state is not WorkspaceLifecycleState.ALLOCATED:
        raise error_type("allocation lifecycle mismatch")
    if allocation.isolation_level is not WorkspaceIsolationLevel.DEDICATED:
        raise error_type("allocation isolation mismatch")
    if allocation.exclusive is not True:
        raise error_type("allocation must be exclusive")
    if allocation.workspace_requirement_satisfied is not True:
        raise error_type("workspace requirement must be satisfied")
    if allocation.execution_ready is not False:
        raise error_type("allocation must not be execution-ready")
    if allocation.tool_permissions_ready is not False:
        raise error_type("tool permissions must not be ready")
    if allocation.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("Git authority must be human-only")
    identity = allocation.repository_identity
    inspection = allocation.inspection_evidence
    if identity.identity_SHA256 != _repository_identity_digest(identity):
        raise error_type("repository identity digest mismatch")
    if inspection.inspection_SHA256 != _inspection_evidence_digest(inspection):
        raise error_type("inspection evidence digest mismatch")
    if allocation.workspace_root != inspection.workspace_root:
        raise error_type("inspection workspace root mismatch")
    if allocation.resolved_workspace_root != inspection.resolved_workspace_root:
        raise error_type("inspection resolved root mismatch")
    if inspection.source_commit != identity.source_commit:
        raise error_type("inspection source commit mismatch")
    if inspection.workspace_branch != identity.workspace_branch:
        raise error_type("inspection branch mismatch")
    if inspection.linked_worktree is not True:
        raise error_type("inspection must prove linked worktree")
    if inspection.clean is not True or inspection.status_entry_count != 0:
        raise error_type("inspection must prove clean worktree")
    if allocation.scope_projection.projection_SHA256 != _scope_projection_digest(
        allocation.scope_projection
    ):
        raise error_type("scope projection digest mismatch")
    if allocation.cleanup_eligibility is not WorkspaceCleanupEligibility.NOT_ELIGIBLE:
        raise error_type("cleanup eligibility must be not eligible")
    if allocation.allocation_id != _allocation_id(
        ticket_id=_ticket_id_from_work_packet_id(allocation.work_packet_id),
        publication_revision=_revision_from_work_packet_id(allocation.work_packet_id),
        allocation_input_SHA256=allocation.allocation_input_SHA256,
    ):
        raise error_type("allocation ID mismatch")
    if allocation.allocation_SHA256 != _allocation_digest(allocation):
        raise error_type("allocation_SHA256 mismatch")


def _validate_result_integrity(
    result: WorkspaceAllocationResult,
    *,
    error_type: type[Exception],
) -> None:
    allocation = result.allocation
    if result.disposition is not WorkspaceAllocationDisposition.ALLOCATED:
        raise error_type("allocation result disposition mismatch")
    _validate_allocation_integrity(allocation, error_type=error_type)
    reservation = next(
        (
            item
            for item in result.updated_registry.reservations
            if item.allocation_id == allocation.allocation_id
        ),
        None,
    )
    if reservation is None:
        raise error_type("updated registry missing allocation reservation")
    if reservation.work_packet_id != allocation.work_packet_id:
        raise error_type("reservation WorkPacket mismatch")
    if result.result_SHA256 != _allocation_result_digest(result):
        raise error_type("result_SHA256 mismatch")


def _ticket_id_from_work_packet_id(work_packet_id: str) -> str:
    body = work_packet_id.removeprefix("WP-")
    ticket, _revision, _digest = body.rsplit("-", 2)
    return ticket.replace("-", ".", 1)


def _revision_from_work_packet_id(work_packet_id: str) -> int:
    match = re.search(r"-R([0-9]{4})-", work_packet_id)
    if match is None:
        raise WorkspaceAllocatorIntegrityError("WorkPacket ID revision is invalid")
    return int(match.group(1))


def _registry_path_key(value: str) -> str:
    return value.rstrip("/").casefold()


def _paths_overlap(first: str, second: str) -> bool:
    left = _registry_path_key(first)
    right = _registry_path_key(second)
    return left == right or left.startswith(f"{right}/") or right.startswith(f"{left}/")


def _validate_registry_uniqueness(
    registry: WorkspaceAllocationRegistry,
    *,
    error_type: type[Exception],
) -> None:
    seen_allocation_ids: set[str] = set()
    seen_work_packet_ids: set[str] = set()
    seen_workspace_roots: set[str] = set()
    seen_resolved_roots: set[str] = set()
    seen_branches: set[str] = set()
    roots: list[str] = []
    for reservation in registry.reservations:
        if reservation.allocation_id in seen_allocation_ids:
            raise error_type("duplicate allocation ID")
        seen_allocation_ids.add(reservation.allocation_id)
        if reservation.work_packet_id in seen_work_packet_ids:
            raise error_type("duplicate WorkPacket ID")
        seen_work_packet_ids.add(reservation.work_packet_id)
        root_key = _registry_path_key(reservation.workspace_root)
        if root_key in seen_workspace_roots:
            raise error_type("duplicate workspace root")
        seen_workspace_roots.add(root_key)
        resolved_key = _registry_path_key(reservation.resolved_workspace_root)
        if resolved_key in seen_resolved_roots:
            raise error_type("duplicate resolved workspace root")
        seen_resolved_roots.add(resolved_key)
        branch_key = reservation.workspace_branch.casefold()
        if branch_key in seen_branches:
            raise error_type("duplicate workspace branch")
        seen_branches.add(branch_key)
        for root in roots:
            if _paths_overlap(root, reservation.resolved_workspace_root):
                raise error_type("workspace root overlap")
        roots.append(reservation.resolved_workspace_root)


def _reject_registry_collisions(
    registry: WorkspaceAllocationRegistry,
    *,
    work_packet_id: str,
    workspace_root: str,
    resolved_workspace_root: str | None,
    workspace_branch: str,
) -> None:
    for reservation in registry.reservations:
        if reservation.work_packet_id == work_packet_id:
            raise WorkspaceAllocatorCollisionError("duplicate WorkPacket allocation")
        if _paths_overlap(reservation.workspace_root, workspace_root):
            raise WorkspaceAllocatorCollisionError("workspace root collision")
        if resolved_workspace_root is not None and _paths_overlap(
            reservation.resolved_workspace_root,
            resolved_workspace_root,
        ):
            raise WorkspaceAllocatorCollisionError("resolved workspace root collision")
        if reservation.workspace_branch.casefold() == workspace_branch.casefold():
            raise WorkspaceAllocatorCollisionError("workspace branch collision")


def _cleanup_eligibility(
    *,
    execution_active: bool,
    unreviewed_changes_present: bool,
    artifacts_preserved: bool,
    human_git_handoff_complete: bool,
) -> WorkspaceCleanupEligibility:
    if (
        not execution_active
        and not unreviewed_changes_present
        and artifacts_preserved
        and human_git_handoff_complete
    ):
        return WorkspaceCleanupEligibility.ELIGIBLE
    return WorkspaceCleanupEligibility.NOT_ELIGIBLE
