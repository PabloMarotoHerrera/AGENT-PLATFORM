"""Governed Pepper Ticket Architect bridge.

This module turns the current Pepper next action into canonical P16/P17/P18
evidence. It does not call providers, dispatch workers, create Kanban tasks,
run commands, mutate Git, invoke Docker, or invoke Graphify.
"""

from __future__ import annotations

from dataclasses import dataclass
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
TICKET_ARCHITECT_RECONCILIATION_DIGEST_ALGORITHM = (
    "agent-platform-ticket-architect-stale-authority-reconciliation-sha256-v1"
)
TICKET_ARCHITECT_CONTRACT_DIGEST_ALGORITHM = (
    "agent-platform-ticket-architect-roadmap-contract-sha256-v1"
)

CANONICAL_PROJECT_ID = "PEPPER"
CANONICAL_PROJECT_NAME = "Pepper"
CANONICAL_MACROPROJECT_ID = "P18.9"
CANONICAL_MACROPROJECT_TITLE = "Pepper Product Personalization"
CANONICAL_TICKET_ID = "P18.9.0"
CANONICAL_TICKET_TITLE = "Product Inventory, IA Decision, and Acceptance Contract"
CANONICAL_NEXT_ACTION_ID = "GENERATE_P18_9_0"
CANONICAL_ROADMAP_AUTHORITY = "human-approved-p18.9-roadmap"
CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY = "accepted-p18.9-implementation-roadmap"
CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH = (
    "0_architecture/governance/agent_platform_roadmap_generation_work_breakdown_contract.md"
)
CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_SECTION = (
    "P18.9 Implementation Roadmap Authority"
)
CANONICAL_ROADMAP_AUTHORITY_PATH = (
    "2_products/pepper-agent/docs/agent-platform/workflow_migration_closure.md"
)
CANONICAL_ROADMAP_AUTHORITY_SECTION = (
    "Advisory decomposition only, not implementation tickets"
)
CANONICAL_WORKFLOW_PROJECT_ID = "P18.9"
CANONICAL_WORKFLOW_TICKET_ID = "P18.9"
HUMAN_APPROVAL_NEXT_ACTION_ID = "APPROVE_P18_9_0"
CANONICAL_APPROVAL_ID = "P18.9.0"

_STORE_DIR = Path("agent-platform") / "pepper-ticket-architect-bridge"
_APPROVAL_DECISION_STORE_FILE = "P18.9.0.approval-decision.json"
_RECONCILIATION_STORE_DIR = _STORE_DIR / "reconciliation-history"
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
_CONTRACT_LIST_FIELDS = frozenset(
    (
        "context",
        "predecessor_evidence",
        "dependency_context",
        "information_architecture",
        "required_surfaces",
        "allowed_paths",
        "forbidden_paths",
        "allowed_actions",
        "forbidden_actions",
        "constraints",
        "non_goals",
        "risk",
        "tasks",
        "acceptance_criteria",
        "expected_artifacts",
        "validation_steps",
        "required_response_sections",
    )
)
_CONTRACT_SINGLE_FIELDS = frozenset(
    (
        "ticket_type",
        "objective",
        "parallelization_hint",
        "completion_verdict",
        "recommended_commit_message",
    )
)


@dataclass(frozen=True)
class GovernedTicketGenerationTarget:
    """Single canonical next governed ticket resolved from workflow authority."""

    project_id: str
    project_name: str
    macroproject_id: str
    macroproject_title: str
    ticket_id: str
    ticket_title: str
    next_action_id: str
    approval_next_action_id: str
    approved_no_execution_next_action_id: str
    revise_next_action_id: str
    canonical_roadmap_authority: str
    roadmap_authority_path: str
    roadmap_authority_section: str
    dependency_ticket_ids: tuple[str, ...] = ()
    predecessor_ticket_id: str | None = None
    readiness_state: str | None = None
    authority_source: str | None = None
    ticket_contract: dict[str, Any] | None = None

    @property
    def action_token(self) -> str:
        return _ticket_action_token(self.ticket_id)

    @property
    def idempotency_key(self) -> str:
        return f"{self.project_id}:{self.macroproject_id}:{self.ticket_id}:{self.next_action_id}"


@dataclass(frozen=True)
class CanonicalNextTicketAuthority:
    """Canonical next governed ticket resolved from workflow and roadmap authority."""

    project_id: str
    project_name: str
    macroproject_id: str
    macroproject_title: str
    ticket_id: str
    ticket_title: str
    next_action_id: str
    canonical_roadmap_authority: str
    roadmap_authority_path: str
    roadmap_authority_section: str
    dependency_ticket_ids: tuple[str, ...]
    predecessor_ticket_id: str | None
    readiness_state: str
    authority_source: str
    ticket_contract: dict[str, Any] | None = None

    def generation_target(self) -> GovernedTicketGenerationTarget:
        return GovernedTicketGenerationTarget(
            project_id=self.project_id,
            project_name=self.project_name,
            macroproject_id=self.macroproject_id,
            macroproject_title=self.macroproject_title,
            ticket_id=self.ticket_id,
            ticket_title=self.ticket_title,
            next_action_id=self.next_action_id,
            approval_next_action_id=approval_action_id(self.ticket_id),
            approved_no_execution_next_action_id=approved_no_execution_action_id(self.ticket_id),
            revise_next_action_id=revise_action_id(self.ticket_id),
            canonical_roadmap_authority=self.canonical_roadmap_authority,
            roadmap_authority_path=canonical_roadmap_authority_path(self.roadmap_authority_path),
            roadmap_authority_section=self.roadmap_authority_section,
            dependency_ticket_ids=self.dependency_ticket_ids,
            predecessor_ticket_id=self.predecessor_ticket_id,
            readiness_state=self.readiness_state,
            authority_source=self.authority_source,
            ticket_contract=self.ticket_contract,
        )

    def asdict(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "macroproject_id": self.macroproject_id,
            "macroproject_title": self.macroproject_title,
            "ticket_id": self.ticket_id,
            "ticket_title": self.ticket_title,
            "next_action_id": self.next_action_id,
            "canonical_roadmap_authority": self.canonical_roadmap_authority,
            "roadmap_authority_path": self.roadmap_authority_path,
            "roadmap_authority_section": self.roadmap_authority_section,
            "dependency_ticket_ids": list(self.dependency_ticket_ids),
            "predecessor_ticket_id": self.predecessor_ticket_id,
            "readiness_state": self.readiness_state,
            "authority_source": self.authority_source,
        }
        if self.ticket_contract:
            record["ticket_contract"] = _json_ready_contract(self.ticket_contract)
            record["ticket_contract_SHA256"] = _ticket_contract_digest(self.ticket_contract)
        return record


def generation_action_id(ticket_id: str) -> str:
    """Return the governed generation action id for a ticket id."""

    return f"GENERATE_{_ticket_action_token(ticket_id)}"


def is_generation_action_id_for_ticket(action_id: str, ticket_id: str) -> bool:
    """Return true when an action id is the canonical generation vocabulary."""

    prefix = generation_action_id(ticket_id)
    candidate = str(action_id or "").strip()
    return candidate == prefix or candidate.startswith(prefix + "_")


def canonical_generation_action_id(ticket_id: str) -> str:
    return f"{generation_action_id(ticket_id)}_REQUIRES_SEPARATE_HUMAN_ACTION"


def canonical_roadmap_authority_path(value: object) -> str:
    """Return the persisted roadmap-authority path in repository-relative form."""

    candidate = str(value or "").strip().replace("\\", "/")
    while candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate:
        raise TicketArchitectBridgeInputError("roadmap authority path is unavailable")
    return candidate


def approval_action_id(ticket_id: str) -> str:
    return f"APPROVE_{_ticket_action_token(ticket_id)}"


def approved_no_execution_action_id(ticket_id: str) -> str:
    return f"{_ticket_action_token(ticket_id)}_APPROVED_NO_EXECUTION"


def revise_action_id(ticket_id: str) -> str:
    return f"REVISE_{_ticket_action_token(ticket_id)}"


def p18_9_0_generation_target() -> GovernedTicketGenerationTarget:
    """Return the historical P18.9.0 target used by compatibility wrappers."""

    return GovernedTicketGenerationTarget(
        project_id=CANONICAL_PROJECT_ID,
        project_name=CANONICAL_PROJECT_NAME,
        macroproject_id=CANONICAL_MACROPROJECT_ID,
        macroproject_title=CANONICAL_MACROPROJECT_TITLE,
        ticket_id=CANONICAL_TICKET_ID,
        ticket_title=CANONICAL_TICKET_TITLE,
        next_action_id=CANONICAL_NEXT_ACTION_ID,
        approval_next_action_id=HUMAN_APPROVAL_NEXT_ACTION_ID,
        approved_no_execution_next_action_id=approved_no_execution_action_id(CANONICAL_TICKET_ID),
        revise_next_action_id=revise_action_id(CANONICAL_TICKET_ID),
        canonical_roadmap_authority=CANONICAL_ROADMAP_AUTHORITY,
        roadmap_authority_path=CANONICAL_ROADMAP_AUTHORITY_PATH,
        roadmap_authority_section=CANONICAL_ROADMAP_AUTHORITY_SECTION,
        dependency_ticket_ids=(),
    )


def _target_from_record(record: dict[str, Any]) -> GovernedTicketGenerationTarget:
    ticket_id = _safe_ticket_id(record.get("ticket_id"))
    if ticket_id == CANONICAL_TICKET_ID:
        return p18_9_0_generation_target()
    authority = resolve_roadmap_ticket_authority(ticket_id)
    canonical_authority = record.get("canonical_next_ticket_authority")
    if not isinstance(canonical_authority, dict):
        canonical_authority = {}
    return GovernedTicketGenerationTarget(
        project_id=str(record.get("project_id") or CANONICAL_PROJECT_ID),
        project_name=str(record.get("project_name") or CANONICAL_PROJECT_NAME),
        macroproject_id=str(record.get("macroproject_id") or CANONICAL_MACROPROJECT_ID),
        macroproject_title=str(record.get("macroproject_title") or CANONICAL_MACROPROJECT_TITLE),
        ticket_id=ticket_id,
        ticket_title=str(authority["ticket_title"]),
        next_action_id=str(
            authority.get("next_action_id")
            or canonical_generation_action_id(ticket_id)
        ),
        approval_next_action_id=approval_action_id(ticket_id),
        approved_no_execution_next_action_id=approved_no_execution_action_id(ticket_id),
        revise_next_action_id=revise_action_id(ticket_id),
        canonical_roadmap_authority=str(authority["authority_type"]),
        roadmap_authority_path=canonical_roadmap_authority_path(authority["authority_path"]),
        roadmap_authority_section=str(authority["authority_section"]),
        dependency_ticket_ids=tuple(authority.get("dependency_ticket_ids") or ()),
        predecessor_ticket_id=str(record.get("predecessor_ticket_id") or "") or None,
        readiness_state=str(canonical_authority.get("readiness_state") or "") or None,
        authority_source=str(canonical_authority.get("authority_source") or "") or None,
        ticket_contract=_contract_from_authority_item(authority),
    )


def resolve_generation_target_from_workflow(
    workflow: dict[str, Any],
) -> GovernedTicketGenerationTarget:
    """Resolve the canonical next-ticket generation target from workflow state."""

    return resolve_canonical_next_ticket(workflow).generation_target()


def resolve_canonical_next_ticket(
    workflow: dict[str, Any] | None = None,
    *,
    roadmap_items: tuple[dict[str, Any], ...] | None = None,
) -> CanonicalNextTicketAuthority:
    """Resolve the single canonical next governed ticket from current authority."""

    state = workflow or {}
    if workflow is not None and not isinstance(workflow, dict):
        raise TicketArchitectBridgeInputError("workflow state is unavailable")

    items = roadmap_items if roadmap_items is not None else resolve_roadmap_ticket_authorities()
    if not items:
        raise TicketArchitectBridgeInputError("roadmap authority cannot resolve target")

    predecessor_ticket_id = _closed_predecessor_ticket_id(state)
    next_ticket_id = str(state.get("next_ticket_id") or "").strip()
    authority_source = "historical_bootstrap_roadmap_default"
    readiness_state = "bootstrap_ready"

    if predecessor_ticket_id:
        derived = _roadmap_successor_ticket_id(predecessor_ticket_id, items)
        if not derived:
            raise TicketArchitectBridgeInputError("roadmap authority cannot resolve successor")
        if next_ticket_id and next_ticket_id not in {derived, predecessor_ticket_id}:
            raise TicketArchitectBridgeInputError(
                "workflow next ticket conflicts with closed predecessor roadmap successor"
            )
        next_ticket_id = derived
        authority_source = "accepted_closed_workflow_state+canonical_roadmap"
        readiness_state = "closed_predecessor_next_ticket_ready"
    elif next_ticket_id:
        _require_workflow_generation_action(state, next_ticket_id)
        authority_source = "workflow_control_next_ticket"
        readiness_state = str(
            state.get("readiness")
            or state.get("workflow_status")
            or "workflow_next_ticket_ready"
        )
    elif _has_active_governed_ticket(state):
        raise TicketArchitectBridgeInputError("no next governed ticket is available")
    else:
        next_ticket_id = str(items[0]["ticket_id"])

    authority = _roadmap_item_for_ticket(next_ticket_id, items)
    _require_workflow_generation_action(
        state,
        next_ticket_id,
        stale_predecessor_ticket_id=predecessor_ticket_id,
    )
    macroproject_id = str(state.get("macroproject_id") or CANONICAL_MACROPROJECT_ID)
    macroproject_title = str(state.get("macroproject_title") or CANONICAL_MACROPROJECT_TITLE)
    next_action_id = _canonical_workflow_generation_action_id(
        state,
        next_ticket_id,
        fallback=str(authority.get("next_action_id") or canonical_generation_action_id(next_ticket_id)),
        stale_predecessor_ticket_id=predecessor_ticket_id,
    )
    return CanonicalNextTicketAuthority(
        project_id=str(state.get("project_id") or CANONICAL_PROJECT_ID),
        project_name=str(state.get("project_name") or CANONICAL_PROJECT_NAME),
        macroproject_id=macroproject_id,
        macroproject_title=macroproject_title,
        ticket_id=next_ticket_id,
        ticket_title=str(authority["ticket_title"]),
        next_action_id=next_action_id,
        canonical_roadmap_authority=str(authority["authority_type"]),
        roadmap_authority_path=canonical_roadmap_authority_path(authority["authority_path"]),
        roadmap_authority_section=str(authority["authority_section"]),
        dependency_ticket_ids=tuple(authority.get("dependency_ticket_ids") or ()),
        predecessor_ticket_id=predecessor_ticket_id,
        readiness_state=readiness_state,
        authority_source=authority_source,
        ticket_contract=_contract_from_authority_item(authority),
    )


def _has_active_governed_ticket(workflow: dict[str, Any]) -> bool:
    return bool(str(workflow.get("current_ticket_id") or "").strip())


def _closed_predecessor_ticket_id(workflow: dict[str, Any]) -> str | None:
    if not workflow:
        return None
    explicit = str(workflow.get("closed_predecessor_ticket_id") or "").strip()
    if explicit:
        return _safe_ticket_id(explicit)
    review_acceptance = workflow.get("review_acceptance_authority")
    if (
        isinstance(review_acceptance, dict)
        and review_acceptance.get("ticket_closed") is True
        and workflow.get("P18_9_0_closed") is True
    ):
        return CANONICAL_TICKET_ID
    if workflow.get("P18_9_0_closed") is True and workflow.get("P18_9_0_completed") is True:
        return CANONICAL_TICKET_ID
    if workflow.get("workflow_status") == "completed" and workflow.get("workflow_state") == "P18.9.0-COMPLETED":
        return CANONICAL_TICKET_ID
    return None


def _workflow_next_action_id(workflow: dict[str, Any]) -> str | None:
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        return None
    return str(next_action.get("id") or "").strip() or None


def _require_workflow_generation_action(
    workflow: dict[str, Any],
    ticket_id: str,
    *,
    stale_predecessor_ticket_id: str | None = None,
) -> None:
    if not workflow:
        return
    action_id = _workflow_next_action_id(workflow)
    if not action_id:
        return
    if not is_generation_action_id_for_ticket(action_id, ticket_id):
        if stale_predecessor_ticket_id and is_generation_action_id_for_ticket(
            action_id,
            stale_predecessor_ticket_id,
        ):
            return
        raise TicketArchitectBridgeInputError("next action is not the canonical generation action")
    next_action = workflow.get("next_action")
    if isinstance(next_action, dict):
        target_ticket_id = str(next_action.get("target_ticket_id") or "").strip()
        allowed_targets = {ticket_id}
        if stale_predecessor_ticket_id:
            allowed_targets.add(stale_predecessor_ticket_id)
        if target_ticket_id and target_ticket_id not in allowed_targets:
            raise TicketArchitectBridgeInputError("next action does not target canonical next ticket")


def _canonical_workflow_generation_action_id(
    workflow: dict[str, Any],
    ticket_id: str,
    *,
    fallback: str,
    stale_predecessor_ticket_id: str | None = None,
) -> str:
    action_id = _workflow_next_action_id(workflow)
    if action_id and is_generation_action_id_for_ticket(action_id, ticket_id):
        return action_id
    if (
        action_id
        and stale_predecessor_ticket_id
        and is_generation_action_id_for_ticket(action_id, stale_predecessor_ticket_id)
    ):
        return fallback
    return fallback


def _roadmap_successor_ticket_id(
    predecessor_ticket_id: str,
    items: tuple[dict[str, Any], ...],
) -> str | None:
    for index, item in enumerate(items):
        if item["ticket_id"] != predecessor_ticket_id:
            continue
        if index + 1 >= len(items):
            return None
        return str(items[index + 1]["ticket_id"])
    return None


def _roadmap_predecessor_ticket_id(
    ticket_id: str,
    items: tuple[dict[str, Any], ...],
) -> str | None:
    requested = _safe_ticket_id(ticket_id)
    for index, item in enumerate(items):
        if item["ticket_id"] != requested:
            continue
        if index <= 0:
            return None
        return str(items[index - 1]["ticket_id"])
    return None


def _roadmap_item_for_ticket(
    ticket_id: str,
    items: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    requested = _safe_ticket_id(ticket_id)
    for item in items:
        if item["ticket_id"] == requested:
            return dict(item)
    raise TicketArchitectBridgeInputError("roadmap authority cannot resolve target")


def resolve_roadmap_ticket_authority(ticket_id: str) -> dict[str, Any]:
    """Resolve one ticket id from canonical P18.9 roadmap authority."""

    return _roadmap_item_for_ticket(ticket_id, resolve_roadmap_ticket_authorities())


def resolve_roadmap_ticket_authorities() -> tuple[dict[str, Any], ...]:
    """Return the canonical ordered P18.9 roadmap ticket authorities."""

    implementation_items = _resolve_implementation_roadmap_ticket_authorities()
    if implementation_items:
        return implementation_items
    return _resolve_advisory_roadmap_ticket_authorities()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _resolve_implementation_roadmap_ticket_authorities() -> tuple[dict[str, Any], ...]:
    path = _repo_root() / CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ()
    in_section = False
    section_seen = False
    section_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(
            rf"##\s+[0-9]+\.\s+{re.escape(CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_SECTION)}",
            stripped,
        ):
            in_section = True
            section_seen = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section:
            section_lines.append(line)
    if not section_seen:
        return ()

    items: list[dict[str, Any]] = []
    contracts: dict[str, dict[str, Any]] = {}
    current_table: str | None = None
    for line in section_lines:
        stripped = line.strip()
        if "|" not in stripped:
            current_table = None
            continue
        cells = [_clean_markdown_table_cell(cell) for cell in stripped.strip("|").split("|")]
        if _is_markdown_separator_row(cells):
            continue
        header = tuple(cell.lower() for cell in cells)
        if len(header) >= 4 and header[:4] == ("ticket", "title", "dependencies", "purpose"):
            current_table = "sequence"
            continue
        if len(header) >= 3 and header[:3] == ("ticket", "field", "value"):
            current_table = "contract"
            continue
        if current_table == "sequence" and len(cells) >= 3 and _is_safe_ticket_id(cells[0]):
            ticket_id = _safe_ticket_id(cells[0])
            ticket_title = str(cells[1]).strip()
            dependency_ticket_ids = _parse_roadmap_dependency_ticket_ids(cells[2])
            authority_path = CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH
            authority_section = CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_SECTION
            authority_type = CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY
            if ticket_id == CANONICAL_TICKET_ID:
                ticket_title = CANONICAL_TICKET_TITLE
                authority_path = CANONICAL_ROADMAP_AUTHORITY_PATH
                authority_section = CANONICAL_ROADMAP_AUTHORITY_SECTION
                authority_type = CANONICAL_ROADMAP_AUTHORITY
            items.append({
                "ticket_id": ticket_id,
                "ticket_title": ticket_title,
                "authority_path": authority_path,
                "authority_section": authority_section,
                "authority_type": authority_type,
                "next_action_id": _roadmap_generation_action_id(ticket_id),
                "dependency_ticket_ids": dependency_ticket_ids,
            })
        elif current_table == "contract" and len(cells) >= 3 and _is_safe_ticket_id(cells[0]):
            _append_roadmap_ticket_contract(contracts, cells)
    for item in items:
        contract = contracts.get(str(item["ticket_id"]))
        if contract:
            _validate_roadmap_ticket_contract(str(item["ticket_id"]), contract)
            item["ticket_contract"] = _json_ready_contract(contract)
    _validate_roadmap_ticket_items(items)
    return tuple(items)


def _clean_markdown_table_cell(value: object) -> str:
    text = str(value or "").strip()
    if "<br" not in text.lower() and text.startswith("`") and text.endswith("`") and len(text) >= 2:
        text = text[1:-1]
    return text.strip()


def _is_markdown_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def _append_roadmap_ticket_contract(
    contracts: dict[str, dict[str, Any]],
    cells: list[str],
) -> None:
    ticket_id = _safe_ticket_id(cells[0])
    field_name = _normalize_contract_field(cells[1])
    if field_name not in _CONTRACT_LIST_FIELDS and field_name not in _CONTRACT_SINGLE_FIELDS:
        raise TicketArchitectBridgeInputError("roadmap ticket contract contains unknown field")
    contract = contracts.setdefault(ticket_id, {})
    if field_name in _CONTRACT_LIST_FIELDS:
        existing = list(contract.get(field_name) or ())
        existing.extend(_split_contract_items(cells[2]))
        contract[field_name] = existing
        return
    if field_name in contract:
        raise TicketArchitectBridgeInputError("roadmap ticket contract contains duplicate field")
    contract[field_name] = _clean_markdown_table_cell(cells[2])


def _normalize_contract_field(value: object) -> str:
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    return re.sub(r"[^a-z0-9_]+", "", text)


def _split_contract_items(value: object) -> tuple[str, ...]:
    text = str(value or "").strip()
    if not text:
        return ()
    parts = re.split(r"\s*<br\s*/?>\s*", text, flags=re.IGNORECASE)
    return tuple(_clean_markdown_table_cell(part) for part in parts if part.strip())


def _validate_roadmap_ticket_contract(ticket_id: str, contract: dict[str, Any]) -> None:
    ticket_type = str(contract.get("ticket_type") or "").strip().lower()
    if ticket_type and ticket_type not in {item.value for item in TicketType}:
        raise TicketArchitectBridgeInputError("roadmap ticket contract contains invalid ticket_type")
    if ticket_type != TicketType.IMPLEMENTATION.value:
        return
    required_fields = (
        "objective",
        "predecessor_evidence",
        "information_architecture",
        "required_surfaces",
        "tasks",
        "acceptance_criteria",
    )
    missing = tuple(field for field in required_fields if not contract.get(field))
    if missing:
        raise TicketArchitectBridgeInputError(
            "P18_9_0_ACCEPTED_IA_HANDOFF_GAP: "
            f"{ticket_id} implementation contract is missing {', '.join(missing)}"
        )


def _contract_from_authority_item(item: dict[str, Any]) -> dict[str, Any] | None:
    contract = item.get("ticket_contract")
    if not isinstance(contract, dict) or not contract:
        return None
    return _json_ready_contract(contract)


def _json_ready_contract(contract: dict[str, Any]) -> dict[str, Any]:
    ready: dict[str, Any] = {}
    for key, value in sorted(contract.items()):
        field_name = _normalize_contract_field(key)
        if field_name in _CONTRACT_LIST_FIELDS:
            ready[field_name] = [str(item).strip() for item in value or () if str(item).strip()]
        elif field_name in _CONTRACT_SINGLE_FIELDS:
            ready[field_name] = str(value or "").strip()
    return ready


def _resolve_advisory_roadmap_ticket_authorities() -> tuple[dict[str, Any], ...]:
    path = _repo_root() / CANONICAL_ROADMAP_AUTHORITY_PATH
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TicketArchitectBridgeInputError("roadmap authority cannot resolve target") from exc
    in_section = False
    items: list[dict[str, Any]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == CANONICAL_ROADMAP_AUTHORITY_SECTION + ":":
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if not in_section or "|" not in stripped:
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2 and _is_safe_ticket_id(cells[0]):
            ticket_id = _safe_ticket_id(cells[0])
            ticket_title = cells[1]
            if ticket_id == CANONICAL_TICKET_ID:
                ticket_title = CANONICAL_TICKET_TITLE
            items.append({
                "ticket_id": ticket_id,
                "ticket_title": ticket_title,
                "authority_path": CANONICAL_ROADMAP_AUTHORITY_PATH,
                "authority_section": CANONICAL_ROADMAP_AUTHORITY_SECTION,
                "authority_type": CANONICAL_ROADMAP_AUTHORITY,
                "next_action_id": _roadmap_generation_action_id(ticket_id),
                "dependency_ticket_ids": (),
            })
    _validate_roadmap_ticket_items(items)
    return tuple(items)


def _roadmap_generation_action_id(ticket_id: str) -> str:
    if ticket_id == CANONICAL_TICKET_ID:
        return CANONICAL_NEXT_ACTION_ID
    return canonical_generation_action_id(ticket_id)


def _parse_roadmap_dependency_ticket_ids(value: object) -> tuple[str, ...]:
    text = str(value or "").strip().strip("`")
    if not text or text.lower() == "none":
        return ()
    dependencies: list[str] = []
    for raw_dependency in re.split(r"[;,]", text):
        dependency = raw_dependency.strip().strip("`")
        if not dependency:
            continue
        dependencies.append(_safe_ticket_id(dependency))
    if len(dependencies) != len(frozenset(dependencies)):
        raise TicketArchitectBridgeInputError("roadmap authority contains duplicate dependencies")
    return tuple(dependencies)


def _roadmap_dependency_metadata(
    target: GovernedTicketGenerationTarget,
) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "ticket_id": dependency_ticket_id,
            "kind": DependencyKind.HARD_PREREQUISITE.value,
            "scope": DependencyScope.INTERNAL_PROJECT.value,
            "rationale": (
                f"{dependency_ticket_id} must be accepted before roadmap generation of "
                f"{target.ticket_id}. This is implementation-roadmap metadata, not a "
                "compile-only dependency-plan edge."
            ),
        }
        for dependency_ticket_id in target.dependency_ticket_ids
    )


def _validate_roadmap_ticket_items(items: list[dict[str, Any]]) -> None:
    if not items:
        raise TicketArchitectBridgeInputError("roadmap authority cannot resolve target")
    ticket_ids = tuple(str(item["ticket_id"]) for item in items)
    if len(ticket_ids) != len(frozenset(ticket_ids)):
        raise TicketArchitectBridgeInputError("roadmap authority contains duplicate tickets")
    if ticket_ids[0] != CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeInputError("roadmap authority must start at P18.9.0")
    seen: set[str] = set()
    for item in items:
        ticket_id = str(item["ticket_id"])
        for dependency_ticket_id in item.get("dependency_ticket_ids") or ():
            if dependency_ticket_id not in seen:
                raise TicketArchitectBridgeInputError(
                    "roadmap authority dependency must reference an earlier ticket"
                )
        seen.add(ticket_id)


def _safe_ticket_id(value: object) -> str:
    candidate = str(value or "").strip()
    if not _is_safe_ticket_id(candidate):
        raise TicketArchitectBridgeInputError("governed ticket id is invalid")
    return candidate


def _is_safe_ticket_id(value: object) -> bool:
    return bool(
        re.fullmatch(
            r"[A-Z][A-Z0-9]{0,31}(?:\.[A-Z0-9]+)+",
            str(value or "").strip(),
        )
    )


def _safe_digest(value: object) -> str:
    candidate = str(value or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", candidate):
        raise TicketArchitectBridgeInputError("authority digest is invalid")
    return candidate


def _ticket_action_token(ticket_id: str) -> str:
    return _safe_ticket_id(ticket_id).replace(".", "_")


def _ticket_verdict_token(ticket_id: str, suffix: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "_", ticket_id.lower()).strip("_")
    suffix_token = re.sub(r"[^a-z0-9]+", "_", suffix.lower()).strip("_")
    return f"{token}_{suffix_token}"[:256]


def _ticket_commit_slug(ticket_id: str) -> str:
    return ticket_id.replace(".", " ")


class TicketArchitectBridgeError(ValueError):
    """Base error for governed Ticket Architect bridge failures."""


class TicketArchitectBridgeInputError(TicketArchitectBridgeError):
    """Raised when the requested project, ticket, or action is not eligible."""


class TicketArchitectBridgeConflict(TicketArchitectBridgeError):
    """Raised when persisted generated authority conflicts with the ticket."""


class TicketArchitectBridgeGenerationError(TicketArchitectBridgeError):
    """Raised when P16, P17, or P18 contract generation fails."""


def generation_record_path() -> Path:
    """Return the profile-scoped P18.9.0 generation authority path."""

    return generation_record_path_for_ticket(CANONICAL_TICKET_ID)


def generation_record_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped generation authority path for one ticket."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    return get_hermes_home() / _STORE_DIR / f"{safe_ticket_id}.json"


def reconciliation_history_path_for_ticket(ticket_id: str) -> Path:
    """Return the profile-scoped stale future-ticket reconciliation history path."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    return get_hermes_home() / _RECONCILIATION_STORE_DIR / f"{safe_ticket_id}.jsonl"


def quarantined_generation_record_path(*, ticket_id: str, bridge_sha256: str) -> Path:
    """Return the deterministic quarantine path for one stale generated record."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    safe_digest = _safe_digest(bridge_sha256)
    return get_hermes_home() / _RECONCILIATION_STORE_DIR / f"{safe_ticket_id}.{safe_digest}.json"


def approval_decision_record_path() -> Path:
    """Return the profile-scoped P18.9.0 human decision authority path."""

    return get_hermes_home() / _STORE_DIR / _APPROVAL_DECISION_STORE_FILE


def load_p18_9_0_generation_record() -> dict[str, Any] | None:
    """Load and validate the persisted P18.9.0 authority record, if present."""

    return load_generation_record(ticket_id=CANONICAL_TICKET_ID)


def load_generation_record(
    *,
    ticket_id: str,
    target: GovernedTicketGenerationTarget | None = None,
) -> dict[str, Any] | None:
    """Load and validate one persisted ticket-generation authority record."""

    resolved_target = target or (
        p18_9_0_generation_target() if ticket_id == CANONICAL_TICKET_ID else None
    )
    path = generation_record_path_for_ticket(ticket_id)
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TicketArchitectBridgeConflict(
            f"{ticket_id} generated authority record is unreadable"
        ) from exc
    return validate_generation_record(record, target=resolved_target)


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

    return validate_generation_record(record, target=p18_9_0_generation_target())


def validate_generation_record(
    record: dict[str, Any],
    *,
    target: GovernedTicketGenerationTarget | None = None,
) -> dict[str, Any]:
    """Validate persisted bridge evidence without regenerating any contracts."""

    if not isinstance(record, dict):
        raise TicketArchitectBridgeConflict("generated authority record must be an object")
    if record.get("bridge_SHA256") != _record_digest(record):
        raise TicketArchitectBridgeConflict("generated authority record digest mismatch")
    resolved_target = target or _target_from_record(record)
    _require_identity(record, target=resolved_target)

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

    if project_spec.project_id != resolved_target.project_id:
        raise TicketArchitectBridgeConflict(f"ProjectSpec must bind {resolved_target.project_id}")
    if ticket_spec.project_id != resolved_target.project_id:
        raise TicketArchitectBridgeConflict(f"TicketSpec must bind {resolved_target.project_id}")
    if ticket_spec.ticket_id != resolved_target.ticket_id:
        raise TicketArchitectBridgeConflict(f"TicketSpec must bind {resolved_target.ticket_id}")
    if ticket_spec.title != resolved_target.ticket_title:
        raise TicketArchitectBridgeConflict("TicketSpec title conflicts with roadmap")
    if ticket_spec != _build_ticket_spec(resolved_target):
        raise TicketArchitectBridgeConflict("TicketSpec conflicts with roadmap contract")
    if context_pack.ticket_id != resolved_target.ticket_id:
        raise TicketArchitectBridgeConflict(f"ContextPack must bind {resolved_target.ticket_id}")
    if dependency_plan.ticket_ids != (resolved_target.ticket_id,):
        raise TicketArchitectBridgeConflict(
            f"dependency plan must contain only {resolved_target.ticket_id}"
        )
    if dependency_plan.blocked_ticket_ids:
        raise TicketArchitectBridgeConflict(
            f"{resolved_target.ticket_id} dependency plan must be unblocked"
        )
    if lint_report.ticket_ids != (resolved_target.ticket_id,):
        raise TicketArchitectBridgeConflict(f"lint report must bind {resolved_target.ticket_id}")
    if lint_report.disposition is not TicketLintDisposition.PASS:
        raise TicketArchitectBridgeConflict(f"{resolved_target.ticket_id} lint report must pass")
    if compilation.work_packet.ticket_id != resolved_target.ticket_id:
        raise TicketArchitectBridgeConflict(f"WorkPacket must bind {resolved_target.ticket_id}")
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


def inspect_invalid_future_ticket_authority(
    *,
    ticket_id: str,
    workflow: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify a future-ticket generation record without mutating state."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    if safe_ticket_id == CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeInputError("historical generated authority is not reconcilable")
    path = generation_record_path_for_ticket(safe_ticket_id)
    if not path.exists():
        return _reconciliation_absent_result(safe_ticket_id, path)
    record = _read_generation_record_unvalidated(path, ticket_id=safe_ticket_id)
    target = _reconciliation_target_for_ticket(safe_ticket_id, workflow=workflow)
    validation_error = _future_generation_validation_error(record, target=target)
    classification = (
        "valid_current_generated_authority"
        if validation_error is None
        else "unaccepted_partial_failed_future_ticket_authority"
    )
    blockers = _future_reconciliation_blockers(record, path=path)
    return {
        "source_system": "pepper-ticket-architect-bridge",
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "ticket_id": safe_ticket_id,
        "record_path": str(path),
        "record_path_relative": str(_STORE_DIR / f"{safe_ticket_id}.json").replace("\\", "/"),
        "classification": classification,
        "reconcilable": validation_error is not None and not blockers,
        "validation_error": validation_error,
        "expected_roadmap_authority_path": target.roadmap_authority_path,
        "actual_roadmap_authority_path": record.get("roadmap_authority_path"),
        "source_next_action_id": record.get("source_next_action_id"),
        "bridge_SHA256": record.get("bridge_SHA256"),
        "created_at": record.get("created_at"),
        "ticket_spec_SHA256": record.get("ticket_spec_SHA256"),
        "dependency_plan_SHA256": record.get("dependency_plan_SHA256"),
        "work_packet_id": record.get("work_packet_id"),
        "work_packet_SHA256": record.get("work_packet_SHA256"),
        "generation_completed_structurally": _generation_completed_structurally(record),
        "human_ticket_approval_present": record.get("human_ticket_approval_present"),
        "Kanban_dispatch": record.get("Kanban_dispatch"),
        "worker_execution": record.get("worker_execution"),
        "Git_mutation": record.get("Git_mutation"),
        "blockers": blockers,
    }


def reconcile_invalid_future_ticket_authority(
    *,
    ticket_id: str,
    workflow: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Quarantine one invalid unaccepted future-ticket generation authority."""

    safe_ticket_id = _safe_ticket_id(ticket_id)
    if safe_ticket_id == CANONICAL_TICKET_ID:
        raise TicketArchitectBridgeInputError("historical generated authority is not reconcilable")
    with _STORE_LOCK:
        path = generation_record_path_for_ticket(safe_ticket_id)
        if not path.exists():
            return _reconciliation_absent_result(safe_ticket_id, path)
        record = _read_generation_record_unvalidated(path, ticket_id=safe_ticket_id)
        target = _reconciliation_target_for_ticket(safe_ticket_id, workflow=workflow)
        validation_error = _future_generation_validation_error(record, target=target)
        if validation_error is None:
            return {
                "source_system": "pepper-ticket-architect-bridge",
                "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
                "ticket_id": safe_ticket_id,
                "record_path": str(path),
                "classification": "valid_current_generated_authority",
                "reconciled": False,
                "idempotent_replay": False,
                "reason": "generated authority already validates against current canonical provenance",
            }
        blockers = _future_reconciliation_blockers(record, path=path)
        if blockers:
            raise TicketArchitectBridgeConflict(
                "invalid future-ticket authority crossed guarded boundary: "
                + "; ".join(blockers)
            )
        record_digest = _safe_digest(record.get("bridge_SHA256"))
        quarantine_path = quarantined_generation_record_path(
            ticket_id=safe_ticket_id,
            bridge_sha256=record_digest,
        )
        history_path = reconciliation_history_path_for_ticket(safe_ticket_id)
        existing_reconciliation = _load_existing_reconciliation(history_path, record_digest)
        if path.exists():
            quarantine_path.parent.mkdir(parents=True, exist_ok=True)
            if not quarantine_path.exists():
                tmp = quarantine_path.with_suffix(quarantine_path.suffix + ".tmp")
                tmp.write_text(
                    json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                tmp.replace(quarantine_path)
            if existing_reconciliation is None:
                _append_reconciliation_history(
                    history_path,
                    record=record,
                    target=target,
                    validation_error=validation_error,
                    quarantine_path=quarantine_path,
                )
            path.unlink()
        return {
            "source_system": "pepper-ticket-architect-bridge",
            "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
            "ticket_id": safe_ticket_id,
            "classification": "unaccepted_partial_failed_future_ticket_authority",
            "reconciled": True,
            "idempotent_replay": existing_reconciliation is not None,
            "record_path": str(path),
            "history_path": str(history_path),
            "quarantine_path": str(quarantine_path),
            "bridge_SHA256": record_digest,
            "validation_error": validation_error,
            "expected_roadmap_authority_path": target.roadmap_authority_path,
            "actual_roadmap_authority_path": record.get("roadmap_authority_path"),
            "source_next_action_id": record.get("source_next_action_id"),
            "ticket_generated": False,
            "human_ticket_approval_present": False,
            "execution_ready": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "fresh_generation_required": True,
        }


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

    return generate_current_ticket(
        workflow=workflow,
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
        target=p18_9_0_generation_target(),
    )


def generate_current_ticket(
    *,
    workflow: dict[str, Any],
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
    target: GovernedTicketGenerationTarget | None = None,
) -> dict[str, Any]:
    """Generate or replay the single canonical next governed ticket."""

    resolved_target = target or resolve_generation_target_from_workflow(workflow)
    eligible_workflow = (
        workflow
        if target is not None
        else _workflow_bound_to_generation_target(workflow, target=resolved_target)
    )
    _validate_requested_identity(
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
        target=resolved_target,
    )
    with _STORE_LOCK:
        existing = load_generation_record(
            ticket_id=resolved_target.ticket_id,
            target=resolved_target,
        )
        if existing is not None:
            return _operational_result(existing, idempotent_replay=True)

        _validate_workflow_eligibility(eligible_workflow, target=resolved_target)
        try:
            record = _build_generation_record(eligible_workflow, target=resolved_target)
            validate_generation_record(record, target=resolved_target)
            _persist_generation_record(record)
        except TicketArchitectBridgeError:
            raise
        except Exception as exc:
            raise TicketArchitectBridgeGenerationError(
                f"{resolved_target.ticket_id} Ticket Architect bridge generation failed"
            ) from exc
    return _operational_result(record, idempotent_replay=False)


def _workflow_bound_to_generation_target(
    workflow: dict[str, Any],
    *,
    target: GovernedTicketGenerationTarget,
) -> dict[str, Any]:
    if not isinstance(workflow, dict):
        return workflow
    bounded = dict(workflow)
    bounded["next_ticket_id"] = target.ticket_id
    bounded["next_ticket_title"] = target.ticket_title
    next_action = workflow.get("next_action")
    label = (
        str(next_action.get("label") or "").strip()
        if isinstance(next_action, dict)
        and next_action.get("id") == target.next_action_id
        and next_action.get("target_ticket_id") == target.ticket_id
        else ""
    )
    bounded["next_action"] = {
        "id": target.next_action_id,
        "label": label or f"Generate governed {target.ticket_id} {target.ticket_title}.",
        "target_ticket_id": target.ticket_id,
        "target_ticket_title": target.ticket_title,
        "required_human_action": "ticket_generation",
    }
    return bounded


def generated_record_to_workflow_overlay(record: dict[str, Any]) -> dict[str, Any]:
    """Return workflow-control fields implied by a validated generated record."""

    target = _target_from_record(record)
    validated = validate_generation_record(record, target=target)
    decision = (
        load_p18_9_0_approval_decision_record(generation_record=validated)
        if target.ticket_id == CANONICAL_TICKET_ID
        else None
    )
    if decision is not None:
        return _decided_record_to_workflow_overlay(validated, decision)
    return {
        "current_ticket_id": target.ticket_id,
        "current_ticket_title": target.ticket_title,
        "next_ticket_id": None,
        "next_ticket_title": None,
        "readiness": "awaiting_ticket_approval",
        "workflow_state": f"{target.ticket_id}-AWAITING-TICKET-APPROVAL",
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
            "id": target.approval_next_action_id,
            "label": (
                f"Review and approve governed {target.ticket_id} {target.ticket_title} "
                "before execution."
            ),
            "target_ticket_id": target.ticket_id,
            "target_ticket_title": target.ticket_title,
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
    target = _target_from_record(generation_record)
    approved = decision_record["decision"] == HumanApprovalDecision.APPROVE.value
    workflow_state = (
        f"{target.ticket_id}-TICKET-APPROVED"
        if approved
        else f"{target.ticket_id}-AWAITING-CORRECTION"
    )
    workflow_status = "ticket_approved" if approved else "awaiting_correction"
    next_action = (
        {
            "id": target.approved_no_execution_next_action_id,
            "label": (
                f"Human ticket approval is recorded for {target.ticket_id}; execution remains "
                "blocked until a separate governed action is authorized."
            ),
            "target_ticket_id": target.ticket_id,
            "target_ticket_title": target.ticket_title,
            "required_human_action": "governed_followup",
        }
        if approved
        else {
            "id": target.revise_next_action_id,
            "label": (
                f"Human rejection is recorded for {target.ticket_id}; correction is required "
                "before any downstream work."
            ),
            "target_ticket_id": target.ticket_id,
            "target_ticket_title": target.ticket_title,
            "required_human_action": "ticket_correction",
        }
    )
    return {
        "current_ticket_id": target.ticket_id,
        "current_ticket_title": target.ticket_title,
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


def _build_generation_record(
    workflow: dict[str, Any],
    *,
    target: GovernedTicketGenerationTarget,
) -> dict[str, Any]:
    project_spec = _build_project_spec(target)
    ticket_spec = _build_ticket_spec(target)
    context_pack = _assemble_context_pack(project_spec, ticket_spec, target=target)
    planning_request = TicketPlanningRequest(
        project_spec=project_spec,
        tickets=(ticket_spec,),
        external_dependency_resolutions=(),
        policy=ParallelPlanningPolicy(),
    )
    dependency_plan = build_ticket_dependency_plan(planning_request)
    _validate_dependency_plan(dependency_plan, target=target)
    lint_report = lint_ticket_collection(
        TicketLintRequest(
            project_spec=project_spec,
            tickets=(ticket_spec,),
            dependency_plan=dependency_plan,
            collection_complete=False,
        )
    )
    _validate_lint_report(lint_report, target=target)
    approval_record, publication_result, compilation_result = _compile_work_packet(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        planning_request=planning_request,
        dependency_plan=dependency_plan,
        lint_report=lint_report,
        target=target,
    )
    transition_result = _build_workflow_transition(compilation_result, target=target)
    observed_at = _utc_now_iso()
    record = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_ARCHITECT_BRIDGE_POLICY_ID,
        "created_at": observed_at,
        "source_next_action_id": target.next_action_id,
        "source_workflow_status": str(workflow.get("workflow_status") or ""),
        "generation_status": "awaiting_ticket_approval",
        "project_id": target.project_id,
        "project_name": target.project_name,
        "macroproject_id": target.macroproject_id,
        "macroproject_title": target.macroproject_title,
        "ticket_id": target.ticket_id,
        "ticket_title": target.ticket_title,
        "canonical_roadmap_authority": target.canonical_roadmap_authority,
        "roadmap_authority_path": canonical_roadmap_authority_path(target.roadmap_authority_path),
        "roadmap_authority_section": target.roadmap_authority_section,
        "roadmap_dependency_ticket_ids": list(target.dependency_ticket_ids),
        "roadmap_dependency_metadata": list(_roadmap_dependency_metadata(target)),
        "idempotency_key": target.idempotency_key,
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
    if target.ticket_contract:
        record["ticket_contract"] = _json_ready_contract(target.ticket_contract)
        record["ticket_contract_SHA256"] = _ticket_contract_digest(target.ticket_contract)
    if target.ticket_id != CANONICAL_TICKET_ID:
        record["predecessor_ticket_id"] = target.predecessor_ticket_id
        record["canonical_next_ticket_authority"] = _canonical_next_ticket_authority_projection(
            target
        )
    record["bridge_SHA256"] = _record_digest(record)
    return record


def _build_project_spec(target: GovernedTicketGenerationTarget) -> ProjectSpec:
    return ProjectSpec(
        project_id=target.project_id,
        title=target.macroproject_title,
        objective=(
            "Personalize Pepper's product experience through canonical governed tickets, "
            "explicit human approvals, and preserved execution boundaries."
        ),
        summary=(
            "P18.9 starts from the accepted P18 workflow migration and produces "
            "product personalization tickets through the governed P16/P17/P18 chain."
        ),
        context=(
            "P18 and P18.R are closed and P18.9 is the active governed macroproject.",
            f"The canonical roadmap identifies {target.ticket_id} as {target.ticket_title}.",
            f"{target.ticket_id} must remain compile-only until explicit human ticket approval.",
        ),
        authority_references=_authority_references(target),
        scope=_scope(),
        constraints=(
            "Use the existing P16 TicketSpec, ContextPack, dependency plan, lint, approval, and publication contracts.",
            "Use the existing P17 WorkPacket compiler only in compile-only mode.",
            "Use the existing P18 governed workflow transition and stop at awaiting_ticket_approval.",
            "Provider dispatch, model inference, Kanban dispatch, worker execution, Docker, Graphify, and Git mutation are not authorized.",
        ),
        non_goals=(
            f"Do not execute {target.ticket_id}.",
            "Do not create a Kanban planning task or worker dispatch.",
            f"Do not auto-approve the {target.ticket_id} ticket.",
            "Do not stage, commit, push, or otherwise mutate Git.",
        ),
        acceptance_criteria=(
            f"{target.ticket_id} is represented as a canonical P16 TicketSpec with the approved title.",
            "A P17 WorkPacket is compiled exactly once and remains execution_ready=false.",
            "The governed workflow reaches awaiting_ticket_approval with human approval still required.",
        ),
        completion_verdict=_ticket_verdict_token(target.ticket_id, "ticket_architect_bridge_ready"),
    )


def _build_ticket_spec(target: GovernedTicketGenerationTarget) -> TicketSpec:
    if target.ticket_id == CANONICAL_TICKET_ID:
        return _build_p18_9_0_ticket_spec(target)
    contract = target.ticket_contract or {}
    if contract:
        return _build_contract_ticket_spec(target, contract=contract)
    return _build_default_ticket_spec(target)


def _build_p18_9_0_ticket_spec(target: GovernedTicketGenerationTarget) -> TicketSpec:
    return TicketSpec(
        project_id=target.project_id,
        ticket_id=target.ticket_id,
        title=target.ticket_title,
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
        authority_references=(
            AuthorityReferenceSpec(
                kind=AuthorityReferenceKind.EXTERNAL_SOURCE,
                value=target.canonical_roadmap_authority,
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
        ),
        dependencies=(),
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=RepositoryScopeSpec(
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
        ),
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


def _build_default_ticket_spec(target: GovernedTicketGenerationTarget) -> TicketSpec:
    return TicketSpec(
        project_id=target.project_id,
        ticket_id=target.ticket_id,
        title=target.ticket_title,
        ticket_type=TicketType.ARCHITECTURE,
        objective=(
            f"Define the governed product architecture and acceptance contract for {target.ticket_title}."
        ),
        context=(
            "The active governed project is PEPPER, while P18.9 is the macroproject identifier.",
            f"{target.ticket_id} is resolved from canonical roadmap authority, not user-supplied arbitrary ticket text.",
            "Execution remains blocked until the generated ticket is explicitly approved by a human.",
        ),
        authority_references=_authority_references(target),
        dependencies=(),
        parallelization_hint=ParallelizationHint.UNSPECIFIED,
        scope=_scope(),
        constraints=(
            "Separate product identity PEPPER from repository and macroproject identifiers.",
            "Architecture and design decisions must cite bounded repository or governance evidence.",
            "Acceptance criteria must be testable before any implementation or design work executes.",
            f"Rollback posture: remove only {target.ticket_id} changes if superseded.",
            "No provider dispatch, model inference, Kanban dispatch, worker execution, Docker, Graphify, or Git mutation is authorized.",
        ),
        tasks=(
            f"Inventory repository and product surfaces relevant to {target.ticket_title}.",
            f"Define the design-system or product-architecture boundary for {target.ticket_id}.",
            "Define acceptance criteria and downstream implementation handoff constraints.",
            "Record unresolved product questions without dispatching workers or creating Kanban tasks.",
        ),
        acceptance_criteria=(
            f"The result names the canonical roadmap target {target.ticket_id} and title {target.ticket_title}.",
            "The design or architecture decision cites repository and governance evidence.",
            "The acceptance contract states what must be true before downstream P18.9 work executes.",
            "The result explicitly reports no worker execution, no Kanban dispatch, no Docker, no Graphify, and no Git mutation.",
        ),
        validation_steps=(
            TicketValidationStepSpec(
                validation_id="V1",
                description=f"Human review confirms {target.ticket_id} governed TicketSpec and acceptance contract are present.",
                command=None,
                expected_result=(
                    "The reviewer can identify the roadmap-derived title, acceptance contract, "
                    f"and preserved execution boundary in the {target.ticket_id} result."
                ),
            ),
        ),
        response_contract=TicketResponseContractSpec(
            required_sections=_REQUIRED_RESPONSE_SECTIONS,
            completion_verdict=(
                "p18_9_0_inventory_ia_acceptance_contract_ready"
                if target.ticket_id == CANONICAL_TICKET_ID
                else _ticket_verdict_token(target.ticket_id, "acceptance_contract_ready")
            ),
        ),
        recommended_commit_message=f"{_ticket_commit_slug(target.ticket_id)} Define {target.ticket_title}",
    )


def _build_contract_ticket_spec(
    target: GovernedTicketGenerationTarget,
    *,
    contract: dict[str, Any],
) -> TicketSpec:
    _validate_roadmap_ticket_contract(target.ticket_id, contract)
    dependency_context = _roadmap_dependency_context(target)
    context = _dedupe_texts(
        (
            "The active governed project is PEPPER, while P18.9 is the macroproject identifier.",
            f"{target.ticket_id} is resolved from canonical roadmap authority, not user-supplied arbitrary ticket text.",
            "Execution remains blocked until the generated ticket is explicitly approved by a human.",
        )
        + _contract_items(contract, "context")
        + _contract_items(contract, "predecessor_evidence")
        + _contract_items(contract, "dependency_context")
        + _contract_items(contract, "information_architecture")
        + ((dependency_context,) if dependency_context else ())
    )
    constraints = _dedupe_texts(
        _contract_items(contract, "constraints")
        + tuple(f"Non-goal: {item}" for item in _contract_items(contract, "non_goals"))
        + tuple(f"Risk: {item}" for item in _contract_items(contract, "risk"))
        + (
            "Roadmap dependencies are preserved as roadmap metadata and context only; they must not create compile-only dependency-plan edges unless the full collection is generated.",
            "No provider dispatch, model inference, Kanban dispatch, worker execution, Docker, Graphify, or Git mutation is authorized by Ticket Architect generation.",
            f"Rollback posture: remove only {target.ticket_id} changes if superseded.",
        )
    )
    tasks = _dedupe_texts(
        tuple(f"Implement required surface: {item}" for item in _contract_items(contract, "required_surfaces"))
        + _contract_items(contract, "tasks")
        + tuple(f"Produce expected artifact: {item}" for item in _contract_items(contract, "expected_artifacts"))
    )
    acceptance_criteria = _dedupe_texts(_contract_items(contract, "acceptance_criteria"))
    if not tasks or not acceptance_criteria:
        raise TicketArchitectBridgeInputError(
            "P18_9_0_ACCEPTED_IA_HANDOFF_GAP: implementation contract is incomplete"
        )
    completion_verdict = _contract_text(contract, "completion_verdict") or _ticket_verdict_token(
        target.ticket_id,
        "implementation_ready",
    )
    return TicketSpec(
        project_id=target.project_id,
        ticket_id=target.ticket_id,
        title=target.ticket_title,
        ticket_type=_contract_ticket_type(contract),
        objective=_contract_text(contract, "objective")
        or f"Implement the governed product work for {target.ticket_title}.",
        context=context,
        authority_references=_authority_references(target),
        dependencies=(),
        parallelization_hint=_contract_parallelization_hint(contract),
        scope=_scope(contract),
        constraints=constraints,
        tasks=tasks,
        acceptance_criteria=acceptance_criteria,
        validation_steps=_contract_validation_steps(target, contract),
        response_contract=TicketResponseContractSpec(
            required_sections=_contract_response_sections(contract),
            completion_verdict=completion_verdict,
        ),
        recommended_commit_message=(
            _contract_text(contract, "recommended_commit_message")
            or f"{_ticket_commit_slug(target.ticket_id)} Implement {target.ticket_title}"
        ),
    )


def _scope(contract: dict[str, Any] | None = None) -> RepositoryScopeSpec:
    if contract:
        allowed_paths = _contract_items(contract, "allowed_paths")
        allowed_actions = _contract_items(contract, "allowed_actions")
        if allowed_paths and allowed_actions:
            return RepositoryScopeSpec(
                allowed_paths=allowed_paths,
                forbidden_paths=_contract_items(contract, "forbidden_paths") or (
                    ".git/**",
                    ".opencode/**",
                    "graphify-out/**",
                    "4_external/sources/**",
                    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
                ),
                allowed_actions=allowed_actions,
                forbidden_actions=_contract_items(contract, "forbidden_actions")
                or _REQUIRED_FORBIDDEN_ACTIONS,
            )
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


def _contract_text(contract: dict[str, Any], field_name: str) -> str | None:
    value = contract.get(field_name)
    if isinstance(value, str):
        return value.strip() or None
    return None


def _contract_items(contract: dict[str, Any], field_name: str) -> tuple[str, ...]:
    value = contract.get(field_name)
    if not isinstance(value, list | tuple):
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def _contract_ticket_type(contract: dict[str, Any]) -> TicketType:
    value = (_contract_text(contract, "ticket_type") or TicketType.ARCHITECTURE.value).lower()
    try:
        return TicketType(value)
    except ValueError as exc:
        raise TicketArchitectBridgeInputError(
            "roadmap ticket contract contains invalid ticket_type"
        ) from exc


def _contract_parallelization_hint(contract: dict[str, Any]) -> ParallelizationHint:
    value = _contract_text(contract, "parallelization_hint")
    if value is None:
        return ParallelizationHint.UNSPECIFIED
    try:
        return ParallelizationHint(value)
    except ValueError as exc:
        raise TicketArchitectBridgeInputError(
            "roadmap ticket contract contains invalid parallelization_hint"
        ) from exc


def _contract_response_sections(contract: dict[str, Any]) -> tuple[str, ...]:
    sections = _contract_items(contract, "required_response_sections")
    return sections or _REQUIRED_RESPONSE_SECTIONS


def _contract_validation_steps(
    target: GovernedTicketGenerationTarget,
    contract: dict[str, Any],
) -> tuple[TicketValidationStepSpec, ...]:
    steps = _contract_items(contract, "validation_steps")
    if not steps:
        return (
            TicketValidationStepSpec(
                validation_id="V1",
                description=f"Human review confirms {target.ticket_id} implementation contract is present.",
                command=None,
                expected_result=(
                    f"The reviewer can identify the roadmap-derived implementation scope, "
                    f"acceptance criteria, and preserved execution boundary in {target.ticket_id}."
                ),
            ),
        )
    parsed: list[TicketValidationStepSpec] = []
    for index, raw_step in enumerate(steps, start=1):
        description, expected_result = _parse_contract_validation_step(raw_step)
        parsed.append(
            TicketValidationStepSpec(
                validation_id=f"V{index}",
                description=description,
                command=None,
                expected_result=expected_result,
            )
        )
    return tuple(parsed)


def _parse_contract_validation_step(value: str) -> tuple[str, str]:
    text = value.strip()
    text = re.sub(r"^V[1-9][0-9]*:\s*", "", text)
    if "=>" in text:
        description, expected = text.split("=>", 1)
        return description.strip(), expected.strip()
    return text, "The reviewer can verify the stated validation condition from generated evidence."


def _roadmap_dependency_context(target: GovernedTicketGenerationTarget) -> str | None:
    if not target.dependency_ticket_ids:
        return None
    return "Roadmap dependencies: " + ", ".join(target.dependency_ticket_ids) + "."


def _dedupe_texts(values: tuple[str, ...]) -> tuple[str, ...]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        deduped.append(text)
        seen.add(text)
    return tuple(deduped)


def _authority_references(
    target: GovernedTicketGenerationTarget,
) -> tuple[AuthorityReferenceSpec, ...]:
    return (
        AuthorityReferenceSpec(
            kind=AuthorityReferenceKind.EXTERNAL_SOURCE,
            value=target.roadmap_authority_path,
            rationale=(
                f"Canonical roadmap authority identifies {target.ticket_id} as "
                f"{target.ticket_title}."
            ),
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


def _assemble_context_pack(
    project_spec: ProjectSpec,
    ticket_spec: TicketSpec,
    *,
    target: GovernedTicketGenerationTarget,
) -> ContextPack:
    authority_refs = _authority_references(target)
    dependency_text = (
        "Roadmap dependencies: " + ", ".join(target.dependency_ticket_ids) + "."
        if target.dependency_ticket_ids
        else "Roadmap dependencies: none."
    )
    sources = (
        ContextSourceSpec(
            source_id="CTX-P18-9-ROADMAP",
            kind=ContextSourceKind.HUMAN_INSTRUCTION,
            title=f"Human-approved {target.ticket_id} roadmap item",
            source_reference=target.roadmap_authority_path,
            content=(
                f"{target.ticket_id} is {target.ticket_title}. This identity comes from "
                f"{target.roadmap_authority_section}. {dependency_text}"
            ),
            authority_references=(authority_refs[0],),
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
            authority_references=(authority_refs[1], authority_refs[3]),
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
            authority_references=(authority_refs[2],),
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


def _validate_dependency_plan(
    plan: TicketDependencyPlan,
    *,
    target: GovernedTicketGenerationTarget,
) -> None:
    if plan.project_id != target.project_id:
        raise TicketArchitectBridgeGenerationError(f"dependency plan must bind {target.project_id}")
    if plan.ticket_ids != (target.ticket_id,):
        raise TicketArchitectBridgeGenerationError(
            f"dependency plan must contain {target.ticket_id}"
        )
    if plan.blocked_ticket_ids:
        raise TicketArchitectBridgeGenerationError(f"{target.ticket_id} dependency plan is blocked")
    if len(plan.waves) != 1 or plan.waves[0].disposition.value != "dependency_ready":
        raise TicketArchitectBridgeGenerationError(
            f"{target.ticket_id} dependency plan must be dependency-ready"
        )


def _validate_lint_report(
    report: TicketLintReport,
    *,
    target: GovernedTicketGenerationTarget,
) -> None:
    if report.project_id != target.project_id:
        raise TicketArchitectBridgeGenerationError(f"lint report must bind {target.project_id}")
    if report.ticket_ids != (target.ticket_id,):
        raise TicketArchitectBridgeGenerationError(f"lint report must contain {target.ticket_id}")
    if report.disposition is not TicketLintDisposition.PASS:
        raise TicketArchitectBridgeGenerationError(f"{target.ticket_id} TicketSpec lint must pass")


def _compile_work_packet(
    *,
    project_spec: ProjectSpec,
    ticket_spec: TicketSpec,
    context_pack: ContextPack,
    planning_request: TicketPlanningRequest,
    dependency_plan: TicketDependencyPlan,
    lint_report: TicketLintReport,
    target: GovernedTicketGenerationTarget,
) -> tuple[TicketApprovalRecord, TicketPublicationResult, WorkPacketCompilationResult]:
    generation_request = TicketGenerationRequest(
        project_spec=project_spec,
        ticket_spec=ticket_spec,
        context_pack=context_pack,
        roles=_generator_roles_for_ticket_type(ticket_spec.ticket_type),
    )
    assignments = prepare_ticket_generator_assignments(generation_request)
    proposals = tuple(
        build_ticket_proposal(
            assignment=assignment,
            proposed_ticket=ticket_spec,
            rationale=(
                f"{target.ticket_id} TicketSpec is generated deterministically from the "
                "approved P18.9 roadmap item and bounded Pepper workflow evidence."
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
        evidence_reference=(
            f"{target.ticket_id} dependency plan before compile-only WorkPacket creation."
        ),
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
                decision_reference=f"{target.ticket_id} compile-only TicketSpec acceptance evidence.",
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
                publication_reference=(
                    f"{target.ticket_id} compile-only canonical TicketSpec publication."
                ),
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
        authorization_reference=f"{target.ticket_id} deterministic compile-only authorization.",
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


def _generator_roles_for_ticket_type(ticket_type: TicketType) -> tuple[TicketGeneratorRole, ...]:
    if ticket_type is TicketType.IMPLEMENTATION:
        return (
            TicketGeneratorRole.ARCHITECTURE,
            TicketGeneratorRole.IMPLEMENTATION,
            TicketGeneratorRole.VALIDATION,
        )
    if ticket_type is TicketType.REFACTOR:
        return (TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.IMPLEMENTATION)
    if ticket_type is TicketType.TEST:
        return (TicketGeneratorRole.IMPLEMENTATION, TicketGeneratorRole.VALIDATION)
    if ticket_type is TicketType.BUGFIX:
        return (TicketGeneratorRole.IMPLEMENTATION, TicketGeneratorRole.VALIDATION)
    if ticket_type is TicketType.INTEGRATION:
        return (TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.INTEGRATION)
    if ticket_type is TicketType.DOCUMENTATION:
        return (TicketGeneratorRole.DOCUMENTATION, TicketGeneratorRole.GOVERNANCE)
    if ticket_type is TicketType.CLOSURE:
        return (TicketGeneratorRole.INTEGRATION, TicketGeneratorRole.GOVERNANCE)
    return (TicketGeneratorRole.ARCHITECTURE, TicketGeneratorRole.GOVERNANCE)


def _build_workflow_transition(
    compilation_result: WorkPacketCompilationResult,
    *,
    target: GovernedTicketGenerationTarget,
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
        project_id=target.macroproject_id,
        ticket_id=target.macroproject_id,
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
        evidence_refs=("ticket_factory_candidate", target.ticket_id),
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
    target: GovernedTicketGenerationTarget,
) -> None:
    if requested_project_id not in {None, "", target.project_id}:
        raise TicketArchitectBridgeInputError(f"requested project is not {target.project_id}")
    if requested_ticket_id not in {None, "", target.ticket_id}:
        raise TicketArchitectBridgeInputError(
            f"requested ticket is not canonical next ticket {target.ticket_id}"
        )
    if requested_next_action_id not in {None, "", target.next_action_id}:
        raise TicketArchitectBridgeInputError(
            f"requested next action is not {target.next_action_id}"
        )


def _validate_workflow_eligibility(
    workflow: dict[str, Any],
    *,
    target: GovernedTicketGenerationTarget,
) -> None:
    if not isinstance(workflow, dict):
        raise TicketArchitectBridgeInputError("workflow state is unavailable")
    if workflow.get("project_id") != target.project_id:
        raise TicketArchitectBridgeInputError(f"active governed project is not {target.project_id}")
    if workflow.get("macroproject_id") != target.macroproject_id:
        raise TicketArchitectBridgeInputError(
            f"active macroproject is not {target.macroproject_id}"
        )
    if workflow.get("current_ticket_id") not in {None, ""}:
        raise TicketArchitectBridgeInputError(
            f"{target.ticket_id} generation requires no active ticket"
        )
    if workflow.get("P18_9_ready") is not True:
        raise TicketArchitectBridgeInputError("P18.9 roadmap is not intake-ready")
    if target.ticket_id == CANONICAL_TICKET_ID and workflow.get("P18_9_ticket_generated") is True:
        raise TicketArchitectBridgeConflict(
            f"workflow says {target.ticket_id} is generated but no authority record exists"
        )
    if target.ticket_id != CANONICAL_TICKET_ID and workflow.get("next_ticket_generated") is True:
        raise TicketArchitectBridgeConflict(
            f"workflow says {target.ticket_id} is generated but no authority record exists"
        )
    next_action = workflow.get("next_action")
    if not isinstance(next_action, dict):
        raise TicketArchitectBridgeInputError("next action is unavailable")
    if next_action.get("id") != target.next_action_id:
        raise TicketArchitectBridgeInputError(
            f"next action is not {target.next_action_id}"
        )
    if next_action.get("target_ticket_id") != target.ticket_id:
        raise TicketArchitectBridgeInputError(
            f"next action does not target {target.ticket_id}"
        )
    if workflow.get("workflow_status") not in {
        "planning_approved_or_intake_ready",
        "intake_ready",
        "completed",
    }:
        raise TicketArchitectBridgeInputError(
            f"workflow is not intake-ready for {target.ticket_id} generation"
        )


def _persist_generation_record(record: dict[str, Any]) -> None:
    target = _target_from_record(record)
    path = generation_record_path_for_ticket(target.ticket_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = load_generation_record(ticket_id=target.ticket_id)
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


def _read_generation_record_unvalidated(path: Path, *, ticket_id: str) -> dict[str, Any]:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TicketArchitectBridgeConflict(
            f"{ticket_id} generated authority record is unreadable"
        ) from exc
    if not isinstance(record, dict):
        raise TicketArchitectBridgeConflict("generated authority record must be an object")
    if _safe_ticket_id(record.get("ticket_id")) != ticket_id:
        raise TicketArchitectBridgeConflict("generated authority ticket_id mismatch")
    if record.get("bridge_SHA256") != _record_digest(record):
        raise TicketArchitectBridgeConflict("generated authority record digest mismatch")
    return record


def _reconciliation_target_for_ticket(
    ticket_id: str,
    *,
    workflow: dict[str, Any] | None,
) -> GovernedTicketGenerationTarget:
    state = dict(workflow or {})
    state.setdefault("project_id", CANONICAL_PROJECT_ID)
    state.setdefault("project_name", CANONICAL_PROJECT_NAME)
    state.setdefault("macroproject_id", CANONICAL_MACROPROJECT_ID)
    state.setdefault("macroproject_title", CANONICAL_MACROPROJECT_TITLE)
    predecessor = _roadmap_predecessor_ticket_id(
        ticket_id,
        resolve_roadmap_ticket_authorities(),
    )
    if predecessor and not _closed_predecessor_ticket_id(state):
        state["closed_predecessor_ticket_id"] = predecessor
    state["next_ticket_id"] = ticket_id
    state["next_action"] = {
        "id": canonical_generation_action_id(ticket_id),
        "target_ticket_id": ticket_id,
    }
    return resolve_generation_target_from_workflow(state)


def _future_generation_validation_error(
    record: dict[str, Any],
    *,
    target: GovernedTicketGenerationTarget,
) -> str | None:
    try:
        validate_generation_record(record, target=target)
    except TicketArchitectBridgeConflict as exc:
        return str(exc) or "generated authority validation failed"
    return None


def _generation_completed_structurally(record: dict[str, Any]) -> bool:
    required_fields = (
        "ticket_spec_SHA256",
        "dependency_plan_SHA256",
        "lint_report_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
        "workflow_transition_result_SHA256",
        "ticket_spec",
        "dependency_plan",
        "lint_report",
        "work_packet_compilation_result",
        "workflow_transition_result",
    )
    return all(record.get(field) is not None and record.get(field) != "" for field in required_fields)


def _future_reconciliation_blockers(record: dict[str, Any], *, path: Path) -> list[str]:
    blockers: list[str] = []
    if record.get("human_ticket_approval_present") is True:
        blockers.append("human ticket approval is recorded")
    for field_name in (
        "ticket_execution_authorized",
        "WorkPacket_execution_authorized",
        "runtime_execution_authorized",
        "worker_execution",
        "Kanban_dispatch",
        "Git_mutation",
    ):
        if record.get(field_name) is not False:
            blockers.append(f"{field_name} crossed boundary")
    for field_name in (
        "provider_dispatch_count",
        "model_inference_count",
        "Git_commands_executed",
        "Docker_commands_executed",
        "Graphify_commands_executed",
    ):
        if record.get(field_name) not in {0, None}:
            blockers.append(f"{field_name} is nonzero")
    blockers.extend(_downstream_authority_blockers(_safe_ticket_id(record.get("ticket_id")), path=path))
    return blockers


def _downstream_authority_blockers(ticket_id: str, *, path: Path) -> list[str]:
    blockers: list[str] = []
    root = get_hermes_home() / "agent-platform"
    if not root.exists():
        return blockers
    current_path = path.resolve()
    reconciliation_root = (get_hermes_home() / _RECONCILIATION_STORE_DIR).resolve()
    for candidate in sorted(root.glob("**/*.json")):
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved == current_path:
            continue
        try:
            resolved.relative_to(reconciliation_root)
            continue
        except ValueError:
            pass
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if _authority_record_targets_ticket(data, ticket_id):
            blockers.append(f"downstream authority exists at {candidate}")
    return blockers


def _authority_record_targets_ticket(value: object, ticket_id: str) -> bool:
    return isinstance(value, dict) and any(
        value.get(field_name) == ticket_id
        for field_name in (
            "ticket_id",
            "approval_id",
            "current_ticket_id",
            "target_ticket_id",
        )
    )


def _reconciliation_absent_result(ticket_id: str, path: Path) -> dict[str, Any]:
    return {
        "source_system": "pepper-ticket-architect-bridge",
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "ticket_id": ticket_id,
        "record_path": str(path),
        "classification": "no_future_ticket_generation_authority",
        "reconcilable": False,
        "reconciled": False,
        "idempotent_replay": False,
        "ticket_generated": False,
    }


def _append_reconciliation_history(
    path: Path,
    *,
    record: dict[str, Any],
    target: GovernedTicketGenerationTarget,
    validation_error: str,
    quarantine_path: Path,
) -> dict[str, Any]:
    entry = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": "pepper-ticket-architect-stale-future-authority-reconciliation-v1",
        "source_system": "pepper-ticket-architect-bridge",
        "reconciled_at": _utc_now_iso(),
        "classification": "unaccepted_partial_failed_future_ticket_authority",
        "ticket_id": target.ticket_id,
        "bridge_SHA256": record["bridge_SHA256"],
        "validation_error": validation_error,
        "expected_roadmap_authority_path": target.roadmap_authority_path,
        "actual_roadmap_authority_path": record.get("roadmap_authority_path"),
        "source_next_action_id": record.get("source_next_action_id"),
        "quarantine_path": str(quarantine_path),
        "quarantine_path_relative": str(
            _RECONCILIATION_STORE_DIR / quarantine_path.name
        ).replace("\\", "/"),
        "ticket_generated": False,
        "human_ticket_approval_present": False,
        "execution_ready": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
    }
    entry["reconciliation_SHA256"] = _reconciliation_record_digest(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    return entry


def _load_existing_reconciliation(path: Path, bridge_sha256: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict) and entry.get("bridge_SHA256") == bridge_sha256:
            return entry
    return None


def _operational_result(record: dict[str, Any], *, idempotent_replay: bool) -> dict[str, Any]:
    target = _target_from_record(record)
    authority = _authority_projection(record)
    return {
        "source_system": "pepper-ticket-architect-bridge",
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_ARCHITECT_BRIDGE_POLICY_ID,
        "idempotent_replay": idempotent_replay,
        "generation_status": "awaiting_ticket_approval",
        "project_id": target.project_id,
        "macroproject_id": target.macroproject_id,
        "ticket_id": target.ticket_id,
        "ticket_title": target.ticket_title,
        "canonical_roadmap_authority": target.canonical_roadmap_authority,
        "roadmap_authority_path": target.roadmap_authority_path,
        "roadmap_authority_section": target.roadmap_authority_section,
        "roadmap_dependency_ticket_ids": list(target.dependency_ticket_ids),
        "roadmap_dependency_metadata": list(_roadmap_dependency_metadata(target)),
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
            "id": target.approval_next_action_id,
            "label": f"Human ticket approval required before {target.ticket_id} execution.",
            "target_ticket_id": target.ticket_id,
            "target_ticket_title": target.ticket_title,
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
    ticket_id = _safe_ticket_id(record.get("ticket_id"))
    return {
        "authority_record": str(_STORE_DIR / f"{ticket_id}.json").replace("\\", "/"),
        "bridge_SHA256": record["bridge_SHA256"],
        "ticket_spec_SHA256": record["ticket_spec_SHA256"],
        "dependency_plan_SHA256": record["dependency_plan_SHA256"],
        "lint_report_SHA256": record["lint_report_SHA256"],
        "work_packet_id": record["work_packet_id"],
        "work_packet_SHA256": record["work_packet_SHA256"],
        "workflow_transition_result_SHA256": record["workflow_transition_result_SHA256"],
    }


def _canonical_next_ticket_authority_projection(
    target: GovernedTicketGenerationTarget,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "project_id": target.project_id,
        "project_name": target.project_name,
        "macroproject_id": target.macroproject_id,
        "macroproject_title": target.macroproject_title,
        "ticket_id": target.ticket_id,
        "ticket_title": target.ticket_title,
        "next_action_id": target.next_action_id,
        "canonical_roadmap_authority": target.canonical_roadmap_authority,
        "roadmap_authority_path": canonical_roadmap_authority_path(target.roadmap_authority_path),
        "roadmap_authority_section": target.roadmap_authority_section,
        "dependency_ticket_ids": list(target.dependency_ticket_ids),
        "predecessor_ticket_id": target.predecessor_ticket_id,
        "readiness_state": target.readiness_state,
        "authority_source": target.authority_source,
    }
    if target.ticket_contract:
        record["ticket_contract"] = _json_ready_contract(target.ticket_contract)
        record["ticket_contract_SHA256"] = _ticket_contract_digest(target.ticket_contract)
    return record


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


def _require_identity(
    record: dict[str, Any],
    *,
    target: GovernedTicketGenerationTarget,
) -> None:
    expected = {
        "schema_version": TICKET_ARCHITECT_BRIDGE_SCHEMA_VERSION,
        "policy_id": TICKET_ARCHITECT_BRIDGE_POLICY_ID,
        "project_id": target.project_id,
        "macroproject_id": target.macroproject_id,
        "ticket_id": target.ticket_id,
        "ticket_title": target.ticket_title,
        "source_next_action_id": target.next_action_id,
        "canonical_roadmap_authority": target.canonical_roadmap_authority,
        "idempotency_key": target.idempotency_key,
        "generation_status": "awaiting_ticket_approval",
    }
    if target.ticket_id == CANONICAL_TICKET_ID:
        if record.get("roadmap_authority_path") not in {None, target.roadmap_authority_path}:
            raise TicketArchitectBridgeConflict("generated authority roadmap_authority_path mismatch")
        if record.get("roadmap_authority_section") not in {None, target.roadmap_authority_section}:
            raise TicketArchitectBridgeConflict("generated authority roadmap_authority_section mismatch")
    else:
        expected["roadmap_authority_path"] = canonical_roadmap_authority_path(target.roadmap_authority_path)
        expected["roadmap_authority_section"] = target.roadmap_authority_section
        expected["roadmap_dependency_ticket_ids"] = list(target.dependency_ticket_ids)
        expected["roadmap_dependency_metadata"] = list(_roadmap_dependency_metadata(target))
        expected["predecessor_ticket_id"] = target.predecessor_ticket_id
        expected["canonical_next_ticket_authority"] = _canonical_next_ticket_authority_projection(
            target
        )
    if target.ticket_contract:
        expected["ticket_contract"] = _json_ready_contract(target.ticket_contract)
        expected["ticket_contract_SHA256"] = _ticket_contract_digest(target.ticket_contract)
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


def _ticket_contract_digest(contract: dict[str, Any]) -> str:
    encoded = json.dumps(
        {
            "algorithm": TICKET_ARCHITECT_CONTRACT_DIGEST_ALGORITHM,
            "contract": _normalize(_json_ready_contract(contract)),
        },
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


def _reconciliation_record_digest(record: dict[str, Any]) -> str:
    payload = {
        key: value for key, value in record.items() if key != "reconciliation_SHA256"
    }
    encoded = json.dumps(
        {
            "algorithm": TICKET_ARCHITECT_RECONCILIATION_DIGEST_ALGORITHM,
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
    "generation_record_path_for_ticket",
    "reconciliation_history_path_for_ticket",
    "quarantined_generation_record_path",
    "approval_decision_record_path",
    "load_generation_record",
    "load_p18_9_0_generation_record",
    "load_p18_9_0_approval_decision_record",
    "validate_generation_record",
    "validate_p18_9_0_generation_record",
    "validate_p18_9_0_approval_decision_record",
    "inspect_invalid_future_ticket_authority",
    "reconcile_invalid_future_ticket_authority",
    "generate_p18_9_0_ticket",
    "generate_current_ticket",
    "resolve_canonical_next_ticket",
    "resolve_generation_target_from_workflow",
    "generated_record_to_workflow_overlay",
    "apply_p18_9_0_approval_decision",
)
