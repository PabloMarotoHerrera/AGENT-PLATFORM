"""P18.3 explicit human ticket approval workflow integration.

This module consumes the accepted P18.2 Ticket Factory runtime result, records an
explicit human approve/reject decision through the existing P16 approval and
publication contracts, and advances the P18.0 governed workflow state machine.
It is intentionally pure: no command execution, worker dispatch, workspace
allocation, dependency queue submission, provider/model call, Git mutation,
Docker, Graphify, G-Brain or Paperclip authority is present.
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

from hermes_cli.agent_platform.ticket_factory import (
    FreshDependencyPlanningEvidence,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    ParallelPlanningPolicy,
    ReviewedTicketProposal,
    TicketApprovalRecord,
    TicketApprovalRequest,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketPlanningRequest,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    TicketPublicationResult,
    TicketSynthesisRequest,
    build_ticket_approval_record,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    build_ticket_synthesis_review,
    prepare_ticket_generator_assignments,
    publish_canonical_ticket,
)
from hermes_cli.agent_platform.workflow.governed_state_machine import (
    GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
    GovernedWorkflowSnapshot,
    GovernedWorkflowState,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowRuntimeKind,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_governed_workflow_transition,
    build_hermes_workflow_projection,
    validate_governed_workflow_transition_request,
)
from hermes_cli.agent_platform.workflow.ticket_factory_runtime import (
    TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID,
    TicketFactoryRuntimeDecision,
    TicketFactoryRuntimeIntegrationResult,
    TicketFactoryRuntimeState,
    validate_ticket_factory_runtime_integration_result,
)
from hermes_cli.agent_platform.work_packet import WORK_PACKET_COMPILER_POLICY_ID


APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION = 1
APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID = "pepper-approval-workflow-integration-v1"

APPROVAL_WORKFLOW_ARTIFACT_BINDING_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-artifact-binding-sha256-v1"
)
APPROVAL_WORKFLOW_DECISION_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-human-decision-sha256-v1"
)
APPROVAL_WORKFLOW_REQUEST_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-request-sha256-v1"
)
APPROVAL_WORKFLOW_PUBLICATION_BOUNDARY_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-publication-boundary-sha256-v1"
)
APPROVAL_WORKFLOW_HANDOFF_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-p18-4-handoff-sha256-v1"
)
APPROVAL_WORKFLOW_FINDING_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-finding-sha256-v1"
)
APPROVAL_WORKFLOW_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-summary-sha256-v1"
)
APPROVAL_WORKFLOW_APPROVAL_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-approval-result-sha256-v1"
)
APPROVAL_WORKFLOW_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-approval-workflow-result-sha256-v1"
)
APPROVAL_WORKFLOW_ID_DIGEST_ALGORITHM = "agent-platform-approval-workflow-id-sha256-v1"

_CANONICAL_MACROPROJECT_ID = "P18"
_CANONICAL_PROJECT_ID = "PEPPER"
_CANONICAL_TICKET_ID = "P18.2"
_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_INTEGRATION_ID_PATTERN = r"^AWI-P18-[a-f0-9]{12}$"
_FINDING_ID_PATTERN = r"^AWIF-[0-9]{3}$"
_WORK_PACKET_ID_PATTERN = r"^WP-[A-Z0-9-]+-R[0-9]{4}-[a-f0-9]{12}$"
_PUBLICATION_ID_PATTERN = r"^PUB-P[1-9][0-9]{0,3}(?:-[A-Z0-9]+)+-[0-9]{4}$"
_REASON_CODE_PATTERN = r"^[a-z][a-z0-9_:-]{2,63}$"
_DECIDED_AT_PATTERN = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
_CONTROL_OR_ANSI_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x1b]")
_PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)")
_SHELL_COMMAND_PATTERN = re.compile(
    r"(?:\bgit\s+(?:add|commit|push|checkout|switch|merge|rebase|reset|stash|tag|worktree)\b)"
    r"|(?:\bdocker\s+(?:build|run|compose|pull|push)\b)"
    r"|(?:\bgraphify\s+(?:update|extract|export|cluster|recluster|query|path|explain)\b)"
    r"|(?:\b(?:subprocess|shell|powershell|cmd\.exe|bash)\b)"
    r"|(?:\bexecute_work_packet\b|\brun_approved_ticket\b|\bdispatch_approved_ticket\b)",
    re.IGNORECASE,
)
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
)
_RAW_CONTEXT_MARKERS = (
    "raw prompt",
    "system prompt",
    "reasoning trace",
    "provider response",
    "model output",
    "raw conversation",
    "chatgpt transcript",
    "opencode transcript",
    "stdout:",
    "stderr:",
    "diff --git",
)
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")

DigestText = Annotated[str, Field(pattern=_DIGEST_PATTERN)]
IntegrationIdentifier = Annotated[str, Field(pattern=_INTEGRATION_ID_PATTERN)]
FindingIdentifier = Annotated[str, Field(pattern=_FINDING_ID_PATTERN)]
WorkPacketIdentifier = Annotated[str, Field(pattern=_WORK_PACKET_ID_PATTERN)]
PublicationIdentifier = Annotated[str, Field(pattern=_PUBLICATION_ID_PATTERN)]
ReasonCode = Annotated[str, Field(pattern=_REASON_CODE_PATTERN)]
DecisionTimestamp = Annotated[str, Field(pattern=_DECIDED_AT_PATTERN)]
BoundedText = Annotated[str, Field(min_length=1, max_length=1024)]


class ApprovalWorkflowIntegrationError(ValueError):
    """Base error for P18.3 approval workflow integration failures."""


class ApprovalWorkflowInputError(ApprovalWorkflowIntegrationError):
    """Raised when caller-supplied approval workflow input is malformed."""


class ApprovalWorkflowIntegrityError(ApprovalWorkflowIntegrationError):
    """Raised when deterministic approval workflow evidence is invalid."""


class ApprovalWorkflowPolicyError(ApprovalWorkflowIntegrationError):
    """Raised when P18.3 approval policy is violated."""


class ApprovalWorkflowStateError(ApprovalWorkflowIntegrationError):
    """Raised when the governed workflow state cannot advance."""


class ApprovalWorkflowValidationError(ApprovalWorkflowIntegrationError):
    """Raised when a P18.3 approval workflow object fails validation."""


class ApprovalWorkflowDecisionAuthority(str, Enum):
    HUMAN = "human"
    PROVIDER = "provider"
    MODEL = "model"
    AUTONOMOUS_AGENT = "autonomous_agent"
    WORKER = "worker"
    SCHEDULER = "scheduler"
    RUNTIME = "runtime"
    GENERATED_DEFAULT = "generated_default"


class ApprovalWorkflowState(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"


class ApprovalWorkflowResultDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


class ApprovalWorkflowFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class ApprovalWorkflowFindingCode(str, Enum):
    P18_2_CONTINUATION_VALID = "p18_2_continuation_valid"
    ARTIFACT_BINDING_VALID = "artifact_binding_valid"
    HUMAN_DECISION_VALID = "human_decision_valid"
    APPROVAL_RECORD_REUSED = "approval_record_reused"
    PUBLICATION_BOUNDARY_VALID = "publication_boundary_valid"
    WORKFLOW_TRANSITION_VALID = "workflow_transition_valid"
    EXECUTION_AUTHORITY_PROHIBITED = "execution_authority_prohibited"
    P18_4_HANDOFF_READY = "p18_4_handoff_ready"
    APPROVAL_UI_BACKEND_DEFERRED = "approval_ui_backend_deferred"
    PERSISTENCE_DEFERRED = "persistence_deferred"
    DUPLICATE_MODEL_AVOIDED = "duplicate_model_avoided"
    INTEGRATION_ACCEPTED = "integration_accepted"


class _ApprovalWorkflowModel(BaseModel):
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
        raise ValueError(f"{label} contains credential-like content")
    if any(marker in lowered for marker in _RAW_CONTEXT_MARKERS):
        raise ValueError(f"{label} contains raw context")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-like content")
    if _PERSONAL_PATH_PATTERN.search(value):
        raise ValueError(f"{label} contains a personal absolute path")
    if _SHELL_COMMAND_PATTERN.search(value):
        raise ValueError(f"{label} contains execution-shaped content")
    return value


def _normalize_for_digest(value: object) -> object:
    if isinstance(value, BaseModel):
        return _normalize_for_digest(value.model_dump(mode="json", warnings=False))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_normalize_for_digest(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize_for_digest(item) for key, item in value.items()}
    return value


def _digest_from_record(algorithm: str, record: object) -> str:
    payload = {"algorithm": algorithm, "record": _normalize_for_digest(record)}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _model_digest(algorithm: str, value: BaseModel, digest_field: str) -> str:
    return _digest_from_record(
        algorithm,
        value.model_dump(mode="json", exclude={digest_field}, warnings=False),
    )


def _make_model(
    model_type: type[_ApprovalWorkflowModel],
    digest_field: str,
    algorithm: str,
    **values: object,
) -> _ApprovalWorkflowModel:
    data = dict(values)
    data[digest_field] = "0" * 64
    provisional = model_type.model_construct(**data)
    data[digest_field] = _digest_from_record(
        algorithm,
        provisional.model_dump(mode="json", exclude={digest_field}, warnings=False),
    )
    return model_type(**data)


class ApprovalWorkflowArtifactBinding(_ApprovalWorkflowModel):
    schema_version: Literal[1] = APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION
    policy_id: Literal["pepper-approval-workflow-integration-v1"] = (
        APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID
    )
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    P18_2_result_SHA256: DigestText
    TicketSpec_SHA256: DigestText
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    WorkPacket_publication_id: PublicationIdentifier
    WorkPacket_publication_revision: int = Field(ge=1, le=9999, strict=True)
    WorkPacket_publication_artifact_SHA256: DigestText
    workflow_snapshot_SHA256: DigestText
    current_workflow_state: Literal[GovernedWorkflowState.AWAITING_TICKET_APPROVAL]
    expected_current_state: Literal[GovernedWorkflowState.AWAITING_TICKET_APPROVAL]
    ticket_factory_runtime_policy_id: Literal[
        "pepper-ticket-factory-runtime-integration-v1"
    ] = TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID
    governed_workflow_policy_id: Literal[
        "pepper-governed-manual-to-runtime-workflow-state-machine-v1"
    ] = GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID
    work_packet_compiler_policy_id: Literal["pepper-work-packet-compiler-policy-v1"] = (
        WORK_PACKET_COMPILER_POLICY_ID
    )
    artifact_binding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_artifact_binding(self) -> ApprovalWorkflowArtifactBinding:
        if self.current_workflow_state is not self.expected_current_state:
            raise ValueError("current workflow state must match expected state")
        if self.artifact_binding_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_ARTIFACT_BINDING_DIGEST_ALGORITHM,
            self,
            "artifact_binding_SHA256",
        ):
            raise ValueError(
                "artifact_binding_SHA256 must match artifact binding digest"
            )
        return self


class ApprovalWorkflowDecisionInput(_ApprovalWorkflowModel):
    schema_version: Literal[1] = APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION
    authority: ApprovalWorkflowDecisionAuthority
    decision: HumanApprovalDecision
    approval_evidence: HumanApprovalEvidence
    reason_code: ReasonCode
    decided_at: DecisionTimestamp
    approval_decision_SHA256: DigestText

    @field_validator("reason_code", "decided_at")
    @classmethod
    def _validate_safe_fields(cls, value: str) -> str:
        return _validate_safe_text(value, "approval decision input")

    @model_validator(mode="after")
    def _validate_decision_digest(self) -> ApprovalWorkflowDecisionInput:
        evidence = self.approval_evidence
        _validate_safe_text(evidence.decision_reference, "approval decision reference")
        _validate_safe_text(evidence.rationale, "approval rationale")
        if evidence.policy_warning_acknowledgement is not None:
            _validate_safe_text(
                evidence.policy_warning_acknowledgement,
                "approval policy warning acknowledgement",
            )
        if evidence.planning_warning_acknowledgement is not None:
            _validate_safe_text(
                evidence.planning_warning_acknowledgement,
                "approval planning warning acknowledgement",
            )
        if self.approval_decision_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_DECISION_DIGEST_ALGORITHM,
            self,
            "approval_decision_SHA256",
        ):
            raise ValueError("approval_decision_SHA256 must match decision digest")
        return self


class ApprovalWorkflowRequest(_ApprovalWorkflowModel):
    schema_version: Literal[1] = APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION
    policy_id: Literal["pepper-approval-workflow-integration-v1"] = (
        APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID
    )
    P18_2_result: TicketFactoryRuntimeIntegrationResult
    artifact_binding: ApprovalWorkflowArtifactBinding
    decision_input: ApprovalWorkflowDecisionInput
    prior_approval_result_SHA256: DigestText | None = None
    prior_artifact_binding_SHA256: DigestText | None = None
    prior_approval_decision: HumanApprovalDecision | None = None
    approval_request_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_request_digest(self) -> ApprovalWorkflowRequest:
        if self.approval_request_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_REQUEST_DIGEST_ALGORITHM,
            self,
            "approval_request_SHA256",
        ):
            raise ValueError(
                "approval_request_SHA256 must match approval request digest"
            )
        return self


class ApprovalWorkflowFinding(_ApprovalWorkflowModel):
    finding_id: FindingIdentifier
    severity: ApprovalWorkflowFindingSeverity
    code: ApprovalWorkflowFindingCode
    subject_id: BoundedText
    summary: BoundedText
    failed_invariant: BoundedText | None = None
    finding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_finding(self) -> ApprovalWorkflowFinding:
        if self.finding_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_FINDING_DIGEST_ALGORITHM,
            self,
            "finding_SHA256",
        ):
            raise ValueError(
                "finding_SHA256 must match approval workflow finding digest"
            )
        if self.severity is ApprovalWorkflowFindingSeverity.BLOCKING:
            if self.failed_invariant is None:
                raise ValueError("blocking findings require failed_invariant")
        elif self.failed_invariant is not None:
            raise ValueError("non-blocking findings must not include failed_invariant")
        return self


class ApprovalWorkflowPublicationBoundary(_ApprovalWorkflowModel):
    publication_required_for_approve: StrictBool
    publication_applied: StrictBool
    human_approved_publication_id: PublicationIdentifier | None = None
    human_approved_publication_revision: int | None = Field(default=None, ge=1)
    human_approved_publication_result_SHA256: DigestText | None = None
    human_approved_publication_artifact_SHA256: DigestText | None = None
    compile_only_publication_id: PublicationIdentifier
    compile_only_publication_revision: int = Field(ge=1, le=9999, strict=True)
    compile_only_publication_artifact_SHA256: DigestText
    approved_ticket_matches_work_packet_source: StrictBool
    published_ticket_matches_approved_ticket: StrictBool
    WorkPacket_recompile_required_before_execution: StrictBool
    publication_boundary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_publication_boundary(self) -> ApprovalWorkflowPublicationBoundary:
        published_fields = (
            self.human_approved_publication_id,
            self.human_approved_publication_revision,
            self.human_approved_publication_result_SHA256,
            self.human_approved_publication_artifact_SHA256,
        )
        if self.publication_applied:
            if any(value is None for value in published_fields):
                raise ValueError("applied publication requires all publication fields")
        elif any(value is not None for value in published_fields):
            raise ValueError(
                "non-applied publication must not include publication fields"
            )
        if self.publication_boundary_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_PUBLICATION_BOUNDARY_DIGEST_ALGORITHM,
            self,
            "publication_boundary_SHA256",
        ):
            raise ValueError("publication_boundary_SHA256 must match boundary digest")
        return self


class ApprovalWorkflowP18_4Handoff(_ApprovalWorkflowModel):
    project_id: Literal["PEPPER"]
    macroproject_id: Literal["P18"]
    ticket_id: Literal["P18.2"]
    TicketSpec_SHA256: DigestText
    WorkPacket_ID: WorkPacketIdentifier
    WorkPacket_SHA256: DigestText
    approval_decision: HumanApprovalDecision
    approval_granted: StrictBool
    approval_decision_SHA256: DigestText
    approval_result_SHA256: DigestText
    workflow_state: GovernedWorkflowState
    approval_policy_id: Literal["pepper-approval-workflow-integration-v1"]
    approval_schema_version: Literal[1]
    execution_started: Literal[False]
    approved_handoff_P18_4_ready: StrictBool
    rejected_handoff_P18_4_ready: Literal[False]
    P18_4_ready: StrictBool
    handoff_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_handoff(self) -> ApprovalWorkflowP18_4Handoff:
        if self.approval_granted != (
            self.approval_decision is HumanApprovalDecision.APPROVE
        ):
            raise ValueError("handoff approval grant must match decision")
        if self.approved_handoff_P18_4_ready != self.approval_granted:
            raise ValueError("approved handoff readiness must match approval grant")
        if self.P18_4_ready != self.approval_granted:
            raise ValueError("P18_4_ready must match approval grant")
        if self.rejected_handoff_P18_4_ready is not False:
            raise ValueError("rejected handoff must never be P18.4-ready")
        if self.handoff_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_HANDOFF_DIGEST_ALGORITHM,
            self,
            "handoff_SHA256",
        ):
            raise ValueError("handoff_SHA256 must match P18.4 handoff digest")
        return self


class ApprovalWorkflowSummary(_ApprovalWorkflowModel):
    P18_2_continuation_valid: StrictBool
    approval_request_valid: StrictBool
    approval_decision_valid: StrictBool
    human_authority_valid: StrictBool
    artifact_binding_valid: StrictBool
    TicketSpec_binding_valid: StrictBool
    WorkPacket_binding_valid: StrictBool
    publication_boundary_valid: StrictBool
    approval_transition_valid: StrictBool
    rejection_transition_valid: StrictBool
    replay_policy_valid: StrictBool
    execution_prohibition_valid: StrictBool
    P18_4_handoff_valid: StrictBool
    information_finding_count: int = Field(ge=0, le=128, strict=True)
    warning_finding_count: int = Field(ge=0, le=128, strict=True)
    blocking_finding_count: int = Field(ge=0, le=128, strict=True)
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> ApprovalWorkflowSummary:
        if self.summary_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_SUMMARY_DIGEST_ALGORITHM,
            self,
            "summary_SHA256",
        ):
            raise ValueError(
                "summary_SHA256 must match approval workflow summary digest"
            )
        return self


class ApprovalWorkflowIntegrationResult(_ApprovalWorkflowModel):
    schema_version: Literal[1] = APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION
    policy_id: Literal["pepper-approval-workflow-integration-v1"] = (
        APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID
    )
    integration_id: IntegrationIdentifier
    state: ApprovalWorkflowState
    decision: ApprovalWorkflowResultDecision
    request: ApprovalWorkflowRequest
    artifact_binding: ApprovalWorkflowArtifactBinding
    decision_input: ApprovalWorkflowDecisionInput
    ticket_approval_record: TicketApprovalRecord
    ticket_publication_result: TicketPublicationResult | None
    publication_boundary: ApprovalWorkflowPublicationBoundary
    workflow_transition_result: GovernedWorkflowTransitionResult
    resulting_workflow_snapshot: GovernedWorkflowSnapshot
    findings: tuple[ApprovalWorkflowFinding, ...]
    summary: ApprovalWorkflowSummary
    handoff: ApprovalWorkflowP18_4Handoff
    approval_result_SHA256: DigestText
    approval_valid: StrictBool
    authority: Literal[ApprovalWorkflowDecisionAuthority.HUMAN]
    approval_granted: StrictBool
    resulting_workflow_state: GovernedWorkflowState
    human_ticket_approval_required: Literal[True]
    human_ticket_approval_present: Literal[True]
    ticket_execution_authorized: Literal[False]
    WorkPacket_execution_authorized: Literal[False]
    ticket_execution_started: Literal[False]
    WorkPacket_execution_started: Literal[False]
    worker_dispatch_count: Literal[0]
    command_execution_count: Literal[0]
    provider_dispatch_count: Literal[0]
    model_inference_count: Literal[0]
    Git_commands_executed: Literal[0]
    Docker_commands_executed: Literal[0]
    Graphify_commands_executed: Literal[0]
    GBrain_calls: Literal[0]
    Paperclip_calls: Literal[0]
    P18_4_ready: StrictBool
    production_readiness_claimed: Literal[False]
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> ApprovalWorkflowIntegrationResult:
        if self.approval_result_SHA256 != _approval_result_core_digest_from_result(
            self
        ):
            raise ValueError("approval_result_SHA256 must match approval result digest")
        if self.result_SHA256 != _model_digest(
            APPROVAL_WORKFLOW_RESULT_DIGEST_ALGORITHM,
            self,
            "result_SHA256",
        ):
            raise ValueError("result_SHA256 must match approval workflow result digest")
        if self.handoff.approval_result_SHA256 != self.approval_result_SHA256:
            raise ValueError("handoff must bind approval result digest")
        if self.P18_4_ready != self.handoff.P18_4_ready:
            raise ValueError("P18_4_ready must match handoff")
        if (
            self.resulting_workflow_state
            is not self.resulting_workflow_snapshot.current_state
        ):
            raise ValueError("resulting_workflow_state must match snapshot")
        return self


def build_approval_workflow_decision_input(
    *,
    decision: HumanApprovalDecision,
    reviewer_id: str,
    decision_reference: str,
    rationale: str,
    reason_code: str,
    decided_at: str,
) -> ApprovalWorkflowDecisionInput:
    """Build a deterministic decision input from an explicit supplied decision."""

    return _make_model(
        ApprovalWorkflowDecisionInput,
        "approval_decision_SHA256",
        APPROVAL_WORKFLOW_DECISION_DIGEST_ALGORITHM,
        authority=ApprovalWorkflowDecisionAuthority.HUMAN,
        decision=decision,
        approval_evidence=HumanApprovalEvidence(
            reviewer_id=reviewer_id,
            decision_reference=decision_reference,
            rationale=rationale,
        ),
        reason_code=reason_code,
        decided_at=decided_at,
    )


def build_canonical_p18_approval_workflow_request(
    *,
    ticket_factory_runtime_result: TicketFactoryRuntimeIntegrationResult,
    decision_input: ApprovalWorkflowDecisionInput,
) -> ApprovalWorkflowRequest:
    binding = _build_artifact_binding(ticket_factory_runtime_result)
    request = _make_model(
        ApprovalWorkflowRequest,
        "approval_request_SHA256",
        APPROVAL_WORKFLOW_REQUEST_DIGEST_ALGORITHM,
        P18_2_result=ticket_factory_runtime_result,
        artifact_binding=binding,
        decision_input=decision_input,
        prior_approval_result_SHA256=None,
        prior_artifact_binding_SHA256=None,
        prior_approval_decision=None,
    )
    validate_approval_workflow_request(request)
    return request


def validate_approval_workflow_request(request: ApprovalWorkflowRequest) -> None:
    try:
        validated = ApprovalWorkflowRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ApprovalWorkflowValidationError(
            "invalid approval workflow request"
        ) from exc
    _validate_p18_2_continuation(validated.P18_2_result)
    _validate_artifact_binding_matches_result(
        validated.artifact_binding, validated.P18_2_result
    )
    _validate_decision_input(validated.decision_input)
    _validate_replay_policy(validated)


def build_approval_workflow_integration(
    request: ApprovalWorkflowRequest,
) -> ApprovalWorkflowIntegrationResult:
    validate_approval_workflow_request(request)
    validated = ApprovalWorkflowRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    p18_2_result = validated.P18_2_result
    decision_input = validated.decision_input
    approval_record = _build_ticket_approval_record(validated)
    publication_result = _publish_if_approved(approval_record, decision_input)
    approval_granted = decision_input.decision is HumanApprovalDecision.APPROVE
    transition_result = _build_transition_result(p18_2_result, approval_granted)
    if not transition_result.accepted:
        raise ApprovalWorkflowStateError("P18.0 approval workflow transition rejected")
    publication_boundary = _build_publication_boundary(
        artifact_binding=validated.artifact_binding,
        approval_record=approval_record,
        publication_result=publication_result,
        p18_2_result=p18_2_result,
    )
    approval_result_SHA256 = _approval_result_core_digest(
        artifact_binding=validated.artifact_binding,
        decision_input=decision_input,
        ticket_approval_record=approval_record,
        ticket_publication_result=publication_result,
        publication_boundary=publication_boundary,
        workflow_transition_result=transition_result,
        approval_granted=approval_granted,
    )
    handoff = _build_handoff(
        artifact_binding=validated.artifact_binding,
        decision_input=decision_input,
        approval_granted=approval_granted,
        workflow_state=transition_result.resulting_snapshot.current_state,
        approval_result_SHA256=approval_result_SHA256,
    )
    findings = _derive_findings(
        approval_granted=approval_granted,
        artifact_binding=validated.artifact_binding,
        decision_input=decision_input,
        transition_result=transition_result,
    )
    summary = _derive_summary(
        findings=findings,
        request=validated,
        publication_boundary=publication_boundary,
        transition_result=transition_result,
        handoff=handoff,
        approval_granted=approval_granted,
    )
    state = (
        ApprovalWorkflowState.COMPLETED
        if summary.blocking_finding_count == 0
        else ApprovalWorkflowState.BLOCKED
    )
    result_decision = (
        ApprovalWorkflowResultDecision.APPROVED
        if approval_granted
        else ApprovalWorkflowResultDecision.REJECTED
    )
    result_values = {
        "schema_version": APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION,
        "policy_id": APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID,
        "state": state,
        "decision": result_decision,
        "request": validated,
        "artifact_binding": validated.artifact_binding,
        "decision_input": decision_input,
        "ticket_approval_record": approval_record,
        "ticket_publication_result": publication_result,
        "publication_boundary": publication_boundary,
        "workflow_transition_result": transition_result,
        "resulting_workflow_snapshot": transition_result.resulting_snapshot,
        "findings": findings,
        "summary": summary,
        "handoff": handoff,
        "approval_result_SHA256": approval_result_SHA256,
        "approval_valid": True,
        "authority": ApprovalWorkflowDecisionAuthority.HUMAN,
        "approval_granted": approval_granted,
        "resulting_workflow_state": transition_result.resulting_snapshot.current_state,
        "human_ticket_approval_required": True,
        "human_ticket_approval_present": True,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "ticket_execution_started": False,
        "WorkPacket_execution_started": False,
        "worker_dispatch_count": 0,
        "command_execution_count": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "GBrain_calls": 0,
        "Paperclip_calls": 0,
        "P18_4_ready": handoff.P18_4_ready,
        "production_readiness_claimed": False,
    }
    result = _make_model(
        ApprovalWorkflowIntegrationResult,
        "result_SHA256",
        APPROVAL_WORKFLOW_RESULT_DIGEST_ALGORITHM,
        integration_id=_integration_id_from_record(result_values),
        **result_values,
    )
    validate_approval_workflow_integration_result(result)
    return result


def validate_approval_workflow_integration_result(
    result: ApprovalWorkflowIntegrationResult,
) -> None:
    try:
        validated = ApprovalWorkflowIntegrationResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise ApprovalWorkflowValidationError(
            "invalid approval workflow integration result"
        ) from exc
    validate_approval_workflow_request(validated.request)
    _validate_findings(validated.findings)
    if validated.summary != _derive_summary(
        findings=validated.findings,
        request=validated.request,
        publication_boundary=validated.publication_boundary,
        transition_result=validated.workflow_transition_result,
        handoff=validated.handoff,
        approval_granted=validated.approval_granted,
    ):
        raise ApprovalWorkflowIntegrityError("approval workflow summary mismatch")
    _validate_result_bindings(validated)


def summarize_approval_workflow_integration(
    result: ApprovalWorkflowIntegrationResult,
) -> ApprovalWorkflowSummary:
    validate_approval_workflow_integration_result(result)
    return result.summary


def _build_artifact_binding(
    result: TicketFactoryRuntimeIntegrationResult,
) -> ApprovalWorkflowArtifactBinding:
    _validate_p18_2_continuation(result)
    packet = result.work_packet_compilation_result.work_packet
    return _make_model(
        ApprovalWorkflowArtifactBinding,
        "artifact_binding_SHA256",
        APPROVAL_WORKFLOW_ARTIFACT_BINDING_DIGEST_ALGORITHM,
        project_id=_CANONICAL_PROJECT_ID,
        macroproject_id=_CANONICAL_MACROPROJECT_ID,
        ticket_id=_CANONICAL_TICKET_ID,
        P18_2_result_SHA256=result.result_SHA256,
        TicketSpec_SHA256=packet.source_ticket_SHA256,
        WorkPacket_ID=packet.work_packet_id,
        WorkPacket_SHA256=packet.work_packet_SHA256,
        WorkPacket_publication_id=packet.publication_id,
        WorkPacket_publication_revision=packet.publication_revision,
        WorkPacket_publication_artifact_SHA256=packet.publication_artifact_SHA256,
        workflow_snapshot_SHA256=result.resulting_workflow_snapshot.workflow_SHA256,
        current_workflow_state=result.resulting_workflow_snapshot.current_state,
        expected_current_state=GovernedWorkflowState.AWAITING_TICKET_APPROVAL,
        ticket_factory_runtime_policy_id=result.policy_id,
        governed_workflow_policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        work_packet_compiler_policy_id=packet.compiler_policy_id,
    )


def _validate_p18_2_continuation(
    result: TicketFactoryRuntimeIntegrationResult,
) -> None:
    try:
        validate_ticket_factory_runtime_integration_result(result)
    except ValueError as exc:
        raise ApprovalWorkflowValidationError("invalid P18.2 continuation") from exc
    packet = result.work_packet_compilation_result.work_packet
    if result.state is not TicketFactoryRuntimeState.COMPLETED:
        raise ApprovalWorkflowStateError("P18.2 continuation must be completed")
    if result.decision is not TicketFactoryRuntimeDecision.ACCEPTED:
        raise ApprovalWorkflowStateError("P18.2 continuation must be accepted")
    if (
        result.resulting_workflow_snapshot.current_state
        is not GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    ):
        raise ApprovalWorkflowStateError(
            "P18.2 continuation must await ticket approval"
        )
    if result.P18_3_ready is not True:
        raise ApprovalWorkflowPolicyError("P18.2 continuation must be P18.3-ready")
    if result.WorkPacket_compilation_count != 1:
        raise ApprovalWorkflowPolicyError(
            "P18.2 must include one WorkPacket compilation"
        )
    if result.human_ticket_approval_present:
        raise ApprovalWorkflowPolicyError(
            "P18.2 continuation must not already include approval"
        )
    if result.ticket_execution_authorized or result.WorkPacket_execution_authorized:
        raise ApprovalWorkflowPolicyError(
            "P18.2 continuation must not authorize execution"
        )
    if not packet.work_packet_id or not packet.work_packet_SHA256:
        raise ApprovalWorkflowIntegrityError("P18.2 WorkPacket identity is missing")
    if packet.source_ticket != result.ticket_spec:
        raise ApprovalWorkflowIntegrityError("P18.2 WorkPacket source ticket mismatch")
    if packet.work_packet_id in {
        "not_executed_pending_human_ticket_approval",
        "not_compiled_pending_human_ticket_approval",
        "not_allocated_pending_human_ticket_approval",
    }:
        raise ApprovalWorkflowIntegrityError("P18.2 WorkPacket uses sentinel identity")


def _validate_artifact_binding_matches_result(
    binding: ApprovalWorkflowArtifactBinding,
    result: TicketFactoryRuntimeIntegrationResult,
) -> None:
    packet = result.work_packet_compilation_result.work_packet
    expected = _build_artifact_binding(result)
    if binding != expected:
        raise ApprovalWorkflowIntegrityError("approval artifact binding mismatch")
    if binding.project_id != result.project_spec.project_id:
        raise ApprovalWorkflowIntegrityError("artifact binding project mismatch")
    if binding.ticket_id != result.ticket_spec.ticket_id:
        raise ApprovalWorkflowIntegrityError("artifact binding ticket mismatch")
    if binding.TicketSpec_SHA256 != packet.source_ticket_SHA256:
        raise ApprovalWorkflowIntegrityError(
            "artifact binding TicketSpec digest mismatch"
        )
    if binding.WorkPacket_ID != packet.work_packet_id:
        raise ApprovalWorkflowIntegrityError("artifact binding WorkPacket ID mismatch")
    if binding.WorkPacket_SHA256 != packet.work_packet_SHA256:
        raise ApprovalWorkflowIntegrityError(
            "artifact binding WorkPacket digest mismatch"
        )


def _validate_decision_input(decision_input: ApprovalWorkflowDecisionInput) -> None:
    if decision_input.authority is not ApprovalWorkflowDecisionAuthority.HUMAN:
        raise ApprovalWorkflowPolicyError("approval decision authority must be human")
    if decision_input.decision not in {
        HumanApprovalDecision.APPROVE,
        HumanApprovalDecision.REJECT,
    }:
        raise ApprovalWorkflowPolicyError("P18.3 supports approve or reject only")
    evidence = decision_input.approval_evidence
    _validate_safe_text(evidence.decision_reference, "approval decision reference")
    _validate_safe_text(evidence.rationale, "approval rationale")
    if evidence.policy_warning_acknowledgement is not None:
        _validate_safe_text(
            evidence.policy_warning_acknowledgement,
            "approval policy warning acknowledgement",
        )
    if evidence.planning_warning_acknowledgement is not None:
        _validate_safe_text(
            evidence.planning_warning_acknowledgement,
            "approval planning warning acknowledgement",
        )


def _validate_replay_policy(request: ApprovalWorkflowRequest) -> None:
    prior_values = (
        request.prior_approval_result_SHA256,
        request.prior_artifact_binding_SHA256,
        request.prior_approval_decision,
    )
    if all(value is None for value in prior_values):
        return
    if any(value is None for value in prior_values):
        raise ApprovalWorkflowPolicyError(
            "prior approval replay evidence is incomplete"
        )
    raise ApprovalWorkflowPolicyError(
        "approval replay is forbidden after first decision"
    )


def _rebuild_synthesis_review(result: TicketFactoryRuntimeIntegrationResult):
    generation_request = TicketGenerationRequest(
        project_spec=result.project_spec,
        ticket_spec=result.ticket_spec,
        context_pack=result.context_pack,
        roles=(TicketGeneratorRole.INTEGRATION, TicketGeneratorRole.IMPLEMENTATION),
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    proposals = tuple(
        build_ticket_proposal(
            assignment=assignment,
            proposed_ticket=result.ticket_spec,
            rationale=(
                "P18.2 TicketSpec is generated from accepted P18.1 intake and "
                "bounded Ticket Factory runtime integration evidence."
            ),
            evidence_source_ids=tuple(
                item.source_id for item in result.context_pack.items
            ),
            assumptions=(),
            risks=(
                "Execution remains unauthorized until later governed workflow stages.",
            ),
            unresolved_questions=(),
        )
        for assignment in assignments
    )
    reviewed = tuple(
        ReviewedTicketProposal(proposal=proposal, lint_report=result.lint_report)
        for proposal in proposals
    )
    return build_ticket_synthesis_review(
        TicketSynthesisRequest(
            generation_request=generation_request,
            assignments=assignments,
            reviewed_proposals=reviewed,
            dependency_plan=result.dependency_plan,
        )
    )


def _fresh_planning_evidence(
    result: TicketFactoryRuntimeIntegrationResult,
) -> FreshDependencyPlanningEvidence:
    planning_request = TicketPlanningRequest(
        project_spec=result.project_spec,
        tickets=(result.ticket_spec,),
        external_dependency_resolutions=(),
        policy=ParallelPlanningPolicy(),
    )
    dependency_plan = build_ticket_dependency_plan(planning_request)
    if dependency_plan != result.dependency_plan:
        raise ApprovalWorkflowIntegrityError(
            "P18.2 dependency plan cannot be recomputed"
        )
    return FreshDependencyPlanningEvidence(
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        evidence_reference="P18.3 validates P18.2 dependency evidence before approval.",
        rationale="Human ticket approval preserves the dependency plan already bound by P18.2.",
    )


def _build_ticket_approval_record(
    request: ApprovalWorkflowRequest,
) -> TicketApprovalRecord:
    result = request.P18_2_result
    review = _rebuild_synthesis_review(result)
    planning_evidence = (
        _fresh_planning_evidence(result)
        if request.decision_input.decision is HumanApprovalDecision.APPROVE
        else None
    )
    return build_ticket_approval_record(
        TicketApprovalRequest(
            project_spec=result.project_spec,
            seed_ticket=result.ticket_spec,
            synthesis_review=review,
            decision=request.decision_input.decision,
            conflict_resolutions=(),
            approval_evidence=request.decision_input.approval_evidence,
            manual_replacement=None,
            fresh_planning_evidence=planning_evidence,
        )
    )


def _publish_if_approved(
    approval_record: TicketApprovalRecord,
    decision_input: ApprovalWorkflowDecisionInput,
) -> TicketPublicationResult | None:
    if decision_input.decision is not HumanApprovalDecision.APPROVE:
        return None
    return publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approval_record,
            publication_evidence=TicketPublicationEvidence(
                publisher_id=decision_input.approval_evidence.reviewer_id,
                publication_reference="P18.3 human-approved canonical TicketSpec publication.",
                rationale=(
                    "Logical in-memory publication records the human-approved "
                    "TicketSpec revision without granting execution authority."
                ),
            ),
            prior_publication=None,
            supersession_rationale=None,
        )
    )


def _build_transition_result(
    result: TicketFactoryRuntimeIntegrationResult,
    approval_granted: bool,
) -> GovernedWorkflowTransitionResult:
    trigger = (
        WorkflowTransitionTrigger.TICKET_APPROVED
        if approval_granted
        else WorkflowTransitionTrigger.HUMAN_REJECTED
    )
    evidence_refs = (
        ("human_ticket_approval",) if approval_granted else ("human_ticket_rejection",)
    )
    runtime_state = (
        "ticket_factory:approved_ticket"
        if approval_granted
        else "pepper:awaiting_correction"
    )
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=result.resulting_workflow_snapshot,
        trigger=trigger,
        authority=WorkflowTransitionAuthority.HUMAN,
        evidence_refs=evidence_refs,
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
            runtime_state=runtime_state,
            task_id=None,
            board_or_queue_id=None,
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        ),
    )
    validate_governed_workflow_transition_request(transition_request)
    return build_governed_workflow_transition(transition_request)


def _build_publication_boundary(
    *,
    artifact_binding: ApprovalWorkflowArtifactBinding,
    approval_record: TicketApprovalRecord,
    publication_result: TicketPublicationResult | None,
    p18_2_result: TicketFactoryRuntimeIntegrationResult,
) -> ApprovalWorkflowPublicationBoundary:
    approval_granted = approval_record.decision is HumanApprovalDecision.APPROVE
    if approval_granted:
        if publication_result is None or approval_record.approved_ticket is None:
            raise ApprovalWorkflowIntegrityError(
                "approved decision requires publication"
            )
        approved_ticket_matches = (
            approval_record.approved_ticket
            == p18_2_result.work_packet_compilation_result.work_packet.source_ticket
        )
        published_ticket_matches = (
            publication_result.publication.canonical_ticket
            == approval_record.approved_ticket
        )
        return _make_model(
            ApprovalWorkflowPublicationBoundary,
            "publication_boundary_SHA256",
            APPROVAL_WORKFLOW_PUBLICATION_BOUNDARY_DIGEST_ALGORITHM,
            publication_required_for_approve=True,
            publication_applied=True,
            human_approved_publication_id=publication_result.publication.publication_id,
            human_approved_publication_revision=publication_result.publication.revision,
            human_approved_publication_result_SHA256=publication_result.result_SHA256,
            human_approved_publication_artifact_SHA256=publication_result.publication.artifact_SHA256,
            compile_only_publication_id=artifact_binding.WorkPacket_publication_id,
            compile_only_publication_revision=artifact_binding.WorkPacket_publication_revision,
            compile_only_publication_artifact_SHA256=artifact_binding.WorkPacket_publication_artifact_SHA256,
            approved_ticket_matches_work_packet_source=approved_ticket_matches,
            published_ticket_matches_approved_ticket=published_ticket_matches,
            WorkPacket_recompile_required_before_execution=False,
        )
    return _make_model(
        ApprovalWorkflowPublicationBoundary,
        "publication_boundary_SHA256",
        APPROVAL_WORKFLOW_PUBLICATION_BOUNDARY_DIGEST_ALGORITHM,
        publication_required_for_approve=True,
        publication_applied=False,
        human_approved_publication_id=None,
        human_approved_publication_revision=None,
        human_approved_publication_result_SHA256=None,
        human_approved_publication_artifact_SHA256=None,
        compile_only_publication_id=artifact_binding.WorkPacket_publication_id,
        compile_only_publication_revision=artifact_binding.WorkPacket_publication_revision,
        compile_only_publication_artifact_SHA256=artifact_binding.WorkPacket_publication_artifact_SHA256,
        approved_ticket_matches_work_packet_source=False,
        published_ticket_matches_approved_ticket=False,
        WorkPacket_recompile_required_before_execution=False,
    )


def _approval_result_core_digest(
    *,
    artifact_binding: ApprovalWorkflowArtifactBinding,
    decision_input: ApprovalWorkflowDecisionInput,
    ticket_approval_record: TicketApprovalRecord,
    ticket_publication_result: TicketPublicationResult | None,
    publication_boundary: ApprovalWorkflowPublicationBoundary,
    workflow_transition_result: GovernedWorkflowTransitionResult,
    approval_granted: bool,
) -> str:
    return _digest_from_record(
        APPROVAL_WORKFLOW_APPROVAL_RESULT_DIGEST_ALGORITHM,
        {
            "artifact_binding": artifact_binding,
            "decision_input": decision_input,
            "ticket_approval_record": ticket_approval_record,
            "ticket_publication_result": ticket_publication_result,
            "publication_boundary": publication_boundary,
            "workflow_transition_result": workflow_transition_result,
            "approval_granted": approval_granted,
        },
    )


def _approval_result_core_digest_from_result(
    result: ApprovalWorkflowIntegrationResult,
) -> str:
    return _approval_result_core_digest(
        artifact_binding=result.artifact_binding,
        decision_input=result.decision_input,
        ticket_approval_record=result.ticket_approval_record,
        ticket_publication_result=result.ticket_publication_result,
        publication_boundary=result.publication_boundary,
        workflow_transition_result=result.workflow_transition_result,
        approval_granted=result.approval_granted,
    )


def _build_handoff(
    *,
    artifact_binding: ApprovalWorkflowArtifactBinding,
    decision_input: ApprovalWorkflowDecisionInput,
    approval_granted: bool,
    workflow_state: GovernedWorkflowState,
    approval_result_SHA256: str,
) -> ApprovalWorkflowP18_4Handoff:
    return _make_model(
        ApprovalWorkflowP18_4Handoff,
        "handoff_SHA256",
        APPROVAL_WORKFLOW_HANDOFF_DIGEST_ALGORITHM,
        project_id=artifact_binding.project_id,
        macroproject_id=artifact_binding.macroproject_id,
        ticket_id=artifact_binding.ticket_id,
        TicketSpec_SHA256=artifact_binding.TicketSpec_SHA256,
        WorkPacket_ID=artifact_binding.WorkPacket_ID,
        WorkPacket_SHA256=artifact_binding.WorkPacket_SHA256,
        approval_decision=decision_input.decision,
        approval_granted=approval_granted,
        approval_decision_SHA256=decision_input.approval_decision_SHA256,
        approval_result_SHA256=approval_result_SHA256,
        workflow_state=workflow_state,
        approval_policy_id=APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID,
        approval_schema_version=APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION,
        execution_started=False,
        approved_handoff_P18_4_ready=approval_granted,
        rejected_handoff_P18_4_ready=False,
        P18_4_ready=approval_granted,
    )


def _build_finding(
    finding_id: str,
    severity: ApprovalWorkflowFindingSeverity,
    code: ApprovalWorkflowFindingCode,
    subject_id: str,
    summary: str,
    failed_invariant: str | None = None,
) -> ApprovalWorkflowFinding:
    return _make_model(
        ApprovalWorkflowFinding,
        "finding_SHA256",
        APPROVAL_WORKFLOW_FINDING_DIGEST_ALGORITHM,
        finding_id=finding_id,
        severity=severity,
        code=code,
        subject_id=subject_id,
        summary=summary,
        failed_invariant=failed_invariant,
    )


def _derive_findings(
    *,
    approval_granted: bool,
    artifact_binding: ApprovalWorkflowArtifactBinding,
    decision_input: ApprovalWorkflowDecisionInput,
    transition_result: GovernedWorkflowTransitionResult,
) -> tuple[ApprovalWorkflowFinding, ...]:
    handoff_summary = (
        "Approved ticket handoff is ready for P18.4 queue eligibility."
        if approval_granted
        else "Rejected ticket is not eligible for P18.4 queue handoff."
    )
    rows = (
        (
            ApprovalWorkflowFindingCode.P18_2_CONTINUATION_VALID,
            artifact_binding.P18_2_result_SHA256,
            "Accepted P18.2 continuation is bound and awaits human ticket approval.",
        ),
        (
            ApprovalWorkflowFindingCode.ARTIFACT_BINDING_VALID,
            artifact_binding.artifact_binding_SHA256,
            "TicketSpec, WorkPacket and workflow snapshot digests are non-transferable.",
        ),
        (
            ApprovalWorkflowFindingCode.HUMAN_DECISION_VALID,
            decision_input.approval_decision_SHA256,
            "Decision authority is explicit human input and not provider/model/runtime generated.",
        ),
        (
            ApprovalWorkflowFindingCode.APPROVAL_RECORD_REUSED,
            decision_input.decision.value,
            "Existing Ticket Factory approval record contract records the human decision.",
        ),
        (
            ApprovalWorkflowFindingCode.PUBLICATION_BOUNDARY_VALID,
            artifact_binding.WorkPacket_publication_id,
            "Existing logical publication contract is applied only for approved tickets.",
        ),
        (
            ApprovalWorkflowFindingCode.WORKFLOW_TRANSITION_VALID,
            transition_result.transition.transition_id,
            "P18.0 governed workflow state machine owns the approval/rejection transition.",
        ),
        (
            ApprovalWorkflowFindingCode.EXECUTION_AUTHORITY_PROHIBITED,
            artifact_binding.WorkPacket_ID,
            "Approval workflow starts no execution, worker, workspace or command authority.",
        ),
        (
            ApprovalWorkflowFindingCode.P18_4_HANDOFF_READY,
            artifact_binding.ticket_id,
            handoff_summary,
        ),
        (
            ApprovalWorkflowFindingCode.APPROVAL_UI_BACKEND_DEFERRED,
            "agent-platform-approvals-ui",
            "Existing approval UI remains read-only/provisional with no new backend action route.",
        ),
        (
            ApprovalWorkflowFindingCode.PERSISTENCE_DEFERRED,
            "approval-workflow-result-envelope",
            "Approval evidence remains deterministic in-memory result evidence for P18.3.",
        ),
        (
            ApprovalWorkflowFindingCode.DUPLICATE_MODEL_AVOIDED,
            "ticket-factory-approval-contracts",
            "No duplicate approval engine, TicketSpec model or WorkPacket model is created.",
        ),
        (
            ApprovalWorkflowFindingCode.INTEGRATION_ACCEPTED,
            artifact_binding.ticket_id,
            "P18.3 approval workflow integration is accepted with zero execution authority.",
        ),
    )
    return tuple(
        _build_finding(
            f"AWIF-{index:03d}",
            ApprovalWorkflowFindingSeverity.INFO,
            code,
            subject_id,
            summary,
        )
        for index, (code, subject_id, summary) in enumerate(rows, start=1)
    )


def _validate_findings(findings: tuple[ApprovalWorkflowFinding, ...]) -> None:
    if not findings:
        raise ApprovalWorkflowValidationError("findings must be non-empty")
    expected = tuple(f"AWIF-{index:03d}" for index in range(1, len(findings) + 1))
    if tuple(item.finding_id for item in findings) != expected:
        raise ApprovalWorkflowValidationError("finding IDs must be contiguous")
    if len({item.finding_SHA256 for item in findings}) != len(findings):
        raise ApprovalWorkflowValidationError("finding digests must be unique")
    for item in findings:
        ApprovalWorkflowFinding.model_validate(item.model_dump(mode="python"))


def _derive_summary(
    *,
    findings: tuple[ApprovalWorkflowFinding, ...],
    request: ApprovalWorkflowRequest,
    publication_boundary: ApprovalWorkflowPublicationBoundary,
    transition_result: GovernedWorkflowTransitionResult,
    handoff: ApprovalWorkflowP18_4Handoff,
    approval_granted: bool,
) -> ApprovalWorkflowSummary:
    _validate_findings(findings)
    information = sum(
        item.severity is ApprovalWorkflowFindingSeverity.INFO for item in findings
    )
    warnings = sum(
        item.severity is ApprovalWorkflowFindingSeverity.WARNING for item in findings
    )
    blocking = sum(
        item.severity is ApprovalWorkflowFindingSeverity.BLOCKING for item in findings
    )
    approval_transition_valid = (
        approval_granted
        and transition_result.accepted
        and transition_result.transition.transition_id == "GWT-003"
        and transition_result.transition.from_state
        is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
        and transition_result.transition.to_state
        is GovernedWorkflowState.TICKET_APPROVED
        and transition_result.transition.trigger
        is WorkflowTransitionTrigger.TICKET_APPROVED
        and transition_result.transition.authority is WorkflowTransitionAuthority.HUMAN
    )
    rejection_transition_valid = (
        not approval_granted
        and transition_result.accepted
        and transition_result.transition.transition_id == "GWT-025"
        and transition_result.transition.from_state
        is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
        and transition_result.transition.to_state
        is GovernedWorkflowState.AWAITING_CORRECTION
        and transition_result.transition.trigger
        is WorkflowTransitionTrigger.HUMAN_REJECTED
        and transition_result.transition.authority is WorkflowTransitionAuthority.HUMAN
    )
    execution_prohibition_valid = (
        not transition_result.resulting_snapshot.runtime_projection.worker_id_present
        and not transition_result.resulting_snapshot.runtime_projection.workspace_binding_present
    )
    return _make_model(
        ApprovalWorkflowSummary,
        "summary_SHA256",
        APPROVAL_WORKFLOW_SUMMARY_DIGEST_ALGORITHM,
        P18_2_continuation_valid=True,
        approval_request_valid=True,
        approval_decision_valid=request.decision_input.decision
        in {HumanApprovalDecision.APPROVE, HumanApprovalDecision.REJECT},
        human_authority_valid=request.decision_input.authority
        is ApprovalWorkflowDecisionAuthority.HUMAN,
        artifact_binding_valid=True,
        TicketSpec_binding_valid=True,
        WorkPacket_binding_valid=True,
        publication_boundary_valid=(
            publication_boundary.publication_applied
            and publication_boundary.approved_ticket_matches_work_packet_source
            and publication_boundary.published_ticket_matches_approved_ticket
        )
        if approval_granted
        else not publication_boundary.publication_applied,
        approval_transition_valid=approval_transition_valid,
        rejection_transition_valid=rejection_transition_valid,
        replay_policy_valid=True,
        execution_prohibition_valid=execution_prohibition_valid,
        P18_4_handoff_valid=handoff.P18_4_ready == approval_granted
        and handoff.execution_started is False,
        information_finding_count=information,
        warning_finding_count=warnings,
        blocking_finding_count=blocking,
    )


def _validate_result_bindings(result: ApprovalWorkflowIntegrationResult) -> None:
    if result.request.artifact_binding != result.artifact_binding:
        raise ApprovalWorkflowIntegrityError(
            "result artifact binding must match request"
        )
    if result.request.decision_input != result.decision_input:
        raise ApprovalWorkflowIntegrityError("result decision input must match request")
    if result.ticket_approval_record.decision != result.decision_input.decision:
        raise ApprovalWorkflowIntegrityError("approval record decision mismatch")
    if result.approval_granted != (
        result.decision_input.decision is HumanApprovalDecision.APPROVE
    ):
        raise ApprovalWorkflowIntegrityError("approval grant mismatch")
    if result.approval_granted:
        if result.ticket_publication_result is None:
            raise ApprovalWorkflowIntegrityError("approved result requires publication")
        if result.workflow_transition_result.transition.transition_id != "GWT-003":
            raise ApprovalWorkflowIntegrityError("approved result must use GWT-003")
    else:
        if result.ticket_publication_result is not None:
            raise ApprovalWorkflowIntegrityError("rejected result must not publish")
        if result.workflow_transition_result.transition.transition_id != "GWT-025":
            raise ApprovalWorkflowIntegrityError("rejected result must use GWT-025")
    if result.authority is not ApprovalWorkflowDecisionAuthority.HUMAN:
        raise ApprovalWorkflowPolicyError("result authority must be human")
    if any((
        result.ticket_execution_authorized,
        result.WorkPacket_execution_authorized,
        result.ticket_execution_started,
        result.WorkPacket_execution_started,
        result.production_readiness_claimed,
    )):
        raise ApprovalWorkflowPolicyError(
            "approval result must not authorize execution"
        )
    if any(
        count != 0
        for count in (
            result.worker_dispatch_count,
            result.command_execution_count,
            result.provider_dispatch_count,
            result.model_inference_count,
            result.Git_commands_executed,
            result.Docker_commands_executed,
            result.Graphify_commands_executed,
            result.GBrain_calls,
            result.Paperclip_calls,
        )
    ):
        raise ApprovalWorkflowPolicyError("approval result contains forbidden activity")


def _integration_id_from_record(record: object) -> str:
    digest = _digest_from_record(APPROVAL_WORKFLOW_ID_DIGEST_ALGORITHM, record)
    return f"AWI-P18-{digest[:12]}"


__all__ = (
    "APPROVAL_WORKFLOW_INTEGRATION_SCHEMA_VERSION",
    "APPROVAL_WORKFLOW_INTEGRATION_POLICY_ID",
    "ApprovalWorkflowDecisionAuthority",
    "ApprovalWorkflowState",
    "ApprovalWorkflowResultDecision",
    "ApprovalWorkflowFindingSeverity",
    "ApprovalWorkflowFindingCode",
    "ApprovalWorkflowArtifactBinding",
    "ApprovalWorkflowDecisionInput",
    "ApprovalWorkflowRequest",
    "ApprovalWorkflowFinding",
    "ApprovalWorkflowPublicationBoundary",
    "ApprovalWorkflowP18_4Handoff",
    "ApprovalWorkflowSummary",
    "ApprovalWorkflowIntegrationResult",
    "ApprovalWorkflowIntegrationError",
    "ApprovalWorkflowInputError",
    "ApprovalWorkflowIntegrityError",
    "ApprovalWorkflowPolicyError",
    "ApprovalWorkflowStateError",
    "ApprovalWorkflowValidationError",
    "build_approval_workflow_decision_input",
    "build_canonical_p18_approval_workflow_request",
    "validate_approval_workflow_request",
    "build_approval_workflow_integration",
    "validate_approval_workflow_integration_result",
    "summarize_approval_workflow_integration",
)
