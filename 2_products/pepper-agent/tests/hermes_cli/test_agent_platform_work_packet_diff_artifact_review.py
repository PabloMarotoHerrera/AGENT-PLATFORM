import re
import sys
from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError

import hermes_cli.agent_platform.work_packet as work_packet
import hermes_cli.agent_platform.work_packet.diff_artifact_review as dar
from hermes_cli.agent_platform.work_packet import (
    DIFF_ARTIFACT_REVIEW_POLICY_ID,
    DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION,
    AggregateReviewState,
    ArtifactReviewVerdict,
    DiffArtifactReviewError,
    DiffArtifactReviewInputError,
    DiffArtifactReviewIntegrityError,
    DiffArtifactReviewObservation,
    DiffArtifactReviewPolicyError,
    DiffArtifactReviewRequest,
    DiffArtifactReviewResult,
    DiffArtifactReviewStateError,
    DiffArtifactReviewValidationError,
    DiffReviewVerdict,
    ReviewArtifactDisposition,
    ReviewArtifactKind,
    ReviewArtifactObservation,
    ReviewArtifactOrigin,
    ReviewDiffStat,
    ReviewExpectedMutation,
    ReviewFinding,
    ReviewFindingCode,
    ReviewFindingSeverity,
    ReviewObservedPath,
    ReviewObservedPathStatus,
    ReviewPathExpectation,
    ToolPermissionOperation,
    ValidationCommandAuthorizationRequest,
    ValidationCommandExecutionRequest,
    ValidationCommandRunnerRequest,
    build_diff_artifact_review,
    build_review_expected_mutations,
    build_single_agent_execution_authorization,
    build_single_agent_runtime_binding,
    build_validation_command_runner_authorization,
    build_validation_command_runtime_binding,
    complete_single_agent_execution,
    complete_validation_command_runner,
    execute_single_agent_tool_action,
    execute_validation_command,
    prepare_single_agent_execution,
    prepare_validation_command_runner,
    validate_diff_artifact_review_result,
)
from hermes_cli.agent_platform.work_packet import outcome_envelopes
from hermes_cli.agent_platform.work_packet.single_agent_execution import (
    SingleAgentActionExecutionRequest,
    SingleAgentExecutionRequest,
)
from tests.hermes_cli import test_agent_platform_work_packet_outcome_envelopes as p17_5
from tests.hermes_cli.test_agent_platform_work_packet_compiler import (
    build_bundle,
    scope as compiler_scope,
    sha256_text,
    ticket as compiler_ticket,
    validation_step,
)
from tests.hermes_cli.test_agent_platform_work_packet_single_agent_execution import (
    action as single_action,
    allocation_result,
    plan as single_plan,
    profile_result,
)


P17_6_EXPORTS = (
    "DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION",
    "DIFF_ARTIFACT_REVIEW_POLICY_ID",
    "ReviewObservedPathStatus",
    "ReviewPathExpectation",
    "ReviewArtifactKind",
    "ReviewArtifactOrigin",
    "ReviewArtifactDisposition",
    "ReviewFindingSeverity",
    "ReviewFindingCode",
    "DiffReviewVerdict",
    "ArtifactReviewVerdict",
    "AggregateReviewState",
    "ReviewExpectedMutation",
    "ReviewObservedPath",
    "ReviewDiffStat",
    "ReviewArtifactObservation",
    "ReviewFinding",
    "DiffArtifactReviewObservation",
    "DiffArtifactReviewRequest",
    "DiffArtifactReviewResult",
    "DiffArtifactReviewError",
    "DiffArtifactReviewInputError",
    "DiffArtifactReviewIntegrityError",
    "DiffArtifactReviewPolicyError",
    "DiffArtifactReviewStateError",
    "DiffArtifactReviewValidationError",
    "build_review_expected_mutations",
    "build_diff_artifact_review",
    "validate_diff_artifact_review_result",
)
FORBIDDEN_PUBLIC_NAMES = (
    "inspect_workspace",
    "inspect_diff",
    "inspect_artifacts",
    "run_git_status",
    "run_git_diff",
    "clean_workspace",
    "rollback_workspace",
    "stage_reviewed_files",
    "commit_reviewed_files",
    "push_reviewed_files",
    "DiffReviewer",
    "ArtifactReviewer",
    "GitReviewer",
    "CleanupManager",
    "RollbackManager",
    "StagingManager",
)
PUBLIC_MODELS = (
    ReviewExpectedMutation,
    ReviewObservedPath,
    ReviewDiffStat,
    ReviewArtifactObservation,
    ReviewFinding,
    DiffArtifactReviewObservation,
    DiffArtifactReviewRequest,
    DiffArtifactReviewResult,
)
CONTROLLED_ENUMS = (
    ReviewObservedPathStatus,
    ReviewPathExpectation,
    ReviewArtifactKind,
    ReviewArtifactOrigin,
    ReviewArtifactDisposition,
    ReviewFindingSeverity,
    ReviewFindingCode,
    DiffReviewVerdict,
    ArtifactReviewVerdict,
    AggregateReviewState,
)
EXPECTED_ENUM_VALUES = (
    (
        ReviewObservedPathStatus,
        (
            "added",
            "modified",
            "deleted",
            "renamed",
            "type_changed",
            "unmerged",
            "untracked",
        ),
    ),
    (ReviewPathExpectation, ("expected", "unexpected", "missing_expected")),
    (
        ReviewArtifactKind,
        (
            "source",
            "test",
            "documentation",
            "configuration",
            "manifest",
            "generated",
            "log",
            "report",
            "binary",
            "cache",
            "temporary",
            "unknown",
        ),
    ),
    (
        ReviewArtifactOrigin,
        (
            "work_packet_declared",
            "execution_produced",
            "validation_produced",
            "human_declared",
            "unknown",
        ),
    ),
    (
        ReviewArtifactDisposition,
        ("acceptable", "requires_human_review", "prohibited", "unexpected"),
    ),
    (ReviewFindingSeverity, ("info", "warning", "blocking")),
    (
        ReviewFindingCode,
        (
            "expected_path_observed",
            "expected_path_missing",
            "unexpected_path_observed",
            "path_outside_workspace",
            "path_outside_repository",
            "git_metadata_path",
            "forbidden_path_component",
            "prohibited_artifact_kind",
            "unknown_artifact_origin",
            "artifact_requires_review",
            "artifact_unexpected",
            "hash_evidence_missing",
            "diff_summary_inconsistent",
            "outcome_not_terminal",
        ),
    ),
    (DiffReviewVerdict, ("accepted", "requires_human_review", "blocked")),
    (ArtifactReviewVerdict, ("accepted", "requires_human_review", "blocked")),
    (AggregateReviewState, ("completed", "blocked")),
)
FORBIDDEN_ENUM_VALUES = (
    "auto_accepted",
    "auto_cleaned",
    "auto_removed",
    "auto_rolled_back",
    "staged",
    "committed",
    "pushed",
)
INVALID_PATHS = (
    "",
    "/absolute/path.py",
    "C:/absolute/path.py",
    "src\\file.py",
    "../file.py",
    "src/./file.py",
    "src//file.py",
    "src/file.py/",
    "src/\x00file.py",
    "src/\nfile.py",
    "src/\rfile.py",
    ".git/config",
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
_AUTO_CONTENT_SHA = object()


def digest_text(value: str) -> str:
    return sha256_text(value)


def compilation_result(
    *,
    commands=("python -m unittest --help", None),
    docs_artifact_kind: str = "documentation",
):
    source_ticket = compiler_ticket(
        ticket_id="P17.6",
        ticket_scope=compiler_scope(
            allowed_paths=("docs/new.md", "src/existing.py", "tests/old_test.py"),
            forbidden_paths=("secrets/**",),
            allowed_actions=(
                f"create_file:docs/new.md|{docs_artifact_kind}",
                "modify_file:src/existing.py|source",
                "delete_file:tests/old_test.py|test",
            ),
        ),
        tasks=(
            "Create expected documentation artifact.",
            "Modify expected source artifact.",
            "Delete expected obsolete test artifact.",
        ),
        validation_steps=tuple(
            validation_step(f"V{index}", command=command)
            for index, command in enumerate(commands, start=1)
        ),
    )
    return build_bundle(source_ticket=source_ticket)["result"]


def terminal_context(
    monkeypatch: pytest.MonkeyPatch,
    workspace_root,
    *,
    kind="result",
    docs_artifact_kind: str = "documentation",
):
    compilation = compilation_result(
        commands=("python -m unittest no_such_test", None)
        if kind == "failure"
        else ("python -m unittest --help", None),
        docs_artifact_kind=docs_artifact_kind,
    )
    (workspace_root / "docs").mkdir(parents=True, exist_ok=True)
    (workspace_root / "src").mkdir(parents=True, exist_ok=True)
    (workspace_root / "tests").mkdir(parents=True, exist_ok=True)
    (workspace_root / "src" / "existing.py").write_bytes(b"old source\n")
    (workspace_root / "tests" / "old_test.py").write_bytes(b"old test\n")
    allocated, status_state = allocation_result(
        monkeypatch, compilation, workspace_root
    )
    permissions = profile_result(compilation, allocated)
    single_binding = build_single_agent_runtime_binding(
        agent_id="agent.p17-6",
        worker_id="worker.p17-6",
        work_packet=compilation.work_packet,
    )
    execution_plan = single_plan((
        single_action(
            1,
            "TASK-001",
            ToolPermissionOperation.CREATE_FILE,
            "docs/new.md",
            content="new docs",
        ),
        single_action(
            2,
            "TASK-002",
            ToolPermissionOperation.REPLACE_FILE,
            "src/existing.py",
            content="new source",
            expected=digest_text("old source\n"),
        ),
        single_action(
            3,
            "TASK-003",
            ToolPermissionOperation.DELETE_FILE,
            "tests/old_test.py",
            expected=digest_text("old test\n"),
        ),
    ))
    execution_authorization = build_single_agent_execution_authorization(
        authorizer_id="execution.authorizer.p17-6",
        authorization_reference="AUTH-P17-6-EXECUTION",
        rationale="Authorize synthetic P17.6 prerequisite execution.",
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=single_binding,
        plan=execution_plan,
        risk_acknowledgement="Synthetic filesystem mutation risk acknowledged.",
    )
    single_request = SingleAgentExecutionRequest(
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        runtime_binding=single_binding,
        plan=execution_plan,
        execution_authorization=execution_authorization,
    )
    session = prepare_single_agent_execution(single_request)
    for index in range(len(execution_plan.actions)):
        action_result = execute_single_agent_tool_action(
            SingleAgentActionExecutionRequest(
                execution_request=single_request,
                session=session,
            )
        )
        session = action_result.updated_session
        if index == 0:
            status_state["status"] = " M docs/new.md"
    single_result = complete_single_agent_execution(session)
    runtime = build_validation_command_runtime_binding(
        python_executable=sys.executable,
        allocation_result=allocated,
    )
    command_steps = tuple(
        step
        for step in compilation.work_packet.validation_steps
        if step.command is not None
    )
    authorization_requests = tuple(
        ValidationCommandAuthorizationRequest(
            validation_id=step.validation_id,
            timeout_seconds=30,
            expected_exit_codes=(0,),
        )
        for step in command_steps
    )
    runner_authorization = build_validation_command_runner_authorization(
        authorizer_id="validation.authorizer.p17-6",
        authorization_reference="AUTH-P17-6-VALIDATION",
        rationale="Authorize exact synthetic validation commands.",
        risk_acknowledgement="Authorized validation code may have side effects.",
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        single_agent_execution_result=single_result,
        runtime_binding=runtime,
        authorization_requests=authorization_requests,
    )
    runner_request = ValidationCommandRunnerRequest(
        compilation_result=compilation,
        allocation_result=allocated,
        profile_result=permissions,
        single_agent_execution_result=single_result,
        runtime_binding=runtime,
        runner_authorization=runner_authorization,
    )
    runner_session = prepare_validation_command_runner(runner_request)
    if kind == "cancellation":
        runner_result = execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=runner_request,
                session=runner_session,
                cancellation_requested=True,
                cancellation_reference="CANCEL-P17-6",
            )
        )
        outcome_request = outcome_envelopes._outcome_request(
            single_agent_execution_result=single_result,
            validation_command_runner_session=runner_result.updated_session,
            cancellation_reference="CANCEL-P17-6",
        )
    elif kind == "failure":
        runner_result = execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=runner_request,
                session=runner_session,
            )
        )
        outcome_request = outcome_envelopes._outcome_request(
            single_agent_execution_result=single_result,
            validation_command_runner_session=runner_result.updated_session,
        )
    else:
        first = execute_validation_command(
            ValidationCommandExecutionRequest(
                runner_request=runner_request,
                session=runner_session,
            )
        )
        runner_completed = complete_validation_command_runner(first.updated_session)
        outcome_request = outcome_envelopes._outcome_request(
            single_agent_execution_result=single_result,
            validation_command_runner_result=runner_completed,
        )
    return {
        "compilation": compilation,
        "allocation": allocated,
        "profile": permissions,
        "outcome": outcome_envelopes.build_outcome_envelope(outcome_request),
    }


@pytest.fixture(scope="module")
def contexts(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("p17_6")
    try:
        return {
            "result": terminal_context(monkeypatch, root / "result", kind="result"),
            "failure": terminal_context(monkeypatch, root / "failure", kind="failure"),
            "cancellation": terminal_context(
                monkeypatch, root / "cancellation", kind="cancellation"
            ),
            "monkeypatch": monkeypatch,
        }
    finally:
        monkeypatch.undo()


def observed_path(
    index: int,
    path: str,
    status: ReviewObservedPathStatus,
    *,
    tracked: bool | None = None,
    staged: bool = False,
    bytes_after: int | None = 10,
    content_sha: str | None = None,
    artifact_declared: bool = True,
) -> ReviewObservedPath:
    if tracked is None:
        tracked = status is not ReviewObservedPathStatus.UNTRACKED
    if status is ReviewObservedPathStatus.DELETED:
        bytes_after = None
        content_sha = None
    elif content_sha is None:
        content_sha = digest_text(path)
    data = {
        "observation_id": f"OPATH-{index:03d}",
        "relative_path": path,
        "status": status,
        "tracked": tracked,
        "staged": staged,
        "bytes_after": bytes_after,
        "content_SHA256": content_sha,
        "artifact_declared": artifact_declared,
    }
    return ReviewObservedPath(
        **data,
        observation_SHA256=dar._observed_path_digest_from_record(data),
    )


def artifact(
    index: int,
    path: str,
    kind: ReviewArtifactKind,
    *,
    origin: ReviewArtifactOrigin = ReviewArtifactOrigin.HUMAN_DECLARED,
    disposition: ReviewArtifactDisposition = ReviewArtifactDisposition.ACCEPTABLE,
    expected: bool = True,
    content_sha: str | None | object = _AUTO_CONTENT_SHA,
    bytes_after: int | None = 10,
    source_action_id: str | None = "ACTION-001",
    source_command_id: str | None = None,
    source_validation_id: str | None = None,
    rationale: str = "Synthetic artifact observation.",
) -> ReviewArtifactObservation:
    if content_sha is _AUTO_CONTENT_SHA:
        content_sha = digest_text(path)
    data = {
        "artifact_id": f"ARTF-{index:03d}",
        "relative_path": path,
        "kind": kind,
        "origin": origin,
        "disposition": disposition,
        "expected": expected,
        "content_SHA256": content_sha,
        "bytes_after": bytes_after,
        "source_action_id": source_action_id,
        "source_command_id": source_command_id,
        "source_validation_id": source_validation_id,
        "rationale": rationale,
    }
    return ReviewArtifactObservation(
        **data,
        artifact_SHA256=dar._artifact_digest_from_record(data),
    )


def observation(
    context, paths, artifacts=(), **updates
) -> DiffArtifactReviewObservation:
    allocation = context["allocation"].allocation
    data = {
        "schema_version": DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION,
        "observation_reference": "HUMAN-OBS-P17-6",
        "human_observer_id": "observer.p17-6",
        "synthetic": False,
        "repository_identity": allocation.repository_identity,
        "workspace_root_binding_SHA256": allocation.allocation_SHA256,
        "source_commit": allocation.repository_identity.source_commit,
        "branch_name": allocation.repository_identity.workspace_branch,
        "index_empty": True,
        "staged_file_count": 0,
        "observed_paths": tuple(paths),
        "artifacts": tuple(artifacts),
        "diff_stat": dar._build_diff_stat(tuple(paths)),
    }
    data.update(updates)
    return DiffArtifactReviewObservation(
        **data,
        observation_SHA256=dar._observation_digest_from_record(data),
    )


def request(context, obs) -> DiffArtifactReviewRequest:
    return DiffArtifactReviewRequest(
        compilation_result=context["compilation"],
        allocation_result=context["allocation"],
        profile_result=context["profile"],
        outcome_envelope=context["outcome"],
        observation=obs,
    )


def unsafe_request(context, obs) -> DiffArtifactReviewRequest:
    return DiffArtifactReviewRequest.model_construct(
        schema_version=DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION,
        policy_id=DIFF_ARTIFACT_REVIEW_POLICY_ID,
        compilation_result=context["compilation"],
        allocation_result=context["allocation"],
        profile_result=context["profile"],
        outcome_envelope=context["outcome"],
        observation=obs,
    )


def canonical_paths() -> tuple[ReviewObservedPath, ...]:
    return (
        observed_path(
            1, "docs/new.md", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
        observed_path(2, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
        observed_path(3, "tests/old_test.py", ReviewObservedPathStatus.DELETED),
    )


def canonical_artifacts() -> tuple[ReviewArtifactObservation, ...]:
    return (
        artifact(1, "docs/new.md", ReviewArtifactKind.DOCUMENTATION),
        artifact(
            2,
            "src/existing.py",
            ReviewArtifactKind.SOURCE,
            source_action_id="ACTION-002",
        ),
        artifact(
            3,
            "tests/old_test.py",
            ReviewArtifactKind.TEST,
            content_sha=None,
            bytes_after=None,
            source_action_id="ACTION-003",
        ),
    )


def expected_doc_mutation(kind: ReviewArtifactKind) -> ReviewExpectedMutation:
    data = {
        "mutation_id": "EMUT-001",
        "relative_path": "docs/new.md",
        "allowed_statuses": (
            ReviewObservedPathStatus.ADDED,
            ReviewObservedPathStatus.UNTRACKED,
        ),
        "artifact_expected": True,
        "expected_artifact_kind": kind,
        "source_action_id": "ACTION-001",
    }
    return ReviewExpectedMutation(
        **data,
        expectation_SHA256=dar._expected_mutation_digest_from_record(data),
    )


def artifact_policy_findings(
    kind: ReviewArtifactKind,
    *,
    disposition: ReviewArtifactDisposition,
    origin: ReviewArtifactOrigin = ReviewArtifactOrigin.HUMAN_DECLARED,
    source_action_id: str | None = "ACTION-001",
    source_command_id: str | None = None,
) -> tuple[ArtifactReviewVerdict, tuple[ReviewFinding, ...]]:
    paths = (
        observed_path(
            1,
            "docs/new.md",
            ReviewObservedPathStatus.UNTRACKED,
            tracked=False,
        ),
    )
    findings = dar._derive_findings(
        expected_mutations=(expected_doc_mutation(kind),),
        observed_paths=paths,
        artifacts=(
            artifact(
                1,
                "docs/new.md",
                kind,
                origin=origin,
                disposition=disposition,
                source_action_id=source_action_id,
                source_command_id=source_command_id,
            ),
        ),
    )
    return dar._derive_artifact_verdict(findings), findings


@pytest.fixture()
def canonical_result(contexts):
    obs = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    return build_diff_artifact_review(request(contexts["result"], obs))


@pytest.fixture()
def sample_models(contexts, canonical_result):
    obs = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    req = request(contexts["result"], obs)
    return {
        ReviewExpectedMutation.__name__: canonical_result.expected_mutations[0],
        ReviewObservedPath.__name__: canonical_paths()[0],
        ReviewDiffStat.__name__: dar._build_diff_stat(canonical_paths()),
        ReviewArtifactObservation.__name__: canonical_artifacts()[0],
        ReviewFinding.__name__: canonical_result.findings[0],
        DiffArtifactReviewObservation.__name__: obs,
        DiffArtifactReviewRequest.__name__: req,
        DiffArtifactReviewResult.__name__: canonical_result,
    }


@pytest.mark.parametrize("exported_name", P17_6_EXPORTS)
def test_all_p17_6_exports_exist(exported_name: str) -> None:
    assert hasattr(work_packet, exported_name)
    assert hasattr(dar, exported_name)


def test_prior_172_exports_remain_exact_prefix() -> None:
    prior = (
        p17_5.P17_0_EXPORTS
        + p17_5.P17_1_EXPORTS
        + p17_5.P17_2_EXPORTS
        + p17_5.P17_3_EXPORTS
        + p17_5.P17_4_EXPORTS
        + p17_5.P17_5_EXPORTS
    )
    assert len(prior) == 172
    assert work_packet.__all__[:172] == prior
    assert work_packet.__all__[172:] == P17_6_EXPORTS
    assert len(work_packet.__all__) == 201
    assert len(set(work_packet.__all__)) == 201
    assert not any(name.startswith("_") for name in work_packet.__all__)


@pytest.mark.parametrize("name", FORBIDDEN_PUBLIC_NAMES)
def test_forbidden_public_names_absent(name: str) -> None:
    assert not hasattr(work_packet, name)
    assert not hasattr(dar, name)


def test_import_smoke_exact_output() -> None:
    assert (
        len(work_packet.__all__),
        len(set(work_packet.__all__)),
        hasattr(work_packet, "DiffArtifactReviewResult"),
        hasattr(work_packet, "build_diff_artifact_review"),
        hasattr(work_packet, "inspect_workspace"),
        hasattr(work_packet, "DiffReviewer"),
    ) == (201, 201, True, True, False, False)


def test_function_import_smoke_exact_output() -> None:
    assert (
        build_review_expected_mutations.__name__,
        build_diff_artifact_review.__name__,
        validate_diff_artifact_review_result.__name__,
    ) == (
        "build_review_expected_mutations",
        "build_diff_artifact_review",
        "validate_diff_artifact_review_result",
    )


@pytest.mark.parametrize(
    "error_cls",
    (
        DiffArtifactReviewError,
        DiffArtifactReviewInputError,
        DiffArtifactReviewIntegrityError,
        DiffArtifactReviewPolicyError,
        DiffArtifactReviewStateError,
        DiffArtifactReviewValidationError,
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


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_alternative_schema_versions_fail(
    model_cls: type[BaseModel], sample_models
) -> None:
    model = sample_models[model_cls.__name__]
    if "schema_version" not in model.model_fields:
        data = model.model_dump(mode="json")
        data["schema_version"] = 2
        with pytest.raises(ValidationError):
            model_cls.model_validate(data)
        return
    data = model.model_dump(mode="json")
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize(
    "model_cls", (DiffArtifactReviewRequest, DiffArtifactReviewResult)
)
def test_alternative_policy_ids_fail(model_cls: type[BaseModel], sample_models) -> None:
    data = sample_models[model_cls.__name__].model_dump(mode="json")
    data["policy_id"] = "alternate-policy"
    with pytest.raises(ValidationError):
        model_cls.model_validate(data)


@pytest.mark.parametrize(
    "field,value",
    (
        ("tracked", "true"),
        ("staged", "false"),
        ("artifact_declared", "true"),
    ),
)
def test_strict_booleans_reject_strings(field: str, value: str) -> None:
    data = observed_path(1, "docs/new.md", ReviewObservedPathStatus.ADDED).model_dump(
        mode="json"
    )
    data[field] = value
    data["observation_SHA256"] = dar._observed_path_digest_from_record({
        k: v for k, v in data.items() if k != "observation_SHA256"
    })
    with pytest.raises(ValidationError):
        ReviewObservedPath.model_validate(data)


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


@pytest.mark.parametrize("value", FORBIDDEN_ENUM_VALUES)
def test_forbidden_enum_values_absent(value: str) -> None:
    for enum_cls in CONTROLLED_ENUMS:
        assert value not in {item.value for item in enum_cls}


def test_schema_and_policy_identity() -> None:
    assert DIFF_ARTIFACT_REVIEW_SCHEMA_VERSION == 1
    assert DIFF_ARTIFACT_REVIEW_POLICY_ID == (
        "pepper-human-observed-deterministic-diff-artifact-review-v1"
    )


def test_expected_mutations_derive_from_work_packet(contexts) -> None:
    expected = build_review_expected_mutations(contexts["result"]["compilation"])
    assert tuple(item.mutation_id for item in expected) == (
        "EMUT-001",
        "EMUT-002",
        "EMUT-003",
    )
    assert tuple(item.relative_path for item in expected) == (
        "docs/new.md",
        "src/existing.py",
        "tests/old_test.py",
    )
    assert expected[0].allowed_statuses == (
        ReviewObservedPathStatus.ADDED,
        ReviewObservedPathStatus.UNTRACKED,
    )
    assert expected[1].allowed_statuses == (ReviewObservedPathStatus.MODIFIED,)
    assert expected[2].allowed_statuses == (ReviewObservedPathStatus.DELETED,)
    assert tuple(item.source_action_id for item in expected) == (
        "ACTION-001",
        "ACTION-002",
        "ACTION-003",
    )


def test_natural_language_only_path_inference_absent() -> None:
    source_ticket = compiler_ticket(
        ticket_id="P17.6",
        ticket_scope=compiler_scope(
            allowed_paths=("src/inferred.py",),
            allowed_actions=("Please edit src/inferred.py",),
        ),
    )
    result = build_bundle(source_ticket=source_ticket)["result"]
    assert build_review_expected_mutations(result) == ()


def test_duplicate_expected_mutation_path_fails() -> None:
    source_ticket = compiler_ticket(
        ticket_id="P17.6",
        ticket_scope=compiler_scope(
            allowed_paths=("docs/new.md",),
            allowed_actions=(
                "create_file:docs/new.md|documentation",
                "modify_file:docs/new.md|documentation",
            ),
        ),
    )
    result = build_bundle(source_ticket=source_ticket)["result"]
    with pytest.raises(DiffArtifactReviewPolicyError):
        build_review_expected_mutations(result)


@pytest.mark.parametrize(
    "path", ("src/file.py", "docs/nested/file.md", "tests/test_file.py")
)
def test_valid_relative_paths_pass(path: str) -> None:
    assert observed_path(1, path, ReviewObservedPathStatus.ADDED).relative_path == path


@pytest.mark.parametrize("path", INVALID_PATHS)
def test_invalid_paths_fail(path: str) -> None:
    with pytest.raises(ValidationError):
        observed_path(1, path, ReviewObservedPathStatus.ADDED)


@pytest.mark.parametrize("status", ReviewObservedPathStatus)
def test_observed_path_statuses_construct(status: ReviewObservedPathStatus) -> None:
    path = observed_path(
        1,
        "src/file.py",
        status,
        tracked=status is not ReviewObservedPathStatus.UNTRACKED,
    )
    assert path.status is status


@pytest.mark.parametrize(
    "status,tracked",
    (
        (ReviewObservedPathStatus.UNTRACKED, True),
        (ReviewObservedPathStatus.MODIFIED, False),
        (ReviewObservedPathStatus.ADDED, False),
        (ReviewObservedPathStatus.DELETED, False),
    ),
)
def test_invalid_tracked_status_combinations_fail(status, tracked) -> None:
    with pytest.raises(ValidationError):
        observed_path(1, "src/file.py", status, tracked=tracked)


def test_staged_path_fails() -> None:
    with pytest.raises(ValidationError):
        observed_path(1, "src/file.py", ReviewObservedPathStatus.MODIFIED, staged=True)


def test_deleted_path_with_content_evidence_fails() -> None:
    data = {
        "observation_id": "OPATH-001",
        "relative_path": "src/deleted.py",
        "status": ReviewObservedPathStatus.DELETED,
        "tracked": True,
        "staged": False,
        "bytes_after": 5,
        "content_SHA256": digest_text("x"),
        "artifact_declared": True,
    }
    with pytest.raises(ValidationError):
        ReviewObservedPath(
            **data, observation_SHA256=dar._observed_path_digest_from_record(data)
        )


def test_nondeleted_path_without_bytes_fails() -> None:
    with pytest.raises(ValidationError):
        observed_path(
            1, "src/file.py", ReviewObservedPathStatus.MODIFIED, bytes_after=None
        )


def test_observed_path_digest_tampering_fails() -> None:
    data = observed_path(
        1, "src/file.py", ReviewObservedPathStatus.MODIFIED
    ).model_dump(mode="json")
    data["observation_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        ReviewObservedPath.model_validate(data)


def test_observation_ids_must_be_contiguous(contexts) -> None:
    paths = (
        observed_path(1, "docs/new.md", ReviewObservedPathStatus.ADDED),
        observed_path(3, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
    )
    with pytest.raises(ValidationError):
        observation(contexts["result"], paths)


def test_observation_paths_must_be_sorted(contexts) -> None:
    paths = (
        observed_path(1, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
        observed_path(2, "docs/new.md", ReviewObservedPathStatus.ADDED),
    )
    with pytest.raises(ValidationError):
        observation(contexts["result"], paths)


def test_duplicate_observed_path_fails(contexts) -> None:
    paths = (
        observed_path(1, "docs/new.md", ReviewObservedPathStatus.ADDED),
        observed_path(2, "docs/new.md", ReviewObservedPathStatus.MODIFIED),
    )
    with pytest.raises(ValidationError):
        observation(contexts["result"], paths)


def test_raw_file_content_field_rejected() -> None:
    data = observed_path(
        1, "src/file.py", ReviewObservedPathStatus.MODIFIED
    ).model_dump(mode="json")
    data["raw_content"] = "file body"
    with pytest.raises(ValidationError):
        ReviewObservedPath.model_validate(data)


def test_diff_stat_derives_counts() -> None:
    stat = dar._build_diff_stat(canonical_paths())
    assert stat.observed_path_count == 3
    assert stat.modified_count == 1
    assert stat.deleted_count == 1
    assert stat.untracked_count == 1
    assert stat.total_bytes_after == 20


@pytest.mark.parametrize(
    "field",
    (
        "observed_path_count",
        "added_count",
        "modified_count",
        "deleted_count",
        "renamed_count",
        "type_changed_count",
        "unmerged_count",
        "untracked_count",
        "total_bytes_after",
    ),
)
def test_negative_diff_stat_counts_fail(field: str) -> None:
    data = dar._build_diff_stat(canonical_paths()).model_dump(mode="json")
    data[field] = -1
    data["diff_stat_SHA256"] = dar._diff_stat_digest_from_record({
        k: v for k, v in data.items() if k != "diff_stat_SHA256"
    })
    with pytest.raises(ValidationError):
        ReviewDiffStat.model_validate(data)


def test_inconsistent_diff_stat_total_fails() -> None:
    data = dar._build_diff_stat(canonical_paths()).model_dump(mode="json")
    data["observed_path_count"] = 99
    data["diff_stat_SHA256"] = dar._diff_stat_digest_from_record({
        k: v for k, v in data.items() if k != "diff_stat_SHA256"
    })
    with pytest.raises(ValidationError):
        ReviewDiffStat.model_validate(data)


def test_diff_stat_digest_tampering_fails() -> None:
    data = dar._build_diff_stat(canonical_paths()).model_dump(mode="json")
    data["diff_stat_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        ReviewDiffStat.model_validate(data)


@pytest.mark.parametrize(
    "kind",
    (
        ReviewArtifactKind.SOURCE,
        ReviewArtifactKind.TEST,
        ReviewArtifactKind.DOCUMENTATION,
        ReviewArtifactKind.CONFIGURATION,
        ReviewArtifactKind.MANIFEST,
    ),
)
def test_expected_acceptable_artifact_kinds_pass(kind: ReviewArtifactKind) -> None:
    assert artifact(1, "docs/new.md", kind).kind is kind


@pytest.mark.parametrize(
    "kind",
    (
        ReviewArtifactKind.GENERATED,
        ReviewArtifactKind.LOG,
        ReviewArtifactKind.REPORT,
        ReviewArtifactKind.BINARY,
        ReviewArtifactKind.UNKNOWN,
    ),
)
def test_artifact_kinds_requiring_review_reject_acceptable_disposition(kind) -> None:
    with pytest.raises(ValidationError):
        artifact(1, "docs/new.md", kind)


@pytest.mark.parametrize(
    "kind", (ReviewArtifactKind.CACHE, ReviewArtifactKind.TEMPORARY)
)
def test_prohibited_artifact_kinds_require_prohibited_disposition(kind) -> None:
    with pytest.raises(ValidationError):
        artifact(1, "docs/new.md", kind)
    assert (
        artifact(
            1,
            "docs/new.md",
            kind,
            disposition=ReviewArtifactDisposition.PROHIBITED,
        ).disposition
        is ReviewArtifactDisposition.PROHIBITED
    )


def test_unknown_origin_cannot_be_acceptable() -> None:
    with pytest.raises(ValidationError):
        artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.SOURCE,
            origin=ReviewArtifactOrigin.UNKNOWN,
        )


def test_execution_artifact_requires_source_action() -> None:
    with pytest.raises(ValidationError):
        artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.SOURCE,
            origin=ReviewArtifactOrigin.EXECUTION_PRODUCED,
            source_action_id=None,
        )


def test_validation_artifact_requires_source_command_or_validation() -> None:
    with pytest.raises(ValidationError):
        artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.SOURCE,
            origin=ReviewArtifactOrigin.VALIDATION_PRODUCED,
            source_action_id=None,
        )


@pytest.mark.parametrize(
    "rationale",
    (
        "line\nbreak",
        "line\rbreak",
        "access_token=value",
        "Authorization: Bearer tokenvalue",
        "raw stdout dump",
        "C:/Users/example/path",
    ),
)
def test_unsafe_artifact_rationale_fails(rationale: str) -> None:
    with pytest.raises(ValidationError):
        artifact(1, "docs/new.md", ReviewArtifactKind.SOURCE, rationale=rationale)


def test_artifact_rationale_length_is_bounded() -> None:
    with pytest.raises(ValidationError):
        artifact(1, "docs/new.md", ReviewArtifactKind.SOURCE, rationale="x" * 513)


def test_artifact_path_absent_from_observation_fails(contexts) -> None:
    paths = (observed_path(1, "docs/new.md", ReviewObservedPathStatus.ADDED),)
    artifacts = (artifact(1, "src/missing.py", ReviewArtifactKind.SOURCE),)
    with pytest.raises(ValidationError):
        observation(contexts["result"], paths, artifacts)


def test_duplicate_artifact_path_fails(contexts) -> None:
    paths = canonical_paths()
    artifacts = (
        artifact(1, "docs/new.md", ReviewArtifactKind.DOCUMENTATION),
        artifact(2, "docs/new.md", ReviewArtifactKind.SOURCE),
    )
    with pytest.raises(ValidationError):
        observation(contexts["result"], paths, artifacts)


def test_artifact_digest_tampering_fails() -> None:
    data = artifact(1, "docs/new.md", ReviewArtifactKind.DOCUMENTATION).model_dump(
        mode="json"
    )
    data["artifact_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        ReviewArtifactObservation.model_validate(data)


def test_all_expected_observed_passes(contexts) -> None:
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], canonical_paths()))
    )
    assert result.diff_verdict is DiffReviewVerdict.ACCEPTED


def test_missing_expected_path_blocks(contexts) -> None:
    paths = canonical_paths()[:2]
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths))
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED
    assert any(
        f.code is ReviewFindingCode.EXPECTED_PATH_MISSING for f in result.findings
    )


def test_unexpected_observed_path_blocks(contexts) -> None:
    paths = canonical_paths() + (
        observed_path(
            4, "zz-unexpected.txt", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
    )
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths))
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED
    assert any(
        f.code is ReviewFindingCode.UNEXPECTED_PATH_OBSERVED for f in result.findings
    )


@pytest.mark.parametrize(
    "path", ("new.md", "nested/docs/new.md", "DOCS/new.md", "docs/*.md")
)
def test_exact_path_matching_required(contexts, path: str) -> None:
    paths = (
        observed_path(1, path, ReviewObservedPathStatus.UNTRACKED, tracked=False),
        observed_path(2, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
        observed_path(3, "tests/old_test.py", ReviewObservedPathStatus.DELETED),
    )
    paths = tuple(sorted(paths, key=lambda item: item.relative_path))
    paths = tuple(
        observed_path(index, item.relative_path, item.status, tracked=item.tracked)
        for index, item in enumerate(paths, start=1)
    )
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths))
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED


def test_expected_path_wrong_status_blocks(contexts) -> None:
    paths = (
        observed_path(1, "docs/new.md", ReviewObservedPathStatus.MODIFIED),
        observed_path(2, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
        observed_path(3, "tests/old_test.py", ReviewObservedPathStatus.DELETED),
    )
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths))
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED


def test_unmerged_path_blocks(contexts) -> None:
    paths = canonical_paths() + (
        observed_path(4, "zz-unmerged.txt", ReviewObservedPathStatus.UNMERGED),
    )
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths))
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED


def test_expected_path_creates_info_finding(canonical_result) -> None:
    assert any(
        f.code is ReviewFindingCode.EXPECTED_PATH_OBSERVED
        and f.severity is ReviewFindingSeverity.INFO
        for f in canonical_result.findings
    )


def test_generated_artifact_creates_warning(monkeypatch, tmp_path) -> None:
    ctx = terminal_context(
        monkeypatch,
        tmp_path / "generated",
        docs_artifact_kind=ReviewArtifactKind.GENERATED.value,
    )
    artifacts = (
        artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.GENERATED,
            disposition=ReviewArtifactDisposition.REQUIRES_HUMAN_REVIEW,
        ),
    )
    result = build_diff_artifact_review(
        request(ctx, observation(ctx, canonical_paths(), artifacts))
    )
    assert result.artifact_verdict is ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    assert any(f.severity is ReviewFindingSeverity.WARNING for f in result.findings)


def test_prohibited_artifact_creates_blocking_finding(contexts) -> None:
    artifacts = (
        artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.CACHE,
            disposition=ReviewArtifactDisposition.PROHIBITED,
        ),
    )
    result = build_diff_artifact_review(
        request(
            contexts["result"],
            observation(contexts["result"], canonical_paths(), artifacts),
        )
    )
    assert result.artifact_verdict is ArtifactReviewVerdict.BLOCKED
    assert any(
        f.code is ReviewFindingCode.PROHIBITED_ARTIFACT_KIND for f in result.findings
    )


def test_missing_artifact_hash_blocks(contexts) -> None:
    artifacts = (
        artifact(1, "docs/new.md", ReviewArtifactKind.DOCUMENTATION, content_sha=None),
    )
    result = build_diff_artifact_review(
        request(
            contexts["result"],
            observation(contexts["result"], canonical_paths(), artifacts),
        )
    )
    assert result.artifact_verdict is ArtifactReviewVerdict.BLOCKED
    assert any(
        f.code is ReviewFindingCode.HASH_EVIDENCE_MISSING for f in result.findings
    )


def test_finding_ids_and_order_are_deterministic(contexts) -> None:
    paths = canonical_paths() + (
        observed_path(
            4, "zz-unexpected.txt", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
    )
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths))
    )
    assert tuple(f.finding_id for f in result.findings) == tuple(
        f"FIND-{index:03d}" for index in range(1, len(result.findings) + 1)
    )
    assert result.findings == tuple(sorted(result.findings, key=dar._finding_sort_key))


@pytest.mark.parametrize(
    "summary",
    (
        "raw diff hunk",
        "file content snapshot",
        "client_secret=value",
        "C:/Users/example/path",
    ),
)
def test_unsafe_finding_summary_fails(summary: str) -> None:
    data = {
        "finding_id": "FIND-001",
        "severity": ReviewFindingSeverity.BLOCKING,
        "code": ReviewFindingCode.UNEXPECTED_PATH_OBSERVED,
        "relative_path": "src/file.py",
        "mutation_id": None,
        "artifact_id": None,
        "summary": summary,
        "failed_invariant": "unexpected path",
    }
    with pytest.raises(ValidationError):
        ReviewFinding(**data, finding_SHA256=dar._finding_digest_from_record(data))


def test_finding_digest_tampering_fails(canonical_result) -> None:
    data = canonical_result.findings[0].model_dump(mode="json")
    data["finding_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        ReviewFinding.model_validate(data)


def test_finding_maximum_bound_enforced(canonical_result) -> None:
    data = canonical_result.model_dump(mode="json")
    data["findings"] = [data["findings"][0]] * 129
    with pytest.raises(ValidationError):
        DiffArtifactReviewResult.model_validate(data)


@pytest.mark.parametrize("kind", ("result", "failure", "cancellation"))
def test_outcome_kind_requests_validate(contexts, kind: str) -> None:
    obs = observation(contexts[kind], canonical_paths())
    result = build_diff_artifact_review(request(contexts[kind], obs))
    assert result.outcome_kind is contexts[kind]["outcome"].envelope_kind


@pytest.mark.parametrize(
    "field",
    (
        "envelope_SHA256",
        "result_envelopes_ready",
        "diff_artifact_review_ready",
        "human_git_handoff_ready",
        "provider_dispatch_count",
        "model_inference_count",
    ),
)
def test_invalid_outcome_posture_fails(contexts, field: str) -> None:
    outcome = contexts["result"]["outcome"].model_dump(mode="json")
    if field == "envelope_SHA256":
        outcome[field] = digest_text("tamper")
    elif field == "result_envelopes_ready":
        outcome[field] = False
    elif field in {"diff_artifact_review_ready", "human_git_handoff_ready"}:
        outcome[field] = True
    else:
        outcome[field] = 1
    with pytest.raises((ValidationError, DiffArtifactReviewInputError)):
        bad_outcome = outcome_envelopes.OutcomeEnvelope.model_validate(outcome)
        build_diff_artifact_review(
            request(
                {**contexts["result"], "outcome": bad_outcome},
                observation(contexts["result"], canonical_paths()),
            )
        )


@pytest.mark.parametrize("binding", ("work_packet", "allocation", "profile"))
def test_cross_contract_binding_mismatch_fails(contexts, binding: str) -> None:
    ctx = dict(contexts["result"])
    if binding == "work_packet":
        work_packet = ctx["compilation"].work_packet.model_copy(
            update={"work_packet_id": "WP-P17-6-MISMATCH-R0001-aaaaaaaaaaaa"}
        )
        ctx["compilation"] = ctx["compilation"].model_copy(
            update={"work_packet": work_packet}
        )
    elif binding == "allocation":
        allocation = ctx["allocation"].allocation.model_copy(
            update={"work_packet_id": "different"}
        )
        ctx["allocation"] = ctx["allocation"].model_copy(
            update={"allocation": allocation}
        )
    else:
        profile = ctx["profile"].profile.model_copy(
            update={"allocation_id": "different"}
        )
        ctx["profile"] = ctx["profile"].model_copy(update={"profile": profile})
    with pytest.raises(DiffArtifactReviewInputError):
        build_diff_artifact_review(
            unsafe_request(ctx, observation(contexts["result"], canonical_paths()))
        )


@pytest.mark.parametrize(
    "field,value",
    (
        ("human_observer_id", "SHADOW-observer"),
        ("synthetic", True),
        ("workspace_root_binding_SHA256", digest_text("bad workspace")),
        ("source_commit", "b" * 40),
        ("branch_name", "other-branch"),
        ("index_empty", False),
        ("staged_file_count", 1),
        ("observation_reference", "line\nbreak"),
    ),
)
def test_invalid_human_observation_fails(contexts, field: str, value) -> None:
    if field in {"workspace_root_binding_SHA256", "source_commit", "branch_name"}:
        obs = observation(contexts["result"], canonical_paths(), **{field: value})
        with pytest.raises(ValidationError):
            request(contexts["result"], obs)
    else:
        with pytest.raises(ValidationError):
            observation(contexts["result"], canonical_paths(), **{field: value})


def test_observation_digest_tampering_fails(contexts) -> None:
    obs = observation(contexts["result"], canonical_paths())
    data = obs.model_dump(mode="json")
    data["observation_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        DiffArtifactReviewObservation.model_validate(data)


def test_repeated_equal_observations_are_equal(contexts) -> None:
    first = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    second = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    assert first == second
    assert first.observation_SHA256 == second.observation_SHA256


def test_canonical_exact_expected_diff_and_artifact_review_flow(contexts) -> None:
    obs = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    result = build_diff_artifact_review(request(contexts["result"], obs))
    assert len(result.expected_mutations) == 3
    assert result.diff_verdict is DiffReviewVerdict.ACCEPTED
    assert result.artifact_verdict is ArtifactReviewVerdict.ACCEPTED
    assert result.diff_artifact_review_requirement_satisfied is True
    assert result.human_git_handoff_ready is False
    assert result.automatic_cleanup_authorized is False
    assert result.automatic_rollback_authorized is False
    assert result.automatic_staging_authorized is False


def test_completed_review_preserves_pending_manual_validation(contexts) -> None:
    obs = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    result = build_diff_artifact_review(request(contexts["result"], obs))
    assert result.state is AggregateReviewState.COMPLETED
    assert result.manual_validation_ids_pending == ("V2",)


def test_completed_review_keeps_non_mutating_authority(canonical_result) -> None:
    assert canonical_result.diff_artifact_review_requirement_satisfied is True
    assert canonical_result.human_git_handoff_ready is False
    assert canonical_result.automatic_cleanup_authorized is False
    assert canonical_result.automatic_rollback_authorized is False
    assert canonical_result.automatic_staging_authorized is False
    assert canonical_result.provider_dispatch_count == 0
    assert canonical_result.model_inference_count == 0


def test_result_preserves_human_supplied_observation(contexts) -> None:
    obs = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    result = build_diff_artifact_review(request(contexts["result"], obs))
    assert result.observation_SHA256 == obs.observation_SHA256
    assert result.observed_paths == obs.observed_paths
    assert result.artifacts == obs.artifacts
    assert result.diff_stat == obs.diff_stat


def test_expected_path_matching_is_exact_not_prefix(contexts) -> None:
    paths = (
        observed_path(
            1,
            "docs/new.md.backup",
            ReviewObservedPathStatus.UNTRACKED,
            tracked=False,
        ),
        observed_path(2, "src/existing.py", ReviewObservedPathStatus.MODIFIED),
        observed_path(3, "tests/old_test.py", ReviewObservedPathStatus.DELETED),
    )
    artifacts = (
        artifact(1, "docs/new.md.backup", ReviewArtifactKind.DOCUMENTATION),
        canonical_artifacts()[1],
        canonical_artifacts()[2],
    )
    result = build_diff_artifact_review(
        request(contexts["result"], observation(contexts["result"], paths, artifacts))
    )
    assert any(
        finding.code is ReviewFindingCode.EXPECTED_PATH_MISSING
        and finding.relative_path == "docs/new.md"
        for finding in result.findings
    )
    assert any(
        finding.code is ReviewFindingCode.UNEXPECTED_PATH_OBSERVED
        and finding.relative_path == "docs/new.md.backup"
        for finding in result.findings
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED


def test_canonical_unexpected_path_blocks_review_flow(contexts) -> None:
    paths = canonical_paths() + (
        observed_path(
            4, "zz-unexpected.txt", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
    )
    obs = observation(contexts["result"], paths, canonical_artifacts())
    result = build_diff_artifact_review(request(contexts["result"], obs))
    assert (
        sum(
            f.code is ReviewFindingCode.UNEXPECTED_PATH_OBSERVED
            for f in result.findings
        )
        == 1
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED
    assert result.state is AggregateReviewState.BLOCKED
    assert result.diff_artifact_review_requirement_satisfied is False
    assert result.automatic_cleanup_authorized is False
    assert result.automatic_rollback_authorized is False
    assert result.automatic_staging_authorized is False


def test_canonical_generated_artifact_requires_human_review_flow(
    monkeypatch, tmp_path
) -> None:
    ctx = terminal_context(
        monkeypatch,
        tmp_path / "generated-flow",
        docs_artifact_kind=ReviewArtifactKind.GENERATED.value,
    )
    artifacts = (
        artifact(
            1,
            "docs/new.md",
            ReviewArtifactKind.GENERATED,
            disposition=ReviewArtifactDisposition.REQUIRES_HUMAN_REVIEW,
        ),
    )
    obs = observation(ctx, canonical_paths(), artifacts)
    result = build_diff_artifact_review(request(ctx, obs))
    assert result.diff_verdict in {
        DiffReviewVerdict.ACCEPTED,
        DiffReviewVerdict.REQUIRES_HUMAN_REVIEW,
    }
    assert result.artifact_verdict is ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    assert result.diff_artifact_review_requirement_satisfied is True
    assert result.human_git_handoff_ready is False
    assert result.automatic_cleanup_authorized is False
    assert result.automatic_rollback_authorized is False
    assert result.automatic_staging_authorized is False


@pytest.mark.parametrize("kind", ("failure", "cancellation"))
def test_non_result_outcomes_do_not_auto_reject_expected_paths(
    contexts, kind: str
) -> None:
    result = build_diff_artifact_review(
        request(contexts[kind], observation(contexts[kind], canonical_paths()))
    )
    assert result.diff_verdict is DiffReviewVerdict.ACCEPTED
    assert result.diff_artifact_review_requirement_satisfied is True
    assert result.automatic_cleanup_authorized is False
    assert result.automatic_rollback_authorized is False


@pytest.mark.parametrize("kind", ("failure", "cancellation"))
def test_non_result_outcomes_still_block_unexpected_mutation(
    contexts, kind: str
) -> None:
    paths = canonical_paths() + (
        observed_path(
            4, "zz-unexpected.txt", ReviewObservedPathStatus.UNTRACKED, tracked=False
        ),
    )
    result = build_diff_artifact_review(
        request(contexts[kind], observation(contexts[kind], paths))
    )
    assert result.diff_verdict is DiffReviewVerdict.BLOCKED
    assert result.diff_artifact_review_requirement_satisfied is False


def test_clean_exact_candidate_set_yields_accepted(canonical_result) -> None:
    assert canonical_result.diff_verdict is DiffReviewVerdict.ACCEPTED
    assert canonical_result.artifact_verdict is ArtifactReviewVerdict.ACCEPTED
    assert canonical_result.state is AggregateReviewState.COMPLETED


def test_warning_yields_requires_human_review(monkeypatch, tmp_path) -> None:
    ctx = terminal_context(
        monkeypatch,
        tmp_path / "report",
        docs_artifact_kind=ReviewArtifactKind.REPORT.value,
    )
    result = build_diff_artifact_review(
        request(
            ctx,
            observation(
                ctx,
                canonical_paths(),
                (
                    artifact(
                        1,
                        "docs/new.md",
                        ReviewArtifactKind.REPORT,
                        disposition=ReviewArtifactDisposition.REQUIRES_HUMAN_REVIEW,
                    ),
                ),
            ),
        )
    )
    assert result.artifact_verdict is ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    assert result.state is AggregateReviewState.COMPLETED


def test_blocking_finding_sets_aggregate_blocked(contexts) -> None:
    result = build_diff_artifact_review(
        request(
            contexts["result"], observation(contexts["result"], canonical_paths()[:1])
        )
    )
    assert result.state is AggregateReviewState.BLOCKED
    assert result.diff_artifact_review_requirement_satisfied is False


@pytest.mark.parametrize(
    "field,value",
    (
        ("diff_verdict", DiffReviewVerdict.BLOCKED),
        ("artifact_verdict", ArtifactReviewVerdict.BLOCKED),
        ("state", AggregateReviewState.BLOCKED),
        ("human_git_handoff_ready", True),
        ("automatic_cleanup_authorized", True),
        ("automatic_rollback_authorized", True),
        ("automatic_staging_authorized", True),
        ("provider_dispatch_count", 1),
        ("model_inference_count", 1),
    ),
)
def test_caller_cannot_override_result_posture(
    canonical_result, field: str, value
) -> None:
    data = canonical_result.model_dump(mode="json")
    data[field] = value.value if isinstance(value, Enum) else value
    data["result_SHA256"] = dar._result_digest_from_record({
        k: v for k, v in data.items() if k != "result_SHA256"
    })
    with pytest.raises(ValidationError):
        DiffArtifactReviewResult.model_validate(data)


def test_result_digest_tampering_fails(canonical_result) -> None:
    data = canonical_result.model_dump(mode="json")
    data["result_SHA256"] = digest_text("tamper")
    with pytest.raises(ValidationError):
        DiffArtifactReviewResult.model_validate(data)


def test_validate_result_accepts_canonical_result(canonical_result) -> None:
    validate_diff_artifact_review_result(canonical_result)


def test_repeated_equal_inputs_produce_equal_result(contexts) -> None:
    obs = observation(contexts["result"], canonical_paths(), canonical_artifacts())
    first = build_diff_artifact_review(request(contexts["result"], obs))
    second = build_diff_artifact_review(request(contexts["result"], obs))
    assert first == second
    assert first.review_id == second.review_id
    assert first.result_SHA256 == second.result_SHA256


@pytest.mark.parametrize(
    "mutation",
    (
        "changed_work_packet",
        "changed_allocation",
        "changed_profile",
        "changed_outcome",
        "changed_observation",
        "changed_artifact",
        "changed_finding",
        "changed_verdict",
    ),
)
def test_changed_inputs_change_identity_or_digest(
    contexts, canonical_result, mutation: str
) -> None:
    if mutation == "changed_observation":
        obs = observation(contexts["result"], canonical_paths()[:2])
        changed = build_diff_artifact_review(request(contexts["result"], obs))
        assert changed.review_id != canonical_result.review_id
    elif mutation == "changed_artifact":
        obs = observation(
            contexts["result"], canonical_paths(), canonical_artifacts()[:1]
        )
        changed = build_diff_artifact_review(request(contexts["result"], obs))
        assert changed.result_SHA256 != canonical_result.result_SHA256
    elif mutation == "changed_finding":
        obs = observation(contexts["result"], canonical_paths()[:1])
        changed = build_diff_artifact_review(request(contexts["result"], obs))
        assert changed.result_SHA256 != canonical_result.result_SHA256
    elif mutation == "changed_verdict":
        obs = observation(contexts["result"], canonical_paths()[:1])
        changed = build_diff_artifact_review(request(contexts["result"], obs))
        assert changed.diff_verdict != canonical_result.diff_verdict
    else:
        data = canonical_result.model_dump(mode="json")
        field = {
            "changed_work_packet": "work_packet_SHA256",
            "changed_allocation": "allocation_SHA256",
            "changed_profile": "profile_SHA256",
            "changed_outcome": "outcome_SHA256",
        }[mutation]
        data[field] = digest_text(mutation)
        data["result_SHA256"] = dar._result_digest_from_record({
            k: v for k, v in data.items() if k != "result_SHA256"
        })
        assert data["result_SHA256"] != canonical_result.result_SHA256


def test_review_id_shape(canonical_result) -> None:
    assert re.match(
        r"^DAR-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$", canonical_result.review_id
    )


def test_digest_is_not_signature(canonical_result) -> None:
    assert len(canonical_result.result_SHA256) == 64
    assert "signature" not in canonical_result.model_dump_json().lower()


@pytest.mark.parametrize(
    "forbidden", ("wall_clock", "datetime", "uuid", "random", "pid", "thread")
)
def test_forbidden_identity_sources_absent(canonical_result, forbidden: str) -> None:
    assert forbidden not in canonical_result.model_dump_json().lower()


@pytest.mark.parametrize("model_cls", PUBLIC_MODELS)
def test_no_forbidden_public_schema_shapes(model_cls: type[BaseModel]) -> None:
    schema_text = str(model_cls.model_json_schema()).lower()
    for forbidden in ("datetime", "uuid", "pathlib", "callable"):
        assert forbidden not in schema_text


@pytest.mark.parametrize(
    "model_name",
    (
        ReviewExpectedMutation.__name__,
        ReviewObservedPath.__name__,
        ReviewArtifactObservation.__name__,
        DiffArtifactReviewObservation.__name__,
        DiffArtifactReviewResult.__name__,
    ),
)
def test_serialized_models_exclude_raw_diff_and_file_content(
    model_name: str, sample_models
) -> None:
    payload = sample_models[model_name].model_dump_json().lower()
    assert "raw diff" not in payload
    assert "diff --git" not in payload
    assert "file content" not in payload
    assert "raw stdout" not in payload
    assert "raw stderr" not in payload


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
        "Git_commands",
        "Docker_calls",
        "Graphify_calls",
        "cleanup_calls",
        "rollback_calls",
        "staging_calls",
        "commit_calls",
        "push_calls",
        "manual_validation_completion",
        "Git_handoff",
    ),
)
def test_authority_boundary_has_no_operational_calls(
    canonical_result, operation: str
) -> None:
    assert canonical_result.provider_dispatch_count == 0
    assert canonical_result.model_inference_count == 0
    assert canonical_result.automatic_cleanup_authorized is False
    assert canonical_result.automatic_rollback_authorized is False
    assert canonical_result.automatic_staging_authorized is False
    assert operation


@pytest.mark.parametrize("kind", ReviewArtifactKind)
def test_artifact_policy_matrix(kind: ReviewArtifactKind) -> None:
    disposition = ReviewArtifactDisposition.ACCEPTABLE
    if kind in {
        ReviewArtifactKind.GENERATED,
        ReviewArtifactKind.LOG,
        ReviewArtifactKind.REPORT,
        ReviewArtifactKind.BINARY,
        ReviewArtifactKind.UNKNOWN,
    }:
        disposition = ReviewArtifactDisposition.REQUIRES_HUMAN_REVIEW
    if kind in {ReviewArtifactKind.CACHE, ReviewArtifactKind.TEMPORARY}:
        disposition = ReviewArtifactDisposition.PROHIBITED
    verdict, _findings = artifact_policy_findings(kind, disposition=disposition)
    if kind in {ReviewArtifactKind.CACHE, ReviewArtifactKind.TEMPORARY}:
        assert verdict is ArtifactReviewVerdict.BLOCKED
    elif kind in {
        ReviewArtifactKind.GENERATED,
        ReviewArtifactKind.LOG,
        ReviewArtifactKind.REPORT,
        ReviewArtifactKind.BINARY,
        ReviewArtifactKind.UNKNOWN,
    }:
        assert verdict is ArtifactReviewVerdict.REQUIRES_HUMAN_REVIEW
    else:
        assert verdict is ArtifactReviewVerdict.ACCEPTED


@pytest.mark.parametrize("origin", ReviewArtifactOrigin)
def test_artifact_origin_policy_matrix(origin: ReviewArtifactOrigin) -> None:
    disposition = ReviewArtifactDisposition.ACCEPTABLE
    source_action_id = "ACTION-001"
    source_command_id = None
    if origin is ReviewArtifactOrigin.UNKNOWN:
        disposition = ReviewArtifactDisposition.REQUIRES_HUMAN_REVIEW
    if origin is ReviewArtifactOrigin.VALIDATION_PRODUCED:
        source_action_id = None
        source_command_id = "VCMD-001"
    verdict, _findings = artifact_policy_findings(
        ReviewArtifactKind.DOCUMENTATION,
        disposition=disposition,
        origin=origin,
        source_action_id=source_action_id,
        source_command_id=source_command_id,
    )
    if origin is ReviewArtifactOrigin.UNKNOWN:
        assert verdict is ArtifactReviewVerdict.BLOCKED
    else:
        assert verdict is ArtifactReviewVerdict.ACCEPTED
