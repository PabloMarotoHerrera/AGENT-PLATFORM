"""Passive, synthetic first-slice graph and separately authored reference traces.

Source bytes/proofs are supplied by the caller. No paths, registry or runtime
imports. Abstract evidence views describe inspected semantics; they are not new
TicketSpec contracts, production adapters or a trusted qualification producer.
"""

from .admissibility_projection import binding_identity, operation_policy
from .handler_correspondence import BindingEvidence
from .harness.admissibility import AdmissionInput, ConsentStatus, PrerequisiteObservation, QualifiedEvaluation
from .harness.contracts import (
    ActorRef, AuthorityCurrentness, AuthorityReference, ContentRef, ContinuationKind,
    ContractRef, DecisionOutcome, Effect, ResultOutcome, Scope, StateDimension, StateSupport, WorkflowState,
)
from .harness.coverage import (
    ActionRelationship, AuthorityRequirement, Boundary, Correspondence, CoverageModel, EvidenceNode, Invalidation,
    OperationNode, Producer, ProducerKind, Remediation,
)
from .harness.observation import CheckStatus, Observation, ObservationStatus, SourceKind, SourceRef
from .harness.reference_model import ReferenceModel, ReferenceScenario, ReferenceState, ScenarioFacts, StructuralScenario
from .pre_review_catalog import product_catalog, product_operations


def _ref(name):
    return ContractRef(contract_id=name, version=1)


def _content(name, char="a"):
    return ContentRef(content_id=name, sha256=char * 64)


def _change(model, **updates):
    return type(model).model_validate({**model.model_dump(), **updates})


SYNTHETIC_ACTOR = ActorRef(actor_id="synthetic-operator")
SYNTHETIC_SCOPE = Scope(project_id="synthetic-project", workflow_id="synthetic-workflow", resource_ids=("SYN-1",))
SYNTHETIC_OWNER = _ref("synthetic-trusted-qualification-owner")


def build_first_slice(bindings: tuple[BindingEvidence, ...], provenance: ContentRef, *,
                      synthetic_assumptions: bool = False) -> CoverageModel:
    """All external/human roots default unavailable, never inferred from names."""
    bindings = tuple(BindingEvidence.model_validate(b) for b in bindings)
    provenance = ContentRef.model_validate(provenance)
    declarations = product_operations()
    proofs = {}
    for proof in bindings:
        key = proof.declaration.capability
        if key in proofs:
            raise ValueError("ambiguous supplied handler proof")
        proofs[key] = proof
    operations, evidence, boundaries = [], {}, {}
    by_id = {o.capability.capability.contract_id: o for o in declarations}

    def external(name, human=False, contract=None):
        ref = _ref(name) if isinstance(name, str) else name
        if ref in evidence:
            return ref
        kind = ProducerKind.HUMAN_PRODUCER if human else ProducerKind.EXTERNAL_PRODUCER
        boundary = _ref("boundary." + ref.contract_id)
        boundaries[boundary] = Boundary(boundary=boundary, kind=kind, provenance=(provenance,),
            assumed_available=synthetic_assumptions)
        evidence[ref] = EvidenceNode(evidence=ref, contract=contract or ref,
            role="HUMAN_DECISION" if human else "FACT", providers=(Producer(
                producer=_ref("external." + ref.contract_id), kind=kind, output=contract or ref,
                boundary=boundary, provenance=(provenance,)),))
        return ref

    def internal(name, producers, role="ARTIFACT"):
        ref = _ref(name)
        contract = by_id[producers[0]].capability.evidence_contract if len(producers) == 1 else _ref("har08.effective-material-authority")
        evidence[ref] = EvidenceNode(evidence=ref, contract=contract, role=role,
            providers=tuple(Producer(producer=_ref("produces." + p + "." + name), kind=ProducerKind.INTERNAL_PRODUCER,
                output=contract, operation=_ref(p), provenance=(provenance,),
                source_contract=by_id[p].capability.evidence_contract,
                projection=_ref("har08.effective-request-view") if len(producers) > 1 else None) for p in producers))
        return ref

    # Explicit source-derived relationships; no join on matching descriptor text.
    for name, producers, role in (
        ("command-plan", ("O01",), "INSPECTION"), ("command-result", ("O02",), "ARTIFACT"),
        ("approved-ticket-body", ("O03.ticket_spec",), "INSPECTION"),
        ("approved-validation-body", ("O03.validation_steps",), "INSPECTION"),
        ("material-defect-inspection", ("O04",), "INSPECTION"), ("revision-request", ("O05",), "ARTIFACT"),
        ("qualified-origin-inspection", ("O06",), "INSPECTION"), ("reconciled-request", ("O07",), "ARTIFACT"),
        ("material-authority", ("O05", "O07"), "ARTIFACT"), ("pending-publication", ("O08",), "ARTIFACT"),
        ("manual-inspection", ("P01",), "INSPECTION"), ("manual-passed", ("P02.passed",), "HUMAN_DECISION"),
        ("manual-failed", ("P02.failed",), "HUMAN_DECISION"), ("blocker-inspection", ("P03.workflow",), "INSPECTION"),
        ("review-inspection", ("P03.review",), "INSPECTION"), ("review-package", ("P03.prepare",), "ARTIFACT")):
        internal(name, producers, role)
    external_rows = {
        "approved-publication": True, "current-workpacket": False, "terminal-evidence": False,
        "candidate-or-zero-change": False, "preliminary-manual-evidence": True,
        "proven-missing-test-reference": False, "source-only-drift": False,
        "command-positive-qualification": False,
    }
    for name, human in external_rows.items():
        external(name, human)
    dependencies = {
        "O01": ("approved-publication", "current-workpacket", "terminal-evidence", "candidate-or-zero-change", "preliminary-manual-evidence"),
        "O02": ("command-plan", "current-workpacket", "terminal-evidence", "preliminary-manual-evidence"),
        "O03.ticket_spec": ("approved-publication", "current-workpacket"),
        "O03.validation_steps": ("approved-publication", "current-workpacket"),
        "O04": ("command-plan", "proven-missing-test-reference", "terminal-evidence"),
        "O05": ("material-defect-inspection", "terminal-evidence", "current-workpacket"),
        "O06": ("revision-request", "approved-validation-body", "source-only-drift", "terminal-evidence"),
        "O07": ("qualified-origin-inspection", "revision-request", "source-only-drift", "terminal-evidence"),
        "O08": ("material-authority", "current-workpacket"),
        "P01": ("terminal-evidence", "current-workpacket"),
        "P02.passed": ("manual-inspection", "command-result", "command-positive-qualification"),
        "P02.failed": ("manual-inspection",),
        "P03.workflow": (), "P03.review": ("terminal-evidence",),
        "P03.prepare": ("terminal-evidence", "command-result", "command-positive-qualification", "manual-passed"),
    }
    for op in declarations:
        name = op.capability.capability.contract_id
        policy = operation_policy(name, SYNTHETIC_ACTOR, SYNTHETIC_SCOPE)
        required = list(_ref(r) for r in dependencies[name])
        # These opaque refs name qualification results, not implemented producers.
        for prerequisite in policy.prerequisites:
            required.append(external(prerequisite))
        authority_requirements = []
        for kind in policy.required_authority_kinds:
            if kind == "manual_validation":
                authority_ref = _ref("manual-passed")
            elif kind == "material_revision_authority":
                authority_ref = _ref("material-authority")
            else:
                authority_ref = external("authority." + kind, human=kind.startswith(("human", "fresh")))
            required.append(authority_ref)
            authority_requirements.append(AuthorityRequirement(kind=kind, evidence=authority_ref,
                human=kind == policy.consent_kind))
        proof = proofs.get(op.capability.capability)
        if proof and proof.declaration != op.handler:
            raise ValueError("handler declaration mismatch")
        correspondence = Correspondence(capability=op.capability.capability,
            adapter=op.capability.execution_adapter, proof=binding_identity(proof), source=proof.source,
            status=proof.status.value) if proof else None
        kinds = ((ContinuationKind.OBSERVATION, ContinuationKind.SAFE_STOP) if op.capability.effect == Effect.OBSERVE
            else (ContinuationKind.EXECUTABLE_CAPABILITY, ContinuationKind.HUMAN_DECISION, ContinuationKind.SAFE_STOP))
        operations.append(OperationNode(capability=op.capability.capability, transition=op.transition.transition,
            policy=policy, correspondence=correspondence, requires=tuple(sorted(set(required), key=str)), continuation_kinds=kinds,
            authority_requirements=tuple(authority_requirements)))
    mapped = {"O02": "VALIDATE_SYN_1_COMMANDS", "O05": "REQUEST_SYN_1_POST_EXECUTION_MATERIAL_REVISION",
        "O07": "RECONCILE_MATERIAL_REVISION_AUTHORITY", "O08": "REVISE_SYN_1", "P03.prepare": "PREPARE_SYN_1_REVIEW"}
    actions = tuple(ActionRelationship(action=_ref(mapped.get(o.capability.contract_id, "unmapped." + o.capability.contract_id)),
        mapping="MAPPED" if o.capability.contract_id in mapped else "UNMAPPED", capability=o.capability,
        kind=ContinuationKind.EXECUTABLE_CAPABILITY if o.capability.contract_id in mapped else
            ContinuationKind.OBSERVATION if o.policy.effect == Effect.OBSERVE else ContinuationKind.HUMAN_DECISION,
        invocable=o.capability.contract_id in mapped,
        correspondence=o.correspondence.proof if o.capability.contract_id in mapped and o.correspondence else None)
        for o in operations)
    actions += tuple(ActionRelationship(action=_ref(name), mapping="MAPPED", capability=None,
        kind=kind, invocable=False) for name, kind in (
            ("RESOLVE_SYN-1_EXECUTION_AUTHORITY", ContinuationKind.SAFE_STOP),
            ("RESOLVE_SYN-1_REVIEW_BLOCKER", ContinuationKind.EXTERNAL_REMEDIATION)))
    return CoverageModel(model=_ref("pepper-first-slice-reference"), catalog=product_catalog(),
        catalog_content=product_catalog().content_identity(), operations=tuple(operations), evidence=tuple(evidence.values()),
        boundaries=tuple(boundaries.values()), actions=actions, permitted_effects=(Effect.OBSERVE, Effect.WRITE_ARTIFACT),
        invalidations=(Invalidation(event=_ref("revision-or-source-change"), evidence=tuple(_ref(r) for r in
            ("command-result", "manual-passed", "revision-request", "reconciled-request", "approved-ticket-body", "approved-validation-body"))),),
        remediation=tuple(Remediation(capability=o.capability, policy=by_id[o.capability.contract_id].capability.recovery_policy,
            kind=ContinuationKind.EXTERNAL_REMEDIATION, provenance=provenance) for o in operations),
        assumptions=("abstract_result_views_not_runtime_schemas", "final_dependent_manual_item_only",
            "legacy_guard_results_require_future_trusted_owner", "single_local_writer", "no_live_availability_claim"))


def synthetic_facts(operation: OperationNode, model: CoverageModel) -> ScenarioFacts:
    """Synthetic owner assumptions only. Does not qualify any real authority."""
    values = {"publication": "approved", "execution": "terminal_inactive", "validation": "passed",
        "review": "ready", "completion": "terminal_bound"}
    state = WorkflowState(**{key: StateDimension(definition=_ref("pepper." + key), value=value,
        support=StateSupport.SUPPORTED) for key, value in values.items()}, authority_currentness=AuthorityCurrentness.CURRENT)
    policy = operation.policy
    authorities = tuple(AuthorityReference(authority_id="synthetic." + k, kind=k, issuer=SYNTHETIC_ACTOR,
        subject=SYNTHETIC_ACTOR, scope=SYNTHETIC_SCOPE, policy=policy.policy, record=_content("record." + k),
        dependencies=(_content("synthetic-ticket-spec"), _content("synthetic-workpacket")),
        currentness=AuthorityCurrentness.CURRENT) for k in policy.required_authority_kinds)
    prereqs = tuple(PrerequisiteObservation(requirement=r, observation=Observation(
        source=SourceRef(source_id=r.contract_id, kind=SourceKind.EVIDENCE, format=_ref("synthetic-guard-result")),
        scope=SYNTHETIC_SCOPE, actor=SYNTHETIC_ACTOR, status=ObservationStatus.PRESENT, reason_code="synthetic_positive_result",
        source_content=_content(r.contract_id), integrity=CheckStatus.VERIFIED, structure=CheckStatus.VERIFIED,
        binding=CheckStatus.VERIFIED, consistency="STABLE_CAPTURE", completeness="BOUND_SOURCE_ONLY")) for r in policy.prerequisites)
    return ScenarioFacts(actor=SYNTHETIC_ACTOR, scope=SYNTHETIC_SCOPE, state=state, authorities=authorities,
        prerequisites=prereqs, authority_version="synthetic-v1", source_version=_content("synthetic-source-v1"),
        effect=policy.effect, handler_evidence=operation.correspondence.proof
            if operation.correspondence and operation.correspondence.status == "VERIFIED" else None,
        consent=ConsentStatus.GRANTED, catalog_content=model.catalog_content)


def _admission(facts, operation, model):
    return AdmissionInput.model_validate({**facts.model_dump(exclude={"policy_override"}), "catalog": model.catalog,
        "capability": model.catalog.resolve_capability(operation.capability).capability,
        "transition": model.catalog.resolve_transition(operation.transition).transition,
        "policy": facts.policy_override or operation.policy})


def _qualification(facts, operation, model):
    value = _admission(facts, operation, model)
    return QualifiedEvaluation(issuer=SYNTHETIC_OWNER, input=value.content_identity(),
        authority_ids=tuple(a.authority_id for a in facts.authorities),
        prerequisites=tuple(p.requirement for p in facts.prerequisites), handler_evidence=facts.handler_evidence)


def build_synthetic_reference_model(coverage: CoverageModel) -> ReferenceModel:
    """Separately authored case expectations; never derived from evaluate()."""
    coverage = CoverageModel.model_validate(coverage)
    cases = []
    operations = {o.capability.contract_id: o for o in coverage.operations}

    def add(case_id, operation_id, expected, mutation=None, *, evidence="AVAILABLE", origin=True,
            material="NONE", successor=None, result=ResultOutcome.SUCCESS, stale_qualification=False, qualified=True,
            active_predecessor=None, successor_rejected=False):
        operation = operations[operation_id]
        facts = synthetic_facts(operation, coverage)
        previous = _qualification(facts, operation, coverage)
        if mutation:
            facts = mutation(facts)
        before = ReferenceState(workflow=facts.state, consent=facts.consent, evidence=evidence,
            correspondence=facts.handler_evidence is not None, material=material, qualified_origin=origin,
            source_version=facts.source_version, authority_version=facts.authority_version, result=result,
            selected_ticket="SYN-1", active_predecessor=active_predecessor, successor_rejected=successor_rejected)
        target = successor(before) if successor else before
        cases.append(ReferenceScenario(scenario_id=case_id, category=case_id, operation=operation.capability,
            facts=facts, before=before, successor=target, expected=(expected,), trusted_issuer=SYNTHETIC_OWNER,
            qualification=(previous if stale_qualification else _qualification(facts, operation, coverage)) if qualified else None,
            assumptions=("synthetic_trusted_owner_only", "qualified_guard_result_assumption")))

    def workflow(facts, dimension, value):
        return _change(facts, state=_change(facts.state, **{dimension: _change(getattr(facts.state, dimension), value=value)}))

    def absent(facts):
        return _change(facts, prerequisites=facts.prerequisites[1:])

    def invalid(facts):
        p = facts.prerequisites[0]
        observation = Observation(source=p.observation.source, scope=facts.scope, actor=facts.actor,
            status=ObservationStatus.INVALID, reason_code="synthetic_invalid_evidence")
        return _change(facts, prerequisites=(_change(p, observation=observation),) + facts.prerequisites[1:])

    def authority(facts, status):
        first = _change(facts.authorities[0], currentness=status,
            superseded_by=_content("synthetic-successor") if status == AuthorityCurrentness.SUPERSEDED else None)
        return _change(facts, authorities=(first,) + facts.authorities[1:],
            state=_change(facts.state, authority_currentness=status))

    # Explicit abstract transition table: inspection is a self-transition; request,
    # reconciliation and revision do not create consent, approval or execution.
    successors = {
        "O02": lambda s: _change(s, command_passed=True),
        "O05": lambda s: _change(s, material="REQUESTED", consent=ConsentStatus.MISSING),
        "O07": lambda s: _change(s, material="RECONCILED", consent=ConsentStatus.MISSING),
        "O08": lambda s: _change(s, material="REVISION_PENDING", consent=ConsentStatus.MISSING, evidence="INVALIDATED",
            source_version=_content("synthetic-revised-source", "b"), authority_version="synthetic-pending-revision",
            workflow=_change(s.workflow, publication=_change(s.workflow.publication, value="pending_approval"),
                execution=_change(s.workflow.execution, value="not_started"), validation=_change(s.workflow.validation, value="pending"),
                review=_change(s.workflow.review, value="not_ready"), completion=_change(s.workflow.completion, value="pending"),
                authority_currentness=AuthorityCurrentness.UNVERIFIED)),
        "P02.passed": lambda s: _change(s, manual_passed=True),
        "P02.failed": lambda s: _change(s, workflow=_change(s.workflow, validation=_change(s.workflow.validation, value="failed"))),
        "P03.prepare": lambda s: _change(s, workflow=_change(s.workflow, review=_change(s.workflow.review, value="pending_human_acceptance"))),
    }
    for operation_id in sorted(operations):
        add("valid." + operation_id, operation_id, DecisionOutcome.ALLOW, successor=successors.get(operation_id))
    for status, expected in ((ConsentStatus.MISSING, DecisionOutcome.WAIT), (ConsentStatus.PENDING, DecisionOutcome.WAIT),
            (ConsentStatus.DENIED, DecisionOutcome.DENY), (ConsentStatus.CONFLICT, DecisionOutcome.SAFE_STOP)):
        add("command-consent." + status.value, "O02", expected, lambda f, s=status: _change(f, consent=s))
    for status in (AuthorityCurrentness.HISTORICAL, AuthorityCurrentness.SUPERSEDED,
            AuthorityCurrentness.UNVERIFIED, AuthorityCurrentness.CONFLICT, AuthorityCurrentness.UNSUPPORTED):
        add("authority." + status.value, "O07", DecisionOutcome.SAFE_STOP, lambda f, s=status: authority(f, s))
    for case, op, expected, mutation, evidence in (
        ("command-prerequisite-missing", "O02", DecisionOutcome.WAIT, absent, "MISSING"),
        ("command-evidence-invalid", "O02", DecisionOutcome.SAFE_STOP, invalid, "INVALID"),
        ("artifact-section-missing", "O03.ticket_spec", DecisionOutcome.WAIT, absent, "MISSING"),
        ("artifact-partial-not-approval", "O03.validation_steps", DecisionOutcome.WAIT, absent, "MISSING"),
        ("artifact-version-mismatch", "O03.ticket_spec", DecisionOutcome.SAFE_STOP, lambda f: authority(f, AuthorityCurrentness.HISTORICAL), "AVAILABLE"),
        ("artifact-rejected-generation", "O03.ticket_spec", DecisionOutcome.WAIT, lambda f: workflow(f, "publication", "rejected"), "AVAILABLE"),
        ("revision-human-decision", "O05", DecisionOutcome.WAIT, lambda f: _change(f, consent=ConsentStatus.PENDING), "AVAILABLE"),
        ("revision-material-evidence-missing", "O05", DecisionOutcome.WAIT, absent, "MISSING"),
        ("revision-stale-workpacket", "O05", DecisionOutcome.SAFE_STOP, lambda f: authority(f, AuthorityCurrentness.HISTORICAL), "AVAILABLE"),
        ("reconciliation-contradictory-chain", "O07", DecisionOutcome.SAFE_STOP, lambda f: authority(f, AuthorityCurrentness.CONFLICT), "AVAILABLE"),
        ("manual-pending", "P03.prepare", DecisionOutcome.WAIT, lambda f: workflow(f, "validation", "pending"), "AVAILABLE"),
        ("manual-failed", "P03.prepare", DecisionOutcome.WAIT, lambda f: workflow(f, "validation", "failed"), "AVAILABLE"),
        ("review-active-execution", "P03.prepare", DecisionOutcome.WAIT, lambda f: workflow(f, "execution", "active"), "AVAILABLE"),
        ("review-missing-attestation", "P03.prepare", DecisionOutcome.WAIT, absent, "MISSING"),
        ("evidence-invalidated", "P03.prepare", DecisionOutcome.WAIT, absent, "INVALIDATED"),
        ("missing-executor", "O02", DecisionOutcome.SAFE_STOP, lambda f: _change(f, handler_evidence=None), "AVAILABLE"),
        ("stale-catalog", "O02", DecisionOutcome.SAFE_STOP, lambda f: _change(f, catalog_content=_content("stale-catalog")), "AVAILABLE"),
        ("unsupported-evidence", "O02", DecisionOutcome.SAFE_STOP, invalid, "INVALID"),
    ):
        add(case, op, expected, mutation, evidence=evidence)
    add("unqualified-origin", "O07", DecisionOutcome.SAFE_STOP, origin=False, qualified=False)
    for case, op in (("artifact-source-drift", "O03.ticket_spec"), ("stale-command-authorization", "O02"),
            ("duplicate-stale-request", "O05"), ("old-allow-after-version-change", "O02")):
        add(case, op, DecisionOutcome.SAFE_STOP, lambda f: _change(f, source_version=_content("synthetic-source-v2", "b")),
            stale_qualification=True)
    for dependency in ("synthetic-ticket-spec", "synthetic-workpacket"):
        def altered_binding(facts, name=dependency):
            first = facts.authorities[0]
            altered = _change(first, dependencies=tuple(_content(name, "b") if d.content_id == name else d for d in first.dependencies))
            return _change(facts, authorities=(altered,) + facts.authorities[1:])
        add("artifact-binding." + dependency, "O03.ticket_spec", DecisionOutcome.SAFE_STOP,
            altered_binding, stale_qualification=True)
    add("duplicate-request-authority", "O05", DecisionOutcome.SAFE_STOP, lambda f: _change(f,
        authorities=f.authorities + (_change(f.authorities[0], authority_id="synthetic-duplicate", record=_content("other-record", "b")),)))
    add("failed-command-not-attestation", "O02", DecisionOutcome.ALLOW, result=ResultOutcome.FAILURE)
    add("unknown-command-not-success", "O02", DecisionOutcome.ALLOW, result=ResultOutcome.UNKNOWN)
    add("active-context-rejected-successor", "P03.workflow", DecisionOutcome.ALLOW,
        lambda f: workflow(f, "execution", "active"), active_predecessor="SYN-1", successor_rejected=True)
    return ReferenceModel(model=_ref("pepper-bounded-synthetic-reference"), coverage=coverage, scenarios=tuple(cases),
        structural=(StructuralScenario(scenario_id="graph.missing-executor", mutation="MISSING_EXECUTOR", subject=_ref("O02"),
            expected_code="executor_correspondence_missing"),
        StructuralScenario(scenario_id="graph.unreachable-producer", mutation="BLOCK_BOUNDARY",
            subject=_ref("boundary.preliminary-manual-evidence"), expected_code="internal_producer_unreachable"),
        StructuralScenario(scenario_id="graph.prerequisite-cycle", mutation="ADD_REQUIREMENT", subject=_ref("O01"),
            requirement=_ref("command-result"), expected_code="prerequisite_cycle")))
