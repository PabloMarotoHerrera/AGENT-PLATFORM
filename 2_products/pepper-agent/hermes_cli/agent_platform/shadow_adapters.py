"""Passive Pepper assembly from explicit captures; no reads, guards or dispatch."""

from typing import Annotated

from pydantic import Field

from .harness.contracts import (
    ActorRef, AuthorityReference, ContentRef, ContractRef, Identifier, Scope,
    WorkflowState, _Contract,
)
from .harness.admissibility import (
    AdmissionInput, ConsentStatus, PrerequisiteObservation, QualifiedEvaluation, evaluate,
)
from .harness.shadow import DecisionView, HarnessObservation, PublicAction
from .handler_correspondence import BindingEvidence, BindingStatus
from .pre_review_catalog import product_catalog, product_operations
from .admissibility_projection import LegacyContext, binding_identity, operation_policy, translate

ADAPTER = ContractRef(contract_id="pepper-shadow-adapter", version=1)


class SnapshotMetadata(_Contract):
    snapshot: ContentRef
    handler_source: ContentRef
    catalog: ContentRef
    context: LegacyContext
    actor: ActorRef
    scope: Scope
    state: WorkflowState
    authority_version: Identifier
    source_version: ContentRef
    consent: ConsentStatus
    authorities: Annotated[tuple[AuthorityReference, ...], Field(max_length=32)] = ()
    prerequisites: Annotated[tuple[PrerequisiteObservation, ...], Field(max_length=32)] = ()
    evidence: Annotated[tuple[ContentRef, ...], Field(max_length=64)] = ()


def assemble(metadata: SnapshotMetadata, binding: BindingEvidence | None) -> AdmissionInput:
    metadata = SnapshotMetadata.model_validate(metadata)
    op = next((o for o in product_operations() if o.capability.capability.contract_id == metadata.context.operation), None)
    if op is None:
        raise ValueError("unsupported_operation")
    proof = None
    if binding is not None:
        binding = BindingEvidence.model_validate(binding)
        if binding.declaration != op.handler or binding.source != metadata.handler_source:
            raise ValueError("stale_or_wrong_handler_correspondence")
        if binding.status == BindingStatus.VERIFIED:
            proof = binding_identity(binding)
    return AdmissionInput(catalog=product_catalog(), catalog_content=metadata.catalog,
        capability=op.capability, transition=op.transition,
        policy=operation_policy(metadata.context.operation, metadata.actor, metadata.scope),
        actor=metadata.actor, scope=metadata.scope, state=metadata.state,
        authorities=metadata.authorities, prerequisites=metadata.prerequisites,
        authority_version=metadata.authority_version, source_version=metadata.source_version,
        effect=op.capability.effect, handler_evidence=proof, consent=metadata.consent)


def observe(metadata: SnapshotMetadata, binding: BindingEvidence | None, *,
            trusted_issuer: ContractRef | None = None,
            qualification: QualifiedEvaluation | None = None) -> HarnessObservation:
    """Qualification is supplied by an explicit test trust assumption, never made here.

    Production has no trusted currentness owner. Default calls cannot yield qualified
    ALLOW. Merely presenting source-verified CURRENT observations is insufficient.
    """
    metadata = SnapshotMetadata.model_validate(metadata)
    value = assemble(metadata, binding)
    evaluation = evaluate(value, trusted_issuer=trusted_issuer, qualification=qualification)
    translation = translate(evaluation, metadata.context,
        binding=binding if evaluation.continuations[0].kind.value == "EXECUTABLE_CAPABILITY" else None)
    action = PublicAction.model_validate(translation.action.public_fields()) if translation.action else None
    states = metadata.state
    view = DecisionView(operation=metadata.context.operation, capability=value.capability.capability,
        policy=value.policy.policy, actor=metadata.actor, scope=metadata.scope,
        current_ticket_id=metadata.context.current_ticket_id, next_ticket_id=metadata.context.next_ticket_id,
        target_ticket_id=metadata.context.target_ticket_id,
        decision_target=metadata.context.target_ticket_id if evaluation.continuations[0].kind.value == "HUMAN_DECISION" else None,
        execution_target=metadata.context.target_ticket_id if evaluation.continuations[0].kind.value == "EXECUTABLE_CAPABILITY" else None,
        separate_successor=PublicAction.model_validate(metadata.context.separate_successor_decision.public_fields())
            if metadata.context.separate_successor_decision else None,
        action=action, mapping=translation.qualification, outcome=evaluation.decision.outcome.value,
        continuation=evaluation.continuations[0].kind, effect=value.effect, consent=value.consent,
        required_authority_kinds=value.policy.required_authority_kinds,
        authority_version=value.authority_version, source_version=value.source_version,
        guards=tuple(sorted(p.requirement.contract_id + ":" + p.observation.status.value
            for p in value.prerequisites)),
        active_execution=metadata.context.active_execution,
        terminal=states.execution.value == "terminal_inactive" if states.execution.support.value == "SUPPORTED" else None,
        review_ready=states.review.value == "ready" if states.review.support.value == "SUPPORTED" else None)
    return HarnessObservation(snapshot=metadata.snapshot, catalog=metadata.catalog, adapter=ADAPTER,
        view=view, admission_input=value, evaluation=evaluation, correspondence=value.handler_evidence,
        candidate_action=PublicAction.model_validate(metadata.context.action.public_fields())
            if translation.reason_code != "no_standalone_public_action" else None,
        translation_reason=translation.reason_code, evidence=metadata.evidence)
