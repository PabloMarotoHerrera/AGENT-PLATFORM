import os
from pathlib import Path
import subprocess
import sys

import pytest

from tests.hermes_cli.test_har04_harness_purity import PROBE


@pytest.mark.parametrize('canary',[None,'sqlite','runtime','registry','provider','write','network','process'])
def test_fresh_journal_core_has_no_effects(tmp_path,canary):
    home=tmp_path/'guarded';home.mkdir()
    script=PROBE+r'''
from hermes_cli.agent_platform.harness.operation_journal import OperationRequest,EffectIntent,ExpectedVersion
from hermes_cli.agent_platform.harness.journal_protocol import initial,advance,owner_for
from hermes_cli.agent_platform.harness.contracts import ActorRef
from tests.hermes_cli.test_har11_dependency_identity import context
from tests.hermes_cli.test_har11_dependency_manifest import content,ref
c=context();v=ExpectedVersion(store=ref('isolated-sqlite-aggregate'),aggregate='fixture',scope=c.scope,value=0)
effect=EffectIntent(effect_id='effect',operation_id='operation',operation_version=1,scope=c.scope,expected=v,payload=content())
r=OperationRequest(operation_id='operation',operation_version=1,actor=ActorRef(actor_id='fixture'),context=c,expected=v,effect=effect,validation_assessment=content())
assert initial(r).stage=='REQUESTED'
print('HAR12_PURE')
'''
    canaries={'sqlite':"__import__('sqlite3')",'runtime':"__import__('hermes_cli.agent_platform.product_runtime')",
        'registry':"__import__('tools.registry')",'provider':"__import__('openai')",'write':"open('forbidden','w')",
        'network':"audit('socket.connect',())",'process':"audit('subprocess.Popen',())"}
    if canary:script+='\n'+canaries[canary]
    result=subprocess.run([sys.executable,'-I','-B','-c',script,str(Path(__file__).resolve().parents[2])],cwd=home,
        env={'HOME':str(home),'HERMES_HOME':str(home/'unread-live-canary'),'PATH':os.defpath,'LANG':'C.UTF-8','TZ':'UTC'},capture_output=True,text=True,timeout=60)
    if canary:assert result.returncode!=0 and 'RuntimeError:' in result.stderr
    else:assert result.returncode==0,result.stderr
    assert not list(home.iterdir())


def test_adapter_import_does_not_initialize_any_store(tmp_path,monkeypatch):
    home=tmp_path/'guarded';home.mkdir()
    script=r'''
import sys,os,sqlite3
from pathlib import Path
sys.path.insert(0,sys.argv[1])
def audit(event,args):
 if event=='sqlite3.connect' or event.startswith(('socket.','subprocess.')):raise RuntimeError('unexpected effect '+event)
 if event=='open' and (isinstance(args[1],str) and any(x in args[1] for x in 'wax+') or isinstance(args[2],int) and args[2]& (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)):raise RuntimeError('unexpected write')
sys.addaudithook(audit)
from hermes_cli.agent_platform.isolated_operation_journal import IsolatedJournal
from hermes_cli.agent_platform.isolated_effect_adapter import IsolatedAppendAdapter
assert not any(n.startswith(('hermes_cli.agent_platform.product_runtime','tools.registry','model_tools','openai')) for n in sys.modules)
'''
    result=subprocess.run([sys.executable,'-I','-B','-c',script,str(Path(__file__).resolve().parents[2])],cwd=home,
        env={'HOME':str(home),'HERMES_HOME':str(home/'forbidden'),'PATH':os.defpath,'LANG':'C.UTF-8'},capture_output=True,text=True,timeout=60)
    assert result.returncode==0,result.stderr
    assert not list(home.iterdir())


def test_real_adapter_writes_only_below_injected_disposable_parent(tmp_path):
    home=tmp_path/'guarded';home.mkdir();allowed=home/'allowed';allowed.mkdir()
    script=r'''
import sys,os
from pathlib import Path
from urllib.parse import urlparse,unquote
sys.path.insert(0,sys.argv[1])
from tests.hermes_cli.test_har12_operation_journal import case
from hermes_cli.agent_platform.isolated_operation_journal import IsolatedJournal
from hermes_cli.agent_platform.isolated_effect_adapter import run_fixture
allowed=Path(sys.argv[2]).resolve();events=[]
def below(value):
 if isinstance(value,int):return
 text=os.fsdecode(value)
 if text.startswith('file:'):text=unquote(urlparse(text).path)
 target=Path(text).resolve()
 if not target.is_relative_to(allowed):raise RuntimeError('outside disposable root '+str(target))
def audit(event,args):
 if event=='sqlite3.connect':below(args[0]);events.append('sqlite-local')
 if event in {'os.mkdir','os.remove','os.rename','os.rmdir'}:below(args[0])
 if event=='open' and (isinstance(args[1],str) and any(x in args[1] for x in 'wax+') or isinstance(args[2],int) and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)):below(args[0])
 if event.startswith(('socket.','subprocess.')):raise RuntimeError('forbidden effect '+event)
sys.addaudithook(audit)
r,q,p=case();s=IsolatedJournal.create_disposable(allowed);s.initialize_aggregate(r.expected)
assert run_fixture(s,r,p,writer='fixture-writer',authorization=q,observed_context=r.context).stage=='COMPLETED'
assert events and s.effect_count()==1
assert not any(n.startswith(('hermes_cli.agent_platform.product_runtime','tools.registry','openai','model_tools')) for n in sys.modules)
'''
    result=subprocess.run([sys.executable,'-I','-B','-c',script,str(Path(__file__).resolve().parents[2]),str(allowed)],cwd=home,
        env={'HOME':str(home),'HERMES_HOME':str(home/'forbidden-live'),'PATH':os.defpath,'LANG':'C.UTF-8'},capture_output=True,text=True,timeout=60)
    assert result.returncode==0,result.stderr
    assert set(home.iterdir())=={allowed}
