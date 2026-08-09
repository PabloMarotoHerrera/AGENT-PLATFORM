from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.retry_incident_rollback as rir
from hermes_cli.agent_platform.workflow import (
    RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION,
    RETRY_INCIDENT_ROLLBACK_POLICY_ID,
    RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION,
    GovernedWorkflowState,
    RetryAttemptPlan,
    RetryIncidentRecord,
    RetryIncidentRollbackBoundary,
    RetryIncidentRollbackCapabilityDecision,
    RetryIncidentRollbackCapabilityReuseAssessment,
    RetryIncidentRollbackDecision,
    RetryIncidentRollbackError,
    RetryIncidentRollbackFinding,
    RetryIncidentRollbackFindingCode,
    RetryIncidentRollbackFindingSeverity,
    RetryIncidentRollbackHumanAuthorization,
    RetryIncidentRollbackInputError,
    RetryIncidentRollbackIntegrityError,
    RetryIncidentRollbackPolicyError,
    RetryIncidentRollbackRequest,
    RetryIncidentRollbackRequestedAction,
    RetryIncidentRollbackResult,
    RetryIncidentRollbackState,
    RetryIncidentRollbackStateError,
    RetryIncidentRollbackSummary,
    RetryIncidentRollbackValidationError,
    RollbackGovernancePlan,
    build_canonical_p18_retry_incident_rollback_request,
    build_retry_incident_rollback_human_authorization,
    build_retry_incident_rollback_reuse_matrix,
    build_retry_incident_rollback_workflow,
    summarize_retry_incident_rollback_workflow,
    validate_retry_incident_rollback_request,
    validate_retry_incident_rollback_result,
)
from tests.hermes_cli import (
    test_agent_platform_governed_workflow_state_machine as p18_0,
)
from tests.hermes_cli import test_agent_platform_project_intake_workflow as p18_1
from tests.hermes_cli import (
    test_agent_platform_ticket_factory_runtime_integration as p18_2,
)
from tests.hermes_cli import (
    test_agent_platform_approval_workflow_integration as p18_3,
)
from tests.hermes_cli import (
    test_agent_platform_dependency_execution_queue as p18_4,
)
from tests.hermes_cli import (
    test_agent_platform_review_validation_loop as p18_5,
)


P18_6_EXPORTS = (
    "RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION",
    "RETRY_INCIDENT_ROLLBACK_POLICY_ID",
    "RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION",
    "RetryIncidentRollbackBoundary",
    "RetryIncidentRollbackCapabilityDecision",
    "RetryIncidentRollbackRequestedAction",
    "RetryIncidentRollbackDecision",
    "RetryIncidentRollbackState",
    "RetryIncidentRollbackFindingSeverity",
    "RetryIncidentRollbackFindingCode",
    "RetryIncidentRollbackHumanAuthorization",
    "RetryIncidentRollbackCapabilityReuseAssessment",
    "RetryIncidentRollbackRequest",
    "RetryAttemptPlan",
    "RetryIncidentRecord",
    "RollbackGovernancePlan",
    "RetryIncidentRollbackFinding",
    "RetryIncidentRollbackSummary",
    "RetryIncidentRollbackResult",
    "RetryIncidentRollbackError",
    "RetryIncidentRollbackInputError",
    "RetryIncidentRollbackIntegrityError",
    "RetryIncidentRollbackPolicyError",
    "RetryIncidentRollbackStateError",
    "RetryIncidentRollbackValidationError",
    "build_retry_incident_rollback_human_authorization",
    "build_retry_incident_rollback_reuse_matrix",
    "build_canonical_p18_retry_incident_rollback_request",
    "validate_retry_incident_rollback_request",
    "build_retry_incident_rollback_workflow",
    "validate_retry_incident_rollback_result",
    "summarize_retry_incident_rollback_workflow",
)

PUBLIC_MODELS = (
    RetryIncidentRollbackHumanAuthorization,
    RetryIncidentRollbackCapabilityReuseAssessment,
    RetryIncidentRollbackRequest,
    RetryAttemptPlan,
    RetryIncidentRecord,
    RollbackGovernancePlan,
    RetryIncidentRollbackFinding,
    RetryIncidentRollbackSummary,
    RetryIncidentRollbackResult,
)
PUBLIC_MODEL_FIELD_CASES = tuple(
    (model_type, field_name)
    for model_type in PUBLIC_MODELS
    for field_name in model_type.model_fields
)
CONTROLLED_ENUMS = (
    RetryIncidentRollbackBoundary,
    RetryIncidentRollbackCapabilityDecision,
    RetryIncidentRollbackRequestedAction,
    RetryIncidentRollbackDecision,
    RetryIncidentRollbackState,
    RetryIncidentRollbackFindingSeverity,
    RetryIncidentRollbackFindingCode,
)
FORBIDDEN_PUBLIC_EXPORTS = (
    "RetryIncidentRollbackExecutor",
    "RetryController",
    "RollbackExecutor",
    "IncidentStore",
    "execute_retry",
    "retry_work_packet",
    "requeue_task",
    "reclaim_task",
    "reassign_task",
    "rollback_worktree",
    "run_git_command",
    "restore_workspace",
    "run_graphify_update",
    "call_provider",
    "call_model",
)
ZERO_COUNT_FIELDS = (
    "Git_commands_executed",
    "staging_calls",
    "commit_calls",
    "push_calls",
    "retry_execution_count",
    "automatic_retry_count",
    "automatic_requeue_count",
    "Kanban_requeue_calls",
    "Kanban_reclaim_calls",
    "Kanban_reassign_calls",
    "rollback_execution_count",
    "workspace_allocation_calls_in_P18_6",
    "workspace_cleanup_calls_in_P18_6",
    "workspace_restore_calls_in_P18_6",
    "provider_dispatch_count",
    "model_inference_count",
    "Docker_commands_executed",
    "Graphify_commands_executed",
    "GBrain_calls",
    "Paperclip_calls",
)
FALSE_AUTHORITY_FIELDS = (
    "Git_staging_performed",
    "Git_commit_performed",
    "Git_push_performed",
    "Kanban_SQLite_canonical_authority",
)
DUPLICATE_FIELDS = (
    "duplicate_retry_controller_created",
    "duplicate_requeue_controller_created",
    "duplicate_incident_store_created",
    "duplicate_rollback_controller_created",
    "duplicate_workspace_restorer_created",
    "duplicate_Git_handoff_created",
    "duplicate_workflow_state_machine_created",
)
FLOW_KEYS = (
    "validation_failure",
    "diff_blocker",
    "execution_incident",
    "execution_retry",
    "execution_retry_exhausted",
    "execution_rollback",
    "cancellation",
)


def _construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def _assert_p18_6_fails(callback) -> None:
    with pytest.raises((ValidationError, ValueError, RetryIncidentRollbackError)):
        callback()


@pytest.fixture(scope="module")
def p18_5_flow_results(tmp_path_factory):
    queue_result = p18_5._build_p18_4_queue_result(tmp_path_factory)
    p17_7_base_handoff = p18_5._build_p17_7_base_handoff(tmp_path_factory)
    monkeypatch = pytest.MonkeyPatch()
    tmp_path = tmp_path_factory.mktemp("p18_6_flow")
    try:
        return p18_5._build_flow_results(
            monkeypatch,
            tmp_path,
            queue_result,
            p17_7_base_handoff,
        )
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="module")
def retry_authorization():
    return build_retry_incident_rollback_human_authorization(
        action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
        authorizer_id="human.p18.6",
        authorization_reference="P18.6 explicit human retry authorization.",
        rationale="Authorize one bounded retry-state transition without requeue execution.",
        authorized_at="2026-08-09T00:00:00Z",
    )


@pytest.fixture(scope="module")
def rollback_authorization():
    return build_retry_incident_rollback_human_authorization(
        action=RetryIncidentRollbackRequestedAction.AUTHORIZE_ROLLBACK,
        authorizer_id="human.p18.6",
        authorization_reference="P18.6 explicit human rollback authorization.",
        rationale="Authorize rollback-required governance state without Git execution.",
        authorized_at="2026-08-09T00:00:00Z",
    )


@pytest.fixture(scope="module")
def recovery_results(p18_5_flow_results, retry_authorization, rollback_authorization):
    def build(source_key, *, action=None, auth=None, observed=1, maximum=2):
        request = build_canonical_p18_retry_incident_rollback_request(
            P18_5_result=p18_5_flow_results[source_key],
            requested_action=action or RetryIncidentRollbackRequestedAction.NONE,
            human_authorization=auth,
            observed_attempt_count=observed,
            max_attempts=maximum,
        )
        return build_retry_incident_rollback_workflow(request)

    return {
        "validation_failure": build("validation_failure"),
        "diff_blocker": build("diff_blocker"),
        "execution_incident": build("execution_failure"),
        "execution_retry": build(
            "execution_failure",
            action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
            auth=retry_authorization,
        ),
        "execution_retry_exhausted": build(
            "execution_failure",
            action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
            auth=retry_authorization,
            observed=2,
            maximum=2,
        ),
        "execution_rollback": build(
            "execution_failure",
            action=RetryIncidentRollbackRequestedAction.AUTHORIZE_ROLLBACK,
            auth=rollback_authorization,
        ),
        "cancellation": build("cancellation"),
    }


@pytest.fixture(scope="module")
def public_model_instances(recovery_results, retry_authorization):
    incident_record = recovery_results["execution_incident"].incident_record
    assert incident_record is not None
    return {
        RetryIncidentRollbackHumanAuthorization: retry_authorization,
        RetryIncidentRollbackCapabilityReuseAssessment: recovery_results[
            "execution_retry"
        ].capability_reuse_assessments[0],
        RetryIncidentRollbackRequest: recovery_results["execution_retry"].request,
        RetryAttemptPlan: recovery_results["execution_retry"].retry_attempt_plan,
        RetryIncidentRecord: incident_record,
        RollbackGovernancePlan: recovery_results["execution_rollback"].rollback_plan,
        RetryIncidentRollbackFinding: recovery_results["execution_retry"].findings[0],
        RetryIncidentRollbackSummary: recovery_results["execution_retry"].summary,
        RetryIncidentRollbackResult: recovery_results["execution_retry"],
    }


@pytest.mark.parametrize("exported_name", P18_6_EXPORTS)
def test_all_p18_6_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(rir, exported_name)


def test_p18_6_exports_are_additive_suffix() -> None:
    p18_0_count = len(p18_0.P18_0_EXPORTS)
    p18_1_count = len(p18_1.P18_1_EXPORTS)
    p18_2_count = len(p18_2.P18_2_EXPORTS)
    p18_3_count = len(p18_3.P18_3_EXPORTS)
    p18_4_count = len(p18_4.P18_4_EXPORTS)
    p18_5_count = len(p18_5.P18_5_EXPORTS)
    p18_6_start = (
        p18_0_count
        + p18_1_count
        + p18_2_count
        + p18_3_count
        + p18_4_count
        + p18_5_count
    )
    p18_6_end = p18_6_start + len(P18_6_EXPORTS)
    assert tuple(workflow.__all__[:p18_0_count]) == p18_0.P18_0_EXPORTS
    assert tuple(workflow.__all__[p18_6_start:p18_6_end]) == P18_6_EXPORTS
    assert tuple(rir.__all__) == P18_6_EXPORTS
    assert len(workflow.__all__) >= p18_6_end
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_runtime_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert forbidden not in rir.__all__
    assert not hasattr(workflow, forbidden)
    assert not hasattr(rir, forbidden)


def test_schema_policy_and_boundary_constants_are_exact() -> None:
    assert RETRY_INCIDENT_ROLLBACK_SCHEMA_VERSION == 1
    assert (
        RETRY_INCIDENT_ROLLBACK_POLICY_ID
        == "pepper-retry-incident-rollback-workflow-v1"
    )
    assert RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION == "RECOVERY_DECISION_ONLY"


@pytest.mark.parametrize(
    "error_cls",
    (
        RetryIncidentRollbackError,
        RetryIncidentRollbackInputError,
        RetryIncidentRollbackIntegrityError,
        RetryIncidentRollbackPolicyError,
        RetryIncidentRollbackStateError,
        RetryIncidentRollbackValidationError,
    ),
)
def test_public_exceptions_are_value_errors(error_cls: type[Exception]) -> None:
    assert issubclass(error_cls, ValueError)


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_controlled_enums_reject_unknown_values(enum_cls: type[Enum]) -> None:
    with pytest.raises(ValueError):
        enum_cls("__unknown_p18_6_enum__")


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_frozen_and_forbid_extra_fields(
    model_cls: type[BaseModel],
) -> None:
    assert model_cls.model_config["frozen"] is True
    assert model_cls.model_config["extra"] == "forbid"
    assert model_cls.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_round_trip(
    model_cls: type[BaseModel], public_model_instances
) -> None:
    model = public_model_instances[model_cls]
    assert model_cls.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_reject_unknown_fields(
    model_cls: type[BaseModel], public_model_instances
) -> None:
    data = public_model_instances[model_cls].model_dump(mode="json")
    data["unknown"] = "blocked"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


def test_reuse_matrix_classifies_runtime_recovery_boundaries() -> None:
    matrix = build_retry_incident_rollback_reuse_matrix()
    assert len(matrix) == 12
    assert all(row.suitable_for_P18_6 for row in matrix)
    assert not any(row.duplicate_created for row in matrix)
    decisions = {row.symbol: row.decision for row in matrix}
    assert decisions["ReviewValidationP18_6Handoff"] is (
        RetryIncidentRollbackCapabilityDecision.RETAIN
    )
    assert decisions["GovernedWorkflowTransitionResult"] is (
        RetryIncidentRollbackCapabilityDecision.RETAIN
    )
    assert decisions["reclaim_task"] is RetryIncidentRollbackCapabilityDecision.DEFER
    assert decisions["consecutive_failures"] is (
        RetryIncidentRollbackCapabilityDecision.CUSTOMIZE
    )
    assert not any(
        row.invoked_by_P18_6
        for row in matrix
        if row.decision is RetryIncidentRollbackCapabilityDecision.DEFER
    )


def test_canonical_P18_correction_required_flow(recovery_results) -> None:
    result = recovery_results["validation_failure"]
    validate_retry_incident_rollback_request(result.request)
    validate_retry_incident_rollback_result(result)
    assert result.decision is RetryIncidentRollbackDecision.AWAIT_HUMAN_CORRECTION
    assert result.state is RetryIncidentRollbackState.CORRECTION_REQUIRED
    assert result.resulting_workflow_snapshot.current_state is (
        GovernedWorkflowState.AWAITING_CORRECTION
    )
    assert result.workflow_transition_results == ()
    assert result.incident_record is None
    assert result.retry_attempt_plan.retry_requested_by_human is False
    assert result.rollback_plan.rollback_requested_by_human is False
    assert summarize_retry_incident_rollback_workflow(result) == result.summary


def test_diff_blocker_waits_for_human_correction(recovery_results) -> None:
    result = recovery_results["diff_blocker"]
    assert result.decision is RetryIncidentRollbackDecision.AWAIT_HUMAN_CORRECTION
    assert result.state is RetryIncidentRollbackState.CORRECTION_REQUIRED
    assert result.resulting_workflow_snapshot.current_state is (
        GovernedWorkflowState.AWAITING_CORRECTION
    )
    assert result.workflow_transition_results == ()
    assert result.incident_record is None


def test_canonical_P18_incident_flow(recovery_results) -> None:
    result = recovery_results["execution_incident"]
    assert result.decision is RetryIncidentRollbackDecision.RECORD_INCIDENT
    assert result.state is RetryIncidentRollbackState.INCIDENT_RECORDED
    assert (
        result.resulting_workflow_snapshot.current_state is GovernedWorkflowState.FAILED
    )
    assert result.workflow_transition_results == ()
    assert result.incident_record is not None
    assert result.incident_record.incident_open is True
    assert result.incident_record.human_triage_required is True
    assert result.retry_execution_count == 0
    assert result.rollback_execution_count == 0


def test_canonical_P18_retry_eligible_failure_flow(
    recovery_results,
) -> None:
    result = recovery_results["execution_retry"]
    assert result.decision is RetryIncidentRollbackDecision.RETRY_PENDING
    assert result.state is RetryIncidentRollbackState.RETRY_PENDING
    assert result.resulting_workflow_snapshot.current_state is (
        GovernedWorkflowState.RETRY_PENDING
    )
    assert len(result.workflow_transition_results) == 1
    transition = result.workflow_transition_results[0].transition
    assert transition.transition_id == "GWT-023"
    assert transition.automatic is False
    assert result.retry_attempt_plan.next_attempt_number == 2
    assert result.retry_attempt_plan.retry_execution_started is False
    assert result.retry_execution_count == 0
    assert result.automatic_requeue_count == 0
    assert result.Kanban_requeue_calls == 0


def test_canonical_P18_rollback_required_flow(
    recovery_results,
) -> None:
    result = recovery_results["execution_rollback"]
    assert result.decision is RetryIncidentRollbackDecision.ROLLBACK_REQUIRED
    assert result.state is RetryIncidentRollbackState.ROLLBACK_REQUIRED
    assert result.resulting_workflow_snapshot.current_state is (
        GovernedWorkflowState.ROLLBACK_REQUIRED
    )
    assert len(result.workflow_transition_results) == 1
    transition = result.workflow_transition_results[0].transition
    assert transition.transition_id == "GWT-024"
    assert transition.automatic is False
    assert result.rollback_plan.human_git_handoff_required is True
    assert result.rollback_plan.rollback_execution_started is False
    assert result.rollback_plan.Git_rollback_authorized is False
    assert result.rollback_execution_count == 0
    assert result.Git_commands_executed == 0


def test_canonical_P18_retry_max_attempts_flow(recovery_results) -> None:
    result = recovery_results["execution_retry_exhausted"]
    assert (
        result.requested_action is RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY
    )
    assert result.retry_authorized_by_human is True
    assert result.retry_budget_exhausted is True
    assert result.retry_attempt_plan.retry_requested_by_human is True
    assert result.retry_attempt_plan.retry_authorized_for_governed_state is False
    assert result.retry_attempt_plan.next_attempt_number is None
    assert result.decision is RetryIncidentRollbackDecision.RECORD_INCIDENT
    assert (
        result.resulting_workflow_snapshot.current_state is GovernedWorkflowState.FAILED
    )
    assert result.workflow_transition_results == ()


def test_canonical_P18_cancellation_recovery_flow(recovery_results) -> None:
    result = recovery_results["cancellation"]
    assert result.decision is RetryIncidentRollbackDecision.CANCELLED
    assert result.state is RetryIncidentRollbackState.CANCELLED
    assert (
        result.resulting_workflow_snapshot.current_state
        is GovernedWorkflowState.CANCELLED
    )
    assert result.workflow_transition_results == ()
    assert result.incident_record is None
    assert result.retry_attempt_plan.retry_requested_by_human is False
    assert result.rollback_plan.rollback_required_for_governed_state is False


def test_accepted_p18_5_result_is_rejected(p18_5_flow_results) -> None:
    _assert_p18_6_fails(
        lambda: build_canonical_p18_retry_incident_rollback_request(
            P18_5_result=p18_5_flow_results["accepted"]
        )
    )


def test_retry_authorization_requires_incident_source(
    p18_5_flow_results, retry_authorization
) -> None:
    _assert_p18_6_fails(
        lambda: build_canonical_p18_retry_incident_rollback_request(
            P18_5_result=p18_5_flow_results["validation_failure"],
            requested_action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
            human_authorization=retry_authorization,
        )
    )


def test_recovery_action_requires_human_authorization(p18_5_flow_results) -> None:
    _assert_p18_6_fails(
        lambda: build_canonical_p18_retry_incident_rollback_request(
            P18_5_result=p18_5_flow_results["execution_failure"],
            requested_action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
        )
    )


def test_human_authorization_action_must_match_request(
    p18_5_flow_results, rollback_authorization
) -> None:
    _assert_p18_6_fails(
        lambda: build_canonical_p18_retry_incident_rollback_request(
            P18_5_result=p18_5_flow_results["execution_failure"],
            requested_action=RetryIncidentRollbackRequestedAction.AUTHORIZE_RETRY,
            human_authorization=rollback_authorization,
        )
    )


def test_replay_policy_blocks_prior_recovery_result(p18_5_flow_results) -> None:
    _assert_p18_6_fails(
        lambda: build_canonical_p18_retry_incident_rollback_request(
            P18_5_result=p18_5_flow_results["execution_failure"],
            prior_recovery_result_SHA256="a" * 64,
        )
    )


def test_request_rejects_stale_p18_5_digest(recovery_results) -> None:
    request = recovery_results["execution_incident"].request
    tampered = _construct_with_updates(request, P18_5_result_SHA256="a" * 64)
    _assert_p18_6_fails(lambda: validate_retry_incident_rollback_request(tampered))


def test_request_rejects_mismatched_handoff_object(recovery_results) -> None:
    request = recovery_results["validation_failure"].request
    other_handoff = recovery_results["cancellation"].request.P18_6_handoff
    tampered = _construct_with_updates(request, P18_6_handoff=other_handoff)
    _assert_p18_6_fails(lambda: validate_retry_incident_rollback_request(tampered))


def test_result_rejects_counter_tamper(recovery_results) -> None:
    result = recovery_results["execution_retry"]
    tampered = _construct_with_updates(result, Git_commands_executed=1)
    _assert_p18_6_fails(lambda: validate_retry_incident_rollback_result(tampered))


@pytest.mark.parametrize("flow_key", FLOW_KEYS)
def test_result_and_summary_serialization_are_stable(
    recovery_results, flow_key: str
) -> None:
    result = recovery_results[flow_key]
    assert (
        RetryIncidentRollbackResult.model_validate_json(result.model_dump_json())
        == result
    )
    assert (
        RetryIncidentRollbackSummary.model_validate_json(
            result.summary.model_dump_json()
        )
        == result.summary
    )


@pytest.mark.parametrize("flow_key", FLOW_KEYS)
def test_rebuilding_same_request_is_deterministic(
    recovery_results, flow_key: str
) -> None:
    result = recovery_results[flow_key]
    rebuilt = build_retry_incident_rollback_workflow(result.request)
    assert rebuilt == result
    assert rebuilt.result_SHA256 == result.result_SHA256


@pytest.mark.parametrize("flow_key", FLOW_KEYS)
@pytest.mark.parametrize("field", ZERO_COUNT_FIELDS)
def test_all_flows_keep_runtime_authority_counters_zero(
    recovery_results,
    flow_key: str,
    field: str,
) -> None:
    assert getattr(recovery_results[flow_key], field) == 0


@pytest.mark.parametrize("flow_key", FLOW_KEYS)
@pytest.mark.parametrize("field", FALSE_AUTHORITY_FIELDS)
def test_all_flows_keep_authority_flags_false(
    recovery_results,
    flow_key: str,
    field: str,
) -> None:
    assert getattr(recovery_results[flow_key], field) is False


@pytest.mark.parametrize("field", DUPLICATE_FIELDS[:-1])
def test_p18_6_creates_no_duplicate_recovery_runtime(
    recovery_results, field: str
) -> None:
    assert getattr(recovery_results["execution_retry"], field) is False


def test_canonical_P18_recovery_never_executes_git_or_retry(recovery_results) -> None:
    for flow_key in FLOW_KEYS:
        result = recovery_results[flow_key]
        assert result.retry_execution_count == 0
        assert result.rollback_execution_count == 0
        assert result.Git_commands_executed == 0
        assert result.Git_staging_performed is False
        assert result.Git_commit_performed is False
        assert result.Git_push_performed is False
        assert result.Kanban_requeue_calls == 0
        assert result.Kanban_reclaim_calls == 0
        assert result.Kanban_reassign_calls == 0
        assert result.workspace_restore_calls_in_P18_6 == 0
    for duplicate_field in DUPLICATE_FIELDS:
        assert getattr(recovery_results["execution_retry"], duplicate_field) is False


@pytest.mark.parametrize("flow_key", FLOW_KEYS)
def test_project_ticket_and_work_packet_identity_preserved(
    recovery_results,
    flow_key: str,
) -> None:
    result = recovery_results[flow_key]
    request = result.request
    assert result.project_id == "PEPPER"
    assert result.macroproject_id == "P18"
    assert result.ticket_id == "P18.2"
    assert result.WorkPacket_ID == request.P18_5_result.WorkPacket_ID
    assert result.WorkPacket_SHA256 == request.P18_5_result.WorkPacket_SHA256
    assert result.P18_5_result_SHA256 == request.P18_5_result.result_SHA256
    assert result.P18_6_handoff_SHA256 == request.P18_6_handoff.handoff_SHA256


@pytest.mark.parametrize("flow_key", FLOW_KEYS)
def test_summary_records_decision_only_boundary(
    recovery_results, flow_key: str
) -> None:
    summary = recovery_results[flow_key].summary
    assert summary.P18_5_handoff_valid is True
    assert summary.source_non_accept_valid is True
    assert summary.recovery_decision_valid is True
    assert summary.retry_attempt_tracking_valid is True
    assert summary.Kanban_runtime_mutation_deferred is True
    assert summary.task_requeue_reclaim_deferred is True
    assert summary.workspace_restoration_deferred is True
    assert summary.no_autonomous_retry_valid is True
    assert summary.no_autonomous_rollback_valid is True
    assert summary.no_runtime_mutation_valid is True


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
