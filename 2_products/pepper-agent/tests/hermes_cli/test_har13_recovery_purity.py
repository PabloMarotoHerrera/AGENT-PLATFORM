import os
from pathlib import Path
import subprocess
import sys
import pytest
from tests.hermes_cli.test_har04_harness_purity import PROBE


@pytest.mark.parametrize('canary',[None,'sqlite','runtime','registry','write','network','process','provider'])
def test_fresh_recovery_core_has_no_effects(tmp_path,canary):
    home=tmp_path/'guarded';home.mkdir()
    script=PROBE+r'''
from hermes_cli.agent_platform.harness.journal_recovery import DurableSnapshot,assess_recovery
from hermes_cli.agent_platform.harness.replay_policy import assess_replay
from hermes_cli.agent_platform.harness.operation_journal import OperationRequest,EffectIntent,ExpectedVersion
from hermes_cli.agent_platform.harness.contracts import ActorRef
from hermes_cli.agent_platform.harness.validation import canonical_json
from tests.hermes_cli.test_har11_dependency_identity import context
from tests.hermes_cli.test_har11_dependency_manifest import content,ref
c=context();v=ExpectedVersion(store=ref('isolated-sqlite-aggregate'),aggregate='fixture',scope=c.scope,value=0)
e=EffectIntent(effect_id='effect',operation_id='operation',operation_version=1,scope=c.scope,expected=v,payload=content())
r=OperationRequest(operation_id='operation',operation_version=1,actor=ActorRef(actor_id='fixture'),context=c,expected=v,effect=e,validation_assessment=content())
s=DurableSnapshot(expected=r,store_schema=1,operation=None,owner=None,entries=(),aggregate=canonical_json(v),effect_key=None,attempt=None,payload_hex=None,receipt=None,provenance=content())
a=assess_recovery(s);assert a.state=='NOT_STARTED' and not a.authorizes_execution
assert not assess_replay(a,r,writer='writer').retry_admissible
'''
    code={'sqlite':"__import__('sqlite3')",'runtime':"__import__('hermes_cli.agent_platform.product_runtime')",'registry':"__import__('tools.registry')",'write':"open('forbidden','w')",'network':"audit('socket.connect',())",'process':"audit('subprocess.Popen',())",'provider':"__import__('openai')"}
    if canary:script+='\n'+code[canary]
    r=subprocess.run([sys.executable,'-I','-B','-c',script,str(Path(__file__).resolve().parents[2])],cwd=home,
        env={'HOME':str(home),'HERMES_HOME':str(home/'forbidden'),'PATH':os.defpath,'LANG':'C.UTF-8'},capture_output=True,text=True,timeout=30)
    if canary:assert r.returncode!=0 and 'RuntimeError:' in r.stderr
    else:assert r.returncode==0,r.stderr
    assert not list(home.iterdir())
