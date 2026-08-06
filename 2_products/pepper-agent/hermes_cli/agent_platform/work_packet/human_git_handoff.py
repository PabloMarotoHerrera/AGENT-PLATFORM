"""Deterministic non-executing human Git handoff contracts.

P17.7 converts one completed P17.6 diff/artifact review into a bounded
human-only Git handoff package. It renders declarative commands for a human to
review and run; it does not inspect Git, launch processes, read files, stage,
commit, push, clean, or roll back anything.
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
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.work_packet.compiler import (
    WorkPacketCompilationResult,
    validate_work_packet,
)
from hermes_cli.agent_platform.work_packet.diff_artifact_review import (
    AggregateReviewState,
    ArtifactReviewVerdict,
    DiffArtifactReviewResult,
    DiffReviewVerdict,
    ReviewFindingCode,
    ReviewFindingSeverity,
    ReviewObservedPath,
    ReviewObservedPathStatus,
    validate_diff_artifact_review_result,
)
from hermes_cli.agent_platform.work_packet.outcome_envelopes import (
    OutcomeEnvelope,
    OutcomeEnvelopeKind,
    validate_outcome_envelope,
)
from hermes_cli.agent_platform.work_packet.tool_permissions import (
    ToolPermissionProfileResult,
    validate_tool_permission_profile,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocationResult,
    WorkspaceRepositoryIdentity,
    validate_workspace_allocation,
)


HUMAN_GIT_HANDOFF_SCHEMA_VERSION = 1
HUMAN_GIT_HANDOFF_POLICY_ID = (
    "pepper-exact-review-bound-non-executing-human-git-handoff-v1"
)

CANDIDATE_DIGEST_ALGORITHM = "agent-platform-git-handoff-candidate-sha256-v1"
APPROVAL_DIGEST_ALGORITHM = "agent-platform-git-handoff-approval-sha256-v1"
VERIFICATION_STEP_DIGEST_ALGORITHM = (
    "agent-platform-git-handoff-verification-step-sha256-v1"
)
COMMAND_DIGEST_ALGORITHM = "agent-platform-git-handoff-command-sha256-v1"
POST_COMMIT_EXPECTATION_DIGEST_ALGORITHM = (
    "agent-platform-git-handoff-post-commit-expectation-sha256-v1"
)
PACKAGE_DIGEST_ALGORITHM = "agent-platform-human-git-handoff-package-sha256-v1"
HANDOFF_ID_DIGEST_ALGORITHM = "agent-platform-human-git-handoff-id-sha256-v1"
RESULT_DIGEST_ALGORITHM = "agent-platform-human-git-handoff-result-sha256-v1"
POWERSHELL_DIGEST_ALGORITHM = "agent-platform-human-git-handoff-powershell-sha256-v1"

POST_COMMIT_PEPPER_FILE_COUNT = 6884
_RENDERED_POWERSHELL_MAX_LENGTH = 32768

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
_CANDIDATE_ID_PATTERN = r"^GHCP-[0-9]{3}$"
_STEP_ID_PATTERN = r"^GHVS-[0-9]{3}$"
_COMMAND_ID_PATTERN = r"^GHCM-[0-9]{3}$"
_PACKAGE_ID_PATTERN = r"^GHP-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$"
_RESULT_ID_PATTERN = r"^HGR-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$"
_WINDOWS_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_WORK_PACKET_REVISION_PATTERN = re.compile(r"-R(?P<revision>[0-9]{4})-")
_SHELL_METACHARACTERS = frozenset(";&|<>`$(){}[]")
_PATH_SECRET_COMPONENTS = (
    "credentials",
    "secrets",
    "private_key",
    "id_rsa",
    "id_ed25519",
    "auth.json",
    "token.json",
)
_FORBIDDEN_GIT_VERBS = frozenset({
    "reset",
    "clean",
    "stash",
    "switch",
    "checkout",
    "branch",
    "merge",
    "rebase",
    "worktree",
    "tag",
})
_ALLOWED_CANDIDATE_REVIEW_STATUSES = frozenset({
    ReviewObservedPathStatus.ADDED,
    ReviewObservedPathStatus.MODIFIED,
    ReviewObservedPathStatus.DELETED,
    ReviewObservedPathStatus.UNTRACKED,
})

__all__ = (
    "HUMAN_GIT_HANDOFF_SCHEMA_VERSION",
    "HUMAN_GIT_HANDOFF_POLICY_ID",
    "GitHandoffState",
    "GitHandoffDecision",
    "GitHandoffPathStatus",
    "GitHandoffVerificationKind",
    "GitHandoffCommandKind",
    "GitHandoffAuthority",
    "GitHandoffCandidate",
    "GitHandoffApproval",
    "GitHandoffVerificationStep",
    "GitHandoffCommand",
    "GitHandoffPostCommitExpectation",
    "GitHandoffPackage",
    "GitHandoffRequest",
    "GitHandoffResult",
    "HumanGitHandoffError",
    "HumanGitHandoffInputError",
    "HumanGitHandoffIntegrityError",
    "HumanGitHandoffPolicyError",
    "HumanGitHandoffStateError",
    "HumanGitHandoffValidationError",
    "build_git_handoff_candidates",
    "validate_human_git_handoff_request",
    "build_human_git_handoff",
    "validate_human_git_handoff_result",
    "render_human_git_handoff_powershell",
)


class HumanGitHandoffError(ValueError):
    """Base error for P17.7 human Git handoff failures."""


class HumanGitHandoffInputError(HumanGitHandoffError):
    """Raised when supplied handoff evidence is structurally invalid."""


class HumanGitHandoffIntegrityError(HumanGitHandoffError):
    """Raised when deterministic handoff digests fail validation."""


class HumanGitHandoffPolicyError(HumanGitHandoffError):
    """Raised when handoff evidence violates the P17.7 policy boundary."""


class HumanGitHandoffStateError(HumanGitHandoffError):
    """Raised when prerequisite state is incompatible with handoff."""


class HumanGitHandoffValidationError(HumanGitHandoffError):
    """Raised when a handoff result cannot be validated."""


class GitHandoffState(str, Enum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class GitHandoffDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


class GitHandoffPathStatus(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"


class GitHandoffVerificationKind(str, Enum):
    PRE_STAGING = "pre_staging"
    CANDIDATE_SET = "candidate_set"
    STAGED_INDEX = "staged_index"
    POST_COMMIT = "post_commit"
    POST_PUSH = "post_push"
    COMMITTED_INTEGRITY = "committed_integrity"


class GitHandoffCommandKind(str, Enum):
    SET_LOCATION = "set_location"
    STAGE_PATH = "stage_path"
    DIFF_CHECK = "diff_check"
    DIFF_STAT = "diff_stat"
    DIFF_PATHS = "diff_paths"
    STATUS = "status"
    COMMIT = "commit"
    PUSH = "push"
    VERIFY = "verify"
    INTEGRITY = "integrity"


class GitHandoffAuthority(str, Enum):
    HUMAN_ONLY = "human_only"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _contains_control(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def _contains_credential_marker(value: str) -> bool:
    lower = value.lower()
    return any(
        marker in lower
        for marker in (
            "access_token",
            "refresh_token",
            "authorization: bearer",
            "authorization: basic",
            "client_secret",
            "api_key",
            "api-key",
            "private key",
            "password=",
            "token=",
            "sk-",
        )
    )


def _validate_public_text(value: str) -> str:
    _reject_nul(value)
    if _contains_control(value):
        raise ValueError("text must not contain control characters")
    if _ANSI_PATTERN.search(value):
        raise ValueError("text must not contain ANSI control sequences")
    lower = value.lower()
    if _contains_credential_marker(value):
        raise ValueError("text must not contain credential-shaped values")
    if any(
        marker in lower
        for marker in (
            "raw stdout",
            "raw stderr",
            "raw diff",
            "diff --git",
            "file content",
            "traceback",
        )
    ):
        raise ValueError("text must not contain raw runtime evidence")
    if "c:/users/" in lower or "c:\\users\\" in lower:
        raise ValueError("text must not contain personal absolute paths")
    return value


def _validate_display_path(value: str) -> str:
    _reject_nul(value)
    if _contains_control(value) or _ANSI_PATTERN.search(value):
        raise ValueError("repository display path must be bounded display text")
    if _contains_credential_marker(value):
        raise ValueError("repository display path must not contain credentials")
    lower = value.lower()
    if any(
        marker in lower
        for marker in (
            "raw stdout",
            "raw stderr",
            "raw diff",
            "diff --git",
            "file content",
            "traceback",
        )
    ):
        raise ValueError(
            "repository display path must not contain raw runtime evidence"
        )
    if "c:/users/" in lower or "c:\\users\\" in lower:
        raise ValueError("repository display path must not contain personal paths")
    return value


def _validate_branch_name(value: str) -> str:
    _validate_public_text(value)
    if value.startswith("-") or value.endswith("/"):
        raise ValueError("branch name must be explicit and bounded")
    if any(character in value for character in _SHELL_METACHARACTERS):
        raise ValueError("branch name must not contain shell metacharacters")
    if ".." in value or "\\" in value or " " in value:
        raise ValueError("branch name must be an exact safe branch token")
    return value


def _validate_remote_name(value: str) -> str:
    if value != "origin":
        raise ValueError("remote name must be origin")
    return value


def _validate_commit_message(value: str) -> str:
    if value != value.strip():
        raise ValueError("commit message must not have surrounding whitespace")
    _validate_public_text(value)
    lower = value.lower()
    if any(character in value for character in _SHELL_METACHARACTERS):
        raise ValueError("commit message must not contain shell syntax")
    if any(marker in lower for marker in ("git ", "--amend", "force push")):
        raise ValueError("commit message must not contain Git instructions")
    if any(marker in lower for marker in ("fixes #", "closes #", "resolves #")):
        raise ValueError("commit message must not contain issue-closing syntax")
    return value


def _validate_relative_path(value: str) -> str:
    if value != value.strip():
        raise ValueError("path must not contain surrounding whitespace")
    if not value:
        raise ValueError("path must be nonempty")
    if _contains_control(value):
        raise ValueError("path must not contain control characters")
    if "\\" in value:
        raise ValueError("path must use forward slashes")
    if value.startswith("/") or _WINDOWS_DRIVE_PATTERN.match(value):
        raise ValueError("path must be repository-relative")
    if value.endswith("/"):
        raise ValueError("path must not end with a slash")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("path must not contain empty or traversal components")
    lowered = tuple(part.lower() for part in parts)
    if ".git" in lowered or any(part.startswith(".git") for part in lowered):
        raise ValueError("path must not reference Git metadata")
    for part in lowered:
        if part == ".env" or part.startswith(".env."):
            raise ValueError("path must not reference environment files")
        if part in _PATH_SECRET_COMPONENTS:
            raise ValueError("path must not reference credential files")
    return value


def _validate_identifier_tuple(value: tuple[str, ...]) -> tuple[str, ...]:
    if len(value) != len(frozenset(value)):
        raise ValueError("identifier tuple must not contain duplicates")
    if value != tuple(sorted(value)):
        raise ValueError("identifier tuple must be deterministic")
    return value


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
CommitText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=40, max_length=40, pattern=_COMMIT_PATTERN),
]
BoundedIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
    AfterValidator(_validate_public_text),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_public_text),
]
ApprovalReferenceText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=192),
    AfterValidator(_validate_public_text),
]
CommitMessageText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
    AfterValidator(_validate_commit_message),
]
BranchNameText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
    AfterValidator(_validate_branch_name),
]
RemoteNameText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=6, max_length=6),
    AfterValidator(_validate_remote_name),
]
RepositoryDisplayPathText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_display_path),
]
RelativePathText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_relative_path),
]
CandidateIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=8, pattern=_CANDIDATE_ID_PATTERN),
]
VerificationStepIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=8, pattern=_STEP_ID_PATTERN),
]
CommandIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=8, pattern=_COMMAND_ID_PATTERN),
]
PackageIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=24, max_length=128, pattern=_PACKAGE_ID_PATTERN),
]
HandoffIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=24, max_length=128, pattern=_RESULT_ID_PATTERN),
]


class _HandoffModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class GitHandoffCandidate(_HandoffModel):
    candidate_id: CandidateIdentifier
    relative_path: RelativePathText
    status: GitHandoffPathStatus
    content_SHA256: DigestText | None = None
    bytes_after: int | None = Field(default=None, ge=0, strict=True)
    source_observation_id: BoundedIdentifier
    source_artifact_id: BoundedIdentifier | None = None
    candidate_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_candidate(self) -> GitHandoffCandidate:
        if self.status is GitHandoffPathStatus.DELETED:
            if self.content_SHA256 is not None or self.bytes_after is not None:
                raise ValueError("deleted candidates must not carry content evidence")
        else:
            if self.content_SHA256 is None or self.bytes_after is None:
                raise ValueError("nondeleted candidates require content evidence")
        if self.candidate_SHA256 != _candidate_digest(self):
            raise ValueError("candidate digest mismatch")
        return self


class GitHandoffApproval(_HandoffModel):
    approval_reference: ApprovalReferenceText
    human_approver_id: BoundedIdentifier
    synthetic: Literal[False] = False
    decision: GitHandoffDecision
    review_id: BoundedIdentifier
    review_SHA256: DigestText
    accepted_finding_ids: tuple[BoundedIdentifier, ...] = ()
    accepted_candidate_ids: tuple[CandidateIdentifier, ...] = Field(min_length=1)
    commit_message: CommitMessageText
    remote_name: RemoteNameText = "origin"
    branch_name: BranchNameText
    expected_parent_commit: CommitText
    rationale: BoundedText
    approval_SHA256: DigestText

    @field_validator("accepted_finding_ids", "accepted_candidate_ids", mode="after")
    @classmethod
    def _validate_identifier_order(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _validate_identifier_tuple(value)

    @model_validator(mode="after")
    def _validate_approval(self) -> GitHandoffApproval:
        if self.human_approver_id.upper().startswith("SHADOW-"):
            raise ValueError("shadow approver cannot authorize human Git handoff")
        if self.approval_SHA256 != _approval_digest(self):
            raise ValueError("approval digest mismatch")
        return self


class GitHandoffVerificationStep(_HandoffModel):
    step_id: VerificationStepIdentifier
    kind: GitHandoffVerificationKind
    order: int = Field(ge=1, strict=True)
    title: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
        AfterValidator(_validate_public_text),
    ]
    expected_condition: BoundedText
    blocking: Literal[True] = True
    step_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_step(self) -> GitHandoffVerificationStep:
        if self.step_id != f"GHVS-{self.order:03d}":
            raise ValueError("verification step ID must match order")
        if self.step_SHA256 != _verification_step_digest(self):
            raise ValueError("verification step digest mismatch")
        return self


class GitHandoffCommand(_HandoffModel):
    command_id: CommandIdentifier
    kind: GitHandoffCommandKind
    order: int = Field(ge=1, strict=True)
    argv: tuple[BoundedIdentifier, ...] = Field(min_length=1)
    display_text: BoundedText
    human_execution_required: Literal[True] = True
    automatic_execution_authorized: Literal[False] = False
    command_SHA256: DigestText

    @field_validator("argv", mode="after")
    @classmethod
    def _validate_argv(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _validate_argv_tokens(value)
        return value

    @model_validator(mode="after")
    def _validate_command(self) -> GitHandoffCommand:
        if self.command_id != f"GHCM-{self.order:03d}":
            raise ValueError("command ID must match order")
        _validate_command_shape(self)
        if self.command_SHA256 != _command_digest(self):
            raise ValueError("command digest mismatch")
        return self


class GitHandoffPostCommitExpectation(_HandoffModel):
    expected_parent_commit: CommitText
    expected_branch: BranchNameText
    expected_remote: RemoteNameText = "origin"
    expected_commit_message: CommitMessageText
    expected_file_count: int = Field(ge=0, strict=True)
    expected_added_count: int = Field(ge=0, strict=True)
    expected_modified_count: int = Field(ge=0, strict=True)
    expected_deleted_count: int = Field(ge=0, strict=True)
    expected_candidate_paths: tuple[RelativePathText, ...]
    expected_worktree_clean: Literal[True] = True
    expected_remote_match: Literal[True] = True
    expected_integrity_file_count: Literal[6884] = POST_COMMIT_PEPPER_FILE_COUNT
    expectation_SHA256: DigestText

    @field_validator("expected_candidate_paths", mode="after")
    @classmethod
    def _validate_candidate_paths(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(frozenset(value)):
            raise ValueError("expected candidate paths must be unique")
        if value != tuple(sorted(value)):
            raise ValueError("expected candidate paths must be sorted")
        return value

    @model_validator(mode="after")
    def _validate_expectation(self) -> GitHandoffPostCommitExpectation:
        if self.expected_file_count != len(self.expected_candidate_paths):
            raise ValueError("expected file count must equal candidate path count")
        if (
            self.expected_added_count
            + self.expected_modified_count
            + self.expected_deleted_count
            != self.expected_file_count
        ):
            raise ValueError("expected status counts must equal file count")
        if self.expectation_SHA256 != _post_commit_expectation_digest(self):
            raise ValueError("post-commit expectation digest mismatch")
        return self


class GitHandoffPackage(_HandoffModel):
    schema_version: Literal[1] = HUMAN_GIT_HANDOFF_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-exact-review-bound-non-executing-human-git-handoff-v1"
    ] = HUMAN_GIT_HANDOFF_POLICY_ID
    package_id: PackageIdentifier
    authority: Literal[GitHandoffAuthority.HUMAN_ONLY] = GitHandoffAuthority.HUMAN_ONLY
    repository_identity: WorkspaceRepositoryIdentity
    repository_display_path: RepositoryDisplayPathText
    branch_name: BranchNameText
    remote_name: RemoteNameText = "origin"
    expected_parent_commit: CommitText
    commit_message: CommitMessageText
    candidates: tuple[GitHandoffCandidate, ...] = Field(min_length=1)
    verification_steps: tuple[GitHandoffVerificationStep, ...] = Field(min_length=6)
    commands: tuple[GitHandoffCommand, ...] = Field(min_length=1)
    post_commit_expectation: GitHandoffPostCommitExpectation
    package_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_package(self) -> GitHandoffPackage:
        _validate_candidate_collection(self.candidates, error_type=ValueError)
        _validate_step_collection(self.verification_steps, error_type=ValueError)
        _validate_command_collection(self.commands, error_type=ValueError)
        if self.repository_identity.workspace_branch != self.branch_name:
            raise ValueError("package branch must match repository identity")
        if self.repository_identity.source_commit != self.expected_parent_commit:
            raise ValueError("package parent must match repository identity")
        expected = _build_post_commit_expectation(
            candidates=self.candidates,
            expected_parent_commit=self.expected_parent_commit,
            expected_branch=self.branch_name,
            expected_remote=self.remote_name,
            expected_commit_message=self.commit_message,
        )
        if self.post_commit_expectation != expected:
            raise ValueError("post-commit expectation mismatch")
        if self.package_id != _package_id(self):
            raise ValueError("package ID mismatch")
        if self.package_SHA256 != _package_digest(self):
            raise ValueError("package digest mismatch")
        return self


class GitHandoffRequest(_HandoffModel):
    schema_version: Literal[1] = HUMAN_GIT_HANDOFF_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-exact-review-bound-non-executing-human-git-handoff-v1"
    ] = HUMAN_GIT_HANDOFF_POLICY_ID
    compilation_result: WorkPacketCompilationResult
    allocation_result: WorkspaceAllocationResult
    profile_result: ToolPermissionProfileResult
    outcome_envelope: OutcomeEnvelope
    diff_artifact_review_result: DiffArtifactReviewResult
    approval: GitHandoffApproval
    repository_display_path: RepositoryDisplayPathText

    @model_validator(mode="after")
    def _validate_request(self) -> GitHandoffRequest:
        _validate_request_bindings(self, error_type=ValueError)
        return self


class GitHandoffResult(_HandoffModel):
    schema_version: Literal[1] = HUMAN_GIT_HANDOFF_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-exact-review-bound-non-executing-human-git-handoff-v1"
    ] = HUMAN_GIT_HANDOFF_POLICY_ID
    handoff_id: HandoffIdentifier
    state: GitHandoffState
    decision: GitHandoffDecision
    authority: Literal[GitHandoffAuthority.HUMAN_ONLY] = GitHandoffAuthority.HUMAN_ONLY
    work_packet_id: BoundedIdentifier
    work_packet_SHA256: DigestText
    allocation_id: BoundedIdentifier
    allocation_SHA256: DigestText
    profile_id: BoundedIdentifier
    profile_SHA256: DigestText
    outcome_kind: OutcomeEnvelopeKind
    outcome_SHA256: DigestText
    review_id: BoundedIdentifier
    review_SHA256: DigestText
    approval_SHA256: DigestText
    package: GitHandoffPackage
    rendered_powershell_SHA256: DigestText
    candidate_count: int = Field(ge=0, strict=True)
    added_count: int = Field(ge=0, strict=True)
    modified_count: int = Field(ge=0, strict=True)
    deleted_count: int = Field(ge=0, strict=True)
    manual_validation_ids_pending: tuple[BoundedIdentifier, ...] = ()
    human_git_handoff_requirement_satisfied: StrictBool
    Git_commands_executed: int = Field(default=0, ge=0, strict=True)
    staging_performed: Literal[False] = False
    commit_performed: Literal[False] = False
    push_performed: Literal[False] = False
    automatic_cleanup_authorized: Literal[False] = False
    automatic_rollback_authorized: Literal[False] = False
    automatic_staging_authorized: Literal[False] = False
    automatic_commit_authorized: Literal[False] = False
    automatic_push_authorized: Literal[False] = False
    provider_dispatch_count: int = Field(default=0, ge=0, strict=True)
    model_inference_count: int = Field(default=0, ge=0, strict=True)
    result_SHA256: DigestText

    @field_validator("manual_validation_ids_pending", mode="after")
    @classmethod
    def _validate_manual_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _validate_identifier_tuple(value)

    @model_validator(mode="after")
    def _validate_result(self) -> GitHandoffResult:
        _validate_result_integrity(self, error_type=ValueError)
        return self


def build_git_handoff_candidates(
    review_result: DiffArtifactReviewResult,
) -> tuple[GitHandoffCandidate, ...]:
    """Derive exact human Git handoff candidates from a P17.6 review."""

    review = _validated_review_result(review_result)
    _require_review_extractable(review, error_type=HumanGitHandoffStateError)
    expected_paths = frozenset(item.relative_path for item in review.expected_mutations)
    observed_paths = frozenset(item.relative_path for item in review.observed_paths)
    if expected_paths != observed_paths:
        raise HumanGitHandoffPolicyError(
            "reviewed paths must exactly match expected paths"
        )
    artifact_by_path = {item.relative_path: item for item in review.artifacts}
    candidates: list[GitHandoffCandidate] = []
    for observed in sorted(review.observed_paths, key=lambda item: item.relative_path):
        if observed.relative_path not in expected_paths:
            raise HumanGitHandoffPolicyError(
                "unexpected reviewed path cannot be handed off"
            )
        status = _candidate_status(observed)
        artifact = artifact_by_path.get(observed.relative_path)
        data = {
            "candidate_id": f"GHCP-{len(candidates) + 1:03d}",
            "relative_path": observed.relative_path,
            "status": status,
            "content_SHA256": observed.content_SHA256,
            "bytes_after": observed.bytes_after,
            "source_observation_id": observed.observation_id,
            "source_artifact_id": artifact.artifact_id
            if artifact is not None
            else None,
        }
        candidates.append(
            GitHandoffCandidate(
                **data,
                candidate_SHA256=_digest_from_record(CANDIDATE_DIGEST_ALGORITHM, data),
            )
        )
    result = tuple(candidates)
    _validate_candidate_collection(result, error_type=HumanGitHandoffPolicyError)
    return result


def validate_human_git_handoff_request(request: GitHandoffRequest) -> None:
    """Validate a P17.7 handoff request without repair or side effects."""

    try:
        validated = GitHandoffRequest.model_validate(request.model_dump(mode="json"))
    except AttributeError as exc:
        raise HumanGitHandoffInputError("request must be a GitHandoffRequest") from exc
    except ValueError as exc:
        raise HumanGitHandoffInputError("invalid human Git handoff request") from exc
    try:
        _validate_request_bindings(validated, error_type=HumanGitHandoffPolicyError)
        _validate_request_approval(validated, error_type=HumanGitHandoffPolicyError)
    except HumanGitHandoffError:
        raise
    except ValueError as exc:
        raise HumanGitHandoffIntegrityError(
            "request integrity validation failed"
        ) from exc


def build_human_git_handoff(request: GitHandoffRequest) -> GitHandoffResult:
    """Build one deterministic non-executing human Git handoff result."""

    try:
        validated = GitHandoffRequest.model_validate(request.model_dump(mode="json"))
    except AttributeError as exc:
        raise HumanGitHandoffInputError("request must be a GitHandoffRequest") from exc
    except ValueError as exc:
        raise HumanGitHandoffInputError("invalid human Git handoff request") from exc
    validate_human_git_handoff_request(validated)
    candidates = build_git_handoff_candidates(validated.diff_artifact_review_result)
    decision = _derive_decision(validated, candidates)
    state = (
        GitHandoffState.COMPLETED
        if decision is GitHandoffDecision.APPROVED
        else GitHandoffState.BLOCKED
    )
    verification_steps = _build_verification_steps()
    commands = _build_commands(
        repository_display_path=validated.repository_display_path,
        branch_name=validated.approval.branch_name,
        remote_name=validated.approval.remote_name,
        expected_parent_commit=validated.approval.expected_parent_commit,
        commit_message=validated.approval.commit_message,
        candidates=candidates,
    )
    expectation = _build_post_commit_expectation(
        candidates=candidates,
        expected_parent_commit=validated.approval.expected_parent_commit,
        expected_branch=validated.approval.branch_name,
        expected_remote=validated.approval.remote_name,
        expected_commit_message=validated.approval.commit_message,
    )
    package_data = {
        "schema_version": HUMAN_GIT_HANDOFF_SCHEMA_VERSION,
        "policy_id": HUMAN_GIT_HANDOFF_POLICY_ID,
        "authority": GitHandoffAuthority.HUMAN_ONLY,
        "repository_identity": validated.allocation_result.allocation.repository_identity,
        "repository_display_path": validated.repository_display_path,
        "branch_name": validated.approval.branch_name,
        "remote_name": validated.approval.remote_name,
        "expected_parent_commit": validated.approval.expected_parent_commit,
        "commit_message": validated.approval.commit_message,
        "candidates": candidates,
        "verification_steps": verification_steps,
        "commands": commands,
        "post_commit_expectation": expectation,
    }
    package_data["package_id"] = _package_id_from_record(package_data)
    package = GitHandoffPackage(
        **package_data,
        package_SHA256=_digest_from_record(PACKAGE_DIGEST_ALGORITHM, package_data),
    )
    rendered = render_human_git_handoff_powershell(package)
    rendered_sha = _digest_text(POWERSHELL_DIGEST_ALGORITHM, rendered)
    packet = validated.compilation_result.work_packet
    allocation = validated.allocation_result.allocation
    profile = validated.profile_result.profile
    review = validated.diff_artifact_review_result
    counts = _candidate_counts(candidates)
    base = {
        "schema_version": HUMAN_GIT_HANDOFF_SCHEMA_VERSION,
        "policy_id": HUMAN_GIT_HANDOFF_POLICY_ID,
        "state": state,
        "decision": decision,
        "authority": GitHandoffAuthority.HUMAN_ONLY,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "profile_id": profile.profile_id,
        "profile_SHA256": profile.profile_SHA256,
        "outcome_kind": validated.outcome_envelope.envelope_kind,
        "outcome_SHA256": validated.outcome_envelope.envelope_SHA256,
        "review_id": review.review_id,
        "review_SHA256": review.result_SHA256,
        "approval_SHA256": validated.approval.approval_SHA256,
        "package": package,
        "rendered_powershell_SHA256": rendered_sha,
        "candidate_count": len(candidates),
        "added_count": counts[0],
        "modified_count": counts[1],
        "deleted_count": counts[2],
        "manual_validation_ids_pending": review.manual_validation_ids_pending,
        "human_git_handoff_requirement_satisfied": decision
        is GitHandoffDecision.APPROVED,
        "Git_commands_executed": 0,
        "staging_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "automatic_cleanup_authorized": False,
        "automatic_rollback_authorized": False,
        "automatic_staging_authorized": False,
        "automatic_commit_authorized": False,
        "automatic_push_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    base["handoff_id"] = _handoff_id(base)
    result = GitHandoffResult(
        **base,
        result_SHA256=_digest_from_record(RESULT_DIGEST_ALGORITHM, base),
    )
    validate_human_git_handoff_result(result)
    return result


def validate_human_git_handoff_result(result: GitHandoffResult) -> None:
    """Validate one immutable P17.7 human Git handoff result."""

    try:
        validated = GitHandoffResult.model_validate(result.model_dump(mode="json"))
    except AttributeError as exc:
        raise HumanGitHandoffValidationError(
            "result must be a GitHandoffResult"
        ) from exc
    except ValueError as exc:
        raise HumanGitHandoffValidationError(
            "invalid human Git handoff result"
        ) from exc
    try:
        _validate_result_integrity(validated, error_type=HumanGitHandoffIntegrityError)
    except HumanGitHandoffError:
        raise
    except ValueError as exc:
        raise HumanGitHandoffIntegrityError(
            "result integrity validation failed"
        ) from exc


def render_human_git_handoff_powershell(package: GitHandoffPackage) -> str:
    """Render bounded PowerShell handoff text without persisting or executing it."""

    try:
        validated = GitHandoffPackage.model_validate(package.model_dump(mode="json"))
    except ValueError as exc:
        raise HumanGitHandoffValidationError("invalid handoff package") from exc
    candidate_lines = tuple(
        "    @{ Id = '"
        + _ps_escape(candidate.candidate_id)
        + "'; RelativePath = '"
        + _ps_escape(candidate.relative_path)
        + "'; Status = '"
        + candidate.status.value
        + "' }"
        for candidate in validated.candidates
    )
    path_array = ", ".join(
        "'" + _ps_escape(candidate.relative_path) + "'"
        for candidate in validated.candidates
    )
    lines = [
        "$ErrorActionPreference = 'Stop'",
        "$Repo = '" + _ps_escape(validated.repository_display_path) + "'",
        "$BranchName = '" + _ps_escape(validated.branch_name) + "'",
        "$ExpectedParent = '" + validated.expected_parent_commit + "'",
        "$RemoteName = '" + validated.remote_name + "'",
        "$CommitMessage = '" + _ps_escape(validated.commit_message) + "'",
        "$Candidates = @(",
        *candidate_lines,
        ")",
        "Set-Location -LiteralPath $Repo",
        "$CurrentBranch = (git rev-parse --abbrev-ref HEAD).Trim()",
        "if ($CurrentBranch -ne $BranchName) { throw 'branch mismatch' }",
        "$CurrentParent = (git rev-parse HEAD).Trim()",
        "if ($CurrentParent -ne $ExpectedParent) { throw 'parent mismatch' }",
        "$RemoteParent = (git rev-parse origin/$BranchName).Trim()",
        "if ($RemoteParent -ne $ExpectedParent) { throw 'remote parent mismatch' }",
        "if ((git diff --cached --name-only).Count -ne 0) { throw 'index not empty' }",
        "git diff --check",
        "$ExpectedPaths = @(" + path_array + ") | Sort-Object",
        "$ObservedPaths = @(git diff --name-only -- $ExpectedPaths) | Sort-Object",
        "if (@($ObservedPaths).Count -ne @($ExpectedPaths).Count) { throw 'candidate count mismatch' }",
        "for ($i = 0; $i -lt $ExpectedPaths.Count; $i++) { if ($ObservedPaths[$i] -ne $ExpectedPaths[$i]) { throw 'candidate path mismatch' } }",
        "foreach ($Candidate in $Candidates) {",
        "    $RelativePath = $Candidate.RelativePath",
        "    git add -- $RelativePath",
        "}",
        "git diff --staged --check",
        "$StagedPaths = @(git diff --staged --name-only) | Sort-Object",
        "if (@($StagedPaths).Count -ne @($ExpectedPaths).Count) { throw 'staged count mismatch' }",
        "for ($i = 0; $i -lt $ExpectedPaths.Count; $i++) { if ($StagedPaths[$i] -ne $ExpectedPaths[$i]) { throw 'staged path mismatch' } }",
        "if ((git status --short --untracked-files=all | Where-Object { $_ -notmatch '^[MARCD]  ' }).Count -ne 0) { throw 'unstaged remainder present' }",
        "git diff --staged --stat",
        "git diff --staged --name-status -- $ExpectedPaths",
        "git commit -m $CommitMessage",
        "git push origin $BranchName",
        "$NewHead = (git rev-parse HEAD).Trim()",
        "$NewParent = (git rev-parse HEAD^).Trim()",
        "if ($NewParent -ne $ExpectedParent) { throw 'post-commit parent mismatch' }",
        "if ((git log -1 --format=%s).Trim() -ne $CommitMessage) { throw 'commit message mismatch' }",
        "$CommittedPaths = @(git diff-tree --no-commit-id --name-only --no-renames -r $NewHead) | Sort-Object",
        "if (@($CommittedPaths).Count -ne @($ExpectedPaths).Count) { throw 'commit path count mismatch' }",
        "for ($i = 0; $i -lt $ExpectedPaths.Count; $i++) { if ($CommittedPaths[$i] -ne $ExpectedPaths[$i]) { throw 'commit path mismatch' } }",
        "$RemoteHead = (git rev-parse origin/$BranchName).Trim()",
        "if ($RemoteHead -ne $NewHead) { throw 'remote mismatch' }",
        "if ((git status --short --untracked-files=all).Count -ne 0) { throw 'worktree not clean' }",
        "python 10_scripts/governance/pepper_baseline_integrity.py --repo-root . --product-root 2_products/pepper-agent --mode all --format json",
    ]
    rendered = "\n".join(lines) + "\n"
    _reject_forbidden_rendered_powershell(rendered)
    if len(rendered) > _RENDERED_POWERSHELL_MAX_LENGTH:
        raise HumanGitHandoffPolicyError("rendered PowerShell exceeds bounded length")
    return rendered


def _validated_review_result(
    review_result: DiffArtifactReviewResult,
) -> DiffArtifactReviewResult:
    try:
        validated = DiffArtifactReviewResult.model_validate(
            review_result.model_dump(mode="json")
        )
        validate_diff_artifact_review_result(validated)
        return validated
    except AttributeError as exc:
        raise HumanGitHandoffInputError(
            "review result must be a DiffArtifactReviewResult"
        ) from exc
    except ValueError as exc:
        raise HumanGitHandoffIntegrityError("review result integrity failed") from exc


def _require_review_extractable(review: DiffArtifactReviewResult, error_type) -> None:
    if review.state is not AggregateReviewState.COMPLETED:
        raise error_type("review must be completed")
    if review.diff_artifact_review_requirement_satisfied is not True:
        raise error_type("review requirement must be satisfied")
    if review.diff_verdict is DiffReviewVerdict.BLOCKED:
        raise error_type("blocked diff verdict cannot be handed off")
    if review.artifact_verdict is ArtifactReviewVerdict.BLOCKED:
        raise error_type("blocked artifact verdict cannot be handed off")
    if review.human_git_handoff_ready is not False:
        raise error_type("review already claims Git handoff readiness")
    if (
        review.automatic_cleanup_authorized
        or review.automatic_rollback_authorized
        or review.automatic_staging_authorized
    ):
        raise error_type("review grants forbidden automatic authority")
    if review.provider_dispatch_count != 0 or review.model_inference_count != 0:
        raise error_type("review has provider or model authority")
    if any(
        finding.severity is ReviewFindingSeverity.BLOCKING
        for finding in review.findings
    ):
        raise error_type("blocking findings cannot be handed off")
    for path in review.observed_paths:
        if path.status not in _ALLOWED_CANDIDATE_REVIEW_STATUSES:
            raise error_type("reviewed path status cannot be handed off")


def _candidate_status(observed: ReviewObservedPath) -> GitHandoffPathStatus:
    if observed.status in {
        ReviewObservedPathStatus.ADDED,
        ReviewObservedPathStatus.UNTRACKED,
    }:
        return GitHandoffPathStatus.ADDED
    if observed.status is ReviewObservedPathStatus.MODIFIED:
        return GitHandoffPathStatus.MODIFIED
    if observed.status is ReviewObservedPathStatus.DELETED:
        return GitHandoffPathStatus.DELETED
    raise HumanGitHandoffPolicyError("unsupported reviewed path status")


def _validate_candidate_collection(
    candidates: tuple[GitHandoffCandidate, ...], *, error_type=ValueError
) -> None:
    ids = tuple(candidate.candidate_id for candidate in candidates)
    expected_ids = tuple(f"GHCP-{index:03d}" for index in range(1, len(candidates) + 1))
    if ids != expected_ids:
        raise error_type("candidate IDs must be contiguous")
    paths = tuple(candidate.relative_path for candidate in candidates)
    if paths != tuple(sorted(paths)):
        raise error_type("candidates must be sorted by path")
    if len(paths) != len(frozenset(paths)):
        raise error_type("candidate paths must be unique")
    for candidate in candidates:
        if candidate.candidate_SHA256 != _candidate_digest(candidate):
            raise error_type("candidate digest mismatch")


def _validate_step_collection(
    steps: tuple[GitHandoffVerificationStep, ...], *, error_type=ValueError
) -> None:
    required = tuple(kind for kind in GitHandoffVerificationKind)
    if tuple(step.kind for step in steps) != required:
        raise error_type("verification steps must contain each required phase")
    for index, step in enumerate(steps, start=1):
        if step.order != index or step.step_id != f"GHVS-{index:03d}":
            raise error_type("verification steps must be contiguous")
        if step.step_SHA256 != _verification_step_digest(step):
            raise error_type("verification step digest mismatch")


def _validate_command_collection(
    commands: tuple[GitHandoffCommand, ...], *, error_type=ValueError
) -> None:
    for index, command in enumerate(commands, start=1):
        if command.order != index or command.command_id != f"GHCM-{index:03d}":
            raise error_type("commands must be contiguous")
        if command.automatic_execution_authorized is not False:
            raise error_type("commands must not authorize automatic execution")
        if command.command_SHA256 != _command_digest(command):
            raise error_type("command digest mismatch")
    if not any(
        command.kind is GitHandoffCommandKind.SET_LOCATION for command in commands
    ):
        raise error_type("command plan requires repository location")
    if not any(command.kind is GitHandoffCommandKind.COMMIT for command in commands):
        raise error_type("command plan requires commit command")
    if not any(command.kind is GitHandoffCommandKind.PUSH for command in commands):
        raise error_type("command plan requires push command")
    if not any(command.kind is GitHandoffCommandKind.INTEGRITY for command in commands):
        raise error_type("command plan requires committed integrity command")


def _validate_argv_tokens(argv: tuple[str, ...]) -> None:
    for token in argv:
        if not token:
            raise ValueError("argv tokens must be nonempty")
        if _contains_control(token) or _ANSI_PATTERN.search(token):
            raise ValueError("argv tokens must not contain control characters")
        if _contains_credential_marker(token):
            raise ValueError("argv tokens must not contain credentials")
        if any(character in token for character in ("*", "?", "[", "]")):
            raise ValueError("argv tokens must not contain wildcards")
        if token in {"|", ">", "<", "&&", ";"}:
            raise ValueError("argv must not contain shell operators")
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", token):
            raise ValueError("argv must not contain environment assignments")


def _validate_command_shape(command: GitHandoffCommand) -> None:
    argv = command.argv
    if command.kind is GitHandoffCommandKind.SET_LOCATION:
        if len(argv) != 2 or argv[0] != "Set-Location":
            raise ValueError("set-location command shape invalid")
        return
    if argv[0] == "git":
        if len(argv) < 2:
            raise ValueError("git command requires a verb")
        verb = argv[1]
        if verb in _FORBIDDEN_GIT_VERBS:
            raise ValueError("forbidden Git command verb")
        if verb == "add":
            if command.kind is not GitHandoffCommandKind.STAGE_PATH:
                raise ValueError("git add is only allowed for exact stage commands")
            if len(argv) != 4 or argv[2] != "--":
                raise ValueError("git add must use exact path separator")
            if argv[3] in {".", "-A", "--all", "-f"}:
                raise ValueError("wildcard or force staging is forbidden")
            _validate_relative_path(argv[3])
        elif verb == "commit":
            if command.kind is not GitHandoffCommandKind.COMMIT:
                raise ValueError("git commit command kind mismatch")
            if "-a" in argv or "--amend" in argv:
                raise ValueError("commit amend or all is forbidden")
            if len(argv) != 4 or argv[2] != "-m":
                raise ValueError("commit must use exact message")
            _validate_commit_message(argv[3])
        elif verb == "push":
            if command.kind is not GitHandoffCommandKind.PUSH:
                raise ValueError("git push command kind mismatch")
            if any(token in {"--force", "-f", "--force-with-lease"} for token in argv):
                raise ValueError("force push is forbidden")
            if len(argv) != 4 or argv[2] != "origin":
                raise ValueError("push must target exact origin branch")
            _validate_branch_name(argv[3])
        elif verb == "diff":
            if command.kind not in {
                GitHandoffCommandKind.DIFF_CHECK,
                GitHandoffCommandKind.DIFF_STAT,
                GitHandoffCommandKind.DIFF_PATHS,
            }:
                raise ValueError("git diff command kind mismatch")
        elif verb == "status":
            if command.kind is not GitHandoffCommandKind.STATUS:
                raise ValueError("git status command kind mismatch")
        elif verb in {"rev-parse", "log", "diff-tree"}:
            if command.kind is not GitHandoffCommandKind.VERIFY:
                raise ValueError("verification command kind mismatch")
        else:
            raise ValueError("unapproved Git command shape")
    elif argv[0] == "python":
        if command.kind is not GitHandoffCommandKind.INTEGRITY:
            raise ValueError("python command is only allowed for integrity")
        if tuple(argv) != _integrity_argv():
            raise ValueError("integrity command shape invalid")
    elif argv[0] == "verify":
        if command.kind is not GitHandoffCommandKind.VERIFY:
            raise ValueError("verify pseudo-command kind mismatch")
    else:
        raise ValueError("unapproved command family")


def _validate_request_bindings(request: GitHandoffRequest, error_type) -> None:
    try:
        validate_work_packet(request.compilation_result.work_packet)
        validate_workspace_allocation(request.allocation_result.allocation)
        validate_tool_permission_profile(request.profile_result.profile)
        validate_outcome_envelope(request.outcome_envelope)
        validate_diff_artifact_review_result(request.diff_artifact_review_result)
    except ValueError as exc:
        raise error_type("prerequisite integrity validation failed") from exc
    packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    outcome = request.outcome_envelope
    selected = _selected_outcome(outcome)
    review = request.diff_artifact_review_result
    approval = request.approval
    if allocation.work_packet_id != packet.work_packet_id:
        raise error_type("WorkPacket to allocation binding mismatch")
    if allocation.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("WorkPacket digest to allocation binding mismatch")
    if profile.work_packet_id != packet.work_packet_id:
        raise error_type("WorkPacket to profile binding mismatch")
    if profile.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("WorkPacket digest to profile binding mismatch")
    if profile.allocation_id != allocation.allocation_id:
        raise error_type("allocation to profile binding mismatch")
    if profile.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("allocation digest to profile binding mismatch")
    if selected.work_packet_id != packet.work_packet_id:
        raise error_type("WorkPacket to outcome binding mismatch")
    if selected.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("WorkPacket digest to outcome binding mismatch")
    if selected.allocation_id != allocation.allocation_id:
        raise error_type("allocation to outcome binding mismatch")
    if selected.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("allocation digest to outcome binding mismatch")
    if selected.profile_id != profile.profile_id:
        raise error_type("profile to outcome binding mismatch")
    if selected.profile_SHA256 != profile.profile_SHA256:
        raise error_type("profile digest to outcome binding mismatch")
    if review.work_packet_id != packet.work_packet_id:
        raise error_type("WorkPacket to review binding mismatch")
    if review.work_packet_SHA256 != packet.work_packet_SHA256:
        raise error_type("WorkPacket digest to review binding mismatch")
    if review.allocation_id != allocation.allocation_id:
        raise error_type("allocation to review binding mismatch")
    if review.allocation_SHA256 != allocation.allocation_SHA256:
        raise error_type("allocation digest to review binding mismatch")
    if review.profile_id != profile.profile_id:
        raise error_type("profile to review binding mismatch")
    if review.profile_SHA256 != profile.profile_SHA256:
        raise error_type("profile digest to review binding mismatch")
    if review.outcome_SHA256 != outcome.envelope_SHA256:
        raise error_type("outcome to review binding mismatch")
    if approval.review_id != review.review_id:
        raise error_type("approval to review ID mismatch")
    if approval.review_SHA256 != review.result_SHA256:
        raise error_type("approval to review digest mismatch")
    if approval.branch_name != allocation.repository_identity.workspace_branch:
        raise error_type("approval branch binding mismatch")
    if approval.expected_parent_commit != allocation.repository_identity.source_commit:
        raise error_type("approval parent binding mismatch")
    if approval.remote_name != "origin":
        raise error_type("approval remote binding mismatch")
    if outcome.result_envelopes_ready is not True:
        raise error_type("outcome result envelopes are not ready")
    _require_review_extractable(review, error_type=error_type)


def _validate_request_approval(request: GitHandoffRequest, error_type) -> None:
    candidates = build_git_handoff_candidates(request.diff_artifact_review_result)
    expected_candidate_ids = tuple(candidate.candidate_id for candidate in candidates)
    if request.approval.accepted_candidate_ids != expected_candidate_ids:
        raise error_type("approval candidate set mismatch")
    blocking = tuple(
        finding.finding_id
        for finding in request.diff_artifact_review_result.findings
        if finding.severity is ReviewFindingSeverity.BLOCKING
    )
    if blocking:
        raise error_type("blocking findings cannot be accepted")
    warning_ids = tuple(
        finding.finding_id
        for finding in request.diff_artifact_review_result.findings
        if finding.severity is ReviewFindingSeverity.WARNING
        or finding.code is ReviewFindingCode.ARTIFACT_REQUIRES_REVIEW
    )
    if (
        request.diff_artifact_review_result.diff_verdict
        is DiffReviewVerdict.REQUIRES_HUMAN_REVIEW
        or request.diff_artifact_review_result.artifact_verdict
        is ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    ):
        if request.approval.accepted_finding_ids != warning_ids:
            raise error_type("warning findings must be accepted exactly")
    elif request.approval.accepted_finding_ids:
        raise error_type("accepted finding IDs must be empty for accepted review")


def _derive_decision(
    request: GitHandoffRequest, candidates: tuple[GitHandoffCandidate, ...]
) -> GitHandoffDecision:
    if request.approval.decision is GitHandoffDecision.REJECTED:
        return GitHandoffDecision.REJECTED
    expected_candidate_ids = tuple(candidate.candidate_id for candidate in candidates)
    if request.approval.accepted_candidate_ids != expected_candidate_ids:
        return GitHandoffDecision.REJECTED
    warning_ids = tuple(
        finding.finding_id
        for finding in request.diff_artifact_review_result.findings
        if finding.severity is ReviewFindingSeverity.WARNING
    )
    if request.approval.accepted_finding_ids not in {(), warning_ids}:
        return GitHandoffDecision.REJECTED
    return GitHandoffDecision.APPROVED


def _build_verification_steps() -> tuple[GitHandoffVerificationStep, ...]:
    specs = (
        (
            GitHandoffVerificationKind.PRE_STAGING,
            "Verify branch, parent, remote and empty index before staging.",
        ),
        (
            GitHandoffVerificationKind.CANDIDATE_SET,
            "Verify unstaged candidate paths equal the reviewed candidate set.",
        ),
        (
            GitHandoffVerificationKind.STAGED_INDEX,
            "Verify staged paths and staged diff checks after exact staging.",
        ),
        (
            GitHandoffVerificationKind.POST_COMMIT,
            "Verify commit parent, message, file set and status counts.",
        ),
        (
            GitHandoffVerificationKind.POST_PUSH,
            "Verify remote branch head equals the new local commit.",
        ),
        (
            GitHandoffVerificationKind.COMMITTED_INTEGRITY,
            "Run committed Pepper integrity after human commit and push.",
        ),
    )
    steps: list[GitHandoffVerificationStep] = []
    for index, (kind, expected) in enumerate(specs, start=1):
        data = {
            "step_id": f"GHVS-{index:03d}",
            "kind": kind,
            "order": index,
            "title": kind.value.replace("_", " ").title(),
            "expected_condition": expected,
            "blocking": True,
        }
        steps.append(
            GitHandoffVerificationStep(
                **data,
                step_SHA256=_digest_from_record(
                    VERIFICATION_STEP_DIGEST_ALGORITHM, data
                ),
            )
        )
    return tuple(steps)


def _command(
    commands: list[GitHandoffCommand],
    kind: GitHandoffCommandKind,
    argv: tuple[str, ...],
    display_text: str,
) -> None:
    data = {
        "command_id": f"GHCM-{len(commands) + 1:03d}",
        "kind": kind,
        "order": len(commands) + 1,
        "argv": argv,
        "display_text": display_text,
        "human_execution_required": True,
        "automatic_execution_authorized": False,
    }
    commands.append(
        GitHandoffCommand(
            **data,
            command_SHA256=_digest_from_record(COMMAND_DIGEST_ALGORITHM, data),
        )
    )


def _build_commands(
    *,
    repository_display_path: str,
    branch_name: str,
    remote_name: str,
    expected_parent_commit: str,
    commit_message: str,
    candidates: tuple[GitHandoffCandidate, ...],
) -> tuple[GitHandoffCommand, ...]:
    commands: list[GitHandoffCommand] = []
    candidate_paths = tuple(candidate.relative_path for candidate in candidates)
    _command(
        commands,
        GitHandoffCommandKind.SET_LOCATION,
        ("Set-Location", repository_display_path),
        "Set repository location for human execution.",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        ("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "Verify current branch equals " + branch_name + ".",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        ("git", "rev-parse", "HEAD"),
        "Verify HEAD equals expected parent " + expected_parent_commit + ".",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        ("git", "rev-parse", remote_name + "/" + branch_name),
        "Verify remote parent equals expected parent.",
    )
    _command(
        commands,
        GitHandoffCommandKind.DIFF_PATHS,
        ("git", "diff", "--cached", "--name-only"),
        "Verify the index is empty before staging.",
    )
    _command(
        commands,
        GitHandoffCommandKind.DIFF_CHECK,
        ("git", "diff", "--check"),
        "Verify unstaged diff has no whitespace errors.",
    )
    _command(
        commands,
        GitHandoffCommandKind.DIFF_PATHS,
        ("git", "diff", "--name-only", "--", *candidate_paths),
        "Verify unstaged candidate paths equal reviewed candidates.",
    )
    for candidate in candidates:
        _command(
            commands,
            GitHandoffCommandKind.STAGE_PATH,
            ("git", "add", "--", candidate.relative_path),
            "Stage one exact reviewed candidate path.",
        )
    _command(
        commands,
        GitHandoffCommandKind.DIFF_CHECK,
        ("git", "diff", "--staged", "--check"),
        "Verify staged diff has no whitespace errors.",
    )
    _command(
        commands,
        GitHandoffCommandKind.DIFF_STAT,
        ("git", "diff", "--staged", "--stat"),
        "Show staged diff stat for human review.",
    )
    _command(
        commands,
        GitHandoffCommandKind.DIFF_PATHS,
        ("git", "diff", "--staged", "--name-status", "--", *candidate_paths),
        "Verify staged candidate set and statuses.",
    )
    _command(
        commands,
        GitHandoffCommandKind.STATUS,
        ("git", "status", "--short"),
        "Verify no unstaged or untracked remainder is present.",
    )
    _command(
        commands,
        GitHandoffCommandKind.COMMIT,
        ("git", "commit", "-m", commit_message),
        "Create the exact reviewed P17.7 commit.",
    )
    _command(
        commands,
        GitHandoffCommandKind.PUSH,
        ("git", "push", remote_name, branch_name),
        "Push the exact branch to origin for human-reviewed P17.7.",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        ("git", "rev-parse", "HEAD^"),
        "Verify new commit parent equals expected parent.",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        ("git", "log", "-1", "--format=%s"),
        "Verify new commit message equals approved message.",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        (
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-status",
            "--no-renames",
            "-r",
            "HEAD",
        ),
        "Verify committed file set and status counts.",
    )
    _command(
        commands,
        GitHandoffCommandKind.VERIFY,
        ("git", "rev-parse", remote_name + "/" + branch_name),
        "Verify remote branch matches local human commit.",
    )
    _command(
        commands,
        GitHandoffCommandKind.STATUS,
        ("git", "status", "--short"),
        "Verify the worktree is clean after commit and push.",
    )
    _command(
        commands,
        GitHandoffCommandKind.INTEGRITY,
        _integrity_argv(),
        "Run committed Pepper integrity after human Git handoff.",
    )
    return tuple(commands)


def _integrity_argv() -> tuple[str, ...]:
    return (
        "python",
        "10_scripts/governance/pepper_baseline_integrity.py",
        "--repo-root",
        ".",
        "--product-root",
        "2_products/pepper-agent",
        "--mode",
        "all",
        "--format",
        "json",
    )


def _build_post_commit_expectation(
    *,
    candidates: tuple[GitHandoffCandidate, ...],
    expected_parent_commit: str,
    expected_branch: str,
    expected_remote: str,
    expected_commit_message: str,
) -> GitHandoffPostCommitExpectation:
    counts = _candidate_counts(candidates)
    data = {
        "expected_parent_commit": expected_parent_commit,
        "expected_branch": expected_branch,
        "expected_remote": expected_remote,
        "expected_commit_message": expected_commit_message,
        "expected_file_count": len(candidates),
        "expected_added_count": counts[0],
        "expected_modified_count": counts[1],
        "expected_deleted_count": counts[2],
        "expected_candidate_paths": tuple(
            candidate.relative_path for candidate in candidates
        ),
        "expected_worktree_clean": True,
        "expected_remote_match": True,
        "expected_integrity_file_count": POST_COMMIT_PEPPER_FILE_COUNT,
    }
    return GitHandoffPostCommitExpectation(
        **data,
        expectation_SHA256=_digest_from_record(
            POST_COMMIT_EXPECTATION_DIGEST_ALGORITHM, data
        ),
    )


def _candidate_counts(
    candidates: tuple[GitHandoffCandidate, ...],
) -> tuple[int, int, int]:
    added = sum(
        1 for candidate in candidates if candidate.status is GitHandoffPathStatus.ADDED
    )
    modified = sum(
        1
        for candidate in candidates
        if candidate.status is GitHandoffPathStatus.MODIFIED
    )
    deleted = sum(
        1
        for candidate in candidates
        if candidate.status is GitHandoffPathStatus.DELETED
    )
    return added, modified, deleted


def _selected_outcome(outcome: OutcomeEnvelope):
    if outcome.envelope_kind is OutcomeEnvelopeKind.RESULT:
        return outcome.result_envelope
    if outcome.envelope_kind is OutcomeEnvelopeKind.FAILURE:
        return outcome.failure_envelope
    return outcome.cancellation_envelope


def _validate_result_integrity(result: GitHandoffResult, error_type) -> None:
    _validate_candidate_collection(result.package.candidates, error_type=error_type)
    _validate_step_collection(result.package.verification_steps, error_type=error_type)
    _validate_command_collection(result.package.commands, error_type=error_type)
    counts = _candidate_counts(result.package.candidates)
    if result.candidate_count != len(result.package.candidates):
        raise error_type("candidate count mismatch")
    if (result.added_count, result.modified_count, result.deleted_count) != counts:
        raise error_type("candidate status counts mismatch")
    expected_decision = (
        GitHandoffDecision.APPROVED
        if result.state is GitHandoffState.COMPLETED
        else GitHandoffDecision.REJECTED
    )
    if result.decision is not expected_decision:
        raise error_type("decision and state mismatch")
    if result.human_git_handoff_requirement_satisfied != (
        result.decision is GitHandoffDecision.APPROVED
    ):
        raise error_type("handoff readiness mismatch")
    if result.Git_commands_executed != 0:
        raise error_type("Git command execution counter must remain zero")
    if (
        result.staging_performed
        or result.commit_performed
        or result.push_performed
        or result.automatic_cleanup_authorized
        or result.automatic_rollback_authorized
        or result.automatic_staging_authorized
        or result.automatic_commit_authorized
        or result.automatic_push_authorized
    ):
        raise error_type("result grants forbidden Git authority")
    if result.provider_dispatch_count != 0 or result.model_inference_count != 0:
        raise error_type("result has provider or model authority")
    if result.rendered_powershell_SHA256 != _digest_text(
        POWERSHELL_DIGEST_ALGORITHM,
        render_human_git_handoff_powershell(result.package),
    ):
        raise error_type("rendered PowerShell digest mismatch")
    if result.handoff_id != _handoff_id(
        result.model_dump(mode="python", exclude={"result_SHA256", "handoff_id"})
    ):
        raise error_type("handoff ID mismatch")
    if result.result_SHA256 != _result_digest(result):
        raise error_type("result digest mismatch")


def _package_id(package: GitHandoffPackage) -> str:
    return _package_id_from_record(
        package.model_dump(mode="python", exclude={"package_SHA256", "package_id"})
    )


def _package_id_from_record(record) -> str:
    ticket, revision = _ticket_revision_from_package_record(record)
    digest = _digest_from_record(HANDOFF_ID_DIGEST_ALGORITHM, record)[:12]
    return f"GHP-{ticket}-R{revision:04d}-{digest}"


def _handoff_id(record) -> str:
    package = record["package"]
    ticket, revision = _ticket_revision_from_package_record(
        package.model_dump(mode="python") if isinstance(package, BaseModel) else package
    )
    digest = _digest_from_record(HANDOFF_ID_DIGEST_ALGORITHM, record)[:12]
    return f"HGR-{ticket}-R{revision:04d}-{digest}"


def _ticket_revision_from_package_record(record) -> tuple[str, int]:
    candidates = record.get("candidates", ())
    if candidates:
        first = candidates[0]
        source = (
            first.source_observation_id
            if isinstance(first, BaseModel)
            else first.get("source_observation_id", "P17-7")
        )
    else:
        source = "P17-7"
    identity = str(record.get("branch_name", source)).upper()
    ticket = _normalize_ticket_id(identity)
    revision = 1
    package_parent = str(record.get("expected_parent_commit", ""))
    revision_match = _WORK_PACKET_REVISION_PATTERN.search(package_parent)
    if revision_match is not None:
        revision = int(revision_match.group("revision"))
    return ticket, revision


def _normalize_ticket_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")
    cleaned = re.sub(r"-+", "-", cleaned)
    if cleaned.startswith("P17-GOVERNED-WORKPACKET-EXECUTION-MVP"):
        return "P17-7"
    return cleaned or "P17-7"


def _candidate_digest(candidate: GitHandoffCandidate) -> str:
    return _digest_from_record(
        CANDIDATE_DIGEST_ALGORITHM,
        candidate.model_dump(mode="python", exclude={"candidate_SHA256"}),
    )


def _approval_digest(approval: GitHandoffApproval) -> str:
    return _digest_from_record(
        APPROVAL_DIGEST_ALGORITHM,
        approval.model_dump(mode="python", exclude={"approval_SHA256"}),
    )


def _verification_step_digest(step: GitHandoffVerificationStep) -> str:
    return _digest_from_record(
        VERIFICATION_STEP_DIGEST_ALGORITHM,
        step.model_dump(mode="python", exclude={"step_SHA256"}),
    )


def _command_digest(command: GitHandoffCommand) -> str:
    return _digest_from_record(
        COMMAND_DIGEST_ALGORITHM,
        command.model_dump(mode="python", exclude={"command_SHA256"}),
    )


def _post_commit_expectation_digest(
    expectation: GitHandoffPostCommitExpectation,
) -> str:
    return _digest_from_record(
        POST_COMMIT_EXPECTATION_DIGEST_ALGORITHM,
        expectation.model_dump(mode="python", exclude={"expectation_SHA256"}),
    )


def _package_digest(package: GitHandoffPackage) -> str:
    return _digest_from_record(
        PACKAGE_DIGEST_ALGORITHM,
        package.model_dump(mode="python", exclude={"package_SHA256"}),
    )


def _result_digest(result: GitHandoffResult) -> str:
    return _digest_from_record(
        RESULT_DIGEST_ALGORITHM,
        result.model_dump(mode="python", exclude={"result_SHA256"}),
    )


def _digest_text(algorithm: str, value: str) -> str:
    payload = {"algorithm": algorithm, "text": value}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _digest_from_record(algorithm: str, record) -> str:
    payload = {"algorithm": algorithm, "record": _canonicalize(record)}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _canonicalize(value):
    if isinstance(value, BaseModel):
        return _canonicalize(value.model_dump(mode="python"))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_canonicalize(item) for item in value]
    if isinstance(value, list):
        return [_canonicalize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _canonicalize(item) for key, item in sorted(value.items())}
    return value


def _ps_escape(value: str) -> str:
    return value.replace("'", "''")


def _reject_forbidden_rendered_powershell(rendered: str) -> None:
    lowered = rendered.lower()
    forbidden = (
        "git add .",
        "git add -a",
        "git add -f",
        "git add --all",
        "git push --force",
        "git push -f",
        "git commit --amend",
        "invoke-expression",
        "start-process",
        "encodedcommand",
        "git reset",
        "git clean",
        "git stash",
        "git switch",
        "git checkout",
        "git merge",
        "git rebase",
        "git worktree",
        "git tag",
        "cmd.exe",
        "powershell.exe",
        "pwsh",
        "bash",
        " sh ",
        " eval",
        " exec",
    )
    for token in forbidden:
        if token in lowered:
            raise HumanGitHandoffPolicyError(
                "rendered PowerShell contains forbidden token"
            )


def _approval_digest_from_record(record) -> str:
    return _digest_from_record(APPROVAL_DIGEST_ALGORITHM, record)


def _candidate_digest_from_record(record) -> str:
    return _digest_from_record(CANDIDATE_DIGEST_ALGORITHM, record)


def _command_digest_from_record(record) -> str:
    return _digest_from_record(COMMAND_DIGEST_ALGORITHM, record)


def _post_commit_expectation_digest_from_record(record) -> str:
    return _digest_from_record(POST_COMMIT_EXPECTATION_DIGEST_ALGORITHM, record)


def _verification_step_digest_from_record(record) -> str:
    return _digest_from_record(VERIFICATION_STEP_DIGEST_ALGORITHM, record)


def _result_digest_from_record(record) -> str:
    return _digest_from_record(RESULT_DIGEST_ALGORITHM, record)
