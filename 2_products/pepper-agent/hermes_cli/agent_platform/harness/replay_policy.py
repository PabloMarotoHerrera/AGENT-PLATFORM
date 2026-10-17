"""Passive replay/ownership advice; no operation is resumed or rewritten."""
from typing import Literal
from .contracts import ContentRef, Observational, _Contract
from .journal_recovery import RecoveryAssessment
from .operation_journal import OperationRequest
from .validation import canonical_json, parse_contract


class ReplayAssessment(_Contract):
    request: ContentRef
    reason: Literal["CONFLICTING_REQUEST", "OWNER_CONFLICT", "SAME_WRITER_NOT_AUTHENTICATED", "NO_REPLAY_PERMISSION"]
    retry_admissible: bool = False
    takeover_admissible: bool = False
    new_attempt_admissible: bool = False
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False


def assess_replay(recovery: RecoveryAssessment, proposed: OperationRequest, *, writer: str):
    a = parse_contract(RecoveryAssessment, canonical_json(recovery))
    r = parse_contract(OperationRequest, canonical_json(proposed))
    reason = "NO_REPLAY_PERMISSION"
    if r.identity() != a.request:
        reason = "CONFLICTING_REQUEST"
    elif a.owner is not None and a.owner.writer != writer:
        reason = "OWNER_CONFLICT"
    elif a.owner is not None:
        reason = "SAME_WRITER_NOT_AUTHENTICATED"
    return ReplayAssessment(request=r.identity(), reason=reason)
