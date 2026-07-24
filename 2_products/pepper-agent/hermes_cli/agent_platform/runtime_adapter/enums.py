"""Stable vocabularies for the AGENT PLATFORM runtime adapter contracts."""

from __future__ import annotations

from enum import StrEnum


class RuntimeLifecycleState(StrEnum):
    """Deterministic lifecycle states for a runtime handle."""

    CREATED = "created"
    VALIDATING = "validating"
    STARTING = "starting"
    WAITING_FOR_READINESS = "waiting_for_readiness"
    READY = "ready"
    CANCELLATION_REQUESTED = "cancellation_requested"
    STOPPING = "stopping"
    STOPPED = "stopped"
    CANCELLED = "cancelled"
    FAILED = "failed"
    ROLLBACK_PENDING = "rollback_pending"
    ROLLED_BACK = "rolled_back"
    ROLLBACK_FAILED = "rollback_failed"


class RuntimeLifecycleAction(StrEnum):
    """Allowed lifecycle transition requests."""

    VALIDATE = "validate"
    START = "start"
    WAIT_FOR_READINESS = "wait_for_readiness"
    MARK_READY = "mark_ready"
    REQUEST_CANCELLATION = "request_cancellation"
    BEGIN_STOP = "begin_stop"
    MARK_STOPPED = "mark_stopped"
    MARK_CANCELLED = "mark_cancelled"
    MARK_FAILED = "mark_failed"
    BEGIN_ROLLBACK = "begin_rollback"
    MARK_ROLLED_BACK = "mark_rolled_back"
    MARK_ROLLBACK_FAILED = "mark_rollback_failed"


class RuntimeProfileClass(StrEnum):
    """P14-authorized runtime profile classes."""

    TEST_LIFECYCLE_PROBE = "test_lifecycle_probe"
    PEPPER_DASHBOARD_PROVIDER_NULL = "pepper_dashboard_provider_null"


class RuntimeEventType(StrEnum):
    """Normalized runtime lifecycle event types."""

    REQUEST_RECEIVED = "request_received"
    REQUEST_REJECTED = "request_rejected"
    WORKSPACE_CREATED = "workspace_created"
    PROFILE_RESOLVED = "profile_resolved"
    ENVIRONMENT_SANITIZED = "environment_sanitized"
    PROCESS_STARTED = "process_started"
    LISTENER_DISCOVERED = "listener_discovered"
    READINESS_PROBE_STARTED = "readiness_probe_started"
    RUNTIME_READY = "runtime_ready"
    READINESS_TIMEOUT = "readiness_timeout"
    CANCELLATION_REQUESTED = "cancellation_requested"
    GRACEFUL_SHUTDOWN_STARTED = "graceful_shutdown_started"
    FORCED_TERMINATION_STARTED = "forced_termination_started"
    PROCESS_EXITED = "process_exited"
    LISTENER_RELEASED = "listener_released"
    WORKSPACE_CLEANUP_STARTED = "workspace_cleanup_started"
    WORKSPACE_CLEANUP_COMPLETED = "workspace_cleanup_completed"
    ROLLBACK_STARTED = "rollback_started"
    ROLLBACK_COMPLETED = "rollback_completed"
    RUNTIME_FAILED = "runtime_failed"


class RuntimeFailureStage(StrEnum):
    """Failure stages preserved in runtime failures and events."""

    REQUEST_VALIDATION = "request_validation"
    PROFILE_RESOLUTION = "profile_resolution"
    ENVIRONMENT_CONSTRUCTION = "environment_construction"
    WORKSPACE_CREATION = "workspace_creation"
    PATH_CONTAINMENT = "path_containment"
    PROCESS_LAUNCH = "process_launch"
    OWNERSHIP_CAPTURE = "ownership_capture"
    LISTENER_DISCOVERY = "listener_discovery"
    READINESS = "readiness"
    RUNTIME_OPERATION = "runtime_operation"
    CANCELLATION = "cancellation"
    GRACEFUL_SHUTDOWN = "graceful_shutdown"
    FORCED_TERMINATION = "forced_termination"
    WORKSPACE_CLEANUP = "workspace_cleanup"
    ROLLBACK = "rollback"
    EVENT_NORMALIZATION = "event_normalization"


class RuntimeSeverity(StrEnum):
    """Runtime event severity levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class RuntimeRetryability(StrEnum):
    """Retry classifications for runtime failures."""

    NEVER = "never"
    SAFE_AFTER_CLEANUP = "safe_after_cleanup"
    POLICY_DECISION_REQUIRED = "policy_decision_required"


class RuntimeProcessStatus(StrEnum):
    """Bounded process status vocabulary."""

    NOT_STARTED = "not_started"
    STARTING = "starting"
    RUNNING = "running"
    EXITED = "exited"
    TERMINATED = "terminated"
    UNKNOWN = "unknown"


class RuntimeReadinessState(StrEnum):
    """Readiness probe state vocabulary."""

    NOT_STARTED = "not_started"
    WAITING = "waiting"
    READY = "ready"
    TIMED_OUT = "timed_out"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RuntimeWorkspaceStatus(StrEnum):
    """Workspace allocation and cleanup state vocabulary."""

    UNALLOCATED = "unallocated"
    ALLOCATED = "allocated"
    RETAINED = "retained"
    CLEANED = "cleaned"
    CLEANUP_FAILED = "cleanup_failed"


class RuntimeCleanupStatus(StrEnum):
    """Cleanup status for failures and rollback evidence."""

    NOT_STARTED = "not_started"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    RETAINED = "retained"


class RuntimeRetentionPolicy(StrEnum):
    """Logical retention policy requested for an adapter workspace."""

    REMOVE_ON_SUCCESS = "remove_on_success"
    REMOVE_ON_TERMINAL = "remove_on_terminal"
    RETAIN_EVIDENCE = "retain_evidence"


class RuntimeOperationOutcome(StrEnum):
    """Top-level runtime operation outcomes."""

    ACCEPTED = "accepted"
    READY = "ready"
    STOPPED = "stopped"
    CANCELLED = "cancelled"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    ROLLBACK_FAILED = "rollback_failed"


class RuntimeLogStream(StrEnum):
    """Bounded log streams that can be referenced by evidence."""

    STDOUT = "stdout"
    STDERR = "stderr"
