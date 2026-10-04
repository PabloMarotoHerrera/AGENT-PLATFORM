"""Explicit zero-change refusal and independently authorized corrective execution."""

import json
import os
from contextlib import contextmanager
from threading import RLock

from hermes_cli.agent_platform import execution_evidence as ev
from hermes_cli.agent_platform import product_runtime as pr

_LOCK = RLock()
STATE = "zero_change_rejected_correction_required"
PROVENANCE = "human_zero_change_rejection_correction"
KEYS = (
    "project_id",
    "macroproject_id",
    "ticket_id",
    "ticket_spec_SHA256",
    "work_packet_id",
    "work_packet_SHA256",
    "projection_SHA256",
)


def action(ticket, run_id, *, corrective=False):
    token = ticket.replace(".", "_").replace("-", "_")
    verb = "START" if corrective else "REJECT"
    tail = "ZERO_CHANGE_CORRECTIVE_EXECUTION" if corrective else "ZERO_CHANGE"
    return f"{verb}_{token}_{tail}_RUN_{run_id}"


def path_for(p, run_id, kind="decision"):
    return (
        pr.zero_change_attestation_record_path_for_ticket(p["ticket_id"]).parent
        / "zero-change-decisions"
        / p["projection_SHA256"]
        / f"r{int(run_id)}-{kind}.json"
    )


def persist(path, record):
    ev.safe_path(path, ev.kb.kanban_home(), missing=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True))


def read(path):
    if not path.exists():
        return None
    record = ev.read_json(path, ev.kb.kanban_home())
    if record.get("decision_SHA256") != ev.digest({
        k: v for k, v in record.items() if k != "decision_SHA256"
    }):
        raise pr.ProductRuntimeConflict("zero-change decision digest mismatch")
    return record


def context(p, run_id):
    pr._validate_execution_start_authority(p)
    task, run, workspace = ev.run_context(p, run_id)
    conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        runs = ev.kb.list_runs(conn, p["kanban_task_id"])
        if max(item.id for item in runs) != run_id:
            raise pr.ProductRuntimeConflict("ambiguous current terminal run order")
        if any(pr._execution_is_active(pr._run_dict(item)) for item in runs):
            raise pr.ProductRuntimeConflict(
                "active execution conflicts with terminal zero-change decision"
            )
    finally:
        conn.close()
    if (
        task.status != "done"
        or run.status != "done"
        or run.outcome != "completed"
        or task.current_run_id
        or task.claim_lock
        or task.worker_pid
    ):
        raise pr.ProductRuntimeConflict(
            "zero-change decision requires an unowned completed current run"
        )
    source_path = pr.governed_source_authority_record_path_for_run(p, run.id)
    # Legacy missing source authority is explicit unavailability, not refusal-ineligibility.
    source = None
    if source_path.exists():
        source = ev.read_json(
            source_path, ev.kb.kanban_home() / "agent-platform/source-authority"
        )
        expected = {
            k: p[k]
            for k in (
                "project_id",
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
                "projection_SHA256",
                "kanban_task_id",
                "kanban_board_slug",
            )
        }
        expected.update(
            run_id=run.id,
            authority_path=str(source_path),
            policy_id=pr.PEPPER_GOVERNED_SOURCE_AUTHORITY_POLICY_ID,
        )
        if any(source.get(k) != v for k, v in expected.items()) or source.get(
            "governed_source_authority_SHA256"
        ) != pr._governed_source_authority_record_digest(source):
            raise pr.ProductRuntimeConflict(
                "zero-change source authority identity mismatch"
            )
        # Refusal binds the immutable source identity, not availability/equality of its files.
        # Candidate inspection and future dispatch retain their full snapshot validation.

    return task, run, workspace, source


def source_identity(source):
    return (
        pr._governed_source_authority_reference(source)
        if source is not None
        else {"available": False, "reason": "durable source authority absent"}
    )


def load(p, run_id, *, validate=True):
    record = read(path_for(p, run_id))
    if record is None:
        return None
    if (
        any(record.get(k) != p.get(k) for k in KEYS)
        or record.get("task_id") != p["kanban_task_id"]
        or record.get("run_id") != run_id
        or record.get("human_decision") != "zero_change_rejected"
    ):
        raise pr.ProductRuntimeConflict("zero-change decision identity mismatch")
    if record.get("human_authorization_text") != action(p["ticket_id"], run_id):
        raise pr.ProductRuntimeConflict("zero-change decision authorization mismatch")
    if validate:
        _, run, _, source = context(p, run_id)
        if record["terminal_run_SHA256"] != ev.digest(pr._run_dict(run)) or record[
            "source_authority_identity"
        ] != source_identity(source):
            raise pr.ProductRuntimeConflict(
                "zero-change decision terminal/source mismatch"
            )
    return record


def current(p):
    if not any(path_for(p, 1).parent.glob("r*-decision.json")):
        return None
    conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        runs = ev.kb.list_runs(conn, p["kanban_task_id"])
    finally:
        conn.close()
    return load(p, runs[-1].id) if runs and path_for(p, runs[-1].id).exists() else None


def require_not_rejected(p):
    if current(p) is not None:
        raise pr.ProductRuntimeConflict(
            "zero-change was rejected; positive attestation/review is mutually exclusive"
        )


def next_action(record):
    return {
        "id": action(record["ticket_id"], record["run_id"], corrective=True),
        "target_ticket_id": record["ticket_id"],
        "required_human_action": "fresh_corrective_execution_authorization",
        "required_human_authorization_text": action(
            record["ticket_id"], record["run_id"], corrective=True
        ),
        "rejected_run_id": record["run_id"],
        "zero_change_decision_SHA256": record["decision_SHA256"],
        "label": "Separately authorize fresh implementation of the same approved WorkPacket from current source.",
    }


def operational(record, replay=False):
    return {
        **record,
        "idempotent_replay": replay,
        "workflow_status": STATE,
        "next_action": next_action(record),
        "execution_started": False,
        "dispatch_performed": False,
        "retry_budget_consumed": False,
        "Git_mutation": False,
        "human_attestation_performed": False,
    }


def _request(
    *,
    human_authorization_text,
    ticket_id,
    run_id,
    project_id,
    ticket_spec_SHA256,
    work_packet_SHA256,
    projection_SHA256,
    reviewer_id="pepper-chat-human",
):
    with _LOCK:
        p = pr._load_current_projection_record()
        guards = dict(
            ticket_id=ticket_id,
            project_id=project_id,
            ticket_spec_SHA256=ticket_spec_SHA256,
            work_packet_SHA256=work_packet_SHA256,
            projection_SHA256=projection_SHA256,
        )
        if any(p.get(k) != v for k, v in guards.items()) or type(run_id) is not int:
            raise pr.ProductRuntimeConflict(
                "zero-change rejection current authority mismatch"
            )
        if human_authorization_text != action(ticket_id, run_id):
            raise pr.ProductRuntimeConflict(
                "exact explicit human zero-change rejection authorization required"
            )
        _, run, _, source = context(p, run_id)
        existing = load(p, run_id)
        if existing:
            if existing["reviewer_id"] != reviewer_id:
                raise pr.ProductRuntimeConflict(
                    "conflicting zero-change decision replay"
                )
            return operational(existing, True)
        completion = pr._current_review_round_completion_source(p)
        if pr.load_current_ticket_zero_change_attestation_record(
            projection_record=p, completion=completion, allow_historical_mismatch=True
        ):
            raise pr.ProductRuntimeConflict(
                "positive zero-change attestation already finalized"
            )
        workflow = pr.build_workflow_control_snapshot()
        if (
            workflow.get("workflow_status")
            != "execution_completed_pending_zero_change_attestation"
            or workflow.get("current_ticket_id") != ticket_id
            or workflow.get("active_execution_count")
            or workflow.get("remaining_blockers")
        ):
            raise pr.ProductRuntimeConflict(
                "current workflow is not eligible for zero-change rejection"
            )
        record = {
            **{k: p[k] for k in KEYS},
            "task_id": p["kanban_task_id"],
            "run_id": run_id,
            "terminal_run_SHA256": ev.digest(pr._run_dict(run)),
            "source_authority_identity": source_identity(source),
            "human_decision": "zero_change_rejected",
            "human_authorization_text": human_authorization_text,
            "reviewer_id": reviewer_id,
            "created_at": pr._utc_now_iso(),
            "policy_id": "pepper-zero-change-rejection-v1",
        }
        record["decision_SHA256"] = ev.digest(record)
        persist(path_for(p, run_id), record)
        return operational(record)


def apply_workflow(snapshot, blockers):
    if snapshot.get("workflow_status") not in {
        "execution_completed",
        "execution_completed_pending_zero_change_attestation",
        STATE,
    }:
        return
    try:
        p = pr._load_current_projection_record()
        if snapshot.get("current_ticket_id") != p["ticket_id"]:
            return
        record = current(p)
        if record:
            snapshot.update(
                workflow_state=STATE,
                workflow_status=STATE,
                governed_workflow_state=STATE,
                validation_state=STATE,
                review_state="zero_change_rejected",
                recovery_state="not_required",
                human_zero_change_attestation_required=False,
                review_prepare_eligible_result=False,
                zero_change_result=False,
                execution_started=False,
                next_action=next_action(record),
                alternative_actions=[],
                zero_change_decision_SHA256=record["decision_SHA256"],
            )
        elif (
            snapshot.get("workflow_status")
            == "execution_completed_pending_zero_change_attestation"
        ):
            if not ev.kb.kanban_db_path(board=p["kanban_board_slug"]).exists():
                return
            conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
            try:
                run = ev.kb.list_runs(conn, p["kanban_task_id"])[-1]
            finally:
                conn.close()
            snapshot["alternative_actions"] = [
                {
                    "id": action(p["ticket_id"], run.id),
                    "target_ticket_id": p["ticket_id"],
                    "required_human_action": "human_zero_change_rejection",
                    "required_human_authorization_text": action(p["ticket_id"], run.id),
                    "run_id": run.id,
                    **{k: p[k] for k in KEYS},
                    "label": "Decline unsupported zero-change attestation without starting execution.",
                }
            ]
    except Exception as exc:
        blockers.append({
            "id": "ZERO-CHANGE-DECISION-AUTHORITY",
            "status": "blocked_by_invalid_zero_change_decision",
            "evidence": str(exc)[:300],
        })


def corrective_blocker(p, fresh):
    try:
        run_id = fresh["prior_terminal_run_id"]
        record = load(p, run_id)
        authorization = read(path_for(p, run_id, "start"))
        if (
            record is None
            or authorization is None
            or fresh != authorization["fresh_execution_request"]
        ):
            raise ValueError(
                "missing or mismatched separately authorized corrective request"
            )
        if authorization["rejection_SHA256"] != record["decision_SHA256"]:
            raise ValueError("corrective request rejection mismatch")
        if authorization["human_authorization_text"] != action(
            p["ticket_id"], run_id, corrective=True
        ):
            raise ValueError("corrective authorization mismatch")
        return None
    except Exception as exc:
        return "ZERO_CHANGE_CORRECTIVE_AUTHORITY_INVALID", str(exc)


def _start(
    *, human_authorization_text, ticket_id, run_id, decision_SHA256, spawn_fn=None
):
    with _LOCK:
        p = pr._load_current_projection_record()
        if p["ticket_id"] != ticket_id or human_authorization_text != action(
            ticket_id, run_id, corrective=True
        ):
            raise pr.ProductRuntimeConflict(
                "exact separate corrective execution authorization required"
            )
        record = load(p, run_id, validate=False)
        if record is None or decision_SHA256 != record["decision_SHA256"]:
            raise pr.ProductRuntimeConflict(
                "corrective execution rejection authority mismatch"
            )
        result_path = path_for(p, run_id, "result")
        result = read(result_path)
        if result:
            return {**result["result"], "idempotent_replay": True}
        context(p, run_id)
        workflow = pr.build_workflow_control_snapshot()
        if (
            workflow.get("workflow_status") != STATE
            or workflow.get("active_execution_count")
            or workflow.get("remaining_blockers")
        ):
            raise pr.ProductRuntimeConflict(
                "corrective execution is not current eligible action"
            )
        provider = pr._executor_provider_readiness(p["assignee_profile"])
        if not provider.get("ok"):
            raise pr.ProductRuntimeConflict("corrective executor provider unavailable")
        probe = pr._preflight_pepper_governed_worker_credentials(
            p, enabled=spawn_fn is None
        )
        if not probe.get("ok"):
            raise pr.ProductRuntimeConflict("corrective worker credential unavailable")
        fresh = {
            "fresh_execution_provenance": PROVENANCE,
            "transition_classification": "HUMAN_ZERO_CHANGE_REJECTED_CORRECTION",
            "prior_terminal_run_id": run_id,
            "prior_terminal_completion_SHA256": record["terminal_run_SHA256"],
            "zero_change_decision_SHA256": decision_SHA256,
            "revision_source_base": "current_canonical_source",
            "implementation_intent": "Implement the original approved WorkPacket; compare requirements, produce missing changes, preserve inspectable equality evidence for any no-op.",
        }
        fresh["fresh_execution_request_SHA256"] = ev.digest(fresh)
        auth = read(path_for(p, run_id, "start"))
        if auth is None:
            auth = {
                "human_authorization_text": human_authorization_text,
                "rejection_SHA256": decision_SHA256,
                "created_at": pr._utc_now_iso(),
                "fresh_execution_request": fresh,
            }
            auth["decision_SHA256"] = ev.digest(auth)
            persist(path_for(p, run_id, "start"), auth)
        elif auth["fresh_execution_request"] != fresh:
            raise pr.ProductRuntimeConflict(
                "conflicting corrective execution authorization"
            )
        req = pr.CurrentTicketExecutionStartRequest(
            human_authorization_text=human_authorization_text,
            project_id=p["project_id"],
            ticket_id=ticket_id,
        )
        start_record = pr._build_execution_start_authorization_record(
            request=req, projection=p, provider_readiness=provider
        )
        start_record.update(
            zero_change_decision_SHA256=decision_SHA256,
            corrective_start_authority_SHA256=auth["decision_SHA256"],
        )
        start_record["start_authorization_SHA256"] = pr._execution_start_record_digest(
            start_record
        )
        old = pr.execution_start_record_path_for_ticket(ticket_id)
        if old.exists() and not path_for(p, run_id, "prior-execution-start").exists():
            prior = {
                "record": json.loads(old.read_text()),
                "record_text": old.read_text(),
            }
            prior["decision_SHA256"] = ev.digest(prior)
            persist(path_for(p, run_id, "prior-execution-start"), prior)
        pr._persist_execution_start_record(start_record)
        dispatched = pr._dispatch_exact_current_kanban_task(
            p,
            spawn_fn=spawn_fn,
            prepared_dispatch={
                "terminal_done_task_rearm_pending": True,
                "fresh_execution_request_reference": fresh,
                "source_run_id": run_id,
                "activation_action_SHA256": auth["decision_SHA256"],
                "backend_derived_live_authority_SHA256": decision_SHA256,
            },
        )
        final = pr._finalize_execution_start_record(
            start_record, dispatch_result=dispatched
        )
        pr._persist_execution_start_record(final)
        result = pr._execution_start_operational_result(final, idempotent_replay=False)
        saved = {"result": result}
        saved["decision_SHA256"] = ev.digest(saved)
        conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
        try:
            created_attempt = any(
                r.id > run_id for r in ev.kb.list_runs(conn, p["kanban_task_id"])
            )
        finally:
            conn.close()
        if created_attempt:
            persist(result_path, saved)
        return result


@contextmanager
def decision_lock(p, run_id):
    # Exclusive creation prevents concurrent positive/negative decisions across processes.
    path = path_for(p, run_id, "lock")
    ev.safe_path(path, ev.kb.kanban_home(), missing=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise pr.ProductRuntimeConflict(
                "zero-change human decision already in progress"
            ) from exc
        try:
            os.close(fd)
            yield
        finally:
            path.unlink()


def request(**kwargs):
    p = pr._load_current_projection_record()
    run_id = kwargs.get("run_id")
    if type(run_id) is not int or run_id < 1:
        raise pr.ProductRuntimeConflict("exact terminal run required")
    with decision_lock(p, run_id):
        return _request(**kwargs)


def start(**kwargs):
    p = pr._load_current_projection_record()
    run_id = kwargs.get("run_id")
    if type(run_id) is not int or run_id < 1:
        raise pr.ProductRuntimeConflict("exact terminal run required")
    with decision_lock(p, run_id):
        return _start(**kwargs)


def serialize_positive(callback, kwargs):
    p = pr._load_current_projection_record()
    if not ev.kb.kanban_db_path(board=p["kanban_board_slug"]).exists():
        return callback(**kwargs)
    conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        runs = ev.kb.list_runs(conn, p["kanban_task_id"])
    finally:
        conn.close()
    if not runs:
        return callback(**kwargs)
    with decision_lock(p, runs[-1].id):
        return callback(**kwargs)
