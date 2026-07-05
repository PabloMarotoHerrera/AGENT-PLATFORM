"""Metadata-only tool sandbox contracts for the governed skeleton.

These records describe tool posture. They do not execute tools, commands,
shells, subprocesses, filesystem actions, network calls, providers, MCP,
Graphify, Codegraph, GBrain, Hermes, Cadence, products, or agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ToolRiskLevel(Enum):
    """Risk levels for metadata-only tool descriptions."""

    LOW_METADATA_ONLY = "low_metadata_only"
    MEDIUM_REVIEW_REQUIRED = "medium_review_required"
    HIGH_BLOCKED = "high_blocked"
    CRITICAL_PROHIBITED = "critical_prohibited"
    UNKNOWN = "unknown"


class ToolDenyReason(Enum):
    """Deny reasons used by the inert sandbox candidate."""

    NO_EXACT_SCOPE = "no_exact_scope"
    EXECUTION_BLOCKED = "execution_blocked"
    SHELL_BLOCKED = "shell_blocked"
    SUBPROCESS_BLOCKED = "subprocess_blocked"
    FILESYSTEM_READ_BLOCKED = "filesystem_read_blocked"
    FILESYSTEM_WRITE_BLOCKED = "filesystem_write_blocked"
    NETWORK_BLOCKED = "network_blocked"
    PACKAGE_MANAGER_BLOCKED = "package_manager_blocked"
    BUILD_BLOCKED = "build_blocked"
    TEST_BLOCKED = "test_blocked"
    CI_BLOCKED = "ci_blocked"
    GIT_BLOCKED = "git_blocked"
    GRAPHIFY_BLOCKED = "graphify_blocked"
    CODEGRAPH_BLOCKED = "codegraph_blocked"
    MCP_BLOCKED = "mcp_blocked"
    LIVE_CONNECTOR_BLOCKED = "live_connector_blocked"
    PRODUCT_BLOCKED = "product_blocked"
    GENERATED_OUTPUT_BLOCKED = "generated_output_blocked"
    PROVIDER_AUTH_BLOCKED = "provider_auth_blocked"
    AGENT_EXECUTION_BLOCKED = "agent_execution_blocked"
    GBRAIN_HERMES_CADENCE_BLOCKED = "gbrain_hermes_cadence_blocked"
    SECRET_CREDENTIAL_RISK = "secret_credential_risk"
    UNKNOWN_SENSITIVITY = "unknown_sensitivity"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    RETENTION_REVIEW_REQUIRED = "retention_review_required"
    ROLLBACK_REVIEW_REQUIRED = "rollback_review_required"
    INCIDENT_ROUTE_REQUIRED = "incident_route_required"
    NOT_ALLOWLISTED = "not_allowlisted"
    UNKNOWN = "unknown"


class ToolSandboxDecisionStatus(Enum):
    """Non-executing sandbox decision statuses."""

    NOT_EXECUTED = "not_executed"
    DENIED = "denied"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    DRY_RUN_ONLY = "dry_run_only"
    METADATA_ONLY = "metadata_only"
    NEEDS_REVIEW = "needs_review"
    INVALID_SCOPE = "invalid_scope"


class ToolSideEffectProfile(Enum):
    """Side-effect profile metadata for future tool review."""

    NO_SIDE_EFFECT = "no_side_effect"
    METADATA_ONLY = "metadata_only"
    READ_ONLY_GOVERNANCE_METADATA = "read_only_governance_metadata"
    FILESYSTEM_READ = "filesystem_read"
    FILESYSTEM_WRITE = "filesystem_write"
    NETWORK = "network"
    PROVIDER_API = "provider_api"
    MCP = "mcp"
    GIT = "git"
    GENERATED_OUTPUT = "generated_output"
    PRODUCT = "product"
    RUNTIME_STATE = "runtime_state"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ToolBlocker:
    """Metadata blocker that prevents tool execution."""

    blocker_id: str
    reason: str
    deny_reason: ToolDenyReason = ToolDenyReason.EXECUTION_BLOCKED
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.BLOCKED
    required_gate: str = "future_exact_human_approved_tool_gate_required"
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ToolApprovalRef:
    """Approval metadata reference, not approval itself."""

    ref_id: str
    description: str = ""
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.NEEDS_REVIEW
    human_approval_required: bool = True
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ToolInputRef:
    """Metadata reference to a tool input surface."""

    ref_id: str
    classification: str = "unknown"
    sensitivity: str = "unknown"
    description: str = ""
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.NEEDS_REVIEW
    blocked: bool = True
    blocker_reason: str = "Input is not approved for executable tool use by default."
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ToolOutputRef:
    """Metadata reference to a possible output, not output creation approval."""

    ref_id: str
    classification: str = "metadata_only"
    description: str = ""
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.BLOCKED
    retention_ref: str = "retention_review_required_before_output_creation"
    rollback_ref: str = "rollback_review_required_before_output_creation"
    incident_ref: str = "incident_route_required_before_output_creation"


@dataclass(frozen=True)
class ToolDescriptor:
    """Metadata-only descriptor for a future tool candidate."""

    tool_id: str
    name: str
    description: str = ""
    risk_level: ToolRiskLevel = ToolRiskLevel.UNKNOWN
    side_effect_profile: ToolSideEffectProfile = ToolSideEffectProfile.UNKNOWN
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.BLOCKED
    tags: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    security_refs: tuple[str, ...] = field(default_factory=tuple)
    tool_boundary_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ToolAllowlistEntry:
    """Descriptive allowlist metadata, not executable permission."""

    entry_id: str
    tool_id: str
    tool_name: str = ""
    candidate_scope: str = "metadata_only_future_candidate"
    risk_level: ToolRiskLevel = ToolRiskLevel.LOW_METADATA_ONLY
    side_effect_profile: ToolSideEffectProfile = ToolSideEffectProfile.METADATA_ONLY
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.DEFERRED
    human_approval_required: bool = True
    approval_refs: tuple[ToolApprovalRef, ...] = field(default_factory=tuple)
    blockers: tuple[ToolBlocker, ...] = field(default_factory=tuple)
    refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ToolExecutionRequest:
    """Metadata-only future request envelope, not a runnable command."""

    request_id: str
    descriptor: ToolDescriptor
    purpose: str = "metadata_only_review"
    scope_statement: str = ""
    exact_scope_declared: bool = False
    requested_side_effect_profile: ToolSideEffectProfile = ToolSideEffectProfile.UNKNOWN
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.NOT_EXECUTED
    input_refs: tuple[ToolInputRef, ...] = field(default_factory=tuple)
    output_refs: tuple[ToolOutputRef, ...] = field(default_factory=tuple)
    approval_refs: tuple[ToolApprovalRef, ...] = field(default_factory=tuple)
    blockers: tuple[ToolBlocker, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    validation_refs: tuple[str, ...] = field(default_factory=tuple)
    security_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)
    retention_refs: tuple[str, ...] = field(default_factory=tuple)
    rollback_refs: tuple[str, ...] = field(default_factory=tuple)
    incident_refs: tuple[str, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)
    provider_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    agent_decision_refs: tuple[str, ...] = field(default_factory=tuple)

    def effective_side_effect_profile(self) -> ToolSideEffectProfile:
        """Return side-effect metadata without inspecting or executing anything."""

        if self.requested_side_effect_profile is not ToolSideEffectProfile.UNKNOWN:
            return self.requested_side_effect_profile
        return self.descriptor.side_effect_profile


@dataclass(frozen=True)
class ToolExecutionDecision:
    """Metadata-only sandbox decision."""

    decision_id: str
    request_id: str
    tool_id: str
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.DENIED
    summary: str = "Tool execution remains blocked."
    risk_level: ToolRiskLevel = ToolRiskLevel.UNKNOWN
    side_effect_profile: ToolSideEffectProfile = ToolSideEffectProfile.UNKNOWN
    deny_reasons: tuple[ToolDenyReason, ...] = field(default_factory=tuple)
    blockers: tuple[ToolBlocker, ...] = field(default_factory=tuple)
    allowlist_entry_id: str | None = None
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    validation_refs: tuple[str, ...] = field(default_factory=tuple)
    security_refs: tuple[str, ...] = field(default_factory=tuple)
    source_classification_refs: tuple[str, ...] = field(default_factory=tuple)
    retention_refs: tuple[str, ...] = field(default_factory=tuple)
    rollback_refs: tuple[str, ...] = field(default_factory=tuple)
    incident_refs: tuple[str, ...] = field(default_factory=tuple)
    audit_refs: tuple[str, ...] = field(default_factory=tuple)
    tool_boundary_refs: tuple[str, ...] = field(default_factory=tuple)
    provider_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    agent_decision_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ToolSandboxPolicy:
    """Deny-by-default policy metadata."""

    policy_id: str = "deny_by_default_tool_sandbox_policy"
    name: str = "Deny by default tool sandbox policy"
    deny_by_default: bool = True
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.BLOCKED
    allowed_side_effect_profiles: tuple[ToolSideEffectProfile, ...] = (
        ToolSideEffectProfile.NO_SIDE_EFFECT,
        ToolSideEffectProfile.METADATA_ONLY,
    )
    required_gates: tuple[str, ...] = (
        "P3.3",
        "P3.BR",
        "P5.2_or_pending_alignment",
        "P5.7_or_pending_alignment",
        "human_approval",
    )
    pending_alignments: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[ToolBlocker, ...] = field(default_factory=tuple)


__all__ = (
    "ToolAllowlistEntry",
    "ToolApprovalRef",
    "ToolBlocker",
    "ToolDenyReason",
    "ToolDescriptor",
    "ToolExecutionDecision",
    "ToolExecutionRequest",
    "ToolInputRef",
    "ToolOutputRef",
    "ToolRiskLevel",
    "ToolSandboxDecisionStatus",
    "ToolSandboxPolicy",
    "ToolSideEffectProfile",
)
