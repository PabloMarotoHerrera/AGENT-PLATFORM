"""Versioned passive journal records; construction grants no effect permission."""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .contracts import ActorRef, ContentRef, ContractRef, Identifier, Observational, Scope, Version, _Contract
from .dependency_identity import DependencyContext, content_identity
from .invalidation import JointIdentityAssessment
from .validation_dag import ValidationAssessment

PROTOCOL = ContractRef(contract_id="harness-operation-journal", version=1)
POLICY = ContractRef(contract_id="isolated-immutable-append", version=1)
ADAPTER = ContractRef(contract_id="isolated-sqlite-append", version=1)
Counter = Annotated[int, Field(ge=0, le=2_147_483_647)]
Stage = Literal["REQUESTED", "PREPARED", "EFFECT_INTENT_RECORDED", "EFFECT_ATTEMPTED",
    "EFFECT_CONFIRMED", "EFFECT_REJECTED", "EFFECT_OUTCOME_UNKNOWN", "COMPLETED", "CONFLICT", "SAFE_STOP"]


class JournalRecord(_Contract):
    def identity(self) -> ContentRef:
        return content_identity("journal-" + type(self).__name__ + "-v1", self)


class ExpectedVersion(JournalRecord):
    store: ContractRef
    aggregate: Identifier
    scope: Scope
    value: Counter


class EffectIntent(JournalRecord):
    effect_id: Identifier
    operation_id: Identifier
    operation_version: Version
    scope: Scope
    expected: ExpectedVersion
    payload: ContentRef
    adapter: ContractRef = ADAPTER
    delivery: Literal["LOCAL_IMMUTABLE_KEY_NO_EXTERNAL_GUARANTEE"] = "LOCAL_IMMUTABLE_KEY_NO_EXTERNAL_GUARANTEE"


class OperationRequest(JournalRecord):
    operation_id: Identifier
    operation_version: Version
    actor: ActorRef
    context: DependencyContext
    expected: ExpectedVersion
    effect: EffectIntent
    validation_assessment: ContentRef
    protocol: ContractRef = PROTOCOL
    policy: ContractRef = POLICY
    qualification: Literal["UNQUALIFIED", "ISOLATED_SYNTHETIC_TEST_ONLY"] = "UNQUALIFIED"

    @model_validator(mode="after")
    def _binding(self):
        if (self.context.scope != self.expected.scope or self.effect.scope != self.context.scope
                or self.effect.expected != self.expected or self.effect.operation_id != self.operation_id
                or self.effect.operation_version != self.operation_version):
            raise ValueError("operation/effect/resource/version mismatch")
        if self.protocol != PROTOCOL or self.policy != POLICY or self.effect.adapter != ADAPTER:
            raise ValueError("unsupported journal/adapter policy")
        return self


class WriterBinding(JournalRecord):
    request: ContentRef
    writer: Identifier
    operation_id: Identifier
    operation_version: Version
    scope: Scope
    expected: ExpectedVersion
    context: ContentRef


class EffectAttempt(JournalRecord):
    attempt_id: Identifier
    request: ContentRef
    effect: EffectIntent
    owner: WriterBinding
    implementation: ContentRef
    authority: ContentRef
    inputs: Annotated[tuple[ContentRef, ...], Field(min_length=1, max_length=32)]


class EffectReceipt(JournalRecord):
    attempt: EffectAttempt
    outcome: Literal["CONFIRMED", "REJECTED"]
    observed: ExpectedVersion
    adapter: ContractRef = ADAPTER
    effect_record: ContentRef | None


class ConflictReport(JournalRecord):
    operation_id: Identifier
    request: ContentRef
    writer: Identifier
    reason: Identifier
    expected_journal_version: Counter
    observed_journal_version: Counter
    expected: ExpectedVersion
    observed: ExpectedVersion | None = None


class UnknownOutcome(JournalRecord):
    attempt: EffectAttempt
    reason: Identifier
    recovery_policy: Literal["EXPLICIT_QUALIFIED_RECOVERY_REQUIRED_NOT_IMPLEMENTED"] = "EXPLICIT_QUALIFIED_RECOVERY_REQUIRED_NOT_IMPLEMENTED"
    retry_allowed: Literal[False] = False


class StageTransition(JournalRecord):
    previous: ContentRef
    expected_journal_version: Counter
    stage: Stage
    reason: Identifier
    attempt: EffectAttempt | None = None
    receipt: EffectReceipt | None = None
    unknown: UnknownOutcome | None = None
    conflict: ConflictReport | None = None


class JournalEntry(JournalRecord):
    request: OperationRequest
    journal_version: Annotated[int, Field(ge=1, le=32)]
    stage: Stage
    predecessor: ContentRef | None
    owner: WriterBinding | None = None
    transition: StageTransition | None = None

    @model_validator(mode="after")
    def _shape(self):
        if self.journal_version == 1:
            if self.stage != "REQUESTED" or any(v is not None for v in (self.predecessor, self.owner, self.transition)):
                raise ValueError("invalid_journal_genesis")
        elif (self.predecessor is None or self.owner is None or self.transition is None
                or self.transition.stage != self.stage or self.transition.previous != self.predecessor
                or self.transition.expected_journal_version+1 != self.journal_version):
            raise ValueError("invalid_journal_link_shape")
        return self


class FixtureAuthorization(JournalRecord):
    """Explicit test assumption, not an authenticated issuer or production permit."""
    request: ContentRef
    human_decision: ContentRef
    identity_assessment: JointIdentityAssessment
    validation: ValidationAssessment
    provenance: ContentRef
    scope: Literal["ISOLATED_SYNTHETIC_TEST_ONLY"]


class CompletionResult(JournalRecord):
    operation_id: Identifier
    request: ContentRef
    entry: ContentRef
    stage: Stage
    receipt: ContentRef | None
    qualification: Literal["ISOLATED_SYNTHETIC_TEST_ONLY"] = "ISOLATED_SYNTHETIC_TEST_ONLY"
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False
