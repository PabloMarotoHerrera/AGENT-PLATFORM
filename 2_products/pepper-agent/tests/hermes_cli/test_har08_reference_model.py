"""Independent case expectations and deliberately bad abstract transitions."""

import pytest

from hermes_cli.agent_platform.harness.admissibility import ConsentStatus, QualifiedEvaluation, evaluate
from hermes_cli.agent_platform.admissibility_projection import LegacyAction, LegacyContext, translate
from hermes_cli.agent_platform.harness.contracts import AuthorityCurrentness, DecisionOutcome, ResultOutcome
from hermes_cli.agent_platform.harness.coverage import ExplorationBounds
from hermes_cli.agent_platform.harness.reference_model import check_reference, generate_scenarios, materialize_admission
from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract
from hermes_cli.agent_platform.pre_review_reference_model import build_synthetic_reference_model
from tests.hermes_cli.test_har08_coverage import bindings_fixture, change, fixture, ref


@pytest.fixture(scope="module")
def model():
    return build_synthetic_reference_model(fixture())


@pytest.fixture(scope="module")
def report(model):
    return check_reference(model)


def test_bounded_model_has_independent_negative_witnesses(model, report):
    assert report.complete and report.passed and not report.violations
    assert report.generated_scenarios == len(model.scenarios) + len(model.structural)
    assert report.explored_states == len(set(report.states))
    assert report.explored_transitions == len(set(report.transitions))
    assert report.explored_states <= report.bounds.states and report.explored_depth <= report.bounds.depth
    assert report.witnesses and report.structural_results and all(r.matched for r in report.structural_results)
    assert report.unique_negative_witnesses == len(report.witnesses) + len(report.structural_results)
    assert len({(w.scenario_id, w.property) for w in report.witnesses}) == len(report.witnesses)
    assert report.assumptions and "live_authority" in report.unsupported_semantics
    assert parse_contract(type(report), canonical_json(report)).content_identity() == report.content_identity()


# Independently stated expectations, not read from the generator or evaluate().
@pytest.mark.parametrize("case,expected", [
    ("valid.O01", "ALLOW"), ("valid.O03.ticket_spec", "ALLOW"),
    ("command-prerequisite-missing", "WAIT"), ("command-consent.MISSING", "WAIT"),
    ("command-consent.DENIED", "DENY"), ("command-evidence-invalid", "SAFE_STOP"),
    ("artifact-version-mismatch", "SAFE_STOP"), ("artifact-source-drift", "SAFE_STOP"),
    ("artifact-rejected-generation", "WAIT"), ("artifact-partial-not-approval", "WAIT"),
    ("revision-human-decision", "WAIT"), ("revision-stale-workpacket", "SAFE_STOP"),
    ("unqualified-origin", "SAFE_STOP"), ("reconciliation-contradictory-chain", "SAFE_STOP"),
    ("valid.O08", "ALLOW"), ("manual-pending", "WAIT"), ("manual-failed", "WAIT"),
    ("review-active-execution", "WAIT"), ("review-missing-attestation", "WAIT"),
    ("valid.P03.prepare", "ALLOW"), ("missing-executor", "SAFE_STOP"),
    ("evidence-invalidated", "WAIT"), ("stale-catalog", "SAFE_STOP"),
    ("authority.UNSUPPORTED", "SAFE_STOP"), ("authority.CONFLICT", "SAFE_STOP"),
    ("stale-command-authorization", "SAFE_STOP"), ("duplicate-stale-request", "SAFE_STOP"),
    ("failed-command-not-attestation", "ALLOW"), ("unknown-command-not-success", "ALLOW"),
    ("old-allow-after-version-change", "SAFE_STOP"), ("active-context-rejected-successor", "ALLOW"),
    ("artifact-binding.synthetic-ticket-spec", "SAFE_STOP"), ("artifact-binding.synthetic-workpacket", "SAFE_STOP"),
    ("duplicate-request-authority", "SAFE_STOP"),
])
def test_c91_c94_independent_case_expectations(report, case, expected):
    actual = next(r for r in report.results if r.scenario_id == case)
    assert actual.outcome.value == expected
    if expected != "ALLOW":
        assert any(w.scenario_id == case for w in report.witnesses)
        assert actual.before == actual.after


def test_inspections_and_authority_transitions_are_distinct(model, report):
    inspections = {"O01", "O03.ticket_spec", "O03.validation_steps", "O04", "O06", "P01", "P03.workflow", "P03.review"}
    for r in report.results:
        if r.scenario_id == "valid." + r.operation.contract_id and r.operation.contract_id in inspections:
            assert r.before == r.after
    for op in ("O05", "O07", "O08"):
        scenario = next(s for s in model.scenarios if s.scenario_id == "valid." + op)
        assert not scenario.successor.successor_approved and not scenario.successor.authority_created
    revision = next(s for s in model.scenarios if s.scenario_id == "valid.O08")
    assert revision.successor.workflow.publication.value == "pending_approval"
    assert revision.successor.workflow.authority_currentness == AuthorityCurrentness.UNVERIFIED
    assert revision.successor.workflow.execution.value != "active"
    assert revision.successor.evidence == "INVALIDATED" and revision.successor.consent == ConsentStatus.MISSING


@pytest.mark.parametrize("operation,human", [("O02", "command_validation_authorization"),
    ("O05", "post_execution_material_revision_request"), ("O07", "authority_reconciliation"),
    ("O08", "ticket_material_revision"), ("P03.prepare", "human_review_preparation")])
def test_exact_public_mapping_is_qualified_by_accepted_har07_translation(model, operation, human):
    scenario = next(s for s in model.scenarios if s.scenario_id == "valid." + operation)
    value = materialize_admission(model, scenario)
    result = evaluate(value, trusted_issuer=scenario.trusted_issuer, qualification=scenario.qualification)
    action = next(a for a in model.coverage.actions if a.capability == ref(operation))
    proof = next(p for p in bindings_fixture() if p.declaration.capability == ref(operation))
    context = LegacyContext(current_ticket_id="SYN-1", target_ticket_id="SYN-1", active_execution=False,
        operation=operation, action=LegacyAction(id=action.action.contract_id, label="Synthetic legacy label",
            target_ticket_id="SYN-1", required_human_action=human))
    translated = translate(result, context, binding=proof)
    assert translated.qualification == "MAPPED" and translated.action.id == action.action.contract_id


def test_unqualified_graph_is_not_claimed_covered_by_synthetic_traces():
    report = check_reference(build_synthetic_reference_model(fixture(False)))
    assert report.coverage.classification == "INCOMPLETE" and not report.passed


def test_deterministic_generator_state_identities_and_digest(model, report):
    reversed_model = change(model, scenarios=tuple(reversed(model.scenarios)), structural=tuple(reversed(model.structural)))
    assert model.content_identity() == reversed_model.content_identity()
    assert canonical_json(generate_scenarios(model, seed=7)) == canonical_json(generate_scenarios(reversed_model, seed=7))
    assert check_reference(reversed_model).content_identity() == report.content_identity()
    assert check_reference(model).states == report.states


@pytest.mark.parametrize("bounds,hit", [(ExplorationBounds(scenarios=1), "scenarios"),
    (ExplorationBounds(states=1), "states"), (ExplorationBounds(depth=0), "depth"), (ExplorationBounds(work=1), "work")])
def test_state_exploration_bounds_never_claim_complete(model, bounds, hit):
    report = check_reference(model, bounds)
    assert not report.complete and not report.passed and hit in report.bound_hits
    assert report.explored_states <= bounds.states
    if hit == "scenarios":
        assert report.generated_scenarios < report.declared_scenarios


def test_unsupported_reference_version_and_duplicate_scenario(model):
    assert not check_reference(change(model, model=ref(model.model.contract_id, 2))).complete
    with pytest.raises(ValueError, match="duplicate"):
        change(model, scenarios=model.scenarios + model.scenarios[:1])
    for seed in (True, -1, 65536):
        with pytest.raises(ValueError):
            generate_scenarios(model, seed=seed)


def bad_trace(model, case, *, facts_update=None, before_update=None, after_update=None):
    original = next(s for s in model.scenarios if s.scenario_id == case)
    scenario = change(original, facts=facts_update(original.facts) if facts_update else original.facts,
        before=before_update(original.before) if before_update else original.before,
        successor=after_update(original.successor) if after_update else original.successor,
        expected=(DecisionOutcome.ALLOW,))
    single = change(model, scenarios=(scenario,), structural=())
    value = materialize_admission(single, scenario)
    proof = QualifiedEvaluation(issuer=scenario.trusted_issuer, input=value.content_identity(),
        authority_ids=tuple(a.authority_id for a in value.authorities),
        prerequisites=tuple(p.requirement for p in value.prerequisites), handler_evidence=value.handler_evidence)
    return change(single, scenarios=(change(scenario, qualification=proof),))


def test_independent_oracle_catches_weakened_consent_policy(model):
    operation = next(o for o in model.coverage.operations if o.capability == ref("O02"))
    weak_policy = change(operation.policy, consent_kind=None)
    bad = bad_trace(model, "valid.O02", facts_update=lambda f: change(f, consent=ConsentStatus.MISSING, policy_override=weak_policy),
        before_update=lambda s: change(s, consent=ConsentStatus.MISSING))
    report = check_reference(bad)
    assert any(w.property == "missing_consent_executable" for w in report.violations)
    assert not report.passed


def test_independent_oracle_catches_active_review_with_weak_policy(model):
    operation = next(o for o in model.coverage.operations if o.capability == ref("P03.prepare"))
    weak_policy = change(operation.policy, states=())
    def active(state):
        return change(state, execution=change(state.execution, value="active"))
    bad = bad_trace(model, "valid.P03.prepare", facts_update=lambda f: change(f, state=active(f.state), policy_override=weak_policy),
        before_update=lambda s: change(s, workflow=active(s.workflow)))
    assert any(w.property == "active_execution_enabled_review" for w in check_reference(bad).violations)


@pytest.mark.parametrize("case,update,property", [
    ("valid.O05", {"successor_approved": True}, "material_transition_created_authority"),
    ("valid.O07", {"authority_created": True}, "material_transition_created_authority"),
    ("active-context-rejected-successor", {"selected_ticket": "SYN-REJECTED"}, "active_predecessor_displaced"),
    ("unknown-command-not-success", {"command_passed": True}, "unknown_result_promoted"),
    ("failed-command-not-attestation", {"manual_passed": True}, "failed_command_became_attestation"),
])
def test_independent_oracle_detects_invalid_abstract_successor(model, case, update, property):
    bad = bad_trace(model, case, after_update=lambda s: change(s, **update))
    assert any(w.property == property for w in check_reference(bad).violations)


@pytest.mark.parametrize("case,update,property", [
    ("valid.O02", {"correspondence": False}, "handlerless_executable"),
    ("valid.O02", {"evidence": "INVALIDATED"}, "missing_or_invalidated_evidence_allowed"),
    ("valid.O07", {"qualified_origin": False}, "unqualified_reconciliation_executable"),
])
def test_independent_oracle_detects_bad_source_or_boundary_claim(model, case, update, property):
    bad = bad_trace(model, case, before_update=lambda s: change(s, **update))
    assert any(w.property == property for w in check_reference(bad).violations)
