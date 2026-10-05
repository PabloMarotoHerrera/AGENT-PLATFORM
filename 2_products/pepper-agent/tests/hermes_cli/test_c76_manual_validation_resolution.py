"""C76 uses isolated homes and the actual projection/decision/dispatch boundary."""

import json
import os
import subprocess
from pathlib import Path
import pytest
from hermes_cli import kanban_db as kb
from hermes_cli.agent_platform import product_runtime as pr, manual_validation as mv
from hermes_cli.agent_platform import manual_validation_resolution as resolution
from tests.hermes_cli.test_c69_zero_change_decision import completed as completed, runs
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c66_invalid_validation_command_revision import (
    evidence as evidence,
)
from tests.hermes_cli import (
    test_agent_platform_work_packet_kanban_projection as fixtures,
)
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import test_agent_platform_work_packet_compiler as compiler
from tools import pepper_workflow_tools as tools

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


@pytest.fixture(autouse=True)
def full_contract(monkeypatch):
    original = generation._synthetic_implementation_target

    def target(*args, **kwargs):
        if "contract" in kwargs:
            kwargs["contract"]["validation_steps"].extend(
                compiler.validation_step(f"V{i}", command=None).model_dump(mode="json")
                for i in range(3, 9)
            )
        return original(*args, **kwargs)

    monkeypatch.setattr(generation, "_synthetic_implementation_target", target)


def attest(validation_id, status):
    c = pr.inspect_current_ticket_manual_validation()
    item = next(i for i in c["items"] if i["validation_id"] == validation_id)
    return pr.attest_current_ticket_manual_validation(
        ticket_id=c["ticket_id"],
        work_packet_id=c["work_packet_id"],
        work_packet_sha256=c["work_packet_SHA256"],
        run_id=c["run_id"],
        validation_id=validation_id,
        validation_contract_sha256=c["validation_contract_SHA256"],
        binding_sha256=item["binding_SHA256"],
        next_action_id=c["next_action_id"],
        status=status,
        human_attestation_text=item["required_attestation_text"][status],
        evidence="Human inspected rendered theme and actual CSS authority.",
    )


@pytest.fixture
def failed(completed, evidence):
    f = completed
    from tests.hermes_cli import test_c68_execution_evidence as c68

    c68.test_persisted_test_summary_without_execution(f, evidence, None, "passed")
    pr.attest_current_ticket_zero_change_for_review_prepare(
        human_attestation_text=pr.governed_ticket_zero_change_attestation_text(
            f.p["ticket_id"]
        ),
        project_id=f.p["project_id"],
        ticket_id=f.p["ticket_id"],
        next_action_id=pr.governed_ticket_lifecycle_action_ids(f.p["ticket_id"])[
            "zero_change_attestation"
        ],
    )
    attest("V4", "failed")
    w = pr.build_workflow_control_snapshot()
    assert w["workflow_status"] == "blocked_manual_validation_failed", w
    assert not w["remaining_blockers"], w["remaining_blockers"]
    f.binding = w["next_action"]["resolution_binding"]
    f.args = dict(
        binding=f.binding,
        decision=resolution.IMPLEMENTATION,
        human_authorization_text=resolution.consent(
            f.binding, resolution.IMPLEMENTATION
        ),
        corrective_guidance="Inspect index.css, tokens.css, shell/sidebar/shared controls; render neutral dark surfaces and restrained Pepper blue; keep semantic green/amber/red.",
    )
    return f


def test_discovery_decision_preservation_and_separate_start(failed):
    f = failed
    before = runs(f)
    result = resolution.resolve(**f.args)
    assert not result["execution_started"] and not result["revision_generated"]
    assert runs(f) == before
    assert resolution.resolve(**f.args)["idempotent_replay"]
    w = pr.build_workflow_control_snapshot()
    assert w["workflow_status"] == resolution.STATE, w
    assert not w["reviewable_result"]
    assert (
        w["next_action"]["tool"] == "start_current_ticket_manual_validation_correction"
    )
    assert resolution.load(f.p, f.run_id)["failed_evidence"]["status"] == "failed"
    with pytest.raises(pr.ProductRuntimeConflict, match="manual validation resolution"):
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="continue",
            ticket_id=f.p["ticket_id"],
            spawn_fn=lambda *a, **k: pytest.fail(
                "generic continuation must not dispatch"
            ),
        )
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.start_current_ticket_execution(
            human_authorization_text="Start P99.4 execution now",
            ticket_id=f.p["ticket_id"],
        )
    assert pr.prepare_current_ticket_review()["review_preparation_recorded"] is False
    with pytest.raises(pr.ProductRuntimeConflict):
        attest("V2", "passed")


@pytest.mark.parametrize(
    "key,value",
    [
        ("run_id", 999),
        ("binding_SHA256", "0" * 64),
        ("ticket_spec_SHA256", "0" * 64),
        ("work_packet_id", "wrong"),
        ("work_packet_SHA256", "0" * 64),
        ("projection_SHA256", "0" * 64),
        ("evidence_SHA256", "0" * 64),
        ("publication_revision", 99),
        ("ticket_id", "P99.5"),
    ],
)
def test_identity_guards(failed, key, value):
    binding = {**failed.binding, key: value}
    with pytest.raises((ValueError, pr.ProductRuntimeError)):
        resolution.resolve(**{
            **failed.args,
            "binding": binding,
            "human_authorization_text": resolution.consent(
                binding, resolution.IMPLEMENTATION
            ),
        })
    assert not resolution.path_for(failed.p, failed.run_id).exists()


@pytest.mark.parametrize("text", ["", "continue", "yes"])
def test_explicit_consent_required(failed, text):
    with pytest.raises(pr.ProductRuntimeConflict):
        resolution.resolve(**{**failed.args, "human_authorization_text": text})
    assert not resolution.path_for(failed.p, failed.run_id).exists()


def test_conflicting_decision_and_tamper(failed):
    f = failed
    resolution.resolve(**f.args)
    with pytest.raises(pr.ProductRuntimeConflict):
        resolution.resolve(**{
            **f.args,
            "decision": resolution.MATERIAL,
            "human_authorization_text": resolution.consent(
                f.binding, resolution.MATERIAL
            ),
        })
    path = resolution.path_for(f.p, f.run_id)
    record = json.loads(path.read_text())
    record["corrective_guidance"] = "tampered"
    path.write_text(json.dumps(record))
    with pytest.raises(pr.ProductRuntimeConflict):
        resolution.load(f.p, f.run_id)
    assert any(
        b["id"] == "MANUAL-VALIDATION-RESOLUTION-AUTHORITY"
        for b in pr.build_workflow_control_snapshot()["remaining_blockers"]
    )


@pytest.mark.parametrize("kind", ["missing_evidence", "changed_evidence", "active"])
def test_missing_changed_evidence_or_active_execution(failed, kind):
    f = failed
    if kind == "active":
        with kb.connect(board=f.p["kanban_board_slug"]) as c:
            c.execute("UPDATE task_runs SET status='running' WHERE id=?", (f.run_id,))
            c.commit()
    else:
        item = next(
            i
            for i in pr.inspect_current_ticket_manual_validation()["items"]
            if i["validation_id"] == "V4"
        )
        path = mv.record_path(item["binding"])
        if kind == "missing_evidence":
            path.unlink()
        else:
            path.write_text("{}")
    with pytest.raises((ValueError, pr.ProductRuntimeError)):
        resolution.resolve(**f.args)
    assert not resolution.path_for(f.p, f.run_id).exists()


def test_tools_reject_extra_arguments(failed):
    assert not json.loads(
        tools._resolve_current_ticket_manual_validation_failure({
            **failed.args,
            "path": "arbitrary",
        })
    )["success"]


def test_material_revision_separate_authorization(failed):
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

    f = failed
    before = runs(f)
    path = bridge.generation_record_path_for_ticket(f.p["ticket_id"])
    original = path.read_bytes()
    result = resolution.resolve(**{
        **f.args,
        "decision": resolution.MATERIAL,
        "human_authorization_text": resolution.consent(f.binding, resolution.MATERIAL),
    })
    assert path.read_bytes() == original and runs(f) == before
    assert result["next_action"]["id"] == "REVISE_P99_4"
    args = dict(
        ticket_id="P99.4",
        next_action_id="REVISE_P99_4",
        revision_contract={
            "ticket_id": "P99.4",
            "objective": "Correct the contract with explicit rendered theme requirements.",
        },
    )
    with pytest.raises((
        ValueError,
        pr.ProductRuntimeError,
        bridge.TicketArchitectBridgeError,
    )):
        pr.revise_current_ticket_for_material_contract_failure(
            **args, human_authorization_text="continue"
        )
    assert path.read_bytes() == original
    revised = pr.revise_current_ticket_for_material_contract_failure(
        **args, human_authorization_text="I explicitly authorize revision of P99.4."
    )
    assert revised["revision_status"] == "awaiting_ticket_approval", revised
    record = bridge.load_generation_record(ticket_id="P99.4")
    assert record["revision_authority"]["revision_reason"] == resolution.REASON
    assert runs(f) == before
    assert resolution.load(f.p, f.run_id)["failed_evidence"]["status"] == "failed"


@pytest.mark.parametrize("new_failure", [False, True])
def test_fresh_dispatch(failed, monkeypatch, evidence, new_failure):
    f = failed
    before = runs(f)
    record = resolution.resolve(**f.args)["resolution"]
    args = dict(
        ticket_id=f.p["ticket_id"],
        run_id=f.run_id,
        decision_SHA256=record["decision_SHA256"],
        human_authorization_text=resolution.start_consent(record),
    )
    for text in ("continue", f.args["human_authorization_text"]):
        with pytest.raises(pr.ProductRuntimeConflict):
            resolution.start(**{**args, "human_authorization_text": text})
    fixtures._patch_synthetic_scratch_materialization(monkeypatch, pr)
    original_materialize = pr._materialize_pepper_governed_scratch_source

    def canonical_source(p, workspace, **kwargs):
        assert kwargs.get("source_root") is None
        assert Path(workspace) != f.workspace
        materialized = original_materialize(p, workspace, **kwargs)
        (Path(workspace) / "2_products/pepper-agent/web/package.json").write_text(
            json.dumps({"scripts": {"test": "vitest run"}})
        )
        materialized["materialized_roots"].append(
            "2_products/pepper-agent/web/package.json"
        )
        return materialized

    monkeypatch.setattr(
        pr, "_materialize_pepper_governed_scratch_source", canonical_source
    )
    monkeypatch.setattr(
        pr, "_executor_provider_readiness", fixtures._ready_executor_provider_payload
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda *a, **k: fixtures._ready_worker_credential_probe(),
    )
    monkeypatch.setattr(pr, "_pepper_governed_worker_env_overlay", lambda p: {})
    monkeypatch.setattr(
        pr,
        "_run_source_authority_git",
        lambda *a: subprocess.CompletedProcess(a, 1, "", "isolated canonical source"),
    )
    monkeypatch.setattr(kb, "_pid_alive", lambda pid: pid == os.getpid())
    seen = []
    result = resolution.start(
        **args,
        spawn_fn=lambda task, workspace, **kw: (
            seen.append((task, workspace)) or os.getpid()
        ),
    )
    assert result["execution_started"], json.dumps(result, indent=2)
    assert len(seen) == 1 and runs(f)[:-1] == before
    new = runs(f)[-1]
    assert new["id"] != f.run_id
    assert Path(result["workspace_path"]) != f.workspace
    assert result["durable_source_authority_validated_before_worker_execution"]
    source = result["durable_source_authority_reference"]
    source_record = json.loads(Path(source["authority_path"]).read_text())
    for k in (
        "ticket_spec_SHA256",
        "work_packet_id",
        "work_packet_SHA256",
        "projection_SHA256",
    ):
        assert source_record[k] == f.p[k]
    assert source["run_id"] == new["id"]
    assert (
        "synthetic = true"
        in (
            Path(result["workspace_path"]) / "2_products/pepper-agent/web/src/App.tsx"
        ).read_text()
    )
    body = json.loads(seen[0][0].body)
    assert body["corrective_implementation_intent"] == f.args["corrective_guidance"]
    assert body["manual_validation_resolution_SHA256"] == record["decision_SHA256"]
    assert resolution.current(f.p) is None
    active = pr.build_workflow_control_snapshot()
    assert active["active_execution_count"] == 1 and not active.get(
        "reviewable_result"
    ), active
    try:
        premature = pr.prepare_current_ticket_review()
    except pr.ProductRuntimeConflict:
        pass
    else:
        assert not premature["review_preparation_recorded"]
    assert resolution.start(
        **args, spawn_fn=lambda *a, **k: pytest.fail("duplicate worker")
    )["idempotent_replay"]
    assert resolution.load(f.p, f.run_id) == record
    validate_new_round(f, new, result, record, monkeypatch, evidence, new_failure)
    (f.home / "c76-isolated-proof.json").write_text(
        json.dumps(
            {
                "start": result,
                "old_run": before[-1],
                "new_run": new,
                "resolution": record,
            },
            indent=2,
        )
    )


def validate_new_round(f, new, result, record, monkeypatch, evidence, new_failure):
    from hermes_state import SessionDB
    from tools import workpacket_validation_tool as validation
    from tools import governed_workpacket_file_guard as guard
    from hermes_cli.agent_platform.work_packet import (
        validation_command_runner as runner,
    )

    workspace = Path(result["workspace_path"])
    package = workspace / "2_products/pepper-agent/web"
    package.mkdir(parents=True, exist_ok=True)
    (package / "package.json").write_text(
        json.dumps({"scripts": {"test": "vitest run"}})
    )
    cli = workspace / "2_products/pepper-agent/node_modules/vitest/vitest.mjs"
    cli.parent.mkdir(parents=True, exist_ok=True)
    cli.write_text("// isolated launch boundary")
    authority = guard.WorkPacketFileAuthority(
        ticket_id=f.p["ticket_id"],
        ticket_spec_SHA256=f.p["ticket_spec_SHA256"],
        work_packet_id=f.p["work_packet_id"],
        work_packet_SHA256=f.p["work_packet_SHA256"],
        projection_SHA256=f.p["projection_SHA256"],
        allowed_paths=tuple(evidence.packet.repository_scope.allowed_paths),
        forbidden_paths=tuple(evidence.packet.repository_scope.forbidden_paths),
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(),
    )
    spec = validation.build_governed_validation_command_specs(
        authority, evidence.packet
    )[0]
    launches = []

    def launch(*a, **kw):
        launches.append(1)
        return runner._LaunchResult(
            exit_code=0,
            stdout_raw=b"RUN v4.1.9 /fixture\n Test Files  2 passed (2)\n Tests  4 passed (4)\n",
            stderr_raw=b"",
            process_started=True,
            terminate_requested=False,
            kill_requested=False,
            timed_out=False,
            output_limit_exceeded=False,
            launch_failed=False,
        )

    monkeypatch.setattr(runner, "_launch_and_capture", launch)
    v1 = json.loads(validation._run_command(authority, spec))
    assert v1["command"] == validation._public_command(spec), (
        v1["command"],
        validation._public_command(spec),
    )
    assert launches and v1["success"], v1
    state = SessionDB(evidence.database)
    sid = "c76-fresh-worker"
    state.create_session(sid, "cli", cwd=str(workspace), profile_name=new["profile"])
    state._conn.execute(
        "UPDATE sessions SET started_at=? WHERE id=?", (new["started_at"] + 1, sid)
    )
    payloads = [
        (
            "kanban_show",
            {},
            {
                "task": {
                    "id": f.p["kanban_task_id"],
                    "current_run_id": new["id"],
                    "workspace_path": str(workspace),
                    "body": json.dumps({
                        "TicketSpec_SHA256": f.p["ticket_spec_SHA256"],
                        "WorkPacket_ID": f.p["work_packet_id"],
                        "WorkPacket_SHA256": f.p["work_packet_SHA256"],
                    }),
                }
            },
        ),
        (
            "workpacket_validation",
            {"action": "list"},
            {
                "success": True,
                "ticket_id": f.p["ticket_id"],
                "work_packet_id": f.p["work_packet_id"],
                "work_packet_SHA256": f.p["work_packet_SHA256"],
                "commands": [validation._public_command(spec)],
            },
        ),
        ("workpacket_validation", {"action": "run", "command_id": spec.command_id}, v1),
    ]
    for i, (name, args, payload) in enumerate(payloads):
        call = f"c76-{i}"
        stamp = new["started_at"] + 10 + i * 2
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
        state.append_message(
            sid,
            "tool",
            content=json.dumps(payload),
            tool_name=name,
            tool_call_id=call,
            timestamp=stamp + 1,
        )
    state.close()
    (package / "src/App.tsx").write_text(
        'export const correctedTheme = "neutral dark Pepper blue";'
    )
    metadata = {
        "implementation_complete": True,
        "validation_passed": True,
        "review_required": True,
        "durable_source_authority_reference": result[
            "durable_source_authority_reference"
        ],
        "validation_results": [
            {"validation_id": "V1", "status": "passed", "exit_code": 0}
        ],
    }
    with kb.connect(board=f.p["kanban_board_slug"]) as conn:
        conn.execute(
            "UPDATE tasks SET status='blocked',block_kind='needs_input',current_run_id=NULL,worker_pid=NULL,claim_lock=NULL,last_failure_error=NULL WHERE id=?",
            (f.p["kanban_task_id"],),
        )
        conn.execute(
            "UPDATE task_runs SET status='blocked',outcome='blocked',ended_at=?,metadata=?,summary='Implementation completed; validation passed; review required',error=NULL WHERE id=?",
            (new["started_at"] + 100, json.dumps(metadata), new["id"]),
        )
        conn.commit()
    c = pr.inspect_current_ticket_manual_validation()
    assert c["run_id"] == new["id"] and len(c["items"]) == 7
    assert all(i["status"] == "pending" for i in c["items"])
    completion = pr._current_review_round_completion_source(f.p)
    from hermes_cli.agent_platform import execution_evidence as ev

    observed = ev.inspect(ticket_id=f.p["ticket_id"], run_id=new["id"])
    assert observed["validation"]["available"], json.dumps(observed, indent=2)
    canonical = [
        r
        for r in validation.review_prepare_validation_result_records(completion)
        if r.get("review_prepare_validation_evidence_mode")
        == "canonical_worker_evidence"
    ]
    assert (
        len(canonical) == 1 and canonical[0]["provenance"]["worker_session_id"] == sid
    ), canonical
    assert not pr.build_workflow_control_snapshot()["reviewable_result"]
    for i in range(2, 9):
        attest(f"V{i}", "failed" if new_failure and i == 4 else "passed")
        if new_failure and i == 4:
            break
    w = pr.build_workflow_control_snapshot()
    assert resolution.load(f.p, f.run_id) == record
    if new_failure:
        assert w["workflow_status"] == "blocked_manual_validation_failed", w
        assert w["next_action"]["resolution_binding"]["run_id"] == new["id"]
        assert not w["reviewable_result"]
        binding = w["next_action"]["resolution_binding"]
        second = resolution.resolve(**{
            **f.args,
            "binding": binding,
            "human_authorization_text": resolution.consent(
                binding, resolution.IMPLEMENTATION
            ),
        })["resolution"]
        assert second["run_id"] == new["id"]
        third = resolution.start(
            ticket_id=f.p["ticket_id"],
            run_id=new["id"],
            decision_SHA256=second["decision_SHA256"],
            human_authorization_text=resolution.start_consent(second),
            spawn_fn=lambda *a, **k: os.getpid(),
        )
        assert third["execution_started"], third
        assert third["kanban_run_id"] > new["id"] and third["workspace_path"] != str(
            workspace
        )
        assert resolution.load(f.p, f.run_id) == record
    else:
        assert w["reviewable_result"] and w["validation_contract_satisfied"], w
        prepared = pr.prepare_current_ticket_review()
        assert prepared["review_preparation_recorded"], prepared


def test_revalidation_before_persistence(failed, monkeypatch):
    original = resolution.context
    calls = []

    def changed(p):
        b, e = original(p)
        calls.append(1)
        if len(calls) > 1:
            b = {**b, "evidence_SHA256": "0" * 64}
        return b, e

    monkeypatch.setattr(resolution, "context", changed)
    with pytest.raises(pr.ProductRuntimeConflict):
        resolution.resolve(**failed.args)
    assert not resolution.path_for(failed.p, failed.run_id).exists()
    assert not json.loads(
        tools._start_current_ticket_manual_validation_correction({
            "spawn_fn": "arbitrary"
        })
    )["success"]
