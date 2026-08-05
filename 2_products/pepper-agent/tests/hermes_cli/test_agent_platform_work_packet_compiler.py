import hashlib
import importlib
import json
from enum import Enum
from typing import get_args, get_origin

import pytest
from pydantic import ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.compiler as compiler_module
from hermes_cli.agent_platform.ticket_factory import (
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPriority,
    ContextSensitivity,
    ContextSourceKind,
    ContextSourceSpec,
    DependencyKind,
    DependencyScope,
    FreshDependencyPlanningEvidence,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    ParallelizationHint,
    ProjectSpec,
    RepositoryScopeSpec,
    ReviewedTicketProposal,
    TicketApprovalRecord,
    TicketApprovalRequest,
    TicketApprovalState,
    TicketDependencySpec,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketLintDisposition,
    TicketLintRequest,
    TicketPlanningRequest,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    TicketPublicationResult,
    TicketPublicationState,
    TicketResponseContractSpec,
    TicketSpec,
    TicketSynthesisRequest,
    TicketType,
    TicketValidationStepSpec,
    WaveDisposition,
    assemble_context_pack,
    build_ticket_approval_record,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    build_ticket_synthesis_review,
    lint_ticket_collection,
    prepare_ticket_generator_assignments,
    publish_canonical_ticket,
    run_ticket_factory_shadow_pilot,
)
from hermes_cli.agent_platform.work_packet import (
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
    build_work_packet_compilation_authorization,
    compile_ticket_spec_to_work_packet,
    validate_work_packet,
)


EXPECTED_EXPORTS = (
    "WORK_PACKET_SCHEMA_VERSION",
    "WORK_PACKET_COMPILER_SCHEMA_VERSION",
    "WORK_PACKET_COMPILER_POLICY_ID",
    "WorkPacketExecutionMode",
    "WorkPacketValidationKind",
    "WorkPacketDownstreamCapability",
    "WorkPacketGitAuthority",
    "WorkPacketAuthorityBoundary",
    "WorkPacketCompilationDisposition",
    "WorkPacketCompilationAuthorization",
    "WorkPacketRepositoryScope",
    "WorkPacketTaskStep",
    "WorkPacketValidationStep",
    "WorkPacketDownstreamRequirement",
    "WorkPacketCompilationRequest",
    "WorkPacketCompilationEvidence",
    "WorkPacket",
    "WorkPacketCompilationResult",
    "WorkPacketCompilerError",
    "WorkPacketCompilerInputError",
    "WorkPacketCompilerAuthorizationError",
    "WorkPacketCompilerIntegrityError",
    "build_work_packet_compilation_authorization",
    "validate_work_packet",
    "compile_ticket_spec_to_work_packet",
)
PUBLIC_MODELS = (
    WorkPacketCompilationAuthorization,
    WorkPacketRepositoryScope,
    WorkPacketTaskStep,
    WorkPacketValidationStep,
    WorkPacketDownstreamRequirement,
    WorkPacketCompilationRequest,
    WorkPacketCompilationEvidence,
    WorkPacket,
    WorkPacketCompilationResult,
)
REQUIRED_RESPONSE_SECTIONS = (
    "Summary",
    "Files inspected",
    "Files modified",
    "Tests/commands run",
    "Decisions made",
    "Limitations",
)
REQUIRED_FORBIDDEN_ACTIONS = (
    "git add",
    "git commit",
    "git push",
    "git reset",
    "git clean",
    "git stash",
    "git worktree",
    "Graphify",
)
CANONICAL_REQUIREMENTS = (
    (WorkPacketDownstreamCapability.WORKSPACE_ALLOCATION, "P17.1"),
    (WorkPacketDownstreamCapability.TOOL_PERMISSION_PROFILE, "P17.2"),
    (WorkPacketDownstreamCapability.SINGLE_AGENT_EXECUTION, "P17.3"),
    (WorkPacketDownstreamCapability.VALIDATION_COMMAND_RUNNER, "P17.4"),
    (WorkPacketDownstreamCapability.RESULT_FAILURE_CANCELLATION_ENVELOPES, "P17.5"),
    (WorkPacketDownstreamCapability.DIFF_ARTIFACT_REVIEW, "P17.6"),
    (WorkPacketDownstreamCapability.HUMAN_GIT_HANDOFF, "P17.7"),
)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def scope(
    *,
    allowed_paths: tuple[str, ...] = (
        "2_products/pepper-agent/hermes_cli/agent_platform/work_packet/**",
    ),
    forbidden_paths: tuple[str, ...] = ("4_external/sources/**",),
    allowed_actions: tuple[str, ...] = ("edit compile-only WorkPacket contracts",),
    forbidden_actions: tuple[str, ...] = REQUIRED_FORBIDDEN_ACTIONS,
) -> RepositoryScopeSpec:
    return RepositoryScopeSpec(
        allowed_paths=allowed_paths,
        forbidden_paths=forbidden_paths,
        allowed_actions=allowed_actions,
        forbidden_actions=forbidden_actions,
    )


def authority() -> AuthorityReferenceSpec:
    return AuthorityReferenceSpec(
        kind=AuthorityReferenceKind.GOVERNANCE_RECORD,
        value="0_architecture/governance/synthetic_p17_0.md",
        rationale="Synthetic P17.0 authority reference.",
    )


def response_contract() -> TicketResponseContractSpec:
    return TicketResponseContractSpec(
        required_sections=REQUIRED_RESPONSE_SECTIONS,
        completion_verdict="synthetic_p17_0_ready",
    )


def validation_step(
    validation_id: str = "V1",
    *,
    command: str | None = "python -m pytest synthetic_work_packet_tests.py",
    required: bool = True,
) -> TicketValidationStepSpec:
    return TicketValidationStepSpec(
        validation_id=validation_id,
        description=f"Run synthetic validation {validation_id}.",
        command=command,
        expected_result=f"Synthetic validation {validation_id} passes.",
        required=required,
    )


def project() -> ProjectSpec:
    return ProjectSpec(
        project_id="P17",
        title="Synthetic P17 project",
        objective="Compile approved tickets into WorkPacket candidates.",
        summary="Synthetic project for P17.0 compiler tests.",
        context=("Synthetic context for compile-only WorkPacket generation.",),
        authority_references=(authority(),),
        scope=scope(),
        constraints=("No runtime execution is authorized.",),
        non_goals=("No workspace allocation is authorized.",),
        acceptance_criteria=("The compiler result is deterministic.",),
        completion_verdict="synthetic_p17_project_ready",
    )


def dependency(
    ticket_id: str,
    *,
    kind: DependencyKind = DependencyKind.SOFT_PREDECESSOR,
    dep_scope: DependencyScope = DependencyScope.EXTERNAL_PROJECT,
) -> TicketDependencySpec:
    return TicketDependencySpec(
        ticket_id=ticket_id,
        kind=kind,
        scope=dep_scope,
        rationale="Synthetic dependency declaration.",
    )


def ticket(
    *,
    ticket_id: str = "P17.0",
    ticket_scope: RepositoryScopeSpec | None = None,
    tasks: tuple[str, ...] = (
        "Define compile-only WorkPacket models.",
        "Compile task and validation steps without execution.",
    ),
    validation_steps: tuple[TicketValidationStepSpec, ...] = (validation_step(),),
    deps: tuple[TicketDependencySpec, ...] = (),
) -> TicketSpec:
    return TicketSpec(
        project_id="P17",
        ticket_id=ticket_id,
        title="Synthetic TicketSpec to WorkPacket compiler",
        ticket_type=TicketType.IMPLEMENTATION,
        objective="Compile approved TicketSpec evidence into a WorkPacket candidate.",
        context=("Synthetic ticket context for compile-only behavior.",),
        authority_references=(authority(),),
        dependencies=deps,
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=ticket_scope or scope(),
        constraints=("Rollback by removing only P17.0 files.",),
        tasks=tasks,
        acceptance_criteria=("The WorkPacket candidate is deterministic.",),
        validation_steps=validation_steps,
        response_contract=response_contract(),
        recommended_commit_message="P17.0 Add TicketSpec to WorkPacket compiler",
    )


def context_source() -> ContextSourceSpec:
    return ContextSourceSpec(
        source_id="CTX-P17-0",
        kind=ContextSourceKind.GOVERNANCE_RECORD,
        title="Synthetic P17.0 source",
        source_reference="governance:synthetic-p17-0",
        content="Synthetic bounded context for WorkPacket compiler tests.",
        authority_references=(),
        sensitivity=ContextSensitivity.INTERNAL,
        priority=ContextPriority.NORMAL,
        required=False,
    )


def build_bundle(
    *,
    source_ticket: TicketSpec | None = None,
    risk_acknowledgement: str | None = None,
    reviewer_id: str = "reviewer.p17-0",
    compile_result: bool = True,
) -> dict[str, object]:
    project_spec = project()
    seed_ticket = source_ticket or ticket()
    pack = assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=project_spec,
            ticket_spec=seed_ticket,
            sources=(context_source(),),
            policy=ContextAssemblyPolicy(),
        )
    )
    generation_request = TicketGenerationRequest(
        project_spec=project_spec,
        ticket_spec=seed_ticket,
        context_pack=pack,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    reviewed = tuple(
        ReviewedTicketProposal(
            proposal=build_ticket_proposal(
                assignment=assignment,
                proposed_ticket=seed_ticket,
                rationale="Synthetic proposal rationale for P17.0.",
                evidence_source_ids=("CTX-P17-0",),
            ),
            lint_report=lint_ticket_collection(
                TicketLintRequest(
                    project_spec=project_spec,
                    tickets=(seed_ticket,),
                    dependency_plan=None,
                    collection_complete=False,
                )
            ),
        )
        for assignment in assignments
    )
    planning_request = TicketPlanningRequest(
        project_spec=project_spec,
        tickets=(seed_ticket,),
    )
    dependency_plan = build_ticket_dependency_plan(planning_request)
    synthesis_review = build_ticket_synthesis_review(
        TicketSynthesisRequest(
            generation_request=generation_request,
            assignments=assignments,
            reviewed_proposals=reviewed,
            dependency_plan=dependency_plan,
        )
    )
    planning_evidence = FreshDependencyPlanningEvidence(
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        evidence_reference="PLANNING-P17-0",
        rationale="Synthetic fresh planning evidence.",
    )
    approval = build_ticket_approval_record(
        TicketApprovalRequest(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            synthesis_review=synthesis_review,
            decision=HumanApprovalDecision.APPROVE,
            approval_evidence=HumanApprovalEvidence(
                reviewer_id=reviewer_id,
                decision_reference="APPROVAL-P17-0",
                rationale="Synthetic approval rationale.",
                planning_warning_acknowledgement="Synthetic planning warning acknowledged.",
            ),
            fresh_planning_evidence=planning_evidence,
        )
    )
    publication = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approval,
            publication_evidence=TicketPublicationEvidence(
                publisher_id="publisher.p17-0",
                publication_reference="PUBLICATION-P17-0",
                rationale="Synthetic publication rationale.",
            ),
        )
    )
    authorization = build_work_packet_compilation_authorization(
        authorizer_id="authorizer.p17-0",
        authorization_reference="COMPILE-AUTH-P17-0",
        rationale="Synthetic human compilation authorization.",
        approval_record=approval,
        publication_result=publication,
        risk_acknowledgement=risk_acknowledgement,
    )
    request = WorkPacketCompilationRequest(
        project_spec=project_spec,
        approval_record=approval,
        publication_result=publication,
        compilation_authorization=authorization,
    )
    result = compile_ticket_spec_to_work_packet(request) if compile_result else None
    return {
        "project": project_spec,
        "ticket": seed_ticket,
        "approval": approval,
        "publication": publication,
        "authorization": authorization,
        "request": request,
        "result": result,
    }


@pytest.fixture(scope="module")
def bundle() -> dict[str, object]:
    return build_bundle()


@pytest.fixture(scope="module")
def result(bundle: dict[str, object]) -> WorkPacketCompilationResult:
    return bundle["result"]


def assert_validation_fails(factory) -> None:
    with pytest.raises(ValidationError):
        factory()


def test_import_smoke_exact_output() -> None:
    required = (
        "WorkPacket",
        "WorkPacketCompilationRequest",
        "WorkPacketCompilationResult",
        "WorkPacketCompilationAuthorization",
        "compile_ticket_spec_to_work_packet",
        "validate_work_packet",
    )
    assert (
        work_packet.__all__[: len(EXPECTED_EXPORTS)] == EXPECTED_EXPORTS,
        len(set(work_packet.__all__)) == len(work_packet.__all__),
        all(hasattr(work_packet, name) for name in required),
        hasattr(work_packet, "ToolPermissionProfile"),
        hasattr(work_packet, "execute_work_packet"),
    ) == (True, True, True, True, False)


@pytest.mark.parametrize("exported_name", EXPECTED_EXPORTS)
def test_each_public_export_is_present(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)


def test_public_export_order_and_private_helpers() -> None:
    assert work_packet.__all__[: len(EXPECTED_EXPORTS)] == EXPECTED_EXPORTS
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)


def test_function_import_smoke_exact_output() -> None:
    assert (
        build_work_packet_compilation_authorization.__name__,
        compile_ticket_spec_to_work_packet.__name__,
        validate_work_packet.__name__,
    ) == (
        "build_work_packet_compilation_authorization",
        "compile_ticket_spec_to_work_packet",
        "validate_work_packet",
    )


def test_module_reload_has_no_runtime_surface_side_effects() -> None:
    reloaded = importlib.reload(work_packet)
    assert reloaded.__all__[: len(EXPECTED_EXPORTS)] == EXPECTED_EXPORTS
    assert len(set(reloaded.__all__)) == len(reloaded.__all__)
    assert not hasattr(reloaded, "execute_work_packet")


def test_constants_are_canonical() -> None:
    assert WORK_PACKET_SCHEMA_VERSION == 1
    assert WORK_PACKET_COMPILER_SCHEMA_VERSION == 1
    assert WORK_PACKET_COMPILER_POLICY_ID == "pepper-work-packet-compiler-policy-v1"


@pytest.mark.parametrize(
    ("enum_class", "members"),
    (
        (WorkPacketExecutionMode, ("single_agent",)),
        (WorkPacketValidationKind, ("command", "manual")),
        (
            WorkPacketDownstreamCapability,
            (
                "workspace_allocation",
                "tool_permission_profile",
                "single_agent_execution",
                "validation_command_runner",
                "result_failure_cancellation_envelopes",
                "diff_artifact_review",
                "human_git_handoff",
            ),
        ),
        (WorkPacketGitAuthority, ("human_only",)),
        (WorkPacketAuthorityBoundary, ("compile_only",)),
        (WorkPacketCompilationDisposition, ("compiled",)),
    ),
)
def test_enum_members_are_exact(
    enum_class: type[Enum], members: tuple[str, ...]
) -> None:
    assert tuple(member.value for member in enum_class) == members
    assert len(enum_class) == len(enum_class.__members__)
    with pytest.raises(ValueError):
        enum_class("unsupported")


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_are_frozen_and_forbid_extra(model: type) -> None:
    assert model.model_config["frozen"] is True
    assert model.model_config["extra"] == "forbid"
    assert model.model_config["validate_default"] is True
    assert model.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_unknown_fields_are_rejected(model: type, bundle: dict[str, object]) -> None:
    sample_by_model = {
        WorkPacketCompilationAuthorization: bundle["authorization"],
        WorkPacketCompilationRequest: bundle["request"],
        WorkPacketCompilationResult: bundle["result"],
        WorkPacket: bundle["result"].work_packet,
        WorkPacketCompilationEvidence: bundle["result"].evidence,
        WorkPacketRepositoryScope: bundle["result"].work_packet.repository_scope,
        WorkPacketTaskStep: bundle["result"].work_packet.tasks[0],
        WorkPacketValidationStep: bundle["result"].work_packet.validation_steps[0],
        WorkPacketDownstreamRequirement: bundle[
            "result"
        ].work_packet.downstream_requirements[0],
    }
    data = sample_by_model[model].model_dump(mode="json")
    data["unexpected"] = "rejected"
    with pytest.raises(ValidationError):
        model.model_validate(data)


@pytest.mark.parametrize(
    ("model", "field"),
    (
        (WorkPacketCompilationAuthorization, "schema_version"),
        (WorkPacketCompilationRequest, "schema_version"),
        (WorkPacketCompilationRequest, "compiler_policy_id"),
        (WorkPacket, "schema_version"),
        (WorkPacket, "compiler_policy_id"),
        (WorkPacketCompilationResult, "schema_version"),
    ),
)
def test_alternative_schema_versions_and_policy_fail(
    model: type,
    field: str,
    bundle: dict[str, object],
) -> None:
    sample_by_model = {
        WorkPacketCompilationAuthorization: bundle["authorization"],
        WorkPacketCompilationRequest: bundle["request"],
        WorkPacket: bundle["result"].work_packet,
        WorkPacketCompilationResult: bundle["result"],
    }
    data = sample_by_model[model].model_dump(mode="json")
    data[field] = 2 if field == "schema_version" else "other-policy"
    with pytest.raises(ValidationError):
        model.model_validate(data)


def test_lists_normalize_to_tuples(bundle: dict[str, object]) -> None:
    data = bundle["result"].work_packet.model_dump(mode="json")
    data["tasks"] = list(data["tasks"])
    data["validation_steps"] = list(data["validation_steps"])
    packet = WorkPacket.model_validate(data)
    assert isinstance(packet.tasks, tuple)
    assert isinstance(packet.validation_steps, tuple)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("compilation_authorized", "true"),
        ("synthetic", "false"),
        ("required", "true"),
        ("satisfied_by_compiler", "false"),
        ("command_execution_authorized", "false"),
        ("execution_ready", "false"),
    ),
)
def test_strict_boolean_shapes_reject_strings(
    field: str,
    value: str,
    bundle: dict[str, object],
) -> None:
    target = {
        "compilation_authorized": bundle["authorization"],
        "synthetic": bundle["authorization"],
        "required": bundle["result"].work_packet.downstream_requirements[0],
        "satisfied_by_compiler": bundle["result"].work_packet.downstream_requirements[
            0
        ],
        "command_execution_authorized": bundle["result"].work_packet.validation_steps[
            0
        ],
        "execution_ready": bundle["result"].work_packet,
    }[field]
    data = target.model_dump(mode="json")
    data[field] = value
    with pytest.raises(ValidationError):
        type(target).model_validate(data)


def test_valid_authorization_builds_and_is_deterministic(
    bundle: dict[str, object],
) -> None:
    approval = bundle["approval"]
    publication = bundle["publication"]
    first = build_work_packet_compilation_authorization(
        authorizer_id="authorizer.p17-0",
        authorization_reference="COMPILE-AUTH-P17-0",
        rationale="Synthetic human compilation authorization.",
        approval_record=approval,
        publication_result=publication,
    )
    second = build_work_packet_compilation_authorization(
        authorizer_id="authorizer.p17-0",
        authorization_reference="COMPILE-AUTH-P17-0",
        rationale="Synthetic human compilation authorization.",
        approval_record=approval,
        publication_result=publication,
    )
    assert first == second == bundle["authorization"]


@pytest.mark.parametrize(
    "updates",
    (
        {"authorization_SHA256": "0" * 64},
        {"compilation_authorized": False},
        {"synthetic": True},
        {"execution_mode": "unsupported"},
        {"git_authority": "machine"},
        {"authorizer_id": "SHADOW-P17"},
    ),
)
def test_invalid_authorization_shapes_fail(
    updates: dict[str, object], bundle: dict[str, object]
) -> None:
    data = bundle["authorization"].model_dump(mode="json")
    data.update(updates)
    with pytest.raises(ValidationError):
        WorkPacketCompilationAuthorization.model_validate(data)


@pytest.mark.parametrize("ticket_id", ("P16.SP0", "P16.SP1"))
def test_pilot_only_ticket_authorization_fails(
    ticket_id: str, bundle: dict[str, object]
) -> None:
    data = bundle["authorization"].model_dump(mode="json")
    data["ticket_id"] = ticket_id
    data["authorization_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        WorkPacketCompilationAuthorization.model_validate(data)


def test_builder_rejects_shadow_authorizer(bundle: dict[str, object]) -> None:
    with pytest.raises(WorkPacketCompilerAuthorizationError) as exc:
        build_work_packet_compilation_authorization(
            authorizer_id="SHADOW-AUTHORIZER",
            authorization_reference="AUTH-P17-0",
            rationale="Synthetic authorization.",
            approval_record=bundle["approval"],
            publication_result=bundle["publication"],
        )
    assert (
        str(exc.value)
        == "shadow-only approval evidence cannot authorize WorkPacket compilation"
    )


def test_builder_rejects_shadow_reviewer() -> None:
    shadow = run_ticket_factory_shadow_pilot()
    with pytest.raises(WorkPacketCompilerAuthorizationError) as exc:
        build_work_packet_compilation_authorization(
            authorizer_id="authorizer.p17-0",
            authorization_reference="AUTH-P17-0",
            rationale="Synthetic authorization.",
            approval_record=shadow.approval_record,
            publication_result=shadow.publication_result,
        )
    assert (
        str(exc.value)
        == "shadow-only approval evidence cannot authorize WorkPacket compilation"
    )


def test_builder_does_not_mutate_inputs(bundle: dict[str, object]) -> None:
    approval = bundle["approval"]
    publication = bundle["publication"]
    before = (approval.model_dump_json(), publication.model_dump_json())
    build_work_packet_compilation_authorization(
        authorizer_id="authorizer.p17-0",
        authorization_reference="AUTH-P17-0",
        rationale="Synthetic authorization.",
        approval_record=approval,
        publication_result=publication,
    )
    assert before == (approval.model_dump_json(), publication.model_dump_json())


@pytest.mark.parametrize(
    "bad_path",
    (
        "/absolute/path",
        "C:/Users/example/repo",
        "dir\\file.py",
        "../escape.py",
        "*",
        "**",
        ".",
        "./**",
        ".git/**",
        ".opencode/**",
        "AGENTS.md",
        "graphify-out/**",
        "4_external/sources/**",
        "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
    ),
)
def test_repository_scope_rejects_unsafe_allowed_paths(
    bad_path: str, result: WorkPacketCompilationResult
) -> None:
    valid = result.work_packet.repository_scope
    data = valid.model_dump(mode="json")
    data["allowed_paths"] = (bad_path,)
    with pytest.raises(ValidationError):
        WorkPacketRepositoryScope.model_validate(data)


@pytest.mark.parametrize(
    "bad_action",
    (
        "git add file.py",
        "git commit -m synthetic",
        "git push origin main",
        "git merge feature",
        "git rebase main",
        "git reset --hard",
        "git clean -fd",
        "git stash",
        "git switch main",
        "git checkout main",
        "git branch new",
        "git tag v1",
        "git worktree add ../x",
        "force push",
    ),
)
def test_repository_scope_rejects_git_allowed_actions(
    bad_action: str, result: WorkPacketCompilationResult
) -> None:
    valid = result.work_packet.repository_scope
    data = valid.model_dump(mode="json")
    data["allowed_actions"] = (bad_action,)
    with pytest.raises(ValidationError):
        WorkPacketRepositoryScope.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ("allowed_paths", "forbidden_paths", "allowed_actions", "forbidden_actions"),
)
def test_repository_scope_rejects_duplicates(
    field: str, result: WorkPacketCompilationResult
) -> None:
    valid = result.work_packet.repository_scope
    data = valid.model_dump(mode="json")
    data[field] = (
        (data[field][0], data[field][0]) if data[field] else ("src/a.py", "src/a.py")
    )
    with pytest.raises(ValidationError):
        WorkPacketRepositoryScope.model_validate(data)


def test_repository_scope_preserves_source_order_and_digest(
    result: WorkPacketCompilationResult,
) -> None:
    source_scope = result.work_packet.source_ticket.scope
    compiled_scope = result.work_packet.repository_scope
    assert compiled_scope.allowed_paths == source_scope.allowed_paths
    assert compiled_scope.forbidden_paths == source_scope.forbidden_paths
    assert compiled_scope.allowed_actions == source_scope.allowed_actions
    assert compiled_scope.forbidden_actions == source_scope.forbidden_actions
    data = compiled_scope.model_dump(mode="json")
    data["scope_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        WorkPacketRepositoryScope.model_validate(data)


def test_task_compilation_preserves_order_text_and_digests(
    result: WorkPacketCompilationResult,
) -> None:
    packet = result.work_packet
    assert tuple(step.step_id for step in packet.tasks) == ("TASK-001", "TASK-002")
    assert tuple(step.ordinal for step in packet.tasks) == (1, 2)
    assert tuple(step.source_task_index for step in packet.tasks) == (0, 1)
    assert (
        tuple(step.instruction for step in packet.tasks) == packet.source_ticket.tasks
    )
    changed = packet.tasks[0].model_dump(mode="json")
    changed["instruction"] = "Changed synthetic task."
    with pytest.raises(ValidationError):
        WorkPacketTaskStep.model_validate(changed)


@pytest.mark.parametrize("task_count", (1, 2, 3, 4, 5))
def test_multiple_task_counts_compile_to_contiguous_ids(task_count: int) -> None:
    tasks = tuple(f"Synthetic task {index}." for index in range(1, task_count + 1))
    compiled = build_bundle(source_ticket=ticket(tasks=tasks))[
        "result"
    ].work_packet.tasks
    assert tuple(step.step_id for step in compiled) == tuple(
        f"TASK-{index:03d}" for index in range(1, task_count + 1)
    )


def test_validation_compilation_classifies_command_and_manual_steps() -> None:
    source = ticket(
        validation_steps=(
            validation_step("V1", command="python -m pytest synthetic_one.py"),
            validation_step("V2", command=None, required=False),
        )
    )
    steps = build_bundle(source_ticket=source)["result"].work_packet.validation_steps
    assert tuple(step.validation_id for step in steps) == ("V1", "V2")
    assert tuple(step.kind for step in steps) == (
        WorkPacketValidationKind.COMMAND,
        WorkPacketValidationKind.MANUAL,
    )
    assert steps[0].command == "python -m pytest synthetic_one.py"
    assert steps[1].command is None
    assert all(step.command_execution_authorized is False for step in steps)


@pytest.mark.parametrize(
    "field", ("description", "command", "expected_result", "required")
)
def test_validation_step_preserves_source_fields(field: str) -> None:
    source_step = validation_step("V1", command="echo $SYNTHETIC_VALUE", required=True)
    compiled = build_bundle(source_ticket=ticket(validation_steps=(source_step,)))[
        "result"
    ].work_packet.validation_steps[0]
    assert getattr(compiled, field) == getattr(source_step, field)


def test_validation_step_digest_and_command_execution_tampering_fail(
    result: WorkPacketCompilationResult,
) -> None:
    step = result.work_packet.validation_steps[0]
    for update in ({"step_SHA256": "0" * 64}, {"command_execution_authorized": True}):
        data = step.model_dump(mode="json")
        data.update(update)
        with pytest.raises(ValidationError):
            WorkPacketValidationStep.model_validate(data)


def test_downstream_requirements_are_exact(result: WorkPacketCompilationResult) -> None:
    requirements = result.work_packet.downstream_requirements
    assert tuple((item.capability, item.owner_ticket) for item in requirements) == (
        CANONICAL_REQUIREMENTS
    )
    assert all(item.required is True for item in requirements)
    assert all(item.satisfied_by_compiler is False for item in requirements)


@pytest.mark.parametrize(("capability", "owner"), CANONICAL_REQUIREMENTS)
def test_each_downstream_requirement_owner(
    capability: WorkPacketDownstreamCapability,
    owner: str,
    result: WorkPacketCompilationResult,
) -> None:
    requirement = next(
        item
        for item in result.work_packet.downstream_requirements
        if item.capability is capability
    )
    assert requirement.owner_ticket == owner


@pytest.mark.parametrize(
    "update",
    (
        {"project_spec": project().model_copy(update={"project_id": "P18"})},
        {"approval_record": None},
        {"publication_result": None},
        {"compilation_authorization": None},
    ),
)
def test_request_rejects_structural_mismatches(
    update: dict[str, object], bundle: dict[str, object]
) -> None:
    data = bundle["request"].model_dump(mode="json")
    for key, value in update.items():
        data[key] = None if value is None else value.model_dump(mode="json")
    with pytest.raises(ValidationError):
        WorkPacketCompilationRequest.model_validate(data)


@pytest.mark.parametrize(
    "field",
    (
        "project_id",
        "ticket_id",
        "publication_id",
        "publication_revision",
        "approval_SHA256",
        "canonical_ticket_SHA256",
        "publication_artifact_SHA256",
    ),
)
def test_request_rejects_authorization_binding_mismatches(
    field: str, bundle: dict[str, object]
) -> None:
    request = bundle["request"]
    auth_data = request.compilation_authorization.model_dump(mode="json")
    auth_data[field] = 2 if field == "publication_revision" else "0" * 64
    if field in {"project_id", "ticket_id"}:
        auth_data[field] = "P18" if field == "project_id" else "P17.1"
    if field == "publication_id":
        auth_data[field] = "PUB-P17-1-0001"
    auth_data["authorization_SHA256"] = "0" * 64
    tampered = request.model_dump(mode="json")
    tampered["compilation_authorization"] = auth_data
    with pytest.raises(ValidationError):
        WorkPacketCompilationRequest.model_validate(tampered)


def test_fresh_lint_passes_with_one_ticket_and_collection_incomplete(
    result: WorkPacketCompilationResult,
) -> None:
    assert result.fresh_lint_report.disposition is TicketLintDisposition.PASS
    assert result.fresh_lint_report.summary.ticket_count == 1
    assert result.fresh_lint_report.ticket_ids == (result.work_packet.ticket_id,)


def test_pass_with_warnings_requires_compilation_risk_acknowledgement() -> None:
    warning_ticket = ticket(
        deps=(
            dependency(
                "P99.1",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        )
    )
    bundle_without_ack = build_bundle(
        source_ticket=warning_ticket, compile_result=False
    )
    with pytest.raises(WorkPacketCompilerAuthorizationError):
        compile_ticket_spec_to_work_packet(bundle_without_ack["request"])
    with_ack = build_bundle(
        source_ticket=warning_ticket,
        risk_acknowledgement="Synthetic compilation warning acknowledged.",
    )
    assert with_ack["result"].fresh_lint_report.disposition is (
        TicketLintDisposition.PASS_WITH_WARNINGS
    )


@pytest.mark.parametrize("disposition", (TicketLintDisposition.BLOCKED, "invalid"))
def test_blocked_or_invalid_lint_disposition_fails(
    disposition: object,
    bundle: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_data = bundle["result"].fresh_lint_report.model_dump()
    report_data["disposition"] = disposition
    report = bundle["result"].fresh_lint_report.model_construct(**report_data)
    monkeypatch.setattr(
        compiler_module, "lint_ticket_collection", lambda _request: report
    )
    with pytest.raises(WorkPacketCompilerInputError):
        compile_ticket_spec_to_work_packet(bundle["request"])


def test_dependency_plan_recomputes_and_target_wave_ready(
    result: WorkPacketCompilationResult,
) -> None:
    plan = result.dependency_plan
    packet = result.work_packet
    assert plan == build_ticket_dependency_plan(
        result.work_packet.model_validate(packet).project_spec
        and TicketPlanningRequest(
            project_spec=packet.project_spec, tickets=(packet.source_ticket,)
        )
    )
    assert packet.ticket_id in plan.ticket_ids
    assert packet.ticket_id not in plan.blocked_ticket_ids
    assert packet.ticket_id in plan.topological_order
    assert any(packet.ticket_id in wave.ticket_ids for wave in plan.waves)
    assert plan.waves[0].disposition is WaveDisposition.DEPENDENCY_READY


def test_missing_planning_evidence_fails(bundle: dict[str, object]) -> None:
    approval = bundle["approval"].model_copy(update={"fresh_planning_evidence": None})
    request = bundle["request"].model_copy(update={"approval_record": approval})
    with pytest.raises(WorkPacketCompilerInputError):
        compile_ticket_spec_to_work_packet(request)


def test_mismatched_recomputed_plan_fails(
    bundle: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        compiler_module,
        "build_ticket_dependency_plan",
        lambda _request: build_ticket_dependency_plan(
            TicketPlanningRequest(
                project_spec=project(), tickets=(ticket(ticket_id="P17.1"),)
            )
        ),
    )
    with pytest.raises(WorkPacketCompilerIntegrityError):
        compile_ticket_spec_to_work_packet(bundle["request"])


def test_valid_compiler_result_contract(result: WorkPacketCompilationResult) -> None:
    packet = result.work_packet
    assert result.disposition is WorkPacketCompilationDisposition.COMPILED
    assert packet.execution_ready is False
    assert packet.authority_boundary is WorkPacketAuthorityBoundary.COMPILE_ONLY
    assert packet.execution_mode is WorkPacketExecutionMode.SINGLE_AGENT
    assert packet.git_authority is WorkPacketGitAuthority.HUMAN_ONLY
    assert packet.project_id == "P17"
    assert packet.ticket_id == "P17.0"
    assert packet.publication_id.startswith("PUB-P17-0-")
    assert packet.publication_revision == 1
    assert packet.project_spec == packet.project_spec
    assert packet.source_ticket == packet.source_ticket
    assert packet.response_contract == packet.source_ticket.response_contract
    assert packet.work_packet_id.startswith("WP-P17-0-R0001-")
    assert packet.work_packet_id.endswith(packet.compilation_input_SHA256[:12])
    assert len(packet.downstream_requirements) == 7
    assert len(packet.compilation_input_SHA256) == 64
    assert len(packet.work_packet_SHA256) == 64
    assert len(result.evidence.evidence_SHA256) == 64
    assert len(result.result_SHA256) == 64


def test_same_request_produces_same_result_and_no_mutation(
    bundle: dict[str, object],
) -> None:
    request = bundle["request"]
    before = request.model_dump_json()
    first = compile_ticket_spec_to_work_packet(request)
    second = compile_ticket_spec_to_work_packet(request)
    assert first == second
    assert request.model_dump_json() == before


@pytest.mark.parametrize(
    "update",
    (
        {"schema_version": 2},
        {"compiler_policy_id": "other"},
        {"authority_boundary": "runtime"},
        {"execution_ready": True},
        {"git_authority": "machine"},
        {"project_id": "P18"},
        {"ticket_id": "P17.1"},
        {"publication_id": "PUB-P17-1-0001"},
        {"source_ticket_SHA256": "0" * 64},
        {"compilation_input_SHA256": "0" * 64},
        {"work_packet_SHA256": "0" * 64},
    ),
)
def test_validate_work_packet_rejects_top_level_tampering(
    update: dict[str, object], result: WorkPacketCompilationResult
) -> None:
    tampered = result.work_packet.model_copy(update=update)
    with pytest.raises(WorkPacketCompilerIntegrityError):
        validate_work_packet(tampered)


@pytest.mark.parametrize(
    "field_update",
    (
        ("repository_scope", {"scope_SHA256": "0" * 64}),
        ("tasks", {"ordinal": 2}),
        ("tasks", {"step_SHA256": "0" * 64}),
        ("validation_steps", {"ordinal": 2}),
        ("validation_steps", {"step_SHA256": "0" * 64}),
        ("validation_steps", {"command_execution_authorized": True}),
    ),
)
def test_validate_work_packet_rejects_nested_tampering(
    field_update: tuple[str, dict[str, object]], result: WorkPacketCompilationResult
) -> None:
    field, update = field_update
    current = getattr(result.work_packet, field)
    if isinstance(current, tuple):
        replacement = current[0].model_copy(update=update)
        tampered = result.work_packet.model_copy(
            update={field: (replacement, *current[1:])}
        )
    else:
        tampered = result.work_packet.model_copy(
            update={field: current.model_copy(update=update)}
        )
    with pytest.raises(WorkPacketCompilerIntegrityError):
        validate_work_packet(tampered)


def test_downstream_requirement_removal_and_reordering_fail(
    result: WorkPacketCompilationResult,
) -> None:
    packet = result.work_packet
    for requirements in (
        packet.downstream_requirements[:-1],
        tuple(reversed(packet.downstream_requirements)),
    ):
        with pytest.raises(WorkPacketCompilerIntegrityError):
            validate_work_packet(
                packet.model_copy(update={"downstream_requirements": requirements})
            )


def test_shadow_report_rejection_smoke_exact_output() -> None:
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
    assert "TicketFactoryShadowPilotReport" not in str(exc.value)


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_json_round_trip(model: type, bundle: dict[str, object]) -> None:
    sample_by_model = {
        WorkPacketCompilationAuthorization: bundle["authorization"],
        WorkPacketCompilationRequest: bundle["request"],
        WorkPacketCompilationResult: bundle["result"],
        WorkPacket: bundle["result"].work_packet,
        WorkPacketCompilationEvidence: bundle["result"].evidence,
        WorkPacketRepositoryScope: bundle["result"].work_packet.repository_scope,
        WorkPacketTaskStep: bundle["result"].work_packet.tasks[0],
        WorkPacketValidationStep: bundle["result"].work_packet.validation_steps[0],
        WorkPacketDownstreamRequirement: bundle[
            "result"
        ].work_packet.downstream_requirements[0],
    }
    sample = sample_by_model[model]
    assert model.model_validate_json(sample.model_dump_json()) == sample


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_model_schemas_generate_and_forbid_additional_properties(
    model: type,
) -> None:
    first = model.model_json_schema()
    second = model.model_json_schema()
    assert first == second
    assert first.get("additionalProperties") is False
    assert first["properties"]


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_model_fields_do_not_use_forbidden_shapes(model: type) -> None:
    forbidden = {dict, object, bytes}
    for field in model.model_fields.values():
        annotation = field.annotation
        assert annotation not in forbidden
        assert get_origin(annotation) not in forbidden
        assert "Any" not in repr(annotation)


@pytest.mark.parametrize(
    "forbidden_name",
    (
        "WorkspaceCreation",
        "WorkspacePath",
        "ProviderSelector",
        "ModelSelector",
        "AgentAllocator",
        "WorkerAllocator",
        "CommandRunner",
        "SubprocessRunner",
        "FilesystemReader",
        "FilesystemWriter",
        "GitAdapter",
        "execute_work_packet",
        "WorkPacketResultEnvelope",
        "WorkPacketFailureEnvelope",
        "DiffReview",
        "ArtifactReview",
        "GitHandoff",
        "workspace_id",
        "process_id",
    ),
)
def test_authority_boundary_has_no_runtime_surfaces(forbidden_name: str) -> None:
    assert not hasattr(work_packet, forbidden_name)


def test_p16_historical_and_shadow_smokes_remain_canonical() -> None:
    from hermes_cli.agent_platform.ticket_factory import (
        run_historical_ticket_regression_corpus,
    )

    historical = run_historical_ticket_regression_corpus()
    shadow = run_ticket_factory_shadow_pilot()
    assert (
        historical.disposition.value,
        len(historical.case_results),
        len(historical.passed_case_ids),
        len(historical.drifted_case_ids),
        historical.run_SHA256,
    ) == (
        "pass",
        12,
        12,
        0,
        "86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d",
    )
    assert (
        shadow.disposition.value,
        shadow.ticket_id,
        shadow.approval_record.state.value,
        shadow.publication_result.publication.state.value,
        shadow.report_SHA256,
    ) == (
        "go_with_constraints",
        "P16.SP1",
        "approved",
        "published",
        "6cb4158558ebe0e321de10c397e16f05ab306ac3a69b3ef46460d6ab188840da",
    )


@pytest.mark.parametrize(
    "digest_field",
    (
        "source_ticket_SHA256",
        "approval_SHA256",
        "publication_artifact_SHA256",
        "compilation_authorization_SHA256",
    ),
)
def test_evidence_digest_binding_fields_are_present(
    digest_field: str, result: WorkPacketCompilationResult
) -> None:
    value = getattr(result.evidence, digest_field)
    assert isinstance(value, str)
    assert len(value) == 64
    int(value, 16)


@pytest.mark.parametrize(
    "forbidden_text",
    (
        "workspace",
        "worktree",
        "provider",
        "model_id",
        "agent_id",
        "worker_id",
        "process_id",
        "execution_id",
        "result_envelope",
        "failure_envelope",
        "cancellation_envelope",
        "git_command",
        "credential",
    ),
)
def test_work_packet_has_no_forbidden_runtime_fields(
    forbidden_text: str, result: WorkPacketCompilationResult
) -> None:
    assert forbidden_text not in result.work_packet.model_fields


def test_digest_values_are_lowercase_sha256(
    result: WorkPacketCompilationResult,
) -> None:
    packet = result.work_packet
    digests = (
        packet.source_ticket_SHA256,
        packet.approval_SHA256,
        packet.publication_artifact_SHA256,
        packet.compilation_authorization_SHA256,
        packet.compilation_input_SHA256,
        packet.work_packet_SHA256,
        result.evidence.evidence_SHA256,
        result.result_SHA256,
    )
    assert all(value == value.lower() and len(value) == 64 for value in digests)
