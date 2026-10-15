"""Pure admission observations. No credential verification or execution boundary.

``qualification`` is injected ONLY by a future trusted owner, never deserialized
from model/tool arguments. Its issuer identity is a declared trust assumption,
not authentication. No such production owner is implemented here. In particular,
CURRENT claims and HAR-05 source verification alone cannot yield ALLOW.
"""

from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .catalog import CatalogSnapshot, LookupStatus
from .contracts import (
    ActorRef, AdmissibilityDecision, AuthorityCurrentness, AuthorityReference,
    CapabilityDescriptor, ContentRef, Continuation, ContinuationKind, ContractRef,
    DecisionOutcome, Effect, Identifier, Scope, StateDimension, StateSupport,
    TransitionDescriptor, WorkflowState, _Contract,
)
from .observation import CheckStatus, Observation, ObservationStatus
from .validation import canonical_json, parse_contract, sha256_bytes


class ConsentStatus(str, Enum):
    MISSING = "MISSING"
    PENDING = "PENDING"
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"
    CONFLICT = "CONFLICT"
    UNSUPPORTED = "UNSUPPORTED"


class StateRequirement(_Contract):
    dimension: Literal["publication", "execution", "validation", "review", "completion"]
    expected: StateDimension


class AdmissionPolicy(_Contract):
    """Requirements, not predicates. Opaque domain rules need qualified results.

    This policy does not implement an inspector merely by naming its reference.
    Unimplemented rules must be declared in unsupported_requirements.
    """

    policy: ContractRef
    capability: ContractRef
    transition: ContractRef | None = None
    catalog: ContentRef
    actor: ActorRef
    scope: Scope
    effect: Effect
    required_authority_kinds: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    prerequisites: Annotated[tuple[ContractRef, ...], Field(max_length=32)]
    states: Annotated[tuple[StateRequirement, ...], Field(max_length=5)] = ()
    consent_kind: Identifier | None = None
    missing_authority: Literal["WAIT", "SAFE_STOP"] = "SAFE_STOP"
    missing_prerequisite: Literal["WAIT", "SAFE_STOP"] = "WAIT"
    unsupported_requirements: Annotated[tuple[ContractRef, ...], Field(max_length=32)] = ()
    allow_kind: Literal[ContinuationKind.EXECUTABLE_CAPABILITY, ContinuationKind.OBSERVATION]
    blocked_kind: Literal[ContinuationKind.SAFE_STOP, ContinuationKind.EXTERNAL_REMEDIATION] = ContinuationKind.SAFE_STOP
    handler_required: bool = True

    @model_validator(mode="after")
    def _unique(self):
        for values in (self.required_authority_kinds, self.prerequisites, self.unsupported_requirements):
            if len(set(values)) != len(values):
                raise ValueError("duplicate policy requirement")
        if len({s.dimension for s in self.states}) != len(self.states):
            raise ValueError("duplicate state requirement")
        if self.consent_kind and self.consent_kind not in self.required_authority_kinds:
            raise ValueError("consent requires its own authority kind")
        for name in ("required_authority_kinds", "prerequisites", "unsupported_requirements"):
            object.__setattr__(self, name, tuple(sorted(getattr(self, name), key=str)))
        object.__setattr__(self, "states", tuple(sorted(self.states, key=lambda s: s.dimension)))
        return self


class PrerequisiteObservation(_Contract):
    requirement: ContractRef
    observation: Observation


class AdmissionInput(_Contract):
    catalog: CatalogSnapshot
    catalog_content: ContentRef
    capability: CapabilityDescriptor
    transition: TransitionDescriptor | None = None
    policy: AdmissionPolicy
    actor: ActorRef
    scope: Scope
    state: WorkflowState
    authorities: Annotated[tuple[AuthorityReference, ...], Field(max_length=32)] = ()
    prerequisites: Annotated[tuple[PrerequisiteObservation, ...], Field(max_length=32)] = ()
    authority_version: Identifier
    source_version: ContentRef
    effect: Effect
    handler_evidence: ContentRef | None = None
    consent: ConsentStatus = ConsentStatus.MISSING

    @model_validator(mode="after")
    def _sets(self):
        if len({a.authority_id for a in self.authorities}) != len(self.authorities):
            raise ValueError("duplicate authority identity")
        if len({p.requirement for p in self.prerequisites}) != len(self.prerequisites):
            raise ValueError("duplicate prerequisite identity")
        object.__setattr__(self, "authorities", tuple(sorted(self.authorities, key=lambda a: a.authority_id)))
        object.__setattr__(self, "prerequisites", tuple(sorted(self.prerequisites,
            key=lambda p: (p.requirement.contract_id, p.requirement.version))))
        return self

    def content_identity(self) -> ContentRef:
        value = AdmissionInput.model_validate(self)
        return ContentRef(content_id="admission-input", sha256=sha256_bytes(
            b"harness-admission-input-v1\0" + canonical_json(value).encode("utf-8")))


class QualifiedEvaluation(_Contract):
    """Future trusted-owner input, NOT proof of the owner's trustworthiness.

    Every listed authority/prerequisite is positively qualified for this exact
    input identity and current source/authority version. Synthetic tests inject
    this assumption explicitly. A serialized prior decision is not this type.
    """

    issuer: ContractRef
    input: ContentRef
    authority_ids: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    prerequisites: Annotated[tuple[ContractRef, ...], Field(max_length=32)]
    handler_evidence: ContentRef | None = None

    @model_validator(mode="after")
    def _sets(self):
        if len(set(self.authority_ids)) != len(self.authority_ids) or len(set(self.prerequisites)) != len(self.prerequisites):
            raise ValueError("duplicate qualification member")
        object.__setattr__(self, "authority_ids", tuple(sorted(self.authority_ids)))
        object.__setattr__(self, "prerequisites", tuple(sorted(self.prerequisites, key=str)))
        return self


class EvaluationContext(_Contract):
    source_input: ContentRef
    trusted_issuer: ContractRef | None
    qualification: QualifiedEvaluation | None


class AdmissionReason(_Contract):
    priority: Annotated[int, Field(ge=0, le=4)]
    code: Identifier
    outcome: DecisionOutcome


class AdmissionEvaluation(_Contract):
    input: ContentRef
    context: EvaluationContext
    decision: AdmissibilityDecision
    reasons: Annotated[tuple[AdmissionReason, ...], Field(min_length=1, max_length=64)]
    continuations: Annotated[tuple[Continuation, ...], Field(min_length=1, max_length=1)]
    qualification_issuer: ContractRef | None = None
    handler_evidence: ContentRef | None = None


def evaluate(value: AdmissionInput, *, trusted_issuer: ContractRef | None = None,
             qualification: QualifiedEvaluation | None = None) -> AdmissionEvaluation:
    """Shared projection/preflight function. Trust parameters are owner-injected.

    Invalid envelopes raise validation errors; no safe actor/scope can be inferred
    from them. Valid but conflicting inputs produce a typed SAFE_STOP observation.
    No clock, reader, availability callback, handler or authority resolver runs.
    """
    value = AdmissionInput.model_validate(value)
    # Bound the entire envelope too, not just its individual collections.
    value = parse_contract(AdmissionInput, canonical_json(value))
    policy, cap, transition = value.policy, value.capability, value.transition
    source_identity = value.content_identity()
    if trusted_issuer is not None:
        trusted_issuer = ContractRef.model_validate(trusted_issuer)
    if qualification is not None:
        qualification = QualifiedEvaluation.model_validate(qualification)
    context = EvaluationContext(source_input=source_identity, trusted_issuer=trusted_issuer,
        qualification=qualification)
    identity = ContentRef(content_id="admission-evaluation-input", sha256=sha256_bytes(
        b"harness-admission-evaluation-v1\0" + canonical_json(context).encode("utf-8")))
    reasons = set()

    def add(priority, code, outcome=DecisionOutcome.SAFE_STOP):
        reasons.add((priority, code, outcome))

    if (policy.policy.version != 1 or policy.unsupported_requirements):
        add(0, "unsupported_policy")
    if value.catalog_content != value.catalog.content_identity() or policy.catalog != value.catalog_content:
        add(0, "catalog_identity_mismatch")
    found = value.catalog.resolve_capability(cap.capability)
    if found.status != LookupStatus.DECLARED or found.capability != cap or policy.capability != cap.capability:
        add(0, "capability_identity_mismatch")
    if (transition.transition if transition else None) != policy.transition:
        add(0, "transition_identity_mismatch")
    if transition:
        found = value.catalog.resolve_transition(transition.transition)
        if found.status != LookupStatus.DECLARED or found.transition != transition or transition.capability != cap.capability:
            add(0, "transition_identity_mismatch")
    if value.effect != cap.effect or policy.effect != cap.effect or (transition and transition.effect != cap.effect):
        add(0, "effect_mismatch")
    if cap.effect != Effect.OBSERVE and policy.allow_kind == ContinuationKind.OBSERVATION:
        add(0, "effectful_observation_mismatch")
    required = set(cap.required_authority_kinds) | set(transition.required_authority_kinds if transition else ())
    if not required <= set(policy.required_authority_kinds):
        add(0, "authority_policy_weakened")
    if transition and not set(transition.prerequisites) <= set(policy.prerequisites):
        add(0, "prerequisite_policy_weakened")
    if policy.actor != value.actor:
        add(0, "actor_mismatch")
    if policy.scope != value.scope:
        add(0, "scope_mismatch")
    qualified = bool(qualification and trusted_issuer and qualification.issuer == trusted_issuer
                     and qualification.input == source_identity)
    if qualification is not None and not qualified:
        add(0, "qualification_binding_mismatch")
    if not qualified:
        add(2, "currentness_unqualified", DecisionOutcome(policy.missing_authority))
    if value.state.authority_currentness != AuthorityCurrentness.CURRENT:
        add(0 if value.state.authority_currentness == AuthorityCurrentness.CONFLICT else 2,
            "state_authority_unqualified", DecisionOutcome.SAFE_STOP
            if value.state.authority_currentness == AuthorityCurrentness.CONFLICT else DecisionOutcome(policy.missing_authority))
    for authority in value.authorities:
        if authority.subject != value.actor or authority.scope != value.scope or authority.policy != policy.policy:
            add(0, "authority_binding_mismatch")
        if authority.currentness == AuthorityCurrentness.CONFLICT:
            add(0, "authority_conflict")
        elif authority.currentness != AuthorityCurrentness.CURRENT:
            add(2, "authority_" + authority.currentness.value.lower(), DecisionOutcome(policy.missing_authority))
        if not qualified or authority.authority_id not in qualification.authority_ids:
            add(2, "authority_not_qualified", DecisionOutcome(policy.missing_authority))
    if not set(policy.required_authority_kinds) <= {a.kind for a in value.authorities}:
        add(2, "required_authority_missing", DecisionOutcome(policy.missing_authority))
    if len({a.kind for a in value.authorities}) != len(value.authorities):
        add(0, "authority_kind_ambiguous")
    if policy.consent_kind:
        if value.consent == ConsentStatus.CONFLICT:
            add(0, "consent_conflict")
        elif value.consent == ConsentStatus.UNSUPPORTED:
            add(0, "consent_schema_unsupported")
        elif value.consent == ConsentStatus.DENIED:
            add(1, "consent_denied", DecisionOutcome.DENY)
        elif value.consent != ConsentStatus.GRANTED:
            add(2, "consent_" + value.consent.value.lower(), DecisionOutcome.WAIT)
    for requirement in policy.states:
        actual = getattr(value.state, requirement.dimension)
        if actual.support != StateSupport.SUPPORTED or requirement.expected.support != StateSupport.SUPPORTED:
            add(0, "state_requirement_unsupported")
        elif actual != requirement.expected:
            add(3, "state_" + requirement.dimension + "_unmet", DecisionOutcome(policy.missing_prerequisite))
    for item in value.prerequisites:
        obs = item.observation
        if obs.scope != value.scope or obs.actor != value.actor:
            add(0, "observation_binding_mismatch")
        if obs.status in (ObservationStatus.CONFLICT, ObservationStatus.INVALID,
                          ObservationStatus.UNSTABLE, ObservationStatus.UNSUPPORTED):
            add(0, "observation_" + obs.status.value.lower())
    by_ref = {p.requirement: p.observation for p in value.prerequisites}
    for requirement in policy.prerequisites:
        obs = by_ref.get(requirement)
        if obs is None or obs.status != ObservationStatus.PRESENT:
            add(3, "prerequisite_missing", DecisionOutcome(policy.missing_prerequisite))
        elif any(check != CheckStatus.VERIFIED for check in (obs.integrity, obs.structure, obs.binding)):
            add(3, "prerequisite_unverified", DecisionOutcome(policy.missing_prerequisite))
        if not qualified or requirement not in qualification.prerequisites:
            add(3, "prerequisite_not_qualified", DecisionOutcome(policy.missing_prerequisite))
    if policy.handler_required and (value.handler_evidence is None or not qualified
            or qualification.handler_evidence != value.handler_evidence):
        add(0, "handler_correspondence_unqualified")
    if not reasons:
        add(4, "requirements_qualified", DecisionOutcome.ALLOW)
    ordered = tuple(AdmissionReason(priority=p, code=c, outcome=o) for p, c, o in sorted(reasons))
    primary = ordered[0]
    # Conflicting out-of-envelope authorities stay in the input trace, never in
    # HAR-04's structurally bound current_authorities collection.
    authorities = tuple(a for a in value.authorities if a.subject == value.actor and a.scope == value.scope)
    decision = AdmissibilityDecision(decision_id="admission." + identity.sha256,
        scope=value.scope, actor=value.actor, capability=cap.capability,
        transition=transition.transition if transition else None, outcome=primary.outcome,
        reason_code=primary.code, policy=policy.policy,
        required_authority_kinds=tuple(sorted(set(policy.required_authority_kinds)
            if required <= set(policy.required_authority_kinds) else required)),
        current_authorities=authorities, expected_authority_version=value.authority_version,
        prerequisites=tuple(sorted({o.observation.source_content for o in value.prerequisites
            if o.observation.source_content}, key=lambda c: (c.content_id, c.sha256))), effect=value.effect)
    kind = (policy.allow_kind if primary.outcome == DecisionOutcome.ALLOW else
            ContinuationKind.SAFE_STOP if primary.outcome == DecisionOutcome.SAFE_STOP else
            ContinuationKind.HUMAN_DECISION if primary.outcome == DecisionOutcome.WAIT
            and primary.code in {"consent_missing", "consent_pending", "consent_expired", "consent_superseded"}
            else ContinuationKind.OBSERVATION if primary.outcome == DecisionOutcome.WAIT
            else ContinuationKind.EXTERNAL_REMEDIATION)
    if primary.outcome == DecisionOutcome.SAFE_STOP:
        kind = policy.blocked_kind
    continuation = Continuation(continuation_id="continuation." + identity.sha256,
        scope=value.scope, actor=value.actor, kind=kind, reason_code=primary.code, policy=policy.policy,
        capability=cap.capability if kind == ContinuationKind.EXECUTABLE_CAPABILITY else None,
        decision_target=cap.capability if kind == ContinuationKind.HUMAN_DECISION else None)
    return AdmissionEvaluation(input=identity, context=context, decision=decision, reasons=ordered,
        continuations=(continuation,), qualification_issuer=trusted_issuer if qualified else None,
        handler_evidence=value.handler_evidence)
