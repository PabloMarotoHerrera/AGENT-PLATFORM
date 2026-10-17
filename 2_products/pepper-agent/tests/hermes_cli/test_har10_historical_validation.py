"""Synthetic historical views, never copied from frozen operational records."""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from hermes_cli.agent_platform.harness.validation import sha256_bytes
from hermes_cli.agent_platform.harness.validation_dag_verifier import assess, verify
from hermes_cli.agent_platform.historical_validation_adapter import project_historical
from tests.hermes_cli.test_har10_validation_dag_verifier import (
    ASSUMPTION, CONTEXT, change, content, fixture, observation, ref,
)


def historical(*, compiled=False):
    steps=[dict(validation_id="V1",description="Run command",command="python -m pytest tests/synthetic.py",expected_result="Pass",required=True),
        dict(validation_id="V10",description="Classify regression failures after V1",command=None,expected_result="Human classifies debt",required=True),
        dict(validation_id="V11",description="Aggregate V1-V10",command=None,expected_result="Human acceptance",required=True)]
    if compiled:
        steps=[dict(s,ordinal=i,kind="manual" if s['command'] is None else "command",command_execution_authorized=False,step_SHA256="a"*64) for i,s in enumerate(steps,1)]
    return dict(schema_version=1,ticket_id="predecessor",validation_steps=steps)


def project(body=None,*,compiled=False,**updates):
    raw=json.dumps(body or historical(compiled=compiled),ensure_ascii=False).encode()
    source=content("historical-injected-bytes").model_copy(update={"sha256":sha256_bytes(raw)})
    return raw,project_historical(raw,source=source,original_schema=ref("pepper-work-packet" if compiled else "pepper-ticket-spec"),context=CONTEXT,**updates)


@pytest.mark.parametrize("compiled",[False,True])
def test_historical_identity_preserved_and_ambiguity_not_exact(compiled):
    body=historical(compiled=compiled); before=json.dumps(body); raw,p=project(body,compiled=compiled)
    assert json.dumps(body)==before and p.source.sha256==sha256_bytes(raw)
    assert p.mapping=="AMBIGUOUS_HISTORICAL_SEMANTICS" and p.graph_identity!=p.source
    assert not p.historical_digest_verified and not p.grants_authority
    assert "historical_mapping_unresolved" in {d.code for d in verify(p.graph).diagnostics}
    assert all(not a.criterion_satisfied for a in assess(p.graph,(),synthetic_authority=ASSUMPTION))
    v11=next(r for r in p.graph.requirements if r.requirement.contract_id=="V11")
    assert v11.human_authority


def test_nontextual_subset_is_partial_not_false_full_compatibility():
    b=historical(); b['validation_steps']=b['validation_steps'][:1]
    _,p=project(b)
    assert p.mapping=="PARTIALLY_OBSERVABLE" and p.graph is not None


@pytest.mark.parametrize("mutation",["missing","duplicate","required","ordinal","kind","manual-authority","ticket","schema","command","wording"])
def test_invalid_historical_fields(mutation):
    b=historical(compiled=True)
    if mutation=="missing": del b['validation_steps']
    elif mutation=="duplicate": b['validation_steps'].append(b['validation_steps'][0])
    elif mutation=="required": b['validation_steps'][0]['required']='true'
    elif mutation=="ordinal": b['validation_steps'][0]['ordinal']=2
    elif mutation=="kind": b['validation_steps'][0]['kind']='manual'
    elif mutation=="manual-authority": b['validation_steps'][1]['command_execution_authorized']=True
    elif mutation=="ticket": b['ticket_id']='successor'
    elif mutation=="schema": del b['schema_version']
    elif mutation=="command": b['validation_steps'][0]['command']=False
    else: del b['validation_steps'][0]['expected_result']
    assert project(b,compiled=True)[1].mapping=="INVALID_HISTORICAL_INPUT"


@pytest.mark.parametrize("schema",[ref("pepper-work-packet",2),ref("unknown-history")])
def test_unknown_history_fails_safely(schema):
    raw=json.dumps(historical()).encode()
    assert project_historical(raw,source=change(content(),sha256=sha256_bytes(raw)),original_schema=schema,context=CONTEXT).mapping=="UNSUPPORTED_HISTORICAL_SCHEMA"


def test_version_conflict():
    b=historical(); b['schema_version']=2
    assert project(b)[1].mapping=="VERSION_CONFLICT"


def test_mutated_source_digest_rejected():
    raw=json.dumps(historical()).encode()
    p=project_historical(raw,source=content(),original_schema=ref("pepper-ticket-spec"),context=CONTEXT)
    assert p.mapping=="INVALID_HISTORICAL_INPUT" and p.graph is None


def test_legacy_prose_sensitivity_exposed_not_erased():
    b=historical(); _,before=project(b)
    b['validation_steps'][1]['description']='Independent observation'
    b['validation_steps'][1]['expected_result']='Human confirms independent condition'
    _,after=project(b)
    assert before.source!=after.source and before.graph_identity!=after.graph_identity
    assert len(before.graph.dependencies)>len(after.graph.dependencies)


def test_description_equivalent_interpretation_still_has_distinct_source_identity():
    b=historical(); _,before=project(b); b['validation_steps'][0]['description']='Execute the command'
    _,after=project(b)
    assert before.source!=after.source
    assert [(d.consumer,d.evidence,d.condition) for d in before.graph.dependencies]==[(d.consumer,d.evidence,d.condition) for d in after.graph.dependencies]


def test_compiled_order_significant_and_repeated_prose_refs_deduplicated():
    b=historical(compiled=True); b['validation_steps'].reverse()
    assert project(b,compiled=True)[1].mapping=="INVALID_HISTORICAL_INPUT"
    b=historical(); b['validation_steps'][1]['description']='V1 V1 V1'
    _,p=project(b)
    assert len([d for d in p.graph.dependencies if d.consumer==ref('V10') and d.evidence==ref('V1')])==1


@pytest.mark.parametrize("category",["COMMAND","INSPECTION","CONSISTENCY","MANUAL","CLASSIFICATION","REVIEW","TERMINAL","IDENTITY","MATERIAL_REVISION","RECONCILIATION"])
def test_bounded_reference_validation_classes(category):
    # Native synthetic reference scenarios for first-slice classes; not a new
    # production plan or a claim of runtime guard parity.
    g=fixture(); g=change(g,requirements=(change(g.requirements[0],category=category),))
    assert verify(g).structurally_valid
    assert not assess(g,())[0].criterion_satisfied


@pytest.mark.parametrize("canary",[None,"runtime","registry","write","database","network","process"])
def test_pure_core_and_passive_adapter_in_fresh_guarded_process(tmp_path,canary):
    from tests.hermes_cli.test_har04_harness_purity import PROBE
    home=tmp_path/'guarded'
    home.mkdir()
    script=PROBE+r'''
allowed_project.add("hermes_cli.agent_platform.historical_validation_adapter")
from tests.hermes_cli.test_har10_validation_dag_verifier import fixture, observation, ASSUMPTION
from tests.hermes_cli.test_har10_historical_validation import project
from hermes_cli.agent_platform.harness.validation_dag_verifier import assess, verify
g=fixture()
assert verify(g).structurally_valid
assert assess(g,(observation(),),synthetic_authority=ASSUMPTION)[0].criterion_satisfied
assert not assess(g,(observation("FAILED"),),synthetic_authority=ASSUMPTION)[0].criterion_satisfied
assert project()[1].mapping=="AMBIGUOUS_HISTORICAL_SEMANTICS"
print("HAR10_PURE")
'''
    canaries={"runtime":"__import__('hermes_cli.agent_platform.product_runtime')","registry":"__import__('tools.registry')",
        "write":"open('forbidden','w')","database":"__import__('sqlite3')","network":"audit('socket.connect',())","process":"audit('subprocess.Popen',())"}
    if canary: script+='\n'+canaries[canary]
    result=subprocess.run([sys.executable,'-I','-B','-c',script,str(Path(__file__).resolve().parents[2])],cwd=home,
        env={'HOME':str(home),'HERMES_HOME':str(home/'hermes'),'PATH':os.defpath,'TZ':'UTC','LANG':'C.UTF-8'},capture_output=True,text=True,timeout=60)
    if canary: assert result.returncode!=0 and 'RuntimeError:' in result.stderr
    else: assert result.returncode==0,result.stderr
    assert list(home.iterdir())==[]
