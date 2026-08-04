"""Deterministic shadow pilot over accepted Ticket Factory contracts.

The pilot composes prior P16 contracts in memory only. It never grants
provider, model, runtime, filesystem, Git, Graphify, Docker or WorkPacket
authority.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory.approval_publishing import (
    ConflictResolutionAction,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    HumanConflictResolution,
    TicketApprovalRecord,
    TicketApprovalRequest,
    TicketApprovalState,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    TicketPublicationResult,
    TicketPublicationState,
    build_ticket_approval_record,
    publish_canonical_ticket,
)
from hermes_cli.agent_platform.ticket_factory.context_packs import (
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPack,
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
    GeneratorAssignment,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketProposal,
    build_ticket_proposal,
    prepare_ticket_generator_assignments,
)
from hermes_cli.agent_platform.ticket_factory.historical_regression import (
    HistoricalRegressionRun,
    HistoricalRegressionRunDisposition,
    run_historical_ticket_regression_corpus,
)
from hermes_cli.agent_platform.ticket_factory.proposal_synthesis import (
    ProposalConflictKind,
    ReviewedTicketProposal,
    TicketSynthesisDisposition,
    TicketSynthesisField,
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
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    lint_ticket_collection,
)

TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION = 1
TICKET_FACTORY_SHADOW_PILOT_ID = "pepper-ticket-factory-shadow-pilot-v1"
TICKET_FACTORY_SHADOW_PILOT_REVISION = 1
SHADOW_PILOT_ALTERNATE_TITLE = "Ticket Factory shadow pilot dissent check"

REQUEST_DIGEST_ALGORITHM = "agent-platform-shadow-pilot-request-sha256-v1"
EVIDENCE_DIGEST_ALGORITHM = "agent-platform-shadow-pilot-evidence-sha256-v1"
STAGE_RESULT_DIGEST_ALGORITHM = "agent-platform-shadow-pilot-stage-sha256-v1"
GATE_RESULT_DIGEST_ALGORITHM = "agent-platform-shadow-pilot-gate-sha256-v1"
REPORT_DIGEST_ALGORITHM = "agent-platform-shadow-pilot-report-sha256-v1"


class TicketFactoryShadowPilotError(ValueError):
    """Base error for shadow pilot contract failures."""


class TicketFactoryShadowPilotInputError(TicketFactoryShadowPilotError):
    """Raised when a shadow pilot request is inconsistent."""


class TicketFactoryShadowPilotExecutionError(TicketFactoryShadowPilotError):
    """Raised when deterministic in-memory composition cannot complete."""


class TicketFactoryShadowPilotIntegrityError(TicketFactoryShadowPilotError):
    """Raised when shadow pilot evidence does not validate."""


class ShadowPilotStage(str, Enum):
    HISTORICAL_PREFLIGHT = "historical_preflight"
    CONTEXT_ASSEMBLY = "context_assembly"
    DEPENDENCY_PLANNING = "dependency_planning"
    GENERATOR_ASSIGNMENT = "generator_assignment"
    PROPOSAL_REVIEW = "proposal_review"
    SYNTHESIS_REVIEW = "synthesis_review"
    HUMAN_APPROVAL = "human_approval"
    CANONICAL_PUBLICATION = "canonical_publication"


class ShadowPilotGate(str, Enum):
    HISTORICAL_REGRESSION_CLEAN = "historical_regression_clean"
    POLICY_LINT_PASS = "policy_lint_pass"
    SYNTHESIS_REVIEW_READY = "synthesis_review_ready"
    HUMAN_APPROVAL_PRESENT = "human_approval_present"


class ShadowPilotGateStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class ShadowPilotDisposition(str, Enum):
    GO_WITH_CONSTRAINTS = "go_with_constraints"
    BLOCKED = "blocked"


class ShadowPilotArtifactKind(str, Enum):
    HISTORICAL_REGRESSION_RUN = "historical_regression_run"
    CONTEXT_PACK = "context_pack"
    DEPENDENCY_PLAN = "dependency_plan"
    GENERATOR_ASSIGNMENTS = "generator_assignments"
    TICKET_PROPOSALS = "ticket_proposals"
    SYNTHESIS_REVIEW = "synthesis_review"
    APPROVAL_RECORD = "approval_record"
    PUBLICATION_RESULT = "publication_result"


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


BoundedText: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
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
EvidenceIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=12,
        max_length=80,
        pattern=r"^EVID-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-[0-9]{3}$",
    ),
]
DigestText: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]


class _ShadowPilotModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _reject_duplicate_values(values: tuple[object, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


class ShadowPilotEvidence(_ShadowPilotModel):
    schema_version: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION
    evidence_id: EvidenceIdentifier
    stage: ShadowPilotStage
    artifact_kind: ShadowPilotArtifactKind
    artifact_type: BoundedText
    artifact_SHA256: DigestText
    rationale: BoundedText
    evidence_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_evidence(self) -> ShadowPilotEvidence:
        expected = _evidence_digest(
            schema_version=self.schema_version,
            evidence_id=self.evidence_id,
            stage=self.stage,
            artifact_kind=self.artifact_kind,
            artifact_type=self.artifact_type,
            artifact_SHA256=self.artifact_SHA256,
            rationale=self.rationale,
        )
        if self.evidence_SHA256 != expected:
            raise ValueError("evidence_SHA256 must match shadow pilot evidence digest")
        return self


class ShadowPilotStageResult(_ShadowPilotModel):
    schema_version: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION
    stage: ShadowPilotStage
    status: ShadowPilotGateStatus
    evidence: ShadowPilotEvidence
    message: BoundedText
    stage_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_stage_result(self) -> ShadowPilotStageResult:
        if self.evidence.stage is not self.stage:
            raise ValueError("stage result evidence must match stage")
        expected = _stage_result_digest(
            schema_version=self.schema_version,
            stage=self.stage,
            status=self.status,
            evidence=self.evidence,
            message=self.message,
        )
        if self.stage_SHA256 != expected:
            raise ValueError("stage_SHA256 must match shadow pilot stage digest")
        return self


class ShadowPilotGateResult(_ShadowPilotModel):
    schema_version: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION
    gate: ShadowPilotGate
    stage: ShadowPilotStage
    status: ShadowPilotGateStatus
    message: BoundedText
    gate_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_gate_result(self) -> ShadowPilotGateResult:
        expected = _gate_result_digest(
            schema_version=self.schema_version,
            gate=self.gate,
            stage=self.stage,
            status=self.status,
            message=self.message,
        )
        if self.gate_SHA256 != expected:
            raise ValueError("gate_SHA256 must match shadow pilot gate digest")
        return self


class TicketFactoryShadowPilotRequest(_ShadowPilotModel):
    schema_version: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION
    pilot_id: Literal["pepper-ticket-factory-shadow-pilot-v1"] = (
        TICKET_FACTORY_SHADOW_PILOT_ID
    )
    revision: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_REVISION
    project_spec: ProjectSpec
    seed_ticket: TicketSpec
    context_sources: tuple[ContextSourceSpec, ...] = Field(min_length=1, max_length=8)
    requested_roles: tuple[TicketGeneratorRole, ...] = Field(min_length=2, max_length=6)
    historical_preflight_required: Literal[True] = True
    shadow_only: Literal[True] = True
    allow_provider_calls: Literal[False] = False
    allow_model_calls: Literal[False] = False
    allow_runtime_execution: Literal[False] = False
    allow_filesystem_writes: Literal[False] = False
    allow_git_mutation: Literal[False] = False

    @model_validator(mode="after")
    def _validate_request(self) -> TicketFactoryShadowPilotRequest:
        if self.project_spec.project_id != self.seed_ticket.project_id:
            raise ValueError(
                "project_spec and seed_ticket project identifiers must match"
            )
        if not self.seed_ticket.ticket_id.startswith(
            f"{self.project_spec.project_id}."
        ):
            raise ValueError("seed_ticket must use the project_id prefix")
        source_ids = tuple(source.source_id for source in self.context_sources)
        _reject_duplicate_values(source_ids, "context_sources")
        role_values = tuple(role.value for role in self.requested_roles)
        _reject_duplicate_values(role_values, "requested_roles")
        return self


class TicketFactoryShadowPilotReport(_ShadowPilotModel):
    schema_version: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION
    pilot_id: Literal["pepper-ticket-factory-shadow-pilot-v1"] = (
        TICKET_FACTORY_SHADOW_PILOT_ID
    )
    revision: Literal[1] = TICKET_FACTORY_SHADOW_PILOT_REVISION
    ticket_id: TicketIdentifier
    request_SHA256: DigestText
    disposition: ShadowPilotDisposition
    stage_results: tuple[ShadowPilotStageResult, ...] = Field(
        min_length=8, max_length=8
    )
    gate_results: tuple[ShadowPilotGateResult, ...] = Field(min_length=4, max_length=4)
    historical_run: HistoricalRegressionRun
    context_pack: ContextPack
    dependency_plan: TicketDependencyPlan
    ticket_lint_report: TicketLintReport
    generation_request: TicketGenerationRequest
    assignments: tuple[GeneratorAssignment, ...] = Field(min_length=2, max_length=6)
    proposals: tuple[TicketProposal, ...] = Field(min_length=2, max_length=6)
    synthesis_review: TicketSynthesisReview
    approval_record: TicketApprovalRecord
    publication_result: TicketPublicationResult
    report_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_report(self) -> TicketFactoryShadowPilotReport:
        _validate_report_artifacts(self, error_type=ValueError)
        expected = _report_digest(self)
        if self.report_SHA256 != expected:
            raise ValueError("report_SHA256 must match shadow pilot report digest")
        return self


_STAGE_ORDER = tuple(ShadowPilotStage)
_GATE_ORDER = tuple(ShadowPilotGate)
_STAGE_ARTIFACT_KIND = {
    ShadowPilotStage.HISTORICAL_PREFLIGHT: ShadowPilotArtifactKind.HISTORICAL_REGRESSION_RUN,
    ShadowPilotStage.CONTEXT_ASSEMBLY: ShadowPilotArtifactKind.CONTEXT_PACK,
    ShadowPilotStage.DEPENDENCY_PLANNING: ShadowPilotArtifactKind.DEPENDENCY_PLAN,
    ShadowPilotStage.GENERATOR_ASSIGNMENT: ShadowPilotArtifactKind.GENERATOR_ASSIGNMENTS,
    ShadowPilotStage.PROPOSAL_REVIEW: ShadowPilotArtifactKind.TICKET_PROPOSALS,
    ShadowPilotStage.SYNTHESIS_REVIEW: ShadowPilotArtifactKind.SYNTHESIS_REVIEW,
    ShadowPilotStage.HUMAN_APPROVAL: ShadowPilotArtifactKind.APPROVAL_RECORD,
    ShadowPilotStage.CANONICAL_PUBLICATION: ShadowPilotArtifactKind.PUBLICATION_RESULT,
}
_GATE_STAGE = {
    ShadowPilotGate.HISTORICAL_REGRESSION_CLEAN: ShadowPilotStage.HISTORICAL_PREFLIGHT,
    ShadowPilotGate.POLICY_LINT_PASS: ShadowPilotStage.PROPOSAL_REVIEW,
    ShadowPilotGate.SYNTHESIS_REVIEW_READY: ShadowPilotStage.SYNTHESIS_REVIEW,
    ShadowPilotGate.HUMAN_APPROVAL_PRESENT: ShadowPilotStage.HUMAN_APPROVAL,
}


def get_ticket_factory_shadow_pilot_stage_order() -> tuple[ShadowPilotStage, ...]:
    """Return the canonical shadow pilot stage order."""

    return _STAGE_ORDER


def get_ticket_factory_shadow_pilot_gate_order() -> tuple[ShadowPilotGate, ...]:
    """Return the canonical shadow pilot gate order."""

    return _GATE_ORDER


def _evidence_digest(
    *,
    schema_version: int,
    evidence_id: str,
    stage: ShadowPilotStage,
    artifact_kind: ShadowPilotArtifactKind,
    artifact_type: str,
    artifact_SHA256: str,
    rationale: str,
) -> str:
    record = {
        "algorithm": EVIDENCE_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "evidence_id": evidence_id,
        "stage": stage.value,
        "artifact_kind": artifact_kind.value,
        "artifact_type": artifact_type,
        "artifact_SHA256": artifact_SHA256,
        "rationale": rationale,
    }
    return _sha256_text(_deterministic_json(record))


def _stage_result_digest(
    *,
    schema_version: int,
    stage: ShadowPilotStage,
    status: ShadowPilotGateStatus,
    evidence: ShadowPilotEvidence,
    message: str,
) -> str:
    record = {
        "algorithm": STAGE_RESULT_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "stage": stage.value,
        "status": status.value,
        "evidence": evidence.model_dump(mode="json"),
        "message": message,
    }
    return _sha256_text(_deterministic_json(record))


def _gate_result_digest(
    *,
    schema_version: int,
    gate: ShadowPilotGate,
    stage: ShadowPilotStage,
    status: ShadowPilotGateStatus,
    message: str,
) -> str:
    record = {
        "algorithm": GATE_RESULT_DIGEST_ALGORITHM,
        "schema_version": schema_version,
        "gate": gate.value,
        "stage": stage.value,
        "status": status.value,
        "message": message,
    }
    return _sha256_text(_deterministic_json(record))


def _request_digest(request: TicketFactoryShadowPilotRequest) -> str:
    record = {
        "algorithm": REQUEST_DIGEST_ALGORITHM,
        **request.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def _aggregate_model_digest(algorithm: str, values: tuple[BaseModel, ...]) -> str:
    record = {
        "algorithm": algorithm,
        "values": [value.model_dump(mode="json") for value in values],
    }
    return _sha256_text(_deterministic_json(record))


def _artifact_digest_for_stage(
    stage: ShadowPilotStage,
    *,
    historical_run: HistoricalRegressionRun,
    context_pack: ContextPack,
    dependency_plan: TicketDependencyPlan,
    assignments: tuple[GeneratorAssignment, ...],
    proposals: tuple[TicketProposal, ...],
    synthesis_review: TicketSynthesisReview,
    approval_record: TicketApprovalRecord,
    publication_result: TicketPublicationResult,
) -> tuple[str, str]:
    if stage is ShadowPilotStage.HISTORICAL_PREFLIGHT:
        return (historical_run.__class__.__name__, historical_run.run_SHA256)
    if stage is ShadowPilotStage.CONTEXT_ASSEMBLY:
        return (context_pack.__class__.__name__, context_pack.context_pack_SHA256)
    if stage is ShadowPilotStage.DEPENDENCY_PLANNING:
        return (dependency_plan.__class__.__name__, dependency_plan.plan_SHA256)
    if stage is ShadowPilotStage.GENERATOR_ASSIGNMENT:
        return (
            "GeneratorAssignmentTuple",
            _aggregate_model_digest(
                "agent-platform-shadow-pilot-assignments-sha256-v1", assignments
            ),
        )
    if stage is ShadowPilotStage.PROPOSAL_REVIEW:
        return (
            "TicketProposalTuple",
            _aggregate_model_digest(
                "agent-platform-shadow-pilot-proposals-sha256-v1", proposals
            ),
        )
    if stage is ShadowPilotStage.SYNTHESIS_REVIEW:
        return (synthesis_review.__class__.__name__, synthesis_review.review_SHA256)
    if stage is ShadowPilotStage.HUMAN_APPROVAL:
        return (approval_record.__class__.__name__, approval_record.approval_SHA256)
    return (publication_result.__class__.__name__, publication_result.result_SHA256)


def _make_evidence(
    *,
    ticket_id: str,
    index: int,
    stage: ShadowPilotStage,
    artifact_type: str,
    artifact_SHA256: str,
) -> ShadowPilotEvidence:
    artifact_kind = _STAGE_ARTIFACT_KIND[stage]
    evidence_id = f"EVID-{ticket_id.replace('.', '-')}-{index:03d}"
    rationale = "Shadow-only in-memory evidence; no external execution or publication authority."
    evidence_SHA256 = _evidence_digest(
        schema_version=TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION,
        evidence_id=evidence_id,
        stage=stage,
        artifact_kind=artifact_kind,
        artifact_type=artifact_type,
        artifact_SHA256=artifact_SHA256,
        rationale=rationale,
    )
    return ShadowPilotEvidence(
        evidence_id=evidence_id,
        stage=stage,
        artifact_kind=artifact_kind,
        artifact_type=artifact_type,
        artifact_SHA256=artifact_SHA256,
        rationale=rationale,
        evidence_SHA256=evidence_SHA256,
    )


def _make_stage_result(
    *,
    stage: ShadowPilotStage,
    evidence: ShadowPilotEvidence,
    message: str,
) -> ShadowPilotStageResult:
    stage_SHA256 = _stage_result_digest(
        schema_version=TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION,
        stage=stage,
        status=ShadowPilotGateStatus.PASS,
        evidence=evidence,
        message=message,
    )
    return ShadowPilotStageResult(
        stage=stage,
        status=ShadowPilotGateStatus.PASS,
        evidence=evidence,
        message=message,
        stage_SHA256=stage_SHA256,
    )


def _make_stage_results(
    *,
    ticket_id: str,
    historical_run: HistoricalRegressionRun,
    context_pack: ContextPack,
    dependency_plan: TicketDependencyPlan,
    assignments: tuple[GeneratorAssignment, ...],
    proposals: tuple[TicketProposal, ...],
    synthesis_review: TicketSynthesisReview,
    approval_record: TicketApprovalRecord,
    publication_result: TicketPublicationResult,
) -> tuple[ShadowPilotStageResult, ...]:
    results: list[ShadowPilotStageResult] = []
    for index, stage in enumerate(_STAGE_ORDER, start=1):
        artifact_type, artifact_SHA256 = _artifact_digest_for_stage(
            stage,
            historical_run=historical_run,
            context_pack=context_pack,
            dependency_plan=dependency_plan,
            assignments=assignments,
            proposals=proposals,
            synthesis_review=synthesis_review,
            approval_record=approval_record,
            publication_result=publication_result,
        )
        evidence = _make_evidence(
            ticket_id=ticket_id,
            index=index,
            stage=stage,
            artifact_type=artifact_type,
            artifact_SHA256=artifact_SHA256,
        )
        results.append(
            _make_stage_result(
                stage=stage,
                evidence=evidence,
                message=f"Shadow stage completed in memory: stage={stage.value}",
            )
        )
    return tuple(results)


def _make_gate_result(gate: ShadowPilotGate, message: str) -> ShadowPilotGateResult:
    stage = _GATE_STAGE[gate]
    gate_SHA256 = _gate_result_digest(
        schema_version=TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION,
        gate=gate,
        stage=stage,
        status=ShadowPilotGateStatus.PASS,
        message=message,
    )
    return ShadowPilotGateResult(
        gate=gate,
        stage=stage,
        status=ShadowPilotGateStatus.PASS,
        message=message,
        gate_SHA256=gate_SHA256,
    )


def _make_gate_results() -> tuple[ShadowPilotGateResult, ...]:
    return (
        _make_gate_result(
            ShadowPilotGate.HISTORICAL_REGRESSION_CLEAN,
            "Historical regression run passed with zero drift.",
        ),
        _make_gate_result(
            ShadowPilotGate.POLICY_LINT_PASS,
            "Shadow ticket and proposal lint evidence is nonblocking.",
        ),
        _make_gate_result(
            ShadowPilotGate.SYNTHESIS_REVIEW_READY,
            "Synthesis review produced a review-ready candidate.",
        ),
        _make_gate_result(
            ShadowPilotGate.HUMAN_APPROVAL_PRESENT,
            "Explicit synthetic human approval evidence is present.",
        ),
    )


def _forbidden_actions() -> tuple[str, ...]:
    return (
        "git add",
        "git commit",
        "git push",
        "git reset",
        "git clean",
        "git stash",
        "git worktree",
        "Graphify",
        "provider calls",
        "model calls",
        "runtime execution",
        "filesystem writes from the pilot",
    )


def _response_sections() -> tuple[str, ...]:
    return (
        "Summary",
        "Files inspected",
        "Files modified",
        "Tests/commands run",
        "Decisions made",
        "Limitations",
    )


def _canonical_project_spec() -> ProjectSpec:
    return ProjectSpec.model_validate({
        "schema_version": 1,
        "project_id": "P16",
        "title": "Ticket Factory shadow pilot project",
        "objective": "Run a deterministic shadow-only pilot across accepted Ticket Factory contracts.",
        "summary": "Synthetic P16.8 project for bounded in-memory shadow evidence.",
        "context": [
            "Accepted P16.0-P16.7 contracts are the only authority for this pilot."
        ],
        "authority_references": [
            {
                "kind": AuthorityReferenceKind.GOVERNANCE_RECORD.value,
                "value": "0_architecture/governance/agent_platform_pepper_ticket_factory_shadow_pilot.md",
                "rationale": "P16.8 governance record authorizes shadow-only evidence.",
                "required": True,
            }
        ],
        "scope": {
            "allowed_paths": [
                "hermes_cli/agent_platform/ticket_factory/shadow_pilot.py"
            ],
            "forbidden_paths": ["4_external/sources/**"],
            "allowed_actions": ["create deterministic in-memory shadow pilot evidence"],
            "forbidden_actions": list(_forbidden_actions()),
        },
        "constraints": [
            "No provider, model, runtime, filesystem, Git, Graphify, Docker or WorkPacket authority is granted."
        ],
        "non_goals": [
            "No real ticket execution, repository publication or production readiness is claimed."
        ],
        "acceptance_criteria": [
            "The pilot emits deterministic shadow-only evidence over accepted contracts."
        ],
        "completion_verdict": "shadow_pilot_project_ready",
    })


def _canonical_seed_ticket() -> TicketSpec:
    return TicketSpec.model_validate({
        "schema_version": 1,
        "project_id": "P16",
        "ticket_id": "P16.SP1",
        "title": "Ticket Factory shadow pilot",
        "ticket_type": "integration",
        "objective": "Exercise the accepted Ticket Factory chain without execution authority.",
        "context": [
            "P16.8 composes P16.0-P16.7 contracts in one deterministic in-memory shadow run."
        ],
        "authority_references": [
            {
                "kind": AuthorityReferenceKind.GOVERNANCE_RECORD.value,
                "value": "0_architecture/governance/agent_platform_pepper_ticket_factory_shadow_pilot.md",
                "rationale": "Shadow pilot governance record.",
                "required": True,
            },
            {
                "kind": AuthorityReferenceKind.COMMIT.value,
                "value": "80e585dcc39b3bc67c10f9ca597c1dca3f442f12",
                "rationale": "Committed P16.7 authority for pre-change identity.",
                "required": True,
            },
        ],
        "dependencies": [],
        "parallelization_hint": "unspecified",
        "scope": {
            "allowed_paths": [
                "0_architecture/governance/agent_platform_pepper_ticket_factory_shadow_pilot.md",
                "2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv",
                "2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv",
                "2_products/pepper-agent/docs/agent-platform/ticket_factory_shadow_pilot.md",
                "2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/__init__.py",
                "2_products/pepper-agent/hermes_cli/agent_platform/ticket_factory/shadow_pilot.py",
                "2_products/pepper-agent/tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py",
            ],
            "forbidden_paths": ["4_external/sources/**"],
            "allowed_actions": [
                "add deterministic shadow pilot contracts and evidence"
            ],
            "forbidden_actions": list(_forbidden_actions()),
        },
        "constraints": [
            "Rollback by removing only the P16.8 shadow pilot module, tests, docs, governance record and registry rows.",
            "The pilot remains shadow-only and must not execute tickets or validation commands.",
        ],
        "tasks": [
            "Create a deterministic in-memory request and report for the shadow pilot.",
            "Run historical regression before downstream shadow evidence is accepted.",
            "Record explicit synthetic human approval and logical publication evidence only.",
        ],
        "acceptance_criteria": [
            "Canonical run prints go_with_constraints P16.SP1 pass 12 12 0 4 4 approved published.",
            "All public evidence models validate with deterministic SHA-256 digests.",
            "Rollback remains limited to removing only P16.8-owned files and rows.",
        ],
        "validation_steps": [
            {
                "validation_id": "V1",
                "description": "Run the focused P16.8 shadow pilot tests.",
                "command": "python -m pytest tests/hermes_cli/test_agent_platform_ticket_factory_shadow_pilot.py -q",
                "expected_result": "The focused suite passes without warnings.",
                "required": True,
            },
            {
                "validation_id": "V2",
                "description": "Run the canonical shadow pilot output smoke.",
                "command": 'python -c "from hermes_cli.agent_platform.ticket_factory import canonical_ticket_factory_shadow_pilot_output; print(canonical_ticket_factory_shadow_pilot_output())"',
                "expected_result": "go_with_constraints P16.SP1 pass 12 12 0 4 4 approved published",
                "required": True,
            },
        ],
        "response_contract": {
            "required_sections": list(_response_sections()),
            "completion_verdict": "hermes_0_19_pepper_ticket_factory_shadow_pilot_ready_with_shadow_only_non_executing_evidence",
            "include_files_inspected": True,
            "include_files_modified": True,
            "include_commands_run": True,
            "include_tests_run": True,
            "include_limitations": True,
        },
        "recommended_commit_message": "P16.8 Add ticket factory shadow pilot",
    })


def _canonical_context_sources() -> tuple[ContextSourceSpec, ...]:
    return (
        ContextSourceSpec.model_validate({
            "source_id": "CTX-SHADOW-PILOT-GOVERNANCE",
            "kind": ContextSourceKind.GOVERNANCE_RECORD.value,
            "title": "P16.8 shadow pilot governance",
            "source_reference": "governance:ticket-factory-shadow-pilot",
            "content": "P16.8 authorizes shadow-only deterministic in-memory evidence over accepted contracts.",
            "authority_references": (),
            "sensitivity": ContextSensitivity.INTERNAL.value,
            "priority": ContextPriority.HIGH.value,
            "required": False,
        }),
        ContextSourceSpec.model_validate({
            "source_id": "CTX-HISTORICAL-REGRESSION",
            "kind": ContextSourceKind.HISTORICAL_TICKET.value,
            "title": "P16.7 historical regression handoff",
            "source_reference": "historical-regression:pepper-ticket-factory-v1",
            "content": "P16.7 provides a frozen 12-case in-memory regression corpus with zero-drift passing evidence.",
            "authority_references": (),
            "sensitivity": ContextSensitivity.INTERNAL.value,
            "priority": ContextPriority.NORMAL.value,
            "required": False,
        }),
    )


def get_canonical_ticket_factory_shadow_pilot_request() -> (
    TicketFactoryShadowPilotRequest
):
    """Return the canonical P16.8 shadow pilot request."""

    return TicketFactoryShadowPilotRequest(
        project_spec=_canonical_project_spec(),
        seed_ticket=_canonical_seed_ticket(),
        context_sources=_canonical_context_sources(),
        requested_roles=(
            TicketGeneratorRole.ARCHITECTURE,
            TicketGeneratorRole.INTEGRATION,
            TicketGeneratorRole.GOVERNANCE,
            TicketGeneratorRole.DOCUMENTATION,
        ),
    )


def _proposal_rationale(role: TicketGeneratorRole) -> str:
    return (
        "Synthetic externally supplied shadow proposal for role "
        f"{role.value}; content is bounded so synthesis preserves one "
        "deterministic title dissent for human approval evidence."
    )


def _proposal_for_assignment(
    assignment: GeneratorAssignment,
    ticket: TicketSpec,
) -> TicketProposal:
    proposed_ticket = (
        _ticket_with_alternate_title(ticket)
        if assignment.role is TicketGeneratorRole.DOCUMENTATION
        else ticket
    )
    return build_ticket_proposal(
        assignment=assignment,
        proposed_ticket=proposed_ticket,
        rationale=_proposal_rationale(assignment.role),
        evidence_source_ids=(
            "CTX-SHADOW-PILOT-GOVERNANCE",
            "CTX-HISTORICAL-REGRESSION",
        ),
        assumptions=("Shadow-only pilot evidence remains non-executing.",),
        risks=("Human rollout and WorkPacket execution remain deferred.",),
        unresolved_questions=(),
    )


def _ticket_with_alternate_title(ticket: TicketSpec) -> TicketSpec:
    return TicketSpec.model_validate({
        **ticket.model_dump(mode="json"),
        "title": SHADOW_PILOT_ALTERNATE_TITLE,
    })


def _reviewed_proposal(
    project_spec: ProjectSpec,
    proposal: TicketProposal,
) -> ReviewedTicketProposal:
    lint_report = lint_ticket_collection(
        TicketLintRequest(
            project_spec=project_spec,
            tickets=(proposal.proposed_ticket,),
            dependency_plan=None,
            collection_complete=False,
        )
    )
    return ReviewedTicketProposal(proposal=proposal, lint_report=lint_report)


def _validate_preconditions(request: TicketFactoryShadowPilotRequest) -> None:
    try:
        TicketFactoryShadowPilotRequest.model_validate(request.model_dump(mode="json"))
    except ValueError as exc:
        raise TicketFactoryShadowPilotInputError(str(exc)) from exc


def _report_digest(report: TicketFactoryShadowPilotReport) -> str:
    record = {
        "algorithm": REPORT_DIGEST_ALGORITHM,
        **report.model_dump(mode="json", exclude={"report_SHA256"}),
    }
    return _sha256_text(_deterministic_json(record))


def _expected_disposition(
    report: TicketFactoryShadowPilotReport,
) -> ShadowPilotDisposition:
    if any(gate.status is ShadowPilotGateStatus.FAIL for gate in report.gate_results):
        return ShadowPilotDisposition.BLOCKED
    return ShadowPilotDisposition.GO_WITH_CONSTRAINTS


def _validate_report_artifacts(
    report: TicketFactoryShadowPilotReport,
    *,
    error_type: type[Exception],
) -> None:
    if report.ticket_id != report.context_pack.ticket_id:
        raise error_type("report ticket_id must match context pack")
    if report.ticket_id != report.dependency_plan.ticket_ids[0]:
        raise error_type("report ticket_id must match dependency plan")
    if report.ticket_lint_report.ticket_ids != (report.ticket_id,):
        raise error_type("lint report must cover the shadow ticket")
    if report.generation_request.ticket_spec.ticket_id != report.ticket_id:
        raise error_type("generation request must target the shadow ticket")
    if report.generation_request.context_pack != report.context_pack:
        raise error_type("generation request must use the report context pack")
    if tuple(stage.stage for stage in report.stage_results) != _STAGE_ORDER:
        raise error_type("stage_results must follow canonical stage order")
    if tuple(gate.gate for gate in report.gate_results) != _GATE_ORDER:
        raise error_type("gate_results must follow canonical gate order")
    for gate in report.gate_results:
        if gate.stage is not _GATE_STAGE[gate.gate]:
            raise error_type("gate stage must match canonical gate mapping")
    if report.historical_run.disposition is not HistoricalRegressionRunDisposition.PASS:
        raise error_type("historical regression preflight must pass")
    if report.historical_run.drifted_case_ids:
        raise error_type("historical regression preflight must have zero drift")
    if report.ticket_lint_report.disposition is TicketLintDisposition.BLOCKED:
        raise error_type("shadow ticket lint report must not be blocked")
    if len(report.assignments) != len(report.proposals):
        raise error_type("assignments and proposals must have equal counts")
    if tuple(assignment.ticket_id for assignment in report.assignments) != (
        report.ticket_id,
    ) * len(report.assignments):
        raise error_type("assignments must target the shadow ticket")
    if tuple(proposal.ticket_id for proposal in report.proposals) != (
        report.ticket_id,
    ) * len(report.proposals):
        raise error_type("proposals must target the shadow ticket")
    if report.synthesis_review.ticket_id != report.ticket_id:
        raise error_type("synthesis review must target the shadow ticket")
    if (
        report.synthesis_review.disposition
        is not TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT
    ):
        raise error_type("synthesis review must be review_ready_with_dissent")
    title_dissent = tuple(
        conflict
        for conflict in report.synthesis_review.conflicts
        if conflict.kind is ProposalConflictKind.FIELD_DISSENT
        and conflict.field is TicketSynthesisField.TITLE
    )
    if len(title_dissent) != 1:
        raise error_type("synthesis review must contain one title dissent conflict")
    if report.synthesis_review.candidate is None:
        raise error_type("synthesis review must include a candidate")
    if (
        report.synthesis_review.candidate.synthesized_ticket
        != report.generation_request.ticket_spec
    ):
        raise error_type("synthesis candidate must preserve the seed ticket")
    if report.approval_record.ticket_id != report.ticket_id:
        raise error_type("approval record must target the shadow ticket")
    if report.approval_record.state is not TicketApprovalState.APPROVED:
        raise error_type("approval record must be approved")
    if report.publication_result.publication.ticket_id != report.ticket_id:
        raise error_type("publication must target the shadow ticket")
    if (
        report.publication_result.publication.state
        is not TicketPublicationState.PUBLISHED
    ):
        raise error_type("publication state must be published")
    if report.disposition is not _expected_disposition(report):
        raise error_type("disposition must match gate statuses")


def validate_ticket_factory_shadow_pilot_report(
    report: TicketFactoryShadowPilotReport,
) -> None:
    """Validate report integrity and cross-artifact identity."""

    try:
        TicketFactoryShadowPilotReport.model_validate(report.model_dump(mode="json"))
    except ValueError as exc:
        raise TicketFactoryShadowPilotIntegrityError(str(exc)) from exc


def run_ticket_factory_shadow_pilot(
    request: TicketFactoryShadowPilotRequest | None = None,
) -> TicketFactoryShadowPilotReport:
    """Run the deterministic in-memory P16.8 shadow pilot."""

    resolved_request = (
        get_canonical_ticket_factory_shadow_pilot_request()
        if request is None
        else request
    )
    _validate_preconditions(resolved_request)

    historical_run = run_historical_ticket_regression_corpus()
    if historical_run.disposition is not HistoricalRegressionRunDisposition.PASS:
        raise TicketFactoryShadowPilotExecutionError(
            "historical regression preflight drifted"
        )

    context_pack = assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=resolved_request.project_spec,
            ticket_spec=resolved_request.seed_ticket,
            sources=resolved_request.context_sources,
            policy=ContextAssemblyPolicy(),
        )
    )
    dependency_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(
            project_spec=resolved_request.project_spec,
            tickets=(resolved_request.seed_ticket,),
            external_dependency_resolutions=(),
        )
    )
    ticket_lint_report = lint_ticket_collection(
        TicketLintRequest(
            project_spec=resolved_request.project_spec,
            tickets=(resolved_request.seed_ticket,),
            dependency_plan=None,
            collection_complete=False,
        )
    )
    if ticket_lint_report.disposition is TicketLintDisposition.BLOCKED:
        raise TicketFactoryShadowPilotExecutionError("shadow ticket lint is blocked")

    generation_request = TicketGenerationRequest(
        project_spec=resolved_request.project_spec,
        ticket_spec=resolved_request.seed_ticket,
        context_pack=context_pack,
        roles=resolved_request.requested_roles,
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    proposals = tuple(
        _proposal_for_assignment(assignment, resolved_request.seed_ticket)
        for assignment in assignments
    )
    reviewed_proposals = tuple(
        _reviewed_proposal(resolved_request.project_spec, proposal)
        for proposal in proposals
    )
    synthesis_review = build_ticket_synthesis_review(
        TicketSynthesisRequest(
            generation_request=generation_request,
            assignments=assignments,
            reviewed_proposals=reviewed_proposals,
            dependency_plan=dependency_plan,
        )
    )
    if (
        synthesis_review.disposition
        is not TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT
    ):
        raise TicketFactoryShadowPilotExecutionError(
            "shadow synthesis review is not review_ready_with_dissent"
        )
    title_conflicts = tuple(
        conflict
        for conflict in synthesis_review.conflicts
        if conflict.kind is ProposalConflictKind.FIELD_DISSENT
        and conflict.field is TicketSynthesisField.TITLE
    )
    if len(title_conflicts) != 1:
        raise TicketFactoryShadowPilotExecutionError(
            "shadow synthesis review must have one title dissent conflict"
        )

    approval_record = build_ticket_approval_record(
        TicketApprovalRequest(
            project_spec=resolved_request.project_spec,
            seed_ticket=resolved_request.seed_ticket,
            synthesis_review=synthesis_review,
            decision=HumanApprovalDecision.APPROVE,
            conflict_resolutions=(
                HumanConflictResolution(
                    conflict_id=title_conflicts[0].conflict_id,
                    action=ConflictResolutionAction.ACCEPT_CANDIDATE,
                    rationale="Accept the strict-majority seed-title candidate while preserving the dissent evidence.",
                    evidence_reference="shadow-pilot:P16.8:title-dissent-resolution",
                ),
            ),
            approval_evidence=HumanApprovalEvidence(
                reviewer_id="shadow-reviewer-p16-8",
                decision_reference="shadow-pilot:P16.8:review",
                rationale="Synthetic human approval evidence for shadow-only pilot readiness.",
            ),
            manual_replacement=None,
            fresh_planning_evidence=None,
        )
    )
    publication_result = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approval_record,
            publication_evidence=TicketPublicationEvidence(
                publisher_id="shadow-publisher-p16-8",
                publication_reference="shadow-pilot:P16.8:publication",
                rationale="Synthetic logical publication evidence for shadow-only pilot readiness.",
            ),
            prior_publication=None,
            supersession_rationale=None,
        )
    )
    stage_results = _make_stage_results(
        ticket_id=resolved_request.seed_ticket.ticket_id,
        historical_run=historical_run,
        context_pack=context_pack,
        dependency_plan=dependency_plan,
        assignments=assignments,
        proposals=proposals,
        synthesis_review=synthesis_review,
        approval_record=approval_record,
        publication_result=publication_result,
    )
    gate_results = _make_gate_results()
    report = TicketFactoryShadowPilotReport.model_construct(
        schema_version=TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION,
        pilot_id=TICKET_FACTORY_SHADOW_PILOT_ID,
        revision=TICKET_FACTORY_SHADOW_PILOT_REVISION,
        ticket_id=resolved_request.seed_ticket.ticket_id,
        request_SHA256=_request_digest(resolved_request),
        disposition=ShadowPilotDisposition.GO_WITH_CONSTRAINTS,
        stage_results=stage_results,
        gate_results=gate_results,
        historical_run=historical_run,
        context_pack=context_pack,
        dependency_plan=dependency_plan,
        ticket_lint_report=ticket_lint_report,
        generation_request=generation_request,
        assignments=assignments,
        proposals=proposals,
        synthesis_review=synthesis_review,
        approval_record=approval_record,
        publication_result=publication_result,
        report_SHA256="0" * 64,
    )
    return TicketFactoryShadowPilotReport(
        **report.model_dump(mode="json", exclude={"report_SHA256"}),
        report_SHA256=_report_digest(report),
    )


def summarize_ticket_factory_shadow_pilot_report(
    report: TicketFactoryShadowPilotReport,
) -> str:
    """Return the canonical one-line shadow pilot evidence summary."""

    validate_ticket_factory_shadow_pilot_report(report)
    return " ".join((
        report.disposition.value,
        report.ticket_id,
        report.historical_run.disposition.value,
        str(len(report.historical_run.case_results)),
        str(len(report.historical_run.passed_case_ids)),
        str(len(report.historical_run.drifted_case_ids)),
        str(len(report.assignments)),
        str(len(report.proposals)),
        report.approval_record.state.value,
        report.publication_result.publication.state.value,
    ))


def canonical_ticket_factory_shadow_pilot_output() -> str:
    """Run the canonical request and return the exact P16.8 smoke output."""

    return summarize_ticket_factory_shadow_pilot_report(
        run_ticket_factory_shadow_pilot()
    )
