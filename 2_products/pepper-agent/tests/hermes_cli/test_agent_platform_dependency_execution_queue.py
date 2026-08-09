from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.dependency_execution_queue as deq
from hermes_cli.agent_platform.ticket_factory import HumanApprovalDecision
from hermes_cli.agent_platform.workflow import (
    DEPENDENCY_AWARE_QUEUE_POLICY_ID,
    DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION,
    ApprovalWorkflowResultDecision,
    DependencyAwareQueueCandidate,
    DependencyAwareQueueDecision,
    DependencyAwareQueueFinding,
    DependencyAwareQueueFindingCode,
    DependencyAwareQueueFindingSeverity,
    DependencyAwareQueueInputError,
    DependencyAwareQueueIntegrationError,
    DependencyAwareQueueIntegrationResult,
    DependencyAwareQueueIntegrityError,
    DependencyAwareQueueP18_5Handoff,
    DependencyAwareQueuePolicyError,
    DependencyAwareQueueRequest,
    DependencyAwareQueueState,
    DependencyAwareQueueStateError,
    DependencyAwareQueueSummary,
    DependencyAwareQueueValidationError,
    DependencyQueueBlocker,
    DependencySatisfactionEvidence,
    DependencySatisfactionState,
    GovernedWorkflowState,
    HermesWorkflowRuntimeKind,
    QueueAdmissionBoundary,
    QueueCapabilityDecision,
    QueueRuntimeCapabilityAssessment,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_approval_workflow_decision_input,
    build_approval_workflow_integration,
    build_canonical_p18_approval_workflow_request,
    build_canonical_p18_dependency_queue_request,
    build_canonical_p18_project_intake_request,
    build_canonical_p18_ticket_factory_runtime_request,
    build_dependency_aware_queue_integration,
    build_dependency_satisfaction_evidence,
    build_governed_workflow_identity,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    build_p17_workflow_binding,
    build_project_intake,
    build_ticket_factory_runtime_integration,
    summarize_dependency_aware_queue_integration,
    validate_dependency_aware_queue_integration_result,
    validate_dependency_aware_queue_request,
)
from hermes_cli.agent_platform.work_packet import (
    build_canonical_p17_closure_request,
    build_p17_work_packet_execution_mvp_closure,
)
from tests.hermes_cli import (
    test_agent_platform_approval_workflow_integration as p18_3,
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


P18_4_EXPORTS = (
    "DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION",
    "DEPENDENCY_AWARE_QUEUE_POLICY_ID",
    "QueueCapabilityDecision",
    "DependencySatisfactionState",
    "DependencyAwareQueueDecision",
    "DependencyAwareQueueState",
    "DependencyAwareQueueFindingSeverity",
    "DependencyAwareQueueFindingCode",
    "QueueRuntimeCapabilityAssessment",
    "DependencySatisfactionEvidence",
    "DependencyAwareQueueRequest",
    "DependencyAwareQueueCandidate",
    "DependencyQueueBlocker",
    "QueueAdmissionBoundary",
    "DependencyAwareQueueFinding",
    "DependencyAwareQueueSummary",
    "DependencyAwareQueueP18_5Handoff",
    "DependencyAwareQueueIntegrationResult",
    "DependencyAwareQueueIntegrationError",
    "DependencyAwareQueueInputError",
    "DependencyAwareQueueIntegrityError",
    "DependencyAwareQueuePolicyError",
    "DependencyAwareQueueStateError",
    "DependencyAwareQueueValidationError",
    "build_dependency_satisfaction_evidence",
    "build_canonical_p18_dependency_queue_request",
    "validate_dependency_aware_queue_request",
    "build_dependency_aware_queue_integration",
    "validate_dependency_aware_queue_integration_result",
    "summarize_dependency_aware_queue_integration",
)

PUBLIC_MODELS = (
    QueueRuntimeCapabilityAssessment,
    DependencySatisfactionEvidence,
    DependencyAwareQueueRequest,
    DependencyAwareQueueCandidate,
    DependencyQueueBlocker,
    QueueAdmissionBoundary,
    DependencyAwareQueueFinding,
    DependencyAwareQueueSummary,
    DependencyAwareQueueP18_5Handoff,
    DependencyAwareQueueIntegrationResult,
)

PUBLIC_MODEL_FIELD_CASES = tuple(
    (model_type, field_name)
    for model_type in PUBLIC_MODELS
    for field_name in model_type.model_fields
)

FORBIDDEN_PUBLIC_EXPORTS = (
    "DependencyQueueExecutor",
    "DependencyQueueDispatcher",
    "DependencyScheduler",
    "DependencyWorker",
    "KanbanQueueStore",
    "dispatch_once",
    "run_dependency_queue",
    "execute_work_packet",
    "execute_approved_ticket",
    "claim_worker",
    "heartbeat_claim",
    "release_stale_claims",
    "allocate_workspace",
    "call_provider",
    "call_model",
    "build_ticket_dependency_plan",
)

ZERO_COUNT_FIELDS = (
    "worker_dispatch_count",
    "command_execution_count",
    "provider_dispatch_count",
    "model_inference_count",
    "Git_commands_executed",
    "Docker_commands_executed",
    "Graphify_commands_executed",
    "claim_count",
    "heartbeat_count",
    "reclaim_count",
    "workspace_allocation_count",
    "validation_command_execution_count",
    "retry_execution_count",
    "automatic_requeue_count",
    "rollback_count",
    "staging_calls",
    "commit_calls",
    "push_calls",
    "GBrain_calls",
    "Paperclip_calls",
    "dispatcher_calls_in_P18_4",
)

P18_0_COMMIT = "7b928e60ed4adf49bfb3e47ab9acf1119aaef870"
P18_UI_A_COMMIT = "f55b8a2cc62c9ba0620a14f51b968107b75a78f1"


@pytest.fixture(scope="module")
def accepted_p17_closure(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_4")
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
        reviewer_id="human.p18.4",
        decision_reference="P18.3 explicit human approval for P18.4.",
        rationale="Approve the generated TicketSpec before governed queue admission.",
        reason_code="approve_ticket",
        decided_at="2026-08-09T00:00:00Z",
    )


@pytest.fixture(scope="module")
def reject_decision():
    return build_approval_workflow_decision_input(
        decision=HumanApprovalDecision.REJECT,
        reviewer_id="human.p18.4",
        decision_reference="P18.3 explicit human rejection for P18.4.",
        rationale="Reject the generated TicketSpec before any queue admission.",
        reason_code="reject_ticket",
        decided_at="2026-08-09T00:00:00Z",
    )


@pytest.fixture(scope="module")
def approve_result(runtime_result, approve_decision):
    request = build_canonical_p18_approval_workflow_request(
        ticket_factory_runtime_result=runtime_result,
        decision_input=approve_decision,
    )
    return build_approval_workflow_integration(request)


@pytest.fixture(scope="module")
def reject_result(runtime_result, reject_decision):
    request = build_canonical_p18_approval_workflow_request(
        ticket_factory_runtime_result=runtime_result,
        decision_input=reject_decision,
    )
    return build_approval_workflow_integration(request)


@pytest.fixture(scope="module")
def satisfied_dependency_evidence():
    return build_dependency_satisfaction_evidence(
        dependency_ticket_id="P18.1",
        required_relationship="prerequisite_approval",
        satisfaction_state=DependencySatisfactionState.SATISFIED,
        evidence_reference="P18.1 intake approval evidence.",
        evidence_SHA256="c" * 64,
    )


@pytest.fixture(scope="module")
def blocked_dependency_evidence():
    return build_dependency_satisfaction_evidence(
        dependency_ticket_id="P18.1",
        required_relationship="prerequisite_approval",
        satisfaction_state=DependencySatisfactionState.UNSATISFIED,
        evidence_reference="P18.1 prerequisite has no queue-ready evidence.",
        evidence_SHA256=None,
    )


@pytest.fixture(scope="module")
def queue_request(approve_result):
    return build_canonical_p18_dependency_queue_request(
        approval_result=approve_result,
    )


@pytest.fixture(scope="module")
def queue_result(queue_request):
    return build_dependency_aware_queue_integration(queue_request)


@pytest.fixture(scope="module")
def blocked_queue_request(approve_result, blocked_dependency_evidence):
    return build_canonical_p18_dependency_queue_request(
        approval_result=approve_result,
        dependency_satisfaction_evidence=(blocked_dependency_evidence,),
    )


@pytest.fixture(scope="module")
def blocked_queue_result(blocked_queue_request):
    return build_dependency_aware_queue_integration(blocked_queue_request)


@pytest.fixture(scope="module")
def public_model_instances(
    queue_request,
    queue_result,
    blocked_dependency_evidence,
    blocked_queue_result,
):
    return {
        QueueRuntimeCapabilityAssessment: queue_result.runtime_capability_assessments[
            0
        ],
        DependencySatisfactionEvidence: blocked_dependency_evidence,
        DependencyAwareQueueRequest: queue_request,
        DependencyAwareQueueCandidate: queue_result.queue_candidate,
        DependencyQueueBlocker: blocked_queue_result.dependency_blockers[0],
        QueueAdmissionBoundary: queue_result.queue_admission_boundary,
        DependencyAwareQueueFinding: queue_result.findings[0],
        DependencyAwareQueueSummary: queue_result.summary,
        DependencyAwareQueueP18_5Handoff: queue_result.handoff,
        DependencyAwareQueueIntegrationResult: queue_result,
    }


def construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def assert_queue_validation_fails(callback) -> None:
    with pytest.raises((
        ValidationError,
        ValueError,
        DependencyAwareQueueIntegrationError,
    )):
        callback()


@pytest.mark.parametrize("exported_name", P18_4_EXPORTS)
def test_all_p18_4_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(deq, exported_name)


def test_p18_4_exports_are_additive_suffix() -> None:
    p18_0_count = len(p18_0.P18_0_EXPORTS)
    p18_1_count = len(p18_1.P18_1_EXPORTS)
    p18_2_count = len(p18_2.P18_2_EXPORTS)
    p18_3_count = len(p18_3.P18_3_EXPORTS)
    p18_4_start = p18_0_count + p18_1_count + p18_2_count + p18_3_count
    p18_4_end = p18_4_start + len(P18_4_EXPORTS)
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
    assert (
        tuple(
            workflow.__all__[
                p18_0_count + p18_1_count + p18_2_count : p18_0_count
                + p18_1_count
                + p18_2_count
                + p18_3_count
            ]
        )
        == p18_3.P18_3_EXPORTS
    )
    assert tuple(workflow.__all__[p18_4_start:p18_4_end]) == P18_4_EXPORTS
    assert tuple(deq.__all__) == P18_4_EXPORTS
    assert len(workflow.__all__) >= p18_4_end
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_queue_runtime_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert forbidden not in deq.__all__
    assert not hasattr(workflow, forbidden)
    assert not hasattr(deq, forbidden)


@pytest.mark.parametrize(
    "enum_type",
    [
        QueueCapabilityDecision,
        DependencySatisfactionState,
        DependencyAwareQueueDecision,
        DependencyAwareQueueState,
        DependencyAwareQueueFindingSeverity,
        DependencyAwareQueueFindingCode,
    ],
)
def test_controlled_enums_reject_unknown_values(enum_type: type[Enum]) -> None:
    with pytest.raises(ValueError):
        enum_type("__not_a_valid_queue_enum_value__")


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


def test_schema_and_policy_constants_are_exact() -> None:
    assert DEPENDENCY_AWARE_QUEUE_SCHEMA_VERSION == 1
    assert (
        DEPENDENCY_AWARE_QUEUE_POLICY_ID == "pepper-dependency-aware-execution-queue-v1"
    )


def test_request_consumes_approved_p18_3_handoff(queue_request, approve_result) -> None:
    validate_dependency_aware_queue_request(queue_request)
    p18_2_result = approve_result.request.P18_2_result
    packet = p18_2_result.work_packet_compilation_result.work_packet
    assert approve_result.decision is ApprovalWorkflowResultDecision.APPROVED
    assert queue_request.approval_result == approve_result
    assert queue_request.P18_3_result_SHA256 == approve_result.result_SHA256
    assert queue_request.approval_result_SHA256 == approve_result.approval_result_SHA256
    assert (
        queue_request.approval_decision_SHA256
        == approve_result.handoff.approval_decision_SHA256
    )
    assert queue_request.TicketSpec_SHA256 == packet.source_ticket_SHA256
    assert queue_request.WorkPacket_ID == packet.work_packet_id
    assert queue_request.WorkPacket_SHA256 == packet.work_packet_SHA256
    assert queue_request.dependency_plan == p18_2_result.dependency_plan
    assert (
        queue_request.dependency_plan_SHA256 == p18_2_result.dependency_plan.plan_SHA256
    )
    assert (
        queue_request.workflow_snapshot.current_state
        is GovernedWorkflowState.TICKET_APPROVED
    )
    assert queue_request.requested_worker_dispatch is False
    assert queue_request.requested_command_execution is False
    assert queue_request.requested_provider_dispatch is False
    assert queue_request.requested_model_inference is False


def test_canonical_p18_dependency_queue_admits_ready_plan(queue_result) -> None:
    assert queue_result.integration_id.startswith("DQI-P18-")
    assert queue_result.state is DependencyAwareQueueState.COMPLETED
    assert queue_result.decision is DependencyAwareQueueDecision.ADMIT
    assert queue_result.approval_granted is True
    assert queue_result.dependencies_satisfied is True
    assert queue_result.queue_eligible is True
    assert queue_result.queue_admitted is True
    assert queue_result.dispatch_eligible is False
    assert queue_result.ticket_execution_authorized is False
    assert queue_result.WorkPacket_execution_authorized is False
    assert queue_result.execution_started is False
    assert queue_result.WorkPacket_execution_started is False
    assert queue_result.P18_5_ready is True
    assert queue_result.production_readiness_claimed is False
    assert tuple(
        item.transition.transition_id
        for item in queue_result.workflow_transition_results
    ) == (
        "GWT-004",
        "GWT-005",
    )
    assert (
        queue_result.workflow_transition_results[0].resulting_snapshot.current_state
        is GovernedWorkflowState.WORK_PACKET_READY
    )
    assert (
        queue_result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.QUEUED
    )
    assert queue_result.handoff.P18_5_ready is True
    assert queue_result.handoff.resulting_workflow_state is GovernedWorkflowState.QUEUED
    assert not queue_result.dependency_blockers


def test_queue_admission_boundary_preserves_zero_runtime_execution(
    queue_result,
) -> None:
    boundary = queue_result.queue_admission_boundary
    assert boundary.queue_persistence_mechanism == "result_envelope_only"
    assert boundary.provisional_runtime_authority == "kanban_projection_deferred"
    assert boundary.canonical_long_term_authority == "p20_paperclip_deferred"
    assert boundary.Kanban_SQLite_canonical is False
    assert boundary.does_not_dispatch is True
    assert boundary.does_not_execute is True
    assert boundary.duplicate_dependency_planner_created is False
    assert boundary.duplicate_execution_queue_created is False
    assert boundary.duplicate_dispatcher_created is False
    assert boundary.duplicate_Kanban_backend_created is False
    assert boundary.duplicate_WorkPacket_executor_created is False
    assert boundary.duplicate_workflow_state_machine_created is False
    for field in ZERO_COUNT_FIELDS:
        assert getattr(queue_result, field) == 0
    assert queue_result.P17_execution_substrate_reused is True
    assert queue_result.P17_execution_invoked is False
    assert queue_result.cycle_detection_reused is True
    assert queue_result.duplicate_cycle_detector_created is False


def test_summary_and_findings_validate_queue_contract(queue_result) -> None:
    summary = summarize_dependency_aware_queue_integration(queue_result)
    assert summary == queue_result.summary
    assert summary.P18_3_continuation_valid is True
    assert summary.project_identity_valid is True
    assert summary.approval_binding_valid is True
    assert summary.dependency_plan_valid is True
    assert summary.dependency_planner_reused is True
    assert summary.dependency_plan_recomputed_unnecessarily is False
    assert summary.dependency_evidence_valid is True
    assert summary.queue_candidate_valid is True
    assert summary.queue_decision_valid is True
    assert summary.queue_admission_valid is True
    assert summary.dependency_blocking_valid is True
    assert summary.workflow_transition_valid is True
    assert summary.dispatcher_boundary_valid is True
    assert summary.execution_prohibition_valid is True
    assert summary.replay_policy_valid is True
    assert summary.P18_5_handoff_valid is True
    assert summary.warning_finding_count == 0
    assert summary.blocking_finding_count == 0
    assert tuple(finding.finding_id for finding in queue_result.findings) == tuple(
        f"DQIF-{index:03d}" for index in range(1, len(queue_result.findings) + 1)
    )
    assert {
        DependencyAwareQueueFindingCode.P18_3_CONTINUATION_VALID,
        DependencyAwareQueueFindingCode.DEPENDENCY_PLANNER_REUSED,
        DependencyAwareQueueFindingCode.DISPATCHER_BOUNDARY_PRESERVED,
        DependencyAwareQueueFindingCode.EXECUTION_AUTHORITY_PROHIBITED,
        DependencyAwareQueueFindingCode.INTEGRATION_ACCEPTED,
    }.issubset({finding.code for finding in queue_result.findings})


def test_unsatisfied_dependency_evidence_blocks_without_dispatch(
    blocked_queue_result,
) -> None:
    assert blocked_queue_result.state is DependencyAwareQueueState.BLOCKED
    assert blocked_queue_result.decision is DependencyAwareQueueDecision.BLOCKED
    assert blocked_queue_result.dependencies_satisfied is False
    assert blocked_queue_result.queue_eligible is False
    assert blocked_queue_result.queue_admitted is False
    assert blocked_queue_result.dispatch_eligible is False
    assert blocked_queue_result.P18_5_ready is False
    assert len(blocked_queue_result.dependency_blockers) == 1
    blocker = blocked_queue_result.dependency_blockers[0]
    assert blocker.dependency_ticket_id == "P18.1"
    assert blocker.satisfaction_state is DependencySatisfactionState.UNSATISFIED
    assert tuple(
        item.transition.transition_id
        for item in blocked_queue_result.workflow_transition_results
    ) == ("GWT-004", "GWT-026")
    assert (
        blocked_queue_result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.BLOCKED
    )
    assert blocked_queue_result.resulting_workflow_snapshot.active_blocker_codes == (
        "dependency_blocked",
    )
    assert blocked_queue_result.handoff.P18_5_ready is False
    assert (
        blocked_queue_result.handoff.resulting_workflow_state
        is GovernedWorkflowState.BLOCKED
    )
    for field in ZERO_COUNT_FIELDS:
        assert getattr(blocked_queue_result, field) == 0


def test_satisfied_dependency_evidence_preserves_admission(
    approve_result, satisfied_dependency_evidence
) -> None:
    request = build_canonical_p18_dependency_queue_request(
        approval_result=approve_result,
        dependency_satisfaction_evidence=(satisfied_dependency_evidence,),
    )
    result = build_dependency_aware_queue_integration(request)
    assert result.decision is DependencyAwareQueueDecision.ADMIT
    assert result.dependencies_satisfied is True
    assert result.dependency_satisfaction_evidence == (satisfied_dependency_evidence,)
    assert not result.dependency_blockers


def test_rejected_p18_3_handoff_is_not_queue_admissible(reject_result) -> None:
    assert_queue_validation_fails(
        lambda: build_canonical_p18_dependency_queue_request(
            approval_result=reject_result,
        )
    )


def test_satisfied_dependency_evidence_requires_digest() -> None:
    assert_queue_validation_fails(
        lambda: build_dependency_satisfaction_evidence(
            dependency_ticket_id="P18.1",
            required_relationship="prerequisite_approval",
            satisfaction_state=DependencySatisfactionState.SATISFIED,
            evidence_reference="P18.1 completion evidence.",
            evidence_SHA256=None,
        )
    )


def test_unknown_dependency_evidence_is_rejected(approve_result) -> None:
    unknown = build_dependency_satisfaction_evidence(
        dependency_ticket_id="P18.999",
        required_relationship="prerequisite_approval",
        satisfaction_state=DependencySatisfactionState.UNKNOWN,
        evidence_reference="Unknown dependency evidence.",
        evidence_SHA256=None,
    )
    assert_queue_validation_fails(
        lambda: build_canonical_p18_dependency_queue_request(
            approval_result=approve_result,
            dependency_satisfaction_evidence=(unknown,),
        )
    )


def test_queue_replay_is_rejected(approve_result, queue_result) -> None:
    assert_queue_validation_fails(
        lambda: build_canonical_p18_dependency_queue_request(
            approval_result=approve_result,
            prior_queue_result_SHA256=queue_result.result_SHA256,
            prior_queue_decision=queue_result.decision,
        )
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("approval_granted", False),
        ("dispatch_eligible", True),
        ("ticket_execution_authorized", True),
        ("WorkPacket_execution_authorized", True),
        ("execution_started", True),
        ("WorkPacket_execution_started", True),
        ("worker_dispatch_count", 1),
        ("command_execution_count", 1),
        ("provider_dispatch_count", 1),
        ("model_inference_count", 1),
        ("Git_commands_executed", 1),
        ("Docker_commands_executed", 1),
        ("Graphify_commands_executed", 1),
        ("claim_count", 1),
        ("heartbeat_count", 1),
        ("reclaim_count", 1),
        ("workspace_allocation_count", 1),
        ("GBrain_calls", 1),
        ("Paperclip_calls", 1),
        ("P17_execution_invoked", True),
        ("dispatcher_calls_in_P18_4", 1),
        ("production_readiness_claimed", True),
        ("result_SHA256", "0" * 64),
    ],
)
def test_result_tampering_is_rejected(queue_result, field_name, value) -> None:
    tampered = construct_with_updates(queue_result, **{field_name: value})
    assert_queue_validation_fails(
        lambda: validate_dependency_aware_queue_integration_result(tampered)
    )


def test_boundary_tampering_is_rejected(queue_result) -> None:
    boundary = construct_with_updates(
        queue_result.queue_admission_boundary,
        duplicate_dependency_planner_created=True,
    )
    tampered = construct_with_updates(queue_result, queue_admission_boundary=boundary)
    assert_queue_validation_fails(
        lambda: validate_dependency_aware_queue_integration_result(tampered)
    )


def test_handoff_tampering_is_rejected(queue_result) -> None:
    handoff = construct_with_updates(queue_result.handoff, P18_5_ready=False)
    tampered = construct_with_updates(queue_result, handoff=handoff)
    assert_queue_validation_fails(
        lambda: validate_dependency_aware_queue_integration_result(tampered)
    )


def test_request_tampering_is_rejected(queue_request) -> None:
    tampered = construct_with_updates(queue_request, requested_worker_dispatch=True)
    assert_queue_validation_fails(
        lambda: validate_dependency_aware_queue_request(tampered)
    )


def test_queue_request_and_result_are_deterministic(approve_result) -> None:
    first_request = build_canonical_p18_dependency_queue_request(
        approval_result=approve_result,
    )
    second_request = build_canonical_p18_dependency_queue_request(
        approval_result=approve_result,
    )
    assert first_request == second_request
    first_result = build_dependency_aware_queue_integration(first_request)
    second_result = build_dependency_aware_queue_integration(second_request)
    assert first_result == second_result
    assert first_result.result_SHA256 == second_result.result_SHA256


def test_admit_and_block_results_have_unique_digests(
    queue_result, blocked_queue_result
) -> None:
    assert queue_result.queue_result_SHA256 != blocked_queue_result.queue_result_SHA256
    assert queue_result.result_SHA256 != blocked_queue_result.result_SHA256
    assert queue_result.integration_id != blocked_queue_result.integration_id


def test_duplicate_dependency_planner_and_runtime_models_are_not_created() -> None:
    assert not hasattr(deq, "build_ticket_dependency_plan")
    assert not hasattr(deq, "DependencyPlanner")
    assert not hasattr(deq, "DependencyQueueExecutor")
    assert not hasattr(deq, "KanbanQueueStore")
    assert not hasattr(deq, "WorkPacketExecutor")


def test_exception_hierarchy_is_bounded() -> None:
    for error_type in (
        DependencyAwareQueueInputError,
        DependencyAwareQueueIntegrityError,
        DependencyAwareQueuePolicyError,
        DependencyAwareQueueStateError,
        DependencyAwareQueueValidationError,
    ):
        assert issubclass(error_type, DependencyAwareQueueIntegrationError)
