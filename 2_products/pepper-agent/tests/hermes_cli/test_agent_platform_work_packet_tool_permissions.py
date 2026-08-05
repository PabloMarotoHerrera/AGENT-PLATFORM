import importlib
from unittest.mock import patch

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.tool_permissions as tool_permissions
import hermes_cli.agent_platform.work_packet.workspace_allocator as allocator_module
from hermes_cli.agent_platform.work_packet import (
    TOOL_PERMISSION_POLICY_ID,
    TOOL_PERMISSION_SCHEMA_VERSION,
    ToolPermissionCheckRequest,
    ToolPermissionDecision,
    ToolPermissionDecisionEvidence,
    ToolPermissionDecisionReason,
    ToolPermissionEvaluationError,
    ToolPermissionGrant,
    ToolPermissionGrantRequest,
    ToolPermissionOperation,
    ToolPermissionProfile,
    ToolPermissionProfileAuthorization,
    ToolPermissionProfileAuthorizationError,
    ToolPermissionProfileDisposition,
    ToolPermissionProfileError,
    ToolPermissionProfileInputError,
    ToolPermissionProfileIntegrityError,
    ToolPermissionProfileRequest,
    ToolPermissionProfileResult,
    ToolPermissionProfileState,
    WorkPacketDownstreamCapability,
    WorkPacketGitAuthority,
    WorkspaceAllocationRequest,
    WorkspaceAllocationResult,
    build_tool_permission_profile,
    build_tool_permission_profile_authorization,
    build_workspace_allocation_authorization,
    build_workspace_repository_identity,
    evaluate_tool_permission,
    get_empty_workspace_allocation_registry,
    validate_tool_permission_decision,
    validate_tool_permission_profile,
)
from tests.hermes_cli.test_agent_platform_work_packet_compiler import (
    EXPECTED_EXPORTS as P17_0_EXPORTS,
    build_bundle,
    scope as compiler_scope,
    ticket as compiler_ticket,
)
from tests.hermes_cli.test_agent_platform_work_packet_workspace_allocator import (
    P17_1_EXPORTS,
)


P17_2_EXPORTS = (
    "TOOL_PERMISSION_SCHEMA_VERSION",
    "TOOL_PERMISSION_POLICY_ID",
    "ToolPermissionOperation",
    "ToolPermissionProfileState",
    "ToolPermissionProfileDisposition",
    "ToolPermissionDecision",
    "ToolPermissionDecisionReason",
    "ToolPermissionGrantRequest",
    "ToolPermissionProfileAuthorization",
    "ToolPermissionGrant",
    "ToolPermissionProfileRequest",
    "ToolPermissionProfile",
    "ToolPermissionProfileResult",
    "ToolPermissionCheckRequest",
    "ToolPermissionDecisionEvidence",
    "ToolPermissionProfileError",
    "ToolPermissionProfileInputError",
    "ToolPermissionProfileAuthorizationError",
    "ToolPermissionProfileIntegrityError",
    "ToolPermissionEvaluationError",
    "build_tool_permission_profile_authorization",
    "build_tool_permission_profile",
    "validate_tool_permission_profile",
    "evaluate_tool_permission",
    "validate_tool_permission_decision",
)
PUBLIC_MODELS = (
    ToolPermissionGrantRequest,
    ToolPermissionProfileAuthorization,
    ToolPermissionGrant,
    ToolPermissionProfileRequest,
    ToolPermissionProfile,
    ToolPermissionProfileResult,
    ToolPermissionCheckRequest,
    ToolPermissionDecisionEvidence,
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
NEVER_GRANTABLE_OPERATIONS = (
    ToolPermissionOperation.EXECUTE_COMMAND,
    ToolPermissionOperation.VALIDATION_COMMAND,
    ToolPermissionOperation.GIT_READ_ONLY,
    ToolPermissionOperation.GIT_MUTATION,
    ToolPermissionOperation.NETWORK_ACCESS,
    ToolPermissionOperation.WORKSPACE_MUTATION,
    ToolPermissionOperation.PROVIDER_CALL,
    ToolPermissionOperation.MODEL_CALL,
    ToolPermissionOperation.AGENT_CONTROL,
    ToolPermissionOperation.WORKER_CONTROL,
)
MUTATING_OPERATIONS = (
    ToolPermissionOperation.CREATE_FILE,
    ToolPermissionOperation.REPLACE_FILE,
    ToolPermissionOperation.DELETE_FILE,
    ToolPermissionOperation.CREATE_DIRECTORY,
    ToolPermissionOperation.DELETE_DIRECTORY,
)
PROTECTED_PATHS = (
    ".git/**",
    ".opencode/**",
    ".agents/**",
    "AGENTS.md",
    "graphify-out/**",
    "4_external/sources/**",
    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
)
SOURCE_COMMIT = "a" * 40
WORKSPACE_BRANCH = "p17/workspace-allocator"
WORKSPACE_ROOT = "C:/worktrees/pepper-p17-1"
ALLOWED_RELATIVE_PATH = (
    "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/tool_permissions.py"
)
FORBIDDEN_RELATIVE_PATH = (
    "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/blocked/vendor.py"
)
OUT_OF_SCOPE_RELATIVE_PATH = "README.md"


def fake_workspace_metadata(
    workspace_root: str,
) -> allocator_module._WorkspacePathMetadata:
    assert workspace_root == WORKSPACE_ROOT
    return allocator_module._WorkspacePathMetadata(
        exists=True,
        is_dir=True,
        is_symlink=False,
        resolved_workspace_root=WORKSPACE_ROOT,
    )


def fake_git_command(workspace_root: str, args: tuple[str, ...]) -> str:
    assert workspace_root == WORKSPACE_ROOT
    responses = {
        ("rev-parse", "--is-inside-work-tree"): "true",
        ("rev-parse", "--show-toplevel"): WORKSPACE_ROOT,
        ("rev-parse", "HEAD"): SOURCE_COMMIT,
        ("branch", "--show-current"): WORKSPACE_BRANCH,
        ("rev-parse", "--git-dir"): "C:/repo/.git/worktrees/pepper-p17-1",
        ("rev-parse", "--git-common-dir"): "C:/repo/.git",
        ("status", "--porcelain=v1", "-uall"): "",
    }
    return responses[args]


def build_compilation_result(
    *,
    allowed_paths: tuple[str, ...] = (
        "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/**",
    ),
    forbidden_paths: tuple[str, ...] = (
        "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/blocked/**",
    ),
):
    source_ticket = compiler_ticket(
        ticket_scope=compiler_scope(
            allowed_paths=allowed_paths,
            forbidden_paths=forbidden_paths,
        )
    )
    return build_bundle(source_ticket=source_ticket)["result"]


def build_allocation_result(compilation_result) -> WorkspaceAllocationResult:
    identity = build_workspace_repository_identity(
        repository_id="pepper-agent",
        source_commit=SOURCE_COMMIT,
        workspace_branch=WORKSPACE_BRANCH,
    )
    authorization = build_workspace_allocation_authorization(
        authorizer_id="workspace.authorizer.p17-1",
        authorization_reference="AUTH-P17-1",
        rationale="Authorize synthetic human-provisioned workspace reservation.",
        compilation_result=compilation_result,
        repository_identity=identity,
        workspace_root=WORKSPACE_ROOT,
    )
    request = WorkspaceAllocationRequest(
        compilation_result=compilation_result,
        repository_identity=identity,
        allocation_authorization=authorization,
        registry=get_empty_workspace_allocation_registry(),
    )
    with (
        patch.object(
            allocator_module, "_workspace_path_metadata", fake_workspace_metadata
        ),
        patch.object(
            allocator_module,
            "_run_git_command",
            fake_git_command,
        ),
    ):
        return work_packet.allocate_workspace(request)


def grant_request(
    compilation_result,
    operation: ToolPermissionOperation = ToolPermissionOperation.READ_FILE,
    *,
    source_allowed_action: str | None = None,
) -> ToolPermissionGrantRequest:
    return ToolPermissionGrantRequest(
        operation=operation,
        source_allowed_action=source_allowed_action
        or compilation_result.work_packet.repository_scope.allowed_actions[0],
        rationale=f"Authorize {operation.value} for synthetic scoped work.",
    )


def build_authorization(
    compilation_result,
    allocation_result,
    operations: tuple[ToolPermissionOperation, ...] = (
        ToolPermissionOperation.READ_FILE,
    ),
    *,
    risk_acknowledgement: str | None = None,
) -> ToolPermissionProfileAuthorization:
    if risk_acknowledgement is None and any(
        operation in MUTATING_OPERATIONS for operation in operations
    ):
        risk_acknowledgement = "Synthetic mutation risk acknowledged."
    return build_tool_permission_profile_authorization(
        authorizer_id="tool.authorizer.p17-2",
        authorization_reference="AUTH-P17-2",
        rationale="Authorize deterministic tool permission profile.",
        compilation_result=compilation_result,
        allocation_result=allocation_result,
        grant_requests=tuple(
            grant_request(compilation_result, operation) for operation in operations
        ),
        risk_acknowledgement=risk_acknowledgement,
    )


def build_profile_context(
    operations: tuple[ToolPermissionOperation, ...] = (
        ToolPermissionOperation.READ_FILE,
    ),
    *,
    allowed_paths: tuple[str, ...] = (
        "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/**",
    ),
    forbidden_paths: tuple[str, ...] = (
        "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/blocked/**",
    ),
):
    compilation_result = build_compilation_result(
        allowed_paths=allowed_paths,
        forbidden_paths=forbidden_paths,
    )
    allocation_result = build_allocation_result(compilation_result)
    authorization = build_authorization(
        compilation_result,
        allocation_result,
        operations,
    )
    request = ToolPermissionProfileRequest(
        compilation_result=compilation_result,
        allocation_result=allocation_result,
        profile_authorization=authorization,
    )
    profile_result = build_tool_permission_profile(request)
    return {
        "compilation_result": compilation_result,
        "allocation_result": allocation_result,
        "authorization": authorization,
        "request": request,
        "profile_result": profile_result,
        "profile": profile_result.profile,
    }


def check_request(
    profile: ToolPermissionProfile,
    allocation,
    *,
    operation: ToolPermissionOperation = ToolPermissionOperation.READ_FILE,
    relative_path: str = ALLOWED_RELATIVE_PATH,
    resolved_target_path: str | None = None,
) -> ToolPermissionCheckRequest:
    return ToolPermissionCheckRequest(
        profile=profile,
        allocation=allocation,
        operation=operation,
        workspace_relative_path=relative_path,
        resolved_target_path=resolved_target_path
        or f"{WORKSPACE_ROOT}/{relative_path}",
        target_resolution_verified=True,
        request_reference="CHECK-P17-2",
    )


@pytest.fixture(scope="module")
def context_all_operations():
    return build_profile_context(GRANTABLE_OPERATIONS)


@pytest.fixture(scope="module")
def context_read_only():
    return build_profile_context((ToolPermissionOperation.READ_FILE,))


@pytest.fixture(scope="module")
def sample_models(context_read_only):
    profile = context_read_only["profile"]
    allocation = context_read_only["allocation_result"].allocation
    decision = evaluate_tool_permission(check_request(profile, allocation))
    return {
        ToolPermissionGrantRequest.__name__: context_read_only[
            "authorization"
        ].grant_requests[0],
        ToolPermissionProfileAuthorization.__name__: context_read_only["authorization"],
        ToolPermissionGrant.__name__: profile.grants[0],
        ToolPermissionProfileRequest.__name__: context_read_only["request"],
        ToolPermissionProfile.__name__: profile,
        ToolPermissionProfileResult.__name__: context_read_only["profile_result"],
        ToolPermissionCheckRequest.__name__: check_request(profile, allocation),
        ToolPermissionDecisionEvidence.__name__: decision,
    }


@pytest.mark.parametrize("exported_name", P17_2_EXPORTS)
def test_p17_2_exports_are_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


@pytest.mark.parametrize("exported_name", P17_0_EXPORTS + P17_1_EXPORTS)
def test_prior_exports_remain_prefix_available(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


def test_public_export_prefix_and_counts() -> None:
    prior_exports = P17_0_EXPORTS + P17_1_EXPORTS
    assert work_packet.__all__[: len(prior_exports)] == prior_exports
    assert (
        work_packet.__all__[len(prior_exports) : len(prior_exports) + 25]
        == P17_2_EXPORTS
    )
    assert len(work_packet.__all__) == 81
    assert len(set(work_packet.__all__)) == 81
    assert not any(name.startswith("_") for name in work_packet.__all__)
    assert not hasattr(work_packet, "execute_tool")
    assert not hasattr(work_packet, "SingleAgentTicketExecutor")
    assert not hasattr(work_packet, "ValidationCommandRunner")


def test_import_smoke_exact_output() -> None:
    required = (
        "WorkPacket",
        "WorkspaceAllocation",
        "ToolPermissionProfile",
        "ToolPermissionDecisionEvidence",
        "build_tool_permission_profile",
        "evaluate_tool_permission",
    )
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        all(hasattr(work_packet, name) for name in required),
        hasattr(work_packet, "execute_tool"),
        hasattr(work_packet, "SingleAgentTicketExecutor"),
        hasattr(work_packet, "ValidationCommandRunner"),
    ) == (81, 81, True, False, False, False)


def test_function_import_smoke_exact_output() -> None:
    assert (
        build_tool_permission_profile_authorization.__name__,
        build_tool_permission_profile.__name__,
        validate_tool_permission_profile.__name__,
        evaluate_tool_permission.__name__,
        validate_tool_permission_decision.__name__,
    ) == (
        "build_tool_permission_profile_authorization",
        "build_tool_permission_profile",
        "validate_tool_permission_profile",
        "evaluate_tool_permission",
        "validate_tool_permission_decision",
    )


def test_import_reload_has_no_runtime_side_effects() -> None:
    imported = importlib.import_module(
        "hermes_cli.agent_platform.work_packet.tool_permissions"
    )
    assert imported.TOOL_PERMISSION_POLICY_ID == TOOL_PERMISSION_POLICY_ID
    assert not hasattr(imported, "Path")
    assert not hasattr(imported, "subprocess")
    assert not hasattr(imported, "requests")
    assert not hasattr(imported, "openai")
    assert not hasattr(imported, "execute_tool")


def test_constants_are_canonical() -> None:
    assert TOOL_PERMISSION_SCHEMA_VERSION == 1
    assert TOOL_PERMISSION_POLICY_ID == "pepper-deny-first-tool-permission-policy-v1"


@pytest.mark.parametrize(
    ("member", "value"),
    tuple((member.name, member.value) for member in ToolPermissionOperation),
)
def test_operation_enum_members_are_exact(member: str, value: str) -> None:
    assert ToolPermissionOperation[member].value == value


@pytest.mark.parametrize(
    ("enum_class", "values"),
    (
        (ToolPermissionProfileState, ("issued",)),
        (ToolPermissionProfileDisposition, ("issued",)),
        (ToolPermissionDecision, ("allow", "deny")),
        (
            ToolPermissionDecisionReason,
            (
                "allowed_by_explicit_grant",
                "operation_not_granted",
                "operation_explicitly_denied",
                "target_path_invalid",
                "target_outside_workspace",
                "target_in_protected_root",
                "target_in_forbidden_scope",
                "target_not_in_allowed_scope",
            ),
        ),
    ),
)
def test_controlled_enum_values_are_exact(enum_class, values: tuple[str, ...]) -> None:
    assert tuple(member.value for member in enum_class) == values
    assert len(enum_class) == len({member.value for member in enum_class})


@pytest.mark.parametrize("bad_value", ("run", "git", "network", "", "READ_FILE"))
def test_unsupported_operation_values_fail(bad_value: str) -> None:
    with pytest.raises(ValueError):
        ToolPermissionOperation(bad_value)


def test_operation_class_counts_are_exact() -> None:
    assert GRANTABLE_OPERATIONS == tuple(tool_permissions._GRANTABLE_OPERATIONS)
    assert NEVER_GRANTABLE_OPERATIONS == tuple(
        tool_permissions._NEVER_GRANTABLE_OPERATIONS
    )
    assert len(GRANTABLE_OPERATIONS) == 7
    assert len(NEVER_GRANTABLE_OPERATIONS) == 10


@pytest.mark.parametrize("model_class", PUBLIC_MODELS)
def test_public_models_are_frozen(model_class: type[BaseModel]) -> None:
    assert model_class.model_config["frozen"] is True
    assert model_class.model_config["extra"] == "forbid"
    assert model_class.model_config["validate_default"] is True
    assert model_class.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model_class", PUBLIC_MODELS)
def test_public_models_reject_extra_fields(
    model_class: type[BaseModel], sample_models
) -> None:
    sample = sample_models[model_class.__name__]
    data = sample.model_dump(mode="json")
    data["unexpected"] = "blocked"
    with pytest.raises(ValidationError):
        model_class.model_validate(data)


@pytest.mark.parametrize("model_class", PUBLIC_MODELS)
def test_public_models_json_round_trip(
    model_class: type[BaseModel], sample_models
) -> None:
    sample = sample_models[model_class.__name__]
    round_trip = model_class.model_validate_json(sample.model_dump_json())
    assert round_trip == sample


@pytest.mark.parametrize("model_class", PUBLIC_MODELS)
def test_public_model_schema_is_closed_and_deterministic(
    model_class: type[BaseModel],
) -> None:
    first = model_class.model_json_schema()
    second = model_class.model_json_schema()
    assert first == second
    assert first["additionalProperties"] is False
    assert "properties" in first


@pytest.mark.parametrize(
    "model_class",
    (
        ToolPermissionProfileAuthorization,
        ToolPermissionProfileRequest,
        ToolPermissionProfile,
        ToolPermissionProfileResult,
        ToolPermissionCheckRequest,
        ToolPermissionDecisionEvidence,
    ),
)
def test_alternative_schema_versions_fail(
    model_class: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_class.__name__].model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_class.model_validate(data)


@pytest.mark.parametrize(
    "model_class",
    (ToolPermissionProfileRequest, ToolPermissionProfile, ToolPermissionCheckRequest),
)
def test_alternative_policy_ids_fail(
    model_class: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_class.__name__].model_dump(mode="json")
    data["policy_id"] = "other-policy"
    with pytest.raises(ValidationError):
        model_class.model_validate(data)


def test_lists_normalize_to_immutable_tuples(sample_models) -> None:
    authorization = sample_models[ToolPermissionProfileAuthorization.__name__]
    data = authorization.model_dump(mode="json")
    data["grant_requests"] = list(data["grant_requests"])
    round_trip = ToolPermissionProfileAuthorization.model_validate(data)
    assert isinstance(round_trip.grant_requests, tuple)
    profile = sample_models[ToolPermissionProfile.__name__]
    profile_data = profile.model_dump(mode="json")
    profile_data["grants"] = list(profile_data["grants"])
    profile_data["denied_operations"] = list(profile_data["denied_operations"])
    profile_data["protected_paths"] = list(profile_data["protected_paths"])
    validated = ToolPermissionProfile.model_validate(profile_data)
    assert isinstance(validated.grants, tuple)
    assert isinstance(validated.denied_operations, tuple)
    assert isinstance(validated.protected_paths, tuple)


def test_strict_booleans_reject_strings(sample_models) -> None:
    data = sample_models[ToolPermissionProfileAuthorization.__name__].model_dump(
        mode="json"
    )
    data["profile_authorized"] = "true"
    with pytest.raises(ValidationError):
        ToolPermissionProfileAuthorization.model_validate(data)
    data = sample_models[ToolPermissionCheckRequest.__name__].model_dump(mode="json")
    data["target_resolution_verified"] = "true"
    with pytest.raises(ValidationError):
        ToolPermissionCheckRequest.model_validate(data)


@pytest.mark.parametrize("operation", GRANTABLE_OPERATIONS)
def test_each_grantable_operation_request_passes(
    operation: ToolPermissionOperation,
) -> None:
    result = build_compilation_result()
    request = grant_request(result, operation)
    assert request.operation is operation


@pytest.mark.parametrize("operation", NEVER_GRANTABLE_OPERATIONS)
def test_never_grantable_operation_request_fails(
    operation: ToolPermissionOperation,
) -> None:
    result = build_compilation_result()
    with pytest.raises(ValidationError):
        grant_request(result, operation)


def test_source_action_must_exist_and_not_be_forbidden() -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    missing = ToolPermissionGrantRequest(
        operation=ToolPermissionOperation.READ_FILE,
        source_allowed_action="not in WorkPacket",
        rationale="Missing source action fails.",
    )
    with pytest.raises(ToolPermissionProfileAuthorizationError):
        build_tool_permission_profile_authorization(
            authorizer_id="tool.authorizer.p17-2",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=result,
            allocation_result=allocation_result,
            grant_requests=(missing,),
        )
    forbidden = ToolPermissionGrantRequest(
        operation=ToolPermissionOperation.READ_FILE,
        source_allowed_action=result.work_packet.repository_scope.forbidden_actions[0],
        rationale="Forbidden source action fails.",
    )
    with pytest.raises(ToolPermissionProfileAuthorizationError):
        build_tool_permission_profile_authorization(
            authorizer_id="tool.authorizer.p17-2",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=result,
            allocation_result=allocation_result,
            grant_requests=(forbidden,),
        )


def test_duplicate_operations_and_empty_grants_fail() -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    duplicate = (
        grant_request(result, ToolPermissionOperation.READ_FILE),
        grant_request(result, ToolPermissionOperation.READ_FILE),
    )
    with pytest.raises(ToolPermissionProfileAuthorizationError):
        build_tool_permission_profile_authorization(
            authorizer_id="tool.authorizer.p17-2",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=result,
            allocation_result=allocation_result,
            grant_requests=duplicate,
        )
    with pytest.raises(ToolPermissionProfileAuthorizationError):
        build_tool_permission_profile_authorization(
            authorizer_id="tool.authorizer.p17-2",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=result,
            allocation_result=allocation_result,
            grant_requests=(),
        )


def test_request_order_is_normalized_to_enum_order() -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    authorization = build_tool_permission_profile_authorization(
        authorizer_id="tool.authorizer.p17-2",
        authorization_reference="AUTH-P17-2",
        rationale="Authorize profile.",
        compilation_result=result,
        allocation_result=allocation_result,
        grant_requests=(
            grant_request(result, ToolPermissionOperation.DELETE_DIRECTORY),
            grant_request(result, ToolPermissionOperation.LIST_DIRECTORY),
            grant_request(result, ToolPermissionOperation.READ_FILE),
        ),
        risk_acknowledgement="Synthetic mutation risk acknowledged.",
    )
    assert tuple(request.operation for request in authorization.grant_requests) == (
        ToolPermissionOperation.LIST_DIRECTORY,
        ToolPermissionOperation.READ_FILE,
        ToolPermissionOperation.DELETE_DIRECTORY,
    )


def test_authorization_is_deterministic_and_digest_valid(context_read_only) -> None:
    result = context_read_only["compilation_result"]
    allocation_result = context_read_only["allocation_result"]
    first = build_authorization(result, allocation_result)
    second = build_authorization(result, allocation_result)
    assert first == second
    assert first.authorization_SHA256 == tool_permissions._profile_authorization_digest(
        first
    )
    data = first.model_dump(mode="json")
    data["authorization_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        ToolPermissionProfileAuthorization.model_validate(data)


def test_authorization_rejects_false_synthetic_shadow_and_caller_binding(
    context_read_only,
) -> None:
    authorization = context_read_only["authorization"]
    data = authorization.model_dump(mode="json")
    data["profile_authorized"] = False
    with pytest.raises(ValidationError):
        ToolPermissionProfileAuthorization.model_validate(data)
    data = authorization.model_dump(mode="json")
    data["synthetic"] = True
    with pytest.raises(ValidationError):
        ToolPermissionProfileAuthorization.model_validate(data)
    with pytest.raises(ToolPermissionProfileAuthorizationError):
        build_tool_permission_profile_authorization(
            authorizer_id="SHADOW-tool-authorizer",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=context_read_only["compilation_result"],
            allocation_result=context_read_only["allocation_result"],
            grant_requests=(grant_request(context_read_only["compilation_result"]),),
        )
    with pytest.raises(TypeError):
        build_tool_permission_profile_authorization(
            authorizer_id="tool.authorizer.p17-2",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=context_read_only["compilation_result"],
            allocation_result=context_read_only["allocation_result"],
            grant_requests=(grant_request(context_read_only["compilation_result"]),),
            work_packet_id="caller-supplied",
        )


@pytest.mark.parametrize("operation", MUTATING_OPERATIONS)
def test_mutating_grants_require_risk_acknowledgement(
    operation: ToolPermissionOperation,
) -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    with pytest.raises(ToolPermissionProfileAuthorizationError):
        build_tool_permission_profile_authorization(
            authorizer_id="tool.authorizer.p17-2",
            authorization_reference="AUTH-P17-2",
            rationale="Authorize profile.",
            compilation_result=result,
            allocation_result=allocation_result,
            grant_requests=(grant_request(result, operation),),
        )


@pytest.mark.parametrize(
    "operation",
    (ToolPermissionOperation.LIST_DIRECTORY, ToolPermissionOperation.READ_FILE),
)
def test_read_only_grants_do_not_require_risk_acknowledgement(
    operation: ToolPermissionOperation,
) -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    authorization = build_authorization(result, allocation_result, (operation,))
    assert authorization.risk_acknowledgement is None


def test_authorization_does_not_mutate_inputs() -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    before = (result.model_dump_json(), allocation_result.model_dump_json())
    build_authorization(result, allocation_result)
    assert before == (result.model_dump_json(), allocation_result.model_dump_json())


@pytest.mark.parametrize(
    "updates",
    (
        ("compilation_result", {"disposition": "not_compiled"}),
        ("work_packet", {"execution_ready": True}),
        ("work_packet", {"git_authority": "machine"}),
    ),
)
def test_compilation_prerequisite_posture_is_required(updates) -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    target, patch_data = updates
    data = result.model_dump(mode="json")
    if target == "work_packet":
        data["work_packet"].update(patch_data)
    else:
        data.update(patch_data)
    with pytest.raises((ValidationError, ToolPermissionProfileError)):
        tampered = type(result).model_validate(data)
        build_authorization(tampered, allocation_result)


@pytest.mark.parametrize(
    "field_update",
    (
        {"disposition": "not_allocated"},
        {"lifecycle_state": "released"},
        {"exclusive": False},
        {"workspace_requirement_satisfied": False},
        {"execution_ready": True},
        {"tool_permissions_ready": True},
    ),
)
def test_allocation_prerequisite_posture_is_required(
    field_update: dict[str, object],
) -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    data = allocation_result.model_dump(mode="json")
    data["allocation"].update(field_update)
    with pytest.raises((ValidationError, ToolPermissionProfileError)):
        tampered = WorkspaceAllocationResult.model_validate(data)
        build_authorization(result, tampered)


def test_missing_tool_permission_requirement_fails() -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    data = result.model_dump(mode="json")
    data["work_packet"]["downstream_requirements"] = [
        requirement
        for requirement in data["work_packet"]["downstream_requirements"]
        if requirement["capability"]
        != WorkPacketDownstreamCapability.TOOL_PERMISSION_PROFILE.value
    ]
    with pytest.raises((ValidationError, ToolPermissionProfileError)):
        tampered = type(result).model_validate(data)
        build_authorization(tampered, allocation_result)


@pytest.mark.parametrize("allowed_paths", (("README.md",), ("docs/**",)))
def test_supported_scope_patterns_pass(allowed_paths: tuple[str, ...]) -> None:
    relative = "README.md" if allowed_paths == ("README.md",) else "docs"
    context = build_profile_context(
        (ToolPermissionOperation.READ_FILE,),
        allowed_paths=allowed_paths,
        forbidden_paths=("4_external/sources/**",),
    )
    decision = evaluate_tool_permission(
        check_request(
            context["profile"],
            context["allocation_result"].allocation,
            relative_path=relative,
            resolved_target_path=f"{WORKSPACE_ROOT}/{relative}",
        )
    )
    assert decision.decision is ToolPermissionDecision.ALLOW


@pytest.mark.parametrize(
    "bad_pattern",
    ("foo/*/bar", "foo/?.py", "foo/[ab].py", "**/file.py"),
)
def test_unsupported_scope_patterns_fail_closed(bad_pattern: str) -> None:
    result = build_compilation_result(allowed_paths=(bad_pattern,))
    allocation_result = build_allocation_result(result)
    authorization = build_authorization(result, allocation_result)
    request = ToolPermissionProfileRequest(
        compilation_result=result,
        allocation_result=allocation_result,
        profile_authorization=authorization,
    )
    with pytest.raises(ToolPermissionProfileInputError):
        build_tool_permission_profile(request)


def test_scope_order_is_preserved_and_not_rewritten() -> None:
    context = build_profile_context(
        (ToolPermissionOperation.READ_FILE,),
        allowed_paths=("docs/**", "README.md"),
        forbidden_paths=("4_external/sources/**", "graphify-out/**"),
    )
    grant = context["profile"].grants[0]
    assert grant.allowed_paths == ("docs/**", "README.md")
    assert grant.forbidden_paths == ("4_external/sources/**", "graphify-out/**")


@pytest.mark.parametrize("operation", GRANTABLE_OPERATIONS)
def test_grant_builds_for_each_operation(operation: ToolPermissionOperation) -> None:
    context = build_profile_context((operation,))
    grant = context["profile"].grants[0]
    assert grant.operation is operation
    assert (
        grant.allowed_paths
        == context["allocation_result"].allocation.scope_projection.allowed_paths
    )
    assert (
        grant.forbidden_paths
        == context["allocation_result"].allocation.scope_projection.forbidden_paths
    )
    assert grant.grant_SHA256 == tool_permissions._grant_digest(grant)


def test_multiple_grants_are_enum_ordered_and_source_objects_unchanged() -> None:
    result = build_compilation_result()
    allocation_result = build_allocation_result(result)
    authorization = build_authorization(
        result,
        allocation_result,
        (
            ToolPermissionOperation.DELETE_DIRECTORY,
            ToolPermissionOperation.READ_FILE,
            ToolPermissionOperation.LIST_DIRECTORY,
        ),
    )
    request = ToolPermissionProfileRequest(
        compilation_result=result,
        allocation_result=allocation_result,
        profile_authorization=authorization,
    )
    before = (
        result.model_dump_json(),
        allocation_result.model_dump_json(),
        request.model_dump_json(),
    )
    profile_result = build_tool_permission_profile(request)
    assert tuple(grant.operation for grant in profile_result.profile.grants) == (
        ToolPermissionOperation.LIST_DIRECTORY,
        ToolPermissionOperation.READ_FILE,
        ToolPermissionOperation.DELETE_DIRECTORY,
    )
    assert before == (
        result.model_dump_json(),
        allocation_result.model_dump_json(),
        request.model_dump_json(),
    )


def test_deny_first_profile_integrity_and_determinism(context_all_operations) -> None:
    profile_result = context_all_operations["profile_result"]
    profile = profile_result.profile
    same = build_tool_permission_profile(context_all_operations["request"])
    assert profile.state is ToolPermissionProfileState.ISSUED
    assert profile.tool_permissions_ready is True
    assert profile.execution_ready is False
    assert profile.git_authority is WorkPacketGitAuthority.HUMAN_ONLY
    assert profile.profile_id.startswith("TP-P17-0-R0001-")
    assert profile.profile_id.endswith(profile.profile_input_SHA256[:12])
    assert len({grant.operation for grant in profile.grants}) == len(profile.grants)
    assert not (
        {grant.operation for grant in profile.grants} & set(profile.denied_operations)
    )
    assert profile.protected_paths == PROTECTED_PATHS
    assert (
        profile.profile_input_SHA256
        == tool_permissions._profile_input_digest_from_record(
            tool_permissions._profile_input_record(profile)
        )
    )
    assert profile.profile_SHA256 == tool_permissions._profile_digest(profile)
    assert profile_result.result_SHA256 == tool_permissions._profile_result_digest(
        profile_result
    )
    assert same == profile_result


@pytest.mark.parametrize("operation", tuple(ToolPermissionOperation))
def test_denied_operations_are_exact_complement(
    context_read_only,
    operation: ToolPermissionOperation,
) -> None:
    profile = context_read_only["profile"]
    granted = {grant.operation for grant in profile.grants}
    assert (operation in profile.denied_operations) == (operation not in granted)


@pytest.mark.parametrize("protected_path", PROTECTED_PATHS)
def test_protected_paths_are_denied_and_grants_cannot_override(
    context_all_operations,
    protected_path: str,
) -> None:
    relative_path = (
        protected_path[:-3] + "/file.txt"
        if protected_path.endswith("/**")
        else protected_path
    )
    decision = evaluate_tool_permission(
        check_request(
            context_all_operations["profile"],
            context_all_operations["allocation_result"].allocation,
            operation=ToolPermissionOperation.READ_FILE,
            relative_path=relative_path,
            resolved_target_path=f"{WORKSPACE_ROOT}/{relative_path}",
        )
    )
    assert decision.decision is ToolPermissionDecision.DENY
    assert decision.reason is ToolPermissionDecisionReason.TARGET_IN_PROTECTED_ROOT
    assert decision.matched_forbidden_pattern == protected_path


def test_permission_request_binding_and_immutability(context_read_only) -> None:
    profile = context_read_only["profile"]
    allocation = context_read_only["allocation_result"].allocation
    request = check_request(profile, allocation)
    assert request.profile == profile
    assert request.allocation == allocation
    assert request.target_resolution_verified is True
    with pytest.raises(ValidationError):
        ToolPermissionCheckRequest.model_validate({
            **request.model_dump(mode="json"),
            "target_resolution_verified": False,
        })
    with pytest.raises(ValidationError):
        ToolPermissionCheckRequest.model_validate({
            **request.model_dump(mode="json"),
            "policy_id": "other-policy",
        })


@pytest.mark.parametrize(
    "field_update",
    (
        {"work_packet_id": "WP-P17-0-R0001-000000000000"},
        {"work_packet_SHA256": "0" * 64},
        {"allocation_id": "WS-P17-0-R0001-000000000000"},
        {"allocation_SHA256": "0" * 64},
        {"workspace_root": "C:/worktrees/other"},
        {"resolved_workspace_root": "C:/worktrees/other"},
    ),
)
def test_permission_request_profile_allocation_mismatch_fails(
    context_read_only,
    field_update: dict[str, object],
) -> None:
    profile_data = context_read_only["profile"].model_dump(mode="json")
    profile_data.update(field_update)
    profile_data["profile_SHA256"] = "0" * 64
    with pytest.raises((ValidationError, ToolPermissionEvaluationError)):
        profile = ToolPermissionProfile.model_validate(profile_data)
        ToolPermissionCheckRequest(
            profile=profile,
            allocation=context_read_only["allocation_result"].allocation,
            operation=ToolPermissionOperation.READ_FILE,
            workspace_relative_path=ALLOWED_RELATIVE_PATH,
            resolved_target_path=f"{WORKSPACE_ROOT}/{ALLOWED_RELATIVE_PATH}",
            request_reference="CHECK-P17-2",
        )


@pytest.mark.parametrize("operation", GRANTABLE_OPERATIONS)
def test_evaluator_allows_each_granted_filesystem_operation(
    context_all_operations,
    operation: ToolPermissionOperation,
) -> None:
    decision = evaluate_tool_permission(
        check_request(
            context_all_operations["profile"],
            context_all_operations["allocation_result"].allocation,
            operation=operation,
        )
    )
    assert decision.decision is ToolPermissionDecision.ALLOW
    assert decision.reason is ToolPermissionDecisionReason.ALLOWED_BY_EXPLICIT_GRANT
    assert decision.matched_allowed_pattern is not None
    assert decision.matched_forbidden_pattern is None
    assert decision.decision_SHA256 == tool_permissions._decision_digest(decision)


def test_evaluator_same_input_same_decision(context_read_only) -> None:
    request = check_request(
        context_read_only["profile"],
        context_read_only["allocation_result"].allocation,
    )
    assert evaluate_tool_permission(request) == evaluate_tool_permission(request)


def test_ungranted_grantable_operation_is_denied(context_read_only) -> None:
    decision = evaluate_tool_permission(
        check_request(
            context_read_only["profile"],
            context_read_only["allocation_result"].allocation,
            operation=ToolPermissionOperation.DELETE_FILE,
        )
    )
    assert decision.decision is ToolPermissionDecision.DENY
    assert decision.reason is ToolPermissionDecisionReason.OPERATION_NOT_GRANTED


@pytest.mark.parametrize("operation", NEVER_GRANTABLE_OPERATIONS)
def test_never_grantable_operations_are_explicitly_denied(
    context_all_operations,
    operation: ToolPermissionOperation,
) -> None:
    decision = evaluate_tool_permission(
        check_request(
            context_all_operations["profile"],
            context_all_operations["allocation_result"].allocation,
            operation=operation,
        )
    )
    assert decision.decision is ToolPermissionDecision.DENY
    assert decision.reason is ToolPermissionDecisionReason.OPERATION_EXPLICITLY_DENIED


@pytest.mark.parametrize(
    ("relative_path", "resolved_path", "reason"),
    (
        ("", f"{WORKSPACE_ROOT}/", ToolPermissionDecisionReason.TARGET_PATH_INVALID),
        (
            "/absolute",
            f"{WORKSPACE_ROOT}/absolute",
            ToolPermissionDecisionReason.TARGET_PATH_INVALID,
        ),
        (
            "bad\\path",
            f"{WORKSPACE_ROOT}/bad/path",
            ToolPermissionDecisionReason.TARGET_PATH_INVALID,
        ),
        (
            "../escape",
            f"{WORKSPACE_ROOT}/escape",
            ToolPermissionDecisionReason.TARGET_PATH_INVALID,
        ),
        (
            "bad\x00path",
            f"{WORKSPACE_ROOT}/badpath",
            ToolPermissionDecisionReason.TARGET_PATH_INVALID,
        ),
        (
            ALLOWED_RELATIVE_PATH,
            f"C:/other/{ALLOWED_RELATIVE_PATH}",
            ToolPermissionDecisionReason.TARGET_OUTSIDE_WORKSPACE,
        ),
        (
            ALLOWED_RELATIVE_PATH,
            f"{WORKSPACE_ROOT}/other.py",
            ToolPermissionDecisionReason.TARGET_OUTSIDE_WORKSPACE,
        ),
        (
            FORBIDDEN_RELATIVE_PATH,
            f"{WORKSPACE_ROOT}/{FORBIDDEN_RELATIVE_PATH}",
            ToolPermissionDecisionReason.TARGET_IN_FORBIDDEN_SCOPE,
        ),
        (
            OUT_OF_SCOPE_RELATIVE_PATH,
            f"{WORKSPACE_ROOT}/{OUT_OF_SCOPE_RELATIVE_PATH}",
            ToolPermissionDecisionReason.TARGET_NOT_IN_ALLOWED_SCOPE,
        ),
    ),
)
def test_path_denials_return_evidence_without_filesystem_access(
    context_read_only,
    relative_path: str,
    resolved_path: str,
    reason: ToolPermissionDecisionReason,
) -> None:
    decision = evaluate_tool_permission(
        check_request(
            context_read_only["profile"],
            context_read_only["allocation_result"].allocation,
            relative_path=relative_path,
            resolved_target_path=resolved_path,
        )
    )
    assert decision.decision is ToolPermissionDecision.DENY
    assert decision.reason is reason


def test_deny_precedence_prefers_protected_before_operation_denial(
    context_read_only,
) -> None:
    decision = evaluate_tool_permission(
        check_request(
            context_read_only["profile"],
            context_read_only["allocation_result"].allocation,
            operation=ToolPermissionOperation.EXECUTE_COMMAND,
            relative_path=".git/config",
            resolved_target_path=f"{WORKSPACE_ROOT}/.git/config",
        )
    )
    assert decision.reason is ToolPermissionDecisionReason.TARGET_IN_PROTECTED_ROOT


@pytest.mark.parametrize("reason", tuple(ToolPermissionDecisionReason))
def test_decision_reason_consistency_validates(
    reason: ToolPermissionDecisionReason, context_read_only
) -> None:
    profile = context_read_only["profile"]
    base = {
        "schema_version": TOOL_PERMISSION_SCHEMA_VERSION,
        "decision": ToolPermissionDecision.ALLOW
        if reason is ToolPermissionDecisionReason.ALLOWED_BY_EXPLICIT_GRANT
        else ToolPermissionDecision.DENY,
        "reason": reason,
        "operation": ToolPermissionOperation.READ_FILE,
        "work_packet_id": profile.work_packet_id,
        "allocation_id": profile.allocation_id,
        "profile_id": profile.profile_id,
        "workspace_relative_path": ALLOWED_RELATIVE_PATH,
        "resolved_target_path": f"{WORKSPACE_ROOT}/{ALLOWED_RELATIVE_PATH}",
        "matched_allowed_pattern": "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/**"
        if reason is ToolPermissionDecisionReason.ALLOWED_BY_EXPLICIT_GRANT
        else None,
        "matched_forbidden_pattern": ".git/**"
        if reason
        in {
            ToolPermissionDecisionReason.TARGET_IN_PROTECTED_ROOT,
            ToolPermissionDecisionReason.TARGET_IN_FORBIDDEN_SCOPE,
        }
        else None,
        "profile_SHA256": profile.profile_SHA256,
    }
    decision_input = tool_permissions._decision_input_digest_from_record(base)
    evidence_data = {**base, "decision_input_SHA256": decision_input}
    evidence = ToolPermissionDecisionEvidence(
        **evidence_data,
        decision_SHA256=tool_permissions._decision_digest_from_record(evidence_data),
    )
    validate_tool_permission_decision(evidence)


def test_decision_tampering_fails(context_read_only) -> None:
    decision = evaluate_tool_permission(
        check_request(
            context_read_only["profile"],
            context_read_only["allocation_result"].allocation,
        )
    )
    for field in (
        "matched_allowed_pattern",
        "decision_input_SHA256",
        "decision_SHA256",
        "profile_SHA256",
    ):
        data = decision.model_dump(mode="json")
        data[field] = None if field == "matched_allowed_pattern" else "0" * 64
        with pytest.raises((ValidationError, ToolPermissionProfileIntegrityError)):
            tampered = ToolPermissionDecisionEvidence.model_validate(data)
            validate_tool_permission_decision(tampered)


def test_profile_tampering_fails(context_read_only) -> None:
    profile = context_read_only["profile"]
    for field in ("profile_input_SHA256", "profile_SHA256"):
        data = profile.model_dump(mode="json")
        data[field] = "0" * 64
        with pytest.raises((ValidationError, ToolPermissionProfileIntegrityError)):
            tampered = ToolPermissionProfile.model_validate(data)
            validate_tool_permission_profile(tampered)


def test_profile_contains_no_runtime_handles_or_payloads(context_read_only) -> None:
    data = context_read_only["profile"].model_dump(mode="json")
    forbidden_keys = {
        "provider_id",
        "model_id",
        "agent_id",
        "worker_id",
        "process_id",
        "execution_id",
        "tool_handle",
        "filesystem_handle",
        "git_handle",
        "command_payload",
        "validation_result",
        "diff",
        "artifact_content",
        "credential",
    }
    assert not (forbidden_keys & set(data))


@pytest.mark.parametrize(
    "name",
    (
        "os",
        "Path",
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "openai",
        "docker",
        "git",
    ),
)
def test_forbidden_runtime_imports_absent(name: str) -> None:
    assert name not in tool_permissions.__dict__


@pytest.mark.parametrize(
    "name",
    (
        "execute_tool",
        "run_command",
        "ValidationCommandRunner",
        "SingleAgentTicketExecutor",
        "ProviderSelector",
        "ModelSelector",
        "WorkerAllocator",
        "ResultEnvelope",
        "DiffReview",
        "ArtifactReview",
        "GitHandoff",
    ),
)
def test_forbidden_runtime_surfaces_absent(name: str) -> None:
    assert not hasattr(tool_permissions, name)


def test_p17_0_shadow_rejection_output_is_retained() -> None:
    with pytest.raises(work_packet.WorkPacketCompilerAuthorizationError) as exc:
        work_packet.build_work_packet_compilation_authorization(
            authorizer_id="SHADOW-AUTHORIZER",
            authorization_reference="AUTH-P17-0",
            rationale="Synthetic authorization.",
            approval_record=build_bundle()["approval"],
            publication_result=build_bundle()["publication"],
        )
    assert (
        f"{type(exc.value).__name__} {exc.value}"
        == "WorkPacketCompilerAuthorizationError shadow-only approval evidence cannot authorize WorkPacket compilation"
    )


def test_permission_decision_smoke_outputs(
    context_read_only, context_all_operations
) -> None:
    read_profile = context_read_only["profile"]
    all_profile = context_all_operations["profile"]
    read_allocation = context_read_only["allocation_result"].allocation
    all_allocation = context_all_operations["allocation_result"].allocation
    decisions = (
        evaluate_tool_permission(check_request(read_profile, read_allocation)),
        evaluate_tool_permission(
            check_request(
                read_profile,
                read_allocation,
                operation=ToolPermissionOperation.DELETE_FILE,
            )
        ),
        evaluate_tool_permission(
            check_request(
                all_profile,
                all_allocation,
                operation=ToolPermissionOperation.EXECUTE_COMMAND,
            )
        ),
        evaluate_tool_permission(
            check_request(
                read_profile,
                read_allocation,
                relative_path=".git/config",
                resolved_target_path=f"{WORKSPACE_ROOT}/.git/config",
            )
        ),
        evaluate_tool_permission(
            check_request(
                read_profile,
                read_allocation,
                relative_path=FORBIDDEN_RELATIVE_PATH,
                resolved_target_path=f"{WORKSPACE_ROOT}/{FORBIDDEN_RELATIVE_PATH}",
            )
        ),
        evaluate_tool_permission(
            check_request(
                read_profile,
                read_allocation,
                resolved_target_path=f"C:/outside/{ALLOWED_RELATIVE_PATH}",
            )
        ),
        evaluate_tool_permission(
            check_request(
                read_profile,
                read_allocation,
                relative_path=OUT_OF_SCOPE_RELATIVE_PATH,
                resolved_target_path=f"{WORKSPACE_ROOT}/{OUT_OF_SCOPE_RELATIVE_PATH}",
            )
        ),
    )
    assert tuple(
        f"{item.decision.value} {item.reason.value} {item.operation.value}"
        for item in decisions
    ) == (
        "allow allowed_by_explicit_grant read_file",
        "deny operation_not_granted delete_file",
        "deny operation_explicitly_denied execute_command",
        "deny target_in_protected_root read_file",
        "deny target_in_forbidden_scope read_file",
        "deny target_outside_workspace read_file",
        "deny target_not_in_allowed_scope read_file",
    )
    assert sum(item.decision is ToolPermissionDecision.ALLOW for item in decisions) == 1
    assert sum(item.decision is ToolPermissionDecision.DENY for item in decisions) == 6
