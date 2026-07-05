"""Non-active provider adapter runtime candidate package.

This package exposes metadata-only provider descriptor, adapter descriptor,
CredentialRef, inert adapter, and in-memory registry types. Importing it does
not read files, inspect environment variables, configure auth, create network
clients, start MCP, configure logging, or activate provider runtime behavior.
"""

from .adapters import BlockedProviderAdapter, NullProviderAdapter, ProviderAdapter
from .models import (
    AdapterDescriptor,
    AuthScope,
    CredentialRef,
    MCPScope,
    NetworkScope,
    ProviderDecision,
    ProviderDecisionStatus,
    ProviderDescriptor,
    ProviderScope,
)
from .registry import ProviderRegistry

__all__ = (
    "ProviderDecisionStatus",
    "ProviderScope",
    "AuthScope",
    "NetworkScope",
    "MCPScope",
    "CredentialRef",
    "ProviderDescriptor",
    "AdapterDescriptor",
    "ProviderDecision",
    "ProviderAdapter",
    "NullProviderAdapter",
    "BlockedProviderAdapter",
    "ProviderRegistry",
)
