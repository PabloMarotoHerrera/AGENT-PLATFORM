"""Deny-first tool permission profiles for Agent Platform P17.2.

The profile builder binds explicit human-selected filesystem grants to one
compile-only WorkPacket and one verified workspace allocation. The evaluator is
pure policy logic: it never invokes tools, touches the filesystem, runs Git or
executes commands.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
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
    WorkPacketCompilationDisposition,
    WorkPacketCompilationResult,
    WorkPacketDownstreamCapability,
    WorkPacketGitAuthority,
    validate_work_packet,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocation,
    WorkspaceAllocationDisposition,
    WorkspaceAllocationResult,
    WorkspaceLifecycleState,
    validate_workspace_allocation,
)

TOOL_PERMISSION_SCHEMA_VERSION = 1
TOOL_PERMISSION_POLICY_ID = "pepper-deny-first-tool-permission-policy-v1"

PROFILE_AUTHORIZATION_DIGEST_ALGORITHM = (
    "agent-platform-tool-permission-profile-authorization-sha256-v1"
)
GRANT_DIGEST_ALGORITHM = "agent-platform-tool-permission-grant-sha256-v1"
PROFILE_INPUT_DIGEST_ALGORITHM = (
    "agent-platform-tool-permission-profile-input-sha256-v1"
)
PROFILE_DIGEST_ALGORITHM = "agent-platform-tool-permission-profile-sha256-v1"
PROFILE_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-tool-permission-profile-result-sha256-v1"
)
DECISION_INPUT_DIGEST_ALGORITHM = (
    "agent-platform-tool-permission-decision-input-sha256-v1"
)
DECISION_DIGEST_ALGORITHM = "agent-platform-tool-permission-decision-sha256-v1"

_PROFILE_ID_PATTERN = r"^TP-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-R[0-9]{4}-[a-f0-9]{12}$"
_HUMAN_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{2,95}$"
_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_DRIVE_ABSOLUTE_PATTERN = re.compile(r"^[A-Za-z]:/")
_DRIVE_ROOT_PATTERN = re.compile(r"^[A-Za-z]:/$")
_DRIVE_RELATIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
_UNSUPPORTED_SCOPE_MARKERS = ("*", "?", "[")

_PROTECTED_PATHS = (
    ".git/**",
    ".opencode/**",
    ".agents/**",
    "AGENTS.md",
    "graphify-out/**",
    "4_external/sources/**",
    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
)


class ToolPermissionProfileError(ValueError):
    """Base error for P17.2 tool permission profile failures."""


class ToolPermissionProfileInputError(ToolPermissionProfileError):
    """Raised when profile inputs or bindings are structurally invalid."""


class ToolPermissionProfileAuthorizationError(ToolPermissionProfileError):
    """Raised when human profile authorization is absent or invalid."""


class ToolPermissionProfileIntegrityError(ToolPermissionProfileError):
    """Raised when deterministic profile or decision evidence is invalid."""


class ToolPermissionEvaluationError(ToolPermissionProfileError):
    """Raised when permission evaluation bindings are structurally invalid."""


class ToolPermissionOperation(str, Enum):
    LIST_DIRECTORY = "list_directory"
    READ_FILE = "read_file"
    CREATE_FILE = "create_file"
    REPLACE_FILE = "replace_file"
    DELETE_FILE = "delete_file"
    CREATE_DIRECTORY = "create_directory"
    DELETE_DIRECTORY = "delete_directory"
    EXECUTE_COMMAND = "execute_command"
    VALIDATION_COMMAND = "validation_command"
    GIT_READ_ONLY = "git_read_only"
    GIT_MUTATION = "git_mutation"
    NETWORK_ACCESS = "network_access"
    WORKSPACE_MUTATION = "workspace_mutation"
    PROVIDER_CALL = "provider_call"
    MODEL_CALL = "model_call"
    AGENT_CONTROL = "agent_control"
    WORKER_CONTROL = "worker_control"


class ToolPermissionProfileState(str, Enum):
    ISSUED = "issued"


class ToolPermissionProfileDisposition(str, Enum):
    ISSUED = "issued"


class ToolPermissionDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class ToolPermissionDecisionReason(str, Enum):
    ALLOWED_BY_EXPLICIT_GRANT = "allowed_by_explicit_grant"
    OPERATION_NOT_GRANTED = "operation_not_granted"
    OPERATION_EXPLICITLY_DENIED = "operation_explicitly_denied"
    TARGET_PATH_INVALID = "target_path_invalid"
    TARGET_OUTSIDE_WORKSPACE = "target_outside_workspace"
    TARGET_IN_PROTECTED_ROOT = "target_in_protected_root"
    TARGET_IN_FORBIDDEN_SCOPE = "target_in_forbidden_scope"
    TARGET_NOT_IN_ALLOWED_SCOPE = "target_not_in_allowed_scope"


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
_NEVER_GRANTABLE_OPERATIONS = tuple(
    operation
    for operation in ToolPermissionOperation
    if operation not in _GRANTABLE_OPERATIONS
)
_OPERATION_ORDER = tuple(ToolPermissionOperation)


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
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
        raise ValueError("workspace path must not contain NUL characters")
    if "\\" in value:
        raise ValueError("workspace path must use forward slashes")
    if not (value.startswith("/") or _DRIVE_ABSOLUTE_PATTERN.match(value)):
        raise ValueError("workspace path must be absolute")
    if value.endswith("/") and not _workspace_root_is_filesystem_root(value):
        raise ValueError("workspace path must not have a trailing separator")
    if any(part in {"", ".", ".."} for part in _workspace_path_parts(value)):
        raise ValueError("workspace path must not contain traversal components")
    return value


def _validate_repository_path_pattern(value: str) -> str:
    if "\x00" in value:
        raise ValueError("repository path must not contain NUL characters")
    if not value:
        raise ValueError("repository path must not be empty")
    if value.startswith("/") or _DRIVE_RELATIVE_PATTERN.match(value):
        raise ValueError("repository path must be relative")
    if "\\" in value:
        raise ValueError("repository path must use forward slashes")
    base = value[:-3] if value.endswith("/**") else value
    if not base or base.endswith("/"):
        raise ValueError("repository path pattern base is invalid")
    if any(marker in base for marker in _UNSUPPORTED_SCOPE_MARKERS):
        raise ValueError("repository path pattern uses unsupported wildcard grammar")
    if any(component in {"", ".", ".."} for component in base.split("/")):
        raise ValueError("repository path must not contain traversal components")
    if "**" in base or ("*" in value and not value.endswith("/**")):
        raise ValueError("repository path pattern uses unsupported wildcard grammar")
    return value


def _validate_grantable_operation(
    value: ToolPermissionOperation,
) -> ToolPermissionOperation:
    if value not in _GRANTABLE_OPERATIONS:
        raise ValueError("operation is not grantable in P17.2")
    return value


ToolPermissionProfileIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=24, max_length=96, pattern=_PROFILE_ID_PATTERN),
]
HumanToolPermissionAuthorizerIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=3, max_length=96, pattern=_HUMAN_ID_PATTERN),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
RepositoryRelativePath: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_repository_path_pattern),
]
AbsoluteWorkspacePath: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=512),
    AfterValidator(_validate_absolute_workspace_path),
]
TargetPathText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=0, max_length=512),
]


class _ToolPermissionModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


class ToolPermissionGrantRequest(_ToolPermissionModel):
    operation: ToolPermissionOperation
    source_allowed_action: BoundedText
    rationale: BoundedText

    @model_validator(mode="after")
    def _validate_request(self) -> ToolPermissionGrantRequest:
        _validate_grantable_operation(self.operation)
        return self


class ToolPermissionProfileAuthorization(_ToolPermissionModel):
    schema_version: Literal[1] = TOOL_PERMISSION_SCHEMA_VERSION
    profile_authorized: Literal[True] = True
    synthetic: Literal[False] = False
    authorizer_id: HumanToolPermissionAuthorizerIdentifier
    authorization_reference: BoundedText
    rationale: BoundedText
    risk_acknowledgement: BoundedText | None = None
    work_packet_id: str
    work_packet_SHA256: DigestText
    allocation_id: str
    allocation_SHA256: DigestText
    grant_requests: tuple[ToolPermissionGrantRequest, ...] = Field(min_length=1)
    authorization_SHA256: DigestText

    @field_validator("grant_requests", mode="after")
    @classmethod
    def _validate_grant_requests(
        cls, value: tuple[ToolPermissionGrantRequest, ...]
    ) -> tuple[ToolPermissionGrantRequest, ...]:
        operations = tuple(request.operation for request in value)
        if len(operations) != len(frozenset(operations)):
            raise ValueError("grant requests must not contain duplicate operations")
        if operations != _sort_operations(operations):
            raise ValueError("grant requests must be ordered by operation taxonomy")
        return value

    @model_validator(mode="after")
    def _validate_authorization(self) -> ToolPermissionProfileAuthorization:
        if _is_shadow_identifier(self.authorizer_id):
            raise ValueError("shadow-only authorizer cannot authorize tool permissions")
        if _requires_risk_acknowledgement(self.grant_requests):
            if self.risk_acknowledgement is None:
                raise ValueError("mutating grants require risk acknowledgement")
        if self.authorization_SHA256 != _profile_authorization_digest(self):
            raise ValueError("authorization_SHA256 must match authorization digest")
        return self


class ToolPermissionGrant(_ToolPermissionModel):
    operation: ToolPermissionOperation
    allowed_paths: tuple[RepositoryRelativePath, ...] = Field(min_length=1)
    forbidden_paths: tuple[RepositoryRelativePath, ...] = ()
    source_allowed_action: BoundedText
    rationale: BoundedText
    grant_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_grant(self) -> ToolPermissionGrant:
        _validate_grantable_operation(self.operation)
        if self.grant_SHA256 != _grant_digest(self):
            raise ValueError("grant_SHA256 must match grant digest")
        return self


class ToolPermissionProfileRequest(_ToolPermissionModel):
    schema_version: Literal[1] = TOOL_PERMISSION_SCHEMA_VERSION
    policy_id: Literal["pepper-deny-first-tool-permission-policy-v1"] = (
        TOOL_PERMISSION_POLICY_ID
    )
    compilation_result: WorkPacketCompilationResult
    allocation_result: WorkspaceAllocationResult
    profile_authorization: ToolPermissionProfileAuthorization

    @model_validator(mode="after")
    def _validate_request(self) -> ToolPermissionProfileRequest:
        _validate_profile_request_bindings(self, error_type=ValueError)
        return self


class ToolPermissionProfile(_ToolPermissionModel):
    schema_version: Literal[1] = TOOL_PERMISSION_SCHEMA_VERSION
    profile_id: ToolPermissionProfileIdentifier
    policy_id: Literal["pepper-deny-first-tool-permission-policy-v1"] = (
        TOOL_PERMISSION_POLICY_ID
    )
    state: Literal[ToolPermissionProfileState.ISSUED] = (
        ToolPermissionProfileState.ISSUED
    )
    tool_permissions_ready: Literal[True] = True
    execution_ready: Literal[False] = False
    work_packet_id: str
    work_packet_SHA256: DigestText
    allocation_id: str
    allocation_SHA256: DigestText
    workspace_root: AbsoluteWorkspacePath
    resolved_workspace_root: AbsoluteWorkspacePath
    git_authority: Literal[WorkPacketGitAuthority.HUMAN_ONLY] = (
        WorkPacketGitAuthority.HUMAN_ONLY
    )
    grants: tuple[ToolPermissionGrant, ...] = Field(min_length=1)
    denied_operations: tuple[ToolPermissionOperation, ...]
    protected_paths: tuple[RepositoryRelativePath, ...]
    scope_projection_SHA256: DigestText
    authorization_SHA256: DigestText
    profile_input_SHA256: DigestText
    profile_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_profile(self) -> ToolPermissionProfile:
        _validate_profile_integrity(self, error_type=ValueError)
        return self


class ToolPermissionProfileResult(_ToolPermissionModel):
    schema_version: Literal[1] = TOOL_PERMISSION_SCHEMA_VERSION
    disposition: Literal[ToolPermissionProfileDisposition.ISSUED] = (
        ToolPermissionProfileDisposition.ISSUED
    )
    profile: ToolPermissionProfile
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ToolPermissionProfileResult:
        if self.profile.tool_permissions_ready is not True:
            raise ValueError("profile must be tool-permissions ready")
        if self.profile.execution_ready is not False:
            raise ValueError("profile must not be execution-ready")
        if self.result_SHA256 != _profile_result_digest(self):
            raise ValueError("result_SHA256 must match result digest")
        return self


class ToolPermissionCheckRequest(_ToolPermissionModel):
    schema_version: Literal[1] = TOOL_PERMISSION_SCHEMA_VERSION
    policy_id: Literal["pepper-deny-first-tool-permission-policy-v1"] = (
        TOOL_PERMISSION_POLICY_ID
    )
    profile: ToolPermissionProfile
    allocation: WorkspaceAllocation
    operation: ToolPermissionOperation
    workspace_relative_path: TargetPathText
    resolved_target_path: TargetPathText
    target_resolution_verified: Literal[True] = True
    request_reference: BoundedText

    @model_validator(mode="after")
    def _validate_request(self) -> ToolPermissionCheckRequest:
        _validate_profile_allocation_binding(
            profile=self.profile,
            allocation=self.allocation,
            error_type=ValueError,
        )
        return self


class ToolPermissionDecisionEvidence(_ToolPermissionModel):
    schema_version: Literal[1] = TOOL_PERMISSION_SCHEMA_VERSION
    decision: ToolPermissionDecision
    reason: ToolPermissionDecisionReason
    operation: ToolPermissionOperation
    work_packet_id: str
    allocation_id: str
    profile_id: ToolPermissionProfileIdentifier
    workspace_relative_path: TargetPathText
    resolved_target_path: TargetPathText
    matched_allowed_pattern: RepositoryRelativePath | None = None
    matched_forbidden_pattern: RepositoryRelativePath | None = None
    profile_SHA256: DigestText
    decision_input_SHA256: DigestText
    decision_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_decision(self) -> ToolPermissionDecisionEvidence:
        _validate_decision_integrity(self, error_type=ValueError)
        return self


def build_tool_permission_profile_authorization(
    *,
    authorizer_id: str,
    authorization_reference: str,
    rationale: str,
    compilation_result: WorkPacketCompilationResult,
    allocation_result: WorkspaceAllocationResult,
    grant_requests: tuple[ToolPermissionGrantRequest, ...],
    risk_acknowledgement: str | None = None,
) -> ToolPermissionProfileAuthorization:
    """Build explicit human authorization for one deny-first profile."""

    result = _validated_compilation_result(compilation_result)
    allocation_result = _validated_allocation_result(allocation_result)
    packet = result.work_packet
    allocation = allocation_result.allocation
    _validate_compilation_result_for_profile(
        result, error_type=ToolPermissionProfileInputError
    )
    _validate_allocation_for_profile(
        allocation, error_type=ToolPermissionProfileInputError
    )
    _validate_work_packet_allocation_binding(
        packet=packet,
        allocation=allocation,
        error_type=ToolPermissionProfileInputError,
    )
    requests = _validated_grant_requests(
        grant_requests=grant_requests,
        packet=packet,
        error_type=ToolPermissionProfileAuthorizationError,
    )
    if _is_shadow_identifier(authorizer_id):
        raise ToolPermissionProfileAuthorizationError(
            "shadow-only authorizer cannot authorize tool permissions"
        )
    if _requires_risk_acknowledgement(requests) and risk_acknowledgement is None:
        raise ToolPermissionProfileAuthorizationError(
            "mutating grants require risk acknowledgement"
        )
    data = {
        "schema_version": TOOL_PERMISSION_SCHEMA_VERSION,
        "profile_authorized": True,
        "synthetic": False,
        "authorizer_id": authorizer_id,
        "authorization_reference": authorization_reference,
        "rationale": rationale,
        "risk_acknowledgement": risk_acknowledgement,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "grant_requests": requests,
    }
    try:
        return ToolPermissionProfileAuthorization(
            **data,
            authorization_SHA256=_profile_authorization_digest_from_record(data),
        )
    except ValueError as exc:
        raise ToolPermissionProfileAuthorizationError(
            "tool permission profile authorization is invalid"
        ) from exc


def build_tool_permission_profile(
    request: ToolPermissionProfileRequest,
) -> ToolPermissionProfileResult:
    """Build a deterministic deny-first profile without invoking any tool."""

    try:
        validated_request = ToolPermissionProfileRequest.model_validate(
            request.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise ToolPermissionProfileInputError(
            "request must be a ToolPermissionProfileRequest"
        ) from exc
    except ValueError as exc:
        raise ToolPermissionProfileInputError(
            "tool permission profile request is invalid"
        ) from exc

    _validate_profile_request_bindings(
        validated_request,
        error_type=ToolPermissionProfileInputError,
    )
    result = validated_request.compilation_result
    allocation_result = validated_request.allocation_result
    authorization = validated_request.profile_authorization
    packet = result.work_packet
    allocation = allocation_result.allocation

    try:
        _validate_scope_pattern_grammar(packet.repository_scope.allowed_paths)
        _validate_scope_pattern_grammar(packet.repository_scope.forbidden_paths)
    except ValueError as exc:
        raise ToolPermissionProfileInputError(
            "WorkPacket scope uses unsupported path pattern grammar"
        ) from exc
    _validate_scope_projection_matches_packet(
        packet=packet,
        allocation=allocation,
        error_type=ToolPermissionProfileInputError,
    )

    grants = tuple(
        _build_grant(
            request=grant_request,
            allowed_paths=allocation.scope_projection.allowed_paths,
            forbidden_paths=allocation.scope_projection.forbidden_paths,
        )
        for grant_request in authorization.grant_requests
    )
    granted_operations = tuple(grant.operation for grant in grants)
    denied_operations = tuple(
        operation
        for operation in _OPERATION_ORDER
        if operation not in granted_operations
    )
    profile_input_data = {
        "schema_version": TOOL_PERMISSION_SCHEMA_VERSION,
        "policy_id": TOOL_PERMISSION_POLICY_ID,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "workspace_root": allocation.workspace_root,
        "resolved_workspace_root": allocation.resolved_workspace_root,
        "git_authority": WorkPacketGitAuthority.HUMAN_ONLY,
        "grants": grants,
        "denied_operations": denied_operations,
        "protected_paths": _PROTECTED_PATHS,
        "scope_projection_SHA256": allocation.scope_projection.projection_SHA256,
        "authorization_SHA256": authorization.authorization_SHA256,
    }
    profile_input_sha = _profile_input_digest_from_record(profile_input_data)
    profile_data = {
        **profile_input_data,
        "profile_id": _profile_id(
            ticket_id=packet.ticket_id,
            publication_revision=packet.publication_revision,
            profile_input_SHA256=profile_input_sha,
        ),
        "state": ToolPermissionProfileState.ISSUED,
        "tool_permissions_ready": True,
        "execution_ready": False,
        "profile_input_SHA256": profile_input_sha,
    }
    profile = ToolPermissionProfile(
        **profile_data,
        profile_SHA256=_profile_digest_from_record(profile_data),
    )
    validate_tool_permission_profile(profile)
    result_data = {
        "schema_version": TOOL_PERMISSION_SCHEMA_VERSION,
        "disposition": ToolPermissionProfileDisposition.ISSUED,
        "profile": profile,
    }
    profile_result = ToolPermissionProfileResult(
        **result_data,
        result_SHA256=_profile_result_digest_from_record(result_data),
    )
    return profile_result


def validate_tool_permission_profile(profile: ToolPermissionProfile) -> None:
    """Validate profile integrity without repair or side effects."""

    try:
        validated = ToolPermissionProfile.model_validate(
            profile.model_dump(mode="json")
        )
    except ValueError as exc:
        raise ToolPermissionProfileIntegrityError(
            "tool permission profile integrity is invalid"
        ) from exc
    _validate_profile_integrity(
        validated,
        error_type=ToolPermissionProfileIntegrityError,
    )


def evaluate_tool_permission(
    request: ToolPermissionCheckRequest,
) -> ToolPermissionDecisionEvidence:
    """Evaluate a tool permission request without invoking the tool."""

    try:
        validated_request = ToolPermissionCheckRequest.model_validate(
            request.model_dump(mode="json")
        )
    except AttributeError as exc:
        raise ToolPermissionEvaluationError(
            "request must be a ToolPermissionCheckRequest"
        ) from exc
    except ValueError as exc:
        raise ToolPermissionEvaluationError(
            "tool permission check request is invalid"
        ) from exc
    profile = validated_request.profile
    allocation = validated_request.allocation
    validate_tool_permission_profile(profile)
    validate_workspace_allocation(allocation)
    _validate_profile_allocation_binding(
        profile=profile,
        allocation=allocation,
        error_type=ToolPermissionEvaluationError,
    )
    decision, reason, matched_allowed, matched_forbidden = _evaluate_permission(
        request=validated_request,
    )
    data = {
        "schema_version": TOOL_PERMISSION_SCHEMA_VERSION,
        "decision": decision,
        "reason": reason,
        "operation": validated_request.operation,
        "work_packet_id": profile.work_packet_id,
        "allocation_id": profile.allocation_id,
        "profile_id": profile.profile_id,
        "workspace_relative_path": validated_request.workspace_relative_path,
        "resolved_target_path": validated_request.resolved_target_path,
        "matched_allowed_pattern": matched_allowed,
        "matched_forbidden_pattern": matched_forbidden,
        "profile_SHA256": profile.profile_SHA256,
    }
    decision_input_sha = _decision_input_digest_from_record(data)
    evidence_data = {**data, "decision_input_SHA256": decision_input_sha}
    return ToolPermissionDecisionEvidence(
        **evidence_data,
        decision_SHA256=_decision_digest_from_record(evidence_data),
    )


def validate_tool_permission_decision(
    decision: ToolPermissionDecisionEvidence,
) -> None:
    """Validate deterministic decision evidence without repair."""

    try:
        validated = ToolPermissionDecisionEvidence.model_validate(
            decision.model_dump(mode="json")
        )
    except ValueError as exc:
        raise ToolPermissionProfileIntegrityError(
            "tool permission decision integrity is invalid"
        ) from exc
    _validate_decision_integrity(
        validated,
        error_type=ToolPermissionProfileIntegrityError,
    )


def _build_grant(
    *,
    request: ToolPermissionGrantRequest,
    allowed_paths: tuple[str, ...],
    forbidden_paths: tuple[str, ...],
) -> ToolPermissionGrant:
    data = {
        "operation": request.operation,
        "allowed_paths": allowed_paths,
        "forbidden_paths": forbidden_paths,
        "source_allowed_action": request.source_allowed_action,
        "rationale": request.rationale,
    }
    return ToolPermissionGrant(
        **data,
        grant_SHA256=_grant_digest_from_record(data),
    )


def _evaluate_permission(
    *, request: ToolPermissionCheckRequest
) -> tuple[
    ToolPermissionDecision,
    ToolPermissionDecisionReason,
    str | None,
    str | None,
]:
    relative_path = request.workspace_relative_path
    resolved_path = request.resolved_target_path
    if not _target_relative_path_is_valid(relative_path):
        return _deny(ToolPermissionDecisionReason.TARGET_PATH_INVALID)
    if not _target_absolute_path_is_valid(resolved_path):
        return _deny(ToolPermissionDecisionReason.TARGET_PATH_INVALID)
    expected_resolved = _workspace_join(
        request.profile.resolved_workspace_root,
        relative_path,
    )
    if resolved_path != expected_resolved or not _is_under_workspace(
        resolved_path,
        request.profile.resolved_workspace_root,
    ):
        return _deny(ToolPermissionDecisionReason.TARGET_OUTSIDE_WORKSPACE)
    protected = _first_matching_pattern(relative_path, request.profile.protected_paths)
    if protected is not None:
        return _deny(
            ToolPermissionDecisionReason.TARGET_IN_PROTECTED_ROOT,
            matched_forbidden_pattern=protected,
        )
    forbidden = _first_matching_pattern(
        relative_path, _profile_forbidden_paths(request.profile)
    )
    if forbidden is not None:
        return _deny(
            ToolPermissionDecisionReason.TARGET_IN_FORBIDDEN_SCOPE,
            matched_forbidden_pattern=forbidden,
        )
    grant = _grant_for_operation(request.profile, request.operation)
    if grant is None:
        reason = (
            ToolPermissionDecisionReason.OPERATION_EXPLICITLY_DENIED
            if request.operation in _NEVER_GRANTABLE_OPERATIONS
            else ToolPermissionDecisionReason.OPERATION_NOT_GRANTED
        )
        return _deny(reason)
    allowed = _first_matching_pattern(relative_path, grant.allowed_paths)
    if allowed is None:
        return _deny(ToolPermissionDecisionReason.TARGET_NOT_IN_ALLOWED_SCOPE)
    return (
        ToolPermissionDecision.ALLOW,
        ToolPermissionDecisionReason.ALLOWED_BY_EXPLICIT_GRANT,
        allowed,
        None,
    )


def _deny(
    reason: ToolPermissionDecisionReason,
    *,
    matched_allowed_pattern: str | None = None,
    matched_forbidden_pattern: str | None = None,
) -> tuple[
    ToolPermissionDecision,
    ToolPermissionDecisionReason,
    str | None,
    str | None,
]:
    return (
        ToolPermissionDecision.DENY,
        reason,
        matched_allowed_pattern,
        matched_forbidden_pattern,
    )


def _validated_compilation_result(
    compilation_result: WorkPacketCompilationResult,
) -> WorkPacketCompilationResult:
    try:
        result = WorkPacketCompilationResult.model_validate(
            compilation_result.model_dump(mode="json")
        )
    except ValueError as exc:
        raise ToolPermissionProfileIntegrityError(
            "WorkPacket compilation result is invalid"
        ) from exc
    validate_work_packet(result.work_packet)
    return result


def _validated_allocation_result(
    allocation_result: WorkspaceAllocationResult,
) -> WorkspaceAllocationResult:
    try:
        result = WorkspaceAllocationResult.model_validate(
            allocation_result.model_dump(mode="json")
        )
    except ValueError as exc:
        raise ToolPermissionProfileIntegrityError(
            "workspace allocation result is invalid"
        ) from exc
    validate_workspace_allocation(result.allocation)
    return result


def _validate_compilation_result_for_profile(
    result: WorkPacketCompilationResult,
    *,
    error_type: type[ValueError],
) -> None:
    packet = result.work_packet
    if result.disposition is not WorkPacketCompilationDisposition.COMPILED:
        raise error_type("WorkPacket compilation result must be compiled")
    if packet.execution_ready is not False:
        raise error_type("WorkPacket must not be execution-ready")
    if packet.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("WorkPacket Git authority must be human-only")
    _require_unsatisfied_tool_permission_requirement(packet, error_type=error_type)


def _validate_allocation_for_profile(
    allocation: WorkspaceAllocation,
    *,
    error_type: type[ValueError],
) -> None:
    if allocation.disposition is not WorkspaceAllocationDisposition.ALLOCATED:
        raise error_type("workspace allocation must be allocated")
    if allocation.lifecycle_state is not WorkspaceLifecycleState.ALLOCATED:
        raise error_type("workspace allocation lifecycle must be allocated")
    if allocation.exclusive is not True:
        raise error_type("workspace allocation must be exclusive")
    if allocation.workspace_requirement_satisfied is not True:
        raise error_type("workspace requirement must be satisfied")
    if allocation.execution_ready is not False:
        raise error_type("workspace allocation must not be execution-ready")
    if allocation.tool_permissions_ready is not False:
        raise error_type("workspace allocation must not already have tool permissions")
    if allocation.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("workspace allocation Git authority must be human-only")


def _validate_work_packet_allocation_binding(
    *,
    packet: WorkPacket,
    allocation: WorkspaceAllocation,
    error_type: type[ValueError],
) -> None:
    if allocation.work_packet_id != packet.work_packet_id:
        raise error_type("workspace allocation WorkPacket ID mismatch")
    if allocation.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("workspace allocation WorkPacket digest mismatch")


def _validate_scope_projection_matches_packet(
    *,
    packet: WorkPacket,
    allocation: WorkspaceAllocation,
    error_type: type[ValueError],
) -> None:
    projection = allocation.scope_projection
    scope = packet.repository_scope
    if projection.allowed_paths != scope.allowed_paths:
        raise error_type("workspace allocation allowed paths mismatch")
    if projection.forbidden_paths != scope.forbidden_paths:
        raise error_type("workspace allocation forbidden paths mismatch")
    if projection.allowed_actions != scope.allowed_actions:
        raise error_type("workspace allocation allowed actions mismatch")
    if projection.forbidden_actions != scope.forbidden_actions:
        raise error_type("workspace allocation forbidden actions mismatch")
    if projection.scope_enforcement_ready is not False:
        raise error_type("workspace scope enforcement must remain deferred")


def _validate_profile_request_bindings(
    request: ToolPermissionProfileRequest,
    *,
    error_type: type[ValueError],
) -> None:
    result = _validated_compilation_result(request.compilation_result)
    allocation_result = _validated_allocation_result(request.allocation_result)
    packet = result.work_packet
    allocation = allocation_result.allocation
    authorization = request.profile_authorization
    _validate_compilation_result_for_profile(result, error_type=error_type)
    _validate_allocation_for_profile(allocation, error_type=error_type)
    _validate_work_packet_allocation_binding(
        packet=packet,
        allocation=allocation,
        error_type=error_type,
    )
    _validate_scope_projection_matches_packet(
        packet=packet,
        allocation=allocation,
        error_type=error_type,
    )
    if authorization.work_packet_id != packet.work_packet_id:
        raise error_type("authorization WorkPacket ID mismatch")
    if authorization.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("authorization WorkPacket digest mismatch")
    if authorization.allocation_id != allocation.allocation_id:
        raise error_type("authorization allocation ID mismatch")
    if authorization.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("authorization allocation digest mismatch")
    _validated_grant_requests(
        grant_requests=authorization.grant_requests,
        packet=packet,
        error_type=error_type,
    )


def _validated_grant_requests(
    *,
    grant_requests: tuple[ToolPermissionGrantRequest, ...],
    packet: WorkPacket,
    error_type: type[ValueError],
) -> tuple[ToolPermissionGrantRequest, ...]:
    if not grant_requests:
        raise error_type("grant requests must not be empty")
    validated = tuple(
        ToolPermissionGrantRequest.model_validate(request.model_dump(mode="json"))
        for request in grant_requests
    )
    operations = tuple(request.operation for request in validated)
    if len(operations) != len(frozenset(operations)):
        raise error_type("grant requests must not contain duplicate operations")
    allowed_actions = packet.repository_scope.allowed_actions
    forbidden_actions = packet.repository_scope.forbidden_actions
    for request in validated:
        if request.operation not in _GRANTABLE_OPERATIONS:
            raise error_type("operation is not grantable in P17.2")
        if request.source_allowed_action not in allowed_actions:
            raise error_type("grant action reference is not allowed by WorkPacket")
        if request.source_allowed_action in forbidden_actions:
            raise error_type("grant action reference is forbidden by WorkPacket")
    return tuple(sorted(validated, key=lambda item: _operation_index(item.operation)))


def _require_unsatisfied_tool_permission_requirement(
    packet: WorkPacket,
    *,
    error_type: type[ValueError],
) -> None:
    for requirement in packet.downstream_requirements:
        if (
            requirement.capability
            is WorkPacketDownstreamCapability.TOOL_PERMISSION_PROFILE
        ):
            if getattr(requirement, "satisfied_by_compiler", False) is not False:
                raise error_type("tool permission requirement is already satisfied")
            return
    raise error_type("tool permission downstream requirement is missing")


def _requires_risk_acknowledgement(
    grant_requests: tuple[ToolPermissionGrantRequest, ...],
) -> bool:
    return any(request.operation in _MUTATING_OPERATIONS for request in grant_requests)


def _validate_scope_pattern_grammar(patterns: tuple[str, ...]) -> None:
    for pattern in patterns:
        _validate_repository_path_pattern(pattern)


def _validate_profile_integrity(
    profile: ToolPermissionProfile,
    *,
    error_type: type[ValueError],
) -> None:
    grant_operations = tuple(grant.operation for grant in profile.grants)
    if grant_operations != _sort_operations(grant_operations):
        raise error_type("profile grants must be ordered by operation taxonomy")
    if len(grant_operations) != len(frozenset(grant_operations)):
        raise error_type("profile grants must have unique operations")
    if any(operation not in _GRANTABLE_OPERATIONS for operation in grant_operations):
        raise error_type("profile contains non-grantable operation")
    expected_denied = tuple(
        operation for operation in _OPERATION_ORDER if operation not in grant_operations
    )
    if profile.denied_operations != expected_denied:
        raise error_type("denied operations must be exact complement of grants")
    if tuple(profile.protected_paths) != _PROTECTED_PATHS:
        raise error_type("protected paths must match canonical tuple")
    profile_input_record = _profile_input_record(profile)
    if profile.profile_input_SHA256 != _profile_input_digest_from_record(
        profile_input_record
    ):
        raise error_type("profile_input_SHA256 mismatch")
    expected_profile_id = _profile_id_from_profile(profile)
    if profile.profile_id != expected_profile_id:
        raise error_type("profile_id mismatch")
    if profile.profile_SHA256 != _profile_digest(profile):
        raise error_type("profile_SHA256 mismatch")
    for grant in profile.grants:
        if grant.grant_SHA256 != _grant_digest(grant):
            raise error_type("grant_SHA256 mismatch")


def _validate_profile_allocation_binding(
    *,
    profile: ToolPermissionProfile,
    allocation: WorkspaceAllocation,
    error_type: type[ValueError],
) -> None:
    if profile.work_packet_id != allocation.work_packet_id:
        raise error_type("profile WorkPacket ID mismatch")
    if profile.work_packet_SHA256 != allocation.work_packet_SHA256:
        raise error_type("profile WorkPacket digest mismatch")
    if profile.allocation_id != allocation.allocation_id:
        raise error_type("profile allocation ID mismatch")
    if profile.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("profile allocation digest mismatch")
    if profile.workspace_root != allocation.workspace_root:
        raise error_type("profile workspace root mismatch")
    if profile.resolved_workspace_root != allocation.resolved_workspace_root:
        raise error_type("profile resolved workspace root mismatch")
    if profile.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("profile Git authority must be human-only")
    if allocation.git_authority is not WorkPacketGitAuthority.HUMAN_ONLY:
        raise error_type("allocation Git authority must be human-only")


def _validate_decision_integrity(
    decision: ToolPermissionDecisionEvidence,
    *,
    error_type: type[ValueError],
) -> None:
    if decision.decision is ToolPermissionDecision.ALLOW:
        if (
            decision.reason
            is not ToolPermissionDecisionReason.ALLOWED_BY_EXPLICIT_GRANT
        ):
            raise error_type("allow decision requires allow reason")
        if decision.matched_allowed_pattern is None:
            raise error_type("allow decision requires matched allowed pattern")
        if decision.matched_forbidden_pattern is not None:
            raise error_type("allow decision must not have matched forbidden pattern")
    else:
        if decision.reason is ToolPermissionDecisionReason.ALLOWED_BY_EXPLICIT_GRANT:
            raise error_type("deny decision must not use allow reason")
        if decision.reason in {
            ToolPermissionDecisionReason.TARGET_IN_PROTECTED_ROOT,
            ToolPermissionDecisionReason.TARGET_IN_FORBIDDEN_SCOPE,
        }:
            if decision.matched_forbidden_pattern is None:
                raise error_type("path denial requires matched forbidden pattern")
    if decision.decision_input_SHA256 != _decision_input_digest(decision):
        raise error_type("decision_input_SHA256 mismatch")
    if decision.decision_SHA256 != _decision_digest(decision):
        raise error_type("decision_SHA256 mismatch")


def _profile_forbidden_paths(profile: ToolPermissionProfile) -> tuple[str, ...]:
    return profile.grants[0].forbidden_paths


def _grant_for_operation(
    profile: ToolPermissionProfile,
    operation: ToolPermissionOperation,
) -> ToolPermissionGrant | None:
    for grant in profile.grants:
        if grant.operation is operation:
            return grant
    return None


def _target_relative_path_is_valid(value: str) -> bool:
    if not value or "\x00" in value or "\\" in value:
        return False
    if value.startswith("/") or _DRIVE_RELATIVE_PATTERN.match(value):
        return False
    if _CONTROL_CHARACTER_PATTERN.search(value):
        return False
    if any(component in {"", ".", ".."} for component in value.split("/")):
        return False
    return True


def _target_absolute_path_is_valid(value: str) -> bool:
    try:
        _validate_absolute_workspace_path(value)
    except ValueError:
        return False
    return True


def _workspace_join(workspace_root: str, relative_path: str) -> str:
    return f"{workspace_root.rstrip('/')}/{relative_path}"


def _is_under_workspace(target: str, workspace_root: str) -> bool:
    root = workspace_root.rstrip("/")
    return target == root or target.startswith(f"{root}/")


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


def _profile_input_record(profile: ToolPermissionProfile) -> dict[str, object]:
    return {
        "schema_version": profile.schema_version,
        "policy_id": profile.policy_id,
        "work_packet_id": profile.work_packet_id,
        "work_packet_SHA256": profile.work_packet_SHA256,
        "allocation_id": profile.allocation_id,
        "allocation_SHA256": profile.allocation_SHA256,
        "workspace_root": profile.workspace_root,
        "resolved_workspace_root": profile.resolved_workspace_root,
        "git_authority": profile.git_authority,
        "grants": profile.grants,
        "denied_operations": profile.denied_operations,
        "protected_paths": profile.protected_paths,
        "scope_projection_SHA256": profile.scope_projection_SHA256,
        "authorization_SHA256": profile.authorization_SHA256,
    }


def _profile_id_from_profile(profile: ToolPermissionProfile) -> str:
    prefix = profile.profile_id.rsplit("-", 1)[0]
    return f"{prefix}-{profile.profile_input_SHA256[:12]}"


def _profile_id(
    *,
    ticket_id: str,
    publication_revision: int,
    profile_input_SHA256: str,
) -> str:
    normalized_ticket = ticket_id.replace(".", "-")
    return f"TP-{normalized_ticket}-R{publication_revision:04d}-{profile_input_SHA256[:12]}"


def _sort_operations(
    operations: tuple[ToolPermissionOperation, ...],
) -> tuple[ToolPermissionOperation, ...]:
    return tuple(sorted(operations, key=_operation_index))


def _operation_index(operation: ToolPermissionOperation) -> int:
    return _OPERATION_ORDER.index(operation)


def _is_shadow_identifier(value: str) -> bool:
    return value.upper().startswith("SHADOW-") or value.casefold().startswith("shadow-")


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


def _profile_authorization_digest(
    authorization: ToolPermissionProfileAuthorization,
) -> str:
    return _profile_authorization_digest_from_record(
        authorization.model_dump(mode="json", exclude={"authorization_SHA256"})
    )


def _profile_authorization_digest_from_record(record: dict[str, object]) -> str:
    return _digest(PROFILE_AUTHORIZATION_DIGEST_ALGORITHM, record)


def _grant_digest(grant: ToolPermissionGrant) -> str:
    return _grant_digest_from_record(
        grant.model_dump(mode="json", exclude={"grant_SHA256"})
    )


def _grant_digest_from_record(record: dict[str, object]) -> str:
    return _digest(GRANT_DIGEST_ALGORITHM, record)


def _profile_input_digest_from_record(record: dict[str, object]) -> str:
    return _digest(PROFILE_INPUT_DIGEST_ALGORITHM, record)


def _profile_digest(profile: ToolPermissionProfile) -> str:
    return _profile_digest_from_record(
        profile.model_dump(mode="json", exclude={"profile_SHA256"})
    )


def _profile_digest_from_record(record: dict[str, object]) -> str:
    return _digest(PROFILE_DIGEST_ALGORITHM, record)


def _profile_result_digest(result: ToolPermissionProfileResult) -> str:
    return _profile_result_digest_from_record(
        result.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _profile_result_digest_from_record(record: dict[str, object]) -> str:
    return _digest(PROFILE_RESULT_DIGEST_ALGORITHM, record)


def _decision_input_digest(decision: ToolPermissionDecisionEvidence) -> str:
    return _decision_input_digest_from_record(
        decision.model_dump(
            mode="json",
            exclude={"decision_input_SHA256", "decision_SHA256"},
        )
    )


def _decision_input_digest_from_record(record: dict[str, object]) -> str:
    return _digest(DECISION_INPUT_DIGEST_ALGORITHM, record)


def _decision_digest(decision: ToolPermissionDecisionEvidence) -> str:
    return _decision_digest_from_record(
        decision.model_dump(mode="json", exclude={"decision_SHA256"})
    )


def _decision_digest_from_record(record: dict[str, object]) -> str:
    return _digest(DECISION_DIGEST_ALGORITHM, record)
