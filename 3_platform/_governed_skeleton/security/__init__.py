"""Non-active security dry-run skeleton package.

This package exposes metadata-only security policy types and an inert
dry-run evaluator. Importing it does not evaluate policy, read files,
inspect environment variables, configure logging, or create persistence.
"""

from .dry_run import SecurityDryRunEvaluator
from .models import (
    DenyReason,
    SecurityControl,
    SecurityDecision,
    SecurityDecisionStatus,
    SecurityDryRunResult,
    SecurityFinding,
    SecuritySubject,
    SensitivityLevel,
    SourceClassification,
)
from .policy import SecurityPolicy, default_deny_policy

__all__ = (
    "SecurityDecisionStatus",
    "SensitivityLevel",
    "SourceClassification",
    "SecuritySubject",
    "SecurityControl",
    "SecurityDecision",
    "DenyReason",
    "SecurityFinding",
    "SecurityDryRunResult",
    "SecurityPolicy",
    "SecurityDryRunEvaluator",
    "default_deny_policy",
)
