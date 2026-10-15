"""Pure declarations, never tool registration, availability or admissibility.

Only transition.capability is owned/resolved here. Schema, policy, predicate,
adapter, evidence and recovery references are opaque external declarations.
"""

from enum import Enum
import hashlib
from typing import Annotated

from pydantic import Field, model_validator

from .contracts import CapabilityDescriptor, ContentRef, ContractRef, TransitionDescriptor, _Contract
from .validation import canonical_json, parse_contract

MAX_CAPABILITIES = 64
MAX_TRANSITIONS = 128
MAX_SNAPSHOT_BYTES = 900_000  # document plus digest stays below HAR-04 1 MiB


def _key(ref: ContractRef) -> tuple[str, int]:
    return ref.contract_id, ref.version


class LookupStatus(str, Enum):
    DECLARED = "DECLARED"
    NOT_DECLARED = "NOT_DECLARED"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    INVALID_REFERENCE = "INVALID_REFERENCE"
    CATALOG_INCONSISTENCY = "CATALOG_INCONSISTENCY"


class CatalogSnapshot(_Contract):
    catalog: ContractRef
    capabilities: Annotated[tuple[CapabilityDescriptor, ...], Field(max_length=MAX_CAPABILITIES)] = ()
    transitions: Annotated[tuple[TransitionDescriptor, ...], Field(max_length=MAX_TRANSITIONS)] = ()
    declaration_inputs: Annotated[tuple[ContentRef, ...], Field(max_length=16)] = ()

    @model_validator(mode="after")
    def _consistent(self) -> "CatalogSnapshot":
        if len({r.content_id for r in self.declaration_inputs}) != len(self.declaration_inputs):
            raise ValueError("duplicate_declaration_input")
        caps = {_key(c.capability): c for c in self.capabilities}
        if len(caps) != len(self.capabilities):
            raise ValueError("duplicate_or_conflicting_capability")
        if len({_key(t.transition) for t in self.transitions}) != len(self.transitions):
            raise ValueError("duplicate_or_conflicting_transition")
        for transition in self.transitions:
            capability = caps.get(_key(transition.capability))
            if capability is None:
                raise ValueError("undeclared_capability_reference")
            if transition.effect != capability.effect:
                raise ValueError("effect_mismatch")
            if not set(capability.required_authority_kinds) <= set(transition.required_authority_kinds):
                raise ValueError("authority_requirements_weakened")
        # Only entry order is normalized; descriptor-internal sequences retain
        # their HAR-04 semantics, including declared prerequisite order.
        object.__setattr__(self, "capabilities", tuple(sorted(self.capabilities, key=lambda c: _key(c.capability))))
        object.__setattr__(self, "transitions", tuple(sorted(self.transitions, key=lambda t: _key(t.transition))))
        object.__setattr__(self, "declaration_inputs", tuple(sorted(self.declaration_inputs,key=lambda r:r.content_id)))
        if len(self.model_dump_json().encode("utf-8")) > MAX_SNAPSHOT_BYTES:
            raise ValueError("catalog_transport_bound")
        return self

    def content_identity(self) -> ContentRef:
        raw = canonical_json(_validated(self)).encode("utf-8")
        return ContentRef(content_id=self.catalog.contract_id,
            sha256=hashlib.sha256(b"harness-catalog-snapshot-v1\0" + raw).hexdigest())

    def list_capabilities(self) -> tuple[CapabilityDescriptor, ...]:
        return _validated(self).capabilities

    def list_transitions(self) -> tuple[TransitionDescriptor, ...]:
        return _validated(self).transitions

    def resolve_capability(self, reference: object) -> "CatalogLookup":
        return _resolve(self, reference, False)

    def resolve_transition(self, reference: object) -> "CatalogLookup":
        return _resolve(self, reference, True)

    def transitions_for(self, reference: ContractRef) -> tuple[TransitionDescriptor, ...]:
        result = self.resolve_capability(reference)
        if result.status != LookupStatus.DECLARED:
            raise ValueError(result.status.value)
        return tuple(t for t in _validated(self).transitions if t.capability == reference)

    def external_references(self) -> tuple[ContractRef, ...]:
        snapshot = _validated(self)
        refs = []
        for cap in snapshot.capabilities:
            refs.extend((cap.input_schema, cap.output_schema, cap.evidence_contract, cap.execution_adapter))
            if cap.recovery_policy is not None:
                refs.append(cap.recovery_policy)
        for transition in snapshot.transitions:
            refs.extend((transition.source_requirement, transition.target_rule, transition.continuation_rule,
                         *transition.prerequisites))
        return tuple({_key(ref): ref for ref in sorted(refs, key=_key)}.values())


class CatalogDocument(_Contract):
    snapshot: CatalogSnapshot
    content: ContentRef

    @model_validator(mode="after")
    def _integrity(self) -> "CatalogDocument":
        if self.content != self.snapshot.content_identity():
            raise ValueError("catalog_content_digest_mismatch")
        return self


class CatalogLookup(_Contract):
    status: LookupStatus
    reference: ContractRef | None = None
    catalog_content: ContentRef | None = None
    capability: CapabilityDescriptor | None = None
    transition: TransitionDescriptor | None = None

    @model_validator(mode="after")
    def _result(self) -> "CatalogLookup":
        count = int(self.capability is not None) + int(self.transition is not None)
        if self.status == LookupStatus.DECLARED:
            if count != 1 or self.reference is None or self.catalog_content is None:
                raise ValueError("declared_lookup_requires_exact_descriptor_and_snapshot")
            actual = self.capability.capability if self.capability else self.transition.transition
            if actual != self.reference:
                raise ValueError("lookup_reference_mismatch")
        elif count:
            raise ValueError("failed_lookup_cannot_publish_descriptor")
        return self


def _validated(snapshot: CatalogSnapshot) -> CatalogSnapshot:
    if not isinstance(snapshot, CatalogSnapshot):
        raise TypeError("expected CatalogSnapshot")
    snapshot = CatalogSnapshot.model_validate(snapshot)
    return parse_contract(CatalogSnapshot, snapshot.model_dump_json())


def build_catalog(catalog: ContractRef, capabilities: tuple[CapabilityDescriptor, ...] = (),
                  transitions: tuple[TransitionDescriptor, ...] = (),
                  declaration_inputs: tuple[ContentRef, ...] = ()) -> CatalogSnapshot:
    return CatalogSnapshot(catalog=catalog, capabilities=capabilities, transitions=transitions,
                           declaration_inputs=declaration_inputs)


def serialize_catalog(snapshot: CatalogSnapshot) -> str:
    snapshot = _validated(snapshot)
    return canonical_json(CatalogDocument(snapshot=snapshot, content=snapshot.content_identity()))


def deserialize_catalog(data: str | bytes) -> CatalogSnapshot:
    return parse_contract(CatalogDocument, data).snapshot


def _resolve(snapshot: CatalogSnapshot, reference: object, transition: bool) -> CatalogLookup:
    try:
        snapshot = _validated(snapshot)
    except (ValueError, TypeError):
        return CatalogLookup(status=LookupStatus.CATALOG_INCONSISTENCY)
    identity = snapshot.content_identity()
    try:
        if not isinstance(reference, ContractRef):
            raise ValueError("exact ContractRef required")
        reference = ContractRef.model_validate(reference)
    except (ValueError, TypeError):
        return CatalogLookup(status=LookupStatus.INVALID_REFERENCE, catalog_content=identity)
    entries = snapshot.transitions if transition else snapshot.capabilities
    for entry in entries:
        actual = entry.transition if transition else entry.capability
        if actual == reference:
            return CatalogLookup(status=LookupStatus.DECLARED, reference=reference,
                catalog_content=identity, **({"transition": entry} if transition else {"capability": entry}))
    known_id = any((e.transition if transition else e.capability).contract_id == reference.contract_id for e in entries)
    return CatalogLookup(status=LookupStatus.UNSUPPORTED_VERSION if known_id else LookupStatus.NOT_DECLARED,
                         reference=reference, catalog_content=identity)
