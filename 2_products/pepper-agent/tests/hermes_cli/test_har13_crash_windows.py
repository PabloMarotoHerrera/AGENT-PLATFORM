import pytest
from tests.hermes_cli.har13_test_helpers import crash,invoke,setup

EXPECTED={
 'W00':('NOT_STARTED',0,'NONE'), 'W01':('PRE_EFFECT_DURABLE',0,'REQUESTED'),
 'W02':('PRE_EFFECT_DURABLE',0,'REQUESTED'), 'W03':('PRE_EFFECT_DURABLE',0,'PREPARED'),
 'W04':('PRE_EFFECT_DURABLE',0,'EFFECT_INTENT_RECORDED'),
 'W05':('ATTEMPT_OUTCOME_UNCERTAIN',0,'EFFECT_ATTEMPTED'),
 'W06':('ATTEMPT_OUTCOME_UNCERTAIN',0,'EFFECT_ATTEMPTED'),
 'W07':('ATTEMPT_OUTCOME_UNCERTAIN',0,'EFFECT_ATTEMPTED'),
 'W08':('EFFECT_CONFIRMED_DURABLE',1,'EFFECT_ATTEMPTED'),
 'W09':('EFFECT_CONFIRMED_DURABLE',1,'EFFECT_CONFIRMED'),
 'W10':('COMPLETED_DURABLE',1,'COMPLETED'), 'W11':('PRE_EFFECT_DURABLE',0,'REQUESTED')}


@pytest.mark.parametrize('window',tuple(EXPECTED))
def test_hard_child_termination_and_independent_restart(tmp_path,window):
    s,r,out=crash(tmp_path,window);state,count,head=EXPECTED[window]
    assert out['assessment']['state']==state
    assert out['effect_count']==count and out['conflict_count']==0
    assert (s.head(r.operation_id).stage if window!='W00' else 'NONE')==head
    assert not out['assessment']['retry_admissible'] and not out['assessment']['takeover_admissible']
    assert not out['assessment']['authorizes_execution']
    if window not in {'W00','W01'}:assert out['assessment']['ownership']=='BOUND_EXITED'
    advice=invoke('replay',s.root)
    assert not advice['new_attempt_admissible'] and not advice['retry_admissible']
    assert invoke('read',s.root)['effect_count']==count


@pytest.mark.parametrize('where',['before','during'])
def test_exception_rollback_is_separate_from_hard_termination(tmp_path,where):
    s,r,q,p=setup(tmp_path);out=invoke('exception',s.root,where)
    assert out['exception']==where+'_transaction'
    read=invoke('read',s.root)
    assert read['effect_count']==0 and read['assessment']['state']=='NOT_STARTED'
