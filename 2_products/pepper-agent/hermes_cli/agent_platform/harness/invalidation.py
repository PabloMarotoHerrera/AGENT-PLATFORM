"""Joint identity comparison. Findings are obligations, never effect permits."""

from typing import Literal

from .contracts import AuthorityCurrentness, ContentRef, ContractRef, Observational, _Contract
from .dependency_identity import (DependencyContext, PriorPositiveDecision,
    SyntheticIdentityAssumption, checked_context)
from .dependency_manifest import DependencyManifest, POLICY, key, verify_manifest
from .validation import canonical_json, parse_contract

Change = Literal["UNCHANGED", "IMPLEMENTATION_CHANGED", "TRANSITIVE_DEPENDENCY_CHANGED",
    "VALIDATION_INPUT_CHANGED", "AUTHORITY_BINDING_CHANGED", "RESOURCE_BINDING_CHANGED",
    "INTENT_CHANGED", "POLICY_CHANGED", "HISTORICAL_SOURCE_CHANGED",
    "DEPENDENCY_CLOSURE_INCOMPLETE", "BROAD_FINGERPRINT_REQUIRED", "UNSUPPORTED_VERSION", "CONFLICT", "UNKNOWN"]
Consequence = Literal["NONE", "FRESH_EVIDENCE_REQUIRED", "FRESH_AUTHORITY_QUALIFICATION_REQUIRED",
    "HUMAN_REAUTHORIZATION_REQUIRED", "HISTORICAL_INTERPRETATION_RECHECK_REQUIRED",
    "EXECUTABILITY_NOT_ESTABLISHED", "BROAD_SOURCE_COMPARISON_REQUIRED", "SAFE_STOP"]


class InvalidationFinding(_Contract):
    cause: Change
    consequences: tuple[Consequence, ...]
    affected_capabilities: tuple[ContractRef, ...]
    changed_dependencies: tuple[ContractRef, ...] = ()


class JointIdentityAssessment(_Contract):
    expected: ContentRef
    candidate: ContentRef
    expected_manifest: ContentRef
    candidate_manifest: ContentRef
    findings: tuple[InvalidationFinding, ...]
    structurally_compatible: bool
    prior_positive_identity_matches: bool | None
    qualification_scope: Literal["UNQUALIFIED", "ISOLATED_SYNTHETIC_TEST_ONLY"]
    qualification_provenance: ContentRef | None
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False


def compare_identities(expected: DependencyContext, candidate: DependencyContext, *,
        expected_manifest: DependencyManifest, candidate_manifest: DependencyManifest,
        synthetic_assumption: SyntheticIdentityAssumption | None = None,
        prior_positive: PriorPositiveDecision | None = None) -> JointIdentityAssessment:
    a, b = checked_context(expected), checked_context(candidate)
    old = parse_contract(DependencyManifest, canonical_json(expected_manifest))
    new = parse_contract(DependencyManifest, canonical_json(candidate_manifest))
    reports = verify_manifest(old), verify_manifest(new)
    assumption = None if synthetic_assumption is None else parse_contract(SyntheticIdentityAssumption, canonical_json(synthetic_assumption))
    prior = None if prior_positive is None else parse_contract(PriorPositiveDecision, canonical_json(prior_positive))
    causes = {}
    cap = b.capability

    def note(cause, consequences, dependencies=()):
        record = causes.setdefault(cause, (set(), set()))
        record[0].update(consequences)
        record[1].update(dependencies)

    for context, manifest, report in ((a, old, reports[0]), (b, new, reports[1])):
        closure = next((c for c in report.capabilities if c.capability == context.capability and c.operation == context.operation), None)
        if context.manifest != manifest.identity() or context.policy != manifest.policy.policy:
            note("CONFLICT", ("SAFE_STOP",))
        if context.policy != POLICY or "unsupported_policy_version" in report.diagnostics:
            note("UNSUPPORTED_VERSION", ("SAFE_STOP",))
        if closure is None or closure.status != "COMPLETE_UNDER_SYNTHETIC_ASSUMPTIONS":
            note("DEPENDENCY_CLOSURE_INCOMPLETE", ("EXECUTABILITY_NOT_ESTABLISHED",))
            note("BROAD_FINGERPRINT_REQUIRED", ("BROAD_SOURCE_COMPARISON_REQUIRED",))
            if closure is None or (closure and closure.status in {"INCONSISTENT", "UNSUPPORTED"}):
                note("CONFLICT" if closure is None or closure.status == "INCONSISTENT" else "UNKNOWN", ("SAFE_STOP",))
        elif context.implementation.content != closure.implementation:
            note("CONFLICT", ("SAFE_STOP",))
        if context.unresolved:
            note("UNKNOWN", ("EXECUTABILITY_NOT_ESTABLISHED",))
        versions = context.expected_versions
        if len({r.contract_id for r in versions}) != len(versions):
            note("CONFLICT", ("SAFE_STOP",))
        known = {key(n.node) for n in manifest.nodes} | {key(context.capability), key(context.operation), key(context.policy)}
        known.update(key(v.source_contract) for v in (context.intent, context.authority, context.implementation, context.resource, *context.validation_inputs))
        if any(key(r) not in known for r in versions):
            note("UNSUPPORTED_VERSION", ("SAFE_STOP",))
    dimensions = (
        (a.intent, b.intent, "INTENT_CHANGED", ("HUMAN_REAUTHORIZATION_REQUIRED",)),
        (a.authority, b.authority, "AUTHORITY_BINDING_CHANGED", ("FRESH_AUTHORITY_QUALIFICATION_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED")),
        (a.implementation, b.implementation, "IMPLEMENTATION_CHANGED", ("FRESH_EVIDENCE_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED")),
        (a.validation_inputs, b.validation_inputs, "VALIDATION_INPUT_CHANGED", ("FRESH_EVIDENCE_REQUIRED",)),
        ((a.resource, a.scope, a.workflow_context), (b.resource, b.scope, b.workflow_context), "RESOURCE_BINDING_CHANGED", ("HUMAN_REAUTHORIZATION_REQUIRED", "FRESH_EVIDENCE_REQUIRED")),
        ((a.policy, old.policy), (b.policy, new.policy), "POLICY_CHANGED", ("HUMAN_REAUTHORIZATION_REQUIRED", "FRESH_EVIDENCE_REQUIRED")),
        (a.historical_source, b.historical_source, "HISTORICAL_SOURCE_CHANGED", ("HISTORICAL_INTERPRETATION_RECHECK_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED")),
        ((a.required_human_decision, a.expected_versions), (b.required_human_decision, b.expected_versions), "AUTHORITY_BINDING_CHANGED", ("FRESH_AUTHORITY_QUALIFICATION_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED")),
    )
    for left, right, cause, consequences in dimensions:
        if left != right:
            note(cause, consequences)
    if a.capability != b.capability or a.operation != b.operation:
        note("CONFLICT", ("SAFE_STOP",))
    if old.inventory.source_boundary != new.inventory.source_boundary:
        note("RESOURCE_BINDING_CHANGED", ("FRESH_AUTHORITY_QUALIFICATION_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED"))
    if old.manifest != new.manifest or old.inventory.inventory != new.inventory.inventory:
        note("POLICY_CHANGED", ("FRESH_AUTHORITY_QUALIFICATION_REQUIRED",))
    old_nodes, new_nodes = {key(n.node): n for n in old.nodes}, {key(n.node): n for n in new.nodes}
    for before in reports[0].capabilities:
        # Match by exact capability rather than ordering in the changed document.
        after = next((c for c in reports[1].capabilities if c.capability == before.capability), None)
        if after is None:
            if before.capability == cap:
                note("DEPENDENCY_CLOSURE_INCOMPLETE", ("SAFE_STOP",))
            continue
        if before.capability != cap:
            continue
        included = {key(r) for r in (*before.included, *after.included)}
        changed = tuple(sorted((new_nodes[k].node if k in new_nodes else old_nodes[k].node for k in included
                                if old_nodes.get(k) != new_nodes.get(k)), key=canonical_json))
        if changed or before.implementation != after.implementation:
            note("TRANSITIVE_DEPENDENCY_CHANGED", ("FRESH_EVIDENCE_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED"), changed)
            if any((new_nodes.get(key(r)) or old_nodes[key(r)]).kind == "POLICY" for r in changed):
                note("POLICY_CHANGED", ("FRESH_EVIDENCE_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED"), changed)
            if any((new_nodes.get(key(r)) or old_nodes[key(r)]).kind == "VALIDATION_INPUT" for r in changed):
                note("VALIDATION_INPUT_CHANGED", ("FRESH_EVIDENCE_REQUIRED",), changed)
            if any((new_nodes.get(key(r)) or old_nodes[key(r)]).kind == "EVIDENCE_SCHEMA" for r in changed):
                note("VALIDATION_INPUT_CHANGED", ("FRESH_EVIDENCE_REQUIRED",), changed)
            if any((new_nodes.get(key(r)) or old_nodes[key(r)]).kind == "RESOURCE_SCOPE" for r in changed):
                note("RESOURCE_BINDING_CHANGED", ("HUMAN_REAUTHORIZATION_REQUIRED", "FRESH_EVIDENCE_REQUIRED"), changed)
            if any((new_nodes.get(key(r)) or old_nodes[key(r)]).kind == "HISTORICAL_CONTRACT" for r in changed):
                note("HISTORICAL_SOURCE_CHANGED", ("HISTORICAL_INTERPRETATION_RECHECK_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED"), changed)
        if before.broad_source != after.broad_source:
            note("BROAD_FINGERPRINT_REQUIRED", ("BROAD_SOURCE_COMPARISON_REQUIRED", "HUMAN_REAUTHORIZATION_REQUIRED"))
    qualified = bool(assumption and assumption.subject == b.identity() and a.qualification == b.qualification == "SYNTHETIC_ASSUMPTION"
                     and a.currentness == b.currentness == AuthorityCurrentness.CURRENT)
    if not qualified or a.provenance != b.provenance:
        note("UNKNOWN", ("FRESH_AUTHORITY_QUALIFICATION_REQUIRED",))
    prior_matches = None if prior is None else prior.subject == b.identity() and not causes and qualified
    if prior is not None and not prior_matches:
        note("AUTHORITY_BINDING_CHANGED", ("FRESH_AUTHORITY_QUALIFICATION_REQUIRED",))
    if not causes:
        note("UNCHANGED", ("NONE",))
    findings = tuple(InvalidationFinding(cause=c, consequences=tuple(sorted(values[0])),
        affected_capabilities=(cap,), changed_dependencies=tuple(sorted(values[1], key=canonical_json))) for c, values in sorted(causes.items()))
    return JointIdentityAssessment(expected=a.identity(), candidate=b.identity(), expected_manifest=old.identity(), candidate_manifest=new.identity(),
        findings=findings, structurally_compatible=set(causes)=={"UNCHANGED"}, prior_positive_identity_matches=prior_matches,
        qualification_scope="ISOLATED_SYNTHETIC_TEST_ONLY" if qualified else "UNQUALIFIED",
        qualification_provenance=assumption.provenance if qualified else None)
