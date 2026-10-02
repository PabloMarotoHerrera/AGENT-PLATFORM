"""C66: persisted governed CLI failures can open a separately authorized revision."""

import json
from types import SimpleNamespace

import pytest

from hermes_state import SessionDB
from hermes_cli import kanban_db
from hermes_cli.agent_platform import product_runtime as pr
from hermes_cli.agent_platform import retry_material_revision as revision
from hermes_cli.agent_platform import validation_contract_failure as defect
from hermes_cli.agent_platform.work_packet import WorkPacketCompilationResult
from hermes_cli.agent_platform.work_packet import validation_command_runner as runner
from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import (
    work_packet_kanban_projection as projection,
)
from tools import governed_workpacket_file_guard as guard
from tools import workpacket_validation_tool as validation
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
    immutable,
)
from tests.hermes_cli import test_agent_platform_work_packet_compiler as compiler

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


@pytest.fixture
def evidence(flow, monkeypatch):
    return persist_evidence(flow, monkeypatch)


def persist_evidence(flow, monkeypatch, *, refresh_recovery=True):
    workspace = flow.candidate.parent
    package = workspace / "2_products/pepper-agent/web"
    package.mkdir(parents=True)
    (package / "package.json").write_text(
        json.dumps({"scripts": {"test": "vitest run"}})
    )
    cli = workspace / "2_products/pepper-agent/node_modules/vitest/vitest.mjs"
    cli.parent.mkdir(parents=True)
    cli.write_text("// isolated fixture: the launch boundary is replaced")
    node = flow.home / "fixture-bin/node"
    node.parent.mkdir()
    node.write_text("isolated fixture executable")
    monkeypatch.setattr(validation, "_resolve_node_executable", lambda: node)
    projected = projection.load_kanban_projection_record(
        ticket_id=flow.record["ticket_id"]
    )
    packet = WorkPacketCompilationResult.model_validate(
        flow.record["work_packet_compilation_result"]
    ).work_packet
    authority = guard.WorkPacketFileAuthority(
        ticket_id=flow.record["ticket_id"],
        ticket_spec_SHA256=flow.record["ticket_spec_SHA256"],
        work_packet_id=flow.record["work_packet_id"],
        work_packet_SHA256=flow.record["work_packet_SHA256"],
        projection_SHA256=projected["projection_SHA256"],
        allowed_paths=tuple(packet.repository_scope.allowed_paths),
        forbidden_paths=tuple(packet.repository_scope.forbidden_paths),
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(),
    )
    spec = validation.build_governed_validation_command_specs(authority, packet)[0]
    stderr = f"ArgumentError: Unknown option `--runInBand`\n    at Command.checkUnknownOptions (file://{cli.parent}/parser.js:12:1)\n    at CLI.parse (file://{cli.parent}/parser.js:20:1)\n"
    monkeypatch.setattr(
        runner,
        "_launch_and_capture",
        lambda *a, **kw: runner._LaunchResult(
            exit_code=1,
            stdout_raw=b"",
            stderr_raw=stderr.encode(),
            process_started=True,
            terminate_requested=False,
            kill_requested=False,
            timed_out=False,
            output_limit_exceeded=False,
            launch_failed=False,
        ),
    )
    result = json.loads(validation._run_command(authority, spec))
    assert result["process_started"] is True
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    metadata = {
        "validation_infrastructure_failure": True,
        "terminal_outcome": "infrastructure_failed",
        "execution_validation_passed": False,
        "work_packet_id": projected["work_packet_id"],
        "work_packet_SHA256": projected["work_packet_SHA256"],
        "kanban_task_id": projected["kanban_task_id"],
        "validation_results": [
            {"validation_id": "V1", "status": "error", "exit_code": 1}
        ],
    }
    try:
        conn.execute(
            "UPDATE task_runs SET metadata=?, summary=? WHERE id=?",
            (
                json.dumps(metadata),
                "validation-infrastructure-failed: unsupported governed CLI option before tests",
                flow.run_id,
            ),
        )
        conn.commit()
        run = kanban_db.list_runs(conn, projected["kanban_task_id"])[-1]
    finally:
        conn.close()
    if refresh_recovery:
        # Rebuild the isolated recovery after persisting the terminal failure evidence.
        pr.recovery_action_record_path_for_ticket(flow.record["ticket_id"]).unlink()
        recovered = pr.recover_current_ticket_execution(
            human_authorization_text=pr.governed_ticket_recovery_authorization_text(
                flow.record["ticket_id"]
            ),
            ticket_id=flow.record["ticket_id"],
        )
        flow.args.update(
            reason_code=defect.REASON,
            recovery_action_SHA256=recovered["recovery_action_SHA256"],
        )
    database = flow.home / "profiles" / run.profile / "state.db"
    state = SessionDB(database)
    sid = "synthetic-c66-worker"
    state.create_session(sid, "cli", cwd=str(workspace), profile_name=run.profile)
    state._conn.execute(
        "UPDATE sessions SET started_at=? WHERE id=?", (run.started_at + 1, sid)
    )
    sequence = 0

    def message(name, args, payload):
        nonlocal sequence
        sequence += 1
        call = f"call-{sequence}"
        stamp = run.started_at + 10 + sequence * 2
        state.append_message(
            sid,
            "assistant",
            tool_calls=[
                {
                    "id": call,
                    "type": "function",
                    "function": {"name": name, "arguments": json.dumps(args)},
                }
            ],
            timestamp=stamp,
        )
        return state.append_message(
            sid,
            "tool",
            content=json.dumps(payload),
            tool_name=name,
            tool_call_id=call,
            timestamp=stamp + 1,
        )

    show = message(
        "kanban_show",
        {"task_id": projected["kanban_task_id"]},
        {
            "task": {
                "id": projected["kanban_task_id"],
                "current_run_id": run.id,
                "workspace_path": str(workspace),
                "body": json.dumps({
                    "TicketSpec_SHA256": projected["ticket_spec_SHA256"],
                    "WorkPacket_ID": projected["work_packet_id"],
                    "WorkPacket_SHA256": projected["work_packet_SHA256"],
                }),
            }
        },
    )
    listed = message(
        "workpacket_validation",
        {"action": "list"},
        {
            "success": True,
            "ticket_id": projected["ticket_id"],
            "work_packet_id": projected["work_packet_id"],
            "work_packet_SHA256": projected["work_packet_SHA256"],
            "commands": [validation._public_command(spec)],
        },
    )
    executed = message(
        "workpacket_validation",
        {"action": "run", "command_id": spec.command_id},
        result,
    )
    state.close()
    return SimpleNamespace(
        database=database,
        result=result,
        run=run,
        projected=projected,
        spec=spec,
        packet=packet,
        workspace=workspace,
        show=show,
        listed=listed,
        executed=executed,
    )


def rewrite(evidence, change, message_id=None):
    state = SessionDB(evidence.database)
    try:
        row_id = evidence.executed if message_id is None else message_id
        payload = json.loads(
            state._conn.execute(
                "SELECT content FROM messages WHERE id=?", (row_id,)
            ).fetchone()[0]
        )
        change(payload)
        state._conn.execute(
            "UPDATE messages SET content=? WHERE id=?", (json.dumps(payload), row_id)
        )
    finally:
        state.close()


def stream(text, kind):
    return runner._captured_stream(kind, text.encode(), 8192).model_dump(mode="json")


def test_explicit_request_binds_proof_and_preserves_retry_run_candidate(flow, evidence):
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "retry_pending"
    alternative = workflow["alternative_actions"][0]
    assert alternative["reason_code"] == defect.REASON
    assert alternative["request_binding"]["reason_code"] == defect.REASON
    before = immutable(flow)
    result = revision.request(**flow.args)
    assert result["retry_authority_status"] == "suspended_not_consumed"
    assert all(
        result[key] is False
        for key in (
            "retry_started",
            "new_run_started",
            "retry_budget_consumed",
            "execution_started",
        )
    )
    assert immutable(flow) == before
    assert pr.build_workflow_control_snapshot()["next_action"]["id"] == "REVISE_P99_4"
    assert revision.request(**flow.args)["idempotent_replay"] is True
    failure = result["material_failure_evidence"]["incompatible_validation_commands"][0]
    assert failure["command_authority_matched"] is True
    assert failure["ad_hoc_command_substitution"] is False
    assert failure["test_execution_started"] is False
    assert len(failure["source_messages"]) == 4


@pytest.mark.parametrize(
    "mutation",
    [
        "authority",
        "argv",
        "working_directory",
        "plan_digest",
        "test_failure",
        "explicit_test_start",
        "vague_infrastructure",
        "wrong_option",
        "untrusted_parser_stack",
        "truncated_stderr",
        "stream_digest",
        "ad_hoc",
        "wrong_run",
        "wrong_ticket_spec",
        "discovery_mismatch",
    ],
)
def test_noncanonical_or_noncontract_failures_are_ineligible(flow, evidence, mutation):
    def alter(data):
        child = data["subcommand_results"][0]
        if mutation == "authority":
            data["command"]["command_authority_SHA256"] = "0" * 64
        elif mutation == "argv":
            child["subcommand"]["effective_argv"].append("--extra")
        elif mutation == "working_directory":
            child["subcommand"]["working_directory"] = str(flow.home)
        elif mutation == "plan_digest":
            data["execution_plan_SHA256"] = "0" * 64
        elif mutation == "test_failure":
            child["stdout"] = stream(
                "Tests: 1 failed; assertion did not match",
                runner.ValidationCommandStreamKind.STDOUT,
            )
            child["stderr"] = stream(
                "AssertionError: expected true",
                runner.ValidationCommandStreamKind.STDERR,
            )
        elif mutation == "explicit_test_start":
            child["test_execution_started"] = True
        elif mutation == "vague_infrastructure":
            child["stderr"] = stream(
                "Environment unavailable: network timeout",
                runner.ValidationCommandStreamKind.STDERR,
            )
        elif mutation == "wrong_option":
            child["stderr"] = stream(
                "ArgumentError: Unknown option `--unapproved`",
                runner.ValidationCommandStreamKind.STDERR,
            )
        elif mutation == "untrusted_parser_stack":
            child["stderr"] = stream(
                f"ArgumentError: Unknown option `--runInBand`\n    at Command.checkUnknownOptions (file://{flow.home}/test.ts:1:1)",
                runner.ValidationCommandStreamKind.STDERR,
            )
        elif mutation == "truncated_stderr":
            child["stderr"]["truncated"] = True
        elif mutation == "stream_digest":
            child["stderr"]["stream_SHA256"] = "0" * 64
        elif mutation == "ad_hoc":
            data["ad_hoc_command_substitution"] = True

    if mutation == "wrong_run":
        rewrite(evidence, lambda d: d["task"].update(current_run_id=999), evidence.show)
    elif mutation == "wrong_ticket_spec":
        rewrite(
            evidence,
            lambda d: d["task"].update(
                body=json.dumps({"TicketSpec_SHA256": "0" * 64})
            ),
            evidence.show,
        )
    elif mutation == "discovery_mismatch":
        rewrite(
            evidence,
            lambda d: d["commands"][0].update(command_authority_SHA256="0" * 64),
            evidence.listed,
        )
    else:
        rewrite(evidence, alter)
    before = immutable(flow)
    assert not pr.build_workflow_control_snapshot().get("alternative_actions")
    with pytest.raises(
        pr.ProductRuntimeConflict, match="material contract failure evidence"
    ):
        revision.request(**flow.args)
    assert immutable(flow) == before
    assert not revision.path_for(flow.record).exists()


def test_historical_worker_runtime_does_not_depend_on_reader_path(
    flow, evidence, monkeypatch
):
    monkeypatch.setattr(validation, "_resolve_node_executable", lambda: None)
    assert (
        pr.build_workflow_control_snapshot()["alternative_actions"][0]["reason_code"]
        == defect.REASON
    )


def test_material_and_retry_consent_stay_separate(flow, evidence):
    with pytest.raises(pr.ProductRuntimeDecisionFailed):
        revision.request(**{
            **flow.args,
            "human_authorization_text": "Autorizo el retry de P99.4.",
        })
    result = pr.start_current_ticket_execution(
        human_authorization_text=flow.args["human_authorization_text"],
        ticket_id="P99.4",
        next_action_id=pr.governed_ticket_lifecycle_action_ids("P99.4")["retry_start"],
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert result["execution_started"] is False
    assert not revision.path_for(flow.record).exists()


def test_new_reason_uses_canonical_revision_and_fresh_approval(flow, evidence):
    requested = revision.request(**flow.args)
    before = immutable(flow)
    blocked = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo el retry de P99.4.",
        ticket_id="P99.4",
        next_action_id=pr.governed_ticket_lifecycle_action_ids("P99.4")["retry_start"],
        spawn_fn=lambda *a, **kw: pytest.fail("must not dispatch"),
    )
    assert blocked["blocker_code"] == "RETRY_SUSPENDED_FOR_MATERIAL_REVISION"
    assert immutable(flow) == before
    command = compiler.command_authority(
        source_command="npm test", command_argv=("npm", "test")
    )
    steps = [
        compiler.validation_step(
            command=command.source_command, command_authority=command
        ).model_dump(mode="json"),
        compiler.validation_step("V2", command=None).model_dump(mode="json"),
    ]
    result = pr.revise_current_ticket_for_material_contract_failure(
        human_authorization_text="I explicitly authorize revision of P99.4.",
        ticket_id="P99.4",
        next_action_id="REVISE_P99_4",
        revision_contract={"ticket_id": "P99.4", "validation_steps": steps},
    )
    assert result["revision_status"] == "awaiting_ticket_approval"
    revised = bridge.load_generation_record(ticket_id="P99.4")
    assert revised["work_packet_SHA256"] != flow.record["work_packet_SHA256"]
    assert (
        revised["revision_authority"]["material_revision_request_SHA256"]
        == requested["material_revision_request_SHA256"]
    )
    assert (
        bridge.load_approval_decision_record(
            ticket_id="P99.4", generation_record=revised
        )
        is None
    )
    assert flow.candidate.read_text() == "preserved implementation candidate"
    with pytest.raises(pr.ProductRuntimeError):
        pr.start_current_ticket_execution(
            human_authorization_text="Autorizo el retry de P99.4.",
            ticket_id="P99.4",
            next_action_id=pr.governed_ticket_lifecycle_action_ids("P99.4")[
                "retry_start"
            ],
            spawn_fn=lambda *a, **kw: pytest.fail("old authority must not dispatch"),
        )


def test_proof_changes_after_request_fail_closed(flow, evidence):
    revision.request(**flow.args)
    rewrite(evidence, lambda d: d["command"].update(command_authority_SHA256="0" * 64))
    assert (
        pr.build_workflow_control_snapshot()["workflow_status"]
        == "material_revision_authority_blocked"
    )


@pytest.mark.parametrize(
    "mismatch",
    [
        "cwd",
        "profile",
        "timestamp",
        "inactive_result",
        "missing_discovery",
        "duplicate_result",
    ],
)
def test_session_lineage_must_be_unambiguous_and_bound_to_run(flow, evidence, mismatch):
    state = SessionDB(evidence.database)
    try:
        if mismatch == "cwd":
            state._conn.execute("UPDATE sessions SET cwd=?", (str(flow.home),))
        elif mismatch == "profile":
            state._conn.execute("UPDATE sessions SET profile_name='other-worker'")
        elif mismatch == "timestamp":
            state._conn.execute(
                "UPDATE sessions SET started_at=?", (evidence.run.started_at - 1,)
            )
        elif mismatch == "inactive_result":
            state._conn.execute(
                "UPDATE messages SET active=0 WHERE id=?", (evidence.executed,)
            )
        elif mismatch == "missing_discovery":
            state._conn.execute("DELETE FROM messages WHERE id=?", (evidence.listed,))
        elif mismatch == "duplicate_result":
            state.append_message(
                "synthetic-c66-worker",
                "tool",
                content=json.dumps(evidence.result),
                tool_name="workpacket_validation",
                tool_call_id="call-3",
                timestamp=evidence.run.started_at + 50,
            )
    finally:
        state.close()
    assert not pr.build_workflow_control_snapshot().get("alternative_actions")
    with pytest.raises(
        pr.ProductRuntimeConflict, match="material contract failure evidence"
    ):
        revision.request(**flow.args)


def test_no_alternative_before_separate_recovery(flow, evidence):
    pr.recovery_action_record_path_for_ticket("P99.4").unlink()
    snapshot = pr.build_workflow_control_snapshot()
    assert snapshot["workflow_status"] == "execution_failed"
    assert not snapshot.get("alternative_actions")
    with pytest.raises(pr.ProductRuntimeConflict, match="retry-pending"):
        revision.request(**flow.args)
    assert not revision.path_for(flow.record).exists()


def test_new_reason_cannot_be_misrepresented_as_missing_authority(flow, evidence):
    with pytest.raises(
        pr.ProductRuntimeConflict, match="material contract failure evidence"
    ):
        revision.request(**{**flow.args, "reason_code": revision.REASON})
    assert not revision.path_for(flow.record).exists()


def test_public_tool_exposes_and_accepts_the_new_reason(flow, evidence):
    from tools import pepper_workflow_tools as tools

    next_action = json.loads(tools._get_next_action({}))
    assert next_action["alternative_actions"][0]["reason_code"] == defect.REASON
    result = json.loads(tools._request_current_ticket_material_revision(flow.args))
    assert result["workflow_status"] == "awaiting_material_revision"
    assert result["reason_code"] == defect.REASON
    assert result["retry_budget_consumed"] is False
