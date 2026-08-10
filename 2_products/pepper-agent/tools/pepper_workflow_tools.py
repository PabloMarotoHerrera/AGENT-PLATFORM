"""Pepper Lead Agent read-only governed workflow tools."""

from __future__ import annotations

import json
from typing import Any

from tools.registry import registry, tool_error


TOOLSET = "pepper_workflow"
DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def _limit(args: dict[str, Any], default: int = DEFAULT_LIMIT) -> int:
    try:
        value = int(args.get("limit", default))
    except (TypeError, ValueError):
        value = default
    return max(1, min(MAX_LIMIT, value))


def _runtime():
    from hermes_cli.agent_platform import product_runtime

    return product_runtime


def _context() -> dict[str, Any]:
    return _runtime().build_lead_agent_operational_context()


def _result(payload: dict[str, Any]) -> str:
    return json.dumps({"success": True, **payload}, ensure_ascii=False)


def _get_current_project(args: dict[str, Any], **_kwargs) -> str:
    ctx = _context()
    return _result({
        "source_tool": "get_current_project",
        "source_system": ctx["source_system"],
        "product_id": ctx["product_id"],
        "project_id": ctx["project_id"],
        "project_name": ctx["project_name"],
        "macroproject_id": ctx["macroproject_id"],
        "macroproject_title": ctx["macroproject_title"],
        "repository_identity_note": (
            "Governed project identity is PEPPER; repository/product directory "
            "names are not the project authority."
        ),
        "evidence_timestamp": ctx["evidence_timestamp"],
        "evidence_version": ctx["evidence_version"],
    })


def _get_current_ticket(args: dict[str, Any], **_kwargs) -> str:
    ctx = _context()
    return _result({
        "source_tool": "get_current_ticket",
        "source_system": ctx["source_system"],
        "available": ctx["available"],
        "message": ctx["message"],
        "project_id": ctx["project_id"],
        "current_ticket_id": ctx["current_ticket_id"],
        "current_ticket_title": ctx["current_ticket_title"],
        "current_gap_id": ctx["current_gap_id"],
        "current_gap_title": ctx["current_gap_title"],
        "next_action": ctx["next_action"],
        "evidence_timestamp": ctx["evidence_timestamp"],
        "evidence_version": ctx["evidence_version"],
    })


def _get_workflow_control(args: dict[str, Any], **_kwargs) -> str:
    ctx = _context()
    return _result({
        "source_tool": "get_workflow_control",
        "source_system": ctx["source_system"],
        "product_id": ctx["product_id"],
        "project_id": ctx["project_id"],
        "current_ticket_id": ctx["current_ticket_id"],
        "workflow_state": ctx["workflow_state"],
        "workflow_status": ctx["workflow_status"],
        "approval_state": ctx["approval_state"],
        "pending_approval_count": ctx["pending_approval_count"],
        "queue_state": ctx["queue_state"],
        "execution_state": ctx["execution_state"],
        "active_execution_count": ctx["active_execution_count"],
        "validation_state": ctx["validation_state"],
        "review_state": ctx["review_state"],
        "recovery_state": ctx["recovery_state"],
        "git_handoff_state": ctx["git_handoff_state"],
        "blocker_count": ctx["blocker_count"],
        "warning_count": ctx["warning_count"],
        "next_action": ctx["next_action"],
        "evidence_timestamp": ctx["evidence_timestamp"],
        "evidence_version": ctx["evidence_version"],
        "workflow_control": ctx["workflow_control"],
    })


def _get_pending_approvals(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    source = pr.build_approval_inbox_source()
    approvals = source.get("approvals", [])
    if not isinstance(approvals, list):
        approvals = []
    count = len(approvals)
    return _result({
        "source_tool": "get_pending_approvals",
        "source_system": source.get("source_system", pr.APPROVAL_SOURCE_SYSTEM),
        "approval_state": "pending_approvals" if count else "no_pending_approvals",
        "pending_approval_count": count,
        "message": "pending approvals found" if count else "no pending approvals",
        "approvals": approvals[:_limit(args)],
    })


def _inspect_pending_approval(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    approval_id = str(args.get("approval_id") or "").strip()
    if not approval_id:
        inbox = pr.build_approval_inbox_source()
        approvals = inbox.get("approvals", [])
        if not isinstance(approvals, list) or not approvals:
            return _result({
                "source_tool": "inspect_pending_approval",
                "source_system": inbox.get("source_system", pr.APPROVAL_SOURCE_SYSTEM),
                "approval_state": "no_pending_approvals",
                "pending_approval_count": 0,
                "message": "no pending approvals",
                "approval": None,
            })
        first = approvals[0]
        if not isinstance(first, dict):
            return tool_error("pending approval projection is malformed")
        approval_id = str(first.get("id") or "").strip()
    if not approval_id:
        return tool_error("approval_id is required when no pending approval can be selected")
    detail = pr.build_approval_detail_source(approval_id)
    return _result({
        "source_tool": "inspect_pending_approval",
        "source_system": detail.get("source_system", pr.APPROVAL_SOURCE_SYSTEM),
        "approval_state": "pending_approval_inspected",
        "approval": detail.get("approval"),
        "evidence": detail.get("evidence", []),
        "decisions": detail.get("decisions", []),
        "auto_approval": False,
    })


def _get_execution_status(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    source = pr.build_execution_collection_source()
    executions = source.get("executions", [])
    if not isinstance(executions, list):
        executions = []
    active = [
        record for record in executions
        if isinstance(record, dict) and pr._execution_is_active(record)
    ]
    return _result({
        "source_tool": "get_execution_status",
        "source_system": source.get("source_system", pr.CONTROLLED_EXECUTION_SOURCE_SYSTEM),
        "execution_state": "active_executions" if active else "no_active_executions",
        "execution_count": len(executions),
        "active_execution_count": len(active),
        "message": "active executions found" if active else "no active executions",
        "active_executions": active[:_limit(args)],
        "recent_executions": executions[:_limit(args)],
        "auto_execution": False,
    })


def _get_review_status(args: dict[str, Any], **_kwargs) -> str:
    ctx = _context()
    return _result({
        "source_tool": "get_review_status",
        "source_system": ctx["source_system"],
        "validation_state": ctx["validation_state"],
        "review_state": ctx["review_state"],
        "recovery_state": ctx["recovery_state"],
        "git_handoff_state": ctx["git_handoff_state"],
        "blocker_count": ctx["blocker_count"],
        "warning_count": ctx["warning_count"],
        "next_action": ctx["next_action"],
        "evidence_timestamp": ctx["evidence_timestamp"],
        "evidence_version": ctx["evidence_version"],
    })


def _get_next_action(args: dict[str, Any], **_kwargs) -> str:
    ctx = _context()
    return _result({
        "source_tool": "get_next_action",
        "source_system": ctx["source_system"],
        "project_id": ctx["project_id"],
        "current_ticket_id": ctx["current_ticket_id"],
        "workflow_status": ctx["workflow_status"],
        "next_action": ctx["next_action"],
        "next_action_label": ctx["next_action_label"],
        "external_dashboard_state_copy_required": False,
        "external_ChatGPT_required": False,
        "auto_execution": False,
        "auto_retry": False,
        "auto_rollback": False,
        "Git_mutation": False,
        "evidence_timestamp": ctx["evidence_timestamp"],
        "evidence_version": ctx["evidence_version"],
    })


_EMPTY_SCHEMA = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


_LIMIT_SCHEMA = {
    "type": "object",
    "properties": {
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": MAX_LIMIT,
            "description": "Maximum number of bounded records to return.",
        }
    },
    "additionalProperties": False,
}


registry.register(
    name="get_current_project",
    toolset=TOOLSET,
    schema={
        "name": "get_current_project",
        "description": "Read Pepper's governed project identity. Do not infer it from cwd.",
        "parameters": _EMPTY_SCHEMA,
    },
    handler=_get_current_project,
    emoji="P",
)

registry.register(
    name="get_current_ticket",
    toolset=TOOLSET,
    schema={
        "name": "get_current_ticket",
        "description": "Read the active governed Pepper ticket and GAP context.",
        "parameters": _EMPTY_SCHEMA,
    },
    handler=_get_current_ticket,
    emoji="T",
)

registry.register(
    name="get_workflow_control",
    toolset=TOOLSET,
    schema={
        "name": "get_workflow_control",
        "description": "Read Pepper workflow-control state from the product runtime projection.",
        "parameters": _EMPTY_SCHEMA,
    },
    handler=_get_workflow_control,
    emoji="W",
    max_result_size_chars=24000,
)

registry.register(
    name="get_pending_approvals",
    toolset=TOOLSET,
    schema={
        "name": "get_pending_approvals",
        "description": "List pending Pepper approvals from the live governed approval backend.",
        "parameters": _LIMIT_SCHEMA,
    },
    handler=_get_pending_approvals,
    emoji="A",
)

registry.register(
    name="inspect_pending_approval",
    toolset=TOOLSET,
    schema={
        "name": "inspect_pending_approval",
        "description": "Inspect one pending approval without approving or rejecting it.",
        "parameters": {
            "type": "object",
            "properties": {
                "approval_id": {
                    "type": "string",
                    "description": "Optional approval id. Omit to inspect the first pending approval.",
                }
            },
            "additionalProperties": False,
        },
    },
    handler=_inspect_pending_approval,
    emoji="I",
)

registry.register(
    name="get_execution_status",
    toolset=TOOLSET,
    schema={
        "name": "get_execution_status",
        "description": "Read active and recent Pepper controlled executions without dispatching work.",
        "parameters": _LIMIT_SCHEMA,
    },
    handler=_get_execution_status,
    emoji="E",
    max_result_size_chars=24000,
)

registry.register(
    name="get_review_status",
    toolset=TOOLSET,
    schema={
        "name": "get_review_status",
        "description": "Read Pepper validation, review, recovery, and Git handoff state.",
        "parameters": _EMPTY_SCHEMA,
    },
    handler=_get_review_status,
    emoji="R",
)

registry.register(
    name="get_next_action",
    toolset=TOOLSET,
    schema={
        "name": "get_next_action",
        "description": "Read Pepper's next governed action from workflow-control state.",
        "parameters": _EMPTY_SCHEMA,
    },
    handler=_get_next_action,
    emoji="N",
)
