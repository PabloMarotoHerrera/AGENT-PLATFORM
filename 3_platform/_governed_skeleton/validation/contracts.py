"""Metadata-only validation contracts for the governed skeleton.

These records describe validation posture. They do not execute checks, read
files, traverse directories, call providers, or persist results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ValidationStatus(Enum):
    """Non-executing validation posture values."""

    NOT_EXECUTED = "not_executed"
    DRY_RUN_ONLY = "dry_run_only"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    METADATA_ONLY = "metadata_only"
    INVALID_SCOPE = "invalid_scope"
    NEEDS_REVIEW = "needs_review"


class ValidationFindingSeverity(Enum):
    """Metadata-only finding severity."""

    INFO = "info"
    WARNING = "warning"
    BLOCKER = "blocker"


class ValidationCheckKind(Enum):
    """Allowed metadata-only validation check categories."""

    DOCUMENTATION_CONFORMANCE = "documentation_conformance"
    METADATA_SCHEMA = "metadata_schema"
    VOCABULARY_CONFORMANCE = "vocabulary_conformance"
    EVIDENCE_REF_SHAPE = "evidence_ref_shape"
    BLOCKER_PROPAGATION = "blocker_propagation"
    SOURCE_CLASSIFICATION_COMPLETENESS = "source_classification_completeness"
    NO_SECRET_NO_CREDENTIAL_METADATA_INVARIANT = (
        "no_secret_no_credential_metadata_invariant"
    )
    GRAPHIFY_EVIDENCE_ONLY_INVARIANT = "graphify_evidence_only_invariant"
    CSS_SUBSTRATE_DEFERRED_INVARIANT = "css_substrate_deferred_invariant"
    GENERATED_OUTPUT_TRACKING_BLOCKED_INVARIANT = (
        "generated_output_tracking_blocked_invariant"
    )
    PRODUCT_SOURCE_BLOCKED_INVARIANT = "product_source_blocked_invariant"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ValidationBlocker:
    """A metadata blocker that prevents validation execution."""

    blocker_id: str
    reason: str
    status: ValidationStatus = ValidationStatus.BLOCKED
    required_gate: str = "future_exact_human_approved_gate_required"
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ValidationInputRef:
    """A metadata reference to an input surface, not permission to read it."""

    ref_id: str
    classification: str = "unknown"
    sensitivity: str = "unknown"
    description: str = ""
    status: ValidationStatus = ValidationStatus.NEEDS_REVIEW
    blocked: bool = True
    blocker_reason: str = "Input is not approved for validation execution by default."
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ValidationOutputRef:
    """A metadata reference to a possible output, not persistence approval."""

    ref_id: str
    classification: str = "metadata_only"
    description: str = ""
    persistence_status: ValidationStatus = ValidationStatus.BLOCKED
    retention_ref: str = "retention_not_approved_for_output_creation"
    rollback_ref: str = "rollback_not_approved_for_output_creation"
    incident_ref: str = "incident_route_required_before_output_creation"


@dataclass(frozen=True)
class ValidationFinding:
    """A metadata-only finding produced by an inert runner."""

    finding_id: str
    message: str
    severity: ValidationFindingSeverity = ValidationFindingSeverity.INFO
    status: ValidationStatus = ValidationStatus.METADATA_ONLY
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ValidationCheck:
    """A metadata-only validation check description.

    The check stores no executable callable and no command payload.
    """

    check_id: str
    title: str
    kind: ValidationCheckKind = ValidationCheckKind.UNKNOWN
    description: str = ""
    status: ValidationStatus = ValidationStatus.NOT_EXECUTED
    input_refs: tuple[ValidationInputRef, ...] = field(default_factory=tuple)
    output_refs: tuple[ValidationOutputRef, ...] = field(default_factory=tuple)
    findings: tuple[ValidationFinding, ...] = field(default_factory=tuple)
    blockers: tuple[ValidationBlocker, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    validation_refs: tuple[str, ...] = field(default_factory=tuple)
    security_refs: tuple[str, ...] = field(default_factory=tuple)
    required_gates: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ValidationPlan:
    """A metadata-only validation plan.

    The plan is dry-run-only by default and does not grant execution approval.
    """

    plan_id: str
    title: str
    description: str = ""
    status: ValidationStatus = ValidationStatus.DRY_RUN_ONLY
    checks: tuple[ValidationCheck, ...] = field(default_factory=tuple)
    input_refs: tuple[ValidationInputRef, ...] = field(default_factory=tuple)
    output_refs: tuple[ValidationOutputRef, ...] = field(default_factory=tuple)
    blockers: tuple[ValidationBlocker, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    validation_refs: tuple[str, ...] = field(default_factory=tuple)
    security_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)
    retention_refs: tuple[str, ...] = field(default_factory=tuple)
    rollback_refs: tuple[str, ...] = field(default_factory=tuple)
    incident_refs: tuple[str, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)
    required_gates: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ValidationResult:
    """Metadata-only result returned by an inert validation runner."""

    result_id: str
    plan_id: str
    status: ValidationStatus = ValidationStatus.NOT_EXECUTED
    summary: str = "Validation was not executed."
    checks: tuple[ValidationCheck, ...] = field(default_factory=tuple)
    findings: tuple[ValidationFinding, ...] = field(default_factory=tuple)
    blockers: tuple[ValidationBlocker, ...] = field(default_factory=tuple)
    input_refs: tuple[ValidationInputRef, ...] = field(default_factory=tuple)
    output_refs: tuple[ValidationOutputRef, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    validation_refs: tuple[str, ...] = field(default_factory=tuple)
    security_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)
    retention_refs: tuple[str, ...] = field(default_factory=tuple)
    rollback_refs: tuple[str, ...] = field(default_factory=tuple)
    incident_refs: tuple[str, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)


__all__ = (
    "ValidationBlocker",
    "ValidationCheck",
    "ValidationCheckKind",
    "ValidationFinding",
    "ValidationFindingSeverity",
    "ValidationInputRef",
    "ValidationOutputRef",
    "ValidationPlan",
    "ValidationResult",
    "ValidationStatus",
)
