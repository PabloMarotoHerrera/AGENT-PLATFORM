from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.review_validation_loop as rvl
import hermes_cli.agent_platform.work_packet.human_git_handoff as hgh
from hermes_cli.agent_platform.ticket_factory import HumanApprovalDecision
from hermes_cli.agent_platform.work_packet import (
    GitHandoffResult,
    OutcomeEnvelopeKind,
    OutcomeFailureCategory,
    SingleAgentActionExecutionRequest,
    SingleAgentExecutionRequest,
    ToolPermissionOperation,
    build_canonical_p17_closure_request,
    build_human_git_handoff,
    build_p17_work_packet_execution_mvp_closure,
    build_single_agent_execution_authorization,
    build_single_agent_runtime_binding,
    complete_single_agent_execution,
    execute_single_agent_tool_action,
    outcome_envelopes,
    prepare_single_agent_execution,
)
from hermes_cli.agent_platform.workflow import (
    REVIEW_VALIDATION_LOOP_POLICY_ID,
    REVIEW_VALIDATION_LOOP_SCHEMA_VERSION,
    REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION,
    DependencyAwareQueueIntegrationResult,
    DependencySatisfactionState,
    GovernedWorkflowState,
    HermesWorkflowRuntimeKind,
    ReviewValidationCapabilityDecision,
    ReviewValidationCapabilityReuseAssessment,
    ReviewValidationExecutionOutcomeBinding,
    ReviewValidationFinding,
    ReviewValidationFindingCode,
    ReviewValidationFindingSeverity,
    ReviewValidationLoopDecision,
    ReviewValidationLoopError,
    ReviewValidationLoopInputError,
    ReviewValidationLoopIntegrityError,
    ReviewValidationLoopIntegrationResult,
    ReviewValidationLoopPolicyError,
    ReviewValidationLoopRequest,
    ReviewValidationLoopState,
    ReviewValidationLoopStateError,
    ReviewValidationLoopValidationError,
    ReviewValidationP18_6Handoff,
    ReviewValidationRuntimeBoundary,
    ReviewValidationSummary,
    build_approval_workflow_decision_input,
    build_approval_workflow_integration,
    build_canonical_p18_approval_workflow_request,
    build_canonical_p18_dependency_queue_request,
    build_canonical_p18_project_intake_request,
    build_canonical_p18_review_validation_request,
    build_canonical_p18_ticket_factory_runtime_request,
    build_dependency_aware_queue_integration,
    build_dependency_satisfaction_evidence,
    build_governed_workflow_identity,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    build_p17_workflow_binding,
    build_project_intake,
    build_review_validation_loop_integration,
    build_review_validation_reuse_matrix,
    build_ticket_factory_runtime_integration,
    summarize_review_validation_loop_integration,
    validate_review_validation_loop_integration_result,
    validate_review_validation_loop_request,
)
from tests.hermes_cli import (
    test_agent_platform_approval_workflow_integration as p18_3,
)
from tests.hermes_cli import (
    test_agent_platform_dependency_execution_queue as p18_4,
)
from tests.hermes_cli import (
    test_agent_platform_governed_workflow_state_machine as p18_0,
)
from tests.hermes_cli import test_agent_platform_project_intake_workflow as p18_1
from tests.hermes_cli import (
    test_agent_platform_ticket_factory_runtime_integration as p18_2,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_diff_artifact_review as p17_6,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_human_git_handoff as p17_7,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_non_critical_ticket_pilot as p17_8,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_single_agent_execution as p17_3,
)


P18_5_EXPORTS = (
    "REVIEW_VALIDATION_LOOP_SCHEMA_VERSION",
    "REVIEW_VALIDATION_LOOP_POLICY_ID",
    "REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION",
    "ReviewValidationRuntimeBoundary",
    "ReviewValidationCapabilityDecision",
    "ReviewValidationLoopDecision",
    "ReviewValidationLoopState",
    "ReviewValidationFindingSeverity",
    "ReviewValidationFindingCode",
    "ReviewValidationCapabilityReuseAssessment",
    "ReviewValidationExecutionOutcomeBinding",
    "ReviewValidationLoopRequest",
    "ReviewValidationFinding",
    "ReviewValidationSummary",
    "ReviewValidationP18_6Handoff",
    "ReviewValidationLoopIntegrationResult",
    "ReviewValidationLoopError",
    "ReviewValidationLoopInputError",
    "ReviewValidationLoopIntegrityError",
    "ReviewValidationLoopPolicyError",
    "ReviewValidationLoopStateError",
    "ReviewValidationLoopValidationError",
    "build_review_validation_reuse_matrix",
    "build_canonical_p18_review_validation_request",
    "validate_review_validation_loop_request",
    "build_review_validation_loop_integration",
    "validate_review_validation_loop_integration_result",
    "summarize_review_validation_loop_integration",
)

PUBLIC_MODELS = (
    ReviewValidationCapabilityReuseAssessment,
    ReviewValidationExecutionOutcomeBinding,
    ReviewValidationLoopRequest,
    ReviewValidationFinding,
    ReviewValidationSummary,
    ReviewValidationP18_6Handoff,
    ReviewValidationLoopIntegrationResult,
)
PUBLIC_MODEL_FIELD_CASES = tuple(
    (model_type, field_name)
    for model_type in PUBLIC_MODELS
    for field_name in model_type.model_fields
)
CONTROLLED_ENUMS = (
    ReviewValidationRuntimeBoundary,
    ReviewValidationCapabilityDecision,
    ReviewValidationLoopDecision,
    ReviewValidationLoopState,
    ReviewValidationFindingSeverity,
    ReviewValidationFindingCode,
)
FORBIDDEN_PUBLIC_EXPORTS = (
    "ReviewValidationExecutor",
    "ReviewValidationRunner",
    "ReviewValidationRetryController",
    "ReviewValidationRollbackController",
    "execute_work_packet",
    "retry_work_packet",
    "rollback_work_packet",
    "run_validation_command",
    "inspect_diff",
    "stage_reviewed_files",
    "commit_reviewed_files",
    "push_reviewed_files",
    "run_git_command",
    "run_graphify_update",
    "start_p18_6_correction",
)
ZERO_COUNT_FIELDS = (
    "Git_commands_executed",
    "staging_calls",
    "commit_calls",
    "push_calls",
    "retry_execution_count",
    "automatic_retry_count",
    "automatic_requeue_count",
    "rollback_count",
    "autonomous_correction_count",
    "provider_dispatch_count",
    "model_inference_count",
    "Docker_commands_executed",
    "Graphify_commands_executed",
    "GBrain_calls",
    "Paperclip_calls",
    "executor_calls_in_P18_5",
    "workspace_allocation_calls_in_P18_5",
    "validation_command_execution_count",
)
FLOW_RESULT_KEYS = (
    "accepted",
    "validation_failure",
    "diff_blocker",
    "execution_failure",
    "cancellation",
)
NON_ACCEPT_FLOW_KEYS = (
    "validation_failure",
    "diff_blocker",
    "execution_failure",
    "cancellation",
)
NO_GIT_BOOLEAN_FIELDS = (
    "Git_staging_performed",
    "Git_commit_performed",
    "Git_push_performed",
)
DUPLICATE_REUSE_FIELDS = (
    "duplicate_validation_runner_created",
    "duplicate_outcome_envelope_created",
    "duplicate_diff_review_engine_created",
    "duplicate_artifact_review_engine_created",
    "duplicate_Git_handoff_created",
    "duplicate_WorkPacket_executor_created",
    "duplicate_workflow_state_machine_created",
    "duplicate_workspace_allocator_created",
)
REQUEST_BINDING_FIELDS = (
    "P18_4_result_SHA256",
    "queue_result_SHA256",
    "TicketSpec_SHA256",
    "WorkPacket_ID",
    "WorkPacket_SHA256",
    "approval_decision_SHA256",
    "dependency_plan_SHA256",
    "execution_outcome_SHA256",
    "diff_artifact_review_SHA256",
    "human_git_handoff_result_SHA256",
)
REQUEST_IDENTITY_TAMPER_CASES = (
    ("project_id", "OTHER"),
    ("macroproject_id", "P19"),
    ("ticket_id", "P18.3"),
    ("WorkPacket_ID", "WP-P18-2-R0001-aaaaaaaaaaaa"),
    ("WorkPacket_SHA256", "a" * 64),
)
RESULT_DIGEST_FIELDS = (
    "execution_outcome_SHA256",
    "validation_result_SHA256",
    "diff_artifact_review_SHA256",
    "human_git_handoff_result_SHA256",
)
RESULT_COUNTER_FIELDS = tuple(
    dict.fromkeys(
        ZERO_COUNT_FIELDS
        + (
            "Git_commands_executed",
            "staging_calls",
            "commit_calls",
            "push_calls",
        )
    )
)
EXPECTED_FLOW_CONTRACTS = (
    (
        "accepted",
        ReviewValidationLoopDecision.ACCEPT,
        ReviewValidationLoopState.COMPLETED,
        OutcomeEnvelopeKind.RESULT.value,
        True,
        True,
        True,
        False,
        GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
    ),
    (
        "validation_failure",
        ReviewValidationLoopDecision.NEEDS_CORRECTION,
        ReviewValidationLoopState.CORRECTION_REQUIRED,
        OutcomeEnvelopeKind.FAILURE.value,
        False,
        False,
        False,
        True,
        GovernedWorkflowState.AWAITING_CORRECTION,
    ),
    (
        "diff_blocker",
        ReviewValidationLoopDecision.NEEDS_CORRECTION,
        ReviewValidationLoopState.CORRECTION_REQUIRED,
        OutcomeEnvelopeKind.RESULT.value,
        True,
        False,
        False,
        True,
        GovernedWorkflowState.AWAITING_CORRECTION,
    ),
    (
        "execution_failure",
        ReviewValidationLoopDecision.INCIDENT,
        ReviewValidationLoopState.INCIDENT,
        OutcomeEnvelopeKind.FAILURE.value,
        False,
        False,
        False,
        True,
        GovernedWorkflowState.FAILED,
    ),
    (
        "cancellation",
        ReviewValidationLoopDecision.CANCELLED,
        ReviewValidationLoopState.CANCELLED,
        OutcomeEnvelopeKind.CANCELLATION.value,
        False,
        False,
        False,
        True,
        GovernedWorkflowState.CANCELLED,
    ),
)
P18_0_COMMIT = "7b928e60ed4adf49bfb3e47ab9acf1119aaef870"
P18_UI_A_COMMIT = "f55b8a2cc62c9ba0620a14f51b968107b75a78f1"


def _fixture_digest(*parts: object) -> str:
    encoded = ":".join(str(part) for part in parts).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _path_text(path: Path) -> str:
    return path.resolve().as_posix()


def _build_p18_4_queue_result(
    tmp_path_factory,
    *,
    blocked: bool = False,
) -> DependencyAwareQueueIntegrationResult:
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_5_p18_4")
    try:
        pilot_context = p17_8.non_delete_context(monkeypatch, root / "pilot")
        pilot = p17_8.build_non_critical_ticket_pilot(
            p17_8.request_for_context(pilot_context)
        )
        closure_request = build_canonical_p17_closure_request(
            non_critical_pilot_result=pilot
        )
        closure = build_p17_work_packet_execution_mvp_closure(closure_request)
        p17_binding = build_p17_workflow_binding(closure)
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
        snapshot = build_initial_governed_workflow_snapshot(
            identity=identity,
            P17_binding=p17_binding,
            runtime_projection=projection,
        )
        intake_request = build_canonical_p18_project_intake_request(
            initial_workflow_snapshot=snapshot,
            committed_p18_0_commit=P18_0_COMMIT,
            approval=p18_1.valid_approval(
                "Human approves bounded P18.1 Pepper project intake context."
            ),
        )
        intake_result = build_project_intake(intake_request)
        runtime_request = build_canonical_p18_ticket_factory_runtime_request(
            project_intake_result=intake_result,
            committed_p18_ui_a_commit=P18_UI_A_COMMIT,
        )
        runtime_result = build_ticket_factory_runtime_integration(runtime_request)
        decision = build_approval_workflow_decision_input(
            decision=HumanApprovalDecision.APPROVE,
            reviewer_id="human.p18.5",
            decision_reference="P18.3 explicit human approval for P18.5.",
            rationale="Approve the generated TicketSpec before governed queue admission.",
            reason_code="approve_ticket",
            decided_at="2026-08-09T00:00:00Z",
        )
        approval_request = build_canonical_p18_approval_workflow_request(
            ticket_factory_runtime_result=runtime_result,
            decision_input=decision,
        )
        approval_result = build_approval_workflow_integration(approval_request)
        dependency_evidence = ()
        if blocked:
            dependency_evidence = (
                build_dependency_satisfaction_evidence(
                    dependency_ticket_id="P18.1",
                    required_relationship="prerequisite_approval",
                    satisfaction_state=DependencySatisfactionState.UNSATISFIED,
                    evidence_reference="P18.1 prerequisite lacks queue-ready evidence.",
                    evidence_SHA256=None,
                ),
            )
        queue_request = build_canonical_p18_dependency_queue_request(
            approval_result=approval_result,
            dependency_satisfaction_evidence=dependency_evidence,
        )
        return build_dependency_aware_queue_integration(queue_request)
    finally:
        monkeypatch.undo()


def _prepare_workspace_dirs(workspace_root: Path) -> None:
    for relative in (
        "2_products/pepper-agent/docs/agent-platform",
        "2_products/pepper-agent/tests/hermes_cli",
        "2_products/pepper-agent/hermes_cli/agent_platform/workflow",
    ):
        (workspace_root / relative).mkdir(parents=True, exist_ok=True)


def _execution_actions(compilation_result):
    tasks = compilation_result.work_packet.tasks
    return tuple(
        p17_3.action(
            index,
            task.step_id,
            ToolPermissionOperation.CREATE_FILE,
            f"2_products/pepper-agent/docs/agent-platform/p18-5-task-{index:02d}.md",
            content=f"P18.5 bounded fixture action {index}.",
        )
        for index, task in enumerate(tasks, start=1)
    )


def _build_execution_context(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    queue_result: DependencyAwareQueueIntegrationResult,
    *,
    kind: str,
) -> dict[str, object]:
    compilation = queue_result.request.approval_result.request.P18_2_result.work_packet_compilation_result
    workspace_root = tmp_path / kind / "workspace"
    allocated, status_state = p17_3.allocation_result(
        monkeypatch, compilation, workspace_root
    )
    _prepare_workspace_dirs(workspace_root)
    operations = (
        (ToolPermissionOperation.READ_FILE,)
        if kind == "execution_failure"
        else p17_3.GRANTABLE_OPERATIONS
    )
    permissions = p17_3.profile_result(compilation, allocated, operations=operations)
    binding = build_single_agent_runtime_binding(
        agent_id="agent.p18-5",
        worker_id="worker.p18-5",
        work_packet=compilation.work_packet,
    )
    execution_plan = p17_3.plan(_execution_actions(compilation))
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p18-5",
        authorization_reference="AUTH-P18-5-EXECUTION",
        rationale="Authorize synthetic P18.5 fixture WorkPacket execution.",
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        risk_acknowledgement="Synthetic filesystem mutation risk acknowledged.",
    )
    execution_request = SingleAgentExecutionRequest(
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        execution_authorization=authorization,
    )
    session = prepare_single_agent_execution(execution_request)
    if kind == "execution_failure":
        blocked = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=execution_request,
                session=session,
            )
        )
        outcome_request = outcome_envelopes._outcome_request(
            single_agent_execution_session=blocked.updated_session,
        )
        return {
            "compilation": compilation,
            "allocation": allocated,
            "profile": permissions,
            "outcome": outcome_envelopes.build_outcome_envelope(outcome_request),
        }

    for action_index in range(len(execution_plan.actions)):
        action_result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=execution_request,
                session=session,
            )
        )
        session = action_result.updated_session
        if action_index == 0:
            status_state["status"] = (
                " M 2_products/pepper-agent/docs/agent-platform/p18-5-task-01.md"
            )
    single_result = complete_single_agent_execution(session)
    outcome = _existing_p17_5_validation_outcome(single_result, kind=kind)
    return {
        "compilation": compilation,
        "allocation": allocated,
        "profile": permissions,
        "outcome": outcome,
    }


def _wrap_existing_terminal_envelope(envelope):
    data = {
        "schema_version": outcome_envelopes.OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": outcome_envelopes.OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_id": outcome_envelopes._wrapper_id(envelope.envelope_id),
        "envelope_kind": envelope.envelope_kind,
        "result_envelope": envelope
        if envelope.envelope_kind is outcome_envelopes.OutcomeEnvelopeKind.RESULT
        else None,
        "failure_envelope": envelope
        if envelope.envelope_kind is outcome_envelopes.OutcomeEnvelopeKind.FAILURE
        else None,
        "cancellation_envelope": envelope
        if envelope.envelope_kind is outcome_envelopes.OutcomeEnvelopeKind.CANCELLATION
        else None,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return outcome_envelopes.OutcomeEnvelope(
        **data,
        envelope_SHA256=outcome_envelopes._outcome_envelope_digest_from_record(data),
    )


def _existing_p17_5_terminal_evidence(
    single_result,
    *,
    kind: str,
    envelope_kind,
    terminal_state,
    failure_category=outcome_envelopes.OutcomeFailureCategory.NONE,
    cancellation_point=outcome_envelopes.OutcomeCancellationPoint.NONE,
    process_started: bool,
):
    validation_session_sha = _fixture_digest(
        "p18.5-existing-validation-session",
        single_result.result_SHA256,
        kind,
    )
    validation_result_sha = (
        _fixture_digest(
            "p18.5-existing-validation-result",
            single_result.result_SHA256,
            kind,
        )
        if envelope_kind is outcome_envelopes.OutcomeEnvelopeKind.RESULT
        else None
    )
    data = {
        "schema_version": outcome_envelopes.OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": outcome_envelopes.OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_kind": envelope_kind,
        "terminal_stage": outcome_envelopes.OutcomeStage.VALIDATION_COMMAND_RUNNER,
        "terminal_state": terminal_state,
        "terminal_disposition": envelope_kind.value,
        "failure_category": failure_category,
        "cancellation_point": cancellation_point,
        "single_agent_session_SHA256": None,
        "single_agent_result_SHA256": single_result.result_SHA256,
        "validation_command_runner_session_SHA256": validation_session_sha,
        "validation_command_runner_result_SHA256": validation_result_sha,
        "terminal_action_id": None,
        "terminal_task_step_id": None,
        "terminal_command_id": "VCMD-001",
        "terminal_validation_id": "V1",
        "process_started": process_started,
    }
    return outcome_envelopes.OutcomeTerminalEvidence(
        **data,
        terminal_evidence_SHA256=outcome_envelopes._terminal_evidence_digest_from_record(
            data
        ),
    )


def _existing_p17_5_validation_outcome(single_result, *, kind: str):
    packet = single_result.session
    if kind == "validation_failure":
        terminal = _existing_p17_5_terminal_evidence(
            single_result,
            kind=kind,
            envelope_kind=outcome_envelopes.OutcomeEnvelopeKind.FAILURE,
            terminal_state=outcome_envelopes.OutcomeTerminalState.BLOCKED,
            failure_category=outcome_envelopes.OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT,
            process_started=True,
        )
        diagnostic = outcome_envelopes._diagnostic_projection(
            kind=outcome_envelopes.OutcomeEnvelopeKind.FAILURE,
            stage=outcome_envelopes.OutcomeStage.VALIDATION_COMMAND_RUNNER,
            state=outcome_envelopes.OutcomeTerminalState.BLOCKED,
            failure_category=outcome_envelopes.OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT,
            cancellation_point=outcome_envelopes.OutcomeCancellationPoint.NONE,
            process_started=True,
        )
        data = {
            "schema_version": outcome_envelopes.OUTCOME_ENVELOPE_SCHEMA_VERSION,
            "policy_id": outcome_envelopes.OUTCOME_ENVELOPE_POLICY_ID,
            "envelope_id": outcome_envelopes._envelope_id(
                outcome_envelopes.OutcomeEnvelopeKind.FAILURE,
                packet.work_packet_id,
                terminal.terminal_evidence_SHA256,
            ),
            "envelope_kind": outcome_envelopes.OutcomeEnvelopeKind.FAILURE,
            "work_packet_id": packet.work_packet_id,
            "work_packet_SHA256": packet.work_packet_SHA256,
            "allocation_id": packet.allocation_id,
            "allocation_SHA256": packet.allocation_SHA256,
            "profile_id": packet.profile_id,
            "profile_SHA256": packet.profile_SHA256,
            "diagnostic_projection": diagnostic,
            "terminal_evidence": terminal,
            "failure_category": outcome_envelopes.OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT,
            "single_agent_session_SHA256": None,
            "single_agent_result_SHA256": single_result.result_SHA256,
            "validation_command_runner_session_SHA256": terminal.validation_command_runner_session_SHA256,
            "failed_action_id": None,
            "failed_task_step_id": None,
            "failed_command_id": "VCMD-001",
            "failed_validation_id": "V1",
            "result_envelopes_ready": True,
            "diff_artifact_review_ready": False,
            "human_git_handoff_ready": False,
            "automatic_retry_authorized": False,
            "automatic_fallback_authorized": False,
            "automatic_resubmission_authorized": False,
            "provider_dispatch_count": 0,
            "model_inference_count": 0,
        }
        return _wrap_existing_terminal_envelope(
            outcome_envelopes.FailureEnvelope(
                **data,
                envelope_SHA256=outcome_envelopes._failure_envelope_digest_from_record(
                    data
                ),
            )
        )
    if kind == "cancellation":
        terminal = _existing_p17_5_terminal_evidence(
            single_result,
            kind=kind,
            envelope_kind=outcome_envelopes.OutcomeEnvelopeKind.CANCELLATION,
            terminal_state=outcome_envelopes.OutcomeTerminalState.CANCELLED,
            cancellation_point=outcome_envelopes.OutcomeCancellationPoint.VALIDATION_COMMAND_PRELAUNCH,
            process_started=False,
        )
        diagnostic = outcome_envelopes._diagnostic_projection(
            kind=outcome_envelopes.OutcomeEnvelopeKind.CANCELLATION,
            stage=outcome_envelopes.OutcomeStage.VALIDATION_COMMAND_RUNNER,
            state=outcome_envelopes.OutcomeTerminalState.CANCELLED,
            failure_category=outcome_envelopes.OutcomeFailureCategory.NONE,
            cancellation_point=outcome_envelopes.OutcomeCancellationPoint.VALIDATION_COMMAND_PRELAUNCH,
            process_started=False,
        )
        data = {
            "schema_version": outcome_envelopes.OUTCOME_ENVELOPE_SCHEMA_VERSION,
            "policy_id": outcome_envelopes.OUTCOME_ENVELOPE_POLICY_ID,
            "envelope_id": outcome_envelopes._envelope_id(
                outcome_envelopes.OutcomeEnvelopeKind.CANCELLATION,
                packet.work_packet_id,
                terminal.terminal_evidence_SHA256,
            ),
            "envelope_kind": outcome_envelopes.OutcomeEnvelopeKind.CANCELLATION,
            "work_packet_id": packet.work_packet_id,
            "work_packet_SHA256": packet.work_packet_SHA256,
            "allocation_id": packet.allocation_id,
            "allocation_SHA256": packet.allocation_SHA256,
            "profile_id": packet.profile_id,
            "profile_SHA256": packet.profile_SHA256,
            "diagnostic_projection": diagnostic,
            "terminal_evidence": terminal,
            "cancellation_point": outcome_envelopes.OutcomeCancellationPoint.VALIDATION_COMMAND_PRELAUNCH,
            "cancellation_reference": "CANCEL-P18-5",
            "single_agent_session_SHA256": None,
            "single_agent_result_SHA256": single_result.result_SHA256,
            "validation_command_runner_session_SHA256": terminal.validation_command_runner_session_SHA256,
            "cancelled_action_id": None,
            "cancelled_task_step_id": None,
            "cancelled_command_id": "VCMD-001",
            "cancelled_validation_id": "V1",
            "process_started": False,
            "result_envelopes_ready": True,
            "diff_artifact_review_ready": False,
            "human_git_handoff_ready": False,
            "automatic_retry_authorized": False,
            "automatic_fallback_authorized": False,
            "automatic_resubmission_authorized": False,
            "provider_dispatch_count": 0,
            "model_inference_count": 0,
        }
        return _wrap_existing_terminal_envelope(
            outcome_envelopes.CancellationEnvelope(
                **data,
                envelope_SHA256=outcome_envelopes._cancellation_envelope_digest_from_record(
                    data
                ),
            )
        )
    terminal = _existing_p17_5_terminal_evidence(
        single_result,
        kind=kind,
        envelope_kind=outcome_envelopes.OutcomeEnvelopeKind.RESULT,
        terminal_state=outcome_envelopes.OutcomeTerminalState.COMPLETED,
        process_started=True,
    )
    diagnostic = outcome_envelopes._diagnostic_projection(
        kind=outcome_envelopes.OutcomeEnvelopeKind.RESULT,
        stage=outcome_envelopes.OutcomeStage.VALIDATION_COMMAND_RUNNER,
        state=outcome_envelopes.OutcomeTerminalState.COMPLETED,
        failure_category=outcome_envelopes.OutcomeFailureCategory.NONE,
        cancellation_point=outcome_envelopes.OutcomeCancellationPoint.NONE,
        process_started=True,
    )
    data = {
        "schema_version": outcome_envelopes.OUTCOME_ENVELOPE_SCHEMA_VERSION,
        "policy_id": outcome_envelopes.OUTCOME_ENVELOPE_POLICY_ID,
        "envelope_id": outcome_envelopes._envelope_id(
            outcome_envelopes.OutcomeEnvelopeKind.RESULT,
            packet.work_packet_id,
            terminal.terminal_evidence_SHA256,
        ),
        "envelope_kind": outcome_envelopes.OutcomeEnvelopeKind.RESULT,
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": packet.allocation_id,
        "allocation_SHA256": packet.allocation_SHA256,
        "profile_id": packet.profile_id,
        "profile_SHA256": packet.profile_SHA256,
        "diagnostic_projection": diagnostic,
        "terminal_evidence": terminal,
        "completed_task_step_ids": single_result.completed_task_step_ids,
        "touched_paths": single_result.touched_paths,
        "read_paths": single_result.read_paths,
        "created_paths": single_result.created_paths,
        "replaced_paths": single_result.replaced_paths,
        "deleted_paths": single_result.deleted_paths,
        "passed_validation_ids": ("V1",),
        "manual_validation_ids_pending": (),
        "single_agent_result_SHA256": single_result.result_SHA256,
        "validation_command_runner_result_SHA256": terminal.validation_command_runner_result_SHA256,
        "result_envelopes_ready": True,
        "diff_artifact_review_ready": False,
        "human_git_handoff_ready": False,
        "automatic_retry_authorized": False,
        "automatic_fallback_authorized": False,
        "automatic_resubmission_authorized": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
    }
    return _wrap_existing_terminal_envelope(
        outcome_envelopes.ResultEnvelope(
            **data,
            envelope_SHA256=outcome_envelopes._result_envelope_digest_from_record(data),
        )
    )


def _review_result(context: dict[str, object], *, blocked: bool = False):
    paths = (
        (
            p17_6.observed_path(
                1,
                "2_products/pepper-agent/docs/agent-platform/p18-5-unexpected.md",
                p17_6.ReviewObservedPathStatus.UNTRACKED,
                tracked=False,
            ),
        )
        if blocked
        else ()
    )
    observation = p17_6.observation(context, paths)
    return p17_6.build_diff_artifact_review(p17_6.request(context, observation))


def _retarget_handoff(
    base: GitHandoffResult,
    context: dict[str, object],
    review,
) -> GitHandoffResult:
    allocation = context["allocation"].allocation
    profile = context["profile"].profile
    outcome = context["outcome"]
    packet = context["compilation"].work_packet
    data = base.model_dump(mode="python")
    data.update({
        "work_packet_id": packet.work_packet_id,
        "work_packet_SHA256": packet.work_packet_SHA256,
        "allocation_id": allocation.allocation_id,
        "allocation_SHA256": allocation.allocation_SHA256,
        "profile_id": profile.profile_id,
        "profile_SHA256": profile.profile_SHA256,
        "outcome_kind": outcome.envelope_kind,
        "outcome_SHA256": outcome.envelope_SHA256,
        "review_id": review.review_id,
        "review_SHA256": review.result_SHA256,
        "manual_validation_ids_pending": review.manual_validation_ids_pending,
    })
    data["handoff_id"] = hgh._handoff_id({
        key: value
        for key, value in data.items()
        if key not in {"handoff_id", "result_SHA256"}
    })
    data["result_SHA256"] = hgh._result_digest_from_record({
        key: value for key, value in data.items() if key != "result_SHA256"
    })
    return GitHandoffResult.model_validate(data)


def _construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def _assert_review_validation_fails(callback) -> None:
    with pytest.raises((ValidationError, ValueError, ReviewValidationLoopError)):
        callback()


def _build_p17_7_base_handoff(tmp_path_factory) -> GitHandoffResult:
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_5_p17_7")
    try:
        context = p17_6.terminal_context(monkeypatch, root / "accepted", kind="result")
        review = p17_7.review_result(context)
        return build_human_git_handoff(p17_7.handoff_request(context, review))
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="module")
def queue_result(tmp_path_factory):
    return _build_p18_4_queue_result(tmp_path_factory)


@pytest.fixture(scope="module")
def blocked_queue_result(tmp_path_factory):
    return _build_p18_4_queue_result(tmp_path_factory, blocked=True)


@pytest.fixture(scope="module")
def p17_7_base_handoff(tmp_path_factory):
    return _build_p17_7_base_handoff(tmp_path_factory)


@pytest.fixture(scope="module")
def flow_results(
    tmp_path_factory,
    queue_result,
    p17_7_base_handoff,
):
    monkeypatch = pytest.MonkeyPatch()
    tmp_path = tmp_path_factory.mktemp("p18_5_flow")
    try:
        return _build_flow_results(
            monkeypatch,
            tmp_path,
            queue_result,
            p17_7_base_handoff,
        )
    finally:
        monkeypatch.undo()


def _build_flow_results(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    queue_result,
    p17_7_base_handoff,
):
    accepted_context = _build_execution_context(
        monkeypatch,
        tmp_path,
        queue_result,
        kind="result",
    )
    accepted_review = _review_result(accepted_context)
    accepted_handoff = _retarget_handoff(
        p17_7_base_handoff,
        accepted_context,
        accepted_review,
    )
    accepted_request = build_canonical_p18_review_validation_request(
        P18_4_result=queue_result,
        outcome_envelope=accepted_context["outcome"],
        diff_artifact_review_result=accepted_review,
        human_git_handoff_result=accepted_handoff,
    )
    accepted = build_review_validation_loop_integration(accepted_request)

    validation_context = _build_execution_context(
        monkeypatch,
        tmp_path,
        queue_result,
        kind="validation_failure",
    )
    validation_request = build_canonical_p18_review_validation_request(
        P18_4_result=queue_result,
        outcome_envelope=validation_context["outcome"],
        diff_artifact_review_result=_review_result(validation_context),
    )
    validation_failure = build_review_validation_loop_integration(validation_request)

    diff_blocker_request = build_canonical_p18_review_validation_request(
        P18_4_result=queue_result,
        outcome_envelope=accepted_context["outcome"],
        diff_artifact_review_result=_review_result(accepted_context, blocked=True),
    )
    diff_blocker = build_review_validation_loop_integration(diff_blocker_request)

    execution_context = _build_execution_context(
        monkeypatch,
        tmp_path,
        queue_result,
        kind="execution_failure",
    )
    execution_request = build_canonical_p18_review_validation_request(
        P18_4_result=queue_result,
        outcome_envelope=execution_context["outcome"],
        diff_artifact_review_result=_review_result(execution_context),
    )
    execution_failure = build_review_validation_loop_integration(execution_request)

    cancellation_context = _build_execution_context(
        monkeypatch,
        tmp_path,
        queue_result,
        kind="cancellation",
    )
    cancellation_request = build_canonical_p18_review_validation_request(
        P18_4_result=queue_result,
        outcome_envelope=cancellation_context["outcome"],
        diff_artifact_review_result=_review_result(cancellation_context),
    )
    cancellation = build_review_validation_loop_integration(cancellation_request)

    return {
        "accepted": accepted,
        "accepted_request": accepted_request,
        "accepted_context": accepted_context,
        "accepted_review": accepted_review,
        "validation_failure": validation_failure,
        "diff_blocker": diff_blocker,
        "execution_failure": execution_failure,
        "cancellation": cancellation,
    }


@pytest.fixture(scope="module")
def public_model_instances(flow_results):
    accepted = flow_results["accepted"]
    return {
        ReviewValidationCapabilityReuseAssessment: accepted.capability_reuse_assessments[
            0
        ],
        ReviewValidationExecutionOutcomeBinding: accepted.execution_outcome_binding,
        ReviewValidationLoopRequest: accepted.request,
        ReviewValidationFinding: accepted.findings[0],
        ReviewValidationSummary: accepted.summary,
        ReviewValidationP18_6Handoff: flow_results["validation_failure"].P18_6_handoff,
        ReviewValidationLoopIntegrationResult: accepted,
    }


@pytest.mark.parametrize("exported_name", P18_5_EXPORTS)
def test_all_p18_5_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(rvl, exported_name)


def test_p18_5_exports_are_additive_suffix() -> None:
    p18_0_count = len(p18_0.P18_0_EXPORTS)
    p18_1_count = len(p18_1.P18_1_EXPORTS)
    p18_2_count = len(p18_2.P18_2_EXPORTS)
    p18_3_count = len(p18_3.P18_3_EXPORTS)
    p18_4_count = len(p18_4.P18_4_EXPORTS)
    p18_5_start = p18_0_count + p18_1_count + p18_2_count + p18_3_count + p18_4_count
    p18_5_end = p18_5_start + len(P18_5_EXPORTS)
    assert tuple(workflow.__all__[:p18_0_count]) == p18_0.P18_0_EXPORTS
    assert tuple(workflow.__all__[p18_5_start:p18_5_end]) == P18_5_EXPORTS
    assert tuple(rvl.__all__) == P18_5_EXPORTS
    assert len(workflow.__all__) >= p18_5_end
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_runtime_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert forbidden not in rvl.__all__
    assert not hasattr(workflow, forbidden)
    assert not hasattr(rvl, forbidden)


def test_schema_policy_and_boundary_constants_are_exact() -> None:
    assert REVIEW_VALIDATION_LOOP_SCHEMA_VERSION == 1
    assert REVIEW_VALIDATION_LOOP_POLICY_ID == "pepper-review-validation-loop-v1"
    assert (
        REVIEW_VALIDATION_RUNTIME_BOUNDARY_CLASSIFICATION
        == "REVIEW_POST_EXECUTION_ONLY"
    )


@pytest.mark.parametrize(
    "error_cls",
    (
        ReviewValidationLoopError,
        ReviewValidationLoopInputError,
        ReviewValidationLoopIntegrityError,
        ReviewValidationLoopPolicyError,
        ReviewValidationLoopStateError,
        ReviewValidationLoopValidationError,
    ),
)
def test_public_exceptions_are_value_errors(error_cls: type[Exception]) -> None:
    assert issubclass(error_cls, ValueError)


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_controlled_enums_reject_unknown_values(enum_cls: type) -> None:
    with pytest.raises(ValueError):
        enum_cls("__unknown_p18_5_enum__")


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_frozen_and_forbid_extra_fields(
    model_cls: type[BaseModel],
) -> None:
    assert model_cls.model_config["frozen"] is True
    assert model_cls.model_config["extra"] == "forbid"
    assert model_cls.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_round_trip(model_cls: type[BaseModel], flow_results) -> None:
    accepted = flow_results["accepted"]
    samples = {
        ReviewValidationCapabilityReuseAssessment: accepted.capability_reuse_assessments[
            0
        ],
        ReviewValidationExecutionOutcomeBinding: accepted.execution_outcome_binding,
        ReviewValidationLoopRequest: accepted.request,
        ReviewValidationFinding: accepted.findings[0],
        ReviewValidationSummary: accepted.summary,
        ReviewValidationP18_6Handoff: flow_results["validation_failure"].P18_6_handoff,
        ReviewValidationLoopIntegrationResult: accepted,
    }
    model = samples[model_cls]
    assert model_cls.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_reject_unknown_fields(
    model_cls: type[BaseModel], flow_results
) -> None:
    accepted = flow_results["accepted"]
    samples = {
        ReviewValidationCapabilityReuseAssessment: accepted.capability_reuse_assessments[
            0
        ],
        ReviewValidationExecutionOutcomeBinding: accepted.execution_outcome_binding,
        ReviewValidationLoopRequest: accepted.request,
        ReviewValidationFinding: accepted.findings[0],
        ReviewValidationSummary: accepted.summary,
        ReviewValidationP18_6Handoff: flow_results["validation_failure"].P18_6_handoff,
        ReviewValidationLoopIntegrationResult: accepted,
    }
    data = samples[model_cls].model_dump(mode="json")
    data["unknown"] = "blocked"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


def test_reuse_matrix_retains_p17_authorities_without_duplicates() -> None:
    matrix = build_review_validation_reuse_matrix()
    assert len(matrix) == 12
    assert all(row.suitable_for_P18_5 for row in matrix)
    assert all(
        row.decision is ReviewValidationCapabilityDecision.RETAIN for row in matrix
    )
    assert not any(row.customized or row.duplicate_created for row in matrix)
    assert {row.symbol for row in matrix} >= {
        "ValidationCommandRunnerResult",
        "OutcomeEnvelope",
        "DiffReviewVerdict",
        "GitHandoffResult",
        "GovernedWorkflowTransitionResult",
    }


def test_accept_flow_reuses_p17_and_waits_for_human_git_handoff(flow_results) -> None:
    result = flow_results["accepted"]
    validate_review_validation_loop_request(result.request)
    validate_review_validation_loop_integration_result(result)
    assert result.decision is ReviewValidationLoopDecision.ACCEPT
    assert result.state is ReviewValidationLoopState.COMPLETED
    assert result.resulting_workflow_snapshot.current_state is (
        GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF
    )
    assert result.validation_passed is True
    assert result.diff_artifact_review_passed is True
    assert result.review_accepted is True
    assert result.human_git_handoff_ready is True
    assert result.P18_6_ready is False
    assert result.P18_6_handoff is None
    assert result.P17_validation_runner_reused is True
    assert result.P17_outcome_envelopes_reused is True
    assert result.P17_diff_artifact_review_reused is True
    assert result.P17_human_Git_handoff_reused_or_deferred_with_evidence is True
    assert summarize_review_validation_loop_integration(result) == result.summary


@pytest.mark.parametrize("field", ZERO_COUNT_FIELDS)
def test_accept_flow_never_mutates_git_or_runtime(field: str, flow_results) -> None:
    assert getattr(flow_results["accepted"], field) == 0
    assert flow_results["accepted"].Git_staging_performed is False
    assert flow_results["accepted"].Git_commit_performed is False
    assert flow_results["accepted"].Git_push_performed is False


def test_validation_failure_flow_hands_off_to_p18_6_without_retry(flow_results) -> None:
    result = flow_results["validation_failure"]
    assert result.decision is ReviewValidationLoopDecision.NEEDS_CORRECTION
    assert result.state is ReviewValidationLoopState.CORRECTION_REQUIRED
    assert (
        result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.AWAITING_CORRECTION
    )
    assert result.execution_outcome_state == OutcomeEnvelopeKind.FAILURE.value
    assert result.validation_passed is False
    assert result.review_accepted is False
    assert result.P18_6_ready is True
    assert result.P18_6_handoff is not None
    assert result.P18_6_handoff.retry_started is False
    assert result.P18_6_handoff.rollback_started is False
    assert OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT.value in (
        result.P18_6_handoff.blocker_codes
    )


def test_diff_blocker_flow_hands_off_to_p18_6_without_retry(flow_results) -> None:
    result = flow_results["diff_blocker"]
    assert result.decision is ReviewValidationLoopDecision.NEEDS_CORRECTION
    assert result.state is ReviewValidationLoopState.CORRECTION_REQUIRED
    assert (
        result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.AWAITING_CORRECTION
    )
    assert result.validation_passed is True
    assert result.diff_artifact_review_passed is False
    assert result.P18_6_ready is True
    assert result.P18_6_handoff is not None
    assert "diff_blocked" in result.P18_6_handoff.blocker_codes


def test_execution_failure_flow_records_incident_without_retry(flow_results) -> None:
    result = flow_results["execution_failure"]
    assert result.decision is ReviewValidationLoopDecision.INCIDENT
    assert result.state is ReviewValidationLoopState.INCIDENT
    assert (
        result.resulting_workflow_snapshot.current_state is GovernedWorkflowState.FAILED
    )
    assert result.execution_outcome_state == OutcomeEnvelopeKind.FAILURE.value
    assert (
        result.execution_outcome_binding.terminal_stage.value
        == "single_agent_execution"
    )
    assert result.P18_6_ready is True
    assert result.P18_6_handoff is not None
    assert result.retry_execution_count == 0
    assert result.rollback_count == 0


def test_cancellation_flow_is_terminal_without_retry(flow_results) -> None:
    result = flow_results["cancellation"]
    assert result.decision is ReviewValidationLoopDecision.CANCELLED
    assert result.state is ReviewValidationLoopState.CANCELLED
    assert (
        result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.CANCELLED
    )
    assert result.execution_outcome_state == OutcomeEnvelopeKind.CANCELLATION.value
    assert result.P18_6_ready is True
    assert result.P18_6_handoff is not None
    assert result.P18_6_handoff.blocker_codes == ("execution_cancelled",)
    assert result.retry_execution_count == 0
    assert result.rollback_count == 0


def test_accept_requires_existing_p17_7_handoff(flow_results, queue_result) -> None:
    context = flow_results["accepted_context"]
    review = flow_results["accepted_review"]
    request = build_canonical_p18_review_validation_request(
        P18_4_result=queue_result,
        outcome_envelope=context["outcome"],
        diff_artifact_review_result=review,
    )
    with pytest.raises(ReviewValidationLoopPolicyError):
        build_review_validation_loop_integration(request)


def test_replay_policy_blocks_prior_review_result(flow_results, queue_result) -> None:
    accepted = flow_results["accepted"]
    context = flow_results["accepted_context"]
    review = flow_results["accepted_review"]
    with pytest.raises(ReviewValidationLoopStateError):
        build_canonical_p18_review_validation_request(
            P18_4_result=queue_result,
            outcome_envelope=context["outcome"],
            diff_artifact_review_result=review,
            prior_review_result_SHA256=accepted.result_SHA256,
            prior_review_decision=accepted.decision,
        )


def test_request_rejects_work_packet_binding_tamper(flow_results) -> None:
    request = flow_results["accepted_request"]
    tampered = ReviewValidationLoopRequest.model_construct(**{
        **request.model_dump(mode="python"),
        "WorkPacket_ID": "WP-P18-2-R0001-aaaaaaaaaaaa",
    })
    with pytest.raises(ReviewValidationLoopValidationError):
        validate_review_validation_loop_request(tampered)


def test_result_rejects_runtime_counter_tamper(flow_results) -> None:
    result = flow_results["accepted"]
    data = result.model_dump(mode="python")
    data["Git_commands_executed"] = 1
    tampered = ReviewValidationLoopIntegrationResult.model_construct(**data)
    with pytest.raises(ReviewValidationLoopValidationError):
        validate_review_validation_loop_integration_result(tampered)


@pytest.mark.parametrize(("model_cls", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_fields_are_individually_frozen(
    model_cls: type[BaseModel],
    field_name: str,
    public_model_instances,
) -> None:
    model = public_model_instances[model_cls]
    with pytest.raises(ValidationError):
        setattr(model, field_name, getattr(model, field_name))


@pytest.mark.parametrize(("model_cls", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_python_dump_round_trip_preserves_each_field(
    model_cls: type[BaseModel],
    field_name: str,
    public_model_instances,
) -> None:
    model = public_model_instances[model_cls]
    round_tripped = model_cls.model_validate(model.model_dump(mode="python"))
    assert getattr(round_tripped, field_name) == getattr(model, field_name)


@pytest.mark.parametrize(("model_cls", "field_name"), PUBLIC_MODEL_FIELD_CASES)
def test_public_model_json_dump_round_trip_preserves_each_field(
    model_cls: type[BaseModel],
    field_name: str,
    public_model_instances,
) -> None:
    model = public_model_instances[model_cls]
    round_tripped = model_cls.model_validate_json(model.model_dump_json())
    assert getattr(round_tripped, field_name) == getattr(model, field_name)


def test_canonical_P18_review_validation_accept_flow(flow_results) -> None:
    result = flow_results["accepted"]
    assert result.decision is ReviewValidationLoopDecision.ACCEPT
    assert result.review_accepted is True
    assert result.validation_passed is True
    assert result.diff_artifact_review_passed is True
    assert result.human_git_handoff_ready is True
    assert result.P18_6_ready is False


def test_canonical_P18_review_validation_validation_failure_flow(flow_results) -> None:
    result = flow_results["validation_failure"]
    assert result.decision is ReviewValidationLoopDecision.NEEDS_CORRECTION
    assert result.validation_passed is False
    assert result.diff_artifact_review_passed is False
    assert result.P18_6_ready is True
    assert result.P18_6_handoff is not None


def test_canonical_P18_review_validation_diff_blocker_flow(flow_results) -> None:
    result = flow_results["diff_blocker"]
    assert result.decision is ReviewValidationLoopDecision.NEEDS_CORRECTION
    assert result.validation_passed is True
    assert result.diff_artifact_review_passed is False
    assert result.P18_6_ready is True
    assert result.P18_6_handoff is not None


def test_canonical_P18_review_validation_execution_failure_flow(flow_results) -> None:
    result = flow_results["execution_failure"]
    assert result.decision is ReviewValidationLoopDecision.INCIDENT
    assert result.execution_outcome_state == OutcomeEnvelopeKind.FAILURE.value
    assert result.validation_result_SHA256 is None
    assert result.P18_6_ready is True


def test_canonical_P18_review_validation_cancellation_flow(flow_results) -> None:
    result = flow_results["cancellation"]
    assert result.decision is ReviewValidationLoopDecision.CANCELLED
    assert result.execution_outcome_state == OutcomeEnvelopeKind.CANCELLATION.value
    assert result.human_git_handoff_ready is False
    assert result.P18_6_ready is True


def test_canonical_P18_review_validation_never_mutates_git(flow_results) -> None:
    for flow_key in FLOW_RESULT_KEYS:
        result = flow_results[flow_key]
        assert result.Git_commands_executed == 0
        assert result.Git_staging_performed is False
        assert result.Git_commit_performed is False
        assert result.Git_push_performed is False


@pytest.mark.parametrize(
    (
        "flow_key",
        "decision",
        "state",
        "outcome_state",
        "validation_passed",
        "diff_passed",
        "handoff_ready",
        "p18_6_ready",
        "workflow_state",
    ),
    EXPECTED_FLOW_CONTRACTS,
)
def test_canonical_flow_contract_matrix(
    flow_results,
    flow_key: str,
    decision: ReviewValidationLoopDecision,
    state: ReviewValidationLoopState,
    outcome_state: str,
    validation_passed: bool,
    diff_passed: bool,
    handoff_ready: bool,
    p18_6_ready: bool,
    workflow_state: GovernedWorkflowState,
) -> None:
    result = flow_results[flow_key]
    assert result.decision is decision
    assert result.state is state
    assert result.execution_outcome_state == outcome_state
    assert result.validation_passed is validation_passed
    assert result.diff_artifact_review_passed is diff_passed
    assert result.review_accepted is (decision is ReviewValidationLoopDecision.ACCEPT)
    assert result.human_git_handoff_ready is handoff_ready
    assert result.P18_6_ready is p18_6_ready
    assert result.resulting_workflow_snapshot.current_state is workflow_state


@pytest.mark.parametrize("flow_key", FLOW_RESULT_KEYS)
@pytest.mark.parametrize("field", ZERO_COUNT_FIELDS)
def test_all_flows_keep_runtime_authority_counters_zero(
    flow_results,
    flow_key: str,
    field: str,
) -> None:
    assert getattr(flow_results[flow_key], field) == 0


@pytest.mark.parametrize("flow_key", FLOW_RESULT_KEYS)
@pytest.mark.parametrize("field", NO_GIT_BOOLEAN_FIELDS)
def test_all_flows_keep_git_mutation_flags_false(
    flow_results,
    flow_key: str,
    field: str,
) -> None:
    assert getattr(flow_results[flow_key], field) is False


@pytest.mark.parametrize("field", DUPLICATE_REUSE_FIELDS)
def test_p18_5_creates_no_duplicate_p17_or_p18_runtime_components(
    flow_results,
    field: str,
) -> None:
    assert getattr(flow_results["accepted"], field) is False


@pytest.mark.parametrize("flow_key", FLOW_RESULT_KEYS)
def test_project_ticket_and_work_packet_identity_preserved(
    flow_results,
    flow_key: str,
) -> None:
    result = flow_results[flow_key]
    request = result.request
    candidate = request.P18_4_result.queue_candidate
    assert result.project_id == "PEPPER"
    assert result.macroproject_id == "P18"
    assert result.ticket_id == "P18.2"
    assert result.WorkPacket_ID == candidate.WorkPacket_ID
    assert result.WorkPacket_SHA256 == candidate.WorkPacket_SHA256
    assert result.execution_outcome_binding.WorkPacket_ID == candidate.WorkPacket_ID
    assert (
        result.execution_outcome_binding.WorkPacket_SHA256
        == candidate.WorkPacket_SHA256
    )


@pytest.mark.parametrize("flow_key", NON_ACCEPT_FLOW_KEYS)
def test_non_accept_flows_emit_p18_6_handoff_without_retry_or_rollback(
    flow_results,
    flow_key: str,
) -> None:
    result = flow_results[flow_key]
    handoff = result.P18_6_handoff
    assert handoff is not None
    assert handoff.project_id == "PEPPER"
    assert handoff.macroproject_id == "P18"
    assert handoff.ticket_id == "P18.2"
    assert handoff.WorkPacket_ID == result.WorkPacket_ID
    assert handoff.WorkPacket_SHA256 == result.WorkPacket_SHA256
    assert handoff.retry_started is False
    assert handoff.rollback_started is False


def test_p18_4_blocked_continuation_is_rejected(
    blocked_queue_result,
    flow_results,
) -> None:
    context = flow_results["accepted_context"]
    review = flow_results["accepted_review"]
    _assert_review_validation_fails(
        lambda: build_canonical_p18_review_validation_request(
            P18_4_result=blocked_queue_result,
            outcome_envelope=context["outcome"],
            diff_artifact_review_result=review,
        )
    )


@pytest.mark.parametrize(("field", "value"), REQUEST_IDENTITY_TAMPER_CASES)
def test_wrong_project_ticket_or_work_packet_identity_is_rejected(
    flow_results,
    field: str,
    value: object,
) -> None:
    request = flow_results["accepted_request"]
    tampered = _construct_with_updates(request, **{field: value})
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_request(tampered)
    )


@pytest.mark.parametrize("field", REQUEST_BINDING_FIELDS)
def test_stale_request_binding_digest_is_rejected(flow_results, field: str) -> None:
    request = flow_results["accepted_request"]
    stale_value = (
        "WP-P18-2-R0001-aaaaaaaaaaaa" if field == "WorkPacket_ID" else "a" * 64
    )
    if getattr(request, field) == stale_value:
        stale_value = "b" * 64
    tampered = _construct_with_updates(request, **{field: stale_value})
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_request(tampered)
    )


def test_stale_p18_4_result_object_is_rejected(flow_results) -> None:
    request = flow_results["accepted_request"]
    stale_p18_4 = _construct_with_updates(request.P18_4_result, result_SHA256="a" * 64)
    tampered = _construct_with_updates(request, P18_4_result=stale_p18_4)
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_request(tampered)
    )


def test_stale_execution_outcome_object_is_rejected(flow_results) -> None:
    request = flow_results["accepted_request"]
    stale_outcome = _construct_with_updates(
        request.outcome_envelope,
        envelope_SHA256="a" * 64,
    )
    tampered = _construct_with_updates(request, outcome_envelope=stale_outcome)
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_request(tampered)
    )


def test_stale_diff_artifact_review_object_is_rejected(flow_results) -> None:
    request = flow_results["accepted_request"]
    stale_review = _construct_with_updates(
        request.diff_artifact_review_result,
        result_SHA256="a" * 64,
    )
    tampered = _construct_with_updates(
        request, diff_artifact_review_result=stale_review
    )
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_request(tampered)
    )


def test_stale_human_git_handoff_object_is_rejected(flow_results) -> None:
    request = flow_results["accepted_request"]
    assert request.human_git_handoff_result is not None
    stale_handoff = _construct_with_updates(
        request.human_git_handoff_result,
        result_SHA256="a" * 64,
    )
    tampered = _construct_with_updates(request, human_git_handoff_result=stale_handoff)
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_request(tampered)
    )


@pytest.mark.parametrize("prior_decision", tuple(ReviewValidationLoopDecision))
def test_duplicate_or_conflicting_second_review_is_rejected(
    flow_results,
    queue_result,
    prior_decision: ReviewValidationLoopDecision,
) -> None:
    accepted = flow_results["accepted"]
    context = flow_results["accepted_context"]
    review = flow_results["accepted_review"]
    _assert_review_validation_fails(
        lambda: build_canonical_p18_review_validation_request(
            P18_4_result=queue_result,
            outcome_envelope=context["outcome"],
            diff_artifact_review_result=review,
            prior_review_result_SHA256=accepted.result_SHA256,
            prior_review_decision=prior_decision,
        )
    )


def test_exact_duplicate_without_prior_review_marker_is_deterministic(
    flow_results,
) -> None:
    rebuilt = build_review_validation_loop_integration(flow_results["accepted_request"])
    assert rebuilt == flow_results["accepted"]
    assert rebuilt.result_SHA256 == flow_results["accepted"].result_SHA256


@pytest.mark.parametrize("field", RESULT_DIGEST_FIELDS)
def test_result_digest_binding_tampering_is_rejected(flow_results, field: str) -> None:
    result = flow_results["accepted"]
    tampered = _construct_with_updates(result, **{field: "a" * 64})
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_integration_result(tampered)
    )


@pytest.mark.parametrize("field", RESULT_COUNTER_FIELDS)
def test_result_authority_counter_tampering_is_rejected(
    flow_results,
    field: str,
) -> None:
    result = flow_results["accepted"]
    tampered = _construct_with_updates(result, **{field: 1})
    _assert_review_validation_fails(
        lambda: validate_review_validation_loop_integration_result(tampered)
    )


@pytest.mark.parametrize("flow_key", FLOW_RESULT_KEYS)
def test_result_and_summary_serialization_are_stable(
    flow_results, flow_key: str
) -> None:
    result = flow_results[flow_key]
    assert (
        ReviewValidationLoopIntegrationResult.model_validate_json(
            result.model_dump_json()
        )
        == result
    )
    assert (
        ReviewValidationSummary.model_validate_json(result.summary.model_dump_json())
        == result.summary
    )


@pytest.mark.parametrize("flow_key", FLOW_RESULT_KEYS)
def test_workflow_transition_results_are_accepted_and_bound(
    flow_results,
    flow_key: str,
) -> None:
    result = flow_results[flow_key]
    assert result.workflow_transition_results
    assert result.resulting_workflow_snapshot == (
        result.workflow_transition_results[-1].resulting_snapshot
    )
    assert all(transition.accepted for transition in result.workflow_transition_results)
    assert all(
        transition.transition.transition_id.startswith("GWT-")
        for transition in result.workflow_transition_results
    )


def test_runtime_boundary_consumes_p17_5_outcome_without_p17_4_invocation(
    flow_results,
) -> None:
    accepted = flow_results["accepted"]
    assert accepted.request.runtime_boundary_classification is (
        ReviewValidationRuntimeBoundary.REVIEW_POST_EXECUTION_ONLY
    )
    assert accepted.executor_calls_in_P18_5 == 0
    assert accepted.workspace_allocation_calls_in_P18_5 == 0
    assert accepted.validation_command_execution_count == 0
    assert accepted.request.outcome_envelope.result_envelope is not None
    assert accepted.P17_outcome_envelopes_reused is True
    assert accepted.P17_validation_runner_reused is True
