"""P18.7 manual-versus-Hermes shadow-run comparison for Pepper.

This module records bounded evidence for a representative manual workflow and
the corresponding Pepper/Hermes governed workflow. It compares the two paths and
derives P18.8 readiness without executing workers, mutating Git, touching Kanban,
calling providers/models, launching subprocesses, or changing default mode.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
import re
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from hermes_cli.agent_platform.workflow.retry_incident_rollback import (
    RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION,
)


MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION = 1
MANUAL_HERMES_SHADOW_RUN_POLICY_ID = "pepper-manual-hermes-shadow-run-v1"

MANUAL_HERMES_SHADOW_REQUEST_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-request-sha256-v1"
)
MANUAL_HERMES_SHADOW_TICKET_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-ticket-sha256-v1"
)
MANUAL_HERMES_SHADOW_MANUAL_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-manual-sha256-v1"
)
MANUAL_HERMES_SHADOW_AUTHORITY_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-authority-sha256-v1"
)
MANUAL_HERMES_SHADOW_PEPPER_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-pepper-sha256-v1"
)
MANUAL_HERMES_SHADOW_WORKSPACE_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-workspace-sha256-v1"
)
MANUAL_HERMES_SHADOW_COMPARISON_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-comparison-sha256-v1"
)
MANUAL_HERMES_SHADOW_UI_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-ui-sha256-v1"
)
MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-audit-sha256-v1"
)
MANUAL_HERMES_SHADOW_GAP_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-gap-sha256-v1"
)
MANUAL_HERMES_SHADOW_EFFORT_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-effort-sha256-v1"
)
MANUAL_HERMES_SHADOW_GIT_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-git-sha256-v1"
)
MANUAL_HERMES_SHADOW_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-summary-sha256-v1"
)
MANUAL_HERMES_SHADOW_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-manual-hermes-shadow-result-sha256-v1"
)

_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
_TICKET_ID_PATTERN = r"^[A-Z0-9][A-Z0-9._-]{2,80}$"
_GAP_ID_PATTERN = r"^P18-8-GAP-[0-9]{3}$"
_WORK_PACKET_ID_PATTERN = r"^WP-[A-Z0-9._-]+-R[0-9]{4}$"
_CONTROL_OR_ANSI_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x1b]")
_PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)")
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
_CREDENTIAL_MARKERS = (
    "access_token",
    "refresh_token",
    "authorization:",
    "bearer ",
    "client_secret",
    "api_key",
    "apikey",
    "private key",
    "password=",
    "token=",
    "secret=",
    "cookie:",
)
_RAW_CONTEXT_MARKERS = (
    "raw prompt",
    "system prompt",
    "reasoning trace",
    "provider response",
    "model output",
    "raw stdout",
    "raw stderr",
    "raw diff",
    "diff --git",
    "source snapshot",
    "raw conversation",
    "chatgpt transcript",
    "opencode transcript",
    "runtime handle",
    "git handle",
)

DigestText = Annotated[str, Field(pattern=_DIGEST_PATTERN)]
CommitSha = Annotated[str, Field(pattern=_COMMIT_PATTERN)]
ShadowTicketIdentifier = Annotated[str, Field(pattern=_TICKET_ID_PATTERN)]
MigrationGapIdentifier = Annotated[str, Field(pattern=_GAP_ID_PATTERN)]
WorkPacketIdentifier = Annotated[str, Field(pattern=_WORK_PACKET_ID_PATTERN)]
BoundedText = Annotated[str, Field(min_length=1, max_length=1024)]


class ManualHermesShadowRunError(ValueError):
    """Base error for P18.7 shadow-run comparison failures."""


class ManualHermesShadowRunInputError(ManualHermesShadowRunError):
    """Raised when P18.7 caller input is malformed."""


class ManualHermesShadowRunIntegrityError(ManualHermesShadowRunError):
    """Raised when P18.7 evidence bindings or digests mismatch."""


class ManualHermesShadowRunPolicyError(ManualHermesShadowRunError):
    """Raised when P18.7 migration policy boundaries are violated."""


class ManualHermesShadowRunStateError(ManualHermesShadowRunError):
    """Raised when P18.7 state or readiness evidence is inconsistent."""


class ManualHermesShadowRunValidationError(ManualHermesShadowRunError):
    """Raised when immutable P18.7 evidence fails validation."""


class ManualHermesShadowRunDecision(str, Enum):
    SHADOW_VALIDATED = "shadow_validated"
    SHADOW_VALIDATED_WITH_CUTOVER_BLOCKERS = "shadow_validated_with_cutover_blockers"


class ManualHermesShadowRunComparisonScore(str, Enum):
    MATCH = "MATCH"
    EQUIVALENT = "EQUIVALENT"
    MISMATCH = "MISMATCH"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    MANUAL_BETTER = "MANUAL_BETTER"
    PEPPER_BETTER = "PEPPER_BETTER"
    BLOCKED = "BLOCKED"


class ManualHermesShadowRunGapCategory(str, Enum):
    UI_BACKEND_GAP = "UI_BACKEND_GAP"
    WORKFLOW_VISIBILITY_GAP = "WORKFLOW_VISIBILITY_GAP"
    HUMAN_ACTION_GAP = "HUMAN_ACTION_GAP"
    EXECUTOR_INTEGRATION_GAP = "EXECUTOR_INTEGRATION_GAP"
    CONTEXT_GAP = "CONTEXT_GAP"
    AUTHORITY_GAP = "AUTHORITY_GAP"
    PERSISTENCE_GAP = "PERSISTENCE_GAP"
    SECURITY_GAP = "SECURITY_GAP"
    OBSERVABILITY_GAP = "OBSERVABILITY_GAP"
    OTHER = "OTHER"


class ManualHermesShadowRunGapSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKER = "blocker"


class ManualHermesShadowRunDependencyPosture(str, Enum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    NOT_REQUIRED = "NOT_REQUIRED"


class ManualHermesShadowRunUIClassification(str, Enum):
    FUNCTIONAL_LIVE_BACKEND = "functional_live_backend"
    FUNCTIONAL_READ_ONLY_PROJECTION = "functional_read_only_projection"
    UNAVAILABLE_BACKEND = "unavailable_backend"
    PLACEHOLDER = "placeholder"
    BROKEN = "broken"


class ManualHermesShadowRunHumanSmokeStatus(str, Enum):
    HUMAN_UI_SMOKE_PASS = "HUMAN_UI_SMOKE_PASS"
    HUMAN_UI_SMOKE_BLOCKED = "HUMAN_UI_SMOKE_BLOCKED"


class ManualHermesShadowRunReadinessDecision(str, Enum):
    P18_8_READY = "P18_8_READY"
    P18_8_BLOCKED = "P18_8_BLOCKED"


class ManualHermesShadowRunStage(str, Enum):
    PROJECT_CONTEXT = "project_context"
    TICKET_SEMANTICS = "ticket_semantics"
    APPROVAL = "approval"
    DEPENDENCY_GATE = "dependency_gate"
    EXECUTION = "execution"
    VALIDATION = "validation"
    REVIEW = "review"
    RECOVERY = "recovery"
    GIT_HANDOFF = "Git_handoff"
    WORKFLOW_STATE = "workflow_state"
    UI_VISIBILITY = "UI_visibility"
    OPERATOR_EFFORT = "operator_effort"
    AUTHORITY = "authority"
    SECURITY = "security"
    EVIDENCE_COMPLETENESS = "evidence_completeness"


class _ManualHermesShadowModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        protected_namespaces=(),
        validate_default=True,
        str_strip_whitespace=True,
    )


def _validate_safe_text(value: str, label: str) -> str:
    if _CONTROL_OR_ANSI_PATTERN.search(value):
        raise ValueError(f"{label} contains control characters")
    lowered = value.lower()
    if any(marker in lowered for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} contains credential-shaped text")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-shaped text")
    if any(marker in lowered for marker in _RAW_CONTEXT_MARKERS):
        raise ValueError(f"{label} contains raw context")
    if _PERSONAL_PATH_PATTERN.search(value):
        raise ValueError(f"{label} contains personal absolute path")
    return value


def _validate_safe_tuple(value: tuple[str, ...], label: str) -> tuple[str, ...]:
    for item in value:
        _validate_safe_text(item, label)
    if len(value) != len(set(value)):
        raise ValueError(f"{label} entries must be unique")
    return value


def _digest_payload(value: object) -> object:
    if isinstance(value, BaseModel):
        return _digest_payload(value.model_dump(mode="python", warnings=False))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_digest_payload(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _digest_payload(item) for key, item in value.items()}
    return value


def _digest_from_record(algorithm: str, record: object) -> str:
    encoded = json.dumps(
        {"algorithm": algorithm, "payload": _digest_payload(record)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _model_digest(algorithm: str, value: BaseModel, digest_field: str) -> str:
    return _digest_from_record(
        algorithm,
        value.model_dump(mode="json", exclude={digest_field}),
    )


def _make_model(
    model_type: type[_ManualHermesShadowModel],
    digest_field: str,
    algorithm: str,
    **values: object,
):
    provisional = model_type.model_construct(**values, **{digest_field: "0" * 64})
    digest = _model_digest(algorithm, provisional, digest_field)
    return model_type.model_validate({**values, digest_field: digest})


def _stable_digest(label: str) -> str:
    return _digest_from_record(
        "agent-platform-manual-hermes-shadow-stable-reference-sha256-v1",
        label,
    )


class ShadowTicketSelection(_ManualHermesShadowModel):
    shadow_ticket_id: ShadowTicketIdentifier
    shadow_ticket_title: BoundedText
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    repository_scope: BoundedText
    risk_classification: Literal["non_critical"]
    why_selected: BoundedText
    expected_candidate_paths: tuple[BoundedText, ...] = Field(max_length=16)
    expected_validation: tuple[BoundedText, ...] = Field(min_length=1, max_length=16)
    destructive_side_effects: Literal[False] = False
    production_credentials_required: Literal[False] = False
    provider_model_setup_required: Literal[False] = False
    broad_refactor_required: Literal[False] = False
    ticket_SHA256: DigestText

    @field_validator(
        "shadow_ticket_title",
        "repository_scope",
        "why_selected",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 shadow ticket")

    @field_validator("expected_candidate_paths", "expected_validation", mode="after")
    @classmethod
    def _validate_tuples(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _validate_safe_tuple(value, "P18.7 shadow ticket")

    @model_validator(mode="after")
    def _validate_ticket(self) -> ShadowTicketSelection:
        if self.shadow_ticket_id in {"P18.7", "P18.8"}:
            raise ValueError("P18.7 shadow ticket cannot be P18.7 or P18.8")
        if self.ticket_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_TICKET_DIGEST_ALGORITHM,
            self,
            "ticket_SHA256",
        ):
            raise ValueError("P18.7 shadow ticket digest mismatch")
        return self


class ManualWorkflowBaseline(_ManualHermesShadowModel):
    manual_project_context_source: BoundedText
    manual_ticket_generation_method: BoundedText
    manual_ticket_artifact_SHA256: DigestText
    manual_executor: BoundedText
    manual_execution_trigger: BoundedText
    manual_result_collection_method: BoundedText
    manual_validation_method: BoundedText
    manual_review_method: BoundedText
    manual_approval_method: BoundedText
    manual_Git_handoff_method: BoundedText
    manual_commit_authority: Literal["human"]
    manual_push_authority: Literal["human"]
    manual_copy_paste_steps: int = Field(ge=0, le=100, strict=True)
    manual_context_restatement_steps: int = Field(ge=0, le=100, strict=True)
    manual_confirmation_steps: int = Field(ge=0, le=100, strict=True)
    manual_shell_steps: int = Field(ge=0, le=100, strict=True)
    manual_review_steps: int = Field(ge=0, le=100, strict=True)
    manual_total_human_decisions: int = Field(ge=1, le=100, strict=True)
    raw_conversation_history_persisted: Literal[False] = False
    raw_OpenCode_transcript_persisted: Literal[False] = False
    manual_path_SHA256: DigestText

    @field_validator(
        "manual_project_context_source",
        "manual_ticket_generation_method",
        "manual_executor",
        "manual_execution_trigger",
        "manual_result_collection_method",
        "manual_validation_method",
        "manual_review_method",
        "manual_approval_method",
        "manual_Git_handoff_method",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 manual baseline")

    @model_validator(mode="after")
    def _validate_baseline(self) -> ManualWorkflowBaseline:
        if self.manual_total_human_decisions < self.manual_confirmation_steps:
            raise ValueError("manual decisions cannot be lower than confirmations")
        if self.manual_path_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_MANUAL_DIGEST_ALGORITHM,
            self,
            "manual_path_SHA256",
        ):
            raise ValueError("P18.7 manual baseline digest mismatch")
        return self


class ManualWorkflowAuthorityEntry(_ManualHermesShadowModel):
    action: BoundedText
    current_owner: BoundedText
    human_required: StrictBool
    machine_automated: StrictBool
    evidence_generated: BoundedText
    authority_SHA256: DigestText

    @field_validator("action", "current_owner", "evidence_generated", mode="after")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 authority map")

    @model_validator(mode="after")
    def _validate_entry(self) -> ManualWorkflowAuthorityEntry:
        if self.authority_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_AUTHORITY_DIGEST_ALGORITHM,
            self,
            "authority_SHA256",
        ):
            raise ValueError("P18.7 authority digest mismatch")
        return self


class PepperWorkflowEvidence(_ManualHermesShadowModel):
    implementation_project_id: Literal["PEPPER"]
    implementation_macroproject_id: Literal["P18"]
    implementation_ticket_id: Literal["P18.2"]
    selected_shadow_ticket_id: ShadowTicketIdentifier
    P18_6_commit: CommitSha
    P18_6_result_SHA256: DigestText
    P18_6_recovery_boundary: Literal["RECOVERY_DECISION_ONLY"]
    P18_1_intake_SHA256: DigestText
    P18_2_ticket_factory_result_SHA256: DigestText
    P18_3_approval_result_SHA256: DigestText
    P18_4_queue_result_SHA256: DigestText
    P17_execution_result_SHA256: DigestText
    P17_outcome_envelope_SHA256: DigestText
    P18_5_review_result_SHA256: DigestText
    P18_6_shadow_recovery_result_SHA256: DigestText | None = None
    P17_human_git_handoff_SHA256: DigestText | None = None
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    workflow_state_progression: tuple[BoundedText, ...] = Field(
        min_length=7, max_length=16
    )
    provider_dispatch_count: int = Field(default=0, ge=0, le=100, strict=True)
    model_inference_count: int = Field(default=0, ge=0, le=100, strict=True)
    provider_model_required: StrictBool = False
    compilation_count: int = Field(default=1, ge=0, le=10, strict=True)
    duplicate_Project_Intake_created: Literal[False] = False
    duplicate_Ticket_Factory_created: Literal[False] = False
    duplicate_approval_engine_created: Literal[False] = False
    duplicate_dependency_queue_created: Literal[False] = False
    duplicate_executor_created: Literal[False] = False
    duplicate_validation_runner_created: Literal[False] = False
    duplicate_review_engine_created: Literal[False] = False
    duplicate_recovery_engine_created: Literal[False] = False
    duplicate_Git_handoff_created: Literal[False] = False
    pepper_path_SHA256: DigestText

    @field_validator("WorkPacket_ID", mode="after")
    @classmethod
    def _validate_work_packet(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 Pepper evidence")

    @field_validator("workflow_state_progression", mode="after")
    @classmethod
    def _validate_progression(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _validate_safe_tuple(value, "P18.7 workflow state progression")

    @model_validator(mode="after")
    def _validate_evidence(self) -> PepperWorkflowEvidence:
        if (
            self.P18_6_recovery_boundary
            != RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION
        ):
            raise ValueError("P18.7 must preserve P18.6 recovery boundary")
        if not self.provider_model_required and (
            self.provider_dispatch_count or self.model_inference_count
        ):
            raise ValueError("provider/model counts must be zero when not required")
        if self.pepper_path_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_PEPPER_DIGEST_ALGORITHM,
            self,
            "pepper_path_SHA256",
        ):
            raise ValueError("P18.7 Pepper evidence digest mismatch")
        return self


class ShadowWorkspaceIsolation(_ManualHermesShadowModel):
    manual_execution_workspace: BoundedText
    Pepper_execution_workspace: BoundedText
    isolation_method: BoundedText
    common_parent_commit: CommitSha
    equivalent_initial_state: Literal[True]
    manual_shadow_workspace_state: BoundedText
    Pepper_shadow_workspace_state: BoundedText
    cleanup_required: StrictBool
    cleanup_performed: StrictBool
    destructive_cleanup_performed: Literal[False] = False
    workspace_SHA256: DigestText

    @field_validator(
        "manual_execution_workspace",
        "Pepper_execution_workspace",
        "isolation_method",
        "manual_shadow_workspace_state",
        "Pepper_shadow_workspace_state",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 workspace isolation")

    @model_validator(mode="after")
    def _validate_workspace(self) -> ShadowWorkspaceIsolation:
        if self.cleanup_performed and not self.cleanup_required:
            raise ValueError("cleanup cannot be performed when it was not required")
        if self.workspace_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_WORKSPACE_DIGEST_ALGORITHM,
            self,
            "workspace_SHA256",
        ):
            raise ValueError("P18.7 workspace digest mismatch")
        return self


class ShadowComparisonDimension(_ManualHermesShadowModel):
    dimension: ManualHermesShadowRunStage
    score: ManualHermesShadowRunComparisonScore
    rationale: BoundedText
    manual_evidence_SHA256: DigestText | None = None
    Pepper_evidence_SHA256: DigestText | None = None
    blocks_cutover: StrictBool = False
    comparison_SHA256: DigestText

    @field_validator("rationale", mode="after")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 comparison")

    @model_validator(mode="after")
    def _validate_comparison(self) -> ShadowComparisonDimension:
        if (
            self.score
            in {
                ManualHermesShadowRunComparisonScore.MISMATCH,
                ManualHermesShadowRunComparisonScore.BLOCKED,
            }
            and not self.blocks_cutover
        ):
            raise ValueError("mismatch or blocked comparison must block cutover")
        if self.comparison_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_COMPARISON_DIGEST_ALGORITHM,
            self,
            "comparison_SHA256",
        ):
            raise ValueError("P18.7 comparison digest mismatch")
        return self


class ShadowUIEndpointEvidence(_ManualHermesShadowModel):
    route: BoundedText
    classification: ManualHermesShadowRunUIClassification
    backend_endpoint: BoundedText
    http_status: int | None = Field(default=None, ge=100, le=599)
    response_schema_classification: BoundedText
    sensitive_fields_absent: StrictBool
    authenticated_backend_available: StrictBool
    mutating_action_available: StrictBool
    authority: BoundedText
    endpoint_SHA256: DigestText

    @field_validator(
        "route",
        "backend_endpoint",
        "response_schema_classification",
        "authority",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 UI endpoint")

    @model_validator(mode="after")
    def _validate_endpoint(self) -> ShadowUIEndpointEvidence:
        if self.classification is ManualHermesShadowRunUIClassification.BROKEN:
            if self.http_status is not None and self.http_status < 400:
                raise ValueError("broken endpoint cannot report successful status")
        if self.mutating_action_available and not self.authenticated_backend_available:
            raise ValueError("mutating UI action requires authenticated backend")
        if self.endpoint_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_UI_DIGEST_ALGORITHM,
            self,
            "endpoint_SHA256",
        ):
            raise ValueError("P18.7 UI endpoint digest mismatch")
        return self


class ShadowUIReadinessEvidence(_ManualHermesShadowModel):
    endpoints: tuple[ShadowUIEndpointEvidence, ...] = Field(min_length=5, max_length=16)
    project_visible: StrictBool
    ticket_visible: StrictBool
    workflow_state_visible: StrictBool
    next_required_human_action_visible: StrictBool
    approval_list_live: StrictBool
    approval_detail_live: StrictBool
    approval_action_available_from_UI: StrictBool
    explicit_human_APPROVE_possible_in_Pepper_UI: StrictBool
    explicit_human_REJECT_possible_in_Pepper_UI: StrictBool
    execution_list_live: StrictBool
    execution_detail_live: StrictBool
    WorkPacket_identity_visible: StrictBool
    execution_state_visible: StrictBool
    validation_state_visible: StrictBool
    review_state_visible: StrictBool
    failure_cancellation_visible: StrictBool
    Git_handoff_readiness_visible: StrictBool
    human_ui_smoke: ManualHermesShadowRunHumanSmokeStatus
    ui_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_ui(self) -> ShadowUIReadinessEvidence:
        routes = tuple(endpoint.route for endpoint in self.endpoints)
        required_routes = (
            "/agent-platform/projects",
            "/agent-platform/projects/:boardSlug",
            "/agent-platform/projects/:boardSlug/tickets/:taskId",
            "/agent-platform/approvals",
            "/agent-platform/executions",
        )
        for route in required_routes:
            if route not in routes:
                raise ValueError(f"P18.7 UI evidence missing route {route}")
        if self.approval_action_available_from_UI and not (
            self.explicit_human_APPROVE_possible_in_Pepper_UI
            and self.explicit_human_REJECT_possible_in_Pepper_UI
        ):
            raise ValueError("approval UI action must expose approve and reject")
        if self.ui_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_UI_DIGEST_ALGORITHM,
            self,
            "ui_SHA256",
        ):
            raise ValueError("P18.7 UI readiness digest mismatch")
        return self


class ShadowDependencyAudit(_ManualHermesShadowModel):
    roadmap_state: ManualHermesShadowRunDependencyPosture
    project_context: ManualHermesShadowRunDependencyPosture
    ticket_generation: ManualHermesShadowRunDependencyPosture
    approval_decision_storage: ManualHermesShadowRunDependencyPosture
    review: ManualHermesShadowRunDependencyPosture
    recovery_decision: ManualHermesShadowRunDependencyPosture
    next_action: ManualHermesShadowRunDependencyPosture
    Git_handoff_construction: ManualHermesShadowRunDependencyPosture
    normal_workflow_requires_this_chat: StrictBool
    audit_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_audit(self) -> ShadowDependencyAudit:
        required_present = any(
            value is ManualHermesShadowRunDependencyPosture.REQUIRED
            for value in (
                self.roadmap_state,
                self.project_context,
                self.ticket_generation,
                self.approval_decision_storage,
                self.review,
                self.recovery_decision,
                self.next_action,
                self.Git_handoff_construction,
            )
        )
        if self.normal_workflow_requires_this_chat != required_present:
            raise ValueError("chat dependency flag must derive from required fields")
        if self.audit_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM,
            self,
            "audit_SHA256",
        ):
            raise ValueError("P18.7 chat dependency digest mismatch")
        return self


class ShadowOpenCodeDependencyAudit(_ManualHermesShadowModel):
    manual_OpenCode_ticket_paste: StrictBool
    manual_OpenCode_start: StrictBool
    manual_OpenCode_result_copy: StrictBool
    manual_OpenCode_result_interpretation: StrictBool
    manual_OpenCode_ticket_paste_count: int = Field(ge=0, le=100, strict=True)
    manual_OpenCode_start_count: int = Field(ge=0, le=100, strict=True)
    manual_OpenCode_result_copy_count: int = Field(ge=0, le=100, strict=True)
    manual_OpenCode_result_interpretation_count: int = Field(ge=0, le=100, strict=True)
    audit_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_audit(self) -> ShadowOpenCodeDependencyAudit:
        pairs = (
            (
                self.manual_OpenCode_ticket_paste,
                self.manual_OpenCode_ticket_paste_count,
            ),
            (self.manual_OpenCode_start, self.manual_OpenCode_start_count),
            (self.manual_OpenCode_result_copy, self.manual_OpenCode_result_copy_count),
            (
                self.manual_OpenCode_result_interpretation,
                self.manual_OpenCode_result_interpretation_count,
            ),
        )
        if any(flag != bool(count) for flag, count in pairs):
            raise ValueError("OpenCode dependency flags must derive from counts")
        if self.audit_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM,
            self,
            "audit_SHA256",
        ):
            raise ValueError("P18.7 OpenCode dependency digest mismatch")
        return self


class ShadowContextPersistenceAudit(_ManualHermesShadowModel):
    minimum_project_context_persisted: tuple[BoundedText, ...] = Field(
        min_length=1, max_length=16
    )
    missing_context_classes: tuple[BoundedText, ...] = Field(max_length=16)
    GBrain_required_for_P18_8: Literal[False] = False
    Paperclip_required_for_P18_8: Literal[False] = False
    next_ticket_requires_historic_chat_memory: StrictBool
    P18_8_context_blocker: StrictBool
    audit_SHA256: DigestText

    @field_validator(
        "minimum_project_context_persisted", "missing_context_classes", mode="after"
    )
    @classmethod
    def _validate_tuples(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _validate_safe_tuple(value, "P18.7 context persistence audit")

    @model_validator(mode="after")
    def _validate_audit(self) -> ShadowContextPersistenceAudit:
        if self.P18_8_context_blocker != self.next_ticket_requires_historic_chat_memory:
            raise ValueError(
                "P18.8 context blocker must derive from historic-chat need"
            )
        if self.audit_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM,
            self,
            "audit_SHA256",
        ):
            raise ValueError("P18.7 context audit digest mismatch")
        return self


class ShadowMigrationGap(_ManualHermesShadowModel):
    gap_id: MigrationGapIdentifier
    category: ManualHermesShadowRunGapCategory
    severity: ManualHermesShadowRunGapSeverity
    affected_workflow_stage: ManualHermesShadowRunStage
    current_manual_workaround: BoundedText
    required_P18_8_correction: BoundedText
    blocks_cutover: StrictBool
    evidence: BoundedText
    gap_SHA256: DigestText

    @field_validator(
        "current_manual_workaround",
        "required_P18_8_correction",
        "evidence",
        mode="after",
    )
    @classmethod
    def _validate_text(cls, value: str) -> str:
        return _validate_safe_text(value, "P18.7 migration gap")

    @model_validator(mode="after")
    def _validate_gap(self) -> ShadowMigrationGap:
        if self.severity is ManualHermesShadowRunGapSeverity.BLOCKER:
            if not self.blocks_cutover:
                raise ValueError("blocker severity must block cutover")
        if self.gap_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_GAP_DIGEST_ALGORITHM,
            self,
            "gap_SHA256",
        ):
            raise ValueError("P18.7 migration gap digest mismatch")
        return self


class ShadowOperatorEffort(_ManualHermesShadowModel):
    manual_path_elapsed_minutes: int = Field(ge=0, le=10000, strict=True)
    Pepper_path_elapsed_minutes: int = Field(ge=0, le=10000, strict=True)
    manual_human_interactions: int = Field(ge=0, le=100, strict=True)
    Pepper_human_interactions: int = Field(ge=0, le=100, strict=True)
    manual_copy_paste_count: int = Field(ge=0, le=100, strict=True)
    Pepper_manual_copy_paste_count: int = Field(ge=0, le=100, strict=True)
    manual_explicit_approvals: int = Field(ge=0, le=20, strict=True)
    Pepper_explicit_approvals: int = Field(ge=0, le=20, strict=True)
    effort_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_effort(self) -> ShadowOperatorEffort:
        if self.manual_copy_paste_count > self.manual_human_interactions:
            raise ValueError("manual copy/paste cannot exceed interactions")
        if self.Pepper_manual_copy_paste_count > self.Pepper_human_interactions:
            raise ValueError("Pepper copy/paste cannot exceed interactions")
        if self.effort_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_EFFORT_DIGEST_ALGORITHM,
            self,
            "effort_SHA256",
        ):
            raise ValueError("P18.7 effort digest mismatch")
        return self


class ShadowGitHandoffComparison(_ManualHermesShadowModel):
    candidate_paths_exact: StrictBool
    staging_boundaries_exact: StrictBool
    diff_check_present: StrictBool
    staged_verification_present: StrictBool
    commit_message_present: StrictBool
    push_target_present: StrictBool
    human_only_execution_preserved: Literal[True]
    automatic_git_add: Literal[False] = False
    automatic_git_commit: Literal[False] = False
    automatic_git_push: Literal[False] = False
    Git_handoff_eligible: StrictBool
    handoff_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_handoff(self) -> ShadowGitHandoffComparison:
        required = all((
            self.candidate_paths_exact,
            self.staging_boundaries_exact,
            self.diff_check_present,
            self.staged_verification_present,
            self.commit_message_present,
            self.push_target_present,
        ))
        if self.Git_handoff_eligible != required:
            raise ValueError(
                "Git handoff eligibility must derive from comparison fields"
            )
        if self.handoff_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_GIT_DIGEST_ALGORITHM,
            self,
            "handoff_SHA256",
        ):
            raise ValueError("P18.7 Git handoff digest mismatch")
        return self


class ManualHermesShadowRunRequest(_ManualHermesShadowModel):
    schema_version: Literal[1] = MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION
    policy_id: Literal["pepper-manual-hermes-shadow-run-v1"] = (
        MANUAL_HERMES_SHADOW_RUN_POLICY_ID
    )
    P18_6_commit: CommitSha
    P18_6_result_SHA256: DigestText
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    implementation_lineage_ticket_id: Literal["P18.2"]
    recovery_boundary: Literal["RECOVERY_DECISION_ONLY"]
    shadow_ticket: ShadowTicketSelection
    manual_baseline: ManualWorkflowBaseline
    manual_authority_map: tuple[ManualWorkflowAuthorityEntry, ...] = Field(
        min_length=12, max_length=32
    )
    Pepper_evidence: PepperWorkflowEvidence
    workspace_isolation: ShadowWorkspaceIsolation
    comparisons: tuple[ShadowComparisonDimension, ...] = Field(
        min_length=15, max_length=24
    )
    UI_readiness: ShadowUIReadinessEvidence
    chat_dependency_audit: ShadowDependencyAudit
    OpenCode_dependency_audit: ShadowOpenCodeDependencyAudit
    context_persistence_audit: ShadowContextPersistenceAudit
    migration_gaps: tuple[ShadowMigrationGap, ...] = Field(max_length=32)
    operator_effort: ShadowOperatorEffort
    Git_handoff_comparison: ShadowGitHandoffComparison
    request_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_request(self) -> ManualHermesShadowRunRequest:
        if self.recovery_boundary != RETRY_INCIDENT_ROLLBACK_BOUNDARY_CLASSIFICATION:
            raise ValueError("P18.7 request must preserve P18.6 recovery boundary")
        if self.P18_6_commit != self.Pepper_evidence.P18_6_commit:
            raise ValueError("P18.6 commit mismatch")
        if self.P18_6_result_SHA256 != self.Pepper_evidence.P18_6_result_SHA256:
            raise ValueError("P18.6 result digest mismatch")
        if (
            self.shadow_ticket.shadow_ticket_id
            != self.Pepper_evidence.selected_shadow_ticket_id
        ):
            raise ValueError("selected shadow ticket mismatch")
        dimensions = tuple(comparison.dimension for comparison in self.comparisons)
        required = tuple(ManualHermesShadowRunStage)
        missing = [dimension for dimension in required if dimension not in dimensions]
        if missing:
            raise ValueError("P18.7 comparison dimensions incomplete")
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("P18.7 comparison dimensions must be unique")
        gap_ids = tuple(gap.gap_id for gap in self.migration_gaps)
        if len(gap_ids) != len(set(gap_ids)):
            raise ValueError("P18.7 migration gap IDs must be unique")
        if self.request_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_REQUEST_DIGEST_ALGORITHM,
            self,
            "request_SHA256",
        ):
            raise ValueError("P18.7 request digest mismatch")
        return self


class ManualHermesShadowRunSummary(_ManualHermesShadowModel):
    semantic_shadow_equivalence: StrictBool
    governance_equivalence: StrictBool
    authority_equivalence: StrictBool
    Pepper_authority_stricter_or_equal: StrictBool
    UI_operational: StrictBool
    Projects_operational: StrictBool
    Tickets_operational: StrictBool
    Approvals_operational: StrictBool
    Executions_operational: StrictBool
    review_visibility_operational: StrictBool
    next_action_visible: StrictBool
    normal_workflow_requires_chat: StrictBool
    manual_OpenCode_ticket_copy_required: StrictBool
    manual_OpenCode_result_copy_required: StrictBool
    cutover_blocking_gap_count: int = Field(ge=0, le=32, strict=True)
    P18_8_ready: ManualHermesShadowRunReadinessDecision
    shadow_run_valid: Literal[True]
    warning_gap_count: int = Field(ge=0, le=32, strict=True)
    informational_gap_count: int = Field(ge=0, le=32, strict=True)
    comparison_dimension_count: Literal[15]
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> ManualHermesShadowRunSummary:
        ready = all((
            self.semantic_shadow_equivalence,
            self.governance_equivalence,
            self.Pepper_authority_stricter_or_equal,
            self.Projects_operational,
            self.Tickets_operational,
            self.Approvals_operational,
            self.Executions_operational,
            self.review_visibility_operational,
            self.next_action_visible,
            not self.normal_workflow_requires_chat,
            not self.manual_OpenCode_ticket_copy_required,
            not self.manual_OpenCode_result_copy_required,
            self.cutover_blocking_gap_count == 0,
        ))
        expected = (
            ManualHermesShadowRunReadinessDecision.P18_8_READY
            if ready
            else ManualHermesShadowRunReadinessDecision.P18_8_BLOCKED
        )
        if self.P18_8_ready is not expected:
            raise ValueError("P18.8 readiness decision mismatch")
        if self.authority_equivalence != self.Pepper_authority_stricter_or_equal:
            raise ValueError("authority equivalence must match strict-or-equal flag")
        if self.UI_operational != all((
            self.Projects_operational,
            self.Tickets_operational,
            self.Approvals_operational,
            self.Executions_operational,
            self.review_visibility_operational,
            self.next_action_visible,
        )):
            raise ValueError("UI operational flag must derive from UI subflags")
        if self.summary_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_SUMMARY_DIGEST_ALGORITHM,
            self,
            "summary_SHA256",
        ):
            raise ValueError("P18.7 summary digest mismatch")
        return self


class ManualHermesShadowRunResult(_ManualHermesShadowModel):
    schema_version: Literal[1] = MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION
    policy_id: Literal["pepper-manual-hermes-shadow-run-v1"] = (
        MANUAL_HERMES_SHADOW_RUN_POLICY_ID
    )
    decision: ManualHermesShadowRunDecision
    request: ManualHermesShadowRunRequest
    summary: ManualHermesShadowRunSummary
    shadow_ticket_id: ShadowTicketIdentifier
    common_parent_commit: CommitSha
    manual_path_digest: DigestText
    Pepper_path_digest: DigestText
    semantic_comparison_digest: DigestText
    authority_comparison_digest: DigestText
    UI_readiness_digest: DigestText
    migration_gap_digest: DigestText
    P18_8_ready: ManualHermesShadowRunReadinessDecision
    provider_dispatch_count: Literal[0]
    model_inference_count: Literal[0]
    subprocess_calls: Literal[0]
    shell_calls: Literal[0]
    filesystem_calls: Literal[0]
    Git_calls: Literal[0]
    network_calls: Literal[0]
    Docker_calls: Literal[0]
    Graphify_calls: Literal[0]
    database_calls: Literal[0]
    direct_Kanban_mutation_calls: Literal[0]
    direct_dispatcher_calls: Literal[0]
    direct_worker_calls: Literal[0]
    direct_validation_runner_calls: Literal[0]
    direct_review_engine_calls: Literal[0]
    direct_recovery_engine_calls: Literal[0]
    staging_calls: Literal[0]
    commit_calls: Literal[0]
    push_calls: Literal[0]
    automatic_git_add: Literal[False]
    automatic_git_commit: Literal[False]
    automatic_git_push: Literal[False]
    duplicate_Project_Intake_created: Literal[False]
    duplicate_Ticket_Factory_created: Literal[False]
    duplicate_approval_engine_created: Literal[False]
    duplicate_dependency_queue_created: Literal[False]
    duplicate_executor_created: Literal[False]
    duplicate_validation_runner_created: Literal[False]
    duplicate_review_engine_created: Literal[False]
    duplicate_recovery_engine_created: Literal[False]
    duplicate_Git_handoff_created: Literal[False]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ManualHermesShadowRunResult:
        if self.shadow_ticket_id != self.request.shadow_ticket.shadow_ticket_id:
            raise ValueError("P18.7 result shadow ticket mismatch")
        if (
            self.common_parent_commit
            != self.request.workspace_isolation.common_parent_commit
        ):
            raise ValueError("P18.7 common parent mismatch")
        if self.P18_8_ready is not self.summary.P18_8_ready:
            raise ValueError("P18.7 readiness mismatch")
        if self.manual_path_digest != self.request.manual_baseline.manual_path_SHA256:
            raise ValueError("P18.7 manual path digest mismatch")
        if self.Pepper_path_digest != self.request.Pepper_evidence.pepper_path_SHA256:
            raise ValueError("P18.7 Pepper path digest mismatch")
        if self.UI_readiness_digest != self.request.UI_readiness.ui_SHA256:
            raise ValueError("P18.7 UI readiness digest mismatch")
        if any((
            self.provider_dispatch_count,
            self.model_inference_count,
            self.subprocess_calls,
            self.shell_calls,
            self.filesystem_calls,
            self.Git_calls,
            self.network_calls,
            self.Docker_calls,
            self.Graphify_calls,
            self.database_calls,
            self.direct_Kanban_mutation_calls,
            self.direct_dispatcher_calls,
            self.direct_worker_calls,
            self.direct_validation_runner_calls,
            self.direct_review_engine_calls,
            self.direct_recovery_engine_calls,
            self.staging_calls,
            self.commit_calls,
            self.push_calls,
        )):
            raise ValueError("P18.7 result must not execute runtime actions")
        if self.result_SHA256 != _model_digest(
            MANUAL_HERMES_SHADOW_RESULT_DIGEST_ALGORITHM,
            self,
            "result_SHA256",
        ):
            raise ValueError("P18.7 result digest mismatch")
        return self


def _build_authority_entry(
    *,
    action: str,
    current_owner: str,
    human_required: bool,
    machine_automated: bool,
    evidence_generated: str,
) -> ManualWorkflowAuthorityEntry:
    return _make_model(
        ManualWorkflowAuthorityEntry,
        "authority_SHA256",
        MANUAL_HERMES_SHADOW_AUTHORITY_DIGEST_ALGORITHM,
        action=action,
        current_owner=current_owner,
        human_required=human_required,
        machine_automated=machine_automated,
        evidence_generated=evidence_generated,
    )


def build_manual_hermes_shadow_authority_map() -> tuple[
    ManualWorkflowAuthorityEntry, ...
]:
    rows = (
        (
            "project selection",
            "human plus lead agent",
            True,
            False,
            "bounded project identity",
        ),
        (
            "ticket generation",
            "lead agent",
            True,
            True,
            "bounded ticket artifact digest",
        ),
        ("ticket approval", "human", True, False, "explicit approval decision"),
        (
            "execution authorization",
            "human",
            True,
            False,
            "bounded execution authorization",
        ),
        ("execution", "OpenCode worker", False, True, "bounded outcome evidence"),
        ("validation", "operator shell", True, True, "validation command evidence"),
        ("review", "human plus lead agent", True, False, "review decision evidence"),
        ("retry decision", "human", True, False, "manual recovery decision"),
        ("rollback decision", "human", True, False, "manual rollback posture"),
        ("Git staging", "human", True, False, "staging command boundary"),
        ("Git commit", "human", True, False, "commit command boundary"),
        ("Git push", "human", True, False, "push target boundary"),
        (
            "next-ticket selection",
            "human plus lead agent",
            True,
            False,
            "roadmap handoff",
        ),
    )
    return tuple(
        _build_authority_entry(
            action=action,
            current_owner=owner,
            human_required=human,
            machine_automated=automated,
            evidence_generated=evidence,
        )
        for action, owner, human, automated, evidence in rows
    )


def _build_comparison(
    *,
    dimension: ManualHermesShadowRunStage,
    score: ManualHermesShadowRunComparisonScore,
    rationale: str,
    manual_evidence_SHA256: str | None,
    Pepper_evidence_SHA256: str | None,
    blocks_cutover: bool = False,
) -> ShadowComparisonDimension:
    return _make_model(
        ShadowComparisonDimension,
        "comparison_SHA256",
        MANUAL_HERMES_SHADOW_COMPARISON_DIGEST_ALGORITHM,
        dimension=dimension,
        score=score,
        rationale=rationale,
        manual_evidence_SHA256=manual_evidence_SHA256,
        Pepper_evidence_SHA256=Pepper_evidence_SHA256,
        blocks_cutover=blocks_cutover,
    )


def build_manual_hermes_shadow_comparison_dimensions(
    *,
    manual_digest: str,
    Pepper_digest: str,
    UI_blocked: bool = True,
    chat_required: bool = True,
) -> tuple[ShadowComparisonDimension, ...]:
    ui_score = (
        ManualHermesShadowRunComparisonScore.BLOCKED
        if UI_blocked
        else ManualHermesShadowRunComparisonScore.MATCH
    )
    effort_score = (
        ManualHermesShadowRunComparisonScore.MANUAL_BETTER
        if chat_required
        else ManualHermesShadowRunComparisonScore.PEPPER_BETTER
    )
    rows = (
        (
            ManualHermesShadowRunStage.PROJECT_CONTEXT,
            ManualHermesShadowRunComparisonScore.EQUIVALENT,
            "Pepper preserves bounded project context without storing raw chats.",
            False,
        ),
        (
            ManualHermesShadowRunStage.TICKET_SEMANTICS,
            ManualHermesShadowRunComparisonScore.EQUIVALENT,
            "Manual ticket objective, scope and constraints are preserved semantically.",
            False,
        ),
        (
            ManualHermesShadowRunStage.APPROVAL,
            ManualHermesShadowRunComparisonScore.EQUIVALENT,
            "Pepper records independent explicit human approval evidence.",
            False,
        ),
        (
            ManualHermesShadowRunStage.DEPENDENCY_GATE,
            ManualHermesShadowRunComparisonScore.MATCH,
            "Both paths treat the selected safe shadow work item as dependency-satisfied.",
            False,
        ),
        (
            ManualHermesShadowRunStage.EXECUTION,
            ManualHermesShadowRunComparisonScore.EQUIVALENT,
            "Execution evidence is bounded to the selected read-only route smoke work item.",
            False,
        ),
        (
            ManualHermesShadowRunStage.VALIDATION,
            ManualHermesShadowRunComparisonScore.MATCH,
            "Both paths rely on deterministic route and workflow regression validation.",
            False,
        ),
        (
            ManualHermesShadowRunStage.REVIEW,
            ManualHermesShadowRunComparisonScore.EQUIVALENT,
            "Pepper P18.5 review semantics match manual review outcome classification.",
            False,
        ),
        (
            ManualHermesShadowRunStage.RECOVERY,
            ManualHermesShadowRunComparisonScore.MATCH,
            "No natural failure occurred, so recovery is fixture-backed and non-destructive.",
            False,
        ),
        (
            ManualHermesShadowRunStage.GIT_HANDOFF,
            ManualHermesShadowRunComparisonScore.MATCH,
            "Human-only Git handoff boundaries remain exact.",
            False,
        ),
        (
            ManualHermesShadowRunStage.WORKFLOW_STATE,
            ManualHermesShadowRunComparisonScore.EQUIVALENT,
            "Pepper exposes deterministic workflow-state evidence over manual milestones.",
            False,
        ),
        (
            ManualHermesShadowRunStage.UI_VISIBILITY,
            ui_score,
            "UI lacks required live approval or execution operation visibility."
            if UI_blocked
            else "UI exposes required workflow visibility and actions.",
            UI_blocked,
        ),
        (
            ManualHermesShadowRunStage.OPERATOR_EFFORT,
            effort_score,
            "Manual chat and OpenCode transfer remain required."
            if chat_required
            else "Pepper removes normal workflow control copy/paste.",
            chat_required,
        ),
        (
            ManualHermesShadowRunStage.AUTHORITY,
            ManualHermesShadowRunComparisonScore.PEPPER_BETTER,
            "Pepper authority is stricter or equal to manual authority.",
            False,
        ),
        (
            ManualHermesShadowRunStage.SECURITY,
            ManualHermesShadowRunComparisonScore.MATCH,
            "Neither path persists credentials, tokens, raw transcripts or hidden reasoning.",
            False,
        ),
        (
            ManualHermesShadowRunStage.EVIDENCE_COMPLETENESS,
            ManualHermesShadowRunComparisonScore.PEPPER_BETTER,
            "Pepper evidence is deterministic and digest-bound across workflow stages.",
            False,
        ),
    )
    return tuple(
        _build_comparison(
            dimension=dimension,
            score=score,
            rationale=rationale,
            manual_evidence_SHA256=manual_digest,
            Pepper_evidence_SHA256=Pepper_digest,
            blocks_cutover=blocks,
        )
        for dimension, score, rationale, blocks in rows
    )


def _build_endpoint(
    *,
    route: str,
    classification: ManualHermesShadowRunUIClassification,
    backend_endpoint: str,
    http_status: int | None,
    response_schema_classification: str,
    sensitive_fields_absent: bool,
    authenticated_backend_available: bool,
    mutating_action_available: bool,
    authority: str,
) -> ShadowUIEndpointEvidence:
    return _make_model(
        ShadowUIEndpointEvidence,
        "endpoint_SHA256",
        MANUAL_HERMES_SHADOW_UI_DIGEST_ALGORITHM,
        route=route,
        classification=classification,
        backend_endpoint=backend_endpoint,
        http_status=http_status,
        response_schema_classification=response_schema_classification,
        sensitive_fields_absent=sensitive_fields_absent,
        authenticated_backend_available=authenticated_backend_available,
        mutating_action_available=mutating_action_available,
        authority=authority,
    )


def build_manual_hermes_shadow_ui_endpoints(
    *,
    approval_backend_live: bool = False,
    execution_backend_live: bool = False,
) -> tuple[ShadowUIEndpointEvidence, ...]:
    approval_classification = (
        ManualHermesShadowRunUIClassification.FUNCTIONAL_LIVE_BACKEND
        if approval_backend_live
        else ManualHermesShadowRunUIClassification.UNAVAILABLE_BACKEND
    )
    execution_classification = (
        ManualHermesShadowRunUIClassification.FUNCTIONAL_LIVE_BACKEND
        if execution_backend_live
        else ManualHermesShadowRunUIClassification.FUNCTIONAL_READ_ONLY_PROJECTION
    )
    return (
        _build_endpoint(
            route="/agent-platform/projects",
            classification=ManualHermesShadowRunUIClassification.FUNCTIONAL_READ_ONLY_PROJECTION,
            backend_endpoint="/api/plugins/kanban/boards",
            http_status=200,
            response_schema_classification="bounded board list projection",
            sensitive_fields_absent=True,
            authenticated_backend_available=True,
            mutating_action_available=False,
            authority="read-only project projection",
        ),
        _build_endpoint(
            route="/agent-platform/projects/:boardSlug",
            classification=ManualHermesShadowRunUIClassification.FUNCTIONAL_READ_ONLY_PROJECTION,
            backend_endpoint="/api/plugins/kanban/board",
            http_status=200,
            response_schema_classification="bounded board detail projection",
            sensitive_fields_absent=True,
            authenticated_backend_available=True,
            mutating_action_available=False,
            authority="read-only ticket projection",
        ),
        _build_endpoint(
            route="/agent-platform/projects/:boardSlug/tickets/:taskId",
            classification=ManualHermesShadowRunUIClassification.FUNCTIONAL_READ_ONLY_PROJECTION,
            backend_endpoint="/api/plugins/kanban/tasks/{task_id}",
            http_status=200,
            response_schema_classification="bounded task detail projection",
            sensitive_fields_absent=True,
            authenticated_backend_available=True,
            mutating_action_available=False,
            authority="read-only task projection",
        ),
        _build_endpoint(
            route="/agent-platform/approvals",
            classification=approval_classification,
            backend_endpoint="not-yet-established approval HTTP backend"
            if not approval_backend_live
            else "/api/agent-platform/approvals",
            http_status=None if not approval_backend_live else 200,
            response_schema_classification="unavailable production approval source"
            if not approval_backend_live
            else "bounded approval list",
            sensitive_fields_absent=True,
            authenticated_backend_available=approval_backend_live,
            mutating_action_available=approval_backend_live,
            authority="human approval required",
        ),
        _build_endpoint(
            route="/agent-platform/executions",
            classification=execution_classification,
            backend_endpoint="/api/plugins/kanban/tasks/{task_id}"
            if not execution_backend_live
            else "/api/agent-platform/executions",
            http_status=200 if execution_backend_live else None,
            response_schema_classification="qualified read-only execution projection"
            if not execution_backend_live
            else "bounded execution list",
            sensitive_fields_absent=True,
            authenticated_backend_available=execution_backend_live,
            mutating_action_available=False,
            authority="read-only execution projection",
        ),
        _build_endpoint(
            route="/agent-platform/executions/:executionId",
            classification=execution_classification,
            backend_endpoint="/api/plugins/kanban/tasks/{task_id}",
            http_status=200 if execution_backend_live else None,
            response_schema_classification="qualified execution detail projection",
            sensitive_fields_absent=True,
            authenticated_backend_available=execution_backend_live,
            mutating_action_available=False,
            authority="read-only execution detail",
        ),
    )


def _build_gap(
    *,
    gap_id: str,
    category: ManualHermesShadowRunGapCategory,
    affected_workflow_stage: ManualHermesShadowRunStage,
    current_manual_workaround: str,
    required_P18_8_correction: str,
    evidence: str,
    severity: ManualHermesShadowRunGapSeverity = ManualHermesShadowRunGapSeverity.BLOCKER,
    blocks_cutover: bool = True,
) -> ShadowMigrationGap:
    return _make_model(
        ShadowMigrationGap,
        "gap_SHA256",
        MANUAL_HERMES_SHADOW_GAP_DIGEST_ALGORITHM,
        gap_id=gap_id,
        category=category,
        severity=severity,
        affected_workflow_stage=affected_workflow_stage,
        current_manual_workaround=current_manual_workaround,
        required_P18_8_correction=required_P18_8_correction,
        blocks_cutover=blocks_cutover,
        evidence=evidence,
    )


def _build_default_gaps(
    *,
    approval_backend_live: bool,
    execution_backend_live: bool,
    chat_required: bool,
    opencode_copy_required: bool,
) -> tuple[ShadowMigrationGap, ...]:
    gaps: list[ShadowMigrationGap] = []
    if not approval_backend_live:
        gaps.append(
            _build_gap(
                gap_id="P18-8-GAP-001",
                category=ManualHermesShadowRunGapCategory.UI_BACKEND_GAP,
                affected_workflow_stage=ManualHermesShadowRunStage.APPROVAL,
                current_manual_workaround="approval decision remains captured outside Pepper UI",
                required_P18_8_correction="add authenticated approval list detail and approve reject actions",
                evidence="approvals UI route has no live production approval HTTP source",
            )
        )
    if not execution_backend_live:
        gaps.append(
            _build_gap(
                gap_id="P18-8-GAP-002",
                category=ManualHermesShadowRunGapCategory.EXECUTOR_INTEGRATION_GAP,
                affected_workflow_stage=ManualHermesShadowRunStage.EXECUTION,
                current_manual_workaround="operator still reads execution state outside governed execution UI",
                required_P18_8_correction="add live governed execution collection detail and status projection",
                evidence="executions UI is limited to qualified read-only Kanban task evidence",
            )
        )
    if chat_required:
        gaps.append(
            _build_gap(
                gap_id="P18-8-GAP-003",
                category=ManualHermesShadowRunGapCategory.CONTEXT_GAP,
                affected_workflow_stage=ManualHermesShadowRunStage.PROJECT_CONTEXT,
                current_manual_workaround="roadmap and next action are restated through this chat",
                required_P18_8_correction="surface roadmap state current ticket and next action in Pepper UI",
                evidence="normal workflow control still depends on chat for context and handoff",
            )
        )
    if opencode_copy_required:
        gaps.append(
            _build_gap(
                gap_id="P18-8-GAP-004",
                category=ManualHermesShadowRunGapCategory.HUMAN_ACTION_GAP,
                affected_workflow_stage=ManualHermesShadowRunStage.EXECUTION,
                current_manual_workaround="operator manually transfers ticket and result to and from OpenCode",
                required_P18_8_correction="bridge accepted worker invocation and result ingestion through Pepper",
                evidence="manual OpenCode ticket paste or result copy remains required",
            )
        )
    return tuple(gaps)


def build_canonical_p18_manual_hermes_shadow_run_request(
    *,
    P18_6_commit: str,
    P18_6_result_SHA256: str,
    common_parent_commit: str,
    UI_blocked: bool = True,
    chat_required: bool = True,
    opencode_copy_required: bool = True,
    authority_regression: bool = False,
) -> ManualHermesShadowRunRequest:
    if authority_regression:
        raise ManualHermesShadowRunPolicyError(
            "Pepper authority regression blocks P18.7"
        )
    approval_backend_live = not UI_blocked
    execution_backend_live = not UI_blocked
    shadow_ticket = _make_model(
        ShadowTicketSelection,
        "ticket_SHA256",
        MANUAL_HERMES_SHADOW_TICKET_DIGEST_ALGORITHM,
        shadow_ticket_id="P18.UI-A-SHADOW-ROUTE-SMOKE",
        shadow_ticket_title="Agent Platform route-readiness shadow smoke",
        project_id="PEPPER",
        macroproject_id="P18",
        repository_scope="Agent Platform UI route and backend readiness projection",
        risk_classification="non_critical",
        why_selected="bounded read-only validation of accepted product UI activation surfaces",
        expected_candidate_paths=(
            "web/src/agent-platform/product-ui-activation-canonical.test.ts",
        ),
        expected_validation=(
            "frontend route activation smoke",
            "P18 workflow regression lane",
        ),
        destructive_side_effects=False,
        production_credentials_required=False,
        provider_model_setup_required=False,
        broad_refactor_required=False,
    )
    manual_baseline = _make_model(
        ManualWorkflowBaseline,
        "manual_path_SHA256",
        MANUAL_HERMES_SHADOW_MANUAL_DIGEST_ALGORITHM,
        manual_project_context_source="bounded roadmap state from current operator conversation",
        manual_ticket_generation_method="lead agent summarizes the next bounded ticket",
        manual_ticket_artifact_SHA256=_stable_digest("manual shadow ticket artifact"),
        manual_executor="OpenCode operator session",
        manual_execution_trigger="human sends ticket to executor",
        manual_result_collection_method="bounded evidence pasted back by operator",
        manual_validation_method="operator runs focused validation commands",
        manual_review_method="human and lead agent review bounded evidence",
        manual_approval_method="human textual approval",
        manual_Git_handoff_method="lead agent gives exact human Git commands",
        manual_commit_authority="human",
        manual_push_authority="human",
        manual_copy_paste_steps=5,
        manual_context_restatement_steps=2,
        manual_confirmation_steps=2,
        manual_shell_steps=4,
        manual_review_steps=2,
        manual_total_human_decisions=4,
        raw_conversation_history_persisted=False,
        raw_OpenCode_transcript_persisted=False,
    )
    pepper_evidence = _make_model(
        PepperWorkflowEvidence,
        "pepper_path_SHA256",
        MANUAL_HERMES_SHADOW_PEPPER_DIGEST_ALGORITHM,
        implementation_project_id="PEPPER",
        implementation_macroproject_id="P18",
        implementation_ticket_id="P18.2",
        selected_shadow_ticket_id=shadow_ticket.shadow_ticket_id,
        P18_6_commit=P18_6_commit,
        P18_6_result_SHA256=P18_6_result_SHA256,
        P18_6_recovery_boundary="RECOVERY_DECISION_ONLY",
        P18_1_intake_SHA256=_stable_digest("P18.7 canonical intake evidence"),
        P18_2_ticket_factory_result_SHA256=_stable_digest(
            "P18.7 canonical ticket factory evidence"
        ),
        P18_3_approval_result_SHA256=_stable_digest(
            "P18.7 canonical approval evidence"
        ),
        P18_4_queue_result_SHA256=_stable_digest("P18.7 canonical queue evidence"),
        P17_execution_result_SHA256=_stable_digest(
            "P18.7 canonical execution evidence"
        ),
        P17_outcome_envelope_SHA256=_stable_digest("P18.7 canonical outcome envelope"),
        P18_5_review_result_SHA256=_stable_digest("P18.7 canonical review evidence"),
        P18_6_shadow_recovery_result_SHA256=_stable_digest(
            "P18.7 canonical fixture recovery evidence"
        ),
        P17_human_git_handoff_SHA256=_stable_digest(
            "P18.7 canonical human Git handoff"
        ),
        WorkPacket_ID="WP-P18-UI-A-SHADOW-R0001",
        WorkPacket_SHA256=_stable_digest("P18.7 canonical WorkPacket"),
        workflow_state_progression=(
            "draft",
            "intake_ready",
            "awaiting_ticket_approval",
            "ticket_approved",
            "work_packet_ready",
            "completed",
            "accepted",
            "human_git_handoff_ready",
        ),
        provider_dispatch_count=0,
        model_inference_count=0,
        provider_model_required=False,
        compilation_count=1,
        duplicate_Project_Intake_created=False,
        duplicate_Ticket_Factory_created=False,
        duplicate_approval_engine_created=False,
        duplicate_dependency_queue_created=False,
        duplicate_executor_created=False,
        duplicate_validation_runner_created=False,
        duplicate_review_engine_created=False,
        duplicate_recovery_engine_created=False,
        duplicate_Git_handoff_created=False,
    )
    workspace_isolation = _make_model(
        ShadowWorkspaceIsolation,
        "workspace_SHA256",
        MANUAL_HERMES_SHADOW_WORKSPACE_DIGEST_ALGORITHM,
        manual_execution_workspace="manual-shadow-read-only-projection",
        Pepper_execution_workspace="pepper-shadow-read-only-projection",
        isolation_method="deterministic read-only evidence mode over common committed checkout",
        common_parent_commit=common_parent_commit,
        equivalent_initial_state=True,
        manual_shadow_workspace_state="no repository mutation",
        Pepper_shadow_workspace_state="no repository mutation",
        cleanup_required=False,
        cleanup_performed=False,
        destructive_cleanup_performed=False,
    )
    comparisons = build_manual_hermes_shadow_comparison_dimensions(
        manual_digest=manual_baseline.manual_path_SHA256,
        Pepper_digest=pepper_evidence.pepper_path_SHA256,
        UI_blocked=UI_blocked,
        chat_required=chat_required,
    )
    UI_readiness = _make_model(
        ShadowUIReadinessEvidence,
        "ui_SHA256",
        MANUAL_HERMES_SHADOW_UI_DIGEST_ALGORITHM,
        endpoints=build_manual_hermes_shadow_ui_endpoints(
            approval_backend_live=approval_backend_live,
            execution_backend_live=execution_backend_live,
        ),
        project_visible=True,
        ticket_visible=not UI_blocked,
        workflow_state_visible=not UI_blocked,
        next_required_human_action_visible=not UI_blocked,
        approval_list_live=approval_backend_live,
        approval_detail_live=approval_backend_live,
        approval_action_available_from_UI=approval_backend_live,
        explicit_human_APPROVE_possible_in_Pepper_UI=approval_backend_live,
        explicit_human_REJECT_possible_in_Pepper_UI=approval_backend_live,
        execution_list_live=execution_backend_live,
        execution_detail_live=execution_backend_live,
        WorkPacket_identity_visible=execution_backend_live,
        execution_state_visible=execution_backend_live,
        validation_state_visible=execution_backend_live,
        review_state_visible=execution_backend_live,
        failure_cancellation_visible=execution_backend_live,
        Git_handoff_readiness_visible=execution_backend_live,
        human_ui_smoke=ManualHermesShadowRunHumanSmokeStatus.HUMAN_UI_SMOKE_BLOCKED
        if UI_blocked
        else ManualHermesShadowRunHumanSmokeStatus.HUMAN_UI_SMOKE_PASS,
    )
    dependency_value = (
        ManualHermesShadowRunDependencyPosture.REQUIRED
        if chat_required
        else ManualHermesShadowRunDependencyPosture.NOT_REQUIRED
    )
    chat_dependency_audit = _make_model(
        ShadowDependencyAudit,
        "audit_SHA256",
        MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM,
        roadmap_state=dependency_value,
        project_context=dependency_value,
        ticket_generation=dependency_value,
        approval_decision_storage=ManualHermesShadowRunDependencyPosture.NOT_REQUIRED,
        review=dependency_value,
        recovery_decision=ManualHermesShadowRunDependencyPosture.NOT_REQUIRED,
        next_action=dependency_value,
        Git_handoff_construction=dependency_value,
        normal_workflow_requires_this_chat=chat_required,
    )
    OpenCode_dependency_audit = _make_model(
        ShadowOpenCodeDependencyAudit,
        "audit_SHA256",
        MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM,
        manual_OpenCode_ticket_paste=opencode_copy_required,
        manual_OpenCode_start=opencode_copy_required,
        manual_OpenCode_result_copy=opencode_copy_required,
        manual_OpenCode_result_interpretation=opencode_copy_required,
        manual_OpenCode_ticket_paste_count=1 if opencode_copy_required else 0,
        manual_OpenCode_start_count=1 if opencode_copy_required else 0,
        manual_OpenCode_result_copy_count=1 if opencode_copy_required else 0,
        manual_OpenCode_result_interpretation_count=1 if opencode_copy_required else 0,
    )
    context_persistence_audit = _make_model(
        ShadowContextPersistenceAudit,
        "audit_SHA256",
        MANUAL_HERMES_SHADOW_AUDIT_DIGEST_ALGORITHM,
        minimum_project_context_persisted=(
            "project identity",
            "roadmap position",
            "workflow result digests",
            "repository branch identity",
        ),
        missing_context_classes=(
            ("operator conversation as primary work-control plane",)
            if chat_required
            else ()
        ),
        GBrain_required_for_P18_8=False,
        Paperclip_required_for_P18_8=False,
        next_ticket_requires_historic_chat_memory=chat_required,
        P18_8_context_blocker=chat_required,
    )
    migration_gaps = _build_default_gaps(
        approval_backend_live=approval_backend_live,
        execution_backend_live=execution_backend_live,
        chat_required=chat_required,
        opencode_copy_required=opencode_copy_required,
    )
    operator_effort = _make_model(
        ShadowOperatorEffort,
        "effort_SHA256",
        MANUAL_HERMES_SHADOW_EFFORT_DIGEST_ALGORITHM,
        manual_path_elapsed_minutes=45,
        Pepper_path_elapsed_minutes=30 if not UI_blocked else 50,
        manual_human_interactions=10,
        Pepper_human_interactions=2 if not chat_required else 8,
        manual_copy_paste_count=5,
        Pepper_manual_copy_paste_count=0 if not opencode_copy_required else 4,
        manual_explicit_approvals=1,
        Pepper_explicit_approvals=1,
    )
    Git_handoff_comparison = _make_model(
        ShadowGitHandoffComparison,
        "handoff_SHA256",
        MANUAL_HERMES_SHADOW_GIT_DIGEST_ALGORITHM,
        candidate_paths_exact=True,
        staging_boundaries_exact=True,
        diff_check_present=True,
        staged_verification_present=True,
        commit_message_present=True,
        push_target_present=True,
        human_only_execution_preserved=True,
        automatic_git_add=False,
        automatic_git_commit=False,
        automatic_git_push=False,
        Git_handoff_eligible=True,
    )
    request = _make_model(
        ManualHermesShadowRunRequest,
        "request_SHA256",
        MANUAL_HERMES_SHADOW_REQUEST_DIGEST_ALGORITHM,
        P18_6_commit=P18_6_commit,
        P18_6_result_SHA256=P18_6_result_SHA256,
        project_id="PEPPER",
        macroproject_id="P18",
        implementation_lineage_ticket_id="P18.2",
        recovery_boundary="RECOVERY_DECISION_ONLY",
        shadow_ticket=shadow_ticket,
        manual_baseline=manual_baseline,
        manual_authority_map=build_manual_hermes_shadow_authority_map(),
        Pepper_evidence=pepper_evidence,
        workspace_isolation=workspace_isolation,
        comparisons=comparisons,
        UI_readiness=UI_readiness,
        chat_dependency_audit=chat_dependency_audit,
        OpenCode_dependency_audit=OpenCode_dependency_audit,
        context_persistence_audit=context_persistence_audit,
        migration_gaps=migration_gaps,
        operator_effort=operator_effort,
        Git_handoff_comparison=Git_handoff_comparison,
    )
    validate_manual_hermes_shadow_run_request(request)
    return request


def validate_manual_hermes_shadow_run_request(
    request: ManualHermesShadowRunRequest,
) -> None:
    try:
        ManualHermesShadowRunRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ManualHermesShadowRunValidationError("invalid P18.7 request") from exc


def _comparison_digest(
    comparisons: tuple[ShadowComparisonDimension, ...],
    dimensions: set[ManualHermesShadowRunStage] | None = None,
) -> str:
    selected = (
        tuple(item for item in comparisons if item.dimension in dimensions)
        if dimensions is not None
        else comparisons
    )
    return _digest_from_record(
        MANUAL_HERMES_SHADOW_COMPARISON_DIGEST_ALGORITHM, selected
    )


def _semantic_equivalent(comparisons: tuple[ShadowComparisonDimension, ...]) -> bool:
    semantic_dimensions = {
        ManualHermesShadowRunStage.PROJECT_CONTEXT,
        ManualHermesShadowRunStage.TICKET_SEMANTICS,
        ManualHermesShadowRunStage.EXECUTION,
        ManualHermesShadowRunStage.VALIDATION,
        ManualHermesShadowRunStage.REVIEW,
        ManualHermesShadowRunStage.RECOVERY,
        ManualHermesShadowRunStage.GIT_HANDOFF,
    }
    allowed = {
        ManualHermesShadowRunComparisonScore.MATCH,
        ManualHermesShadowRunComparisonScore.EQUIVALENT,
        ManualHermesShadowRunComparisonScore.PEPPER_BETTER,
        ManualHermesShadowRunComparisonScore.NOT_APPLICABLE,
    }
    return all(
        item.score in allowed
        for item in comparisons
        if item.dimension in semantic_dimensions
    )


def _governance_equivalent(comparisons: tuple[ShadowComparisonDimension, ...]) -> bool:
    governance_dimensions = {
        ManualHermesShadowRunStage.APPROVAL,
        ManualHermesShadowRunStage.DEPENDENCY_GATE,
        ManualHermesShadowRunStage.WORKFLOW_STATE,
        ManualHermesShadowRunStage.AUTHORITY,
        ManualHermesShadowRunStage.SECURITY,
        ManualHermesShadowRunStage.EVIDENCE_COMPLETENESS,
    }
    allowed = {
        ManualHermesShadowRunComparisonScore.MATCH,
        ManualHermesShadowRunComparisonScore.EQUIVALENT,
        ManualHermesShadowRunComparisonScore.PEPPER_BETTER,
    }
    return all(
        item.score in allowed
        for item in comparisons
        if item.dimension in governance_dimensions
    )


def _pepper_authority_stricter_or_equal(
    comparisons: tuple[ShadowComparisonDimension, ...],
) -> bool:
    authority = next(
        item
        for item in comparisons
        if item.dimension is ManualHermesShadowRunStage.AUTHORITY
    )
    return authority.score in {
        ManualHermesShadowRunComparisonScore.MATCH,
        ManualHermesShadowRunComparisonScore.EQUIVALENT,
        ManualHermesShadowRunComparisonScore.PEPPER_BETTER,
    }


def _build_summary(
    request: ManualHermesShadowRunRequest,
) -> ManualHermesShadowRunSummary:
    blocker_count = sum(1 for gap in request.migration_gaps if gap.blocks_cutover)
    warning_count = sum(
        1
        for gap in request.migration_gaps
        if gap.severity is ManualHermesShadowRunGapSeverity.WARNING
    )
    info_count = sum(
        1
        for gap in request.migration_gaps
        if gap.severity is ManualHermesShadowRunGapSeverity.INFO
    )
    ui = request.UI_readiness
    projects_operational = ui.project_visible
    tickets_operational = ui.ticket_visible and ui.workflow_state_visible
    approvals_operational = all((
        ui.approval_list_live,
        ui.approval_detail_live,
        ui.approval_action_available_from_UI,
        ui.explicit_human_APPROVE_possible_in_Pepper_UI,
        ui.explicit_human_REJECT_possible_in_Pepper_UI,
    ))
    executions_operational = all((
        ui.execution_list_live,
        ui.execution_detail_live,
        ui.WorkPacket_identity_visible,
        ui.execution_state_visible,
        ui.validation_state_visible,
    ))
    review_visibility = ui.review_state_visible and ui.Git_handoff_readiness_visible
    next_action = ui.next_required_human_action_visible
    semantic = _semantic_equivalent(request.comparisons)
    governance = _governance_equivalent(request.comparisons)
    authority = _pepper_authority_stricter_or_equal(request.comparisons)
    ready = all((
        semantic,
        governance,
        authority,
        projects_operational,
        tickets_operational,
        approvals_operational,
        executions_operational,
        review_visibility,
        next_action,
        not request.chat_dependency_audit.normal_workflow_requires_this_chat,
        not request.OpenCode_dependency_audit.manual_OpenCode_ticket_paste,
        not request.OpenCode_dependency_audit.manual_OpenCode_result_copy,
        blocker_count == 0,
    ))
    return _make_model(
        ManualHermesShadowRunSummary,
        "summary_SHA256",
        MANUAL_HERMES_SHADOW_SUMMARY_DIGEST_ALGORITHM,
        semantic_shadow_equivalence=semantic,
        governance_equivalence=governance,
        authority_equivalence=authority,
        Pepper_authority_stricter_or_equal=authority,
        UI_operational=all((
            projects_operational,
            tickets_operational,
            approvals_operational,
            executions_operational,
            review_visibility,
            next_action,
        )),
        Projects_operational=projects_operational,
        Tickets_operational=tickets_operational,
        Approvals_operational=approvals_operational,
        Executions_operational=executions_operational,
        review_visibility_operational=review_visibility,
        next_action_visible=next_action,
        normal_workflow_requires_chat=(
            request.chat_dependency_audit.normal_workflow_requires_this_chat
        ),
        manual_OpenCode_ticket_copy_required=(
            request.OpenCode_dependency_audit.manual_OpenCode_ticket_paste
        ),
        manual_OpenCode_result_copy_required=(
            request.OpenCode_dependency_audit.manual_OpenCode_result_copy
        ),
        cutover_blocking_gap_count=blocker_count,
        P18_8_ready=ManualHermesShadowRunReadinessDecision.P18_8_READY
        if ready
        else ManualHermesShadowRunReadinessDecision.P18_8_BLOCKED,
        shadow_run_valid=True,
        warning_gap_count=warning_count,
        informational_gap_count=info_count,
        comparison_dimension_count=15,
    )


def build_manual_hermes_shadow_run(
    request: ManualHermesShadowRunRequest,
) -> ManualHermesShadowRunResult:
    validate_manual_hermes_shadow_run_request(request)
    validated = ManualHermesShadowRunRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    summary = _build_summary(validated)
    semantic_dimensions = {
        ManualHermesShadowRunStage.PROJECT_CONTEXT,
        ManualHermesShadowRunStage.TICKET_SEMANTICS,
        ManualHermesShadowRunStage.EXECUTION,
        ManualHermesShadowRunStage.VALIDATION,
        ManualHermesShadowRunStage.REVIEW,
        ManualHermesShadowRunStage.RECOVERY,
        ManualHermesShadowRunStage.GIT_HANDOFF,
    }
    authority_dimensions = {
        ManualHermesShadowRunStage.AUTHORITY,
        ManualHermesShadowRunStage.SECURITY,
    }
    result_values = {
        "schema_version": MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION,
        "policy_id": MANUAL_HERMES_SHADOW_RUN_POLICY_ID,
        "decision": ManualHermesShadowRunDecision.SHADOW_VALIDATED
        if summary.P18_8_ready is ManualHermesShadowRunReadinessDecision.P18_8_READY
        else ManualHermesShadowRunDecision.SHADOW_VALIDATED_WITH_CUTOVER_BLOCKERS,
        "request": validated,
        "summary": summary,
        "shadow_ticket_id": validated.shadow_ticket.shadow_ticket_id,
        "common_parent_commit": validated.workspace_isolation.common_parent_commit,
        "manual_path_digest": validated.manual_baseline.manual_path_SHA256,
        "Pepper_path_digest": validated.Pepper_evidence.pepper_path_SHA256,
        "semantic_comparison_digest": _comparison_digest(
            validated.comparisons,
            semantic_dimensions,
        ),
        "authority_comparison_digest": _comparison_digest(
            validated.comparisons,
            authority_dimensions,
        ),
        "UI_readiness_digest": validated.UI_readiness.ui_SHA256,
        "migration_gap_digest": _digest_from_record(
            MANUAL_HERMES_SHADOW_GAP_DIGEST_ALGORITHM,
            validated.migration_gaps,
        ),
        "P18_8_ready": summary.P18_8_ready,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "subprocess_calls": 0,
        "shell_calls": 0,
        "filesystem_calls": 0,
        "Git_calls": 0,
        "network_calls": 0,
        "Docker_calls": 0,
        "Graphify_calls": 0,
        "database_calls": 0,
        "direct_Kanban_mutation_calls": 0,
        "direct_dispatcher_calls": 0,
        "direct_worker_calls": 0,
        "direct_validation_runner_calls": 0,
        "direct_review_engine_calls": 0,
        "direct_recovery_engine_calls": 0,
        "staging_calls": 0,
        "commit_calls": 0,
        "push_calls": 0,
        "automatic_git_add": False,
        "automatic_git_commit": False,
        "automatic_git_push": False,
        "duplicate_Project_Intake_created": False,
        "duplicate_Ticket_Factory_created": False,
        "duplicate_approval_engine_created": False,
        "duplicate_dependency_queue_created": False,
        "duplicate_executor_created": False,
        "duplicate_validation_runner_created": False,
        "duplicate_review_engine_created": False,
        "duplicate_recovery_engine_created": False,
        "duplicate_Git_handoff_created": False,
    }
    result = _make_model(
        ManualHermesShadowRunResult,
        "result_SHA256",
        MANUAL_HERMES_SHADOW_RESULT_DIGEST_ALGORITHM,
        **result_values,
    )
    validate_manual_hermes_shadow_run_result(result)
    return result


def validate_manual_hermes_shadow_run_result(
    result: ManualHermesShadowRunResult,
) -> None:
    try:
        validated = ManualHermesShadowRunResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ManualHermesShadowRunValidationError("invalid P18.7 result") from exc
    validate_manual_hermes_shadow_run_request(validated.request)


def summarize_manual_hermes_shadow_run(
    result: ManualHermesShadowRunResult,
) -> ManualHermesShadowRunSummary:
    validate_manual_hermes_shadow_run_result(result)
    return result.summary


__all__ = (
    "MANUAL_HERMES_SHADOW_RUN_SCHEMA_VERSION",
    "MANUAL_HERMES_SHADOW_RUN_POLICY_ID",
    "ManualHermesShadowRunDecision",
    "ManualHermesShadowRunComparisonScore",
    "ManualHermesShadowRunGapCategory",
    "ManualHermesShadowRunGapSeverity",
    "ManualHermesShadowRunDependencyPosture",
    "ManualHermesShadowRunUIClassification",
    "ManualHermesShadowRunHumanSmokeStatus",
    "ManualHermesShadowRunReadinessDecision",
    "ManualHermesShadowRunStage",
    "ShadowTicketSelection",
    "ManualWorkflowBaseline",
    "ManualWorkflowAuthorityEntry",
    "PepperWorkflowEvidence",
    "ShadowWorkspaceIsolation",
    "ShadowComparisonDimension",
    "ShadowUIEndpointEvidence",
    "ShadowUIReadinessEvidence",
    "ShadowDependencyAudit",
    "ShadowOpenCodeDependencyAudit",
    "ShadowContextPersistenceAudit",
    "ShadowMigrationGap",
    "ShadowOperatorEffort",
    "ShadowGitHandoffComparison",
    "ManualHermesShadowRunRequest",
    "ManualHermesShadowRunSummary",
    "ManualHermesShadowRunResult",
    "ManualHermesShadowRunError",
    "ManualHermesShadowRunInputError",
    "ManualHermesShadowRunIntegrityError",
    "ManualHermesShadowRunPolicyError",
    "ManualHermesShadowRunStateError",
    "ManualHermesShadowRunValidationError",
    "build_manual_hermes_shadow_authority_map",
    "build_manual_hermes_shadow_comparison_dimensions",
    "build_manual_hermes_shadow_ui_endpoints",
    "build_canonical_p18_manual_hermes_shadow_run_request",
    "validate_manual_hermes_shadow_run_request",
    "build_manual_hermes_shadow_run",
    "validate_manual_hermes_shadow_run_result",
    "summarize_manual_hermes_shadow_run",
)
