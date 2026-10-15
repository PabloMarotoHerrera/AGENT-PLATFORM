"""Product declarations for the approved O01–O08/P01–P03 first slice.

No tool imports, registration, discovery, current workflow selection or executor.
Continuations below are templates instantiated as data only on explicit request.
"""

from typing import Annotated

from pydantic import Field, model_validator

from .handler_correspondence import (
    BindingEvidence, BindingStatus, HandlerDeclaration, Selector, inspect_correspondence,
)
from .harness import (
    ActorRef, CapabilityDescriptor, ContentRef, Continuation, ContinuationKind, ContractRef,
    Effect, Scope, TransitionDescriptor, canonical_json, sha256_bytes,
)
from .harness.catalog import CatalogSnapshot, build_catalog
from .harness.contracts import Identifier, _Contract


def _ref(name):
    return ContractRef(contract_id=name, version=1)


class ProductOperation(_Contract):
    capability: CapabilityDescriptor
    transition: TransitionDescriptor
    handler: HandlerDeclaration
    inspector: ContractRef
    policy: ContractRef
    invalidation: ContractRef

    @model_validator(mode="after")
    def _binding(self) -> "ProductOperation":
        if self.handler.capability != self.capability.capability or self.transition.capability != self.capability.capability:
            raise ValueError("operation references disagree")
        build_catalog(_ref("operation-validation"), (self.capability,), (self.transition,))
        return self


class ContinuationTemplate(_Contract):
    template_id: Identifier
    kind: ContinuationKind
    reason_code: Identifier
    policy: ContractRef
    operation: ContractRef | None = None
    decision_target: ContractRef | None = None

    @model_validator(mode="after")
    def _kind(self) -> "ContinuationTemplate":
        if (self.kind == ContinuationKind.EXECUTABLE_CAPABILITY) != (self.operation is not None):
            raise ValueError("only executable templates may bind an operation")
        if (self.kind == ContinuationKind.HUMAN_DECISION) != (self.decision_target is not None):
            raise ValueError("human template requires decision target only")
        return self


def _operation(name, tool, symbol, selectors, effect, authorities, inspector, policy):
    ref = _ref(name)
    cap = CapabilityDescriptor(capability=ref, input_schema=_ref(tool + ".input"),
        output_schema=_ref(tool + ".result"), effect=effect, required_authority_kinds=authorities,
        evidence_contract=_ref(name + ".evidence"), execution_adapter=_ref("handler." + symbol),
        recovery_policy=_ref(name + ".recovery"))
    transition = TransitionDescriptor(transition=_ref(name + ".transition"), source_requirement=_ref(name + ".source"),
        capability=ref, prerequisites=(_ref(inspector),_ref(policy)), required_authority_kinds=authorities,
        effect=effect, target_rule=_ref(name + ".target"), failure_code="authority_or_evidence_failure",
        conflict_code="binding_conflict", continuation_rule=_ref(name + ".continuation"))
    return ProductOperation(capability=cap, transition=transition,
        handler=HandlerDeclaration(capability=ref,tool_name=tool,handler_symbol=symbol,
            selectors=tuple(Selector(field=k,value=v) for k,v in selectors)),
        inspector=_ref(inspector),policy=_ref(policy),invalidation=_ref(name + ".invalidation"))


def product_operations() -> tuple[ProductOperation, ...]:
    """Inert named references. Policy IDs do not load or enforce those policies."""
    rows = [
        ("O01", "prepare_current_ticket_review", "_prepare_current_ticket_review", (("operation","inspect_commands"),), Effect.OBSERVE, (), "command_validation.inspect", "pepper-pre-review-command-validation-v1"),
        ("O02", "prepare_current_ticket_review", "_prepare_current_ticket_review", (("operation","run_commands"),), Effect.WRITE_ARTIFACT, ("human_command_consent","current_workpacket"), "command_validation.inspect", "pepper-pre-review-command-validation-v1"),
        ("O03.ticket_spec", "inspect_pending_approval_artifact_section", "_inspect_pending_approval_artifact_section", (("authority_scope","current_approved"),("section_id","ticket_spec")), Effect.OBSERVE, ("current_approved_publication",), "approved_artifact_inspection.inspect", "pepper-ticket-architect-bridge-p18-9-0-v1"),
        ("O03.validation_steps", "inspect_pending_approval_artifact_section", "_inspect_pending_approval_artifact_section", (("authority_scope","current_approved"),("section_id","validation_steps")), Effect.OBSERVE, ("current_approved_publication",), "approved_artifact_inspection.inspect", "pepper-ticket-architect-bridge-p18-9-0-v1"),
    ]
    tool, handler = "request_current_ticket_material_revision", "_request_current_ticket_material_revision"
    for name, operation, inspector, policy, mutates in (
        ("O04","inspect","post_execution_material_revision.inspect","pepper-post-execution-material-revision-v1",False),
        ("O05","request","post_execution_material_revision.inspect","pepper-post-execution-material-revision-v1",True),
        ("O06","inspect_reconciliation","material_revision_reconciliation.inspect","pepper-material-revision-authority-reconciliation-v1",False),
        ("O07","reconcile","material_revision_reconciliation.inspect","pepper-material-revision-authority-reconciliation-v1",True),
    ):
        rows.append((name,tool,handler,(("origin","post_execution"),("operation",operation)),
            Effect.WRITE_ARTIFACT if mutates else Effect.OBSERVE,
            ("current_workpacket","fresh_human_binding") if mutates else ("current_workpacket",),inspector,policy))
    rows.extend([
        ("O08","revise_current_ticket_for_material_contract_failure","_revise_current_ticket_for_material_contract_failure",(),Effect.WRITE_ARTIFACT,("human_revision_consent","material_revision_authority"),"approved_artifact_inspection.inspect","pepper-ticket-architect-material-revision-authority-v1"),
        ("P01","inspect_current_ticket_manual_validation","_inspect_current_ticket_manual_validation",(),Effect.OBSERVE,(),"manual_validation.inspect","pepper-manual-validation-v1"),
        ("P02.passed","attest_current_ticket_manual_validation","_attest_current_ticket_manual_validation",(("status","passed"),),Effect.WRITE_ARTIFACT,("human_item_attestation",),"manual_validation.inspect","pepper-manual-validation-v1"),
        ("P02.failed","attest_current_ticket_manual_validation","_attest_current_ticket_manual_validation",(("status","failed"),),Effect.WRITE_ARTIFACT,("human_item_attestation",),"manual_validation.inspect","pepper-manual-validation-v1"),
        ("P03.workflow","get_workflow_control","_get_workflow_control",(("blockers_only",True),),Effect.OBSERVE,(),"workflow_control.blockers","pepper-p18-9-0-review-prepare-action-v1"),
        ("P03.review","get_review_status","_get_review_status",(),Effect.OBSERVE,(),"review_readiness.inspect","pepper-p18-9-0-review-prepare-action-v1"),
        ("P03.prepare","prepare_current_ticket_review","_prepare_current_ticket_review",(("operation","prepare"),),Effect.WRITE_ARTIFACT,("human_prepare_request","current_terminal_evidence","manual_validation"),"review_readiness.inspect","pepper-p18-9-0-review-prepare-action-v1"),
    ])
    return tuple(_operation(*row) for row in rows)


def product_catalog() -> CatalogSnapshot:
    operations = product_operations()
    payload = "\n".join(canonical_json(o) for o in sorted(operations,key=lambda o:o.capability.capability.contract_id))
    identity = ContentRef(content_id="pepper-operation-declarations",
        sha256=sha256_bytes(b"pepper-operation-declarations-v1\0"+payload.encode("utf-8")))
    return build_catalog(_ref("pepper-pre-review-material-revision"),
        tuple(o.capability for o in operations),tuple(o.transition for o in operations),(identity,))


def qualify_bindings(source: bytes) -> tuple[BindingEvidence, ...]:
    return tuple(inspect_correspondence(source,op.handler) for op in product_operations())


def continuation_templates() -> tuple[ContinuationTemplate, ...]:
    result = []
    for op in product_operations():
        observer = op.capability.effect == Effect.OBSERVE
        # Inspection is an observational next-action template, not an executable
        # offer. Its operation still has independently checked tool correspondence.
        result.append(ContinuationTemplate(template_id=op.capability.capability.contract_id,
            kind=ContinuationKind.OBSERVATION if observer else ContinuationKind.HUMAN_DECISION,
            reason_code="inspection_required" if observer else "fresh_human_decision_required",policy=op.policy,
            decision_target=None if observer else op.capability.capability))
        if not observer:
            result.append(ContinuationTemplate(template_id=op.capability.capability.contract_id+".requested",
                kind=ContinuationKind.EXECUTABLE_CAPABILITY,reason_code="requires_future_preflight",
                policy=op.policy,operation=op.capability.capability))
    result.extend((
        ContinuationTemplate(template_id="RESOLVE_EXECUTION_AUTHORITY",kind=ContinuationKind.SAFE_STOP,
            reason_code="execution_authority_blocked",policy=_ref("har03-execution-authority-blocker")),
        ContinuationTemplate(template_id="RESOLVE_REVIEW_BLOCKER",kind=ContinuationKind.EXTERNAL_REMEDIATION,
            reason_code="review_blocker_requires_resolution",policy=_ref("review-blocker-diagnostic")),
    ))
    return tuple(result)


def materialize_continuation(template: ContinuationTemplate, scope: Scope, actor: ActorRef,
                             source: bytes | None = None) -> Continuation:
    """Construct data only. A checked source binding never grants execution."""
    from .harness.validation import canonical_json, parse_contract
    template = ContinuationTemplate.model_validate(template)
    template = parse_contract(ContinuationTemplate, canonical_json(template))
    if template.operation is not None:
        op = next((o for o in product_operations() if o.capability.capability == template.operation),None)
        if op is None or template.policy != op.policy:
            raise ValueError("operation_policy_or_handler_mismatch")
        if source is None or inspect_correspondence(source, op.handler).status != BindingStatus.VERIFIED:
            raise ValueError("source correspondence missing_or_conflicting")
    elif source is not None:
        raise ValueError("diagnostic_human_or_observation_template_has_no_invocable_binding")
    return Continuation(continuation_id=template.template_id,scope=scope,actor=actor,kind=template.kind,
        reason_code=template.reason_code,policy=template.policy,capability=template.operation,
        decision_target=template.decision_target)
