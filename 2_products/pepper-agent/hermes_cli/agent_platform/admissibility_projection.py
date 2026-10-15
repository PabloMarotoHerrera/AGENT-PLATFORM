"""Passive public action qualification; no workflow selection or dispatch.

Preserves an explicitly supplied legacy selection, including omitted optional
fields. It never manufactures tool arguments, consent, labels or action IDs.
HAR-09 may supply shadow inputs later; no production caller is connected now.
"""

import re
from typing import Annotated, Literal

from pydantic import Field

from .handler_correspondence import BindingEvidence, BindingStatus
from .harness.admissibility import AdmissionEvaluation, AdmissionPolicy, StateRequirement
from .harness.contracts import (
    ActorRef, ContentRef, ContinuationKind, ContractRef, DecisionOutcome, Identifier,
    Observational, Scope, StateDimension, StateSupport, _Contract,
)
from .harness.validation import canonical_json, sha256_bytes
from .pre_review_catalog import product_catalog, product_operations


def operation_policy(operation_id: str, actor: ActorRef, scope: Scope) -> AdmissionPolicy:
    """Declarative first-slice requirements, without implementing domain guards.

    The legacy-guard-result prerequisite names a future trusted producer's
    complete guard result, including the bindings in the pre-edit matrix. Merely
    naming it, or supplying a HAR-05 PRESENT observation, never satisfies it.
    No such production qualification boundary exists in HAR-07.
    """
    operation = next((o for o in product_operations() if o.capability.capability.contract_id == operation_id), None)
    if operation is None:
        raise ValueError("operation_not_declared")
    cap, transition = operation.capability, operation.transition
    consent_kinds = {"O02": "human_command_consent", "O05": "fresh_human_binding",
        "O07": "fresh_human_binding", "O08": "human_revision_consent",
        "P02.passed": "human_item_attestation", "P02.failed": "human_item_attestation",
        "P03.prepare": "human_prepare_request"}
    state_values = {}
    if operation_id in {"O01", "O02", "O04", "O05", "O06", "O07", "O08",
                         "P01", "P02.passed", "P02.failed"}:
        state_values.update(execution="terminal_inactive", completion="terminal_bound")
    if operation_id in {"O03.ticket_spec", "O03.validation_steps"}:
        state_values["publication"] = "approved"
    if operation_id == "P03.prepare":
        state_values.update(publication="approved", execution="terminal_inactive",
            validation="passed", review="ready", completion="terminal_bound")
    states = tuple(StateRequirement(dimension=dimension, expected=StateDimension(
        definition=ContractRef(contract_id="pepper." + dimension, version=1),
        value=value, support=StateSupport.SUPPORTED)) for dimension, value in state_values.items())
    return AdmissionPolicy(policy=operation.policy, capability=cap.capability,
        transition=transition.transition, catalog=product_catalog().content_identity(), actor=actor,
        scope=scope, effect=cap.effect, required_authority_kinds=cap.required_authority_kinds,
        prerequisites=transition.prerequisites + (ContractRef(
            contract_id=operation_id + ".legacy-guard-result", version=1),), states=states,
        consent_kind=consent_kinds.get(operation_id),
        allow_kind=ContinuationKind.OBSERVATION if cap.effect.value == "OBSERVE" else ContinuationKind.EXECUTABLE_CAPABILITY)


class LegacyAction(_Contract):
    id: Annotated[str, Field(min_length=1, max_length=160)]
    label: Annotated[str, Field(max_length=240)]
    target_ticket_id: Identifier | None = None
    target_ticket_title: Annotated[str, Field(max_length=240)] | None = None
    required_human_action: Annotated[str, Field(max_length=160)] | None = None
    executable: bool | None = None
    read_only: bool | None = None

    def public_fields(self) -> dict:
        # model_fields_set preserves absent versus explicit null/false.
        return {k: v for k, v in self.model_dump(exclude_unset=True).items() if k != "schema_version"}


class LegacyContext(_Contract):
    current_ticket_id: Identifier | None
    next_ticket_id: Identifier | None = None
    action: LegacyAction
    operation: Identifier
    target_ticket_id: Identifier
    active_execution: bool
    separate_successor_decision: LegacyAction | None = None


class PublicActionTranslation(_Contract):
    qualification: Literal["MAPPED", "UNMAPPED", "UNSUPPORTED"]
    reason_code: Identifier
    input: ContentRef
    current_ticket_id: Identifier | None
    next_ticket_id: Identifier | None
    action: LegacyAction | None = None
    separate_successor_decision: LegacyAction | None = None
    invocable: bool = False
    handler: BindingEvidence | None = None
    observational: Observational = True


def binding_identity(binding: BindingEvidence) -> ContentRef:
    binding = BindingEvidence.model_validate(binding)
    return ContentRef(content_id="handler-correspondence", sha256=sha256_bytes(
        b"har07-handler-correspondence-v1\0" + canonical_json(binding).encode("utf-8")))


def translate(evaluation: AdmissionEvaluation, context: LegacyContext, *,
              binding: BindingEvidence | None = None) -> PublicActionTranslation:
    """Qualify supplied selected action; never select a different public action.

    invocable describes a candidate offer, never enables a runtime action.
    Unmapped results deliberately have no action/handler. Active C26 context and
    its distinct successor human decision are retained, never promoted/reselected.
    """
    evaluation = AdmissionEvaluation.model_validate(evaluation)
    context = LegacyContext.model_validate(context)
    if binding is not None:
        binding = BindingEvidence.model_validate(binding)
    decision = evaluation.decision
    continuation = evaluation.continuations[0]
    base = dict(input=evaluation.input, current_ticket_id=context.current_ticket_id,
        next_ticket_id=context.next_ticket_id,
        separate_successor_decision=context.separate_successor_decision)

    def fail(reason, qualification="UNSUPPORTED"):
        return PublicActionTranslation(qualification=qualification, reason_code=reason, **base)

    if (continuation.actor != decision.actor or continuation.scope != decision.scope
            or continuation.policy != decision.policy or continuation.reason_code != decision.reason_code
            or (continuation.capability and continuation.capability != decision.capability)
            or (continuation.decision_target and continuation.decision_target != decision.capability)):
        return fail("continuation_binding_mismatch")
    target = context.target_ticket_id
    if target not in decision.scope.resource_ids:
        return fail("target_scope_mismatch")
    if context.action.target_ticket_id not in (None, target):
        return fail("legacy_target_mismatch")
    token = target.replace(".", "_")
    diagnostics = {
        "RESOLVE_EXECUTION_AUTHORITY": (f"RESOLVE_{token}_EXECUTION_AUTHORITY", ContinuationKind.SAFE_STOP),
        "RESOLVE_REVIEW_BLOCKER": (f"RESOLVE_{token}_REVIEW_BLOCKER", ContinuationKind.EXTERNAL_REMEDIATION),
    }
    if context.operation in diagnostics:
        action_id, kind = diagnostics[context.operation]
        if (context.action.id != action_id or continuation.kind != kind
                or context.action.executable is True or binding is not None):
            return fail("diagnostic_not_invocable")
        if context.operation == "RESOLVE_EXECUTION_AUTHORITY" and (
                context.action.executable is not False or context.action.read_only is not True):
            return fail("execution_diagnostic_flags_mismatch")
        return PublicActionTranslation(qualification="MAPPED", reason_code="diagnostic_preserved",
            action=context.action, **base)
    operation = next((o for o in product_operations() if o.capability.capability.contract_id == context.operation), None)
    if operation is None or operation.capability.capability != decision.capability or operation.policy != decision.policy:
        return fail("operation_not_declared", "UNMAPPED")
    if decision.transition != operation.transition.transition:
        return fail("operation_transition_mismatch")
    # Match governed_ticket_lifecycle_action_token without importing runtime.
    # The two RESOLVE diagnostics above historically use dot replacement only.
    token = re.sub(r"[^A-Za-z0-9]+", "_", target).strip("_").upper()
    mappings = {
        "O02": (f"VALIDATE_{token}_COMMANDS", "command_validation_authorization"),
        "O05": (f"REQUEST_{token}_POST_EXECUTION_MATERIAL_REVISION", "post_execution_material_revision_request"),
        "O07": ("RECONCILE_MATERIAL_REVISION_AUTHORITY", "authority_reconciliation"),
        "O08": (f"REVISE_{token}", "ticket_material_revision"),
        "P03.prepare": (f"PREPARE_{token}_REVIEW", "review_preparation"),
    }
    if context.operation not in mappings:
        return fail("no_standalone_public_action", "UNMAPPED")
    action_id, human_action = mappings[context.operation]
    if context.action.id != action_id:
        return fail("public_action_id_mismatch", "UNMAPPED")
    # Existing prepare overlays have different human labels (some omit the
    # field); preserve the supplied label instead of inventing a uniform one.
    if context.operation != "P03.prepare" and context.action.required_human_action != human_action:
        return fail("public_human_action_mismatch")
    if context.operation == "O08" and context.active_execution:
        return fail("successor_decision_must_remain_separate")
    if context.operation == "P03.prepare" and context.active_execution:
        return fail("active_execution_blocks_review")
    if target != context.current_ticket_id and not (context.operation == "O08"
            and context.current_ticket_id is None and target == context.next_ticket_id):
        return fail("current_context_mismatch")
    invocable = continuation.kind == ContinuationKind.EXECUTABLE_CAPABILITY
    if invocable:
        if context.action.executable is False or context.action.read_only is True:
            return fail("legacy_nonexecutable_classification_preserved")
        if (decision.outcome != DecisionOutcome.ALLOW or evaluation.qualification_issuer is None
                or binding is None or binding.status != BindingStatus.VERIFIED
                or binding.declaration != operation.handler or binding_identity(binding) != evaluation.handler_evidence):
            return fail("executable_offer_not_qualified")
    elif continuation.kind != ContinuationKind.HUMAN_DECISION or decision.outcome != DecisionOutcome.WAIT:
        return fail("blocked_offer_has_no_public_capability")
    if not invocable and (context.action.executable is True or binding is not None):
        return fail("pending_decision_not_invocable")
    return PublicActionTranslation(qualification="MAPPED", reason_code="legacy_selection_preserved",
        action=context.action, invocable=invocable, handler=binding if invocable else None, **base)
