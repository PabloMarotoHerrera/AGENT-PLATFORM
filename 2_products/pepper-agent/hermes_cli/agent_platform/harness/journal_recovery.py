"""Pure bounded interpretation of injected durable bytes, never repair or permission."""
from typing import Annotated, Literal
from pydantic import Field
from .contracts import ContentRef, ContractRef, Observational, _Contract
from .dependency_identity import content_identity
from .journal_protocol import advance, initial, owner_for, verify_receipt
from .operation_journal import (ConflictReport, EffectAttempt, EffectReceipt, ExpectedVersion,
    JournalEntry, OperationRequest, WriterBinding)
from .validation import canonical_json, parse_contract, verify_content_digest

POLICY = ContractRef(contract_id="passive-journal-recovery", version=1)
Text = Annotated[str, Field(max_length=1_048_576)]
State = Literal["NOT_STARTED", "PRE_EFFECT_DURABLE", "ATTEMPT_OUTCOME_UNCERTAIN",
    "EFFECT_CONFIRMED_DURABLE", "COMPLETED_DURABLE", "EFFECT_REJECTED_DURABLE",
    "CONFLICT", "CORRUPT_HISTORY", "UNSUPPORTED_VERSION", "SAFE_STOP"]


class StoredEntry(_Contract):
    revision: int
    body: Text


class DurableSnapshot(_Contract):
    expected: OperationRequest
    store_schema: int
    operation: Text | None
    owner: Text | None
    entries: Annotated[tuple[StoredEntry, ...], Field(max_length=33)]
    aggregate: Text | None
    effect_key: str | None
    attempt: Text | None
    payload_hex: Annotated[str | None, Field(max_length=131072)]
    receipt: Text | None
    conflicts: Annotated[tuple[Text, ...], Field(max_length=129)] = ()
    complete: bool = True
    owner_process: Literal["ACTIVE", "EXITED", "UNKNOWN"] = "UNKNOWN"
    provenance: ContentRef
    read_error: Literal["NONE", "UNREADABLE"] = "NONE"

    def identity(self):
        return content_identity("durable-journal-snapshot-v1", self)


class RecoveryAssessment(_Contract):
    snapshot: ContentRef
    request: ContentRef
    policy: ContractRef = POLICY
    state: State
    head: ContentRef | None
    receipt: ContentRef | None
    owner: WriterBinding | None
    ownership: Literal["UNOBSERVED", "UNBOUND", "BOUND_ACTIVE", "BOUND_EXITED", "BOUND_UNKNOWN", "INCONSISTENT"]
    passive_next_step: Literal["NONE", "OBSERVE_OUTCOME", "REVIEW_EXISTING_RECEIPT", "OPERATOR_REVIEW"]
    required_authority: Literal["NONE", "QUALIFIED_OBSERVATION_AND_HUMAN_RECOVERY"]
    diagnostics: tuple[str, ...]
    retry_admissible: bool = False
    takeover_admissible: bool = False
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False


def assess_recovery(snapshot: DurableSnapshot, *, policy: ContractRef = POLICY):
    s = parse_contract(DurableSnapshot, canonical_json(snapshot))
    r = s.expected
    head = receipt = owner = None
    ownership = "UNOBSERVED"

    def result(state, *diagnostics):
        step = "REVIEW_EXISTING_RECEIPT" if state == "EFFECT_CONFIRMED_DURABLE" else "OBSERVE_OUTCOME" if state == "ATTEMPT_OUTCOME_UNCERTAIN" else "NONE" if state in {"NOT_STARTED", "COMPLETED_DURABLE", "EFFECT_REJECTED_DURABLE"} else "OPERATOR_REVIEW"
        return RecoveryAssessment(snapshot=s.identity(), request=r.identity(), state=state,
            head=head.identity() if head else None, receipt=receipt.identity() if receipt else None,
            owner=owner, ownership=ownership, passive_next_step=step,
            required_authority="NONE" if step == "NONE" else "QUALIFIED_OBSERVATION_AND_HUMAN_RECOVERY",
            diagnostics=tuple(sorted(diagnostics)))

    if policy != POLICY or s.store_schema != 1:
        return result("UNSUPPORTED_VERSION", "unsupported_recovery_or_store_version")
    if not s.complete or s.read_error != "NONE":
        return result("SAFE_STOP", "incomplete_or_unreadable_snapshot")
    ownership = "UNBOUND"
    try:
        if s.aggregate is None:
            raise ValueError("aggregate_missing")
        aggregate = parse_contract(ExpectedVersion, s.aggregate)
        if (aggregate.store != r.expected.store or aggregate.aggregate != r.expected.aggregate
                or aggregate.scope != r.expected.scope):
            raise ValueError("aggregate_binding_mismatch")
        if s.operation is None:
            if s.owner is not None or s.entries or any(v is not None for v in (s.receipt, s.attempt, s.effect_key, s.payload_hex)) or s.conflicts:
                raise ValueError("orphaned_durable_evidence")
            return result("NOT_STARTED") if aggregate == r.expected else result("CONFLICT", "aggregate_version_conflict")
        request = parse_contract(OperationRequest, s.operation)
        if request != r:
            return result("CONFLICT", "request_identity_conflict")
        if not s.entries or len(s.entries) > 32:
            raise ValueError("missing_or_excessive_history")
        entries = tuple(parse_contract(JournalEntry, row.body) for row in s.entries)
        if entries[0] != initial(r) or any(row.revision != e.journal_version for row, e in zip(s.entries, entries)):
            raise ValueError("invalid_genesis_or_row_revision")
        if s.owner is not None:
            ownership = "INCONSISTENT"
            owner = parse_contract(WriterBinding, s.owner)
            if owner != owner_for(r, owner.writer):
                raise ValueError("owner_binding_mismatch")
            ownership = {"ACTIVE":"BOUND_ACTIVE", "EXITED":"BOUND_EXITED", "UNKNOWN":"BOUND_UNKNOWN"}[s.owner_process]
        if any(e.owner is not None and e.owner != owner for e in entries):
            ownership = "INCONSISTENT"
            raise ValueError("owner_history_mismatch")
        for a, b in zip(entries, entries[1:]):
            if b.transition is None or b.owner is None or advance(a, b.transition, b.owner) != b:
                raise ValueError("predecessor_chain_mismatch")
        head = entries[-1]
        for raw in s.conflicts:
            conflict = parse_contract(ConflictReport, raw)
            if conflict.operation_id != r.operation_id or conflict.observed_journal_version > head.journal_version:
                raise ValueError("conflict_audit_mismatch")
        if s.receipt is None and any(e.transition and e.transition.receipt is not None for e in entries):
            raise ValueError("journal_receipt_missing")
        effect_fields = (s.effect_key, s.attempt, s.payload_hex, s.receipt)
        if any(v is not None for v in effect_fields):
            if any(v is None for v in effect_fields) or owner is None:
                raise ValueError("partial_effect_record")
            receipt = parse_contract(EffectReceipt, s.receipt)
            attempt = parse_contract(EffectAttempt, s.attempt)
            if (s.effect_key != r.effect.effect_id or receipt.attempt != attempt
                    or not verify_content_digest(bytes.fromhex(s.payload_hex), r.effect.payload)):
                raise ValueError("foreign_or_corrupt_effect_record")
            verify_receipt(r, owner, receipt)
            if not any(e.stage == "EFFECT_ATTEMPTED" and e.transition.attempt == attempt for e in entries):
                raise ValueError("receipt_without_durable_attempt")
            if aggregate != receipt.observed:
                return result("CONFLICT", "aggregate_version_conflict")
        elif aggregate != r.expected:
            return result("CONFLICT", "aggregate_version_conflict")
        for e in entries:
            if e.transition and e.transition.receipt is not None and e.transition.receipt != receipt:
                raise ValueError("journal_receipt_missing_or_foreign")
        if head.stage == "COMPLETED":
            if receipt is None or receipt.outcome != "CONFIRMED":
                raise ValueError("completed_without_receipt")
            return result("COMPLETED_DURABLE")
        if receipt is not None:
            return result("EFFECT_CONFIRMED_DURABLE" if receipt.outcome == "CONFIRMED" else "EFFECT_REJECTED_DURABLE", "no_effect_replay")
        if head.stage in {"EFFECT_ATTEMPTED", "EFFECT_OUTCOME_UNKNOWN"}:
            return result("ATTEMPT_OUTCOME_UNCERTAIN", "absence_is_not_proof_of_no_effect")
        if head.stage == "CONFLICT":
            return result("CONFLICT", "durable_conflict")
        if head.stage == "SAFE_STOP":
            return result("SAFE_STOP", "durable_safe_stop")
        return result("PRE_EFFECT_DURABLE", "no_dispatch_permission")
    except (ValueError, TypeError, KeyError, RecursionError):
        return result("CORRUPT_HISTORY", "invalid_durable_binding_or_history")
