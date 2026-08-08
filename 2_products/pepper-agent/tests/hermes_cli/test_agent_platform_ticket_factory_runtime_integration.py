from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.ticket_factory_runtime as tfr
from hermes_cli.agent_platform.ticket_factory import (
    ContextPack,
    ContextSensitivity,
    TicketDependencyPlan,
    TicketLintDisposition,
    TicketLintReport,
    TicketSpec,
    TicketType,
    WaveDisposition,
)
from hermes_cli.agent_platform.workflow import (
    GovernedWorkflowState,
    HermesWorkflowRuntimeKind,
    TicketFactoryRuntimeBinding,
    TicketFactoryRuntimeDecision,
    TicketFactoryRuntimeFinding,
    TicketFactoryRuntimeFindingCode,
    TicketFactoryRuntimeFindingSeverity,
    TicketFactoryRuntimeIntegrationError,
    TicketFactoryRuntimeIntegrationResult,
    TicketFactoryRuntimeRequest,
    TicketFactoryRuntimeState,
    TicketFactoryRuntimeSummary,
    TicketFactoryWorkPacketContinuation,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_canonical_p18_project_intake_request,
    build_canonical_p18_ticket_factory_runtime_request,
    build_governed_workflow_identity,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    build_p17_workflow_binding,
    build_project_intake,
    build_ticket_factory_runtime_integration,
    summarize_ticket_factory_runtime_integration,
    validate_ticket_factory_runtime_integration_result,
    validate_ticket_factory_runtime_request,
)
from hermes_cli.agent_platform.work_packet import (
    WorkPacketCompilationResult,
    build_canonical_p17_closure_request,
    build_p17_work_packet_execution_mvp_closure,
)
from tests.hermes_cli import (
    test_agent_platform_governed_workflow_state_machine as p18_0,
)
from tests.hermes_cli import test_agent_platform_project_intake_workflow as p18_1
from tests.hermes_cli import (
    test_agent_platform_work_packet_non_critical_ticket_pilot as p17_8,
)


P18_2_EXPORTS = (
    "TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION",
    "TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID",
    "TicketFactoryRuntimeState",
    "TicketFactoryRuntimeDecision",
    "TicketFactoryRuntimeFindingSeverity",
    "TicketFactoryRuntimeFindingCode",
    "TicketFactoryRuntimeBinding",
    "TicketFactoryWorkPacketContinuation",
    "TicketFactoryRuntimeRequest",
    "TicketFactoryRuntimeFinding",
    "TicketFactoryRuntimeSummary",
    "TicketFactoryRuntimeIntegrationResult",
    "TicketFactoryRuntimeIntegrationError",
    "TicketFactoryRuntimeInputError",
    "TicketFactoryRuntimeIntegrityError",
    "TicketFactoryRuntimePolicyError",
    "TicketFactoryRuntimeStateError",
    "TicketFactoryRuntimeValidationError",
    "build_canonical_p18_ticket_factory_runtime_request",
    "validate_ticket_factory_runtime_request",
    "build_ticket_factory_runtime_integration",
    "validate_ticket_factory_runtime_integration_result",
    "summarize_ticket_factory_runtime_integration",
)

PUBLIC_MODELS = (
    TicketFactoryRuntimeBinding,
    TicketFactoryWorkPacketContinuation,
    TicketFactoryRuntimeRequest,
    TicketFactoryRuntimeFinding,
    TicketFactoryRuntimeSummary,
    TicketFactoryRuntimeIntegrationResult,
)

PUBLIC_MODEL_FIELD_CASES = tuple(
    (model_type, field_name)
    for model_type in PUBLIC_MODELS
    for field_name in model_type.model_fields
)

FORBIDDEN_PUBLIC_EXPORTS = (
    "TicketFactoryExecutor",
    "TicketFactoryRuntimeServer",
    "execute_ticket_factory_runtime",
    "run_ticket_factory_agent",
    "call_ticket_factory_provider",
    "compile_work_packet_automatically",
    "approve_ticket_automatically",
    "GitTicketPublisher",
    "DockerTicketRuntime",
    "GraphifyTicketContextLoader",
    "PaperclipTicketStore",
    "GBrainTicketMemory",
)

P18_0_COMMIT = "7b928e60ed4adf49bfb3e47ab9acf1119aaef870"
P18_UI_A_COMMIT = "f55b8a2cc62c9ba0620a14f51b968107b75a78f1"


@pytest.fixture(scope="module")
def accepted_p17_closure(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_2")
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
def intake_result(initial_snapshot):
    approval = p18_1.valid_approval(
        "Human approves bounded P18.1 Pepper project intake context."
    )
    request = build_canonical_p18_project_intake_request(
        initial_workflow_snapshot=initial_snapshot,
        committed_p18_0_commit=P18_0_COMMIT,
        approval=approval,
    )
    return build_project_intake(request)


@pytest.fixture(scope="module")
def runtime_request(intake_result):
    return build_canonical_p18_ticket_factory_runtime_request(
        project_intake_result=intake_result,
        committed_p18_ui_a_commit=P18_UI_A_COMMIT,
    )


@pytest.fixture(scope="module")
def runtime_result(runtime_request):
    return build_ticket_factory_runtime_integration(runtime_request)


@pytest.fixture(scope="module")
def public_model_instances(runtime_request, runtime_result):
    return {
        TicketFactoryRuntimeBinding: runtime_result.binding,
        TicketFactoryWorkPacketContinuation: runtime_result.work_packet_continuation,
        TicketFactoryRuntimeRequest: runtime_request,
        TicketFactoryRuntimeFinding: runtime_result.findings[0],
        TicketFactoryRuntimeSummary: runtime_result.summary,
        TicketFactoryRuntimeIntegrationResult: runtime_result,
    }


def construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


@pytest.mark.parametrize("exported_name", P18_2_EXPORTS)
def test_all_p18_2_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(tfr, exported_name)


def test_p18_2_exports_are_additive_suffix() -> None:
    p18_0_count = len(p18_0.P18_0_EXPORTS)
    p18_1_count = len(p18_1.P18_1_EXPORTS)
    assert tuple(workflow.__all__[:p18_0_count]) == p18_0.P18_0_EXPORTS
    assert tuple(workflow.__all__[p18_0_count : p18_0_count + p18_1_count]) == (
        p18_1.P18_1_EXPORTS
    )
    assert tuple(workflow.__all__[p18_0_count + p18_1_count :]) == P18_2_EXPORTS
    assert tuple(tfr.__all__) == P18_2_EXPORTS
    assert len(P18_2_EXPORTS) == 23
    assert len(workflow.__all__) == 90
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_runtime_authority_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert forbidden not in tfr.__all__
    assert not hasattr(workflow, forbidden)
    assert not hasattr(tfr, forbidden)


@pytest.mark.parametrize(
    "enum_type",
    [
        TicketFactoryRuntimeState,
        TicketFactoryRuntimeDecision,
        TicketFactoryRuntimeFindingSeverity,
        TicketFactoryRuntimeFindingCode,
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


@pytest.mark.parametrize(("model_type", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_fields_are_individually_frozen(
    model_type: type[BaseModel], field_name: str, public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    with pytest.raises(ValidationError):
        setattr(instance, field_name, getattr(instance, field_name))


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


@pytest.mark.parametrize(("model_type", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_json_round_trip_preserves_each_field(
    model_type: type[BaseModel], field_name: str, public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    round_tripped = model_type.model_validate_json(instance.model_dump_json())
    assert getattr(round_tripped, field_name) == getattr(instance, field_name)


@pytest.mark.parametrize(("model_type", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_python_dump_round_trip_preserves_each_field(
    model_type: type[BaseModel], field_name: str, public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    round_tripped = model_type.model_validate(instance.model_dump(mode="python"))
    assert getattr(round_tripped, field_name) == getattr(instance, field_name)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_model_schema_additional_properties_false(
    model_type: type[BaseModel],
) -> None:
    assert model_type.model_json_schema()["additionalProperties"] is False


def test_request_consumes_accepted_p18_1_intake(runtime_request, intake_result) -> None:
    validate_ticket_factory_runtime_request(runtime_request)
    assert runtime_request.project_intake_result == intake_result
    assert intake_result.P18_2_ready is True
    assert (
        intake_result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.INTAKE_READY
    )
    assert runtime_request.P18_UI_A_parent_commit == P18_UI_A_COMMIT


def test_canonical_P18_ticket_factory_runtime_integration_flow(runtime_result) -> None:
    assert runtime_result.integration_id.startswith("TFI-P18-")
    assert runtime_result.state is TicketFactoryRuntimeState.COMPLETED
    assert runtime_result.decision is TicketFactoryRuntimeDecision.ACCEPTED
    assert runtime_result.ticket_spec.ticket_id == "P18.2"
    assert (
        runtime_result.workflow_transition_result.transition.transition_id == "GWT-002"
    )
    assert (
        runtime_result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    )
    assert runtime_result.summary.TicketSpec_runtime_integration_satisfied is True
    assert runtime_result.P18_3_ready is True
    assert runtime_result.provider_dispatch_count == 0
    assert runtime_result.model_inference_count == 0
    assert runtime_result.Git_commands_executed == 0
    assert runtime_result.WorkPacket_compilation_count == 1
    assert runtime_result.human_ticket_approval_present is False
    assert runtime_result.ticket_execution_authorized is False
    assert runtime_result.WorkPacket_execution_authorized is False


def test_canonical_ticket_factory_rejects_invalid_project_intake(intake_result) -> None:
    invalid_intake = construct_with_updates(intake_result, P18_2_ready=False)
    with pytest.raises((ValidationError, TicketFactoryRuntimeIntegrationError)):
        request = TicketFactoryRuntimeRequest(
            project_intake_result=invalid_intake,
            P18_UI_A_parent_commit=P18_UI_A_COMMIT,
        )
        validate_ticket_factory_runtime_request(request)


def test_canonical_ticket_factory_rejects_unapproved_execution_authority(
    runtime_result,
) -> None:
    tampered = construct_with_updates(
        runtime_result, WorkPacket_execution_authorized=True
    )
    with pytest.raises(TicketFactoryRuntimeIntegrationError):
        validate_ticket_factory_runtime_integration_result(tampered)


def test_request_rejects_wrong_p18_ui_a_parent(intake_result) -> None:
    request = TicketFactoryRuntimeRequest(
        project_intake_result=intake_result,
        P18_UI_A_parent_commit="0" * 40,
    )
    with pytest.raises(TicketFactoryRuntimeIntegrationError):
        validate_ticket_factory_runtime_request(request)


def test_ticket_factory_project_and_ticket_specs(runtime_result) -> None:
    project = runtime_result.project_spec
    ticket = runtime_result.ticket_spec
    assert project.project_id == "P18"
    assert project.title == "Manual-to-Hermes Workflow Migration"
    assert ticket.project_id == "P18"
    assert ticket.ticket_id == "P18.2"
    assert ticket.title == "Ticket Factory Runtime Integration"
    assert ticket.ticket_type is TicketType.INTEGRATION
    assert ticket.parallelization_hint.value == "unspecified"
    assert ticket.dependencies == ()
    assert (
        ticket.recommended_commit_message
        == "P18.2 Add Ticket Factory runtime integration"
    )
    assert any(reference.value == "P18.1" for reference in ticket.authority_references)
    assert any(
        reference.value == "P18.UI-A" for reference in ticket.authority_references
    )


def test_ticket_scope_preserves_authority_boundaries(runtime_result) -> None:
    scope = runtime_result.ticket_spec.scope
    assert (
        "2_products/pepper-agent/hermes_cli/agent_platform/workflow/**"
        in scope.allowed_paths
    )
    assert ".git/**" in scope.forbidden_paths
    forbidden = "\n".join(scope.forbidden_actions)
    for marker in (
        "git add",
        "git commit",
        "git push",
        "git reset",
        "git clean",
        "git stash",
        "git worktree",
        "Graphify",
        "Docker",
        "provider dispatch",
        "model inference",
    ):
        assert marker in forbidden


def test_context_pack_is_bounded_and_ordered(runtime_result) -> None:
    pack: ContextPack = runtime_result.context_pack
    assert pack.project_id == "P18"
    assert pack.ticket_id == "P18.2"
    assert pack.items[0].source_id == "CTX-PROJECT-SPEC"
    assert pack.items[1].source_id == "CTX-TICKET-SPEC"
    source_ids = {item.source_id for item in pack.items}
    assert {"CTX-P18-1-INTAKE", "CTX-P18-UI-A", "CTX-P18-2-HANDOFF"}.issubset(
        source_ids
    )
    assert all(item.sensitivity is not ContextSensitivity.SECRET for item in pack.items)
    assert not pack.omitted_source_ids


def test_dependency_plan_and_lint_are_ready(runtime_result) -> None:
    plan: TicketDependencyPlan = runtime_result.dependency_plan
    report: TicketLintReport = runtime_result.lint_report
    assert plan.project_id == "P18"
    assert plan.ticket_ids == ("P18.2",)
    assert plan.edges == ()
    assert plan.blocked_ticket_ids == ()
    assert plan.unresolved_soft_external_dependency_ids == ()
    assert len(plan.waves) == 1
    assert plan.waves[0].ticket_ids == ("P18.2",)
    assert plan.waves[0].disposition is WaveDisposition.DEPENDENCY_READY
    assert report.project_id == "P18"
    assert report.ticket_ids == ("P18.2",)
    assert report.disposition is TicketLintDisposition.PASS
    assert report.summary.error_count == 0
    assert runtime_result.work_packet_compilation_result.dependency_plan == plan
    assert runtime_result.work_packet_compilation_result.fresh_lint_report == report


def test_governed_p18_1_prerequisite_is_preserved_as_authority(
    runtime_request,
    runtime_result,
) -> None:
    p18_2_roadmap_item = next(
        item
        for item in runtime_request.project_intake_result.roadmap.items
        if item.ticket_id == "P18.2"
    )
    assert p18_2_roadmap_item.prerequisite_ticket_ids == ("P18.1",)
    assert any(
        reference.value == "P18.1"
        for reference in runtime_result.ticket_spec.authority_references
    )
    assert runtime_result.work_packet_compilation_result.work_packet.source_ticket == (
        runtime_result.ticket_spec
    )


def test_work_packet_continuation_records_compile_only_evidence(runtime_result) -> None:
    continuation = runtime_result.work_packet_continuation
    compilation = runtime_result.work_packet_compilation_result
    assert continuation.source_ticket_id == "P18.2"
    assert (
        continuation.dependency_plan_SHA256
        == runtime_result.dependency_plan.plan_SHA256
    )
    assert continuation.lint_report_SHA256 == runtime_result.lint_report.report_SHA256
    assert continuation.compilation_result_SHA256 == compilation.result_SHA256
    assert continuation.work_packet_id == compilation.work_packet.work_packet_id
    assert continuation.work_packet_SHA256 == compilation.work_packet.work_packet_SHA256
    assert continuation.approved_ticket_required is True
    assert (
        continuation.work_packet_compilation_allowed_before_human_ticket_approval
        is True
    )
    assert continuation.human_ticket_approval_required_before_execution is True
    assert continuation.human_ticket_approval_present is False
    assert continuation.logical_publication_required is True
    assert continuation.compilation_authorization_present is True
    assert continuation.work_packet_compilation_completed is True
    assert continuation.command_execution_authorized is False
    assert continuation.runtime_execution_authorized is False
    assert continuation.human_git_authority_required is True
    assert continuation.compiler_invocation_count == 1
    assert runtime_result.WorkPacket_compilation_count == 1


def test_work_packet_compilation_result_is_real_compile_only_output(
    runtime_result,
) -> None:
    compilation = runtime_result.work_packet_compilation_result
    packet = compilation.work_packet
    assert isinstance(compilation, WorkPacketCompilationResult)
    assert compilation.disposition.value == "compiled"
    assert compilation.dependency_plan == runtime_result.dependency_plan
    assert compilation.fresh_lint_report == runtime_result.lint_report
    assert packet.ticket_id == "P18.2"
    assert packet.source_ticket == runtime_result.ticket_spec
    assert packet.work_packet_id.startswith("WP-P18-2-")
    assert packet.work_packet_id not in (
        "not_executed_pending_human_ticket_approval",
        "not_compiled_pending_human_ticket_approval",
        "not_allocated_pending_human_ticket_approval",
    )
    assert len(packet.work_packet_SHA256) == 64
    assert packet.authority_boundary.value == "compile_only"
    assert packet.execution_ready is False
    assert packet.git_authority.value == "human_only"
    assert all(
        step.command_execution_authorized is False for step in packet.validation_steps
    )


def test_p17_work_packet_compiler_invoked_exactly_once(
    runtime_request,
    monkeypatch,
) -> None:
    calls = []
    original = tfr.compile_ticket_spec_to_work_packet

    def counting_compile(request):
        calls.append(request)
        return original(request)

    monkeypatch.setattr(tfr, "compile_ticket_spec_to_work_packet", counting_compile)
    result = build_ticket_factory_runtime_integration(runtime_request)
    assert len(calls) == 1
    assert result.WorkPacket_compilation_count == 1
    assert result.work_packet_compilation_result.work_packet.ticket_id == "P18.2"


def test_workflow_transition_stops_at_ticket_approval(runtime_result) -> None:
    transition = runtime_result.workflow_transition_result
    assert transition.accepted is True
    assert runtime_result.state is TicketFactoryRuntimeState.COMPLETED
    assert transition.transition.transition_id == "GWT-002"
    assert transition.transition.from_state is GovernedWorkflowState.INTAKE_READY
    assert (
        transition.transition.to_state is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    )
    assert transition.transition.trigger is WorkflowTransitionTrigger.TICKET_GENERATED
    assert (
        transition.transition.authority is WorkflowTransitionAuthority.GOVERNED_RUNTIME
    )
    assert (
        transition.resulting_snapshot.current_state
        is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    )
    assert transition.resulting_snapshot.pending_human_action == "ticket_approval"
    assert transition.human_action_required is True
    assert runtime_result.P18_3_ready is True


def test_summary_and_result_authority_boundary(runtime_result) -> None:
    summary = summarize_ticket_factory_runtime_integration(runtime_result)
    assert summary == runtime_result.summary
    assert summary.TicketSpec_runtime_integration_satisfied is True
    assert summary.P18_3_ready is True
    assert summary.human_ticket_approval_required is True
    assert runtime_result.production_readiness_claimed is False
    assert runtime_result.provider_dispatch_count == 0
    assert runtime_result.model_inference_count == 0
    assert runtime_result.Git_commands_executed == 0
    assert runtime_result.Docker_commands_executed == 0
    assert runtime_result.Graphify_commands_executed == 0
    assert runtime_result.WorkPacket_compilation_count == 1
    assert runtime_result.WorkPacket_execution_authorized is False
    assert runtime_result.work_packet_continuation.command_execution_authorized is False


def test_result_validation_rejects_binding_digest_tampering(runtime_result) -> None:
    tampered_binding = construct_with_updates(
        runtime_result.binding,
        binding_SHA256="0" * 64,
    )
    tampered = construct_with_updates(runtime_result, binding=tampered_binding)
    with pytest.raises(TicketFactoryRuntimeIntegrationError):
        validate_ticket_factory_runtime_integration_result(tampered)


def test_result_validation_rejects_ticket_tampering(runtime_result) -> None:
    tampered_ticket = TicketSpec.model_validate({
        **runtime_result.ticket_spec.model_dump(mode="json"),
        "ticket_id": "P18.3",
    })
    tampered = construct_with_updates(runtime_result, ticket_spec=tampered_ticket)
    with pytest.raises(TicketFactoryRuntimeIntegrationError):
        validate_ticket_factory_runtime_integration_result(tampered)


def test_result_validation_rejects_work_packet_digest_tampering(
    runtime_result,
) -> None:
    compilation = runtime_result.work_packet_compilation_result
    tampered_packet = construct_with_updates(
        compilation.work_packet,
        work_packet_SHA256="0" * 64,
    )
    tampered_compilation = construct_with_updates(
        compilation,
        work_packet=tampered_packet,
    )
    tampered = construct_with_updates(
        runtime_result,
        work_packet_compilation_result=tampered_compilation,
    )
    with pytest.raises(TicketFactoryRuntimeIntegrationError):
        validate_ticket_factory_runtime_integration_result(tampered)


def test_result_validation_rejects_compilation_result_digest_tampering(
    runtime_result,
) -> None:
    tampered_compilation = construct_with_updates(
        runtime_result.work_packet_compilation_result,
        result_SHA256="0" * 64,
    )
    tampered = construct_with_updates(
        runtime_result,
        work_packet_compilation_result=tampered_compilation,
    )
    with pytest.raises(TicketFactoryRuntimeIntegrationError):
        validate_ticket_factory_runtime_integration_result(tampered)


def test_runtime_integration_is_deterministic(runtime_request) -> None:
    first = build_ticket_factory_runtime_integration(runtime_request)
    second = build_ticket_factory_runtime_integration(runtime_request)
    assert first == second
    assert first.integration_id.startswith("TFI-P18-")
    assert len(first.result_SHA256) == 64
