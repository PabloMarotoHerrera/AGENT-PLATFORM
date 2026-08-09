from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.workflow as workflow
import hermes_cli.agent_platform.workflow.governed_state_machine as gsm
from hermes_cli.agent_platform.workflow import (
    GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
    GovernedWorkflowIdentity,
    GovernedWorkflowSnapshot,
    GovernedWorkflowState,
    GovernedWorkflowStateDefinition,
    GovernedWorkflowStateMachineError,
    GovernedWorkflowStateMachinePolicyError,
    GovernedWorkflowStateMachineResult,
    GovernedWorkflowStateMachineStateError,
    GovernedWorkflowStateMachineValidationError,
    GovernedWorkflowTransition,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowProjection,
    HermesWorkflowRuntimeKind,
    P17WorkflowBinding,
    WorkflowReuseSummary,
    WorkflowRuntimeMappingKind,
    WorkflowRuntimeStateMapping,
    WorkflowStateMachineFinding,
    WorkflowStateMachineFindingCode,
    WorkflowStateMachineFindingSeverity,
    WorkflowStateOwner,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_governed_workflow_identity,
    build_governed_workflow_state_machine_result,
    build_governed_workflow_transition,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    build_p17_workflow_binding,
    build_workflow_runtime_state_mappings,
    validate_governed_workflow_snapshot,
    validate_governed_workflow_transition_request,
    validate_hermes_workflow_projection,
)
from hermes_cli.agent_platform.work_packet import (
    build_canonical_p17_closure_request,
    build_p17_work_packet_execution_mvp_closure,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_non_critical_ticket_pilot as p17_8,
)


P18_0_EXPORTS = (
    "GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION",
    "GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID",
    "GovernedWorkflowState",
    "WorkflowStateOwner",
    "WorkflowTransitionTrigger",
    "WorkflowTransitionAuthority",
    "HermesWorkflowRuntimeKind",
    "WorkflowRuntimeMappingKind",
    "WorkflowStateMachineFindingSeverity",
    "WorkflowStateMachineFindingCode",
    "GovernedWorkflowStateDefinition",
    "GovernedWorkflowTransition",
    "GovernedWorkflowIdentity",
    "GovernedWorkflowSnapshot",
    "HermesWorkflowProjection",
    "WorkflowRuntimeStateMapping",
    "GovernedWorkflowTransitionRequest",
    "GovernedWorkflowTransitionResult",
    "P17WorkflowBinding",
    "WorkflowStateMachineFinding",
    "WorkflowReuseSummary",
    "GovernedWorkflowStateMachineResult",
    "GovernedWorkflowStateMachineError",
    "GovernedWorkflowStateMachineInputError",
    "GovernedWorkflowStateMachineIntegrityError",
    "GovernedWorkflowStateMachinePolicyError",
    "GovernedWorkflowStateMachineStateError",
    "GovernedWorkflowStateMachineValidationError",
    "build_governed_workflow_identity",
    "build_hermes_workflow_projection",
    "build_p17_workflow_binding",
    "build_initial_governed_workflow_snapshot",
    "build_workflow_runtime_state_mappings",
    "validate_hermes_workflow_projection",
    "validate_governed_workflow_snapshot",
    "validate_governed_workflow_transition_request",
    "build_governed_workflow_transition",
    "build_governed_workflow_state_machine_result",
)

PUBLIC_MODELS = (
    GovernedWorkflowStateDefinition,
    GovernedWorkflowTransition,
    GovernedWorkflowIdentity,
    GovernedWorkflowSnapshot,
    HermesWorkflowProjection,
    WorkflowRuntimeStateMapping,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    P17WorkflowBinding,
    WorkflowStateMachineFinding,
    WorkflowReuseSummary,
    GovernedWorkflowStateMachineResult,
)

EXPECTED_STATES = (
    "draft",
    "intake_ready",
    "awaiting_ticket_approval",
    "ticket_approved",
    "work_packet_ready",
    "queued",
    "blocked",
    "allocating",
    "ready_to_execute",
    "executing",
    "validating",
    "reviewing",
    "awaiting_correction",
    "awaiting_human_approval",
    "awaiting_human_git_handoff",
    "completed",
    "failed",
    "cancelled",
    "incident",
    "retry_pending",
    "rollback_required",
)

EXPECTED_TRIGGERS = (
    "project_intake_completed",
    "ticket_generated",
    "ticket_approved",
    "work_packet_compiled",
    "dependencies_ready",
    "dependencies_blocked",
    "workspace_allocated",
    "execution_started",
    "execution_completed",
    "execution_failed",
    "validation_started",
    "validation_completed",
    "validation_failed",
    "review_started",
    "review_accepted",
    "review_rejected",
    "correction_required",
    "human_approved",
    "human_rejected",
    "git_handoff_ready",
    "human_git_completed",
    "cancel_requested",
    "incident_detected",
    "retry_authorized",
    "rollback_authorized",
)

EXPECTED_FINDING_CODES = (
    "hermes_capability_reused",
    "hermes_capability_customized",
    "hermes_capability_replacement_required",
    "hermes_capability_gap",
    "duplicate_runtime_logic_detected",
    "state_mapping_complete",
    "state_mapping_missing",
    "authority_mismatch",
    "p17_binding_valid",
    "p17_binding_invalid",
    "human_boundary_preserved",
    "runtime_projection_non_authoritative",
    "workflow_ready",
)

HUMAN_STATES = {
    GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
    GovernedWorkflowState.AWAITING_CORRECTION,
    GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
    GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
}

BLOCKER_STATES = {
    GovernedWorkflowState.BLOCKED,
    GovernedWorkflowState.AWAITING_CORRECTION,
    GovernedWorkflowState.FAILED,
    GovernedWorkflowState.INCIDENT,
    GovernedWorkflowState.RETRY_PENDING,
    GovernedWorkflowState.ROLLBACK_REQUIRED,
}


@pytest.fixture(scope="module")
def accepted_p17_closure(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p18_0")
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
def identity():
    return build_governed_workflow_identity(
        project_id="P18",
        ticket_id="P18.0",
        ticket_revision=1,
        work_packet_id="WP-P18-0-R0001",
        work_packet_SHA256="a" * 64,
    )


@pytest.fixture(scope="module")
def initial_projection():
    return projection_for_state(GovernedWorkflowState.DRAFT)


@pytest.fixture(scope="module")
def initial_snapshot(identity, p17_binding, initial_projection):
    return build_initial_governed_workflow_snapshot(
        identity=identity,
        P17_binding=p17_binding,
        runtime_projection=initial_projection,
    )


@pytest.fixture(scope="module")
def mappings():
    return build_workflow_runtime_state_mappings()


@pytest.fixture(scope="module")
def state_machine_result(p17_binding):
    return build_governed_workflow_state_machine_result(p17_binding)


def construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def digest_model(model: BaseModel, algorithm: str) -> str:
    return gsm._model_digest(algorithm, model)


def make_snapshot(
    state: GovernedWorkflowState,
    identity: GovernedWorkflowIdentity,
    p17_binding: P17WorkflowBinding,
    *,
    projection: HermesWorkflowProjection | None = None,
    index: int = 0,
) -> GovernedWorkflowSnapshot:
    state_definition = gsm._state_definition_for(state)
    completed = tuple(f"GWT-{number:03d}" for number in range(1, index + 1))
    blockers = ("dependency_blocked",) if state is GovernedWorkflowState.BLOCKED else ()
    if state is GovernedWorkflowState.AWAITING_CORRECTION:
        blockers = ("correction_required",)
    if state is GovernedWorkflowState.FAILED:
        blockers = ("execution_failed",)
    if state is GovernedWorkflowState.INCIDENT:
        blockers = ("incident_detected",)
    if state is GovernedWorkflowState.RETRY_PENDING:
        blockers = ("retry_pending",)
    if state is GovernedWorkflowState.ROLLBACK_REQUIRED:
        blockers = ("rollback_required",)
    return gsm._make_model(
        GovernedWorkflowSnapshot,
        "workflow_SHA256",
        gsm.WORKFLOW_SNAPSHOT_DIGEST_ALGORITHM,
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        identity=identity,
        current_state=state,
        state_owner=state_definition.owner,
        transition_index=index,
        completed_transition_ids=completed,
        active_blocker_codes=blockers,
        pending_human_action=gsm._pending_human_action(state),
        P17_binding_SHA256=p17_binding.binding_SHA256,
        runtime_projection=projection or projection_for_state(state),
    )


def projection_for_state(state: GovernedWorkflowState) -> HermesWorkflowProjection:
    if state is GovernedWorkflowState.QUEUED:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="todo",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    if state is GovernedWorkflowState.BLOCKED:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="blocked",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=True,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    if state is GovernedWorkflowState.READY_TO_EXECUTE:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="ready",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=True,
            workspace_binding_present=True,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    if state is GovernedWorkflowState.EXECUTING:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="running",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=True,
            workspace_binding_present=True,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=True,
        )
    if state is GovernedWorkflowState.REVIEWING:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="review",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=True,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    if state is GovernedWorkflowState.COMPLETED:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="done",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=True,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    if state is GovernedWorkflowState.FAILED:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.RUNTIME_ADAPTER,
            runtime_state="failed",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=True,
            dependency_blocked=False,
            retry_state_present=True,
            reclaim_state_present=False,
        )
    if state is GovernedWorkflowState.CANCELLED:
        return build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.RUNTIME_ADAPTER,
            runtime_state="cancelled",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    return build_hermes_workflow_projection(
        runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
        runtime_state=f"pepper:{state.value}",
        task_id=None,
        board_or_queue_id=None,
        worker_id_present=False,
        workspace_binding_present=state
        in {
            GovernedWorkflowState.ALLOCATING,
            GovernedWorkflowState.VALIDATING,
            GovernedWorkflowState.AWAITING_HUMAN_APPROVAL,
            GovernedWorkflowState.AWAITING_HUMAN_GIT_HANDOFF,
        },
        dependency_blocked=False,
        retry_state_present=state is GovernedWorkflowState.RETRY_PENDING,
        reclaim_state_present=False,
    )


def transition_request(
    snapshot: GovernedWorkflowSnapshot,
    transition: GovernedWorkflowTransition,
    *,
    authority: WorkflowTransitionAuthority | None = None,
    trigger: WorkflowTransitionTrigger | None = None,
    evidence_refs: tuple[str, ...] | None = None,
    projection: HermesWorkflowProjection | None = None,
) -> GovernedWorkflowTransitionRequest:
    return GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=snapshot,
        trigger=trigger or transition.trigger,
        authority=authority or transition.authority,
        evidence_refs=evidence_refs
        if evidence_refs is not None
        else transition.required_evidence,
        runtime_projection=projection or projection_for_state(transition.to_state),
    )


def snapshot_for_transition(
    transition: GovernedWorkflowTransition,
    identity: GovernedWorkflowIdentity,
    p17_binding: P17WorkflowBinding,
) -> GovernedWorkflowSnapshot:
    return make_snapshot(transition.from_state, identity, p17_binding)


@pytest.mark.parametrize("exported_name", P18_0_EXPORTS)
def test_all_p18_0_exports_exist(exported_name: str) -> None:
    assert hasattr(workflow, exported_name)
    assert hasattr(gsm, exported_name)


def test_public_exports_are_unique_and_exact_tail() -> None:
    assert tuple(workflow.__all__[: len(P18_0_EXPORTS)]) == P18_0_EXPORTS
    assert tuple(gsm.__all__[: len(P18_0_EXPORTS)]) == P18_0_EXPORTS
    assert len(P18_0_EXPORTS) == 38
    assert len(set(workflow.__all__)) == len(workflow.__all__)
    assert not any(name.startswith("_") for name in workflow.__all__)


@pytest.mark.parametrize(
    "forbidden",
    (
        "WorkflowExecutor",
        "StateMachineExecutor",
        "HermesRuntimeExecutor",
        "execute_workflow",
        "run_workflow",
        "execute_transition",
        "run_transition",
        "retry_workflow",
        "rollback_workflow",
        "ProductionWorkflow",
        "AutonomousWorkflow",
    ),
)
def test_forbidden_public_runtime_exports_absent(forbidden: str) -> None:
    assert forbidden not in workflow.__all__
    assert not hasattr(workflow, forbidden)


def test_schema_and_policy_constants_are_exact() -> None:
    assert GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION == 1
    assert (
        GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
        == "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    )


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_are_frozen(
    model_type: type[BaseModel], state_machine_result
) -> None:
    samples = {
        GovernedWorkflowStateDefinition: state_machine_result.state_definitions[0],
        GovernedWorkflowTransition: state_machine_result.transitions[0],
        GovernedWorkflowIdentity: state_machine_result.P17_binding,
        GovernedWorkflowSnapshot: make_snapshot(
            GovernedWorkflowState.DRAFT,
            build_governed_workflow_identity(
                project_id="P18",
                ticket_id="P18.0",
                ticket_revision=1,
                work_packet_id="WP-P18-0-R0001",
                work_packet_SHA256="a" * 64,
            ),
            state_machine_result.P17_binding,
        ),
        HermesWorkflowProjection: projection_for_state(GovernedWorkflowState.DRAFT),
        WorkflowRuntimeStateMapping: state_machine_result.runtime_mappings[0],
        GovernedWorkflowTransitionRequest: transition_request(
            make_snapshot(
                state_machine_result.transitions[0].from_state,
                build_governed_workflow_identity(
                    project_id="P18",
                    ticket_id="P18.0",
                    ticket_revision=1,
                    work_packet_id="WP-P18-0-R0001",
                    work_packet_SHA256="a" * 64,
                ),
                state_machine_result.P17_binding,
            ),
            state_machine_result.transitions[0],
        ),
        GovernedWorkflowTransitionResult: build_governed_workflow_transition(
            transition_request(
                make_snapshot(
                    state_machine_result.transitions[0].from_state,
                    build_governed_workflow_identity(
                        project_id="P18",
                        ticket_id="P18.0",
                        ticket_revision=1,
                        work_packet_id="WP-P18-0-R0001",
                        work_packet_SHA256="a" * 64,
                    ),
                    state_machine_result.P17_binding,
                ),
                state_machine_result.transitions[0],
            )
        ),
        P17WorkflowBinding: state_machine_result.P17_binding,
        WorkflowStateMachineFinding: state_machine_result.findings[0],
        WorkflowReuseSummary: state_machine_result.reuse_summary,
        GovernedWorkflowStateMachineResult: state_machine_result,
    }
    sample = samples[model_type]
    with pytest.raises(ValidationError):
        sample.__setattr__(next(iter(type(sample).model_fields)), "tampered")


@pytest.mark.parametrize("enum_type", (GovernedWorkflowState,))
def test_governed_workflow_states_are_exact(enum_type: type[Enum]) -> None:
    assert tuple(item.value for item in enum_type) == EXPECTED_STATES


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_every_canonical_state_has_definition(
    state: GovernedWorkflowState, state_machine_result
) -> None:
    definitions = {item.state: item for item in state_machine_result.state_definitions}
    assert state in definitions
    assert definitions[state].owner in set(WorkflowStateOwner)


@pytest.mark.parametrize("state_definition", gsm._STATE_DEFINITIONS)
def test_state_definition_owner_is_never_ambiguous(
    state_definition: GovernedWorkflowStateDefinition,
) -> None:
    assert state_definition.owner.value != "ambiguous_owner"
    assert state_definition.owner in set(WorkflowStateOwner)


@pytest.mark.parametrize("state_definition", gsm._STATE_DEFINITIONS)
def test_state_terminal_consistency(
    state_definition: GovernedWorkflowStateDefinition,
) -> None:
    if state_definition.state in {
        GovernedWorkflowState.COMPLETED,
        GovernedWorkflowState.CANCELLED,
    }:
        assert state_definition.terminal is True
    else:
        assert state_definition.terminal is False


@pytest.mark.parametrize("state_definition", gsm._STATE_DEFINITIONS)
def test_state_human_authority_consistency(
    state_definition: GovernedWorkflowStateDefinition,
) -> None:
    if state_definition.state in HUMAN_STATES:
        assert state_definition.human_authority_required is True
        assert state_definition.owner is WorkflowStateOwner.HUMAN
    if state_definition.owner is WorkflowStateOwner.HUMAN:
        assert state_definition.human_authority_required is True


@pytest.mark.parametrize("state_definition", gsm._STATE_DEFINITIONS)
def test_state_operational_execution_consistency(
    state_definition: GovernedWorkflowStateDefinition,
) -> None:
    if state_definition.operational_execution_allowed:
        assert state_definition.state in {
            GovernedWorkflowState.EXECUTING,
            GovernedWorkflowState.VALIDATING,
        }
    assert state_definition.retry_allowed is False
    assert state_definition.rollback_allowed is False


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_snapshot_for_every_state_validates(
    state: GovernedWorkflowState, identity, p17_binding
) -> None:
    snapshot = make_snapshot(state, identity, p17_binding)
    validate_governed_workflow_snapshot(snapshot)
    assert snapshot.current_state is state


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_snapshot_digest_for_every_state_is_deterministic(
    state: GovernedWorkflowState, identity, p17_binding
) -> None:
    first = make_snapshot(state, identity, p17_binding)
    second = make_snapshot(state, identity, p17_binding)
    assert first.workflow_SHA256 == second.workflow_SHA256


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_snapshot_owner_tampering_fails(
    state: GovernedWorkflowState, identity, p17_binding
) -> None:
    snapshot = make_snapshot(state, identity, p17_binding)
    wrong_owner = next(
        owner for owner in WorkflowStateOwner if owner is not snapshot.state_owner
    )
    bad = construct_with_updates(snapshot, state_owner=wrong_owner)
    with pytest.raises(ValidationError):
        GovernedWorkflowSnapshot.model_validate(bad)


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_snapshot_digest_tampering_fails(
    state: GovernedWorkflowState, identity, p17_binding
) -> None:
    snapshot = make_snapshot(state, identity, p17_binding)
    bad = construct_with_updates(snapshot, workflow_SHA256="0" * 64)
    with pytest.raises(ValidationError):
        GovernedWorkflowSnapshot.model_validate(bad)


def test_unknown_state_fails(identity, p17_binding) -> None:
    with pytest.raises(ValidationError):
        gsm._make_model(
            GovernedWorkflowSnapshot,
            "workflow_SHA256",
            gsm.WORKFLOW_SNAPSHOT_DIGEST_ALGORITHM,
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            identity=identity,
            current_state="ready",
            state_owner=WorkflowStateOwner.PEPPER_GOVERNANCE,
            transition_index=0,
            completed_transition_ids=(),
            active_blocker_codes=(),
            pending_human_action=None,
            P17_binding_SHA256=p17_binding.binding_SHA256,
            runtime_projection=projection_for_state(GovernedWorkflowState.DRAFT),
        )


@pytest.mark.parametrize(
    "alias", ("ready", "approved", "in_progress", "done", "rolled_back")
)
def test_state_aliases_fail(alias: str, identity, p17_binding) -> None:
    with pytest.raises(ValidationError):
        GovernedWorkflowSnapshot(
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            identity=identity,
            current_state=alias,
            state_owner=WorkflowStateOwner.PEPPER_GOVERNANCE,
            transition_index=0,
            completed_transition_ids=(),
            active_blocker_codes=(),
            pending_human_action=None,
            P17_binding_SHA256=p17_binding.binding_SHA256,
            runtime_projection=projection_for_state(GovernedWorkflowState.DRAFT),
            workflow_SHA256="0" * 64,
        )


@pytest.mark.parametrize("trigger", WorkflowTransitionTrigger)
def test_trigger_enum_values_are_controlled(trigger: WorkflowTransitionTrigger) -> None:
    assert trigger.value in EXPECTED_TRIGGERS


@pytest.mark.parametrize("authority", WorkflowTransitionAuthority)
def test_authority_enum_values_are_controlled(
    authority: WorkflowTransitionAuthority,
) -> None:
    assert authority.value in {"system", "human", "governed_runtime", "policy"}


@pytest.mark.parametrize("mapping_kind", WorkflowRuntimeMappingKind)
def test_mapping_kind_enum_values_are_controlled(
    mapping_kind: WorkflowRuntimeMappingKind,
) -> None:
    assert mapping_kind.value in {
        "exact",
        "composite",
        "governance_only",
        "runtime_only",
    }


@pytest.mark.parametrize("severity", WorkflowStateMachineFindingSeverity)
def test_finding_severity_values_are_controlled(
    severity: WorkflowStateMachineFindingSeverity,
) -> None:
    assert severity.value in {"info", "warning", "blocking"}


@pytest.mark.parametrize("code", WorkflowStateMachineFindingCode)
def test_finding_code_values_are_controlled(
    code: WorkflowStateMachineFindingCode,
) -> None:
    assert code.value in EXPECTED_FINDING_CODES


@pytest.mark.parametrize("mapping", build_workflow_runtime_state_mappings())
def test_runtime_mapping_validates(mapping: WorkflowRuntimeStateMapping) -> None:
    assert mapping.mapping_SHA256 == digest_model(
        mapping, gsm.WORKFLOW_MAPPING_DIGEST_ALGORITHM
    )


@pytest.mark.parametrize("mapping", build_workflow_runtime_state_mappings())
def test_runtime_mapping_kind_consistency(mapping: WorkflowRuntimeStateMapping) -> None:
    assert mapping.exact is (mapping.mapping_kind is WorkflowRuntimeMappingKind.EXACT)


@pytest.mark.parametrize("mapping", build_workflow_runtime_state_mappings())
def test_runtime_mapping_notes_are_bounded(
    mapping: WorkflowRuntimeStateMapping,
) -> None:
    assert "database" not in mapping.notes.lower()
    assert "raw" not in mapping.notes.lower()


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_every_governed_state_has_runtime_mapping(
    state: GovernedWorkflowState, mappings
) -> None:
    assert any(mapping.governed_state is state for mapping in mappings)


@pytest.mark.parametrize(
    "runtime_state",
    (
        "kanban:triage",
        "kanban:todo",
        "kanban:scheduled",
        "kanban:ready",
        "kanban:running",
        "kanban:blocked",
        "kanban:review",
        "kanban:done",
        "kanban:archived",
    ),
)
def test_relevant_kanban_runtime_state_is_mapped(runtime_state: str, mappings) -> None:
    assert any(mapping.runtime_state == runtime_state for mapping in mappings)


def test_duplicate_mapping_fails(state_machine_result) -> None:
    with pytest.raises(ValidationError):
        gsm._make_model(
            GovernedWorkflowStateMachineResult,
            "result_SHA256",
            gsm.WORKFLOW_RESULT_DIGEST_ALGORITHM,
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            state_definitions=state_machine_result.state_definitions,
            transitions=state_machine_result.transitions,
            runtime_mappings=state_machine_result.runtime_mappings
            + (state_machine_result.runtime_mappings[0],),
            P17_binding=state_machine_result.P17_binding,
            findings=state_machine_result.findings,
            reuse_summary=state_machine_result.reuse_summary,
            state_machine_ready=True,
            P18_1_ready=True,
            production_readiness_claimed=False,
        )


def test_canonical_invalid_runtime_state_mapping_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="mystery",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )


@pytest.mark.parametrize("transition", gsm._TRANSITIONS)
def test_allowed_transition_request_validates(
    transition: GovernedWorkflowTransition, identity, p17_binding
) -> None:
    snapshot = snapshot_for_transition(transition, identity, p17_binding)
    request = transition_request(snapshot, transition)
    validate_governed_workflow_transition_request(request)


@pytest.mark.parametrize("transition", gsm._TRANSITIONS)
def test_allowed_transition_builds_accepted(
    transition: GovernedWorkflowTransition, identity, p17_binding
) -> None:
    snapshot = snapshot_for_transition(transition, identity, p17_binding)
    result = build_governed_workflow_transition(
        transition_request(snapshot, transition)
    )
    assert result.accepted is True
    assert result.transition.transition_id == transition.transition_id
    assert result.resulting_snapshot.current_state is transition.to_state


@pytest.mark.parametrize("transition", gsm._TRANSITIONS)
def test_transition_digest_valid(transition: GovernedWorkflowTransition) -> None:
    assert transition.transition_SHA256 == digest_model(
        transition, gsm.WORKFLOW_TRANSITION_DIGEST_ALGORITHM
    )


@pytest.mark.parametrize("transition", gsm._TRANSITIONS)
def test_wrong_authority_rejects(
    transition: GovernedWorkflowTransition, identity, p17_binding
) -> None:
    wrong = next(
        authority
        for authority in WorkflowTransitionAuthority
        if authority is not transition.authority
    )
    snapshot = snapshot_for_transition(transition, identity, p17_binding)
    request = transition_request(snapshot, transition, authority=wrong)
    with pytest.raises(GovernedWorkflowStateMachineStateError):
        validate_governed_workflow_transition_request(request)
    result = build_governed_workflow_transition(request)
    assert result.accepted is False
    assert result.resulting_snapshot == snapshot


@pytest.mark.parametrize("transition", gsm._TRANSITIONS)
def test_missing_evidence_rejects(
    transition: GovernedWorkflowTransition, identity, p17_binding
) -> None:
    snapshot = snapshot_for_transition(transition, identity, p17_binding)
    request = transition_request(snapshot, transition, evidence_refs=())
    with pytest.raises(GovernedWorkflowStateMachinePolicyError):
        validate_governed_workflow_transition_request(request)
    result = build_governed_workflow_transition(request)
    assert result.accepted is False
    assert result.resulting_snapshot == snapshot


@pytest.mark.parametrize("transition", gsm._TRANSITIONS)
def test_transition_result_is_deterministic(
    transition: GovernedWorkflowTransition, identity, p17_binding
) -> None:
    snapshot = snapshot_for_transition(transition, identity, p17_binding)
    request = transition_request(snapshot, transition)
    first = build_governed_workflow_transition(request)
    second = build_governed_workflow_transition(request)
    assert first.result_SHA256 == second.result_SHA256
    assert first == second


def test_transition_ids_are_contiguous() -> None:
    assert tuple(t.transition_id for t in gsm._TRANSITIONS) == tuple(
        f"GWT-{index:03d}" for index in range(1, len(gsm._TRANSITIONS) + 1)
    )


def test_caller_cannot_select_arbitrary_target_state(initial_snapshot) -> None:
    transition = gsm._TRANSITIONS[0]
    with pytest.raises(ValidationError):
        GovernedWorkflowTransitionRequest(
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            current_snapshot=initial_snapshot,
            trigger=transition.trigger,
            authority=transition.authority,
            evidence_refs=transition.required_evidence,
            runtime_projection=projection_for_state(transition.to_state),
            target_state=GovernedWorkflowState.COMPLETED,
        )


def test_canonical_human_approval_cannot_be_bypassed(identity, p17_binding) -> None:
    transition = next(
        item
        for item in gsm._TRANSITIONS
        if item.trigger is WorkflowTransitionTrigger.HUMAN_APPROVED
    )
    snapshot = make_snapshot(transition.from_state, identity, p17_binding)
    request = transition_request(
        snapshot,
        transition,
        authority=WorkflowTransitionAuthority.GOVERNED_RUNTIME,
    )
    with pytest.raises(GovernedWorkflowStateMachineStateError):
        validate_governed_workflow_transition_request(request)
    result = build_governed_workflow_transition(request)
    assert result.accepted is False
    assert result.human_action_required is True
    assert result.resulting_snapshot.current_state is transition.from_state


def test_git_completion_remains_human_authority(identity, p17_binding) -> None:
    transition = next(
        item
        for item in gsm._TRANSITIONS
        if item.trigger is WorkflowTransitionTrigger.HUMAN_GIT_COMPLETED
    )
    assert transition.authority is WorkflowTransitionAuthority.HUMAN
    assert transition.automatic is False
    snapshot = make_snapshot(transition.from_state, identity, p17_binding)
    request = transition_request(snapshot, transition)
    assert build_governed_workflow_transition(request).accepted is True


@pytest.mark.parametrize(
    "trigger",
    (
        WorkflowTransitionTrigger.RETRY_AUTHORIZED,
        WorkflowTransitionTrigger.ROLLBACK_AUTHORIZED,
    ),
)
def test_retry_and_rollback_are_not_automatic(
    trigger: WorkflowTransitionTrigger,
) -> None:
    transition = next(item for item in gsm._TRANSITIONS if item.trigger is trigger)
    assert transition.authority is WorkflowTransitionAuthority.HUMAN
    assert transition.automatic is False


def test_execution_start_requires_worker_and_workspace(identity, p17_binding) -> None:
    transition = next(
        item
        for item in gsm._TRANSITIONS
        if item.trigger is WorkflowTransitionTrigger.EXECUTION_STARTED
    )
    snapshot = make_snapshot(transition.from_state, identity, p17_binding)
    bad_projection = build_hermes_workflow_projection(
        runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
        runtime_state="ready",
        task_id="task-p18-0",
        board_or_queue_id="board-p18",
        worker_id_present=False,
        workspace_binding_present=False,
        dependency_blocked=False,
        retry_state_present=False,
        reclaim_state_present=False,
    )
    request = transition_request(snapshot, transition, projection=bad_projection)
    with pytest.raises(GovernedWorkflowStateMachinePolicyError):
        validate_governed_workflow_transition_request(request)


def test_terminal_state_rejects_transition(identity, p17_binding) -> None:
    transition = gsm._TRANSITIONS[0]
    snapshot = make_snapshot(GovernedWorkflowState.COMPLETED, identity, p17_binding)
    request = transition_request(snapshot, transition)
    with pytest.raises(GovernedWorkflowStateMachineStateError):
        validate_governed_workflow_transition_request(request)


def test_canonical_governed_workflow_happy_path(initial_snapshot) -> None:
    path = (
        "GWT-001",
        "GWT-002",
        "GWT-003",
        "GWT-004",
        "GWT-005",
        "GWT-008",
        "GWT-009",
        "GWT-010",
        "GWT-011",
        "GWT-013",
        "GWT-015",
        "GWT-018",
        "GWT-020",
    )
    transitions = {item.transition_id: item for item in gsm._TRANSITIONS}
    snapshot = initial_snapshot
    digests = []
    for transition_id in path:
        transition = transitions[transition_id]
        result = build_governed_workflow_transition(
            transition_request(snapshot, transition)
        )
        assert result.accepted is True
        digests.append(result.result_SHA256)
        snapshot = result.resulting_snapshot
    assert snapshot.current_state is GovernedWorkflowState.COMPLETED
    assert snapshot.transition_index == len(path)
    assert tuple(snapshot.completed_transition_ids) == path
    assert len(digests) == len(set(digests))


def test_dependency_block_and_unblock_flow(identity, p17_binding) -> None:
    queued = make_snapshot(GovernedWorkflowState.QUEUED, identity, p17_binding)
    block_transition = next(
        item for item in gsm._TRANSITIONS if item.transition_id == "GWT-006"
    )
    blocked = build_governed_workflow_transition(
        transition_request(queued, block_transition)
    ).resulting_snapshot
    assert blocked.current_state is GovernedWorkflowState.BLOCKED
    assert blocked.active_blocker_codes == ("dependency_blocked",)
    unblock_transition = next(
        item for item in gsm._TRANSITIONS if item.transition_id == "GWT-007"
    )
    unblocked = build_governed_workflow_transition(
        transition_request(blocked, unblock_transition)
    ).resulting_snapshot
    assert unblocked.current_state is GovernedWorkflowState.QUEUED
    assert unblocked.active_blocker_codes == ()


def test_work_packet_ready_can_block_before_queue_admission(
    identity, p17_binding
) -> None:
    work_packet_ready = make_snapshot(
        GovernedWorkflowState.WORK_PACKET_READY,
        identity,
        p17_binding,
    )
    transition = next(
        item for item in gsm._TRANSITIONS if item.transition_id == "GWT-026"
    )
    result = build_governed_workflow_transition(
        transition_request(work_packet_ready, transition)
    )
    assert result.accepted is True
    assert transition.from_state is GovernedWorkflowState.WORK_PACKET_READY
    assert transition.to_state is GovernedWorkflowState.BLOCKED
    assert transition.trigger is WorkflowTransitionTrigger.DEPENDENCIES_BLOCKED
    assert transition.authority is WorkflowTransitionAuthority.POLICY
    assert transition.required_evidence == ("dependency_blocker",)
    assert transition.automatic is True
    assert result.resulting_snapshot.current_state is GovernedWorkflowState.BLOCKED
    assert result.resulting_snapshot.active_blocker_codes == ("dependency_blocked",)


def test_ticket_approval_rejection_uses_governed_transition(
    identity, p17_binding
) -> None:
    awaiting_approval = make_snapshot(
        GovernedWorkflowState.AWAITING_TICKET_APPROVAL, identity, p17_binding
    )
    transition = next(
        item for item in gsm._TRANSITIONS if item.transition_id == "GWT-025"
    )
    result = build_governed_workflow_transition(
        transition_request(awaiting_approval, transition)
    )
    assert result.accepted is True
    assert transition.trigger is WorkflowTransitionTrigger.HUMAN_REJECTED
    assert transition.authority is WorkflowTransitionAuthority.HUMAN
    assert transition.automatic is False
    assert (
        result.resulting_snapshot.current_state
        is GovernedWorkflowState.AWAITING_CORRECTION
    )
    assert result.resulting_snapshot.active_blocker_codes == ("correction_required",)
    assert result.resulting_snapshot.pending_human_action == "correction"


def test_identity_is_deterministic() -> None:
    first = build_governed_workflow_identity(
        project_id="P18",
        ticket_id="P18.0",
        ticket_revision=1,
        work_packet_id="WP-P18-0-R0001",
        work_packet_SHA256="b" * 64,
    )
    second = build_governed_workflow_identity(
        project_id="P18",
        ticket_id="P18.0",
        ticket_revision=1,
        work_packet_id="WP-P18-0-R0001",
        work_packet_SHA256="b" * 64,
    )
    assert first == second
    assert first.workflow_id.startswith("GWF-")


def test_identity_changes_when_workpacket_changes() -> None:
    first = build_governed_workflow_identity(
        project_id="P18",
        ticket_id="P18.0",
        ticket_revision=1,
        work_packet_id="WP-P18-0-R0001",
        work_packet_SHA256="b" * 64,
    )
    second = build_governed_workflow_identity(
        project_id="P18",
        ticket_id="P18.0",
        ticket_revision=1,
        work_packet_id="WP-P18-0-R0002",
        work_packet_SHA256="c" * 64,
    )
    assert first.workflow_id != second.workflow_id
    assert first.identity_SHA256 != second.identity_SHA256


def test_identity_digest_tampering_fails(identity) -> None:
    bad = construct_with_updates(identity, identity_SHA256="0" * 64)
    with pytest.raises(ValidationError):
        GovernedWorkflowIdentity.model_validate(bad)


def test_identity_has_no_wall_clock_uuid_or_randomness(identity) -> None:
    assert "uuid" not in identity.workflow_id.lower()
    assert "time" not in identity.workflow_id.lower()
    assert "random" not in identity.workflow_id.lower()
    assert not any(
        name in gsm.__dict__ for name in ("time", "datetime", "uuid", "random")
    )


def test_p17_binding_canonical_passes(p17_binding) -> None:
    assert p17_binding.WorkPacket_execution_MVP_available is True
    assert p17_binding.human_Git_authority_required is True
    assert p17_binding.non_critical_scope is True
    assert p17_binding.production_readiness_claimed is False


@pytest.mark.parametrize(
    "field,value",
    (
        ("P17_closure_id", "P17C-badbadbadbad"),
        ("P17_closure_SHA256", "0" * 64),
        ("WorkPacket_execution_MVP_available", False),
        ("human_Git_authority_required", False),
        ("non_critical_scope", False),
        ("production_readiness_claimed", True),
    ),
)
def test_p17_binding_tampering_fails(p17_binding, field: str, value) -> None:
    bad = construct_with_updates(p17_binding, **{field: value})
    with pytest.raises((ValidationError, ValueError)):
        P17WorkflowBinding.model_validate(bad)


def test_p17_binding_digest_tampering_fails(p17_binding) -> None:
    bad = construct_with_updates(p17_binding, binding_SHA256="0" * 64)
    with pytest.raises(ValidationError):
        P17WorkflowBinding.model_validate(bad)


@pytest.mark.parametrize("state", GovernedWorkflowState)
def test_projection_for_state_validates(state: GovernedWorkflowState) -> None:
    projection = projection_for_state(state)
    validate_hermes_workflow_projection(projection)
    assert projection.runtime_projection_is_authoritative_governance_state is False


def test_projection_digest_tampering_fails() -> None:
    projection = projection_for_state(GovernedWorkflowState.QUEUED)
    bad = construct_with_updates(projection, projection_SHA256="0" * 64)
    with pytest.raises(ValidationError):
        HermesWorkflowProjection.model_validate(bad)


@pytest.mark.parametrize(
    "runtime_state",
    ("sqlite rowid 1", "SELECT raw rows", "runtime handle 7", "raw stdout payload"),
)
def test_projection_rejects_raw_runtime_data(runtime_state: str) -> None:
    with pytest.raises(ValidationError):
        build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
            runtime_state=runtime_state,
            task_id=None,
            board_or_queue_id=None,
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )


@pytest.mark.parametrize("runtime_kind", HermesWorkflowRuntimeKind)
def test_projection_kind_is_controlled(runtime_kind: HermesWorkflowRuntimeKind) -> None:
    if runtime_kind is HermesWorkflowRuntimeKind.KANBAN_SWARM:
        projection = build_hermes_workflow_projection(
            runtime_kind=runtime_kind,
            runtime_state="todo",
            task_id="task-p18-0",
            board_or_queue_id="board-p18",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    else:
        projection = build_hermes_workflow_projection(
            runtime_kind=runtime_kind,
            runtime_state="pepper:projection",
            task_id=None
            if runtime_kind is HermesWorkflowRuntimeKind.GOVERNANCE_ONLY
            else "task-p18-0",
            board_or_queue_id=None
            if runtime_kind is HermesWorkflowRuntimeKind.GOVERNANCE_ONLY
            else "board-p18",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )
    assert projection.runtime_kind is runtime_kind


def test_governance_projection_cannot_carry_runtime_ids() -> None:
    with pytest.raises(ValidationError):
        build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
            runtime_state="pepper:draft",
            task_id="task-p18-0",
            board_or_queue_id=None,
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        )


def test_reuse_summary_counts_and_flags(state_machine_result) -> None:
    summary = state_machine_result.reuse_summary
    assert summary.capabilities_assessed == 15
    assert summary.capabilities_reused == 7
    assert summary.capabilities_customized == 5
    assert summary.capabilities_replaced == 0
    assert summary.capabilities_deferred == 3
    assert summary.duplicate_runtime_capabilities_created == 0
    assert summary.Kanban_Swarm_assessed is True
    assert summary.prior_Hermes_0_19_analysis_reused is True
    assert summary.current_targeted_revalidation_performed is True


@pytest.mark.parametrize(
    "flag",
    (
        "Kanban_Swarm_assessed",
        "planner_assessed",
        "dispatcher_assessed",
        "heartbeat_assessed",
        "retry_assessed",
        "reclaim_assessed",
        "workspace_lifecycle_assessed",
        "approval_surfaces_assessed",
        "dashboard_TUI_surfaces_assessed",
    ),
)
def test_reuse_summary_required_surface_assessed(
    state_machine_result, flag: str
) -> None:
    assert getattr(state_machine_result.reuse_summary, flag) is True


def test_reuse_summary_duplicate_runtime_logic_fails(state_machine_result) -> None:
    summary = construct_with_updates(
        state_machine_result.reuse_summary,
        duplicate_runtime_capabilities_created=1,
    )
    with pytest.raises(ValidationError):
        WorkflowReuseSummary.model_validate(summary)


def test_state_machine_result_ready_posture(state_machine_result) -> None:
    assert state_machine_result.state_machine_ready is True
    assert state_machine_result.P18_1_ready is True
    assert state_machine_result.production_readiness_claimed is False
    assert not any(
        finding.severity is WorkflowStateMachineFindingSeverity.BLOCKING
        for finding in state_machine_result.findings
    )


def test_state_machine_result_digest_valid(state_machine_result) -> None:
    assert state_machine_result.result_SHA256 == digest_model(
        state_machine_result, gsm.WORKFLOW_RESULT_DIGEST_ALGORITHM
    )


def test_state_machine_result_digest_tampering_fails(state_machine_result) -> None:
    bad = construct_with_updates(state_machine_result, result_SHA256="0" * 64)
    with pytest.raises(ValidationError):
        GovernedWorkflowStateMachineResult.model_validate(bad)


@pytest.mark.parametrize("finding", range(1, 19))
def test_findings_are_contiguous(finding: int, state_machine_result) -> None:
    assert (
        state_machine_result.findings[finding - 1].finding_id == f"GSMF-{finding:03d}"
    )


@pytest.mark.parametrize("finding", range(1, 19))
def test_finding_digest_valid(finding: int, state_machine_result) -> None:
    item = state_machine_result.findings[finding - 1]
    assert item.finding_SHA256 == digest_model(
        item, gsm.WORKFLOW_FINDING_DIGEST_ALGORITHM
    )


def test_blocking_finding_prevents_readiness(state_machine_result) -> None:
    blocking = gsm._build_finding(
        "GSMF-019",
        WorkflowStateMachineFindingSeverity.BLOCKING,
        WorkflowStateMachineFindingCode.STATE_MAPPING_MISSING,
        "runtime mappings",
        "A mapping is missing.",
    )
    with pytest.raises(ValidationError):
        gsm._make_model(
            GovernedWorkflowStateMachineResult,
            "result_SHA256",
            gsm.WORKFLOW_RESULT_DIGEST_ALGORITHM,
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            state_definitions=state_machine_result.state_definitions,
            transitions=state_machine_result.transitions,
            runtime_mappings=state_machine_result.runtime_mappings,
            P17_binding=state_machine_result.P17_binding,
            findings=state_machine_result.findings + (blocking,),
            reuse_summary=state_machine_result.reuse_summary,
            state_machine_ready=True,
            P18_1_ready=True,
            production_readiness_claimed=False,
        )


def test_pepper_identity_flags_are_represented(state_machine_result) -> None:
    assert (
        state_machine_result.reuse_summary.duplicate_runtime_capabilities_created == 0
    )
    assert state_machine_result.reuse_summary.capabilities_replaced == 0
    assert state_machine_result.reuse_summary.capabilities_customized > 0
    assert state_machine_result.reuse_summary.capabilities_reused > 0


def test_p19_gbrain_boundary_not_claimed(state_machine_result) -> None:
    assert state_machine_result.reuse_summary.capabilities_deferred >= 1
    assert not any(
        "G-Brain exists" in finding.summary for finding in state_machine_result.findings
    )


def test_p20_paperclip_boundary_not_claimed(state_machine_result) -> None:
    assert state_machine_result.reuse_summary.capabilities_deferred >= 1
    assert not any(
        "Paperclip exists" in finding.summary
        for finding in state_machine_result.findings
    )


@pytest.mark.parametrize(
    "forbidden_name",
    (
        "os",
        "subprocess",
        "pathlib",
        "Path",
        "socket",
        "requests",
        "httpx",
        "sqlite3",
        "docker",
        "graphify",
        "git",
        "Repo",
    ),
)
def test_operational_authority_modules_absent(forbidden_name: str) -> None:
    assert forbidden_name not in gsm.__dict__


@pytest.mark.parametrize(
    "operation",
    (
        "run",
        "Popen",
        "check_output",
        "system",
        "open",
        "connect",
        "execute",
        "retry_workflow",
        "rollback_workflow",
    ),
)
def test_operational_authority_functions_absent(operation: str) -> None:
    assert operation not in gsm.__dict__


def test_exception_hierarchy_is_bounded() -> None:
    for error_type in (
        GovernedWorkflowStateMachinePolicyError,
        GovernedWorkflowStateMachineStateError,
        GovernedWorkflowStateMachineValidationError,
    ):
        assert issubclass(error_type, GovernedWorkflowStateMachineError)


def test_alternative_schema_version_rejected(initial_snapshot) -> None:
    transition = gsm._TRANSITIONS[0]
    with pytest.raises(ValidationError):
        GovernedWorkflowTransitionRequest(
            schema_version=2,
            policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
            current_snapshot=initial_snapshot,
            trigger=transition.trigger,
            authority=transition.authority,
            evidence_refs=transition.required_evidence,
            runtime_projection=projection_for_state(transition.to_state),
        )


def test_alternative_policy_id_rejected(initial_snapshot) -> None:
    transition = gsm._TRANSITIONS[0]
    with pytest.raises(ValidationError):
        GovernedWorkflowTransitionRequest(
            schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
            policy_id="other-policy",
            current_snapshot=initial_snapshot,
            trigger=transition.trigger,
            authority=transition.authority,
            evidence_refs=transition.required_evidence,
            runtime_projection=projection_for_state(transition.to_state),
        )


def test_runtime_negotiation_and_schema_migration_absent() -> None:
    assert not hasattr(workflow, "negotiate_workflow_schema")
    assert not hasattr(workflow, "migrate_workflow_schema")


def test_p18_1_consumable_public_models_exported() -> None:
    for name in (
        "GovernedWorkflowState",
        "GovernedWorkflowTransition",
        "GovernedWorkflowIdentity",
        "GovernedWorkflowSnapshot",
        "GovernedWorkflowTransitionRequest",
        "GovernedWorkflowTransitionResult",
        "HermesWorkflowProjection",
        "WorkflowRuntimeStateMapping",
        "P17WorkflowBinding",
        "WorkflowReuseSummary",
        "GovernedWorkflowStateMachineResult",
    ):
        assert name in workflow.__all__


def test_state_machine_does_not_implement_memory_or_work_control_runtime() -> None:
    assert not hasattr(workflow, "GBrain")
    assert not hasattr(workflow, "Paperclip")
    assert not hasattr(workflow, "DurableWorkControlPlane")


def test_result_does_not_claim_production(state_machine_result) -> None:
    assert state_machine_result.production_readiness_claimed is False


def test_manual_validation_warning_only(state_machine_result) -> None:
    warning_findings = [
        finding
        for finding in state_machine_result.findings
        if finding.severity is WorkflowStateMachineFindingSeverity.WARNING
    ]
    assert len(warning_findings) == 1
    assert (
        warning_findings[0].code
        is WorkflowStateMachineFindingCode.HERMES_CAPABILITY_GAP
    )
