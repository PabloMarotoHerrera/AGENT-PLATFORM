"""Inert agent runtime skeleton.

Runtime classes return metadata-only decisions. They do not execute agents,
tasks, handoffs, tools, providers, MCP, live connectors, product code, Graphify,
Codegraph, GBrain, Hermes, Cadence, commands, filesystem actions, network calls,
or persistence.
"""

from __future__ import annotations

from typing import Protocol

from .contracts import (
    AgentBlockedReason,
    AgentBlocker,
    AgentExecutionDecision,
    AgentExecutionDecisionStatus,
    AgentRuntimeState,
    AgentTaskEnvelope,
)


class AgentRuntime(Protocol):
    """Interface for metadata-only agent runtime decisions."""

    def decide(self, task: AgentTaskEnvelope) -> AgentExecutionDecision:
        """Return decision metadata; this does not execute an agent."""


def blocked_agent_decision_from_task(
    task: AgentTaskEnvelope,
    *,
    decision_id: str | None = None,
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED,
    runtime_state: AgentRuntimeState = AgentRuntimeState.BLOCKED,
    summary: str = "Agent runtime activation remains blocked.",
    blocked_reasons: tuple[AgentBlockedReason, ...] = (
        AgentBlockedReason.RUNTIME_ACTIVATION_BLOCKED,
        AgentBlockedReason.TASK_EXECUTION_BLOCKED,
        AgentBlockedReason.HUMAN_APPROVAL_REQUIRED,
    ),
) -> AgentExecutionDecision:
    """Create a metadata-only blocked decision without executing the task."""

    blockers = tuple(
        AgentBlocker(
            blocker_id=f"agent_blocked_reason:{reason.value}",
            reason=f"Agent task is blocked: {reason.value}.",
            blocked_reason=reason,
            refs=("P3.5", "P3.BR"),
        )
        for reason in blocked_reasons
    )
    return AgentExecutionDecision(
        decision_id=decision_id or f"{task.envelope_id}:blocked",
        task_id=task.envelope_id,
        status=status,
        runtime_state=runtime_state,
        summary=summary,
        blocked_reasons=blocked_reasons,
        blockers=(*task.blockers, *blockers),
        limitations=task.limitations,
        approval_refs=task.approval_refs,
        tool_refs=task.tool_refs,
        provider_refs=task.provider_refs,
        evidence_refs=task.evidence_refs,
        validation_refs=task.validation_refs,
        security_refs=task.security_refs,
        retention_refs=task.retention_refs,
        rollback_refs=task.rollback_refs,
        incident_refs=task.incident_refs,
        audit_refs=task.audit_refs,
        source_classification_refs=task.source_classification_refs,
    )


class NoOpAgentRuntime:
    """No-op runtime that never executes agent tasks."""

    def decide(self, task: AgentTaskEnvelope) -> AgentExecutionDecision:
        """Return no-op metadata; this does not execute an agent or task."""

        return blocked_agent_decision_from_task(
            task,
            decision_id=f"{task.envelope_id}:noop",
            status=AgentExecutionDecisionStatus.NO_OP,
            runtime_state=AgentRuntimeState.NO_OP,
            summary="NoOpAgentRuntime returned metadata only; no agent execution occurred.",
            blocked_reasons=(
                AgentBlockedReason.RUNTIME_ACTIVATION_BLOCKED,
                AgentBlockedReason.TASK_EXECUTION_BLOCKED,
                AgentBlockedReason.HUMAN_APPROVAL_REQUIRED,
            ),
        )


class BlockedAgentRuntime:
    """Runtime posture for explicitly blocked agent execution."""

    def decide(self, task: AgentTaskEnvelope) -> AgentExecutionDecision:
        """Return blocked metadata; this does not execute an agent or task."""

        return blocked_agent_decision_from_task(
            task,
            decision_id=f"{task.envelope_id}:blocked",
            status=AgentExecutionDecisionStatus.BLOCKED,
            runtime_state=AgentRuntimeState.BLOCKED,
            summary="BlockedAgentRuntime returned blocked metadata; agent execution remains blocked.",
            blocked_reasons=(
                AgentBlockedReason.RUNTIME_ACTIVATION_BLOCKED,
                AgentBlockedReason.TASK_EXECUTION_BLOCKED,
                AgentBlockedReason.HANDOFF_EXECUTION_BLOCKED,
                AgentBlockedReason.TOOL_EXECUTION_BLOCKED,
                AgentBlockedReason.PROVIDER_AUTH_BLOCKED,
                AgentBlockedReason.HUMAN_APPROVAL_REQUIRED,
            ),
        )


__all__ = (
    "AgentRuntime",
    "BlockedAgentRuntime",
    "NoOpAgentRuntime",
    "blocked_agent_decision_from_task",
)
