"""Bounded persisted execution evidence. No workflow builders or execution APIs."""

import hashlib
import fnmatch
import json
import os
from pathlib import Path
import re
import sqlite3
from collections.abc import Mapping

from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    assert_existing_path_contained,
)
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)

LIMIT = 25
MAX_MESSAGES = 2000


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def unavailable(reason):
    return {"available": False, "reason": reason}


def safe_path(path, root, *, missing=False):
    path, root = Path(path), Path(root)
    if not path.is_absolute() or not path.is_relative_to(root):
        raise ValueError("path outside canonical authority")
    cursor = path
    while cursor != root.parent:
        if cursor.is_symlink():
            raise ValueError("symlink evidence is unavailable")
        cursor = cursor.parent
    if not missing or path.exists():
        assert_existing_path_contained(path, containment_root=root)
    return path


def read_json(path, root, *, maximum=16_000_000):
    path = safe_path(path, root)
    if path.stat().st_size > maximum:
        raise ValueError("evidence record exceeds inspection bound")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    if len(raw) > maximum:
        raise ValueError("evidence record exceeds inspection bound")
    return json.loads(raw)


def connection(path):
    safe_path(path, kb.kanban_home())
    from hermes_cli.agent_platform import evidence_sqlite

    return evidence_sqlite.connect(path)


def run_context(p, run_id, *, latest=True):
    conn = connection(kb.kanban_db_path(board=p["kanban_board_slug"]))
    try:
        task = kb.get_task(conn, p["kanban_task_id"])
        runs = kb.list_runs(conn, p["kanban_task_id"])
        run = next((r for r in runs if r.id == run_id), None)
    finally:
        conn.close()
    if task is None or run is None or (latest and runs[-1].id != run.id):
        raise ValueError("run does not match current task authority")
    if run.ended_at is None or run.profile != p["assignee_profile"]:
        raise ValueError("terminal run/profile authority required")
    metadata = run.metadata or {}
    if any(
        k in metadata and metadata[k] != p[k]
        for k in (
            "ticket_id",
            "ticket_spec_SHA256",
            "work_packet_id",
            "work_packet_SHA256",
            "projection_SHA256",
        )
    ):
        raise ValueError("terminal run immutable authority mismatch")
    workspace = Path(task.workspace_path or "")
    root = kb.kanban_home() / "kanban/workspaces"
    safe_path(workspace, root, missing=True)
    body = json.loads(task.body or "{}")
    if body.get("retry_workspace_allocation") is not None:
        from .retry_workspace import verify

        with connection(kb.kanban_db_path(board=p["kanban_board_slug"])) as conn:
            verify(conn, task)
    if workspace.name != task.id or body.get("fresh_execution_attempt_number") is not None:
        attempt = body.get("fresh_execution_attempt_number")
        if (
            type(attempt) is not int
            or attempt != len(runs)
            or attempt < 2
            or workspace.name != f"{task.id}-attempt-{attempt}"
            or body.get("fresh_execution_workspace_path") != str(workspace)
            or not body.get("fresh_execution_request_SHA256")
        ):
            from .retry_workspace import historical

            historical(p, task, run, runs, workspace)
    if any(
        body.get(k) != p[v]
        for k, v in (
            ("TicketSpec_SHA256", "ticket_spec_SHA256"),
            ("WorkPacket_ID", "work_packet_id"),
            ("WorkPacket_SHA256", "work_packet_SHA256"),
        )
    ):
        raise ValueError("task immutable authority mismatch")
    return task, run, workspace


def _walk_error(error):
    raise ValueError("evidence tree unreadable") from error


def source(p, run):
    path = pr.governed_source_authority_record_path_for_run(p, run.id)
    record = read_json(path, kb.kanban_home() / "agent-platform/source-authority", maximum=32_000_000)
    if not isinstance(record, dict) or not {"snapshot_root", "snapshot_manifest_path", "snapshot_file_count", "snapshot_total_bytes"} <= record.keys():
        raise ValueError("source authority record identity incomplete")
    if (
        record.get("snapshot_file_count", 0) > 100000
        or record.get("snapshot_total_bytes", 0) > 2_000_000_000
    ):
        raise ValueError("source snapshot exceeds bounded inspection limits")
    root = safe_path(record["snapshot_root"], path.parent)
    manifest_path = safe_path(record["snapshot_manifest_path"], path.parent)
    if manifest_path.stat().st_size > 32_000_000:
        raise ValueError("source snapshot manifest exceeds inspection bound")
    # Reject redirects before the existing validator reads any file in the tree.
    for parent, dirs, files in os.walk(root, followlinks=False, onerror=_walk_error):
        for name in dirs + files:
            if (Path(parent) / name).is_symlink():
                raise ValueError("source snapshot contains symlink")
    pr._validate_governed_source_authority_record(record, projection=p, run_id=run.id)
    return record


def _scope(path, manifest):
    return (
        pr._review_candidate_path_in_workpacket_scope(
            path, tuple(manifest["writable_allowed_paths"])
        )
        and not any(
            fnmatch.fnmatchcase(path, pattern)
            for pattern in manifest.get("forbidden_paths", [])
        )
        and not pr._governed_autonomy_candidate_diff_excluded(
            path, excluded_roots=tuple(manifest.get("product_diff_excluded_roots", []))
        )
    )


def candidate(p, run, workspace, baseline, *, own_source=None, offset=0):
    manifest = (own_source or baseline)["materialization_manifest"]
    src = {
        f["relative_path"]: f["SHA256"]
        for f in baseline["snapshot_manifest"]["files"]
        if _scope(f["relative_path"], manifest)
    }
    base = {
        "source_authority_SHA256": baseline["governed_source_authority_SHA256"],
        "source_snapshot_SHA256": baseline["snapshot_SHA256"],
        "source_file_count": len(src),
        "candidate_root": str(workspace),
        "candidate_manifest_kind": "observed governed file hashes; not a persisted terminal candidate manifest",
        "source_snapshot_root": baseline["snapshot_root"],
        "source_snapshot_manifest_SHA256": baseline["snapshot_manifest_SHA256"],
        "candidate_exists": workspace.exists(),
        "scope": manifest["writable_allowed_paths"],
        "candidate_file_count": None,
        "source_candidate_equal": None,
        "zero_change_status": "UNAVAILABLE",
        "human_attestation_required": True,
    }
    if not workspace.is_dir():
        if own_source is None:
            from .terminal_candidate_evidence import load

            retained = load(p, run, baseline, workspace, offset)
            if retained is not None:
                return retained
        return {
            **base,
            **unavailable(
                "canonical candidate workspace absent; absence is not equality"
            ),
        }
    actual = read_json(
        workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST, workspace
    )
    pr._validate_review_candidate_manifest_identity(
        actual,
        projection=p,
        workspace_root=workspace,
        manifest_path=workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST,
    )
    if any(
        actual.get(k) != manifest.get(k)
        for k in (
            "writable_allowed_paths",
            "forbidden_paths",
            "product_diff_excluded_roots",
        )
    ):
        raise ValueError("candidate source materialization scope mismatch")
    expected_source = own_source or baseline
    reference = actual.get("durable_source_authority_reference", {})
    if actual.get("durable_source_authority_SHA256") != expected_source[
        "governed_source_authority_SHA256"
    ] or any(
        reference.get(k) != v
        for k, v in pr._governed_source_authority_reference(expected_source).items()
    ):
        raise ValueError("candidate durable source authority mismatch")
    files = {}
    for parent, dirs, names in os.walk(
        workspace, followlinks=False, onerror=_walk_error
    ):
        for name in dirs + names:
            child = Path(parent) / name
            if child.is_symlink():
                raise ValueError("candidate symlink evidence is unavailable")
        for name in names:
            path = Path(parent) / name
            rel = path.relative_to(workspace).as_posix()
            if _scope(rel, manifest):
                safe_path(path, workspace)
                files[rel] = pr._sha256_file_or_none(path)
                if files[rel] is None or len(files) > 10000:
                    raise ValueError(
                        "candidate file evidence unavailable or exceeds bound"
                    )
    entries = [
        {
            "path": rel,
            "source_SHA256": src.get(rel),
            "candidate_SHA256": files.get(rel),
            "change": "equal"
            if src.get(rel) == files.get(rel)
            else "added"
            if rel not in src
            else "deleted"
            if rel not in files
            else "modified",
        }
        for rel in sorted(src.keys() | files.keys())
    ]
    changes = [x for x in entries if x["change"] != "equal"]
    return {
        **base,
        "available": True,
        "candidate_file_count": len(files),
        "candidate_manifest_SHA256": digest(files),
        "source_manifest_SHA256": digest(src),
        "diff_SHA256": digest(entries),
        "changed_path_count": len(changes),
        "added_files": sum(x["change"] == "added" for x in changes),
        "modified_files": sum(x["change"] == "modified" for x in changes),
        "deleted_files": sum(x["change"] == "deleted" for x in changes),
        "source_candidate_equal": not changes,
        "zero_change_status": "CONTRADICTED" if changes else "PROVEN",
        "derivation": "exact SHA256 equality of all governed paths against validated durable source snapshot; current file observation",
        "files": entries[offset : offset + LIMIT],
        "changed_paths": changes[offset : offset + LIMIT],
        "file_offset": offset,
        "file_total": len(entries),
        "next_offset": offset + LIMIT if offset + LIMIT < len(entries) else None,
    }


def _json(value):
    return json.loads(value) if isinstance(value, str) else value


def _current_task_witness(p, run, workspace, args, payload, invocation, result):
    """Accept only explicit-task or canonical worker-local empty arguments.

    Both forms require the same independent result authority. The wider transcript
    window preserves final conclusions, but cannot supply a post-terminal witness.
    """
    if args not in ({}, {"task_id": p["kanban_task_id"]}):
        return False
    if (
        not run.started_at
        <= invocation["timestamp"]
        <= result["timestamp"]
        <= run.ended_at + 1
    ):
        return False
    task = payload.get("task")
    if not isinstance(task, dict):
        return False
    try:
        body = _json(task.get("body", "{}"))
    except (ValueError, TypeError):
        return False
    return (
        isinstance(body, dict)
        and task.get("id") == p["kanban_task_id"]
        and type(task.get("current_run_id")) is int
        and task["current_run_id"] == run.id
        and task.get("workspace_path") == str(workspace)
        and all(
            body.get(k) == p[v]
            for k, v in (
                ("TicketSpec_SHA256", "ticket_spec_SHA256"),
                ("WorkPacket_ID", "work_packet_id"),
                ("WorkPacket_SHA256", "work_packet_SHA256"),
            )
        )
    )


def worker(p, task, run, workspace, *, offset=0):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", run.profile):
        raise ValueError("invalid worker profile")
    found = []
    direct = (run.metadata or {}).get("worker_session_id")
    for db in (
        kb.kanban_home() / "state.db",
        kb.kanban_home() / "profiles" / run.profile / "state.db",
    ):
        if not db.exists():
            continue
        conn = connection(db)
        try:
            sessions = conn.execute(
                "SELECT id,cwd,profile_name,started_at,ended_at,model,source,billing_provider FROM sessions WHERE cwd=? AND profile_name=? AND started_at>=? AND started_at<=?",
                (str(workspace), run.profile, run.started_at, run.ended_at + 1),
            ).fetchall()
            for session in sessions:
                size = conn.execute(
                    "SELECT coalesce(sum(length(content)+coalesce(length(tool_calls),0)),0) FROM messages WHERE session_id=? AND active=1",
                    (session["id"],),
                ).fetchone()[0]
                if size > 8_000_000:
                    raise ValueError("worker transcript byte bound exceeded")
                rows = [
                    dict(r)
                    for r in conn.execute(
                        "SELECT id,role,content,tool_calls,tool_call_id,tool_name,timestamp FROM messages WHERE session_id=? AND active=1 ORDER BY id LIMIT ?",
                        (session["id"], MAX_MESSAGES + 1),
                    )
                ]
                if len(rows) > MAX_MESSAGES:
                    raise ValueError("worker transcript exceeds inspection bound")
                calls, paired, witness, paired_ids = {}, [], None, set()
                for row in rows:
                    if (
                        row["timestamp"] < run.started_at
                        or row["timestamp"] > run.ended_at + 30
                    ):
                        continue
                    if row["role"] == "assistant":
                        for call in _json(row["tool_calls"] or "[]"):
                            fn = call["function"]
                            if call["id"] in calls:
                                raise ValueError("ambiguous duplicate tool invocation")
                            calls[call["id"]] = (
                                fn["name"],
                                _json(fn.get("arguments", "{}")),
                                row,
                            )
                    elif row["role"] == "tool" and row["tool_call_id"] in calls:
                        name, args, invocation = calls[row["tool_call_id"]]
                        if (
                            name != row["tool_name"]
                            or row["tool_call_id"] in paired_ids
                        ):
                            raise ValueError("tool invocation/result mismatch")
                        paired_ids.add(row["tool_call_id"])
                        try:
                            payload = _json(row["content"])
                        except (ValueError, TypeError):
                            payload = None
                        if name == "kanban_show" and isinstance(payload, dict):
                            if _current_task_witness(
                                p, run, workspace, args, payload, invocation, row
                            ):
                                witness = row
                        paired.append((name, args, invocation, row, payload))
                if witness is not None:
                    found.append((db, dict(session), rows, paired, witness, calls))
        finally:
            conn.close()
    if len(found) != 1 or (direct and found[0][1]["id"] != direct):
        raise ValueError("worker session binding unavailable or ambiguous")
    db, session, rows, paired, witness, calls = found[0]
    public = []
    for name, args, invocation, result, payload in paired:
        category = (
            "validation"
            if name == "workpacket_validation"
            else "mutation"
            if re.search(r"write|patch|edit|apply", name)
            else "search"
            if re.search(r"search|list.*tree", name)
            else "read"
            if re.search(r"read|repository_context|repository_authority", name)
            else "other"
        )
        public.append({
            "tool": name,
            "category": category,
            "argument_SHA256": digest(args),
            "target": str(
                args.get("path") or args.get("file_path") or args.get("query") or ""
            )[:300],
            "invocation_message_id": invocation["id"],
            "invocation_SHA256": digest(invocation),
            "result_message_id": result["id"],
            "result_SHA256": digest(result),
            "success": payload.get("success") if isinstance(payload, dict) else None,
            "denied": bool(
                isinstance(payload, dict)
                and any(
                    "denied" in str(payload.get(k, "")).lower()
                    for k in ("error", "code", "blocker_code")
                )
            ),
            "after_terminal_timestamp": result["timestamp"] > run.ended_at + 1,
        })
    summaries = [
        r
        for r in rows
        if r["role"] == "assistant"
        and r["content"]
        and run.started_at <= r["timestamp"] <= run.ended_at + 30
    ]
    final = summaries[-1] if summaries else None
    result = {
        "available": True,
        "session": session,
        "database": str(db),
        "session_SHA256": digest(session),
        "task_witness_message_id": witness["id"],
        "task_witness_SHA256": digest(witness),
        "direct_run_session_link": bool(direct),
        "transcript_SHA256": digest(rows),
        "message_count": len(rows),
        "final_conclusion": None
        if final is None
        else {
            "text": final["content"][:4000],
            "message_id": final["id"],
            "message_SHA256": digest(final),
            "truncated": len(final["content"]) > 4000,
            "post_terminal": final["timestamp"] > run.ended_at + 1,
        },
        "terminal_summary": (run.summary or "")[:4000],
        "terminal_run_SHA256": digest(pr._run_dict(run)),
        "mutation_call_count": sum(x["category"] == "mutation" for x in public),
        "denied_mutations": sum(
            x["category"] == "mutation" and x["denied"] for x in public
        ),
        "calls": public[offset : offset + LIMIT],
        "call_total": len(public),
        "next_offset": offset + LIMIT if offset + LIMIT < len(public) else None,
        "limitation": "No mutation calls is transcript evidence, not filesystem equality. Closing summary may follow the integer terminal timestamp by up to 30 seconds; it never supplies validation authority.",
    }
    result["provider"] = session.get("billing_provider")
    result["provider_unavailable_reason"] = (
        "billing_provider not persisted" if not result["provider"] else None
    )
    result["assistant_observations"] = [
        {
            "message_id": r["id"],
            "message_SHA256": digest(r),
            "text": r["content"][:1000],
            "truncated": len(r["content"]) > 1000,
        }
        for r in summaries[offset : offset + 5]
    ]
    result["assistant_observation_total"] = len(summaries)
    result["assistant_next_offset"] = (
        offset + 5 if offset + 5 < len(summaries) else None
    )
    paired_ids = {item[3]["tool_call_id"] for item in paired}
    unresolved = [
        {
            "tool": name,
            "invocation_message_id": row["id"],
            "invocation_SHA256": digest(row),
            "result_available": False,
        }
        for call_id, (name, args, row) in calls.items()
        if call_id not in paired_ids
    ]
    result["unresolved_calls"] = unresolved[offset : offset + LIMIT]
    result["unresolved_call_total"] = len(unresolved)
    result["unresolved_next_offset"] = (
        offset + LIMIT if offset + LIMIT < len(unresolved) else None
    )
    result["mutation_call_count"] += sum(
        bool(re.search(r"write|patch|edit|apply", x["tool"])) for x in unresolved
    )
    result["implementation_plan_record"] = unavailable(
        "no dedicated persisted plan record; bounded assistant observations carry any recorded planning text"
    )
    return result, paired


def vitest_summary(stdout, stderr):
    if any(
        x.truncated or x.redaction_count or x.decode_replacement_count
        for x in (stdout, stderr)
    ):
        return unavailable("complete unredacted streams required for exact test counts")
    text = re.sub(r"\x1b\[[0-9;]*m", "", stdout.retained_text or "")
    if not re.search(r"(?m)^\s*RUN\s+v\d+\.\d+", text):
        return unavailable("no canonical Vitest summary")
    counts = {}
    for label in ("Test Files", "Tests"):
        lines = re.findall(r"(?m)^\s*" + label + r"\s+(.+?)\s*$", text)
        if len(lines) != 1:
            return unavailable("missing or ambiguous test summary")
        match = re.fullmatch(
            r"((?:\d+ (?:passed|failed|skipped|todo)(?:\s*\|\s*)?)+)\s+\((\d+)\)",
            lines[0],
        )
        if not match:
            return unavailable("unsupported summary format")
        pairs = re.findall(r"(\d+) (passed|failed|skipped|todo)", match[1])
        if len({k for _, k in pairs}) != len(pairs) or sum(
            int(n) for n, _ in pairs
        ) != int(match[2]):
            return unavailable("inconsistent summary totals")
        counts[label] = {k: int(n) for n, k in pairs} | {"total": int(match[2])}
    f, t = counts["Test Files"], counts["Tests"]
    return {
        "available": True,
        "test_files_discovered": f["total"],
        "test_files_passed": f.get("passed", 0),
        "test_files_failed": f.get("failed", 0),
        "tests_total": t["total"],
        "tests_passed": t.get("passed", 0),
        "tests_failed": t.get("failed", 0),
        "tests_skipped": t.get("skipped", 0),
        "tests_todo": t.get("todo", 0),
        "test_collection_started": True,
        "tests_executed": t.get("passed", 0) + t.get("failed", 0) > 0,
        "basis_stdout_SHA256": stdout.stream_SHA256,
    }


def validation(p, run, workspace, source_record, paired, packet, *, offset=0):
    from tools import governed_workpacket_file_guard as guard
    from tools import workpacket_validation_tool as vt
    from hermes_cli.agent_platform.work_packet.validation_command_runner import (
        ValidationCommandCapturedStream,
    )
    from hermes_cli.agent_platform import validation_contract_failure as failure

    root = Path(source_record["snapshot_root"])
    file_authority = guard.WorkPacketFileAuthority(
        ticket_id=p["ticket_id"],
        ticket_spec_SHA256=p["ticket_spec_SHA256"],
        work_packet_id=p["work_packet_id"],
        work_packet_SHA256=p["work_packet_SHA256"],
        projection_SHA256=p["projection_SHA256"],
        allowed_paths=tuple(packet.repository_scope.allowed_paths),
        forbidden_paths=tuple(packet.repository_scope.forbidden_paths),
        workspace_root=root,
        resolved_workspace_root=root,
    )
    specs = {
        s.command_id: s
        for s in vt.build_governed_validation_command_specs(file_authority, packet)
        if s.acceptance_authorized
    }
    discovered = {}
    results = []
    excluded = []

    def remap(value):
        if isinstance(value, str):
            return value.replace(str(root), str(workspace))
        if isinstance(value, list):
            return [remap(x) for x in value]
        if isinstance(value, dict):
            return {k: remap(v) for k, v in value.items()}
        return value

    for name, args, invocation, row, result in paired:
        if name != "workpacket_validation":
            continue
        if (
            row["timestamp"] > run.ended_at + 1
            or invocation["timestamp"] > run.ended_at + 1
        ):
            # The transcript includes a short tail for worker conclusions. Tail
            # calls cannot establish this run's validation, nor erase a valid
            # in-run result. Retain their identities as explicit exclusions.
            excluded.append({
                "invocation_message_id": invocation["id"],
                "result_message_id": row["id"],
                "invocation_timestamp": invocation["timestamp"],
                "result_timestamp": row["timestamp"],
                "invocation_SHA256": digest(invocation),
                "result_SHA256": digest(row),
                "reason": "outside terminal run interval; not validation authority",
            })
            continue
        if not isinstance(result, dict) or any(
            result.get(k) != p[k]
            for k in ("ticket_id", "work_packet_id", "work_packet_SHA256")
        ):
            raise ValueError("validation result authority mismatch")
        if args.get("action") == "list" and result.get("success") is True:
            discovered.update({c["command_id"]: c for c in result.get("commands", [])})
            continue
        if args.get("action") != "run":
            continue
        if not vt._validation_result_digest_valid_for_matching(result):
            raise ValueError("persisted validation result digest mismatch")
        spec = specs.get(args.get("command_id"))
        command = result.get("command")
        if spec is None or command != discovered.get(args.get("command_id")):
            raise ValueError("validation discovery/invocation mismatch")
        expected = remap(vt._public_command(spec))
        ignore = {
            "runtime_available",
            "runtime_unavailable_reason",
            "execution_plan_SHA256",
        }
        if (
            set(command) != set(expected)
            or any(command[k] != v for k, v in expected.items() if k not in ignore)
            or command.get("runtime_available") is not True
        ):
            raise ValueError("governed command authority mismatch")
        children = result.get("subcommand_results", [])
        plans = remap([vt._public_plan_step(x) for x in vt._command_plan(spec)])
        if (
            len(children) != 1
            or len(plans) != 1
            or result.get("subcommand_count") != 1
            or result.get("completed_subcommand_count") != 1
        ):
            raise ValueError(
                "only one complete bounded validation invocation is inspectable"
            )
        child = children[0]
        actual = child.get("subcommand", {})
        argv = actual.get("effective_argv", [])
        if (
            not argv
            or not Path(argv[0]).is_absolute()
            or Path(argv[0]).name != Path(plans[0]["effective_argv"][0]).name
        ):
            raise ValueError("validation runtime identity mismatch")
        plans[0]["effective_argv"][0] = argv[0]
        plan_sha = vt._digest_payload(
            vt._WORKPACKET_VALIDATION_EXECUTION_PLAN_DIGEST_ALGORITHM,
            {
                "command_id": command["command_id"],
                "validation_id": command["validation_id"],
                "source_command": command["source_command"],
                "working_directory": command["working_directory"],
                "expected_exit_codes": command["expected_exit_codes"],
                "execution_plan": plans,
            },
        )
        if (
            actual != plans[0]
            or command["execution_plan_SHA256"] != plan_sha
            or result.get("execution_plan_SHA256") != plan_sha
            or child.get("command") != command
        ):
            raise ValueError("validation execution plan mismatch")
        for item in (result, child):
            if item.get("policy_id") != vt.GOVERNED_VALIDATION_POLICY_ID or any(
                item.get(k) != p[k]
                for k in ("ticket_id", "work_packet_id", "work_packet_SHA256")
            ):
                raise ValueError("validation policy/identity mismatch")
        if any(
            child.get(k) != result.get(k)
            for k in (
                "exit_code",
                "process_started",
                "success",
                "disposition",
                "failure_reason",
            )
        ):
            raise ValueError("validation outcome mismatch")
        stdout = ValidationCommandCapturedStream.model_validate(child.get("stdout"))
        stderr = ValidationCommandCapturedStream.model_validate(child.get("stderr"))
        parsed = vitest_summary(stdout, stderr)
        passed = (
            child.get("process_started") is True
            and child.get("success") is True
            and child.get("exit_code") in command["expected_exit_codes"]
            and child.get("disposition") == "passed"
            and result.get("all_subcommands_passed") is True
        )
        pretest = failure._unsupported_option(child, actual, command)
        outcome = (
            "TESTS_PASSED"
            if passed
            and parsed.get("tests_executed")
            and parsed.get("tests_failed") == 0
            else "TESTS_FAILED"
            if parsed.get("tests_executed")
            and parsed.get("tests_failed", 0) > 0
            and not passed
            else "PRE_TEST_COMMAND_FAILURE"
            if pretest
            else "UNDETERMINED"
        )
        streams = {}
        for key, stream in (("stdout", stdout), ("stderr", stderr)):
            data = stream.model_dump(mode="json")
            text = data.get("retained_text") or ""
            data["retained_text"] = text[:8192]
            data["display_truncated"] = len(text) > 8192
            streams[key] = data
        results.append({
            "command": command,
            "discovered_command": discovered[command["command_id"]],
            "authority_match": True,
            "execution_plan": actual,
            "execution_plan_SHA256": plan_sha,
            "process_started": child.get("process_started"),
            "success": child.get("success"),
            "exit_code": child.get("exit_code"),
            "expected_exit_codes": command["expected_exit_codes"],
            "disposition": child.get("disposition"),
            "failure_reason": child.get("failure_reason"),
            "timed_out": child.get(
                "timed_out", child.get("failure_reason") == "timeout"
            ),
            "started_at": child.get("started_at"),
            "ended_at": child.get("ended_at"),
            "duration": child.get("duration_seconds"),
            "invocation_timestamp": invocation["timestamp"],
            "result_timestamp": row["timestamp"],
            "validation_result_SHA256": digest(result),
            "source_message_id": row["id"],
            "source_message_SHA256": digest(row),
            "invocation_message_id": invocation["id"],
            "invocation_message_SHA256": digest(invocation),
            "outcome": outcome,
            "test_evidence": parsed,
            **streams,
        })
    if not results:
        return {
            **unavailable("no persisted governed validation run invocation"),
            "excluded_post_terminal_count": len(excluded),
            "excluded_post_terminal_calls": excluded[:LIMIT],
        }
    if len(results) > 5:
        raise ValueError("validation results exceed inspection bound")
    return {
        "available": True,
        "excluded_post_terminal_count": len(excluded),
        "excluded_post_terminal_calls": excluded[:LIMIT],
        "excluded_post_terminal_truncated": len(excluded) > LIMIT,
        "results": results[offset : offset + 1],
        "result_total": len(results),
        "source_authority_SHA256": source_record["governed_source_authority_SHA256"],
        "next_offset": offset + 1 if offset + 1 < len(results) else None,
        "validation_execution_performed": False,
    }


def review_validation_records(completion):
    """Derive review records from current persisted evidence, without enriching completion.

    Completion identity must stay byte-equivalent for existing human attestations.
    The review digest covers the compact transport; provenance retains the distinct
    original tool-result digest and invocation/session/run identities.
    """
    from tools import workpacket_validation_tool as vt

    if not isinstance(completion, Mapping):
        return ()
    if not completion.get("durable_source_authority_SHA256") or not completion.get(
        "kanban_completion_result_SHA256"
    ):
        return ()
    try:
        p = pr._load_current_projection_record()
        canonical = pr._kanban_completion_result_source(p, read_only=True)
        if canonical.get("blocker_code") or completion != canonical:
            return ()
        evidence = inspect(
            project_id=p["project_id"],
            ticket_id=p["ticket_id"],
            run_id=canonical["run_id"],
            section="validation",
        )
        validation_evidence = evidence["validation"]
        worker_evidence = evidence["worker"]
        # C68 validates at most five invocations, but a single result is the
        # only unambiguous transport. Never select a passing page among retries.
        if (
            not worker_evidence.get("available")
            or not validation_evidence.get("available")
            or validation_evidence.get("result_total") != 1
            or validation_evidence.get("source_authority_SHA256")
            != canonical["durable_source_authority_SHA256"]
            or evidence["binding"] != {k: p[k] for k in evidence["binding"]}
            or evidence["workspace"] != canonical["kanban_task_workspace_path"]
        ):
            return ()
        result = validation_evidence["results"][0]
        if result["outcome"] not in {
            "TESTS_PASSED",
            "TESTS_FAILED",
            "PRE_TEST_COMMAND_FAILURE",
        }:
            return ()
        if result["success"] is True and (
            result["outcome"] != "TESTS_PASSED"
            or result["timed_out"] is not False
            or result["failure_reason"] != "none"
        ):
            return ()
        record = {
            "review_prepare_validation_evidence_mode": "canonical_worker_evidence",
            **{k: p[k] for k in ("ticket_id", "work_packet_id", "work_packet_SHA256")},
            **{
                k: result[k]
                for k in (
                    "command",
                    "success",
                    "process_started",
                    "exit_code",
                    "expected_exit_codes",
                    "disposition",
                    "failure_reason",
                    "timed_out",
                    "outcome",
                    "execution_plan_SHA256",
                )
            },
            "provenance": {
                **evidence["binding"],
                "run_id": canonical["run_id"],
                "workspace": evidence["workspace"],
                "kanban_completion_result_SHA256": canonical[
                    "kanban_completion_result_SHA256"
                ],
                "durable_source_authority_SHA256": canonical[
                    "durable_source_authority_SHA256"
                ],
                "worker_session_id": worker_evidence["session"]["id"],
                **{
                    k: worker_evidence[k]
                    for k in (
                        "session_SHA256",
                        "task_witness_message_id",
                        "task_witness_SHA256",
                        "terminal_run_SHA256",
                        "transcript_SHA256",
                    )
                },
                **{
                    k: result[k]
                    for k in (
                        "invocation_message_id",
                        "invocation_message_SHA256",
                        "source_message_id",
                        "source_message_SHA256",
                        "invocation_timestamp",
                        "result_timestamp",
                        "validation_result_SHA256",
                    )
                },
                "execution_evidence_SHA256": evidence["evidence_SHA256"],
            },
        }
        record["validation_result_SHA256"] = vt._validation_result_payload_digest(
            record
        )
        # Fail closed if authority changed while reading the separate stores.
        if (
            p != pr._load_current_projection_record()
            or canonical != pr._kanban_completion_result_source(p, read_only=True)
        ):
            return ()
        return (record,)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, RuntimeError):
        return ()


def inspect(
    *, ticket_id, run_id, section="summary", offset=0, historical=None, project_id=None
):
    """Inspect current terminal authority; historical inputs are guards, never paths to open."""
    if (
        section
        not in {"summary", "worker", "candidate", "validation", "historical_candidate"}
        or type(offset) is not int
        or not 0 <= offset <= 10000
        or type(run_id) is not int
    ):
        raise ValueError("invalid bounded evidence request")
    from .retry_workspace import freshness

    p = pr._load_current_projection_record()
    if ticket_id != p["ticket_id"] or project_id not in (None, p["project_id"]):
        raise ValueError("current ticket authority mismatch")
    task, run, workspace = run_context(p, run_id)
    from hermes_cli.agent_platform.work_packet import WorkPacketCompilationResult

    generation = bridge.load_immutable_approved_current_ticket_authority(
        ticket_id=ticket_id, require_approved_decision=True
    )["generation_record"]
    if any(
        generation[k] != p[k]
        for k in ("ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256")
    ):
        raise ValueError("current generation changed during inspection")
    packet = WorkPacketCompilationResult.model_validate(
        generation["work_packet_compilation_result"]
    ).work_packet
    result = {
        "success": True,
        "read_only": True,
        "workflow_mutation": False,
        "human_attestation_performed": False,
        "manual_validation_satisfied": False,
        "execution_started": False,
        "Git_mutation": False,
        "binding": {
            k: p[k]
            for k in (
                "project_id",
                "ticket_id",
                "ticket_spec_SHA256",
                "work_packet_id",
                "work_packet_SHA256",
                "projection_SHA256",
                "kanban_task_id",
                "assignee_profile",
            )
        },
        "run_id": run.id,
        "run_status": run.status,
        "outcome": run.outcome,
        "workspace": str(workspace),
        **freshness(task),
        "section": section,
    }

    def bounded(fn):
        try:
            return fn()
        except (
            OSError,
            ValueError,
            KeyError,
            TypeError,
            sqlite3.Error,
            RuntimeError,
        ) as exc:
            return unavailable(str(exc)[:300])

    src = bounded(lambda: source(p, run))
    paired = []
    if section in {"summary", "worker", "validation"}:
        pair = bounded(lambda: worker(p, task, run, workspace, offset=offset))
        if isinstance(pair, tuple):
            result["worker"], paired = pair
        else:
            result["worker"] = pair
    if section in {"summary", "candidate"}:
        result["candidate"] = (
            bounded(lambda: candidate(p, run, workspace, src, offset=offset))
            if "snapshot_root" in src
            else {**src, "zero_change_status": "UNAVAILABLE"}
        )
    if section in {"summary", "validation"}:
        result["validation"] = (
            bounded(
                lambda: validation(
                    p, run, workspace, src, paired, packet, offset=offset
                )
            )
            if "snapshot_root" in src and paired
            else unavailable("bound worker or source evidence unavailable")
        )
    if section == "historical_candidate":
        if (
            not isinstance(historical, dict)
            or set(historical)
            != {
                "ticket_id",
                "work_packet_SHA256",
                "projection_SHA256",
                "task_id",
                "run_id",
                "workspace",
            }
            or historical["ticket_id"] != ticket_id
            or historical["run_id"] == run.id
        ):
            raise ValueError("complete distinct historical identity required")
        hp = read_json(
            projection._historical_projection_path(historical),
            projection.kanban_projection_record_path_for_ticket(ticket_id).parent,
        )
        if (
            not projection._projection_is_superseded(hp, generation)
            or hp["projection_SHA256"] != historical["projection_SHA256"]
            or hp["kanban_task_id"] != historical["task_id"]
        ):
            raise ValueError("historical projection authority mismatch")
        _ht, hr, hw = run_context(hp, historical["run_id"], latest=False)
        if str(hw) != historical["workspace"]:
            raise ValueError("historical workspace guard mismatch")
        own = bounded(lambda: source(hp, hr))
        result["historical_binding"] = {
            **historical,
            "ticket_spec_SHA256": hp["ticket_spec_SHA256"],
            "work_packet_id": hp["work_packet_id"],
        }
        result["historical_candidate"] = (
            bounded(lambda: candidate(hp, hr, hw, src, own_source=own, offset=offset))
            if "snapshot_root" in src and "snapshot_root" in own
            else unavailable("validated source manifest unavailable")
        )
    result["evidence_SHA256"] = digest(result)
    return result
