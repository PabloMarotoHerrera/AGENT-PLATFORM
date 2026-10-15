"""Fresh-process import AND catalog/product-data operations under effect guards."""
import os
from pathlib import Path
import subprocess
import sys


def test_fresh_catalog_and_passive_product_adapter_have_no_effects(tmp_path):
    from tests.hermes_cli.test_har04_harness_purity import PROBE
    home=tmp_path/'probe';home.mkdir()
    code=PROBE+r'''
from hermes_cli.agent_platform.harness.catalog import build_catalog,serialize_catalog,deserialize_catalog
snapshot=build_catalog(harness.ContractRef(contract_id='empty',version=1))
assert deserialize_catalog(serialize_catalog(snapshot))==snapshot
allowed_project.update({'hermes_cli.agent_platform.handler_correspondence','hermes_cli.agent_platform.pre_review_catalog'})
from hermes_cli.agent_platform.pre_review_catalog import product_catalog,qualify_bindings,continuation_templates
assert product_catalog().list_capabilities()
assert continuation_templates()
proof=qualify_bindings(b"raise RuntimeError('no execution')\n")
assert all(p.status.value=='ABSENT' for p in proof)
print('HAR06_PURE_DECLARATION_AND_BINDING')
'''
    result=subprocess.run([sys.executable,'-I','-B','-c',code,str(Path(__file__).resolve().parents[2])],
        cwd=home,env={'HOME':str(home),'HERMES_HOME':str(home/'hermes'),'PATH':os.defpath,'LANG':'C.UTF-8'},
        capture_output=True,text=True,timeout=30)
    assert result.returncode==0,result.stderr
    assert 'HAR06_PURE_DECLARATION_AND_BINDING' in result.stdout
    assert list(home.iterdir())==[]
