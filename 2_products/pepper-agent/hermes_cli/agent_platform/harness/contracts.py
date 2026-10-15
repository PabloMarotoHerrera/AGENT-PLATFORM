"""Inert platform contracts. Validation checks claims, never grants permission.

All identifiers are opaque. References are not resolved here; in particular a
CURRENT claim and an ALLOW observation require fresh checks by future adapters.
There are no handlers, storage readers, policy evaluators or product imports.
"""

from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


def _version(value: object) -> int:
    if type(value) is not int or value != 1:
        raise ValueError("unsupported envelope schema version")
    return value


def _observational(value: object) -> bool:
    if value is not True:
        raise ValueError("envelope is strictly observational")
    return True


Identifier = Annotated[str, Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$", max_length=128)]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$", min_length=64, max_length=64)]
Version = Annotated[int, Field(ge=1, le=65535)]
SchemaVersion = Annotated[Literal[1], BeforeValidator(_version)]
Observational = Annotated[Literal[True], BeforeValidator(_observational)]


class _Contract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True,
                             validate_default=True, revalidate_instances="always")
    schema_version: SchemaVersion = 1


class Effect(str, Enum):
    OBSERVE = "OBSERVE"
    COMPUTE = "COMPUTE"
    WRITE_ARTIFACT = "WRITE_ARTIFACT"
    EXTERNAL_WRITE = "EXTERNAL_WRITE"
    PHYSICAL_CONTROL = "PHYSICAL_CONTROL"


class ContinuationKind(str, Enum):
    EXECUTABLE_CAPABILITY = "EXECUTABLE_CAPABILITY"
    HUMAN_DECISION = "HUMAN_DECISION"
    OBSERVATION = "OBSERVATION"
    EXTERNAL_REMEDIATION = "EXTERNAL_REMEDIATION"
    SAFE_STOP = "SAFE_STOP"


class AuthorityCurrentness(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    SUPERSEDED = "SUPERSEDED"
    UNSUPPORTED = "UNSUPPORTED"
    CONFLICT = "CONFLICT"


class StateSupport(str, Enum):
    SUPPORTED = "SUPPORTED"
    UNKNOWN = "UNKNOWN"
    UNSUPPORTED = "UNSUPPORTED"


class DecisionOutcome(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    WAIT = "WAIT"
    SAFE_STOP = "SAFE_STOP"


class ResultOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    DENIED = "DENIED"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


class EffectStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_APPLIED = "NOT_APPLIED"
    UNKNOWN = "UNKNOWN"


class ContractRef(_Contract):
    contract_id: Identifier
    version: Version


class ContentRef(_Contract):
    content_id: Identifier
    sha256: Digest


class ActorRef(_Contract):
    actor_id: Identifier
    trust_model: Literal["trusted_local_operator"] = "trusted_local_operator"


class Scope(_Contract):
    project_id: Identifier
    workflow_id: Identifier
    resource_ids: Annotated[tuple[Identifier, ...], Field(min_length=1, max_length=32)]

    @model_validator(mode="after")
    def _resources(self) -> "Scope":
        if len(set(self.resource_ids)) != len(self.resource_ids):
            raise ValueError("duplicate resources")
        # Scope is a set; other contract sequences retain declared order.
        object.__setattr__(self, "resource_ids", tuple(sorted(self.resource_ids)))
        return self


class CapabilityDescriptor(_Contract):
    capability: ContractRef
    input_schema: ContractRef
    output_schema: ContractRef
    effect: Effect
    required_authority_kinds: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    evidence_contract: ContractRef
    execution_adapter: ContractRef
    recovery_policy: ContractRef | None = None


class TransitionDescriptor(_Contract):
    transition: ContractRef
    source_requirement: ContractRef
    capability: ContractRef
    prerequisites: Annotated[tuple[ContractRef, ...], Field(max_length=32)]
    required_authority_kinds: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    effect: Effect
    target_rule: ContractRef
    failure_code: Identifier
    conflict_code: Identifier
    continuation_rule: ContractRef


class StateDimension(_Contract):
    definition: ContractRef
    value: Identifier
    support: StateSupport


class WorkflowState(_Contract):
    publication: StateDimension
    execution: StateDimension
    validation: StateDimension
    review: StateDimension
    completion: StateDimension
    authority_currentness: AuthorityCurrentness


class Continuation(_Contract):
    continuation_id: Identifier
    scope: Scope
    actor: ActorRef
    kind: ContinuationKind
    reason_code: Identifier
    policy: ContractRef
    capability: ContractRef | None = None
    decision_target: ContractRef | None = None

    @model_validator(mode="after")
    def _kind(self) -> "Continuation":
        executable = self.kind == ContinuationKind.EXECUTABLE_CAPABILITY
        if executable != (self.capability is not None):
            raise ValueError("only executable offers carry a capability reference")
        human = self.kind == ContinuationKind.HUMAN_DECISION
        if human != (self.decision_target is not None):
            raise ValueError("only human decisions carry a decision target")
        return self


class AuthorityReference(_Contract):
    authority_id: Identifier
    kind: Identifier
    issuer: ActorRef
    subject: ActorRef
    scope: Scope
    policy: ContractRef
    record: ContentRef
    dependencies: Annotated[tuple[ContentRef, ...], Field(max_length=32)]
    currentness: AuthorityCurrentness = AuthorityCurrentness.UNVERIFIED
    superseded_by: ContentRef | None = None

    @model_validator(mode="after")
    def _supersession(self) -> "AuthorityReference":
        if (self.currentness == AuthorityCurrentness.SUPERSEDED) != (self.superseded_by is not None):
            raise ValueError("superseded authority requires an explicit successor")
        return self


def _bindings(scope: Scope, actor: ActorRef, authorities: tuple[AuthorityReference, ...]) -> None:
    if len({a.authority_id for a in authorities}) != len(authorities):
        raise ValueError("duplicate authority identity")
    for authority in authorities:
        if authority.scope != scope or authority.subject != actor:
            raise ValueError("authority scope/subject mismatch")


class AdmissibilityDecision(_Contract):
    """A recorded observation, including ALLOW; never an execution credential."""

    decision_id: Identifier
    scope: Scope
    actor: ActorRef
    capability: ContractRef
    transition: ContractRef | None = None
    outcome: DecisionOutcome
    reason_code: Identifier
    policy: ContractRef
    required_authority_kinds: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    current_authorities: Annotated[tuple[AuthorityReference, ...], Field(max_length=32)]
    expected_authority_version: Identifier | None = None
    prerequisites: Annotated[tuple[ContentRef, ...], Field(max_length=32)]
    effect: Effect
    observational: Observational = True

    @model_validator(mode="after")
    def _claims(self) -> "AdmissibilityDecision":
        _bindings(self.scope, self.actor, self.current_authorities)
        if self.outcome == DecisionOutcome.ALLOW:
            if self.expected_authority_version is None:
                raise ValueError("allow observation requires an authority version")
            if any(a.currentness != AuthorityCurrentness.CURRENT for a in self.current_authorities):
                raise ValueError("allow observation contradicts authority currentness claims")
            if not set(self.required_authority_kinds).issubset({a.kind for a in self.current_authorities}):
                raise ValueError("missing required authority kind")
        return self


class ExecutionRequest(_Contract):
    """Data proposed for future preflight; construction does not execute or authorize."""

    operation_id: Identifier
    capability: ContractRef
    scope: Scope
    actor: ActorRef
    authorities: Annotated[tuple[AuthorityReference, ...], Field(min_length=1, max_length=32)]
    input: ContentRef
    implementation: ContentRef
    effect: Effect
    admissibility_observation: ContentRef
    expected_authority_version: Identifier
    idempotency_key: Identifier | None = None
    replay_ref: ContentRef | None = None

    @model_validator(mode="after")
    def _claims(self) -> "ExecutionRequest":
        _bindings(self.scope, self.actor, self.authorities)
        if any(a.currentness != AuthorityCurrentness.CURRENT for a in self.authorities):
            raise ValueError("request requires fresh-currentness claims, not historical authority")
        if self.replay_ref is not None and self.idempotency_key is None:
            raise ValueError("replay reference requires idempotency key")
        return self


class EvidenceReference(_Contract):
    evidence_id: Identifier
    evidence_type: Identifier
    sha256: Digest
    producer_operation_id: Identifier
    producer_capability: ContractRef
    producer_actor: ActorRef
    scope: Scope
    input: ContentRef
    storage_locator: Annotated[str, Field(min_length=1, max_length=512, pattern=r"^[^\x00-\x1f\x7f]+$")]
    integrity: Literal["unverified", "verified", "mismatch"]
    retention: Literal["unspecified", "retained", "expired"]


class ExecutionResult(_Contract):
    operation_id: Identifier
    capability: ContractRef
    scope: Scope
    actor: ActorRef
    request: ContentRef
    input: ContentRef
    outcome: ResultOutcome
    effect_status: EffectStatus
    reason_code: Identifier
    output: ContentRef | None = None
    evidence: Annotated[tuple[EvidenceReference, ...], Field(max_length=32)]
    replay_ref: ContentRef | None = None

    @model_validator(mode="after")
    def _result(self) -> "ExecutionResult":
        if self.outcome == ResultOutcome.UNKNOWN and self.effect_status != EffectStatus.UNKNOWN:
            raise ValueError("unknown outcome cannot confirm effects")
        if self.outcome == ResultOutcome.SUCCESS:
            if self.effect_status != EffectStatus.CONFIRMED or self.output is None or not self.evidence:
                raise ValueError("success requires confirmed output and evidence")
        if self.outcome == ResultOutcome.DENIED and self.effect_status != EffectStatus.NOT_APPLIED:
            raise ValueError("denied request cannot have applied effects")
        for evidence in self.evidence:
            if (evidence.scope != self.scope or evidence.producer_actor != self.actor
                    or evidence.producer_operation_id != self.operation_id
                    or evidence.producer_capability != self.capability or evidence.input != self.input):
                raise ValueError("evidence producer/input/scope mismatch")
        return self


class WorkflowProjection(_Contract):
    projection_id: Identifier
    scope: Scope
    actor: ActorRef
    observed_authority_version: Identifier
    observed_state_version: Identifier
    state: WorkflowState
    continuations: Annotated[tuple[Continuation, ...], Field(max_length=32)]
    pending_human_decisions: Annotated[tuple[Continuation, ...], Field(max_length=32)]
    wait_conditions: Annotated[tuple[ContractRef, ...], Field(max_length=32)]
    safe_stops: Annotated[tuple[Continuation, ...], Field(max_length=32)]
    diagnostics: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    observational: Observational = True

    @model_validator(mode="after")
    def _offers(self) -> "WorkflowProjection":
        offers = self.continuations + self.pending_human_decisions + self.safe_stops
        if len({o.continuation_id for o in offers}) != len(offers):
            raise ValueError("duplicate continuation identity")
        if any(o.scope != self.scope or o.actor != self.actor for o in offers):
            raise ValueError("continuation scope/actor mismatch")
        if any(o.kind != ContinuationKind.HUMAN_DECISION for o in self.pending_human_decisions):
            raise ValueError("pending human decisions require human-decision offers")
        if any(o.kind != ContinuationKind.SAFE_STOP for o in self.safe_stops):
            raise ValueError("safe stops require safe-stop offers")
        return self
