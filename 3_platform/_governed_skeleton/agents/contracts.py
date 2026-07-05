"""Metadata-only agent task and handoff contracts.

These records describe agent runtime posture. They do not execute agents, tasks,
handoffs, tools, providers, MCP, shell commands, subprocesses, filesystem
actions, network calls, Graphify, Codegraph, GBrain, Hermes, Cadence, product
actions, or active runtime behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AgentRuntimeState(Enum):
    """Metadata-only agent runtime states."""

    NOT_STARTED = "not_started"
    METADATA_ONLY = "metadata_only"
    NO_OP = "no_op"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    NEEDS_REVIEW = "needs_review"
    INVALID_SCOPE = "invalid_scope"
    RETIRED = "retired"


class AgentExecutionDecisionStatus(Enum):
    """Non-executing decision statuses for agent envelopes."""

    NOT_EXECUTED = "not_executed"
    DENIED = "denied"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    NO_OP = "no_op"
    METADATA_ONLY = "metadata_only"
    NEEDS_REVIEW = "needs_review"
    INVALID_SCOPE = "invalid_scope"


class AgentBlockedReason(Enum):
    """Blocked reasons for inert agent runtime decisions."""

    RUNTIME_ACTIVATION_BLOCKED = "runtime_activation_blocked"
    TASK_EXECUTION_BLOCKED = "task_execution_blocked"
    HANDOFF_EXECUTION_BLOCKED = "handoff_execution_blocked"
    SCHEDULER_BLOCKED = "scheduler_blocked"
    ORCHESTRATION_BLOCKED = "orchestration_blocked"
    AUTONOMOUS_LOOP_BLOCKED = "autonomous_loop_blocked"
    TOOL_EXECUTION_BLOCKED = "tool_execution_blocked"
    PROVIDER_AUTH_BLOCKED = "provider_auth_blocked"
    MCP_BLOCKED = "mcp_blocked"
    LIVE_CONNECTOR_BLOCKED = "live_connector_blocked"
    PRODUCT_SOURCE_BLOCKED = "product_source_blocked"
    PRODUCT_ACTION_BLOCKED = "product_action_blocked"
    SOURCE_LOADING_BLOCKED = "source_loading_blocked"
    SECRET_CREDENTIAL_RISK = "secret_credential_risk"
    UNKNOWN_SENSITIVITY = "unknown_sensitivity"
    VALIDATION_EXECUTION_BLOCKED = "validation_execution_blocked"
    SECURITY_REVIEW_REQUIRED = "security_review_required"
    RETENTION_REVIEW_REQUIRED = "retention_review_required"
    ROLLBACK_REVIEW_REQUIRED = "rollback_review_required"
    INCIDENT_ROUTE_REQUIRED = "incident_route_required"
    GBRAIN_HERMES_CADENCE_BLOCKED = "gbrain_hermes_cadence_blocked"
    SUBSTRATE_SELECTION_BLOCKED = "substrate_selection_blocked"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    PENDING_CONTEXT_ALIGNMENT = "pending_context_alignment"
    PENDING_TOOL_ALIGNMENT = "pending_tool_alignment"
    PENDING_PROVIDER_ALIGNMENT = "pending_provider_alignment"
    PENDING_AUDIT_ALIGNMENT = "pending_audit_alignment"
    UNKNOWN = "unknown"


class AgentEnvelopeKind(Enum):
    """Metadata-only envelope kinds."""

    TASK = "task"
    INSTRUCTION = "instruction"
    CONTEXT = "context"
    OUTPUT = "output"
    HANDOFF = "handoff"
    APPROVAL = "approval"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AgentEvidenceRef:
    """Evidence metadata reference, not authority."""

    ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.METADATA_ONLY


@dataclass(frozen=True)
class AgentValidationRef:
    """Validation metadata reference, not validation execution."""

    ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.METADATA_ONLY


@dataclass(frozen=True)
class AgentSecurityRef:
    """Security metadata reference, not security enforcement activation."""

    ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW


@dataclass(frozen=True)
class AgentRetentionRef:
    """Retention metadata reference, not persistence approval."""

    ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW


@dataclass(frozen=True)
class AgentRollbackRef:
    """Rollback metadata reference, not rollback automation."""

    ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW


@dataclass(frozen=True)
class AgentIncidentRef:
    """Incident metadata reference, not automatic incident routing."""

    ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW


@dataclass(frozen=True)
class AgentBlocker:
    """Metadata blocker that prevents agent execution."""

    blocker_id: str
    reason: str
    blocked_reason: AgentBlockedReason = AgentBlockedReason.RUNTIME_ACTIVATION_BLOCKED
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED
    required_gate: str = "future_exact_human_approved_agent_gate_required"
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentLimitation:
    """Metadata limitation for future review."""

    limitation_id: str
    description: str
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentRuntimeRef:
    """Metadata-only runtime reference, not runtime activation."""

    runtime_id: str
    name: str = "metadata_only_agent_runtime_candidate"
    state: AgentRuntimeState = AgentRuntimeState.BLOCKED
    description: str = ""
    activation_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentApprovalRef:
    """Approval metadata reference, not approval itself."""

    approval_id: str
    kind: AgentEnvelopeKind = AgentEnvelopeKind.APPROVAL
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW
    human_approval_required: bool = True
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentToolRef:
    """Tool metadata reference, not tool execution."""

    tool_ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED
    tool_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentProviderRef:
    """Provider metadata reference, not provider activation."""

    provider_ref_id: str
    description: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED
    provider_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentInstructionEnvelope:
    """Metadata-only instruction envelope, not executable instruction."""

    envelope_id: str
    title: str
    kind: AgentEnvelopeKind = AgentEnvelopeKind.INSTRUCTION
    instruction_summary: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.METADATA_ONLY
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)
    evidence_refs: tuple[AgentEvidenceRef, ...] = field(default_factory=tuple)
    validation_refs: tuple[AgentValidationRef, ...] = field(default_factory=tuple)
    security_refs: tuple[AgentSecurityRef, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentContextEnvelope:
    """Metadata-only context envelope, not source loading permission."""

    envelope_id: str
    title: str
    kind: AgentEnvelopeKind = AgentEnvelopeKind.CONTEXT
    context_summary: str = ""
    sensitivity: str = "unknown"
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NEEDS_REVIEW
    context_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)
    evidence_refs: tuple[AgentEvidenceRef, ...] = field(default_factory=tuple)
    validation_refs: tuple[AgentValidationRef, ...] = field(default_factory=tuple)
    security_refs: tuple[AgentSecurityRef, ...] = field(default_factory=tuple)
    retention_refs: tuple[AgentRetentionRef, ...] = field(default_factory=tuple)
    rollback_refs: tuple[AgentRollbackRef, ...] = field(default_factory=tuple)
    incident_refs: tuple[AgentIncidentRef, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentOutputEnvelope:
    """Metadata-only output envelope, not output persistence approval."""

    envelope_id: str
    title: str
    kind: AgentEnvelopeKind = AgentEnvelopeKind.OUTPUT
    output_summary: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NOT_EXECUTED
    persistence_status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)
    evidence_refs: tuple[AgentEvidenceRef, ...] = field(default_factory=tuple)
    validation_refs: tuple[AgentValidationRef, ...] = field(default_factory=tuple)
    security_refs: tuple[AgentSecurityRef, ...] = field(default_factory=tuple)
    retention_refs: tuple[AgentRetentionRef, ...] = field(default_factory=tuple)
    rollback_refs: tuple[AgentRollbackRef, ...] = field(default_factory=tuple)
    incident_refs: tuple[AgentIncidentRef, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentTaskEnvelope:
    """Metadata-only task envelope, not a runnable task."""

    envelope_id: str
    title: str
    kind: AgentEnvelopeKind = AgentEnvelopeKind.TASK
    objective_summary: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.NOT_EXECUTED
    runtime_ref: AgentRuntimeRef | None = None
    instruction_envelope: AgentInstructionEnvelope | None = None
    context_envelope: AgentContextEnvelope | None = None
    output_envelope: AgentOutputEnvelope | None = None
    approval_refs: tuple[AgentApprovalRef, ...] = field(default_factory=tuple)
    tool_refs: tuple[AgentToolRef, ...] = field(default_factory=tuple)
    provider_refs: tuple[AgentProviderRef, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)
    evidence_refs: tuple[AgentEvidenceRef, ...] = field(default_factory=tuple)
    validation_refs: tuple[AgentValidationRef, ...] = field(default_factory=tuple)
    security_refs: tuple[AgentSecurityRef, ...] = field(default_factory=tuple)
    retention_refs: tuple[AgentRetentionRef, ...] = field(default_factory=tuple)
    rollback_refs: tuple[AgentRollbackRef, ...] = field(default_factory=tuple)
    incident_refs: tuple[AgentIncidentRef, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentHandoffEnvelope:
    """Metadata-only handoff envelope, not handoff execution."""

    envelope_id: str
    title: str
    kind: AgentEnvelopeKind = AgentEnvelopeKind.HANDOFF
    source_task_id: str = ""
    source_runtime_ref: AgentRuntimeRef | None = None
    target_runtime_ref: AgentRuntimeRef | None = None
    handoff_summary: str = ""
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED
    approval_refs: tuple[AgentApprovalRef, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)
    evidence_refs: tuple[AgentEvidenceRef, ...] = field(default_factory=tuple)
    validation_refs: tuple[AgentValidationRef, ...] = field(default_factory=tuple)
    security_refs: tuple[AgentSecurityRef, ...] = field(default_factory=tuple)
    retention_refs: tuple[AgentRetentionRef, ...] = field(default_factory=tuple)
    rollback_refs: tuple[AgentRollbackRef, ...] = field(default_factory=tuple)
    incident_refs: tuple[AgentIncidentRef, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AgentExecutionDecision:
    """Metadata-only execution decision, not agent execution."""

    decision_id: str
    task_id: str
    status: AgentExecutionDecisionStatus = AgentExecutionDecisionStatus.BLOCKED
    runtime_state: AgentRuntimeState = AgentRuntimeState.BLOCKED
    summary: str = "Agent execution remains blocked."
    handoff_id: str | None = None
    blocked_reasons: tuple[AgentBlockedReason, ...] = field(default_factory=tuple)
    blockers: tuple[AgentBlocker, ...] = field(default_factory=tuple)
    limitations: tuple[AgentLimitation, ...] = field(default_factory=tuple)
    approval_refs: tuple[AgentApprovalRef, ...] = field(default_factory=tuple)
    tool_refs: tuple[AgentToolRef, ...] = field(default_factory=tuple)
    provider_refs: tuple[AgentProviderRef, ...] = field(default_factory=tuple)
    evidence_refs: tuple[AgentEvidenceRef, ...] = field(default_factory=tuple)
    validation_refs: tuple[AgentValidationRef, ...] = field(default_factory=tuple)
    security_refs: tuple[AgentSecurityRef, ...] = field(default_factory=tuple)
    retention_refs: tuple[AgentRetentionRef, ...] = field(default_factory=tuple)
    rollback_refs: tuple[AgentRollbackRef, ...] = field(default_factory=tuple)
    incident_refs: tuple[AgentIncidentRef, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)


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
    "AgentIncidentRef",
    "AgentInstructionEnvelope",
    "AgentLimitation",
    "AgentOutputEnvelope",
    "AgentProviderRef",
    "AgentRetentionRef",
    "AgentRollbackRef",
    "AgentRuntimeRef",
    "AgentRuntimeState",
    "AgentSecurityRef",
    "AgentTaskEnvelope",
    "AgentToolRef",
    "AgentValidationRef",
)
