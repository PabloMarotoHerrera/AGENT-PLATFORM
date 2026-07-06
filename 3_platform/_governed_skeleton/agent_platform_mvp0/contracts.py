"""Stdlib-only metadata contracts for the inert MVP-0 skeleton.

These contracts are metadata only. They do not read files, write files,
execute commands, call networks, call providers, activate MCP, execute
OpenCode, execute Graphify, activate GBrain/GStack/Hermes, import product
code, persist state, or mutate Git.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Mvp0ActivationLevel(str, Enum):
    """P8 activation-level metadata for MVP-0 surfaces."""

    P8_L0_DOCUMENTATION_DESIGN = "p8_l0_documentation_design"
    P8_L1_SCHEMA_STATIC_TEMPLATE = "p8_l1_schema_static_template"
    P8_L2_LOCAL_NON_EXECUTING_SURFACE = "p8_l2_local_non_executing_surface"
    P8_L3_READ_ONLY_METADATA_ADAPTER = "p8_l3_read_only_metadata_adapter_not_authorized"
    P8_L4_HUMAN_APPROVED_CONTROLLED_EXECUTION_CANDIDATE = (
        "p8_l4_human_approved_controlled_execution_candidate_not_authorized"
    )
    P8_L5_AUTONOMOUS_RUNTIME_BLOCKED = "p8_l5_autonomous_runtime_blocked"


class Mvp0OperationStatus(str, Enum):
    """Safe default operation status vocabulary."""

    METADATA_ONLY = "metadata_only"
    NOT_EXECUTED = "not_executed"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    NOT_APPROVED_FOR_EXECUTION = "not_approved_for_execution"
    NOT_APPROVED_FOR_RUNTIME = "not_approved_for_runtime"
    INVALID_SCOPE = "invalid_scope"


class Mvp0BlockedReason(str, Enum):
    """Reasons an MVP-0 operation remains blocked."""

    RUNTIME_ACTIVATION_BLOCKED = "runtime_activation_blocked"
    AUTONOMOUS_ORCHESTRATION_BLOCKED = "autonomous_orchestration_blocked"
    AUTOMATIC_DISPATCH_BLOCKED = "automatic_dispatch_blocked"
    AUTOMATIC_REVIEW_BLOCKED = "automatic_review_blocked"
    AUTOMATIC_INTEGRATION_BLOCKED = "automatic_integration_blocked"
    GIT_MUTATION_BLOCKED = "git_mutation_blocked"
    PROVIDER_API_MCP_BLOCKED = "provider_api_mcp_blocked"
    CREDENTIAL_USE_BLOCKED = "credential_use_blocked"
    OPENCODE_EXECUTION_BLOCKED = "opencode_execution_blocked"
    GRAPHIFY_EXECUTION_BLOCKED = "graphify_execution_blocked"
    GBRAIN_RUNTIME_BLOCKED = "gbrain_runtime_blocked"
    GSTACK_EXECUTION_BLOCKED = "gstack_execution_blocked"
    HERMES_RUNTIME_BLOCKED = "hermes_runtime_blocked"
    CADENCE_BLOCKED = "cadence_blocked"
    LIVE_CONNECTOR_BLOCKED = "live_connector_blocked"
    PRODUCT_SOURCE_BLOCKED = "product_source_blocked"
    SOURCE_LOADING_BLOCKED = "source_loading_blocked"
    PERSISTENCE_BLOCKED = "persistence_blocked"
    VECTOR_GRAPH_DB_BLOCKED = "vector_graph_db_blocked"
    SUBSTRATE_SELECTION_BLOCKED = "substrate_selection_blocked"
    MISSING_HUMAN_APPROVAL = "missing_human_approval"
    MISSING_P8_GATE = "missing_p8_gate"
    UNKNOWN = "unknown"


class Mvp0SurfaceKind(str, Enum):
    """MVP-0 metadata surface kinds."""

    USER_OBJECTIVE = "user_objective"
    WORK_PACKET_DRAFT = "work_packet_draft"
    HARNESS_INPUT_PACKAGE_DRAFT = "harness_input_package_draft"
    HARNESS_OUTPUT_PACKAGE = "harness_output_package"
    REVIEW_CHECKLIST = "review_checklist"
    INTEGRATION_CHECKLIST = "integration_checklist"
    DRIFT_REGISTER = "drift_register"
    ACCEPTED_OUTPUT_REGISTER = "accepted_output_register"
    REJECTED_OUTPUT_REGISTER = "rejected_output_register"
    COMMIT_CANDIDATE = "commit_candidate"
    COMMIT_COMMAND_BLOCK = "commit_command_block"
    UNKNOWN_BLOCKED = "unknown_blocked"


class Mvp0ReviewStatus(str, Enum):
    """Manual review status metadata."""

    NOT_REVIEWED = "not_reviewed"
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    ACCEPTED_BY_HUMAN_REVIEW = "accepted_by_human_review"
    REJECTED_BY_HUMAN_REVIEW = "rejected_by_human_review"
    BLOCKED_BY_BOUNDARY = "blocked_by_boundary"


@dataclass(frozen=True)
class EvidenceRef:
    ref_id: str = "evidence_ref_metadata_only"
    label: str = "metadata-only evidence ref"
    source: str = "curated_governance_metadata"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    limitations: Tuple[str, ...] = ("evidence supports; it does not decide",)


@dataclass(frozen=True)
class ContextRef:
    ref_id: str = "context_ref_metadata_only"
    label: str = "metadata-only context ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    blocked_reason: Mvp0BlockedReason = Mvp0BlockedReason.SOURCE_LOADING_BLOCKED


@dataclass(frozen=True)
class MemoryRef:
    ref_id: str = "memory_ref_metadata_only"
    label: str = "metadata-only memory ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    blocked_reason: Mvp0BlockedReason = Mvp0BlockedReason.GBRAIN_RUNTIME_BLOCKED


@dataclass(frozen=True)
class BoundaryRef:
    ref_id: str = "boundary_ref_metadata_only"
    label: str = "metadata-only boundary ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class AuditRef:
    ref_id: str = "audit_ref_metadata_only"
    label: str = "metadata-only audit ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class RetentionRef:
    ref_id: str = "retention_ref_metadata_only"
    label: str = "metadata-only retention ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class RollbackRef:
    ref_id: str = "rollback_ref_metadata_only"
    label: str = "metadata-only rollback ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class IncidentRef:
    ref_id: str = "incident_ref_metadata_only"
    label: str = "metadata-only incident ref"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class HumanApprovalRef:
    ref_id: str = "human_approval_ref_not_approval"
    label: str = "ApprovalRef is not approval"
    status: Mvp0OperationStatus = Mvp0OperationStatus.NEEDS_HUMAN_REVIEW


@dataclass(frozen=True)
class Mvp0OperationResult:
    operation_name: str = "metadata_only_operation"
    status: Mvp0OperationStatus = Mvp0OperationStatus.NOT_EXECUTED
    activation_level: Mvp0ActivationLevel = Mvp0ActivationLevel.P8_L2_LOCAL_NON_EXECUTING_SURFACE
    blocked_reasons: Tuple[Mvp0BlockedReason, ...] = (Mvp0BlockedReason.MISSING_HUMAN_APPROVAL,)
    human_review_required: bool = True
    message: str = "metadata-only result; operation not executed"
    evidence_refs: Tuple[EvidenceRef, ...] = ()
    boundary_refs: Tuple[BoundaryRef, ...] = ()
    limitations: Tuple[str, ...] = ("not runtime", "not Git mutation")


@dataclass(frozen=True)
class Mvp0SessionEnvelope:
    session_id: str = "mvp0_session_metadata_only"
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    activation_level: Mvp0ActivationLevel = Mvp0ActivationLevel.P8_L2_LOCAL_NON_EXECUTING_SURFACE
    objective_ref: str = "user_objective_not_captured_by_runtime"
    evidence_refs: Tuple[EvidenceRef, ...] = ()
    boundary_refs: Tuple[BoundaryRef, ...] = ()
    review_status: Mvp0ReviewStatus = Mvp0ReviewStatus.NEEDS_HUMAN_REVIEW


@dataclass(frozen=True)
class UserObjectiveEnvelope:
    objective_id: str = "user_objective_metadata_only"
    title: str = "metadata-only user objective"
    description: str = "not executed"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.USER_OBJECTIVE
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    human_review_required: bool = True


@dataclass(frozen=True)
class WorkPacketDraftRef:
    draft_id: str = "work_packet_draft_ref_metadata_only"
    title: str = "metadata-only WorkPacket draft ref"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.WORK_PACKET_DRAFT
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    limitations: Tuple[str, ...] = ("does not render WorkPacket", "does not dispatch")


@dataclass(frozen=True)
class HarnessInputPackageDraftRef:
    draft_id: str = "harness_input_package_draft_ref_metadata_only"
    target_harness: str = "H0_user_operated_harness"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.HARNESS_INPUT_PACKAGE_DRAFT
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    limitations: Tuple[str, ...] = ("does not execute OpenCode", "does not dispatch")


@dataclass(frozen=True)
class HarnessOutputPackageRef:
    package_id: str = "harness_output_package_ref_metadata_only"
    source_harness: str = "user_pasted_harness_output"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.HARNESS_OUTPUT_PACKAGE
    status: Mvp0OperationStatus = Mvp0OperationStatus.NEEDS_HUMAN_REVIEW
    limitations: Tuple[str, ...] = ("does not parse output", "does not trust output")


@dataclass(frozen=True)
class ReviewChecklistRef:
    checklist_id: str = "review_checklist_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.REVIEW_CHECKLIST
    review_status: Mvp0ReviewStatus = Mvp0ReviewStatus.NEEDS_HUMAN_REVIEW
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    limitations: Tuple[str, ...] = ("does not execute review", "does not assign reviewers")


@dataclass(frozen=True)
class IntegrationChecklistRef:
    checklist_id: str = "integration_checklist_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.INTEGRATION_CHECKLIST
    review_status: Mvp0ReviewStatus = Mvp0ReviewStatus.NEEDS_HUMAN_REVIEW
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY
    limitations: Tuple[str, ...] = ("does not integrate outputs",)


@dataclass(frozen=True)
class DriftRegisterRef:
    register_id: str = "drift_register_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.DRIFT_REGISTER
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class AcceptedOutputRegisterRef:
    register_id: str = "accepted_output_register_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.ACCEPTED_OUTPUT_REGISTER
    status: Mvp0OperationStatus = Mvp0OperationStatus.NEEDS_HUMAN_REVIEW


@dataclass(frozen=True)
class RejectedOutputRegisterRef:
    register_id: str = "rejected_output_register_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.REJECTED_OUTPUT_REGISTER
    status: Mvp0OperationStatus = Mvp0OperationStatus.METADATA_ONLY


@dataclass(frozen=True)
class CommitCandidateRef:
    commit_candidate_id: str = "commit_candidate_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.COMMIT_CANDIDATE
    status: Mvp0OperationStatus = Mvp0OperationStatus.NEEDS_HUMAN_REVIEW
    limitations: Tuple[str, ...] = ("does not render final Git commands", "does not mutate Git")


@dataclass(frozen=True)
class CommitCommandBlockRef:
    command_block_id: str = "commit_command_block_ref_metadata_only"
    surface_kind: Mvp0SurfaceKind = Mvp0SurfaceKind.COMMIT_COMMAND_BLOCK
    status: Mvp0OperationStatus = Mvp0OperationStatus.NEEDS_HUMAN_REVIEW
    limitations: Tuple[str, ...] = ("Never recommend git add .", "user performs Git manually")
