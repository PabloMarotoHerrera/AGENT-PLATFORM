"""Independent expected invariants on explicitly synthetic graphs/authority."""

import pytest

from hermes_cli.agent_platform.harness.contracts import ContentRef, ContractRef, Effect
from hermes_cli.agent_platform.harness.validation_dag import (
    AcceptanceCriterion, EvidenceDependency, EvidenceProducer, SyntheticAuthorityAssumption,
    ValidationBoundary, ValidationContext, ValidationDAG, ValidationObservation, ValidationRequirement,
)
from hermes_cli.agent_platform.harness.validation_dag_verifier import POLICY, assess, verify


def ref(name, version=1):
    return ContractRef(contract_id=name, version=version)


def content(name="synthetic-source", char="a"):
    return ContentRef(content_id=name, sha256=char * 64)


def change(value, **updates):
    return type(value).model_validate({**value.model_dump(), **updates})


CONTEXT = ValidationContext(current_ticket="predecessor", successor_ticket="successor",
    execution_target="predecessor", human_decision_target="predecessor", revision="R2", run="run45")
ASSUMPTION = SyntheticAuthorityAssumption(owner=content("synthetic-owner"),
    scope="ISOLATED_SYNTHETIC_TEST_ONLY", provenance=content("fixture-only"))


def fixture(kind="ALL_PASSED"):
    human = kind != "ALL_PASSED"
    condition = "RECORDED" if kind == "FAILURE_CLASSIFICATION" else "PASSED"
    criterion = AcceptanceCriterion(criterion=ref("criterion"), kind=kind, required_facts=(condition,),
        authority_class="HUMAN" if human else "NONE", machine_evaluable=not human, human_decision_required=human)
    requirement = ValidationRequirement(requirement=ref("requirement"), category="CLASSIFICATION" if human else "COMMAND",
        criterion=criterion.criterion, expects=(ref("result"),), context=CONTEXT, human_authority=human)
    producer = EvidenceProducer(producer=ref("runner"), output=ref("result"), effect=Effect.COMPUTE, qualification="QUALIFIED")
    dep = EvidenceDependency(dependency_id="edge", consumer=requirement.requirement, producer=producer.producer,
        evidence=producer.output, expected_source=content(), condition=condition,
        failure_behavior="EXPOSE_HUMAN_CLASSIFICATION" if kind == "FAILURE_CLASSIFICATION" else "BLOCK")
    return ValidationDAG(graph=ref("synthetic-validation"), policy=POLICY, requirements=(requirement,),
        producers=(producer,), dependencies=(dep,), criteria=(criterion,),
        boundaries=(ValidationBoundary(producer=ref("human"), output=ref("human-decision"), kind="HUMAN", provenance=content("human-source")),))


def observation(status="PASSED"):
    return ValidationObservation(evidence=ref("result"), artifact=content("result-bytes"), producer=ref("runner"),
        source=content(), context=CONTEXT, status=status, outcome=status if status in {"PASSED", "FAILED"} else "UNKNOWN",
        qualification="SYNTHETIC_ASSUMPTION", owner=ASSUMPTION.owner)


def decision(o, **updates):
    value = ValidationObservation(evidence=ref("human-decision"), artifact=content("decision-bytes"), producer=ref("human"),
        source=content("human-source"), context=CONTEXT, status="PASSED", outcome="PASSED", qualification="SYNTHETIC_ASSUMPTION",
        owner=ASSUMPTION.owner, authority_class="HUMAN", human_decision="APPROVED", decision_for=ref("requirement"), binds_evidence=(o.identity(),))
    return change(value, **updates)


def assess_one(g=None, obs=None, **kwargs):
    return assess(g or fixture(), obs if obs is not None else (observation(),), **kwargs)[0]


def codes(g):
    return {d.code for d in verify(g).diagnostics}


def test_acyclic_graph_is_structural_not_authority():
    report = verify(fixture())
    assert report.structurally_valid and not report.grants_authority and report.observational
    assert report.topological_order.index("P:runner:1") < report.topological_order.index("R:requirement:1")


def test_cycle_has_real_bounded_witness():
    g = fixture()
    g = change(g, producers=(change(g.producers[0], requires=(ref("requirement"),)),))
    report = verify(g)
    assert "dependency_cycle" in codes(g)
    assert report.cycle_witnesses[0][0] == report.cycle_witnesses[0][-1]
    assert len(report.cycle_witnesses) == 1


def test_multiple_requirement_cycle():
    g = fixture()
    r2 = change(g.requirements[0], requirement=ref("second"), expects=(ref("second-result"),))
    p1 = change(g.producers[0], requires=(r2.requirement,))
    p2 = change(p1, producer=ref("second-runner"), output=ref("second-result"), requires=(ref("requirement"),))
    d2 = change(g.dependencies[0], dependency_id="edge2", consumer=r2.requirement, producer=p2.producer, evidence=p2.output)
    report = verify(change(g, requirements=(*g.requirements, r2), producers=(p1,p2), dependencies=(*g.dependencies,d2)))
    assert not report.structurally_valid and len(report.cycle_witnesses[0]) == 5


@pytest.mark.parametrize("mutation,code", [
    ("missing", "missing_internal_producer"), ("version", "producer_version_mismatch"),
    ("criterion", "missing_criterion"), ("duplicate", "duplicate_producer"),
    ("edge", "duplicate_edge"), ("requirement", "duplicate_requirement"),
    ("unreachable", "unreachable_required_evidence"), ("output", "producer_output_mismatch"),
    ("policy", "unsupported_policy"), ("upstream", "missing_producer_prerequisite"),
    ("authority", "authority_classification_conflict"), ("effect", "unbound_effectful_producer"),
])
def test_structural_fail_closed(mutation, code):
    g=fixture()
    updates={
        "missing": {"producers": ()},
        "version": {"producers": (change(g.producers[0], producer=ref("runner",2)),)},
        "criterion": {"criteria": ()}, "duplicate": {"producers": g.producers*2},
        "edge": {"dependencies": g.dependencies*2}, "requirement": {"requirements":g.requirements*2},
        "unreachable": {"dependencies": ()},
        "output": {"producers": (change(g.producers[0], output=ref("other")),)},
        "policy": {"policy": ref(POLICY.contract_id,2)},
        "upstream": {"producers": (change(g.producers[0], requires=(ref("absent"),)),)},
        "authority": {"requirements": (change(g.requirements[0],human_authority=True),)},
        "effect": {"producers": (change(g.producers[0],effect=Effect.WRITE_ARTIFACT),)},
    }
    candidate=change(g,**updates[mutation])
    assert code in codes(candidate)
    assert not assess_one(candidate, synthetic_authority=ASSUMPTION).criterion_satisfied


def test_bound_effect_still_must_match_criterion_effect_policy():
    g=fixture()
    p=change(g.producers[0],effect=Effect.EXTERNAL_WRITE,handler_correspondence=content("proof"),effect_policy=ref("effect-policy"))
    assert "producer_effect_policy_conflict" in codes(change(g,producers=(p,)))


@pytest.mark.parametrize("kind",["EXTERNAL","HUMAN"])
def test_declared_boundary_is_structurally_valid_but_unresolved(kind):
    g=fixture()
    b=ValidationBoundary(producer=ref("runner"),output=ref("result"),kind=kind,provenance=content())
    g=change(g,producers=(),boundaries=(b,))
    assert verify(g).structurally_valid
    a=assess_one(g,())
    assert kind.lower()+"_boundary_unresolved" in a.reason_codes and not a.criterion_satisfied


@pytest.mark.parametrize("status",["ABSENT","PRESENT","FAILED","INVALID","STALE","CONFLICT","UNSUPPORTED","UNAVAILABLE"])
def test_not_passed_is_never_machine_acceptance(status):
    a=assess_one(obs=(observation(status),),synthetic_authority=ASSUMPTION)
    assert not a.criterion_satisfied and not a.accepted and not a.grants_authority


def test_failed_evidence_enables_classification_without_acceptance():
    a=assess_one(fixture("FAILURE_CLASSIFICATION"),(observation("FAILED"),),synthetic_authority=ASSUMPTION)
    assert a.acceptance_readiness=="HUMAN_CLASSIFICATION_REQUIRED"
    assert a.prerequisite_state=="SATISFIED" and not a.criterion_satisfied and not a.accepted


def test_failed_classification_record_is_not_v11_acceptance():
    g=fixture("FAILURE_CLASSIFICATION"); o=observation("FAILED")
    a=assess_one(g,(o,decision(o)),synthetic_authority=ASSUMPTION)
    assert a.criterion_satisfied and a.acceptance_readiness=="HUMAN_DECISION_RECORDED" and not a.accepted
    v11=fixture("HUMAN_ACCEPTANCE")
    assert not assess_one(v11,(o,decision(o)),synthetic_authority=ASSUMPTION).criterion_satisfied


def test_human_only_never_auto_satisfied():
    a=assess_one(fixture("HUMAN_ACCEPTANCE"),synthetic_authority=ASSUMPTION)
    assert a.acceptance_readiness=="HUMAN_DECISION_REQUIRED" and not a.criterion_satisfied


def test_positive_human_record_is_explicit_synthetic_assumption_only():
    o=observation(); g=fixture("HUMAN_ACCEPTANCE")
    assert not assess_one(g,(o,decision(o))).criterion_satisfied
    a=assess_one(g,(o,decision(o)),synthetic_authority=ASSUMPTION)
    assert a.criterion_satisfied and not a.accepted
    assert a.graph==g.identity() and o.identity() in a.observed_evidence
    assert a.qualification_scope=='ISOLATED_SYNTHETIC_TEST_ONLY'
    assert a.synthetic_assumption==ASSUMPTION.provenance


@pytest.mark.parametrize("mutation",["stale","wrong-ticket","wrong-version","historical","rejected","pending","wrong-owner","unqualified","wrong-producer","wrong-source","wrong-target"])
def test_human_replay_or_mismatched_decision_is_rejected(mutation):
    o=observation(); d=decision(o)
    updates={"stale":{"status":"STALE","outcome":"UNKNOWN"},
        "wrong-ticket":{"context":change(CONTEXT,current_ticket="successor")},
        "wrong-version":{"binds_evidence":(change(o,evidence=ref("result",2)).identity(),)},
        "historical":{"historical":True},"rejected":{"human_decision":"REJECTED"},
        "pending":{"human_decision":"PENDING"},"wrong-owner":{"owner":content("other")},
        "unqualified":{"qualification":"UNQUALIFIED"},"wrong-producer":{"producer":ref("runner")},
        "wrong-source":{"source":content("other")},"wrong-target":{"context":change(CONTEXT,human_decision_target="successor")}}
    assert not assess_one(fixture("HUMAN_ACCEPTANCE"),(o,change(d,**updates[mutation])),synthetic_authority=ASSUMPTION).criterion_satisfied


def test_contradictory_evidence_never_selects_convenient_pass():
    a=assess_one(obs=(observation(),observation("FAILED")),synthetic_authority=ASSUMPTION)
    assert "evidence_conflict_requires_human_resolution" in a.reason_codes and not a.criterion_satisfied
    assert a.resolution_authority=='HUMAN_OWNER' and a.required_human_continuation


def test_duplicate_identical_observation_is_idempotent():
    assert assess_one(obs=(observation(),)*2,synthetic_authority=ASSUMPTION).criterion_satisfied


@pytest.mark.parametrize("field,value",[("source",content("changed")),("context",change(CONTEXT,run="new-run")),("producer",ref("runner",2)),("historical",True)])
def test_upstream_binding_change_invalidates(field,value):
    assert not assess_one(obs=(change(observation(),**{field:value}),),synthetic_authority=ASSUMPTION).criterion_satisfied


def test_failed_to_accepted_policy_is_structurally_rejected():
    g=fixture(); d=change(g.dependencies[0],condition="RECORDED")
    assert "failed_to_accepted_policy" in codes(change(g,dependencies=(d,)))


def test_c26_successor_cannot_inherit_predecessor_execution_target():
    o=change(observation(),context=change(CONTEXT,current_ticket="successor",human_decision_target="successor"))
    assert not assess_one(obs=(o,),synthetic_authority=ASSUMPTION).criterion_satisfied
    assert CONTEXT.current_ticket!=CONTEXT.successor_ticket and CONTEXT.execution_target=="predecessor"


def test_observation_bound():
    with pytest.raises(ValueError):
        assess(fixture(),(observation(),)*513)


def reference_graph():
    """Bounded authored first-slice graph; facts are synthetic verification ports.

    Producer completion means evidence production only. Existing effect owners
    and their guards are explicitly external, never executable implementations.
    """
    inventory=(('approved-instructions','INSPECTION'),('terminal','TERMINAL'),
        ('digest','CONSISTENCY'),('command','COMMAND'),('command-evidence','INSPECTION'),
        ('manual-inspection','INSPECTION'),('manual-passed','MANUAL'),('manual-failed','MANUAL'),
        ('classification','CLASSIFICATION'),('successor-identity','IDENTITY'),
        ('material-request','MATERIAL_REVISION'),('reconciliation','RECONCILIATION'),('review','REVIEW'))
    upstream={'command':('terminal','digest','approved-instructions'),
        'command-evidence':('command',),'manual-inspection':('terminal','approved-instructions'),
        'manual-passed':('manual-inspection',),'manual-failed':('manual-inspection',),
        'classification':('command-evidence',),'material-request':('terminal','successor-identity'),
        'reconciliation':('material-request','digest'),
        'review':('terminal','command-evidence','manual-passed')}
    requirements=[]; producers=[]; dependencies=[]; criteria=[]
    for name,category in inventory:
        human=category in {'MANUAL','CLASSIFICATION','REVIEW'}
        c=AcceptanceCriterion(criterion=ref('criterion.'+name),kind='HUMAN_ACCEPTANCE' if human else 'ALL_PASSED',
            required_facts=('PASSED',),authority_class='HUMAN' if human else 'NONE',machine_evaluable=not human,human_decision_required=human)
        r=ValidationRequirement(requirement=ref(name),category=category,criterion=c.criterion,expects=(ref('evidence.'+name),),context=CONTEXT,human_authority=human)
        p=EvidenceProducer(producer=ref('producer.'+name),output=r.expects[0],effect=Effect.OBSERVE,
            requires=tuple(ref(x) for x in upstream.get(name,())),qualification='UNQUALIFIED',historical_source=content('synthetic-owner-port'))
        requirements.append(r); criteria.append(c); producers.append(p)
        dependencies.append(EvidenceDependency(dependency_id='edge.'+name,consumer=r.requirement,producer=p.producer,
            evidence=p.output,expected_source=content(),condition='PASSED'))
    # The graph declares the human and external boundaries, but cannot satisfy them.
    b=ValidationBoundary(producer=ref('external-authority'),output=ref('authority-proof'),kind='EXTERNAL',provenance=content('unresolved-external'))
    external=ValidationRequirement(requirement=ref('external'),category='IDENTITY',criterion=criteria[0].criterion,
        expects=(b.output,),context=CONTEXT)
    requirements.append(external)
    dependencies.append(EvidenceDependency(dependency_id='edge.external',consumer=external.requirement,
        producer=b.producer,evidence=b.output,expected_source=b.provenance,condition='PASSED'))
    return ValidationDAG(graph=ref('synthetic-first-slice'),policy=POLICY,requirements=tuple(requirements),
        producers=tuple(producers),dependencies=tuple(dependencies),criteria=tuple(criteria),
        boundaries=(*fixture().boundaries,b))


def test_reference_graph_domain_and_independent_expected_topology():
    g=reference_graph(); report=verify(g)
    assert report.structurally_valid
    assert (report.requirement_count,report.producer_count,report.boundary_count)==(14,13,2)
    order=report.topological_order
    assert order.index('R:terminal:1')<order.index('P:producer.command:1')<order.index('R:command:1')
    assert order.index('R:command-evidence:1')<order.index('P:producer.review:1')
    assert order.index('R:material-request:1')<order.index('P:producer.reconciliation:1')
    assert all(not a.criterion_satisfied for a in assess(g,()))


def test_upstream_failure_invalidates_even_present_downstream_pass():
    g=fixture()
    r2=change(g.requirements[0],requirement=ref('downstream'),expects=(ref('downstream-result'),))
    p2=change(g.producers[0],producer=ref('downstream-runner'),output=ref('downstream-result'),requires=(ref('requirement'),))
    d2=change(g.dependencies[0],dependency_id='edge2',consumer=r2.requirement,producer=p2.producer,evidence=p2.output)
    g=change(g,requirements=(*g.requirements,r2),producers=(*g.producers,p2),dependencies=(*g.dependencies,d2))
    second=change(observation(),producer=p2.producer,evidence=p2.output)
    result={a.requirement.contract_id:a for a in assess(g,(observation('FAILED'),second),synthetic_authority=ASSUMPTION)}
    assert not result['downstream'].criterion_satisfied
    assert 'upstream_requirement_unsatisfied' in result['downstream'].reason_codes


def test_conflicting_human_decisions_require_resolution():
    o=observation(); d=decision(o)
    a=assess_one(fixture('HUMAN_ACCEPTANCE'),(o,d,change(d,human_decision='REJECTED')),synthetic_authority=ASSUMPTION)
    assert not a.criterion_satisfied and 'conflicting_human_decisions' in a.reason_codes


@pytest.mark.parametrize('qualification',['UNQUALIFIED','UNAVAILABLE','UNSUPPORTED'])
def test_producer_unqualified_or_unavailable(qualification):
    g=fixture(); g=change(g,producers=(change(g.producers[0],qualification=qualification),))
    assert not assess_one(g,synthetic_authority=ASSUMPTION).criterion_satisfied


def test_large_invalid_graph_has_explicit_bounded_diagnostics():
    g=fixture()
    producers=tuple(change(g.producers[0],producer=ref('runner'+str(i)),
        requires=tuple(ref('absent'+str(j)) for j in range(32))) for i in range(128))
    report=verify(change(g,producers=producers))
    assert not report.structurally_valid and report.witness_limit_reached
    assert len(report.diagnostics)==1024
    assert report.diagnostics[-1].code=='diagnostic_bound_hit'
