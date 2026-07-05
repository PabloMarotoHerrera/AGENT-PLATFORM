"""Inert tool sandbox skeleton.

Sandbox classes return metadata-only decisions. They do not execute tools, shell,
subprocesses, commands, filesystem reads or writes, network calls, providers,
MCP, Graphify, Codegraph, live connectors, product code, agents, or persistence.
"""

from __future__ import annotations

from typing import Protocol

from .allowlist import ToolAllowlist, build_denied_tool_decision
from .contracts import (
    ToolDenyReason,
    ToolExecutionDecision,
    ToolExecutionRequest,
    ToolSandboxDecisionStatus,
)


class ToolSandbox(Protocol):
    """Interface for metadata-only sandbox decisions."""

    def decide(self, request: ToolExecutionRequest) -> ToolExecutionDecision:
        """Return decision metadata; this does not execute a tool."""


class NoOpToolExecutor:
    """No-op executor that never executes requests."""

    def decide(self, request: ToolExecutionRequest) -> ToolExecutionDecision:
        """Return not-executed metadata; this does not execute a tool."""

        return build_denied_tool_decision(
            request,
            status=ToolSandboxDecisionStatus.NOT_EXECUTED,
            deny_reasons=(
                ToolDenyReason.EXECUTION_BLOCKED,
                ToolDenyReason.HUMAN_APPROVAL_REQUIRED,
            ),
            summary="NoOpToolExecutor returned metadata only; tool execution remains blocked.",
        )


class BlockedToolExecutor:
    """Executor posture for explicitly blocked tool execution."""

    def decide(self, request: ToolExecutionRequest) -> ToolExecutionDecision:
        """Return blocked metadata; this does not execute a tool."""

        return build_denied_tool_decision(
            request,
            status=ToolSandboxDecisionStatus.BLOCKED,
            deny_reasons=(
                ToolDenyReason.EXECUTION_BLOCKED,
                ToolDenyReason.HUMAN_APPROVAL_REQUIRED,
                ToolDenyReason.NOT_ALLOWLISTED,
            ),
            summary="BlockedToolExecutor returned blocked metadata; no tool was executed.",
        )


class DenyByDefaultToolSandbox:
    """Sandbox that delegates metadata review to a deny-by-default allowlist."""

    def __init__(self, allowlist: ToolAllowlist | None = None) -> None:
        self.allowlist = allowlist or ToolAllowlist()

    def decide(self, request: ToolExecutionRequest) -> ToolExecutionDecision:
        """Return allowlist metadata decision; this does not execute a tool."""

        return self.allowlist.decide(request)


__all__ = (
    "BlockedToolExecutor",
    "DenyByDefaultToolSandbox",
    "NoOpToolExecutor",
    "ToolSandbox",
)
