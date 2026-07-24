from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.environment import (
    RuntimeEnvironmentSanitizationReport,
    RuntimePlatformFamily,
)
from hermes_cli.agent_platform.runtime_adapter.adapter import RuntimeAdapterLaunchError
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    MissingRuntimeEventReferenceError,
    RuntimeEventIdentifierError,
    RuntimeEventJournal,
    RuntimeEventStagePolicy,
    RuntimeEventTimestampError,
    RuntimeFailureNormalizationError,
    UnexpectedRuntimeEventReferenceError,
    UnknownRuntimeFailureCodeError,
    get_runtime_event_descriptor,
    list_runtime_event_descriptors,
    list_runtime_failure_descriptors,
    normalize_runtime_failure,
    validate_environment_report_for_normalization,
)
from hermes_cli.agent_platform.runtime_adapter.listener_discovery import (
    RuntimeListenerDiscoveryTimeoutError,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    OwnedProcessSnapshot,
    ProcessLaunchError,
    RuntimeProcessOwnerError,
)
from hermes_cli.agent_platform.runtime_adapter.readiness import (
    RuntimeReadinessProductConfigurationError,
)
from hermes_cli.agent_platform.runtime_adapter.stream_capture import (
    BoundedStreamSnapshot,
)


UTC = timezone.utc
SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "event_normalization.py"
)


def utc(seconds: int) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=seconds)


def runtime_handle(
    state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.CREATED,
) -> ra.RuntimeHandle:
    return ra.RuntimeHandle(
        schema_version=1,
        runtime_id="runtime.p14-5.test",
        correlation_id="corr.p14-5.test",
        profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        workspace_id="ws_p14_5_test",
        lifecycle_state=state,
        created_at_utc=utc(0),
    )


def event_id_factory(*event_ids: str):
    values = iter(event_ids)
    return lambda: next(values)


def failure_id_factory(failure_id: str):
    return lambda: failure_id


def evidence_ref(evidence_id: str, evidence_kind: str) -> ra.RuntimeEvidenceRef:
    return ra.RuntimeEvidenceRef(
        evidence_id=evidence_id,
        evidence_kind=evidence_kind,
    )


def process_snapshot(runtime_id: str = "runtime.p14-5.test") -> OwnedProcessSnapshot:
    process_ref = ra.RuntimeProcessRef(
        launcher_pid=12345,
        listener_pid=None,
        descendant_pids=(),
        process_status=ra.RuntimeProcessStatus.RUNNING,
        started_at_utc=utc(1),
        exited_at_utc=None,
        exit_code=None,
    )
    return OwnedProcessSnapshot(
        runtime_id=runtime_id,
        process_reference=process_ref,
        stdout_snapshot=BoundedStreamSnapshot(
            stream=ra.RuntimeLogStream.STDOUT,
            total_bytes_read=0,
            bounded_bytes=0,
            discarded_bytes=0,
            truncated=False,
            drain_complete=True,
        ),
        stderr_snapshot=BoundedStreamSnapshot(
            stream=ra.RuntimeLogStream.STDERR,
            total_bytes_read=0,
            bounded_bytes=0,
            discarded_bytes=0,
            truncated=False,
            drain_complete=True,
        ),
        tree_captured_at_utc=utc(1),
    )


def workspace_allocation(runtime_id: str = "runtime.p14-5.test") -> SimpleNamespace:
    return SimpleNamespace(
        runtime_id=runtime_id,
        workspace_ref=ra.RuntimeWorkspaceRef(
            workspace_id="ws_p14_5_test",
            workspace_policy_id="runtime.workspace.test.lifecycle_probe.v1",
            status=ra.RuntimeWorkspaceStatus.ALLOCATED,
            managed_files_root_bound=False,
        ),
    )


def readiness_ref() -> ra.RuntimeReadinessRef:
    return ra.RuntimeReadinessRef(
        probe_id="probe.p14-5.test",
        state=ra.RuntimeReadinessState.READY,
        attempt_count=1,
        deadline_at_utc=utc(10),
        observed_at_utc=utc(2),
        listener_port=8765,
    )


def environment_report() -> RuntimeEnvironmentSanitizationReport:
    return RuntimeEnvironmentSanitizationReport(
        profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        environment_policy_id="runtime.environment.test.lifecycle_probe.v1",
        platform_family=RuntimePlatformFamily.POSIX,
        source_variable_count=1,
        output_variable_count=6,
        inherited_variable_names=(),
        managed_variable_names=("HERMES_HOME", "HOME", "TEMP", "TMP", "TMPDIR"),
        fixed_variable_names=(
            "PYTHONDONTWRITEBYTECODE",
            "PYTHONIOENCODING",
            "PYTHONUNBUFFERED",
            "PYTHONUTF8",
        ),
        explicit_path_entry_count=0,
        excluded_variable_count=1,
        excluded_sensitive_variable_names=("OPENAI_API_KEY",),
        managed_home_bound=True,
        managed_files_root_required=False,
        managed_files_root_supplied=False,
        provider_variables_present_in_output=False,
    )


def test_event_descriptors_cover_runtime_events_and_are_safe() -> None:
    descriptors = list_runtime_event_descriptors()
    descriptor_event_types = {descriptor.event_type for descriptor in descriptors}

    assert descriptor_event_types == set(ra.RuntimeEventType)
    assert len(descriptor_event_types) == len(descriptors)
    for descriptor in descriptors:
        assert get_runtime_event_descriptor(descriptor.event_type) is descriptor
        assert descriptor.allowed_lifecycle_states
        assert descriptor.message_code.startswith("runtime.")
        assert "\n" not in descriptor.sanitized_message
        assert "\r" not in descriptor.sanitized_message
        if descriptor.stage_policy is RuntimeEventStagePolicy.FAILURE_DERIVED:
            assert descriptor.fixed_stage is None
            assert descriptor.requires_failure_reference is True
        else:
            assert descriptor.fixed_stage is not None

    with pytest.raises(FrozenInstanceError):
        descriptors[0].sanitized_message = "mutated"


def test_event_journal_appends_sequence_and_enforces_reference_policy() -> None:
    handle = runtime_handle()
    journal = RuntimeEventJournal(
        runtime_handle=handle,
        event_id_factory=event_id_factory("evt_request", "evt_process", "evt_ready"),
    )

    request = journal.append(
        event_type=ra.RuntimeEventType.REQUEST_RECEIVED,
        lifecycle_state=ra.RuntimeLifecycleState.CREATED,
        timestamp_utc=utc(0),
        monotonic_offset_ms=0,
    )
    assert request.sequence == 0
    assert request.runtime_id == handle.runtime_id
    assert request.failure_reference is None

    with pytest.raises(MissingRuntimeEventReferenceError):
        journal.append(
            event_type=ra.RuntimeEventType.PROCESS_STARTED,
            lifecycle_state=ra.RuntimeLifecycleState.STARTING,
            timestamp_utc=utc(1),
            monotonic_offset_ms=10,
        )

    started = journal.append(
        event_type=ra.RuntimeEventType.PROCESS_STARTED,
        lifecycle_state=ra.RuntimeLifecycleState.STARTING,
        timestamp_utc=utc(1),
        monotonic_offset_ms=10,
        process_snapshot=process_snapshot(),
    )
    assert started.sequence == 1
    assert started.process_reference == evidence_ref("process_12345", "runtime_process")

    with pytest.raises(UnexpectedRuntimeEventReferenceError):
        journal.append(
            event_type=ra.RuntimeEventType.ENVIRONMENT_SANITIZED,
            lifecycle_state=ra.RuntimeLifecycleState.VALIDATING,
            timestamp_utc=utc(2),
            monotonic_offset_ms=20,
            process_snapshot=process_snapshot(),
        )
    with pytest.raises(UnexpectedRuntimeEventReferenceError):
        journal.append(
            event_type=ra.RuntimeEventType.WORKSPACE_CREATED,
            lifecycle_state=ra.RuntimeLifecycleState.VALIDATING,
            timestamp_utc=utc(2),
            monotonic_offset_ms=20,
            workspace_allocation=workspace_allocation("runtime.other"),
        )


def test_event_journal_rejects_time_regression_and_invalid_identifiers() -> None:
    journal = RuntimeEventJournal(
        runtime_handle=runtime_handle(),
        event_id_factory=event_id_factory("evt_duplicate", "evt_duplicate"),
    )
    journal.append(
        event_type=ra.RuntimeEventType.REQUEST_RECEIVED,
        lifecycle_state=ra.RuntimeLifecycleState.CREATED,
        timestamp_utc=utc(1),
        monotonic_offset_ms=10,
    )

    with pytest.raises(RuntimeEventTimestampError):
        journal.append(
            event_type=ra.RuntimeEventType.PROFILE_RESOLVED,
            lifecycle_state=ra.RuntimeLifecycleState.VALIDATING,
            timestamp_utc=utc(0),
            monotonic_offset_ms=11,
        )
    with pytest.raises(RuntimeEventTimestampError):
        journal.append(
            event_type=ra.RuntimeEventType.PROFILE_RESOLVED,
            lifecycle_state=ra.RuntimeLifecycleState.VALIDATING,
            timestamp_utc=utc(2),
            monotonic_offset_ms=9,
        )
    with pytest.raises(RuntimeEventIdentifierError):
        journal.append(
            event_type=ra.RuntimeEventType.PROFILE_RESOLVED,
            lifecycle_state=ra.RuntimeLifecycleState.VALIDATING,
            timestamp_utc=utc(2),
            monotonic_offset_ms=12,
        )

    invalid_id_journal = RuntimeEventJournal(
        runtime_handle=runtime_handle(),
        event_id_factory=event_id_factory("evt_bad/id"),
    )
    with pytest.raises(RuntimeEventIdentifierError):
        invalid_id_journal.append(
            event_type=ra.RuntimeEventType.REQUEST_RECEIVED,
            lifecycle_state=ra.RuntimeLifecycleState.CREATED,
            timestamp_utc=utc(0),
            monotonic_offset_ms=0,
        )


def test_failure_normalization_maps_supported_errors_and_bounds_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handle = runtime_handle()
    error = ProcessLaunchError(
        runtime_id=handle.runtime_id,
        profile_id=handle.profile_id,
        exception_class="SecretExceptionValue",
    )
    normalized = normalize_runtime_failure(
        error=error,
        runtime_handle=handle,
        process_status=ra.RuntimeProcessStatus.NOT_STARTED,
        workspace_status=ra.RuntimeWorkspaceStatus.ALLOCATED,
        evidence_refs=(
            evidence_ref("evidence.z", "runtime_workspace"),
            evidence_ref("evidence.a", "runtime_process"),
        ),
        failure_id_factory=failure_id_factory("fail_process_launch"),
    )

    assert normalized.source_error_code == "process_launch_error"
    assert normalized.failure.failure_id == "fail_process_launch"
    assert normalized.evidence_ref == evidence_ref(
        "fail_process_launch", "runtime_failure"
    )
    assert normalized.failure.stage is ra.RuntimeFailureStage.PROCESS_LAUNCH
    assert normalized.failure.retryability is ra.RuntimeRetryability.SAFE_AFTER_CLEANUP
    assert normalized.failure.cleanup_status is ra.RuntimeCleanupStatus.PENDING
    assert normalized.failure.evidence_refs == (
        evidence_ref("evidence.a", "runtime_process"),
        evidence_ref("evidence.z", "runtime_workspace"),
    )
    assert "SecretExceptionValue" not in normalized.failure.sanitized_summary

    with pytest.raises(RuntimeFailureNormalizationError):
        normalize_runtime_failure(
            error=RuntimeError("unsupported"),
            runtime_handle=handle,
            process_status=ra.RuntimeProcessStatus.UNKNOWN,
            workspace_status=ra.RuntimeWorkspaceStatus.UNALLOCATED,
        )
    with pytest.raises(RuntimeFailureNormalizationError):
        normalize_runtime_failure(
            error=error,
            runtime_handle=handle,
            process_status=ra.RuntimeProcessStatus.UNKNOWN,
            workspace_status=ra.RuntimeWorkspaceStatus.UNALLOCATED,
            evidence_refs=(
                evidence_ref("dup", "runtime_process"),
                evidence_ref("dup", "runtime_workspace"),
            ),
        )
    with pytest.raises(RuntimeFailureNormalizationError):
        normalize_runtime_failure(
            error=error,
            runtime_handle=handle,
            process_status=ra.RuntimeProcessStatus.UNKNOWN,
            workspace_status=ra.RuntimeWorkspaceStatus.UNALLOCATED,
            failure_id_factory=failure_id_factory("fail_bad/id"),
        )

    unknown = RuntimeProcessOwnerError(runtime_id=handle.runtime_id)
    monkeypatch.setattr(RuntimeProcessOwnerError, "error_code", "unknown_runtime_error")
    with pytest.raises(UnknownRuntimeFailureCodeError):
        normalize_runtime_failure(
            error=unknown,
            runtime_handle=handle,
            process_status=ra.RuntimeProcessStatus.UNKNOWN,
            workspace_status=ra.RuntimeWorkspaceStatus.UNALLOCATED,
        )


def test_p14_8_failure_normalization_maps_internal_adapter_errors() -> None:
    handle = runtime_handle(ra.RuntimeLifecycleState.FAILED)
    descriptors = {
        descriptor.error_code for descriptor in list_runtime_failure_descriptors()
    }
    expected_codes = {
        "runtime_listener_discovery_timeout",
        "runtime_readiness_product_configuration_error",
        "runtime_adapter_launch_error",
    }

    assert expected_codes.issubset(descriptors)

    cases = (
        (
            RuntimeListenerDiscoveryTimeoutError(
                runtime_id=handle.runtime_id,
                port=8765,
                attempt_count=2,
                mechanism="fixture",
            ),
            "runtime_listener_discovery_timeout",
            ra.RuntimeFailureStage.LISTENER_DISCOVERY,
            ra.RuntimeRetryability.SAFE_AFTER_CLEANUP,
            ra.RuntimeCleanupStatus.PENDING,
        ),
        (
            RuntimeReadinessProductConfigurationError(
                runtime_id=handle.runtime_id,
                probe_id="probe.p148",
                endpoint_kind="product_configuration",
                attempt_count=1,
                validation_category="fixture",
            ),
            "runtime_readiness_product_configuration_error",
            ra.RuntimeFailureStage.READINESS,
            ra.RuntimeRetryability.SAFE_AFTER_CLEANUP,
            ra.RuntimeCleanupStatus.PENDING,
        ),
        (
            RuntimeAdapterLaunchError(
                runtime_id=handle.runtime_id,
                profile_id=handle.profile_id,
                operation="launch",
                exception_class="FixtureError",
            ),
            "runtime_adapter_launch_error",
            ra.RuntimeFailureStage.PROCESS_LAUNCH,
            ra.RuntimeRetryability.SAFE_AFTER_CLEANUP,
            ra.RuntimeCleanupStatus.PENDING,
        ),
    )

    for error, code, stage, retryability, cleanup_status in cases:
        normalized = normalize_runtime_failure(
            error=error,
            runtime_handle=handle,
            process_status=ra.RuntimeProcessStatus.UNKNOWN,
            workspace_status=ra.RuntimeWorkspaceStatus.ALLOCATED,
            failure_id_factory=failure_id_factory(f"fail_{code}"),
        )

        assert normalized.source_error_code == code
        assert normalized.failure.failure_code == code
        assert normalized.failure.stage is stage
        assert normalized.failure.retryability is retryability
        assert normalized.failure.cleanup_status is cleanup_status


def test_failure_descriptors_and_environment_report_validation_are_bounded() -> None:
    descriptors = list_runtime_failure_descriptors()
    codes = {descriptor.error_code for descriptor in descriptors}

    assert len(codes) == len(descriptors)
    assert "process_launch_error" in codes
    assert "workspace_allocation_error" in codes
    assert "path_outside_containment_root" in codes
    p14_6_codes = {
        "owned_process_graceful_stop_error",
        "owned_process_graceful_stop_timeout",
        "runtime_lifecycle_control_error",
        "runtime_lifecycle_request_identity_error",
        "runtime_lifecycle_operation_conflict",
        "runtime_lifecycle_ownership_error",
        "runtime_graceful_shutdown_error",
        "runtime_forced_shutdown_error",
        "runtime_process_release_error",
        "runtime_rollback_error",
        "runtime_rollback_identity_error",
        "runtime_rollback_state_error",
        "runtime_rollback_process_still_owned",
        "runtime_rollback_marker_error",
        "runtime_rollback_tree_limit_error",
        "runtime_rollback_entry_type_error",
        "runtime_rollback_containment_error",
        "runtime_rollback_deletion_error",
        "runtime_rollback_allocator_release_error",
    }
    assert p14_6_codes <= codes
    assert validate_environment_report_for_normalization(
        environment_report()
    ).profile_id == (ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
    for descriptor in descriptors:
        assert descriptor.sanitized_summary
        assert "\n" not in descriptor.sanitized_summary
        assert "\r" not in descriptor.sanitized_summary


def test_event_normalization_source_guard_and_root_exports() -> None:
    forbidden_text = {
        "subprocess",
        "create_subprocess",
        "socket",
        "requests",
        "httpx",
        "urllib.request",
        "os.environ",
        "os.getenv",
        "path.home",
        "expanduser",
        ".mkdir",
        "open(",
        "logger.",
        "logging.",
        "graphify",
    }
    text = SOURCE_PATH.read_text(encoding="utf-8")
    lowered = text.lower()
    for forbidden in forbidden_text:
        assert forbidden not in lowered, forbidden

    tree = ast.parse(text)
    prohibited_imports = {
        "os",
        "subprocess",
        "threading",
        "signal",
        "socket",
        "requests",
        "httpx",
        "pathlib",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = {alias.name for alias in node.names}
            assert imported.isdisjoint(prohibited_imports), imported
        if isinstance(node, ast.ImportFrom):
            assert node.module not in prohibited_imports

    assert not hasattr(ra, "RuntimeEventJournal")
    assert not hasattr(ra, "RuntimeEventDescriptor")
    assert not hasattr(ra, "NormalizedRuntimeFailure")
    assert "RuntimeEventJournal" not in ra.__all__
