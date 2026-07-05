"""Inert tool allowlist metadata logic.

The allowlist is deny by default. A metadata match is not execution approval and
does not execute tools, call payloads, read files, traverse directories, run
commands, persist decisions, or create generated artifacts.
"""

from __future__ import annotations

from .contracts import (
    ToolAllowlistEntry,
    ToolBlocker,
    ToolDenyReason,
    ToolExecutionDecision,
    ToolExecutionRequest,
    ToolRiskLevel,
    ToolSandboxDecisionStatus,
    ToolSandboxPolicy,
    ToolSideEffectProfile,
)


_SIDE_EFFECT_DENY_REASONS: dict[ToolSideEffectProfile, ToolDenyReason] = {
    ToolSideEffectProfile.FILESYSTEM_READ: ToolDenyReason.FILESYSTEM_READ_BLOCKED,
    ToolSideEffectProfile.FILESYSTEM_WRITE: ToolDenyReason.FILESYSTEM_WRITE_BLOCKED,
    ToolSideEffectProfile.NETWORK: ToolDenyReason.NETWORK_BLOCKED,
    ToolSideEffectProfile.PROVIDER_API: ToolDenyReason.PROVIDER_AUTH_BLOCKED,
    ToolSideEffectProfile.MCP: ToolDenyReason.MCP_BLOCKED,
    ToolSideEffectProfile.GIT: ToolDenyReason.GIT_BLOCKED,
    ToolSideEffectProfile.GENERATED_OUTPUT: ToolDenyReason.GENERATED_OUTPUT_BLOCKED,
    ToolSideEffectProfile.PRODUCT: ToolDenyReason.PRODUCT_BLOCKED,
    ToolSideEffectProfile.RUNTIME_STATE: ToolDenyReason.AGENT_EXECUTION_BLOCKED,
    ToolSideEffectProfile.UNKNOWN: ToolDenyReason.UNKNOWN_SENSITIVITY,
}


def build_denied_tool_decision(
    request: ToolExecutionRequest,
    *,
    status: ToolSandboxDecisionStatus = ToolSandboxDecisionStatus.DENIED,
    deny_reasons: tuple[ToolDenyReason, ...] = (ToolDenyReason.EXECUTION_BLOCKED,),
    summary: str = "Tool execution remains blocked.",
    allowlist_entry_id: str | None = None,
) -> ToolExecutionDecision:
    """Build a metadata-only denied decision without executing anything."""

    blockers = tuple(
        ToolBlocker(
            blocker_id=f"tool_deny_reason:{reason.value}",
            reason=f"Tool request denied: {reason.value}.",
            deny_reason=reason,
            refs=("P3.3", "P3.BR"),
        )
        for reason in deny_reasons
    )
    side_effect_profile = request.effective_side_effect_profile()
    return ToolExecutionDecision(
        decision_id=f"{request.request_id}:denied",
        request_id=request.request_id,
        tool_id=request.descriptor.tool_id,
        status=status,
        summary=summary,
        risk_level=request.descriptor.risk_level,
        side_effect_profile=side_effect_profile,
        deny_reasons=deny_reasons,
        blockers=(*request.blockers, *blockers),
        allowlist_entry_id=allowlist_entry_id,
        evidence_refs=request.evidence_refs,
        validation_refs=request.validation_refs,
        security_refs=request.security_refs,
        source_classification_refs=request.source_classification_refs,
        retention_refs=request.retention_refs,
        rollback_refs=request.rollback_refs,
        incident_refs=request.incident_refs,
        audit_refs=request.audit_refs,
        tool_boundary_refs=request.descriptor.tool_boundary_refs,
        provider_decision_refs=request.provider_decision_refs,
        agent_decision_refs=request.agent_decision_refs,
    )


class ToolAllowlist:
    """Deny-by-default metadata allowlist.

    The class evaluates request metadata only. It never executes a request.
    """

    def __init__(
        self,
        entries: tuple[ToolAllowlistEntry, ...] = (),
        policy: ToolSandboxPolicy | None = None,
    ) -> None:
        self.entries = entries
        self.policy = policy or ToolSandboxPolicy()

    def match(self, request: ToolExecutionRequest) -> ToolAllowlistEntry | None:
        """Return matching metadata entry, not execution approval."""

        for entry in self.entries:
            if entry.tool_id == request.descriptor.tool_id:
                return entry
        return None

    def decide(self, request: ToolExecutionRequest) -> ToolExecutionDecision:
        """Return a metadata-only deny/defer decision for the request."""

        reasons = [
            ToolDenyReason.EXECUTION_BLOCKED,
            ToolDenyReason.HUMAN_APPROVAL_REQUIRED,
        ]
        if not request.exact_scope_declared:
            reasons.append(ToolDenyReason.NO_EXACT_SCOPE)

        side_effect_profile = request.effective_side_effect_profile()
        if side_effect_profile not in self.policy.allowed_side_effect_profiles:
            reasons.append(
                _SIDE_EFFECT_DENY_REASONS.get(
                    side_effect_profile,
                    ToolDenyReason.UNKNOWN,
                )
            )

        entry = self.match(request)
        allowlist_entry_id = entry.entry_id if entry is not None else None
        if entry is None:
            reasons.append(ToolDenyReason.NOT_ALLOWLISTED)
        else:
            reasons.extend(blocker.deny_reason for blocker in entry.blockers)
            if entry.risk_level in (
                ToolRiskLevel.HIGH_BLOCKED,
                ToolRiskLevel.CRITICAL_PROHIBITED,
                ToolRiskLevel.UNKNOWN,
            ):
                reasons.append(ToolDenyReason.UNKNOWN_SENSITIVITY)

        unique_reasons = tuple(dict.fromkeys(reasons))
        return build_denied_tool_decision(
            request,
            status=ToolSandboxDecisionStatus.DENIED,
            deny_reasons=unique_reasons,
            summary="Allowlist metadata reviewed; execution is denied by default.",
            allowlist_entry_id=allowlist_entry_id,
        )


__all__ = (
    "ToolAllowlist",
    "build_denied_tool_decision",
)
