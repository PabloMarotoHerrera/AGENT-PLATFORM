import builtins
import importlib
import socket
import sys
from collections.abc import Callable
from enum import Enum
from typing import get_args, get_origin

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import ticket_factory
from hermes_cli.agent_platform.ticket_factory import (
    CONTEXT_PACK_SCHEMA_VERSION,
    DEPENDENCY_PLAN_SCHEMA_VERSION,
    PROJECT_SPEC_SCHEMA_VERSION,
    TICKET_GENERATOR_ROLE_SCHEMA_VERSION,
    TICKET_SPEC_SCHEMA_VERSION,
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPack,
    ContextPackAssemblyError,
    ContextPackBudgetError,
    ContextPackItem,
    ContextPackSensitiveContentError,
    ContextPriority,
    ContextSensitivity,
    ContextSourceKind,
    ContextSourceSpec,
    DependencyCollectionValidationError,
    DependencyCycleError,
    DependencyEdge,
    DependencyKind,
    DependencyPlanningError,
    DependencyScope,
    ExternalDependencyResolution,
    ExternalDependencyState,
    GeneratorAssignment,
    GeneratorRoleProfile,
    OptionalSourceOverflowStrategy,
    ParallelPlanningPolicy,
    ParallelWave,
    ParallelizationHint,
    ProjectSpec,
    RepositoryScopeSpec,
    ScopeCollision,
    ScopeCollisionKind,
    TicketBlocker,
    TicketBlockerKind,
    TicketDependencyPlan,
    TicketDependencySpec,
    TicketGenerationRequest,
    TicketGeneratorCompatibilityError,
    TicketGeneratorRole,
    TicketGeneratorRoleError,
    TicketPlanningRequest,
    TicketProposal,
    TicketProposalValidationError,
    TicketResponseContractSpec,
    TicketSpec,
    TicketType,
    TicketValidationStepSpec,
    WaveDisposition,
    assemble_context_pack,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    get_ticket_generator_role_profile,
    list_ticket_generator_role_profiles,
    prepare_ticket_generator_assignments,
    validate_ticket_generator_proposal,
)


P16_0_EXPORTS = (
    "PROJECT_SPEC_SCHEMA_VERSION",
    "TICKET_SPEC_SCHEMA_VERSION",
    "TicketType",
    "DependencyKind",
    "DependencyScope",
    "ParallelizationHint",
    "AuthorityReferenceKind",
    "AuthorityReferenceSpec",
    "TicketDependencySpec",
    "RepositoryScopeSpec",
    "TicketValidationStepSpec",
    "TicketResponseContractSpec",
    "ProjectSpec",
    "TicketSpec",
)
P16_1_EXPORTS = (
    "CONTEXT_PACK_SCHEMA_VERSION",
    "ContextSourceKind",
    "ContextSensitivity",
    "ContextPriority",
    "OptionalSourceOverflowStrategy",
    "ContextSourceSpec",
    "ContextAssemblyPolicy",
    "ContextAssemblyRequest",
    "ContextPackItem",
    "ContextPack",
    "ContextPackAssemblyError",
    "ContextPackBudgetError",
    "ContextPackSensitiveContentError",
    "assemble_context_pack",
)
P16_2_EXPORTS = (
    "TICKET_GENERATOR_ROLE_SCHEMA_VERSION",
    "TicketGeneratorRole",
    "GeneratorRoleProfile",
    "TicketGenerationRequest",
    "GeneratorAssignment",
    "TicketProposal",
    "TicketGeneratorRoleError",
    "TicketGeneratorCompatibilityError",
    "TicketProposalValidationError",
    "get_ticket_generator_role_profile",
    "list_ticket_generator_role_profiles",
    "prepare_ticket_generator_assignments",
    "build_ticket_proposal",
    "validate_ticket_generator_proposal",
)
P16_3_EXPORTS = (
    "DEPENDENCY_PLAN_SCHEMA_VERSION",
    "ExternalDependencyState",
    "ScopeCollisionKind",
    "TicketBlockerKind",
    "WaveDisposition",
    "ExternalDependencyResolution",
    "DependencyEdge",
    "ScopeCollision",
    "TicketBlocker",
    "ParallelPlanningPolicy",
    "TicketPlanningRequest",
    "ParallelWave",
    "TicketDependencyPlan",
    "DependencyPlanningError",
    "DependencyCollectionValidationError",
    "DependencyCycleError",
    "build_ticket_dependency_plan",
)
PUBLIC_MODELS = (
    ExternalDependencyResolution,
    DependencyEdge,
    ScopeCollision,
    TicketBlocker,
    ParallelPlanningPolicy,
    TicketPlanningRequest,
    ParallelWave,
    TicketDependencyPlan,
)


def scope(*paths: str, **overrides: object) -> RepositoryScopeSpec:
    data = {
        "allowed_paths": paths or ("src/shared.py",),
        "forbidden_paths": ("4_external/sources/**",),
        "allowed_actions": ("edit planning dependency contracts",),
        "forbidden_actions": ("execute tickets",),
    }
    data.update(overrides)
    return RepositoryScopeSpec.model_validate(data)


def authority(**overrides: object) -> AuthorityReferenceSpec:
    data = {
        "kind": AuthorityReferenceKind.GOVERNANCE_RECORD,
        "value": "0_architecture/governance/example.md",
        "rationale": "Synthetic authority reference.",
    }
    data.update(overrides)
    return AuthorityReferenceSpec.model_validate(data)


def response_contract(**overrides: object) -> TicketResponseContractSpec:
    data = {
        "required_sections": ("Summary", "Tests"),
        "completion_verdict": "synthetic_ticket_ready",
    }
    data.update(overrides)
    return TicketResponseContractSpec.model_validate(data)


def validation_step(**overrides: object) -> TicketValidationStepSpec:
    data = {
        "validation_id": "V1",
        "description": "Run the focused synthetic validation.",
        "command": "python -m pytest synthetic_tests.py",
        "expected_result": "The synthetic test suite reports success.",
    }
    data.update(overrides)
    return TicketValidationStepSpec.model_validate(data)


def dependency(
    ticket_id: str,
    *,
    kind: DependencyKind = DependencyKind.HARD_PREREQUISITE,
    dep_scope: DependencyScope = DependencyScope.INTERNAL_PROJECT,
    rationale: str = "Synthetic dependency declaration.",
) -> TicketDependencySpec:
    return TicketDependencySpec(
        ticket_id=ticket_id,
        kind=kind,
        scope=dep_scope,
        rationale=rationale,
    )


def project(**overrides: object) -> ProjectSpec:
    data = {
        "project_id": "P16",
        "title": "Synthetic planning project",
        "objective": "Define synthetic immutable planning contracts.",
        "summary": "This synthetic project validates dependency planning only.",
        "context": ("A synthetic context entry describes the planning boundary.",),
        "authority_references": (authority(),),
        "scope": scope("src/**"),
        "constraints": ("No execution behavior is authorized.",),
        "non_goals": ("Parallel waves are not execution authority.",),
        "acceptance_criteria": ("The project contract validates declarative data.",),
        "completion_verdict": "synthetic_project_ready",
    }
    data.update(overrides)
    return ProjectSpec.model_validate(data)


def ticket(
    ticket_id: str = "P16.1",
    *,
    project_id: str = "P16",
    deps: tuple[TicketDependencySpec, ...] = (),
    paths: tuple[str, ...] = ("src/shared.py",),
    hint: ParallelizationHint = ParallelizationHint.UNSPECIFIED,
    title: str | None = None,
    objective: str | None = None,
) -> TicketSpec:
    return TicketSpec(
        project_id=project_id,
        ticket_id=ticket_id,
        title=title or f"Synthetic ticket {ticket_id}",
        ticket_type=TicketType.IMPLEMENTATION,
        objective=objective or f"Plan dependency behavior for {ticket_id}.",
        context=(f"Synthetic context for {ticket_id}.",),
        authority_references=(authority(),),
        dependencies=deps,
        parallelization_hint=hint,
        scope=scope(*paths),
        constraints=("Validation commands remain inert text.",),
        tasks=(f"Create immutable dependency planning data for {ticket_id}.",),
        acceptance_criteria=(f"{ticket_id} validates dependency planning.",),
        validation_steps=(validation_step(),),
        response_contract=response_contract(),
        recommended_commit_message=f"Add synthetic {ticket_id}",
    )


def resolution(
    ticket_id: str = "P15.1",
    *,
    state: ExternalDependencyState = ExternalDependencyState.SATISFIED,
    evidence_reference: str | None = "external evidence record",
    rationale: str = "Synthetic external dependency resolution.",
) -> ExternalDependencyResolution:
    return ExternalDependencyResolution(
        ticket_id=ticket_id,
        state=state,
        evidence_reference=evidence_reference,
        rationale=rationale,
    )


def request(
    *tickets: TicketSpec,
    resolutions: tuple[ExternalDependencyResolution, ...] = (),
    policy: ParallelPlanningPolicy | None = None,
    project_spec: ProjectSpec | None = None,
) -> TicketPlanningRequest:
    return TicketPlanningRequest(
        project_spec=project_spec or project(),
        tickets=tickets or (ticket(),),
        external_dependency_resolutions=resolutions,
        policy=policy or ParallelPlanningPolicy(),
    )


def unchecked_request(
    *tickets: TicketSpec,
    resolutions: tuple[ExternalDependencyResolution, ...] = (),
    policy: ParallelPlanningPolicy | None = None,
    project_spec: ProjectSpec | None = None,
) -> TicketPlanningRequest:
    return TicketPlanningRequest.model_construct(
        project_spec=project_spec or project(),
        tickets=tickets or (ticket(),),
        external_dependency_resolutions=resolutions,
        policy=policy or ParallelPlanningPolicy(),
    )


def plan(
    *tickets: TicketSpec,
    resolutions: tuple[ExternalDependencyResolution, ...] = (),
    policy: ParallelPlanningPolicy | None = None,
) -> TicketDependencyPlan:
    return build_ticket_dependency_plan(
        request(*tickets, resolutions=resolutions, policy=policy)
    )


def assert_validation_fails(factory: Callable[[], object]) -> None:
    with pytest.raises(ValidationError):
        factory()


def walk_schema_nodes(value: object) -> tuple[object, ...]:
    nodes = [value]
    index = 0
    while index < len(nodes):
        current = nodes[index]
        index += 1
        if isinstance(current, dict):
            nodes.extend(current.values())
        elif isinstance(current, list):
            nodes.extend(current)
    return tuple(nodes)


def annotation_contains_forbidden(annotation: object) -> bool:
    typing_module = importlib.import_module("typing")
    if annotation is typing_module.Any:
        return True
    origin = get_origin(annotation)
    if origin is None:
        return annotation in {dict, object, bytes}
    if origin is dict:
        return True
    return any(
        annotation_contains_forbidden(argument) for argument in get_args(annotation)
    )


def test_package_imports_and_exports_p16_3_surface() -> None:
    assert len(P16_3_EXPORTS) == 17
    assert isinstance(ticket_factory.__all__, tuple)
    assert len(ticket_factory.__all__) == len(set(ticket_factory.__all__))
    for expected in (P16_0_EXPORTS, P16_1_EXPORTS, P16_2_EXPORTS, P16_3_EXPORTS):
        assert set(expected).issubset(set(ticket_factory.__all__))
        assert (
            tuple(name for name in ticket_factory.__all__ if name in expected)
            == expected
        )
        for name in expected:
            assert hasattr(ticket_factory, name)
    assert "PLANNING_INPUT_DIGEST_ALGORITHM" not in ticket_factory.__all__


def test_import_has_no_runtime_provider_network_or_file_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    before_modules = set(sys.modules)

    def fail_socket(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("network access is not allowed")

    def fail_open(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)
    monkeypatch.setattr(builtins, "open", fail_open)
    imported = importlib.import_module(
        "hermes_cli.agent_platform.ticket_factory.dependency_planning"
    )
    assert imported.TicketDependencyPlan.__name__ == "TicketDependencyPlan"
    new_modules = set(sys.modules) - before_modules
    assert not any(name.startswith("providers") for name in new_modules)
    assert not any(name.startswith("agent.") for name in new_modules)
    assert not any("runtime_adapter" in name for name in new_modules)


def test_schema_version_constants_and_defaults() -> None:
    assert PROJECT_SPEC_SCHEMA_VERSION == 1
    assert TICKET_SPEC_SCHEMA_VERSION == 1
    assert CONTEXT_PACK_SCHEMA_VERSION == 1
    assert TICKET_GENERATOR_ROLE_SCHEMA_VERSION == 1
    assert DEPENDENCY_PLAN_SCHEMA_VERSION == 1
    assert plan(ticket()).schema_version == 1


def test_alternative_plan_schema_version_is_rejected() -> None:
    data = plan(ticket()).model_dump(mode="json")
    data["schema_version"] = 2
    assert_validation_fails(lambda: TicketDependencyPlan.model_validate(data))


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_are_frozen_and_extra_forbid(model_type: type) -> None:
    assert model_type.model_config["frozen"] is True
    assert model_type.model_config["extra"] == "forbid"


@pytest.mark.parametrize(
    "model_type, data",
    [
        (
            ExternalDependencyResolution,
            {
                "ticket_id": "P15.1",
                "state": "unresolved",
                "rationale": "Synthetic rationale.",
            },
        ),
        (
            DependencyEdge,
            {
                "prerequisite_ticket_id": "P16.1",
                "dependent_ticket_id": "P16.2",
                "kind": "hard_prerequisite",
                "scope": "internal_project",
                "blocks_readiness": True,
            },
        ),
        (
            ScopeCollision,
            {
                "collision_id": "SCOPE-001",
                "left_ticket_id": "P16.1",
                "right_ticket_id": "P16.2",
                "left_path_pattern": "src/a.py",
                "right_path_pattern": "src/a.py",
                "kind": "exact_pattern",
                "blocks_same_wave": True,
            },
        ),
        (
            TicketBlocker,
            {
                "ticket_id": "P16.2",
                "blocked_by_ticket_id": "P15.1",
                "kind": "external_unresolved",
                "direct": True,
                "rationale": "Synthetic blocker.",
            },
        ),
        (ParallelPlanningPolicy, {}),
        (
            TicketPlanningRequest,
            {"project_spec": project(), "tickets": (ticket(),)},
        ),
        (
            ParallelWave,
            {
                "wave_index": 1,
                "wave_id": "WAVE-001",
                "ticket_ids": ("P16.1",),
                "disposition": "dependency_ready",
            },
        ),
        (TicketDependencyPlan, plan(ticket()).model_dump(mode="json")),
    ],
)
def test_unknown_fields_are_rejected(model_type: type, data: dict[str, object]) -> None:
    data["unexpected"] = "value"
    assert_validation_fails(lambda: model_type.model_validate(data))


def test_mutable_sequences_normalize_to_tuples() -> None:
    req = TicketPlanningRequest.model_validate({
        "project_spec": project(),
        "tickets": [ticket()],
        "external_dependency_resolutions": [],
        "policy": {},
    })
    generated = build_ticket_dependency_plan(req)
    assert isinstance(req.tickets, tuple)
    assert isinstance(req.external_dependency_resolutions, tuple)
    assert isinstance(generated.ticket_ids, tuple)
    assert isinstance(generated.edges, tuple)
    assert isinstance(generated.waves, tuple)


@pytest.mark.parametrize(
    "factory",
    [
        lambda: DependencyEdge(
            prerequisite_ticket_id="P16.1",
            dependent_ticket_id="P16.2",
            kind=DependencyKind.HARD_PREREQUISITE,
            scope=DependencyScope.INTERNAL_PROJECT,
            blocks_readiness="true",
        ),
        lambda: ScopeCollision(
            collision_id="SCOPE-001",
            left_ticket_id="P16.1",
            right_ticket_id="P16.2",
            left_path_pattern="src/a.py",
            right_path_pattern="src/a.py",
            kind=ScopeCollisionKind.EXACT_PATTERN,
            blocks_same_wave="true",
        ),
        lambda: TicketBlocker(
            ticket_id="P16.2",
            blocked_by_ticket_id="P15.1",
            kind=TicketBlockerKind.EXTERNAL_UNRESOLVED,
            direct="true",
            rationale="Synthetic blocker.",
        ),
        lambda: ParallelPlanningPolicy(separate_serial_tickets=False),
        lambda: ParallelPlanningPolicy(separate_known_scope_collisions=False),
        lambda: ParallelPlanningPolicy(ambiguous_glob_requires_review=False),
    ],
)
def test_strict_booleans_reject_strings_and_disabled_safety(
    factory: Callable[[], object],
) -> None:
    assert_validation_fails(factory)


def test_no_mutable_defaults_on_public_models() -> None:
    for model_type in PUBLIC_MODELS:
        for field in model_type.model_fields.values():
            assert not isinstance(field.default, (list, dict, set))


def test_enum_values_and_aliases() -> None:
    assert tuple(item.value for item in ExternalDependencyState) == (
        "satisfied",
        "unresolved",
        "blocked",
    )
    assert tuple(item.value for item in ScopeCollisionKind) == (
        "exact_pattern",
        "recursive_prefix",
        "global_pattern",
        "ambiguous_glob",
    )
    assert tuple(item.value for item in TicketBlockerKind) == (
        "external_unresolved",
        "external_blocked",
        "upstream_blocked",
    )
    assert tuple(item.value for item in WaveDisposition) == (
        "dependency_ready",
        "serial",
        "scope_review_required",
    )
    for enum_type in (
        ExternalDependencyState,
        ScopeCollisionKind,
        TicketBlockerKind,
        WaveDisposition,
    ):
        assert len(enum_type.__members__) == len(tuple(enum_type))
        assert issubclass(enum_type, Enum)


def test_satisfied_external_resolution_requires_evidence() -> None:
    assert_validation_fails(
        lambda: resolution(
            evidence_reference=None, state=ExternalDependencyState.SATISFIED
        )
    )


def test_unresolved_external_resolution_may_omit_evidence() -> None:
    item = resolution(
        evidence_reference=None,
        state=ExternalDependencyState.UNRESOLVED,
    )
    assert item.evidence_reference is None


def test_blocked_external_resolution_validates() -> None:
    item = resolution(
        evidence_reference=None,
        state=ExternalDependencyState.BLOCKED,
        rationale="Synthetic upstream blocker.",
    )
    assert item.state is ExternalDependencyState.BLOCKED


def test_duplicate_external_resolutions_fail() -> None:
    dep = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    t1 = ticket(deps=(dep,))
    res = resolution("P15.1")
    assert_validation_fails(lambda: request(t1, resolutions=(res, res)))


def test_external_resolution_for_undeclared_dependency_fails() -> None:
    assert_validation_fails(
        lambda: request(ticket(), resolutions=(resolution("P15.1"),))
    )


def test_external_resolution_does_not_perform_lookup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dep = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)

    def fail_open(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("file access is not allowed")

    def fail_socket(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(socket, "socket", fail_socket)
    generated = plan(ticket(deps=(dep,)), resolutions=(resolution("P15.1"),))
    assert generated.blocked_ticket_ids == ()


def test_one_ticket_collection_succeeds() -> None:
    generated = plan(ticket())
    assert generated.ticket_ids == ("P16.1",)


def test_duplicate_ticket_ids_fail() -> None:
    assert_validation_fails(lambda: request(ticket("P16.1"), ticket("P16.1")))


def test_foreign_project_ticket_fails() -> None:
    foreign = ticket("P15.1", project_id="P15")
    assert_validation_fails(lambda: request(foreign))


def test_internal_dependency_target_missing_fails() -> None:
    t2 = ticket("P16.2", deps=(dependency("P16.1"),))
    assert_validation_fails(lambda: request(t2))


def test_internal_dependency_with_foreign_prefix_fails() -> None:
    t2 = ticket("P16.2", deps=(dependency("P15.1"),))
    assert_validation_fails(lambda: request(t2))


def test_external_dependency_with_current_project_prefix_fails() -> None:
    dep = dependency("P16.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    assert_validation_fails(lambda: request(ticket("P16.2", deps=(dep,))))


def test_ticket_input_permutation_remains_valid_and_canonical() -> None:
    t1 = ticket("P16.1")
    t2 = ticket("P16.2")
    first = plan(t2, t1)
    second = plan(t1, t2)
    assert first.ticket_ids == ("P16.1", "P16.2")
    assert first == second


def test_512_ticket_collection_is_accepted() -> None:
    tickets = tuple(
        ticket(f"P16.{index}", paths=(f"src/{index}.py",)) for index in range(1, 513)
    )
    generated = plan(*tickets)
    assert len(generated.ticket_ids) == 512


def test_oversized_ticket_collection_fails() -> None:
    tickets = tuple(ticket(f"P16.{index}") for index in range(1, 514))
    assert_validation_fails(lambda: request(*tickets))


@pytest.mark.parametrize(
    "dep_kind, dep_scope, expected_blocks",
    [
        (DependencyKind.HARD_PREREQUISITE, DependencyScope.INTERNAL_PROJECT, True),
        (DependencyKind.SOFT_PREDECESSOR, DependencyScope.INTERNAL_PROJECT, False),
        (DependencyKind.HARD_PREREQUISITE, DependencyScope.EXTERNAL_PROJECT, True),
        (DependencyKind.SOFT_PREDECESSOR, DependencyScope.EXTERNAL_PROJECT, False),
    ],
)
def test_edge_construction_maps_dependency_kind_to_readiness(
    dep_kind: DependencyKind, dep_scope: DependencyScope, expected_blocks: bool
) -> None:
    prerequisite = "P16.1" if dep_scope is DependencyScope.INTERNAL_PROJECT else "P15.1"
    dep = dependency(prerequisite, kind=dep_kind, dep_scope=dep_scope)
    tickets = (ticket("P16.1"), ticket("P16.2", deps=(dep,)))
    if dep_scope is DependencyScope.EXTERNAL_PROJECT:
        tickets = (ticket("P16.2", deps=(dep,)),)
    generated = plan(*tickets)
    assert generated.edges[0].prerequisite_ticket_id == prerequisite
    assert generated.edges[0].dependent_ticket_id == "P16.2"
    assert generated.edges[0].blocks_readiness is expected_blocks


def test_inconsistent_dependency_edge_blocks_readiness_fails() -> None:
    assert_validation_fails(
        lambda: DependencyEdge(
            prerequisite_ticket_id="P16.1",
            dependent_ticket_id="P16.2",
            kind=DependencyKind.SOFT_PREDECESSOR,
            scope=DependencyScope.INTERNAL_PROJECT,
            blocks_readiness=True,
        )
    )


def test_edge_order_is_deterministic_and_unique() -> None:
    t1 = ticket("P16.1")
    t2 = ticket("P16.2", deps=(dependency("P16.1"),))
    t3 = ticket("P16.3", deps=(dependency("P16.1"), dependency("P16.2")))
    first = plan(t3, t2, t1).edges
    second = plan(t1, t3, t2).edges
    assert first == second
    assert len(first) == len(
        set((edge.prerequisite_ticket_id, edge.dependent_ticket_id) for edge in first)
    )


def test_acyclic_hard_graph_succeeds() -> None:
    generated = plan(ticket("P16.1"), ticket("P16.2", deps=(dependency("P16.1"),)))
    assert generated.topological_order == ("P16.1", "P16.2")


@pytest.mark.parametrize(
    "tickets, expected_cycle",
    [
        (
            (
                ticket("P16.1", deps=(dependency("P16.2"),)),
                ticket("P16.2", deps=(dependency("P16.1"),)),
            ),
            ("P16.1", "P16.2"),
        ),
        (
            (
                ticket("P16.1", deps=(dependency("P16.3"),)),
                ticket("P16.2", deps=(dependency("P16.1"),)),
                ticket("P16.3", deps=(dependency("P16.2"),)),
            ),
            ("P16.1", "P16.2", "P16.3"),
        ),
        (
            (
                ticket("P16.1"),
                ticket("P16.2", deps=(dependency("P16.3"),)),
                ticket("P16.3", deps=(dependency("P16.2"),)),
            ),
            ("P16.2", "P16.3"),
        ),
    ],
)
def test_hard_cycles_fail_with_deterministic_witness(
    tickets: tuple[TicketSpec, ...], expected_cycle: tuple[str, ...]
) -> None:
    with pytest.raises(DependencyCycleError) as exc_info:
        build_ticket_dependency_plan(request(*reversed(tickets)))
    assert exc_info.value.cycle_ticket_ids == expected_cycle


def test_cycle_exception_excludes_full_ticket_content() -> None:
    secret_objective = "Sensitive synthetic objective not for error output."
    command_text = "python -m pytest sensitive_synthetic_tests.py"
    t1 = ticket(
        "P16.1",
        deps=(dependency("P16.2"),),
        objective=secret_objective,
    )
    t2 = ticket("P16.2", deps=(dependency("P16.1"),))
    with pytest.raises(DependencyCycleError) as exc_info:
        build_ticket_dependency_plan(request(t1, t2))
    message = str(exc_info.value)
    assert "P16.1" in message
    assert secret_objective not in message
    assert command_text not in message


def test_soft_only_cycle_succeeds_as_advisory_metadata() -> None:
    t1 = ticket(
        "P16.1",
        deps=(dependency("P16.2", kind=DependencyKind.SOFT_PREDECESSOR),),
    )
    t2 = ticket(
        "P16.2",
        deps=(dependency("P16.1", kind=DependencyKind.SOFT_PREDECESSOR),),
    )
    generated = plan(t1, t2)
    assert generated.topological_order == ("P16.1", "P16.2")


def test_mixed_graph_with_no_hard_cycle_succeeds() -> None:
    t1 = ticket("P16.1")
    t2 = ticket("P16.2", deps=(dependency("P16.1"),))
    t3 = ticket(
        "P16.3",
        deps=(dependency("P16.2", kind=DependencyKind.SOFT_PREDECESSOR),),
    )
    assert plan(t3, t2, t1).topological_order == ("P16.1", "P16.2", "P16.3")


def test_canonical_ticket_order_numeric_and_alpha_segments() -> None:
    generated = plan(
        ticket("P16.R"),
        ticket("P16.10"),
        ticket("P16.C1"),
        ticket("P16.3"),
        ticket("P16.2"),
    )
    assert generated.ticket_ids == ("P16.2", "P16.3", "P16.10", "P16.C1", "P16.R")


@pytest.mark.parametrize(
    "ticket_ids, expected",
    [
        (("P16.1.10", "P16.1.2"), ("P16.1.2", "P16.1.10")),
        (("P16.B", "P16.A"), ("P16.A", "P16.B")),
        (("P16.R", "P16.C1"), ("P16.C1", "P16.R")),
    ],
)
def test_canonical_ticket_order_components(
    ticket_ids: tuple[str, ...], expected: tuple[str, ...]
) -> None:
    assert plan(*(ticket(ticket_id) for ticket_id in ticket_ids)).ticket_ids == expected


def test_topological_linear_diamond_and_disconnected_ordering() -> None:
    linear = plan(ticket("P16.1"), ticket("P16.2", deps=(dependency("P16.1"),)))
    assert linear.topological_order == ("P16.1", "P16.2")
    diamond = plan(
        ticket("P16.1"),
        ticket("P16.2", deps=(dependency("P16.1"),)),
        ticket("P16.3", deps=(dependency("P16.1"),)),
        ticket("P16.4", deps=(dependency("P16.2"), dependency("P16.3"))),
    )
    assert diamond.topological_order == ("P16.1", "P16.2", "P16.3", "P16.4")
    disconnected = plan(
        ticket("P16.3"),
        ticket("P16.1"),
        ticket("P16.2", deps=(dependency("P16.1"),)),
    )
    assert disconnected.topological_order == ("P16.1", "P16.2", "P16.3")


def test_topological_order_contains_blocked_tickets_and_all_tickets_once() -> None:
    external = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    generated = plan(ticket("P16.1", deps=(external,)), ticket("P16.2"))
    assert generated.blocked_ticket_ids == ("P16.1",)
    assert set(generated.topological_order) == set(generated.ticket_ids)
    assert len(generated.topological_order) == len(generated.ticket_ids)


def test_soft_predecessor_does_not_force_hard_order() -> None:
    t1 = ticket(
        "P16.1",
        deps=(dependency("P16.2", kind=DependencyKind.SOFT_PREDECESSOR),),
    )
    t2 = ticket("P16.2")
    assert plan(t1, t2).topological_order == ("P16.1", "P16.2")


def test_topological_order_is_input_permutation_independent() -> None:
    t1 = ticket("P16.1")
    t2 = ticket("P16.2", deps=(dependency("P16.1"),))
    t3 = ticket("P16.3", deps=(dependency("P16.1"),))
    assert plan(t3, t2, t1).topological_order == plan(t1, t2, t3).topological_order


@pytest.mark.parametrize(
    "state, expected_kind",
    [
        (None, TicketBlockerKind.EXTERNAL_UNRESOLVED),
        (ExternalDependencyState.UNRESOLVED, TicketBlockerKind.EXTERNAL_UNRESOLVED),
        (ExternalDependencyState.BLOCKED, TicketBlockerKind.EXTERNAL_BLOCKED),
    ],
)
def test_hard_external_dependency_blocks_directly(
    state: ExternalDependencyState | None, expected_kind: TicketBlockerKind
) -> None:
    dep = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    resolutions = (
        ()
        if state is None
        else (resolution("P15.1", state=state, evidence_reference=None),)
    )
    generated = plan(ticket("P16.1", deps=(dep,)), resolutions=resolutions)
    assert generated.blocked_ticket_ids == ("P16.1",)
    assert generated.blockers[0].kind is expected_kind
    assert generated.blockers[0].direct is True


def test_satisfied_hard_external_dependency_unblocks() -> None:
    dep = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    generated = plan(ticket("P16.1", deps=(dep,)), resolutions=(resolution("P15.1"),))
    assert generated.blocked_ticket_ids == ()
    assert generated.blockers == ()
    assert generated.waves[0].ticket_ids == ("P16.1",)


def test_soft_external_unresolved_does_not_block_and_is_retained() -> None:
    dep = dependency(
        "P15.1",
        kind=DependencyKind.SOFT_PREDECESSOR,
        dep_scope=DependencyScope.EXTERNAL_PROJECT,
    )
    generated = plan(ticket("P16.1", deps=(dep,)))
    assert generated.blocked_ticket_ids == ()
    assert generated.unresolved_soft_external_dependency_ids == ("P15.1",)


def test_blocker_propagates_one_and_multiple_levels_over_hard_edges() -> None:
    external = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    t1 = ticket("P16.1", deps=(external,))
    t2 = ticket("P16.2", deps=(dependency("P16.1"),))
    t3 = ticket("P16.3", deps=(dependency("P16.2"),))
    generated = plan(t1, t2, t3)
    assert generated.blocked_ticket_ids == ("P16.1", "P16.2", "P16.3")
    assert ("P16.2", "P16.1", TicketBlockerKind.UPSTREAM_BLOCKED) in {
        (blocker.ticket_id, blocker.blocked_by_ticket_id, blocker.kind)
        for blocker in generated.blockers
    }
    assert ("P16.3", "P16.2", TicketBlockerKind.UPSTREAM_BLOCKED) in {
        (blocker.ticket_id, blocker.blocked_by_ticket_id, blocker.kind)
        for blocker in generated.blockers
    }


def test_blocker_does_not_propagate_over_soft_edge() -> None:
    external = dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    t1 = ticket("P16.1", deps=(external,))
    t2 = ticket(
        "P16.2",
        deps=(dependency("P16.1", kind=DependencyKind.SOFT_PREDECESSOR),),
    )
    generated = plan(t1, t2)
    assert generated.blocked_ticket_ids == ("P16.1",)
    assert generated.waves[0].ticket_ids == ("P16.2",)


def test_multiple_blockers_remain_deterministic_and_blocked_tickets_are_not_waved() -> (
    None
):
    deps = (
        dependency("P15.2", dep_scope=DependencyScope.EXTERNAL_PROJECT),
        dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT),
    )
    generated = plan(ticket("P16.1", deps=deps), ticket("P16.2"))
    assert tuple(blocker.blocked_by_ticket_id for blocker in generated.blockers) == (
        "P15.1",
        "P15.2",
    )
    assert all("P16.1" not in wave.ticket_ids for wave in generated.waves)


@pytest.mark.parametrize(
    "left_paths, right_paths, expected_kind, expected_blocks",
    [
        (("src/a.py",), ("src/a.py",), ScopeCollisionKind.EXACT_PATTERN, True),
        (("docs/**",), ("docs/file.md",), ScopeCollisionKind.RECURSIVE_PREFIX, True),
        (("**",), ("src/a.py",), ScopeCollisionKind.GLOBAL_PATTERN, True),
        (("src/*.py",), ("src/a.py",), ScopeCollisionKind.AMBIGUOUS_GLOB, False),
    ],
)
def test_scope_collision_kinds_and_blocking(
    left_paths: tuple[str, ...],
    right_paths: tuple[str, ...],
    expected_kind: ScopeCollisionKind,
    expected_blocks: bool,
) -> None:
    generated = plan(
        ticket("P16.1", paths=left_paths), ticket("P16.2", paths=right_paths)
    )
    assert generated.scope_collisions[0].kind is expected_kind
    assert generated.scope_collisions[0].blocks_same_wave is expected_blocks


def test_nonoverlapping_literals_produce_no_scope_collision() -> None:
    generated = plan(
        ticket("P16.1", paths=("src/a.py",)), ticket("P16.2", paths=("src/b.py",))
    )
    assert generated.scope_collisions == ()


def test_scope_collision_pair_order_and_ids_are_deterministic() -> None:
    t1 = ticket("P16.1", paths=("src/a.py",))
    t2 = ticket("P16.2", paths=("src/a.py",))
    first = plan(t2, t1).scope_collisions
    second = plan(t1, t2).scope_collisions
    assert first == second
    assert first[0].collision_id == "SCOPE-001"
    assert first[0].left_ticket_id == "P16.1"
    assert first[0].right_ticket_id == "P16.2"


def test_scope_collision_detection_does_not_check_filesystem_or_expand_globs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_open(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("filesystem access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    generated = plan(
        ticket("P16.1", paths=("missing/**/*.py",)),
        ticket("P16.2", paths=("missing/file.py",)),
    )
    assert generated.scope_collisions[0].kind is ScopeCollisionKind.AMBIGUOUS_GLOB


def test_parallel_policy_defaults_and_json_round_trip() -> None:
    policy = ParallelPlanningPolicy()
    assert policy.max_wave_size == 32
    assert policy.separate_serial_tickets is True
    assert policy.separate_known_scope_collisions is True
    assert policy.ambiguous_glob_requires_review is True
    assert (
        ParallelPlanningPolicy.model_validate_json(policy.model_dump_json()) == policy
    )


@pytest.mark.parametrize("max_wave_size", [1, 64])
def test_parallel_policy_boundary_values_validate(max_wave_size: int) -> None:
    assert (
        ParallelPlanningPolicy(max_wave_size=max_wave_size).max_wave_size
        == max_wave_size
    )


@pytest.mark.parametrize("max_wave_size", [0, 65])
def test_parallel_policy_out_of_range_values_fail(max_wave_size: int) -> None:
    assert_validation_fails(lambda: ParallelPlanningPolicy(max_wave_size=max_wave_size))


def test_independent_tickets_share_dependency_ready_wave() -> None:
    generated = plan(
        ticket("P16.1", paths=("src/a.py",)), ticket("P16.2", paths=("src/b.py",))
    )
    assert generated.waves[0].ticket_ids == ("P16.1", "P16.2")
    assert generated.waves[0].disposition is WaveDisposition.DEPENDENCY_READY


def test_linear_dependencies_create_sequential_waves() -> None:
    generated = plan(ticket("P16.1"), ticket("P16.2", deps=(dependency("P16.1"),)))
    assert tuple(wave.ticket_ids for wave in generated.waves) == (
        ("P16.1",),
        ("P16.2",),
    )


def test_diamond_graph_creates_expected_waves() -> None:
    generated = plan(
        ticket("P16.1"),
        ticket("P16.2", deps=(dependency("P16.1"),), paths=("src/b.py",)),
        ticket("P16.3", deps=(dependency("P16.1"),), paths=("src/c.py",)),
        ticket("P16.4", deps=(dependency("P16.2"), dependency("P16.3"))),
    )
    assert tuple(wave.ticket_ids for wave in generated.waves) == (
        ("P16.1",),
        ("P16.2", "P16.3"),
        ("P16.4",),
    )


def test_serial_hint_creates_one_ticket_wave_and_isolates_ready_ticket() -> None:
    generated = plan(
        ticket("P16.1", hint=ParallelizationHint.SERIAL),
        ticket("P16.2", paths=("src/b.py",)),
    )
    assert generated.waves[0].ticket_ids == ("P16.1",)
    assert generated.waves[0].disposition is WaveDisposition.SERIAL
    assert generated.waves[1].ticket_ids == ("P16.2",)


def test_known_collision_separates_tickets() -> None:
    generated = plan(
        ticket("P16.1", paths=("src/a.py",)), ticket("P16.2", paths=("src/a.py",))
    )
    assert tuple(wave.ticket_ids for wave in generated.waves) == (
        ("P16.1",),
        ("P16.2",),
    )


def test_ambiguous_collision_marks_scope_review_without_separation() -> None:
    generated = plan(
        ticket("P16.1", paths=("src/*.py",)), ticket("P16.2", paths=("src/a.py",))
    )
    assert generated.waves[0].ticket_ids == ("P16.1", "P16.2")
    assert generated.waves[0].disposition is WaveDisposition.SCOPE_REVIEW_REQUIRED
    assert generated.waves[0].scope_collision_ids == ("SCOPE-001",)


def test_maximum_wave_size_is_respected() -> None:
    generated = plan(
        ticket("P16.1", paths=("src/a.py",)),
        ticket("P16.2", paths=("src/b.py",)),
        ticket("P16.3", paths=("src/c.py",)),
        policy=ParallelPlanningPolicy(max_wave_size=2),
    )
    assert tuple(wave.ticket_ids for wave in generated.waves) == (
        ("P16.1", "P16.2"),
        ("P16.3",),
    )


def test_every_unblocked_ticket_appears_once_and_hard_prerequisite_is_earlier() -> None:
    generated = plan(ticket("P16.1"), ticket("P16.2", deps=(dependency("P16.1"),)))
    waved = tuple(
        ticket_id for wave in generated.waves for ticket_id in wave.ticket_ids
    )
    assert waved == ("P16.1", "P16.2")
    positions = {
        ticket_id: index
        for index, wave in enumerate(generated.waves, start=1)
        for ticket_id in wave.ticket_ids
    }
    assert positions["P16.1"] < positions["P16.2"]


def test_wave_partition_is_input_permutation_independent_and_ids_are_deterministic() -> (
    None
):
    t1 = ticket("P16.1", paths=("src/a.py",))
    t2 = ticket("P16.2", paths=("src/b.py",))
    first = plan(t2, t1).waves
    second = plan(t1, t2).waves
    assert first == second
    assert tuple(wave.wave_id for wave in first) == ("WAVE-001",)
    assert all(wave.ticket_ids for wave in first)


def test_same_request_produces_same_input_digest() -> None:
    req = request(ticket())
    assert (
        build_ticket_dependency_plan(req).planning_input_SHA256
        == build_ticket_dependency_plan(req).planning_input_SHA256
    )


def test_ticket_permutation_preserves_input_digest() -> None:
    t1 = ticket("P16.1")
    t2 = ticket("P16.2")
    assert plan(t2, t1).planning_input_SHA256 == plan(t1, t2).planning_input_SHA256


def test_resolution_permutation_preserves_input_digest() -> None:
    deps = (
        dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT),
        dependency("P15.2", dep_scope=DependencyScope.EXTERNAL_PROJECT),
    )
    t1 = ticket(deps=deps)
    r1 = resolution("P15.1")
    r2 = resolution("P15.2")
    assert (
        plan(t1, resolutions=(r2, r1)).planning_input_SHA256
        == plan(t1, resolutions=(r1, r2)).planning_input_SHA256
    )


@pytest.mark.parametrize(
    "changed_plan",
    [
        lambda: plan(ticket(title="Changed title for digest.")),
        lambda: plan(
            ticket(
                deps=(dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT),)
            ),
            resolutions=(resolution("P15.1", rationale="Changed external rationale."),),
        ),
        lambda: plan(ticket(), policy=ParallelPlanningPolicy(max_wave_size=1)),
    ],
)
def test_changed_request_material_changes_input_digest(
    changed_plan: Callable[[], TicketDependencyPlan],
) -> None:
    assert plan(ticket()).planning_input_SHA256 != changed_plan().planning_input_SHA256


def test_same_plan_produces_same_plan_digest() -> None:
    assert plan(ticket()).plan_SHA256 == plan(ticket()).plan_SHA256


@pytest.mark.parametrize(
    "changed_plan",
    [
        lambda: plan(ticket("P16.1"), ticket("P16.2", deps=(dependency("P16.1"),))),
        lambda: plan(
            ticket(
                deps=(dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT),)
            )
        ),
        lambda: plan(
            ticket("P16.1", paths=("src/a.py",)), ticket("P16.2", paths=("src/a.py",))
        ),
        lambda: plan(
            ticket("P16.1", paths=("src/a.py",)),
            ticket("P16.2", paths=("src/b.py",)),
            policy=ParallelPlanningPolicy(max_wave_size=1),
        ),
    ],
)
def test_changed_plan_material_changes_plan_digest(
    changed_plan: Callable[[], TicketDependencyPlan],
) -> None:
    assert plan(ticket()).plan_SHA256 != changed_plan().plan_SHA256


def test_digests_are_lowercase_sha256() -> None:
    generated = plan(ticket())
    for digest in (generated.planning_input_SHA256, generated.plan_SHA256):
        assert len(digest) == 64
        assert digest == digest.lower()
        assert all(character in "0123456789abcdef" for character in digest)


def test_plan_digest_excludes_its_own_field() -> None:
    generated = plan(ticket())
    data = generated.model_dump(mode="json")
    data["plan_SHA256"] = "0" * 64
    assert_validation_fails(lambda: TicketDependencyPlan.model_validate(data))


def test_request_and_plan_json_round_trip() -> None:
    req = request(ticket())
    generated = build_ticket_dependency_plan(req)
    assert TicketPlanningRequest.model_validate_json(req.model_dump_json()) == req
    assert (
        TicketDependencyPlan.model_validate_json(generated.model_dump_json())
        == generated
    )


def test_nested_model_and_enum_json_round_trip() -> None:
    generated = plan(ticket())
    if generated.edges:
        assert (
            DependencyEdge.model_validate_json(generated.edges[0].model_dump_json())
            == generated.edges[0]
        )
    assert (
        ParallelWave.model_validate_json(generated.waves[0].model_dump_json())
        == generated.waves[0]
    )
    assert generated.waves[0].disposition is WaveDisposition.DEPENDENCY_READY


def test_tuples_remain_immutable() -> None:
    generated = plan(ticket())
    with pytest.raises(AttributeError):
        generated.ticket_ids.append("P16.2")
    with pytest.raises(AttributeError):
        generated.waves[0].ticket_ids.append("P16.2")


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_model_json_schema_generation(model_type: type) -> None:
    assert model_type.model_json_schema()["title"] == model_type.__name__


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_json_schema_rejects_additional_properties(model_type: type) -> None:
    assert model_type.model_json_schema()["additionalProperties"] is False


def test_json_schema_contains_no_unrestricted_object_payload() -> None:
    for model_type in PUBLIC_MODELS:
        for node in walk_schema_nodes(model_type.model_json_schema()):
            if isinstance(node, dict) and node.get("type") == "object":
                assert node.get("additionalProperties") is False
                assert "properties" in node


def test_schema_generation_is_deterministic_in_process() -> None:
    for model_type in PUBLIC_MODELS:
        assert model_type.model_json_schema() == model_type.model_json_schema()


def test_no_public_any_or_mapping_annotations() -> None:
    for model_type in PUBLIC_MODELS:
        for field in model_type.model_fields.values():
            assert not annotation_contains_forbidden(field.annotation)
            assert get_origin(field.annotation) is not dict


def test_public_model_field_order() -> None:
    assert tuple(ExternalDependencyResolution.model_fields) == (
        "ticket_id",
        "state",
        "evidence_reference",
        "rationale",
    )
    assert tuple(DependencyEdge.model_fields) == (
        "prerequisite_ticket_id",
        "dependent_ticket_id",
        "kind",
        "scope",
        "blocks_readiness",
    )
    assert tuple(ScopeCollision.model_fields) == (
        "collision_id",
        "left_ticket_id",
        "right_ticket_id",
        "left_path_pattern",
        "right_path_pattern",
        "kind",
        "blocks_same_wave",
    )
    assert tuple(TicketBlocker.model_fields) == (
        "ticket_id",
        "blocked_by_ticket_id",
        "kind",
        "direct",
        "rationale",
    )
    assert tuple(ParallelPlanningPolicy.model_fields) == (
        "max_wave_size",
        "separate_serial_tickets",
        "separate_known_scope_collisions",
        "ambiguous_glob_requires_review",
    )
    assert tuple(TicketPlanningRequest.model_fields) == (
        "project_spec",
        "tickets",
        "external_dependency_resolutions",
        "policy",
    )
    assert tuple(ParallelWave.model_fields) == (
        "wave_index",
        "wave_id",
        "ticket_ids",
        "disposition",
        "scope_collision_ids",
    )
    assert tuple(TicketDependencyPlan.model_fields) == (
        "schema_version",
        "project_id",
        "ticket_ids",
        "planning_input_SHA256",
        "edges",
        "scope_collisions",
        "blockers",
        "topological_order",
        "waves",
        "blocked_ticket_ids",
        "unresolved_soft_external_dependency_ids",
        "policy",
        "plan_SHA256",
    )


def test_no_runtime_authority_public_api_exists() -> None:
    forbidden_names = (
        "ProviderProfile",
        "ModelSelection",
        "PromptTemplate",
        "render_prompt",
        "run_generator",
        "execute_generator",
        "AgentAssignment",
        "WorkerAssignment",
        "WorktreeAssignment",
        "ExecutionLane",
        "RuntimeConcurrency",
        "ToolExecution",
        "TicketLinter",
        "ProposalSynthesizer",
        "ApprovalDecision",
        "PublishedTicket",
        "WorkPacket",
        "GraphifyOperation",
    )
    for name in forbidden_names:
        assert not hasattr(ticket_factory, name)


def test_no_filesystem_loader_or_network_resolver_exists() -> None:
    forbidden = (
        "load",
        "load_file",
        "read_file",
        "from_file",
        "save",
        "write_file",
        "fetch",
        "resolve_url",
        "network_resolve",
        "expand_glob",
        "inspect_git",
    )
    for name in forbidden:
        assert not hasattr(ticket_factory, name)


def test_exception_hierarchy_is_bounded() -> None:
    assert issubclass(DependencyCollectionValidationError, DependencyPlanningError)
    assert issubclass(DependencyCycleError, DependencyPlanningError)
    assert issubclass(DependencyPlanningError, ValueError)
