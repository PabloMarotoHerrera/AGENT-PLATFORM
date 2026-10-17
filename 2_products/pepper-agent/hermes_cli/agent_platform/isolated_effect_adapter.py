"""Fake C94 immutable append in an explicitly created disposable SQLite store.

This is not the production reconciliation owner or an arbitrary callback runner.
Effect+receipt+aggregate CAS share one local transaction. Journal confirmation and
completion are separate durable stages. No external exactly-once or recovery.
"""

from .harness.journal_protocol import (completion, qualify, verify_attempt, verify_receipt)
from .harness.operation_journal import (EffectAttempt, EffectReceipt, ExpectedVersion,
    StageTransition, UnknownOutcome)
from .harness.validation import canonical_json, parse_contract, verify_content_digest
from .isolated_operation_journal import IsolatedJournal, JournalConflict


def transition(head, stage, reason='fixture_stage', **kwargs):
    return StageTransition(previous=head.identity(), expected_journal_version=head.journal_version,
        stage=stage, reason=reason, **kwargs)


def attempt_for(request, owner, attempt_id):
    return EffectAttempt(attempt_id=attempt_id, request=request.identity(), effect=request.effect,
        owner=owner, implementation=request.context.implementation.content, authority=request.context.authority.content,
        inputs=tuple(v.content for v in request.context.validation_inputs))


class IsolatedAppendAdapter:
    def apply(self, journal, attempt, payload, *, authorization, observed_context, reject=False):
        if type(journal) is not IsolatedJournal:
            raise TypeError('explicit_disposable_substrate_required')
        if type(reject) is not bool:
            raise TypeError('explicit_fixture_rejection_boolean_required')
        if type(payload) is not bytes or len(payload) > 65_536 or not verify_content_digest(payload, attempt.effect.payload):
            raise ValueError('effect_payload_mismatch')
        conflict = None
        with journal.transaction() as c:
            head = journal._entries(c, attempt.effect.operation_id)[-1]
            request = head.request
            if head.stage != 'EFFECT_ATTEMPTED' or head.transition.attempt != attempt:
                raise ValueError('effect_attempt_not_dispatchable')
            qualify(request, authorization, observed_context)
            verify_attempt(request, head.owner, attempt)
            row = c.execute('SELECT attempt,payload,receipt FROM effects WHERE id=?', (attempt.effect.effect_id,)).fetchone()
            if row is not None:
                if row[0] != canonical_json(attempt) or row[1] != payload:
                    conflict = journal._conflict(c, request, head.owner.writer, 'conflicting_effect_key', head.journal_version, head)
                else:
                    receipt = journal._receipt(c, attempt.effect.effect_id)
                    verify_receipt(request, head.owner, receipt)
                    return receipt
            observed = journal._observed(c, request.expected)
            # This is the final pre-effect CAS, inside the effect transaction.
            if conflict is not None:
                pass
            elif observed != request.expected:
                conflict = journal._conflict(c, request, head.owner.writer, 'pre_effect_version_conflict', head.journal_version, head, observed)
            else:
                updated = ExpectedVersion.model_validate({**observed.model_dump(), 'value':observed.value+(not reject)})
                if not reject:
                    changed = c.execute('UPDATE aggregates SET body=? WHERE id=? AND body=?',
                        (canonical_json(updated), observed.aggregate, canonical_json(observed))).rowcount
                    if changed != 1:
                        raise ValueError('atomic_compare_and_swap_failed')
                receipt = EffectReceipt(attempt=attempt, outcome='REJECTED' if reject else 'CONFIRMED', observed=updated,
                    effect_record=None if reject else attempt.effect.payload)
                verify_receipt(request, head.owner, receipt)
                c.execute('INSERT INTO effects VALUES (?,?,?,?)',
                    (attempt.effect.effect_id, canonical_json(attempt), payload, canonical_json(receipt)))
        if conflict:
            raise JournalConflict(conflict)
        return receipt


def run_fixture(journal, request, payload, *, writer, authorization, observed_context, failure=None):
    """Bounded test sequence. Injected failure windows are not HAR13 recovery."""
    if type(journal) is not IsolatedJournal:
        raise TypeError('explicit_disposable_substrate_required')
    if failure not in {None, 'before_effect', 'after_effect', 'after_receipt'}:
        raise ValueError('unsupported_fixture_failure_window')
    head = journal.request(request)
    if head.stage != 'REQUESTED':
        # In particular ATTEMPTED/UNKNOWN cannot be interpreted as not executed.
        return completion(head)
    owner = journal.claim(request.operation_id, writer, head.journal_version)
    for stage in ('PREPARED', 'EFFECT_INTENT_RECORDED'):
        head = journal.move(request.operation_id, writer, transition(head, stage),
            authorization=authorization, observed_context=observed_context)
    if failure == 'before_effect':
        head = journal.move(request.operation_id, writer, transition(head, 'SAFE_STOP', 'fixture_failure_before_effect'))
        return completion(head)
    attempt = attempt_for(request, owner, 'first-attempt')
    head = journal.move(request.operation_id, writer, transition(head, 'EFFECT_ATTEMPTED', attempt=attempt),
        authorization=authorization, observed_context=observed_context)
    try:
        receipt = IsolatedAppendAdapter().apply(journal, attempt, payload,
            authorization=authorization, observed_context=observed_context)
        if failure == 'after_effect':
            raise RuntimeError('fixture_failure_after_effect_before_journal_receipt')
    except Exception:
        unknown = UnknownOutcome(attempt=attempt, reason='effect_confirmation_not_established')
        head = journal.move(request.operation_id, writer, transition(head, 'EFFECT_OUTCOME_UNKNOWN', attempt=attempt, unknown=unknown))
        return completion(head)
    head = journal.move(request.operation_id, writer, transition(head, 'EFFECT_CONFIRMED', attempt=attempt, receipt=receipt))
    if failure == 'after_receipt':
        return completion(head)
    head = journal.move(request.operation_id, writer, transition(head, 'COMPLETED', attempt=attempt, receipt=receipt))
    return completion(head)
