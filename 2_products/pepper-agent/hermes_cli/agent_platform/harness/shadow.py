"""Bounded observational comparisons; never permissions or dispatch instructions."""

from enum import Enum
import json
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .contracts import (
    ActorRef, ContentRef, ContinuationKind, ContractRef, Effect, Identifier,
    Observational, Scope, _Contract,
)
from .admissibility import AdmissionEvaluation, AdmissionInput, ConsentStatus
from .validation import canonical_json, sha256_bytes


class Category(str, Enum):
    PARITY = "PARITY"
    EXPECTED_QUALIFICATION_GAP = "EXPECTED_QUALIFICATION_GAP"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    UNSUPPORTED_OPERATION = "UNSUPPORTED_OPERATION"
    PUBLIC_MAPPING_MISMATCH = "PUBLIC_MAPPING_MISMATCH"
    AUTHORITY_SEMANTIC_MISMATCH = "AUTHORITY_SEMANTIC_MISMATCH"
    POLICY_SEMANTIC_MISMATCH = "POLICY_SEMANTIC_MISMATCH"
    STATE_PRECEDENCE_MISMATCH = "STATE_PRECEDENCE_MISMATCH"
    TARGET_IDENTITY_MISMATCH = "TARGET_IDENTITY_MISMATCH"
    CONTINUATION_KIND_MISMATCH = "CONTINUATION_KIND_MISMATCH"
    EFFECT_CLASSIFICATION_MISMATCH = "EFFECT_CLASSIFICATION_MISMATCH"
    LEGACY_OBSERVATION_INVALID = "LEGACY_OBSERVATION_INVALID"
    SHADOW_EVALUATION_INVALID = "SHADOW_EVALUATION_INVALID"
    UNEXPLAINED_DIFFERENCE = "UNEXPLAINED_DIFFERENCE"


class Provenance(str, Enum):
    EMPIRICAL = "EXECUTED_ISOLATED_LEGACY"
    HISTORICAL = "ACCEPTED_HISTORICAL_ASSERTION"
    STATIC = "STATIC_INTERPRETATION"
    SYNTHETIC = "SYNTHETIC_ASSUMPTION"


class PublicAction(_Contract):
    id: Annotated[str, Field(min_length=1, max_length=160)]
    label: Annotated[str, Field(max_length=240)]
    target_ticket_id: Identifier | None = None
    target_ticket_title: Annotated[str, Field(max_length=240)] | None = None
    required_human_action: Annotated[str, Field(max_length=160)] | None = None
    executable: bool | None = None
    read_only: bool | None = None

    def fields(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude={"schema_version"})


class DecisionView(_Contract):
    operation: Identifier
    capability: ContractRef | None
    policy: ContractRef | None
    actor: ActorRef
    scope: Scope
    current_ticket_id: Identifier | None
    next_ticket_id: Identifier | None = None
    target_ticket_id: Identifier | None
    decision_target: Identifier | None = None
    execution_target: Identifier | None = None
    separate_successor: PublicAction | None = None
    action: PublicAction | None = None
    mapping: Literal["MAPPED", "UNMAPPED", "UNSUPPORTED"]
    outcome: Literal["ALLOW", "WAIT", "DENY", "SAFE_STOP", "UNKNOWN"]
    continuation: ContinuationKind
    effect: Effect
    consent: ConsentStatus
    required_authority_kinds: Annotated[tuple[Identifier, ...], Field(max_length=32)]
    authority_version: Identifier
    source_version: ContentRef
    guards: Annotated[tuple[Identifier, ...], Field(max_length=64)] = ()
    active_execution: bool
    terminal: bool | None
    review_ready: bool | None


class LegacyObservation(_Contract):
    source: ContentRef
    snapshot: ContentRef
    provenance: Provenance
    authority_qualification: Literal["ASSERTED", "SYNTHETIC_TRUST_ASSUMPTION", "UNOBSERVED"] = "ASSERTED"
    view: DecisionView
    evidence: Annotated[tuple[ContentRef, ...], Field(max_length=64)] = ()
    unobservable: Annotated[tuple[Identifier, ...], Field(max_length=32)] = ()
    valid: bool = True


class HarnessObservation(_Contract):
    snapshot: ContentRef
    catalog: ContentRef
    adapter: ContractRef
    view: DecisionView
    admission_input: AdmissionInput | None
    evaluation: AdmissionEvaluation | None
    correspondence: ContentRef | None
    candidate_action: PublicAction | None = None
    translation_reason: Identifier = "not_translated"
    evidence: Annotated[tuple[ContentRef, ...], Field(max_length=64)] = ()
    unobservable: Annotated[tuple[Identifier, ...], Field(max_length=32)] = ()


class Difference(_Contract):
    field: Identifier
    legacy: Annotated[str, Field(max_length=4096)]
    harness: Annotated[str, Field(max_length=4096)]
    category: Category


class Comparison(_Contract):
    policy: ContractRef = ContractRef(contract_id="harness-shadow-comparison", version=1)
    legacy: ContentRef
    harness: ContentRef
    operation: Identifier
    target: Identifier | None
    legacy_outcome: Literal["ALLOW", "WAIT", "DENY", "SAFE_STOP", "UNKNOWN"]
    harness_outcome: Literal["ALLOW", "WAIT", "DENY", "SAFE_STOP", "UNKNOWN"]
    legacy_mapping: Literal["MAPPED", "UNMAPPED", "UNSUPPORTED"]
    harness_mapping: Literal["MAPPED", "UNMAPPED", "UNSUPPORTED"]
    legacy_continuation: ContinuationKind
    harness_continuation: ContinuationKind
    qualification: Literal["EXPLICIT_TRUST_ASSUMPTION", "UNQUALIFIED"]
    provenance: Provenance
    category: Category
    severity: Literal["INFORMATIONAL", "INCOMPLETE_QUALIFICATION", "INVESTIGATE", "SAFETY_CRITICAL"]
    reason_code: Identifier
    differences: Annotated[tuple[Difference, ...], Field(max_length=64)]
    unobservable: Annotated[tuple[Identifier, ...], Field(max_length=64)]
    observational: Observational = True
    grants_authority: Literal[False] = False
    effects: Literal["NONE"] = "NONE"

    def content_identity(self) -> ContentRef:
        return identity("shadow-comparison", Comparison.model_validate(self))


def identity(name: str, value: _Contract) -> ContentRef:
    # HAR-04 canonical JSON includes defaults. Bind the historically meaningful
    # public-field presence too, so absent and explicit null cannot share an
    # observation identity even though their canonical value JSON is identical.
    presence = []

    def visit(node, path):
        if isinstance(node, PublicAction):
            presence.append((path, sorted(node.fields())))
        elif isinstance(node, _Contract):
            for field in type(node).model_fields:
                visit(getattr(node, field), path + "." + field)
        elif isinstance(node, tuple):
            for index, child in enumerate(node):
                visit(child, path + "." + str(index))

    visit(value, "input")
    return ContentRef(content_id=name, sha256=sha256_bytes(
        (name + "-v1\0" + canonical_json(value) + "\0" + json.dumps(presence, separators=(",", ":"))).encode("utf-8")))


def compare(legacy: LegacyObservation, harness: HarnessObservation) -> Comparison:
    legacy = LegacyObservation.model_validate(legacy)
    harness = HarnessObservation.model_validate(harness)
    a, b = legacy.view, harness.view
    e = harness.evaluation
    qualification_withdrawal = (e is not None and e.qualification_issuer is None
        and b.outcome != "ALLOW" and harness.translation_reason in {
            "executable_offer_not_qualified", "blocked_offer_has_no_public_capability"})
    differences = []

    def difference(field, left, right, category):
        # repr preserves absent/null/false and is bounded by contract inputs.
        differences.append(Difference(field=field, legacy=repr(left)[:4096],
            harness=repr(right)[:4096], category=category))

    invalid = False
    v, e = harness.admission_input, harness.evaluation
    if (v is None) != (e is None):
        invalid = True
    if v is not None and e is not None:
        evaluation_identity = ContentRef(content_id="admission-evaluation-input", sha256=sha256_bytes(
            b"harness-admission-evaluation-v1\0" + canonical_json(e.context).encode("utf-8")))
        invalid = (e.context.source_input != v.content_identity() or e.input != evaluation_identity
            or harness.catalog != v.catalog_content or b.capability != e.decision.capability
            or b.operation != v.capability.capability.contract_id
            or b.policy != e.decision.policy or b.actor != v.actor or b.scope != v.scope
            or b.outcome != e.decision.outcome.value or b.continuation != e.continuations[0].kind
            or b.effect != v.effect or b.consent != v.consent
            or b.authority_version != v.authority_version or b.source_version != v.source_version
            or harness.correspondence != v.handler_evidence
            or e.handler_evidence != v.handler_evidence
            or e.decision.actor != v.actor or e.decision.scope != v.scope
            or e.decision.expected_authority_version != v.authority_version
            or e.decision.effect != v.effect or e.continuations[0].actor != v.actor
            or e.continuations[0].scope != v.scope
            or b.required_authority_kinds != v.policy.required_authority_kinds)
        if b.outcome == "ALLOW":
            q = e.context.qualification
            invalid = invalid or (q is None or e.qualification_issuer is None
                or q.input != v.content_identity() or q.issuer != e.context.trusted_issuer
                or e.qualification_issuer != q.issuer or q.handler_evidence != v.handler_evidence)
        if b.action and b.action.executable is True and (
                e.decision.outcome.value != "ALLOW" or e.qualification_issuer is None
                or e.context.qualification is None or harness.correspondence is None):
            invalid = True
    elif not (b.capability is None and b.continuation in {
            ContinuationKind.SAFE_STOP, ContinuationKind.EXTERNAL_REMEDIATION}):
        invalid = b.mapping != "UNSUPPORTED"
    if v is None:
        # Generic typed diagnostics/unsupported observations have no invocable
        # binding. Product adapters own their names and expected diagnostic kind.
        invalid = invalid or b.capability is not None or b.continuation == ContinuationKind.EXECUTABLE_CAPABILITY or bool(
            b.action and b.action.executable is True) or harness.correspondence is not None
    if not legacy.valid:
        difference("legacy_valid", False, True, Category.LEGACY_OBSERVATION_INVALID)
    if invalid:
        difference("evaluation_binding", "current_input", "invalid_or_replayed", Category.SHADOW_EVALUATION_INVALID)
    if legacy.snapshot != harness.snapshot:
        difference("snapshot", legacy.snapshot, harness.snapshot, Category.INSUFFICIENT_EVIDENCE)
    categories = {
        "operation": Category.PUBLIC_MAPPING_MISMATCH, "capability": Category.PUBLIC_MAPPING_MISMATCH,
        "policy": Category.POLICY_SEMANTIC_MISMATCH, "actor": Category.AUTHORITY_SEMANTIC_MISMATCH,
        "scope": Category.AUTHORITY_SEMANTIC_MISMATCH,
        "current_ticket_id": Category.STATE_PRECEDENCE_MISMATCH,
        "next_ticket_id": Category.STATE_PRECEDENCE_MISMATCH,
        "target_ticket_id": Category.TARGET_IDENTITY_MISMATCH,
        "decision_target": Category.TARGET_IDENTITY_MISMATCH,
        "execution_target": Category.TARGET_IDENTITY_MISMATCH,
        "separate_successor": Category.STATE_PRECEDENCE_MISMATCH,
        "mapping": Category.PUBLIC_MAPPING_MISMATCH, "effect": Category.EFFECT_CLASSIFICATION_MISMATCH,
        "consent": Category.AUTHORITY_SEMANTIC_MISMATCH,
        "required_authority_kinds": Category.AUTHORITY_SEMANTIC_MISMATCH,
        "authority_version": Category.AUTHORITY_SEMANTIC_MISMATCH,
        "source_version": Category.AUTHORITY_SEMANTIC_MISMATCH,
        "guards": Category.POLICY_SEMANTIC_MISMATCH,
        "active_execution": Category.STATE_PRECEDENCE_MISMATCH,
        "terminal": Category.STATE_PRECEDENCE_MISMATCH, "review_ready": Category.STATE_PRECEDENCE_MISMATCH,
    }
    for field, category in categories.items():
        left, right = getattr(a, field), getattr(b, field)
        if left != right:
            if field == "mapping" and qualification_withdrawal and right == "UNSUPPORTED":
                category = Category.EXPECTED_QUALIFICATION_GAP
            if field in {"execution_target", "decision_target"} and qualification_withdrawal and right is None and left == a.target_ticket_id:
                category = Category.EXPECTED_QUALIFICATION_GAP
            difference(field, left, right, category)
    aa, bb = a.action.fields() if a.action else None, b.action.fields() if b.action else None
    qualified = e is not None and e.qualification_issuer is not None
    gap = e is not None and not qualified and b.outcome != "ALLOW"
    if aa != bb:
        # Only executability withdrawn due to missing qualification is an expected gap.
        stripped_a = {k: val for k, val in (aa or {}).items() if k not in {"executable", "read_only"}}
        stripped_b = {k: val for k, val in (bb or {}).items() if k not in {"executable", "read_only"}}
        category = Category.EXPECTED_QUALIFICATION_GAP if (gap and aa is not None and (
            (bb is not None and stripped_a == stripped_b and bb.get("executable") is not True)
            or (bb is None and qualification_withdrawal and harness.candidate_action is not None
                and aa == harness.candidate_action.fields()))) else Category.PUBLIC_MAPPING_MISMATCH
        difference("action", aa, bb, category)
    for field in ("outcome", "continuation"):
        if getattr(a, field) != getattr(b, field):
            difference(field, getattr(a, field), getattr(b, field), Category.EXPECTED_QUALIFICATION_GAP
                if gap else Category.CONTINUATION_KIND_MISMATCH if field == "continuation" else Category.POLICY_SEMANTIC_MISMATCH)
    if legacy.evidence != harness.evidence:
        difference("evidence", legacy.evidence, harness.evidence, Category.INSUFFICIENT_EVIDENCE)
    unobservable = tuple(sorted(set(legacy.unobservable + harness.unobservable)))
    if legacy.authority_qualification == "UNOBSERVED":
        unobservable = tuple(sorted(set(unobservable + ("legacy_authority_qualification",))))
    critical = [d for d in differences if d.category not in {
        Category.EXPECTED_QUALIFICATION_GAP, Category.INSUFFICIENT_EVIDENCE}]
    if critical:
        category, severity = critical[0].category, "SAFETY_CRITICAL"
    elif v is None and (a.mapping == "UNSUPPORTED" or b.mapping == "UNSUPPORTED"):
        category, severity = Category.UNSUPPORTED_OPERATION, "INCOMPLETE_QUALIFICATION"
    elif any(d.category == Category.INSUFFICIENT_EVIDENCE for d in differences) or unobservable:
        category, severity = Category.INSUFFICIENT_EVIDENCE, "INCOMPLETE_QUALIFICATION"
    elif gap:
        category, severity = Category.EXPECTED_QUALIFICATION_GAP, "INCOMPLETE_QUALIFICATION"
    else:
        category, severity = Category.PARITY, "INFORMATIONAL"
    return Comparison(legacy=identity("legacy-observation", legacy), harness=identity("harness-observation", harness),
        operation=a.operation, target=a.target_ticket_id, legacy_outcome=a.outcome, harness_outcome=b.outcome,
        legacy_mapping=a.mapping, harness_mapping=b.mapping,
        legacy_continuation=a.continuation, harness_continuation=b.continuation,
        qualification="EXPLICIT_TRUST_ASSUMPTION" if qualified else "UNQUALIFIED",
        provenance=legacy.provenance, category=category, severity=severity, reason_code=category.value.lower(),
        differences=tuple(differences), unobservable=unobservable)


class CorpusReport(_Contract):
    corpus: ContentRef
    adapter: ContractRef
    catalog: ContentRef
    policy: ContractRef = ContractRef(contract_id="harness-shadow-comparison", version=1)
    comparisons: Annotated[tuple[Comparison, ...], Field(min_length=1, max_length=256)]
    scenario_ids: Annotated[tuple[Identifier, ...], Field(min_length=1, max_length=256)]
    unresolved_producers: Annotated[tuple[Identifier, ...], Field(max_length=64)]
    limitations: Annotated[tuple[Identifier, ...], Field(min_length=1, max_length=32)]
    truncated: Literal[False] = False
    operationally_qualified: Literal[False] = False
    observational: Observational = True

    @model_validator(mode="after")
    def _cases(self):
        if len(self.comparisons) != len(self.scenario_ids) or len(set(self.scenario_ids)) != len(self.scenario_ids):
            raise ValueError("corpus_case_identity_mismatch")
        return self

    def counts(self) -> dict:
        return {c.value: sum(x.category == c for x in self.comparisons) for c in Category}

    def content_identity(self) -> ContentRef:
        return identity("shadow-corpus-report", CorpusReport.model_validate(self))
