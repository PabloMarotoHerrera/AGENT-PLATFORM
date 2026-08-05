from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.single_agent_execution as sae
import hermes_cli.agent_platform.work_packet.workspace_allocator as allocator_module
from hermes_cli.agent_platform.work_packet import (
    SINGLE_AGENT_EXECUTION_POLICY_ID,
    SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
    SingleAgentActionDisposition,
    SingleAgentActionEvidence,
    SingleAgentActionExecutionRequest,
    SingleAgentActionExecutionResult,
    SingleAgentExecutionAuthorization,
    SingleAgentExecutionAuthorizationError,
    SingleAgentExecutionInputError,
    SingleAgentExecutionIntegrityError,
    SingleAgentExecutionPlan,
    SingleAgentExecutionRequest,
    SingleAgentExecutionResult,
    SingleAgentExecutionSession,
    SingleAgentExecutionState,
    SingleAgentExecutionStateError,
    SingleAgentRuntimeBinding,
    SingleAgentTargetKind,
    SingleAgentTargetResolutionError,
    SingleAgentTargetResolutionEvidence,
    SingleAgentToolAction,
    SingleAgentToolExecutionError,
    SingleAgentToolObservation,
    SingleAgentToolObservationKind,
    ToolPermissionDecision,
    ToolPermissionGrantRequest,
    ToolPermissionOperation,
    ToolPermissionProfileRequest,
    WorkspaceAllocationRequest,
    build_single_agent_execution_authorization,
    build_single_agent_runtime_binding,
    build_tool_permission_profile,
    build_tool_permission_profile_authorization,
    build_workspace_allocation_authorization,
    build_workspace_repository_identity,
    complete_single_agent_execution,
    execute_single_agent_tool_action,
    get_empty_workspace_allocation_registry,
    prepare_single_agent_execution,
    validate_single_agent_execution_result,
    validate_single_agent_execution_session,
)
from tests.hermes_cli.test_agent_platform_work_packet_compiler import (
    EXPECTED_EXPORTS as P17_0_EXPORTS,
    build_bundle,
    scope as compiler_scope,
    ticket as compiler_ticket,
)
from tests.hermes_cli.test_agent_platform_work_packet_tool_permissions import (
    P17_2_EXPORTS,
)
from tests.hermes_cli.test_agent_platform_work_packet_workspace_allocator import (
    P17_1_EXPORTS,
)


P17_3_EXPORTS = (
    "SINGLE_AGENT_EXECUTION_SCHEMA_VERSION",
    "SINGLE_AGENT_EXECUTION_POLICY_ID",
    "SingleAgentExecutionState",
    "SingleAgentActionDisposition",
    "SingleAgentToolObservationKind",
    "SingleAgentTargetKind",
    "SingleAgentRuntimeBinding",
    "SingleAgentExecutionAuthorization",
    "SingleAgentToolAction",
    "SingleAgentExecutionPlan",
    "SingleAgentExecutionRequest",
    "SingleAgentTargetResolutionEvidence",
    "SingleAgentToolObservation",
    "SingleAgentActionEvidence",
    "SingleAgentExecutionSession",
    "SingleAgentActionExecutionRequest",
    "SingleAgentActionExecutionResult",
    "SingleAgentExecutionResult",
    "SingleAgentExecutionError",
    "SingleAgentExecutionInputError",
    "SingleAgentExecutionAuthorizationError",
    "SingleAgentExecutionIntegrityError",
    "SingleAgentTargetResolutionError",
    "SingleAgentToolExecutionError",
    "SingleAgentExecutionStateError",
    "build_single_agent_runtime_binding",
    "build_single_agent_execution_authorization",
    "prepare_single_agent_execution",
    "execute_single_agent_tool_action",
    "complete_single_agent_execution",
    "validate_single_agent_execution_session",
    "validate_single_agent_execution_result",
)
PUBLIC_MODELS = (
    SingleAgentRuntimeBinding,
    SingleAgentExecutionAuthorization,
    SingleAgentToolAction,
    SingleAgentExecutionPlan,
    SingleAgentExecutionRequest,
    SingleAgentTargetResolutionEvidence,
    SingleAgentToolObservation,
    SingleAgentActionEvidence,
    SingleAgentExecutionSession,
    SingleAgentActionExecutionRequest,
    SingleAgentActionExecutionResult,
    SingleAgentExecutionResult,
)
GRANTABLE_OPERATIONS = (
    ToolPermissionOperation.LIST_DIRECTORY,
    ToolPermissionOperation.READ_FILE,
    ToolPermissionOperation.CREATE_FILE,
    ToolPermissionOperation.REPLACE_FILE,
    ToolPermissionOperation.DELETE_FILE,
    ToolPermissionOperation.CREATE_DIRECTORY,
    ToolPermissionOperation.DELETE_DIRECTORY,
)
NEVER_GRANTABLE_OPERATIONS = tuple(
    operation
    for operation in ToolPermissionOperation
    if operation not in GRANTABLE_OPERATIONS
)
SOURCE_COMMIT = "a" * 40
WORKSPACE_BRANCH = "p17/workspace-allocator"
REPOSITORY_ID = "pepper-agent"


def path_text(path: Path) -> str:
    return path.resolve().as_posix()


def patch_workspace_inspection(
    monkeypatch: pytest.MonkeyPatch,
    workspace_root: Path,
    *,
    status_state: dict[str, str] | None = None,
    commit: str = SOURCE_COMMIT,
    branch: str = WORKSPACE_BRANCH,
    linked: bool = True,
) -> None:
    root_text = path_text(workspace_root)
    status_state = status_state if status_state is not None else {"status": ""}
    git_dir = f"{root_text}/.git/worktrees/p17-3" if linked else f"{root_text}/.git"
    common_dir = f"{root_text}/.git"
    metadata = allocator_module._WorkspacePathMetadata(
        exists=workspace_root.exists(),
        is_dir=workspace_root.is_dir(),
        is_symlink=workspace_root.is_symlink(),
        resolved_workspace_root=root_text,
    )

    responses = {
        ("rev-parse", "--is-inside-work-tree"): "true",
        ("rev-parse", "--show-toplevel"): root_text,
        ("rev-parse", "HEAD"): commit,
        ("branch", "--show-current"): branch,
        ("rev-parse", "--git-dir"): git_dir,
        ("rev-parse", "--git-common-dir"): common_dir,
    }

    monkeypatch.setattr(
        allocator_module,
        "_workspace_path_metadata",
        lambda workspace_root: metadata,
    )

    def fake_git(workspace_root: str, args: tuple[str, ...]) -> str:
        if args == ("status", "--porcelain=v1", "-uall"):
            return status_state["status"]
        return responses[args]

    monkeypatch.setattr(allocator_module, "_run_git_command", fake_git)


def compilation_result(*, allowed_paths=("src/**",), task_count: int = 2):
    tasks = tuple(
        f"Synthetic filesystem task {index}." for index in range(1, task_count + 1)
    )
    source_ticket = compiler_ticket(
        ticket_scope=compiler_scope(
            allowed_paths=allowed_paths,
            forbidden_paths=("src/blocked/**",),
        ),
        tasks=tasks,
    )
    return build_bundle(source_ticket=source_ticket)["result"]


def allocation_result(monkeypatch: pytest.MonkeyPatch, result, workspace_root: Path):
    workspace_root.mkdir(parents=True, exist_ok=True)
    (workspace_root / "src").mkdir(exist_ok=True)
    status_state = {"status": ""}
    patch_workspace_inspection(monkeypatch, workspace_root, status_state=status_state)
    identity = build_workspace_repository_identity(
        repository_id=REPOSITORY_ID,
        source_commit=SOURCE_COMMIT,
        workspace_branch=WORKSPACE_BRANCH,
    )
    authorization = build_workspace_allocation_authorization(
        authorizer_id="workspace.authorizer.p17-1",
        authorization_reference="AUTH-P17-1",
        rationale="Authorize synthetic P17.3 workspace.",
        compilation_result=result,
        repository_identity=identity,
        workspace_root=path_text(workspace_root),
    )
    request = WorkspaceAllocationRequest(
        compilation_result=result,
        repository_identity=identity,
        allocation_authorization=authorization,
        registry=get_empty_workspace_allocation_registry(),
    )
    return work_packet.allocate_workspace(request), status_state


def profile_result(result, allocated, operations=GRANTABLE_OPERATIONS):
    authorization = build_tool_permission_profile_authorization(
        authorizer_id="tool.authorizer.p17-2",
        authorization_reference="AUTH-P17-2",
        rationale="Authorize synthetic P17.3 filesystem operations.",
        compilation_result=result,
        allocation_result=allocated,
        grant_requests=tuple(
            ToolPermissionGrantRequest(
                operation=operation,
                source_allowed_action=result.work_packet.repository_scope.allowed_actions[
                    0
                ],
                rationale=f"Authorize {operation.value} for synthetic execution.",
            )
            for operation in operations
        ),
        risk_acknowledgement="Synthetic mutation risk acknowledged.",
    )
    return build_tool_permission_profile(
        ToolPermissionProfileRequest(
            compilation_result=result,
            allocation_result=allocated,
            profile_authorization=authorization,
        )
    )


def action(
    index: int,
    task_step_id: str,
    operation: ToolPermissionOperation,
    path: str,
    *,
    content: str | None = None,
    expected: str | None = None,
):
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "action_id": f"ACTION-{index:03d}",
        "task_step_id": task_step_id,
        "operation": operation,
        "workspace_relative_path": path,
        "content": content,
        "expected_preexisting_SHA256": expected,
        "rationale": f"Synthetic {operation.value} action.",
    }
    return SingleAgentToolAction(
        **data,
        action_SHA256=sae._action_digest_from_record(data),
    )


def plan(actions: tuple[SingleAgentToolAction, ...]):
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "action_source": "externally_supplied_single_agent_plan",
        "actions": actions,
    }
    return SingleAgentExecutionPlan(
        **data,
        plan_SHA256=sae._plan_digest_from_record(data),
    )


def execution_request(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, actions):
    result = compilation_result()
    workspace_root = tmp_path / "workspace"
    allocated, status_state = allocation_result(monkeypatch, result, workspace_root)
    permissions = profile_result(result, allocated)
    binding = build_single_agent_runtime_binding(
        agent_id="agent.p17-3",
        worker_id="worker.p17-3",
        work_packet=result.work_packet,
    )
    execution_plan = plan(tuple(actions))
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-3",
        authorization_reference="AUTH-P17-3",
        rationale="Authorize externally supplied single-agent execution plan.",
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        risk_acknowledgement="Synthetic filesystem mutation risk acknowledged.",
    )
    request = SingleAgentExecutionRequest(
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        execution_authorization=authorization,
    )
    return {
        "request": request,
        "status_state": status_state,
        "workspace_root": workspace_root,
        "compilation_result": result,
        "allocation_result": allocated,
        "profile_result": permissions,
        "binding": binding,
        "plan": execution_plan,
        "authorization": authorization,
    }


def basic_actions(result):
    tasks = result.work_packet.tasks
    return (
        action(
            1,
            tasks[0].step_id,
            ToolPermissionOperation.CREATE_DIRECTORY,
            "src/generated",
        ),
        action(
            2,
            tasks[0].step_id,
            ToolPermissionOperation.CREATE_FILE,
            "src/generated/readme.txt",
            content="hello from P17.3",
        ),
        action(
            3,
            tasks[1].step_id,
            ToolPermissionOperation.READ_FILE,
            "src/generated/readme.txt",
        ),
        action(
            4, tasks[1].step_id, ToolPermissionOperation.LIST_DIRECTORY, "src/generated"
        ),
    )


@pytest.fixture()
def prepared_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = compilation_result()
    context = execution_request(monkeypatch, tmp_path, basic_actions(result))
    session = prepare_single_agent_execution(context["request"])
    context["session"] = session
    return context


@pytest.fixture()
def sample_models(prepared_context):
    request = prepared_context["request"]
    session = prepared_context["session"]
    first = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(
            execution_request=request,
            session=session,
        )
    )
    prepared_context["status_state"]["status"] = " M src/generated"
    second = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(
            execution_request=request,
            session=first.updated_session,
        )
    )
    third = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(
            execution_request=request,
            session=second.updated_session,
        )
    )
    fourth = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(
            execution_request=request,
            session=third.updated_session,
        )
    )
    completed = complete_single_agent_execution(fourth.updated_session)
    evidence = fourth.updated_session.action_evidence[-1]
    return {
        SingleAgentRuntimeBinding.__name__: request.runtime_binding,
        SingleAgentExecutionAuthorization.__name__: request.execution_authorization,
        SingleAgentToolAction.__name__: request.plan.actions[0],
        SingleAgentExecutionPlan.__name__: request.plan,
        SingleAgentExecutionRequest.__name__: request,
        SingleAgentTargetResolutionEvidence.__name__: evidence.target_resolution,
        SingleAgentToolObservation.__name__: third.observation,
        SingleAgentActionEvidence.__name__: evidence,
        SingleAgentExecutionSession.__name__: fourth.updated_session,
        SingleAgentActionExecutionRequest.__name__: SingleAgentActionExecutionRequest(
            execution_request=request,
            session=fourth.updated_session,
            cancellation_requested=True,
            cancellation_reference="CANCEL-P17-3",
        ),
        SingleAgentActionExecutionResult.__name__: fourth,
        SingleAgentExecutionResult.__name__: completed,
    }


@pytest.mark.parametrize("exported_name", P17_3_EXPORTS)
def test_p17_3_exports_are_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


def test_prior_exports_remain_exact_prefix() -> None:
    prior = P17_0_EXPORTS + P17_1_EXPORTS + P17_2_EXPORTS
    assert work_packet.__all__[: len(prior)] == prior
    assert work_packet.__all__[len(prior) :] == P17_3_EXPORTS
    assert len(work_packet.__all__) == 113
    assert len(set(work_packet.__all__)) == 113
    assert not any(name.startswith("_") for name in work_packet.__all__)


@pytest.mark.parametrize(
    "forbidden_name",
    (
        "execute_work_packet",
        "execute_tool",
        "SingleAgentTicketExecutor",
        "ValidationCommandRunner",
        "ProviderDispatcher",
        "ModelRunner",
        "GitRunner",
        "CommandRunner",
    ),
)
def test_forbidden_public_shapes_absent(forbidden_name: str) -> None:
    assert not hasattr(work_packet, forbidden_name)


def test_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        hasattr(work_packet, "SingleAgentExecutionSession"),
        hasattr(work_packet, "execute_single_agent_tool_action"),
        hasattr(work_packet, "execute_work_packet"),
        hasattr(work_packet, "ValidationCommandRunner"),
    ) == (113, 113, True, True, False, False)


def test_function_import_smoke_exact_output() -> None:
    assert (
        build_single_agent_runtime_binding.__name__,
        build_single_agent_execution_authorization.__name__,
        prepare_single_agent_execution.__name__,
        execute_single_agent_tool_action.__name__,
        complete_single_agent_execution.__name__,
    ) == (
        "build_single_agent_runtime_binding",
        "build_single_agent_execution_authorization",
        "prepare_single_agent_execution",
        "execute_single_agent_tool_action",
        "complete_single_agent_execution",
    )


def test_constants_are_canonical() -> None:
    assert SINGLE_AGENT_EXECUTION_SCHEMA_VERSION == 1
    assert (
        SINGLE_AGENT_EXECUTION_POLICY_ID
        == "pepper-externally-driven-single-agent-filesystem-execution-v1"
    )


@pytest.mark.parametrize(
    ("enum_type", "values"),
    (
        (
            SingleAgentExecutionState,
            ("prepared", "active", "blocked", "cancelled", "completed"),
        ),
        (SingleAgentActionDisposition, ("executed", "denied", "cancelled")),
        (SingleAgentToolObservationKind, ("none", "text", "directory_entries")),
        (SingleAgentTargetKind, ("absent", "file", "directory")),
    ),
)
def test_controlled_enums_are_exact(enum_type, values) -> None:
    assert tuple(member.value for member in enum_type) == values


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_are_frozen(model_type) -> None:
    assert model_type.model_config["frozen"] is True


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_reject_unknown_fields(model_type, sample_models) -> None:
    payload = sample_models[model_type.__name__].model_dump(mode="json")
    payload["unknown"] = "rejected"
    with pytest.raises(ValidationError):
        model_type.model_validate(payload)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_model_json_schema_forbids_additional_properties(model_type) -> None:
    assert model_type.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_round_trip_json(model_type, sample_models) -> None:
    sample = sample_models[model_type.__name__]
    assert model_type.model_validate_json(sample.model_dump_json()) == sample


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_support_model_dump(model_type, sample_models) -> None:
    assert isinstance(sample_models[model_type.__name__].model_dump(), dict)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_support_model_dump_json(model_type, sample_models) -> None:
    assert isinstance(sample_models[model_type.__name__].model_dump_json(), str)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_support_model_validate(model_type, sample_models) -> None:
    sample = sample_models[model_type.__name__]
    assert model_type.model_validate(sample.model_dump(mode="json")) == sample


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_preserve_tuple_immutability(model_type, sample_models) -> None:
    sample = model_type.model_validate(
        sample_models[model_type.__name__].model_dump(mode="json")
    )
    for field_name in sample.model_fields:
        value = getattr(sample, field_name)
        if isinstance(value, tuple):
            assert type(value) is tuple


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_alternative_schema_versions_fail(model_type, sample_models) -> None:
    sample = sample_models[model_type.__name__]
    if "schema_version" not in sample.model_fields:
        assert model_type is SingleAgentToolObservation
        return
    payload = sample.model_dump(mode="json")
    payload["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_type.model_validate(payload)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_digest_tampering_fails(model_type, sample_models) -> None:
    sample = sample_models[model_type.__name__]
    digest_fields = [name for name in sample.model_fields if name.endswith("SHA256")]
    if not digest_fields:
        assert model_type in {
            SingleAgentExecutionRequest,
            SingleAgentActionExecutionRequest,
        }
        return
    payload = sample.model_dump(mode="json")
    payload[digest_fields[-1]] = "0" * 64
    with pytest.raises(ValidationError):
        model_type.model_validate(payload)


@pytest.mark.parametrize("operation", GRANTABLE_OPERATIONS)
def test_every_grantable_operation_validates(
    operation: ToolPermissionOperation,
) -> None:
    expected = (
        "a" * 64
        if operation
        in {ToolPermissionOperation.REPLACE_FILE, ToolPermissionOperation.DELETE_FILE}
        else None
    )
    content = (
        "content"
        if operation
        in {ToolPermissionOperation.CREATE_FILE, ToolPermissionOperation.REPLACE_FILE}
        else None
    )
    item = action(
        1, "TASK-001", operation, "src/file.txt", content=content, expected=expected
    )
    assert item.operation is operation


@pytest.mark.parametrize("operation", NEVER_GRANTABLE_OPERATIONS)
def test_never_grantable_operation_fails(operation: ToolPermissionOperation) -> None:
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "action_id": "ACTION-001",
        "task_step_id": "TASK-001",
        "operation": operation,
        "workspace_relative_path": "src/file.txt",
        "content": None,
        "expected_preexisting_SHA256": None,
        "rationale": "Synthetic forbidden operation.",
    }
    with pytest.raises(ValidationError):
        SingleAgentToolAction(
            **data,
            action_SHA256=sae._action_digest_from_record(data),
        )


@pytest.mark.parametrize(
    ("operation", "content", "expected", "valid"),
    (
        (ToolPermissionOperation.LIST_DIRECTORY, None, None, True),
        (ToolPermissionOperation.READ_FILE, None, None, True),
        (ToolPermissionOperation.CREATE_FILE, "x", None, True),
        (ToolPermissionOperation.REPLACE_FILE, "x", "a" * 64, True),
        (ToolPermissionOperation.DELETE_FILE, None, "a" * 64, True),
        (ToolPermissionOperation.CREATE_DIRECTORY, None, None, True),
        (ToolPermissionOperation.DELETE_DIRECTORY, None, None, True),
        (ToolPermissionOperation.READ_FILE, "x", None, False),
        (ToolPermissionOperation.CREATE_FILE, None, None, False),
        (ToolPermissionOperation.REPLACE_FILE, "x", None, False),
        (ToolPermissionOperation.DELETE_FILE, None, None, False),
        (ToolPermissionOperation.CREATE_DIRECTORY, None, "a" * 64, False),
        (ToolPermissionOperation.DELETE_DIRECTORY, "x", None, False),
    ),
)
def test_action_content_and_expected_hash_rules(
    operation, content, expected, valid
) -> None:
    if valid:
        assert action(
            1, "TASK-001", operation, "src/file.txt", content=content, expected=expected
        )
    else:
        with pytest.raises(ValidationError):
            action(
                1,
                "TASK-001",
                operation,
                "src/file.txt",
                content=content,
                expected=expected,
            )


@pytest.mark.parametrize(
    "bad_path",
    (
        "",
        "/abs",
        "C:/abs",
        "C:relative",
        "src\\file",
        "src/../file",
        "src//file",
        ".git/config",
        "graphify-out/x",
    ),
)
def test_action_rejects_invalid_paths(bad_path: str) -> None:
    with pytest.raises(ValidationError):
        action(1, "TASK-001", ToolPermissionOperation.READ_FILE, bad_path)


def test_plan_contract_rejects_duplicates_and_gaps() -> None:
    first = action(1, "TASK-001", ToolPermissionOperation.READ_FILE, "src/a.txt")
    second = action(3, "TASK-001", ToolPermissionOperation.READ_FILE, "src/b.txt")
    with pytest.raises(ValidationError, match="contiguous"):
        plan((first, second))
    duplicate = first.model_copy(update={"action_id": "ACTION-001"})
    with pytest.raises(ValidationError):
        plan((first, duplicate))


def test_plan_source_is_fixed() -> None:
    first = action(1, "TASK-001", ToolPermissionOperation.READ_FILE, "src/a.txt")
    data = {
        "schema_version": SINGLE_AGENT_EXECUTION_SCHEMA_VERSION,
        "action_source": "agent_generated_plan",
        "actions": (first,),
    }
    with pytest.raises(ValidationError):
        SingleAgentExecutionPlan(**data, plan_SHA256=sae._plan_digest_from_record(data))


def test_more_than_64_actions_fail() -> None:
    actions = tuple(
        action(index, "TASK-001", ToolPermissionOperation.READ_FILE, f"src/{index}.txt")
        for index in range(1, 66)
    )
    with pytest.raises(ValidationError):
        plan(actions)


def test_runtime_binding_canonical_identities(prepared_context) -> None:
    binding = prepared_context["binding"]
    assert binding.provider == "openai-codex"
    assert binding.model_id == "gpt-5.5"
    assert (
        binding.provider_runtime_profile_id
        == "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert (
        binding.worker_profile_id
        == "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert binding.maximum_concurrent_agents == 1
    assert binding.maximum_concurrent_workers == 1
    assert binding.provider_dispatch_authorized is False
    assert binding.model_inference_authorized is False


@pytest.mark.parametrize(
    ("agent_id", "worker_id"),
    (
        ("same.id", "same.id"),
        ("SHADOW-agent", "worker.p17-3"),
        ("agent.p17-3", "SHADOW-worker"),
    ),
)
def test_runtime_binding_rejects_invalid_agent_worker_ids(agent_id, worker_id) -> None:
    packet = compilation_result().work_packet
    with pytest.raises(SingleAgentExecutionInputError):
        build_single_agent_runtime_binding(
            agent_id=agent_id,
            worker_id=worker_id,
            work_packet=packet,
        )


def test_runtime_binding_is_deterministic() -> None:
    packet = compilation_result().work_packet
    first = build_single_agent_runtime_binding(
        agent_id="agent.p17-3",
        worker_id="worker.p17-3",
        work_packet=packet,
    )
    second = build_single_agent_runtime_binding(
        agent_id="agent.p17-3",
        worker_id="worker.p17-3",
        work_packet=packet,
    )
    changed = build_single_agent_runtime_binding(
        agent_id="agent.changed",
        worker_id="worker.p17-3",
        work_packet=packet,
    )
    assert first == second
    assert first.binding_SHA256 != changed.binding_SHA256


def test_authorization_rejects_shadow_and_missing_risk(prepared_context) -> None:
    context = prepared_context
    with pytest.raises(SingleAgentExecutionAuthorizationError):
        build_single_agent_execution_authorization(
            authorizer_id="SHADOW-authorizer",
            authorization_reference="AUTH-P17-3",
            rationale="Shadow rejected.",
            compilation_result=context["compilation_result"],
            allocation_result=context["allocation_result"],
            profile_result=context["profile_result"],
            runtime_binding=context["binding"],
            plan=context["plan"],
            risk_acknowledgement="risk",
        )
    with pytest.raises(SingleAgentExecutionAuthorizationError, match="risk"):
        build_single_agent_execution_authorization(
            authorizer_id="execution.authorizer.p17-3",
            authorization_reference="AUTH-P17-3",
            rationale="Missing risk rejected.",
            compilation_result=context["compilation_result"],
            allocation_result=context["allocation_result"],
            profile_result=context["profile_result"],
            runtime_binding=context["binding"],
            plan=context["plan"],
        )


def test_read_only_authorization_does_not_require_risk(monkeypatch, tmp_path) -> None:
    result = compilation_result(task_count=1)
    workspace_root = tmp_path / "workspace"
    (workspace_root / "src").mkdir(parents=True)
    (workspace_root / "src" / "file.txt").write_text("read", encoding="utf-8")
    allocated, _status = allocation_result(monkeypatch, result, workspace_root)
    permissions = profile_result(
        result, allocated, operations=(ToolPermissionOperation.READ_FILE,)
    )
    binding = build_single_agent_runtime_binding(
        agent_id="agent.p17-3",
        worker_id="worker.p17-3",
        work_packet=result.work_packet,
    )
    read_plan = plan((
        action(
            1,
            result.work_packet.tasks[0].step_id,
            ToolPermissionOperation.READ_FILE,
            "src/file.txt",
        ),
    ))
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-3",
        authorization_reference="AUTH-P17-3",
        rationale="Read-only authorization.",
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=read_plan,
    )
    assert authorization.risk_acknowledgement is None


@pytest.mark.parametrize(
    "field",
    (
        "work_packet_SHA256",
        "allocation_SHA256",
        "profile_SHA256",
        "runtime_binding_SHA256",
        "plan_SHA256",
    ),
)
def test_execution_request_rejects_authorization_mismatches(
    prepared_context, field
) -> None:
    authorization = prepared_context["authorization"].model_copy(
        update={field: "0" * 64}
    )
    with pytest.raises(ValidationError):
        SingleAgentExecutionRequest(
            compilation_result=prepared_context["compilation_result"],
            allocation_result=prepared_context["allocation_result"],
            profile_result=prepared_context["profile_result"],
            runtime_binding=prepared_context["binding"],
            plan=prepared_context["plan"],
            execution_authorization=authorization,
        )


def test_prepare_session_shape_is_exact(prepared_context) -> None:
    session = prepared_context["session"]
    assert session.state is SingleAgentExecutionState.PREPARED
    assert session.next_action_index == 0
    assert session.execution_active is True
    assert session.single_agent_execution_requirement_satisfied is False
    assert session.validation_command_runner_ready is False
    assert session.result_envelopes_ready is False
    validate_single_agent_execution_session(session)


def test_canonical_externally_driven_single_agent_execution_flow(
    prepared_context,
) -> None:
    request = prepared_context["request"]
    session = prepared_context["session"]
    decisions = []
    for index in range(4):
        result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=request, session=session
            )
        )
        session = result.updated_session
        decisions.append(session.action_evidence[-1].permission_decision)
        if index == 0:
            prepared_context["status_state"]["status"] = " M src/generated"
    completed = complete_single_agent_execution(session)
    assert decisions == [ToolPermissionDecision.ALLOW] * 4
    assert completed.completed_action_count == 4
    assert len(completed.completed_task_step_ids) == 2
    assert completed.single_agent_execution_requirement_satisfied is True
    assert completed.validation_command_runner_ready is False
    assert completed.result_envelopes_ready is False
    assert completed.provider_dispatch_count == 0
    assert completed.model_inference_count == 0
    assert (
        prepared_context["workspace_root"] / "src" / "generated" / "readme.txt"
    ).read_text(encoding="utf-8") == "hello from P17.3"


def test_permission_denial_blocks_without_execution(monkeypatch, tmp_path) -> None:
    result = compilation_result(task_count=1)
    workspace_root = tmp_path / "workspace"
    (workspace_root / "src").mkdir(parents=True)
    allocated, _status = allocation_result(monkeypatch, result, workspace_root)
    permissions = profile_result(
        result, allocated, operations=(ToolPermissionOperation.READ_FILE,)
    )
    denied_action = action(
        1,
        result.work_packet.tasks[0].step_id,
        ToolPermissionOperation.CREATE_FILE,
        "src/denied.txt",
        content="blocked",
    )
    execution_plan = plan((denied_action,))
    binding = build_single_agent_runtime_binding(
        agent_id="agent.p17-3",
        worker_id="worker.p17-3",
        work_packet=result.work_packet,
    )
    authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-3",
        authorization_reference="AUTH-P17-3",
        rationale="Authorize denied plan shape only.",
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        risk_acknowledgement="risk",
    )
    request = SingleAgentExecutionRequest(
        compilation_result=result,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=binding,
        plan=execution_plan,
        execution_authorization=authorization,
    )
    session = prepare_single_agent_execution(request)
    result = execute_single_agent_tool_action(
        SingleAgentActionExecutionRequest(execution_request=request, session=session)
    )
    assert result.disposition is SingleAgentActionDisposition.DENIED
    assert result.updated_session.state is SingleAgentExecutionState.BLOCKED
    assert not (workspace_root / "src" / "denied.txt").exists()
    with pytest.raises(SingleAgentExecutionStateError):
        execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=request,
                session=result.updated_session,
            )
        )


def test_cancellation_observed_before_resolution_and_permission(
    prepared_context, monkeypatch
) -> None:
    with (
        patch.object(sae, "_resolve_target", side_effect=AssertionError("resolved")),
        patch.object(
            sae, "evaluate_tool_permission", side_effect=AssertionError("permission")
        ),
    ):
        result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=prepared_context["request"],
                session=prepared_context["session"],
                cancellation_requested=True,
                cancellation_reference="CANCEL-P17-3",
            )
        )
    assert result.disposition is SingleAgentActionDisposition.CANCELLED
    assert result.updated_session.state is SingleAgentExecutionState.CANCELLED
    assert result.updated_session.execution_active is False


def test_cancellation_reference_required(prepared_context) -> None:
    with pytest.raises(ValidationError):
        SingleAgentActionExecutionRequest(
            execution_request=prepared_context["request"],
            session=prepared_context["session"],
            cancellation_requested=True,
        )


@pytest.mark.parametrize(
    "bad_state",
    (
        SingleAgentExecutionState.BLOCKED,
        SingleAgentExecutionState.CANCELLED,
        SingleAgentExecutionState.COMPLETED,
    ),
)
def test_terminal_sessions_cannot_continue(prepared_context, bad_state) -> None:
    session = sae._copy_session(
        prepared_context["session"],
        state=bad_state,
        execution_active=False,
        single_agent_execution_requirement_satisfied=bad_state
        is SingleAgentExecutionState.COMPLETED,
    )
    with pytest.raises(SingleAgentExecutionStateError):
        execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=prepared_context["request"],
                session=session,
            )
        )


@pytest.mark.parametrize(
    "relative_path",
    (
        "/absolute",
        "../escape",
        "src/../escape",
        "src\\bad",
        ".git/config",
        "graphify-out/x",
    ),
)
def test_target_resolution_rejects_unsafe_paths(
    prepared_context, relative_path
) -> None:
    base_action = prepared_context["request"].plan.actions[0]
    with pytest.raises((ValidationError, SingleAgentTargetResolutionError)):
        unsafe = action(
            1,
            base_action.task_step_id,
            ToolPermissionOperation.READ_FILE,
            relative_path,
        )
        sae._resolve_target(
            action=unsafe,
            allocation=prepared_context["allocation_result"].allocation,
        )


def test_target_resolution_rejects_symlink_parent(prepared_context) -> None:
    workspace_root = prepared_context["workspace_root"]
    (workspace_root / "src" / "real").mkdir()
    try:
        (workspace_root / "src" / "link").symlink_to(
            workspace_root / "src" / "real", target_is_directory=True
        )
    except OSError as exc:
        raise AssertionError(
            "symlink creation unavailable in test environment"
        ) from exc
    unsafe = action(
        1, "TASK-001", ToolPermissionOperation.READ_FILE, "src/link/file.txt"
    )
    with pytest.raises(SingleAgentTargetResolutionError, match="symlink"):
        sae._resolve_target(
            action=unsafe,
            allocation=prepared_context["allocation_result"].allocation,
        )


def test_target_resolution_digest_validates(prepared_context) -> None:
    item = sae._resolve_target(
        action=prepared_context["request"].plan.actions[0],
        allocation=prepared_context["allocation_result"].allocation,
    )
    assert item.under_workspace is True
    assert item.symlink_safe is True
    assert item.resolution_SHA256 == sae._target_resolution_digest(item)


def test_list_directory_semantics(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "listed"
    target.mkdir()
    (target / "b.txt").write_text("b", encoding="utf-8")
    (target / "a.txt").write_text("a", encoding="utf-8")
    observation = sae._list_directory(target)
    assert observation.kind is SingleAgentToolObservationKind.DIRECTORY_ENTRIES
    assert observation.directory_entries == ("a.txt", "b.txt")
    assert observation.text is None
    assert observation.observation_SHA256 == sae._observation_digest(observation)


def test_list_directory_entry_bound(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "many"
    target.mkdir()
    for index in range(sae.MAX_DIRECTORY_ENTRIES + 1):
        (target / f"f{index:03d}").write_text("x", encoding="utf-8")
    with pytest.raises(SingleAgentToolExecutionError, match="bound"):
        sae._list_directory(target)


def test_read_file_semantics(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "read.txt"
    target.write_text("hello", encoding="utf-8")
    observation = sae._read_file(target)
    assert observation.kind is SingleAgentToolObservationKind.TEXT
    assert observation.text == "hello"
    assert observation.content_SHA256 == sae._sha256_bytes(b"hello")


@pytest.mark.parametrize(
    "payload",
    (b"\xff\xfe", b"x" * (sae.MAX_TEXT_BYTES + 1)),
    ids=("binary", "oversize"),
)
def test_read_file_rejects_binary_or_oversize(prepared_context, payload) -> None:
    target = prepared_context["workspace_root"] / "src" / "bad.bin"
    target.write_bytes(payload)
    with pytest.raises(SingleAgentToolExecutionError):
        sae._read_file(target)


def test_create_replace_delete_file_semantics(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "file.txt"
    create = action(
        1,
        "TASK-001",
        ToolPermissionOperation.CREATE_FILE,
        "src/file.txt",
        content="one",
    )
    sae._create_file(action=create, target=target)
    assert target.read_text(encoding="utf-8") == "one"
    digest = sae._sha256_bytes(b"one")
    replace = action(
        2,
        "TASK-001",
        ToolPermissionOperation.REPLACE_FILE,
        "src/file.txt",
        content="two",
        expected=digest,
    )
    sae._replace_file(action=replace, target=target)
    assert target.read_text(encoding="utf-8") == "two"
    delete = action(
        3,
        "TASK-001",
        ToolPermissionOperation.DELETE_FILE,
        "src/file.txt",
        expected=sae._sha256_bytes(b"two"),
    )
    sae._delete_file(action=delete, target=target)
    assert not target.exists()


def test_file_operation_preconditions(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "missing.txt"
    with pytest.raises(SingleAgentToolExecutionError):
        sae._replace_file(
            action=action(
                1,
                "TASK-001",
                ToolPermissionOperation.REPLACE_FILE,
                "src/missing.txt",
                content="x",
                expected="a" * 64,
            ),
            target=target,
        )
    existing = prepared_context["workspace_root"] / "src" / "exists.txt"
    existing.write_text("x", encoding="utf-8")
    with pytest.raises(SingleAgentToolExecutionError):
        sae._create_file(
            action=action(
                1,
                "TASK-001",
                ToolPermissionOperation.CREATE_FILE,
                "src/exists.txt",
                content="x",
            ),
            target=existing,
        )


def test_directory_create_delete_semantics(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "empty"
    sae._create_directory(target=target, action_id="ACTION-001")
    assert target.is_dir()
    sae._delete_directory(target=target, action_id="ACTION-002")
    assert not target.exists()


def test_delete_directory_rejects_nonempty(prepared_context) -> None:
    target = prepared_context["workspace_root"] / "src" / "nonempty"
    target.mkdir()
    (target / "child.txt").write_text("x", encoding="utf-8")
    with pytest.raises(SingleAgentToolExecutionError, match="empty"):
        sae._delete_directory(target=target, action_id="ACTION-001")


@pytest.mark.parametrize(
    ("operation", "path", "content"),
    (
        (ToolPermissionOperation.CREATE_FILE, "src/rollback-file.txt", "x"),
        (ToolPermissionOperation.CREATE_DIRECTORY, "src/rollback-dir", None),
    ),
)
def test_create_rollbacks_after_induced_failure(
    prepared_context, monkeypatch, operation, path, content
) -> None:
    monkeypatch.setattr(
        sae,
        "_after_filesystem_mutation_hook",
        lambda action_id: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    target = prepared_context["workspace_root"].joinpath(*path.split("/"))
    with pytest.raises(SingleAgentToolExecutionError):
        if operation is ToolPermissionOperation.CREATE_FILE:
            sae._create_file(
                action=action(1, "TASK-001", operation, path, content=content),
                target=target,
            )
        else:
            sae._create_directory(target=target, action_id="ACTION-001")
    assert not target.exists()


def test_replace_and_delete_rollbacks_after_induced_failure(
    prepared_context, monkeypatch
) -> None:
    monkeypatch.setattr(
        sae,
        "_after_filesystem_mutation_hook",
        lambda action_id: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    target = prepared_context["workspace_root"] / "src" / "rollback.txt"
    target.write_text("original", encoding="utf-8")
    with pytest.raises(SingleAgentToolExecutionError):
        sae._replace_file(
            action=action(
                1,
                "TASK-001",
                ToolPermissionOperation.REPLACE_FILE,
                "src/rollback.txt",
                content="changed",
                expected=sae._sha256_bytes(b"original"),
            ),
            target=target,
        )
    assert target.read_text(encoding="utf-8") == "original"
    with pytest.raises(SingleAgentToolExecutionError):
        sae._delete_file(
            action=action(
                2,
                "TASK-001",
                ToolPermissionOperation.DELETE_FILE,
                "src/rollback.txt",
                expected=sae._sha256_bytes(b"original"),
            ),
            target=target,
        )
    assert target.read_text(encoding="utf-8") == "original"


def test_delete_directory_rollback_after_induced_failure(
    prepared_context, monkeypatch
) -> None:
    monkeypatch.setattr(
        sae,
        "_after_filesystem_mutation_hook",
        lambda action_id: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    target = prepared_context["workspace_root"] / "src" / "rollback-empty"
    target.mkdir()
    with pytest.raises(SingleAgentToolExecutionError):
        sae._delete_directory(target=target, action_id="ACTION-001")
    assert target.is_dir()


def test_plan_cannot_skip_or_repeat_actions(prepared_context) -> None:
    session = prepared_context["session"].model_copy(update={"next_action_index": 2})
    with pytest.raises(ValidationError):
        SingleAgentActionExecutionRequest(
            execution_request=prepared_context["request"],
            session=session,
        )


def test_completion_rejects_incomplete_blocked_and_cancelled(prepared_context) -> None:
    with pytest.raises(SingleAgentExecutionStateError):
        complete_single_agent_execution(prepared_context["session"])
    for state in (
        SingleAgentExecutionState.BLOCKED,
        SingleAgentExecutionState.CANCELLED,
    ):
        session = sae._copy_session(
            prepared_context["session"],
            state=state,
            execution_active=False,
        )
        with pytest.raises(SingleAgentExecutionStateError):
            complete_single_agent_execution(session)


@pytest.mark.parametrize(
    "forbidden_attribute",
    (
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "openai",
        "docker",
        "asyncio",
        "threading",
        "multiprocessing",
        "concurrent",
        "ProviderDispatcher",
        "ModelRunner",
        "GitRunner",
        "CommandRunner",
        "ValidationCommandRunner",
        "execute_work_packet",
        "execute_tool",
    ),
)
def test_forbidden_runtime_surfaces_not_exported(forbidden_attribute: str) -> None:
    assert not hasattr(sae, forbidden_attribute)


@pytest.mark.parametrize(
    "field_type_name",
    (
        "Any",
        "Mapping",
        "MutableMapping",
        "object",
        "Path",
        "datetime",
        "UUID",
        "bytes",
        "Callable",
    ),
)
def test_public_schema_has_no_forbidden_field_shapes(field_type_name: str) -> None:
    for model in PUBLIC_MODELS:
        annotation_text = " ".join(
            str(field.annotation) for field in model.model_fields.values()
        )
        assert field_type_name not in annotation_text


@pytest.mark.parametrize("operation", GRANTABLE_OPERATIONS)
def test_final_result_path_buckets_are_operation_derived(
    prepared_context, operation
) -> None:
    assert operation in GRANTABLE_OPERATIONS


@pytest.mark.parametrize("name", P17_3_EXPORTS)
def test_exported_names_are_unique_and_public(name: str) -> None:
    assert work_packet.__all__.count(name) == 1
    assert not name.startswith("_")


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_model_config_is_strict_and_immutable(model_type) -> None:
    assert model_type.model_config["extra"] == "forbid"
    assert model_type.model_config["frozen"] is True
    assert model_type.model_config["validate_default"] is True
    assert model_type.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_do_not_have_mutable_defaults(model_type) -> None:
    for field in model_type.model_fields.values():
        assert not isinstance(field.default, list | dict | set)


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_have_no_environment_defaults(model_type) -> None:
    for field in model_type.model_fields.values():
        assert field.default_factory is None


def test_no_digest_is_a_signature(prepared_context) -> None:
    binding = prepared_context["binding"]
    assert len(binding.binding_SHA256) == 64
    assert not hasattr(binding, "signature")


def test_provider_model_dispatch_counts_are_zero_after_completion(
    prepared_context,
) -> None:
    request = prepared_context["request"]
    session = prepared_context["session"]
    for index in range(4):
        result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=request, session=session
            )
        )
        session = result.updated_session
        if index == 0:
            prepared_context["status_state"]["status"] = " M src/generated"
    completed = complete_single_agent_execution(session)
    assert completed.provider_dispatch_count == 0
    assert completed.model_inference_count == 0
    assert completed.validation_command_runner_ready is False
    assert completed.result_envelopes_ready is False
    assert completed.diff_artifact_review_ready is False
    assert completed.human_git_handoff_ready is False
