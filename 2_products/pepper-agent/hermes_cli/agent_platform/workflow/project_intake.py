"""Governed Pepper project-intake workflow contracts for Agent Platform P18.1.

This module is intentionally pure.  It validates bounded caller-supplied intake
evidence, projects deterministic digests, and advances the P18.0 governed
workflow state machine from draft to intake-ready through the public P18.0
transition builder.  It does not inspect Git, read files, call databases,
dispatch providers or models, execute Kanban, persist memory, or claim
production readiness.
"""

from __future__ import annotations

import hashlib
import json
import re
from enum import Enum
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.workflow.governed_state_machine import (
    GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
    GovernedWorkflowIdentity,
    GovernedWorkflowSnapshot,
    GovernedWorkflowState,
    GovernedWorkflowStateMachineResult,
    GovernedWorkflowTransition,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowProjection,
    P17WorkflowBinding,
    WorkflowReuseSummary,
    WorkflowRuntimeStateMapping,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_governed_workflow_transition,
    validate_governed_workflow_snapshot,
    validate_governed_workflow_transition_request,
)


PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION = 1
PROJECT_INTAKE_WORKFLOW_POLICY_ID = "pepper-governed-project-intake-workflow-v1"

PROJECT_INTAKE_ID_DIGEST_ALGORITHM = "agent-platform-project-intake-id-sha256-v1"
PROJECT_INTAKE_IDENTITY_DIGEST_ALGORITHM = (
    "agent-platform-project-intake-identity-sha256-v1"
)
PROJECT_ROADMAP_ITEM_DIGEST_ALGORITHM = "agent-platform-project-roadmap-item-sha256-v1"
PROJECT_ROADMAP_DIGEST_ALGORITHM = "agent-platform-project-roadmap-sha256-v1"
PROJECT_REPOSITORY_BINDING_DIGEST_ALGORITHM = (
    "agent-platform-project-repository-binding-sha256-v1"
)
PROJECT_INTAKE_CONSTRAINT_DIGEST_ALGORITHM = (
    "agent-platform-project-intake-constraint-sha256-v1"
)
PROJECT_CONTEXT_REFERENCE_DIGEST_ALGORITHM = (
    "agent-platform-project-context-reference-sha256-v1"
)
PROJECT_INTAKE_APPROVAL_DIGEST_ALGORITHM = (
    "agent-platform-project-intake-approval-sha256-v1"
)
PROJECT_INTAKE_FINDING_DIGEST_ALGORITHM = (
    "agent-platform-project-intake-finding-sha256-v1"
)
PROJECT_INTAKE_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-project-intake-summary-sha256-v1"
)
PROJECT_INTAKE_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-project-intake-result-sha256-v1"
)

_CANONICAL_PROJECT_ID = "PEPPER"
_CANONICAL_PROJECT_NAME = "Pepper"
_CANONICAL_MACROPROJECT_ID = "P18"
_CANONICAL_MACROPROJECT_TITLE = "Manual-to-Hermes Workflow Migration"
_CANONICAL_ROADMAP_ID = "P18-manual-to-hermes-workflow-migration"
_CANONICAL_REPOSITORY_ID = "AGENT-PLATFORM-PEPPER"
_CANONICAL_REPOSITORY_DISPLAY_NAME = "AGENT PLATFORM"
_CANONICAL_BRANCH = "p18-manual-to-hermes-workflow-migration"
_CANONICAL_PRODUCT_ROOT = "2_products/pepper-agent"
_CANONICAL_P18_0_COMMIT = "7b928e60ed4adf49bfb3e47ab9acf1119aaef870"
_CANONICAL_UPSTREAM_MAIN_COMMIT = "92d1e790e70176ed542b1ae44d6e8af771be512b"
_CANONICAL_BRANCH_POLICY = "one_branch_per_macroproject;one_commit_per_ticket"

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
_INTAKE_ID_PATTERN = r"^PINT-P18-[a-f0-9]{12}$"
_FINDING_ID_PATTERN = r"^PINF-[0-9]{3}$"
_IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,95}$"
_SAFE_PATH_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,159}$"
_ANSI_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\\\Users\\\\|/Users/|/home/)")
_SHELL_COMMAND_PATTERN = re.compile(
    r"(?:\bgit\s+(?:add|commit|push|checkout|switch|merge|rebase|reset|stash|tag)\b)"
    r"|(?:\bdocker\s+(?:build|run|compose|pull|push)\b)"
    r"|(?:\b(?:curl|wget|powershell|cmd\.exe|bash|sh)\s+)"
    r"|(?:\brm\s+-rf\b)|(?:\bpython\s+-c\b)",
    re.IGNORECASE,
)
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
_CREDENTIAL_MARKERS = (
    "access_token",
    "refresh_token",
    "authorization:",
    "bearer ",
    "client_secret",
    "api_key",
    "private key",
    "oauth code",
    "password=",
    "token=",
    "secret=",
)
_RAW_CONTEXT_MARKERS = (
    "raw prompt",
    "system prompt",
    "reasoning trace",
    "provider response",
    "raw conversation",
    "chatgpt transcript",
    "opencode transcript",
    "stdout:",
    "stderr:",
    "diff --git",
)

DigestText = Annotated[str, Field(pattern=_DIGEST_PATTERN)]
CommitText = Annotated[str, Field(pattern=_COMMIT_PATTERN)]
IntakeIdentifier = Annotated[str, Field(pattern=_INTAKE_ID_PATTERN)]
FindingIdentifier = Annotated[str, Field(pattern=_FINDING_ID_PATTERN)]
ProjectIdentifier = Annotated[str, Field(min_length=1, max_length=64)]
ProjectName = Annotated[str, Field(min_length=1, max_length=128)]
MacroprojectTitle = Annotated[str, Field(min_length=1, max_length=160)]
RoadmapIdentifier = Annotated[str, Field(min_length=1, max_length=96)]
TicketIdentifier = Annotated[str, Field(min_length=1, max_length=32)]
BoundedText = Annotated[str, Field(min_length=1, max_length=512)]
SourceText = Annotated[str, Field(min_length=1, max_length=160)]
ProductRootText = Annotated[str, Field(pattern=_SAFE_PATH_PATTERN, max_length=160)]
BranchPolicyText = Annotated[str, Field(min_length=1, max_length=96)]

ConstraintCategory = Literal[
    "architecture",
    "authority",
    "security",
    "Git",
    "dependency",
    "runtime",
    "workflow",
    "reuse",
    "future_boundary",
]
ContextReferenceKind = Literal[
    "canonical_document",
    "public_contract",
    "roadmap",
    "repository_metadata",
    "prior_ticket",
    "runtime_capability_analysis",
]
ContextReferenceAuthority = Literal["canonical", "supporting", "informational"]

_P18_0_CONTRACTS_CONSUMED = (
    GovernedWorkflowState,
    GovernedWorkflowTransition,
    GovernedWorkflowIdentity,
    GovernedWorkflowSnapshot,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowProjection,
    WorkflowRuntimeStateMapping,
    P17WorkflowBinding,
    WorkflowReuseSummary,
    GovernedWorkflowStateMachineResult,
)
_P18_0_CONTRACT_FUNCTIONS_CONSUMED = (
    validate_governed_workflow_snapshot,
    validate_governed_workflow_transition_request,
    build_governed_workflow_transition,
)


class ProjectIntakeError(ValueError):
    """Base error for P18.1 project-intake contract failures."""


class ProjectIntakeInputError(ProjectIntakeError):
    """Raised when caller-supplied intake input is malformed."""


class ProjectIntakeIntegrityError(ProjectIntakeError):
    """Raised when deterministic intake integrity checks fail."""


class ProjectIntakePolicyError(ProjectIntakeError):
    """Raised when project-intake policy is violated."""


class ProjectIntakeStateError(ProjectIntakeError):
    """Raised when workflow state cannot accept intake progression."""


class ProjectIntakeValidationError(ProjectIntakeError):
    """Raised when immutable project-intake result validation fails."""


class ProjectIntakeState(str, Enum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    ACCEPTED = "accepted"


class ProjectIntakeDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ProjectIntakeProjectKind(str, Enum):
    PEPPER = "pepper"


class ProjectIntakeFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class ProjectIntakeFindingCode(str, Enum):
    PROJECT_ID_VALID = "project_id_valid"
    PROJECT_ID_INVALID = "project_id_invalid"
    ROADMAP_VALID = "roadmap_valid"
    ROADMAP_INVALID = "roadmap_invalid"
    CURRENT_TICKET_VALID = "current_ticket_valid"
    CURRENT_TICKET_INVALID = "current_ticket_invalid"
    REPOSITORY_BINDING_VALID = "repository_binding_valid"
    REPOSITORY_BINDING_INVALID = "repository_binding_invalid"
    BRANCH_BINDING_VALID = "branch_binding_valid"
    BRANCH_BINDING_INVALID = "branch_binding_invalid"
    PRODUCT_ROOT_VALID = "product_root_valid"
    PRODUCT_ROOT_INVALID = "product_root_invalid"
    PREREQUISITE_BINDING_VALID = "prerequisite_binding_valid"
    PREREQUISITE_BINDING_INVALID = "prerequisite_binding_invalid"
    CONSTRAINTS_VALID = "constraints_valid"
    CONSTRAINTS_INVALID = "constraints_invalid"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    HUMAN_APPROVAL_PRESENT = "human_approval_present"
    WORKFLOW_BINDING_VALID = "workflow_binding_valid"
    WORKFLOW_BINDING_INVALID = "workflow_binding_invalid"
    INTAKE_ACCEPTED = "intake_accepted"
    INTAKE_REJECTED = "intake_rejected"


class _ProjectIntakeModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        protected_namespaces=(),
        validate_default=True,
        str_strip_whitespace=True,
    )


def _validate_bounded_text(value: str, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if value != value.strip():
        raise ValueError(f"{label} must be stripped")
    if not value:
        raise ValueError(f"{label} must be non-empty")
    if any(character in value for character in ("\n", "\r", "\x00")):
        raise ValueError(f"{label} contains unsafe control characters")
    if _ANSI_PATTERN.search(value):
        raise ValueError(f"{label} contains ANSI escape content")
    if _PERSONAL_PATH_PATTERN.search(value):
        raise ValueError(f"{label} contains an absolute personal path")
    if _SHELL_COMMAND_PATTERN.search(value):
        raise ValueError(f"{label} contains shell command content")
    lowered = value.lower()
    if any(marker in lowered for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} contains credential-like content")
    if any(marker in lowered for marker in _RAW_CONTEXT_MARKERS):
        raise ValueError(f"{label} contains raw context content")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-like content")
    return value


def _validate_identifier(value: str, label: str) -> str:
    _validate_bounded_text(value, label)
    if not re.fullmatch(_IDENTIFIER_PATTERN, value):
        raise ValueError(f"{label} must be a bounded identifier")
    return value


def _validate_product_root(value: str) -> str:
    _validate_bounded_text(value, "product_root")
    if value != _CANONICAL_PRODUCT_ROOT:
        raise ValueError("product_root must bind the canonical Pepper product root")
    if value.startswith("/") or "\\" in value or ":" in value:
        raise ValueError("product_root must be repository-relative")
    if ".." in value.split("/"):
        raise ValueError("product_root cannot traverse parents")
    return value


def _normalize_for_digest(value: object) -> object:
    if isinstance(value, BaseModel):
        return _normalize_for_digest(value.model_dump(mode="json", warnings=False))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_normalize_for_digest(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize_for_digest(item) for key, item in value.items()}
    return value


def _digest_from_record(algorithm: str, record: object) -> str:
    payload = {"algorithm": algorithm, "record": _normalize_for_digest(record)}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _model_digest(algorithm: str, value: BaseModel, digest_field: str) -> str:
    record = value.model_dump(
        mode="json",
        exclude={digest_field},
        warnings=False,
    )
    return _digest_from_record(algorithm, record)


def _make_model(
    model_type: type[_ProjectIntakeModel],
    digest_field: str,
    algorithm: str,
    **values: object,
) -> _ProjectIntakeModel:
    data = dict(values)
    data[digest_field] = _digest_from_record(algorithm, data)
    return model_type(**data)


def _validated_model(
    model_type: type[_ProjectIntakeModel], value: object
) -> _ProjectIntakeModel:
    try:
        if isinstance(value, BaseModel):
            return model_type.model_validate(
                value.model_dump(mode="python", warnings=False)
            )
        return model_type.model_validate(value)
    except (AttributeError, ValueError) as exc:
        raise ProjectIntakeValidationError(f"invalid {model_type.__name__}") from exc


class ProjectIntakeIdentity(_ProjectIntakeModel):
    project_id: ProjectIdentifier
    project_name: ProjectName
    project_kind: ProjectIntakeProjectKind
    macroproject_id: ProjectIdentifier
    macroproject_title: MacroprojectTitle
    roadmap_id: RoadmapIdentifier
    identity_SHA256: DigestText

    @field_validator(
        "project_id",
        "project_name",
        "macroproject_id",
        "macroproject_title",
        "roadmap_id",
        mode="after",
    )
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "project intake identity field")

    @model_validator(mode="after")
    def _validate_identity(self) -> ProjectIntakeIdentity:
        if self.project_id != _CANONICAL_PROJECT_ID:
            raise ValueError("project_id must be PEPPER")
        if self.project_name != _CANONICAL_PROJECT_NAME:
            raise ValueError("project_name must be Pepper")
        if self.project_kind is not ProjectIntakeProjectKind.PEPPER:
            raise ValueError("project_kind must be pepper")
        if self.macroproject_id != _CANONICAL_MACROPROJECT_ID:
            raise ValueError("macroproject_id must be P18")
        if self.macroproject_title != _CANONICAL_MACROPROJECT_TITLE:
            raise ValueError("macroproject_title must bind P18")
        if self.roadmap_id != _CANONICAL_ROADMAP_ID:
            raise ValueError("roadmap_id must bind the canonical P18 roadmap")
        if self.identity_SHA256 != _model_digest(
            PROJECT_INTAKE_IDENTITY_DIGEST_ALGORITHM, self, "identity_SHA256"
        ):
            raise ValueError(
                "identity_SHA256 must match project-intake identity digest"
            )
        return self


class ProjectRoadmapItem(_ProjectIntakeModel):
    ticket_id: TicketIdentifier
    title: BoundedText
    ordinal: int = Field(ge=1, le=999, strict=True)
    prerequisite_ticket_ids: tuple[TicketIdentifier, ...] = Field(max_length=16)
    completed: StrictBool
    current: StrictBool
    deferred: StrictBool
    roadmap_item_SHA256: DigestText

    @field_validator("ticket_id", mode="after")
    @classmethod
    def _validate_ticket_id(cls, value: str) -> str:
        return _validate_identifier(value, "ticket_id")

    @field_validator("title", mode="after")
    @classmethod
    def _validate_title(cls, value: str) -> str:
        return _validate_bounded_text(value, "roadmap item title")

    @field_validator("prerequisite_ticket_ids", mode="after")
    @classmethod
    def _validate_prerequisites(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("prerequisite_ticket_ids must be unique")
        return tuple(
            _validate_identifier(item, "prerequisite_ticket_id") for item in value
        )

    @model_validator(mode="after")
    def _validate_item(self) -> ProjectRoadmapItem:
        if self.ticket_id in self.prerequisite_ticket_ids:
            raise ValueError("roadmap item cannot depend on itself")
        if self.completed and self.current:
            raise ValueError("completed item cannot be current")
        if self.deferred and self.current:
            raise ValueError("deferred item cannot be current")
        if self.roadmap_item_SHA256 != _model_digest(
            PROJECT_ROADMAP_ITEM_DIGEST_ALGORITHM, self, "roadmap_item_SHA256"
        ):
            raise ValueError("roadmap_item_SHA256 must match roadmap item digest")
        return self


class ProjectRoadmap(_ProjectIntakeModel):
    roadmap_id: RoadmapIdentifier
    macroproject_id: ProjectIdentifier
    items: tuple[ProjectRoadmapItem, ...] = Field(min_length=10, max_length=10)
    current_ticket_id: TicketIdentifier
    completed_ticket_ids: tuple[TicketIdentifier, ...] = Field(max_length=10)
    next_ticket_ids: tuple[TicketIdentifier, ...] = Field(max_length=4)
    roadmap_SHA256: DigestText

    @field_validator("roadmap_id", "macroproject_id", "current_ticket_id", mode="after")
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "roadmap field")

    @field_validator("completed_ticket_ids", "next_ticket_ids", mode="after")
    @classmethod
    def _validate_ticket_tuple(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("roadmap ticket tuple fields must be unique")
        return tuple(_validate_identifier(item, "roadmap ticket id") for item in value)

    @model_validator(mode="after")
    def _validate_roadmap(self) -> ProjectRoadmap:
        if self.roadmap_id != _CANONICAL_ROADMAP_ID:
            raise ValueError("roadmap_id must bind the canonical P18 roadmap")
        if self.macroproject_id != _CANONICAL_MACROPROJECT_ID:
            raise ValueError("roadmap macroproject_id must be P18")
        item_ids = tuple(item.ticket_id for item in self.items)
        ordinals = tuple(item.ordinal for item in self.items)
        canonical_item_ids = tuple(
            ticket_id for ticket_id, _title in _CANONICAL_ROADMAP_TITLES
        )
        canonical_titles = tuple(
            title for _ticket_id, title in _CANONICAL_ROADMAP_TITLES
        )
        if item_ids != canonical_item_ids:
            raise ValueError("roadmap items must be the canonical P18 sequence")
        if tuple(item.title for item in self.items) != canonical_titles:
            raise ValueError("roadmap items must use canonical P18 titles")
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("roadmap ticket IDs must be unique")
        if len(ordinals) != len(set(ordinals)):
            raise ValueError("roadmap ordinals must be unique")
        if ordinals != tuple(range(1, len(self.items) + 1)):
            raise ValueError("roadmap items must be in deterministic ordinal order")
        for item in self.items:
            missing = set(item.prerequisite_ticket_ids).difference(item_ids)
            if missing:
                raise ValueError("roadmap prerequisite IDs must be explicit")
        current_items = tuple(item.ticket_id for item in self.items if item.current)
        if current_items != ("P18.1",):
            raise ValueError("roadmap must have exactly P18.1 as current item")
        completed_items = tuple(item.ticket_id for item in self.items if item.completed)
        if self.completed_ticket_ids != completed_items:
            raise ValueError("completed_ticket_ids must match completed items")
        if self.completed_ticket_ids != ("P18.0",):
            raise ValueError("P18.0 must be the only completed P18 roadmap item")
        if self.next_ticket_ids != ("P18.2",):
            raise ValueError("P18.2 must be the next ticket after project intake")
        if self.current_ticket_id != "P18.1":
            raise ValueError("current_ticket_id must be P18.1")
        if self.roadmap_SHA256 != _model_digest(
            PROJECT_ROADMAP_DIGEST_ALGORITHM, self, "roadmap_SHA256"
        ):
            raise ValueError("roadmap_SHA256 must match roadmap digest")
        return self


class ProjectRepositoryBinding(_ProjectIntakeModel):
    repository_id: ProjectIdentifier
    repository_display_name: ProjectName
    expected_branch: BoundedText
    product_root: ProductRootText
    branch_parent_commit: CommitText
    upstream_main_commit: CommitText
    branch_policy: BranchPolicyText
    repository_binding_SHA256: DigestText

    @field_validator(
        "repository_id",
        "repository_display_name",
        "expected_branch",
        "branch_policy",
        mode="after",
    )
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "repository binding field")

    @field_validator("product_root", mode="after")
    @classmethod
    def _validate_product_root_field(cls, value: str) -> str:
        return _validate_product_root(value)

    @model_validator(mode="after")
    def _validate_repository(self) -> ProjectRepositoryBinding:
        if self.repository_id != _CANONICAL_REPOSITORY_ID:
            raise ValueError("repository_id must bind the canonical Pepper repository")
        if self.repository_display_name != _CANONICAL_REPOSITORY_DISPLAY_NAME:
            raise ValueError("repository_display_name must be AGENT PLATFORM")
        if self.expected_branch != _CANONICAL_BRANCH:
            raise ValueError("expected_branch must bind the P18 macroproject branch")
        if self.branch_parent_commit != _CANONICAL_P18_0_COMMIT:
            raise ValueError("branch_parent_commit must bind committed P18.0")
        if self.upstream_main_commit != _CANONICAL_UPSTREAM_MAIN_COMMIT:
            raise ValueError("upstream_main_commit must bind accepted upstream main")
        if self.branch_policy != _CANONICAL_BRANCH_POLICY:
            raise ValueError(
                "branch_policy must be one_branch_per_macroproject and one_commit_per_ticket"
            )
        if self.repository_binding_SHA256 != _model_digest(
            PROJECT_REPOSITORY_BINDING_DIGEST_ALGORITHM,
            self,
            "repository_binding_SHA256",
        ):
            raise ValueError(
                "repository_binding_SHA256 must match repository binding digest"
            )
        return self


class ProjectIntakeConstraint(_ProjectIntakeModel):
    constraint_id: ProjectIdentifier
    category: ConstraintCategory
    description: BoundedText
    blocking: StrictBool
    source: SourceText
    constraint_SHA256: DigestText

    @field_validator("constraint_id", mode="after")
    @classmethod
    def _validate_constraint_id(cls, value: str) -> str:
        return _validate_identifier(value, "constraint_id")

    @field_validator("description", "source", mode="after")
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "constraint field")

    @model_validator(mode="after")
    def _validate_constraint(self) -> ProjectIntakeConstraint:
        if self.constraint_SHA256 != _model_digest(
            PROJECT_INTAKE_CONSTRAINT_DIGEST_ALGORITHM, self, "constraint_SHA256"
        ):
            raise ValueError("constraint_SHA256 must match project constraint digest")
        return self


class ProjectContextReference(_ProjectIntakeModel):
    reference_id: ProjectIdentifier
    reference_kind: ContextReferenceKind
    reference_name: BoundedText
    source_scope: BoundedText
    authority: ContextReferenceAuthority
    required: StrictBool
    reference_SHA256: DigestText

    @field_validator("reference_id", mode="after")
    @classmethod
    def _validate_reference_id(cls, value: str) -> str:
        return _validate_identifier(value, "reference_id")

    @field_validator("reference_name", "source_scope", mode="after")
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "context reference field")

    @model_validator(mode="after")
    def _validate_reference(self) -> ProjectContextReference:
        if self.reference_SHA256 != _model_digest(
            PROJECT_CONTEXT_REFERENCE_DIGEST_ALGORITHM, self, "reference_SHA256"
        ):
            raise ValueError("reference_SHA256 must match context reference digest")
        return self


class ProjectIntakeApproval(_ProjectIntakeModel):
    approval_required: StrictBool
    approved: StrictBool
    approval_scope: BoundedText
    approved_by_human: StrictBool
    approval_statement: Annotated[str, Field(min_length=1, max_length=512)]
    approval_SHA256: DigestText

    @field_validator("approval_scope", "approval_statement", mode="after")
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "project intake approval field")

    @model_validator(mode="after")
    def _validate_approval(self) -> ProjectIntakeApproval:
        if self.approved and not self.approval_required:
            raise ValueError("approved intake approval must also be required")
        if self.approval_SHA256 != _model_digest(
            PROJECT_INTAKE_APPROVAL_DIGEST_ALGORITHM, self, "approval_SHA256"
        ):
            raise ValueError(
                "approval_SHA256 must match project intake approval digest"
            )
        return self


class ProjectIntakeRequest(_ProjectIntakeModel):
    schema_version: Literal[1] = PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION
    policy_id: Literal["pepper-governed-project-intake-workflow-v1"] = (
        PROJECT_INTAKE_WORKFLOW_POLICY_ID
    )
    identity: ProjectIntakeIdentity
    roadmap: ProjectRoadmap
    repository_binding: ProjectRepositoryBinding
    constraints: tuple[ProjectIntakeConstraint, ...] = Field(
        min_length=1, max_length=128
    )
    context_references: tuple[ProjectContextReference, ...] = Field(
        min_length=1, max_length=128
    )
    approval: ProjectIntakeApproval
    initial_workflow_snapshot: GovernedWorkflowSnapshot


class ProjectIntakeFinding(_ProjectIntakeModel):
    finding_id: FindingIdentifier
    severity: ProjectIntakeFindingSeverity
    code: ProjectIntakeFindingCode
    subject_id: BoundedText
    summary: BoundedText
    failed_invariant: BoundedText | None
    finding_SHA256: DigestText

    @field_validator("subject_id", "summary", mode="after")
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "intake finding field")

    @field_validator("failed_invariant", mode="after")
    @classmethod
    def _validate_optional_text(cls, value: str | None) -> str | None:
        if value is not None:
            return _validate_bounded_text(value, "intake finding invariant")
        return value

    @model_validator(mode="after")
    def _validate_finding(self) -> ProjectIntakeFinding:
        invalid_code = (
            self.code.value.endswith("_invalid")
            or self.code is ProjectIntakeFindingCode.INTAKE_REJECTED
        )
        if invalid_code and self.severity is not ProjectIntakeFindingSeverity.BLOCKING:
            raise ValueError("invalid/rejected findings must be blocking")
        if not invalid_code and self.severity is ProjectIntakeFindingSeverity.BLOCKING:
            raise ValueError("blocking findings require invalid/rejected code")
        if self.finding_SHA256 != _model_digest(
            PROJECT_INTAKE_FINDING_DIGEST_ALGORITHM, self, "finding_SHA256"
        ):
            raise ValueError("finding_SHA256 must match project intake finding digest")
        return self


class ProjectIntakeSummary(_ProjectIntakeModel):
    project_identity_valid: StrictBool
    roadmap_valid: StrictBool
    repository_binding_valid: StrictBool
    constraints_valid: StrictBool
    context_references_valid: StrictBool
    human_approval_present: StrictBool
    workflow_transition_valid: StrictBool
    information_finding_count: int = Field(ge=0, le=128, strict=True)
    warning_finding_count: int = Field(ge=0, le=128, strict=True)
    blocking_finding_count: int = Field(ge=0, le=128, strict=True)
    project_intake_requirement_satisfied: StrictBool
    P18_2_ready: StrictBool
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> ProjectIntakeSummary:
        valid_flags = (
            self.project_identity_valid,
            self.roadmap_valid,
            self.repository_binding_valid,
            self.constraints_valid,
            self.context_references_valid,
            self.human_approval_present,
            self.workflow_transition_valid,
        )
        if self.blocking_finding_count == 0 and not all(valid_flags):
            raise ValueError("valid summary flags are required when no blockers exist")
        requirement_met = all(valid_flags) and self.blocking_finding_count == 0
        if self.project_intake_requirement_satisfied != requirement_met:
            raise ValueError(
                "project intake requirement must derive from validated flags"
            )
        if self.P18_2_ready != requirement_met:
            raise ValueError(
                "P18_2 readiness must derive from project intake requirement"
            )
        if self.summary_SHA256 != _model_digest(
            PROJECT_INTAKE_SUMMARY_DIGEST_ALGORITHM, self, "summary_SHA256"
        ):
            raise ValueError("summary_SHA256 must match project intake summary digest")
        return self


class ProjectIntakeResult(_ProjectIntakeModel):
    schema_version: Literal[1] = PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION
    policy_id: Literal["pepper-governed-project-intake-workflow-v1"] = (
        PROJECT_INTAKE_WORKFLOW_POLICY_ID
    )
    intake_id: IntakeIdentifier
    state: ProjectIntakeState
    decision: ProjectIntakeDecision
    identity: ProjectIntakeIdentity
    roadmap: ProjectRoadmap
    repository_binding: ProjectRepositoryBinding
    constraints: tuple[ProjectIntakeConstraint, ...] = Field(
        min_length=1, max_length=128
    )
    context_references: tuple[ProjectContextReference, ...] = Field(
        min_length=1, max_length=128
    )
    approval: ProjectIntakeApproval
    previous_workflow_snapshot_SHA256: DigestText
    workflow_transition_result: GovernedWorkflowTransitionResult
    resulting_workflow_snapshot: GovernedWorkflowSnapshot
    findings: tuple[ProjectIntakeFinding, ...] = Field(min_length=1, max_length=128)
    summary: ProjectIntakeSummary
    project_intake_requirement_satisfied: StrictBool
    P18_2_ready: StrictBool
    production_readiness_claimed: Literal[False]
    provider_dispatch_count: int = Field(ge=0, le=0, strict=True)
    model_inference_count: int = Field(ge=0, le=0, strict=True)
    Git_commands_executed: int = Field(ge=0, le=0, strict=True)
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ProjectIntakeResult:
        _validate_findings(self.findings)
        if (
            self.previous_workflow_snapshot_SHA256
            != self.workflow_transition_result.previous_snapshot_SHA256
        ):
            raise ValueError("previous snapshot digest must bind transition result")
        if (
            self.resulting_workflow_snapshot
            != self.workflow_transition_result.resulting_snapshot
        ):
            raise ValueError("resulting snapshot must match transition result")
        if (
            self.resulting_workflow_snapshot.current_state
            is not GovernedWorkflowState.INTAKE_READY
        ):
            raise ValueError("resulting workflow snapshot must be intake_ready")
        if (
            self.workflow_transition_result.transition.from_state
            is not GovernedWorkflowState.DRAFT
        ):
            raise ValueError("project intake transition must start from draft")
        if (
            self.workflow_transition_result.transition.to_state
            is not GovernedWorkflowState.INTAKE_READY
        ):
            raise ValueError("project intake transition must target intake_ready")
        if self.workflow_transition_result.accepted:
            if self.state is not ProjectIntakeState.ACCEPTED:
                raise ValueError("accepted transition requires accepted intake state")
            if self.decision is not ProjectIntakeDecision.ACCEPTED:
                raise ValueError("accepted transition requires accepted decision")
        else:
            if self.state is not ProjectIntakeState.BLOCKED:
                raise ValueError("rejected transition requires blocked intake state")
            if self.decision is not ProjectIntakeDecision.REJECTED:
                raise ValueError("rejected transition requires rejected decision")
        if (
            self.project_intake_requirement_satisfied
            != self.summary.project_intake_requirement_satisfied
        ):
            raise ValueError("result requirement flag must match summary")
        if self.P18_2_ready != self.summary.P18_2_ready:
            raise ValueError("result P18_2 readiness must match summary")
        expected_intake_id = _intake_id_from_result(self)
        if self.intake_id != expected_intake_id:
            raise ValueError("intake_id must match deterministic intake identity")
        if self.result_SHA256 != _model_digest(
            PROJECT_INTAKE_RESULT_DIGEST_ALGORITHM, self, "result_SHA256"
        ):
            raise ValueError("result_SHA256 must match project intake result digest")
        return self


_CANONICAL_ROADMAP_TITLES: tuple[tuple[str, str], ...] = (
    ("P18.0", "Governed Workflow State Machine"),
    ("P18.1", "Project Intake Workflow"),
    ("P18.2", "Ticket Factory Runtime Integration"),
    ("P18.3", "Approval Workflow Integration"),
    ("P18.4", "Dependency-Aware Execution Queue"),
    ("P18.5", "Review and Validation Loop"),
    ("P18.6", "Retry, Incident and Rollback Workflow"),
    ("P18.7", "Manual-versus-Hermes Shadow Run"),
    ("P18.8", "Controlled Default-Mode Cutover"),
    ("P18.R", "Workflow Migration Closure"),
)


def _canonical_roadmap_item(
    index: int, ticket_id: str, title: str
) -> ProjectRoadmapItem:
    prerequisites = (
        () if ticket_id == "P18.0" else (_CANONICAL_ROADMAP_TITLES[index - 2][0],)
    )
    return _make_model(
        ProjectRoadmapItem,
        "roadmap_item_SHA256",
        PROJECT_ROADMAP_ITEM_DIGEST_ALGORITHM,
        ticket_id=ticket_id,
        title=title,
        ordinal=index,
        prerequisite_ticket_ids=prerequisites,
        completed=ticket_id == "P18.0",
        current=ticket_id == "P18.1",
        deferred=False,
    )


def _build_canonical_identity() -> ProjectIntakeIdentity:
    return _make_model(
        ProjectIntakeIdentity,
        "identity_SHA256",
        PROJECT_INTAKE_IDENTITY_DIGEST_ALGORITHM,
        project_id=_CANONICAL_PROJECT_ID,
        project_name=_CANONICAL_PROJECT_NAME,
        project_kind=ProjectIntakeProjectKind.PEPPER,
        macroproject_id=_CANONICAL_MACROPROJECT_ID,
        macroproject_title=_CANONICAL_MACROPROJECT_TITLE,
        roadmap_id=_CANONICAL_ROADMAP_ID,
    )


def _build_canonical_roadmap() -> ProjectRoadmap:
    items = tuple(
        _canonical_roadmap_item(index, ticket_id, title)
        for index, (ticket_id, title) in enumerate(_CANONICAL_ROADMAP_TITLES, start=1)
    )
    return _make_model(
        ProjectRoadmap,
        "roadmap_SHA256",
        PROJECT_ROADMAP_DIGEST_ALGORITHM,
        roadmap_id=_CANONICAL_ROADMAP_ID,
        macroproject_id=_CANONICAL_MACROPROJECT_ID,
        items=items,
        current_ticket_id="P18.1",
        completed_ticket_ids=("P18.0",),
        next_ticket_ids=("P18.2",),
    )


def _build_canonical_repository_binding(
    committed_p18_0_commit: str,
) -> ProjectRepositoryBinding:
    return _make_model(
        ProjectRepositoryBinding,
        "repository_binding_SHA256",
        PROJECT_REPOSITORY_BINDING_DIGEST_ALGORITHM,
        repository_id=_CANONICAL_REPOSITORY_ID,
        repository_display_name=_CANONICAL_REPOSITORY_DISPLAY_NAME,
        expected_branch=_CANONICAL_BRANCH,
        product_root=_CANONICAL_PRODUCT_ROOT,
        branch_parent_commit=committed_p18_0_commit,
        upstream_main_commit=_CANONICAL_UPSTREAM_MAIN_COMMIT,
        branch_policy=_CANONICAL_BRANCH_POLICY,
    )


def _build_constraint(
    constraint_id: str,
    category: ConstraintCategory,
    description: str,
    source: str,
    *,
    blocking: bool = True,
) -> ProjectIntakeConstraint:
    return _make_model(
        ProjectIntakeConstraint,
        "constraint_SHA256",
        PROJECT_INTAKE_CONSTRAINT_DIGEST_ALGORITHM,
        constraint_id=constraint_id,
        category=category,
        description=description,
        blocking=blocking,
        source=source,
    )


def _build_canonical_constraints() -> tuple[ProjectIntakeConstraint, ...]:
    return (
        _build_constraint(
            "PIC-001",
            "architecture",
            "Pepper is a customized Hermes-derived product, not an external wrapper.",
            "P18.1 product identity",
        ),
        _build_constraint(
            "PIC-002",
            "reuse",
            "Reuse and customize inherited Pepper and Hermes capabilities before replacement.",
            "P18.1 reuse-first gate",
        ),
        _build_constraint(
            "PIC-003",
            "runtime",
            "Duplicate equivalent runtime, project registry, roadmap engine or workflow state machine logic is prohibited.",
            "P18.1 reuse-first gate",
        ),
        _build_constraint(
            "PIC-004",
            "authority",
            "Human Git authority remains required; automatic Git mutation is not authorized.",
            "P17 authority boundary",
        ),
        _build_constraint(
            "PIC-005",
            "workflow",
            "Upstream Hermes setup and generic dashboard provider state are not P17 or P18 authority.",
            "P18.1 governance boundary",
        ),
        _build_constraint(
            "PIC-006",
            "security",
            "Project intake does not claim production readiness or production default operation.",
            "P18.1 authority boundary",
        ),
        _build_constraint(
            "PIC-007",
            "future_boundary",
            "Persistent shared memory and G-Brain are deferred to P19.",
            "P19 boundary",
        ),
        _build_constraint(
            "PIC-008",
            "future_boundary",
            "Paperclip durable work-control authority is deferred to P20.",
            "P20 boundary",
        ),
        _build_constraint(
            "PIC-009",
            "future_boundary",
            "Governed multi-agent automation is deferred to P21.",
            "P21 boundary",
        ),
        _build_constraint(
            "PIC-010",
            "dependency",
            "Ticket Factory runtime integration and dependency queue migration remain deferred beyond P18.1.",
            "P18.2 and P18.4 boundary",
        ),
    )


def _build_reference(
    reference_id: str,
    reference_kind: ContextReferenceKind,
    reference_name: str,
    source_scope: str,
    authority: ContextReferenceAuthority,
    *,
    required: bool,
) -> ProjectContextReference:
    return _make_model(
        ProjectContextReference,
        "reference_SHA256",
        PROJECT_CONTEXT_REFERENCE_DIGEST_ALGORITHM,
        reference_id=reference_id,
        reference_kind=reference_kind,
        reference_name=reference_name,
        source_scope=source_scope,
        authority=authority,
        required=required,
    )


def _build_canonical_references() -> tuple[ProjectContextReference, ...]:
    return (
        _build_reference(
            "PCTX-001",
            "public_contract",
            "P18.0 governed workflow state machine",
            "workflow/governed_state_machine.py",
            "canonical",
            required=True,
        ),
        _build_reference(
            "PCTX-002",
            "canonical_document",
            "P17 WorkPacket Execution MVP closure",
            "docs/agent-platform/work_packet_execution_mvp_closure.md",
            "canonical",
            required=True,
        ),
        _build_reference(
            "PCTX-003",
            "roadmap",
            "P18 manual-to-Hermes workflow migration roadmap",
            "P18 ticket inventory",
            "canonical",
            required=True,
        ),
        _build_reference(
            "PCTX-004",
            "repository_metadata",
            "Pepper repository-relative product binding",
            "AGENT PLATFORM repository metadata",
            "supporting",
            required=True,
        ),
        _build_reference(
            "PCTX-005",
            "prior_ticket",
            "P18.0 accepted workflow state-machine commit",
            "P18.0 commit identity",
            "canonical",
            required=True,
        ),
        _build_reference(
            "PCTX-006",
            "runtime_capability_analysis",
            "Existing Hermes and Pepper capability reconciliation",
            "targeted current-state revalidation",
            "supporting",
            required=True,
        ),
    )


def build_project_intake_approval(
    *,
    approved: bool,
    approved_by_human: bool,
    approval_statement: str,
) -> ProjectIntakeApproval:
    return _make_model(
        ProjectIntakeApproval,
        "approval_SHA256",
        PROJECT_INTAKE_APPROVAL_DIGEST_ALGORITHM,
        approval_required=True,
        approved=approved,
        approval_scope="P18.1 bounded Pepper project intake context",
        approved_by_human=approved_by_human,
        approval_statement=approval_statement,
    )


def build_canonical_p18_project_intake_request(
    *,
    initial_workflow_snapshot: GovernedWorkflowSnapshot,
    committed_p18_0_commit: str,
    approval: ProjectIntakeApproval,
) -> ProjectIntakeRequest:
    if approval.approved_by_human is not True:
        raise ProjectIntakePolicyError(
            "project intake approval must be approved by a human"
        )
    request = ProjectIntakeRequest(
        schema_version=PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION,
        policy_id=PROJECT_INTAKE_WORKFLOW_POLICY_ID,
        identity=_build_canonical_identity(),
        roadmap=_build_canonical_roadmap(),
        repository_binding=_build_canonical_repository_binding(committed_p18_0_commit),
        constraints=_build_canonical_constraints(),
        context_references=_build_canonical_references(),
        approval=approval,
        initial_workflow_snapshot=initial_workflow_snapshot,
    )
    validate_project_intake_request(request)
    return request


def validate_project_intake_request(request: ProjectIntakeRequest) -> None:
    try:
        validated = ProjectIntakeRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ProjectIntakeValidationError("invalid project intake request") from exc

    if validated.schema_version != PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION:
        raise ProjectIntakePolicyError("schema_version must be exact")
    if validated.policy_id != PROJECT_INTAKE_WORKFLOW_POLICY_ID:
        raise ProjectIntakePolicyError("policy_id must be exact")
    _validate_identity(validated.identity)
    _validate_roadmap(validated.roadmap)
    _validate_repository_binding(validated.repository_binding)
    _validate_constraints(validated.constraints)
    _validate_context_references(validated.context_references)
    _validate_approval_for_request(validated.approval)
    try:
        validate_governed_workflow_snapshot(validated.initial_workflow_snapshot)
    except ValueError as exc:
        raise ProjectIntakeValidationError(
            "initial workflow snapshot is invalid"
        ) from exc
    if (
        validated.initial_workflow_snapshot.current_state
        is not GovernedWorkflowState.DRAFT
    ):
        raise ProjectIntakeStateError("initial workflow state must be draft")
    if (
        validated.initial_workflow_snapshot.identity.project_id
        != _CANONICAL_MACROPROJECT_ID
    ):
        raise ProjectIntakePolicyError("workflow identity must bind P18")
    if (
        validated.initial_workflow_snapshot.identity.ticket_id
        != validated.roadmap.current_ticket_id
    ):
        raise ProjectIntakePolicyError(
            "workflow identity must bind current ticket P18.1"
        )
    if validated.initial_workflow_snapshot.runtime_projection.runtime_projection_is_authoritative_governance_state:
        raise ProjectIntakePolicyError(
            "runtime projection cannot be governance authority"
        )
    if not validated.approval.approval_required or not validated.approval.approved:
        raise ProjectIntakePolicyError(
            "project intake requires explicit human approval"
        )


def build_project_intake(request: ProjectIntakeRequest) -> ProjectIntakeResult:
    validate_project_intake_request(request)
    validated = ProjectIntakeRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    findings = _derive_findings(validated)
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=validated.initial_workflow_snapshot,
        trigger=WorkflowTransitionTrigger.PROJECT_INTAKE_COMPLETED,
        authority=WorkflowTransitionAuthority.SYSTEM,
        evidence_refs=("project_intake_evidence",),
        runtime_projection=validated.initial_workflow_snapshot.runtime_projection,
    )
    validate_governed_workflow_transition_request(transition_request)
    transition_result = build_governed_workflow_transition(transition_request)
    if not transition_result.accepted:
        raise ProjectIntakeStateError("P18.0 project-intake transition was rejected")
    if transition_result.transition.from_state is not GovernedWorkflowState.DRAFT:
        raise ProjectIntakeStateError("project intake transition must start from draft")
    if transition_result.transition.to_state is not GovernedWorkflowState.INTAKE_READY:
        raise ProjectIntakeStateError(
            "project intake transition must target intake_ready"
        )
    summary = _derive_summary(findings, transition_result)
    state = (
        ProjectIntakeState.ACCEPTED
        if summary.project_intake_requirement_satisfied
        else ProjectIntakeState.BLOCKED
    )
    decision = (
        ProjectIntakeDecision.ACCEPTED
        if summary.project_intake_requirement_satisfied
        else ProjectIntakeDecision.REJECTED
    )
    result_values = {
        "schema_version": PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION,
        "policy_id": PROJECT_INTAKE_WORKFLOW_POLICY_ID,
        "state": state,
        "decision": decision,
        "identity": validated.identity,
        "roadmap": validated.roadmap,
        "repository_binding": validated.repository_binding,
        "constraints": validated.constraints,
        "context_references": validated.context_references,
        "approval": validated.approval,
        "previous_workflow_snapshot_SHA256": validated.initial_workflow_snapshot.workflow_SHA256,
        "workflow_transition_result": transition_result,
        "resulting_workflow_snapshot": transition_result.resulting_snapshot,
        "findings": findings,
        "summary": summary,
        "project_intake_requirement_satisfied": summary.project_intake_requirement_satisfied,
        "P18_2_ready": summary.P18_2_ready,
        "production_readiness_claimed": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
    }
    result = _make_model(
        ProjectIntakeResult,
        "result_SHA256",
        PROJECT_INTAKE_RESULT_DIGEST_ALGORITHM,
        intake_id=_intake_id_from_record(result_values),
        **result_values,
    )
    validate_project_intake_result(result)
    return result


def validate_project_intake_result(result: ProjectIntakeResult) -> None:
    try:
        validated = ProjectIntakeResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ProjectIntakeValidationError("invalid project intake result") from exc
    if validated.schema_version != PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION:
        raise ProjectIntakeValidationError("result schema_version must be exact")
    if validated.policy_id != PROJECT_INTAKE_WORKFLOW_POLICY_ID:
        raise ProjectIntakeValidationError("result policy_id must be exact")
    _validate_identity(validated.identity)
    _validate_roadmap(validated.roadmap)
    _validate_repository_binding(validated.repository_binding)
    _validate_constraints(validated.constraints)
    _validate_context_references(validated.context_references)
    _validate_approval_for_request(validated.approval)
    _validate_findings(validated.findings)
    if validated.summary != _derive_summary(
        validated.findings, validated.workflow_transition_result
    ):
        raise ProjectIntakeValidationError("summary must match result findings")
    if validated.production_readiness_claimed is not False:
        raise ProjectIntakeValidationError("production readiness must be false")
    if validated.provider_dispatch_count != 0:
        raise ProjectIntakeValidationError("provider dispatch count must be zero")
    if validated.model_inference_count != 0:
        raise ProjectIntakeValidationError("model inference count must be zero")
    if validated.Git_commands_executed != 0:
        raise ProjectIntakeValidationError("Git command count must be zero")


def summarize_project_intake(result: ProjectIntakeResult) -> ProjectIntakeSummary:
    validate_project_intake_result(result)
    return result.summary


def _validate_identity(identity: ProjectIntakeIdentity) -> None:
    _validated_model(ProjectIntakeIdentity, identity)


def _validate_roadmap(roadmap: ProjectRoadmap) -> None:
    _validated_model(ProjectRoadmap, roadmap)


def _validate_repository_binding(repository_binding: ProjectRepositoryBinding) -> None:
    _validated_model(ProjectRepositoryBinding, repository_binding)


def _validate_constraints(constraints: tuple[ProjectIntakeConstraint, ...]) -> None:
    if not constraints:
        raise ProjectIntakePolicyError("constraints must be non-empty")
    if len(constraints) > 128:
        raise ProjectIntakePolicyError("constraints exceed maximum")
    ids = tuple(item.constraint_id for item in constraints)
    if len(ids) != len(set(ids)):
        raise ProjectIntakePolicyError("constraint IDs must be unique")
    for item in constraints:
        _validated_model(ProjectIntakeConstraint, item)
    descriptions = "\n".join(item.description.lower() for item in constraints)
    required_phrases = (
        "customized hermes-derived product",
        "reuse and customize inherited",
        "duplicate equivalent runtime",
        "human git authority remains required",
        "upstream hermes setup",
        "production readiness",
        "g-brain are deferred to p19",
        "paperclip durable work-control authority is deferred to p20",
        "multi-agent automation is deferred to p21",
        "ticket factory runtime integration",
    )
    for phrase in required_phrases:
        if phrase not in descriptions:
            raise ProjectIntakePolicyError(
                f"missing required project constraint: {phrase}"
            )


def _validate_context_references(
    references: tuple[ProjectContextReference, ...],
) -> None:
    if not references:
        raise ProjectIntakePolicyError("context references must be non-empty")
    if len(references) > 128:
        raise ProjectIntakePolicyError("context references exceed maximum")
    ids = tuple(item.reference_id for item in references)
    if len(ids) != len(set(ids)):
        raise ProjectIntakePolicyError("context reference IDs must be unique")
    for item in references:
        _validated_model(ProjectContextReference, item)
    if not all(item.required for item in references):
        raise ProjectIntakePolicyError(
            "canonical project intake references are required"
        )


def _validate_approval_for_request(approval: ProjectIntakeApproval) -> None:
    _validated_model(ProjectIntakeApproval, approval)
    if approval.approval_required is not True:
        raise ProjectIntakePolicyError("project intake approval is required")
    if approval.approved is not True:
        raise ProjectIntakePolicyError("project intake approval must be present")
    if approval.approved_by_human is not True:
        raise ProjectIntakePolicyError("project intake approval must be human-approved")


def _build_finding(
    finding_id: str,
    severity: ProjectIntakeFindingSeverity,
    code: ProjectIntakeFindingCode,
    subject_id: str,
    summary: str,
    failed_invariant: str | None = None,
) -> ProjectIntakeFinding:
    return _make_model(
        ProjectIntakeFinding,
        "finding_SHA256",
        PROJECT_INTAKE_FINDING_DIGEST_ALGORITHM,
        finding_id=finding_id,
        severity=severity,
        code=code,
        subject_id=subject_id,
        summary=summary,
        failed_invariant=failed_invariant,
    )


def _derive_findings(request: ProjectIntakeRequest) -> tuple[ProjectIntakeFinding, ...]:
    rows = (
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.PROJECT_ID_VALID,
            request.identity.project_id,
            "Canonical Pepper project identity is valid.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.ROADMAP_VALID,
            request.roadmap.roadmap_id,
            "Canonical P18 roadmap is valid.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.CURRENT_TICKET_VALID,
            request.roadmap.current_ticket_id,
            "P18.1 is the current governed intake ticket.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.REPOSITORY_BINDING_VALID,
            request.repository_binding.repository_id,
            "Repository binding is repository-relative and bound to P18.0.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.BRANCH_BINDING_VALID,
            request.repository_binding.expected_branch,
            "Expected P18 branch policy is valid.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.PRODUCT_ROOT_VALID,
            request.repository_binding.product_root,
            "Pepper product root is repository-relative.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.PREREQUISITE_BINDING_VALID,
            "P18.0",
            "P18.0 is completed and bound as the project-intake prerequisite.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.CONSTRAINTS_VALID,
            "P18.1 constraints",
            "Required project constraints and future boundaries are present.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.HUMAN_APPROVAL_REQUIRED,
            "human approval",
            "Project intake requires explicit human approval.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.HUMAN_APPROVAL_PRESENT,
            "human approval",
            "Human intake approval evidence is present.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.WORKFLOW_BINDING_VALID,
            request.initial_workflow_snapshot.workflow_SHA256,
            "Initial P18.0 workflow snapshot is valid and in draft state.",
        ),
        (
            ProjectIntakeFindingSeverity.INFO,
            ProjectIntakeFindingCode.INTAKE_ACCEPTED,
            "P18.1",
            "Project intake is ready to transition to intake_ready.",
        ),
    )
    return tuple(
        _build_finding(f"PINF-{index:03d}", severity, code, subject_id, summary)
        for index, (severity, code, subject_id, summary) in enumerate(rows, start=1)
    )


def _validate_findings(findings: tuple[ProjectIntakeFinding, ...]) -> None:
    if not findings:
        raise ProjectIntakeValidationError("findings must be non-empty")
    if len(findings) > 128:
        raise ProjectIntakeValidationError("findings exceed maximum")
    expected = tuple(f"PINF-{index:03d}" for index in range(1, len(findings) + 1))
    if tuple(item.finding_id for item in findings) != expected:
        raise ProjectIntakeValidationError("finding IDs must be contiguous")
    if len({item.finding_SHA256 for item in findings}) != len(findings):
        raise ProjectIntakeValidationError("finding digests must be unique")
    for item in findings:
        _validated_model(ProjectIntakeFinding, item)


def _derive_summary(
    findings: tuple[ProjectIntakeFinding, ...],
    transition_result: GovernedWorkflowTransitionResult,
) -> ProjectIntakeSummary:
    _validate_findings(findings)
    information = sum(
        item.severity is ProjectIntakeFindingSeverity.INFO for item in findings
    )
    warnings = sum(
        item.severity is ProjectIntakeFindingSeverity.WARNING for item in findings
    )
    blocking = sum(
        item.severity is ProjectIntakeFindingSeverity.BLOCKING for item in findings
    )
    transition_valid = (
        transition_result.accepted
        and transition_result.transition.from_state is GovernedWorkflowState.DRAFT
        and transition_result.transition.to_state is GovernedWorkflowState.INTAKE_READY
        and transition_result.resulting_snapshot.current_state
        is GovernedWorkflowState.INTAKE_READY
    )
    requirement = blocking == 0 and transition_valid
    return _make_model(
        ProjectIntakeSummary,
        "summary_SHA256",
        PROJECT_INTAKE_SUMMARY_DIGEST_ALGORITHM,
        project_identity_valid=blocking == 0,
        roadmap_valid=blocking == 0,
        repository_binding_valid=blocking == 0,
        constraints_valid=blocking == 0,
        context_references_valid=blocking == 0,
        human_approval_present=blocking == 0,
        workflow_transition_valid=transition_valid,
        information_finding_count=information,
        warning_finding_count=warnings,
        blocking_finding_count=blocking,
        project_intake_requirement_satisfied=requirement,
        P18_2_ready=requirement,
    )


def _intake_id_from_record(record: object) -> str:
    digest = _digest_from_record(PROJECT_INTAKE_ID_DIGEST_ALGORITHM, record)
    return f"PINT-P18-{digest[:12]}"


def _intake_id_from_result(result: ProjectIntakeResult) -> str:
    record = result.model_dump(
        mode="json",
        exclude={"intake_id", "result_SHA256"},
        warnings=False,
    )
    return _intake_id_from_record(record)


__all__ = (
    "PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION",
    "PROJECT_INTAKE_WORKFLOW_POLICY_ID",
    "ProjectIntakeState",
    "ProjectIntakeDecision",
    "ProjectIntakeProjectKind",
    "ProjectIntakeFindingSeverity",
    "ProjectIntakeFindingCode",
    "ProjectIntakeIdentity",
    "ProjectRoadmapItem",
    "ProjectRoadmap",
    "ProjectRepositoryBinding",
    "ProjectIntakeConstraint",
    "ProjectContextReference",
    "ProjectIntakeApproval",
    "ProjectIntakeRequest",
    "ProjectIntakeFinding",
    "ProjectIntakeSummary",
    "ProjectIntakeResult",
    "ProjectIntakeError",
    "ProjectIntakeInputError",
    "ProjectIntakeIntegrityError",
    "ProjectIntakePolicyError",
    "ProjectIntakeStateError",
    "ProjectIntakeValidationError",
    "build_canonical_p18_project_intake_request",
    "validate_project_intake_request",
    "build_project_intake",
    "validate_project_intake_result",
    "summarize_project_intake",
)
