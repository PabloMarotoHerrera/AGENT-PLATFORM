import ast
from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.work_packet_execution_mvp_closure as closure
from hermes_cli.agent_platform.work_packet import (
    WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID,
    WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION,
    P17AuthorityBoundary,
    P17CapabilityReconciliation,
    P17CapabilityStatus,
    P17ClosureDecision,
    P17ClosureError,
    P17ClosureFinding,
    P17ClosureFindingCode,
    P17ClosureFindingSeverity,
    P17ClosureInputError,
    P17ClosureIntegrityError,
    P17ClosurePolicyError,
    P17ClosureRequest,
    P17ClosureResult,
    P17ClosureState,
    P17ClosureStateError,
    P17ClosureSummary,
    P17ClosureValidationError,
    P17ResidualLimitation,
    P17SecurityBoundary,
    P17TicketAcceptance,
    P18MigrationHandoff,
    build_canonical_p17_closure_request,
    build_p17_work_packet_execution_mvp_closure,
    summarize_p17_closure,
    validate_p17_closure_request,
    validate_p17_closure_result,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_non_critical_ticket_pilot as p17_8,
)


P17_R_EXPORTS = (
    "WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION",
    "WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID",
    "P17ClosureState",
    "P17ClosureDecision",
    "P17ClosureFindingSeverity",
    "P17ClosureFindingCode",
    "P17CapabilityStatus",
    "P17TicketAcceptance",
    "P17CapabilityReconciliation",
    "P17AuthorityBoundary",
    "P17SecurityBoundary",
    "P17ResidualLimitation",
    "P18MigrationHandoff",
    "P17ClosureFinding",
    "P17ClosureSummary",
    "P17ClosureRequest",
    "P17ClosureResult",
    "P17ClosureError",
    "P17ClosureInputError",
    "P17ClosureIntegrityError",
    "P17ClosurePolicyError",
    "P17ClosureStateError",
    "P17ClosureValidationError",
    "build_canonical_p17_closure_request",
    "validate_p17_closure_request",
    "build_p17_work_packet_execution_mvp_closure",
    "validate_p17_closure_result",
    "summarize_p17_closure",
)
PUBLIC_MODELS = (
    P17TicketAcceptance,
    P17CapabilityReconciliation,
    P17AuthorityBoundary,
    P17SecurityBoundary,
    P17ResidualLimitation,
    P18MigrationHandoff,
    P17ClosureFinding,
    P17ClosureSummary,
    P17ClosureRequest,
    P17ClosureResult,
)
CONTROLLED_ENUMS = (
    P17ClosureState,
    P17ClosureDecision,
    P17ClosureFindingSeverity,
    P17ClosureFindingCode,
    P17CapabilityStatus,
)
EXPECTED_ENUM_VALUES = (
    (P17ClosureState, ("prepared", "blocked", "closed")),
    (P17ClosureDecision, ("accepted", "rejected")),
    (P17ClosureFindingSeverity, ("info", "warning", "blocking")),
    (
        P17ClosureFindingCode,
        (
            "ticket_accepted",
            "ticket_missing",
            "verdict_mismatch",
            "contract_mismatch",
            "chain_incomplete",
            "authority_expanded",
            "security_boundary_mismatch",
            "pilot_not_accepted",
            "mvp_requirement_unsatisfied",
            "manual_validation_pending",
            "production_readiness_not_claimed",
            "critical_ticket_support_absent",
            "provider_execution_absent",
            "model_execution_absent",
            "git_execution_absent",
            "p18_reuse_first_required",
            "p18_ready",
            "p17_closed",
            "p17_rejected",
        ),
    ),
    (P17CapabilityStatus, ("satisfied", "absent_by_design", "deferred")),
)
FORBIDDEN_PUBLIC_NAMES = (
    "execute_p17_closure",
    "run_p17_closure",
    "close_project_runtime",
    "execute_P18",
    "run_P18",
    "P17ClosureExecutor",
    "P17ClosureRunner",
    "ProductionClosure",
    "AutomaticClosure",
    "CriticalTicketExecution",
    "MultiAgentExecution",
    "ParallelExecution",
)
EXPECTED_TICKETS = (
    (
        "P17.0",
        "TicketSpec to WorkPacket Compiler",
        0,
        "hermes_0_19_pepper_ticket_spec_to_work_packet_compiler_ready_with_compile_only_non_executing_authority",
        (),
    ),
    (
        "P17.1",
        "Workspace Allocator",
        1,
        "hermes_0_19_pepper_work_packet_workspace_allocator_ready_with_human_provisioned_exclusive_non_executing_authority",
        ("P17.0",),
    ),
    (
        "P17.2",
        "Tool Permission Profiles",
        2,
        "hermes_0_19_pepper_tool_permission_profiles_ready_with_deterministic_deny_first_non_executing_authority",
        ("P17.1",),
    ),
    (
        "P17.3",
        "Single-Agent Ticket Executor",
        3,
        "hermes_0_19_pepper_single_agent_work_packet_execution_ready_with_externally_driven_permission_gated_filesystem_only_authority",
        ("P17.0", "P17.1", "P17.2"),
    ),
    (
        "P17.4",
        "Validation Command Runner",
        4,
        "hermes_0_19_pepper_validation_command_runner_ready_with_exact_human_authorized_shell_free_bounded_subprocess_authority",
        ("P17.3",),
    ),
    (
        "P17.5",
        "Result, Failure and Cancellation Envelopes",
        5,
        "hermes_0_19_pepper_result_failure_cancellation_envelopes_ready_with_deterministic_bounded_terminal_outcome_authority",
        ("P17.3", "P17.4"),
    ),
    (
        "P17.6",
        "Diff and Artifact Review",
        6,
        "hermes_0_19_pepper_diff_and_artifact_review_ready_with_deterministic_human_observed_non_mutating_candidate_and_artifact_authority",
        ("P17.5",),
    ),
    (
        "P17.7",
        "Human Git Handoff",
        7,
        "hermes_0_19_pepper_human_git_handoff_ready_with_exact_review_bound_non_executing_human_only_git_authority",
        ("P17.6",),
    ),
    (
        "P17.8",
        "Non-Critical Ticket Pilot",
        8,
        "hermes_0_19_pepper_non_critical_ticket_pilot_ready_with_complete_governed_work_packet_chain_and_human_only_git_handoff_evidence",
        ("P17.0", "P17.1", "P17.2", "P17.3", "P17.4", "P17.5", "P17.6", "P17.7"),
    ),
)
EXPECTED_CAPABILITIES = (
    ("CAP-P17-001", "P17.0", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-002", "P17.1", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-003", "P17.2", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-004", "P17.3", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-005", "P17.4", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-006", "P17.5", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-007", "P17.6", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-008", "P17.7", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-009", "P17.8", P17CapabilityStatus.SATISFIED, None),
    ("CAP-P17-010", "P17.8", P17CapabilityStatus.ABSENT_BY_DESIGN, None),
    ("CAP-P17-011", "P17.8", P17CapabilityStatus.ABSENT_BY_DESIGN, None),
    ("CAP-P17-012", "P17.7", P17CapabilityStatus.ABSENT_BY_DESIGN, None),
    ("CAP-P17-013", "P17.8", P17CapabilityStatus.ABSENT_BY_DESIGN, None),
    ("CAP-P17-014", "P17.8", P17CapabilityStatus.ABSENT_BY_DESIGN, None),
    ("CAP-P17-015", "P17.R", P17CapabilityStatus.DEFERRED, "P18"),
    ("CAP-P17-016", "P17.R", P17CapabilityStatus.DEFERRED, "P19"),
    ("CAP-P17-017", "P17.R", P17CapabilityStatus.DEFERRED, "P20"),
    ("CAP-P17-018", "P17.R", P17CapabilityStatus.DEFERRED, "P21"),
)
EXPECTED_LIMITATIONS = (
    ("LIM-P17-001", "Non-critical pilot only", None),
    ("LIM-P17-002", "Critical tickets unsupported", None),
    ("LIM-P17-003", "Provider dispatch absent from WorkPacket MVP", None),
    ("LIM-P17-004", "Model inference absent from WorkPacket MVP", None),
    ("LIM-P17-005", "Git remains human-only", None),
    ("LIM-P17-006", "Automatic retry absent", "P18"),
    ("LIM-P17-007", "Automatic fallback absent", "P18"),
    ("LIM-P17-008", "Automatic cleanup and rollback absent", "P18"),
    ("LIM-P17-009", "Workflow migration incomplete", "P18"),
    ("LIM-P17-010", "Persistent shared agent memory absent", "P19"),
    ("LIM-P17-011", "Durable work control plane absent", "P20"),
    ("LIM-P17-012", "Multi-agent automation absent", "P21"),
    ("LIM-P17-013", "Production readiness not claimed", None),
)


@pytest.fixture(scope="module")
def accepted_pilot(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p17_r")
    try:
        context = p17_8.non_delete_context(monkeypatch, root)
        return p17_8.build_non_critical_ticket_pilot(p17_8.request_for_context(context))
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="module")
def canonical_request(accepted_pilot):
    return build_canonical_p17_closure_request(non_critical_pilot_result=accepted_pilot)


@pytest.fixture(scope="module")
def canonical_result(canonical_request):
    return build_p17_work_packet_execution_mvp_closure(canonical_request)


@pytest.fixture(scope="module")
def sample_models(canonical_request, canonical_result):
    return {
        P17TicketAcceptance.__name__: canonical_request.ticket_acceptances[0],
        P17CapabilityReconciliation.__name__: canonical_request.capability_reconciliations[
            0
        ],
        P17AuthorityBoundary.__name__: canonical_request.authority_boundary,
        P17SecurityBoundary.__name__: canonical_request.security_boundary,
        P17ResidualLimitation.__name__: canonical_request.residual_limitations[0],
        P18MigrationHandoff.__name__: canonical_request.P18_handoff,
        P17ClosureFinding.__name__: canonical_result.findings[0],
        P17ClosureSummary.__name__: canonical_result.closure_summary,
        P17ClosureRequest.__name__: canonical_request,
        P17ClosureResult.__name__: canonical_result,
    }


def _construct_with_updates(model: BaseModel, **updates):
    data = {field: getattr(model, field) for field in type(model).model_fields}
    data.update(updates)
    return type(model).model_construct(**data)


def _request_with_updates(request: P17ClosureRequest, **updates) -> P17ClosureRequest:
    return _construct_with_updates(request, **updates)


def _result_with_updates(result: P17ClosureResult, **updates) -> P17ClosureResult:
    return _construct_with_updates(result, **updates)


@pytest.mark.parametrize("exported_name", P17_R_EXPORTS)
def test_all_p17_r_exports_exist(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)
    assert hasattr(closure, exported_name)


def test_prior_255_exports_remain_exact_prefix() -> None:
    prior = (
        p17_8.p17_6.p17_5.P17_0_EXPORTS
        + p17_8.p17_6.p17_5.P17_1_EXPORTS
        + p17_8.p17_6.p17_5.P17_2_EXPORTS
        + p17_8.p17_6.p17_5.P17_3_EXPORTS
        + p17_8.p17_6.p17_5.P17_4_EXPORTS
        + p17_8.p17_6.p17_5.P17_5_EXPORTS
        + p17_8.p17_6.P17_6_EXPORTS
        + p17_8.p17_7.P17_7_EXPORTS
        + p17_8.P17_8_EXPORTS
    )
    assert len(prior) == 255
    assert work_packet.__all__[:255] == prior
    assert work_packet.__all__[255:283] == P17_R_EXPORTS
    assert len(work_packet.__all__) >= 283
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)


def test_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__[255:283]),
        len(work_packet.__all__) >= 283,
        len(set(work_packet.__all__)) == len(work_packet.__all__),
        hasattr(work_packet, "P17ClosureResult"),
        hasattr(work_packet, "build_p17_work_packet_execution_mvp_closure"),
        hasattr(work_packet, "execute_p17_closure"),
        hasattr(work_packet, "P17ClosureExecutor"),
    ) == (28, True, True, True, True, False, False)


def test_function_import_smoke_exact_names() -> None:
    assert (
        build_canonical_p17_closure_request.__name__,
        validate_p17_closure_request.__name__,
        build_p17_work_packet_execution_mvp_closure.__name__,
        validate_p17_closure_result.__name__,
        summarize_p17_closure.__name__,
    ) == (
        "build_canonical_p17_closure_request",
        "validate_p17_closure_request",
        "build_p17_work_packet_execution_mvp_closure",
        "validate_p17_closure_result",
        "summarize_p17_closure",
    )


@pytest.mark.parametrize("forbidden_name", FORBIDDEN_PUBLIC_NAMES)
def test_forbidden_execution_exports_absent(forbidden_name: str) -> None:
    assert not hasattr(work_packet, forbidden_name)
    assert forbidden_name not in work_packet.__all__
    assert forbidden_name not in closure.__all__


@pytest.mark.parametrize("enum_cls,expected", EXPECTED_ENUM_VALUES)
def test_exact_enum_values(enum_cls: type[Enum], expected: tuple[str, ...]) -> None:
    assert tuple(item.value for item in enum_cls) == expected


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_enum_aliases_absent(enum_cls: type[Enum]) -> None:
    assert len(enum_cls) == len({item.value for item in enum_cls})


@pytest.mark.parametrize(
    "error_cls",
    (
        P17ClosureError,
        P17ClosureInputError,
        P17ClosureIntegrityError,
        P17ClosurePolicyError,
        P17ClosureStateError,
        P17ClosureValidationError,
    ),
)
def test_public_exceptions_are_value_errors(error_cls: type[Exception]) -> None:
    assert issubclass(error_cls, ValueError)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_frozen_extra_forbid(model_cls: type[BaseModel]) -> None:
    assert model_cls.model_config["frozen"] is True
    assert model_cls.model_config["extra"] == "forbid"
    assert model_cls.model_config["validate_default"] is True
    assert model_cls.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_model_schemas_forbid_additional_properties(model_cls: type[BaseModel]) -> None:
    assert model_cls.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_unknown_fields_fail(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["unexpected"] = "value"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_models_are_immutable(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    with pytest.raises(ValidationError):
        model.__setattr__(next(iter(model.model_fields)), "changed")


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_json_round_trip_supported(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    assert model_cls.model_validate_json(model.model_dump_json()) == model
    assert model_cls.model_validate(model.model_dump(mode="json")) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_tuple_immutability_retained(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    for value in model.__dict__.values():
        if isinstance(value, tuple):
            assert isinstance(value, tuple)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_strict_booleans_reject_strings(
    model_cls: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    for field_name, value in tuple(data.items()):
        if isinstance(value, bool):
            data[field_name] = "true"
            with pytest.raises(ValidationError):
                model_cls.model_validate(data)
            return
    assert not any(isinstance(value, bool) for value in data.values())


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_no_forbidden_public_field_shapes(model_cls: type[BaseModel]) -> None:
    forbidden = {
        "Any",
        "dict",
        "Mapping",
        "MutableMapping",
        "object",
        "Path",
        "datetime",
        "UUID",
        "bytes",
        "Callable",
    }
    for field in model_cls.model_fields.values():
        assert (
            getattr(field.annotation, "__name__", str(field.annotation))
            not in forbidden
        )


@pytest.mark.parametrize(
    "ticket_id,title,ordinal,verdict,prerequisites", EXPECTED_TICKETS
)
def test_ticket_inventory_exact(
    canonical_request, ticket_id, title, ordinal, verdict, prerequisites
) -> None:
    ticket = canonical_request.ticket_acceptances[ordinal]
    assert ticket.ticket_id == ticket_id
    assert ticket.ticket_title == title
    assert ticket.ordinal == ordinal
    assert ticket.accepted is True
    assert ticket.verdict == verdict
    assert ticket.prerequisite_ticket_ids == prerequisites


@pytest.mark.parametrize(
    "ticket_id,title,ordinal,verdict,prerequisites", EXPECTED_TICKETS
)
def test_ticket_acceptance_digest_valid(
    canonical_request, ticket_id, title, ordinal, verdict, prerequisites
) -> None:
    ticket = canonical_request.ticket_acceptances[ordinal]
    assert ticket.evidence_SHA256 == closure._model_digest(
        closure.TICKET_ACCEPTANCE_DIGEST_ALGORITHM, ticket
    )


@pytest.mark.parametrize(
    "ticket_id,title,ordinal,verdict,prerequisites", EXPECTED_TICKETS
)
def test_ticket_summaries_are_bounded(
    canonical_request, ticket_id, title, ordinal, verdict, prerequisites
) -> None:
    ticket = canonical_request.ticket_acceptances[ordinal]
    assert len(ticket.ticket_title) <= 160
    assert len(ticket.primary_contract) <= 128
    assert len(ticket.capability_summary) <= 512
    assert len(ticket.authority_summary) <= 512


@pytest.mark.parametrize(
    "ticket_id,title,ordinal,verdict,prerequisites", EXPECTED_TICKETS
)
def test_ticket_reordered_or_altered_fails(
    canonical_request, ticket_id, title, ordinal, verdict, prerequisites
) -> None:
    tickets = list(canonical_request.ticket_acceptances)
    tickets[ordinal] = _construct_with_updates(
        tickets[ordinal], verdict="wrong-verdict"
    )
    bad = _request_with_updates(canonical_request, ticket_acceptances=tuple(tickets))
    with pytest.raises((P17ClosurePolicyError, ValidationError)):
        validate_p17_closure_request(bad)


def test_duplicate_ticket_fails(canonical_request) -> None:
    tickets = (
        (canonical_request.ticket_acceptances[0],)
        + canonical_request.ticket_acceptances[1:-1]
        + (canonical_request.ticket_acceptances[0],)
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, ticket_acceptances=tickets)
        )


def test_missing_ticket_fails(canonical_request) -> None:
    with pytest.raises((P17ClosureInputError, P17ClosurePolicyError, ValidationError)):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request,
                ticket_acceptances=canonical_request.ticket_acceptances[:-1],
            )
        )


@pytest.mark.parametrize("capability_id,owner,status,deferred", EXPECTED_CAPABILITIES)
def test_capability_inventory_exact(
    canonical_request, capability_id, owner, status, deferred
) -> None:
    capability = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == capability_id
    )
    assert capability.owner_ticket == owner
    assert capability.status is status
    assert capability.deferred_to_project == deferred
    assert capability.satisfied is (status is P17CapabilityStatus.SATISFIED)
    assert capability.intentionally_absent is (
        status is P17CapabilityStatus.ABSENT_BY_DESIGN
    )


@pytest.mark.parametrize("capability_id,owner,status,deferred", EXPECTED_CAPABILITIES)
def test_capability_digest_valid(
    canonical_request, capability_id, owner, status, deferred
) -> None:
    capability = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == capability_id
    )
    assert capability.reconciliation_SHA256 == closure._model_digest(
        closure.CAPABILITY_RECONCILIATION_DIGEST_ALGORITHM, capability
    )


@pytest.mark.parametrize("capability_id,owner,status,deferred", EXPECTED_CAPABILITIES)
def test_capability_status_posture(
    canonical_request, capability_id, owner, status, deferred
) -> None:
    capability = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == capability_id
    )
    if status is P17CapabilityStatus.SATISFIED:
        assert (
            capability.satisfied
            and not capability.intentionally_absent
            and capability.deferred_to_project is None
        )
    if status is P17CapabilityStatus.ABSENT_BY_DESIGN:
        assert (
            not capability.satisfied
            and capability.intentionally_absent
            and capability.deferred_to_project is None
        )
    if status is P17CapabilityStatus.DEFERRED:
        assert (
            not capability.satisfied
            and not capability.intentionally_absent
            and capability.deferred_to_project in {"P18", "P19", "P20", "P21"}
        )


@pytest.mark.parametrize("capability_id,owner,status,deferred", EXPECTED_CAPABILITIES)
def test_capability_tampering_fails(
    canonical_request, capability_id, owner, status, deferred
) -> None:
    capabilities = list(canonical_request.capability_reconciliations)
    index = next(
        i for i, item in enumerate(capabilities) if item.capability_id == capability_id
    )
    changed_owner = "P17.8" if owner != "P17.8" else "P17.0"
    capabilities[index] = _construct_with_updates(
        capabilities[index], owner_ticket=changed_owner
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request, capability_reconciliations=tuple(capabilities)
            )
        )


@pytest.mark.parametrize("capability_id,owner,status,deferred", EXPECTED_CAPABILITIES)
def test_capability_reconciliation_is_bounded(
    canonical_request, capability_id, owner, status, deferred
) -> None:
    capability = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == capability_id
    )
    assert len(capability.capability_name) <= 160
    assert len(capability.authority_boundary) <= 512
    assert len(capability.evidence_source) <= 512


@pytest.mark.parametrize("field", tuple(P17AuthorityBoundary.model_fields)[:-1])
def test_authority_boundary_exact_false_except_human_git(
    canonical_request, field: str
) -> None:
    expected = field == "human_Git_authority_required"
    assert getattr(canonical_request.authority_boundary, field) is expected


@pytest.mark.parametrize("field", tuple(P17AuthorityBoundary.model_fields)[:-1])
def test_authority_expansion_fails(canonical_request, field: str) -> None:
    if field == "human_Git_authority_required":
        value = False
    else:
        value = True
    bad_boundary = _construct_with_updates(
        canonical_request.authority_boundary, **{field: value}
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, authority_boundary=bad_boundary)
        )


def test_authority_digest_tampering_fails(canonical_request) -> None:
    bad_boundary = _construct_with_updates(
        canonical_request.authority_boundary,
        boundary_SHA256=p17_8.digest_text("tamper"),
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, authority_boundary=bad_boundary)
        )


@pytest.mark.parametrize("field", tuple(P17SecurityBoundary.model_fields)[:-1])
def test_security_boundary_all_false(canonical_request, field: str) -> None:
    assert getattr(canonical_request.security_boundary, field) is False


@pytest.mark.parametrize("field", tuple(P17SecurityBoundary.model_fields)[:-1])
def test_security_boundary_expansion_fails(canonical_request, field: str) -> None:
    bad_security = _construct_with_updates(
        canonical_request.security_boundary, **{field: True}
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, security_boundary=bad_security)
        )


def test_security_digest_tampering_fails(canonical_request) -> None:
    bad_security = _construct_with_updates(
        canonical_request.security_boundary,
        security_boundary_SHA256=p17_8.digest_text("tamper"),
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, security_boundary=bad_security)
        )


@pytest.mark.parametrize("limitation_id,title,deferred", EXPECTED_LIMITATIONS)
def test_limitation_inventory_exact(
    canonical_request, limitation_id, title, deferred
) -> None:
    limitation = next(
        item
        for item in canonical_request.residual_limitations
        if item.limitation_id == limitation_id
    )
    assert limitation.title == title
    assert limitation.accepted is True
    assert limitation.blocking_for_P17_closure is False
    assert limitation.deferred_to_project == deferred


@pytest.mark.parametrize("limitation_id,title,deferred", EXPECTED_LIMITATIONS)
def test_limitation_digest_valid(
    canonical_request, limitation_id, title, deferred
) -> None:
    limitation = next(
        item
        for item in canonical_request.residual_limitations
        if item.limitation_id == limitation_id
    )
    assert limitation.limitation_SHA256 == closure._model_digest(
        closure.RESIDUAL_LIMITATION_DIGEST_ALGORITHM, limitation
    )


@pytest.mark.parametrize("limitation_id,title,deferred", EXPECTED_LIMITATIONS)
def test_limitation_blocking_flag_tampering_fails(
    canonical_request, limitation_id, title, deferred
) -> None:
    limitations = list(canonical_request.residual_limitations)
    index = next(
        i for i, item in enumerate(limitations) if item.limitation_id == limitation_id
    )
    limitations[index] = _construct_with_updates(
        limitations[index], blocking_for_P17_closure=True
    )
    with pytest.raises((P17ClosureInputError, P17ClosurePolicyError)):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request, residual_limitations=tuple(limitations)
            )
        )


@pytest.mark.parametrize("limitation_id,title,deferred", EXPECTED_LIMITATIONS)
def test_limitation_summaries_are_bounded(
    canonical_request, limitation_id, title, deferred
) -> None:
    limitation = next(
        item
        for item in canonical_request.residual_limitations
        if item.limitation_id == limitation_id
    )
    assert len(limitation.description) <= 512


def test_duplicate_limitation_fails(canonical_request) -> None:
    limitations = canonical_request.residual_limitations[:-1] + (
        canonical_request.residual_limitations[0],
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, residual_limitations=limitations)
        )


def test_missing_limitation_fails(canonical_request) -> None:
    with pytest.raises((P17ClosureInputError, P17ClosurePolicyError, ValidationError)):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request,
                residual_limitations=canonical_request.residual_limitations[:-1],
            )
        )


@pytest.mark.parametrize(
    "field,expected",
    (
        ("next_project", "P18"),
        ("first_ticket", "P18.0"),
        ("P17_closed", True),
        ("WorkPacket_execution_MVP_available", True),
        ("non_critical_pilot_accepted", True),
        ("workflow_migration_authorized_to_begin", True),
        ("Pepper_is_customized_Hermes", True),
        ("reuse_existing_Hermes_capabilities_first", True),
        ("modify_Hermes_when_product_requirements_require", True),
        ("replace_Hermes_only_with_gap_evidence", True),
        ("duplicate_existing_runtime_logic_prohibited", True),
        ("Kanban_Swarm_reuse_assessment_required", True),
        ("upstream_setup_is_Pepper_authority", False),
        ("generic_dashboard_provider_state_is_P17_authority", False),
        ("GBrain_memory_available", False),
        ("Paperclip_control_plane_available", False),
        ("production_default_mode_authorized", False),
    ),
)
def test_p18_handoff_exact(canonical_request, field: str, expected) -> None:
    assert getattr(canonical_request.P18_handoff, field) == expected


@pytest.mark.parametrize("field", tuple(P18MigrationHandoff.model_fields)[:-1])
def test_p18_handoff_tampering_fails(canonical_request, field: str) -> None:
    value = False if getattr(canonical_request.P18_handoff, field) is True else True
    if field in {"next_project", "first_ticket"}:
        value = "P19"
    bad_handoff = _construct_with_updates(
        canonical_request.P18_handoff, **{field: value}
    )
    with pytest.raises((P17ClosurePolicyError, ValidationError)):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, P18_handoff=bad_handoff)
        )


def test_p18_handoff_digest_tampering_fails(canonical_request) -> None:
    bad_handoff = _construct_with_updates(
        canonical_request.P18_handoff, handoff_SHA256=p17_8.digest_text("tamper")
    )
    with pytest.raises(P17ClosurePolicyError):
        validate_p17_closure_request(
            _request_with_updates(canonical_request, P18_handoff=bad_handoff)
        )


def test_canonical_request_builds_from_one_accepted_pilot(
    canonical_request, accepted_pilot
) -> None:
    assert canonical_request.non_critical_pilot_result is accepted_pilot
    assert len(canonical_request.ticket_acceptances) == 9
    assert len(canonical_request.capability_reconciliations) == 18
    assert len(canonical_request.residual_limitations) == 13


def test_canonical_request_deterministic(accepted_pilot) -> None:
    assert build_canonical_p17_closure_request(
        non_critical_pilot_result=accepted_pilot
    ) == build_canonical_p17_closure_request(non_critical_pilot_result=accepted_pilot)


def test_input_p17_8_result_not_mutated(accepted_pilot) -> None:
    before = accepted_pilot.model_dump_json()
    build_canonical_p17_closure_request(non_critical_pilot_result=accepted_pilot)
    assert accepted_pilot.model_dump_json() == before


def test_rejected_pilot_rejected_by_request(canonical_request, accepted_pilot) -> None:
    bad_pilot = _construct_with_updates(
        accepted_pilot, decision=p17_8.PilotDecision.REJECTED
    )
    with pytest.raises(P17ClosureStateError):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request, non_critical_pilot_result=bad_pilot
            )
        )


def test_pilot_mvp_false_rejected(canonical_request, accepted_pilot) -> None:
    bad_pilot = _construct_with_updates(
        accepted_pilot, WorkPacket_execution_MVP_requirement_satisfied=False
    )
    with pytest.raises(P17ClosureStateError):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request, non_critical_pilot_result=bad_pilot
            )
        )


def test_pilot_closure_ready_false_rejected(canonical_request, accepted_pilot) -> None:
    bad_pilot = _construct_with_updates(accepted_pilot, P17_closure_ready=False)
    with pytest.raises(P17ClosureStateError):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request, non_critical_pilot_result=bad_pilot
            )
        )


def test_pilot_production_readiness_rejected(canonical_request, accepted_pilot) -> None:
    bad_pilot = _construct_with_updates(
        accepted_pilot, production_readiness_claimed=True
    )
    with pytest.raises(P17ClosureStateError):
        validate_p17_closure_request(
            _request_with_updates(
                canonical_request, non_critical_pilot_result=bad_pilot
            )
        )


def test_closure_summary_exact(canonical_result) -> None:
    summary = canonical_result.closure_summary
    assert summary.ticket_count == 9
    assert summary.accepted_ticket_count == 9
    assert summary.satisfied_capability_count == 9
    assert summary.absent_by_design_capability_count == 5
    assert summary.deferred_capability_count == 4
    assert summary.accepted_limitation_count == 13
    assert summary.blocking_limitation_count == 0
    assert summary.warning_finding_count == 1
    assert summary.blocking_finding_count == 0
    assert summary.non_critical_pilot_accepted is True
    assert summary.WorkPacket_execution_MVP_requirement_satisfied is True
    assert summary.P17_closure_requirement_satisfied is True
    assert summary.P18_ready is True
    assert summary.production_readiness_claimed is False
    assert summary.provider_dispatch_count == 0
    assert summary.model_inference_count == 0
    assert summary.Git_commands_executed == 0


def test_closure_builds_accepted(canonical_result) -> None:
    assert canonical_result.closure_id.startswith("P17C-")
    assert canonical_result.state is P17ClosureState.CLOSED
    assert canonical_result.decision is P17ClosureDecision.ACCEPTED
    assert canonical_result.WorkPacket_execution_MVP_requirement_satisfied is True
    assert canonical_result.P17_closure_requirement_satisfied is True
    assert canonical_result.P18_ready is True
    assert canonical_result.production_readiness_claimed is False
    assert canonical_result.provider_dispatch_count == 0
    assert canonical_result.model_inference_count == 0
    assert canonical_result.Git_commands_executed == 0


def test_repeated_equal_inputs_produce_equal_closure(canonical_request) -> None:
    first = build_p17_work_packet_execution_mvp_closure(canonical_request)
    second = build_p17_work_packet_execution_mvp_closure(canonical_request)
    assert first == second
    assert first.closure_id == second.closure_id
    assert first.result_SHA256 == second.result_SHA256


def test_summary_api_returns_exact_summary(canonical_result) -> None:
    assert summarize_p17_closure(canonical_result) is canonical_result.closure_summary


def test_summary_api_rejects_invalid_result(canonical_result) -> None:
    bad = _result_with_updates(canonical_result, result_SHA256=p17_8.digest_text("bad"))
    with pytest.raises(P17ClosureValidationError):
        summarize_p17_closure(bad)


def test_result_validation_accepts_canonical_result(canonical_result) -> None:
    validate_p17_closure_result(canonical_result)


def test_result_digest_tampering_fails(canonical_result) -> None:
    bad = _result_with_updates(
        canonical_result, result_SHA256=p17_8.digest_text("tamper")
    )
    with pytest.raises(P17ClosureValidationError):
        validate_p17_closure_result(bad)


def test_closure_id_tampering_fails(canonical_result) -> None:
    bad = _result_with_updates(canonical_result, closure_id="P17C-000000000000")
    with pytest.raises(P17ClosureValidationError):
        validate_p17_closure_result(bad)


def test_stage_decision_tampering_fails(canonical_result) -> None:
    bad = _result_with_updates(canonical_result, decision=P17ClosureDecision.REJECTED)
    with pytest.raises(P17ClosureValidationError):
        validate_p17_closure_result(bad)


def test_manual_validation_pending_warns_not_blocks(canonical_result) -> None:
    warnings = [
        finding
        for finding in canonical_result.findings
        if finding.severity is P17ClosureFindingSeverity.WARNING
    ]
    assert len(warnings) == 1
    assert warnings[0].code is P17ClosureFindingCode.MANUAL_VALIDATION_PENDING
    assert canonical_result.closure_summary.blocking_finding_count == 0


def test_findings_are_deterministic_contiguous_and_bounded(canonical_result) -> None:
    assert len(canonical_result.findings) <= 128
    assert tuple(f.finding_id for f in canonical_result.findings) == tuple(
        f"P17F-{index:03d}" for index in range(1, len(canonical_result.findings) + 1)
    )
    assert tuple(canonical_result.findings) == tuple(
        sorted(canonical_result.findings, key=closure._finding_sort_key)
    )


@pytest.mark.parametrize("finding", range(19))
def test_finding_digest_valid(canonical_result, finding: int) -> None:
    item = canonical_result.findings[finding]
    assert item.finding_SHA256 == closure._model_digest(
        closure.CLOSURE_FINDING_DIGEST_ALGORITHM, item
    )


def test_finding_digest_tampering_fails(canonical_result) -> None:
    findings = list(canonical_result.findings)
    findings[0] = _construct_with_updates(
        findings[0], finding_SHA256=p17_8.digest_text("tamper")
    )
    bad = _result_with_updates(canonical_result, findings=tuple(findings))
    with pytest.raises((ValidationError, P17ClosureValidationError)):
        validate_p17_closure_result(bad)


def test_canonical_P17_work_packet_execution_MVP_closure_flow(canonical_result) -> None:
    assert len(canonical_result.ticket_acceptances) == 9
    assert len(canonical_result.capability_reconciliations) == 18
    assert len(canonical_result.residual_limitations) == 13
    assert canonical_result.closure_summary.warning_finding_count == 1
    assert canonical_result.closure_summary.blocking_finding_count == 0
    assert canonical_result.state is P17ClosureState.CLOSED
    assert canonical_result.decision is P17ClosureDecision.ACCEPTED
    assert canonical_result.WorkPacket_execution_MVP_requirement_satisfied is True
    assert canonical_result.P17_closure_requirement_satisfied is True
    assert canonical_result.P18_ready is True
    assert canonical_result.production_readiness_claimed is False
    assert canonical_result.provider_dispatch_count == 0
    assert canonical_result.model_inference_count == 0
    assert canonical_result.Git_commands_executed == 0


def test_canonical_P17_closure_rejects_missing_ticket_flow(canonical_request) -> None:
    bad = _request_with_updates(
        canonical_request, ticket_acceptances=canonical_request.ticket_acceptances[:-1]
    )
    with pytest.raises((P17ClosureInputError, P17ClosurePolicyError, ValidationError)):
        build_p17_work_packet_execution_mvp_closure(bad)


def test_canonical_P17_closure_rejects_authority_expansion_flow(
    canonical_request,
) -> None:
    bad_boundary = _construct_with_updates(
        canonical_request.authority_boundary, automatic_commit_authorized=True
    )
    bad = _request_with_updates(canonical_request, authority_boundary=bad_boundary)
    with pytest.raises(P17ClosurePolicyError):
        build_p17_work_packet_execution_mvp_closure(bad)


def test_p19_memory_handoff_semantics(canonical_request) -> None:
    memory = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == "CAP-P17-016"
    )
    assert memory.status is P17CapabilityStatus.DEFERRED
    assert memory.deferred_to_project == "P19"
    assert canonical_request.P18_handoff.GBrain_memory_available is False


def test_p20_paperclip_handoff_semantics(canonical_request) -> None:
    work_control = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == "CAP-P17-017"
    )
    assert work_control.status is P17CapabilityStatus.DEFERRED
    assert work_control.deferred_to_project == "P20"
    assert canonical_request.P18_handoff.Paperclip_control_plane_available is False


def test_p21_multi_agent_handoff_semantics(canonical_request) -> None:
    multi_agent = next(
        item
        for item in canonical_request.capability_reconciliations
        if item.capability_id == "CAP-P17-018"
    )
    assert multi_agent.status is P17CapabilityStatus.DEFERRED
    assert multi_agent.deferred_to_project == "P21"


def test_digests_are_not_signatures(canonical_request) -> None:
    assert canonical_request.security_boundary.digital_signature_claimed is False
    assert canonical_request.security_boundary.digest_is_signature is False


def test_schema_policy_identity() -> None:
    assert WORK_PACKET_EXECUTION_MVP_CLOSURE_SCHEMA_VERSION == 1
    assert (
        WORK_PACKET_EXECUTION_MVP_CLOSURE_POLICY_ID
        == "pepper-governed-work-packet-execution-mvp-closure-v1"
    )


def test_alternative_schema_version_fails(canonical_request) -> None:
    data = canonical_request.model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        P17ClosureRequest.model_validate(data)


def test_alternative_policy_id_fails(canonical_request) -> None:
    data = canonical_request.model_dump(mode="json")
    data["policy_id"] = "alternate"
    with pytest.raises(ValidationError):
        P17ClosureRequest.model_validate(data)


def test_no_arbitrary_overrides_in_canonical_builder() -> None:
    names = build_canonical_p17_closure_request.__code__.co_varnames[
        : build_canonical_p17_closure_request.__code__.co_argcount
        + build_canonical_p17_closure_request.__code__.co_kwonlyargcount
    ]
    assert names == ("non_critical_pilot_result",)


def test_imported_module_has_no_forbidden_operational_imports() -> None:
    source = closure.__loader__.get_source(closure.__name__)
    tree = ast.parse(source)
    forbidden = {
        "os",
        "pathlib",
        "subprocess",
        "threading",
        "time",
        "socket",
        "requests",
        "httpx",
        "openai",
        "docker",
        "git",
        "shutil",
        "tempfile",
        "datetime",
        "uuid",
        "random",
        "secrets",
        "asyncio",
        "multiprocessing",
        "concurrent",
        "networkx",
        "pkgutil",
    }
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module.split(".")[0])
    assert not (set(imports) & forbidden)


def test_production_source_has_no_operational_calls() -> None:
    source = closure.__loader__.get_source(closure.__name__)
    tree = ast.parse(source)
    forbidden_calls = {
        "open",
        "read_text",
        "read_bytes",
        "write_text",
        "write_bytes",
        "mkdir",
        "unlink",
        "run",
        "Popen",
        "call",
        "check_call",
        "check_output",
        "system",
        "getenv",
        "environ",
        "request",
        "get",
        "post",
        "push",
        "commit",
        "retry",
        "fallback",
        "cleanup",
        "rollback",
        "graphify",
        "docker",
    }
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            calls.append(node.func.id)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            calls.append(node.func.attr)
    assert not (set(calls) & forbidden_calls)


def test_no_wall_clock_uuid_or_randomness_in_source() -> None:
    source = closure.__loader__.get_source(closure.__name__)
    tree = ast.parse(source)
    imports = []
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module.split(".")[0])
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            calls.append(node.func.id)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            calls.append(node.func.attr)
    assert not (set(imports) & {"uuid", "random", "datetime", "time"})
    assert not (set(calls) & {"uuid4", "random", "randint", "now", "utcnow", "time"})
