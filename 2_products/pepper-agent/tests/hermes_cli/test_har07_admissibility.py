"""Synthetic trusted-owner fixtures; no live authority or source inspection."""

from copy import deepcopy

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.admissibility_projection import (
    LegacyAction, LegacyContext, binding_identity, operation_policy, translate,
)
from hermes_cli.agent_platform.handler_correspondence import BindingEvidence, BindingStatus
from hermes_cli.agent_platform.harness.admissibility import (
    AdmissionEvaluation, AdmissionInput, ConsentStatus, PrerequisiteObservation,
    QualifiedEvaluation, evaluate,
)
from hermes_cli.agent_platform.harness.contracts import (
    ActorRef, AuthorityCurrentness, AuthorityReference, ContentRef, ContinuationKind,
    ContractRef, DecisionOutcome, Effect, Scope, StateDimension, StateSupport, WorkflowState,
)
from hermes_cli.agent_platform.harness.observation import (
    CheckStatus, Observation, ObservationStatus, SourceKind, SourceRef,
)
from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract
from hermes_cli.agent_platform.pre_review_catalog import product_catalog, product_operations


def ref(name, version=1):
    return ContractRef(contract_id=name, version=version)


def content(name, char="a"):
    return ContentRef(content_id=name, sha256=char * 64)


ISSUER = ref("synthetic-trusted-owner")
ACTOR = ActorRef(actor_id="local-human")
SCOPE = Scope(project_id="synthetic-project", workflow_id="synthetic-workflow", resource_ids=("T.1",))


def change(model, **updates):
    return type(model).model_validate({**model.model_dump(), **updates})


def fixture(operation_id="O02"):
    operation = next(o for o in product_operations() if o.capability.capability.contract_id == operation_id)
    policy = operation_policy(operation_id, ACTOR, SCOPE)
    # Synthetic correspondence metadata, not a claim about the live registry.
    proof = BindingEvidence(declaration=operation.handler, status=BindingStatus.VERIFIED,
        reason_code="synthetic_static_proof", source=content("synthetic-handler-source"),
        registry_import_line=1, registration_line=3, handler_line=2,
        handler_ast_sha256="b" * 64, registration_ast_sha256="c" * 64)
    authorities = tuple(AuthorityReference(authority_id="auth." + kind, kind=kind,
        issuer=ACTOR, subject=ACTOR, scope=SCOPE, policy=policy.policy,
        record=content("record." + kind), dependencies=(), currentness=AuthorityCurrentness.CURRENT)
        for kind in policy.required_authority_kinds)
    prerequisites = tuple(PrerequisiteObservation(requirement=r, observation=Observation(
        source=SourceRef(source_id=r.contract_id, kind=SourceKind.EVIDENCE, format=ref("synthetic-result")),
        scope=SCOPE, actor=ACTOR, status=ObservationStatus.PRESENT, reason_code="synthetic_capture",
        source_content=content(r.contract_id), observed_schema_version=1,
        integrity=CheckStatus.VERIFIED, structure=CheckStatus.VERIFIED, binding=CheckStatus.VERIFIED,
        consistency="STABLE_CAPTURE", completeness="BOUND_SOURCE_ONLY")) for r in policy.prerequisites)
    values = dict(publication="approved", execution="terminal_inactive", validation="passed",
        review="ready", completion="terminal_bound")
    state = WorkflowState(**{k: StateDimension(definition=ref("pepper." + k), value=v,
        support=StateSupport.SUPPORTED) for k, v in values.items()}, authority_currentness=AuthorityCurrentness.CURRENT)
    value = AdmissionInput(catalog=product_catalog(), catalog_content=product_catalog().content_identity(),
        capability=operation.capability, transition=operation.transition, policy=policy,
        actor=ACTOR, scope=SCOPE, state=state, authorities=authorities, prerequisites=prerequisites,
        authority_version="synthetic-v1", source_version=content("synthetic-source-version"),
        effect=operation.capability.effect, handler_evidence=binding_identity(proof), consent=ConsentStatus.GRANTED)
    return value, proof


def qualified(value):
    # This is an explicit test trust assumption, not a production resolver.
    return QualifiedEvaluation(issuer=ISSUER, input=value.content_identity(),
        authority_ids=tuple(a.authority_id for a in value.authorities),
        prerequisites=tuple(p.requirement for p in value.prerequisites), handler_evidence=value.handler_evidence)


def admit(value):
    return evaluate(value, trusted_issuer=ISSUER, qualification=qualified(value))


def context(operation="O02", **updates):
    action_id, human = {
        "O02": ("VALIDATE_T_1_COMMANDS", "command_validation_authorization"),
        "O05": ("REQUEST_T_1_POST_EXECUTION_MATERIAL_REVISION", "post_execution_material_revision_request"),
        "O07": ("RECONCILE_MATERIAL_REVISION_AUTHORITY", "authority_reconciliation"),
        "O08": ("REVISE_T_1", "ticket_material_revision"),
        "P03.prepare": ("PREPARE_T_1_REVIEW", "human_review_preparation"),
    }.get(operation, ("NO_STANDALONE_ACTION", "inspection"))
    return LegacyContext(**{**dict(current_ticket_id="T.1", action=LegacyAction(id=action_id,
        label="Existing legacy label", target_ticket_id="T.1", required_human_action=human),
        operation=operation, target_ticket_id="T.1", active_execution=False), **updates})


def test_complete_synthetic_allow_is_observation_only():
    value, _ = fixture()
    result = admit(value)
    assert result.decision.outcome == DecisionOutcome.ALLOW
    assert result.decision.observational is True
    assert result.continuations[0].kind == ContinuationKind.EXECUTABLE_CAPABILITY
    assert result.continuations[0].capability == value.capability.capability
    assert "operation_id" not in result.model_dump()
    assert parse_contract(AdmissionEvaluation, canonical_json(result)) == result


def test_determinism_and_collection_order():
    value, _ = fixture()
    reordered = change(value, authorities=tuple(reversed(value.authorities)),
        prerequisites=tuple(reversed(value.prerequisites)))
    assert value.content_identity() == reordered.content_identity()
    assert canonical_json(admit(value)) == canonical_json(admit(reordered)) == canonical_json(admit(value))


@pytest.mark.parametrize("case", ["capability", "transition", "policy_version", "effect", "weaken_authority",
    "weaken_prerequisite", "actor", "project", "resource", "catalog", "unsupported_rule", "state_schema"])
def test_identity_policy_failures_stop(case):
    value, _ = fixture()
    if case == "capability":
        value = change(value, policy=change(value.policy, capability=ref("unknown")))
    elif case == "transition":
        value = change(value, transition=change(value.transition, capability=ref("unknown")))
    elif case == "policy_version":
        value = change(value, policy=change(value.policy, policy=ref(value.policy.policy.contract_id, 2)))
    elif case == "effect":
        value = change(value, effect=Effect.OBSERVE)
    elif case == "weaken_authority":
        value = change(value, policy=change(value.policy, required_authority_kinds=(), consent_kind=None))
    elif case == "weaken_prerequisite":
        value = change(value, policy=change(value.policy, prerequisites=()))
    elif case == "actor":
        value = change(value, actor=ActorRef(actor_id="another-human"))
    elif case in ("project", "resource"):
        scope = change(SCOPE, **({"project_id": "other"} if case == "project" else {"resource_ids": ("other",)}))
        value = change(value, scope=scope)
    elif case == "catalog":
        value = change(value, catalog_content=content("stale-catalog"))
    elif case == "unsupported_rule":
        value = change(value, policy=change(value.policy, unsupported_requirements=(ref("domain.not-implemented"),)))
    elif case == "state_schema":
        value, _ = fixture("P03.prepare")
        value = change(value, state=change(value.state, review=change(value.state.review, support=StateSupport.UNSUPPORTED)))
    result = admit(value)
    assert result.decision.outcome == DecisionOutcome.SAFE_STOP
    assert result.continuations[0].capability is None


@pytest.mark.parametrize("status", [AuthorityCurrentness.UNVERIFIED, AuthorityCurrentness.HISTORICAL,
    AuthorityCurrentness.SUPERSEDED, AuthorityCurrentness.CONFLICT, AuthorityCurrentness.UNSUPPORTED])
def test_authority_currentness_never_inferred(status):
    value, _ = fixture()
    authority = change(value.authorities[0], currentness=status,
        superseded_by=content("successor") if status == AuthorityCurrentness.SUPERSEDED else None)
    value = change(value, authorities=(authority,) + value.authorities[1:])
    assert admit(value).decision.outcome != DecisionOutcome.ALLOW


def test_missing_authority_kind_stops():
    value, _ = fixture()
    assert admit(change(value, authorities=value.authorities[1:])).decision.outcome == DecisionOutcome.SAFE_STOP


def test_ambiguous_authority_kind_stops():
    value, _ = fixture()
    duplicate = change(value.authorities[0], authority_id="second", record=content("different"))
    assert admit(change(value, authorities=value.authorities + (duplicate,))).decision.reason_code == "authority_kind_ambiguous"


@pytest.mark.parametrize("consent,expected", [(ConsentStatus.MISSING, "WAIT"), (ConsentStatus.PENDING, "WAIT"),
    (ConsentStatus.DENIED, "DENY"), (ConsentStatus.EXPIRED, "WAIT"), (ConsentStatus.SUPERSEDED, "WAIT"),
    (ConsentStatus.CONFLICT, "SAFE_STOP"), (ConsentStatus.UNSUPPORTED, "SAFE_STOP")])
def test_consent_states(consent, expected):
    value, _ = fixture()
    result = admit(change(value, consent=consent))
    assert result.decision.outcome.value == expected
    assert result.continuations[0].capability is None
    if expected == "WAIT":
        assert result.continuations[0].kind == ContinuationKind.HUMAN_DECISION
        assert result.continuations[0].decision_target == value.capability.capability


@pytest.mark.parametrize("status", [ObservationStatus.INVALID, ObservationStatus.CONFLICT,
    ObservationStatus.UNSTABLE, ObservationStatus.UNSUPPORTED])
def test_invalid_or_unstable_prerequisite_stops(status):
    value, _ = fixture()
    item = value.prerequisites[0]
    obs = Observation(source=item.observation.source, scope=SCOPE, actor=ACTOR, status=status, reason_code="synthetic_failure")
    value = change(value, prerequisites=(change(item, observation=obs),) + value.prerequisites[1:])
    assert admit(value).decision.outcome == DecisionOutcome.SAFE_STOP


def test_missing_prerequisite_waits():
    value, _ = fixture()
    assert admit(change(value, prerequisites=value.prerequisites[1:])).decision.outcome == DecisionOutcome.WAIT


def test_present_verified_capture_and_current_claims_are_insufficient():
    value, _ = fixture()
    assert all(p.observation.currentness == AuthorityCurrentness.UNVERIFIED for p in value.prerequisites)
    assert evaluate(value).decision.outcome != DecisionOutcome.ALLOW
    assert evaluate(value, qualification=qualified(value)).decision.outcome != DecisionOutcome.ALLOW


def test_prerequisite_requires_qualification_beyond_present():
    value, _ = fixture()
    result = evaluate(value, trusted_issuer=ISSUER, qualification=change(qualified(value), prerequisites=()))
    assert result.decision.outcome == DecisionOutcome.WAIT
    assert "prerequisite_not_qualified" in {r.code for r in result.reasons}


def test_safety_precedence_over_denial_and_later_missing_evidence():
    value, _ = fixture()
    value = change(value, consent=ConsentStatus.DENIED, effect=Effect.OBSERVE, prerequisites=())
    result = admit(value)
    assert result.decision.outcome == DecisionOutcome.SAFE_STOP
    assert result.decision.reason_code == "effect_mismatch"
    assert {"effect_mismatch", "consent_denied", "prerequisite_missing"} <= {r.code for r in result.reasons}
    assert result == admit(change(value, authorities=tuple(reversed(value.authorities))))


def test_denial_precedes_pending_prerequisites():
    value, _ = fixture()
    result = admit(change(value, consent=ConsentStatus.DENIED, prerequisites=()))
    assert result.decision.outcome == DecisionOutcome.DENY
    assert result.decision.reason_code == "consent_denied"


def test_projection_preflight_parity_and_revocation():
    value, _ = fixture()
    projection = admit(value)
    assert projection == admit(deepcopy(value))
    old = parse_contract(AdmissionEvaluation, canonical_json(projection))
    for changed in (change(value, authority_version="synthetic-v2"),
            change(value, source_version=content("source-v2", "b")), change(value, consent=ConsentStatus.DENIED)):
        fresh = evaluate(changed, trusted_issuer=ISSUER, qualification=qualified(value))
        assert fresh.decision.outcome != DecisionOutcome.ALLOW
        assert fresh.input != old.input
    assert admit(change(value, consent=ConsentStatus.DENIED)).decision.outcome == DecisionOutcome.DENY
    with pytest.raises(ValidationError):
        evaluate(old)
    with pytest.raises(ValidationError):
        evaluate(value, trusted_issuer=ISSUER, qualification=old)


@pytest.mark.parametrize("operation", [o.capability.capability.contract_id for o in product_operations()])
def test_all_first_slice_declarations_have_explicit_policy(operation):
    value, _ = fixture(operation)
    assert set(value.transition.prerequisites) <= set(value.policy.prerequisites)
    assert set(value.capability.required_authority_kinds) <= set(value.policy.required_authority_kinds)
    assert admit(value).decision.outcome == DecisionOutcome.ALLOW
    if value.effect == Effect.OBSERVE:
        assert admit(value).continuations[0].kind == ContinuationKind.OBSERVATION
        # OBSERVE is a declaration, never a proof of implementation purity.
        assert evaluate(value).decision.outcome != DecisionOutcome.ALLOW


@pytest.mark.parametrize("operation", ["O02", "O05", "O07", "O08", "P03.prepare"])
def test_qualified_public_ids_and_legacy_optional_absence_preserved(operation):
    value, proof = fixture(operation)
    ctx = context(operation)
    result = translate(admit(value), ctx, binding=proof)
    assert result.qualification == "MAPPED"
    assert result.action.public_fields() == ctx.action.public_fields()
    assert "executable" not in result.action.public_fields()
    assert result.invocable is True


@pytest.mark.parametrize("operation", ["O01", "O03.ticket_spec", "O03.validation_steps", "O04", "O06", "P01",
    "P02.passed", "P02.failed", "P03.workflow", "P03.review"])
def test_no_invented_action_for_inspection_or_attestation(operation):
    value, _ = fixture(operation)
    result = translate(admit(value), context(operation))
    assert result.qualification == "UNMAPPED"
    assert result.action is None and result.handler is None and not result.invocable


@pytest.mark.parametrize("status", [BindingStatus.ABSENT, BindingStatus.AMBIGUOUS,
    BindingStatus.CONTRADICTORY, BindingStatus.UNVERIFIABLE])
def test_unqualified_handler_correspondence_never_invocable(status):
    value, proof = fixture()
    result = translate(admit(value), context(), binding=change(proof, status=status))
    assert result.qualification == "UNSUPPORTED" and not result.invocable
    assert not translate(admit(value), context()).invocable


def test_handler_proof_identity_and_selectors_must_match():
    value, proof = fixture()
    altered = change(proof, source=content("different-source", "b"))
    assert not translate(admit(value), context(), binding=altered).invocable
    assert admit(change(value, handler_evidence=None)).decision.outcome == DecisionOutcome.SAFE_STOP


def test_pending_human_offer_has_no_binding_or_implied_approval():
    value, proof = fixture()
    result = admit(change(value, consent=ConsentStatus.PENDING))
    translated = translate(result, context())
    assert translated.qualification == "MAPPED" and not translated.invocable and translated.handler is None
    assert translate(result, context(), binding=proof).qualification == "UNSUPPORTED"


@pytest.mark.parametrize("flags", [{"executable": False}, {"read_only": True}])
def test_translation_never_promotes_explicit_legacy_nonexecutable_action(flags):
    value, proof = fixture()
    ctx = context()
    ctx = change(ctx, action=change(ctx.action, **flags))
    result = translate(admit(value), ctx, binding=proof)
    assert result.qualification == "UNSUPPORTED" and not result.invocable
    assert result.handler is None and result.action is None


def test_unqualified_c94_source_fails_closed():
    value, proof = fixture("O07")
    result = evaluate(value)
    assert result.decision.outcome == DecisionOutcome.SAFE_STOP
    assert result.continuations[0].kind == ContinuationKind.SAFE_STOP
    assert not translate(result, context("O07"), binding=proof).invocable


@pytest.mark.parametrize("family,kind", [("EXECUTION_AUTHORITY", ContinuationKind.SAFE_STOP),
    ("REVIEW_BLOCKER", ContinuationKind.EXTERNAL_REMEDIATION)])
def test_diagnostic_shapes_preserved_without_handler(family, kind):
    value, proof = fixture()
    value = change(value, policy=change(value.policy, blocked_kind=kind))
    result = evaluate(value)
    flags = {"executable": False, "read_only": True} if family == "EXECUTION_AUTHORITY" else {}
    ctx = context(operation="RESOLVE_" + family, action=LegacyAction(id="RESOLVE_T_1_" + family,
        label="Existing diagnostic", target_ticket_id="T.1", **flags), active_execution=True)
    translated = translate(result, ctx)
    assert translated.qualification == "MAPPED"
    assert translated.action.public_fields() == ctx.action.public_fields()
    assert not translated.invocable and translated.handler is None
    assert not translate(result, ctx, binding=proof).invocable


def test_c26_active_context_keeps_successor_decision_separate():
    value, _ = fixture()
    successor = LegacyAction(id="REVISE_T_2", label="Separate rejected successor", target_ticket_id="T.2")
    ctx = context(operation="RESOLVE_EXECUTION_AUTHORITY", active_execution=True,
        next_ticket_id="T.2", separate_successor_decision=successor,
        action=LegacyAction(id="RESOLVE_T_1_EXECUTION_AUTHORITY", label="Blocked active ticket",
            target_ticket_id="T.1", executable=False, read_only=True))
    result = translate(evaluate(value), ctx)
    assert result.current_ticket_id == "T.1" and result.next_ticket_id == "T.2"
    assert result.separate_successor_decision == successor
    assert result.action.id == "RESOLVE_T_1_EXECUTION_AUTHORITY"


def test_c26_rejected_successor_without_active_ticket_keeps_none_current():
    value, proof = fixture("O08")
    result = translate(admit(value), context("O08", current_ticket_id=None, next_ticket_id="T.1"), binding=proof)
    assert result.qualification == "MAPPED" and result.current_ticket_id is None
    assert result.action.target_ticket_id == "T.1"


def test_c26_active_monitor_outside_slice_is_unmapped_without_reselection():
    value, _ = fixture()
    successor = LegacyAction(id="REVISE_T_2", label="Separate decision", target_ticket_id="T.2")
    ctx = context(operation="C26.monitor", active_execution=True, next_ticket_id="T.2",
        separate_successor_decision=successor, action=LegacyAction(id="MONITOR_T_1_EXECUTION", label="Monitor"))
    result = translate(admit(value), ctx)
    assert result.qualification == "UNMAPPED" and result.current_ticket_id == "T.1"
    assert result.next_ticket_id == "T.2" and result.separate_successor_decision == successor
    assert result.action is None and not result.invocable


def test_missing_authority_policy_wait_is_explicit_and_still_not_allow():
    value, _ = fixture("O01")
    value = change(value, policy=change(value.policy, missing_authority="WAIT", handler_required=False))
    assert evaluate(value).decision.outcome == DecisionOutcome.WAIT


def test_currentness_qualification_is_bound_to_owner_and_exact_input():
    value, _ = fixture()
    proof = qualified(value)
    assert evaluate(value, trusted_issuer=ref("other-owner"), qualification=proof).decision.outcome == DecisionOutcome.SAFE_STOP
    partial = change(proof, authority_ids=())
    assert evaluate(value, trusted_issuer=ISSUER, qualification=partial).decision.outcome != DecisionOutcome.ALLOW
    complete = admit(value)
    absent = evaluate(value)
    assert complete.input != absent.input and complete.decision.decision_id != absent.decision.decision_id
    assert complete.context.source_input == absent.context.source_input == value.content_identity()
    assert complete.context.qualification == proof


def test_active_execution_never_advertises_review_preparation():
    value, proof = fixture("P03.prepare")
    state = change(value.state, execution=change(value.state.execution, value="active"))
    assert admit(change(value, state=state)).decision.outcome != DecisionOutcome.ALLOW
    assert not translate(admit(value), context("P03.prepare", active_execution=True), binding=proof).invocable


@pytest.mark.parametrize("operation", ["O01", "O02", "O04", "O05", "O06", "O07", "O08", "P01", "P02.passed", "P02.failed"])
def test_terminal_bound_operations_reject_active_or_unknown_execution(operation):
    value, _ = fixture(operation)
    for support, name in ((StateSupport.SUPPORTED, "active"), (StateSupport.UNKNOWN, "unknown")):
        state = change(value.state, execution=change(value.state.execution, value=name, support=support))
        assert admit(change(value, state=state)).decision.outcome != DecisionOutcome.ALLOW


@pytest.mark.parametrize("dimension", ["publication", "execution", "validation", "review", "completion"])
def test_terminal_review_ready_requires_all_dimensions(dimension):
    value, _ = fixture("P03.prepare")
    state = change(value.state, **{dimension: change(getattr(value.state, dimension), value="incomplete")})
    assert admit(change(value, state=state)).decision.outcome == DecisionOutcome.WAIT
    assert admit(change(value, prerequisites=())).decision.outcome == DecisionOutcome.WAIT


def test_unknown_public_action_never_falls_back():
    value, proof = fixture()
    result = translate(admit(value), context(action=LegacyAction(id="INTERNAL_O02_requested", label="Wrong")), binding=proof)
    assert result.qualification == "UNMAPPED" and result.action is None


@pytest.mark.parametrize("ticket,action", [("t-1", "VALIDATE_T_1_COMMANDS"),
    ("P18.9.13-X", "VALIDATE_P18_9_13_X_COMMANDS")])
def test_public_capability_token_matches_legacy_normalization(monkeypatch, ticket, action):
    monkeypatch.setitem(globals(), "SCOPE", change(SCOPE, resource_ids=(ticket,)))
    value, proof = fixture()
    ctx = context(current_ticket_id=ticket, target_ticket_id=ticket,
        action=LegacyAction(id=action, label="Existing action", target_ticket_id=ticket,
            required_human_action="command_validation_authorization"))
    assert translate(admit(value), ctx, binding=proof).action.id == action


def test_unchecked_copies_and_extra_execution_fields_rejected():
    value, _ = fixture()
    broken = value.model_copy(update={"catalog_content": value.catalog_content.model_copy(update={"schema_version": True})})
    with pytest.raises(ValidationError):
        admit(broken)
    with pytest.raises(ValidationError):
        AdmissionInput.model_validate({**value.model_dump(), "execute": True})


def test_typed_continuation_guards_reject_contradictory_offer():
    value, proof = fixture()
    result = admit(value)
    continuation = change(result.continuations[0], capability=ref("other"))
    forged = change(result, continuations=(continuation,))
    assert not translate(forged, context(), binding=proof).invocable
    denied = admit(change(value, consent=ConsentStatus.DENIED))
    forged = change(result, decision=denied.decision)
    assert not translate(forged, context(), binding=proof).invocable
