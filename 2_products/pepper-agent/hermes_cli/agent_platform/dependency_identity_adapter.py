"""Injected source facts and historical bytes, never active discovery or consent.

The existing Pepper runtime closure is not safely narrowable here. All actual
first-slice operations retain broad fallback, even with VERIFIED source bindings.
"""

import json
from typing import Annotated, Literal

from pydantic import Field

from .handler_correspondence import BindingEvidence, BindingStatus, inspect_correspondence
from .pre_review_catalog import product_operations
from .historical_validation_adapter import HistoricalValidationProjection
from .harness.contracts import ContentRef, ContractRef, Digest, Identifier, Observational, _Contract
from .harness.dependency_identity import content_identity
from .harness.dependency_manifest import (CapabilityRoot, DependencyEdge, DependencyManifest,
    DependencyPolicy, SourceInventory)
from .harness.validation import MAX_JSON_BYTES, _unique_object, canonical_json, parse_contract, sha256_bytes


class FirstSliceIdentityProjection(_Contract):
    manifest: DependencyManifest
    source_correspondences: tuple[BindingEvidence, ...]
    reasons: tuple[Identifier, ...]
    consumer_scope: Literal["UNKNOWN_REQUIRE_BROAD_COVERAGE"] = "UNKNOWN_REQUIRE_BROAD_COVERAGE"
    runtime_availability_established: Literal[False] = False
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False


def first_slice_manifest(inventory: SourceInventory, *, tool_source: bytes,
                         bindings: tuple[BindingEvidence, ...], broad_source: ContentRef) -> FirstSliceIdentityProjection:
    inventory = parse_contract(SourceInventory, canonical_json(inventory))
    broad_source = ContentRef.model_validate(broad_source)
    if type(bindings) is not tuple or len(bindings) > 32:
        raise ValueError("bounded explicit correspondence tuple required")
    proofs = tuple(parse_contract(BindingEvidence, canonical_json(b)) for b in bindings)
    if type(tool_source) is not bytes or len(tool_source) > 2_097_152:
        raise ValueError("bounded source bytes required")
    reasons = {"actual_runtime_closure_unqualified", "existing_broad_fingerprint_preserved", "static_binding_is_not_availability"}
    # The injected inventory retains all supplied facts/edges; no omission or
    # dynamic dependency is made complete by a passive product declaration.
    actual_inventory = SourceInventory.model_validate({**inventory.model_dump(), "discovery": "BROAD_REQUIRED"})
    roots = tuple(f.node.node for f in inventory.facts if f.node.source_key == "tools/pepper_workflow_tools.py")
    if len(roots) != 1:
        reasons.add("missing_or_ambiguous_entrypoint_source")
        roots = (ContractRef(contract_id="unresolved-hermes-entrypoint", version=1),)
    elif next(f for f in inventory.facts if f.node.node == roots[0]).node.content.sha256 != sha256_bytes(tool_source):
        reasons.add("source_inventory_correspondence_mismatch")
        roots = (ContractRef(contract_id="unresolved-hermes-entrypoint", version=1),)
    caps, fresh = [], []
    for operation in product_operations():
        matches = [p for p in proofs if p.declaration == operation.handler]
        expected = inspect_correspondence(tool_source, operation.handler)
        fresh.append(expected)
        if len(matches) != 1 or matches[0] != expected or expected.status != BindingStatus.VERIFIED:
            reasons.add("source_correspondence_unqualified")
            cap_roots = (ContractRef(contract_id="unqualified." + operation.capability.capability.contract_id, version=1),)
        else:
            cap_roots = roots
        # BROAD_TREE here is a conservative coverage obligation. It does not
        # assert that every invocation of every tool reads the complete tree.
        caps.append(CapabilityRoot(capability=operation.capability.capability,
            operation=operation.transition.transition, roots=cap_roots, consumes_full_tree=False,
            source_mode="BROAD_TREE", broad_source=broad_source))
    manifest = DependencyManifest(manifest=ContractRef(contract_id="pepper-first-slice-identity", version=1),
        policy=DependencyPolicy(), nodes=tuple(f.node for f in actual_inventory.facts),
        edges=tuple(DependencyEdge(consumer=f.node.node, dependency=d) for f in actual_inventory.facts for d in f.dependencies),
        capabilities=tuple(caps), inventory=actual_inventory)
    return FirstSliceIdentityProjection(manifest=manifest, source_correspondences=tuple(fresh), reasons=tuple(sorted(reasons)))


class HistoricalFieldObservation(_Contract):
    field: Identifier
    value_digest: Digest


class HistoricalIdentityProjection(_Contract):
    original_source: ContentRef
    original_schema: ContractRef
    compatibility_policy: ContractRef = ContractRef(contract_id="pepper-historical-identity-view", version=1)
    mapping: Literal["EXACT_SUPPORTED_REPRESENTATION", "PARTIAL_PROJECTION", "AMBIGUOUS_HISTORICAL_IDENTITY",
                     "UNSUPPORTED_SCHEMA", "INVALID_SOURCE", "CONFLICTING_VERSIONS", "BROADER_IDENTITY_FALLBACK_REQUIRED"]
    historical_algorithm_owner: ContractRef | None
    original_combined_identity: ContentRef | None
    observed_combined_fields: Annotated[tuple[HistoricalFieldObservation, ...], Field(max_length=64)]
    har10_mapping: Identifier | None = None
    unresolved: tuple[Identifier, ...]
    independently_verified_dimensions: Literal[False] = False
    original_digest_verified: Literal[False] = False
    observational: Observational = True
    grants_authority: Literal[False] = False
    authorizes_execution: Literal[False] = False

    def identity(self):
        return content_identity("harness-historical-identity-projection-v1", self)


_HISTORY = {
    "pepper-command-validation-record": ("pepper-pre-review-command-validation-v1", "binding", "record_SHA256"),
    "pepper-material-revision-request": ("pepper-post-execution-material-revision-v1", "request_binding", "material_revision_request_SHA256"),
    "pepper-material-revision-reconciliation": ("pepper-material-revision-authority-reconciliation-v1", "reconciliation_binding", "reconciliation_SHA256"),
}


def historical_identity(raw: bytes, *, source: ContentRef, original_schema: ContractRef,
        har10_projection: HistoricalValidationProjection | None = None) -> HistoricalIdentityProjection:
    source = ContentRef.model_validate(source)
    schema = ContractRef.model_validate(original_schema)
    h10 = None if har10_projection is None else parse_contract(HistoricalValidationProjection, canonical_json(har10_projection))

    def result(mapping, reasons, owner=None, combined=None, fields=()):
        return HistoricalIdentityProjection(original_source=source, original_schema=schema, mapping=mapping,
            historical_algorithm_owner=owner, original_combined_identity=combined,
            observed_combined_fields=fields, har10_mapping=h10.mapping if h10 else None,
            unresolved=tuple(sorted(reasons)))

    if type(raw) is not bytes or len(raw) > MAX_JSON_BYTES or sha256_bytes(raw) != source.sha256:
        return result("INVALID_SOURCE", ("invalid_source_bytes_or_digest",))
    definition = _HISTORY.get(schema.contract_id)
    if schema.version != 1 or definition is None:
        return result("UNSUPPORTED_SCHEMA", ("unsupported_historical_schema",))
    policy, binding_key, digest_key = definition
    try:
        body = json.loads(raw, object_pairs_hook=_unique_object)
        if not isinstance(body, dict):
            raise ValueError("expected object")
        if "schema_version" in body and (type(body["schema_version"]) is not int or body["schema_version"] != 1):
            return result("CONFLICTING_VERSIONS", ("conflicting_wire_version",))
        if body.get("policy_id") != policy or not isinstance(body.get(binding_key), dict):
            raise ValueError("unrecognized policy/binding")
        combined = ContentRef(content_id=digest_key, sha256=body[digest_key])
        binding = body[binding_key]
        if not binding or len(binding) > 64:
            raise ValueError("invalid combined binding")
        fields = tuple(HistoricalFieldObservation(field=k,
            value_digest=sha256_bytes(("historical-field-observation-v1:" + json.dumps(v, sort_keys=True,
                separators=(",", ":"), ensure_ascii=False, allow_nan=False)).encode())) for k, v in sorted(binding.items()))
    except (ValueError, TypeError, KeyError, RecursionError):
        return result("INVALID_SOURCE", ("invalid_historical_view",))
    reasons = {"historical_digest_owner_not_executed", "combined_binding_not_independent_signatures", "currentness_and_consent_unqualified"}
    if h10 and h10.mapping != "EXACT_COMPATIBLE":
        reasons.add("har10_ambiguity_or_incompleteness_retained")
    broad = "canonical_validation_source" in binding or "current_request_binding" in binding
    mapping = "BROADER_IDENTITY_FALLBACK_REQUIRED" if broad else "PARTIAL_PROJECTION"
    if h10 and h10.mapping == "AMBIGUOUS_HISTORICAL_SEMANTICS":
        mapping = "AMBIGUOUS_HISTORICAL_IDENTITY"
    return result(mapping, reasons, ContractRef(contract_id=policy, version=1), combined, fields)
