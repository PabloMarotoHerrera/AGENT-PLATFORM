import json
import pytest
from tests.hermes_cli.har13_test_helpers import setup,spawn,handshake,reap,invoke
from tests.hermes_cli.har13_process_fixture import derived
from hermes_cli.agent_platform.isolated_effect_adapter import attempt_for,transition


def race(root,action,args):
    children=[spawn(action,root,*a) for a in args]
    try:
        for child in children:handshake(child,root,action+'-ready')
        for child in children:child.stdin.write('continue\n');child.stdin.flush()
        results=[]
        for child in children:
            out,err=child.communicate(timeout=25);assert child.returncode==0,err;results.append(json.loads(out))
        return results
    finally:
        for child in children:reap(child)


def test_two_processes_cannot_steal_one_owner(tmp_path):
    s,r,q,p=setup(tmp_path);s.request(r)
    out=race(s.root,'claim',[('writer-a',),('writer-b',)])
    assert sum(v['result']=='CONFLICT' for v in out)==1
    assert len({v['pid'] for v in out})==2 and len(s.conflicts(r.operation_id))==1


@pytest.mark.parametrize('same_key',[False,True])
def test_processes_compete_on_same_expected_version_and_effect_key(tmp_path,same_key):
    s,r,q,p=setup(tmp_path)
    for name,writer in [('first','writer-a'),('second','writer-b')]:
        req,auth,payload=derived(name,same_key);h=s.request(req);owner=s.claim(req.operation_id,writer,1)
        for stage in ('PREPARED','EFFECT_INTENT_RECORDED'):
            h=s.move(req.operation_id,writer,transition(h,stage),authorization=auth,observed_context=req.context)
        a=attempt_for(req,owner,'first-attempt')
        s.move(req.operation_id,writer,transition(h,'EFFECT_ATTEMPTED',attempt=a),authorization=auth,observed_context=req.context)
    suffix=('same-key',) if same_key else ()
    out=race(s.root,'effect',[('first',*suffix),('second',*suffix)])
    assert sorted(v['result'] for v in out)==['CONFIRMED','CONFLICT']
    assert s.effect_count()==1 and s.observe_version(r.expected).value==1


def test_same_serialized_writer_after_exit_is_only_a_fixture_assumption(tmp_path):
    from tests.hermes_cli.har13_test_helpers import crash
    s,r,out=crash(tmp_path,'W05')
    child=spawn('claim',s.root,'writer-a')
    try:
        handshake(child,s.root,'claim-ready');output,err=child.communicate('continue\n',timeout=25)
        assert child.returncode==0,err
        result=json.loads(output);assert result['result']=='writer-a'
        assert result['qualification']=='ISOLATED_TRUSTED_FIXTURE_ONLY_NOT_AUTHENTICATION'
        assert invoke('replay',s.root)['reason']=='SAME_WRITER_NOT_AUTHENTICATED'
        assert invoke('read',s.root)['effect_count']==0
    finally:reap(child)


def test_active_process_owner_is_not_replaced(tmp_path):
    s,r,q,p=setup(tmp_path);owner=spawn('crash',s.root,'W02')
    try:
        handshake(owner,s.root,'W02');assert owner.poll() is None
        out=race(s.root,'claim',[('writer-b',)])
        assert out[0]['result']=='CONFLICT' and owner.poll() is None
        assert s.head(r.operation_id).stage=='REQUESTED' and not s.effect_count()
    finally:reap(owner)
