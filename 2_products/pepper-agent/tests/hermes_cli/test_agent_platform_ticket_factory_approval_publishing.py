import builtins
import hashlib
import importlib
import json
import socket
import sys
from collections.abc import Callable
from enum import Enum
from typing import get_args, get_origin

import pytest
from pydantic import ValidationError

import hermes_cli.agent_platform.ticket_factory.approval_publishing as approval_publishing_module
from hermes_cli.agent_platform import ticket_factory
from hermes_cli.agent_platform.ticket_factory import (
    CONTEXT_PACK_SCHEMA_VERSION,
    DEPENDENCY_PLAN_SCHEMA_VERSION,
    HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION,
    MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION,
    PROJECT_SPEC_SCHEMA_VERSION,
    TICKET_GENERATOR_ROLE_SCHEMA_VERSION,
    TICKET_POLICY_SCHEMA_VERSION,
    TICKET_SPEC_SCHEMA_VERSION,
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    CanonicalTicketSource,
    ConflictResolutionAction,
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPack,
    ContextPriority,
    ContextSensitivity,
    ContextSourceKind,
    ContextSourceSpec,
    DependencyKind,
    DependencyScope,
    FreshDependencyPlanningEvidence,
    GeneratorAssignment,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    HumanConflictResolution,
    ManualTicketReplacement,
    ParallelizationHint,
    ProjectSpec,
    PublishedTicketArtifact,
    RepositoryScopeSpec,
    ReviewedTicketProposal,
    TicketApprovalInputError,
    TicketApprovalPublishingError,
    TicketApprovalRecord,
    TicketApprovalRequest,
    TicketApprovalState,
    TicketApprovalValidationError,
    TicketDependencyPlan,
    TicketDependencySpec,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    TicketPlanningRequest,
    TicketPublicationAuthorizationError,
    TicketPublicationEvidence,
    TicketPublicationFormat,
    TicketPublicationRequest,
    TicketPublicationResult,
    TicketPublicationState,
    TicketResponseContractSpec,
    TicketSpec,
    TicketSupersessionRecord,
    TicketSynthesisDisposition,
    TicketSynthesisField,
    TicketSynthesisReview,
    TicketType,
    TicketValidationStepSpec,
    assemble_context_pack,
    build_ticket_approval_record,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    build_ticket_synthesis_review,
    lint_ticket_collection,
    prepare_ticket_generator_assignments,
    publish_canonical_ticket,
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
P16_6_EXPORTS = (
    "HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION",
    "HumanApprovalDecision",
    "ConflictResolutionAction",
    "TicketApprovalState",
    "CanonicalTicketSource",
    "TicketPublicationState",
    "TicketPublicationFormat",
    "HumanApprovalEvidence",
    "HumanConflictResolution",
    "ManualTicketReplacement",
    "FreshDependencyPlanningEvidence",
    "TicketApprovalRequest",
    "TicketApprovalRecord",
    "TicketPublicationEvidence",
    "TicketPublicationRequest",
    "PublishedTicketArtifact",
    "TicketSupersessionRecord",
    "TicketPublicationResult",
    "TicketApprovalPublishingError",
    "TicketApprovalInputError",
    "TicketApprovalValidationError",
    "TicketPublicationAuthorizationError",
    "build_ticket_approval_record",
    "publish_canonical_ticket",
)
PUBLIC_MODELS = (
    HumanApprovalEvidence,
    HumanConflictResolution,
    ManualTicketReplacement,
    FreshDependencyPlanningEvidence,
    TicketApprovalRequest,
    TicketApprovalRecord,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    PublishedTicketArtifact,
    TicketSupersessionRecord,
    TicketPublicationResult,
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
    allowed_paths: tuple[str, ...] = ("src/p16_6.py",),
    forbidden_actions: tuple[str, ...] = REQUIRED_FORBIDDEN_ACTION_MARKERS,
) -> RepositoryScopeSpec:
    return RepositoryScopeSpec(
        allowed_paths=allowed_paths,
        forbidden_paths=("4_external/sources/**",),
        allowed_actions=("edit human approval publication evidence",),
        forbidden_actions=forbidden_actions,
    )


def authority(**overrides: object) -> AuthorityReferenceSpec:
    data = {
        "kind": AuthorityReferenceKind.GOVERNANCE_RECORD,
        "value": "0_architecture/governance/synthetic_p16_6.md",
        "rationale": "Synthetic P16.6 authority reference.",
        "required": True,
    }
    data.update(overrides)
    return AuthorityReferenceSpec.model_validate(data)


def response_contract(**overrides: object) -> TicketResponseContractSpec:
    data = {
        "required_sections": REQUIRED_RESPONSE_SECTIONS,
        "completion_verdict": "synthetic_p16_6_ready",
    }
    data.update(overrides)
    return TicketResponseContractSpec.model_validate(data)


def validation_step(**overrides: object) -> TicketValidationStepSpec:
    data = {
        "validation_id": "V1",
        "description": "Run the synthetic P16.6 validation.",
        "command": "python -m pytest synthetic_approval_publishing_tests.py",
        "expected_result": "The synthetic P16.6 validation reports success.",
        "required": True,
    }
    data.update(overrides)
    return TicketValidationStepSpec.model_validate(data)


def dependency(
    ticket_id: str = "P16.1",
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
        "title": "Synthetic approval publishing project",
        "objective": "Validate human approval and canonical publication evidence.",
        "summary": "This synthetic project validates P16.6 only.",
        "context": ("Synthetic planning context for approval publishing.",),
        "authority_references": (authority(),),
        "scope": scope(allowed_paths=("src/**",)),
        "constraints": ("No execution authority is granted.",),
        "non_goals": ("No automated approval or file publication is authorized.",),
        "acceptance_criteria": (
            "Approval records and publication artifacts are deterministic.",
        ),
        "completion_verdict": "synthetic_project_approval_publishing_ready",
    }
    data.update(overrides)
    return ProjectSpec.model_validate(data)


def ticket(
    ticket_id: str = "P16.6",
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
        title=title or f"Synthetic approval ticket {ticket_id}",
        ticket_type=ticket_type,
        objective=objective or "Validate deterministic human approval evidence.",
        context=("Synthetic ticket context for approval publishing.",),
        authority_references=(authority(),),
        dependencies=deps,
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=ticket_scope
        or scope(allowed_paths=(f"src/{ticket_id.lower().replace('.', '_')}.py",)),
        constraints=("Rollback by restoring prior approval evidence.",),
        tasks=("Implement deterministic human approval publication evidence.",),
        acceptance_criteria=("The approval publication evidence is reversible.",),
        validation_steps=(validation_step(),),
        response_contract=response
        or response_contract(
            completion_verdict=f"synthetic_{ticket_id.lower().replace('.', '_')}_ready"
        ),
        recommended_commit_message="P16.6 Add approval publishing evidence",
    )


def source(**overrides: object) -> ContextSourceSpec:
    data = {
        "source_id": "CTX-APPROVAL-PUBLISHING-EVIDENCE",
        "kind": ContextSourceKind.GOVERNANCE_RECORD,
        "title": "Synthetic approval publishing evidence",
        "source_reference": "governance:synthetic-approval-publishing",
        "content": "Synthetic caller supplied content for approval review.",
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
        rationale=f"Synthetic {assignment.role.value} rationale for approval review.",
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
) -> tuple[ProjectSpec, TicketSpec, TicketSynthesisReview]:
    resolved_seed = seed or ticket()
    req = generation_request(ticket_spec=resolved_seed, roles=roles)
    assignments = prepare_ticket_generator_assignments(req)
    proposals = proposed_tickets or tuple(resolved_seed for _assignment in assignments)
    reviewed = tuple(
        reviewed_proposal(req, assignment, proposed_ticket)
        for assignment, proposed_ticket in zip(assignments, proposals, strict=True)
    )
    review = build_ticket_synthesis_review(
        ticket_factory.TicketSynthesisRequest(
            generation_request=req,
            assignments=assignments,
            reviewed_proposals=reviewed,
            dependency_plan=None,
        )
    )
    return (req.project_spec, resolved_seed, review)


def approval_evidence(
    *,
    reviewer_id: str = "reviewer.p16-6",
    decision_reference: str = "APPROVAL-P16-6-001",
    policy_ack: str | None = None,
    planning_ack: str | None = None,
) -> HumanApprovalEvidence:
    return HumanApprovalEvidence(
        reviewer_id=reviewer_id,
        decision_reference=decision_reference,
        rationale="Synthetic human approval rationale.",
        policy_warning_acknowledgement=policy_ack,
        planning_warning_acknowledgement=planning_ack,
    )


def publication_evidence(
    *,
    publisher_id: str = "publisher.p16-6",
    reference: str = "PUBLICATION-P16-6-001",
) -> TicketPublicationEvidence:
    return TicketPublicationEvidence(
        publisher_id=publisher_id,
        publication_reference=reference,
        rationale="Synthetic human publication rationale.",
    )


def conflict_resolution(
    conflict_id: str, action: ConflictResolutionAction
) -> HumanConflictResolution:
    return HumanConflictResolution(
        conflict_id=conflict_id,
        action=action,
        rationale=f"Synthetic human conflict resolution for {conflict_id}.",
        evidence_reference=f"EVIDENCE-{conflict_id}",
    )


def approval_request(
    *,
    project_spec: ProjectSpec | None = None,
    seed_ticket: TicketSpec | None = None,
    review: TicketSynthesisReview | None = None,
    decision: HumanApprovalDecision = HumanApprovalDecision.APPROVE,
    resolutions: tuple[HumanConflictResolution, ...] = (),
    evidence: HumanApprovalEvidence | None = None,
    manual_replacement: ManualTicketReplacement | None = None,
    fresh_planning_evidence: FreshDependencyPlanningEvidence | None = None,
) -> TicketApprovalRequest:
    if project_spec is None or seed_ticket is None or review is None:
        project_spec, seed_ticket, review = synthesis_request()
    return TicketApprovalRequest(
        project_spec=project_spec,
        seed_ticket=seed_ticket,
        synthesis_review=review,
        decision=decision,
        conflict_resolutions=resolutions,
        approval_evidence=evidence or approval_evidence(),
        manual_replacement=manual_replacement,
        fresh_planning_evidence=fresh_planning_evidence,
    )


def approved_record() -> TicketApprovalRecord:
    return build_ticket_approval_record(approval_request())


def planning_evidence_for(
    project_spec: ProjectSpec,
    selected_ticket: TicketSpec,
    *,
    tickets: tuple[TicketSpec, ...] | None = None,
) -> FreshDependencyPlanningEvidence:
    request = TicketPlanningRequest(
        project_spec=project_spec,
        tickets=tickets or (selected_ticket,),
    )
    return FreshDependencyPlanningEvidence(
        planning_request=request,
        dependency_plan=build_ticket_dependency_plan(request),
        evidence_reference="PLANNING-EVIDENCE-P16-6",
        rationale="Synthetic fresh planning rationale.",
    )


def assert_validation_fails(factory: Callable[[], object]) -> None:
    with pytest.raises(ValidationError):
        factory()


def blocking_review() -> tuple[ProjectSpec, TicketSpec, TicketSynthesisReview]:
    seed = ticket(ticket_scope=scope(allowed_paths=()))
    first = ticket(ticket_scope=scope(allowed_paths=("src/a.py",)))
    second = ticket(ticket_scope=scope(allowed_paths=("src/b.py",)))
    return synthesis_request(
        seed=seed,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(first, second),
    )


def human_review_required_review() -> tuple[
    ProjectSpec, TicketSpec, TicketSynthesisReview
]:
    seed = ticket(objective="Seed objective remains authoritative.")
    first = ticket(objective="Architecture objective variant.")
    second = ticket(objective="Implementation objective variant.")
    return synthesis_request(
        seed=seed,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(first, second),
    )


def test_p16_6_exports_import_correctly() -> None:
    assert HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION == 1
    assert HumanApprovalDecision.APPROVE.value == "approve"
    assert ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT.value == (
        "resolve_with_manual_replacement"
    )
    assert TicketApprovalState.APPROVED.value == "approved"
    assert CanonicalTicketSource.SYNTHESIZED_CANDIDATE.value == "synthesized_candidate"
    assert TicketPublicationState.PUBLISHED.value == "published"
    assert TicketPublicationFormat.CANONICAL_JSON_V1.value == "canonical_json_v1"
    assert build_ticket_approval_record.__name__ == "build_ticket_approval_record"
    assert publish_canonical_ticket.__name__ == "publish_canonical_ticket"


def test_public_export_group_preserves_prior_tail_order() -> None:
    exported = ticket_factory.__all__
    assert len(P16_6_EXPORTS) == 24
    assert len(exported) == len(frozenset(exported))
    positions = [exported.index(name) for name in P16_6_EXPORTS]
    assert positions == sorted(positions)
    assert exported[-len(P16_4_EXPORTS) :] == P16_4_EXPORTS
    assert "APPROVAL_RECORD_DIGEST_ALGORITHM" not in exported
    assert "PUBLICATION_RESULT_DIGEST_ALGORITHM" not in exported


def test_no_import_time_filesystem_or_network_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module_name = "hermes_cli.agent_platform.ticket_factory.approval_publishing"
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
    assert imported.HUMAN_APPROVAL_PUBLISHING_SCHEMA_VERSION == 1


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_are_frozen_and_extra_forbid(model: type) -> None:
    assert model.model_config["frozen"] is True
    assert model.model_config["extra"] == "forbid"
    assert model.model_config["validate_default"] is True
    assert model.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize(
    "model, data",
    [
        (HumanApprovalEvidence, lambda: approval_evidence().model_dump(mode="json")),
        (
            HumanConflictResolution,
            lambda: conflict_resolution(
                "CONFLICT-0001", ConflictResolutionAction.ACKNOWLEDGE
            ).model_dump(mode="json"),
        ),
        (
            ManualTicketReplacement,
            lambda: ManualTicketReplacement(
                replacement_ticket=ticket(),
                rationale="Synthetic replacement rationale.",
                evidence_references=("EVIDENCE-1",),
            ).model_dump(mode="json"),
        ),
        (
            FreshDependencyPlanningEvidence,
            lambda: planning_evidence_for(project(), ticket()).model_dump(mode="json"),
        ),
        (TicketApprovalRequest, lambda: approval_request().model_dump(mode="json")),
        (TicketApprovalRecord, lambda: approved_record().model_dump(mode="json")),
        (
            TicketPublicationEvidence,
            lambda: publication_evidence().model_dump(mode="json"),
        ),
        (
            TicketPublicationRequest,
            lambda: TicketPublicationRequest(
                approval_record=approved_record(),
                publication_evidence=publication_evidence(),
            ).model_dump(mode="json"),
        ),
        (
            PublishedTicketArtifact,
            lambda: publish_canonical_ticket(
                TicketPublicationRequest(
                    approval_record=approved_record(),
                    publication_evidence=publication_evidence(),
                )
            ).publication.model_dump(mode="json"),
        ),
        (
            TicketSupersessionRecord,
            lambda: publish_canonical_ticket(
                TicketPublicationRequest(
                    approval_record=approved_record(),
                    publication_evidence=publication_evidence(
                        reference="PUBLICATION-P16-6-002"
                    ),
                    prior_publication=publish_canonical_ticket(
                        TicketPublicationRequest(
                            approval_record=approved_record(),
                            publication_evidence=publication_evidence(),
                        )
                    ).publication,
                    supersession_rationale="Synthetic supersession rationale.",
                )
            ).supersession.model_dump(mode="json"),
        ),
        (
            TicketPublicationResult,
            lambda: publish_canonical_ticket(
                TicketPublicationRequest(
                    approval_record=approved_record(),
                    publication_evidence=publication_evidence(),
                )
            ).model_dump(mode="json"),
        ),
    ],
)
def test_public_models_reject_unknown_fields(
    model: type, data: Callable[[], dict[str, object]]
) -> None:
    payload = data()
    payload["unexpected"] = "value"
    assert_validation_fails(lambda: model.model_validate(payload))


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
    assert tuple(item.value for item in HumanApprovalDecision) == (
        "approve",
        "reject",
        "request_revision",
    )
    assert tuple(item.value for item in ConflictResolutionAction) == (
        "acknowledge",
        "accept_candidate",
        "resolve_with_manual_replacement",
        "reject",
    )
    assert tuple(item.value for item in TicketApprovalState) == (
        "approved",
        "rejected",
        "revision_required",
    )
    assert tuple(item.value for item in CanonicalTicketSource) == (
        "synthesized_candidate",
        "manual_replacement",
    )
    assert tuple(item.value for item in TicketPublicationState) == (
        "published",
        "superseded",
    )
    for enum_type in (
        HumanApprovalDecision,
        ConflictResolutionAction,
        TicketApprovalState,
        CanonicalTicketSource,
        TicketPublicationState,
        TicketPublicationFormat,
    ):
        assert issubclass(enum_type, Enum)
        assert len(enum_type.__members__) == len(tuple(enum_type))


def test_public_model_field_order() -> None:
    assert tuple(HumanApprovalEvidence.model_fields) == (
        "reviewer_id",
        "decision_reference",
        "rationale",
        "policy_warning_acknowledgement",
        "planning_warning_acknowledgement",
    )
    assert tuple(HumanConflictResolution.model_fields) == (
        "conflict_id",
        "action",
        "rationale",
        "evidence_reference",
    )
    assert tuple(ManualTicketReplacement.model_fields) == (
        "replacement_ticket",
        "rationale",
        "evidence_references",
    )
    assert tuple(FreshDependencyPlanningEvidence.model_fields) == (
        "planning_request",
        "dependency_plan",
        "evidence_reference",
        "rationale",
    )
    assert tuple(TicketApprovalRequest.model_fields) == (
        "project_spec",
        "seed_ticket",
        "synthesis_review",
        "decision",
        "conflict_resolutions",
        "approval_evidence",
        "manual_replacement",
        "fresh_planning_evidence",
    )
    assert tuple(TicketApprovalRecord.model_fields) == (
        "schema_version",
        "project_id",
        "ticket_id",
        "synthesis_review_SHA256",
        "decision",
        "state",
        "canonical_source",
        "approved_ticket",
        "approval_evidence",
        "conflict_resolutions",
        "approved_ticket_lint_report",
        "fresh_planning_evidence",
        "approval_input_SHA256",
        "approval_SHA256",
    )
    assert tuple(TicketPublicationResult.model_fields) == (
        "schema_version",
        "publication",
        "supersession",
        "publication_input_SHA256",
        "result_SHA256",
    )


def test_approve_unanimous_candidate_builds_nonexecuting_record() -> None:
    record = approved_record()
    assert record.schema_version == 1
    assert record.state is TicketApprovalState.APPROVED
    assert record.decision is HumanApprovalDecision.APPROVE
    assert record.canonical_source is CanonicalTicketSource.SYNTHESIZED_CANDIDATE
    assert record.approved_ticket == ticket()
    assert record.approved_ticket_lint_report is not None
    assert record.approved_ticket_lint_report.disposition is TicketLintDisposition.PASS
    assert record.conflict_resolutions == ()
    assert len(record.approval_input_SHA256) == 64
    assert len(record.approval_SHA256) == 64
    assert record.approval_input_SHA256 != record.approval_SHA256


def test_approval_digest_evidence_is_stable_sensitive_and_self_excluding() -> None:
    first = approved_record()
    second = approved_record()
    changed_project, changed_seed, changed_review = synthesis_request(
        seed=ticket(title="Changed approval title"),
    )
    changed = build_ticket_approval_record(
        approval_request(
            project_spec=changed_project,
            seed_ticket=changed_seed,
            review=changed_review,
        )
    )
    assert first.approval_input_SHA256 == second.approval_input_SHA256
    assert first.approval_SHA256 == second.approval_SHA256
    assert first.approval_SHA256 != changed.approval_SHA256
    tampered = first.model_dump(mode="json")
    tampered["approval_SHA256"] = "0" * 64
    assert_validation_fails(lambda: TicketApprovalRecord.model_validate(tampered))


def test_approval_sorts_conflict_resolutions_deterministically() -> None:
    seed = ticket(title="Seed title", objective="Seed objective remains.")
    first = ticket(title="First title", objective="First objective variant.")
    second = ticket(title="Second title", objective="Second objective variant.")
    project_spec, seed_ticket, review = synthesis_request(
        seed=seed,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(first, second),
    )
    assert len(review.conflicts) >= 2
    reversed_resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id, ConflictResolutionAction.ACCEPT_CANDIDATE
        )
        for conflict in reversed(review.conflicts)
    )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            resolutions=reversed_resolutions,
        )
    )
    assert tuple(
        resolution.conflict_id for resolution in record.conflict_resolutions
    ) == (tuple(conflict.conflict_id for conflict in review.conflicts))


def test_approval_requires_exactly_one_resolution_per_conflict() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
            )
        )


def test_human_review_conflict_cannot_be_acknowledged_for_approval() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(conflict.conflict_id, ConflictResolutionAction.ACKNOWLEDGE)
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
            )
        )


def test_reject_decision_records_nonapproval_without_ticket() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(conflict.conflict_id, ConflictResolutionAction.REJECT)
        for conflict in review.conflicts
    )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            decision=HumanApprovalDecision.REJECT,
            resolutions=resolutions,
        )
    )
    assert record.state is TicketApprovalState.REJECTED
    assert record.approved_ticket is None
    assert record.canonical_source is None
    assert record.approved_ticket_lint_report is None


def test_revision_decision_records_nonapproval_without_ticket() -> None:
    record = build_ticket_approval_record(
        approval_request(decision=HumanApprovalDecision.REQUEST_REVISION)
    )
    assert record.state is TicketApprovalState.REVISION_REQUIRED
    assert record.approved_ticket is None
    assert record.fresh_planning_evidence is None


def test_nonapproval_rejects_manual_replacement_and_planning() -> None:
    replacement = ManualTicketReplacement(
        replacement_ticket=ticket(),
        rationale="Synthetic replacement rationale.",
        evidence_references=("EVIDENCE-1",),
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                decision=HumanApprovalDecision.REJECT,
                manual_replacement=replacement,
            )
        )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                decision=HumanApprovalDecision.REQUEST_REVISION,
                fresh_planning_evidence=planning_evidence_for(project(), ticket()),
            )
        )


def test_blocking_conflict_requires_manual_replacement() -> None:
    project_spec, seed_ticket, review = blocking_review()
    assert review.disposition is TicketSynthesisDisposition.BLOCKED
    assert any(conflict.blocking for conflict in review.conflicts)
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id, ConflictResolutionAction.ACCEPT_CANDIDATE
        )
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
            )
        )


def test_blocking_conflict_can_be_approved_with_manual_replacement_and_plan() -> None:
    project_spec, seed_ticket, review = blocking_review()
    replacement_ticket = ticket(
        ticket_scope=scope(allowed_paths=("src/replacement.py",))
    )
    replacement = ManualTicketReplacement(
        replacement_ticket=replacement_ticket,
        rationale="Synthetic replacement rationale.",
        evidence_references=("EVIDENCE-1",),
    )
    planning = planning_evidence_for(project_spec, replacement_ticket)
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id,
            ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT,
        )
        for conflict in review.conflicts
    )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            resolutions=resolutions,
            manual_replacement=replacement,
            fresh_planning_evidence=planning,
        )
    )
    assert record.state is TicketApprovalState.APPROVED
    assert record.canonical_source is CanonicalTicketSource.MANUAL_REPLACEMENT
    assert record.approved_ticket == replacement_ticket
    assert record.fresh_planning_evidence == planning


def test_manual_replacement_identity_must_match_seed() -> None:
    replacement = ManualTicketReplacement(
        replacement_ticket=ticket("P16.7"),
        rationale="Synthetic replacement rationale.",
        evidence_references=("EVIDENCE-1",),
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(approval_request(manual_replacement=replacement))


def test_changed_candidate_requires_fresh_planning_evidence() -> None:
    changed = ticket(deps=(dependency("P16.1"),))
    project_spec, seed_ticket, review = synthesis_request(
        proposed_tickets=(changed, changed, changed),
    )
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
            )
        )


def test_planning_warning_requires_acknowledgement() -> None:
    changed = ticket(
        deps=(
            dependency(
                "P99.1",
                kind=DependencyKind.SOFT_PREDECESSOR,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        )
    )
    project_spec, seed_ticket, review = synthesis_request(
        proposed_tickets=(changed, changed, changed),
    )
    planning = planning_evidence_for(project_spec, changed)
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                fresh_planning_evidence=planning,
            )
        )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            evidence=approval_evidence(planning_ack="Human accepted planning warning."),
            fresh_planning_evidence=planning,
        )
    )
    assert record.state is TicketApprovalState.APPROVED


def test_fresh_planning_evidence_must_recompute() -> None:
    planning_request = TicketPlanningRequest(
        project_spec=project(), tickets=(ticket(),)
    )
    other_request = TicketPlanningRequest(
        project_spec=project(), tickets=(ticket("P16.7"),)
    )
    with pytest.raises(ValidationError):
        FreshDependencyPlanningEvidence(
            planning_request=planning_request,
            dependency_plan=build_ticket_dependency_plan(other_request),
            evidence_reference="PLANNING-EVIDENCE-P16-6",
            rationale="Synthetic stale planning evidence.",
        )


def test_duplicate_conflict_resolution_ids_are_rejected() -> None:
    duplicate = conflict_resolution(
        "CONFLICT-0001", ConflictResolutionAction.ACKNOWLEDGE
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                decision=HumanApprovalDecision.REJECT,
                resolutions=(duplicate, duplicate),
            )
        )


def test_manual_replacement_evidence_references_must_be_unique() -> None:
    with pytest.raises(ValidationError):
        ManualTicketReplacement(
            replacement_ticket=ticket(),
            rationale="Synthetic replacement rationale.",
            evidence_references=("EVIDENCE-1", "EVIDENCE-1"),
        )


def test_approval_rejects_reject_resolution() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(conflict.conflict_id, ConflictResolutionAction.REJECT)
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
            )
        )


def test_manual_replacement_action_requires_replacement() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id,
            ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT,
        )
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
            )
        )


def test_manual_replacement_cannot_accept_candidate_conflict() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    replacement = ManualTicketReplacement(
        replacement_ticket=seed_ticket,
        rationale="Synthetic replacement rationale.",
        evidence_references=("EVIDENCE-1",),
    )
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id, ConflictResolutionAction.ACCEPT_CANDIDATE
        )
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
                manual_replacement=replacement,
            )
        )


def test_publish_approved_record_builds_canonical_artifact() -> None:
    record = approved_record()
    result = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(),
        )
    )
    assert result.schema_version == 1
    assert result.publication.publication_id == "PUB-P16-6-0001"
    assert result.publication.revision == 1
    assert result.publication.state is TicketPublicationState.PUBLISHED
    assert result.publication.format is TicketPublicationFormat.CANONICAL_JSON_V1
    assert result.publication.canonical_ticket == record.approved_ticket
    assert result.publication.approval_SHA256 == record.approval_SHA256
    assert result.supersession is None
    assert len(result.publication.canonical_ticket_SHA256) == 64
    assert len(result.publication.artifact_SHA256) == 64
    assert len(result.result_SHA256) == 64


def test_publish_rejects_nonapproved_record() -> None:
    record = build_ticket_approval_record(
        approval_request(decision=HumanApprovalDecision.REQUEST_REVISION)
    )
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(
            TicketPublicationRequest(
                approval_record=record,
                publication_evidence=publication_evidence(),
            )
        )


def test_publication_supersedes_prior_publication() -> None:
    record = approved_record()
    first = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(),
        )
    )
    second = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-6-002"
            ),
            prior_publication=first.publication,
            supersession_rationale="Synthetic supersession rationale.",
        )
    )
    assert second.publication.publication_id == "PUB-P16-6-0002"
    assert second.publication.revision == 2
    assert (
        second.publication.supersedes_publication_id == first.publication.publication_id
    )
    assert second.supersession is not None
    assert (
        second.supersession.superseded_publication_id
        == first.publication.publication_id
    )
    assert (
        second.supersession.replacement_publication_id
        == second.publication.publication_id
    )


def test_publication_rejects_prior_without_rationale() -> None:
    record = approved_record()
    first = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(),
        )
    )
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(
            TicketPublicationRequest(
                approval_record=record,
                publication_evidence=publication_evidence(
                    reference="PUBLICATION-P16-6-002"
                ),
                prior_publication=first.publication,
            )
        )


def test_publication_rejects_prior_ticket_mismatch() -> None:
    record = approved_record()
    other_project, other_seed, other_review = synthesis_request(seed=ticket("P16.7"))
    other_record = build_ticket_approval_record(
        approval_request(
            project_spec=other_project,
            seed_ticket=other_seed,
            review=other_review,
        )
    )
    other_publication = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=other_record,
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-7-001"
            ),
        )
    ).publication
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(
            TicketPublicationRequest(
                approval_record=record,
                publication_evidence=publication_evidence(
                    reference="PUBLICATION-P16-6-002"
                ),
                prior_publication=other_publication,
                supersession_rationale="Synthetic mismatch supersession rationale.",
            )
        )


def test_published_artifact_rejects_tampered_digest() -> None:
    artifact = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approved_record(),
            publication_evidence=publication_evidence(),
        )
    ).publication
    tampered = artifact.model_dump(mode="json")
    tampered["artifact_SHA256"] = "0" * 64
    assert_validation_fails(lambda: PublishedTicketArtifact.model_validate(tampered))


def test_publication_result_rejects_tampered_digest() -> None:
    result = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approved_record(),
            publication_evidence=publication_evidence(),
        )
    )
    tampered = result.model_dump(mode="json")
    tampered["result_SHA256"] = "0" * 64
    assert_validation_fails(lambda: TicketPublicationResult.model_validate(tampered))


def test_publication_input_digest_captures_publication_evidence() -> None:
    record = approved_record()
    first = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-6-001"
            ),
        )
    )
    second = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-6-ALT"
            ),
        )
    )
    assert first.publication.artifact_SHA256 == second.publication.artifact_SHA256
    assert first.publication_input_SHA256 != second.publication_input_SHA256
    assert first.result_SHA256 != second.result_SHA256


def test_serialization_round_trip_and_tuple_immutability() -> None:
    request = approval_request()
    record = build_ticket_approval_record(request)
    publication = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(),
        )
    )
    assert (
        TicketApprovalRequest.model_validate_json(request.model_dump_json()) == request
    )
    assert TicketApprovalRecord.model_validate_json(record.model_dump_json()) == record
    assert (
        TicketPublicationResult.model_validate_json(publication.model_dump_json())
        == publication
    )
    with pytest.raises(AttributeError):
        record.conflict_resolutions.append(
            conflict_resolution("CONFLICT-0001", ConflictResolutionAction.ACKNOWLEDGE)
        )


def test_approval_and_publication_do_not_mutate_inputs() -> None:
    request = approval_request()
    request_before = request.model_dump(mode="json")
    record = build_ticket_approval_record(request)
    assert request.model_dump(mode="json") == request_before
    publication_request = TicketPublicationRequest(
        approval_record=record,
        publication_evidence=publication_evidence(),
    )
    publication_request_before = publication_request.model_dump(mode="json")
    publish_canonical_ticket(publication_request)
    assert publication_request.model_dump(mode="json") == publication_request_before


def test_no_execution_or_filesystem_authority_surface_exists() -> None:
    forbidden_names = (
        "ApprovalExecutor",
        "PublicationWriter",
        "CanonicalTicketWriter",
        "WorkPacket",
        "ExecutionLane",
        "AgentAssignment",
        "WorkerAssignment",
        "run_approved_ticket",
        "execute_approved_ticket",
        "write_canonical_ticket",
        "save_published_ticket",
        "load_approval_record",
        "graphify_update",
    )
    assert not any(hasattr(ticket_factory, name) for name in forbidden_names)
    result_json = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approved_record(),
            publication_evidence=publication_evidence(),
        )
    ).model_dump_json()
    forbidden_terms = (
        "workpacket",
        "worker_identity",
        "agent_identity",
        "workspace_path",
        "filesystem_path",
        "git_ref",
        "process_id",
    )
    assert not any(term in result_json.casefold() for term in forbidden_terms)


def test_identifier_and_text_validation_rejects_unsafe_values() -> None:
    with pytest.raises(ValidationError):
        approval_evidence(reviewer_id="bad reviewer")
    with pytest.raises(ValidationError):
        HumanApprovalEvidence(
            reviewer_id="ok.reviewer",
            decision_reference="APPROVAL\x00REFERENCE",
            rationale="Synthetic rationale.",
        )


def test_exception_hierarchy_and_required_imported_symbols_are_used() -> None:
    assert issubclass(TicketApprovalInputError, TicketApprovalPublishingError)
    assert issubclass(TicketApprovalValidationError, TicketApprovalPublishingError)
    assert issubclass(
        TicketPublicationAuthorizationError, TicketApprovalPublishingError
    )
    assert issubclass(TicketApprovalPublishingError, ValueError)
    assert PROJECT_SPEC_SCHEMA_VERSION == 1
    assert TICKET_SPEC_SCHEMA_VERSION == 1
    assert CONTEXT_PACK_SCHEMA_VERSION == 1
    assert TICKET_GENERATOR_ROLE_SCHEMA_VERSION == 1
    assert DEPENDENCY_PLAN_SCHEMA_VERSION == 1
    assert TICKET_POLICY_SCHEMA_VERSION == 1
    assert MULTI_GENERATOR_SYNTHESIS_SCHEMA_VERSION == 1
    assert get_args and get_origin and Callable
    assert ProjectSpec and TicketSpec and ContextPack and TicketDependencyPlan
    assert TicketLintReport and TicketSynthesisField


def warning_lint_report() -> TicketLintReport:
    first = ticket(title="Duplicate warning title")
    second = ticket(
        "P16.7",
        title="Duplicate warning title",
        response=response_contract(completion_verdict="synthetic_p16_7_warning_ready"),
    )
    planning_request = TicketPlanningRequest(
        project_spec=project(), tickets=(first, second)
    )
    return lint_ticket_collection(
        TicketLintRequest(
            project_spec=project(),
            tickets=(first, second),
            dependency_plan=build_ticket_dependency_plan(planning_request),
            collection_complete=False,
        )
    )


def approved_publication_result() -> TicketPublicationResult:
    return publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approved_record(),
            publication_evidence=publication_evidence(),
        )
    )


def superseding_publication_result() -> TicketPublicationResult:
    first = approved_publication_result()
    return publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approved_record(),
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-6-SECOND"
            ),
            prior_publication=first.publication,
            supersession_rationale="Synthetic supersession rationale.",
        )
    )


def strict_majority_warning_review() -> tuple[
    ProjectSpec, TicketSpec, TicketSynthesisReview
]:
    majority = ticket(title="Majority approval title")
    dissent = ticket(title="Dissent approval title")
    return synthesis_request(proposed_tickets=(majority, majority, dissent))


def no_candidate_review() -> tuple[ProjectSpec, TicketSpec, TicketSynthesisReview]:
    blocked = ticket(ticket_scope=scope(allowed_paths=()))
    return synthesis_request(
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION),
        proposed_tickets=(ticket(), blocked),
    )


def scope_review_planning_evidence(
    selected_ticket: TicketSpec,
) -> FreshDependencyPlanningEvidence:
    peer = ticket(
        "P16.7",
        title="Synthetic peer ticket for ambiguous scope review",
        ticket_scope=scope(allowed_paths=("src/p16_6.py",)),
        response=response_contract(completion_verdict="synthetic_p16_7_scope_ready"),
    )
    planning_request = TicketPlanningRequest(
        project_spec=project(), tickets=(selected_ticket, peer)
    )
    plan = build_ticket_dependency_plan(planning_request)
    assert any(
        wave.disposition.value == "scope_review_required"
        and selected_ticket.ticket_id in wave.ticket_ids
        for wave in plan.waves
    )
    return FreshDependencyPlanningEvidence(
        planning_request=planning_request,
        dependency_plan=plan,
        evidence_reference="PLANNING-SCOPE-REVIEW-P16-6",
        rationale="Synthetic scope review planning rationale.",
    )


@pytest.mark.parametrize(
    "factory, field",
    [
        (lambda: approved_record(), "schema_version"),
        (lambda: approved_publication_result().publication, "schema_version"),
        (lambda: approved_publication_result(), "schema_version"),
    ],
)
def test_schema_version_rejects_alternative_literals(
    factory: Callable[[], object], field: str
) -> None:
    payload = factory().model_dump(mode="json")
    payload[field] = 2
    model = type(factory())
    assert_validation_fails(lambda: model.model_validate(payload))


@pytest.mark.parametrize(
    "reviewer_id",
    [
        "ab",
        ".badreviewer",
        "bad reviewer",
        "bad/reviewer",
        "x" * 97,
    ],
)
def test_human_approval_evidence_rejects_invalid_reviewer_ids(
    reviewer_id: str,
) -> None:
    with pytest.raises(ValidationError):
        approval_evidence(reviewer_id=reviewer_id)


@pytest.mark.parametrize(
    "field, value",
    [
        ("decision_reference", ""),
        ("decision_reference", "APPROVAL\x00REFERENCE"),
        ("rationale", ""),
        ("rationale", "Rationale\x00with-nul"),
        ("policy_warning_acknowledgement", ""),
        ("planning_warning_acknowledgement", ""),
    ],
)
def test_human_approval_evidence_rejects_invalid_text_fields(
    field: str, value: str
) -> None:
    payload = approval_evidence().model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: HumanApprovalEvidence.model_validate(payload))


@pytest.mark.parametrize(
    "publisher_id",
    ["ab", " publisher", "bad publisher", "bad/publisher", "x" * 97],
)
def test_publication_evidence_rejects_invalid_publisher_ids(
    publisher_id: str,
) -> None:
    with pytest.raises(ValidationError):
        publication_evidence(publisher_id=publisher_id)


@pytest.mark.parametrize(
    "field, value",
    [
        ("publication_reference", ""),
        ("publication_reference", "PUBLICATION\x00REFERENCE"),
        ("rationale", ""),
        ("rationale", "Rationale\x00with-nul"),
    ],
)
def test_publication_evidence_rejects_invalid_text_fields(
    field: str, value: str
) -> None:
    payload = publication_evidence().model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: TicketPublicationEvidence.model_validate(payload))


@pytest.mark.parametrize(
    "conflict_id",
    ["CONFLICT-001", "CONFLICT-ABC1", "CONFLICT-00000000000", "BAD-0001"],
)
def test_conflict_resolution_rejects_invalid_conflict_id_shapes(
    conflict_id: str,
) -> None:
    with pytest.raises(ValidationError):
        conflict_resolution(conflict_id, ConflictResolutionAction.ACKNOWLEDGE)


@pytest.mark.parametrize(
    "field, value",
    [
        ("rationale", ""),
        ("rationale", "Rationale\x00with-nul"),
        ("evidence_reference", ""),
        ("evidence_reference", "Evidence\x00with-nul"),
    ],
)
def test_conflict_resolution_rejects_invalid_text_fields(
    field: str, value: str
) -> None:
    payload = conflict_resolution(
        "CONFLICT-0001", ConflictResolutionAction.ACKNOWLEDGE
    ).model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: HumanConflictResolution.model_validate(payload))


@pytest.mark.parametrize(
    "field, value",
    [
        ("approval_input_SHA256", "0" * 63),
        ("approval_input_SHA256", "G" * 64),
        ("approval_SHA256", "0" * 63),
        ("approval_SHA256", "G" * 64),
    ],
)
def test_approval_record_digest_fields_reject_invalid_shapes(
    field: str, value: str
) -> None:
    payload = approved_record().model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: TicketApprovalRecord.model_validate(payload))


@pytest.mark.parametrize(
    "field, value",
    [
        ("canonical_ticket_SHA256", "0" * 63),
        ("canonical_ticket_SHA256", "G" * 64),
        ("approval_SHA256", "0" * 63),
        ("artifact_SHA256", "G" * 64),
    ],
)
def test_published_artifact_digest_fields_reject_invalid_shapes(
    field: str, value: str
) -> None:
    payload = approved_publication_result().publication.model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: PublishedTicketArtifact.model_validate(payload))


@pytest.mark.parametrize(
    "field, value",
    [
        ("publication_input_SHA256", "0" * 63),
        ("publication_input_SHA256", "G" * 64),
        ("result_SHA256", "0" * 63),
        ("result_SHA256", "G" * 64),
    ],
)
def test_publication_result_digest_fields_reject_invalid_shapes(
    field: str, value: str
) -> None:
    payload = approved_publication_result().model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: TicketPublicationResult.model_validate(payload))


@pytest.mark.parametrize(
    "publication_id",
    ["PUB-P16.6-0001", "PUB-P16-6-1", "PUB-016-6-0001", "BAD-P16-6-0001"],
)
def test_published_artifact_rejects_invalid_publication_id_shapes(
    publication_id: str,
) -> None:
    payload = approved_publication_result().publication.model_dump(mode="json")
    payload["publication_id"] = publication_id
    assert_validation_fails(lambda: PublishedTicketArtifact.model_validate(payload))


@pytest.mark.parametrize(
    "mutate, error_type",
    [
        (
            lambda project_spec, seed_ticket, review: {
                "project_spec": project(project_id="P17")
            },
            TicketApprovalInputError,
        ),
        (
            lambda project_spec, seed_ticket, review: {
                "review": review.model_copy(update={"project_id": "P17"})
            },
            TicketApprovalInputError,
        ),
        (
            lambda project_spec, seed_ticket, review: {
                "review": review.model_copy(update={"ticket_id": "P16.7"})
            },
            TicketApprovalInputError,
        ),
        (
            lambda project_spec, seed_ticket, review: {
                "review": review.model_copy(update={"review_SHA256": "0" * 64})
            },
            TicketApprovalValidationError,
        ),
        (
            lambda project_spec, seed_ticket, review: {
                "review": review.model_copy(
                    update={
                        "candidate": review.candidate.model_copy(
                            update={"candidate_SHA256": "0" * 64}
                        )
                    }
                )
            },
            TicketApprovalValidationError,
        ),
    ],
)
def test_approval_request_rejects_identity_and_digest_drift(
    mutate: Callable[
        [ProjectSpec, TicketSpec, TicketSynthesisReview], dict[str, object]
    ],
    error_type: type[Exception],
) -> None:
    project_spec, seed_ticket, review = synthesis_request()
    assert review.candidate is not None
    overrides = mutate(project_spec, seed_ticket, review)
    request = TicketApprovalRequest.model_construct(
        project_spec=overrides.get("project_spec", project_spec),
        seed_ticket=seed_ticket,
        synthesis_review=overrides.get("review", review),
        decision=HumanApprovalDecision.APPROVE,
        conflict_resolutions=(),
        approval_evidence=approval_evidence(),
        manual_replacement=None,
        fresh_planning_evidence=None,
    )
    with pytest.raises(error_type):
        build_ticket_approval_record(request)


@pytest.mark.parametrize(
    "update",
    [
        {"schema_version": 2},
        {"project_id": "P17", "ticket_id": "P17.1"},
        {"ticket_id": "P16.7"},
        {"ticket_type": TicketType.TEST},
    ],
)
def test_manual_replacement_fixed_identity_invariants(
    update: dict[str, object],
) -> None:
    replacement_ticket = ticket().model_copy(update=update)
    replacement = ManualTicketReplacement(
        replacement_ticket=replacement_ticket,
        rationale="Synthetic replacement rationale.",
        evidence_references=("EVIDENCE-1",),
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(approval_request(manual_replacement=replacement))


def test_manual_replacement_rejects_incomplete_nested_ticket_spec() -> None:
    payload = {
        "replacement_ticket": {"project_id": "P16", "ticket_id": "P16.6"},
        "rationale": "Synthetic replacement rationale.",
        "evidence_references": ("EVIDENCE-1",),
    }
    assert_validation_fails(lambda: ManualTicketReplacement.model_validate(payload))


@pytest.mark.parametrize(
    "action",
    [
        ConflictResolutionAction.ACCEPT_CANDIDATE,
        ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT,
    ],
)
def test_nonapproval_rejects_approval_only_resolution_actions(
    action: ConflictResolutionAction,
) -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(conflict.conflict_id, action)
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                decision=HumanApprovalDecision.REJECT,
                resolutions=resolutions,
            )
        )


@pytest.mark.parametrize(
    "action",
    [ConflictResolutionAction.ACKNOWLEDGE, ConflictResolutionAction.REJECT],
)
def test_nonapproval_accepts_nonexecuting_resolution_actions(
    action: ConflictResolutionAction,
) -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(conflict.conflict_id, action)
        for conflict in review.conflicts
    )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            decision=HumanApprovalDecision.REQUEST_REVISION,
            resolutions=resolutions,
        )
    )
    assert record.state is TicketApprovalState.REVISION_REQUIRED
    assert record.conflict_resolutions == tuple(
        sorted(resolutions, key=lambda item: item.conflict_id)
    )


@pytest.mark.parametrize(
    "resolutions_factory",
    [
        lambda review: (),
        lambda review: (
            *(
                conflict_resolution(
                    conflict.conflict_id, ConflictResolutionAction.ACCEPT_CANDIDATE
                )
                for conflict in review.conflicts
            ),
            conflict_resolution(
                "CONFLICT-9999", ConflictResolutionAction.ACCEPT_CANDIDATE
            ),
        ),
    ],
)
def test_approval_requires_complete_and_exact_conflict_coverage(
    resolutions_factory: Callable[
        [TicketSynthesisReview], tuple[HumanConflictResolution, ...]
    ],
) -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions_factory(review),
            )
        )


def test_approval_rejects_resolution_for_unknown_conflict_when_review_has_none() -> (
    None
):
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                resolutions=(
                    conflict_resolution(
                        "CONFLICT-0001", ConflictResolutionAction.ACCEPT_CANDIDATE
                    ),
                )
            )
        )


@pytest.mark.parametrize(
    "action",
    [ConflictResolutionAction.ACKNOWLEDGE, ConflictResolutionAction.ACCEPT_CANDIDATE],
)
def test_warning_conflicts_allow_acknowledge_or_candidate_acceptance(
    action: ConflictResolutionAction,
) -> None:
    project_spec, seed_ticket, review = strict_majority_warning_review()
    assert review.disposition is TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT
    resolutions = tuple(
        conflict_resolution(conflict.conflict_id, action)
        for conflict in review.conflicts
    )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            resolutions=resolutions,
        )
    )
    assert record.state is TicketApprovalState.APPROVED


def test_human_review_required_conflict_accept_candidate_can_approve() -> None:
    project_spec, seed_ticket, review = human_review_required_review()
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id, ConflictResolutionAction.ACCEPT_CANDIDATE
        )
        for conflict in review.conflicts
    )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            resolutions=resolutions,
        )
    )
    assert record.state is TicketApprovalState.APPROVED
    assert record.canonical_source is CanonicalTicketSource.SYNTHESIZED_CANDIDATE


def test_approval_with_no_candidate_requires_manual_replacement() -> None:
    project_spec, seed_ticket, review = no_candidate_review()
    assert review.candidate is None
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id,
            ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT,
        )
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalInputError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
            )
        )


def test_fresh_lint_warning_requires_policy_acknowledgement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report = warning_lint_report()
    assert report.disposition is TicketLintDisposition.PASS_WITH_WARNINGS
    monkeypatch.setattr(
        approval_publishing_module,
        "lint_ticket_collection",
        lambda _request: report,
    )
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(approval_request())
    record = build_ticket_approval_record(
        approval_request(
            evidence=approval_evidence(policy_ack="Human accepted policy warning.")
        )
    )
    assert record.approved_ticket_lint_report == report


def test_fresh_lint_blocked_manual_replacement_blocks_approval() -> None:
    project_spec, seed_ticket, review = blocking_review()
    blocked_replacement_ticket = ticket(ticket_scope=scope(allowed_paths=()))
    replacement = ManualTicketReplacement(
        replacement_ticket=blocked_replacement_ticket,
        rationale="Synthetic blocked replacement rationale.",
        evidence_references=("EVIDENCE-1",),
    )
    planning = planning_evidence_for(project_spec, blocked_replacement_ticket)
    resolutions = tuple(
        conflict_resolution(
            conflict.conflict_id,
            ConflictResolutionAction.RESOLVE_WITH_MANUAL_REPLACEMENT,
        )
        for conflict in review.conflicts
    )
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                resolutions=resolutions,
                manual_replacement=replacement,
                fresh_planning_evidence=planning,
            )
        )


def test_scope_change_requires_fresh_planning_evidence() -> None:
    changed = ticket(ticket_scope=scope(allowed_paths=("src/changed_scope.py",)))
    project_spec, seed_ticket, review = synthesis_request(
        proposed_tickets=(changed, changed, changed),
    )
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
            )
        )


@pytest.mark.parametrize(
    "evidence_factory, error_type",
    [
        (
            lambda selected: planning_evidence_for(
                project(project_id="P17"),
                ticket("P17.1", project_id="P17"),
            ),
            TicketApprovalInputError,
        ),
        (
            lambda selected: planning_evidence_for(project(), ticket("P16.7")),
            TicketApprovalValidationError,
        ),
        (
            lambda selected: planning_evidence_for(
                project(), ticket(title="Planning content mismatch")
            ),
            TicketApprovalValidationError,
        ),
    ],
)
def test_fresh_planning_evidence_rejects_project_presence_and_content_mismatch(
    evidence_factory: Callable[[TicketSpec], FreshDependencyPlanningEvidence],
    error_type: type[Exception],
) -> None:
    changed = ticket(deps=(dependency("P16.1"),))
    project_spec, seed_ticket, review = synthesis_request(
        proposed_tickets=(changed, changed, changed),
    )
    with pytest.raises(error_type):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                fresh_planning_evidence=evidence_factory(changed),
            )
        )


def test_fresh_planning_evidence_rejects_blocked_selected_ticket() -> None:
    changed = ticket(
        deps=(
            dependency(
                "P99.2",
                kind=DependencyKind.HARD_PREREQUISITE,
                dep_scope=DependencyScope.EXTERNAL_PROJECT,
            ),
        )
    )
    project_spec, seed_ticket, review = synthesis_request(
        proposed_tickets=(changed, changed, changed),
    )
    planning = planning_evidence_for(project_spec, changed)
    assert changed.ticket_id in planning.dependency_plan.blocked_ticket_ids
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                fresh_planning_evidence=planning,
            )
        )


def test_dependency_plan_digest_tamper_is_rejected_by_fresh_planning_evidence() -> None:
    request = TicketPlanningRequest(project_spec=project(), tickets=(ticket(),))
    plan = build_ticket_dependency_plan(request).model_copy(
        update={"plan_SHA256": "0" * 64}
    )
    evidence = FreshDependencyPlanningEvidence.model_construct(
        planning_request=request,
        dependency_plan=plan,
        evidence_reference="PLANNING-TAMPER-P16-6",
        rationale="Synthetic tampered plan rationale.",
    )
    project_spec, seed_ticket, review = synthesis_request()
    approval = TicketApprovalRequest.model_construct(
        project_spec=project_spec,
        seed_ticket=seed_ticket,
        synthesis_review=review,
        decision=HumanApprovalDecision.APPROVE,
        conflict_resolutions=(),
        approval_evidence=approval_evidence(),
        manual_replacement=None,
        fresh_planning_evidence=evidence,
    )
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(approval)


def test_scope_review_wave_requires_planning_acknowledgement() -> None:
    changed = ticket(ticket_scope=scope(allowed_paths=("src/*.py",)))
    project_spec, seed_ticket, review = synthesis_request(
        proposed_tickets=(changed, changed, changed),
    )
    planning = scope_review_planning_evidence(changed)
    with pytest.raises(TicketApprovalValidationError):
        build_ticket_approval_record(
            approval_request(
                project_spec=project_spec,
                seed_ticket=seed_ticket,
                review=review,
                fresh_planning_evidence=planning,
            )
        )
    record = build_ticket_approval_record(
        approval_request(
            project_spec=project_spec,
            seed_ticket=seed_ticket,
            review=review,
            evidence=approval_evidence(planning_ack="Human accepted scope review."),
            fresh_planning_evidence=planning,
        )
    )
    assert record.fresh_planning_evidence == planning


@pytest.mark.parametrize(
    "update",
    [
        {"decision": HumanApprovalDecision.REJECT},
        {"approved_ticket": None},
        {"canonical_source": None},
        {"approved_ticket_lint_report": None},
    ],
)
def test_approved_record_state_invariants(update: dict[str, object]) -> None:
    payload = approved_record().model_dump(mode="json")
    payload.update(update)
    assert_validation_fails(lambda: TicketApprovalRecord.model_validate(payload))


@pytest.mark.parametrize(
    "update",
    [
        {"decision": HumanApprovalDecision.APPROVE.value},
        {"approved_ticket": ticket().model_dump(mode="json")},
        {"canonical_source": CanonicalTicketSource.SYNTHESIZED_CANDIDATE.value},
        {
            "approved_ticket_lint_report": approved_record().approved_ticket_lint_report.model_dump(
                mode="json"
            )
        },
        {
            "fresh_planning_evidence": planning_evidence_for(
                project(), ticket()
            ).model_dump(mode="json")
        },
    ],
)
def test_nonapproved_record_state_invariants(update: dict[str, object]) -> None:
    payload = build_ticket_approval_record(
        approval_request(decision=HumanApprovalDecision.REJECT)
    ).model_dump(mode="json")
    payload.update(update)
    assert_validation_fails(lambda: TicketApprovalRecord.model_validate(payload))


@pytest.mark.parametrize(
    "request_factory",
    [
        lambda: approval_request(
            evidence=approval_evidence(decision_reference="APPROVAL-P16-6-002")
        ),
        lambda: approval_request(
            evidence=approval_evidence(reviewer_id="reviewer.alt-p16-6")
        ),
        lambda: approval_request(decision=HumanApprovalDecision.REQUEST_REVISION),
        lambda: approval_request(
            manual_replacement=ManualTicketReplacement(
                replacement_ticket=ticket(title="Manual replacement digest title"),
                rationale="Synthetic replacement rationale.",
                evidence_references=("EVIDENCE-1",),
            )
        ),
    ],
)
def test_approval_input_digest_is_sensitive_to_distinct_inputs(
    request_factory: Callable[[], TicketApprovalRequest],
) -> None:
    base = approved_record()
    changed = build_ticket_approval_record(request_factory())
    assert base.approval_input_SHA256 != changed.approval_input_SHA256
    assert base.approval_SHA256 != changed.approval_SHA256


@pytest.mark.parametrize(
    "field, value",
    [
        ("decision", HumanApprovalDecision.REQUEST_REVISION.value),
        ("state", TicketApprovalState.REVISION_REQUIRED.value),
        ("canonical_source", CanonicalTicketSource.MANUAL_REPLACEMENT.value),
        ("synthesis_review_SHA256", "1" * 64),
    ],
)
def test_approval_record_digest_detects_field_tampering(
    field: str, value: object
) -> None:
    payload = approved_record().model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: TicketApprovalRecord.model_validate(payload))


def test_publication_rejects_tampered_approval_record_digest() -> None:
    record = approved_record().model_copy(update={"approval_SHA256": "0" * 64})
    request = TicketPublicationRequest.model_construct(
        approval_record=record,
        publication_evidence=publication_evidence(),
        prior_publication=None,
        supersession_rationale=None,
    )
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(request)


def test_publication_rejects_supersession_rationale_without_prior() -> None:
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(
            TicketPublicationRequest(
                approval_record=approved_record(),
                publication_evidence=publication_evidence(),
                supersession_rationale="Synthetic orphan supersession rationale.",
            )
        )


def test_publication_rejects_prior_project_mismatch() -> None:
    other_project = project(project_id="P17")
    other_seed = ticket("P17.1", project_id="P17")
    request = generation_request(project_spec=other_project, ticket_spec=other_seed)
    assignments = prepare_ticket_generator_assignments(request)
    reviewed = tuple(
        reviewed_proposal(request, assignment, other_seed) for assignment in assignments
    )
    other_review = build_ticket_synthesis_review(
        ticket_factory.TicketSynthesisRequest(
            generation_request=request,
            assignments=assignments,
            reviewed_proposals=reviewed,
            dependency_plan=None,
        )
    )
    other_record = build_ticket_approval_record(
        approval_request(
            project_spec=other_project,
            seed_ticket=other_seed,
            review=other_review,
        )
    )
    prior = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=other_record,
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P17-1-001"
            ),
        )
    ).publication
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(
            TicketPublicationRequest(
                approval_record=approved_record(),
                publication_evidence=publication_evidence(
                    reference="PUBLICATION-P16-6-002"
                ),
                prior_publication=prior,
                supersession_rationale="Synthetic project mismatch rationale.",
            )
        )


def test_publication_rejects_tampered_prior_publication_digest() -> None:
    first = approved_publication_result().publication
    prior = first.model_copy(update={"artifact_SHA256": "0" * 64})
    request = TicketPublicationRequest.model_construct(
        approval_record=approved_record(),
        publication_evidence=publication_evidence(reference="PUBLICATION-P16-6-002"),
        prior_publication=prior,
        supersession_rationale="Synthetic prior tamper rationale.",
    )
    with pytest.raises(TicketPublicationAuthorizationError):
        publish_canonical_ticket(request)


def test_canonical_json_is_deterministic_and_exact_round_trip() -> None:
    artifact = approved_publication_result().publication
    parsed = json.loads(artifact.canonical_ticket_JSON)
    assert parsed == artifact.canonical_ticket.model_dump(mode="json")
    assert artifact.canonical_ticket_JSON == json.dumps(
        parsed, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )
    assert TicketSpec.model_validate(parsed) == artifact.canonical_ticket


def test_canonical_ticket_digest_matches_canonical_json_bytes() -> None:
    artifact = approved_publication_result().publication
    assert (
        artifact.canonical_ticket_SHA256
        == hashlib.sha256(artifact.canonical_ticket_JSON.encode("utf-8")).hexdigest()
    )


@pytest.mark.parametrize(
    "field, value",
    [
        ("publication_id", "PUB-P16-6-0002"),
        ("canonical_ticket_JSON", "{}"),
        ("canonical_ticket_SHA256", "1" * 64),
        ("revision", 0),
        ("supersedes_publication_id", "PUB-P16-6-0002"),
    ],
)
def test_published_artifact_rejects_lineage_and_content_tampering(
    field: str, value: object
) -> None:
    payload = approved_publication_result().publication.model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: PublishedTicketArtifact.model_validate(payload))


@pytest.mark.parametrize(
    "nested_field, value",
    [("project_id", "P17"), ("ticket_id", "P16.7")],
)
def test_published_artifact_rejects_canonical_ticket_identity_mismatch(
    nested_field: str, value: object
) -> None:
    payload = approved_publication_result().publication.model_dump(mode="json")
    payload["canonical_ticket"][nested_field] = value
    assert_validation_fails(lambda: PublishedTicketArtifact.model_validate(payload))


@pytest.mark.parametrize(
    "field, value",
    [
        ("supersession_SHA256", "0" * 64),
        ("rationale", "Changed supersession rationale."),
        ("evidence_reference", "Changed supersession evidence."),
    ],
)
def test_supersession_record_rejects_digest_tampering(
    field: str, value: object
) -> None:
    supersession = superseding_publication_result().supersession
    assert supersession is not None
    payload = supersession.model_dump(mode="json")
    payload[field] = value
    assert_validation_fails(lambda: TicketSupersessionRecord.model_validate(payload))


def test_supersession_record_rejects_self_replacement() -> None:
    supersession = superseding_publication_result().supersession
    assert supersession is not None
    payload = supersession.model_dump(mode="json")
    payload["replacement_publication_id"] = payload["superseded_publication_id"]
    assert_validation_fails(lambda: TicketSupersessionRecord.model_validate(payload))


@pytest.mark.parametrize(
    "mutate",
    [
        lambda result: result.model_dump(mode="json")
        | {
            "supersession": superseding_publication_result().supersession.model_dump(
                mode="json"
            )
        },
        lambda result: result.model_dump(mode="json")
        | {
            "publication": superseding_publication_result().publication.model_dump(
                mode="json"
            ),
            "supersession": None,
        },
        lambda result: (
            lambda payload: (
                payload["publication"].update({
                    "supersedes_publication_id": "PUB-P16-6-9999"
                })
                or payload
            )
        )(superseding_publication_result().model_dump(mode="json")),
        lambda result: (
            lambda payload: (
                payload["supersession"].update({
                    "replacement_publication_id": "PUB-P16-6-9999"
                })
                or payload
            )
        )(superseding_publication_result().model_dump(mode="json")),
        lambda result: result.model_dump(mode="json") | {"result_SHA256": "0" * 64},
    ],
)
def test_publication_result_rejects_lineage_and_digest_tampering(
    mutate: Callable[[TicketPublicationResult], dict[str, object]],
) -> None:
    payload = mutate(approved_publication_result())
    assert_validation_fails(lambda: TicketPublicationResult.model_validate(payload))


@pytest.mark.parametrize(
    "request_factory",
    [
        lambda record: TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(reference="PUBLICATION-P16-6-A"),
        ),
        lambda record: TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(
                publisher_id="publisher.alt-p16-6"
            ),
        ),
        lambda record: TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(reference="PUBLICATION-P16-6-B"),
            prior_publication=approved_publication_result().publication,
            supersession_rationale="Synthetic sensitivity supersession rationale.",
        ),
    ],
)
def test_publication_input_digest_is_sensitive_to_request_evidence(
    request_factory: Callable[[TicketApprovalRecord], TicketPublicationRequest],
) -> None:
    record = approved_record()
    base = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=record,
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-6-BASE"
            ),
        )
    )
    changed = publish_canonical_ticket(request_factory(record))
    assert base.publication_input_SHA256 != changed.publication_input_SHA256
    assert base.result_SHA256 != changed.result_SHA256


def test_prior_publication_object_is_not_mutated_by_supersession() -> None:
    first = approved_publication_result().publication
    before = first.model_dump(mode="json")
    publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approved_record(),
            publication_evidence=publication_evidence(
                reference="PUBLICATION-P16-6-SUPERSEDE"
            ),
            prior_publication=first,
            supersession_rationale="Synthetic prior immutability rationale.",
        )
    )
    assert first.model_dump(mode="json") == before


@pytest.mark.parametrize(
    "model, factory",
    [
        (HumanApprovalEvidence, approval_evidence),
        (
            HumanConflictResolution,
            lambda: conflict_resolution(
                "CONFLICT-0001", ConflictResolutionAction.ACKNOWLEDGE
            ),
        ),
        (
            ManualTicketReplacement,
            lambda: ManualTicketReplacement(
                replacement_ticket=ticket(),
                rationale="Synthetic replacement rationale.",
                evidence_references=("EVIDENCE-1",),
            ),
        ),
        (
            FreshDependencyPlanningEvidence,
            lambda: planning_evidence_for(project(), ticket()),
        ),
        (TicketPublicationEvidence, publication_evidence),
    ],
)
def test_public_model_round_trips_for_leaf_evidence_models(
    model: type, factory: Callable[[], object]
) -> None:
    instance = factory()
    assert model.model_validate(instance.model_dump(mode="json")) == instance
    assert model.model_validate_json(instance.model_dump_json()) == instance


def test_published_artifact_json_round_trip_preserves_canonical_json() -> None:
    artifact = approved_publication_result().publication
    round_trip = PublishedTicketArtifact.model_validate_json(artifact.model_dump_json())
    assert round_trip == artifact
    assert round_trip.canonical_ticket_JSON == artifact.canonical_ticket_JSON


def test_publication_request_rejects_unknown_fields_before_publication() -> None:
    payload = TicketPublicationRequest(
        approval_record=approved_record(), publication_evidence=publication_evidence()
    ).model_dump(mode="json")
    payload["filesystem_path"] = "canonical/P16.6.json"
    assert_validation_fails(lambda: TicketPublicationRequest.model_validate(payload))


def test_publication_result_has_no_external_persistence_or_execution_fields() -> None:
    result = approved_publication_result()
    dumped = result.model_dump(mode="json")
    forbidden = {
        "path",
        "url",
        "repository",
        "branch",
        "commit",
        "command",
        "process",
        "worker",
        "agent",
        "workpacket",
        "environment",
        "token",
    }
    top_level_keys = set(dumped)
    publication_keys = set(dumped["publication"])
    supersession_keys = (
        set() if dumped["supersession"] is None else set(dumped["supersession"])
    )
    assert forbidden.isdisjoint(top_level_keys)
    assert forbidden.isdisjoint(publication_keys)
    assert forbidden.isdisjoint(supersession_keys)


def test_approval_record_has_no_automatic_approval_or_runtime_authority_fields() -> (
    None
):
    dumped = approved_record().model_dump(mode="json")
    flattened = json.dumps(dumped, sort_keys=True).casefold()
    forbidden = (
        "automatic_approval",
        "auto_approve",
        "runtime",
        "execute",
        "workpacket",
        "worker",
        "agent",
        "tool_call",
    )
    assert not any(term in flattened for term in forbidden)


def test_model_copy_tamper_does_not_mutate_original_approval_record() -> None:
    record = approved_record()
    before = record.model_dump(mode="json")
    record.model_copy(update={"approval_SHA256": "0" * 64})
    assert record.model_dump(mode="json") == before


def test_model_copy_tamper_does_not_mutate_original_publication_artifact() -> None:
    artifact = approved_publication_result().publication
    before = artifact.model_dump(mode="json")
    artifact.model_copy(update={"artifact_SHA256": "0" * 64})
    assert artifact.model_dump(mode="json") == before
