"""Human request for a proven immutable command-reference defect before review."""

import json
import shlex
from pathlib import Path

from hermes_constants import get_hermes_home
from . import command_validation as cv
from .post_accept_material_revision import serialized, revision_action

POLICY = "pepper-post-execution-material-revision-v1"
REASON = "post_execution_validation_contract_reference_defect"
CATEGORY = "immutable_validation_command_reference_defect"
MAX_BYTES = 4 * 1024 * 1024


def digest(record):
    return cv.digest({"policy_id": POLICY, "record": {
        k: v for k, v in record.items() if k != "material_revision_request_SHA256"
    }})


def action_id(ticket):
    from .product_runtime import governed_ticket_lifecycle_action_token
    return f"REQUEST_{governed_ticket_lifecycle_action_token(ticket)}_POST_EXECUTION_MATERIAL_REVISION"


def consent(binding):
    return f"{action_id(binding['ticket_id'])} BINDING {cv.digest(binding)}"


def path_for(generation):
    from .workflow.ticket_architect_bridge import _safe_ticket_id, _safe_digest
    return get_hermes_home() / "agent-platform/post-execution-material-revision" / (
        f"{_safe_ticket_id(generation['ticket_id'])}.{_safe_digest(generation['work_packet_SHA256'])}.json"
    )


def validate_record(record, generation, _depth=0):
    binding = record["request_binding"]
    if record.get("material_revision_request_SHA256") != digest(record):
        raise ValueError("post-execution material request digest mismatch")
    if "reconciliation_authority" in record:
        from . import material_revision_reconciliation as reconciliation
        authority = reconciliation.validate(record["reconciliation_authority"], generation, _depth)
        if record != reconciliation.effective(authority):
            raise ValueError("reconciled material request mismatch")
        return record
    expected = {"policy_id": POLICY, "reason_code": REASON,
                "human_authorization_text": consent(binding),
                "successor_generated": False, "execution_started": False,
                "Git_mutation": False, "material_revision_required": True}
    expected.update({k: generation[k] for k in (
        "ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256")})
    if any(record.get(k) != v for k, v in expected.items()):
        raise ValueError("post-execution material request authority mismatch")
    if any(binding.get(k) != record.get(k) for k in (
        "ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256")):
        raise ValueError("post-execution request binding mismatch")
    if (binding.get("defect_category") != CATEGORY or not binding.get("defects")
            or binding.get("requested_material_fields") != ["validation_steps"]):
        raise ValueError("qualified validation reference defect required")
    return record


def load(generation):
    path = path_for(generation)
    if not path.exists():
        return None
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("material request exceeds bound")
    original = validate_record(json.loads(raw), generation)
    if "reconciliation_authority" in original:
        raise ValueError("original request cannot be replaced by reconciled authority")
    from .material_revision_reconciliation import resolve
    return resolve(generation, original)


def context(projection):
    from . import product_runtime as pr
    from .workflow import ticket_architect_bridge as bridge
    from .execution_evidence import connection
    from hermes_cli import kanban_db as kb
    from tools.pre_review_validation_commands import PRODUCT, contained_file

    contract = pr._acceptance_contract_for_review_projection(projection)
    if not any(step.get("required") and str(step.get("command") or "").startswith("scripts/run_tests.sh ")
               for step in contract.get("work_packet_validation_steps", [])):
        raise ValueError("no qualified repository test-reference contract")
    command = cv.inspect()
    binding = command["binding"]
    if any(binding.get(k) != projection.get(k) for k in (
        "ticket_id", "work_packet_SHA256", "projection_SHA256", "kanban_task_id")):
        raise ValueError("post-execution request current projection mismatch")
    for fn in (pr.review_prepare_record_path_for_ticket, pr.review_decision_record_path_for_ticket,
               pr.human_git_handoff_completion_record_path_for_ticket):
        if fn(binding["ticket_id"]).exists():
            raise ValueError("post-execution request is available only before review")
    conn = connection(kb.kanban_db_path(board=projection["kanban_board_slug"]))
    try:
        task = kb.get_task(conn, projection["kanban_task_id"])
        if (task is None or task.current_run_id is not None or task.claim_lock
                or (task.worker_pid and kb._pid_alive(task.worker_pid))
                or conn.execute("SELECT 1 FROM tasks WHERE current_run_id IS NOT NULL LIMIT 1").fetchone()
                or conn.execute("SELECT 1 FROM task_runs WHERE ended_at IS NULL LIMIT 1").fetchone()):
            raise ValueError("inactive terminal execution required")
    finally:
        conn.close()
    defects = []
    for spec in command["command_capability"]["commands"]:
        plan = spec.get("execution_plan") or []
        if (spec.get("runtime_available") is not False or not plan
                or not plan[0].get("repository_test_wrapper")
                or not str(spec.get("runtime_unavailable_reason") or "").startswith("required test paths unavailable: ")):
            continue
        product = Path(plan[0]["working_directory"])
        root = product.parent.parent
        missing = [p for p in shlex.split(spec["source_command"])[1:]
                   if contained_file(root, f"{PRODUCT}/{p}") is None]
        if missing:
            defects.append({"validation_id": spec["validation_id"],
                            "defect_locus": f"validation_steps.{spec['validation_id']}.command",
                            "source_command": spec["source_command"],
                            "command_authority_SHA256": spec["command_authority_SHA256"],
                            "execution_plan_SHA256": spec["execution_plan_SHA256"],
                            "missing_paths": missing})
    if not defects:
        raise ValueError("no qualified immutable validation command reference defect")
    generation = bridge.load_generation_record(ticket_id=binding["ticket_id"])
    current = {**binding, "defect_category": CATEGORY, "defects": defects,
               "requested_material_fields": ["validation_steps"]}
    completion = pr._current_review_round_completion_source_raw(projection)
    history = {"projection": projection, "completion": completion,
               "zero_change_authority": pr.resolve_zero_change_authority(projection, completion),
               "validation_contract": pr._acceptance_contract_for_review_projection(projection)}
    return generation, current, history


def validate_current(record, projection):
    generation, binding, history = context(projection)
    validate_record(record, generation)
    if (record["request_binding"] != binding or record["historical_authority"] != history
            or load(generation) != record):
        raise ValueError("post-execution material request current authority changed")
    if "reconciliation_authority" in record:
        from .material_revision_reconciliation import context as reconciliation_context
        reconciliation_context(projection)
    return record


def request_action(binding):
    return {"id": action_id(binding["ticket_id"]), "target_ticket_id": binding["ticket_id"],
            "required_human_action": "post_execution_material_revision_request",
            "tool": "request_current_ticket_material_revision", "origin": "post_execution",
            "request_binding": binding, "human_authorization_text": consent(binding),
            "label": "Request material revision for the proven command-reference defect; generation requires separate REVISE consent."}


def inspect():
    from . import product_runtime as pr
    projection = pr._load_current_projection_record()
    try:
        generation, binding, _ = context(projection)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        return {"read_only": True, "requestable": False, "blocker": str(exc)[:300],
                "ticket_id": projection["ticket_id"], "successor_generated": False}
    record = load(generation)
    if record is not None:
        validate_current(record, projection)
    return {"read_only": True, "requestable": record is None, "request_binding": binding,
            "material_revision_request_SHA256": record["material_revision_request_SHA256"] if record else None,
            "next_action": revision_action(binding["ticket_id"]) if record else request_action(binding),
            "successor_generated": False}


def public(record):
    """Keep full historical evidence durable; expose bounded request authority."""
    return {k: record[k] for k in (
        "success", "idempotent_replay", "policy_id", "request_binding",
        "material_revision_request_SHA256", "next_action", "successor_generated",
        "execution_started", "Git_mutation",
    )}


@serialized
def request(*, binding, human_authorization_text, next_action_id, authorizer_id="pepper-chat-human"):
    from . import product_runtime as pr
    from .workflow import ticket_architect_bridge as bridge
    from .zero_change_decision import persist
    with bridge._STORE_LOCK:
        projection = pr._load_current_projection_record()
        generation, current, history = context(projection)
        if (binding != current or human_authorization_text != consent(current)
                or next_action_id != action_id(current["ticket_id"])):
            raise ValueError("exact current binding and explicit human request required")
        authorizer_id = bridge._reviewer_id_from_actor(authorizer_id)
        existing = load(generation)
        if existing is not None:
            validate_current(existing, projection)
            if existing["authorizer_id"] != authorizer_id:
                raise ValueError("conflicting material request authorizer")
            return {**existing, "success": True, "idempotent_replay": True}
        workflow = pr.build_workflow_control_snapshot()
        if (workflow.get("workflow_status") not in {"execution_completed", "execution_completed_pending_manual_validation"}
                or workflow.get("remaining_blockers") or workflow.get("active_execution_count") != 0
                or workflow.get("pending_ticket_approval_count") != 0
                or workflow.get("recovery_state") != "not_required"):
            raise ValueError("post-execution material request is not the current boundary")
        record = {"policy_id": POLICY, "reason_code": REASON, **current,
                  "request_binding": current, "historical_authority": history,
                  "human_authorization_text": human_authorization_text, "authorizer_id": authorizer_id,
                  "created_at": pr._utc_now_iso(), "material_revision_required": True,
                  "successor_generated": False, "execution_started": False, "Git_mutation": False,
                  "next_action": revision_action(current["ticket_id"])}
        record["material_revision_request_SHA256"] = digest(record)
        if len(json.dumps(record).encode()) > MAX_BYTES:
            raise ValueError("material request exceeds bound")
        if pr._load_current_projection_record() != projection or context(projection) != (generation, current, history):
            raise ValueError("material request authority changed before persistence")
        persist(path_for(generation), record)
        return {**record, "success": True, "idempotent_replay": False}


def apply_workflow(snapshot, blockers):
    from . import product_runtime as pr
    exists = False
    try:
        if snapshot.get("workflow_status") not in {"execution_completed", "execution_completed_pending_manual_validation"}:
            return
        projection = pr._load_current_projection_record()
        exists = path_for(projection).exists()
        generation, binding, _ = context(projection)
        record = load(generation)
        if record is None:
            snapshot.setdefault("alternative_actions", []).append(request_action(binding))
            return
        validate_current(record, projection)
        snapshot.update(workflow_status="awaiting_material_revision",
                        workflow_state=f"{generation['ticket_id']}-AWAITING-MATERIAL-REVISION",
                        governed_workflow_state="awaiting_material_revision", review_state="material_revision_required",
                        material_revision_required=True, material_revision_request_authority=record,
                        next_action=revision_action(generation["ticket_id"]), alternative_actions=[],
                        validation_contract_satisfied=False, reviewable_result=False,
                        command_validation_available=False,
                        required_human_action="ticket_material_revision",
                        ticket_execution_authorized=False, WorkPacket_execution_authorized=False,
                        runtime_execution_authorized=False)
        snapshot.pop("command_validation_action", None)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        if exists:
            from .material_revision_reconciliation import inspect as inspect_reconciliation
            reconciliation = inspect_reconciliation(projection)
            snapshot.update(workflow_status="material_revision_authority_blocked", alternative_actions=[],
                            required_human_action="authority_reconciliation",
                            material_revision_reconciliation=reconciliation,
                            command_validation_available=False, reviewable_result=False,
                            ticket_execution_authorized=False, WorkPacket_execution_authorized=False,
                            runtime_execution_authorized=False,
                            next_action=reconciliation.get("next_action", {
                                "id": "RECONCILE_MATERIAL_REVISION_AUTHORITY",
                                "required_human_action": "authority_reconciliation"}))
            snapshot.pop("command_validation_action", None)
            blockers.append({"id": "POST-EXECUTION-MATERIAL-REVISION-AUTHORITY", "status": "blocked", "evidence": str(exc)[:300]})
