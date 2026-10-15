"""Behavior tests using synthetic declarations/proofs, never source-file reads."""

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.handler_correspondence import BindingEvidence, BindingStatus
from hermes_cli.agent_platform.harness.contracts import ContentRef, ContinuationKind, ContractRef, Effect
from hermes_cli.agent_platform.harness.coverage import (
    EvidenceSeed, ExplorationBounds, ProducerKind, RequirementConflict, verify_coverage,
)
from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract
from hermes_cli.agent_platform.pre_review_catalog import product_operations
from hermes_cli.agent_platform.pre_review_reference_model import build_first_slice


def ref(name, version=1):
    return ContractRef(contract_id=name, version=version)


def content(name="synthetic-investigation", char="a"):
    return ContentRef(content_id=name, sha256=char * 64)


def change(instance, **updates):
    return type(instance).model_validate({**instance.model_dump(), **updates})


def bindings_fixture():
    return tuple(BindingEvidence(declaration=o.handler, status=BindingStatus.VERIFIED,
        reason_code="synthetic_static_correspondence", source=content("synthetic-source"),
        registry_import_line=1, registration_line=3, handler_line=2,
        handler_ast_sha256="b" * 64, registration_ast_sha256="c" * 64) for o in product_operations())


def fixture(assumptions=True):
    return build_first_slice(bindings_fixture(), content(), synthetic_assumptions=assumptions)


def operation(model, name):
    return next(o for o in model.operations if o.capability == ref(name))


def evidence(model, name):
    return next(e for e in model.evidence if e.evidence == ref(name))


def with_operation(model, name, **updates):
    old = operation(model, name)
    return change(model, operations=tuple(change(o, **updates) if o == old else o for o in model.operations))


def with_evidence(model, name, **updates):
    old = evidence(model, name)
    return change(model, evidence=tuple(change(e, **updates) if e == old else e for e in model.evidence))


def codes(report):
    return {i.code for i in report.issues}


def reachable(report, name):
    return next(o.reachable for o in report.operations if o.capability == ref(name))


def test_complete_model_is_conditional_not_current_authority():
    model = fixture()
    report = verify_coverage(model)
    assert report.classification == "COVERED_WITH_EXTERNAL_ASSUMPTIONS" and report.complete
    assert all(o.reachable for o in report.operations)
    assert set(o.capability for o in model.operations) == {o.capability.capability for o in product_operations()}
    assert report.catalog == model.catalog.content_identity()
    assert report.boundary_count == len(model.boundaries)
    assert report.assumptions and not any(i.classification == "INVALID" for i in report.issues)
    assert all(b.assumed_available for b in model.boundaries)
    assert "recovery_not_implemented" in codes(report)
    assert parse_contract(type(report), canonical_json(report)).content_identity() == report.content_identity()


def test_default_external_and_human_sources_are_not_satisfied():
    model = fixture(False)
    report = verify_coverage(model)
    assert report.classification == "INCOMPLETE"
    assert not any(o.reachable for o in report.operations)
    assert "external_boundary_unqualified" in codes(report)
    assert {b.kind for b in model.boundaries} == {ProducerKind.EXTERNAL_PRODUCER, ProducerKind.HUMAN_PRODUCER}
    assert report.unresolved_count > 0


@pytest.mark.parametrize("status", [None, "ABSENT", "AMBIGUOUS", "CONTRADICTORY", "UNVERIFIABLE"])
def test_missing_or_ambiguous_executor_is_invalid(status):
    model = fixture()
    correspondence = operation(model, "O02").correspondence
    model = with_operation(model, "O02", correspondence=None if status is None else change(correspondence, status=status))
    report = verify_coverage(model)
    assert "executor_correspondence_missing" in codes(report)
    assert report.classification == "INVALID" and not reachable(report, "O02")


@pytest.mark.parametrize("case,code", [("policy", "policy_not_applicable"), ("effect", "declaration_effect_or_identity_conflict"),
    ("authority", "authority_requirements_weakened"), ("prerequisite", "policy_prerequisite_missing"),
    ("transition", "exact_declaration_missing"), ("adapter", "executor_identity_mismatch"),
    ("unsupported", "policy_requirement_unsupported")])
def test_policy_and_exact_declaration_relationships(case, code):
    model = fixture()
    op = operation(model, "O02")
    updates = {}
    if case == "policy":
        updates["policy"] = change(op.policy, policy=ref(op.policy.policy.contract_id, 2))
    elif case == "effect":
        updates["policy"] = change(op.policy, effect=Effect.OBSERVE)
    elif case == "authority":
        updates["policy"] = change(op.policy, required_authority_kinds=(), consent_kind=None)
    elif case == "prerequisite":
        updates["requires"] = ()
    elif case == "transition":
        updates["transition"] = ref(op.transition.contract_id, 2)
    elif case == "adapter":
        updates["correspondence"] = change(op.correspondence, adapter=ref("other-adapter"))
    else:
        updates["policy"] = change(op.policy, unsupported_requirements=(ref("unknown-rule"),))
    assert code in codes(verify_coverage(with_operation(model, "O02", **updates)))
    if case == "unsupported":
        assert not reachable(verify_coverage(with_operation(model, "O02", **updates)), "O02")


@pytest.mark.parametrize("case,code", [("missing", "producer_missing"), ("unknown-operation", "producer_operation_missing"),
    ("version", "producer_version_unsupported"), ("contract", "producer_contract_invalid"),
    ("source-contract", "producer_source_contract_invalid"), ("unresolved", "producer_unresolved"),
    ("invalid", "producer_contract_invalid"), ("provenance", "producer_provenance_missing")])
def test_missing_invalid_or_unsupported_producer(case, code):
    model = fixture()
    node = evidence(model, "command-plan")
    provider = node.providers[0]
    updates = {
        "unknown-operation": {"operation": ref("not-declared")}, "version": {"producer": ref("future-producer", 2)},
        "contract": {"output": ref("wrong-output")}, "source-contract": {"source_contract": ref("wrong-source-contract")},
        "unresolved": {"kind": ProducerKind.UNRESOLVED}, "invalid": {"kind": ProducerKind.INVALID}, "provenance": {"provenance": ()},
    }
    providers = () if case == "missing" else (change(provider, **updates[case]),)
    report = verify_coverage(with_evidence(model, "command-plan", providers=providers))
    assert code in codes(report) and not reachable(report, "O02")


def test_internal_producer_unreachable_from_external_or_impossible_prerequisite():
    model = fixture()
    boundary = next(b for b in model.boundaries if b.boundary == ref("boundary.preliminary-manual-evidence"))
    blocked = change(model, boundaries=tuple(change(b, assumed_available=False) if b == boundary else b for b in model.boundaries))
    report = verify_coverage(blocked)
    assert "internal_producer_unreachable" in codes(report) and not reachable(report, "O02")
    assert any(i.subject == ref("command-plan") and i.code == "internal_producer_unreachable" for i in report.issues)
    op = operation(model, "O01")
    impossible = with_operation(model, "O01", requires=op.requires + (ref("no-producer"),))
    assert "prerequisite_undeclared" in codes(verify_coverage(impossible))
    assert not reachable(verify_coverage(impossible), "O02")


def cycle_model():
    model = fixture()
    op = operation(model, "O01")
    return with_operation(model, "O01", requires=op.requires + (ref("command-result"),))


def test_cycle_witness_and_qualified_seed_are_distinct():
    model = cycle_model()
    report = verify_coverage(model)
    assert "prerequisite_cycle" in codes(report)
    assert any({ref("O01"), ref("O02")} <= set(cycle) for cycle in report.cycles)
    assert not reachable(report, "O02")
    seeded = change(model, initial_evidence=(EvidenceSeed(evidence=ref("command-plan"),
        provenance=content("qualified-initial-plan"), assumption="explicit-current-plan-seed"),))
    report = verify_coverage(seeded)
    assert "cycle_seeded_or_alternative" in codes(report)
    assert "prerequisite_cycle" not in codes(report) and reachable(report, "O02")
    assert report.cycles and report.assumptions


def test_or_alternatives_are_not_and_and_unique_ownership_is_checked():
    model = fixture()
    node = evidence(model, "command-plan")
    other = operation(model, "P03.workflow")
    cap = model.catalog.resolve_capability(other.capability).capability
    alternative = change(node.providers[0], producer=ref("explicit-alternative"), operation=other.capability,
        source_contract=cap.evidence_contract, projection=ref("explicit-plan-view"))
    model = with_evidence(model, "command-plan", providers=node.providers + (alternative,))
    broken = with_operation(model, "O01", correspondence=None)
    assert reachable(verify_coverage(broken), "O02")
    unique = with_evidence(model, "command-plan", ownership="UNIQUE")
    assert "producer_ownership_ambiguous" in codes(verify_coverage(unique))
    assert not reachable(verify_coverage(unique), "O02")


def test_policy_allow_continuation_cannot_be_omitted():
    model = fixture()
    report = verify_coverage(with_operation(model, "O02", continuation_kinds=(ContinuationKind.HUMAN_DECISION, ContinuationKind.SAFE_STOP)))
    assert "continuation_policy_mismatch" in codes(report) and not reachable(report, "O02")


def test_unmapped_manual_attestation_keeps_human_boundary():
    model = fixture()
    for name in ("P02.passed", "P02.failed"):
        action = next(a for a in model.actions if a.capability == ref(name))
        assert action.mapping == "UNMAPPED" and action.kind == ContinuationKind.HUMAN_DECISION
        assert not action.invocable and action.correspondence is None


def test_contradictory_and_requirements_block_producer_and_consumer():
    model = fixture()
    conflict = RequirementConflict(left=ref("approved-publication"), right=ref("current-workpacket"), provenance=content())
    report = verify_coverage(change(model, conflicts=(conflict,)))
    assert "contradictory_prerequisites" in codes(report)
    assert not reachable(report, "O01") and not reachable(report, "O02")


def test_authority_and_consent_producer_edges_cannot_be_omitted_or_automated():
    model = fixture()
    report = verify_coverage(with_operation(model, "O02", authority_requirements=()))
    assert "authority_producer_mapping_missing" in codes(report)
    op = operation(model, "O02")
    mappings = tuple(change(a, human=False) if a.kind == op.policy.consent_kind else a for a in op.authority_requirements)
    assert "consent_producer_not_human" in codes(verify_coverage(with_operation(model, "O02", authority_requirements=mappings)))


def test_invalidated_evidence_is_neither_seeded_nor_automatically_current():
    model = fixture()
    seed = EvidenceSeed(evidence=ref("command-result"), provenance=content(), assumption="old-command-result")
    invalidated = change(model, initial_evidence=(seed,), invalidated=(ref("command-result"),))
    report = verify_coverage(invalidated)
    assert ref("command-result") not in report.reachable_evidence
    assert not reachable(report, "P03.prepare")
    assert reachable(verify_coverage(change(invalidated, invalidated=())), "P03.prepare")


def test_observe_only_effect_assumption_does_not_produce_command_results():
    report = verify_coverage(change(fixture(), permitted_effects=(Effect.OBSERVE,)))
    assert not reachable(report, "O02") and ref("command-result") not in report.reachable_evidence


@pytest.mark.parametrize("case", ["diagnostic", "action-capability", "recovery-authority", "invalidation-target", "stale-catalog"])
def test_invalid_action_recovery_and_identity_relationships(case):
    model = fixture()
    if case == "diagnostic":
        model = change(model, actions=tuple(change(a, invocable=True) if a.capability is None else a for a in model.actions))
    elif case == "action-capability":
        model = change(model, actions=(change(model.actions[0], capability=ref("unknown")),) + model.actions[1:])
    elif case == "recovery-authority":
        model = change(model, remediation=(change(model.remediation[0], grants_authority=True),) + model.remediation[1:])
    elif case == "invalidation-target":
        model = change(model, invalidations=(change(model.invalidations[0], evidence=(ref("unknown"),)),))
    else:
        model = change(model, catalog_content=content("stale"))
    assert verify_coverage(model).classification == "INVALID"


@pytest.mark.parametrize("collection", ["operations", "evidence", "boundaries", "actions"])
def test_duplicate_identity_is_rejected_without_order_dependence(collection):
    model = fixture()
    items = getattr(model, collection)
    model = change(model, **{collection: items + items[:1]})
    assert "duplicate_identity" in codes(verify_coverage(model))
    reverse = change(model, **{collection: tuple(reversed(getattr(model, collection)))})
    assert verify_coverage(model).content_identity() == verify_coverage(reverse).content_identity()


def test_graph_report_identity_is_independent_of_set_construction_order():
    model = fixture()
    reverse = change(model, operations=tuple(change(o, requires=tuple(reversed(o.requires))) for o in reversed(model.operations)),
        evidence=tuple(change(e, providers=tuple(reversed(e.providers))) for e in reversed(model.evidence)),
        boundaries=tuple(reversed(model.boundaries)), actions=tuple(reversed(model.actions)))
    assert model.content_identity() == reverse.content_identity()
    assert canonical_json(verify_coverage(model)) == canonical_json(verify_coverage(reverse))


@pytest.mark.parametrize("bounds", [ExplorationBounds(operations=1), ExplorationBounds(evidence=1),
    ExplorationBounds(edges=1), ExplorationBounds(work=1)])
def test_graph_bound_exhaustion_is_explicitly_incomplete(bounds):
    report = verify_coverage(fixture(), bounds)
    assert report.bound_hits and not report.complete
    assert report.classification == "INCOMPLETE"
    assert report.work_used <= bounds.work


def test_unsupported_model_version_and_unsafe_schema_copies():
    model = fixture()
    assert verify_coverage(change(model, model=ref(model.model.contract_id, 2))).classification == "UNSUPPORTED"
    with pytest.raises(ValidationError):
        verify_coverage(model.model_copy(update={"schema_version": True}))
