"""I-05 minimal agent runtime boundary metadata layer.

This module models agent descriptors, capability descriptors, task envelopes,
and handoff records in memory only. It does not run agents, schedule work,
execute tasks, execute handoffs, execute tools, call providers, call APIs,
authenticate, inspect credentials, activate MCP, approve permissions, or imply
readiness. Agent registration is not agent activation. Task envelope creation
is not task execution. Handoff record creation is not handoff execution.
Validation evaluates; governance decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class AgentKind(str, Enum):
    """Declared agent kinds for metadata records."""

    GOVERNANCE_AGENT = "governance_agent"
    VALIDATION_AGENT = "validation_agent"
    SECURITY_AGENT = "security_agent"
    CONTEXT_AGENT = "context_agent"
    PROVIDER_ADAPTER_AGENT = "provider_adapter_agent"
    TOOL_BOUNDARY_AGENT = "tool_boundary_agent"
    PRODUCT_AGENT = "product_agent"
    IMPLEMENTATION_AGENT = "implementation_agent"
    REVIEW_AGENT = "review_agent"
    ORCHESTRATION_AGENT = "orchestration_agent"
    UNKNOWN = "unknown"


class AgentActivationStatus(str, Enum):
    """Activation posture for metadata-only agent records."""

    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    ACTIVATION_NOT_APPROVED = "activation_not_approved"
    REJECTED_FOR_SCOPE = "rejected_for_scope"


class AgentTaskStatus(str, Enum):
    """Task envelope statuses for metadata-only records."""

    DRAFT = "draft"
    PROPOSED_FOR_REVIEW = "proposed_for_review"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    RECORDED_METADATA_ONLY = "recorded_metadata_only"


class AgentHandoffStatus(str, Enum):
    """Handoff statuses for metadata-only records."""

    DRAFT = "draft"
    PROPOSED_FOR_REVIEW = "proposed_for_review"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    RECORDED_METADATA_ONLY = "recorded_metadata_only"


AGENT_REGISTRATION_IS_NOT_AGENT_ACTIVATION = "agent registration is not agent activation"
TASK_ENVELOPE_CREATION_IS_NOT_TASK_EXECUTION = (
    "task envelope creation is not task execution"
)
HANDOFF_RECORD_CREATION_IS_NOT_HANDOFF_EXECUTION = (
    "handoff record creation is not handoff execution"
)
CAPABILITY_REGISTRATION_IS_NOT_TOOL_PERMISSION = (
    "capability registration is not tool permission"
)
PROVIDER_ADAPTER_REFS_ARE_METADATA_ONLY = "provider/adapter refs are metadata only"
TOOL_REFS_ARE_METADATA_ONLY = "tool refs are metadata only"
EVIDENCE_REFS_ARE_METADATA_ONLY = "evidence_refs are metadata references only"


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
class AgentDescriptor:
    """Metadata-only agent descriptor."""

    agent_id: str
    name: str
    agent_kind: str
    description: str
    activation_status: str = AgentActivationStatus.ACTIVATION_NOT_APPROVED.value
    allowed_scope: str = ""
    forbidden_scope: str = ""
    provider_refs: Sequence[str] = field(default_factory=tuple)
    adapter_refs: Sequence[str] = field(default_factory=tuple)
    tool_refs: Sequence[str] = field(default_factory=tuple)
    context_pack_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "agent_kind", _value(self.agent_kind))
        object.__setattr__(self, "activation_status", _value(self.activation_status))
        object.__setattr__(self, "provider_refs", _tuple_of_strings(self.provider_refs))
        object.__setattr__(self, "adapter_refs", _tuple_of_strings(self.adapter_refs))
        object.__setattr__(self, "tool_refs", _tuple_of_strings(self.tool_refs))
        object.__setattr__(self, "context_pack_refs", _tuple_of_strings(self.context_pack_refs))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class AgentCapabilityDescriptor:
    """Metadata-only agent capability descriptor."""

    capability_id: str
    agent_id: str
    name: str
    description: str
    activation_status: str = AgentActivationStatus.ACTIVATION_NOT_APPROVED.value
    input_classes: Sequence[str] = field(default_factory=tuple)
    output_classes: Sequence[str] = field(default_factory=tuple)
    side_effects: Sequence[str] = field(default_factory=tuple)
    tool_required: bool = False
    provider_required: bool = False
    context_required: bool = False
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
class AgentTaskEnvelope:
    """Metadata-only task envelope; not task execution."""

    task_id: str
    agent_id: str
    target_id: str
    intent: str
    status: str = AgentTaskStatus.DRAFT.value
    context_pack_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_decision_refs: Sequence[str] = field(default_factory=tuple)
    provider_adapter_refs: Sequence[str] = field(default_factory=tuple)
    tool_refs: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    created_by: str = ""
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "context_pack_refs", _tuple_of_strings(self.context_pack_refs))
        object.__setattr__(self, "validation_refs", _tuple_of_strings(self.validation_refs))
        object.__setattr__(self, "security_decision_refs", _tuple_of_strings(self.security_decision_refs))
        object.__setattr__(self, "provider_adapter_refs", _tuple_of_strings(self.provider_adapter_refs))
        object.__setattr__(self, "tool_refs", _tuple_of_strings(self.tool_refs))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))


@dataclass(frozen=True)
class AgentHandoffRecord:
    """Metadata-only handoff record; not handoff execution."""

    handoff_id: str
    from_agent_id: str
    to_agent_id: str
    task_id: str
    reason: str
    status: str = AgentHandoffStatus.DRAFT.value
    context_pack_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "context_pack_refs", _tuple_of_strings(self.context_pack_refs))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))


class AgentRuntimeBoundary:
    """In-memory agent runtime boundary metadata layer only."""

    def __init__(self) -> None:
        self._agents: Dict[str, AgentDescriptor] = {}
        self._capabilities: Dict[str, AgentCapabilityDescriptor] = {}
        self._tasks: Dict[str, AgentTaskEnvelope] = {}
        self._handoffs: Dict[str, AgentHandoffRecord] = {}

    def register_agent(self, agent: AgentDescriptor) -> AgentDescriptor:
        errors = self.validate_agent(agent)
        if errors:
            raise ValueError("; ".join(errors))
        if agent.agent_id in self._agents:
            raise ValueError(f"duplicate agent_id: {agent.agent_id}")
        self._agents[agent.agent_id] = agent
        return agent

    def register_capability(self, capability: AgentCapabilityDescriptor) -> AgentCapabilityDescriptor:
        errors = self.validate_capability(capability)
        if isinstance(capability, AgentCapabilityDescriptor) and capability.agent_id not in self._agents:
            errors.append(f"agent_id is not registered: {capability.agent_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if capability.capability_id in self._capabilities:
            raise ValueError(f"duplicate capability_id: {capability.capability_id}")
        self._capabilities[capability.capability_id] = capability
        return capability

    def register_task_envelope(self, task: AgentTaskEnvelope) -> AgentTaskEnvelope:
        errors = self.validate_task_envelope(task)
        if isinstance(task, AgentTaskEnvelope) and task.agent_id not in self._agents:
            errors.append(f"agent_id is not registered: {task.agent_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if task.task_id in self._tasks:
            raise ValueError(f"duplicate task_id: {task.task_id}")
        self._tasks[task.task_id] = task
        return task

    def register_handoff_record(self, handoff: AgentHandoffRecord) -> AgentHandoffRecord:
        errors = self.validate_handoff_record(handoff)
        if isinstance(handoff, AgentHandoffRecord):
            if handoff.from_agent_id not in self._agents:
                errors.append(f"from_agent_id is not registered: {handoff.from_agent_id}")
            if handoff.to_agent_id not in self._agents:
                errors.append(f"to_agent_id is not registered: {handoff.to_agent_id}")
            if handoff.task_id not in self._tasks:
                errors.append(f"task_id is not registered: {handoff.task_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if handoff.handoff_id in self._handoffs:
            raise ValueError(f"duplicate handoff_id: {handoff.handoff_id}")
        self._handoffs[handoff.handoff_id] = handoff
        return handoff

    def get_agent(self, agent_id: str) -> Optional[AgentDescriptor]:
        return self._agents.get(agent_id)

    def get_capability(self, capability_id: str) -> Optional[AgentCapabilityDescriptor]:
        return self._capabilities.get(capability_id)

    def get_task_envelope(self, task_id: str) -> Optional[AgentTaskEnvelope]:
        return self._tasks.get(task_id)

    def get_handoff_record(self, handoff_id: str) -> Optional[AgentHandoffRecord]:
        return self._handoffs.get(handoff_id)

    def list_agents(self) -> List[AgentDescriptor]:
        return list(self._agents.values())

    def list_capabilities(self) -> List[AgentCapabilityDescriptor]:
        return list(self._capabilities.values())

    def list_task_envelopes(self) -> List[AgentTaskEnvelope]:
        return list(self._tasks.values())

    def list_handoff_records(self) -> List[AgentHandoffRecord]:
        return list(self._handoffs.values())

    def list_capabilities_by_agent(self, agent_id: str) -> List[AgentCapabilityDescriptor]:
        return [capability for capability in self._capabilities.values() if capability.agent_id == agent_id]

    def list_task_envelopes_by_agent(self, agent_id: str) -> List[AgentTaskEnvelope]:
        return [task for task in self._tasks.values() if task.agent_id == agent_id]

    def list_handoff_records_by_task(self, task_id: str) -> List[AgentHandoffRecord]:
        return [handoff for handoff in self._handoffs.values() if handoff.task_id == task_id]

    @staticmethod
    def validate_agent(agent: AgentDescriptor) -> List[str]:
        if not isinstance(agent, AgentDescriptor):
            return ["agent must be an AgentDescriptor"]
        errors: List[str] = []
        required_text = {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "agent_kind": agent.agent_kind,
            "description": agent.description,
            "activation_status": agent.activation_status,
            "allowed_scope": agent.allowed_scope,
            "forbidden_scope": agent.forbidden_scope,
            "created_at": agent.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("agent_kind", agent.agent_kind, AgentKind))
        errors.extend(_validate_allowed("activation_status", agent.activation_status, AgentActivationStatus))
        errors.extend(_validate_bool("review_required", agent.review_required))
        errors.extend(_validate_refs("provider_refs", agent.provider_refs))
        errors.extend(_validate_refs("adapter_refs", agent.adapter_refs))
        errors.extend(_validate_refs("tool_refs", agent.tool_refs))
        errors.extend(_validate_refs("context_pack_refs", agent.context_pack_refs))
        errors.extend(_validate_refs("evidence_refs", agent.evidence_refs))
        errors.extend(_validate_refs("limitations", agent.limitations))
        errors.extend(_validate_refs("blockers", agent.blockers))
        errors.extend(_validate_activation_posture(agent.activation_status, agent.review_required))
        if _has_any_refs(agent.provider_refs, agent.adapter_refs, agent.tool_refs):
            errors.extend(_validate_required_review_blocker("provider_adapter_or_tool_refs", agent.review_required, agent.blockers))
        if agent.agent_kind == AgentKind.ORCHESTRATION_AGENT.value:
            errors.extend(_validate_required_review_blocker("orchestration_agent", agent.review_required, agent.blockers))
        return errors

    @staticmethod
    def validate_capability(capability: AgentCapabilityDescriptor) -> List[str]:
        if not isinstance(capability, AgentCapabilityDescriptor):
            return ["capability must be an AgentCapabilityDescriptor"]
        errors: List[str] = []
        required_text = {
            "capability_id": capability.capability_id,
            "agent_id": capability.agent_id,
            "name": capability.name,
            "description": capability.description,
            "activation_status": capability.activation_status,
            "created_at": capability.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("activation_status", capability.activation_status, AgentActivationStatus))
        errors.extend(_validate_bool("tool_required", capability.tool_required))
        errors.extend(_validate_bool("provider_required", capability.provider_required))
        errors.extend(_validate_bool("context_required", capability.context_required))
        errors.extend(_validate_bool("review_required", capability.review_required))
        errors.extend(_validate_refs("input_classes", capability.input_classes))
        errors.extend(_validate_refs("output_classes", capability.output_classes))
        errors.extend(_validate_refs("side_effects", capability.side_effects))
        errors.extend(_validate_refs("evidence_refs", capability.evidence_refs))
        errors.extend(_validate_refs("limitations", capability.limitations))
        errors.extend(_validate_refs("blockers", capability.blockers))
        errors.extend(_validate_activation_posture(capability.activation_status, capability.review_required))
        if _has_declared_side_effects(capability.side_effects):
            errors.extend(_validate_required_review_blocker("side_effects", capability.review_required, capability.blockers))
        if capability.tool_required or capability.provider_required or capability.context_required:
            errors.extend(_validate_required_review_blocker("tool_provider_or_context_required", capability.review_required, capability.blockers))
        return errors

    @staticmethod
    def validate_task_envelope(task: AgentTaskEnvelope) -> List[str]:
        if not isinstance(task, AgentTaskEnvelope):
            return ["task must be an AgentTaskEnvelope"]
        errors: List[str] = []
        required_text = {
            "task_id": task.task_id,
            "agent_id": task.agent_id,
            "target_id": task.target_id,
            "intent": task.intent,
            "status": task.status,
            "created_by": task.created_by,
            "created_at": task.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("status", task.status, AgentTaskStatus))
        errors.extend(_validate_bool("review_required", task.review_required))
        errors.extend(_validate_refs("context_pack_refs", task.context_pack_refs))
        errors.extend(_validate_refs("validation_refs", task.validation_refs))
        errors.extend(_validate_refs("security_decision_refs", task.security_decision_refs))
        errors.extend(_validate_refs("provider_adapter_refs", task.provider_adapter_refs))
        errors.extend(_validate_refs("tool_refs", task.tool_refs))
        errors.extend(_validate_refs("blockers", task.blockers))
        errors.extend(_validate_refs("limitations", task.limitations))
        if task.status == AgentTaskStatus.RECORDED_METADATA_ONLY.value and task.review_required is False:
            errors.append("recorded_metadata_only is not task execution")
        if _has_any_refs(task.provider_adapter_refs, task.tool_refs):
            errors.extend(_validate_required_review_blocker("provider_adapter_or_tool_refs", task.review_required, task.blockers))
        return errors

    @staticmethod
    def validate_handoff_record(handoff: AgentHandoffRecord) -> List[str]:
        if not isinstance(handoff, AgentHandoffRecord):
            return ["handoff must be an AgentHandoffRecord"]
        errors: List[str] = []
        required_text = {
            "handoff_id": handoff.handoff_id,
            "from_agent_id": handoff.from_agent_id,
            "to_agent_id": handoff.to_agent_id,
            "task_id": handoff.task_id,
            "reason": handoff.reason,
            "status": handoff.status,
            "created_at": handoff.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("status", handoff.status, AgentHandoffStatus))
        errors.extend(_validate_bool("review_required", handoff.review_required))
        errors.extend(_validate_refs("context_pack_refs", handoff.context_pack_refs))
        errors.extend(_validate_refs("evidence_refs", handoff.evidence_refs))
        errors.extend(_validate_refs("blockers", handoff.blockers))
        errors.extend(_validate_refs("limitations", handoff.limitations))
        if handoff.status == AgentHandoffStatus.RECORDED_METADATA_ONLY.value and handoff.review_required is False:
            errors.append("recorded_metadata_only is not handoff execution")
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
    if status == AgentActivationStatus.METADATA_ONLY.value and review_required is False:
        errors.append("metadata_only is not agent activation")
    if status != AgentActivationStatus.ACTIVATION_NOT_APPROVED.value and review_required is False:
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
