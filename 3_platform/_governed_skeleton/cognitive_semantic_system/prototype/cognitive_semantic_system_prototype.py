"""I-07 minimal Cognitive Semantic System metadata prototype.

This module models cognitive entities, semantic claims, semantic relations, and
substrate candidate records in memory only. It does not select a final
substrate, create graph/vector/database/ontology runtime, inspect Graphify,
load source contents, execute reasoning, call providers, execute tools, or
approve permissions. Semantic entity registration is not truth creation.
Semantic claim registration is not validation. Semantic relation registration
is not reasoning execution. Validation evaluates; governance decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class SemanticEntityKind(str, Enum):
    """Declared semantic entity kinds."""

    GOAL = "goal"
    TASK = "task"
    CONTEXT_PACK = "context_pack"
    EVIDENCE = "evidence"
    CLAIM = "claim"
    ACTION = "action"
    RECOMMENDATION = "recommendation"
    OUTPUT = "output"
    VALIDATION_RECORD = "validation_record"
    SECURITY_DECISION = "security_decision"
    AGENT_RECORD = "agent_record"
    TOOL_RECORD = "tool_record"
    PROVIDER_ADAPTER_RECORD = "provider_adapter_record"
    PRODUCT_GOVERNANCE = "product_governance"
    IMPLEMENTATION_ARTIFACT = "implementation_artifact"
    GOVERNANCE_DECISION = "governance_decision"
    SUBSTRATE_CANDIDATE = "substrate_candidate"
    UNKNOWN = "unknown"


class SemanticRelationKind(str, Enum):
    """Declared semantic relation kinds."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    REFINES = "refines"
    DEPENDS_ON = "depends_on"
    DERIVED_FROM = "derived_from"
    CONTEXTUALIZES = "contextualizes"
    CONSTRAINS = "constrains"
    VALIDATES_SCOPE = "validates_scope"
    SECURITY_LIMITS = "security_limits"
    BLOCKS = "blocks"
    SUPERSEDES = "supersedes"
    CANDIDATE_FOR = "candidate_for"
    UNKNOWN = "unknown"


class SemanticRecordStatus(str, Enum):
    """Statuses for metadata-only semantic records."""

    DRAFT = "draft"
    CANDIDATE = "candidate"
    LINKED_FOR_REVIEW = "linked_for_review"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    RECORDED_METADATA_ONLY = "recorded_metadata_only"


class SubstrateCandidateKind(str, Enum):
    """Substrate candidate kinds, not selected substrates."""

    GRAPH_CANDIDATE = "graph_candidate"
    VECTOR_INDEX_CANDIDATE = "vector_index_candidate"
    RELATIONAL_STORE_CANDIDATE = "relational_store_candidate"
    DOCUMENT_INDEX_CANDIDATE = "document_index_candidate"
    ONTOLOGY_CANDIDATE = "ontology_candidate"
    HYBRID_CANDIDATE = "hybrid_candidate"
    MEMORY_ONLY_CANDIDATE = "memory_only_candidate"
    UNKNOWN = "unknown"


class SubstrateDecisionStatus(str, Enum):
    """Decision postures that never mean selected."""

    CANDIDATE_ONLY = "candidate_only"
    DEFERRED = "deferred"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"


CSS_NAME_IS_ACCEPTED = "Cognitive Semantic System name is accepted"
PROTOTYPE_IS_NOT_FINAL_SUBSTRATE = "prototype is not final substrate selection"
GRAPH_REMAINS_CANDIDATE_ONLY = "graph remains candidate only"
GRAPHIFY_REMAINS_EVIDENCE_ONLY = "Graphify remains evidence only, not authority"
SEMANTIC_ENTITY_REGISTRATION_IS_NOT_TRUTH = (
    "semantic entity registration is not truth creation"
)
SEMANTIC_CLAIM_REGISTRATION_IS_NOT_VALIDATION = (
    "semantic claim registration is not validation"
)
SEMANTIC_RELATION_REGISTRATION_IS_NOT_REASONING = (
    "semantic relation registration is not reasoning execution"
)
SUBSTRATE_CANDIDATE_METADATA_IS_NOT_ADOPTION = (
    "substrate candidate metadata is not substrate adoption"
)


def _value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    return value


def _tuple_of_strings(values: object) -> object:
    if isinstance(values, str):
        return values
    try:
        return tuple(values)
    except TypeError:
        return values


@dataclass(frozen=True)
class CognitiveEntity:
    """Metadata-only cognitive entity; not truth creation."""

    entity_id: str
    entity_kind: str
    title: str
    summary: str
    status: str = SemanticRecordStatus.DRAFT.value
    context_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_kind", _value(self.entity_kind))
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "context_refs", _tuple_of_strings(self.context_refs))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "validation_refs", _tuple_of_strings(self.validation_refs))
        object.__setattr__(self, "security_refs", _tuple_of_strings(self.security_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class SemanticClaim:
    """Metadata-only semantic claim; not validation."""

    claim_id: str
    subject_entity_id: str
    claim: str
    status: str = SemanticRecordStatus.DRAFT.value
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "validation_refs", _tuple_of_strings(self.validation_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class SemanticRelation:
    """Metadata-only semantic relation; not reasoning execution."""

    relation_id: str
    source_entity_id: str
    target_entity_id: str
    relation_kind: str
    status: str = SemanticRecordStatus.DRAFT.value
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "relation_kind", _value(self.relation_kind))
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class SubstrateCandidateRecord:
    """Metadata-only substrate candidate; not substrate selection."""

    candidate_id: str
    candidate_kind: str
    name: str
    description: str
    decision_status: str = SubstrateDecisionStatus.DEFERRED.value
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_kind", _value(self.candidate_kind))
        object.__setattr__(self, "decision_status", _value(self.decision_status))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


class CognitiveSemanticSystemPrototype:
    """In-memory Cognitive Semantic System metadata prototype only."""

    def __init__(self) -> None:
        self._entities: Dict[str, CognitiveEntity] = {}
        self._claims: Dict[str, SemanticClaim] = {}
        self._relations: Dict[str, SemanticRelation] = {}
        self._substrate_candidates: Dict[str, SubstrateCandidateRecord] = {}

    def register_entity(self, entity: CognitiveEntity) -> CognitiveEntity:
        errors = self.validate_entity(entity)
        if errors:
            raise ValueError("; ".join(errors))
        if entity.entity_id in self._entities:
            raise ValueError(f"duplicate entity_id: {entity.entity_id}")
        self._entities[entity.entity_id] = entity
        return entity

    def register_claim(self, claim: SemanticClaim) -> SemanticClaim:
        errors = self.validate_claim(claim)
        if isinstance(claim, SemanticClaim) and claim.subject_entity_id not in self._entities:
            errors.append(f"subject_entity_id is not registered: {claim.subject_entity_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if claim.claim_id in self._claims:
            raise ValueError(f"duplicate claim_id: {claim.claim_id}")
        self._claims[claim.claim_id] = claim
        return claim

    def register_relation(self, relation: SemanticRelation) -> SemanticRelation:
        errors = self.validate_relation(relation)
        if isinstance(relation, SemanticRelation):
            if relation.source_entity_id not in self._entities:
                errors.append(f"source_entity_id is not registered: {relation.source_entity_id}")
            if relation.target_entity_id not in self._entities:
                errors.append(f"target_entity_id is not registered: {relation.target_entity_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if relation.relation_id in self._relations:
            raise ValueError(f"duplicate relation_id: {relation.relation_id}")
        self._relations[relation.relation_id] = relation
        return relation

    def register_substrate_candidate(
        self, candidate: SubstrateCandidateRecord
    ) -> SubstrateCandidateRecord:
        errors = self.validate_substrate_candidate(candidate)
        if errors:
            raise ValueError("; ".join(errors))
        if candidate.candidate_id in self._substrate_candidates:
            raise ValueError(f"duplicate candidate_id: {candidate.candidate_id}")
        self._substrate_candidates[candidate.candidate_id] = candidate
        return candidate

    def get_entity(self, entity_id: str) -> Optional[CognitiveEntity]:
        return self._entities.get(entity_id)

    def get_claim(self, claim_id: str) -> Optional[SemanticClaim]:
        return self._claims.get(claim_id)

    def get_relation(self, relation_id: str) -> Optional[SemanticRelation]:
        return self._relations.get(relation_id)

    def get_substrate_candidate(
        self, candidate_id: str
    ) -> Optional[SubstrateCandidateRecord]:
        return self._substrate_candidates.get(candidate_id)

    def list_entities(self) -> List[CognitiveEntity]:
        return list(self._entities.values())

    def list_claims(self) -> List[SemanticClaim]:
        return list(self._claims.values())

    def list_relations(self) -> List[SemanticRelation]:
        return list(self._relations.values())

    def list_substrate_candidates(self) -> List[SubstrateCandidateRecord]:
        return list(self._substrate_candidates.values())

    def list_claims_by_subject(self, subject_entity_id: str) -> List[SemanticClaim]:
        return [claim for claim in self._claims.values() if claim.subject_entity_id == subject_entity_id]

    def list_relations_by_source(self, source_entity_id: str) -> List[SemanticRelation]:
        return [relation for relation in self._relations.values() if relation.source_entity_id == source_entity_id]

    def list_relations_by_target(self, target_entity_id: str) -> List[SemanticRelation]:
        return [relation for relation in self._relations.values() if relation.target_entity_id == target_entity_id]

    def list_substrate_candidates_by_kind(
        self, candidate_kind: str
    ) -> List[SubstrateCandidateRecord]:
        return [candidate for candidate in self._substrate_candidates.values() if candidate.candidate_kind == candidate_kind]

    def list_substrate_candidates_by_decision_status(
        self, decision_status: str
    ) -> List[SubstrateCandidateRecord]:
        return [candidate for candidate in self._substrate_candidates.values() if candidate.decision_status == decision_status]

    @staticmethod
    def validate_entity(entity: CognitiveEntity) -> List[str]:
        if not isinstance(entity, CognitiveEntity):
            return ["entity must be a CognitiveEntity"]
        errors: List[str] = []
        required_text = {
            "entity_id": entity.entity_id,
            "entity_kind": entity.entity_kind,
            "title": entity.title,
            "summary": entity.summary,
            "status": entity.status,
            "created_at": entity.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("entity_kind", entity.entity_kind, SemanticEntityKind))
        errors.extend(_validate_allowed("status", entity.status, SemanticRecordStatus))
        errors.extend(_validate_bool("review_required", entity.review_required))
        for field_name in (
            "context_refs",
            "evidence_refs",
            "validation_refs",
            "security_refs",
            "limitations",
            "blockers",
        ):
            errors.extend(_validate_refs(field_name, getattr(entity, field_name)))
        errors.extend(_validate_review_posture(entity.status, entity.review_required, "entity"))
        return errors

    @staticmethod
    def validate_claim(claim: SemanticClaim) -> List[str]:
        if not isinstance(claim, SemanticClaim):
            return ["claim must be a SemanticClaim"]
        errors: List[str] = []
        required_text = {
            "claim_id": claim.claim_id,
            "subject_entity_id": claim.subject_entity_id,
            "claim": claim.claim,
            "status": claim.status,
            "created_at": claim.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("status", claim.status, SemanticRecordStatus))
        errors.extend(_validate_bool("review_required", claim.review_required))
        for field_name in ("evidence_refs", "validation_refs", "limitations", "blockers"):
            errors.extend(_validate_refs(field_name, getattr(claim, field_name)))
        errors.extend(_validate_review_posture(claim.status, claim.review_required, "claim"))
        return errors

    @staticmethod
    def validate_relation(relation: SemanticRelation) -> List[str]:
        if not isinstance(relation, SemanticRelation):
            return ["relation must be a SemanticRelation"]
        errors: List[str] = []
        required_text = {
            "relation_id": relation.relation_id,
            "source_entity_id": relation.source_entity_id,
            "target_entity_id": relation.target_entity_id,
            "relation_kind": relation.relation_kind,
            "status": relation.status,
            "created_at": relation.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("relation_kind", relation.relation_kind, SemanticRelationKind))
        errors.extend(_validate_allowed("status", relation.status, SemanticRecordStatus))
        errors.extend(_validate_bool("review_required", relation.review_required))
        for field_name in ("evidence_refs", "limitations", "blockers"):
            errors.extend(_validate_refs(field_name, getattr(relation, field_name)))
        errors.extend(_validate_review_posture(relation.status, relation.review_required, "relation"))
        return errors

    @staticmethod
    def validate_substrate_candidate(candidate: SubstrateCandidateRecord) -> List[str]:
        if not isinstance(candidate, SubstrateCandidateRecord):
            return ["candidate must be a SubstrateCandidateRecord"]
        errors: List[str] = []
        required_text = {
            "candidate_id": candidate.candidate_id,
            "candidate_kind": candidate.candidate_kind,
            "name": candidate.name,
            "description": candidate.description,
            "decision_status": candidate.decision_status,
            "created_at": candidate.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("candidate_kind", candidate.candidate_kind, SubstrateCandidateKind))
        errors.extend(_validate_allowed("decision_status", candidate.decision_status, SubstrateDecisionStatus))
        errors.extend(_validate_bool("review_required", candidate.review_required))
        for field_name in ("evidence_refs", "limitations", "blockers"):
            errors.extend(_validate_refs(field_name, getattr(candidate, field_name)))
        if isinstance(candidate.decision_status, str) and "selected" in candidate.decision_status:
            errors.append("substrate candidate status must not select a substrate")
        if candidate.review_required is False:
            errors.append("substrate candidate metadata requires review")
        return errors


def _validate_required_text(values: Dict[str, object]) -> List[str]:
    errors: List[str] = []
    for field_name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name} is required")
    return errors


def _validate_allowed(field_name: str, value: object, enum_type: object) -> List[str]:
    if not isinstance(value, str):
        return []
    allowed = {member.value for member in enum_type}
    if value not in allowed:
        return [f"{field_name} must be one of: {', '.join(sorted(allowed))}"]
    return []


def _validate_bool(field_name: str, value: object) -> List[str]:
    if not isinstance(value, bool):
        return [f"{field_name} must be a boolean"]
    return []


def _validate_refs(field_name: str, values: object) -> List[str]:
    if isinstance(values, str):
        return [f"{field_name} must be a sequence of strings"]
    try:
        iterator = iter(values)
    except TypeError:
        return [f"{field_name} must be a sequence of strings"]
    errors: List[str] = []
    for index, value in enumerate(iterator):
        if not isinstance(value, str):
            errors.append(f"{field_name}[{index}] must be a string")
        elif "\n" in value or "\r" in value:
            errors.append(f"{field_name} must be references or IDs, not raw contents")
    return errors


def _validate_review_posture(status: object, review_required: object, record_name: str) -> List[str]:
    if status == SemanticRecordStatus.RECORDED_METADATA_ONLY.value and review_required is False:
        return [f"{record_name} recorded_metadata_only is not approval"]
    if status in {
        SemanticRecordStatus.CANDIDATE.value,
        SemanticRecordStatus.LINKED_FOR_REVIEW.value,
        SemanticRecordStatus.NEEDS_REVIEW.value,
        SemanticRecordStatus.BLOCKED.value,
    } and review_required is False:
        return [f"{record_name} status requires review"]
    return []
