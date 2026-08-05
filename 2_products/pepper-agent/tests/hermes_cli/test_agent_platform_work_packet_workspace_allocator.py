import importlib
from enum import Enum
from pathlib import Path
from typing import get_args, get_origin

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.workspace_allocator as allocator_module
from hermes_cli.agent_platform.work_packet import (
    WORKSPACE_ALLOCATION_POLICY_ID,
    WORKSPACE_ALLOCATION_SCHEMA_VERSION,
    WORK_PACKET_COMPILER_POLICY_ID,
    WORK_PACKET_COMPILER_SCHEMA_VERSION,
    WORK_PACKET_SCHEMA_VERSION,
    WorkPacket,
    WorkPacketAuthorityBoundary,
    WorkPacketCompilationAuthorization,
    WorkPacketCompilationDisposition,
    WorkPacketCompilationEvidence,
    WorkPacketCompilationRequest,
    WorkPacketCompilationResult,
    WorkPacketCompilerAuthorizationError,
    WorkPacketCompilerError,
    WorkPacketCompilerInputError,
    WorkPacketCompilerIntegrityError,
    WorkPacketDownstreamCapability,
    WorkPacketDownstreamRequirement,
    WorkPacketExecutionMode,
    WorkPacketGitAuthority,
    WorkPacketRepositoryScope,
    WorkPacketTaskStep,
    WorkPacketValidationKind,
    WorkPacketValidationStep,
    WorkspaceAllocation,
    WorkspaceAllocationAuthorization,
    WorkspaceAllocationDisposition,
    WorkspaceAllocationRegistry,
    WorkspaceAllocationRequest,
    WorkspaceAllocationResult,
    WorkspaceAllocatorAuthorizationError,
    WorkspaceAllocatorCollisionError,
    WorkspaceAllocatorError,
    WorkspaceAllocatorInputError,
    WorkspaceAllocatorInspectionError,
    WorkspaceAllocatorIntegrityError,
    WorkspaceCleanupAssessment,
    WorkspaceCleanupEligibility,
    WorkspaceInspectionEvidence,
    WorkspaceIsolationLevel,
    WorkspaceKind,
    WorkspaceLifecycleState,
    WorkspaceRepositoryIdentity,
    WorkspaceReservation,
    WorkspaceScopeProjection,
    allocate_workspace,
    assess_workspace_cleanup_eligibility,
    build_work_packet_compilation_authorization,
    build_workspace_allocation_authorization,
    build_workspace_repository_identity,
    compile_ticket_spec_to_work_packet,
    get_empty_workspace_allocation_registry,
    inspect_human_provisioned_workspace,
    validate_work_packet,
    validate_workspace_allocation,
    validate_workspace_allocation_registry,
)
from tests.hermes_cli.test_agent_platform_work_packet_compiler import (
    EXPECTED_EXPORTS as P17_0_EXPORTS,
    build_bundle,
)


P17_1_EXPORTS = (
    "WORKSPACE_ALLOCATION_SCHEMA_VERSION",
    "WORKSPACE_ALLOCATION_POLICY_ID",
    "WorkspaceKind",
    "WorkspaceLifecycleState",
    "WorkspaceIsolationLevel",
    "WorkspaceAllocationDisposition",
    "WorkspaceCleanupEligibility",
    "WorkspaceRepositoryIdentity",
    "WorkspaceAllocationAuthorization",
    "WorkspaceInspectionEvidence",
    "WorkspaceScopeProjection",
    "WorkspaceReservation",
    "WorkspaceAllocationRegistry",
    "WorkspaceAllocationRequest",
    "WorkspaceAllocation",
    "WorkspaceAllocationResult",
    "WorkspaceCleanupAssessment",
    "WorkspaceAllocatorError",
    "WorkspaceAllocatorInputError",
    "WorkspaceAllocatorAuthorizationError",
    "WorkspaceAllocatorInspectionError",
    "WorkspaceAllocatorCollisionError",
    "WorkspaceAllocatorIntegrityError",
    "build_workspace_repository_identity",
    "build_workspace_allocation_authorization",
    "get_empty_workspace_allocation_registry",
    "inspect_human_provisioned_workspace",
    "allocate_workspace",
    "validate_workspace_allocation",
    "validate_workspace_allocation_registry",
    "assess_workspace_cleanup_eligibility",
)
PUBLIC_MODELS = (
    WorkspaceRepositoryIdentity,
    WorkspaceAllocationAuthorization,
    WorkspaceInspectionEvidence,
    WorkspaceScopeProjection,
    WorkspaceReservation,
    WorkspaceAllocationRegistry,
    WorkspaceAllocationRequest,
    WorkspaceAllocation,
    WorkspaceAllocationResult,
    WorkspaceCleanupAssessment,
)
SOURCE_COMMIT = "a" * 40
OTHER_COMMIT = "b" * 40
WORKSPACE_BRANCH = "p17/workspace-allocator"
OTHER_BRANCH = "p17/other-workspace"
WORKSPACE_ROOT = "C:/worktrees/pepper-p17-1"
OTHER_ROOT = "C:/worktrees/pepper-p17-2"
CHILD_ROOT = "C:/worktrees/pepper-p17-1/child"
REPOSITORY_ID = "pepper-agent"
READ_ONLY_COMMANDS = (
    ("rev-parse", "--is-inside-work-tree"),
    ("rev-parse", "--show-toplevel"),
    ("rev-parse", "HEAD"),
    ("branch", "--show-current"),
    ("rev-parse", "--git-dir"),
    ("rev-parse", "--git-common-dir"),
    ("status", "--porcelain=v1", "-uall"),
)


def assert_validation_fails(factory) -> None:
    with pytest.raises(ValidationError):
        factory()


def metadata(
    *,
    exists: bool = True,
    is_dir: bool = True,
    is_symlink: bool = False,
    resolved_workspace_root: str = WORKSPACE_ROOT,
) -> allocator_module._WorkspacePathMetadata:
    return allocator_module._WorkspacePathMetadata(
        exists=exists,
        is_dir=is_dir,
        is_symlink=is_symlink,
        resolved_workspace_root=resolved_workspace_root,
    )


def git_responses(
    *,
    top_level: str = WORKSPACE_ROOT,
    commit: str = SOURCE_COMMIT,
    branch: str = WORKSPACE_BRANCH,
    git_dir: str = "C:/repo/.git/worktrees/pepper-p17-1",
    common_dir: str = "C:/repo/.git",
    inside: str = "true",
    status: str = "",
) -> dict[tuple[str, ...], str]:
    return {
        ("rev-parse", "--is-inside-work-tree"): inside,
        ("rev-parse", "--show-toplevel"): top_level,
        ("rev-parse", "HEAD"): commit,
        ("branch", "--show-current"): branch,
        ("rev-parse", "--git-dir"): git_dir,
        ("rev-parse", "--git-common-dir"): common_dir,
        ("status", "--porcelain=v1", "-uall"): status,
    }


def patch_inspection(
    monkeypatch: pytest.MonkeyPatch,
    *,
    path_metadata: allocator_module._WorkspacePathMetadata | None = None,
    responses: dict[tuple[str, ...], str] | None = None,
) -> list[tuple[str, ...]]:
    calls: list[tuple[str, ...]] = []
    response_map = responses or git_responses()

    monkeypatch.setattr(
        allocator_module,
        "_workspace_path_metadata",
        lambda workspace_root: path_metadata or metadata(),
    )

    def fake_git(workspace_root: str, args: tuple[str, ...]) -> str:
        assert workspace_root == WORKSPACE_ROOT
        calls.append(args)
        return response_map[args]

    monkeypatch.setattr(allocator_module, "_run_git_command", fake_git)
    return calls


@pytest.fixture(scope="module")
def compilation_result() -> WorkPacketCompilationResult:
    return build_bundle()["result"]


@pytest.fixture()
def repository_identity() -> WorkspaceRepositoryIdentity:
    return build_workspace_repository_identity(
        repository_id=REPOSITORY_ID,
        source_commit=SOURCE_COMMIT,
        workspace_branch=WORKSPACE_BRANCH,
    )


@pytest.fixture()
def allocation_authorization(
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
) -> WorkspaceAllocationAuthorization:
    return build_workspace_allocation_authorization(
        authorizer_id="workspace.authorizer.p17-1",
        authorization_reference="AUTH-P17-1",
        rationale="Authorize synthetic human-provisioned workspace reservation.",
        compilation_result=compilation_result,
        repository_identity=repository_identity,
        workspace_root=WORKSPACE_ROOT,
    )


@pytest.fixture()
def empty_registry() -> WorkspaceAllocationRegistry:
    return get_empty_workspace_allocation_registry()


@pytest.fixture()
def allocation_request(
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
    allocation_authorization: WorkspaceAllocationAuthorization,
    empty_registry: WorkspaceAllocationRegistry,
) -> WorkspaceAllocationRequest:
    return WorkspaceAllocationRequest(
        compilation_result=compilation_result,
        repository_identity=repository_identity,
        allocation_authorization=allocation_authorization,
        registry=empty_registry,
    )


@pytest.fixture()
def inspection_evidence(
    monkeypatch: pytest.MonkeyPatch,
    repository_identity: WorkspaceRepositoryIdentity,
) -> WorkspaceInspectionEvidence:
    patch_inspection(monkeypatch)
    return inspect_human_provisioned_workspace(
        workspace_root=WORKSPACE_ROOT,
        repository_identity=repository_identity,
    )


@pytest.fixture()
def allocation_result(
    monkeypatch: pytest.MonkeyPatch,
    allocation_request: WorkspaceAllocationRequest,
) -> WorkspaceAllocationResult:
    patch_inspection(monkeypatch)
    return allocate_workspace(allocation_request)


@pytest.fixture()
def allocation(allocation_result: WorkspaceAllocationResult) -> WorkspaceAllocation:
    return allocation_result.allocation


def make_reservation(
    allocation: WorkspaceAllocation,
    *,
    allocation_id: str | None = None,
    work_packet_id: str | None = None,
    workspace_root: str | None = None,
    resolved_workspace_root: str | None = None,
    source_commit: str | None = None,
    workspace_branch: str | None = None,
) -> WorkspaceReservation:
    data = {
        "allocation_id": allocation_id or allocation.allocation_id,
        "work_packet_id": work_packet_id or allocation.work_packet_id,
        "work_packet_SHA256": allocation.work_packet_SHA256,
        "workspace_root": workspace_root or allocation.workspace_root,
        "resolved_workspace_root": resolved_workspace_root
        or allocation.resolved_workspace_root,
        "source_commit": source_commit or allocation.repository_identity.source_commit,
        "workspace_branch": workspace_branch
        or allocation.repository_identity.workspace_branch,
        "lifecycle_state": WorkspaceLifecycleState.ALLOCATED,
    }
    return WorkspaceReservation(
        **data,
        allocation_SHA256=allocator_module._reservation_digest_from_record(data),
    )


def make_registry(
    reservations: tuple[WorkspaceReservation, ...], *, revision: int = 1
) -> WorkspaceAllocationRegistry:
    ordered = tuple(sorted(reservations, key=lambda item: item.allocation_id))
    data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "policy_id": WORKSPACE_ALLOCATION_POLICY_ID,
        "revision": revision,
        "reservations": ordered,
    }
    return WorkspaceAllocationRegistry(
        **data,
        registry_SHA256=allocator_module._registry_digest_from_record(data),
    )


@pytest.mark.parametrize("exported_name", P17_1_EXPORTS)
def test_p17_1_exports_are_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


@pytest.mark.parametrize("exported_name", P17_0_EXPORTS)
def test_p17_0_exports_remain_available(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


def test_public_export_prefix_and_counts() -> None:
    assert work_packet.__all__[: len(P17_0_EXPORTS)] == P17_0_EXPORTS
    assert work_packet.__all__[: len(P17_0_EXPORTS) + len(P17_1_EXPORTS)] == (
        P17_0_EXPORTS + P17_1_EXPORTS
    )
    assert len(work_packet.__all__) >= 56
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)
    assert not hasattr(work_packet, "execute_work_packet")
    assert not hasattr(work_packet, "create_git_worktree")


def test_import_smoke_exact_output() -> None:
    required = (
        "WorkPacket",
        "WorkspaceAllocation",
        "WorkspaceAllocationResult",
        "WorkspaceAllocationRegistry",
        "allocate_workspace",
        "inspect_human_provisioned_workspace",
    )
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        all(hasattr(work_packet, name) for name in required),
        hasattr(work_packet, "execute_work_packet"),
        hasattr(work_packet, "create_git_worktree"),
    ) == (
        len(work_packet.__all__),
        len(work_packet.__all__),
        True,
        False,
        False,
    )


def test_function_import_smoke_exact_output() -> None:
    assert (
        build_workspace_repository_identity.__name__,
        build_workspace_allocation_authorization.__name__,
        get_empty_workspace_allocation_registry.__name__,
        inspect_human_provisioned_workspace.__name__,
        allocate_workspace.__name__,
        validate_workspace_allocation.__name__,
        assess_workspace_cleanup_eligibility.__name__,
    ) == (
        "build_workspace_repository_identity",
        "build_workspace_allocation_authorization",
        "get_empty_workspace_allocation_registry",
        "inspect_human_provisioned_workspace",
        "allocate_workspace",
        "validate_workspace_allocation",
        "assess_workspace_cleanup_eligibility",
    )


def test_module_reload_has_no_inspection_or_git_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_git(*args, **kwargs):
        raise AssertionError("import attempted Git inspection")

    monkeypatch.setattr(allocator_module.subprocess, "run", fail_git)
    reloaded = importlib.reload(work_packet)
    assert reloaded.__all__[: len(P17_0_EXPORTS)] == P17_0_EXPORTS
    assert len(reloaded.__all__) >= 56


def test_constants_are_canonical() -> None:
    assert WORK_PACKET_SCHEMA_VERSION == 1
    assert WORK_PACKET_COMPILER_SCHEMA_VERSION == 1
    assert WORK_PACKET_COMPILER_POLICY_ID == "pepper-work-packet-compiler-policy-v1"
    assert WORKSPACE_ALLOCATION_SCHEMA_VERSION == 1
    assert (
        WORKSPACE_ALLOCATION_POLICY_ID
        == "pepper-human-provisioned-workspace-allocation-v1"
    )


@pytest.mark.parametrize(
    ("enum_class", "members"),
    (
        (WorkspaceKind, ("human_provisioned_git_worktree",)),
        (WorkspaceLifecycleState, ("allocated",)),
        (WorkspaceIsolationLevel, ("dedicated",)),
        (WorkspaceAllocationDisposition, ("allocated",)),
        (WorkspaceCleanupEligibility, ("not_eligible", "eligible")),
    ),
)
def test_enums_are_exact(enum_class: type[Enum], members: tuple[str, ...]) -> None:
    assert tuple(item.value for item in enum_class) == members
    assert len(enum_class) == len(enum_class.__members__)
    with pytest.raises(ValueError):
        enum_class("unsupported")


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_are_frozen_extra_forbid(model: type[BaseModel]) -> None:
    assert model.model_config.get("frozen") is True
    assert model.model_config.get("extra") == "forbid"
    assert model.model_config.get("validate_default") is True
    assert model.model_config.get("str_strip_whitespace") is True


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_reject_extra_fields(model: type[BaseModel]) -> None:
    payload = model.model_json_schema()
    assert payload.get("additionalProperties") is False


@pytest.mark.parametrize(
    "model",
    (
        WorkspaceAllocationAuthorization,
        WorkspaceAllocationRegistry,
        WorkspaceAllocationRequest,
        WorkspaceAllocation,
        WorkspaceAllocationResult,
    ),
)
def test_alternative_schema_versions_fail(
    model: type[BaseModel], allocation_result
) -> None:
    sample = sample_for_model(model, allocation_result)
    data = sample.model_dump(mode="json")
    data["schema_version"] = 2
    assert_validation_fails(lambda: model(**data))


@pytest.mark.parametrize(
    "model",
    (WorkspaceAllocationRegistry, WorkspaceAllocationRequest, WorkspaceAllocation),
)
def test_alternative_policy_ids_fail(model: type[BaseModel], allocation_result) -> None:
    sample = sample_for_model(model, allocation_result)
    data = sample.model_dump(mode="json")
    data["policy_id"] = "other-policy"
    assert_validation_fails(lambda: model(**data))


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_model_collections_are_immutable(model: type[BaseModel]) -> None:
    for field in model.model_fields.values():
        origin = get_origin(field.annotation)
        assert origin not in (list, dict, set)


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_fields_have_no_forbidden_runtime_shapes(model: type[BaseModel]) -> None:
    for field in model.model_fields.values():
        annotation = field.annotation
        assert annotation is not Path
        assert get_origin(annotation) is not dict
        assert get_origin(annotation) is not object


def test_repository_identity_builds_and_is_deterministic(
    repository_identity: WorkspaceRepositoryIdentity,
) -> None:
    repeated = build_workspace_repository_identity(
        repository_id=REPOSITORY_ID,
        source_commit=SOURCE_COMMIT,
        workspace_branch=WORKSPACE_BRANCH,
    )
    assert repository_identity == repeated
    assert repository_identity.repository_id == REPOSITORY_ID
    assert repository_identity.source_commit == SOURCE_COMMIT
    assert repository_identity.workspace_branch == WORKSPACE_BRANCH
    assert len(repository_identity.identity_SHA256) == 64


@pytest.mark.parametrize(
    "source_commit",
    ("A" * 40, "a" * 39, "g" * 40, "a" * 41),
)
def test_repository_identity_rejects_invalid_commits(source_commit: str) -> None:
    with pytest.raises(WorkspaceAllocatorInputError):
        build_workspace_repository_identity(
            repository_id=REPOSITORY_ID,
            source_commit=source_commit,
            workspace_branch=WORKSPACE_BRANCH,
        )


@pytest.mark.parametrize(
    "workspace_branch",
    (
        "has space",
        "-leading",
        "topic..x",
        "topic@{1",
        "topic~1",
        "topic^",
        "bad:ref",
        "bad?ref",
        "bad*ref",
        "bad[ref",
        "bad\\ref",
    ),
)
def test_repository_identity_rejects_invalid_branches(workspace_branch: str) -> None:
    with pytest.raises(WorkspaceAllocatorInputError):
        build_workspace_repository_identity(
            repository_id=REPOSITORY_ID,
            source_commit=SOURCE_COMMIT,
            workspace_branch=workspace_branch,
        )


def test_repository_identity_digest_changes_with_commit(
    repository_identity: WorkspaceRepositoryIdentity,
) -> None:
    changed = build_workspace_repository_identity(
        repository_id=REPOSITORY_ID,
        source_commit=OTHER_COMMIT,
        workspace_branch=WORKSPACE_BRANCH,
    )
    assert changed.identity_SHA256 != repository_identity.identity_SHA256


@pytest.mark.parametrize("workspace_root", ("C:/worktrees/p17", "/tmp/p17"))
def test_workspace_path_valid_forms_do_not_inspect_filesystem(
    workspace_root: str,
) -> None:
    assert (
        WorkspaceAllocationAuthorization.model_fields["workspace_root"].annotation
        is not Path
    )
    assert (
        allocator_module._validate_absolute_workspace_path(workspace_root)
        == workspace_root
    )


@pytest.mark.parametrize(
    "workspace_root",
    (
        "relative/path",
        "C:\\worktrees\\p17",
        "C:/worktrees/../p17",
        "C:/worktrees/p17\x00",
        "C:/worktrees/p17/",
        "C:/repo/.git",
        "C:/repo/.opencode/work",
        "C:/repo/graphify-out/work",
        "C:/repo/4_external/sources/work",
        "C:/repo/2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
    ),
)
def test_workspace_path_rejects_unsafe_forms(workspace_root: str) -> None:
    with pytest.raises(ValueError):
        allocator_module._validate_absolute_workspace_path(workspace_root)


def test_allocation_authorization_builds_and_is_deterministic(
    allocation_authorization: WorkspaceAllocationAuthorization,
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
) -> None:
    repeated = build_workspace_allocation_authorization(
        authorizer_id="workspace.authorizer.p17-1",
        authorization_reference="AUTH-P17-1",
        rationale="Authorize synthetic human-provisioned workspace reservation.",
        compilation_result=compilation_result,
        repository_identity=repository_identity,
        workspace_root=WORKSPACE_ROOT,
    )
    assert allocation_authorization == repeated
    assert allocation_authorization.synthetic is False
    assert allocation_authorization.allocation_authorized is True
    assert (
        allocation_authorization.workspace_kind
        is WorkspaceKind.HUMAN_PROVISIONED_GIT_WORKTREE
    )
    assert allocation_authorization.git_authority is WorkPacketGitAuthority.HUMAN_ONLY


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("synthetic", True),
        ("allocation_authorized", False),
        ("authorization_SHA256", "0" * 64),
    ),
)
def test_allocation_authorization_rejects_tampering(
    allocation_authorization: WorkspaceAllocationAuthorization,
    field: str,
    value: object,
) -> None:
    data = allocation_authorization.model_dump(mode="json")
    data[field] = value
    assert_validation_fails(lambda: WorkspaceAllocationAuthorization(**data))


def test_allocation_authorization_rejects_shadow_authorizer(
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
) -> None:
    with pytest.raises(WorkspaceAllocatorAuthorizationError):
        build_workspace_allocation_authorization(
            authorizer_id="SHADOW-authorizer",
            authorization_reference="AUTH-P17-1",
            rationale="Authorize synthetic workspace reservation.",
            compilation_result=compilation_result,
            repository_identity=repository_identity,
            workspace_root=WORKSPACE_ROOT,
        )


def test_allocation_authorization_preserves_inputs(
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
) -> None:
    result_before = compilation_result.model_dump(mode="json")
    identity_before = repository_identity.model_dump(mode="json")
    build_workspace_allocation_authorization(
        authorizer_id="workspace.authorizer.p17-1",
        authorization_reference="AUTH-P17-1",
        rationale="Authorize synthetic workspace reservation.",
        compilation_result=compilation_result,
        repository_identity=repository_identity,
        workspace_root=WORKSPACE_ROOT,
    )
    assert compilation_result.model_dump(mode="json") == result_before
    assert repository_identity.model_dump(mode="json") == identity_before


def test_p17_0_prerequisite_posture(
    compilation_result: WorkPacketCompilationResult,
) -> None:
    packet = compilation_result.work_packet
    requirement = next(
        item
        for item in packet.downstream_requirements
        if item.capability is WorkPacketDownstreamCapability.WORKSPACE_ALLOCATION
    )
    assert compilation_result.disposition is WorkPacketCompilationDisposition.COMPILED
    assert packet.authority_boundary is WorkPacketAuthorityBoundary.COMPILE_ONLY
    assert packet.execution_ready is False
    assert packet.git_authority is WorkPacketGitAuthority.HUMAN_ONLY
    assert requirement.required is True
    assert requirement.satisfied_by_compiler is False


@pytest.mark.parametrize("missing", (True, False))
def test_p17_0_workspace_requirement_is_required(
    compilation_result: WorkPacketCompilationResult,
    repository_identity: WorkspaceRepositoryIdentity,
    missing: bool,
) -> None:
    packet = compilation_result.work_packet
    requirements = tuple(
        item
        for item in packet.downstream_requirements
        if item.capability is not WorkPacketDownstreamCapability.WORKSPACE_ALLOCATION
    )
    if not missing:
        requirement = next(
            item
            for item in packet.downstream_requirements
            if item.capability is WorkPacketDownstreamCapability.WORKSPACE_ALLOCATION
        )
        requirements = (
            *requirements,
            requirement.model_copy(update={"satisfied_by_compiler": True}),
        )
    tampered_packet = packet.model_copy(
        update={"downstream_requirements": requirements}
    )
    tampered_result = compilation_result.model_copy(
        update={"work_packet": tampered_packet}
    )
    with pytest.raises(WorkspaceAllocatorIntegrityError):
        build_workspace_allocation_authorization(
            authorizer_id="workspace.authorizer.p17-1",
            authorization_reference="AUTH-P17-1",
            rationale="Authorize synthetic workspace reservation.",
            compilation_result=tampered_result,
            repository_identity=repository_identity,
            workspace_root=WORKSPACE_ROOT,
        )


def test_read_only_git_command_policy(
    monkeypatch: pytest.MonkeyPatch, repository_identity
) -> None:
    calls = patch_inspection(monkeypatch)
    inspect_human_provisioned_workspace(
        workspace_root=WORKSPACE_ROOT,
        repository_identity=repository_identity,
    )
    assert tuple(calls) == READ_ONLY_COMMANDS


@pytest.mark.parametrize(
    "forbidden_args",
    (
        ("fetch",),
        ("pull",),
        ("clone",),
        ("checkout", "main"),
        ("switch", "main"),
        ("worktree", "add"),
        ("add", "."),
        ("commit", "-m", "x"),
        ("push",),
        ("merge", "main"),
        ("rebase", "main"),
        ("reset", "--hard"),
        ("clean", "-fd"),
        ("stash",),
        ("branch", "new"),
        ("tag", "v1"),
    ),
)
def test_forbidden_git_commands_are_rejected(forbidden_args: tuple[str, ...]) -> None:
    with pytest.raises(WorkspaceAllocatorInspectionError):
        allocator_module._run_git_command(WORKSPACE_ROOT, forbidden_args)


def test_git_subprocess_shape_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}

    class Completed:
        returncode = 0
        stdout = "true\n"

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return Completed()

    monkeypatch.setattr(allocator_module.subprocess, "run", fake_run)
    assert (
        allocator_module._run_git_command(
            WORKSPACE_ROOT,
            ("rev-parse", "--is-inside-work-tree"),
        )
        == "true"
    )
    assert captured["command"] == [
        "git",
        "--no-optional-locks",
        "-C",
        WORKSPACE_ROOT,
        "rev-parse",
        "--is-inside-work-tree",
    ]
    assert captured["kwargs"]["shell"] is False
    assert captured["kwargs"]["timeout"] == 5
    assert captured["kwargs"]["capture_output"] is True
    assert captured["kwargs"]["text"] is True
    assert captured["kwargs"]["encoding"] == "utf-8"


@pytest.mark.parametrize(
    ("path_metadata", "error"),
    (
        (metadata(exists=False), "exist"),
        (metadata(is_dir=False), "directory"),
        (metadata(is_symlink=True), "symlink"),
        (metadata(resolved_workspace_root="C:/other/root"), "canonical"),
    ),
)
def test_workspace_inspection_rejects_bad_metadata(
    monkeypatch: pytest.MonkeyPatch,
    repository_identity: WorkspaceRepositoryIdentity,
    path_metadata: allocator_module._WorkspacePathMetadata,
    error: str,
) -> None:
    patch_inspection(monkeypatch, path_metadata=path_metadata)
    with pytest.raises(WorkspaceAllocatorInspectionError, match=error):
        inspect_human_provisioned_workspace(
            workspace_root=WORKSPACE_ROOT,
            repository_identity=repository_identity,
        )


@pytest.mark.parametrize(
    ("responses", "error"),
    (
        (git_responses(top_level="C:/other/root"), "top level"),
        (git_responses(inside="false"), "inside"),
        (git_responses(commit=OTHER_COMMIT), "commit"),
        (git_responses(branch=OTHER_BRANCH), "branch"),
        (git_responses(branch=""), "named branch"),
        (git_responses(git_dir="C:/repo/.git", common_dir="C:/repo/.git"), "linked"),
        (git_responses(status=" M file.py"), "clean"),
        (git_responses(status="?? new.py"), "clean"),
    ),
)
def test_workspace_inspection_rejects_bad_git_evidence(
    monkeypatch: pytest.MonkeyPatch,
    repository_identity: WorkspaceRepositoryIdentity,
    responses: dict[tuple[str, ...], str],
    error: str,
) -> None:
    patch_inspection(monkeypatch, responses=responses)
    with pytest.raises(WorkspaceAllocatorInspectionError, match=error):
        inspect_human_provisioned_workspace(
            workspace_root=WORKSPACE_ROOT,
            repository_identity=repository_identity,
        )


def test_primary_checkout_rejection_exact_output(
    monkeypatch: pytest.MonkeyPatch,
    repository_identity: WorkspaceRepositoryIdentity,
) -> None:
    patch_inspection(
        monkeypatch,
        responses=git_responses(git_dir="C:/repo/.git", common_dir="C:/repo/.git"),
    )
    with pytest.raises(WorkspaceAllocatorInspectionError) as exc:
        inspect_human_provisioned_workspace(
            workspace_root=WORKSPACE_ROOT,
            repository_identity=repository_identity,
        )
    assert (
        f"{type(exc.value).__name__} {exc.value}"
        == "WorkspaceAllocatorInspectionError workspace must be a human-provisioned linked Git worktree"
    )


def test_workspace_inspection_evidence_digest_recomputes(
    inspection_evidence: WorkspaceInspectionEvidence,
) -> None:
    assert inspection_evidence.inside_work_tree is True
    assert inspection_evidence.linked_worktree is True
    assert inspection_evidence.clean is True
    assert inspection_evidence.status_entry_count == 0
    assert (
        inspection_evidence.inspection_SHA256
        == allocator_module._inspection_evidence_digest(inspection_evidence)
    )


def test_scope_projection_is_exact(allocation: WorkspaceAllocation) -> None:
    projection = allocation.scope_projection
    source_scope = build_bundle()["result"].work_packet.repository_scope
    assert projection.allowed_paths == source_scope.allowed_paths
    assert projection.forbidden_paths == source_scope.forbidden_paths
    assert projection.allowed_actions == source_scope.allowed_actions
    assert projection.forbidden_actions == source_scope.forbidden_actions
    assert projection.scope_enforcement_ready is False
    assert projection.projection_SHA256 == allocator_module._scope_projection_digest(
        projection
    )


def test_empty_registry_is_deterministic_and_immutable() -> None:
    first = get_empty_workspace_allocation_registry()
    second = get_empty_workspace_allocation_registry()
    assert first == second
    assert first.revision == 0
    assert first.reservations == ()
    assert first.registry_SHA256 == allocator_module._registry_digest(first)
    with pytest.raises(ValidationError):
        first.revision = 1


def test_valid_registry_passes(allocation: WorkspaceAllocation) -> None:
    registry = make_registry((make_reservation(allocation),))
    validate_workspace_allocation_registry(registry)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    (
        ("allocation_id", None, "duplicate allocation"),
        ("work_packet_id", None, "duplicate WorkPacket"),
        ("workspace_root", None, "duplicate workspace root"),
        ("resolved_workspace_root", None, "duplicate resolved"),
        ("workspace_branch", None, "duplicate workspace branch"),
        ("resolved_workspace_root", CHILD_ROOT, "workspace root overlap"),
        ("resolved_workspace_root", WORKSPACE_ROOT.casefold(), "duplicate resolved"),
    ),
)
def test_registry_rejects_collisions(
    allocation: WorkspaceAllocation,
    field: str,
    value: str | None,
    error: str,
) -> None:
    first = make_reservation(allocation)
    overrides = {
        "allocation_id": "WS-P17-0-R0001-111111111111",
        "work_packet_id": "WP-P17-0-R0001-111111111111",
        "workspace_root": OTHER_ROOT,
        "resolved_workspace_root": OTHER_ROOT,
        "workspace_branch": OTHER_BRANCH,
    }
    if value is None:
        overrides[field] = getattr(first, field)
    else:
        overrides[field] = value
    second = make_reservation(allocation, **overrides)
    with pytest.raises(
        (ValidationError, WorkspaceAllocatorCollisionError), match=error
    ):
        validate_workspace_allocation_registry(make_registry((first, second)))


def test_registry_allows_same_source_commit_for_different_worktrees(
    allocation: WorkspaceAllocation,
) -> None:
    first = make_reservation(allocation)
    second = make_reservation(
        allocation,
        allocation_id="WS-P17-0-R0001-111111111111",
        work_packet_id="WP-P17-0-R0001-111111111111",
        workspace_root=OTHER_ROOT,
        resolved_workspace_root=OTHER_ROOT,
        workspace_branch=OTHER_BRANCH,
        source_commit=SOURCE_COMMIT,
    )
    validate_workspace_allocation_registry(make_registry((first, second)))


def test_registry_rejects_noncanonical_order(allocation: WorkspaceAllocation) -> None:
    first = make_reservation(allocation, allocation_id="WS-P17-0-R0001-222222222222")
    second = make_reservation(
        allocation,
        allocation_id="WS-P17-0-R0001-111111111111",
        work_packet_id="WP-P17-0-R0001-111111111111",
        workspace_root=OTHER_ROOT,
        resolved_workspace_root=OTHER_ROOT,
        workspace_branch=OTHER_BRANCH,
    )
    data = {
        "schema_version": WORKSPACE_ALLOCATION_SCHEMA_VERSION,
        "policy_id": WORKSPACE_ALLOCATION_POLICY_ID,
        "revision": 1,
        "reservations": (first, second),
    }
    with pytest.raises(ValidationError):
        WorkspaceAllocationRegistry(
            **data,
            registry_SHA256=allocator_module._registry_digest_from_record(data),
        )


def test_registry_tamper_fails(allocation: WorkspaceAllocation) -> None:
    registry = make_registry((make_reservation(allocation),))
    tampered = registry.model_copy(update={"registry_SHA256": "0" * 64})
    with pytest.raises(WorkspaceAllocatorIntegrityError):
        validate_workspace_allocation_registry(tampered)


@pytest.mark.parametrize(
    "tamper",
    (
        "policy_id",
        "authorization_work_packet",
        "authorization_repository",
        "authorization_root",
        "authorization_digest",
        "registry_digest",
        "require_clean_worktree",
        "require_linked_worktree",
    ),
)
def test_allocation_request_rejects_invalid_bindings(
    allocation_request: WorkspaceAllocationRequest,
    tamper: str,
) -> None:
    data = allocation_request.model_dump(mode="json")
    if tamper == "policy_id":
        data["policy_id"] = "other"
        assert_validation_fails(lambda: WorkspaceAllocationRequest(**data))
        return
    if tamper == "require_clean_worktree":
        data["require_clean_worktree"] = False
        assert_validation_fails(lambda: WorkspaceAllocationRequest(**data))
        return
    if tamper == "require_linked_worktree":
        data["require_linked_worktree"] = False
        assert_validation_fails(lambda: WorkspaceAllocationRequest(**data))
        return
    if tamper == "authorization_work_packet":
        data["allocation_authorization"]["work_packet_id"] = (
            "WP-P17-0-R0001-111111111111"
        )
    if tamper == "authorization_repository":
        data["allocation_authorization"]["repository_identity_SHA256"] = "1" * 64
    if tamper == "authorization_root":
        data["allocation_authorization"]["workspace_root"] = OTHER_ROOT
    if tamper == "authorization_digest":
        data["allocation_authorization"]["authorization_SHA256"] = "0" * 64
    if tamper == "registry_digest":
        data["registry"]["registry_SHA256"] = "0" * 64
    assert_validation_fails(lambda: WorkspaceAllocationRequest(**data))


def test_allocation_request_is_immutable(
    allocation_request: WorkspaceAllocationRequest,
) -> None:
    with pytest.raises(ValidationError):
        WorkspaceAllocationRequest(**{
            **allocation_request.model_dump(mode="json"),
            "unknown": "field",
        })


def test_allocation_pipeline_success_and_determinism(
    monkeypatch: pytest.MonkeyPatch,
    allocation_request: WorkspaceAllocationRequest,
) -> None:
    request_before = allocation_request.model_dump(mode="json")
    patch_inspection(monkeypatch)
    first = allocate_workspace(allocation_request)
    patch_inspection(monkeypatch)
    second = allocate_workspace(allocation_request)
    allocation = first.allocation
    assert first == second
    assert allocation_request.model_dump(mode="json") == request_before
    assert allocation.disposition is WorkspaceAllocationDisposition.ALLOCATED
    assert allocation.lifecycle_state is WorkspaceLifecycleState.ALLOCATED
    assert allocation.isolation_level is WorkspaceIsolationLevel.DEDICATED
    assert allocation.exclusive is True
    assert allocation.workspace_requirement_satisfied is True
    assert allocation.execution_ready is False
    assert allocation.tool_permissions_ready is False
    assert allocation.cleanup_eligibility is WorkspaceCleanupEligibility.NOT_ELIGIBLE
    assert allocation.allocation_id.endswith(allocation.allocation_input_SHA256[:12])
    assert allocation.allocation_SHA256 == allocator_module._allocation_digest(
        allocation
    )
    assert first.result_SHA256 == allocator_module._allocation_result_digest(first)
    assert first.updated_registry.revision == 1
    assert len(first.updated_registry.reservations) == 1


@pytest.mark.parametrize(
    ("collision", "error"),
    (
        ("work_packet", "duplicate WorkPacket"),
        ("workspace_root", "workspace root collision"),
        ("resolved_root", "resolved workspace root collision"),
        ("ancestor", "workspace root collision"),
        ("descendant", "workspace root collision"),
        ("branch", "workspace branch collision"),
    ),
)
def test_allocation_pipeline_rejects_collisions(
    monkeypatch: pytest.MonkeyPatch,
    allocation_request: WorkspaceAllocationRequest,
    allocation: WorkspaceAllocation,
    collision: str,
    error: str,
) -> None:
    kwargs = {
        "allocation_id": "WS-P17-0-R0001-111111111111",
        "work_packet_id": "WP-P17-0-R0001-111111111111",
        "workspace_root": OTHER_ROOT,
        "resolved_workspace_root": OTHER_ROOT,
        "workspace_branch": OTHER_BRANCH,
    }
    if collision == "work_packet":
        kwargs["work_packet_id"] = allocation.work_packet_id
    if collision == "workspace_root":
        kwargs["workspace_root"] = WORKSPACE_ROOT
    if collision == "resolved_root":
        kwargs["resolved_workspace_root"] = WORKSPACE_ROOT
    if collision == "ancestor":
        kwargs["workspace_root"] = "C:/worktrees"
        kwargs["resolved_workspace_root"] = "C:/worktrees"
    if collision == "descendant":
        kwargs["workspace_root"] = CHILD_ROOT
        kwargs["resolved_workspace_root"] = CHILD_ROOT
    if collision == "branch":
        kwargs["workspace_branch"] = WORKSPACE_BRANCH
    registry = make_registry((make_reservation(allocation, **kwargs),))
    request = allocation_request.model_copy(update={"registry": registry})
    patch_inspection(monkeypatch)
    with pytest.raises(WorkspaceAllocatorCollisionError, match=error):
        allocate_workspace(request)


@pytest.mark.parametrize(
    "field",
    (
        "schema_version",
        "policy_id",
        "disposition",
        "lifecycle_state",
        "isolation_level",
        "exclusive",
        "workspace_requirement_satisfied",
        "execution_ready",
        "tool_permissions_ready",
        "git_authority",
        "workspace_root",
        "source_commit",
        "workspace_branch",
        "inspection_SHA256",
        "projection_SHA256",
        "allocation_input_SHA256",
        "allocation_SHA256",
    ),
)
def test_allocation_validation_rejects_tampering(
    allocation: WorkspaceAllocation,
    field: str,
) -> None:
    update = {}
    if field == "schema_version":
        update["schema_version"] = 2
    elif field == "policy_id":
        update["policy_id"] = "other"
    elif field == "disposition":
        update["disposition"] = "other"
    elif field == "lifecycle_state":
        update["lifecycle_state"] = "other"
    elif field == "isolation_level":
        update["isolation_level"] = "shared"
    elif field == "exclusive":
        update["exclusive"] = False
    elif field == "workspace_requirement_satisfied":
        update["workspace_requirement_satisfied"] = False
    elif field == "execution_ready":
        update["execution_ready"] = True
    elif field == "tool_permissions_ready":
        update["tool_permissions_ready"] = True
    elif field == "git_authority":
        update["git_authority"] = "system"
    elif field == "workspace_root":
        update["workspace_root"] = OTHER_ROOT
    elif field in {"source_commit", "workspace_branch", "inspection_SHA256"}:
        evidence = allocation.inspection_evidence.model_copy(
            update={
                "source_commit": OTHER_COMMIT
                if field == "source_commit"
                else allocation.inspection_evidence.source_commit,
                "workspace_branch": OTHER_BRANCH
                if field == "workspace_branch"
                else allocation.inspection_evidence.workspace_branch,
                "inspection_SHA256": "0" * 64
                if field == "inspection_SHA256"
                else allocation.inspection_evidence.inspection_SHA256,
            }
        )
        update["inspection_evidence"] = evidence
    elif field == "projection_SHA256":
        update["scope_projection"] = allocation.scope_projection.model_copy(
            update={"projection_SHA256": "0" * 64}
        )
    elif field == "allocation_input_SHA256":
        update["allocation_input_SHA256"] = "0" * 64
    elif field == "allocation_SHA256":
        update["allocation_SHA256"] = "0" * 64
    with pytest.raises(WorkspaceAllocatorIntegrityError):
        validate_workspace_allocation(allocation.model_copy(update=update))


def test_valid_allocation_validates(allocation: WorkspaceAllocation) -> None:
    validate_workspace_allocation(allocation)


@pytest.mark.parametrize(
    ("execution_active", "unreviewed_changes", "artifacts", "handoff", "eligible"),
    (
        (True, False, True, True, WorkspaceCleanupEligibility.NOT_ELIGIBLE),
        (False, True, True, True, WorkspaceCleanupEligibility.NOT_ELIGIBLE),
        (False, False, False, True, WorkspaceCleanupEligibility.NOT_ELIGIBLE),
        (False, False, True, False, WorkspaceCleanupEligibility.NOT_ELIGIBLE),
        (False, False, True, True, WorkspaceCleanupEligibility.ELIGIBLE),
    ),
)
def test_cleanup_assessment_cases(
    allocation: WorkspaceAllocation,
    execution_active: bool,
    unreviewed_changes: bool,
    artifacts: bool,
    handoff: bool,
    eligible: WorkspaceCleanupEligibility,
) -> None:
    before = allocation.model_dump(mode="json")
    assessment = assess_workspace_cleanup_eligibility(
        allocation=allocation,
        execution_active=execution_active,
        unreviewed_changes_present=unreviewed_changes,
        artifacts_preserved=artifacts,
        human_git_handoff_complete=handoff,
    )
    assert assessment.eligibility is eligible
    assert assessment.assessment_SHA256 == allocator_module._cleanup_assessment_digest(
        assessment
    )
    assert allocation.model_dump(mode="json") == before


def test_newly_allocated_workspace_cleanup_not_eligible_by_default(
    allocation: WorkspaceAllocation,
) -> None:
    assert allocation.cleanup_eligibility is WorkspaceCleanupEligibility.NOT_ELIGIBLE


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_json_round_trip(
    model: type[BaseModel], allocation_result: WorkspaceAllocationResult
) -> None:
    sample = sample_for_model(model, allocation_result)
    round_tripped = model.model_validate_json(sample.model_dump_json())
    assert round_tripped == sample
    for value in round_tripped.model_dump().values():
        assert not isinstance(value, list)


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_model_schema_generation_is_deterministic(
    model: type[BaseModel],
) -> None:
    first = model.model_json_schema()
    second = model.model_json_schema()
    assert first == second
    assert first.get("additionalProperties") is False
    assert "properties" in first


@pytest.mark.parametrize(
    "forbidden_name",
    (
        "create_git_worktree",
        "create_workspace_directory",
        "copy_workspace_files",
        "delete_workspace",
        "persist_workspace_registry",
        "ToolPermissionProfileExecutor",
        "ProviderSelector",
        "ModelSelector",
        "AgentAllocator",
        "WorkerAllocator",
        "execute_work_packet",
        "run_validation_command",
        "review_diff",
        "review_artifact",
        "create_git_handoff",
    ),
)
def test_forbidden_public_authority_shapes_are_absent(forbidden_name: str) -> None:
    assert not hasattr(work_packet, forbidden_name)
    assert forbidden_name not in work_packet.__all__


def test_no_global_mutable_registry_is_exposed() -> None:
    assert not hasattr(allocator_module, "workspace_allocation_registry")
    assert not hasattr(allocator_module, "ACTIVE_ALLOCATIONS")
    assert (
        get_empty_workspace_allocation_registry()
        is not get_empty_workspace_allocation_registry()
    )


def test_p17_0_shadow_rejection_still_exact() -> None:
    from hermes_cli.agent_platform.ticket_factory import run_ticket_factory_shadow_pilot

    report = run_ticket_factory_shadow_pilot()
    with pytest.raises(WorkPacketCompilerAuthorizationError) as exc:
        build_work_packet_compilation_authorization(
            authorizer_id="authorizer.p17-0",
            authorization_reference="AUTH-P17-0",
            rationale="Synthetic authorization.",
            approval_record=report.approval_record,
            publication_result=report.publication_result,
        )
    assert (
        f"{type(exc.value).__name__} {exc.value}"
        == "WorkPacketCompilerAuthorizationError shadow-only approval evidence cannot authorize WorkPacket compilation"
    )


def sample_for_model(
    model: type[BaseModel], result: WorkspaceAllocationResult
) -> BaseModel:
    samples = {
        WorkspaceRepositoryIdentity: result.allocation.repository_identity,
        WorkspaceAllocationAuthorization: build_workspace_allocation_authorization(
            authorizer_id="workspace.authorizer.p17-1",
            authorization_reference="AUTH-P17-1",
            rationale="Authorize synthetic human-provisioned workspace reservation.",
            compilation_result=build_bundle()["result"],
            repository_identity=result.allocation.repository_identity,
            workspace_root=WORKSPACE_ROOT,
        ),
        WorkspaceInspectionEvidence: result.allocation.inspection_evidence,
        WorkspaceScopeProjection: result.allocation.scope_projection,
        WorkspaceReservation: result.updated_registry.reservations[0],
        WorkspaceAllocationRegistry: result.updated_registry,
        WorkspaceAllocationRequest: WorkspaceAllocationRequest(
            compilation_result=build_bundle()["result"],
            repository_identity=result.allocation.repository_identity,
            allocation_authorization=build_workspace_allocation_authorization(
                authorizer_id="workspace.authorizer.p17-1",
                authorization_reference="AUTH-P17-1",
                rationale="Authorize synthetic human-provisioned workspace reservation.",
                compilation_result=build_bundle()["result"],
                repository_identity=result.allocation.repository_identity,
                workspace_root=WORKSPACE_ROOT,
            ),
            registry=get_empty_workspace_allocation_registry(),
        ),
        WorkspaceAllocation: result.allocation,
        WorkspaceAllocationResult: result,
        WorkspaceCleanupAssessment: assess_workspace_cleanup_eligibility(
            allocation=result.allocation,
            execution_active=False,
            unreviewed_changes_present=False,
            artifacts_preserved=True,
            human_git_handoff_complete=True,
        ),
    }
    return samples[model]
