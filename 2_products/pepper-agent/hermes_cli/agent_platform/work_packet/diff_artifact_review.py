"""Deterministic human-observed diff and artifact review contracts.

P17.6 classifies supplied workspace observations against the compiled
WorkPacket mutation policy. It does not inspect the filesystem, invoke Git,
launch subprocesses, clean workspaces, roll back changes, or stage files.
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
from hermes_cli.agent_platform.work_packet.outcome_envelopes import (
    OutcomeEnvelope,
    OutcomeEnvelopeKind,
    validate_outcome_envelope,
)
from hermes_cli.agent_platform.work_packet.tool_permissions import (
    ToolPermissionOperation,
    ToolPermissionProfileResult,
    validate_tool_permission_profile,
)
from hermes_cli.agent_platform.work_packet.workspace_allocator import (
    WorkspaceAllocationResult,
    WorkspaceRepositoryIdentity,
    validate_workspace_allocation,
)


DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION = 1
DIFF_ARTIFACT_REVIEW_POLICY_ID = (
    "pepper-human-observed-deterministic-diff-artifact-review-v1"
)

EXPECTED_MUTATION_DIGEST_ALGORITHM = "agent-platform-review-expected-mutation-sha256-v1"
OBSERVED_PATH_DIGEST_ALGORITHM = "agent-platform-review-observed-path-sha256-v1"
DIFF_STAT_DIGEST_ALGORITHM = "agent-platform-review-diff-stat-sha256-v1"
ARTIFACT_DIGEST_ALGORITHM = "agent-platform-review-artifact-observation-sha256-v1"
FINDING_DIGEST_ALGORITHM = "agent-platform-review-finding-sha256-v1"
OBSERVATION_DIGEST_ALGORITHM = (
    "agent-platform-diff-artifact-review-observation-sha256-v1"
)
REVIEW_ID_DIGEST_ALGORITHM = "agent-platform-diff-artifact-review-id-sha256-v1"
RESULT_DIGEST_ALGORITHM = "agent-platform-diff-artifact-review-result-sha256-v1"

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_RELATIVE_ID_PATTERN = r"^[A-Z]+-[0-9]{3}$"
_REVIEW_ID_PATTERN = r"^DAR-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$"
_WINDOWS_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_ACTION_PATTERN = re.compile(
    r"^(?P<operation>create_file|modify_file|replace_file|delete_file)"
    r"(?::|\||\s+)"
    r"(?P<path>[^|\s][^|]*)"
    r"(?:\|(?P<kind>source|test|documentation|configuration|manifest|"
    r"generated|log|report|binary|cache|temporary|unknown))?$"
)
_PATH_SECRET_COMPONENTS = (
    "credentials",
    "secrets",
    "private_key",
    "id_rsa",
    "id_ed25519",
    "auth.json",
    "token.json",
)
_PROHIBITED_ARTIFACT_KINDS = ("cache", "temporary")
_REVIEW_REQUIRED_ARTIFACT_KINDS = (
    "generated",
    "log",
    "report",
    "binary",
    "unknown",
)
_ACCEPTABLE_ARTIFACT_KINDS = (
    "source",
    "test",
    "documentation",
    "configuration",
    "manifest",
)
_ALLOWED_ARTIFACT_ORIGINS = ("work_packet_declared", "human_declared")
_BLOCKING_FINDING_CODES = (
    "expected_path_missing",
    "unexpected_path_observed",
    "path_outside_workspace",
    "path_outside_repository",
    "git_metadata_path",
    "forbidden_path_component",
    "prohibited_artifact_kind",
    "unknown_artifact_origin",
    "artifact_unexpected",
    "hash_evidence_missing",
    "diff_summary_inconsistent",
    "outcome_not_terminal",
)
_SEVERITY_ORDER = ("blocking", "warning", "info")
_KIND_ORDER = (
    "source",
    "test",
    "documentation",
    "configuration",
    "manifest",
    "generated",
    "log",
    "report",
    "binary",
    "cache",
    "temporary",
    "unknown",
)

__all__ = (
    "DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION",
    "DIFF_ARTIFACT_REVIEW_POLICY_ID",
    "ReviewObservedPathStatus",
    "ReviewPathExpectation",
    "ReviewArtifactKind",
    "ReviewArtifactOrigin",
    "ReviewArtifactDisposition",
    "ReviewFindingSeverity",
    "ReviewFindingCode",
    "DiffReviewVerdict",
    "ArtifactReviewVerdict",
    "AggregateReviewState",
    "ReviewExpectedMutation",
    "ReviewObservedPath",
    "ReviewDiffStat",
    "ReviewArtifactObservation",
    "ReviewFinding",
    "DiffArtifactReviewObservation",
    "DiffArtifactReviewRequest",
    "DiffArtifactReviewResult",
    "DiffArtifactReviewError",
    "DiffArtifactReviewInputError",
    "DiffArtifactReviewIntegrityError",
    "DiffArtifactReviewPolicyError",
    "DiffArtifactReviewStateError",
    "DiffArtifactReviewValidationError",
    "build_review_expected_mutations",
    "build_diff_artifact_review",
    "validate_diff_artifact_review_result",
)


class DiffArtifactReviewError(ValueError):
    """Base error for P17.6 diff and artifact review failures."""


class DiffArtifactReviewInputError(DiffArtifactReviewError):
    """Raised when supplied review evidence is structurally invalid."""


class DiffArtifactReviewIntegrityError(DiffArtifactReviewError):
    """Raised when deterministic review digests fail validation."""


class DiffArtifactReviewPolicyError(DiffArtifactReviewError):
    """Raised when review evidence violates the P17.6 policy boundary."""


class DiffArtifactReviewStateError(DiffArtifactReviewError):
    """Raised when prerequisite state is incompatible with review."""


class DiffArtifactReviewValidationError(DiffArtifactReviewError):
    """Raised when a review result cannot be validated."""


class ReviewObservedPathStatus(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    RENAMED = "renamed"
    TYPE_CHANGED = "type_changed"
    UNMERGED = "unmerged"
    UNTRACKED = "untracked"


class ReviewPathExpectation(str, Enum):
    EXPECTED = "expected"
    UNEXPECTED = "unexpected"
    MISSING_EXPECTED = "missing_expected"


class ReviewArtifactKind(str, Enum):
    SOURCE = "source"
    TEST = "test"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    MANIFEST = "manifest"
    GENERATED = "generated"
    LOG = "log"
    REPORT = "report"
    BINARY = "binary"
    CACHE = "cache"
    TEMPORARY = "temporary"
    UNKNOWN = "unknown"


class ReviewArtifactOrigin(str, Enum):
    WORK_PACKET_DECLARED = "work_packet_declared"
    EXECUTION_PRODUCED = "execution_produced"
    VALIDATION_PRODUCED = "validation_produced"
    HUMAN_DECLARED = "human_declared"
    UNKNOWN = "unknown"


class ReviewArtifactDisposition(str, Enum):
    ACCEPTABLE = "acceptable"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"
    PROHIBITED = "prohibited"
    UNEXPECTED = "unexpected"


class ReviewFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class ReviewFindingCode(str, Enum):
    EXPECTED_PATH_OBSERVED = "expected_path_observed"
    EXPECTED_PATH_MISSING = "expected_path_missing"
    UNEXPECTED_PATH_OBSERVED = "unexpected_path_observed"
    PATH_OUTSIDE_WORKSPACE = "path_outside_workspace"
    PATH_OUTSIDE_REPOSITORY = "path_outside_repository"
    GIT_METADATA_PATH = "git_metadata_path"
    FORBIDDEN_PATH_COMPONENT = "forbidden_path_component"
    PROHIBITED_ARTIFACT_KIND = "prohibited_artifact_kind"
    UNKNOWN_ARTIFACT_ORIGIN = "unknown_artifact_origin"
    ARTIFACT_REQUIRES_REVIEW = "artifact_requires_review"
    ARTIFACT_UNEXPECTED = "artifact_unexpected"
    HASH_EVIDENCE_MISSING = "hash_evidence_missing"
    DIFF_SUMMARY_INCONSISTENT = "diff_summary_inconsistent"
    OUTCOME_NOT_TERMINAL = "outcome_not_terminal"


class DiffReviewVerdict(str, Enum):
    ACCEPTED = "accepted"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"
    BLOCKED = "blocked"


class ArtifactReviewVerdict(str, Enum):
    ACCEPTED = "accepted"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"
    BLOCKED = "blocked"


class AggregateReviewState(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _validate_public_text(value: str) -> str:
    _reject_nul(value)
    if any(character in value for character in ("\n", "\r")):
        raise ValueError("text must be single-line")
    if _ANSI_PATTERN.search(value):
        raise ValueError("text must not contain ANSI control sequences")
    lower = value.lower()
    if any(marker in lower for marker in ("access_token", "refresh_token")):
        raise ValueError("text must not contain credential-shaped values")
    if any(marker in lower for marker in ("authorization: bearer", "client_secret")):
        raise ValueError("text must not contain credential-shaped values")
    if any(
        marker in lower
        for marker in ("raw stdout", "raw stderr", "raw diff", "file content")
    ):
        raise ValueError("text must not contain raw runtime evidence")
    if "c:/users/" in lower or "c:\\users\\" in lower:
        raise ValueError("text must not contain personal absolute paths")
    return value


def _validate_relative_path(value: str) -> str:
    if value != value.strip():
        raise ValueError("path must not contain surrounding whitespace")
    if not value:
        raise ValueError("path must be nonempty")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
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


DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=_DIGEST_PATTERN),
]
BoundedIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=128),
    AfterValidator(_reject_nul),
]
ReviewIdentifier: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=8, max_length=24, pattern=_RELATIVE_ID_PATTERN),
]
ReviewRelativePath: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_relative_path),
]
BoundedPublicText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_public_text),
]
BoundedInvariantText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=192),
    AfterValidator(_validate_public_text),
]
GitCommitText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=40, max_length=40, pattern=r"^[a-f0-9]{40}$"),
]
ReviewIdText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=24, max_length=128, pattern=_REVIEW_ID_PATTERN),
]


class _ReviewModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )


class ReviewExpectedMutation(_ReviewModel):
    mutation_id: ReviewIdentifier
    relative_path: ReviewRelativePath
    allowed_statuses: tuple[ReviewObservedPathStatus, ...] = Field(min_length=1)
    artifact_expected: StrictBool
    expected_artifact_kind: ReviewArtifactKind | None
    source_action_id: BoundedIdentifier
    expectation_SHA256: DigestText

    @field_validator("allowed_statuses", mode="after")
    @classmethod
    def _validate_statuses(
        cls, value: tuple[ReviewObservedPathStatus, ...]
    ) -> tuple[ReviewObservedPathStatus, ...]:
        if len(value) != len(frozenset(value)):
            raise ValueError("allowed statuses must be unique")
        if value != tuple(sorted(value, key=lambda item: item.value)):
            raise ValueError("allowed statuses must be sorted")
        return value

    @model_validator(mode="after")
    def _validate_mutation(self) -> ReviewExpectedMutation:
        if self.artifact_expected and self.expected_artifact_kind is None:
            raise ValueError("expected artifact kind is required")
        if not self.artifact_expected and self.expected_artifact_kind is not None:
            raise ValueError("unexpected artifact kind requires artifact expectation")
        if self.expectation_SHA256 != _expected_mutation_digest(self):
            raise ValueError("expected mutation digest mismatch")
        return self


class ReviewObservedPath(_ReviewModel):
    observation_id: ReviewIdentifier
    relative_path: ReviewRelativePath
    status: ReviewObservedPathStatus
    tracked: StrictBool
    staged: StrictBool = False
    bytes_after: int | None = Field(default=None, ge=0, strict=True)
    content_SHA256: DigestText | None = None
    artifact_declared: StrictBool
    observation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_observed_path(self) -> ReviewObservedPath:
        if self.staged:
            raise ValueError("observed paths must not be staged")
        if self.status is ReviewObservedPathStatus.UNTRACKED:
            if self.tracked:
                raise ValueError("untracked status requires tracked=false")
            if not self.artifact_declared:
                raise ValueError("untracked paths require explicit artifact posture")
        elif not self.tracked:
            raise ValueError("tracked status requires tracked=true")
        if self.status is ReviewObservedPathStatus.DELETED:
            if self.bytes_after is not None or self.content_SHA256 is not None:
                raise ValueError("deleted paths must not carry content evidence")
        elif self.bytes_after is None:
            raise ValueError("nondeleted paths require bounded byte evidence")
        if self.observation_SHA256 != _observed_path_digest(self):
            raise ValueError("observed path digest mismatch")
        return self


class ReviewDiffStat(_ReviewModel):
    observed_path_count: int = Field(ge=0, strict=True)
    added_count: int = Field(ge=0, strict=True)
    modified_count: int = Field(ge=0, strict=True)
    deleted_count: int = Field(ge=0, strict=True)
    renamed_count: int = Field(ge=0, strict=True)
    type_changed_count: int = Field(ge=0, strict=True)
    unmerged_count: int = Field(ge=0, strict=True)
    untracked_count: int = Field(ge=0, strict=True)
    total_bytes_after: int = Field(ge=0, strict=True)
    diff_stat_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_diff_stat(self) -> ReviewDiffStat:
        total = (
            self.added_count
            + self.modified_count
            + self.deleted_count
            + self.renamed_count
            + self.type_changed_count
            + self.unmerged_count
            + self.untracked_count
        )
        if total != self.observed_path_count:
            raise ValueError("status counts must match observed path count")
        if self.diff_stat_SHA256 != _diff_stat_digest(self):
            raise ValueError("diff stat digest mismatch")
        return self


class ReviewArtifactObservation(_ReviewModel):
    artifact_id: ReviewIdentifier
    relative_path: ReviewRelativePath
    kind: ReviewArtifactKind
    origin: ReviewArtifactOrigin
    disposition: ReviewArtifactDisposition
    expected: StrictBool
    content_SHA256: DigestText | None = None
    bytes_after: int | None = Field(default=None, ge=0, strict=True)
    source_action_id: BoundedIdentifier | None = None
    source_command_id: BoundedIdentifier | None = None
    source_validation_id: BoundedIdentifier | None = None
    rationale: BoundedPublicText
    artifact_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_artifact(self) -> ReviewArtifactObservation:
        if self.kind.value in _PROHIBITED_ARTIFACT_KINDS:
            if self.disposition is not ReviewArtifactDisposition.PROHIBITED:
                raise ValueError(
                    "prohibited artifact kind requires prohibited disposition"
                )
        if self.kind.value in _REVIEW_REQUIRED_ARTIFACT_KINDS:
            if self.disposition is ReviewArtifactDisposition.ACCEPTABLE:
                raise ValueError("artifact kind requires human review")
        if self.origin is ReviewArtifactOrigin.UNKNOWN:
            if self.disposition is ReviewArtifactDisposition.ACCEPTABLE:
                raise ValueError("unknown origin cannot be acceptable")
        if self.origin is ReviewArtifactOrigin.EXECUTION_PRODUCED:
            if self.source_action_id is None:
                raise ValueError("execution artifact requires source action")
        if self.origin is ReviewArtifactOrigin.VALIDATION_PRODUCED:
            if self.source_command_id is None and self.source_validation_id is None:
                raise ValueError("validation artifact requires source command evidence")
        if self.artifact_SHA256 != _artifact_digest(self):
            raise ValueError("artifact digest mismatch")
        return self


class ReviewFinding(_ReviewModel):
    finding_id: ReviewIdentifier
    severity: ReviewFindingSeverity
    code: ReviewFindingCode
    relative_path: ReviewRelativePath | None = None
    mutation_id: ReviewIdentifier | None = None
    artifact_id: ReviewIdentifier | None = None
    summary: BoundedPublicText
    failed_invariant: BoundedInvariantText
    finding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_finding(self) -> ReviewFinding:
        if self.code.value in _BLOCKING_FINDING_CODES:
            if self.severity is not ReviewFindingSeverity.BLOCKING:
                raise ValueError("blocking finding code requires blocking severity")
        if self.code is ReviewFindingCode.EXPECTED_PATH_OBSERVED:
            if self.severity is not ReviewFindingSeverity.INFO:
                raise ValueError("expected path observation must be informational")
        if self.finding_SHA256 != _finding_digest(self):
            raise ValueError("finding digest mismatch")
        return self


class DiffArtifactReviewObservation(_ReviewModel):
    schema_version: Literal[1] = DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION
    observation_reference: BoundedPublicText
    human_observer_id: BoundedIdentifier
    synthetic: StrictBool = False
    repository_identity: WorkspaceRepositoryIdentity
    workspace_root_binding_SHA256: DigestText
    source_commit: GitCommitText
    branch_name: BoundedIdentifier
    index_empty: StrictBool = True
    staged_file_count: int = Field(default=0, ge=0, strict=True)
    observed_paths: tuple[ReviewObservedPath, ...] = ()
    artifacts: tuple[ReviewArtifactObservation, ...] = ()
    diff_stat: ReviewDiffStat
    observation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_observation(self) -> DiffArtifactReviewObservation:
        if self.synthetic:
            raise ValueError("human observation must not be synthetic")
        if self.human_observer_id.startswith("SHADOW-"):
            raise ValueError("shadow observer cannot provide review observation")
        if not self.index_empty or self.staged_file_count != 0:
            raise ValueError("review observation requires empty index")
        _validate_observed_path_collection(self.observed_paths)
        _validate_artifact_collection(self.artifacts, self.observed_paths)
        expected_stat = _build_diff_stat(self.observed_paths)
        if self.diff_stat != expected_stat:
            raise ValueError("diff stat must derive from observed paths")
        if self.observation_SHA256 != _observation_digest(self):
            raise ValueError("review observation digest mismatch")
        return self


class DiffArtifactReviewRequest(_ReviewModel):
    schema_version: Literal[1] = DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-human-observed-deterministic-diff-artifact-review-v1"
    ] = DIFF_ARTIFACT_REVIEW_POLICY_ID
    compilation_result: WorkPacketCompilationResult
    allocation_result: WorkspaceAllocationResult
    profile_result: ToolPermissionProfileResult
    outcome_envelope: OutcomeEnvelope
    observation: DiffArtifactReviewObservation

    @model_validator(mode="after")
    def _validate_request(self) -> DiffArtifactReviewRequest:
        _validate_request_bindings(self, error_type=ValueError)
        return self


class DiffArtifactReviewResult(_ReviewModel):
    schema_version: Literal[1] = DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION
    policy_id: Literal[
        "pepper-human-observed-deterministic-diff-artifact-review-v1"
    ] = DIFF_ARTIFACT_REVIEW_POLICY_ID
    review_id: ReviewIdText
    state: AggregateReviewState
    work_packet_id: BoundedIdentifier
    work_packet_SHA256: DigestText
    allocation_id: BoundedIdentifier
    allocation_SHA256: DigestText
    profile_id: BoundedIdentifier
    profile_SHA256: DigestText
    outcome_kind: OutcomeEnvelopeKind
    outcome_SHA256: DigestText
    observation_SHA256: DigestText
    expected_mutations: tuple[ReviewExpectedMutation, ...]
    observed_paths: tuple[ReviewObservedPath, ...]
    artifacts: tuple[ReviewArtifactObservation, ...]
    findings: tuple[ReviewFinding, ...] = Field(max_length=128)
    diff_stat: ReviewDiffStat
    diff_verdict: DiffReviewVerdict
    artifact_verdict: ArtifactReviewVerdict
    manual_validation_ids_pending: tuple[BoundedIdentifier, ...] = ()
    diff_artifact_review_requirement_satisfied: StrictBool
    human_git_handoff_ready: StrictBool = False
    automatic_cleanup_authorized: StrictBool = False
    automatic_rollback_authorized: StrictBool = False
    automatic_staging_authorized: StrictBool = False
    provider_dispatch_count: int = Field(default=0, ge=0, strict=True)
    model_inference_count: int = Field(default=0, ge=0, strict=True)
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> DiffArtifactReviewResult:
        _validate_result_integrity(self, error_type=ValueError)
        return self


def build_review_expected_mutations(
    compilation_result: WorkPacketCompilationResult,
) -> tuple[ReviewExpectedMutation, ...]:
    """Derive expected mutation policy from a compiled WorkPacket scope."""

    try:
        validated = WorkPacketCompilationResult.model_validate(
            compilation_result.model_dump(mode="json")
        )
        validate_work_packet(validated.work_packet)
    except (AttributeError, ValueError) as exc:
        raise DiffArtifactReviewInputError(
            "invalid WorkPacket compilation result"
        ) from exc
    mutations: list[ReviewExpectedMutation] = []
    seen_paths: set[str] = set()
    for action in validated.work_packet.repository_scope.allowed_actions:
        parsed = _parse_expected_action(action)
        if parsed is None:
            continue
        operation, relative_path, artifact_kind = parsed
        if relative_path in seen_paths:
            raise DiffArtifactReviewPolicyError("duplicate expected mutation path")
        seen_paths.add(relative_path)
        data = {
            "mutation_id": f"EMUT-{len(mutations) + 1:03d}",
            "relative_path": relative_path,
            "allowed_statuses": _statuses_for_operation(operation),
            "artifact_expected": artifact_kind is not None,
            "expected_artifact_kind": artifact_kind,
            "source_action_id": f"ACTION-{len(mutations) + 1:03d}",
        }
        mutations.append(
            ReviewExpectedMutation(
                **data,
                expectation_SHA256=_expected_mutation_digest_from_record(data),
            )
        )
    return tuple(mutations)


def build_diff_artifact_review(
    request: DiffArtifactReviewRequest,
) -> DiffArtifactReviewResult:
    """Build a deterministic review result from one human-supplied observation."""

    validated = _validated_request(request)
    expected_mutations = build_review_expected_mutations(validated.compilation_result)
    expected_by_path = {item.relative_path: item for item in expected_mutations}
    observed_by_path = {
        item.relative_path: item for item in validated.observation.observed_paths
    }
    findings = _derive_findings(
        expected_mutations=expected_mutations,
        observed_paths=validated.observation.observed_paths,
        artifacts=validated.observation.artifacts,
    )
    diff_verdict = _derive_diff_verdict(findings)
    artifact_verdict = _derive_artifact_verdict(findings)
    state = (
        AggregateReviewState.BLOCKED
        if diff_verdict is DiffReviewVerdict.BLOCKED
        or artifact_verdict is ArtifactReviewVerdict.BLOCKED
        else AggregateReviewState.COMPLETED
    )
    selected = _selected_outcome(validated.outcome_envelope)
    base = {
        "schema_version": DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION,
        "policy_id": DIFF_ARTIFACT_REVIEW_POLICY_ID,
        "state": state,
        "work_packet_id": validated.compilation_result.work_packet.work_packet_id,
        "work_packet_SHA256": validated.compilation_result.work_packet.work_packet_SHA256,
        "allocation_id": validated.allocation_result.allocation.allocation_id,
        "allocation_SHA256": validated.allocation_result.allocation.allocation_SHA256,
        "profile_id": validated.profile_result.profile.profile_id,
        "profile_SHA256": validated.profile_result.profile.profile_SHA256,
        "outcome_kind": validated.outcome_envelope.envelope_kind,
        "outcome_SHA256": validated.outcome_envelope.envelope_SHA256,
        "observation_SHA256": validated.observation.observation_SHA256,
        "expected_mutations": expected_mutations,
        "observed_paths": validated.observation.observed_paths,
        "artifacts": validated.observation.artifacts,
        "findings": findings,
        "diff_stat": validated.observation.diff_stat,
        "diff_verdict": diff_verdict,
        "artifact_verdict": artifact_verdict,
        "manual_validation_ids_pending": _manual_validation_ids(selected),
        "diff_artifact_review_requirement_satisfied": state
        is AggregateReviewState.COMPLETED,
        "human_git_handoff_ready": False,
        "automatic_cleanup_authorized": False,
        "automatic_rollback_authorized": False,
        "automatic_staging_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    base["review_id"] = _review_id(base)
    return DiffArtifactReviewResult(
        **base,
        result_SHA256=_result_digest_from_record(base),
    )


def validate_diff_artifact_review_result(
    result: DiffArtifactReviewResult,
) -> None:
    """Validate one immutable P17.6 diff and artifact review result."""

    try:
        DiffArtifactReviewResult.model_validate(result.model_dump(mode="json"))
    except (AttributeError, ValueError) as exc:
        raise DiffArtifactReviewValidationError(
            "invalid diff artifact review result"
        ) from exc


def _validated_request(request: DiffArtifactReviewRequest) -> DiffArtifactReviewRequest:
    try:
        return DiffArtifactReviewRequest.model_validate(request.model_dump(mode="json"))
    except (AttributeError, ValueError) as exc:
        raise DiffArtifactReviewInputError(
            "invalid diff artifact review request"
        ) from exc


def _validate_request_bindings(request: DiffArtifactReviewRequest, error_type) -> None:
    try:
        validate_work_packet(request.compilation_result.work_packet)
        validate_workspace_allocation(request.allocation_result.allocation)
        validate_tool_permission_profile(request.profile_result.profile)
        validate_outcome_envelope(request.outcome_envelope)
    except ValueError as exc:
        raise error_type("prerequisite integrity validation failed") from exc
    packet = request.compilation_result.work_packet
    allocation = request.allocation_result.allocation
    profile = request.profile_result.profile
    outcome = request.outcome_envelope
    selected = _selected_outcome(outcome)
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
    if outcome.result_envelopes_ready is not True:
        raise error_type("outcome result envelopes are not ready")
    if outcome.diff_artifact_review_ready is not False:
        raise error_type("outcome already has diff artifact review")
    if outcome.human_git_handoff_ready is not False:
        raise error_type("outcome already has Git handoff readiness")
    if outcome.provider_dispatch_count != 0 or outcome.model_inference_count != 0:
        raise error_type("outcome has provider or model authority")
    if request.observation.repository_identity != allocation.repository_identity:
        raise error_type("observation repository identity mismatch")
    if (
        request.observation.workspace_root_binding_SHA256
        != allocation.allocation_SHA256
    ):
        raise error_type("observation workspace binding mismatch")
    if (
        request.observation.source_commit
        != allocation.repository_identity.source_commit
    ):
        raise error_type("observation source commit mismatch")
    if (
        request.observation.branch_name
        != allocation.repository_identity.workspace_branch
    ):
        raise error_type("observation branch mismatch")


def _validate_result_integrity(result: DiffArtifactReviewResult, error_type) -> None:
    _validate_expected_mutation_collection(
        result.expected_mutations, error_type=error_type
    )
    _validate_observed_path_collection(result.observed_paths, error_type=error_type)
    _validate_artifact_collection(
        result.artifacts, result.observed_paths, error_type=error_type
    )
    _validate_finding_collection(result.findings, error_type=error_type)
    if result.diff_stat != _build_diff_stat(result.observed_paths):
        raise error_type("diff stat does not match observed paths")
    expected_diff = _derive_diff_verdict(result.findings)
    expected_artifact = _derive_artifact_verdict(result.findings)
    if result.diff_verdict is not expected_diff:
        raise error_type("diff verdict mismatch")
    if result.artifact_verdict is not expected_artifact:
        raise error_type("artifact verdict mismatch")
    expected_state = (
        AggregateReviewState.BLOCKED
        if expected_diff is DiffReviewVerdict.BLOCKED
        or expected_artifact is ArtifactReviewVerdict.BLOCKED
        else AggregateReviewState.COMPLETED
    )
    if result.state is not expected_state:
        raise error_type("aggregate state mismatch")
    if result.diff_artifact_review_requirement_satisfied != (
        result.state is AggregateReviewState.COMPLETED
    ):
        raise error_type("review readiness mismatch")
    if (
        result.human_git_handoff_ready
        or result.automatic_cleanup_authorized
        or result.automatic_rollback_authorized
        or result.automatic_staging_authorized
    ):
        raise error_type("review result grants forbidden authority")
    if result.provider_dispatch_count != 0 or result.model_inference_count != 0:
        raise error_type("review result has provider or model authority")
    if result.review_id != _review_id(
        result.model_dump(mode="python", exclude={"result_SHA256", "review_id"})
    ):
        raise error_type("review ID mismatch")
    if result.result_SHA256 != _result_digest(result):
        raise error_type("review result digest mismatch")


def _validate_expected_mutation_collection(
    values: tuple[ReviewExpectedMutation, ...], *, error_type=ValueError
) -> None:
    ids = tuple(item.mutation_id for item in values)
    expected_ids = tuple(f"EMUT-{index:03d}" for index in range(1, len(values) + 1))
    if ids != expected_ids:
        raise error_type("expected mutation IDs must be contiguous")
    paths = tuple(item.relative_path for item in values)
    if len(paths) != len(frozenset(paths)):
        raise error_type("expected mutation paths must be unique")
    for item in values:
        if item.expectation_SHA256 != _expected_mutation_digest(item):
            raise error_type("expected mutation digest mismatch")


def _validate_observed_path_collection(
    values: tuple[ReviewObservedPath, ...], *, error_type=ValueError
) -> None:
    ids = tuple(item.observation_id for item in values)
    expected_ids = tuple(f"OPATH-{index:03d}" for index in range(1, len(values) + 1))
    if ids != expected_ids:
        raise error_type("observed path IDs must be contiguous")
    paths = tuple(item.relative_path for item in values)
    if paths != tuple(sorted(paths)):
        raise error_type("observed paths must be sorted")
    if len(paths) != len(frozenset(paths)):
        raise error_type("observed paths must be unique")
    for item in values:
        if item.observation_SHA256 != _observed_path_digest(item):
            raise error_type("observed path digest mismatch")


def _validate_artifact_collection(
    artifacts: tuple[ReviewArtifactObservation, ...],
    observed_paths: tuple[ReviewObservedPath, ...],
    *,
    error_type=ValueError,
) -> None:
    ids = tuple(item.artifact_id for item in artifacts)
    expected_ids = tuple(f"ARTF-{index:03d}" for index in range(1, len(artifacts) + 1))
    if ids != expected_ids:
        raise error_type("artifact IDs must be contiguous")
    paths = tuple(item.relative_path for item in artifacts)
    if paths != tuple(sorted(paths)):
        raise error_type("artifacts must be sorted")
    if len(paths) != len(frozenset(paths)):
        raise error_type("artifact paths must be unique")
    observed = frozenset(item.relative_path for item in observed_paths)
    for item in artifacts:
        if item.relative_path not in observed:
            raise error_type("artifact path absent from observed paths")
        if item.artifact_SHA256 != _artifact_digest(item):
            raise error_type("artifact digest mismatch")


def _validate_finding_collection(
    findings: tuple[ReviewFinding, ...], *, error_type=ValueError
) -> None:
    if len(findings) > 128:
        raise error_type("finding bound exceeded")
    ids = tuple(item.finding_id for item in findings)
    expected_ids = tuple(f"FIND-{index:03d}" for index in range(1, len(findings) + 1))
    if ids != expected_ids:
        raise error_type("finding IDs must be contiguous")
    ordered = tuple(sorted(findings, key=_finding_sort_key))
    if findings != ordered:
        raise error_type("findings must be deterministically ordered")
    for item in findings:
        if item.finding_SHA256 != _finding_digest(item):
            raise error_type("finding digest mismatch")


def _parse_expected_action(value: str):
    match = _ACTION_PATTERN.match(value.strip())
    if match is None:
        return None
    operation = match.group("operation")
    relative_path = _validate_relative_path(match.group("path").strip())
    kind_text = match.group("kind")
    kind = ReviewArtifactKind(kind_text) if kind_text is not None else None
    return operation, relative_path, kind


def _statuses_for_operation(operation: str) -> tuple[ReviewObservedPathStatus, ...]:
    if operation == ToolPermissionOperation.CREATE_FILE.value:
        return (ReviewObservedPathStatus.ADDED, ReviewObservedPathStatus.UNTRACKED)
    if operation in {"modify_file", ToolPermissionOperation.REPLACE_FILE.value}:
        return (ReviewObservedPathStatus.MODIFIED,)
    if operation == ToolPermissionOperation.DELETE_FILE.value:
        return (ReviewObservedPathStatus.DELETED,)
    raise DiffArtifactReviewPolicyError("unsupported expected mutation operation")


def _derive_findings(
    *,
    expected_mutations: tuple[ReviewExpectedMutation, ...],
    observed_paths: tuple[ReviewObservedPath, ...],
    artifacts: tuple[ReviewArtifactObservation, ...],
) -> tuple[ReviewFinding, ...]:
    expected_by_path = {item.relative_path: item for item in expected_mutations}
    observed_by_path = {item.relative_path: item for item in observed_paths}
    drafts: list[
        tuple[
            ReviewFindingSeverity,
            ReviewFindingCode,
            str | None,
            str | None,
            str | None,
            str,
            str,
        ]
    ] = []
    for mutation in expected_mutations:
        observed = observed_by_path.get(mutation.relative_path)
        if observed is None:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.EXPECTED_PATH_MISSING,
                mutation.relative_path,
                mutation.mutation_id,
                None,
                "Expected mutation path was not observed.",
                "expected mandatory path missing",
            ))
        elif observed.status not in mutation.allowed_statuses:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.UNEXPECTED_PATH_OBSERVED,
                mutation.relative_path,
                mutation.mutation_id,
                None,
                "Expected path was observed with an unallowed status.",
                "observed status not allowed",
            ))
        else:
            drafts.append((
                ReviewFindingSeverity.INFO,
                ReviewFindingCode.EXPECTED_PATH_OBSERVED,
                mutation.relative_path,
                mutation.mutation_id,
                None,
                "Expected mutation path was observed.",
                "expected path observed",
            ))
    for observed in observed_paths:
        if observed.relative_path not in expected_by_path:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.UNEXPECTED_PATH_OBSERVED,
                observed.relative_path,
                None,
                None,
                "Unexpected observed path is outside expected mutation policy.",
                "unexpected observed path",
            ))
        if observed.status is ReviewObservedPathStatus.UNMERGED:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.DIFF_SUMMARY_INCONSISTENT,
                observed.relative_path,
                None,
                None,
                "Unmerged path blocks deterministic review.",
                "unmerged path observed",
            ))
    for artifact in artifacts:
        mutation = expected_by_path.get(artifact.relative_path)
        if mutation is None or not artifact.expected or not mutation.artifact_expected:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.ARTIFACT_UNEXPECTED,
                artifact.relative_path,
                None,
                artifact.artifact_id,
                "Artifact is not expected by mutation policy.",
                "unexpected artifact",
            ))
        elif mutation.expected_artifact_kind is not artifact.kind:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.ARTIFACT_UNEXPECTED,
                artifact.relative_path,
                mutation.mutation_id,
                artifact.artifact_id,
                "Artifact kind differs from expected mutation policy.",
                "artifact kind mismatch",
            ))
        if artifact.kind.value in _PROHIBITED_ARTIFACT_KINDS:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.PROHIBITED_ARTIFACT_KIND,
                artifact.relative_path,
                None,
                artifact.artifact_id,
                "Artifact kind is prohibited by review policy.",
                "prohibited artifact kind",
            ))
        if artifact.disposition is ReviewArtifactDisposition.UNEXPECTED:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.ARTIFACT_UNEXPECTED,
                artifact.relative_path,
                None,
                artifact.artifact_id,
                "Artifact disposition is unexpected.",
                "artifact disposition unexpected",
            ))
        if artifact.origin is ReviewArtifactOrigin.UNKNOWN:
            drafts.append((
                ReviewFindingSeverity.BLOCKING,
                ReviewFindingCode.UNKNOWN_ARTIFACT_ORIGIN,
                artifact.relative_path,
                None,
                artifact.artifact_id,
                "Artifact origin is unknown.",
                "unknown artifact origin",
            ))
        if artifact.kind.value in _REVIEW_REQUIRED_ARTIFACT_KINDS:
            drafts.append((
                ReviewFindingSeverity.WARNING,
                ReviewFindingCode.ARTIFACT_REQUIRES_REVIEW,
                artifact.relative_path,
                None,
                artifact.artifact_id,
                "Artifact kind requires human review.",
                "artifact requires human review",
            ))
        observed = observed_by_path.get(artifact.relative_path)
        if (
            observed is not None
            and observed.status is not ReviewObservedPathStatus.DELETED
        ):
            if artifact.content_SHA256 is None:
                drafts.append((
                    ReviewFindingSeverity.BLOCKING,
                    ReviewFindingCode.HASH_EVIDENCE_MISSING,
                    artifact.relative_path,
                    None,
                    artifact.artifact_id,
                    "Artifact hash evidence is missing.",
                    "artifact hash required",
                ))
    drafts = tuple(sorted(drafts, key=_draft_sort_key))[:128]
    findings: list[ReviewFinding] = []
    for index, draft in enumerate(drafts, start=1):
        severity, code, relative_path, mutation_id, artifact_id, summary, invariant = (
            draft
        )
        data = {
            "finding_id": f"FIND-{index:03d}",
            "severity": severity,
            "code": code,
            "relative_path": relative_path,
            "mutation_id": mutation_id,
            "artifact_id": artifact_id,
            "summary": summary,
            "failed_invariant": invariant,
        }
        findings.append(
            ReviewFinding(**data, finding_SHA256=_finding_digest_from_record(data))
        )
    return tuple(findings)


def _derive_diff_verdict(findings: tuple[ReviewFinding, ...]) -> DiffReviewVerdict:
    diff_codes = {
        ReviewFindingCode.EXPECTED_PATH_MISSING,
        ReviewFindingCode.UNEXPECTED_PATH_OBSERVED,
        ReviewFindingCode.PATH_OUTSIDE_WORKSPACE,
        ReviewFindingCode.PATH_OUTSIDE_REPOSITORY,
        ReviewFindingCode.GIT_METADATA_PATH,
        ReviewFindingCode.FORBIDDEN_PATH_COMPONENT,
        ReviewFindingCode.DIFF_SUMMARY_INCONSISTENT,
        ReviewFindingCode.OUTCOME_NOT_TERMINAL,
    }
    for finding in findings:
        if (
            finding.code in diff_codes
            and finding.severity is ReviewFindingSeverity.BLOCKING
        ):
            return DiffReviewVerdict.BLOCKED
    for finding in findings:
        if (
            finding.code in diff_codes
            and finding.severity is ReviewFindingSeverity.WARNING
        ):
            return DiffReviewVerdict.REQUIRES_HUMAN_REVIEW
    return DiffReviewVerdict.ACCEPTED


def _derive_artifact_verdict(
    findings: tuple[ReviewFinding, ...],
) -> ArtifactReviewVerdict:
    artifact_codes = {
        ReviewFindingCode.PROHIBITED_ARTIFACT_KIND,
        ReviewFindingCode.UNKNOWN_ARTIFACT_ORIGIN,
        ReviewFindingCode.ARTIFACT_REQUIRES_REVIEW,
        ReviewFindingCode.ARTIFACT_UNEXPECTED,
        ReviewFindingCode.HASH_EVIDENCE_MISSING,
    }
    for finding in findings:
        if (
            finding.code in artifact_codes
            and finding.severity is ReviewFindingSeverity.BLOCKING
        ):
            return ArtifactReviewVerdict.BLOCKED
    for finding in findings:
        if (
            finding.code in artifact_codes
            and finding.severity is ReviewFindingSeverity.WARNING
        ):
            return ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    return ArtifactReviewVerdict.ACCEPTED


def _selected_outcome(outcome: OutcomeEnvelope):
    if outcome.envelope_kind is OutcomeEnvelopeKind.RESULT and outcome.result_envelope:
        return outcome.result_envelope
    if (
        outcome.envelope_kind is OutcomeEnvelopeKind.FAILURE
        and outcome.failure_envelope
    ):
        return outcome.failure_envelope
    if (
        outcome.envelope_kind is OutcomeEnvelopeKind.CANCELLATION
        and outcome.cancellation_envelope
    ):
        return outcome.cancellation_envelope
    raise DiffArtifactReviewStateError("outcome envelope is not terminal")


def _manual_validation_ids(selected) -> tuple[str, ...]:
    if hasattr(selected, "manual_validation_ids_pending"):
        return selected.manual_validation_ids_pending
    return ()


def _build_diff_stat(observed_paths: tuple[ReviewObservedPath, ...]) -> ReviewDiffStat:
    data = {
        "observed_path_count": len(observed_paths),
        "added_count": _count_status(observed_paths, ReviewObservedPathStatus.ADDED),
        "modified_count": _count_status(
            observed_paths, ReviewObservedPathStatus.MODIFIED
        ),
        "deleted_count": _count_status(
            observed_paths, ReviewObservedPathStatus.DELETED
        ),
        "renamed_count": _count_status(
            observed_paths, ReviewObservedPathStatus.RENAMED
        ),
        "type_changed_count": _count_status(
            observed_paths, ReviewObservedPathStatus.TYPE_CHANGED
        ),
        "unmerged_count": _count_status(
            observed_paths, ReviewObservedPathStatus.UNMERGED
        ),
        "untracked_count": _count_status(
            observed_paths, ReviewObservedPathStatus.UNTRACKED
        ),
        "total_bytes_after": sum(item.bytes_after or 0 for item in observed_paths),
    }
    return ReviewDiffStat(**data, diff_stat_SHA256=_diff_stat_digest_from_record(data))


def _count_status(
    observed_paths: tuple[ReviewObservedPath, ...], status: ReviewObservedPathStatus
) -> int:
    return sum(1 for item in observed_paths if item.status is status)


def _review_id(data) -> str:
    digest = _digest(REVIEW_ID_DIGEST_ALGORITHM, _json_record(data))
    ticket = data["work_packet_id"].split("-R", 1)[0]
    ticket = re.sub(r"[^A-Za-z0-9]+", "-", ticket).strip("-").upper() or "WORK-PACKET"
    return f"DAR-{ticket}-R0001-{digest[:12]}"


def _expected_mutation_digest(value: ReviewExpectedMutation) -> str:
    return _expected_mutation_digest_from_record(
        value.model_dump(mode="json", exclude={"expectation_SHA256"})
    )


def _observed_path_digest(value: ReviewObservedPath) -> str:
    return _observed_path_digest_from_record(
        value.model_dump(mode="json", exclude={"observation_SHA256"})
    )


def _diff_stat_digest(value: ReviewDiffStat) -> str:
    return _diff_stat_digest_from_record(
        value.model_dump(mode="json", exclude={"diff_stat_SHA256"})
    )


def _artifact_digest(value: ReviewArtifactObservation) -> str:
    return _artifact_digest_from_record(
        value.model_dump(mode="json", exclude={"artifact_SHA256"})
    )


def _finding_digest(value: ReviewFinding) -> str:
    return _finding_digest_from_record(
        value.model_dump(mode="json", exclude={"finding_SHA256"})
    )


def _observation_digest(value: DiffArtifactReviewObservation) -> str:
    return _observation_digest_from_record(
        value.model_dump(mode="json", exclude={"observation_SHA256"})
    )


def _result_digest(value: DiffArtifactReviewResult) -> str:
    return _result_digest_from_record(
        value.model_dump(mode="json", exclude={"result_SHA256"})
    )


def _expected_mutation_digest_from_record(record) -> str:
    return _digest(EXPECTED_MUTATION_DIGEST_ALGORITHM, record)


def _observed_path_digest_from_record(record) -> str:
    return _digest(OBSERVED_PATH_DIGEST_ALGORITHM, record)


def _diff_stat_digest_from_record(record) -> str:
    return _digest(DIFF_STAT_DIGEST_ALGORITHM, record)


def _artifact_digest_from_record(record) -> str:
    return _digest(ARTIFACT_DIGEST_ALGORITHM, record)


def _finding_digest_from_record(record) -> str:
    return _digest(FINDING_DIGEST_ALGORITHM, record)


def _observation_digest_from_record(record) -> str:
    return _digest(OBSERVATION_DIGEST_ALGORITHM, record)


def _result_digest_from_record(record) -> str:
    return _digest(RESULT_DIGEST_ALGORITHM, record)


def _digest(algorithm: str, value) -> str:
    payload = f"{algorithm}:{_stable_json(value)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _stable_json(value) -> str:
    return json.dumps(
        _json_record(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _json_record(value):
    if isinstance(value, BaseModel):
        return _json_record(value.model_dump(mode="json"))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_json_record(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_record(item) for key, item in sorted(value.items())}
    return value


def _draft_sort_key(draft) -> tuple[int, str, str, str, str]:
    severity, code, relative_path, mutation_id, artifact_id, _summary, _invariant = (
        draft
    )
    return (
        _SEVERITY_ORDER.index(severity.value),
        code.value,
        relative_path or "",
        mutation_id or "",
        artifact_id or "",
    )


def _finding_sort_key(finding: ReviewFinding) -> tuple[int, str, str, str, str]:
    return (
        _SEVERITY_ORDER.index(finding.severity.value),
        finding.code.value,
        finding.relative_path or "",
        finding.mutation_id or "",
        finding.artifact_id or "",
    )
