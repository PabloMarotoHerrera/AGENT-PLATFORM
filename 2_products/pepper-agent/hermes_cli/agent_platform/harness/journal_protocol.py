"""Pure stage/binding rules. No stores, clocks, authority issuer or recovery."""

from .contracts import AuthorityCurrentness
from .dependency_identity import content_identity
from .operation_journal import (ADAPTER, CompletionResult, EffectAttempt, EffectReceipt,
    FixtureAuthorization, JournalEntry, OperationRequest, StageTransition, WriterBinding)
from .validation import canonical_json, parse_contract

ALLOWED = {
    "REQUESTED": {"PREPARED", "CONFLICT", "SAFE_STOP"},
    "PREPARED": {"EFFECT_INTENT_RECORDED", "CONFLICT", "SAFE_STOP"},
    "EFFECT_INTENT_RECORDED": {"EFFECT_ATTEMPTED", "CONFLICT", "SAFE_STOP"},
    "EFFECT_ATTEMPTED": {"EFFECT_CONFIRMED", "EFFECT_REJECTED", "EFFECT_OUTCOME_UNKNOWN"},
    "EFFECT_CONFIRMED": {"COMPLETED", "SAFE_STOP"},
    "EFFECT_REJECTED": set(), "EFFECT_OUTCOME_UNKNOWN": set(),
    "COMPLETED": set(), "CONFLICT": set(), "SAFE_STOP": set(),
}


def checked(model, value):
    return parse_contract(model, canonical_json(value))


def owner_for(request: OperationRequest, writer: str) -> WriterBinding:
    r = checked(OperationRequest, request)
    return WriterBinding(request=r.identity(), writer=writer, operation_id=r.operation_id,
        operation_version=r.operation_version, scope=r.context.scope, expected=r.expected, context=r.context.identity())


def qualify(request: OperationRequest, authorization: FixtureAuthorization | None, observed_context) -> None:
    r = checked(OperationRequest, request)
    if authorization is None:
        raise ValueError("fixture_authorization_missing")
    q = checked(FixtureAuthorization, authorization)
    # No actor/issuer string can satisfy this explicit synthetic boundary.
    if (r.qualification != "ISOLATED_SYNTHETIC_TEST_ONLY" or q.request != r.identity()
            or r.context.required_human_decision is None or q.human_decision != r.context.required_human_decision
            or r.context.currentness != AuthorityCurrentness.CURRENT
            or r.context.qualification != "SYNTHETIC_ASSUMPTION" or observed_context != r.context):
        raise ValueError("fixture_human_source_currentness_unqualified")
    a = q.identity_assessment
    if (not a.structurally_compatible or a.candidate != r.context.identity() or a.expected != a.candidate
            or a.candidate_manifest != r.context.manifest or a.expected_manifest != a.candidate_manifest
            or a.qualification_scope != "ISOLATED_SYNTHETIC_TEST_ONLY"
            or {f.cause for f in a.findings} != {"UNCHANGED"}):
        raise ValueError("fixture_identity_unqualified")
    v = q.validation
    if (content_identity("journal-validation-assessment-v1", v) != r.validation_assessment
            or v.qualification_scope != "ISOLATED_SYNTHETIC_TEST_ONLY" or v.synthetic_assumption is None
            or not v.criterion_satisfied or not v.evidence_valid or not v.evidence_available
            or v.prerequisite_state != "SATISFIED" or v.invalid_dependencies or v.missing_producers
            or v.acceptance_readiness not in {"READY_MACHINE", "HUMAN_DECISION_RECORDED"}):
        raise ValueError("fixture_validation_unqualified")


def verify_attempt(request: OperationRequest, owner: WriterBinding, attempt: EffectAttempt):
    a = checked(EffectAttempt, attempt)
    if (owner != owner_for(request, owner.writer) or a.request != request.identity() or a.owner != owner
            or a.effect != request.effect or a.implementation != request.context.implementation.content
            or a.authority != request.context.authority.content
            or a.inputs != tuple(v.content for v in request.context.validation_inputs)):
        raise ValueError("attempt_binding_mismatch")


def verify_receipt(request: OperationRequest, owner: WriterBinding, receipt: EffectReceipt):
    r = checked(EffectReceipt, receipt)
    verify_attempt(request, owner, r.attempt)
    expected = request.expected
    if (r.adapter != ADAPTER or r.observed.store != expected.store or r.observed.aggregate != expected.aggregate
            or r.observed.scope != expected.scope or r.observed.value != expected.value + (r.outcome == "CONFIRMED")
            or r.effect_record != (request.effect.payload if r.outcome == "CONFIRMED" else None)):
        raise ValueError("receipt_binding_mismatch")


def initial(request):
    return JournalEntry(request=checked(OperationRequest, request), journal_version=1,
        stage="REQUESTED", predecessor=None)


def advance(previous: JournalEntry, transition: StageTransition, owner: WriterBinding) -> JournalEntry:
    p, t = checked(JournalEntry, previous), checked(StageTransition, transition)
    if t.previous != p.identity() or t.expected_journal_version != p.journal_version:
        raise ValueError("journal_predecessor_or_version_mismatch")
    if t.stage not in ALLOWED[p.stage] or owner != owner_for(p.request, owner.writer) or (p.owner is not None and p.owner != owner):
        raise ValueError("illegal_stage_or_owner")
    prior_attempt = p.transition.attempt if p.transition else None
    prior_receipt = p.transition.receipt if p.transition else None
    if t.stage == "EFFECT_ATTEMPTED":
        if t.attempt is None:
            raise ValueError("attempt_required")
        verify_attempt(p.request, owner, t.attempt)
    elif t.attempt is not None and t.attempt != prior_attempt:
        raise ValueError("foreign_attempt")
    if t.stage in {"EFFECT_CONFIRMED", "EFFECT_REJECTED", "COMPLETED"}:
        if t.receipt is None:
            raise ValueError("receipt_required")
        verify_receipt(p.request, owner, t.receipt)
        if t.receipt.attempt != prior_attempt:
            raise ValueError("receipt_attempt_mismatch")
        if t.stage == "EFFECT_REJECTED" and t.receipt.outcome != "REJECTED":
            raise ValueError("rejected_receipt_required")
        if t.stage != "EFFECT_REJECTED" and t.receipt.outcome != "CONFIRMED":
            raise ValueError("confirmed_receipt_required")
        if t.stage == "COMPLETED" and t.receipt != prior_receipt:
            raise ValueError("completion_receipt_changed")
    elif t.receipt is not None:
        raise ValueError("unexpected_receipt")
    if t.stage == "EFFECT_OUTCOME_UNKNOWN":
        if t.unknown is None or t.unknown.attempt != prior_attempt:
            raise ValueError("unknown_attempt_required")
    elif t.unknown is not None:
        raise ValueError("unexpected_unknown")
    if (t.stage == "CONFLICT") != (t.conflict is not None):
        raise ValueError("conflict_report_required")
    if t.conflict is not None and (t.conflict.operation_id != p.request.operation_id
            or t.conflict.request != p.request.identity() or t.conflict.writer != owner.writer
            or t.conflict.expected != p.request.expected):
        raise ValueError("foreign_conflict_report")
    return JournalEntry(request=p.request, journal_version=p.journal_version+1, stage=t.stage,
        predecessor=p.identity(), owner=owner, transition=t)


def completion(entry):
    e = checked(JournalEntry, entry)
    receipt = e.transition.receipt if e.transition else None
    if e.stage == "COMPLETED":
        if receipt is None or receipt.outcome != "CONFIRMED":
            raise ValueError("completion_receipt_required")
        verify_receipt(e.request, e.owner, receipt)
    return CompletionResult(operation_id=e.request.operation_id, request=e.request.identity(), entry=e.identity(),
        stage=e.stage, receipt=receipt.identity() if receipt else None)
