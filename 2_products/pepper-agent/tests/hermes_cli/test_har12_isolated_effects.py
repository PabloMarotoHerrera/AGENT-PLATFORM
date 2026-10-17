import pytest

from hermes_cli.agent_platform.harness.journal_protocol import completion
from hermes_cli.agent_platform.harness.operation_journal import EffectReceipt, UnknownOutcome
from hermes_cli.agent_platform.harness.validation import canonical_json
from hermes_cli.agent_platform.isolated_effect_adapter import (IsolatedAppendAdapter, attempt_for, run_fixture, transition)
from hermes_cli.agent_platform.isolated_operation_journal import IsolatedJournal, JournalConflict
from tests.hermes_cli.test_har12_operation_journal import case, change, content
from tests.hermes_cli.test_har11_dependency_manifest import fixture
from tests.hermes_cli.test_har11_invalidation import compare
from tests.hermes_cli.test_har12_journal_store import prepared


def attempted(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path);a=attempt_for(r,o,'first-attempt')
    h=s.move(r.operation_id,o.writer,transition(h,'EFFECT_ATTEMPTED',attempt=a),authorization=q,observed_context=r.context)
    return s,r,q,p,h,o,a


def test_success_has_one_effect_bound_receipt_and_separate_completion(tmp_path):
    r,q,p=case();s=IsolatedJournal.create_disposable(tmp_path);s.initialize_aggregate(r.expected)
    result=run_fixture(s,r,p,writer='writer-a',authorization=q,observed_context=r.context)
    assert result.stage=='COMPLETED' and not result.grants_authority and not result.authorizes_execution
    assert s.reconnect().observe_effect(r.effect.effect_id).identity()==result.receipt
    assert s.effect_count()==1 and s.observe_version(r.expected).value==1
    stages=[e.stage for e in s.trace(r.operation_id)]
    assert stages==['REQUESTED','PREPARED','EFFECT_INTENT_RECORDED','EFFECT_ATTEMPTED','EFFECT_CONFIRMED','COMPLETED']
    again=run_fixture(s,r,p,writer='writer-b',authorization=None,observed_context=r.context)
    assert again==result and s.effect_count()==1


def test_identical_effect_key_is_reused_without_second_compare_or_write(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path);adapter=IsolatedAppendAdapter()
    one=adapter.apply(s,a,p,authorization=q,observed_context=r.context)
    two=adapter.apply(s.reconnect(),a,p,authorization=q,observed_context=r.context)
    assert one==two and s.effect_count()==1 and s.observe_version(r.expected).value==1


def test_stale_version_at_final_effect_boundary_preserves_attempt_and_conflict(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    with s.transaction() as c:c.execute('UPDATE aggregates SET body=?',(canonical_json(change(r.expected,value=1)),))
    with pytest.raises(JournalConflict) as e:IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    assert e.value.report.reason=='pre_effect_version_conflict'
    assert s.effect_count()==0 and s.head(r.operation_id)==h
    assert s.conflicts(r.operation_id)[0].observed.value==1


@pytest.mark.parametrize('defect',['payload','source','authority','human','validation','historical-identity'])
def test_no_effect_on_failed_effect_adjacent_qualification(tmp_path,defect):
    s,r,q,p,h,o,a=attempted(tmp_path);observed=r.context
    if defect=='payload':p=b'changed'
    elif defect=='source':observed=change(observed,implementation=change(observed.implementation,content=content('changed')))
    elif defect=='authority':observed=change(observed,authority=change(observed.authority,content=content('changed')))
    elif defect=='human':q=None
    elif defect=='validation':q=change(q,validation=change(q.validation,criterion_satisfied=False))
    else:q=change(q,identity_assessment=change(q.identity_assessment,qualification_scope='UNQUALIFIED'))
    with pytest.raises(ValueError):IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=observed)
    assert s.effect_count()==0 and s.observe_version(r.expected).value==0


@pytest.mark.parametrize('failure,stage,count',[('before_effect','SAFE_STOP',0),
    ('after_effect','EFFECT_OUTCOME_UNKNOWN',1),('after_receipt','EFFECT_CONFIRMED',1)])
def test_failure_windows_are_not_completed_or_blindly_retried(tmp_path,failure,stage,count):
    r,q,p=case();s=IsolatedJournal.create_disposable(tmp_path);s.initialize_aggregate(r.expected)
    result=run_fixture(s,r,p,writer='writer-a',authorization=q,observed_context=r.context,failure=failure)
    assert result.stage==stage and s.reconnect().effect_count()==count
    repeated=run_fixture(s,r,p,writer='writer-a',authorization=q,observed_context=r.context)
    assert repeated==result and s.effect_count()==count
    if failure=='after_effect':assert s.observe_effect(r.effect.effect_id) is not None and result.receipt is None


def test_attempted_interruption_has_no_implied_absence_or_second_dispatch(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    assert s.observe_effect(r.effect.effect_id) is None
    result=run_fixture(s.reconnect(),r,p,writer=o.writer,authorization=q,observed_context=r.context)
    assert result.stage=='EFFECT_ATTEMPTED' and not s.effect_count()
    with pytest.raises(JournalConflict):s.claim(r.operation_id,'replacement',h.journal_version)


def test_unknown_before_observation_cannot_schedule_any_new_attempt(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    h=s.move(r.operation_id,o.writer,transition(h,'EFFECT_OUTCOME_UNKNOWN',attempt=a,
        unknown=UnknownOutcome(attempt=a,reason='interrupted-unobserved')))
    with pytest.raises(ValueError):
        s.move(r.operation_id,o.writer,transition(h,'EFFECT_ATTEMPTED',attempt=a),authorization=q,observed_context=r.context)
    assert not s.effect_count() and s.head(r.operation_id)==h


def test_self_consistent_fabricated_receipt_is_not_durable_evidence(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    receipt=EffectReceipt(attempt=a,outcome='CONFIRMED',observed=change(r.expected,value=1),effect_record=r.effect.payload)
    with pytest.raises(ValueError):s.move(r.operation_id,o.writer,transition(h,'EFFECT_CONFIRMED',attempt=a,receipt=receipt))
    assert s.head(r.operation_id)==h and not s.effect_count()


def test_confirmed_receipt_cannot_be_moved_to_another_resource(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    receipt=IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    foreign=change(receipt,attempt=change(a,effect=change(a.effect,scope=change(a.effect.scope,project_id='foreign-project'))))
    with pytest.raises(ValueError):s.move(r.operation_id,o.writer,transition(h,'EFFECT_CONFIRMED',attempt=a,receipt=foreign))
    assert s.head(r.operation_id)==h


def test_rejected_effect_receipt_is_durable_but_cannot_complete(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    receipt=IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context,reject=True)
    assert receipt.outcome=='REJECTED' and receipt.effect_record is None and s.observe_version(r.expected).value==0
    h=s.move(r.operation_id,o.writer,transition(h,'EFFECT_REJECTED',attempt=a,receipt=receipt))
    with pytest.raises(ValueError):s.move(r.operation_id,o.writer,transition(h,'COMPLETED',attempt=a,receipt=receipt))
    assert completion(h).stage=='EFFECT_REJECTED'


def test_conflicting_effect_identity_and_cross_project_key_are_not_reused(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    receipt=IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    # A different operation must never receive the first operation's immutable receipt.
    r2=change(r,operation_id='second-operation',effect=change(r.effect,operation_id='second-operation'))
    q2=change(q,request=r2.identity())
    h2=s.request(r2);o2=s.claim(r2.operation_id,'writer-b',h2.journal_version)
    # New expected version would require fresh request/qualification. Keep zero and prove conflict.
    with pytest.raises(JournalConflict):s.move(r2.operation_id,o2.writer,transition(h2,'PREPARED'),authorization=q2,observed_context=r2.context)
    assert s.effect_count()==1 and s.observe_effect(r.effect.effect_id)==receipt


def test_conflicting_duplicate_key_records_typed_conflict(tmp_path):
    s,r,q,p,h,o,a=attempted(tmp_path)
    first=IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    expected=change(r.expected,value=1)
    r2=change(r,operation_id='second-operation',expected=expected,
        effect=change(r.effect,operation_id='second-operation',expected=expected))
    q2=change(q,request=r2.identity());h=s.request(r2);o=s.claim(r2.operation_id,'writer-b',h.journal_version)
    for stage in ('PREPARED','EFFECT_INTENT_RECORDED'):
        h=s.move(r2.operation_id,o.writer,transition(h,stage),authorization=q2,observed_context=r2.context)
    a2=attempt_for(r2,o,'first-attempt')
    h=s.move(r2.operation_id,o.writer,transition(h,'EFFECT_ATTEMPTED',attempt=a2),authorization=q2,observed_context=r2.context)
    with pytest.raises(JournalConflict) as e:IsolatedAppendAdapter().apply(s,a2,p,authorization=q2,observed_context=r2.context)
    assert e.value.report.reason=='conflicting_effect_key'
    assert s.observe_effect(r.effect.effect_id)==first and s.effect_count()==1 and s.observe_version(expected).value==1


def test_racing_effects_use_atomic_local_version_comparison(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    s,r,q,p,h,o,a=attempted(tmp_path)
    r2=change(r,operation_id='second-operation',effect=change(r.effect,effect_id='second-effect',operation_id='second-operation'))
    q2=change(q,request=r2.identity());h2=s.request(r2);o2=s.claim(r2.operation_id,'writer-b',h2.journal_version)
    for stage in ('PREPARED','EFFECT_INTENT_RECORDED'):
        h2=s.move(r2.operation_id,o2.writer,transition(h2,stage),authorization=q2,observed_context=r2.context)
    a2=attempt_for(r2,o2,'first-attempt')
    s.move(r2.operation_id,o2.writer,transition(h2,'EFFECT_ATTEMPTED',attempt=a2),authorization=q2,observed_context=r2.context)
    barrier=Barrier(2)
    def apply(args):
        attempt,auth=args;barrier.wait()
        try:return IsolatedAppendAdapter().apply(s.reconnect(),attempt,p,authorization=auth,observed_context=r.context).outcome
        except JournalConflict:return 'CONFLICT'
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(apply,((a,q),(a2,q2))))
    assert sorted(out)==['CONFIRMED','CONFLICT'] and s.effect_count()==1
    assert s.observe_version(r.expected).value==1


@pytest.mark.parametrize('column,value',[('payload',b'corrupt'),('attempt','{}'),('receipt','{}')])
def test_corrupt_durable_effect_cannot_replay_or_complete(tmp_path,column,value):
    s,r,q,p,h,o,a=attempted(tmp_path)
    IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    with s.transaction() as c:
        # Column selection is a closed fixture list, not external SQL input.
        c.execute('UPDATE effects SET '+column+'=? WHERE id=?',(value,r.effect.effect_id))
    with pytest.raises(ValueError):s.observe_effect(r.effect.effect_id)
    with pytest.raises(ValueError):IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    assert s.effect_count()==1


@pytest.mark.parametrize('field',['project_id','resource_ids'])
def test_effect_key_collision_cannot_cross_scoped_resources(tmp_path,field):
    s,r,q,p,h,o,a=attempted(tmp_path)
    first=IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context)
    scope=change(r.context.scope,**({field:'other-project'} if field=='project_id' else {field:('other-resource',)}))
    ctx=change(r.context,scope=scope);expected=change(r.expected,scope=scope,aggregate='other-aggregate')
    r2=change(r,operation_id='other-operation',context=ctx,expected=expected,
        effect=change(r.effect,operation_id='other-operation',scope=scope,expected=expected))
    m=fixture();q2=change(q,request=r2.identity(),identity_assessment=compare(m,m,ctx,ctx))
    s.initialize_aggregate(expected);h=s.request(r2);o=s.claim(r2.operation_id,'other-writer',h.journal_version)
    for stage in ('PREPARED','EFFECT_INTENT_RECORDED'):
        h=s.move(r2.operation_id,o.writer,transition(h,stage),authorization=q2,observed_context=ctx)
    a2=attempt_for(r2,o,'first-attempt')
    s.move(r2.operation_id,o.writer,transition(h,'EFFECT_ATTEMPTED',attempt=a2),authorization=q2,observed_context=ctx)
    with pytest.raises(JournalConflict):IsolatedAppendAdapter().apply(s,a2,p,authorization=q2,observed_context=ctx)
    assert s.effect_count()==1 and s.observe_version(expected).value==0 and s.observe_effect(r.effect.effect_id)==first
