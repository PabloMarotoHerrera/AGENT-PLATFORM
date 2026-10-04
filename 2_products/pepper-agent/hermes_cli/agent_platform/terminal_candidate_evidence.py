"""Immutable terminal candidate evidence, captured before scratch cleanup."""

import json
import os
from pathlib import Path

from hermes_cli.agent_platform import execution_evidence as ev


def path_for(p, run):
    return (
        ev.pr.governed_source_authority_record_path_for_run(p, run.id).parent
        / "terminal-candidate.json"
    )


def identity(p, run, source):
    return {
        **ev.pr._current_ticket_projection_identity_fields(p),
        "projection_SHA256": p["projection_SHA256"],
        "task_id": p["kanban_task_id"],
        "run_id": run.id,
        "terminal_run_SHA256": ev.digest(ev.pr._run_dict(run)),
        "source_authority_SHA256": source["governed_source_authority_SHA256"],
    }


def load(p, run, source, workspace, offset=0):
    path = path_for(p, run)
    if not path.exists():
        return None
    record = ev.read_json(path, path.parent)
    payload = {k: v for k, v in record.items() if k != "evidence_SHA256"}
    if record.get("evidence_SHA256") != ev.digest(payload) or record.get(
        "binding"
    ) != identity(p, run, source):
        raise ValueError("terminal candidate evidence authority mismatch")
    if record.get("policy_id") != "pepper-terminal-candidate-evidence-v1":
        raise ValueError("terminal candidate policy mismatch")
    result = record["candidate"]
    if result["candidate_root"] != str(workspace) or result["file_total"] != len(
        result["files"]
    ):
        raise ValueError("terminal candidate manifest incomplete")
    entries = result["files"]
    src = {
        f["relative_path"]: f["SHA256"]
        for f in source["snapshot_manifest"]["files"]
        if ev._scope(f["relative_path"], source["materialization_manifest"])
    }
    observed = {}
    seen = set()
    for item in entries:
        rel = item["path"]
        if rel in seen or not ev._scope(rel, source["materialization_manifest"]):
            raise ValueError("terminal candidate scope mismatch")
        ev.safe_path(workspace / rel, workspace, missing=True)
        seen.add(rel)
        sha = item["candidate_SHA256"]
        if sha is not None:
            if not ev.re.fullmatch(r"[a-f0-9]{64}", sha):
                raise ValueError("invalid terminal candidate hash")
            observed[rel] = sha
        expected = (
            "equal"
            if src.get(rel) == sha
            else "added"
            if rel not in src
            else "deleted"
            if sha is None
            else "modified"
        )
        if item["source_SHA256"] != src.get(rel) or item["change"] != expected:
            raise ValueError("terminal candidate classification mismatch")
    changes = [e for e in entries if e["change"] != "equal"]
    if (
        result.get("available") is not True
        or result.get("source_authority_SHA256")
        != source["governed_source_authority_SHA256"]
        or result.get("source_snapshot_SHA256") != source["snapshot_SHA256"]
        or result.get("source_file_count") != len(src)
        or result.get("scope")
        != source["materialization_manifest"]["writable_allowed_paths"]
        or result.get("added_files") != sum(e["change"] == "added" for e in changes)
        or result.get("modified_files")
        != sum(e["change"] == "modified" for e in changes)
        or result.get("deleted_files") != sum(e["change"] == "deleted" for e in changes)
        or seen != src.keys() | observed.keys()
        or result["source_manifest_SHA256"] != ev.digest(src)
        or result["candidate_manifest_SHA256"] != ev.digest(observed)
        or result["diff_SHA256"] != ev.digest(entries)
        or result["candidate_file_count"] != len(observed)
        or result["changed_path_count"] != len(changes)
        or result["source_candidate_equal"] != (not changes)
        or result["zero_change_status"] != ("CONTRADICTED" if changes else "PROVEN")
    ):
        raise ValueError("terminal candidate evidence digest/count mismatch")
    return {
        **result,
        "candidate_exists": workspace.exists(),
        "candidate_manifest_kind": "immutable terminal governed hashes",
        "derivation": "validated pre-cleanup terminal manifest against durable source authority",
        "terminal_evidence_SHA256": record["evidence_SHA256"],
        "files": entries[offset : offset + ev.LIMIT],
        "changed_paths": changes[offset : offset + ev.LIMIT],
        "file_offset": offset,
        "next_offset": offset + ev.LIMIT if offset + ev.LIMIT < len(entries) else None,
    }


def sync_record(path):
    with path.open("rb") as stream:
        os.fsync(stream.fileno())
    if os.name == "posix":
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def before_cleanup(conn, task_id):
    """Permit unmanaged cleanup; retain governed scratch on any evidence gap."""
    task = ev.kb.get_task(conn, task_id)
    if task is None:
        return True
    try:
        body = json.loads(task.body or "{}")
    except (TypeError, ValueError):
        # Ordinary Kanban task descriptions are prose, not governed JSON.
        return not any(
            marker in str(task.body) for marker in ("WorkPacket_", "TicketSpec_")
        )
    if not isinstance(body, dict) or not body.get("WorkPacket_SHA256"):
        return True
    try:
        p = ev.pr._load_current_projection_record()
        if p["kanban_task_id"] != task_id:
            return False
        runs = ev.kb.list_runs(conn, task_id)
        run = runs[-1]
        if task.status != "done" or run.ended_at is None or run.outcome != "completed":
            return False
        _, checked, workspace = ev.run_context(p, run.id)
        source = ev.source(p, checked)
        if path_for(p, run).exists():
            previous = load(p, run, source, workspace)
            sync_record(path_for(p, run))
            return previous is not None and previous["source_candidate_equal"] is True
        result = ev.candidate(p, run, workspace, source)
        if not result.get("available"):
            return False
        entries = list(result["files"])
        while result.get("next_offset") is not None:
            result = ev.candidate(
                p, run, workspace, source, offset=result["next_offset"]
            )
            entries.extend(result["files"])
        # A second complete observation must be identical: no torn manifest.
        check = ev.candidate(p, run, workspace, source)
        if result["diff_SHA256"] != check["diff_SHA256"]:
            return False
        result.update(
            files=entries,
            changed_paths=[e for e in entries if e["change"] != "equal"],
            file_offset=0,
            next_offset=None,
        )
        record = {
            "captured_at": ev.pr._utc_now_iso(),
            "policy_id": "pepper-terminal-candidate-evidence-v1",
            "binding": identity(p, run, source),
            "candidate": result,
        }
        record["evidence_SHA256"] = ev.digest(record)
        path = path_for(p, run)
        ev.safe_path(path, path.parent, missing=True)
        encoded = json.dumps(record, sort_keys=True)
        if len(encoded.encode("utf-8")) > 16_000_000 or len(entries) > 10000:
            return False
        with path.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
        load(p, run, source, workspace)
        sync_record(path)
        # Changed candidates retain their contents for the existing review surface.
        return result["source_candidate_equal"] is True
    except Exception:
        return False
