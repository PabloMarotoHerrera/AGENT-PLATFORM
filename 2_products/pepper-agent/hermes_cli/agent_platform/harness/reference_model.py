"""Finite reference traces and independent safety assertions, never an executor.

Expected outcomes and successor states are authored table data, not answers
computed by HAR-07. HAR-07 is the sole admission evaluator. Breadth-first graph
exploration is over explicitly supplied synthetic roots/edges only.
"""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .admissibility import AdmissionInput, AdmissionPolicy, ConsentStatus, PrerequisiteObservation, QualifiedEvaluation, evaluate
from .contracts import (
    ActorRef, AuthorityCurrentness, AuthorityReference, ContentRef, ContinuationKind, ContractRef, DecisionOutcome,
    Effect, Identifier, ResultOutcome, Scope, WorkflowState, _Contract,
)
from .coverage import CoverageModel, CoverageReport, ExplorationBounds, verify_coverage
from .validation import canonical_json, parse_contract, sha256_bytes


def _identity(value: _Contract, name: str) -> ContentRef:
    return ContentRef(content_id=name, sha256=sha256_bytes(name.encode() + b"\0" + canonical_json(value).encode()))


class ReferenceState(_Contract):
    workflow: WorkflowState
    consent: ConsentStatus
    evidence: Literal["AVAILABLE", "MISSING", "INVALID", "INVALIDATED", "UNKNOWN"]
    correspondence: bool
    material: Literal["NONE", "REQUESTED", "RECONCILED", "REVISION_PENDING"] = "NONE"
    qualified_origin: bool = True
    source_version: ContentRef
    authority_version: Identifier
    successor_approved: bool = False
    authority_created: bool = False
    manual_passed: bool = False
    command_passed: bool = False
    result: ResultOutcome = ResultOutcome.SUCCESS
    active_predecessor: Identifier | None = None
    selected_ticket: Identifier | None = None
    successor_rejected: bool = False

    def content_identity(self) -> ContentRef:
        return _identity(ReferenceState.model_validate(self), "har08-reference-state")


class ScenarioFacts(_Contract):
    """Compact fixture data; materialized into the existing AdmissionInput.

    Catalog/descriptors/policy are shared by exact model operation identity.
    No alternative admission semantics live in this envelope.
    """
    actor: ActorRef
    scope: Scope
    state: WorkflowState
    authorities: Annotated[tuple[AuthorityReference, ...], Field(max_length=32)]
    prerequisites: Annotated[tuple[PrerequisiteObservation, ...], Field(max_length=32)]
    authority_version: Identifier
    source_version: ContentRef
    effect: Effect
    handler_evidence: ContentRef | None
    consent: ConsentStatus
    catalog_content: ContentRef
    policy_override: AdmissionPolicy | None = None


class ReferenceScenario(_Contract):
    scenario_id: Identifier
    category: Identifier
    operation: ContractRef
    facts: ScenarioFacts
    trusted_issuer: ContractRef | None
    qualification: QualifiedEvaluation | None
    before: ReferenceState
    successor: ReferenceState
    expected: Annotated[tuple[DecisionOutcome, ...], Field(min_length=1, max_length=4)]
    assumptions: Annotated[tuple[Identifier, ...], Field(max_length=8)] = ()


class StructuralScenario(_Contract):
    scenario_id: Identifier
    mutation: Literal["MISSING_EXECUTOR", "BLOCK_BOUNDARY", "ADD_REQUIREMENT"]
    subject: ContractRef
    requirement: ContractRef | None = None
    expected_code: Identifier


class ReferenceModel(_Contract):
    model: ContractRef
    coverage: CoverageModel
    scenarios: Annotated[tuple[ReferenceScenario, ...], Field(max_length=1024)]
    structural: Annotated[tuple[StructuralScenario, ...], Field(max_length=32)] = ()

    @model_validator(mode="after")
    def _order(self):
        if len({s.scenario_id for s in self.scenarios}) != len(self.scenarios):
            raise ValueError("duplicate scenario identity")
        if len({s.scenario_id for s in (*self.scenarios, *self.structural)}) != len(self.scenarios) + len(self.structural):
            raise ValueError("duplicate structural scenario identity")
        if any(s.operation not in {o.capability for o in self.coverage.operations} for s in self.scenarios):
            raise ValueError("scenario operation not declared")
        object.__setattr__(self, "scenarios", tuple(sorted(self.scenarios, key=lambda s: s.scenario_id)))
        object.__setattr__(self, "structural", tuple(sorted(self.structural, key=lambda s: s.scenario_id)))
        return self

    def content_identity(self) -> ContentRef:
        return _identity(ReferenceModel.model_validate(self), "har08-reference-model")


def materialize_admission(model: ReferenceModel, scenario: ReferenceScenario) -> AdmissionInput:
    """Exact lookup and data assembly only; evaluate remains the only evaluator."""
    operation = next(o for o in model.coverage.operations if o.capability == scenario.operation)
    cap = model.coverage.catalog.resolve_capability(operation.capability).capability
    transition = model.coverage.catalog.resolve_transition(operation.transition).transition
    facts = ScenarioFacts.model_validate(scenario.facts)
    values = facts.model_dump(exclude={"policy_override"})
    return AdmissionInput.model_validate({**values, "catalog": model.coverage.catalog,
        "capability": cap, "transition": transition, "policy": facts.policy_override or operation.policy})


class GeneratedScenarios(_Contract):
    model: ContentRef
    seed: Annotated[int, Field(ge=0, le=65535)]
    scenarios: Annotated[tuple[ReferenceScenario, ...], Field(max_length=1024)]
    declared_count: int
    incomplete: bool
    structural: Annotated[tuple[StructuralScenario, ...], Field(max_length=32)] = ()


def generate_scenarios(model: ReferenceModel, bounds: ExplorationBounds = ExplorationBounds(),
                       seed: int = 0) -> GeneratedScenarios:
    model = ReferenceModel.model_validate(model)
    model = parse_contract(ReferenceModel, canonical_json(model))
    bounds = ExplorationBounds.model_validate(bounds)
    # A deterministic rotation is useful for checking sensitivity to order; no
    # pseudorandom dependency or hidden exhaustive Cartesian-product claim.
    cases = model.scenarios
    if type(seed) is not int or not 0 <= seed <= 65535:
        raise ValueError("unsupported scenario seed")
    if cases:
        offset = seed % len(cases)
        cases = cases[offset:] + cases[:offset]
    selected = cases[:bounds.scenarios]
    structural = model.structural[:max(0, bounds.scenarios - len(selected))]
    count = len(cases) + len(model.structural)
    return GeneratedScenarios(model=model.content_identity(), seed=seed, scenarios=selected, structural=structural,
        declared_count=count, incomplete=count > bounds.scenarios)


class NegativeWitness(_Contract):
    scenario_id: Identifier
    property: Identifier
    before: ContentRef
    actual: DecisionOutcome


class ScenarioResult(_Contract):
    scenario_id: Identifier
    category: Identifier
    operation: ContractRef
    outcome: DecisionOutcome
    expected: Annotated[tuple[DecisionOutcome, ...], Field(min_length=1, max_length=4)]
    before: ContentRef
    after: ContentRef
    evaluation: ContentRef
    reason_codes: Annotated[tuple[Identifier, ...], Field(max_length=64)]


class StructuralResult(_Contract):
    scenario_id: Identifier
    model: ContentRef
    expected_code: Identifier
    actual_codes: Annotated[tuple[Identifier, ...], Field(max_length=256)]
    matched: bool


class ModelCheckReport(_Contract):
    model: ContentRef
    coverage: CoverageReport
    generated_scenarios: int
    declared_scenarios: int
    results: Annotated[tuple[ScenarioResult, ...], Field(max_length=1024)]
    states: Annotated[tuple[ContentRef, ...], Field(max_length=4096)]
    transitions: Annotated[tuple[tuple[ContentRef, ContentRef, Identifier], ...], Field(max_length=2048)]
    explored_states: int
    explored_transitions: int
    explored_depth: int
    witnesses: Annotated[tuple[NegativeWitness, ...], Field(max_length=1024)]
    violations: Annotated[tuple[NegativeWitness, ...], Field(max_length=1024)]
    bounds: ExplorationBounds
    bound_hits: Annotated[tuple[Identifier, ...], Field(max_length=8)]
    assumptions: Annotated[tuple[Identifier, ...], Field(max_length=128)]
    unsupported_semantics: tuple[Identifier, ...] = ("live_authority", "effect_execution", "concurrency", "unmodeled_environment")
    complete: bool
    structural_results: Annotated[tuple[StructuralResult, ...], Field(max_length=32)] = ()
    unique_negative_witnesses: int
    passed: bool

    def content_identity(self) -> ContentRef:
        return _identity(ModelCheckReport.model_validate(self), "har08-model-check-report")


def check_reference(model: ReferenceModel, bounds: ExplorationBounds = ExplorationBounds(), seed: int = 0) -> ModelCheckReport:
    model = ReferenceModel.model_validate(model)
    generated = generate_scenarios(model, bounds, seed)
    bounds = ExplorationBounds.model_validate(bounds)
    coverage = verify_coverage(model.coverage, bounds)
    results, witnesses, violations = [], [], []
    states, roots, edges = {}, set(), set()
    hits = set(coverage.bound_hits)
    if generated.incomplete:
        hits.add("scenarios")
    assumptions = set(model.coverage.assumptions)
    work = coverage.work_used
    if model.model.version != 1:
        hits.add("unsupported_model_version")
    for scenario in generated.scenarios:
        work += 1
        if work > bounds.work:
            hits.add("work")
            break
        value, before = materialize_admission(model, scenario), scenario.before
        result = evaluate(value, trusted_issuer=scenario.trusted_issuer, qualification=scenario.qualification)
        actual = result.decision.outcome
        after = scenario.successor if actual == DecisionOutcome.ALLOW else before
        before_id, after_id = before.content_identity(), after.content_identity()
        failures = []
        executable = any(c.kind == ContinuationKind.EXECUTABLE_CAPABILITY for c in result.continuations)
        # These independently stated invariants deliberately check abstract facts
        # even if a supplied policy/positive qualification was accidentally weak.
        if before.consent != ConsentStatus.GRANTED and executable:
            failures.append("missing_consent_executable")
        if value.policy.consent_kind and before.consent == ConsentStatus.DENIED and actual == DecisionOutcome.ALLOW:
            failures.append("denied_consent_allowed")
        if (any(a.currentness != AuthorityCurrentness.CURRENT for a in value.authorities)
                or before.workflow.authority_currentness != AuthorityCurrentness.CURRENT) and actual == DecisionOutcome.ALLOW:
            failures.append("noncurrent_authority_allowed")
        if before.evidence != "AVAILABLE" and actual == DecisionOutcome.ALLOW:
            failures.append("missing_or_invalidated_evidence_allowed")
        if not before.correspondence and executable:
            failures.append("handlerless_executable")
        if actual in (DecisionOutcome.WAIT, DecisionOutcome.SAFE_STOP, DecisionOutcome.DENY) and executable:
            failures.append("blocked_outcome_executable")
        if any(c.kind in (ContinuationKind.EXTERNAL_REMEDIATION, ContinuationKind.SAFE_STOP) and c.capability is not None
                for c in result.continuations):
            failures.append("diagnostic_became_tool")
        if scenario.operation.contract_id == "O07" and not before.qualified_origin and executable:
            failures.append("unqualified_reconciliation_executable")
        if scenario.operation.contract_id == "P03.prepare" and before.workflow.execution.value != "terminal_inactive" and executable:
            failures.append("active_execution_enabled_review")
        if scenario.operation.contract_id in ("O05", "O07", "O08") and (after.successor_approved or after.authority_created):
            failures.append("material_transition_created_authority")
        if before.active_predecessor and after.selected_ticket != before.active_predecessor:
            failures.append("active_predecessor_displaced")
        if scenario.qualification and scenario.qualification.input != value.content_identity() and actual == DecisionOutcome.ALLOW:
            failures.append("old_projection_reused_after_version_change")
        if before.result == ResultOutcome.UNKNOWN and (after.command_passed or after.manual_passed
                or after.workflow.completion.value in ("success", "completed")):
            failures.append("unknown_result_promoted")
        if before.result == ResultOutcome.FAILURE and (after.command_passed or after.manual_passed):
            failures.append("failed_command_became_attestation")
        if actual not in scenario.expected:
            failures.append("independent_expectation_mismatch")
        if before.workflow != value.state or before.consent != value.consent or before.source_version != value.source_version:
            failures.append("abstract_input_binding_mismatch")
        for code in sorted(set(failures)):
            violations.append(NegativeWitness(scenario_id=scenario.scenario_id, property=code, before=before_id, actual=actual))
        if actual != DecisionOutcome.ALLOW:
            witnesses.append(NegativeWitness(scenario_id=scenario.scenario_id, property=scenario.category,
                before=before_id, actual=actual))
        required_states = {before_id, after_id} - set(states)
        if len(states) + len(required_states) > bounds.states:
            hits.add("states")
            break
        states[before_id], states[after_id] = before, after
        roots.add(before_id)
        edges.add((before_id, after_id, scenario.scenario_id))
        assumptions.update(scenario.assumptions)
        results.append(ScenarioResult(scenario_id=scenario.scenario_id, category=scenario.category, operation=scenario.operation,
            outcome=actual, expected=scenario.expected, before=before_id, after=after_id, evaluation=result.input,
            reason_codes=tuple(r.code for r in result.reasons)))
    structural_results = []
    for scenario in generated.structural:
        if work >= bounds.work:
            hits.add("work")
            break
        operations = model.coverage.operations
        boundaries = model.coverage.boundaries
        if scenario.mutation in ("MISSING_EXECUTOR", "ADD_REQUIREMENT"):
            replaced = []
            for operation in operations:
                values = operation.model_dump()
                if operation.capability == scenario.subject:
                    if scenario.mutation == "MISSING_EXECUTOR":
                        values["correspondence"] = None
                    else:
                        if scenario.requirement is None:
                            raise ValueError("structural requirement missing")
                        values["requires"] = operation.requires + (scenario.requirement,)
                replaced.append(type(operation).model_validate(values))
            operations = tuple(replaced)
        else:
            boundaries = tuple(type(b).model_validate({**b.model_dump(), "assumed_available": False})
                if b.boundary == scenario.subject else b for b in boundaries)
        variant = CoverageModel.model_validate({**model.coverage.model_dump(), "operations": operations, "boundaries": boundaries})
        remaining = ExplorationBounds.model_validate({**bounds.model_dump(), "work": max(1, bounds.work - work)})
        report = verify_coverage(variant, remaining)
        work += report.work_used
        hits.update(report.bound_hits)
        codes = tuple(sorted({i.code for i in report.issues}))
        structural_results.append(StructuralResult(scenario_id=scenario.scenario_id, model=variant.content_identity(),
            expected_code=scenario.expected_code, actual_codes=codes, matched=scenario.expected_code in codes))
    # Bounded BFS independent of the monotone producer closure used above.
    queue = [(r, 0) for r in sorted(roots, key=str)]
    visited, traversed = set(), set()
    depth = 0
    while queue:
        state, distance = queue.pop(0)
        if state in visited:
            continue
        work += 1
        if work > bounds.work:
            hits.add("work")
            break
        visited.add(state)
        depth = max(depth, distance)
        for edge in sorted(edges, key=str):
            if edge[0] != state:
                continue
            if distance >= bounds.depth and edge[1] not in visited:
                hits.add("depth")
                continue
            traversed.add(edge)
            if edge[1] not in visited:
                queue.append((edge[1], distance + 1))
    if len(violations) > 1024 or len(witnesses) > 1024:
        hits.add("witnesses")
    return ModelCheckReport(model=model.content_identity(), coverage=coverage,
        generated_scenarios=len(results) + len(structural_results), declared_scenarios=generated.declared_count, results=tuple(results),
        states=tuple(sorted(visited, key=str)), transitions=tuple(sorted(traversed, key=str)),
        explored_states=len(visited), explored_transitions=len(traversed), explored_depth=depth,
        witnesses=tuple(sorted(witnesses, key=lambda w: (w.scenario_id, w.property)))[:1024],
        violations=tuple(sorted(violations, key=lambda w: (w.scenario_id, w.property)))[:1024], bounds=bounds,
        bound_hits=tuple(sorted(hits)), assumptions=tuple(sorted(assumptions)), complete=not hits,
        structural_results=tuple(structural_results), unique_negative_witnesses=len(witnesses) + sum(r.matched for r in structural_results),
        passed=not hits and not violations and all(r.matched for r in structural_results)
            and coverage.classification in ("STRUCTURALLY_COVERED", "COVERED_WITH_EXTERNAL_ASSUMPTIONS"))
