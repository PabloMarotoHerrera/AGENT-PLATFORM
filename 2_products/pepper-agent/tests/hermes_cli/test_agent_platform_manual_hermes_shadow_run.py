from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.manual_hermes_shadow_run as shadow
from hermes_cli.agent_platform.workflow import (
    MANUAL_HERMES_SHADOW_RUN_POLICY_ID,
    MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION,
    ManualHermesShadowRunComparisonScore,
    ManualHermesShadowRunDecision,
    ManualHermesShadowRunDependencyPosture,
    ManualHermesShadowRunError,
    ManualHermesShadowRunGapCategory,
    ManualHermesShadowRunGapSeverity,
    ManualHermesShadowRunHumanSmokeStatus,
    ManualHermesShadowRunInputError,
    ManualHermesShadowRunIntegrityError,
    ManualHermesShadowRunPolicyError,
    ManualHermesShadowRunReadinessDecision,
    ManualHermesShadowRunRequest,
    ManualHermesShadowRunResult,
    ManualHermesShadowRunStage,
    ManualHermesShadowRunStateError,
    ManualHermesShadowRunSummary,
    ManualHermesShadowRunUIClassification,
    ManualHermesShadowRunValidationError,
    ManualWorkflowAuthorityEntry,
    ManualWorkflowBaseline,
    PepperWorkflowEvidence,
    ShadowComparisonDimension,
    ShadowContextPersistenceAudit,
    ShadowDependencyAudit,
    ShadowGitHandoffComparison,
    ShadowMigrationGap,
    ShadowOpenCodeDependencyAudit,
    ShadowOperatorEffort,
    ShadowTicketSelection,
    ShadowUIEndpointEvidence,
    ShadowUIReadinessEvidence,
    ShadowWorkspaceIsolation,
    build_canonical_p18_manual_hermes_shadow_run_request,
    build_manual_hermes_shadow_authority_map,
    build_manual_hermes_shadow_comparison_dimensions,
    build_manual_hermes_shadow_run,
    build_manual_hermes_shadow_ui_endpoints,
    summarize_manual_hermes_shadow_run,
    validate_manual_hermes_shadow_run_request,
    validate_manual_hermes_shadow_run_result,
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
    test_agent_platform_retry_incident_rollback as p18_6,
)
from tests.hermes_cli import (
    test_agent_platform_review_validation_loop as p18_5,
)
from tests.hermes_cli import (
    test_agent_platform_ticket_factory_runtime_integration as p18_2,
)


P18_6_COMMIT = "4658fd1576e546fc3029a6125e41186c7e5cbe26"
P18_6_RESULT_SHA256 = "54ca05cf9bfdb99047b94954a57571ce94c9afeb4fbc5ac7600a73d5b3000b2c"

P18_7_EXPORTS = (
    "MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION",
    "MANUAL_HERMES_SHADOW_RUN_POLICY_ID",
    "ManualHermesShadowRunDecision",
    "ManualHermesShadowRunComparisonScore",
    "ManualHermesShadowRunGapCategory",
    "ManualHermesShadowRunGapSeverity",
    "ManualHermesShadowRunDependencyPosture",
    "ManualHermesShadowRunUIClassification",
    "ManualHermesShadowRunHumanSmokeStatus",
    "ManualHermesShadowRunReadinessDecision",
    "ManualHermesShadowRunStage",
    "ShadowTicketSelection",
    "ManualWorkflowBaseline",
    "ManualWorkflowAuthorityEntry",
    "PepperWorkflowEvidence",
    "ShadowWorkspaceIsolation",
    "ShadowComparisonDimension",
    "ShadowUIEndpointEvidence",
    "ShadowUIReadinessEvidence",
    "ShadowDependencyAudit",
    "ShadowOpenCodeDependencyAudit",
    "ShadowContextPersistenceAudit",
    "ShadowMigrationGap",
    "ShadowOperatorEffort",
    "ShadowGitHandoffComparison",
    "ManualHermesShadowRunRequest",
    "ManualHermesShadowRunSummary",
    "ManualHermesShadowRunResult",
    "ManualHermesShadowRunError",
    "ManualHermesShadowRunInputError",
    "ManualHermesShadowRunIntegrityError",
    "ManualHermesShadowRunPolicyError",
    "ManualHermesShadowRunStateError",
    "ManualHermesShadowRunValidationError",
    "build_manual_hermes_shadow_authority_map",
    "build_manual_hermes_shadow_comparison_dimensions",
    "build_manual_hermes_shadow_ui_endpoints",
    "build_canonical_p18_manual_hermes_shadow_run_request",
    "validate_manual_hermes_shadow_run_request",
    "build_manual_hermes_shadow_run",
    "validate_manual_hermes_shadow_run_result",
    "summarize_manual_hermes_shadow_run",
)

PUBLIC_MODELS = (
    ShadowTicketSelection,
    ManualWorkflowBaseline,
    ManualWorkflowAuthorityEntry,
    PepperWorkflowEvidence,
    ShadowWorkspaceIsolation,
    ShadowComparisonDimension,
    ShadowUIEndpointEvidence,
    ShadowUIReadinessEvidence,
    ShadowDependencyAudit,
    ShadowOpenCodeDependencyAudit,
    ShadowContextPersistenceAudit,
    ShadowMigrationGap,
    ShadowOperatorEffort,
    ShadowGitHandoffComparison,
    ManualHermesShadowRunRequest,
    ManualHermesShadowRunSummary,
    ManualHermesShadowRunResult,
)
PUBLIC_MODEL_FIELD_CASES = tuple(
    (model_type, field_name)
    for model_type in PUBLIC_MODELS
    for field_name in model_type.model_fields
)
CONTROLLED_ENUMS = (
    ManualHermesShadowRunDecision,
    ManualHermesShadowRunComparisonScore,
    ManualHermesShadowRunGapCategory,
    ManualHermesShadowRunGapSeverity,
    ManualHermesShadowRunDependencyPosture,
    ManualHermesShadowRunUIClassification,
    ManualHermesShadowRunHumanSmokeStatus,
    ManualHermesShadowRunReadinessDecision,
    ManualHermesShadowRunStage,
)
FORBIDDEN_PUBLIC_EXPORTS = (
    "MANUAL_HERMES_SHADOW_RUN_VERDICT",
    "auto_cutover",
    "force_default_mode",
    "bypass_manual_approval",
    "auto_commit_shadow",
    "auto_push_shadow",
    "skip_shadow_comparison",
    "ShadowExecutor",
    "run_OpenCode_worker",
    "invoke_provider",
    "run_git_command",
)
ZERO_COUNT_FIELDS = (
    "provider_dispatch_count",
    "model_inference_count",
    "subprocess_calls",
    "shell_calls",
    "filesystem_calls",
    "Git_calls",
    "network_calls",
    "Docker_calls",
    "Graphify_calls",
    "database_calls",
    "direct_Kanban_mutation_calls",
    "direct_dispatcher_calls",
    "direct_worker_calls",
    "direct_validation_runner_calls",
    "direct_review_engine_calls",
    "direct_recovery_engine_calls",
    "staging_calls",
    "commit_calls",
    "push_calls",
)
FALSE_AUTHORITY_FIELDS = (
    "automatic_git_add",
    "automatic_git_commit",
    "automatic_git_push",
    "duplicate_Project_Intake_created",
    "duplicate_Ticket_Factory_created",
    "duplicate_approval_engine_created",
    "duplicate_dependency_queue_created",
    "duplicate_executor_created",
    "duplicate_validation_runner_created",
    "duplicate_review_engine_created",
    "duplicate_recovery_engine_created",
    "duplicate_Git_handoff_created",
)
REQUIRED_DIMENSIONS = tuple(ManualHermesShadowRunStage)
UNSAFE_TEXTS = (
    "contains access_token marker",
    "contains bearer credential marker",
    "contains private key marker",
    "contains raw prompt marker",
    "contains reasoning trace marker",
    "contains raw stdout marker",
    "contains model output marker",
    "contains ChatGPT transcript marker",
    "contains C:/Users/example path",
    "contains /home/example path",
)


def _construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def _assert_p18_7_fails(callback) -> None:
    with pytest.raises((ValidationError, ValueError, ManualHermesShadowRunError)):
        callback()


@pytest.fixture(scope="module")
def blocked_request() -> ManualHermesShadowRunRequest:
    return build_canonical_p18_manual_hermes_shadow_run_request(
        P18_6_commit=P18_6_COMMIT,
        P18_6_result_SHA256=P18_6_RESULT_SHA256,
        common_parent_commit=P18_6_COMMIT,
    )


@pytest.fixture(scope="module")
def blocked_result(blocked_request) -> ManualHermesShadowRunResult:
    return build_manual_hermes_shadow_run(blocked_request)


@pytest.fixture(scope="module")
def ready_request() -> ManualHermesShadowRunRequest:
    return build_canonical_p18_manual_hermes_shadow_run_request(
        P18_6_commit=P18_6_COMMIT,
        P18_6_result_SHA256=P18_6_RESULT_SHA256,
        common_parent_commit=P18_6_COMMIT,
        UI_blocked=False,
        chat_required=False,
        opencode_copy_required=False,
    )


@pytest.fixture(scope="module")
def ready_result(ready_request) -> ManualHermesShadowRunResult:
    return build_manual_hermes_shadow_run(ready_request)


@pytest.fixture(scope="module")
def public_model_instances(blocked_result):
    request = blocked_result.request
    return {
        ShadowTicketSelection: request.shadow_ticket,
        ManualWorkflowBaseline: request.manual_baseline,
        ManualWorkflowAuthorityEntry: request.manual_authority_map[0],
        PepperWorkflowEvidence: request.Pepper_evidence,
        ShadowWorkspaceIsolation: request.workspace_isolation,
        ShadowComparisonDimension: request.comparisons[0],
        ShadowUIEndpointEvidence: request.UI_readiness.endpoints[0],
        ShadowUIReadinessEvidence: request.UI_readiness,
        ShadowDependencyAudit: request.chat_dependency_audit,
        ShadowOpenCodeDependencyAudit: request.OpenCode_dependency_audit,
        ShadowContextPersistenceAudit: request.context_persistence_audit,
        ShadowMigrationGap: request.migration_gaps[0],
        ShadowOperatorEffort: request.operator_effort,
        ShadowGitHandoffComparison: request.Git_handoff_comparison,
        ManualHermesShadowRunRequest: request,
        ManualHermesShadowRunSummary: blocked_result.summary,
        ManualHermesShadowRunResult: blocked_result,
    }


@pytest.mark.parametrize("exported_name", P18_7_EXPORTS)
def test_all_p18_7_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(shadow, exported_name)


def test_p18_7_exports_are_additive_suffix() -> None:
    p18_7_start = (
        len(p18_0.P18_0_EXPORTS)
        + len(p18_1.P18_1_EXPORTS)
        + len(p18_2.P18_2_EXPORTS)
        + len(p18_3.P18_3_EXPORTS)
        + len(p18_4.P18_4_EXPORTS)
        + len(p18_5.P18_5_EXPORTS)
        + len(p18_6.P18_6_EXPORTS)
    )
    p18_7_end = p18_7_start + len(P18_7_EXPORTS)
    assert p18_7_start == 207
    assert tuple(workflow.__all__[: len(p18_0.P18_0_EXPORTS)]) == p18_0.P18_0_EXPORTS
    assert tuple(workflow.__all__[p18_7_start:p18_7_end]) == P18_7_EXPORTS
    assert tuple(shadow.__all__) == P18_7_EXPORTS
    assert len(workflow.__all__) >= p18_7_end
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize("forbidden", FORBIDDEN_PUBLIC_EXPORTS)
def test_forbidden_cutover_or_runtime_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert forbidden not in shadow.__all__
    assert not hasattr(workflow, forbidden)
    assert not hasattr(shadow, forbidden)


def test_schema_and_policy_constants_are_exact() -> None:
    assert MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION == 1
    assert MANUAL_HERMES_SHADOW_RUN_POLICY_ID == "pepper-manual-hermes-shadow-run-v1"


@pytest.mark.parametrize(
    "error_cls",
    (
        ManualHermesShadowRunError,
        ManualHermesShadowRunInputError,
        ManualHermesShadowRunIntegrityError,
        ManualHermesShadowRunPolicyError,
        ManualHermesShadowRunStateError,
        ManualHermesShadowRunValidationError,
    ),
)
def test_public_exceptions_are_value_errors(error_cls: type[Exception]) -> None:
    assert issubclass(error_cls, ValueError)


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_controlled_enums_reject_unknown_values(enum_cls: type[Enum]) -> None:
    with pytest.raises(ValueError):
        enum_cls("__unknown_p18_7_enum__")


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


def test_canonical_P18_shadow_semantically_equivalent_flow(blocked_result) -> None:
    validate_manual_hermes_shadow_run_result(blocked_result)
    assert blocked_result.summary.semantic_shadow_equivalence is True
    assert blocked_result.summary.governance_equivalence is True
    assert blocked_result.shadow_ticket_id == "P18.UI-A-SHADOW-ROUTE-SMOKE"
    assert blocked_result.request.shadow_ticket.destructive_side_effects is False
    assert (
        blocked_result.request.manual_baseline.raw_conversation_history_persisted
        is False
    )
    assert (
        blocked_result.request.manual_baseline.raw_OpenCode_transcript_persisted
        is False
    )
    assert summarize_manual_hermes_shadow_run(blocked_result) == blocked_result.summary


def test_canonical_P18_shadow_detects_approval_UI_blocker(blocked_result) -> None:
    assert blocked_result.summary.Approvals_operational is False
    assert blocked_result.request.UI_readiness.approval_list_live is False
    assert (
        blocked_result.request.UI_readiness.approval_action_available_from_UI is False
    )
    assert any(
        gap.gap_id == "P18-8-GAP-001"
        and gap.category is ManualHermesShadowRunGapCategory.UI_BACKEND_GAP
        and gap.blocks_cutover
        for gap in blocked_result.request.migration_gaps
    )


def test_canonical_P18_shadow_detects_execution_UI_blocker(blocked_result) -> None:
    assert blocked_result.summary.Executions_operational is False
    assert blocked_result.request.UI_readiness.execution_list_live is False
    assert blocked_result.request.UI_readiness.execution_state_visible is False
    assert any(
        gap.gap_id == "P18-8-GAP-002"
        and gap.category is ManualHermesShadowRunGapCategory.EXECUTOR_INTEGRATION_GAP
        and gap.blocks_cutover
        for gap in blocked_result.request.migration_gaps
    )


def test_canonical_P18_shadow_detects_manual_chat_dependency(blocked_result) -> None:
    audit = blocked_result.request.chat_dependency_audit
    assert audit.normal_workflow_requires_this_chat is True
    assert audit.roadmap_state is ManualHermesShadowRunDependencyPosture.REQUIRED
    assert blocked_result.summary.normal_workflow_requires_chat is True
    assert any(
        gap.gap_id == "P18-8-GAP-003" and gap.blocks_cutover
        for gap in blocked_result.request.migration_gaps
    )


def test_canonical_P18_shadow_rejects_authority_regression() -> None:
    _assert_p18_7_fails(
        lambda: build_canonical_p18_manual_hermes_shadow_run_request(
            P18_6_commit=P18_6_COMMIT,
            P18_6_result_SHA256=P18_6_RESULT_SHA256,
            common_parent_commit=P18_6_COMMIT,
            authority_regression=True,
        )
    )


def test_canonical_P18_shadow_preserves_human_Git_authority(blocked_result) -> None:
    handoff = blocked_result.request.Git_handoff_comparison
    assert handoff.Git_handoff_eligible is True
    assert handoff.human_only_execution_preserved is True
    assert handoff.automatic_git_add is False
    assert handoff.automatic_git_commit is False
    assert handoff.automatic_git_push is False
    assert blocked_result.automatic_git_add is False
    assert blocked_result.automatic_git_commit is False
    assert blocked_result.automatic_git_push is False


def test_canonical_P18_shadow_computes_P18_8_readiness(
    blocked_result, ready_result
) -> None:
    assert (
        blocked_result.P18_8_ready
        is ManualHermesShadowRunReadinessDecision.P18_8_BLOCKED
    )
    assert blocked_result.decision is (
        ManualHermesShadowRunDecision.SHADOW_VALIDATED_WITH_CUTOVER_BLOCKERS
    )
    assert (
        ready_result.P18_8_ready is ManualHermesShadowRunReadinessDecision.P18_8_READY
    )
    assert ready_result.decision is ManualHermesShadowRunDecision.SHADOW_VALIDATED
    assert ready_result.summary.cutover_blocking_gap_count == 0


def test_ready_flow_has_operational_ui_and_no_copy_paste(ready_result) -> None:
    summary = ready_result.summary
    assert summary.UI_operational is True
    assert summary.Projects_operational is True
    assert summary.Tickets_operational is True
    assert summary.Approvals_operational is True
    assert summary.Executions_operational is True
    assert summary.review_visibility_operational is True
    assert summary.next_action_visible is True
    assert summary.normal_workflow_requires_chat is False
    assert summary.manual_OpenCode_ticket_copy_required is False
    assert summary.manual_OpenCode_result_copy_required is False
    assert ready_result.request.UI_readiness.human_ui_smoke is (
        ManualHermesShadowRunHumanSmokeStatus.HUMAN_UI_SMOKE_PASS
    )


def test_blocked_flow_records_explicit_gap_taxonomy(blocked_result) -> None:
    gaps = blocked_result.request.migration_gaps
    assert len(gaps) == 4
    assert blocked_result.summary.cutover_blocking_gap_count == 4
    assert {gap.category for gap in gaps} == {
        ManualHermesShadowRunGapCategory.UI_BACKEND_GAP,
        ManualHermesShadowRunGapCategory.EXECUTOR_INTEGRATION_GAP,
        ManualHermesShadowRunGapCategory.CONTEXT_GAP,
        ManualHermesShadowRunGapCategory.HUMAN_ACTION_GAP,
    }
    assert all(gap.severity is ManualHermesShadowRunGapSeverity.BLOCKER for gap in gaps)


def test_ticket_text_is_equivalent_but_not_prose_identical(blocked_result) -> None:
    ticket_dimension = next(
        item
        for item in blocked_result.request.comparisons
        if item.dimension is ManualHermesShadowRunStage.TICKET_SEMANTICS
    )
    assert ticket_dimension.score is ManualHermesShadowRunComparisonScore.EQUIVALENT
    assert "semantically" in ticket_dimension.rationale
    assert blocked_result.request.manual_baseline.manual_ticket_artifact_SHA256 != (
        blocked_result.request.shadow_ticket.ticket_SHA256
    )


def test_dependency_queue_shadow_evidence_is_admitted(blocked_result) -> None:
    progression = blocked_result.request.Pepper_evidence.workflow_state_progression
    assert "work_packet_ready" in progression
    assert blocked_result.request.Pepper_evidence.P18_4_queue_result_SHA256
    assert blocked_result.request.Pepper_evidence.compilation_count == 1


def test_provider_and_model_counts_are_zero(blocked_result) -> None:
    pepper = blocked_result.request.Pepper_evidence
    assert pepper.provider_model_required is False
    assert pepper.provider_dispatch_count == 0
    assert pepper.model_inference_count == 0
    assert blocked_result.provider_dispatch_count == 0
    assert blocked_result.model_inference_count == 0


def test_chat_dependency_audit_derives_required_flag(
    blocked_result, ready_result
) -> None:
    assert (
        blocked_result.request.chat_dependency_audit.normal_workflow_requires_this_chat
    )
    assert not ready_result.request.chat_dependency_audit.normal_workflow_requires_this_chat


def test_OpenCode_dependency_audit_derives_copy_flags(
    blocked_result, ready_result
) -> None:
    assert blocked_result.request.OpenCode_dependency_audit.manual_OpenCode_ticket_paste
    assert blocked_result.request.OpenCode_dependency_audit.manual_OpenCode_result_copy
    assert (
        not ready_result.request.OpenCode_dependency_audit.manual_OpenCode_ticket_paste
    )
    assert (
        not ready_result.request.OpenCode_dependency_audit.manual_OpenCode_result_copy
    )


def test_context_persistence_gap_is_distinct_from_GBrain(blocked_result) -> None:
    audit = blocked_result.request.context_persistence_audit
    assert audit.GBrain_required_for_P18_8 is False
    assert audit.Paperclip_required_for_P18_8 is False
    assert audit.P18_8_context_blocker is True
    assert "project identity" in audit.minimum_project_context_persisted


def test_ui_endpoint_contracts_are_bounded(blocked_result) -> None:
    endpoints = {
        endpoint.route: endpoint
        for endpoint in blocked_result.request.UI_readiness.endpoints
    }
    assert endpoints["/agent-platform/projects"].classification is (
        ManualHermesShadowRunUIClassification.FUNCTIONAL_READ_ONLY_PROJECTION
    )
    assert endpoints["/agent-platform/approvals"].classification is (
        ManualHermesShadowRunUIClassification.UNAVAILABLE_BACKEND
    )
    assert all(endpoint.sensitive_fields_absent for endpoint in endpoints.values())


def test_manual_authority_map_covers_required_actions() -> None:
    actions = {entry.action for entry in build_manual_hermes_shadow_authority_map()}
    assert {
        "project selection",
        "ticket generation",
        "ticket approval",
        "execution authorization",
        "execution",
        "validation",
        "review",
        "retry decision",
        "rollback decision",
        "Git staging",
        "Git commit",
        "Git push",
        "next-ticket selection",
    } <= actions


def test_request_rejects_stale_p18_6_commit(blocked_request) -> None:
    tampered = _construct_with_updates(blocked_request, P18_6_commit="0" * 40)
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_request(tampered))


def test_request_rejects_stale_p18_6_result_digest(blocked_request) -> None:
    tampered = _construct_with_updates(blocked_request, P18_6_result_SHA256="b" * 64)
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_request(tampered))


def test_request_rejects_wrong_shadow_ticket(blocked_request) -> None:
    pepper = _construct_with_updates(
        blocked_request.Pepper_evidence,
        selected_shadow_ticket_id="OTHER-SHADOW-TICKET",
    )
    tampered = _construct_with_updates(blocked_request, Pepper_evidence=pepper)
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_request(tampered))


def test_request_rejects_wrong_project(blocked_request) -> None:
    tampered = _construct_with_updates(blocked_request, project_id="OTHER")
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_request(tampered))


def test_pepper_evidence_rejects_wrong_WorkPacket(blocked_request) -> None:
    pepper = _construct_with_updates(
        blocked_request.Pepper_evidence, WorkPacket_ID="BAD"
    )
    _assert_p18_7_fails(lambda: PepperWorkflowEvidence.model_validate(pepper))


def test_result_rejects_wrong_parent_commit(blocked_result) -> None:
    tampered = _construct_with_updates(blocked_result, common_parent_commit="0" * 40)
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_result(tampered))


def test_result_rejects_runtime_counter_tamper(blocked_result) -> None:
    tampered = _construct_with_updates(blocked_result, Git_calls=1)
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_result(tampered))


def test_result_rejects_digest_tamper(blocked_result) -> None:
    tampered = _construct_with_updates(blocked_result, result_SHA256="b" * 64)
    _assert_p18_7_fails(lambda: validate_manual_hermes_shadow_run_result(tampered))


def test_rebuilding_same_request_is_deterministic(
    blocked_request, blocked_result
) -> None:
    rebuilt = build_manual_hermes_shadow_run(blocked_request)
    assert rebuilt == blocked_result
    assert rebuilt.result_SHA256 == blocked_result.result_SHA256


def test_serialization_stability(blocked_result) -> None:
    assert (
        ManualHermesShadowRunResult.model_validate_json(
            blocked_result.model_dump_json()
        )
        == blocked_result
    )
    assert (
        ManualHermesShadowRunSummary.model_validate_json(
            blocked_result.summary.model_dump_json()
        )
        == blocked_result.summary
    )


@pytest.mark.parametrize("dimension", REQUIRED_DIMENSIONS)
def test_comparison_dimensions_are_complete(blocked_result, dimension) -> None:
    comparisons = {item.dimension: item for item in blocked_result.request.comparisons}
    assert dimension in comparisons
    assert comparisons[dimension].comparison_SHA256


@pytest.mark.parametrize("endpoint", build_manual_hermes_shadow_ui_endpoints())
def test_endpoint_evidence_round_trips(endpoint) -> None:
    assert (
        ShadowUIEndpointEvidence.model_validate_json(endpoint.model_dump_json())
        == endpoint
    )


@pytest.mark.parametrize("unsafe_text", UNSAFE_TEXTS)
def test_shadow_ticket_rejects_unsafe_text(blocked_request, unsafe_text: str) -> None:
    ticket = _construct_with_updates(
        blocked_request.shadow_ticket,
        why_selected=unsafe_text,
    )
    _assert_p18_7_fails(lambda: ShadowTicketSelection.model_validate(ticket))


@pytest.mark.parametrize("unsafe_text", UNSAFE_TEXTS)
def test_manual_baseline_rejects_unsafe_text(blocked_request, unsafe_text: str) -> None:
    baseline = _construct_with_updates(
        blocked_request.manual_baseline,
        manual_review_method=unsafe_text,
    )
    _assert_p18_7_fails(lambda: ManualWorkflowBaseline.model_validate(baseline))


@pytest.mark.parametrize("unsafe_text", UNSAFE_TEXTS)
def test_gap_rejects_unsafe_text(blocked_request, unsafe_text: str) -> None:
    gap = _construct_with_updates(
        blocked_request.migration_gaps[0],
        evidence=unsafe_text,
    )
    _assert_p18_7_fails(lambda: ShadowMigrationGap.model_validate(gap))


@pytest.mark.parametrize("field", ZERO_COUNT_FIELDS)
def test_result_keeps_runtime_authority_counters_zero(
    blocked_result, field: str
) -> None:
    assert getattr(blocked_result, field) == 0


@pytest.mark.parametrize("field", FALSE_AUTHORITY_FIELDS)
def test_result_keeps_authority_and_duplicate_flags_false(
    blocked_result, field: str
) -> None:
    assert getattr(blocked_result, field) is False


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
