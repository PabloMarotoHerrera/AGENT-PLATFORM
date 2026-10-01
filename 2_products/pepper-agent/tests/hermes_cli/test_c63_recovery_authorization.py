"""C63: recovery consent remains distinct from execution consent."""

import pytest
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.workflow import retry_incident_rollback as recovery
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)

TICKET = "P999.12"
BASE = "I explicitly authorize the governed recovery action RECOVER_P999_12_EXECUTION for ticket P999.12, run 34."


@pytest.mark.parametrize(
    "suffix",
    [
        "",
        " Recovery only.",
        " Do not retry.",
        " Do not start a retry or a new execution as part of this action.",
        " Do not start another run.",
        " Do not rerun.",
        " Do not authorize retry.",
        " Do not retry or start a new execution.",
        " No reintentar.",
    ],
)
def test_explicit_recovery_with_prohibitions(suffix):
    assert (
        pr.execution_recovery_authorization_text_diagnostics(
            BASE + suffix, current_ticket_id=TICKET, current_run_id=34
        )
        is None
    )


@pytest.mark.parametrize(
    "text",
    [
        "Retry P999.12 run 34 and start the next execution.",
        "Inspect recovery for P999.12.",
        "Recovery for P999.12.",
        "Do not authorize recovery for P999.12.",
        "I do not authorize recovery for P999.12.",
        "Maybe I authorize recovery for P999.12.",
        BASE + " Retry now.",
        BASE + " I authorize a rerun.",
        BASE + " Start a new execution.",
        BASE + " Start another run.",
        BASE + " Do not retry, but start a new execution.",
        BASE + " Do not retry and start a new execution.",
        BASE + " I do not authorize recovery.",
        BASE + " I authorize execution.",
        BASE + " Execute now.",
        BASE + " Dispatch the worker.",
    ],
)
def test_nonconsent_or_execution_consent_fails_closed(text):
    assert (
        pr.execution_recovery_authorization_text_diagnostics(
            text, current_ticket_id=TICKET, current_run_id=34
        )
        is not None
    )


@pytest.mark.parametrize(
    "text",
    [
        BASE.replace("P999.12", "P999.13"),
        BASE.replace("run 34", "run 35"),
        BASE.replace("RECOVER_P999_12_EXECUTION", "RECOVER_P999_13_EXECUTION"),
        BASE + " for P999.13",
        BASE + " run 35",
    ],
)
def test_wrong_ticket_run_or_action_rejected(text):
    assert (
        pr.execution_recovery_authorization_text_diagnostics(
            text, current_ticket_id=TICKET, current_run_id=34
        )
        is not None
    )


@pytest.mark.parametrize("ticket", ["P18.9.0", "P18.9.1", TICKET])
def test_existing_canonical_recovery_phrase(ticket):
    assert (
        pr.execution_recovery_authorization_text_diagnostics(
            pr.governed_ticket_recovery_authorization_text(ticket),
            current_ticket_id=ticket,
        )
        is None
    )


@pytest.mark.parametrize(
    "identifier",
    [
        "a" * 64,
        "P18.9.12",
        "run 34",
        "RECOVER_P18_9_12_EXECUTION",
        "WP-P18-9-12-R0002-17ac7b18753f",
    ],
)
def test_governance_identifiers_are_not_credentials(identifier):
    text = BASE + " " + identifier
    assert recovery._validate_safe_text(text, "authorization_reference") == text


@pytest.mark.parametrize(
    "secret",
    [
        "authorization: bearer example",
        "access_token=example",
        "sk-" + "x" * 24,
        "password=example",
    ],
)
def test_credential_guard_unchanged(secret):
    with pytest.raises(ValueError, match="credential-shaped"):
        recovery._validate_safe_text(BASE + " " + secret, "authorization_reference")


@pytest.mark.parametrize("wrong_run", [False, True])
def test_real_recovery_records_no_retry_or_new_run(
    projection_home, monkeypatch, wrong_run
):
    from hermes_cli import kanban_db

    fixtures._install_execution_profile(monkeypatch, projection_home)
    fixtures._approve_current_ticket()
    projected = fixtures._project_via_runtime()
    run_id = fixtures._force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    text = f"I authorize governed recovery for P18.9.0 run {run_id + int(wrong_run)}. Recovery only. Do not start a retry or new execution."
    path = pr.recovery_action_record_path_for_ticket("P18.9.0")
    if wrong_run:
        with pytest.raises(pr.ProductRuntimeDecisionFailed, match="different run"):
            pr.recover_current_ticket_execution(
                human_authorization_text=text, ticket_id="P18.9.0"
            )
        assert not path.exists()
    else:
        result = pr.recover_current_ticket_execution(
            human_authorization_text=text, ticket_id="P18.9.0"
        )
        assert result["recovery_authorization_recorded"] is True
        assert result["future_retry_requires_separate_start_authorization"] is True
        for key in (
            "retry_execution_started",
            "second_run_started",
            "dispatch_performed",
            "execution_started",
            "worker_execution",
            "Kanban_dispatch",
            "Git_mutation",
            "auto_retry",
        ):
            assert result[key] is False
        record = pr.load_p18_9_0_recovery_action_record()
        assert record["latest_failed_run_id"] == run_id
        assert record["human_authorization_text"] == text
        assert (
            pr.recover_current_ticket_execution(
                human_authorization_text=text, ticket_id="P18.9.0"
            )["idempotent_replay"]
            is True
        )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert [
            run.id for run in kanban_db.list_runs(conn, projected["kanban_task_id"])
        ] == [run_id]
        assert kanban_db.get_task(conn, projected["kanban_task_id"]).status == "blocked"
    finally:
        conn.close()


def test_reported_multiline_authorization_and_tool_prevalidator():
    from tools import pepper_workflow_tools as tools

    text = """I explicitly authorize the governed recovery action
RECOVER_P18_9_12_EXECUTION
for ticket P18.9.12, run 34.

This authorization is for recovery only.

Do not start a retry or a new execution as part of this action."""
    assert (
        tools._validate_explicit_recovery_request(
            text,
            current_ticket_id="P18.9.12",
            requested_next_action_id="RECOVER_P18_9_12_EXECUTION",
        )
        == text
    )
    assert (
        pr.execution_recovery_authorization_text_diagnostics(
            text, current_ticket_id="P18.9.12", current_run_id=34
        )
        is None
    )


def test_requested_ticket_guard_is_enforced():
    result = pr.execution_recovery_authorization_text_diagnostics(
        BASE, current_ticket_id=TICKET, requested_ticket_id="P999.13"
    )
    assert result["blocker_code"] == "EXECUTION_RECOVERY_AUTHORIZATION_TICKET_MISMATCH"
