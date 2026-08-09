"""Immutable planning contracts for Pepper project and ticket specs.

The contracts in this module are inert Pydantic models. They validate planning
data only; they do not load files, inspect repositories, resolve dependencies,
or execute validation commands.
"""

from __future__ import annotations

from enum import Enum
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

PROJECT_SPEC_SCHEMA_VERSION = 1
TICKET_SPEC_SCHEMA_VERSION = 1
_NUMERIC_PROJECT_IDENTIFIER_PATTERN = r"P[1-9][0-9]{0,3}"
_P_NUMERIC_SHAPED_IDENTIFIER_PATTERN = r"P[0-9]+"
_PRODUCT_PROJECT_IDENTIFIER_PATTERN = r"[A-Z][A-Z0-9_]{1,31}"
_PROJECT_IDENTIFIER_PATTERN = rf"^(?:{_NUMERIC_PROJECT_IDENTIFIER_PATTERN}|{_PRODUCT_PROJECT_IDENTIFIER_PATTERN})$"
_NUMERIC_PROJECT_IDENTIFIER_RE = re.compile(rf"^{_NUMERIC_PROJECT_IDENTIFIER_PATTERN}$")
_P_NUMERIC_SHAPED_IDENTIFIER_RE = re.compile(
    rf"^{_P_NUMERIC_SHAPED_IDENTIFIER_PATTERN}$"
)


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_whitespace(value: str) -> str:
    if any(character.isspace() for character in value):
        raise ValueError("value must not contain whitespace")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


def _validate_project_identifier(value: str) -> str:
    if _P_NUMERIC_SHAPED_IDENTIFIER_RE.fullmatch(
        value
    ) and not _NUMERIC_PROJECT_IDENTIFIER_RE.fullmatch(value):
        raise ValueError("numeric project identifier must be P1 through P9999")
    return value


def _ticket_namespace(ticket_id: str) -> str:
    return ticket_id.split(".", 1)[0]


def _ticket_id_matches_project(project_id: str, ticket_id: str) -> bool:
    ticket_namespace = _ticket_namespace(ticket_id)
    if ticket_namespace == project_id:
        return True
    if _NUMERIC_PROJECT_IDENTIFIER_RE.fullmatch(project_id):
        return False
    return _NUMERIC_PROJECT_IDENTIFIER_RE.fullmatch(ticket_namespace) is not None


def _ticket_ids_share_project_namespace(
    project_id: str, ticket_id: str, dependency_ticket_id: str
) -> bool:
    if _NUMERIC_PROJECT_IDENTIFIER_RE.fullmatch(project_id):
        return _ticket_namespace(dependency_ticket_id) == project_id
    return _ticket_namespace(dependency_ticket_id) == _ticket_namespace(ticket_id)


def _validate_repository_path_pattern(value: str) -> str:
    if "\x00" in value:
        raise ValueError("repository path pattern must not contain NUL characters")
    if "\\" in value:
        raise ValueError("repository path pattern must use forward slashes")
    if value.startswith("/"):
        raise ValueError("repository path pattern must be relative")
    if len(value) >= 2 and value[1] == ":" and value[0].isalpha():
        raise ValueError("repository path pattern must not be a Windows drive path")
    if "`" in value:
        raise ValueError("repository path pattern must not contain backticks")
    components = value.split("/")
    if any(component == ".." for component in components):
        raise ValueError("repository path pattern must not contain parent traversal")
    return value


ShortText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_reject_nul),
]
LongText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=8192),
    AfterValidator(_reject_nul),
]
VerdictToken: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=1,
        max_length=256,
        pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$",
    ),
]
RepositoryPathPattern: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_validate_repository_path_pattern),
]
ValidationIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=2, max_length=32, pattern=r"^V[1-9][0-9]*$"),
]
ProjectIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=2, max_length=32, pattern=_PROJECT_IDENTIFIER_PATTERN),
    AfterValidator(_validate_project_identifier),
]
TicketIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=4,
        max_length=64,
        pattern=r"^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$",
    ),
]


class TicketType(str, Enum):
    ARCHITECTURE = "architecture"
    DOCUMENTATION = "documentation"
    IMPLEMENTATION = "implementation"
    REFACTOR = "refactor"
    TEST = "test"
    BUGFIX = "bugfix"
    INTEGRATION = "integration"
    CLOSURE = "closure"


class DependencyKind(str, Enum):
    HARD_PREREQUISITE = "hard_prerequisite"
    SOFT_PREDECESSOR = "soft_predecessor"


class DependencyScope(str, Enum):
    INTERNAL_PROJECT = "internal_project"
    EXTERNAL_PROJECT = "external_project"


class ParallelizationHint(str, Enum):
    UNSPECIFIED = "unspecified"
    SERIAL = "serial"
    PARALLEL_CANDIDATE = "parallel_candidate"


class AuthorityReferenceKind(str, Enum):
    TICKET = "ticket"
    GOVERNANCE_RECORD = "governance_record"
    REPOSITORY_PATH = "repository_path"
    COMMIT = "commit"
    EXTERNAL_SOURCE = "external_source"


class _TicketFactoryModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


def _reject_duplicate_values(values: tuple[str, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


def _reject_duplicate_authority_references(
    references: tuple[AuthorityReferenceSpec, ...],
) -> None:
    pairs = tuple((reference.kind, reference.value) for reference in references)
    if len(pairs) != len(frozenset(pairs)):
        raise ValueError(
            "authority_references must not contain duplicate kind/value pairs"
        )


class AuthorityReferenceSpec(_TicketFactoryModel):
    kind: AuthorityReferenceKind
    value: ShortText
    rationale: ShortText
    required: StrictBool = True


class TicketDependencySpec(_TicketFactoryModel):
    ticket_id: TicketIdentifier
    kind: DependencyKind
    scope: DependencyScope
    rationale: ShortText


class RepositoryScopeSpec(_TicketFactoryModel):
    allowed_paths: tuple[RepositoryPathPattern, ...]
    forbidden_paths: tuple[RepositoryPathPattern, ...]
    allowed_actions: tuple[ShortText, ...]
    forbidden_actions: tuple[ShortText, ...]

    @model_validator(mode="after")
    def _validate_scope(self) -> RepositoryScopeSpec:
        for field_name in (
            "allowed_paths",
            "forbidden_paths",
            "allowed_actions",
            "forbidden_actions",
        ):
            _reject_duplicate_values(getattr(self, field_name), field_name)
        if not (
            self.allowed_paths
            or self.forbidden_paths
            or self.allowed_actions
            or self.forbidden_actions
        ):
            raise ValueError("at least one repository scope field must be non-empty")
        return self


class TicketValidationStepSpec(_TicketFactoryModel):
    validation_id: ValidationIdentifier
    description: ShortText
    command: LongText | None
    expected_result: LongText
    required: StrictBool = True


class TicketResponseContractSpec(_TicketFactoryModel):
    required_sections: tuple[ShortText, ...] = Field(min_length=1)
    completion_verdict: VerdictToken
    include_files_inspected: StrictBool = True
    include_files_modified: StrictBool = True
    include_commands_run: StrictBool = True
    include_tests_run: StrictBool = True
    include_limitations: StrictBool = True

    @field_validator("required_sections", mode="after")
    @classmethod
    def _validate_required_sections(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "required_sections")
        return value


class ProjectSpec(_TicketFactoryModel):
    schema_version: Literal[1] = PROJECT_SPEC_SCHEMA_VERSION
    project_id: ProjectIdentifier
    title: ShortText
    objective: LongText
    summary: LongText
    context: tuple[LongText, ...] = Field(min_length=1)
    authority_references: tuple[AuthorityReferenceSpec, ...]
    scope: RepositoryScopeSpec
    constraints: tuple[LongText, ...]
    non_goals: tuple[LongText, ...]
    acceptance_criteria: tuple[LongText, ...] = Field(min_length=1)
    completion_verdict: VerdictToken

    @model_validator(mode="after")
    def _validate_project_spec(self) -> ProjectSpec:
        _reject_duplicate_values(self.context, "context")
        _reject_duplicate_authority_references(self.authority_references)
        _reject_duplicate_values(self.constraints, "constraints")
        _reject_duplicate_values(self.non_goals, "non_goals")
        _reject_duplicate_values(self.acceptance_criteria, "acceptance_criteria")
        return self


class TicketSpec(_TicketFactoryModel):
    schema_version: Literal[1] = TICKET_SPEC_SCHEMA_VERSION
    project_id: ProjectIdentifier
    ticket_id: TicketIdentifier
    title: ShortText
    ticket_type: TicketType
    objective: LongText
    context: tuple[LongText, ...] = Field(min_length=1)
    authority_references: tuple[AuthorityReferenceSpec, ...]
    dependencies: tuple[TicketDependencySpec, ...]
    # ParallelizationHint is not execution authority.
    parallelization_hint: ParallelizationHint = ParallelizationHint.UNSPECIFIED
    scope: RepositoryScopeSpec
    constraints: tuple[LongText, ...]
    tasks: tuple[LongText, ...] = Field(min_length=1)
    acceptance_criteria: tuple[LongText, ...] = Field(min_length=1)
    validation_steps: tuple[TicketValidationStepSpec, ...] = Field(min_length=1)
    response_contract: TicketResponseContractSpec
    recommended_commit_message: ShortText | None = None

    @model_validator(mode="after")
    def _validate_ticket_spec(self) -> TicketSpec:
        if not _ticket_id_matches_project(self.project_id, self.ticket_id):
            raise ValueError("ticket_id must use the project_id prefix")
        dependency_ids = tuple(dependency.ticket_id for dependency in self.dependencies)
        if self.ticket_id in dependency_ids:
            raise ValueError("ticket dependencies must not include the ticket itself")
        _reject_duplicate_values(dependency_ids, "dependencies")
        _reject_duplicate_authority_references(self.authority_references)
        _reject_duplicate_values(self.context, "context")
        _reject_duplicate_values(self.constraints, "constraints")
        _reject_duplicate_values(self.tasks, "tasks")
        _reject_duplicate_values(self.acceptance_criteria, "acceptance_criteria")
        validation_ids = tuple(step.validation_id for step in self.validation_steps)
        _reject_duplicate_values(validation_ids, "validation_steps")
        return self
