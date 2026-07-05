"""In-memory metadata-only provider registry for P5.5.

ProviderRegistry stores ProviderDescriptor and AdapterDescriptor objects only.
It has no persistence, no provider clients, no provider call, no network, no
auth configuration, no MCP activation, no telemetry, and no product behavior.
"""

from __future__ import annotations

from .adapters import BlockedProviderAdapter, NullProviderAdapter, ProviderAdapter
from .models import AdapterDescriptor, ProviderDecision, ProviderDecisionStatus, ProviderDescriptor


class ProviderRegistry:
    """In-memory metadata-only registry for provider and adapter descriptors."""

    def __init__(self) -> None:
        self._providers: dict[str, ProviderDescriptor] = {}
        self._adapters: dict[str, AdapterDescriptor] = {}

    def register_provider(self, descriptor: ProviderDescriptor) -> ProviderDecision:
        """Store ProviderDescriptor metadata and return a non-activation decision."""

        if not isinstance(descriptor, ProviderDescriptor):
            raise TypeError("ProviderRegistry.register_provider requires ProviderDescriptor metadata")
        self._providers[descriptor.provider_id] = descriptor
        return self._decision_for_provider(descriptor)

    def register_adapter(self, descriptor: AdapterDescriptor) -> ProviderDecision:
        """Store AdapterDescriptor metadata and return a non-activation decision."""

        if not isinstance(descriptor, AdapterDescriptor):
            raise TypeError("ProviderRegistry.register_adapter requires AdapterDescriptor metadata")
        self._adapters[descriptor.adapter_id] = descriptor
        provider = self._providers.get(descriptor.provider_id)
        return self._decision_for_adapter(descriptor, provider)

    def get_provider(self, provider_id: str) -> ProviderDescriptor | None:
        """Return provider metadata by ID without side effects."""

        return self._providers.get(provider_id)

    def get_adapter(self, adapter_id: str) -> AdapterDescriptor | None:
        """Return adapter metadata by ID without side effects."""

        return self._adapters.get(adapter_id)

    def list_provider_descriptors(self) -> tuple[ProviderDescriptor, ...]:
        """Return registered provider metadata only."""

        return tuple(self._providers.values())

    def list_adapter_descriptors(self) -> tuple[AdapterDescriptor, ...]:
        """Return registered adapter metadata only."""

        return tuple(self._adapters.values())

    def adapter_for(self, adapter_id: str) -> ProviderAdapter:
        """Return an inert adapter wrapper, never a live provider client."""

        descriptor = self._adapters.get(adapter_id)
        if descriptor is None:
            missing = AdapterDescriptor(
                adapter_id=adapter_id,
                provider_id="unknown_provider",
                adapter_name="missing adapter metadata",
                adapter_owner="unknown",
                adapter_scope="missing adapter metadata; activation blocked",
                activation_blockers=("missing_adapter_descriptor", "provider_auth_blocker"),
            )
            return BlockedProviderAdapter(missing, blockers=("missing_adapter_descriptor",))
        if descriptor.activation_blockers:
            return BlockedProviderAdapter(descriptor)
        return NullProviderAdapter(descriptor)

    def decision_for(self, provider_id: str, adapter_id: str | None = None) -> ProviderDecision:
        """Return metadata-only decision for provider or adapter IDs."""

        provider = self._providers.get(provider_id)
        if provider is None:
            return ProviderDecision(
                decision_id=f"P5.5-PROVIDER-DECISION-{provider_id}",
                provider_id=provider_id,
                adapter_id=adapter_id,
                status=ProviderDecisionStatus.BLOCKED,
                reason="Provider metadata is missing; provider/auth/API/MCP activation remains blocked.",
                blockers=("missing_provider_descriptor", "provider_auth_blocker"),
            )
        if adapter_id is None:
            return self._decision_for_provider(provider)
        adapter = self._adapters.get(adapter_id)
        if adapter is None:
            return ProviderDecision(
                decision_id=f"P5.5-PROVIDER-DECISION-{provider_id}-{adapter_id}",
                provider_id=provider_id,
                adapter_id=adapter_id,
                status=ProviderDecisionStatus.BLOCKED,
                reason="Adapter metadata is missing; provider/auth/API/MCP activation remains blocked.",
                blockers=("missing_adapter_descriptor", "provider_auth_blocker"),
            )
        return self._decision_for_adapter(adapter, provider)

    def _decision_for_provider(self, descriptor: ProviderDescriptor) -> ProviderDecision:
        status = self._status_for_descriptor(descriptor)
        return ProviderDecision(
            decision_id=f"P5.5-PROVIDER-DECISION-{descriptor.provider_id}",
            provider_id=descriptor.provider_id,
            status=status,
            reason="ProviderRegistry stores metadata-only ProviderDescriptor records; no provider call is approved.",
            blockers=descriptor.activation_blockers,
            evidence_refs=descriptor.evidence_refs,
            validation_refs=descriptor.validation_refs,
            security_refs=descriptor.security_refs,
            limitations=descriptor.limitations + ("no provider call", "no network", "no MCP activation"),
        )

    def _decision_for_adapter(
        self,
        descriptor: AdapterDescriptor,
        provider: ProviderDescriptor | None,
    ) -> ProviderDecision:
        adapter = BlockedProviderAdapter(descriptor) if descriptor.activation_blockers else NullProviderAdapter(descriptor)
        return adapter.decision(provider)

    def _status_for_descriptor(self, descriptor: ProviderDescriptor) -> ProviderDecisionStatus:
        if descriptor.activation_approved:
            return ProviderDecisionStatus.BLOCKED
        if not descriptor.metadata_only:
            return ProviderDecisionStatus.BLOCKED
        if descriptor.activation_blockers:
            return ProviderDecisionStatus.PROVIDER_AUTH_API_MCP_ACTIVATION_DEFERRED
        return ProviderDecisionStatus.METADATA_ONLY
