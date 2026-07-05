"""Inert agent handoff planning metadata.

The handoff planner is metadata-only. It does not execute handoffs, dispatch
agents, trigger tools or providers, mutate runtime state, create background jobs,
activate scheduler/orchestration, persist output, or create always-on behavior.
"""

from __future__ import annotations

from .contracts import (
    AgentBlockedReason,
    AgentBlocker,
    AgentExecutionDecision,
    AgentExecutionDecisionStatus,
    AgentHandoffEnvelope,
    AgentRuntimeRef,
    AgentRuntimeState,
    AgentTaskEnvelope,
)


def blocked_handoff_decision(
    handoff: AgentHandoffEnvelope,
    *,
    decision_id: str | None = None,
) -> AgentExecutionDecision:
    """Create metadata-only handoff decision; this does not execute handoff."""

    reasons = (
        AgentBlockedReason.HANDOFF_EXECUTION_BLOCKED,
        AgentBlockedReason.RUNTIME_ACTIVATION_BLOCKED,
        AgentBlockedReason.HUMAN_APPROVAL_REQUIRED,
    )
    blocker = AgentBlocker(
        blocker_id="agent_handoff_execution_blocked",
        reason="Agent handoff execution remains blocked by governance posture.",
        blocked_reason=AgentBlockedReason.HANDOFF_EXECUTION_BLOCKED,
        refs=("P3.5", "P3.BR"),
    )
    return AgentExecutionDecision(
        decision_id=decision_id or f"{handoff.envelope_id}:blocked",
        task_id=handoff.source_task_id,
        handoff_id=handoff.envelope_id,
        status=AgentExecutionDecisionStatus.BLOCKED,
        runtime_state=AgentRuntimeState.BLOCKED,
        summary="Agent handoff planning returned metadata only; handoff execution remains blocked.",
        blocked_reasons=reasons,
        blockers=(*handoff.blockers, blocker),
        limitations=handoff.limitations,
        approval_refs=handoff.approval_refs,
        evidence_refs=handoff.evidence_refs,
        validation_refs=handoff.validation_refs,
        security_refs=handoff.security_refs,
        retention_refs=handoff.retention_refs,
        rollback_refs=handoff.rollback_refs,
        incident_refs=handoff.incident_refs,
        audit_refs=handoff.audit_refs,
        source_classification_refs=handoff.source_classification_refs,
    )


class AgentHandoffPlanner:
    """Metadata-only handoff planner that preserves refs and blockers."""

    def plan(
        self,
        task: AgentTaskEnvelope,
        *,
        handoff_id: str | None = None,
        target_runtime_ref: AgentRuntimeRef | None = None,
    ) -> AgentHandoffEnvelope:
        """Return a metadata-only handoff envelope without dispatching agents."""

        blocker = AgentBlocker(
            blocker_id="agent_handoff_planning_blocked_execution",
            reason="Handoff planning is metadata-only and cannot execute handoffs.",
            blocked_reason=AgentBlockedReason.HANDOFF_EXECUTION_BLOCKED,
            refs=("P3.5", "P3.BR"),
        )
        return AgentHandoffEnvelope(
            envelope_id=handoff_id or f"{task.envelope_id}:handoff",
            title=f"Metadata-only handoff for {task.title}",
            source_task_id=task.envelope_id,
            source_runtime_ref=task.runtime_ref,
            target_runtime_ref=target_runtime_ref,
            handoff_summary="Handoff is represented as metadata only; no handoff execution occurs.",
            status=AgentExecutionDecisionStatus.BLOCKED,
            approval_refs=task.approval_refs,
            blockers=(*task.blockers, blocker),
            limitations=task.limitations,
            evidence_refs=task.evidence_refs,
            validation_refs=task.validation_refs,
            security_refs=task.security_refs,
            retention_refs=task.retention_refs,
            rollback_refs=task.rollback_refs,
            incident_refs=task.incident_refs,
            audit_refs=task.audit_refs,
            source_classification_refs=task.source_classification_refs,
        )

    def decide(self, handoff: AgentHandoffEnvelope) -> AgentExecutionDecision:
        """Return blocked decision metadata; this does not execute handoff."""

        return blocked_handoff_decision(handoff)


__all__ = (
    "AgentHandoffPlanner",
    "blocked_handoff_decision",
)
