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
    PROJECT_SPEC_SCHEMA_VERSION,
    TICKET_SPEC_SCHEMA_VERSION,
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    DependencyKind,
    DependencyScope,
    ParallelizationHint,
    ProjectSpec,
    RepositoryScopeSpec,
    TicketDependencySpec,
    TicketResponseContractSpec,
    TicketSpec,
    TicketType,
    TicketValidationStepSpec,
)


EXPECTED_EXPORTS = (
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

PUBLIC_MODELS = (
    AuthorityReferenceSpec,
    TicketDependencySpec,
    RepositoryScopeSpec,
    TicketValidationStepSpec,
    TicketResponseContractSpec,
    ProjectSpec,
    TicketSpec,
)


def scope(**overrides: object) -> RepositoryScopeSpec:
    data = {
        "allowed_paths": ("2_products/pepper-agent/hermes_cli/**",),
        "forbidden_paths": ("4_external/sources/**",),
        "allowed_actions": ("edit planning schema",),
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
        "ticket_id": "P16.1",
        "kind": DependencyKind.SOFT_PREDECESSOR,
        "scope": DependencyScope.INTERNAL_PROJECT,
        "rationale": "Synthetic dependency declaration.",
    }
    data.update(overrides)
    return TicketDependencySpec.model_validate(data)


def project_data(**overrides: object) -> object:
    data = {
        "project_id": "P16",
        "title": "Synthetic planning project",
        "objective": "Define synthetic immutable planning contracts.",
        "summary": "This synthetic project validates planning schema behavior only.",
        "context": ("A synthetic context entry describes the planning boundary.",),
        "authority_references": (authority(),),
        "scope": scope(),
        "constraints": ("No execution behavior is authorized.",),
        "non_goals": ("Ticket generation is deferred.",),
        "acceptance_criteria": ("The project contract validates declarative data.",),
        "completion_verdict": "synthetic_project_ready",
    }
    data.update(overrides)
    return data


def project(**overrides: object) -> ProjectSpec:
    return ProjectSpec.model_validate(project_data(**overrides))


def ticket_data(**overrides: object) -> object:
    data = {
        "project_id": "P16",
        "ticket_id": "P16.0",
        "title": "Synthetic schema ticket",
        "ticket_type": TicketType.IMPLEMENTATION,
        "objective": "Define synthetic ticket schema data.",
        "context": ("A synthetic context entry describes ticket planning.",),
        "authority_references": (authority(),),
        "dependencies": (dependency(ticket_id="P16.2"),),
        "scope": scope(),
        "constraints": ("Validation commands remain inert text.",),
        "tasks": ("Create immutable schema contracts.",),
        "acceptance_criteria": ("The ticket contract validates local invariants.",),
        "validation_steps": (validation_step(),),
        "response_contract": response_contract(),
        "recommended_commit_message": "P16.0 Add synthetic schemas",
    }
    data.update(overrides)
    return data


def ticket(**overrides: object) -> TicketSpec:
    return TicketSpec.model_validate(ticket_data(**overrides))


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


def test_package_imports_and_exports_supported_surface() -> None:
    assert isinstance(ticket_factory.__all__, tuple)
    assert len(ticket_factory.__all__) == len(set(ticket_factory.__all__))
    assert set(EXPECTED_EXPORTS).issubset(set(ticket_factory.__all__))
    preserved_order = tuple(
        exported_name
        for exported_name in ticket_factory.__all__
        if exported_name in EXPECTED_EXPORTS
    )
    assert preserved_order == EXPECTED_EXPORTS
    for exported_name in EXPECTED_EXPORTS:
        assert hasattr(ticket_factory, exported_name)
    assert "ShortText" not in ticket_factory.__all__


def test_import_has_no_runtime_or_provider_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package_names = (
        "hermes_cli.agent_platform.ticket_factory",
        "hermes_cli.agent_platform.ticket_factory.specs",
    )
    before_modules = set(sys.modules)
    for package_name in package_names:
        sys.modules.pop(package_name, None)

    def fail_socket(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)
    imported = importlib.import_module("hermes_cli.agent_platform.ticket_factory")
    assert imported.ProjectSpec.__name__ == "ProjectSpec"
    new_modules = set(sys.modules) - before_modules
    assert not any(name.startswith("providers") for name in new_modules)
    assert not any(name.startswith("agent.") for name in new_modules)
    assert not any("provider_runtime" in name for name in new_modules)
    assert not any("provider_worker" in name for name in new_modules)
    assert not any("runtime_adapter" in name for name in new_modules)


def test_project_spec_schema_version_defaults_to_one() -> None:
    assert PROJECT_SPEC_SCHEMA_VERSION == 1
    assert project().schema_version == 1


def test_ticket_spec_schema_version_defaults_to_one() -> None:
    assert TICKET_SPEC_SCHEMA_VERSION == 1
    assert ticket().schema_version == 1


def test_alternative_schema_versions_are_rejected() -> None:
    assert_validation_fails(lambda: project(schema_version=2))
    assert_validation_fails(lambda: ticket(schema_version=2))


@pytest.mark.parametrize("project_id", ["P1", "P16", "P999", "PEPPER"])
def test_accepted_project_identifiers_pass(project_id: str) -> None:
    assert project(project_id=project_id).project_id == project_id


@pytest.mark.parametrize("project_id", ["p16", "16", "P0", "P16.0", "P-16", "P16/"])
def test_rejected_project_identifiers_fail(project_id: str) -> None:
    assert_validation_fails(lambda: project(project_id=project_id))


@pytest.mark.parametrize("ticket_id", ["P16.0", "P16.1", "P16.0A", "P16.R", "P16.CR"])
def test_accepted_ticket_identifiers_pass(ticket_id: str) -> None:
    assert ticket(ticket_id=ticket_id).ticket_id == ticket_id


def test_accepted_cross_project_ticket_identifier_passes_dependency_contract() -> None:
    assert dependency(ticket_id="P15.C3A").ticket_id == "P15.C3A"


@pytest.mark.parametrize(
    "ticket_id", ["P16", "p16.0", "P16.", "P16..0", "P16-0", "P0.1", "P16/0"]
)
def test_rejected_ticket_identifiers_fail(ticket_id: str) -> None:
    assert_validation_fails(lambda: ticket(ticket_id=ticket_id))


def test_project_ticket_prefix_mismatch_fails() -> None:
    assert_validation_fails(lambda: ticket(project_id="P15", ticket_id="P16.0"))


def test_product_project_accepts_governed_macroproject_ticket_namespace() -> None:
    assert ticket(project_id="PEPPER", ticket_id="P18.2").ticket_id == "P18.2"


def test_product_project_rejects_product_id_as_ticket_namespace() -> None:
    assert_validation_fails(lambda: ticket(project_id="PEPPER", ticket_id="PEPPER.2"))


def test_whitespace_identifier_is_rejected_without_rewrite() -> None:
    assert_validation_fails(lambda: project(project_id=" P16"))
    assert_validation_fails(lambda: ticket(ticket_id="P16.0 "))


@pytest.mark.parametrize("model_type", PUBLIC_MODELS)
def test_every_public_model_is_frozen(model_type: type) -> None:
    assert model_type.model_config["frozen"] is True
    assert model_type.model_config["extra"] == "forbid"


def test_unknown_top_level_fields_fail() -> None:
    assert_validation_fails(lambda: project(unexpected="value"))


def test_unknown_nested_fields_fail() -> None:
    assert_validation_fails(
        lambda: RepositoryScopeSpec.model_validate({
            "allowed_paths": ["README.md"],
            "forbidden_paths": [],
            "allowed_actions": [],
            "forbidden_actions": [],
            "unexpected": "value",
        })
    )


def test_mutable_input_sequences_are_stored_as_tuples() -> None:
    spec = ticket(
        context=["Context."],
        tasks=["Task."],
        acceptance_criteria=["Done."],
        validation_steps=[validation_step()],
    )
    assert isinstance(spec.context, tuple)
    assert isinstance(spec.tasks, tuple)
    assert isinstance(spec.acceptance_criteria, tuple)
    assert isinstance(spec.validation_steps, tuple)


def test_frozen_model_rejects_assignment() -> None:
    spec = project()
    with pytest.raises(ValidationError):
        spec.title = "changed"


def test_whitespace_only_text_fails() -> None:
    assert_validation_fails(lambda: project(title="   "))


def test_nul_text_fails() -> None:
    assert_validation_fails(lambda: project(summary="bad\x00text"))


def test_oversized_text_fails() -> None:
    assert_validation_fails(lambda: project(title="x" * 513))
    assert_validation_fails(lambda: project(objective="x" * 8193))


@pytest.mark.parametrize("completion_verdict", ["Bad", "bad token", "bad-token"])
def test_invalid_verdict_forms_fail(completion_verdict: str) -> None:
    assert_validation_fails(lambda: project(completion_verdict=completion_verdict))


@pytest.mark.parametrize(
    "path",
    [
        "README.md",
        "0_architecture/governance/**",
        "2_products/pepper-agent/hermes_cli/**",
        ".gitignore",
    ],
)
def test_repository_paths_accept_relative_forward_slash_and_globs(path: str) -> None:
    assert scope(allowed_paths=(path,)).allowed_paths == (path,)


@pytest.mark.parametrize(
    "path",
    [
        "C:\\repo\\file.py",
        "/absolute/path",
        "../outside",
        "folder/../../outside",
        "folder\\file.py",
        "file:`0",
    ],
)
def test_repository_paths_reject_absolute_windows_backslash_parent_and_bounded_forms(
    path: str,
) -> None:
    assert_validation_fails(lambda: scope(allowed_paths=(path,)))


def test_repository_path_existence_is_not_checked() -> None:
    missing = "synthetic/path/that/does/not/exist.md"
    assert scope(allowed_paths=(missing,)).allowed_paths == (missing,)


def test_duplicate_context_fails() -> None:
    assert_validation_fails(lambda: project(context=("Duplicate.", "Duplicate.")))


def test_duplicate_authority_reference_fails() -> None:
    item = authority()
    assert_validation_fails(lambda: project(authority_references=(item, item)))


def test_duplicate_scope_entry_fails() -> None:
    assert_validation_fails(lambda: scope(allowed_paths=("README.md", "README.md")))


def test_duplicate_dependency_fails() -> None:
    first = dependency(ticket_id="P16.1")
    second = dependency(ticket_id="P16.1", kind=DependencyKind.HARD_PREREQUISITE)
    assert_validation_fails(lambda: ticket(dependencies=(first, second)))


def test_duplicate_task_fails() -> None:
    assert_validation_fails(lambda: ticket(tasks=("Task.", "Task.")))


def test_duplicate_acceptance_criterion_fails() -> None:
    assert_validation_fails(lambda: ticket(acceptance_criteria=("Done.", "Done.")))


def test_duplicate_validation_id_fails() -> None:
    first = validation_step(validation_id="V1")
    second = validation_step(validation_id="V1", description="Second validation.")
    assert_validation_fails(lambda: ticket(validation_steps=(first, second)))


def test_duplicate_response_section_fails() -> None:
    assert_validation_fails(
        lambda: response_contract(required_sections=("Summary", "Summary"))
    )


def test_self_dependency_fails() -> None:
    assert_validation_fails(
        lambda: ticket(dependencies=(dependency(ticket_id="P16.0"),))
    )


def test_unknown_external_dependency_remains_declarative_data() -> None:
    external = dependency(ticket_id="P99.1", scope=DependencyScope.EXTERNAL_PROJECT)
    spec = ticket(dependencies=(external,))
    assert spec.dependencies[0].ticket_id == "P99.1"


def test_no_dependency_resolution_surface_exists() -> None:
    assert not hasattr(ticket_factory, "DependencyGraph")
    assert not hasattr(ticket_factory, "resolve_dependencies")
    assert not hasattr(ticket_factory, "topological_sort")


def test_parallelization_default_is_unspecified() -> None:
    assert (
        ticket(dependencies=()).parallelization_hint is ParallelizationHint.UNSPECIFIED
    )


def test_parallelization_enum_values_serialize_correctly() -> None:
    for hint in ParallelizationHint:
        assert (
            ticket(parallelization_hint=hint).model_dump(mode="json")[
                "parallelization_hint"
            ]
            == hint.value
        )


def test_no_scheduling_or_execution_object_exists() -> None:
    forbidden_names = (
        "ExecutionLane",
        "Schedule",
        "Scheduler",
        "WorkPacket",
        "AgentAssignment",
    )
    for name in forbidden_names:
        assert not hasattr(ticket_factory, name)


def test_none_validation_command_is_accepted() -> None:
    assert validation_step(command=None).command is None


def test_inert_command_text_round_trips_without_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def mark_called(*_args: object, **_kwargs: object) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(socket, "socket", mark_called)
    command = "python synthetic_validation.py"
    step = validation_step(command=command)
    assert (
        TicketValidationStepSpec.model_validate_json(step.model_dump_json()).command
        == command
    )
    assert called is False


def test_project_spec_json_round_trip() -> None:
    spec = project()
    assert ProjectSpec.model_validate_json(spec.model_dump_json()) == spec


def test_ticket_spec_json_round_trip() -> None:
    spec = ticket()
    assert TicketSpec.model_validate_json(spec.model_dump_json()) == spec


def test_enum_values_round_trip() -> None:
    spec = ticket(
        ticket_type=TicketType.TEST, parallelization_hint=ParallelizationHint.SERIAL
    )
    payload = spec.model_dump(mode="json")
    assert payload["ticket_type"] == "test"
    assert payload["parallelization_hint"] == "serial"
    assert TicketSpec.model_validate(payload).ticket_type is TicketType.TEST


def test_tuples_remain_immutable_after_validation() -> None:
    spec = ticket()
    with pytest.raises(AttributeError):
        spec.tasks.append("new task")


def test_project_spec_json_schema_generation() -> None:
    schema = ProjectSpec.model_json_schema()
    assert schema["title"] == "ProjectSpec"
    assert "AuthorityReferenceSpec" in schema["$defs"]


def test_ticket_spec_json_schema_generation() -> None:
    schema = TicketSpec.model_json_schema()
    assert schema["title"] == "TicketSpec"
    assert "TicketDependencySpec" in schema["$defs"]
    assert "TicketType" in schema["$defs"]


def test_json_schema_rejects_additional_properties() -> None:
    for model_type in PUBLIC_MODELS:
        schema = model_type.model_json_schema()
        assert schema["additionalProperties"] is False


def test_json_schema_contains_no_unrestricted_object_schema() -> None:
    for model_type in (ProjectSpec, TicketSpec):
        for node in walk_schema_nodes(model_type.model_json_schema()):
            if isinstance(node, dict) and node.get("type") == "object":
                assert node.get("additionalProperties") is False
                assert "properties" in node


def test_fixed_version_visible_in_json_schema() -> None:
    assert ProjectSpec.model_json_schema()["properties"]["schema_version"]["const"] == 1
    assert TicketSpec.model_json_schema()["properties"]["schema_version"]["const"] == 1


def test_schema_generation_is_deterministic_in_process() -> None:
    assert ProjectSpec.model_json_schema() == ProjectSpec.model_json_schema()
    assert TicketSpec.model_json_schema() == TicketSpec.model_json_schema()


def test_no_public_any_annotations() -> None:
    for model_type in PUBLIC_MODELS:
        for field in model_type.model_fields.values():
            assert not annotation_contains_forbidden(field.annotation)


def test_no_mapping_payload_fields() -> None:
    for model_type in PUBLIC_MODELS:
        for field in model_type.model_fields.values():
            assert get_origin(field.annotation) is not dict


def test_no_file_loading_functions_exist() -> None:
    forbidden = (
        "load",
        "load_json",
        "load_file",
        "from_file",
        "save",
        "save_json",
        "write_file",
    )
    for name, value in inspect.getmembers(ticket_factory):
        assert not (callable(value) and name in forbidden)


def test_no_command_execution_functions_exist() -> None:
    forbidden = ("execute", "run", "run_command", "invoke", "dispatch")
    for name, value in inspect.getmembers(ticket_factory):
        assert not (callable(value) and name in forbidden)


def test_no_workpacket_or_runtime_state_types_exist() -> None:
    forbidden = (
        "WorkPacket",
        "ExecutionRun",
        "ExecutionCommand",
        "RuntimeState",
        "ApprovalRequest",
    )
    for name in forbidden:
        assert not hasattr(ticket_factory, name)


def test_boolean_fields_are_strict() -> None:
    assert_validation_fails(lambda: authority(required="true"))
    assert_validation_fails(lambda: validation_step(required=1))
    assert_validation_fails(lambda: response_contract(include_tests_run="yes"))


def test_required_collections_are_non_empty() -> None:
    assert_validation_fails(lambda: project(context=()))
    assert_validation_fails(lambda: ticket(tasks=()))
    assert_validation_fails(lambda: ticket(validation_steps=()))


def test_optional_collections_may_be_empty() -> None:
    spec = ticket(authority_references=(), dependencies=(), constraints=())
    assert spec.authority_references == ()
    assert spec.dependencies == ()
    assert spec.constraints == ()


def test_response_contract_default_flags_are_true() -> None:
    contract = response_contract()
    assert contract.include_files_inspected is True
    assert contract.include_files_modified is True
    assert contract.include_commands_run is True
    assert contract.include_tests_run is True
    assert contract.include_limitations is True


def test_public_enums_expose_exact_values() -> None:
    assert tuple(item.value for item in TicketType) == (
        "architecture",
        "documentation",
        "implementation",
        "refactor",
        "test",
        "bugfix",
        "integration",
        "closure",
    )
    assert tuple(item.value for item in DependencyKind) == (
        "hard_prerequisite",
        "soft_predecessor",
    )
    assert tuple(item.value for item in DependencyScope) == (
        "internal_project",
        "external_project",
    )
    assert tuple(item.value for item in ParallelizationHint) == (
        "unspecified",
        "serial",
        "parallel_candidate",
    )
    assert tuple(item.value for item in AuthorityReferenceKind) == (
        "ticket",
        "governance_record",
        "repository_path",
        "commit",
        "external_source",
    )


def test_public_enums_have_no_aliases() -> None:
    for enum_type in (
        TicketType,
        DependencyKind,
        DependencyScope,
        ParallelizationHint,
        AuthorityReferenceKind,
    ):
        assert len(enum_type.__members__) == len(tuple(enum_type))
        assert issubclass(enum_type, Enum)


def test_project_spec_field_order() -> None:
    assert tuple(ProjectSpec.model_fields) == (
        "schema_version",
        "project_id",
        "title",
        "objective",
        "summary",
        "context",
        "authority_references",
        "scope",
        "constraints",
        "non_goals",
        "acceptance_criteria",
        "completion_verdict",
    )


def test_ticket_spec_field_order() -> None:
    assert tuple(TicketSpec.model_fields) == (
        "schema_version",
        "project_id",
        "ticket_id",
        "title",
        "ticket_type",
        "objective",
        "context",
        "authority_references",
        "dependencies",
        "parallelization_hint",
        "scope",
        "constraints",
        "tasks",
        "acceptance_criteria",
        "validation_steps",
        "response_contract",
        "recommended_commit_message",
    )
