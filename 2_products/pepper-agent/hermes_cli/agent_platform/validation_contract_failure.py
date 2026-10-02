"""Read-only, run-bound evidence of an incompatible governed CLI invocation.

A terminal summary alone is never authority. Require the persisted discovery,
invocation and result from the worker session, plus a task/run identity witness.
"""

import hashlib
import json
from pathlib import Path
import re
import sqlite3

REASON = "governed_validation_command_incompatible"


def _sha(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _json(value):
    return json.loads(value) if isinstance(value, str) else value


def _no_tests_started(value):
    return not any(
        value.get(key) is not None and value.get(key) is not False
        for key in (
            "test_execution_started",
            "tests_executed",
            "validation_passed",
            "execution_validation_passed",
            "ad_hoc_command_substitution",
        )
    )


def _unsupported_option(result, expected_plan, command):
    """Recognize only a captured CLI-parser rejection, not arbitrary stderr."""
    from hermes_cli.agent_platform.work_packet.validation_command_runner import (
        ValidationCommandCapturedStream,
    )

    if not _no_tests_started(result) or result.get("success") is not False:
        return None
    if (
        result.get("process_started") is not True
        or result.get("failure_reason") != "nonzero_exit"
    ):
        return None
    if (
        result.get("terminate_requested") is not False
        or result.get("kill_requested") is not False
    ):
        return None
    if (
        type(result.get("exit_code")) is not int
        or result["exit_code"] in command["expected_exit_codes"]
    ):
        return None
    stdout = ValidationCommandCapturedStream.model_validate(result.get("stdout"))
    stderr = ValidationCommandCapturedStream.model_validate(result.get("stderr"))
    if stdout.raw_byte_count or any((
        stderr.truncated,
        stderr.redaction_count,
        stderr.decode_replacement_count,
    )):
        return None
    detail = stderr.retained_text or ""
    match = re.search(
        r"(?mi)^[\w.$]*Error: (?:unknown|unsupported|unrecognized) option [`'\"](--?[\w-]+)[`'\"]\s*$",
        detail,
    )
    if match is None or match[1] not in command["command_argv"]:
        return None
    argv = expected_plan.get("effective_argv", [])
    entry = expected_plan.get("cli_entry")
    if len(argv) < 2 or not entry or len(Path(entry).parts) < 2:
        return None
    # The observed parser stack must belong to the exact authorized CLI package.
    package_depth = len(Path(entry).parts) - (3 if entry.startswith("@") else 2)
    if package_depth < 0:
        return None
    package = Path(argv[1]).resolve().parents[package_depth]
    frames = re.findall(r"(?m)^\s+at ([\w.$]+) \(file://([^\n()]+):\d+:\d+\)$", detail)
    if not frames or frames[0][0].split(".")[-1] not in {
        "checkUnknownOptions",
        "parseArgs",
        "parseOptions",
        "parse",
    }:
        return None
    file_paths = re.findall(r"file://([^\s()]+?):\d+(?::\d+)?", detail)
    if not file_paths or any(
        not Path(path).resolve().is_relative_to(package) for path in file_paths
    ):
        return None
    return {
        "failure_classification": "unsupported_cli_option",
        "unsupported_option": match[1],
        "failure_detail": detail[:2048],
        "test_execution_started": False,
        "test_execution_stage_basis": "captured_cli_parser_rejection_before_command_action",
        "stdout_SHA256": stdout.stream_SHA256,
        "stderr_SHA256": stderr.stream_SHA256,
    }


def _declaration_matches(command, spec):
    from tools import workpacket_validation_tool as validation

    expected = validation._public_command(spec)
    # Node resolution belongs to the historical worker, not the reader's PATH.
    runtime_fields = {
        "runtime_available",
        "runtime_unavailable_reason",
        "execution_plan_SHA256",
    }
    return (
        isinstance(command, dict)
        and set(command) == set(expected)
        and all(
            command[key] == value
            for key, value in expected.items()
            if key not in runtime_fields
        )
        and command.get("runtime_available") is True
        and command.get("runtime_unavailable_reason") is None
    )


def _matching_result(result, spec, projection, discovered):
    from tools import workpacket_validation_tool as validation

    command = result.get("command")
    if command != discovered or not _declaration_matches(command, spec):
        return None
    plans = [
        validation._public_plan_step(step) for step in validation._command_plan(spec)
    ]
    # Keep this evidence rule bounded to a single unambiguous governed invocation.
    if len(plans) != 1:
        return None
    if result.get("policy_id") != validation.GOVERNED_VALIDATION_POLICY_ID:
        return None
    if any(
        result.get(key) != projection[key]
        for key in ("ticket_id", "work_packet_id", "work_packet_SHA256")
    ):
        return None
    if (
        not _no_tests_started(result)
        or result.get("success") is not False
        or result.get("process_started") is not True
        or result.get("disposition") != "failed"
        or result.get("failure_reason") != "nonzero_exit"
        or result.get("execution_plan_SHA256") != command["execution_plan_SHA256"]
        or result.get("subcommand_count") != 1
        or result.get("completed_subcommand_count") != 1
        or result.get("all_subcommands_passed") is not False
    ):
        return None
    children = result.get("subcommand_results")
    if not isinstance(children, list) or len(children) != 1:
        return None
    child = children[0]
    observed_plan = child.get("subcommand", {})
    observed_argv = observed_plan.get("effective_argv", [])
    template_argv = plans[0]["effective_argv"]
    if (
        not observed_argv
        or not template_argv
        or not Path(observed_argv[0]).is_absolute()
        or not Path(observed_argv[0]).is_file()
        or Path(observed_argv[0]).name != Path(template_argv[0]).name
    ):
        return None
    plans[0]["effective_argv"] = [observed_argv[0], *template_argv[1:]]
    expected_digest = validation._digest_payload(
        validation._WORKPACKET_VALIDATION_EXECUTION_PLAN_DIGEST_ALGORITHM,
        {
            "command_id": command["command_id"],
            "validation_id": command["validation_id"],
            "source_command": command["source_command"],
            "working_directory": command["working_directory"],
            "expected_exit_codes": command["expected_exit_codes"],
            "execution_plan": plans,
        },
    )
    if expected_digest != command["execution_plan_SHA256"]:
        return None
    if (
        child.get("command") != command
        or child.get("subcommand") != plans[0]
        or child.get("policy_id") != result["policy_id"]
        or child.get("exit_code") != result.get("exit_code")
        or any(
            child.get(key) != result[key]
            for key in ("ticket_id", "work_packet_id", "work_packet_SHA256")
        )
    ):
        return None
    failure = _unsupported_option(child, plans[0], command)
    if failure is None:
        return None
    return {
        **failure,
        "validation_id": spec.validation_id,
        "command": command,
        "execution_plan": plans,
        "command_authority_matched": True,
        "ad_hoc_command_substitution": False,
        "validation_result_SHA256": _sha(result),
        "exit_code": result["exit_code"],
    }


def _session_evidence(rows, projection, run, workspace, specs):
    witness = None
    calls = {}
    discoveries = {}
    attempts = []
    for row in rows:
        if row["role"] == "assistant":
            for call in _json(row["tool_calls"] or "[]"):
                function = call.get("function", {})
                calls[call.get("id")] = (
                    function.get("name"),
                    _json(function.get("arguments", "{}")),
                    row,
                )
            continue
        if row["role"] != "tool":
            continue
        call = calls.get(row["tool_call_id"])
        if call is None or call[0] != row["tool_name"]:
            continue
        data = _json(row["content"])
        if not isinstance(data, dict):
            continue
        if row["tool_name"] == "kanban_show":
            task = data.get("task", {})
            body = _json(task.get("body", "{}"))
            if (
                call[1].get("task_id") == projection["kanban_task_id"]
                and task.get("id") == projection["kanban_task_id"]
                and task.get("current_run_id") == run.id
                and task.get("workspace_path") == str(workspace)
                and all(
                    body.get(key) == projection[field]
                    for key, field in (
                        ("TicketSpec_SHA256", "ticket_spec_SHA256"),
                        ("WorkPacket_ID", "work_packet_id"),
                        ("WorkPacket_SHA256", "work_packet_SHA256"),
                    )
                )
            ):
                witness = row
        if row["tool_name"] != "workpacket_validation" or witness is None:
            continue
        if call[1].get("action") == "list" and data.get("success") is True:
            if all(
                data.get(key) == projection[key]
                for key in ("ticket_id", "work_packet_id", "work_packet_SHA256")
            ):
                for command in data.get("commands", []):
                    discoveries[command.get("command_id")] = (command, row)
        elif call[1].get("action") == "run":
            # Any extra run or substituted command makes this evidence ambiguous.
            spec = next(
                (
                    item
                    for item in specs
                    if item.command_id == call[1].get("command_id")
                ),
                None,
            )
            discovered = discoveries.get(call[1].get("command_id"))
            if (
                spec is None
                or discovered is None
                or not _declaration_matches(discovered[0], spec)
            ):
                return None
            failure = _matching_result(data, spec, projection, discovered[0])
            if failure is None:
                return None
            failure["source_messages"] = [
                {"message_id": item["id"], "message_SHA256": _sha(item)}
                for item in (witness, discovered[1], call[2], row)
            ]
            attempts.append(failure)
    return attempts[0] if len(attempts) == 1 else None


def evidence(projection, run, workspace, work_packet, specs):
    """Return bounded persisted evidence, or None; never create state or run tools."""
    from hermes_cli import kanban_db

    metadata = run.metadata or {}
    if (
        not isinstance(metadata, dict)
        or metadata.get("validation_infrastructure_failure") is not True
        or not _no_tests_started(metadata)
        or metadata.get("terminal_outcome") != "infrastructure_failed"
        or metadata.get("kanban_task_id") != projection["kanban_task_id"]
        or any(
            metadata.get(key) != projection[key]
            for key in ("work_packet_id", "work_packet_SHA256")
        )
        or run.profile != projection["assignee_profile"]
    ):
        return None
    required = {
        step.validation_id
        for step in work_packet.validation_steps
        if step.required
        and step.command_authority is not None
        and step.command_execution_authorized
    }
    specs = [
        spec
        for spec in specs
        if spec.validation_id in required and spec.acceptance_authorized
    ]
    if not specs or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", run.profile):
        return None
    home = kanban_db.kanban_home()
    matches = []
    for path in (home / "state.db", home / "profiles" / run.profile / "state.db"):
        if not path.is_file():
            continue
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            sessions = conn.execute(
                "SELECT id, cwd, profile_name, started_at FROM sessions WHERE cwd=? AND profile_name=? AND started_at>=? AND started_at<=?",
                (str(workspace), run.profile, run.started_at, run.ended_at),
            ).fetchall()
            for session in sessions:
                rows = [
                    dict(row)
                    for row in conn.execute(
                        "SELECT id, session_id, role, content, tool_calls, tool_call_id, tool_name, timestamp FROM messages WHERE session_id=? AND active=1 AND timestamp>=? AND timestamp<=? ORDER BY id",
                        (session["id"], run.started_at, run.ended_at),
                    )
                ]
                try:
                    failure = _session_evidence(rows, projection, run, workspace, specs)
                except (ValueError, TypeError, KeyError, IndexError):
                    failure = None
                if failure:
                    terminal = metadata.get("validation_results", [])
                    if not any(
                        item.get("validation_id") == failure["validation_id"]
                        and item.get("status") == "error"
                        and item.get("exit_code") == failure["exit_code"]
                        for item in terminal
                        if isinstance(item, dict)
                    ):
                        continue
                    failure["terminal_failure_classification"] = metadata[
                        "terminal_outcome"
                    ]
                    failure["source_session"] = {
                        "database_path": str(path),
                        **dict(session),
                        "session_binding_SHA256": _sha(dict(session)),
                    }
                    matches.append(failure)
        except sqlite3.DatabaseError:
            return None
        finally:
            conn.close()
    if len(matches) != 1:
        return None
    return {"reason_code": REASON, "incompatible_validation_commands": matches}
