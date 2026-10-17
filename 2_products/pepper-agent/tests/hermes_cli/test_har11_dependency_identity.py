import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness.contracts import AuthorityCurrentness, Scope
from hermes_cli.agent_platform.harness.dependency_identity import (
    AuthorityBindingRef, DependencyContext, HumanIntentRef, ImplementationRef,
    ResourceBindingRef, ValidationInputRef, bind_identity,
)
from hermes_cli.agent_platform.harness.dependency_manifest import POLICY
from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract
from hermes_cli.agent_platform.harness.validation_dag import ValidationContext
from tests.hermes_cli.test_har11_dependency_manifest import change, closure, content, fixture, ref


def context(m=None,cap='cap-a'):
    m=m or fixture(); c=closure(m,cap)
    def bound(model,name):
        return bind_identity(model,ref(name),source_contract=ref(name+'.schema'),provenance=content('synthetic-owner'))
    return DependencyContext(capability=ref(cap),operation=ref(cap+'.operation'),
        intent=bound(HumanIntentRef,'human-request'),authority=bound(AuthorityBindingRef,'immutable-decision'),
        implementation=ImplementationRef(content=c.implementation or content('unqualified-implementation'),source_contract=ref('implementation-schema'),provenance=content('synthetic-owner')),
        validation_inputs=(bound(ValidationInputRef,'validation-data'),),resource=bound(ResourceBindingRef,'resource'),
        scope=Scope(project_id='project-a',workflow_id='workflow-a',resource_ids=('resource-a',)),
        workflow_context=ValidationContext(current_ticket='predecessor',successor_ticket='successor',execution_target='predecessor',human_decision_target='predecessor',revision='R2',run='run45'),
        policy=POLICY,manifest=m.identity(),expected_versions=(ref('parser'),),provenance=content('synthetic-context-owner'),
        qualification='SYNTHETIC_ASSUMPTION',currentness=AuthorityCurrentness.CURRENT)


def test_five_domains_do_not_collapse_on_identical_payload():
    models=(HumanIntentRef,AuthorityBindingRef,ImplementationRef,ValidationInputRef,ResourceBindingRef)
    identities=[bind_identity(m,ref('same'),source_contract=ref('same'),provenance=content()) for m in models]
    assert len({v.content.sha256 for v in identities})==5
    assert len({v.domain for v in identities})==5


def test_typed_dimensions_and_immutable_context():
    c=context()
    with pytest.raises(ValidationError):c.intent=c.authority
    with pytest.raises(ValidationError):change(c,intent=c.authority)
    assert parse_contract(DependencyContext,canonical_json(c))==c


@pytest.mark.parametrize('patch',[{'schema_version':2},{'schema_version':True},{'extra':True},{'validation_inputs':[]},{'validation_inputs':context().validation_inputs*33}])
def test_strict_context(patch):
    with pytest.raises(ValidationError):change(context(),**patch)


def test_input_and_versions_are_unordered_unique_declarations():
    c=context();v=change(c.validation_inputs[0],content=content('other'))
    a=change(c,validation_inputs=(*c.validation_inputs,v),expected_versions=(ref('policy'),ref('parser')))
    b=change(a,validation_inputs=a.validation_inputs[::-1],expected_versions=a.expected_versions[::-1])
    assert a.identity()==b.identity()
    with pytest.raises(ValidationError):change(c,validation_inputs=c.validation_inputs*2)


def test_unknown_identity_type_cannot_select_code():
    with pytest.raises(TypeError):bind_identity(str,ref('x'),source_contract=ref('x'),provenance=content())


def test_manifest_bounds_and_unknown_dependency_kind():
    m=fixture()
    with pytest.raises(ValidationError):change(m,nodes=m.nodes*29)
    with pytest.raises(ValidationError):change(m,edges=m.edges*150)
    with pytest.raises(ValidationError):change(m.nodes[0],kind='guessed-from-extension')
    with pytest.raises(ValueError):parse_contract(DependencyContext,' '*1048577)
