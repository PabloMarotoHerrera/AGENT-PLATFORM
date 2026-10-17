"""Versioned passive validation declarations; no execution or approval objects.

Edges point producer/output evidence -> requirement. Producer prerequisites point
requirement -> producer. Display labels are excluded only from semantic identity;
the complete document identity still binds them. Historical digests are untouched.
"""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .contracts import ContentRef, ContractRef, Effect, Identifier, Observational, _Contract
from .validation import canonical_json, parse_contract, sha256_bytes

EvidenceStatus = Literal["ABSENT", "PRESENT", "PASSED", "FAILED", "INVALID", "STALE",
                         "CONFLICT", "UNSUPPORTED", "UNAVAILABLE"]
Condition = Literal["RECORDED", "PASSED", "FAILED", "HUMAN_APPROVED"]
AuthorityClass = Literal["NONE", "QUALIFIED_OWNER", "HUMAN"]


class ValidationContext(_Contract):
    current_ticket: Identifier
    successor_ticket: Identifier | None = None
    execution_target: Identifier
    human_decision_target: Identifier
    revision: Identifier
    run: Identifier


class AcceptanceCriterion(_Contract):
    criterion: ContractRef
    kind: Literal["ALL_PASSED", "HUMAN_ACCEPTANCE", "FAILURE_CLASSIFICATION"]
    required_facts: Annotated[tuple[Condition, ...], Field(min_length=1, max_length=4)]
    authority_class: AuthorityClass
    machine_evaluable: bool
    human_decision_required: bool
    permitted_effects: Annotated[tuple[Effect, ...], Field(min_length=1, max_length=5)] = (Effect.COMPUTE, Effect.OBSERVE)

    @model_validator(mode="after")
    def _authority(self):
        if self.kind != "ALL_PASSED":
            if self.machine_evaluable or not self.human_decision_required or self.authority_class != "HUMAN":
                raise ValueError("human criteria require an explicit human boundary")
        elif not self.machine_evaluable or self.human_decision_required:
            raise ValueError("machine criterion must be machine evaluable")
        elif self.authority_class == "HUMAN":
            raise ValueError("human authority cannot be machine evaluated")
        if len(set(self.required_facts)) != len(self.required_facts):
            raise ValueError("duplicate criterion fact")
        object.__setattr__(self, "required_facts", tuple(sorted(self.required_facts)))
        object.__setattr__(self, "permitted_effects", tuple(sorted(set(self.permitted_effects))))
        return self


class ValidationRequirement(_Contract):
    requirement: ContractRef
    category: Literal["COMMAND", "INSPECTION", "CONSISTENCY", "MANUAL", "CLASSIFICATION", "REVIEW", "TERMINAL", "IDENTITY", "MATERIAL_REVISION", "RECONCILIATION"]
    criterion: ContractRef
    expects: Annotated[tuple[ContractRef, ...], Field(min_length=1, max_length=32)]
    context: ValidationContext
    human_authority: bool = False
    description: Annotated[str, Field(max_length=2000)] = ""

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "expects", tuple(sorted(self.expects, key=canonical_json)))
        return self


class EvidenceProducer(_Contract):
    producer: ContractRef
    output: ContractRef
    effect: Effect
    qualification: Literal["UNQUALIFIED", "QUALIFIED", "UNAVAILABLE", "UNSUPPORTED"] = "UNQUALIFIED"
    requires: Annotated[tuple[ContractRef, ...], Field(max_length=32)] = ()
    historical_source: ContentRef | None = None
    handler_correspondence: ContentRef | None = None
    effect_policy: ContractRef | None = None

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "requires", tuple(sorted(self.requires, key=canonical_json)))
        return self


class EvidenceDependency(_Contract):
    dependency_id: Identifier
    consumer: ContractRef
    producer: ContractRef
    evidence: ContractRef
    expected_source: ContentRef
    condition: Condition
    required: bool = True
    failure_behavior: Literal["BLOCK", "EXPOSE_HUMAN_CLASSIFICATION"] = "BLOCK"


class ValidationBoundary(_Contract):
    producer: ContractRef
    output: ContractRef
    kind: Literal["EXTERNAL", "HUMAN"]
    provenance: ContentRef


class ValidationDAG(_Contract):
    graph: ContractRef
    policy: ContractRef
    requirements: Annotated[tuple[ValidationRequirement, ...], Field(max_length=64)]
    producers: Annotated[tuple[EvidenceProducer, ...], Field(max_length=128)]
    dependencies: Annotated[tuple[EvidenceDependency, ...], Field(max_length=256)]
    criteria: Annotated[tuple[AcceptanceCriterion, ...], Field(max_length=64)]
    boundaries: Annotated[tuple[ValidationBoundary, ...], Field(max_length=128)] = ()
    historical_mapping: Literal["NATIVE", "EXACT_COMPATIBLE", "PARTIALLY_OBSERVABLE", "AMBIGUOUS_HISTORICAL_SEMANTICS"] = "NATIVE"
    historical_source: ContentRef | None = None
    compatibility_policy: ContractRef | None = None
    unresolved_history: Annotated[tuple[Identifier, ...], Field(max_length=128)] = ()

    @model_validator(mode="after")
    def _order(self):
        for field in ("requirements", "producers", "dependencies", "criteria", "boundaries"):
            object.__setattr__(self, field, tuple(sorted(getattr(self, field), key=canonical_json)))
        object.__setattr__(self, "unresolved_history", tuple(sorted(self.unresolved_history)))
        if self.historical_mapping != "NATIVE" and (self.historical_source is None or self.compatibility_policy is None):
            raise ValueError("historical projection needs source and policy")
        return self

    def identity(self, *, presentation: bool = False) -> ContentRef:
        graph = parse_contract(ValidationDAG, canonical_json(self))
        if not presentation:
            # Description changes retain semantic identity, but not document identity.
            graph = ValidationDAG.model_validate({**graph.model_dump(), "requirements": tuple(
                ValidationRequirement.model_validate({**r.model_dump(), "description": ""}) for r in graph.requirements)})
        domain = "harness-validation-document-v1" if presentation else "harness-validation-dag-v1"
        return ContentRef(content_id=domain, sha256=sha256_bytes((domain + ":" + canonical_json(graph)).encode()))


class ValidationObservation(_Contract):
    evidence: ContractRef
    artifact: ContentRef
    producer: ContractRef
    source: ContentRef
    context: ValidationContext
    status: EvidenceStatus
    outcome: Literal["PASSED", "FAILED", "UNKNOWN"] = "UNKNOWN"
    qualification: Literal["UNQUALIFIED", "SYNTHETIC_ASSUMPTION"] = "UNQUALIFIED"
    owner: ContentRef | None = None
    authority_class: AuthorityClass = "NONE"
    human_decision: Literal["PENDING", "APPROVED", "REJECTED", "NONE"] = "NONE"
    decision_for: ContractRef | None = None
    binds_evidence: Annotated[tuple[ContentRef, ...], Field(max_length=32)] = ()
    historical: bool = False

    @model_validator(mode="after")
    def _status(self):
        if self.status in {"PASSED", "FAILED"} and self.outcome != self.status:
            raise ValueError("evidence status/outcome conflict")
        if self.outcome != "UNKNOWN" and self.status not in {"PASSED", "FAILED"}:
            raise ValueError("only observed outcomes have passed/failed status")
        object.__setattr__(self, "binds_evidence", tuple(sorted(self.binds_evidence, key=canonical_json)))
        return self

    def identity(self) -> ContentRef:
        return ContentRef(content_id="harness-validation-observation-v1", sha256=sha256_bytes(
            ("harness-validation-observation-v1:" + canonical_json(self)).encode()))


class SyntheticAuthorityAssumption(_Contract):
    """Explicit fixture input only; no production trusted owner is implemented."""
    owner: ContentRef
    scope: Literal["ISOLATED_SYNTHETIC_TEST_ONLY"]
    provenance: ContentRef


class ValidationAssessment(_Contract):
    graph: ContentRef
    requirement: ContractRef
    observed_evidence: Annotated[tuple[ContentRef, ...], Field(max_length=512)]
    qualification_scope: Literal["UNQUALIFIED", "ISOLATED_SYNTHETIC_TEST_ONLY"]
    synthetic_assumption: ContentRef | None = None
    prerequisite_state: Literal["SATISFIED", "BLOCKED"]
    evidence_available: bool
    evidence_valid: bool
    acceptance_readiness: Literal["BLOCKED", "READY_MACHINE", "HUMAN_DECISION_REQUIRED", "HUMAN_CLASSIFICATION_REQUIRED", "HUMAN_DECISION_RECORDED"]
    criterion_satisfied: bool
    required_human_continuation: bool
    resolution_authority: Literal["NONE", "CONTRACT_OWNER", "HUMAN_OWNER"]
    reason_codes: tuple[Identifier, ...]
    missing_producers: tuple[ContractRef, ...] = ()
    invalid_dependencies: tuple[Identifier, ...] = ()
    observational: Observational = True
    grants_authority: Literal[False] = False
    accepted: Literal[False] = False
