import json
import pytest
from pydantic import ValidationError
from hermes_cli.agent_platform.harness.journal_recovery import DurableSnapshot,assess_recovery
from hermes_cli.agent_platform.harness.operation_journal import EffectReceipt
from hermes_cli.agent_platform.isolated_journal_recovery import read_snapshot
from hermes_cli.agent_platform.isolated_effect_adapter import run_fixture
from hermes_cli.agent_platform.harness.validation import canonical_json,parse_contract
from tests.hermes_cli.har13_test_helpers import setup
from tests.hermes_cli.test_har12_operation_journal import change,content,ref


def snapshot(tmp_path,mode=None):
    s,r,q,p=setup(tmp_path)
    if mode is not None:run_fixture(s,r,p,writer='writer-a',authorization=q,observed_context=r.context,failure=None if mode=='success' else mode)
    return s,read_snapshot(s,r,provenance=content('explicit-fixture-readback'))


def test_strict_immutable_bounded_and_deterministic(tmp_path):
    s,snap=snapshot(tmp_path)
    assert parse_contract(DurableSnapshot,canonical_json(snap))==snap
    a=assess_recovery(snap);assert canonical_json(a)==canonical_json(assess_recovery(snap))
    assert not a.grants_authority and not a.authorizes_execution
    with pytest.raises(ValidationError):snap.complete=False
    for patch in ({'schema_version':2},{'unknown':True},{'payload_hex':'a'*131073}):
        with pytest.raises(ValidationError):change(snap,**patch)
    assert assess_recovery(snap,policy=ref('passive-journal-recovery',2)).state=='UNSUPPORTED_VERSION'


@pytest.mark.parametrize('mode,state',[('success','COMPLETED_DURABLE'),('after_effect','EFFECT_CONFIRMED_DURABLE'),
 ('after_receipt','EFFECT_CONFIRMED_DURABLE'),('before_effect','SAFE_STOP')])
def test_partial_stages_are_never_promoted(tmp_path,mode,state):
    s,snap=snapshot(tmp_path,mode);a=assess_recovery(snap)
    assert a.state==state and not a.retry_admissible


@pytest.mark.parametrize('field',['predecessor','revision','request','owner','payload','receipt','aggregate','schema','audit','resource'])
def test_independent_persisted_corruption_is_preserved_and_fails_closed(tmp_path,field):
    s,snap=snapshot(tmp_path,'success');r=snap.expected
    with s.transaction() as c:
        if field in {'predecessor','revision','resource'}:
            raw=json.loads(c.execute('SELECT body FROM entries WHERE revision=6').fetchone()[0])
            if field=='predecessor':
                raw['predecessor']['sha256']='b'*64
                raw['transition']['previous']['sha256']='b'*64
            elif field=='revision':raw['journal_version']=5
            else:raw['request']['context']['scope']['resource_ids']=['foreign-resource']
            c.execute('UPDATE entries SET body=? WHERE revision=6',(json.dumps(raw),))
        elif field=='request':c.execute('UPDATE operations SET request=?',('{}',))
        elif field=='owner':c.execute('UPDATE operations SET owner=?',('{}',))
        elif field=='payload':c.execute('UPDATE effects SET payload=?',(b'corrupt',))
        elif field=='receipt':c.execute('UPDATE effects SET receipt=?',('{}',))
        elif field=='aggregate':c.execute('UPDATE aggregates SET body=?',(canonical_json(change(r.expected,value=99)),))
        elif field=='schema':c.execute('PRAGMA user_version=2')
        else:c.execute('INSERT INTO conflicts(op,body) VALUES (?,?)',(r.operation_id,'{}'))
    before=s.path.read_bytes();raw=read_snapshot(s,r,provenance=content('corruption-observed'))
    result=assess_recovery(raw)
    assert result.state in {'CORRUPT_HISTORY','CONFLICT','UNSUPPORTED_VERSION'}
    assert s.path.read_bytes()==before and not result.retry_admissible and not result.authorizes_execution


@pytest.mark.parametrize('status',['ACTIVE','EXITED','UNKNOWN'])
def test_process_liveness_is_not_owner_authority(tmp_path,status):
    s,snap=snapshot(tmp_path,'after_receipt')
    a=assess_recovery(change(snap,owner_process=status))
    assert a.ownership=='BOUND_'+status and not a.takeover_admissible


def test_missing_receipt_never_fabricates_confirmation(tmp_path):
    s,snap=snapshot(tmp_path,'success')
    with s.transaction() as c:c.execute('DELETE FROM effects')  # Explicit disposable corruption fixture only.
    a=assess_recovery(read_snapshot(s,snap.expected,provenance=content('missing-row')))
    assert a.state=='CORRUPT_HISTORY' and a.receipt is None


def test_incomplete_observation_does_not_assume_not_started(tmp_path):
    s,snap=snapshot(tmp_path)
    assert assess_recovery(change(snap,complete=False)).state=='SAFE_STOP'


def test_foreign_receipt_is_not_recoverable_confirmation(tmp_path):
    s,snap=snapshot(tmp_path,'after_effect')
    receipt=parse_contract(EffectReceipt,snap.receipt)
    foreign_scope=change(receipt.observed.scope,project_id='foreign-project')
    receipt=change(receipt,observed=change(receipt.observed,scope=foreign_scope))
    bad=change(snap,receipt=canonical_json(receipt),aggregate=canonical_json(receipt.observed))
    assert assess_recovery(bad).state=='CORRUPT_HISTORY'
