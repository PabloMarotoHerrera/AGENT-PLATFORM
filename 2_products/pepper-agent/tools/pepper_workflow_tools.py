"""Pepper Lead Agent bounded governed workflow tools."""

from __future__ import annotations

import json
import re
import unicodedata
from typing import Any

from tools.registry import registry, tool_error


TOOLSET = "pepper_workflow"
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
CURRENT_TICKET_APPROVAL_ID = "P18.9.0"
CURRENT_TICKET_START_NEXT_ACTION_ID = "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
CURRENT_TICKET_RECOVERY_NEXT_ACTION_ID = "RECOVER_P18_9_0_EXECUTION"
CURRENT_TICKET_RETRY_START_NEXT_ACTION_ID = "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
CURRENT_TICKET_REVIEW_PREPARE_NEXT_ACTION_ID = "PREPARE_P18_9_0_REVIEW"
CURRENT_TICKET_REVIEW_ACCEPTANCE_NEXT_ACTION_ID = "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"
CURRENT_TICKET_RECOVERY_AUTHORIZATION_TEXT = (
    "Autorizo explícitamente la recuperación de la ejecución fallida de P18.9.0."
)
CURRENT_TICKET_REVIEW_ACCEPTANCE_TEXT = (
    "Acepto explícitamente la review de P18.9.0 y el resultado preparado para aceptación humana."
)
CURRENT_TICKET_RETRY_START_AUTHORIZATION_TEXTS = frozenset({
    "Autorizo explícitamente el retry de P18.9.0.",
    "Reintenta P18.9.0.",
    "Inicia el segundo intento de P18.9.0.",
})
CURRENT_PROJECT_ID = "PEPPER"


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


def _normalize_intent_text(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").strip())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.lower()


def _mentioned_ticket_ids(text: str) -> set[str]:
    return {
        match.group(0).replace("_", ".").replace("-", ".").upper()
        for match in re.finditer(r"\bp\d+(?:[._-]\d+)+\b", text, flags=re.IGNORECASE)
    }


def _ticket_action_token(ticket_id: str) -> str:
    return str(ticket_id or "").strip().replace(".", "_").upper()


def _approval_action_id(ticket_id: str) -> str:
    return f"APPROVE_{_ticket_action_token(ticket_id)}"


def _validate_explicit_human_decision(
    *,
    decision: str,
    human_decision_text: object,
    current_ticket_id: str,
) -> str:
    raw = str(human_decision_text or "").strip()
    if not raw:
        raise ValueError("human_decision_text is required")
    normalized = _normalize_intent_text(raw)
    if "?" in raw or "¿" in raw:
        raise ValueError("approval decision text must not be a question")
    if any(
        phrase in normalized
        for phrase in (
            "creo que",
            "pienso que",
            "tal vez",
            "quizas",
            "quiza",
            "maybe",
            "probably",
            "what if",
            "que pasa si",
            "si lo apruebo",
        )
    ):
        raise ValueError("approval decision text is ambiguous")

    ticket_ids = _mentioned_ticket_ids(normalized)
    if ticket_ids and current_ticket_id not in ticket_ids:
        raise ValueError("approval decision text targets a different ticket")

    approval_intent = bool(
        re.search(r"\b(apruebo|aprueba|apruebalo|aprobar|aprobado|approve|approved)\b", normalized)
    )
    rejection_intent = bool(
        re.search(r"\b(rechazo|rechaza|rechazalo|rechazar|rechazado|reject|rejected|deny|denied)\b", normalized)
    )
    if approval_intent and rejection_intent:
        raise ValueError("approval decision text contains conflicting decisions")
    if decision == "approve" and not approval_intent:
        raise ValueError("explicit human approval text is required")
    if decision == "reject" and not rejection_intent:
        raise ValueError("explicit human rejection text is required")
    return raw


def _validate_optional_current_approval_guards(args: dict[str, Any], context: dict[str, Any]) -> str:
    current_ticket_id = str(context.get("current_ticket_id") or "").strip()
    if not current_ticket_id:
        raise ValueError("no current pending ticket approval is active")
    approval_id = str(args.get("approval_id") or current_ticket_id).strip()
    if approval_id != current_ticket_id:
        raise ValueError("approval guard does not match the current pending ticket")
    if str(args.get("project_id") or CURRENT_PROJECT_ID).strip() != CURRENT_PROJECT_ID:
        raise ValueError("active governed project must be PEPPER")
    if str(args.get("ticket_id") or current_ticket_id).strip() != current_ticket_id:
        raise ValueError("ticket guard does not match the current pending ticket")
    expected_next_action = _approval_action_id(current_ticket_id)
    next_action_id = str(args.get("next_action_id") or expected_next_action).strip()
    if next_action_id != expected_next_action:
        raise ValueError(f"approval next action must be {expected_next_action}")
    return approval_id


def _validate_optional_current_ticket_digests(args: dict[str, Any], context: dict[str, Any]) -> None:
    authority = context.get("workflow_control", {}).get("generated_ticket_authority")
    if not isinstance(authority, dict):
        authority = context.get("generated_ticket_authority")
    if not isinstance(authority, dict):
        raise ValueError("current generated ticket authority is unavailable")
    checks = (
        ("ticket_spec_sha256", "ticket_spec_SHA256", "TicketSpec digest"),
        ("work_packet_id", "work_packet_id", "WorkPacket ID"),
        ("work_packet_sha256", "work_packet_SHA256", "WorkPacket digest"),
    )
    for arg_name, authority_name, label in checks:
        supplied = str(args.get(arg_name) or "").strip()
        if supplied and supplied != str(authority.get(authority_name) or "").strip():
            raise ValueError(f"{label} does not match current pending ticket authority")


def _validate_pending_current_ticket_approval(
    *,
    context: dict[str, Any],
    approval: dict[str, Any],
) -> None:
    if context.get("project_id") != CURRENT_PROJECT_ID:
        raise ValueError("current project is not PEPPER")
    if context.get("macroproject_id") != "P18.9":
        raise ValueError("current macroproject is not P18.9")
    current_ticket_id = str(context.get("current_ticket_id") or "").strip()
    if not current_ticket_id:
        raise ValueError("no current active ticket approval")
    next_action = context.get("next_action")
    if not isinstance(next_action, dict):
        raise ValueError("current next action is unavailable")
    expected_next_action = _approval_action_id(current_ticket_id)
    if next_action.get("id") != expected_next_action:
        raise ValueError(f"current next action is not {expected_next_action}")
    if next_action.get("target_ticket_id") != current_ticket_id:
        raise ValueError(f"current next action does not target {current_ticket_id}")
    if approval.get("id") != current_ticket_id:
        raise ValueError("approval target mismatch")
    if approval.get("status") != "pending":
        raise ValueError("approval is not pending")
    if approval.get("request_type") != "ticket_approval":
        raise ValueError("approval is not a ticket approval")
    target = approval.get("target")
    if not isinstance(target, dict):
        raise ValueError("approval target is unavailable")
    if current_ticket_id not in str(target.get("label") or ""):
        raise ValueError(f"approval target does not match {current_ticket_id}")


def _validate_current_ticket_identity_context(context: dict[str, Any]) -> None:
    if context.get("project_id") != CURRENT_PROJECT_ID:
        raise ValueError("current project is not PEPPER")
    if context.get("macroproject_id") != "P18.9":
        raise ValueError("current macroproject is not P18.9")
    if not str(context.get("current_ticket_id") or "").strip():
        raise ValueError("no current active ticket")


def _validate_explicit_projection_request(value: object, *, current_ticket_id: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_request_text is required")
    normalized = _normalize_intent_text(raw)
    if "?" in raw or "¿" in raw:
        raise ValueError("projection request text must not be a question")
    ticket_ids = _mentioned_ticket_ids(normalized)
    if ticket_ids and current_ticket_id not in ticket_ids:
        raise ValueError("projection request text targets a different ticket")
    if not re.search(r"\b(prepara|preparar|prepare|project|proyecta|proyectar|kanban|ejecucion|execution)\b", normalized):
        raise ValueError("explicit preparation/projection request text is required")
    return raw


def _validate_explicit_generation_request(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_request_text is required")
    normalized = _normalize_intent_text(raw)
    if "?" in raw or "¿" in raw:
        raise ValueError("generation request text must not be a question")
    if any(
        phrase in normalized
        for phrase in (
            "parece correcto",
            "parece bien",
            "podemos continuar",
            "can we continue",
            "looks correct",
            "looks good",
            "seems right",
        )
    ):
        raise ValueError("generation request text is ambiguous")
    if not re.search(r"\b(generate|generar|genera|crear|crea|create)\b", normalized):
        raise ValueError("explicit governed ticket generation request text is required")
    return raw


def _validate_explicit_reconciliation_request(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_request_text is required")
    normalized = _normalize_intent_text(raw)
    if "?" in raw or "¿" in raw:
        raise ValueError("reconciliation request text must not be a question")
    if not re.search(r"\b(reconcile|reconciliar|quarantine|cuarentena|invalidar|invalidate)\b", normalized):
        raise ValueError("explicit stale-authority reconciliation request text is required")
    return raw


def _validate_explicit_start_request(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_authorization_text is required")
    normalized = _normalize_intent_text(raw)
    if "?" in raw or "¿" in raw:
        raise ValueError("execution start authorization text must not be a question")
    if any(
        phrase in normalized
        for phrase in (
            "creo que",
            "pienso que",
            "tal vez",
            "parece que",
            "quizas",
            "quiza",
            "maybe",
            "probably",
            "looks like",
            "what if",
            "que pasa si",
            "si lo ejecuto",
            "if i start",
        )
    ):
        raise ValueError("execution start authorization text is ambiguous")
    ticket_ids = _mentioned_ticket_ids(normalized)
    if ticket_ids and CURRENT_TICKET_APPROVAL_ID not in ticket_ids:
        raise ValueError("execution start authorization targets a different ticket")
    if "recuperacion" in normalized or "recuperar" in normalized or "recovery" in normalized:
        raise ValueError("execution start authorization must not be recovery authorization")
    retry_intent = bool(
        re.search(r"\b(retry|reintenta|reintentar|reintento)\b", normalized)
        or "segundo intento" in normalized
        or "volver a ejecutar" in normalized
    )
    if retry_intent and raw not in CURRENT_TICKET_RETRY_START_AUTHORIZATION_TEXTS:
        raise ValueError("exact explicit P18.9.0 retry-start authorization text is required")
    if not re.search(
        r"\b(start|execute|execution|dispatch|run|retry|authorize|authorized|authorization|inicia|iniciar|inicio|ejecuta|ejecutar|ejecucion|despacha|despachar|lanza|lanzar|arranca|arrancar|autoriza|autorizo|autorizar|autorizado|autorizacion|reintenta|reintentar|reintento)\b",
        normalized,
    ):
        raise ValueError("explicit execution start authorization text is required")
    return raw


def _validate_explicit_recovery_request(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_authorization_text is required")
    if "?" in raw or "¿" in raw:
        raise ValueError("execution recovery authorization text must not be a question")
    if raw != CURRENT_TICKET_RECOVERY_AUTHORIZATION_TEXT:
        raise ValueError(
            "exact explicit P18.9.0 recovery authorization text is required"
        )
    return raw


def _validate_explicit_review_prepare_request(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_request_text is required")
    normalized = _normalize_intent_text(raw)
    if "?" in raw or "¿" in raw:
        raise ValueError("review preparation request text must not be a question")
    if any(
        phrase in normalized
        for phrase in (
            "creo que",
            "pienso que",
            "tal vez",
            "parece que",
            "quizas",
            "quiza",
            "maybe",
            "probably",
            "looks like",
            "what if",
            "que pasa si",
        )
    ):
        raise ValueError("review preparation request text is ambiguous")
    ticket_ids = _mentioned_ticket_ids(normalized)
    if ticket_ids and CURRENT_TICKET_APPROVAL_ID not in ticket_ids:
        raise ValueError("review preparation request targets a different ticket")
    if not re.search(
        r"\b(prepare|prepara|preparar|review|revision|validacion|validation|validar|acceptance|aceptacion)\b",
        normalized,
    ):
        raise ValueError("explicit P18.9.0 review preparation request text is required")
    return raw


def _validate_explicit_review_acceptance_request(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_acceptance_text is required")
    if "?" in raw or "¿" in raw:
        raise ValueError("review acceptance text must not be a question")
    if raw != CURRENT_TICKET_REVIEW_ACCEPTANCE_TEXT:
        raise ValueError("exact explicit P18.9.0 review acceptance text is required")
    return raw


def _start_authorization_text_from_args_or_user_task(
    args: dict[str, Any],
    kwargs: dict[str, Any],
) -> object:
    value = args.get("human_authorization_text")
    if str(value or "").strip():
        return value
    return kwargs.get("user_task")


def _recovery_authorization_text_from_args_or_user_task(
    args: dict[str, Any],
    kwargs: dict[str, Any],
) -> object:
    value = args.get("human_authorization_text")
    if str(value or "").strip():
        return value
    return kwargs.get("user_task")


def _review_prepare_request_text_from_args_or_user_task(
    args: dict[str, Any],
    kwargs: dict[str, Any],
) -> object:
    value = args.get("human_request_text")
    if str(value or "").strip():
        return value
    return kwargs.get("user_task")


def _review_acceptance_text_from_args_or_user_task(
    args: dict[str, Any],
    kwargs: dict[str, Any],
) -> object:
    value = args.get("human_acceptance_text")
    if str(value or "").strip():
        return value
    return kwargs.get("user_task")


def _generation_request_text_from_args_or_user_task(
    args: dict[str, Any],
    kwargs: dict[str, Any],
) -> object:
    value = args.get("human_request_text")
    if str(value or "").strip():
        return value
    return kwargs.get("user_task")


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
        "next_ticket_id": ctx["next_ticket_id"],
        "next_ticket_title": ctx["next_ticket_title"],
        "workflow_state": ctx["workflow_state"],
        "workflow_status": ctx["workflow_status"],
        "approval_state": ctx["approval_state"],
        "pending_approval_count": ctx["pending_approval_count"],
        "pending_ticket_approval_count": ctx["pending_ticket_approval_count"],
        "queue_state": ctx["queue_state"],
        "execution_state": ctx["execution_state"],
        "active_execution_count": ctx["active_execution_count"],
        "validation_state": ctx["validation_state"],
        "review_state": ctx["review_state"],
        "recovery_state": ctx["recovery_state"],
        "failure_category": ctx.get("failure_category"),
        "failure_summary": ctx.get("failure_summary"),
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


def _decide_pending_approval(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    decision = str(args.get("decision") or "").strip().lower()
    if decision not in {"approve", "reject"}:
        return tool_error("decision must be approve or reject", success=False)
    try:
        context = pr.build_lead_agent_operational_context()
        _validate_current_ticket_identity_context(context)
        approval_id = _validate_optional_current_approval_guards(args, context)
        human_decision_text = _validate_explicit_human_decision(
            decision=decision,
            human_decision_text=args.get("human_decision_text"),
            current_ticket_id=str(context["current_ticket_id"]),
        )
        _validate_optional_current_ticket_digests(args, context)
        approvals = context.get("approvals", {}).get("items", [])
        if not isinstance(approvals, list):
            approvals = []
        pending_match = next(
            (
                approval for approval in approvals
                if isinstance(approval, dict) and approval.get("id") == approval_id
            ),
            None,
        )
        if pending_match is not None:
            _validate_pending_current_ticket_approval(
                context=context,
                approval=pending_match,
            )
        elif context.get("workflow_status") not in {"ticket_approved", "awaiting_correction"}:
            raise ValueError("current pending ticket approval is unavailable")
        result = pr.apply_approval_decision(
            approval_id,
            pr.ApprovalDecisionRequest(
                decision=decision,
                actor="pepper-chat-human",
            ),
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        return tool_error(str(exc) or "approval decision failed", success=False)

    return _result({
        "source_tool": "decide_pending_approval",
        "source_system": result.get("source_system", pr.APPROVAL_SOURCE_SYSTEM),
        "approval_id": approval_id,
        "decision": result.get("decision", decision),
        "status": result.get("status"),
        "applied": result.get("applied", True),
        "idempotent_replay": bool(result.get("idempotent_replay", False)),
        "actor": result.get("actor"),
        "human_decision_text": human_decision_text,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "workflow_state": updated_context.get("workflow_state"),
        "workflow_status": updated_context.get("workflow_status"),
        "approval_state": updated_context.get("approval_state"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "pending_ticket_approval_count": updated_context.get("pending_ticket_approval_count"),
        "next_action": updated_context.get("next_action"),
        "workflow_transition_id": result.get("workflow_transition_id"),
        "ticket_execution_authorized": False,
        "WorkPacket_execution_authorized": False,
        "runtime_execution_authorized": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "WorkPacket_compilation_count": result.get("WorkPacket_compilation_count"),
        "WorkPacket_recompile_required": result.get("WorkPacket_recompile_required"),
        "auto_approval": False,
        "auto_execution": False,
        "auto_retry": False,
        "auto_rollback": False,
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
        "failure_category": ctx.get("failure_category"),
        "failure_summary": ctx.get("failure_summary"),
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
        "next_ticket_id": ctx["next_ticket_id"],
        "next_ticket_title": ctx["next_ticket_title"],
        "workflow_status": ctx["workflow_status"],
        "recovery_state": ctx["recovery_state"],
        "failure_category": ctx.get("failure_category"),
        "failure_summary": ctx.get("failure_summary"),
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


def _generate_current_ticket(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        human_request_text = _validate_explicit_generation_request(
            _generation_request_text_from_args_or_user_task(args, _kwargs)
        )
        result = pr.generate_current_governed_ticket(
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
            next_action_id=str(args.get("next_action_id") or "").strip() or None,
        )
    except Exception as exc:
        return tool_error(str(exc) or "current governed ticket generation failed")
    return _result({
        "source_tool": "generate_current_ticket",
        "human_request_text": human_request_text,
        **result,
    })


def _reconcile_invalid_current_generation_authority(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        human_request_text = _validate_explicit_reconciliation_request(
            args.get("human_request_text")
        )
        result = pr.reconcile_invalid_current_generation_authority(
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        return tool_error(str(exc) or "invalid generation authority reconciliation failed")
    return _result({
        "source_tool": "reconcile_invalid_current_generation_authority",
        "human_request_text": human_request_text,
        **result,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "next_ticket_id": updated_context.get("next_ticket_id"),
        "next_ticket_title": updated_context.get("next_ticket_title"),
        "workflow_status": updated_context.get("workflow_status"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "active_execution_count": updated_context.get("active_execution_count"),
        "next_action": updated_context.get("next_action"),
    })


def _prepare_current_ticket_execution(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        context = pr.build_lead_agent_operational_context()
        current_ticket_id = str(context.get("current_ticket_id") or "").strip()
        if not current_ticket_id:
            raise ValueError("no current approved governed ticket is active")
        human_request_text = _validate_explicit_projection_request(
            args.get("human_request_text"),
            current_ticket_id=current_ticket_id,
        )
        result = pr.project_current_approved_workpacket_to_kanban(
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
            next_action_id=str(args.get("next_action_id") or "").strip() or None,
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        extra = {"success": False}
        blocker_code = getattr(exc, "blocker_code", None)
        diagnostics = getattr(exc, "diagnostics", None)
        if blocker_code:
            extra["blocker_code"] = blocker_code
        if isinstance(diagnostics, dict) and diagnostics:
            extra["profile_assignment_diagnostics"] = diagnostics
        return tool_error(str(exc) or "current approved WorkPacket projection failed", **extra)
    return _result({
        "source_tool": "prepare_current_ticket_execution",
        "human_request_text": human_request_text,
        **result,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "workflow_state": updated_context.get("workflow_state"),
        "workflow_status": updated_context.get("workflow_status"),
        "approval_state": updated_context.get("approval_state"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "pending_ticket_approval_count": updated_context.get("pending_ticket_approval_count"),
        "queue_state": updated_context.get("queue_state"),
        "execution_state": updated_context.get("execution_state"),
        "next_action": updated_context.get("next_action"),
        "dispatch_performed": False,
        "worker_execution": False,
        "execution_started": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
    })


def _start_current_ticket_execution(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        human_authorization_text = _validate_explicit_start_request(
            _start_authorization_text_from_args_or_user_task(args, _kwargs)
        )
        result = pr.start_current_ticket_execution(
            human_authorization_text=human_authorization_text,
            authorizer_id="pepper-chat-human",
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
            next_action_id=str(args.get("next_action_id") or "").strip() or None,
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        return tool_error(str(exc) or "current ticket execution start failed", success=False)
    return _result({
        "source_tool": "start_current_ticket_execution",
        "human_authorization_text": human_authorization_text,
        **result,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "workflow_state": updated_context.get("workflow_state"),
        "workflow_status": updated_context.get("workflow_status"),
        "approval_state": updated_context.get("approval_state"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "pending_ticket_approval_count": updated_context.get("pending_ticket_approval_count"),
        "queue_state": updated_context.get("queue_state"),
        "execution_state": updated_context.get("execution_state"),
        "next_action": updated_context.get("next_action"),
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    })


def _recover_current_ticket_execution(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        human_authorization_text = _validate_explicit_recovery_request(
            _recovery_authorization_text_from_args_or_user_task(args, _kwargs)
        )
        result = pr.recover_current_ticket_execution(
            human_authorization_text=human_authorization_text,
            authorizer_id="pepper-chat-human",
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
            next_action_id=str(args.get("next_action_id") or "").strip() or None,
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        return tool_error(str(exc) or "current ticket execution recovery failed", success=False)
    return _result({
        "source_tool": "recover_current_ticket_execution",
        "human_authorization_text": human_authorization_text,
        **result,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "workflow_state": updated_context.get("workflow_state"),
        "workflow_status": updated_context.get("workflow_status"),
        "approval_state": updated_context.get("approval_state"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "pending_ticket_approval_count": updated_context.get("pending_ticket_approval_count"),
        "queue_state": updated_context.get("queue_state"),
        "execution_state": updated_context.get("execution_state"),
        "recovery_state": updated_context.get("recovery_state"),
        "failure_category": updated_context.get("failure_category"),
        "failure_summary": updated_context.get("failure_summary"),
        "next_action": updated_context.get("next_action"),
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    })


def _prepare_current_ticket_review(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        human_request_text = _validate_explicit_review_prepare_request(
            _review_prepare_request_text_from_args_or_user_task(args, _kwargs)
        )
        result = pr.prepare_current_ticket_review(
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
            next_action_id=str(args.get("next_action_id") or "").strip() or None,
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        return tool_error(str(exc) or "current ticket review preparation failed", success=False)
    return _result({
        "source_tool": "prepare_current_ticket_review",
        "human_request_text": human_request_text,
        **result,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "workflow_state": updated_context.get("workflow_state"),
        "workflow_status": updated_context.get("workflow_status"),
        "approval_state": updated_context.get("approval_state"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "pending_ticket_approval_count": updated_context.get("pending_ticket_approval_count"),
        "queue_state": updated_context.get("queue_state"),
        "execution_state": updated_context.get("execution_state"),
        "validation_state": updated_context.get("validation_state"),
        "review_state": updated_context.get("review_state"),
        "git_handoff_state": updated_context.get("git_handoff_state"),
        "next_action": updated_context.get("next_action"),
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
    })


def _accept_current_ticket_review(args: dict[str, Any], **_kwargs) -> str:
    pr = _runtime()
    try:
        human_acceptance_text = _validate_explicit_review_acceptance_request(
            _review_acceptance_text_from_args_or_user_task(args, _kwargs)
        )
        result = pr.accept_current_ticket_review(
            human_acceptance_text=human_acceptance_text,
            acceptor_id="pepper-chat-human",
            project_id=str(args.get("project_id") or "").strip() or None,
            ticket_id=str(args.get("ticket_id") or "").strip() or None,
            next_action_id=str(args.get("next_action_id") or "").strip() or None,
        )
        updated_context = pr.build_lead_agent_operational_context()
    except Exception as exc:
        return tool_error(str(exc) or "current ticket review acceptance failed", success=False)
    return _result({
        "source_tool": "accept_current_ticket_review",
        "human_acceptance_text": human_acceptance_text,
        **result,
        "current_ticket_id": updated_context.get("current_ticket_id"),
        "workflow_state": updated_context.get("workflow_state"),
        "workflow_status": updated_context.get("workflow_status"),
        "approval_state": updated_context.get("approval_state"),
        "pending_approval_count": updated_context.get("pending_approval_count"),
        "pending_ticket_approval_count": updated_context.get("pending_ticket_approval_count"),
        "queue_state": updated_context.get("queue_state"),
        "execution_state": updated_context.get("execution_state"),
        "validation_state": updated_context.get("validation_state"),
        "review_state": updated_context.get("review_state"),
        "git_handoff_state": updated_context.get("git_handoff_state"),
        "next_action": updated_context.get("next_action"),
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "auto_retry": False,
        "auto_rollback": False,
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


_GENERATE_CURRENT_TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must equal the canonical next ticket if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must equal the current canonical generation action if supplied.",
        },
        "human_request_text": {
            "type": "string",
            "description": "Exact user text that explicitly requests generation of the current canonical next governed ticket.",
        },
    },
    "additionalProperties": False,
}


_RECONCILE_INVALID_CURRENT_GENERATION_AUTHORITY_SCHEMA = {
    "type": "object",
    "properties": {
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must equal the current canonical next ticket if supplied.",
        },
        "human_request_text": {
            "type": "string",
            "description": "Exact user text explicitly requesting stale generated-authority reconciliation.",
        },
    },
    "required": ["human_request_text"],
    "additionalProperties": False,
}


_DECIDE_PENDING_APPROVAL_SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {
            "type": "string",
            "enum": ["approve", "reject"],
            "description": "Explicit human decision for the current governed ticket approval.",
        },
        "human_decision_text": {
            "type": "string",
            "description": "Exact user phrase that explicitly approves or rejects the current ticket.",
        },
        "approval_id": {
            "type": "string",
            "description": "Optional approval guard. Must equal the current pending ticket approval if supplied.",
        },
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must equal the current pending ticket if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must equal APPROVE_<current-ticket-token> if supplied.",
        },
        "ticket_spec_sha256": {
            "type": "string",
            "description": "Optional TicketSpec SHA256 guard. Must match the current generated ticket authority if supplied.",
        },
        "work_packet_id": {
            "type": "string",
            "description": "Optional WorkPacket ID guard. Must match the current generated ticket authority if supplied.",
        },
        "work_packet_sha256": {
            "type": "string",
            "description": "Optional WorkPacket SHA256 guard. Must match the current generated ticket authority if supplied.",
        },
    },
    "required": ["decision", "human_decision_text"],
    "additionalProperties": False,
}


_PREPARE_CURRENT_TICKET_EXECUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "human_request_text": {
            "type": "string",
            "description": "Exact user phrase explicitly asking to prepare/project the current approved governed ticket for execution.",
        },
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must equal the current approved ticket if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must equal <current-ticket-token>_APPROVED_NO_EXECUTION if supplied.",
        },
    },
    "required": ["human_request_text"],
    "additionalProperties": False,
}


_START_CURRENT_TICKET_EXECUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "human_authorization_text": {
            "type": "string",
            "description": "Exact user phrase explicitly authorizing start/dispatch of P18.9.0 execution or the accepted retry-start phrase when retry is pending.",
        },
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must be P18.9.0 if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must be START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION or START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION if supplied.",
        },
    },
    "required": ["human_authorization_text"],
    "additionalProperties": False,
}


_RECOVER_CURRENT_TICKET_EXECUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "human_authorization_text": {
            "type": "string",
            "description": (
                "Exact human phrase authorizing recovery: "
                f"{CURRENT_TICKET_RECOVERY_AUTHORIZATION_TEXT}"
            ),
        },
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must be P18.9.0 if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must be RECOVER_P18_9_0_EXECUTION if supplied.",
        },
    },
    "required": ["human_authorization_text"],
    "additionalProperties": False,
}


_PREPARE_CURRENT_TICKET_REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "human_request_text": {
            "type": "string",
            "description": "Exact user phrase explicitly asking to prepare P18.9.0 review validation.",
        },
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must be P18.9.0 if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must be PREPARE_P18_9_0_REVIEW if supplied.",
        },
    },
    "required": ["human_request_text"],
    "additionalProperties": False,
}


_ACCEPT_CURRENT_TICKET_REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "human_acceptance_text": {
            "type": "string",
            "description": (
                "Exact human phrase accepting the prepared P18.9.0 review: "
                f"{CURRENT_TICKET_REVIEW_ACCEPTANCE_TEXT}"
            ),
        },
        "project_id": {
            "type": "string",
            "description": "Optional governed project guard. Must be PEPPER if supplied.",
        },
        "ticket_id": {
            "type": "string",
            "description": "Optional governed ticket guard. Must be P18.9.0 if supplied.",
        },
        "next_action_id": {
            "type": "string",
            "description": "Optional next-action guard. Must be AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE if supplied.",
        },
    },
    "required": ["human_acceptance_text"],
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
    name="decide_pending_approval",
    toolset=TOOLSET,
    schema={
        "name": "decide_pending_approval",
        "description": (
            "Apply the explicit human approve/reject decision for only the current "
            "Pepper P18.9.0 pending ticket approval through the canonical approval backend. "
            "No execution, Kanban dispatch, WorkPacket recompilation, or Git mutation."
        ),
        "parameters": _DECIDE_PENDING_APPROVAL_SCHEMA,
    },
    handler=_decide_pending_approval,
    emoji="D",
    max_result_size_chars=24000,
)

registry.register(
    name="prepare_current_ticket_execution",
    toolset=TOOLSET,
    schema={
        "name": "prepare_current_ticket_execution",
        "description": (
            "Project only the current approved governed WorkPacket to a Hermes Kanban "
            "task for future execution preparation. Does not dispatch, execute, create a "
            "workspace, mutate Git, invoke Docker, or invoke Graphify."
        ),
        "parameters": _PREPARE_CURRENT_TICKET_EXECUTION_SCHEMA,
    },
    handler=_prepare_current_ticket_execution,
    emoji="Q",
    max_result_size_chars=24000,
)

registry.register(
    name="start_current_ticket_execution",
    toolset=TOOLSET,
    schema={
        "name": "start_current_ticket_execution",
        "description": (
            "Apply a separate explicit human authorization to start only the current "
            "Pepper P18.9.0 Kanban worker or retry run 2 when retry is pending. Validates provider, profile, workspace, "
            "dependency, and concurrency gates before dispatch; no Git, Docker, "
            "Graphify, automatic retry, or rollback."
        ),
        "parameters": _START_CURRENT_TICKET_EXECUTION_SCHEMA,
    },
    handler=_start_current_ticket_execution,
    emoji="S",
    max_result_size_chars=24000,
)

registry.register(
    name="recover_current_ticket_execution",
    toolset=TOOLSET,
    schema={
        "name": "recover_current_ticket_execution",
        "description": (
            "Record the exact explicit human recovery authorization for failed Pepper "
            "P18.9.0 and prepare retry-pending governance. Does not start run 2, "
            "requeue or reclaim Kanban, create a new task, mutate Git, invoke Docker, "
            "or invoke Graphify."
        ),
        "parameters": _RECOVER_CURRENT_TICKET_EXECUTION_SCHEMA,
    },
    handler=_recover_current_ticket_execution,
    emoji="V",
    max_result_size_chars=24000,
)

registry.register(
    name="prepare_current_ticket_review",
    toolset=TOOLSET,
    schema={
        "name": "prepare_current_ticket_review",
        "description": (
            "Prepare the completed current Pepper P18.9.0 run for governed review "
            "validation by binding completion evidence to the ticket acceptance contract. "
            "Does not accept, close, rerun, retry, mutate Git, invoke Docker, or invoke Graphify."
        ),
        "parameters": _PREPARE_CURRENT_TICKET_REVIEW_SCHEMA,
    },
    handler=_prepare_current_ticket_review,
    emoji="P",
    max_result_size_chars=24000,
)

registry.register(
    name="accept_current_ticket_review",
    toolset=TOOLSET,
    schema={
        "name": "accept_current_ticket_review",
        "description": (
            "Record exact explicit human acceptance for the prepared current Pepper P18.9.0 "
            "review package and close P18.9.0. Does not generate P18.9.1, execute, rerun, "
            "retry, mutate Git, invoke Docker, or invoke Graphify."
        ),
        "parameters": _ACCEPT_CURRENT_TICKET_REVIEW_SCHEMA,
    },
    handler=_accept_current_ticket_review,
    emoji="A",
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


registry.register(
    name="reconcile_invalid_current_generation_authority",
    toolset=TOOLSET,
    schema={
        "name": "reconcile_invalid_current_generation_authority",
        "description": (
            "Quarantine invalid unaccepted future-ticket generation authority for only the "
            "current canonical next ticket. Does not generate, approve, project, execute, "
            "dispatch workers, mutate Git, invoke Docker, or invoke Graphify."
        ),
        "parameters": _RECONCILE_INVALID_CURRENT_GENERATION_AUTHORITY_SCHEMA,
    },
    handler=_reconcile_invalid_current_generation_authority,
    emoji="X",
    max_result_size_chars=24000,
)


registry.register(
    name="generate_current_ticket",
    toolset=TOOLSET,
    schema={
        "name": "generate_current_ticket",
        "description": (
            "Generate only Pepper's canonical current next governed ticket when the active "
            "next action is a ticket-generation action. Stops at awaiting_ticket_approval; "
            "no approval, execution, worker dispatch, Docker, Graphify, or Git."
        ),
        "parameters": _GENERATE_CURRENT_TICKET_SCHEMA,
    },
    handler=_generate_current_ticket,
    emoji="G",
    max_result_size_chars=24000,
)
