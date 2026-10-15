"""HAR-04 structural invariants, without activating any workflow or executor."""

import json

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness import (
    ActorRef, AdmissibilityDecision, AuthorityCurrentness, AuthorityReference,
    CapabilityDescriptor, ContentRef, Continuation, ContinuationKind, ContractRef,
    DecisionOutcome, Effect, EffectStatus, EvidenceReference, ExecutionRequest,
    ExecutionResult, ResultOutcome, Scope, StateDimension, StateSupport,
    TransitionDescriptor, WorkflowProjection, WorkflowState, canonical_json,
    parse_contract, sha256_bytes, verify_content_digest,
)


def examples():
    ref = ContractRef(contract_id="contract", version=1)
    content = ContentRef(content_id="input", sha256=sha256_bytes(b"input"))
    actor = ActorRef(actor_id="operator")
    scope = Scope(project_id="project", workflow_id="workflow", resource_ids=("resource",))
    capability = CapabilityDescriptor(capability=ref, input_schema=ref, output_schema=ref,
        effect=Effect.COMPUTE, required_authority_kinds=("approval",),
        evidence_contract=ref, execution_adapter=ref)
    transition = TransitionDescriptor(transition=ref, source_requirement=ref, capability=ref,
        prerequisites=(ref,), required_authority_kinds=("approval",), effect=Effect.COMPUTE,
        target_rule=ref, failure_code="failed", conflict_code="conflict", continuation_rule=ref)
    dimension = StateDimension(definition=ref, value="unknown", support=StateSupport.UNKNOWN)
    state = WorkflowState(publication=dimension, execution=dimension, validation=dimension,
        review=dimension, completion=dimension, authority_currentness=AuthorityCurrentness.UNVERIFIED)
    continuation = Continuation(continuation_id="RESOLVE_diagnostic", scope=scope, actor=actor,
        kind=ContinuationKind.EXTERNAL_REMEDIATION, reason_code="missing_authority", policy=ref)
    authority = AuthorityReference(authority_id="authority", kind="approval", issuer=actor,
        subject=actor, scope=scope, policy=ref, record=content, dependencies=(content,),
        currentness=AuthorityCurrentness.CURRENT)
    decision = AdmissibilityDecision(decision_id="decision", scope=scope, actor=actor,
        capability=ref, outcome=DecisionOutcome.ALLOW, reason_code="observed", policy=ref,
        required_authority_kinds=("approval",), current_authorities=(authority,),
        expected_authority_version="authority-v1", prerequisites=(content,), effect=Effect.COMPUTE)
    request = ExecutionRequest(operation_id="operation", capability=ref, scope=scope, actor=actor,
        authorities=(authority,), input=content, implementation=content, effect=Effect.COMPUTE,
        admissibility_observation=content, expected_authority_version="authority-v1")
    evidence = EvidenceReference(evidence_id="evidence", evidence_type="regression", sha256=content.sha256,
        producer_operation_id="operation", producer_capability=ref, producer_actor=actor,
        scope=scope, input=content, storage_locator="opaque:artifact", integrity="unverified",
        retention="unspecified")
    result = ExecutionResult(operation_id="operation", capability=ref, scope=scope, actor=actor,
        request=content, input=content, outcome=ResultOutcome.SUCCESS, effect_status=EffectStatus.CONFIRMED,
        reason_code="finished", output=content, evidence=(evidence,))
    projection = WorkflowProjection(projection_id="projection", scope=scope, actor=actor,
        observed_authority_version="authority-v1", observed_state_version="state-v1", state=state,
        continuations=(continuation,), pending_human_decisions=(), wait_conditions=(ref,),
        safe_stops=(), diagnostics=("missing_authority",))
    return (ref, content, actor, scope, capability, transition, dimension, state,
            continuation, authority, decision, request, evidence, result, projection)


EXAMPLES = examples()


def changed(model, **updates):
    """Exercise validated construction, not Pydantic's unchecked copy shortcut."""
    return type(model).model_validate({**dict(model), **updates})


@pytest.mark.parametrize("model", EXAMPLES, ids=lambda m: type(m).__name__)
def test_every_contract_roundtrip_is_strict_immutable_and_deterministic(model):
    encoded = canonical_json(model)
    assert parse_contract(type(model), encoded) == model
    assert canonical_json(parse_contract(type(model), encoded.encode())) == encoded
    reordered = json.dumps(dict(reversed(list(json.loads(encoded).items()))))
    assert canonical_json(parse_contract(type(model), reordered)) == encoded
    with pytest.raises(ValidationError):
        model.schema_version = 2
    for version in (2, 0, True, "1", 1.0):
        with pytest.raises(ValidationError):
            changed(model, schema_version=version)
    with pytest.raises(ValidationError):
        changed(model, execution_authorized=True)
    required = next(name for name, field in type(model).model_fields.items() if field.is_required())
    fields = dict(model)
    del fields[required]
    with pytest.raises(ValidationError):
        type(model).model_validate(fields)
    with pytest.raises(ValidationError):
        changed(model, **{required: lambda: True})


@pytest.mark.parametrize("identifier", ("", "*", "../file", "x" * 129, "f()", "x\n", " operator"))
def test_identifier_bounds_and_no_executable_expressions(identifier):
    with pytest.raises(ValidationError):
        ContractRef(contract_id=identifier, version=1)


@pytest.mark.parametrize("version", (True, "1", 0, 65536))
def test_reference_version_bounds(version):
    with pytest.raises(ValidationError):
        ContractRef(contract_id="contract", version=version)


def test_reference_versions_are_opaque_and_state_support_is_explicit():
    dimension = changed(EXAMPLES[6], definition=ContractRef(contract_id="state", version=12),
                        support=StateSupport.UNSUPPORTED)
    assert parse_contract(StateDimension, canonical_json(dimension)).support == StateSupport.UNSUPPORTED
    # No coupling execution success to review, publication or completion.
    state = EXAMPLES[7]
    assert changed(state, execution=changed(dimension, value="success")).review == state.review


@pytest.mark.parametrize("kind", list(ContinuationKind))
def test_typed_continuations_do_not_supply_authority(kind):
    ref = EXAMPLES[0]
    data = dict(EXAMPLES[8])
    data.update(kind=kind, capability=ref if kind == ContinuationKind.EXECUTABLE_CAPABILITY else None,
                decision_target=ref if kind == ContinuationKind.HUMAN_DECISION else None)
    offer = Continuation(**data)
    assert parse_contract(Continuation, canonical_json(offer)) == offer
    with pytest.raises(ValidationError):
        changed(EXAMPLES[11], authorities=(offer,))
    for field in ("handler", "callback", "execute", "consent"):
        with pytest.raises(ValidationError):
            changed(offer, **{field: "approved"})


def test_continuations_fail_closed_for_conflicting_kinds():
    offer, ref = EXAMPLES[8], EXAMPLES[0]
    with pytest.raises(ValidationError):
        changed(offer, kind=ContinuationKind.EXECUTABLE_CAPABILITY)
    for kind in (ContinuationKind.EXTERNAL_REMEDIATION, ContinuationKind.SAFE_STOP,
                 ContinuationKind.HUMAN_DECISION, ContinuationKind.OBSERVATION):
        with pytest.raises(ValidationError):
            changed(offer, kind=kind, capability=ref)
    with pytest.raises(ValidationError):
        changed(offer, kind=ContinuationKind.HUMAN_DECISION)
    with pytest.raises(ValidationError):
        changed(offer, decision_target=ref)


def test_descriptor_and_projection_cannot_stand_in_for_authority_or_request():
    for model in (EXAMPLES[4], EXAMPLES[-1], EXAMPLES[10]):
        with pytest.raises(ValidationError):
            parse_contract(ExecutionRequest, canonical_json(model))
        with pytest.raises(ValidationError):
            changed(EXAMPLES[11], authorities=(model,))
    assert EXAMPLES[-1].continuations[0].capability is None
    for model in (EXAMPLES[-1], EXAMPLES[10]):
        with pytest.raises(ValidationError):
            changed(model, observational=False)


@pytest.mark.parametrize("field,value", [("project_id", "other"), ("workflow_id", "other"),
                                        ("resource_ids", ("other",)),
                                        ("resource_ids", ("resource", "other"))])
def test_scope_cannot_be_widened_or_moved(field, value):
    scope = changed(EXAMPLES[3], **{field: value})
    for model in (EXAMPLES[10], EXAMPLES[11], EXAMPLES[13], EXAMPLES[14]):
        with pytest.raises(ValidationError):
            changed(model, scope=scope)


def test_actor_bindings_and_resource_set_normalization():
    for model in (EXAMPLES[10], EXAMPLES[11], EXAMPLES[13], EXAMPLES[14]):
        with pytest.raises(ValidationError):
            changed(model, actor=ActorRef(actor_id="other"))
    assert canonical_json(changed(EXAMPLES[3], resource_ids=("b", "a"))) == canonical_json(
        changed(EXAMPLES[3], resource_ids=("a", "b")))
    for resources in ((), ("a", "a"), tuple(f"r{i}" for i in range(33))):
        with pytest.raises(ValidationError):
            changed(EXAMPLES[3], resource_ids=resources)


@pytest.mark.parametrize("currentness", [v for v in AuthorityCurrentness if v != AuthorityCurrentness.CURRENT])
def test_historical_or_unverified_authority_is_data_not_a_current_claim(currentness):
    authority = changed(EXAMPLES[9], currentness=currentness,
        superseded_by=EXAMPLES[1] if currentness == AuthorityCurrentness.SUPERSEDED else None)
    assert parse_contract(AuthorityReference, canonical_json(authority)) == authority
    with pytest.raises(ValidationError):
        changed(EXAMPLES[11], authorities=(authority,))
    with pytest.raises(ValidationError):
        changed(EXAMPLES[10], current_authorities=(authority,))
    observation = changed(EXAMPLES[10], outcome=DecisionOutcome.WAIT, current_authorities=(authority,))
    assert observation.current_authorities[0].currentness == currentness


def test_supersession_required_kinds_and_replay_are_explicit():
    for updates in ({"currentness": AuthorityCurrentness.SUPERSEDED}, {"superseded_by": EXAMPLES[1]}):
        with pytest.raises(ValidationError):
            changed(EXAMPLES[9], **updates)
    for updates in ({"current_authorities": ()}, {"expected_authority_version": None},
                    {"required_authority_kinds": ("other",)},
                    {"current_authorities": (EXAMPLES[9], EXAMPLES[9])}):
        with pytest.raises(ValidationError):
            changed(EXAMPLES[10], **updates)
    with pytest.raises(ValidationError):
        changed(EXAMPLES[11], replay_ref=EXAMPLES[1])
    assert changed(EXAMPLES[11], replay_ref=EXAMPLES[1], idempotency_key="key").replay_ref == EXAMPLES[1]


@pytest.mark.parametrize("outcome", list(DecisionOutcome))
def test_decisions_remain_observations(outcome):
    decision = changed(EXAMPLES[10], outcome=outcome)
    assert parse_contract(AdmissibilityDecision, canonical_json(decision)).observational is True


def test_unknown_result_is_not_success_and_evidence_is_bound():
    result = EXAMPLES[13]
    unknown = changed(result, outcome=ResultOutcome.UNKNOWN, effect_status=EffectStatus.UNKNOWN,
                      output=None, evidence=())
    assert parse_contract(ExecutionResult, canonical_json(unknown)).outcome == ResultOutcome.UNKNOWN
    for updates in ({"outcome": ResultOutcome.UNKNOWN}, {"effect_status": EffectStatus.UNKNOWN},
                    {"output": None}, {"evidence": ()}, {"outcome": ResultOutcome.DENIED}):
        with pytest.raises(ValidationError):
            changed(result, **updates)
    for updates in ({"producer_operation_id": "other"}, {"producer_capability": ContractRef(contract_id="other", version=1)},
                    {"input": ContentRef(content_id="other", sha256="0" * 64)}):
        with pytest.raises(ValidationError):
            changed(result, evidence=(changed(EXAMPLES[12], **updates),))
    for outcome in (ResultOutcome.FAILURE, ResultOutcome.CANCELLED, ResultOutcome.DENIED):
        assert changed(unknown, outcome=outcome, effect_status=EffectStatus.NOT_APPLIED).outcome == outcome


def test_digest_integrity_requires_bytes_not_a_signature_or_locator():
    content = EXAMPLES[1]
    assert verify_content_digest(b"input", content)
    assert verify_content_digest(b"input", EXAMPLES[12])
    assert not verify_content_digest(b"tampered", content)
    assert not verify_content_digest(b"input", changed(content, sha256="0" * 64))
    for digest in ("f" * 63, "G" * 64, "A" * 64, "0" * 64 + "\n"):
        with pytest.raises(ValidationError):
            changed(content, sha256=digest)
    with pytest.raises(TypeError):
        verify_content_digest("opaque:path", content)
    with pytest.raises(TypeError):
        verify_content_digest(b"input", EXAMPLES[9])


def test_projection_collections_and_tags_are_consistent():
    projection, offer = EXAMPLES[-1], EXAMPLES[8]
    for updates in ({"safe_stops": (offer,)}, {"pending_human_decisions": (offer,)},
                    {"continuations": (offer, offer)}, {"diagnostics": ("x",) * 33}):
        with pytest.raises(ValidationError):
            changed(projection, **updates)
    human = changed(offer, continuation_id="human", kind=ContinuationKind.HUMAN_DECISION,
                    decision_target=EXAMPLES[0])
    stop = changed(offer, continuation_id="stop", kind=ContinuationKind.SAFE_STOP)
    assert changed(projection, pending_human_decisions=(human,), safe_stops=(stop,)).safe_stops == (stop,)


def test_transport_is_bounded_unambiguous_and_revalidates_unsafe_copies():
    for data in ('{"contract_id":"a","contract_id":"b","version":1}',
                 '{"contract_id":"a","version":NaN}', "[" * 2000 + "]" * 2000,
                 " " * 1_048_577):
        with pytest.raises(ValueError):
            parse_contract(ContractRef, data)
    for data in (lambda: True, {}):
        with pytest.raises(TypeError):
            parse_contract(ContractRef, data)
    with pytest.raises(TypeError):
        parse_contract(dict, "{}")
    with pytest.raises(TypeError):
        canonical_json({})
    with pytest.raises(ValidationError):
        canonical_json(EXAMPLES[0].model_copy(update={"version": 0}))


@pytest.mark.parametrize("model", EXAMPLES, ids=lambda m: type(m).__name__)
def test_every_sequence_is_bounded_and_nested_contracts_revalidate(model):
    for name, value in dict(model).items():
        if isinstance(value, tuple) and value:
            with pytest.raises(ValidationError):
                changed(model, **{name: value * 33})
        elif hasattr(value, "schema_version"):
            with pytest.raises(ValidationError):
                changed(model, **{name: value.model_copy(update={"schema_version": 2})})
