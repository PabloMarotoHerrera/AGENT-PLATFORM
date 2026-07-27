"""Enumerations for governed provider accounting metadata."""

from __future__ import annotations

from enum import StrEnum


class ProviderUsageSource(StrEnum):
    """Synthetic-safe usage evidence sources accepted by P15.5."""

    CODEX_RESPONSES_PROVIDER_REPORTED = "codex_responses_provider_reported"
    CODEX_APP_SERVER_PROVIDER_REPORTED = "codex_app_server_provider_reported"
    PROVIDER_OMITTED = "provider_omitted"


class ProviderUsageCompleteness(StrEnum):
    """Completeness labels for normalized provider usage evidence."""

    COMPLETE = "complete"
    MISSING = "missing"


class ProviderCostStatus(StrEnum):
    """Cost accounting states for the selected subscription route."""

    INCLUDED = "included"
    UNAVAILABLE = "unavailable"


class ProviderCostSource(StrEnum):
    """Cost source labels that do not require live billing or pricing calls."""

    SUBSCRIPTION_INCLUDED = "subscription_included"
    NONE = "none"


class ProviderTimeoutStage(StrEnum):
    """Timeout stages inherited by the P15.5 accounting record."""

    CONNECTION = "connection"
    RESPONSE_HEADER = "response_header"
    COMPLETE_INFERENCE = "complete_inference"
    CANCELLATION = "cancellation"
    WORKER_SHUTDOWN = "worker_shutdown"


class ProviderAccountingOutcome(StrEnum):
    """Terminal outcome values recorded by the accounting boundary."""

    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"


class ProviderTimeoutDisposition(StrEnum):
    """Whether elapsed time stayed inside or exceeded the governed budget."""

    WITHIN_BUDGET = "within_budget"
    TIMED_OUT = "timed_out"


class ProviderAccountingLinkState(StrEnum):
    """Result-link validation states for usage_record_id evidence."""

    MATCHED = "matched"


__all__ = [
    "ProviderAccountingLinkState",
    "ProviderAccountingOutcome",
    "ProviderCostSource",
    "ProviderCostStatus",
    "ProviderTimeoutDisposition",
    "ProviderTimeoutStage",
    "ProviderUsageCompleteness",
    "ProviderUsageSource",
]
