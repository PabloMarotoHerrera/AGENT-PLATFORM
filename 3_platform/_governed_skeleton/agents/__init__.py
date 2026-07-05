"""Inert agent runtime and handoff skeleton exports.

Importing this package performs no runtime initialization, reads no environment,
executes no commands, activates no providers, tools, agents, MCP, live
connectors, scheduler, orchestration, or always-on behavior.
"""

from .contracts import (
    AgentApprovalRef,
    AgentBlockedReason,
    AgentBlocker,
    AgentContextEnvelope,
    AgentEnvelopeKind,
    AgentEvidenceRef,
    AgentExecutionDecision,
    AgentExecutionDecisionStatus,
    AgentHandoffEnvelope,
    AgentIncidentRef,
    AgentInstructionEnvelope,
    AgentLimitation,
    AgentOutputEnvelope,
    AgentProviderRef,
    AgentRetentionRef,
    AgentRollbackRef,
    AgentRuntimeRef,
    AgentRuntimeState,
    AgentSecurityRef,
    AgentTaskEnvelope,
    AgentToolRef,
    AgentValidationRef,
)
from .handoff import AgentHandoffPlanner, blocked_handoff_decision
from .runtime import AgentRuntime, BlockedAgentRuntime, NoOpAgentRuntime, blocked_agent_decision_from_task


__all__ = (
    "AgentApprovalRef",
    "AgentBlockedReason",
    "AgentBlocker",
    "AgentContextEnvelope",
    "AgentEnvelopeKind",
    "AgentEvidenceRef",
    "AgentExecutionDecision",
    "AgentExecutionDecisionStatus",
    "AgentHandoffEnvelope",
    "AgentHandoffPlanner",
    "AgentIncidentRef",
    "AgentInstructionEnvelope",
    "AgentLimitation",
    "AgentOutputEnvelope",
    "AgentProviderRef",
    "AgentRetentionRef",
    "AgentRollbackRef",
    "AgentRuntime",
    "AgentRuntimeRef",
    "AgentRuntimeState",
    "AgentSecurityRef",
    "AgentTaskEnvelope",
    "AgentToolRef",
    "AgentValidationRef",
    "BlockedAgentRuntime",
    "NoOpAgentRuntime",
    "blocked_agent_decision_from_task",
    "blocked_handoff_decision",
)
