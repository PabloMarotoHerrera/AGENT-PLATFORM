import pytest

from hermes_cli.agent_platform.harness.contracts import AuthorityCurrentness
from hermes_cli.agent_platform.harness.dependency_identity import PriorPositiveDecision, SyntheticIdentityAssumption
from hermes_cli.agent_platform.harness.invalidation import compare_identities
from tests.hermes_cli.test_har11_dependency_identity import context
from tests.hermes_cli.test_har11_dependency_manifest import change, closure, content, fixture, mutate_content, ref


def compare(m=None,n=None,a=None,b=None,qualified=True,prior=None):
    m=m or fixture();n=n or m;a=a or context(m);b=b or context(n)
    assumption=SyntheticIdentityAssumption(subject=b.identity(),provenance=content('synthetic-currentness-proof'),scope='ISOLATED_SYNTHETIC_TEST_ONLY') if qualified else None
    return compare_identities(a,b,expected_manifest=m,candidate_manifest=n,synthetic_assumption=assumption,prior_positive=prior)


def causes(result):return {f.cause for f in result.findings}


def test_matching_identity_is_not_consent_or_execution():
    r=compare()
    assert causes(r)=={'UNCHANGED'} and r.structurally_compatible
    assert not r.grants_authority and not r.authorizes_execution and r.observational
    assert r.qualification_scope=='ISOLATED_SYNTHETIC_TEST_ONLY'


def test_matching_current_claim_or_actor_name_without_qualification_cannot_allow():
    r=compare(qualified=False)
    assert 'UNKNOWN' in causes(r) and 'UNCHANGED' not in causes(r)
    assert not r.structurally_compatible


@pytest.mark.parametrize('name',['handler-a','helper','parser','policy','instructions'])
def test_direct_transitive_and_consumed_docs_change(name):
    m=fixture();r=compare(m,mutate_content(m,name))
    assert {'IMPLEMENTATION_CHANGED','TRANSITIVE_DEPENDENCY_CHANGED'}<=causes(r)
    assert any('HUMAN_REAUTHORIZATION_REQUIRED' in f.consequences for f in r.findings)


@pytest.mark.parametrize('name',['parser','policy'])
def test_each_declared_shared_dependent_is_invalidated(name):
    m=fixture();n=mutate_content(m,name)
    for cap in ['cap-a','cap-b']:
        r=compare(m,n,context(m,cap),context(n,cap))
        assert 'TRANSITIVE_DEPENDENCY_CHANGED' in causes(r)
        assert all(f.affected_capabilities==(ref(cap),) for f in r.findings)


def test_unrelated_presentation_change_under_verified_policy_keeps_semantic_implementation():
    m=fixture();n=mutate_content(m,'display')
    assert causes(compare(m,n))=={'UNCHANGED'}


def test_broad_fingerprint_cannot_be_replaced_by_narrow_hash():
    m=fixture(True);n=change(m,capabilities=tuple(change(c,source_mode='NARROW_TRANSITIVE',broad_source=None) for c in m.capabilities))
    r=compare(m,n)
    assert {'DEPENDENCY_CLOSURE_INCOMPLETE','BROAD_FINGERPRINT_REQUIRED'}<=causes(r)
    assert 'UNCHANGED' not in causes(r)


def test_broad_fingerprint_and_display_change_require_new_evidence():
    m=fixture(True);n=mutate_content(m,'display')
    assert 'TRANSITIVE_DEPENDENCY_CHANGED' in causes(compare(m,n))
    n=change(m,capabilities=tuple(change(c,broad_source=content('whole-tree','b')) for c in m.capabilities))
    assert 'BROAD_FINGERPRINT_REQUIRED' in causes(compare(m,n))


@pytest.mark.parametrize('field,cause',[('intent','INTENT_CHANGED'),('authority','AUTHORITY_BINDING_CHANGED'),('resource','RESOURCE_BINDING_CHANGED')])
def test_independent_identity_changes(field,cause):
    a=context();b=change(a,**{field:change(getattr(a,field),content=content('changed'))})
    assert cause in causes(compare(a=a,b=b))


def test_input_version_change_requires_new_evidence_even_with_identical_implementation():
    a=context();b=change(a,validation_inputs=(change(a.validation_inputs[0],source_contract=ref('validation-data.schema',2)),))
    r=compare(a=a,b=b)
    assert causes(r)=={'VALIDATION_INPUT_CHANGED'} and a.implementation==b.implementation
    assert r.findings[0].consequences==('FRESH_EVIDENCE_REQUIRED',)


def test_historical_binding_and_policy_change_all_causes_preserved():
    a=context();b=change(a,intent=change(a.intent,content=content('new-intent')),historical_source=content('old-record'),
        policy=ref('harness-dependency-identity',2),required_human_decision=content('new-human-decision'))
    r=compare(a=a,b=b)
    assert {'INTENT_CHANGED','POLICY_CHANGED','HISTORICAL_SOURCE_CHANGED','AUTHORITY_BINDING_CHANGED','UNSUPPORTED_VERSION','CONFLICT'}<=causes(r)
    assert [f.cause for f in r.findings]==sorted(causes(r))


@pytest.mark.parametrize('change_kind',['source','input','resource','historical'])
def test_prior_allow_not_reusable_after_drift(change_kind):
    m=fixture();a=context(m);prior=PriorPositiveDecision(subject=a.identity(),decision=content('prior-allow'),claim='ALLOW',issuer='human-looking-name')
    n=mutate_content(m,'parser') if change_kind=='source' else m;b=context(n)
    if change_kind=='input':b=change(b,validation_inputs=(change(b.validation_inputs[0],content=content('new-data')),))
    elif change_kind=='resource':b=change(b,scope=change(b.scope,resource_ids=('resource-b',)))
    elif change_kind=='historical':b=change(b,historical_source=content('new-historical-source'))
    r=compare(m,n,a,b,prior=prior)
    assert r.prior_positive_identity_matches is False and not r.authorizes_execution


def test_prior_allow_with_forged_unchanged_context_cannot_hide_manifest_drift():
    m=fixture();a=context(m);n=mutate_content(m,'parser')
    prior=PriorPositiveDecision(subject=a.identity(),decision=content(),claim='ALLOW',issuer='actor')
    r=compare(m,n,a,a,prior=prior)
    assert not r.prior_positive_identity_matches and 'CONFLICT' in causes(r)


@pytest.mark.parametrize('discovery',['PARTIAL','UNKNOWN_DYNAMIC','BROAD_REQUIRED'])
def test_partial_closure_never_unchanged(discovery):
    m=fixture();n=change(m,assumption=None,inventory=change(m.inventory,discovery=discovery))
    r=compare(m,n)
    assert 'DEPENDENCY_CLOSURE_INCOMPLETE' in causes(r) and 'UNCHANGED' not in causes(r)


@pytest.mark.parametrize('state',[AuthorityCurrentness.UNVERIFIED,AuthorityCurrentness.HISTORICAL,AuthorityCurrentness.SUPERSEDED,AuthorityCurrentness.CONFLICT])
def test_unknown_or_stale_currentness_fails_safely(state):
    b=change(context(),currentness=state)
    assert 'UNKNOWN' in causes(compare(b=b))


def test_c26_rejected_successor_does_not_inherit_predecessor_identity():
    a=context();b=change(a,workflow_context=change(a.workflow_context,current_ticket='successor',human_decision_target='successor'))
    assert 'RESOURCE_BINDING_CHANGED' in causes(compare(a=a,b=b))


def test_wrong_expected_dependency_version_is_unsupported():
    a=context();b=change(a,expected_versions=(ref('parser',2),))
    assert 'UNSUPPORTED_VERSION' in causes(compare(a=a,b=b))


@pytest.mark.parametrize('kind,cause',[('VALIDATION_INPUT','VALIDATION_INPUT_CHANGED'),('EVIDENCE_SCHEMA','VALIDATION_INPUT_CHANGED'),
    ('RESOURCE_SCOPE','RESOURCE_BINDING_CHANGED'),('HISTORICAL_CONTRACT','HISTORICAL_SOURCE_CHANGED')])
def test_dependency_kind_preserves_specific_change_cause(kind,cause):
    m=mutate_content(fixture(),'helper',kind=kind);n=mutate_content(m,'helper')
    # Change the content again; mutation helper uses a fixed b digest.
    node=next(x for x in n.nodes if x.node==ref('helper'))
    from tests.hermes_cli.test_har11_dependency_manifest import qualify
    changed=change(node,content=content('helper','c'))
    n=qualify(change(n,nodes=tuple(changed if x.node==ref('helper') else x for x in n.nodes),
        inventory=change(n.inventory,facts=tuple(change(f,node=changed) if f.node.node==ref('helper') else f for f in n.inventory.facts))))
    assert cause in causes(compare(m,n))


def test_stale_synthetic_currentness_proof_is_not_transferred():
    from hermes_cli.agent_platform.harness.invalidation import compare_identities
    m=fixture();a=context(m);n=mutate_content(m,'parser');b=context(n)
    old=SyntheticIdentityAssumption(subject=a.identity(),provenance=content(),scope='ISOLATED_SYNTHETIC_TEST_ONLY')
    r=compare_identities(a,b,expected_manifest=m,candidate_manifest=n,synthetic_assumption=old)
    assert 'UNKNOWN' in causes(r) and r.qualification_scope=='UNQUALIFIED'
