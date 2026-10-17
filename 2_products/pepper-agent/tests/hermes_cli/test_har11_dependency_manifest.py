"""Independent toy discovery inventory; all positive completeness is synthetic."""

import pytest

from hermes_cli.agent_platform.harness.contracts import ContentRef, ContractRef
from hermes_cli.agent_platform.harness.dependency_manifest import (
    CapabilityRoot, DependencyEdge, DependencyManifest, DependencyNode, DependencyPolicy,
    ConsumerScopeFact, DiscoveryAssumption, InventoryFact, SourceInventory, verify_manifest,
)
from hermes_cli.agent_platform.harness.validation import canonical_json


def ref(name, version=1):
    return ContractRef(contract_id=name, version=version)


def content(name='synthetic-source', char='a'):
    return ContentRef(content_id=name, sha256=char*64)


def change(value, **updates):
    return type(value).model_validate({**value.model_dump(), **updates})


def qualify(m):
    # This is fixture-only positive qualification, never a production producer.
    return change(m, assumption=DiscoveryAssumption(inventory=m.inventory.identity(),source_boundary=m.inventory.source_boundary,
        policy=m.policy.policy,provenance=content('synthetic-discovery-proof'),scope='ISOLATED_SYNTHETIC_TEST_ONLY',presentation_exclusion_justified=True))


def consumer_facts(caps):
    return tuple(ConsumerScopeFact(capability=c.capability,operation=c.operation,roots=c.roots,
        consumption='FULL_TREE' if c.consumes_full_tree else 'BOUNDED') for c in caps)


def fixture(broad=False):
    # A diamond: handler -> helper -> shared-parser; handler -> shared-parser.
    rows=[('handler-a','EXECUTABLE_SOURCE',('helper','parser','policy','display','instructions')),
        ('handler-b','EXECUTABLE_SOURCE',('parser','policy','data','config')),
        ('helper','SHARED_LIBRARY',('parser',)),('parser','PARSER',()),('policy','POLICY',()),
        ('data','VALIDATION_INPUT',()),('config','CONFIGURATION',()),
        ('display','DOCUMENTATION_PRESENTATION_ONLY',()),('instructions','DOCUMENTATION_CONSUMED',())]
    facts=tuple(InventoryFact(node=DependencyNode(node=ref(name),kind=kind,content=content(name),
        source_key=name+('.md' if name in {'display','instructions'} else '.py')),
        dependencies=tuple(ref(d) for d in deps)) for name,kind,deps in rows)
    inventory=SourceInventory(inventory=ref('toy-inventory'),source_boundary=content('toy-program-boundary'),facts=facts,discovery='BOUNDED_SYNTHETIC')
    model=DependencyManifest(manifest=ref('toy-manifest'),policy=DependencyPolicy(exclude_justified_presentation=True),
        nodes=tuple(f.node for f in facts),edges=tuple(DependencyEdge(consumer=f.node.node,dependency=d) for f in facts for d in f.dependencies),
        capabilities=tuple(CapabilityRoot(capability=ref(cap),operation=ref(cap+'.operation'),roots=(ref(handler),),
            consumes_full_tree=broad,source_mode='BROAD_TREE' if broad else 'NARROW_TRANSITIVE',broad_source=content('whole-tree') if broad else None)
            for cap,handler in [('cap-a','handler-a'),('cap-b','handler-b')]),inventory=inventory)
    return qualify(change(model,inventory=change(inventory,consumers=consumer_facts(model.capabilities))))


def mutate_content(m, name, *, kind=None):
    node=next(n for n in m.nodes if n.node==ref(name))
    new=change(node,content=content(name,'b'),**({'kind':kind} if kind else {}))
    inventory=change(m.inventory,facts=tuple(change(f,node=new) if f.node.node==node.node else f for f in m.inventory.facts))
    return qualify(change(m,nodes=tuple(new if n==node else n for n in m.nodes),inventory=inventory))


def closure(m, name='cap-a'):
    return next(c for c in verify_manifest(m).capabilities if c.capability==ref(name))


def test_transitive_diamond_is_not_duplicate_and_topology_is_dependencies_first():
    m=fixture();r=verify_manifest(m)
    assert r.discovery_complete_under_assumptions and not r.authorizes_execution
    assert set(x.contract_id for x in closure(m).reachable)=={'handler-a','helper','parser','policy','display','instructions'}
    assert r.traversal_order.index(ref('parser'))<r.traversal_order.index(ref('helper'))<r.traversal_order.index(ref('handler-a'))
    assert len(closure(m).reachable)==6


def test_input_order_does_not_change_identity_or_report():
    m=fixture(); other=change(m,nodes=m.nodes[::-1],edges=m.edges[::-1],capabilities=m.capabilities[::-1])
    assert canonical_json(verify_manifest(m))==canonical_json(verify_manifest(other))
    assert m.identity()==other.identity()


@pytest.mark.parametrize('name',['parser','policy'])
def test_shared_dependency_fanout(name):
    m=fixture();n=mutate_content(m,name)
    for cap in ['cap-a','cap-b']:
        assert closure(m,cap).implementation!=closure(n,cap).implementation


def test_consumed_markdown_changes_implementation_presentation_does_not():
    m=fixture()
    assert closure(m).implementation!=closure(mutate_content(m,'instructions')).implementation
    assert closure(m).implementation==closure(mutate_content(m,'display')).implementation
    assert ref('display') in closure(m).excluded_presentation


def test_broad_consumer_preserves_presentation_and_whole_tree_sensitivity():
    m=fixture(True)
    assert not closure(m).excluded_presentation
    assert closure(m).implementation!=closure(mutate_content(m,'display')).implementation
    caps=tuple(change(c,broad_source=content('whole-tree','b')) for c in m.capabilities)
    assert closure(m).implementation!=closure(change(m,capabilities=caps)).implementation


def test_missing_transitive_source_cannot_be_qualified_by_reachability():
    m=fixture(); n=change(m,nodes=tuple(n for n in m.nodes if n.node!=ref('parser')))
    r=verify_manifest(n)
    assert 'missing_dependency' in r.diagnostics and 'source_inventory_omission' in r.diagnostics
    assert not r.discovery_complete_under_assumptions and closure(n).implementation is None


def test_dropping_declared_edge_does_not_redefine_inventory():
    m=fixture();n=change(m,edges=tuple(e for e in m.edges if e.dependency!=ref('parser')))
    assert 'source_inventory_edge_mismatch' in verify_manifest(n).diagnostics


@pytest.mark.parametrize('discovery',['DECLARED_ONLY','PARTIAL','UNKNOWN_DYNAMIC','BROAD_REQUIRED'])
def test_traversal_closed_is_not_discovery_complete(discovery):
    m=fixture();n=change(m,inventory=change(m.inventory,discovery=discovery),assumption=None)
    assert not verify_manifest(n).discovery_complete_under_assumptions
    assert all(c.implementation is None for c in verify_manifest(n).capabilities)


def test_unknown_dynamic_even_inside_claimed_synthetic_inventory_blocks():
    m=fixture();n=mutate_content(m,'helper',kind='UNKNOWN_DYNAMIC')
    assert closure(n).status=='UNKNOWN_DYNAMIC' and closure(n).implementation is None


def test_inventory_content_drift_and_stale_assumption():
    m=fixture();n=change(m,nodes=tuple(change(n,content=content('changed')) if n.node==ref('parser') else n for n in m.nodes))
    assert 'source_inventory_drift' in verify_manifest(n).diagnostics
    n=change(m,inventory=change(m.inventory,source_boundary=content('different-boundary')))
    assert 'stale_or_mismatched_discovery_assumption' in verify_manifest(n).diagnostics


@pytest.mark.parametrize('mutation,code',[('duplicate','duplicate_or_conflicting_node'),('version','conflicting_node_versions'),
    ('edge','duplicate_edge'),('missing-root','missing_root_or_version'),('policy','unsupported_policy_version'),('narrow-broad','broad_consumer_cannot_be_narrowed')])
def test_invalid_manifests_never_have_complete_implementation(mutation,code):
    m=fixture()
    updates={'duplicate':{'nodes':m.nodes+(m.nodes[0],)},'version':{'nodes':m.nodes+(change(m.nodes[0],node=ref(m.nodes[0].node.contract_id,2)),)},
        'edge':{'edges':m.edges+(m.edges[0],)},'missing-root':{'capabilities':tuple(change(c,roots=(ref('missing'),)) for c in m.capabilities)},
        'policy':{'policy':change(m.policy,policy=ref('harness-dependency-identity',2))},
        'narrow-broad':{'capabilities':tuple(change(c,consumes_full_tree=True) for c in m.capabilities)}}
    r=verify_manifest(change(m,**updates[mutation]));assert code in set(r.diagnostics)|set(x for c in r.capabilities for x in c.reasons)
    assert not r.discovery_complete_under_assumptions


def test_cycle_has_bounded_actual_witness():
    m=fixture();facts=tuple(change(f,dependencies=(ref('handler-a'),)) if f.node.node==ref('parser') else f for f in m.inventory.facts)
    inventory=change(m.inventory,facts=facts)
    n=qualify(change(m,inventory=inventory,edges=m.edges+(DependencyEdge(consumer=ref('parser'),dependency=ref('handler-a')),)))
    r=verify_manifest(n)
    assert 'dependency_cycle' in r.diagnostics and r.cycle_witness[0]==r.cycle_witness[-1]
    assert len(r.cycle_witness)<=257 and not r.discovery_complete_under_assumptions


def test_presentation_role_requires_independent_source_classification_and_exclusion_proof():
    m=fixture();r=verify_manifest(change(m,assumption=change(m.assumption,presentation_exclusion_justified=False)))
    assert not r.capabilities[0].excluded_presentation
    n=change(m,nodes=tuple(change(n,kind='DOCUMENTATION_PRESENTATION_ONLY') if n.node==ref('instructions') else n for n in m.nodes))
    assert 'source_inventory_drift' in verify_manifest(n).diagnostics


def first_slice_reference():
    """Authored toy first-slice families, not real Pepper closure qualification."""
    m=fixture()
    extra=tuple(InventoryFact(node=DependencyNode(node=ref(name),kind=kind,content=content(name),source_key=name))
        for name,kind in [('human-boundary','HISTORICAL_CONTRACT'),('resource-scope','RESOURCE_SCOPE'),
                          ('result-schema','EVIDENCE_SCHEMA'),('dynamic-hook','UNKNOWN_DYNAMIC')])
    facts=tuple(change(f,dependencies=(*f.dependencies,ref('human-boundary'),ref('resource-scope'),ref('result-schema')))
        if f.node.node==ref('handler-b') else f for f in m.inventory.facts)+extra
    inventory=change(m.inventory,facts=facts)
    families=['C91.inspect','C91.execute','C92.request','C93.ticket','C93.steps','C94.reconcile',
        'material.revise','manual.inspect','manual.passed','manual.failed','review.inspect','review.prepare','C26.context']
    caps=tuple(CapabilityRoot(capability=ref('synthetic.'+name),operation=ref('synthetic.'+name+'.operation'),
        roots=(ref('handler-a' if i%2==0 else 'handler-b'),),consumes_full_tree=name=='C91.execute',
        source_mode='BROAD_TREE' if name=='C91.execute' else 'NARROW_TRANSITIVE',
        broad_source=content('toy-whole-source') if name=='C91.execute' else None) for i,name in enumerate(families))
    caps+=(CapabilityRoot(capability=ref('synthetic.dynamic'),operation=ref('synthetic.dynamic.operation'),roots=(ref('dynamic-hook'),)),)
    inventory=change(inventory,consumers=consumer_facts(caps))
    return qualify(change(m,inventory=inventory,nodes=tuple(f.node for f in facts),
        edges=tuple(DependencyEdge(consumer=f.node.node,dependency=d) for f in facts for d in f.dependencies),capabilities=caps))


def test_first_slice_reference_has_qualified_toy_families_and_explicit_unknown_boundary():
    r=verify_manifest(first_slice_reference())
    assert (r.node_count,len(r.capabilities))==(13,14)
    assert len([c for c in r.capabilities if c.status=='COMPLETE_UNDER_SYNTHETIC_ASSUMPTIONS'])==13
    assert next(c for c in r.capabilities if c.capability==ref('synthetic.dynamic')).status=='UNKNOWN_DYNAMIC'
    assert not r.discovery_complete_under_assumptions and not r.authorizes_execution


def test_shared_parser_mutation_reaches_all_toy_families_with_known_closures():
    m=first_slice_reference();n=mutate_content(m,'parser')
    a={c.capability:c for c in verify_manifest(m).capabilities}
    for c in verify_manifest(n).capabilities:
        if c.capability!=ref('synthetic.dynamic'):
            assert c.implementation!=a[c.capability].implementation


def test_maximum_valid_report_stays_inside_har04_transport_bound():
    # Worst-case identifier lengths, deep closure, sixteen capability reports.
    names=['n'+str(i).zfill(3)+'x'*124 for i in range(128)]
    facts=tuple(InventoryFact(node=DependencyNode(node=ref(name),kind='SHARED_LIBRARY',content=content('source'),source_key=name),
        dependencies=(ref(names[i+1]),) if i+1<len(names) else ()) for i,name in enumerate(names))
    inventory=SourceInventory(inventory=ref('maximal-synthetic'),source_boundary=content(),facts=facts,discovery='BOUNDED_SYNTHETIC')
    caps=tuple(CapabilityRoot(capability=ref('cap'+str(i)),operation=ref('operation'+str(i)),roots=(ref(names[0]),)) for i in range(16))
    inventory=change(inventory,consumers=consumer_facts(caps))
    m=qualify(DependencyManifest(manifest=ref('maximal'),policy=DependencyPolicy(),nodes=tuple(f.node for f in facts),
        edges=tuple(DependencyEdge(consumer=f.node.node,dependency=d) for f in facts for d in f.dependencies),capabilities=caps,inventory=inventory))
    report=verify_manifest(m)
    assert report.discovery_complete_under_assumptions
    assert len(canonical_json(report).encode())<=1048576


def test_consumer_claim_cannot_override_independent_full_tree_fact():
    m=fixture(True)
    n=change(m,capabilities=tuple(change(c,consumes_full_tree=False,source_mode='NARROW_TRANSITIVE',broad_source=None) for c in m.capabilities))
    assert not verify_manifest(n).discovery_complete_under_assumptions
    assert 'consumer_scope_conflict' in closure(n).reasons


def test_missing_consumer_scope_cannot_be_made_complete_by_closed_node_graph():
    m=fixture();n=qualify(change(m,inventory=change(m.inventory,consumers=())))
    assert closure(n).implementation is None and 'consumer_scope_unqualified' in closure(n).reasons
