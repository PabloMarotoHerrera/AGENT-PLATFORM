"""Governed Ticket Factory runtime integration for Agent Platform P18.2.

This module bridges the accepted P18.1 project-intake result into the existing
P16 Ticket Factory planning contracts and the P18.0 governed workflow state
machine.  It is intentionally pure: no provider calls, model calls, filesystem
access, database access, Git mutation, Docker, Graphify, workspace allocation
or runtime execution are performed here.  The only WorkPacket action is a
deterministic in-memory P17 compile-only contract call.
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
    AuthorityReferenceKind,
    AuthorityReferenceSpec,
    ContextAssemblyPolicy,
    ContextAssemblyRequest,
    ContextPack,
    ContextPriority,
    ContextSensitivity,
    ContextSourceKind,
    ContextSourceSpec,
    DependencyKind,
    DependencyScope,
    FreshDependencyPlanningEvidence,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    ParallelPlanningPolicy,
    ParallelizationHint,
    ProjectSpec,
    RepositoryScopeSpec,
    ReviewedTicketProposal,
    TicketDependencyPlan,
    TicketDependencySpec,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    TicketApprovalRequest,
    TicketPlanningRequest,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    TicketResponseContractSpec,
    TicketSynthesisRequest,
    TicketSpec,
    TicketType,
    TicketValidationStepSpec,
    WaveDisposition,
    assemble_context_pack,
    build_ticket_approval_record,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    build_ticket_synthesis_review,
    lint_ticket_collection,
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
    validate_governed_workflow_snapshot,
    validate_governed_workflow_transition_request,
)
from hermes_cli.agent_platform.workflow.project_intake import (
    ProjectIntakeResult,
    validate_project_intake_result,
)
from hermes_cli.agent_platform.work_packet import (
    WORK_PACKET_COMPILER_POLICY_ID,
    WorkPacketCompilationRequest,
    WorkPacketCompilationResult,
    build_work_packet_compilation_authorization,
    compile_ticket_spec_to_work_packet,
)


TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION = 1
TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID = (
    "pepper-ticket-factory-runtime-integration-v1"
)

TICKET_FACTORY_RUNTIME_BINDING_DIGEST_ALGORITHM = (
    "agent-platform-ticket-factory-runtime-binding-sha256-v1"
)
TICKET_FACTORY_WORK_PACKET_CONTINUATION_DIGEST_ALGORITHM = (
    "agent-platform-ticket-factory-work-packet-continuation-sha256-v1"
)
TICKET_FACTORY_RUNTIME_FINDING_DIGEST_ALGORITHM = (
    "agent-platform-ticket-factory-runtime-finding-sha256-v1"
)
TICKET_FACTORY_RUNTIME_SUMMARY_DIGEST_ALGORITHM = (
    "agent-platform-ticket-factory-runtime-summary-sha256-v1"
)
TICKET_FACTORY_RUNTIME_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-ticket-factory-runtime-result-sha256-v1"
)
TICKET_FACTORY_RUNTIME_ID_DIGEST_ALGORITHM = (
    "agent-platform-ticket-factory-runtime-id-sha256-v1"
)

_CANONICAL_P18_UI_A_COMMIT = "f55b8a2cc62c9ba0620a14f51b968107b75a78f1"
_CANONICAL_PROJECT_ID = "P18"
_CANONICAL_TICKET_ID = "P18.2"
_CANONICAL_PREREQUISITE_TICKET_ID = "P18.1"
_CANONICAL_PROJECT_TITLE = "Manual-to-Hermes Workflow Migration"
_CANONICAL_TICKET_TITLE = "Ticket Factory Runtime Integration"
_DIGEST_PATTERN = r"^[a-f0-9]{64}$"
_COMMIT_PATTERN = r"^[a-f0-9]{40}$"
_INTEGRATION_ID_PATTERN = r"^TFI-P18-[a-f0-9]{12}$"
_FINDING_ID_PATTERN = r"^TFRF-[0-9]{3}$"
_CONTROL_OR_ANSI_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x1b]")
_PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[/\\]Users[/\\]|/Users/|/home/)")
_SHELL_COMMAND_PATTERN = re.compile(
    r"(?:\bgit\s+(?:add|commit|push|checkout|switch|merge|rebase|reset|stash|tag|worktree)\b)"
    r"|(?:\bdocker\s+(?:build|run|compose|pull|push)\b)"
    r"|(?:\bgraphify\s+(?:update|extract|export|cluster|recluster|query|path|explain)\b)"
    r"|(?:\brm\s+-rf\b)",
    re.IGNORECASE,
)
_CREDENTIAL_MARKERS = (
    "access_token",
    "refresh_token",
    "authorization:",
    "bearer ",
    "client_secret",
    "api_key",
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
    "raw conversation",
    "chatgpt transcript",
    "opencode transcript",
    "stdout:",
    "stderr:",
    "diff --git",
)
_SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
_REQUIRED_RESPONSE_SECTIONS = (
    "Summary",
    "Files inspected",
    "Files modified",
    "Tests/commands run",
    "Decisions made",
    "Limitations",
)
_REQUIRED_FORBIDDEN_ACTIONS = (
    "git add",
    "git commit",
    "git push",
    "git reset",
    "git clean",
    "git stash",
    "git worktree",
    "Graphify",
    "Docker",
    "provider dispatch",
    "model inference",
)
_ALLOWED_PATHS = (
    "2_products/pepper-agent/hermes_cli/agent_platform/workflow/**",
    "2_products/pepper-agent/tests/hermes_cli/**",
    "2_products/pepper-agent/docs/agent-platform/**",
    "2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv",
    "2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv",
)

DigestText = Annotated[str, Field(pattern=_DIGEST_PATTERN)]
CommitText = Annotated[str, Field(pattern=_COMMIT_PATTERN)]
IntegrationIdentifier = Annotated[str, Field(pattern=_INTEGRATION_ID_PATTERN)]
FindingIdentifier = Annotated[str, Field(pattern=_FINDING_ID_PATTERN)]
BoundedText = Annotated[str, Field(min_length=1, max_length=1024)]


class TicketFactoryRuntimeIntegrationError(ValueError):
    """Base error for P18.2 Ticket Factory runtime integration failures."""


class TicketFactoryRuntimeInputError(TicketFactoryRuntimeIntegrationError):
    """Raised when caller-supplied P18.2 integration input is malformed."""


class TicketFactoryRuntimeIntegrityError(TicketFactoryRuntimeIntegrationError):
    """Raised when deterministic P18.2 integrity evidence is invalid."""


class TicketFactoryRuntimePolicyError(TicketFactoryRuntimeIntegrationError):
    """Raised when P18.2 integration policy is violated."""


class TicketFactoryRuntimeStateError(TicketFactoryRuntimeIntegrationError):
    """Raised when workflow state cannot accept P18.2 progression."""


class TicketFactoryRuntimeValidationError(TicketFactoryRuntimeIntegrationError):
    """Raised when immutable P18.2 integration evidence fails validation."""


class TicketFactoryRuntimeState(str, Enum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class TicketFactoryRuntimeDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class TicketFactoryRuntimeFindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class TicketFactoryRuntimeFindingCode(str, Enum):
    PROJECT_INTAKE_READY = "project_intake_ready"
    PROJECT_SPEC_BUILT = "project_spec_built"
    TICKET_SPEC_BUILT = "ticket_spec_built"
    CONTEXT_PACK_ASSEMBLED = "context_pack_assembled"
    DEPENDENCY_PLAN_READY = "dependency_plan_ready"
    TICKET_LINT_ACCEPTED = "ticket_lint_accepted"
    WORK_PACKET_CONTINUATION_READY = "work_packet_continuation_ready"
    WORKFLOW_TRANSITION_READY = "workflow_transition_ready"
    TICKET_APPROVAL_REQUIRED = "ticket_approval_required"
    AUTHORITY_BOUNDARY_PRESERVED = "authority_boundary_preserved"
    INTEGRATION_ACCEPTED = "integration_accepted"
    INTEGRATION_REJECTED = "integration_rejected"


class _TicketFactoryRuntimeModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        protected_namespaces=(),
        validate_default=True,
        str_strip_whitespace=True,
    )


def _validate_bounded_text(value: str, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if value != value.strip():
        raise ValueError(f"{label} must be stripped")
    if not value:
        raise ValueError(f"{label} must be non-empty")
    if _CONTROL_OR_ANSI_PATTERN.search(value):
        raise ValueError(f"{label} contains unsafe control characters")
    if _PERSONAL_PATH_PATTERN.search(value):
        raise ValueError(f"{label} contains an absolute personal path")
    if _SHELL_COMMAND_PATTERN.search(value):
        raise ValueError(f"{label} contains shell command content")
    lowered = value.lower()
    if any(marker in lowered for marker in _CREDENTIAL_MARKERS):
        raise ValueError(f"{label} contains credential-like content")
    if any(marker in lowered for marker in _RAW_CONTEXT_MARKERS):
        raise ValueError(f"{label} contains raw context content")
    if _SECRET_TOKEN_PATTERN.search(value):
        raise ValueError(f"{label} contains credential-like content")
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
    model_type: type[_TicketFactoryRuntimeModel],
    digest_field: str,
    algorithm: str,
    **values: object,
) -> _TicketFactoryRuntimeModel:
    data = dict(values)
    data[digest_field] = _digest_from_record(algorithm, data)
    return model_type(**data)


def _validated_model(
    model_type: type[_TicketFactoryRuntimeModel], value: object
) -> _TicketFactoryRuntimeModel:
    try:
        if isinstance(value, BaseModel):
            return model_type.model_validate(
                value.model_dump(mode="python", warnings=False)
            )
        return model_type.model_validate(value)
    except (AttributeError, ValueError) as exc:
        raise TicketFactoryRuntimeValidationError(
            f"invalid {model_type.__name__}"
        ) from exc


class TicketFactoryRuntimeBinding(_TicketFactoryRuntimeModel):
    schema_version: Literal[1] = TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION
    policy_id: Literal["pepper-ticket-factory-runtime-integration-v1"] = (
        TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID
    )
    project_intake_result_SHA256: DigestText
    source_workflow_snapshot_SHA256: DigestText
    P18_UI_A_parent_commit: CommitText
    ticket_factory_project_id: Literal["P18"] = _CANONICAL_PROJECT_ID
    ticket_factory_ticket_id: Literal["P18.2"] = _CANONICAL_TICKET_ID
    ticket_factory_runtime_owner: Literal["pepper_governed_runtime"] = (
        "pepper_governed_runtime"
    )
    provider_dispatch_authorized: Literal[False] = False
    model_inference_authorized: Literal[False] = False
    work_packet_compilation_authorized_before_ticket_approval: Literal[True] = True
    binding_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_binding(self) -> TicketFactoryRuntimeBinding:
        if self.P18_UI_A_parent_commit != _CANONICAL_P18_UI_A_COMMIT:
            raise ValueError("P18_UI_A_parent_commit must bind committed P18.UI-A")
        if self.binding_SHA256 != _model_digest(
            TICKET_FACTORY_RUNTIME_BINDING_DIGEST_ALGORITHM,
            self,
            "binding_SHA256",
        ):
            raise ValueError("binding_SHA256 must match Ticket Factory binding digest")
        return self


class TicketFactoryWorkPacketContinuation(_TicketFactoryRuntimeModel):
    source_ticket_id: Literal["P18.2"] = _CANONICAL_TICKET_ID
    compiler_policy_id: Literal["pepper-work-packet-compiler-policy-v1"] = (
        WORK_PACKET_COMPILER_POLICY_ID
    )
    dependency_plan_SHA256: DigestText
    lint_report_SHA256: DigestText
    compilation_result_SHA256: DigestText
    work_packet_id: BoundedText
    work_packet_SHA256: DigestText
    approved_ticket_required: Literal[True] = True
    work_packet_compilation_allowed_before_human_ticket_approval: Literal[True] = True
    human_ticket_approval_required_before_execution: Literal[True] = True
    human_ticket_approval_present: Literal[False] = False
    logical_publication_required: Literal[True] = True
    compilation_authorization_present: Literal[True] = True
    work_packet_compilation_completed: Literal[True] = True
    command_execution_authorized: Literal[False] = False
    runtime_execution_authorized: Literal[False] = False
    human_git_authority_required: Literal[True] = True
    compiler_invocation_count: int = Field(ge=1, le=1, strict=True)
    continuation_SHA256: DigestText

    @field_validator("work_packet_id", mode="after")
    @classmethod
    def _validate_work_packet_id(cls, value: str) -> str:
        return _validate_bounded_text(value, "WorkPacket identifier")

    @model_validator(mode="after")
    def _validate_continuation(self) -> TicketFactoryWorkPacketContinuation:
        if self.continuation_SHA256 != _model_digest(
            TICKET_FACTORY_WORK_PACKET_CONTINUATION_DIGEST_ALGORITHM,
            self,
            "continuation_SHA256",
        ):
            raise ValueError(
                "continuation_SHA256 must match WorkPacket continuation digest"
            )
        return self


class TicketFactoryRuntimeRequest(_TicketFactoryRuntimeModel):
    schema_version: Literal[1] = TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION
    policy_id: Literal["pepper-ticket-factory-runtime-integration-v1"] = (
        TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID
    )
    project_intake_result: ProjectIntakeResult
    P18_UI_A_parent_commit: CommitText


class TicketFactoryRuntimeFinding(_TicketFactoryRuntimeModel):
    finding_id: FindingIdentifier
    severity: TicketFactoryRuntimeFindingSeverity
    code: TicketFactoryRuntimeFindingCode
    subject_id: BoundedText
    summary: BoundedText
    failed_invariant: BoundedText | None
    finding_SHA256: DigestText

    @field_validator("subject_id", "summary", mode="after")
    @classmethod
    def _validate_text_fields(cls, value: str) -> str:
        return _validate_bounded_text(value, "Ticket Factory finding field")

    @field_validator("failed_invariant", mode="after")
    @classmethod
    def _validate_optional_text(cls, value: str | None) -> str | None:
        if value is not None:
            return _validate_bounded_text(value, "Ticket Factory finding invariant")
        return value

    @model_validator(mode="after")
    def _validate_finding(self) -> TicketFactoryRuntimeFinding:
        invalid_code = self.code is TicketFactoryRuntimeFindingCode.INTEGRATION_REJECTED
        if (
            invalid_code
            and self.severity is not TicketFactoryRuntimeFindingSeverity.BLOCKING
        ):
            raise ValueError("rejected findings must be blocking")
        if (
            not invalid_code
            and self.severity is TicketFactoryRuntimeFindingSeverity.BLOCKING
        ):
            raise ValueError("blocking findings require rejected code")
        if self.finding_SHA256 != _model_digest(
            TICKET_FACTORY_RUNTIME_FINDING_DIGEST_ALGORITHM,
            self,
            "finding_SHA256",
        ):
            raise ValueError("finding_SHA256 must match Ticket Factory finding digest")
        return self


class TicketFactoryRuntimeSummary(_TicketFactoryRuntimeModel):
    project_intake_consumed: StrictBool
    project_spec_created: StrictBool
    ticket_spec_created: StrictBool
    context_pack_created: StrictBool
    dependency_plan_created: StrictBool
    lint_report_accepted: StrictBool
    work_packet_continuation_ready: StrictBool
    workflow_transition_valid: StrictBool
    human_ticket_approval_required: StrictBool
    information_finding_count: int = Field(ge=0, le=128, strict=True)
    warning_finding_count: int = Field(ge=0, le=128, strict=True)
    blocking_finding_count: int = Field(ge=0, le=128, strict=True)
    TicketSpec_runtime_integration_satisfied: StrictBool
    P18_3_ready: StrictBool
    summary_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_summary(self) -> TicketFactoryRuntimeSummary:
        valid_flags = (
            self.project_intake_consumed,
            self.project_spec_created,
            self.ticket_spec_created,
            self.context_pack_created,
            self.dependency_plan_created,
            self.lint_report_accepted,
            self.work_packet_continuation_ready,
            self.workflow_transition_valid,
            self.human_ticket_approval_required,
        )
        if self.blocking_finding_count == 0 and not all(valid_flags):
            raise ValueError("valid summary flags are required when no blockers exist")
        requirement = all(valid_flags) and self.blocking_finding_count == 0
        if self.TicketSpec_runtime_integration_satisfied != requirement:
            raise ValueError("TicketSpec integration flag must derive from summary")
        if self.P18_3_ready != requirement:
            raise ValueError("P18.3 readiness must derive from TicketSpec integration")
        if self.summary_SHA256 != _model_digest(
            TICKET_FACTORY_RUNTIME_SUMMARY_DIGEST_ALGORITHM,
            self,
            "summary_SHA256",
        ):
            raise ValueError("summary_SHA256 must match Ticket Factory summary digest")
        return self


class TicketFactoryRuntimeIntegrationResult(_TicketFactoryRuntimeModel):
    schema_version: Literal[1] = TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION
    policy_id: Literal["pepper-ticket-factory-runtime-integration-v1"] = (
        TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID
    )
    integration_id: IntegrationIdentifier
    state: TicketFactoryRuntimeState
    decision: TicketFactoryRuntimeDecision
    binding: TicketFactoryRuntimeBinding
    project_spec: ProjectSpec
    ticket_spec: TicketSpec
    context_pack: ContextPack
    dependency_plan: TicketDependencyPlan
    lint_report: TicketLintReport
    work_packet_continuation: TicketFactoryWorkPacketContinuation
    work_packet_compilation_result: WorkPacketCompilationResult
    previous_workflow_snapshot_SHA256: DigestText
    workflow_transition_result: GovernedWorkflowTransitionResult
    resulting_workflow_snapshot: GovernedWorkflowSnapshot
    findings: tuple[TicketFactoryRuntimeFinding, ...] = Field(
        min_length=1, max_length=128
    )
    summary: TicketFactoryRuntimeSummary
    TicketSpec_runtime_integration_satisfied: StrictBool
    P18_3_ready: StrictBool
    human_ticket_approval_present: Literal[False]
    ticket_execution_authorized: Literal[False]
    WorkPacket_execution_authorized: Literal[False]
    production_readiness_claimed: Literal[False]
    provider_dispatch_count: int = Field(ge=0, le=0, strict=True)
    model_inference_count: int = Field(ge=0, le=0, strict=True)
    Git_commands_executed: int = Field(ge=0, le=0, strict=True)
    Docker_commands_executed: int = Field(ge=0, le=0, strict=True)
    Graphify_commands_executed: int = Field(ge=0, le=0, strict=True)
    WorkPacket_compilation_count: int = Field(ge=1, le=1, strict=True)
    result_SHA256: DigestText

    @model_validator(mode="after")
    def _validate_result(self) -> TicketFactoryRuntimeIntegrationResult:
        _validate_findings(self.findings)
        _validate_result_bindings(self)
        if self.workflow_transition_result.accepted:
            if self.state is not TicketFactoryRuntimeState.COMPLETED:
                raise ValueError(
                    "accepted transition requires completed integration state"
                )
            if self.decision is not TicketFactoryRuntimeDecision.ACCEPTED:
                raise ValueError("accepted transition requires accepted decision")
        else:
            if self.state is not TicketFactoryRuntimeState.BLOCKED:
                raise ValueError(
                    "rejected transition requires blocked integration state"
                )
            if self.decision is not TicketFactoryRuntimeDecision.REJECTED:
                raise ValueError("rejected transition requires rejected decision")
        if (
            self.TicketSpec_runtime_integration_satisfied
            != self.summary.TicketSpec_runtime_integration_satisfied
        ):
            raise ValueError("result integration flag must match summary")
        if self.P18_3_ready != self.summary.P18_3_ready:
            raise ValueError("result P18.3 readiness must match summary")
        if self.integration_id != _integration_id_from_result(self):
            raise ValueError(
                "integration_id must match deterministic integration identity"
            )
        if self.result_SHA256 != _model_digest(
            TICKET_FACTORY_RUNTIME_RESULT_DIGEST_ALGORITHM,
            self,
            "result_SHA256",
        ):
            raise ValueError("result_SHA256 must match Ticket Factory result digest")
        return self


def build_canonical_p18_ticket_factory_runtime_request(
    *,
    project_intake_result: ProjectIntakeResult,
    committed_p18_ui_a_commit: str,
) -> TicketFactoryRuntimeRequest:
    request = TicketFactoryRuntimeRequest(
        schema_version=TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION,
        policy_id=TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID,
        project_intake_result=project_intake_result,
        P18_UI_A_parent_commit=committed_p18_ui_a_commit,
    )
    validate_ticket_factory_runtime_request(request)
    return request


def validate_ticket_factory_runtime_request(
    request: TicketFactoryRuntimeRequest,
) -> None:
    try:
        validated = TicketFactoryRuntimeRequest.model_validate(
            request.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise TicketFactoryRuntimeValidationError(
            "invalid Ticket Factory runtime request"
        ) from exc
    _validate_request_policy(validated)


def build_ticket_factory_runtime_integration(
    request: TicketFactoryRuntimeRequest,
) -> TicketFactoryRuntimeIntegrationResult:
    validate_ticket_factory_runtime_request(request)
    validated = TicketFactoryRuntimeRequest.model_validate(
        request.model_dump(mode="python", warnings=False)
    )
    intake = validated.project_intake_result
    binding = _build_runtime_binding(validated)
    project_spec = _build_project_spec(validated)
    ticket_spec = _build_ticket_spec(validated)
    context_pack = _assemble_context_pack(project_spec, ticket_spec, validated)
    planning_request = TicketPlanningRequest(
        project_spec=project_spec,
        tickets=(ticket_spec,),
        external_dependency_resolutions=(),
        policy=ParallelPlanningPolicy(),
    )
    dependency_plan = build_ticket_dependency_plan(planning_request)
    lint_report = lint_ticket_collection(
        TicketLintRequest(
            project_spec=project_spec,
            tickets=(ticket_spec,),
            dependency_plan=dependency_plan,
            collection_complete=False,
        )
    )
    _validate_ready_dependency_plan(dependency_plan)
    _validate_lint_report(lint_report)
    work_packet_compilation_result = _compile_work_packet(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        lint_report=lint_report,
    )
    continuation = _build_work_packet_continuation(
        ticket_spec=ticket_spec,
        dependency_plan=dependency_plan,
        lint_report=lint_report,
        compilation_result=work_packet_compilation_result,
    )
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=intake.resulting_workflow_snapshot,
        trigger=WorkflowTransitionTrigger.TICKET_GENERATED,
        authority=WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        evidence_refs=("ticket_factory_candidate",),
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
            runtime_state="pepper:ticket_approval",
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
    transition_result = build_governed_workflow_transition(transition_request)
    if not transition_result.accepted:
        raise TicketFactoryRuntimeStateError("P18.0 Ticket Factory transition rejected")
    findings = _derive_findings(
        validated, dependency_plan, lint_report, transition_result
    )
    summary = _derive_summary(
        findings,
        dependency_plan,
        lint_report,
        continuation,
        transition_result,
    )
    state = (
        TicketFactoryRuntimeState.COMPLETED
        if summary.TicketSpec_runtime_integration_satisfied
        else TicketFactoryRuntimeState.BLOCKED
    )
    decision = (
        TicketFactoryRuntimeDecision.ACCEPTED
        if summary.TicketSpec_runtime_integration_satisfied
        else TicketFactoryRuntimeDecision.REJECTED
    )
    result_values = {
        "schema_version": TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION,
        "policy_id": TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID,
        "state": state,
        "decision": decision,
        "binding": binding,
        "project_spec": project_spec,
        "ticket_spec": ticket_spec,
        "context_pack": context_pack,
        "dependency_plan": dependency_plan,
        "lint_report": lint_report,
        "work_packet_continuation": continuation,
        "work_packet_compilation_result": work_packet_compilation_result,
        "previous_workflow_snapshot_SHA256": intake.resulting_workflow_snapshot.workflow_SHA256,
        "workflow_transition_result": transition_result,
        "resulting_workflow_snapshot": transition_result.resulting_snapshot,
        "findings": findings,
        "summary": summary,
        "TicketSpec_runtime_integration_satisfied": summary.TicketSpec_runtime_integration_satisfied,
        "P18_3_ready": summary.P18_3_ready,
        "human_ticket_approval_present": False,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "production_readiness_claimed": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "WorkPacket_compilation_count": 1,
    }
    result = _make_model(
        TicketFactoryRuntimeIntegrationResult,
        "result_SHA256",
        TICKET_FACTORY_RUNTIME_RESULT_DIGEST_ALGORITHM,
        integration_id=_integration_id_from_record(result_values),
        **result_values,
    )
    validate_ticket_factory_runtime_integration_result(result)
    return result


def validate_ticket_factory_runtime_integration_result(
    result: TicketFactoryRuntimeIntegrationResult,
) -> None:
    try:
        validated = TicketFactoryRuntimeIntegrationResult.model_validate(
            result.model_dump(mode="python", warnings=False)
        )
    except (AttributeError, ValueError) as exc:
        raise TicketFactoryRuntimeValidationError(
            "invalid Ticket Factory runtime integration result"
        ) from exc
    _validated_model(TicketFactoryRuntimeBinding, validated.binding)
    _validated_model(
        TicketFactoryWorkPacketContinuation, validated.work_packet_continuation
    )
    _validate_findings(validated.findings)
    if validated.summary != _derive_summary(
        validated.findings,
        validated.dependency_plan,
        validated.lint_report,
        validated.work_packet_continuation,
        validated.workflow_transition_result,
    ):
        raise TicketFactoryRuntimeValidationError("summary must match result evidence")
    _validate_result_bindings(validated)
    if validated.production_readiness_claimed is not False:
        raise TicketFactoryRuntimeValidationError("production readiness must be false")
    if validated.provider_dispatch_count != 0:
        raise TicketFactoryRuntimeValidationError(
            "provider dispatch count must be zero"
        )
    if validated.model_inference_count != 0:
        raise TicketFactoryRuntimeValidationError("model inference count must be zero")
    if validated.Git_commands_executed != 0:
        raise TicketFactoryRuntimeValidationError("Git command count must be zero")
    if validated.Docker_commands_executed != 0:
        raise TicketFactoryRuntimeValidationError("Docker command count must be zero")
    if validated.Graphify_commands_executed != 0:
        raise TicketFactoryRuntimeValidationError("Graphify command count must be zero")
    if validated.WorkPacket_compilation_count != 1:
        raise TicketFactoryRuntimeValidationError(
            "WorkPacket compilation count must be one"
        )
    if validated.human_ticket_approval_present is not False:
        raise TicketFactoryRuntimeValidationError("P18.3 human approval must be absent")
    if validated.ticket_execution_authorized is not False:
        raise TicketFactoryRuntimeValidationError(
            "ticket execution must be unauthorized"
        )
    if validated.WorkPacket_execution_authorized is not False:
        raise TicketFactoryRuntimeValidationError(
            "WorkPacket execution must be unauthorized"
        )


def summarize_ticket_factory_runtime_integration(
    result: TicketFactoryRuntimeIntegrationResult,
) -> TicketFactoryRuntimeSummary:
    validate_ticket_factory_runtime_integration_result(result)
    return result.summary


def _validate_request_policy(request: TicketFactoryRuntimeRequest) -> None:
    if request.schema_version != TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION:
        raise TicketFactoryRuntimePolicyError("schema_version must be exact")
    if request.policy_id != TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID:
        raise TicketFactoryRuntimePolicyError("policy_id must be exact")
    if request.P18_UI_A_parent_commit != _CANONICAL_P18_UI_A_COMMIT:
        raise TicketFactoryRuntimePolicyError(
            "P18.2 must resume from committed P18.UI-A parent"
        )
    try:
        validate_project_intake_result(request.project_intake_result)
        validate_governed_workflow_snapshot(
            request.project_intake_result.resulting_workflow_snapshot
        )
    except ValueError as exc:
        raise TicketFactoryRuntimeValidationError(
            "project intake result is invalid"
        ) from exc
    intake = request.project_intake_result
    if not intake.P18_2_ready:
        raise TicketFactoryRuntimeStateError("project intake must declare P18.2 ready")
    if (
        intake.resulting_workflow_snapshot.current_state
        is not GovernedWorkflowState.INTAKE_READY
    ):
        raise TicketFactoryRuntimeStateError(
            "project intake workflow snapshot must be intake_ready"
        )
    if intake.roadmap.next_ticket_ids != (_CANONICAL_TICKET_ID,):
        raise TicketFactoryRuntimePolicyError("project intake must hand off to P18.2")
    if _roadmap_prerequisite_ticket_ids(request) != (
        _CANONICAL_PREREQUISITE_TICKET_ID,
    ):
        raise TicketFactoryRuntimePolicyError(
            "P18.2 must preserve P18.1 as prerequisite"
        )


def _roadmap_prerequisite_ticket_ids(
    request: TicketFactoryRuntimeRequest,
) -> tuple[str, ...]:
    for item in request.project_intake_result.roadmap.items:
        if item.ticket_id == _CANONICAL_TICKET_ID:
            return item.prerequisite_ticket_ids
    raise TicketFactoryRuntimePolicyError("project intake roadmap must include P18.2")


def _build_runtime_binding(
    request: TicketFactoryRuntimeRequest,
) -> TicketFactoryRuntimeBinding:
    intake = request.project_intake_result
    return _make_model(
        TicketFactoryRuntimeBinding,
        "binding_SHA256",
        TICKET_FACTORY_RUNTIME_BINDING_DIGEST_ALGORITHM,
        schema_version=TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION,
        policy_id=TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID,
        project_intake_result_SHA256=intake.result_SHA256,
        source_workflow_snapshot_SHA256=intake.resulting_workflow_snapshot.workflow_SHA256,
        P18_UI_A_parent_commit=request.P18_UI_A_parent_commit,
        ticket_factory_project_id=_CANONICAL_PROJECT_ID,
        ticket_factory_ticket_id=_CANONICAL_TICKET_ID,
        ticket_factory_runtime_owner="pepper_governed_runtime",
        provider_dispatch_authorized=False,
        model_inference_authorized=False,
        work_packet_compilation_authorized_before_ticket_approval=True,
    )


def _scope() -> RepositoryScopeSpec:
    return RepositoryScopeSpec(
        allowed_paths=_ALLOWED_PATHS,
        forbidden_paths=(
            ".git/**",
            ".opencode/**",
            "graphify-out/**",
            "4_external/sources/**",
            "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
        ),
        allowed_actions=(
            "add bounded P18.2 workflow contracts",
            "add focused Ticket Factory integration tests",
            "update governed documentation and import manifest rows",
        ),
        forbidden_actions=_REQUIRED_FORBIDDEN_ACTIONS,
    )


def _authority_references(
    request: TicketFactoryRuntimeRequest,
) -> tuple[AuthorityReferenceSpec, ...]:
    intake = request.project_intake_result
    return (
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.TICKET,
            value="P18.1",
            rationale="Accepted project intake result supplies governed P18 context.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.GOVERNANCE_RECORD,
            value=intake.result_SHA256,
            rationale="P18.1 result digest is the bounded intake authority.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.TICKET,
            value="P18.UI-A",
            rationale="Committed Pepper product UI activation is the P18.2 parent.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.COMMIT,
            value=request.P18_UI_A_parent_commit,
            rationale="P18.2 resumes from this committed parent only.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.REPOSITORY_PATH,
            value="hermes_cli/agent_platform/workflow/ticket_factory_runtime.py",
            rationale="P18.2 adds a product-local workflow integration contract.",
        ),
    )


def _build_project_spec(request: TicketFactoryRuntimeRequest) -> ProjectSpec:
    intake = request.project_intake_result
    return ProjectSpec(
        project_id=_CANONICAL_PROJECT_ID,
        title=_CANONICAL_PROJECT_TITLE,
        objective=(
            "Migrate the manual Pepper workflow into governed Hermes runtime "
            "integration while preserving human authority boundaries."
        ),
        summary=(
            "P18 consumes P18.0 workflow contracts, P18.1 intake evidence and "
            "existing P16/P17 planning contracts without creating a parallel runtime."
        ),
        context=(
            f"Project intake {intake.intake_id} reached intake_ready state.",
            "P18.UI-A activated Pepper product UI before P18.2 resumed.",
            "P18.2 creates Ticket Factory planning evidence and stops at human ticket approval.",
        ),
        authority_references=_authority_references(request),
        scope=_scope(),
        constraints=(
            "Pepper remains a customized Hermes-derived product.",
            "Reuse P16 Ticket Factory and P17 WorkPacket compiler contracts before adding runtime logic.",
            "Human Git authority remains required and automatic Git mutation is not authorized.",
            "Provider dispatch, model inference, Docker, Graphify and production deployment are not authorized.",
        ),
        non_goals=(
            "Do not perform P18.3 human approval workflow integration.",
            "Do not allocate, queue or execute a WorkPacket in P18.2.",
            "Do not create G-Brain, Paperclip or a replacement Kanban store.",
        ),
        acceptance_criteria=(
            "P18.2 produces a validated TicketSpec from accepted P18.1 intake evidence.",
            "P18.2 records dependency, lint and WorkPacket continuation evidence without execution.",
            "The governed workflow transitions to awaiting_ticket_approval through GWT-002.",
        ),
        completion_verdict="p18_2_ticket_factory_runtime_integration_ready",
    )


def _build_ticket_spec(request: TicketFactoryRuntimeRequest) -> TicketSpec:
    return TicketSpec(
        project_id=_CANONICAL_PROJECT_ID,
        ticket_id=_CANONICAL_TICKET_ID,
        title=_CANONICAL_TICKET_TITLE,
        ticket_type=TicketType.INTEGRATION,
        objective=(
            "Integrate accepted P18.1 intake with existing Ticket Factory planning "
            "contracts and advance the governed workflow to ticket approval."
        ),
        context=(
            "P18.1 intake is the bounded source of project identity and context.",
            "P16 Ticket Factory contracts remain the TicketSpec planning authority.",
            "P17 WorkPacket compiler is used once for compile-only evidence before execution approval.",
            "P18.3 owns the next human ticket approval integration step.",
        ),
        authority_references=_authority_references(request),
        dependencies=(),
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=_scope(),
        constraints=(
            "Reuse existing Ticket Factory and WorkPacket contracts; duplicate runtime logic is prohibited.",
            "Human ticket approval remains required before the TicketSpec becomes approved.",
            "Rollback by removing only P18.2 workflow, test, documentation and governance rows.",
            "Provider dispatch, model inference, Docker, Graphify and Git mutation remain unauthorized.",
        ),
        tasks=(
            "Build ProjectSpec and TicketSpec from accepted P18.1 intake evidence.",
            "Assemble a bounded ContextPack from governed intake references without raw transcripts.",
            "Build TicketDependencyPlan and TicketLintReport using existing Ticket Factory contracts.",
            "Compile the generated TicketSpec once through the existing P17 WorkPacket compiler.",
            "Advance the governed workflow with GWT-002 to awaiting_ticket_approval.",
            "Record WorkPacket continuation requirements without authorizing execution.",
        ),
        acceptance_criteria=(
            "The integration result contains validated ProjectSpec, TicketSpec, ContextPack, dependency plan and lint evidence.",
            "The workflow transition is accepted from intake_ready to awaiting_ticket_approval.",
            "WorkPacket compilation count is one while runtime execution, provider/model dispatch, Docker, Graphify and Git mutation counts remain zero.",
        ),
        validation_steps=(
            TicketValidationStepSpec(
                validation_id="V1",
                description="Run the focused P18.2 Ticket Factory runtime integration contract tests.",
                command=(
                    "scripts/run_tests.sh "
                    "tests/hermes_cli/test_agent_platform_ticket_factory_runtime_integration.py -q"
                ),
                expected_result="Focused P18.2 Ticket Factory runtime integration tests pass.",
            ),
        ),
        response_contract=TicketResponseContractSpec(
            required_sections=_REQUIRED_RESPONSE_SECTIONS,
            completion_verdict="p18_2_ticket_factory_runtime_integration_ready",
        ),
        recommended_commit_message="P18.2 Add Ticket Factory runtime integration",
    )


def _context_sources(
    request: TicketFactoryRuntimeRequest,
) -> tuple[ContextSourceSpec, ...]:
    intake = request.project_intake_result
    return (
        ContextSourceSpec(
            source_id="CTX-P18-1-INTAKE",
            kind=ContextSourceKind.GOVERNANCE_RECORD,
            title="Accepted P18.1 intake result",
            source_reference="P18.1 project intake result digest",
            content=(
                f"Intake {intake.intake_id} is accepted, P18_2_ready is true, "
                f"and result digest is {intake.result_SHA256}."
            ),
            authority_references=_authority_references(request)[:2],
            sensitivity=ContextSensitivity.INTERNAL,
            priority=ContextPriority.CRITICAL,
            required=True,
        ),
        ContextSourceSpec(
            source_id="CTX-P18-UI-A",
            kind=ContextSourceKind.GOVERNANCE_RECORD,
            title="Committed Pepper product UI activation parent",
            source_reference="P18.UI-A committed parent digest",
            content=(
                "P18.UI-A is runtime-validated and committed as parent "
                f"{request.P18_UI_A_parent_commit}."
            ),
            authority_references=_authority_references(request)[2:4],
            sensitivity=ContextSensitivity.INTERNAL,
            priority=ContextPriority.HIGH,
            required=True,
        ),
        ContextSourceSpec(
            source_id="CTX-P18-2-HANDOFF",
            kind=ContextSourceKind.HUMAN_INSTRUCTION,
            title="P18.2 handoff boundary",
            source_reference="P18.1 and P18.UI-A handoff",
            content=(
                "P18.2 owns TicketSpec production and workflow progression to "
                "awaiting_ticket_approval; P18.3 owns human approval integration."
            ),
            authority_references=(),
            sensitivity=ContextSensitivity.INTERNAL,
            priority=ContextPriority.HIGH,
            required=True,
        ),
    )


def _assemble_context_pack(
    project_spec: ProjectSpec,
    ticket_spec: TicketSpec,
    request: TicketFactoryRuntimeRequest,
) -> ContextPack:
    return assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=project_spec,
            ticket_spec=ticket_spec,
            sources=_context_sources(request),
            policy=ContextAssemblyPolicy(max_items=8, max_total_characters=32768),
        )
    )


def _validate_ready_dependency_plan(plan: TicketDependencyPlan) -> None:
    if plan.project_id != _CANONICAL_PROJECT_ID:
        raise TicketFactoryRuntimePolicyError("dependency plan must bind P18")
    if plan.ticket_ids != (_CANONICAL_TICKET_ID,):
        raise TicketFactoryRuntimePolicyError("dependency plan must contain only P18.2")
    if plan.blocked_ticket_ids:
        raise TicketFactoryRuntimeStateError("P18.2 dependency plan must be unblocked")
    if len(plan.waves) != 1:
        raise TicketFactoryRuntimePolicyError(
            "P18.2 dependency plan must have one wave"
        )
    wave = plan.waves[0]
    if wave.ticket_ids != (_CANONICAL_TICKET_ID,):
        raise TicketFactoryRuntimePolicyError("P18.2 must be in the ready wave")
    if wave.disposition is not WaveDisposition.DEPENDENCY_READY:
        raise TicketFactoryRuntimeStateError("P18.2 wave must be dependency_ready")


def _validate_lint_report(report: TicketLintReport) -> None:
    if report.project_id != _CANONICAL_PROJECT_ID:
        raise TicketFactoryRuntimePolicyError("lint report must bind P18")
    if report.ticket_ids != (_CANONICAL_TICKET_ID,):
        raise TicketFactoryRuntimePolicyError("lint report must contain only P18.2")
    if report.disposition is not TicketLintDisposition.PASS:
        raise TicketFactoryRuntimePolicyError("P18.2 ticket lint must pass")


def _compile_work_packet(
    *,
    project_spec: ProjectSpec,
    ticket_spec: TicketSpec,
    context_pack: ContextPack,
    planning_request: TicketPlanningRequest,
    dependency_plan: TicketDependencyPlan,
    lint_report: TicketLintReport,
) -> WorkPacketCompilationResult:
    generation_request = TicketGenerationRequest(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        roles=(TicketGeneratorRole.INTEGRATION, TicketGeneratorRole.IMPLEMENTATION),
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    proposals = tuple(
        build_ticket_proposal(
            assignment=assignment,
            proposed_ticket=ticket_spec,
            rationale=(
                "P18.2 TicketSpec is generated from accepted P18.1 intake and "
                "bounded Ticket Factory runtime integration evidence."
            ),
            evidence_source_ids=tuple(item.source_id for item in context_pack.items),
            assumptions=(),
            risks=(
                "Execution remains unauthorized until later governed workflow stages.",
            ),
            unresolved_questions=(),
        )
        for assignment in assignments
    )
    reviewed = tuple(
        ReviewedTicketProposal(proposal=proposal, lint_report=lint_report)
        for proposal in proposals
    )
    synthesis_review = build_ticket_synthesis_review(
        TicketSynthesisRequest(
            generation_request=generation_request,
            assignments=assignments,
            reviewed_proposals=reviewed,
            dependency_plan=dependency_plan,
        )
    )
    planning_evidence = FreshDependencyPlanningEvidence(
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        evidence_reference="P18.2 dependency plan before compile-only WorkPacket creation.",
        rationale="The P17 compiler requires fresh deterministic dependency evidence.",
    )
    approval_record = build_ticket_approval_record(
        TicketApprovalRequest(
            project_spec=project_spec,
            seed_ticket=ticket_spec,
            synthesis_review=synthesis_review,
            decision=HumanApprovalDecision.APPROVE,
            conflict_resolutions=(),
            approval_evidence=HumanApprovalEvidence(
                reviewer_id="pepper-governed-runtime",
                decision_reference="P18.2 compile-only TicketSpec acceptance evidence.",
                rationale=(
                    "Accept deterministic TicketSpec for compile-only WorkPacket "
                    "creation; P18.3 human ticket approval remains pending."
                ),
            ),
            manual_replacement=None,
            fresh_planning_evidence=planning_evidence,
        )
    )
    publication_result = publish_canonical_ticket(
        TicketPublicationRequest(
            approval_record=approval_record,
            publication_evidence=TicketPublicationEvidence(
                publisher_id="pepper-governed-runtime",
                publication_reference="P18.2 compile-only canonical TicketSpec publication.",
                rationale=(
                    "Logical in-memory publication is required by the existing P17 "
                    "compiler and grants no execution authority."
                ),
            ),
            prior_publication=None,
            supersession_rationale=None,
        )
    )
    authorization = build_work_packet_compilation_authorization(
        authorizer_id="pepper-governed-runtime",
        authorization_reference="P18.2 deterministic compile-only authorization.",
        rationale=(
            "Invoke the accepted P17 compiler once to create a compile-only "
            "WorkPacket while preserving zero execution authority."
        ),
        approval_record=approval_record,
        publication_result=publication_result,
        risk_acknowledgement=None,
    )
    return compile_ticket_spec_to_work_packet(
        WorkPacketCompilationRequest(
            project_spec=project_spec,
            approval_record=approval_record,
            publication_result=publication_result,
            compilation_authorization=authorization,
        )
    )


def _build_work_packet_continuation(
    *,
    ticket_spec: TicketSpec,
    dependency_plan: TicketDependencyPlan,
    lint_report: TicketLintReport,
    compilation_result: WorkPacketCompilationResult,
) -> TicketFactoryWorkPacketContinuation:
    if ticket_spec.ticket_id != _CANONICAL_TICKET_ID:
        raise TicketFactoryRuntimePolicyError("WorkPacket continuation must bind P18.2")
    if compilation_result.work_packet.ticket_id != _CANONICAL_TICKET_ID:
        raise TicketFactoryRuntimePolicyError("compiled WorkPacket must bind P18.2")
    return _make_model(
        TicketFactoryWorkPacketContinuation,
        "continuation_SHA256",
        TICKET_FACTORY_WORK_PACKET_CONTINUATION_DIGEST_ALGORITHM,
        source_ticket_id=_CANONICAL_TICKET_ID,
        compiler_policy_id=WORK_PACKET_COMPILER_POLICY_ID,
        dependency_plan_SHA256=dependency_plan.plan_SHA256,
        lint_report_SHA256=lint_report.report_SHA256,
        compilation_result_SHA256=compilation_result.result_SHA256,
        work_packet_id=compilation_result.work_packet.work_packet_id,
        work_packet_SHA256=compilation_result.work_packet.work_packet_SHA256,
        approved_ticket_required=True,
        work_packet_compilation_allowed_before_human_ticket_approval=True,
        human_ticket_approval_required_before_execution=True,
        human_ticket_approval_present=False,
        logical_publication_required=True,
        compilation_authorization_present=True,
        work_packet_compilation_completed=True,
        command_execution_authorized=False,
        runtime_execution_authorized=False,
        human_git_authority_required=True,
        compiler_invocation_count=1,
    )


def _build_finding(
    finding_id: str,
    severity: TicketFactoryRuntimeFindingSeverity,
    code: TicketFactoryRuntimeFindingCode,
    subject_id: str,
    summary: str,
    failed_invariant: str | None = None,
) -> TicketFactoryRuntimeFinding:
    return _make_model(
        TicketFactoryRuntimeFinding,
        "finding_SHA256",
        TICKET_FACTORY_RUNTIME_FINDING_DIGEST_ALGORITHM,
        finding_id=finding_id,
        severity=severity,
        code=code,
        subject_id=subject_id,
        summary=summary,
        failed_invariant=failed_invariant,
    )


def _derive_findings(
    request: TicketFactoryRuntimeRequest,
    dependency_plan: TicketDependencyPlan,
    lint_report: TicketLintReport,
    transition_result: GovernedWorkflowTransitionResult,
) -> tuple[TicketFactoryRuntimeFinding, ...]:
    rows = (
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.PROJECT_INTAKE_READY,
            request.project_intake_result.intake_id,
            "Accepted P18.1 intake result is ready for P18.2.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.PROJECT_SPEC_BUILT,
            _CANONICAL_PROJECT_ID,
            "Ticket Factory ProjectSpec is built from governed intake context.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.TICKET_SPEC_BUILT,
            _CANONICAL_TICKET_ID,
            "P18.2 TicketSpec is produced by the existing Ticket Factory schema.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.CONTEXT_PACK_ASSEMBLED,
            _CANONICAL_TICKET_ID,
            "Bounded ContextPack is assembled without raw transcripts or secrets.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.DEPENDENCY_PLAN_READY,
            dependency_plan.plan_SHA256,
            "Dependency plan places P18.2 in a dependency-ready wave.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.TICKET_LINT_ACCEPTED,
            lint_report.report_SHA256,
            "Ticket policy lint passes for the P18.2 TicketSpec.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.WORK_PACKET_CONTINUATION_READY,
            WORK_PACKET_COMPILER_POLICY_ID,
            "Compile-only WorkPacket evidence is recorded while execution waits for human approval.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.WORKFLOW_TRANSITION_READY,
            transition_result.result_SHA256,
            "Governed workflow advances to awaiting_ticket_approval through GWT-002.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.TICKET_APPROVAL_REQUIRED,
            "P18.3",
            "Human ticket approval remains required and is deferred to P18.3.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.AUTHORITY_BOUNDARY_PRESERVED,
            "P18.2 authority boundary",
            "Provider, model, Git, Docker, Graphify and WorkPacket execution counts remain zero.",
        ),
        (
            TicketFactoryRuntimeFindingSeverity.INFO,
            TicketFactoryRuntimeFindingCode.INTEGRATION_ACCEPTED,
            _CANONICAL_TICKET_ID,
            "P18.2 Ticket Factory runtime integration is ready for P18.3.",
        ),
    )
    return tuple(
        _build_finding(f"TFRF-{index:03d}", severity, code, subject_id, summary)
        for index, (severity, code, subject_id, summary) in enumerate(rows, start=1)
    )


def _validate_findings(findings: tuple[TicketFactoryRuntimeFinding, ...]) -> None:
    if not findings:
        raise TicketFactoryRuntimeValidationError("findings must be non-empty")
    if len(findings) > 128:
        raise TicketFactoryRuntimeValidationError("findings exceed maximum")
    expected = tuple(f"TFRF-{index:03d}" for index in range(1, len(findings) + 1))
    if tuple(item.finding_id for item in findings) != expected:
        raise TicketFactoryRuntimeValidationError("finding IDs must be contiguous")
    if len({item.finding_SHA256 for item in findings}) != len(findings):
        raise TicketFactoryRuntimeValidationError("finding digests must be unique")
    for item in findings:
        _validated_model(TicketFactoryRuntimeFinding, item)


def _derive_summary(
    findings: tuple[TicketFactoryRuntimeFinding, ...],
    dependency_plan: TicketDependencyPlan,
    lint_report: TicketLintReport,
    continuation: TicketFactoryWorkPacketContinuation,
    transition_result: GovernedWorkflowTransitionResult,
) -> TicketFactoryRuntimeSummary:
    _validate_findings(findings)
    information = sum(
        item.severity is TicketFactoryRuntimeFindingSeverity.INFO for item in findings
    )
    warnings = sum(
        item.severity is TicketFactoryRuntimeFindingSeverity.WARNING
        for item in findings
    )
    blocking = sum(
        item.severity is TicketFactoryRuntimeFindingSeverity.BLOCKING
        for item in findings
    )
    dependency_ready = (
        dependency_plan.ticket_ids == (_CANONICAL_TICKET_ID,)
        and not dependency_plan.blocked_ticket_ids
        and len(dependency_plan.waves) == 1
        and dependency_plan.waves[0].disposition is WaveDisposition.DEPENDENCY_READY
    )
    lint_accepted = lint_report.disposition is TicketLintDisposition.PASS
    continuation_ready = (
        continuation.work_packet_compilation_allowed_before_human_ticket_approval
        and continuation.work_packet_compilation_completed
        and continuation.compiler_invocation_count == 1
        and not continuation.human_ticket_approval_present
        and not continuation.command_execution_authorized
        and not continuation.runtime_execution_authorized
    )
    transition_valid = (
        transition_result.accepted
        and transition_result.transition.from_state
        is GovernedWorkflowState.INTAKE_READY
        and transition_result.transition.to_state
        is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
        and transition_result.transition.trigger
        is WorkflowTransitionTrigger.TICKET_GENERATED
        and transition_result.transition.authority
        is WorkflowTransitionAuthority.GOVERNED_RUNTIME
        and transition_result.resulting_snapshot.current_state
        is GovernedWorkflowState.AWAITING_TICKET_APPROVAL
        and transition_result.human_action_required
    )
    return _make_model(
        TicketFactoryRuntimeSummary,
        "summary_SHA256",
        TICKET_FACTORY_RUNTIME_SUMMARY_DIGEST_ALGORITHM,
        project_intake_consumed=blocking == 0,
        project_spec_created=blocking == 0,
        ticket_spec_created=blocking == 0,
        context_pack_created=blocking == 0,
        dependency_plan_created=dependency_ready,
        lint_report_accepted=lint_accepted,
        work_packet_continuation_ready=continuation_ready,
        workflow_transition_valid=transition_valid,
        human_ticket_approval_required=transition_result.human_action_required,
        information_finding_count=information,
        warning_finding_count=warnings,
        blocking_finding_count=blocking,
        TicketSpec_runtime_integration_satisfied=(
            blocking == 0
            and dependency_ready
            and lint_accepted
            and continuation_ready
            and transition_valid
        ),
        P18_3_ready=(
            blocking == 0
            and dependency_ready
            and lint_accepted
            and continuation_ready
            and transition_valid
        ),
    )


def _validate_result_bindings(result: TicketFactoryRuntimeIntegrationResult) -> None:
    if result.project_spec.project_id != _CANONICAL_PROJECT_ID:
        raise ValueError("project_spec must bind P18")
    if result.ticket_spec.project_id != result.project_spec.project_id:
        raise ValueError("ticket_spec project_id must match project_spec")
    if result.ticket_spec.ticket_id != _CANONICAL_TICKET_ID:
        raise ValueError("ticket_spec must bind P18.2")
    if result.context_pack.project_id != result.project_spec.project_id:
        raise ValueError("context pack project_id must match project")
    if result.context_pack.ticket_id != result.ticket_spec.ticket_id:
        raise ValueError("context pack ticket_id must match ticket")
    if result.dependency_plan.ticket_ids != (_CANONICAL_TICKET_ID,):
        raise ValueError("dependency plan must bind P18.2")
    if result.lint_report.ticket_ids != (_CANONICAL_TICKET_ID,):
        raise ValueError("lint report must bind P18.2")
    if (
        result.work_packet_continuation.dependency_plan_SHA256
        != result.dependency_plan.plan_SHA256
    ):
        raise ValueError("WorkPacket continuation must bind dependency plan digest")
    if (
        result.work_packet_continuation.lint_report_SHA256
        != result.lint_report.report_SHA256
    ):
        raise ValueError("WorkPacket continuation must bind lint report digest")
    if (
        result.work_packet_continuation.compilation_result_SHA256
        != result.work_packet_compilation_result.result_SHA256
    ):
        raise ValueError("WorkPacket continuation must bind compilation result digest")
    if (
        result.work_packet_continuation.work_packet_id
        != result.work_packet_compilation_result.work_packet.work_packet_id
    ):
        raise ValueError("WorkPacket continuation must bind WorkPacket ID")
    if (
        result.work_packet_continuation.work_packet_SHA256
        != result.work_packet_compilation_result.work_packet.work_packet_SHA256
    ):
        raise ValueError("WorkPacket continuation must bind WorkPacket digest")
    if (
        result.work_packet_compilation_result.work_packet.ticket_id
        != _CANONICAL_TICKET_ID
    ):
        raise ValueError("compiled WorkPacket must bind P18.2")
    if result.work_packet_compilation_result.work_packet.execution_ready is not False:
        raise ValueError("compiled WorkPacket must not be execution-ready")
    if any(
        step.command_execution_authorized
        for step in result.work_packet_compilation_result.work_packet.validation_steps
    ):
        raise ValueError("compiled WorkPacket must not authorize command execution")
    if result.work_packet_compilation_result.fresh_lint_report != result.lint_report:
        raise ValueError("compilation result must preserve lint report")
    if result.work_packet_compilation_result.dependency_plan != result.dependency_plan:
        raise ValueError("compilation result must preserve dependency plan")
    if (
        result.previous_workflow_snapshot_SHA256
        != result.workflow_transition_result.previous_snapshot_SHA256
    ):
        raise ValueError("previous snapshot digest must bind transition result")
    if (
        result.resulting_workflow_snapshot
        != result.workflow_transition_result.resulting_snapshot
    ):
        raise ValueError("resulting snapshot must match transition result")
    if (
        result.resulting_workflow_snapshot.current_state
        is not GovernedWorkflowState.AWAITING_TICKET_APPROVAL
    ):
        raise ValueError("resulting workflow snapshot must be awaiting_ticket_approval")
    if result.resulting_workflow_snapshot.pending_human_action != "ticket_approval":
        raise ValueError("P18.2 must stop at ticket approval human action")


def _integration_id_from_record(record: object) -> str:
    digest = _digest_from_record(TICKET_FACTORY_RUNTIME_ID_DIGEST_ALGORITHM, record)
    return f"TFI-P18-{digest[:12]}"


def _integration_id_from_result(result: TicketFactoryRuntimeIntegrationResult) -> str:
    record = result.model_dump(
        mode="json",
        exclude={"integration_id", "result_SHA256"},
        warnings=False,
    )
    return _integration_id_from_record(record)


__all__ = (
    "TICKET_FACTORY_RUNTIME_INTEGRATION_SCHEMA_VERSION",
    "TICKET_FACTORY_RUNTIME_INTEGRATION_POLICY_ID",
    "TicketFactoryRuntimeState",
    "TicketFactoryRuntimeDecision",
    "TicketFactoryRuntimeFindingSeverity",
    "TicketFactoryRuntimeFindingCode",
    "TicketFactoryRuntimeBinding",
    "TicketFactoryWorkPacketContinuation",
    "TicketFactoryRuntimeRequest",
    "TicketFactoryRuntimeFinding",
    "TicketFactoryRuntimeSummary",
    "TicketFactoryRuntimeIntegrationResult",
    "TicketFactoryRuntimeIntegrationError",
    "TicketFactoryRuntimeInputError",
    "TicketFactoryRuntimeIntegrityError",
    "TicketFactoryRuntimePolicyError",
    "TicketFactoryRuntimeStateError",
    "TicketFactoryRuntimeValidationError",
    "build_canonical_p18_ticket_factory_runtime_request",
    "validate_ticket_factory_runtime_request",
    "build_ticket_factory_runtime_integration",
    "validate_ticket_factory_runtime_integration_result",
    "summarize_ticket_factory_runtime_integration",
)
