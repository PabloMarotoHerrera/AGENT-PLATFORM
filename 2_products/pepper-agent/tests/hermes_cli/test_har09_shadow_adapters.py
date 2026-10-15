"""Explicit synthetic trust assumptions; none of these facts are live authority."""

import pytest
from functools import lru_cache
from pydantic import ValidationError

from hermes_cli.agent_platform.admissibility_projection import LegacyAction, LegacyContext
from hermes_cli.agent_platform.harness.admissibility import QualifiedEvaluation, ConsentStatus
from hermes_cli.agent_platform.harness.contracts import ContinuationKind, DecisionOutcome
from hermes_cli.agent_platform.harness.reference_model import materialize_admission
from hermes_cli.agent_platform.harness.shadow import (
    Category, DecisionView, LegacyObservation, Provenance, PublicAction, compare,
)
from hermes_cli.agent_platform.pre_review_reference_model import build_synthetic_reference_model
from hermes_cli.agent_platform.shadow_adapters import SnapshotMetadata, assemble, observe
from tests.hermes_cli.test_har08_coverage import bindings_fixture, fixture, content


def change(instance, **updates):
    # Preserve nested optional-field presence; dumping first would turn absent
    # public fields into explicit nulls and change the observation being tested.
    return type(instance).model_validate(instance.model_copy(update=updates))

MAPPINGS = {
    "O02": ("VALIDATE_SYN_1_COMMANDS", "command_validation_authorization"),
    "O05": ("REQUEST_SYN_1_POST_EXECUTION_MATERIAL_REVISION", "post_execution_material_revision_request"),
    "O07": ("RECONCILE_MATERIAL_REVISION_AUTHORITY", "authority_reconciliation"),
    "O08": ("REVISE_SYN_1", "ticket_material_revision"),
    "P03.prepare": ("PREPARE_SYN_1_REVIEW", "human_review_preparation"),
}


@lru_cache(maxsize=1)
def reference_fixture():
    return build_synthetic_reference_model(fixture())


def case(name="valid.O07"):
    model = reference_fixture()
    scenario = next(s for s in model.scenarios if s.scenario_id == name)
    value = materialize_admission(model, scenario)
    op = scenario.operation.contract_id
    proof = next(b for b in bindings_fixture() if b.declaration.capability == scenario.operation)
    action_id, human = MAPPINGS.get(op, ("INSPECT_SYN_1", "inspection"))
    context = LegacyContext(current_ticket_id="SYN-1", target_ticket_id="SYN-1",
        operation=op, active_execution=scenario.before.workflow.execution.value == "active",
        action=LegacyAction(id=action_id, label="Synthetic legacy label", target_ticket_id="SYN-1",
            required_human_action=human))
    metadata = SnapshotMetadata(snapshot=content("synthetic-snapshot"), handler_source=proof.source,
        catalog=value.catalog_content, context=context, actor=value.actor, scope=value.scope,
        state=value.state, authority_version=value.authority_version, source_version=value.source_version,
        consent=value.consent, authorities=value.authorities, prerequisites=value.prerequisites)
    return scenario, metadata, proof if value.handler_evidence is not None else None


def assumed_qualification(metadata, proof, issuer):
    """Test-only trust assumption; no adapter/production qualification factory."""
    v = assemble(metadata, proof)
    return QualifiedEvaluation(issuer=issuer, input=v.content_identity(),
        authority_ids=tuple(a.authority_id for a in v.authorities),
        prerequisites=tuple(p.requirement for p in v.prerequisites), handler_evidence=v.handler_evidence)


def expected_legacy(scenario, metadata):
    """Authored HAR-08 expectation, distinct from the HAR-07 evaluation result."""
    outcome = scenario.expected[0].value
    op = metadata.context.operation
    human = outcome == "WAIT" and metadata.consent in {
        ConsentStatus.MISSING, ConsentStatus.PENDING, ConsentStatus.EXPIRED, ConsentStatus.SUPERSEDED}
    kind = (ContinuationKind.SAFE_STOP if outcome == "SAFE_STOP" else
        ContinuationKind.EXTERNAL_REMEDIATION if outcome == "DENY" else
        ContinuationKind.HUMAN_DECISION if human else ContinuationKind.OBSERVATION if outcome == "WAIT"
        or scenario.facts.effect.value == "OBSERVE" else ContinuationKind.EXECUTABLE_CAPABILITY)
    mapped = op in MAPPINGS and not metadata.context.active_execution and (
        kind == ContinuationKind.EXECUTABLE_CAPABILITY or human)
    action = PublicAction.model_validate(metadata.context.action.public_fields()) if mapped else None
    return LegacyObservation(source=content("synthetic-legacy-source"), snapshot=metadata.snapshot,
        provenance=Provenance.SYNTHETIC, authority_qualification="SYNTHETIC_TRUST_ASSUMPTION",
        view=DecisionView(operation=op, capability=scenario.operation,
            policy=assemble(metadata, None).policy.policy, actor=metadata.actor, scope=metadata.scope,
            current_ticket_id=metadata.context.current_ticket_id, target_ticket_id=metadata.context.target_ticket_id,
            action=action, mapping="MAPPED" if mapped else "UNSUPPORTED" if op in MAPPINGS else "UNMAPPED",
            outcome=outcome, continuation=kind, effect=scenario.facts.effect, consent=metadata.consent,
            decision_target="SYN-1" if human else None,
            execution_target="SYN-1" if kind == ContinuationKind.EXECUTABLE_CAPABILITY else None,
            required_authority_kinds=assemble(metadata, None).policy.required_authority_kinds,
            authority_version=metadata.authority_version, source_version=metadata.source_version,
            guards=tuple(sorted(p.requirement.contract_id + ":" + p.observation.status.value for p in metadata.prerequisites)),
            active_execution=metadata.context.active_execution,
            terminal=metadata.state.execution.value == "terminal_inactive", review_ready=metadata.state.review.value == "ready"))


@pytest.mark.parametrize("operation", [b.declaration.capability.contract_id for b in bindings_fixture()])
def test_all_fifteen_operations_require_independent_qualification(operation):
    s, metadata, proof = case("valid." + operation)
    observed = observe(metadata, proof)
    assert observed.evaluation.decision.outcome != DecisionOutcome.ALLOW
    assert observed.evaluation.qualification_issuer is None
    qualified = observe(metadata, proof, trusted_issuer=s.trusted_issuer,
        qualification=assumed_qualification(metadata, proof, s.trusted_issuer))
    assert qualified.evaluation.decision.outcome == DecisionOutcome.ALLOW
    assert qualified.view.mapping == ("MAPPED" if operation in MAPPINGS else "UNMAPPED")
    assert not any(k in qualified.model_dump() for k in ("execution_request", "dispatch"))


@pytest.mark.parametrize("status", ["ABSENT", "AMBIGUOUS", "CONTRADICTORY", "UNVERIFIABLE"])
def test_nonverified_correspondence_never_becomes_executable(status):
    s, metadata, proof = case()
    from hermes_cli.agent_platform.handler_correspondence import BindingStatus
    proof = change(proof, status=BindingStatus(status))
    result = observe(metadata, proof, trusted_issuer=s.trusted_issuer,
        qualification=assumed_qualification(metadata, proof, s.trusted_issuer))
    assert result.view.outcome == "SAFE_STOP" and not (result.view.action and result.view.action.executable)


def test_stale_source_proof_is_rejected_instead_of_reused():
    _, metadata, proof = case()
    with pytest.raises(ValueError, match="stale_or_wrong"):
        assemble(change(metadata, handler_source=content("new-source", "b")), proof)


def test_unqualified_c94_adapter_never_publishes_executable():
    _, metadata, proof = case()
    result = observe(metadata, proof)
    assert result.view.outcome != "ALLOW"
    assert result.view.action is None or result.view.action.executable is not True
    assert result.correspondence is not None  # Source proof alone is insufficient.


def test_old_allow_qualification_cannot_survive_revocation():
    s, metadata, proof = case()
    old = assumed_qualification(metadata, proof, s.trusted_issuer)
    revoked = change(metadata, authority_version="revoked", consent=ConsentStatus.DENIED)
    observation = observe(revoked, proof, trusted_issuer=s.trusted_issuer, qualification=old)
    assert observation.view.outcome != "ALLOW"
    assert observation.evaluation.qualification_issuer is None


def test_unknown_operation_and_unsafe_model_copy_are_not_accepted():
    _, metadata, proof = case()
    with pytest.raises(ValueError, match="unsupported_operation"):
        assemble(change(metadata, context=change(metadata.context, operation="MONITOR")), proof)
    with pytest.raises(ValidationError):
        assemble(metadata.model_copy(update={"schema_version": True}), proof)
