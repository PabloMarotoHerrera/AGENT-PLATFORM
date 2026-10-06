"""Read-only current terminal candidate bytes, without prepared-review authority."""

import hashlib
from pathlib import Path, PurePosixPath

from . import execution_evidence as ev
from . import manual_validation as mv
from . import product_runtime as pr
from . import retry_workspace

OPERATIONS = {"list", "metadata", "content", "diff", "aggregate_diff"}
MAX_FILE_BYTES = 1_000_000
MAX_TEXT_BYTES = 8_000_000
MAX_OUTPUT_BYTES = 64_000


def context(ticket_id, run_id, project_id):
    p = pr._load_current_projection_record()
    if ticket_id != p["ticket_id"] or project_id not in (None, p["project_id"]):
        raise ValueError("current ticket/project authority mismatch")
    pr._validate_execution_start_authority(p)
    generation = ev.bridge.load_immutable_approved_current_ticket_authority(
        ticket_id=ticket_id, require_approved_decision=True
    )["generation_record"]
    if any(
        generation[k] != p[k]
        for k in ("ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256")
    ):
        raise ValueError("current approved generation mismatch")
    task, run, workspace = ev.run_context(p, run_id)
    conn = ev.connection(ev.kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        runs = ev.kb.list_runs(conn, task.id)
        if max(r.id for r in runs) != run_id or any(
            pr._execution_is_active(pr._run_dict(r)) for r in runs
        ):
            raise ValueError("active or ambiguous current terminal run")
    finally:
        conn.close()
    if task.current_run_id or task.worker_pid or task.claim_lock:
        raise ValueError("current task still owned by execution")
    prepared = pr._load_current_ticket_review_prepare_record_raw(projection_record=p)
    if prepared is not None:
        if (
            prepared.get("review_prepare_action_SHA256") != pr._review_prepare_record_digest(prepared)
            or pr.load_current_ticket_review_prepare_record(
                projection_record=p, allow_historical_mismatch=True,
            ) is not None
        ):
            raise ValueError("prepared review exists; use prepared-review inspection")
    source = ev.source(p, run)
    scope = generation["work_packet_compilation_result"]["work_packet"][
        "repository_scope"
    ]
    manifest = source["materialization_manifest"]
    if set(manifest["writable_allowed_paths"]) != set(scope["allowed_paths"]) or set(
        manifest["forbidden_paths"]
    ) != set(scope["forbidden_paths"]):
        raise ValueError(
            "source materialization scope differs from approved WorkPacket"
        )
    observed = ev.candidate(p, run, workspace, source)
    if not observed.get("available"):
        raise ValueError("current candidate unavailable")
    if workspace.exists():
        actual = ev.read_json(
            workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST, workspace
        )
        if actual.get("source_root") != source["snapshot_root"]:
            raise ValueError("candidate source root is not the durable source snapshot")
    # This is the same completion/contract predicate used by the manual-validation
    # overlay, with a read-only SQLite snapshot and no lifecycle reconciliation.
    completion = pr._kanban_completion_result_source(p, read_only=True)
    contract = pr._acceptance_contract_for_review_projection(p)
    if (
        completion.get("blocker_code")
        or completion.get("run_id") != run.id
        or not pr._review_prepare_human_git_handoff_required(completion)
    ):
        raise ValueError(
            "current terminal candidate is not at the manual-validation boundary"
        )
    items = mv.inspect(contract, completion)
    if not any(x["status"] == "pending" for x in items) or any(
        x["status"] == "failed" for x in items
    ):
        raise ValueError("pending manual validation required")
    return p, task, run, workspace, source, observed, items


def binding(p, task, run, workspace, source, observed):
    return {
        **{
            k: p[k]
            for k in (
                "project_id",
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
                "projection_SHA256",
            )
        },
        "task_id": task.id,
        "run_id": run.id,
        "workspace": str(workspace),
        "terminal_run_SHA256": ev.digest(pr._run_dict(run)),
        "source_authority_SHA256": source["governed_source_authority_SHA256"],
        **{
            k: observed[k]
            for k in (
                "source_manifest_SHA256",
                "candidate_manifest_SHA256",
                "diff_SHA256",
            )
        },
    }


def read_bytes(root, path, expected):
    target = ev.safe_path(root / path, root, missing=expected is None)
    if expected is None:
        if target.exists():
            raise ValueError("unexpected source/candidate file; repeat list")
        return b""
    if not target.is_file():
        raise ValueError("source/candidate is not a regular file")
    if target.stat().st_size > MAX_FILE_BYTES:
        return None
    with target.open("rb") as stream:
        raw = stream.read(MAX_FILE_BYTES + 1)
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("source/candidate hash changed; repeat list")
    return raw


def text(raw):
    if raw is None or b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def bounded(value, maximum):
    raw = value.encode("utf-8")
    retained = raw[:maximum].decode("utf-8", errors="ignore")
    return {
        "text": retained,
        "SHA256": hashlib.sha256(raw).hexdigest(),
        "byte_count": len(raw),
        "line_count": len(value.splitlines()),
        "retained_byte_count": len(retained.encode("utf-8")),
        "retained_line_count": len(retained.splitlines()),
        "max_bytes": maximum,
        "truncated": len(raw) > maximum,
        "complete": len(raw) <= maximum,
    }


def inspect(
    *,
    operation,
    ticket_id,
    reviewed_run_id,
    project_id=None,
    candidate_path=None,
    candidate_binding_SHA256=None,
    evidence_offset=0,
    max_bytes=None,
):
    """List establishes a stateless hash guard required by all subsequent reads."""
    if operation not in OPERATIONS or type(reviewed_run_id) is not int:
        raise ValueError("exact current terminal run and valid operation required")
    if type(evidence_offset) is not int or not 0 <= evidence_offset <= 10000:
        raise ValueError("invalid bounded page offset")
    if max_bytes is not None and (type(max_bytes) is not int or max_bytes <= 0):
        raise ValueError("positive integer byte bound required")
    maximum = min(max_bytes or 32000, MAX_OUTPUT_BYTES)
    if operation != "list" and not candidate_binding_SHA256:
        raise ValueError("list first and supply candidate_binding_SHA256")
    if operation in {"metadata", "content", "diff"}:
        if (
            not isinstance(candidate_path, str)
            or not candidate_path
            or "\\" in candidate_path
            or ":" in candidate_path
            or PurePosixPath(candidate_path).is_absolute()
            or any(x in {"", ".", ".."} for x in candidate_path.split("/"))
        ):
            raise ValueError("exact candidate-listed relative path required")
    elif candidate_path is not None:
        raise ValueError("this operation does not accept a path")
    p, task, run, workspace, source, observed, items = context(
        ticket_id, reviewed_run_id, project_id
    )
    identity = binding(p, task, run, workspace, source, observed)
    identity_sha = ev.digest(identity)
    if candidate_binding_SHA256 not in (None, identity_sha):
        raise ValueError("candidate binding changed; repeat list")
    if not observed["changed_path_count"]:
        raise ValueError("current candidate has no changed paths")
    page = ev.candidate(p, run, workspace, source, offset=evidence_offset)
    if page["diff_SHA256"] != observed["diff_SHA256"]:
        raise ValueError("candidate changed during observation; repeat list")
    result = {
        **pr._review_candidate_inspection_base_result(
            p, operation="pre_review_" + operation
        ),
        "success": True,
        "read_only": True,
        "inspection_authority": "current_terminal_candidate",
        **retry_workspace.freshness(task),
        "review_prepared": False,
        "review_preparation_recorded": False,
        "workflow_mutation": False,
        "manual_validation_satisfied": False,
        "manual_validation_recorded": False,
        "binding": identity,
        "source_authority": {
            "source_authority_kind": source["source_authority_kind"],
            "source_HEAD": source.get("git_source_authority", {}).get("git_HEAD"),
            "source_authority_SHA256": source["governed_source_authority_SHA256"],
            "source_snapshot_SHA256": source["snapshot_SHA256"],
            "snapshot_manifest_SHA256": source["snapshot_manifest_SHA256"],
            "materialization_manifest_SHA256": source["materialization_manifest_SHA256"],
        },
        "candidate_binding_SHA256": identity_sha,
        "workflow_status": "execution_completed_pending_manual_validation",
        "manual_validation_statuses": {x["validation_id"]: x["status"] for x in items},
        "integrity_validation_result": "passed",
        "WorkPacket_scope_validation_result": "passed",
        **{
            k: observed[k]
            for k in (
                "candidate_file_count",
                "changed_path_count",
                "source_manifest_SHA256",
                "candidate_manifest_SHA256",
                "diff_SHA256",
            )
        },
        "changed_paths": page["changed_paths"],
        "offset": evidence_offset,
        "page_size": ev.LIMIT,
        "list_complete": evidence_offset == 0
        and observed["changed_path_count"] <= ev.LIMIT,
        "list_truncated": observed["changed_path_count"] > ev.LIMIT,
        "next_offset": evidence_offset + ev.LIMIT
        if evidence_offset + ev.LIMIT < observed["changed_path_count"]
        else None,
        "inspection_status": "list_available",
    }
    if operation != "list":
        # C68 paginates both manifests and changed paths. Collect only the changed
        # pages needed; recheck the aggregate identity on every observation.
        changes = list(observed["changed_paths"])
        for offset in range(ev.LIMIT, observed["changed_path_count"], ev.LIMIT):
            more = ev.candidate(p, run, workspace, source, offset=offset)
            if more["diff_SHA256"] != observed["diff_SHA256"]:
                raise ValueError("candidate changed during pagination; repeat list")
            changes.extend(more["changed_paths"])
        if candidate_path is not None:
            changes = [x for x in changes if x["path"] == candidate_path]
            if not changes:
                raise ValueError("path is not an exact current changed candidate path")
        elif operation == "aggregate_diff":
            changes = changes[evidence_offset : evidence_offset + ev.LIMIT]
        sections, omitted, total_read, full = [], [], 0, []
        for entry in changes:
            rel = entry["path"]
            if not ev._scope(rel, source["materialization_manifest"]):
                raise ValueError("candidate path outside governed scope")
            if not observed["candidate_exists"]:
                omitted.append(rel)
                continue
            a = read_bytes(Path(source["snapshot_root"]), rel, entry["source_SHA256"])
            b = read_bytes(workspace, rel, entry["candidate_SHA256"])
            total_read += len(a or b"") + len(b or b"")
            if total_read > MAX_TEXT_BYTES:
                omitted.append(rel)
                continue
            section = dict(entry)
            for label, raw in (("source", a), ("candidate", b)):
                value = text(raw)
                section[label] = {"available": value is not None}
                if value is not None:
                    section[label].update(bounded(value, maximum))
                    if operation != "content":
                        section[label].pop("text")
            if operation in {"diff", "aggregate_diff"}:
                if text(a) is None or text(b) is None:
                    omitted.append(rel)
                else:
                    diff = pr._review_candidate_unified_diff(
                        rel,
                        source_text=text(a),
                        candidate_text=text(b),
                        max_bytes=MAX_TEXT_BYTES,
                    )
                    section["diff"] = bounded(diff["text"], maximum)
                    if operation == "aggregate_diff":
                        full.append((rel, diff["text"]))
                        section["diff"].pop("text")
            sections.append(section)
        result.update(
            inspection_status=operation + "_available",
            sections=sections,
            omitted_paths=omitted,
            text_input_max_bytes=MAX_FILE_BYTES,
        )
        if operation == "aggregate_diff":
            result["aggregate_diff"] = bounded(
                "".join(value for _, value in full), maximum
            )
            result["aggregate_diff"]["complete"] &= (
                not omitted and result["next_offset"] is None and evidence_offset == 0
            )
            if result["aggregate_diff"]["truncated"]:
                end = 0
                for rel, value in full:
                    end += len(value.encode("utf-8"))
                    if end > maximum:
                        omitted.append(rel)
            result["aggregate_diff"]["scope"] = "changed-path page"
    # Revalidate source, current run/contract, and the complete candidate after byte
    # reads. A concurrent edit/dispatch cannot return a stale successful response.
    p2, t2, r2, w2, s2, o2, i2 = context(ticket_id, reviewed_run_id, project_id)
    if binding(p2, t2, r2, w2, s2, o2) != identity or i2 != items:
        raise ValueError("authority changed during inspection; repeat list")
    return result
