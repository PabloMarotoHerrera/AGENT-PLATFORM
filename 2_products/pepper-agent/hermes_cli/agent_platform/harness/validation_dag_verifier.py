"""Bounded structural verification and diagnostic assessment, never execution.

No production authority qualifier is provided. Positive qualification can only be
explored with an explicitly named isolated synthetic assumption. Even then the
result is observational and cannot accept a workflow or dispatch an effect.
"""

from typing import Annotated, Literal

from pydantic import Field

from .contracts import ContentRef, ContractRef, Effect, Identifier, Observational, _Contract
from .validation import MAX_JSON_BYTES, canonical_json, parse_contract
from .validation_dag import (SyntheticAuthorityAssumption, ValidationAssessment,
                             ValidationDAG, ValidationObservation)

POLICY = ContractRef(contract_id="harness-validation-verifier", version=1)


def key(ref):
    return ref.contract_id, ref.version


def token(kind, ref):
    return kind + ":" + ref.contract_id + ":" + str(ref.version)


class Diagnostic(_Contract):
    code: Identifier
    subjects: Annotated[tuple[Identifier, ...], Field(max_length=256)] = ()
    resolution_authority: Literal["CONTRACT_OWNER", "HUMAN_OWNER"] = "CONTRACT_OWNER"


class ValidationReport(_Contract):
    graph: ContentRef
    policy: ContractRef = POLICY
    node_count: int
    edge_count: int
    producer_count: int
    requirement_count: int
    criterion_count: int
    boundary_count: int
    topological_order: tuple[str, ...]
    cycle_witnesses: tuple[tuple[str, ...], ...]
    diagnostics: Annotated[tuple[Diagnostic, ...], Field(max_length=1024)]
    witness_limit_reached: bool
    structurally_valid: bool
    limitations: tuple[str, ...] = (
        "Finite declarations only; no runtime availability or production currentness.",
        "External and human boundaries unresolved unless explicitly assumed in synthetic fixtures.",
        "Diagnostic readiness never grants approval, authority or execution.",
        "Historical ambiguity/incomplete mappings block readiness; legacy owners remain unchanged.",
    )
    observational: Observational = True
    grants_authority: Literal[False] = False


def verify(graph: ValidationDAG) -> ValidationReport:
    g = parse_contract(ValidationDAG, canonical_json(graph))
    findings = set()

    def note(code, *subjects):
        findings.add((code, tuple(sorted(subjects))))

    def index(values, attr, name):
        found = {}
        for v in values:
            k = key(getattr(v, attr))
            if k in found:
                note("duplicate_" + name, k[0])
            found[k] = v
        return found

    reqs = index(g.requirements, "requirement", "requirement")
    producers = index(g.producers, "producer", "producer")
    criteria = index(g.criteria, "criterion", "criterion")
    boundaries = index(g.boundaries, "producer", "boundary")
    if g.policy != POLICY:
        note("unsupported_policy", g.policy.contract_id)
    if g.historical_mapping != "NATIVE" and (g.historical_mapping != "EXACT_COMPATIBLE" or g.unresolved_history):
        note("historical_mapping_unresolved", g.historical_mapping)
    nodes = {token("R", r.requirement) for r in g.requirements} | {token("P", p.producer) for p in g.producers} | {token("P", b.producer) for b in g.boundaries}
    adjacency = {n: set() for n in nodes}
    for k in producers.keys() & boundaries.keys():
        note("contradictory_producer_boundary", k[0])
    for p in g.producers:
        if p.effect not in (Effect.COMPUTE, Effect.OBSERVE) and (p.handler_correspondence is None or p.effect_policy is None):
            note("unbound_effectful_producer", p.producer.contract_id)
        for ref in p.requires:
            if key(ref) not in reqs:
                note("missing_producer_prerequisite", p.producer.contract_id, ref.contract_id)
            else:
                adjacency[token("R", ref)].add(token("P", p.producer))
    seen_edges = set()
    for d in g.dependencies:
        if d.dependency_id in seen_edges:
            note("duplicate_edge", d.dependency_id)
        seen_edges.add(d.dependency_id)
        r = reqs.get(key(d.consumer))
        p = producers.get(key(d.producer)) or boundaries.get(key(d.producer))
        if r is None:
            note("missing_consumer", d.dependency_id)
        if p is None:
            versions = [x for x in (*g.producers, *g.boundaries) if x.producer.contract_id == d.producer.contract_id]
            note("producer_version_mismatch" if versions else "missing_internal_producer", d.producer.contract_id)
        elif p.output != d.evidence:
            note("producer_output_mismatch", d.dependency_id)
        if r and p:
            adjacency[token("P", d.producer)].add(token("R", r.requirement))
            c = criteria.get(key(r.criterion))
            if c and hasattr(p, "effect") and p.effect not in c.permitted_effects:
                note("producer_effect_policy_conflict", d.dependency_id)
            if d.condition not in (c.required_facts if c else ()):
                note("undeclared_criterion_fact", d.dependency_id)
            if c and c.kind == "ALL_PASSED" and (d.condition != "PASSED" or d.failure_behavior != "BLOCK"):
                note("failed_to_accepted_policy", d.dependency_id)
            if c and c.kind == "HUMAN_ACCEPTANCE" and d.condition != "PASSED":
                note("human_aggregate_requires_passed", d.dependency_id)
    for r in g.requirements:
        c = criteria.get(key(r.criterion))
        deps = [d for d in g.dependencies if d.consumer == r.requirement and d.required]
        if c is None:
            note("missing_criterion", r.requirement.contract_id)
        elif r.human_authority != c.human_decision_required:
            note("authority_classification_conflict", r.requirement.contract_id)
        if {key(d.evidence) for d in deps} != {key(e) for e in r.expects}:
            note("unreachable_required_evidence", r.requirement.contract_id)
        if len({key(e) for e in r.expects}) != len(r.expects):
            note("duplicate_evidence_expectation", r.requirement.contract_id)
        if c and set(c.required_facts) != {d.condition for d in deps}:
            note("criterion_facts_incomplete", r.requirement.contract_id)
    # Kahn ordering, stable across declaration/edge serialization order.
    incoming = {n: 0 for n in nodes}
    for targets in adjacency.values():
        for target in targets:
            incoming[target] += 1
    ready = sorted(n for n in nodes if incoming[n] == 0)
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for target in sorted(adjacency[n]):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    # One deterministic actual cycle witness is sufficient; never enumerate paths.
    cycles = []
    if len(order) != len(nodes):
        visited, active, stack = set(), set(), []

        def visit(n):
            visited.add(n)
            active.add(n)
            stack.append(n)
            for target in sorted(adjacency[n]):
                if target in active:
                    return tuple(stack[stack.index(target):] + [target])
                if target not in visited:
                    witness = visit(target)
                    if witness:
                        return witness
            stack.pop()
            active.remove(n)
            return None

        for n in sorted(nodes):
            if n not in visited:
                witness = visit(n)
                if witness:
                    cycles.append(witness)
                    break
        note("dependency_cycle")
    limited = len(findings) > 1024
    diagnostics = [Diagnostic(code=c, subjects=s) for c, s in sorted(findings)[:1023 if limited else 1024]]
    if limited:
        diagnostics.append(Diagnostic(code="diagnostic_bound_hit"))
    return ValidationReport(graph=g.identity(), node_count=len(nodes),
        edge_count=sum(len(v) for v in adjacency.values()), producer_count=len(g.producers),
        requirement_count=len(g.requirements), criterion_count=len(g.criteria), boundary_count=len(g.boundaries),
        topological_order=tuple(order), cycle_witnesses=tuple(cycles),
        diagnostics=tuple(diagnostics), witness_limit_reached=limited,
        structurally_valid=not findings)


def assess(graph: ValidationDAG, observations: tuple[ValidationObservation, ...], *,
           synthetic_authority: SyntheticAuthorityAssumption | None = None) -> tuple[ValidationAssessment, ...]:
    g = parse_contract(ValidationDAG, canonical_json(graph))
    if type(observations) is not tuple or len(observations) > 512:
        raise ValueError("at most 512 explicit observations")
    if sum(len(canonical_json(o).encode()) for o in observations) > MAX_JSON_BYTES:
        raise ValueError("observation batch exceeds transport bound")
    obs = tuple(parse_contract(ValidationObservation, canonical_json(o)) for o in observations)
    assumption = None if synthetic_authority is None else parse_contract(SyntheticAuthorityAssumption, canonical_json(synthetic_authority))
    report = verify(g)
    producers = {key(p.producer): p for p in g.producers}
    boundaries = {key(b.producer): b for b in g.boundaries}
    criteria = {key(c.criterion): c for c in g.criteria}
    result = {}

    def qualified(o):
        return bool(assumption and o.owner == assumption.owner and o.qualification == "SYNTHETIC_ASSUMPTION" and not o.historical)

    position = {n: i for i, n in enumerate(report.topological_order)}
    for r in sorted(g.requirements, key=lambda r: (position.get(token("R", r.requirement), 1000), key(r.requirement))):
        reasons, invalid, missing = set(), set(), set()
        if not report.structurally_valid:
            reasons.add("invalid_graph")
        c = criteria.get(key(r.criterion))
        selected = []
        available = valid = True
        failed = False
        for d in (d for d in g.dependencies if d.consumer == r.requirement and d.required):
            matches = [o for o in obs if o.evidence == d.evidence and o.decision_for is None]
            matches = list({canonical_json(o): o for o in matches}.values())
            p = producers.get(key(d.producer))
            boundary = boundaries.get(key(d.producer))
            if not p and not boundary:
                missing.add(d.producer)
                reasons.add("missing_internal_producer")
            elif p and p.qualification != "QUALIFIED":
                reasons.add("producer_" + p.qualification.lower())
            if not matches:
                available = valid = False
                reasons.add("human_boundary_unresolved" if boundary and boundary.kind == "HUMAN" else "external_boundary_unresolved" if boundary else "evidence_absent")
                invalid.add(d.dependency_id)
                continue
            if len(matches) != 1:
                reasons.add("evidence_conflict_requires_human_resolution")
                invalid.add(d.dependency_id)
                valid = False
                continue
            o = matches[0]
            selected.append(o)
            if o.context != r.context or o.producer != d.producer or o.source != d.expected_source:
                reasons.add("evidence_binding_mismatch")
            if not qualified(o):
                reasons.add("evidence_unqualified_or_historical")
            if o.status not in {"PRESENT", "PASSED", "FAILED"}:
                reasons.add("evidence_" + o.status.lower())
                valid = False
                if o.status in {"ABSENT", "UNAVAILABLE"}:
                    available = False
            if c and not c.human_decision_required and c.authority_class != "NONE" and o.authority_class != c.authority_class:
                reasons.add("evidence_authority_class_mismatch")
            if d.condition == "HUMAN_APPROVED" and not (boundary and boundary.kind == "HUMAN"):
                reasons.add("human_authority_boundary_missing")
            if boundary and boundary.kind == "HUMAN" and o.status == "PASSED" and (o.authority_class != "HUMAN" or o.human_decision != "APPROVED"):
                reasons.add("human_evidence_without_human_decision")
            if p and any(not result.get(key(ref), False) for ref in p.requires):
                reasons.add("upstream_requirement_unsatisfied")
            failed |= o.status == "FAILED"
            satisfied = (d.condition == "RECORDED" and o.status in {"PRESENT", "PASSED", "FAILED"}) or (d.condition == "PASSED" and o.status == "PASSED" and o.outcome == "PASSED") or (d.condition == "FAILED" and o.status == "FAILED" and o.outcome == "FAILED") or (d.condition == "HUMAN_APPROVED" and o.status == "PASSED" and o.human_decision == "APPROVED" and o.authority_class == "HUMAN")
            if not satisfied:
                reasons.add("dependency_condition_unsatisfied")
                invalid.add(d.dependency_id)
        prereqs = not reasons
        human = bool(c and c.human_decision_required)
        readiness = "BLOCKED"
        satisfied = False
        if prereqs and c:
            if human:
                readiness = "HUMAN_CLASSIFICATION_REQUIRED" if c.kind == "FAILURE_CLASSIFICATION" and failed else "HUMAN_DECISION_REQUIRED"
                decisions = [o for o in obs if o.decision_for == r.requirement]
                bound = tuple(sorted((o.identity() for o in selected), key=canonical_json))
                if len(decisions) == 1:
                    o = decisions[0]
                    b = boundaries.get(key(o.producer))
                    if qualified(o) and o.context == r.context and o.status == "PASSED" and o.human_decision == "APPROVED" and o.authority_class == "HUMAN" and b and b.kind == "HUMAN" and o.evidence == b.output and o.source == b.provenance and o.binds_evidence == bound:
                        readiness, satisfied = "HUMAN_DECISION_RECORDED", True
                    else:
                        reasons.add("human_decision_unqualified_rejected_or_mismatched")
                elif len(decisions) > 1:
                    reasons.add("conflicting_human_decisions")
            elif not failed and c.kind == "ALL_PASSED":
                readiness, satisfied = "READY_MACHINE", True
        result[key(r.requirement)] = satisfied
        conflict = any("conflict" in code for code in reasons)
        yield_value = ValidationAssessment(graph=report.graph, requirement=r.requirement,
            observed_evidence=tuple(sorted((o.identity() for o in obs if o.decision_for == r.requirement or (o.decision_for is None and o.evidence in r.expects)), key=canonical_json)),
            qualification_scope="ISOLATED_SYNTHETIC_TEST_ONLY" if assumption else "UNQUALIFIED",
            synthetic_assumption=assumption.provenance if assumption else None,
            prerequisite_state="SATISFIED" if prereqs else "BLOCKED",
            evidence_available=available, evidence_valid=valid and not reasons,
            acceptance_readiness=readiness, criterion_satisfied=satisfied,
            required_human_continuation=(human and not satisfied) or conflict,
            resolution_authority="HUMAN_OWNER" if (human and not satisfied) or conflict else "CONTRACT_OWNER" if not report.structurally_valid else "NONE",
            reason_codes=tuple(sorted(reasons)), missing_producers=tuple(sorted(missing, key=canonical_json)),
            invalid_dependencies=tuple(sorted(invalid)))
        result[("assessment", key(r.requirement))] = yield_value
    return tuple(result[("assessment", key(r.requirement))] for r in sorted(g.requirements, key=lambda r: key(r.requirement)))
