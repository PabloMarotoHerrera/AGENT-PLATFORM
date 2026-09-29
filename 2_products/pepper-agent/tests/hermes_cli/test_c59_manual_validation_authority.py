"""Human validation is separate from terminal execution, zero-change and review."""

import json

import pytest

from hermes_cli.agent_platform import manual_validation as mv
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)
from tools import pepper_workflow_tools as tools


@pytest.fixture
def terminal(projection_home, monkeypatch):
    fixture = fixtures._c18_v2_synthetic_noop_review_ready_fixture(
        monkeypatch,
        ticket_id="P99.174",
        completion_mutator=fixtures._c19_legacy_semantic_noop_mutator,
    )
    fixture.contract["validation_steps"] = []
    fixture.contract["work_packet_validation_steps"] = [
        {
            "validation_id": "V1",
            "kind": "manual",
            "required": True,
            "command": None,
            "command_execution_authorized": False,
            "description": "Confirm the architecture meets the approved product scope.",
            "expected_result": "Every approved product boundary is represented.",
        }
    ]
    fixture.contract["criteria_revision_SHA256"] = fixture.pr._criteria_revision_digest(
        fixture.contract
    )
    fixture.contract["acceptance_contract_SHA256"] = (
        fixture.pr._acceptance_contract_digest(fixture.contract)
    )
    return fixture


def _args(fixture, status="passed"):
    context = fixture.pr.inspect_current_ticket_manual_validation()
    item = context["items"][0]
    return {
        "ticket_id": fixture.ticket_id,
        "work_packet_id": context["work_packet_id"],
        "work_packet_sha256": context["work_packet_SHA256"],
        "run_id": context["run_id"],
        "validation_id": item["validation_id"],
        "validation_contract_sha256": context["validation_contract_SHA256"],
        "binding_sha256": item["binding_SHA256"],
        "next_action_id": context["next_action_id"],
        "status": status,
        "human_attestation_text": item["required_attestation_text"][status],
        "evidence": "I inspected the approved product boundaries and verified each listed requirement.",
    }


def test_c59_manual_noop_sequence_and_public_reads(terminal):
    pr = terminal.pr
    zero = fixtures._record_c19_zero_change_attestation(terminal)
    assert zero["zero_change_result"] is True
    zero_path = pr.zero_change_attestation_record_path_for_ticket(terminal.ticket_id)
    zero_bytes = zero_path.read_bytes()
    completion_before = json.dumps(terminal.completion, sort_keys=True)
    assert not pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == pr._manual_validation_action_id(
        terminal.ticket_id
    )
    for reader in (
        tools._get_workflow_control,
        tools._get_review_status,
        tools._get_next_action,
    ):
        result = json.loads(reader({}))
        assert result["manual_validation"]["items"][0]["status"] == "pending"
        assert result["next_action"]["id"] == workflow["next_action"]["id"]
    inspection = json.loads(tools._inspect_current_ticket_manual_validation({}))
    assert inspection["success"] is True
    assert (
        inspection["manual_validation"]["items"][0]["description"]
        == terminal.contract["work_packet_validation_steps"][0]["description"]
    )
    blocked = pr.prepare_current_ticket_review()
    assert blocked["review_preparation_recorded"] is False
    args = _args(terminal)
    result = json.loads(tools._attest_current_ticket_manual_validation(args))
    assert result["success"] is True, result
    assert result["manual_validation"]["validation_contract_satisfied"] is True
    assert result["manual_validation"]["validated_noop_result"] is True
    assert result["manual_validation"]["reviewable_result"] is True
    assert result["review_preparation_recorded"] is False
    assert zero_path.read_bytes() == zero_bytes
    assert json.dumps(terminal.completion, sort_keys=True) == completion_before
    replay = pr.attest_current_ticket_manual_validation(**args)
    assert replay["idempotent_replay"] is True
    assert replay["evidence_SHA256"] == result["evidence_SHA256"]
    workflow = pr.build_workflow_control_snapshot()
    assert (
        workflow["next_action"]["id"]
        == pr.governed_ticket_lifecycle_action_ids(terminal.ticket_id)["review_prepare"]
    )
    prepared = pr.prepare_current_ticket_review()
    assert prepared["review_preparation_recorded"] is True, prepared
    assert prepared["validated_noop_result"] is True
    assert not pr.review_decision_record_path_for_ticket(terminal.ticket_id).exists()


def test_c59_failed_evidence_blocks_review_and_conflicting_replay(terminal):
    fixtures._record_c19_zero_change_attestation(terminal)
    pr = terminal.pr
    args = _args(terminal, "failed")
    result = pr.attest_current_ticket_manual_validation(**args)
    assert result["status"] == "failed"
    assert not result["manual_validation"]["validation_contract_satisfied"]
    assert (
        pr.build_workflow_control_snapshot()["workflow_status"]
        == "blocked_manual_validation_failed"
    )
    assert pr.prepare_current_ticket_review()["review_preparation_recorded"] is False
    with pytest.raises(ValueError, match="conflicting"):
        pr.attest_current_ticket_manual_validation(**_args(terminal))


@pytest.mark.parametrize(
    "field,value",
    [
        ("ticket_id", "P99.999"),
        ("work_packet_id", "wrong"),
        ("work_packet_sha256", "f" * 64),
        ("run_id", 999),
        ("validation_id", "V2"),
        ("validation_contract_sha256", "f" * 64),
        ("binding_sha256", "f" * 64),
        ("next_action_id", "PREPARE_REVIEW"),
        ("human_attestation_text", "looks good"),
        ("evidence", ""),
        ("status", "pending"),
    ],
)
def test_c59_mismatched_request_cannot_persist(terminal, field, value):
    fixtures._record_c19_zero_change_attestation(terminal)
    args = _args(terminal)
    args[field] = value
    result = json.loads(tools._attest_current_ticket_manual_validation(args))
    assert result["success"] is False
    assert (
        terminal.pr.inspect_current_ticket_manual_validation()["items"][0]["status"]
        == "pending"
    )


def test_c59_zero_change_cannot_substitute_for_validation(terminal):
    with pytest.raises(Exception, match="zero-change|candidate"):
        terminal.pr.inspect_current_ticket_manual_validation()
    fixtures._record_c19_zero_change_attestation(terminal)
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )
    assert (
        terminal.pr.inspect_current_ticket_manual_validation()["items"][0][
            "evidence_SHA256"
        ]
        is None
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "contract",
        "ticket_revision",
        "work_packet_revision",
        "run",
        "other_ticket",
        "description",
        "expected_result",
    ],
)
def test_c59_stale_evidence_never_satisfies_new_authority(terminal, mutation):
    fixtures._record_c19_zero_change_attestation(terminal)
    args = _args(terminal)
    terminal.pr.attest_current_ticket_manual_validation(**args)
    original = terminal.pr.inspect_current_ticket_manual_validation()["items"][0]
    path = mv.record_path(original["binding"])
    before = path.read_bytes()
    if mutation == "contract":
        terminal.contract["acceptance_criteria"].append("New required boundary")
    elif mutation == "ticket_revision":
        terminal.contract["ticket_spec_SHA256"] = "f" * 64
    elif mutation == "work_packet_revision":
        terminal.contract["work_packet_SHA256"] = "f" * 64
    elif mutation == "run":
        terminal.completion["run_id"] += 1
    elif mutation == "other_ticket":
        terminal.contract["ticket_id"] = "P99.999"
    else:
        terminal.contract["work_packet_validation_steps"][0][mutation] = (
            "Changed contract wording"
        )
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )
    result = json.loads(tools._attest_current_ticket_manual_validation(args))
    assert result["success"] is False
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "field,value",
    [("required", False), ("kind", "command"), ("command_execution_authorized", True)],
)
def test_c59_nonrequired_or_nonmanual_item_cannot_be_attested(terminal, field, value):
    fixtures._record_c19_zero_change_attestation(terminal)
    args = _args(terminal)
    terminal.contract["work_packet_validation_steps"][0][field] = value
    result = json.loads(tools._attest_current_ticket_manual_validation(args))
    assert result["success"] is False


@pytest.mark.parametrize("mutation", ["digest", "binding", "zero_change_record"])
def test_c59_invalid_persisted_evidence_fails_closed(terminal, mutation):
    zero = fixtures._record_c19_zero_change_attestation(terminal)
    args = _args(terminal)
    terminal.pr.attest_current_ticket_manual_validation(**args)
    item = terminal.pr.inspect_current_ticket_manual_validation()["items"][0]
    path = mv.record_path(item["binding"])
    record = json.loads(path.read_text())
    if mutation == "digest":
        record["evidence"] = "tampered"
    elif mutation == "binding":
        record["binding"]["run_id"] += 1
        record["evidence_SHA256"] = mv.digest({
            k: v for k, v in record.items() if k != "evidence_SHA256"
        })
    else:
        record = zero
    path.write_text(json.dumps(record), encoding="utf-8")
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )
    workflow = terminal.pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "blocked_invalid_manual_validation_authority"
    assert (
        terminal.pr.prepare_current_ticket_review()["review_preparation_recorded"]
        is False
    )


def test_c59_multiple_manual_items_and_command_gate_remain_required(terminal):
    second = dict(
        terminal.contract["work_packet_validation_steps"][0], validation_id="V2"
    )
    terminal.contract["work_packet_validation_steps"].append(second)
    fixtures._record_c19_zero_change_attestation(terminal)
    terminal.pr.attest_current_ticket_manual_validation(**_args(terminal))
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )
    context = terminal.pr.inspect_current_ticket_manual_validation()
    item = context["items"][1]
    args = _args(terminal)
    args.update(
        validation_id="V2",
        binding_sha256=item["binding_SHA256"],
        human_attestation_text=item["required_attestation_text"]["passed"],
    )
    terminal.pr.attest_current_ticket_manual_validation(**args)
    assert terminal.pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )
    # A command requirement cannot be satisfied by human evidence for manual items.
    terminal.contract["work_packet_validation_steps"].append({
        "validation_id": "V3",
        "kind": "command",
        "command": "python -m pytest",
        "required": True,
    })
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        terminal.completion, terminal.contract
    )


def test_c59_candidate_changes_use_the_same_manual_boundary(terminal, tmp_path):
    completion = terminal.completion
    terminal.projection_record.update(
        assignee_profile="implementation_product",
        selected_profile="implementation_product",
    )
    candidate = fixtures._c13_review_round_completion(
        terminal.pr,
        terminal.projection_record,
        tmp_path,
        run_id=completion["run_id"],
        label="manual-candidate",
    )
    completion.update(
        terminal_outcome_class="validated_review_required",
        candidate_changes_available=True,
        candidate_changes_reference=candidate.completion["candidate_changes_reference"],
        source_materialization_reference=candidate.completion[
            "source_materialization_reference"
        ],
        reported_files_modified=[candidate.candidate_path],
    )
    completion["kanban_completion_result_SHA256"] = (
        terminal.pr._kanban_completion_result_digest(completion)
    )
    fixtures._install_c19_current_terminal_run_authority(
        terminal.projection_record, completion
    )
    context = terminal.pr.inspect_current_ticket_manual_validation()
    assert context["zero_change_result"] is False
    assert not context["reviewable_result"]
    result = terminal.pr.attest_current_ticket_manual_validation(**_args(terminal))
    assert result["manual_validation"]["reviewable_result"] is True
    assert result["manual_validation"]["validated_noop_result"] is False
    assert terminal.pr._review_prepare_reviewable_result(completion, terminal.contract)


def test_c59_read_execution_surface_never_attests(terminal):
    fixtures._record_c19_zero_change_attestation(terminal)
    context = terminal.pr.inspect_current_ticket_manual_validation()
    path = mv.record_path(context["items"][0]["binding"])
    for _ in range(2):
        result = json.loads(tools._get_execution_status({}))
        assert result["manual_validation"]["items"][0]["status"] == "pending"
    assert not path.exists()


def test_c59_required_manual_validation_has_reachable_boundary(terminal):
    fixtures._record_c19_zero_change_attestation(terminal)
    workflow = terminal.pr.build_workflow_control_snapshot()
    blocked = terminal.pr.prepare_current_ticket_review()
    assert (
        workflow["next_action"]["id"],
        blocked["blocker_code"],
        blocked["review_preparation_recorded"],
    ) == (
        "ATTEST_P99_174_MANUAL_VALIDATION",
        "MANUAL_VALIDATION_REQUIRED",
        False,
    )


def test_c59_successful_evidence_is_immutable_and_registry_tools_are_available(
    terminal,
):
    from model_tools import handle_function_call

    fixtures._record_c19_zero_change_attestation(terminal)
    inspected = json.loads(
        handle_function_call("inspect_current_ticket_manual_validation", {})
    )
    assert inspected["success"] is True
    args = _args(terminal)
    result = json.loads(
        handle_function_call("attest_current_ticket_manual_validation", args)
    )
    assert result["success"] is True
    item = terminal.pr.inspect_current_ticket_manual_validation()["items"][0]
    path = mv.record_path(item["binding"])
    before = path.read_bytes()
    args["evidence"] = "Different human evidence must not overwrite the original."
    conflict = json.loads(
        handle_function_call("attest_current_ticket_manual_validation", args)
    )
    assert conflict["success"] is False
    assert path.read_bytes() == before
    for flag in (
        "ticket_execution_authorized",
        "WorkPacket_execution_authorized",
        "runtime_execution_authorized",
        "worker_execution",
        "Kanban_dispatch",
        "Git_mutation",
        "review_preparation_recorded",
        "review_decision_recorded",
    ):
        assert result[flag] is False


@pytest.mark.parametrize(
    "failure",
    ["validation_infrastructure_failure", "validation_passed", "validation_complete"],
)
def test_c59_manual_evidence_does_not_clear_existing_failure_flags(terminal, failure):
    fixtures._record_c19_zero_change_attestation(terminal)
    terminal.pr.attest_current_ticket_manual_validation(**_args(terminal))
    # Preserve the source identity while checking that the predicate still
    # honors explicit failure observations in a validation-enriched result.
    completion = dict(terminal.completion)
    completion["run_metadata"] = dict(completion["run_metadata"])
    completion["run_metadata"][failure] = failure == "validation_infrastructure_failure"
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        completion, terminal.contract
    )


def test_c59_mixed_contract_preserves_manual_binding_after_command_validation(terminal):
    terminal.contract["work_packet_validation_steps"].append({
        "validation_id": "V2",
        "kind": "command",
        "required": True,
        "command": "python -m pytest",
        "expected_exit_codes": [0],
    })
    fixtures._record_c19_zero_change_attestation(terminal)
    result = terminal.pr.attest_current_ticket_manual_validation(**_args(terminal))
    assert result["manual_validation"]["items"][0]["status"] == "passed"
    assert result["manual_validation"]["validation_contract_satisfied"] is False
    validation = {
        "validation_command_results": fixtures._successful_contract_validation_results(
            terminal.contract
        ),
        "validation_passed": True,
        "validation_complete": True,
        "validation_executed": True,
    }
    enriched = terminal.pr._review_completion_with_prepare_validation_results(
        terminal.completion, validation=validation
    )
    assert terminal.pr._review_completion_validation_contract_satisfied(
        enriched, terminal.contract
    )
    enriched["candidate_changes_reference"] = {"candidate_SHA256": "f" * 64}
    assert not terminal.pr._review_completion_validation_contract_satisfied(
        enriched, terminal.contract
    )
