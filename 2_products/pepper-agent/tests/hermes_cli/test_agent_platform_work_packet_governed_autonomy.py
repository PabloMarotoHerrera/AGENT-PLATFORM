from __future__ import annotations

from enum import Enum
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.governed_autonomy as autonomy
from hermes_cli.agent_platform.work_packet import (
    GOVERNED_AUTONOMY_BOUNDARY_CLASSIFICATION,
    GOVERNED_AUTONOMY_POLICY_ID,
    GOVERNED_AUTONOMY_SCHEMA_VERSION,
    AutonomyCommandCapturedStream,
    AutonomyCommandDecision,
    AutonomyCommandDenialReason,
    AutonomyCommandDisposition,
    AutonomyCommandEvaluation,
    AutonomyCommandExecutionResult,
    AutonomyCommandFailureReason,
    AutonomyCommandProposal,
    AutonomyCommandStreamKind,
    AutonomyContinuationLineage,
    AutonomyContinuationState,
    AutonomyContinuationStopReason,
    CapabilityGapDisposition,
    CapabilityGapEvidence,
    CapabilityGapKind,
    GovernedAutonomyBudget,
    GovernedAutonomyEnvelope,
    GovernedAutonomyIntegrityError,
    GovernedAutonomyPolicyError,
    GovernedAutonomyReuseAssessment,
    GovernedAutonomyReuseDisposition,
    TaskLocalCapabilityContract,
    TaskLocalToolLanguage,
    TaskLocalToolMaterializationResult,
    TaskLocalToolMaterializationState,
    ToolCandidate,
    ToolPermissionOperation,
    build_governed_autonomy_envelope,
    build_governed_autonomy_reuse_matrix,
    build_single_agent_execution_authorization,
    build_single_agent_runtime_binding,
    build_task_local_capability_contract,
    build_tool_candidate,
    classify_capability_gap,
    complete_single_agent_execution,
    evaluate_autonomy_command,
    execute_autonomy_command,
    execute_single_agent_tool_action,
    materialize_task_local_tool,
    prepare_single_agent_execution,
    propose_autonomy_command,
    start_governed_autonomy_continuation,
    advance_governed_autonomy_continuation,
    validate_governed_autonomy_continuation,
    validate_governed_autonomy_envelope,
)
from tests.hermes_cli import test_agent_platform_work_packet_execution_mvp_closure as p17_r
from tests.hermes_cli.test_agent_platform_work_packet_single_agent_execution import (
    action as single_action,
    allocation_result as single_allocation_result,
    compilation_result as single_compilation_result,
    plan as single_plan,
    profile_result as single_profile_result,
)
from tests.hermes_cli.test_agent_platform_work_packet_validation_command_runner import (
    completed_single_agent_context,
)


P01AH_EXPORTS = autonomy.__all__
PUBLIC_MODELS = (
    GovernedAutonomyBudget,
    GovernedAutonomyReuseAssessment,
    GovernedAutonomyEnvelope,
    CapabilityGapEvidence,
    TaskLocalCapabilityContract,
    ToolCandidate,
    TaskLocalToolMaterializationResult,
    AutonomyCommandProposal,
    AutonomyCommandEvaluation,
    AutonomyCommandCapturedStream,
    AutonomyCommandExecutionResult,
    AutonomyContinuationLineage,
)
CONTROLLED_ENUMS = (
    GovernedAutonomyReuseDisposition,
    CapabilityGapKind,
    CapabilityGapDisposition,
    TaskLocalToolLanguage,
    TaskLocalToolMaterializationState,
    AutonomyCommandDecision,
    AutonomyCommandDenialReason,
    AutonomyCommandDisposition,
    AutonomyCommandFailureReason,
    AutonomyCommandStreamKind,
    AutonomyContinuationState,
    AutonomyContinuationStopReason,
)


def _construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def _envelope_from_context(context, budget: GovernedAutonomyBudget | None = None):
    return build_governed_autonomy_envelope(
        compilation_result=context["compilation"],
        allocation_result=context["allocation"],
        profile_result=context["profile"],
        single_agent_execution_result=context["single_result"],
        budget=budget,
    )


def _python_contract_candidate(envelope: GovernedAutonomyEnvelope):
    gap = classify_capability_gap(
        envelope=envelope,
        observed_failure="ModuleNotFoundError: missing task-local assertion helper",
        requested_capability="Need a local helper to inspect generated text.",
    )
    contract = build_task_local_capability_contract(
        envelope=envelope,
        gap=gap,
        tool_name="assert_generated_text",
        language=TaskLocalToolLanguage.PYTHON,
        implementation_path="src/tools/assert_generated_text.py",
    )
    candidate = build_tool_candidate(
        contract=contract,
        source_text=(
            "from pathlib import Path\n"
            "import sys\n"
            "text = Path(sys.argv[1]).read_text(encoding='utf-8')\n"
            "if 'hello from P17.3' not in text:\n"
            "    raise SystemExit(2)\n"
            "print('helper-ok')\n"
        ),
    )
    return gap, contract, candidate


def _completed_frontend_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = single_compilation_result(
        allowed_paths=("2_products/pepper-agent/web/src/**",),
        task_count=2,
    )
    workspace_root = tmp_path / "frontend_workspace"
    fixture_dir = workspace_root / "2_products/pepper-agent/web/src/autonomy"
    fixture_dir.mkdir(parents=True)
    fixture_path = "2_products/pepper-agent/web/src/autonomy/Component.test.tsx"
    (workspace_root / fixture_path).write_text(
        "import { render } from '@testing-library/react'\n"
        "test('renders', () => render(<div>Pepper</div>))",
        encoding="utf-8",
    )
    allocated, _status_state = single_allocation_result(monkeypatch, result, workspace_root)
    permissions = single_profile_result(result, allocated)
    binding = build_single_agent_runtime_binding(
        agent_id="agent.01ah.frontend",
        worker_id="worker.01ah.frontend",
        work_packet=result.work_packet,
    )
    tasks = result.work_packet.tasks
    execution_plan = single_plan(
        (
            single_action(
                1,
                tasks[0].step_id,
                ToolPermissionOperation.READ_FILE,
                fixture_path,
            ),
            single_action(
                2,
                tasks[1].step_id,
                ToolPermissionOperation.LIST_DIRECTORY,
                "2_products/pepper-agent/web/src/autonomy",
            ),
        )
    )
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.01ah",
        authorization_reference="AUTH-01AH-FRONTEND",
        rationale="Authorize frontend fixture read-only execution context.",
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        risk_acknowledgement="Synthetic frontend fixture risk acknowledged.",
    )
    request = work_packet.SingleAgentExecutionRequest(
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        execution_authorization=authorization,
    )
    session = prepare_single_agent_execution(request)
    first = execute_single_agent_tool_action(
        work_packet.SingleAgentActionExecutionRequest(
            execution_request=request,
            session=session,
        )
    )
    second = execute_single_agent_tool_action(
        work_packet.SingleAgentActionExecutionRequest(
            execution_request=request,
            session=first.updated_session,
        )
    )
    single_result = complete_single_agent_execution(second.updated_session)
    return {
        "compilation": result,
        "allocation": allocated,
        "profile": permissions,
        "single_result": single_result,
        "workspace_root": workspace_root,
        "fixture_path": fixture_path,
    }


@pytest.fixture()
def python_autonomy_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = completed_single_agent_context(monkeypatch, tmp_path)
    context["envelope"] = _envelope_from_context(context)
    return context


@pytest.fixture()
def completed_python_slice(python_autonomy_context):
    envelope = python_autonomy_context["envelope"]
    gap, contract, candidate = _python_contract_candidate(envelope)
    materialization = materialize_task_local_tool(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
    )
    proposal = propose_autonomy_command(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
        source_command="python src/tools/assert_generated_text.py src/generated/readme.txt",
        timeout_seconds=10,
    )
    evaluation = evaluate_autonomy_command(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
        proposal=proposal,
    )
    result = execute_autonomy_command(evaluation)
    lineage = start_governed_autonomy_continuation(envelope=envelope, gap=gap)
    completed_lineage = advance_governed_autonomy_continuation(
        envelope=envelope,
        lineage=lineage,
        candidate=candidate,
        command_evaluation=evaluation,
        command_result=result,
        progress_marker="validated-src-generated-readme",
    )
    return {
        **python_autonomy_context,
        "gap": gap,
        "contract": contract,
        "candidate": candidate,
        "materialization": materialization,
        "proposal": proposal,
        "evaluation": evaluation,
        "result": result,
        "lineage": completed_lineage,
    }


@pytest.mark.parametrize("exported_name", P01AH_EXPORTS)
def test_01ah_exports_are_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)
    assert hasattr(autonomy, exported_name)


def test_01ah_exports_append_after_p17_r() -> None:
    assert work_packet.__all__[255:283] == p17_r.P17_R_EXPORTS
    assert work_packet.__all__[283 : 283 + len(P01AH_EXPORTS)] == P01AH_EXPORTS
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)


def test_constants_are_canonical() -> None:
    assert GOVERNED_AUTONOMY_SCHEMA_VERSION == 1
    assert GOVERNED_AUTONOMY_POLICY_ID == "pepper-governed-task-local-autonomy-v1"
    assert GOVERNED_AUTONOMY_BOUNDARY_CLASSIFICATION == "CAPABILITY != AUTHORITY"


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_controlled_enums_have_no_aliases(enum_cls: type[Enum]) -> None:
    assert len(enum_cls) == len({item.value for item in enum_cls})


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_frozen(model_cls: type[BaseModel]) -> None:
    assert model_cls.model_config["frozen"] is True
    assert model_cls.model_config["extra"] == "forbid"
    assert model_cls.model_config["validate_default"] is True


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_model_schemas_reject_additional_properties(
    model_cls: type[BaseModel],
) -> None:
    assert model_cls.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_json_round_trip(model_cls: type[BaseModel], completed_python_slice) -> None:
    sample_models = {
        GovernedAutonomyBudget.__name__: completed_python_slice["envelope"].budget,
        GovernedAutonomyReuseAssessment.__name__: build_governed_autonomy_reuse_matrix()[0],
        GovernedAutonomyEnvelope.__name__: completed_python_slice["envelope"],
        CapabilityGapEvidence.__name__: completed_python_slice["gap"],
        TaskLocalCapabilityContract.__name__: completed_python_slice["contract"],
        ToolCandidate.__name__: completed_python_slice["candidate"],
        TaskLocalToolMaterializationResult.__name__: completed_python_slice[
            "materialization"
        ],
        AutonomyCommandProposal.__name__: completed_python_slice["proposal"],
        AutonomyCommandEvaluation.__name__: completed_python_slice["evaluation"],
        AutonomyCommandCapturedStream.__name__: completed_python_slice["result"].stdout,
        AutonomyCommandExecutionResult.__name__: completed_python_slice["result"],
        AutonomyContinuationLineage.__name__: completed_python_slice["lineage"],
    }
    model = sample_models[model_cls.__name__]
    assert model_cls.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_reject_unknown_fields(model_cls: type[BaseModel], completed_python_slice) -> None:
    sample_models = {
        GovernedAutonomyBudget.__name__: completed_python_slice["envelope"].budget,
        GovernedAutonomyReuseAssessment.__name__: build_governed_autonomy_reuse_matrix()[0],
        GovernedAutonomyEnvelope.__name__: completed_python_slice["envelope"],
        CapabilityGapEvidence.__name__: completed_python_slice["gap"],
        TaskLocalCapabilityContract.__name__: completed_python_slice["contract"],
        ToolCandidate.__name__: completed_python_slice["candidate"],
        TaskLocalToolMaterializationResult.__name__: completed_python_slice[
            "materialization"
        ],
        AutonomyCommandProposal.__name__: completed_python_slice["proposal"],
        AutonomyCommandEvaluation.__name__: completed_python_slice["evaluation"],
        AutonomyCommandCapturedStream.__name__: completed_python_slice["result"].stdout,
        AutonomyCommandExecutionResult.__name__: completed_python_slice["result"],
        AutonomyContinuationLineage.__name__: completed_python_slice["lineage"],
    }
    payload = sample_models[model_cls.__name__].model_dump(mode="json")
    payload["unknown"] = "rejected"
    with pytest.raises(ValidationError):
        model_cls.model_validate(payload)


def test_reuse_matrix_distinguishes_reused_adapted_and_new() -> None:
    matrix = build_governed_autonomy_reuse_matrix()
    by_component = {item.component: item.disposition for item in matrix}
    assert by_component["workpacket.file_guard"] is GovernedAutonomyReuseDisposition.HERMES_REUSED
    assert by_component["workpacket.tool_permissions"] is GovernedAutonomyReuseDisposition.HERMES_REUSED
    assert by_component["validation_command.subprocess_pattern"] is GovernedAutonomyReuseDisposition.HERMES_ADAPTED
    assert by_component["hermes.dynamic_tool_surfaces"] is GovernedAutonomyReuseDisposition.HERMES_ADAPTED
    assert by_component["pepper.autonomy_envelope"] is GovernedAutonomyReuseDisposition.PEPPER_NEW


def test_python_self_repair_materializes_validates_and_continues(completed_python_slice) -> None:
    materialization = completed_python_slice["materialization"]
    evaluation = completed_python_slice["evaluation"]
    result = completed_python_slice["result"]
    lineage = completed_python_slice["lineage"]
    helper_path = (
        completed_python_slice["workspace_root"] / "src/tools/assert_generated_text.py"
    )
    assert helper_path.is_file()
    assert materialization.state is TaskLocalToolMaterializationState.MATERIALIZED
    assert evaluation.decision is AutonomyCommandDecision.ALLOW
    assert evaluation.shell is False
    assert result.disposition is AutonomyCommandDisposition.PASSED
    assert result.stdout.retained_text is not None
    assert "helper-ok" in result.stdout.retained_text
    assert result.provider_dispatch_count == 0
    assert result.model_inference_count == 0
    assert lineage.state is AutonomyContinuationState.COMPLETED
    assert lineage.successful_command_count == 1
    validate_governed_autonomy_envelope(completed_python_slice["envelope"])
    validate_governed_autonomy_continuation(lineage)


def test_frontend_fixture_self_repair_uses_workpacket_scope(monkeypatch, tmp_path) -> None:
    context = _completed_frontend_context(monkeypatch, tmp_path)
    envelope = _envelope_from_context(context)
    gap = classify_capability_gap(
        envelope=envelope,
        observed_failure="No helper exists to inspect the frontend test fixture.",
        requested_capability="Need a task-local assertion helper for TSX fixture text.",
    )
    contract = build_task_local_capability_contract(
        envelope=envelope,
        gap=gap,
        tool_name="assert_frontend_fixture",
        language=TaskLocalToolLanguage.PYTHON,
        implementation_path="2_products/pepper-agent/web/src/autonomy/assert_fixture.py",
    )
    candidate = build_tool_candidate(
        contract=contract,
        source_text=(
            "from pathlib import Path\n"
            "import sys\n"
            "text = Path(sys.argv[1]).read_text(encoding='utf-8')\n"
            "if 'render(<div>Pepper</div>)' not in text:\n"
            "    raise SystemExit(3)\n"
            "print('frontend-helper-ok')\n"
        ),
    )
    materialize_task_local_tool(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
    )
    proposal = propose_autonomy_command(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
        source_command=(
            "python 2_products/pepper-agent/web/src/autonomy/assert_fixture.py "
            f"{context['fixture_path']}"
        ),
        timeout_seconds=10,
    )
    evaluation = evaluate_autonomy_command(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
        proposal=proposal,
    )
    result = execute_autonomy_command(evaluation)
    assert gap.disposition is CapabilityGapDisposition.REPAIRABLE_TASK_LOCAL
    assert evaluation.decision is AutonomyCommandDecision.ALLOW
    assert result.disposition is AutonomyCommandDisposition.PASSED
    assert result.stdout.retained_text is not None
    assert "frontend-helper-ok" in result.stdout.retained_text


@pytest.mark.parametrize(
    ("requested_command", "expected_kind"),
    (
        ("git status", CapabilityGapKind.GIT_AUTHORITY_REQUIRED),
        ("python -m pip install pytest", CapabilityGapKind.PACKAGE_INSTALL_AUTHORITY_REQUIRED),
        ("curl https://example.invalid/data.json", CapabilityGapKind.NETWORK_AUTHORITY_REQUIRED),
        ("docker compose up", CapabilityGapKind.DOCKER_AUTHORITY_REQUIRED),
        ("graphify update .", CapabilityGapKind.GRAPHIFY_AUTHORITY_REQUIRED),
        (
            "python helper.py Authorization: Bearer abcdefghijklmnop",
            CapabilityGapKind.CREDENTIAL_AUTHORITY_REQUIRED,
        ),
    ),
)
def test_authority_required_gaps_do_not_self_repair(
    python_autonomy_context,
    requested_command: str,
    expected_kind: CapabilityGapKind,
) -> None:
    gap = classify_capability_gap(
        envelope=python_autonomy_context["envelope"],
        observed_failure="Worker requested authority outside the WorkPacket.",
        requested_capability="Need to continue execution.",
        requested_command=requested_command,
    )
    assert gap.kind is expected_kind
    assert gap.disposition is CapabilityGapDisposition.HUMAN_AUTHORITY_REQUIRED
    assert gap.requires_human_authority is True
    with pytest.raises(GovernedAutonomyPolicyError):
        build_task_local_capability_contract(
            envelope=python_autonomy_context["envelope"],
            gap=gap,
            tool_name="blocked_helper",
            language=TaskLocalToolLanguage.PYTHON,
            implementation_path="src/tools/blocked_helper.py",
        )


@pytest.mark.parametrize(
    ("source_command", "expected_reason"),
    (
        ("git status", AutonomyCommandDenialReason.GIT_AUTHORITY_REQUIRED),
        ("python -m pip install pytest", AutonomyCommandDenialReason.PACKAGE_INSTALL_AUTHORITY_REQUIRED),
        ("curl https://example.invalid", AutonomyCommandDenialReason.NETWORK_AUTHORITY_REQUIRED),
        ("graphify update .", AutonomyCommandDenialReason.GRAPHIFY_AUTHORITY_REQUIRED),
    ),
)
def test_command_evaluation_denies_authority_expansion(
    python_autonomy_context,
    source_command: str,
    expected_reason: AutonomyCommandDenialReason,
) -> None:
    envelope = python_autonomy_context["envelope"]
    _gap, contract, candidate = _python_contract_candidate(envelope)
    proposal = propose_autonomy_command(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
        source_command=source_command,
    )
    evaluation = evaluate_autonomy_command(
        envelope=envelope,
        contract=contract,
        candidate=candidate,
        proposal=proposal,
    )
    assert evaluation.decision is AutonomyCommandDecision.DENY
    assert evaluation.denial_reason is expected_reason
    assert evaluation.effective_argv == ()


@pytest.mark.parametrize(
    "implementation_path",
    (
        "src/node_modules/generated_helper.py",
        "src/package-lock.json",
        "graphify-out/generated_helper.py",
    ),
)
def test_task_local_contract_preserves_file_guard_scope(
    python_autonomy_context,
    implementation_path: str,
) -> None:
    envelope = python_autonomy_context["envelope"]
    gap = classify_capability_gap(
        envelope=envelope,
        observed_failure="missing helper",
        requested_capability="Need task-local helper.",
    )
    with pytest.raises(GovernedAutonomyPolicyError):
        build_task_local_capability_contract(
            envelope=envelope,
            gap=gap,
            tool_name="scope_guard",
            language=TaskLocalToolLanguage.PYTHON,
            implementation_path=implementation_path,
        )


def test_continuation_blocks_no_progress(python_autonomy_context) -> None:
    envelope = _envelope_from_context(
        python_autonomy_context,
        budget=GovernedAutonomyBudget(max_no_progress_iterations=2),
    )
    gap, _contract, _candidate = _python_contract_candidate(envelope)
    lineage = start_governed_autonomy_continuation(envelope=envelope, gap=gap)
    first = advance_governed_autonomy_continuation(
        envelope=envelope,
        lineage=lineage,
    )
    second = advance_governed_autonomy_continuation(
        envelope=envelope,
        lineage=first,
    )
    assert first.state is AutonomyContinuationState.CONTINUING
    assert second.state is AutonomyContinuationState.BLOCKED
    assert second.stop_reason is AutonomyContinuationStopReason.NO_PROGRESS


def test_continuation_blocks_budget_exhaustion(python_autonomy_context) -> None:
    envelope = _envelope_from_context(
        python_autonomy_context,
        budget=GovernedAutonomyBudget(max_tool_candidates=1, max_repair_attempts=1),
    )
    gap, _contract, candidate = _python_contract_candidate(envelope)
    lineage = start_governed_autonomy_continuation(envelope=envelope, gap=gap)
    first = advance_governed_autonomy_continuation(
        envelope=envelope,
        lineage=lineage,
        candidate=candidate,
        progress_marker="candidate-1",
    )
    second = advance_governed_autonomy_continuation(
        envelope=envelope,
        lineage=first,
        candidate=candidate,
        progress_marker="candidate-2",
    )
    assert first.state is AutonomyContinuationState.CONTINUING
    assert second.state is AutonomyContinuationState.BLOCKED
    assert second.stop_reason is AutonomyContinuationStopReason.BUDGET_EXHAUSTED


def test_continuation_revalidates_authority_envelope(python_autonomy_context) -> None:
    envelope = python_autonomy_context["envelope"]
    gap, _contract, _candidate = _python_contract_candidate(envelope)
    lineage = start_governed_autonomy_continuation(envelope=envelope, gap=gap)
    tampered = _construct_with_updates(envelope, work_packet_SHA256="0" * 64)
    with pytest.raises(GovernedAutonomyIntegrityError):
        advance_governed_autonomy_continuation(
            envelope=tampered,
            lineage=lineage,
            progress_marker="should-not-run",
        )


def test_live_activation_is_not_authorized(python_autonomy_context) -> None:
    envelope = python_autonomy_context["envelope"]
    assert envelope.live_lineage_activation_authorized is False
    assert envelope.provider_dispatch_count == 0
    assert envelope.model_inference_count == 0
