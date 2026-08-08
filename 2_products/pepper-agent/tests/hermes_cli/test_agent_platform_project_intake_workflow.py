from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.project_intake as pi
from hermes_cli.agent_platform.workflow import (
    GovernedWorkflowSnapshot,
    GovernedWorkflowState,
    HermesWorkflowRuntimeKind,
    ProjectContextReference,
    ProjectIntakeApproval,
    ProjectIntakeConstraint,
    ProjectIntakeDecision,
    ProjectIntakeError,
    ProjectIntakeFinding,
    ProjectIntakeFindingCode,
    ProjectIntakeFindingSeverity,
    ProjectIntakeIdentity,
    ProjectIntakeProjectKind,
    ProjectIntakeRequest,
    ProjectIntakeResult,
    ProjectIntakeState,
    ProjectIntakeSummary,
    ProjectRepositoryBinding,
    ProjectRoadmap,
    ProjectRoadmapItem,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_canonical_p18_project_intake_request,
    build_governed_workflow_identity,
    build_governed_workflow_transition,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    build_p17_workflow_binding,
    build_project_intake,
    summarize_project_intake,
    validate_project_intake_request,
    validate_project_intake_result,
)
from hermes_cli.agent_platform.work_packet import (
    build_canonical_p17_closure_request,
    build_p17_work_packet_execution_mvp_closure,
)
from tests.hermes_cli import (
    test_agent_platform_governed_workflow_state_machine as p18_0,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_non_critical_ticket_pilot as p17_8,
)


P18_1_EXPORTS = (
    "PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION",
    "PROJECT_INTAKE_WORKFLOW_POLICY_ID",
    "ProjectIntakeState",
    "ProjectIntakeDecision",
    "ProjectIntakeProjectKind",
    "ProjectIntakeFindingSeverity",
    "ProjectIntakeFindingCode",
    "ProjectIntakeIdentity",
    "ProjectRoadmapItem",
    "ProjectRoadmap",
    "ProjectRepositoryBinding",
    "ProjectIntakeConstraint",
    "ProjectContextReference",
    "ProjectIntakeApproval",
    "ProjectIntakeRequest",
    "ProjectIntakeFinding",
    "ProjectIntakeSummary",
    "ProjectIntakeResult",
    "ProjectIntakeError",
    "ProjectIntakeInputError",
    "ProjectIntakeIntegrityError",
    "ProjectIntakePolicyError",
    "ProjectIntakeStateError",
    "ProjectIntakeValidationError",
    "build_canonical_p18_project_intake_request",
    "validate_project_intake_request",
    "build_project_intake",
    "validate_project_intake_result",
    "summarize_project_intake",
)

PUBLIC_MODELS = (
    ProjectIntakeIdentity,
    ProjectRoadmapItem,
    ProjectRoadmap,
    ProjectRepositoryBinding,
    ProjectIntakeConstraint,
    ProjectContextReference,
    ProjectIntakeApproval,
    ProjectIntakeRequest,
    ProjectIntakeFinding,
    ProjectIntakeSummary,
    ProjectIntakeResult,
)

FORBIDDEN_PUBLIC_EXPORTS = (
    "ProjectIntakeExecutor",
    "ProjectManager",
    "ProjectRegistry",
    "execute_project_intake",
    "run_project_intake",
    "create_project_runtime",
    "execute_ticket_factory",
    "GitProjectInitializer",
    "GBrainProjectMemory",
    "PaperclipProject",
    "ProjectWorkflowEngine",
    "RoadmapEngine",
    "KanbanProjectModel",
    "WorkspaceAllocator",
    "TicketFactoryExecutor",
)

P18_0_COMMIT = "7b928e60ed4adf49bfb3e47ab9acf1119aaef870"


@pytest.fixture(scope="module")
def accepted_p17_closure(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_1")
    try:
        context = p17_8.non_delete_context(monkeypatch, root)
        pilot = p17_8.build_non_critical_ticket_pilot(
            p17_8.request_for_context(context)
        )
        request = build_canonical_p17_closure_request(non_critical_pilot_result=pilot)
        return build_p17_work_packet_execution_mvp_closure(request)
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="module")
def p17_binding(accepted_p17_closure):
    return build_p17_workflow_binding(accepted_p17_closure)


@pytest.fixture(scope="module")
def initial_snapshot(p17_binding):
    identity = build_governed_workflow_identity(
        project_id="P18",
        ticket_id="P18.1",
        ticket_revision=1,
        work_packet_id="WP-P18-1-R0001",
        work_packet_SHA256="b" * 64,
    )
    projection = build_hermes_workflow_projection(
        runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
        runtime_state="pepper:draft",
        task_id=None,
        board_or_queue_id=None,
        worker_id_present=False,
        workspace_binding_present=False,
        dependency_blocked=False,
        retry_state_present=False,
        reclaim_state_present=False,
    )
    return build_initial_governed_workflow_snapshot(
        identity=identity,
        P17_binding=p17_binding,
        runtime_projection=projection,
    )


@pytest.fixture(scope="module")
def approval():
    return pi.build_project_intake_approval(
        approved=True,
        approved_by_human=True,
        approval_statement="Human approves bounded P18.1 Pepper project intake context.",
    )


@pytest.fixture(scope="module")
def intake_request(initial_snapshot, approval):
    return build_canonical_p18_project_intake_request(
        initial_workflow_snapshot=initial_snapshot,
        committed_p18_0_commit=P18_0_COMMIT,
        approval=approval,
    )


@pytest.fixture(scope="module")
def intake_result(intake_request):
    return build_project_intake(intake_request)


@pytest.fixture(scope="module")
def public_model_instances(intake_request, intake_result):
    return {
        ProjectIntakeIdentity: intake_request.identity,
        ProjectRoadmapItem: intake_request.roadmap.items[0],
        ProjectRoadmap: intake_request.roadmap,
        ProjectRepositoryBinding: intake_request.repository_binding,
        ProjectIntakeConstraint: intake_request.constraints[0],
        ProjectContextReference: intake_request.context_references[0],
        ProjectIntakeApproval: intake_request.approval,
        ProjectIntakeRequest: intake_request,
        ProjectIntakeFinding: intake_result.findings[0],
        ProjectIntakeSummary: intake_result.summary,
        ProjectIntakeResult: intake_result,
    }


def construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def request_with_updates(
    request: ProjectIntakeRequest, **updates
) -> ProjectIntakeRequest:
    data = {
        field: getattr(request, field) for field in ProjectIntakeRequest.model_fields
    }
    data.update(updates)
    return ProjectIntakeRequest.model_construct(**data)


def valid_approval(
    statement: str = "Human approves bounded P18.1 Pepper project intake context.",
):
    return pi.build_project_intake_approval(
        approved=True,
        approved_by_human=True,
        approval_statement=statement,
    )


def invalid_request_raises(request: ProjectIntakeRequest) -> None:
    with pytest.raises(ProjectIntakeError):
        validate_project_intake_request(request)


@pytest.mark.parametrize("exported_name", P18_1_EXPORTS)
def test_all_p18_1_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(pi, exported_name)


def test_p18_0_exports_are_exact_prefix_after_p18_1() -> None:
    p18_0_count = len(p18_0.P18_0_EXPORTS)
    p18_1_count = len(P18_1_EXPORTS)
    assert len(p18_0.P18_0_EXPORTS) == 38
    assert tuple(workflow.__all__[:p18_0_count]) == p18_0.P18_0_EXPORTS
    assert tuple(pi.__all__) == P18_1_EXPORTS
    assert tuple(workflow.__all__[p18_0_count : p18_0_count + p18_1_count]) == (
        P18_1_EXPORTS
    )
    assert len(P18_1_EXPORTS) == 29
    assert len(workflow.__all__) >= 67
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_project_runtime_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert not hasattr(workflow, forbidden)
    assert forbidden not in pi.__all__


@pytest.mark.parametrize(
    "enum_type",
    [
        ProjectIntakeState,
        ProjectIntakeDecision,
        ProjectIntakeProjectKind,
        ProjectIntakeFindingSeverity,
        ProjectIntakeFindingCode,
    ],
)
def test_controlled_enums_reject_unknown_values(enum_type: type[Enum]) -> None:
    with pytest.raises(ValueError):
        enum_type("unknown")


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_are_frozen(
    model_type: type[BaseModel], public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    with pytest.raises(ValidationError):
        setattr(instance, next(iter(model_type.model_fields)), "mutated")


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_forbid_extra_fields(
    model_type: type[BaseModel], public_model_instances
) -> None:
    data = public_model_instances[model_type].model_dump(mode="json")
    data["extra"] = "forbidden"
    with pytest.raises(ValidationError):
        model_type.model_validate(data)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_json_round_trip(
    model_type: type[BaseModel], public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    assert model_type.model_validate_json(instance.model_dump_json()) == instance


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_model_schema_additional_properties_false(
    model_type: type[BaseModel],
) -> None:
    assert model_type.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_use_safe_field_types(model_type: type[BaseModel]) -> None:
    forbidden = {
        "Any",
        "dict",
        "Mapping",
        "MutableMapping",
        "Path",
        "datetime",
        "UUID",
        "bytes",
        "Callable",
    }
    annotations = {field.annotation for field in model_type.model_fields.values()}
    annotation_text = "\n".join(str(item) for item in annotations)
    assert not any(name in annotation_text for name in forbidden)


@pytest.mark.parametrize(
    "field_name", ["approval_required", "approved", "approved_by_human"]
)
def test_strict_booleans_for_approval(
    field_name: str, approval: ProjectIntakeApproval
) -> None:
    data = approval.model_dump(mode="json")
    data[field_name] = "true"
    with pytest.raises(ValidationError):
        ProjectIntakeApproval.model_validate(data)


@pytest.mark.parametrize("field_name", ["completed", "current", "deferred"])
def test_strict_booleans_for_roadmap_item(
    field_name: str, intake_request: ProjectIntakeRequest
) -> None:
    data = intake_request.roadmap.items[0].model_dump(mode="json")
    data[field_name] = 1
    with pytest.raises(ValidationError):
        ProjectRoadmapItem.model_validate(data)


def test_tuple_immutability_retained(intake_request: ProjectIntakeRequest) -> None:
    assert isinstance(intake_request.constraints, tuple)
    assert isinstance(intake_request.context_references, tuple)
    assert isinstance(intake_request.roadmap.items, tuple)
    with pytest.raises(AttributeError):
        intake_request.constraints.append(intake_request.constraints[0])


def test_schema_and_policy_constants_are_exact() -> None:
    assert pi.PROJECT_INTAKE_WORKFLOW_SCHEMA_VERSION == 1
    assert (
        pi.PROJECT_INTAKE_WORKFLOW_POLICY_ID
        == "pepper-governed-project-intake-workflow-v1"
    )


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("project_id", "OTHER"),
        ("project_name", "Other"),
        ("project_kind", "unknown"),
        ("macroproject_id", "P19"),
        ("macroproject_title", "Other Migration"),
        ("roadmap_id", "P18-other"),
        ("project_id", ""),
        ("project_name", "Pepper\nProject"),
    ),
)
def test_project_identity_rejects_invalid_values(
    intake_request: ProjectIntakeRequest, field_name: str, value: str
) -> None:
    identity = construct_with_updates(intake_request.identity, **{field_name: value})
    invalid_request_raises(request_with_updates(intake_request, identity=identity))


def test_project_identity_digest_tampering_fails(
    intake_request: ProjectIntakeRequest,
) -> None:
    identity = construct_with_updates(intake_request.identity, identity_SHA256="0" * 64)
    invalid_request_raises(request_with_updates(intake_request, identity=identity))


@pytest.mark.parametrize(
    "unsafe",
    (
        "line\nbreak",
        "carriage\rreturn",
        "nul\x00byte",
        "\x1b[31mansi",
        "password=value",
        "access_token value",
        "authorization: bearer value",
        "sk-abcdefghijklmnop",
        "raw prompt text",
        "reasoning trace text",
        "provider response text",
        "ChatGPT transcript text",
        "OpenCode transcript text",
        "stdout: raw output",
        "stderr: raw output",
        "diff --git a b",
        "git commit -m bad",
        "docker run image",
        "python -c print(1)",
        "C:\\Users\\pablo\\secret",
    ),
)
def test_unsafe_text_content_rejected_in_identity(
    unsafe: str, intake_request: ProjectIntakeRequest
) -> None:
    identity = construct_with_updates(intake_request.identity, project_name=unsafe)
    invalid_request_raises(request_with_updates(intake_request, identity=identity))


def test_canonical_p18_roadmap_properties(intake_request: ProjectIntakeRequest) -> None:
    roadmap = intake_request.roadmap
    assert len(roadmap.items) == 10
    assert roadmap.macroproject_id == "P18"
    assert roadmap.current_ticket_id == "P18.1"
    assert roadmap.completed_ticket_ids == ("P18.0",)
    assert roadmap.next_ticket_ids == ("P18.2",)
    assert roadmap.items[0].completed is True
    assert roadmap.items[1].current is True
    assert not any(item.completed for item in roadmap.items[2:])


@pytest.mark.parametrize(
    "index,ticket_id",
    tuple(
        enumerate((
            "P18.0",
            "P18.1",
            "P18.2",
            "P18.3",
            "P18.4",
            "P18.5",
            "P18.6",
            "P18.7",
            "P18.8",
            "P18.R",
        ))
    ),
)
def test_canonical_roadmap_ticket_sequence(
    index: int, ticket_id: str, intake_request: ProjectIntakeRequest
) -> None:
    assert intake_request.roadmap.items[index].ticket_id == ticket_id
    assert intake_request.roadmap.items[index].ordinal == index + 1


@pytest.mark.parametrize(
    "mutator",
    (
        lambda roadmap: construct_with_updates(roadmap.items[1], ticket_id="P18.0"),
        lambda roadmap: construct_with_updates(roadmap.items[1], ordinal=1),
        lambda roadmap: construct_with_updates(roadmap.items[2], current=True),
        lambda roadmap: construct_with_updates(roadmap.items[0], current=True),
        lambda roadmap: construct_with_updates(roadmap.items[1], completed=True),
        lambda roadmap: construct_with_updates(roadmap.items[1], deferred=True),
        lambda roadmap: construct_with_updates(
            roadmap.items[2], prerequisite_ticket_ids=("P99.0",)
        ),
        lambda roadmap: construct_with_updates(
            roadmap.items[2], prerequisite_ticket_ids=("P18.2",)
        ),
        lambda roadmap: construct_with_updates(
            roadmap.items[2], roadmap_item_SHA256="0" * 64
        ),
    ),
)
def test_invalid_roadmap_item_shapes_fail(
    mutator, intake_request: ProjectIntakeRequest
) -> None:
    roadmap = intake_request.roadmap
    replacement = mutator(roadmap)
    items = tuple(
        replacement
        if item.ticket_id == replacement.ticket_id
        or item.ordinal == replacement.ordinal
        else item
        for item in roadmap.items
    )
    if replacement.ticket_id == "P18.0" and replacement.ordinal == 2:
        items = (roadmap.items[0], replacement, *roadmap.items[2:])
    invalid_roadmap = construct_with_updates(roadmap, items=items)
    invalid_request_raises(
        request_with_updates(intake_request, roadmap=invalid_roadmap)
    )


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("roadmap_id", "P18-other"),
        ("macroproject_id", "P17"),
        ("current_ticket_id", "P18.2"),
        ("completed_ticket_ids", ("P18.0", "P18.1")),
        ("next_ticket_ids", ("P18.3",)),
        ("roadmap_SHA256", "0" * 64),
    ),
)
def test_invalid_roadmap_fields_fail(
    intake_request: ProjectIntakeRequest, field_name: str, value
) -> None:
    roadmap = construct_with_updates(intake_request.roadmap, **{field_name: value})
    invalid_request_raises(request_with_updates(intake_request, roadmap=roadmap))


def test_repository_binding_canonical_values(
    intake_request: ProjectIntakeRequest,
) -> None:
    binding = intake_request.repository_binding
    assert binding.repository_display_name == "AGENT PLATFORM"
    assert binding.expected_branch == "p18-manual-to-hermes-workflow-migration"
    assert binding.product_root == "2_products/pepper-agent"
    assert binding.branch_parent_commit == P18_0_COMMIT
    assert binding.upstream_main_commit == "92d1e790e70176ed542b1ae44d6e8af771be512b"
    assert binding.branch_policy == "one_branch_per_macroproject;one_commit_per_ticket"


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("repository_id", "OTHER"),
        ("repository_display_name", "Other Repo"),
        ("expected_branch", "main"),
        ("product_root", "C:\\Users\\pablo\\pepper-agent"),
        ("product_root", "../pepper-agent"),
        ("product_root", "2_products/other"),
        ("branch_parent_commit", "0" * 40),
        ("upstream_main_commit", "0" * 40),
        ("branch_policy", "branch_per_ticket"),
        ("repository_binding_SHA256", "0" * 64),
    ),
)
def test_invalid_repository_binding_fails(
    intake_request: ProjectIntakeRequest, field_name: str, value: str
) -> None:
    binding = construct_with_updates(
        intake_request.repository_binding, **{field_name: value}
    )
    invalid_request_raises(
        request_with_updates(intake_request, repository_binding=binding)
    )


def test_canonical_constraints_cover_required_boundaries(
    intake_request: ProjectIntakeRequest,
) -> None:
    descriptions = "\n".join(
        item.description.lower() for item in intake_request.constraints
    )
    assert len(intake_request.constraints) == 10
    assert "customized hermes-derived product" in descriptions
    assert "reuse and customize inherited" in descriptions
    assert "duplicate equivalent runtime" in descriptions
    assert "human git authority remains required" in descriptions
    assert "g-brain are deferred to p19" in descriptions
    assert "paperclip durable work-control authority is deferred to p20" in descriptions
    assert "multi-agent automation is deferred to p21" in descriptions


@pytest.mark.parametrize("constraint", range(10))
def test_each_canonical_constraint_is_blocking(
    constraint: int, intake_request: ProjectIntakeRequest
) -> None:
    assert intake_request.constraints[constraint].blocking is True


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("constraint_id", "PIC-001"),
        ("category", "unknown"),
        ("description", "password=value"),
        ("description", "raw prompt copied here"),
        ("source", "stdout: output"),
        ("constraint_SHA256", "0" * 64),
    ),
)
def test_invalid_constraint_inventory_fails(
    intake_request: ProjectIntakeRequest, field_name: str, value: str
) -> None:
    target_index = 1 if field_name == "constraint_id" else 0
    target = intake_request.constraints[target_index]
    replacement = construct_with_updates(target, **{field_name: value})
    constraints = tuple(
        replacement if index == target_index else item
        for index, item in enumerate(intake_request.constraints)
    )
    invalid_request_raises(
        request_with_updates(intake_request, constraints=constraints)
    )


@pytest.mark.parametrize("drop_index", range(10))
def test_missing_each_canonical_constraint_blocks(
    drop_index: int, intake_request: ProjectIntakeRequest
) -> None:
    constraints = tuple(
        item
        for index, item in enumerate(intake_request.constraints)
        if index != drop_index
    )
    invalid_request_raises(
        request_with_updates(intake_request, constraints=constraints)
    )


def test_context_references_are_bounded_not_content_snapshots(
    intake_request: ProjectIntakeRequest,
) -> None:
    assert len(intake_request.context_references) == 6
    joined = "\n".join(
        f"{item.reference_name} {item.source_scope}"
        for item in intake_request.context_references
    ).lower()
    assert "raw prompt" not in joined
    assert "transcript" not in joined
    assert "diff --git" not in joined
    assert "stdout:" not in joined
    assert all(item.required for item in intake_request.context_references)


@pytest.mark.parametrize("reference_index", range(6))
def test_each_context_reference_has_digest(
    reference_index: int, intake_request: ProjectIntakeRequest
) -> None:
    assert (
        len(intake_request.context_references[reference_index].reference_SHA256) == 64
    )


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("reference_id", "PCTX-001"),
        ("reference_kind", "snapshot"),
        ("reference_name", "OpenCode transcript copied"),
        ("source_scope", "diff --git raw content"),
        ("authority", "runtime"),
        ("required", False),
        ("reference_SHA256", "0" * 64),
    ),
)
def test_invalid_context_references_fail(
    intake_request: ProjectIntakeRequest, field_name: str, value
) -> None:
    target_index = 1 if field_name == "reference_id" else 0
    target = intake_request.context_references[target_index]
    replacement = construct_with_updates(target, **{field_name: value})
    references = tuple(
        replacement if index == target_index else item
        for index, item in enumerate(intake_request.context_references)
    )
    invalid_request_raises(
        request_with_updates(intake_request, context_references=references)
    )


def test_human_approval_is_declarative_not_signature(
    approval: ProjectIntakeApproval,
) -> None:
    assert approval.approval_required is True
    assert approval.approved is True
    assert approval.approved_by_human is True
    assert "signature" not in ProjectIntakeApproval.model_fields
    assert "credential" not in approval.approval_statement.lower()


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("approval_required", False),
        ("approved", False),
        ("approved_by_human", False),
        ("approval_statement", "password=value"),
        ("approval_statement", "raw conversation copied"),
        ("approval_scope", "stdout: output"),
        ("approval_SHA256", "0" * 64),
    ),
)
def test_invalid_human_approval_blocks_intake(
    intake_request: ProjectIntakeRequest, field_name: str, value
) -> None:
    approval = construct_with_updates(intake_request.approval, **{field_name: value})
    invalid_request_raises(request_with_updates(intake_request, approval=approval))


def test_canonical_project_intake_requires_human_approval(
    initial_snapshot: GovernedWorkflowSnapshot,
) -> None:
    approval = pi.build_project_intake_approval(
        approved=True,
        approved_by_human=False,
        approval_statement="Human approval missing.",
    )
    with pytest.raises(ProjectIntakeError):
        build_canonical_p18_project_intake_request(
            initial_workflow_snapshot=initial_snapshot,
            committed_p18_0_commit=P18_0_COMMIT,
            approval=approval,
        )


def test_initial_workflow_snapshot_must_validate(
    intake_request: ProjectIntakeRequest,
) -> None:
    validate_project_intake_request(intake_request)
    assert (
        intake_request.initial_workflow_snapshot.current_state
        is GovernedWorkflowState.DRAFT
    )


def test_initial_workflow_snapshot_must_be_draft(
    intake_request: ProjectIntakeRequest, p17_binding
) -> None:
    non_draft = p18_0.make_snapshot(
        GovernedWorkflowState.INTAKE_READY,
        intake_request.initial_workflow_snapshot.identity,
        p17_binding,
    )
    invalid_request_raises(
        request_with_updates(intake_request, initial_workflow_snapshot=non_draft)
    )


def test_altered_workflow_identity_fails(intake_request: ProjectIntakeRequest) -> None:
    bad_identity = build_governed_workflow_identity(
        project_id="P17",
        ticket_id="P18.1",
        ticket_revision=1,
        work_packet_id="WP-P18-1-R0001",
        work_packet_SHA256="b" * 64,
    )
    bad_snapshot = construct_with_updates(
        intake_request.initial_workflow_snapshot,
        identity=bad_identity,
    )
    invalid_request_raises(
        request_with_updates(intake_request, initial_workflow_snapshot=bad_snapshot)
    )


def test_altered_snapshot_digest_fails(intake_request: ProjectIntakeRequest) -> None:
    bad_snapshot = construct_with_updates(
        intake_request.initial_workflow_snapshot,
        workflow_SHA256="0" * 64,
    )
    invalid_request_raises(
        request_with_updates(intake_request, initial_workflow_snapshot=bad_snapshot)
    )


def test_intake_uses_p18_0_transition_builder(
    intake_request: ProjectIntakeRequest,
) -> None:
    transition_request = pi.GovernedWorkflowTransitionRequest(
        schema_version=pi.GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=pi.GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=intake_request.initial_workflow_snapshot,
        trigger=WorkflowTransitionTrigger.PROJECT_INTAKE_COMPLETED,
        authority=WorkflowTransitionAuthority.SYSTEM,
        evidence_refs=("project_intake_evidence",),
        runtime_projection=intake_request.initial_workflow_snapshot.runtime_projection,
    )
    transition = build_governed_workflow_transition(transition_request)
    assert transition.accepted is True
    assert transition.transition.from_state is GovernedWorkflowState.DRAFT
    assert transition.transition.to_state is GovernedWorkflowState.INTAKE_READY
    assert (
        transition.resulting_snapshot.current_state
        is GovernedWorkflowState.INTAKE_READY
    )


def test_rejected_p18_0_transition_leaves_snapshot_unchanged(
    intake_request: ProjectIntakeRequest,
) -> None:
    transition_request = pi.GovernedWorkflowTransitionRequest(
        schema_version=pi.GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=pi.GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=intake_request.initial_workflow_snapshot,
        trigger=WorkflowTransitionTrigger.PROJECT_INTAKE_COMPLETED,
        authority=WorkflowTransitionAuthority.SYSTEM,
        evidence_refs=(),
        runtime_projection=intake_request.initial_workflow_snapshot.runtime_projection,
    )
    transition = build_governed_workflow_transition(transition_request)
    assert transition.accepted is False
    assert transition.resulting_snapshot == intake_request.initial_workflow_snapshot


def test_canonical_P18_project_intake_flow(intake_result: ProjectIntakeResult) -> None:
    assert intake_result.state is ProjectIntakeState.ACCEPTED
    assert intake_result.decision is ProjectIntakeDecision.ACCEPTED
    assert (
        intake_result.workflow_transition_result.transition.from_state
        is GovernedWorkflowState.DRAFT
    )
    assert (
        intake_result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.INTAKE_READY
    )
    assert intake_result.project_intake_requirement_satisfied is True
    assert intake_result.P18_2_ready is True


def test_canonical_project_intake_rejects_missing_human_approval(
    initial_snapshot: GovernedWorkflowSnapshot,
) -> None:
    approval = pi.build_project_intake_approval(
        approved=False,
        approved_by_human=True,
        approval_statement="Human approval intentionally absent.",
    )
    with pytest.raises(ProjectIntakeError):
        build_canonical_p18_project_intake_request(
            initial_workflow_snapshot=initial_snapshot,
            committed_p18_0_commit=P18_0_COMMIT,
            approval=approval,
        )


def test_canonical_project_intake_rejects_wrong_repository_binding(
    intake_request: ProjectIntakeRequest,
) -> None:
    bad_binding = construct_with_updates(
        intake_request.repository_binding, expected_branch="main"
    )
    invalid_request_raises(
        request_with_updates(intake_request, repository_binding=bad_binding)
    )


def test_accepted_intake_result_posture(intake_result: ProjectIntakeResult) -> None:
    assert intake_result.state.value == "accepted"
    assert intake_result.decision.value == "accepted"
    assert intake_result.summary.blocking_finding_count == 0
    assert intake_result.summary.project_intake_requirement_satisfied is True
    assert intake_result.summary.P18_2_ready is True
    assert intake_result.production_readiness_claimed is False
    assert intake_result.provider_dispatch_count == 0
    assert intake_result.model_inference_count == 0
    assert intake_result.Git_commands_executed == 0


@pytest.mark.parametrize("finding", range(12))
def test_intake_findings_are_info_and_contiguous(
    finding: int, intake_result: ProjectIntakeResult
) -> None:
    item = intake_result.findings[finding]
    assert item.finding_id == f"PINF-{finding + 1:03d}"
    assert item.severity is ProjectIntakeFindingSeverity.INFO
    assert item.failed_invariant is None


@pytest.mark.parametrize("code", tuple(ProjectIntakeFindingCode))
def test_every_finding_code_is_controlled(code: ProjectIntakeFindingCode) -> None:
    assert ProjectIntakeFindingCode(code.value) is code


def test_finding_digest_tampering_fails(intake_result: ProjectIntakeResult) -> None:
    bad_finding = construct_with_updates(
        intake_result.findings[0], finding_SHA256="0" * 64
    )
    bad_result = construct_with_updates(
        intake_result,
        findings=(bad_finding, *intake_result.findings[1:]),
    )
    with pytest.raises(ProjectIntakeError):
        validate_project_intake_result(bad_result)


def test_summary_api_returns_exact_summary(intake_result: ProjectIntakeResult) -> None:
    assert summarize_project_intake(intake_result) == intake_result.summary


def test_summary_digest_tampering_fails(intake_result: ProjectIntakeResult) -> None:
    bad_summary = construct_with_updates(intake_result.summary, summary_SHA256="0" * 64)
    bad_result = construct_with_updates(intake_result, summary=bad_summary)
    with pytest.raises(ProjectIntakeError):
        validate_project_intake_result(bad_result)


def test_result_digest_tampering_fails(intake_result: ProjectIntakeResult) -> None:
    bad_result = construct_with_updates(intake_result, result_SHA256="0" * 64)
    with pytest.raises(ProjectIntakeError):
        validate_project_intake_result(bad_result)


def test_intake_id_shape_and_determinism(intake_request: ProjectIntakeRequest) -> None:
    first = build_project_intake(intake_request)
    second = build_project_intake(intake_request)
    assert first == second
    assert first.intake_id == second.intake_id
    assert first.intake_id.startswith("PINT-P18-")
    assert len(first.intake_id) == len("PINT-P18-123456789abc")


def test_changed_roadmap_changes_intake_id(
    intake_request: ProjectIntakeRequest,
) -> None:
    altered_item = pi._make_model(
        ProjectRoadmapItem,
        "roadmap_item_SHA256",
        pi.PROJECT_ROADMAP_ITEM_DIGEST_ALGORITHM,
        ticket_id="P18.8",
        title="Controlled Default-Mode Cutover",
        ordinal=9,
        prerequisite_ticket_ids=("P18.7",),
        completed=False,
        current=False,
        deferred=True,
    )
    items = (
        *intake_request.roadmap.items[:8],
        altered_item,
        intake_request.roadmap.items[9],
    )
    roadmap = pi._make_model(
        ProjectRoadmap,
        "roadmap_SHA256",
        pi.PROJECT_ROADMAP_DIGEST_ALGORITHM,
        roadmap_id=intake_request.roadmap.roadmap_id,
        macroproject_id=intake_request.roadmap.macroproject_id,
        items=items,
        current_ticket_id="P18.1",
        completed_ticket_ids=("P18.0",),
        next_ticket_ids=("P18.2",),
    )
    changed = build_project_intake(
        request_with_updates(intake_request, roadmap=roadmap)
    )
    assert changed.intake_id != build_project_intake(intake_request).intake_id


def test_changed_repository_binding_changes_or_blocks_intake_id(
    intake_request: ProjectIntakeRequest,
) -> None:
    altered = construct_with_updates(
        intake_request.repository_binding,
        branch_parent_commit="0" * 40,
    )
    invalid_request_raises(
        request_with_updates(intake_request, repository_binding=altered)
    )


def test_changed_approval_changes_intake_id(
    intake_request: ProjectIntakeRequest,
) -> None:
    changed = valid_approval(
        "Human approves bounded P18.1 Pepper project intake context again."
    )
    changed_request = request_with_updates(intake_request, approval=changed)
    assert (
        build_project_intake(changed_request).intake_id
        != build_project_intake(intake_request).intake_id
    )


def test_no_clock_uuid_or_randomness_in_public_result(
    intake_result: ProjectIntakeResult,
) -> None:
    payload = intake_result.model_dump_json().lower()
    assert "uuid" not in payload
    assert "timestamp" not in payload
    assert "random" not in payload
    assert "hostname" not in payload
    assert "process" not in payload
    assert "thread" not in payload


def test_digest_is_not_signature(intake_result: ProjectIntakeResult) -> None:
    payload = intake_result.model_dump_json().lower()
    assert "signature" not in payload
    assert "digital signature" not in payload


@pytest.mark.parametrize(
    "forbidden_text",
    (
        "vector store",
        "memory database",
        "semantic memory",
        "chat-history memory",
        "persistent knowledge graph",
        "long-term context store",
        "Paperclip database",
        "durable work-control implementation",
        "Ticket Factory executor",
        "Kanban DB row",
        "provider dispatch authorized",
        "model inference authorized",
        "automatic Git authority",
        "production readiness true",
    ),
)
def test_result_does_not_claim_deferred_or_operational_authority(
    forbidden_text: str, intake_result: ProjectIntakeResult
) -> None:
    assert forbidden_text.lower() not in intake_result.model_dump_json().lower()


def test_p18_2_handoff_fields(intake_result: ProjectIntakeResult) -> None:
    assert intake_result.project_intake_requirement_satisfied is True
    assert (
        intake_result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.INTAKE_READY
    )
    assert intake_result.P18_2_ready is True
    assert intake_result.roadmap.next_ticket_ids == ("P18.2",)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_model_field_order_is_stable(model_type: type[BaseModel]) -> None:
    expected = {
        ProjectIntakeIdentity: (
            "project_id",
            "project_name",
            "project_kind",
            "macroproject_id",
            "macroproject_title",
            "roadmap_id",
            "identity_SHA256",
        ),
        ProjectRoadmapItem: (
            "ticket_id",
            "title",
            "ordinal",
            "prerequisite_ticket_ids",
            "completed",
            "current",
            "deferred",
            "roadmap_item_SHA256",
        ),
        ProjectRoadmap: (
            "roadmap_id",
            "macroproject_id",
            "items",
            "current_ticket_id",
            "completed_ticket_ids",
            "next_ticket_ids",
            "roadmap_SHA256",
        ),
        ProjectRepositoryBinding: (
            "repository_id",
            "repository_display_name",
            "expected_branch",
            "product_root",
            "branch_parent_commit",
            "upstream_main_commit",
            "branch_policy",
            "repository_binding_SHA256",
        ),
        ProjectIntakeConstraint: (
            "constraint_id",
            "category",
            "description",
            "blocking",
            "source",
            "constraint_SHA256",
        ),
        ProjectContextReference: (
            "reference_id",
            "reference_kind",
            "reference_name",
            "source_scope",
            "authority",
            "required",
            "reference_SHA256",
        ),
        ProjectIntakeApproval: (
            "approval_required",
            "approved",
            "approval_scope",
            "approved_by_human",
            "approval_statement",
            "approval_SHA256",
        ),
        ProjectIntakeRequest: (
            "schema_version",
            "policy_id",
            "identity",
            "roadmap",
            "repository_binding",
            "constraints",
            "context_references",
            "approval",
            "initial_workflow_snapshot",
        ),
        ProjectIntakeFinding: (
            "finding_id",
            "severity",
            "code",
            "subject_id",
            "summary",
            "failed_invariant",
            "finding_SHA256",
        ),
        ProjectIntakeSummary: (
            "project_identity_valid",
            "roadmap_valid",
            "repository_binding_valid",
            "constraints_valid",
            "context_references_valid",
            "human_approval_present",
            "workflow_transition_valid",
            "information_finding_count",
            "warning_finding_count",
            "blocking_finding_count",
            "project_intake_requirement_satisfied",
            "P18_2_ready",
            "summary_SHA256",
        ),
        ProjectIntakeResult: (
            "schema_version",
            "policy_id",
            "intake_id",
            "state",
            "decision",
            "identity",
            "roadmap",
            "repository_binding",
            "constraints",
            "context_references",
            "approval",
            "previous_workflow_snapshot_SHA256",
            "workflow_transition_result",
            "resulting_workflow_snapshot",
            "findings",
            "summary",
            "project_intake_requirement_satisfied",
            "P18_2_ready",
            "production_readiness_claimed",
            "provider_dispatch_count",
            "model_inference_count",
            "Git_commands_executed",
            "result_SHA256",
        ),
    }
    assert tuple(model_type.model_fields) == expected[model_type]


@pytest.mark.parametrize(
    "category",
    (
        "architecture",
        "authority",
        "security",
        "Git",
        "dependency",
        "runtime",
        "workflow",
        "reuse",
        "future_boundary",
    ),
)
def test_constraint_categories_are_controlled(category: str) -> None:
    constraint = pi._build_constraint(
        "PIC-999", category, "Bounded controlled constraint text.", "P18.1 test"
    )
    assert constraint.category == category


@pytest.mark.parametrize(
    "kind",
    (
        "canonical_document",
        "public_contract",
        "roadmap",
        "repository_metadata",
        "prior_ticket",
        "runtime_capability_analysis",
    ),
)
def test_reference_kinds_are_controlled(kind: str) -> None:
    reference = pi._build_reference(
        "PCTX-999",
        kind,
        "Bounded reference",
        "bounded scope",
        "supporting",
        required=True,
    )
    assert reference.reference_kind == kind


@pytest.mark.parametrize("authority", ("canonical", "supporting", "informational"))
def test_reference_authority_values_are_controlled(authority: str) -> None:
    reference = pi._build_reference(
        "PCTX-998",
        "public_contract",
        "Bounded reference",
        "bounded scope",
        authority,
        required=True,
    )
    assert reference.authority == authority


def test_product_identity_flags_are_reflected_by_constraints(
    intake_request: ProjectIntakeRequest,
) -> None:
    descriptions = "\n".join(item.description for item in intake_request.constraints)
    assert "customized Hermes-derived product" in descriptions
    assert "external wrapper" in descriptions


def test_reuse_boundary_no_duplicate_project_logic(
    intake_result: ProjectIntakeResult,
) -> None:
    assert "ProjectRegistry" not in workflow.__all__
    assert "RoadmapEngine" not in workflow.__all__
    assert "create_project_runtime" not in workflow.__all__
    assert intake_result.provider_dispatch_count == 0
    assert intake_result.model_inference_count == 0
    assert intake_result.Git_commands_executed == 0


def test_gbrain_and_paperclip_boundaries_are_deferred(
    intake_request: ProjectIntakeRequest,
) -> None:
    descriptions = "\n".join(item.description for item in intake_request.constraints)
    assert "deferred to P19" in descriptions
    assert "deferred to P20" in descriptions
    assert "deferred to P21" in descriptions
