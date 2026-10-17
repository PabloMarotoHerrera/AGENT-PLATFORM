import os
from pathlib import Path
import subprocess
import sys

import pytest

from tests.hermes_cli.test_har04_harness_purity import PROBE


@pytest.mark.parametrize('canary',[None,'runtime','registry','model-tools','provider','write','database','network','process'])
def test_fresh_core_comparison_and_historical_projection_have_no_effects(tmp_path,canary):
    home=tmp_path/'guarded';home.mkdir()
    script=PROBE+r'''
allowed_project.update({'hermes_cli.agent_platform.dependency_identity_adapter',
 'hermes_cli.agent_platform.handler_correspondence','hermes_cli.agent_platform.pre_review_catalog',
 'hermes_cli.agent_platform.historical_validation_adapter'})
forbidden_roots.update({'model_tools','hermes_state','hermes_constants'})
from tests.hermes_cli.test_har11_invalidation import compare,causes
from tests.hermes_cli.test_har11_dependency_manifest import fixture,mutate_content
from tests.hermes_cli.test_har11_historical_identity import historical
from hermes_cli.agent_platform.dependency_identity_adapter import historical_identity
m=fixture()
assert causes(compare(m,m))=={'UNCHANGED'}
assert 'TRANSITIVE_DEPENDENCY_CHANGED' in causes(compare(m,mutate_content(m,'parser')))
assert 'UNKNOWN' in causes(compare(m,m,qualified=False))
body,raw,source,schema=historical()
projection=historical_identity(raw,source=source,original_schema=schema)
assert not projection.grants_authority and not projection.original_digest_verified
print('HAR11_PURE')
'''
    canaries={'runtime':"__import__('hermes_cli.agent_platform.product_runtime')",'registry':"__import__('tools.registry')",
        'model-tools':"__import__('model_tools')",'provider':"__import__('openai')",'write':"open('forbidden','w')",
        'database':"__import__('sqlite3')",'network':"audit('socket.connect',())",'process':"audit('subprocess.Popen',())"}
    if canary:script+='\n'+canaries[canary]
    r=subprocess.run([sys.executable,'-I','-B','-c',script,str(Path(__file__).resolve().parents[2])],cwd=home,
        env={'HOME':str(home),'HERMES_HOME':str(home/'hermes'),'PATH':os.defpath,'LANG':'C.UTF-8','TZ':'UTC'},capture_output=True,text=True,timeout=60)
    if canary:assert r.returncode!=0 and 'RuntimeError:' in r.stderr
    else:assert r.returncode==0,r.stderr
    assert list(home.iterdir())==[]
