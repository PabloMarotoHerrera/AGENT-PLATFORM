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
    TICKET_POLICY_SCHEMA_VERSION,
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
    TicketLintDiagnostic,
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    TicketLintRuleCode,
    TicketLintScope,
    TicketLintSeverity,
    TicketLintSummary,
    TicketPlanningRequest,
    TicketPolicyError,
    TicketPolicyInputError,
    TicketPolicyProfile,
    TicketPolicyProfileName,
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
    get_ticket_policy_profile,
    lint_ticket_collection,
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
P16_4_EXPORTS = (
    "TICKET_POLICY_SCHEMA_VERSION",
    "TicketPolicyProfileName",
    "TicketLintSeverity",
    "TicketLintScope",
    "TicketLintDisposition",
    "TicketLintRuleCode",
    "TicketPolicyProfile",
    "TicketLintRequest",
    "TicketLintDiagnostic",
    "TicketLintSummary",
    "TicketLintReport",
    "TicketPolicyError",
    "TicketPolicyInputError",
    "get_ticket_policy_profile",
    "lint_ticket_collection",
)
PUBLIC_MODELS = (
    TicketPolicyProfile,
    TicketLintRequest,
    TicketLintDiagnostic,
    TicketLintSummary,
    TicketLintReport,
)
REQUIRED_RESPONSE_SECTIONS = (
    "Summary",
    "Files inspected",
    "Files modified",
    "Tests/commands run",
    "Decisions made",
    "Limitations",
)
REQUIRED_FORBIDDEN_ACTION_MARKERS = (
    "git add",
    "git commit",
    "git push",
    "git reset",
    "git clean",
    "git stash",
    "git worktree",
    "Graphify",
)
FORBIDDEN_VALIDATION_COMMAND_MARKERS = (
    "git add",
    "git commit",
    "git push",
    "git reset",
    "git clean",
    "git stash",
    "git worktree add",
    "git worktree remove",
    "graphify update",
    "graphify extract",
    "graphify export",
    "graphify cluster",
    "graphify recluster",
)


def scope(**overrides: object) -> RepositoryScopeSpec:
    data = {
        "allowed_paths": ("src/ticket.py",),
        "forbidden_paths": ("4_external/sources/**",),
        "allowed_actions": ("edit governed ticket policy contracts",),
        "forbidden_actions": REQUIRED_FORBIDDEN_ACTION_MARKERS,
    }
    data.update(overrides)
    return RepositoryScopeSpec.model_validate(data)


def authority(**overrides: object) -> AuthorityReferenceSpec:
    data = {
        "kind": AuthorityReferenceKind.GOVERNANCE_RECORD,
        "value": "0_architecture/governance/synthetic.md",
        "rationale": "Synthetic authority reference.",
        "required": True,
    }
    data.update(overrides)
    return AuthorityReferenceSpec.model_validate(data)


def response_contract(**overrides: object) -> TicketResponseContractSpec:
    data = {
        "required_sections": REQUIRED_RESPONSE_SECTIONS,
        "completion_verdict": "synthetic_ticket_ready",
    }
    data.update(overrides)
    return TicketResponseContractSpec.model_validate(data)


def validation_step(**overrides: object) -> TicketValidationStepSpec:
    data = {
        "validation_id": "V1",
        "description": "Run the synthetic validation.",
        "command": "python -m pytest synthetic_tests.py",
        "expected_result": "The synthetic validation reports success.",
        "required": True,
    }
    data.update(overrides)
    return TicketValidationStepSpec.model_validate(data)


def dependency(
    ticket_id: str,
    *,
    kind: DependencyKind = DependencyKind.HARD_PREREQUISITE,
    dep_scope: DependencyScope = DependencyScope.INTERNAL_PROJECT,
) -> TicketDependencySpec:
    return TicketDependencySpec(
        ticket_id=ticket_id,
        kind=kind,
        scope=dep_scope,
        rationale="Synthetic dependency declaration.",
    )


def project(**overrides: object) -> ProjectSpec:
    data = {
        "project_id": "P16",
        "title": "Synthetic ticket policy project",
        "objective": "Validate deterministic non-mutating ticket policy linting.",
        "summary": "This synthetic project validates P16.4 only.",
        "context": ("Synthetic planning context.",),
        "authority_references": (authority(),),
        "scope": scope(allowed_paths=("src/**",)),
        "constraints": ("No execution authority is granted.",),
        "non_goals": ("No ticket execution is authorized.",),
        "acceptance_criteria": ("The linter reports deterministic diagnostics.",),
        "completion_verdict": "synthetic_project_policy_ready",
    }
    data.update(overrides)
    return ProjectSpec.model_validate(data)


def ticket(
    ticket_id: str = "P16.1",
    *,
    title: str | None = None,
    ticket_type: TicketType = TicketType.IMPLEMENTATION,
    auth_refs: tuple[AuthorityReferenceSpec, ...] | None = None,
    deps: tuple[TicketDependencySpec, ...] = (),
    ticket_scope: RepositoryScopeSpec | None = None,
    constraints: tuple[str, ...] = ("Rollback by restoring the prior contract.",),
    tasks: tuple[str, ...] = ("Implement the deterministic policy evidence.",),
    acceptance_criteria: tuple[str, ...] = ("Rollback evidence is retained.",),
    validation_steps: tuple[TicketValidationStepSpec, ...] | None = None,
    response: TicketResponseContractSpec | None = None,
    recommended_commit_message: str | None = "P16 synthetic commit",
    project_id: str = "P16",
) -> TicketSpec:
    data = {
        "project_id": project_id,
        "ticket_id": ticket_id,
        "title": title or f"Synthetic ticket {ticket_id}",
        "ticket_type": ticket_type,
        "objective": "Validate one deterministic policy rule.",
        "context": ("Synthetic ticket context.",),
        "authority_references": (authority(),) if auth_refs is None else auth_refs,
        "dependencies": deps,
        "parallelization_hint": ParallelizationHint.UNSPECIFIED,
        "scope": ticket_scope
        or scope(allowed_paths=(f"src/{ticket_id.lower().replace('.', '_')}.py",)),
        "constraints": constraints,
        "tasks": tasks,
        "acceptance_criteria": acceptance_criteria,
        "validation_steps": validation_steps or (validation_step(),),
        "response_contract": response
        or response_contract(
            completion_verdict=f"synthetic_{ticket_id.lower().replace('.', '_')}_ready"
        ),
        "recommended_commit_message": recommended_commit_message,
    }
    return TicketSpec.model_validate(data)


def request(
    *tickets: TicketSpec,
    dependency_plan: TicketDependencyPlan | None = None,
    collection_complete: bool = False,
) -> TicketLintRequest:
    return TicketLintRequest(
        project_spec=project(),
        tickets=tickets or (ticket(),),
        dependency_plan=dependency_plan,
        collection_complete=collection_complete,
    )


def plan(*tickets: TicketSpec) -> TicketDependencyPlan:
    return build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=tickets)
    )


def diagnostics_by_code(
    report: TicketLintReport, code: TicketLintRuleCode
) -> tuple[TicketLintDiagnostic, ...]:
    return tuple(
        diagnostic for diagnostic in report.diagnostics if diagnostic.code is code
    )


def report_codes(report: TicketLintReport) -> tuple[TicketLintRuleCode, ...]:
    return tuple(diagnostic.code for diagnostic in report.diagnostics)


def assert_not_mutated(
    before: tuple[dict[str, object], ...], tickets: tuple[TicketSpec, ...]
) -> None:
    assert before == tuple(item.model_dump(mode="json") for item in tickets)


def test_p16_4_exports_import_correctly() -> None:
    assert TICKET_POLICY_SCHEMA_VERSION == 1
    assert TicketPolicyProfileName.GOVERNED_STANDARD_V1.value == "governed_standard_v1"
    assert TicketLintDisposition.BLOCKED.value == "blocked"
    assert TicketLintReport.__name__ == "TicketLintReport"
    assert lint_ticket_collection.__name__ == "lint_ticket_collection"


@pytest.mark.parametrize("export_name", P16_0_EXPORTS)
def test_p16_0_exports_remain_available(export_name: str) -> None:
    assert hasattr(ticket_factory, export_name)


@pytest.mark.parametrize("export_name", P16_1_EXPORTS)
def test_p16_1_exports_remain_available(export_name: str) -> None:
    assert hasattr(ticket_factory, export_name)


@pytest.mark.parametrize("export_name", P16_2_EXPORTS)
def test_p16_2_exports_remain_available(export_name: str) -> None:
    assert hasattr(ticket_factory, export_name)


@pytest.mark.parametrize("export_name", P16_3_EXPORTS)
def test_p16_3_exports_remain_available(export_name: str) -> None:
    assert hasattr(ticket_factory, export_name)


def test_public_export_groups_preserve_relative_order() -> None:
    exported = ticket_factory.__all__
    assert len(exported) == len(frozenset(exported))
    for group in (
        P16_0_EXPORTS,
        P16_1_EXPORTS,
        P16_2_EXPORTS,
        P16_3_EXPORTS,
        P16_4_EXPORTS,
    ):
        positions = [exported.index(name) for name in group]
        assert positions == sorted(positions)
    assert exported[-len(P16_4_EXPORTS) :] == P16_4_EXPORTS


def test_future_additive_exports_remain_allowed() -> None:
    assert set(
        P16_0_EXPORTS + P16_1_EXPORTS + P16_2_EXPORTS + P16_3_EXPORTS + P16_4_EXPORTS
    ).issubset(set(ticket_factory.__all__))


def test_no_import_time_filesystem_or_network_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module_name = "hermes_cli.agent_platform.ticket_factory.ticket_policy"
    original_module = sys.modules.pop(module_name, None)

    def fail_open(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("unexpected open")

    def fail_socket(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("unexpected socket")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(socket, "socket", fail_socket)
    try:
        imported = importlib.import_module(module_name)
    finally:
        sys.modules.pop(module_name, None)
        if original_module is not None:
            sys.modules[module_name] = original_module
    assert imported.TICKET_POLICY_SCHEMA_VERSION == 1


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_are_frozen_and_extra_forbid(model: type) -> None:
    assert model.model_config["frozen"] is True
    assert model.model_config["extra"] == "forbid"
    assert model.model_config["validate_default"] is True
    assert model.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_reject_unknown_fields(model: type) -> None:
    valid_data = {
        TicketPolicyProfile: get_ticket_policy_profile().model_dump(mode="json"),
        TicketLintRequest: request().model_dump(mode="json"),
        TicketLintDiagnostic: TicketLintDiagnostic(
            diagnostic_id="LINT-0001",
            code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
            severity=TicketLintSeverity.ERROR,
            scope=TicketLintScope.COLLECTION,
            ticket_id=None,
            field_path="dependency_plan",
            message="Synthetic diagnostic.",
            remediation="Synthetic remediation.",
            blocking=True,
        ).model_dump(mode="json"),
        TicketLintSummary: TicketLintSummary(
            ticket_count=1,
            diagnostic_count=0,
            error_count=0,
            warning_count=0,
            info_count=0,
            blocked_ticket_ids=(),
            warning_ticket_ids=(),
            collection_blocked=False,
        ).model_dump(mode="json"),
        TicketLintReport: lint_ticket_collection(request()).model_dump(mode="json"),
    }[model]
    valid_data["unexpected"] = "value"
    with pytest.raises(ValidationError):
        model.model_validate(valid_data)


def test_mutable_sequences_normalize_to_tuples() -> None:
    profile_data = get_ticket_policy_profile().model_dump(mode="json")
    profile_data["required_response_sections"] = list(REQUIRED_RESPONSE_SECTIONS)
    assert isinstance(
        TicketPolicyProfile.model_validate(profile_data).required_response_sections,
        tuple,
    )
    request_data = request().model_dump(mode="json")
    request_data["tickets"] = list(request_data["tickets"])
    assert isinstance(TicketLintRequest.model_validate(request_data).tickets, tuple)


def test_strict_booleans_reject_strings() -> None:
    request_data = request().model_dump(mode="json")
    request_data["collection_complete"] = "false"
    with pytest.raises(ValidationError):
        TicketLintRequest.model_validate(request_data)
    diagnostic_data = TicketLintDiagnostic(
        diagnostic_id="LINT-0001",
        code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
        severity=TicketLintSeverity.ERROR,
        scope=TicketLintScope.COLLECTION,
        ticket_id=None,
        field_path="dependency_plan",
        message="Synthetic diagnostic.",
        remediation="Synthetic remediation.",
        blocking=True,
    ).model_dump(mode="json")
    diagnostic_data["blocking"] = "true"
    with pytest.raises(ValidationError):
        TicketLintDiagnostic.model_validate(diagnostic_data)


def test_schema_version_defaults_and_alternatives_rejected() -> None:
    assert get_ticket_policy_profile().schema_version == 1
    assert lint_ticket_collection(request()).schema_version == 1
    profile_data = get_ticket_policy_profile().model_dump(mode="json")
    profile_data["schema_version"] = 2
    with pytest.raises(ValidationError):
        TicketPolicyProfile.model_validate(profile_data)
    report_data = lint_ticket_collection(request()).model_dump(mode="json")
    report_data["schema_version"] = 2
    with pytest.raises(ValidationError):
        TicketLintReport.model_validate(report_data)


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_have_no_mutable_defaults(model: type) -> None:
    for field in model.model_fields.values():
        assert not isinstance(field.default, (list, dict, set))


def test_canonical_profile_contents_are_exact() -> None:
    profile = get_ticket_policy_profile()
    assert profile.name is TicketPolicyProfileName.GOVERNED_STANDARD_V1
    assert profile.required_response_sections == REQUIRED_RESPONSE_SECTIONS
    assert (
        profile.required_forbidden_action_markers == REQUIRED_FORBIDDEN_ACTION_MARKERS
    )
    assert profile.authority_reference_required_ticket_types == (
        TicketType.ARCHITECTURE,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    )
    assert profile.commit_message_required_ticket_types == (
        TicketType.IMPLEMENTATION,
        TicketType.REFACTOR,
        TicketType.TEST,
        TicketType.BUGFIX,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    )
    assert profile.rollback_required_ticket_types == (
        TicketType.IMPLEMENTATION,
        TicketType.REFACTOR,
        TicketType.BUGFIX,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    )
    assert profile.rollback_markers == ("rollback", "restore", "revert", "remove only")
    assert (
        profile.forbidden_validation_command_markers
        == FORBIDDEN_VALIDATION_COMMAND_MARKERS
    )
    assert profile.closure_suffixes == ("R", "CR")
    assert profile.duplicate_title_severity is TicketLintSeverity.WARNING
    assert profile.duplicate_commit_message_severity is TicketLintSeverity.WARNING
    assert profile.duplicate_completion_verdict_severity is TicketLintSeverity.ERROR


def test_canonical_profile_lookup_is_single_deterministic_immutable_profile() -> None:
    profile = get_ticket_policy_profile()
    assert (
        get_ticket_policy_profile(TicketPolicyProfileName.GOVERNED_STANDARD_V1)
        == profile
    )
    assert len(tuple(TicketPolicyProfileName)) == 1
    with pytest.raises(ValidationError):
        profile.name = TicketPolicyProfileName.GOVERNED_STANDARD_V1


@pytest.mark.parametrize(
    "field_name",
    (
        "required_response_sections",
        "required_forbidden_action_markers",
        "authority_reference_required_ticket_types",
        "commit_message_required_ticket_types",
        "rollback_required_ticket_types",
        "rollback_markers",
        "forbidden_validation_command_markers",
        "closure_suffixes",
    ),
)
def test_duplicate_profile_entries_fail_validation(field_name: str) -> None:
    data = get_ticket_policy_profile().model_dump(mode="json")
    values = list(data[field_name])
    values.append(values[0])
    data[field_name] = values
    with pytest.raises(ValidationError):
        TicketPolicyProfile.model_validate(data)


def test_one_ticket_request_validates_with_defaults() -> None:
    lint_request = request()
    assert lint_request.dependency_plan is None
    assert lint_request.collection_complete is False
    assert lint_request.policy_name is TicketPolicyProfileName.GOVERNED_STANDARD_V1


def test_multi_ticket_request_validates_with_matching_plan() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    lint_request = request(first, second, dependency_plan=plan(first, second))
    assert len(lint_request.tickets) == 2


def test_request_validation_rejects_duplicate_ticket_ids() -> None:
    first = ticket("P16.1", title="First title")
    duplicate = ticket("P16.1", title="Second title")
    with pytest.raises(ValidationError):
        request(first, duplicate)


def test_request_validation_rejects_foreign_project_and_prefix() -> None:
    with pytest.raises(ValidationError):
        ticket("P16.1", project_id="P99")
    foreign_prefix = ticket("P99.1", project_id="P99")
    bad_request = TicketLintRequest.model_construct(
        project_spec=project(),
        tickets=(foreign_prefix,),
        dependency_plan=None,
        collection_complete=False,
        policy_name=TicketPolicyProfileName.GOVERNED_STANDARD_V1,
    )
    with pytest.raises(TicketPolicyInputError):
        lint_ticket_collection(bad_request)


def test_request_validation_rejects_mismatched_plan_project_and_ticket_set() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2")
    matching_plan = plan(first, second)
    bad_project_plan = matching_plan.model_copy(update={"project_id": "P99"})
    bad_project_request = TicketLintRequest.model_construct(
        project_spec=project(),
        tickets=(first, second),
        dependency_plan=bad_project_plan,
        collection_complete=False,
        policy_name=TicketPolicyProfileName.GOVERNED_STANDARD_V1,
    )
    with pytest.raises(TicketPolicyInputError):
        lint_ticket_collection(bad_project_request)
    bad_set_plan = matching_plan.model_copy(update={"ticket_ids": ("P16.1",)})
    bad_set_request = TicketLintRequest.model_construct(
        project_spec=project(),
        tickets=(first, second),
        dependency_plan=bad_set_plan,
        collection_complete=False,
        policy_name=TicketPolicyProfileName.GOVERNED_STANDARD_V1,
    )
    with pytest.raises(TicketPolicyInputError):
        lint_ticket_collection(bad_set_request)


def test_ticket_permutation_remains_valid_and_empty_or_oversized_collections_fail() -> (
    None
):
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    matching_plan = plan(first, second)
    assert request(second, first, dependency_plan=matching_plan).tickets == (
        second,
        first,
    )
    with pytest.raises(ValidationError):
        TicketLintRequest(project_spec=project(), tickets=())
    many = tuple(
        ticket(f"P16.{index}", title=f"Ticket {index}") for index in range(1, 513)
    )
    assert len(request(*many, dependency_plan=plan(*many)).tickets) == 512
    too_many = many + (ticket("P16.513", title="Ticket 513"),)
    with pytest.raises(ValidationError):
        TicketLintRequest(project_spec=project(), tickets=too_many)


def test_scope_policy_passing_ticket_has_no_scope_diagnostics() -> None:
    report = lint_ticket_collection(request(ticket()))
    assert not {
        TicketLintRuleCode.ALLOWED_PATHS_REQUIRED,
        TicketLintRuleCode.FORBIDDEN_ACTIONS_REQUIRED,
        TicketLintRuleCode.SCOPE_EXACT_CONTRADICTION,
        TicketLintRuleCode.REQUIRED_FORBIDDEN_ACTION_MISSING,
    }.intersection(report_codes(report))


def test_empty_allowed_paths_and_forbidden_actions_emit_errors_without_mutation() -> (
    None
):
    bad_ticket = ticket(
        ticket_scope=scope(
            allowed_paths=(), forbidden_actions=(), allowed_actions=("edit",)
        )
    )
    before = (bad_ticket.model_dump(mode="json"),)
    report = lint_ticket_collection(request(bad_ticket))
    assert TicketLintRuleCode.ALLOWED_PATHS_REQUIRED in report_codes(report)
    assert TicketLintRuleCode.FORBIDDEN_ACTIONS_REQUIRED in report_codes(report)
    assert_not_mutated(before, (bad_ticket,))


def test_exact_allowed_forbidden_path_contradiction_only_matches_exact_normalized_pattern() -> (
    None
):
    contradictory = ticket(
        ticket_scope=scope(allowed_paths=("src/a.py",), forbidden_paths=(" src/a.py ",))
    )
    report = lint_ticket_collection(request(contradictory))
    assert TicketLintRuleCode.SCOPE_EXACT_CONTRADICTION in report_codes(report)
    glob_like = ticket(
        ticket_scope=scope(allowed_paths=("src/*.py",), forbidden_paths=("src/a.py",))
    )
    assert TicketLintRuleCode.SCOPE_EXACT_CONTRADICTION not in report_codes(
        lint_ticket_collection(request(glob_like))
    )


@pytest.mark.parametrize("missing_marker", REQUIRED_FORBIDDEN_ACTION_MARKERS)
def test_each_missing_forbidden_action_marker_emits_deterministic_error(
    missing_marker: str,
) -> None:
    actions = tuple(
        marker
        for marker in REQUIRED_FORBIDDEN_ACTION_MARKERS
        if marker != missing_marker
    )
    bad_ticket = ticket(ticket_scope=scope(forbidden_actions=actions))
    diagnostics = diagnostics_by_code(
        lint_ticket_collection(request(bad_ticket)),
        TicketLintRuleCode.REQUIRED_FORBIDDEN_ACTION_MISSING,
    )
    assert [diagnostic.message for diagnostic in diagnostics] == [
        f"Forbidden-action marker is missing: marker={missing_marker}"
    ]


def test_forbidden_action_marker_matching_is_case_insensitive_and_whitespace_normalized() -> (
    None
):
    actions = tuple(
        f"  {marker.upper()}  " for marker in REQUIRED_FORBIDDEN_ACTION_MARKERS
    )
    report = lint_ticket_collection(
        request(ticket(ticket_scope=scope(forbidden_actions=actions)))
    )
    assert TicketLintRuleCode.REQUIRED_FORBIDDEN_ACTION_MISSING not in report_codes(
        report
    )


@pytest.mark.parametrize(
    "ticket_type", (TicketType.ARCHITECTURE, TicketType.INTEGRATION, TicketType.CLOSURE)
)
def test_required_authority_ticket_types_pass_with_required_reference(
    ticket_type: TicketType,
) -> None:
    ticket_id = "P16.R" if ticket_type is TicketType.CLOSURE else "P16.1"
    report = lint_ticket_collection(request(ticket(ticket_id, ticket_type=ticket_type)))
    assert TicketLintRuleCode.AUTHORITY_REFERENCE_REQUIRED not in report_codes(report)


@pytest.mark.parametrize(
    "ticket_type", (TicketType.ARCHITECTURE, TicketType.INTEGRATION, TicketType.CLOSURE)
)
def test_missing_required_authority_reference_emits_error(
    ticket_type: TicketType,
) -> None:
    ticket_id = "P16.R" if ticket_type is TicketType.CLOSURE else "P16.1"
    bad_ticket = ticket(
        ticket_id, ticket_type=ticket_type, auth_refs=(authority(required=False),)
    )
    report = lint_ticket_collection(request(bad_ticket))
    diagnostic = diagnostics_by_code(
        report, TicketLintRuleCode.AUTHORITY_REFERENCE_REQUIRED
    )[0]
    assert diagnostic.field_path == "authority_references"


def test_implementation_ticket_does_not_require_authority_and_references_are_not_resolved() -> (
    None
):
    no_authority = ticket(auth_refs=())
    report = lint_ticket_collection(request(no_authority))
    assert TicketLintRuleCode.AUTHORITY_REFERENCE_REQUIRED not in report_codes(report)


@pytest.mark.parametrize(
    "ticket_type",
    (
        TicketType.IMPLEMENTATION,
        TicketType.REFACTOR,
        TicketType.TEST,
        TicketType.BUGFIX,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    ),
)
def test_required_commit_message_ticket_types_fail_when_missing(
    ticket_type: TicketType,
) -> None:
    ticket_id = "P16.R" if ticket_type is TicketType.CLOSURE else "P16.1"
    bad_ticket = ticket(
        ticket_id, ticket_type=ticket_type, recommended_commit_message=None
    )
    report = lint_ticket_collection(request(bad_ticket))
    assert TicketLintRuleCode.RECOMMENDED_COMMIT_MESSAGE_REQUIRED in report_codes(
        report
    )


@pytest.mark.parametrize(
    "ticket_type", (TicketType.ARCHITECTURE, TicketType.DOCUMENTATION)
)
def test_architecture_and_documentation_may_omit_commit_message(
    ticket_type: TicketType,
) -> None:
    no_commit = ticket(ticket_type=ticket_type, recommended_commit_message=None)
    report = lint_ticket_collection(request(no_commit))
    assert TicketLintRuleCode.RECOMMENDED_COMMIT_MESSAGE_REQUIRED not in report_codes(
        report
    )


@pytest.mark.parametrize(
    ("field_name", "marker"),
    (
        ("constraints", "rollback"),
        ("tasks", "restore"),
        ("acceptance_criteria", "revert"),
        ("constraints", "remove-only"),
    ),
)
def test_rollback_markers_pass_in_each_source_field(
    field_name: str, marker: str
) -> None:
    kwargs = {
        "constraints": ("No rollback marker here.",),
        "tasks": ("No restoration marker here.",),
        "acceptance_criteria": ("No reversion marker here.",),
    }
    kwargs[field_name] = (f"Use {marker} evidence when needed.",)
    report = lint_ticket_collection(request(ticket(**kwargs)))
    assert TicketLintRuleCode.ROLLBACK_CONSTRAINT_REQUIRED not in report_codes(report)


@pytest.mark.parametrize(
    "ticket_type",
    (
        TicketType.IMPLEMENTATION,
        TicketType.REFACTOR,
        TicketType.BUGFIX,
        TicketType.INTEGRATION,
        TicketType.CLOSURE,
    ),
)
def test_required_rollback_ticket_types_fail_without_evidence(
    ticket_type: TicketType,
) -> None:
    ticket_id = "P16.R" if ticket_type is TicketType.CLOSURE else "P16.1"
    bad_ticket = ticket(
        ticket_id,
        ticket_type=ticket_type,
        constraints=("No restoration evidence.",),
        tasks=("Perform deterministic linting.",),
        acceptance_criteria=("The linter reports findings.",),
    )
    assert TicketLintRuleCode.ROLLBACK_CONSTRAINT_REQUIRED in report_codes(
        lint_ticket_collection(request(bad_ticket))
    )


@pytest.mark.parametrize(
    "ticket_type", (TicketType.ARCHITECTURE, TicketType.DOCUMENTATION)
)
def test_architecture_and_documentation_do_not_require_rollback(
    ticket_type: TicketType,
) -> None:
    no_rollback = ticket(
        ticket_type=ticket_type,
        constraints=("No marker.",),
        tasks=("Perform deterministic linting.",),
        acceptance_criteria=("The linter reports findings.",),
    )
    assert TicketLintRuleCode.ROLLBACK_CONSTRAINT_REQUIRED not in report_codes(
        lint_ticket_collection(request(no_rollback))
    )


def test_rollback_matching_is_case_insensitive_and_inputs_remain_unchanged() -> None:
    checked = ticket(constraints=("RESTORE prior state if needed.",))
    before = (checked.model_dump(mode="json"),)
    assert TicketLintRuleCode.ROLLBACK_CONSTRAINT_REQUIRED not in report_codes(
        lint_ticket_collection(request(checked))
    )
    assert_not_mutated(before, (checked,))


def test_all_required_response_sections_pass_and_order_does_not_matter() -> None:
    reversed_sections = tuple(reversed(REQUIRED_RESPONSE_SECTIONS))
    checked = ticket(response=response_contract(required_sections=reversed_sections))
    assert TicketLintRuleCode.REQUIRED_RESPONSE_SECTION_MISSING not in report_codes(
        lint_ticket_collection(request(checked))
    )


@pytest.mark.parametrize("missing_section", REQUIRED_RESPONSE_SECTIONS)
def test_each_missing_response_section_emits_error(missing_section: str) -> None:
    sections = tuple(
        section for section in REQUIRED_RESPONSE_SECTIONS if section != missing_section
    )
    bad_ticket = ticket(response=response_contract(required_sections=sections))
    diagnostics = diagnostics_by_code(
        lint_ticket_collection(request(bad_ticket)),
        TicketLintRuleCode.REQUIRED_RESPONSE_SECTION_MISSING,
    )
    assert any(missing_section in diagnostic.message for diagnostic in diagnostics)


def test_response_section_matching_ignores_case_and_surrounding_whitespace_but_not_similar_text() -> (
    None
):
    sections = tuple(f"  {section.upper()}  " for section in REQUIRED_RESPONSE_SECTIONS)
    assert TicketLintRuleCode.REQUIRED_RESPONSE_SECTION_MISSING not in report_codes(
        lint_ticket_collection(
            request(ticket(response=response_contract(required_sections=sections)))
        )
    )
    similar = tuple(
        section.replace("Summary", "Summaries")
        for section in REQUIRED_RESPONSE_SECTIONS
    )
    assert TicketLintRuleCode.REQUIRED_RESPONSE_SECTION_MISSING in report_codes(
        lint_ticket_collection(
            request(ticket(response=response_contract(required_sections=similar)))
        )
    )


def test_completion_verdict_is_not_approval_authority() -> None:
    report = lint_ticket_collection(request(ticket()))
    assert "approval" not in report.model_dump_json().casefold()


def test_required_validation_step_passes_and_all_optional_fails() -> None:
    assert TicketLintRuleCode.REQUIRED_VALIDATION_STEP_MISSING not in report_codes(
        lint_ticket_collection(
            request(ticket(validation_steps=(validation_step(required=True),)))
        )
    )
    report = lint_ticket_collection(
        request(ticket(validation_steps=(validation_step(required=False),)))
    )
    assert TicketLintRuleCode.REQUIRED_VALIDATION_STEP_MISSING in report_codes(report)


def test_null_and_safe_inert_validation_commands_pass() -> None:
    null_command = ticket(validation_steps=(validation_step(command=None),))
    safe_command = ticket(
        validation_steps=(validation_step(command="python -m pytest tests"),)
    )
    assert TicketLintRuleCode.FORBIDDEN_VALIDATION_COMMAND not in report_codes(
        lint_ticket_collection(request(null_command))
    )
    assert TicketLintRuleCode.FORBIDDEN_VALIDATION_COMMAND not in report_codes(
        lint_ticket_collection(request(safe_command))
    )


@pytest.mark.parametrize("marker", FORBIDDEN_VALIDATION_COMMAND_MARKERS)
def test_each_forbidden_validation_command_marker_is_detected_without_full_command(
    marker: str,
) -> None:
    command = f"echo before && {marker} synthetic-target && echo after"
    bad_ticket = ticket(validation_steps=(validation_step(command=command),))
    diagnostic = diagnostics_by_code(
        lint_ticket_collection(request(bad_ticket)),
        TicketLintRuleCode.FORBIDDEN_VALIDATION_COMMAND,
    )[0]
    assert "validation_id=V1" in diagnostic.message
    assert f"marker={marker}" in diagnostic.message
    assert command not in diagnostic.message
    assert diagnostic.field_path == "validation_steps.V1.command"


def test_validation_commands_are_not_rewritten_or_executed() -> None:
    checked = ticket(
        validation_steps=(validation_step(command="python -m pytest tests"),)
    )
    before = (checked.model_dump(mode="json"),)
    lint_ticket_collection(request(checked))
    assert_not_mutated(before, (checked,))


def test_one_ticket_collection_may_omit_dependency_plan() -> None:
    report = lint_ticket_collection(request(ticket()))
    assert TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED not in report_codes(report)


def test_multi_ticket_collection_requires_matching_dependency_plan() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2")
    assert TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED in report_codes(
        lint_ticket_collection(request(first, second))
    )
    assert TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED not in report_codes(
        lint_ticket_collection(
            request(first, second, dependency_plan=plan(first, second))
        )
    )


def test_dependency_plan_is_not_rebuilt_or_waves_changed() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    dependency_plan = plan(first, second)
    before = dependency_plan.model_dump(mode="json")
    lint_ticket_collection(request(second, first, dependency_plan=dependency_plan))
    assert dependency_plan.model_dump(mode="json") == before


def test_input_permutation_preserves_dependency_plan_diagnostics() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    dependency_plan = plan(first, second)
    first_report = lint_ticket_collection(
        request(first, second, dependency_plan=dependency_plan)
    )
    second_report = lint_ticket_collection(
        request(second, first, dependency_plan=dependency_plan)
    )
    assert first_report.diagnostics == second_report.diagnostics


def test_blocked_ticket_policy_reports_direct_and_inherited_blockers_deterministically() -> (
    None
):
    first = ticket(
        "P16.1",
        deps=(dependency("P99.1", dep_scope=DependencyScope.EXTERNAL_PROJECT),),
    )
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    dependency_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(first, second))
    )
    report = lint_ticket_collection(
        request(first, second, dependency_plan=dependency_plan)
    )
    diagnostics = diagnostics_by_code(report, TicketLintRuleCode.DEPENDENCY_BLOCKED)
    assert tuple(diagnostic.ticket_id for diagnostic in diagnostics) == (
        "P16.1",
        "P16.2",
    )
    assert "blocked_by_ticket_ids=P99.1" in diagnostics[0].message
    assert "blocked_by_ticket_ids=P16.1" in diagnostics[1].message
    assert all("TicketBlocker" not in diagnostic.message for diagnostic in diagnostics)
    assert set(report.ticket_ids) == {"P16.1", "P16.2"}


def test_blocker_is_not_overridden() -> None:
    blocked = ticket(
        "P16.1", deps=(dependency("P99.1", dep_scope=DependencyScope.EXTERNAL_PROJECT),)
    )
    dependency_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(blocked,))
    )
    assert (
        lint_ticket_collection(
            request(blocked, dependency_plan=dependency_plan)
        ).summary.collection_blocked
        is True
    )


def test_unresolved_soft_external_dependency_emits_nonblocking_warning() -> None:
    checked = ticket(
        "P16.1",
        deps=(
            dependency(
                "P99.1",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        ),
    )
    dependency_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(checked,))
    )
    report = lint_ticket_collection(request(checked, dependency_plan=dependency_plan))
    diagnostic = diagnostics_by_code(
        report, TicketLintRuleCode.SOFT_EXTERNAL_DEPENDENCY_UNRESOLVED
    )[0]
    assert diagnostic.severity is TicketLintSeverity.WARNING
    assert diagnostic.blocking is False
    assert report.disposition is TicketLintDisposition.PASS_WITH_WARNINGS


def test_multiple_soft_external_dependencies_are_deterministic_and_not_hard_blockers() -> (
    None
):
    checked = ticket(
        "P16.1",
        deps=(
            dependency(
                "P99.2",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
            dependency(
                "P99.1",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        ),
    )
    dependency_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(checked,))
    )
    diagnostics = diagnostics_by_code(
        lint_ticket_collection(request(checked, dependency_plan=dependency_plan)),
        TicketLintRuleCode.SOFT_EXTERNAL_DEPENDENCY_UNRESOLVED,
    )
    assert [diagnostic.message.rsplit("=", 1)[-1] for diagnostic in diagnostics] == [
        "P99.1",
        "P99.2",
    ]


def test_missing_plan_yields_no_fabricated_soft_dependency_diagnostic() -> None:
    checked = ticket(
        "P16.1",
        deps=(
            dependency(
                "P99.1",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        ),
    )
    assert TicketLintRuleCode.SOFT_EXTERNAL_DEPENDENCY_UNRESOLVED not in report_codes(
        lint_ticket_collection(request(checked))
    )


def test_scope_review_wave_emits_human_review_warning_only() -> None:
    first = ticket("P16.1", ticket_scope=scope(allowed_paths=("src/*.py",)))
    second = ticket("P16.2", ticket_scope=scope(allowed_paths=("src/*.md",)))
    dependency_plan = plan(first, second)
    diagnostic = diagnostics_by_code(
        lint_ticket_collection(request(first, second, dependency_plan=dependency_plan)),
        TicketLintRuleCode.SCOPE_REVIEW_REQUIRED,
    )[0]
    assert "wave_id=WAVE-001" in diagnostic.message
    assert "SCOPE-" in diagnostic.message
    assert "actual write conflict" not in diagnostic.message.casefold()
    assert "safe execution" not in diagnostic.message.casefold()


@pytest.mark.parametrize(
    "hint", (ParallelizationHint.UNSPECIFIED, ParallelizationHint.SERIAL)
)
def test_dependency_ready_and_serial_waves_emit_no_scope_review_warning(
    hint: ParallelizationHint,
) -> None:
    checked = ticket("P16.1")
    checked = checked.model_copy(update={"parallelization_hint": hint})
    dependency_plan = plan(checked)
    assert all(
        wave.disposition is not WaveDisposition.SCOPE_REVIEW_REQUIRED
        for wave in dependency_plan.waves
    )
    assert TicketLintRuleCode.SCOPE_REVIEW_REQUIRED not in report_codes(
        lint_ticket_collection(request(checked, dependency_plan=dependency_plan))
    )


@pytest.mark.parametrize("ticket_id", ("P16.R", "P16.CR"))
def test_closure_suffix_ticket_type_passes(ticket_id: str) -> None:
    report = lint_ticket_collection(
        request(ticket(ticket_id, ticket_type=TicketType.CLOSURE))
    )
    assert TicketLintRuleCode.CLOSURE_IDENTIFIER_SUFFIX_INVALID not in report_codes(
        report
    )
    assert TicketLintRuleCode.CLOSURE_IDENTIFIER_TYPE_MISMATCH not in report_codes(
        report
    )


@pytest.mark.parametrize("ticket_id", ("P16.R", "P16.CR"))
def test_closure_suffix_nonclosure_ticket_fails_without_rename(ticket_id: str) -> None:
    checked = ticket(ticket_id, ticket_type=TicketType.IMPLEMENTATION)
    before = (checked.model_dump(mode="json"),)
    assert TicketLintRuleCode.CLOSURE_IDENTIFIER_TYPE_MISMATCH in report_codes(
        lint_ticket_collection(request(checked))
    )
    assert_not_mutated(before, (checked,))


@pytest.mark.parametrize("ticket_id", ("P16.1", "P16.X"))
def test_closure_ticket_requires_r_or_cr_suffix(ticket_id: str) -> None:
    assert TicketLintRuleCode.CLOSURE_IDENTIFIER_SUFFIX_INVALID in report_codes(
        lint_ticket_collection(
            request(ticket(ticket_id, ticket_type=TicketType.CLOSURE))
        )
    )


def test_complete_collection_closure_count_policy() -> None:
    implementation = ticket("P16.1")
    closure = ticket(
        "P16.R", ticket_type=TicketType.CLOSURE, deps=(dependency("P16.1"),)
    )
    assert TicketLintRuleCode.CLOSURE_TICKET_REQUIRED not in report_codes(
        lint_ticket_collection(request(implementation))
    )
    assert TicketLintRuleCode.CLOSURE_TICKET_REQUIRED in report_codes(
        lint_ticket_collection(request(implementation, collection_complete=True))
    )
    closure_plan = plan(implementation, closure)
    assert TicketLintRuleCode.CLOSURE_TICKET_REQUIRED not in report_codes(
        lint_ticket_collection(
            request(
                implementation,
                closure,
                dependency_plan=closure_plan,
                collection_complete=True,
            )
        )
    )
    second_closure = ticket("P16.CR", ticket_type=TicketType.CLOSURE)
    assert TicketLintRuleCode.MULTIPLE_CLOSURE_TICKETS in report_codes(
        lint_ticket_collection(
            request(
                implementation,
                closure,
                second_closure,
                dependency_plan=plan(implementation, closure, second_closure),
                collection_complete=True,
            )
        )
    )


def test_incomplete_collection_multiple_closures_does_not_trigger_count_policy() -> (
    None
):
    first = ticket("P16.R", ticket_type=TicketType.CLOSURE)
    second = ticket("P16.CR", ticket_type=TicketType.CLOSURE)
    report = lint_ticket_collection(
        request(first, second, dependency_plan=plan(first, second))
    )
    assert TicketLintRuleCode.MULTIPLE_CLOSURE_TICKETS not in report_codes(report)


def test_closure_dependency_direct_and_transitive_hard_coverage_passes() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    closure = ticket(
        "P16.R", ticket_type=TicketType.CLOSURE, deps=(dependency("P16.2"),)
    )
    report = lint_ticket_collection(
        request(
            first,
            second,
            closure,
            dependency_plan=plan(first, second, closure),
            collection_complete=True,
        )
    )
    assert TicketLintRuleCode.CLOSURE_DEPENDENCY_COVERAGE not in report_codes(report)


@pytest.mark.parametrize(
    "dep_kind", (DependencyKind.SOFT_PREDECESSOR, DependencyKind.HARD_PREREQUISITE)
)
def test_closure_dependency_missing_soft_or_external_coverage_fails(
    dep_kind: DependencyKind,
) -> None:
    implementation = ticket("P16.1")
    dep_scope = (
        DependencyScope.EXTERNAL_PROJECT
        if dep_kind is DependencyKind.HARD_PREREQUISITE
        else DependencyScope.INTERNAL_PROJECT
    )
    target = "P99.1" if dep_scope is DependencyScope.EXTERNAL_PROJECT else "P16.1"
    closure = ticket(
        "P16.R",
        ticket_type=TicketType.CLOSURE,
        deps=(dependency(target, kind=dep_kind, dep_scope=dep_scope),),
    )
    dependency_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(implementation, closure))
    )
    diagnostics = diagnostics_by_code(
        lint_ticket_collection(
            request(
                implementation,
                closure,
                dependency_plan=dependency_plan,
                collection_complete=True,
            )
        ),
        TicketLintRuleCode.CLOSURE_DEPENDENCY_COVERAGE,
    )
    assert diagnostics[0].ticket_id == "P16.R"
    assert "uncovered_ticket_id=P16.1" in diagnostics[0].message


def test_every_uncovered_ticket_is_identified_deterministically_and_no_dependency_is_inferred() -> (
    None
):
    first = ticket("P16.1")
    second = ticket("P16.2")
    closure = ticket("P16.R", ticket_type=TicketType.CLOSURE)
    dependency_plan = plan(first, second, closure)
    diagnostics = diagnostics_by_code(
        lint_ticket_collection(
            request(
                first,
                second,
                closure,
                dependency_plan=dependency_plan,
                collection_complete=True,
            )
        ),
        TicketLintRuleCode.CLOSURE_DEPENDENCY_COVERAGE,
    )
    assert [diagnostic.message.rsplit("=", 1)[-1] for diagnostic in diagnostics] == [
        "P16.1",
        "P16.2",
    ]


def test_closure_coverage_does_not_approve_project_closure() -> None:
    implementation = ticket("P16.1")
    closure = ticket(
        "P16.R", ticket_type=TicketType.CLOSURE, deps=(dependency("P16.1"),)
    )
    report = lint_ticket_collection(
        request(
            implementation,
            closure,
            dependency_plan=plan(implementation, closure),
            collection_complete=True,
        )
    )
    assert "approval" not in report.model_dump_json().casefold()


@pytest.mark.parametrize(
    "left_title,right_title",
    (
        ("Unique A", "Unique B"),
        ("Same Title", "same title"),
        ("Same   Title", " same title "),
    ),
)
def test_duplicate_title_policy(left_title: str, right_title: str) -> None:
    first = ticket("P16.1", title=left_title)
    second = ticket("P16.2", title=right_title)
    report = lint_ticket_collection(
        request(first, second, dependency_plan=plan(first, second))
    )
    diagnostics = diagnostics_by_code(report, TicketLintRuleCode.DUPLICATE_TICKET_TITLE)
    if left_title == "Unique A":
        assert not diagnostics
    else:
        assert diagnostics[0].severity is TicketLintSeverity.WARNING
        assert diagnostics[0].ticket_id == "P16.2"
        assert first.title == left_title


@pytest.mark.parametrize(
    "left_message,right_message,expected_duplicate",
    (
        ("Commit A", "Commit B", False),
        ("Same Commit", "same commit", True),
        ("Same   Commit", " same commit ", True),
    ),
)
def test_duplicate_commit_message_policy(
    left_message: str, right_message: str, expected_duplicate: bool
) -> None:
    first = ticket("P16.1", recommended_commit_message=left_message)
    second = ticket("P16.2", recommended_commit_message=right_message)
    null_message = ticket("P16.3", recommended_commit_message=None)
    report = lint_ticket_collection(
        request(
            first,
            second,
            null_message,
            dependency_plan=plan(first, second, null_message),
        )
    )
    diagnostics = diagnostics_by_code(
        report, TicketLintRuleCode.DUPLICATE_COMMIT_MESSAGE
    )
    assert bool(diagnostics) is expected_duplicate
    if diagnostics:
        assert diagnostics[0].severity is TicketLintSeverity.WARNING
        assert diagnostics[0].ticket_id == "P16.2"


def test_duplicate_completion_verdict_policy_blocks_later_ticket_only() -> None:
    first = ticket(
        "P16.1", response=response_contract(completion_verdict="same_verdict")
    )
    second = ticket(
        "P16.2", response=response_contract(completion_verdict="same_verdict")
    )
    report = lint_ticket_collection(
        request(first, second, dependency_plan=plan(first, second))
    )
    diagnostics = diagnostics_by_code(
        report, TicketLintRuleCode.DUPLICATE_COMPLETION_VERDICT
    )
    assert diagnostics[0].severity is TicketLintSeverity.ERROR
    assert diagnostics[0].ticket_id == "P16.2"
    assert report.disposition is TicketLintDisposition.BLOCKED
    assert first.response_contract.completion_verdict == "same_verdict"


def test_unique_completion_verdicts_pass_duplicate_policy() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2")
    assert TicketLintRuleCode.DUPLICATE_COMPLETION_VERDICT not in report_codes(
        lint_ticket_collection(
            request(first, second, dependency_plan=plan(first, second))
        )
    )


def test_diagnostic_ordering_and_ids_are_deterministic() -> None:
    first = ticket(
        "P16.2",
        ticket_scope=scope(allowed_paths=(), forbidden_actions=()),
        recommended_commit_message=None,
    )
    second = ticket("P16.10", title=first.title, recommended_commit_message=None)
    report = lint_ticket_collection(
        request(second, first, dependency_plan=plan(first, second))
    )
    assert [diagnostic.diagnostic_id for diagnostic in report.diagnostics] == [
        f"LINT-{index:04d}" for index in range(1, len(report.diagnostics) + 1)
    ]
    severity_ranks = {
        TicketLintSeverity.ERROR: 0,
        TicketLintSeverity.WARNING: 1,
        TicketLintSeverity.INFO: 2,
    }
    assert [
        severity_ranks[diagnostic.severity] for diagnostic in report.diagnostics
    ] == sorted(
        severity_ranks[diagnostic.severity] for diagnostic in report.diagnostics
    )
    permuted = lint_ticket_collection(
        request(first, second, dependency_plan=plan(first, second))
    )
    assert report.diagnostics == permuted.diagnostics


def test_manual_diagnostic_contract_enforces_severity_blocking_and_scope() -> None:
    with pytest.raises(ValidationError):
        TicketLintDiagnostic(
            diagnostic_id="LINT-0001",
            code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
            severity=TicketLintSeverity.ERROR,
            scope=TicketLintScope.COLLECTION,
            ticket_id=None,
            field_path="dependency_plan",
            message="Message.",
            remediation="Remediation.",
            blocking=False,
        )
    with pytest.raises(ValidationError):
        TicketLintDiagnostic(
            diagnostic_id="LINT-0001",
            code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
            severity=TicketLintSeverity.WARNING,
            scope=TicketLintScope.COLLECTION,
            ticket_id=None,
            field_path="dependency_plan",
            message="Message.",
            remediation="Remediation.",
            blocking=True,
        )
    with pytest.raises(ValidationError):
        TicketLintDiagnostic(
            diagnostic_id="LINT-0001",
            code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
            severity=TicketLintSeverity.ERROR,
            scope=TicketLintScope.TICKET,
            ticket_id=None,
            field_path="dependency_plan",
            message="Message.",
            remediation="Remediation.",
            blocking=True,
        )


def test_summary_and_disposition_mapping() -> None:
    passing = lint_ticket_collection(request(ticket()))
    assert passing.summary.diagnostic_count == 0
    assert passing.disposition is TicketLintDisposition.PASS
    soft = ticket(
        "P16.1",
        deps=(
            dependency(
                "P99.1",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        ),
    )
    soft_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(soft,))
    )
    warning = lint_ticket_collection(request(soft, dependency_plan=soft_plan))
    assert warning.summary.warning_count == 1
    assert warning.disposition is TicketLintDisposition.PASS_WITH_WARNINGS
    blocked = lint_ticket_collection(
        request(ticket(ticket_scope=scope(allowed_paths=())))
    )
    assert blocked.summary.error_count > 0
    assert blocked.disposition is TicketLintDisposition.BLOCKED
    assert (
        blocked.summary.diagnostic_count
        == blocked.summary.error_count
        + blocked.summary.warning_count
        + blocked.summary.info_count
    )


def test_summary_ticket_id_sets_are_unique_and_collection_error_can_block_without_ticket_id() -> (
    None
):
    first = ticket("P16.1", recommended_commit_message="P16 first")
    second = ticket("P16.2", recommended_commit_message="P16 second")
    report = lint_ticket_collection(request(first, second))
    assert report.summary.collection_blocked is True
    assert report.summary.blocked_ticket_ids == ()
    assert report.summary.warning_ticket_ids == ()


def test_digest_evidence_is_stable_and_sensitive_to_changes() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    dependency_plan = plan(first, second)
    first_report = lint_ticket_collection(
        request(first, second, dependency_plan=dependency_plan)
    )
    second_report = lint_ticket_collection(
        request(second, first, dependency_plan=dependency_plan)
    )
    assert first_report.lint_input_SHA256 == second_report.lint_input_SHA256
    assert first_report.report_SHA256 == second_report.report_SHA256
    changed_ticket = ticket("P16.2", title="Changed title", deps=(dependency("P16.1"),))
    changed_report = lint_ticket_collection(
        request(first, changed_ticket, dependency_plan=plan(first, changed_ticket))
    )
    assert changed_report.lint_input_SHA256 != first_report.lint_input_SHA256
    complete_report = lint_ticket_collection(
        request(
            first, second, dependency_plan=dependency_plan, collection_complete=True
        )
    )
    assert complete_report.lint_input_SHA256 != first_report.lint_input_SHA256
    assert len(first_report.lint_input_SHA256) == 64
    assert first_report.lint_input_SHA256 == first_report.lint_input_SHA256.lower()


def test_report_digest_changes_with_diagnostics_summary_and_disposition_and_excludes_self() -> (
    None
):
    passing = lint_ticket_collection(request(ticket()))
    blocked = lint_ticket_collection(
        request(ticket(ticket_scope=scope(allowed_paths=())))
    )
    assert passing.report_SHA256 != blocked.report_SHA256
    tampered = passing.model_dump(mode="json")
    tampered["report_SHA256"] = "0" * 64
    with pytest.raises(ValidationError):
        TicketLintReport.model_validate(tampered)
    assert "report_SHA256" not in passing.report_SHA256


@pytest.mark.parametrize(
    "model_factory",
    (
        lambda: get_ticket_policy_profile(),
        lambda: request(),
        lambda: lint_ticket_collection(request()).diagnostics,
        lambda: lint_ticket_collection(request()).summary,
        lambda: lint_ticket_collection(request()),
    ),
)
def test_serialization_round_trip_and_tuple_immutability(
    model_factory: Callable[[], object],
) -> None:
    value = model_factory()
    if isinstance(value, tuple):
        assert value == ()
        return
    json_value = value.model_dump_json()
    restored = type(value).model_validate_json(json_value)
    assert restored == value
    for field_name in getattr(restored, "model_fields", {}):
        field_value = getattr(restored, field_name)
        if isinstance(field_value, tuple):
            assert not hasattr(field_value, "append")


def test_diagnostic_json_round_trip_with_enum_values() -> None:
    diagnostic = TicketLintDiagnostic(
        diagnostic_id="LINT-0001",
        code=TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED,
        severity=TicketLintSeverity.ERROR,
        scope=TicketLintScope.COLLECTION,
        ticket_id=None,
        field_path="dependency_plan",
        message="Synthetic diagnostic.",
        remediation="Synthetic remediation.",
        blocking=True,
    )
    restored = TicketLintDiagnostic.model_validate_json(diagnostic.model_dump_json())
    assert restored.code is TicketLintRuleCode.DEPENDENCY_PLAN_REQUIRED


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_json_schemas_generate_with_no_unrestricted_payload(model: type) -> None:
    first_schema = model.model_json_schema()
    second_schema = model.model_json_schema()
    assert first_schema == second_schema
    assert first_schema["additionalProperties"] is False
    assert "properties" in first_schema
    for definition in first_schema.get("$defs", {}).values():
        if definition.get("type") == "object":
            assert definition.get("additionalProperties") is False


def test_public_fields_do_not_use_forbidden_shapes() -> None:
    forbidden_origins = {dict}
    for model in PUBLIC_MODELS:
        for field in model.model_fields.values():
            annotation = field.annotation
            assert annotation is not object
            assert get_origin(annotation) not in forbidden_origins
            assert "Any" not in str(annotation)
            assert "Path" not in str(annotation)
            assert "datetime" not in str(annotation)
            assert "UUID" not in str(annotation)
            assert "bytes" not in str(annotation)
            assert "Callable" not in str(annotation)


def test_enums_have_no_aliases_and_reject_unrestricted_strings() -> None:
    for enum_type in (
        TicketPolicyProfileName,
        TicketLintSeverity,
        TicketLintScope,
        TicketLintDisposition,
        TicketLintRuleCode,
    ):
        assert issubclass(enum_type, Enum)
        assert len(enum_type.__members__) == len(tuple(enum_type))
    with pytest.raises(ValidationError):
        TicketLintDiagnostic(
            diagnostic_id="LINT-0001",
            code="not_a_rule",
            severity=TicketLintSeverity.ERROR,
            scope=TicketLintScope.COLLECTION,
            ticket_id=None,
            field_path="x",
            message="Message.",
            remediation="Remediation.",
            blocking=True,
        )


def test_non_mutating_authority_surface_absent() -> None:
    forbidden_names = (
        "AutoFix",
        "TicketPatch",
        "TicketRewrite",
        "ApprovedTicket",
        "PublishedTicket",
        "CanonicalTicket",
        "ProposalWinner",
        "SynthesisResult",
        "WorkPacket",
        "ExecutionLane",
        "AgentAssignment",
        "WorkerAssignment",
        "WorktreeAssignment",
        "execute_validation_command",
        "load_ticket_policy_file",
        "resolve_network_authority",
        "graphify_update",
    )
    assert not any(hasattr(ticket_factory, name) for name in forbidden_names)


def test_linting_does_not_mutate_project_tickets_or_dependency_plan() -> None:
    first = ticket("P16.1")
    second = ticket("P16.2", deps=(dependency("P16.1"),))
    dependency_plan = plan(first, second)
    lint_request = request(first, second, dependency_plan=dependency_plan)
    project_before = lint_request.project_spec.model_dump(mode="json")
    tickets_before = tuple(
        item.model_dump(mode="json") for item in lint_request.tickets
    )
    plan_before = dependency_plan.model_dump(mode="json")
    lint_ticket_collection(lint_request)
    assert lint_request.project_spec.model_dump(mode="json") == project_before
    assert (
        tuple(item.model_dump(mode="json") for item in lint_request.tickets)
        == tickets_before
    )
    assert dependency_plan.model_dump(mode="json") == plan_before


def test_report_contains_no_fixed_ticket_patch_approval_publication_runtime_or_workpacket_state() -> (
    None
):
    report_json = lint_ticket_collection(request(ticket())).model_dump_json().casefold()
    forbidden_terms = (
        "autofix",
        "ticketpatch",
        "ticketrewrite",
        "approval_state",
        "publication_state",
        "runtime_state",
        "agent_identity",
        "worker_identity",
        "workpacket",
    )
    assert not any(term in report_json for term in forbidden_terms)


def test_required_imported_symbols_are_used() -> None:
    assert PROJECT_SPEC_SCHEMA_VERSION == 1
    assert TICKET_SPEC_SCHEMA_VERSION == 1
    assert CONTEXT_PACK_SCHEMA_VERSION == 1
    assert TICKET_GENERATOR_ROLE_SCHEMA_VERSION == 1
    assert DEPENDENCY_PLAN_SCHEMA_VERSION == 1
    assert ProjectSpec and TicketSpec and TicketDependencyPlan
    assert ContextPack and GeneratorAssignment and TicketProposal
    assert ContextAssemblyPolicy and ContextAssemblyRequest and ContextPackItem
    assert (
        ContextPackAssemblyError
        and ContextPackBudgetError
        and ContextPackSensitiveContentError
    )
    assert (
        ContextPriority
        and ContextSensitivity
        and ContextSourceKind
        and ContextSourceSpec
    )
    assert (
        OptionalSourceOverflowStrategy
        and ExternalDependencyResolution
        and ExternalDependencyState
    )
    assert (
        DependencyEdge
        and DependencyPlanningError
        and DependencyCollectionValidationError
    )
    assert DependencyCycleError and ScopeCollision and ScopeCollisionKind
    assert (
        TicketBlocker and TicketBlockerKind and ParallelPlanningPolicy and ParallelWave
    )
    assert TicketGenerationRequest and TicketGeneratorRole and GeneratorRoleProfile
    assert (
        TicketGeneratorRoleError
        and TicketGeneratorCompatibilityError
        and TicketProposalValidationError
    )
    assert (
        assemble_context_pack
        and build_ticket_proposal
        and get_ticket_generator_role_profile
    )
    assert list_ticket_generator_role_profiles and prepare_ticket_generator_assignments
    assert validate_ticket_generator_proposal and TicketPolicyError
    assert get_args and get_origin
