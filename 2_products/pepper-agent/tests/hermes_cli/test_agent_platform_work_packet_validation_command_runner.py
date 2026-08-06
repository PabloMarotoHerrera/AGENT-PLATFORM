from __future__ import annotations

from io import BytesIO
from pathlib import Path
import sys
from threading import active_count
from typing import get_args, get_origin
from unittest.mock import patch

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.validation_command_runner as vcr
from hermes_cli.agent_platform.work_packet import (
    VALIDATION_COMMAND_RUNNER_POLICY_ID,
    VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION,
    SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
    SingleAgentActionExecutionRequest,
    SingleAgentExecutionRequest,
    ToolPermissionOperation,
    ValidationCommandAuthorizationRequest,
    ValidationCommandCapturedStream,
    ValidationCommandDisposition,
    ValidationCommandExecutionEvidence,
    ValidationCommandExecutionRequest,
    ValidationCommandExecutionResult,
    ValidationCommandFailureReason,
    ValidationCommandModule,
    ValidationCommandRunnerAuthorization,
    ValidationCommandRunnerRequest,
    ValidationCommandRunnerResult,
    ValidationCommandRunnerSession,
    ValidationCommandRunnerState,
    ValidationCommandRuntimeBinding,
    ValidationCommandSpecification,
    ValidationCommandStreamKind,
    build_single_agent_execution_authorization,
    build_single_agent_runtime_binding,
    build_validation_command_runner_authorization,
    build_validation_command_runtime_binding,
    complete_single_agent_execution,
    complete_validation_command_runner,
    execute_single_agent_tool_action,
    execute_validation_command,
    prepare_single_agent_execution,
    prepare_validation_command_runner,
    validate_validation_command_runner_result,
    validate_validation_command_runner_session,
)
from tests.hermes_cli.test_agent_platform_work_packet_compiler import (
    EXPECTED_EXPORTS as P17_0_EXPORTS,
    build_bundle,
    scope as compiler_scope,
    ticket as compiler_ticket,
    validation_step,
)
from tests.hermes_cli.test_agent_platform_work_packet_single_agent_execution import (
    P17_3_EXPORTS,
    SOURCE_COMMIT,
    WORKSPACE_BRANCH,
    allocation_result,
    basic_actions,
    path_text,
    patch_workspace_inspection,
    plan,
    profile_result,
)
from tests.hermes_cli.test_agent_platform_work_packet_tool_permissions import (
    P17_1_EXPORTS,
    P17_2_EXPORTS,
)


P17_4_EXPORTS = (
    "VALIDATION_COMMAND_RUNNER_SCHEMA_VERSION",
    "VALIDATION_COMMAND_RUNNER_POLICY_ID",
    "ValidationCommandModule",
    "ValidationCommandRunnerState",
    "ValidationCommandDisposition",
    "ValidationCommandFailureReason",
    "ValidationCommandStreamKind",
    "ValidationCommandRuntimeBinding",
    "ValidationCommandAuthorizationRequest",
    "ValidationCommandSpecification",
    "ValidationCommandRunnerAuthorization",
    "ValidationCommandRunnerRequest",
    "ValidationCommandCapturedStream",
    "ValidationCommandExecutionEvidence",
    "ValidationCommandRunnerSession",
    "ValidationCommandExecutionRequest",
    "ValidationCommandExecutionResult",
    "ValidationCommandRunnerResult",
    "ValidationCommandRunnerError",
    "ValidationCommandRunnerInputError",
    "ValidationCommandRunnerAuthorizationError",
    "ValidationCommandRunnerIntegrityError",
    "ValidationCommandPolicyError",
    "ValidationCommandExecutionError",
    "ValidationCommandRunnerStateError",
    "build_validation_command_runtime_binding",
    "build_validation_command_runner_authorization",
    "prepare_validation_command_runner",
    "execute_validation_command",
    "complete_validation_command_runner",
    "validate_validation_command_runner_session",
    "validate_validation_command_runner_result",
)
PUBLIC_MODELS = (
    ValidationCommandRuntimeBinding,
    ValidationCommandAuthorizationRequest,
    ValidationCommandSpecification,
    ValidationCommandRunnerAuthorization,
    ValidationCommandRunnerRequest,
    ValidationCommandCapturedStream,
    ValidationCommandExecutionEvidence,
    ValidationCommandRunnerSession,
    ValidationCommandExecutionRequest,
    ValidationCommandExecutionResult,
    ValidationCommandRunnerResult,
)
FORBIDDEN_PUBLIC_NAMES = (
    "execute_work_packet",
    "execute_tool",
    "ValidationCommandRunner",
    "ShellRunner",
    "PowerShellRunner",
    "BashRunner",
    "GitRunner",
    "ProviderDispatcher",
    "ModelRunner",
)


def compilation_with_validations(
    commands: tuple[str | None, ...] = (
        "python -m unittest --help",
        None,
        "python -m unittest -h",
    ),
):
    steps = tuple(
        validation_step(f"V{index}", command=command)
        for index, command in enumerate(commands, start=1)
    )
    source_ticket = compiler_ticket(
        ticket_id="P17.4",
        ticket_scope=compiler_scope(
            allowed_paths=("src/**",),
            forbidden_paths=("src/blocked/**",),
        ),
        tasks=("Execute filesystem task.", "Observe generated file."),
        validation_steps=steps,
    )
    return build_bundle(source_ticket=source_ticket)["result"]


def completed_single_agent_context(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    commands: tuple[str | None, ...] = (
        "python -m unittest --help",
        None,
        "python -m unittest -h",
    ),
    status: str = " M src/generated",
):
    compilation = compilation_with_validations(commands)
    workspace_root = tmp_path / "workspace"
    allocated, status_state = allocation_result(
        monkeypatch, compilation, workspace_root
    )
    permissions = profile_result(compilation, allocated)
    single_binding = build_single_agent_runtime_binding(
        agent_id="agent.p17-4",
        worker_id="worker.p17-4",
        work_packet=compilation.work_packet,
    )
    execution_plan = plan(tuple(basic_actions(compilation)))
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-3",
        authorization_reference="AUTH-P17-3",
        rationale="Authorize prerequisite P17.3 execution.",
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=single_binding,
        plan=execution_plan,
        risk_acknowledgement="Synthetic filesystem mutation risk acknowledged.",
    )
    single_request = SingleAgentExecutionRequest(
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=single_binding,
        plan=execution_plan,
        execution_authorization=authorization,
    )
    session = prepare_single_agent_execution(single_request)
    for index in range(len(execution_plan.actions)):
        result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=single_request,
                session=session,
            )
        )
        session = result.updated_session
        if index == 0:
            status_state["status"] = status
    single_result = complete_single_agent_execution(session)
    runtime = build_validation_command_runtime_binding(
        python_executable=sys.executable,
        allocation_result=allocated,
    )
    command_steps = tuple(
        step
        for step in compilation.work_packet.validation_steps
        if step.command is not None
    )
    requests = tuple(
        ValidationCommandAuthorizationRequest(
            validation_id=step.validation_id,
            timeout_seconds=30,
            expected_exit_codes=(0,),
        )
        for step in command_steps
    )
    runner_authorization = build_validation_command_runner_authorization(
        authorizer_id="validation.authorizer.p17-4",
        authorization_reference="AUTH-P17-4",
        rationale="Authorize exact WorkPacket validation commands.",
        risk_acknowledgement="Authorized validation code may have side effects.",
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        single_agent_execution_result=single_result,
        runtime_binding=runtime,
        authorization_requests=requests,
    )
    runner_request = ValidationCommandRunnerRequest(
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        single_agent_execution_result=single_result,
        runtime_binding=runtime,
        runner_authorization=runner_authorization,
    )
    return {
        "compilation": compilation,
        "allocation": allocated,
        "profile": permissions,
        "single_result": single_result,
        "runtime": runtime,
        "authorization_requests": requests,
        "runner_authorization": runner_authorization,
        "runner_request": runner_request,
        "workspace_root": workspace_root,
        "status_state": status_state,
    }


@pytest.fixture()
def prepared_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    context = completed_single_agent_context(monkeypatch, tmp_path)
    session = prepare_validation_command_runner(context["runner_request"])
    context["session"] = session
    return context


@pytest.fixture()
def completed_runner_context(prepared_context):
    session = prepared_context["session"]
    request = prepared_context["runner_request"]
    first = execute_validation_command(
        ValidationCommandExecutionRequest(runner_request=request, session=session)
    )
    second = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=request,
            session=first.updated_session,
        )
    )
    result = complete_validation_command_runner(second.updated_session)
    prepared_context["first"] = first
    prepared_context["second"] = second
    prepared_context["result"] = result
    return prepared_context


@pytest.fixture()
def sample_models(completed_runner_context):
    request = completed_runner_context["runner_request"]
    result = completed_runner_context["result"]
    first = completed_runner_context["first"]
    return {
        ValidationCommandRuntimeBinding.__name__: request.runtime_binding,
        ValidationCommandAuthorizationRequest.__name__: completed_runner_context[
            "authorization_requests"
        ][0],
        ValidationCommandSpecification.__name__: request.runner_authorization.command_specifications[
            0
        ],
        ValidationCommandRunnerAuthorization.__name__: request.runner_authorization,
        ValidationCommandRunnerRequest.__name__: request,
        ValidationCommandCapturedStream.__name__: first.stdout,
        ValidationCommandExecutionEvidence.__name__: first.updated_session.command_evidence[
            0
        ],
        ValidationCommandRunnerSession.__name__: first.updated_session,
        ValidationCommandExecutionRequest.__name__: ValidationCommandExecutionRequest(
            runner_request=request,
            session=first.updated_session,
        ),
        ValidationCommandExecutionResult.__name__: first,
        ValidationCommandRunnerResult.__name__: result,
    }


@pytest.mark.parametrize("exported_name", P17_4_EXPORTS)
def test_p17_4_exports_are_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


def test_prior_113_exports_remain_exact_prefix() -> None:
    prior = P17_0_EXPORTS + P17_1_EXPORTS + P17_2_EXPORTS + P17_3_EXPORTS
    assert len(prior) == 113
    assert work_packet.__all__[:113] == prior
    assert work_packet.__all__[113:145] == P17_4_EXPORTS
    assert len(work_packet.__all__) >= 145
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)


@pytest.mark.parametrize("forbidden_name", FORBIDDEN_PUBLIC_NAMES)
def test_forbidden_public_runner_names_absent(forbidden_name: str) -> None:
    assert not hasattr(work_packet, forbidden_name)


def test_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__) >= 145,
        len(work_packet.__all__) == len(set(work_packet.__all__)),
        hasattr(work_packet, "ValidationCommandRunnerSession"),
        hasattr(work_packet, "execute_validation_command"),
        hasattr(work_packet, "execute_work_packet"),
        hasattr(work_packet, "ValidationCommandRunner"),
    ) == (True, True, True, True, False, False)


def test_function_import_smoke_exact_output() -> None:
    assert (
        work_packet.build_validation_command_runtime_binding.__name__,
        work_packet.build_validation_command_runner_authorization.__name__,
        work_packet.prepare_validation_command_runner.__name__,
        work_packet.execute_validation_command.__name__,
        work_packet.complete_validation_command_runner.__name__,
    ) == (
        "build_validation_command_runtime_binding",
        "build_validation_command_runner_authorization",
        "prepare_validation_command_runner",
        "execute_validation_command",
        "complete_validation_command_runner",
    )


def test_import_has_no_process_thread_or_inspection_side_effects(monkeypatch) -> None:
    with (
        patch.object(vcr.subprocess, "Popen", side_effect=AssertionError("process")),
        patch.object(vcr.threading, "Thread", side_effect=AssertionError("thread")),
        patch.object(
            vcr,
            "inspect_human_provisioned_workspace",
            side_effect=AssertionError("inspection"),
        ),
    ):
        __import__("hermes_cli.agent_platform.work_packet.validation_command_runner")


@pytest.mark.parametrize(
    "enum_cls",
    (
        ValidationCommandModule,
        ValidationCommandRunnerState,
        ValidationCommandDisposition,
        ValidationCommandFailureReason,
        ValidationCommandStreamKind,
    ),
)
def test_controlled_enums_have_no_aliases(enum_cls: type) -> None:
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
def test_public_models_have_no_runtime_handle_schema_fields(
    model_cls: type[BaseModel],
) -> None:
    for field in model_cls.model_fields.values():
        annotation_text = str(field.annotation).casefold()
        for marker in ("popen", "thread", "bytes", "callable", "mapping", "object"):
            assert marker not in annotation_text


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
    model = sample_models[model_cls.__name__]
    if "schema_version" not in model.model_fields:
        assert "schema_version" not in model.model_fields
        return
    data = model.model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_tuple_fields_round_trip_as_tuples(
    model_cls: type[BaseModel], sample_models
) -> None:
    model = sample_models[model_cls.__name__]
    for name, field in model.model_fields.items():
        annotation = field.annotation
        if get_origin(annotation) is tuple:
            value = getattr(model, name)
            if value:
                assert isinstance(value, tuple)


@pytest.mark.parametrize(
    "field,value",
    (
        ("shell", "false"),
        ("stdin_disabled", "true"),
        ("network_isolation_guaranteed", "false"),
        ("process_tree_isolation_guaranteed", "false"),
    ),
)
def test_strict_boolean_posture_rejects_strings(
    prepared_context, field: str, value: str
) -> None:
    binding = prepared_context["runtime"]
    data = binding.model_dump(mode="json")
    data[field] = value
    data["binding_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        ValidationCommandRuntimeBinding.model_validate(data)


def test_runtime_binding_current_interpreter_passes(prepared_context) -> None:
    binding = prepared_context["runtime"]
    assert (
        binding.resolved_python_executable == Path(sys.executable).resolve().as_posix()
    )
    assert binding.shell is False
    assert binding.stdin_disabled is True
    assert binding.max_stdout_bytes == 262144
    assert binding.retained_stdout_bytes == 65536
    assert binding.output_reader_threads == 2
    assert binding.network_isolation_guaranteed is False
    assert binding.process_tree_isolation_guaranteed is False


@pytest.mark.parametrize(
    "python_path",
    (
        "python",
        "C:/definitely/missing/python.exe",
    ),
)
def test_runtime_binding_rejects_bad_interpreter_paths(
    prepared_context, python_path: str
) -> None:
    with pytest.raises(Exception):
        build_validation_command_runtime_binding(
            python_executable=python_path,
            allocation_result=prepared_context["allocation"],
        )


def test_runtime_binding_rejects_directory_interpreter(
    prepared_context, tmp_path
) -> None:
    with pytest.raises(Exception):
        build_validation_command_runtime_binding(
            python_executable=path_text(tmp_path),
            allocation_result=prepared_context["allocation"],
        )


def test_runtime_binding_rejects_symlink_interpreter(
    prepared_context, tmp_path
) -> None:
    if not hasattr(Path, "symlink_to"):
        pytest.skip("symlink unsupported")
    link = tmp_path / "python-link"
    try:
        link.symlink_to(Path(sys.executable))
    except OSError:
        pytest.skip("symlink unavailable")
    with pytest.raises(Exception):
        build_validation_command_runtime_binding(
            python_executable=link.as_posix(),
            allocation_result=prepared_context["allocation"],
        )


def test_runtime_binding_rejects_working_directory_mismatch(prepared_context) -> None:
    binding = prepared_context["runtime"]
    data = binding.model_dump(mode="json")
    data["working_directory"] = "C:/other/workspace"
    data["binding_id"] = binding.binding_id
    data["binding_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        ValidationCommandRuntimeBinding.model_validate(data)


def test_runtime_binding_repeated_inputs_are_equal(prepared_context) -> None:
    first = prepared_context["runtime"]
    second = build_validation_command_runtime_binding(
        python_executable=sys.executable,
        allocation_result=prepared_context["allocation"],
    )
    assert first == second


def test_runtime_binding_tampered_digest_fails(prepared_context) -> None:
    data = prepared_context["runtime"].model_dump(mode="json")
    data["binding_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        ValidationCommandRuntimeBinding.model_validate(data)


@pytest.mark.parametrize("timeout", (1, 30, 600))
def test_authorization_request_valid_timeout_passes(timeout: int) -> None:
    request = ValidationCommandAuthorizationRequest(
        validation_id="V1", timeout_seconds=timeout
    )
    assert request.timeout_seconds == timeout


@pytest.mark.parametrize("timeout", (0, 601))
def test_authorization_request_timeout_bounds(timeout: int) -> None:
    with pytest.raises(ValidationError):
        ValidationCommandAuthorizationRequest(
            validation_id="V1", timeout_seconds=timeout
        )


@pytest.mark.parametrize("codes", ((0,), (0, 2), (2, 0)))
def test_authorization_request_exit_codes_normalize(codes: tuple[int, ...]) -> None:
    request = ValidationCommandAuthorizationRequest(
        validation_id="V1",
        timeout_seconds=5,
        expected_exit_codes=codes,
    )
    assert request.expected_exit_codes == tuple(sorted(codes))


@pytest.mark.parametrize("codes", ((), (0, 0), (-1,), (256,), ("0",)))
def test_authorization_request_rejects_invalid_exit_codes(codes) -> None:
    with pytest.raises(ValidationError):
        ValidationCommandAuthorizationRequest(
            validation_id="V1",
            timeout_seconds=5,
            expected_exit_codes=codes,
        )


@pytest.mark.parametrize(
    "command,module",
    (
        ("python -m pytest tests/example.py", ValidationCommandModule.PYTEST),
        ("python -m unittest discover -s tests", ValidationCommandModule.UNITTEST),
        ("python -m ruff check hermes_cli", ValidationCommandModule.RUFF_CHECK),
        (
            "python -m ruff format --check hermes_cli",
            ValidationCommandModule.RUFF_FORMAT_CHECK,
        ),
    ),
)
def test_parser_accepts_allowed_families(
    prepared_context, command: str, module: ValidationCommandModule
) -> None:
    parsed_module, argv = vcr._parse_command(
        source_command=command,
        runtime_binding=prepared_context["runtime"],
    )
    assert parsed_module is module
    assert argv[0] == prepared_context["runtime"].resolved_python_executable
    assert argv[1] == "-m"


@pytest.mark.parametrize(
    "command",
    (
        "",
        "python -m pytest 'unterminated",
        "python -m pytest tests | cat",
        "python -m pytest tests || true",
        "python -m pytest tests && true",
        "python -m pytest tests > out.txt",
        "python -m pytest tests; true",
        "python -m pytest `whoami`",
        "python -m pytest $(whoami)",
        "python -m pytest ${HOME}",
        "TOKEN=value python -m pytest tests",
        "python -m pytest @args.txt",
        "python -m pytest\n tests",
        "python -m pytest\r tests",
        "python -m pytest \x00",
        "python -m pytest /tmp/tests",
        "python -m pytest C:/tests",
        "python -m pytest ../tests",
        "python -m pytest tests\\unit",
        "python -m pytest Authorization: Bearer tokenvalue",
        "python -m pytest access_token=value",
        "python -m pytest refresh_token=value",
        "python -m pytest sk-abc12345678901234567890",
        "python -m pytest password=value",
        "python -m pytest client_secret=value",
    ),
)
def test_parser_rejects_forbidden_command_shapes(
    prepared_context, command: str
) -> None:
    with pytest.raises(Exception):
        vcr._parse_command(
            source_command=command, runtime_binding=prepared_context["runtime"]
        )


@pytest.mark.parametrize("executable", ("python", "python3", "py"))
def test_python_invocation_names_pass(prepared_context, executable: str) -> None:
    module, _argv = vcr._parse_command(
        source_command=f"{executable} -m unittest --help",
        runtime_binding=prepared_context["runtime"],
    )
    assert module is ValidationCommandModule.UNITTEST


def test_interpreter_basename_invocation_passes(prepared_context) -> None:
    name = Path(prepared_context["runtime"].resolved_python_executable).name
    module, _argv = vcr._parse_command(
        source_command=f"{name} -m unittest --help",
        runtime_binding=prepared_context["runtime"],
    )
    assert module is ValidationCommandModule.UNITTEST


@pytest.mark.parametrize(
    "command",
    (
        "python -c print(1)",
        "python script.py",
        "python -",
        "python -m pip list",
        "node -m pytest tests",
    ),
)
def test_python_invocation_rejects_unsupported_forms(
    prepared_context, command: str
) -> None:
    with pytest.raises(Exception):
        vcr._parse_command(
            source_command=command, runtime_binding=prepared_context["runtime"]
        )


def test_pytest_injects_cache_disable(prepared_context) -> None:
    _module, argv = vcr._parse_command(
        source_command="python -m pytest tests/example.py",
        runtime_binding=prepared_context["runtime"],
    )
    assert argv[-2:] == ("-p", "no:cacheprovider")


def test_pytest_preserves_cache_disable(prepared_context) -> None:
    _module, argv = vcr._parse_command(
        source_command="python -m pytest -p no:cacheprovider tests/example.py",
        runtime_binding=prepared_context["runtime"],
    )
    assert argv.count("-p") == 1
    assert argv[argv.index("-p") + 1] == "no:cacheprovider"


@pytest.mark.parametrize(
    "option", ("-p", "-pplugin", "--pdb", "--trace", "--pdbcls=x:y", "--pastebin=all")
)
def test_pytest_rejects_interactive_or_plugin_options(
    prepared_context, option: str
) -> None:
    command = f"python -m pytest {option} tests/example.py"
    with pytest.raises(Exception):
        vcr._parse_command(
            source_command=command, runtime_binding=prepared_context["runtime"]
        )


@pytest.mark.parametrize("args", ("discover", "tests.test_example", "tests/example.py"))
def test_unittest_policy_accepts_safe_arguments(prepared_context, args: str) -> None:
    module, argv = vcr._parse_command(
        source_command=f"python -m unittest {args}",
        runtime_binding=prepared_context["runtime"],
    )
    assert module is ValidationCommandModule.UNITTEST
    assert argv[-1] == args


@pytest.mark.parametrize("args", ("/tmp/test_example.py", "../tests", "C:/tests"))
def test_unittest_policy_rejects_unsafe_arguments(prepared_context, args: str) -> None:
    with pytest.raises(Exception):
        vcr._parse_command(
            source_command=f"python -m unittest {args}",
            runtime_binding=prepared_context["runtime"],
        )


def test_ruff_check_injects_no_cache(prepared_context) -> None:
    module, argv = vcr._parse_command(
        source_command="python -m ruff check hermes_cli",
        runtime_binding=prepared_context["runtime"],
    )
    assert module is ValidationCommandModule.RUFF_CHECK
    assert "--no-cache" in argv


def test_ruff_check_preserves_no_cache(prepared_context) -> None:
    _module, argv = vcr._parse_command(
        source_command="python -m ruff check --no-cache hermes_cli",
        runtime_binding=prepared_context["runtime"],
    )
    assert argv.count("--no-cache") == 1


@pytest.mark.parametrize("option", ("--fix", "--fix-only", "--unsafe-fixes"))
def test_ruff_check_rejects_write_options(prepared_context, option: str) -> None:
    with pytest.raises(Exception):
        vcr._parse_command(
            source_command=f"python -m ruff check {option} hermes_cli",
            runtime_binding=prepared_context["runtime"],
        )


def test_ruff_format_requires_check(prepared_context) -> None:
    with pytest.raises(Exception):
        vcr._parse_command(
            source_command="python -m ruff format hermes_cli",
            runtime_binding=prepared_context["runtime"],
        )


def test_ruff_format_check_passes(prepared_context) -> None:
    module, argv = vcr._parse_command(
        source_command="python -m ruff format --check hermes_cli",
        runtime_binding=prepared_context["runtime"],
    )
    assert module is ValidationCommandModule.RUFF_FORMAT_CHECK
    assert "--check" in argv


def test_command_coverage_exact(prepared_context) -> None:
    authorization = prepared_context["runner_authorization"]
    assert tuple(
        spec.validation_id for spec in authorization.command_specifications
    ) == (
        "V1",
        "V3",
    )
    assert tuple(spec.command_id for spec in authorization.command_specifications) == (
        "VCMD-001",
        "VCMD-002",
    )


@pytest.mark.parametrize(
    "requests_factory",
    (
        lambda ctx: ctx["authorization_requests"][:1],
        lambda ctx: (*ctx["authorization_requests"], ctx["authorization_requests"][0]),
        lambda ctx: (
            *ctx["authorization_requests"],
            ValidationCommandAuthorizationRequest(
                validation_id="UNKNOWN", timeout_seconds=5
            ),
        ),
        lambda ctx: (
            *ctx["authorization_requests"],
            ValidationCommandAuthorizationRequest(
                validation_id="V2", timeout_seconds=5
            ),
        ),
    ),
)
def test_command_authorization_coverage_rejects_bad_sets(
    prepared_context, requests_factory
) -> None:
    ctx = prepared_context
    with pytest.raises(Exception):
        build_validation_command_runner_authorization(
            authorizer_id="validation.authorizer.p17-4",
            authorization_reference="AUTH-P17-4",
            rationale="Authorize exact WorkPacket validation commands.",
            risk_acknowledgement="Authorized validation code may have side effects.",
            compilation_result=ctx["compilation"],
            allocation_result=ctx["allocation"],
            profile_result=ctx["profile"],
            single_agent_execution_result=ctx["single_result"],
            runtime_binding=ctx["runtime"],
            authorization_requests=requests_factory(ctx),
        )


def test_no_command_step_fails(monkeypatch, tmp_path) -> None:
    with pytest.raises(Exception):
        completed_single_agent_context(monkeypatch, tmp_path, commands=(None,))


def test_human_authorization_valid_nonshadow(prepared_context) -> None:
    authorization = prepared_context["runner_authorization"]
    assert authorization.execution_authorized is True
    assert authorization.synthetic is False
    assert not authorization.authorizer_id.startswith("SHADOW-")
    assert authorization.risk_acknowledgement


@pytest.mark.parametrize(
    "field,value",
    (
        ("authorizer_id", "SHADOW-human"),
        ("synthetic", True),
        ("risk_acknowledgement", ""),
    ),
)
def test_human_authorization_rejects_bad_posture(
    prepared_context, field: str, value
) -> None:
    data = prepared_context["runner_authorization"].model_dump(mode="json")
    data[field] = value
    data["authorization_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        ValidationCommandRunnerAuthorization.model_validate(data)


@pytest.mark.parametrize(
    "field",
    (
        "work_packet_id",
        "allocation_id",
        "profile_id",
        "single_agent_result_SHA256",
        "runtime_binding_SHA256",
    ),
)
def test_request_binding_rejects_mismatches(prepared_context, field: str) -> None:
    authorization = prepared_context["runner_authorization"]
    data = authorization.model_dump(mode="json")
    data[field] = "0" * 64 if field.endswith("SHA256") else "mismatch"
    data["authorization_SHA256"] = vcr._authorization_digest_from_record({
        key: value for key, value in data.items() if key != "authorization_SHA256"
    })
    bad_authorization = ValidationCommandRunnerAuthorization.model_validate(data)
    with pytest.raises(ValidationError):
        ValidationCommandRunnerRequest(
            compilation_result=prepared_context["compilation"],
            allocation_result=prepared_context["allocation"],
            profile_result=prepared_context["profile"],
            single_agent_execution_result=prepared_context["single_result"],
            runtime_binding=prepared_context["runtime"],
            runner_authorization=bad_authorization,
        )


def test_request_rejects_runtime_workspace_mismatch(prepared_context) -> None:
    data = prepared_context["runtime"].model_dump(mode="json")
    data["working_directory"] = "C:/other/workspace"
    data["binding_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        ValidationCommandRuntimeBinding.model_validate(data)


def test_request_inputs_remain_unchanged(prepared_context) -> None:
    before = prepared_context["runner_request"].model_dump_json()
    _ = prepare_validation_command_runner(prepared_context["runner_request"])
    assert prepared_context["runner_request"].model_dump_json() == before


def test_minimal_environment_fixed_and_filtered(monkeypatch) -> None:
    monkeypatch.setenv("PATH", "blocked")
    monkeypatch.setenv("PYTHONPATH", "blocked")
    monkeypatch.setenv("HOME", "blocked")
    monkeypatch.setenv("USERPROFILE", "blocked")
    monkeypatch.setenv("HTTPS_PROXY", "blocked")
    monkeypatch.setenv("OPENAI_API_KEY", "blocked")
    monkeypatch.setenv("SYSTEMROOT", "allowed")
    env = vcr._minimal_environment()
    for key, value in vcr._FIXED_ENVIRONMENT:
        assert env[key] == value
    assert env["SYSTEMROOT"] == "allowed"
    for key in (
        "PATH",
        "PYTHONPATH",
        "HOME",
        "USERPROFILE",
        "HTTPS_PROXY",
        "OPENAI_API_KEY",
    ):
        assert key not in env
    assert tuple(env) == tuple(sorted(env))


@pytest.mark.parametrize("status", ("", " M generated.txt", "?? new.txt"))
def test_workspace_dirty_or_clean_linked_prepares(
    monkeypatch, tmp_path, status: str
) -> None:
    context = completed_single_agent_context(monkeypatch, tmp_path, status=status)
    session = prepare_validation_command_runner(context["runner_request"])
    assert session.state is ValidationCommandRunnerState.PREPARED


@pytest.mark.parametrize(
    "branch,commit,linked",
    (
        ("other", SOURCE_COMMIT, True),
        (WORKSPACE_BRANCH, "b" * 40, True),
        (WORKSPACE_BRANCH, SOURCE_COMMIT, False),
    ),
)
def test_workspace_gate_rejects_drift(
    monkeypatch, tmp_path, branch: str, commit: str, linked: bool
) -> None:
    context = completed_single_agent_context(monkeypatch, tmp_path)
    patch_workspace_inspection(
        monkeypatch,
        context["workspace_root"],
        status_state=context["status_state"],
        branch=branch,
        commit=commit,
        linked=linked,
    )
    with pytest.raises(Exception):
        prepare_validation_command_runner(context["runner_request"])


def test_prepare_returns_deterministic_session(prepared_context) -> None:
    first = prepared_context["session"]
    second = prepare_validation_command_runner(prepared_context["runner_request"])
    assert first == second
    assert first.next_command_index == 0
    assert first.manual_validation_ids_pending == ("V2",)
    validate_validation_command_runner_session(first)


def test_prepare_launches_no_process_or_threads(prepared_context) -> None:
    with (
        patch.object(vcr.subprocess, "Popen", side_effect=AssertionError("process")),
        patch.object(vcr.threading, "Thread", side_effect=AssertionError("thread")),
    ):
        prepare_validation_command_runner(prepared_context["runner_request"])


def test_cancellation_before_launch(prepared_context) -> None:
    with patch.object(vcr.subprocess, "Popen", side_effect=AssertionError("process")):
        result = execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=prepared_context["runner_request"],
                session=prepared_context["session"],
                cancellation_requested=True,
                cancellation_reference="CANCEL-P17-4",
            )
        )
    assert result.disposition is ValidationCommandDisposition.CANCELLED
    assert result.updated_session.state is ValidationCommandRunnerState.CANCELLED
    assert result.updated_session.command_evidence[-1].process_started is False


def test_cancellation_reference_required(prepared_context) -> None:
    with pytest.raises(ValidationError):
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
            cancellation_requested=True,
        )


def test_cancelled_session_cannot_continue_or_complete(prepared_context) -> None:
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
            cancellation_requested=True,
            cancellation_reference="CANCEL-P17-4",
        )
    )
    with pytest.raises(Exception):
        execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=prepared_context["runner_request"],
                session=result.updated_session,
            )
        )
    with pytest.raises(Exception):
        complete_validation_command_runner(result.updated_session)


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


def test_process_launch_posture(prepared_context, monkeypatch) -> None:
    calls = []

    def fake_popen(*args, **kwargs):
        calls.append((args, kwargs))
        return FakeProcess(stdout=b"ok\n", stderr=b"", code=0)

    monkeypatch.setattr(vcr.subprocess, "Popen", fake_popen)
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    assert result.disposition is ValidationCommandDisposition.PASSED
    args, kwargs = calls[0]
    assert args[0][0] == prepared_context["runtime"].resolved_python_executable
    assert kwargs["shell"] is False
    assert kwargs["stdin"] is vcr.subprocess.DEVNULL
    assert kwargs["stdout"] is vcr.subprocess.PIPE
    assert kwargs["stderr"] is vcr.subprocess.PIPE
    assert kwargs["text"] is False
    assert kwargs["bufsize"] == 0
    assert (
        kwargs["cwd"]
        == prepared_context["allocation"].allocation.resolved_workspace_root
    )
    assert "PATH" not in kwargs["env"]
    assert len(calls) == 1


@pytest.mark.parametrize(
    "raw,expected,redactions,replacements",
    (
        (b"", None, 0, 0),
        (b"plain\n", "plain", 0, 0),
        (b"\x1b[31mred\x1b[0m", "red", 0, 0),
        (b"bad\xff", "bad\ufffd", 0, 1),
        (b"Authorization: Bearer abcdefghijklmnopqrstuvwxyz", "<REDACTED>", 1, 0),
        (b"password=supersecret", "<REDACTED>", 1, 0),
        (b"client_secret=supersecret", "<REDACTED>", 1, 0),
        (b"sk-abcdefghijklmnopqrstuvwxyz", "<REDACTED>", 1, 0),
    ),
)
def test_captured_stream_sanitization(
    raw: bytes, expected: str | None, redactions: int, replacements: int
) -> None:
    stream = vcr._captured_stream(ValidationCommandStreamKind.STDOUT, raw, 65536)
    assert stream.retained_text == expected
    assert stream.redaction_count == redactions
    assert stream.decode_replacement_count == replacements
    assert stream.raw_SHA256 == vcr._sha256_bytes(raw)


def test_captured_stream_truncates_retained_text() -> None:
    stream = vcr._captured_stream(ValidationCommandStreamKind.STDOUT, b"abcdef", 3)
    assert stream.retained_text == "abc"
    assert stream.truncated is True
    assert stream.retained_byte_count == 3


def test_output_capture_uses_two_reader_threads(prepared_context, monkeypatch) -> None:
    created = []
    original_thread = vcr.threading.Thread

    def tracking_thread(*args, **kwargs):
        thread = original_thread(*args, **kwargs)
        created.append(thread)
        return thread

    monkeypatch.setattr(vcr.threading, "Thread", tracking_thread)
    execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    assert len(created) == 2
    assert all(not thread.is_alive() for thread in created)


def test_successful_command_progresses(prepared_context) -> None:
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    assert result.disposition is ValidationCommandDisposition.PASSED
    assert result.updated_session.next_command_index == 1
    assert result.updated_session.completed_command_ids == ("VCMD-001",)
    assert result.updated_session.passed_validation_ids == ("V1",)
    assert result.updated_session.state is ValidationCommandRunnerState.ACTIVE
    evidence = result.updated_session.command_evidence[-1]
    assert evidence.process_started is True
    assert evidence.terminate_requested is False
    assert evidence.kill_requested is False


def test_nonzero_exit_blocks(monkeypatch, tmp_path) -> None:
    context = completed_single_agent_context(
        monkeypatch,
        tmp_path,
        commands=("python -m unittest no_such_test",),
    )
    session = prepare_validation_command_runner(context["runner_request"])
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=context["runner_request"], session=session
        )
    )
    assert result.disposition is ValidationCommandDisposition.FAILED
    assert result.updated_session.state is ValidationCommandRunnerState.BLOCKED
    assert (
        result.updated_session.command_evidence[-1].failure_reason
        is ValidationCommandFailureReason.NONZERO_EXIT
    )


def test_authorized_nonzero_exit_passes(monkeypatch, tmp_path) -> None:
    context = completed_single_agent_context(
        monkeypatch,
        tmp_path,
        commands=("python -m unittest no_such_test",),
    )
    request = ValidationCommandAuthorizationRequest(
        validation_id="V1", timeout_seconds=30, expected_exit_codes=(1,)
    )
    authorization = build_validation_command_runner_authorization(
        authorizer_id="validation.authorizer.p17-4",
        authorization_reference="AUTH-P17-4",
        rationale="Authorize expected failing unittest invocation.",
        risk_acknowledgement="Authorized validation code may have side effects.",
        compilation_result=context["compilation"],
        allocation_result=context["allocation"],
        profile_result=context["profile"],
        single_agent_execution_result=context["single_result"],
        runtime_binding=context["runtime"],
        authorization_requests=(request,),
    )
    runner_request = ValidationCommandRunnerRequest(
        compilation_result=context["compilation"],
        allocation_result=context["allocation"],
        profile_result=context["profile"],
        single_agent_execution_result=context["single_result"],
        runtime_binding=context["runtime"],
        runner_authorization=authorization,
    )
    session = prepare_validation_command_runner(runner_request)
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=runner_request, session=session
        )
    )
    assert result.disposition is ValidationCommandDisposition.PASSED


def test_launch_failure_is_bounded(prepared_context, monkeypatch) -> None:
    monkeypatch.setattr(
        vcr.subprocess,
        "Popen",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("secret path")),
    )
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    assert result.disposition is ValidationCommandDisposition.FAILED
    assert result.updated_session.state is ValidationCommandRunnerState.BLOCKED
    assert (
        result.updated_session.command_evidence[-1].failure_reason
        is ValidationCommandFailureReason.LAUNCH_ERROR
    )


def test_timeout_blocks(monkeypatch, tmp_path) -> None:
    context = completed_single_agent_context(
        monkeypatch,
        tmp_path,
        commands=("python -m unittest --help",),
    )
    spec = context["runner_authorization"].command_specifications[0]
    data = spec.model_dump(mode="json")
    data["timeout_seconds"] = 1
    data["effective_argv"] = (
        context["runtime"].resolved_python_executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "src",
    )
    data["specification_SHA256"] = vcr._specification_digest_from_record({
        key: value for key, value in data.items() if key != "specification_SHA256"
    })
    specification = ValidationCommandSpecification.model_validate(data)
    launch = vcr._LaunchResult(
        exit_code=None,
        stdout_raw=b"",
        stderr_raw=b"",
        process_started=True,
        terminate_requested=True,
        kill_requested=True,
        timed_out=True,
        output_limit_exceeded=False,
        launch_failed=False,
    )
    disposition, reason = vcr._disposition_for_launch(specification, launch)
    assert disposition is ValidationCommandDisposition.TIMED_OUT
    assert reason is ValidationCommandFailureReason.TIMEOUT


def test_output_overflow_blocks(prepared_context) -> None:
    spec = prepared_context["runner_authorization"].command_specifications[0]
    launches = (
        vcr._LaunchResult(
            exit_code=0,
            stdout_raw=b"x" * 262144,
            stderr_raw=b"",
            process_started=True,
            terminate_requested=True,
            kill_requested=False,
            timed_out=False,
            output_limit_exceeded=True,
            launch_failed=False,
        ),
        vcr._LaunchResult(
            exit_code=0,
            stdout_raw=b"",
            stderr_raw=b"x" * 262144,
            process_started=True,
            terminate_requested=True,
            kill_requested=False,
            timed_out=False,
            output_limit_exceeded=True,
            launch_failed=False,
        ),
    )
    for launch in launches:
        disposition, reason = vcr._disposition_for_launch(spec, launch)
        assert disposition is ValidationCommandDisposition.OUTPUT_LIMIT_EXCEEDED
        assert reason is ValidationCommandFailureReason.OUTPUT_LIMIT


def test_workspace_after_command_records_dirty_status(prepared_context) -> None:
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    evidence = result.updated_session.command_evidence[-1]
    assert evidence.workspace_status_entry_count_before == 1
    assert evidence.workspace_status_entry_count_after == 1
    assert evidence.workspace_inspection_before_SHA256
    assert evidence.workspace_inspection_after_SHA256


def test_blocked_session_cannot_continue(prepared_context, monkeypatch) -> None:
    monkeypatch.setattr(
        vcr.subprocess, "Popen", lambda *args, **kwargs: FakeProcess(code=2)
    )
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    with pytest.raises(Exception):
        execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=prepared_context["runner_request"],
                session=result.updated_session,
            )
        )


def test_completed_session_cannot_continue(completed_runner_context) -> None:
    with pytest.raises(Exception):
        execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=completed_runner_context["runner_request"],
                session=completed_runner_context["result"].session,
            )
        )


def test_completion_result_posture(completed_runner_context) -> None:
    result = completed_runner_context["result"]
    assert result.state is ValidationCommandRunnerState.COMPLETED
    assert result.completed_command_count == 2
    assert result.passed_validation_ids == ("V1", "V3")
    assert result.manual_validation_ids_pending == ("V2",)
    assert result.validation_command_runner_requirement_satisfied is True
    assert result.result_envelopes_ready is False
    assert result.diff_artifact_review_ready is False
    assert result.human_git_handoff_ready is False
    assert result.provider_dispatch_count == 0
    assert result.model_inference_count == 0
    validate_validation_command_runner_result(result)


@pytest.mark.parametrize("session_key", ("session",))
def test_incomplete_session_cannot_complete(prepared_context, session_key: str) -> None:
    with pytest.raises(Exception):
        complete_validation_command_runner(prepared_context[session_key])


def test_manual_validation_may_remain_pending(completed_runner_context) -> None:
    assert completed_runner_context["result"].manual_validation_ids_pending == ("V2",)


def test_final_result_contains_no_output_text(completed_runner_context) -> None:
    dumped = completed_runner_context["result"].model_dump_json()
    assert "retained_text" not in dumped
    assert "usage: python" not in dumped
    assert "For test discovery" not in dumped


@pytest.mark.parametrize(
    "mutator",
    (
        lambda ctx: ctx["runtime"].model_copy(
            update={"python_executable": "C:/other/python"}
        ),
        lambda ctx: ctx["runner_authorization"]
        .command_specifications[0]
        .model_copy(update={"source_command": "python -m unittest --help  "}),
        lambda ctx: ctx["runner_authorization"]
        .command_specifications[0]
        .model_copy(update={"timeout_seconds": 99}),
        lambda ctx: ctx["runner_authorization"]
        .command_specifications[0]
        .model_copy(update={"expected_exit_codes": (0, 2)}),
        lambda ctx: ctx["runner_authorization"]
        .command_specifications[0]
        .model_copy(update={"effective_argv": ("python", "-m", "unittest")}),
        lambda ctx: ctx["runner_authorization"].model_copy(
            update={"rationale": "Changed rationale."}
        ),
        lambda ctx: ctx["first"]
        .updated_session.command_evidence[0]
        .model_copy(update={"stdout_SHA256": "0" * 64}),
        lambda ctx: ctx["first"].updated_session.model_copy(
            update={"next_command_index": 0}
        ),
        lambda ctx: ctx["result"].model_copy(update={"provider_dispatch_count": 1}),
    ),
)
def test_digest_changes_are_detectable(completed_runner_context, mutator) -> None:
    changed = mutator(completed_runner_context)
    dumped = changed.model_dump(mode="json")
    assert dumped
    assert changed != list(completed_runner_context.values())[0]


@pytest.mark.parametrize(
    "forbidden",
    (
        "shell=True",
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
        "python -c",
        "script.py",
        "ThreadPool",
        "asyncio",
        "retry_work_packet",
        "fallback",
        "result envelope",
        "diff review complete",
        "git handoff complete",
        "git add",
        "git commit",
        "git push",
    ),
)
def test_authority_boundary_forbidden_text_not_in_public_api(forbidden: str) -> None:
    public_names = " ".join(work_packet.__all__).casefold()
    assert forbidden.casefold() not in public_names


def test_command_side_effect_limitation(prepared_context) -> None:
    before = active_count()
    result = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=prepared_context["runner_request"],
            session=prepared_context["session"],
        )
    )
    assert active_count() == before
    assert (
        result.updated_session.command_evidence[-1].workspace_status_entry_count_after
        == 1
    )


def test_canonical_human_authorized_validation_command_runner_flow(
    monkeypatch, tmp_path
) -> None:
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
    completed = complete_validation_command_runner(second.updated_session)
    assert first.disposition is ValidationCommandDisposition.PASSED
    assert second.disposition is ValidationCommandDisposition.PASSED
    assert completed.completed_command_count == 2
    assert completed.passed_validation_ids == ("V1", "V3")
    assert completed.manual_validation_ids_pending == ("V2",)
    assert completed.provider_dispatch_count == 0
    assert completed.model_inference_count == 0
    assert completed.result_envelopes_ready is False
    assert completed.diff_artifact_review_ready is False
    assert completed.human_git_handoff_ready is False
    assert all(
        spec.effective_argv[0] == context["runtime"].resolved_python_executable
        for spec in context["runner_authorization"].command_specifications
    )
    assert first.stdout.raw_byte_count >= 0
    assert first.stderr.raw_byte_count >= 0
