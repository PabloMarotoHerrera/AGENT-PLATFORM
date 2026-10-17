"""Historical fixtures are synthetic bytes, not frozen live authority records."""

import json
from pathlib import Path

import pytest

from hermes_cli.agent_platform.dependency_identity_adapter import first_slice_manifest, historical_identity
from hermes_cli.agent_platform.handler_correspondence import BindingStatus, inspect_correspondence
from hermes_cli.agent_platform.pre_review_catalog import product_operations
from hermes_cli.agent_platform.harness.dependency_manifest import DependencyNode, InventoryFact, SourceInventory, verify_manifest
from hermes_cli.agent_platform.harness.validation import sha256_bytes
from tests.hermes_cli.test_har11_dependency_manifest import change, content, ref


def historical(schema='pepper-material-revision-request',**updates):
    definitions={'pepper-command-validation-record':('pepper-pre-review-command-validation-v1','binding','record_SHA256'),
        'pepper-material-revision-request':('pepper-post-execution-material-revision-v1','request_binding','material_revision_request_SHA256'),
        'pepper-material-revision-reconciliation':('pepper-material-revision-authority-reconciliation-v1','reconciliation_binding','reconciliation_SHA256')}
    policy,binding,digest=definitions[schema]
    body={'policy_id':policy,binding:{'project_id':'synthetic-project','ticket_id':'synthetic-ticket',
        'work_packet_SHA256':'b'*64,'canonical_validation_source':{'source_files_SHA256':'c'*64,'source_root':'synthetic-offline-source'}},digest:'a'*64,**updates}
    raw=json.dumps(body,sort_keys=True).encode();source=change(content('historical-source'),sha256=sha256_bytes(raw))
    return body,raw,source,ref(schema)


@pytest.mark.parametrize('schema',['pepper-command-validation-record','pepper-material-revision-request','pepper-material-revision-reconciliation'])
def test_supported_historical_combined_binding_is_not_split_into_signatures(schema):
    body,raw,source,schema=historical(schema)
    original=bytes(raw);p=historical_identity(raw,source=source,original_schema=schema)
    assert p.mapping=='BROADER_IDENTITY_FALLBACK_REQUIRED' and p.original_source==source
    assert p.original_combined_identity.sha256=='a'*64
    assert not p.independently_verified_dimensions and not p.original_digest_verified
    assert not p.authorizes_execution and p.identity()!=source and raw==original
    assert 'combined_binding_not_independent_signatures' in p.unresolved


def test_unknown_historical_schema_and_versions_are_not_guessed():
    _,raw,source,schema=historical()
    for s in [change(schema,version=2),ref('unknown-history')]:
        assert historical_identity(raw,source=source,original_schema=s).mapping=='UNSUPPORTED_SCHEMA'


@pytest.mark.parametrize('mutation',['raw','policy','binding','digest','version','duplicate-json'])
def test_invalid_history_or_conflicting_version(mutation):
    body,raw,source,schema=historical()
    if mutation=='raw':source=content('wrong-source')
    else:
        if mutation=='policy':body['policy_id']='unknown'
        elif mutation=='binding':body['request_binding']=[]
        elif mutation=='digest':body['material_revision_request_SHA256']='invalid'
        elif mutation=='version':body['schema_version']=2
        raw=json.dumps(body).encode()
        if mutation=='duplicate-json':raw=b'{"x":1,"x":2}'
        source=change(source,sha256=sha256_bytes(raw))
    p=historical_identity(raw,source=source,original_schema=schema)
    assert p.mapping==('CONFLICTING_VERSIONS' if mutation=='version' else 'INVALID_SOURCE')


def test_c92_binding_and_original_digest_remain_exactly_distinct_from_derived_projection():
    body,raw,source,schema=historical();before=json.dumps(body,sort_keys=True)
    p=historical_identity(raw,source=source,original_schema=schema)
    assert json.dumps(body,sort_keys=True)==before and p.original_combined_identity.sha256==body['material_revision_request_SHA256']
    assert p.identity().sha256!=p.original_combined_identity.sha256
    body['request_binding']['canonical_validation_source']['source_files_SHA256']='d'*64
    changed=json.dumps(body,sort_keys=True).encode()
    q=historical_identity(changed,source=change(source,sha256=sha256_bytes(changed)),original_schema=schema)
    assert p.identity()!=q.identity() and q.original_combined_identity==p.original_combined_identity
    assert not q.original_digest_verified  # changed bytes do not validate old consent


def test_har10_ambiguity_is_retained():
    from tests.hermes_cli.test_har10_historical_validation import project
    body,raw,source,schema=historical()
    h10=project()[1]
    p=historical_identity(raw,source=source,original_schema=schema,har10_projection=h10)
    assert p.mapping=='AMBIGUOUS_HISTORICAL_IDENTITY'
    assert p.har10_mapping=='AMBIGUOUS_HISTORICAL_SEMANTICS'
    assert 'har10_ambiguity_or_incompleteness_retained' in p.unresolved


@pytest.fixture(scope='module')
def offline_source_payload():
    # Bounded offline evidence generation in the test owner, never adapter I/O.
    product=Path(__file__).resolve().parents[2]
    raw=(product/'tools/pepper_workflow_tools.py').read_bytes()
    node=DependencyNode(node=ref('hermes-entry'),kind='EXECUTABLE_SOURCE',content=change(content('source'),sha256=sha256_bytes(raw)),source_key='tools/pepper_workflow_tools.py')
    dynamic=DependencyNode(node=ref('runtime-dynamic'),kind='UNKNOWN_DYNAMIC',content=content('unqualified-runtime-scope'),source_key='hermes_cli/agent_platform/product_runtime.py')
    inventory=SourceInventory(inventory=ref('injected-offline-inventory'),source_boundary=content('offline-code-boundary'),
        facts=(InventoryFact(node=node,dependencies=(dynamic.node,)),InventoryFact(node=dynamic)),discovery='UNKNOWN_DYNAMIC')
    proofs=tuple(inspect_correspondence(raw,o.handler) for o in product_operations())
    return raw,inventory,proofs


def test_actual_first_slice_proofs_never_establish_narrow_closure_or_availability(offline_source_payload):
    raw,inventory,proofs=offline_source_payload
    assert len(proofs)==15 and all(p.status==BindingStatus.VERIFIED for p in proofs)
    p=first_slice_manifest(inventory,tool_source=raw,bindings=proofs,broad_source=content('injected-existing-broad-fingerprint'))
    r=verify_manifest(p.manifest)
    assert len(r.capabilities)==15 and not r.discovery_complete_under_assumptions
    assert all(c.implementation is None for c in r.capabilities)
    assert all(c.source_mode=='BROAD_TREE' for c in p.manifest.capabilities)
    assert p.consumer_scope=='UNKNOWN_REQUIRE_BROAD_COVERAGE'
    assert not p.runtime_availability_established and not p.authorizes_execution


@pytest.mark.parametrize('mutation',['missing-proof','duplicate-proof','stale-source','missing-inventory'])
def test_passive_adapter_qualifies_missing_ambiguous_stale_source(offline_source_payload,mutation):
    raw,inventory,proofs=offline_source_payload
    if mutation=='missing-proof':proofs=proofs[1:]
    elif mutation=='duplicate-proof':proofs=proofs+(proofs[0],)
    elif mutation=='stale-source':raw+=b'\n# changed explicit source\n'
    else:inventory=change(inventory,facts=())
    p=first_slice_manifest(inventory,tool_source=raw,bindings=proofs,broad_source=content('broad'))
    assert not verify_manifest(p.manifest).discovery_complete_under_assumptions
    assert p.reasons!=('static_binding_is_not_availability',)
