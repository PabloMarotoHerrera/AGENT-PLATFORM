"""Human-requested contract revision from a recovered, unconsumed failed run."""

import hashlib
import json
from pathlib import Path

from hermes_constants import get_hermes_home

POLICY = "pepper-retry-material-revision-request-v1"
REASON = "required_validation_command_authority_missing"


def _eligible(evidence):
    from hermes_cli.agent_platform.validation_contract_failure import (
        REASON as incompatible,
    )

    if not isinstance(evidence, dict):
        return False
    if evidence.get("reason_code") == REASON:
        return isinstance(
            evidence.get("missing_required_validation_steps"), list
        ) and bool(evidence["missing_required_validation_steps"])
    failures = evidence.get("incompatible_validation_commands")
    return (
        evidence.get("reason_code") == incompatible
        and isinstance(failures, list)
        and len(failures) == 1
        and all(
            isinstance(item, dict)
            and item.get("failure_classification") == "unsupported_cli_option"
            and item.get("command_authority_matched") is True
            and item.get("ad_hoc_command_substitution") is False
            and item.get("test_execution_started") is False
            and isinstance(item.get("command"), dict)
            and item["command"].get("command_authority_SHA256")
            and item.get("source_messages")
            and item.get("source_session")
            for item in failures
        )
    )


def digest(record: dict) -> str:
    payload = {
        k: v for k, v in record.items() if k != "material_revision_request_SHA256"
    }
    return hashlib.sha256(
        (
            POLICY
            + ":"
            + json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        ).encode()
    ).hexdigest()


def action_id(ticket_id: str) -> str:
    from hermes_cli.agent_platform.product_runtime import (
        governed_ticket_lifecycle_action_token,
    )

    return (
        f"REQUEST_{governed_ticket_lifecycle_action_token(ticket_id)}_MATERIAL_REVISION"
    )


def path_for(generation: dict) -> Path:
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import (
        _safe_ticket_id,
        _safe_digest,
    )

    ticket = _safe_ticket_id(generation["ticket_id"])
    sha = _safe_digest(generation["work_packet_SHA256"])
    return (
        get_hermes_home()
        / "agent-platform"
        / "pepper-material-revision-request"
        / f"{ticket}.{sha}.json"
    )


def validate_record(record: dict, generation: dict) -> dict:
    if record.get("material_revision_request_SHA256") != digest(record):
        raise ValueError("material revision request digest mismatch")
    expected = {
        "policy_id": POLICY,
        "schema_version": 1,
        "retry_authority_status": "suspended_not_consumed",
        "material_revision_required": True,
        "execution_started": False,
        "retry_budget_consumed": False,
        "retry_started": False,
        "new_run_started": False,
        "Git_mutation": False,
    }
    expected.update({
        k: generation[k]
        for k in (
            "ticket_id",
            "ticket_spec_SHA256",
            "work_packet_id",
            "work_packet_SHA256",
        )
    })
    for key, value in expected.items():
        if record.get(key) != value:
            raise ValueError(f"material revision request {key} mismatch")
    if record.get("human_authorization_text") != action_id(generation["ticket_id"]):
        raise ValueError("explicit material revision request authorization mismatch")
    if (
        not record.get("material_failure_evidence")
        or not record.get("recovery_action_SHA256")
        or not record.get("failed_run_id")
    ):
        raise ValueError("material revision request source evidence absent")
    from hermes_cli.agent_platform.workflow.ticket_architect_bridge import _safe_digest

    for field in ("projection_SHA256", "recovery_action_SHA256", "failed_run_SHA256"):
        _safe_digest(record.get(field))
    evidence = record["material_failure_evidence"]
    if (
        not isinstance(evidence, dict)
        or evidence.get("reason_code") != record.get("reason_code")
        or not _eligible(evidence)
        or type(record["failed_run_id"]) is not int
        or record["failed_run_id"] < 1
    ):
        raise ValueError("material revision request bounded evidence invalid")
    return record


def load(generation: dict) -> dict | None:
    path = path_for(generation)
    if not path.exists():
        return None
    return validate_record(json.loads(path.read_text(encoding="utf-8")), generation)


def context(projection: dict) -> tuple[dict, dict, dict]:
    """Read canonical approval, terminal run, recovery and missing command authority."""
    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    from hermes_cli.agent_platform.work_packet import WorkPacketCompilationResult
    from tools import governed_workpacket_file_guard as guard
    from tools import workpacket_validation_tool as validation

    authority = bridge.load_immutable_approved_current_ticket_authority(
        ticket_id=projection["ticket_id"], require_approved_decision=True
    )
    if authority is None:
        raise ValueError("current approved material revision source unavailable")
    generation = authority["generation_record"]
    for key in (
        "ticket_id",
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
    ):
        if projection.get(key) != generation[key]:
            raise ValueError(f"material revision projection {key} mismatch")
    recovery = pr.load_current_ticket_recovery_action_record(
        projection_record=projection
    )
    if (
        recovery is None
        or recovery.get("recovery_status") != "retry_pending"
        or recovery.get("retry_execution_count") != 0
    ):
        raise ValueError("unconsumed retry-pending recovery authority required")
    conn = kanban_db.connect(board=projection["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projection["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projection["kanban_task_id"])
        if (
            task is None
            or task.status != "blocked"
            or task.current_run_id is not None
            or not runs
        ):
            raise ValueError("terminal blocked material revision source required")
        task_body = json.loads(task.body or "{}")
        if any(
            task_body.get(key) != projection[field]
            for key, field in (
                ("WorkPacket_ID", "work_packet_id"),
                ("WorkPacket_SHA256", "work_packet_SHA256"),
            )
        ):
            raise ValueError("material revision task/WorkPacket binding mismatch")
        if any(pr._execution_is_active(pr._run_dict(item)) for item in runs):
            raise ValueError("material revision source has active runs")
        run = runs[-1]
        if (
            run.ended_at is None
            or (run.outcome or run.status) not in pr._GOVERNED_TICKET_FAILURE_OUTCOMES
        ):
            raise ValueError("terminal failed material revision source required")
        if (
            run.id != recovery["latest_failed_run_id"]
            or len(runs) != recovery["observed_attempt_count"]
        ):
            raise ValueError("material revision failed-run/recovery binding mismatch")
        if getattr(task, "worker_pid", None) and kanban_db._pid_alive(task.worker_pid):
            raise ValueError("material revision source worker is still active")
        workspace = Path(task.workspace_path or "")
        if not workspace.is_absolute() or not workspace.is_dir():
            raise ValueError("material revision candidate workspace unavailable")
        if str(workspace) != recovery.get("kanban_task_workspace_path"):
            raise ValueError("material revision candidate/recovery binding mismatch")
        run_digest = hashlib.sha256(
            json.dumps(pr._run_dict(run), sort_keys=True, default=str).encode()
        ).hexdigest()
    finally:
        conn.close()
    work_packet = WorkPacketCompilationResult.model_validate(
        generation["work_packet_compilation_result"]
    ).work_packet
    scope = work_packet.repository_scope
    file_authority = guard.WorkPacketFileAuthority(
        ticket_id=generation["ticket_id"],
        ticket_spec_SHA256=generation["ticket_spec_SHA256"],
        work_packet_id=generation["work_packet_id"],
        work_packet_SHA256=generation["work_packet_SHA256"],
        projection_SHA256=projection["projection_SHA256"],
        allowed_paths=tuple(scope.allowed_paths),
        forbidden_paths=tuple(scope.forbidden_paths),
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(),
    )
    specs = validation.build_governed_validation_command_specs(
        file_authority, work_packet
    )
    missing = [
        step.model_dump(mode="json")
        for step in work_packet.validation_steps
        if step.required
        and step.command
        and step.command_authority is None
        and not step.command_execution_authorized
        and not any(
            spec.validation_id == step.validation_id
            and spec.source_command == step.command
            for spec in specs
        )
    ]
    evidence = {"reason_code": REASON, "missing_required_validation_steps": missing}
    if not missing:
        from hermes_cli.agent_platform.validation_contract_failure import (
            evidence as command_evidence,
        )

        evidence = (
            command_evidence(projection, run, workspace, work_packet, specs) or evidence
        )
    binding = {
        "project_id": generation["project_id"],
        "macroproject_id": generation["macroproject_id"],
        **{
            k: generation[k]
            for k in (
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
            )
        },
        "projection_SHA256": projection["projection_SHA256"],
        "recovery_action_SHA256": recovery["recovery_action_SHA256"],
        "failed_run_id": run.id,
        "failed_run_SHA256": run_digest,
        "kanban_task_id": task.id,
        "workspace_path": str(workspace),
        "observed_attempt_count": len(runs),
        "max_attempts": recovery["max_attempts"],
        "material_failure_evidence": evidence,
        "reason_code": evidence["reason_code"],
    }
    return generation, recovery, binding


def validate_current(record: dict, projection: dict) -> dict:
    generation, _recovery, binding = context(projection)
    validate_record(record, generation)
    if load(generation) != record:
        raise ValueError("material revision request is not persisted current authority")
    for key, value in binding.items():
        if record.get(key) != value:
            raise ValueError(f"material revision request {key} source changed")
    if not _eligible(binding["material_failure_evidence"]):
        raise ValueError("material contract failure evidence absent")
    return record


def request(
    *,
    human_authorization_text: str,
    ticket_id: str,
    failed_run_id: int,
    work_packet_SHA256: str,
    recovery_action_SHA256: str,
    reason_code: str,
    authorizer_id: str = "pepper-chat-human",
) -> dict:
    from hermes_cli.agent_platform import product_runtime as pr
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

    if type(failed_run_id) is not int or failed_run_id < 1:
        raise pr.ProductRuntimeConflict(
            "material revision requires an integer failed run ID"
        )
    if human_authorization_text.strip() != action_id(ticket_id):
        raise pr.ProductRuntimeDecisionFailed(
            "exact explicit material revision request authorization required"
        )
    request_model = pr.CurrentTicketExecutionRecoveryRequest(
        human_authorization_text=human_authorization_text,
        authorizer_id=authorizer_id,
        ticket_id=ticket_id,
    )
    # Snapshot reconciliation may itself use the store lock. Revalidate the
    # canonical projection/run/recovery binding below while holding it.
    workflow = pr.build_workflow_control_snapshot()
    with bridge._STORE_LOCK:
        if (
            workflow.get("current_ticket_id") != ticket_id
            or workflow.get("workflow_status")
            not in {"retry_pending", "awaiting_material_revision"}
            or workflow.get("active_execution_count")
        ):
            raise pr.ProductRuntimeConflict(
                "current inactive retry-pending ticket required"
            )
        projection = pr._load_current_projection_record()
        generation, _recovery, binding = context(projection)
        for key, expected in (
            ("ticket_id", ticket_id),
            ("failed_run_id", failed_run_id),
            ("work_packet_SHA256", work_packet_SHA256),
            ("recovery_action_SHA256", recovery_action_SHA256),
        ):
            if binding[key] != expected:
                raise pr.ProductRuntimeConflict(
                    f"material revision request {key} mismatch"
                )
        if reason_code != binding["reason_code"] or not _eligible(
            binding["material_failure_evidence"]
        ):
            raise pr.ProductRuntimeConflict(
                "bounded material contract failure evidence required"
            )
        existing = load(generation)
        if existing is not None:
            validate_current(existing, projection)
            return {**existing, "idempotent_replay": True}
        if workflow.get("workflow_status") != "retry_pending":
            raise pr.ProductRuntimeConflict(
                "material revision request requires retry_pending"
            )
        record = {
            "schema_version": 1,
            "policy_id": POLICY,
            **binding,
            "reason_code": reason_code,
            "human_authorization_text": request_model.human_authorization_text,
            "authorizer_id": request_model.authorizer_id,
            "created_at": pr._utc_now_iso(),
            "material_revision_required": True,
            "retry_authority_status": "suspended_not_consumed",
            "execution_started": False,
            "retry_started": False,
            "new_run_started": False,
            "retry_budget_consumed": False,
            "Git_mutation": False,
        }
        record["material_revision_request_SHA256"] = digest(record)
        bridge._write_json_atomic(path_for(generation), record)
        return {**record, "idempotent_replay": False}


def apply_workflow(snapshot: dict, blockers: list) -> None:
    """Expose an alternative choice, or the gate selected by durable human consent."""
    if snapshot.get("workflow_status") != "retry_pending":
        return
    from hermes_cli.agent_platform import product_runtime as pr

    request_exists = False
    try:
        projection = pr._load_current_projection_record()
        request_exists = path_for(projection).exists()
        generation, _recovery, binding = context(projection)
        if snapshot.get("current_ticket_id") != generation["ticket_id"]:
            raise ValueError("material revision current ticket mismatch")
        record = load(generation)
        if record is None:
            if _eligible(binding["material_failure_evidence"]):
                snapshot["alternative_actions"] = [
                    {
                        "id": action_id(generation["ticket_id"]),
                        "target_ticket_id": generation["ticket_id"],
                        "required_human_action": "material_revision_request",
                        "label": "Request the material-revision gate; changes workflow authority but does not revise or start execution. A separate REVISE decision is required.",
                        "human_authorization_text": action_id(generation["ticket_id"]),
                        "request_binding": binding,
                        "reason_code": binding["reason_code"],
                    }
                ]
            return
        validate_current(record, projection)
        snapshot.update({
            "workflow_status": "awaiting_material_revision",
            "governed_workflow_state": "awaiting_material_revision",
            "review_state": "material_revision_required",
            "readiness": "material_revision_required",
            "validation_state": "material_contract_failure",
            "retry_started": False,
            "new_run_started": False,
            "retry_budget_consumed": False,
            "workflow_state": f"{generation['ticket_id']}-AWAITING-MATERIAL-REVISION",
            "material_revision_required": True,
            "material_revision_request_authority": record,
            "retry_state": "suspended_not_consumed",
            "recovery_state": "suspended_for_material_revision",
            "queue_state": "material_revision_required_not_queued",
            "ticket_execution_authorized": False,
            "WorkPacket_execution_authorized": False,
            "runtime_execution_authorized": False,
            "alternative_actions": [],
            "next_action": {
                "id": pr.governed_ticket_lifecycle_action_ids(generation["ticket_id"])[
                    "revise"
                ],
                "target_ticket_id": generation["ticket_id"],
                "required_human_action": "ticket_material_revision",
                "label": "Explicitly revise the current contract; the new publication will require human approval.",
            },
        })
    except Exception as exc:
        if not request_exists:
            return
        # A corrupt request must never restore executable retry authority.
        snapshot.update({
            "workflow_status": "material_revision_authority_blocked",
            "ticket_execution_authorized": False,
            "WorkPacket_execution_authorized": False,
            "runtime_execution_authorized": False,
            "alternative_actions": [],
        })
        snapshot["next_action"] = {
            "id": "RECONCILE_MATERIAL_REVISION_AUTHORITY",
            "required_human_action": "authority_reconciliation",
        }
        blockers.append({
            "id": "MATERIAL-REVISION-REQUEST-AUTHORITY",
            "status": "blocked",
            "evidence": str(exc)[:300],
        })
