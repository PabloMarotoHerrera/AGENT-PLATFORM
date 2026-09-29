"""Ticket metadata must cross the canonical P17.7 commit-message boundary."""

from types import SimpleNamespace

import pytest
from pydantic import TypeAdapter, ValidationError

from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.work_packet import human_git_handoff as hgh
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli.test_agent_platform_work_packet_kanban_projection import (
    projection_home as projection_home,
)

LIVE_TITLE = "Work: Execution Lifecycle, Review, Recovery, and Git Handoff UX"
FALLBACK = "P18.9.6 Apply accepted ticket changes"
UNSAFE = [
    LIVE_TITLE,
    "Document git commit",
    "Document git add",
    "Handle --amend",
    "Avoid force push",
    "Fixes #123",
    "Closes #42",
    "Resolves #9",
    "Improve shell; remove cache",
    "Handle $(command)",
    "Handle `command`",
    "api_key=synthetic",
    "raw stdout evidence",
    "C:/Users/example/project",
    "Title\nInjected line",
    "\x00",
    "\x1b[31mTitle",
]


@pytest.mark.parametrize(
    "title",
    UNSAFE
    + [
        "x" * 500,
        "",
        "   ",
        "/home/example/project",
        "/Users/example/project",
        r"D:\Profiles\example",
    ],
)
def test_c56_reserved_or_unbounded_title_uses_neutral_fallback(title):
    binding = SimpleNamespace(ticket_id="P18.9.6", ticket_title=title)
    message = pr._p17_7_handoff_commit_message(binding)
    assert message == FALLBACK
    assert TypeAdapter(hgh.CommitMessageText).validate_python(message) == message
    assert pr._p17_7_handoff_commit_message(binding) == message


@pytest.mark.parametrize("ticket_id", ["P18.9.6", "P99.12"])
def test_c56_safe_title_retains_ticket_identity(ticket_id):
    binding = SimpleNamespace(
        ticket_id=ticket_id, ticket_title="Improve review navigation"
    )
    message = pr._p17_7_handoff_commit_message(binding)
    assert message == f"{ticket_id} Improve review navigation"
    assert TypeAdapter(hgh.CommitMessageText).validate_python(message) == message
    assert len(message) <= 120


@pytest.mark.parametrize("title", UNSAFE)
def test_c56_core_policy_still_rejects_direct_unsafe_subjects(title):
    with pytest.raises(ValueError):
        hgh._validate_commit_message(f"P18.9.6 {title}")


def test_c56_invalid_fallback_fails_closed():
    with pytest.raises(ValidationError):
        pr._p17_7_handoff_commit_message(
            SimpleNamespace(ticket_id="git invalid", ticket_title="--amend")
        )


@pytest.fixture
def accepted(projection_home, tmp_path, monkeypatch):
    original = fixtures._c13_projection_record

    def projection(runtime, ticket_id):
        return {**original(runtime, ticket_id), "ticket_title": LIVE_TITLE}

    monkeypatch.setattr(fixtures, "_c13_projection_record", projection)
    fixture = fixtures._c14_review_authority_fixture(
        pr, tmp_path, monkeypatch, ticket_id="P18.9.6"
    )
    return fixture


def _build(fixture):
    return pr._build_p17_7_current_human_git_handoff_result(
        projection=fixture.projection,
        review_prepare=fixture.review,
        accepted_review=fixture.accepted_record,
        git_snapshot=fixtures._p18_9_2_handoff_git_snapshot(status_entries=[]),
    )


def test_c56_accepted_review_builds_consistent_nonexecuting_package(accepted):
    result, rendered = _build(accepted)
    package = result.package
    assert package.commit_message == FALLBACK
    command = next(
        c for c in package.commands if c.kind == hgh.GitHandoffCommandKind.COMMIT
    )
    assert command.argv == ("git", "commit", "-m", FALLBACK)
    assert package.post_commit_expectation.expected_commit_message == FALLBACK
    assert f"$CommitMessage = '{FALLBACK}'" in rendered
    assert LIVE_TITLE not in rendered
    assert result.authority == hgh.GitHandoffAuthority.HUMAN_ONLY
    assert result.Git_commands_executed == 0
    for field in (
        "staging_performed",
        "commit_performed",
        "push_performed",
        "automatic_staging_authorized",
        "automatic_commit_authorized",
        "automatic_push_authorized",
    ):
        assert getattr(result, field) is False
    assert all(
        c.human_execution_required and not c.automatic_execution_authorized
        for c in package.commands
    )
    hgh.validate_human_git_handoff_result(result)
    again, again_rendered = _build(accepted)
    assert again.model_dump() == result.model_dump()
    assert again_rendered == rendered


def test_c56_public_prepare_accepts_reserved_title(accepted, monkeypatch):
    fixture = accepted
    workflow = fixtures._c14_handoff_completion_workflow(pr, fixture.projection)
    workflow["next_action"]["id"] = "PREPARE_P18_9_6_HUMAN_GIT_HANDOFF"
    monkeypatch.setattr(pr, "build_workflow_control_snapshot", lambda: workflow)
    monkeypatch.setattr(
        pr, "_human_git_handoff_completion_active_execution_blocker", lambda p: None
    )
    context = pr._current_review_candidate_authority_context(
        projection=fixture.projection, review_prepare=fixture.review
    )
    snapshot = fixtures._p18_9_2_handoff_git_snapshot(
        status_entries=[],
        path_SHA256={p: e["source_SHA256"] for p, e in context["files"].items()},
    )
    # Reproduce the old adapter input through the public preparation boundary.
    with monkeypatch.context() as patch:
        patch.setattr(
            pr,
            "_p17_7_handoff_commit_message",
            lambda binding: f"{binding.ticket_id} {LIVE_TITLE}",
        )
        blocked = pr.prepare_current_ticket_human_git_handoff(
            project_id="PEPPER",
            ticket_id="P18.9.6",
            next_action_id="PREPARE_P18_9_6_HUMAN_GIT_HANDOFF",
            git_snapshot_fn=lambda: snapshot,
        )
    assert blocked["blocker_code"] == "P17_7_HUMAN_GIT_HANDOFF_PACKAGE_INVALID"
    assert (
        "commit message must not contain Git instructions" in blocked["blocker_detail"]
    )
    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert not pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.6").exists()
    result = pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.6",
        next_action_id="PREPARE_P18_9_6_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: snapshot,
    )
    assert result["handoff_preparation_recorded"] is True, result
    assert result["commit_message"] == FALLBACK
    assert result["Git_mutation"] is False
    assert result["Git_commands_executed"] == 0
    assert f"$CommitMessage = '{FALLBACK}'" in result["rendered_handoff_powershell"]
    assert LIVE_TITLE not in result["rendered_handoff_powershell"]


def test_c56_subject_changes_propagate_to_all_digests(accepted):
    first, _ = _build(accepted)
    changed = SimpleNamespace(**{
        **accepted.__dict__,
        "projection": {
            **accepted.projection,
            "ticket_title": "Improve review navigation",
        },
    })
    second, _ = _build(changed)
    assert first.package.commit_message != second.package.commit_message
    assert first.package.package_SHA256 != second.package.package_SHA256
    assert (
        first.package.post_commit_expectation.expectation_SHA256
        != second.package.post_commit_expectation.expectation_SHA256
    )
    first_commit = next(
        c for c in first.package.commands if c.kind == hgh.GitHandoffCommandKind.COMMIT
    )
    second_commit = next(
        c for c in second.package.commands if c.kind == hgh.GitHandoffCommandKind.COMMIT
    )
    assert first_commit.command_SHA256 != second_commit.command_SHA256
    assert first.rendered_powershell_SHA256 != second.rendered_powershell_SHA256
    assert first.result_SHA256 != second.result_SHA256
