"""Bounded structural verification. Reachable never means authorized or available.

Operation requirements are AND; evidence providers are explicit OR alternatives
unless unique ownership is requested. Human/external roots require named,
provenanced assumptions. No storage, discovery, predicates or execution.
"""

from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .admissibility import AdmissionPolicy
from .catalog import CatalogSnapshot, LookupStatus
from .contracts import ContentRef, ContinuationKind, ContractRef, Effect, Identifier, _Contract
from .validation import canonical_json, parse_contract, sha256_bytes


class ProducerKind(str, Enum):
    INTERNAL_PRODUCER = "INTERNAL_PRODUCER"
    EXTERNAL_PRODUCER = "EXTERNAL_PRODUCER"
    HUMAN_PRODUCER = "HUMAN_PRODUCER"
    UNRESOLVED = "UNRESOLVED"
    INVALID = "INVALID"


class Correspondence(_Contract):
    """Injected passive HAR-06 proof summary; no runtime availability claim."""
    capability: ContractRef
    adapter: ContractRef
    proof: ContentRef
    source: ContentRef
    status: Literal["VERIFIED", "ABSENT", "AMBIGUOUS", "CONTRADICTORY", "UNVERIFIABLE"]


class Producer(_Contract):
    producer: ContractRef
    kind: ProducerKind
    output: ContractRef
    operation: ContractRef | None = None
    boundary: ContractRef | None = None
    provenance: Annotated[tuple[ContentRef, ...], Field(max_length=4)] = ()
    source_contract: ContractRef | None = None
    projection: ContractRef | None = None


class EvidenceNode(_Contract):
    evidence: ContractRef
    contract: ContractRef
    role: Literal["ARTIFACT", "INSPECTION", "FACT", "HUMAN_DECISION"]
    providers: Annotated[tuple[Producer, ...], Field(max_length=8)] = ()
    ownership: Literal["OR", "UNIQUE"] = "OR"

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "providers", tuple(sorted(self.providers, key=canonical_json)))
        return self


class Boundary(_Contract):
    boundary: ContractRef
    kind: Literal[ProducerKind.EXTERNAL_PRODUCER, ProducerKind.HUMAN_PRODUCER]
    provenance: Annotated[tuple[ContentRef, ...], Field(min_length=1, max_length=4)]
    assumed_available: bool = False


class EvidenceSeed(_Contract):
    evidence: ContractRef
    provenance: ContentRef
    assumption: Identifier


class OperationNode(_Contract):
    capability: ContractRef
    transition: ContractRef
    policy: AdmissionPolicy
    correspondence: Correspondence | None
    requires: Annotated[tuple[ContractRef, ...], Field(max_length=32)]
    invocable: bool = True
    continuation_kinds: Annotated[tuple[ContinuationKind, ...], Field(min_length=1, max_length=5)]
    authority_requirements: Annotated[tuple["AuthorityRequirement", ...], Field(max_length=32)] = ()

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "requires", tuple(sorted(self.requires, key=str)))
        object.__setattr__(self, "continuation_kinds", tuple(sorted(self.continuation_kinds)))
        object.__setattr__(self, "authority_requirements", tuple(sorted(self.authority_requirements, key=canonical_json)))
        return self


class AuthorityRequirement(_Contract):
    kind: Identifier
    evidence: ContractRef
    human: bool = False


class ActionRelationship(_Contract):
    action: ContractRef
    mapping: Literal["MAPPED", "UNMAPPED", "UNSUPPORTED"]
    capability: ContractRef | None
    kind: ContinuationKind
    invocable: bool
    correspondence: ContentRef | None = None


class Invalidation(_Contract):
    event: ContractRef
    evidence: Annotated[tuple[ContractRef, ...], Field(min_length=1, max_length=128)]


class Remediation(_Contract):
    capability: ContractRef
    policy: ContractRef
    kind: Literal[ContinuationKind.EXTERNAL_REMEDIATION, ContinuationKind.SAFE_STOP]
    provenance: ContentRef
    implemented: bool = False
    grants_authority: bool = False


class RequirementConflict(_Contract):
    left: ContractRef
    right: ContractRef
    provenance: ContentRef


class CoverageModel(_Contract):
    model: ContractRef
    catalog: CatalogSnapshot
    catalog_content: ContentRef
    operations: Annotated[tuple[OperationNode, ...], Field(max_length=32)]
    evidence: Annotated[tuple[EvidenceNode, ...], Field(max_length=128)]
    boundaries: Annotated[tuple[Boundary, ...], Field(max_length=128)] = ()
    actions: Annotated[tuple[ActionRelationship, ...], Field(max_length=64)] = ()
    invalidations: Annotated[tuple[Invalidation, ...], Field(max_length=16)] = ()
    remediation: Annotated[tuple[Remediation, ...], Field(max_length=32)] = ()
    initial_evidence: Annotated[tuple[EvidenceSeed, ...], Field(max_length=128)] = ()
    invalidated: Annotated[tuple[ContractRef, ...], Field(max_length=128)] = ()
    permitted_effects: Annotated[tuple[Effect, ...], Field(max_length=5)] = ()
    assumptions: Annotated[tuple[Identifier, ...], Field(max_length=64)] = ()
    conflicts: Annotated[tuple[RequirementConflict, ...], Field(max_length=32)] = ()

    @model_validator(mode="after")
    def _order(self):
        for name, key in (("operations", lambda x: str(x.capability)), ("evidence", lambda x: str(x.evidence)),
                ("boundaries", lambda x: str(x.boundary)), ("actions", lambda x: str(x.action)),
                ("invalidations", lambda x: str(x.event)), ("remediation", lambda x: str(x.capability)),
                ("initial_evidence", lambda x: str(x.evidence))):
            object.__setattr__(self, name, tuple(sorted(getattr(self, name), key=lambda x: (key(x), canonical_json(x)))))
        object.__setattr__(self, "invalidated", tuple(sorted(self.invalidated, key=str)))
        object.__setattr__(self, "permitted_effects", tuple(sorted(self.permitted_effects)))
        object.__setattr__(self, "assumptions", tuple(sorted(self.assumptions)))
        object.__setattr__(self, "conflicts", tuple(sorted(self.conflicts, key=canonical_json)))
        return self

    def content_identity(self) -> ContentRef:
        return ContentRef(content_id=self.model.contract_id, sha256=sha256_bytes(
            b"har08-coverage-model-v1\0" + canonical_json(CoverageModel.model_validate(self)).encode()))


class ExplorationBounds(_Contract):
    operations: Annotated[int, Field(ge=1, le=32)] = 32
    evidence: Annotated[int, Field(ge=1, le=128)] = 128
    edges: Annotated[int, Field(ge=1, le=1024)] = 1024
    states: Annotated[int, Field(ge=1, le=4096)] = 512
    depth: Annotated[int, Field(ge=0, le=16)] = 4
    scenarios: Annotated[int, Field(ge=1, le=1024)] = 256
    work: Annotated[int, Field(ge=1, le=100000)] = 100000


class CoverageIssue(_Contract):
    code: Identifier
    subject: ContractRef
    classification: Literal["INVALID", "INCOMPLETE", "ASSUMPTION", "UNSUPPORTED"]
    witness: Annotated[tuple[ContractRef, ...], Field(max_length=32)] = ()


class OperationCoverage(_Contract):
    capability: ContractRef
    classification: Literal["STRUCTURALLY_COVERED", "COVERED_WITH_EXTERNAL_ASSUMPTIONS", "INCOMPLETE", "INVALID", "UNSUPPORTED"]
    reachable: bool


class CoverageReport(_Contract):
    model: ContentRef
    catalog: ContentRef
    correspondence_sources: Annotated[tuple[ContentRef, ...], Field(max_length=32)]
    correspondence_proofs: Annotated[tuple[ContentRef, ...], Field(max_length=32)]
    operation_count: int
    capability_count: int
    transition_count: int
    evidence_count: int
    producer_consumer_edges: int
    boundary_count: int
    unresolved_count: int
    issues: Annotated[tuple[CoverageIssue, ...], Field(max_length=256)]
    cycles: Annotated[tuple[tuple[ContractRef, ...], ...], Field(max_length=32)]
    operations: Annotated[tuple[OperationCoverage, ...], Field(max_length=32)]
    reachable_evidence: Annotated[tuple[ContractRef, ...], Field(max_length=128)]
    assumptions: Annotated[tuple[Identifier, ...], Field(max_length=256)]
    classification: Literal["STRUCTURALLY_COVERED", "COVERED_WITH_EXTERNAL_ASSUMPTIONS", "INCOMPLETE", "INVALID", "UNSUPPORTED"]
    bounds: ExplorationBounds
    bound_hits: Annotated[tuple[Identifier, ...], Field(max_length=8)]
    work_used: int
    complete: bool

    def content_identity(self) -> ContentRef:
        return ContentRef(content_id="har08-coverage-report", sha256=sha256_bytes(
            b"har08-coverage-report-v1\0" + canonical_json(CoverageReport.model_validate(self)).encode()))


def verify_coverage(model: CoverageModel, bounds: ExplorationBounds = ExplorationBounds()) -> CoverageReport:
    model = CoverageModel.model_validate(model)
    model = parse_contract(CoverageModel, canonical_json(model))
    bounds = ExplorationBounds.model_validate(bounds)
    issues = set()
    hits = set()
    work = 0

    def issue(code, subject, classification="INVALID", witness=()):
        issues.add((code, subject, classification, tuple(witness)))

    def tick():
        nonlocal work
        if work >= bounds.work:
            hits.add("work")
            return False
        work += 1
        return True

    def index(items, attribute):
        result = {}
        for item in items:
            key = getattr(item, attribute)
            if key in result:
                issue("duplicate_identity", key)
            result[key] = item
        return result

    ops = index(model.operations, "capability")
    evidence = index(model.evidence, "evidence")
    boundaries = index(model.boundaries, "boundary")
    index(model.actions, "action")
    index(model.invalidations, "event")
    index(model.initial_evidence, "evidence")
    index(model.remediation, "capability")
    edges = sum(len(o.requires) for o in model.operations) + sum(len(e.providers) for e in model.evidence)
    edges += len(model.actions) + sum(len(i.evidence) for i in model.invalidations) + len(model.remediation) + len(model.conflicts)
    for name, actual, limit in (("operations", len(model.operations), bounds.operations),
            ("evidence", len(model.evidence), bounds.evidence), ("edges", edges, bounds.edges)):
        if actual > limit:
            hits.add(name)
    if model.model.version != 1:
        issue("unsupported_model_version", model.model, "UNSUPPORTED")
    if model.catalog_content != model.catalog.content_identity():
        issue("catalog_identity_mismatch", model.model)
    invalid_ops = set()
    for op in model.operations:
        cap = model.catalog.resolve_capability(op.capability)
        trans = model.catalog.resolve_transition(op.transition)
        if cap.status != LookupStatus.DECLARED or trans.status != LookupStatus.DECLARED:
            issue("exact_declaration_missing", op.capability)
            invalid_ops.add(op.capability)
            continue
        c, t, p = cap.capability, trans.transition, op.policy
        if t.capability != c.capability or t.effect != c.effect or p.effect != c.effect:
            issue("declaration_effect_or_identity_conflict", op.capability)
        if p.capability != c.capability or p.transition != t.transition or p.catalog != model.catalog_content or p.policy.version != 1:
            issue("policy_not_applicable", op.capability)
        if p.unsupported_requirements:
            issue("policy_requirement_unsupported", op.capability, "UNSUPPORTED")
        if p.allow_kind not in op.continuation_kinds:
            issue("continuation_policy_mismatch", op.capability)
        if not set(c.required_authority_kinds) <= set(t.required_authority_kinds) <= set(p.required_authority_kinds):
            issue("authority_requirements_weakened", op.capability)
        if not set(p.prerequisites) <= set(op.requires) or not set(t.prerequisites) <= set(op.requires):
            issue("policy_prerequisite_missing", op.capability)
        if len(set(op.requires)) != len(op.requires):
            issue("duplicate_requirement", op.capability)
        mappings = {a.kind: a for a in op.authority_requirements}
        if len(mappings) != len(op.authority_requirements) or not set(p.required_authority_kinds) <= set(mappings):
            issue("authority_producer_mapping_missing", op.capability)
        for requirement in op.authority_requirements:
            if requirement.evidence not in op.requires:
                issue("authority_requirement_not_consumed", op.capability)
            if requirement.kind == p.consent_kind:
                node = evidence.get(requirement.evidence)
                if not requirement.human or node is None or not node.providers or any(
                        provider.kind != ProducerKind.HUMAN_PRODUCER for provider in node.providers):
                    issue("consent_producer_not_human", op.capability)
        if op.invocable and (op.correspondence is None or op.correspondence.status != "VERIFIED"):
            issue("executor_correspondence_missing", op.capability)
        if op.correspondence and (op.correspondence.capability != c.capability or op.correspondence.adapter != c.execution_adapter):
            issue("executor_identity_mismatch", op.capability)
        if ContinuationKind.EXECUTABLE_CAPABILITY in op.continuation_kinds and not op.invocable:
            issue("continuation_not_invocable", op.capability)
        if c.effect != Effect.OBSERVE and not {ContinuationKind.HUMAN_DECISION, ContinuationKind.SAFE_STOP} <= set(op.continuation_kinds):
            issue("human_stop_boundary_missing", op.capability)
        for requirement in op.requires:
            if requirement not in evidence:
                issue("prerequisite_undeclared", op.capability, witness=(requirement,))
        for conflict in model.conflicts:
            if {conflict.left, conflict.right} <= set(op.requires):
                issue("contradictory_prerequisites", op.capability, witness=(conflict.left, conflict.right))
    for conflict in model.conflicts:
        if conflict.left == conflict.right or conflict.left not in evidence or conflict.right not in evidence:
            issue("conflict_relationship_invalid", model.model)
    invalid_ops.update(subject for _, subject, kind, _ in issues if kind in ("INVALID", "UNSUPPORTED") and subject in ops)
    if model.catalog_content != model.catalog.content_identity() or model.model.version != 1:
        invalid_ops.update(ops)
    providers = {}
    seen_producers = set()
    ambiguous_evidence = {e.evidence for e in model.evidence if sum(n.evidence == e.evidence for n in model.evidence) > 1}
    ambiguous_boundaries = {b.boundary for b in model.boundaries if sum(n.boundary == b.boundary for n in model.boundaries) > 1}
    producer_counts = {}
    for node in model.evidence:
        for p in node.providers:
            producer_counts[p.producer] = producer_counts.get(p.producer, 0) + 1
    for node in model.evidence:
        valid = []
        if not node.providers:
            issue("producer_missing", node.evidence, "INCOMPLETE")
        if node.ownership == "UNIQUE" and len(node.providers) != 1:
            issue("producer_ownership_ambiguous", node.evidence)
        for producer in sorted(node.providers, key=lambda p: str(p.producer)):
            if producer.producer in seen_producers:
                issue("producer_identity_ambiguous", producer.producer)
            seen_producers.add(producer.producer)
            if (producer_counts[producer.producer] > 1 or node.evidence in ambiguous_evidence
                    or (node.ownership == "UNIQUE" and len(node.providers) != 1)):
                continue
            if producer.producer.version != 1:
                issue("producer_version_unsupported", node.evidence, "UNSUPPORTED")
                continue
            if producer.output != node.contract or producer.kind == ProducerKind.INVALID:
                issue("producer_contract_invalid", node.evidence)
                continue
            if producer.kind == ProducerKind.UNRESOLVED:
                issue("producer_unresolved", node.evidence, "INCOMPLETE")
                continue
            if not producer.provenance:
                issue("producer_provenance_missing", node.evidence, "INCOMPLETE")
                continue
            if producer.kind == ProducerKind.INTERNAL_PRODUCER:
                if producer.operation not in ops or producer.boundary is not None:
                    issue("producer_operation_missing", node.evidence)
                    continue
                source = model.catalog.resolve_capability(producer.operation).capability
                if source is None or producer.source_contract != source.evidence_contract or (
                        producer.output != producer.source_contract and producer.projection is None):
                    issue("producer_source_contract_invalid", node.evidence)
                    continue
            else:
                boundary = boundaries.get(producer.boundary)
                if (producer.operation is not None or boundary is None or boundary.kind != producer.kind
                        or producer.boundary in ambiguous_boundaries):
                    issue("producer_boundary_invalid", node.evidence)
                    continue
            valid.append(producer)
        providers[node.evidence] = tuple(valid)
    for action in model.actions:
        diagnostic = action.kind in (ContinuationKind.SAFE_STOP, ContinuationKind.EXTERNAL_REMEDIATION)
        if diagnostic and (action.invocable or action.correspondence is not None or action.capability is not None):
            issue("diagnostic_has_executor", action.action)
        if not diagnostic and (action.capability not in ops or (action.invocable and action.correspondence is None)):
            issue("action_capability_or_executor_missing", action.action)
        if action.capability in ops:
            op = ops[action.capability]
            if action.mapping == "MAPPED" and action.kind not in op.continuation_kinds:
                issue("action_continuation_mismatch", action.action)
            if action.invocable and (action.mapping != "MAPPED" or action.kind != ContinuationKind.EXECUTABLE_CAPABILITY
                    or not op.invocable or not op.correspondence or action.correspondence != op.correspondence.proof):
                issue("action_correspondence_conflict", action.action)
    for relation in model.invalidations:
        if len(set(relation.evidence)) != len(relation.evidence):
            issue("duplicate_invalidation_target", relation.event)
        for ref in relation.evidence:
            if ref not in evidence:
                issue("invalidation_target_missing", relation.event, witness=(ref,))
    for relation in model.remediation:
        if relation.capability not in ops or relation.grants_authority:
            issue("remediation_cannot_grant_authority", relation.capability)
        if not relation.implemented:
            issue("recovery_not_implemented", relation.capability, "ASSUMPTION")
    invalidated = set(model.invalidated)
    for ref in invalidated:
        if ref not in evidence:
            issue("invalidated_evidence_undeclared", ref)
    available = {s.evidence for s in model.initial_evidence if s.evidence in evidence and s.evidence not in invalidated}
    for seed in model.initial_evidence:
        if seed.evidence not in evidence:
            issue("initial_seed_undeclared", seed.evidence)
    reached = set()
    changed = True
    # Monotone finite closure, not a topological sort. Every producer's AND
    # prerequisites must be reached, but one explicit OR provider suffices.
    while changed and not hits:
        changed = False
        for node in model.evidence:
            if not tick():
                break
            if node.evidence in invalidated or node.evidence in available:
                continue
            for producer in providers[node.evidence]:
                if producer.kind == ProducerKind.INTERNAL_PRODUCER:
                    possible = producer.operation in reached
                else:
                    possible = boundaries[producer.boundary].assumed_available
                if possible:
                    available.add(node.evidence)
                    changed = True
                    break
        for op in model.operations:
            if not tick():
                break
            cap = model.catalog.resolve_capability(op.capability).capability
            if op.capability not in invalid_ops and cap and cap.effect in model.permitted_effects and set(op.requires) <= available:
                if op.capability not in reached:
                    reached.add(op.capability)
                    changed = True
    graph = {ref: set() for ref in ops}
    for op in model.operations:
        for requirement in op.requires:
            graph[op.capability].update(p.operation for p in providers.get(requirement, ())
                if p.kind == ProducerKind.INTERNAL_PRODUCER and p.operation in ops)
    closure = {r: set(v) for r, v in graph.items()}
    for pivot in sorted(ops, key=str):
        if "work" in hits:
            break
        for origin in sorted(ops, key=str):
            if not tick():
                break
            if pivot in closure[origin]:
                closure[origin].update(closure[pivot])
    cycles = set()
    for ref in ops:
        if ref in closure[ref]:
            cycles.add(tuple(sorted((other for other in ops if other in closure[ref] and ref in closure[other]), key=str)))
    ordered_cycles = tuple(sorted(cycles, key=str))
    for cycle in ordered_cycles:
        resolved = set(cycle) <= reached
        issue("cycle_seeded_or_alternative" if resolved else "prerequisite_cycle", cycle[0],
            "ASSUMPTION" if resolved else "INVALID", cycle)
    for op in model.operations:
        if op.capability not in reached:
            issue("operation_unreachable", op.capability, "INCOMPLETE",
                tuple(r for r in op.requires if r not in available)[:32])
    for node in model.evidence:
        if node.evidence not in available and any(p.kind == ProducerKind.INTERNAL_PRODUCER for p in providers[node.evidence]):
            issue("internal_producer_unreachable", node.evidence, "INCOMPLETE")
    for boundary in model.boundaries:
        if not boundary.assumed_available:
            issue("external_boundary_unqualified", boundary.boundary, "INCOMPLETE")
    ordered = sorted(issues, key=lambda i: (i[2], i[0], str(i[1]), str(i[3])))
    if len(ordered) > 256:
        hits.add("report_issues")
    assumptions = set(model.assumptions) | {s.assumption for s in model.initial_evidence}
    assumptions.update("boundary." + b.boundary.contract_id for b in model.boundaries if b.assumed_available)
    classifications = {i[2] for i in issues}
    classification = ("INVALID" if "INVALID" in classifications else "UNSUPPORTED" if "UNSUPPORTED" in classifications
        else "INCOMPLETE" if hits or "INCOMPLETE" in classifications else
        "COVERED_WITH_EXTERNAL_ASSUMPTIONS" if assumptions else "STRUCTURALLY_COVERED")
    results = []
    for op in model.operations:
        bad = any(i[1] == op.capability and i[2] == "INVALID" for i in issues)
        unsupported = any(i[1] == op.capability and i[2] == "UNSUPPORTED" for i in issues)
        results.append(OperationCoverage(capability=op.capability, reachable=op.capability in reached,
            classification="INVALID" if bad else "UNSUPPORTED" if unsupported else "INCOMPLETE" if op.capability not in reached else
            "COVERED_WITH_EXTERNAL_ASSUMPTIONS" if assumptions else "STRUCTURALLY_COVERED"))
    return CoverageReport(model=model.content_identity(), catalog=model.catalog_content,
        correspondence_sources=tuple(sorted({o.correspondence.source for o in model.operations if o.correspondence}, key=str)),
        correspondence_proofs=tuple(sorted({o.correspondence.proof for o in model.operations if o.correspondence}, key=str)),
        operation_count=len(model.operations), capability_count=len(model.catalog.capabilities),
        transition_count=len(model.catalog.transitions), evidence_count=len(model.evidence),
        producer_consumer_edges=edges, boundary_count=len(boundaries),
        unresolved_count=len({i[1] for i in issues if i[2] == "INCOMPLETE"}),
        issues=tuple(CoverageIssue(code=c, subject=s, classification=k, witness=w) for c, s, k, w in ordered[:256]),
        cycles=ordered_cycles, operations=tuple(results), reachable_evidence=tuple(sorted(available, key=str)),
        assumptions=tuple(sorted(assumptions)), classification=classification, bounds=bounds,
        bound_hits=tuple(sorted(hits)), work_used=work, complete=not hits)
