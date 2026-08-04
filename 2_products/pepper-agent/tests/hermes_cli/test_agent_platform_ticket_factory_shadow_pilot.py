import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import ticket_factory
import hermes_cli.agent_platform.ticket_factory.shadow_pilot as shadow_pilot


P16_4_FINAL_EXPORTS = (
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
P16_8_EXPORTS = (
    "TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION",
    "TICKET_FACTORY_SHADOW_PILOT_ID",
    "TICKET_FACTORY_SHADOW_PILOT_REVISION",
    "ShadowPilotStage",
    "ShadowPilotGate",
    "ShadowPilotGateStatus",
    "ShadowPilotDisposition",
    "ShadowPilotArtifactKind",
    "ShadowPilotEvidence",
    "ShadowPilotStageResult",
    "ShadowPilotGateResult",
    "TicketFactoryShadowPilotRequest",
    "TicketFactoryShadowPilotReport",
    "TicketFactoryShadowPilotError",
    "TicketFactoryShadowPilotInputError",
    "TicketFactoryShadowPilotExecutionError",
    "TicketFactoryShadowPilotIntegrityError",
    "get_canonical_ticket_factory_shadow_pilot_request",
    "run_ticket_factory_shadow_pilot",
    "validate_ticket_factory_shadow_pilot_report",
    "summarize_ticket_factory_shadow_pilot_report",
    "get_ticket_factory_shadow_pilot_stage_order",
    "get_ticket_factory_shadow_pilot_gate_order",
    "canonical_ticket_factory_shadow_pilot_output",
)
UNEXPORTED_DIGEST_CONSTANTS = (
    "REQUEST_DIGEST_ALGORITHM",
    "EVIDENCE_DIGEST_ALGORITHM",
    "STAGE_RESULT_DIGEST_ALGORITHM",
    "GATE_RESULT_DIGEST_ALGORITHM",
    "REPORT_DIGEST_ALGORITHM",
)
PUBLIC_MODELS = (
    shadow_pilot.ShadowPilotEvidence,
    shadow_pilot.ShadowPilotStageResult,
    shadow_pilot.ShadowPilotGateResult,
    shadow_pilot.TicketFactoryShadowPilotRequest,
    shadow_pilot.TicketFactoryShadowPilotReport,
)
EXPECTED_ENUM_VALUES = {
    shadow_pilot.ShadowPilotStage: (
        "historical_preflight",
        "context_assembly",
        "dependency_planning",
        "generator_assignment",
        "proposal_review",
        "synthesis_review",
        "human_approval",
        "canonical_publication",
    ),
    shadow_pilot.ShadowPilotGate: (
        "historical_regression_clean",
        "policy_lint_pass",
        "synthesis_review_ready",
        "human_approval_present",
    ),
    shadow_pilot.ShadowPilotGateStatus: ("pass", "fail"),
    shadow_pilot.ShadowPilotDisposition: ("go_with_constraints", "blocked"),
    shadow_pilot.ShadowPilotArtifactKind: (
        "historical_regression_run",
        "context_pack",
        "dependency_plan",
        "generator_assignments",
        "ticket_proposals",
        "synthesis_review",
        "approval_record",
        "publication_result",
    ),
}
EXPECTED_REQUEST_SHA256 = (
    "cd13ac9cfd84ee693c3ebb4550a6c46787ff19973b924f75042181056d0a5270"
)
EXPECTED_REPORT_SHA256 = (
    "6cb4158558ebe0e321de10c397e16f05ab306ac3a69b3ef46460d6ab188840da"
)
EXPECTED_ALTERNATE_TITLE = "Ticket Factory shadow pilot dissent check"
EXPECTED_CANONICAL_OUTPUT = (
    "go_with_constraints P16.SP1 pass 12 12 0 4 4 approved published"
)
EXPECTED_STAGE_ARTIFACTS = (
    (
        "historical_preflight",
        "historical_regression_run",
        "HistoricalRegressionRun",
        "86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d",
    ),
    (
        "context_assembly",
        "context_pack",
        "ContextPack",
        "6317f46b4154916e7f87a25c62012cd5191262753f7428706e557a49ef28afed",
    ),
    (
        "dependency_planning",
        "dependency_plan",
        "TicketDependencyPlan",
        "a7f91ccfe52c740e6c16cc78832d6a82c8029e504fbe749202629d7bc8598c71",
    ),
    (
        "generator_assignment",
        "generator_assignments",
        "GeneratorAssignmentTuple",
        "9eb83b519735e06514b6c1bc91cab1089fa137c273d99935c67a23983f3b840d",
    ),
    (
        "proposal_review",
        "ticket_proposals",
        "TicketProposalTuple",
        "f6fd320756c7aa371f6cc20a2605b44d77470de38e1d934b86e4e8636da1baba",
    ),
    (
        "synthesis_review",
        "synthesis_review",
        "TicketSynthesisReview",
        "bd8cea414fb65a2ed88fb28199e25b582f6a8cc2d2dfcdfb9c250d4682a36ff5",
    ),
    (
        "human_approval",
        "approval_record",
        "TicketApprovalRecord",
        "054656084f28aad357178a6709ade3cdf1058ce085590f1b374d88e281d27a30",
    ),
    (
        "canonical_publication",
        "publication_result",
        "TicketPublicationResult",
        "5177775fdb44b34c289887a1d92abcc6b1b780204eaec9bbb0d059cf354b82b4",
    ),
)
EXPECTED_GATES = (
    (
        "historical_regression_clean",
        "historical_preflight",
        "25b335dffb051630890ba1ded594dfeaf122fc79abbfd62135976451b1e9b846",
    ),
    (
        "policy_lint_pass",
        "proposal_review",
        "5bc5393b6f347447c00c02548b49d16e4e7b4e94cf1ce9a414f15e09c4355b23",
    ),
    (
        "synthesis_review_ready",
        "synthesis_review",
        "34796a3f45a5899f37afee4d766c6c05e67801250baab67857573e78d0082c53",
    ),
    (
        "human_approval_present",
        "human_approval",
        "0447feddda75613f520c7f369990388c1eead63966e38b16d4e21bb311df5877",
    ),
)
EXPECTED_ASSIGNMENTS = (
    (
        "architecture",
        "GEN-P16-SP1-ARCHITECTURE",
        "aedd3a30341aeffce6fa6bb600532add42ea2198006dc75d2b380d4b0f6abaf6",
    ),
    (
        "integration",
        "GEN-P16-SP1-INTEGRATION",
        "6bd5f70d582935c36925bb74d4d69f2b4d7927b2ff3464f270209ff4ff30ad14",
    ),
    (
        "governance",
        "GEN-P16-SP1-GOVERNANCE",
        "12e7781b9ba77da727d7f15931b840343971d6c45885386e405462b78c96c9b7",
    ),
    (
        "documentation",
        "GEN-P16-SP1-DOCUMENTATION",
        "10e29001b65216e9f337cc12ab8da7ae497b10ecae31a3f40c9ee7ec53b2892b",
    ),
)
EXPECTED_PROPOSALS = (
    (
        "architecture",
        "3e45ab822c456a09a6cc85e754d34ffedb23dea16fa23bf9e445f068eea071c7",
    ),
    (
        "integration",
        "939b20964d6e2c1fdbd3c087d86b5e2fa6e1e5830833081bfa85cfe358077e34",
    ),
    (
        "governance",
        "abf5508fb3274570718f10fde7de268d6fc2c6b6dcd15d4864ba0a846ad21057",
    ),
    (
        "documentation",
        "7da66a54770a2239986830f791964165b842d462afe0ecc02f86a1cffb9bbb83",
    ),
)
EXPECTED_FIELD_DECISIONS = (
    ("title", "4b01b53e76cdf213c358a8aff025185ccd3b7f4e096d6d028102b0911d168d31"),
    ("objective", "91a58c4dfed9983071cfed2a0261abe9c05d7b958b5befeb419cba23f915bb0f"),
    ("context", "06443f492841b2eae7a7da92a0c7ead492ed813ae82a6b663016c2744c973083"),
    (
        "authority_references",
        "8ac96c86fb209fae4a32cc9ef98f764e35163029db11d5a01d913abe9edaf218",
    ),
    (
        "dependencies",
        "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    ),
    (
        "parallelization_hint",
        "01816b89263624e64a47d2d5727923a8d8b2d8bbcf7e50e80a987e1c2c3978d9",
    ),
    ("scope", "0e9653e49f1771dfde9dc13ff68b805fa2470cb3bfdca086414955d54c1a4304"),
    ("constraints", "14113e8d5d8656f6dee33b5582518e68b4d4687e6f83c572d86bfd04cee2a418"),
    ("tasks", "374bbfa71141b14439d07ea798b4455ce0145fec29d65f2bde0e884273de778e"),
    (
        "acceptance_criteria",
        "a0d9dcde989bb47f84e3348f729c2fd80dfcedf0660f91897046fafbc721fe07",
    ),
    (
        "validation_steps",
        "a8eed59721f4726e45656e931e9e8bb92b68b9632b3613e0c64d4fe09bfaa812",
    ),
    (
        "response_contract",
        "6830b188770a0e28095104e3f3aad2e036e23a74baf2333fa00ce2950d23670e",
    ),
    (
        "recommended_commit_message",
        "c3564fb13b0cb81fe53e217289c547a09bca536c350c924d0a061dd55709f6b6",
    ),
)


@pytest.fixture(scope="module")
def shadow_request() -> shadow_pilot.TicketFactoryShadowPilotRequest:
    return shadow_pilot.get_canonical_ticket_factory_shadow_pilot_request()


@pytest.fixture(scope="module")
def report() -> shadow_pilot.TicketFactoryShadowPilotReport:
    return shadow_pilot.run_ticket_factory_shadow_pilot()


@pytest.fixture(scope="module")
def stage_by_name(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> dict[str, shadow_pilot.ShadowPilotStageResult]:
    return {stage.stage.value: stage for stage in report.stage_results}


@pytest.fixture(scope="module")
def gate_by_name(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> dict[str, shadow_pilot.ShadowPilotGateResult]:
    return {gate.gate.value: gate for gate in report.gate_results}


@pytest.mark.parametrize("export_name", P16_8_EXPORTS)
def test_p16_8_root_exports_resolve_to_module(export_name: str) -> None:
    root_value = getattr(ticket_factory, export_name)
    module_value = getattr(shadow_pilot, export_name)

    assert export_name in ticket_factory.__all__
    if isinstance(module_value, int | str):
        assert root_value == module_value
    else:
        assert root_value is module_value


def test_p16_8_adds_exactly_24_root_exports() -> None:
    assert len(P16_8_EXPORTS) == 24
    assert len(set(P16_8_EXPORTS)) == 24
    assert all(export_name in ticket_factory.__all__ for export_name in P16_8_EXPORTS)


def test_p16_8_root_exports_are_inserted_before_p16_4_final_block() -> None:
    assert ticket_factory.__all__[-len(P16_4_FINAL_EXPORTS) :] == P16_4_FINAL_EXPORTS
    assert ticket_factory.__all__.index(
        P16_8_EXPORTS[0]
    ) < ticket_factory.__all__.index(P16_4_FINAL_EXPORTS[0])


@pytest.mark.parametrize("constant_name", UNEXPORTED_DIGEST_CONSTANTS)
def test_digest_algorithm_constants_are_not_root_exports(constant_name: str) -> None:
    assert hasattr(shadow_pilot, constant_name)
    assert constant_name not in ticket_factory.__all__
    assert not hasattr(ticket_factory, constant_name)


@pytest.mark.parametrize("model", PUBLIC_MODELS)
def test_public_models_are_frozen_extra_forbid(model: type) -> None:
    assert model.model_config.get("frozen") is True
    assert model.model_config.get("extra") == "forbid"
    assert model.model_config.get("validate_default") is True


@pytest.mark.parametrize("enum_type,expected_values", EXPECTED_ENUM_VALUES.items())
def test_public_enums_have_frozen_values(
    enum_type: type, expected_values: tuple[str, ...]
) -> None:
    assert tuple(item.value for item in enum_type) == expected_values


def test_shadow_pilot_identity_constants() -> None:
    assert shadow_pilot.TICKET_FACTORY_SHADOW_PILOT_SCHEMA_VERSION == 1
    assert (
        shadow_pilot.TICKET_FACTORY_SHADOW_PILOT_ID
        == "pepper-ticket-factory-shadow-pilot-v1"
    )
    assert shadow_pilot.TICKET_FACTORY_SHADOW_PILOT_REVISION == 1


def test_canonical_request_identity(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    assert shadow_request.pilot_id == "pepper-ticket-factory-shadow-pilot-v1"
    assert shadow_request.revision == 1
    assert shadow_request.seed_ticket.ticket_id == "P16.SP1"
    assert shadow_request.shadow_only is True
    assert shadow_request.allow_provider_calls is False
    assert shadow_request.allow_model_calls is False
    assert shadow_request.allow_runtime_execution is False
    assert shadow_request.allow_filesystem_writes is False
    assert shadow_request.allow_git_mutation is False


def test_canonical_request_round_trips(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    assert (
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate_json(
            shadow_request.model_dump_json()
        )
        == shadow_request
    )


def test_canonical_report_identity(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert report.pilot_id == "pepper-ticket-factory-shadow-pilot-v1"
    assert report.ticket_id == "P16.SP1"
    assert report.request_SHA256 == EXPECTED_REQUEST_SHA256
    assert report.report_SHA256 == EXPECTED_REPORT_SHA256
    assert report.disposition is shadow_pilot.ShadowPilotDisposition.GO_WITH_CONSTRAINTS


def test_canonical_report_round_trips(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert (
        shadow_pilot.TicketFactoryShadowPilotReport.model_validate_json(
            report.model_dump_json()
        )
        == report
    )


def test_validate_report_returns_none(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert shadow_pilot.validate_ticket_factory_shadow_pilot_report(report) is None


def test_canonical_output_exact() -> None:
    assert (
        shadow_pilot.canonical_ticket_factory_shadow_pilot_output()
        == EXPECTED_CANONICAL_OUTPUT
    )
    assert (
        ticket_factory.canonical_ticket_factory_shadow_pilot_output()
        == EXPECTED_CANONICAL_OUTPUT
    )


def test_summarize_report_exact(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert (
        shadow_pilot.summarize_ticket_factory_shadow_pilot_report(report)
        == EXPECTED_CANONICAL_OUTPUT
    )


def test_stage_order_function_matches_report(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert tuple(stage.stage for stage in report.stage_results) == (
        shadow_pilot.get_ticket_factory_shadow_pilot_stage_order()
    )


def test_gate_order_function_matches_report(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert tuple(gate.gate for gate in report.gate_results) == (
        shadow_pilot.get_ticket_factory_shadow_pilot_gate_order()
    )


@pytest.mark.parametrize(
    "stage_name,artifact_kind,artifact_type,artifact_sha", EXPECTED_STAGE_ARTIFACTS
)
def test_stage_evidence_is_frozen(
    stage_name: str,
    artifact_kind: str,
    artifact_type: str,
    artifact_sha: str,
    stage_by_name: dict[str, shadow_pilot.ShadowPilotStageResult],
) -> None:
    stage = stage_by_name[stage_name]

    assert stage.status is shadow_pilot.ShadowPilotGateStatus.PASS
    assert stage.evidence.stage.value == stage_name
    assert stage.evidence.artifact_kind.value == artifact_kind
    assert stage.evidence.artifact_type == artifact_type
    assert stage.evidence.artifact_SHA256 == artifact_sha


@pytest.mark.parametrize("gate_name,stage_name,gate_sha", EXPECTED_GATES)
def test_gate_evidence_is_frozen(
    gate_name: str,
    stage_name: str,
    gate_sha: str,
    gate_by_name: dict[str, shadow_pilot.ShadowPilotGateResult],
) -> None:
    gate = gate_by_name[gate_name]

    assert gate.stage.value == stage_name
    assert gate.status is shadow_pilot.ShadowPilotGateStatus.PASS
    assert gate.gate_SHA256 == gate_sha


@pytest.mark.parametrize("stage_name", [item[0] for item in EXPECTED_STAGE_ARTIFACTS])
def test_stage_results_round_trip(
    stage_name: str,
    stage_by_name: dict[str, shadow_pilot.ShadowPilotStageResult],
) -> None:
    stage = stage_by_name[stage_name]

    assert (
        shadow_pilot.ShadowPilotStageResult.model_validate(
            stage.model_dump(mode="json")
        )
        == stage
    )


@pytest.mark.parametrize("stage_name", [item[0] for item in EXPECTED_STAGE_ARTIFACTS])
def test_stage_evidence_round_trips(
    stage_name: str,
    stage_by_name: dict[str, shadow_pilot.ShadowPilotStageResult],
) -> None:
    evidence = stage_by_name[stage_name].evidence

    assert (
        shadow_pilot.ShadowPilotEvidence.model_validate(
            evidence.model_dump(mode="json")
        )
        == evidence
    )


@pytest.mark.parametrize("gate_name", [item[0] for item in EXPECTED_GATES])
def test_gate_results_round_trip(
    gate_name: str,
    gate_by_name: dict[str, shadow_pilot.ShadowPilotGateResult],
) -> None:
    gate = gate_by_name[gate_name]

    assert (
        shadow_pilot.ShadowPilotGateResult.model_validate(gate.model_dump(mode="json"))
        == gate
    )


@pytest.mark.parametrize("stage_name", [item[0] for item in EXPECTED_STAGE_ARTIFACTS])
def test_stage_evidence_rejects_tampered_digest(
    stage_name: str,
    stage_by_name: dict[str, shadow_pilot.ShadowPilotStageResult],
) -> None:
    data = stage_by_name[stage_name].evidence.model_dump(mode="json")
    data["evidence_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="evidence_SHA256"):
        shadow_pilot.ShadowPilotEvidence.model_validate(data)


@pytest.mark.parametrize("stage_name", [item[0] for item in EXPECTED_STAGE_ARTIFACTS])
def test_stage_result_rejects_tampered_digest(
    stage_name: str,
    stage_by_name: dict[str, shadow_pilot.ShadowPilotStageResult],
) -> None:
    data = stage_by_name[stage_name].model_dump(mode="json")
    data["stage_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="stage_SHA256"):
        shadow_pilot.ShadowPilotStageResult.model_validate(data)


@pytest.mark.parametrize("gate_name", [item[0] for item in EXPECTED_GATES])
def test_gate_result_rejects_tampered_digest(
    gate_name: str,
    gate_by_name: dict[str, shadow_pilot.ShadowPilotGateResult],
) -> None:
    data = gate_by_name[gate_name].model_dump(mode="json")
    data["gate_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="gate_SHA256"):
        shadow_pilot.ShadowPilotGateResult.model_validate(data)


def test_historical_preflight_is_pass(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    run = report.historical_run

    assert run.disposition.value == "pass"
    assert len(run.case_results) == 12
    assert len(run.passed_case_ids) == 12
    assert run.drifted_case_ids == ()


@pytest.mark.parametrize("case_index", range(12))
def test_historical_preflight_case_ids_are_ordered(
    case_index: int,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert (
        report.historical_run.case_results[case_index].case_id
        == f"HIST-{case_index + 1:03d}"
    )


@pytest.mark.parametrize("case_index", range(12))
def test_historical_preflight_cases_are_matched(
    case_index: int,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert report.historical_run.case_results[case_index].matched is True
    assert report.historical_run.case_results[case_index].drifts == ()


@pytest.mark.parametrize("role,assignment_id,assignment_sha", EXPECTED_ASSIGNMENTS)
def test_assignments_are_canonical(
    role: str,
    assignment_id: str,
    assignment_sha: str,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assignment = next(item for item in report.assignments if item.role.value == role)

    assert assignment.assignment_id == assignment_id
    assert assignment.ticket_id == "P16.SP1"
    assert assignment.assignment_SHA256 == assignment_sha


@pytest.mark.parametrize("role,proposal_sha", EXPECTED_PROPOSALS)
def test_proposals_are_canonical(
    role: str,
    proposal_sha: str,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    proposal = next(item for item in report.proposals if item.role.value == role)

    assert proposal.ticket_id == "P16.SP1"
    assert proposal.proposal_SHA256 == proposal_sha
    assert proposal.evidence_source_ids == (
        "CTX-SHADOW-PILOT-GOVERNANCE",
        "CTX-HISTORICAL-REGRESSION",
    )


@pytest.mark.parametrize("role,proposal_sha", EXPECTED_PROPOSALS[:3])
def test_three_canonical_proposals_use_seed_title(
    role: str,
    proposal_sha: str,
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    proposal = next(
        item for item in report.proposals if item.proposal_SHA256 == proposal_sha
    )

    assert proposal.role.value == role
    assert proposal.proposed_ticket == shadow_request.seed_ticket


def test_one_canonical_proposal_uses_distinct_alternate_title(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    proposal = next(
        item for item in report.proposals if item.role.value == "documentation"
    )

    assert proposal.proposed_ticket.title == EXPECTED_ALTERNATE_TITLE
    assert proposal.proposed_ticket.title != shadow_request.seed_ticket.title
    assert proposal.proposed_ticket.model_dump(mode="json") == {
        **shadow_request.seed_ticket.model_dump(mode="json"),
        "title": EXPECTED_ALTERNATE_TITLE,
    }


def test_alternate_title_survives_model_normalization() -> None:
    assert (
        shadow_pilot.SHADOW_PILOT_ALTERNATE_TITLE.strip()
        == shadow_pilot.SHADOW_PILOT_ALTERNATE_TITLE
    )
    assert (
        shadow_pilot.SHADOW_PILOT_ALTERNATE_TITLE
        != shadow_pilot.get_canonical_ticket_factory_shadow_pilot_request().seed_ticket.title
    )


@pytest.mark.parametrize("role,proposal_sha", EXPECTED_PROPOSALS)
def test_proposal_digests_round_trip(
    role: str,
    proposal_sha: str,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    proposal = next(item for item in report.proposals if item.role.value == role)

    assert proposal.proposal_SHA256 == proposal_sha
    assert type(proposal).model_validate(proposal.model_dump(mode="json")) == proposal


def test_ticket_lint_report_passes(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    assert report.ticket_lint_report.disposition.value == "pass"
    assert report.ticket_lint_report.summary.diagnostic_count == 0
    assert report.ticket_lint_report.report_SHA256 == (
        "32733854df63ec60a5c05c3601873d75b4dca28df2f788407e512a14ab67d39d"
    )


def test_dependency_plan_is_single_shadow_ticket(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    plan = report.dependency_plan

    assert plan.ticket_ids == ("P16.SP1",)
    assert plan.edges == ()
    assert plan.blocked_ticket_ids == ()
    assert plan.waves[0].ticket_ids == ("P16.SP1",)
    assert plan.plan_SHA256 == (
        "a7f91ccfe52c740e6c16cc78832d6a82c8029e504fbe749202629d7bc8598c71"
    )


def test_context_pack_contains_authorized_sources(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    source_ids = tuple(item.source_id for item in report.context_pack.items)

    assert source_ids[:2] == ("CTX-PROJECT-SPEC", "CTX-TICKET-SPEC")
    assert "CTX-SHADOW-PILOT-GOVERNANCE" in source_ids
    assert "CTX-HISTORICAL-REGRESSION" in source_ids
    assert report.context_pack.context_pack_SHA256 == (
        "6317f46b4154916e7f87a25c62012cd5191262753f7428706e557a49ef28afed"
    )


def test_synthesis_review_is_review_ready_with_title_dissent(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    review = report.synthesis_review
    title_conflicts = [
        conflict
        for conflict in review.conflicts
        if conflict.kind is ticket_factory.ProposalConflictKind.FIELD_DISSENT
        and conflict.field is ticket_factory.TicketSynthesisField.TITLE
    ]

    assert (
        review.disposition
        is ticket_factory.TicketSynthesisDisposition.REVIEW_READY_WITH_DISSENT
    )
    assert len(review.eligible_proposal_SHA256s) == 4
    assert review.excluded_proposal_SHA256s == ()
    assert len(review.conflicts) == 1
    assert len(title_conflicts) == 1
    assert review.candidate is not None
    assert review.candidate.synthesized_ticket == report.generation_request.ticket_spec
    assert len(review.field_decisions) == 13


@pytest.mark.parametrize("field_name,selected_sha", EXPECTED_FIELD_DECISIONS)
def test_synthesis_field_decisions_have_expected_resolution(
    field_name: str,
    selected_sha: str,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    decision = next(
        item
        for item in report.synthesis_review.field_decisions
        if item.field.value == field_name
    )

    if field_name == "title":
        assert decision.agreement_level.value == "strict_majority"
        assert decision.resolution.value == "adopt_strict_majority"
    else:
        assert decision.agreement_level.value == "unanimous"
        assert decision.resolution.value == "adopt_unanimous"
    assert decision.selected_value_SHA256 == selected_sha


@pytest.mark.parametrize("field_name,selected_sha", EXPECTED_FIELD_DECISIONS)
def test_synthesis_field_support_covers_all_proposals(
    field_name: str,
    selected_sha: str,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    decision = next(
        item
        for item in report.synthesis_review.field_decisions
        if item.field.value == field_name
    )

    assert decision.selected_value_SHA256 == selected_sha
    if field_name == "title":
        assert len(decision.variants) == 2
        assert tuple(variant.support_count for variant in decision.variants) == (3, 1)
        assert len(decision.supporting_proposal_SHA256s) == 3
        assert len(decision.dissenting_proposal_SHA256s) == 1
    else:
        assert len(decision.variants) == 1
        assert decision.variants[0].support_count == 4
        assert len(decision.supporting_proposal_SHA256s) == 4
        assert decision.dissenting_proposal_SHA256s == ()


def test_title_variant_counts_are_three_and_one(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    title_decision = next(
        item
        for item in report.synthesis_review.field_decisions
        if item.field is ticket_factory.TicketSynthesisField.TITLE
    )
    titles = tuple(proposal.proposed_ticket.title for proposal in report.proposals)

    assert len(frozenset(titles)) == 2
    assert titles.count(shadow_request.seed_ticket.title) == 3
    assert titles.count(EXPECTED_ALTERNATE_TITLE) == 1
    assert tuple(variant.support_count for variant in title_decision.variants) == (3, 1)


def test_non_title_synthesis_fields_are_unanimous(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    for decision in report.synthesis_review.field_decisions:
        if decision.field is ticket_factory.TicketSynthesisField.TITLE:
            continue
        assert (
            decision.agreement_level is ticket_factory.ProposalAgreementLevel.UNANIMOUS
        )
        assert decision.resolution is ticket_factory.FieldResolutionKind.ADOPT_UNANIMOUS
        assert len(decision.variants) == 1


def test_synthesis_conflicts_are_only_title_dissent(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    conflicts = report.synthesis_review.conflicts
    dissent = [
        conflict
        for conflict in conflicts
        if conflict.kind is ticket_factory.ProposalConflictKind.FIELD_DISSENT
    ]
    split = [
        conflict
        for conflict in conflicts
        if conflict.kind is ticket_factory.ProposalConflictKind.FIELD_SPLIT
    ]
    dependency_stale = [
        conflict
        for conflict in conflicts
        if conflict.kind is ticket_factory.ProposalConflictKind.DEPENDENCY_PLAN_STALE
    ]
    scope_stale = [
        conflict
        for conflict in conflicts
        if conflict.kind is ticket_factory.ProposalConflictKind.SCOPE_PLAN_STALE
    ]

    assert len(dissent) == 1
    assert dissent[0].field is ticket_factory.TicketSynthesisField.TITLE
    assert split == []
    assert dependency_stale == []
    assert scope_stale == []


def test_approval_record_is_explicit_and_approved(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    approval = report.approval_record

    assert approval.state.value == "approved"
    assert approval.decision.value == "approve"
    assert approval.approved_ticket is not None
    assert approval.approved_ticket.ticket_id == "P16.SP1"


def test_approval_resolves_actual_generated_conflict(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    conflict = report.synthesis_review.conflicts[0]
    resolutions = report.approval_record.conflict_resolutions

    assert len(report.synthesis_review.conflicts) == 1
    assert len(resolutions) == 1
    assert resolutions[0].conflict_id == conflict.conflict_id
    assert (
        resolutions[0].action
        is ticket_factory.ConflictResolutionAction.ACCEPT_CANDIDATE
    )
    assert (
        report.approval_record.canonical_source
        is ticket_factory.CanonicalTicketSource.SYNTHESIZED_CANDIDATE
    )
    assert report.approval_record.state is ticket_factory.TicketApprovalState.APPROVED


def test_approval_conflict_coverage_is_complete(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    conflict_ids = {
        conflict.conflict_id for conflict in report.synthesis_review.conflicts
    }
    resolution_ids = {
        resolution.conflict_id
        for resolution in report.approval_record.conflict_resolutions
    }

    assert resolution_ids == conflict_ids


def test_publication_result_is_logical_publication_only(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    publication = report.publication_result.publication

    assert publication.state.value == "published"
    assert publication.revision == 1
    assert publication.ticket_id == "P16.SP1"
    assert report.publication_result.supersession is None


def test_request_rejects_provider_authority(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["allow_provider_calls"] = True

    with pytest.raises(ValidationError):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_request_rejects_model_authority(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["allow_model_calls"] = True

    with pytest.raises(ValidationError):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_request_rejects_runtime_authority(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["allow_runtime_execution"] = True

    with pytest.raises(ValidationError):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_request_rejects_filesystem_write_authority(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["allow_filesystem_writes"] = True

    with pytest.raises(ValidationError):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_request_rejects_git_mutation_authority(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["allow_git_mutation"] = True

    with pytest.raises(ValidationError):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_request_rejects_duplicate_context_sources(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["context_sources"][1] = data["context_sources"][0]

    with pytest.raises(ValidationError, match="context_sources"):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_request_rejects_duplicate_roles(
    shadow_request: shadow_pilot.TicketFactoryShadowPilotRequest,
) -> None:
    data = shadow_request.model_dump(mode="json")
    data["requested_roles"][1] = data["requested_roles"][0]

    with pytest.raises(ValidationError, match="requested_roles"):
        shadow_pilot.TicketFactoryShadowPilotRequest.model_validate(data)


def test_report_rejects_tampered_report_digest(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    data = report.model_dump(mode="json")
    data["report_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="report_SHA256"):
        shadow_pilot.TicketFactoryShadowPilotReport.model_validate(data)


def test_validate_wrapper_raises_integrity_error_for_tampered_report(
    report: shadow_pilot.TicketFactoryShadowPilotReport,
) -> None:
    tampered = report.model_copy(update={"report_SHA256": "0" * 64})

    with pytest.raises(shadow_pilot.TicketFactoryShadowPilotIntegrityError):
        shadow_pilot.validate_ticket_factory_shadow_pilot_report(tampered)


def test_import_smoke_contract_names_resolve() -> None:
    names = (
        ticket_factory.TicketFactoryShadowPilotRequest.__name__,
        ticket_factory.TicketFactoryShadowPilotReport.__name__,
        ticket_factory.ShadowPilotDisposition.__name__,
        ticket_factory.get_canonical_ticket_factory_shadow_pilot_request.__name__,
        ticket_factory.run_ticket_factory_shadow_pilot.__name__,
    )

    assert names == (
        "TicketFactoryShadowPilotRequest",
        "TicketFactoryShadowPilotReport",
        "ShadowPilotDisposition",
        "get_canonical_ticket_factory_shadow_pilot_request",
        "run_ticket_factory_shadow_pilot",
    )
