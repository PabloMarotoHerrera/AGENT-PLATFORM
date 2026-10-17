"""Bounded fixture-only C94 append model; no historical records or owners."""

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness.contracts import ActorRef, AuthorityCurrentness
from hermes_cli.agent_platform.harness.dependency_identity import content_identity
from hermes_cli.agent_platform.harness.journal_protocol import (advance, initial, owner_for, qualify, verify_receipt)
from hermes_cli.agent_platform.harness.operation_journal import (EffectIntent, EffectReceipt,
    ExpectedVersion, FixtureAuthorization, JournalEntry, OperationRequest, UnknownOutcome)
from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract, sha256_bytes
from hermes_cli.agent_platform.isolated_effect_adapter import attempt_for, transition
from hermes_cli.agent_platform.isolated_operation_journal import STORE
from tests.hermes_cli.test_har10_validation_dag_verifier import (
    ASSUMPTION, assess_one, fixture as validation_fixture, observation)
from tests.hermes_cli.test_har11_dependency_identity import context
from tests.hermes_cli.test_har11_dependency_manifest import content, fixture, ref
from tests.hermes_cli.test_har11_invalidation import compare


def change(model, **updates):
    return type(model).model_validate({**model.model_dump(), **updates})


def case():
    m = fixture()
    c = context(m)
    c = change(c, required_human_decision=content('explicit-fixture-human-decision'),
        workflow_context=change(c.workflow_context, current_ticket='fixture-c94', execution_target='fixture-c94',
            human_decision_target='fixture-c94', revision='fixture-r1', run='fixture-run'))
    g = validation_fixture()
    g = change(g, requirements=(change(g.requirements[0], context=c.workflow_context),))
    v = assess_one(g, (change(observation(), context=c.workflow_context),), synthetic_authority=ASSUMPTION)
    expected = ExpectedVersion(store=STORE, aggregate='fixture-authority-head', scope=c.scope, value=0)
    payload = b'{"fixture_only":true,"selected_effect":"C94-exclusive-append","predecessor":"synthetic"}'
    effect = EffectIntent(effect_id='fixture-predecessor-link', operation_id='fixture-c94-append', operation_version=1,
        scope=c.scope, expected=expected, payload=change(content('fake-reconciliation-record'), sha256=sha256_bytes(payload)))
    request = OperationRequest(operation_id=effect.operation_id, operation_version=1,
        actor=ActorRef(actor_id='fixture-operator'), context=c, expected=expected, effect=effect,
        validation_assessment=content_identity('journal-validation-assessment-v1', v),
        qualification='ISOLATED_SYNTHETIC_TEST_ONLY')
    authorization = FixtureAuthorization(request=request.identity(), human_decision=c.required_human_decision,
        identity_assessment=compare(m,m,c,c), validation=v, provenance=content('explicit-fixture-owner-assumption'),
        scope='ISOLATED_SYNTHETIC_TEST_ONLY')
    return request, authorization, payload


def pure_attempted():
    request, q, payload = case(); owner = owner_for(request, 'writer-a');head = initial(request)
    for stage in ('PREPARED','EFFECT_INTENT_RECORDED'):
        head = advance(head, transition(head,stage),owner)
    attempt = attempt_for(request,owner,'attempt-a')
    head = advance(head,transition(head,'EFFECT_ATTEMPTED',attempt=attempt),owner)
    return head,owner,attempt


def test_strict_frozen_roundtrip_and_canonical_identity():
    request,q,_=case()
    assert parse_contract(OperationRequest,canonical_json(request))==request
    assert request.identity()==parse_contract(OperationRequest,canonical_json(request)).identity()
    with pytest.raises(ValidationError):request.operation_version=2
    with pytest.raises(ValidationError):request.effect.scope.project_id='other'
    assert not q.identity_assessment.authorizes_execution and not q.validation.accepted


@pytest.mark.parametrize('patch',[{'schema_version':2},{'schema_version':True},{'operation_version':'1'},
    {'unexpected':True},{'operation_id':'x'*129},{'protocol':ref('harness-operation-journal',2)},
    {'policy':ref('other')},{'operation_version':0}])
def test_request_rejects_unsupported_or_unbounded_contract(patch):
    with pytest.raises(ValidationError):change(case()[0],**patch)


@pytest.mark.parametrize('field',['operation_id','operation_version','scope','expected','adapter'])
def test_request_effect_binding(field):
    r,_,_=case()
    values={'operation_id':'other','operation_version':2,'scope':change(r.context.scope,project_id='other'),
        'expected':change(r.expected,value=1),'adapter':ref('isolated-sqlite-append',2)}
    with pytest.raises(ValidationError):change(r,effect=change(r.effect,**{field:values[field]}))


@pytest.mark.parametrize('stage',['COMPLETED','EFFECT_ATTEMPTED','EFFECT_CONFIRMED','EFFECT_OUTCOME_UNKNOWN'])
def test_initial_cannot_skip_stages(stage):
    r,_,_=case();head=initial(r);owner=owner_for(r,'writer-a')
    with pytest.raises(ValueError):advance(head,transition(head,stage),owner)


@pytest.mark.parametrize('kind',['predecessor','version','owner'])
def test_transition_exact_predecessor_revision_and_owner(kind):
    r,_,_=case();p=initial(r);o=owner_for(r,'writer-a');p=advance(p,transition(p,'PREPARED'),o)
    t=transition(p,'EFFECT_INTENT_RECORDED')
    if kind=='predecessor':t=change(t,previous=content('foreign'))
    elif kind=='version':t=change(t,expected_journal_version=0)
    else:o=owner_for(r,'writer-b')
    with pytest.raises(ValueError):advance(p,t,o)


def test_completion_needs_confirmed_bound_receipt():
    p,o,a=pure_attempted()
    with pytest.raises(ValueError):advance(p,transition(p,'EFFECT_CONFIRMED',attempt=a),o)
    with pytest.raises(ValueError):advance(p,transition(p,'COMPLETED',attempt=a),o)


@pytest.mark.parametrize('field',['effect','operation','resource','project','payload','implementation','authority','inputs','adapter','version','effect-record'])
def test_receipt_cannot_be_substituted(field):
    p,o,a=pure_attempted();r=p.request
    receipt=EffectReceipt(attempt=a,outcome='CONFIRMED',observed=change(r.expected,value=1),effect_record=r.effect.payload)
    if field=='effect':a=change(a,effect=change(a.effect,effect_id='foreign'))
    elif field=='operation':a=change(a,effect=change(a.effect,operation_id='foreign'))
    elif field in {'resource','project'}:
        scope=change(a.effect.scope,**({'project_id':'foreign'} if field=='project' else {'resource_ids':('foreign',)}))
        a=change(a,effect=change(a.effect,scope=scope))
    elif field=='payload':a=change(a,effect=change(a.effect,payload=content('foreign')))
    elif field=='implementation':a=change(a,implementation=content('foreign'))
    elif field=='authority':a=change(a,authority=content('foreign'))
    elif field=='inputs':a=change(a,inputs=(content('foreign'),))
    elif field=='adapter':receipt=change(receipt,adapter=ref('foreign'))
    elif field=='effect-record':receipt=change(receipt,effect_record=content('foreign'))
    else:receipt=change(receipt,observed=change(receipt.observed,value=2))
    receipt=change(receipt,attempt=a)
    with pytest.raises(ValueError):verify_receipt(r,o,receipt)


def test_unknown_has_no_retry_or_automatic_recovery():
    p,o,a=pure_attempted()
    p=advance(p,transition(p,'EFFECT_OUTCOME_UNKNOWN',attempt=a,
        unknown=UnknownOutcome(attempt=a,reason='missing-confirmation')),o)
    assert not p.transition.unknown.retry_allowed
    with pytest.raises(ValueError):advance(p,transition(p,'EFFECT_ATTEMPTED',attempt=a),o)


@pytest.mark.parametrize('defect',['missing','human','history','currentness','identity','validation','source','readiness-only'])
def test_qualification_never_inherits_authority(defect):
    r,q,_=case();observed=r.context
    if defect=='missing':q=None
    elif defect=='human':r=change(r,context=change(r.context,required_human_decision=None))
    elif defect=='history':r=change(r,context=change(r.context,currentness=AuthorityCurrentness.HISTORICAL))
    elif defect=='currentness':r=change(r,context=change(r.context,currentness=AuthorityCurrentness.UNVERIFIED))
    elif defect=='identity':q=change(q,identity_assessment=change(q.identity_assessment,qualification_scope='UNQUALIFIED'))
    elif defect=='validation':q=change(q,validation=change(q.validation,evidence_valid=False))
    elif defect=='source':observed=change(observed,implementation=change(observed.implementation,content=content('new-source')))
    else:q=None  # HAR10 readiness + HAR11 positive observations alone do not permit effects.
    with pytest.raises(ValueError):qualify(r,q,observed)
