"""Independent comparison expectations and explicit provenance; no source probes."""

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness.contracts import ContinuationKind, Effect, ContentRef
from hermes_cli.agent_platform.harness.admissibility import ConsentStatus
from hermes_cli.agent_platform.harness.shadow import (
    Category, CorpusReport, HarnessObservation, LegacyObservation, Provenance, PublicAction, compare, identity,
)
from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract, sha256_bytes
from hermes_cli.agent_platform.pre_review_reference_model import build_synthetic_reference_model
from hermes_cli.agent_platform.shadow_adapters import ADAPTER, observe
from tests.hermes_cli.test_har08_coverage import fixture, content, ref
from tests.hermes_cli.test_har09_shadow_adapters import case, expected_legacy, assumed_qualification, change


def positive_pair():
    s, m, b = case()
    return expected_legacy(s, m), observe(m, b, trusted_issuer=s.trusted_issuer,
        qualification=assumed_qualification(m, b, s.trusted_issuer))


def corpus():
    model = build_synthetic_reference_model(fixture())
    comparisons = []
    names = []
    for s in model.scenarios:
        _, m, proof = case(s.scenario_id)
        legacy = expected_legacy(s, m)
        observed = observe(m, proof, trusted_issuer=s.trusted_issuer, qualification=s.qualification)
        comparisons.append(compare(legacy, observed))
        names.append(s.scenario_id)
    a, b = positive_pair()
    # Missing owner under otherwise positive legacy claims is a gap, never parity.
    _, m, proof = case()
    comparisons.append(compare(a, observe(m, proof)))
    names.append("missing-owner-current-claim")
    for name, kind in (("RESOLVE_EXECUTION_AUTHORITY", ContinuationKind.SAFE_STOP),
            ("RESOLVE_REVIEW_BLOCKER", ContinuationKind.EXTERNAL_REMEDIATION)):
        action = PublicAction(id="RESOLVE_SYN_1_" + name.removeprefix("RESOLVE_"), label="Diagnostic",
            target_ticket_id="SYN-1", executable=False, read_only=True)
        v = change(a.view, operation=name, capability=None, policy=ref("diagnostic-policy"),
            outcome="SAFE_STOP", continuation=kind, action=action, execution_target=None, effect=Effect.OBSERVE)
        la = change(a, view=v, provenance=Provenance.STATIC)
        hb = change(b, view=v, evaluation=None, admission_input=None, correspondence=None)
        comparisons.append(compare(la, hb)); names.append(name)
    for name in ("MONITOR", "START"):
        v = change(a.view, operation=name, capability=None, mapping="UNSUPPORTED", action=None,
            outcome="UNKNOWN", continuation=ContinuationKind.SAFE_STOP, execution_target=None)
        comparisons.append(compare(change(a, view=v), change(b, view=v, evaluation=None,
            admission_input=None, correspondence=None)))
        names.append("unsupported-" + name)
    # C26's separate successor decision must survive, with and without an active predecessor.
    for active in (True, False):
        successor = PublicAction(id="REVISE_SYN_2", label="Separate successor decision", target_ticket_id="SYN-2")
        v = change(a.view, current_ticket_id="SYN-1" if active else None,
            next_ticket_id="SYN-2", separate_successor=successor, active_execution=active)
        comparisons.append(compare(change(a, view=v, provenance=Provenance.HISTORICAL), change(b, view=v)))
        names.append("c26-separate-successor-active" if active else "c26-separate-successor-inactive")
    corpus_identity = ContentRef(content_id="har09-isolated-corpus", sha256=sha256_bytes(
        ("har09-corpus-inputs-v1\0" + "\n".join(name + ":" + c.legacy.sha256 + ":" + c.harness.sha256
            for name, c in zip(names, comparisons))).encode("utf-8")))
    return CorpusReport(corpus=corpus_identity, adapter=ADAPTER, catalog=model.coverage.catalog_content,
        comparisons=tuple(comparisons), scenario_ids=tuple(names),
        unresolved_producers=("trusted_currentness_owner", "qualified_guard_owner"),
        limitations=("synthetic_qualification_not_operational", "bounded_corpus_only", "no_live_currentness"))


def test_corpus_deterministic_roundtrip_and_provenance():
    report = corpus()
    assert len(report.comparisons) >= 40 and not report.operationally_qualified and not report.truncated
    assert report.content_identity() == corpus().content_identity()
    assert parse_contract(CorpusReport, canonical_json(report)).content_identity() == report.content_identity()
    assert sum(report.counts().values()) == len(report.comparisons)
    assert report.counts()["UNEXPLAINED_DIFFERENCE"] == 0
    assert all(c.category != Category.PARITY for c in report.comparisons if c.unobservable)
    assert {c.provenance for c in report.comparisons} == {Provenance.SYNTHETIC, Provenance.STATIC, Provenance.HISTORICAL}


@pytest.mark.parametrize("field,value,category", [
    ("target_ticket_id", "OTHER", Category.TARGET_IDENTITY_MISMATCH),
    ("decision_target", "OTHER", Category.TARGET_IDENTITY_MISMATCH),
    ("execution_target", "OTHER", Category.TARGET_IDENTITY_MISMATCH),
    ("current_ticket_id", "OTHER", Category.STATE_PRECEDENCE_MISMATCH),
    ("effect", Effect.OBSERVE, Category.EFFECT_CLASSIFICATION_MISMATCH),
    ("policy", ref("wrong-policy"), Category.POLICY_SEMANTIC_MISMATCH),
    ("consent", ConsentStatus.DENIED, Category.AUTHORITY_SEMANTIC_MISMATCH),
    ("active_execution", True, Category.STATE_PRECEDENCE_MISMATCH),
    ("source_version", content("drift", "b"), Category.AUTHORITY_SEMANTIC_MISMATCH),
])
def test_critical_disagreements_never_hidden_as_parity(field, value, category):
    a, b = positive_pair()
    result = compare(change(a, view=change(a.view, **{field: value})), b)
    assert result.category == category and result.severity == "SAFETY_CRITICAL"


@pytest.mark.parametrize("field,value", [("id", "WRONG_ACTION"), ("required_human_action", "wrong-human-action"),
    ("executable", False), ("read_only", True), ("target_ticket_id", "OTHER")])
def test_public_field_correspondence_is_exact(field, value):
    a, b = positive_pair()
    result = compare(change(a, view=change(a.view, action=change(a.view.action, **{field: value}))), b)
    assert result.category == Category.PUBLIC_MAPPING_MISMATCH and result.severity == "SAFETY_CRITICAL"


def test_absent_null_false_are_different_and_never_normalized():
    a, b = positive_pair()
    for value in (None, False):
        action = a.view.action.model_copy(update={"executable": value})
        assert "executable" in action.fields()
        assert compare(change(a, view=change(a.view, action=action)), b).category == Category.PUBLIC_MAPPING_MISMATCH


def test_observation_identity_binds_optional_field_presence():
    a, _ = positive_pair()
    explicit_null = change(a, view=change(a.view, action=change(a.view.action, executable=None)))
    assert canonical_json(a) == canonical_json(explicit_null)
    assert identity("legacy-observation", a) != identity("legacy-observation", explicit_null)


def test_missing_owner_is_gap_but_wrong_target_still_critical():
    s, m, proof = case()
    a = expected_legacy(s, m); b = observe(m, proof)
    assert compare(a, b).category == Category.EXPECTED_QUALIFICATION_GAP
    assert compare(change(a, view=change(a.view, target_ticket_id="OTHER")), b).category == Category.TARGET_IDENTITY_MISMATCH


@pytest.mark.parametrize("field,value", [("id", "WRONG_ACTION"),
    ("required_human_action", "wrong-human-action"), ("executable", True), ("read_only", False)])
def test_missing_owner_does_not_hide_a_wrong_legacy_candidate(field, value):
    s, metadata, proof = case()
    a = expected_legacy(s, metadata)
    b = observe(metadata, proof)
    wrong = change(a, view=change(a.view, action=change(a.view.action, **{field: value})))
    result = compare(wrong, b)
    assert result.category == Category.PUBLIC_MAPPING_MISMATCH
    assert result.severity == "SAFETY_CRITICAL"


def test_forged_executable_c94_without_owner_is_invalid():
    s, m, proof = case()
    a = expected_legacy(s, m); b = observe(m, proof)
    forged = change(b, view=change(b.view, action=PublicAction.model_validate(m.context.action.public_fields() | {"executable": True})))
    assert compare(a, forged).category == Category.SHADOW_EVALUATION_INVALID


def test_replayed_allow_and_missing_legacy_evidence_are_explicit():
    a, b = positive_pair()
    revoked = change(b.admission_input, authority_version="revoked")
    assert compare(a, change(b, admission_input=revoked)).category == Category.SHADOW_EVALUATION_INVALID
    assert compare(change(a, valid=False), b).category == Category.LEGACY_OBSERVATION_INVALID
    assert compare(change(a, unobservable=("legacy_guard",)), b).category == Category.INSUFFICIENT_EVIDENCE
    assert compare(change(a, evidence=(content(),)), b).category == Category.INSUFFICIENT_EVIDENCE


@pytest.mark.parametrize("name", ["RESOLVE_EXECUTION_AUTHORITY", "RESOLVE_REVIEW_BLOCKER"])
def test_diagnostics_can_never_have_executable_binding(name):
    a, b = positive_pair()
    v = change(a.view, operation=name, capability=None, action=change(a.view.action, executable=True))
    forged = change(b, view=v, evaluation=None, admission_input=None)
    assert compare(change(a, view=v), forged).category == Category.SHADOW_EVALUATION_INVALID


def test_report_bounds_and_unsafe_copies_rejected():
    report = corpus()
    with pytest.raises(ValidationError): change(report, scenario_ids=report.scenario_ids[:-1])
    with pytest.raises(ValidationError): change(report, comparisons=report.comparisons * 10)
    with pytest.raises(ValidationError): compare(positive_pair()[0].model_copy(update={"schema_version": True}), positive_pair()[1])
