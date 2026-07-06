"""No-op helpers for the inert MVP-0 skeleton.

All helpers return metadata-only operation results. They never execute a
requested operation, never call tools/providers/MCP, never mutate files,
never mutate Git, and never persist state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .contracts import (
    BoundaryRef,
    EvidenceRef,
    Mvp0ActivationLevel,
    Mvp0BlockedReason,
    Mvp0OperationResult,
    Mvp0OperationStatus,
)


@dataclass(frozen=True)
class BlockedMvp0Operation:
    """Metadata describing an operation that must not execute."""

    operation_name: str = "blocked_mvp0_operation"
    status: Mvp0OperationStatus = Mvp0OperationStatus.NOT_EXECUTED
    blocked_reasons: Tuple[Mvp0BlockedReason, ...] = (Mvp0BlockedReason.UNKNOWN,)
    human_review_required: bool = True
    note: str = "metadata-only blocked operation"


def build_blocked_result(
    operation_name: str,
    blocked_reasons: Tuple[Mvp0BlockedReason, ...] = (Mvp0BlockedReason.UNKNOWN,),
    message: str = "operation blocked; metadata-only result; NOT_EXECUTED",
) -> Mvp0OperationResult:
    """Build a blocked metadata-only result without executing anything."""

    return Mvp0OperationResult(
        operation_name=operation_name,
        status=Mvp0OperationStatus.NOT_EXECUTED,
        activation_level=Mvp0ActivationLevel.P8_L2_LOCAL_NON_EXECUTING_SURFACE,
        blocked_reasons=blocked_reasons,
        human_review_required=True,
        message=message,
        evidence_refs=(EvidenceRef(),),
        boundary_refs=(BoundaryRef(),),
        limitations=("metadata-only", "not executed", "needs human review"),
    )


def build_metadata_only_result(
    operation_name: str,
    message: str = "metadata-only result; no operation executed",
) -> Mvp0OperationResult:
    """Build a metadata-only result for inert placeholder behavior."""

    return Mvp0OperationResult(
        operation_name=operation_name,
        status=Mvp0OperationStatus.METADATA_ONLY,
        activation_level=Mvp0ActivationLevel.P8_L2_LOCAL_NON_EXECUTING_SURFACE,
        blocked_reasons=(),
        human_review_required=True,
        message=message,
        evidence_refs=(EvidenceRef(),),
        boundary_refs=(BoundaryRef(),),
        limitations=("metadata-only", "no execution", "no persistence"),
    )


def build_needs_human_review_result(
    operation_name: str,
    message: str = "needs human review; no operation executed",
) -> Mvp0OperationResult:
    """Build a metadata-only result requiring human review."""

    return Mvp0OperationResult(
        operation_name=operation_name,
        status=Mvp0OperationStatus.NEEDS_HUMAN_REVIEW,
        activation_level=Mvp0ActivationLevel.P8_L2_LOCAL_NON_EXECUTING_SURFACE,
        blocked_reasons=(Mvp0BlockedReason.MISSING_HUMAN_APPROVAL,),
        human_review_required=True,
        message=message,
        evidence_refs=(EvidenceRef(),),
        boundary_refs=(BoundaryRef(),),
        limitations=("metadata-only", "human approval required", "not executed"),
    )
