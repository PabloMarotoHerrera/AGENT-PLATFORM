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
    MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION,
    PROJECT_SPEC_SCHEMA_VERSION,
    TICKET_GENERATOR_ROLE_SCHEMA_VERSION,
    TICKET_POLICY_SCHEMA_VERSION,
    TICKET_SPEC_SCHEMA_VERSION,
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPack,
    ContextPriority,
    ContextSensitivity,
    ContextSourceKind,
    ContextSourceSpec,
    DependencyKind,
    DependencyScope,
    FieldResolutionKind,
    FieldSynthesisDecision,
    GeneratorAssignment,
    ParallelizationHint,
    ProjectSpec,
    ProposalAgreementLevel,
    ProposalConflict,
    ProposalConflictKind,
    ProposalConflictSeverity,
    ProposalVariantEvidence,
    RepositoryScopeSpec,
    ReviewedTicketProposal,
    SynthesizedTicketCandidate,
    TicketDependencyPlan,
    TicketDependencySpec,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    TicketPlanningRequest,
    TicketResponseContractSpec,
    TicketSpec,
    TicketSynthesisDisposition,
    TicketSynthesisError,
    TicketSynthesisField,
    TicketSynthesisInputError,
    TicketSynthesisRequest,
    TicketSynthesisReview,
    TicketSynthesisValidationError,
    TicketType,
    TicketValidationStepSpec,
    assemble_context_pack,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    build_ticket_synthesis_review,
    lint_ticket_collection,
    prepare_ticket_generator_assignments,
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
P16_5_EXPORTS = (
    "MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION",
    "TicketSynthesisField",
    "ProposalAgreementLevel",
    "FieldResolutionKind",
    "ProposalConflictKind",
    "ProposalConflictSeverity",
    "TicketSynthesisDisposition",
    "ReviewedTicketProposal",
    "TicketSynthesisRequest",
    "ProposalVariantEvidence",
    "FieldSynthesisDecision",
    "ProposalConflict",
    "SynthesizedTicketCandidate",
    "TicketSynthesisReview",
    "TicketSynthesisError",
    "TicketSynthesisInputError",
    "TicketSynthesisValidationError",
    "build_ticket_synthesis_review",
)
PUBLIC_MODELS = (
    ReviewedTicketProposal,
    TicketSynthesisRequest,
    ProposalVariantEvidence,
    FieldSynthesisDecision,
    ProposalConflict,
    SynthesizedTicketCandidate,
    TicketSynthesisReview,
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


def scope(
    *,
    allowed_paths: tuple[str, ...] = ("src/p16_5.py",),
    forbidden_actions: tuple[str, ...] = REQUIRED_FORBIDDEN_ACTION_MARKERS,
) -> RepositoryScopeSpec:
    return RepositoryScopeSpec(
        allowed_paths=allowed_paths,
        forbidden_paths=("4_external/sources/**",),
        allowed_actions=("edit deterministic synthesis review evidence",),
        forbidden_actions=forbidden_actions,
    )


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
        "completion_verdict": "synthetic_p16_5_ready",
    }
    data.update(overrides)
    return TicketResponseContractSpec.model_validate(data)


def validation_step(**overrides: object) -> TicketValidationStepSpec:
    data = {
        "validation_id": "V1",
        "description": "Run the synthetic synthesis validation.",
        "command": "python -m pytest synthetic_synthesis_tests.py",
        "expected_result": "The synthetic synthesis validation reports success.",
        "required": True,
    }
    data.update(overrides)
    return TicketValidationStepSpec.model_validate(data)


def dependency(
    ticket_id: str = "P99.1",
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


def project(**overrides: object) -> ProjectSpec:
    data = {
        "project_id": "P16",
        "title": "Synthetic synthesis project",
        "objective": "Validate deterministic noncanonical synthesis review evidence.",
        "summary": "This synthetic project validates P16.5 only.",
        "context": ("Synthetic planning context for synthesis.",),
        "authority_references": (authority(),),
        "scope": scope(allowed_paths=("src/**",)),
        "constraints": ("No execution authority is granted.",),
        "non_goals": ("No proposal execution or approval is authorized.",),
        "acceptance_criteria": (
            "The synthesis review reports deterministic evidence.",
        ),
        "completion_verdict": "synthetic_project_synthesis_ready",
    }
    data.update(overrides)
    return ProjectSpec.model_validate(data)


def ticket(
    ticket_id: str = "P16.5",
    *,
    title: str | None = None,
    objective: str | None = None,
    deps: tuple[TicketDependencySpec, ...] = (),
    ticket_scope: RepositoryScopeSpec | None = None,
    ticket_type: TicketType = TicketType.IMPLEMENTATION,
    project_id: str = "P16",
    response: TicketResponseContractSpec | None = None,
) -> TicketSpec:
    return TicketSpec(
        project_id=project_id,
        ticket_id=ticket_id,
        title=title or f"Synthetic synthesis ticket {ticket_id}",
        ticket_type=ticket_type,
        objective=objective or "Validate deterministic synthesis evidence.",
        context=("Synthetic ticket context for synthesis.",),
        authority_references=(authority(),),
        dependencies=deps,
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=ticket_scope
        or scope(allowed_paths=(f"src/{ticket_id.lower().replace('.', '_')}.py",)),
        constraints=("Rollback by restoring the prior synthesis contract.",),
        tasks=("Implement deterministic noncanonical synthesis evidence.",),
        acceptance_criteria=("Rollback evidence is retained for synthesis.",),
        validation_steps=(validation_step(),),
        response_contract=response
        or response_contract(
            completion_verdict=f"synthetic_{ticket_id.lower().replace('.', '_')}_ready"
        ),
        recommended_commit_message="P16.5 Add synthesis review evidence",
    )


def source(**overrides: object) -> ContextSourceSpec:
    data = {
        "source_id": "CTX-SYNTHESIS-EVIDENCE",
        "kind": ContextSourceKind.GOVERNANCE_RECORD,
        "title": "Synthetic synthesis evidence",
        "source_reference": "governance:synthetic-synthesis",
        "content": "Synthetic caller supplied content for synthesis review.",
        "authority_references": (),
        "sensitivity": ContextSensitivity.INTERNAL,
        "priority": ContextPriority.NORMAL,
        "required": False,
    }
    data.update(overrides)
    return ContextSourceSpec.model_validate(data)


def context_pack(
    *,
    project_spec: ProjectSpec | None = None,
    ticket_spec: TicketSpec | None = None,
    policy: ContextAssemblyPolicy | None = None,
) -> ContextPack:
    resolved_project = project_spec or project()
    resolved_ticket = ticket_spec or ticket()
    return assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=resolved_project,
            ticket_spec=resolved_ticket,
            sources=(source(),),
            policy=policy or ContextAssemblyPolicy(),
        )
    )


def generation_request(
    *,
    project_spec: ProjectSpec | None = None,
    ticket_spec: TicketSpec | None = None,
    roles: tuple[TicketGeneratorRole, ...] = (
        TicketGeneratorRole.ARCHITECTURE,
        TicketGeneratorRole.IMPLEMENTATION,
        TicketGeneratorRole.VALIDATION,
    ),
) -> TicketGenerationRequest:
    resolved_project = project_spec or project()
    resolved_ticket = ticket_spec or ticket()
    return TicketGenerationRequest(
        project_spec=resolved_project,
        ticket_spec=resolved_ticket,
        context_pack=context_pack(
            project_spec=resolved_project,
            ticket_spec=resolved_ticket,
        ),
        roles=roles,
    )


def lint_report_for(
    request: TicketGenerationRequest, proposed_ticket: TicketSpec
) -> TicketLintReport:
    return lint_ticket_collection(
        TicketLintRequest(
            project_spec=request.project_spec,
            tickets=(proposed_ticket,),
            dependency_plan=None,
            collection_complete=False,
        )
    )


def reviewed_proposal(
    request: TicketGenerationRequest,
    assignment: GeneratorAssignment,
    proposed_ticket: TicketSpec,
) -> ReviewedTicketProposal:
    proposal = build_ticket_proposal(
        assignment=assignment,
        proposed_ticket=proposed_ticket,
        rationale=f"Synthetic {assignment.role.value} rationale for synthesis review.",
        evidence_source_ids=("CTX-PROJECT-SPEC",),
    )
    return ReviewedTicketProposal(
        proposal=proposal,
        lint_report=lint_report_for(request, proposed_ticket),
    )


def synthesis_request(
    *,
    seed: TicketSpec | None = None,
    roles: tuple[TicketGeneratorRole, ...] = (
        TicketGeneratorRole.ARCHITECTURE,
        TicketGeneratorRole.IMPLEMENTATION,
        TicketGeneratorRole.VALIDATION,
    ),
    proposed_tickets: tuple[TicketSpec, ...] | None = None,
    dependency_plan: TicketDependencyPlan | None = None,
    reverse_inputs: bool = False,
) -> TicketSynthesisRequest:
    resolved_seed = seed or ticket()
    req = generation_request(ticket_spec=resolved_seed, roles=roles)
    assignments = prepare_ticket_generator_assignments(req)
    proposals = proposed_tickets or tuple(resolved_seed for _assignment in assignments)
    reviewed = tuple(
        reviewed_proposal(req, assignment, proposed_ticket)
        for assignment, proposed_ticket in zip(assignments, proposals, strict=True)
    )
    if reverse_inputs:
        assignments = tuple(reversed(assignments))
        reviewed = tuple(reversed(reviewed))
    return TicketSynthesisRequest(
        generation_request=req,
        assignments=assignments,
        reviewed_proposals=reviewed,
        dependency_plan=dependency_plan,
    )


def decision_by_field(
    review: TicketSynthesisReview, field: TicketSynthesisField
) -> FieldSynthesisDecision:
    return next(
        decision for decision in review.field_decisions if decision.field is field
    )


def conflict_kinds(review: TicketSynthesisReview) -> tuple[ProposalConflictKind, ...]:
    return tuple(conflict.kind for conflict in review.conflicts)


def assert_validation_fails(factory: Callable[[], object]) -> None:
    with pytest.raises(ValidationError):
        factory()


SYNTHESIS_FIELDS = tuple(TicketSynthesisField)
ALL_GENERATOR_ROLES = tuple(TicketGeneratorRole)
CANONICAL_THREE_ROLE_ORDER = (
    TicketGeneratorRole.ARCHITECTURE,
    TicketGeneratorRole.IMPLEMENTATION,
    TicketGeneratorRole.VALIDATION,
)
ATOMIC_TUPLE_FIELDS = (
    TicketSynthesisField.CONTEXT,
    TicketSynthesisField.AUTHORITY_REFERENCES,
    TicketSynthesisField.DEPENDENCIES,
    TicketSynthesisField.CONSTRAINTS,
    TicketSynthesisField.TASKS,
    TicketSynthesisField.ACCEPTANCE_CRITERIA,
    TicketSynthesisField.VALIDATION_STEPS,
)


def _label_token(label: str) -> str:
    return label.lower().replace("_", "-")


def _label_slug(label: str) -> str:
    return label.lower().replace("-", "_")


def _dependency_ticket_id_for_label(label: str) -> str:
    if "first" in label:
        return "P99.41"
    if "second" in label:
        return "P99.42"
    if "third" in label:
        return "P99.43"
    if "majority" in label:
        return "P99.51"
    if "dissent" in label:
        return "P99.52"
    if "warning" in label:
        return "P99.61"
    return "P99.31"


def field_value(field: TicketSynthesisField, label: str) -> object:
    token = _label_token(label)
    slug = _label_slug(label)
    if field is TicketSynthesisField.TITLE:
        return f"Synthetic {label} synthesis title"
    if field is TicketSynthesisField.OBJECTIVE:
        return f"Validate distinct {label} synthesis objective evidence."
    if field is TicketSynthesisField.CONTEXT:
        return (f"Synthetic {label} context evidence is atomic.",)
    if field is TicketSynthesisField.AUTHORITY_REFERENCES:
        return (
            authority(
                value=f"0_architecture/governance/{token}.md",
                rationale=f"Synthetic {label} authority reference.",
            ).model_dump(mode="json"),
        )
    if field is TicketSynthesisField.DEPENDENCIES:
        return (
            dependency(_dependency_ticket_id_for_label(label)).model_dump(mode="json"),
        )
    if field is TicketSynthesisField.PARALLELIZATION_HINT:
        if "second" in label or "dissent" in label:
            return ParallelizationHint.SERIAL.value
        if "third" in label:
            return ParallelizationHint.UNSPECIFIED.value
        return ParallelizationHint.PARALLEL_CANDIDATE.value
    if field is TicketSynthesisField.SCOPE:
        return scope(allowed_paths=(f"src/{token}/**",)).model_dump(mode="json")
    if field is TicketSynthesisField.CONSTRAINTS:
        return (f"Rollback by restoring prior {label} synthesis evidence.",)
    if field is TicketSynthesisField.TASKS:
        return (f"Implement deterministic {label} synthesis review evidence.",)
    if field is TicketSynthesisField.ACCEPTANCE_CRITERIA:
        return (f"The {label} synthesis evidence is reviewable and reversible.",)
    if field is TicketSynthesisField.VALIDATION_STEPS:
        return (
            validation_step(
                validation_id="V2",
                description=f"Run the {label} synthesis validation.",
                command=f"python -m pytest synthetic_{slug}_synthesis_tests.py",
                expected_result=f"The {label} synthesis validation reports success.",
            ).model_dump(mode="json"),
        )
    if field is TicketSynthesisField.RESPONSE_CONTRACT:
        return response_contract(
            completion_verdict=f"synthetic_{slug}_synthesis_ready"
        ).model_dump(mode="json")
    if field is TicketSynthesisField.RECOMMENDED_COMMIT_MESSAGE:
        return f"P16.5 Add {label} synthesis review evidence"
    raise AssertionError(f"unhandled field: {field}")


def ticket_with_field(
    field: TicketSynthesisField,
    label: str,
    *,
    base: TicketSpec | None = None,
) -> TicketSpec:
    data = (base or ticket()).model_dump(mode="json")
    data[field.value] = field_value(field, label)
    return TicketSpec.model_validate(data)


def dumped_field(ticket_spec: TicketSpec, field: TicketSynthesisField) -> object:
    return ticket_spec.model_dump(mode="json")[field.value]


def reviewed_with_lint_report(
    reviewed: ReviewedTicketProposal, lint_report: TicketLintReport
) -> ReviewedTicketProposal:
    return ReviewedTicketProposal(proposal=reviewed.proposal, lint_report=lint_report)


def synthesis_request_with_reviewed(
    request: TicketSynthesisRequest,
    reviewed: tuple[ReviewedTicketProposal, ...],
    *,
    dependency_plan: TicketDependencyPlan | None = None,
) -> TicketSynthesisRequest:
    return TicketSynthesisRequest.model_construct(
        generation_request=request.generation_request,
        assignments=request.assignments,
        reviewed_proposals=reviewed,
        dependency_plan=dependency_plan,
    )


def build_warning_lint_report(
    request: TicketGenerationRequest, proposed_ticket: TicketSpec
) -> TicketLintReport:
    warning_ticket = ticket_with_field(
        TicketSynthesisField.DEPENDENCIES,
        "warning-soft-external",
        base=proposed_ticket,
    )
    warning_plan = build_ticket_dependency_plan(
        TicketPlanningRequest(
            project_spec=request.project_spec, tickets=(warning_ticket,)
        )
    )
    return lint_ticket_collection(
        TicketLintRequest(
            project_spec=request.project_spec,
            tickets=(warning_ticket,),
            dependency_plan=warning_plan,
            collection_complete=False,
        )
    )


def test_p16_5_exports_import_correctly() -> None:
    assert MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION == 1
    assert TicketSynthesisField.TITLE.value == "title"
    assert ProposalAgreementLevel.SPLIT.value == "split"
    assert FieldResolutionKind.PRESERVE_SEED.value == "preserve_seed"
    assert ProposalConflictKind.FIELD_DISSENT.value == "field_dissent"
    assert ProposalConflictSeverity.BLOCKING.value == "blocking"
    assert TicketSynthesisDisposition.REVIEW_READY.value == "review_ready"
    assert build_ticket_synthesis_review.__name__ == "build_ticket_synthesis_review"


def test_public_export_groups_preserve_relative_order() -> None:
    exported = ticket_factory.__all__
    assert len(P16_5_EXPORTS) == 18
    assert len(exported) == len(frozenset(exported))
    for group in (
        P16_0_EXPORTS,
        P16_1_EXPORTS,
        P16_2_EXPORTS,
        P16_3_EXPORTS,
        P16_4_EXPORTS,
        P16_5_EXPORTS,
    ):
        positions = [exported.index(name) for name in group]
        assert positions == sorted(positions)
    assert exported[-len(P16_4_EXPORTS) :] == P16_4_EXPORTS
    assert "SYNTHESIS_REVIEW_DIGEST_ALGORITHM" not in exported


def test_no_import_time_filesystem_or_network_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module_name = "hermes_cli.agent_platform.ticket_factory.proposal_synthesis"
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
    assert imported.MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION == 1


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_are_frozen_and_extra_forbid(model: type) -> None:
    assert model.model_config["frozen"] is True
    assert model.model_config["extra"] == "forbid"
    assert model.model_config["validate_default"] is True
    assert model.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize(
    "model, data",
    [
        (
            ReviewedTicketProposal,
            lambda: synthesis_request().reviewed_proposals[0].model_dump(mode="json"),
        ),
        (TicketSynthesisRequest, lambda: synthesis_request().model_dump(mode="json")),
        (
            ProposalVariantEvidence,
            lambda: decision_by_field(
                build_ticket_synthesis_review(synthesis_request()),
                TicketSynthesisField.TITLE,
            )
            .variants[0]
            .model_dump(mode="json"),
        ),
        (
            FieldSynthesisDecision,
            lambda: build_ticket_synthesis_review(synthesis_request())
            .field_decisions[0]
            .model_dump(mode="json"),
        ),
        (
            ProposalConflict,
            lambda: build_ticket_synthesis_review(
                synthesis_request(
                    roles=(
                        TicketGeneratorRole.ARCHITECTURE,
                        TicketGeneratorRole.IMPLEMENTATION,
                    ),
                    proposed_tickets=(
                        ticket(title="Split A"),
                        ticket(title="Split B"),
                    ),
                )
            )
            .conflicts[0]
            .model_dump(mode="json"),
        ),
        (
            SynthesizedTicketCandidate,
            lambda: build_ticket_synthesis_review(
                synthesis_request()
            ).candidate.model_dump(mode="json"),
        ),
        (
            TicketSynthesisReview,
            lambda: build_ticket_synthesis_review(synthesis_request()).model_dump(
                mode="json"
            ),
        ),
    ],
)
def test_public_models_reject_unknown_fields(
    model: type, data: Callable[[], dict[str, object]]
) -> None:
    payload = data()
    payload["unexpected"] = "value"
    assert_validation_fails(lambda: model.model_validate(payload))


def test_schema_version_defaults_and_alternatives_are_rejected() -> None:
    review = build_ticket_synthesis_review(synthesis_request())
    assert review.schema_version == 1
    assert review.candidate is not None
    assert review.candidate.schema_version == 1
    review_data = review.model_dump(mode="json")
    review_data["schema_version"] = 2
    assert_validation_fails(lambda: TicketSynthesisReview.model_validate(review_data))
    candidate_data = review.candidate.model_dump(mode="json")
    candidate_data["schema_version"] = 2
    assert_validation_fails(
        lambda: SynthesizedTicketCandidate.model_validate(candidate_data)
    )


def test_unanimous_review_builds_review_ready_noncanonical_candidate() -> None:
    review = build_ticket_synthesis_review(synthesis_request())
    assert review.disposition is TicketSynthesisDisposition.REVIEW_READY
    assert review.conflicts == ()
    assert review.candidate is not None
    assert review.candidate.candidate_id == "CAND-P16-5"
    assert review.candidate.synthesized_ticket == ticket()
    assert len(review.field_decisions) == len(tuple(TicketSynthesisField))
    assert all(
        decision.agreement_level is ProposalAgreementLevel.UNANIMOUS
        for decision in review.field_decisions
    )
    assert all(
        decision.resolution is FieldResolutionKind.ADOPT_UNANIMOUS
        for decision in review.field_decisions
    )
    assert not hasattr(review, "approved")
    assert not hasattr(review.candidate, "canonical")
    assert not hasattr(review.candidate, "published")


def test_strict_majority_field_is_adopted_with_dissent_evidence() -> None:
    majority = ticket(title="Majority synthesis title")
    dissent = ticket(title="Dissent synthesis title")
    request = synthesis_request(proposed_tickets=(majority, majority, dissent))
    review = build_ticket_synthesis_review(request)
    title_decision = decision_by_field(review, TicketSynthesisField.TITLE)
    assert review.candidate is not None
    assert review.candidate.synthesized_ticket.title == "Majority synthesis title"
    assert title_decision.agreement_level is ProposalAgreementLevel.STRICT_MAJORITY
    assert title_decision.resolution is FieldResolutionKind.ADOPT_STRICT_MAJORITY
    assert title_decision.variants[0].support_count == 2
    assert len(title_decision.dissenting_proposal_SHA256s) == 1
    assert conflict_kinds(review) == (ProposalConflictKind.FIELD_DISSENT,)
    assert review.disposition is TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT


def test_split_field_preserves_seed_and_requires_human_resolution() -> None:
    seed = ticket(objective="Seed objective remains authoritative for split.")
    first = ticket(objective="Architecture objective variant.")
    second = ticket(objective="Implementation objective variant.")
    request = synthesis_request(
        seed=seed,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(first, second),
    )
    review = build_ticket_synthesis_review(request)
    objective_decision = decision_by_field(review, TicketSynthesisField.OBJECTIVE)
    assert review.candidate is not None
    assert review.candidate.synthesized_ticket.objective == seed.objective
    assert objective_decision.agreement_level is ProposalAgreementLevel.SPLIT
    assert objective_decision.resolution is FieldResolutionKind.PRESERVE_SEED
    assert objective_decision.supporting_proposal_SHA256s == ()
    assert len(objective_decision.dissenting_proposal_SHA256s) == 2
    assert conflict_kinds(review) == (ProposalConflictKind.FIELD_SPLIT,)
    assert review.disposition is TicketSynthesisDisposition.HUMAN_RESOLUTION_REQUIRED


def test_lint_blocked_proposals_are_excluded_from_voting() -> None:
    blocked = ticket(ticket_scope=scope(allowed_paths=()))
    request = synthesis_request(proposed_tickets=(ticket(), ticket(), blocked))
    review = build_ticket_synthesis_review(request)
    blocked_reviewed = request.reviewed_proposals[2]
    assert blocked_reviewed.lint_report.disposition is TicketLintDisposition.BLOCKED
    assert review.excluded_proposal_SHA256s == (
        blocked_reviewed.proposal.proposal_SHA256,
    )
    assert review.candidate is not None
    assert blocked_reviewed.proposal.proposal_SHA256 not in (
        review.candidate.source_proposal_SHA256s
    )
    assert conflict_kinds(review) == (ProposalConflictKind.LINT_BLOCKED_PROPOSAL,)
    assert review.disposition is TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT


def test_insufficient_eligible_proposals_blocks_candidate_construction() -> None:
    blocked = ticket(ticket_scope=scope(allowed_paths=()))
    request = synthesis_request(
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(ticket(), blocked),
    )
    review = build_ticket_synthesis_review(request)
    assert review.candidate is None
    assert review.field_decisions == ()
    assert review.disposition is TicketSynthesisDisposition.BLOCKED
    assert ProposalConflictKind.INSUFFICIENT_ELIGIBLE_PROPOSALS in conflict_kinds(
        review
    )
    assert any(conflict.blocking for conflict in review.conflicts)


def test_candidate_lint_blocked_conflict_is_blocking_review_evidence() -> None:
    seed = ticket(ticket_scope=scope(allowed_paths=()))
    first = ticket(ticket_scope=scope(allowed_paths=("src/a.py",)))
    second = ticket(ticket_scope=scope(allowed_paths=("src/b.py",)))
    request = synthesis_request(
        seed=seed,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(first, second),
    )
    review = build_ticket_synthesis_review(request)
    assert review.candidate is not None
    assert review.candidate.candidate_lint_report.disposition is (
        TicketLintDisposition.BLOCKED
    )
    assert ProposalConflictKind.CANDIDATE_LINT_BLOCKED in conflict_kinds(review)
    assert review.disposition is TicketSynthesisDisposition.BLOCKED


def test_dependency_plan_staleness_is_reported_without_rebuilding_plan() -> None:
    seed = ticket()
    plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(seed,))
    )
    changed = ticket(deps=(dependency("P99.1"),))
    request = synthesis_request(
        seed=seed,
        proposed_tickets=(changed, changed, seed),
        dependency_plan=plan,
    )
    before = plan.model_dump(mode="json")
    review = build_ticket_synthesis_review(request)
    assert review.candidate is not None
    assert review.candidate.synthesized_ticket.dependencies == changed.dependencies
    assert ProposalConflictKind.DEPENDENCY_PLAN_STALE in conflict_kinds(review)
    assert review.disposition is TicketSynthesisDisposition.HUMAN_RESOLUTION_REQUIRED
    assert plan.model_dump(mode="json") == before


def test_input_permutation_produces_identical_review_evidence() -> None:
    majority = ticket(title="Majority synthesis title")
    dissent = ticket(title="Dissent synthesis title")
    first = synthesis_request(proposed_tickets=(majority, majority, dissent))
    second = synthesis_request(
        proposed_tickets=(majority, majority, dissent),
        reverse_inputs=True,
    )
    assert build_ticket_synthesis_review(first) == build_ticket_synthesis_review(second)


def test_digest_evidence_is_stable_sensitive_and_self_excluding() -> None:
    first = build_ticket_synthesis_review(synthesis_request())
    second = build_ticket_synthesis_review(synthesis_request())
    changed = build_ticket_synthesis_review(
        synthesis_request(proposed_tickets=(ticket(title="Changed"),) * 3)
    )
    assert first.synthesis_input_SHA256 == second.synthesis_input_SHA256
    assert first.review_SHA256 == second.review_SHA256
    assert first.review_SHA256 != changed.review_SHA256
    assert first.candidate is not None
    assert len(first.synthesis_input_SHA256) == 64
    assert first.synthesis_input_SHA256 == first.synthesis_input_SHA256.lower()
    assert first.candidate.candidate_SHA256 != first.review_SHA256
    tampered_review = first.model_dump(mode="json")
    tampered_review["review_SHA256"] = "0" * 64
    assert_validation_fails(
        lambda: TicketSynthesisReview.model_validate(tampered_review)
    )
    tampered_candidate = first.candidate.model_dump(mode="json")
    tampered_candidate["candidate_SHA256"] = "0" * 64
    assert_validation_fails(
        lambda: SynthesizedTicketCandidate.model_validate(tampered_candidate)
    )


def test_request_validation_rejects_assignment_and_proposal_binding_drift() -> None:
    request = synthesis_request()
    assignments = request.assignments[:-1]
    bad_assignment_request = TicketSynthesisRequest.model_construct(
        generation_request=request.generation_request,
        assignments=assignments,
        reviewed_proposals=request.reviewed_proposals,
        dependency_plan=None,
    )
    with pytest.raises(TicketSynthesisInputError):
        build_ticket_synthesis_review(bad_assignment_request)

    reviewed = request.reviewed_proposals[0]
    tampered_proposal = reviewed.proposal.model_copy(
        update={"proposal_SHA256": "0" * 64}
    )
    bad_reviewed = ReviewedTicketProposal.model_construct(
        proposal=tampered_proposal,
        lint_report=reviewed.lint_report,
    )
    bad_proposal_request = TicketSynthesisRequest.model_construct(
        generation_request=request.generation_request,
        assignments=request.assignments,
        reviewed_proposals=(bad_reviewed, *request.reviewed_proposals[1:]),
        dependency_plan=None,
    )
    with pytest.raises(TicketSynthesisValidationError):
        build_ticket_synthesis_review(bad_proposal_request)


def test_lint_report_binding_must_match_proposal_ticket() -> None:
    request = synthesis_request()
    reviewed = request.reviewed_proposals[0]
    mismatched_report = lint_report_for(request.generation_request, ticket("P16.6"))
    bad_reviewed = ReviewedTicketProposal.model_construct(
        proposal=reviewed.proposal,
        lint_report=mismatched_report,
    )
    bad_request = TicketSynthesisRequest.model_construct(
        generation_request=request.generation_request,
        assignments=request.assignments,
        reviewed_proposals=(bad_reviewed, *request.reviewed_proposals[1:]),
        dependency_plan=None,
    )
    with pytest.raises(TicketSynthesisValidationError):
        build_ticket_synthesis_review(bad_request)


def test_manual_contract_enforces_conflict_severity_and_candidate_consistency() -> None:
    with pytest.raises(ValidationError):
        ProposalConflict(
            conflict_id="CONFLICT-0001",
            kind=ProposalConflictKind.FIELD_SPLIT,
            severity=ProposalConflictSeverity.HUMAN_REVIEW_REQUIRED,
            field=None,
            proposal_SHA256=None,
            related_proposal_SHA256s=(),
            message="Synthetic conflict.",
            remediation="Synthetic remediation.",
            blocking=False,
        )
    review = build_ticket_synthesis_review(synthesis_request())
    assert review.candidate is not None
    tampered = review.model_copy(
        update={
            "candidate": review.candidate.model_copy(
                update={"source_proposal_SHA256s": review.proposal_SHA256s[:1]}
            )
        }
    ).model_dump(mode="json")
    tampered["review_SHA256"] = review.review_SHA256
    assert_validation_fails(lambda: TicketSynthesisReview.model_validate(tampered))


def test_serialization_round_trip_and_tuple_immutability() -> None:
    request = synthesis_request()
    review = build_ticket_synthesis_review(request)
    assert (
        TicketSynthesisRequest.model_validate_json(request.model_dump_json()) == request
    )
    assert TicketSynthesisReview.model_validate_json(review.model_dump_json()) == review
    assert review.candidate is not None
    assert (
        SynthesizedTicketCandidate.model_validate_json(
            review.candidate.model_dump_json()
        )
        == review.candidate
    )
    with pytest.raises(AttributeError):
        review.proposal_SHA256s.append("0" * 64)
    with pytest.raises(AttributeError):
        review.field_decisions[0].variants.append(review.field_decisions[0].variants[0])


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_json_schemas_generate_with_no_unrestricted_payload(model: type) -> None:
    schema = model.model_json_schema()
    assert schema == model.model_json_schema()
    assert schema["additionalProperties"] is False
    assert "properties" in schema
    for definition in schema.get("$defs", {}).values():
        if definition.get("type") == "object":
            assert definition.get("additionalProperties") is False


def test_public_fields_do_not_use_forbidden_shapes() -> None:
    for model in PUBLIC_MODELS:
        for field in model.model_fields.values():
            annotation = field.annotation
            assert annotation is not object
            assert get_origin(annotation) is not dict
            assert "Any" not in str(annotation)
            assert "Path" not in str(annotation)
            assert "datetime" not in str(annotation)
            assert "UUID" not in str(annotation)
            assert "bytes" not in str(annotation)
            assert "Callable" not in str(annotation)


def test_enum_values_and_aliases() -> None:
    assert tuple(item.value for item in TicketSynthesisField) == (
        "title",
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
    assert tuple(item.value for item in ProposalAgreementLevel) == (
        "unanimous",
        "strict_majority",
        "split",
    )
    assert tuple(item.value for item in TicketSynthesisDisposition) == (
        "review_ready",
        "review_ready_with_dissent",
        "human_resolution_required",
        "blocked",
    )
    for enum_type in (
        TicketSynthesisField,
        ProposalAgreementLevel,
        FieldResolutionKind,
        ProposalConflictKind,
        ProposalConflictSeverity,
        TicketSynthesisDisposition,
    ):
        assert issubclass(enum_type, Enum)
        assert len(enum_type.__members__) == len(tuple(enum_type))


def test_public_model_field_order() -> None:
    assert tuple(ReviewedTicketProposal.model_fields) == ("proposal", "lint_report")
    assert tuple(TicketSynthesisRequest.model_fields) == (
        "generation_request",
        "assignments",
        "reviewed_proposals",
        "dependency_plan",
    )
    assert tuple(ProposalVariantEvidence.model_fields) == (
        "variant_SHA256",
        "support_count",
        "supporting_proposal_SHA256s",
        "supporting_roles",
    )
    assert tuple(FieldSynthesisDecision.model_fields) == (
        "field",
        "agreement_level",
        "resolution",
        "seed_value_SHA256",
        "selected_value_SHA256",
        "variants",
        "supporting_proposal_SHA256s",
        "dissenting_proposal_SHA256s",
    )
    assert tuple(ProposalConflict.model_fields) == (
        "conflict_id",
        "kind",
        "severity",
        "field",
        "proposal_SHA256",
        "related_proposal_SHA256s",
        "message",
        "remediation",
        "blocking",
    )
    assert tuple(SynthesizedTicketCandidate.model_fields) == (
        "schema_version",
        "candidate_id",
        "project_id",
        "ticket_id",
        "synthesized_ticket",
        "source_proposal_SHA256s",
        "excluded_proposal_SHA256s",
        "field_decisions",
        "unresolved_conflict_ids",
        "candidate_lint_report",
        "candidate_SHA256",
    )
    assert tuple(TicketSynthesisReview.model_fields) == (
        "schema_version",
        "project_id",
        "ticket_id",
        "synthesis_input_SHA256",
        "proposal_SHA256s",
        "eligible_proposal_SHA256s",
        "excluded_proposal_SHA256s",
        "field_decisions",
        "conflicts",
        "candidate",
        "disposition",
        "review_SHA256",
    )


def test_no_execution_approval_publication_or_workpacket_surface_exists() -> None:
    forbidden_names = (
        "ProposalSynthesizer",
        "ProposalWinner",
        "ApprovalRequest",
        "ApprovalDecision",
        "PublishedTicket",
        "CanonicalTicket",
        "WorkPacket",
        "ExecutionLane",
        "AgentAssignment",
        "WorkerAssignment",
        "WorktreeAssignment",
        "run_generator",
        "execute_generator",
        "execute_validation_command",
        "load_ticket_file",
        "save_ticket_file",
        "graphify_update",
    )
    assert not any(hasattr(ticket_factory, name) for name in forbidden_names)
    review_json = build_ticket_synthesis_review(synthesis_request()).model_dump_json()
    forbidden_terms = (
        "approval_state",
        "publication_state",
        "runtime_state",
        "agent_identity",
        "worker_identity",
        "workpacket",
        "canonical_ticket",
    )
    assert not any(term in review_json.casefold() for term in forbidden_terms)


def test_synthesis_does_not_mutate_inputs() -> None:
    request = synthesis_request()
    request_before = request.model_dump(mode="json")
    assignments_before = tuple(
        assignment.model_dump(mode="json") for assignment in request.assignments
    )
    proposals_before = tuple(
        proposal.model_dump(mode="json") for proposal in request.reviewed_proposals
    )
    build_ticket_synthesis_review(request)
    assert request.model_dump(mode="json") == request_before
    assert (
        tuple(assignment.model_dump(mode="json") for assignment in request.assignments)
        == assignments_before
    )
    assert (
        tuple(
            proposal.model_dump(mode="json") for proposal in request.reviewed_proposals
        )
        == proposals_before
    )


def test_exception_hierarchy_and_required_imported_symbols_are_used() -> None:
    assert issubclass(TicketSynthesisInputError, TicketSynthesisError)
    assert issubclass(TicketSynthesisValidationError, TicketSynthesisError)
    assert issubclass(TicketSynthesisError, ValueError)
    assert PROJECT_SPEC_SCHEMA_VERSION == 1
    assert TICKET_SPEC_SCHEMA_VERSION == 1
    assert CONTEXT_PACK_SCHEMA_VERSION == 1
    assert TICKET_GENERATOR_ROLE_SCHEMA_VERSION == 1
    assert DEPENDENCY_PLAN_SCHEMA_VERSION == 1
    assert TICKET_POLICY_SCHEMA_VERSION == 1
    assert ProjectSpec and TicketSpec and ContextPack and TicketDependencyPlan
    assert GeneratorAssignment and TicketGenerationRequest and TicketLintReport
    assert get_args and get_origin and Callable


@pytest.mark.parametrize("field", SYNTHESIS_FIELDS)
def test_unanimous_decision_for_each_field_uses_canonical_role_support(
    field: TicketSynthesisField,
) -> None:
    proposed = ticket_with_field(field, f"unanimous-{field.value}")
    review = build_ticket_synthesis_review(
        synthesis_request(proposed_tickets=(proposed, proposed, proposed))
    )
    decision = decision_by_field(review, field)
    assert review.candidate is not None
    assert dumped_field(review.candidate.synthesized_ticket, field) == dumped_field(
        proposed, field
    )
    assert decision.agreement_level is ProposalAgreementLevel.UNANIMOUS
    assert decision.resolution is FieldResolutionKind.ADOPT_UNANIMOUS
    assert decision.variants[0].support_count == 3
    assert decision.variants[0].supporting_roles == CANONICAL_THREE_ROLE_ORDER
    assert decision.supporting_proposal_SHA256s == review.proposal_SHA256s
    assert decision.dissenting_proposal_SHA256s == ()


@pytest.mark.parametrize("field", SYNTHESIS_FIELDS)
def test_strict_majority_adopts_each_field_and_preserves_dissent(
    field: TicketSynthesisField,
) -> None:
    majority = ticket_with_field(field, f"majority-{field.value}")
    dissent = ticket_with_field(field, f"dissent-{field.value}")
    review = build_ticket_synthesis_review(
        synthesis_request(proposed_tickets=(majority, majority, dissent))
    )
    decision = decision_by_field(review, field)
    assert review.candidate is not None
    assert dumped_field(review.candidate.synthesized_ticket, field) == dumped_field(
        majority, field
    )
    assert decision.agreement_level is ProposalAgreementLevel.STRICT_MAJORITY
    assert decision.resolution is FieldResolutionKind.ADOPT_STRICT_MAJORITY
    assert decision.variants[0].support_count == 2
    assert decision.variants[1].support_count == 1
    assert len(decision.supporting_proposal_SHA256s) == 2
    assert len(decision.dissenting_proposal_SHA256s) == 1
    assert ProposalConflictKind.FIELD_DISSENT in conflict_kinds(review)


@pytest.mark.parametrize("field", SYNTHESIS_FIELDS)
def test_two_way_split_preserves_seed_for_each_field(
    field: TicketSynthesisField,
) -> None:
    seed = ticket_with_field(field, f"seed-{field.value}")
    first = ticket_with_field(field, f"first-{field.value}", base=seed)
    second = ticket_with_field(field, f"second-{field.value}", base=seed)
    review = build_ticket_synthesis_review(
        synthesis_request(
            seed=seed,
            roles=(
                TicketGeneratorRole.ARCHITECTURE,
                TicketGeneratorRole.IMPLEMENTATION,
            ),
            proposed_tickets=(first, second),
        )
    )
    decision = decision_by_field(review, field)
    assert review.candidate is not None
    assert dumped_field(review.candidate.synthesized_ticket, field) == dumped_field(
        seed, field
    )
    assert decision.agreement_level is ProposalAgreementLevel.SPLIT
    assert decision.resolution is FieldResolutionKind.PRESERVE_SEED
    assert decision.selected_value_SHA256 == decision.seed_value_SHA256
    assert decision.supporting_proposal_SHA256s == ()
    assert len(decision.dissenting_proposal_SHA256s) == 2


@pytest.mark.parametrize("field", SYNTHESIS_FIELDS)
def test_three_way_split_rejects_plurality_for_each_field(
    field: TicketSynthesisField,
) -> None:
    seed = ticket_with_field(field, f"seed-three-way-{field.value}")
    first = ticket_with_field(field, f"first-three-way-{field.value}", base=seed)
    second = ticket_with_field(field, f"second-three-way-{field.value}", base=seed)
    third = ticket_with_field(field, f"third-three-way-{field.value}", base=seed)
    review = build_ticket_synthesis_review(
        synthesis_request(seed=seed, proposed_tickets=(first, second, third))
    )
    decision = decision_by_field(review, field)
    assert review.candidate is not None
    assert dumped_field(review.candidate.synthesized_ticket, field) == dumped_field(
        seed, field
    )
    assert decision.agreement_level is ProposalAgreementLevel.SPLIT
    assert all(variant.support_count == 1 for variant in decision.variants)
    assert tuple(variant.variant_SHA256 for variant in decision.variants) == tuple(
        sorted(variant.variant_SHA256 for variant in decision.variants)
    )
    assert ProposalConflictKind.FIELD_SPLIT in conflict_kinds(review)


@pytest.mark.parametrize("field", SYNTHESIS_FIELDS)
def test_digest_evidence_is_sensitive_to_each_synthesis_field(
    field: TicketSynthesisField,
) -> None:
    base_review = build_ticket_synthesis_review(synthesis_request())
    proposed = ticket_with_field(field, f"digest-{field.value}")
    changed_review = build_ticket_synthesis_review(
        synthesis_request(proposed_tickets=(proposed, proposed, proposed))
    )
    assert base_review.synthesis_input_SHA256 != changed_review.synthesis_input_SHA256
    assert base_review.review_SHA256 != changed_review.review_SHA256
    assert base_review.candidate is not None
    assert changed_review.candidate is not None
    assert base_review.candidate.candidate_SHA256 != (
        changed_review.candidate.candidate_SHA256
    )


@pytest.mark.parametrize("field", ATOMIC_TUPLE_FIELDS)
def test_atomic_tuple_and_nested_fields_are_not_merged(
    field: TicketSynthesisField,
) -> None:
    majority = ticket_with_field(field, f"atomic-majority-{field.value}")
    dissent = ticket_with_field(field, f"atomic-dissent-{field.value}")
    review = build_ticket_synthesis_review(
        synthesis_request(proposed_tickets=(majority, majority, dissent))
    )
    assert review.candidate is not None
    assert dumped_field(review.candidate.synthesized_ticket, field) == dumped_field(
        majority, field
    )
    assert dumped_field(review.candidate.synthesized_ticket, field) != dumped_field(
        dissent, field
    )


def test_pass_with_warnings_lint_report_remains_eligible() -> None:
    request = synthesis_request(
        proposed_tickets=(
            ticket_with_field(
                TicketSynthesisField.DEPENDENCIES, "warning-soft-external"
            ),
            ticket(),
            ticket(),
        )
    )
    warning_report = build_warning_lint_report(
        request.generation_request,
        request.reviewed_proposals[0].proposal.proposed_ticket,
    )
    assert warning_report.disposition is TicketLintDisposition.PASS_WITH_WARNINGS
    reviewed = (
        reviewed_with_lint_report(request.reviewed_proposals[0], warning_report),
        *request.reviewed_proposals[1:],
    )
    review = build_ticket_synthesis_review(
        synthesis_request_with_reviewed(request, reviewed)
    )
    assert request.reviewed_proposals[0].proposal.proposal_SHA256 in (
        review.eligible_proposal_SHA256s
    )
    assert request.reviewed_proposals[0].proposal.proposal_SHA256 not in (
        review.excluded_proposal_SHA256s
    )
    assert review.candidate is not None


def test_scope_plan_staleness_is_reported_without_rebuilding_plan() -> None:
    seed = ticket()
    plan = build_ticket_dependency_plan(
        TicketPlanningRequest(project_spec=project(), tickets=(seed,))
    )
    changed = ticket_with_field(
        TicketSynthesisField.SCOPE, "scope-plan-stale", base=seed
    )
    before = plan.model_dump(mode="json")
    review = build_ticket_synthesis_review(
        synthesis_request(
            seed=seed, proposed_tickets=(changed, changed, seed), dependency_plan=plan
        )
    )
    assert ProposalConflictKind.SCOPE_PLAN_STALE in conflict_kinds(review)
    assert review.disposition is TicketSynthesisDisposition.HUMAN_RESOLUTION_REQUIRED
    assert plan.model_dump(mode="json") == before


@pytest.mark.parametrize(
    "case, mutate",
    [
        (
            "min_assignments",
            lambda data: data.update({"assignments": data["assignments"][:1]}),
        ),
        (
            "max_assignments",
            lambda data: data.update({
                "assignments": (
                    *data["assignments"],
                    *data["assignments"],
                    data["assignments"][0],
                )
            }),
        ),
        (
            "min_reviewed_proposals",
            lambda data: data.update({
                "reviewed_proposals": data["reviewed_proposals"][:1]
            }),
        ),
        (
            "max_reviewed_proposals",
            lambda data: data.update({
                "reviewed_proposals": (
                    *data["reviewed_proposals"],
                    *data["reviewed_proposals"],
                    data["reviewed_proposals"][0],
                )
            }),
        ),
    ],
)
def test_request_model_rejects_collection_bounds(
    case: str, mutate: Callable[[dict[str, object]], object]
) -> None:
    data = synthesis_request().model_dump(mode="json")
    mutate(data)
    assert case
    with pytest.raises(ValidationError):
        TicketSynthesisRequest.model_validate(data)


@pytest.mark.parametrize(
    "case, factory, error_type",
    [
        (
            "missing_assignment",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments[:-1],
                reviewed_proposals=request.reviewed_proposals,
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "duplicate_assignment_id",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=(
                    request.assignments[0],
                    request.assignments[0],
                    request.assignments[2],
                ),
                reviewed_proposals=request.reviewed_proposals,
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "duplicate_assignment_role",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=(
                    request.assignments[0],
                    request.assignments[1].model_copy(
                        update={"role": request.assignments[0].role}
                    ),
                    request.assignments[2],
                ),
                reviewed_proposals=request.reviewed_proposals,
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "assignment_digest_drift",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=(
                    request.assignments[0].model_copy(
                        update={"assignment_SHA256": "0" * 64}
                    ),
                    *request.assignments[1:],
                ),
                reviewed_proposals=request.reviewed_proposals,
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "missing_reviewed_proposal",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=request.reviewed_proposals[:-1],
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "duplicate_proposal_sha",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=(
                    request.reviewed_proposals[0],
                    request.reviewed_proposals[0],
                    request.reviewed_proposals[2],
                ),
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "proposal_assignment_drift",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=(
                    ReviewedTicketProposal.model_construct(
                        proposal=request.reviewed_proposals[0].proposal.model_copy(
                            update={
                                "assignment_id": request.reviewed_proposals[
                                    1
                                ].proposal.assignment_id
                            }
                        ),
                        lint_report=request.reviewed_proposals[0].lint_report,
                    ),
                    *request.reviewed_proposals[1:],
                ),
                dependency_plan=None,
            ),
            TicketSynthesisInputError,
        ),
        (
            "proposal_digest_drift",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=(
                    ReviewedTicketProposal.model_construct(
                        proposal=request.reviewed_proposals[0].proposal.model_copy(
                            update={"proposal_SHA256": "0" * 64}
                        ),
                        lint_report=request.reviewed_proposals[0].lint_report,
                    ),
                    *request.reviewed_proposals[1:],
                ),
                dependency_plan=None,
            ),
            TicketSynthesisValidationError,
        ),
        (
            "missing_context_pack_evidence",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=(
                    ReviewedTicketProposal.model_construct(
                        proposal=request.reviewed_proposals[0].proposal.model_copy(
                            update={"evidence_source_ids": ("CTX-MISSING-EVIDENCE",)}
                        ),
                        lint_report=request.reviewed_proposals[0].lint_report,
                    ),
                    *request.reviewed_proposals[1:],
                ),
                dependency_plan=None,
            ),
            TicketSynthesisValidationError,
        ),
        (
            "lint_report_digest_drift",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=(
                    ReviewedTicketProposal.model_construct(
                        proposal=request.reviewed_proposals[0].proposal,
                        lint_report=request.reviewed_proposals[
                            0
                        ].lint_report.model_copy(update={"report_SHA256": "0" * 64}),
                    ),
                    *request.reviewed_proposals[1:],
                ),
                dependency_plan=None,
            ),
            TicketSynthesisValidationError,
        ),
        (
            "dependency_plan_project_mismatch",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=request.reviewed_proposals,
                dependency_plan=build_ticket_dependency_plan(
                    TicketPlanningRequest(
                        project_spec=project(project_id="P17"),
                        tickets=(ticket("P17.1", project_id="P17"),),
                    )
                ),
            ),
            TicketSynthesisInputError,
        ),
        (
            "dependency_plan_missing_seed_ticket",
            lambda request: TicketSynthesisRequest.model_construct(
                generation_request=request.generation_request,
                assignments=request.assignments,
                reviewed_proposals=request.reviewed_proposals,
                dependency_plan=build_ticket_dependency_plan(
                    TicketPlanningRequest(
                        project_spec=project(),
                        tickets=(ticket("P16.6"),),
                    )
                ),
            ),
            TicketSynthesisInputError,
        ),
    ],
)
def test_builder_rejects_distinct_request_binding_errors(
    case: str,
    factory: Callable[[TicketSynthesisRequest], TicketSynthesisRequest],
    error_type: type[Exception],
) -> None:
    request = synthesis_request()
    assert case
    with pytest.raises(error_type):
        build_ticket_synthesis_review(factory(request))


@pytest.mark.parametrize(
    "case, mutate",
    [
        (
            "variant_duplicate_supporting_digests",
            lambda data: data.update({
                "supporting_proposal_SHA256s": (data["supporting_proposal_SHA256s"][0],)
                * 2
            }),
        ),
        (
            "variant_duplicate_supporting_roles",
            lambda data: data.update({
                "supporting_roles": (data["supporting_roles"][0],) * 2
            }),
        ),
        (
            "variant_support_count_mismatch",
            lambda data: data.update({"support_count": data["support_count"] + 1}),
        ),
        (
            "variant_role_order_mismatch",
            lambda data: data.update({
                "supporting_roles": tuple(reversed(data["supporting_roles"]))
            }),
        ),
    ],
)
def test_variant_evidence_rejects_distinct_invariant_drift(
    case: str, mutate: Callable[[dict[str, object]], object]
) -> None:
    variant = decision_by_field(
        build_ticket_synthesis_review(synthesis_request()), TicketSynthesisField.TITLE
    ).variants[0]
    data = variant.model_dump(mode="json")
    mutate(data)
    with pytest.raises(ValidationError):
        assert case
        ProposalVariantEvidence.model_validate(data)


@pytest.mark.parametrize(
    "case, mutate",
    [
        (
            "decision_duplicate_supporting_digests",
            lambda data: data.update({
                "supporting_proposal_SHA256s": (data["supporting_proposal_SHA256s"][0],)
                * 2
            }),
        ),
        (
            "decision_duplicate_dissenting_digests",
            lambda data: data.update({
                "dissenting_proposal_SHA256s": (data["dissenting_proposal_SHA256s"][0],)
                * 2
            }),
        ),
        (
            "unanimous_resolution_mismatch",
            lambda data: data.update({
                "resolution": FieldResolutionKind.PRESERVE_SEED.value
            }),
        ),
        (
            "unanimous_dissent_present",
            lambda data: data.update({"dissenting_proposal_SHA256s": ("f" * 64,)}),
        ),
        (
            "split_selected_digest_mismatch",
            lambda data: data.update({"selected_value_SHA256": "f" * 64}),
        ),
        (
            "strict_majority_missing_dissent",
            lambda data: data.update({"dissenting_proposal_SHA256s": ()}),
        ),
    ],
)
def test_field_decision_rejects_distinct_invariant_drift(
    case: str, mutate: Callable[[dict[str, object]], object]
) -> None:
    if case.startswith("split"):
        review = build_ticket_synthesis_review(
            synthesis_request(
                roles=(
                    TicketGeneratorRole.ARCHITECTURE,
                    TicketGeneratorRole.IMPLEMENTATION,
                ),
                proposed_tickets=(ticket(title="Split A"), ticket(title="Split B")),
            )
        )
    elif case.startswith("strict") or "dissenting" in case:
        review = build_ticket_synthesis_review(
            synthesis_request(
                proposed_tickets=(
                    ticket(title="Majority"),
                    ticket(title="Majority"),
                    ticket(title="Dissent"),
                )
            )
        )
    else:
        review = build_ticket_synthesis_review(synthesis_request())
    data = decision_by_field(review, TicketSynthesisField.TITLE).model_dump(mode="json")
    mutate(data)
    with pytest.raises(ValidationError):
        assert case
        FieldSynthesisDecision.model_validate(data)


@pytest.mark.parametrize(
    "case, mutate",
    [
        (
            "candidate_id_mismatch",
            lambda data: data.update({"candidate_id": "CAND-P16-6"}),
        ),
        ("project_id_mismatch", lambda data: data.update({"project_id": "P17"})),
        ("ticket_id_mismatch", lambda data: data.update({"ticket_id": "P16.6"})),
        (
            "source_excluded_overlap",
            lambda data: data.update({
                "excluded_proposal_SHA256s": (data["source_proposal_SHA256s"][0],)
            }),
        ),
        (
            "duplicate_source_proposals",
            lambda data: data.update({
                "source_proposal_SHA256s": (data["source_proposal_SHA256s"][0],) * 2
            }),
        ),
        (
            "duplicate_unresolved_conflicts",
            lambda data: data.update({
                "unresolved_conflict_ids": ("CONFLICT-0001",) * 2
            }),
        ),
        (
            "missing_field_decision",
            lambda data: data.update({"field_decisions": data["field_decisions"][:-1]}),
        ),
        (
            "candidate_lint_report_mismatch",
            lambda data: data.update({
                "candidate_lint_report": {
                    **data["candidate_lint_report"],
                    "ticket_ids": ("P16.6",),
                }
            }),
        ),
    ],
)
def test_candidate_contract_rejects_distinct_invariant_or_digest_drift(
    case: str, mutate: Callable[[dict[str, object]], object]
) -> None:
    review = build_ticket_synthesis_review(synthesis_request())
    assert review.candidate is not None
    data = review.candidate.model_dump(mode="json")
    mutate(data)
    with pytest.raises(ValidationError):
        assert case
        SynthesizedTicketCandidate.model_validate(data)


@pytest.mark.parametrize(
    "case, mutate",
    [
        (
            "eligible_excluded_not_partition",
            lambda data: data.update({
                "eligible_proposal_SHA256s": data["proposal_SHA256s"][:1]
            }),
        ),
        (
            "eligible_excluded_overlap",
            lambda data: data.update({
                "excluded_proposal_SHA256s": (data["eligible_proposal_SHA256s"][0],)
            }),
        ),
        (
            "duplicate_proposal_sha",
            lambda data: data.update({
                "proposal_SHA256s": (data["proposal_SHA256s"][0],) * 2
            }),
        ),
        (
            "conflict_order_mismatch",
            lambda data: data.update({"conflicts": tuple(reversed(data["conflicts"]))}),
        ),
        (
            "candidate_project_mismatch",
            lambda data: data.update({
                "candidate": {**data["candidate"], "project_id": "P17"}
            }),
        ),
        (
            "candidate_sources_mismatch",
            lambda data: data.update({
                "candidate": {
                    **data["candidate"],
                    "source_proposal_SHA256s": data["proposal_SHA256s"][:1],
                }
            }),
        ),
        (
            "candidate_conflict_ids_mismatch",
            lambda data: data.update({
                "candidate": {**data["candidate"], "unresolved_conflict_ids": ()}
            }),
        ),
        (
            "disposition_mismatch",
            lambda data: data.update({"disposition": "review_ready"}),
        ),
    ],
)
def test_review_contract_rejects_distinct_invariant_or_digest_drift(
    case: str, mutate: Callable[[dict[str, object]], object]
) -> None:
    majority = ticket_with_field(
        TicketSynthesisField.OBJECTIVE,
        "review-majority-objective",
        base=ticket(title="Majority"),
    )
    dissent = ticket_with_field(
        TicketSynthesisField.OBJECTIVE,
        "review-dissent-objective",
        base=ticket(title="Dissent"),
    )
    review = build_ticket_synthesis_review(
        synthesis_request(proposed_tickets=(majority, majority, dissent))
    )
    data = review.model_dump(mode="json")
    mutate(data)
    with pytest.raises(ValidationError):
        assert case
        TicketSynthesisReview.model_validate(data)


def test_review_tuple_partition_preserves_canonical_role_order_without_set_merge() -> (
    None
):
    request = synthesis_request(reverse_inputs=True)
    review = build_ticket_synthesis_review(request)
    assert review.candidate is not None
    assert review.eligible_proposal_SHA256s == review.proposal_SHA256s
    assert review.excluded_proposal_SHA256s == ()
    assert review.candidate.source_proposal_SHA256s == review.proposal_SHA256s
    assert tuple(item.proposal.role for item in request.reviewed_proposals) == tuple(
        reversed(CANONICAL_THREE_ROLE_ORDER)
    )
    canonical_review = build_ticket_synthesis_review(synthesis_request())
    assert review.proposal_SHA256s == canonical_review.proposal_SHA256s
