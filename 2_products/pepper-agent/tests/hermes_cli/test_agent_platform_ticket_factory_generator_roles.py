import builtins
import importlib
import inspect
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
    DependencyKind,
    DependencyScope,
    GeneratorAssignment,
    GeneratorRoleProfile,
    OptionalSourceOverflowStrategy,
    ParallelizationHint,
    ProjectSpec,
    RepositoryScopeSpec,
    TicketDependencySpec,
    TicketGenerationRequest,
    TicketGeneratorCompatibilityError,
    TicketGeneratorRole,
    TicketGeneratorRoleError,
    TicketProposal,
    TicketProposalValidationError,
    TicketResponseContractSpec,
    TicketSpec,
    TicketType,
    TicketValidationStepSpec,
    assemble_context_pack,
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
PUBLIC_MODELS = (
    GeneratorRoleProfile,
    TicketGenerationRequest,
    GeneratorAssignment,
    TicketProposal,
)
CANONICAL_ROLES = (
    TicketGeneratorRole.ARCHITECTURE,
    TicketGeneratorRole.IMPLEMENTATION,
    TicketGeneratorRole.VALIDATION,
    TicketGeneratorRole.INTEGRATION,
    TicketGeneratorRole.GOVERNANCE,
    TicketGeneratorRole.DOCUMENTATION,
)


def scope(**overrides: object) -> RepositoryScopeSpec:
    data = {
        "allowed_paths": ("2_products/pepper-agent/hermes_cli/**",),
        "forbidden_paths": ("4_external/sources/**",),
        "allowed_actions": ("edit planning generator-role contracts",),
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


def dependency(**overrides: object) -> TicketDependencySpec:
    data = {
        "ticket_id": "P16.0",
        "kind": DependencyKind.SOFT_PREDECESSOR,
        "scope": DependencyScope.INTERNAL_PROJECT,
        "rationale": "Synthetic dependency declaration.",
    }
    data.update(overrides)
    return TicketDependencySpec.model_validate(data)


def project_data(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "project_id": "P16",
        "title": "Synthetic planning project",
        "objective": "Define synthetic immutable planning contracts.",
        "summary": "This synthetic project validates generator-role behavior only.",
        "context": ("A synthetic context entry describes the planning boundary.",),
        "authority_references": (authority(),),
        "scope": scope(),
        "constraints": ("No execution behavior is authorized.",),
        "non_goals": ("Ticket generation remains external to P16.2.",),
        "acceptance_criteria": ("The project contract validates declarative data.",),
        "completion_verdict": "synthetic_project_ready",
    }
    data.update(overrides)
    return data


def project(**overrides: object) -> ProjectSpec:
    return ProjectSpec.model_validate(project_data(**overrides))


def ticket_data(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "project_id": "P16",
        "ticket_id": "P16.2",
        "title": "Synthetic generator roles ticket",
        "ticket_type": TicketType.IMPLEMENTATION,
        "objective": "Define synthetic generator-role contracts.",
        "context": ("A synthetic context entry describes ticket planning.",),
        "authority_references": (authority(),),
        "dependencies": (dependency(),),
        "scope": scope(),
        "constraints": ("Validation commands remain inert text.",),
        "tasks": ("Create immutable generator-role contracts.",),
        "acceptance_criteria": ("The generator-role contract validates invariants.",),
        "validation_steps": (validation_step(),),
        "response_contract": response_contract(),
        "recommended_commit_message": "P16.2 Add synthetic generator roles",
    }
    data.update(overrides)
    return data


def ticket(**overrides: object) -> TicketSpec:
    return TicketSpec.model_validate(ticket_data(**overrides))


def source(**overrides: object) -> ContextSourceSpec:
    source_id = str(overrides.get("source_id", "CTX-GOV-A"))
    kind = overrides.get("kind", ContextSourceKind.GOVERNANCE_RECORD)
    kind_value = kind.value if isinstance(kind, ContextSourceKind) else str(kind)
    data = {
        "source_id": source_id,
        "kind": kind,
        "title": "Synthetic governance source",
        "source_reference": f"{kind_value}:{source_id}",
        "content": f"Synthetic caller supplied content for {source_id}.",
        "authority_references": (),
        "sensitivity": ContextSensitivity.INTERNAL,
        "priority": ContextPriority.NORMAL,
        "required": False,
    }
    data.update(overrides)
    return ContextSourceSpec.model_validate(data)


def context_pack(
    *sources: ContextSourceSpec,
    project_spec: ProjectSpec | None = None,
    ticket_spec: TicketSpec | None = None,
    policy: ContextAssemblyPolicy | None = None,
) -> ContextPack:
    return assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=project_spec or project(),
            ticket_spec=ticket_spec or ticket(),
            sources=sources,
            policy=policy or ContextAssemblyPolicy(),
        )
    )


def generation_request(
    *,
    project_spec: ProjectSpec | None = None,
    ticket_spec: TicketSpec | None = None,
    pack: ContextPack | None = None,
    roles: tuple[TicketGeneratorRole, ...] = (TicketGeneratorRole.IMPLEMENTATION,),
) -> TicketGenerationRequest:
    resolved_project = project_spec or project()
    resolved_ticket = ticket_spec or ticket()
    resolved_pack = pack or context_pack(
        project_spec=resolved_project, ticket_spec=resolved_ticket
    )
    return TicketGenerationRequest(
        project_spec=resolved_project,
        ticket_spec=resolved_ticket,
        context_pack=resolved_pack,
        roles=roles,
    )


def first_assignment(
    *,
    ticket_spec: TicketSpec | None = None,
    pack: ContextPack | None = None,
    roles: tuple[TicketGeneratorRole, ...] = (TicketGeneratorRole.IMPLEMENTATION,),
) -> GeneratorAssignment:
    return prepare_ticket_generator_assignments(
        generation_request(ticket_spec=ticket_spec, pack=pack, roles=roles)
    )[0]


def proposal(
    *,
    assignment: GeneratorAssignment | None = None,
    proposed_ticket: TicketSpec | None = None,
    evidence_source_ids: tuple[str, ...] = ("CTX-PROJECT-SPEC",),
    rationale: str = "Synthetic rationale for the independent proposal.",
    assumptions: tuple[str, ...] = (),
    risks: tuple[str, ...] = (),
    unresolved_questions: tuple[str, ...] = (),
) -> TicketProposal:
    resolved_assignment = assignment or first_assignment()
    return build_ticket_proposal(
        assignment=resolved_assignment,
        proposed_ticket=proposed_ticket
        or ticket(ticket_type=resolved_assignment.ticket_type),
        rationale=rationale,
        evidence_source_ids=evidence_source_ids,
        assumptions=assumptions,
        risks=risks,
        unresolved_questions=unresolved_questions,
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


def test_package_imports_and_exports_p16_2_surface() -> None:
    assert isinstance(ticket_factory.__all__, tuple)
    assert len(ticket_factory.__all__) == len(set(ticket_factory.__all__))
    for expected in (P16_0_EXPORTS, P16_1_EXPORTS, P16_2_EXPORTS):
        assert set(expected).issubset(set(ticket_factory.__all__))
        preserved_order = tuple(
            name for name in ticket_factory.__all__ if name in expected
        )
        assert preserved_order == expected
        for name in expected:
            assert hasattr(ticket_factory, name)
    assert "GENERATOR_INPUT_DIGEST_ALGORITHM" not in ticket_factory.__all__


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
    imported = importlib.import_module("hermes_cli.agent_platform.ticket_factory")
    assert imported.TicketGeneratorRole.__name__ == "TicketGeneratorRole"
    new_modules = set(sys.modules) - before_modules
    assert not any(name.startswith("providers") for name in new_modules)
    assert not any(name.startswith("agent.") for name in new_modules)
    assert not any("provider_runtime" in name for name in new_modules)
    assert not any("provider_worker" in name for name in new_modules)
    assert not any("runtime_adapter" in name for name in new_modules)


def test_schema_version_constant_and_defaults() -> None:
    assert PROJECT_SPEC_SCHEMA_VERSION == 1
    assert TICKET_SPEC_SCHEMA_VERSION == 1
    assert CONTEXT_PACK_SCHEMA_VERSION == 1
    assert TICKET_GENERATOR_ROLE_SCHEMA_VERSION == 1
    assert first_assignment().schema_version == 1
    assert proposal().schema_version == 1


def test_alternative_assignment_schema_version_is_rejected() -> None:
    data = first_assignment().model_dump(mode="json")
    data["schema_version"] = 2
    assert_validation_fails(lambda: GeneratorAssignment.model_validate(data))


def test_alternative_proposal_schema_version_is_rejected() -> None:
    data = proposal().model_dump(mode="json")
    data["schema_version"] = 2
    assert_validation_fails(lambda: TicketProposal.model_validate(data))


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_public_models_are_frozen_and_extra_forbid(model_type: type) -> None:
    assert model_type.model_config["frozen"] is True
    assert model_type.model_config["extra"] == "forbid"


def test_unknown_fields_are_rejected() -> None:
    data = generation_request().model_dump(mode="json")
    data["unexpected"] = "value"
    assert_validation_fails(lambda: TicketGenerationRequest.model_validate(data))


def test_mutable_sequences_normalize_to_tuples() -> None:
    req = TicketGenerationRequest.model_validate({
        "project_spec": project(),
        "ticket_spec": ticket(),
        "context_pack": context_pack(),
        "roles": ["implementation"],
    })
    prop = build_ticket_proposal(
        assignment=prepare_ticket_generator_assignments(req)[0],
        proposed_ticket=ticket(),
        rationale="Synthetic rationale.",
        evidence_source_ids=["CTX-PROJECT-SPEC"],
        assumptions=["Synthetic assumption."],
        risks=["Synthetic risk."],
        unresolved_questions=["Synthetic question."],
    )
    assert isinstance(req.roles, tuple)
    assert isinstance(prop.evidence_source_ids, tuple)
    assert isinstance(prop.assumptions, tuple)
    assert isinstance(prop.risks, tuple)
    assert isinstance(prop.unresolved_questions, tuple)


def test_frozen_models_reject_assignment() -> None:
    profile = get_ticket_generator_role_profile(TicketGeneratorRole.IMPLEMENTATION)
    with pytest.raises(ValidationError):
        profile.title = "changed"


def test_no_mutable_defaults_on_public_models() -> None:
    for model_type in PUBLIC_MODELS:
        for field in model_type.model_fields.values():
            assert not isinstance(field.default, (list, dict, set))


def test_role_enum_values_and_canonical_order() -> None:
    assert tuple(role.value for role in TicketGeneratorRole) == (
        "architecture",
        "implementation",
        "validation",
        "integration",
        "governance",
        "documentation",
    )


def test_invalid_role_strings_fail() -> None:
    assert_validation_fails(
        lambda: TicketGenerationRequest.model_validate({
            "project_spec": project(),
            "ticket_spec": ticket(),
            "context_pack": context_pack(),
            "roles": ["planner"],
        })
    )
    with pytest.raises(ValueError):
        get_ticket_generator_role_profile("planner")


def test_role_enum_has_no_aliases() -> None:
    assert len(TicketGeneratorRole.__members__) == len(tuple(TicketGeneratorRole))
    assert issubclass(TicketGeneratorRole, Enum)


def test_role_profile_registry_contains_exactly_six_unique_profiles() -> None:
    profiles = list_ticket_generator_role_profiles()
    assert len(profiles) == 6
    assert tuple(profile.role for profile in profiles) == CANONICAL_ROLES
    assert len({profile.role for profile in profiles}) == 6


@pytest.mark.parametrize("role", CANONICAL_ROLES)
def test_profile_lookup_is_stable_and_immutable(role: TicketGeneratorRole) -> None:
    first = get_ticket_generator_role_profile(role)
    second = get_ticket_generator_role_profile(role)
    assert first is second
    with pytest.raises(ValidationError):
        first.objective = "changed"


@pytest.mark.parametrize("profile", list_ticket_generator_role_profiles())
def test_every_profile_has_required_collections(profile: GeneratorRoleProfile) -> None:
    assert profile.focus_areas
    assert profile.required_checks
    assert profile.prohibited_claims
    assert profile.primary_ticket_types
    assert profile.supported_ticket_types
    assert set(profile.primary_ticket_types).issubset(profile.supported_ticket_types)


def test_every_ticket_type_has_at_least_one_primary_role() -> None:
    primary_types = {
        ticket_type
        for profile in list_ticket_generator_role_profiles()
        for ticket_type in profile.primary_ticket_types
    }
    assert set(TicketType).issubset(primary_types)


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("focus_areas", ("duplicate", "duplicate")),
        ("required_checks", ("duplicate", "duplicate")),
        ("prohibited_claims", ("duplicate", "duplicate")),
        (
            "primary_ticket_types",
            (TicketType.IMPLEMENTATION, TicketType.IMPLEMENTATION),
        ),
        (
            "supported_ticket_types",
            (TicketType.IMPLEMENTATION, TicketType.IMPLEMENTATION),
        ),
    ],
)
def test_duplicate_profile_collection_entries_fail(
    field_name: str, value: tuple[object, ...]
) -> None:
    data = get_ticket_generator_role_profile(
        TicketGeneratorRole.IMPLEMENTATION
    ).model_dump(mode="python")
    data[field_name] = value
    assert_validation_fails(lambda: GeneratorRoleProfile.model_validate(data))


def test_profile_primary_types_must_be_supported() -> None:
    data = get_ticket_generator_role_profile(
        TicketGeneratorRole.IMPLEMENTATION
    ).model_dump(mode="python")
    data["supported_ticket_types"] = (TicketType.REFACTOR,)
    assert_validation_fails(lambda: GeneratorRoleProfile.model_validate(data))


@pytest.mark.parametrize(
    "role, ticket_type",
    [
        (TicketGeneratorRole.ARCHITECTURE, TicketType.ARCHITECTURE),
        (TicketGeneratorRole.ARCHITECTURE, TicketType.REFACTOR),
        (TicketGeneratorRole.IMPLEMENTATION, TicketType.IMPLEMENTATION),
        (TicketGeneratorRole.IMPLEMENTATION, TicketType.BUGFIX),
        (TicketGeneratorRole.VALIDATION, TicketType.TEST),
        (TicketGeneratorRole.INTEGRATION, TicketType.INTEGRATION),
        (TicketGeneratorRole.GOVERNANCE, TicketType.CLOSURE),
        (TicketGeneratorRole.DOCUMENTATION, TicketType.DOCUMENTATION),
    ],
)
def test_primary_role_ticket_types_validate(
    role: TicketGeneratorRole, ticket_type: TicketType
) -> None:
    req = generation_request(ticket_spec=ticket(ticket_type=ticket_type), roles=(role,))
    assert req.roles == (role,)


def test_unsupported_role_ticket_combination_fails() -> None:
    with pytest.raises(ValidationError):
        generation_request(
            ticket_spec=ticket(ticket_type=TicketType.BUGFIX),
            roles=(TicketGeneratorRole.DOCUMENTATION,),
        )


def test_request_without_primary_role_fails() -> None:
    with pytest.raises(ValidationError):
        generation_request(
            ticket_spec=ticket(ticket_type=TicketType.IMPLEMENTATION),
            roles=(TicketGeneratorRole.ARCHITECTURE,),
        )


def test_request_with_only_supported_non_primary_roles_fails() -> None:
    with pytest.raises(ValidationError):
        generation_request(
            ticket_spec=ticket(ticket_type=TicketType.CLOSURE),
            roles=(TicketGeneratorRole.VALIDATION, TicketGeneratorRole.INTEGRATION),
        )


def test_compatible_multi_role_request_succeeds() -> None:
    req = generation_request(
        ticket_spec=ticket(ticket_type=TicketType.IMPLEMENTATION),
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
    )
    assert req.roles == (
        TicketGeneratorRole.ARCHITECTURE,
        TicketGeneratorRole.IMPLEMENTATION,
    )


def test_six_unique_roles_are_accepted_when_compatible() -> None:
    integration_ticket = ticket(ticket_type=TicketType.INTEGRATION)
    req = generation_request(ticket_spec=integration_ticket, roles=CANONICAL_ROLES)
    assert req.roles == CANONICAL_ROLES


def test_matching_project_ticket_and_context_pack_succeed() -> None:
    req = generation_request()
    assert req.project_spec.project_id == req.ticket_spec.project_id
    assert req.context_pack.project_id == req.ticket_spec.project_id
    assert req.context_pack.ticket_id == req.ticket_spec.ticket_id


def test_mismatched_project_spec_project_id_fails() -> None:
    with pytest.raises(ValidationError):
        generation_request(project_spec=project(project_id="P15"))


def test_mismatched_context_pack_project_id_fails() -> None:
    other_project = project(project_id="P15")
    other_ticket = ticket(project_id="P15", ticket_id="P15.2")
    pack = context_pack(project_spec=other_project, ticket_spec=other_ticket)
    with pytest.raises(ValidationError):
        generation_request(pack=pack)


def test_mismatched_context_pack_ticket_id_fails() -> None:
    other_ticket = ticket(ticket_id="P16.3")
    pack = context_pack(ticket_spec=other_ticket)
    with pytest.raises(ValidationError):
        generation_request(pack=pack)


def test_empty_roles_fail() -> None:
    assert_validation_fails(lambda: generation_request(roles=()))


def test_duplicate_roles_fail() -> None:
    assert_validation_fails(
        lambda: generation_request(
            roles=(
                TicketGeneratorRole.IMPLEMENTATION,
                TicketGeneratorRole.IMPLEMENTATION,
            )
        )
    )


def test_role_input_order_is_not_assignment_order_authority() -> None:
    req = generation_request(
        ticket_spec=ticket(ticket_type=TicketType.INTEGRATION),
        roles=tuple(reversed(CANONICAL_ROLES)),
    )
    assignments = prepare_ticket_generator_assignments(req)
    assert tuple(assignment.role for assignment in assignments) == CANONICAL_ROLES


def test_same_input_produces_same_input_digest() -> None:
    req = generation_request()
    first = prepare_ticket_generator_assignments(req)[0]
    second = prepare_ticket_generator_assignments(req)[0]
    assert first.input_SHA256 == second.input_SHA256


def test_changed_project_spec_changes_input_digest() -> None:
    base = first_assignment()
    changed_project = project(summary="Changed project summary for digest evidence.")
    changed_ticket = ticket()
    changed_pack = context_pack(
        project_spec=changed_project, ticket_spec=changed_ticket
    )
    changed = first_assignment(
        pack=changed_pack,
        ticket_spec=changed_ticket,
        roles=(TicketGeneratorRole.IMPLEMENTATION,),
    )
    changed_req = generation_request(
        project_spec=changed_project,
        ticket_spec=changed_ticket,
        pack=changed_pack,
        roles=(TicketGeneratorRole.IMPLEMENTATION,),
    )
    changed = prepare_ticket_generator_assignments(changed_req)[0]
    assert base.input_SHA256 != changed.input_SHA256


def test_changed_ticket_spec_changes_input_digest() -> None:
    base = first_assignment()
    changed_ticket = ticket(title="Changed synthetic ticket title")
    changed_pack = context_pack(ticket_spec=changed_ticket)
    changed = first_assignment(ticket_spec=changed_ticket, pack=changed_pack)
    assert base.input_SHA256 != changed.input_SHA256


def test_changed_context_pack_changes_input_digest() -> None:
    base = first_assignment()
    changed_pack = context_pack(source(source_id="CTX-GOV-B"))
    changed = first_assignment(pack=changed_pack)
    assert base.input_SHA256 != changed.input_SHA256


def test_input_digest_is_lowercase_sha256() -> None:
    digest = first_assignment().input_SHA256
    assert len(digest) == 64
    assert digest == digest.lower()
    assert all(character in "0123456789abcdef" for character in digest)


def test_context_source_order_normalization_does_not_introduce_digest_drift() -> None:
    first_pack = context_pack(
        source(source_id="CTX-REPO-B", kind=ContextSourceKind.REPOSITORY_FILE),
        source(source_id="CTX-GOV-B", kind=ContextSourceKind.GOVERNANCE_RECORD),
    )
    second_pack = context_pack(
        source(source_id="CTX-GOV-B", kind=ContextSourceKind.GOVERNANCE_RECORD),
        source(source_id="CTX-REPO-B", kind=ContextSourceKind.REPOSITORY_FILE),
    )
    assert first_pack == second_pack
    assert (
        first_assignment(pack=first_pack).input_SHA256
        == first_assignment(pack=second_pack).input_SHA256
    )


def test_one_role_creates_one_assignment() -> None:
    assignments = prepare_ticket_generator_assignments(generation_request())
    assert len(assignments) == 1
    assert assignments[0].role is TicketGeneratorRole.IMPLEMENTATION


def test_multiple_roles_create_canonical_order_assignments() -> None:
    roles = (
        TicketGeneratorRole.IMPLEMENTATION,
        TicketGeneratorRole.ARCHITECTURE,
    )
    assignments = prepare_ticket_generator_assignments(generation_request(roles=roles))
    assert tuple(assignment.role for assignment in assignments) == (
        TicketGeneratorRole.ARCHITECTURE,
        TicketGeneratorRole.IMPLEMENTATION,
    )


def test_role_permutation_produces_identical_assignments_and_digests() -> None:
    roles = (TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION)
    first = prepare_ticket_generator_assignments(generation_request(roles=roles))
    second = prepare_ticket_generator_assignments(
        generation_request(roles=tuple(reversed(roles)))
    )
    assert first == second
    assert tuple(item.assignment_SHA256 for item in first) == tuple(
        item.assignment_SHA256 for item in second
    )


def test_assignment_id_format_is_exact() -> None:
    assert first_assignment().assignment_id == "GEN-P16-2-IMPLEMENTATION"
    gov_ticket = ticket(
        project_id="P15", ticket_id="P15.C3A", ticket_type=TicketType.CLOSURE
    )
    gov_project = project(project_id="P15")
    gov_pack = context_pack(project_spec=gov_project, ticket_spec=gov_ticket)
    gov_assignment = prepare_ticket_generator_assignments(
        TicketGenerationRequest(
            project_spec=gov_project,
            ticket_spec=gov_ticket,
            context_pack=gov_pack,
            roles=(TicketGeneratorRole.GOVERNANCE,),
        )
    )[0]
    assert gov_assignment.assignment_id == "GEN-P15-C3A-GOVERNANCE"


def test_assignment_role_matches_profile_and_ticket_type() -> None:
    assignment = first_assignment()
    assert assignment.role_profile.role is assignment.role
    assert assignment.ticket_type is TicketType.IMPLEMENTATION
    assert assignment.ticket_type in assignment.role_profile.supported_ticket_types


def test_input_digest_is_shared_across_same_request_assignments() -> None:
    assignments = prepare_ticket_generator_assignments(
        generation_request(
            roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION)
        )
    )
    assert len({assignment.input_SHA256 for assignment in assignments}) == 1


def test_assignment_digests_differ_by_role() -> None:
    assignments = prepare_ticket_generator_assignments(
        generation_request(
            roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION)
        )
    )
    assert assignments[0].assignment_SHA256 != assignments[1].assignment_SHA256


def test_same_request_produces_stable_assignments() -> None:
    req = generation_request()
    assert prepare_ticket_generator_assignments(
        req
    ) == prepare_ticket_generator_assignments(req)


def test_assignment_preparation_does_not_mutate_inputs() -> None:
    req = generation_request()
    before = req.model_dump_json()
    prepare_ticket_generator_assignments(req)
    assert req.model_dump_json() == before


def test_assignment_rejects_tampered_digest() -> None:
    data = first_assignment().model_dump(mode="json")
    data["assignment_SHA256"] = "0" * 64
    assert_validation_fails(lambda: GeneratorAssignment.model_validate(data))


def test_assignment_rejects_tampered_assignment_id() -> None:
    data = first_assignment().model_dump(mode="json")
    data["assignment_id"] = "GEN-P16-2-ARCHITECTURE"
    assert_validation_fails(lambda: GeneratorAssignment.model_validate(data))


def test_valid_proposal_construction_succeeds() -> None:
    prop = proposal()
    assert prop.assignment_id == first_assignment().assignment_id
    assert prop.role is TicketGeneratorRole.IMPLEMENTATION
    assert prop.evidence_source_ids == ("CTX-PROJECT-SPEC",)


def test_proposal_identity_and_assignment_binding_are_preserved() -> None:
    assignment = first_assignment()
    prop = proposal(assignment=assignment)
    assert prop.assignment_id == assignment.assignment_id
    assert prop.assignment_SHA256 == assignment.assignment_SHA256
    assert prop.role == assignment.role
    assert prop.project_id == assignment.project_id
    assert prop.ticket_id == assignment.ticket_id


def test_proposal_collections_are_preserved_as_tuples() -> None:
    prop = proposal(
        evidence_source_ids=("CTX-PROJECT-SPEC", "CTX-TICKET-SPEC"),
        assumptions=("Synthetic assumption.",),
        risks=("Synthetic risk.",),
        unresolved_questions=("Synthetic question.",),
    )
    assert prop.evidence_source_ids == ("CTX-PROJECT-SPEC", "CTX-TICKET-SPEC")
    assert prop.assumptions == ("Synthetic assumption.",)
    assert prop.risks == ("Synthetic risk.",)
    assert prop.unresolved_questions == ("Synthetic question.",)


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("evidence_source_ids", ("CTX-PROJECT-SPEC", "CTX-PROJECT-SPEC")),
        ("assumptions", ("Duplicate.", "Duplicate.")),
        ("risks", ("Duplicate.", "Duplicate.")),
        ("unresolved_questions", ("Duplicate.", "Duplicate.")),
    ],
)
def test_duplicate_proposal_collections_fail(
    field_name: str, value: tuple[str, ...]
) -> None:
    data = proposal().model_dump(mode="python")
    data[field_name] = value
    data["proposal_SHA256"] = "0" * 64
    assert_validation_fails(lambda: TicketProposal.model_validate(data))


def test_proposed_project_mismatch_fails() -> None:
    assignment = first_assignment()
    with pytest.raises(TicketProposalValidationError):
        proposal(
            assignment=assignment,
            proposed_ticket=ticket(project_id="P15", ticket_id="P15.2"),
        )


def test_proposed_ticket_mismatch_fails() -> None:
    assignment = first_assignment()
    with pytest.raises(TicketProposalValidationError):
        proposal(assignment=assignment, proposed_ticket=ticket(ticket_id="P16.3"))


def test_proposed_ticket_type_mismatch_fails() -> None:
    assignment = first_assignment()
    with pytest.raises(TicketProposalValidationError):
        proposal(
            assignment=assignment, proposed_ticket=ticket(ticket_type=TicketType.TEST)
        )


def test_same_proposal_produces_same_digest() -> None:
    assignment = first_assignment()
    first = proposal(assignment=assignment)
    second = proposal(assignment=assignment)
    assert first.proposal_SHA256 == second.proposal_SHA256


@pytest.mark.parametrize(
    "overrides",
    [
        {"rationale": "Changed synthetic rationale."},
        {"proposed_ticket": ticket(title="Changed proposal ticket title")},
        {"evidence_source_ids": ("CTX-TICKET-SPEC",)},
        {"assumptions": ("Changed assumption.",)},
        {"risks": ("Changed risk.",)},
        {"unresolved_questions": ("Changed question.",)},
    ],
)
def test_proposal_digest_changes_for_material_fields(
    overrides: dict[str, object],
) -> None:
    base = proposal()
    changed = proposal(**overrides)
    assert base.proposal_SHA256 != changed.proposal_SHA256


def test_proposal_digest_is_lowercase_sha256() -> None:
    digest = proposal().proposal_SHA256
    assert len(digest) == 64
    assert digest == digest.lower()
    assert all(character in "0123456789abcdef" for character in digest)


def test_proposal_digest_excludes_its_own_field() -> None:
    prop = proposal()
    data = prop.__dict__.copy()
    tampered = TicketProposal.model_construct(**{**data, "proposal_SHA256": "0" * 64})
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(generation_request(), tampered)


def test_valid_proposal_validates_against_request() -> None:
    req = generation_request()
    assert validate_ticket_generator_proposal(req, proposal()) == proposal()


def test_unrequested_role_proposal_fails_validation() -> None:
    req = generation_request(roles=(TicketGeneratorRole.IMPLEMENTATION,))
    architecture_assignment = prepare_ticket_generator_assignments(
        generation_request(
            roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION)
        )
    )[0]
    prop = proposal(assignment=architecture_assignment)
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(req, prop)


def test_unknown_assignment_id_fails_validation() -> None:
    prop = proposal()
    tampered = TicketProposal.model_construct(**{
        **prop.__dict__,
        "assignment_id": "GEN-P16-2-ARCHITECTURE",
    })
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(generation_request(), tampered)


def test_wrong_assignment_digest_fails_validation() -> None:
    prop = proposal()
    tampered = TicketProposal.model_construct(**{
        **prop.__dict__,
        "assignment_SHA256": "0" * 64,
    })
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(generation_request(), tampered)


def test_wrong_project_id_fails_validation() -> None:
    prop = proposal()
    tampered = TicketProposal.model_construct(**{**prop.__dict__, "project_id": "P15"})
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(generation_request(), tampered)


def test_wrong_ticket_id_fails_validation() -> None:
    prop = proposal()
    tampered = TicketProposal.model_construct(**{**prop.__dict__, "ticket_id": "P16.3"})
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(generation_request(), tampered)


def test_missing_context_pack_evidence_fails_validation() -> None:
    prop = proposal(evidence_source_ids=("CTX-MISSING-EVIDENCE",))
    with pytest.raises(TicketProposalValidationError):
        validate_ticket_generator_proposal(generation_request(), prop)


@pytest.mark.parametrize("source_id", ["CTX-PROJECT-SPEC", "CTX-TICKET-SPEC"])
def test_reserved_context_pack_evidence_succeeds(source_id: str) -> None:
    req = generation_request()
    assert validate_ticket_generator_proposal(
        req, proposal(evidence_source_ids=(source_id,))
    ).evidence_source_ids == (source_id,)


def test_caller_source_evidence_succeeds() -> None:
    pack = context_pack(source(source_id="CTX-CALLER-EVIDENCE"))
    req = generation_request(pack=pack)
    assignment = prepare_ticket_generator_assignments(req)[0]
    prop = proposal(assignment=assignment, evidence_source_ids=("CTX-CALLER-EVIDENCE",))
    assert validate_ticket_generator_proposal(req, prop) == prop


def test_proposal_validation_does_not_lint_ticket_semantics() -> None:
    loose_ticket = ticket(tasks=("Synthetic task with intentionally broad wording.",))
    assignment = first_assignment(
        ticket_spec=loose_ticket, pack=context_pack(ticket_spec=loose_ticket)
    )
    req = generation_request(
        ticket_spec=loose_ticket, pack=context_pack(ticket_spec=loose_ticket)
    )
    prop = proposal(assignment=assignment, proposed_ticket=loose_ticket)
    assert validate_ticket_generator_proposal(req, prop) == prop


def test_proposal_validation_does_not_approve_or_publish() -> None:
    prop = validate_ticket_generator_proposal(generation_request(), proposal())
    assert not hasattr(prop, "approved")
    assert not hasattr(prop, "published")
    assert not hasattr(prop, "canonical")


def test_request_json_round_trip() -> None:
    req = generation_request()
    assert TicketGenerationRequest.model_validate_json(req.model_dump_json()) == req


def test_assignment_json_round_trip() -> None:
    assignment = first_assignment()
    assert (
        GeneratorAssignment.model_validate_json(assignment.model_dump_json())
        == assignment
    )


def test_proposal_json_round_trip() -> None:
    prop = proposal()
    assert TicketProposal.model_validate_json(prop.model_dump_json()) == prop


def test_enum_values_round_trip() -> None:
    req = TicketGenerationRequest.model_validate(
        generation_request().model_dump(mode="json")
    )
    assert req.roles == (TicketGeneratorRole.IMPLEMENTATION,)


def test_tuples_remain_immutable() -> None:
    req = generation_request()
    prop = proposal()
    with pytest.raises(AttributeError):
        req.roles.append(TicketGeneratorRole.ARCHITECTURE)
    with pytest.raises(AttributeError):
        prop.evidence_source_ids.append("CTX-TICKET-SPEC")


def test_public_model_json_schema_generation() -> None:
    for model_type in PUBLIC_MODELS:
        schema = model_type.model_json_schema()
        assert schema["title"] == model_type.__name__


def test_json_schema_rejects_additional_properties() -> None:
    for model_type in PUBLIC_MODELS:
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
    assert tuple(GeneratorRoleProfile.model_fields) == (
        "role",
        "title",
        "objective",
        "focus_areas",
        "required_checks",
        "prohibited_claims",
        "primary_ticket_types",
        "supported_ticket_types",
    )
    assert tuple(TicketGenerationRequest.model_fields) == (
        "project_spec",
        "ticket_spec",
        "context_pack",
        "roles",
    )
    assert tuple(GeneratorAssignment.model_fields) == (
        "schema_version",
        "assignment_id",
        "role",
        "project_id",
        "ticket_id",
        "ticket_type",
        "input_SHA256",
        "role_profile",
        "assignment_SHA256",
    )
    assert tuple(TicketProposal.model_fields) == (
        "schema_version",
        "assignment_id",
        "assignment_SHA256",
        "role",
        "project_id",
        "ticket_id",
        "proposed_ticket",
        "rationale",
        "evidence_source_ids",
        "assumptions",
        "risks",
        "unresolved_questions",
        "proposal_SHA256",
    )


def test_no_provider_model_prompt_agent_worker_or_scheduler_api_exists() -> None:
    forbidden_names = (
        "ProviderProfile",
        "ModelSelection",
        "PromptTemplate",
        "render_prompt",
        "AgentInstance",
        "Worker",
        "ParallelScheduler",
        "Schedule",
        "run_generator",
        "execute_generator",
    )
    for name in forbidden_names:
        assert not hasattr(ticket_factory, name)


def test_no_dag_linter_synthesis_approval_publication_or_workpacket_exists() -> None:
    forbidden_names = (
        "DependencyGraph",
        "TicketLinter",
        "ProposalSynthesizer",
        "ProposalSet",
        "ApprovalRequest",
        "PublicationRecord",
        "WorkPacket",
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
    )
    for name, value in inspect.getmembers(ticket_factory):
        assert not (callable(value) and name in forbidden)


def test_exception_hierarchy_is_bounded() -> None:
    assert issubclass(TicketGeneratorCompatibilityError, TicketGeneratorRoleError)
    assert issubclass(TicketProposalValidationError, TicketGeneratorRoleError)
    assert issubclass(TicketGeneratorRoleError, ValueError)


def test_error_messages_do_not_echo_ticket_or_context_content() -> None:
    content = "sensitive-context-content-not-for-error"
    pack = context_pack(source(source_id="CTX-PRIVATE-EVIDENCE", content=content))
    req = generation_request(pack=pack)
    assignment = prepare_ticket_generator_assignments(req)[0]
    prop = proposal(
        assignment=assignment, evidence_source_ids=("CTX-MISSING-EVIDENCE",)
    )
    with pytest.raises(TicketProposalValidationError) as exc_info:
        validate_ticket_generator_proposal(req, prop)
    message = str(exc_info.value)
    assert "CTX-MISSING-EVIDENCE" in message
    assert content not in message
    assert req.ticket_spec.objective not in message
