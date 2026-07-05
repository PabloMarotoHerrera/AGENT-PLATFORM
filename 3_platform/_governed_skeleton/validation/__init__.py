"""Inert validation runner skeleton exports.

Importing this package performs no runtime initialization, reads no environment,
executes no commands, and activates no providers, tools, agents, or connectors.
"""

from .contracts import (
    ValidationBlocker,
    ValidationCheck,
    ValidationCheckKind,
    ValidationFinding,
    ValidationFindingSeverity,
    ValidationInputRef,
    ValidationOutputRef,
    ValidationPlan,
    ValidationResult,
    ValidationStatus,
)
from .runner import (
    BlockedValidationRunner,
    DryRunValidationRunner,
    NoOpValidationRunner,
    ValidationRunner,
    blocked_result_from_plan,
)


__all__ = (
    "BlockedValidationRunner",
    "DryRunValidationRunner",
    "NoOpValidationRunner",
    "ValidationBlocker",
    "ValidationCheck",
    "ValidationCheckKind",
    "ValidationFinding",
    "ValidationFindingSeverity",
    "ValidationInputRef",
    "ValidationOutputRef",
    "ValidationPlan",
    "ValidationResult",
    "ValidationRunner",
    "ValidationStatus",
    "blocked_result_from_plan",
)
