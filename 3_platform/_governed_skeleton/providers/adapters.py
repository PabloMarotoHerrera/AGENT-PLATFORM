"""Inert provider adapter classes for P5.5.

ProviderAdapter, NullProviderAdapter, and BlockedProviderAdapter expose only
metadata descriptions and blocked decisions. They perform no provider call,
no network action, no auth flow, no MCP activation, no source loading, no
product behavior, no persistence, and no telemetry.
"""

from __future__ import annotations

from .models import AdapterDescriptor, ProviderDecision, ProviderDecisionStatus, ProviderDescriptor


NO_PROVIDER_CALL_LIMITATION = "no provider call"
NO_NETWORK_LIMITATION = "no network"
NO_MCP_LIMITATION = "no MCP activation"


class ProviderAdapter:
    """Base metadata-only adapter wrapper; not a provider client."""

    def __init__(self, descriptor: AdapterDescriptor) -> None:
        if not isinstance(descriptor, AdapterDescriptor):
            raise TypeError("ProviderAdapter requires AdapterDescriptor metadata")
        self._descriptor = descriptor

    @property
    def descriptor(self) -> AdapterDescriptor:
        """Return adapter metadata without side effects."""

        return self._descriptor

    def describe(self) -> AdapterDescriptor:
        """Return adapter metadata only."""

        return self._descriptor

    def decision(self, provider: ProviderDescriptor | None = None) -> ProviderDecision:
        """Return a blocked metadata decision; never perform a provider call."""

        provider_id = provider.provider_id if provider is not None else self._descriptor.provider_id
        evidence_refs = provider.evidence_refs if provider is not None else self._descriptor.evidence_refs
        validation_refs = provider.validation_refs if provider is not None else self._descriptor.validation_refs
        security_refs = provider.security_refs if provider is not None else self._descriptor.security_refs
        blockers = self._combined_blockers(provider)
        return ProviderDecision(
            decision_id=f"P5.5-PROVIDER-DECISION-{provider_id}-{self._descriptor.adapter_id}",
            provider_id=provider_id,
            adapter_id=self._descriptor.adapter_id,
            status=ProviderDecisionStatus.PROVIDER_AUTH_API_MCP_ACTIVATION_DEFERRED,
            reason="ProviderAdapter is metadata-only; provider/auth/API/MCP activation remains blocked.",
            blockers=blockers,
            evidence_refs=evidence_refs,
            validation_refs=validation_refs,
            security_refs=security_refs,
            limitations=self._limitations(),
        )

    def activation_decision(self, provider: ProviderDescriptor | None = None) -> ProviderDecision:
        """Return the non-activation decision for this adapter metadata."""

        return self.decision(provider)

    def _combined_blockers(self, provider: ProviderDescriptor | None) -> tuple[str, ...]:
        provider_blockers = provider.activation_blockers if provider is not None else ()
        return tuple(dict.fromkeys(provider_blockers + self._descriptor.activation_blockers))

    def _limitations(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(
                self._descriptor.limitations
                + (NO_PROVIDER_CALL_LIMITATION, NO_NETWORK_LIMITATION, NO_MCP_LIMITATION)
            )
        )


class NullProviderAdapter(ProviderAdapter):
    """Null adapter for metadata-only registration with no runtime behavior."""

    def decision(self, provider: ProviderDescriptor | None = None) -> ProviderDecision:
        decision = super().decision(provider)
        return ProviderDecision(
            decision_id=decision.decision_id,
            provider_id=decision.provider_id,
            adapter_id=decision.adapter_id,
            status=ProviderDecisionStatus.METADATA_ONLY,
            reason="NullProviderAdapter records metadata only and performs no provider call.",
            required_gates=decision.required_gates,
            blockers=decision.blockers,
            evidence_refs=decision.evidence_refs,
            validation_refs=decision.validation_refs,
            security_refs=decision.security_refs,
            human_approval_required=decision.human_approval_required,
            metadata_only=True,
            activation_approved=False,
            provider_call_allowed=False,
            network_allowed=False,
            mcp_activation_allowed=False,
            side_effects=(),
            limitations=decision.limitations,
        )


class BlockedProviderAdapter(ProviderAdapter):
    """Blocked adapter that always returns a blocked non-activation decision."""

    def __init__(self, descriptor: AdapterDescriptor, blockers: tuple[str, ...] = ()) -> None:
        super().__init__(descriptor)
        self._extra_blockers = blockers

    def decision(self, provider: ProviderDescriptor | None = None) -> ProviderDecision:
        decision = super().decision(provider)
        blockers = tuple(dict.fromkeys(decision.blockers + self._extra_blockers))
        return ProviderDecision(
            decision_id=decision.decision_id,
            provider_id=decision.provider_id,
            adapter_id=decision.adapter_id,
            status=ProviderDecisionStatus.BLOCKED,
            reason="BlockedProviderAdapter preserves provider/auth/API/MCP activation blockers.",
            required_gates=decision.required_gates,
            blockers=blockers,
            evidence_refs=decision.evidence_refs,
            validation_refs=decision.validation_refs,
            security_refs=decision.security_refs,
            human_approval_required=decision.human_approval_required,
            metadata_only=True,
            activation_approved=False,
            provider_call_allowed=False,
            network_allowed=False,
            mcp_activation_allowed=False,
            side_effects=(),
            limitations=decision.limitations,
        )
