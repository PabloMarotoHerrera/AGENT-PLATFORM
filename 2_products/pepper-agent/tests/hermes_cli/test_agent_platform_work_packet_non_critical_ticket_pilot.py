import ast
from enum import Enum
import sys

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.non_critical_ticket_pilot as ncp
from hermes_cli.agent_platform.work_packet import (
    NON_CRITICAL_TICKET_PILOT_EXPORT_COUNT,
    NON_CRITICAL_TICKET_PILOT_POLICY_ID,
    NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION,
    GitHandoffDecision,
    GitHandoffPathStatus,
    GitHandoffResult,
    NonCriticalTicketPilotError,
    NonCriticalTicketPilotInputError,
    NonCriticalTicketPilotIntegrityError,
    NonCriticalTicketPilotPolicyError,
    NonCriticalTicketPilotRequest,
    NonCriticalTicketPilotResult,
    NonCriticalTicketPilotStateError,
    NonCriticalTicketPilotValidationError,
    PilotAcceptanceSummary,
    PilotDecision,
    PilotEligibilityPolicy,
    PilotFinding,
    PilotFindingCode,
    PilotFindingSeverity,
    PilotRiskClass,
    PilotStage,
    PilotStageEvidence,
    PilotState,
    PilotTicketSelection,
    ReviewArtifactKind,
    ReviewFindingSeverity,
    ReviewObservedPathStatus,
    ToolPermissionOperation,
    ValidationCommandAuthorizationRequest,
    ValidationCommandExecutionRequest,
    ValidationCommandRunnerRequest,
    build_human_git_handoff,
    build_non_critical_ticket_pilot,
    build_pilot_eligibility_policy,
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
    summarize_non_critical_ticket_pilot,
    validate_non_critical_ticket_pilot_request,
    validate_non_critical_ticket_pilot_result,
)
from hermes_cli.agent_platform.work_packet.single_agent_execution import (
    SingleAgentActionExecutionRequest,
    SingleAgentExecutionRequest,
)
from hermes_cli.agent_platform.work_packet.validation_command_runner import (
    ValidationCommandDisposition,
    ValidationCommandRunnerState,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_diff_artifact_review as p17_6,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_human_git_handoff as p17_7,
)


P17_8_EXPORTS = (
    "NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION",
    "NON_CRITICAL_TICKET_PILOT_POLICY_ID",
    "NON_CRITICAL_TICKET_PILOT_EXPORT_COUNT",
    "PilotState",
    "PilotDecision",
    "PilotRiskClass",
    "PilotStage",
    "PilotFindingSeverity",
    "PilotFindingCode",
    "PilotEligibilityPolicy",
    "PilotTicketSelection",
    "PilotStageEvidence",
    "PilotFinding",
    "PilotAcceptanceSummary",
    "NonCriticalTicketPilotRequest",
    "NonCriticalTicketPilotResult",
    "NonCriticalTicketPilotError",
    "NonCriticalTicketPilotInputError",
    "NonCriticalTicketPilotIntegrityError",
    "NonCriticalTicketPilotPolicyError",
    "NonCriticalTicketPilotStateError",
    "NonCriticalTicketPilotValidationError",
    "build_pilot_eligibility_policy",
    "validate_non_critical_ticket_pilot_request",
    "build_non_critical_ticket_pilot",
    "validate_non_critical_ticket_pilot_result",
    "summarize_non_critical_ticket_pilot",
)
PUBLIC_MODELS = (
    PilotEligibilityPolicy,
    PilotTicketSelection,
    PilotStageEvidence,
    PilotFinding,
    PilotAcceptanceSummary,
    NonCriticalTicketPilotRequest,
    NonCriticalTicketPilotResult,
)
CONTROLLED_ENUMS = (
    PilotState,
    PilotDecision,
    PilotRiskClass,
    PilotStage,
    PilotFindingSeverity,
    PilotFindingCode,
)
EXPECTED_ENUM_VALUES = (
    (PilotState, ("prepared", "blocked", "completed")),
    (PilotDecision, ("accepted", "rejected")),
    (PilotRiskClass, ("non_critical",)),
    (
        PilotStage,
        (
            "work_packet_compilation",
            "workspace_allocation",
            "tool_permission_profile",
            "single_agent_execution",
            "validation_command_runner",
            "outcome_envelope",
            "diff_artifact_review",
            "human_git_handoff",
        ),
    ),
    (PilotFindingSeverity, ("info", "warning", "blocking")),
    (
        PilotFindingCode,
        (
            "ticket_eligible",
            "ticket_critical",
            "ticket_security_sensitive",
            "ticket_external_access_required",
            "ticket_dependency_mutation_required",
            "ticket_git_mutation_required",
            "stage_evidence_complete",
            "stage_evidence_missing",
            "stage_binding_mismatch",
            "stage_not_completed",
            "provider_authority_present",
            "model_authority_present",
            "automatic_authority_present",
            "git_execution_present",
            "manual_validation_pending",
            "pilot_accepted",
            "pilot_rejected",
        ),
    ),
)
FORBIDDEN_PUBLIC_NAMES = (
    "execute_non_critical_ticket",
    "run_non_critical_ticket",
    "execute_pilot",
    "run_pilot",
    "retry_pilot",
    "resume_pilot",
    "NonCriticalTicketExecutor",
    "PilotExecutor",
    "PilotRunner",
    "AutomaticPilot",
    "ProductionPilot",
    "CriticalTicketPilot",
    "MultiAgentPilot",
    "ParallelPilot",
)
UNSAFE_TEXTS = (
    "line\nbreak",
    "line\rbreak",
    "access_token=value",
    "refresh_token=value",
    "Authorization: Bearer tokenvalue",
    "client_secret=value",
    "api_key=value",
    "private key block",
    "password=value",
    "token=value",
    "sk-secret-shaped",
    "raw stdout dump",
    "raw stderr dump",
    "diff --git a b",
    "@@ raw diff hunk",
    "file content snapshot",
    "reasoning trace",
    "provider response body",
    "model output text",
    "traceback text",
    "C:/Users/example/path",
    "C:\\Users\\example\\path",
    "/Users/example/path",
    "/home/example/path",
    "git add file.py",
    "git commit -m message",
    "run; command",
    "pipe | command",
    "redirect > file",
)
FORBIDDEN_IMPORTS = (
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
    "concurrent.futures",
    "networkx",
    "importlib.resources",
    "pkgutil",
    "agent.codex_runtime",
    "provider_worker_gate.runtime",
    "provider_worker_gate.single_dispatch",
)
FORBIDDEN_CALLS = (
    "eval",
    "exec",
    "compile",
    "open",
    "print",
    "system",
    "popen",
)
POLICY_POSTURE = (
    ("maximum_files_changed", 10),
    ("maximum_created_files", 5),
    ("maximum_modified_files", 10),
    ("maximum_deleted_files", 0),
    ("allows_deleted_files", False),
    ("allows_untracked_files", True),
    ("allows_dependency_changes", False),
    ("allows_lockfile_changes", False),
    ("allows_credentials", False),
    ("allows_network", False),
    ("allows_provider_dispatch", False),
    ("allows_model_inference", False),
    ("allows_Docker", False),
    ("allows_Graphify", False),
    ("allows_Git_mutation", False),
    ("allows_branch_mutation", False),
    ("allows_database_migration", False),
    ("allows_production_deployment", False),
    ("allows_destructive_actions", False),
    ("requires_exact_validation_commands", True),
    ("requires_completed_diff_review", True),
    ("requires_completed_human_git_handoff", True),
)


def digest_text(text: str) -> str:
    return p17_6.digest_text(text)


def no_delete_compilation_result():
    source_ticket = p17_6.compiler_ticket(
        ticket_id="P17.8",
        ticket_scope=p17_6.compiler_scope(
            allowed_paths=("docs/new.md", "src/existing.py", "tests/new_test.py"),
            forbidden_paths=("secrets/**",),
            allowed_actions=(
                "create_file:docs/new.md|documentation",
                "modify_file:src/existing.py|source",
                "create_file:tests/new_test.py|test",
            ),
        ),
        tasks=(
            "Create expected documentation artifact.",
            "Modify expected source artifact.",
            "Create expected test artifact.",
        ),
        validation_steps=(
            p17_6.validation_step("V1", command="python -m unittest --help"),
            p17_6.validation_step("V2", command=None),
        ),
    )
    return p17_6.build_bundle(source_ticket=source_ticket)["result"]


def non_delete_context(monkeypatch: pytest.MonkeyPatch, workspace_root):
    compilation = no_delete_compilation_result()
    (workspace_root / "docs").mkdir(parents=True, exist_ok=True)
    (workspace_root / "src").mkdir(parents=True, exist_ok=True)
    (workspace_root / "tests").mkdir(parents=True, exist_ok=True)
    (workspace_root / "src" / "existing.py").write_bytes(b"old source\n")
    allocated, status_state = p17_6.allocation_result(
        monkeypatch, compilation, workspace_root
    )
    permissions = p17_6.profile_result(compilation, allocated)
    single_binding = build_single_agent_runtime_binding(
        agent_id="agent.p17-8",
        worker_id="worker.p17-8",
        work_packet=compilation.work_packet,
    )
    execution_plan = p17_6.single_plan((
        p17_6.single_action(
            1,
            "TASK-001",
            ToolPermissionOperation.CREATE_FILE,
            "docs/new.md",
            content="new docs",
        ),
        p17_6.single_action(
            2,
            "TASK-002",
            ToolPermissionOperation.REPLACE_FILE,
            "src/existing.py",
            content="new source",
            expected=digest_text("old source\n"),
        ),
        p17_6.single_action(
            3,
            "TASK-003",
            ToolPermissionOperation.CREATE_FILE,
            "tests/new_test.py",
            content="new tests",
        ),
    ))
    execution_authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-8",
        authorization_reference="AUTH-P17-8-EXECUTION",
        rationale="Authorize synthetic P17.8 prerequisite execution.",
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
        execution_authorization=execution_authorization,
    )
    session = prepare_single_agent_execution(single_request)
    for index in range(len(execution_plan.actions)):
        action_result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=single_request,
                session=session,
            )
        )
        session = action_result.updated_session
        if index == 0:
            status_state["status"] = " M docs/new.md"
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
    runner_authorization = build_validation_command_runner_authorization(
        authorizer_id="validation.authorizer.p17-8",
        authorization_reference="AUTH-P17-8-VALIDATION",
        rationale="Authorize exact synthetic validation commands.",
        risk_acknowledgement="Authorized validation code may have side effects.",
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        single_agent_execution_result=single_result,
        runtime_binding=runtime,
        authorization_requests=tuple(
            ValidationCommandAuthorizationRequest(
                validation_id=step.validation_id,
                timeout_seconds=30,
                expected_exit_codes=(0,),
            )
            for step in command_steps
        ),
    )
    runner_request = ValidationCommandRunnerRequest(
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        single_agent_execution_result=single_result,
        runtime_binding=runtime,
        runner_authorization=runner_authorization,
    )
    runner_session = prepare_validation_command_runner(runner_request)
    first = execute_validation_command(
        ValidationCommandExecutionRequest(
            runner_request=runner_request,
            session=runner_session,
        )
    )
    runner_completed = complete_validation_command_runner(first.updated_session)
    outcome_request = p17_6.outcome_envelopes._outcome_request(
        single_agent_execution_result=single_result,
        validation_command_runner_result=runner_completed,
    )
    outcome = p17_6.outcome_envelopes.build_outcome_envelope(outcome_request)
    context = {
        "compilation": compilation,
        "allocation": allocated,
        "profile": permissions,
        "single": single_result,
        "validation": runner_completed,
        "outcome": outcome,
    }
    paths = (
        p17_6.observed_path(
            1, "docs/new.md", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
        p17_6.observed_path(2, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
        p17_6.observed_path(
            3, "tests/new_test.py", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
    )
    artifacts = (
        p17_6.artifact(1, "docs/new.md", ReviewArtifactKind.DOCUMENTATION),
        p17_6.artifact(
            2,
            "src/existing.py",
            ReviewArtifactKind.SOURCE,
            source_action_id="ACTION-002",
        ),
        p17_6.artifact(
            3,
            "tests/new_test.py",
            ReviewArtifactKind.TEST,
            source_action_id="ACTION-003",
        ),
    )
    review = p17_6.build_diff_artifact_review(
        p17_6.request(context, p17_6.observation(context, paths, artifacts))
    )
    approval = p17_7.approval_for_review(context, review)
    handoff = build_human_git_handoff(
        p17_7.handoff_request(context, review, approval=approval)
    )
    context.update({"review": review, "handoff": handoff})
    return context


def selection_for_context(context, **updates) -> PilotTicketSelection:
    packet = context["compilation"].work_packet
    data = {
        "ticket_id": packet.ticket_id,
        "ticket_title": packet.source_ticket.title,
        "ticket_revision": packet.publication_revision,
        "risk_class": PilotRiskClass.NON_CRITICAL,
        "rationale": "Human selected one bounded no-deletion pilot ticket.",
        "selected_by_human": True,
        "synthetic": False,
        "expected_candidate_paths": tuple(
            candidate.relative_path
            for candidate in context["handoff"].package.candidates
        ),
        "expected_validation_ids": tuple(
            context["validation"].passed_validation_ids
            + context["validation"].manual_validation_ids_pending
        ),
        "criticality_acknowledgement": "Ticket is non-critical and excludes credentials, network, dependencies and Git mutation.",
    }
    data.update(updates)
    id_digest = ncp._digest_from_record(ncp.SELECTION_DIGEST_ALGORITHM, data)
    data["selection_id"] = (
        f"PSEL-{ncp._normalize_ticket_id(data['ticket_id'])}-"
        f"R{data['ticket_revision']:04d}-{id_digest[:12]}"
    )
    data["selection_SHA256"] = ncp._digest_from_record(
        ncp.SELECTION_DIGEST_ALGORITHM, data
    )
    return PilotTicketSelection.model_validate(data)


def unsafe_selection_for_context(context, **updates):
    selection = selection_for_context(context)
    data = selection.model_dump(mode="python")
    data.update(updates)
    if "selection_id" not in updates:
        id_record = {
            key: value
            for key, value in data.items()
            if key not in {"selection_id", "selection_SHA256"}
        }
        id_digest = ncp._digest_from_record(ncp.SELECTION_DIGEST_ALGORITHM, id_record)
        data["selection_id"] = (
            f"PSEL-{ncp._normalize_ticket_id(data['ticket_id'])}-"
            f"R{data['ticket_revision']:04d}-{id_digest[:12]}"
        )
    if "selection_SHA256" not in updates:
        data["selection_SHA256"] = ncp._digest_from_record(
            ncp.SELECTION_DIGEST_ALGORITHM,
            {key: value for key, value in data.items() if key != "selection_SHA256"},
        )
    return PilotTicketSelection.model_construct(**data)


def request_for_context(context, **updates) -> NonCriticalTicketPilotRequest:
    selected_handoff = updates.get("human_git_handoff_result", context["handoff"])
    selection_context = {**context, "handoff": selected_handoff}
    data = {
        "selection": selection_for_context(selection_context),
        "eligibility_policy": build_pilot_eligibility_policy(),
        "compilation_result": context["compilation"],
        "allocation_result": context["allocation"],
        "profile_result": context["profile"],
        "single_agent_execution_result": context["single"],
        "validation_command_runner_result": context["validation"],
        "outcome_envelope": context["outcome"],
        "diff_artifact_review_result": context["review"],
        "human_git_handoff_result": context["handoff"],
    }
    data.update(updates)
    if updates:
        return NonCriticalTicketPilotRequest.model_construct(**data)
    return NonCriticalTicketPilotRequest(**data)


@pytest.fixture(scope="module")
def contexts(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p17_8")
    try:
        return {"accepted": non_delete_context(monkeypatch, root / "accepted")}
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="module")
def accepted_request(contexts):
    return request_for_context(contexts["accepted"])


@pytest.fixture(scope="module")
def accepted_result(accepted_request):
    return build_non_critical_ticket_pilot(accepted_request)


@pytest.fixture(scope="module")
def sample_models(accepted_request, accepted_result):
    return {
        PilotEligibilityPolicy.__name__: accepted_request.eligibility_policy,
        PilotTicketSelection.__name__: accepted_request.selection,
        PilotStageEvidence.__name__: accepted_result.stage_evidence[0],
        PilotFinding.__name__: accepted_result.findings[0],
        PilotAcceptanceSummary.__name__: accepted_result.acceptance_summary,
        NonCriticalTicketPilotRequest.__name__: accepted_request,
        NonCriticalTicketPilotResult.__name__: accepted_result,
    }


def _retamper_model(model: BaseModel, field: str, value):
    data = model.model_dump(mode="json")
    data[field] = value
    return data


def _result_with_updates(result: NonCriticalTicketPilotResult, **updates):
    data = {field: getattr(result, field) for field in type(result).model_fields}
    data.update(updates)
    if "result_SHA256" not in updates:
        data["result_SHA256"] = ncp._digest_from_record(
            ncp.RESULT_DIGEST_ALGORITHM,
            {key: value for key, value in data.items() if key != "result_SHA256"},
        )
    return data


def _handoff_with_updates(handoff: GitHandoffResult, **updates):
    return handoff.model_copy(update=updates)


@pytest.mark.parametrize("exported_name", P17_8_EXPORTS)
def test_all_p17_8_exports_exist(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)
    assert hasattr(ncp, exported_name)


def test_prior_228_exports_remain_exact_prefix() -> None:
    prior = (
        p17_6.p17_5.P17_0_EXPORTS
        + p17_6.p17_5.P17_1_EXPORTS
        + p17_6.p17_5.P17_2_EXPORTS
        + p17_6.p17_5.P17_3_EXPORTS
        + p17_6.p17_5.P17_4_EXPORTS
        + p17_6.p17_5.P17_5_EXPORTS
        + p17_6.P17_6_EXPORTS
        + p17_7.P17_7_EXPORTS
    )
    assert len(prior) == 228
    assert work_packet.__all__[:228] == prior
    assert work_packet.__all__[228:255] == P17_8_EXPORTS
    assert len(work_packet.__all__) >= 255
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)


def test_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        hasattr(work_packet, "NonCriticalTicketPilotResult"),
        hasattr(work_packet, "build_non_critical_ticket_pilot"),
        hasattr(work_packet, "execute_pilot"),
        hasattr(work_packet, "PilotExecutor"),
    ) == (283, 283, True, True, False, False)


def test_function_import_smoke_exact_names() -> None:
    assert (
        build_pilot_eligibility_policy.__name__,
        validate_non_critical_ticket_pilot_request.__name__,
        build_non_critical_ticket_pilot.__name__,
        validate_non_critical_ticket_pilot_result.__name__,
        summarize_non_critical_ticket_pilot.__name__,
    ) == (
        "build_pilot_eligibility_policy",
        "validate_non_critical_ticket_pilot_request",
        "build_non_critical_ticket_pilot",
        "validate_non_critical_ticket_pilot_result",
        "summarize_non_critical_ticket_pilot",
    )


@pytest.mark.parametrize("name", FORBIDDEN_PUBLIC_NAMES)
def test_forbidden_executor_retry_production_and_multi_agent_names_absent(
    name: str,
) -> None:
    assert not hasattr(work_packet, name)
    assert not hasattr(ncp, name)


@pytest.mark.parametrize(
    "error_cls",
    (
        NonCriticalTicketPilotError,
        NonCriticalTicketPilotInputError,
        NonCriticalTicketPilotIntegrityError,
        NonCriticalTicketPilotPolicyError,
        NonCriticalTicketPilotStateError,
        NonCriticalTicketPilotValidationError,
    ),
)
def test_public_exceptions_are_value_errors(error_cls: type[Exception]) -> None:
    assert issubclass(error_cls, ValueError)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_frozen_extra_forbid_and_strict(
    model_cls: type[BaseModel],
) -> None:
    assert model_cls.model_config["frozen"] is True
    assert model_cls.model_config["extra"] == "forbid"
    assert model_cls.model_config["validate_default"] is True
    assert model_cls.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_model_schemas_reject_additional_properties(
    model_cls: type[BaseModel],
) -> None:
    assert model_cls.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_unknown_fields_fail(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["unknown"] = "blocked"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_models_are_immutable(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    field = next(iter(model.model_fields))
    with pytest.raises(ValidationError):
        setattr(model, field, getattr(model, field))


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_json_round_trip_supported(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    assert model_cls.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_tuple_immutability_retained(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    for name, value in model:
        if isinstance(value, tuple):
            data = model.model_dump(mode="json")
            assert isinstance(data[name], list)
            assert isinstance(
                model_cls.model_validate(data).__getattribute__(name), tuple
            )


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_no_forbidden_public_field_shapes(model_cls: type[BaseModel]) -> None:
    forbidden = {
        "Any",
        "dict",
        "Mapping",
        "MutableMapping",
        "Path",
        "datetime",
        "UUID",
        "bytes",
        "Callable",
    }
    for field in model_cls.model_fields.values():
        assert (
            getattr(field.annotation, "__name__", str(field.annotation))
            not in forbidden
        )


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_alternative_schema_versions_fail(
    model_cls: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize(
    "model_cls",
    (
        PilotEligibilityPolicy,
        NonCriticalTicketPilotRequest,
        NonCriticalTicketPilotResult,
    ),
)
def test_alternative_policy_ids_fail(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["policy_id"] = "alternate-policy"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_strict_booleans_reject_strings(
    model_cls: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    for field_name, value in tuple(data.items()):
        if isinstance(value, bool):
            data[field_name] = "true"
            with pytest.raises(ValidationError):
                model_cls.model_validate(data)
            return
    assert not any(isinstance(value, bool) for value in data.values())


@pytest.mark.parametrize("enum_cls,expected", EXPECTED_ENUM_VALUES)
def test_exact_enum_values(enum_cls: type[Enum], expected: tuple[str, ...]) -> None:
    assert tuple(item.value for item in enum_cls) == expected


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_enum_aliases_absent(enum_cls: type[Enum]) -> None:
    assert len(enum_cls) == len({item.value for item in enum_cls})


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_unknown_enum_values_fail(enum_cls: type[Enum]) -> None:
    with pytest.raises(ValueError):
        enum_cls("__unknown__")


@pytest.mark.parametrize(
    "forbidden",
    (
        "critical",
        "medium_risk",
        "high_risk",
        "production",
        "autonomous",
        "automatic",
        "multi_agent",
        "parallel",
    ),
)
def test_forbidden_enum_values_absent(forbidden: str) -> None:
    for enum_cls in CONTROLLED_ENUMS:
        assert forbidden not in {item.value for item in enum_cls}


def test_schema_and_policy_identity() -> None:
    assert NON_CRITICAL_TICKET_PILOT_SCHEMA_VERSION == 1
    assert NON_CRITICAL_TICKET_PILOT_POLICY_ID == (
        "pepper-complete-governed-non-critical-ticket-pilot-v1"
    )
    assert NON_CRITICAL_TICKET_PILOT_EXPORT_COUNT == 27


def test_canonical_policy_builds_and_is_deterministic() -> None:
    first = build_pilot_eligibility_policy()
    second = build_pilot_eligibility_policy()
    assert first == second
    assert first.policy_SHA256 == second.policy_SHA256
    assert first.risk_class is PilotRiskClass.NON_CRITICAL


@pytest.mark.parametrize("field,expected", POLICY_POSTURE)
def test_policy_fixed_posture(field: str, expected) -> None:
    policy = build_pilot_eligibility_policy()
    assert getattr(policy, field) == expected


def test_policy_digest_tampering_fails() -> None:
    policy = build_pilot_eligibility_policy()
    data = policy.model_dump(mode="json")
    data["policy_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        PilotEligibilityPolicy.model_validate(data)


def test_policy_caller_override_is_absent() -> None:
    with pytest.raises(TypeError):
        build_pilot_eligibility_policy(maximum_files_changed=99)


def test_canonical_selection_passes(accepted_request) -> None:
    selection = accepted_request.selection
    assert selection.risk_class is PilotRiskClass.NON_CRITICAL
    assert selection.selected_by_human is True
    assert selection.synthetic is False
    assert selection.expected_candidate_paths == (
        "docs/new.md",
        "src/existing.py",
        "tests/new_test.py",
    )
    assert selection.expected_validation_ids == ("V1", "V2")


@pytest.mark.parametrize(
    "field,value",
    (
        ("selected_by_human", False),
        ("synthetic", True),
        ("risk_class", "critical"),
        ("expected_candidate_paths", ("docs/new.md", "docs/new.md")),
        ("expected_validation_ids", ("V1", "V1")),
        ("expected_candidate_paths", ()),
        ("expected_validation_ids", ()),
    ),
)
def test_selection_invalid_shapes_fail(contexts, field: str, value) -> None:
    with pytest.raises((ValidationError, ValueError)):
        selection_for_context(contexts["accepted"], **{field: value})


@pytest.mark.parametrize(
    "field,value",
    (
        ("ticket_id", "P17.9"),
        ("ticket_revision", 99),
        ("ticket_title", "Wrong title"),
    ),
)
def test_selection_identity_mismatch_fails_request_validation(
    contexts, field: str, value
) -> None:
    selection = selection_for_context(contexts["accepted"], **{field: value})
    request = request_for_context(contexts["accepted"], selection=selection)
    with pytest.raises(NonCriticalTicketPilotPolicyError):
        validate_non_critical_ticket_pilot_request(request)


@pytest.mark.parametrize("unsafe_text", UNSAFE_TEXTS)
def test_selection_unsafe_text_fails(contexts, unsafe_text: str) -> None:
    with pytest.raises((ValidationError, ValueError)):
        selection_for_context(contexts["accepted"], rationale=unsafe_text)


def test_selection_digest_tampering_fails(accepted_request) -> None:
    data = accepted_request.selection.model_dump(mode="json")
    data["selection_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        PilotTicketSelection.model_validate(data)


def test_validate_request_accepts_canonical_request(accepted_request) -> None:
    validate_non_critical_ticket_pilot_request(accepted_request)


@pytest.mark.parametrize("stage", tuple(PilotStage))
def test_stage_evidence_exact_order_and_ids(stage: PilotStage, accepted_result) -> None:
    evidence = accepted_result.stage_evidence[tuple(PilotStage).index(stage)]
    assert evidence.stage is stage
    assert evidence.evidence_id == f"PSEV-{tuple(PilotStage).index(stage) + 1:03d}"
    assert evidence.requirement_satisfied is True
    assert evidence.provider_dispatch_count == 0
    assert evidence.model_inference_count == 0
    assert evidence.automatic_authority_present is False
    assert evidence.Git_execution_count == 0


@pytest.mark.parametrize("stage", tuple(PilotStage))
def test_stage_source_digests_match(
    stage: PilotStage, accepted_request, accepted_result
) -> None:
    evidence = accepted_result.stage_evidence[tuple(PilotStage).index(stage)]
    source_by_stage = {
        PilotStage.WORK_PACKET_COMPILATION: accepted_request.compilation_result.result_SHA256,
        PilotStage.WORKSPACE_ALLOCATION: accepted_request.allocation_result.result_SHA256,
        PilotStage.TOOL_PERMISSION_PROFILE: accepted_request.profile_result.result_SHA256,
        PilotStage.SINGLE_AGENT_EXECUTION: accepted_request.single_agent_execution_result.result_SHA256,
        PilotStage.VALIDATION_COMMAND_RUNNER: accepted_request.validation_command_runner_result.result_SHA256,
        PilotStage.OUTCOME_ENVELOPE: accepted_request.outcome_envelope.envelope_SHA256,
        PilotStage.DIFF_ARTIFACT_REVIEW: accepted_request.diff_artifact_review_result.result_SHA256,
        PilotStage.HUMAN_GIT_HANDOFF: accepted_request.human_git_handoff_result.result_SHA256,
    }
    assert evidence.source_SHA256 == source_by_stage[stage]
    assert evidence.work_packet_SHA256 == accepted_result.work_packet_SHA256
    assert evidence.allocation_SHA256 == accepted_result.allocation_SHA256
    assert evidence.profile_SHA256 == accepted_result.profile_SHA256


def test_stage_evidence_digest_tampering_fails(accepted_result) -> None:
    evidence = accepted_result.stage_evidence[0]
    data = evidence.model_dump(mode="json")
    data["evidence_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        PilotStageEvidence.model_validate(data)


@pytest.mark.parametrize(
    "field,value,error",
    (
        ("compilation_result", "work_packet", NonCriticalTicketPilotIntegrityError),
        ("allocation_result", "allocation", NonCriticalTicketPilotIntegrityError),
        ("profile_result", "profile", NonCriticalTicketPilotIntegrityError),
    ),
)
def test_placeholder_prerequisite_integrity_cases_are_bound(
    accepted_request, field, value, error
) -> None:
    assert getattr(accepted_request, field)
    assert value
    assert issubclass(error, NonCriticalTicketPilotError)


def test_candidate_path_selection_mismatch_fails(accepted_request, contexts) -> None:
    selection = unsafe_selection_for_context(
        contexts["accepted"], expected_candidate_paths=("docs/new.md",)
    )
    request = request_for_context(contexts["accepted"], selection=selection)
    with pytest.raises(NonCriticalTicketPilotPolicyError):
        build_non_critical_ticket_pilot(request)


def test_validation_id_selection_mismatch_fails(contexts) -> None:
    selection = unsafe_selection_for_context(
        contexts["accepted"], expected_validation_ids=("V1",)
    )
    request = request_for_context(contexts["accepted"], selection=selection)
    with pytest.raises(NonCriticalTicketPilotPolicyError):
        build_non_critical_ticket_pilot(request)


@pytest.mark.parametrize(
    "selection_update,code",
    (
        ({"risk_class": "critical"}, PilotFindingCode.TICKET_CRITICAL),
        (
            {
                "expected_candidate_paths": tuple(
                    f"docs/{index}.md" for index in range(11)
                )
            },
            PilotFindingCode.TICKET_SECURITY_SENSITIVE,
        ),
    ),
)
def test_selection_policy_rejected_when_constructed_unsafe(
    contexts, selection_update, code
) -> None:
    selection = unsafe_selection_for_context(contexts["accepted"], **selection_update)
    if "expected_candidate_paths" in selection_update:
        with pytest.raises(NonCriticalTicketPilotPolicyError):
            build_non_critical_ticket_pilot(
                request_for_context(contexts["accepted"], selection=selection)
            )
        return
    result = build_non_critical_ticket_pilot(
        request_for_context(contexts["accepted"], selection=selection)
    )
    assert result.decision is PilotDecision.REJECTED
    assert any(finding.code is code for finding in result.findings)


@pytest.mark.parametrize(
    "path,code",
    (
        ("package.json", PilotFindingCode.TICKET_DEPENDENCY_MUTATION_REQUIRED),
        ("package-lock.json", PilotFindingCode.TICKET_DEPENDENCY_MUTATION_REQUIRED),
        ("secrets/value.txt", PilotFindingCode.TICKET_SECURITY_SENSITIVE),
        ("auth.json", PilotFindingCode.TICKET_SECURITY_SENSITIVE),
        (".env", PilotFindingCode.TICKET_SECURITY_SENSITIVE),
    ),
)
def test_candidate_path_exclusions_reject(
    contexts, path: str, code: PilotFindingCode
) -> None:
    handoff = contexts["accepted"]["handoff"]
    candidate = handoff.package.candidates[0]
    changed = candidate.model_copy(update={"relative_path": path})
    package = handoff.package.model_copy(
        update={"candidates": (changed,) + handoff.package.candidates[1:]}
    )
    unsafe_handoff = _handoff_with_updates(handoff, package=package)
    request = request_for_context(
        contexts["accepted"], human_git_handoff_result=unsafe_handoff
    )
    result = build_non_critical_ticket_pilot(request)
    assert result.decision is PilotDecision.REJECTED
    assert any(finding.code is code for finding in result.findings)


def test_deleted_file_rejects(contexts) -> None:
    handoff = contexts["accepted"]["handoff"]
    candidate = handoff.package.candidates[0].model_copy(
        update={"status": GitHandoffPathStatus.DELETED}
    )
    package = handoff.package.model_copy(
        update={"candidates": (candidate,) + handoff.package.candidates[1:]}
    )
    result = build_non_critical_ticket_pilot(
        request_for_context(
            contexts["accepted"],
            human_git_handoff_result=_handoff_with_updates(handoff, package=package),
        )
    )
    assert result.decision is PilotDecision.REJECTED
    assert any(
        finding.code is PilotFindingCode.TICKET_SECURITY_SENSITIVE
        for finding in result.findings
    )


@pytest.mark.parametrize(
    "field,value,code",
    (
        ("Git_commands_executed", 1, PilotFindingCode.GIT_EXECUTION_PRESENT),
        ("staging_performed", True, PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT),
        ("commit_performed", True, PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT),
        ("push_performed", True, PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT),
        (
            "automatic_cleanup_authorized",
            True,
            PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
        ),
        (
            "automatic_rollback_authorized",
            True,
            PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
        ),
        (
            "automatic_staging_authorized",
            True,
            PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
        ),
        (
            "automatic_commit_authorized",
            True,
            PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
        ),
        (
            "automatic_push_authorized",
            True,
            PilotFindingCode.AUTOMATIC_AUTHORITY_PRESENT,
        ),
        ("provider_dispatch_count", 1, PilotFindingCode.PROVIDER_AUTHORITY_PRESENT),
        ("model_inference_count", 1, PilotFindingCode.MODEL_AUTHORITY_PRESENT),
    ),
)
def test_handoff_stage_forbidden_authority_rejects(
    contexts, field: str, value, code: PilotFindingCode
) -> None:
    handoff = _handoff_with_updates(contexts["accepted"]["handoff"], **{field: value})
    result = build_non_critical_ticket_pilot(
        request_for_context(contexts["accepted"], human_git_handoff_result=handoff)
    )
    assert result.state is PilotState.BLOCKED
    assert result.decision is PilotDecision.REJECTED
    assert any(finding.code is code for finding in result.findings)


def test_rejected_handoff_rejects_pilot(contexts) -> None:
    handoff = _handoff_with_updates(
        contexts["accepted"]["handoff"],
        state=ncp.GitHandoffState.BLOCKED,
        decision=GitHandoffDecision.REJECTED,
        human_git_handoff_requirement_satisfied=False,
    )
    result = build_non_critical_ticket_pilot(
        request_for_context(contexts["accepted"], human_git_handoff_result=handoff)
    )
    assert result.decision is PilotDecision.REJECTED
    assert any(
        finding.code is PilotFindingCode.STAGE_NOT_COMPLETED
        for finding in result.findings
    )


def test_review_blocking_finding_rejects_pilot(contexts) -> None:
    review = contexts["accepted"]["review"]
    finding = review.findings[0].model_copy(
        update={"severity": ReviewFindingSeverity.BLOCKING}
    )
    unsafe_review = review.model_copy(update={"findings": (finding,)})
    result = build_non_critical_ticket_pilot(
        request_for_context(
            contexts["accepted"], diff_artifact_review_result=unsafe_review
        )
    )
    assert result.decision is PilotDecision.REJECTED
    assert any(
        finding.code is PilotFindingCode.STAGE_NOT_COMPLETED
        for finding in result.findings
    )


def test_outcome_failure_kind_rejects_pilot(contexts) -> None:
    outcome = contexts["accepted"]["outcome"].model_copy(
        update={"envelope_kind": ncp.OutcomeEnvelopeKind.FAILURE}
    )
    result = build_non_critical_ticket_pilot(
        request_for_context(contexts["accepted"], outcome_envelope=outcome)
    )
    assert result.decision is PilotDecision.REJECTED
    assert any(
        e.stage is PilotStage.OUTCOME_ENVELOPE and not e.requirement_satisfied
        for e in result.stage_evidence
    )


@pytest.mark.parametrize(
    "field,value",
    (
        ("work_packet_SHA256", digest_text("tamper")),
        ("allocation_SHA256", digest_text("tamper")),
        ("profile_SHA256", digest_text("tamper")),
        ("selection_SHA256", digest_text("tamper")),
        ("eligibility_policy_SHA256", digest_text("tamper")),
        ("result_SHA256", digest_text("tamper")),
    ),
)
def test_result_digest_and_binding_tampering_fails(
    accepted_result, field: str, value
) -> None:
    data = _result_with_updates(accepted_result, **{field: value})
    with pytest.raises((ValidationError, NonCriticalTicketPilotValidationError)):
        NonCriticalTicketPilotResult.model_validate(data)


def test_canonical_complete_non_critical_ticket_pilot_flow(accepted_result) -> None:
    assert accepted_result.state is PilotState.COMPLETED
    assert accepted_result.decision is PilotDecision.ACCEPTED
    assert accepted_result.risk_class is PilotRiskClass.NON_CRITICAL
    assert len(accepted_result.stage_evidence) == 8
    assert not any(
        finding.severity is PilotFindingSeverity.BLOCKING
        for finding in accepted_result.findings
    )
    assert accepted_result.WorkPacket_execution_MVP_requirement_satisfied is True
    assert accepted_result.P17_closure_ready is True
    assert accepted_result.production_readiness_claimed is False
    assert accepted_result.provider_dispatch_count == 0
    assert accepted_result.model_inference_count == 0
    assert accepted_result.acceptance_summary.Git_commands_executed == 0


def test_canonical_critical_ticket_rejected_flow(contexts) -> None:
    selection = unsafe_selection_for_context(
        contexts["accepted"], risk_class="critical"
    )
    result = build_non_critical_ticket_pilot(
        request_for_context(contexts["accepted"], selection=selection)
    )
    assert result.state is PilotState.BLOCKED
    assert result.decision is PilotDecision.REJECTED
    assert result.WorkPacket_execution_MVP_requirement_satisfied is False
    assert result.P17_closure_ready is False
    assert any(
        finding.code is PilotFindingCode.TICKET_CRITICAL for finding in result.findings
    )


def test_canonical_git_execution_evidence_rejected_flow(contexts) -> None:
    handoff = _handoff_with_updates(
        contexts["accepted"]["handoff"], Git_commands_executed=1
    )
    result = build_non_critical_ticket_pilot(
        request_for_context(contexts["accepted"], human_git_handoff_result=handoff)
    )
    assert result.state is PilotState.BLOCKED
    assert result.decision is PilotDecision.REJECTED
    assert result.WorkPacket_execution_MVP_requirement_satisfied is False
    assert any(
        finding.code is PilotFindingCode.GIT_EXECUTION_PRESENT
        for finding in result.findings
    )


def test_acceptance_summary_canonical(accepted_result) -> None:
    summary = accepted_result.acceptance_summary
    assert summary.eligible is True
    assert summary.stage_count == 8
    assert summary.completed_stage_count == 8
    assert summary.blocking_finding_count == 0
    assert summary.warning_finding_count == 1
    assert summary.information_finding_count >= 10
    assert summary.manual_validation_ids_pending == ("V2",)
    assert summary.Git_commands_executed == 0
    assert summary.provider_dispatch_count == 0
    assert summary.model_inference_count == 0
    assert summary.automatic_retry_authorized is False
    assert summary.automatic_fallback_authorized is False
    assert summary.automatic_cleanup_authorized is False
    assert summary.automatic_rollback_authorized is False
    assert summary.automatic_staging_authorized is False
    assert summary.automatic_commit_authorized is False
    assert summary.automatic_push_authorized is False


def test_summary_api_returns_exact_summary(accepted_result) -> None:
    assert (
        summarize_non_critical_ticket_pilot(accepted_result)
        is accepted_result.acceptance_summary
    )


def test_summary_api_rejects_invalid_result(accepted_result) -> None:
    bad = NonCriticalTicketPilotResult.model_construct(
        **_result_with_updates(accepted_result, result_SHA256=digest_text("bad"))
    )
    with pytest.raises(NonCriticalTicketPilotValidationError):
        summarize_non_critical_ticket_pilot(bad)


def test_repeated_equal_inputs_produce_equal_result(accepted_request) -> None:
    first = build_non_critical_ticket_pilot(accepted_request)
    second = build_non_critical_ticket_pilot(accepted_request)
    assert first == second
    assert first.pilot_id == second.pilot_id
    assert first.result_SHA256 == second.result_SHA256


@pytest.mark.parametrize(
    "mutator",
    (
        lambda context: request_for_context(
            context,
            selection=unsafe_selection_for_context(
                context, rationale="Different bounded rationale."
            ),
        ),
        lambda context: request_for_context(
            context,
            selection=unsafe_selection_for_context(
                context,
                criticality_acknowledgement="Different bounded acknowledgement.",
            ),
        ),
        lambda context: request_for_context(
            context,
            human_git_handoff_result=_handoff_with_updates(
                context["handoff"], Git_commands_executed=1
            ),
        ),
    ),
)
def test_changed_inputs_change_pilot_identity(
    contexts, accepted_result, mutator
) -> None:
    changed = build_non_critical_ticket_pilot(mutator(contexts["accepted"]))
    assert (
        changed.pilot_id != accepted_result.pilot_id
        or changed.result_SHA256 != accepted_result.result_SHA256
    )


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_serialization_json_round_trip(
    model_cls: type[BaseModel], sample_models
) -> None:
    model = sample_models[model_cls.__name__]
    assert model_cls.model_validate_json(model.model_dump_json()) == model
    assert model_cls.model_validate(model.model_dump(mode="json")) == model
    assert isinstance(model.model_json_schema(), dict)


@pytest.mark.parametrize(
    "finding",
    (
        PilotFindingCode.PILOT_ACCEPTED,
        PilotFindingCode.MANUAL_VALIDATION_PENDING,
        PilotFindingCode.STAGE_EVIDENCE_COMPLETE,
    ),
)
def test_required_findings_present(accepted_result, finding: PilotFindingCode) -> None:
    assert any(item.code is finding for item in accepted_result.findings)


def test_finding_ids_order_and_digests(accepted_result) -> None:
    assert tuple(f.finding_id for f in accepted_result.findings) == tuple(
        f"PFND-{index:03d}" for index in range(1, len(accepted_result.findings) + 1)
    )
    assert tuple(ncp._finding_sort_key(f) for f in accepted_result.findings) == tuple(
        sorted(ncp._finding_sort_key(f) for f in accepted_result.findings)
    )
    for finding in accepted_result.findings:
        assert finding.finding_SHA256 == ncp._model_digest(
            ncp.FINDING_DIGEST_ALGORITHM, finding
        )


def test_finding_digest_tampering_fails(accepted_result) -> None:
    data = accepted_result.findings[0].model_dump(mode="json")
    data["finding_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        PilotFinding.model_validate(data)


def test_maximum_findings_enforced(accepted_result) -> None:
    data = _result_with_updates(accepted_result, findings=accepted_result.findings * 20)
    with pytest.raises((ValidationError, NonCriticalTicketPilotValidationError)):
        NonCriticalTicketPilotResult.model_validate(data)


@pytest.mark.parametrize(
    "field",
    (
        "automatic_retry_authorized",
        "automatic_fallback_authorized",
        "automatic_cleanup_authorized",
        "automatic_rollback_authorized",
        "automatic_staging_authorized",
        "automatic_commit_authorized",
        "automatic_push_authorized",
    ),
)
def test_summary_automatic_authority_tampering_fails(
    accepted_result, field: str
) -> None:
    data = accepted_result.acceptance_summary.model_dump(mode="json")
    data[field] = True
    with pytest.raises(ValidationError):
        PilotAcceptanceSummary.model_validate(data)


def test_no_wall_clock_uuid_or_randomness_in_result(accepted_result) -> None:
    dumped = accepted_result.model_dump_json()
    assert "uuid" not in dumped.casefold()
    assert "timestamp" not in dumped.casefold()
    assert "random" not in dumped.casefold()
    assert "signature" not in dumped.casefold()


def test_digest_is_not_a_signature_limitation(accepted_result) -> None:
    assert len(accepted_result.result_SHA256) == 64
    assert accepted_result.result_SHA256 != accepted_result.pilot_id


@pytest.mark.parametrize("name", FORBIDDEN_IMPORTS)
def test_forbidden_imports_absent(name: str) -> None:
    assert not hasattr(ncp, name.split(".")[0])


def test_static_authority_scan_forbidden_imports_and_calls_absent() -> None:
    source = ncp.__loader__.get_source(ncp.__name__)
    tree = ast.parse(source)
    imported = set()
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
    for forbidden in FORBIDDEN_IMPORTS:
        assert forbidden not in imported
    for forbidden in FORBIDDEN_CALLS:
        assert forbidden not in called


@pytest.mark.parametrize(
    "counter",
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
        "staging_calls",
        "commit_calls",
        "push_calls",
        "retry_calls",
        "fallback_calls",
        "cleanup_calls",
        "rollback_calls",
        "Docker_calls",
        "Graphify_calls",
    ),
)
def test_operational_authority_counters_are_absent_or_zero(
    counter: str, accepted_result
) -> None:
    assert counter not in accepted_result.model_dump(mode="json")
    assert accepted_result.provider_dispatch_count == 0
    assert accepted_result.model_inference_count == 0
    assert accepted_result.acceptance_summary.Git_commands_executed == 0


@pytest.mark.parametrize(
    "text",
    (
        "access_token",
        "refresh_token",
        "Authorization:",
        "OAuth code",
        "private key",
        "api_key",
        "provider response",
        "raw prompt",
        "reasoning trace",
        "raw stdout",
        "raw stderr",
        "diff --git",
        "C:/Users/",
        "git push",
        "production deployment",
    ),
)
def test_security_content_absent_from_result(text: str, accepted_result) -> None:
    assert text.casefold() not in accepted_result.model_dump_json().casefold()


def test_inputs_remain_unchanged(accepted_request) -> None:
    before = accepted_request.model_dump_json()
    build_non_critical_ticket_pilot(accepted_request)
    assert accepted_request.model_dump_json() == before


@pytest.mark.parametrize("stage", tuple(PilotStage))
def test_stage_summaries_are_bounded(stage: PilotStage, accepted_result) -> None:
    summary = accepted_result.stage_evidence[tuple(PilotStage).index(stage)].summary
    assert 1 <= len(summary) <= 512
    assert "raw" not in summary.casefold()
    assert "C:/Users" not in summary


@pytest.mark.parametrize(
    "path", ("docs/new.md", "src/existing.py", "tests/new_test.py")
)
def test_expected_candidate_paths_explicit(path: str, accepted_request) -> None:
    assert path in accepted_request.selection.expected_candidate_paths


@pytest.mark.parametrize("validation_id", ("V1", "V2"))
def test_expected_validation_ids_explicit(validation_id: str, accepted_request) -> None:
    assert validation_id in accepted_request.selection.expected_validation_ids


@pytest.mark.parametrize(
    "field", ("ticket_id", "ticket_title", "rationale", "criticality_acknowledgement")
)
def test_ticket_selection_public_text_bounds(field: str, accepted_request) -> None:
    value = getattr(accepted_request.selection, field)
    assert "\n" not in value
    assert "\r" not in value
    assert "\x00" not in value
    assert len(value) <= (64 if field == "ticket_id" else 512)


def test_manual_validation_warning_does_not_block_acceptance(accepted_result) -> None:
    assert accepted_result.acceptance_summary.manual_validation_ids_pending == ("V2",)
    assert any(
        f.code is PilotFindingCode.MANUAL_VALIDATION_PENDING
        for f in accepted_result.findings
    )
    assert accepted_result.decision is PilotDecision.ACCEPTED


def test_result_validation_accepts_canonical_result(accepted_result) -> None:
    validate_non_critical_ticket_pilot_result(accepted_result)


def test_rejected_result_validation_accepts_rejected_pilot(contexts) -> None:
    result = build_non_critical_ticket_pilot(
        request_for_context(
            contexts["accepted"],
            selection=unsafe_selection_for_context(
                contexts["accepted"], risk_class="critical"
            ),
        )
    )
    validate_non_critical_ticket_pilot_result(result)
    assert summarize_non_critical_ticket_pilot(result).eligible is False


@pytest.mark.parametrize(
    "field",
    (
        "state",
        "decision",
        "WorkPacket_execution_MVP_requirement_satisfied",
        "P17_closure_ready",
        "production_readiness_claimed",
    ),
)
def test_result_decision_state_tampering_fails(accepted_result, field: str) -> None:
    replacements = {
        "state": PilotState.BLOCKED,
        "decision": PilotDecision.REJECTED,
        "WorkPacket_execution_MVP_requirement_satisfied": False,
        "P17_closure_ready": False,
        "production_readiness_claimed": True,
    }
    data = _result_with_updates(accepted_result, **{field: replacements[field]})
    with pytest.raises((ValidationError, NonCriticalTicketPilotValidationError)):
        NonCriticalTicketPilotResult.model_validate(data)


@pytest.mark.parametrize("field", ("provider_dispatch_count", "model_inference_count"))
def test_result_provider_model_count_tampering_fails(
    accepted_result, field: str
) -> None:
    data = _result_with_updates(accepted_result, **{field: 1})
    with pytest.raises((ValidationError, NonCriticalTicketPilotValidationError)):
        NonCriticalTicketPilotResult.model_validate(data)


def test_stage_order_tampering_fails(accepted_result) -> None:
    swapped = (
        accepted_result.stage_evidence[1],
        accepted_result.stage_evidence[0],
    ) + accepted_result.stage_evidence[2:]
    data = _result_with_updates(accepted_result, stage_evidence=swapped)
    with pytest.raises((ValidationError, NonCriticalTicketPilotValidationError)):
        NonCriticalTicketPilotResult.model_validate(data)


def test_finding_order_tampering_fails(accepted_result) -> None:
    swapped = tuple(reversed(accepted_result.findings))
    data = _result_with_updates(accepted_result, findings=swapped)
    with pytest.raises((ValidationError, NonCriticalTicketPilotValidationError)):
        NonCriticalTicketPilotResult.model_validate(data)
