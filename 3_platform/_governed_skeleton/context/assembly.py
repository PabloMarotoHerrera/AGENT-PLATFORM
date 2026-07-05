"""Metadata-only context assembly runtime candidate skeleton.

context inclusion is not permission
source refs are metadata only
no source loading
implementation skeleton is not activation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class ContextAssemblyStatus(str, Enum):
    """Metadata-only assembly decision status."""

    READY_METADATA_ONLY = "ready_metadata_only"
    PARTIAL_METADATA_ONLY = "partial_metadata_only"
    BLOCKED = "blocked"


class ContextItemStatus(str, Enum):
    """Metadata-only item decision status."""

    CANDIDATE = "candidate"
    INCLUDED_METADATA_ONLY = "included_metadata_only"
    BLOCKED = "blocked"


class ContextSourceClassification(str, Enum):
    """Source classification for metadata-only context source refs."""

    GOVERNANCE_RECORD = "governance_record"
    IMPLEMENTATION_RECORD = "implementation_record"
    SECURITY_POLICY = "security_policy"
    REPOSITORY_BOUNDARY = "repository_boundary"
    EXTERNAL_SOURCE_REFERENCE = "external_source_reference"
    EXTERNAL_SOURCE_CONTENT = "external_source_content"
    PRODUCT_SOURCE = "product_source"
    GENERATED_OUTPUT_REFERENCE = "generated_output_reference"
    GENERATED_RAW_OUTPUT = "generated_raw_output"
    GRAPHIFY_OUTPUT_REFERENCE = "graphify_output_reference"
    GRAPHIFY_RAW_OUTPUT = "graphify_raw_output"
    LOCAL_ONLY_CONTENT = "local_only_content"
    UNKNOWN = "unknown"


class ContextSensitivity(str, Enum):
    """Sensitivity labels used before any metadata-only inclusion."""

    PUBLIC_METADATA = "public_metadata"
    INTERNAL_METADATA = "internal_metadata"
    LOCAL_ONLY = "local_only"
    SECRET = "secret"
    CREDENTIAL = "credential"
    PROVIDER_AUTH = "provider_auth"
    UNKNOWN = "unknown"


class ContextBlocker(str, Enum):
    """Blockers that prevent metadata-only context item inclusion."""

    NO_CANDIDATE_SOURCE_REFS = "no_candidate_source_refs"
    METADATA_ONLY_DISABLED = "metadata_only_disabled"
    PREBLOCKED_ITEM = "preblocked_item"
    UNKNOWN_SENSITIVITY = "unknown_sensitivity"
    SECRET_OR_CREDENTIAL = "secret_or_credential"
    PROVIDER_AUTH_MATERIAL = "provider_auth_material"
    PRODUCT_SOURCE = "product_source"
    EXTERNAL_SOURCE_CONTENT = "external_source_content"
    GENERATED_RAW_OUTPUT = "generated_raw_output"
    GRAPHIFY_RAW_OUTPUT = "graphify_raw_output"
    LOCAL_ONLY_CONTENT = "local_only_content"


class ContextLimitation(str, Enum):
    """Limitations that must propagate with every metadata-only decision."""

    CONTEXT_INCLUSION_IS_NOT_PERMISSION = "context inclusion is not permission"
    SOURCE_REFS_ARE_METADATA_ONLY = "source refs are metadata only"
    NO_SOURCE_LOADING = "no source loading"
    IMPLEMENTATION_SKELETON_IS_NOT_ACTIVATION = (
        "implementation skeleton is not activation"
    )
    VALIDATION_NOT_RUN = "validation_not_run"
    PENDING_P5_1_VALIDATION_RUNNER_ALIGNMENT = (
        "pending_P5.1_validation_runner_alignment"
    )
    PENDING_P5_2_SECURITY_POLICY_DRY_RUN_ALIGNMENT = (
        "pending_P5.2_security_policy_dry_run_alignment"
    )
    PENDING_P5_7_AUDIT_RETENTION_ROLLBACK_HOOKS_ALIGNMENT = (
        "pending_P5.7_audit_retention_rollback_hooks_alignment"
    )
    COGNITIVE_SEMANTIC_SYSTEM_SUBSTRATE_DEFERRED = (
        "cognitive_semantic_system_substrate_deferred"
    )


def _default_limitations() -> Sequence[ContextLimitation]:
    return (
        ContextLimitation.CONTEXT_INCLUSION_IS_NOT_PERMISSION,
        ContextLimitation.SOURCE_REFS_ARE_METADATA_ONLY,
        ContextLimitation.NO_SOURCE_LOADING,
        ContextLimitation.IMPLEMENTATION_SKELETON_IS_NOT_ACTIVATION,
        ContextLimitation.VALIDATION_NOT_RUN,
        ContextLimitation.PENDING_P5_1_VALIDATION_RUNNER_ALIGNMENT,
        ContextLimitation.PENDING_P5_2_SECURITY_POLICY_DRY_RUN_ALIGNMENT,
        ContextLimitation.PENDING_P5_7_AUDIT_RETENTION_ROLLBACK_HOOKS_ALIGNMENT,
        ContextLimitation.COGNITIVE_SEMANTIC_SYSTEM_SUBSTRATE_DEFERRED,
    )


@dataclass(frozen=True)
class ContextSourceRef:
    """Metadata-only reference to a source; it is never a source loader."""

    source_id: str
    label: str
    classification: ContextSourceClassification = ContextSourceClassification.UNKNOWN
    sensitivity: ContextSensitivity = ContextSensitivity.UNKNOWN
    metadata: Mapping[str, str] = field(default_factory=dict)
    limitations: Sequence[ContextLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class ContextItem:
    """A candidate context item that can only carry metadata."""

    item_id: str
    source_ref: ContextSourceRef
    purpose: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)
    status: ContextItemStatus = ContextItemStatus.CANDIDATE
    blockers: Sequence[ContextBlocker] = field(default_factory=tuple)
    limitations: Sequence[ContextLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class ContextSelectionPolicy:
    """Metadata-only source selection policy."""

    allow_metadata_only: bool = True
    block_unknown_sensitivity: bool = True
    block_secret_or_credential: bool = True
    block_product_source: bool = True
    block_external_source_content: bool = True
    block_generated_raw_output: bool = True
    block_graphify_raw_output: bool = True
    block_local_only_content: bool = True
    required_limitations: Sequence[ContextLimitation] = field(
        default_factory=_default_limitations
    )


@dataclass(frozen=True)
class ContextAssemblyRequest:
    """Metadata-only context assembly request."""

    request_id: str
    purpose: str = ""
    candidate_sources: Sequence[ContextSourceRef] = field(default_factory=tuple)
    candidate_items: Sequence[ContextItem] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)
    limitations: Sequence[ContextLimitation] = field(default_factory=tuple)


@dataclass(frozen=True)
class ContextAssemblyPlan:
    """Evaluated metadata-only context assembly plan."""

    plan_id: str
    items: Sequence[ContextItem] = field(default_factory=tuple)
    blockers: Sequence[ContextBlocker] = field(default_factory=tuple)
    limitations: Sequence[ContextLimitation] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ContextPack:
    """Metadata-only pack containing only unblocked context items."""

    pack_id: str
    items: Sequence[ContextItem] = field(default_factory=tuple)
    limitations: Sequence[ContextLimitation] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ContextAssemblyDecision:
    """Final metadata-only assembly decision."""

    request_id: str
    status: ContextAssemblyStatus
    plan: ContextAssemblyPlan
    context_pack: ContextPack
    blockers: Sequence[ContextBlocker] = field(default_factory=tuple)
    limitations: Sequence[ContextLimitation] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)


def _merge_blockers(
    *groups: Sequence[ContextBlocker],
) -> Sequence[ContextBlocker]:
    merged: list[ContextBlocker] = []
    for group in groups:
        for blocker in group:
            if blocker not in merged:
                merged.append(blocker)
    return tuple(merged)


def _merge_limitations(
    *groups: Sequence[ContextLimitation],
) -> Sequence[ContextLimitation]:
    merged: list[ContextLimitation] = []
    for group in groups:
        for limitation in group:
            if limitation not in merged:
                merged.append(limitation)
    return tuple(merged)


def _source_blockers(
    source_ref: ContextSourceRef,
    policy: ContextSelectionPolicy,
) -> Sequence[ContextBlocker]:
    blockers: list[ContextBlocker] = []

    if not policy.allow_metadata_only:
        blockers.append(ContextBlocker.METADATA_ONLY_DISABLED)

    if (
        policy.block_unknown_sensitivity
        and source_ref.sensitivity is ContextSensitivity.UNKNOWN
    ):
        blockers.append(ContextBlocker.UNKNOWN_SENSITIVITY)

    if policy.block_secret_or_credential and source_ref.sensitivity in (
        ContextSensitivity.SECRET,
        ContextSensitivity.CREDENTIAL,
    ):
        blockers.append(ContextBlocker.SECRET_OR_CREDENTIAL)

    if (
        policy.block_secret_or_credential
        and source_ref.sensitivity is ContextSensitivity.PROVIDER_AUTH
    ):
        blockers.append(ContextBlocker.PROVIDER_AUTH_MATERIAL)

    if (
        policy.block_product_source
        and source_ref.classification is ContextSourceClassification.PRODUCT_SOURCE
    ):
        blockers.append(ContextBlocker.PRODUCT_SOURCE)

    if (
        policy.block_external_source_content
        and source_ref.classification is ContextSourceClassification.EXTERNAL_SOURCE_CONTENT
    ):
        blockers.append(ContextBlocker.EXTERNAL_SOURCE_CONTENT)

    if (
        policy.block_generated_raw_output
        and source_ref.classification is ContextSourceClassification.GENERATED_RAW_OUTPUT
    ):
        blockers.append(ContextBlocker.GENERATED_RAW_OUTPUT)

    if (
        policy.block_graphify_raw_output
        and source_ref.classification is ContextSourceClassification.GRAPHIFY_RAW_OUTPUT
    ):
        blockers.append(ContextBlocker.GRAPHIFY_RAW_OUTPUT)

    if policy.block_local_only_content and (
        source_ref.classification is ContextSourceClassification.LOCAL_ONLY_CONTENT
        or source_ref.sensitivity is ContextSensitivity.LOCAL_ONLY
    ):
        blockers.append(ContextBlocker.LOCAL_ONLY_CONTENT)

    return tuple(blockers)


def _items_from_sources(request: ContextAssemblyRequest) -> Sequence[ContextItem]:
    items: list[ContextItem] = []

    for item in request.candidate_items:
        items.append(item)

    for source_ref in request.candidate_sources:
        items.append(
            ContextItem(
                item_id=f"{request.request_id}:{source_ref.source_id}",
                source_ref=source_ref,
                purpose=request.purpose,
                metadata=source_ref.metadata,
            )
        )

    return tuple(items)


def _evaluate_item(
    item: ContextItem,
    policy: ContextSelectionPolicy,
    inherited_limitations: Sequence[ContextLimitation],
) -> ContextItem:
    preblocked = ()
    if item.status is ContextItemStatus.BLOCKED:
        preblocked = (ContextBlocker.PREBLOCKED_ITEM,)

    blockers = _merge_blockers(
        item.blockers,
        preblocked,
        _source_blockers(item.source_ref, policy),
    )
    limitations = _merge_limitations(
        inherited_limitations,
        item.source_ref.limitations,
        item.limitations,
    )
    status = ContextItemStatus.INCLUDED_METADATA_ONLY
    if blockers:
        status = ContextItemStatus.BLOCKED

    return ContextItem(
        item_id=item.item_id,
        source_ref=item.source_ref,
        purpose=item.purpose,
        metadata=item.metadata,
        status=status,
        blockers=blockers,
        limitations=limitations,
    )


def _assembly_status(items: Sequence[ContextItem]) -> ContextAssemblyStatus:
    if not items:
        return ContextAssemblyStatus.BLOCKED

    included_count = 0
    blocked_count = 0
    for item in items:
        if item.status is ContextItemStatus.INCLUDED_METADATA_ONLY:
            included_count += 1
        if item.status is ContextItemStatus.BLOCKED:
            blocked_count += 1

    if included_count == 0:
        return ContextAssemblyStatus.BLOCKED
    if blocked_count > 0:
        return ContextAssemblyStatus.PARTIAL_METADATA_ONLY
    return ContextAssemblyStatus.READY_METADATA_ONLY


def build_context_assembly_decision(
    request: ContextAssemblyRequest,
    policy: ContextSelectionPolicy,
) -> ContextAssemblyDecision:
    """Build a pure, metadata-only context assembly decision."""

    base_limitations = _merge_limitations(
        _default_limitations(),
        policy.required_limitations,
        request.limitations,
    )

    evaluated_items: list[ContextItem] = []
    for item in _items_from_sources(request):
        evaluated_items.append(_evaluate_item(item, policy, base_limitations))

    decision_blockers: list[ContextBlocker] = []
    if not evaluated_items:
        decision_blockers.append(ContextBlocker.NO_CANDIDATE_SOURCE_REFS)

    for item in evaluated_items:
        for blocker in item.blockers:
            if blocker not in decision_blockers:
                decision_blockers.append(blocker)

    included_items: list[ContextItem] = []
    for item in evaluated_items:
        if item.status is ContextItemStatus.INCLUDED_METADATA_ONLY:
            included_items.append(item)

    blockers = tuple(decision_blockers)
    limitations = base_limitations
    status = _assembly_status(tuple(evaluated_items))
    plan = ContextAssemblyPlan(
        plan_id=f"{request.request_id}:metadata_only_plan",
        items=tuple(evaluated_items),
        blockers=blockers,
        limitations=limitations,
        metadata=request.metadata,
    )
    context_pack = ContextPack(
        pack_id=f"{request.request_id}:metadata_only_pack",
        items=tuple(included_items),
        limitations=limitations,
        metadata=request.metadata,
    )

    return ContextAssemblyDecision(
        request_id=request.request_id,
        status=status,
        plan=plan,
        context_pack=context_pack,
        blockers=blockers,
        limitations=limitations,
        metadata=request.metadata,
    )
