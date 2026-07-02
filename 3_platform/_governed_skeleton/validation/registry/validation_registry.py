"""I-01 minimal validation registry boundary.

This module models validation records in memory only. It does not execute
validations, persist records, call external systems, inspect environment
state, activate providers, approve governance decisions, or imply readiness.
Validation evaluates; governance decides.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence


class ProofLevel(str, Enum):
    """Allowed proof levels for metadata records."""

    PL_0 = "PL-0"
    PL_1 = "PL-1"
    PL_2 = "PL-2"
    PL_3 = "PL-3"
    PL_4 = "PL-4"
    PL_5 = "PL-5"
    PL_6 = "PL-6"
    PL_7 = "PL-7"
    PL_8 = "PL-8"


class ValidationStatus(str, Enum):
    """Allowed status values for scope-bound validation metadata."""

    DRAFT = "draft"
    EVIDENCE_RECORDED = "evidence_recorded"
    BLOCKED = "blocked"
    VALIDATED_FOR_SCOPE = "validated_for_scope"
    REJECTED_FOR_SCOPE = "rejected_for_scope"
    NEEDS_REVIEW = "needs_review"


VALIDATION_STATUS_IS_NOT_GOVERNANCE_APPROVAL = (
    "validated_for_scope is not governance approval"
)
PROOF_LEVEL_IS_NOT_AUTHORIZATION = "proof_level is not authorization"
EVIDENCE_REFS_ARE_METADATA_ONLY = "evidence_refs are metadata references only"


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
class ValidationRecord:
    """Metadata-only validation record.

    The record retains evidence references, limitations, and blockers. A
    status of validated_for_scope does not mean governance approval.
    """

    record_id: str
    target_id: str
    claim: str
    status: str
    proof_level: str
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    blockers: Sequence[str] = field(default_factory=tuple)
    created_by: str = ""
    created_at: str = ""
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", _value(self.status))
        object.__setattr__(self, "proof_level", _value(self.proof_level))
        object.__setattr__(self, "evidence_refs", _tuple_of_strings(self.evidence_refs))
        object.__setattr__(self, "limitations", _tuple_of_strings(self.limitations))
        object.__setattr__(self, "blockers", _tuple_of_strings(self.blockers))


class ValidationRegistry:
    """In-memory registry for validation metadata records only."""

    def __init__(self) -> None:
        self._records: Dict[str, ValidationRecord] = {}

    def add_record(self, record: ValidationRecord) -> ValidationRecord:
        """Add a record after field validation and duplicate ID rejection."""
        errors = self.validate_record(record)
        if errors:
            raise ValueError("; ".join(errors))
        if record.record_id in self._records:
            raise ValueError(f"duplicate record_id: {record.record_id}")
        self._records[record.record_id] = record
        return record

    def get_record(self, record_id: str) -> Optional[ValidationRecord]:
        """Return a record by ID, or None when absent."""
        return self._records.get(record_id)

    def list_records(self) -> List[ValidationRecord]:
        """Return all records in insertion order."""
        return list(self._records.values())

    def list_records_by_target(self, target_id: str) -> List[ValidationRecord]:
        """Return records associated with a target ID."""
        return [record for record in self._records.values() if record.target_id == target_id]

    @staticmethod
    def validate_record(record: ValidationRecord) -> List[str]:
        """Return validation errors for required metadata fields."""
        if not isinstance(record, ValidationRecord):
            return ["record must be a ValidationRecord"]

        errors: List[str] = []
        required_text = {
            "record_id": record.record_id,
            "target_id": record.target_id,
            "claim": record.claim,
            "status": record.status,
            "proof_level": record.proof_level,
            "created_by": record.created_by,
            "created_at": record.created_at,
        }

        for field_name, value in required_text.items():
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{field_name} is required")

        allowed_statuses = {status.value for status in ValidationStatus}
        if isinstance(record.status, str) and record.status not in allowed_statuses:
            errors.append(f"status must be one of: {', '.join(sorted(allowed_statuses))}")

        allowed_proof_levels = {level.value for level in ProofLevel}
        if isinstance(record.proof_level, str) and record.proof_level not in allowed_proof_levels:
            errors.append(
                f"proof_level must be one of: {', '.join(sorted(allowed_proof_levels))}"
            )

        errors.extend(_validate_string_sequence("evidence_refs", record.evidence_refs))
        errors.extend(_validate_string_sequence("limitations", record.limitations))
        errors.extend(_validate_string_sequence("blockers", record.blockers))

        try:
            evidence_refs = iter(record.evidence_refs)
        except TypeError:
            evidence_refs = iter(())
        for evidence_ref in evidence_refs:
            if isinstance(evidence_ref, str) and ("\n" in evidence_ref or "\r" in evidence_ref):
                errors.append("evidence_refs must be references or IDs, not raw contents")

        if not isinstance(record.review_required, bool):
            errors.append("review_required must be a boolean")
        if record.status == ValidationStatus.VALIDATED_FOR_SCOPE.value and not record.review_required:
            errors.append(VALIDATION_STATUS_IS_NOT_GOVERNANCE_APPROVAL)

        return errors


def _validate_string_sequence(field_name: str, values: Sequence[str]) -> List[str]:
    if isinstance(values, str):
        return [f"{field_name} must be a sequence of strings"]
    errors: List[str] = []
    try:
        iterator = iter(values)
    except TypeError:
        return [f"{field_name} must be a sequence of strings"]
    for index, value in enumerate(iterator):
        if not isinstance(value, str):
            errors.append(f"{field_name}[{index}] must be a string")
    return errors
