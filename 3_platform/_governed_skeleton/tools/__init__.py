"""Inert tool sandbox skeleton exports.

Importing this package performs no runtime initialization, reads no environment,
executes no commands, and activates no providers, tools, agents, MCP, or
connectors.
"""

from .allowlist import ToolAllowlist, build_denied_tool_decision
from .contracts import (
    ToolAllowlistEntry,
    ToolApprovalRef,
    ToolBlocker,
    ToolDenyReason,
    ToolDescriptor,
    ToolExecutionDecision,
    ToolExecutionRequest,
    ToolInputRef,
    ToolOutputRef,
    ToolRiskLevel,
    ToolSandboxDecisionStatus,
    ToolSandboxPolicy,
    ToolSideEffectProfile,
)
from .sandbox import (
    BlockedToolExecutor,
    DenyByDefaultToolSandbox,
    NoOpToolExecutor,
    ToolSandbox,
)


__all__ = (
    "BlockedToolExecutor",
    "DenyByDefaultToolSandbox",
    "NoOpToolExecutor",
    "ToolAllowlist",
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
    "ToolSandbox",
    "ToolSandboxDecisionStatus",
    "ToolSandboxPolicy",
    "ToolSideEffectProfile",
    "build_denied_tool_decision",
)
