from __future__ import annotations

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import runtime_adapter as ra


UTC = timezone.utc
PACKAGE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
)


EXPECTED_ENUMS = {
    ra.RuntimeLifecycleState: [
        "created",
        "validating",
        "starting",
        "waiting_for_readiness",
        "ready",
        "cancellation_requested",
        "stopping",
        "stopped",
        "cancelled",
        "failed",
        "rollback_pending",
        "rolled_back",
        "rollback_failed",
    ],
    ra.RuntimeLifecycleAction: [
        "validate",
        "start",
        "wait_for_readiness",
        "mark_ready",
        "request_cancellation",
        "begin_stop",
        "mark_stopped",
        "mark_cancelled",
        "mark_failed",
        "begin_rollback",
        "mark_rolled_back",
        "mark_rollback_failed",
    ],
    ra.RuntimeProfileClass: [
        "test_lifecycle_probe",
        "hermes_dashboard_experimental",
    ],
    ra.RuntimeEventType: [
        "request_received",
        "request_rejected",
        "workspace_created",
        "profile_resolved",
        "environment_sanitized",
        "process_started",
        "listener_discovered",
        "readiness_probe_started",
        "runtime_ready",
        "readiness_timeout",
        "cancellation_requested",
        "graceful_shutdown_started",
        "forced_termination_started",
        "process_exited",
        "listener_released",
        "workspace_cleanup_started",
        "workspace_cleanup_completed",
        "rollback_started",
        "rollback_completed",
        "runtime_failed",
    ],
    ra.RuntimeFailureStage: [
        "request_validation",
        "profile_resolution",
        "environment_construction",
        "workspace_creation",
        "path_containment",
        "process_launch",
        "ownership_capture",
        "listener_discovery",
        "readiness",
        "runtime_operation",
        "cancellation",
        "graceful_shutdown",
        "forced_termination",
        "workspace_cleanup",
        "rollback",
        "event_normalization",
    ],
    ra.RuntimeSeverity: ["debug", "info", "warning", "error", "critical"],
    ra.RuntimeRetryability: [
        "never",
        "safe_after_cleanup",
        "policy_decision_required",
    ],
    ra.RuntimeProcessStatus: [
        "not_started",
        "starting",
        "running",
        "exited",
        "terminated",
        "unknown",
    ],
    ra.RuntimeReadinessState: [
        "not_started",
        "waiting",
        "ready",
        "timed_out",
        "failed",
        "cancelled",
    ],
    ra.RuntimeWorkspaceStatus: [
        "unallocated",
        "allocated",
        "retained",
        "cleaned",
        "cleanup_failed",
    ],
    ra.RuntimeCleanupStatus: [
        "not_started",
        "pending",
        "completed",
        "failed",
        "retained",
    ],
    ra.RuntimeRetentionPolicy: [
        "remove_on_success",
        "remove_on_terminal",
        "retain_evidence",
    ],
    ra.RuntimeOperationOutcome: [
        "accepted",
        "ready",
        "stopped",
        "cancelled",
        "failed",
        "rolled_back",
        "rollback_failed",
    ],
    ra.RuntimeLogStream: ["stdout", "stderr"],
}


TRANSITIONS = {
    ra.RuntimeLifecycleState.CREATED: [
        (ra.RuntimeLifecycleAction.VALIDATE, ra.RuntimeLifecycleState.VALIDATING),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.VALIDATING: [
        (ra.RuntimeLifecycleAction.START, ra.RuntimeLifecycleState.STARTING),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.STARTING: [
        (
            ra.RuntimeLifecycleAction.WAIT_FOR_READINESS,
            ra.RuntimeLifecycleState.WAITING_FOR_READINESS,
        ),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.STOPPING),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.WAITING_FOR_READINESS: [
        (ra.RuntimeLifecycleAction.MARK_READY, ra.RuntimeLifecycleState.READY),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.STOPPING),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.READY: [
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.STOPPING),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.CANCELLATION_REQUESTED: [
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLATION_REQUESTED,
        ),
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.STOPPING),
        (ra.RuntimeLifecycleAction.MARK_CANCELLED, ra.RuntimeLifecycleState.CANCELLED),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.STOPPING: [
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.STOPPING),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.STOPPING,
        ),
        (ra.RuntimeLifecycleAction.MARK_STOPPED, ra.RuntimeLifecycleState.STOPPED),
        (ra.RuntimeLifecycleAction.MARK_CANCELLED, ra.RuntimeLifecycleState.CANCELLED),
        (ra.RuntimeLifecycleAction.MARK_FAILED, ra.RuntimeLifecycleState.FAILED),
    ],
    ra.RuntimeLifecycleState.STOPPED: [
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.STOPPED),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.STOPPED,
        ),
        (
            ra.RuntimeLifecycleAction.BEGIN_ROLLBACK,
            ra.RuntimeLifecycleState.ROLLBACK_PENDING,
        ),
    ],
    ra.RuntimeLifecycleState.CANCELLED: [
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.CANCELLED,
        ),
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.CANCELLED),
        (
            ra.RuntimeLifecycleAction.BEGIN_ROLLBACK,
            ra.RuntimeLifecycleState.ROLLBACK_PENDING,
        ),
    ],
    ra.RuntimeLifecycleState.FAILED: [
        (
            ra.RuntimeLifecycleAction.BEGIN_ROLLBACK,
            ra.RuntimeLifecycleState.ROLLBACK_PENDING,
        ),
    ],
    ra.RuntimeLifecycleState.ROLLBACK_PENDING: [
        (
            ra.RuntimeLifecycleAction.BEGIN_ROLLBACK,
            ra.RuntimeLifecycleState.ROLLBACK_PENDING,
        ),
        (
            ra.RuntimeLifecycleAction.MARK_ROLLED_BACK,
            ra.RuntimeLifecycleState.ROLLED_BACK,
        ),
        (
            ra.RuntimeLifecycleAction.MARK_ROLLBACK_FAILED,
            ra.RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
    ],
    ra.RuntimeLifecycleState.ROLLED_BACK: [
        (ra.RuntimeLifecycleAction.BEGIN_STOP, ra.RuntimeLifecycleState.ROLLED_BACK),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.ROLLED_BACK,
        ),
        (
            ra.RuntimeLifecycleAction.BEGIN_ROLLBACK,
            ra.RuntimeLifecycleState.ROLLED_BACK,
        ),
        (
            ra.RuntimeLifecycleAction.MARK_ROLLED_BACK,
            ra.RuntimeLifecycleState.ROLLED_BACK,
        ),
    ],
    ra.RuntimeLifecycleState.ROLLBACK_FAILED: [
        (
            ra.RuntimeLifecycleAction.BEGIN_STOP,
            ra.RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
        (
            ra.RuntimeLifecycleAction.REQUEST_CANCELLATION,
            ra.RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
        (
            ra.RuntimeLifecycleAction.MARK_ROLLBACK_FAILED,
            ra.RuntimeLifecycleState.ROLLBACK_FAILED,
        ),
    ],
}


def utc(offset_seconds: int = 0) -> datetime:
    return datetime(2026, 7, 18, 12, 0, tzinfo=UTC) + timedelta(seconds=offset_seconds)


def timeout_policy(**overrides: int) -> ra.RuntimeTimeoutPolicy:
    values = {
        "readiness_timeout_ms": 10_000,
        "graceful_shutdown_timeout_ms": 1_000,
        "forced_termination_timeout_ms": 1_000,
        "poll_interval_ms": 100,
        "max_stdout_bytes": 4_096,
        "max_stderr_bytes": 4_096,
    }
    values.update(overrides)
    return ra.RuntimeTimeoutPolicy(**values)


def workspace_binding(**overrides: object) -> ra.RuntimeWorkspaceBinding:
    values = {
        "workspace_policy_id": "workspace-policy.isolated-local",
        "retention_policy": ra.RuntimeRetentionPolicy.REMOVE_ON_TERMINAL,
        "require_managed_files_root": True,
    }
    values.update(overrides)
    return ra.RuntimeWorkspaceBinding(**values)


def workspace_ref(**overrides: object) -> ra.RuntimeWorkspaceRef:
    values = {
        "workspace_id": "workspace-001",
        "workspace_policy_id": "workspace-policy.isolated-local",
        "status": ra.RuntimeWorkspaceStatus.ALLOCATED,
        "managed_files_root_bound": True,
    }
    values.update(overrides)
    return ra.RuntimeWorkspaceRef(**values)


def evidence_ref(evidence_id: str = "evidence-001") -> ra.RuntimeEvidenceRef:
    return ra.RuntimeEvidenceRef(evidence_id=evidence_id, evidence_kind="runtime_event")


def runtime_handle(
    *,
    state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.READY,
    runtime_id: str = "rt_01j4n7y9f5",
    correlation_id: str = "corr:p14.1:001",
    profile_id: str = ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
) -> ra.RuntimeHandle:
    return ra.RuntimeHandle(
        schema_version=ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        profile_id=profile_id,
        workspace_id="workspace-001",
        lifecycle_state=state,
        created_at_utc=utc(),
    )


def process_ref(**overrides: object) -> ra.RuntimeProcessRef:
    values = {
        "launcher_pid": 1001,
        "listener_pid": 1001,
        "descendant_pids": (1002, 1003),
        "process_status": ra.RuntimeProcessStatus.RUNNING,
        "started_at_utc": utc(),
        "exited_at_utc": None,
        "exit_code": None,
    }
    values.update(overrides)
    return ra.RuntimeProcessRef(**values)


def readiness_ref(**overrides: object) -> ra.RuntimeReadinessRef:
    values = {
        "probe_id": "probe-001",
        "state": ra.RuntimeReadinessState.READY,
        "attempt_count": 1,
        "deadline_at_utc": utc(10),
        "observed_at_utc": utc(1),
        "listener_port": 9129,
    }
    values.update(overrides)
    return ra.RuntimeReadinessRef(**values)


def log_ref(stream: ra.RuntimeLogStream) -> ra.RuntimeLogRef:
    return ra.RuntimeLogRef(
        stream=stream,
        evidence_ref=evidence_ref(f"evidence-log-{stream.value}"),
        captured_bytes=128,
        truncated=False,
    )


def event(
    sequence: int,
    *,
    runtime_id: str = "rt_01j4n7y9f5",
    correlation_id: str = "corr:p14.1:001",
    profile_id: str = ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
    event_id: str | None = None,
) -> ra.RuntimeEvent:
    return ra.RuntimeEvent(
        schema_version=ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION,
        event_id=event_id or f"event-{sequence:03d}",
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        sequence=sequence,
        event_type=ra.RuntimeEventType.RUNTIME_READY,
        lifecycle_state=ra.RuntimeLifecycleState.READY,
        profile_id=profile_id,
        timestamp_utc=utc(sequence),
        monotonic_offset_ms=sequence * 10,
        stage=ra.RuntimeFailureStage.READINESS,
        severity=ra.RuntimeSeverity.INFO,
        message_code="runtime_ready",
        sanitized_message="Runtime is ready",
        process_reference=evidence_ref("process-evidence"),
        workspace_reference=evidence_ref("workspace-evidence"),
        readiness_reference=evidence_ref("readiness-evidence"),
        failure_reference=None,
    )


def failure(**overrides: object) -> ra.RuntimeFailure:
    values = {
        "schema_version": ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION,
        "failure_id": "failure-001",
        "runtime_id": "rt_01j4n7y9f5",
        "profile_id": ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        "stage": ra.RuntimeFailureStage.READINESS,
        "failure_code": "readiness_timeout",
        "sanitized_summary": "Readiness timed out",
        "retryability": ra.RuntimeRetryability.SAFE_AFTER_CLEANUP,
        "cleanup_status": ra.RuntimeCleanupStatus.PENDING,
        "process_status": ra.RuntimeProcessStatus.RUNNING,
        "workspace_status": ra.RuntimeWorkspaceStatus.ALLOCATED,
        "evidence_refs": (evidence_ref("failure-evidence"),),
    }
    values.update(overrides)
    return ra.RuntimeFailure(**values)


def operation_result(**overrides: object) -> ra.RuntimeOperationResult:
    values = {
        "schema_version": ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION,
        "runtime_handle": runtime_handle(),
        "outcome": ra.RuntimeOperationOutcome.READY,
        "process_reference": process_ref(),
        "workspace_reference": workspace_ref(),
        "readiness_reference": readiness_ref(),
        "log_references": (
            log_ref(ra.RuntimeLogStream.STDOUT),
            log_ref(ra.RuntimeLogStream.STDERR),
        ),
        "failure": None,
        "events": (event(0), event(1)),
    }
    values.update(overrides)
    return ra.RuntimeOperationResult(**values)


def assert_validation_error(model: type[object], **values: object) -> None:
    with pytest.raises(ValidationError):
        model(**values)


def test_vocabularies_are_exact_and_schema_version_is_stable() -> None:
    for enum_type, expected_values in EXPECTED_ENUMS.items():
        actual = [item.value for item in enum_type]
        assert actual == expected_values
        assert len(actual) == len(set(actual))

    assert ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION == 1
    assert ra.TEST_LIFECYCLE_PROBE_PROFILE_ID == "test.lifecycle_probe"
    assert (
        ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID == "hermes.dashboard.experimental"
    )
    assert len(ra.RuntimeLifecycleState) == 13
    assert len(ra.RuntimeLifecycleAction) == 12


def test_public_exports_are_reviewed_contract_api_only() -> None:
    expected_exports = {
        "HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID",
        "RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION",
        "TEST_LIFECYCLE_PROBE_PROFILE_ID",
        "InvalidRuntimeTransitionError",
        "RuntimeAdapterContractError",
        "RuntimeCancelRequest",
        "RuntimeCleanupStatus",
        "RuntimeContractValidationError",
        "RuntimeEvent",
        "RuntimeEventType",
        "RuntimeEvidenceRef",
        "RuntimeFailure",
        "RuntimeFailureStage",
        "RuntimeHandle",
        "RuntimeLaunchRequest",
        "RuntimeLifecycleAction",
        "RuntimeLifecycleState",
        "RuntimeLogRef",
        "RuntimeLogStream",
        "RuntimeOperationOutcome",
        "RuntimeOperationResult",
        "RuntimeProcessRef",
        "RuntimeProcessStatus",
        "RuntimeProfileClass",
        "RuntimeProfileRef",
        "RuntimeReadinessRef",
        "RuntimeReadinessState",
        "RuntimeRetentionPolicy",
        "RuntimeRetryability",
        "RuntimeRollbackRequest",
        "RuntimeSeverity",
        "RuntimeStopRequest",
        "RuntimeTimeoutPolicy",
        "RuntimeWorkspaceBinding",
        "RuntimeWorkspaceRef",
        "RuntimeWorkspaceStatus",
        "allowed_runtime_actions",
        "is_runtime_terminal",
        "transition_runtime_state",
    }
    assert set(ra.__all__) == expected_exports


def test_models_are_frozen_extra_forbid_and_round_trip_deterministically() -> None:
    result = operation_result()
    dumped = result.model_dump(mode="json")
    round_tripped = ra.RuntimeOperationResult.model_validate(dumped)

    assert round_tripped == result
    assert tuple(dumped["events"]) == tuple(dumped["events"])
    assert "object at 0x" not in str(dumped)

    with pytest.raises(ValidationError):
        ra.RuntimeEvidenceRef(
            evidence_id="evidence-001", evidence_kind="kind", extra=True
        )
    with pytest.raises(ValidationError):
        result.outcome = ra.RuntimeOperationOutcome.FAILED  # type: ignore[misc]


def test_collections_normalize_to_tuples_and_schema_version_is_enforced() -> None:
    launch = ra.RuntimeLaunchRequest(
        schema_version=1,
        runtime_profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        workspace_binding=workspace_binding(),
        correlation_id="corr:p14.1:001",
        requested_by="P14.1",
        timeout_policy=timeout_policy(),
        evidence_context=[evidence_ref("evidence-001")],
    )
    assert isinstance(launch.evidence_context, tuple)

    assert_validation_error(
        ra.RuntimeLaunchRequest,
        **{**launch.model_dump(mode="python"), "schema_version": 2},
    )


def test_identifier_policy_rejects_paths_shell_text_and_whitespace() -> None:
    valid_ids = [
        "rt_01j4n7y9f5",
        "corr:p14.2:001",
        "test.lifecycle_probe",
        "hermes.dashboard.experimental",
        "workspace-policy.isolated-local",
        "P14.1",
        "runtime_ready",
    ]
    for identifier in valid_ids:
        assert evidence_ref(identifier).evidence_id == identifier

    invalid_ids = [
        "../runtime",
        r"C:\Users\pablo",
        "$(command)",
        "runtime id",
        "profile/one",
        r"profile\one",
        "",
        "x" * 129,
    ]
    for identifier in invalid_ids:
        assert_validation_error(
            ra.RuntimeEvidenceRef,
            evidence_id=identifier,
            evidence_kind="kind",
        )


def test_naive_datetimes_are_rejected_and_aware_datetimes_normalize_to_utc() -> None:
    naive = datetime(2026, 7, 18, 12, 0)
    assert_validation_error(
        ra.RuntimeHandle,
        schema_version=1,
        runtime_id="rt-1",
        correlation_id="corr-1",
        profile_id="profile-1",
        workspace_id="workspace-1",
        lifecycle_state=ra.RuntimeLifecycleState.CREATED,
        created_at_utc=naive,
    )

    offset = datetime(2026, 7, 18, 8, 0, tzinfo=timezone(timedelta(hours=-4)))
    handle = runtime_handle(
        state=ra.RuntimeLifecycleState.CREATED, profile_id="profile-1"
    )
    normalized = ra.RuntimeHandle.model_validate({
        **handle.model_dump(),
        "created_at_utc": offset,
    })
    assert normalized.created_at_utc == utc()


def test_request_contracts_exclude_execution_authority_fields() -> None:
    forbidden_request_fields = {
        "command",
        "argv",
        "executable",
        "executable_path",
        "shell",
        "environment",
        "env",
        "cwd",
        "working_directory",
        "output_path",
        "signal",
        "kill_command",
    }
    request_models = [
        ra.RuntimeLaunchRequest,
        ra.RuntimeStopRequest,
        ra.RuntimeCancelRequest,
        ra.RuntimeRollbackRequest,
    ]
    for model in request_models:
        assert forbidden_request_fields.isdisjoint(model.model_fields)

    assert "path" not in ra.RuntimeWorkspaceBinding.model_fields
    assert "executable" not in ra.RuntimeProfileRef.model_fields
    assert "environment_policy_id" in ra.RuntimeProfileRef.model_fields


def test_timeout_policy_bounds_and_poll_interval_invariant() -> None:
    lower_cases = {
        "readiness_timeout_ms": 0,
        "graceful_shutdown_timeout_ms": 0,
        "forced_termination_timeout_ms": 0,
        "poll_interval_ms": 49,
        "max_stdout_bytes": 1_023,
        "max_stderr_bytes": 1_023,
    }
    upper_cases = {
        "readiness_timeout_ms": 300_001,
        "graceful_shutdown_timeout_ms": 60_001,
        "forced_termination_timeout_ms": 60_001,
        "poll_interval_ms": 5_001,
        "max_stdout_bytes": 1_048_577,
        "max_stderr_bytes": 1_048_577,
    }
    for field, value in {**lower_cases, **upper_cases}.items():
        with pytest.raises(ValidationError):
            timeout_policy(**{field: value})
    with pytest.raises(ValidationError):
        timeout_policy(readiness_timeout_ms=100, poll_interval_ms=100)


def test_profile_ref_distinguishes_syntax_from_registration_and_records_files_root_invariant() -> (
    None
):
    custom = ra.RuntimeProfileRef(
        profile_id="syntactic.only.profile",
        profile_class=ra.RuntimeProfileClass.TEST_LIFECYCLE_PROBE,
        environment_policy_id="env-policy.test",
        workspace_policy_id="workspace-policy.test",
        readiness_policy_id="readiness-policy.test",
        shutdown_policy_id="shutdown-policy.test",
        files_root_policy_id=None,
    )
    assert custom.profile_id == "syntactic.only.profile"

    with pytest.raises(ValidationError):
        ra.RuntimeProfileRef(
            profile_id=ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID,
            profile_class=ra.RuntimeProfileClass.HERMES_DASHBOARD_EXPERIMENTAL,
            environment_policy_id="env-policy.dashboard",
            workspace_policy_id="workspace-policy.dashboard",
            readiness_policy_id="readiness-policy.dashboard",
            shutdown_policy_id="shutdown-policy.dashboard",
            files_root_policy_id=None,
        )


def test_state_machine_matches_exact_transition_table_and_rejects_invalid_transitions() -> (
    None
):
    transition_count = 0
    for state, transitions in TRANSITIONS.items():
        assert ra.allowed_runtime_actions(state) == tuple(
            action for action, _ in transitions
        )
        for action, target in transitions:
            transition_count += 1
            assert ra.transition_runtime_state(state, action) == target

    assert transition_count == 43
    with pytest.raises(ra.InvalidRuntimeTransitionError) as exc_info:
        ra.transition_runtime_state(
            ra.RuntimeLifecycleState.CREATED,
            ra.RuntimeLifecycleAction.MARK_READY,
        )
    error = exc_info.value
    assert error.error_code == "invalid_runtime_transition"
    assert error.current_state is ra.RuntimeLifecycleState.CREATED
    assert error.requested_action is ra.RuntimeLifecycleAction.MARK_READY
    assert error.allowed_actions == ra.allowed_runtime_actions(
        ra.RuntimeLifecycleState.CREATED
    )


def test_terminal_policy_preserves_rollback_distinction() -> None:
    terminal_without_rollback = {
        ra.RuntimeLifecycleState.STOPPED,
        ra.RuntimeLifecycleState.CANCELLED,
        ra.RuntimeLifecycleState.FAILED,
        ra.RuntimeLifecycleState.ROLLED_BACK,
        ra.RuntimeLifecycleState.ROLLBACK_FAILED,
    }
    terminal_with_rollback = {
        ra.RuntimeLifecycleState.ROLLED_BACK,
        ra.RuntimeLifecycleState.ROLLBACK_FAILED,
    }
    for state in ra.RuntimeLifecycleState:
        assert ra.is_runtime_terminal(state, rollback_required=False) is (
            state in terminal_without_rollback
        )
        assert ra.is_runtime_terminal(state, rollback_required=True) is (
            state in terminal_with_rollback
        )


def test_process_evidence_pid_and_exit_consistency() -> None:
    assert process_ref().process_status is ra.RuntimeProcessStatus.RUNNING
    assert_validation_error(
        ra.RuntimeProcessRef,
        **{**process_ref().model_dump(), "launcher_pid": 0},
    )
    assert_validation_error(
        ra.RuntimeProcessRef,
        **{**process_ref().model_dump(), "descendant_pids": (1002, 1002)},
    )
    assert_validation_error(
        ra.RuntimeProcessRef,
        **{**process_ref().model_dump(), "descendant_pids": (1001,)},
    )
    assert_validation_error(
        ra.RuntimeProcessRef,
        **{**process_ref().model_dump(), "listener_pid": 1002},
    )
    assert_validation_error(
        ra.RuntimeProcessRef,
        **{**process_ref().model_dump(), "exited_at_utc": utc(2)},
    )
    assert_validation_error(
        ra.RuntimeProcessRef,
        **{**process_ref().model_dump(), "exit_code": 0},
    )
    assert "command" not in ra.RuntimeProcessRef.model_fields


def test_readiness_evidence_bounds_and_consistency() -> None:
    assert readiness_ref().state is ra.RuntimeReadinessState.READY
    assert_validation_error(
        ra.RuntimeReadinessRef,
        **{**readiness_ref().model_dump(), "listener_port": 0},
    )
    assert_validation_error(
        ra.RuntimeReadinessRef,
        **{**readiness_ref().model_dump(), "attempt_count": -1},
    )
    assert_validation_error(
        ra.RuntimeReadinessRef,
        **{**readiness_ref().model_dump(), "observed_at_utc": None},
    )
    assert_validation_error(
        ra.RuntimeReadinessRef,
        **{
            **readiness_ref().model_dump(),
            "state": ra.RuntimeReadinessState.NOT_STARTED,
            "attempt_count": 1,
        },
    )
    assert_validation_error(
        ra.RuntimeReadinessRef,
        **{**readiness_ref().model_dump(), "observed_at_utc": utc(11)},
    )
    assert "health_url" not in ra.RuntimeReadinessRef.model_fields
    assert "response_body" not in ra.RuntimeReadinessRef.model_fields


def test_events_reject_unbounded_messages_and_invalid_result_event_sets() -> None:
    assert_validation_error(
        ra.RuntimeEvent,
        **{**event(0).model_dump(), "sanitized_message": "x" * 513},
    )
    assert_validation_error(
        ra.RuntimeEvent,
        **{**event(0).model_dump(), "sanitized_message": "bad\nmessage"},
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "events": (event(1), event(1, event_id="event-002")),
        },
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "events": (event(0), event(1, event_id="event-000")),
        },
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "events": (event(0), event(1, runtime_id="rt-other")),
        },
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "events": tuple(event(i) for i in range(257)),
        },
    )


def test_failure_and_result_envelopes_enforce_identity_outcome_and_log_rules() -> None:
    good_failure = failure()
    failed_handle = runtime_handle(state=ra.RuntimeLifecycleState.FAILED)
    failed_result = operation_result(
        runtime_handle=failed_handle,
        outcome=ra.RuntimeOperationOutcome.FAILED,
        failure=good_failure,
        events=(),
    )
    assert failed_result.failure == good_failure

    assert_validation_error(
        ra.RuntimeFailure,
        **{**good_failure.model_dump(), "sanitized_summary": "bad\rsummary"},
    )
    assert_validation_error(
        ra.RuntimeFailure,
        **{
            **good_failure.model_dump(),
            "evidence_refs": (evidence_ref("dup"), evidence_ref("dup")),
        },
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{**operation_result().model_dump(), "failure": good_failure},
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "runtime_handle": failed_handle,
            "outcome": ra.RuntimeOperationOutcome.FAILED,
            "failure": None,
            "events": (),
        },
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "log_references": (
                log_ref(ra.RuntimeLogStream.STDOUT),
                log_ref(ra.RuntimeLogStream.STDOUT),
            ),
        },
    )
    assert_validation_error(
        ra.RuntimeOperationResult,
        **{
            **operation_result().model_dump(),
            "outcome": ra.RuntimeOperationOutcome.STOPPED,
        },
    )


def test_source_guard_blocks_process_network_filesystem_and_command_surfaces() -> None:
    execution_authorized_modules = {
        "adapter.py",
        "listener_discovery.py",
        "readiness.py",
    }
    prohibited_modules = {
        "subprocess",
        "commands",
        "shlex",
        "socket",
        "requests",
        "httpx",
        "urllib.request",
        "multiprocessing",
        "threading",
        "signal",
        "psutil",
        "win32api",
        "win32job",
        "win32process",
    }
    prohibited_calls = {
        "create_subprocess_exec",
        "create_subprocess_shell",
        "system",
        "popen",
        "open",
        "mkdir",
        "unlink",
        "rmdir",
        "remove",
        "replace",
    }
    for source_path in PACKAGE_ROOT.glob("*.py"):
        if source_path.name in execution_authorized_modules:
            continue
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name for alias in node.names}
                assert imported.isdisjoint(prohibited_modules), source_path
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert module not in prohibited_modules, source_path
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                assert name not in prohibited_calls, source_path

    forbidden_public_fields = {
        "command",
        "argv",
        "executable",
        "executable_path",
        "shell",
        "environment",
        "env",
        "cwd",
        "working_directory",
        "output_path",
        "signal",
        "kill_command",
    }
    public_models = [
        ra.RuntimeTimeoutPolicy,
        ra.RuntimeProfileRef,
        ra.RuntimeWorkspaceBinding,
        ra.RuntimeWorkspaceRef,
        ra.RuntimeEvidenceRef,
        ra.RuntimeLaunchRequest,
        ra.RuntimeStopRequest,
        ra.RuntimeCancelRequest,
        ra.RuntimeRollbackRequest,
        ra.RuntimeHandle,
        ra.RuntimeProcessRef,
        ra.RuntimeReadinessRef,
        ra.RuntimeLogRef,
        ra.RuntimeEvent,
        ra.RuntimeFailure,
        ra.RuntimeOperationResult,
    ]
    for model in public_models:
        forbidden = forbidden_public_fields & set(model.model_fields)
        if forbidden == {"environment_policy_id"}:
            forbidden = set()
        assert not forbidden, (model.__name__, forbidden)
