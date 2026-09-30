"""Explicit, immutable selection of a terminal material revision for human review."""

import json

from hermes_constants import get_hermes_home

POLICY = "pepper-terminal-review-revision-selection-v1"


def _runtime():
    from . import product_runtime

    return product_runtime


def _path(projection, run_id):
    pr = _runtime()
    key = pr._digest_payload(
        POLICY,
        {
            "projection_SHA256": projection["projection_SHA256"],
            "run_id": run_id,
        },
    )
    return (
        get_hermes_home()
        / "agent-platform"
        / "terminal-review-selections"
        / f"{key}.json"
    )


def _read(path):
    pr = _runtime()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("record must be an object")
        return value
    except (OSError, ValueError) as exc:
        raise pr.ProductRuntimeConflict(
            "terminal review selection evidence is unreadable"
        ) from exc


def _context(projection, saved=None):
    pr = _runtime()
    activation = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=projection
    )
    runtime = (
        pr.load_current_ticket_governed_autonomy_runtime_state(
            projection_record=projection,
            activation_record=activation,
        )
        if activation
        else None
    )
    if not runtime:
        raise pr.ProductRuntimeConflict(
            "terminal review selection requires revision runtime authority"
        )
    effective = pr._resolve_effective_current_governed_autonomy_authority(
        projection=projection,
        activation=activation,
        previous=runtime,
    )
    pr._require_current_governed_autonomy_authority_match(
        projection=projection,
        activation=activation,
        previous=runtime,
        effective_authority=effective,
    )
    completion = pr._kanban_completion_result_source(
        projection, reconcile_lifecycle=False
    )
    blocker = pr._completion_current_terminal_run_authority_blocker(
        projection,
        completion,
        unavailable_code="TERMINAL_REVIEW_RUN_UNAVAILABLE",
        mismatch_code="TERMINAL_REVIEW_RUN_MISMATCH",
    )
    if blocker or completion.get("blocker_code"):
        raise pr.ProductRuntimeConflict(str(blocker or completion["blocker_code"]))
    run_id = completion.get("run_id")
    # A subsequent REVISE records pending authority before persisting its decision.
    # Validate the immutable selection against its linked execution runtime.
    pending = runtime.get("fresh_execution_request_reference") or {}
    selected = (saved or {}).get("selection") or {}
    if (
        saved
        and runtime.get("governed_autonomy_runtime_status")
        == "review_revision_request_recorded_pending_continuation"
        and pending.get("fresh_execution_provenance") == "human_review_changes_requested"
        and pending.get("reviewed_run_id") == selected.get("terminal_run_id") == run_id
        and pending.get("prior_terminal_run_id") == run_id
        and pending.get("reviewed_candidate_SHA256") == selected.get("candidate_SHA256")
        and pending.get("fresh_execution_request_SHA256")
        != selected.get("review_revision_request_SHA256")
    ):
        for item in pr._governed_autonomy_runtime_lineage_records_newest_first(
            runtime, ticket_id=projection["ticket_id"]
        ):
            ancestor = pr._governed_autonomy_validate_runtime_lineage_candidate(
                item["record"], projection=projection, activation=activation
            )
            if (
                ancestor.get("kanban_run_id") == run_id
                and ancestor.get("fresh_execution_request_SHA256")
                == selected.get("review_revision_request_SHA256")
            ):
                runtime = ancestor
                break
    if runtime.get("kanban_run_id") != run_id:
        raise pr.ProductRuntimeConflict(
            "terminal review selection runtime run mismatch"
        )
    if not pr._review_prepare_human_git_handoff_required(completion):
        raise pr.ProductRuntimeConflict(
            "terminal revision has no eligible human-review candidate"
        )
    request = runtime.get("fresh_execution_request_reference") or {}
    if request.get("fresh_execution_provenance") != "human_review_changes_requested":
        raise pr.ProductRuntimeConflict(
            "terminal review selection requires material revision lineage"
        )
    decision = (saved or {}).get("predecessor_decision")
    if decision is None:
        decision = _read(
            pr.review_decision_record_path_for_ticket(projection["ticket_id"])
        )
    if not pr._review_decision_has_basic_current_ticket_identity(
        decision, projection=projection
    ):
        raise pr.ProductRuntimeConflict(
            "terminal review selection predecessor decision invalid"
        )
    predecessor = decision.get("reviewed_run_id")
    if (
        decision.get("review_decision") != "changes_requested"
        or not isinstance(predecessor, int)
        or isinstance(predecessor, bool)
        or predecessor >= run_id
        or request != decision.get("review_revision_request_reference")
        or runtime.get("fresh_execution_request_SHA256")
        != request.get("fresh_execution_request_SHA256")
        or runtime.get("prior_terminal_run_id") != predecessor
        or request.get("prior_terminal_run_id") != predecessor
        or request.get("reviewed_run_id") != predecessor
        or request.get("review_decision_SHA256")
        != decision.get("review_decision_identity_SHA256")
        or request.get("bounded_review_feedback_SHA256")
        != decision.get("bounded_review_feedback_SHA256")
        or not pr._governed_autonomy_fresh_execution_request_created_attempt(runtime)
    ):
        raise pr.ProductRuntimeConflict(
            "terminal review selection revision lineage mismatch"
        )
    package = (saved or {}).get("predecessor_package")
    if package is None:
        package = _read(
            pr.review_prepare_record_path_for_ticket(projection["ticket_id"])
        )
    if (
        not pr._review_prepare_record_matches_projection_identity(package, projection)
        or package.get("review_prepare_action_SHA256")
        != pr._review_prepare_record_digest(package)
        or package.get("successful_run_id") != predecessor
        or package.get("review_package_SHA256") != request.get("review_package_SHA256")
        or package.get("review_prepare_action_SHA256")
        != request.get("review_prepare_action_SHA256")
    ):
        raise pr.ProductRuntimeConflict(
            "terminal review selection predecessor package mismatch"
        )
    # Validate the unchanged human decision against its historical package,
    # rather than resolving the current candidate while validating its predecessor.
    pr.validate_current_ticket_review_decision_record(
        decision,
        projection_record=projection,
        review_prepare_record=package,
    )
    candidate = pr._review_candidate_reference_digest(
        projection,
        {"successful_run_id": run_id},
        completion.get("candidate_changes_reference"),
    )
    view = candidate_view({"completion": completion})
    # Validate every file with the same path, scope and hash guards as inspection.
    context = pr._current_review_candidate_authority_context(
        projection=projection,
        review_prepare=view,
    )
    for entry in context["files"].values():
        pr._review_candidate_file_context(context, entry)
    selection = {
        "choice": "terminal_governed_run_review",
        "work_packet_SHA256": projection["work_packet_SHA256"],
        "review_revision_request_SHA256": request["fresh_execution_request_SHA256"],
        "predecessor_reviewed_run_id": predecessor,
        "terminal_run_id": run_id,
        "candidate_SHA256": candidate,
    }
    return {
        "policy_id": POLICY,
        "selection": selection,
        "identity": {
            key: projection[key]
            for key in (
                "project_id",
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
                "projection_SHA256",
                "kanban_board_slug",
                "kanban_task_id",
            )
        },
        "predecessor_decision": decision,
        "predecessor_package": package,
        "completion": completion,
    }


def candidate_view(record):
    completion = record["completion"]
    return {
        "successful_run_id": completion["run_id"],
        "successful_run_status": completion["run_status"],
        "successful_run_outcome": completion["run_outcome"],
        "kanban_completion_result_SHA256": completion[
            "kanban_completion_result_SHA256"
        ],
        "kanban_completion_result": completion,
    }


def load(projection):
    pr = _runtime()
    if not (
        get_hermes_home() / "agent-platform" / "terminal-review-selections"
    ).exists():
        return None
    identity = pr._current_kanban_terminal_run_identity(projection)
    if not identity:
        return None
    path = _path(projection, identity["terminal_run_id"])
    if not path.exists():
        return None
    saved = _read(path)
    payload = {k: v for k, v in saved.items() if k != "selection_SHA256"}
    if saved.get("selection_SHA256") != pr._digest_payload(POLICY, payload):
        raise pr.ProductRuntimeConflict("terminal review selection digest mismatch")
    current = _context(projection, saved)
    if current != payload:
        raise pr.ProductRuntimeConflict("terminal review selection authority drift")
    return saved


def select(projection, selection):
    pr = _runtime()
    if not isinstance(selection, dict):
        raise pr.ProductRuntimeConflict("terminal review selection must be an object")
    existing = load(projection)
    record = _context(projection, existing)
    if selection != record["selection"] or any(
        type(selection.get(k)) is not int
        for k in ("terminal_run_id", "predecessor_reviewed_run_id")
    ):
        raise pr.ProductRuntimeConflict("terminal review selection guard mismatch")
    record["selection_SHA256"] = pr._digest_payload(POLICY, record)
    path = _path(projection, record["selection"]["terminal_run_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump(record, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
    except FileExistsError:
        if _read(path) != record:
            raise pr.ProductRuntimeConflict(
                "terminal review selection conflicts with existing authority"
            )
        existing = record
    workflow = pr.build_workflow_control_snapshot()
    return {
        "continuation_status": "terminal_revision_promoted_for_review",
        "terminal_review_selection": record["selection"],
        "selection_SHA256": record["selection_SHA256"],
        "reviewed_run_id": record["selection"]["terminal_run_id"],
        "reviewed_candidate_SHA256": record["selection"]["candidate_SHA256"],
        "idempotent_replay": existing is not None,
        "next_action": workflow["next_action"],
        "workflow_status": workflow["workflow_status"],
        "fresh_execution_requested": False,
        "kanban_run_created": False,
        "dispatch_performed": False,
        "execution_started": False,
        "worker_execution": False,
        "worker_process_started": False,
        "Kanban_dispatch": False,
        "Git_mutation": False,
        "review_decision_recorded": False,
    }


def supersedes(projection, record, kind):
    promoted = load(projection)
    return promoted is not None and record == promoted[f"predecessor_{kind}"]


def overlay(projection, promoted):
    pr = _runtime()
    return {
        "workflow_status": "execution_completed",
        "readiness": "terminal_revision_selected_for_review",
        "workflow_state": f"{projection['ticket_id']}-TERMINAL-REVISION-SELECTED-FOR-REVIEW",
        "execution_state": "no_active_executions",
        "active_execution_count": 0,
        "queue_state": "governed_autonomy_kanban_execution_terminal",
        "validation_state": "execution_completed_pending_validation",
        "review_state": "ready_for_review_validation",
        "recovery_state": "not_required",
        "reviewed_run_id": promoted["selection"]["terminal_run_id"],
        "reviewed_candidate_SHA256": promoted["selection"]["candidate_SHA256"],
        "terminal_review_selection": promoted["selection"],
        "review_decision_recorded": False,
        "human_acceptance_recorded": False,
        "review_decision_required": True,
        "human_acceptance_required": True,
        "next_action": {
            "id": pr.governed_ticket_lifecycle_action_ids(projection["ticket_id"])[
                "review_prepare"
            ],
            "target_ticket_id": projection["ticket_id"],
            "required_human_action": "review_validation_preparation",
        },
    }


def require_unconsumed_execution_choice(projection, *, text, resume_sha, override):
    """Only a new persisted review decision can cross a selected review boundary."""
    pr = _runtime()
    promoted = load(projection)
    if promoted is None or not (text or resume_sha or override is not None):
        return
    selected = promoted["selection"]
    decision = pr.load_current_ticket_review_decision_record(
        projection_record=projection
    )
    revision = (decision or {}).get("review_revision_request_reference") or {}
    new_sha = revision.get("fresh_execution_request_SHA256")
    if (
        decision
        and decision.get("review_decision") == "changes_requested"
        and decision.get("reviewed_run_id") == selected["terminal_run_id"]
        and decision.get("reviewed_candidate_SHA256") == selected["candidate_SHA256"]
        and new_sha
        and new_sha != selected["review_revision_request_SHA256"]
        and not text
        and (resume_sha == new_sha or override == revision)
    ):
        return
    raise pr.ProductRuntimeConflict(
        "TERMINAL_REVIEW_SELECTION_CHOICE_CONSUMED: selected terminal revision "
        "requires validation/review; fresh execution requires a new review decision"
    )
