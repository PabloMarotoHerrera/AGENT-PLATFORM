"""Pure observation vocabulary and injectable port; no storage or runtime imports.

Completeness is local to the explicitly bound source, never an authority chain.
Even a stable, structurally valid record is not current execution permission.
"""

from enum import Enum
from typing import Annotated, Literal, Protocol

from pydantic import Field, model_validator

from .contracts import (
    ActorRef, AuthorityCurrentness, AuthorityReference, ContentRef, ContractRef,
    Identifier, Observational, Scope, Version, _Contract,
)


class SourceKind(str, Enum):
    FACT = "FACT"
    AUTHORITY = "AUTHORITY"
    EVIDENCE = "EVIDENCE"


class ObservationStatus(str, Enum):
    ABSENT = "ABSENT"
    PRESENT = "PRESENT"
    INVALID = "INVALID"
    CONFLICT = "CONFLICT"
    UNSUPPORTED = "UNSUPPORTED"
    UNSTABLE = "UNSTABLE"
    UNAVAILABLE = "UNAVAILABLE"


class CheckStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"


class SourceRef(_Contract):
    source_id: Identifier
    kind: SourceKind
    format: ContractRef


class ObservationRequest(_Contract):
    source: SourceRef
    scope: Scope
    actor: ActorRef
    expected_content: ContentRef | None = None
    related_sources: Annotated[tuple[SourceRef, ...], Field(max_length=4)] = ()

    @model_validator(mode="after")
    def _identities(self) -> "ObservationRequest":
        ids = (self.source.source_id,) + tuple(s.source_id for s in self.related_sources)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate observation source")
        if self.expected_content and self.expected_content.content_id != self.source.source_id:
            raise ValueError("expected content must bind the requested source")
        return self


class ObservedRecord(_Contract):
    record_id: Identifier
    content: ContentRef
    state: Identifier | None = None


class Observation(_Contract):
    source: SourceRef
    scope: Scope
    actor: ActorRef
    status: ObservationStatus
    reason_code: Identifier
    source_content: ContentRef | None = None
    observed_schema_version: Version | None = None
    records: Annotated[tuple[ObservedRecord, ...], Field(max_length=32)] = ()
    authority: AuthorityReference | None = None
    integrity: CheckStatus = CheckStatus.UNVERIFIED
    structure: CheckStatus = CheckStatus.UNVERIFIED
    binding: CheckStatus = CheckStatus.UNVERIFIED
    consistency: Literal["UNRESOLVED", "STABLE_CAPTURE"] = "UNRESOLVED"
    completeness: Literal["INCOMPLETE", "BOUND_SOURCE_ONLY"] = "INCOMPLETE"
    currentness: Literal[AuthorityCurrentness.UNVERIFIED] = AuthorityCurrentness.UNVERIFIED
    observational: Observational = True

    @model_validator(mode="after")
    def _claims(self) -> "Observation":
        if self.source_content and self.source_content.content_id != self.source.source_id:
            raise ValueError("content/source identity mismatch")
        if len({r.record_id for r in self.records}) != len(self.records):
            raise ValueError("duplicate observed record")
        if self.status == ObservationStatus.PRESENT:
            if (self.source_content is None or self.consistency != "STABLE_CAPTURE"
                    or self.completeness != "BOUND_SOURCE_ONLY" or self.binding != CheckStatus.VERIFIED):
                raise ValueError("present observation requires a stable, explicitly bound source")
            if CheckStatus.FAILED in (self.integrity, self.structure):
                raise ValueError("present observation contradicts failed checks")
        elif self.authority is not None or self.records or self.completeness != "INCOMPLETE":
            raise ValueError("failed or absent observation cannot publish complete records")
        if self.integrity == CheckStatus.VERIFIED and self.source_content is None:
            raise ValueError("verified integrity requires content")
        if self.authority:
            if (self.source.kind != SourceKind.AUTHORITY or self.authority.scope != self.scope
                    or self.authority.subject != self.actor
                    or self.authority.currentness == AuthorityCurrentness.CURRENT):
                raise ValueError("observation cannot promote authority or change its bindings")
        return self


class ObservationPort(Protocol):
    """An injected reader, not a registry, initializer or execution gateway."""

    def observe_fact(self, request: ObservationRequest) -> Observation: ...

    def observe_authority(self, request: ObservationRequest) -> Observation: ...

    def observe_related(self, request: ObservationRequest) -> tuple[Observation, ...]: ...
