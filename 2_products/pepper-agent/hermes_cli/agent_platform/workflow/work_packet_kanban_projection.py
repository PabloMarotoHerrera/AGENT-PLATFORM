"""Approved Pepper WorkPacket to Hermes Kanban projection.

This bridge treats Hermes Kanban as a provisional execution substrate and keeps
P16/P17/P18 as the canonical Pepper authority. It creates no dispatcher run,
worker process, workspace, command execution, Git mutation, Docker invocation,
Graphify invocation, retry, rollback, or Paperclip migration.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
import threading
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from hermes_constants import get_hermes_home
from hermes_cli import kanban_db
from hermes_cli.agent_platform.ticket_factory import TicketDependencyPlan
from hermes_cli.agent_platform.workflow.dependency_execution_queue import (
    DEPENDENCY_AWARE_QUEUE_POLICY_ID,
    DependencyAwareQueueDecision,
    derive_dependency_queue_admission_for_ticket,
)
from hermes_cli.agent_platform.workflow.governed_state_machine import (
    GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
    GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
    GovernedWorkflowTransitionRequest,
    GovernedWorkflowTransitionResult,
    HermesWorkflowRuntimeKind,
    WorkflowTransitionAuthority,
    WorkflowTransitionTrigger,
    build_governed_workflow_transition,
    build_hermes_workflow_projection,
    validate_governed_workflow_transition_request,
)
from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
    CANONICAL_PROJECT_ID,
    CANONICAL_TICKET_ID,
    TicketArchitectBridgeError,
    approved_no_execution_action_id,
    load_approval_decision_record,
    load_generation_record,
    validate_historical_approved_predecessor_approval_decision_record,
    validate_historical_approved_predecessor_generation_record,
    validate_approval_decision_record,
    validate_generation_record,
)
from hermes_cli.profiles import list_profiles, normalize_profile_name


WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION = 1
WORK_PACKET_KANBAN_PROJECTION_POLICY_ID = "pepper-workpacket-kanban-projection-v1"
PEPPER_EXECUTION_PROFILES_SCHEMA_VERSION = 1
PEPPER_EXECUTION_PROFILES_POLICY_ID = "pepper-execution-profiles-v1"
PEPPER_EXECUTION_PROFILES_POLICY_REVISION = "01U"
WORK_PACKET_KANBAN_PROJECTION_DIGEST_ALGORITHM = (
    "agent-platform-workpacket-kanban-projection-sha256-v1"
)

_STORE_LOCK = threading.Lock()
_STORE_DIR = Path("agent-platform") / "pepper-workpacket-kanban-projection"
_STORE_FILE = "P18.9.0.kanban-projection.json"
_KANBAN_BOARD = "default"
_WORKSPACE_KIND = "scratch"
_TASK_SKILLS: tuple[str, ...] = ()
_LEGACY_SEMANTIC_TASK_SKILLS = ("codebase-inspection",)
_TASK_MAX_RETRIES = 1
_MAX_CONCURRENT_WORKERS_FOR_TICKET = 1
_PROFILE_TEXT_TOKEN = re.compile(r"[a-z0-9]+")
_PEPPER_EXECUTION_PROFILE_ROLE = "architecture_product"
_PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE = "implementation_product"
_PEPPER_LEAD_AGENT_ROLE = "lead_agent"
_PEPPER_TICKET_ARCHITECT_ROLE = "ticket_architect"
_PEPPER_DEFAULT_PROFILE_ROLE = "default_control_profile"
_PEPPER_UNCLASSIFIED_PROFILE_ROLE = "unclassified"
_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS = ("pepper_repository",)
_PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_TOOLSETS = (
    "pepper_repository",
    "file",
)
_PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_WRITE_TOOLSETS = ("file",)
_PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS = ("no_mcp",)
_PEPPER_SEMANTIC_CAPABILITIES = ("codebase-inspection",)
_PEPPER_IMPLEMENTATION_SEMANTIC_CAPABILITIES = (
    "codebase-inspection",
    "codebase-edit",
)
_PEPPER_CAPABILITY_RESOLUTION_POLICY = "semantic_capability_to_profile_toolset"
_PEPPER_CAPABILITY_RESOLUTION = (
    {
        "semantic_capability": "codebase-inspection",
        "resolved_surface": "profile_toolset",
        "toolset": "pepper_repository",
        "hermes_task_skill": None,
    },
)
_PEPPER_IMPLEMENTATION_CAPABILITY_RESOLUTION = (
    *_PEPPER_CAPABILITY_RESOLUTION,
    {
        "semantic_capability": "codebase-edit",
        "resolved_surface": "profile_toolset",
        "toolset": "file",
        "hermes_task_skill": None,
    },
)
_PEPPER_REQUIRED_CAPABILITY_LABELS = (
    "codebase-inspection",
    "governed repository read",
    "architecture and product analysis",
    "Ticket/IA documentation authority",
)
_PEPPER_IMPLEMENTATION_REQUIRED_CAPABILITY_LABELS = (
    "codebase-inspection",
    "governed repository read",
    "bounded file write/patch authority",
    "product implementation authority",
)
PEPPER_EXECUTION_PROFILE_TAXONOMY = {
    _PEPPER_LEAD_AGENT_ROLE: {
        "worker_assignable": False,
        "authority": "conversational_control_surface",
    },
    _PEPPER_TICKET_ARCHITECT_ROLE: {
        "worker_assignable": False,
        "authority": "ticket_and_workpacket_authority",
    },
    _PEPPER_EXECUTION_PROFILE_ROLE: {
        "worker_assignable": True,
        "authority": "bounded_product_architecture_execution_profile",
        "required_toolsets": _PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS,
        "required_sentinels": _PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS,
    },
    _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE: {
        "worker_assignable": True,
        "authority": "bounded_product_implementation_execution_profile",
        "required_toolsets": _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_TOOLSETS,
        "required_write_toolsets": _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_WRITE_TOOLSETS,
        "required_sentinels": _PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS,
    },
}
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class WorkPacketKanbanProjectionError(ValueError):
    """Base error for WorkPacket/Kanban projection failures."""


class WorkPacketKanbanProjectionInputError(WorkPacketKanbanProjectionError):
    """Raised when caller-supplied projection guards are malformed."""


class WorkPacketKanbanProjectionConflict(WorkPacketKanbanProjectionError):
    """Raised when existing projection authority or task mapping conflicts."""


class WorkPacketKanbanProjectionProfileGap(WorkPacketKanbanProjectionError):
    """Raised when no existing Hermes profile can own the projected task."""

    def __init__(
        self,
        blocker_code: str = "PROFILE_ASSIGNMENT_GAP",
        *,
        diagnostics: dict[str, Any] | None = None,
    ) -> None:
        self.blocker_code = blocker_code
        self.diagnostics = diagnostics or {}
        super().__init__(blocker_code)


class WorkPacketKanbanProjectionProfileSelectionRequired(
    WorkPacketKanbanProjectionProfileGap
):
    """Raised when multiple governed execution profiles could own the task."""


class WorkPacketKanbanProjectionBlocked(WorkPacketKanbanProjectionError):
    """Raised when dependency admission blocks projection."""


def _safe_ticket_id(value: object) -> str:
    ticket_id = str(value or "").strip()
    if not _SAFE_ID.fullmatch(ticket_id):
        raise WorkPacketKanbanProjectionInputError("ticket id is invalid")
    return ticket_id


def _ticket_action_token(ticket_id: str) -> str:
    return _safe_ticket_id(ticket_id).replace(".", "_").replace("-", "_").upper()


def execution_start_action_id(ticket_id: str) -> str:
    return f"START_{_ticket_action_token(ticket_id)}_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"


def kanban_projection_record_path() -> Path:
    """Return the profile-scoped P18.9.0 Kanban projection authority path."""

    return get_hermes_home() / _STORE_DIR / _STORE_FILE


def kanban_projection_record_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped Kanban projection authority path for one ticket."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    if safe_ticket_id == CANONICAL_TICKET_ID:
        return kanban_projection_record_path()
    return get_hermes_home() / _STORE_DIR / f"{safe_ticket_id}.json"


def load_p18_9_0_kanban_projection_record(
    *,
    generation_record: dict[str, Any] | None = None,
    decision_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the persisted P18.9.0 Kanban projection, if present."""

    return load_kanban_projection_record(
        ticket_id=CANONICAL_TICKET_ID,
        generation_record=generation_record,
        decision_record=decision_record,
    )


def load_kanban_projection_record(
    *,
    ticket_id: str,
    generation_record: dict[str, Any] | None = None,
    decision_record: dict[str, Any] | None = None,
    allow_terminal_completed_predecessor_historical: bool = False,
) -> dict[str, Any] | None:
    """Load and validate the persisted Kanban projection for one ticket."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    _require_explicit_terminal_completed_predecessor_historical_authority(
        ticket_id=safe_ticket_id,
        generation_record=generation_record,
        decision_record=decision_record,
        allow_terminal_completed_predecessor_historical=allow_terminal_completed_predecessor_historical,
    )
    path = kanban_projection_record_path_for_ticket(safe_ticket_id)
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkPacketKanbanProjectionConflict(
            f"{safe_ticket_id} Kanban projection record is unreadable"
        ) from exc
    return validate_kanban_projection_record(
        record,
        ticket_id=safe_ticket_id,
        generation_record=generation_record,
        decision_record=decision_record,
        allow_terminal_completed_predecessor_historical=allow_terminal_completed_predecessor_historical,
    )


def validate_p18_9_0_kanban_projection_record(
    record: dict[str, Any],
    *,
    generation_record: dict[str, Any] | None = None,
    decision_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate projection mapping without touching dispatcher or execution."""

    return validate_kanban_projection_record(
        record,
        ticket_id=CANONICAL_TICKET_ID,
        generation_record=generation_record,
        decision_record=decision_record,
    )


def validate_kanban_projection_record(
    record: dict[str, Any],
    *,
    ticket_id: str,
    generation_record: dict[str, Any] | None = None,
    decision_record: dict[str, Any] | None = None,
    allow_terminal_completed_predecessor_historical: bool = False,
) -> dict[str, Any]:
    """Validate projection mapping without touching dispatcher or execution."""

    if not isinstance(record, dict):
        raise WorkPacketKanbanProjectionConflict("Kanban projection record must be an object")
    if record.get("projection_SHA256") != _projection_record_digest(record):
        raise WorkPacketKanbanProjectionConflict("Kanban projection record digest mismatch")
    safe_ticket_id = _safe_ticket_id(ticket_id)
    _require_explicit_terminal_completed_predecessor_historical_authority(
        ticket_id=safe_ticket_id,
        generation_record=generation_record,
        decision_record=decision_record,
        allow_terminal_completed_predecessor_historical=allow_terminal_completed_predecessor_historical,
    )
    generation = _generation_authority(
        ticket_id=safe_ticket_id,
        generation_record=generation_record,
        allow_terminal_completed_predecessor_historical=allow_terminal_completed_predecessor_historical,
    )
    if generation is None:
        raise WorkPacketKanbanProjectionConflict("projection has no generated WorkPacket authority")
    if generation.get("ticket_id") != safe_ticket_id:
        raise WorkPacketKanbanProjectionConflict("projection generated ticket mismatch")
    decision = _approval_decision_authority(
        ticket_id=safe_ticket_id,
        generation_record=generation,
        decision_record=decision_record,
        allow_terminal_completed_predecessor_historical=allow_terminal_completed_predecessor_historical,
    )
    if decision is None:
        raise WorkPacketKanbanProjectionConflict("projection has no approval decision authority")
    _require_projection_identity(record, generation, decision)
    return record


def _require_explicit_terminal_completed_predecessor_historical_authority(
    *,
    ticket_id: str,
    generation_record: dict[str, Any] | None,
    decision_record: dict[str, Any] | None,
    allow_terminal_completed_predecessor_historical: bool,
) -> None:
    if not allow_terminal_completed_predecessor_historical:
        return
    if generation_record is None:
        raise WorkPacketKanbanProjectionConflict(
            f"{ticket_id} historical predecessor generation authority must be supplied"
        )
    if decision_record is None:
        raise WorkPacketKanbanProjectionConflict(
            f"{ticket_id} historical predecessor approval decision authority must be supplied"
        )


def _generation_authority(
    *,
    ticket_id: str,
    generation_record: dict[str, Any] | None,
    allow_terminal_completed_predecessor_historical: bool,
) -> dict[str, Any] | None:
    if generation_record is not None:
        if allow_terminal_completed_predecessor_historical:
            return validate_historical_approved_predecessor_generation_record(
                generation_record,
            )
        return validate_generation_record(generation_record)
    if allow_terminal_completed_predecessor_historical:
        raise WorkPacketKanbanProjectionConflict(
            f"{ticket_id} historical predecessor generation authority must be supplied"
        )
    return load_generation_record(ticket_id=ticket_id)


def _approval_decision_authority(
    *,
    ticket_id: str,
    generation_record: dict[str, Any],
    decision_record: dict[str, Any] | None = None,
    allow_terminal_completed_predecessor_historical: bool = False,
) -> dict[str, Any] | None:
    safe_ticket_id = _safe_ticket_id(ticket_id)
    try:
        if allow_terminal_completed_predecessor_historical:
            if decision_record is not None:
                return validate_historical_approved_predecessor_approval_decision_record(
                    decision_record,
                    ticket_id=safe_ticket_id,
                    generation_record=generation_record,
                )
            raise WorkPacketKanbanProjectionConflict(
                f"{safe_ticket_id} historical predecessor approval decision authority must be supplied"
            )
        if decision_record is not None:
            return validate_approval_decision_record(
                decision_record,
                ticket_id=safe_ticket_id,
                generation_record=generation_record,
            )
        return load_approval_decision_record(
            ticket_id=safe_ticket_id,
            generation_record=generation_record,
        )
    except TicketArchitectBridgeError as exc:
        raise WorkPacketKanbanProjectionConflict(
            f"{safe_ticket_id} approval decision authority is invalid"
        ) from exc


def project_approved_p18_9_0_workpacket_to_kanban(
    *,
    workflow: dict[str, Any],
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    """Project the approved P18.9.0 WorkPacket into Hermes Kanban without dispatch."""

    return project_current_approved_workpacket_to_kanban(
        workflow=workflow,
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
    )


def project_current_approved_workpacket_to_kanban(
    *,
    workflow: dict[str, Any],
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    """Project the current approved Pepper WorkPacket into Kanban without dispatch."""

    target = resolve_current_approved_workpacket_projection(
        workflow=workflow,
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
    )
    ticket_id = str(target["ticket_id"])
    with _STORE_LOCK:
        generation = load_generation_record(ticket_id=ticket_id)
        if generation is None:
            raise WorkPacketKanbanProjectionConflict(f"{ticket_id} has no generated WorkPacket")
        decision = _approval_decision_authority(
            ticket_id=ticket_id,
            generation_record=generation,
        )
        if decision is None or decision.get("decision") != "approve":
            raise WorkPacketKanbanProjectionConflict(f"{ticket_id} is not approved")
        _require_resolved_authority_matches(target, generation, decision)
        existing = load_kanban_projection_record(
            ticket_id=ticket_id,
            generation_record=generation,
            decision_record=decision,
        )
        if existing is not None:
            _require_existing_task_matches(existing)
            return _operational_result(existing, idempotent_replay=True)
        if target["workflow_status"] == "queued":
            raise WorkPacketKanbanProjectionConflict(
                f"{ticket_id} workflow is queued but projection authority is absent"
            )

        dependency_plan = TicketDependencyPlan.model_validate(generation["dependency_plan"])
        admission = derive_dependency_queue_admission_for_ticket(
            dependency_plan=dependency_plan,
            ticket_id=ticket_id,
        )
        if admission["decision"] != DependencyAwareQueueDecision.ADMIT.value:
            raise WorkPacketKanbanProjectionBlocked("DEPENDENCY_ADMISSION_BLOCKED")
        profile = resolve_execution_profile_for_ticket(generation)
        transitions = _build_projection_transitions(generation, decision, admission)
        task_id, task_status = _project_task(generation, decision, admission, profile)
        record = _build_projection_record(
            generation=generation,
            decision=decision,
            admission=admission,
            transitions=transitions,
            profile=profile,
            task_id=task_id,
            task_status=task_status,
        )
        validate_kanban_projection_record(
            record,
            ticket_id=ticket_id,
            generation_record=generation,
            decision_record=decision,
        )
        _persist_projection_record(record)
    return _operational_result(record, idempotent_replay=False)


def resolve_current_approved_workpacket_projection(
    *,
    workflow: dict[str, Any],
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    """Resolve the single current approved generated WorkPacket projection target."""

    workflow_state = _validate_workflow_eligibility(workflow)
    ticket_id = workflow_state["ticket_id"]
    _validate_requested_identity_for_ticket(
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
        ticket_id=ticket_id,
    )
    generation = load_generation_record(ticket_id=ticket_id)
    if generation is None:
        raise WorkPacketKanbanProjectionConflict(f"{ticket_id} has no generated WorkPacket")
    decision = _approval_decision_authority(ticket_id=ticket_id, generation_record=generation)
    if decision is None or decision.get("decision") != "approve":
        raise WorkPacketKanbanProjectionConflict(f"{ticket_id} is not approved")
    return {
        "ticket_id": ticket_id,
        "project_id": generation["project_id"],
        "macroproject_id": generation["macroproject_id"],
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "WorkPacket_compilation_count": generation["WorkPacket_compilation_count"],
        "approval_publication_SHA256": decision["approval_publication_SHA256"],
        "approval_decision": decision["decision"],
        "approval_status": decision["status"],
        "workflow_status": workflow_state["workflow_status"],
    }


def _require_resolved_authority_matches(
    target: dict[str, Any],
    generation: dict[str, Any],
    decision: dict[str, Any],
) -> None:
    expected = {
        "ticket_id": generation.get("ticket_id"),
        "project_id": generation.get("project_id"),
        "macroproject_id": generation.get("macroproject_id"),
        "ticket_spec_SHA256": generation.get("ticket_spec_SHA256"),
        "work_packet_id": generation.get("work_packet_id"),
        "work_packet_SHA256": generation.get("work_packet_SHA256"),
        "WorkPacket_compilation_count": generation.get("WorkPacket_compilation_count"),
        "approval_publication_SHA256": decision.get("approval_publication_SHA256"),
        "approval_decision": decision.get("decision"),
        "approval_status": decision.get("status"),
    }
    for key, value in expected.items():
        if target.get(key) != value:
            raise WorkPacketKanbanProjectionConflict(f"resolved {key} mismatch")


def resolve_p18_9_0_execution_profile() -> dict[str, Any]:
    """Resolve the existing governed Hermes assignee for P18.9.0."""

    return _resolve_execution_profile(required_role=_PEPPER_EXECUTION_PROFILE_ROLE)


def resolve_execution_profile_for_ticket(generation_record: dict[str, Any]) -> dict[str, Any]:
    """Resolve the governed Hermes assignee for the generated ticket type."""

    return _resolve_execution_profile(
        required_role=_required_execution_profile_role(generation_record),
        generation_record=generation_record,
    )


def _required_execution_profile_role(generation_record: dict[str, Any]) -> str:
    ticket_spec = generation_record.get("ticket_spec") if isinstance(generation_record, dict) else None
    ticket_type = str(
        ticket_spec.get("ticket_type") if isinstance(ticket_spec, dict) else ""
    ).strip().lower()
    if ticket_type == "implementation":
        return _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE
    return _PEPPER_EXECUTION_PROFILE_ROLE


def _execution_profile_requirements(required_role: str) -> dict[str, Any]:
    if required_role == _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE:
        return {
            "role": required_role,
            "required_toolsets": list(_PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_TOOLSETS),
            "allowed_toolsets": list(_PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_TOOLSETS),
            "required_sentinels": list(_PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS),
            "required_write_toolsets": list(
                _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_REQUIRED_WRITE_TOOLSETS
            ),
            "semantic_capabilities": list(_PEPPER_IMPLEMENTATION_SEMANTIC_CAPABILITIES),
            "capability_resolution_policy": _PEPPER_CAPABILITY_RESOLUTION_POLICY,
            "capability_resolution": _role_capability_resolution(required_role),
            "required_capability_labels": list(
                _PEPPER_IMPLEMENTATION_REQUIRED_CAPABILITY_LABELS
            ),
        }
    return {
        "role": _PEPPER_EXECUTION_PROFILE_ROLE,
        "required_toolsets": list(_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS),
        "allowed_toolsets": list(_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS),
        "required_sentinels": list(_PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS),
        "required_write_toolsets": [],
        "semantic_capabilities": list(_PEPPER_SEMANTIC_CAPABILITIES),
        "capability_resolution_policy": _PEPPER_CAPABILITY_RESOLUTION_POLICY,
        "capability_resolution": _role_capability_resolution(_PEPPER_EXECUTION_PROFILE_ROLE),
        "required_capability_labels": list(_PEPPER_REQUIRED_CAPABILITY_LABELS),
    }


def _ticket_execution_requirements(
    required_role: str,
    generation_record: dict[str, Any] | None,
) -> dict[str, Any]:
    ticket_spec = generation_record.get("ticket_spec") if isinstance(generation_record, dict) else None
    ticket_type = str(
        ticket_spec.get("ticket_type") if isinstance(ticket_spec, dict) else ""
    ).strip().lower()
    return {
        "schema_version": PEPPER_EXECUTION_PROFILES_SCHEMA_VERSION,
        "policy_id": PEPPER_EXECUTION_PROFILES_POLICY_ID,
        "policy_revision": PEPPER_EXECUTION_PROFILES_POLICY_REVISION,
        "ticket_id": str(generation_record.get("ticket_id") or "") if isinstance(generation_record, dict) else "",
        "ticket_type": ticket_type,
        **_execution_profile_requirements(required_role),
    }


def _resolve_execution_profile(
    *,
    required_role: str,
    generation_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if required_role not in {
        _PEPPER_EXECUTION_PROFILE_ROLE,
        _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE,
    }:
        diagnostics = _profile_assignment_diagnostics(
            required_role=required_role,
            generation_record=generation_record,
            roster=[],
            candidates=[],
            blocker_code="PROFILE_ASSIGNMENT_GAP",
            selected_profile=None,
        )
        raise WorkPacketKanbanProjectionProfileGap(
            "PROFILE_ASSIGNMENT_GAP",
            diagnostics=diagnostics,
        )

    try:
        profiles = list_profiles()
    except Exception as exc:
        diagnostics = _profile_assignment_diagnostics(
            required_role=required_role,
            generation_record=generation_record,
            roster=[],
            candidates=[],
            blocker_code="PROFILE_ASSIGNMENT_GAP",
            selected_profile=None,
        )
        raise WorkPacketKanbanProjectionProfileGap(
            "PROFILE_ASSIGNMENT_GAP",
            diagnostics=diagnostics,
        ) from exc
    roster = [classify_pepper_execution_profile(profile) for profile in profiles]
    if not roster:
        diagnostics = _profile_assignment_diagnostics(
            required_role=required_role,
            generation_record=generation_record,
            roster=roster,
            candidates=[],
            blocker_code="PROFILE_ASSIGNMENT_GAP",
            selected_profile=None,
        )
        raise WorkPacketKanbanProjectionProfileGap(
            "PROFILE_ASSIGNMENT_GAP",
            diagnostics=diagnostics,
        )
    candidates = [
        item for item in roster
        if item["role"] == required_role
        and item["worker_assignable"] is True
    ]
    if len(candidates) > 1:
        diagnostics = _profile_assignment_diagnostics(
            required_role=required_role,
            generation_record=generation_record,
            roster=roster,
            candidates=candidates,
            blocker_code="HUMAN_PROFILE_SELECTION_REQUIRED",
            selected_profile=None,
        )
        raise WorkPacketKanbanProjectionProfileSelectionRequired(
            "HUMAN_PROFILE_SELECTION_REQUIRED",
            diagnostics=diagnostics,
        )
    if candidates:
        selected = candidates[0]
        requirements = _ticket_execution_requirements(required_role, generation_record)
        diagnostics = _profile_assignment_diagnostics(
            required_role=required_role,
            generation_record=generation_record,
            roster=roster,
            candidates=candidates,
            blocker_code=None,
            selected_profile=selected["canonical_name"],
        )
        return {
            "assignee_profile": selected["canonical_name"],
            "selected_profile": selected["canonical_name"],
            "profile_assignment_policy_id": PEPPER_EXECUTION_PROFILES_POLICY_ID,
            "profile_assignment_policy_revision": PEPPER_EXECUTION_PROFILES_POLICY_REVISION,
            "profile_assignment_basis": "governed_role_taxonomy",
            "selection_rationale": "deterministic_single_governed_role_match",
            "candidate_profiles": [item["canonical_name"] for item in candidates],
            "profile_assignment_gap": False,
            "execution_profile_role": required_role,
            "selected_role": required_role,
            "profile_classification_basis": selected["classification_basis"],
            "profile_toolsets": selected["cli_toolsets"],
            "profile_toolset_policy": "explicit_bounded_cli_toolsets",
            "required_profile_toolsets": requirements["required_toolsets"],
            "required_profile_sentinels": requirements["required_sentinels"],
            "required_write_toolsets": requirements["required_write_toolsets"],
            "required_capabilities": requirements["semantic_capabilities"],
            "ticket_execution_requirements": requirements,
            "profile_assignment_diagnostics": diagnostics,
            "lead_agent_auto_assigned": False,
            "ticket_architect_executor_distinct": True,
            "human_profile_selection_required": False,
            "available_profiles": roster,
        }
    blocker_code = _profile_assignment_blocker_code(required_role, roster)
    diagnostics = _profile_assignment_diagnostics(
        required_role=required_role,
        generation_record=generation_record,
        roster=roster,
        candidates=candidates,
        blocker_code=blocker_code,
        selected_profile=None,
    )
    raise WorkPacketKanbanProjectionProfileGap(
        blocker_code,
        diagnostics=diagnostics,
    )


def _profile_assignment_blocker_code(required_role: str, roster: list[dict[str, Any]]) -> str:
    if required_role != _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE:
        return "PROFILE_ASSIGNMENT_GAP"
    for item in roster:
        if item.get("role") != required_role:
            continue
        reasons = set(item.get("rejection_reasons") or [])
        if (
            "implementation_profile_read_only" in reasons
            or any(str(reason).startswith("missing_required_write_toolsets:") for reason in reasons)
        ):
            return "IMPLEMENTATION_WORKER_WRITE_CAPABILITY_GAP"
    return "PROFILE_ASSIGNMENT_GAP"


def _profile_assignment_diagnostics(
    *,
    required_role: str,
    generation_record: dict[str, Any] | None,
    roster: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    blocker_code: str | None,
    selected_profile: str | None,
) -> dict[str, Any]:
    role_candidates = [item for item in roster if item.get("role") == required_role]
    return {
        "schema_version": PEPPER_EXECUTION_PROFILES_SCHEMA_VERSION,
        "policy_id": PEPPER_EXECUTION_PROFILES_POLICY_ID,
        "policy_revision": PEPPER_EXECUTION_PROFILES_POLICY_REVISION,
        "profile_assignment_basis": "governed_role_taxonomy",
        "blocker_code": blocker_code,
        "selected_profile": selected_profile,
        "required_role": required_role,
        "ticket_execution_requirements": _ticket_execution_requirements(
            required_role,
            generation_record,
        ),
        "candidate_profiles": [item["canonical_name"] for item in candidates],
        "role_candidate_profiles": [item["canonical_name"] for item in role_candidates],
        "available_profile_count": len(roster),
        "available_profiles": roster,
        "rejection_reasons_by_profile": {
            item["canonical_name"]: list(item.get("rejection_reasons") or [])
            for item in roster
        },
        "human_profile_selection_required": blocker_code == "HUMAN_PROFILE_SELECTION_REQUIRED",
    }


def classify_pepper_execution_profile(profile: Any) -> dict[str, Any]:
    """Classify one Hermes profile against Pepper's worker role taxonomy."""

    name = str(_profile_value(profile, "name") or "").strip()
    description = str(_profile_value(profile, "description") or "").strip()
    is_default = bool(_profile_value(profile, "is_default", False))
    try:
        canonical_name = normalize_profile_name(name)
    except Exception:
        canonical_name = name.strip().lower()
    name_words = _profile_words(name)
    words = _profile_words(name, description)
    name_compact = "".join(name_words)
    compact = "".join(words)

    if is_default or canonical_name == "default":
        role = _PEPPER_DEFAULT_PROFILE_ROLE
        basis = "default_profile_not_worker_assignable"
    elif _is_lead_agent_profile(name_words, name_compact):
        role = _PEPPER_LEAD_AGENT_ROLE
        basis = "lead_agent_not_worker_assignable"
    elif _is_ticket_architect_profile(name_words, name_compact):
        role = _PEPPER_TICKET_ARCHITECT_ROLE
        basis = "ticket_architect_not_executor"
    elif _is_architecture_product_execution_profile(words):
        role = _PEPPER_EXECUTION_PROFILE_ROLE
        basis = "product_architecture_role_terms"
    elif _is_implementation_product_execution_profile(words):
        role = _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE
        basis = "product_implementation_role_terms"
    else:
        role = _PEPPER_UNCLASSIFIED_PROFILE_ROLE
        basis = "no_matching_execution_role_terms"

    toolset_policy = _profile_toolset_policy(profile, role=role)
    rejection_reasons: list[str] = []
    if role not in {_PEPPER_EXECUTION_PROFILE_ROLE, _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE}:
        rejection_reasons.append(basis)
    if not toolset_policy["bounded"]:
        rejection_reasons.extend(toolset_policy["violations"])

    return {
        "name": name,
        "canonical_name": canonical_name,
        "description": description,
        "is_default": is_default,
        "role": role,
        "classification_basis": basis,
        "worker_assignable": (
            role in {_PEPPER_EXECUTION_PROFILE_ROLE, _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE}
            and toolset_policy["bounded"] is True
        ),
        "cli_toolsets": toolset_policy["cli_toolsets"],
        "toolset_source": toolset_policy["source"],
        "toolset_bounded": toolset_policy["bounded"],
        "required_toolsets": toolset_policy["required_toolsets"],
        "required_sentinels": toolset_policy["required_sentinels"],
        "required_write_toolsets": toolset_policy["required_write_toolsets"],
        "write_capable": toolset_policy["write_capable"],
        "rejection_reasons": rejection_reasons,
    }


def _profile_value(profile: Any, key: str, default: Any = "") -> Any:
    if isinstance(profile, dict):
        return profile.get(key, default)
    return getattr(profile, key, default)


def _profile_words(*values: object) -> tuple[str, ...]:
    text = " ".join(str(value or "") for value in values).casefold()
    return tuple(_PROFILE_TEXT_TOKEN.findall(text))


def _is_lead_agent_profile(words: tuple[str, ...], compact: str) -> bool:
    word_set = set(words)
    return "leadagent" in compact or {"lead", "agent"}.issubset(word_set)


def _is_ticket_architect_profile(words: tuple[str, ...], compact: str) -> bool:
    word_set = set(words)
    return "ticketarchitect" in compact or {"ticket", "architect"}.issubset(word_set)


def _is_architecture_product_execution_profile(words: tuple[str, ...]) -> bool:
    word_set = set(words)
    product_terms = {"product", "inventory"}
    architecture_terms = {
        "architecture",
        "architectural",
        "ia",
        "inventory",
        "presentation",
        "wizard",
        "acceptance",
        "contract",
        "audit",
    }
    return bool(word_set & product_terms) and bool(word_set & architecture_terms)


def _is_implementation_product_execution_profile(words: tuple[str, ...]) -> bool:
    word_set = set(words)
    implementation_terms = {
        "implementation",
        "implement",
        "frontend",
        "front",
        "ui",
        "shell",
        "routing",
        "navigation",
    }
    product_surface_terms = {
        "product",
        "frontend",
        "ui",
        "shell",
        "routing",
        "navigation",
        "surface",
    }
    return bool(word_set & implementation_terms) and bool(word_set & product_surface_terms)


def _profile_toolset_policy(profile: Any, *, role: str) -> dict[str, Any]:
    requirements = _execution_profile_requirements(role)
    required_toolsets = tuple(requirements["required_toolsets"])
    allowed_toolsets = tuple(requirements["allowed_toolsets"])
    required_sentinels = tuple(requirements["required_sentinels"])
    required_write_toolsets = tuple(requirements["required_write_toolsets"])
    raw_toolsets, source = _profile_explicit_cli_toolsets(profile)
    normalized = tuple(
        str(toolset).strip()
        for toolset in raw_toolsets
        if str(toolset).strip()
    )
    explicit_toolsets = tuple(dict.fromkeys(
        toolset for toolset in normalized
        if toolset not in required_sentinels
    ))
    actual = tuple(
        toolset for toolset in required_toolsets
        if toolset in explicit_toolsets
    ) + tuple(
        sorted(toolset for toolset in explicit_toolsets if toolset not in required_toolsets)
    )
    violations: list[str] = []
    if source is None:
        violations.append("explicit_cli_toolsets_required")
    missing = sorted(set(required_toolsets) - set(actual))
    if missing:
        violations.append("missing_required_toolsets:" + ",".join(missing))
    extra = sorted(set(actual) - set(allowed_toolsets))
    if extra:
        violations.append("unbounded_toolsets:" + ",".join(extra))
    missing_write = sorted(set(required_write_toolsets) - set(actual))
    write_capable = not missing_write
    if missing_write:
        violations.append("missing_required_write_toolsets:" + ",".join(missing_write))
        if role == _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE and set(actual) == set(
            _PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS
        ):
            violations.append("implementation_profile_read_only")
    missing_sentinels = sorted(
        set(required_sentinels) - set(normalized)
    )
    if missing_sentinels:
        violations.append("missing_required_sentinels:" + ",".join(missing_sentinels))
    if _profile_uses_nondefault_context_engine(profile):
        violations.append("nondefault_context_engine_not_bounded")
    if _profile_disables_required_toolsets(profile, required_toolsets=required_toolsets):
        violations.append("required_toolset_disabled")
    return {
        "source": source,
        "cli_toolsets": list(actual),
        "bounded": not violations,
        "required_toolsets": list(required_toolsets),
        "required_sentinels": list(required_sentinels),
        "required_write_toolsets": list(required_write_toolsets),
        "write_capable": write_capable,
        "violations": violations,
    }


def _profile_explicit_cli_toolsets(profile: Any) -> tuple[tuple[str, ...], str | None]:
    attr_toolsets = _profile_value(profile, "cli_toolsets", None)
    if isinstance(attr_toolsets, (list, tuple)):
        return tuple(str(toolset) for toolset in attr_toolsets), "profile.cli_toolsets"
    config = _read_profile_config(profile)
    platform_toolsets = config.get("platform_toolsets") if isinstance(config, dict) else None
    if isinstance(platform_toolsets, dict):
        cli_toolsets = platform_toolsets.get("cli")
        if isinstance(cli_toolsets, list):
            return tuple(str(toolset) for toolset in cli_toolsets), "config.platform_toolsets.cli"
    return (), None


def _read_profile_config(profile: Any) -> dict[str, Any]:
    path_value = _profile_value(profile, "path", None)
    if not path_value:
        return {}
    config_path = Path(path_value) / "config.yaml"
    if not config_path.is_file():
        return {}
    try:
        import yaml

        with open(config_path, "r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _profile_uses_nondefault_context_engine(profile: Any) -> bool:
    config = _read_profile_config(profile)
    context = config.get("context") if isinstance(config, dict) else None
    if not isinstance(context, dict):
        return False
    engine = str(context.get("engine") or "compressor").strip().lower()
    return bool(engine and engine != "compressor")


def _profile_disables_required_toolsets(
    profile: Any,
    *,
    required_toolsets: tuple[str, ...],
) -> bool:
    config = _read_profile_config(profile)
    agent = config.get("agent") if isinstance(config, dict) else None
    if not isinstance(agent, dict):
        return False
    disabled = agent.get("disabled_toolsets") or []
    if not isinstance(disabled, list):
        return False
    return bool(
        set(required_toolsets) & {str(item) for item in disabled}
    )


def kanban_projection_to_workflow_overlay(record: dict[str, Any]) -> dict[str, Any]:
    """Return workflow-control fields implied by a validated Kanban projection."""

    ticket_id = _safe_ticket_id(record.get("ticket_id"))
    validated = validate_kanban_projection_record(record, ticket_id=ticket_id)
    return {
        "readiness": "queued_not_executing",
        "workflow_state": f"{ticket_id}-QUEUED-NOT-EXECUTING",
        "workflow_status": "queued",
        "approval_state": "ticket_approved",
        "pending_ticket_approval_count": 0,
        "queue_state": "kanban_projection_ready_not_dispatched",
        "execution_state": "not_started",
        "validation_state": "queued_not_executed",
        "review_state": "not_started_execution_pending",
        "recovery_state": "not_required",
        "git_handoff_state": "human_git_authority_preserved",
        "P18_9_ticket_generated": True,
        "P18_9_ticket_approved": True,
        "P18_9_work_packet_compiled": True,
        "P18_9_kanban_projection_present": True,
        "kanban_projection_authority": _projection_authority(validated),
        "assignee_profile": validated["assignee_profile"],
        "selected_profile": validated["selected_profile"],
        "profile_assignment_policy_id": validated["profile_assignment_policy_id"],
        "profile_assignment_policy_revision": validated.get("profile_assignment_policy_revision"),
        "selection_rationale": validated["selection_rationale"],
        "execution_profile_role": validated["execution_profile_role"],
        "selected_role": validated["selected_role"],
        "profile_toolsets": validated["profile_toolsets"],
        "required_profile_toolsets": validated.get("required_profile_toolsets", []),
        "required_write_toolsets": validated.get("required_write_toolsets", []),
        "required_capabilities": validated.get("required_capabilities", []),
        "lead_agent_auto_assigned": validated["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": validated["ticket_architect_executor_distinct"],
        "next_action": {
            "id": execution_start_action_id(ticket_id),
            "label": (
                f"{ticket_id} is projected to Kanban and ready for a separate explicit "
                "human authorization to start execution."
            ),
            "target_ticket_id": ticket_id,
            "target_ticket_title": validated["ticket_title"],
            "required_human_action": "execution_start_authorization",
        },
        "execution_started": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
    }


def _validate_requested_identity(
    *,
    requested_project_id: str | None,
    requested_ticket_id: str | None,
    requested_next_action_id: str | None,
) -> None:
    _validate_requested_identity_for_ticket(
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
        ticket_id=CANONICAL_TICKET_ID,
    )


def _validate_requested_identity_for_ticket(
    *,
    requested_project_id: str | None,
    requested_ticket_id: str | None,
    requested_next_action_id: str | None,
    ticket_id: str,
) -> None:
    safe_ticket_id = _safe_ticket_id(ticket_id)
    expected_next_action_id = approved_no_execution_action_id(safe_ticket_id)
    if requested_project_id not in {None, "", CANONICAL_PROJECT_ID}:
        raise WorkPacketKanbanProjectionInputError("requested project is not PEPPER")
    if requested_ticket_id not in {None, "", safe_ticket_id}:
        raise WorkPacketKanbanProjectionInputError(
            f"requested ticket is not {safe_ticket_id}"
        )
    if requested_next_action_id not in {None, "", expected_next_action_id}:
        raise WorkPacketKanbanProjectionInputError(
            f"requested next action is not {expected_next_action_id}"
        )


def _validate_workflow_eligibility(workflow: dict[str, Any]) -> dict[str, str]:
    if not isinstance(workflow, dict):
        raise WorkPacketKanbanProjectionInputError("workflow state is unavailable")
    if workflow.get("project_id") != CANONICAL_PROJECT_ID:
        raise WorkPacketKanbanProjectionInputError("active governed project is not PEPPER")
    ticket_id = _safe_ticket_id(workflow.get("current_ticket_id"))
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        raise WorkPacketKanbanProjectionInputError("next action is unavailable")
    if next_action.get("target_ticket_id") != ticket_id:
        raise WorkPacketKanbanProjectionInputError(f"next action does not target {ticket_id}")
    workflow_status = str(workflow.get("workflow_status") or "").strip()
    if workflow_status == "ticket_approved":
        expected_next_action_id = approved_no_execution_action_id(ticket_id)
        if next_action.get("id") != expected_next_action_id:
            raise WorkPacketKanbanProjectionInputError("next action is not projection preparation")
    elif workflow_status == "queued":
        if workflow.get("queue_state") != "kanban_projection_ready_not_dispatched":
            raise WorkPacketKanbanProjectionInputError("queue state is not projected")
        if next_action.get("id") != execution_start_action_id(ticket_id):
            raise WorkPacketKanbanProjectionInputError("next action is not execution start authorization")
    elif workflow_status != "awaiting_ticket_approval":
        raise WorkPacketKanbanProjectionInputError(f"{ticket_id} is not ticket_approved")
    if int(workflow.get("pending_ticket_approval_count") or 0) != 0:
        if workflow_status != "awaiting_ticket_approval":
            raise WorkPacketKanbanProjectionInputError("pending ticket approvals remain")
    if int(workflow.get("active_execution_count") or 0) != 0:
        raise WorkPacketKanbanProjectionBlocked("EXECUTION_ALREADY_ACTIVE")
    if workflow.get("execution_state") == "active_executions":
        raise WorkPacketKanbanProjectionBlocked("EXECUTION_ALREADY_ACTIVE")
    return {"ticket_id": ticket_id, "workflow_status": workflow_status}


def _build_projection_transitions(
    generation: dict[str, Any],
    decision: dict[str, Any],
    admission: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    ticket_id = _safe_ticket_id(generation.get("ticket_id"))
    approval_transition = GovernedWorkflowTransitionResult.model_validate(
        decision["workflow_transition_result"]
    )
    work_packet_ready_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=approval_transition.resulting_snapshot,
        trigger=WorkflowTransitionTrigger.WORK_PACKET_COMPILED,
        authority=WorkflowTransitionAuthority.GOVERNED_RUNTIME,
        evidence_refs=("work_packet_compilation_result",),
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.WORK_PACKET,
            runtime_state="p17:work_packet_ready",
            task_id=None,
            board_or_queue_id=None,
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=False,
            retry_state_present=False,
            reclaim_state_present=False,
        ),
    )
    validate_governed_workflow_transition_request(work_packet_ready_request)
    work_packet_ready_transition = build_governed_workflow_transition(
        work_packet_ready_request
    )
    queued_request = GovernedWorkflowTransitionRequest(
        schema_version=GOVERNED_WORKFLOW_STATE_MACHINE_SCHEMA_VERSION,
        policy_id=GOVERNED_WORKFLOW_STATE_MACHINE_POLICY_ID,
        current_snapshot=work_packet_ready_transition.resulting_snapshot,
        trigger=WorkflowTransitionTrigger.DEPENDENCIES_READY,
        authority=WorkflowTransitionAuthority.POLICY,
        evidence_refs=("dependency_plan_ready",),
        runtime_projection=build_hermes_workflow_projection(
            runtime_kind=HermesWorkflowRuntimeKind.KANBAN_SWARM,
            runtime_state="todo",
            task_id=None,
            board_or_queue_id=f"{ticket_id}-kanban-projection",
            worker_id_present=False,
            workspace_binding_present=False,
            dependency_blocked=not bool(admission["queue_admitted"]),
            retry_state_present=False,
            reclaim_state_present=False,
        ),
    )
    validate_governed_workflow_transition_request(queued_request)
    queued_transition = build_governed_workflow_transition(queued_request)
    if not work_packet_ready_transition.accepted or not queued_transition.accepted:
        raise WorkPacketKanbanProjectionConflict("workflow projection transition rejected")
    return (
        work_packet_ready_transition.model_dump(mode="json"),
        queued_transition.model_dump(mode="json"),
    )


def _project_task(
    generation: dict[str, Any],
    decision: dict[str, Any],
    admission: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[str, str]:
    idempotency_key = _idempotency_key(generation)
    body = _task_body(generation, decision, admission, profile, task_id=None)
    conn = kanban_db.connect(board=_KANBAN_BOARD)
    try:
        existing = _find_task_by_idempotency_key(conn, idempotency_key)
        if existing is not None:
            _require_existing_task_body_matches(existing, generation, profile=profile)
            task = kanban_db.get_task(conn, existing["id"])
            if task is None:
                raise WorkPacketKanbanProjectionConflict("existing Kanban task is missing")
            return task.id, task.status
        task_id = kanban_db.create_task(
            conn,
            title=f"{generation['ticket_id']} {generation['ticket_title']}",
            body=body,
            assignee=profile["assignee_profile"],
            created_by="pepper-workpacket-kanban-projection",
            workspace_kind=_WORKSPACE_KIND,
            priority=50,
            tenant="pepper",
            idempotency_key=idempotency_key,
            skills=_TASK_SKILLS,
            max_retries=_TASK_MAX_RETRIES,
            board=_KANBAN_BOARD,
        )
        kanban_db.recompute_ready(conn)
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            raise WorkPacketKanbanProjectionConflict("created Kanban task is missing")
        return task.id, task.status
    finally:
        conn.close()


def _find_task_by_idempotency_key(conn, idempotency_key: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT id, body, assignee FROM tasks WHERE idempotency_key = ? AND status != 'archived' "
        "ORDER BY created_at DESC LIMIT 1",
        (idempotency_key,),
    ).fetchone()
    return dict(row) if row else None


def _require_existing_task_matches(record: dict[str, Any]) -> None:
    conn = kanban_db.connect(board=record["kanban_board_slug"])
    try:
        row = conn.execute(
            "SELECT id, body, status, assignee FROM tasks WHERE id = ? AND status != 'archived'",
            (record["kanban_task_id"],),
        ).fetchone()
        if row is None:
            raise WorkPacketKanbanProjectionConflict("projection Kanban task is missing")
        _require_existing_task_body_matches(dict(row), record)
    finally:
        conn.close()


def _require_existing_task_body_matches(
    task_row: dict[str, Any],
    authority: dict[str, Any],
    *,
    profile: dict[str, Any] | None = None,
) -> None:
    try:
        payload = json.loads(task_row.get("body") or "{}")
    except json.JSONDecodeError as exc:
        raise WorkPacketKanbanProjectionConflict("existing Kanban task body is not projection JSON") from exc
    expected_ticket_id = authority.get("ticket_id") or authority.get("ticket_ID")
    if payload.get("ticket_id") != expected_ticket_id:
        raise WorkPacketKanbanProjectionConflict("existing Kanban task ticket mismatch")
    if payload.get("WorkPacket_ID") != authority.get("work_packet_id", authority.get("WorkPacket_ID")):
        raise WorkPacketKanbanProjectionConflict("existing Kanban task WorkPacket ID mismatch")
    if payload.get("WorkPacket_SHA256") != authority.get("work_packet_SHA256", authority.get("WorkPacket_SHA256")):
        raise WorkPacketKanbanProjectionConflict("existing Kanban task WorkPacket digest mismatch")
    if payload.get("TicketSpec_SHA256") != authority.get("ticket_spec_SHA256", authority.get("TicketSpec_SHA256")):
        raise WorkPacketKanbanProjectionConflict("existing Kanban task TicketSpec digest mismatch")
    expected_profile = profile or authority
    expected_assignee = expected_profile.get("assignee_profile")
    if expected_assignee is not None:
        if task_row.get("assignee") != expected_assignee:
            raise WorkPacketKanbanProjectionConflict("existing Kanban task assignee mismatch")
        if payload.get("assignee_profile") != expected_assignee:
            raise WorkPacketKanbanProjectionConflict("existing Kanban task body assignee mismatch")
    expected_policy = expected_profile.get("profile_assignment_policy_id")
    if expected_policy is not None and payload.get("profile_assignment_policy_id") != expected_policy:
        raise WorkPacketKanbanProjectionConflict("existing Kanban task profile policy mismatch")
    expected_role = expected_profile.get("execution_profile_role")
    if expected_role is not None and payload.get("execution_profile_role") != expected_role:
        raise WorkPacketKanbanProjectionConflict("existing Kanban task profile role mismatch")


def _build_projection_record(
    *,
    generation: dict[str, Any],
    decision: dict[str, Any],
    admission: dict[str, Any],
    transitions: tuple[dict[str, Any], dict[str, Any]],
    profile: dict[str, Any],
    task_id: str,
    task_status: str,
) -> dict[str, Any]:
    ticket_id = _safe_ticket_id(generation["ticket_id"])
    next_action_id = execution_start_action_id(ticket_id)
    record = {
        "schema_version": WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION,
        "policy_id": WORK_PACKET_KANBAN_PROJECTION_POLICY_ID,
        "created_at": _utc_now_iso(),
        "project_id": generation["project_id"],
        "macroproject_id": generation["macroproject_id"],
        "ticket_id": ticket_id,
        "ticket_title": generation["ticket_title"],
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "WorkPacket_compilation_count": generation["WorkPacket_compilation_count"],
        "approval_id": decision["approval_id"],
        "approval_status": decision["status"],
        "approval_decision": decision["decision"],
        "approval_publication_SHA256": decision["approval_publication_SHA256"],
        "ticket_approval_record_SHA256": decision["ticket_approval_record"]["approval_SHA256"],
        "dependency_plan_SHA256": generation["dependency_plan_SHA256"],
        "dependency_admission": admission,
        "dependency_admission_policy_id": DEPENDENCY_AWARE_QUEUE_POLICY_ID,
        "dependency_plan_reused": True,
        "dependency_planner_reused": True,
        "dependency_plan_recomputed_unnecessarily": False,
        "approval_bypass": False,
        "dependency_bypass": False,
        "workflow_transition_results": transitions,
        "resulting_workflow_state": "queued",
        "provisional_execution_projection": True,
        "Kanban_canonical_authority": False,
        "kanban_board_slug": _KANBAN_BOARD,
        "kanban_task_id": task_id,
        "kanban_task_status": task_status,
        "kanban_task_idempotency_key": _idempotency_key(generation),
        "assignee_profile": profile["assignee_profile"],
        "selected_profile": profile["selected_profile"],
        "profile_assignment_policy_id": profile["profile_assignment_policy_id"],
        "profile_assignment_policy_revision": profile["profile_assignment_policy_revision"],
        "profile_assignment_basis": profile["profile_assignment_basis"],
        "selection_rationale": profile["selection_rationale"],
        "candidate_profiles": profile["candidate_profiles"],
        "profile_assignment_gap": profile["profile_assignment_gap"],
        "execution_profile_role": profile["execution_profile_role"],
        "selected_role": profile["selected_role"],
        "profile_classification_basis": profile["profile_classification_basis"],
        "profile_toolsets": profile["profile_toolsets"],
        "profile_toolset_policy": profile["profile_toolset_policy"],
        "required_profile_toolsets": profile["required_profile_toolsets"],
        "required_profile_sentinels": profile["required_profile_sentinels"],
        "required_write_toolsets": profile["required_write_toolsets"],
        "required_capabilities": profile["required_capabilities"],
        "ticket_execution_requirements": profile["ticket_execution_requirements"],
        "lead_agent_auto_assigned": profile["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": profile["ticket_architect_executor_distinct"],
        "human_profile_selection_required": profile["human_profile_selection_required"],
        "concurrent_workers_for_ticket": _MAX_CONCURRENT_WORKERS_FOR_TICKET,
        "task_max_retries": _TASK_MAX_RETRIES,
        "task_skills": list(_TASK_SKILLS),
        "semantic_capabilities": _role_semantic_capabilities(profile["execution_profile_role"]),
        "capability_resolution_policy": _PEPPER_CAPABILITY_RESOLUTION_POLICY,
        "capability_resolution": _capability_resolution(profile["execution_profile_role"]),
        "required_capability_labels": _role_required_capability_labels(profile["execution_profile_role"]),
        "workspace_kind": _WORKSPACE_KIND,
        "workspace_created": False,
        "workspace_allocation_count": 0,
        "dispatch_performed": False,
        "dispatcher_calls": 0,
        "worker_process_started": False,
        "worker_execution": False,
        "execution_started": False,
        "command_execution_count": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "retry_execution_count": 0,
        "rollback_count": 0,
        "Paperclip_calls": 0,
        "next_action": {
            "id": next_action_id,
            "target_ticket_id": ticket_id,
            "required_human_action": "execution_start_authorization",
        },
    }
    record["projection_SHA256"] = _projection_record_digest(record)
    return record


def _task_body(
    generation: dict[str, Any],
    decision: dict[str, Any],
    admission: dict[str, Any],
    profile: dict[str, Any],
    *,
    task_id: str | None,
) -> str:
    payload = {
        "projection": "Pepper approved WorkPacket to Hermes Kanban",
        "provisional_execution_projection": True,
        "Kanban_canonical_authority": False,
        "project_id": generation["project_id"],
        "macroproject_id": generation["macroproject_id"],
        "ticket_id": generation["ticket_id"],
        "ticket_title": generation["ticket_title"],
        "TicketSpec_SHA256": generation["ticket_spec_SHA256"],
        "WorkPacket_ID": generation["work_packet_id"],
        "WorkPacket_SHA256": generation["work_packet_SHA256"],
        "approval_id": decision["approval_id"],
        "approval_publication_SHA256": decision["approval_publication_SHA256"],
        "dependency_plan_SHA256": generation["dependency_plan_SHA256"],
        "dependency_admission_policy_id": DEPENDENCY_AWARE_QUEUE_POLICY_ID,
        "dependency_admission_decision": admission["decision"],
        "assignee_profile": profile["assignee_profile"],
        "selected_profile": profile["selected_profile"],
        "profile_assignment_policy_id": profile["profile_assignment_policy_id"],
        "profile_assignment_policy_revision": profile["profile_assignment_policy_revision"],
        "profile_assignment_basis": profile["profile_assignment_basis"],
        "selection_rationale": profile["selection_rationale"],
        "execution_profile_role": profile["execution_profile_role"],
        "selected_role": profile["selected_role"],
        "profile_toolsets": profile["profile_toolsets"],
        "profile_toolset_policy": profile["profile_toolset_policy"],
        "required_profile_toolsets": profile["required_profile_toolsets"],
        "required_write_toolsets": profile["required_write_toolsets"],
        "required_capabilities": profile["required_capabilities"],
        "lead_agent_auto_assigned": profile["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": profile["ticket_architect_executor_distinct"],
        "concurrent_workers_for_ticket": _MAX_CONCURRENT_WORKERS_FOR_TICKET,
        "task_max_retries": _TASK_MAX_RETRIES,
        "task_skills": list(_TASK_SKILLS),
        "semantic_capabilities": _role_semantic_capabilities(profile["execution_profile_role"]),
        "capability_resolution_policy": _PEPPER_CAPABILITY_RESOLUTION_POLICY,
        "capability_resolution": _capability_resolution(profile["execution_profile_role"]),
        "task_id": task_id,
        "dispatch_performed": False,
        "execution_started": False,
        "Git_mutation": False,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _operational_result(record: dict[str, Any], *, idempotent_replay: bool) -> dict[str, Any]:
    return {
        "source_system": "pepper-workpacket-kanban-projection",
        "schema_version": WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION,
        "policy_id": WORK_PACKET_KANBAN_PROJECTION_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "projection_status": "projected",
        "project_id": record["project_id"],
        "macroproject_id": record["macroproject_id"],
        "ticket_id": record["ticket_id"],
        "ticket_title": record["ticket_title"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "approval_publication_SHA256": record["approval_publication_SHA256"],
        "ticket_approval_record_SHA256": record["ticket_approval_record_SHA256"],
        "dependency_admission": record["dependency_admission"],
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_status": record["kanban_task_status"],
        "duplicate_task": False,
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "profile_assignment_policy_id": record["profile_assignment_policy_id"],
        "profile_assignment_policy_revision": record.get("profile_assignment_policy_revision"),
        "profile_assignment_basis": record["profile_assignment_basis"],
        "selection_rationale": record["selection_rationale"],
        "execution_profile_role": record["execution_profile_role"],
        "selected_role": record["selected_role"],
        "profile_toolsets": record["profile_toolsets"],
        "profile_toolset_policy": record["profile_toolset_policy"],
        "required_profile_toolsets": record.get("required_profile_toolsets", []),
        "required_profile_sentinels": record.get("required_profile_sentinels", []),
        "required_write_toolsets": record.get("required_write_toolsets", []),
        "required_capabilities": record.get("required_capabilities", []),
        "ticket_execution_requirements": record.get("ticket_execution_requirements", {}),
        "lead_agent_auto_assigned": record["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": record["ticket_architect_executor_distinct"],
        "human_profile_selection_required": record["human_profile_selection_required"],
        "concurrent_workers_for_ticket": record["concurrent_workers_for_ticket"],
        "task_max_retries": record["task_max_retries"],
        "task_skills": record["task_skills"],
        "semantic_capabilities": record.get("semantic_capabilities", []),
        "capability_resolution_policy": record.get("capability_resolution_policy"),
        "capability_resolution": record.get("capability_resolution", []),
        "workspace_kind": record["workspace_kind"],
        "workspace_created": False,
        "provisional_execution_projection": True,
        "Kanban_canonical_authority": False,
        "workflow_status": "queued",
        "queue_state": "kanban_projection_ready_not_dispatched",
        "execution_started": False,
        "worker_execution": False,
        "dispatch_performed": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "command_execution_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "next_action": record["next_action"],
        "authority": _projection_authority(record),
    }


def _require_projection_identity(
    record: dict[str, Any],
    generation: dict[str, Any],
    decision: dict[str, Any],
) -> None:
    required_role = _required_execution_profile_role(generation)
    expected = {
        "schema_version": WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION,
        "policy_id": WORK_PACKET_KANBAN_PROJECTION_POLICY_ID,
        "project_id": generation["project_id"],
        "macroproject_id": generation["macroproject_id"],
        "ticket_id": generation["ticket_id"],
        "ticket_title": generation["ticket_title"],
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "WorkPacket_compilation_count": generation["WorkPacket_compilation_count"],
        "approval_id": decision["approval_id"],
        "approval_status": "approved",
        "approval_decision": "approve",
        "approval_publication_SHA256": decision["approval_publication_SHA256"],
        "dependency_plan_SHA256": generation["dependency_plan_SHA256"],
        "dependency_admission_policy_id": DEPENDENCY_AWARE_QUEUE_POLICY_ID,
        "dependency_plan_reused": True,
        "dependency_planner_reused": True,
        "dependency_plan_recomputed_unnecessarily": False,
        "approval_bypass": False,
        "dependency_bypass": False,
        "provisional_execution_projection": True,
        "Kanban_canonical_authority": False,
        "kanban_board_slug": _KANBAN_BOARD,
        "workspace_kind": _WORKSPACE_KIND,
        "workspace_created": False,
        "workspace_allocation_count": 0,
        "profile_assignment_policy_id": PEPPER_EXECUTION_PROFILES_POLICY_ID,
        "profile_assignment_basis": "governed_role_taxonomy",
        "selection_rationale": "deterministic_single_governed_role_match",
        "profile_assignment_gap": False,
        "execution_profile_role": required_role,
        "selected_role": required_role,
        "profile_toolset_policy": "explicit_bounded_cli_toolsets",
        "lead_agent_auto_assigned": False,
        "ticket_architect_executor_distinct": True,
        "human_profile_selection_required": False,
        "concurrent_workers_for_ticket": _MAX_CONCURRENT_WORKERS_FOR_TICKET,
        "task_max_retries": _TASK_MAX_RETRIES,
        "dispatch_performed": False,
        "dispatcher_calls": 0,
        "worker_process_started": False,
        "worker_execution": False,
        "execution_started": False,
        "command_execution_count": 0,
        "provider_dispatch_count": 0,
        "model_inference_count": 0,
        "Git_commands_executed": 0,
        "Docker_commands_executed": 0,
        "Graphify_commands_executed": 0,
        "retry_execution_count": 0,
        "rollback_count": 0,
        "Paperclip_calls": 0,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise WorkPacketKanbanProjectionConflict(f"projection {key} mismatch")
    if record.get("profile_assignment_policy_revision") not in {
        None,
        PEPPER_EXECUTION_PROFILES_POLICY_REVISION,
    }:
        raise WorkPacketKanbanProjectionConflict("projection profile assignment revision mismatch")
    if not _SAFE_ID.fullmatch(str(record.get("kanban_task_id") or "")):
        raise WorkPacketKanbanProjectionConflict("projection Kanban task id is invalid")
    if record.get("selected_profile") != record.get("assignee_profile"):
        raise WorkPacketKanbanProjectionConflict("projection selected profile mismatch")
    if record.get("kanban_task_status") not in kanban_db.VALID_STATUSES:
        raise WorkPacketKanbanProjectionConflict("projection Kanban task status is invalid")
    admission = record.get("dependency_admission")
    if not isinstance(admission, dict):
        raise WorkPacketKanbanProjectionConflict("dependency admission is invalid")
    if admission.get("policy_id") != DEPENDENCY_AWARE_QUEUE_POLICY_ID:
        raise WorkPacketKanbanProjectionConflict("dependency admission policy mismatch")
    if admission.get("decision") != DependencyAwareQueueDecision.ADMIT.value:
        raise WorkPacketKanbanProjectionConflict("dependency admission must be admitted")
    if admission.get("queue_admitted") is not True:
        raise WorkPacketKanbanProjectionConflict("dependency admission must be queue_admitted")
    if record.get("task_skills") not in _accepted_task_skill_lists():
        raise WorkPacketKanbanProjectionConflict("projection task skills mismatch")
    requirements = _execution_profile_requirements(required_role)
    if record.get("profile_toolsets") != requirements["required_toolsets"]:
        raise WorkPacketKanbanProjectionConflict("projection profile toolsets mismatch")
    required_profile_toolsets = record.get("required_profile_toolsets")
    if (
        required_profile_toolsets is not None
        and required_profile_toolsets != requirements["required_toolsets"]
    ):
        raise WorkPacketKanbanProjectionConflict("projection required profile toolsets mismatch")
    required_write_toolsets = record.get("required_write_toolsets")
    if (
        required_write_toolsets is not None
        and required_write_toolsets != requirements["required_write_toolsets"]
    ):
        raise WorkPacketKanbanProjectionConflict("projection required write toolsets mismatch")


def _accepted_task_skill_lists() -> list[list[str]]:
    return [list(_TASK_SKILLS), list(_LEGACY_SEMANTIC_TASK_SKILLS)]


def _role_semantic_capabilities(role: str) -> list[str]:
    if role == _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE:
        return list(_PEPPER_IMPLEMENTATION_SEMANTIC_CAPABILITIES)
    return list(_PEPPER_SEMANTIC_CAPABILITIES)


def _role_capability_resolution(role: str) -> list[dict[str, Any]]:
    if role == _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE:
        return [dict(item) for item in _PEPPER_IMPLEMENTATION_CAPABILITY_RESOLUTION]
    return [dict(item) for item in _PEPPER_CAPABILITY_RESOLUTION]


def _role_required_capability_labels(role: str) -> list[str]:
    if role == _PEPPER_IMPLEMENTATION_EXECUTION_PROFILE_ROLE:
        return list(_PEPPER_IMPLEMENTATION_REQUIRED_CAPABILITY_LABELS)
    return list(_PEPPER_REQUIRED_CAPABILITY_LABELS)


def _capability_resolution(role: str = _PEPPER_EXECUTION_PROFILE_ROLE) -> list[dict[str, Any]]:
    return _role_capability_resolution(role)


def _persist_projection_record(record: dict[str, Any]) -> None:
    ticket_id = _safe_ticket_id(record.get("ticket_id"))
    path = kanban_projection_record_path_for_ticket(ticket_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = load_kanban_projection_record(ticket_id=ticket_id)
        if existing is not None:
            return
    tmp = path.with_suffix(path.suffix + ".tmp")
    serialized = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(path)


def _projection_authority(record: dict[str, Any]) -> dict[str, Any]:
    ticket_id = _safe_ticket_id(record.get("ticket_id"))
    path = kanban_projection_record_path_for_ticket(ticket_id)
    relative = path.relative_to(get_hermes_home())
    return {
        "authority_record": str(relative).replace("\\", "/"),
        "projection_SHA256": record["projection_SHA256"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_idempotency_key": record["kanban_task_idempotency_key"],
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "profile_assignment_policy_id": record["profile_assignment_policy_id"],
        "profile_assignment_policy_revision": record.get("profile_assignment_policy_revision"),
        "selection_rationale": record["selection_rationale"],
        "execution_profile_role": record["execution_profile_role"],
        "selected_role": record["selected_role"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "dependency_plan_SHA256": record["dependency_plan_SHA256"],
        "Kanban_canonical_authority": False,
        "provisional_execution_projection": True,
    }


def _idempotency_key(generation: dict[str, Any]) -> str:
    return ":".join((
        f"pepper:{_safe_ticket_id(generation['ticket_id'])}:workpacket-kanban-projection",
        generation["work_packet_id"],
        generation["work_packet_SHA256"],
    ))


def _projection_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "projection_SHA256"
    }
    encoded = json.dumps(
        {"algorithm": WORK_PACKET_KANBAN_PROJECTION_DIGEST_ALGORITHM, "record": _normalize(payload)},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalize(value: object) -> object:
    if isinstance(value, BaseModel):
        return _normalize(value.model_dump(mode="json", warnings=False))
    if isinstance(value, tuple | list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    return value


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


__all__ = (
    "WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION",
    "WORK_PACKET_KANBAN_PROJECTION_POLICY_ID",
    "PEPPER_EXECUTION_PROFILES_SCHEMA_VERSION",
    "PEPPER_EXECUTION_PROFILES_POLICY_ID",
    "PEPPER_EXECUTION_PROFILES_POLICY_REVISION",
    "PEPPER_EXECUTION_PROFILE_TAXONOMY",
    "WorkPacketKanbanProjectionError",
    "WorkPacketKanbanProjectionInputError",
    "WorkPacketKanbanProjectionConflict",
    "WorkPacketKanbanProjectionProfileGap",
    "WorkPacketKanbanProjectionProfileSelectionRequired",
    "WorkPacketKanbanProjectionBlocked",
    "kanban_projection_record_path",
    "kanban_projection_record_path_for_ticket",
    "load_kanban_projection_record",
    "load_p18_9_0_kanban_projection_record",
    "validate_kanban_projection_record",
    "validate_p18_9_0_kanban_projection_record",
    "resolve_current_approved_workpacket_projection",
    "project_current_approved_workpacket_to_kanban",
    "project_approved_p18_9_0_workpacket_to_kanban",
    "resolve_execution_profile_for_ticket",
    "resolve_p18_9_0_execution_profile",
    "classify_pepper_execution_profile",
    "execution_start_action_id",
    "kanban_projection_to_workflow_overlay",
)
