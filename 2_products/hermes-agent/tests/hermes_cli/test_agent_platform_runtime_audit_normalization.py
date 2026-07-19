from __future__ import annotations

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.audit_normalization import (
    RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION,
    RuntimeAuditEventOrderError,
    RuntimeAuditEventProjection,
    RuntimeAuditEvidenceReferenceError,
    RuntimeAuditProjection,
    project_runtime_operation_audit,
)
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    RuntimeEventJournal,
    normalize_runtime_failure,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import ProcessLaunchError


UTC = timezone.utc
SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "runtime_adapter"
    / "audit_normalization.py"
)


def utc(seconds: int) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=seconds)


def runtime_handle(
    state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.FAILED,
) -> ra.RuntimeHandle:
    return ra.RuntimeHandle(
        schema_version=1,
        runtime_id="runtime.audit.test",
        correlation_id="corr.audit.test",
        profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        workspace_id="ws_audit_test",
        lifecycle_state=state,
        created_at_utc=utc(0),
    )


def evidence_ref(evidence_id: str, evidence_kind: str) -> ra.RuntimeEvidenceRef:
    return ra.RuntimeEvidenceRef(evidence_id=evidence_id, evidence_kind=evidence_kind)


def event_id_factory(*event_ids: str):
    values = iter(event_ids)
    return lambda: next(values)


def failure_for(handle: ra.RuntimeHandle):
    return normalize_runtime_failure(
        error=ProcessLaunchError(
            runtime_id=handle.runtime_id,
            profile_id=handle.profile_id,
            exception_class="HiddenLaunchFailure",
        ),
        runtime_handle=handle,
        process_status=ra.RuntimeProcessStatus.NOT_STARTED,
        workspace_status=ra.RuntimeWorkspaceStatus.ALLOCATED,
        evidence_refs=(evidence_ref("workspace.evidence", "runtime_workspace"),),
        failure_id_factory=lambda: "fail_audit_test",
    )


def failed_result(*, include_failure_event: bool = True) -> ra.RuntimeOperationResult:
    handle = runtime_handle()
    failure = failure_for(handle)
    journal = RuntimeEventJournal(
        runtime_handle=handle,
        event_id_factory=event_id_factory("evt_audit_request", "evt_audit_failed"),
    )
    journal.append(
        event_type=ra.RuntimeEventType.REQUEST_RECEIVED,
        lifecycle_state=ra.RuntimeLifecycleState.CREATED,
        timestamp_utc=utc(0),
        monotonic_offset_ms=0,
    )
    if include_failure_event:
        journal.append(
            event_type=ra.RuntimeEventType.RUNTIME_FAILED,
            lifecycle_state=ra.RuntimeLifecycleState.FAILED,
            timestamp_utc=utc(1),
            monotonic_offset_ms=10,
            normalized_failure=failure,
        )
    return ra.RuntimeOperationResult(
        schema_version=1,
        runtime_handle=handle,
        outcome=ra.RuntimeOperationOutcome.FAILED,
        process_reference=None,
        workspace_reference=ra.RuntimeWorkspaceRef(
            workspace_id=handle.workspace_id,
            workspace_policy_id="runtime.workspace.test.lifecycle_probe.v1",
            status=ra.RuntimeWorkspaceStatus.ALLOCATED,
            managed_files_root_bound=False,
        ),
        readiness_reference=None,
        log_references=(
            ra.RuntimeLogRef(
                stream=ra.RuntimeLogStream.STDOUT,
                evidence_ref=evidence_ref("log.stdout", "runtime_log"),
                captured_bytes=256,
                truncated=False,
            ),
        ),
        failure=failure.failure,
        events=journal.events(),
    )


def success_result() -> ra.RuntimeOperationResult:
    handle = runtime_handle(ra.RuntimeLifecycleState.READY)
    journal = RuntimeEventJournal(
        runtime_handle=handle,
        event_id_factory=event_id_factory("evt_success_request"),
    )
    journal.append(
        event_type=ra.RuntimeEventType.REQUEST_RECEIVED,
        lifecycle_state=ra.RuntimeLifecycleState.CREATED,
        timestamp_utc=utc(0),
        monotonic_offset_ms=0,
    )
    return ra.RuntimeOperationResult(
        schema_version=1,
        runtime_handle=handle,
        outcome=ra.RuntimeOperationOutcome.READY,
        process_reference=None,
        workspace_reference=None,
        readiness_reference=None,
        log_references=(),
        failure=None,
        events=journal.events(),
    )


def manual_event(
    *,
    event_id: str,
    sequence: int,
    timestamp_utc: datetime,
    monotonic_offset_ms: int,
    process_reference: ra.RuntimeEvidenceRef | None = None,
    workspace_reference: ra.RuntimeEvidenceRef | None = None,
    failure_reference: ra.RuntimeEvidenceRef | None = None,
) -> ra.RuntimeEvent:
    handle = runtime_handle(ra.RuntimeLifecycleState.READY)
    return ra.RuntimeEvent(
        schema_version=1,
        event_id=event_id,
        runtime_id=handle.runtime_id,
        correlation_id=handle.correlation_id,
        sequence=sequence,
        event_type=ra.RuntimeEventType.REQUEST_RECEIVED,
        lifecycle_state=ra.RuntimeLifecycleState.CREATED,
        profile_id=handle.profile_id,
        timestamp_utc=timestamp_utc,
        monotonic_offset_ms=monotonic_offset_ms,
        stage=ra.RuntimeFailureStage.REQUEST_VALIDATION,
        severity=ra.RuntimeSeverity.INFO,
        message_code="runtime.request.received",
        sanitized_message="Runtime request received.",
        process_reference=process_reference,
        workspace_reference=workspace_reference,
        readiness_reference=None,
        failure_reference=failure_reference,
    )


def operation_result_with_events(
    events: tuple[ra.RuntimeEvent, ...],
) -> ra.RuntimeOperationResult:
    handle = runtime_handle(ra.RuntimeLifecycleState.READY)
    return ra.RuntimeOperationResult(
        schema_version=1,
        runtime_handle=handle,
        outcome=ra.RuntimeOperationOutcome.READY,
        process_reference=None,
        workspace_reference=None,
        readiness_reference=None,
        log_references=(),
        failure=None,
        events=events,
    )


def test_audit_projection_preserves_safe_fields_and_evidence_refs() -> None:
    projection = project_runtime_operation_audit(failed_result())

    assert projection.schema_version == RUNTIME_AUDIT_PROJECTION_SCHEMA_VERSION
    assert projection.projection_kind == "runtime_audit_projection"
    assert projection.authority == "non_authoritative"
    assert projection.event_count == 2
    assert projection.failure is not None
    assert projection.failure.failure_id == "fail_audit_test"
    assert projection.failure.sanitized_summary == "Runtime process launch failed."
    assert projection.log_evidence_refs == (evidence_ref("log.stdout", "runtime_log"),)
    assert projection.workspace_evidence_present is True
    assert projection.process_evidence_present is False
    assert projection.readiness_evidence_present is False
    assert projection.events[1].evidence_refs == (
        evidence_ref("fail_audit_test", "runtime_failure"),
    )
    assert not hasattr(projection, "process_reference")
    assert not hasattr(projection, "workspace_reference")
    assert "HiddenLaunchFailure" not in repr(projection)


def test_audit_projection_rejects_missing_and_mismatched_failure_references() -> None:
    with pytest.raises(RuntimeAuditEvidenceReferenceError):
        project_runtime_operation_audit(failed_result(include_failure_event=False))

    result = failed_result()
    wrong_failure_ref = evidence_ref("fail_other", "runtime_failure")
    mismatched_event = ra.RuntimeEvent(**{
        **result.events[1].model_dump(),
        "failure_reference": wrong_failure_ref,
    })
    mismatched_result = ra.RuntimeOperationResult(**{
        **result.model_dump(),
        "events": (result.events[0], mismatched_event),
    })
    with pytest.raises(RuntimeAuditEvidenceReferenceError):
        project_runtime_operation_audit(mismatched_result)


def test_audit_projection_rejects_event_order_and_evidence_ambiguity() -> None:
    out_of_order = operation_result_with_events((
        manual_event(
            event_id="evt_order_1",
            sequence=0,
            timestamp_utc=utc(2),
            monotonic_offset_ms=20,
        ),
        manual_event(
            event_id="evt_order_2",
            sequence=1,
            timestamp_utc=utc(1),
            monotonic_offset_ms=21,
        ),
    ))
    with pytest.raises(RuntimeAuditEventOrderError):
        project_runtime_operation_audit(out_of_order)

    duplicate_evidence = operation_result_with_events((
        manual_event(
            event_id="evt_duplicate_evidence",
            sequence=0,
            timestamp_utc=utc(0),
            monotonic_offset_ms=0,
            process_reference=evidence_ref("shared.evidence", "runtime_process"),
            workspace_reference=evidence_ref("shared.evidence", "runtime_workspace"),
        ),
    ))
    with pytest.raises(RuntimeAuditEvidenceReferenceError):
        project_runtime_operation_audit(duplicate_evidence)


def test_audit_projection_models_are_frozen_bounded_and_not_root_exported() -> None:
    projection = project_runtime_operation_audit(success_result())

    with pytest.raises(ValidationError):
        projection.event_count = 0
    with pytest.raises(ValidationError):
        RuntimeAuditProjection(**{**projection.model_dump(), "event_count": 999})
    with pytest.raises(ValidationError):
        RuntimeAuditEventProjection(**{
            **projection.events[0].model_dump(),
            "evidence_refs": (
                evidence_ref("z.ref", "runtime_workspace"),
                evidence_ref("a.ref", "runtime_process"),
            ),
        })

    assert not hasattr(ra, "RuntimeAuditProjection")
    assert not hasattr(ra, "project_runtime_operation_audit")
    assert "RuntimeAuditProjection" not in ra.__all__


def test_audit_normalization_source_guard_blocks_runtime_and_persistence_authority() -> (
    None
):
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
        "sqlite",
        "audit_log",
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
        "sqlite3",
        "pathlib",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = {alias.name for alias in node.names}
            assert imported.isdisjoint(prohibited_imports), imported
        if isinstance(node, ast.ImportFrom):
            assert node.module not in prohibited_imports
