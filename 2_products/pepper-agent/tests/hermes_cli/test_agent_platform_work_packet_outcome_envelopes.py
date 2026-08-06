from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import get_origin
from unittest.mock import patch

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.outcome_envelopes as envelopes
import hermes_cli.agent_platform.work_packet.validation_command_runner as vcr
from hermes_cli.agent_platform.work_packet import (
    OUTCOME_ENVELOPE_POLICY_ID,
    OUTCOME_ENVELOPE_SCHEMA_VERSION,
    CancellationEnvelope,
    FailureEnvelope,
    OutcomeCancellationPoint,
    OutcomeDiagnosticProjection,
    OutcomeEnvelope,
    OutcomeEnvelopeInputError,
    OutcomeEnvelopeKind,
    OutcomeEnvelopeRequest,
    OutcomeEnvelopeStateError,
    OutcomeFailureCategory,
    OutcomeRetryPosture,
    OutcomeStage,
    OutcomeTerminalEvidence,
    OutcomeTerminalState,
    ResultEnvelope,
    SingleAgentActionExecutionRequest,
    SingleAgentExecutionRequest,
    ToolPermissionOperation,
    ValidationCommandDisposition,
    ValidationCommandExecutionRequest,
    ValidationCommandFailureReason,
    ValidationCommandRunnerState,
    build_single_agent_execution_authorization,
    build_cancellation_envelope,
    build_failure_envelope,
    build_outcome_envelope,
    build_result_envelope,
    complete_validation_command_runner,
    execute_single_agent_tool_action,
    execute_validation_command,
    prepare_single_agent_execution,
    prepare_validation_command_runner,
    validate_outcome_envelope,
    validate_outcome_envelope_request,
)
from tests.hermes_cli.test_agent_platform_work_packet_compiler import (
    EXPECTED_EXPORTS as P17_0_EXPORTS,
)
from tests.hermes_cli.test_agent_platform_work_packet_single_agent_execution import (
    P17_3_EXPORTS,
    basic_actions as single_agent_basic_actions,
    compilation_result as single_agent_compilation_result,
    execution_request as single_agent_execution_request,
    profile_result as single_agent_profile_result,
)
from tests.hermes_cli.test_agent_platform_work_packet_tool_permissions import (
    P17_1_EXPORTS,
    P17_2_EXPORTS,
)
from tests.hermes_cli.test_agent_platform_work_packet_validation_command_runner import (
    P17_4_EXPORTS,
    completed_single_agent_context,
)


P17_5_EXPORTS = (
    "OUTCOME_ENVELOPE_SCHEMA_VERSION",
    "OUTCOME_ENVELOPE_POLICY_ID",
    "OutcomeEnvelopeKind",
    "OutcomeStage",
    "OutcomeTerminalState",
    "OutcomeFailureCategory",
    "OutcomeRetryPosture",
    "OutcomeCancellationPoint",
    "OutcomeDiagnosticProjection",
    "OutcomeTerminalEvidence",
    "ResultEnvelope",
    "FailureEnvelope",
    "CancellationEnvelope",
    "OutcomeEnvelopeRequest",
    "OutcomeEnvelope",
    "OutcomeEnvelopeError",
    "OutcomeEnvelopeInputError",
    "OutcomeEnvelopeIntegrityError",
    "OutcomeEnvelopePolicyError",
    "OutcomeEnvelopeStateError",
    "OutcomeEnvelopeValidationError",
    "build_result_envelope",
    "build_failure_envelope",
    "build_cancellation_envelope",
    "build_outcome_envelope",
    "validate_outcome_envelope_request",
    "validate_outcome_envelope",
)
REQUIRED_MODEL_NAMES = (
    "OutcomeDiagnosticProjection",
    "OutcomeTerminalEvidence",
    "ResultEnvelope",
    "FailureEnvelope",
    "CancellationEnvelope",
    "OutcomeEnvelopeRequest",
    "OutcomeEnvelope",
)
REPLACEMENT_NAMES = (
    "WorkPacketOutcomeResultEnvelope",
    "WorkPacketOutcomeFailureEnvelope",
    "WorkPacketOutcomeCancellationEnvelope",
    "WorkPacketOutcomeEnvelope",
)
FORBIDDEN_PUBLIC_SYMBOLS = (
    "retry_work_packet",
    "resume_work_packet",
    "resubmit_work_packet",
    "execute_work_packet",
    "execute_tool",
    "OutcomeEnvelopeBuilder",
    "ResultEnvelopeBuilder",
    "FailureEnvelopeBuilder",
    "CancellationEnvelopeBuilder",
    "RetryManager",
    "ResubmissionManager",
    "DiffReviewer",
    "GitHandoff",
)
PUBLIC_MODELS = (
    OutcomeDiagnosticProjection,
    OutcomeTerminalEvidence,
    ResultEnvelope,
    FailureEnvelope,
    CancellationEnvelope,
    OutcomeEnvelopeRequest,
    OutcomeEnvelope,
)
CONTROLLED_ENUMS = (
    OutcomeEnvelopeKind,
    OutcomeStage,
    OutcomeTerminalState,
    OutcomeFailureCategory,
    OutcomeRetryPosture,
    OutcomeCancellationPoint,
)
FORBIDDEN_MODULE_NAMES = (
    "os",
    "pathlib",
    "subprocess",
    "threading",
    "time",
    "socket",
    "requests",
    "httpx",
    "openai",
    "docker",
    "git",
    "shutil",
    "tempfile",
    "datetime",
    "uuid",
    "random",
    "secrets",
    "asyncio",
    "multiprocessing",
    "concurrent",
)
AUTHORITY_SURFACE_NAMES = (
    "Popen",
    "Thread",
    "Process",
    "Pool",
    "Session",
    "Client",
    "AsyncClient",
    "OpenAI",
    "DockerClient",
    "Repo",
    "retry_work_packet",
    "resume_work_packet",
    "resubmit_work_packet",
    "execute_work_packet",
    "execute_tool",
    "inspect_human_provisioned_workspace",
    "evaluate_tool_permission",
    "open",
    "print",
    "compile",
    "eval",
    "exec",
)
COMMON_POSTURE_FIELDS = (
    "result_envelopes_ready",
    "diff_artifact_review_ready",
    "human_git_handoff_ready",
    "automatic_retry_authorized",
    "automatic_fallback_authorized",
    "automatic_resubmission_authorized",
    "provider_dispatch_count",
    "model_inference_count",
)
BOOLEAN_POSTURE_FIELDS = (
    "result_envelopes_ready",
    "diff_artifact_review_ready",
    "human_git_handoff_ready",
    "automatic_retry_authorized",
    "automatic_fallback_authorized",
    "automatic_resubmission_authorized",
)
DIGEST_FIELD_NAMES = (
    "diagnostic_SHA256",
    "terminal_evidence_SHA256",
    "envelope_SHA256",
    "request_SHA256",
)
EXPECTED_ENUM_VALUES = (
    (OutcomeEnvelopeKind, ("result", "failure", "cancellation")),
    (OutcomeStage, ("single_agent_execution", "validation_command_runner")),
    (OutcomeTerminalState, ("completed", "blocked", "cancelled")),
    (
        OutcomeFailureCategory,
        (
            "none",
            "single_agent_blocked",
            "single_agent_action_denied",
            "validation_command_nonzero_exit",
            "validation_command_timeout",
            "validation_command_output_limit",
            "validation_command_launch_error",
        ),
    ),
    (OutcomeRetryPosture, ("not_authorized",)),
    (
        OutcomeCancellationPoint,
        ("none", "single_agent_before_action", "validation_command_prelaunch"),
    ),
)
EXPECTED_FUNCTION_NAMES = (
    (build_result_envelope, "build_result_envelope"),
    (build_failure_envelope, "build_failure_envelope"),
    (build_cancellation_envelope, "build_cancellation_envelope"),
    (build_outcome_envelope, "build_outcome_envelope"),
    (validate_outcome_envelope_request, "validate_outcome_envelope_request"),
    (validate_outcome_envelope, "validate_outcome_envelope"),
)


class FakeProcess:
    def __init__(self, stdout: bytes = b"", stderr: bytes = b"", code: int = 0) -> None:
        self.stdout = BytesIO(stdout)
        self.stderr = BytesIO(stderr)
        self.code = code
        self.terminated = False
        self.killed = False

    def poll(self):
        return self.code

    def wait(self):
        self.terminated = True
        return self.code

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True


def completed_validation_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = completed_single_agent_context(monkeypatch, tmp_path)
    session = prepare_validation_command_runner(context["runner_request"])
    first = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=context["runner_request"],
            session=session,
        )
    )
    second = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=context["runner_request"],
            session=first.updated_session,
        )
    )
    result = complete_validation_command_runner(second.updated_session)
    context["first"] = first
    context["second"] = second
    context["result"] = result
    return context


def single_agent_denied_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    compilation = single_agent_compilation_result()
    actions = single_agent_basic_actions(compilation)
    context = single_agent_execution_request(monkeypatch, tmp_path, actions)
    denied_profile = single_agent_profile_result(
        context["compilation_result"],
        context["allocation_result"],
        operations=(ToolPermissionOperation.READ_FILE,),
    )
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-5",
        authorization_reference="AUTH-P17-5-DENIED",
        rationale="Authorize externally supplied plan against denied profile.",
        compilation_result=context["compilation_result"],
        allocation_result=context["allocation_result"],
        profile_result=denied_profile,
        runtime_binding=context["binding"],
        plan=context["plan"],
        risk_acknowledgement="Synthetic denied-action risk acknowledged.",
    )
    context["request"] = SingleAgentExecutionRequest(
        compilation_result=context["compilation_result"],
        allocation_result=context["allocation_result"],
        profile_result=denied_profile,
        runtime_binding=context["binding"],
        plan=context["plan"],
        execution_authorization=authorization,
    )
    session = prepare_single_agent_execution(context["request"])
    result = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(
            execution_request=context["request"],
            session=session,
        )
    )
    context["blocked"] = result
    return context


def validation_launch_result(
    *,
    exit_code: int | None,
    process_started: bool,
    terminate_requested: bool,
    kill_requested: bool,
    timed_out: bool,
    output_limit_exceeded: bool,
    launch_failed: bool,
) -> vcr._LaunchResult:
    return vcr._LaunchResult(
        exit_code=exit_code,
        stdout_raw=b"bounded stdout",
        stderr_raw=b"bounded stderr",
        process_started=process_started,
        terminate_requested=terminate_requested,
        kill_requested=kill_requested,
        timed_out=timed_out,
        output_limit_exceeded=output_limit_exceeded,
        launch_failed=launch_failed,
    )


def validation_failure_context(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    category: OutcomeFailureCategory,
):
    context = completed_single_agent_context(
        monkeypatch,
        tmp_path,
        commands=("python -m unittest no_such_test",),
    )
    if category is OutcomeFailureCategory.VALIDATION_COMMAND_TIMEOUT:
        monkeypatch.setattr(
            vcr,
            "_launch_and_capture",
            lambda specification, environment: validation_launch_result(
                exit_code=None,
                process_started=True,
                terminate_requested=True,
                kill_requested=False,
                timed_out=True,
                output_limit_exceeded=False,
                launch_failed=False,
            ),
        )
    elif category is OutcomeFailureCategory.VALIDATION_COMMAND_OUTPUT_LIMIT:
        monkeypatch.setattr(
            vcr,
            "_launch_and_capture",
            lambda specification, environment: validation_launch_result(
                exit_code=None,
                process_started=True,
                terminate_requested=True,
                kill_requested=True,
                timed_out=False,
                output_limit_exceeded=True,
                launch_failed=False,
            ),
        )
    elif category is OutcomeFailureCategory.VALIDATION_COMMAND_LAUNCH_ERROR:
        monkeypatch.setattr(
            vcr,
            "_launch_and_capture",
            lambda specification, environment: validation_launch_result(
                exit_code=None,
                process_started=False,
                terminate_requested=False,
                kill_requested=False,
                timed_out=False,
                output_limit_exceeded=False,
                launch_failed=True,
            ),
        )
    session = prepare_validation_command_runner(context["runner_request"])
    failed = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=context["runner_request"],
            session=session,
        )
    )
    context["failed"] = failed
    return context


@pytest.fixture()
def result_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = completed_validation_context(monkeypatch, tmp_path / "result")
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_result=context["result"],
    )
    outcome = build_outcome_envelope(request)
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["result_envelope"] = outcome.result_envelope
    return context


@pytest.fixture()
def p17_3_failure_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = single_agent_denied_context(monkeypatch, tmp_path / "p17-3-failure")
    request = envelopes._outcome_request(
        single_agent_execution_session=context["blocked"].updated_session,
    )
    outcome = build_outcome_envelope(request)
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["failure_envelope"] = outcome.failure_envelope
    return context


@pytest.fixture()
def p17_3_cancellation_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    compilation = single_agent_compilation_result()
    context = single_agent_execution_request(
        monkeypatch,
        tmp_path / "p17-3-cancel",
        single_agent_basic_actions(compilation),
    )
    session = prepare_single_agent_execution(context["request"])
    cancelled = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(
            execution_request=context["request"],
            session=session,
            cancellation_requested=True,
            cancellation_reference="CANCEL-P17-5",
        )
    )
    request = envelopes._outcome_request(
        single_agent_execution_session=cancelled.updated_session,
        cancellation_reference="CANCEL-P17-5",
    )
    outcome = build_outcome_envelope(request)
    context["cancelled"] = cancelled
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["cancellation_envelope"] = outcome.cancellation_envelope
    return context


@pytest.fixture()
def p17_4_nonzero_failure_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = validation_failure_context(
        monkeypatch,
        tmp_path / "p17-4-nonzero",
        category=OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT,
    )
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_session=context["failed"].updated_session,
    )
    outcome = build_outcome_envelope(request)
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["failure_envelope"] = outcome.failure_envelope
    return context


@pytest.fixture()
def p17_4_timeout_failure_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = validation_failure_context(
        monkeypatch,
        tmp_path / "p17-4-timeout",
        category=OutcomeFailureCategory.VALIDATION_COMMAND_TIMEOUT,
    )
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_session=context["failed"].updated_session,
    )
    outcome = build_outcome_envelope(request)
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["failure_envelope"] = outcome.failure_envelope
    return context


@pytest.fixture()
def p17_4_output_limit_failure_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = validation_failure_context(
        monkeypatch,
        tmp_path / "p17-4-output-limit",
        category=OutcomeFailureCategory.VALIDATION_COMMAND_OUTPUT_LIMIT,
    )
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_session=context["failed"].updated_session,
    )
    outcome = build_outcome_envelope(request)
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["failure_envelope"] = outcome.failure_envelope
    return context


@pytest.fixture()
def p17_4_launch_failure_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = validation_failure_context(
        monkeypatch,
        tmp_path / "p17-4-launch",
        category=OutcomeFailureCategory.VALIDATION_COMMAND_LAUNCH_ERROR,
    )
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_session=context["failed"].updated_session,
    )
    outcome = build_outcome_envelope(request)
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["failure_envelope"] = outcome.failure_envelope
    return context


@pytest.fixture()
def p17_4_cancellation_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = completed_single_agent_context(monkeypatch, tmp_path / "p17-4-cancel")
    session = prepare_validation_command_runner(context["runner_request"])
    with patch.object(vcr.subprocess, "Popen", side_effect=AssertionError("process")):
        cancelled = execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=context["runner_request"],
                session=session,
                cancellation_requested=True,
                cancellation_reference="CANCEL-P17-5",
            )
        )
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_session=cancelled.updated_session,
        cancellation_reference="CANCEL-P17-5",
    )
    outcome = build_outcome_envelope(request)
    context["cancelled"] = cancelled
    context["outcome_request"] = request
    context["outcome"] = outcome
    context["cancellation_envelope"] = outcome.cancellation_envelope
    return context


@pytest.fixture()
def sample_models(
    result_context,
    p17_3_failure_context,
    p17_4_cancellation_context,
):
    return {
        OutcomeDiagnosticProjection.__name__: result_context[
            "result_envelope"
        ].diagnostic_projection,
        OutcomeTerminalEvidence.__name__: result_context[
            "result_envelope"
        ].terminal_evidence,
        ResultEnvelope.__name__: result_context["result_envelope"],
        FailureEnvelope.__name__: p17_3_failure_context["failure_envelope"],
        CancellationEnvelope.__name__: p17_4_cancellation_context[
            "cancellation_envelope"
        ],
        OutcomeEnvelopeRequest.__name__: result_context["outcome_request"],
        OutcomeEnvelope.__name__: result_context["outcome"],
    }


@pytest.mark.parametrize("exported_name", P17_5_EXPORTS)
def test_exact_p17_5_exports_are_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


def test_prior_145_exports_remain_exact_prefix() -> None:
    prior = P17_0_EXPORTS + P17_1_EXPORTS + P17_2_EXPORTS + P17_3_EXPORTS
    prior = prior + P17_4_EXPORTS
    assert len(prior) == 145
    assert work_packet.__all__[:145] == prior
    assert work_packet.__all__[145:] == P17_5_EXPORTS
    assert len(work_packet.__all__) == 172
    assert len(set(work_packet.__all__)) == 172
    assert not any(name.startswith("_") for name in work_packet.__all__)


def test_required_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        hasattr(work_packet, "OutcomeEnvelope"),
        hasattr(work_packet, "build_outcome_envelope"),
        hasattr(work_packet, "retry_work_packet"),
        hasattr(work_packet, "OutcomeEnvelopeBuilder"),
    ) == (172, 172, True, True, False, False)


def test_required_function_import_smoke_exact_output() -> None:
    assert tuple(function.__name__ for function, _ in EXPECTED_FUNCTION_NAMES) == tuple(
        expected for _, expected in EXPECTED_FUNCTION_NAMES
    )


@pytest.mark.parametrize("model_name", REQUIRED_MODEL_NAMES)
def test_required_model_names_are_public(model_name: str) -> None:
    assert hasattr(work_packet, model_name)
    assert hasattr(envelopes, model_name)


@pytest.mark.parametrize("replacement_name", REPLACEMENT_NAMES)
def test_replacement_public_names_are_absent(replacement_name: str) -> None:
    assert not hasattr(work_packet, replacement_name)
    assert not hasattr(envelopes, replacement_name)


@pytest.mark.parametrize("forbidden_name", FORBIDDEN_PUBLIC_SYMBOLS)
def test_forbidden_public_symbols_absent_from_package(forbidden_name: str) -> None:
    assert not hasattr(work_packet, forbidden_name)


@pytest.mark.parametrize("forbidden_name", FORBIDDEN_PUBLIC_SYMBOLS)
def test_forbidden_public_symbols_absent_from_module(forbidden_name: str) -> None:
    assert not hasattr(envelopes, forbidden_name)


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
def test_public_models_json_round_trip(
    model_cls: type[BaseModel], sample_models
) -> None:
    model = sample_models[model_cls.__name__]
    assert model_cls.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_immutable(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    first_field = next(iter(model.model_fields))
    with pytest.raises(ValidationError):
        setattr(model, first_field, getattr(model, first_field))


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_unknown_fields_are_rejected(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["unknown"] = "blocked"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_alternative_schema_versions_are_rejected(
    model_cls: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_tuple_fields_round_trip_as_tuples(
    model_cls: type[BaseModel], sample_models
) -> None:
    model = sample_models[model_cls.__name__]
    for name, field in model.model_fields.items():
        if get_origin(field.annotation) is tuple:
            assert isinstance(getattr(model, name), tuple)


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_controlled_enums_have_no_aliases(enum_cls: type) -> None:
    assert len(enum_cls) == len({item.value for item in enum_cls})


@pytest.mark.parametrize("enum_cls,expected", EXPECTED_ENUM_VALUES)
def test_controlled_enum_values_are_exact(
    enum_cls: type, expected: tuple[str, ...]
) -> None:
    assert tuple(item.value for item in enum_cls) == expected


@pytest.mark.parametrize("function,expected", EXPECTED_FUNCTION_NAMES)
def test_public_builder_and_validator_names_are_exact(function, expected: str) -> None:
    assert function.__name__ == expected


def test_canonical_completed_execution_result_envelope_flow(result_context) -> None:
    envelope = result_context["result_envelope"]
    outcome = result_context["outcome"]
    assert outcome.envelope_kind is OutcomeEnvelopeKind.RESULT
    assert envelope.envelope_kind is OutcomeEnvelopeKind.RESULT
    assert envelope.diagnostic_projection.terminal_stage is (
        OutcomeStage.VALIDATION_COMMAND_RUNNER
    )
    assert (
        envelope.diagnostic_projection.terminal_state is OutcomeTerminalState.COMPLETED
    )
    assert envelope.terminal_evidence.terminal_state is OutcomeTerminalState.COMPLETED
    assert (
        envelope.completed_task_step_ids
        == result_context["single_result"].completed_task_step_ids
    )
    assert envelope.passed_validation_ids == ("V1", "V3")
    assert envelope.manual_validation_ids_pending == ("V2",)
    assert envelope.result_envelopes_ready is True
    assert envelope.diff_artifact_review_ready is False
    assert envelope.human_git_handoff_ready is False
    assert envelope.automatic_retry_authorized is False
    assert envelope.automatic_fallback_authorized is False
    assert envelope.automatic_resubmission_authorized is False
    assert envelope.provider_dispatch_count == 0
    assert envelope.model_inference_count == 0
    validate_outcome_envelope_request(result_context["outcome_request"])
    validate_outcome_envelope(outcome)


def test_canonical_validation_failure_envelope_flow(
    p17_4_nonzero_failure_context,
) -> None:
    failed = p17_4_nonzero_failure_context["failed"]
    envelope = p17_4_nonzero_failure_context["failure_envelope"]
    assert failed.disposition is ValidationCommandDisposition.FAILED
    assert (
        failed.updated_session.command_evidence[-1].failure_reason
        is ValidationCommandFailureReason.NONZERO_EXIT
    )
    assert envelope.envelope_kind is OutcomeEnvelopeKind.FAILURE
    assert envelope.failure_category is (
        OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT
    )
    assert envelope.terminal_evidence.terminal_state is OutcomeTerminalState.BLOCKED
    assert envelope.failed_command_id == "VCMD-001"
    assert envelope.failed_validation_id == "V1"
    assert (
        envelope.single_agent_result_SHA256
        == p17_4_nonzero_failure_context["single_result"].result_SHA256
    )


def test_canonical_prelaunch_cancellation_envelope_flow(
    p17_4_cancellation_context,
) -> None:
    cancelled = p17_4_cancellation_context["cancelled"]
    envelope = p17_4_cancellation_context["cancellation_envelope"]
    assert cancelled.updated_session.state is ValidationCommandRunnerState.CANCELLED
    assert envelope.envelope_kind is OutcomeEnvelopeKind.CANCELLATION
    assert (
        envelope.cancellation_point
        is OutcomeCancellationPoint.VALIDATION_COMMAND_PRELAUNCH
    )
    assert envelope.process_started is False
    assert envelope.terminal_evidence.process_started is False
    assert envelope.cancelled_command_id == "VCMD-001"
    assert envelope.cancelled_validation_id == "V1"


def test_p17_3_failure_envelope_uses_actual_denied_disposition(
    p17_3_failure_context,
) -> None:
    envelope = p17_3_failure_context["failure_envelope"]
    assert envelope.envelope_kind is OutcomeEnvelopeKind.FAILURE
    assert (
        envelope.failure_category is OutcomeFailureCategory.SINGLE_AGENT_ACTION_DENIED
    )
    assert (
        envelope.terminal_evidence.terminal_stage is OutcomeStage.SINGLE_AGENT_EXECUTION
    )
    assert envelope.terminal_evidence.terminal_disposition == "denied"
    assert envelope.failed_action_id == "ACTION-001"
    assert envelope.failed_task_step_id
    assert envelope.single_agent_result_SHA256 is None


def test_p17_3_cancellation_envelope_uses_actual_cancelled_disposition(
    p17_3_cancellation_context,
) -> None:
    envelope = p17_3_cancellation_context["cancellation_envelope"]
    assert envelope.envelope_kind is OutcomeEnvelopeKind.CANCELLATION
    assert (
        envelope.cancellation_point
        is OutcomeCancellationPoint.SINGLE_AGENT_BEFORE_ACTION
    )
    assert (
        envelope.terminal_evidence.terminal_stage is OutcomeStage.SINGLE_AGENT_EXECUTION
    )
    assert envelope.terminal_evidence.terminal_disposition == "cancelled"
    assert envelope.cancelled_action_id == "ACTION-001"
    assert envelope.process_started is False


@pytest.mark.parametrize(
    "fixture_name,category",
    (
        (
            "p17_4_nonzero_failure_context",
            OutcomeFailureCategory.VALIDATION_COMMAND_NONZERO_EXIT,
        ),
        (
            "p17_4_timeout_failure_context",
            OutcomeFailureCategory.VALIDATION_COMMAND_TIMEOUT,
        ),
        (
            "p17_4_output_limit_failure_context",
            OutcomeFailureCategory.VALIDATION_COMMAND_OUTPUT_LIMIT,
        ),
        (
            "p17_4_launch_failure_context",
            OutcomeFailureCategory.VALIDATION_COMMAND_LAUNCH_ERROR,
        ),
    ),
)
def test_p17_4_failure_categories_are_projected(
    request: pytest.FixtureRequest,
    fixture_name: str,
    category: OutcomeFailureCategory,
) -> None:
    context = request.getfixturevalue(fixture_name)
    envelope = context["failure_envelope"]
    assert envelope.failure_category is category
    assert envelope.diagnostic_projection.failure_category is category
    assert envelope.terminal_evidence.failure_category is category
    assert envelope.terminal_evidence.terminal_state is OutcomeTerminalState.BLOCKED


@pytest.mark.parametrize(
    "fixture_name,expected_kind",
    (
        ("result_context", OutcomeEnvelopeKind.RESULT),
        ("p17_3_failure_context", OutcomeEnvelopeKind.FAILURE),
        ("p17_3_cancellation_context", OutcomeEnvelopeKind.CANCELLATION),
        ("p17_4_nonzero_failure_context", OutcomeEnvelopeKind.FAILURE),
        ("p17_4_timeout_failure_context", OutcomeEnvelopeKind.FAILURE),
        ("p17_4_output_limit_failure_context", OutcomeEnvelopeKind.FAILURE),
        ("p17_4_launch_failure_context", OutcomeEnvelopeKind.FAILURE),
        ("p17_4_cancellation_context", OutcomeEnvelopeKind.CANCELLATION),
    ),
)
def test_outcome_wrapper_selects_exactly_one_envelope(
    request: pytest.FixtureRequest,
    fixture_name: str,
    expected_kind: OutcomeEnvelopeKind,
) -> None:
    outcome = request.getfixturevalue(fixture_name)["outcome"]
    present = tuple(
        item
        for item in (
            outcome.result_envelope,
            outcome.failure_envelope,
            outcome.cancellation_envelope,
        )
        if item is not None
    )
    assert outcome.envelope_kind is expected_kind
    assert len(present) == 1
    assert present[0].envelope_kind is expected_kind


@pytest.mark.parametrize("field", COMMON_POSTURE_FIELDS)
@pytest.mark.parametrize(
    "fixture_name",
    (
        "result_context",
        "p17_3_failure_context",
        "p17_3_cancellation_context",
        "p17_4_nonzero_failure_context",
        "p17_4_timeout_failure_context",
        "p17_4_output_limit_failure_context",
        "p17_4_launch_failure_context",
        "p17_4_cancellation_context",
    ),
)
def test_common_posture_fields_are_bounded(
    request: pytest.FixtureRequest,
    fixture_name: str,
    field: str,
) -> None:
    outcome = request.getfixturevalue(fixture_name)["outcome"]
    selected = envelopes._selected_envelope(outcome)
    value = getattr(selected, field)
    if field == "result_envelopes_ready":
        assert value is True
    elif field.endswith("count"):
        assert value == 0
    else:
        assert value is False


@pytest.mark.parametrize("field", BOOLEAN_POSTURE_FIELDS)
@pytest.mark.parametrize(
    "model_name", ("ResultEnvelope", "FailureEnvelope", "CancellationEnvelope")
)
def test_boolean_posture_fields_reject_strings(
    result_context,
    p17_3_failure_context,
    p17_4_cancellation_context,
    model_name: str,
    field: str,
) -> None:
    samples = {
        "ResultEnvelope": result_context["result_envelope"],
        "FailureEnvelope": p17_3_failure_context["failure_envelope"],
        "CancellationEnvelope": p17_4_cancellation_context["cancellation_envelope"],
    }
    model = samples[model_name]
    data = model.model_dump(mode="json")
    if field not in data:
        return
    data[field] = "true" if field == "result_envelopes_ready" else "false"
    with pytest.raises(ValidationError):
        type(model).model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_policy_id_is_exact(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    if "policy_id" in model.model_fields:
        assert (
            model.policy_id
            == "pepper-deterministic-bounded-terminal-outcome-envelopes-v1"
        )


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_models_have_no_mutable_defaults(model_cls: type[BaseModel]) -> None:
    for field in model_cls.model_fields.values():
        assert not isinstance(field.default, list | dict | set)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_have_no_runtime_handle_schema_fields(
    model_cls: type[BaseModel],
) -> None:
    for field in model_cls.model_fields.values():
        annotation_text = str(field.annotation).casefold()
        for marker in ("popen", "thread", "bytes", "callable", "mapping", "object"):
            assert marker not in annotation_text


@pytest.mark.parametrize("field", DIGEST_FIELD_NAMES)
@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_digest_tampering_is_rejected(
    model_cls: type[BaseModel], sample_models, field: str
) -> None:
    model = sample_models[model_cls.__name__]
    if field not in model.model_fields:
        return
    data = model.model_dump(mode="json")
    data[field] = "0" * 64
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize(
    "field,value",
    (
        ("envelope_id", "OE-RESULT-deadbeefdeadbeef"),
        ("passed_validation_ids", ("V3", "V1")),
        ("manual_validation_ids_pending", ("V2", "V2")),
        ("single_agent_result_SHA256", "0" * 64),
        ("validation_command_runner_result_SHA256", "0" * 64),
    ),
)
def test_result_envelope_invariant_tampering_is_rejected(
    result_context, field: str, value
) -> None:
    data = result_context["result_envelope"].model_dump(mode="json")
    data[field] = value
    with pytest.raises(ValidationError):
        ResultEnvelope.model_validate(data)


@pytest.mark.parametrize(
    "field,value",
    (
        ("failure_category", "none"),
        ("failed_action_id", "ACTION-999"),
        ("single_agent_session_SHA256", "0" * 64),
        ("result_envelopes_ready", False),
        ("automatic_retry_authorized", True),
    ),
)
def test_failure_envelope_invariant_tampering_is_rejected(
    p17_3_failure_context, field: str, value
) -> None:
    data = p17_3_failure_context["failure_envelope"].model_dump(mode="json")
    data[field] = value
    with pytest.raises(ValidationError):
        FailureEnvelope.model_validate(data)


@pytest.mark.parametrize(
    "field,value",
    (
        ("cancellation_point", "none"),
        ("process_started", True),
        ("cancelled_command_id", "VCMD-999"),
        ("validation_command_runner_session_SHA256", "0" * 64),
        ("automatic_resubmission_authorized", True),
    ),
)
def test_cancellation_envelope_invariant_tampering_is_rejected(
    p17_4_cancellation_context, field: str, value
) -> None:
    data = p17_4_cancellation_context["cancellation_envelope"].model_dump(mode="json")
    data[field] = value
    with pytest.raises(ValidationError):
        CancellationEnvelope.model_validate(data)


def test_result_builder_is_deterministic(result_context) -> None:
    first = build_result_envelope(
        single_agent_execution_result=result_context["single_result"],
        validation_command_runner_result=result_context["result"],
    )
    second = build_result_envelope(
        single_agent_execution_result=result_context["single_result"],
        validation_command_runner_result=result_context["result"],
    )
    assert first == second
    assert first.envelope_id == second.envelope_id
    assert first.envelope_SHA256 == second.envelope_SHA256


def test_failure_builder_is_deterministic(p17_4_nonzero_failure_context) -> None:
    first = build_failure_envelope(
        validation_command_runner_session=p17_4_nonzero_failure_context[
            "failed"
        ].updated_session,
        single_agent_execution_result=p17_4_nonzero_failure_context["single_result"],
    )
    second = build_failure_envelope(
        validation_command_runner_session=p17_4_nonzero_failure_context[
            "failed"
        ].updated_session,
        single_agent_execution_result=p17_4_nonzero_failure_context["single_result"],
    )
    assert first == second
    assert first.envelope_id == second.envelope_id
    assert first.envelope_SHA256 == second.envelope_SHA256


def test_cancellation_builder_is_deterministic(p17_4_cancellation_context) -> None:
    first = build_cancellation_envelope(
        validation_command_runner_session=p17_4_cancellation_context[
            "cancelled"
        ].updated_session,
        single_agent_execution_result=p17_4_cancellation_context["single_result"],
        cancellation_reference="CANCEL-P17-5",
    )
    second = build_cancellation_envelope(
        validation_command_runner_session=p17_4_cancellation_context[
            "cancelled"
        ].updated_session,
        single_agent_execution_result=p17_4_cancellation_context["single_result"],
        cancellation_reference="CANCEL-P17-5",
    )
    assert first == second
    assert first.envelope_id == second.envelope_id
    assert first.envelope_SHA256 == second.envelope_SHA256


def test_completed_result_projection_requires_bound_single_agent_result(
    result_context,
) -> None:
    with pytest.raises(OutcomeEnvelopeInputError):
        build_result_envelope(
            single_agent_execution_result=result_context["single_result"].model_copy(
                update={"result_SHA256": "0" * 64}
            ),
            validation_command_runner_result=result_context["result"],
        )


def test_validation_failure_projection_checks_optional_single_result_binding(
    p17_4_nonzero_failure_context,
) -> None:
    with pytest.raises(OutcomeEnvelopeInputError):
        build_failure_envelope(
            validation_command_runner_session=p17_4_nonzero_failure_context[
                "failed"
            ].updated_session,
            single_agent_execution_result=p17_4_nonzero_failure_context[
                "single_result"
            ].model_copy(update={"result_SHA256": "0" * 64}),
        )


def test_validation_cancellation_projection_checks_optional_single_result_binding(
    p17_4_cancellation_context,
) -> None:
    with pytest.raises(OutcomeEnvelopeInputError):
        build_cancellation_envelope(
            validation_command_runner_session=p17_4_cancellation_context[
                "cancelled"
            ].updated_session,
            single_agent_execution_result=p17_4_cancellation_context[
                "single_result"
            ].model_copy(update={"result_SHA256": "0" * 64}),
        )


def test_non_terminal_validation_session_is_rejected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    context = completed_single_agent_context(monkeypatch, tmp_path / "non-terminal-vcr")
    session = prepare_validation_command_runner(context["runner_request"])
    request = envelopes._outcome_request(
        single_agent_execution_result=context["single_result"],
        validation_command_runner_session=session,
    )
    with pytest.raises(OutcomeEnvelopeStateError):
        build_outcome_envelope(request)


def test_non_terminal_single_agent_session_is_rejected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    compilation = single_agent_compilation_result()
    context = single_agent_execution_request(
        monkeypatch,
        tmp_path / "non-terminal-single-agent",
        single_agent_basic_actions(compilation),
    )
    session = prepare_single_agent_execution(context["request"])
    request = envelopes._outcome_request(single_agent_execution_session=session)
    with pytest.raises(OutcomeEnvelopeStateError):
        build_outcome_envelope(request)


@pytest.mark.parametrize(
    "updates",
    (
        {},
        {"single_agent_execution_session": "also-present"},
        {"validation_command_runner_session": "also-present"},
        {"validation_command_runner_result": "also-present"},
    ),
)
def test_invalid_request_shapes_are_rejected(
    result_context, updates: dict[str, object]
) -> None:
    data = result_context["outcome_request"].model_dump(mode="json")
    if not updates:
        data.update(
            single_agent_execution_result=None,
            validation_command_runner_result=None,
            request_SHA256="0" * 64,
        )
    else:
        data.update(updates)
        data["request_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        OutcomeEnvelopeRequest.model_validate(data)


def test_wrapper_with_multiple_selected_envelopes_is_rejected(
    result_context,
    p17_3_failure_context,
) -> None:
    data = result_context["outcome"].model_dump(mode="json")
    data["failure_envelope"] = p17_3_failure_context["failure_envelope"].model_dump(
        mode="json"
    )
    with pytest.raises(ValidationError):
        OutcomeEnvelope.model_validate(data)


def test_final_result_contains_no_raw_or_retained_stream_text(result_context) -> None:
    dumped = result_context["outcome"].model_dump_json()
    assert "retained_text" not in dumped
    assert "bounded stdout" not in dumped
    assert "bounded stderr" not in dumped
    assert "usage: python" not in dumped


@pytest.mark.parametrize("module_name", FORBIDDEN_MODULE_NAMES)
def test_forbidden_authority_modules_are_not_imported(module_name: str) -> None:
    assert not hasattr(envelopes, module_name)


@pytest.mark.parametrize("surface_name", AUTHORITY_SURFACE_NAMES)
def test_no_execution_retry_or_git_surface(surface_name: str) -> None:
    assert not hasattr(envelopes, surface_name)


def test_projection_import_has_no_process_or_filesystem_authority() -> None:
    assert not hasattr(envelopes, "subprocess")
    assert not hasattr(envelopes, "Path")
    assert not hasattr(envelopes, "os")
    assert not hasattr(envelopes, "threading")
    assert not hasattr(envelopes, "inspect_human_provisioned_workspace")


@pytest.mark.parametrize(
    "counter_name",
    (
        "subprocess_launches",
        "threads_created",
        "filesystem_reads",
        "filesystem_writes",
        "workspace_inspections",
        "environment_reads",
        "network_calls",
        "provider_calls",
        "model_calls",
        "Git_commands",
        "Docker_calls",
        "Graphify_calls",
        "automatic_retries",
        "automatic_fallbacks",
        "automatic_resubmissions",
    ),
)
def test_authority_counter_contract_is_zero(result_context, counter_name: str) -> None:
    _ = counter_name
    envelope = result_context["result_envelope"]
    assert envelope.provider_dispatch_count == 0
    assert envelope.model_inference_count == 0
    assert envelope.automatic_retry_authorized is False
    assert envelope.automatic_fallback_authorized is False
    assert envelope.automatic_resubmission_authorized is False


@pytest.mark.parametrize(
    "forbidden",
    (
        "shell",
        "powershell",
        "cmd.exe",
        "bash",
        "git ",
        "docker",
        "graphify",
        "provider_dispatch",
        "model_inference",
        "credential",
        "socket",
        "retry_work_packet",
        "resubmit_work_packet",
        "OutcomeEnvelopeBuilder",
        "git add",
        "git commit",
        "git push",
    ),
)
def test_authority_boundary_forbidden_text_not_in_public_api(forbidden: str) -> None:
    public_names = " ".join(work_packet.__all__).casefold()
    assert forbidden.casefold() not in public_names
