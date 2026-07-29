import hashlib
import importlib
import inspect
import json
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
    OptionalSourceOverflowStrategy,
    ProjectSpec,
    RepositoryScopeSpec,
    TicketDependencySpec,
    TicketResponseContractSpec,
    TicketSpec,
    TicketType,
    TicketValidationStepSpec,
    assemble_context_pack,
)


EXPECTED_P16_1_EXPORTS = (
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

PUBLIC_CONTEXT_MODELS = (
    ContextSourceSpec,
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPackItem,
    ContextPack,
)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def scope(**overrides: object) -> RepositoryScopeSpec:
    data = {
        "allowed_paths": ("2_products/pepper-agent/hermes_cli/**",),
        "forbidden_paths": ("4_external/sources/**",),
        "allowed_actions": ("edit planning context contracts",),
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
        "summary": "This synthetic project validates context pack behavior only.",
        "context": ("A synthetic context entry describes the planning boundary.",),
        "authority_references": (authority(),),
        "scope": scope(),
        "constraints": ("No execution behavior is authorized.",),
        "non_goals": ("Ticket generation remains deferred.",),
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
        "ticket_id": "P16.1",
        "title": "Synthetic context pack ticket",
        "ticket_type": TicketType.IMPLEMENTATION,
        "objective": "Define synthetic context pack assembly data.",
        "context": ("A synthetic context entry describes ticket planning.",),
        "authority_references": (authority(),),
        "dependencies": (dependency(),),
        "scope": scope(),
        "constraints": ("Validation commands remain inert text.",),
        "tasks": ("Create immutable context pack contracts.",),
        "acceptance_criteria": ("The context pack validates local invariants.",),
        "validation_steps": (validation_step(),),
        "response_contract": response_contract(),
        "recommended_commit_message": "P16.1 Add synthetic context packs",
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
        "title": "Synthetic context source",
        "source_reference": f"{kind_value}:{source_id}",
        "content": f"Synthetic caller supplied content for {source_id}.",
        "authority_references": (),
        "sensitivity": ContextSensitivity.INTERNAL,
        "priority": ContextPriority.NORMAL,
        "required": False,
    }
    data.update(overrides)
    return ContextSourceSpec.model_validate(data)


def request(
    *sources: ContextSourceSpec,
    project_spec: ProjectSpec | None = None,
    ticket_spec: TicketSpec | None = None,
    policy: ContextAssemblyPolicy | None = None,
) -> ContextAssemblyRequest:
    return ContextAssemblyRequest.model_validate({
        "project_spec": project_spec or project(),
        "ticket_spec": ticket_spec or ticket(),
        "sources": sources,
        "policy": policy or ContextAssemblyPolicy(),
    })


def pack(
    *sources: ContextSourceSpec, policy: ContextAssemblyPolicy | None = None
) -> ContextPack:
    return assemble_context_pack(request(*sources, policy=policy))


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


def test_package_imports_and_exports_context_pack_surface() -> None:
    assert isinstance(ticket_factory.__all__, tuple)
    assert len(ticket_factory.__all__) == len(set(ticket_factory.__all__))
    assert set(EXPECTED_P16_1_EXPORTS).issubset(set(ticket_factory.__all__))
    preserved_order = tuple(
        exported_name
        for exported_name in ticket_factory.__all__
        if exported_name in EXPECTED_P16_1_EXPORTS
    )
    assert preserved_order == EXPECTED_P16_1_EXPORTS
    for exported_name in EXPECTED_P16_1_EXPORTS:
        assert hasattr(ticket_factory, exported_name)
    assert "CONTEXT_PACK_DIGEST_ALGORITHM" not in ticket_factory.__all__


def test_context_pack_import_has_no_runtime_or_provider_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package_names = (
        "hermes_cli.agent_platform.ticket_factory",
        "hermes_cli.agent_platform.ticket_factory.context_packs",
        "hermes_cli.agent_platform.ticket_factory.specs",
    )
    before_modules = set(sys.modules)
    for package_name in package_names:
        sys.modules.pop(package_name, None)

    def fail_socket(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)
    imported = importlib.import_module("hermes_cli.agent_platform.ticket_factory")
    assert imported.ContextPack.__name__ == "ContextPack"
    new_modules = set(sys.modules) - before_modules
    assert not any(name.startswith("providers") for name in new_modules)
    assert not any(name.startswith("agent.") for name in new_modules)
    assert not any("provider_runtime" in name for name in new_modules)
    assert not any("provider_worker" in name for name in new_modules)
    assert not any("runtime_adapter" in name for name in new_modules)


def test_context_pack_schema_version_defaults_to_one() -> None:
    assembled = pack()
    assert CONTEXT_PACK_SCHEMA_VERSION == 1
    assert assembled.schema_version == 1


def test_alternative_context_pack_schema_versions_are_rejected() -> None:
    payload = pack().model_dump(mode="json")
    payload["schema_version"] = 2
    assert_validation_fails(lambda: ContextPack.model_validate(payload))


@pytest.mark.parametrize("source_id", ["CTX-A", "CTX-P16-GOV", "CTX-SOURCE-123"])
def test_accepted_source_identifiers_pass(source_id: str) -> None:
    assert source(source_id=source_id).source_id == source_id


@pytest.mark.parametrize(
    "source_id",
    [
        "CTX",
        "ctx-GOV-A",
        "CTX-GOV_A",
        "CTX-GOV/A",
        "CTX-GOV A",
        " CTX-GOV-A",
        "CTX-PROJECT-SPEC",
        "CTX-TICKET-SPEC",
    ],
)
def test_rejected_source_identifiers_fail(source_id: str) -> None:
    assert_validation_fails(lambda: source(source_id=source_id))


@pytest.mark.parametrize(
    "kind", [ContextSourceKind.PROJECT_SPEC, ContextSourceKind.TICKET_SPEC]
)
def test_assembler_owned_source_kinds_are_rejected_for_caller_sources(
    kind: ContextSourceKind,
) -> None:
    assert_validation_fails(lambda: source(kind=kind))


def test_request_rejects_project_ticket_mismatch() -> None:
    assert_validation_fails(
        lambda: request(project_spec=project(project_id="P15"), ticket_spec=ticket())
    )


def test_request_rejects_duplicate_source_ids() -> None:
    first = source(source_id="CTX-DUP-A", source_reference="ref:first")
    second = source(source_id="CTX-DUP-A", source_reference="ref:second")
    assert_validation_fails(lambda: request(first, second))


def test_request_rejects_duplicate_source_kind_reference_pairs() -> None:
    first = source(
        source_id="CTX-DUP-A",
        kind=ContextSourceKind.REPOSITORY_FILE,
        source_reference="2_products/pepper-agent/README.md",
    )
    second = source(
        source_id="CTX-DUP-B",
        kind=ContextSourceKind.REPOSITORY_FILE,
        source_reference="2_products/pepper-agent/README.md",
    )
    assert_validation_fails(lambda: request(first, second))


def test_source_rejects_duplicate_authority_reference_pairs() -> None:
    item = authority()
    assert_validation_fails(lambda: source(authority_references=(item, item)))


def test_context_pack_exceptions_have_bounded_hierarchy() -> None:
    assert issubclass(ContextPackBudgetError, ContextPackAssemblyError)
    assert issubclass(ContextPackSensitiveContentError, ContextPackAssemblyError)
    assert issubclass(ContextPackAssemblyError, ValueError)


@pytest.mark.parametrize("model_type", PUBLIC_CONTEXT_MODELS)
def test_every_public_context_model_is_frozen(model_type: type) -> None:
    assert model_type.model_config["frozen"] is True
    assert model_type.model_config["extra"] == "forbid"


def test_unknown_context_pack_fields_fail() -> None:
    payload = source().model_dump(mode="json")
    payload["unexpected"] = "value"
    assert_validation_fails(lambda: ContextSourceSpec.model_validate(payload))


def test_frozen_context_model_rejects_assignment() -> None:
    item = source()
    with pytest.raises(ValidationError):
        item.title = "changed"


def test_mutable_context_input_sequences_are_stored_as_tuples() -> None:
    context_source = ContextSourceSpec.model_validate({
        "source_id": "CTX-LIST-A",
        "kind": "governance_record",
        "title": "Synthetic list source",
        "source_reference": "governance:CTX-LIST-A",
        "content": "Synthetic list content.",
        "authority_references": [authority()],
    })
    assembly_request = ContextAssemblyRequest.model_validate({
        "project_spec": project(),
        "ticket_spec": ticket(),
        "sources": [context_source],
    })
    assembled = assemble_context_pack(assembly_request)
    assert isinstance(context_source.authority_references, tuple)
    assert isinstance(assembly_request.sources, tuple)
    assert isinstance(assembled.items, tuple)
    assert isinstance(assembled.items[2].authority_references, tuple)


def test_context_source_text_constraints_are_bounded() -> None:
    assert source(title="  Trimmed title  ").title == "Trimmed title"
    assert_validation_fails(lambda: source(title="   "))
    assert_validation_fails(lambda: source(content="bad\x00text"))
    assert_validation_fails(lambda: source(content="x" * 32769))


def test_context_assembly_policy_defaults_and_bounds() -> None:
    policy = ContextAssemblyPolicy()
    assert policy.max_items == 32
    assert policy.max_total_characters == 65536
    assert policy.max_item_characters == 16384
    assert (
        policy.optional_overflow_strategy
        is OptionalSourceOverflowStrategy.TRUNCATE_THEN_OMIT
    )
    assert_validation_fails(
        lambda: ContextAssemblyPolicy(
            max_total_characters=4096, max_item_characters=4097
        )
    )


def test_context_source_enum_values_serialize_correctly() -> None:
    assert tuple(item.value for item in ContextSourceKind) == (
        "project_spec",
        "ticket_spec",
        "governance_record",
        "repository_file",
        "external_source",
        "human_instruction",
        "historical_ticket",
    )
    assert tuple(item.value for item in ContextSensitivity) == (
        "public",
        "internal",
        "sensitive",
        "secret",
    )
    assert tuple(item.value for item in ContextPriority) == (
        "critical",
        "high",
        "normal",
        "low",
    )
    assert tuple(item.value for item in OptionalSourceOverflowStrategy) == (
        "reject",
        "truncate_then_omit",
        "omit",
    )


def test_context_enums_have_no_aliases() -> None:
    for enum_type in (
        ContextSourceKind,
        ContextSensitivity,
        ContextPriority,
        OptionalSourceOverflowStrategy,
    ):
        assert len(enum_type.__members__) == len(tuple(enum_type))
        assert issubclass(enum_type, Enum)


def test_context_source_spec_field_order() -> None:
    assert tuple(ContextSourceSpec.model_fields) == (
        "source_id",
        "kind",
        "title",
        "source_reference",
        "content",
        "authority_references",
        "sensitivity",
        "priority",
        "required",
    )


def test_context_assembly_policy_field_order() -> None:
    assert tuple(ContextAssemblyPolicy.model_fields) == (
        "max_items",
        "max_total_characters",
        "max_item_characters",
        "optional_overflow_strategy",
    )


def test_context_assembly_request_field_order() -> None:
    assert tuple(ContextAssemblyRequest.model_fields) == (
        "project_spec",
        "ticket_spec",
        "sources",
        "policy",
    )


def test_context_pack_item_field_order() -> None:
    assert tuple(ContextPackItem.model_fields) == (
        "source_id",
        "kind",
        "title",
        "source_reference",
        "authority_references",
        "sensitivity",
        "priority",
        "required",
        "content",
        "original_character_count",
        "included_character_count",
        "truncated",
        "source_SHA256",
        "included_SHA256",
    )


def test_context_pack_field_order() -> None:
    assert tuple(ContextPack.model_fields) == (
        "schema_version",
        "project_id",
        "ticket_id",
        "items",
        "omitted_source_ids",
        "truncated_source_ids",
        "total_included_characters",
        "policy",
        "context_pack_SHA256",
    )


def test_assemble_context_pack_materializes_project_and_ticket_first() -> None:
    project_spec = project()
    ticket_spec = ticket()
    assembled = assemble_context_pack(
        request(project_spec=project_spec, ticket_spec=ticket_spec)
    )
    assert tuple(item.source_id for item in assembled.items) == (
        "CTX-PROJECT-SPEC",
        "CTX-TICKET-SPEC",
    )
    project_item, ticket_item = assembled.items
    expected_project_content = deterministic_json(project_spec.model_dump(mode="json"))
    expected_ticket_content = deterministic_json(ticket_spec.model_dump(mode="json"))
    assert project_item.kind is ContextSourceKind.PROJECT_SPEC
    assert ticket_item.kind is ContextSourceKind.TICKET_SPEC
    assert project_item.content == expected_project_content
    assert ticket_item.content == expected_ticket_content
    assert project_item.source_SHA256 == sha256_text(expected_project_content)
    assert project_item.included_SHA256 == project_item.source_SHA256
    assert ticket_item.source_SHA256 == sha256_text(expected_ticket_content)
    assert ticket_item.included_SHA256 == ticket_item.source_SHA256
    assert project_item.authority_references == project_spec.authority_references
    assert ticket_item.authority_references == ticket_spec.authority_references
    assert assembled.omitted_source_ids == ()
    assert assembled.truncated_source_ids == ()
    assert assembled.total_included_characters == sum(
        item.included_character_count for item in assembled.items
    )
    assert len(assembled.context_pack_SHA256) == 64
    assert assembled.context_pack_SHA256 == assembled.context_pack_SHA256.lower()


def test_caller_sources_are_sorted_deterministically_after_reserved_items() -> None:
    sources = (
        source(
            source_id="CTX-EXT-A",
            kind=ContextSourceKind.EXTERNAL_SOURCE,
            priority=ContextPriority.LOW,
            required=True,
        ),
        source(
            source_id="CTX-REPO-C",
            kind=ContextSourceKind.REPOSITORY_FILE,
            priority=ContextPriority.NORMAL,
        ),
        source(
            source_id="CTX-HUMAN-A",
            kind=ContextSourceKind.HUMAN_INSTRUCTION,
            priority=ContextPriority.CRITICAL,
            required=True,
        ),
        source(
            source_id="CTX-GOV-B",
            kind=ContextSourceKind.GOVERNANCE_RECORD,
            priority=ContextPriority.HIGH,
        ),
        source(
            source_id="CTX-REPO-A",
            kind=ContextSourceKind.REPOSITORY_FILE,
            priority=ContextPriority.CRITICAL,
            required=True,
        ),
        source(
            source_id="CTX-GOV-A",
            kind=ContextSourceKind.GOVERNANCE_RECORD,
            priority=ContextPriority.CRITICAL,
            required=True,
        ),
    )
    assembled = pack(*sources)
    assert tuple(item.source_id for item in assembled.items) == (
        "CTX-PROJECT-SPEC",
        "CTX-TICKET-SPEC",
        "CTX-GOV-A",
        "CTX-REPO-A",
        "CTX-HUMAN-A",
        "CTX-EXT-A",
        "CTX-GOV-B",
        "CTX-REPO-C",
    )


def test_context_pack_digest_is_independent_of_input_source_order() -> None:
    sources = (
        source(source_id="CTX-REPO-A", kind=ContextSourceKind.REPOSITORY_FILE),
        source(source_id="CTX-GOV-A", kind=ContextSourceKind.GOVERNANCE_RECORD),
        source(source_id="CTX-HUMAN-A", kind=ContextSourceKind.HUMAN_INSTRUCTION),
    )
    first = pack(*sources)
    second = pack(*reversed(sources))
    assert first.context_pack_SHA256 == second.context_pack_SHA256
    assert first.model_dump_json() == second.model_dump_json()


def test_equal_rank_caller_sources_are_ordered_by_source_id() -> None:
    sources = (
        source(source_id="CTX-RANK-C", kind=ContextSourceKind.REPOSITORY_FILE),
        source(source_id="CTX-RANK-A", kind=ContextSourceKind.REPOSITORY_FILE),
        source(source_id="CTX-RANK-B", kind=ContextSourceKind.REPOSITORY_FILE),
    )
    assembled = pack(*sources)
    assert tuple(item.source_id for item in assembled.items[2:]) == (
        "CTX-RANK-A",
        "CTX-RANK-B",
        "CTX-RANK-C",
    )


def test_policy_change_changes_context_pack_digest_with_same_items() -> None:
    first = pack(policy=ContextAssemblyPolicy())
    second = pack(policy=ContextAssemblyPolicy(max_total_characters=65537))
    assert first.items == second.items
    assert first.omitted_source_ids == second.omitted_source_ids == ()
    assert first.truncated_source_ids == second.truncated_source_ids == ()
    assert first.total_included_characters == second.total_included_characters
    assert first.policy != second.policy
    assert first.context_pack_SHA256 != second.context_pack_SHA256


def test_required_sources_are_never_truncated_or_omitted() -> None:
    required_source = source(
        source_id="CTX-REQUIRED-A",
        content="x" * 4097,
        required=True,
    )
    policy = ContextAssemblyPolicy(max_item_characters=4096)
    with pytest.raises(ContextPackBudgetError) as exc_info:
        pack(required_source, policy=policy)
    message = str(exc_info.value)
    assert "CTX-REQUIRED-A" in message
    assert "max_item_characters" in message
    assert "x" * 4097 not in message


def test_required_total_budget_overflow_fails_with_bounded_error() -> None:
    required_source = source(
        source_id="CTX-REQUIRED-TOTAL",
        content="y" * 4096,
        required=True,
    )
    policy = ContextAssemblyPolicy(max_total_characters=4096, max_item_characters=4096)
    with pytest.raises(ContextPackBudgetError) as exc_info:
        pack(required_source, policy=policy)
    message = str(exc_info.value)
    assert "CTX-REQUIRED-TOTAL" in message
    assert "max_total_characters" in message
    assert "y" * 4096 not in message


def test_generated_project_source_item_budget_error_is_bounded() -> None:
    policy = ContextAssemblyPolicy(max_item_characters=256)
    project_spec = project()
    with pytest.raises(ContextPackBudgetError) as exc_info:
        assemble_context_pack(request(project_spec=project_spec, policy=policy))
    message = str(exc_info.value)
    assert "CTX-PROJECT-SPEC" in message
    assert "max_item_characters" in message
    assert project_spec.title not in message
    assert project_spec.summary not in message
    assert project_spec.context[0] not in message


def test_optional_sources_are_omitted_when_max_items_is_exhausted() -> None:
    first = source(source_id="CTX-OPTIONAL-A", priority=ContextPriority.HIGH)
    second = source(source_id="CTX-OPTIONAL-B", priority=ContextPriority.LOW)
    assembled = pack(first, second, policy=ContextAssemblyPolicy(max_items=3))
    assert tuple(item.source_id for item in assembled.items) == (
        "CTX-PROJECT-SPEC",
        "CTX-TICKET-SPEC",
        "CTX-OPTIONAL-A",
    )
    assert assembled.omitted_source_ids == ("CTX-OPTIONAL-B",)
    assert assembled.truncated_source_ids == ()


def test_optional_reject_strategy_raises_on_overflow() -> None:
    optional_source = source(source_id="CTX-OPTIONAL-REJECT")
    policy = ContextAssemblyPolicy(
        max_items=2,
        optional_overflow_strategy=OptionalSourceOverflowStrategy.REJECT,
    )
    with pytest.raises(ContextPackBudgetError) as exc_info:
        pack(optional_source, policy=policy)
    message = str(exc_info.value)
    assert "CTX-OPTIONAL-REJECT" in message
    assert "max_items" in message


def test_optional_omit_strategy_records_oversized_source_id() -> None:
    optional_source = source(source_id="CTX-OPTIONAL-OMIT", content="z" * 4200)
    policy = ContextAssemblyPolicy(
        max_item_characters=4096,
        optional_overflow_strategy=OptionalSourceOverflowStrategy.OMIT,
    )
    assembled = pack(optional_source, policy=policy)
    assert tuple(item.source_id for item in assembled.items) == (
        "CTX-PROJECT-SPEC",
        "CTX-TICKET-SPEC",
    )
    assert assembled.omitted_source_ids == ("CTX-OPTIONAL-OMIT",)
    assert assembled.truncated_source_ids == ()


def test_optional_truncate_then_omit_strategy_truncates_when_possible() -> None:
    optional_source = source(source_id="CTX-OPTIONAL-LONG", content="q" * 4200)
    assembled = pack(
        optional_source,
        policy=ContextAssemblyPolicy(max_item_characters=4096),
    )
    item = assembled.items[2]
    assert item.source_id == "CTX-OPTIONAL-LONG"
    assert item.original_character_count == 4200
    assert item.included_character_count == 4096
    assert item.truncated is True
    assert item.content.startswith("q")
    assert item.content.endswith("\n[CONTEXT_TRUNCATED]")
    assert item.source_SHA256 == sha256_text("q" * 4200)
    assert item.included_SHA256 == sha256_text(item.content)
    assert item.source_SHA256 != item.included_SHA256
    assert assembled.truncated_source_ids == ("CTX-OPTIONAL-LONG",)
    assert assembled.omitted_source_ids == ()


def test_truncation_marker_is_hashed_exactly_once() -> None:
    marker = "\n[CONTEXT_TRUNCATED]"
    optional_source = source(source_id="CTX-OPTIONAL-MARKER", content="m" * 4200)
    assembled = pack(
        optional_source,
        policy=ContextAssemblyPolicy(max_item_characters=4096),
    )
    item = assembled.items[2]
    expected_content = f"{'m' * (4096 - len(marker))}{marker}"
    assert item.truncated is True
    assert item.content == expected_content
    assert item.content.count(marker) == 1
    assert item.included_SHA256 == sha256_text(expected_content)


@pytest.mark.parametrize(
    "sensitivity", [ContextSensitivity.SENSITIVE, ContextSensitivity.SECRET]
)
def test_sensitive_and_secret_sources_are_rejected_without_content_echo(
    sensitivity: ContextSensitivity,
) -> None:
    sensitive_content = "private-note-not-for-output"
    sensitive_source = source(
        source_id="CTX-SENSITIVE-A",
        content=sensitive_content,
        sensitivity=sensitivity,
    )
    with pytest.raises(ContextPackSensitiveContentError) as exc_info:
        pack(sensitive_source)
    message = str(exc_info.value)
    assert "CTX-SENSITIVE-A" in message
    assert sensitivity.value in message
    assert sensitive_content not in message


def test_secret_source_error_omits_title_reference_and_content() -> None:
    secret_title = "Synthetic Secret Source Title"
    secret_reference = "external:synthetic-secret-reference"
    secret_content = "secret-source-content-not-for-errors"
    secret_source = source(
        source_id="CTX-SECRET-BOUNDED",
        title=secret_title,
        source_reference=secret_reference,
        content=secret_content,
        sensitivity=ContextSensitivity.SECRET,
    )
    with pytest.raises(ContextPackSensitiveContentError) as exc_info:
        pack(secret_source)
    message = str(exc_info.value)
    assert "CTX-SECRET-BOUNDED" in message
    assert "secret" in message
    assert secret_title not in message
    assert secret_reference not in message
    assert secret_content not in message


def test_secret_shaped_bearer_marker_is_rejected_without_content_echo() -> None:
    token_value = "token-value-not-real"
    token_source = source(
        source_id="CTX-BEARER-A",
        content=f"Authorization: Bearer {token_value}",
    )
    with pytest.raises(ContextPackSensitiveContentError) as exc_info:
        pack(token_source)
    message = str(exc_info.value)
    assert "CTX-BEARER-A" in message
    assert "bearer_token" in message
    assert token_value not in message


def test_secret_shaped_provider_key_marker_is_rejected() -> None:
    provider_key = "sk-" + "a" * 20
    token_source = source(source_id="CTX-PROVIDER-KEY", content=provider_key)
    with pytest.raises(ContextPackSensitiveContentError) as exc_info:
        pack(token_source)
    message = str(exc_info.value)
    assert "CTX-PROVIDER-KEY" in message
    assert "openai_style_key" in message
    assert provider_key not in message


def test_private_key_marker_is_rejected_without_literal_secret_fixture() -> None:
    marker = "-----BEGIN " + "PRIVATE KEY-----"
    key_source = source(source_id="CTX-PRIVATE-KEY", content=marker)
    with pytest.raises(ContextPackSensitiveContentError) as exc_info:
        pack(key_source)
    message = str(exc_info.value)
    assert "CTX-PRIVATE-KEY" in message
    assert "private_key" in message
    assert marker not in message


def test_placeholder_secret_markers_are_allowed() -> None:
    placeholder_source = source(
        source_id="CTX-PLACEHOLDER-A",
        content=(
            "Authorization: Bearer <REDACTED>\n"
            "access_token=synthetic-access-token\n"
            "refresh_token=<SECRET>"
        ),
    )
    assembled = pack(placeholder_source)
    assert assembled.items[2].source_id == "CTX-PLACEHOLDER-A"


def test_context_pack_item_rejects_tampered_character_counts() -> None:
    item_payload = pack().items[0].model_dump(mode="json")
    item_payload["included_character_count"] += 1
    assert_validation_fails(lambda: ContextPackItem.model_validate(item_payload))


def test_context_pack_item_rejects_untruncated_count_mismatch() -> None:
    truncated_item = pack(
        source(source_id="CTX-ITEM-TRUNCATED", content="t" * 4200),
        policy=ContextAssemblyPolicy(max_item_characters=4096),
    ).items[2]
    item_payload = truncated_item.model_dump(mode="json")
    item_payload["truncated"] = False
    assert_validation_fails(lambda: ContextPackItem.model_validate(item_payload))


def test_context_pack_item_rejects_tampered_digests() -> None:
    item_payload = pack().items[0].model_dump(mode="json")
    item_payload["included_SHA256"] = "0" * 64
    assert_validation_fails(lambda: ContextPackItem.model_validate(item_payload))


def test_context_pack_rejects_tampered_total_characters() -> None:
    payload = pack().model_dump(mode="json")
    payload["total_included_characters"] += 1
    assert_validation_fails(lambda: ContextPack.model_validate(payload))


def test_context_pack_rejects_omitted_included_overlap() -> None:
    payload = pack().model_dump(mode="json")
    payload["omitted_source_ids"] = ["CTX-PROJECT-SPEC"]
    assert_validation_fails(lambda: ContextPack.model_validate(payload))


def test_context_pack_rejects_truncated_source_id_not_included() -> None:
    payload = pack().model_dump(mode="json")
    payload["truncated_source_ids"] = ["CTX-MISSING-TRUNCATED"]
    assert_validation_fails(lambda: ContextPack.model_validate(payload))


def test_context_pack_rejects_tampered_pack_digest() -> None:
    payload = pack().model_dump(mode="json")
    payload["context_pack_SHA256"] = "0" * 64
    assert_validation_fails(lambda: ContextPack.model_validate(payload))


def test_context_pack_json_round_trip() -> None:
    assembled = pack(source(source_id="CTX-ROUND-TRIP"))
    assert ContextPack.model_validate_json(assembled.model_dump_json()) == assembled


def test_context_pack_json_schema_generation() -> None:
    schema = ContextPack.model_json_schema()
    assert schema["title"] == "ContextPack"
    assert "ContextPackItem" in schema["$defs"]
    assert "ContextAssemblyPolicy" in schema["$defs"]


def test_context_pack_json_schema_rejects_additional_properties() -> None:
    for model_type in PUBLIC_CONTEXT_MODELS:
        schema = model_type.model_json_schema()
        assert schema["additionalProperties"] is False


def test_context_pack_json_schema_contains_no_unrestricted_object_schema() -> None:
    for model_type in PUBLIC_CONTEXT_MODELS:
        for node in walk_schema_nodes(model_type.model_json_schema()):
            if isinstance(node, dict) and node.get("type") == "object":
                assert node.get("additionalProperties") is False
                assert "properties" in node


def test_no_public_context_any_annotations() -> None:
    for model_type in PUBLIC_CONTEXT_MODELS:
        for field in model_type.model_fields.values():
            assert not annotation_contains_forbidden(field.annotation)


def test_no_context_mapping_payload_fields() -> None:
    for model_type in PUBLIC_CONTEXT_MODELS:
        for field in model_type.model_fields.values():
            assert get_origin(field.annotation) is not dict


def test_context_pack_has_no_file_loading_functions() -> None:
    forbidden = (
        "load",
        "load_json",
        "load_file",
        "from_file",
        "save",
        "save_json",
        "write_file",
        "read_file",
        "fetch",
        "search",
    )
    for name, value in inspect.getmembers(ticket_factory):
        assert not (callable(value) and name in forbidden)


def test_context_pack_has_no_command_execution_functions() -> None:
    forbidden = (
        "execute",
        "run",
        "run_command",
        "invoke",
        "dispatch",
        "schedule",
        "publish",
    )
    for name, value in inspect.getmembers(ticket_factory):
        assert not (callable(value) and name in forbidden)


def test_context_pack_has_no_runtime_ticket_generation_or_approval_types() -> None:
    forbidden = (
        "WorkPacket",
        "ExecutionRun",
        "ExecutionCommand",
        "RuntimeState",
        "ApprovalRequest",
        "DependencyGraph",
        "TicketGenerator",
        "PromptTemplate",
        "ProviderRequest",
        "AgentAssignment",
    )
    for name in forbidden:
        assert not hasattr(ticket_factory, name)
