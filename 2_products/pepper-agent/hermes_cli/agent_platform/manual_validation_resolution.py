"""Immutable human classification and separately authorized manual correction."""

from . import product_runtime as pr, manual_validation as mv
from . import zero_change_decision as correction
from . import execution_evidence as ev
from .post_accept_material_revision import serialized
from .workflow import ticket_architect_bridge as bridge

POLICY = "pepper-manual-validation-resolution-v1"
REASON = "manual_validation_failure_material_revision"
IMPLEMENTATION = "IMPLEMENTATION_CORRECTION_REQUIRED"
MATERIAL = "MATERIAL_REVISION_REQUIRED"
STATE = "manual_validation_correction_authorized"
PROVENANCE = "human_manual_validation_failure_correction"


def action(ticket, run_id=None):
    token = pr.governed_ticket_lifecycle_action_token(ticket)
    return (
        f"RESOLVE_{token}_MANUAL_VALIDATION_FAILURE"
        if run_id is None
        else f"START_{token}_MANUAL_VALIDATION_CORRECTIVE_EXECUTION_RUN_{run_id}"
    )


def path_for(p, run_id, kind="decision"):
    return (
        correction.path_for(p, run_id).parents[2]
        / "manual-validation-resolutions"
        / p["projection_SHA256"]
        / f"r{int(run_id)}-{kind}.json"
    )


def digest(record):
    return ev.digest({
        k: v
        for k, v in record.items()
        if k not in {"decision_SHA256", "material_revision_request_SHA256"}
    })


def consent(binding, decision):
    return f"{action(binding['ticket_id'])} {decision} BINDING {ev.digest(binding)}"


def start_consent(record):
    return f"{action(record['ticket_id'], record['run_id'])} DECISION {record['decision_SHA256']}"


def fresh_request(record):
    fresh = {
        "fresh_execution_provenance": PROVENANCE,
        "transition_classification": "HUMAN_MANUAL_VALIDATION_CORRECTION",
        "prior_terminal_run_id": record["run_id"],
        "prior_terminal_completion_SHA256": record["terminal_run_SHA256"],
        "manual_validation_resolution_SHA256": record["decision_SHA256"],
        "revision_source_base": "current_canonical_source",
        "implementation_intent": record["corrective_guidance"],
    }
    fresh["fresh_execution_request_SHA256"] = ev.digest(fresh)
    return fresh


def start_authority(p, record):
    auth = correction.read(path_for(p, record["run_id"], "start"))
    if auth is not None and (
        record["human_decision"] != IMPLEMENTATION
        or auth.get("resolution_SHA256") != record["decision_SHA256"]
        or auth.get("human_authorization_text") != start_consent(record)
        or auth.get("fresh_execution_request") != fresh_request(record)
    ):
        raise pr.ProductRuntimeConflict("conflicting corrective start authority")
    return auth


def guidance(value):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 8000:
        raise pr.ProductRuntimeConflict(
            "corrective guidance must contain 1-8000 characters"
        )
    if any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise pr.ProductRuntimeConflict(
            "corrective guidance contains control characters"
        )
    return value.strip()


def context(p):
    pr._validate_execution_start_authority(p)
    authority = bridge.load_immutable_approved_current_ticket_authority(
        ticket_id=p["ticket_id"],
        require_approved_decision=True,
    )
    if authority is None:
        raise pr.ProductRuntimeConflict("current approved WorkPacket is required")
    generation = authority["generation_record"]
    from .workflow.work_packet_kanban_projection import (
        validate_kanban_projection_record,
    )

    validate_kanban_projection_record(
        p,
        ticket_id=p["ticket_id"],
        generation_record=generation,
        decision_record=authority["approval_decision_record"],
    )
    manual = pr._current_manual_validation_context(p)
    failed = [i for i in manual["items"] if i["status"] == "failed"]
    if len(failed) != 1:
        raise pr.ProductRuntimeConflict(
            "one current required failed manual validation is required"
        )
    item = failed[0]
    task, run, _ = ev.run_context(p, manual["run_id"])
    require_terminal_candidate(p, task, run)
    conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        if conn.execute("SELECT COUNT(*) FROM tasks WHERE status='running'").fetchone()[
            0
        ]:
            raise pr.ProductRuntimeConflict(
                "concurrent active execution prevents resolution"
            )
    finally:
        conn.close()
    evidence = mv.load(item["binding"])
    binding = {k: p[k] for k in correction.KEYS}
    binding.update(
        publication_revision=generation["ticket_publication_result"]["publication"][
            "revision"
        ],
        run_id=run.id,
        validation_id=item["validation_id"],
        binding_SHA256=item["binding_SHA256"],
        validation_contract_SHA256=item["binding"]["validation_contract_SHA256"],
        evidence_SHA256=item["evidence_SHA256"],
        terminal_run_SHA256=ev.digest(pr._run_dict(run)),
        approved_generation_SHA256=ev.digest(generation),
        approval_decision_SHA256=ev.digest(authority["approval_decision_record"]),
        kanban_task_id=p["kanban_task_id"],
        kanban_board_slug=p["kanban_board_slug"],
    )
    return binding, evidence


def require_terminal_candidate(p, task, run):
    if task.current_run_id or task.worker_pid or task.claim_lock:
        raise pr.ProductRuntimeConflict("terminal candidate is still owned")
    completed = (
        task.status == "done" and run.status == "done" and run.outcome == "completed"
    )
    # Re-queueing can move a terminal needs_input task to triage/ready. The
    # canonical verifier retains that run's validated review boundary while
    # checking ownership, immutable scope, candidate changes and validation.
    review_boundary = pr._terminal_run_review_boundary_evidence(
        task, run, projection_record=p
    ) is not None
    if not completed and not review_boundary:
        raise pr.ProductRuntimeConflict(
            "completed or validated review-boundary candidate required"
        )


def validate_record(record, generation):
    if not isinstance(record, dict) or record.get("decision_SHA256") != digest(record):
        raise pr.ProductRuntimeConflict("manual resolution digest mismatch")
    b = record["binding"]
    if (
        record.get("policy_id") != POLICY
        or record.get("human_decision") not in {IMPLEMENTATION, MATERIAL}
        or record.get("material_revision_request_SHA256") != record["decision_SHA256"]
        or any(record.get(k) != b.get(k) for k in b)
        or any(
            record.get(k) != generation.get(k)
            for k in (
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
            )
        )
        or record.get("human_authorization_text")
        != consent(b, record["human_decision"])
        or record.get("corrective_guidance_SHA256")
        != ev.digest(guidance(record["corrective_guidance"]))
        or not record.get("authorizer")
        or not record.get("created_at")
    ):
        raise pr.ProductRuntimeConflict("manual resolution authority mismatch")
    evidence = record["failed_evidence"]
    mv.validate_record(evidence, evidence["binding"])
    identity = evidence["binding"]
    if (
        evidence["status"] != "failed"
        or evidence["evidence_SHA256"] != b["evidence_SHA256"]
        or mv.digest(identity) != b["binding_SHA256"]
        or any(
            identity.get(k) != b.get(k)
            for k in (
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
                "run_id",
                "validation_id",
                "validation_contract_SHA256",
            )
        )
    ):
        raise pr.ProductRuntimeConflict("manual resolution failed evidence mismatch")
    return record


def load(p, run_id):
    path = path_for(p, run_id)
    if not path.exists():
        return None
    record = ev.read_json(path, ev.kb.kanban_home())
    validate_record(record, p)
    if (
        record["projection_SHA256"] != p["projection_SHA256"]
        or record["run_id"] != run_id
    ):
        raise pr.ProductRuntimeConflict("manual resolution projection/run mismatch")
    if mv.load(record["failed_evidence"]["binding"]) != record["failed_evidence"]:
        raise pr.ProductRuntimeConflict("manual failure evidence missing or changed")
    return record


def current(p):
    if not path_for(p, 1).parent.exists():
        return None
    conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        runs = ev.kb.list_runs(conn, p["kanban_task_id"])
    finally:
        conn.close()
    return load(p, runs[-1].id) if runs else None


def validate_current(record, p):
    binding, evidence = context(p)
    if (
        load(p, binding["run_id"]) != record
        or record["binding"] != binding
        or record["failed_evidence"] != evidence
    ):
        raise pr.ProductRuntimeConflict("manual resolution current authority changed")


def discovery(p):
    binding, _ = context(p)
    return {
        "id": action(p["ticket_id"]),
        "target_ticket_id": p["ticket_id"],
        "required_human_action": "manual_validation_failure_resolution",
        "tool": "resolve_current_ticket_manual_validation_failure",
        "resolution_binding": binding,
        "choices": [
            {"decision": d, "required_human_authorization_text": consent(binding, d)}
            for d in (IMPLEMENTATION, MATERIAL)
        ],
        "label": "Explicitly classify the failed manual validation; resolution never starts execution.",
    }


def next_action(record):
    if record["human_decision"] == MATERIAL:
        return {
            "id": bridge.revise_action_id(record["ticket_id"]),
            "target_ticket_id": record["ticket_id"],
            "required_human_action": "ticket_material_revision",
            "label": "Separately authorize a structured material revision; no automatic generation.",
        }
    return {
        "id": action(record["ticket_id"], record["run_id"]),
        "target_ticket_id": record["ticket_id"],
        "run_id": record["run_id"],
        "decision_SHA256": record["decision_SHA256"],
        "required_human_action": "fresh_corrective_execution_authorization",
        "required_human_authorization_text": start_consent(record),
        "tool": "start_current_ticket_manual_validation_correction",
        "label": "Separately authorize a fresh run of the same approved WorkPacket from canonical source.",
    }


def operational(record, replay=False):
    return {
        "resolution": record,
        "decision_SHA256": record["decision_SHA256"],
        "idempotent_replay": replay,
        "next_action": next_action(record),
        "execution_started": False,
        "dispatch_performed": False,
        "revision_generated": False,
        "Git_mutation": False,
    }


@serialized
def resolve(
    *,
    binding,
    decision,
    human_authorization_text,
    corrective_guidance,
    authorizer="pepper-chat-human",
):
    if not isinstance(binding, dict) or type(binding.get("run_id")) is not int:
        raise pr.ProductRuntimeConflict("exact resolution binding required")
    if decision not in {IMPLEMENTATION, MATERIAL}:
        raise pr.ProductRuntimeConflict(
            "explicit supported resolution classification required"
        )
    if human_authorization_text != consent(binding, decision):
        raise pr.ProductRuntimeConflict(
            "exact explicit human resolution authorization required"
        )
    corrective_guidance = guidance(corrective_guidance)
    if not isinstance(authorizer, str) or not 1 <= len(authorizer.strip()) <= 128:
        raise pr.ProductRuntimeConflict("bounded authorizer required")
    p = pr._load_current_projection_record()
    with correction.decision_lock(p, binding["run_id"]):
        old = load(p, binding["run_id"])
        if old:
            if (
                old["binding"] != binding
                or old["human_decision"] != decision
                or old["corrective_guidance"] != corrective_guidance
                or old["authorizer"] != authorizer
            ):
                raise pr.ProductRuntimeConflict(
                    "conflicting immutable manual resolution"
                )
            return operational(old, True)
        actual, evidence = context(p)
        if actual != binding:
            raise pr.ProductRuntimeConflict("manual resolution binding changed")
        workflow = pr.build_workflow_control_snapshot()
        if workflow.get(
            "workflow_status"
        ) != "blocked_manual_validation_failed" or workflow.get("remaining_blockers"):
            raise pr.ProductRuntimeConflict(
                "manual failure is not the current resolvable action"
            )
        record = {
            **binding,
            "binding": binding,
            "policy_id": POLICY,
            "failed_evidence": evidence,
            "human_decision": decision,
            "human_authorization_text": human_authorization_text,
            "corrective_guidance": corrective_guidance,
            "corrective_guidance_SHA256": ev.digest(corrective_guidance),
            "authorizer": authorizer,
            "created_at": pr._utc_now_iso(),
        }
        record["decision_SHA256"] = digest(record)
        record["material_revision_request_SHA256"] = record["decision_SHA256"]
        validate_record(record, p)
        latest = pr._load_current_projection_record()
        if latest != p or context(latest) != (actual, evidence):
            raise pr.ProductRuntimeConflict(
                "manual resolution authority changed before persistence"
            )
        correction.persist(path_for(p, binding["run_id"]), record)
        return operational(record)


def apply_workflow(snapshot, blockers):
    if snapshot.get("workflow_status") not in {
        "blocked_manual_validation_failed",
        STATE,
        "awaiting_material_revision",
        "queued",
    }:
        return
    try:
        p = pr._load_current_projection_record()
        record = current(p)
        if record is None:
            if snapshot.get("workflow_status") == "blocked_manual_validation_failed":
                snapshot["next_action"] = discovery(p)
                snapshot["human_action_required"] = True
            return
        validate_current(record, p)
        auth = start_authority(p, record)
        if snapshot.get("workflow_status") == "queued":
            # A failed pre-run dispatch replaces the general start record but
            # does not consume the immutable, separately consented correction.
            attempt = pr.load_p18_9_0_execution_start_record(projection_record=p)
            if (
                auth is None
                or attempt is None
                or attempt.get("corrective_start_authority_SHA256") != auth["decision_SHA256"]
                or attempt.get("manual_validation_resolution_SHA256") != record["decision_SHA256"]
                or attempt.get("dispatch_performed") is not False
                or attempt.get("kanban_run_id") is not None
                or attempt.get("execution_started") is not False
            ):
                raise pr.ProductRuntimeConflict("queued corrective start authority mismatch")
        material = record["human_decision"] == MATERIAL
        snapshot.update(
            human_action_required=True,
            governed_workflow_state=f"{p['ticket_id']}-AWAITING-MATERIAL-REVISION"
            if material
            else STATE,
            workflow_status="awaiting_material_revision" if material else STATE,
            workflow_state=f"{p['ticket_id']}-AWAITING-MATERIAL-REVISION"
            if material
            else STATE,
            validation_state="manual_validation_failed_historical_correction_pending",
            review_state="blocked_pending_corrective_execution"
            if not material
            else "material_revision_required",
            reviewable_result=False,
            validation_contract_satisfied=False,
            next_action=next_action(record),
            alternative_actions=[],
            manual_validation_resolution=record,
        )
        if material:
            snapshot.update(
                material_revision_required=True,
                material_revision_request_authority=record,
            )
        elif auth is not None:
            snapshot["recovery_state"] = "manual_correction_start_retryable"
            snapshot["next_action"].update(
                retry_same_authority=True,
                corrective_start_authority_SHA256=auth["decision_SHA256"],
                label="Retry the recorded corrective-start authority; no fresh run has been created.",
            )
    except Exception as exc:
        # Do not advertise the legacy resolvable placeholder when its current
        # authority failed validation. The blocker is the actionable diagnosis.
        snapshot.update(
            next_action=None,
            alternative_actions=[],
            human_action_required=True,
            reviewable_result=False,
            validation_contract_satisfied=False,
        )
        blockers.append({
            "id": "MANUAL-VALIDATION-RESOLUTION-AUTHORITY",
            "status": "blocked_by_invalid_manual_resolution",
            "evidence": str(exc)[:300],
        })


def corrective_blocker(p, fresh, *, task=None, runs=None):
    try:
        run_id = fresh["prior_terminal_run_id"]
        record = load(p, run_id)
        if task is None:
            validate_current(record, p)
        else:
            # The dispatcher holds the Kanban write transaction here. Never
            # invoke lifecycle reconciliation through a second connection.
            pr._validate_execution_start_authority(p)
            from .workflow.work_packet_kanban_projection import (
                kanban_projection_record_path_for_ticket,
            )

            current_projection = ev.read_json(
                kanban_projection_record_path_for_ticket(p["ticket_id"]),
                ev.kb.kanban_home(),
            )
            generation = ev.read_json(
                bridge.generation_record_path_for_ticket(p["ticket_id"]),
                ev.kb.kanban_home(),
            )
            approval = ev.read_json(
                bridge.approval_decision_record_path_for_ticket(p["ticket_id"]),
                ev.kb.kanban_home(),
            )
            if (
                current_projection != p
                or not runs
                or ev.digest(generation) != record["approved_generation_SHA256"]
                or ev.digest(approval) != record["approval_decision_SHA256"]
            ):
                raise ValueError("current projection/run authority changed")
            if (
                runs[-1].id != run_id
                or ev.digest(pr._run_dict(runs[-1])) != record["terminal_run_SHA256"]
                or task.current_run_id
                or task.claim_lock
                or task.worker_pid
            ):
                raise ValueError(
                    "current terminal run changed inside dispatch transaction"
                )
            require_terminal_candidate(p, task, runs[-1])
        auth = start_authority(p, record)
        if (
            record["human_decision"] != IMPLEMENTATION
            or not auth
            or auth["resolution_SHA256"] != record["decision_SHA256"]
            or auth["human_authorization_text"] != start_consent(record)
            or auth["fresh_execution_request"] != fresh
        ):
            raise ValueError("separate corrective execution authority mismatch")
        return None
    except Exception as exc:
        return "MANUAL_VALIDATION_CORRECTIVE_AUTHORITY_INVALID", str(exc)


@serialized
def start(
    *, ticket_id, run_id, decision_SHA256, human_authorization_text, spawn_fn=None
):
    if type(run_id) is not int or run_id < 1:
        raise pr.ProductRuntimeConflict("exact failed run required")
    p = pr._load_current_projection_record()
    with correction.decision_lock(p, run_id):
        record = load(p, run_id)
        if (
            not record
            or p["ticket_id"] != ticket_id
            or record["human_decision"] != IMPLEMENTATION
            or record["decision_SHA256"] != decision_SHA256
            or human_authorization_text != start_consent(record)
        ):
            raise pr.ProductRuntimeConflict(
                "exact separate corrective execution authorization required"
            )
        replay = correction.read(path_for(p, run_id, "result"))
        if replay:
            return {**replay["result"], "idempotent_replay": True}
        validate_current(record, p)
        workflow = pr.build_workflow_control_snapshot()
        if (
            workflow.get("workflow_status") != STATE
            or workflow.get("remaining_blockers")
            or workflow.get("active_execution_count")
        ):
            raise pr.ProductRuntimeConflict(
                "manual corrective execution is not current eligible action"
            )
        provider = pr._executor_provider_readiness(p["assignee_profile"])
        probe = pr._preflight_pepper_governed_worker_credentials(
            p, enabled=spawn_fn is None
        )
        if not provider.get("ok") or not probe.get("ok"):
            raise pr.ProductRuntimeConflict("corrective worker/provider unavailable")
        fresh = fresh_request(record)
        validate_current(record, pr._load_current_projection_record())
        auth = start_authority(p, record)
        if auth is None:
            auth = {
                "human_authorization_text": human_authorization_text,
                "resolution_SHA256": decision_SHA256,
                "created_at": pr._utc_now_iso(),
                "fresh_execution_request": fresh,
            }
            auth["decision_SHA256"] = ev.digest(auth)
            correction.persist(path_for(p, run_id, "start"), auth)
        elif auth["fresh_execution_request"] != fresh:
            raise pr.ProductRuntimeConflict("conflicting corrective start authority")
        return correction.dispatch_correction(
            p=p,
            run_id=run_id,
            human_authorization_text=human_authorization_text,
            decision_SHA256=decision_SHA256,
            auth=auth,
            fresh=fresh,
            provider=provider,
            spawn_fn=spawn_fn,
            storage=path_for,
            decision_field="manual_validation_resolution_SHA256",
        )
