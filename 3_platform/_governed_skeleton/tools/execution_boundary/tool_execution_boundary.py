"""I-06 minimal tool execution boundary metadata layer.

This module models tool descriptors, capability descriptors, execution
requests, and execution decisions in memory only. It does not execute tools,
run shell commands, spawn processes, read or write files, call providers, call
APIs, use network, authenticate, inspect credentials, activate MCP, approve
permissions, or imply readiness. Tool registration is not tool activation.
Execution request creation is not execution approval. Execution decision
metadata is not execution authorization. Validation evaluates; governance
decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class ToolKind(str, Enum):
    """Declared tool kinds for metadata records."""

    METADATA_TOOL = "metadata_tool"
    VALIDATION_TOOL = "validation_tool"
    SECURITY_TOOL = "security_tool"
    CONTEXT_TOOL = "context_tool"
    AGENT_METADATA_TOOL = "agent_metadata_tool"
    PROVIDER_ADAPTER_METADATA_TOOL = "provider_adapter_metadata_tool"
    SHELL_TOOL = "shell_tool"
    FILESYSTEM_TOOL = "filesystem_tool"
    GIT_TOOL = "git_tool"
    PACKAGE_MANAGER_TOOL = "package_manager_tool"
    BUILD_TOOL = "build_tool"
    TEST_RUNNER_TOOL = "test_runner_tool"
    NETWORK_TOOL = "network_tool"
    PROVIDER_API_TOOL = "provider_api_tool"
    MCP_TOOL = "mcp_tool"
    PRODUCT_TOOL = "product_tool"
    SIMULATION_TOOL = "simulation_tool"
    UNKNOWN = "unknown"


class ToolActivationStatus(str, Enum):
    """Activation posture for metadata-only tool records."""

    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    ACTIVATION_NOT_APPROVED = "activation_not_approved"
    REJECTED_FOR_SCOPE = "rejected_for_scope"


class ToolRiskLevel(str, Enum):
    """Declared risk levels for tool execution metadata."""

    METADATA_ONLY = "metadata_only"
    GOVERNANCE_METADATA = "governance_metadata"
    LOCAL_ONLY_RISK = "local_only_risk"
    FILESYSTEM_RISK = "filesystem_risk"
    SHELL_RISK = "shell_risk"
    NETWORK_RISK = "network_risk"
    CREDENTIAL_RISK = "credential_risk"
    PROVIDER_RISK = "provider_risk"
    MCP_RISK = "mcp_risk"
    DEPENDENCY_RISK = "dependency_risk"
    PRODUCT_RISK = "product_risk"
    DESTRUCTIVE_RISK = "destructive_risk"
    UNKNOWN = "unknown"


class ToolExecutionRequestStatus(str, Enum):
    """Request statuses for metadata-only execution requests."""

    DRAFT = "draft"
    PROPOSED_FOR_REVIEW = "proposed_for_review"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    RECORDED_METADATA_ONLY = "recorded_metadata_only"


class ToolExecutionDecisionStatus(str, Enum):
    """Decision statuses for metadata-only execution decisions."""

    METADATA_RECORDED_ONLY = "metadata_recorded_only"
    EXECUTION_NOT_APPROVED = "execution_not_approved"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"


TOOL_REGISTRATION_IS_NOT_TOOL_ACTIVATION = "tool registration is not tool activation"
CAPABILITY_REGISTRATION_IS_NOT_TOOL_PERMISSION = (
    "capability registration is not tool permission"
)
EXECUTION_REQUEST_CREATION_IS_NOT_EXECUTION_APPROVAL = (
    "execution request creation is not execution approval"
)
EXECUTION_DECISION_METADATA_IS_NOT_EXECUTION_AUTHORIZATION = (
    "execution decision metadata is not execution authorization"
)
PROVIDER_ADAPTER_MCP_REFS_ARE_METADATA_ONLY = (
    "provider/adapter/MCP refs are metadata only"
)
EVIDENCE_REFS_ARE_METADATA_ONLY = "evidence_refs are metadata references only"

RISKY_TOOL_KINDS = {
    ToolKind.SHELL_TOOL.value,
    ToolKind.FILESYSTEM_TOOL.value,
    ToolKind.GIT_TOOL.value,
    ToolKind.PACKAGE_MANAGER_TOOL.value,
    ToolKind.BUILD_TOOL.value,
    ToolKind.TEST_RUNNER_TOOL.value,
    ToolKind.NETWORK_TOOL.value,
    ToolKind.PROVIDER_API_TOOL.value,
    ToolKind.MCP_TOOL.value,
    ToolKind.PRODUCT_TOOL.value,
    ToolKind.SIMULATION_TOOL.value,
    ToolKind.UNKNOWN.value,
}

LOW_RISK_LEVELS = {
    ToolRiskLevel.METADATA_ONLY.value,
    ToolRiskLevel.GOVERNANCE_METADATA.value,
}


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
class ToolDescriptor:
    """Metadata-only tool descriptor."""

    tool_id: str
    name: str
    tool_kind: str
    description: str
    activation_status: str = ToolActivationStatus.ACTIVATION_NOT_APPROVED.value
    allowed_scope: str = ""
    forbidden_scope: str = ""
    side_effects: Sequence[str] = field(default_factory=tuple)
    filesystem_required: bool = False
    shell_required: bool = False
    network_required: bool = False
    credential_required: bool = False
    provider_refs: Sequence[str] = field(default_factory=tuple)
    adapter_refs: Sequence[str] = field(default_factory=tuple)
    mcp_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "tool_kind", _value(self.tool_kind))
        object.__setattr__(self, "activation_status", _value(self.activation_status))
        object.__setattr__(self, "side_effects", _tuple_of_strings(self.side_effects))
        object.__setattr__(self, "provider_refs", _tuple_of_strings(self.provider_refs))
        object.__setattr__(self, "adapter_refs", _tuple_of_strings(self.adapter_refs))
        object.__setattr__(self, "mcp_refs", _tuple_of_strings(self.mcp_refs))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class ToolCapabilityDescriptor:
    """Metadata-only tool capability descriptor."""

    capability_id: str
    tool_id: str
    name: str
    description: str
    activation_status: str = ToolActivationStatus.ACTIVATION_NOT_APPROVED.value
    input_classes: Sequence[str] = field(default_factory=tuple)
    output_classes: Sequence[str] = field(default_factory=tuple)
    side_effects: Sequence[str] = field(default_factory=tuple)
    filesystem_behavior: str = ""
    shell_behavior: str = ""
    network_behavior: str = ""
    credential_behavior: str = ""
    provider_behavior: str = ""
    mcp_behavior: str = ""
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


@dataclass(frozen=True)
class ToolExecutionRequest:
    """Metadata-only tool execution request; not execution approval."""

    request_id: str
    tool_id: str
    capability_id: str
    requested_by: str
    target_id: str
    intent: str
    input_summary: str
    risk_level: str
    status: str = ToolExecutionRequestStatus.DRAFT.value
    context_pack_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_decision_refs: Sequence[str] = field(default_factory=tuple)
    agent_task_refs: Sequence[str] = field(default_factory=tuple)
    provider_adapter_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "risk_level", _value(self.risk_level))
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "context_pack_refs", _tuple_of_strings(self.context_pack_refs))
        object.__setattr__(self, "validation_refs", _tuple_of_strings(self.validation_refs))
        object.__setattr__(self, "security_decision_refs", _tuple_of_strings(self.security_decision_refs))
        object.__setattr__(self, "agent_task_refs", _tuple_of_strings(self.agent_task_refs))
        object.__setattr__(self, "provider_adapter_refs", _tuple_of_strings(self.provider_adapter_refs))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class ToolExecutionDecision:
    """Metadata-only tool execution decision; not execution authorization."""

    decision_id: str
    request_id: str
    status: str = ToolExecutionDecisionStatus.EXECUTION_NOT_APPROVED.value
    reasons: Sequence[str] = field(default_factory=tuple)
    risk_level: str = ToolRiskLevel.UNKNOWN.value
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    created_by: str = ""
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "risk_level", _value(self.risk_level))
        object.__setattr__(self, "reasons", _tuple_of_strings(self.reasons))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))


class ToolExecutionBoundary:
    """In-memory tool execution boundary metadata layer only."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDescriptor] = {}
        self._capabilities: Dict[str, ToolCapabilityDescriptor] = {}
        self._requests: Dict[str, ToolExecutionRequest] = {}
        self._decisions: Dict[str, ToolExecutionDecision] = {}

    def register_tool(self, tool: ToolDescriptor) -> ToolDescriptor:
        errors = self.validate_tool(tool)
        if errors:
            raise ValueError("; ".join(errors))
        if tool.tool_id in self._tools:
            raise ValueError(f"duplicate tool_id: {tool.tool_id}")
        self._tools[tool.tool_id] = tool
        return tool

    def register_capability(self, capability: ToolCapabilityDescriptor) -> ToolCapabilityDescriptor:
        errors = self.validate_capability(capability)
        if isinstance(capability, ToolCapabilityDescriptor) and capability.tool_id not in self._tools:
            errors.append(f"tool_id is not registered: {capability.tool_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if capability.capability_id in self._capabilities:
            raise ValueError(f"duplicate capability_id: {capability.capability_id}")
        self._capabilities[capability.capability_id] = capability
        return capability

    def register_execution_request(self, request: ToolExecutionRequest) -> ToolExecutionRequest:
        errors = self.validate_execution_request(request)
        if isinstance(request, ToolExecutionRequest):
            if request.tool_id not in self._tools:
                errors.append(f"tool_id is not registered: {request.tool_id}")
            if request.capability_id not in self._capabilities:
                errors.append(f"capability_id is not registered: {request.capability_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if request.request_id in self._requests:
            raise ValueError(f"duplicate request_id: {request.request_id}")
        self._requests[request.request_id] = request
        return request

    def register_execution_decision(self, decision: ToolExecutionDecision) -> ToolExecutionDecision:
        errors = self.validate_execution_decision(decision)
        if isinstance(decision, ToolExecutionDecision) and decision.request_id not in self._requests:
            errors.append(f"request_id is not registered: {decision.request_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if decision.decision_id in self._decisions:
            raise ValueError(f"duplicate decision_id: {decision.decision_id}")
        self._decisions[decision.decision_id] = decision
        return decision

    def get_tool(self, tool_id: str) -> Optional[ToolDescriptor]:
        return self._tools.get(tool_id)

    def get_capability(self, capability_id: str) -> Optional[ToolCapabilityDescriptor]:
        return self._capabilities.get(capability_id)

    def get_execution_request(self, request_id: str) -> Optional[ToolExecutionRequest]:
        return self._requests.get(request_id)

    def get_execution_decision(self, decision_id: str) -> Optional[ToolExecutionDecision]:
        return self._decisions.get(decision_id)

    def list_tools(self) -> List[ToolDescriptor]:
        return list(self._tools.values())

    def list_capabilities(self) -> List[ToolCapabilityDescriptor]:
        return list(self._capabilities.values())

    def list_execution_requests(self) -> List[ToolExecutionRequest]:
        return list(self._requests.values())

    def list_execution_decisions(self) -> List[ToolExecutionDecision]:
        return list(self._decisions.values())

    def list_capabilities_by_tool(self, tool_id: str) -> List[ToolCapabilityDescriptor]:
        return [capability for capability in self._capabilities.values() if capability.tool_id == tool_id]

    def list_execution_requests_by_tool(self, tool_id: str) -> List[ToolExecutionRequest]:
        return [request for request in self._requests.values() if request.tool_id == tool_id]

    def list_execution_decisions_by_request(self, request_id: str) -> List[ToolExecutionDecision]:
        return [decision for decision in self._decisions.values() if decision.request_id == request_id]

    @staticmethod
    def validate_tool(tool: ToolDescriptor) -> List[str]:
        if not isinstance(tool, ToolDescriptor):
            return ["tool must be a ToolDescriptor"]
        errors: List[str] = []
        required_text = {
            "tool_id": tool.tool_id,
            "name": tool.name,
            "tool_kind": tool.tool_kind,
            "description": tool.description,
            "activation_status": tool.activation_status,
            "allowed_scope": tool.allowed_scope,
            "forbidden_scope": tool.forbidden_scope,
            "created_at": tool.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("tool_kind", tool.tool_kind, ToolKind))
        errors.extend(_validate_allowed("activation_status", tool.activation_status, ToolActivationStatus))
        for field_name in (
            "filesystem_required",
            "shell_required",
            "network_required",
            "credential_required",
            "review_required",
        ):
            errors.extend(_validate_bool(field_name, getattr(tool, field_name)))
        for field_name in (
            "side_effects",
            "provider_refs",
            "adapter_refs",
            "mcp_refs",
            "evidence_refs",
            "limitations",
            "blockers",
        ):
            errors.extend(_validate_refs(field_name, getattr(tool, field_name)))
        errors.extend(_validate_activation_posture(tool.activation_status, tool.review_required))
        if _tool_requires_review(tool):
            errors.extend(_validate_required_review_blocker("tool_risk", tool.review_required, tool.blockers))
        return errors

    @staticmethod
    def validate_capability(capability: ToolCapabilityDescriptor) -> List[str]:
        if not isinstance(capability, ToolCapabilityDescriptor):
            return ["capability must be a ToolCapabilityDescriptor"]
        errors: List[str] = []
        required_text = {
            "capability_id": capability.capability_id,
            "tool_id": capability.tool_id,
            "name": capability.name,
            "description": capability.description,
            "activation_status": capability.activation_status,
            "filesystem_behavior": capability.filesystem_behavior,
            "shell_behavior": capability.shell_behavior,
            "network_behavior": capability.network_behavior,
            "credential_behavior": capability.credential_behavior,
            "provider_behavior": capability.provider_behavior,
            "mcp_behavior": capability.mcp_behavior,
            "created_at": capability.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("activation_status", capability.activation_status, ToolActivationStatus))
        errors.extend(_validate_bool("review_required", capability.review_required))
        for field_name in (
            "input_classes",
            "output_classes",
            "side_effects",
            "evidence_refs",
            "limitations",
            "blockers",
        ):
            errors.extend(_validate_refs(field_name, getattr(capability, field_name)))
        errors.extend(_validate_activation_posture(capability.activation_status, capability.review_required))
        if _capability_requires_review(capability):
            errors.extend(_validate_required_review_blocker("capability_risk", capability.review_required, capability.blockers))
        return errors

    @staticmethod
    def validate_execution_request(request: ToolExecutionRequest) -> List[str]:
        if not isinstance(request, ToolExecutionRequest):
            return ["request must be a ToolExecutionRequest"]
        errors: List[str] = []
        required_text = {
            "request_id": request.request_id,
            "tool_id": request.tool_id,
            "capability_id": request.capability_id,
            "requested_by": request.requested_by,
            "target_id": request.target_id,
            "intent": request.intent,
            "input_summary": request.input_summary,
            "risk_level": request.risk_level,
            "status": request.status,
            "created_at": request.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("risk_level", request.risk_level, ToolRiskLevel))
        errors.extend(_validate_allowed("status", request.status, ToolExecutionRequestStatus))
        errors.extend(_validate_bool("review_required", request.review_required))
        for field_name in (
            "context_pack_refs",
            "validation_refs",
            "security_decision_refs",
            "agent_task_refs",
            "provider_adapter_refs",
            "evidence_refs",
            "limitations",
            "blockers",
        ):
            errors.extend(_validate_refs(field_name, getattr(request, field_name)))
        errors.extend(_validate_input_summary(request.input_summary))
        if request.status == ToolExecutionRequestStatus.RECORDED_METADATA_ONLY.value and request.review_required is False:
            errors.append("recorded_metadata_only is not execution approval")
        if request.risk_level not in LOW_RISK_LEVELS:
            errors.extend(_validate_required_review_blocker("execution_request_risk", request.review_required, request.blockers))
        if _has_any_refs(request.provider_adapter_refs):
            errors.extend(_validate_required_review_blocker("provider_adapter_refs", request.review_required, request.blockers))
        return errors

    @staticmethod
    def validate_execution_decision(decision: ToolExecutionDecision) -> List[str]:
        if not isinstance(decision, ToolExecutionDecision):
            return ["decision must be a ToolExecutionDecision"]
        errors: List[str] = []
        required_text = {
            "decision_id": decision.decision_id,
            "request_id": decision.request_id,
            "status": decision.status,
            "risk_level": decision.risk_level,
            "created_by": decision.created_by,
            "created_at": decision.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("status", decision.status, ToolExecutionDecisionStatus))
        errors.extend(_validate_allowed("risk_level", decision.risk_level, ToolRiskLevel))
        errors.extend(_validate_bool("review_required", decision.review_required))
        for field_name in ("reasons", "limitations", "blockers", "evidence_refs"):
            errors.extend(_validate_refs(field_name, getattr(decision, field_name)))
        if decision.status == ToolExecutionDecisionStatus.METADATA_RECORDED_ONLY.value and decision.review_required is False:
            errors.append("metadata_recorded_only is not execution authorization")
        if decision.status != ToolExecutionDecisionStatus.EXECUTION_NOT_APPROVED.value and decision.review_required is False:
            errors.append("execution decision status requires review")
        if decision.risk_level not in LOW_RISK_LEVELS:
            errors.extend(_validate_required_review_blocker("execution_decision_risk", decision.review_required, decision.blockers))
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


def _validate_refs(field_name: str, values: object) -> List[str]:
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
        elif "\n" in value or "\r" in value:
            errors.append(f"{field_name} must be references or IDs, not raw contents")
    return errors


def _validate_activation_posture(status: object, review_required: object) -> List[str]:
    errors: List[str] = []
    if status == ToolActivationStatus.METADATA_ONLY.value and review_required is False:
        errors.append("metadata_only is not tool activation")
    if status != ToolActivationStatus.ACTIVATION_NOT_APPROVED.value and review_required is False:
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


def _validate_input_summary(value: object) -> List[str]:
    if not isinstance(value, str):
        return []
    if "\n" in value or "\r" in value:
        return ["input_summary must be a summary, not a raw payload"]
    return []


def _tool_requires_review(tool: ToolDescriptor) -> bool:
    return (
        tool.tool_kind in RISKY_TOOL_KINDS
        or tool.filesystem_required
        or tool.shell_required
        or tool.network_required
        or tool.credential_required
        or _has_any_refs(tool.provider_refs, tool.adapter_refs, tool.mcp_refs)
        or _has_declared_side_effects(tool.side_effects)
    )


def _capability_requires_review(capability: ToolCapabilityDescriptor) -> bool:
    behavior_values = (
        capability.filesystem_behavior,
        capability.shell_behavior,
        capability.network_behavior,
        capability.credential_behavior,
        capability.provider_behavior,
        capability.mcp_behavior,
    )
    return _has_declared_side_effects(capability.side_effects) or any(
        value.strip().lower() not in {"", "none", "metadata_only"}
        for value in behavior_values
        if isinstance(value, str)
    )


def _has_any_refs(*value_groups: object) -> bool:
    return any(_iter_strings(group) for group in value_groups)


def _has_declared_side_effects(values: object) -> bool:
    return any(value.strip().lower() not in {"", "none", "metadata_only"} for value in _iter_strings(values))


def _iter_strings(values: object) -> List[str]:
    if isinstance(values, str):
        return []
    try:
        return [value for value in values if isinstance(value, str)]
    except TypeError:
        return []
