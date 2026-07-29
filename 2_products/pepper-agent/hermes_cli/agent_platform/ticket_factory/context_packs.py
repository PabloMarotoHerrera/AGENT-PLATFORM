"""Deterministic in-memory Context Pack assembly for Pepper planning specs."""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import re
from typing import Annotated, Literal, NamedTuple, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    model_validator,
)

from hermes_cli.agent_platform.ticket_factory.specs import (
    AuthorityReferenceSpec,
    ProjectSpec,
    TicketSpec,
)

CONTEXT_PACK_SCHEMA_VERSION = 1
CONTEXT_PACK_DIGEST_ALGORITHM = "agent-platform-context-pack-sha256-v1"
TRUNCATION_MARKER = "\n[CONTEXT_TRUNCATED]"
MIN_TOTAL_TRUNCATION_BUDGET = 128
PROJECT_SPEC_SOURCE_ID = "CTX-PROJECT-SPEC"
TICKET_SPEC_SOURCE_ID = "CTX-TICKET-SPEC"
_RESERVED_SOURCE_IDS = frozenset({PROJECT_SPEC_SOURCE_ID, TICKET_SPEC_SOURCE_ID})
_ALLOWED_PLACEHOLDER_VALUES = frozenset({
    "<REDACTED>",
    "REDACTED",
    "<SECRET>",
    "synthetic-token",
    "synthetic-access-token",
    "synthetic-refresh-token",
})
_PRIVATE_KEY_MARKER = "-----BEGIN " + "PRIVATE KEY-----"
_OPENSSH_KEY_MARKER = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
_BEARER_PATTERN = re.compile(r"\bAuthorization\s*:\s*Bearer\s+([^\s]+)", re.IGNORECASE)
_OPENAI_SECRET_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")
_ACCESS_TOKEN_LABEL = "access_" + "token"
_REFRESH_TOKEN_LABEL = "refresh_" + "token"
_ASSIGNMENT_PATTERNS = (
    (
        _ACCESS_TOKEN_LABEL,
        re.compile(rf"\b{_ACCESS_TOKEN_LABEL}\s*=\s*([^\s&]+)", re.IGNORECASE),
    ),
    (
        _REFRESH_TOKEN_LABEL,
        re.compile(rf"\b{_REFRESH_TOKEN_LABEL}\s*=\s*([^\s&]+)", re.IGNORECASE),
    ),
)


class ContextPackAssemblyError(ValueError):
    """Base error for bounded context-pack assembly failures."""


class ContextPackBudgetError(ContextPackAssemblyError):
    """Raised when the explicit assembly policy cannot fit required content."""


class ContextPackSensitiveContentError(ContextPackAssemblyError):
    """Raised when sensitive source posture or secret-shaped markers are found."""


def _reject_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("text must not contain NUL characters")
    return value


def _reject_identifier_whitespace(value: object) -> object:
    if isinstance(value, str) and any(character.isspace() for character in value):
        raise ValueError("identifier must not contain whitespace")
    return value


ContextSourceIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=5,
        max_length=96,
        pattern=r"^CTX-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    ),
]
ContextTitle: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=256),
    AfterValidator(_reject_nul),
]
ContextReference: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1024),
    AfterValidator(_reject_nul),
]
ContextContent: TypeAlias = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=32768),
    AfterValidator(_reject_nul),
]
ContextDigest: TypeAlias = Annotated[
    str,
    StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$"),
]
_ProjectIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(min_length=2, max_length=5, pattern=r"^P[1-9][0-9]{0,3}$"),
]
_TicketIdentifier: TypeAlias = Annotated[
    str,
    BeforeValidator(_reject_identifier_whitespace),
    StringConstraints(
        min_length=4,
        max_length=64,
        pattern=r"^P[1-9][0-9]{0,3}(?:\.[A-Z0-9]+)+$",
    ),
]


class ContextSourceKind(str, Enum):
    PROJECT_SPEC = "project_spec"
    TICKET_SPEC = "ticket_spec"
    GOVERNANCE_RECORD = "governance_record"
    REPOSITORY_FILE = "repository_file"
    EXTERNAL_SOURCE = "external_source"
    HUMAN_INSTRUCTION = "human_instruction"
    HISTORICAL_TICKET = "historical_ticket"


class ContextSensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"
    SECRET = "secret"


class ContextPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class OptionalSourceOverflowStrategy(str, Enum):
    REJECT = "reject"
    TRUNCATE_THEN_OMIT = "truncate_then_omit"
    OMIT = "omit"


class _ContextPackModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
        str_strip_whitespace=True,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _deterministic_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _authority_reference_pairs(
    references: tuple[AuthorityReferenceSpec, ...],
) -> tuple[tuple[str, str], ...]:
    return tuple((reference.kind.value, reference.value) for reference in references)


def _reject_duplicate_authority_references(
    references: tuple[AuthorityReferenceSpec, ...],
) -> None:
    pairs = _authority_reference_pairs(references)
    if len(pairs) != len(frozenset(pairs)):
        raise ValueError(
            "authority_references must not contain duplicate kind/value pairs"
        )


def _reject_duplicate_values(values: tuple[str, ...], field_name: str) -> None:
    if len(values) != len(frozenset(values)):
        raise ValueError(f"{field_name} must not contain duplicate entries")


class ContextSourceSpec(_ContextPackModel):
    source_id: ContextSourceIdentifier
    kind: ContextSourceKind
    title: ContextTitle
    source_reference: ContextReference
    content: ContextContent
    authority_references: tuple[AuthorityReferenceSpec, ...] = ()
    sensitivity: ContextSensitivity = ContextSensitivity.INTERNAL
    priority: ContextPriority = ContextPriority.NORMAL
    required: StrictBool = False

    @model_validator(mode="after")
    def _validate_source(self) -> ContextSourceSpec:
        if self.source_id in _RESERVED_SOURCE_IDS:
            raise ValueError("reserved source identifiers are assembler-owned")
        if self.kind in {ContextSourceKind.PROJECT_SPEC, ContextSourceKind.TICKET_SPEC}:
            raise ValueError(
                "project_spec and ticket_spec source kinds are assembler-owned"
            )
        _reject_duplicate_authority_references(self.authority_references)
        return self


class ContextAssemblyPolicy(_ContextPackModel):
    max_items: int = Field(default=32, ge=2, le=66)
    max_total_characters: int = Field(default=65536, ge=4096, le=131072)
    max_item_characters: int = Field(default=16384, ge=256, le=32768)
    optional_overflow_strategy: OptionalSourceOverflowStrategy = (
        OptionalSourceOverflowStrategy.TRUNCATE_THEN_OMIT
    )

    @model_validator(mode="after")
    def _validate_policy(self) -> ContextAssemblyPolicy:
        if self.max_item_characters > self.max_total_characters:
            raise ValueError("max_item_characters must not exceed max_total_characters")
        return self


class ContextAssemblyRequest(_ContextPackModel):
    project_spec: ProjectSpec
    ticket_spec: TicketSpec
    sources: tuple[ContextSourceSpec, ...] = Field(default=(), max_length=64)
    policy: ContextAssemblyPolicy = Field(default_factory=ContextAssemblyPolicy)

    @model_validator(mode="after")
    def _validate_request(self) -> ContextAssemblyRequest:
        if self.project_spec.project_id != self.ticket_spec.project_id:
            raise ValueError(
                "project_spec and ticket_spec project identifiers must match"
            )
        source_ids = tuple(source.source_id for source in self.sources)
        _reject_duplicate_values(source_ids, "sources")
        kind_reference_pairs = tuple(
            (source.kind.value, source.source_reference) for source in self.sources
        )
        if len(kind_reference_pairs) != len(frozenset(kind_reference_pairs)):
            raise ValueError("sources must not contain duplicate kind/reference pairs")
        return self


class ContextPackItem(_ContextPackModel):
    source_id: ContextSourceIdentifier
    kind: ContextSourceKind
    title: ContextTitle
    source_reference: ContextReference
    authority_references: tuple[AuthorityReferenceSpec, ...]
    sensitivity: ContextSensitivity
    priority: ContextPriority
    required: StrictBool
    content: ContextContent
    original_character_count: int = Field(ge=0, le=32768)
    included_character_count: int = Field(ge=0, le=32768)
    truncated: StrictBool
    source_SHA256: ContextDigest
    included_SHA256: ContextDigest

    @model_validator(mode="after")
    def _validate_item(self) -> ContextPackItem:
        if self.included_character_count > self.original_character_count:
            raise ValueError("included_character_count must not exceed original count")
        if self.included_character_count != len(self.content):
            raise ValueError("included_character_count must match content length")
        if self.included_SHA256 != _sha256_text(self.content):
            raise ValueError("included_SHA256 must match included content")
        if self.truncated:
            if self.included_character_count >= self.original_character_count:
                raise ValueError("truncated items must include less than the original")
            if self.source_SHA256 == self.included_SHA256:
                raise ValueError(
                    "truncated items must have distinct source and included digests"
                )
        else:
            if self.included_character_count != self.original_character_count:
                raise ValueError("untruncated items must have equal counts")
            if self.source_SHA256 != self.included_SHA256:
                raise ValueError("untruncated items must have equal digests")
        _reject_duplicate_authority_references(self.authority_references)
        return self


class ContextPack(_ContextPackModel):
    schema_version: Literal[1] = CONTEXT_PACK_SCHEMA_VERSION
    project_id: _ProjectIdentifier
    ticket_id: _TicketIdentifier
    items: tuple[ContextPackItem, ...] = Field(min_length=2)
    omitted_source_ids: tuple[ContextSourceIdentifier, ...]
    truncated_source_ids: tuple[ContextSourceIdentifier, ...]
    total_included_characters: int = Field(ge=0, le=131072)
    policy: ContextAssemblyPolicy
    context_pack_SHA256: ContextDigest

    @model_validator(mode="after")
    def _validate_pack(self) -> ContextPack:
        if not self.ticket_id.startswith(f"{self.project_id}."):
            raise ValueError("ticket_id must use the project_id prefix")
        if self.items[0].source_id != PROJECT_SPEC_SOURCE_ID:
            raise ValueError("first context pack item must be CTX-PROJECT-SPEC")
        if self.items[1].source_id != TICKET_SPEC_SOURCE_ID:
            raise ValueError("second context pack item must be CTX-TICKET-SPEC")
        item_source_ids = tuple(item.source_id for item in self.items)
        _reject_duplicate_values(item_source_ids, "items")
        _reject_duplicate_values(self.omitted_source_ids, "omitted_source_ids")
        _reject_duplicate_values(self.truncated_source_ids, "truncated_source_ids")
        included = frozenset(item_source_ids)
        omitted = frozenset(self.omitted_source_ids)
        truncated = frozenset(self.truncated_source_ids)
        if included & omitted:
            raise ValueError("omitted source identifiers must not be included")
        if not truncated.issubset(included):
            raise ValueError("truncated source identifiers must be included")
        if truncated != frozenset(
            item.source_id for item in self.items if item.truncated
        ):
            raise ValueError("truncated_source_ids must match truncated items")
        total = sum(item.included_character_count for item in self.items)
        if self.total_included_characters != total:
            raise ValueError("total_included_characters must match items")
        expected_digest = _context_pack_digest(
            project_id=self.project_id,
            ticket_id=self.ticket_id,
            items=self.items,
            omitted_source_ids=self.omitted_source_ids,
            truncated_source_ids=self.truncated_source_ids,
            total_included_characters=self.total_included_characters,
            policy=self.policy,
        )
        if self.context_pack_SHA256 != expected_digest:
            raise ValueError(
                "context_pack_SHA256 must match context pack digest record"
            )
        return self


class _MaterializedSource(NamedTuple):
    source_id: str
    kind: ContextSourceKind
    title: str
    source_reference: str
    authority_references: tuple[AuthorityReferenceSpec, ...]
    sensitivity: ContextSensitivity
    priority: ContextPriority
    required: bool
    content: str


_PRIORITY_RANK = {
    ContextPriority.CRITICAL: 0,
    ContextPriority.HIGH: 1,
    ContextPriority.NORMAL: 2,
    ContextPriority.LOW: 3,
}
_CALLER_KIND_RANK = {
    ContextSourceKind.GOVERNANCE_RECORD: 0,
    ContextSourceKind.REPOSITORY_FILE: 1,
    ContextSourceKind.HUMAN_INSTRUCTION: 2,
    ContextSourceKind.HISTORICAL_TICKET: 3,
    ContextSourceKind.EXTERNAL_SOURCE: 4,
}


def _source_sort_key(
    source: ContextSourceSpec,
) -> tuple[int, int, int, str]:
    return (
        0 if source.required else 1,
        _PRIORITY_RANK[source.priority],
        _CALLER_KIND_RANK[source.kind],
        source.source_id,
    )


def _safe_error(message: str, source_id: str, category: str) -> str:
    return f"{message}: source_id={source_id}; category={category}"


def _validate_content_safety(source_id: str, content: str) -> None:
    if _PRIVATE_KEY_MARKER in content:
        raise ContextPackSensitiveContentError(
            _safe_error("secret-shaped marker rejected", source_id, "private_key")
        )
    if _OPENSSH_KEY_MARKER in content:
        raise ContextPackSensitiveContentError(
            _safe_error(
                "secret-shaped marker rejected", source_id, "openssh_private_key"
            )
        )
    bearer_match = _BEARER_PATTERN.search(content)
    if bearer_match and bearer_match.group(1) not in _ALLOWED_PLACEHOLDER_VALUES:
        raise ContextPackSensitiveContentError(
            _safe_error("secret-shaped marker rejected", source_id, "bearer_token")
        )
    for label, pattern in _ASSIGNMENT_PATTERNS:
        match = pattern.search(content)
        if match and match.group(1) not in _ALLOWED_PLACEHOLDER_VALUES:
            raise ContextPackSensitiveContentError(
                _safe_error("secret-shaped marker rejected", source_id, label)
            )
    if _OPENAI_SECRET_PATTERN.search(content):
        raise ContextPackSensitiveContentError(
            _safe_error("secret-shaped marker rejected", source_id, "openai_style_key")
        )


def _generated_project_source(project_spec: ProjectSpec) -> _MaterializedSource:
    content = _deterministic_json(project_spec.model_dump(mode="json"))
    return _MaterializedSource(
        source_id=PROJECT_SPEC_SOURCE_ID,
        kind=ContextSourceKind.PROJECT_SPEC,
        title=f"ProjectSpec {project_spec.project_id}",
        source_reference=f"ProjectSpec:{project_spec.project_id}",
        authority_references=project_spec.authority_references,
        sensitivity=ContextSensitivity.INTERNAL,
        priority=ContextPriority.CRITICAL,
        required=True,
        content=content,
    )


def _generated_ticket_source(ticket_spec: TicketSpec) -> _MaterializedSource:
    content = _deterministic_json(ticket_spec.model_dump(mode="json"))
    return _MaterializedSource(
        source_id=TICKET_SPEC_SOURCE_ID,
        kind=ContextSourceKind.TICKET_SPEC,
        title=f"TicketSpec {ticket_spec.ticket_id}",
        source_reference=f"TicketSpec:{ticket_spec.ticket_id}",
        authority_references=ticket_spec.authority_references,
        sensitivity=ContextSensitivity.INTERNAL,
        priority=ContextPriority.CRITICAL,
        required=True,
        content=content,
    )


def _caller_source(source: ContextSourceSpec) -> _MaterializedSource:
    if source.sensitivity in {ContextSensitivity.SENSITIVE, ContextSensitivity.SECRET}:
        raise ContextPackSensitiveContentError(
            _safe_error(
                "sensitive source rejected", source.source_id, source.sensitivity.value
            )
        )
    return _MaterializedSource(
        source_id=source.source_id,
        kind=source.kind,
        title=source.title,
        source_reference=source.source_reference,
        authority_references=source.authority_references,
        sensitivity=source.sensitivity,
        priority=source.priority,
        required=source.required,
        content=source.content,
    )


def _make_item(
    source: _MaterializedSource,
    *,
    included_content: str,
    truncated: bool,
) -> ContextPackItem:
    return ContextPackItem(
        source_id=source.source_id,
        kind=source.kind,
        title=source.title,
        source_reference=source.source_reference,
        authority_references=source.authority_references,
        sensitivity=source.sensitivity,
        priority=source.priority,
        required=source.required,
        content=included_content,
        original_character_count=len(source.content),
        included_character_count=len(included_content),
        truncated=truncated,
        source_SHA256=_sha256_text(source.content),
        included_SHA256=_sha256_text(included_content),
    )


def _required_budget_error(source: _MaterializedSource, category: str) -> None:
    raise ContextPackBudgetError(
        _safe_error(
            "required source exceeds assembly policy", source.source_id, category
        )
    )


def _optional_budget_error(source: _MaterializedSource, category: str) -> None:
    raise ContextPackBudgetError(
        _safe_error(
            "optional source exceeds assembly policy", source.source_id, category
        )
    )


def _include_required_source(
    *,
    source: _MaterializedSource,
    policy: ContextAssemblyPolicy,
    items: list[ContextPackItem],
    total_included: int,
) -> int:
    if len(items) + 1 > policy.max_items:
        _required_budget_error(source, "max_items")
    if len(source.content) > policy.max_item_characters:
        _required_budget_error(source, "max_item_characters")
    if total_included + len(source.content) > policy.max_total_characters:
        _required_budget_error(source, "max_total_characters")
    items.append(_make_item(source, included_content=source.content, truncated=False))
    return total_included + len(source.content)


def _truncate_optional_content(content: str, character_limit: int) -> str | None:
    content_capacity = character_limit - len(TRUNCATION_MARKER)
    if content_capacity < 1:
        return None
    return f"{content[:content_capacity]}{TRUNCATION_MARKER}"


def _include_optional_source(
    *,
    source: _MaterializedSource,
    policy: ContextAssemblyPolicy,
    items: list[ContextPackItem],
    omitted_source_ids: list[str],
    truncated_source_ids: list[str],
    total_included: int,
) -> int:
    strategy = policy.optional_overflow_strategy
    if len(items) + 1 > policy.max_items:
        if strategy is OptionalSourceOverflowStrategy.REJECT:
            _optional_budget_error(source, "max_items")
        omitted_source_ids.append(source.source_id)
        return total_included

    remaining_total = policy.max_total_characters - total_included
    source_length = len(source.content)
    if source_length <= policy.max_item_characters and source_length <= remaining_total:
        items.append(
            _make_item(source, included_content=source.content, truncated=False)
        )
        return total_included + source_length

    item_overflow = source_length > policy.max_item_characters
    if strategy is OptionalSourceOverflowStrategy.REJECT:
        _optional_budget_error(
            source,
            "max_item_characters" if item_overflow else "max_total_characters",
        )
    if strategy is OptionalSourceOverflowStrategy.OMIT:
        omitted_source_ids.append(source.source_id)
        return total_included
    if remaining_total < MIN_TOTAL_TRUNCATION_BUDGET:
        omitted_source_ids.append(source.source_id)
        return total_included

    character_limit = min(policy.max_item_characters, remaining_total)
    truncated_content = _truncate_optional_content(source.content, character_limit)
    if truncated_content is None:
        omitted_source_ids.append(source.source_id)
        return total_included
    items.append(_make_item(source, included_content=truncated_content, truncated=True))
    truncated_source_ids.append(source.source_id)
    return total_included + len(truncated_content)


def _context_pack_digest(
    *,
    project_id: str,
    ticket_id: str,
    items: tuple[ContextPackItem, ...],
    omitted_source_ids: tuple[str, ...],
    truncated_source_ids: tuple[str, ...],
    total_included_characters: int,
    policy: ContextAssemblyPolicy,
) -> str:
    record = {
        "algorithm": CONTEXT_PACK_DIGEST_ALGORITHM,
        "schema_version": CONTEXT_PACK_SCHEMA_VERSION,
        "project_id": project_id,
        "ticket_id": ticket_id,
        "items": [
            {
                "source_id": item.source_id,
                "kind": item.kind.value,
                "title": item.title,
                "source_reference": item.source_reference,
                "authority_references": [
                    reference.model_dump(mode="json")
                    for reference in item.authority_references
                ],
                "sensitivity": item.sensitivity.value,
                "priority": item.priority.value,
                "required": item.required,
                "original_character_count": item.original_character_count,
                "included_character_count": item.included_character_count,
                "truncated": item.truncated,
                "source_SHA256": item.source_SHA256,
                "included_SHA256": item.included_SHA256,
            }
            for item in items
        ],
        "omitted_source_ids": list(omitted_source_ids),
        "truncated_source_ids": list(truncated_source_ids),
        "total_included_characters": total_included_characters,
        "policy": policy.model_dump(mode="json"),
    }
    return _sha256_text(_deterministic_json(record))


def assemble_context_pack(request: ContextAssemblyRequest) -> ContextPack:
    """Assemble one immutable context pack from explicit in-memory sources."""

    sorted_sources = tuple(sorted(request.sources, key=_source_sort_key))
    materialized_sources = (
        _generated_project_source(request.project_spec),
        _generated_ticket_source(request.ticket_spec),
        *tuple(_caller_source(source) for source in sorted_sources),
    )
    for source in materialized_sources:
        _validate_content_safety(source.source_id, source.content)

    items: list[ContextPackItem] = []
    omitted_source_ids: list[str] = []
    truncated_source_ids: list[str] = []
    total_included = 0
    policy = request.policy
    for source in materialized_sources:
        if source.required:
            total_included = _include_required_source(
                source=source,
                policy=policy,
                items=items,
                total_included=total_included,
            )
        else:
            total_included = _include_optional_source(
                source=source,
                policy=policy,
                items=items,
                omitted_source_ids=omitted_source_ids,
                truncated_source_ids=truncated_source_ids,
                total_included=total_included,
            )

    items_tuple = tuple(items)
    omitted_tuple = tuple(omitted_source_ids)
    truncated_tuple = tuple(truncated_source_ids)
    digest = _context_pack_digest(
        project_id=request.project_spec.project_id,
        ticket_id=request.ticket_spec.ticket_id,
        items=items_tuple,
        omitted_source_ids=omitted_tuple,
        truncated_source_ids=truncated_tuple,
        total_included_characters=total_included,
        policy=policy,
    )
    return ContextPack(
        project_id=request.project_spec.project_id,
        ticket_id=request.ticket_spec.ticket_id,
        items=items_tuple,
        omitted_source_ids=omitted_tuple,
        truncated_source_ids=truncated_tuple,
        total_included_characters=total_included,
        policy=policy,
        context_pack_SHA256=digest,
    )
