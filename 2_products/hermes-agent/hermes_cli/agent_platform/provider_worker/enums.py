"""Enumerations for governed provider-worker profile metadata."""

from __future__ import annotations

from enum import StrEnum


class ProviderWorkerProfileState(StrEnum):
    """Lifecycle state values for bounded worker profiles."""

    PROFILE_READY_RUNTIME_UNVERIFIED = "profile_ready_runtime_unverified"
    READY_FOR_INFERENCE_GATE = "ready_for_inference_gate"
    BLOCKED = "blocked"


class ProviderWorkerInputKind(StrEnum):
    """Input kinds accepted by the bounded worker protocol."""

    TEXT = "text"


class ProviderWorkerOutputKind(StrEnum):
    """Output kinds emitted by the bounded worker protocol."""

    TEXT = "text"


class ProviderWorkerFeaturePolicy(StrEnum):
    """Feature posture values for the bounded worker profile."""

    DISABLED = "disabled"


class ProviderWorkerRequestState(StrEnum):
    """Validation states for future worker requests."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ProviderWorkerResultState(StrEnum):
    """Terminal result envelope states."""

    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProviderWorkerFailureStage(StrEnum):
    """Bounded failure stages for worker protocol envelopes."""

    PROFILE_VALIDATION = "profile_validation"
    PROVIDER_BINDING = "provider_binding"
    REQUEST_VALIDATION = "request_validation"
    EXECUTION = "execution"
    CANCELLATION = "cancellation"
    SHUTDOWN = "shutdown"


class ProviderWorkerOversizedRequestPolicy(StrEnum):
    """Oversized request posture for the bounded worker profile."""

    FAIL_BEFORE_PROVIDER_CALL = "fail_before_provider_call"


__all__ = [
    "ProviderWorkerFailureStage",
    "ProviderWorkerFeaturePolicy",
    "ProviderWorkerInputKind",
    "ProviderWorkerOutputKind",
    "ProviderWorkerOversizedRequestPolicy",
    "ProviderWorkerProfileState",
    "ProviderWorkerRequestState",
    "ProviderWorkerResultState",
]
