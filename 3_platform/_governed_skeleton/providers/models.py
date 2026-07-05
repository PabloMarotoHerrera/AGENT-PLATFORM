"""Metadata-only provider adapter runtime candidate data models.

The objects in this module are inert metadata. They must not contain provider
clients, network clients, MCP clients, auth sessions, API keys, tokens,
passwords, private keys, credential values, provider config contents, request
payloads, responses, product source, external source contents, or raw generated
output.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProviderDecisionStatus(Enum):
    """Canonical metadata-only provider decision statuses."""

    PROVIDER_AUTH_API_MCP_ACTIVATION_DEFERRED = "provider_auth_api_mcp_activation_deferred"
    ACTIVATION_NOT_APPROVED = "activation_not_approved"
    CANDIDATE_FOR_FUTURE_EXACT_ACTIVATION = "candidate_for_future_exact_activation"
    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    PENDING_REVIEW = "pending_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ProviderScope:
    """Metadata-only provider scope; not permission to connect or call."""

    scope_id: str
    provider_id: str
    provider_kind: str = "unknown_provider"
    allowed_metadata_use: str = "describe provider posture and blockers only"
    forbidden_use: tuple[str, ...] = (
        "provider activation",
        "provider call",
        "network call",
        "auth use",
        "MCP activation",
    )
    required_gates: tuple[str, ...] = ("GT-08", "GT-05", "GT-15")
    blockers: tuple[str, ...] = (
        "provider_auth_blocker",
        "provider_network_blocker",
        "provider_mcp_blocker",
    )
    limitations: tuple[str, ...] = ("Provider metadata is not provider activation.",)


@dataclass(frozen=True)
class AuthScope:
    """Metadata-only auth scope; not auth approval."""

    auth_scope_id: str
    provider_id: str
    auth_type: str = "none"
    credential_ref_ids: tuple[str, ...] = ()
    approval_gate: str = "GT-08 plus explicit secure approval"
    security_review_required: bool = True
    credential_values_allowed: bool = False
    auth_active: bool = False
    forbidden_material: tuple[str, ...] = (
        "secret values",
        "credential values",
        "API keys",
        "tokens",
        "passwords",
        "private keys",
        "provider config contents",
        "browser auth",
        "local credential store contents",
    )
    blockers: tuple[str, ...] = ("credential_exposure_blocker", "provider_auth_blocker")
    limitations: tuple[str, ...] = ("CredentialRef metadata only; no credential value handling.",)


@dataclass(frozen=True)
class NetworkScope:
    """Metadata-only network scope; not network/API/provider permission."""

    network_scope_id: str
    provider_id: str
    network_kind: str = "none"
    endpoint_classification: str = "none"
    data_sent: str = "none"
    data_received: str = "none"
    approval_gate: str = "GT-08"
    network_allowed: bool = False
    api_call_allowed: bool = False
    provider_call_allowed: bool = False
    telemetry_allowed: bool = False
    blockers: tuple[str, ...] = ("provider_network_blocker",)
    limitations: tuple[str, ...] = ("no network", "no API call", "no provider call")


@dataclass(frozen=True)
class MCPScope:
    """Metadata-only MCP scope; not MCP activation."""

    mcp_scope_id: str
    provider_id: str
    mcp_server_ref: str = "none"
    mcp_capability_refs: tuple[str, ...] = ()
    approval_gate: str = "GT-08 plus GT-07/GT-05 as applicable"
    mcp_activation_allowed: bool = False
    mcp_tool_invocation_allowed: bool = False
    mcp_resource_exposure_allowed: bool = False
    blockers: tuple[str, ...] = ("provider_mcp_blocker",)
    limitations: tuple[str, ...] = ("MCP metadata is not MCP activation.",)


@dataclass(frozen=True)
class CredentialRef:
    """Redacted credential reference metadata only; never a credential value."""

    credential_ref_id: str
    provider_id: str
    credential_kind: str = "none"
    credential_owner: str = "unknown"
    storage_classification: str = "none"
    sensitivity: str = "credential_related"
    local_only: bool = True
    secret_related: bool = False
    credential_related: bool = True
    value_present: bool = False
    value_validation_allowed: bool = False
    allowed_metadata_use: str = "record that a future credential gate may be required"
    forbidden_use: tuple[str, ...] = (
        "credential value inspection",
        "credential value retention",
        "auth use",
        "provider call",
        "network call",
        "publication",
    )
    approval_gate: str = "GT-08 plus explicit secure approval"
    review_required: bool = True
    blockers: tuple[str, ...] = ("credential_exposure_blocker", "provider_auth_blocker")
    limitations: tuple[str, ...] = ("API key availability is not API key approval.",)


@dataclass(frozen=True)
class ProviderDescriptor:
    """Metadata record for a provider candidate, not a live provider."""

    provider_id: str
    provider_name: str
    provider_owner: str
    provider_scope: ProviderScope
    auth_scope: AuthScope
    network_scope: NetworkScope
    mcp_scope: MCPScope
    provider_kind: str = "unknown_provider"
    provider_status: ProviderDecisionStatus = ProviderDecisionStatus.PROVIDER_AUTH_API_MCP_ACTIVATION_DEFERRED
    provider_capabilities: tuple[str, ...] = ()
    adapter_refs: tuple[str, ...] = ()
    credential_refs: tuple[CredentialRef, ...] = ()
    endpoint_refs: tuple[str, ...] = ()
    config_refs: tuple[str, ...] = ()
    context_refs: tuple[str, ...] = ()
    tool_refs: tuple[str, ...] = ()
    agent_refs: tuple[str, ...] = ()
    product_refs: tuple[str, ...] = ()
    activation_blockers: tuple[str, ...] = (
        "provider_auth_blocker",
        "provider_network_blocker",
        "provider_mcp_blocker",
    )
    evidence_refs: tuple[str, ...] = ()
    validation_refs: tuple[str, ...] = ()
    security_refs: tuple[str, ...] = ()
    retention_posture: str = "metadata-only"
    review_required: bool = True
    metadata_only: bool = True
    activation_approved: bool = False
    limitations: tuple[str, ...] = ("Provider metadata is not provider activation.",)


@dataclass(frozen=True)
class AdapterDescriptor:
    """Metadata record for an adapter candidate, not runtime adapter code."""

    adapter_id: str
    provider_id: str
    adapter_name: str
    adapter_owner: str
    adapter_scope: str
    adapter_kind: str = "unknown_adapter"
    adapter_status: ProviderDecisionStatus = ProviderDecisionStatus.ACTIVATION_NOT_APPROVED
    supported_operations: tuple[str, ...] = ()
    input_contract_refs: tuple[str, ...] = ()
    output_contract_refs: tuple[str, ...] = ()
    provider_capability_refs: tuple[str, ...] = ()
    context_requirement_refs: tuple[str, ...] = ()
    tool_requirement_refs: tuple[str, ...] = ()
    agent_requirement_refs: tuple[str, ...] = ()
    auth_posture: str = "not approved"
    network_posture: str = "not approved"
    mcp_posture: str = "not approved"
    execution_posture: str = "not approved"
    activation_requirements: tuple[str, ...] = ("GT-08", "GT-05", "GT-15")
    activation_blockers: tuple[str, ...] = (
        "provider_auth_blocker",
        "provider_network_blocker",
        "provider_mcp_blocker",
        "tool_execution_blocker",
    )
    evidence_refs: tuple[str, ...] = ()
    validation_refs: tuple[str, ...] = ()
    security_refs: tuple[str, ...] = ()
    retention_posture: str = "metadata-only"
    review_required: bool = True
    metadata_only: bool = True
    activation_approved: bool = False
    limitations: tuple[str, ...] = ("Adapter metadata is not adapter activation.",)


@dataclass(frozen=True)
class ProviderDecision:
    """Metadata-only decision returned by inert provider adapter components."""

    decision_id: str
    provider_id: str
    status: ProviderDecisionStatus
    adapter_id: str | None = None
    reason: str = "Provider/auth/API/MCP activation remains blocked."
    required_gates: tuple[str, ...] = ("GT-08", "GT-05", "GT-15")
    blockers: tuple[str, ...] = (
        "provider_auth_blocker",
        "provider_network_blocker",
        "provider_mcp_blocker",
    )
    evidence_refs: tuple[str, ...] = ()
    validation_refs: tuple[str, ...] = ()
    security_refs: tuple[str, ...] = ()
    human_approval_required: bool = True
    metadata_only: bool = True
    activation_approved: bool = False
    provider_call_allowed: bool = False
    network_allowed: bool = False
    mcp_activation_allowed: bool = False
    side_effects: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ("no provider call", "no network", "no MCP activation")
