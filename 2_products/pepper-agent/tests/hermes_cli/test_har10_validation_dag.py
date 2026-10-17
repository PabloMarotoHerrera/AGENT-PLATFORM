import json

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness.validation import canonical_json, parse_contract
from hermes_cli.agent_platform.harness.validation_dag import AcceptanceCriterion, ValidationDAG, ValidationObservation
from tests.hermes_cli.test_har10_validation_dag_verifier import (
    ASSUMPTION, CONTEXT, change, content, fixture, observation, ref,
)


def test_immutable_contract_and_nested_models():
    g=fixture()
    with pytest.raises(ValidationError): g.policy=ref("changed")
    with pytest.raises(ValidationError): g.requirements[0].description="changed"


@pytest.mark.parametrize("patch",[{"schema_version":2},{"schema_version":True},{"unknown":1},{"requirements":[]},{"policy":{"contract_id":"x","version":"1"}}])
def test_strict_models(patch):
    with pytest.raises(ValidationError):
        ValidationDAG.model_validate({**fixture().model_dump(),**patch})


def test_canonical_roundtrip():
    g=fixture()
    assert canonical_json(parse_contract(ValidationDAG,canonical_json(g)))==canonical_json(g)


def test_unordered_declarations_have_stable_identity():
    g=fixture(); r=change(g.requirements[0],requirement=ref("second")); d=change(g.dependencies[0],dependency_id="second-edge",consumer=r.requirement)
    g=change(g,requirements=(*g.requirements,r),dependencies=(*g.dependencies,d))
    assert g.identity()==change(g,requirements=g.requirements[::-1],dependencies=g.dependencies[::-1]).identity()


def test_description_is_presentation_only_for_native_semantics():
    g=fixture(); other=change(g,requirements=(change(g.requirements[0],description="V10 depends on V1-V9 misleading display only"),))
    assert g.identity()==other.identity()
    assert g.identity(presentation=True)!=other.identity(presentation=True)


@pytest.mark.parametrize("field",["condition","source","producer-version","human-authority"])
def test_semantic_identity_changes(field):
    g=fixture()
    if field=="condition": other=change(g,dependencies=(change(g.dependencies[0],condition="FAILED"),))
    elif field=="source": other=change(g,dependencies=(change(g.dependencies[0],expected_source=content("other")),))
    elif field=="producer-version": other=change(g,producers=(change(g.producers[0],producer=ref("runner",2)),))
    else: other=change(g,requirements=(change(g.requirements[0],human_authority=True),))
    assert g.identity()!=other.identity()


def test_observation_identity_binds_source_and_version():
    o=observation()
    assert o.identity()!=change(o,source=content("other")).identity()
    assert o.identity()!=change(o,evidence=ref("result",2)).identity()


@pytest.mark.parametrize("patch",[{"requirements":fixture().requirements*65},{"dependencies":fixture().dependencies*257},{"producers":fixture().producers*129},{"criteria":fixture().criteria*65}])
def test_graph_bounds(patch):
    with pytest.raises(ValidationError): change(fixture(),**patch)


def test_transport_bound_and_unknown_condition():
    data=json.loads(canonical_json(fixture())); data['dependencies'][0]['condition']='from-prose'
    with pytest.raises(ValidationError): parse_contract(ValidationDAG,json.dumps(data))
    with pytest.raises(ValueError): parse_contract(ValidationDAG,b' '*1048577)


def test_human_contract_rejects_machine_authority():
    with pytest.raises(ValidationError):
        AcceptanceCriterion(criterion=ref("v11-equivalent"),kind="HUMAN_ACCEPTANCE",required_facts=("PASSED",),authority_class="NONE",machine_evaluable=True,human_decision_required=False)


def test_inconsistent_status_cannot_hide_failed_outcome():
    with pytest.raises(ValidationError): change(observation(),outcome="FAILED")


def test_synthetic_qualification_cannot_claim_production_scope():
    with pytest.raises(ValidationError): change(ASSUMPTION,scope="PRODUCTION")
