from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.approval_workflow as aw
from hermes_cli.agent_platform.ticket_factory import HumanApprovalDecision
from hermes_cli.agent_platform.workflow import (
    ApprovalWorkflowArtifactBinding,
    ApprovalWorkflowDecisionAuthority,
    ApprovalWorkflowDecisionInput,
    ApprovalWorkflowFinding,
    ApprovalWorkflowFindingCode,
    ApprovalWorkflowFindingSeverity,
    ApprovalWorkflowInputError,
    ApprovalWorkflowIntegrityError,
    ApprovalWorkflowIntegrationError,
    ApprovalWorkflowIntegrationResult,
    ApprovalWorkflowP18_4Handoff,
    ApprovalWorkflowPolicyError,
    ApprovalWorkflowPublicationBoundary,
    ApprovalWorkflowRequest,
    ApprovalWorkflowResultDecision,
    ApprovalWorkflowState,
    ApprovalWorkflowStateError,
    ApprovalWorkflowSummary,
    ApprovalWorkflowValidationError,
    GovernedWorkflowState,
    HermesWorkflowRuntimeKind,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_approval_workflow_decision_input,
    build_approval_workflow_integration,
    build_canonical_p18_approval_workflow_request,
    build_canonical_p18_project_intake_request,
    build_canonical_p18_ticket_factory_runtime_request,
    build_governed_workflow_identity,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    build_p17_workflow_binding,
    build_project_intake,
    build_ticket_factory_runtime_integration,
    summarize_approval_workflow_integration,
    validate_approval_workflow_integration_result,
    validate_approval_workflow_request,
)
from hermes_cli.agent_platform.work_packet import (
    build_canonical_p17_closure_request,
    build_p17_work_packet_execution_mvp_closure,
)
from tests.hermes_cli import (
    test_agent_platform_governed_workflow_state_machine as p18_0,
)
from tests.hermes_cli import test_agent_platform_project_intake_workflow as p18_1
from tests.hermes_cli import (
    test_agent_platform_ticket_factory_runtime_integration as p18_2,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_non_critical_ticket_pilot as p17_8,
)


P18_3_EXPORTS = (
    "APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION",
    "APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID",
    "ApprovalWorkflowDecisionAuthority",
    "ApprovalWorkflowState",
    "ApprovalWorkflowResultDecision",
    "ApprovalWorkflowFindingSeverity",
    "ApprovalWorkflowFindingCode",
    "ApprovalWorkflowArtifactBinding",
    "ApprovalWorkflowDecisionInput",
    "ApprovalWorkflowRequest",
    "ApprovalWorkflowFinding",
    "ApprovalWorkflowPublicationBoundary",
    "ApprovalWorkflowP18_4Handoff",
    "ApprovalWorkflowSummary",
    "ApprovalWorkflowIntegrationResult",
    "ApprovalWorkflowIntegrationError",
    "ApprovalWorkflowInputError",
    "ApprovalWorkflowIntegrityError",
    "ApprovalWorkflowPolicyError",
    "ApprovalWorkflowStateError",
    "ApprovalWorkflowValidationError",
    "build_approval_workflow_decision_input",
    "build_canonical_p18_approval_workflow_request",
    "validate_approval_workflow_request",
    "build_approval_workflow_integration",
    "validate_approval_workflow_integration_result",
    "summarize_approval_workflow_integration",
)

PUBLIC_MODELS = (
    ApprovalWorkflowArtifactBinding,
    ApprovalWorkflowDecisionInput,
    ApprovalWorkflowRequest,
    ApprovalWorkflowFinding,
    ApprovalWorkflowPublicationBoundary,
    ApprovalWorkflowP18_4Handoff,
    ApprovalWorkflowSummary,
    ApprovalWorkflowIntegrationResult,
)

PUBLIC_MODEL_FIELD_CASES = tuple(
    (model_type, field_name)
    for model_type in PUBLIC_MODELS
    for field_name in model_type.model_fields
)

FORBIDDEN_PUBLIC_EXPORTS = (
    "execute_approved_ticket",
    "execute_work_packet",
    "dispatch_approved_ticket",
    "run_approved_ticket",
    "auto_approve_ticket",
    "approve_with_model",
    "approve_with_provider",
    "ApprovalWorkflowExecutor",
    "ApprovalWorkflowEngine",
    "ApprovalWorkflowHTTPServer",
)

P18_0_COMMIT = "7b928e60ed4adf49bfb3e47ab9acf1119aaef870"
P18_UI_A_COMMIT = "f55b8a2cc62c9ba0620a14f51b968107b75a78f1"


@pytest.fixture(scope="module")
def accepted_p17_closure(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_3")
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
def runtime_result(intake_result):
    request = build_canonical_p18_ticket_factory_runtime_request(
        project_intake_result=intake_result,
        committed_p18_ui_a_commit=P18_UI_A_COMMIT,
    )
    return build_ticket_factory_runtime_integration(request)


@pytest.fixture(scope="module")
def approve_decision():
    return build_approval_workflow_decision_input(
        decision=HumanApprovalDecision.APPROVE,
        reviewer_id="human.p18.3",
        decision_reference="P18.3 explicit human approval.",
        rationale=(
            "Approve the generated TicketSpec while preserving no execution authority."
        ),
        reason_code="approve_ticket",
        decided_at="2026-08-09T00:00:00Z",
    )


@pytest.fixture(scope="module")
def reject_decision():
    return build_approval_workflow_decision_input(
        decision=HumanApprovalDecision.REJECT,
        reviewer_id="human.p18.3",
        decision_reference="P18.3 explicit human rejection.",
        rationale=(
            "Reject the generated TicketSpec and return it to correction without execution."
        ),
        reason_code="reject_ticket",
        decided_at="2026-08-09T00:00:00Z",
    )


@pytest.fixture(scope="module")
def approve_request(runtime_result, approve_decision):
    return build_canonical_p18_approval_workflow_request(
        ticket_factory_runtime_result=runtime_result,
        decision_input=approve_decision,
    )


@pytest.fixture(scope="module")
def reject_request(runtime_result, reject_decision):
    return build_canonical_p18_approval_workflow_request(
        ticket_factory_runtime_result=runtime_result,
        decision_input=reject_decision,
    )


@pytest.fixture(scope="module")
def approve_result(approve_request):
    return build_approval_workflow_integration(approve_request)


@pytest.fixture(scope="module")
def reject_result(reject_request):
    return build_approval_workflow_integration(reject_request)


@pytest.fixture(scope="module")
def public_model_instances(approve_request, approve_result):
    return {
        ApprovalWorkflowArtifactBinding: approve_result.artifact_binding,
        ApprovalWorkflowDecisionInput: approve_result.decision_input,
        ApprovalWorkflowRequest: approve_request,
        ApprovalWorkflowFinding: approve_result.findings[0],
        ApprovalWorkflowPublicationBoundary: approve_result.publication_boundary,
        ApprovalWorkflowP18_4Handoff: approve_result.handoff,
        ApprovalWorkflowSummary: approve_result.summary,
        ApprovalWorkflowIntegrationResult: approve_result,
    }


def construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def assert_approval_validation_fails(callback) -> None:
    with pytest.raises((ValidationError, ValueError, ApprovalWorkflowIntegrationError)):
        callback()


@pytest.mark.parametrize("exported_name", P18_3_EXPORTS)
def test_all_p18_3_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(aw, exported_name)


def test_p18_3_exports_are_additive_suffix() -> None:
    p18_0_count = len(p18_0.P18_0_EXPORTS)
    p18_1_count = len(p18_1.P18_1_EXPORTS)
    p18_2_count = len(p18_2.P18_2_EXPORTS)
    assert tuple(workflow.__all__[:p18_0_count]) == p18_0.P18_0_EXPORTS
    assert tuple(workflow.__all__[p18_0_count : p18_0_count + p18_1_count]) == (
        p18_1.P18_1_EXPORTS
    )
    assert (
        tuple(
            workflow.__all__[
                p18_0_count + p18_1_count : p18_0_count + p18_1_count + p18_2_count
            ]
        )
        == p18_2.P18_2_EXPORTS
    )
    p18_3_start = p18_0_count + p18_1_count + p18_2_count
    p18_3_end = p18_3_start + len(P18_3_EXPORTS)
    assert tuple(workflow.__all__[p18_3_start:p18_3_end]) == P18_3_EXPORTS
    assert tuple(aw.__all__) == P18_3_EXPORTS
    assert len(p18_0.P18_0_EXPORTS) == 38
    assert len(p18_1.P18_1_EXPORTS) == 29
    assert len(p18_2.P18_2_EXPORTS) == 23
    assert len(P18_3_EXPORTS) == 27
    assert len(workflow.__all__) >= p18_3_end
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_execution_authority_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert forbidden not in aw.__all__
    assert not hasattr(workflow, forbidden)
    assert not hasattr(aw, forbidden)


@pytest.mark.parametrize(
    "enum_type",
    [
        ApprovalWorkflowDecisionAuthority,
        ApprovalWorkflowState,
        ApprovalWorkflowResultDecision,
        ApprovalWorkflowFindingSeverity,
        ApprovalWorkflowFindingCode,
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


@pytest.mark.parametrize(("model_type", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_python_dump_round_trip_preserves_each_field(
    model_type: type[BaseModel], field_name: str, public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    round_tripped = model_type.model_validate(instance.model_dump(mode="python"))
    assert getattr(round_tripped, field_name) == getattr(instance, field_name)


@pytest.mark.parametrize(("model_type", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_json_dump_round_trip_preserves_each_field(
    model_type: type[BaseModel], field_name: str, public_model_instances
) -> None:
    instance = public_model_instances[model_type]
    round_tripped = model_type.model_validate_json(instance.model_dump_json())
    assert getattr(round_tripped, field_name) == getattr(instance, field_name)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_model_schema_additional_properties_false(
    model_type: type[BaseModel],
) -> None:
    assert model_type.model_json_schema()["additionalProperties"] is False


def test_canonical_P18_human_ticket_approval_flow(approve_result) -> None:
    assert approve_result.integration_id.startswith("AWI-P18-")
    assert approve_result.state is ApprovalWorkflowState.COMPLETED
    assert approve_result.decision is ApprovalWorkflowResultDecision.APPROVED
    assert approve_result.approval_valid is True
    assert approve_result.authority is ApprovalWorkflowDecisionAuthority.HUMAN
    assert approve_result.approval_granted is True
    assert approve_result.human_ticket_approval_present is True
    assert (
        approve_result.workflow_transition_result.transition.transition_id == "GWT-003"
    )
    assert (
        approve_result.resulting_workflow_state is GovernedWorkflowState.TICKET_APPROVED
    )
    assert approve_result.ticket_execution_authorized is False
    assert approve_result.WorkPacket_execution_authorized is False
    assert approve_result.ticket_execution_started is False
    assert approve_result.WorkPacket_execution_started is False
    assert approve_result.worker_dispatch_count == 0
    assert approve_result.command_execution_count == 0
    assert approve_result.provider_dispatch_count == 0
    assert approve_result.model_inference_count == 0
    assert approve_result.Git_commands_executed == 0
    assert approve_result.P18_4_ready is True


def test_canonical_P18_human_ticket_rejection_flow(reject_result) -> None:
    assert reject_result.state is ApprovalWorkflowState.COMPLETED
    assert reject_result.decision is ApprovalWorkflowResultDecision.REJECTED
    assert reject_result.approval_valid is True
    assert reject_result.authority is ApprovalWorkflowDecisionAuthority.HUMAN
    assert reject_result.approval_granted is False
    assert reject_result.human_ticket_approval_present is True
    assert (
        reject_result.workflow_transition_result.transition.transition_id == "GWT-025"
    )
    assert (
        reject_result.resulting_workflow_state
        is GovernedWorkflowState.AWAITING_CORRECTION
    )
    assert reject_result.ticket_publication_result is None
    assert reject_result.ticket_execution_authorized is False
    assert reject_result.WorkPacket_execution_authorized is False
    assert reject_result.worker_dispatch_count == 0
    assert reject_result.P18_4_ready is False


def test_canonical_P18_approval_rejects_tampered_work_packet(approve_request) -> None:
    tampered_binding = construct_with_updates(
        approve_request.artifact_binding,
        WorkPacket_SHA256="0" * 64,
    )
    tampered = construct_with_updates(
        approve_request, artifact_binding=tampered_binding
    )
    assert_approval_validation_fails(
        lambda: build_approval_workflow_integration(tampered)
    )


def test_canonical_P18_approval_rejects_non_human_authority(approve_request) -> None:
    non_human = construct_with_updates(
        approve_request.decision_input,
        authority=ApprovalWorkflowDecisionAuthority.MODEL,
    )
    tampered = construct_with_updates(approve_request, decision_input=non_human)
    assert_approval_validation_fails(
        lambda: build_approval_workflow_integration(tampered)
    )


def test_p18_2_continuation_binding_identity(runtime_result, approve_request) -> None:
    packet = runtime_result.work_packet_compilation_result.work_packet
    binding = approve_request.artifact_binding
    assert binding.project_id == "PEPPER"
    assert binding.macroproject_id == "P18"
    assert binding.ticket_id == "P18.2"
    assert runtime_result.binding.ticket_factory_project_id == "PEPPER"
    assert runtime_result.binding.ticket_factory_macroproject_id == "P18"
    assert binding.P18_2_result_SHA256 == runtime_result.result_SHA256
    assert binding.TicketSpec_SHA256 == packet.source_ticket_SHA256
    assert binding.WorkPacket_ID == packet.work_packet_id
    assert binding.WorkPacket_SHA256 == packet.work_packet_SHA256
    assert (
        binding.current_workflow_state is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    )
    assert runtime_result.WorkPacket_compilation_count == 1
    assert runtime_result.human_ticket_approval_present is False
    assert runtime_result.ticket_execution_authorized is False
    assert runtime_result.WorkPacket_execution_authorized is False


def test_approval_publication_boundary_reuses_existing_contract(
    runtime_result, approve_result
) -> None:
    publication = approve_result.ticket_publication_result
    assert publication is not None
    assert publication.publication.canonical_ticket == runtime_result.ticket_spec
    assert publication.publication.revision == 1
    assert publication.publication.publication_id == "PUB-P18-2-0001"
    assert approve_result.publication_boundary.publication_required_for_approve is True
    assert approve_result.publication_boundary.publication_applied is True
    assert (
        approve_result.publication_boundary.approved_ticket_matches_work_packet_source
        is True
    )
    assert (
        approve_result.publication_boundary.published_ticket_matches_approved_ticket
        is True
    )
    assert (
        approve_result.publication_boundary.compile_only_publication_artifact_SHA256
        == runtime_result.work_packet_compilation_result.work_packet.publication_artifact_SHA256
    )
    assert (
        approve_result.publication_boundary.WorkPacket_recompile_required_before_execution
        is False
    )


def test_rejection_does_not_publish_or_revise_ticket(reject_result) -> None:
    assert reject_result.ticket_approval_record.approved_ticket is None
    assert reject_result.ticket_publication_result is None
    assert reject_result.publication_boundary.publication_applied is False
    assert reject_result.publication_boundary.human_approved_publication_id is None
    assert (
        reject_result.publication_boundary.published_ticket_matches_approved_ticket
        is False
    )


def test_p18_0_approval_transition_is_reused(approve_result) -> None:
    transition = approve_result.workflow_transition_result.transition
    assert transition.transition_id == "GWT-003"
    assert transition.from_state is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    assert transition.to_state is GovernedWorkflowState.TICKET_APPROVED
    assert transition.trigger is WorkflowTransitionTrigger.TICKET_APPROVED
    assert transition.authority is WorkflowTransitionAuthority.HUMAN
    assert transition.required_evidence == ("human_ticket_approval",)
    assert transition.automatic is False


def test_p18_0_rejection_transition_is_reused(reject_result) -> None:
    transition = reject_result.workflow_transition_result.transition
    assert transition.transition_id == "GWT-025"
    assert transition.from_state is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    assert transition.to_state is GovernedWorkflowState.AWAITING_CORRECTION
    assert transition.trigger is WorkflowTransitionTrigger.HUMAN_REJECTED
    assert transition.authority is WorkflowTransitionAuthority.HUMAN
    assert transition.required_evidence == ("human_ticket_rejection",)
    assert transition.automatic is False


def test_summary_and_result_authority_boundary(approve_result) -> None:
    summary = summarize_approval_workflow_integration(approve_result)
    assert summary == approve_result.summary
    assert summary.P18_2_continuation_valid is True
    assert summary.approval_request_valid is True
    assert summary.approval_decision_valid is True
    assert summary.human_authority_valid is True
    assert summary.artifact_binding_valid is True
    assert summary.TicketSpec_binding_valid is True
    assert summary.WorkPacket_binding_valid is True
    assert summary.publication_boundary_valid is True
    assert summary.approval_transition_valid is True
    assert summary.replay_policy_valid is True
    assert summary.execution_prohibition_valid is True
    assert summary.P18_4_handoff_valid is True
    assert summary.warning_finding_count == 0
    assert summary.blocking_finding_count == 0


def test_rejection_summary_tracks_rejection_transition(reject_result) -> None:
    summary = reject_result.summary
    assert summary.rejection_transition_valid is True
    assert summary.approval_transition_valid is False
    assert summary.publication_boundary_valid is True
    assert summary.P18_4_handoff_valid is True
    assert summary.warning_finding_count == 0
    assert summary.blocking_finding_count == 0


def test_p18_4_handoff_approve_contains_immutable_queue_evidence(
    approve_result,
) -> None:
    handoff = approve_result.handoff
    assert handoff.project_id == "PEPPER"
    assert handoff.macroproject_id == "P18"
    assert handoff.ticket_id == "P18.2"
    assert handoff.approval_decision is HumanApprovalDecision.APPROVE
    assert handoff.approval_granted is True
    assert handoff.approval_result_SHA256 == approve_result.approval_result_SHA256
    assert handoff.workflow_state is GovernedWorkflowState.TICKET_APPROVED
    assert handoff.execution_started is False
    assert handoff.approved_handoff_P18_4_ready is True
    assert handoff.rejected_handoff_P18_4_ready is False
    assert handoff.P18_4_ready is True


def test_p18_4_handoff_reject_is_not_queue_eligible(reject_result) -> None:
    handoff = reject_result.handoff
    assert handoff.approval_decision is HumanApprovalDecision.REJECT
    assert handoff.approval_granted is False
    assert handoff.workflow_state is GovernedWorkflowState.AWAITING_CORRECTION
    assert handoff.execution_started is False
    assert handoff.approved_handoff_P18_4_ready is False
    assert handoff.rejected_handoff_P18_4_ready is False
    assert handoff.P18_4_ready is False


@pytest.mark.parametrize(
    "authority",
    [
        ApprovalWorkflowDecisionAuthority.PROVIDER,
        ApprovalWorkflowDecisionAuthority.MODEL,
        ApprovalWorkflowDecisionAuthority.AUTONOMOUS_AGENT,
        ApprovalWorkflowDecisionAuthority.WORKER,
        ApprovalWorkflowDecisionAuthority.SCHEDULER,
        ApprovalWorkflowDecisionAuthority.RUNTIME,
        ApprovalWorkflowDecisionAuthority.GENERATED_DEFAULT,
    ],
)
def test_non_human_approval_authorities_are_rejected(
    approve_request, authority
) -> None:
    non_human = construct_with_updates(
        approve_request.decision_input, authority=authority
    )
    tampered = construct_with_updates(approve_request, decision_input=non_human)
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_request(tampered)
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("project_id", "P18"),
        ("project_id", "P19"),
        ("macroproject_id", "PEPPER"),
        ("macroproject_id", "P19"),
        ("ticket_id", "P18.3"),
        ("P18_2_result_SHA256", "0" * 64),
        ("TicketSpec_SHA256", "1" * 64),
        ("WorkPacket_ID", "WP-P18-2-R0001-000000000000"),
        ("WorkPacket_SHA256", "2" * 64),
        ("workflow_snapshot_SHA256", "3" * 64),
        ("current_workflow_state", GovernedWorkflowState.INTAKE_READY),
        ("expected_current_state", GovernedWorkflowState.TICKET_APPROVED),
        ("ticket_factory_runtime_policy_id", "wrong-policy"),
        ("governed_workflow_policy_id", "wrong-policy"),
        ("work_packet_compiler_policy_id", "wrong-policy"),
    ],
)
def test_artifact_binding_tampering_is_rejected(
    approve_request, field_name, value
) -> None:
    tampered_binding = construct_with_updates(
        approve_request.artifact_binding,
        **{field_name: value},
    )
    tampered = construct_with_updates(
        approve_request, artifact_binding=tampered_binding
    )
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_request(tampered)
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("schema_version", 2),
        ("policy_id", "wrong-policy"),
        ("approval_request_SHA256", "0" * 64),
    ],
)
def test_request_policy_and_digest_tampering_is_rejected(
    approve_request, field_name, value
) -> None:
    tampered = construct_with_updates(approve_request, **{field_name: value})
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_request(tampered)
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("schema_version", 2),
        ("reason_code", "approve ticket"),
        ("decided_at", "not-a-time"),
        ("approval_decision_SHA256", "0" * 64),
    ],
)
def test_decision_input_policy_and_digest_tampering_is_rejected(
    approve_request, field_name, value
) -> None:
    tampered_decision = construct_with_updates(
        approve_request.decision_input,
        **{field_name: value},
    )
    tampered = construct_with_updates(approve_request, decision_input=tampered_decision)
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_request(tampered)
    )


def test_request_revision_decision_is_not_owned_by_p18_3(runtime_result) -> None:
    decision = build_approval_workflow_decision_input(
        decision=HumanApprovalDecision.REQUEST_REVISION,
        reviewer_id="human.p18.3",
        decision_reference="P18.3 explicit human revision request.",
        rationale="Request revision without starting an autonomous repair loop.",
        reason_code="request_revision",
        decided_at="2026-08-09T00:00:00Z",
    )
    assert_approval_validation_fails(
        lambda: build_canonical_p18_approval_workflow_request(
            ticket_factory_runtime_result=runtime_result,
            decision_input=decision,
        )
    )


def test_execution_attempt_embedded_in_approval_input_is_rejected() -> None:
    assert_approval_validation_fails(
        lambda: build_approval_workflow_decision_input(
            decision=HumanApprovalDecision.APPROVE,
            reviewer_id="human.p18.3",
            decision_reference="P18.3 explicit human approval.",
            rationale="git commit -m approve and execute_work_packet immediately",
            reason_code="approve_ticket",
            decided_at="2026-08-09T00:00:00Z",
        )
    )


def test_approval_without_compiled_work_packet_is_rejected(
    runtime_result, approve_decision
) -> None:
    tampered_runtime = construct_with_updates(
        runtime_result, WorkPacket_compilation_count=0
    )
    assert_approval_validation_fails(
        lambda: build_canonical_p18_approval_workflow_request(
            ticket_factory_runtime_result=tampered_runtime,
            decision_input=approve_decision,
        )
    )


def test_approval_where_p18_3_ready_is_false_is_rejected(
    runtime_result, approve_decision
) -> None:
    tampered_runtime = construct_with_updates(runtime_result, P18_3_ready=False)
    assert_approval_validation_fails(
        lambda: build_canonical_p18_approval_workflow_request(
            ticket_factory_runtime_result=tampered_runtime,
            decision_input=approve_decision,
        )
    )


def test_approval_where_p18_2_already_has_human_approval_is_rejected(
    runtime_result, approve_decision
) -> None:
    tampered_runtime = construct_with_updates(
        runtime_result, human_ticket_approval_present=True
    )
    assert_approval_validation_fails(
        lambda: build_canonical_p18_approval_workflow_request(
            ticket_factory_runtime_result=tampered_runtime,
            decision_input=approve_decision,
        )
    )


def test_approval_where_p18_2_authorizes_execution_is_rejected(
    runtime_result, approve_decision
) -> None:
    tampered_runtime = construct_with_updates(
        runtime_result, ticket_execution_authorized=True
    )
    assert_approval_validation_fails(
        lambda: build_canonical_p18_approval_workflow_request(
            ticket_factory_runtime_result=tampered_runtime,
            decision_input=approve_decision,
        )
    )


def test_exact_duplicate_replay_is_rejected(approve_request, approve_result) -> None:
    replay = construct_with_updates(
        approve_request,
        prior_approval_result_SHA256=approve_result.result_SHA256,
        prior_artifact_binding_SHA256=approve_result.artifact_binding.artifact_binding_SHA256,
        prior_approval_decision=HumanApprovalDecision.APPROVE,
    )
    assert_approval_validation_fails(lambda: validate_approval_workflow_request(replay))


def test_conflicting_second_decision_is_rejected(
    approve_request, approve_result
) -> None:
    conflicting_decision = build_approval_workflow_decision_input(
        decision=HumanApprovalDecision.REJECT,
        reviewer_id="human.p18.3",
        decision_reference="P18.3 conflicting human rejection.",
        rationale="Reject after approval should not overwrite the existing decision.",
        reason_code="reject_ticket",
        decided_at="2026-08-09T00:00:00Z",
    )
    replay = construct_with_updates(
        approve_request,
        decision_input=conflicting_decision,
        prior_approval_result_SHA256=approve_result.result_SHA256,
        prior_artifact_binding_SHA256=approve_result.artifact_binding.artifact_binding_SHA256,
        prior_approval_decision=HumanApprovalDecision.APPROVE,
    )
    assert_approval_validation_fails(lambda: validate_approval_workflow_request(replay))


def test_stale_artifact_approval_is_rejected(approve_request, approve_result) -> None:
    stale_binding = construct_with_updates(
        approve_request.artifact_binding,
        TicketSpec_SHA256="4" * 64,
    )
    stale = construct_with_updates(
        approve_request,
        artifact_binding=stale_binding,
        prior_approval_result_SHA256=approve_result.result_SHA256,
        prior_artifact_binding_SHA256=approve_result.artifact_binding.artifact_binding_SHA256,
        prior_approval_decision=HumanApprovalDecision.APPROVE,
    )
    assert_approval_validation_fails(lambda: validate_approval_workflow_request(stale))


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("approval_valid", False),
        ("authority", ApprovalWorkflowDecisionAuthority.RUNTIME),
        ("approval_granted", False),
        ("human_ticket_approval_present", False),
        ("ticket_execution_authorized", True),
        ("WorkPacket_execution_authorized", True),
        ("ticket_execution_started", True),
        ("WorkPacket_execution_started", True),
        ("worker_dispatch_count", 1),
        ("command_execution_count", 1),
        ("provider_dispatch_count", 1),
        ("model_inference_count", 1),
        ("Git_commands_executed", 1),
        ("Docker_commands_executed", 1),
        ("Graphify_commands_executed", 1),
        ("GBrain_calls", 1),
        ("Paperclip_calls", 1),
        ("production_readiness_claimed", True),
        ("result_SHA256", "0" * 64),
    ],
)
def test_result_tampering_is_rejected(approve_result, field_name, value) -> None:
    tampered = construct_with_updates(approve_result, **{field_name: value})
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_integration_result(tampered)
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("publication_applied", False),
        ("human_approved_publication_id", None),
        ("human_approved_publication_revision", None),
        ("human_approved_publication_result_SHA256", None),
        ("human_approved_publication_artifact_SHA256", None),
        ("approved_ticket_matches_work_packet_source", False),
        ("published_ticket_matches_approved_ticket", False),
        ("publication_boundary_SHA256", "0" * 64),
    ],
)
def test_publication_boundary_tampering_is_rejected(
    approve_result, field_name, value
) -> None:
    boundary = construct_with_updates(
        approve_result.publication_boundary,
        **{field_name: value},
    )
    tampered = construct_with_updates(approve_result, publication_boundary=boundary)
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_integration_result(tampered)
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("approval_granted", False),
        ("approval_decision_SHA256", "0" * 64),
        ("approval_result_SHA256", "1" * 64),
        ("workflow_state", GovernedWorkflowState.AWAITING_CORRECTION),
        ("execution_started", True),
        ("approved_handoff_P18_4_ready", False),
        ("rejected_handoff_P18_4_ready", True),
        ("P18_4_ready", False),
        ("handoff_SHA256", "2" * 64),
    ],
)
def test_handoff_tampering_is_rejected(approve_result, field_name, value) -> None:
    handoff = construct_with_updates(approve_result.handoff, **{field_name: value})
    tampered = construct_with_updates(approve_result, handoff=handoff)
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_integration_result(tampered)
    )


def test_approve_request_is_deterministic(runtime_result, approve_decision) -> None:
    first = build_canonical_p18_approval_workflow_request(
        ticket_factory_runtime_result=runtime_result,
        decision_input=approve_decision,
    )
    second = build_canonical_p18_approval_workflow_request(
        ticket_factory_runtime_result=runtime_result,
        decision_input=approve_decision,
    )
    assert first == second
    assert first.approval_request_SHA256 == second.approval_request_SHA256


def test_approve_result_is_deterministic(approve_request) -> None:
    first = build_approval_workflow_integration(approve_request)
    second = build_approval_workflow_integration(approve_request)
    assert first == second
    assert first.result_SHA256 == second.result_SHA256


def test_approve_and_reject_results_have_unique_digests(
    approve_result, reject_result
) -> None:
    assert approve_result.approval_result_SHA256 != reject_result.approval_result_SHA256
    assert approve_result.result_SHA256 != reject_result.result_SHA256
    assert approve_result.integration_id != reject_result.integration_id


def test_result_validation_rejects_summary_tampering(approve_result) -> None:
    summary = construct_with_updates(approve_result.summary, warning_finding_count=1)
    tampered = construct_with_updates(approve_result, summary=summary)
    assert_approval_validation_fails(
        lambda: validate_approval_workflow_integration_result(tampered)
    )


def test_duplicate_approval_models_are_not_created() -> None:
    assert not hasattr(aw, "TicketSpec")
    assert not hasattr(aw, "WorkPacket")
    assert not hasattr(aw, "ApprovalWorkflowEngine")
    assert not hasattr(aw, "TicketApprovalEngine")
    assert hasattr(aw, "TicketApprovalRecord")
    assert hasattr(aw, "TicketPublicationResult")


def test_paperclip_gbrain_and_runtime_execution_counts_are_zero(
    approve_result, reject_result
) -> None:
    for result in (approve_result, reject_result):
        assert result.worker_dispatch_count == 0
        assert result.command_execution_count == 0
        assert result.provider_dispatch_count == 0
        assert result.model_inference_count == 0
        assert result.Git_commands_executed == 0
        assert result.Docker_commands_executed == 0
        assert result.Graphify_commands_executed == 0
        assert result.GBrain_calls == 0
        assert result.Paperclip_calls == 0
        assert result.ticket_execution_authorized is False
        assert result.WorkPacket_execution_authorized is False
