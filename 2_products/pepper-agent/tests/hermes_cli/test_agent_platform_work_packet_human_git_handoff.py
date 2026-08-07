from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.human_git_handoff as hgh
from hermes_cli.agent_platform.work_packet import (
    HUMAN_GIT_HANDOFF_POLICY_ID,
    HUMAN_GIT_HANDOFF_SCHEMA_VERSION,
    ArtifactReviewVerdict,
    GitHandoffApproval,
    GitHandoffAuthority,
    GitHandoffCandidate,
    GitHandoffCommand,
    GitHandoffCommandKind,
    GitHandoffDecision,
    GitHandoffPackage,
    GitHandoffPathStatus,
    GitHandoffPostCommitExpectation,
    GitHandoffRequest,
    GitHandoffResult,
    GitHandoffState,
    GitHandoffVerificationKind,
    GitHandoffVerificationStep,
    HumanGitHandoffError,
    HumanGitHandoffInputError,
    HumanGitHandoffIntegrityError,
    HumanGitHandoffPolicyError,
    HumanGitHandoffStateError,
    HumanGitHandoffValidationError,
    ReviewArtifactDisposition,
    ReviewArtifactKind,
    ReviewFindingCode,
    ReviewFindingSeverity,
    ReviewObservedPathStatus,
    build_git_handoff_candidates,
    build_human_git_handoff,
    render_human_git_handoff_powershell,
    validate_human_git_handoff_request,
    validate_human_git_handoff_result,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_diff_artifact_review as p17_6,
)


P17_7_EXPORTS = (
    "HUMAN_GIT_HANDOFF_SCHEMA_VERSION",
    "HUMAN_GIT_HANDOFF_POLICY_ID",
    "GitHandoffState",
    "GitHandoffDecision",
    "GitHandoffPathStatus",
    "GitHandoffVerificationKind",
    "GitHandoffCommandKind",
    "GitHandoffAuthority",
    "GitHandoffCandidate",
    "GitHandoffApproval",
    "GitHandoffVerificationStep",
    "GitHandoffCommand",
    "GitHandoffPostCommitExpectation",
    "GitHandoffPackage",
    "GitHandoffRequest",
    "GitHandoffResult",
    "HumanGitHandoffError",
    "HumanGitHandoffInputError",
    "HumanGitHandoffIntegrityError",
    "HumanGitHandoffPolicyError",
    "HumanGitHandoffStateError",
    "HumanGitHandoffValidationError",
    "build_git_handoff_candidates",
    "validate_human_git_handoff_request",
    "build_human_git_handoff",
    "validate_human_git_handoff_result",
    "render_human_git_handoff_powershell",
)
PUBLIC_MODELS = (
    GitHandoffCandidate,
    GitHandoffApproval,
    GitHandoffVerificationStep,
    GitHandoffCommand,
    GitHandoffPostCommitExpectation,
    GitHandoffPackage,
    GitHandoffRequest,
    GitHandoffResult,
)
CONTROLLED_ENUMS = (
    GitHandoffState,
    GitHandoffDecision,
    GitHandoffPathStatus,
    GitHandoffVerificationKind,
    GitHandoffCommandKind,
    GitHandoffAuthority,
)
EXPECTED_ENUM_VALUES = (
    (GitHandoffState, ("prepared", "blocked", "completed")),
    (GitHandoffDecision, ("approved", "rejected")),
    (GitHandoffPathStatus, ("added", "modified", "deleted")),
    (
        GitHandoffVerificationKind,
        (
            "pre_staging",
            "candidate_set",
            "staged_index",
            "post_commit",
            "post_push",
            "committed_integrity",
        ),
    ),
    (
        GitHandoffCommandKind,
        (
            "set_location",
            "stage_path",
            "diff_check",
            "diff_stat",
            "diff_paths",
            "status",
            "commit",
            "push",
            "verify",
            "integrity",
        ),
    ),
    (GitHandoffAuthority, ("human_only",)),
)
FORBIDDEN_PUBLIC_NAMES = (
    "GitHandoffExecutor",
    "GitHandoffRunner",
    "GitCommitter",
    "GitPusher",
    "stage_reviewed_files",
    "commit_reviewed_files",
    "push_reviewed_files",
    "run_git_command",
    "execute_git_handoff",
    "inspect_workspace",
    "clean_workspace",
    "rollback_workspace",
)
INVALID_RELATIVE_PATHS = (
    "",
    "/absolute/path.py",
    "C:/absolute/path.py",
    "src\\file.py",
    "../file.py",
    "src/../file.py",
    "src/./file.py",
    "src//file.py",
    "src/file.py/",
    "src/\x00file.py",
    "src/\nfile.py",
    "src/\rfile.py",
    ".git/config",
    ".gitignore",
    "src/.git/config",
    ".env",
    ".env.local",
    "credentials/config.json",
    "secrets/value.txt",
    "private_key/key.pem",
    "id_rsa",
    "id_ed25519",
    "auth.json",
    "token.json",
)
INVALID_BRANCH_NAMES = (
    "-starts-with-dash",
    "ends-with-slash/",
    "feature bad",
    "feature\\bad",
    "feature..bad",
    "feature;bad",
    "feature&bad",
    "feature|bad",
    "feature<bad",
    "feature>bad",
    "feature`bad",
    "feature$bad",
    "feature(bad",
    "feature)bad",
    "feature{bad",
    "feature}bad",
    "feature[bad",
    "feature]bad",
    "line\nbreak",
    "access_token=value",
    "C:/Users/example/branch",
)
INVALID_COMMIT_MESSAGES = (
    "git status",
    "run git commit",
    "use --amend",
    "force push this",
    "fixes #123",
    "closes #123",
    "resolves #123",
    "message; rm",
    "message& rm",
    "message| rm",
    "message<in",
    "message>out",
    "message`cmd",
    "message$env",
    "message(with parens)",
    "message{block}",
    "message[glob]",
    "line\nbreak",
    "access_token=value",
    "raw stdout dump",
    "C:/Users/example/path",
)
UNSAFE_PUBLIC_TEXTS = (
    "line\nbreak",
    "line\rbreak",
    "access_token=value",
    "Authorization: Bearer tokenvalue",
    "client_secret=value",
    "api_key=value",
    "private key block",
    "password=value",
    "token=value",
    "sk-secret-shaped",
    "raw stdout dump",
    "raw stderr dump",
    "raw diff hunk",
    "diff --git a b",
    "file content snapshot",
    "traceback text",
    "C:/Users/example/path",
    "C:\\Users\\example\\path",
)
INVALID_ARGV_TOKENS = (
    "src/*.py",
    "src/file?.py",
    "src/[abc].py",
    "line\nbreak",
    "access_token=value",
    "Authorization: Bearer tokenvalue",
    "ENV=value",
    "|",
    ">",
    "<",
    "&&",
    ";",
)
FORBIDDEN_RENDERED_TOKENS = (
    "git add .",
    "git add -A",
    "git add --all",
    "git push --force",
    "git push -f",
    "git commit --amend",
    "Invoke-Expression",
    "Start-Process",
    "EncodedCommand",
    "git reset",
    "git clean",
    "git stash",
    "git switch",
    "git checkout",
    "git merge",
    "git rebase",
    "git worktree",
    "git tag",
    "cmd.exe",
    "powershell.exe",
    "pwsh",
    "bash",
)
RESULT_TAMPERS = (
    ("candidate_count", 99),
    ("added_count", 99),
    ("modified_count", 99),
    ("deleted_count", 99),
    ("state", GitHandoffState.BLOCKED.value),
    ("decision", GitHandoffDecision.REJECTED.value),
    ("human_git_handoff_requirement_satisfied", False),
    ("Git_commands_executed", 1),
    ("staging_performed", True),
    ("commit_performed", True),
    ("push_performed", True),
    ("automatic_cleanup_authorized", True),
    ("automatic_rollback_authorized", True),
    ("automatic_staging_authorized", True),
    ("automatic_commit_authorized", True),
    ("automatic_push_authorized", True),
    ("provider_dispatch_count", 1),
    ("model_inference_count", 1),
    ("rendered_powershell_SHA256", p17_6.digest_text("tamper")),
    ("handoff_id", "HGR-P17-7-R0001-aaaaaaaaaaaa"),
    ("result_SHA256", p17_6.digest_text("tamper")),
)
REQUEST_BINDING_TAMPERS = (
    "work_packet_id",
    "work_packet_sha",
    "allocation_work_packet_id",
    "allocation_work_packet_sha",
    "profile_work_packet_id",
    "profile_allocation_id",
    "outcome_sha",
    "review_work_packet_id",
    "review_allocation_id",
    "review_profile_id",
    "review_outcome_sha",
    "approval_review_id",
    "approval_review_sha",
    "approval_branch",
    "approval_parent",
)
COMMAND_SHAPE_CASES = (
    (GitHandoffCommandKind.VERIFY, ("git", "reset", "--hard")),
    (GitHandoffCommandKind.VERIFY, ("git", "clean", "-fd")),
    (GitHandoffCommandKind.VERIFY, ("git", "stash")),
    (GitHandoffCommandKind.VERIFY, ("git", "switch", "main")),
    (GitHandoffCommandKind.VERIFY, ("git", "checkout", "main")),
    (GitHandoffCommandKind.VERIFY, ("git", "merge", "main")),
    (GitHandoffCommandKind.VERIFY, ("git", "rebase", "main")),
    (GitHandoffCommandKind.VERIFY, ("git", "worktree", "list")),
    (GitHandoffCommandKind.VERIFY, ("git", "tag", "v1")),
    (GitHandoffCommandKind.STAGE_PATH, ("git", "add", ".")),
    (GitHandoffCommandKind.STAGE_PATH, ("git", "add", "-A")),
    (GitHandoffCommandKind.STAGE_PATH, ("git", "add", "--all")),
    (GitHandoffCommandKind.STAGE_PATH, ("git", "add", "--", "src/*.py")),
    (GitHandoffCommandKind.COMMIT, ("git", "commit", "--amend")),
    (GitHandoffCommandKind.COMMIT, ("git", "commit", "-am", "message")),
    (GitHandoffCommandKind.PUSH, ("git", "push", "origin", "branch", "--force")),
    (GitHandoffCommandKind.PUSH, ("git", "push", "upstream", "branch")),
    (GitHandoffCommandKind.INTEGRITY, ("python", "-c", "print(1)")),
    (GitHandoffCommandKind.SET_LOCATION, ("Set-Location",)),
    (GitHandoffCommandKind.STATUS, ("verify", "manual")),
    (GitHandoffCommandKind.VERIFY, ("git", "status")),
    (GitHandoffCommandKind.STATUS, ("git", "rev-parse", "HEAD")),
)


@pytest.fixture(scope="module")
def contexts(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p17_7")
    try:
        return {
            "accepted": p17_6.terminal_context(
                monkeypatch, root / "accepted", kind="result"
            ),
            "warning": p17_6.terminal_context(
                monkeypatch,
                root / "warning",
                kind="result",
                docs_artifact_kind=ReviewArtifactKind.REPORT.value,
            ),
            "failure": p17_6.terminal_context(
                monkeypatch, root / "failure", kind="failure"
            ),
            "cancellation": p17_6.terminal_context(
                monkeypatch, root / "cancellation", kind="cancellation"
            ),
        }
    finally:
        monkeypatch.undo()


def warning_artifacts():
    return (
        p17_6.artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.REPORT,
            disposition=ReviewArtifactDisposition.REQUIRES_HUMAN_REVIEW,
        ),
        p17_6.canonical_artifacts()[1],
        p17_6.canonical_artifacts()[2],
    )


def review_result(context, *, warning: bool = False):
    artifacts = warning_artifacts() if warning else p17_6.canonical_artifacts()
    obs = p17_6.observation(context, p17_6.canonical_paths(), artifacts)
    return p17_6.build_diff_artifact_review(p17_6.request(context, obs))


def warning_finding_ids(review) -> tuple[str, ...]:
    return tuple(
        finding.finding_id
        for finding in review.findings
        if finding.severity is ReviewFindingSeverity.WARNING
        or finding.code is ReviewFindingCode.ARTIFACT_REQUIRES_REVIEW
    )


def approval_for_review(
    context,
    review,
    *,
    decision: GitHandoffDecision = GitHandoffDecision.APPROVED,
    accepted_finding_ids: tuple[str, ...] = (),
    accepted_candidate_ids: tuple[str, ...] | None = None,
    commit_message: str = "P17.7 Add human handoff",
    approver_id: str = "human.p17-7",
) -> GitHandoffApproval:
    candidates = build_git_handoff_candidates(review)
    data = {
        "approval_reference": "APPROVAL-P17-7",
        "human_approver_id": approver_id,
        "synthetic": False,
        "decision": decision,
        "review_id": review.review_id,
        "review_SHA256": review.result_SHA256,
        "accepted_finding_ids": tuple(sorted(accepted_finding_ids)),
        "accepted_candidate_ids": accepted_candidate_ids
        if accepted_candidate_ids is not None
        else tuple(candidate.candidate_id for candidate in candidates),
        "commit_message": commit_message,
        "remote_name": "origin",
        "branch_name": context[
            "allocation"
        ].allocation.repository_identity.workspace_branch,
        "expected_parent_commit": context[
            "allocation"
        ].allocation.repository_identity.source_commit,
        "rationale": "Human approved exact reviewed handoff.",
    }
    return GitHandoffApproval(
        **data,
        approval_SHA256=hgh._approval_digest_from_record(data),
    )


def handoff_request(
    context,
    review,
    *,
    approval: GitHandoffApproval | None = None,
    repository_display_path: str = "PEPPER_WORKSPACE",
) -> GitHandoffRequest:
    return GitHandoffRequest(
        compilation_result=context["compilation"],
        allocation_result=context["allocation"],
        profile_result=context["profile"],
        outcome_envelope=context["outcome"],
        diff_artifact_review_result=review,
        approval=approval
        if approval is not None
        else approval_for_review(context, review),
        repository_display_path=repository_display_path,
    )


@pytest.fixture(scope="module")
def accepted_request(contexts):
    review = review_result(contexts["accepted"])
    return handoff_request(contexts["accepted"], review)


@pytest.fixture(scope="module")
def accepted_result(accepted_request):
    return build_human_git_handoff(accepted_request)


@pytest.fixture(scope="module")
def sample_models(accepted_request, accepted_result):
    package = accepted_result.package
    return {
        GitHandoffCandidate.__name__: package.candidates[0],
        GitHandoffApproval.__name__: accepted_request.approval,
        GitHandoffVerificationStep.__name__: package.verification_steps[0],
        GitHandoffCommand.__name__: package.commands[0],
        GitHandoffPostCommitExpectation.__name__: package.post_commit_expectation,
        GitHandoffPackage.__name__: package,
        GitHandoffRequest.__name__: accepted_request,
        GitHandoffResult.__name__: accepted_result,
    }


def _without(data: dict, field: str) -> dict:
    return {key: value for key, value in data.items() if key != field}


def _candidate_with_updates(candidate: GitHandoffCandidate, **updates):
    data = candidate.model_dump(mode="json")
    data.update(updates)
    data["candidate_SHA256"] = hgh._candidate_digest_from_record(
        _without(data, "candidate_SHA256")
    )
    return GitHandoffCandidate.model_validate(data)


def _approval_data(approval: GitHandoffApproval, **updates):
    data = approval.model_dump(mode="json")
    data.update(updates)
    data["approval_SHA256"] = hgh._approval_digest_from_record(
        _without(data, "approval_SHA256")
    )
    return data


def _command_data(order: int, kind: GitHandoffCommandKind, argv: tuple[str, ...]):
    data = {
        "command_id": f"GHCM-{order:03d}",
        "kind": kind,
        "order": order,
        "argv": argv,
        "display_text": "Verify invalid command is rejected.",
        "human_execution_required": True,
        "automatic_execution_authorized": False,
    }
    data["command_SHA256"] = hgh._command_digest_from_record(data)
    return data


def _retamper_result(result: GitHandoffResult, field: str, value):
    data = result.model_dump(mode="json")
    data[field] = value
    if field != "result_SHA256":
        data["result_SHA256"] = hgh._result_digest_from_record(
            _without(data, "result_SHA256")
        )
    return data


@pytest.mark.parametrize("exported_name", P17_7_EXPORTS)
def test_all_p17_7_exports_exist(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)
    assert hasattr(hgh, exported_name)


def test_p17_0_through_p17_6_exports_remain_exact_prefix() -> None:
    prior = (
        p17_6.p17_5.P17_0_EXPORTS
        + p17_6.p17_5.P17_1_EXPORTS
        + p17_6.p17_5.P17_2_EXPORTS
        + p17_6.p17_5.P17_3_EXPORTS
        + p17_6.p17_5.P17_4_EXPORTS
        + p17_6.p17_5.P17_5_EXPORTS
        + p17_6.P17_6_EXPORTS
    )
    assert len(prior) == 201
    assert work_packet.__all__[:201] == prior
    assert work_packet.__all__[201:228] == P17_7_EXPORTS
    assert len(work_packet.__all__) >= 228
    assert len(set(work_packet.__all__)) == len(work_packet.__all__)
    assert not any(name.startswith("_") for name in work_packet.__all__)


def test_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        len(hgh.__all__),
        hasattr(work_packet, "GitHandoffResult"),
        hasattr(work_packet, "build_human_git_handoff"),
        hasattr(work_packet, "GitHandoffExecutor"),
    ) == (len(work_packet.__all__), len(work_packet.__all__), 27, True, True, False)


@pytest.mark.parametrize("name", FORBIDDEN_PUBLIC_NAMES)
def test_forbidden_public_names_absent(name: str) -> None:
    assert not hasattr(work_packet, name)
    assert not hasattr(hgh, name)


@pytest.mark.parametrize(
    "function,expected",
    (
        (build_git_handoff_candidates, "build_git_handoff_candidates"),
        (validate_human_git_handoff_request, "validate_human_git_handoff_request"),
        (build_human_git_handoff, "build_human_git_handoff"),
        (validate_human_git_handoff_result, "validate_human_git_handoff_result"),
        (
            render_human_git_handoff_powershell,
            "render_human_git_handoff_powershell",
        ),
    ),
)
def test_function_import_smoke_exact_names(function, expected: str) -> None:
    assert function.__name__ == expected


def test_legacy_instruction_renderer_is_not_public_or_package_level() -> None:
    assert work_packet.__all__[227] == "render_human_git_handoff_powershell"
    assert not hasattr(work_packet, "render_human_git_handoff_instructions")
    assert "render_human_git_handoff_instructions" not in hgh.__all__


@pytest.mark.parametrize(
    "error_cls",
    (
        HumanGitHandoffError,
        HumanGitHandoffInputError,
        HumanGitHandoffIntegrityError,
        HumanGitHandoffPolicyError,
        HumanGitHandoffStateError,
        HumanGitHandoffValidationError,
    ),
)
def test_public_exceptions_are_value_errors(error_cls: type[Exception]) -> None:
    assert issubclass(error_cls, ValueError)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_models_are_frozen(model_cls: type[BaseModel]) -> None:
    assert model_cls.model_config["frozen"] is True
    assert model_cls.model_config["extra"] == "forbid"
    assert model_cls.model_config["validate_default"] is True
    assert model_cls.model_config["str_strip_whitespace"] is True


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_public_model_schemas_reject_additional_properties(
    model_cls: type[BaseModel],
) -> None:
    assert model_cls.model_json_schema()["additionalProperties"] is False


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_unknown_fields_fail(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["unknown"] = "blocked"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_models_are_immutable(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    field = next(iter(model.model_fields))
    with pytest.raises(ValidationError):
        setattr(model, field, getattr(model, field))


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_json_round_trip_supported(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    assert model_cls.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_tuple_immutability_retained(model_cls: type[BaseModel], sample_models) -> None:
    model = sample_models[model_cls.__name__]
    for name, value in model:
        if isinstance(value, tuple):
            data = model.model_dump(mode="json")
            assert isinstance(data[name], list)
            assert isinstance(
                model_cls.model_validate(data).__getattribute__(name), tuple
            )


@pytest.mark.parametrize(
    "model_cls", (GitHandoffPackage, GitHandoffRequest, GitHandoffResult)
)
def test_alternative_schema_versions_fail(
    model_cls: type[BaseModel], sample_models
) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize(
    "model_cls", (GitHandoffPackage, GitHandoffRequest, GitHandoffResult)
)
def test_alternative_policy_ids_fail(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["policy_id"] = "alternate-policy"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize("enum_cls,expected", EXPECTED_ENUM_VALUES)
def test_exact_enum_values(enum_cls: type[Enum], expected: tuple[str, ...]) -> None:
    assert tuple(item.value for item in enum_cls) == expected


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_enum_aliases_absent(enum_cls: type[Enum]) -> None:
    assert len(enum_cls) == len({item.value for item in enum_cls})


@pytest.mark.parametrize("enum_cls", CONTROLLED_ENUMS)
def test_unknown_enum_values_fail(enum_cls: type[Enum]) -> None:
    with pytest.raises(ValueError):
        enum_cls("__unknown__")


@pytest.mark.parametrize(
    "forbidden",
    (
        "auto_staged",
        "auto_committed",
        "auto_pushed",
        "executed",
        "workspace_cleanup",
        "rollback",
        "provider_dispatch",
        "model_inference",
    ),
)
def test_forbidden_enum_values_absent(forbidden: str) -> None:
    for enum_cls in CONTROLLED_ENUMS:
        assert forbidden not in {item.value for item in enum_cls}


def test_schema_and_policy_identity() -> None:
    assert HUMAN_GIT_HANDOFF_SCHEMA_VERSION == 1
    assert HUMAN_GIT_HANDOFF_POLICY_ID == (
        "pepper-exact-review-bound-non-executing-human-git-handoff-v1"
    )


def test_build_candidates_from_canonical_review(accepted_request) -> None:
    candidates = build_git_handoff_candidates(
        accepted_request.diff_artifact_review_result
    )
    assert tuple(candidate.candidate_id for candidate in candidates) == (
        "GHCP-001",
        "GHCP-002",
        "GHCP-003",
    )
    assert tuple(candidate.relative_path for candidate in candidates) == (
        "docs/new.md",
        "src/existing.py",
        "tests/old_test.py",
    )
    assert tuple(candidate.status for candidate in candidates) == (
        GitHandoffPathStatus.ADDED,
        GitHandoffPathStatus.MODIFIED,
        GitHandoffPathStatus.DELETED,
    )


def test_canonical_accepted_review_builds_exact_human_git_handoff_flow(
    accepted_result,
) -> None:
    assert accepted_result.state is GitHandoffState.COMPLETED
    assert accepted_result.decision is GitHandoffDecision.APPROVED
    assert accepted_result.authority is GitHandoffAuthority.HUMAN_ONLY
    assert accepted_result.candidate_count == 3
    assert accepted_result.added_count == 1
    assert accepted_result.modified_count == 1
    assert accepted_result.deleted_count == 1
    assert accepted_result.human_git_handoff_requirement_satisfied is True
    assert accepted_result.Git_commands_executed == 0
    assert accepted_result.staging_performed is False
    assert accepted_result.commit_performed is False
    assert accepted_result.push_performed is False
    assert accepted_result.provider_dispatch_count == 0
    assert accepted_result.model_inference_count == 0


def test_canonical_warning_review_requires_exact_human_finding_acceptance_flow(
    contexts,
) -> None:
    review = review_result(contexts["warning"], warning=True)
    assert review.artifact_verdict is ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    approval = approval_for_review(
        contexts["warning"],
        review,
        accepted_finding_ids=warning_finding_ids(review),
    )
    result = build_human_git_handoff(
        handoff_request(contexts["warning"], review, approval=approval)
    )
    assert result.state is GitHandoffState.COMPLETED
    assert result.decision is GitHandoffDecision.APPROVED
    assert result.package.candidates[0].source_artifact_id == "ARTF-001"


def test_canonical_rejected_approval_blocks_handoff_without_git_execution_flow(
    contexts,
) -> None:
    review = review_result(contexts["accepted"])
    approval = approval_for_review(
        contexts["accepted"], review, decision=GitHandoffDecision.REJECTED
    )
    result = build_human_git_handoff(
        handoff_request(contexts["accepted"], review, approval=approval)
    )
    assert result.state is GitHandoffState.BLOCKED
    assert result.decision is GitHandoffDecision.REJECTED
    assert result.human_git_handoff_requirement_satisfied is False
    assert result.Git_commands_executed == 0
    assert result.staging_performed is False
    assert result.commit_performed is False
    assert result.push_performed is False


def test_canonical_accepted_review_human_git_handoff_flow(accepted_result) -> None:
    assert accepted_result.state is GitHandoffState.COMPLETED
    assert accepted_result.decision is GitHandoffDecision.APPROVED
    assert accepted_result.human_git_handoff_requirement_satisfied is True
    assert accepted_result.Git_commands_executed == 0
    assert accepted_result.staging_performed is False
    assert accepted_result.commit_performed is False
    assert accepted_result.push_performed is False


def test_canonical_warning_review_requires_explicit_human_acceptance_flow(
    contexts,
) -> None:
    review = review_result(contexts["warning"], warning=True)
    approval = approval_for_review(
        contexts["warning"],
        review,
        accepted_finding_ids=warning_finding_ids(review),
    )
    result = build_human_git_handoff(
        handoff_request(contexts["warning"], review, approval=approval)
    )
    assert result.state is GitHandoffState.COMPLETED
    assert result.decision is GitHandoffDecision.APPROVED
    assert result.human_git_handoff_requirement_satisfied is True


def test_canonical_blocking_review_rejects_git_handoff_flow(contexts) -> None:
    paths = p17_6.canonical_paths()[:2]
    obs = p17_6.observation(contexts["accepted"], paths)
    review = p17_6.build_diff_artifact_review(p17_6.request(contexts["accepted"], obs))
    with pytest.raises(HumanGitHandoffStateError, match="review must be completed"):
        build_git_handoff_candidates(review)


def test_validate_request_accepts_canonical_request(accepted_request) -> None:
    validate_human_git_handoff_request(accepted_request)


def test_validate_result_accepts_canonical_result(accepted_result) -> None:
    validate_human_git_handoff_result(accepted_result)


def test_repeated_equal_inputs_produce_equal_result(accepted_request) -> None:
    first = build_human_git_handoff(accepted_request)
    second = build_human_git_handoff(accepted_request)
    assert first == second
    assert first.handoff_id == second.handoff_id
    assert first.result_SHA256 == second.result_SHA256
    assert first.rendered_powershell_SHA256 == second.rendered_powershell_SHA256


def test_rendered_powershell_is_deterministic_and_human_bounded(
    accepted_result,
) -> None:
    first = render_human_git_handoff_powershell(accepted_result.package)
    second = render_human_git_handoff_powershell(accepted_result.package)
    assert first == second
    assert first.startswith("$ErrorActionPreference = 'Stop'\n")
    assert "git add -- $RelativePath" in first
    assert "git commit -m $CommitMessage" in first
    assert "git push origin $BranchName" in first
    assert "pepper_baseline_integrity.py" in first
    assert len(first) < 32768


@pytest.mark.parametrize("forbidden", FORBIDDEN_RENDERED_TOKENS)
def test_rendered_powershell_excludes_forbidden_tokens(
    accepted_result, forbidden: str
) -> None:
    assert (
        forbidden.lower()
        not in render_human_git_handoff_powershell(accepted_result.package).lower()
    )


def test_package_expectation_matches_candidates(accepted_result) -> None:
    expectation = accepted_result.package.post_commit_expectation
    assert expectation.expected_file_count == 3
    assert expectation.expected_added_count == 1
    assert expectation.expected_modified_count == 1
    assert expectation.expected_deleted_count == 1
    assert expectation.expected_candidate_paths == (
        "docs/new.md",
        "src/existing.py",
        "tests/old_test.py",
    )
    assert expectation.expected_worktree_clean is True
    assert expectation.expected_remote_match is True
    assert expectation.expected_integrity_file_count == 6884


def test_verification_steps_are_exact_blocking_sequence(accepted_result) -> None:
    steps = accepted_result.package.verification_steps
    assert tuple(step.step_id for step in steps) == tuple(
        f"GHVS-{index:03d}" for index in range(1, 7)
    )
    assert tuple(step.kind for step in steps) == tuple(GitHandoffVerificationKind)
    assert all(step.blocking is True for step in steps)


def test_commands_are_human_required_non_automatic_sequence(accepted_result) -> None:
    commands = accepted_result.package.commands
    assert tuple(command.command_id for command in commands) == tuple(
        f"GHCM-{index:03d}" for index in range(1, len(commands) + 1)
    )
    assert all(command.human_execution_required is True for command in commands)
    assert all(command.automatic_execution_authorized is False for command in commands)
    assert (
        sum(command.kind is GitHandoffCommandKind.STAGE_PATH for command in commands)
        == 3
    )
    assert any(command.kind is GitHandoffCommandKind.COMMIT for command in commands)
    assert any(command.kind is GitHandoffCommandKind.PUSH for command in commands)
    assert any(command.kind is GitHandoffCommandKind.INTEGRITY for command in commands)


@pytest.mark.parametrize("path", INVALID_RELATIVE_PATHS)
def test_invalid_candidate_relative_paths_fail(accepted_result, path: str) -> None:
    candidate = accepted_result.package.candidates[0]
    data = candidate.model_dump(mode="json")
    data["relative_path"] = path
    data["candidate_SHA256"] = hgh._candidate_digest_from_record(
        _without(data, "candidate_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffCandidate.model_validate(data)


@pytest.mark.parametrize("branch", INVALID_BRANCH_NAMES)
def test_invalid_branch_names_fail(accepted_request, branch: str) -> None:
    data = _approval_data(accepted_request.approval, branch_name=branch)
    with pytest.raises(ValidationError):
        GitHandoffApproval.model_validate(data)


@pytest.mark.parametrize("message", INVALID_COMMIT_MESSAGES)
def test_invalid_commit_messages_fail(accepted_request, message: str) -> None:
    data = _approval_data(accepted_request.approval, commit_message=message)
    with pytest.raises(ValidationError):
        GitHandoffApproval.model_validate(data)


@pytest.mark.parametrize("text", UNSAFE_PUBLIC_TEXTS)
def test_unsafe_approval_references_fail(accepted_request, text: str) -> None:
    data = _approval_data(accepted_request.approval, approval_reference=text)
    with pytest.raises(ValidationError):
        GitHandoffApproval.model_validate(data)


@pytest.mark.parametrize("text", UNSAFE_PUBLIC_TEXTS)
def test_unsafe_approval_rationales_fail(accepted_request, text: str) -> None:
    data = _approval_data(accepted_request.approval, rationale=text)
    with pytest.raises(ValidationError):
        GitHandoffApproval.model_validate(data)


@pytest.mark.parametrize("text", UNSAFE_PUBLIC_TEXTS)
def test_unsafe_repository_display_paths_fail(accepted_request, text: str) -> None:
    data = accepted_request.model_dump(mode="json")
    data["repository_display_path"] = text
    with pytest.raises(ValidationError):
        GitHandoffRequest.model_validate(data)


@pytest.mark.parametrize(
    "field,value",
    (
        ("synthetic", True),
        ("human_approver_id", "SHADOW-human"),
        ("decision", "unknown"),
        ("accepted_candidate_ids", ("GHCP-002", "GHCP-001")),
        ("accepted_candidate_ids", ("GHCP-001", "GHCP-001")),
        ("accepted_finding_ids", ("FIND-002", "FIND-001")),
        ("accepted_finding_ids", ("FIND-001", "FIND-001")),
        ("remote_name", "upstream"),
        ("expected_parent_commit", "b" * 39),
        ("approval_SHA256", p17_6.digest_text("tamper")),
    ),
)
def test_invalid_approval_fields_fail(accepted_request, field: str, value) -> None:
    data = accepted_request.approval.model_dump(mode="json")
    data[field] = value
    if field != "approval_SHA256":
        data["approval_SHA256"] = hgh._approval_digest_from_record(
            _without(data, "approval_SHA256")
        )
    with pytest.raises(ValidationError):
        GitHandoffApproval.model_validate(data)


def test_warning_review_without_exact_finding_acceptance_fails(contexts) -> None:
    review = review_result(contexts["warning"], warning=True)
    request = handoff_request(contexts["warning"], review)
    with pytest.raises(HumanGitHandoffPolicyError):
        validate_human_git_handoff_request(request)


def test_accepted_review_with_unneeded_finding_acceptance_fails(contexts) -> None:
    review = review_result(contexts["accepted"])
    approval = approval_for_review(
        contexts["accepted"], review, accepted_finding_ids=("FIND-001",)
    )
    request = handoff_request(contexts["accepted"], review, approval=approval)
    with pytest.raises(HumanGitHandoffPolicyError):
        validate_human_git_handoff_request(request)


def test_candidate_set_mismatch_fails_request_policy(contexts) -> None:
    review = review_result(contexts["accepted"])
    approval = approval_for_review(
        contexts["accepted"], review, accepted_candidate_ids=("GHCP-001",)
    )
    request = handoff_request(contexts["accepted"], review, approval=approval)
    with pytest.raises(HumanGitHandoffPolicyError):
        validate_human_git_handoff_request(request)


@pytest.mark.parametrize("tamper", REQUEST_BINDING_TAMPERS)
def test_request_binding_tampering_fails(
    contexts, accepted_request, tamper: str
) -> None:
    request = accepted_request
    if tamper == "work_packet_id":
        packet = request.compilation_result.work_packet.model_copy(
            update={"work_packet_id": "WP-P17-7-MISMATCH-R0001-aaaaaaaaaaaa"}
        )
        compilation = request.compilation_result.model_copy(
            update={"work_packet": packet}
        )
        request = request.model_copy(update={"compilation_result": compilation})
    elif tamper == "work_packet_sha":
        packet = request.compilation_result.work_packet.model_copy(
            update={"work_packet_SHA256": p17_6.digest_text(tamper)}
        )
        compilation = request.compilation_result.model_copy(
            update={"work_packet": packet}
        )
        request = request.model_copy(update={"compilation_result": compilation})
    elif tamper == "allocation_work_packet_id":
        allocation = request.allocation_result.allocation.model_copy(
            update={"work_packet_id": "different"}
        )
        request = request.model_copy(
            update={
                "allocation_result": request.allocation_result.model_copy(
                    update={"allocation": allocation}
                )
            }
        )
    elif tamper == "allocation_work_packet_sha":
        allocation = request.allocation_result.allocation.model_copy(
            update={"work_packet_SHA256": p17_6.digest_text(tamper)}
        )
        request = request.model_copy(
            update={
                "allocation_result": request.allocation_result.model_copy(
                    update={"allocation": allocation}
                )
            }
        )
    elif tamper == "profile_work_packet_id":
        profile = request.profile_result.profile.model_copy(
            update={"work_packet_id": "different"}
        )
        request = request.model_copy(
            update={
                "profile_result": request.profile_result.model_copy(
                    update={"profile": profile}
                )
            }
        )
    elif tamper == "profile_allocation_id":
        profile = request.profile_result.profile.model_copy(
            update={"allocation_id": "different"}
        )
        request = request.model_copy(
            update={
                "profile_result": request.profile_result.model_copy(
                    update={"profile": profile}
                )
            }
        )
    elif tamper == "outcome_sha":
        request = request.model_copy(
            update={
                "outcome_envelope": request.outcome_envelope.model_copy(
                    update={"envelope_SHA256": p17_6.digest_text(tamper)}
                )
            }
        )
    elif tamper == "review_work_packet_id":
        review = request.diff_artifact_review_result.model_copy(
            update={"work_packet_id": "different"}
        )
        request = request.model_copy(update={"diff_artifact_review_result": review})
    elif tamper == "review_allocation_id":
        review = request.diff_artifact_review_result.model_copy(
            update={"allocation_id": "different"}
        )
        request = request.model_copy(update={"diff_artifact_review_result": review})
    elif tamper == "review_profile_id":
        review = request.diff_artifact_review_result.model_copy(
            update={"profile_id": "different"}
        )
        request = request.model_copy(update={"diff_artifact_review_result": review})
    elif tamper == "review_outcome_sha":
        review = request.diff_artifact_review_result.model_copy(
            update={"outcome_SHA256": p17_6.digest_text(tamper)}
        )
        request = request.model_copy(update={"diff_artifact_review_result": review})
    elif tamper == "approval_review_id":
        approval = request.approval.model_copy(update={"review_id": "different"})
        request = request.model_copy(update={"approval": approval})
    elif tamper == "approval_review_sha":
        approval = request.approval.model_copy(
            update={"review_SHA256": p17_6.digest_text(tamper)}
        )
        request = request.model_copy(update={"approval": approval})
    elif tamper == "approval_branch":
        approval = request.approval.model_copy(update={"branch_name": "other"})
        request = request.model_copy(update={"approval": approval})
    elif tamper == "approval_parent":
        approval = request.approval.model_copy(
            update={"expected_parent_commit": "b" * 40}
        )
        request = request.model_copy(update={"approval": approval})
    with pytest.raises(HumanGitHandoffError):
        build_human_git_handoff(request)


@pytest.mark.parametrize("kind", ("failure", "cancellation"))
def test_terminal_non_result_outcomes_can_be_handed_off(contexts, kind: str) -> None:
    review = review_result(contexts[kind])
    result = build_human_git_handoff(handoff_request(contexts[kind], review))
    assert result.outcome_kind is contexts[kind]["outcome"].envelope_kind
    assert result.state is GitHandoffState.COMPLETED


def test_blocked_review_cannot_be_handed_off(contexts) -> None:
    paths = p17_6.canonical_paths()[:2]
    obs = p17_6.observation(contexts["accepted"], paths)
    review = p17_6.build_diff_artifact_review(p17_6.request(contexts["accepted"], obs))
    with pytest.raises(HumanGitHandoffStateError):
        build_git_handoff_candidates(review)


@pytest.mark.parametrize(
    "status",
    (
        ReviewObservedPathStatus.RENAMED,
        ReviewObservedPathStatus.TYPE_CHANGED,
        ReviewObservedPathStatus.UNMERGED,
    ),
)
def test_unsupported_observed_statuses_cannot_be_candidates(
    contexts, status: ReviewObservedPathStatus
) -> None:
    paths = (
        p17_6.observed_path(1, "docs/new.md", status),
        p17_6.canonical_paths()[1],
        p17_6.canonical_paths()[2],
    )
    paths = tuple(sorted(paths, key=lambda item: item.relative_path))
    paths = tuple(
        p17_6.observed_path(
            index, item.relative_path, item.status, tracked=item.tracked
        )
        for index, item in enumerate(paths, start=1)
    )
    obs = p17_6.observation(contexts["accepted"], paths)
    review = p17_6.build_diff_artifact_review(p17_6.request(contexts["accepted"], obs))
    with pytest.raises(HumanGitHandoffStateError):
        build_git_handoff_candidates(review)


def test_candidate_digest_tampering_fails(accepted_result) -> None:
    data = accepted_result.package.candidates[0].model_dump(mode="json")
    data["candidate_SHA256"] = p17_6.digest_text("tamper")
    with pytest.raises(ValidationError):
        GitHandoffCandidate.model_validate(data)


def test_deleted_candidate_with_content_evidence_fails(accepted_result) -> None:
    candidate = accepted_result.package.candidates[2]
    data = candidate.model_dump(mode="json")
    data["content_SHA256"] = p17_6.digest_text("content")
    data["bytes_after"] = 10
    data["candidate_SHA256"] = hgh._candidate_digest_from_record(
        _without(data, "candidate_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffCandidate.model_validate(data)


def test_nondeleted_candidate_without_content_evidence_fails(accepted_result) -> None:
    candidate = accepted_result.package.candidates[0]
    data = candidate.model_dump(mode="json")
    data["content_SHA256"] = None
    data["bytes_after"] = None
    data["candidate_SHA256"] = hgh._candidate_digest_from_record(
        _without(data, "candidate_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffCandidate.model_validate(data)


def test_candidate_collection_must_be_sorted(accepted_result) -> None:
    data = accepted_result.package.model_dump(mode="json")
    data["candidates"] = [
        data["candidates"][1],
        data["candidates"][0],
        data["candidates"][2],
    ]
    data["package_SHA256"] = hgh._digest_from_record(
        hgh.PACKAGE_DIGEST_ALGORITHM, _without(data, "package_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffPackage.model_validate(data)


def test_candidate_collection_must_have_contiguous_ids(accepted_result) -> None:
    package = accepted_result.package
    changed = _candidate_with_updates(package.candidates[1], candidate_id="GHCP-003")
    data = package.model_dump(mode="json")
    data["candidates"][1] = changed.model_dump(mode="json")
    data["package_SHA256"] = hgh._digest_from_record(
        hgh.PACKAGE_DIGEST_ALGORITHM, _without(data, "package_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffPackage.model_validate(data)


@pytest.mark.parametrize("field,value", RESULT_TAMPERS)
def test_result_tampering_fails(accepted_result, field: str, value) -> None:
    with pytest.raises(ValidationError):
        GitHandoffResult.model_validate(_retamper_result(accepted_result, field, value))


@pytest.mark.parametrize(
    "field,value",
    (
        ("branch_name", "other"),
        ("expected_parent_commit", "b" * 40),
        ("commit_message", "P17.7 Alternate handoff"),
        ("remote_name", "upstream"),
        ("repository_display_path", "C:/Users/example/workspace"),
        ("package_id", "GHP-P17-7-R0001-aaaaaaaaaaaa"),
        ("package_SHA256", p17_6.digest_text("tamper")),
    ),
)
def test_package_tampering_fails(accepted_result, field: str, value) -> None:
    data = accepted_result.package.model_dump(mode="json")
    data[field] = value
    if field != "package_SHA256":
        data["package_SHA256"] = hgh._digest_from_record(
            hgh.PACKAGE_DIGEST_ALGORITHM, _without(data, "package_SHA256")
        )
    with pytest.raises(ValidationError):
        GitHandoffPackage.model_validate(data)


@pytest.mark.parametrize(
    "field,value",
    (
        ("expected_file_count", 99),
        ("expected_added_count", 99),
        ("expected_modified_count", 99),
        ("expected_deleted_count", 99),
        ("expected_candidate_paths", ("src/existing.py", "docs/new.md")),
        ("expected_worktree_clean", False),
        ("expected_remote_match", False),
        ("expected_integrity_file_count", 1),
        ("expectation_SHA256", p17_6.digest_text("tamper")),
    ),
)
def test_post_commit_expectation_tampering_fails(
    accepted_result, field: str, value
) -> None:
    data = accepted_result.package.post_commit_expectation.model_dump(mode="json")
    data[field] = value
    if field != "expectation_SHA256":
        data["expectation_SHA256"] = hgh._post_commit_expectation_digest_from_record(
            _without(data, "expectation_SHA256")
        )
    with pytest.raises(ValidationError):
        GitHandoffPostCommitExpectation.model_validate(data)


@pytest.mark.parametrize("kind,argv", COMMAND_SHAPE_CASES)
def test_invalid_command_shapes_fail(
    kind: GitHandoffCommandKind, argv: tuple[str, ...]
) -> None:
    with pytest.raises(ValidationError):
        GitHandoffCommand.model_validate(_command_data(1, kind, argv))


@pytest.mark.parametrize("token", INVALID_ARGV_TOKENS)
def test_invalid_argv_tokens_fail(token: str) -> None:
    data = _command_data(1, GitHandoffCommandKind.VERIFY, ("verify", token))
    with pytest.raises(ValidationError):
        GitHandoffCommand.model_validate(data)


def test_command_digest_tampering_fails(accepted_result) -> None:
    data = accepted_result.package.commands[0].model_dump(mode="json")
    data["command_SHA256"] = p17_6.digest_text("tamper")
    with pytest.raises(ValidationError):
        GitHandoffCommand.model_validate(data)


def test_command_order_must_match_identifier(accepted_result) -> None:
    data = accepted_result.package.commands[0].model_dump(mode="json")
    data["order"] = 2
    data["command_SHA256"] = hgh._command_digest_from_record(
        _without(data, "command_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffCommand.model_validate(data)


def test_command_cannot_authorize_automatic_execution(accepted_result) -> None:
    data = accepted_result.package.commands[0].model_dump(mode="json")
    data["automatic_execution_authorized"] = True
    data["command_SHA256"] = hgh._command_digest_from_record(
        _without(data, "command_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffCommand.model_validate(data)


def test_verification_step_digest_tampering_fails(accepted_result) -> None:
    data = accepted_result.package.verification_steps[0].model_dump(mode="json")
    data["step_SHA256"] = p17_6.digest_text("tamper")
    with pytest.raises(ValidationError):
        GitHandoffVerificationStep.model_validate(data)


def test_verification_step_order_must_match_identifier(accepted_result) -> None:
    data = accepted_result.package.verification_steps[0].model_dump(mode="json")
    data["order"] = 2
    data["step_SHA256"] = hgh._verification_step_digest_from_record(
        _without(data, "step_SHA256")
    )
    with pytest.raises(ValidationError):
        GitHandoffVerificationStep.model_validate(data)


def test_render_validation_rejects_tampered_package(accepted_result) -> None:
    package = accepted_result.package.model_copy(
        update={"package_SHA256": p17_6.digest_text("tamper")}
    )
    with pytest.raises(HumanGitHandoffValidationError):
        render_human_git_handoff_powershell(package)


def test_validate_request_rejects_non_request() -> None:
    with pytest.raises(HumanGitHandoffInputError):
        validate_human_git_handoff_request(object())


def test_build_rejects_non_request() -> None:
    with pytest.raises(HumanGitHandoffInputError):
        build_human_git_handoff(object())


def test_validate_result_rejects_non_result() -> None:
    with pytest.raises(HumanGitHandoffValidationError):
        validate_human_git_handoff_result(object())


def test_render_rejects_non_package() -> None:
    with pytest.raises(AttributeError):
        render_human_git_handoff_powershell(object())


def test_serialized_result_excludes_raw_runtime_evidence(accepted_result) -> None:
    payload = accepted_result.model_dump_json().lower()
    for forbidden in (
        "raw diff",
        "diff --git",
        "file content",
        "raw stdout",
        "raw stderr",
        "traceback",
        "authorization: bearer",
        "client_secret",
        "api_key",
    ):
        assert forbidden not in payload


@pytest.mark.parametrize(
    "operation",
    (
        "subprocess_launches",
        "shell_calls",
        "process_launches",
        "threads_created",
        "filesystem_reads",
        "filesystem_writes",
        "workspace_inspections",
        "environment_reads",
        "network_calls",
        "provider_calls",
        "model_calls",
        "Git_commands_executed",
        "Docker_calls",
        "Graphify_calls",
        "cleanup_calls",
        "rollback_calls",
        "automatic_staging",
        "automatic_commit",
        "automatic_push",
    ),
)
def test_authority_boundary_has_no_operational_execution(
    accepted_result, operation: str
) -> None:
    assert accepted_result.Git_commands_executed == 0
    assert accepted_result.staging_performed is False
    assert accepted_result.commit_performed is False
    assert accepted_result.push_performed is False
    assert accepted_result.automatic_cleanup_authorized is False
    assert accepted_result.automatic_rollback_authorized is False
    assert accepted_result.automatic_staging_authorized is False
    assert accepted_result.automatic_commit_authorized is False
    assert accepted_result.automatic_push_authorized is False
    assert accepted_result.provider_dispatch_count == 0
    assert accepted_result.model_inference_count == 0
    assert operation


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_no_forbidden_public_schema_shapes(model_cls: type[BaseModel]) -> None:
    schema_text = str(model_cls.model_json_schema()).lower()
    for forbidden in ("datetime", "uuid", "pathlib", "callable"):
        assert forbidden not in schema_text


def test_handoff_id_and_package_id_shapes(accepted_result) -> None:
    assert accepted_result.handoff_id.startswith("HGR-")
    assert accepted_result.package.package_id.startswith("GHP-")
    assert accepted_result.handoff_id.endswith(accepted_result.handoff_id[-12:])
    assert len(accepted_result.result_SHA256) == 64


def test_digest_is_not_signature(accepted_result) -> None:
    assert "signature" not in accepted_result.model_dump_json().lower()
    assert "private" not in accepted_result.model_dump_json().lower()
