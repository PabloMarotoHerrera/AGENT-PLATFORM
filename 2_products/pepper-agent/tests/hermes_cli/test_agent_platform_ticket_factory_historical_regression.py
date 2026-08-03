import hashlib
import json
from collections import Counter

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import ticket_factory
import hermes_cli.agent_platform.ticket_factory.historical_regression as historical_regression


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
P16_7_EXPORTS = (
    "HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION",
    "HISTORICAL_REGRESSION_CORPUS_ID",
    "HISTORICAL_REGRESSION_CORPUS_REVISION",
    "HistoricalRegressionStage",
    "HistoricalRegressionCaseClass",
    "HistoricalProvenanceKind",
    "HistoricalRegressionExpectedOutcome",
    "HistoricalRegressionDriftKind",
    "HistoricalRegressionRunDisposition",
    "HistoricalTicketProvenance",
    "HistoricalRegressionExpectation",
    "HistoricalRegressionCase",
    "HistoricalRegressionCorpus",
    "HistoricalRegressionObservation",
    "HistoricalRegressionDrift",
    "HistoricalRegressionCaseResult",
    "HistoricalRegressionRun",
    "HistoricalRegressionError",
    "HistoricalRegressionCorpusError",
    "HistoricalRegressionExecutionError",
    "get_historical_ticket_regression_corpus",
    "validate_historical_ticket_regression_corpus",
    "run_historical_ticket_regression_case",
    "run_historical_ticket_regression_corpus",
)
UNEXPORTED_DIGEST_CONSTANTS = (
    "CASE_DIGEST_ALGORITHM",
    "CORPUS_DIGEST_ALGORITHM",
    "OUTPUT_DIGEST_ALGORITHM",
    "OBSERVATION_DIGEST_ALGORITHM",
    "CASE_RESULT_DIGEST_ALGORITHM",
    "RUN_DIGEST_ALGORITHM",
)
PUBLIC_MODELS = (
    historical_regression.HistoricalTicketProvenance,
    historical_regression.HistoricalRegressionExpectation,
    historical_regression.HistoricalRegressionCase,
    historical_regression.HistoricalRegressionCorpus,
    historical_regression.HistoricalRegressionObservation,
    historical_regression.HistoricalRegressionDrift,
    historical_regression.HistoricalRegressionCaseResult,
    historical_regression.HistoricalRegressionRun,
)
EXPECTED_ENUM_VALUES = {
    historical_regression.HistoricalRegressionStage: (
        "ticket_spec_validation",
        "dependency_planning",
        "ticket_policy_lint",
        "proposal_synthesis",
        "human_approval",
        "canonical_publication",
    ),
    historical_regression.HistoricalRegressionCaseClass: (
        "accepted",
        "rejected",
        "boundary",
    ),
    historical_regression.HistoricalProvenanceKind: (
        "current_canonical_governance",
        "read_only_git_history",
        "sanitized_synthetic_derivation",
    ),
    historical_regression.HistoricalRegressionExpectedOutcome: (
        "success",
        "error",
    ),
    historical_regression.HistoricalRegressionDriftKind: (
        "unexpected_success",
        "unexpected_error",
        "output_type_mismatch",
        "output_digest_mismatch",
        "exception_type_mismatch",
        "exception_message_mismatch",
    ),
    historical_regression.HistoricalRegressionRunDisposition: (
        "pass",
        "drift_detected",
    ),
}
EXPECTED_CORPUS_SHA256 = (
    "6b949789efafa2fac5d74eb16915aeb8c4c2a2d7123778c777e800f37beda099"
)
EXPECTED_RUN_SHA256 = "86bf357804b482d8a62d7b43ce5070e75723b3ccc19958c510466b3c6506d20d"
EXPECTED_CASES = (
    {
        "case_id": "HIST-001",
        "stage": "ticket_spec_validation",
        "case_class": "accepted",
        "provenance": "current_canonical_governance",
        "source_ticket_id": "P16.0",
        "tags": ("accepted", "ticket-spec", "p16-0"),
        "input_bytes": 1799,
        "input_sha256": "5a3f422b61d4befdcd7e49b3dd33b54eb8994c79d5462ed8741e04cf6caf94f5",
        "case_sha256": "f2d1cdf09a49170dbc3ba724d8d54885b5b790fd8e604c87b55ce7ad1ac59419",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketSpec",
            "output_SHA256": "5a3f422b61d4befdcd7e49b3dd33b54eb8994c79d5462ed8741e04cf6caf94f5",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "1c6dba5b584a5ed31b192e47bf7ff4ffad01577f314ecee721101b3ae88c16ab",
        "result_sha256": "af47bc6de5de4b32fd8bc55d062eefd308fd0bd0fabd5ddbdfc6d157f359cf57",
    },
    {
        "case_id": "HIST-002",
        "stage": "ticket_spec_validation",
        "case_class": "rejected",
        "provenance": "read_only_git_history",
        "source_ticket_id": "P16.0",
        "tags": ("rejected", "ticket-spec", "schema-version"),
        "input_bytes": 1793,
        "input_sha256": "ddba30943de6ad71083d98474eef3608c8cc3cb0c8fc2030390f7907a5d1b1a5",
        "case_sha256": "1d5d3df7058728a1e82da37f65f88a393f0923402c8421b1ace1d33e6c32c38f",
        "expectation": {
            "outcome": "error",
            "output_type": None,
            "output_SHA256": None,
            "exception_type": "ValidationError",
            "exception_message_fragment": "1 validation error for TicketSpec schema_version Input should be 1 [type=literal_error, input_value=2, input_type=int] For further information visit https://err",
        },
        "observation_sha256": "a0181bd42f6862cbac5c26df8bc9925ecf3d54959392cb6555537fdab968f219",
        "result_sha256": "90dd8841ce24d187a98d49e0de95c8ad5a5c734c0c949c03702fa09f291336e3",
    },
    {
        "case_id": "HIST-003",
        "stage": "dependency_planning",
        "case_class": "accepted",
        "provenance": "current_canonical_governance",
        "source_ticket_id": "P16.3",
        "tags": ("accepted", "dependency-plan", "deterministic"),
        "input_bytes": 5007,
        "input_sha256": "35581af1d5bb495aedf0b24630c90972eb72327dd0ab9778c6e9c9cdc028e22a",
        "case_sha256": "6313f4517f92dab5f9cbe06f4d4834e1ba04a594d06c97f677e07107013b7554",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketDependencyPlan",
            "output_SHA256": "3255fb67dd77582174650dab5fdb5d806ff83c5ffda676842a10eb6f79963721",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "6c09315d7a740f8fced7b4fdb3a92737927fc9b168069eb08c86a6d0ca40f74c",
        "result_sha256": "42d529c7e0af918fa1818887d2f08f0cfbe55ae8eba7279cad179cb94287912b",
    },
    {
        "case_id": "HIST-004",
        "stage": "dependency_planning",
        "case_class": "rejected",
        "provenance": "read_only_git_history",
        "source_ticket_id": "P16.3",
        "tags": ("rejected", "dependency-cycle", "hard-prerequisite"),
        "input_bytes": 5148,
        "input_sha256": "835a1ce8aaccd06faa46d8991650b33d4651d74db8a5bbe848d00afccb217950",
        "case_sha256": "d90ad478c269642558bf933621d3ded73797da5ae47e0f201b363e9242557a24",
        "expectation": {
            "outcome": "error",
            "output_type": None,
            "output_SHA256": None,
            "exception_type": "DependencyCycleError",
            "exception_message_fragment": "hard dependency cycle detected: ticket_ids=P16.3 > P16.4",
        },
        "observation_sha256": "accb851f9b2c64620094349b0849390e6949a91b1eca3ca63bf62987dd73adcb",
        "result_sha256": "f75d2cd7a4348d73b8d310b3b88f0ee67fd3ded2fb50aca823a509eda65684e9",
    },
    {
        "case_id": "HIST-005",
        "stage": "ticket_policy_lint",
        "case_class": "accepted",
        "provenance": "current_canonical_governance",
        "source_ticket_id": "P16.4",
        "tags": ("accepted", "policy-lint", "pass-report"),
        "input_bytes": 2997,
        "input_sha256": "516248f991d4487d8a3c5ae94a67cef4b9bb4dd590c3ea48e1fb6b0551ad68d3",
        "case_sha256": "55baecec205728755ec36f5e869b954d0914f1a006ef3f054a0da6efa88c3fe5",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketLintReport",
            "output_SHA256": "a0adfb6696634cdbcd474491776f7d3202d1caa27b1205e21ed4ec950e4f66ea",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "744fa69dc5acd4ad2689c4212eb389cf141676c723ad07a6ba17f44ee428dd5a",
        "result_sha256": "7a024ffb05140f99e505e9edda5bdbc66a4e2e1dad58da2f9e15f9768a1ff5dc",
    },
    {
        "case_id": "HIST-006",
        "stage": "ticket_policy_lint",
        "case_class": "rejected",
        "provenance": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.4",
        "tags": ("rejected", "policy-lint", "blocked-report"),
        "input_bytes": 2805,
        "input_sha256": "ffa448539643fb0c73c40408eeff69ecc86c96327e7329922a2f498f18e8a19a",
        "case_sha256": "82f938efce2d7262ad655b2bd08c6338904fdc3695b2d15c40edb4d30b4e4740",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketLintReport",
            "output_SHA256": "9f590329a1b96e639ed92c403a0c844ad7564fc596a805ce69c8746f0062cbc2",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "2f4de90071a9c4b028afe8268e383188b8e1f73a0719251bb1a952a8ce858857",
        "result_sha256": "b4c6c3d6fcd984f5b865ea5415e485dc4515ff70eab33bd32635acca6d0ba331",
    },
    {
        "case_id": "HIST-007",
        "stage": "proposal_synthesis",
        "case_class": "accepted",
        "provenance": "current_canonical_governance",
        "source_ticket_id": "P16.5",
        "tags": ("accepted", "synthesis", "unanimous"),
        "input_bytes": 16384,
        "input_sha256": "04be34b0b5a252c22f5619c05aa520ea6ea10614b3bf0d827224123df1da2774",
        "case_sha256": "0378cdaf18b2ccb89af59aa4b135deb56d82b86ed1ec8f851ac7b70c51dbf220",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketSynthesisReview",
            "output_SHA256": "e4e827948d8877acca346ebf9ada08eeb710470c810733c94932ce70083be378",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "48c69b7e899bb768e317f8f3cd9bc252e2020c8de327c5d697391570417d6da9",
        "result_sha256": "00ae79ecc7ad0c8822598f3e66124b2926da9fdd3e857649b8b2e8b028feddd3",
    },
    {
        "case_id": "HIST-008",
        "stage": "proposal_synthesis",
        "case_class": "boundary",
        "provenance": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.5",
        "tags": ("boundary", "synthesis", "split-field"),
        "input_bytes": 16391,
        "input_sha256": "5d6281e682ba54df17565d98b3306d46b6781a32a71058ac8908f7c6fb1a9223",
        "case_sha256": "9e93f2aaa0cb63391625e7b68460531b9b8568bc14b8e5254837bb2bf8ec631b",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketSynthesisReview",
            "output_SHA256": "f0a4849862f10692abb0a031c8bd74d5309a25240f5b99f117be037429ed3fe0",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "7a9391c10063cf2194e9529b5c655bb615a4d65c6afd8f0e88a1f8a0f54371b0",
        "result_sha256": "87336074b7db07f14ee210bc1a607919792be6fb56a140fb24418c32f546c7db",
    },
    {
        "case_id": "HIST-009",
        "stage": "human_approval",
        "case_class": "accepted",
        "provenance": "current_canonical_governance",
        "source_ticket_id": "P16.6",
        "tags": ("accepted", "human-approval", "approve"),
        "input_bytes": 27512,
        "input_sha256": "0c21a504eb3fb0f628ffccf25a6508b8edc145ce0ee9717b02e3d5ade4c6d260",
        "case_sha256": "fd1177310d20441de95f2366f007b7c922863b3cd9a6d48cd7f744228345dcd5",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketApprovalRecord",
            "output_SHA256": "de58a99212656d87e15b4471a95b3b8213b03f70a8912d390a606f39684d7346",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "a291db2188efd0a32f67c44982b43286996f45f3777286e4030798fd514d8856",
        "result_sha256": "8f8ffa2eec82a75f54256d9c14d2a0a99bb6eab13ba800264170e005ce0b80c7",
    },
    {
        "case_id": "HIST-010",
        "stage": "human_approval",
        "case_class": "rejected",
        "provenance": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.6",
        "tags": ("rejected", "human-approval", "conflict-resolution"),
        "input_bytes": 28269,
        "input_sha256": "4102e23866d97fa14d186653ded6fb20551f0ab55daed61fed4cfea0fa356a39",
        "case_sha256": "db4f15bb8d606dc50200f2579d1b71e65a5668c03b393ceac437ef5ee3906af6",
        "expectation": {
            "outcome": "error",
            "output_type": None,
            "output_SHA256": None,
            "exception_type": "TicketApprovalInputError",
            "exception_message_fragment": "approval requires exactly one resolution per conflict",
        },
        "observation_sha256": "aff04eede6c5a863b76944c71d96311a2cddab1a29a358619fa29414eeba0a22",
        "result_sha256": "7b963582c634dba9f391eae00a8fe0cb54a3837f98fe2e417a4d0f13c78ae0b6",
    },
    {
        "case_id": "HIST-011",
        "stage": "canonical_publication",
        "case_class": "accepted",
        "provenance": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.6",
        "tags": ("accepted", "canonical-publication", "first-revision"),
        "input_bytes": 3304,
        "input_sha256": "bdc97b45c6c31a363de9a9a95b865c25898c5fbe99009b2ad52fbd4e821d7993",
        "case_sha256": "a239c1d9458f8eeca6d89464f0fe1ffb9cd0cad5266cc27b3364ac7e0b6f4371",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketPublicationResult",
            "output_SHA256": "1d6d1497380652858155dbb7b9ac52abf84f725b3bb410d3b791fe21e775124f",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "db1b4871927eb1296fc06467948c579b87bd8a73feccbe375fd7dcc4c0d53ec3",
        "result_sha256": "b421524a72624d0a6923cb5daf6ac2e516a0c44bb138103f52020a726be7bde6",
    },
    {
        "case_id": "HIST-012",
        "stage": "canonical_publication",
        "case_class": "boundary",
        "provenance": "sanitized_synthetic_derivation",
        "source_ticket_id": "P16.6",
        "tags": ("boundary", "canonical-publication", "supersession"),
        "input_bytes": 7552,
        "input_sha256": "b13ac7cc7716ef071e64013e28a0de1910ce2ff0a872fc0257c42c2fd58c4f7c",
        "case_sha256": "4ccfaaba58ca0e356accbed97180937115a7727854bf2cbec615d9c1f46e4983",
        "expectation": {
            "outcome": "success",
            "output_type": "TicketPublicationResult",
            "output_SHA256": "4da6c4af7eec5bac43d77103304abcaaf91d6d3d2138f7cb099d8b73fa87bf52",
            "exception_type": None,
            "exception_message_fragment": None,
        },
        "observation_sha256": "eebdbbb939c54e2c1087e8a4cdef9bcdc81f36b4a111040a50dff73850b7a58c",
        "result_sha256": "7072fa6a20a6cc1290627cf89ba87e763cba8f483294d6a485e018bc325f9acd",
    },
)
EXPECTED_BY_ID = {item["case_id"]: item for item in EXPECTED_CASES}


@pytest.fixture(scope="module")
def corpus() -> historical_regression.HistoricalRegressionCorpus:
    return historical_regression.get_historical_ticket_regression_corpus()


@pytest.fixture(scope="module")
def regression_run(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> historical_regression.HistoricalRegressionRun:
    return historical_regression.run_historical_ticket_regression_corpus(corpus)


@pytest.fixture(scope="module")
def case_by_id(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> dict[str, historical_regression.HistoricalRegressionCase]:
    return {case.case_id: case for case in corpus.cases}


@pytest.fixture(scope="module")
def result_by_id(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> dict[str, historical_regression.HistoricalRegressionCaseResult]:
    return {result.case_id: result for result in regression_run.case_results}


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@pytest.mark.parametrize("export_name", P16_7_EXPORTS)
def test_p16_7_root_exports_resolve_to_module(export_name: str) -> None:
    root_value = getattr(ticket_factory, export_name)
    module_value = getattr(historical_regression, export_name)

    assert export_name in ticket_factory.__all__
    if isinstance(module_value, int | str):
        assert root_value == module_value
    else:
        assert root_value is module_value


def test_p16_7_root_exports_preserve_p16_4_final_block() -> None:
    assert ticket_factory.__all__[-len(P16_4_FINAL_EXPORTS) :] == P16_4_FINAL_EXPORTS


def test_p16_7_root_exports_are_inserted_before_p16_4_final_block() -> None:
    first_p16_7_index = ticket_factory.__all__.index(P16_7_EXPORTS[0])
    first_p16_4_index = ticket_factory.__all__.index(P16_4_FINAL_EXPORTS[0])

    assert first_p16_7_index < first_p16_4_index


@pytest.mark.parametrize("constant_name", UNEXPORTED_DIGEST_CONSTANTS)
def test_digest_algorithm_constants_are_not_root_exports(constant_name: str) -> None:
    assert hasattr(historical_regression, constant_name)
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


def test_corpus_identity_constants() -> None:
    assert historical_regression.HISTORICAL_REGRESSION_CORPUS_SCHEMA_VERSION == 1
    assert (
        historical_regression.HISTORICAL_REGRESSION_CORPUS_ID
        == "pepper-ticket-factory-historical-regression-v1"
    )
    assert historical_regression.HISTORICAL_REGRESSION_CORPUS_REVISION == 1


def test_corpus_has_frozen_identity(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    assert corpus.schema_version == 1
    assert corpus.corpus_id == "pepper-ticket-factory-historical-regression-v1"
    assert corpus.revision == 1
    assert corpus.corpus_SHA256 == EXPECTED_CORPUS_SHA256


def test_corpus_has_exact_case_count(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    assert len(corpus.cases) == 12


def test_corpus_case_order_is_frozen(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    assert tuple(case.case_id for case in corpus.cases) == tuple(
        item["case_id"] for item in EXPECTED_CASES
    )


def test_corpus_validates_without_recomputing_from_observations(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    assert (
        historical_regression.validate_historical_ticket_regression_corpus(corpus)
        is None
    )


def test_corpus_json_round_trips(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    round_tripped = (
        historical_regression.HistoricalRegressionCorpus.model_validate_json(
            corpus.model_dump_json()
        )
    )

    assert round_tripped == corpus


def test_corpus_stage_composition(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    stage_counts = Counter(case.stage.value for case in corpus.cases)

    assert stage_counts == {
        "ticket_spec_validation": 2,
        "dependency_planning": 2,
        "ticket_policy_lint": 2,
        "proposal_synthesis": 2,
        "human_approval": 2,
        "canonical_publication": 2,
    }


def test_corpus_class_composition(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    class_counts = Counter(case.case_class.value for case in corpus.cases)

    assert class_counts == {"accepted": 6, "rejected": 4, "boundary": 2}


def test_corpus_provenance_composition(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    provenance_counts = Counter(case.provenance.kind.value for case in corpus.cases)

    assert provenance_counts == {
        "current_canonical_governance": 5,
        "read_only_git_history": 2,
        "sanitized_synthetic_derivation": 5,
    }


def test_corpus_case_names_are_unique(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    case_names = tuple(case.name for case in corpus.cases)

    assert len(case_names) == len(frozenset(case_names))


def test_corpus_case_digests_are_unique(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    case_digests = tuple(case.case_SHA256 for case in corpus.cases)

    assert len(case_digests) == len(frozenset(case_digests))


def test_corpus_result_is_pass(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    assert (
        regression_run.disposition
        is historical_regression.HistoricalRegressionRunDisposition.PASS
    )
    assert regression_run.run_SHA256 == EXPECTED_RUN_SHA256
    assert regression_run.drifted_case_ids == ()


def test_corpus_result_covers_all_cases(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    assert regression_run.passed_case_ids == tuple(
        item["case_id"] for item in EXPECTED_CASES
    )
    assert tuple(result.case_id for result in regression_run.case_results) == tuple(
        item["case_id"] for item in EXPECTED_CASES
    )


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_stage_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.stage.value == expected["stage"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_class_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.case_class.value == expected["case_class"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_provenance_kind_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.provenance.kind.value == expected["provenance"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_source_ticket_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.provenance.source_ticket_id == expected["source_ticket_id"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_tags_are_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.tags == expected["tags"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_input_size_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert len(case.input_JSON.encode("utf-8")) == expected["input_bytes"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_input_digest_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert sha256_text(case.input_JSON) == expected["input_sha256"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_digest_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.case_SHA256 == expected["case_sha256"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_expectation_is_frozen(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.expectation.model_dump(mode="json") == expected["expectation"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_input_is_canonical_json(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]
    parsed = json.loads(case.input_JSON)

    assert canonical_json(parsed) == case.input_JSON


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_input_is_sanitized(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]
    lowered = case.input_JSON.casefold()

    assert "c:\\users\\" not in lowered
    assert "/home/" not in lowered
    assert "sk-" not in lowered
    assert "bearer " not in lowered
    assert "private key" not in lowered
    assert "prompt dump" not in lowered
    assert "reasoning trace" not in lowered


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_provenance_sanitized_rule(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert case.provenance.sanitized is True
    assert "raw historical document content" in case.provenance.rationale


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_git_commit_provenance_rule(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    if expected["provenance"] == "read_only_git_history":
        assert (
            case.provenance.source_commit_SHA
            == "3245b93074fd2218cb9f98ba3d25e53cf9bfbec1"
        )
    else:
        assert case.provenance.source_commit_SHA is None


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_round_trips_through_model_validation(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]

    assert (
        historical_regression.HistoricalRegressionCase.model_validate(
            case.model_dump(mode="json")
        )
        == case
    )


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_rejects_tampered_digest(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]
    data = case.model_dump(mode="json")
    data["case_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="case_SHA256"):
        historical_regression.HistoricalRegressionCase.model_validate(data)


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_execution_matches_frozen_expectation(
    expected: dict[str, object],
    case_by_id: dict[str, historical_regression.HistoricalRegressionCase],
) -> None:
    case = case_by_id[str(expected["case_id"])]
    result = historical_regression.run_historical_ticket_regression_case(case)

    assert result.matched is True
    assert result.drifts == ()
    assert result.observation.outcome.value == expected["expectation"]["outcome"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_observation_digest_is_frozen(
    expected: dict[str, object],
    result_by_id: dict[str, historical_regression.HistoricalRegressionCaseResult],
) -> None:
    result = result_by_id[str(expected["case_id"])]

    assert result.observation.observation_SHA256 == expected["observation_sha256"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_result_digest_is_frozen(
    expected: dict[str, object],
    result_by_id: dict[str, historical_regression.HistoricalRegressionCaseResult],
) -> None:
    result = result_by_id[str(expected["case_id"])]

    assert result.result_SHA256 == expected["result_sha256"]


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_result_round_trips_through_model_validation(
    expected: dict[str, object],
    result_by_id: dict[str, historical_regression.HistoricalRegressionCaseResult],
) -> None:
    result = result_by_id[str(expected["case_id"])]

    assert (
        historical_regression.HistoricalRegressionCaseResult.model_validate(
            result.model_dump(mode="json")
        )
        == result
    )


@pytest.mark.parametrize(
    "expected", EXPECTED_CASES, ids=[item["case_id"] for item in EXPECTED_CASES]
)
def test_case_success_or_error_fields_are_partitioned(
    expected: dict[str, object],
    result_by_id: dict[str, historical_regression.HistoricalRegressionCaseResult],
) -> None:
    result = result_by_id[str(expected["case_id"])]
    observation = result.observation

    if expected["expectation"]["outcome"] == "success":
        assert observation.output_type == expected["expectation"]["output_type"]
        assert observation.output_SHA256 == expected["expectation"]["output_SHA256"]
        assert observation.exception_type is None
        assert observation.exception_message is None
    else:
        assert observation.output_type is None
        assert observation.output_SHA256 is None
        assert observation.exception_type == expected["expectation"]["exception_type"]
        assert (
            expected["expectation"]["exception_message_fragment"]
            in observation.exception_message
        )


def test_validate_rejects_duplicate_case_ids(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    data = corpus.model_dump(mode="json")
    data["cases"][1] = data["cases"][0]

    with pytest.raises(ValidationError, match="duplicate"):
        historical_regression.HistoricalRegressionCorpus.model_validate(data)


def test_validate_rejects_tampered_corpus_digest(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    data = corpus.model_dump(mode="json")
    data["corpus_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="corpus_SHA256"):
        historical_regression.HistoricalRegressionCorpus.model_validate(data)


def test_validate_wrapper_raises_corpus_error_for_tampered_corpus(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    tampered = historical_regression.HistoricalRegressionCorpus.model_construct(
        schema_version=corpus.schema_version,
        corpus_id=corpus.corpus_id,
        revision=corpus.revision,
        cases=corpus.cases,
        corpus_SHA256="0" * 64,
    )

    with pytest.raises(historical_regression.HistoricalRegressionCorpusError):
        historical_regression.validate_historical_ticket_regression_corpus(tampered)


def test_run_rejects_tampered_corpus_before_execution(
    corpus: historical_regression.HistoricalRegressionCorpus,
) -> None:
    tampered = historical_regression.HistoricalRegressionCorpus.model_construct(
        schema_version=corpus.schema_version,
        corpus_id=corpus.corpus_id,
        revision=corpus.revision,
        cases=corpus.cases,
        corpus_SHA256="0" * 64,
    )

    with pytest.raises(historical_regression.HistoricalRegressionCorpusError):
        historical_regression.run_historical_ticket_regression_corpus(tampered)


def test_run_result_json_round_trips(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    assert (
        historical_regression.HistoricalRegressionRun.model_validate_json(
            regression_run.model_dump_json()
        )
        == regression_run
    )


def test_run_result_rejects_tampered_digest(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    data = regression_run.model_dump(mode="json")
    data["run_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="run_SHA256"):
        historical_regression.HistoricalRegressionRun.model_validate(data)


def test_run_result_rejects_inconsistent_disposition(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    data = regression_run.model_dump(mode="json")
    data["disposition"] = "drift_detected"

    with pytest.raises(ValidationError, match="disposition"):
        historical_regression.HistoricalRegressionRun.model_validate(data)


def test_observation_rejects_tampered_digest(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    data = regression_run.case_results[0].observation.model_dump(mode="json")
    data["observation_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="observation_SHA256"):
        historical_regression.HistoricalRegressionObservation.model_validate(data)


def test_case_result_rejects_tampered_digest(
    regression_run: historical_regression.HistoricalRegressionRun,
) -> None:
    data = regression_run.case_results[0].model_dump(mode="json")
    data["result_SHA256"] = "0" * 64

    with pytest.raises(ValidationError, match="result_SHA256"):
        historical_regression.HistoricalRegressionCaseResult.model_validate(data)
