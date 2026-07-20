"""Test-only P14.7 runtime-adapter conformance harness."""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path, PureWindowsPath
from types import MappingProxyType

from pydantic import ValidationError

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.audit_normalization import (
    project_runtime_operation_audit,
)
from hermes_cli.agent_platform.runtime_adapter.environment import (
    InvalidRuntimeEnvironmentPathError,
    RuntimePlatformFamily,
    sanitize_runtime_environment,
)
from hermes_cli.agent_platform.runtime_adapter.event_normalization import (
    RuntimeEventJournal,
    RuntimeFailureNormalizationError,
    normalize_runtime_failure,
)
from hermes_cli.agent_platform.runtime_adapter.lifecycle_control import (
    RuntimeLifecycleClock,
    RuntimeLifecycleOperationConflictError,
    RuntimeTerminationCoordinator,
)
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    PathOutsideContainmentRootError,
    RuntimePathContainmentError,
    assert_existing_path_contained,
    assert_path_chain_safe,
    validate_safe_path_segment,
)
from hermes_cli.agent_platform.runtime_adapter.process_owner import (
    DuplicateRuntimeOwnershipError,
    HermesProcessOwner,
    InvalidListenerOwnershipError,
    OwnedProcessDrainIncompleteError,
    OwnedProcessGracefulStopResult,
    OwnedProcessSnapshot,
    OwnedProcessStillRunningError,
    ResolvedProcessLaunchPlan,
    RuntimeProcessOwnerError,
    UnknownRuntimeOwnershipError,
)
from hermes_cli.agent_platform.runtime_adapter.process_tree import ProcessTreeBackend
from hermes_cli.agent_platform.runtime_adapter.profiles import (
    RuntimeArgumentSelector,
    RuntimeExecutionScope,
    RuntimeExecutableSelector,
    UnknownRuntimeProfileError,
    get_runtime_profile,
)
from hermes_cli.agent_platform.runtime_adapter.rollback import (
    RuntimeWorkspaceRollbackCoordinator,
)
from hermes_cli.agent_platform.runtime_adapter.stream_capture import (
    BoundedStreamSnapshot,
)
from hermes_cli.agent_platform.runtime_adapter.workspace import (
    DuplicateRuntimeWorkspaceError,
    RuntimeWorkspaceAllocation,
    RuntimeWorkspaceAllocator,
    UnknownRuntimeWorkspaceError,
    validate_managed_files_path,
)


UTC = timezone.utc
EXPECTED_CASE_IDS = (
    "CONTRACT-001",
    "CONTRACT-002",
    "PROFILE-001",
    "PROFILE-002",
    "ENVIRONMENT-001",
    "ENVIRONMENT-002",
    "ENVIRONMENT-003",
    "WORKSPACE-001",
    "WORKSPACE-002",
    "PATH-001",
    "PROCESS-001",
    "PROCESS-002",
    "STREAM-001",
    "CANCELLATION-001",
    "CANCELLATION-002",
    "SHUTDOWN-001",
    "SHUTDOWN-002",
    "ROLLBACK-001",
    "ROLLBACK-002",
    "EVENT-001",
    "AUDIT-001",
    "FAILURE-001",
    "CONCURRENCY-001",
    "CLEANUP-001",
)
ALLOWED_SKIP_REASONS = frozenset({
    "host.symlink_creation_unavailable",
    "host.windows_junction_creation_unavailable",
    "host.graceful_signal_unavailable",
    "host.process_tree_inspection_unavailable",
    "host.special_file_creation_unavailable",
})
PROHIBITED_ENVIRONMENT_NAMES = frozenset({
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AWS_ACCESS_KEY_ID",
    "AZURE_CLIENT_SECRET",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GITHUB_TOKEN",
    "SSH_AUTH_SOCK",
    "MCP_TOKEN",
    "HTTP_PROXY",
    "PYTHONPATH",
    "NODE_OPTIONS",
})
MARKER_NAME = ".agent-platform-runtime-workspace.json"
_PROCESS_WAIT_TIMEOUT_MS = 15_000
_MAX_FAILURE_EVIDENCE_CHARACTERS = 160


class RuntimeAdapterConformanceOutcome(StrEnum):
    PASSED = "passed"
    SKIPPED_CAPABILITY = "skipped_capability"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class RuntimeAdapterConformanceCase:
    case_id: str
    title: str


@dataclass(frozen=True, slots=True)
class RuntimeAdapterConformanceResult:
    case_id: str
    outcome: RuntimeAdapterConformanceOutcome
    reason_code: str | None = None
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RuntimeAdapterConformanceSummary:
    results: tuple[RuntimeAdapterConformanceResult, ...]

    @property
    def passed_case_ids(self) -> tuple[str, ...]:
        return tuple(
            result.case_id
            for result in self.results
            if result.outcome is RuntimeAdapterConformanceOutcome.PASSED
        )

    @property
    def skipped_case_ids(self) -> tuple[str, ...]:
        return tuple(
            result.case_id
            for result in self.results
            if result.outcome is RuntimeAdapterConformanceOutcome.SKIPPED_CAPABILITY
        )

    @property
    def failed_case_ids(self) -> tuple[str, ...]:
        return tuple(
            result.case_id
            for result in self.results
            if result.outcome is RuntimeAdapterConformanceOutcome.FAILED
        )

    @property
    def skipped_reasons(self) -> MappingProxyType:
        return MappingProxyType({
            result.case_id: result.reason_code
            for result in self.results
            if result.outcome is RuntimeAdapterConformanceOutcome.SKIPPED_CAPABILITY
        })


@dataclass(frozen=True, slots=True)
class _RuntimeContext:
    runtime_id: str
    profile: object
    allocator: RuntimeWorkspaceAllocator
    owner: HermesProcessOwner
    allocation: RuntimeWorkspaceAllocation
    handle: ra.RuntimeHandle
    source_environment: MappingProxyType
    sanitized_environment: object | None = None


class _ConformanceSkip(RuntimeError):
    def __init__(self, reason_code: str) -> None:
        self.reason_code = reason_code
        super().__init__(reason_code)


class _ConformanceAssertionError(AssertionError):
    error_code = "conformance.assertion_failed"

    def __init__(
        self,
        *,
        category: str,
        expected: str,
        observed: object,
        stage: str,
    ) -> None:
        self.category = _safe_evidence_text(category)
        self.expected = _safe_evidence_text(expected)
        self.observed = _safe_evidence_text(observed)
        self.stage = _safe_evidence_text(stage)
        self.evidence = (
            f"code={self.error_code}",
            f"category={self.category}",
            f"stage={self.stage}",
            f"expected={self.expected}",
            f"observed={self.observed}",
        )
        super().__init__(" ".join(self.evidence))


class _GracefulTimeoutProcessOwner:
    def __init__(self, owner: HermesProcessOwner) -> None:
        self._owner = owner

    def request_graceful_stop(
        self,
        runtime_id: str,
        *,
        timeout_ms: int,
    ) -> OwnedProcessGracefulStopResult:
        return OwnedProcessGracefulStopResult(
            runtime_id=runtime_id,
            mechanism=(
                "windows_ctrl_break" if sys.platform == "win32" else "posix_sigterm"
            ),
            supported=True,
            exit_observed=False,
            timed_out=True,
            snapshot=self._owner.snapshot(runtime_id),
        )

    def terminate_owned_tree(
        self,
        runtime_id: str,
        *,
        timeout_ms: int,
    ) -> OwnedProcessSnapshot:
        return self._owner.terminate_owned_tree(runtime_id, timeout_ms=timeout_ms)

    def release(self, runtime_id: str) -> None:
        self._owner.release(runtime_id)

    def owned_runtime_ids(self) -> tuple[str, ...]:
        return self._owner.owned_runtime_ids()


class ConformanceExecutionDenied(RuntimeError):
    error_code = "conformance.profile.execution_scope_denied"

    def __init__(self, profile_id: str) -> None:
        self.profile_id = profile_id
        super().__init__(f"code={self.error_code} profile_id={profile_id}")


class _DeterministicClock(RuntimeLifecycleClock):
    def __init__(self) -> None:
        self._timestamp = datetime(2026, 1, 1, tzinfo=UTC)
        self._offset_ms = 0

    def utc_now(self) -> datetime:
        value = self._timestamp
        self._timestamp = self._timestamp + timedelta(milliseconds=10)
        return value

    def monotonic_offset_ms(self) -> int:
        value = self._offset_ms
        self._offset_ms += 10
        return value


CASES = tuple(
    RuntimeAdapterConformanceCase(case_id=case_id, title=case_id.lower())
    for case_id in EXPECTED_CASE_IDS
)


class RuntimeAdapterConformanceHarness:
    """Compose P14 internals under inert, test-only conditions."""

    def __init__(
        self,
        *,
        tmp_path: Path,
        python_executable: str | None = None,
        lifecycle_probe: Path | None = None,
    ) -> None:
        self._tmp_path = Path(tmp_path)
        self._python_executable = python_executable or sys.executable
        self._probe = lifecycle_probe or Path(__file__).with_name(
            "runtime_adapter_lifecycle_probe.py"
        )
        self._sequence = 0
        self._known_pids: set[int] = set()

    def registered_cases(self) -> tuple[RuntimeAdapterConformanceCase, ...]:
        return CASES

    def run_all(self) -> RuntimeAdapterConformanceSummary:
        return RuntimeAdapterConformanceSummary(
            results=tuple(self.run_case(case.case_id) for case in CASES)
        )

    def run_case(self, case_id: str) -> RuntimeAdapterConformanceResult:
        dispatch = {
            "CONTRACT-001": self._case_contract_authority,
            "CONTRACT-002": self._case_contract_round_trip,
            "PROFILE-001": self._case_test_profile,
            "PROFILE-002": self._case_dashboard_profile_denied,
            "ENVIRONMENT-001": self._case_synthetic_environment,
            "ENVIRONMENT-002": self._case_child_home,
            "ENVIRONMENT-003": self._case_provider_null_child,
            "WORKSPACE-001": self._case_test_workspace,
            "WORKSPACE-002": self._case_dashboard_workspace,
            "PATH-001": self._case_path_escape_matrix,
            "PROCESS-001": self._case_natural_process,
            "PROCESS-002": self._case_process_tree,
            "STREAM-001": self._case_stream_bounding,
            "CANCELLATION-001": self._case_pre_process_cancellation,
            "CANCELLATION-002": self._case_active_cancellation,
            "SHUTDOWN-001": self._case_graceful_shutdown,
            "SHUTDOWN-002": self._case_forced_shutdown,
            "ROLLBACK-001": self._case_successful_rollback,
            "ROLLBACK-002": self._case_marker_failure,
            "EVENT-001": self._case_event_sequence,
            "AUDIT-001": self._case_audit_projection,
            "FAILURE-001": self._case_failure_matrix,
            "CONCURRENCY-001": self._case_concurrency,
            "CLEANUP-001": self._case_cleanup,
        }
        if case_id not in dispatch:
            return RuntimeAdapterConformanceResult(
                case_id=case_id,
                outcome=RuntimeAdapterConformanceOutcome.FAILED,
                reason_code="conformance.unknown_case",
            )
        try:
            evidence = dispatch[case_id]()
        except _ConformanceSkip as exc:
            return RuntimeAdapterConformanceResult(
                case_id=case_id,
                outcome=RuntimeAdapterConformanceOutcome.SKIPPED_CAPABILITY,
                reason_code=exc.reason_code,
            )
        except Exception as exc:
            reason_code = getattr(exc, "error_code", "conformance.case_failed")
            return RuntimeAdapterConformanceResult(
                case_id=case_id,
                outcome=RuntimeAdapterConformanceOutcome.FAILED,
                reason_code=reason_code,
                evidence=_failure_evidence(exc),
            )
        return RuntimeAdapterConformanceResult(
            case_id=case_id,
            outcome=RuntimeAdapterConformanceOutcome.PASSED,
            evidence=tuple(evidence),
        )

    def _case_contract_authority(self) -> tuple[str, ...]:
        _assert(ra.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION == 1)
        forbidden_launch = {"executable", "argv", "arguments", "environment", "cwd"}
        _assert(forbidden_launch.isdisjoint(ra.RuntimeLaunchRequest.model_fields))
        _assert("signal" not in ra.RuntimeStopRequest.model_fields)
        _assert("pid" not in ra.RuntimeCancelRequest.model_fields)
        _assert("path" not in ra.RuntimeRollbackRequest.model_fields)
        _assert(not hasattr(ra, "RuntimeAdapterConformanceHarness"))
        _assert(not hasattr(ra, "GovernedRuntimeAdapter"))
        _assert("RuntimeAdapterConformanceHarness" not in ra.__all__)
        return ("contract_authority_preserved",)

    def _case_contract_round_trip(self) -> tuple[str, ...]:
        request = self._launch_request()
        handle = self._handle("rt.p147.contract", "ws_" + "1" * 32)
        process_ref = ra.RuntimeProcessRef(
            launcher_pid=12345,
            listener_pid=None,
            descendant_pids=(),
            process_status=ra.RuntimeProcessStatus.EXITED,
            started_at_utc=_utc_now(),
            exited_at_utc=_utc_now(),
            exit_code=0,
        )
        workspace_ref = ra.RuntimeWorkspaceRef(
            workspace_id=handle.workspace_id,
            workspace_policy_id="runtime.workspace.test.lifecycle_probe.v1",
            status=ra.RuntimeWorkspaceStatus.ALLOCATED,
            managed_files_root_bound=False,
        )
        failure = ra.RuntimeFailure(
            schema_version=1,
            failure_id="fail_p147_contract",
            runtime_id=handle.runtime_id,
            profile_id=handle.profile_id,
            stage=ra.RuntimeFailureStage.REQUEST_VALIDATION,
            failure_code="runtime_contract_validation_error",
            sanitized_summary="Runtime contract validation failed.",
            retryability=ra.RuntimeRetryability.NEVER,
            cleanup_status=ra.RuntimeCleanupStatus.NOT_STARTED,
            process_status=ra.RuntimeProcessStatus.NOT_STARTED,
            workspace_status=ra.RuntimeWorkspaceStatus.UNALLOCATED,
            evidence_refs=(),
        )
        event = ra.RuntimeEvent(
            schema_version=1,
            event_id="evt_p147_contract",
            runtime_id=handle.runtime_id,
            correlation_id=handle.correlation_id,
            sequence=0,
            event_type=ra.RuntimeEventType.RUNTIME_FAILED,
            lifecycle_state=ra.RuntimeLifecycleState.FAILED,
            profile_id=handle.profile_id,
            timestamp_utc=_utc_now(),
            monotonic_offset_ms=0,
            stage=ra.RuntimeFailureStage.REQUEST_VALIDATION,
            severity=ra.RuntimeSeverity.ERROR,
            message_code="runtime.failed",
            sanitized_message="Runtime operation failed.",
            process_reference=None,
            workspace_reference=None,
            readiness_reference=None,
            failure_reference=ra.RuntimeEvidenceRef(
                evidence_id=failure.failure_id,
                evidence_kind="runtime_failure",
            ),
        )
        failed_handle = self._handle(
            handle.runtime_id,
            handle.workspace_id,
            state=ra.RuntimeLifecycleState.FAILED,
        )
        result = ra.RuntimeOperationResult(
            schema_version=1,
            runtime_handle=failed_handle,
            outcome=ra.RuntimeOperationOutcome.FAILED,
            process_reference=None,
            workspace_reference=None,
            readiness_reference=None,
            log_references=(),
            failure=failure,
            events=(event,),
        )
        for model in (
            request,
            handle,
            process_ref,
            workspace_ref,
            event,
            failure,
            result,
        ):
            _assert_round_trip(model)
            _assert_frozen(model)
        with _expect_error():
            ra.RuntimeLaunchRequest(**{**request.model_dump(), "extra": True})
        return ("immutable_contract_round_trip",)

    def _case_test_profile(self) -> tuple[str, ...]:
        profile = get_runtime_profile(ra.TEST_LIFECYCLE_PROBE_PROFILE_ID)
        _assert(profile.execution_scope is RuntimeExecutionScope.INERT_TEST_ONLY)
        _assert(
            profile.executable_selector
            is RuntimeExecutableSelector.CURRENT_PRODUCT_PYTHON
        )
        _assert(profile.argument_selector is RuntimeArgumentSelector.LIFECYCLE_PROBE)
        _assert(profile.profile_ref.files_root_policy_id is None)
        _assert(not profile.default_workspace_binding.require_managed_files_root)
        return ("test_profile_resolved",)

    def _case_dashboard_profile_denied(self) -> tuple[str, ...]:
        profile = get_runtime_profile(ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID)
        _assert(profile.execution_scope is RuntimeExecutionScope.P14_8_ONLY)
        _assert(profile.default_workspace_binding.require_managed_files_root)
        ctx = self._allocate_context(
            "profile.dashboard",
            profile_id=ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID,
        )
        try:
            with _expect_error(ConformanceExecutionDenied) as captured:
                self._launch_plan(ctx, "--sleep-ms", "10")
            _assert(captured.error_code == "conformance.profile.execution_scope_denied")
        finally:
            self._cleanup_context(ctx)
        return ("dashboard_execution_denied",)

    def _case_synthetic_environment(self) -> tuple[str, ...]:
        ctx = self._allocate_context("env.synthetic")
        try:
            sanitized = self._sanitize(ctx)
            mapping = sanitized.as_mapping()
            _assert("PATH" not in {key.upper() for key in mapping})
            _assert(not PROHIBITED_ENVIRONMENT_NAMES & {key.upper() for key in mapping})
            _assert(sanitized.report.provider_variables_present_in_output is False)
            _assert(sanitized.report.managed_home_bound is True)
            _assert(sanitized.report.excluded_variable_count >= 10)
        finally:
            self._cleanup_context(ctx)
        return ("synthetic_environment_isolated",)

    def _case_child_home(self) -> tuple[str, ...]:
        ctx = self._allocate_context("env.child.home")
        try:
            self._sanitize(ctx)
            snapshot = self._launch_and_wait(
                ctx,
                "--verify-managed-environment",
                "--expected-workspace-root",
                str(ctx.allocation.paths.workspace_root),
            )
            _assert(snapshot.process_reference.exit_code == 0)
            _assert(snapshot.stdout_snapshot.total_bytes_read == 0)
            _assert(snapshot.stderr_snapshot.total_bytes_read == 0)
        finally:
            self._cleanup_context(ctx)
        return ("child_home_isolated",)

    def _case_provider_null_child(self) -> tuple[str, ...]:
        ctx = self._allocate_context("env.provider.null")
        try:
            self._sanitize(ctx)
            snapshot = self._launch_and_wait(
                ctx,
                "--verify-provider-null",
                "--expect-no-path",
            )
            _assert(snapshot.process_reference.exit_code == 0)
        finally:
            self._cleanup_context(ctx)
        return ("provider_null_child",)

    def _case_test_workspace(self) -> tuple[str, ...]:
        ctx = self._allocate_context("workspace.test")
        try:
            allocation = ctx.allocation
            _assert(allocation.workspace_ref.workspace_id.startswith("ws_"))
            _assert(
                allocation.paths.workspace_root.parent == self._base_for(ctx.runtime_id)
            )
            _assert(
                allocation.workspace_ref.status is ra.RuntimeWorkspaceStatus.ALLOCATED
            )
            _assert(allocation.files_root_binding is None)
            _assert(allocation.paths.files_root is None)
            _assert(allocation.paths.ownership_marker.name == MARKER_NAME)
            marker = json.loads(
                allocation.paths.ownership_marker.read_text(encoding="utf-8")
            )
            _assert(marker["runtime_id"] == allocation.runtime_id)
        finally:
            self._cleanup_context(ctx)
        return ("test_workspace_allocated",)

    def _case_dashboard_workspace(self) -> tuple[str, ...]:
        ctx = self._allocate_context(
            "workspace.dashboard",
            profile_id=ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID,
        )
        try:
            binding = ctx.allocation.files_root_binding
            _assert(binding is not None)
            _assert(binding.default_path == binding.locked_root)
            _assert(binding.can_change_path is False)
            _assert(ctx.allocation.paths.files_root is not None)
            with _expect_error(RuntimePathContainmentError):
                validate_managed_files_path(
                    binding,
                    binding.locked_root.parent / "files-root-sibling",
                    require_exists=False,
                )
            with _expect_error(RuntimePathContainmentError):
                validate_managed_files_path(
                    binding,
                    self._tmp_path / "outside-files-root",
                    require_exists=False,
                )
        finally:
            self._cleanup_context(ctx)
        return ("dashboard_workspace_files_root_locked",)

    def _case_path_escape_matrix(self) -> tuple[str, ...]:
        root = self._tmp_path / self._token("path-root")
        root.mkdir()
        safe = root / "safe"
        safe.mkdir()
        with _expect_error(RuntimePathContainmentError):
            assert_path_chain_safe(root / ".." / "escape", containment_root=root)
        with _expect_error(RuntimePathContainmentError):
            assert_path_chain_safe(self._tmp_path / "outside", containment_root=root)
        sibling = root.parent / f"{root.name}-sibling"
        sibling.mkdir()
        with _expect_error(PathOutsideContainmentRootError):
            assert_existing_path_contained(sibling, containment_root=root)
        with _expect_error(RuntimePathContainmentError):
            validate_safe_path_segment("unsafe/child")
        with _expect_error(RuntimePathContainmentError):
            assert_path_chain_safe(
                root / "bad.." / ".." / "child", containment_root=root
            )
        if sys.platform == "win32":
            with _expect_error(RuntimePathContainmentError):
                assert_path_chain_safe(Path(r"\\server\share\x"), containment_root=root)
            with _expect_error(RuntimePathContainmentError):
                assert_path_chain_safe(Path(r"\\?\C:\x"), containment_root=root)
            drive = PureWindowsPath(str(root)).drive or "C:"
            other_drive = "Z:" if drive.casefold() != "Z:" else "Y:"
            with _expect_error(RuntimePathContainmentError):
                assert_path_chain_safe(Path(other_drive + r"\x"), containment_root=root)
        try:
            link = root / "link"
            os.symlink(safe, link)
        except (OSError, NotImplementedError):
            return ("path_escape_matrix_without_symlink",)
        with _expect_error(RuntimePathContainmentError):
            assert_existing_path_contained(link, containment_root=root)
        return ("path_escape_matrix",)

    def _case_natural_process(self) -> tuple[str, ...]:
        ctx = self._allocate_context("process.natural")
        try:
            self._sanitize(ctx)
            snapshot = self._launch_and_wait(
                ctx, "--sleep-ms", "10", "--exit-code", "0"
            )
            _assert(
                snapshot.process_reference.launcher_pid is not None,
                category="launcher_pid_missing",
                expected="launcher_pid_present",
                observed=_snapshot_observed_state(snapshot),
                stage="process_natural_exit",
            )
            _assert(
                snapshot.process_reference.exit_code == 0,
                category="unexpected_exit_code",
                expected="exit_code=0",
                observed=_snapshot_observed_state(snapshot),
                stage="process_natural_exit",
            )
            _assert(
                snapshot.process_reference.exited_at_utc is not None,
                category="exit_timestamp_missing",
                expected="exited_at_present",
                observed=_snapshot_observed_state(snapshot),
                stage="process_natural_exit",
            )
            _assert(
                ctx.runtime_id not in ctx.owner.owned_runtime_ids(),
                category="owner_release_incomplete",
                expected="runtime_owner_released",
                observed=f"owned_runtime_count={len(ctx.owner.owned_runtime_ids())}",
                stage="process_natural_release",
            )
        finally:
            self._cleanup_context(ctx)
        return ("natural_process_lifecycle",)

    def _case_process_tree(self) -> tuple[str, ...]:
        ctx = self._allocate_context("process.tree")
        try:
            self._sanitize(ctx)
            launched = self._launch(
                ctx,
                "--sleep-ms",
                "5000",
                "--spawn-child",
                "--child-sleep-ms",
                "5000",
            )
            _assert(launched.process_reference.launcher_pid is not None)
            snapshot = self._wait_for_snapshot(
                ctx.owner,
                ctx.runtime_id,
                lambda snap: bool(snap.process_reference.descendant_pids),
                timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
                stage="process_tree_descendant_observed",
            )
            _assert(snapshot.process_reference.descendant_pids)
            ctx.owner.bind_listener_pid(
                ctx.runtime_id, launched.process_reference.launcher_pid
            )
            ctx.owner.bind_listener_pid(
                ctx.runtime_id, snapshot.process_reference.descendant_pids[0]
            )
            with _expect_error(InvalidListenerOwnershipError):
                ctx.owner.bind_listener_pid(ctx.runtime_id, os.getpid())
            terminated = ctx.owner.terminate_owned_tree(
                ctx.runtime_id,
                timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
            )
            _assert(
                terminated.process_reference.process_status
                is not ra.RuntimeProcessStatus.RUNNING
            )
            ctx.owner.release(ctx.runtime_id)
            _assert(ctx.runtime_id not in ctx.owner.owned_runtime_ids())
        finally:
            self._cleanup_context(ctx)
        return ("exact_tree_ownership",)

    def _case_stream_bounding(self) -> tuple[str, ...]:
        small = self._allocate_context("stream.small")
        large = self._allocate_context("stream.large")
        try:
            self._sanitize(small)
            small_snapshot = self._launch_and_wait(
                small,
                "--stdout-bytes",
                "32",
                "--stderr-bytes",
                "32",
                stdout_limit_bytes=1024,
                stderr_limit_bytes=1024,
            )
            _assert(small_snapshot.stdout_snapshot.truncated is False)
            _assert(small_snapshot.stderr_snapshot.truncated is False)
            self._sanitize(large)
            large_snapshot = self._launch_and_wait(
                large,
                "--stdout-bytes",
                "3000",
                "--stderr-bytes",
                "3000",
                stdout_limit_bytes=1024,
                stderr_limit_bytes=1024,
            )
            for stream_snapshot in (
                large_snapshot.stdout_snapshot,
                large_snapshot.stderr_snapshot,
            ):
                _assert(stream_snapshot.total_bytes_read == 3000)
                _assert(stream_snapshot.bounded_bytes == 1024)
                _assert(stream_snapshot.discarded_bytes == 1976)
                _assert(stream_snapshot.truncated is True)
                _assert(stream_snapshot.drain_complete is True)
        finally:
            self._cleanup_context(small)
            self._cleanup_context(large)
        return ("bounded_streams",)

    def _case_pre_process_cancellation(self) -> tuple[str, ...]:
        for state in (
            ra.RuntimeLifecycleState.CREATED,
            ra.RuntimeLifecycleState.VALIDATING,
        ):
            handle = self._handle(
                self._runtime_id(f"cancel.{state.value}"),
                "ws_" + "2" * 32,
                state=state,
            )
            journal = self._journal(handle)
            result = RuntimeTerminationCoordinator(
                process_owner=HermesProcessOwner(),
                clock=_DeterministicClock(),
            ).cancel(
                request=self._cancel_request(handle),
                runtime_handle=handle,
                event_journal=journal,
                timeout_policy=get_runtime_profile(
                    ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
                ).timeout_policy,
            )
            _assert(result.outcome is ra.RuntimeOperationOutcome.CANCELLED)
            _assert(
                result.runtime_handle.lifecycle_state
                is ra.RuntimeLifecycleState.CANCELLED
            )
            _assert(result.process_reference is None)
        return ("pre_process_cancellation",)

    def _case_active_cancellation(self) -> tuple[str, ...]:
        ctx = self._allocate_context("cancel.active")
        try:
            self._sanitize(ctx)
            self._launch(ctx, "--sleep-ms", "5000")
            result = RuntimeTerminationCoordinator(
                process_owner=ctx.owner,
                clock=_DeterministicClock(),
            ).cancel(
                request=self._cancel_request(ctx.handle),
                runtime_handle=ctx.handle,
                event_journal=self._journal(ctx.handle),
                timeout_policy=get_runtime_profile(
                    ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
                ).timeout_policy,
            )
            _assert(result.outcome is ra.RuntimeOperationOutcome.CANCELLED)
            _assert(ctx.runtime_id not in ctx.owner.owned_runtime_ids())
            _assert(ctx.allocation.paths.workspace_root.exists())
            event_types = tuple(event.event_type for event in result.events)
            _assert(event_types[0] is ra.RuntimeEventType.CANCELLATION_REQUESTED)
            _assert(event_types[-1] is ra.RuntimeEventType.PROCESS_EXITED)
        finally:
            self._cleanup_context(ctx)
        return ("active_cancellation",)

    def _case_graceful_shutdown(self) -> tuple[str, ...]:
        ctx = self._allocate_context("shutdown.graceful")
        try:
            self._sanitize(ctx)
            launched = self._launch(
                ctx,
                "--sleep-ms",
                "5000",
                "--graceful-exit-code",
                "0",
            )
            _assert(launched.process_reference.launcher_pid is not None)
            ctx.owner.bind_listener_pid(
                ctx.runtime_id, launched.process_reference.launcher_pid
            )
            result = self._shutdown(ctx)
            _assert(result.outcome is ra.RuntimeOperationOutcome.STOPPED)
            _assert(
                ra.RuntimeEventType.FORCED_TERMINATION_STARTED
                not in _event_types(result)
            )
            _assert(ra.RuntimeEventType.LISTENER_RELEASED in _event_types(result))
            _assert(ctx.runtime_id not in ctx.owner.owned_runtime_ids())
            _assert(ctx.allocation.paths.workspace_root.exists())
        finally:
            self._cleanup_context(ctx)
        return ("graceful_shutdown",)

    def _case_forced_shutdown(self) -> tuple[str, ...]:
        ctx = self._allocate_context("shutdown.forced")
        try:
            self._sanitize(ctx)
            launched = self._launch(
                ctx,
                "--sleep-ms",
                "10000",
                "--spawn-child",
                "--child-sleep-ms",
                "10000",
                "--ignore-graceful-stop",
            )
            _assert(launched.process_reference.launcher_pid is not None)
            self._wait_for_snapshot(
                ctx.owner,
                ctx.runtime_id,
                lambda snap: bool(snap.process_reference.descendant_pids),
                timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
                stage="forced_shutdown_descendant_observed",
            )
            result = self._shutdown(
                ctx,
                graceful_ms=100,
                process_owner=_GracefulTimeoutProcessOwner(ctx.owner),
            )
            _assert(result.outcome is ra.RuntimeOperationOutcome.STOPPED)
            _assert(
                ra.RuntimeEventType.FORCED_TERMINATION_STARTED in _event_types(result)
            )
            _assert(result.process_reference is not None)
            _assert(result.process_reference.descendant_pids == ())
            _assert(ctx.runtime_id not in ctx.owner.owned_runtime_ids())
            _assert(ctx.allocation.paths.workspace_root.exists())
        finally:
            self._cleanup_context(ctx)
        return ("forced_fallback",)

    def _case_successful_rollback(self) -> tuple[str, ...]:
        ctx = self._allocate_context("rollback.success")
        sibling = ctx.allocation.paths.workspace_root.parent / ("ws_" + "9" * 32)
        sibling.mkdir()
        try:
            self._sanitize(ctx)
            self._launch(ctx, "--sleep-ms", "5000", "--graceful-exit-code", "0")
            stopped = self._shutdown(ctx)
            result = self._rollback(ctx, stopped.runtime_handle)
            _assert(result.outcome is ra.RuntimeOperationOutcome.ROLLED_BACK)
            _assert(not ctx.allocation.paths.workspace_root.exists())
            _assert(sibling.is_dir())
            _assert(
                tuple(event.event_type for event in result.events[-4:])
                == (
                    ra.RuntimeEventType.ROLLBACK_STARTED,
                    ra.RuntimeEventType.WORKSPACE_CLEANUP_STARTED,
                    ra.RuntimeEventType.WORKSPACE_CLEANUP_COMPLETED,
                    ra.RuntimeEventType.ROLLBACK_COMPLETED,
                )
            )
            with _expect_error(UnknownRuntimeWorkspaceError):
                ctx.allocator.get(ctx.runtime_id)
        finally:
            self._cleanup_context(ctx)
        return ("successful_rollback",)

    def _case_marker_failure(self) -> tuple[str, ...]:
        ctx = self._allocate_context("rollback.marker")
        sibling = ctx.allocation.paths.workspace_root.parent / ("ws_" + "8" * 32)
        sibling.mkdir()
        try:
            ctx.allocation.paths.ownership_marker.write_text(
                json.dumps({"schema_version": 1, "runtime_id": "rt.other"}),
                encoding="utf-8",
            )
            stopped = self._handle(
                ctx.runtime_id,
                ctx.allocation.workspace_ref.workspace_id,
                state=ra.RuntimeLifecycleState.STOPPED,
            )
            result = self._rollback(ctx, stopped)
            _assert(result.outcome is ra.RuntimeOperationOutcome.ROLLBACK_FAILED)
            _assert(result.failure is not None)
            _assert(result.failure.failure_code == "runtime_rollback_marker_error")
            _assert(ctx.allocation.paths.workspace_root.exists())
            _assert(sibling.is_dir())
            _assert(ctx.allocator.get(ctx.runtime_id) is ctx.allocation)
            _assert(str(ctx.allocation.paths.workspace_root) not in str(result.failure))
        finally:
            self._restore_marker(ctx.allocation)
            self._cleanup_context(ctx)
        return ("marker_failure_closed",)

    def _case_event_sequence(self) -> tuple[str, ...]:
        result = self._complete_lifecycle("event.sequence")
        event_types = tuple(event.event_type for event in result.events)
        required = (
            ra.RuntimeEventType.REQUEST_RECEIVED,
            ra.RuntimeEventType.PROFILE_RESOLVED,
            ra.RuntimeEventType.WORKSPACE_CREATED,
            ra.RuntimeEventType.ENVIRONMENT_SANITIZED,
            ra.RuntimeEventType.PROCESS_STARTED,
            ra.RuntimeEventType.GRACEFUL_SHUTDOWN_STARTED,
            ra.RuntimeEventType.PROCESS_EXITED,
            ra.RuntimeEventType.ROLLBACK_STARTED,
            ra.RuntimeEventType.WORKSPACE_CLEANUP_STARTED,
            ra.RuntimeEventType.WORKSPACE_CLEANUP_COMPLETED,
            ra.RuntimeEventType.ROLLBACK_COMPLETED,
        )
        for event_type in required:
            _assert(event_type in event_types)
        _assert(ra.RuntimeEventType.RUNTIME_READY not in event_types)
        _assert(
            tuple(event.sequence for event in result.events)
            == tuple(range(len(result.events)))
        )
        _assert(len({event.event_id for event in result.events}) == len(result.events))
        _assert(_nondecreasing(event.timestamp_utc for event in result.events))
        _assert(_nondecreasing(event.monotonic_offset_ms for event in result.events))
        return ("cross_component_event_sequence",)

    def _case_audit_projection(self) -> tuple[str, ...]:
        result = self._complete_lifecycle("audit.projection")
        audit = project_runtime_operation_audit(result)
        _assert(audit.projection_kind == "runtime_audit_projection")
        _assert(audit.authority == "non_authoritative")
        _assert(audit.runtime_id == result.runtime_handle.runtime_id)
        _assert(audit.correlation_id == result.runtime_handle.correlation_id)
        _assert(audit.event_count == len(result.events))
        _assert(
            tuple(event.sequence for event in audit.events)
            == tuple(range(audit.event_count))
        )
        audit_text = audit.model_dump_json()
        _assert(str(self._tmp_path) not in audit_text)
        _assert("OPENAI" not in audit_text)
        _assert("ANTHROPIC" not in audit_text)
        return ("in_memory_audit_projection",)

    def _case_failure_matrix(self) -> tuple[str, ...]:
        failures: list[str] = []
        with _expect_error(UnknownRuntimeProfileError) as unknown_profile:
            get_runtime_profile("unknown.profile")
        failures.append(unknown_profile.error_code)
        with _expect_error(ConformanceExecutionDenied) as dashboard_denied:
            ctx = self._allocate_context(
                "failure.dashboard",
                profile_id=ra.HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID,
            )
            try:
                self._launch_plan(ctx)
            finally:
                self._cleanup_context(ctx)
        failures.append(dashboard_denied.error_code)

        ctx = self._allocate_context("failure.matrix")
        try:
            self._sanitize(ctx)
            self._launch(ctx, "--sleep-ms", "5000")
            with _expect_error(DuplicateRuntimeOwnershipError) as duplicate_owner:
                ctx.owner.launch(ctx.handle, self._launch_plan(ctx))
            failures.append(duplicate_owner.error_code)
            with _expect_error(InvalidListenerOwnershipError) as listener:
                ctx.owner.bind_listener_pid(ctx.runtime_id, os.getpid())
            failures.append(listener.error_code)
            with _expect_error(DuplicateRuntimeWorkspaceError) as duplicate_workspace:
                ctx.allocator.allocate(runtime_id=ctx.runtime_id, profile=ctx.profile)
            failures.append(duplicate_workspace.error_code)
        finally:
            self._cleanup_context(ctx)

        with _expect_error(RuntimePathContainmentError) as path_escape:
            root = self._tmp_path / self._token("failure-path")
            root.mkdir()
            assert_path_chain_safe(
                self._tmp_path / "outside-failure", containment_root=root
            )
        failures.append(path_escape.error_code)

        bad_env = self._allocate_context("failure.env")
        try:
            broken_paths = type(bad_env.allocation.environment_paths)(
                hermes_home="relative",
                home=bad_env.allocation.environment_paths.home,
                user_profile=bad_env.allocation.environment_paths.user_profile,
                app_data=bad_env.allocation.environment_paths.app_data,
                local_app_data=bad_env.allocation.environment_paths.local_app_data,
                temp=bad_env.allocation.environment_paths.temp,
                files_root=bad_env.allocation.environment_paths.files_root,
            )
            with _expect_error(InvalidRuntimeEnvironmentPathError) as invalid_env:
                sanitize_runtime_environment(
                    profile=bad_env.profile,
                    platform_family=self._platform_family(),
                    source_environment=self._synthetic_source_environment(),
                    paths=broken_paths,
                )
            failures.append(invalid_env.error_code)
        finally:
            self._cleanup_context(bad_env)

        handle = self._handle("rt.p147.failure.event", "ws_" + "7" * 32)
        journal = self._journal(handle)
        with _expect_error(Exception) as invalid_event:
            journal.append(
                event_type=ra.RuntimeEventType.PROFILE_RESOLVED,
                lifecycle_state=ra.RuntimeLifecycleState.CREATED,
                timestamp_utc=_utc_now(),
                monotonic_offset_ms=0,
            )
        failures.append(
            getattr(invalid_event, "error_code", invalid_event.__class__.__name__)
        )

        with _expect_error(RuntimeFailureNormalizationError) as unsupported_error:
            normalize_runtime_failure(
                error=RuntimeError("raw-message-that-must-not-project"),
                runtime_handle=handle,
                process_status=ra.RuntimeProcessStatus.UNKNOWN,
                workspace_status=ra.RuntimeWorkspaceStatus.UNALLOCATED,
                cleanup_status=ra.RuntimeCleanupStatus.FAILED,
            )
        failures.append(unsupported_error.error_code)

        marker_result = self.run_case("ROLLBACK-002")
        _assert(marker_result.outcome is RuntimeAdapterConformanceOutcome.PASSED)
        failures.append("runtime_rollback_marker_error")
        _assert(all("raw-message" not in item for item in failures))
        return tuple(sorted(set(failures)))

    def _case_concurrency(self) -> tuple[str, ...]:
        first = self._allocate_context("concurrency.one")
        second = self._allocate_context("concurrency.two")
        try:
            self._sanitize(first)
            self._sanitize(second)
            self._launch(first, "--sleep-ms", "5000")
            self._launch(second, "--sleep-ms", "5000")
            _assert(
                first.allocation.workspace_ref.workspace_id
                != second.allocation.workspace_ref.workspace_id
            )
            first_result = RuntimeTerminationCoordinator(
                process_owner=first.owner,
                clock=_DeterministicClock(),
            ).cancel(
                request=self._cancel_request(first.handle),
                runtime_handle=first.handle,
                event_journal=self._journal(first.handle),
                timeout_policy=get_runtime_profile(
                    ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
                ).timeout_policy,
            )
            second_result = self._shutdown(second)
            _assert(first_result.outcome is ra.RuntimeOperationOutcome.CANCELLED)
            _assert(second_result.outcome is ra.RuntimeOperationOutcome.STOPPED)
            _assert(second.allocation.paths.workspace_root.exists())
            self._assert_conflicting_lifecycle_fails_closed()
        finally:
            self._cleanup_context(first)
            self._cleanup_context(second)
        return ("runtime_isolation",)

    def _case_cleanup(self) -> tuple[str, ...]:
        ctx = self._allocate_context("cleanup.zero")
        try:
            self._sanitize(ctx)
            self._launch(ctx, "--sleep-ms", "5000", "--graceful-exit-code", "0")
            stopped = self._shutdown(ctx)
            self._rollback(ctx, stopped.runtime_handle)
        finally:
            self._cleanup_context(ctx)
        _assert(not tuple(self._tmp_path.rglob(MARKER_NAME)))
        _assert(
            not any(
                thread.name.startswith("runtime-adapter-")
                for thread in threading.enumerate()
            )
        )
        backend = ProcessTreeBackend()
        _assert(not any(backend.pid_exists(pid) for pid in self._known_pids))
        return ("zero_residue",)

    def _complete_lifecycle(self, token: str) -> ra.RuntimeOperationResult:
        ctx = self._allocate_context(token)
        clock = _DeterministicClock()
        try:
            sanitized = self._sanitize(ctx)
            journal = self._journal(ctx.handle)
            self._append(
                journal,
                clock,
                ra.RuntimeEventType.REQUEST_RECEIVED,
                ra.RuntimeLifecycleState.CREATED,
            )
            self._append(
                journal,
                clock,
                ra.RuntimeEventType.PROFILE_RESOLVED,
                ra.RuntimeLifecycleState.VALIDATING,
            )
            self._append(
                journal,
                clock,
                ra.RuntimeEventType.WORKSPACE_CREATED,
                ra.RuntimeLifecycleState.VALIDATING,
                workspace_allocation=ctx.allocation,
            )
            _assert(sanitized.report.provider_variables_present_in_output is False)
            self._append(
                journal,
                clock,
                ra.RuntimeEventType.ENVIRONMENT_SANITIZED,
                ra.RuntimeLifecycleState.VALIDATING,
            )
            launched = self._launch(
                ctx,
                "--sleep-ms",
                "5000",
                "--graceful-exit-code",
                "0",
            )
            self._append(
                journal,
                clock,
                ra.RuntimeEventType.PROCESS_STARTED,
                ra.RuntimeLifecycleState.STARTING,
                process_snapshot=launched,
            )
            stopped = RuntimeTerminationCoordinator(
                process_owner=ctx.owner,
                clock=clock,
            ).shutdown(
                request=self._stop_request(ctx.handle),
                runtime_handle=ctx.handle,
                event_journal=journal,
                timeout_policy=get_runtime_profile(
                    ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
                ).timeout_policy,
            )
            return self._rollback(
                ctx, stopped.runtime_handle, journal=journal, clock=clock
            )
        finally:
            self._cleanup_context(ctx)

    def _assert_conflicting_lifecycle_fails_closed(self) -> None:
        entered = threading.Event()
        release = threading.Event()

        class BlockingOwner:
            def request_graceful_stop(self, runtime_id: str, *, timeout_ms: int):
                entered.set()
                release.wait(timeout=5)
                return _graceful_result(runtime_id)

            def release(self, runtime_id: str) -> None:
                return None

            def owned_runtime_ids(self) -> tuple[str, ...]:
                return ()

        coordinator = RuntimeTerminationCoordinator(
            process_owner=BlockingOwner(),
            clock=_DeterministicClock(),
        )
        handle = self._handle("rt.p147.conflict", "ws_" + "6" * 32)

        def locked_call() -> None:
            coordinator.shutdown(
                request=self._stop_request(handle),
                runtime_handle=handle,
                event_journal=self._journal(handle),
                timeout_policy=get_runtime_profile(
                    ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
                ).timeout_policy,
            )

        thread = threading.Thread(target=locked_call, name="p147-conflict-check")
        thread.start()
        try:
            _assert(entered.wait(timeout=5))
            with _expect_error(RuntimeLifecycleOperationConflictError):
                coordinator.shutdown(
                    request=self._stop_request(handle),
                    runtime_handle=handle,
                    event_journal=self._journal(handle),
                    timeout_policy=get_runtime_profile(
                        ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
                    ).timeout_policy,
                )
        finally:
            release.set()
            thread.join(timeout=5)

    def _allocate_context(
        self,
        token: str,
        *,
        profile_id: str = ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
    ) -> _RuntimeContext:
        profile = get_runtime_profile(profile_id)
        runtime_id = self._runtime_id(token)
        base = self._base_for(runtime_id)
        base.mkdir()
        workspace_token = f"{self._sequence:032x}"
        allocator = RuntimeWorkspaceAllocator(
            trusted_base_root=base,
            workspace_id_factory=lambda: "ws_" + workspace_token,
        )
        allocation = allocator.allocate(runtime_id=runtime_id, profile=profile)
        handle = self._handle(
            runtime_id,
            allocation.workspace_ref.workspace_id,
            profile_id=profile.profile_ref.profile_id,
        )
        return _RuntimeContext(
            runtime_id=runtime_id,
            profile=profile,
            allocator=allocator,
            owner=HermesProcessOwner(),
            allocation=allocation,
            handle=handle,
            source_environment=MappingProxyType(self._synthetic_source_environment()),
        )

    def _sanitize(self, ctx: _RuntimeContext):
        sanitized = sanitize_runtime_environment(
            profile=ctx.profile,
            platform_family=self._platform_family(),
            source_environment=ctx.source_environment,
            paths=ctx.allocation.environment_paths,
        )
        object.__setattr__(ctx, "sanitized_environment", sanitized)
        return sanitized

    def _launch_plan(
        self,
        ctx: _RuntimeContext,
        *arguments: str,
        stdout_limit_bytes: int = 4096,
        stderr_limit_bytes: int = 4096,
    ) -> ResolvedProcessLaunchPlan:
        if ctx.profile.execution_scope is not RuntimeExecutionScope.INERT_TEST_ONLY:
            raise ConformanceExecutionDenied(ctx.profile.profile_ref.profile_id)
        sanitized = ctx.sanitized_environment or self._sanitize(ctx)
        return ResolvedProcessLaunchPlan(
            profile_id=ctx.profile.profile_ref.profile_id,
            workspace_id=ctx.allocation.workspace_ref.workspace_id,
            executable=self._python_executable,
            arguments=(str(self._probe), *arguments),
            working_directory=str(ctx.allocation.paths.workdir),
            environment_items=sanitized.items,
            stdout_limit_bytes=stdout_limit_bytes,
            stderr_limit_bytes=stderr_limit_bytes,
        )

    def _launch(
        self,
        ctx: _RuntimeContext,
        *arguments: str,
        stdout_limit_bytes: int = 4096,
        stderr_limit_bytes: int = 4096,
    ) -> OwnedProcessSnapshot:
        snapshot = ctx.owner.launch(
            ctx.handle,
            self._launch_plan(
                ctx,
                *arguments,
                stdout_limit_bytes=stdout_limit_bytes,
                stderr_limit_bytes=stderr_limit_bytes,
            ),
        )
        if snapshot.process_reference.launcher_pid is not None:
            self._known_pids.add(snapshot.process_reference.launcher_pid)
        self._known_pids.update(snapshot.process_reference.descendant_pids)
        return snapshot

    def _launch_and_wait(
        self,
        ctx: _RuntimeContext,
        *arguments: str,
        stdout_limit_bytes: int = 4096,
        stderr_limit_bytes: int = 4096,
    ) -> OwnedProcessSnapshot:
        self._launch(
            ctx,
            *arguments,
            stdout_limit_bytes=stdout_limit_bytes,
            stderr_limit_bytes=stderr_limit_bytes,
        )
        snapshot = self._wait_for_snapshot(
            ctx.owner,
            ctx.runtime_id,
            lambda snap: (
                snap.process_reference.process_status
                is not ra.RuntimeProcessStatus.RUNNING
            ),
            timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
            stage="process_exit_observed",
        )
        ctx.owner.release(ctx.runtime_id)
        return snapshot

    def _shutdown(
        self,
        ctx: _RuntimeContext,
        *,
        graceful_ms: int | None = None,
        journal: RuntimeEventJournal | None = None,
        clock: RuntimeLifecycleClock | None = None,
        process_owner: HermesProcessOwner | _GracefulTimeoutProcessOwner | None = None,
    ) -> ra.RuntimeOperationResult:
        profile_timeout = get_runtime_profile(
            ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
        ).timeout_policy
        timeout = profile_timeout
        if graceful_ms is not None:
            timeout = ra.RuntimeTimeoutPolicy(
                readiness_timeout_ms=1000,
                graceful_shutdown_timeout_ms=graceful_ms,
                forced_termination_timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
                poll_interval_ms=50,
                max_stdout_bytes=profile_timeout.max_stdout_bytes,
                max_stderr_bytes=profile_timeout.max_stderr_bytes,
            )
        return RuntimeTerminationCoordinator(
            process_owner=process_owner or ctx.owner,
            clock=clock or _DeterministicClock(),
        ).shutdown(
            request=self._stop_request(ctx.handle),
            runtime_handle=ctx.handle,
            event_journal=journal or self._journal(ctx.handle),
            timeout_policy=timeout,
        )

    def _rollback(
        self,
        ctx: _RuntimeContext,
        runtime_handle: ra.RuntimeHandle,
        *,
        journal: RuntimeEventJournal | None = None,
        clock: RuntimeLifecycleClock | None = None,
    ) -> ra.RuntimeOperationResult:
        return RuntimeWorkspaceRollbackCoordinator(
            workspace_allocator=ctx.allocator,
            process_owner=ctx.owner,
            clock=clock or _DeterministicClock(),
        ).rollback(
            request=self._rollback_request(runtime_handle),
            runtime_handle=runtime_handle,
            profile=ctx.profile,
            allocation=ctx.allocation,
            event_journal=journal or self._journal(runtime_handle),
        )

    def _cleanup_context(self, ctx: _RuntimeContext) -> None:
        self._cleanup_owner(ctx.owner, ctx.runtime_id)
        if ctx.allocation.paths.workspace_root.exists():
            self._restore_marker(ctx.allocation)
            handle = self._handle(
                ctx.runtime_id,
                ctx.allocation.workspace_ref.workspace_id,
                profile_id=ctx.profile.profile_ref.profile_id,
                state=ra.RuntimeLifecycleState.STOPPED,
            )
            result = self._rollback(ctx, handle)
            _assert(
                result.outcome is ra.RuntimeOperationOutcome.ROLLED_BACK,
                category="cleanup_rollback_failed",
                expected="rolled_back",
                observed=getattr(result.outcome, "value", result.outcome),
                stage="cleanup_workspace_rollback",
            )

    def _cleanup_owner(self, owner: HermesProcessOwner, runtime_id: str) -> None:
        if runtime_id not in owner.owned_runtime_ids():
            return
        try:
            snapshot = owner.snapshot(runtime_id)
            if (
                snapshot.process_reference.process_status
                is ra.RuntimeProcessStatus.RUNNING
            ):
                owner.terminate_owned_tree(
                    runtime_id,
                    timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
                )
            self._wait_for_snapshot(
                owner,
                runtime_id,
                lambda snap: (
                    snap.process_reference.process_status
                    is not ra.RuntimeProcessStatus.RUNNING
                ),
                timeout_ms=_PROCESS_WAIT_TIMEOUT_MS,
                stage="cleanup_process_exit_observed",
            )
            owner.release(runtime_id)
        except (
            RuntimeProcessOwnerError,
            UnknownRuntimeOwnershipError,
            OwnedProcessStillRunningError,
            OwnedProcessDrainIncompleteError,
        ):
            return

    def _wait_for_snapshot(
        self,
        owner: HermesProcessOwner,
        runtime_id: str,
        predicate,
        *,
        timeout_ms: int,
        stage: str,
    ) -> OwnedProcessSnapshot:
        deadline = time.monotonic() + (timeout_ms / 1000)
        last_snapshot = owner.snapshot(runtime_id)
        while time.monotonic() < deadline:
            last_snapshot = owner.snapshot(runtime_id)
            if last_snapshot.process_reference.launcher_pid is not None:
                self._known_pids.add(last_snapshot.process_reference.launcher_pid)
            self._known_pids.update(last_snapshot.process_reference.descendant_pids)
            if predicate(last_snapshot):
                return last_snapshot
            time.sleep(0.05)
        raise _ConformanceAssertionError(
            category="process_wait_timeout",
            expected="owned_process_state_predicate_true",
            observed=_snapshot_observed_state(last_snapshot),
            stage=stage,
        )

    def _restore_marker(self, allocation: RuntimeWorkspaceAllocation) -> None:
        if not allocation.paths.workspace_root.exists():
            return
        payload = {
            "schema_version": 1,
            "runtime_id": allocation.runtime_id,
            "workspace_id": allocation.workspace_ref.workspace_id,
            "workspace_policy_id": allocation.workspace_policy_id,
        }
        allocation.paths.ownership_marker.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    def _append(
        self,
        journal: RuntimeEventJournal,
        clock: RuntimeLifecycleClock,
        event_type: ra.RuntimeEventType,
        lifecycle_state: ra.RuntimeLifecycleState,
        *,
        process_snapshot: OwnedProcessSnapshot | None = None,
        workspace_allocation: RuntimeWorkspaceAllocation | None = None,
    ) -> None:
        journal.append(
            event_type=event_type,
            lifecycle_state=lifecycle_state,
            timestamp_utc=clock.utc_now(),
            monotonic_offset_ms=clock.monotonic_offset_ms(),
            process_snapshot=process_snapshot,
            workspace_allocation=workspace_allocation,
        )

    def _journal(self, handle: ra.RuntimeHandle) -> RuntimeEventJournal:
        counter = iter(
            f"evt_p147_{self._token(handle.runtime_id)}_{index:03d}"
            for index in range(256)
        )
        return RuntimeEventJournal(
            runtime_handle=handle, event_id_factory=lambda: next(counter)
        )

    def _handle(
        self,
        runtime_id: str,
        workspace_id: str,
        *,
        profile_id: str = ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
        state: ra.RuntimeLifecycleState = ra.RuntimeLifecycleState.STARTING,
    ) -> ra.RuntimeHandle:
        return ra.RuntimeHandle(
            schema_version=1,
            runtime_id=runtime_id,
            correlation_id=f"corr.p147.{self._token(runtime_id)}",
            profile_id=profile_id,
            workspace_id=workspace_id,
            lifecycle_state=state,
            created_at_utc=_utc_now(),
        )

    def _launch_request(self) -> ra.RuntimeLaunchRequest:
        return ra.RuntimeLaunchRequest(
            schema_version=1,
            runtime_profile_id=ra.TEST_LIFECYCLE_PROBE_PROFILE_ID,
            workspace_binding=get_runtime_profile(
                ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
            ).default_workspace_binding,
            correlation_id="corr.p147.launch",
            requested_by="tester.p147",
            timeout_policy=get_runtime_profile(
                ra.TEST_LIFECYCLE_PROBE_PROFILE_ID
            ).timeout_policy,
            evidence_context=(),
        )

    def _stop_request(self, handle: ra.RuntimeHandle) -> ra.RuntimeStopRequest:
        return ra.RuntimeStopRequest(
            schema_version=1,
            runtime_id=handle.runtime_id,
            correlation_id=handle.correlation_id,
            requested_by="tester.p147",
            reason_code="test.stop",
        )

    def _cancel_request(self, handle: ra.RuntimeHandle) -> ra.RuntimeCancelRequest:
        return ra.RuntimeCancelRequest(
            schema_version=1,
            runtime_id=handle.runtime_id,
            correlation_id=handle.correlation_id,
            requested_by="tester.p147",
            reason_code="test.cancel",
        )

    def _rollback_request(self, handle: ra.RuntimeHandle) -> ra.RuntimeRollbackRequest:
        return ra.RuntimeRollbackRequest(
            schema_version=1,
            runtime_id=handle.runtime_id,
            correlation_id=handle.correlation_id,
            requested_by="tester.p147",
            reason_code="test.rollback",
        )

    def _synthetic_source_environment(self) -> dict[str, str]:
        source = {name: "sentinel" for name in PROHIBITED_ENVIRONMENT_NAMES}
        source["PATH"] = "sentinel-path"
        if self._platform_family() is RuntimePlatformFamily.WINDOWS:
            system_root = (
                os.environ.get("SystemRoot")
                or os.environ.get("WINDIR")
                or r"C:\Windows"
            )
            source["SystemRoot"] = system_root
            source["WINDIR"] = system_root
        return source

    def _platform_family(self) -> RuntimePlatformFamily:
        if sys.platform == "win32":
            return RuntimePlatformFamily.WINDOWS
        return RuntimePlatformFamily.POSIX

    def _runtime_id(self, token: str) -> str:
        self._sequence += 1
        return f"rt.p147.{self._token(token)}.{self._sequence}"

    def _base_for(self, runtime_id: str) -> Path:
        return self._tmp_path / f"base-{self._token(runtime_id)}"

    def _token(self, value: str) -> str:
        return "".join(
            character if character.isalnum() else "." for character in value
        )[:48]


def _graceful_result(runtime_id: str):
    from hermes_cli.agent_platform.runtime_adapter.process_owner import (
        OwnedProcessGracefulStopResult,
    )

    snap = OwnedProcessSnapshot(
        runtime_id=runtime_id,
        process_reference=ra.RuntimeProcessRef(
            launcher_pid=12345,
            listener_pid=None,
            descendant_pids=(),
            process_status=ra.RuntimeProcessStatus.EXITED,
            started_at_utc=_utc_now(),
            exited_at_utc=_utc_now(),
            exit_code=0,
        ),
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
        tree_captured_at_utc=_utc_now(),
    )
    return OwnedProcessGracefulStopResult(
        runtime_id=runtime_id,
        mechanism="already_exited",
        supported=True,
        exit_observed=True,
        timed_out=False,
        snapshot=snap,
    )


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _assert(
    condition: bool,
    *,
    category: str = "condition_failed",
    expected: str = "condition_true",
    observed: object = "condition_false",
    stage: str = "assertion",
) -> None:
    if not condition:
        raise _ConformanceAssertionError(
            category=category,
            expected=expected,
            observed=observed,
            stage=stage,
        )


def _failure_evidence(exc: BaseException) -> tuple[str, ...]:
    if isinstance(exc, _ConformanceAssertionError):
        return exc.evidence
    error_code = getattr(exc, "error_code", "conformance.case_failed")
    return (
        f"code={_safe_evidence_text(error_code)}",
        f"exception={exc.__class__.__name__}",
    )


def _snapshot_observed_state(snapshot: OwnedProcessSnapshot) -> str:
    process = snapshot.process_reference
    return ";".join((
        f"status={process.process_status.value}",
        f"exit_code={process.exit_code}",
        f"descendant_count={len(process.descendant_pids)}",
        f"stdout_bytes={snapshot.stdout_snapshot.total_bytes_read}",
        f"stderr_bytes={snapshot.stderr_snapshot.total_bytes_read}",
        f"stdout_drained={snapshot.stdout_snapshot.drain_complete}",
        f"stderr_drained={snapshot.stderr_snapshot.drain_complete}",
    ))


def _safe_evidence_text(value: object) -> str:
    text = str(value)
    safe = []
    for character in text:
        if character.isalnum() or character in "._=;:-":
            safe.append(character)
        elif character.isspace():
            safe.append("_")
    bounded = "".join(safe)[:_MAX_FAILURE_EVIDENCE_CHARACTERS]
    return bounded or "none"


def _assert_round_trip(model) -> None:
    payload = model.model_dump_json()
    round_trip = model.__class__.model_validate_json(payload)
    _assert(round_trip == model)
    _assert(payload == model.model_dump_json())


def _assert_frozen(model) -> None:
    with _expect_error((ValidationError, TypeError, AttributeError)):
        setattr(model, "schema_version", 2)


def _event_types(result: ra.RuntimeOperationResult) -> tuple[ra.RuntimeEventType, ...]:
    return tuple(event.event_type for event in result.events)


def _nondecreasing(values) -> bool:
    sequence = tuple(values)
    return all(left <= right for left, right in zip(sequence, sequence[1:]))


class _expect_error:
    def __init__(self, expected: object = Exception) -> None:
        self._expected = expected
        self._exception: BaseException | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if exc is None:
            raise AssertionError("expected conformance error")
        expected = self._expected
        if isinstance(expected, tuple):
            if not isinstance(exc, expected):
                return False
        elif not isinstance(exc, expected):
            return False
        self._exception = exc
        return True

    def __getattr__(self, name: str):
        if self._exception is None:
            raise AttributeError(name)
        return getattr(self._exception, name)


__all__ = [
    "ALLOWED_SKIP_REASONS",
    "EXPECTED_CASE_IDS",
    "RuntimeAdapterConformanceCase",
    "RuntimeAdapterConformanceHarness",
    "RuntimeAdapterConformanceOutcome",
    "RuntimeAdapterConformanceResult",
    "RuntimeAdapterConformanceSummary",
]
