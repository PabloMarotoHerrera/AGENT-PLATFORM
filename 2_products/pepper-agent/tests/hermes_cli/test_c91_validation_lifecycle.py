"""Real isolated lifecycle with only the process launch substituted."""

import json
import pytest

from hermes_cli.agent_platform import product_runtime as pr, command_validation as cv
from hermes_cli.agent_platform.work_packet import validation_command_runner as runner
from tests.hermes_cli.test_c69_zero_change_decision import completed as completed, runs
from tests.hermes_cli.test_c65_retry_material_revision import flow as flow, projection_home as projection_home
from tests.hermes_cli.test_c66_invalid_validation_command_revision import evidence as evidence
from tests.hermes_cli import test_agent_platform_ticket_architect_bridge as generation
from tests.hermes_cli import test_agent_platform_work_packet_compiler as compiler
from tools import pepper_workflow_tools as public

pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


@pytest.fixture(autouse=True)
def mixed_contract(monkeypatch):
    original = generation._synthetic_implementation_target

    def target(*args, **kwargs):
        contract = kwargs.get("contract")
        if contract:
            contract["validation_steps"][1]["description"] = "Human rendered inspection"
            for vid, description in [("V3", "Classify regression failures and known-debt"), ("V4", "Integrated acceptance aggregates V1-V3")]:
                step = compiler.validation_step(vid, command=None).model_dump(mode="json")
                step["description"] = description
                contract["validation_steps"].append(step)
        return original(*args, **kwargs)
    monkeypatch.setattr(generation, "_synthetic_implementation_target", target)


@pytest.fixture
def terminal(completed, monkeypatch):
    f = completed
    (f.home / "profiles" / f.p["assignee_profile"] / "config.yaml").write_text(
        "model:\n  provider: openai-codex\n  default: gpt-5.5\n  api_mode: codex_responses\n"
        "platform_toolsets:\n  cli:\n    - pepper_repository\n    - file\n    - no_mcp\n"
    )
    pr.attest_current_ticket_zero_change_for_review_prepare(
        human_attestation_text=pr.governed_ticket_zero_change_attestation_text(f.p["ticket_id"]),
        project_id=f.p["project_id"], ticket_id=f.p["ticket_id"],
        next_action_id=pr.governed_ticket_lifecycle_action_ids(f.p["ticket_id"])["zero_change_attestation"],
    )
    f.launched = []
    def launch(*args, **kwargs):
        f.launched.append(args)
        return runner._LaunchResult(exit_code=0, stdout_raw=b"isolated command passed", stderr_raw=b"",
            process_started=True, terminate_requested=False, kill_requested=False,
            timed_out=False, output_limit_exceeded=False, launch_failed=False)
    monkeypatch.setattr(runner, "_launch_and_capture", launch)
    return f


def attest(vid):
    context = pr.inspect_current_ticket_manual_validation()
    item = next(i for i in context["items"] if i["validation_id"] == vid)
    return pr.attest_current_ticket_manual_validation(
        ticket_id=context["ticket_id"], work_packet_id=context["work_packet_id"],
        work_packet_sha256=context["work_packet_SHA256"], run_id=context["run_id"],
        validation_id=vid, validation_contract_sha256=context["validation_contract_SHA256"],
        binding_sha256=item["binding_SHA256"], next_action_id=context["next_action_id"],
        status="passed", human_attestation_text=item["required_attestation_text"]["passed"],
        evidence="Explicit human inspection of actual evidence against the current item.",
    )


def execute():
    c = cv.inspect()
    return cv.execute(binding=c["binding"], human_authorization_text=c["required_human_authorization_text"])


def test_split_lifecycle_preserves_bindings_and_requires_final_human(terminal, monkeypatch):
    before = pr.inspect_current_ticket_manual_validation()
    original_runs = runs(terminal)
    zero_path = pr.zero_change_attestation_record_path_for_ticket(terminal.p["ticket_id"])
    zero = zero_path.read_bytes()
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]
    with pytest.raises(pr.ProductRuntimeConflict, match="prerequisites"):
        attest("V3")
    attest("V2")
    w = pr.build_workflow_control_snapshot()
    assert w["validation_lifecycle_phase"] == "command_validation_pending"
    action = w["command_validation_action"]
    result = json.loads(public._prepare_current_ticket_review({
        "operation": action["operation"], "binding": action["binding"],
        "human_authorization_text": action["required_human_authorization_text"],
    }))
    assert result["success"], result
    assert result["record"]["validation"]["validation_passed"] is True, result
    assert terminal.launched
    after = pr.inspect_current_ticket_manual_validation()
    assert [i["binding"] for i in before["items"]] == [i["binding"] for i in after["items"]]
    assert [i["status"] for i in after["items"]] == ["passed", "pending", "pending"]
    assert pr.build_workflow_control_snapshot()["validation_lifecycle_phase"] == "manual_validation_final_pending"
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]
    with pytest.raises(pr.ProductRuntimeConflict, match="prerequisites"):
        attest("V4")
    monkeypatch.setattr(runner, "_launch_and_capture", lambda *a, **k: pytest.fail("replay/review must reuse evidence"))
    assert execute()["idempotent_replay"]
    attest("V3")
    attest("V4")
    assert pr.build_workflow_control_snapshot()["review_preparation_eligibility"]["available"]
    result = pr.prepare_current_ticket_review()
    assert result["review_preparation_recorded"], result
    assert zero_path.read_bytes() == zero
    assert runs(terminal) == original_runs
    assert not pr.review_decision_record_path_for_ticket(terminal.p["ticket_id"]).exists()


def test_commands_reachable_with_all_manual_pending(terminal):
    before = pr.inspect_current_ticket_manual_validation()
    assert execute()["record"]["validation"]["validation_passed"]
    assert [i["status"] for i in pr.inspect_current_ticket_manual_validation()["items"]] == ["pending"] * 3
    assert before["validation_contract_satisfied"] is False


@pytest.mark.parametrize("key", ["ticket_id", "revision", "ticket_spec_SHA256", "work_packet_id", "work_packet_SHA256", "run_id", "completion_SHA256", "validation_contract_SHA256", "projection_SHA256"])
def test_wrong_authority_cannot_launch(terminal, key):
    c = cv.inspect()
    binding = {**c["binding"], key: "wrong"}
    with pytest.raises(ValueError, match="mismatch"):
        cv.execute(binding=binding, human_authorization_text=cv.consent(binding))
    assert not terminal.launched


@pytest.mark.parametrize("text", ["", "yes", "prepare review"])
def test_human_consent_required(terminal, text):
    with pytest.raises(ValueError, match="authorization"):
        cv.execute(binding=cv.inspect()["binding"], human_authorization_text=text)
    assert not terminal.launched


def test_arbitrary_shell_and_unknown_operation_denied(terminal):
    for args in [{"operation": "run_commands", "command": "echo arbitrary"}, {"operation": "execute_shell"}]:
        assert json.loads(public._prepare_current_ticket_review(args))["success"] is False
    assert not terminal.launched


@pytest.mark.parametrize("tamper", ["record", "result", "authority"])
def test_persisted_evidence_tampering_fails_closed(terminal, tamper):
    record = execute()["record"]
    path = cv.path_for(record["binding"])
    if tamper == "record":
        record["binding"]["run_id"] += 1
    elif tamper == "result":
        record["validation"]["validation_command_results"][0]["exit_code"] = 42
    else:
        record["validation"]["review_prepare_validation_authority"]["pre_review_binding"]["run_id"] += 1
    if tamper != "record":
        record["record_SHA256"] = cv.digest({k: v for k, v in record.items() if k != "record_SHA256"})
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError):
        cv.inspect()


def test_failed_commands_do_not_satisfy_contract(terminal, monkeypatch):
    original = runner._launch_and_capture
    def fail(*a, **k):
        result = original(*a, **k)
        result.exit_code = 1
        return result
    monkeypatch.setattr(runner, "_launch_and_capture", fail)
    result = execute()
    assert result["record"]["validation"]["validation_passed"] is False
    assert cv.inspect()["command_validation_complete"]
    assert not cv.inspect()["command_validation_passed"]
    attest("V2")
    attest("V3")  # A human can truthfully classify recorded failures.
    attest("V4")  # This does not change the failing command evidence.
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]


def test_dependencies_are_generic(flow):
    contract = {"work_packet_validation_steps": [{"validation_id": "T1", "kind": "command", "required": True}, {"validation_id": "T2", "kind": "manual"}, {"validation_id": "T3", "kind": "manual"}]}
    assert cv.dependencies({"validation_id": "T3", "description": "Aggregates T1-T2"}, contract) == ["T1", "T2"]
    assert cv.dependencies({"validation_id": "T2", "description": "Human rendered acceptance"}, contract) == []


def test_canonical_context_preserves_terminal_without_snapshot(terminal, monkeypatch):
    import shutil
    f = terminal
    root = f.home / "canonical-repository"
    shutil.copytree(f.workspace, root)
    monkeypatch.setattr(pr, "_agent_platform_repository_root", lambda: root)
    monkeypatch.setattr(pr, "_completion_durable_source_authority_reference", lambda *a, **k: None)
    monkeypatch.setattr(pr, "_governed_autonomy_materialization_manifest", lambda *a, **k: (None, None))
    before = runs(f)
    c = cv.inspect()
    assert c["binding"]["canonical_validation_source"]["source_root"] == str(root)
    # No executor/provider environment or worker re-dispatch is needed.
    monkeypatch.setattr(pr, "_pepper_governed_worker_env_overlay", lambda *a, **k: pytest.fail("no worker authority"))
    assert execute()["record"]["validation"]["validation_passed"]
    assert runs(f) == before
    assert not pr.prepare_current_ticket_review()["review_preparation_recorded"]
    assert cv.inspect()["command_validation_complete"]
    (root / "2_products/pepper-agent/web/src/example.ts").write_text("changed current source")
    assert not cv.inspect()["command_validation_complete"]
    with pytest.raises(ValueError, match="mismatch"):
        cv.execute(binding=c["binding"], human_authorization_text=c["required_human_authorization_text"])


def test_final_manual_evidence_rejects_changed_command_results(terminal, monkeypatch):
    execute()
    attest("V2")
    attest("V3")
    completion = pr._current_review_round_completion_source(terminal.p)
    contract = pr._acceptance_contract_for_review_projection(terminal.p)
    from hermes_cli.agent_platform import manual_validation as mv
    item = next(i for i in mv.inspect(contract, completion) if i["validation_id"] == "V3")
    assert item["dependency_evidence"]["V1"]
    monkeypatch.setattr(cv, "dependency_evidence", lambda *a: {"V1": "different-result-digest"})
    with pytest.raises(ValueError, match="dependency evidence changed"):
        mv.inspect(contract, completion)
