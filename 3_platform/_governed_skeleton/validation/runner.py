"""Inert validation runner skeletons.

Runners in this module return metadata-only results. They do not execute
checks, read files, traverse directories, run commands, persist output, or call
tools, agents, providers, MCP, Graphify, Codegraph, GBrain, Hermes, or Cadence.
"""

from __future__ import annotations

from typing import Protocol

from .contracts import (
    ValidationBlocker,
    ValidationFinding,
    ValidationFindingSeverity,
    ValidationPlan,
    ValidationResult,
    ValidationStatus,
)


class ValidationRunner(Protocol):
    """Interface for inert validation metadata runners."""

    def run(self, plan: ValidationPlan) -> ValidationResult:
        """Return metadata for the plan; this does not execute checks."""


def blocked_result_from_plan(
    plan: ValidationPlan,
    *,
    result_id: str | None = None,
    status: ValidationStatus = ValidationStatus.BLOCKED,
    summary: str = "Validation execution remains blocked.",
    reason: str = "Validation execution remains blocked by governance posture.",
) -> ValidationResult:
    """Create a metadata-only blocked result from a plan.

    This helper does not inspect, mutate, or execute plan checks.
    """

    blocker = ValidationBlocker(
        blocker_id="validation_execution_blocked",
        reason=reason,
        status=ValidationStatus.BLOCKED,
        required_gate="future_exact_human_approved_validation_gate_required",
        refs=("P3.1", "P3.3", "P3.BR"),
    )
    finding = ValidationFinding(
        finding_id="validation_execution_not_performed",
        message="Validation runner metadata was produced; checks do not execute.",
        severity=ValidationFindingSeverity.BLOCKER,
        status=ValidationStatus.METADATA_ONLY,
        refs=("P3.1", "P3.3", "P3.BR"),
    )
    return ValidationResult(
        result_id=result_id or f"{plan.plan_id}:blocked",
        plan_id=plan.plan_id,
        status=status,
        summary=summary,
        checks=plan.checks,
        findings=(finding,),
        blockers=(*plan.blockers, blocker),
        input_refs=plan.input_refs,
        output_refs=plan.output_refs,
        evidence_refs=plan.evidence_refs,
        validation_refs=plan.validation_refs,
        security_refs=plan.security_refs,
        source_classification_refs=plan.source_classification_refs,
        retention_refs=plan.retention_refs,
        rollback_refs=plan.rollback_refs,
        incident_refs=plan.incident_refs,
        audit_refs=plan.audit_refs,
    )


class NoOpValidationRunner:
    """No-op runner that reports not-executed metadata only."""

    def run(self, plan: ValidationPlan) -> ValidationResult:
        """Return a not-executed result; this does not execute checks."""

        return blocked_result_from_plan(
            plan,
            result_id=f"{plan.plan_id}:noop",
            status=ValidationStatus.NOT_EXECUTED,
            summary="NoOpValidationRunner returned metadata only; validation was not executed.",
            reason="NoOpValidationRunner is inert and cannot execute validation checks.",
        )


class DryRunValidationRunner:
    """Dry-run runner that plans metadata only and treats dry-run as non-execution."""

    def run(self, plan: ValidationPlan) -> ValidationResult:
        """Return a dry-run-only result; this does not execute checks."""

        return blocked_result_from_plan(
            plan,
            result_id=f"{plan.plan_id}:dry-run",
            status=ValidationStatus.DRY_RUN_ONLY,
            summary="DryRunValidationRunner returned metadata only; dry-run is not execution.",
            reason="Dry-run mode is metadata-only and cannot execute validation checks.",
        )


class BlockedValidationRunner:
    """Runner posture for explicitly blocked validation execution."""

    def run(self, plan: ValidationPlan) -> ValidationResult:
        """Return a blocked result; this does not execute checks."""

        return blocked_result_from_plan(
            plan,
            result_id=f"{plan.plan_id}:blocked",
            status=ValidationStatus.BLOCKED,
            summary="BlockedValidationRunner returned blocked metadata; validation execution remains blocked.",
            reason="Validation execution remains blocked until exact gates and human approval exist.",
        )


__all__ = (
    "BlockedValidationRunner",
    "DryRunValidationRunner",
    "NoOpValidationRunner",
    "ValidationRunner",
    "blocked_result_from_plan",
)
