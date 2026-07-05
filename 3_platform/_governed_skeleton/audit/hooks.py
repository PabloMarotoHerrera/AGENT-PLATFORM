"""Metadata-only audit / retention / rollback hook skeleton.

implementation skeleton is not activation
audit hook skeleton is not active runtime logging
retention policy reference is not persistence
rollback plan reference is not rollback automation
incident route reference is not incident automation
no persistence
no automatic rollback
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class AuditEventKind(str, Enum):
    """Metadata-only audit event kind values."""

    METADATA_RECORD_CREATED = "metadata_record_created"
    DECISION_RECORD_CREATED = "decision_record_created"
    BLOCKER_RECORDED = "blocker_recorded"
    LIMITATION_RECORDED = "limitation_recorded"
    RETENTION_REF_RECORDED = "retention_ref_recorded"
    ROLLBACK_REF_RECORDED = "rollback_ref_recorded"
    INCIDENT_ROUTE_RECORDED = "incident_route_recorded"
    QUARANTINE_DECISION_RECORDED = "quarantine_decision_recorded"
    PUBLICATION_BLOCKER_RECORDED = "publication_blocker_recorded"
    SOURCE_TRACKING_BLOCKER_RECORDED = "source_tracking_blocker_recorded"
    GENERATED_OUTPUT_BLOCKER_RECORDED = "generated_output_blocker_recorded"
    NO_OP_SINK_INVOKED = "no_op_sink_invoked"
    PERSISTENCE_BLOCKED = "persistence_blocked"


class AuditSinkDecision(str, Enum):
    """Metadata-only sink decision values."""

    ACCEPTED_NOOP = "accepted_noop"
    BLOCKED_PERSISTENCE = "blocked_persistence"
    BLOCKED_SENSITIVE_CONTENT = "blocked_sensitive_content"
    BLOCKED_PUBLICATION = "blocked_publication"
    BLOCKED_SOURCE_TRACKING = "blocked_source_tracking"
    BLOCKED_GENERATED_OUTPUT_TRACKING = "blocked_generated_output_tracking"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class RetentionPolicyRef:
    """Retention policy metadata; retention policy reference is not persistence."""

    retention_policy_ref_id: str
    retention_posture: str = "metadata_only"
    policy_scope: str = "metadata_ref_only"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RollbackPlanRef:
    """Rollback metadata; rollback plan reference is not rollback automation."""

    rollback_plan_ref_id: str
    rollback_posture: str = "metadata_only"
    rollback_scope: str = "future_review_only"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class IncidentRouteRef:
    """Incident route metadata; incident route reference is not incident automation."""

    incident_route_ref_id: str
    route_posture: str = "safe_metadata_only"
    route_scope: str = "future_review_only"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PublicationBlocker:
    """Publication blocker metadata; not publication approval."""

    blocker_id: str
    blocked_ref: str
    reason: str
    source_classification: str = "unknown_sensitivity"
    sensitivity: str = "unknown_sensitivity"
    required_gate: str = "GT-12"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceTrackingBlocker:
    """Source tracking blocker metadata; not source tracking approval."""

    blocker_id: str
    blocked_ref: str
    reason: str
    source_classification: str = "unknown_sensitivity"
    sensitivity: str = "unknown_sensitivity"
    required_gate: str = "GT-02/GT-12"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class GeneratedOutputBlocker:
    """Generated output blocker metadata; not generated output tracking approval."""

    blocker_id: str
    blocked_ref: str
    reason: str
    generated_output_posture: str = "tracking_blocked"
    source_classification: str = "generated_local_only"
    sensitivity: str = "generated_sensitive"
    required_gate: str = "GT-12/GT-15"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class QuarantineDecision:
    """Quarantine metadata; it does not automate quarantine, deletion, or movement."""

    quarantine_decision_id: str
    target_ref: str
    trigger: str
    reason: str
    decision_posture: str = "metadata_only_quarantine_required"
    source_classification: str = "unknown_sensitivity"
    sensitivity: str = "unknown_sensitivity"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    retention_policy_refs: Sequence[RetentionPolicyRef] = field(default_factory=tuple)
    rollback_plan_refs: Sequence[RollbackPlanRef] = field(default_factory=tuple)
    incident_route_refs: Sequence[IncidentRouteRef] = field(default_factory=tuple)
    publication_blockers: Sequence[PublicationBlocker] = field(default_factory=tuple)
    source_tracking_blockers: Sequence[SourceTrackingBlocker] = field(
        default_factory=tuple
    )
    generated_output_blockers: Sequence[GeneratedOutputBlocker] = field(
        default_factory=tuple
    )
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditEvent:
    """Safe metadata-only audit event shape, not an active runtime log entry."""

    audit_event_id: str
    event_kind: AuditEventKind
    target_ref: str
    target_type: str
    source_classification: str = "unknown_sensitivity"
    sensitivity: str = "unknown_sensitivity"
    actor_ref: str = "metadata_actor"
    generated_output_posture: str = "not_generated"
    tracking_posture: str = "tracking_blocked"
    retention_posture: str = "metadata_only"
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    validation_refs: Sequence[str] = field(default_factory=tuple)
    security_refs: Sequence[str] = field(default_factory=tuple)
    audit_refs: Sequence[str] = field(default_factory=tuple)
    retention_policy_refs: Sequence[RetentionPolicyRef] = field(default_factory=tuple)
    rollback_plan_refs: Sequence[RollbackPlanRef] = field(default_factory=tuple)
    incident_route_refs: Sequence[IncidentRouteRef] = field(default_factory=tuple)
    publication_blockers: Sequence[PublicationBlocker] = field(default_factory=tuple)
    source_tracking_blockers: Sequence[SourceTrackingBlocker] = field(
        default_factory=tuple
    )
    generated_output_blockers: Sequence[GeneratedOutputBlocker] = field(
        default_factory=tuple
    )
    quarantine_decisions: Sequence[QuarantineDecision] = field(default_factory=tuple)
    limitations: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


def _default_limitations() -> Sequence[str]:
    return (
        "implementation skeleton is not activation",
        "audit hook skeleton is not active runtime logging",
        "retention policy reference is not persistence",
        "rollback plan reference is not rollback automation",
        "incident route reference is not incident automation",
        "no persistence",
        "no automatic rollback",
        "no runtime logging with sensitive content",
        "no publication",
        "no source tracking",
        "no generated output tracking",
        "no source loading",
        "caller_supplied_metadata_must_be_safe",
    )


def _merge_strings(*groups: Sequence[str]) -> Sequence[str]:
    merged: list[str] = []
    for group in groups:
        for item in group:
            if item not in merged:
                merged.append(item)
    return tuple(merged)


def _has_restricted_key_marker(key: str) -> bool:
    normalized = key.lower()
    restricted_markers = (
        "content",
        "payload",
        "secret",
        "credential",
        "token",
        "password",
        "private_key",
        "api_key",
        "auth",
        "cookie",
        "session",
        "env",
        "raw",
        "value",
        "provider_config",
    )
    for marker in restricted_markers:
        if marker in normalized:
            return True
    return False


def _safe_metadata(metadata: Mapping[str, str]) -> Mapping[str, str]:
    shaped: dict[str, str] = {}
    for key, value in metadata.items():
        if not _has_restricted_key_marker(key):
            shaped[key] = value
    return shaped


def _restricted_source_or_sensitivity(
    source_classification: str,
    sensitivity: str,
) -> bool:
    restricted_values = (
        "unknown_sensitivity",
        "secret_value",
        "credential_reference",
        "provider_auth_material",
        "local_only",
        "local_only_source",
        "generated_local_only",
        "generated_raw_output",
        "graphify_raw_output",
        "product_restricted",
        "external_restricted",
        "external_source",
        "external_source_candidate",
        "runtime_state",
    )
    return source_classification in restricted_values or sensitivity in restricted_values


def _merge_publication_blockers(
    *groups: Sequence[PublicationBlocker],
) -> Sequence[PublicationBlocker]:
    merged: list[PublicationBlocker] = []
    for group in groups:
        for blocker in group:
            if blocker not in merged:
                merged.append(blocker)
    return tuple(merged)


def _merge_source_tracking_blockers(
    *groups: Sequence[SourceTrackingBlocker],
) -> Sequence[SourceTrackingBlocker]:
    merged: list[SourceTrackingBlocker] = []
    for group in groups:
        for blocker in group:
            if blocker not in merged:
                merged.append(blocker)
    return tuple(merged)


def _merge_generated_output_blockers(
    *groups: Sequence[GeneratedOutputBlocker],
) -> Sequence[GeneratedOutputBlocker]:
    merged: list[GeneratedOutputBlocker] = []
    for group in groups:
        for blocker in group:
            if blocker not in merged:
                merged.append(blocker)
    return tuple(merged)


def evaluate_publication_blockers(
    event: AuditEvent,
) -> Sequence[PublicationBlocker]:
    """Preserve and shape publication blockers from supplied metadata only."""

    blockers: list[PublicationBlocker] = []
    if _restricted_source_or_sensitivity(event.source_classification, event.sensitivity):
        blockers.append(
            PublicationBlocker(
                blocker_id=f"{event.audit_event_id}:publication_blocked",
                blocked_ref=event.target_ref,
                reason="publication_blocked_by_source_or_sensitivity",
                source_classification=event.source_classification,
                sensitivity=event.sensitivity,
                evidence_refs=event.evidence_refs,
                validation_refs=event.validation_refs,
                security_refs=event.security_refs,
                limitations=_default_limitations(),
            )
        )
    return _merge_publication_blockers(event.publication_blockers, tuple(blockers))


def evaluate_source_tracking_blockers(
    event: AuditEvent,
) -> Sequence[SourceTrackingBlocker]:
    """Preserve and shape source tracking blockers from supplied metadata only."""

    blockers: list[SourceTrackingBlocker] = []
    tracking_blocked = event.tracking_posture not in (
        "not_applicable",
        "not_tracked",
    )
    if tracking_blocked or _restricted_source_or_sensitivity(
        event.source_classification,
        event.sensitivity,
    ):
        blockers.append(
            SourceTrackingBlocker(
                blocker_id=f"{event.audit_event_id}:source_tracking_blocked",
                blocked_ref=event.target_ref,
                reason="source_tracking_blocked_by_posture_or_sensitivity",
                source_classification=event.source_classification,
                sensitivity=event.sensitivity,
                evidence_refs=event.evidence_refs,
                validation_refs=event.validation_refs,
                security_refs=event.security_refs,
                limitations=_default_limitations(),
            )
        )
    return _merge_source_tracking_blockers(
        event.source_tracking_blockers,
        tuple(blockers),
    )


def evaluate_generated_output_blockers(
    event: AuditEvent,
) -> Sequence[GeneratedOutputBlocker]:
    """Preserve and shape generated output blockers from supplied metadata only."""

    blockers: list[GeneratedOutputBlocker] = []
    generated_output_blocked = event.generated_output_posture not in (
        "not_generated",
        "not_applicable",
        "metadata_only",
    )
    if generated_output_blocked or event.source_classification in (
        "generated_local_only",
        "generated_raw_output",
        "graphify_raw_output",
    ):
        blockers.append(
            GeneratedOutputBlocker(
                blocker_id=f"{event.audit_event_id}:generated_output_blocked",
                blocked_ref=event.target_ref,
                reason="generated_output_tracking_blocked_by_posture",
                generated_output_posture=event.generated_output_posture,
                source_classification=event.source_classification,
                sensitivity=event.sensitivity,
                evidence_refs=event.evidence_refs,
                validation_refs=event.validation_refs,
                security_refs=event.security_refs,
                limitations=_default_limitations(),
            )
        )
    return _merge_generated_output_blockers(
        event.generated_output_blockers,
        tuple(blockers),
    )


def build_audit_event(
    audit_event_id: str,
    event_kind: AuditEventKind,
    target_ref: str,
    target_type: str,
    source_classification: str,
    sensitivity: str,
    metadata: Mapping[str, str],
    actor_ref: str = "metadata_actor",
    generated_output_posture: str = "not_generated",
    tracking_posture: str = "tracking_blocked",
    retention_posture: str = "metadata_only",
    evidence_refs: Sequence[str] = (),
    validation_refs: Sequence[str] = (),
    security_refs: Sequence[str] = (),
    audit_refs: Sequence[str] = (),
    retention_policy_refs: Sequence[RetentionPolicyRef] = (),
    rollback_plan_refs: Sequence[RollbackPlanRef] = (),
    incident_route_refs: Sequence[IncidentRouteRef] = (),
    publication_blockers: Sequence[PublicationBlocker] = (),
    source_tracking_blockers: Sequence[SourceTrackingBlocker] = (),
    generated_output_blockers: Sequence[GeneratedOutputBlocker] = (),
    quarantine_decisions: Sequence[QuarantineDecision] = (),
    limitations: Sequence[str] = (),
) -> AuditEvent:
    """Build a safe metadata-only audit event without logging or persistence."""

    shaped_event = AuditEvent(
        audit_event_id=audit_event_id,
        event_kind=event_kind,
        target_ref=target_ref,
        target_type=target_type,
        source_classification=source_classification,
        sensitivity=sensitivity,
        actor_ref=actor_ref,
        generated_output_posture=generated_output_posture,
        tracking_posture=tracking_posture,
        retention_posture=retention_posture,
        evidence_refs=evidence_refs,
        validation_refs=validation_refs,
        security_refs=security_refs,
        audit_refs=audit_refs,
        retention_policy_refs=retention_policy_refs,
        rollback_plan_refs=rollback_plan_refs,
        incident_route_refs=incident_route_refs,
        publication_blockers=publication_blockers,
        source_tracking_blockers=source_tracking_blockers,
        generated_output_blockers=generated_output_blockers,
        quarantine_decisions=quarantine_decisions,
        limitations=_merge_strings(_default_limitations(), limitations),
        metadata=_safe_metadata(metadata),
    )

    return AuditEvent(
        audit_event_id=shaped_event.audit_event_id,
        event_kind=shaped_event.event_kind,
        target_ref=shaped_event.target_ref,
        target_type=shaped_event.target_type,
        source_classification=shaped_event.source_classification,
        sensitivity=shaped_event.sensitivity,
        actor_ref=shaped_event.actor_ref,
        generated_output_posture=shaped_event.generated_output_posture,
        tracking_posture=shaped_event.tracking_posture,
        retention_posture=shaped_event.retention_posture,
        evidence_refs=shaped_event.evidence_refs,
        validation_refs=shaped_event.validation_refs,
        security_refs=shaped_event.security_refs,
        audit_refs=shaped_event.audit_refs,
        retention_policy_refs=shaped_event.retention_policy_refs,
        rollback_plan_refs=shaped_event.rollback_plan_refs,
        incident_route_refs=shaped_event.incident_route_refs,
        publication_blockers=evaluate_publication_blockers(shaped_event),
        source_tracking_blockers=evaluate_source_tracking_blockers(shaped_event),
        generated_output_blockers=evaluate_generated_output_blockers(shaped_event),
        quarantine_decisions=shaped_event.quarantine_decisions,
        limitations=shaped_event.limitations,
        metadata=shaped_event.metadata,
    )


def build_quarantine_decision(
    quarantine_decision_id: str,
    target_ref: str,
    trigger: str,
    reason: str,
    source_classification: str,
    sensitivity: str,
    metadata: Mapping[str, str],
    evidence_refs: Sequence[str] = (),
    validation_refs: Sequence[str] = (),
    security_refs: Sequence[str] = (),
    retention_policy_refs: Sequence[RetentionPolicyRef] = (),
    rollback_plan_refs: Sequence[RollbackPlanRef] = (),
    incident_route_refs: Sequence[IncidentRouteRef] = (),
    limitations: Sequence[str] = (),
) -> QuarantineDecision:
    """Build quarantine metadata without automating quarantine."""

    event = build_audit_event(
        audit_event_id=f"{quarantine_decision_id}:audit_event",
        event_kind=AuditEventKind.QUARANTINE_DECISION_RECORDED,
        target_ref=target_ref,
        target_type="quarantine_decision",
        source_classification=source_classification,
        sensitivity=sensitivity,
        metadata=metadata,
        evidence_refs=evidence_refs,
        validation_refs=validation_refs,
        security_refs=security_refs,
        retention_policy_refs=retention_policy_refs,
        rollback_plan_refs=rollback_plan_refs,
        incident_route_refs=incident_route_refs,
        limitations=limitations,
    )
    return QuarantineDecision(
        quarantine_decision_id=quarantine_decision_id,
        target_ref=target_ref,
        trigger=trigger,
        reason=reason,
        source_classification=source_classification,
        sensitivity=sensitivity,
        evidence_refs=evidence_refs,
        validation_refs=validation_refs,
        security_refs=security_refs,
        retention_policy_refs=retention_policy_refs,
        rollback_plan_refs=rollback_plan_refs,
        incident_route_refs=incident_route_refs,
        publication_blockers=event.publication_blockers,
        source_tracking_blockers=event.source_tracking_blockers,
        generated_output_blockers=event.generated_output_blockers,
        limitations=event.limitations,
        metadata=event.metadata,
    )


@dataclass(frozen=True)
class NoOpAuditSink:
    """No-op sink: audit hook skeleton is not active runtime logging."""

    sink_id: str = "noop_audit_sink"
    sink_posture: str = "no_op_no_persistence"
    limitations: Sequence[str] = field(default_factory=_default_limitations)

    def decide(self, event: AuditEvent) -> AuditSinkDecision:
        """Return a no-op decision without writing or persisting anything."""

        if event.publication_blockers:
            return AuditSinkDecision.ACCEPTED_NOOP
        return AuditSinkDecision.ACCEPTED_NOOP


@dataclass(frozen=True)
class BlockedPersistenceSink:
    """Persistence sink that always denies persistence; no persistence."""

    sink_id: str = "blocked_persistence_sink"
    sink_posture: str = "blocked_persistence"
    limitations: Sequence[str] = field(default_factory=_default_limitations)

    def decide(self, event: AuditEvent) -> AuditSinkDecision:
        """Always deny persistence without writing, logging, or storing anything."""

        if event.sensitivity in ("secret_value", "credential_reference"):
            return AuditSinkDecision.BLOCKED_PERSISTENCE
        return AuditSinkDecision.BLOCKED_PERSISTENCE
