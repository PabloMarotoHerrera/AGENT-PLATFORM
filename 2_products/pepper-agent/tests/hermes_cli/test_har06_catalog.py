"""Declarative semantics only; no registry/tool imports or runtime fixtures."""
import json

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness import (
    CapabilityDescriptor, ContractRef, ContinuationKind, Effect, ExecutionRequest,
    AdmissibilityDecision, TransitionDescriptor, canonical_json,
)
from hermes_cli.agent_platform.harness.catalog import (
    CatalogDocument, CatalogLookup, CatalogSnapshot, LookupStatus, build_catalog,
    deserialize_catalog, serialize_catalog,
)
from hermes_cli.agent_platform.handler_correspondence import (
    BindingEvidence, BindingStatus, HandlerDeclaration, Selector, inspect_correspondence,
)
from hermes_cli.agent_platform.pre_review_catalog import (
    ContinuationTemplate, ProductOperation, continuation_templates,
    materialize_continuation, product_catalog, product_operations,
)


def ref(name='sample',version=1):return ContractRef(contract_id=name,version=version)
def cap(name='sample',version=1,effect=Effect.COMPUTE):
    return CapabilityDescriptor(capability=ref(name,version),input_schema=ref('input'),output_schema=ref('output'),
        effect=effect,required_authority_kinds=('approval',),evidence_contract=ref('evidence'),execution_adapter=ref('uninstalled.adapter'))
def trans(c,name='transition',authorities=('approval','additional')):
    return TransitionDescriptor(transition=ref(name),source_requirement=ref('source'),capability=c.capability,
        prerequisites=(ref('prerequisite'),),required_authority_kinds=authorities,effect=c.effect,
        target_rule=ref('target'),failure_code='failure',conflict_code='conflict',continuation_rule=ref('continuation'))
def change(model,**updates):return type(model).model_validate({**dict(model),**updates})


def test_empty_catalog_is_explicitly_supported_and_exact_lookup_qualified():
    s=build_catalog(ref('catalog'))
    assert s.list_capabilities()==s.list_transitions()==s.external_references()==()
    assert s.resolve_capability(ref()).status==LookupStatus.NOT_DECLARED
    assert s.resolve_transition(ref()).status==LookupStatus.NOT_DECLARED
    assert deserialize_catalog(serialize_catalog(s))==s


@pytest.mark.parametrize('effect',list(Effect))
def test_effect_examples_do_not_resolve_implementation_or_authority(effect):
    c=cap('sample.'+effect.value.lower(),effect=effect);t=trans(c);s=build_catalog(ref('catalog'),(c,),(t,))
    result=s.resolve_capability(c.capability)
    assert result.status==LookupStatus.DECLARED and result.capability==c
    assert s.resolve_transition(t.transition).transition==t
    assert result.catalog_content==s.content_identity()
    for target in (ExecutionRequest,AdmissibilityDecision):
        with pytest.raises(ValidationError):target.model_validate_json(canonical_json(result))
    for extra in ('available','authorized','handler','check_fn','execution_request'):
        with pytest.raises(ValidationError):change(result,**{extra:True})
    assert c.execution_adapter in s.external_references()


def test_versions_are_exact_without_newest_fallback_and_multiple_transitions_work():
    a,b=cap(version=1),cap(version=2);x,y=trans(a,'x'),trans(a,'y')
    s=build_catalog(ref('catalog'),(b,a),(y,x))
    assert s.resolve_capability(ref(version=1)).capability==a
    assert s.resolve_capability(ref(version=2)).capability==b
    assert s.resolve_capability(ref(version=3)).status==LookupStatus.UNSUPPORTED_VERSION
    assert s.resolve_transition(ref('x',2)).status==LookupStatus.UNSUPPORTED_VERSION
    assert s.transitions_for(a.capability)==(x,y)
    with pytest.raises(ValueError):s.transitions_for(ref('missing'))
    for invalid in ('sample',{},None,ref().model_copy(update={'version':True})):
        assert s.resolve_capability(invalid).status==LookupStatus.INVALID_REFERENCE


@pytest.mark.parametrize('case',('duplicate_cap','conflicting_cap','duplicate_transition','missing_cap','effect','weakened'))
def test_catalog_contradictions_fail_closed(case):
    c=cap();t=trans(c);caps=(c,);ts=(t,)
    if case=='duplicate_cap':caps=(c,c)
    if case=='conflicting_cap':caps=(c,change(c,effect=Effect.PHYSICAL_CONTROL))
    if case=='duplicate_transition':ts=(t,t)
    if case=='missing_cap':caps=()
    if case=='effect':ts=(change(t,effect=Effect.EXTERNAL_WRITE),)
    if case=='weakened':ts=(change(t,required_authority_kinds=()),)
    with pytest.raises(ValidationError):build_catalog(ref('catalog'),caps,ts)


def test_order_digest_and_roundtrip_preserve_descriptor_sequence_semantics():
    a,b=cap('a'),cap('b');x,y=trans(a,'x'),trans(b,'y')
    s=build_catalog(ref('catalog'),(a,b),(x,y));r=build_catalog(ref('catalog'),(b,a),(y,x))
    assert s==r and serialize_catalog(s)==serialize_catalog(r) and s.content_identity()==r.content_identity()
    t=change(x,prerequisites=(ref('one'),ref('two')))
    left=build_catalog(ref('catalog'),(a,),(t,))
    right=build_catalog(ref('catalog'),(a,),(change(t,prerequisites=tuple(reversed(t.prerequisites))),))
    assert left.content_identity()!=right.content_identity()
    document=json.loads(serialize_catalog(s));document['content']['sha256']='0'*64
    with pytest.raises(ValidationError):deserialize_catalog(json.dumps(document))
    assert deserialize_catalog(serialize_catalog(s))==s
    assert change(s,catalog=ref('catalog',2)).content_identity()!=s.content_identity()
    from hermes_cli.agent_platform.harness import ContentRef
    dependency=ContentRef(content_id='declarations',sha256='0'*64)
    assert change(s,declaration_inputs=(dependency,)).content_identity()!=s.content_identity()
    with pytest.raises(ValidationError):change(s,declaration_inputs=(dependency,dependency))


def test_versions_unknown_fields_callbacks_bounds_and_unsafe_copies_are_rejected():
    c=cap();s=build_catalog(ref('catalog'),(c,))
    for updates in ({'schema_version':2},{'schema_version':True},{'handler':lambda:True},
                    {'capabilities':(c,)*65},{'transitions':(trans(c),)*129}):
        with pytest.raises(ValidationError):change(s,**updates)
    with pytest.raises(ValidationError):s.capabilities=()
    with pytest.raises(ValueError):deserialize_catalog(' '*1_048_577)
    inconsistent=s.model_copy(update={'transitions':(trans(cap('missing')), )})
    assert inconsistent.resolve_capability(c.capability).status==LookupStatus.CATALOG_INCONSISTENCY
    with pytest.raises(ValidationError):serialize_catalog(inconsistent)


def test_catalog_specific_byte_bound_is_enforced_with_valid_collection_sizes():
    c=cap();base=trans(c)
    kinds=tuple('kind'+str(i)+'x'*120 for i in range(31))+('approval',)
    refs=tuple(ref('reference'+str(i)+'x'*110) for i in range(32))
    declarations=tuple(change(base,transition=ref('t'+str(i)),prerequisites=refs,
                             required_authority_kinds=kinds) for i in range(128))
    with pytest.raises(ValidationError,match='catalog_transport_bound'):
        build_catalog(ref('catalog'),(c,),declarations)


def test_qualified_lookup_cannot_publish_conflicting_or_grant_fields():
    c=cap();s=build_catalog(ref('catalog'),(c,));lookup=s.resolve_capability(c.capability)
    for updates in ({'status':LookupStatus.NOT_DECLARED},{'reference':ref('other')},
                    {'catalog_content':None},{'transition':trans(c)}):
        with pytest.raises(ValidationError):change(lookup,**updates)
    original=serialize_catalog(s)
    s.resolve_capability(ref('absent'))
    assert serialize_catalog(s)==original


def source(tool='tool',symbol='_handler',values=('inspect','request')):
    # The leading exception/callbacks prove these bytes are never executed.
    return ("from tools.registry import registry\nraise AssertionError('must never execute source')\n"
        "def _handler(args):\n    raise AssertionError('must never invoke handler')\n"
        f"registry.register(name={tool!r}, schema={{'parameters':{{'properties':{{'operation':{{'enum':{list(values)!r}}}}}}}}},handler={symbol},check_fn=lambda: 1/0)\n").encode()
def declaration():
    return HandlerDeclaration(capability=ref(),tool_name='tool',handler_symbol='_handler',
        selectors=(Selector(field='operation',value='inspect'),))


@pytest.mark.parametrize('variant,status',[
    ('valid',BindingStatus.VERIFIED),('absent',BindingStatus.ABSENT),
    ('duplicate',BindingStatus.AMBIGUOUS),('handler',BindingStatus.CONTRADICTORY),
    ('selector',BindingStatus.CONTRADICTORY),('dynamic',BindingStatus.UNVERIFIABLE),
    ('syntax',BindingStatus.UNVERIFIABLE),('decorator',BindingStatus.UNVERIFIABLE),
    ('late',BindingStatus.CONTRADICTORY),('schema_call',BindingStatus.UNVERIFIABLE),
    ('owner',BindingStatus.UNVERIFIABLE),('rebound',BindingStatus.UNVERIFIABLE),
])
def test_passive_binding_qualifies_failures_without_running_source(variant,status):
    raw=source()
    if variant=='absent':raw=source(tool='other')
    if variant=='duplicate':raw+=raw[raw.index(b'registry.register'):]
    if variant=='handler':raw=source(symbol='_other')
    if variant=='selector':raw=source(values=('request',))
    if variant=='dynamic':raw=raw.replace(b"name='tool'",b'name=discover_name()')
    if variant=='syntax':raw=b'not python!!!'
    if variant=='decorator':raw=raw.replace(b'def _handler',b'@decorate\ndef _handler')
    if variant=='late':raw=b"registry.register(name='tool',handler=_handler,schema={})\ndef _handler(args):pass\n"
    if variant=='schema_call':raw=raw.replace(b"['inspect', 'request']",b'probe_availability()')
    if variant=='owner':raw=raw.replace(b'from tools.registry import registry',b'from other.registry import registry')
    if variant=='rebound':raw=raw.replace(b'registry.register',b'registry = other_registry\nregistry.register')
    before=raw;result=inspect_correspondence(raw,declaration())
    assert result.status==status and raw==before
    if status==BindingStatus.VERIFIED:
        assert result.handler_ast_sha256 and result.registration_ast_sha256
        assert result.source.sha256 and result.handler_line<result.registration_line
    assert inspect_correspondence(raw,declaration())==result


def test_binding_limits_literal_paths_and_callback_fields_are_inert():
    with pytest.raises(ValueError):inspect_correspondence(b' '*2_097_153,declaration())
    with pytest.raises(TypeError):inspect_correspondence('path/to/module.py',declaration())
    for updates in ({'handler_symbol':'module.run()'},{'callback':lambda:True}):
        with pytest.raises(ValidationError):change(declaration(),**updates)
    with pytest.raises(ValidationError):HandlerDeclaration(capability=ref(),tool_name='tool',handler_symbol='_h',selectors=(Selector(field='x',value='a'),)*2)


def test_product_slice_reuses_existing_tool_names_and_real_continuation_classes():
    operations=product_operations();catalog=product_catalog()
    assert catalog.declaration_inputs[0].content_id=='pepper-operation-declarations'
    assert tuple(o.capability for o in sorted(operations,key=lambda o:o.capability.capability.contract_id))==catalog.capabilities
    assert {o.handler.tool_name for o in operations} >= {'prepare_current_ticket_review','request_current_ticket_material_revision','revise_current_ticket_for_material_contract_failure'}
    assert all(o.policy and o.inspector and o.invalidation and o.capability.recovery_policy for o in operations)
    templates=continuation_templates()
    assert {t.kind for t in templates}==set(ContinuationKind)
    from hermes_cli.agent_platform.harness import ActorRef,Scope
    scope=Scope(project_id='p',workflow_id='w',resource_ids=('r',));actor=ActorRef(actor_id='a')
    for template in templates:
        if template.kind==ContinuationKind.EXECUTABLE_CAPABILITY:
            with pytest.raises(ValueError):materialize_continuation(template,scope,actor)
            with pytest.raises(ValueError):materialize_continuation(template,scope,actor,b'')
        else:
            value=materialize_continuation(template,scope,actor)
            assert value.capability is None
            with pytest.raises(ValueError):materialize_continuation(template,scope,actor,source())
    executable=next(t for t in templates if t.kind==ContinuationKind.EXECUTABLE_CAPABILITY)
    op=next(o for o in operations if o.capability.capability==executable.operation)
    raw=(f'from tools.registry import registry\ndef {op.handler.handler_symbol}(args):pass\nregistry.register(name={op.handler.tool_name!r},handler={op.handler.handler_symbol},schema={{"parameters":{{"properties":{{"operation":{{"enum":["run_commands"]}}}}}}}})\n').encode()
    offer=materialize_continuation(executable,scope,actor,raw)
    assert offer.capability==op.capability.capability
    with pytest.raises(ValidationError):ExecutionRequest.model_validate_json(canonical_json(offer))


def test_new_public_models_roundtrip_and_remain_immutable():
    from hermes_cli.agent_platform.harness.validation import parse_contract
    s=product_catalog();binding=inspect_correspondence(source(),declaration())
    values=(s,CatalogDocument(snapshot=s,content=s.content_identity()),s.resolve_capability(ref('O01')),
        Selector(field='operation',value='inspect'),declaration(),binding,product_operations()[0],continuation_templates()[0])
    for model in values:
        assert parse_contract(type(model),canonical_json(model))==model
        with pytest.raises(ValidationError):change(model,schema_version=2)
        with pytest.raises(ValidationError):change(model,authorized=True)
        with pytest.raises(ValidationError):model.schema_version=2


def test_historical_authority_is_not_a_catalog_reference_or_grant():
    from tests.hermes_cli.test_har04_harness_contracts import examples
    from hermes_cli.agent_platform.harness import AuthorityCurrentness
    old=change(examples()[9],currentness=AuthorityCurrentness.HISTORICAL)
    s=build_catalog(ref('catalog'),(cap(),))
    assert s.resolve_capability(old).status==LookupStatus.INVALID_REFERENCE
    assert old.currentness==AuthorityCurrentness.HISTORICAL
    with pytest.raises(ValidationError):change(s,authority=old)
