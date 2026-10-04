"""Explicit post-accept/pre-Git material revision authority; no materialization."""

from functools import wraps
import hashlib
import json
import threading

from hermes_constants import get_hermes_home

POLICY = "pepper-post-accept-material-revision-v1"
REASON = "post_accept_pre_git_material_revision"
_BOUNDARY = threading.RLock()


def serialized(fn):
    """Serialize public review/handoff/execution decisions with supersession."""

    @wraps(fn)
    def call(*args, **kwargs):
        with _BOUNDARY:
            return fn(*args, **kwargs)

    return call


def digest(record):
    body = {k: v for k, v in record.items() if k != "material_revision_request_SHA256"}
    return hashlib.sha256(
        (
            POLICY
            + ":"
            + json.dumps(
                body,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        ).encode()
    ).hexdigest()


def action_id(ticket):
    from .product_runtime import governed_ticket_lifecycle_action_token

    return f"REQUEST_{governed_ticket_lifecycle_action_token(ticket)}_POST_ACCEPT_MATERIAL_REVISION"


def path_for(generation):
    from .workflow.ticket_architect_bridge import _safe_ticket_id, _safe_digest

    return (
        get_hermes_home()
        / "agent-platform/post-accept-material-revision"
        / f"{_safe_ticket_id(generation['ticket_id'])}.{_safe_digest(generation['work_packet_SHA256'])}.json"
    )


def validate_record(record, generation):
    from . import product_runtime as pr

    if record.get("material_revision_request_SHA256") != digest(record):
        raise ValueError("post-accept revision digest mismatch")
    expected = {
        "policy_id": POLICY,
        "reason_code": REASON,
        "human_authorization_text": action_id(generation["ticket_id"]),
        "handoff_state": "superseded_by_material_revision",
        "execution_started": False,
        "materialization_performed": False,
        "Git_mutation": False,
        "successor_generated": False,
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
    if any(record.get(k) != v for k, v in expected.items()):
        raise ValueError("post-accept revision authority mismatch")
    history = record.get("historical_authority", {})
    if history.get("review_decision", {}).get("review_decision") != "accept":
        raise ValueError("historical accepted review required")
    for container, field, calculate in (
        (
            "review_decision",
            "review_decision_SHA256",
            pr._review_decision_record_digest,
        ),
        (
            "review_prepare",
            "review_prepare_action_SHA256",
            pr._review_prepare_record_digest,
        ),
        (
            "handoff",
            "handoff_prepare_record_SHA256",
            pr._human_git_handoff_prepare_record_digest,
        ),
    ):
        saved = history.get(container, {})
        if saved.get(field) != calculate(saved):
            raise ValueError("historical authority digest mismatch")
    for field, container in (
        ("review_decision_SHA256", "review_decision"),
        ("review_decision_identity_SHA256", "review_decision"),
        ("review_package_SHA256", "review_prepare"),
        ("review_prepare_action_SHA256", "review_prepare"),
        ("handoff_prepare_record_SHA256", "handoff"),
        ("handoff_prepare_identity_SHA256", "handoff"),
        ("P17_7_handoff_package_SHA256", "handoff"),
    ):
        if not record.get(field) or record[field] != history.get(container, {}).get(
            field
        ):
            raise ValueError(f"post-accept historical {field} mismatch")
    return record


def load(generation):
    path = path_for(generation)
    if not path.exists():
        return None
    return validate_record(json.loads(path.read_text(encoding="utf-8")), generation)


def supersedes_lifecycle_record(projection, record, section):
    """Exclude only the authenticated predecessor of a current material revision.

    Ticket identity alone is never enough. The current generated publication,
    approval, projection and durable human transition must agree, and the file
    must equal the immutable historical evidence carried by that transition.
    Current records continue through their ordinary strict validators.
    """
    from . import product_runtime as pr
    from .workflow import ticket_architect_bridge as bridge

    identity = ("ticket_id", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256")
    if not isinstance(record, dict) or all(record.get(k) == projection.get(k) for k in identity):
        return False
    generation = bridge.load_generation_record(ticket_id=projection["ticket_id"])
    authority = (generation or {}).get("revision_authority") or {}
    if authority.get("revision_reason") != REASON:
        return False
    pr._validate_execution_start_authority(projection)
    approval = bridge.load_approval_decision_record(
        ticket_id=projection["ticket_id"], generation_record=generation,
    )
    publication = generation["ticket_publication_result"]["publication"]
    if (
        any(generation.get(k) != projection.get(k) for k in identity)
        or publication["revision"] != authority["new_publication_revision"]
        or not approval or approval.get("decision") != "approve"
        or approval.get("approval_publication_SHA256") != projection.get("approval_publication_SHA256")
    ):
        raise pr.ProductRuntimeConflict("current material-revision projection/approval authority mismatch")
    from .workflow.work_packet_kanban_projection import validate_kanban_projection_record
    validate_kanban_projection_record(
        projection, ticket_id=projection["ticket_id"],
        generation_record=generation, decision_record=approval,
    )
    transition = authority["material_revision_request_record"]
    durable = load(transition)
    if durable != transition:
        raise pr.ProductRuntimeConflict("post-accept historical transition is missing or changed")
    historical = transition["historical_authority"][section]
    if record != historical:
        raise pr.ProductRuntimeConflict(
            f"post-accept historical {section} differs from authenticated predecessor; "
            f"historical_revision={authority['previous_publication_revision']} "
            f"current_revision={publication['revision']} "
            f"expected_ticket_spec_SHA256={historical.get('ticket_spec_SHA256')} "
            f"actual_ticket_spec_SHA256={record.get('ticket_spec_SHA256')}"
        )
    return True


def assert_handoff_current(projection):
    # Even corrupt authority must never resurrect the old executable handoff.
    if path_for(projection).exists():
        raise ValueError(
            "human Git handoff superseded by post-accept material revision"
        )


def context(projection, *, git_snapshot_fn=None):
    from . import product_runtime as pr
    from .execution_evidence import connection
    from hermes_cli import kanban_db as kb
    from .workflow import ticket_architect_bridge as bridge

    authority = bridge.load_immutable_approved_current_ticket_authority(
        ticket_id=projection["ticket_id"], require_approved_decision=True
    )
    if authority is None:
        raise ValueError("current approved publication required")
    generation = authority["generation_record"]
    for key in (
        "ticket_id",
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
    ):
        if generation[key] != projection[key]:
            raise ValueError("post-accept current publication changed")
    # Presence itself fails closed, including invalid or incomplete completion.
    if pr.human_git_handoff_completion_record_path_for_ticket(
        projection["ticket_id"]
    ).exists():
        raise ValueError("handoff completion/closure evidence already exists")
    review = pr.load_current_ticket_review_decision_record(projection_record=projection)
    if review is None or review.get("review_decision") != "accept":
        raise ValueError("accepted current review required")
    prepared = pr.load_current_ticket_review_prepare_record(
        projection_record=projection
    )
    handoff = pr.load_current_ticket_human_git_handoff_prepare_record(
        projection_record=projection, review_decision_record=review
    )
    if prepared is None or handoff is None:
        raise ValueError("prepared unexecuted handoff required")
    conn = connection(kb.kanban_db_path(board=projection["kanban_board_slug"]))
    try:
        task = kb.get_task(conn, projection["kanban_task_id"])
        runs = kb.list_runs(conn, projection["kanban_task_id"])
        if (
            task is None
            or task.current_run_id is not None
            or task.claim_lock
            or (task.worker_pid and kb._pid_alive(task.worker_pid))
            or not runs
            or any(pr._execution_is_active(pr._run_dict(r)) for r in runs)
            or runs[-1].id != review["reviewed_run_id"]
            or runs[-1].ended_at is None
        ):
            raise ValueError(
                "post-accept revision requires the inactive reviewed terminal run"
            )
        if conn.execute(
            "SELECT 1 FROM tasks WHERE current_run_id IS NOT NULL LIMIT 1"
        ).fetchone():
            raise ValueError("another execution is active")
        if conn.execute(
            "SELECT 1 FROM task_runs WHERE ended_at IS NULL LIMIT 1"
        ).fetchone():
            raise ValueError("an unterminated execution exists")
    finally:
        conn.close()
    # Do not apply handoff's unrelated-dirt gate. Still prove no materialization,
    # source drift or staging of the accepted candidate has crossed the boundary.
    snapshot = pr._current_handoff_execution_git_snapshot(
        candidate_paths=tuple(handoff["candidate_paths"]),
        git_snapshot_fn=git_snapshot_fn,
    )
    execution = pr._human_git_handoff_execution_context(handoff, git_snapshot=snapshot)
    if (
        execution["candidate_source_basis_status"] != "unchanged"
        or execution["index_status"]["status"] != "empty"
        or not snapshot.get("head")
        or not snapshot.get("branch")
    ):
        raise ValueError(
            "candidate materialized, staged, drifted or source evidence unavailable"
        )
    # Generated successors must not coexist with reopening their predecessor.
    store = bridge.generation_record_path_for_ticket(generation["ticket_id"]).parent
    for path in store.glob("*.json"):
        other = json.loads(path.read_text(encoding="utf-8"))
        if other.get("ticket_id") != generation["ticket_id"] and (
            other.get("predecessor_ticket_id") == generation["ticket_id"]
            or (
                isinstance(other.get("canonical_roadmap_authority"), dict)
                and other["canonical_roadmap_authority"].get("predecessor_ticket_id")
                == generation["ticket_id"]
            )
        ):
            raise ValueError("a successor ticket already exists")
    from . import retry_material_revision

    if retry_material_revision.path_for(generation).exists():
        raise ValueError("conflicting material revision request exists")
    binding = {
        **{
            k: generation[k]
            for k in (
                "project_id",
                "macroproject_id",
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
            )
        },
        "publication_revision": bridge._publication_from_generation_record(
            generation
        ).revision,
        "projection_SHA256": projection["projection_SHA256"],
        "kanban_task_id": projection["kanban_task_id"],
        **{
            k: review[k]
            for k in (
                "reviewed_run_id",
                "reviewed_candidate_SHA256",
                "review_decision_SHA256",
                "review_decision_identity_SHA256",
            )
        },
        **{
            k: prepared[k]
            for k in ("review_package_SHA256", "review_prepare_action_SHA256")
        },
        **{
            k: handoff[k]
            for k in (
                "handoff_prepare_record_SHA256",
                "handoff_prepare_identity_SHA256",
                "P17_7_handoff_package_SHA256",
                "P17_7_handoff_result_SHA256",
                "materialization_plan_SHA256",
            )
        },
    }
    return (
        generation,
        binding,
        {
            "review_decision": review,
            "review_prepare": prepared,
            "handoff": handoff,
            "projection": projection,
        },
    )


def validate_current(record, projection):
    generation, binding, history = context(projection)
    validate_record(record, generation)
    if load(generation) != record or any(
        record.get(k) != v for k, v in binding.items()
    ):
        raise ValueError("post-accept revision current authority changed")
    if record["historical_authority"] != history:
        raise ValueError("post-accept historical authority changed")
    return record


@serialized
def request(
    *,
    human_authorization_text,
    binding,
    next_action_id,
    authorizer_id="pepper-chat-human",
):
    from . import product_runtime as pr
    from .workflow import ticket_architect_bridge as bridge

    if not isinstance(binding, dict):
        raise ValueError("exact post-accept binding required")
    action = action_id(binding.get("ticket_id", ""))
    if human_authorization_text != action or next_action_id != action:
        raise ValueError("exact post-accept human authorization required")
    authorizer_id = bridge._reviewer_id_from_actor(authorizer_id)
    with bridge._STORE_LOCK:
        projection = pr._load_current_projection_record()
        generation, current, history = context(projection)
        if binding != current:
            raise ValueError("post-accept request binding mismatch")
        existing = load(generation)
        if existing is not None:
            validate_current(existing, projection)
            if existing["authorizer_id"] != authorizer_id:
                raise ValueError("conflicting post-accept revision decision")
            return {**existing, "success": True, "idempotent_replay": True}
        record = {
            "schema_version": 1,
            "policy_id": POLICY,
            "reason_code": REASON,
            **current,
            "historical_authority": history,
            "historical_handoff_diagnosis": pr._human_git_handoff_prepare_execution_context_status(
                history["handoff"],
                git_snapshot=pr._current_handoff_execution_git_snapshot(
                    candidate_paths=tuple(history["handoff"]["candidate_paths"])
                ),
            ),
            "human_authorization_text": human_authorization_text,
            "authorizer_id": authorizer_id,
            "created_at": pr._utc_now_iso(),
            "human_decision": "request_successor_material_revision",
            "prior_state": "review_accepted_pending_human_git_handoff",
            "resulting_state": "awaiting_material_revision",
            "handoff_state": "superseded_by_material_revision",
            "successor_revision_intent": "same_ticket_fresh_canonical_source",
            "material_revision_required": True,
            "execution_started": False,
            "materialization_performed": False,
            "Git_mutation": False,
            "successor_generated": False,
            "next_action": revision_action(generation["ticket_id"]),
        }
        # Revalidate after construction and immediately before exclusive creation.
        if pr._load_current_projection_record() != projection or context(
            projection
        ) != (generation, current, history):
            raise ValueError("post-accept authority changed before persistence")
        record["material_revision_request_SHA256"] = digest(record)
        path = path_for(generation)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        return {**record, "success": True, "idempotent_replay": False}


def revision_action(ticket):
    from .product_runtime import governed_ticket_lifecycle_action_ids

    return {
        "id": governed_ticket_lifecycle_action_ids(ticket)["revise"],
        "target_ticket_id": ticket,
        "required_human_action": "ticket_material_revision",
        "label": "Separately authorize generation of the successor material revision; approval and execution remain separate.",
    }


def apply_workflow(snapshot, blockers):
    from . import product_runtime as pr

    exists = False
    try:
        projection = pr._load_current_projection_record()
        exists = path_for(projection).exists()
        if exists:
            from .workflow import ticket_architect_bridge as bridge

            current_generation = bridge.load_generation_record(
                ticket_id=projection["ticket_id"]
            )
            if (
                current_generation
                and current_generation["work_packet_SHA256"]
                != projection["work_packet_SHA256"]
            ):
                return
        if (
            not exists
            and snapshot.get("workflow_status")
            != "review_accepted_pending_human_git_handoff"
        ):
            return
        if snapshot.get("current_ticket_id") != projection["ticket_id"]:
            return
        generation, binding, _history = context(projection)
        if snapshot.get("current_ticket_id") != generation["ticket_id"] or snapshot.get(
            "active_execution_count"
        ):
            raise ValueError("current inactive accepted ticket required")
        record = load(generation)
        if record is None:
            snapshot.setdefault("alternative_actions", []).append({
                "id": action_id(generation["ticket_id"]),
                "target_ticket_id": generation["ticket_id"],
                "required_human_action": "post_accept_material_revision_request",
                "human_authorization_text": action_id(generation["ticket_id"]),
                "request_binding": binding,
                "label": "Request a successor material revision instead of executing the accepted handoff. Requires an explicit human choice.",
            })
            return
        validate_current(record, projection)
        snapshot.update({
            "workflow_status": "awaiting_material_revision",
            "workflow_state": f"{generation['ticket_id']}-AWAITING-MATERIAL-REVISION",
            "governed_workflow_state": "awaiting_material_revision",
            "review_state": "accepted_historical",
            "validation_state": "review_accepted_historical",
            "git_handoff_state": "superseded_by_material_revision",
            "human_git_handoff_state": "superseded_by_material_revision",
            "git_handoff_required": False,
            "material_revision_required": True,
            "material_revision_request_authority": record,
            "alternative_actions": [],
            "ticket_execution_authorized": False,
            "WorkPacket_execution_authorized": False,
            "runtime_execution_authorized": False,
            "next_action": revision_action(generation["ticket_id"]),
        })
        for key in (
            "current_ticket_human_git_handoff_prepare",
            "human_git_handoff_prepare_authority",
            "handoff_execution_context_blocker_code",
            "handoff_execution_context_blocker_detail",
        ):
            snapshot.pop(key, None)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        if exists:
            snapshot.update({
                "workflow_status": "material_revision_authority_blocked",
                "git_handoff_state": "superseded_by_material_revision",
                "alternative_actions": [],
                "next_action": {
                    "id": "RECONCILE_MATERIAL_REVISION_AUTHORITY",
                    "required_human_action": "authority_reconciliation",
                },
            })
            snapshot.pop("current_ticket_human_git_handoff_prepare", None)
            snapshot.pop("human_git_handoff_prepare_authority", None)
            blockers.append({
                "id": "POST-ACCEPT-MATERIAL-REVISION-AUTHORITY",
                "status": "blocked",
                "evidence": str(exc)[:300],
            })


def inspect_history(
    *,
    ticket_id,
    work_packet_SHA256,
    evidence_section=None,
    evidence_offset=0,
    candidate_path=None,
    max_bytes=None,
):
    from . import product_runtime as pr

    generation = {"ticket_id": ticket_id, "work_packet_SHA256": work_packet_SHA256}
    raw = json.loads(path_for(generation).read_text(encoding="utf-8"))
    if (
        raw.get("ticket_id") != ticket_id
        or raw.get("work_packet_SHA256") != work_packet_SHA256
    ):
        raise ValueError("historical request binding mismatch")
    validate_record(raw, raw)
    result = {
        "success": True,
        "read_only": True,
        "historical": True,
        "current_handoff_executable": False,
        "transition": raw,
    }
    if evidence_section in {"list", "metadata", "content", "diff", "aggregate_diff"}:
        history = raw["historical_authority"]
        return {
            **pr._build_current_review_candidate_inspection_result(
                projection=history["projection"],
                review_prepare=history["review_prepare"],
                operation=evidence_section,
                candidate_path=candidate_path,
                max_bytes=max_bytes,
            ),
            "historical": True,
            "current_handoff_executable": False,
            "material_revision_request_SHA256": raw["material_revision_request_SHA256"],
        }
    if evidence_section is not None:
        sections = {
            **raw["historical_authority"],
            "handoff_diagnosis": raw["historical_handoff_diagnosis"],
            "transition": raw,
        }
        if (
            evidence_section not in sections
            or type(evidence_offset) is not int
            or evidence_offset < 0
        ):
            raise ValueError("invalid historical evidence section or offset")
        text = json.dumps(
            sections[evidence_section], ensure_ascii=False, sort_keys=True
        )
        result.pop("transition")
        result.update(
            evidence_text=text[evidence_offset : evidence_offset + 12000],
            evidence_offset=evidence_offset,
            next_offset=evidence_offset + 12000
            if evidence_offset + 12000 < len(text)
            else None,
        )
    return result
