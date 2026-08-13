"""P18.9.0 approved WorkPacket to Hermes Kanban projection.

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
    CANONICAL_APPROVAL_ID,
    CANONICAL_MACROPROJECT_ID,
    CANONICAL_PROJECT_ID,
    CANONICAL_TICKET_ID,
    CANONICAL_TICKET_TITLE,
    load_p18_9_0_approval_decision_record,
    load_p18_9_0_generation_record,
    validate_p18_9_0_approval_decision_record,
    validate_p18_9_0_generation_record,
)
from hermes_cli.profiles import list_profiles, normalize_profile_name


WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION = 1
WORK_PACKET_KANBAN_PROJECTION_POLICY_ID = "pepper-workpacket-kanban-projection-v1"
PEPPER_EXECUTION_PROFILES_SCHEMA_VERSION = 1
PEPPER_EXECUTION_PROFILES_POLICY_ID = "pepper-execution-profiles-v1"
WORK_PACKET_KANBAN_PROJECTION_DIGEST_ALGORITHM = (
    "agent-platform-workpacket-kanban-projection-sha256-v1"
)

_STORE_LOCK = threading.Lock()
_STORE_DIR = Path("agent-platform") / "pepper-workpacket-kanban-projection"
_STORE_FILE = "P18.9.0.kanban-projection.json"
_KANBAN_BOARD = "default"
_IDEMPOTENCY_PREFIX = "pepper:P18.9.0:workpacket-kanban-projection"
_WORKSPACE_KIND = "scratch"
_TASK_SKILLS: tuple[str, ...] = ()
_LEGACY_SEMANTIC_TASK_SKILLS = ("codebase-inspection",)
_TASK_MAX_RETRIES = 1
_MAX_CONCURRENT_WORKERS_FOR_TICKET = 1
_PROFILE_TEXT_TOKEN = re.compile(r"[a-z0-9]+")
_PEPPER_EXECUTION_PROFILE_ROLE = "architecture_product"
_PEPPER_LEAD_AGENT_ROLE = "lead_agent"
_PEPPER_TICKET_ARCHITECT_ROLE = "ticket_architect"
_PEPPER_DEFAULT_PROFILE_ROLE = "default_control_profile"
_PEPPER_UNCLASSIFIED_PROFILE_ROLE = "unclassified"
_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS = ("pepper_repository",)
_PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS = ("no_mcp",)
_PEPPER_SEMANTIC_CAPABILITIES = ("codebase-inspection",)
_PEPPER_CAPABILITY_RESOLUTION_POLICY = "semantic_capability_to_profile_toolset"
_PEPPER_CAPABILITY_RESOLUTION = (
    {
        "semantic_capability": "codebase-inspection",
        "resolved_surface": "profile_toolset",
        "toolset": "pepper_repository",
        "hermes_task_skill": None,
    },
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
}
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class WorkPacketKanbanProjectionError(ValueError):
    """Base error for P18.9.0 WorkPacket/Kanban projection failures."""


class WorkPacketKanbanProjectionInputError(WorkPacketKanbanProjectionError):
    """Raised when caller-supplied projection guards are malformed."""


class WorkPacketKanbanProjectionConflict(WorkPacketKanbanProjectionError):
    """Raised when existing projection authority or task mapping conflicts."""


class WorkPacketKanbanProjectionProfileGap(WorkPacketKanbanProjectionError):
    """Raised when no existing Hermes profile can own the projected task."""


class WorkPacketKanbanProjectionProfileSelectionRequired(
    WorkPacketKanbanProjectionProfileGap
):
    """Raised when multiple governed execution profiles could own the task."""


class WorkPacketKanbanProjectionBlocked(WorkPacketKanbanProjectionError):
    """Raised when dependency admission blocks projection."""


def kanban_projection_record_path() -> Path:
    """Return the profile-scoped P18.9.0 Kanban projection authority path."""

    return get_hermes_home() / _STORE_DIR / _STORE_FILE


def load_p18_9_0_kanban_projection_record(
    *,
    generation_record: dict[str, Any] | None = None,
    decision_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load and validate the persisted P18.9.0 Kanban projection, if present."""

    path = kanban_projection_record_path()
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkPacketKanbanProjectionConflict(
            "P18.9.0 Kanban projection record is unreadable"
        ) from exc
    return validate_p18_9_0_kanban_projection_record(
        record,
        generation_record=generation_record,
        decision_record=decision_record,
    )


def validate_p18_9_0_kanban_projection_record(
    record: dict[str, Any],
    *,
    generation_record: dict[str, Any] | None = None,
    decision_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate projection mapping without touching dispatcher or execution."""

    if not isinstance(record, dict):
        raise WorkPacketKanbanProjectionConflict("Kanban projection record must be an object")
    if record.get("projection_SHA256") != _projection_record_digest(record):
        raise WorkPacketKanbanProjectionConflict("Kanban projection record digest mismatch")
    generation = (
        validate_p18_9_0_generation_record(generation_record)
        if generation_record is not None
        else load_p18_9_0_generation_record()
    )
    if generation is None:
        raise WorkPacketKanbanProjectionConflict("projection has no generated WorkPacket authority")
    decision = (
        validate_p18_9_0_approval_decision_record(
            decision_record,
            generation_record=generation,
        )
        if decision_record is not None
        else load_p18_9_0_approval_decision_record(generation_record=generation)
    )
    if decision is None:
        raise WorkPacketKanbanProjectionConflict("projection has no approval decision authority")
    _require_projection_identity(record, generation, decision)
    return record


def project_approved_p18_9_0_workpacket_to_kanban(
    *,
    workflow: dict[str, Any],
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    """Project the approved P18.9.0 WorkPacket into Hermes Kanban without dispatch."""

    _validate_requested_identity(
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
    )
    with _STORE_LOCK:
        generation = load_p18_9_0_generation_record()
        if generation is None:
            raise WorkPacketKanbanProjectionConflict("P18.9.0 has no generated WorkPacket")
        decision = load_p18_9_0_approval_decision_record(generation_record=generation)
        if decision is None or decision.get("decision") != "approve":
            raise WorkPacketKanbanProjectionConflict("P18.9.0 is not approved")
        existing = load_p18_9_0_kanban_projection_record(
            generation_record=generation,
            decision_record=decision,
        )
        if existing is not None:
            _require_existing_task_matches(existing)
            return _operational_result(existing, idempotent_replay=True)

        _validate_workflow_eligibility(workflow)
        dependency_plan = TicketDependencyPlan.model_validate(generation["dependency_plan"])
        admission = derive_dependency_queue_admission_for_ticket(
            dependency_plan=dependency_plan,
            ticket_id=CANONICAL_TICKET_ID,
        )
        if admission["decision"] != DependencyAwareQueueDecision.ADMIT.value:
            raise WorkPacketKanbanProjectionBlocked("DEPENDENCY_ADMISSION_BLOCKED")
        profile = resolve_p18_9_0_execution_profile()
        transitions = _build_projection_transitions(decision, admission)
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
        validate_p18_9_0_kanban_projection_record(
            record,
            generation_record=generation,
            decision_record=decision,
        )
        _persist_projection_record(record)
    return _operational_result(record, idempotent_replay=False)


def resolve_p18_9_0_execution_profile() -> dict[str, Any]:
    """Resolve the existing governed Hermes assignee for P18.9.0."""

    try:
        profiles = list_profiles()
    except Exception as exc:
        raise WorkPacketKanbanProjectionProfileGap("PROFILE_ASSIGNMENT_GAP") from exc
    roster = [classify_pepper_execution_profile(profile) for profile in profiles]
    if not roster:
        raise WorkPacketKanbanProjectionProfileGap("PROFILE_ASSIGNMENT_GAP")
    candidates = [
        item for item in roster
        if item["role"] == _PEPPER_EXECUTION_PROFILE_ROLE
        and item["worker_assignable"] is True
    ]
    if len(candidates) > 1:
        raise WorkPacketKanbanProjectionProfileSelectionRequired(
            "HUMAN_PROFILE_SELECTION_REQUIRED"
        )
    if candidates:
        selected = candidates[0]
        return {
            "assignee_profile": selected["canonical_name"],
            "selected_profile": selected["canonical_name"],
            "profile_assignment_policy_id": PEPPER_EXECUTION_PROFILES_POLICY_ID,
            "profile_assignment_basis": "governed_role_taxonomy",
            "selection_rationale": "deterministic_single_governed_role_match",
            "candidate_profiles": [item["canonical_name"] for item in candidates],
            "profile_assignment_gap": False,
            "execution_profile_role": _PEPPER_EXECUTION_PROFILE_ROLE,
            "selected_role": _PEPPER_EXECUTION_PROFILE_ROLE,
            "profile_classification_basis": selected["classification_basis"],
            "profile_toolsets": selected["cli_toolsets"],
            "profile_toolset_policy": "explicit_bounded_cli_toolsets",
            "lead_agent_auto_assigned": False,
            "ticket_architect_executor_distinct": True,
            "human_profile_selection_required": False,
            "available_profiles": roster,
        }
    raise WorkPacketKanbanProjectionProfileGap("PROFILE_ASSIGNMENT_GAP")


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
    else:
        role = _PEPPER_UNCLASSIFIED_PROFILE_ROLE
        basis = "no_matching_execution_role_terms"

    toolset_policy = _profile_toolset_policy(profile)
    rejection_reasons: list[str] = []
    if role != _PEPPER_EXECUTION_PROFILE_ROLE:
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
            role == _PEPPER_EXECUTION_PROFILE_ROLE
            and toolset_policy["bounded"] is True
        ),
        "cli_toolsets": toolset_policy["cli_toolsets"],
        "toolset_source": toolset_policy["source"],
        "toolset_bounded": toolset_policy["bounded"],
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


def _profile_toolset_policy(profile: Any) -> dict[str, Any]:
    raw_toolsets, source = _profile_explicit_cli_toolsets(profile)
    normalized = tuple(
        str(toolset).strip()
        for toolset in raw_toolsets
        if str(toolset).strip()
    )
    actual = tuple(dict.fromkeys(
        toolset for toolset in normalized
        if toolset not in _PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS
    ))
    violations: list[str] = []
    if source is None:
        violations.append("explicit_cli_toolsets_required")
    missing = sorted(set(_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS) - set(actual))
    if missing:
        violations.append("missing_required_toolsets:" + ",".join(missing))
    extra = sorted(set(actual) - set(_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS))
    if extra:
        violations.append("unbounded_toolsets:" + ",".join(extra))
    missing_sentinels = sorted(
        set(_PEPPER_EXECUTION_PROFILE_REQUIRED_SENTINELS) - set(normalized)
    )
    if missing_sentinels:
        violations.append("missing_required_sentinels:" + ",".join(missing_sentinels))
    if _profile_uses_nondefault_context_engine(profile):
        violations.append("nondefault_context_engine_not_bounded")
    if _profile_disables_required_toolsets(profile):
        violations.append("required_toolset_disabled")
    return {
        "source": source,
        "cli_toolsets": list(actual),
        "bounded": not violations,
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


def _profile_disables_required_toolsets(profile: Any) -> bool:
    config = _read_profile_config(profile)
    agent = config.get("agent") if isinstance(config, dict) else None
    if not isinstance(agent, dict):
        return False
    disabled = agent.get("disabled_toolsets") or []
    if not isinstance(disabled, list):
        return False
    return bool(
        set(_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS) & {str(item) for item in disabled}
    )


def kanban_projection_to_workflow_overlay(record: dict[str, Any]) -> dict[str, Any]:
    """Return workflow-control fields implied by a validated Kanban projection."""

    validated = validate_p18_9_0_kanban_projection_record(record)
    return {
        "readiness": "queued_not_executing",
        "workflow_state": "P18.9.0-QUEUED-NOT-EXECUTING",
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
        "selection_rationale": validated["selection_rationale"],
        "execution_profile_role": validated["execution_profile_role"],
        "selected_role": validated["selected_role"],
        "profile_toolsets": validated["profile_toolsets"],
        "lead_agent_auto_assigned": validated["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": validated["ticket_architect_executor_distinct"],
        "next_action": {
            "id": "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            "label": (
                "P18.9.0 is projected to Kanban and ready for a separate explicit "
                "human authorization to start execution."
            ),
            "target_ticket_id": CANONICAL_TICKET_ID,
            "target_ticket_title": CANONICAL_TICKET_TITLE,
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
    if requested_project_id not in {None, "", CANONICAL_PROJECT_ID}:
        raise WorkPacketKanbanProjectionInputError("requested project is not PEPPER")
    if requested_ticket_id not in {None, "", CANONICAL_TICKET_ID}:
        raise WorkPacketKanbanProjectionInputError("requested ticket is not P18.9.0")
    if requested_next_action_id not in {None, "", "P18_9_0_APPROVED_NO_EXECUTION"}:
        raise WorkPacketKanbanProjectionInputError(
            "requested next action is not P18_9_0_APPROVED_NO_EXECUTION"
        )


def _validate_workflow_eligibility(workflow: dict[str, Any]) -> None:
    if not isinstance(workflow, dict):
        raise WorkPacketKanbanProjectionInputError("workflow state is unavailable")
    if workflow.get("project_id") != CANONICAL_PROJECT_ID:
        raise WorkPacketKanbanProjectionInputError("active governed project is not PEPPER")
    if workflow.get("macroproject_id") != CANONICAL_MACROPROJECT_ID:
        raise WorkPacketKanbanProjectionInputError("active macroproject is not P18.9")
    if workflow.get("current_ticket_id") != CANONICAL_TICKET_ID:
        raise WorkPacketKanbanProjectionInputError("active ticket is not P18.9.0")
    if workflow.get("workflow_status") != "ticket_approved":
        raise WorkPacketKanbanProjectionInputError("P18.9.0 is not ticket_approved")
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        raise WorkPacketKanbanProjectionInputError("next action is unavailable")
    if next_action.get("id") != "P18_9_0_APPROVED_NO_EXECUTION":
        raise WorkPacketKanbanProjectionInputError("next action is not projection preparation")
    if next_action.get("target_ticket_id") != CANONICAL_TICKET_ID:
        raise WorkPacketKanbanProjectionInputError("next action does not target P18.9.0")


def _build_projection_transitions(
    decision: dict[str, Any],
    admission: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
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
            board_or_queue_id="P18.9.0-kanban-projection",
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
            title=f"{CANONICAL_TICKET_ID} {CANONICAL_TICKET_TITLE}",
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
    if payload.get("ticket_id") != CANONICAL_TICKET_ID:
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
    record = {
        "schema_version": WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION,
        "policy_id": WORK_PACKET_KANBAN_PROJECTION_POLICY_ID,
        "created_at": _utc_now_iso(),
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "WorkPacket_compilation_count": generation["WorkPacket_compilation_count"],
        "approval_id": CANONICAL_APPROVAL_ID,
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
        "profile_assignment_basis": profile["profile_assignment_basis"],
        "selection_rationale": profile["selection_rationale"],
        "candidate_profiles": profile["candidate_profiles"],
        "profile_assignment_gap": profile["profile_assignment_gap"],
        "execution_profile_role": profile["execution_profile_role"],
        "selected_role": profile["selected_role"],
        "profile_classification_basis": profile["profile_classification_basis"],
        "profile_toolsets": profile["profile_toolsets"],
        "profile_toolset_policy": profile["profile_toolset_policy"],
        "lead_agent_auto_assigned": profile["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": profile["ticket_architect_executor_distinct"],
        "human_profile_selection_required": profile["human_profile_selection_required"],
        "concurrent_workers_for_ticket": _MAX_CONCURRENT_WORKERS_FOR_TICKET,
        "task_max_retries": _TASK_MAX_RETRIES,
        "task_skills": list(_TASK_SKILLS),
        "semantic_capabilities": list(_PEPPER_SEMANTIC_CAPABILITIES),
        "capability_resolution_policy": _PEPPER_CAPABILITY_RESOLUTION_POLICY,
        "capability_resolution": _capability_resolution(),
        "required_capability_labels": [
            "codebase-inspection",
            "governed repository read",
            "architecture and product analysis",
            "Ticket/IA documentation authority",
        ],
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
            "id": "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            "target_ticket_id": CANONICAL_TICKET_ID,
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
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "TicketSpec_SHA256": generation["ticket_spec_SHA256"],
        "WorkPacket_ID": generation["work_packet_id"],
        "WorkPacket_SHA256": generation["work_packet_SHA256"],
        "approval_id": CANONICAL_APPROVAL_ID,
        "approval_publication_SHA256": decision["approval_publication_SHA256"],
        "dependency_plan_SHA256": generation["dependency_plan_SHA256"],
        "dependency_admission_policy_id": DEPENDENCY_AWARE_QUEUE_POLICY_ID,
        "dependency_admission_decision": admission["decision"],
        "assignee_profile": profile["assignee_profile"],
        "selected_profile": profile["selected_profile"],
        "profile_assignment_policy_id": profile["profile_assignment_policy_id"],
        "profile_assignment_basis": profile["profile_assignment_basis"],
        "selection_rationale": profile["selection_rationale"],
        "execution_profile_role": profile["execution_profile_role"],
        "selected_role": profile["selected_role"],
        "profile_toolsets": profile["profile_toolsets"],
        "profile_toolset_policy": profile["profile_toolset_policy"],
        "lead_agent_auto_assigned": profile["lead_agent_auto_assigned"],
        "ticket_architect_executor_distinct": profile["ticket_architect_executor_distinct"],
        "concurrent_workers_for_ticket": _MAX_CONCURRENT_WORKERS_FOR_TICKET,
        "task_max_retries": _TASK_MAX_RETRIES,
        "task_skills": list(_TASK_SKILLS),
        "semantic_capabilities": list(_PEPPER_SEMANTIC_CAPABILITIES),
        "capability_resolution_policy": _PEPPER_CAPABILITY_RESOLUTION_POLICY,
        "capability_resolution": _capability_resolution(),
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
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "WorkPacket_compilation_count": record["WorkPacket_compilation_count"],
        "dependency_admission": record["dependency_admission"],
        "kanban_board_slug": record["kanban_board_slug"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_status": record["kanban_task_status"],
        "duplicate_task": False,
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "profile_assignment_policy_id": record["profile_assignment_policy_id"],
        "profile_assignment_basis": record["profile_assignment_basis"],
        "selection_rationale": record["selection_rationale"],
        "execution_profile_role": record["execution_profile_role"],
        "selected_role": record["selected_role"],
        "profile_toolsets": record["profile_toolsets"],
        "profile_toolset_policy": record["profile_toolset_policy"],
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
    expected = {
        "schema_version": WORK_PACKET_KANBAN_PROJECTION_SCHEMA_VERSION,
        "policy_id": WORK_PACKET_KANBAN_PROJECTION_POLICY_ID,
        "project_id": CANONICAL_PROJECT_ID,
        "macroproject_id": CANONICAL_MACROPROJECT_ID,
        "ticket_id": CANONICAL_TICKET_ID,
        "ticket_title": CANONICAL_TICKET_TITLE,
        "ticket_spec_SHA256": generation["ticket_spec_SHA256"],
        "work_packet_id": generation["work_packet_id"],
        "work_packet_SHA256": generation["work_packet_SHA256"],
        "WorkPacket_compilation_count": 1,
        "approval_id": CANONICAL_APPROVAL_ID,
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
        "execution_profile_role": _PEPPER_EXECUTION_PROFILE_ROLE,
        "selected_role": _PEPPER_EXECUTION_PROFILE_ROLE,
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
    if record.get("profile_toolsets") != list(_PEPPER_EXECUTION_PROFILE_REQUIRED_TOOLSETS):
        raise WorkPacketKanbanProjectionConflict("projection profile toolsets mismatch")


def _accepted_task_skill_lists() -> list[list[str]]:
    return [list(_TASK_SKILLS), list(_LEGACY_SEMANTIC_TASK_SKILLS)]


def _capability_resolution() -> list[dict[str, Any]]:
    return [dict(item) for item in _PEPPER_CAPABILITY_RESOLUTION]


def _persist_projection_record(record: dict[str, Any]) -> None:
    path = kanban_projection_record_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = load_p18_9_0_kanban_projection_record()
        if existing is not None:
            return
    tmp = path.with_suffix(path.suffix + ".tmp")
    serialized = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(path)


def _projection_authority(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_record": str(_STORE_DIR / _STORE_FILE).replace("\\", "/"),
        "projection_SHA256": record["projection_SHA256"],
        "kanban_task_id": record["kanban_task_id"],
        "kanban_task_idempotency_key": record["kanban_task_idempotency_key"],
        "assignee_profile": record["assignee_profile"],
        "selected_profile": record["selected_profile"],
        "profile_assignment_policy_id": record["profile_assignment_policy_id"],
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
        _IDEMPOTENCY_PREFIX,
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
    "PEPPER_EXECUTION_PROFILE_TAXONOMY",
    "WorkPacketKanbanProjectionError",
    "WorkPacketKanbanProjectionInputError",
    "WorkPacketKanbanProjectionConflict",
    "WorkPacketKanbanProjectionProfileGap",
    "WorkPacketKanbanProjectionProfileSelectionRequired",
    "WorkPacketKanbanProjectionBlocked",
    "kanban_projection_record_path",
    "load_p18_9_0_kanban_projection_record",
    "validate_p18_9_0_kanban_projection_record",
    "project_approved_p18_9_0_workpacket_to_kanban",
    "resolve_p18_9_0_execution_profile",
    "classify_pepper_execution_profile",
    "kanban_projection_to_workflow_overlay",
)
