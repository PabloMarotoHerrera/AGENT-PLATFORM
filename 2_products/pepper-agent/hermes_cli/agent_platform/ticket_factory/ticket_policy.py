"""Deterministic non-mutating ticket policy linting contracts."""

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

from hermes_cli.agent_platform.ticket_factory.dependency_planning import (
    TicketDependencyPlan,
    WaveDisposition,
)
from hermes_cli.agent_platform.ticket_factory.specs import (
    DependencyKind,
    DependencyScope,
    ProjectIdentifier,
    ProjectSpec,
    TicketIdentifier,
    TicketSpec,
    TicketType,
)

TICKET_POLICY_SCHEMA_VERSION = 1
TICKET_POLICY_INPUT_DIGEST_ALGORITHM = "agent-platform-ticket-policy-input-sha256-v1"
TICKET_LINT_REPORT_DIGEST_ALGORITHM = "agent-platform-ticket-lint-report-sha256-v1"


class TicketPolicyError(ValueError):
    """Base error for ticket policy linting failures."""


class TicketPolicyInputError(TicketPolicyError):
    """Raised when lint input is inconsistent with its project or plan."""


class TicketPolicyProfileName(str, Enum):
    GOVERNED_STANDARD_V1 = "governed_standard_v1"


class TicketLintSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class TicketLintScope(str, Enum):
    PROJECT = "project"
    COLLECTION = "collection"
    TICKET = "ticket"


class TicketLintDisposition(str, Enum):
    PASS = "pass"
    PASS_WITH_WARNINGS = "pass_with_warnings"
    BLOCKED = "blocked"


class TicketLintRuleCode(str, Enum):
    ALLOWED_PATHS_REQUIRED = "allowed_paths_required"
    FORBIDDEN_ACTIONS_REQUIRED = "forbidden_actions_required"
    SCOPE_EXACT_CONTRADICTION = "scope_exact_contradiction"
    REQUIRED_FORBIDDEN_ACTION_MISSING = "required_forbidden_action_missing"
    AUTHORITY_REFERENCE_REQUIRED = "authority_reference_required"
    RECOMMENDED_COMMIT_MESSAGE_REQUIRED = "recommended_commit_message_required"
    ROLLBACK_CONSTRAINT_REQUIRED = "rollback_constraint_required"
    REQUIRED_RESPONSE_SECTION_MISSING = "required_response_section_missing"
    REQUIRED_VALIDATION_STEP_MISSING = "required_validation_step_missing"
    FORBIDDEN_VALIDATION_COMMAND = "forbidden_validation_command"
    DEPENDENCY_PLAN_REQUIRED = "dependency_plan_required"
    DEPENDENCY_BLOCKED = "dependency_blocked"
    SOFT_EXTERNAL_DEPENDENCY_UNRESOLVED = "soft_external_dependency_unresolved"
    SCOPE_REVIEW_REQUIRED = "scope_review_required"
    CLOSURE_TICKET_REQUIRED = "closure_ticket_required"
    MULTIPLE_CLOSURE_TICKETS = "multiple_closure_tickets"
    CLOSURE_IDENTIFIER_TYPE_MISMATCH = "closure_identifier_type_mismatch"
    CLOSURE_IDENTIFIER_SUFFIX_INVALID = "closure_identifier_suffix_invalid"
    CLOSURE_DEPENDENCY_COVERAGE = "closure_dependency_coverage"
    DUPLICATE_TICKET_TITLE = "duplicate_ticket_title"
    DUPLICATE_COMMIT_MESSAGE = "duplicate_commit_message"
    DUPLICATE_COMPLETION_VERDICT = "duplicate_completion_verdict"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


ShortText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_reject_nul),
]
DiagnosticText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
DiagnosticIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=9, max_length=16, pattern=r"^LINT-[0-9]{4,10}$"),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]


class _TicketPolicyModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


class TicketPolicyProfile(_TicketPolicyModel):
    schema_version: Literal[1] = TICKET_POLICY_SCHEMA_VERSION
    name: TicketPolicyProfileName
    required_response_sections: tuple[ShortText, ...] = Field(min_length=1)
    required_forbidden_action_markers: tuple[ShortText, ...] = Field(min_length=1)
    authority_reference_required_ticket_types: tuple[TicketType, ...] = Field(
        min_length=1
    )
    commit_message_required_ticket_types: tuple[TicketType, ...] = Field(min_length=1)
    rollback_required_ticket_types: tuple[TicketType, ...] = Field(min_length=1)
    rollback_markers: tuple[ShortText, ...] = Field(min_length=1)
    forbidden_validation_command_markers: tuple[ShortText, ...] = Field(min_length=1)
    closure_suffixes: tuple[ShortText, ...] = Field(min_length=1)
    duplicate_title_severity: TicketLintSeverity
    duplicate_commit_message_severity: TicketLintSeverity
    duplicate_completion_verdict_severity: TicketLintSeverity

    @model_validator(mode="after")
    def _validate_profile(self) -> TicketPolicyProfile:
        for field_name in (
            "required_response_sections",
            "required_forbidden_action_markers",
            "authority_reference_required_ticket_types",
            "commit_message_required_ticket_types",
            "rollback_required_ticket_types",
            "rollback_markers",
            "forbidden_validation_command_markers",
            "closure_suffixes",
        ):
            _reject_duplicate_values(getattr(self, field_name), field_name)
        return self


class TicketLintRequest(_TicketPolicyModel):
    project_spec: ProjectSpec
    tickets: tuple[TicketSpec, ...] = Field(min_length=1, max_length=512)
    dependency_plan: TicketDependencyPlan | None = None
    collection_complete: StrictBool = False
    policy_name: TicketPolicyProfileName = TicketPolicyProfileName.GOVERNED_STANDARD_V1

    @model_validator(mode="after")
    def _validate_request(self) -> TicketLintRequest:
        _validate_request_collection(self, error_type=ValueError)
        return self


class TicketLintDiagnostic(_TicketPolicyModel):
    diagnostic_id: DiagnosticIdentifier
    code: TicketLintRuleCode
    severity: TicketLintSeverity
    scope: TicketLintScope
    ticket_id: TicketIdentifier | None
    field_path: DiagnosticText
    message: DiagnosticText
    remediation: DiagnosticText
    blocking: StrictBool

    @model_validator(mode="after")
    def _validate_diagnostic(self) -> TicketLintDiagnostic:
        if self.severity is TicketLintSeverity.ERROR and not self.blocking:
            raise ValueError("error diagnostics must be blocking")
        if self.severity is not TicketLintSeverity.ERROR and self.blocking:
            raise ValueError("non-error diagnostics must be nonblocking")
        if self.scope is TicketLintScope.TICKET and self.ticket_id is None:
            raise ValueError("ticket-scope diagnostics require ticket_id")
        if self.scope is not TicketLintScope.TICKET and self.ticket_id is not None:
            raise ValueError(
                "project and collection diagnostics must not set ticket_id"
            )
        return self


class TicketLintSummary(_TicketPolicyModel):
    ticket_count: int = Field(ge=0, strict=True)
    diagnostic_count: int = Field(ge=0, strict=True)
    error_count: int = Field(ge=0, strict=True)
    warning_count: int = Field(ge=0, strict=True)
    info_count: int = Field(ge=0, strict=True)
    blocked_ticket_ids: tuple[TicketIdentifier, ...]
    warning_ticket_ids: tuple[TicketIdentifier, ...]
    collection_blocked: StrictBool

    @model_validator(mode="after")
    def _validate_summary(self) -> TicketLintSummary:
        if self.diagnostic_count != (
            self.error_count + self.warning_count + self.info_count
        ):
            raise ValueError("diagnostic_count must equal severity counts")
        _reject_duplicate_values(self.blocked_ticket_ids, "blocked_ticket_ids")
        _reject_duplicate_values(self.warning_ticket_ids, "warning_ticket_ids")
        if tuple(sorted(self.blocked_ticket_ids, key=_ticket_sort_key)) != (
            self.blocked_ticket_ids
        ):
            raise ValueError("blocked_ticket_ids must be in canonical order")
        if tuple(sorted(self.warning_ticket_ids, key=_ticket_sort_key)) != (
            self.warning_ticket_ids
        ):
            raise ValueError("warning_ticket_ids must be in canonical order")
        if self.collection_blocked is not (self.error_count > 0):
            raise ValueError("collection_blocked must match error presence")
        return self


class TicketLintReport(_TicketPolicyModel):
    # TicketLintReport is policy evidence, not approval or publication authority.
    schema_version: Literal[1] = TICKET_POLICY_SCHEMA_VERSION
    project_id: ProjectIdentifier
    policy_name: TicketPolicyProfileName
    ticket_ids: tuple[TicketIdentifier, ...]
    lint_input_SHA256: DigestText
    diagnostics: tuple[TicketLintDiagnostic, ...]
    summary: TicketLintSummary
    disposition: TicketLintDisposition
    report_SHA256: DigestText

    @field_validator("ticket_ids", mode="after")
    @classmethod
    def _validate_ticket_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "ticket_ids")
        if tuple(sorted(value, key=_ticket_sort_key)) != value:
            raise ValueError("ticket_ids must be in canonical order")
        return value

    @model_validator(mode="after")
    def _validate_report(self) -> TicketLintReport:
        diagnostic_ids = tuple(
            diagnostic.diagnostic_id for diagnostic in self.diagnostics
        )
        _reject_duplicate_values(diagnostic_ids, "diagnostic_ids")
        expected_ids = tuple(
            _diagnostic_id(index) for index in range(1, len(self.diagnostics) + 1)
        )
        if diagnostic_ids != expected_ids:
            raise ValueError("diagnostic identifiers must be sequential")
        if (
            tuple(sorted(self.diagnostics, key=_diagnostic_sort_key))
            != self.diagnostics
        ):
            raise ValueError("diagnostics must be in deterministic order")
        expected_summary = _summary_from_diagnostics(
            ticket_count=len(self.ticket_ids), diagnostics=self.diagnostics
        )
        if self.summary != expected_summary:
            raise ValueError("summary must match diagnostics")
        if self.disposition is not _disposition_for_summary(self.summary):
            raise ValueError("disposition must match summary")
        expected_digest = _report_digest(
            schema_version=self.schema_version,
            project_id=self.project_id,
            policy_name=self.policy_name,
            ticket_ids=self.ticket_ids,
            lint_input_SHA256=self.lint_input_SHA256,
            diagnostics=self.diagnostics,
            summary=self.summary,
            disposition=self.disposition,
        )
        if self.report_SHA256 != expected_digest:
            raise ValueError("report_SHA256 must match lint report digest record")
        return self


_TICKET_ID_PATTERN = re.compile(r"^P([1-9][0-9]{0,3})((?:\.[A-Z0-9]+)+)$")
_TOKEN_PATTERN = re.compile(r"[0-9]+|[A-Z]+")
_WHITESPACE_PATTERN = re.compile(r"\s+")

_SEVERITY_RANK = {
    TicketLintSeverity.ERROR: 0,
    TicketLintSeverity.WARNING: 1,
    TicketLintSeverity.INFO: 2,
}
_SCOPE_RANK = {
    TicketLintScope.PROJECT: 0,
    TicketLintScope.COLLECTION: 1,
    TicketLintScope.TICKET: 2,
}
_RULE_CODE_RANK = {code: index for index, code in enumerate(TicketLintRuleCode)}

_CANONICAL_PROFILE = TicketPolicyProfile(
    name=TicketPolicyProfileName.GOVERNED_STANDARD_V1,
    required_response_sections=(
        "Summary",
        "Files inspected",
        "Files modified",
        "Tests/commands run",
        "Decisions made",
        "Limitations",
    ),
    required_forbidden_action_markers=(
        "git add",
        "git commit",
        "git push",
        "git reset",
        "git clean",
        "git stash",
        "git worktree",
        "Graphify",
    ),
    authority_reference_required_ticket_types=(
        TicketType.ARCHITECTURE,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    ),
    commit_message_required_ticket_types=(
        TicketType.IMPLEMENTATION,
        TicketType.REFACTOR,
        TicketType.TEST,
        TicketType.BUGFIX,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    ),
    rollback_required_ticket_types=(
        TicketType.IMPLEMENTATION,
        TicketType.REFACTOR,
        TicketType.BUGFIX,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    ),
    rollback_markers=("rollback", "restore", "revert", "remove only"),
    forbidden_validation_command_markers=(
        "git add",
        "git commit",
        "git push",
        "git reset",
        "git clean",
        "git stash",
        "git worktree add",
        "git worktree remove",
        "graphify update",
        "graphify extract",
        "graphify export",
        "graphify cluster",
        "graphify recluster",
    ),
    closure_suffixes=("R", "CR"),
    duplicate_title_severity=TicketLintSeverity.WARNING,
    duplicate_commit_message_severity=TicketLintSeverity.WARNING,
    duplicate_completion_verdict_severity=TicketLintSeverity.ERROR,
)


def get_ticket_policy_profile(
    name: TicketPolicyProfileName = TicketPolicyProfileName.GOVERNED_STANDARD_V1,
) -> TicketPolicyProfile:
    """Return the single governed ticket-policy profile."""

    if name is not TicketPolicyProfileName.GOVERNED_STANDARD_V1:
        raise TicketPolicyInputError(
            f"unknown ticket policy profile: name={name.value}"
        )
    return _CANONICAL_PROFILE


def lint_ticket_collection(request: TicketLintRequest) -> TicketLintReport:
    """Lint a ticket collection without mutating, repairing or executing it."""

    _validate_request_collection(request, error_type=TicketPolicyInputError)
    profile = get_ticket_policy_profile(request.policy_name)
    tickets = _canonical_tickets(request.tickets)
    diagnostics = _assign_diagnostic_ids(
        _collect_diagnostics(request, profile, tickets)
    )
    summary = _summary_from_diagnostics(
        ticket_count=len(tickets), diagnostics=diagnostics
    )
    disposition = _disposition_for_summary(summary)
    ticket_ids = tuple(ticket.ticket_id for ticket in tickets)
    lint_input_SHA256 = _lint_input_digest(request, profile, tickets)
    report_SHA256 = _report_digest(
        schema_version=TICKET_POLICY_SCHEMA_VERSION,
        project_id=request.project_spec.project_id,
        policy_name=request.policy_name,
        ticket_ids=ticket_ids,
        lint_input_SHA256=lint_input_SHA256,
        diagnostics=diagnostics,
        summary=summary,
        disposition=disposition,
    )
    return TicketLintReport(
        project_id=request.project_spec.project_id,
        policy_name=request.policy_name,
        ticket_ids=ticket_ids,
        lint_input_SHA256=lint_input_SHA256,
        diagnostics=diagnostics,
        summary=summary,
        disposition=disposition,
        report_SHA256=report_SHA256,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _ticket_sort_key(
    ticket_id: str,
) -> tuple[int, tuple[tuple[tuple[int, int | str], ...], ...]]:
    match = _TICKET_ID_PATTERN.match(ticket_id)
    if match is None:
        return (0, ())
    project_number = int(match.group(1))
    segments = match.group(2).strip(".").split(".")
    segment_keys: list[tuple[tuple[int, int | str], ...]] = []
    for segment in segments:
        tokens: list[tuple[int, int | str]] = []
        for token in _TOKEN_PATTERN.findall(segment):
            if token.isdigit():
                tokens.append((0, int(token)))
            else:
                tokens.append((1, token))
        segment_keys.append(tuple(tokens))
    return (project_number, tuple(segment_keys))


def _canonical_tickets(tickets: tuple[TicketSpec, ...]) -> tuple[TicketSpec, ...]:
    return tuple(sorted(tickets, key=lambda ticket: _ticket_sort_key(ticket.ticket_id)))


def _normalize_text(value: str) -> str:
    return _WHITESPACE_PATTERN.sub(" ", value.strip()).casefold()


def _normalize_rollback_text(value: str) -> str:
    return _normalize_text(value.replace("-", " "))


def _final_ticket_segment(ticket_id: str) -> str:
    return ticket_id.rsplit(".", 1)[-1]


def _diagnostic_id(index: int) -> str:
    return f"LINT-{index:04d}"


def _blocking_for_severity(severity: TicketLintSeverity) -> bool:
    return severity is TicketLintSeverity.ERROR


def _diagnostic_sort_key(diagnostic: TicketLintDiagnostic) -> tuple[object, ...]:
    return (
        _SEVERITY_RANK[diagnostic.severity],
        _SCOPE_RANK[diagnostic.scope],
        0 if diagnostic.ticket_id is None else 1,
        () if diagnostic.ticket_id is None else _ticket_sort_key(diagnostic.ticket_id),
        _RULE_CODE_RANK[diagnostic.code],
        diagnostic.field_path,
        diagnostic.message,
    )


def _base_diagnostic(
    *,
    code: TicketLintRuleCode,
    severity: TicketLintSeverity,
    scope: TicketLintScope,
    ticket_id: str | None,
    field_path: str,
    message: str,
    remediation: str,
) -> TicketLintDiagnostic:
    return TicketLintDiagnostic(
        diagnostic_id="LINT-0001",
        code=code,
        severity=severity,
        scope=scope,
        ticket_id=ticket_id,
        field_path=field_path,
        message=message,
        remediation=remediation,
        blocking=_blocking_for_severity(severity),
    )


def _assign_diagnostic_ids(
    diagnostics: tuple[TicketLintDiagnostic, ...],
) -> tuple[TicketLintDiagnostic, ...]:
    return tuple(
        diagnostic.model_copy(update={"diagnostic_id": _diagnostic_id(index)})
        for index, diagnostic in enumerate(
            sorted(diagnostics, key=_diagnostic_sort_key), start=1
        )
    )


def _validate_request_collection(
    request: TicketLintRequest, *, error_type: type[Exception]
) -> None:
    project_id = request.project_spec.project_id
    ticket_ids = tuple(ticket.ticket_id for ticket in request.tickets)
    if len(ticket_ids) != len(frozenset(ticket_ids)):
        raise error_type("ticket IDs must be unique")
    for ticket in request.tickets:
        if ticket.project_id != project_id:
            raise error_type(
                f"ticket project_id must match project: ticket_id={ticket.ticket_id}"
            )
        if not ticket.ticket_id.startswith(f"{project_id}."):
            raise error_type(
                f"ticket_id must use project prefix: ticket_id={ticket.ticket_id}"
            )
    if request.dependency_plan is not None:
        if request.dependency_plan.project_id != project_id:
            raise error_type(
                "dependency plan project_id must match project: "
                f"dependency_plan_project_id={request.dependency_plan.project_id}"
            )
        if frozenset(request.dependency_plan.ticket_ids) != frozenset(ticket_ids):
            raise error_type("dependency plan ticket set must match request tickets")


def _collect_diagnostics(
    request: TicketLintRequest,
    profile: TicketPolicyProfile,
    tickets: tuple[TicketSpec, ...],
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    diagnostics.extend(_scope_policy_diagnostics(tickets, profile))
    diagnostics.extend(_authority_policy_diagnostics(tickets, profile))
    diagnostics.extend(_commit_message_policy_diagnostics(tickets, profile))
    diagnostics.extend(_rollback_policy_diagnostics(tickets, profile))
    diagnostics.extend(_response_contract_policy_diagnostics(tickets, profile))
    diagnostics.extend(_validation_step_policy_diagnostics(tickets, profile))
    diagnostics.extend(_dependency_plan_policy_diagnostics(request))
    diagnostics.extend(_closure_policy_diagnostics(request, profile, tickets))
    diagnostics.extend(_duplicate_policy_diagnostics(tickets, profile))
    return tuple(diagnostics)


def _scope_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    for ticket in tickets:
        if not ticket.scope.allowed_paths:
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.ALLOWED_PATHS_REQUIRED,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="scope.allowed_paths",
                    message="Ticket scope must declare at least one allowed path pattern.",
                    remediation="Add explicit allowed path evidence before review.",
                )
            )
        if not ticket.scope.forbidden_actions:
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.FORBIDDEN_ACTIONS_REQUIRED,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="scope.forbidden_actions",
                    message="Ticket scope must declare forbidden actions.",
                    remediation="Add explicit forbidden-action evidence before review.",
                )
            )
        allowed_patterns = {
            _normalize_text(path): path for path in ticket.scope.allowed_paths
        }
        forbidden_patterns = {
            _normalize_text(path): path for path in ticket.scope.forbidden_paths
        }
        for normalized in sorted(
            frozenset(allowed_patterns).intersection(forbidden_patterns)
        ):
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.SCOPE_EXACT_CONTRADICTION,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="scope.allowed_paths/scope.forbidden_paths",
                    message=(
                        "Allowed and forbidden scope contain the same path pattern: "
                        f"path_pattern={allowed_patterns[normalized]}"
                    ),
                    remediation="Remove the exact contradictory declaration.",
                )
            )
        normalized_actions = tuple(
            _normalize_text(action) for action in ticket.scope.forbidden_actions
        )
        for marker in profile.required_forbidden_action_markers:
            normalized_marker = _normalize_text(marker)
            if any(normalized_marker in action for action in normalized_actions):
                continue
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.REQUIRED_FORBIDDEN_ACTION_MISSING,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="scope.forbidden_actions",
                    message=(f"Forbidden-action marker is missing: marker={marker}"),
                    remediation="Declare the missing forbidden-action marker.",
                )
            )
    return tuple(diagnostics)


def _authority_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    required_types = frozenset(profile.authority_reference_required_ticket_types)
    diagnostics: list[TicketLintDiagnostic] = []
    for ticket in tickets:
        if ticket.ticket_type not in required_types:
            continue
        if any(reference.required for reference in ticket.authority_references):
            continue
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.AUTHORITY_REFERENCE_REQUIRED,
                severity=TicketLintSeverity.ERROR,
                scope=TicketLintScope.TICKET,
                ticket_id=ticket.ticket_id,
                field_path="authority_references",
                message="Ticket type requires at least one required authority reference.",
                remediation="Add required authority evidence without resolving it here.",
            )
        )
    return tuple(diagnostics)


def _commit_message_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    required_types = frozenset(profile.commit_message_required_ticket_types)
    return tuple(
        _base_diagnostic(
            code=TicketLintRuleCode.RECOMMENDED_COMMIT_MESSAGE_REQUIRED,
            severity=TicketLintSeverity.ERROR,
            scope=TicketLintScope.TICKET,
            ticket_id=ticket.ticket_id,
            field_path="recommended_commit_message",
            message="Ticket type requires a recommended commit message.",
            remediation="Add a recommended commit message without executing Git.",
        )
        for ticket in tickets
        if ticket.ticket_type in required_types
        and ticket.recommended_commit_message is None
    )


def _rollback_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    required_types = frozenset(profile.rollback_required_ticket_types)
    markers = tuple(
        _normalize_rollback_text(marker) for marker in profile.rollback_markers
    )
    diagnostics: list[TicketLintDiagnostic] = []
    for ticket in tickets:
        if ticket.ticket_type not in required_types:
            continue
        searchable = tuple(
            _normalize_rollback_text(text)
            for text in (
                *ticket.constraints,
                *ticket.tasks,
                *ticket.acceptance_criteria,
            )
        )
        if any(marker in text for marker in markers for text in searchable):
            continue
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.ROLLBACK_CONSTRAINT_REQUIRED,
                severity=TicketLintSeverity.ERROR,
                scope=TicketLintScope.TICKET,
                ticket_id=ticket.ticket_id,
                field_path="constraints/tasks/acceptance_criteria",
                message="Ticket type requires rollback or restoration evidence.",
                remediation="Add rollback evidence to constraints, tasks or acceptance criteria.",
            )
        )
    return tuple(diagnostics)


def _response_contract_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    for ticket in tickets:
        declared = frozenset(
            _normalize_text(section)
            for section in ticket.response_contract.required_sections
        )
        for section in profile.required_response_sections:
            if _normalize_text(section) in declared:
                continue
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.REQUIRED_RESPONSE_SECTION_MISSING,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="response_contract.required_sections",
                    message=f"Required response section is missing: section={section}",
                    remediation="Add the missing response-contract section.",
                )
            )
    return tuple(diagnostics)


def _validation_step_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    markers = tuple(
        (marker, _normalize_text(marker))
        for marker in profile.forbidden_validation_command_markers
    )
    for ticket in tickets:
        if not any(step.required for step in ticket.validation_steps):
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.REQUIRED_VALIDATION_STEP_MISSING,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="validation_steps",
                    message="Ticket requires at least one required validation step.",
                    remediation="Mark at least one validation step as required.",
                )
            )
        for step in ticket.validation_steps:
            if step.command is None:
                continue
            normalized_command = _normalize_text(step.command)
            for marker, normalized_marker in markers:
                if normalized_marker not in normalized_command:
                    continue
                diagnostics.append(
                    _base_diagnostic(
                        code=TicketLintRuleCode.FORBIDDEN_VALIDATION_COMMAND,
                        severity=TicketLintSeverity.ERROR,
                        scope=TicketLintScope.TICKET,
                        ticket_id=ticket.ticket_id,
                        field_path=f"validation_steps.{step.validation_id}.command",
                        message=(
                            "Validation command contains forbidden marker: "
                            f"validation_id={step.validation_id}; marker={marker}"
                        ),
                        remediation="Replace the validation step with non-mutating evidence.",
                    )
                )
    return tuple(diagnostics)


def _dependency_plan_policy_diagnostics(
    request: TicketLintRequest,
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    plan = request.dependency_plan
    if len(request.tickets) > 1 and plan is None:
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
                severity=TicketLintSeverity.ERROR,
                scope=TicketLintScope.COLLECTION,
                ticket_id=None,
                field_path="dependency_plan",
                message="Multi-ticket collections require dependency-plan evidence.",
                remediation="Provide a matching TicketDependencyPlan.",
            )
        )
        return tuple(diagnostics)
    if plan is None:
        return tuple(diagnostics)
    blockers_by_ticket_id: dict[str, list[str]] = {}
    for blocker in plan.blockers:
        blockers_by_ticket_id.setdefault(blocker.ticket_id, []).append(
            blocker.blocked_by_ticket_id
        )
    for ticket_id in plan.blocked_ticket_ids:
        blocked_by = tuple(
            sorted(blockers_by_ticket_id.get(ticket_id, ()), key=_ticket_sort_key)
        )
        joined = ",".join(blocked_by) if blocked_by else "unknown"
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.DEPENDENCY_BLOCKED,
                severity=TicketLintSeverity.ERROR,
                scope=TicketLintScope.TICKET,
                ticket_id=ticket_id,
                field_path="dependency_plan.blocked_ticket_ids",
                message=f"Dependency plan marks ticket blocked: blocked_by_ticket_ids={joined}",
                remediation="Resolve dependency blockers before treating the ticket as ready.",
            )
        )
    for dependency_id in plan.unresolved_soft_external_dependency_ids:
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.SOFT_EXTERNAL_DEPENDENCY_UNRESOLVED,
                severity=TicketLintSeverity.WARNING,
                scope=TicketLintScope.COLLECTION,
                ticket_id=None,
                field_path="dependency_plan.unresolved_soft_external_dependency_ids",
                message=(
                    "Soft external dependency remains unresolved: "
                    f"dependency_ticket_id={dependency_id}"
                ),
                remediation="Review advisory external dependency evidence.",
            )
        )
    for wave in plan.waves:
        if wave.disposition is not WaveDisposition.SCOPE_REVIEW_REQUIRED:
            continue
        collisions = ",".join(wave.scope_collision_ids)
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.SCOPE_REVIEW_REQUIRED,
                severity=TicketLintSeverity.WARNING,
                scope=TicketLintScope.COLLECTION,
                ticket_id=None,
                field_path="dependency_plan.waves",
                message=(
                    "Ambiguous declared-scope evidence requires human review: "
                    f"wave_id={wave.wave_id}; scope_collision_ids={collisions}"
                ),
                remediation="Review ambiguous scope evidence without assuming execution safety.",
            )
        )
    return tuple(diagnostics)


def _closure_policy_diagnostics(
    request: TicketLintRequest,
    profile: TicketPolicyProfile,
    tickets: tuple[TicketSpec, ...],
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    closure_suffixes = frozenset(profile.closure_suffixes)
    closure_tickets = tuple(
        ticket for ticket in tickets if ticket.ticket_type is TicketType.CLOSURE
    )
    for ticket in tickets:
        suffix = _final_ticket_segment(ticket.ticket_id)
        if suffix in closure_suffixes and ticket.ticket_type is not TicketType.CLOSURE:
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.CLOSURE_IDENTIFIER_TYPE_MISMATCH,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="ticket_id/ticket_type",
                    message="Closure identifier suffix requires ticket_type=closure.",
                    remediation="Align the ticket identifier and ticket type manually.",
                )
            )
        if ticket.ticket_type is TicketType.CLOSURE and suffix not in closure_suffixes:
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.CLOSURE_IDENTIFIER_SUFFIX_INVALID,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket.ticket_id,
                    field_path="ticket_id",
                    message="Closure ticket identifier must end with R or CR.",
                    remediation="Rename only through the governed ticket process.",
                )
            )
    if request.collection_complete:
        if not closure_tickets:
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.CLOSURE_TICKET_REQUIRED,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.COLLECTION,
                    ticket_id=None,
                    field_path="tickets",
                    message="Complete collections require exactly one closure ticket.",
                    remediation="Add one closure ticket before final collection review.",
                )
            )
        elif len(closure_tickets) > 1:
            diagnostics.append(
                _base_diagnostic(
                    code=TicketLintRuleCode.MULTIPLE_CLOSURE_TICKETS,
                    severity=TicketLintSeverity.ERROR,
                    scope=TicketLintScope.COLLECTION,
                    ticket_id=None,
                    field_path="tickets",
                    message="Complete collections must not contain multiple closure tickets.",
                    remediation="Select one closure ticket through later human review.",
                )
            )
        elif request.dependency_plan is not None:
            diagnostics.extend(
                _closure_dependency_coverage_diagnostics(
                    closure_ticket=closure_tickets[0],
                    tickets=tickets,
                    plan=request.dependency_plan,
                )
            )
    return tuple(diagnostics)


def _closure_dependency_coverage_diagnostics(
    *,
    closure_ticket: TicketSpec,
    tickets: tuple[TicketSpec, ...],
    plan: TicketDependencyPlan,
) -> tuple[TicketLintDiagnostic, ...]:
    hard_prerequisites_by_dependent: dict[str, set[str]] = {
        ticket.ticket_id: set() for ticket in tickets
    }
    ticket_ids = frozenset(hard_prerequisites_by_dependent)
    for edge in plan.edges:
        if (
            edge.kind is DependencyKind.HARD_PREREQUISITE
            and edge.scope is DependencyScope.INTERNAL_PROJECT
            and edge.prerequisite_ticket_id in ticket_ids
            and edge.dependent_ticket_id in ticket_ids
        ):
            hard_prerequisites_by_dependent[edge.dependent_ticket_id].add(
                edge.prerequisite_ticket_id
            )
    covered: set[str] = set()
    pending = sorted(
        hard_prerequisites_by_dependent[closure_ticket.ticket_id], key=_ticket_sort_key
    )
    while pending:
        current = pending.pop(0)
        if current in covered:
            continue
        covered.add(current)
        for prerequisite in sorted(
            hard_prerequisites_by_dependent[current], key=_ticket_sort_key
        ):
            if prerequisite not in covered:
                pending.append(prerequisite)
        pending.sort(key=_ticket_sort_key)
    diagnostics: list[TicketLintDiagnostic] = []
    for ticket in tickets:
        if ticket.ticket_id == closure_ticket.ticket_id:
            continue
        if ticket.ticket_type is TicketType.CLOSURE:
            continue
        if ticket.ticket_id in covered:
            continue
        diagnostics.append(
            _base_diagnostic(
                code=TicketLintRuleCode.CLOSURE_DEPENDENCY_COVERAGE,
                severity=TicketLintSeverity.ERROR,
                scope=TicketLintScope.TICKET,
                ticket_id=closure_ticket.ticket_id,
                field_path="dependency_plan.edges",
                message=(
                    "Closure ticket lacks transitive hard coverage for ticket: "
                    f"uncovered_ticket_id={ticket.ticket_id}"
                ),
                remediation="Add explicit hard dependency coverage before closure review.",
            )
        )
    return tuple(diagnostics)


def _duplicate_policy_diagnostics(
    tickets: tuple[TicketSpec, ...], profile: TicketPolicyProfile
) -> tuple[TicketLintDiagnostic, ...]:
    diagnostics: list[TicketLintDiagnostic] = []
    diagnostics.extend(
        _duplicate_text_diagnostics(
            tickets=tickets,
            values=tuple((ticket.ticket_id, ticket.title) for ticket in tickets),
            code=TicketLintRuleCode.DUPLICATE_TICKET_TITLE,
            severity=profile.duplicate_title_severity,
            field_path="title",
            message="Ticket title duplicates an earlier canonical ticket title.",
            remediation="Choose a distinct ticket title.",
        )
    )
    diagnostics.extend(
        _duplicate_text_diagnostics(
            tickets=tickets,
            values=tuple(
                (ticket.ticket_id, ticket.recommended_commit_message)
                for ticket in tickets
                if ticket.recommended_commit_message is not None
            ),
            code=TicketLintRuleCode.DUPLICATE_COMMIT_MESSAGE,
            severity=profile.duplicate_commit_message_severity,
            field_path="recommended_commit_message",
            message="Recommended commit message duplicates an earlier canonical ticket.",
            remediation="Choose a distinct recommended commit message.",
        )
    )
    diagnostics.extend(
        _duplicate_text_diagnostics(
            tickets=tickets,
            values=tuple(
                (
                    ticket.ticket_id,
                    ticket.response_contract.completion_verdict,
                )
                for ticket in tickets
            ),
            code=TicketLintRuleCode.DUPLICATE_COMPLETION_VERDICT,
            severity=profile.duplicate_completion_verdict_severity,
            field_path="response_contract.completion_verdict",
            message="Completion verdict must uniquely identify one ticket outcome.",
            remediation="Choose a distinct completion verdict.",
        )
    )
    return tuple(diagnostics)


def _duplicate_text_diagnostics(
    *,
    tickets: tuple[TicketSpec, ...],
    values: tuple[tuple[str, str | None], ...],
    code: TicketLintRuleCode,
    severity: TicketLintSeverity,
    field_path: str,
    message: str,
    remediation: str,
) -> tuple[TicketLintDiagnostic, ...]:
    ticket_order = {ticket.ticket_id: index for index, ticket in enumerate(tickets)}
    groups: dict[str, list[str]] = {}
    for ticket_id, value in values:
        if value is None:
            continue
        groups.setdefault(_normalize_text(value), []).append(ticket_id)
    diagnostics: list[TicketLintDiagnostic] = []
    for grouped_ticket_ids in groups.values():
        if len(grouped_ticket_ids) < 2:
            continue
        ordered = tuple(sorted(grouped_ticket_ids, key=lambda item: ticket_order[item]))
        for ticket_id in ordered[1:]:
            diagnostics.append(
                _base_diagnostic(
                    code=code,
                    severity=severity,
                    scope=TicketLintScope.TICKET,
                    ticket_id=ticket_id,
                    field_path=field_path,
                    message=message,
                    remediation=remediation,
                )
            )
    return tuple(diagnostics)


def _summary_from_diagnostics(
    *, ticket_count: int, diagnostics: tuple[TicketLintDiagnostic, ...]
) -> TicketLintSummary:
    error_count = sum(
        1
        for diagnostic in diagnostics
        if diagnostic.severity is TicketLintSeverity.ERROR
    )
    warning_count = sum(
        1
        for diagnostic in diagnostics
        if diagnostic.severity is TicketLintSeverity.WARNING
    )
    info_count = sum(
        1
        for diagnostic in diagnostics
        if diagnostic.severity is TicketLintSeverity.INFO
    )
    blocked_ticket_ids = tuple(
        sorted(
            frozenset(
                diagnostic.ticket_id
                for diagnostic in diagnostics
                if diagnostic.severity is TicketLintSeverity.ERROR
                and diagnostic.ticket_id is not None
            ),
            key=_ticket_sort_key,
        )
    )
    warning_ticket_ids = tuple(
        sorted(
            frozenset(
                diagnostic.ticket_id
                for diagnostic in diagnostics
                if diagnostic.severity is TicketLintSeverity.WARNING
                and diagnostic.ticket_id is not None
            ),
            key=_ticket_sort_key,
        )
    )
    return TicketLintSummary(
        ticket_count=ticket_count,
        diagnostic_count=len(diagnostics),
        error_count=error_count,
        warning_count=warning_count,
        info_count=info_count,
        blocked_ticket_ids=blocked_ticket_ids,
        warning_ticket_ids=warning_ticket_ids,
        collection_blocked=error_count > 0,
    )


def _disposition_for_summary(summary: TicketLintSummary) -> TicketLintDisposition:
    if summary.error_count > 0:
        return TicketLintDisposition.BLOCKED
    if summary.warning_count > 0:
        return TicketLintDisposition.PASS_WITH_WARNINGS
    return TicketLintDisposition.PASS


def _lint_input_digest(
    request: TicketLintRequest,
    profile: TicketPolicyProfile,
    tickets: tuple[TicketSpec, ...],
) -> str:
    record = {
        "algorithm": TICKET_POLICY_INPUT_DIGEST_ALGORITHM,
        "project_spec": request.project_spec.model_dump(mode="json"),
        "tickets": [ticket.model_dump(mode="json") for ticket in tickets],
        "dependency_plan": (
            None
            if request.dependency_plan is None
            else request.dependency_plan.model_dump(mode="json")
        ),
        "collection_complete": request.collection_complete,
        "policy_name": request.policy_name.value,
        "policy_profile": profile.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _report_digest(
    *,
    schema_version: int,
    project_id: str,
    policy_name: TicketPolicyProfileName,
    ticket_ids: tuple[str, ...],
    lint_input_SHA256: str,
    diagnostics: tuple[TicketLintDiagnostic, ...],
    summary: TicketLintSummary,
    disposition: TicketLintDisposition,
) -> str:
    record = {
        "algorithm": TICKET_LINT_REPORT_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "project_id": project_id,
        "policy_name": policy_name.value,
        "ticket_ids": list(ticket_ids),
        "lint_input_SHA256": lint_input_SHA256,
        "diagnostics": [
            diagnostic.model_dump(mode="json") for diagnostic in diagnostics
        ],
        "summary": summary.model_dump(mode="json"),
        "disposition": disposition.value,
    }
    return _sha256_text(_deterministic_json(record))
