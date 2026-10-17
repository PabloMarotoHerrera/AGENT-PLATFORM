"""Bounded declared closures, qualified only inside explicit synthetic assumptions.

Inventory facts are injected, not discovered. Traversal closure is distinct from
discovery completeness. Actual dynamic/runtime closures require broad fallback.
"""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .contracts import ContentRef, ContractRef, Identifier, Observational, _Contract
from .dependency_identity import content_identity
from .validation import canonical_json, parse_contract

Kind = Literal["EXECUTABLE_SOURCE", "SHARED_LIBRARY", "PARSER", "POLICY", "CONFIGURATION",
    "VALIDATION_INPUT", "EVIDENCE_SCHEMA", "RESOURCE_SCOPE", "HISTORICAL_CONTRACT",
    "DOCUMENTATION_CONSUMED", "DOCUMENTATION_PRESENTATION_ONLY", "UNKNOWN_DYNAMIC"]
ClosureStatus = Literal["COMPLETE_UNDER_SYNTHETIC_ASSUMPTIONS", "PARTIAL", "UNKNOWN_DYNAMIC",
    "BROAD_FALLBACK_REQUIRED", "INCONSISTENT", "UNSUPPORTED"]
POLICY = ContractRef(contract_id="harness-dependency-identity", version=1)


def key(ref):
    return ref.contract_id, ref.version


class DependencyNode(_Contract):
    node: ContractRef
    kind: Kind
    content: ContentRef
    source_key: Annotated[str, Field(min_length=1, max_length=512)]
    supported: bool = True


class DependencyEdge(_Contract):
    consumer: ContractRef
    dependency: ContractRef


class InventoryFact(_Contract):
    node: DependencyNode
    dependencies: Annotated[tuple[ContractRef, ...], Field(max_length=32)] = ()

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "dependencies", tuple(sorted(self.dependencies, key=canonical_json)))
        return self


class ConsumerScopeFact(_Contract):
    """Offline owner's behavioral scope fact, independent of manifest claims."""
    capability: ContractRef
    operation: ContractRef
    roots: Annotated[tuple[ContractRef, ...], Field(min_length=1, max_length=16)]
    consumption: Literal["BOUNDED", "FULL_TREE", "UNKNOWN"]

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "roots", tuple(sorted(self.roots, key=canonical_json)))
        return self


class SourceInventory(_Contract):
    inventory: ContractRef
    source_boundary: ContentRef
    facts: Annotated[tuple[InventoryFact, ...], Field(max_length=128)]
    consumers: Annotated[tuple[ConsumerScopeFact, ...], Field(max_length=16)] = ()
    discovery: Literal["DECLARED_ONLY", "BOUNDED_SYNTHETIC", "PARTIAL", "UNKNOWN_DYNAMIC", "BROAD_REQUIRED"]

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "facts", tuple(sorted(self.facts, key=canonical_json)))
        object.__setattr__(self, "consumers", tuple(sorted(self.consumers, key=canonical_json)))
        return self

    def identity(self):
        return content_identity("harness-source-inventory-v1", self)


class DiscoveryAssumption(_Contract):
    inventory: ContentRef
    source_boundary: ContentRef
    policy: ContractRef
    provenance: ContentRef
    scope: Literal["ISOLATED_SYNTHETIC_TEST_ONLY"]
    presentation_exclusion_justified: bool = False


class CapabilityRoot(_Contract):
    capability: ContractRef
    operation: ContractRef
    roots: Annotated[tuple[ContractRef, ...], Field(min_length=1, max_length=16)]
    consumes_full_tree: bool = False
    source_mode: Literal["NARROW_TRANSITIVE", "BROAD_TREE"] = "NARROW_TRANSITIVE"
    broad_source: ContentRef | None = None

    @model_validator(mode="after")
    def _order(self):
        object.__setattr__(self, "roots", tuple(sorted(self.roots, key=canonical_json)))
        return self


class DependencyPolicy(_Contract):
    policy: ContractRef = POLICY
    exclude_justified_presentation: bool = False


class DependencyManifest(_Contract):
    manifest: ContractRef
    policy: DependencyPolicy
    nodes: Annotated[tuple[DependencyNode, ...], Field(max_length=128)]
    edges: Annotated[tuple[DependencyEdge, ...], Field(max_length=512)]
    capabilities: Annotated[tuple[CapabilityRoot, ...], Field(max_length=16)]
    inventory: SourceInventory
    assumption: DiscoveryAssumption | None = None

    @model_validator(mode="after")
    def _order(self):
        for name in ("nodes", "edges", "capabilities"):
            object.__setattr__(self, name, tuple(sorted(getattr(self, name), key=canonical_json)))
        return self

    def identity(self):
        return content_identity("harness-dependency-manifest-v1", self)


class ClosureIdentity(_Contract):
    capability: ContractRef
    operation: ContractRef
    roots: tuple[ContractRef, ...]
    policy: DependencyPolicy
    nodes: tuple[DependencyNode, ...]
    edges: tuple[DependencyEdge, ...]
    broad_source: ContentRef | None


class CapabilityClosure(_Contract):
    capability: ContractRef
    operation: ContractRef
    status: ClosureStatus
    reachable: tuple[ContractRef, ...]
    included: tuple[ContractRef, ...]
    excluded_presentation: tuple[ContractRef, ...]
    implementation: ContentRef | None
    broad_source: ContentRef | None
    reasons: tuple[Identifier, ...]


class ManifestReport(_Contract):
    manifest: ContentRef
    policy: ContractRef
    node_count: int
    edge_count: int
    traversal_order: tuple[ContractRef, ...]
    cycle_witness: tuple[ContractRef, ...]
    diagnostics: Annotated[tuple[Identifier, ...], Field(max_length=64)]
    capabilities: tuple[CapabilityClosure, ...]
    discovery_complete_under_assumptions: bool
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False


def verify_manifest(manifest: DependencyManifest) -> ManifestReport:
    m = parse_contract(DependencyManifest, canonical_json(manifest))
    errors = set()
    nodes = {key(n.node): n for n in m.nodes}
    facts = {key(f.node.node): f for f in m.inventory.facts}
    consumers = {key(c.capability): c for c in m.inventory.consumers}
    if len(nodes) != len(m.nodes) or len(facts) != len(m.inventory.facts):
        errors.add("duplicate_or_conflicting_node")
    if len({n.node.contract_id for n in m.nodes}) != len(nodes):
        errors.add("conflicting_node_versions")
    if len({key(c.capability) for c in m.capabilities}) != len(m.capabilities):
        errors.add("duplicate_capability")
    if len(consumers) != len(m.inventory.consumers):
        errors.add("duplicate_consumer_scope_fact")
    if not m.capabilities:
        errors.add("missing_capability_roots")
    if m.policy.policy != POLICY:
        errors.add("unsupported_policy_version")
    adjacency = {k: set() for k in nodes}
    edges = {(key(e.consumer), key(e.dependency)) for e in m.edges}
    if len(edges) != len(m.edges):
        errors.add("duplicate_edge")
    for parent, child in edges:
        if parent not in nodes or child not in nodes:
            errors.add("missing_dependency")
        else:
            adjacency[parent].add(child)
    # Inventory equality is independently checked, not inferred from reachability.
    if set(nodes) != set(facts):
        errors.add("source_inventory_omission")
    for k, fact in facts.items():
        if k not in nodes or nodes[k] != fact.node:
            errors.add("source_inventory_drift")
        if len(set(key(r) for r in fact.dependencies)) != len(fact.dependencies):
            errors.add("duplicate_inventory_dependency")
        declared = {child for parent, child in edges if parent == k}
        if declared != {key(r) for r in fact.dependencies}:
            errors.add("source_inventory_edge_mismatch")
        if fact.node.kind == "DOCUMENTATION_PRESENTATION_ONLY" and fact.dependencies:
            errors.add("presentation_has_behavioral_dependencies")
    visited, active, order, stack = set(), set(), [], []
    witness = []

    def visit(k):
        visited.add(k)
        active.add(k)
        stack.append(k)
        for child in sorted(adjacency[k]):
            if child in active:
                if not witness:
                    witness.extend(stack[stack.index(child):] + [child])
            elif child not in visited:
                visit(child)
        stack.pop()
        active.remove(k)
        order.append(nodes[k].node)

    for k in sorted(nodes):
        if k not in visited:
            visit(k)
    if witness:
        errors.add("dependency_cycle")
    assumption = m.assumption
    qualified = bool(assumption and m.inventory.discovery == "BOUNDED_SYNTHETIC"
        and assumption.inventory == m.inventory.identity() and assumption.source_boundary == m.inventory.source_boundary
        and assumption.policy == m.policy.policy)
    if assumption and not qualified:
        errors.add("stale_or_mismatched_discovery_assumption")
    closures = []
    for cap in m.capabilities:
        reasons = set(errors)
        scope_fact = consumers.get(key(cap.capability))
        scope_known = bool(scope_fact and scope_fact.operation == cap.operation and scope_fact.roots == cap.roots
                           and scope_fact.consumption != "UNKNOWN")
        if not scope_known:
            reasons.add("consumer_scope_unqualified")
        if scope_fact and (scope_fact.operation != cap.operation or scope_fact.roots != cap.roots
                          or (scope_fact.consumption != "UNKNOWN" and cap.consumes_full_tree != (scope_fact.consumption == "FULL_TREE"))):
            reasons.add("consumer_scope_conflict")
        if len(set(key(r) for r in cap.roots)) != len(cap.roots):
            reasons.add("duplicate_root")
        if cap.broad_source is not None and cap.source_mode == "NARROW_TRANSITIVE" and not cap.consumes_full_tree:
            reasons.add("unexpected_broad_source_binding")
        reachable = set()
        pending = [key(r) for r in cap.roots]
        while pending:
            k = pending.pop()
            if k in reachable:
                continue
            if k not in nodes:
                reasons.add("missing_root_or_version")
                continue
            reachable.add(k)
            pending.extend(sorted(adjacency[k], reverse=True))
        dynamic = any(nodes[k].kind == "UNKNOWN_DYNAMIC" for k in reachable)
        unsupported = any(not nodes[k].supported for k in reachable)
        broad_required = cap.consumes_full_tree or cap.source_mode == "BROAD_TREE" or m.inventory.discovery == "BROAD_REQUIRED" or not scope_known or (scope_fact is not None and scope_fact.consumption == "FULL_TREE")
        if cap.consumes_full_tree and cap.source_mode != "BROAD_TREE":
            reasons.add("broad_consumer_cannot_be_narrowed")
        if broad_required and cap.broad_source is None:
            reasons.add("broad_fingerprint_missing")
        if dynamic:
            reasons.add("unknown_dynamic_dependency")
        if unsupported:
            reasons.add("unsupported_dependency")
        if not qualified:
            reasons.add("discovery_incomplete")
        if errors or reasons & {"missing_root_or_version", "broad_consumer_cannot_be_narrowed", "broad_fingerprint_missing", "duplicate_root", "unexpected_broad_source_binding", "consumer_scope_conflict"}:
            status = "INCONSISTENT"
        elif unsupported:
            status = "UNSUPPORTED"
        elif dynamic or m.inventory.discovery == "UNKNOWN_DYNAMIC":
            status = "UNKNOWN_DYNAMIC"
        elif not qualified or not scope_known:
            status = "BROAD_FALLBACK_REQUIRED" if broad_required else "PARTIAL"
        else:
            status = "COMPLETE_UNDER_SYNTHETIC_ASSUMPTIONS"
        excluded = {k for k in reachable if nodes[k].kind == "DOCUMENTATION_PRESENTATION_ONLY"
            and m.policy.exclude_justified_presentation and qualified and assumption.presentation_exclusion_justified
            and scope_known and not broad_required}
        included = reachable - excluded
        identity = ClosureIdentity(capability=cap.capability, operation=cap.operation, roots=cap.roots,
            policy=m.policy, nodes=tuple(nodes[k] for k in sorted(included)),
            edges=tuple(sorted((e for e in m.edges if key(e.consumer) in included and key(e.dependency) in included), key=canonical_json)),
            broad_source=cap.broad_source if broad_required else None)
        closures.append(CapabilityClosure(capability=cap.capability, operation=cap.operation, status=status,
            reachable=tuple(nodes[k].node for k in sorted(reachable)), included=tuple(nodes[k].node for k in sorted(included)),
            excluded_presentation=tuple(nodes[k].node for k in sorted(excluded)),
            implementation=content_identity("harness-capability-implementation-v1", identity) if status == "COMPLETE_UNDER_SYNTHETIC_ASSUMPTIONS" else None,
            broad_source=cap.broad_source, reasons=tuple(sorted(reasons))))
    return ManifestReport(manifest=m.identity(), policy=m.policy.policy, node_count=len(nodes), edge_count=len(edges),
        traversal_order=tuple(order), cycle_witness=tuple(nodes[k].node for k in witness),
        diagnostics=tuple(sorted(errors)), capabilities=tuple(sorted(closures, key=lambda c: key(c.capability))),
        discovery_complete_under_assumptions=qualified and not errors and all(c.status == "COMPLETE_UNDER_SYNTHETIC_ASSUMPTIONS" for c in closures))
