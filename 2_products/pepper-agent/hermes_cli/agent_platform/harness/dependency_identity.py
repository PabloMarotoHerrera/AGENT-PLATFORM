"""Independent identity domains. Integrity matching never authenticates an issuer."""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .contracts import (AuthorityCurrentness, ContentRef, ContractRef, Identifier,
                        Observational, Scope, _Contract)
from .validation import canonical_json, parse_contract, sha256_bytes
from .validation_dag import ValidationContext


class _IdentityRef(_Contract):
    content: ContentRef
    source_contract: ContractRef
    provenance: ContentRef


class HumanIntentRef(_IdentityRef):
    domain: Literal["human-intent-v1"] = "human-intent-v1"


class AuthorityBindingRef(_IdentityRef):
    domain: Literal["immutable-authority-v1"] = "immutable-authority-v1"


class ImplementationRef(_IdentityRef):
    domain: Literal["executable-implementation-v1"] = "executable-implementation-v1"


class ValidationInputRef(_IdentityRef):
    domain: Literal["validation-input-v1"] = "validation-input-v1"


class ResourceBindingRef(_IdentityRef):
    domain: Literal["resource-binding-v1"] = "resource-binding-v1"


def content_identity(domain: str, value: _Contract) -> ContentRef:
    """New domain-separated identity, using unchanged HAR-04 canonical transport."""
    return ContentRef(content_id=domain, sha256=sha256_bytes((domain + ":" + canonical_json(value)).encode()))


def bind_identity(model, value: _Contract, *, source_contract: ContractRef,
                  provenance: ContentRef):
    if model not in (HumanIntentRef, AuthorityBindingRef, ImplementationRef, ValidationInputRef, ResourceBindingRef):
        raise TypeError("explicit identity domain required")
    domain = model.model_fields["domain"].default
    return model(content=content_identity(domain, value), source_contract=source_contract, provenance=provenance)


class DependencyContext(_Contract):
    capability: ContractRef
    operation: ContractRef
    intent: HumanIntentRef
    authority: AuthorityBindingRef
    implementation: ImplementationRef
    validation_inputs: Annotated[tuple[ValidationInputRef, ...], Field(min_length=1, max_length=32)]
    resource: ResourceBindingRef
    scope: Scope
    workflow_context: ValidationContext
    policy: ContractRef
    manifest: ContentRef
    expected_versions: Annotated[tuple[ContractRef, ...], Field(max_length=32)] = ()
    historical_source: ContentRef | None = None
    required_human_decision: ContentRef | None = None
    provenance: ContentRef
    currentness: AuthorityCurrentness = AuthorityCurrentness.UNVERIFIED
    qualification: Literal["UNQUALIFIED", "SYNTHETIC_ASSUMPTION"] = "UNQUALIFIED"
    unresolved: Annotated[tuple[Identifier, ...], Field(max_length=64)] = ()

    @model_validator(mode="after")
    def _order(self):
        for name in ("validation_inputs", "expected_versions"):
            values = getattr(self, name)
            if len(set(canonical_json(v) for v in values)) != len(values):
                raise ValueError("duplicate identity/version reference")
            object.__setattr__(self, name, tuple(sorted(values, key=canonical_json)))
        object.__setattr__(self, "unresolved", tuple(sorted(set(self.unresolved))))
        return self

    def identity(self) -> ContentRef:
        return content_identity("harness-dependency-context-v1", self)


class SyntheticIdentityAssumption(_Contract):
    subject: ContentRef
    provenance: ContentRef
    scope: Literal["ISOLATED_SYNTHETIC_TEST_ONLY"]


class PriorPositiveDecision(_Contract):
    subject: ContentRef
    decision: ContentRef
    claim: Literal["ALLOW"]
    issuer: Identifier
    observational: Observational = True
    grants_authority: Literal[False] = False


def checked_context(context: DependencyContext) -> DependencyContext:
    return parse_contract(DependencyContext, canonical_json(context))
