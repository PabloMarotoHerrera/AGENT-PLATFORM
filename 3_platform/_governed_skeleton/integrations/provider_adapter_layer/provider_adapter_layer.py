"""I-04 minimal provider/adapter metadata layer boundary.

This module models provider descriptors, adapter descriptors, and adapter
capabilities in memory only. It does not call providers, call APIs, use
network, authenticate, inspect credentials, activate MCP, execute tools,
approve permissions, or imply readiness. Provider registration is not provider
activation. Adapter registration is not adapter activation. MCP adapter metadata
is not MCP activation. Validation evaluates; governance decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class ProviderKind(str, Enum):
    """Declared provider kinds for metadata records."""

    LLM_PROVIDER = "llm_provider"
    CLOUD_PROVIDER = "cloud_provider"
    STORAGE_PROVIDER = "storage_provider"
    IDENTITY_AUTH_PROVIDER = "identity_auth_provider"
    PACKAGE_REGISTRY_PROVIDER = "package_registry_provider"
    TELEMETRY_ANALYTICS_PROVIDER = "telemetry_analytics_provider"
    HOSTING_DEPLOYMENT_PROVIDER = "hosting_deployment_provider"
    SIMULATION_SOLVER_PROVIDER = "simulation_solver_provider"
    OMNIVERSE_NUCLEUS_PROVIDER = "omniverse_nucleus_provider"
    DATA_INGESTION_PROVIDER = "data_ingestion_provider"
    NOTIFICATION_PROVIDER = "notification_provider"
    LOCAL_SERVICE_PROVIDER = "local_service_provider"
    UNKNOWN = "unknown"


class AdapterKind(str, Enum):
    """Declared adapter kinds for metadata records."""

    PROVIDER_API_ADAPTER = "provider_api_adapter"
    LOCAL_TOOL_ADAPTER = "local_tool_adapter"
    SHELL_COMMAND_ADAPTER = "shell_command_adapter"
    FILE_SYSTEM_ADAPTER = "file_system_adapter"
    GIT_ADAPTER = "git_adapter"
    VALIDATION_ADAPTER = "validation_adapter"
    SECURITY_ADAPTER = "security_adapter"
    PRODUCT_BACKEND_ADAPTER = "product_backend_adapter"
    OMNIVERSE_ADAPTER = "omniverse_adapter"
    ENERGYPLUS_ADAPTER = "energyplus_adapter"
    WEB_PLATFORM_ADAPTER = "web_platform_adapter"
    DESKTOP_ADAPTER = "desktop_adapter"
    CLI_ADAPTER = "cli_adapter"
    MCP_ADAPTER = "mcp_adapter"
    UNKNOWN = "unknown"


class ActivationStatus(str, Enum):
    """Activation posture for metadata-only records."""

    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    ACTIVATION_NOT_APPROVED = "activation_not_approved"
    REJECTED_FOR_SCOPE = "rejected_for_scope"


PROVIDER_REGISTRATION_IS_NOT_PROVIDER_ACTIVATION = (
    "provider registration is not provider activation"
)
ADAPTER_REGISTRATION_IS_NOT_ADAPTER_ACTIVATION = (
    "adapter registration is not adapter activation"
)
MCP_ADAPTER_METADATA_IS_NOT_MCP_ACTIVATION = "MCP adapter metadata is not MCP activation"
CREDENTIAL_REFS_ARE_METADATA_ONLY = "credential_refs are metadata references only"
EVIDENCE_REFS_ARE_METADATA_ONLY = "evidence_refs are metadata references only"
NETWORK_REQUIRED_IS_NOT_NETWORK_APPROVAL = "network_required is not network approval"


def _value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    return value


def _tuple_of_strings(values: object) -> object:
    if isinstance(values, str):
        return values
    try:
        return tuple(values)
    except TypeError:
        return values


@dataclass(frozen=True)
class ProviderDescriptor:
    """Metadata-only provider descriptor."""

    provider_id: str
    name: str
    provider_kind: str
    description: str
    activation_status: str = ActivationStatus.ACTIVATION_NOT_APPROVED.value
    auth_required: bool = False
    network_required: bool = False
    data_exposure_risk: str = ""
    credential_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider_kind", _value(self.provider_kind))
        object.__setattr__(self, "activation_status", _value(self.activation_status))
        object.__setattr__(self, "credential_refs", _tuple_of_strings(self.credential_refs))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class AdapterDescriptor:
    """Metadata-only adapter descriptor."""

    adapter_id: str
    provider_id: str
    name: str
    adapter_kind: str
    description: str
    activation_status: str = ActivationStatus.ACTIVATION_NOT_APPROVED.value
    allowed_scope: str = ""
    forbidden_scope: str = ""
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "adapter_kind", _value(self.adapter_kind))
        object.__setattr__(self, "activation_status", _value(self.activation_status))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class AdapterCapability:
    """Metadata-only adapter capability descriptor."""

    capability_id: str
    adapter_id: str
    name: str
    description: str
    activation_status: str = ActivationStatus.ACTIVATION_NOT_APPROVED.value
    input_classes: Sequence[str] = field(default_factory=tuple)
    output_classes: Sequence[str] = field(default_factory=tuple)
    side_effects: Sequence[str] = field(default_factory=tuple)
    network_behavior: str = ""
    credential_behavior: str = ""
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "activation_status", _value(self.activation_status))
        object.__setattr__(self, "input_classes", _tuple_of_strings(self.input_classes))
        object.__setattr__(self, "output_classes", _tuple_of_strings(self.output_classes))
        object.__setattr__(self, "side_effects", _tuple_of_strings(self.side_effects))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


class ProviderAdapterLayer:
    """In-memory provider/adapter metadata layer only."""

    def __init__(self) -> None:
        self._providers: Dict[str, ProviderDescriptor] = {}
        self._adapters: Dict[str, AdapterDescriptor] = {}
        self._capabilities: Dict[str, AdapterCapability] = {}

    def register_provider(self, provider: ProviderDescriptor) -> ProviderDescriptor:
        errors = self.validate_provider(provider)
        if errors:
            raise ValueError("; ".join(errors))
        if provider.provider_id in self._providers:
            raise ValueError(f"duplicate provider_id: {provider.provider_id}")
        self._providers[provider.provider_id] = provider
        return provider

    def register_adapter(self, adapter: AdapterDescriptor) -> AdapterDescriptor:
        errors = self.validate_adapter(adapter)
        if isinstance(adapter, AdapterDescriptor) and adapter.provider_id not in self._providers:
            errors.append(f"provider_id is not registered: {adapter.provider_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if adapter.adapter_id in self._adapters:
            raise ValueError(f"duplicate adapter_id: {adapter.adapter_id}")
        self._adapters[adapter.adapter_id] = adapter
        return adapter

    def register_capability(self, capability: AdapterCapability) -> AdapterCapability:
        errors = self.validate_capability(capability)
        if isinstance(capability, AdapterCapability) and capability.adapter_id not in self._adapters:
            errors.append(f"adapter_id is not registered: {capability.adapter_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if capability.capability_id in self._capabilities:
            raise ValueError(f"duplicate capability_id: {capability.capability_id}")
        self._capabilities[capability.capability_id] = capability
        return capability

    def get_provider(self, provider_id: str) -> Optional[ProviderDescriptor]:
        return self._providers.get(provider_id)

    def get_adapter(self, adapter_id: str) -> Optional[AdapterDescriptor]:
        return self._adapters.get(adapter_id)

    def get_capability(self, capability_id: str) -> Optional[AdapterCapability]:
        return self._capabilities.get(capability_id)

    def list_providers(self) -> List[ProviderDescriptor]:
        return list(self._providers.values())

    def list_adapters(self) -> List[AdapterDescriptor]:
        return list(self._adapters.values())

    def list_capabilities(self) -> List[AdapterCapability]:
        return list(self._capabilities.values())

    def list_adapters_by_provider(self, provider_id: str) -> List[AdapterDescriptor]:
        return [adapter for adapter in self._adapters.values() if adapter.provider_id == provider_id]

    def list_capabilities_by_adapter(self, adapter_id: str) -> List[AdapterCapability]:
        return [capability for capability in self._capabilities.values() if capability.adapter_id == adapter_id]

    @staticmethod
    def validate_provider(provider: ProviderDescriptor) -> List[str]:
        if not isinstance(provider, ProviderDescriptor):
            return ["provider must be a ProviderDescriptor"]
        errors: List[str] = []
        required_text = {
            "provider_id": provider.provider_id,
            "name": provider.name,
            "provider_kind": provider.provider_kind,
            "description": provider.description,
            "activation_status": provider.activation_status,
            "data_exposure_risk": provider.data_exposure_risk,
            "created_at": provider.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("provider_kind", provider.provider_kind, ProviderKind))
        errors.extend(_validate_allowed("activation_status", provider.activation_status, ActivationStatus))
        errors.extend(_validate_bool("auth_required", provider.auth_required))
        errors.extend(_validate_bool("network_required", provider.network_required))
        errors.extend(_validate_bool("review_required", provider.review_required))
        errors.extend(_validate_string_sequence("credential_refs", provider.credential_refs))
        errors.extend(_validate_string_sequence("evidence_refs", provider.evidence_refs))
        errors.extend(_validate_string_sequence("limitations", provider.limitations))
        errors.extend(_validate_string_sequence("blockers", provider.blockers))
        errors.extend(_validate_metadata_refs("credential_refs", provider.credential_refs))
        errors.extend(_validate_metadata_refs("evidence_refs", provider.evidence_refs))
        errors.extend(_validate_activation_posture(provider.activation_status, provider.review_required))
        if provider.auth_required:
            errors.extend(_validate_required_review_blocker("auth_required", provider.review_required, provider.blockers))
        if provider.network_required:
            errors.extend(
                _validate_required_review_blocker(
                    "network_required", provider.review_required, provider.blockers
                )
            )
        return errors

    @staticmethod
    def validate_adapter(adapter: AdapterDescriptor) -> List[str]:
        if not isinstance(adapter, AdapterDescriptor):
            return ["adapter must be an AdapterDescriptor"]
        errors: List[str] = []
        required_text = {
            "adapter_id": adapter.adapter_id,
            "provider_id": adapter.provider_id,
            "name": adapter.name,
            "adapter_kind": adapter.adapter_kind,
            "description": adapter.description,
            "activation_status": adapter.activation_status,
            "allowed_scope": adapter.allowed_scope,
            "forbidden_scope": adapter.forbidden_scope,
            "created_at": adapter.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("adapter_kind", adapter.adapter_kind, AdapterKind))
        errors.extend(_validate_allowed("activation_status", adapter.activation_status, ActivationStatus))
        errors.extend(_validate_bool("review_required", adapter.review_required))
        errors.extend(_validate_string_sequence("evidence_refs", adapter.evidence_refs))
        errors.extend(_validate_string_sequence("limitations", adapter.limitations))
        errors.extend(_validate_string_sequence("blockers", adapter.blockers))
        errors.extend(_validate_metadata_refs("evidence_refs", adapter.evidence_refs))
        errors.extend(_validate_activation_posture(adapter.activation_status, adapter.review_required))
        return errors

    @staticmethod
    def validate_capability(capability: AdapterCapability) -> List[str]:
        if not isinstance(capability, AdapterCapability):
            return ["capability must be an AdapterCapability"]
        errors: List[str] = []
        required_text = {
            "capability_id": capability.capability_id,
            "adapter_id": capability.adapter_id,
            "name": capability.name,
            "description": capability.description,
            "activation_status": capability.activation_status,
            "network_behavior": capability.network_behavior,
            "credential_behavior": capability.credential_behavior,
            "created_at": capability.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("activation_status", capability.activation_status, ActivationStatus))
        errors.extend(_validate_bool("review_required", capability.review_required))
        errors.extend(_validate_string_sequence("input_classes", capability.input_classes))
        errors.extend(_validate_string_sequence("output_classes", capability.output_classes))
        errors.extend(_validate_string_sequence("side_effects", capability.side_effects))
        errors.extend(_validate_string_sequence("evidence_refs", capability.evidence_refs))
        errors.extend(_validate_string_sequence("limitations", capability.limitations))
        errors.extend(_validate_string_sequence("blockers", capability.blockers))
        errors.extend(_validate_metadata_refs("evidence_refs", capability.evidence_refs))
        errors.extend(_validate_activation_posture(capability.activation_status, capability.review_required))
        if _has_declared_side_effects(capability.side_effects):
            errors.extend(
                _validate_required_review_blocker(
                    "side_effects", capability.review_required, capability.blockers
                )
            )
        return errors


def _validate_required_text(values: Dict[str, object]) -> List[str]:
    errors: List[str] = []
    for field_name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name} is required")
    return errors


def _validate_allowed(field_name: str, value: object, enum_type: object) -> List[str]:
    if not isinstance(value, str):
        return []
    allowed = {member.value for member in enum_type}
    if value not in allowed:
        return [f"{field_name} must be one of: {', '.join(sorted(allowed))}"]
    return []


def _validate_bool(field_name: str, value: object) -> List[str]:
    if not isinstance(value, bool):
        return [f"{field_name} must be a boolean"]
    return []


def _validate_string_sequence(field_name: str, values: object) -> List[str]:
    if isinstance(values, str):
        return [f"{field_name} must be a sequence of strings"]
    try:
        iterator = iter(values)
    except TypeError:
        return [f"{field_name} must be a sequence of strings"]
    errors: List[str] = []
    for index, value in enumerate(iterator):
        if not isinstance(value, str):
            errors.append(f"{field_name}[{index}] must be a string")
    return errors


def _validate_metadata_refs(field_name: str, values: object) -> List[str]:
    errors: List[str] = []
    for value in _iter_strings(values):
        if "\n" in value or "\r" in value:
            errors.append(f"{field_name} must be references or IDs, not raw contents")
    return errors


def _validate_activation_posture(status: object, review_required: object) -> List[str]:
    errors: List[str] = []
    if status == ActivationStatus.METADATA_ONLY.value and review_required is False:
        errors.append("metadata_only is not provider activation or adapter activation")
    if status != ActivationStatus.ACTIVATION_NOT_APPROVED.value and review_required is False:
        errors.append("activation status requires review")
    return errors


def _validate_required_review_blocker(
    trigger_name: str, review_required: object, blockers: object
) -> List[str]:
    errors: List[str] = []
    if review_required is not True:
        errors.append(f"{trigger_name} requires review")
    if not _iter_strings(blockers):
        errors.append(f"{trigger_name} requires retained blockers")
    return errors


def _has_declared_side_effects(values: object) -> bool:
    return any(value.strip().lower() not in {"", "none", "metadata_only"} for value in _iter_strings(values))


def _iter_strings(values: object) -> List[str]:
    if isinstance(values, str):
        return []
    try:
        return [value for value in values if isinstance(value, str)]
    except TypeError:
        return []
