"""Frozen in-memory historical regression corpus for Ticket Factory contracts.

Historical expectations are frozen regression oracles and must not be derived
from the current observed outputs during a corpus run.
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
    ValidationError,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory.approval_publishing import (
    HumanApprovalDecision,
    HumanApprovalEvidence,
    TicketApprovalRecord,
    TicketApprovalRequest,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    TicketPublicationResult,
    build_ticket_approval_record,
    publish_canonical_ticket,
)
from hermes_cli.agent_platform.ticket_factory.context_packs import (
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPriority,
    ContextSensitivity,
    ContextSourceKind,
    ContextSourceSpec,
    assemble_context_pack,
)
from hermes_cli.agent_platform.ticket_factory.dependency_planning import (
    TicketDependencyPlan,
    TicketPlanningRequest,
    build_ticket_dependency_plan,
)
from hermes_cli.agent_platform.ticket_factory.generator_roles import (
    TicketGenerationRequest,
    TicketGeneratorRole,
    build_ticket_proposal,
    prepare_ticket_generator_assignments,
)
from hermes_cli.agent_platform.ticket_factory.proposal_synthesis import (
    ReviewedTicketProposal,
    TicketSynthesisRequest,
    TicketSynthesisReview,
    build_ticket_synthesis_review,
)
from hermes_cli.agent_platform.ticket_factory.specs import (
    AuthorityReferenceKind,
    ProjectSpec,
    TicketSpec,
)
from hermes_cli.agent_platform.ticket_factory.ticket_policy import (
    TicketLintReport,
    TicketLintRequest,
    lint_ticket_collection,
)

HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION = 1
HISTORICAL_REGRESSION_CORPUS_ID = "pepper-ticket-factory-historical-regression-v1"
HISTORICAL_REGRESSION_CORPUS_REVISION = 1

CASE_DIGEST_ALGORITHM = "agent-platform-historical-regression-case-sha256-v1"
CORPUS_DIGEST_ALGORITHM = "agent-platform-historical-regression-corpus-sha256-v1"
OUTPUT_DIGEST_ALGORITHM = "agent-platform-historical-regression-output-sha256-v1"
OBSERVATION_DIGEST_ALGORITHM = (
    "agent-platform-historical-regression-observation-sha256-v1"
)
CASE_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-historical-regression-case-result-sha256-v1"
)
RUN_DIGEST_ALGORITHM = "agent-platform-historical-regression-run-sha256-v1"

MAX_FIXTURE_JSON_BYTES = 1_048_576
_P16_6_COMMIT_SHA = "3245b93074fd2218cb9f98ba3d25e53cf9bfbec1"


class HistoricalRegressionError(ValueError):
    """Base error for historical regression corpus failures."""


class HistoricalRegressionCorpusError(HistoricalRegressionError):
    """Raised when corpus or case integrity is invalid."""


class HistoricalRegressionExecutionError(HistoricalRegressionError):
    """Raised when fixed dispatch cannot execute a structurally valid case."""


class HistoricalRegressionStage(str, Enum):
    TICKET_SPEC_VALIDATION = "ticket_spec_validation"
    DEPENDENCY_PLANNING = "dependency_planning"
    TICKET_POLICY_LINT = "ticket_policy_lint"
    PROPOSAL_SYNTHESIS = "proposal_synthesis"
    HUMAN_APPROVAL = "human_approval"
    CANONICAL_PUBLICATION = "canonical_publication"


class HistoricalRegressionCaseClass(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BOUNDARY = "boundary"


class HistoricalProvenanceKind(str, Enum):
    CURRENT_CANONICAL_GOVERNANCE = "current_canonical_governance"
    READ_ONLY_GIT_HISTORY = "read_only_git_history"
    SANITIZED_SYNTHETIC_DERIVATION = "sanitized_synthetic_derivation"


class HistoricalRegressionExpectedOutcome(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class HistoricalRegressionDriftKind(str, Enum):
    UNEXPECTED_SUCCESS = "unexpected_success"
    UNEXPECTED_ERROR = "unexpected_error"
    OUTPUT_TYPE_MISMATCH = "output_type_mismatch"
    OUTPUT_DIGEST_MISMATCH = "output_digest_mismatch"
    EXCEPTION_TYPE_MISMATCH = "exception_type_mismatch"
    EXCEPTION_MESSAGE_MISMATCH = "exception_message_mismatch"


class HistoricalRegressionRunDisposition(str, Enum):
    PASS = "pass"
    DRIFT_DETECTED = "drift_detected"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


_WINDOWS_USER_PATH = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+", re.IGNORECASE)
_POSIX_USER_PATH = re.compile(r"(^|\s)/home/[^/\s]+/")
_GIT_SHA = re.compile(r"^[a-f0-9]{40}$")
_DIGEST = re.compile(r"^[a-f0-9]{64}$")
_WHITESPACE = re.compile(r"\s+")

_SENSITIVE_MARKERS = (
    "sk-",
    "bearer ",
    "private key",
    "credential content",
    "secret token",
    "prompt dump",
    "reasoning trace",
    "provider response",
)
_DELETED_FILENAME_MARKERS = (
    "deleted historical markdown",
    "obsolete prerequisite filename",
    "restored historical ticket",
)


def _reject_sensitive_or_local_text(value: str) -> str:
    lowered = value.casefold()
    if _WINDOWS_USER_PATH.search(value) or _POSIX_USER_PATH.search(value):
        raise ValueError("text must not contain personal absolute paths")
    if any(marker in lowered for marker in _SENSITIVE_MARKERS):
        raise ValueError(
            "text must not contain secret-shaped or raw transcript content"
        )
    if any(marker in lowered for marker in _DELETED_FILENAME_MARKERS):
        raise ValueError("deleted filenames must not be used as authority")
    return value


BoundedIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=1, max_length=96, pattern=r"^[A-Za-z][A-Za-z0-9_:-]*$"
    ),
]
BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
    AfterValidator(_reject_sensitive_or_local_text),
]
BoundedOptionalText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    AfterValidator(_reject_nul),
    AfterValidator(_reject_sensitive_or_local_text),
]
BoundedFreeText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=0, max_length=512),
    AfterValidator(_reject_nul),
    AfterValidator(_reject_sensitive_or_local_text),
]
HistoricalCaseIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=8, max_length=8, pattern=r"^HIST-[0-9]{3}$"),
]
ProvenanceIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=9, max_length=32, pattern=r"^PROV-HIST-[0-9]{3}$"),
]
TicketIdentifierOrNone: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=4, max_length=64, pattern=r"^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$"
    ),
]
GitSHAOrNone: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=40, max_length=40, pattern=r"^[a-f0-9]{40}$"),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]
TagIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=1, max_length=64, pattern=r"^[a-z0-9]+(?:[-_][a-z0-9]+)*$"
    ),
]
DriftIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=10, max_length=10, pattern=r"^DRIFT-[0-9]{4}$"),
]
FixtureJSONText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=1, max_length=MAX_FIXTURE_JSON_BYTES),
    AfterValidator(_reject_nul),
]


class _HistoricalRegressionModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


class HistoricalTicketProvenance(_HistoricalRegressionModel):
    provenance_id: ProvenanceIdentifier
    kind: HistoricalProvenanceKind
    source_ticket_id: TicketIdentifierOrNone | None
    source_reference: BoundedText
    source_commit_SHA: GitSHAOrNone | None
    sanitized: Literal[True]
    rationale: BoundedText

    @model_validator(mode="after")
    def _validate_provenance(self) -> HistoricalTicketProvenance:
        if self.kind is HistoricalProvenanceKind.READ_ONLY_GIT_HISTORY:
            if self.source_commit_SHA is None:
                raise ValueError(
                    "read-only Git history provenance requires source_commit_SHA"
                )
        elif self.source_commit_SHA is not None:
            raise ValueError(
                "source_commit_SHA is allowed only for read-only Git history"
            )
        return self


class HistoricalRegressionExpectation(_HistoricalRegressionModel):
    outcome: HistoricalRegressionExpectedOutcome
    output_type: BoundedIdentifier | None
    output_SHA256: DigestText | None
    exception_type: BoundedIdentifier | None
    exception_message_fragment: BoundedOptionalText | None

    @model_validator(mode="after")
    def _validate_expectation(self) -> HistoricalRegressionExpectation:
        if self.outcome is HistoricalRegressionExpectedOutcome.SUCCESS:
            if self.output_type is None or self.output_SHA256 is None:
                raise ValueError("success expectations require output type and digest")
            if (
                self.exception_type is not None
                or self.exception_message_fragment is not None
            ):
                raise ValueError(
                    "success expectations must not include exception fields"
                )
        else:
            if self.output_type is not None or self.output_SHA256 is not None:
                raise ValueError("error expectations must not include output fields")
            if self.exception_type is None or self.exception_message_fragment is None:
                raise ValueError(
                    "error expectations require exception type and fragment"
                )
        return self


class HistoricalRegressionCase(_HistoricalRegressionModel):
    case_id: HistoricalCaseIdentifier
    name: BoundedText
    case_class: HistoricalRegressionCaseClass
    description: BoundedText
    provenance: HistoricalTicketProvenance
    stage: HistoricalRegressionStage
    input_JSON: FixtureJSONText
    expectation: HistoricalRegressionExpectation
    tags: tuple[TagIdentifier, ...] = Field(min_length=1)
    case_SHA256: DigestText

    @field_validator("input_JSON", mode="after")
    @classmethod
    def _validate_input_json(cls, value: str) -> str:
        _validate_canonical_fixture_json(value)
        _reject_sensitive_or_local_text(value)
        return value

    @field_validator("tags", mode="after")
    @classmethod
    def _validate_tags(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        _reject_duplicate_values(value, "tags")
        return value

    @model_validator(mode="after")
    def _validate_case(self) -> HistoricalRegressionCase:
        if int(self.case_id.rsplit("-", 1)[1]) <= 0:
            raise ValueError("case ID must be positive")
        expected = _case_digest(self)
        if self.case_SHA256 != expected:
            raise ValueError("case_SHA256 must match historical case digest")
        return self


class HistoricalRegressionCorpus(_HistoricalRegressionModel):
    schema_version: Literal[1] = HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION
    corpus_id: Literal["pepper-ticket-factory-historical-regression-v1"] = (
        HISTORICAL_REGRESSION_CORPUS_ID
    )
    revision: Literal[1] = HISTORICAL_REGRESSION_CORPUS_REVISION
    cases: tuple[HistoricalRegressionCase, ...] = Field(min_length=12, max_length=12)
    corpus_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_corpus(self) -> HistoricalRegressionCorpus:
        _validate_corpus_invariants(self)
        return self


class HistoricalRegressionObservation(_HistoricalRegressionModel):
    stage: HistoricalRegressionStage
    outcome: HistoricalRegressionExpectedOutcome
    output_type: BoundedIdentifier | None
    output_SHA256: DigestText | None
    exception_type: BoundedIdentifier | None
    exception_message: BoundedFreeText | None
    observation_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_observation(self) -> HistoricalRegressionObservation:
        if self.outcome is HistoricalRegressionExpectedOutcome.SUCCESS:
            if self.output_type is None or self.output_SHA256 is None:
                raise ValueError("success observations require output type and digest")
            if self.exception_type is not None or self.exception_message is not None:
                raise ValueError(
                    "success observations must not include exception fields"
                )
        else:
            if self.output_type is not None or self.output_SHA256 is not None:
                raise ValueError("error observations must not include output fields")
            if self.exception_type is None or self.exception_message is None:
                raise ValueError("error observations require exception evidence")
        if self.observation_SHA256 != _observation_digest(self):
            raise ValueError("observation_SHA256 must match observation digest")
        return self


class HistoricalRegressionDrift(_HistoricalRegressionModel):
    drift_id: DriftIdentifier
    case_id: HistoricalCaseIdentifier
    kind: HistoricalRegressionDriftKind
    expected_value: BoundedFreeText | None
    observed_value: BoundedFreeText | None
    message: BoundedText
    blocking: Literal[True]


class HistoricalRegressionCaseResult(_HistoricalRegressionModel):
    case_id: HistoricalCaseIdentifier
    matched: StrictBool
    observation: HistoricalRegressionObservation
    drifts: tuple[HistoricalRegressionDrift, ...]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> HistoricalRegressionCaseResult:
        if self.matched and self.drifts:
            raise ValueError("matched case results must not include drifts")
        if not self.matched and not self.drifts:
            raise ValueError("drifted case results require drift records")
        drift_ids = tuple(drift.drift_id for drift in self.drifts)
        _reject_duplicate_values(drift_ids, "drift_ids")
        for drift in self.drifts:
            if drift.case_id != self.case_id:
                raise ValueError("drift case_id must match case result")
        if self.result_SHA256 != _case_result_digest(self):
            raise ValueError("result_SHA256 must match case result digest")
        return self


class HistoricalRegressionRun(_HistoricalRegressionModel):
    schema_version: Literal[1] = HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION
    corpus_id: BoundedIdentifier
    corpus_SHA256: DigestText
    case_results: tuple[HistoricalRegressionCaseResult, ...] = Field(min_length=1)
    passed_case_ids: tuple[HistoricalCaseIdentifier, ...]
    drifted_case_ids: tuple[HistoricalCaseIdentifier, ...]
    disposition: HistoricalRegressionRunDisposition
    run_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_run(self) -> HistoricalRegressionRun:
        result_ids = tuple(result.case_id for result in self.case_results)
        passed = tuple(result.case_id for result in self.case_results if result.matched)
        drifted = tuple(
            result.case_id for result in self.case_results if not result.matched
        )
        if self.passed_case_ids != passed:
            raise ValueError("passed_case_ids must follow passing case results")
        if self.drifted_case_ids != drifted:
            raise ValueError("drifted_case_ids must follow drifted case results")
        if set(passed).intersection(drifted):
            raise ValueError("passed and drifted case IDs must not overlap")
        if set(passed).union(drifted) != set(result_ids):
            raise ValueError("passed and drifted case IDs must partition results")
        expected_disposition = (
            HistoricalRegressionRunDisposition.PASS
            if not drifted
            else HistoricalRegressionRunDisposition.DRIFT_DETECTED
        )
        if self.disposition is not expected_disposition:
            raise ValueError("run disposition must match drifted case IDs")
        if self.run_SHA256 != _run_digest(self):
            raise ValueError("run_SHA256 must match historical run digest")
        return self


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


def _validate_canonical_fixture_json(value: str) -> None:
    if len(value.encode("utf-8")) > MAX_FIXTURE_JSON_BYTES:
        raise ValueError("fixture JSON exceeds maximum byte length")
    try:
        parsed = json.loads(value)
    except ValueError as exc:
        raise ValueError("fixture JSON must parse") from exc
    if _deterministic_json(parsed) != value:
        raise ValueError("fixture JSON must use canonical compact sorted encoding")


def _case_digest(case: HistoricalRegressionCase) -> str:
    record = case.model_dump(mode="json", exclude={"case_SHA256"})
    return _sha256_text(
        _deterministic_json({"algorithm": CASE_DIGEST_ALGORITHM, **record})
    )


def _corpus_digest(corpus: HistoricalRegressionCorpus) -> str:
    record = corpus.model_dump(mode="json", exclude={"corpus_SHA256"})
    return _sha256_text(
        _deterministic_json({"algorithm": CORPUS_DIGEST_ALGORITHM, **record})
    )


def _output_digest(output: BaseModel) -> str:
    return _sha256_text(_deterministic_json(output.model_dump(mode="json")))


def _observation_digest(observation: HistoricalRegressionObservation) -> str:
    record = observation.model_dump(mode="json", exclude={"observation_SHA256"})
    return _sha256_text(
        _deterministic_json({"algorithm": OBSERVATION_DIGEST_ALGORITHM, **record})
    )


def _case_result_digest(result: HistoricalRegressionCaseResult) -> str:
    record = result.model_dump(mode="json", exclude={"result_SHA256"})
    return _sha256_text(
        _deterministic_json({"algorithm": CASE_RESULT_DIGEST_ALGORITHM, **record})
    )


def _run_digest(run: HistoricalRegressionRun) -> str:
    record = run.model_dump(mode="json", exclude={"run_SHA256"})
    return _sha256_text(
        _deterministic_json({"algorithm": RUN_DIGEST_ALGORITHM, **record})
    )


def _case_number(case_id: str) -> int:
    return int(case_id.rsplit("-", 1)[1])


def _validate_corpus_invariants(corpus: HistoricalRegressionCorpus) -> None:
    if corpus.schema_version != HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION:
        raise ValueError("invalid historical regression corpus schema version")
    if corpus.corpus_id != HISTORICAL_REGRESSION_CORPUS_ID:
        raise ValueError("invalid historical regression corpus ID")
    if corpus.revision != HISTORICAL_REGRESSION_CORPUS_REVISION:
        raise ValueError("invalid historical regression corpus revision")
    if len(corpus.cases) != 12:
        raise ValueError("historical regression corpus must contain exactly 12 cases")
    case_ids = tuple(case.case_id for case in corpus.cases)
    _reject_duplicate_values(case_ids, "case_ids")
    if tuple(sorted(case_ids, key=_case_number)) != case_ids:
        raise ValueError("case IDs must be in ascending numeric order")
    _reject_duplicate_values(tuple(case.name for case in corpus.cases), "case_names")
    _reject_duplicate_values(
        tuple(case.case_SHA256 for case in corpus.cases), "case_digests"
    )
    for case in corpus.cases:
        _validate_canonical_fixture_json(case.input_JSON)
        if case.case_SHA256 != _case_digest(case):
            raise ValueError(f"case digest mismatch: case_id={case.case_id}")
    _validate_composition(corpus.cases)
    if corpus.corpus_SHA256 != _corpus_digest(corpus):
        raise ValueError("corpus_SHA256 must match historical corpus digest")


def _validate_composition(cases: tuple[HistoricalRegressionCase, ...]) -> None:
    stage_counts = {stage: 0 for stage in HistoricalRegressionStage}
    class_counts = {case_class: 0 for case_class in HistoricalRegressionCaseClass}
    provenance_counts = {kind: 0 for kind in HistoricalProvenanceKind}
    for case in cases:
        stage_counts[case.stage] += 1
        class_counts[case.case_class] += 1
        provenance_counts[case.provenance.kind] += 1
    if any(count != 2 for count in stage_counts.values()):
        raise ValueError("each historical regression stage must have exactly two cases")
    if class_counts[HistoricalRegressionCaseClass.ACCEPTED] < 4:
        raise ValueError("accepted case coverage is insufficient")
    if class_counts[HistoricalRegressionCaseClass.REJECTED] < 4:
        raise ValueError("rejected case coverage is insufficient")
    if class_counts[HistoricalRegressionCaseClass.BOUNDARY] < 2:
        raise ValueError("boundary case coverage is insufficient")
    if provenance_counts[HistoricalProvenanceKind.CURRENT_CANONICAL_GOVERNANCE] < 4:
        raise ValueError("current-governance provenance coverage is insufficient")
    if provenance_counts[HistoricalProvenanceKind.READ_ONLY_GIT_HISTORY] < 2:
        raise ValueError("read-only Git-history provenance coverage is insufficient")
    if provenance_counts[HistoricalProvenanceKind.SANITIZED_SYNTHETIC_DERIVATION] < 2:
        raise ValueError("synthetic provenance coverage is insufficient")


def _expectation(
    *,
    outcome: str,
    output_type: str | None = None,
    output_SHA256: str | None = None,
    exception_type: str | None = None,
    exception_message_fragment: str | None = None,
) -> HistoricalRegressionExpectation:
    return HistoricalRegressionExpectation(
        outcome=HistoricalRegressionExpectedOutcome(outcome),
        output_type=output_type,
        output_SHA256=output_SHA256,
        exception_type=exception_type,
        exception_message_fragment=exception_message_fragment,
    )


_REQUIRED_RESPONSE_SECTIONS = (
    "Summary",
    "Files inspected",
    "Files modified",
    "Tests/commands run",
    "Decisions made",
    "Limitations",
)
_FORBIDDEN_ACTIONS = (
    "git add",
    "git commit",
    "git push",
    "git reset",
    "git clean",
    "git stash",
    "git worktree",
    "Graphify",
)


def _authority_reference() -> dict[str, object]:
    return {
        "kind": AuthorityReferenceKind.GOVERNANCE_RECORD.value,
        "value": "0_architecture/governance/agent_platform_pepper_historical_ticket_regression_corpus.md",
        "rationale": "Synthetic current-governance authority reference.",
        "required": True,
    }


def _scope(
    path: str, forbidden_actions: tuple[str, ...] = _FORBIDDEN_ACTIONS
) -> dict[str, object]:
    return {
        "allowed_paths": [path],
        "forbidden_paths": ["4_external/sources/**"],
        "allowed_actions": ["edit frozen in-memory historical regression corpus"],
        "forbidden_actions": list(forbidden_actions),
    }


def _response_contract(
    verdict: str, sections: tuple[str, ...] = _REQUIRED_RESPONSE_SECTIONS
) -> dict[str, object]:
    return {
        "required_sections": list(sections),
        "completion_verdict": verdict,
        "include_files_inspected": True,
        "include_files_modified": True,
        "include_commands_run": True,
        "include_tests_run": True,
        "include_limitations": True,
    }


def _validation_step() -> dict[str, object]:
    return {
        "validation_id": "V1",
        "description": "Run the synthetic historical regression validation.",
        "command": "python -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_historical_regression.py",
        "expected_result": "The synthetic validation reports success.",
        "required": True,
    }


def _dependency(ticket_id: str) -> dict[str, object]:
    return {
        "ticket_id": ticket_id,
        "kind": "hard_prerequisite",
        "scope": "internal_project",
        "rationale": "Synthetic dependency preserves historical sequencing.",
    }


def _project_data() -> dict[str, object]:
    return {
        "schema_version": 1,
        "project_id": "P16",
        "title": "Historical regression corpus project",
        "objective": "Preserve deterministic Ticket Factory regression evidence.",
        "summary": "Synthetic project for the in-memory P16.7 corpus.",
        "context": [
            "Current canonical governance defines the Ticket Factory authority."
        ],
        "authority_references": [_authority_reference()],
        "scope": _scope("hermes_cli/agent_platform/ticket_factory/**"),
        "constraints": ["No execution authority is granted."],
        "non_goals": [
            "No provider calls, WorkPackets or external publication are authorized."
        ],
        "acceptance_criteria": ["The corpus run is deterministic and in memory."],
        "completion_verdict": "historical_regression_corpus_ready",
    }


def _ticket_data(
    ticket_id: str,
    *,
    title: str,
    commit_message: str,
    dependencies: tuple[dict[str, object], ...] = (),
    forbidden_actions: tuple[str, ...] = _FORBIDDEN_ACTIONS,
    sections: tuple[str, ...] = _REQUIRED_RESPONSE_SECTIONS,
    constraints: tuple[str, ...] = (
        "Rollback by removing only the synthetic corpus change.",
    ),
) -> dict[str, object]:
    suffix = ticket_id.lower().replace(".", "_")
    return {
        "schema_version": 1,
        "project_id": "P16",
        "ticket_id": ticket_id,
        "title": title,
        "ticket_type": "implementation",
        "objective": "Validate frozen historical regression behavior.",
        "context": [
            "Synthetic compact context derived from accepted Ticket Factory contracts."
        ],
        "authority_references": [_authority_reference()],
        "dependencies": list(dependencies),
        "parallelization_hint": "unspecified",
        "scope": _scope(
            f"hermes_cli/agent_platform/ticket_factory/{suffix}.py",
            forbidden_actions,
        ),
        "constraints": list(constraints),
        "tasks": ["Create deterministic in-memory regression evidence."],
        "acceptance_criteria": ["Regression evidence remains frozen and sanitized."],
        "validation_steps": [_validation_step()],
        "response_contract": _response_contract(f"historical_{suffix}_ready", sections),
        "recommended_commit_message": commit_message,
    }


def _ticket_spec(**kwargs: object) -> TicketSpec:
    return TicketSpec.model_validate(_ticket_data(**kwargs))


def _project_spec() -> ProjectSpec:
    return ProjectSpec.model_validate(_project_data())


def _context_source() -> ContextSourceSpec:
    return ContextSourceSpec.model_validate({
        "source_id": "CTX-HISTORICAL-REGRESSION",
        "kind": ContextSourceKind.GOVERNANCE_RECORD.value,
        "title": "Historical regression governance",
        "source_reference": "governance:historical-regression-corpus",
        "content": "Synthetic compact context for historical regression.",
        "authority_references": (),
        "sensitivity": ContextSensitivity.INTERNAL.value,
        "priority": ContextPriority.NORMAL.value,
        "required": False,
    })


def _generation_request(
    project: ProjectSpec, ticket: TicketSpec
) -> TicketGenerationRequest:
    context_pack = assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=project,
            ticket_spec=ticket,
            sources=(_context_source(),),
            policy=ContextAssemblyPolicy(),
        )
    )
    return TicketGenerationRequest(
        project_spec=project,
        ticket_spec=ticket,
        context_pack=context_pack,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
    )


def _reviewed_proposal(
    project: ProjectSpec,
    assignment: object,
    ticket: TicketSpec,
    rationale_suffix: str = "",
) -> ReviewedTicketProposal:
    proposal = build_ticket_proposal(
        assignment=assignment,
        proposed_ticket=ticket,
        rationale="Synthetic externally supplied proposal evidence." + rationale_suffix,
        evidence_source_ids=("CTX-HISTORICAL-REGRESSION",),
        assumptions=(),
        risks=(),
        unresolved_questions=(),
    )
    lint_report = lint_ticket_collection(
        TicketLintRequest(
            project_spec=project,
            tickets=(ticket,),
            dependency_plan=None,
            collection_complete=False,
        )
    )
    return ReviewedTicketProposal(proposal=proposal, lint_report=lint_report)


def _synthesis_fixture(
    split: bool,
) -> tuple[TicketSynthesisReview, TicketSynthesisRequest, ProjectSpec, TicketSpec]:
    project = _project_spec()
    seed = _ticket_spec(
        ticket_id="P16.5",
        title="Historical synthesis seed",
        commit_message="P16.5 Add synthesis review evidence",
    )
    generation = _generation_request(project, seed)
    assignments = prepare_ticket_generator_assignments(generation)
    alternative = (
        _ticket_spec(
            ticket_id="P16.5",
            title="Historical synthesis alternative",
            commit_message="P16.5 Add synthesis review evidence",
        )
        if split
        else seed
    )
    request = TicketSynthesisRequest(
        generation_request=generation,
        assignments=assignments,
        reviewed_proposals=(
            _reviewed_proposal(project, assignments[0], seed),
            _reviewed_proposal(
                project,
                assignments[1],
                alternative,
                " Alternative title evidence.",
            ),
        ),
        dependency_plan=None,
    )
    return build_ticket_synthesis_review(request), request, project, seed


def _approval_fixture() -> tuple[TicketApprovalRecord, TicketApprovalRequest]:
    review, _request, project, seed = _synthesis_fixture(split=False)
    request = TicketApprovalRequest(
        project_spec=project,
        seed_ticket=seed,
        synthesis_review=review,
        decision=HumanApprovalDecision.APPROVE,
        conflict_resolutions=(),
        approval_evidence=HumanApprovalEvidence(
            reviewer_id="synthetic-reviewer-p16-7",
            decision_reference="synthetic-human-review:P16.7",
            rationale="Synthetic human approval evidence for deterministic regression.",
        ),
        manual_replacement=None,
        fresh_planning_evidence=None,
    )
    return build_ticket_approval_record(request), request


def _fixture_input_json(case_id: str) -> str:
    if case_id == "HIST-001":
        return _deterministic_json(
            _ticket_data(
                ticket_id="P16.0",
                title="Valid historical TicketSpec acceptance",
                commit_message="P16.0 Add project and ticket spec schema",
            )
        )
    if case_id == "HIST-002":
        data = _ticket_data(
            ticket_id="P16.0",
            title="Invalid schema version rejection",
            commit_message="P16.0 Add project and ticket spec schema",
        )
        data["schema_version"] = 2
        return _deterministic_json(data)
    if case_id == "HIST-003":
        tickets = (
            _ticket_spec(
                ticket_id="P16.1",
                title="Historical dependency base",
                commit_message="P16.1 Add context pack assembler",
            ),
            _ticket_spec(
                ticket_id="P16.2",
                title="Historical dependent",
                commit_message="P16.2 Add generator roles",
                dependencies=(_dependency("P16.1"),),
            ),
        )
        request = TicketPlanningRequest(
            project_spec=_project_spec(),
            tickets=tickets,
            external_dependency_resolutions=(),
        )
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-004":
        tickets = (
            _ticket_spec(
                ticket_id="P16.3",
                title="Historical regression ticket P16.3",
                commit_message="P16.3 Add planner",
                dependencies=(_dependency("P16.4"),),
            ),
            _ticket_spec(
                ticket_id="P16.4",
                title="Historical regression ticket P16.4",
                commit_message="P16.4 Add linter",
                dependencies=(_dependency("P16.3"),),
            ),
        )
        request = TicketPlanningRequest(
            project_spec=_project_spec(),
            tickets=tickets,
            external_dependency_resolutions=(),
        )
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-005":
        request = TicketLintRequest(
            project_spec=_project_spec(),
            tickets=(
                _ticket_spec(
                    ticket_id="P16.4",
                    title="Policy pass historical ticket",
                    commit_message="P16.4 Add linter",
                ),
            ),
            dependency_plan=None,
            collection_complete=False,
        )
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-006":
        blocked = _ticket_spec(
            ticket_id="P16.4",
            title="Policy blocked historical ticket",
            commit_message="P16.4 Add linter",
            forbidden_actions=("execute tickets",),
            sections=("Summary",),
            constraints=("No rollback marker here.",),
        )
        request = TicketLintRequest(
            project_spec=_project_spec(),
            tickets=(blocked,),
            dependency_plan=None,
            collection_complete=False,
        )
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-007":
        _review, request, _project, _seed = _synthesis_fixture(split=False)
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-008":
        _review, request, _project, _seed = _synthesis_fixture(split=True)
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-009":
        _record, request = _approval_fixture()
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-010":
        review, _request, project, seed = _synthesis_fixture(split=True)
        request = TicketApprovalRequest(
            project_spec=project,
            seed_ticket=seed,
            synthesis_review=review,
            decision=HumanApprovalDecision.APPROVE,
            conflict_resolutions=(),
            approval_evidence=HumanApprovalEvidence(
                reviewer_id="synthetic-reviewer-p16-7",
                decision_reference="synthetic-human-review:P16.7-conflict",
                rationale="Synthetic approval attempts conflict handling.",
            ),
            manual_replacement=None,
            fresh_planning_evidence=None,
        )
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-011":
        record, _approval_request = _approval_fixture()
        request = TicketPublicationRequest(
            approval_record=record,
            publication_evidence=TicketPublicationEvidence(
                publisher_id="synthetic-publisher-p16-7",
                publication_reference="synthetic-publication:P16.7:rev1",
                rationale="Synthetic logical first publication.",
            ),
            prior_publication=None,
            supersession_rationale=None,
        )
        return _deterministic_json(request.model_dump(mode="json"))
    if case_id == "HIST-012":
        record, _approval_request = _approval_fixture()
        first_request = TicketPublicationRequest(
            approval_record=record,
            publication_evidence=TicketPublicationEvidence(
                publisher_id="synthetic-publisher-p16-7",
                publication_reference="synthetic-publication:P16.7:rev1",
                rationale="Synthetic logical first publication.",
            ),
            prior_publication=None,
            supersession_rationale=None,
        )
        first = publish_canonical_ticket(first_request)
        request = TicketPublicationRequest(
            approval_record=record,
            publication_evidence=TicketPublicationEvidence(
                publisher_id="synthetic-publisher-p16-7",
                publication_reference="synthetic-publication:P16.7:rev2",
                rationale="Synthetic logical supersession publication.",
            ),
            prior_publication=first.publication,
            supersession_rationale="Synthetic supersession boundary evidence.",
        )
        return _deterministic_json(request.model_dump(mode="json"))
    raise HistoricalRegressionCorpusError(f"unknown historical case fixture: {case_id}")


_CASE_SOURCE = (
    {
        "case_id": "HIST-001",
        "name": "Valid TicketSpec acceptance",
        "case_class": "accepted",
        "description": "Validates a compact TicketSpec that preserves the accepted schema pattern.",
        "provenance_kind": "current_canonical_governance",
        "source_ticket_id": "P16.0",
        "stage": "ticket_spec_validation",
        "tags": ("accepted", "ticket-spec", "p16-0"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketSpec",
            output_SHA256="5a3f422b61d4befdcd7e49b3dd33b54eb8994c79d5462ed8741e04cf6caf94f5",
        ),
        "case_SHA256": "f2d1cdf09a49170dbc3ba724d8d54885b5b790fd8e604c87b55ce7ad1ac59419",
    },
    {
        "case_id": "HIST-002",
        "name": "Invalid TicketSpec rejection",
        "case_class": "rejected",
        "description": "Rejects an alternate TicketSpec schema version from a historical cleanup pattern.",
        "provenance_kind": "read_only_git_history",
        "source_ticket_id": "P16.0",
        "stage": "ticket_spec_validation",
        "tags": ("rejected", "ticket-spec", "schema-version"),
        "expectation": _expectation(
            outcome="error",
            exception_type="ValidationError",
            exception_message_fragment=(
                "1 validation error for TicketSpec schema_version Input should be 1 "
                "[type=literal_error, input_value=2, input_type=int] For further information visit https://err"
            ),
        ),
        "case_SHA256": "1d5d3df7058728a1e82da37f65f88a393f0923402c8421b1ace1d33e6c32c38f",
    },
    {
        "case_id": "HIST-003",
        "name": "Deterministic dependency plan",
        "case_class": "accepted",
        "description": "Builds a deterministic two-ticket dependency plan with one hard edge.",
        "provenance_kind": "current_canonical_governance",
        "source_ticket_id": "P16.3",
        "stage": "dependency_planning",
        "tags": ("accepted", "dependency-plan", "deterministic"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketDependencyPlan",
            output_SHA256="3255fb67dd77582174650dab5fdb5d806ff83c5ffda676842a10eb6f79963721",
        ),
        "case_SHA256": "6313f4517f92dab5f9cbe06f4d4834e1ba04a594d06c97f677e07107013b7554",
    },
    {
        "case_id": "HIST-004",
        "name": "Hard dependency cycle rejection",
        "case_class": "rejected",
        "description": "Captures hard prerequisite cycle rejection without restoring old tickets.",
        "provenance_kind": "read_only_git_history",
        "source_ticket_id": "P16.3",
        "stage": "dependency_planning",
        "tags": ("rejected", "dependency-cycle", "hard-prerequisite"),
        "expectation": _expectation(
            outcome="error",
            exception_type="DependencyCycleError",
            exception_message_fragment="hard dependency cycle detected: ticket_ids=P16.3 > P16.4",
        ),
        "case_SHA256": "d90ad478c269642558bf933621d3ded73797da5ae47e0f201b363e9242557a24",
    },
    {
        "case_id": "HIST-005",
        "name": "Policy pass report",
        "case_class": "accepted",
        "description": "Records a clean deterministic ticket-policy lint result.",
        "provenance_kind": "current_canonical_governance",
        "source_ticket_id": "P16.4",
        "stage": "ticket_policy_lint",
        "tags": ("accepted", "policy-lint", "pass-report"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketLintReport",
            output_SHA256="a0adfb6696634cdbcd474491776f7d3202d1caa27b1205e21ed4ec950e4f66ea",
        ),
        "case_SHA256": "55baecec205728755ec36f5e869b954d0914f1a006ef3f054a0da6efa88c3fe5",
    },
    {
        "case_id": "HIST-006",
        "name": "Policy blocked report",
        "case_class": "rejected",
        "description": "Records a blocked lint report for missing governed ticket posture.",
        "provenance_kind": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.4",
        "stage": "ticket_policy_lint",
        "tags": ("rejected", "policy-lint", "blocked-report"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketLintReport",
            output_SHA256="9f590329a1b96e639ed92c403a0c844ad7564fc596a805ce69c8746f0062cbc2",
        ),
        "case_SHA256": "82f938efce2d7262ad655b2bd08c6338904fdc3695b2d15c40edb4d30b4e4740",
    },
    {
        "case_id": "HIST-007",
        "name": "Unanimous synthesis review",
        "case_class": "accepted",
        "description": "Synthesizes a noncanonical review from unanimous proposal evidence.",
        "provenance_kind": "current_canonical_governance",
        "source_ticket_id": "P16.5",
        "stage": "proposal_synthesis",
        "tags": ("accepted", "synthesis", "unanimous"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketSynthesisReview",
            output_SHA256="e4e827948d8877acca346ebf9ada08eeb710470c810733c94932ce70083be378",
        ),
        "case_SHA256": "0378cdaf18b2ccb89af59aa4b135deb56d82b86ed1ec8f851ac7b70c51dbf220",
    },
    {
        "case_id": "HIST-008",
        "name": "Split synthesis review",
        "case_class": "boundary",
        "description": "Synthesizes a split-field review requiring human resolution.",
        "provenance_kind": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.5",
        "stage": "proposal_synthesis",
        "tags": ("boundary", "synthesis", "split-field"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketSynthesisReview",
            output_SHA256="f0a4849862f10692abb0a031c8bd74d5309a25240f5b99f117be037429ed3fe0",
        ),
        "case_SHA256": "9e93f2aaa0cb63391625e7b68460531b9b8568bc14b8e5254837bb2bf8ec631b",
    },
    {
        "case_id": "HIST-009",
        "name": "Explicit approval success",
        "case_class": "accepted",
        "description": "Builds explicit human-gated approval evidence for a clean review.",
        "provenance_kind": "current_canonical_governance",
        "source_ticket_id": "P16.6",
        "stage": "human_approval",
        "tags": ("accepted", "human-approval", "approve"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketApprovalRecord",
            output_SHA256="de58a99212656d87e15b4471a95b3b8213b03f70a8912d390a606f39684d7346",
        ),
        "case_SHA256": "fd1177310d20441de95f2366f007b7c922863b3cd9a6d48cd7f744228345dcd5",
    },
    {
        "case_id": "HIST-010",
        "name": "Approval validation rejection",
        "case_class": "rejected",
        "description": "Captures approval rejection when conflicts lack explicit resolution.",
        "provenance_kind": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.6",
        "stage": "human_approval",
        "tags": ("rejected", "human-approval", "conflict-resolution"),
        "expectation": _expectation(
            outcome="error",
            exception_type="TicketApprovalInputError",
            exception_message_fragment="approval requires exactly one resolution per conflict",
        ),
        "case_SHA256": "db4f15bb8d606dc50200f2579d1b71e65a5668c03b393ceac437ef5ee3906af6",
    },
    {
        "case_id": "HIST-011",
        "name": "First canonical publication",
        "case_class": "accepted",
        "description": "Publishes the first logical canonical artifact in memory.",
        "provenance_kind": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.6",
        "stage": "canonical_publication",
        "tags": ("accepted", "canonical-publication", "first-revision"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketPublicationResult",
            output_SHA256="1d6d1497380652858155dbb7b9ac52abf84f725b3bb410d3b791fe21e775124f",
        ),
        "case_SHA256": "a239c1d9458f8eeca6d89464f0fe1ffb9cd0cad5266cc27b3364ac7e0b6f4371",
    },
    {
        "case_id": "HIST-012",
        "name": "Publication supersession boundary",
        "case_class": "boundary",
        "description": "Publishes a superseding logical canonical artifact in memory.",
        "provenance_kind": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.6",
        "stage": "canonical_publication",
        "tags": ("boundary", "canonical-publication", "supersession"),
        "expectation": _expectation(
            outcome="success",
            output_type="TicketPublicationResult",
            output_SHA256="4da6c4af7eec5bac43d77103304abcaaf91d6d3d2138f7cb099d8b73fa87bf52",
        ),
        "case_SHA256": "4ccfaaba58ca0e356accbed97180937115a7727854bf2cbec615d9c1f46e4983",
    },
)

_CORPUS_SHA256 = "6b949789efafa2fac5d74eb16915aeb8c4c2a2d7123778c777e800f37beda099"


def _source_reference(kind: str) -> str:
    if kind == HistoricalProvenanceKind.CURRENT_CANONICAL_GOVERNANCE.value:
        return "current canonical governance: Ticket Factory accepted contract"
    if kind == HistoricalProvenanceKind.READ_ONLY_GIT_HISTORY.value:
        return "bounded read-only P16 branch history: P16.6 direct parent"
    return "sanitized synthetic ticket archetype: compact behavior fixture"


def _provenance(
    case_id: str, kind: str, source_ticket_id: str
) -> HistoricalTicketProvenance:
    return HistoricalTicketProvenance(
        provenance_id=f"PROV-{case_id}",
        kind=HistoricalProvenanceKind(kind),
        source_ticket_id=source_ticket_id,
        source_reference=_source_reference(kind),
        source_commit_SHA=(
            _P16_6_COMMIT_SHA
            if kind == HistoricalProvenanceKind.READ_ONLY_GIT_HISTORY.value
            else None
        ),
        sanitized=True,
        rationale=(
            "Preserves behavior pattern only; no raw historical document content is embedded."
        ),
    )


def _build_canonical_cases() -> tuple[HistoricalRegressionCase, ...]:
    return tuple(
        HistoricalRegressionCase(
            case_id=str(item["case_id"]),
            name=str(item["name"]),
            case_class=HistoricalRegressionCaseClass(str(item["case_class"])),
            description=str(item["description"]),
            provenance=_provenance(
                str(item["case_id"]),
                str(item["provenance_kind"]),
                str(item["source_ticket_id"]),
            ),
            stage=HistoricalRegressionStage(str(item["stage"])),
            input_JSON=_fixture_input_json(str(item["case_id"])),
            expectation=item["expectation"],
            tags=item["tags"],
            case_SHA256=str(item["case_SHA256"]),
        )
        for item in _CASE_SOURCE
    )


def get_historical_ticket_regression_corpus() -> HistoricalRegressionCorpus:
    """Return the single frozen in-memory historical regression corpus."""

    return HistoricalRegressionCorpus(
        cases=_build_canonical_cases(),
        corpus_SHA256=_CORPUS_SHA256,
    )


def validate_historical_ticket_regression_corpus(
    corpus: HistoricalRegressionCorpus,
) -> None:
    """Validate corpus identity, composition and frozen digest integrity."""

    try:
        HistoricalRegressionCorpus.model_validate(corpus.model_dump(mode="json"))
    except ValueError as exc:
        raise HistoricalRegressionCorpusError(str(exc)) from exc


def _dispatch_case(case: HistoricalRegressionCase) -> BaseModel:
    if case.stage is HistoricalRegressionStage.TICKET_SPEC_VALIDATION:
        return TicketSpec.model_validate_json(case.input_JSON)
    if case.stage is HistoricalRegressionStage.DEPENDENCY_PLANNING:
        planning_request = TicketPlanningRequest.model_validate_json(case.input_JSON)
        return build_ticket_dependency_plan(planning_request)
    if case.stage is HistoricalRegressionStage.TICKET_POLICY_LINT:
        lint_request = TicketLintRequest.model_validate_json(case.input_JSON)
        return lint_ticket_collection(lint_request)
    if case.stage is HistoricalRegressionStage.PROPOSAL_SYNTHESIS:
        synthesis_request = TicketSynthesisRequest.model_validate_json(case.input_JSON)
        return build_ticket_synthesis_review(synthesis_request)
    if case.stage is HistoricalRegressionStage.HUMAN_APPROVAL:
        approval_request = TicketApprovalRequest.model_validate_json(case.input_JSON)
        return build_ticket_approval_record(approval_request)
    if case.stage is HistoricalRegressionStage.CANONICAL_PUBLICATION:
        publication_request = TicketPublicationRequest.model_validate_json(
            case.input_JSON
        )
        return publish_canonical_ticket(publication_request)
    raise HistoricalRegressionExecutionError(
        f"unsupported historical stage: {case.stage.value}"
    )


def _bounded_exception_message(exc: Exception) -> str:
    return _WHITESPACE.sub(" ", str(exc).strip())[:512]


def _success_observation(
    stage: HistoricalRegressionStage, output: BaseModel
) -> HistoricalRegressionObservation:
    observation = HistoricalRegressionObservation.model_construct(
        stage=stage,
        outcome=HistoricalRegressionExpectedOutcome.SUCCESS,
        output_type=output.__class__.__name__,
        output_SHA256=_output_digest(output),
        exception_type=None,
        exception_message=None,
        observation_SHA256="0" * 64,
    )
    return HistoricalRegressionObservation(
        **observation.model_dump(mode="json", exclude={"observation_SHA256"}),
        observation_SHA256=_observation_digest(observation),
    )


def _error_observation(
    stage: HistoricalRegressionStage, exc: Exception
) -> HistoricalRegressionObservation:
    observation = HistoricalRegressionObservation.model_construct(
        stage=stage,
        outcome=HistoricalRegressionExpectedOutcome.ERROR,
        output_type=None,
        output_SHA256=None,
        exception_type=exc.__class__.__name__,
        exception_message=_bounded_exception_message(exc),
        observation_SHA256="0" * 64,
    )
    return HistoricalRegressionObservation(
        **observation.model_dump(mode="json", exclude={"observation_SHA256"}),
        observation_SHA256=_observation_digest(observation),
    )


_DRIFT_KIND_RANK = {
    kind: index for index, kind in enumerate(HistoricalRegressionDriftKind)
}


def _drift_sort_key(
    item: tuple[HistoricalRegressionDriftKind, str | None, str | None, str],
) -> tuple[object, ...]:
    kind, expected, observed, message = item
    return (
        _DRIFT_KIND_RANK[kind],
        "" if expected is None else expected,
        "" if observed is None else observed,
        message,
    )


def _make_drifts(
    case: HistoricalRegressionCase, observation: HistoricalRegressionObservation
) -> tuple[HistoricalRegressionDrift, ...]:
    expected = case.expectation
    drift_inputs: list[
        tuple[HistoricalRegressionDriftKind, str | None, str | None, str]
    ] = []
    if expected.outcome is HistoricalRegressionExpectedOutcome.SUCCESS:
        if observation.outcome is HistoricalRegressionExpectedOutcome.ERROR:
            drift_inputs.append((
                HistoricalRegressionDriftKind.UNEXPECTED_ERROR,
                expected.output_type,
                observation.exception_type,
                "Expected successful output but observed bounded exception evidence.",
            ))
        else:
            if expected.output_type != observation.output_type:
                drift_inputs.append((
                    HistoricalRegressionDriftKind.OUTPUT_TYPE_MISMATCH,
                    expected.output_type,
                    observation.output_type,
                    "Observed output type differs from frozen expectation.",
                ))
            if expected.output_SHA256 != observation.output_SHA256:
                drift_inputs.append((
                    HistoricalRegressionDriftKind.OUTPUT_DIGEST_MISMATCH,
                    expected.output_SHA256,
                    observation.output_SHA256,
                    "Observed output digest differs from frozen expectation.",
                ))
    elif observation.outcome is HistoricalRegressionExpectedOutcome.SUCCESS:
        drift_inputs.append((
            HistoricalRegressionDriftKind.UNEXPECTED_SUCCESS,
            expected.exception_type,
            observation.output_type,
            "Expected bounded exception evidence but observed successful output.",
        ))
    else:
        if expected.exception_type != observation.exception_type:
            drift_inputs.append((
                HistoricalRegressionDriftKind.EXCEPTION_TYPE_MISMATCH,
                expected.exception_type,
                observation.exception_type,
                "Observed exception type differs from frozen expectation.",
            ))
        fragment = expected.exception_message_fragment or ""
        message = observation.exception_message or ""
        if fragment not in message:
            drift_inputs.append((
                HistoricalRegressionDriftKind.EXCEPTION_MESSAGE_MISMATCH,
                fragment,
                message,
                "Observed bounded exception message lacks frozen expected fragment.",
            ))
    return tuple(
        HistoricalRegressionDrift(
            drift_id=f"DRIFT-{index:04d}",
            case_id=case.case_id,
            kind=kind,
            expected_value=expected_value,
            observed_value=observed_value,
            message=message,
            blocking=True,
        )
        for index, (kind, expected_value, observed_value, message) in enumerate(
            sorted(drift_inputs, key=_drift_sort_key), start=1
        )
    )


def run_historical_ticket_regression_case(
    case: HistoricalRegressionCase,
) -> HistoricalRegressionCaseResult:
    """Run one frozen historical regression case and return drift evidence."""

    try:
        validated_case = HistoricalRegressionCase.model_validate(
            case.model_dump(mode="json")
        )
        _validate_canonical_fixture_json(validated_case.input_JSON)
    except ValueError as exc:
        raise HistoricalRegressionCorpusError(str(exc)) from exc
    try:
        output = _dispatch_case(validated_case)
    except (ValueError, ValidationError) as exc:
        observation = _error_observation(validated_case.stage, exc)
    else:
        observation = _success_observation(validated_case.stage, output)
    drifts = _make_drifts(validated_case, observation)
    result = HistoricalRegressionCaseResult.model_construct(
        case_id=validated_case.case_id,
        matched=not drifts,
        observation=observation,
        drifts=drifts,
        result_SHA256="0" * 64,
    )
    return HistoricalRegressionCaseResult(
        **result.model_dump(mode="json", exclude={"result_SHA256"}),
        result_SHA256=_case_result_digest(result),
    )


def run_historical_ticket_regression_corpus(
    corpus: HistoricalRegressionCorpus | None = None,
) -> HistoricalRegressionRun:
    """Run every case in deterministic corpus order without stopping on drift."""

    resolved = (
        corpus if corpus is not None else get_historical_ticket_regression_corpus()
    )
    validate_historical_ticket_regression_corpus(resolved)
    results = tuple(
        run_historical_ticket_regression_case(case) for case in resolved.cases
    )
    passed = tuple(result.case_id for result in results if result.matched)
    drifted = tuple(result.case_id for result in results if not result.matched)
    run = HistoricalRegressionRun.model_construct(
        schema_version=HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION,
        corpus_id=resolved.corpus_id,
        corpus_SHA256=resolved.corpus_SHA256,
        case_results=results,
        passed_case_ids=passed,
        drifted_case_ids=drifted,
        disposition=(
            HistoricalRegressionRunDisposition.PASS
            if not drifted
            else HistoricalRegressionRunDisposition.DRIFT_DETECTED
        ),
        run_SHA256="0" * 64,
    )
    return HistoricalRegressionRun(
        **run.model_dump(mode="json", exclude={"run_SHA256"}),
        run_SHA256=_run_digest(run),
    )
