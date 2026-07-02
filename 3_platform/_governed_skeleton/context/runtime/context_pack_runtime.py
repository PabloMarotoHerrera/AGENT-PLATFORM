"""I-03 minimal context pack metadata runtime boundary.

This module models context source references, context items, and context packs
in memory only. It does not load source contents, inspect local-only material,
copy product or external source, scan secrets, execute tools, call providers,
approve permissions, or imply readiness. Context inclusion is not permission.
Context inclusion is not source tracking. Validation evaluates; governance
decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class ContextSensitivity(str, Enum):
    """Declared sensitivity values for context metadata."""

    PUBLIC_METADATA = "public_metadata"
    GOVERNANCE_METADATA = "governance_metadata"
    SAFE_SUMMARY = "safe_summary"
    LOCAL_ONLY = "local_only"
    GENERATED_SENSITIVE = "generated_sensitive"
    SECRET = "secret"
    CREDENTIAL = "credential"
    RAW_PRODUCT_SOURCE = "raw_product_source"
    RAW_EXTERNAL_SOURCE = "raw_external_source"
    DATASET = "dataset"
    MODEL = "model"
    ARTIFACT = "artifact"
    UNKNOWN = "unknown"


class ContextSourceType(str, Enum):
    """Declared source types for context references."""

    GOVERNANCE_DOCUMENT = "governance_document"
    ARCHITECTURE_RECORD = "architecture_record"
    VALIDATION_RECORD = "validation_record"
    SECURITY_DECISION = "security_decision"
    PRODUCT_GOVERNANCE = "product_governance"
    IMPLEMENTATION_RECORD = "implementation_record"
    EXTERNAL_METADATA = "external_metadata"
    MIGRATION_METADATA = "migration_metadata"
    SAFE_SUMMARY = "safe_summary"
    UNKNOWN = "unknown"


class ContextItemStatus(str, Enum):
    """Context item statuses for metadata-only review."""

    DRAFT = "draft"
    CANDIDATE = "candidate"
    INCLUDED_FOR_REVIEW = "included_for_review"
    BLOCKED = "blocked"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    NEEDS_REVIEW = "needs_review"


class ContextPackStatus(str, Enum):
    """Context pack statuses for metadata-only assembly."""

    DRAFT = "draft"
    ASSEMBLED_FOR_REVIEW = "assembled_for_review"
    BLOCKED = "blocked"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    NEEDS_REVIEW = "needs_review"


CONTEXT_INCLUSION_IS_NOT_PERMISSION = "context inclusion is not permission"
CONTEXT_INCLUSION_IS_NOT_SOURCE_TRACKING = "context inclusion is not source tracking"
CONTEXT_INCLUSION_IS_NOT_MIGRATION = "context inclusion is not migration"
ASSEMBLED_FOR_REVIEW_IS_NOT_GOVERNANCE_APPROVAL = (
    "assembled_for_review is not governance approval"
)
ALLOWED_FOR_CONTEXT_IS_NOT_SOURCE_TRACKING_APPROVAL = (
    "allowed_for_context is not source tracking approval"
)
EVIDENCE_REFS_ARE_METADATA_ONLY = "evidence_refs are metadata references only"

BLOCKED_SENSITIVITIES = {
    ContextSensitivity.SECRET.value,
    ContextSensitivity.CREDENTIAL.value,
    ContextSensitivity.RAW_PRODUCT_SOURCE.value,
    ContextSensitivity.RAW_EXTERNAL_SOURCE.value,
}

REVIEW_SENSITIVITIES = {
    ContextSensitivity.LOCAL_ONLY.value,
    ContextSensitivity.GENERATED_SENSITIVE.value,
    ContextSensitivity.DATASET.value,
    ContextSensitivity.MODEL.value,
    ContextSensitivity.ARTIFACT.value,
    ContextSensitivity.UNKNOWN.value,
}

REVIEW_ITEM_STATUSES = {
    ContextItemStatus.BLOCKED.value,
    ContextItemStatus.REJECTED_FOR_SCOPE.value,
    ContextItemStatus.NEEDS_REVIEW.value,
}

REVIEW_PACK_STATUSES = {
    ContextPackStatus.BLOCKED.value,
    ContextPackStatus.REJECTED_FOR_SCOPE.value,
    ContextPackStatus.NEEDS_REVIEW.value,
}


def _value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    return value


def _tuple_of_strings(values: object) -> object:
    if isinstance(values, str):
        return values
    try:
        return tuple(values)
    except TypeError:
        return values


@dataclass(frozen=True)
class ContextSourceRef:
    """Metadata-only reference to a possible context source."""

    source_id: str
    source_type: str
    title: str
    reference: str
    sensitivity: str
    allowed_for_context: bool = False
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_type", _value(self.source_type))
        object.__setattr__(self, "sensitivity", _value(self.sensitivity))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class ContextItem:
    """Metadata-only context item containing a safe summary."""

    item_id: str
    source_id: str
    target_id: str
    claim: str
    summary: str
    sensitivity: str
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    status: str = ContextItemStatus.DRAFT.value
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "sensitivity", _value(self.sensitivity))
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


@dataclass(frozen=True)
class ContextPack:
    """Metadata-only context pack containing context item IDs."""

    pack_id: str
    target_id: str
    purpose: str
    item_ids: Sequence[str] = field(default_factory=tuple)
    status: str = ContextPackStatus.DRAFT.value
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_by: str = ""
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "item_ids", _tuple_of_strings(self.item_ids))
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


class ContextPackRuntime:
    """In-memory context metadata runtime only."""

    def __init__(self) -> None:
        self._sources: Dict[str, ContextSourceRef] = {}
        self._items: Dict[str, ContextItem] = {}
        self._packs: Dict[str, ContextPack] = {}

    def register_source_ref(self, source_ref: ContextSourceRef) -> ContextSourceRef:
        errors = self.validate_source_ref(source_ref)
        if errors:
            raise ValueError("; ".join(errors))
        if source_ref.source_id in self._sources:
            raise ValueError(f"duplicate source_id: {source_ref.source_id}")
        self._sources[source_ref.source_id] = source_ref
        return source_ref

    def create_context_item(self, item: ContextItem) -> ContextItem:
        errors = self.validate_context_item(item)
        if item.source_id not in self._sources:
            errors.append(f"source_id is not registered: {item.source_id}")
        if errors:
            raise ValueError("; ".join(errors))
        if item.item_id in self._items:
            raise ValueError(f"duplicate item_id: {item.item_id}")
        self._items[item.item_id] = item
        return item

    def create_context_pack(self, pack: ContextPack) -> ContextPack:
        errors = self.validate_context_pack(pack)
        for item_id in _iter_strings(pack.item_ids):
            if item_id not in self._items:
                errors.append(f"item_id is not registered: {item_id}")
            else:
                errors.extend(_validate_pack_item_eligibility(self._items[item_id]))
        if errors:
            raise ValueError("; ".join(errors))
        if pack.pack_id in self._packs:
            raise ValueError(f"duplicate pack_id: {pack.pack_id}")
        self._packs[pack.pack_id] = pack
        return pack

    def add_item_to_pack(self, pack_id: str, item_id: str) -> ContextPack:
        pack = self._packs.get(pack_id)
        if pack is None:
            raise ValueError(f"pack_id is not registered: {pack_id}")
        if item_id not in self._items:
            raise ValueError(f"item_id is not registered: {item_id}")
        eligibility_errors = _validate_pack_item_eligibility(self._items[item_id])
        if eligibility_errors:
            raise ValueError("; ".join(eligibility_errors))
        if item_id in pack.item_ids:
            return pack
        updated = ContextPack(
            pack_id=pack.pack_id,
            target_id=pack.target_id,
            purpose=pack.purpose,
            item_ids=tuple(pack.item_ids) + (item_id,),
            status=pack.status,
            limitations=pack.limitations,
            blockers=pack.blockers,
            created_by=pack.created_by,
            created_at=pack.created_at,
            review_required=pack.review_required,
        )
        errors = self.validate_context_pack(updated)
        if errors:
            raise ValueError("; ".join(errors))
        self._packs[pack_id] = updated
        return updated

    def get_source_ref(self, source_id: str) -> Optional[ContextSourceRef]:
        return self._sources.get(source_id)

    def get_context_item(self, item_id: str) -> Optional[ContextItem]:
        return self._items.get(item_id)

    def get_context_pack(self, pack_id: str) -> Optional[ContextPack]:
        return self._packs.get(pack_id)

    def list_source_refs(self) -> List[ContextSourceRef]:
        return list(self._sources.values())

    def list_context_items(self) -> List[ContextItem]:
        return list(self._items.values())

    def list_context_packs(self) -> List[ContextPack]:
        return list(self._packs.values())

    def list_context_items_by_target(self, target_id: str) -> List[ContextItem]:
        return [item for item in self._items.values() if item.target_id == target_id]

    @staticmethod
    def validate_source_ref(source_ref: ContextSourceRef) -> List[str]:
        if not isinstance(source_ref, ContextSourceRef):
            return ["source_ref must be a ContextSourceRef"]
        errors: List[str] = []
        required_text = {
            "source_id": source_ref.source_id,
            "source_type": source_ref.source_type,
            "title": source_ref.title,
            "reference": source_ref.reference,
            "sensitivity": source_ref.sensitivity,
            "created_at": source_ref.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("source_type", source_ref.source_type, ContextSourceType))
        errors.extend(_validate_allowed("sensitivity", source_ref.sensitivity, ContextSensitivity))
        errors.extend(_validate_string_sequence("limitations", source_ref.limitations))
        errors.extend(_validate_string_sequence("blockers", source_ref.blockers))
        if not isinstance(source_ref.allowed_for_context, bool):
            errors.append("allowed_for_context must be a boolean")
        if source_ref.sensitivity in BLOCKED_SENSITIVITIES:
            errors.append("blocked sensitivity cannot be registered for context")
        if source_ref.sensitivity in REVIEW_SENSITIVITIES and source_ref.allowed_for_context:
            errors.append("review sensitivity cannot be allowed_for_context by default")
        return errors

    @staticmethod
    def validate_context_item(item: ContextItem) -> List[str]:
        if not isinstance(item, ContextItem):
            return ["item must be a ContextItem"]
        errors: List[str] = []
        required_text = {
            "item_id": item.item_id,
            "source_id": item.source_id,
            "target_id": item.target_id,
            "claim": item.claim,
            "summary": item.summary,
            "sensitivity": item.sensitivity,
            "status": item.status,
            "created_at": item.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_allowed("sensitivity", item.sensitivity, ContextSensitivity))
        errors.extend(_validate_allowed("status", item.status, ContextItemStatus))
        errors.extend(_validate_string_sequence("evidence_refs", item.evidence_refs))
        errors.extend(_validate_string_sequence("limitations", item.limitations))
        errors.extend(_validate_string_sequence("blockers", item.blockers))
        errors.extend(_validate_metadata_refs("evidence_refs", item.evidence_refs))
        if not isinstance(item.review_required, bool):
            errors.append("review_required must be a boolean")
        if item.sensitivity in BLOCKED_SENSITIVITIES:
            errors.append("blocked sensitivity cannot be included in context")
        if item.sensitivity in REVIEW_SENSITIVITIES and item.status not in REVIEW_ITEM_STATUSES:
            errors.append("review sensitivity must be blocked, rejected, or needs_review")
        if item.status == ContextItemStatus.INCLUDED_FOR_REVIEW.value and not item.review_required:
            errors.append("included_for_review is not permission")
        return errors

    @staticmethod
    def validate_context_pack(pack: ContextPack) -> List[str]:
        if not isinstance(pack, ContextPack):
            return ["pack must be a ContextPack"]
        errors: List[str] = []
        required_text = {
            "pack_id": pack.pack_id,
            "target_id": pack.target_id,
            "purpose": pack.purpose,
            "status": pack.status,
            "created_by": pack.created_by,
            "created_at": pack.created_at,
        }
        errors.extend(_validate_required_text(required_text))
        errors.extend(_validate_string_sequence("item_ids", pack.item_ids))
        errors.extend(_validate_string_sequence("limitations", pack.limitations))
        errors.extend(_validate_string_sequence("blockers", pack.blockers))
        errors.extend(_validate_allowed("status", pack.status, ContextPackStatus))
        if not isinstance(pack.review_required, bool):
            errors.append("review_required must be a boolean")
        if pack.status == ContextPackStatus.ASSEMBLED_FOR_REVIEW.value and not pack.review_required:
            errors.append(ASSEMBLED_FOR_REVIEW_IS_NOT_GOVERNANCE_APPROVAL)
        return errors


def _validate_required_text(values: Dict[str, object]) -> List[str]:
    errors: List[str] = []
    for field_name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name} is required")
    return errors


def _validate_allowed(field_name: str, value: object, enum_type: object) -> List[str]:
    if not isinstance(value, str):
        return []
    allowed = {member.value for member in enum_type}
    if value not in allowed:
        return [f"{field_name} must be one of: {', '.join(sorted(allowed))}"]
    return []


def _validate_string_sequence(field_name: str, values: object) -> List[str]:
    if isinstance(values, str):
        return [f"{field_name} must be a sequence of strings"]
    try:
        iterator = iter(values)
    except TypeError:
        return [f"{field_name} must be a sequence of strings"]
    errors: List[str] = []
    for index, value in enumerate(iterator):
        if not isinstance(value, str):
            errors.append(f"{field_name}[{index}] must be a string")
    return errors


def _validate_metadata_refs(field_name: str, values: object) -> List[str]:
    errors: List[str] = []
    for value in _iter_strings(values):
        if "\n" in value or "\r" in value:
            errors.append(f"{field_name} must be references or IDs, not raw contents")
    return errors


def _validate_pack_item_eligibility(item: ContextItem) -> List[str]:
    errors: List[str] = []
    if item.sensitivity in BLOCKED_SENSITIVITIES:
        errors.append(f"item_id cannot be packed due to blocked sensitivity: {item.item_id}")
    if item.sensitivity in REVIEW_SENSITIVITIES:
        errors.append(f"item_id cannot be packed until review is resolved: {item.item_id}")
    if item.status in REVIEW_ITEM_STATUSES:
        errors.append(f"item_id cannot be packed with review/blocking status: {item.item_id}")
    return errors


def _iter_strings(values: object) -> List[str]:
    if isinstance(values, str):
        return []
    try:
        return [value for value in values if isinstance(value, str)]
    except TypeError:
        return []
