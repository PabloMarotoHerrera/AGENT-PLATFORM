"""Governed P18.9.0 Ticket Architect bridge.

This module turns the current Pepper next action into canonical P16/P17/P18
evidence. It does not call providers, dispatch workers, create Kanban tasks,
run commands, mutate Git, invoke Docker, or invoke Graphify.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from pathlib import Path
import re
import threading
from typing import Any

from pydantic import BaseModel

from hermes_constants import get_hermes_home
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
    FreshDependencyPlanningEvidence,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    ParallelPlanningPolicy,
    ParallelizationHint,
    ProjectSpec,
    RepositoryScopeSpec,
    ReviewedTicketProposal,
    TicketApprovalRecord,
    TicketApprovalRequest,
    TicketDependencyPlan,
    TicketGenerationRequest,
    TicketGeneratorRole,
    TicketLintDisposition,
    TicketLintReport,
    TicketLintRequest,
    TicketPlanningRequest,
    TicketPublicationEvidence,
    TicketPublicationRequest,
    TicketPublicationResult,
    TicketResponseContractSpec,
    TicketSpec,
    TicketSynthesisRequest,
    TicketType,
    TicketValidationStepSpec,
    assemble_context_pack,
    build_ticket_approval_record,
    build_ticket_dependency_plan,
    build_ticket_proposal,
    build_ticket_synthesis_review,
    lint_ticket_collection,
    prepare_ticket_generator_assignments,
    publish_canonical_ticket,
)
from hermes_cli.agent_platform.work_packet import (
    WORK_PACKET_COMPILER_POLICY_ID,
    WorkPacketCompilationRequest,
    WorkPacketCompilationResult,
    build_work_packet_compilation_authorization,
    compile_ticket_spec_to_work_packet,
)
from hermes_cli.agent_platform.workflow import governed_state_machine as gsm
from hermes_cli.agent_platform.workflow.governed_state_machine import (
    GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
    GovernedWorkflowState,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowRuntimeKind,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_governed_workflow_identity,
    build_governed_workflow_transition,
    build_hermes_workflow_projection,
    build_initial_governed_workflow_snapshot,
    validate_governed_workflow_transition_request,
)


TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION = 1
TICKET_ARCHITECT_BRIDGE_POLICY_ID = "pepper-ticket-architect-bridge-p18-9-0-v1"
TICKET_ARCHITECT_BRIDGE_DIGEST_ALGORITHM = (
    "agent-platform-ticket-architect-bridge-record-sha256-v1"
)
TICKET_APPROVAL_PUBLICATION_POLICY_ID = (
    "pepper-ticket-approval-publication-p18-9-0-v1"
)
TICKET_APPROVAL_PUBLICATION_DIGEST_ALGORITHM = (
    "agent-platform-ticket-approval-publication-p18-9-0-sha256-v1"
)

CANONICAL_PROJECT_ID = "PEPPER"
CANONICAL_PROJECT_NAME = "Pepper"
CANONICAL_MACROPROJECT_ID = "P18.9"
CANONICAL_MACROPROJECT_TITLE = "Pepper Product Personalization"
CANONICAL_TICKET_ID = "P18.9.0"
CANONICAL_TICKET_TITLE = "Product Inventory, IA Decision, and Acceptance Contract"
CANONICAL_NEXT_ACTION_ID = "GENERATE_P18_9_0"
CANONICAL_ROADMAP_AUTHORITY = "human-approved-p18.9-roadmap"
CANONICAL_WORKFLOW_PROJECT_ID = "P18.9"
CANONICAL_WORKFLOW_TICKET_ID = "P18.9"
HUMAN_APPROVAL_NEXT_ACTION_ID = "APPROVE_P18_9_0"
CANONICAL_APPROVAL_ID = "P18.9.0"

_STORE_DIR = Path("agent-platform") / "pepper-ticket-architect-bridge"
_STORE_FILE = "P18.9.0.json"
_APPROVAL_DECISION_STORE_FILE = "P18.9.0.approval-decision.json"
_STORE_LOCK = threading.Lock()
_P17_ACCEPTED_CLOSURE_SHA256 = hashlib.sha256(
    b"pepper-p17-accepted-work-packet-execution-mvp-closure-reused-for-p18-9-0"
).hexdigest()

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
    "Kanban dispatch",
    "worker execution",
    "runtime execution",
)


class TicketArchitectBridgeError(ValueError):
    """Base error for P18.9.0 bridge failures."""


class TicketArchitectBridgeInputError(TicketArchitectBridgeError):
    """Raised when the requested project, ticket, or action is not eligible."""


class TicketArchitectBridgeConflict(TicketArchitectBridgeError):
    """Raised when persisted generated authority conflicts with P18.9.0."""


class TicketArchitectBridgeGenerationError(TicketArchitectBridgeError):
    """Raised when P16, P17, or P18 contract generation fails."""


def generation_record_path() -> Path:
    """Return the profile-scoped P18.9.0 generation authority path."""

    return get_hermes_home() / _STORE_DIR / _STORE_FILE


def approval_decision_record_path() -> Path:
    """Return the profile-scoped P18.9.0 human decision authority path."""

    return get_hermes_home() / _STORE_DIR / _APPROVAL_DECISION_STORE_FILE


def load_p18_9_0_generation_record() -> dict[str, Any] | None:
    """Load and validate the persisted P18.9.0 authority record, if present."""

    path = generation_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TicketArchitectBridgeConflict(
            "P18.9.0 generated authority record is unreadable"
        ) from exc
    return validate_p18_9_0_generation_record(record)


def load_p18_9_0_approval_decision_record(
    *,
    generation_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the persisted P18.9.0 human decision, if present."""

    path = approval_decision_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TicketArchitectBridgeConflict(
            "P18.9.0 approval decision record is unreadable"
        ) from exc
    return validate_p18_9_0_approval_decision_record(
        record,
        generation_record=generation_record,
    )


def validate_p18_9_0_generation_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate persisted bridge evidence without regenerating any contracts."""

    if not isinstance(record, dict):
        raise TicketArchitectBridgeConflict("generated authority record must be an object")
    if record.get("bridge_SHA256") != _record_digest(record):
        raise TicketArchitectBridgeConflict("generated authority record digest mismatch")
    _require_identity(record)

    try:
        project_spec = ProjectSpec.model_validate(record["project_spec"])
        ticket_spec = TicketSpec.model_validate(record["ticket_spec"])
        context_pack = ContextPack.model_validate(record["context_pack"])
        dependency_plan = TicketDependencyPlan.model_validate(record["dependency_plan"])
        lint_report = TicketLintReport.model_validate(record["lint_report"])
        TicketApprovalRecord.model_validate(record["ticket_approval_record"])
        TicketPublicationResult.model_validate(record["ticket_publication_result"])
        compilation = WorkPacketCompilationResult.model_validate(
            record["work_packet_compilation_result"]
        )
        transition = GovernedWorkflowTransitionResult.model_validate(
            record["workflow_transition_result"]
        )
    except (KeyError, ValueError) as exc:
        raise TicketArchitectBridgeConflict(
            "generated authority record contains invalid contract evidence"
        ) from exc

    if project_spec.project_id != CANONICAL_PROJECT_ID:
        raise TicketArchitectBridgeConflict("ProjectSpec must bind PEPPER")
    if ticket_spec.project_id != CANONICAL_PROJECT_ID:
        raise TicketArchitectBridgeConflict("TicketSpec must bind PEPPER")
    if ticket_spec.ticket_id != CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeConflict("TicketSpec must bind P18.9.0")
    if ticket_spec.title != CANONICAL_TICKET_TITLE:
        raise TicketArchitectBridgeConflict("TicketSpec title conflicts with roadmap")
    if context_pack.ticket_id != CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeConflict("ContextPack must bind P18.9.0")
    if dependency_plan.ticket_ids != (CANONICAL_TICKET_ID,):
        raise TicketArchitectBridgeConflict("dependency plan must contain only P18.9.0")
    if dependency_plan.blocked_ticket_ids:
        raise TicketArchitectBridgeConflict("P18.9.0 dependency plan must be unblocked")
    if lint_report.ticket_ids != (CANONICAL_TICKET_ID,):
        raise TicketArchitectBridgeConflict("lint report must bind P18.9.0")
    if lint_report.disposition is not TicketLintDisposition.PASS:
        raise TicketArchitectBridgeConflict("P18.9.0 lint report must pass")
    if compilation.work_packet.ticket_id != CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeConflict("WorkPacket must bind P18.9.0")
    if compilation.work_packet.execution_ready is not False:
        raise TicketArchitectBridgeConflict("WorkPacket must remain compile-only")
    if compilation.dependency_plan != dependency_plan:
        raise TicketArchitectBridgeConflict("WorkPacket must preserve dependency plan")
    if compilation.fresh_lint_report != lint_report:
        raise TicketArchitectBridgeConflict("WorkPacket must preserve lint report")
    if not transition.accepted:
        raise TicketArchitectBridgeConflict("workflow transition must be accepted")
    if transition.transition.transition_id != "GWT-002":
        raise TicketArchitectBridgeConflict("workflow transition must use GWT-002")
    if transition.resulting_snapshot.current_state is not GovernedWorkflowState.AWAITING_TICKET_APPROVAL:
        raise TicketArchitectBridgeConflict("workflow must stop at awaiting_ticket_approval")
    if transition.resulting_snapshot.pending_human_action != "ticket_approval":
        raise TicketArchitectBridgeConflict("workflow must require ticket approval")
    if record.get("WorkPacket_compilation_count") != 1:
        raise TicketArchitectBridgeConflict("WorkPacket compilation count must be one")
    for field_name in (
        "worker_execution",
        "Kanban_dispatch",
        "Git_mutation",
        "ticket_execution_authorized",
        "WorkPacket_execution_authorized",
        "runtime_execution_authorized",
    ):
        if record.get(field_name) is not False:
            raise TicketArchitectBridgeConflict(f"{field_name} must be false")
    return record


def validate_p18_9_0_approval_decision_record(
    record: dict[str, Any],
    *,
    generation_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate persisted human decision evidence without recompiling work."""

    if not isinstance(record, dict):
        raise TicketArchitectBridgeConflict("approval decision record must be an object")
    if record.get("approval_publication_SHA256") != _approval_decision_record_digest(record):
        raise TicketArchitectBridgeConflict("approval decision record digest mismatch")
    generation = (
        validate_p18_9_0_generation_record(generation_record)
        if generation_record is not None
        else load_p18_9_0_generation_record()
    )
    if generation is None:
        raise TicketArchitectBridgeConflict("approval decision has no generated authority")
    _require_approval_decision_identity(record, generation)

    decision = record.get("decision")
    try:
        approval_record = TicketApprovalRecord.model_validate(record["ticket_approval_record"])
        publication = (
            TicketPublicationResult.model_validate(record["ticket_publication_result"])
            if record.get("ticket_publication_result") is not None
            else None
        )
        transition = GovernedWorkflowTransitionResult.model_validate(
            record["workflow_transition_result"]
        )
    except (KeyError, ValueError) as exc:
        raise TicketArchitectBridgeConflict(
            "approval decision record contains invalid contract evidence"
        ) from exc

    if approval_record.project_id != CANONICAL_PROJECT_ID:
        raise TicketArchitectBridgeConflict("approval record must bind PEPPER")
    if approval_record.ticket_id != CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeConflict("approval record must bind P18.9.0")
    if approval_record.decision.value != decision:
        raise TicketArchitectBridgeConflict("approval record decision mismatch")
    if decision == HumanApprovalDecision.APPROVE.value:
        if record.get("status") != "approved":
            raise TicketArchitectBridgeConflict("approved decision status mismatch")
        if approval_record.approved_ticket is None or publication is None:
            raise TicketArchitectBridgeConflict("approved decision requires publication")
        if approval_record.approved_ticket != TicketSpec.model_validate(generation["ticket_spec"]):
            raise TicketArchitectBridgeConflict("approved ticket must preserve generated TicketSpec")
        if publication.publication.canonical_ticket != approval_record.approved_ticket:
            raise TicketArchitectBridgeConflict("publication must preserve approved TicketSpec")
        if transition.transition.transition_id != "GWT-003":
            raise TicketArchitectBridgeConflict("approved decision must use GWT-003")
        if transition.resulting_snapshot.current_state is not GovernedWorkflowState.TICKET_APPROVED:
            raise TicketArchitectBridgeConflict("approved decision must reach ticket_approved")
    elif decision == HumanApprovalDecision.REJECT.value:
        if record.get("status") != "rejected":
            raise TicketArchitectBridgeConflict("rejected decision status mismatch")
        if approval_record.approved_ticket is not None or publication is not None:
            raise TicketArchitectBridgeConflict("rejected decision must not publish")
        if transition.transition.transition_id != "GWT-025":
            raise TicketArchitectBridgeConflict("rejected decision must use GWT-025")
        if transition.resulting_snapshot.current_state is not GovernedWorkflowState.AWAITING_CORRECTION:
            raise TicketArchitectBridgeConflict("rejected decision must await correction")
    else:
        raise TicketArchitectBridgeConflict("approval decision must be approve or reject")

    if not transition.accepted:
        raise TicketArchitectBridgeConflict("approval workflow transition must be accepted")
    if transition.previous_snapshot_SHA256 != generation["workflow_transition_result"]["resulting_snapshot"]["workflow_SHA256"]:
        raise TicketArchitectBridgeConflict("approval transition must start from generated workflow")
    for field_name in (
        "ticket_execution_authorized",
        "WorkPacket_execution_authorized",
        "runtime_execution_authorized",
        "worker_execution",
        "Kanban_dispatch",
        "Git_mutation",
        "WorkPacket_recompile_required",
    ):
        if record.get(field_name) is not False:
            raise TicketArchitectBridgeConflict(f"{field_name} must be false")
    for field_name in (
        "provider_dispatch_count",
        "model_inference_count",
        "Git_commands_executed",
        "Docker_commands_executed",
        "Graphify_commands_executed",
    ):
        if record.get(field_name) != 0:
            raise TicketArchitectBridgeConflict(f"{field_name} must be zero")
    if record.get("WorkPacket_compilation_count") != 1:
        raise TicketArchitectBridgeConflict("WorkPacket compilation count must remain one")
    return record


def apply_p18_9_0_approval_decision(
    *,
    decision: str,
    actor: str,
    decided_at: float | None = None,
) -> dict[str, Any]:
    """Persist one explicit human approve/reject decision for generated P18.9.0."""

    if decision not in {HumanApprovalDecision.APPROVE.value, HumanApprovalDecision.REJECT.value}:
        raise TicketArchitectBridgeInputError("approval decision must be approve or reject")
    with _STORE_LOCK:
        generation = load_p18_9_0_generation_record()
        if generation is None:
            raise TicketArchitectBridgeConflict("P18.9.0 has no generated ticket to approve")
        existing = load_p18_9_0_approval_decision_record(generation_record=generation)
        if existing is not None:
            if existing.get("decision") == decision:
                return _approval_decision_operational_result(
                    existing,
                    idempotent_replay=True,
                )
            raise TicketArchitectBridgeConflict(
                "P18.9.0 ticket approval is already decided with the opposite decision"
            )
        record = _build_approval_decision_record(
            generation,
            decision=decision,
            actor=actor,
            decided_at=decided_at,
        )
        validate_p18_9_0_approval_decision_record(record, generation_record=generation)
        _persist_approval_decision_record(record)
    return _approval_decision_operational_result(record)


def generate_p18_9_0_ticket(
    *,
    workflow: dict[str, Any],
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    """Generate or replay the canonical P18.9.0 TicketSpec authority."""

    _validate_requested_identity(
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
    )
    with _STORE_LOCK:
        existing = load_p18_9_0_generation_record()
        if existing is not None:
            return _operational_result(existing, idempotent_replay=True)

        _validate_workflow_eligibility(workflow)
        try:
            record = _build_generation_record(workflow)
            validate_p18_9_0_generation_record(record)
            _persist_generation_record(record)
        except TicketArchitectBridgeError:
            raise
        except Exception as exc:
            raise TicketArchitectBridgeGenerationError(
                "P18.9.0 Ticket Architect bridge generation failed"
            ) from exc
    return _operational_result(record, idempotent_replay=False)


def generated_record_to_workflow_overlay(record: dict[str, Any]) -> dict[str, Any]:
    """Return workflow-control fields implied by a validated generated record."""

    validated = validate_p18_9_0_generation_record(record)
    decision = load_p18_9_0_approval_decision_record(generation_record=validated)
    if decision is not None:
        return _decided_record_to_workflow_overlay(validated, decision)
    return {
        "current_ticket_id": CANONICAL_TICKET_ID,
        "current_ticket_title": CANONICAL_TICKET_TITLE,
        "next_ticket_id": None,
        "next_ticket_title": None,
        "readiness": "awaiting_ticket_approval",
        "workflow_state": "P18.9.0-AWAITING-TICKET-APPROVAL",
        "workflow_status": "awaiting_ticket_approval",
        "approval_state": "pending_ticket_approval",
        "pending_ticket_approval_count": 1,
        "queue_state": "awaiting_human_ticket_approval",
        "validation_state": "ticket_generated_compile_only_not_executed",
        "review_state": "awaiting_human_ticket_approval",
        "recovery_state": "not_required",
        "git_handoff_state": "human_git_authority_preserved",
        "P18_9_ticket_generated": True,
        "P18_9_ticket_approved": False,
        "P18_9_work_packet_compiled": True,
        "generated_ticket_authority": _authority_projection(validated),
        "next_action": {
            "id": HUMAN_APPROVAL_NEXT_ACTION_ID,
            "label": (
                "Review and approve governed P18.9.0 Product Inventory, IA Decision, "
                "and Acceptance Contract before execution."
            ),
            "target_ticket_id": CANONICAL_TICKET_ID,
            "target_ticket_title": CANONICAL_TICKET_TITLE,
            "required_human_action": "ticket_approval",
        },
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
    }


def _decided_record_to_workflow_overlay(
    generation_record: dict[str, Any],
    decision_record: dict[str, Any],
) -> dict[str, Any]:
    approved = decision_record["decision"] == HumanApprovalDecision.APPROVE.value
    workflow_state = (
        "P18.9.0-TICKET-APPROVED" if approved else "P18.9.0-AWAITING-CORRECTION"
    )
    workflow_status = "ticket_approved" if approved else "awaiting_correction"
    next_action = (
        {
            "id": "P18_9_0_APPROVED_NO_EXECUTION",
            "label": (
                "Human ticket approval is recorded for P18.9.0; execution remains "
                "blocked until a separate governed action is authorized."
            ),
            "target_ticket_id": CANONICAL_TICKET_ID,
            "target_ticket_title": CANONICAL_TICKET_TITLE,
            "required_human_action": "governed_followup",
        }
        if approved
        else {
            "id": "REVISE_P18_9_0",
            "label": (
                "Human rejection is recorded for P18.9.0; correction is required "
                "before any downstream work."
            ),
            "target_ticket_id": CANONICAL_TICKET_ID,
            "target_ticket_title": CANONICAL_TICKET_TITLE,
            "required_human_action": "ticket_correction",
        }
    )
    return {
        "current_ticket_id": CANONICAL_TICKET_ID,
        "current_ticket_title": CANONICAL_TICKET_TITLE,
        "next_ticket_id": None,
        "next_ticket_title": None,
        "readiness": workflow_status,
        "workflow_state": workflow_state,
        "workflow_status": workflow_status,
        "approval_state": workflow_status,
        "pending_ticket_approval_count": 0,
        "queue_state": "ticket_approved_not_queued" if approved else "awaiting_ticket_correction",
        "validation_state": (
            "ticket_approved_compile_only_not_executed"
            if approved
            else "ticket_rejected_no_execution"
        ),
        "review_state": "human_ticket_approval_recorded" if approved else "human_ticket_rejection_recorded",
        "recovery_state": "not_required" if approved else "awaiting_correction",
        "git_handoff_state": "human_git_authority_preserved",
        "P18_9_ticket_generated": True,
        "P18_9_ticket_approved": approved,
        "P18_9_work_packet_compiled": True,
        "generated_ticket_authority": _authority_projection(generation_record),
        "ticket_approval_authority": _approval_decision_projection(decision_record),
        "next_action": next_action,
        "human_ticket_approval_present": True,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
    }


def _build_generation_record(workflow: dict[str, Any]) -> dict[str, Any]:
    project_spec = _build_project_spec()
    ticket_spec = _build_ticket_spec()
    context_pack = _assemble_context_pack(project_spec, ticket_spec)
    planning_request = TicketPlanningRequest(
        project_spec=project_spec,
        tickets=(ticket_spec,),
        external_dependency_resolutions=(),
        policy=ParallelPlanningPolicy(),
    )
    dependency_plan = build_ticket_dependency_plan(planning_request)
    _validate_dependency_plan(dependency_plan)
    lint_report = lint_ticket_collection(
        TicketLintRequest(
            project_spec=project_spec,
            tickets=(ticket_spec,),
            dependency_plan=dependency_plan,
            collection_complete=False,
        )
    )
    _validate_lint_report(lint_report)
    approval_record, publication_result, compilation_result = _compile_work_packet(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        lint_report=lint_report,
    )
    transition_result = _build_workflow_transition(compilation_result)
    observed_at = _utc_now_iso()
    record = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_ARCHITECT_BRIDGE_POLICY_ID,
        "created_at": observed_at,
        "source_next_action_id": CANONICAL_NEXT_ACTION_ID,
        "source_workflow_status": str(workflow.get("workflow_status") or ""),
        "generation_status": "awaiting_ticket_approval",
        "project_id": CANONICAL_PROJECT_ID,
        "project_name": CANONICAL_PROJECT_NAME,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "macroproject_title": CANONICAL_MACROPROJECT_TITLE,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "canonical_roadmap_authority": CANONICAL_ROADMAP_AUTHORITY,
        "idempotency_key": _idempotency_key(),
        "project_spec": project_spec.model_dump(mode="json"),
        "ticket_spec": ticket_spec.model_dump(mode="json"),
        "context_pack": context_pack.model_dump(mode="json"),
        "dependency_plan": dependency_plan.model_dump(mode="json"),
        "lint_report": lint_report.model_dump(mode="json"),
        "ticket_approval_record": approval_record.model_dump(mode="json"),
        "ticket_publication_result": publication_result.model_dump(mode="json"),
        "work_packet_compilation_result": compilation_result.model_dump(mode="json"),
        "workflow_transition_result": transition_result.model_dump(mode="json"),
        "ticket_spec_SHA256": compilation_result.evidence.source_ticket_SHA256,
        "dependency_plan_SHA256": dependency_plan.plan_SHA256,
        "lint_report_SHA256": lint_report.report_SHA256,
        "work_packet_id": compilation_result.work_packet.work_packet_id,
        "work_packet_SHA256": compilation_result.work_packet.work_packet_SHA256,
        "workflow_transition_result_SHA256": transition_result.result_SHA256,
        "human_ticket_approval_required": True,
        "human_ticket_approval_present": False,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "WorkPacket_compilation_count": 1,
    }
    record["bridge_SHA256"] = _record_digest(record)
    return record


def _build_project_spec() -> ProjectSpec:
    return ProjectSpec(
        project_id=CANONICAL_PROJECT_ID,
        title=CANONICAL_MACROPROJECT_TITLE,
        objective=(
            "Personalize Pepper's product experience from governed product inventory, "
            "information architecture, and explicit acceptance contracts."
        ),
        summary=(
            "P18.9 starts from the accepted P18 workflow migration and produces "
            "product personalization tickets through the governed P16/P17/P18 chain."
        ),
        context=(
            "P18 and P18.R are closed and P18.9 is the active governed macroproject.",
            "The human-approved P18.9 roadmap identifies P18.9.0 as the first item.",
            "P18.9.0 must define inventory, IA decisions, and acceptance contracts before execution.",
        ),
        authority_references=_authority_references(),
        scope=_scope(),
        constraints=(
            "Use the existing P16 TicketSpec, ContextPack, dependency plan, lint, approval, and publication contracts.",
            "Use the existing P17 WorkPacket compiler only in compile-only mode.",
            "Use the existing P18 governed workflow transition and stop at awaiting_ticket_approval.",
            "Provider dispatch, model inference, Kanban dispatch, worker execution, Docker, Graphify, and Git mutation are not authorized.",
        ),
        non_goals=(
            "Do not execute P18.9.0.",
            "Do not create a Kanban planning task or worker dispatch.",
            "Do not auto-approve the P18.9.0 ticket.",
            "Do not stage, commit, push, or otherwise mutate Git.",
        ),
        acceptance_criteria=(
            "P18.9.0 is represented as a canonical P16 TicketSpec with the approved title.",
            "A P17 WorkPacket is compiled exactly once and remains execution_ready=false.",
            "The governed workflow reaches awaiting_ticket_approval with human approval still required.",
        ),
        completion_verdict="p18_9_0_ticket_architect_bridge_ready",
    )


def _build_ticket_spec() -> TicketSpec:
    return TicketSpec(
        project_id=CANONICAL_PROJECT_ID,
        ticket_id=CANONICAL_TICKET_ID,
        title=CANONICAL_TICKET_TITLE,
        ticket_type=TicketType.ARCHITECTURE,
        objective=(
            "Inventory Pepper product surfaces, make the first information-architecture "
            "decision, and define the acceptance contract for P18.9 personalization."
        ),
        context=(
            "The active governed project is PEPPER, while P18.9 is the macroproject identifier.",
            "P18.9.0 is the first governed ticket after P18/P18.R closure.",
            "The stale Product UX / IA Baseline label is non-authoritative and must not override the approved roadmap title.",
            "Execution remains blocked until the generated ticket is explicitly approved by a human.",
        ),
        authority_references=_authority_references(),
        dependencies=(),
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=_scope(),
        constraints=(
            "Separate product identity PEPPER from repository and macroproject identifiers.",
            "Inventory and IA decisions must cite bounded repository or governance evidence.",
            "Acceptance criteria must be testable before any implementation ticket executes.",
            "Rollback posture: remove only the P18.9.0 inventory, IA, and acceptance-contract changes if superseded.",
            "No provider dispatch, model inference, Kanban dispatch, worker execution, Docker, Graphify, or Git mutation is authorized.",
        ),
        tasks=(
            "Inventory Pepper product surfaces relevant to product personalization and identify the authority for each surface.",
            "Decide the initial information architecture boundary for P18.9 personalization work.",
            "Define acceptance criteria for the product inventory, IA decision, and downstream implementation handoff.",
            "Record unresolved product questions without dispatching workers or creating Kanban tasks.",
        ),
        acceptance_criteria=(
            "The product inventory distinguishes current product runtime, dashboard, repository-context, and workflow-control surfaces.",
            "The IA decision names the first personalization boundary and the evidence that supports it.",
            "The acceptance contract states what must be true before any downstream P18.9 implementation ticket executes.",
            "The result explicitly reports no worker execution, no Kanban dispatch, no Docker, no Graphify, and no Git mutation.",
        ),
        validation_steps=(
            TicketValidationStepSpec(
                validation_id="V1",
                description="Human review confirms P18.9.0 inventory, IA decision, and acceptance contract are present.",
                command=None,
                expected_result=(
                    "The reviewer can identify the inventory, IA decision, acceptance contract, "
                    "and preserved execution boundary in the P18.9.0 result."
                ),
            ),
        ),
        response_contract=TicketResponseContractSpec(
            required_sections=_REQUIRED_RESPONSE_SECTIONS,
            completion_verdict="p18_9_0_inventory_ia_acceptance_contract_ready",
        ),
        recommended_commit_message="P18.9.0 Define product inventory IA acceptance contract",
    )


def _scope() -> RepositoryScopeSpec:
    return RepositoryScopeSpec(
        allowed_paths=(
            "0_architecture/**",
            "2_products/pepper-agent/docs/**",
            "2_products/pepper-agent/hermes_cli/agent_platform/**",
            "2_products/pepper-agent/tools/pepper_workflow_tools.py",
            "2_products/pepper-agent/toolsets.py",
            "2_products/pepper-agent/tests/hermes_cli/**",
            "2_products/pepper-agent/web/src/agent-platform/**",
            "2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv",
            "2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv",
        ),
        forbidden_paths=(
            ".git/**",
            ".opencode/**",
            "graphify-out/**",
            "4_external/sources/**",
            "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
        ),
        allowed_actions=(
            "inspect bounded Pepper product runtime, dashboard, repository-context, and workflow-control evidence",
            "document product inventory and information architecture decisions",
            "define acceptance contracts and unresolved product questions",
            "add focused non-executing tests for the P18.9.0 contract if needed",
        ),
        forbidden_actions=_REQUIRED_FORBIDDEN_ACTIONS,
    )


def _authority_references() -> tuple[AuthorityReferenceSpec, ...]:
    return (
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.EXTERNAL_SOURCE,
            value=CANONICAL_ROADMAP_AUTHORITY,
            rationale="Human instruction identifies the approved P18.9.0 roadmap title.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.TICKET,
            value="P18.8",
            rationale="Accepted controlled default-mode cutover is historical prerequisite evidence.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.TICKET,
            value="P18.R",
            rationale="Accepted workflow migration closure authorizes the P18.9 handoff.",
        ),
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.GOVERNANCE_RECORD,
            value="HUMAN_P18_8_CUTOVER_SMOKE_PASS",
            rationale="Human smoke evidence confirms default-mode control before P18.9.",
        ),
    )


def _assemble_context_pack(project_spec: ProjectSpec, ticket_spec: TicketSpec) -> ContextPack:
    sources = (
        ContextSourceSpec(
            source_id="CTX-P18-9-ROADMAP",
            kind=ContextSourceKind.HUMAN_INSTRUCTION,
            title="Human-approved P18.9.0 roadmap item",
            source_reference=CANONICAL_ROADMAP_AUTHORITY,
            content=(
                "P18.9.0 is Product Inventory, IA Decision, and Acceptance Contract. "
                "This title supersedes stale Product UX / IA Baseline labels."
            ),
            authority_references=(_authority_references()[0],),
            sensitivity=ContextSensitivity.INTERNAL,
            priority=ContextPriority.CRITICAL,
            required=True,
        ),
        ContextSourceSpec(
            source_id="CTX-P18-8-SMOKE",
            kind=ContextSourceKind.GOVERNANCE_RECORD,
            title="P18.8 controlled default-mode smoke",
            source_reference="HUMAN_P18_8_CUTOVER_SMOKE_PASS",
            content="P18.8 controlled default-mode human smoke passed before P18.9 intake.",
            authority_references=(_authority_references()[1], _authority_references()[3]),
            sensitivity=ContextSensitivity.INTERNAL,
            priority=ContextPriority.HIGH,
            required=True,
        ),
        ContextSourceSpec(
            source_id="CTX-P18R-CLOSURE",
            kind=ContextSourceKind.GOVERNANCE_RECORD,
            title="P18.R workflow migration closure",
            source_reference="P18.R accepted closure",
            content=(
                "P18.R is accepted and closed; P18.9 is the next governed "
                "Pepper Product Personalization macroproject."
            ),
            authority_references=(_authority_references()[2],),
            sensitivity=ContextSensitivity.INTERNAL,
            priority=ContextPriority.HIGH,
            required=True,
        ),
    )
    return assemble_context_pack(
        ContextAssemblyRequest(
            project_spec=project_spec,
            ticket_spec=ticket_spec,
            sources=sources,
            policy=ContextAssemblyPolicy(max_items=8, max_total_characters=32768),
        )
    )


def _validate_dependency_plan(plan: TicketDependencyPlan) -> None:
    if plan.project_id != CANONICAL_PROJECT_ID:
        raise TicketArchitectBridgeGenerationError("dependency plan must bind PEPPER")
    if plan.ticket_ids != (CANONICAL_TICKET_ID,):
        raise TicketArchitectBridgeGenerationError("dependency plan must contain P18.9.0")
    if plan.blocked_ticket_ids:
        raise TicketArchitectBridgeGenerationError("P18.9.0 dependency plan is blocked")
    if len(plan.waves) != 1 or plan.waves[0].disposition.value != "dependency_ready":
        raise TicketArchitectBridgeGenerationError("P18.9.0 dependency plan must be dependency-ready")


def _validate_lint_report(report: TicketLintReport) -> None:
    if report.project_id != CANONICAL_PROJECT_ID:
        raise TicketArchitectBridgeGenerationError("lint report must bind PEPPER")
    if report.ticket_ids != (CANONICAL_TICKET_ID,):
        raise TicketArchitectBridgeGenerationError("lint report must contain P18.9.0")
    if report.disposition is not TicketLintDisposition.PASS:
        raise TicketArchitectBridgeGenerationError("P18.9.0 TicketSpec lint must pass")


def _compile_work_packet(
    *,
    project_spec: ProjectSpec,
    ticket_spec: TicketSpec,
    context_pack: ContextPack,
    planning_request: TicketPlanningRequest,
    dependency_plan: TicketDependencyPlan,
    lint_report: TicketLintReport,
) -> tuple[TicketApprovalRecord, TicketPublicationResult, WorkPacketCompilationResult]:
    generation_request = TicketGenerationRequest(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.GOVERNANCE),
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    proposals = tuple(
        build_ticket_proposal(
            assignment=assignment,
            proposed_ticket=ticket_spec,
            rationale=(
                "P18.9.0 TicketSpec is generated deterministically from the approved "
                "P18.9 roadmap item and bounded Pepper workflow evidence."
            ),
            evidence_source_ids=tuple(item.source_id for item in context_pack.items),
            assumptions=(),
            risks=("Execution remains unauthorized until human ticket approval.",),
            unresolved_questions=(),
        )
        for assignment in assignments
    )
    reviewed = tuple(ReviewedTicketProposal(proposal=item, lint_report=lint_report) for item in proposals)
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
        evidence_reference="P18.9.0 dependency plan before compile-only WorkPacket creation.",
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
                decision_reference="P18.9.0 compile-only TicketSpec acceptance evidence.",
                rationale=(
                    "Accept deterministic P16 TicketSpec for compile-only P17 WorkPacket "
                    "creation; P18 human ticket approval remains pending."
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
                publication_reference="P18.9.0 compile-only canonical TicketSpec publication.",
                rationale=(
                    "Logical P16 publication is required by the existing P17 compiler "
                    "and grants no P18 execution authority."
                ),
            ),
            prior_publication=None,
            supersession_rationale=None,
        )
    )
    authorization = build_work_packet_compilation_authorization(
        authorizer_id="pepper-governed-runtime",
        authorization_reference="P18.9.0 deterministic compile-only authorization.",
        rationale=(
            "Invoke the accepted P17 compiler once to create a compile-only WorkPacket "
            "while preserving zero execution authority."
        ),
        approval_record=approval_record,
        publication_result=publication_result,
        risk_acknowledgement=None,
    )
    compilation = compile_ticket_spec_to_work_packet(
        WorkPacketCompilationRequest(
            project_spec=project_spec,
            approval_record=approval_record,
            publication_result=publication_result,
            compilation_authorization=authorization,
        )
    )
    return approval_record, publication_result, compilation


def _build_workflow_transition(
    compilation_result: WorkPacketCompilationResult,
) -> GovernedWorkflowTransitionResult:
    p17_binding = gsm._make_model(
        gsm.P17WorkflowBinding,
        "binding_SHA256",
        gsm.WORKFLOW_P17_BINDING_DIGEST_ALGORITHM,
        P17_closure_id="P17.R",
        P17_closure_SHA256=_P17_ACCEPTED_CLOSURE_SHA256,
        WorkPacket_execution_MVP_available=True,
        human_Git_authority_required=True,
        non_critical_scope=True,
        production_readiness_claimed=False,
    )
    identity = build_governed_workflow_identity(
        project_id=CANONICAL_WORKFLOW_PROJECT_ID,
        ticket_id=CANONICAL_WORKFLOW_TICKET_ID,
        ticket_revision=1,
        work_packet_id=compilation_result.work_packet.work_packet_id,
        work_packet_SHA256=compilation_result.work_packet.work_packet_SHA256,
    )
    initial_projection = build_hermes_workflow_projection(
        runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
        runtime_state="pepper:intake_ready",
        task_id=None,
        board_or_queue_id=None,
        worker_id_present=False,
        workspace_binding_present=False,
        dependency_blocked=False,
        retry_state_present=False,
        reclaim_state_present=False,
    )
    current_snapshot = build_initial_governed_workflow_snapshot(
        identity=identity,
        P17_binding=p17_binding,
        runtime_projection=initial_projection,
        current_state=GovernedWorkflowState.INTAKE_READY,
    )
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=current_snapshot,
        trigger=WorkflowTransitionTrigger.TICKET_GENERATED,
        authority=WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        evidence_refs=("ticket_factory_candidate", CANONICAL_TICKET_ID),
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
        raise TicketArchitectBridgeGenerationError("P18 GWT-002 transition rejected")
    return transition_result


def _build_approval_decision_record(
    generation: dict[str, Any],
    *,
    decision: str,
    actor: str,
    decided_at: float | None,
) -> dict[str, Any]:
    project_spec = ProjectSpec.model_validate(generation["project_spec"])
    ticket_spec = TicketSpec.model_validate(generation["ticket_spec"])
    reviewer_id = _reviewer_id_from_actor(actor)
    approval_decision = HumanApprovalDecision(decision)
    approval_record = build_ticket_approval_record(
        TicketApprovalRequest(
            project_spec=project_spec,
            seed_ticket=ticket_spec,
            synthesis_review=_rebuild_synthesis_review_for_record(generation),
            decision=approval_decision,
            conflict_resolutions=(),
            approval_evidence=HumanApprovalEvidence(
                reviewer_id=reviewer_id,
                decision_reference=f"P18.9.0 human ticket decision by {reviewer_id}.",
                rationale=(
                    "Record the explicit human ticket decision for the existing "
                    "generated P18.9.0 TicketSpec without granting execution authority."
                ),
            ),
            manual_replacement=None,
            fresh_planning_evidence=(
                _fresh_planning_evidence_for_record(generation)
                if approval_decision is HumanApprovalDecision.APPROVE
                else None
            ),
        )
    )
    publication_result = (
        publish_canonical_ticket(
            TicketPublicationRequest(
                approval_record=approval_record,
                publication_evidence=TicketPublicationEvidence(
                    publisher_id=reviewer_id,
                    publication_reference="P18.9.0 human-approved canonical TicketSpec publication.",
                    rationale=(
                        "Logical publication records the human-approved P18.9.0 "
                        "TicketSpec and grants no execution authority."
                    ),
                ),
                prior_publication=None,
                supersession_rationale=None,
            )
        )
        if approval_decision is HumanApprovalDecision.APPROVE
        else None
    )
    workflow_transition = _build_approval_transition(generation, approval_decision)
    decided_at_value = float(decided_at) if decided_at is not None else datetime.now(timezone.utc).timestamp()
    record = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_APPROVAL_PUBLICATION_POLICY_ID,
        "approval_id": CANONICAL_APPROVAL_ID,
        "created_at": _utc_from_timestamp(decided_at_value),
        "decided_at": decided_at_value,
        "actor": str(actor or "pepper-dashboard-human").strip() or "pepper-dashboard-human",
        "reviewer_id": reviewer_id,
        "decision": approval_decision.value,
        "status": "approved" if approval_decision is HumanApprovalDecision.APPROVE else "rejected",
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "bridge_SHA256": generation["bridge_SHA256"],
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "generated_workflow_transition_result_SHA256": generation[
            "workflow_transition_result_SHA256"
        ],
        "ticket_approval_record": approval_record.model_dump(mode="json"),
        "ticket_publication_result": (
            publication_result.model_dump(mode="json")
            if publication_result is not None
            else None
        ),
        "workflow_transition_result": workflow_transition.model_dump(mode="json"),
        "workflow_transition_result_SHA256": workflow_transition.result_SHA256,
        "human_ticket_approval_required": True,
        "human_ticket_approval_present": True,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "WorkPacket_compilation_count": 1,
        "WorkPacket_recompile_required": False,
    }
    record["approval_publication_SHA256"] = _approval_decision_record_digest(record)
    return record


def _rebuild_synthesis_review_for_record(generation: dict[str, Any]):
    project_spec = ProjectSpec.model_validate(generation["project_spec"])
    ticket_spec = TicketSpec.model_validate(generation["ticket_spec"])
    context_pack = ContextPack.model_validate(generation["context_pack"])
    lint_report = TicketLintReport.model_validate(generation["lint_report"])
    dependency_plan = TicketDependencyPlan.model_validate(generation["dependency_plan"])
    generation_request = TicketGenerationRequest(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        roles=(TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.GOVERNANCE),
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    proposals = tuple(
        build_ticket_proposal(
            assignment=assignment,
            proposed_ticket=ticket_spec,
            rationale=(
                "P18.9.0 TicketSpec is generated deterministically from the approved "
                "P18.9 roadmap item and bounded Pepper workflow evidence."
            ),
            evidence_source_ids=tuple(item.source_id for item in context_pack.items),
            assumptions=(),
            risks=("Execution remains unauthorized until human ticket approval.",),
            unresolved_questions=(),
        )
        for assignment in assignments
    )
    reviewed = tuple(
        ReviewedTicketProposal(proposal=proposal, lint_report=lint_report)
        for proposal in proposals
    )
    return build_ticket_synthesis_review(
        TicketSynthesisRequest(
            generation_request=generation_request,
            assignments=assignments,
            reviewed_proposals=reviewed,
            dependency_plan=dependency_plan,
        )
    )


def _fresh_planning_evidence_for_record(generation: dict[str, Any]) -> FreshDependencyPlanningEvidence:
    project_spec = ProjectSpec.model_validate(generation["project_spec"])
    ticket_spec = TicketSpec.model_validate(generation["ticket_spec"])
    dependency_plan = TicketDependencyPlan.model_validate(generation["dependency_plan"])
    planning_request = TicketPlanningRequest(
        project_spec=project_spec,
        tickets=(ticket_spec,),
        external_dependency_resolutions=(),
        policy=ParallelPlanningPolicy(),
    )
    if build_ticket_dependency_plan(planning_request) != dependency_plan:
        raise TicketArchitectBridgeConflict("P18.9.0 dependency plan cannot be recomputed")
    return FreshDependencyPlanningEvidence(
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        evidence_reference="P18.9.0 approval validates generated dependency evidence.",
        rationale="Human ticket approval preserves the dependency plan bound by generation.",
    )


def _build_approval_transition(
    generation: dict[str, Any],
    decision: HumanApprovalDecision,
) -> GovernedWorkflowTransitionResult:
    generated_transition = GovernedWorkflowTransitionResult.model_validate(
        generation["workflow_transition_result"]
    )
    approval_granted = decision is HumanApprovalDecision.APPROVE
    transition_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=generated_transition.resulting_snapshot,
        trigger=(
            WorkflowTransitionTrigger.TICKET_APPROVED
            if approval_granted
            else WorkflowTransitionTrigger.HUMAN_REJECTED
        ),
        authority=WorkflowTransitionAuthority.HUMAN,
        evidence_refs=("human_ticket_approval",) if approval_granted else ("human_ticket_rejection",),
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.GOVERNANCE_ONLY,
            runtime_state=(
                "pepper:p18_9_0_ticket_approved"
                if approval_granted
                else "pepper:p18_9_0_awaiting_correction"
            ),
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
        raise TicketArchitectBridgeConflict("P18.9.0 approval transition rejected")
    return transition_result


def _validate_requested_identity(
    *,
    requested_project_id: str | None,
    requested_ticket_id: str | None,
    requested_next_action_id: str | None,
) -> None:
    if requested_project_id not in {None, "", CANONICAL_PROJECT_ID}:
        raise TicketArchitectBridgeInputError("requested project is not PEPPER")
    if requested_ticket_id not in {None, "", CANONICAL_TICKET_ID}:
        raise TicketArchitectBridgeInputError("requested ticket is not P18.9.0")
    if requested_next_action_id not in {None, "", CANONICAL_NEXT_ACTION_ID}:
        raise TicketArchitectBridgeInputError("requested next action is not GENERATE_P18_9_0")


def _validate_workflow_eligibility(workflow: dict[str, Any]) -> None:
    if not isinstance(workflow, dict):
        raise TicketArchitectBridgeInputError("workflow state is unavailable")
    if workflow.get("project_id") != CANONICAL_PROJECT_ID:
        raise TicketArchitectBridgeInputError("active governed project is not PEPPER")
    if workflow.get("macroproject_id") != CANONICAL_MACROPROJECT_ID:
        raise TicketArchitectBridgeInputError("active macroproject is not P18.9")
    if workflow.get("current_ticket_id") not in {None, ""}:
        raise TicketArchitectBridgeInputError("P18.9.0 generation requires no active ticket")
    if workflow.get("P18_9_ready") is not True:
        raise TicketArchitectBridgeInputError("P18.9 roadmap is not intake-ready")
    if workflow.get("P18_9_ticket_generated") is True:
        raise TicketArchitectBridgeConflict("workflow says P18.9.0 is generated but no authority record exists")
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        raise TicketArchitectBridgeInputError("next action is unavailable")
    if next_action.get("id") != CANONICAL_NEXT_ACTION_ID:
        raise TicketArchitectBridgeInputError("next action is not GENERATE_P18_9_0")
    if next_action.get("target_ticket_id") != CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeInputError("next action does not target P18.9.0")
    if workflow.get("workflow_status") not in {"planning_approved_or_intake_ready", "intake_ready"}:
        raise TicketArchitectBridgeInputError("workflow is not intake-ready for P18.9.0 generation")


def _persist_generation_record(record: dict[str, Any]) -> None:
    path = generation_record_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = load_p18_9_0_generation_record()
        if existing is not None:
            return
    tmp = path.with_suffix(path.suffix + ".tmp")
    serialized = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(path)


def _persist_approval_decision_record(record: dict[str, Any]) -> None:
    path = approval_decision_record_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = load_p18_9_0_approval_decision_record()
        if existing is not None:
            return
    tmp = path.with_suffix(path.suffix + ".tmp")
    serialized = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(path)


def _operational_result(record: dict[str, Any], *, idempotent_replay: bool) -> dict[str, Any]:
    authority = _authority_projection(record)
    return {
        "source_system": "pepper-ticket-architect-bridge",
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_ARCHITECT_BRIDGE_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "generation_status": "awaiting_ticket_approval",
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "canonical_roadmap_authority": CANONICAL_ROADMAP_AUTHORITY,
        "workflow_status": "awaiting_ticket_approval",
        "workflow_transition_id": "GWT-002",
        "human_ticket_approval_required": True,
        "human_ticket_approval_present": False,
        "execution_ready": False,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "WorkPacket_compilation_count": 1,
        "authority": authority,
        "next_action": {
            "id": HUMAN_APPROVAL_NEXT_ACTION_ID,
            "label": "Human ticket approval required before P18.9.0 execution.",
            "target_ticket_id": CANONICAL_TICKET_ID,
            "required_human_action": "ticket_approval",
        },
    }


def _approval_decision_operational_result(
    record: dict[str, Any],
    *,
    idempotent_replay: bool = False,
) -> dict[str, Any]:
    return {
        "source_system": "pepper-ticket-architect-bridge",
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_APPROVAL_PUBLICATION_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "approval_id": CANONICAL_APPROVAL_ID,
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "decision": record["decision"],
        "status": record["status"],
        "actor": record["actor"],
        "decided_at": record["decided_at"],
        "workflow_transition_id": record["workflow_transition_result"]["transition"]["transition_id"],
        "human_ticket_approval_present": True,
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "WorkPacket_compilation_count": 1,
        "WorkPacket_recompile_required": False,
        "authority": _approval_decision_projection(record),
    }


def _authority_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_record": str(_STORE_DIR / _STORE_FILE).replace("\\", "/"),
        "bridge_SHA256": record["bridge_SHA256"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "dependency_plan_SHA256": record["dependency_plan_SHA256"],
        "lint_report_SHA256": record["lint_report_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "workflow_transition_result_SHA256": record["workflow_transition_result_SHA256"],
    }


def _approval_decision_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_record": str(_STORE_DIR / _APPROVAL_DECISION_STORE_FILE).replace("\\", "/"),
        "approval_id": record["approval_id"],
        "approval_publication_SHA256": record["approval_publication_SHA256"],
        "decision": record["decision"],
        "status": record["status"],
        "ticket_approval_record_SHA256": record["ticket_approval_record"]["approval_SHA256"],
        "ticket_publication_result_SHA256": (
            record["ticket_publication_result"]["result_SHA256"]
            if record.get("ticket_publication_result") is not None
            else None
        ),
        "workflow_transition_result_SHA256": record["workflow_transition_result_SHA256"],
    }


def _require_identity(record: dict[str, Any]) -> None:
    expected = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_ARCHITECT_BRIDGE_POLICY_ID,
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "canonical_roadmap_authority": CANONICAL_ROADMAP_AUTHORITY,
        "idempotency_key": _idempotency_key(),
        "generation_status": "awaiting_ticket_approval",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise TicketArchitectBridgeConflict(f"generated authority {key} mismatch")


def _require_approval_decision_identity(
    record: dict[str, Any],
    generation: dict[str, Any],
) -> None:
    expected = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_APPROVAL_PUBLICATION_POLICY_ID,
        "approval_id": CANONICAL_APPROVAL_ID,
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "bridge_SHA256": generation["bridge_SHA256"],
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "generated_workflow_transition_result_SHA256": generation[
            "workflow_transition_result_SHA256"
        ],
        "human_ticket_approval_required": True,
        "human_ticket_approval_present": True,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise TicketArchitectBridgeConflict(f"approval decision {key} mismatch")


def _record_digest(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "bridge_SHA256"}
    encoded = json.dumps(
        {"algorithm": TICKET_ARCHITECT_BRIDGE_DIGEST_ALGORITHM, "record": _normalize(payload)},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _approval_decision_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "approval_publication_SHA256"
    }
    encoded = json.dumps(
        {
            "algorithm": TICKET_APPROVAL_PUBLICATION_DIGEST_ALGORITHM,
            "record": _normalize(payload),
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalize(value: object) -> object:
    if isinstance(value, BaseModel):
        return _normalize(value.model_dump(mode="json", warnings=False))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple | list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    return value


def _idempotency_key() -> str:
    return f"{CANONICAL_PROJECT_ID}:{CANONICAL_MACROPROJECT_ID}:{CANONICAL_TICKET_ID}:{CANONICAL_NEXT_ACTION_ID}"


def _reviewer_id_from_actor(actor: str) -> str:
    raw = str(actor or "pepper-dashboard-human").strip() or "pepper-dashboard-human"
    candidate = re.sub(r"[^A-Za-z0-9._:@+-]+", "-", raw).strip(".-_:@+")
    if not candidate or not candidate[0].isalnum() or len(candidate) < 3:
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
        candidate = f"human-{digest}"
    return candidate[:96]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _utc_from_timestamp(value: float) -> str:
    return datetime.fromtimestamp(value, timezone.utc).isoformat().replace("+00:00", "Z")


__all__ = (
    "TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION",
    "TICKET_ARCHITECT_BRIDGE_POLICY_ID",
    "TICKET_APPROVAL_PUBLICATION_POLICY_ID",
    "CANONICAL_PROJECT_ID",
    "CANONICAL_MACROPROJECT_ID",
    "CANONICAL_TICKET_ID",
    "CANONICAL_TICKET_TITLE",
    "CANONICAL_NEXT_ACTION_ID",
    "CANONICAL_APPROVAL_ID",
    "TicketArchitectBridgeError",
    "TicketArchitectBridgeInputError",
    "TicketArchitectBridgeConflict",
    "TicketArchitectBridgeGenerationError",
    "generation_record_path",
    "approval_decision_record_path",
    "load_p18_9_0_generation_record",
    "load_p18_9_0_approval_decision_record",
    "validate_p18_9_0_generation_record",
    "validate_p18_9_0_approval_decision_record",
    "generate_p18_9_0_ticket",
    "generated_record_to_workflow_overlay",
    "apply_p18_9_0_approval_decision",
)
