from __future__ import annotations

import json
from pathlib import Path
import sys
import time
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as projection


_EXECUTOR_PROFILE = "pepper-architecture-product"
_IMPLEMENTATION_PROFILE = "pepper-frontend-implementation"
_P18_9_1_TITLE = "Pepper Shell, Routing, and Compact Navigation"
NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _workflow(**overrides):
    data = {
        "schema_version": 1,
        "source_system": "pepper-controlled-default-mode-cutover",
        "product_id": "pepper",
        "project_id": "PEPPER",
        "project_name": "Pepper",
        "macroproject_id": "P18.9",
        "macroproject_title": "Pepper Product Personalization",
        "current_ticket_id": None,
        "current_ticket_title": None,
        "current_gap_id": None,
        "current_gap_title": None,
        "next_ticket_id": "P18.9.0",
        "next_ticket_title": bridge.CANONICAL_TICKET_TITLE,
        "workflow_status": "planning_approved_or_intake_ready",
        "queue_state": "ready_to_generate_P18_9_0",
        "P18_9_ready": True,
        "P18_9_ticket_generated": False,
        "next_action": {
            "id": "GENERATE_P18_9_0",
            "label": "Generate governed P18.9.0 before execution.",
            "target_ticket_id": "P18.9.0",
            "target_ticket_title": bridge.CANONICAL_TICKET_TITLE,
        },
    }
    data.update(overrides)
    return data


def _next_ticket_workflow(**overrides):
    data = _workflow(
        current_ticket_id=None,
        current_ticket_title=None,
        next_ticket_id="P18.9.1",
        next_ticket_title=_P18_9_1_TITLE,
        workflow_state="P18.9.0-COMPLETED",
        workflow_status="completed",
        queue_state="p18_9_0_closed_next_ticket_ready",
        validation_state="review_accepted",
        review_state="accepted",
        P18_9_ticket_generated=True,
        P18_9_0_closed=True,
        next_ticket_ready=True,
        next_ticket_generated=False,
        next_action={
            "id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
            "label": f"Generate governed P18.9.1 {_P18_9_1_TITLE}.",
            "target_ticket_id": "P18.9.1",
            "target_ticket_title": _P18_9_1_TITLE,
            "required_human_action": "ticket_generation",
        },
    )
    data.update(overrides)
    return data


@pytest.fixture
def projection_home(tmp_path, monkeypatch):
    home = tmp_path / "hermes-home"
    local_appdata = tmp_path / "local-appdata"
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.setenv("HERMES_KANBAN_HOME", str(home))
    monkeypatch.setenv("LOCALAPPDATA", str(local_appdata))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    return home


def _profile_stub(
    home,
    *,
    name=_EXECUTOR_PROFILE,
    description="Pepper product architecture execution profile",
    is_default=False,
    cli_toolsets=("pepper_repository", "no_mcp"),
    model_config=False,
):
    path = home / "profiles" / name
    path.mkdir(parents=True, exist_ok=True)
    lines = []
    if model_config:
        lines.extend([
            "model:",
            "  provider: openai-codex",
            "  default: gpt-5.5",
            "  api_mode: codex_responses",
        ])
    if cli_toolsets is not None:
        lines.extend(["platform_toolsets:", "  cli:"])
        lines.extend(f"    - {toolset}" for toolset in cli_toolsets)
    if lines:
        (path / "config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return SimpleNamespace(
        name=name,
        description=description,
        is_default=is_default,
        path=path,
    )


def _install_execution_profile(monkeypatch, home, **overrides) -> None:
    overrides.setdefault("model_config", True)
    profile = _profile_stub(home, **overrides)
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])


def _install_executor_profile_roster(monkeypatch, profiles) -> None:
    from hermes_cli import profiles as profile_module

    monkeypatch.setattr(profile_module, "list_profiles", lambda: list(profiles))


def _ready_governed_credential_status(now=NOW):
    from hermes_cli.agent_platform.provider_credentials.contracts import (
        ProviderClientTokenStatus,
        ProviderCredentialStatus,
    )

    return ProviderCredentialStatus(
        configured=True,
        durable_store_present=True,
        durable_store_valid=True,
        protection_valid=True,
        provider_state_present=False,
        pool_state_present=True,
        token_pair_present=True,
        credential_count=1,
        active_provider_matches=True,
        last_refresh_utc=now,
        expires_at_utc=now + timedelta(hours=1),
        client_token_status=ProviderClientTokenStatus(
            access_token_present=True,
            refresh_token_present=True,
            expiry_known=True,
            issued_at_utc=now,
            expires_at_utc=now + timedelta(hours=1),
            remaining_lifetime_ms=3_600_000,
            usable_for_bounded_lease=True,
        ),
    )


def _patch_ready_governed_provider(monkeypatch, canonical_root):
    from hermes_cli.agent_platform.provider_credentials import store
    from hermes_cli.agent_platform.provider_worker import resolution

    captured = {}

    def default_root(*, hermes_home=None):
        captured["hermes_home_arg"] = hermes_home
        return canonical_root

    def read_status(root, *, now):
        captured["credential_root"] = root
        captured["credential_status_now"] = now
        return _ready_governed_credential_status(now)

    def resolve_worker(request):
        captured["worker_request"] = request
        return SimpleNamespace(profile_id=request.worker_profile_id)

    monkeypatch.setattr(store, "default_openai_codex_credential_store_root", default_root)
    monkeypatch.setattr(store, "read_openai_codex_credential_status", read_status)
    monkeypatch.setattr(resolution, "resolve_provider_worker_profile", resolve_worker)
    return captured


def _ready_executor_provider_payload(profile_name=_EXECUTOR_PROFILE) -> dict:
    return {
        "ok": True,
        "provider": "openai-codex",
        "model": "gpt-5.5",
        "api_mode": "codex_responses",
        "credential_profile_id": "openai-codex.primary",
        "credential_policy_revision": "provider-runtime-v1.provider-worker-v1.provider-credential-v1",
        "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
        "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
        "executor_config_source": "test",
        "executor_profile": profile_name,
    }


def _ready_worker_credential_probe() -> dict:
    return {
        "ok": True,
        "probe_status": "passed",
        "credential_profile_id": "openai-codex.primary",
        "credential_resolution_source": "canonical_governed_home",
        "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
        "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
        "legacy_auth_json_used": False,
        "API_key_fallback_used": False,
        "credential_pool_fallback_used": False,
        "legacy_refresh_fallback": False,
        "credential_refresh_calls_per_request_maximum": 0,
    }


def _write_fixture_file(root: Path, relative_path: str, text: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _source_materialization_authority(
    workspace: Path,
    *,
    allowed_paths: tuple[str, ...],
    forbidden_paths: tuple[str, ...] = (),
):
    from tools import governed_workpacket_file_guard as file_guard

    return file_guard.WorkPacketFileAuthority(
        ticket_id="P18.9.1",
        work_packet_id="WP-P18-9-1-R0001-123456789abc",
        work_packet_SHA256="a" * 64,
        ticket_spec_SHA256="b" * 64,
        projection_SHA256="c" * 64,
        allowed_paths=allowed_paths,
        forbidden_paths=forbidden_paths,
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(strict=True),
    )


def _persist_started_execution_record(pr, projected, run_id: int) -> None:
    authority = projected
    if "projection_SHA256" not in authority or "dependency_plan_SHA256" not in authority:
        authority = projection.load_kanban_projection_record(
            ticket_id=projected.get("ticket_id") or "P18.9.0"
        )
    assert authority is not None
    ticket_id = authority["ticket_id"]
    action_ids = pr.governed_ticket_lifecycle_action_ids(ticket_id)
    record = pr._build_execution_start_authorization_record(
        request=pr.CurrentTicketExecutionStartRequest(
            human_authorization_text=f"Start {ticket_id} execution now",
            project_id="PEPPER",
            ticket_id=ticket_id,
            next_action_id=action_ids["execution_start"],
        ),
        projection=authority,
        provider_readiness=_ready_executor_provider_payload(authority["assignee_profile"]),
    )
    record = pr._finalize_execution_start_record(
        record,
        dispatch_result={
            "start_status": "started",
            "blocker_code": None,
            "blocker_detail": None,
            "dispatch_performed": True,
            "execution_started": True,
            "worker_execution": True,
            "worker_process_started": True,
            "worker_pid_recorded": True,
            "Kanban_dispatch": True,
            "kanban_task_status": "running",
            "kanban_run_id": run_id,
            "workspace_path": "synthetic-workspace",
            "workspace_created": True,
        },
    )
    pr._persist_execution_start_record(record)


def _force_projected_execution_failure(
    *,
    projected: dict,
    pr,
    kanban_db,
    monkeypatch,
    task_skills=(),
) -> int:
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        claimed = kanban_db.claim_task(
            conn,
            projected["kanban_task_id"],
            claimer="pepper-worker-start-action",
        )
        assert claimed is not None
        workspace = kanban_db.resolve_workspace(claimed, board=projected["kanban_board_slug"])
        kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
        kanban_db._set_worker_pid(conn, claimed.id, 12628)
        old_started = int(time.time()) - 7200
        old_expiry = int(time.time()) - 6300
        conn.execute(
            "UPDATE tasks SET started_at = ?, claim_expires = ?, "
            "last_heartbeat_at = NULL, skills = ? WHERE id = ?",
            (
                old_started,
                old_expiry,
                json.dumps(list(task_skills)),
                claimed.id,
            ),
        )
        conn.execute(
            "UPDATE task_runs SET started_at = ?, claim_expires = ?, "
            "last_heartbeat_at = NULL WHERE id = ?",
            (old_started, old_expiry, claimed.current_run_id),
        )
        conn.commit()
        run_id = int(claimed.current_run_id)
    finally:
        conn.close()
    _persist_started_execution_record(pr, projected, run_id)
    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda _pid: False)
    return run_id


def _force_additional_projected_crashed_run(
    *,
    projected: dict,
    pr,
    kanban_db,
    monkeypatch,
    pid: int = 34692,
) -> int:
    previous = pr.build_workflow_control_snapshot()
    assert previous["workflow_status"] == "execution_failed"
    assert previous["recovery_state"] == "recovery_required"
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.unblock_task(conn, projected["kanban_task_id"])
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        claimed = kanban_db.claim_task(
            conn,
            projected["kanban_task_id"],
            claimer="pepper-worker-retry-start-action",
        )
        assert claimed is not None
        workspace = kanban_db.resolve_workspace(claimed, board=projected["kanban_board_slug"])
        kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
        kanban_db._set_worker_pid(conn, claimed.id, pid)
        old_started = int(time.time()) - 7200
        old_expiry = int(time.time()) - 6300
        conn.execute(
            "UPDATE tasks SET started_at = ?, claim_expires = ?, "
            "last_heartbeat_at = NULL, skills = ? WHERE id = ?",
            (old_started, old_expiry, json.dumps([]), claimed.id),
        )
        conn.execute(
            "UPDATE task_runs SET started_at = ?, claim_expires = ?, "
            "last_heartbeat_at = NULL WHERE id = ?",
            (old_started, old_expiry, claimed.current_run_id),
        )
        conn.commit()
        run_id = int(claimed.current_run_id)
    finally:
        conn.close()
    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda observed_pid: int(observed_pid) != pid)
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["recovery_state"] == "recovery_required"
    assert str(pid) in workflow["worker_lifecycle"]["blocker_detail"]
    return run_id


def _approve_current_ticket() -> tuple[dict, dict]:
    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_p18_9_0_ticket(workflow=_workflow())
    approved = pr.apply_approval_decision(
        "P18.9.0",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )
    assert approved["status"] == "approved"
    generation = bridge.load_p18_9_0_generation_record()
    decision = bridge.load_p18_9_0_approval_decision_record()
    assert generation is not None
    assert decision is not None
    return generation, decision


def _install_implementation_profile(monkeypatch, home, **overrides) -> None:
    data = {
        "name": _IMPLEMENTATION_PROFILE,
        "description": "Pepper frontend product implementation execution profile",
        "cli_toolsets": ("pepper_repository", "file", "no_mcp"),
    }
    data.update(overrides)
    _install_execution_profile(monkeypatch, home, **data)


def _approve_next_ticket() -> tuple[dict, dict]:
    from hermes_cli.agent_platform import product_runtime as pr

    bridge.generate_current_ticket(workflow=_next_ticket_workflow())
    approved = pr.apply_approval_decision(
        "P18.9.1",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )
    assert approved["status"] == "approved"
    generation = bridge.load_generation_record(ticket_id="P18.9.1")
    decision = bridge.load_approval_decision_record(ticket_id="P18.9.1")
    assert generation is not None
    assert decision is not None
    return generation, decision


def _approved_workflow_for_record(record: dict) -> dict:
    return {
        **_next_ticket_workflow(),
        **bridge.generated_record_to_workflow_overlay(record),
        "active_execution_count": 0,
        "execution_state": "no_active_executions",
    }


def _project_next_ticket_direct():
    generation = bridge.load_generation_record(ticket_id="P18.9.1")
    assert generation is not None
    return projection.project_current_approved_workpacket_to_kanban(
        workflow=_approved_workflow_for_record(generation),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
    )


def _projection_authority_record(projected: dict) -> dict:
    authority = projection.load_kanban_projection_record(
        ticket_id=projected["ticket_id"],
    )
    assert authority is not None
    return authority


def _closed_p18_9_0_with_projected_p18_9_1(projection_home, monkeypatch):
    _install_execution_profile(monkeypatch, projection_home)
    _generation, _projected, _started, _review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    accepted = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )
    assert accepted["P18_9_0_closed"] is True

    _install_implementation_profile(monkeypatch, projection_home)
    _approve_next_ticket()
    projected = _project_next_ticket_direct()
    return pr, projected, _projection_authority_record(projected)


def _patch_synthetic_scratch_materialization(monkeypatch, pr) -> None:
    def materialize(_projection, workspace, *, env_overlay=None, source_root=None):
        _ = env_overlay, source_root
        workspace_path = Path(workspace)
        manifest_path = workspace_path / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "source_materialized": True,
            "dependency_substrate_materialized": True,
            "dependency_substrate_kind": "synthetic_test_fixture",
            "dependency_install_performed": False,
            "canonical_package_lock_materialized": False,
            "manifest_path": str(manifest_path),
            "product_diff_excluded_roots": ["2_products/pepper-agent/node_modules"],
        }
        manifest_path.write_text(
            json.dumps(record, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return record

    monkeypatch.setattr(pr, "_materialize_pepper_governed_scratch_source", materialize)


def _start_p18_9_1_execution(pr, monkeypatch, *, pid: int = 5321) -> dict:
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda _projection_record, *, enabled=True: _ready_worker_credential_probe(),
    )
    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: pid,
    )
    assert result["start_status"] == "started"
    assert (Path(result["workspace_path"]) / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).is_file()
    assert result["kanban_run_id"] is not None
    return result


def _claim_next_projected_run(kanban_db, projected: dict, *, pid: int) -> int:
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        if task.status in {"blocked", "scheduled"}:
            assert kanban_db.unblock_task(conn, projected["kanban_task_id"])
        claimed = kanban_db.claim_task(
            conn,
            projected["kanban_task_id"],
            claimer="pepper-worker-start-action",
        )
        assert claimed is not None
        workspace = kanban_db.resolve_workspace(
            claimed,
            board=projected["kanban_board_slug"],
        )
        kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
        kanban_db._set_worker_pid(conn, claimed.id, pid)
        return int(claimed.current_run_id)
    finally:
        conn.close()


def _block_projected_run(
    kanban_db,
    projected: dict,
    run_id: int,
    *,
    reason: str,
    kind: str | None,
) -> None:
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.block_task(
            conn,
            projected["kanban_task_id"],
            reason=reason,
            kind=kind,
            expected_run_id=run_id,
        )
    finally:
        conn.close()


def _finish_projected_run_as_terminal(
    kanban_db,
    projected: dict,
    run_id: int,
    *,
    status: str,
    outcome: str,
    summary: str,
) -> None:
    now = int(time.time())
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        conn.execute(
            "UPDATE tasks SET status = 'blocked', current_run_id = NULL, "
            "worker_pid = NULL, claim_lock = NULL, claim_expires = NULL, "
            "last_failure_error = ? WHERE id = ? AND current_run_id = ?",
            (summary, projected["kanban_task_id"], run_id),
        )
        conn.execute(
            "UPDATE task_runs SET status = ?, outcome = ?, summary = ?, "
            "error = ?, ended_at = ?, claim_lock = NULL, claim_expires = NULL, "
            "worker_pid = NULL WHERE id = ?",
            (status, outcome, summary, summary, now, run_id),
        )
        conn.commit()
    finally:
        conn.close()


def _force_p18_9_1_blocked_run_4(pr, kanban_db, projected: dict, monkeypatch) -> int:
    first = _start_p18_9_1_execution(pr, monkeypatch, pid=6401)
    _block_projected_run(
        kanban_db,
        projected,
        first["kanban_run_id"],
        reason="synthetic P18.9.1 run 2 blocked",
        kind="needs_input",
    )
    run_3 = _claim_next_projected_run(kanban_db, projected, pid=6402)
    _block_projected_run(
        kanban_db,
        projected,
        run_3,
        reason="synthetic P18.9.1 run 3 blocked",
        kind="capability",
    )
    run_4 = _claim_next_projected_run(kanban_db, projected, pid=6403)
    assert run_4 == 4
    _block_projected_run(
        kanban_db,
        projected,
        run_4,
        reason="WORKSPACE_PATH_ESCAPE: worker workspace path escaped canonical repo",
        kind="transient",
    )
    return run_4


def _queued_workflow_for_projection(projected: dict) -> dict:
    authority = _projection_authority_record(projected)
    generation = bridge.load_generation_record(ticket_id=projected["ticket_id"])
    assert generation is not None
    workflow = _approved_workflow_for_record(generation)
    workflow.update(projection.kanban_projection_to_workflow_overlay(authority))
    workflow["active_execution_count"] = 0
    workflow["remaining_blockers"] = []
    workflow["blocker_count"] = 0
    return workflow


def _synthetic_implementation_contract(label: str) -> dict[str, object]:
    return {
        "ticket_type": "implementation",
        "objective": f"Implement synthetic governed surface {label}.",
        "predecessor_evidence": ["Synthetic predecessor accepted IA handoff."],
        "information_architecture": [f"CONTROL: Synthetic {label}"],
        "required_surfaces": [f"Synthetic surface {label}"],
        "allowed_paths": ["2_products/pepper-agent/web/src/agent-platform/shell/**"],
        "allowed_actions": ["Reuse existing synthetic shell seam."],
        "constraints": ["Do not create a second synthetic router."],
        "tasks": [f"Implement synthetic task {label} through the existing seam."],
        "acceptance_criteria": [
            f"Synthetic surface {label} is implemented through the existing seam."
        ],
        "validation_steps": [
            f"V1: Human review confirms synthetic contract {label} => The generated TicketSpec is implementation-oriented."
        ],
        "completion_verdict": f"synthetic_{label.lower()}_implementation_ready",
    }


def _synthetic_implementation_target(ticket_id: str = "P99.2"):
    return bridge.GovernedTicketGenerationTarget(
        project_id="PEPPER",
        project_name="Pepper",
        macroproject_id="P99.0",
        macroproject_title="Synthetic Implementation Macroproject",
        ticket_id=ticket_id,
        ticket_title="Synthetic Future Projection",
        next_action_id=bridge.canonical_generation_action_id(ticket_id),
        approval_next_action_id=bridge.approval_action_id(ticket_id),
        approved_no_execution_next_action_id=bridge.approved_no_execution_action_id(ticket_id),
        revise_next_action_id=bridge.revise_action_id(ticket_id),
        canonical_roadmap_authority="synthetic_test_roadmap",
        roadmap_authority_path="synthetic-roadmap.md",
        roadmap_authority_section="Synthetic roadmap",
        dependency_ticket_ids=(),
        predecessor_ticket_id=None,
        readiness_state="synthetic_ready",
        authority_source="synthetic_contract_fixture",
        ticket_contract=_synthetic_implementation_contract("Projection"),
    )


def _synthetic_workflow_for_target(target) -> dict:
    return {
        "project_id": target.project_id,
        "project_name": target.project_name,
        "macroproject_id": target.macroproject_id,
        "macroproject_title": target.macroproject_title,
        "current_ticket_id": None,
        "next_ticket_id": target.ticket_id,
        "next_ticket_title": target.ticket_title,
        "workflow_status": "completed",
        "P18_9_ready": True,
        "next_action": {
            "id": target.next_action_id,
            "target_ticket_id": target.ticket_id,
            "target_ticket_title": target.ticket_title,
        },
    }


def _project_via_runtime():
    from hermes_cli.agent_platform import product_runtime as pr

    return pr.project_current_approved_workpacket_to_kanban(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="P18_9_0_APPROVED_NO_EXECUTION",
    )


def test_scratch_source_materialization_copies_frontend_readable_closure(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package-lock.json",
        "must not be materialized\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/vitest.config.ts",
        "export default {};\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/App.tsx",
        "export const app = 'canonical';\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/shared/readable.ts",
        "export const shared = true;\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/agent-platform/shell/navigation.ts",
        "export const nav = 'canonical';\n",
    )
    _write_fixture_file(
        workspace,
        "2_products/pepper-agent/web/src/agent-platform/shell/stale.patch",
        "stale worker artifact\n",
    )
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/web/src/App.tsx",
            "2_products/pepper-agent/web/src/agent-platform/shell/**",
        ),
    )

    record = pr._materialize_workpacket_scratch_source_tree(
        authority,
        source_root=source_root,
    )

    scratch_app = workspace / "2_products/pepper-agent/web/src/App.tsx"
    canonical_app = source_root / "2_products/pepper-agent/web/src/App.tsx"
    assert scratch_app.read_text(encoding="utf-8") == "export const app = 'canonical';\n"
    assert (workspace / "2_products/pepper-agent/web/src/shared/readable.ts").is_file()
    assert (workspace / "2_products/pepper-agent/web/package.json").is_file()
    assert not (workspace / "2_products/pepper-agent/web/package-lock.json").exists()
    assert not (
        workspace / "2_products/pepper-agent/web/src/agent-platform/shell/stale.patch"
    ).exists()
    assert record["source_materialized"] is True
    assert record["canonical_package_lock_materialized"] is False
    assert record["dependency_install_performed"] is False
    assert "2_products/pepper-agent/web/src" in record["readable_source_roots"]
    assert record["writable_allowed_paths"] == list(authority.allowed_paths)
    assert Path(record["manifest_path"]).is_file()

    scratch_app.write_text("export const app = 'scratch edit';\n", encoding="utf-8")

    assert canonical_app.read_text(encoding="utf-8") == "export const app = 'canonical';\n"


def test_scratch_source_materialization_copies_python_allowed_files(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/hermes_cli/agent_platform/example.py",
        "VALUE = 'canonical'\n",
    )
    _write_fixture_file(
        workspace,
        "2_products/pepper-agent/hermes_cli/agent_platform/new_file.py",
        "stale retry file\n",
    )
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/hermes_cli/agent_platform/example.py",
            "2_products/pepper-agent/hermes_cli/agent_platform/new_file.py",
        ),
    )

    record = pr._materialize_workpacket_scratch_source_tree(
        authority,
        source_root=source_root,
    )

    copied = workspace / "2_products/pepper-agent/hermes_cli/agent_platform/example.py"
    missing = workspace / "2_products/pepper-agent/hermes_cli/agent_platform/new_file.py"
    assert copied.read_text(encoding="utf-8") == "VALUE = 'canonical'\n"
    assert not missing.exists()
    assert missing.parent.is_dir()
    assert "2_products/pepper-agent/hermes_cli/agent_platform/new_file.py" in record[
        "missing_source_paths"
    ]


def test_scratch_source_materialization_skips_dependency_and_lockfile_noise(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package-lock.json",
        "must not be materialized\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/node_modules/vitest/vitest.mjs",
        "must not be source-materialized\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/agent-platform/shell/component.test.tsx",
        "test('scratch source', () => {})\n",
    )
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/**",),
    )

    record = pr._materialize_workpacket_scratch_source_tree(
        authority,
        source_root=source_root,
    )

    assert (workspace / "2_products/pepper-agent/web/package.json").is_file()
    assert (
        workspace / "2_products/pepper-agent/web/src/agent-platform/shell/component.test.tsx"
    ).is_file()
    assert not (workspace / "2_products/pepper-agent/web/package-lock.json").exists()
    assert not (workspace / "2_products/pepper-agent/web/node_modules").exists()
    assert record["canonical_package_lock_materialized"] is False
    assert record["dependency_install_performed"] is False


def test_workpacket_validation_discovers_scratch_only_frontend_tests(
    tmp_path,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr
    from tools import workpacket_validation_tool as validation_tool

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/agent-platform/shell/navigation.ts",
        "export const nav = true;\n",
    )
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/web/src/agent-platform/shell/scratch-only.test.tsx",
        ),
    )
    pr._materialize_workpacket_scratch_source_tree(authority, source_root=source_root)
    scratch_test = (
        workspace
        / "2_products/pepper-agent/web/src/agent-platform/shell/scratch-only.test.tsx"
    )
    scratch_test.write_text("test('scratch only', () => {})\n", encoding="utf-8")
    node = tmp_path / "node"
    vitest = tmp_path / "vitest.mjs"
    node.write_text("", encoding="utf-8")
    vitest.write_text("", encoding="utf-8")
    monkeypatch.setattr(validation_tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        validation_tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, _entry: vitest,
    )
    work_packet = SimpleNamespace(
        validation_steps=(
            SimpleNamespace(
                validation_id="V2",
                description="Focused frontend tests validate scratch state.",
                expected_result="The focused frontend tests pass.",
                command=None,
            ),
        ),
        source_ticket=SimpleNamespace(ticket_type="implementation"),
    )

    specs = validation_tool.build_governed_validation_command_specs(
        authority,
        work_packet,
    )

    assert len(specs) == 1
    spec = specs[0]
    assert spec.working_directory == (
        workspace / "2_products/pepper-agent/web"
    ).resolve().as_posix()
    assert spec.effective_argv[:3] == (node.as_posix(), vitest.as_posix(), "run")
    assert spec.effective_argv[3:] == (
        "src/agent-platform/shell/scratch-only.test.tsx",
    )


def test_dependency_substrate_materializes_snapshot_and_runs_scratch_validation(
    tmp_path,
    monkeypatch,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr
    from tools import workpacket_validation_tool as validation_tool

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/package-lock.json",
        json.dumps({"lockfileVersion": 3}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/agent-platform/shell/scratch-validation.test.ts",
        "export const SCRATCH_MARKER = 'from scratch';\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/vitest/vitest.mjs",
        "import os\n"
        "import pathlib\n"
        "import sys\n"
        "print('FAKE_VITEST')\n"
        "print('cwd=' + os.getcwd())\n"
        "for arg in sys.argv[2:]:\n"
        "    print(pathlib.Path(arg).read_text(encoding='utf-8'))\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/vite/package.json",
        json.dumps({"name": "vite"}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/react/package.json",
        json.dumps({"name": "react"}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/react-dom/package.json",
        json.dumps({"name": "react-dom"}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/@vitejs/plugin-react/package.json",
        json.dumps({"name": "@vitejs/plugin-react"}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/.cache/ignored.txt",
        "cache noise\n",
    )
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/web/src/agent-platform/shell/scratch-validation.test.ts",
        ),
    )
    work_packet = SimpleNamespace(
        validation_steps=(
            SimpleNamespace(
                validation_id="V-FRONTEND",
                description="Focused frontend tests validate scratch state.",
                expected_result="The focused frontend tests pass.",
                command=None,
            ),
        ),
        source_ticket=SimpleNamespace(ticket_type="implementation"),
    )
    monkeypatch.setattr(
        validation_tool,
        "_resolve_node_executable",
        lambda: Path(sys.executable).resolve(strict=True),
    )

    pr._materialize_workpacket_scratch_source_tree(authority, source_root=source_root)
    record = pr._materialize_workpacket_dependency_substrate(
        authority,
        work_packet,
        source_root=source_root,
    )

    scratch_node_modules = workspace / "2_products/pepper-agent/node_modules"
    scratch_vitest = scratch_node_modules / "vitest/vitest.mjs"
    assert record["dependency_substrate_materialized"] is True
    assert record["dependency_substrate_kind"] == "physical_node_modules_snapshot"
    assert record["dependency_install_performed"] is False
    assert record["product_diff_excluded_roots"] == [
        "2_products/pepper-agent/node_modules",
    ]
    assert scratch_vitest.is_file()
    assert not scratch_vitest.is_symlink()
    assert not (scratch_node_modules / ".cache").exists()
    substrate = record["dependency_substrates"][0]
    assert substrate["canonical_package_lock_SHA256"] is not None
    assert substrate["canonical_package_lock_materialized"] is False
    assert substrate["dependency_install_performed"] is False

    specs = validation_tool.build_governed_validation_command_specs(
        authority,
        work_packet,
    )
    assert len(specs) == 1
    spec = specs[0]
    assert spec.runtime_available is True
    result = json.loads(validation_tool._run_command(authority, spec))

    package_dir = workspace / "2_products/pepper-agent/web"
    stdout = result["stdout"]["retained_text"]
    assert result["success"] is True
    assert result["process_started"] is True
    assert result["exit_code"] == 0
    assert result["command"]["working_directory"] == package_dir.as_posix()
    assert "FAKE_VITEST" in stdout
    assert package_dir.as_posix() in stdout.replace("\\", "/")
    assert "SCRATCH_MARKER" in stdout


def test_dependency_substrate_missing_vitest_fails_before_worker_spawn(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/agent-platform/shell/scratch-validation.test.ts",
        "test('missing substrate', () => {})\n",
    )
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/web/src/agent-platform/shell/scratch-validation.test.ts",
        ),
    )
    work_packet = SimpleNamespace(
        validation_steps=(
            SimpleNamespace(
                validation_id="V-FRONTEND",
                description="Focused frontend tests validate scratch state.",
                expected_result="The focused frontend tests pass.",
                command=None,
            ),
        ),
        source_ticket=SimpleNamespace(ticket_type="implementation"),
    )

    pr._materialize_workpacket_scratch_source_tree(authority, source_root=source_root)
    with pytest.raises(pr.ProductRuntimeDependencyGap) as exc_info:
        pr._materialize_workpacket_dependency_substrate(
            authority,
            work_packet,
            source_root=source_root,
        )

    assert exc_info.value.external_code == pr.IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP
    assert exc_info.value.dependency_code == pr.DEPENDENCY_SOURCE_NOT_FOUND


def test_dependency_substrate_excludes_workspace_package_reparse_points(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/web/src/agent-platform/shell/scratch-validation.test.ts",
        "test('workspace link exclusion', () => {})\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/vitest/vitest.mjs",
        "#!/usr/bin/env node\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/node_modules/vite/package.json",
        json.dumps({"name": "vite"}),
    )
    workspace_package = source_root / "2_products/pepper-agent/apps/shared"
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/apps/shared/package.json",
        json.dumps({"name": "@hermes/shared"}),
    )
    linked_package = source_root / "2_products/pepper-agent/node_modules/@hermes/shared"
    linked_package.parent.mkdir(parents=True, exist_ok=True)
    try:
        linked_package.symlink_to(workspace_package, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"directory symlink creation unavailable: {exc}")
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            "2_products/pepper-agent/web/src/agent-platform/shell/scratch-validation.test.ts",
        ),
    )
    work_packet = SimpleNamespace(
        validation_steps=(
            SimpleNamespace(
                validation_id="V-FRONTEND",
                description="Focused frontend tests validate scratch state.",
                expected_result="The focused frontend tests pass.",
                command=None,
            ),
        ),
        source_ticket=SimpleNamespace(ticket_type="implementation"),
    )

    pr._materialize_workpacket_scratch_source_tree(authority, source_root=source_root)
    record = pr._materialize_workpacket_dependency_substrate(
        authority,
        work_packet,
        source_root=source_root,
    )

    substrate = record["dependency_substrates"][0]
    assert {
        "relative_path": "@hermes/shared",
        "resolved_target": str(workspace_package.resolve(strict=True)),
        "reason": "workspace_package_reparse_point_excluded",
    } in substrate["excluded_reparse_directories"]
    assert not (
        workspace / "2_products/pepper-agent/node_modules/@hermes/shared"
    ).exists()


def test_current_ticket_lifecycle_binding_derives_actions_and_paths(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    generation, _decision = _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli.agent_platform import product_runtime as pr

    binding = pr.resolve_current_ticket_lifecycle_binding(projection_record=projected)

    assert binding.ticket_id == "P18.9.0"
    assert binding.ticket_action_token == "P18_9_0"
    assert binding.ticket_hyphen_token == "P18-9-0"
    assert binding.ticket_spec_sha256 == generation["ticket_spec_SHA256"]
    assert binding.work_packet_id == generation["work_packet_id"]
    assert binding.work_packet_sha256 == generation["work_packet_SHA256"]
    assert binding.work_packet_compilation_count == 1
    assert binding.execution_start_next_action_id == "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert binding.execution_recovery_next_action_id == "RECOVER_P18_9_0_EXECUTION"
    assert binding.retry_start_next_action_id == "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    assert binding.review_prepare_next_action_id == "PREPARE_P18_9_0_REVIEW"
    assert binding.review_acceptance_next_action_id == "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"
    assert binding.monitor_execution_next_action_id == "MONITOR_P18_9_0_EXECUTION"
    assert binding.approved_no_execution_next_action_id == "P18_9_0_APPROVED_NO_EXECUTION"
    authority = projection.load_p18_9_0_kanban_projection_record()
    assert authority is not None
    assert pr.validate_governed_ticket_lifecycle_projection_authority(authority) == binding

    assert pr.governed_ticket_lifecycle_action_ids("P18.10.2")["retry_start"] == (
        "START_P18_10_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    )
    assert pr.p18_9_0_execution_start_record_path() == (
        projection_home
        / "agent-platform"
        / "pepper-worker-start-action"
        / "P18.9.0.execution-start.json"
    )
    assert pr.p18_9_0_review_acceptance_history_path() == (
        projection_home
        / "agent-platform"
        / "pepper-review-human-acceptance-action"
        / "P18.9.0.review-acceptance.history.jsonl"
    )


def _prepare_completed_review_package(monkeypatch):
    generation, _decision = _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda projection, enabled=True: _ready_worker_credential_probe(),
    )
    started = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        ok = kanban_db.complete_task(
            conn,
            projected["kanban_task_id"],
            summary=(
                "Summary\nP18.9.0 inventory, IA decision, and acceptance contract "
                "prepared.\nFiles inspected\n- bounded Pepper authorities\nFiles "
                "modified\n- none\nTests/commands run\n- none\nDecisions made\n- "
                "read-only handoff\nLimitations\n- awaits human review acceptance"
            ),
            metadata={
                "files_inspected": ["2_products/pepper-agent/hermes_cli/agent_platform/product_runtime.py"],
                "files_modified": [],
                "tests_run": [],
                "Git_mutation": False,
            },
            expected_run_id=started["kanban_run_id"],
        )
        assert ok is True
    finally:
        conn.close()
    review = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="PREPARE_P18_9_0_REVIEW",
    )
    return generation, projected, started, review


def _drifted_acceptance_contract(pr, contract: dict) -> dict:
    drifted = dict(contract)
    drifted["acceptance_criteria"] = [
        *contract["acceptance_criteria"],
        "Synthetic current-builder-only criterion.",
    ]
    drifted["criteria_revision_SHA256"] = pr._criteria_revision_digest(drifted)
    drifted["acceptance_contract_SHA256"] = pr._acceptance_contract_digest(drifted)
    return drifted


def test_projection_requires_approved_ticket(projection_home, monkeypatch) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    bridge.generate_p18_9_0_ticket(workflow=_workflow())

    with pytest.raises(projection.WorkPacketKanbanProjectionConflict):
        _project_via_runtime()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        assert kanban_db.list_tasks(conn) == []
    finally:
        conn.close()


def test_projection_preserves_workpacket_and_creates_ready_kanban_task(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    generation, decision = _approve_current_ticket()

    result = _project_via_runtime()
    record = projection.load_p18_9_0_kanban_projection_record()

    assert result["projection_status"] == "projected"
    assert result["ticket_spec_SHA256"] == generation["ticket_spec_SHA256"]
    assert result["work_packet_id"] == generation["work_packet_id"]
    assert result["work_packet_SHA256"] == generation["work_packet_SHA256"]
    assert result["WorkPacket_compilation_count"] == 1
    assert result["dependency_admission"]["policy_id"] == projection.DEPENDENCY_AWARE_QUEUE_POLICY_ID
    assert result["dependency_admission"]["decision"] == "admit"
    assert result["dependency_admission"]["dependency_plan_reused"] is True
    assert result["dependency_admission"]["dependency_bypass"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["profile_assignment_policy_id"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_ID
    assert result["profile_assignment_basis"] == "governed_role_taxonomy"
    assert result["assignee_profile"] == _EXECUTOR_PROFILE
    assert result["selected_profile"] == _EXECUTOR_PROFILE
    assert result["execution_profile_role"] == "architecture_product"
    assert result["selected_role"] == "architecture_product"
    assert result["selection_rationale"] == "deterministic_single_governed_role_match"
    assert result["profile_toolsets"] == ["pepper_repository"]
    assert result["lead_agent_auto_assigned"] is False
    assert result["ticket_architect_executor_distinct"] is True
    assert result["human_profile_selection_required"] is False
    assert result["concurrent_workers_for_ticket"] == 1
    assert result["task_max_retries"] == 1
    assert result["task_skills"] == []
    assert result["semantic_capabilities"] == ["codebase-inspection"]
    assert result["capability_resolution"] == [
        {
            "semantic_capability": "codebase-inspection",
            "resolved_surface": "profile_toolset",
            "toolset": "pepper_repository",
            "hermes_task_skill": None,
        }
    ]
    assert result["Kanban_canonical_authority"] is False
    assert record is not None
    assert record["approval_publication_SHA256"] == decision["approval_publication_SHA256"]

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=result["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, result["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert task.assignee == _EXECUTOR_PROFILE
        assert task.skills == []
        assert task.max_retries == 1
        assert task.workspace_kind == "scratch"
        assert task.workspace_path is None
        assert kanban_db.list_runs(conn, task.id) == []
        body = json.loads(task.body or "{}")
        assert body["WorkPacket_ID"] == generation["work_packet_id"]
        assert body["WorkPacket_SHA256"] == generation["work_packet_SHA256"]
        assert body["TicketSpec_SHA256"] == generation["ticket_spec_SHA256"]
        assert body["provisional_execution_projection"] is True
        assert body["Kanban_canonical_authority"] is False
        assert body["assignee_profile"] == _EXECUTOR_PROFILE
        assert body["selected_profile"] == _EXECUTOR_PROFILE
        assert body["profile_assignment_policy_id"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_ID
        assert body["execution_profile_role"] == "architecture_product"
        assert body["selected_role"] == "architecture_product"
        assert body["selection_rationale"] == "deterministic_single_governed_role_match"
        assert body["profile_toolsets"] == ["pepper_repository"]
        assert body["task_skills"] == []
        assert body["semantic_capabilities"] == ["codebase-inspection"]
        assert body["capability_resolution"] == result["capability_resolution"]
        assert body["lead_agent_auto_assigned"] is False
        assert body["ticket_architect_executor_distinct"] is True
    finally:
        conn.close()


def test_generic_projection_preserves_p18_9_1_workpacket_and_creates_ready_task(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    generation, decision = _approve_next_ticket()

    resolved = projection.resolve_current_approved_workpacket_projection(
        workflow=_approved_workflow_for_record(generation),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
    )
    result = _project_next_ticket_direct()
    replay = _project_next_ticket_direct()
    record = projection.load_kanban_projection_record(ticket_id="P18.9.1")

    assert resolved["ticket_id"] == "P18.9.1"
    assert resolved["ticket_spec_SHA256"] == generation["ticket_spec_SHA256"]
    assert resolved["work_packet_id"] == generation["work_packet_id"]
    assert resolved["work_packet_SHA256"] == generation["work_packet_SHA256"]
    assert resolved["approval_publication_SHA256"] == decision["approval_publication_SHA256"]
    assert result["projection_status"] == "projected"
    assert result["ticket_id"] == "P18.9.1"
    assert result["ticket_spec_SHA256"] == generation["ticket_spec_SHA256"]
    assert result["work_packet_id"] == generation["work_packet_id"]
    assert result["work_packet_SHA256"] == generation["work_packet_SHA256"]
    assert result["WorkPacket_compilation_count"] == 1
    assert result["assignee_profile"] == _IMPLEMENTATION_PROFILE
    assert result["selected_profile"] == _IMPLEMENTATION_PROFILE
    assert result["execution_profile_role"] == "implementation_product"
    assert result["selected_role"] == "implementation_product"
    assert result["profile_toolsets"] == ["pepper_repository", "file"]
    assert result["required_write_toolsets"] == ["file"]
    assert result["required_capabilities"] == ["codebase-inspection", "codebase-edit"]
    assert result["ticket_execution_requirements"]["ticket_type"] == "implementation"
    assert result["profile_assignment_policy_id"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_ID
    assert result["profile_assignment_policy_revision"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_REVISION
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["next_action"]["id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert replay["idempotent_replay"] is True
    assert replay["kanban_task_id"] == result["kanban_task_id"]
    assert projection.kanban_projection_record_path_for_ticket("P18.9.1") == (
        projection_home / "agent-platform" / "pepper-workpacket-kanban-projection" / "P18.9.1.json"
    )
    assert record is not None
    assert record["approval_publication_SHA256"] == decision["approval_publication_SHA256"]
    assert record["dispatch_performed"] is False
    assert record["worker_execution"] is False

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=result["kanban_board_slug"])
    try:
        tasks = kanban_db.list_tasks(conn)
        task = kanban_db.get_task(conn, result["kanban_task_id"])
        assert [task.id for task in tasks] == [result["kanban_task_id"]]
        assert task is not None
        assert task.status == "ready"
        assert task.assignee == _IMPLEMENTATION_PROFILE
        assert kanban_db.list_runs(conn, task.id) == []
        body = json.loads(task.body or "{}")
        assert body["ticket_id"] == "P18.9.1"
        assert body["WorkPacket_ID"] == generation["work_packet_id"]
        assert body["WorkPacket_SHA256"] == generation["work_packet_SHA256"]
        assert body["TicketSpec_SHA256"] == generation["ticket_spec_SHA256"]
        assert body["execution_profile_role"] == "implementation_product"
        assert body["profile_toolsets"] == ["pepper_repository", "file"]
        assert body["required_write_toolsets"] == ["file"]
        assert body["required_capabilities"] == ["codebase-inspection", "codebase-edit"]
    finally:
        conn.close()


def test_synthetic_future_ticket_projection_uses_generic_primitive(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    target = _synthetic_implementation_target()
    bridge.generate_current_ticket(
        workflow=_synthetic_workflow_for_target(target),
        target=target,
    )
    approval = bridge.apply_ticket_approval_decision(
        ticket_id=target.ticket_id,
        decision="approve",
        actor="synthetic-human",
    )
    generation = bridge.load_generation_record(ticket_id=target.ticket_id)
    assert generation is not None
    workflow = {
        **_synthetic_workflow_for_target(target),
        **bridge.generated_record_to_workflow_overlay(generation),
        "active_execution_count": 0,
        "execution_state": "no_active_executions",
    }

    result = projection.project_current_approved_workpacket_to_kanban(
        workflow=workflow,
        requested_project_id="PEPPER",
        requested_ticket_id=target.ticket_id,
        requested_next_action_id="P99_2_APPROVED_NO_EXECUTION",
    )

    assert result["ticket_id"] == target.ticket_id
    assert result["ticket_spec_SHA256"] == generation["ticket_spec_SHA256"]
    assert result["work_packet_id"] == generation["work_packet_id"]
    assert result["work_packet_SHA256"] == generation["work_packet_SHA256"]
    assert result["assignee_profile"] == _IMPLEMENTATION_PROFILE
    assert result["execution_profile_role"] == "implementation_product"
    assert result["approval_publication_SHA256"] == approval["authority"]["approval_publication_SHA256"]
    assert result["dispatch_performed"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["next_action"]["id"] == "START_P99_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"

    overlay = projection.kanban_projection_to_workflow_overlay(
        projection.load_kanban_projection_record(ticket_id=target.ticket_id)
    )
    assert overlay["workflow_status"] == "queued"
    assert overlay["next_action"]["id"] == "START_P99_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"


def test_legacy_semantic_task_skill_projection_still_validates_as_evidence(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    generation, decision = _approve_current_ticket()
    _project_via_runtime()
    record = projection.load_p18_9_0_kanban_projection_record()
    assert record is not None

    legacy = dict(record)
    legacy["task_skills"] = ["codebase-inspection"]
    legacy.pop("projection_SHA256", None)
    legacy["projection_SHA256"] = projection._projection_record_digest(legacy)

    validated = projection.validate_p18_9_0_kanban_projection_record(
        legacy,
        generation_record=generation,
        decision_record=decision,
    )

    assert validated["task_skills"] == ["codebase-inspection"]


def test_projection_is_deterministic_and_idempotent(projection_home, monkeypatch) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()

    first = _project_via_runtime()
    second = _project_via_runtime()

    assert first["kanban_task_id"] == second["kanban_task_id"]
    assert first["idempotent_replay"] is False
    assert second["idempotent_replay"] is True
    assert second["duplicate_task"] is False

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        tasks = kanban_db.list_tasks(conn)
        assert [task.id for task in tasks] == [first["kanban_task_id"]]
    finally:
        conn.close()


def test_conflicting_duplicate_projection_task_is_rejected(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    generation, _decision = _approve_current_ticket()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        kanban_db.create_task(
            conn,
            title="conflicting P18.9.0 projection",
            body=json.dumps({
                "ticket_id": "P18.9.0",
                "TicketSpec_SHA256": generation["ticket_spec_SHA256"],
                "WorkPacket_ID": generation["work_packet_id"],
                "WorkPacket_SHA256": "0" * 64,
            }),
            assignee=_EXECUTOR_PROFILE,
            created_by="test",
            idempotency_key=projection._idempotency_key(generation),
            board="default",
        )
    finally:
        conn.close()

    with pytest.raises(projection.WorkPacketKanbanProjectionConflict):
        _project_via_runtime()


def test_profile_assignment_gap_is_explicit(projection_home, monkeypatch) -> None:
    monkeypatch.setattr(projection, "list_profiles", lambda: [])
    _approve_current_ticket()

    with pytest.raises(projection.WorkPacketKanbanProjectionProfileGap) as exc:
        _project_via_runtime()

    assert "PROFILE_ASSIGNMENT_GAP" in str(exc.value)


def test_default_only_profile_roster_is_assignment_gap(
    projection_home,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        projection,
        "list_profiles",
        lambda: [
            SimpleNamespace(name="default", description="", is_default=True),
        ],
    )
    _approve_current_ticket()

    with pytest.raises(projection.WorkPacketKanbanProjectionProfileGap) as exc:
        _project_via_runtime()

    assert "PROFILE_ASSIGNMENT_GAP" in str(exc.value)


def test_execution_profile_classifier_accepts_bounded_architecture_product_profile(
    projection_home,
) -> None:
    profile = _profile_stub(projection_home)

    classification = projection.classify_pepper_execution_profile(profile)

    assert classification["canonical_name"] == _EXECUTOR_PROFILE
    assert classification["role"] == "architecture_product"
    assert classification["worker_assignable"] is True
    assert classification["cli_toolsets"] == ["pepper_repository"]
    assert classification["rejection_reasons"] == []


def test_p18_9_0_selects_non_default_architecture_product_profile(
    projection_home,
    monkeypatch,
) -> None:
    default = SimpleNamespace(name="default", description="", is_default=True)
    lead = _profile_stub(
        projection_home,
        name="pepper-lead-agent",
        description="Pepper Lead Agent control surface",
    )
    wrong_role = _profile_stub(
        projection_home,
        name="pepper-backend-worker",
        description="Backend implementation profile",
    )
    executor = _profile_stub(projection_home)
    monkeypatch.setattr(projection, "list_profiles", lambda: [default, lead, wrong_role, executor])

    selected = projection.resolve_p18_9_0_execution_profile()

    assert selected["selected_profile"] == _EXECUTOR_PROFILE
    assert selected["assignee_profile"] == _EXECUTOR_PROFILE
    assert selected["selected_role"] == "architecture_product"
    assert selected["execution_profile_role"] == "architecture_product"
    assert selected["selection_rationale"] == "deterministic_single_governed_role_match"
    assert selected["candidate_profiles"] == [_EXECUTOR_PROFILE]
    assert selected["lead_agent_auto_assigned"] is False


def test_profile_description_participates_in_architecture_product_selection(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(
        projection_home,
        name="pepper-planning-worker",
        description=(
            "Repository-informed product architecture, information architecture, "
            "inventory, and acceptance-contract planning; not a Lead Agent or "
            "Ticket Architect."
        ),
    )
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])

    classification = projection.classify_pepper_execution_profile(profile)
    selected = projection.resolve_p18_9_0_execution_profile()

    assert classification["role"] == "architecture_product"
    assert classification["classification_basis"] == "product_architecture_role_terms"
    assert selected["selected_profile"] == "pepper-planning-worker"
    assert selected["selected_role"] == "architecture_product"


def test_execution_profile_classifier_accepts_bounded_implementation_profile(
    projection_home,
) -> None:
    profile = _profile_stub(
        projection_home,
        name=_IMPLEMENTATION_PROFILE,
        description="Pepper frontend product implementation execution profile",
        cli_toolsets=("pepper_repository", "file", "no_mcp"),
    )

    classification = projection.classify_pepper_execution_profile(profile)

    assert classification["canonical_name"] == _IMPLEMENTATION_PROFILE
    assert classification["role"] == "implementation_product"
    assert classification["classification_basis"] == "product_implementation_role_terms"
    assert classification["worker_assignable"] is True
    assert classification["cli_toolsets"] == ["pepper_repository", "file"]
    assert classification["required_write_toolsets"] == ["file"]
    assert classification["write_capable"] is True
    assert classification["rejection_reasons"] == []


def test_profile_assignment_does_not_expose_secret_material(
    projection_home,
) -> None:
    profile = _profile_stub(projection_home)
    (profile.path / ".env").write_text("OPENAI_API_KEY=SHOULD_NOT_LEAK\n", encoding="utf-8")

    classification = projection.classify_pepper_execution_profile(profile)
    serialized = json.dumps(classification, sort_keys=True)

    assert "SHOULD_NOT_LEAK" not in serialized
    assert "OPENAI_API_KEY" not in serialized


def test_executor_provider_binding_resolves_governed_primary_without_profile_local_credentials(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(projection_home, model_config=True)
    _install_executor_profile_roster(monkeypatch, [profile])
    canonical_root = (
        projection_home
        / "agent-platform"
        / "provider-credentials"
        / "openai-codex.primary"
    )
    captured = _patch_ready_governed_provider(monkeypatch, canonical_root)
    monkeypatch.setenv("OPENAI_API_KEY", "PROFILE_ENV_SHOULD_NOT_BE_USED")
    (profile.path / ".env").write_text(
        "OPENAI_API_KEY=PROFILE_FILE_SHOULD_NOT_BE_USED\n",
        encoding="utf-8",
    )
    (profile.path / "auth.json").write_text(
        json.dumps({"access_token": "PROFILE_LOCAL_SHOULD_NOT_LEAK"}),
        encoding="utf-8",
    )

    from hermes_cli.agent_platform import lead_agent
    from hermes_cli.agent_platform import product_runtime as pr

    result = pr._executor_provider_readiness(_EXECUTOR_PROFILE)
    serialized = json.dumps(result, sort_keys=True)
    classification = projection.classify_pepper_execution_profile(profile)

    assert result["ok"] is True
    assert result["executor_profile"] == _EXECUTOR_PROFILE
    assert result["provider"] == "openai-codex"
    assert result["model"] == "gpt-5.5"
    assert result["api_mode"] == "codex_responses"
    assert result["credential_profile_id"] == "openai-codex.primary"
    assert result["credential_policy_revision"] == (
        "provider-runtime-v1.provider-worker-v1.provider-credential-v1"
    )
    assert result["provider_runtime_profile_id"] == (
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert result["worker_profile_id"] == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert result["credential_resolution_source"] == "canonical_governed_home"
    assert result["durable_store_valid"] is True
    assert result["token_pair_present"] is True
    assert result["legacy_auth_json_used"] is False
    assert result["API_key_fallback_used"] is False
    assert result["governed_refresh_path"] == "provider_worker_resolution_no_refresh"
    assert result["legacy_refresh_fallback"] is False
    assert result["credential_refresh_calls_per_request_maximum"] == 0
    assert captured["hermes_home_arg"] == projection_home
    assert captured["hermes_home_arg"] != profile.path
    assert captured["credential_root"] == canonical_root
    assert profile.path not in captured["credential_root"].parents
    assert not (profile.path / "agent-platform" / "provider-credentials").exists()
    assert "PROFILE_LOCAL_SHOULD_NOT_LEAK" not in serialized
    assert "PROFILE_ENV_SHOULD_NOT_BE_USED" not in serialized
    assert "PROFILE_FILE_SHOULD_NOT_BE_USED" not in serialized
    assert classification["cli_toolsets"] == ["pepper_repository"]
    assert classification["worker_assignable"] is True
    assert lead_agent.PEPPER_LEAD_AGENT_PROVIDER == "openai-codex"
    assert lead_agent.PEPPER_LEAD_AGENT_MODEL == "gpt-5.5"
    assert lead_agent.PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE == "openai-codex.primary"


def test_executor_provider_binding_accepts_implementation_product_profile(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(
        projection_home,
        name=_IMPLEMENTATION_PROFILE,
        description="Pepper frontend product implementation execution profile",
        cli_toolsets=("pepper_repository", "file", "no_mcp"),
        model_config=True,
    )
    _install_executor_profile_roster(monkeypatch, [profile])
    canonical_root = (
        projection_home
        / "agent-platform"
        / "provider-credentials"
        / "openai-codex.primary"
    )
    captured = _patch_ready_governed_provider(monkeypatch, canonical_root)
    (profile.path / "auth.json").write_text(
        json.dumps({"access_token": "IMPLEMENTATION_PROFILE_LOCAL_SHOULD_NOT_LEAK"}),
        encoding="utf-8",
    )

    from hermes_cli.agent_platform import product_runtime as pr

    result = pr._executor_provider_readiness(_IMPLEMENTATION_PROFILE)
    serialized = json.dumps(result, sort_keys=True)
    classification = projection.classify_pepper_execution_profile(profile)

    assert result["ok"] is True
    assert result["executor_profile"] == _IMPLEMENTATION_PROFILE
    assert result["provider"] == "openai-codex"
    assert result["model"] == "gpt-5.5"
    assert result["api_mode"] == "codex_responses"
    assert result["credential_profile_id"] == "openai-codex.primary"
    assert result["credential_policy_revision"] == (
        "provider-runtime-v1.provider-worker-v1.provider-credential-v1"
    )
    assert result["provider_runtime_profile_id"] == (
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert result["worker_profile_id"] == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert result["credential_resolution_source"] == "canonical_governed_home"
    assert result["legacy_auth_json_used"] is False
    assert result["API_key_fallback_used"] is False
    assert captured["hermes_home_arg"] == projection_home
    assert captured["credential_root"] == canonical_root
    assert profile.path not in captured["credential_root"].parents
    assert "IMPLEMENTATION_PROFILE_LOCAL_SHOULD_NOT_LEAK" not in serialized
    assert classification["role"] == "implementation_product"
    assert classification["worker_assignable"] is True


def test_executor_provider_binding_rejects_default_profile_even_with_model_config(
    projection_home,
    monkeypatch,
) -> None:
    default_profile = _profile_stub(
        projection_home,
        name="default",
        description="Pepper product architecture execution profile",
        is_default=True,
        model_config=True,
    )
    _install_executor_profile_roster(monkeypatch, [default_profile])

    from hermes_cli.agent_platform import product_runtime as pr

    result = pr._executor_provider_readiness("default")

    assert result["ok"] is False
    assert result["blocker_code"] == "PROFILE_ASSIGNMENT_GAP"
    assert result["validation_category"] == "selected_profile_not_worker_assignable"


@pytest.mark.parametrize(
    ("name", "description", "expected_role"),
    [
        (
            "pepper-lead-agent",
            "Pepper Lead Agent product architecture control surface",
            "lead_agent",
        ),
        (
            "ticket-architect",
            "Ticket Architect for Pepper product architecture planning",
            "ticket_architect",
        ),
    ],
)
def test_non_executor_profile_roles_are_rejected(
    projection_home,
    monkeypatch,
    name,
    description,
    expected_role,
) -> None:
    profile = _profile_stub(projection_home, name=name, description=description)
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])

    classification = projection.classify_pepper_execution_profile(profile)
    assert classification["role"] == expected_role
    assert classification["worker_assignable"] is False
    with pytest.raises(projection.WorkPacketKanbanProjectionProfileGap) as exc:
        projection.resolve_p18_9_0_execution_profile()

    assert "PROFILE_ASSIGNMENT_GAP" in str(exc.value)


def test_unbounded_execution_profile_toolsets_are_assignment_gap(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(
        projection_home,
        cli_toolsets=("pepper_repository", "terminal", "no_mcp"),
    )
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])

    classification = projection.classify_pepper_execution_profile(profile)
    assert classification["role"] == "architecture_product"
    assert classification["worker_assignable"] is False
    assert "unbounded_toolsets:terminal" in classification["rejection_reasons"]
    with pytest.raises(projection.WorkPacketKanbanProjectionProfileGap) as exc:
        projection.resolve_p18_9_0_execution_profile()

    assert "PROFILE_ASSIGNMENT_GAP" in str(exc.value)


def test_ambiguous_execution_profiles_require_human_selection(
    projection_home,
    monkeypatch,
) -> None:
    alpha = _profile_stub(projection_home, name="pepper-architecture-product-a")
    beta = _profile_stub(projection_home, name="pepper-architecture-product-b")
    monkeypatch.setattr(projection, "list_profiles", lambda: [beta, alpha])

    with pytest.raises(
        projection.WorkPacketKanbanProjectionProfileSelectionRequired
    ) as exc:
        projection.resolve_p18_9_0_execution_profile()

    assert "HUMAN_PROFILE_SELECTION_REQUIRED" in str(exc.value)


def test_implementation_ticket_profile_assignment_gap_is_explicit(
    projection_home,
    monkeypatch,
) -> None:
    monkeypatch.setattr(projection, "list_profiles", lambda: [])
    generation, _decision = _approve_next_ticket()

    with pytest.raises(projection.WorkPacketKanbanProjectionProfileGap) as exc:
        projection.project_current_approved_workpacket_to_kanban(
            workflow=_approved_workflow_for_record(generation),
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )

    assert "PROFILE_ASSIGNMENT_GAP" in str(exc.value)
    assert exc.value.blocker_code == "PROFILE_ASSIGNMENT_GAP"
    assert exc.value.diagnostics["required_role"] == "implementation_product"
    assert exc.value.diagnostics["candidate_profiles"] == []


def test_read_only_implementation_profile_is_write_capability_gap(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(
        projection_home,
        name=_IMPLEMENTATION_PROFILE,
        description="Pepper frontend product implementation execution profile",
        cli_toolsets=("pepper_repository", "no_mcp"),
    )
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])
    generation, _decision = _approve_next_ticket()

    with pytest.raises(projection.WorkPacketKanbanProjectionProfileGap) as exc:
        projection.project_current_approved_workpacket_to_kanban(
            workflow=_approved_workflow_for_record(generation),
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )

    diagnostics = exc.value.diagnostics
    assert str(exc.value) == "IMPLEMENTATION_WORKER_WRITE_CAPABILITY_GAP"
    assert exc.value.blocker_code == "IMPLEMENTATION_WORKER_WRITE_CAPABILITY_GAP"
    assert diagnostics["policy_id"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_ID
    assert diagnostics["policy_revision"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_REVISION
    assert diagnostics["required_role"] == "implementation_product"
    assert diagnostics["ticket_execution_requirements"]["required_toolsets"] == [
        "pepper_repository",
        "file",
    ]
    assert diagnostics["ticket_execution_requirements"]["required_write_toolsets"] == ["file"]
    assert diagnostics["role_candidate_profiles"] == [_IMPLEMENTATION_PROFILE]
    assert diagnostics["candidate_profiles"] == []
    reasons = diagnostics["rejection_reasons_by_profile"][_IMPLEMENTATION_PROFILE]
    assert "missing_required_toolsets:file" in reasons
    assert "missing_required_write_toolsets:file" in reasons
    assert "implementation_profile_read_only" in reasons

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        assert kanban_db.list_tasks(conn) == []
    finally:
        conn.close()


def test_implementation_ticket_ambiguous_profiles_require_human_selection(
    projection_home,
    monkeypatch,
) -> None:
    alpha = _profile_stub(
        projection_home,
        name="pepper-frontend-implementation-a",
        description="Pepper frontend product implementation execution profile",
        cli_toolsets=("pepper_repository", "file", "no_mcp"),
    )
    beta = _profile_stub(
        projection_home,
        name="pepper-shell-implementation-b",
        description="Pepper shell product implementation execution profile",
        cli_toolsets=("pepper_repository", "file", "no_mcp"),
    )
    monkeypatch.setattr(projection, "list_profiles", lambda: [beta, alpha])
    generation, _decision = _approve_next_ticket()

    with pytest.raises(
        projection.WorkPacketKanbanProjectionProfileSelectionRequired
    ) as exc:
        projection.project_current_approved_workpacket_to_kanban(
            workflow=_approved_workflow_for_record(generation),
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )

    assert "HUMAN_PROFILE_SELECTION_REQUIRED" in str(exc.value)


def test_existing_projection_task_with_wrong_profile_policy_is_rejected(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    generation, _decision = _approve_current_ticket()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        kanban_db.create_task(
            conn,
            title="old P18.9.0 projection",
            body=json.dumps({
                "ticket_id": "P18.9.0",
                "TicketSpec_SHA256": generation["ticket_spec_SHA256"],
                "WorkPacket_ID": generation["work_packet_id"],
                "WorkPacket_SHA256": generation["work_packet_SHA256"],
                "assignee_profile": "ticket-architect",
                "profile_assignment_policy_id": "old-policy",
                "execution_profile_role": "ticket_architect",
            }),
            assignee="ticket-architect",
            created_by="test",
            idempotency_key=projection._idempotency_key(generation),
            board="default",
        )
    finally:
        conn.close()

    with pytest.raises(projection.WorkPacketKanbanProjectionConflict) as exc:
        _project_via_runtime()

    assert "profile" in str(exc.value) or "assignee" in str(exc.value)


def test_blocked_dependency_admission_does_not_create_ready_task(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()

    def blocked_admission(*, dependency_plan, ticket_id, dependency_satisfaction_evidence=()):
        return {
            "schema_version": 1,
            "policy_id": projection.DEPENDENCY_AWARE_QUEUE_POLICY_ID,
            "ticket_id": ticket_id,
            "dependency_plan_SHA256": dependency_plan.plan_SHA256,
            "dependency_plan_reused": True,
            "dependency_planner_reused": True,
            "dependency_plan_recomputed_unnecessarily": False,
            "decision": "blocked",
            "dependencies_satisfied": False,
            "queue_eligible": False,
            "queue_admitted": False,
            "dependency_blockers": [{"dependency_ticket_id": "P18.9.X"}],
            "approval_bypass": False,
            "dependency_bypass": False,
            "dispatch_eligible": False,
            "execution_started": False,
            "worker_dispatch_count": 0,
            "command_execution_count": 0,
            "Git_commands_executed": 0,
            "Docker_commands_executed": 0,
            "Graphify_commands_executed": 0,
        }

    monkeypatch.setattr(
        projection,
        "derive_dependency_queue_admission_for_ticket",
        blocked_admission,
    )

    with pytest.raises(projection.WorkPacketKanbanProjectionBlocked):
        _project_via_runtime()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        assert kanban_db.list_tasks(conn) == []
    finally:
        conn.close()


def test_generic_projection_blocks_active_execution_before_task_creation(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    generation, _decision = _approve_next_ticket()
    workflow = {
        **_approved_workflow_for_record(generation),
        "active_execution_count": 1,
        "execution_state": "active_executions",
    }

    with pytest.raises(projection.WorkPacketKanbanProjectionBlocked) as exc:
        projection.project_current_approved_workpacket_to_kanban(
            workflow=workflow,
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )

    assert "EXECUTION_ALREADY_ACTIVE" in str(exc.value)

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        assert kanban_db.list_tasks(conn) == []
    finally:
        conn.close()


def test_generic_projection_rejects_wrong_approval_revision_before_task_creation(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    generation, decision = _approve_next_ticket()
    workflow = _approved_workflow_for_record(generation)
    tampered = dict(decision)
    tampered["work_packet_SHA256"] = "0" * 64
    tampered["approval_publication_SHA256"] = bridge._approval_decision_record_digest(tampered)
    bridge.approval_decision_record_path_for_ticket("P18.9.1").write_text(
        json.dumps(tampered, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(projection.WorkPacketKanbanProjectionConflict):
        projection.project_current_approved_workpacket_to_kanban(
            workflow=workflow,
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board="default")
    try:
        assert kanban_db.list_tasks(conn) == []
    finally:
        conn.close()


def test_chat_tool_prepares_current_ticket_execution_projection(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_execution",
            {
                "human_request_text": "Prepara P18.9.0 para ejecucion",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "P18_9_0_APPROVED_NO_EXECUTION",
            },
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "prepare_current_ticket_execution"
    assert result["workflow_status"] == "queued"
    assert result["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert result["assignee_profile"] == _EXECUTOR_PROFILE
    assert result["profile_assignment_policy_id"] == projection.PEPPER_EXECUTION_PROFILES_POLICY_ID
    assert result["selected_profile"] == _EXECUTOR_PROFILE
    assert result["execution_profile_role"] == "architecture_product"
    assert result["selected_role"] == "architecture_product"
    assert result["profile_toolsets"] == ["pepper_repository"]
    assert result["lead_agent_auto_assigned"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False


def test_chat_tool_prepares_current_generic_ticket_execution_projection(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    generation, _decision = _approve_next_ticket()

    from hermes_cli.agent_platform import product_runtime as pr

    def workflow_snapshot() -> dict:
        record = bridge.load_generation_record(ticket_id="P18.9.1")
        assert record is not None
        workflow = _approved_workflow_for_record(record)
        projected = projection.load_kanban_projection_record(
            ticket_id="P18.9.1",
            generation_record=record,
        )
        if projected is not None:
            workflow.update(projection.kanban_projection_to_workflow_overlay(projected))
        return workflow

    monkeypatch.setattr(pr, "build_workflow_control_snapshot", workflow_snapshot)
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_execution",
            {
                "human_request_text": "Prepara P18.9.1 para ejecucion",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.1",
                "next_action_id": "P18_9_1_APPROVED_NO_EXECUTION",
            },
        )
    )

    assert result["success"] is True
    assert result["ticket_id"] == "P18.9.1"
    assert result["ticket_spec_SHA256"] == generation["ticket_spec_SHA256"]
    assert result["work_packet_id"] == generation["work_packet_id"]
    assert result["work_packet_SHA256"] == generation["work_packet_SHA256"]
    assert result["workflow_status"] == "queued"
    assert result["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert result["assignee_profile"] == _IMPLEMENTATION_PROFILE
    assert result["execution_profile_role"] == "implementation_product"
    assert result["next_action"]["id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False


def test_chat_tool_returns_profile_assignment_diagnostics_on_gap(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(
        projection_home,
        name=_IMPLEMENTATION_PROFILE,
        description="Pepper frontend product implementation execution profile",
        cli_toolsets=("pepper_repository", "no_mcp"),
    )
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])
    _approve_next_ticket()

    from hermes_cli.agent_platform import product_runtime as pr

    def workflow_snapshot() -> dict:
        record = bridge.load_generation_record(ticket_id="P18.9.1")
        assert record is not None
        return _approved_workflow_for_record(record)

    monkeypatch.setattr(pr, "build_workflow_control_snapshot", workflow_snapshot)
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_execution",
            {
                "human_request_text": "Prepara P18.9.1 para ejecucion",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.1",
                "next_action_id": "P18_9_1_APPROVED_NO_EXECUTION",
            },
        )
    )

    diagnostics = result["profile_assignment_diagnostics"]
    assert result["success"] is False
    assert result["blocker_code"] == "IMPLEMENTATION_WORKER_WRITE_CAPABILITY_GAP"
    assert diagnostics["required_role"] == "implementation_product"
    assert diagnostics["candidate_profiles"] == []
    assert diagnostics["role_candidate_profiles"] == [_IMPLEMENTATION_PROFILE]
    assert "implementation_profile_read_only" in diagnostics[
        "rejection_reasons_by_profile"
    ][_IMPLEMENTATION_PROFILE]


def test_current_ticket_start_blocks_when_executor_provider_unconfigured(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home, model_config=False)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("spawn must stay blocked"),
    )

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "EXECUTOR_PROVIDER_RESOLUTION_GAP"
    assert result["execution_authorization_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert not pr.p18_9_0_execution_start_record_path().exists()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_executor_provider_binding_readiness_does_not_dispatch_projected_task(
    projection_home,
    monkeypatch,
) -> None:
    profile = _profile_stub(projection_home, model_config=True)
    monkeypatch.setattr(projection, "list_profiles", lambda: [profile])
    _install_executor_profile_roster(monkeypatch, [profile])
    _approve_current_ticket()
    projected = _project_via_runtime()
    canonical_root = (
        projection_home
        / "agent-platform"
        / "provider-credentials"
        / "openai-codex.primary"
    )
    _patch_ready_governed_provider(monkeypatch, canonical_root)

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    readiness = pr._executor_provider_readiness(_EXECUTOR_PROFILE)
    workflow = pr.build_workflow_control_snapshot()

    assert readiness["ok"] is True
    assert workflow["workflow_status"] == "queued"
    assert workflow["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert workflow["execution_started"] is False
    assert workflow["worker_execution"] is False
    assert workflow["next_action"]["id"] == (
        "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert task.worker_pid is None
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_current_ticket_start_blocks_legacy_semantic_task_skill_before_spawn(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        conn.execute(
            "UPDATE tasks SET skills = ? WHERE id = ?",
            (json.dumps(["codebase-inspection"]), projected["kanban_task_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("spawn must stay blocked"),
    )

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "TASK_SKILL_EXECUTOR_CAPABILITY_MISMATCH"
    assert result["execution_authorization_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert not pr.p18_9_0_execution_start_record_path().exists()

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_current_ticket_start_claims_only_projected_task(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: {
            "ok": True,
            "provider": "openai-codex",
            "model": "gpt-5.5",
            "api_mode": "codex_responses",
            "credential_profile_id": "openai-codex.primary",
            "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
            "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
            "executor_config_source": "test",
            "executor_profile": profile_name,
        },
    )

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        other_task_id = kanban_db.create_task(
            conn,
            title="unrelated higher priority ready work",
            body="{}",
            assignee=_EXECUTOR_PROFILE,
            created_by="test",
            workspace_kind="scratch",
            priority=100,
            board=projected["kanban_board_slug"],
        )
        kanban_db.recompute_ready(conn)
    finally:
        conn.close()

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )

    assert result["start_status"] == "started"
    assert result["execution_authorization_recorded"] is True
    assert result["ticket_execution_authorized"] is True
    assert result["WorkPacket_execution_authorized"] is True
    assert result["runtime_execution_authorized"] is True
    assert result["dispatch_performed"] is True
    assert result["execution_started"] is True
    assert result["worker_execution"] is True
    assert result["Kanban_dispatch"] is True
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["workspace_kind"] == "scratch"
    assert result["workspace_path"]
    assert result["kanban_run_id"] is not None
    assert result["runs"][0]["status"] == "running"

    record = pr.load_p18_9_0_execution_start_record()
    assert record is not None
    assert record["execution_authorized"] is True
    assert record["start_status"] == "started"
    assert record["work_packet_id"] == projected["work_packet_id"]
    assert record["work_packet_SHA256"] == projected["work_packet_SHA256"]

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        projected_task = kanban_db.get_task(conn, projected["kanban_task_id"])
        other_task = kanban_db.get_task(conn, other_task_id)
        assert projected_task is not None
        assert other_task is not None
        assert projected_task.status == "running"
        assert projected_task.worker_pid == 4321
        assert other_task.status == "ready"
        assert kanban_db.list_runs(conn, other_task_id) == []
    finally:
        conn.close()

    context = pr.build_lead_agent_operational_context()
    assert context["workflow_status"] == "executing"
    assert context["queue_state"] == "kanban_dispatched"
    assert context["next_action"]["id"] == "MONITOR_P18_9_0_EXECUTION"


def test_current_ticket_start_binds_generic_projection_and_record_path(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    generation, _decision = _approve_next_ticket()
    projected = _project_next_ticket_direct()
    authority = _projection_authority_record(projected)

    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(projected),
    )
    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda _projection, *, enabled=True: _ready_worker_credential_probe(),
    )
    _patch_synthetic_scratch_materialization(monkeypatch, pr)

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 5321,
    )

    current_path = pr.execution_start_record_path_for_ticket("P18.9.1")
    assert result["start_status"] == "started"
    assert result["ticket_id"] == "P18.9.1"
    assert result["ticket_spec_SHA256"] == generation["ticket_spec_SHA256"]
    assert result["work_packet_id"] == authority["work_packet_id"]
    assert result["work_packet_SHA256"] == authority["work_packet_SHA256"]
    assert result["kanban_task_id"] == authority["kanban_task_id"]
    assert result["assignee_profile"] == _IMPLEMENTATION_PROFILE
    assert result["next_action"]["target_ticket_id"] == "P18.9.1"
    assert current_path.exists()
    assert not pr.p18_9_0_execution_start_record_path().exists()

    record = pr.load_p18_9_0_execution_start_record(projection_record=authority)
    assert record is not None
    assert record["ticket_id"] == "P18.9.1"
    assert record["projection_SHA256"] == authority["projection_SHA256"]
    assert record["kanban_task_id"] == authority["kanban_task_id"]
    assert record["assignee_profile"] == _IMPLEMENTATION_PROFILE


def test_current_ticket_start_p18_9_1_consent_reaches_provider_preflight_without_spawn(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home, model_config=False)
    _approve_next_ticket()
    projected = _project_next_ticket_direct()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(projected),
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("provider preflight must block before spawn"),
    )

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "EXECUTOR_PROVIDER_RESOLUTION_GAP"
    assert result["authorization_diagnostics"] is None
    assert result["execution_authorization_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_process_started"] is False
    assert not pr.execution_start_record_path_for_ticket("P18.9.1").exists()
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert task.current_run_id is None
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_initial_start_rejects_retry_text_for_current_p18_9_1(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    _approve_next_ticket()
    projected = _project_next_ticket_direct()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(projected),
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Retry P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("retry text must not start initial execution"),
    )

    diagnostics = result["authorization_diagnostics"]
    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "EXECUTION_AUTHORIZATION_KIND_MISMATCH"
    assert "initial execution start authorization" in result["blocker_detail"]
    assert diagnostics["current_ticket_id"] == "P18.9.1"
    assert diagnostics["requested_ticket_id"] == "P18.9.1"
    assert diagnostics["current_next_action_id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert diagnostics["requested_next_action_id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert diagnostics["authorization_kind"] == "execution_retry_authorization"
    assert diagnostics["expected_authorization_kind"] == "execution_start_authorization"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert not pr.execution_start_record_path_for_ticket("P18.9.1").exists()
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_historical_retry_text_cannot_authorize_current_p18_9_1_initial_start(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    _approve_next_ticket()
    projected = _project_next_ticket_direct()

    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(projected),
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("historical retry text must not spawn current ticket"),
    )

    diagnostics = result["authorization_diagnostics"]
    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "EXECUTION_AUTHORIZATION_TICKET_MISMATCH"
    assert diagnostics["current_ticket_id"] == "P18.9.1"
    assert diagnostics["requested_ticket_id"] == "P18.9.1"
    assert diagnostics["mentioned_ticket_ids"] == ["P18.9.0"]
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert not pr.execution_start_record_path_for_ticket("P18.9.1").exists()


def test_current_ticket_start_rejects_stale_next_action_before_authorization_record(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    _approve_next_ticket()
    projected = _project_next_ticket_direct()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(projected),
    )

    with pytest.raises(pr.ProductRuntimeConflict) as excinfo:
        pr.start_current_ticket_execution(
            human_authorization_text="Start P18.9.1 execution now",
            project_id="PEPPER",
            ticket_id="P18.9.1",
            next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("stale action must not spawn"),
        )

    assert "execution start requires START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION" in str(
        excinfo.value
    )
    assert not pr.execution_start_record_path_for_ticket("P18.9.1").exists()
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_historical_p18_9_0_start_authority_does_not_replay_for_next_ticket(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    historical_projection = _project_via_runtime()
    historical_authority = _projection_authority_record(historical_projection)

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(historical_projection),
    )
    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda _projection, *, enabled=True: _ready_worker_credential_probe(),
    )
    historical = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )
    assert historical["execution_started"] is True
    assert pr.p18_9_0_execution_start_record_path().exists()
    conn = kanban_db.connect(board=historical_authority["kanban_board_slug"])
    try:
        assert kanban_db.complete_task(
            conn,
            historical_authority["kanban_task_id"],
            summary=(
                "Summary\nP18.9.0 historical execution completed for stale-authority regression.\n"
                "Files inspected\n- none\nFiles modified\n- none\nTests/commands run\n- none\n"
                "Decisions made\n- closed historical task\nLimitations\n- synthetic test fixture"
            ),
            expected_run_id=historical["kanban_run_id"],
        )
    finally:
        conn.close()

    _install_implementation_profile(monkeypatch, projection_home)
    _approve_next_ticket()
    current_projection = _project_next_ticket_direct()
    current_authority = _projection_authority_record(current_projection)
    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(current_projection),
    )
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    current = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 5321,
    )

    assert current["start_status"] == "started"
    assert current["idempotent_replay"] is False
    assert current["ticket_id"] == "P18.9.1"
    assert current["kanban_task_id"] == current_authority["kanban_task_id"]
    historical_record = json.loads(
        pr.p18_9_0_execution_start_record_path().read_text(encoding="utf-8")
    )
    assert pr.validate_p18_9_0_execution_start_record(
        historical_record,
        projection_record=historical_authority,
    )["ticket_id"] == "P18.9.0"
    current_record = pr.load_p18_9_0_execution_start_record(
        projection_record=current_authority,
    )
    assert current_record is not None
    assert current_record["ticket_id"] == "P18.9.1"
    assert current_record["kanban_task_id"] == current_authority["kanban_task_id"]


def test_current_ticket_start_blocks_mismatched_current_authorization_record(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    _approve_next_ticket()
    projected = _project_next_ticket_direct()
    authority = _projection_authority_record(projected)

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "build_workflow_control_snapshot",
        lambda: _queued_workflow_for_projection(projected),
    )
    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda _projection, *, enabled=True: _ready_worker_credential_probe(),
    )

    stale = pr._build_execution_start_authorization_record(
        request=pr.CurrentTicketExecutionStartRequest(
            human_authorization_text="Start P18.9.0 execution now",
            project_id="PEPPER",
            ticket_id="P18.9.0",
            next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        ),
        projection=authority,
        provider_readiness=_ready_executor_provider_payload(_IMPLEMENTATION_PROFILE),
    )
    stale["ticket_id"] = "P18.9.0"
    stale["ticket_spec_SHA256"] = "0" * 64
    stale["work_packet_id"] = "WP-P18-9-0-STALE"
    stale["work_packet_SHA256"] = "1" * 64
    stale["projection_SHA256"] = "2" * 64
    stale["kanban_task_id"] = "t_stale"
    stale["assignee_profile"] = "pepper-architecture-product"
    stale["selected_profile"] = "pepper-architecture-product"
    stale["start_authorization_SHA256"] = pr._execution_start_record_digest(stale)
    path = pr.execution_start_record_path_for_ticket("P18.9.1")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(stale, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("spawn must stay blocked"),
    )

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "EXECUTION_START_AUTHORITY_STALE"
    assert result["execution_authorization_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    mismatch = result["authorization_mismatch"]
    assert mismatch["mismatched_field"] == "ticket_id"
    assert mismatch["current_ticket_id"] == "P18.9.1"
    assert mismatch["authorization_ticket_id"] == "P18.9.0"
    assert mismatch["expected_projection_SHA256"] == authority["projection_SHA256"]
    assert mismatch["authorization_projection_SHA256"] == "2" * 64
    assert mismatch["expected_kanban_task_id"] == authority["kanban_task_id"]
    assert mismatch["authorization_kanban_task_id"] == "t_stale"
    assert mismatch["expected_executor_profile"] == _IMPLEMENTATION_PROFILE
    assert mismatch["authorization_executor_profile"] == "pepper-architecture-product"

    persisted = json.loads(path.read_text(encoding="utf-8"))
    assert persisted["ticket_id"] == "P18.9.0"
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_current_ticket_start_blocks_worker_credential_probe_before_claim(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
    )

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "WORKER_CREDENTIAL_AUTHORITY_MISMATCH"
    assert result["execution_authorization_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_process_started"] is False
    assert not pr.p18_9_0_execution_start_record_path().exists()

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "ready"
        assert task.current_run_id is None
        assert task.worker_pid is None
        assert kanban_db.list_runs(conn, task.id) == []
    finally:
        conn.close()


def test_exact_dispatch_passes_non_secret_governed_worker_overlay(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr
    from hermes_cli.agent_platform.worker_credentials import (
        PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION,
    )

    captured = {}

    def capture_spawn(_task, _workspace, *, board=None, env_overlay=None):
        captured["board"] = board
        captured["env_overlay"] = dict(env_overlay or {})
        return 4321

    result = pr._dispatch_exact_current_kanban_task(projected, spawn_fn=capture_spawn)

    assert result["start_status"] == "started"
    assert result["source_materialized"] is False
    assert result["source_materialization"] is None
    assert captured["board"] == projected["kanban_board_slug"]
    overlay = captured["env_overlay"]
    assert overlay["HERMES_AGENT_PLATFORM_GOVERNED_WORKER"] == "pepper-kanban-worker"
    assert overlay["HERMES_AGENT_PLATFORM_CREDENTIAL_STORE_ID"] == "openai-codex.primary"
    assert overlay["HERMES_AGENT_PLATFORM_PROVIDER"] == "openai-codex"
    assert overlay["HERMES_AGENT_PLATFORM_MODEL"] == "gpt-5.5"
    assert overlay["HERMES_AGENT_PLATFORM_API_MODE"] == "codex_responses"
    assert overlay["HERMES_AGENT_PLATFORM_PROVIDER_RUNTIME_PROFILE_ID"] == (
        "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert overlay["HERMES_AGENT_PLATFORM_WORKER_PROFILE_ID"] == (
        "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert overlay["HERMES_AGENT_PLATFORM_WORKPACKET_ID"] == projected["work_packet_id"]
    assert overlay["HERMES_AGENT_PLATFORM_WORKPACKET_SHA256"] == projected["work_packet_SHA256"]
    assert overlay["HERMES_AGENT_PLATFORM_TICKET_SPEC_SHA256"] == projected["ticket_spec_SHA256"]
    assert overlay["HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_SHA256"] == (
        projected["authority"]["projection_SHA256"]
    )
    assert overlay["HERMES_AGENT_PLATFORM_CREDENTIAL_POLICY_REVISION"] == (
        PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION
    )
    assert overlay["HERMES_AGENT_PLATFORM_PROFILE_ASSIGNMENT_POLICY_ID"] == (
        projection.PEPPER_EXECUTION_PROFILES_POLICY_ID
    )
    assert overlay["HERMES_AGENT_PLATFORM_PROFILE_ASSIGNMENT_POLICY_REVISION"] == (
        projection.PEPPER_EXECUTION_PROFILES_POLICY_REVISION
    )
    assert overlay["HERMES_AGENT_PLATFORM_GENERATION_RECORD_PATH"] == str(
        bridge.generation_record_path_for_ticket(projected["ticket_id"])
    )
    assert overlay["HERMES_AGENT_PLATFORM_APPROVAL_DECISION_RECORD_PATH"] == str(
        bridge.approval_decision_record_path_for_ticket(projected["ticket_id"])
    )
    assert overlay["HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_RECORD_PATH"] == str(
        projection.kanban_projection_record_path_for_ticket(projected["ticket_id"])
    )
    joined = json.dumps(overlay, sort_keys=True)
    assert "access_token" not in joined
    assert "refresh_token" not in joined
    assert "api_key" not in joined.lower()
    applied_env = {}
    kanban_db._apply_worker_env_overlay(applied_env, overlay)
    assert applied_env == overlay
    with pytest.raises(ValueError, match="unsupported key"):
        kanban_db._apply_worker_env_overlay(
            {},
            {"HERMES_AGENT_PLATFORM_API_KEY": "SHOULD_NOT_PASS"},
        )


def test_current_ticket_start_records_immediate_worker_exit_as_failed_dispatch(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: {
            "ok": True,
            "provider": "openai-codex",
            "model": "gpt-5.5",
            "api_mode": "codex_responses",
            "credential_profile_id": "openai-codex.primary",
            "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
            "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
            "executor_config_source": "test",
            "executor_profile": profile_name,
        },
    )
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda _projection, *, enabled=True: _ready_worker_credential_probe(),
    )

    class _ExitedProc:
        pid = 2468

        def poll(self):
            return 1

    monkeypatch.setattr("subprocess.Popen", lambda *_args, **_kwargs: _ExitedProc())

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
    )

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == "KANBAN_WORKER_SPAWN_FAILED"
    assert result["dispatch_performed"] is True
    assert result["execution_started"] is False
    assert result["worker_execution"] is False

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.worker_pid is None
        assert task.current_run_id is None
        assert task.last_failure_error
        assert "worker exited during bootstrap" in task.last_failure_error
        assert len(runs) == 1
        assert runs[0].status == "gave_up"
        assert runs[0].outcome == "gave_up"
        assert runs[0].ended_at is not None
    finally:
        conn.close()

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["blocker_count"] == 1
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"


def test_workflow_snapshot_reconciles_recorded_dead_worker_pid_to_failed_state(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: {
            "ok": True,
            "provider": "openai-codex",
            "model": "gpt-5.5",
            "api_mode": "codex_responses",
            "credential_profile_id": "openai-codex.primary",
            "provider_runtime_profile_id": "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
            "worker_profile_id": "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
            "executor_config_source": "test",
            "executor_profile": profile_name,
        },
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 987654321,
    )
    assert result["start_status"] == "started"
    assert result["execution_started"] is True

    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda _pid: False)
    workflow = pr.build_workflow_control_snapshot()

    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["blocker_count"] == 1
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"
    assert workflow["worker_lifecycle"]["latest_run_outcome"] == "crashed"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.worker_pid is None
        assert task.current_run_id is None
        assert len(runs) == 1
        assert runs[0].status == "crashed"
        assert runs[0].outcome == "crashed"
        assert runs[0].ended_at is not None
    finally:
        conn.close()


def test_workflow_snapshot_keeps_healthy_active_worker_running(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )
    assert result["start_status"] == "started"
    assert result["execution_started"] is True

    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 4321)
    workflow = pr.build_workflow_control_snapshot()

    assert workflow["workflow_status"] == "executing"
    assert workflow["execution_state"] == "active_executions"
    assert workflow["recovery_state"] == "not_required"
    assert workflow["review_state"] == "not_started_execution_in_progress"
    assert workflow["next_action"]["id"] == "MONITOR_P18_9_0_EXECUTION"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "running"
        assert task.worker_pid == 4321
        assert task.current_run_id == result["kanban_run_id"]
        assert len(runs) == 1
        assert runs[0].status == "running"
        assert runs[0].ended_at is None
    finally:
        conn.close()


def test_workflow_snapshot_reconciles_historical_non_host_orphan_to_recovery(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        claimed = kanban_db.claim_task(
            conn,
            projected["kanban_task_id"],
            claimer="pepper-worker-start-action",
        )
        assert claimed is not None
        workspace = kanban_db.resolve_workspace(claimed, board=projected["kanban_board_slug"])
        kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
        kanban_db._set_worker_pid(conn, claimed.id, 12628)
        old_started = int(time.time()) - 7200
        old_expiry = int(time.time()) - 6300
        conn.execute(
            "UPDATE tasks SET started_at = ?, claim_expires = ?, "
            "last_heartbeat_at = NULL, skills = ? WHERE id = ?",
            (
                old_started,
                old_expiry,
                json.dumps(["codebase-inspection"]),
                claimed.id,
            ),
        )
        conn.execute(
            "UPDATE task_runs SET started_at = ?, claim_expires = ?, "
            "last_heartbeat_at = NULL WHERE id = ?",
            (old_started, old_expiry, claimed.current_run_id),
        )
        conn.commit()
        run_id = int(claimed.current_run_id)
    finally:
        conn.close()
    _persist_started_execution_record(pr, projected, run_id)

    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda _pid: False)
    workflow = pr.build_workflow_control_snapshot()

    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["review_state"] == "not_started_execution_failed"
    assert workflow["failure_category"] == "worker_bootstrap_failure"
    assert "orphaned active run" in workflow["failure_summary"]
    assert workflow["worker_lifecycle"]["failure_category"] == "worker_bootstrap_failure"
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"
    assert workflow["Git_mutation"] is False

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        events = kanban_db.list_events(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.worker_pid is None
        assert task.current_run_id is None
        assert task.consecutive_failures == 1
        assert task.last_failure_error
        assert "orphaned active run" in task.last_failure_error
        assert len(runs) == 1
        assert runs[0].id == run_id
        assert runs[0].status == "crashed"
        assert runs[0].outcome == "crashed"
        assert runs[0].ended_at is not None
        assert runs[0].metadata["reconciliation"] == "orphaned_active_run"
        assert runs[0].metadata["failure_category"] == "worker_bootstrap_failure"
        assert [run.id for run in runs] == [1]
        assert any(event.kind == "gave_up" for event in events)
    finally:
        conn.close()

    context = pr.build_lead_agent_operational_context()
    assert context["workflow_status"] == "execution_failed"
    assert context["execution_state"] == "no_active_executions"
    assert context["recovery_state"] == "recovery_required"
    assert context["failure_category"] == "worker_bootstrap_failure"
    assert context["auto_retry"] is False
    assert context["auto_rollback"] is False
    assert context["Git_mutation"] is False

    import tools.pepper_workflow_tools as pepper_tools

    execution_status = json.loads(pepper_tools._get_execution_status({}))
    workflow_control = json.loads(pepper_tools._get_workflow_control({}))
    review_status = json.loads(pepper_tools._get_review_status({}))
    next_action = json.loads(pepper_tools._get_next_action({}))

    assert execution_status["execution_state"] == "no_active_executions"
    assert execution_status["active_execution_count"] == 0
    assert execution_status["recent_executions"][0]["status"] == "crashed"
    assert execution_status["recent_executions"][0]["failure_category"] == "worker_bootstrap_failure"
    assert workflow_control["workflow_status"] == "execution_failed"
    assert workflow_control["recovery_state"] == "recovery_required"
    assert workflow_control["failure_category"] == "worker_bootstrap_failure"
    assert review_status["review_state"] == "not_started_execution_failed"
    assert review_status["recovery_state"] == "recovery_required"
    assert review_status["failure_category"] == "worker_bootstrap_failure"
    assert next_action["workflow_status"] == "execution_failed"
    assert next_action["recovery_state"] == "recovery_required"
    assert next_action["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"
    assert next_action["auto_retry"] is False
    assert next_action["auto_rollback"] is False


def test_recover_current_ticket_execution_records_retry_pending_without_run_2(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    run_id = _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    failed = pr.build_workflow_control_snapshot()
    assert failed["workflow_status"] == "execution_failed"
    assert failed["recovery_state"] == "recovery_required"
    assert failed["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"

    result = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )

    assert result["recovery_status"] == "retry_pending"
    assert result["recovery_authorization_recorded"] is True
    assert result["runtime_boundary_classification"] == "RECOVERY_DECISION_ONLY"
    assert result["P18_6_policy_id"] == "pepper-retry-incident-rollback-workflow-v1"
    assert result["governed_workflow_transition_id"] == "GWT-023"
    assert result["retry_identity_model"] == "same_kanban_task_new_run"
    assert result["future_retry_prepared"] is True
    assert result["future_retry_requires_separate_start_authorization"] is True
    assert result["observed_attempt_count"] == 1
    assert result["max_attempts"] == 2
    assert result["next_attempt_number"] == 2
    assert result["future_task_skills"] == []
    assert result["observed_task_skills"] == ["codebase-inspection"]
    assert result["future_retry_capability_surface"] == "pepper_repository"
    assert result["unresolved_Hermes_task_skills"] == []
    assert result["retry_execution_started"] is False
    assert result["retry_execution_count"] == 0
    assert result["automatic_retry_count"] == 0
    assert result["automatic_requeue_count"] == 0
    assert result["Kanban_requeue_calls"] == 0
    assert result["Kanban_reclaim_calls"] == 0
    assert result["Kanban_reassign_calls"] == 0
    assert result["new_kanban_task_created"] is False
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["kanban_run_count"] == 1
    assert result["second_run_started"] is False
    assert result["human_smoke_marker"] == "PEPPER-RECOVERY-ACTION-READY-FOR-HUMAN-SMOKE"

    record = pr.load_p18_9_0_recovery_action_record()
    assert record is not None
    assert record["recovery_action_SHA256"] == result["recovery_action_SHA256"]
    assert record["human_authorization"]["action"] == "authorize_retry"

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "retry_pending"
    assert workflow["queue_state"] == "kanban_retry_prepared_not_dispatched"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["recovery_state"] == "retry_pending"
    assert workflow["blocker_count"] == 0
    assert workflow["next_action"]["id"] == "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    assert workflow["recovery_authority"]["retry_execution_count"] == 0
    assert workflow["recovery_authority"]["Kanban_requeue_calls"] == 0
    assert workflow["recovery_authority"]["future_task_skills"] == []
    assert workflow["recovery_authority"]["future_retry_capability_surface"] == "pepper_repository"

    replay = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert replay["idempotent_replay"] is True
    assert replay["recovery_action_SHA256"] == result["recovery_action_SHA256"]

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.current_run_id is None
        assert len(runs) == 1
        assert runs[0].id == run_id
        assert runs[0].status == "crashed"
        assert runs[0].outcome == "crashed"
    finally:
        conn.close()


def test_start_current_ticket_execution_starts_retry_run_2_from_retry_pending(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    run_1 = _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert recovery["recovery_status"] == "retry_pending"

    recovery_text_retry = pr.start_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("recovery text must not start retry"),
    )
    assert recovery_text_retry["retry_start_status"] == "blocked"
    assert recovery_text_retry["blocker_code"] == "EXECUTION_AUTHORIZATION_KIND_MISMATCH"
    assert recovery_text_retry["authorization_diagnostics"]["authorization_kind"] == (
        "execution_recovery_authorization"
    )

    initial_text_retry = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("initial text must not start retry"),
    )
    assert initial_text_retry["retry_start_status"] == "blocked"
    assert initial_text_retry["blocker_code"] == "EXECUTION_AUTHORIZATION_KIND_MISMATCH"
    assert initial_text_retry["authorization_diagnostics"]["authorization_kind"] == (
        "execution_start_authorization"
    )

    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 4321)

    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )

    assert result["source_system"] == pr.PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM
    assert result["policy_id"] == pr.PEPPER_RETRY_START_ACTION_POLICY_ID
    assert result["start_status"] == "started"
    assert result["retry_start_status"] == "started"
    assert result["retry_start_authorization_recorded"] is True
    assert result["recovery_action_SHA256"] == recovery["recovery_action_SHA256"]
    assert result["retry_identity_model"] == "same_kanban_task_new_run"
    assert result["previous_attempt_count"] == 1
    assert result["next_attempt_number"] == 2
    assert result["max_attempts"] == 2
    assert result["latest_failed_run_id"] == run_1
    assert result["future_task_skills"] == []
    assert result["observed_task_skills"] == ["codebase-inspection"]
    assert result["future_retry_capability_surface"] == "pepper_repository"
    assert result["unresolved_Hermes_task_skills"] == []
    assert result["task_prepare_status"] == "prepared"
    assert result["task_unblocked"] is True
    assert result["task_skills_corrected"] is True
    assert result["dispatch_performed"] is True
    assert result["execution_started"] is True
    assert result["worker_execution"] is True
    assert result["worker_process_started"] is True
    assert result["Kanban_dispatch"] is True
    assert result["retry_execution_started"] is True
    assert result["retry_execution_count"] == 1
    assert result["automatic_retry_count"] == 0
    assert result["automatic_requeue_count"] == 0
    assert result["Kanban_requeue_calls"] == 0
    assert result["Kanban_reclaim_calls"] == 0
    assert result["new_kanban_task_created"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["human_smoke_marker"] == "PEPPER-RETRY-START-ACTION-READY-FOR-HUMAN-SMOKE"
    assert result["next_action"]["id"] == "MONITOR_P18_9_0_EXECUTION"

    record = pr.load_p18_9_0_retry_start_record()
    assert record is not None
    assert record["retry_start_authorization_SHA256"] == result["retry_start_authorization_SHA256"]
    assert record["human_authorization_text"] == "Autorizo explícitamente el retry de P18.9.0."

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        events = kanban_db.list_events(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "running"
        assert task.current_run_id == result["kanban_run_id"]
        assert task.worker_pid == 4321
        assert task.skills == []
        assert task.consecutive_failures == 0
        assert len(runs) == 2
        assert [run.id for run in runs] == [run_1, result["kanban_run_id"]]
        assert runs[0].status == "crashed"
        assert runs[0].outcome == "crashed"
        assert runs[0].ended_at is not None
        assert runs[1].status == "running"
        assert runs[1].outcome is None
        assert runs[1].ended_at is None
        assert any(event.kind == "unblocked" for event in events)
        assert any(event.kind == "retry_prepared" for event in events)
    finally:
        conn.close()

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "executing"
    assert workflow["queue_state"] == "kanban_dispatched"
    assert workflow["execution_state"] == "active_executions"
    assert workflow["active_execution_count"] == 1
    assert workflow["recovery_state"] == "not_required"
    assert workflow["retry_state"] == "retry_executing"
    assert workflow["retry_start_authority"]["next_attempt_number"] == 2
    assert workflow["next_action"]["id"] == "MONITOR_P18_9_0_EXECUTION"

    replay = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("idempotent retry replay must not spawn"),
    )
    assert replay["idempotent_replay"] is True
    assert replay["retry_start_authorization_SHA256"] == result["retry_start_authorization_SHA256"]
    assert replay["kanban_run_count"] == 2
    assert replay["current_invocation_side_effects"]["dispatch_performed"] is False
    assert replay["historical_action_result"]["dispatch_performed"] is True
    assert replay["dispatch_performed"] is False


def test_failed_retry_start_record_does_not_bypass_new_recovery_cycle(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    run_1 = _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    first_recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert first_recovery["recovery_status"] == "retry_pending"
    first_cycle = first_recovery["recovery_cycle_id"]

    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda projection, enabled=True: _ready_worker_credential_probe(),
    )
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 34692)
    first_retry = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 34692,
    )
    assert first_retry["retry_start_status"] == "started"
    assert first_retry["recovery_cycle_id"] == first_cycle
    run_2 = first_retry["kanban_run_id"]

    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: False)
    failed_workflow = pr.build_workflow_control_snapshot()
    assert failed_workflow["workflow_status"] == "execution_failed"
    assert failed_workflow["recovery_state"] == "recovery_required"
    assert failed_workflow["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"
    assert failed_workflow["worker_lifecycle"]["latest_run_outcome"] == "crashed"

    second_recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert second_recovery["idempotent_replay"] is False
    assert second_recovery["recovery_status"] == "retry_pending"
    assert second_recovery["recovery_action_SHA256"] != first_recovery["recovery_action_SHA256"]
    assert second_recovery["recovery_cycle_id"] != first_cycle
    assert second_recovery["latest_failed_run_id"] == run_2
    assert second_recovery["observed_attempt_count"] == 2
    assert second_recovery["next_attempt_number"] == 3

    assert pr.p18_9_0_recovery_action_history_path().exists()
    assert pr.p18_9_0_retry_start_record_path().exists()
    projection_record = projection.load_p18_9_0_kanban_projection_record()
    old_retry_record = pr.load_p18_9_0_retry_start_record(
        projection_record=projection_record,
        recovery_record=pr.load_p18_9_0_recovery_action_record(projection_record=projection_record),
        allow_historical_mismatch=True,
    )
    assert old_retry_record is not None
    assert old_retry_record["recovery_cycle_id"] == first_cycle

    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 7777)
    second_retry = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 7777,
    )
    assert second_retry["idempotent_replay"] is False
    assert second_retry["retry_start_status"] == "started"
    assert second_retry["recovery_cycle_id"] == second_recovery["recovery_cycle_id"]
    assert second_retry["retry_start_authorization_SHA256"] != first_retry["retry_start_authorization_SHA256"]
    assert second_retry["latest_failed_run_id"] == run_2
    assert second_retry["previous_attempt_count"] == 2
    assert second_retry["next_attempt_number"] == 3
    assert second_retry["kanban_run_count"] == 3
    assert second_retry["worker_process_started"] is True
    assert second_retry["Git_mutation"] is False
    assert second_retry["auto_retry"] is False
    assert second_retry["auto_rollback"] is False
    assert pr.p18_9_0_retry_start_history_path().exists()

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert [run.id for run in runs] == [run_1, run_2, second_retry["kanban_run_id"]]
        assert runs[0].status == "crashed"
        assert runs[1].status == "crashed"
        assert runs[2].status == "running"
    finally:
        conn.close()


def test_recovered_historical_dead_pid_does_not_reblock_retry_run_3(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    run_1 = _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    run_2 = _force_additional_projected_crashed_run(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        pid=34692,
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("retry must require recovery first"),
    )
    assert result["retry_start_status"] == "blocked"
    assert result["blocker_code"] == "RECOVERY_AUTHORITY_GAP"

    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert recovery["recovery_status"] == "retry_pending"
    assert recovery["observed_attempt_count"] == 2
    assert recovery["max_attempts"] == 3
    assert recovery["next_attempt_number"] == 3
    assert recovery["latest_failed_run_id"] == run_2
    assert recovery["execution_started"] is False
    assert recovery["auto_retry"] is False
    assert recovery["auto_rollback"] is False

    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda projection, enabled=True: _ready_worker_credential_probe(),
    )
    original_unblock = kanban_db.unblock_task
    monkeypatch.setattr(kanban_db, "unblock_task", lambda *_args, **_kwargs: False)

    blocked = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("blocked prep must not spawn"),
    )
    assert blocked["retry_start_status"] == "blocked"
    assert blocked["blocker_code"] == "KANBAN_UNBLOCK_FAILED"
    assert blocked["kanban_run_id"] is None
    assert blocked["kanban_run_count"] == 2
    assert blocked["execution_started"] is False
    assert blocked["worker_process_started"] is False

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "retry_pending"
    assert workflow["recovery_state"] == "retry_pending"
    assert workflow["blocker_count"] == 0
    assert workflow["next_action"]["id"] == "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    assert workflow["retry_start_blocker"]["blocker_code"] == "KANBAN_UNBLOCK_FAILED"
    assert workflow["retry_start_blocker"]["historical_lifecycle_blocker_consumed"] is True
    assert "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED" not in json.dumps(workflow)

    monkeypatch.setattr(kanban_db, "unblock_task", original_unblock)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 5555)
    retry = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 5555,
    )

    assert retry["retry_start_status"] == "started"
    assert retry["previous_attempt_count"] == 2
    assert retry["next_attempt_number"] == 3
    assert retry["latest_failed_run_id"] == run_2
    assert retry["kanban_run_count"] == 3
    assert retry["worker_process_started"] is True
    assert retry["Git_mutation"] is False
    assert retry["auto_retry"] is False
    assert retry["auto_rollback"] is False

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.current_run_id == retry["kanban_run_id"]
        assert task.worker_pid == 5555
        assert [run.id for run in runs] == [run_1, run_2, retry["kanban_run_id"]]
        assert runs[0].status == "crashed"
        assert runs[0].outcome == "crashed"
        assert runs[1].status == "crashed"
        assert runs[1].outcome == "crashed"
        assert "34692" in (runs[1].error or "")
        assert "not alive" in (runs[1].error or "")
        assert runs[2].status == "running"
        assert runs[2].ended_at is None
    finally:
        conn.close()


def test_recovered_retry_blocks_current_active_worker(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert recovery["recovery_status"] == "retry_pending"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.unblock_task(conn, projected["kanban_task_id"])
        conn.execute(
            "UPDATE tasks SET worker_pid = ? WHERE id = ?",
            (5555, projected["kanban_task_id"]),
        )
        conn.commit()
    finally:
        conn.close()
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 5555)

    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("active worker must block retry"),
    )
    assert result["retry_start_status"] == "blocked"
    assert result["blocker_code"] == "EXECUTION_ALREADY_ACTIVE"
    assert result["worker_process_started"] is False


def test_recovered_retry_blocks_current_unresolved_claim(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
        task_skills=("codebase-inspection",),
    )
    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )
    assert recovery["recovery_status"] == "retry_pending"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.unblock_task(conn, projected["kanban_task_id"])
        conn.execute(
            "UPDATE tasks SET claim_lock = ?, claim_expires = ? WHERE id = ?",
            ("unresolved-current-claim", int(time.time()) + 3600, projected["kanban_task_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.0.",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("unresolved claim must block retry"),
    )
    assert result["retry_start_status"] == "blocked"
    assert result["blocker_code"] == "WORKER_LIFECYCLE_RECONCILIATION_REQUIRED"
    assert "unresolved current claim" in result["blocker_detail"]
    assert result["worker_process_started"] is False


def test_recover_current_ticket_execution_blocks_workpacket_authority_drift(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    _force_projected_execution_failure(
        projected=projected,
        pr=pr,
        kanban_db=kanban_db,
        monkeypatch=monkeypatch,
    )
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "execution_failed"

    synthetic_work_packet_id = (
        f"WP-{projected['kanban_board_slug'].upper()}-"
        f"{projected['kanban_task_id'].upper()}"
    )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        body = json.loads(task.body or "{}")
        body["WorkPacket_ID"] = synthetic_work_packet_id
        conn.execute(
            "UPDATE tasks SET body = ? WHERE id = ?",
            (json.dumps(body), projected["kanban_task_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    result = pr.recover_current_ticket_execution(
        human_authorization_text=pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="RECOVER_P18_9_0_EXECUTION",
    )

    assert result["recovery_status"] == "blocked"
    assert result["blocker_code"] == "WORKPACKET_AUTHORITY_DRIFT_GAP"
    assert result["future_retry_prepared"] is False
    assert result["retry_execution_count"] == 0
    assert result["Kanban_requeue_calls"] == 0
    assert result["execution_started"] is False
    assert not pr.p18_9_0_recovery_action_record_path().exists()


def test_future_projection_capability_resolution_has_no_unresolved_task_skill(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()

    projected = _project_via_runtime()

    assert projected["task_skills"] == []
    assert projected["semantic_capabilities"] == ["codebase-inspection"]
    assert projected["capability_resolution"] == [
        {
            "semantic_capability": "codebase-inspection",
            "resolved_surface": "profile_toolset",
            "toolset": "pepper_repository",
            "hermes_task_skill": None,
        }
    ]
    assert "pepper_repository" in projected["profile_toolsets"]


def test_prepare_current_ticket_review_binds_completed_run_to_acceptance_contract(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    generation, _decision = _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda projection, enabled=True: _ready_worker_credential_probe(),
    )
    started = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )
    assert started["start_status"] == "started"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        ok = kanban_db.complete_task(
            conn,
            projected["kanban_task_id"],
            summary=(
                "Summary\nP18.9.0 inventory, IA decision, and acceptance contract "
                "prepared.\nFiles inspected\n- bounded Pepper authorities\nFiles "
                "modified\n- none\nTests/commands run\n- none\nDecisions made\n- "
                "read-only handoff\nLimitations\n- awaits human review acceptance"
            ),
            metadata={
                "files_inspected": ["2_products/pepper-agent/hermes_cli/agent_platform/product_runtime.py"],
                "files_modified": [],
                "tests_run": [],
                "Git_mutation": False,
            },
            expected_run_id=started["kanban_run_id"],
        )
        assert ok is True
    finally:
        conn.close()

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_0_REVIEW"

    result = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="PREPARE_P18_9_0_REVIEW",
    )

    assert result["source_system"] == pr.PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM
    assert result["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert result["review_preparation_recorded"] is True
    assert result["successful_run_id"] == started["kanban_run_id"]
    assert result["acceptance_contract"]["acceptance_criteria"] == list(
        generation["ticket_spec"]["acceptance_criteria"]
    )
    assert result["acceptance_contract"]["response_contract"] == generation["ticket_spec"]["response_contract"]
    assert result["acceptance_contract"]["completion_verdict"] == (
        "p18_9_0_inventory_ia_acceptance_contract_ready"
    )
    assert result["kanban_completion_result"]["completion_detail_sources"] == [
        "task_runs.summary",
        "task_runs.metadata",
    ]
    assert result["human_acceptance_required"] is True
    assert result["human_acceptance_recorded"] is False
    assert result["git_handoff_required"] is False
    assert result["git_handoff_state"] == "not_required_for_ticket_result"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["human_smoke_marker"] == (
        "PEPPER-REVIEW-PREPARE-ACTION-READY-FOR-HUMAN-SMOKE"
    )
    assert result["next_action"]["id"] == "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"

    record = pr.load_p18_9_0_review_prepare_record()
    assert record is not None
    assert record["review_prepare_action_SHA256"] == result["review_prepare_action_SHA256"]
    assert record["review_package_SHA256"] == result["review_package_SHA256"]

    prepared_workflow = pr.build_workflow_control_snapshot()
    assert prepared_workflow["workflow_status"] == "review_prepared_pending_human_acceptance"
    assert prepared_workflow["validation_state"] == "review_prepared_pending_human_acceptance"
    assert prepared_workflow["review_state"] == "prepared_pending_human_acceptance"
    assert prepared_workflow["git_handoff_state"] == "not_required_for_ticket_result"
    assert prepared_workflow["next_action"]["id"] == "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"
    assert prepared_workflow["blocker_count"] == 0

    replay = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="PREPARE_P18_9_0_REVIEW",
    )
    assert replay["idempotent_replay"] is True
    assert replay["review_prepare_action_SHA256"] == result["review_prepare_action_SHA256"]
    assert replay["current_invocation_side_effects"]["dispatch_performed"] is False
    assert replay["current_invocation_side_effects"]["Git_mutation"] is False


def test_accept_current_ticket_review_closes_p18_9_0_and_exposes_next_ticket(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _generation, _projected, started, review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    result = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )

    assert result["source_system"] == pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM
    assert result["review_acceptance_status"] == "accepted"
    assert result["review_acceptance_recorded"] is True
    assert result["successful_run_id"] == started["kanban_run_id"]
    assert result["review_prepare_action_SHA256"] == review["review_prepare_action_SHA256"]
    assert result["review_package_SHA256"] == review["review_package_SHA256"]
    assert result["human_acceptance_text"] == pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT
    assert result["human_acceptance_required"] is True
    assert result["human_acceptance_recorded"] is True
    assert result["ticket_closed"] is True
    assert result["P18_9_0_closed"] is True
    assert result["workflow_status"] == "completed"
    assert result["validation_state"] == "review_accepted"
    assert result["review_state"] == "accepted"
    assert result["git_handoff_required"] is False
    assert result["git_handoff_state"] == "not_required_for_ticket_result"
    assert result["next_ticket_id"] == "P18.9.1"
    assert result["next_ticket_title"] == "Pepper Shell, Routing, and Compact Navigation"
    assert result["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["human_smoke_marker"] == pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_READY_MARKER

    record = pr.load_p18_9_0_review_acceptance_record()
    assert record is not None
    assert record["review_acceptance_action_SHA256"] == result["review_acceptance_action_SHA256"]
    assert record["next_ticket_authority"]["auto_generated"] is False
    assert record["next_ticket_authority"]["execution_authorized"] is False

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "completed"
    assert workflow["current_ticket_id"] is None
    assert workflow["next_ticket_id"] == "P18.9.1"
    assert workflow["next_ticket_title"] == "Pepper Shell, Routing, and Compact Navigation"
    assert workflow["human_acceptance_required"] is False
    assert workflow["human_acceptance_recorded"] is True
    assert workflow["P18_9_0_closed"] is True
    assert workflow["next_ticket_ready"] is True
    assert workflow["next_ticket_generated"] is False
    assert "P18_9_1_ready" not in workflow
    assert "P18_9_1_generated" not in workflow
    assert workflow["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert workflow["blocker_count"] == 0

    import tools.pepper_workflow_tools as pepper_tools

    current_ticket = json.loads(pepper_tools._get_current_ticket({}))
    pending_approvals = json.loads(pepper_tools._get_pending_approvals({}))
    workflow_control = json.loads(pepper_tools._get_workflow_control({}))
    next_action = json.loads(pepper_tools._get_next_action({}))

    assert current_ticket["success"] is True
    assert current_ticket["current_ticket_id"] is None
    assert current_ticket["message"] == "no active governed ticket"
    assert pending_approvals["success"] is True
    assert pending_approvals["pending_approval_count"] == 0
    assert workflow_control["success"] is True
    assert workflow_control["current_ticket_id"] is None
    assert workflow_control["pending_approval_count"] == 0
    assert workflow_control["active_execution_count"] == 0
    assert workflow_control["next_ticket_id"] == "P18.9.1"
    assert workflow_control["next_ticket_title"] == "Pepper Shell, Routing, and Compact Navigation"
    assert next_action["success"] is True
    assert next_action["current_ticket_id"] is None
    assert next_action["next_ticket_id"] == "P18.9.1"
    assert next_action["next_ticket_title"] == "Pepper Shell, Routing, and Compact Navigation"
    assert next_action["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"

    replay = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )
    assert replay["idempotent_replay"] is True
    assert replay["review_acceptance_action_SHA256"] == result["review_acceptance_action_SHA256"]
    assert replay["current_invocation_side_effects"]["dispatch_performed"] is False
    assert replay["current_invocation_side_effects"]["Git_mutation"] is False


def test_historical_review_acceptance_recomputes_current_next_ticket(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _generation, _projected, _started, _review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )
    record = pr.load_p18_9_0_review_acceptance_record()
    assert record is not None

    legacy_next_ticket = {
        "authority_path": "2_products/pepper-agent/docs/agent-platform/workflow_migration_closure.md",
        "authority_section": "Advisory decomposition only, not implementation tickets",
        "authority_type": "current_repository_roadmap_authority",
        "auto_generated": False,
        "execution_authorized": False,
        "next_action_id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION",
        "ticket_id": "P18.9.1",
        "ticket_title": "Pepper Design System",
    }
    record["next_ticket_authority"] = legacy_next_ticket
    record["next_ticket_id"] = legacy_next_ticket["ticket_id"]
    record["next_ticket_title"] = legacy_next_ticket["ticket_title"]
    record["next_ticket_authority_path"] = legacy_next_ticket["authority_path"]
    record["next_action"] = {
        "id": legacy_next_ticket["next_action_id"],
        "label": (
            "P18.9.0 is accepted and closed; P18.9.1 Pepper Design System "
            "may be generated only by a separate governed action."
        ),
        "required_human_action": "separate_next_ticket_generation",
        "target_ticket_id": legacy_next_ticket["ticket_id"],
        "target_ticket_title": legacy_next_ticket["ticket_title"],
    }
    record["review_acceptance_action_SHA256"] = pr._review_acceptance_record_digest(record)
    pr.p18_9_0_review_acceptance_record_path().write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    validated = pr.load_p18_9_0_review_acceptance_record()
    workflow = pr.build_workflow_control_snapshot()

    assert validated is not None
    assert validated["next_ticket_title"] == "Pepper Design System"
    assert workflow["next_ticket_id"] == "P18.9.1"
    assert workflow["next_ticket_title"] == "Pepper Shell, Routing, and Compact Navigation"
    assert workflow["next_action"]["target_ticket_title"] == (
        "Pepper Shell, Routing, and Compact Navigation"
    )


def test_closed_p18_9_0_with_queued_p18_9_1_reconstructs_current_ticket(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected_next, next_authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    projection.kanban_projection_record_path_for_ticket("P18.9.0").touch()
    workflow = pr.build_workflow_control_snapshot()
    binding = pr.resolve_current_ticket_lifecycle_binding()

    assert workflow["P18_9_0_closed"] is True
    assert workflow["P18_9_0_review_acceptance_present"] is True
    assert workflow["current_ticket_id"] == "P18.9.1"
    assert workflow["current_ticket_title"] == _P18_9_1_TITLE
    assert workflow["workflow_status"] == "queued"
    assert workflow["workflow_state"] == "P18.9.1-QUEUED-NOT-EXECUTING"
    assert workflow["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert workflow["next_action"]["id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert workflow["next_action"]["target_ticket_id"] == "P18.9.1"
    assert workflow["kanban_projection_authority"]["projection_SHA256"] == (
        next_authority["projection_SHA256"]
    )
    assert workflow["blocker_count"] == 0
    assert workflow["remaining_blockers"] == []
    assert binding.ticket_id == "P18.9.1"
    assert binding.work_packet_id == next_authority["work_packet_id"]


def test_closed_p18_9_0_with_active_p18_9_1_reconstructs_executing(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    started = _start_p18_9_1_execution(pr, monkeypatch, pid=5321)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 5321)

    workflow = pr.build_workflow_control_snapshot()

    assert workflow["current_ticket_id"] == "P18.9.1"
    assert workflow["workflow_status"] == "executing"
    assert workflow["workflow_state"] == "P18.9.1-EXECUTING"
    assert workflow["queue_state"] == "kanban_dispatched"
    assert workflow["execution_state"] == "active_executions"
    assert workflow["active_execution_count"] == 1
    assert workflow["review_state"] == "not_started_execution_in_progress"
    assert workflow["next_action"]["id"] == "MONITOR_P18_9_1_EXECUTION"
    assert workflow["next_action"]["target_ticket_id"] == "P18.9.1"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == started["kanban_run_id"]
        assert runs[-1].status == "running"
    finally:
        conn.close()


def test_closed_p18_9_0_p18_9_1_latest_completed_run_prepares_review(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    first = _start_p18_9_1_execution(pr, monkeypatch, pid=6101)
    _block_projected_run(
        kanban_db,
        projected,
        first["kanban_run_id"],
        reason="synthetic first P18.9.1 attempt blocked before completion",
        kind="needs_input",
    )
    latest_run_id = _claim_next_projected_run(kanban_db, projected, pid=6102)
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.complete_task(
            conn,
            projected["kanban_task_id"],
            summary=(
                "Summary\nP18.9.1 implementation completed after a prior blocked run.\n"
                "Files inspected\n- synthetic\nFiles modified\n- synthetic\n"
                "Tests/commands run\n- synthetic\nDecisions made\n- latest run wins\n"
                "Limitations\n- awaits review"
            ),
            metadata={"files_modified": ["synthetic"], "Git_mutation": False},
            expected_run_id=latest_run_id,
        )
    finally:
        conn.close()

    workflow = pr.build_workflow_control_snapshot()

    assert workflow["current_ticket_id"] == "P18.9.1"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["workflow_state"] == "P18.9.1-EXECUTION-COMPLETED"
    assert workflow["queue_state"] == "kanban_execution_terminal"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_1_REVIEW"
    assert workflow["next_action"]["target_ticket_id"] == "P18.9.1"
    assert workflow["blocker_count"] == 0


@pytest.mark.parametrize(
    ("status", "outcome", "expected_category"),
    (
        ("failed", "failed", "failed"),
        ("cancelled", "cancelled", "cancelled"),
    ),
)
def test_closed_p18_9_0_p18_9_1_terminal_run_requires_recovery(
    projection_home,
    monkeypatch,
    status,
    outcome,
    expected_category,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    started = _start_p18_9_1_execution(pr, monkeypatch, pid=6201)
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        started["kanban_run_id"],
        status=status,
        outcome=outcome,
        summary=f"synthetic P18.9.1 terminal {outcome} outcome",
    )

    workflow = pr.build_workflow_control_snapshot()

    assert workflow["current_ticket_id"] == "P18.9.1"
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["workflow_state"] == "P18.9.1-EXECUTION-FAILED-RECOVERY-REQUIRED"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["review_state"] == "not_started_execution_failed"
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["failure_category"] == expected_category
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"
    assert workflow["next_action"]["target_ticket_id"] == "P18.9.1"
    assert workflow["blocker_count"] == 1


def test_closed_p18_9_0_p18_9_1_run_without_start_authority_stays_queued(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_id = _claim_next_projected_run(kanban_db, projected, pid=6301)
    _block_projected_run(
        kanban_db,
        projected,
        run_id,
        reason="ungoverned projected task run must not override missing start authority",
        kind="needs_input",
    )

    workflow = pr.build_workflow_control_snapshot()

    assert not pr.execution_start_record_path_for_ticket("P18.9.1").exists()
    assert workflow["current_ticket_id"] == "P18.9.1"
    assert workflow["workflow_status"] == "queued"
    assert workflow["workflow_state"] == "P18.9.1-QUEUED-NOT-EXECUTING"
    assert workflow["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert workflow["next_action"]["id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert workflow["blocker_count"] == 0


def test_closed_p18_9_0_p18_9_1_run_4_blocked_reconstructs_tool_surfaces(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db
    import tools.pepper_workflow_tools as pepper_tools

    first = _start_p18_9_1_execution(pr, monkeypatch, pid=6401)
    _block_projected_run(
        kanban_db,
        projected,
        first["kanban_run_id"],
        reason="synthetic P18.9.1 run 2 blocked",
        kind="needs_input",
    )
    run_3 = _claim_next_projected_run(kanban_db, projected, pid=6402)
    _block_projected_run(
        kanban_db,
        projected,
        run_3,
        reason="synthetic P18.9.1 run 3 blocked",
        kind="capability",
    )
    run_4 = _claim_next_projected_run(kanban_db, projected, pid=6403)
    assert run_4 == 4
    _block_projected_run(
        kanban_db,
        projected,
        run_4,
        reason="WORKSPACE_PATH_ESCAPE: worker workspace path escaped canonical repo",
        kind="transient",
    )

    workflow = pr.build_workflow_control_snapshot()
    context = pr.build_lead_agent_operational_context()
    execution_status = json.loads(pepper_tools._get_execution_status({}))
    workflow_control = json.loads(pepper_tools._get_workflow_control({}))
    review_status = json.loads(pepper_tools._get_review_status({}))
    next_action = json.loads(pepper_tools._get_next_action({}))
    replay = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.1 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("initial start must replay, not dispatch again"),
    )

    assert workflow["current_ticket_id"] == "P18.9.1"
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["execution_state"] == "no_active_executions"
    assert workflow["active_execution_count"] == 0
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["failure_category"] == "blocked"
    assert "WORKSPACE_PATH_ESCAPE" in workflow["failure_summary"]
    assert workflow["worker_lifecycle"]["runs"][-1]["id"] == run_4
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"

    assert context["workflow_status"] == "execution_failed"
    assert context["current_ticket_id"] == "P18.9.1"
    assert context["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"
    assert execution_status["execution_state"] == "no_active_executions"
    assert execution_status["active_execution_count"] == 0
    assert execution_status["recent_executions"][0]["id"] == run_4
    assert execution_status["recent_executions"][0]["status"] == "blocked"
    assert execution_status["recent_executions"][0]["failure_category"] == "blocked"
    assert workflow_control["workflow_status"] == "execution_failed"
    assert workflow_control["recovery_state"] == "recovery_required"
    assert workflow_control["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"
    assert review_status["review_state"] == "not_started_execution_failed"
    assert review_status["recovery_state"] == "recovery_required"
    assert next_action["workflow_status"] == "execution_failed"
    assert next_action["recovery_state"] == "recovery_required"
    assert next_action["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"
    assert replay["idempotent_replay"] is True
    assert replay["start_status"] == "failed"
    assert replay["dispatch_performed"] is True


def test_current_p18_9_1_recovery_records_retry_pending_without_run_5(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    failed = pr.build_workflow_control_snapshot()
    assert failed["workflow_status"] == "execution_failed"
    assert failed["recovery_state"] == "recovery_required"
    assert failed["active_execution_count"] == 0
    assert failed["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"

    recovery_text = pr.governed_ticket_recovery_authorization_text("P18.9.1")
    retry_with_recovery_text = pr.start_current_ticket_execution(
        human_authorization_text=recovery_text,
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("recovery text must not start retry"),
    )
    assert retry_with_recovery_text["retry_start_status"] == "blocked"
    assert retry_with_recovery_text["blocker_code"] == "EXECUTION_AUTHORIZATION_KIND_MISMATCH"

    retry_text_recovery = "Autorizo explícitamente el retry de P18.9.1."
    with pytest.raises(pr.ProductRuntimeDecisionFailed):
        pr.recover_current_ticket_execution(
            human_authorization_text=retry_text_recovery,
            project_id="PEPPER",
            ticket_id="P18.9.1",
            next_action_id="RECOVER_P18_9_1_EXECUTION",
        )

    result = pr.recover_current_ticket_execution(
        human_authorization_text=recovery_text,
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )

    assert result["recovery_status"] == "retry_pending"
    assert result["ticket_id"] == "P18.9.1"
    assert result["latest_failed_run_id"] == run_4
    assert result["observed_attempt_count"] == 3
    assert result["next_attempt_number"] == 4
    assert result["recovery_authorization_recorded"] is True
    assert result["future_retry_requires_separate_start_authorization"] is True
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["retry_execution_started"] is False
    assert result["retry_execution_count"] == 0
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["Git_mutation"] is False
    assert result["kanban_run_count"] == 3
    assert result["second_run_started"] is False
    assert pr.recovery_action_record_path_for_ticket("P18.9.1").exists()
    assert not pr.p18_9_0_recovery_action_record_path().exists()
    record = pr.load_current_ticket_recovery_action_record(projection_record=authority)
    assert record is not None
    assert record["ticket_id"] == "P18.9.1"
    assert record["human_authorization_text"] == recovery_text
    assert record["latest_failed_run_id"] == run_4

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "retry_pending"
    assert workflow["workflow_state"] == "P18.9.1-RETRY-PENDING-NOT-DISPATCHED"
    assert workflow["recovery_state"] == "retry_pending"
    assert workflow["next_action"]["id"] == "START_P18_9_1_RETRY_REQUIRES_HUMAN_AUTHORIZATION"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.current_run_id is None
        assert runs[-1].id == run_4
        assert all(run.id <= run_4 for run in runs)
        assert all(run.id != 5 for run in runs)
        assert runs[-1].status == "blocked"
    finally:
        conn.close()


def test_current_p18_9_1_recovery_rejects_wrong_ticket_guard(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    with pytest.raises(pr.ProductRuntimeConflict) as excinfo:
        pr.recover_current_ticket_execution(
            human_authorization_text=pr.governed_ticket_recovery_authorization_text("P18.9.1"),
            project_id="PEPPER",
            ticket_id="P18.9.0",
            next_action_id="RECOVER_P18_9_1_EXECUTION",
        )

    assert "bounded to ticket P18.9.1" in str(excinfo.value)
    assert not pr.recovery_action_record_path_for_ticket("P18.9.1").exists()


def test_current_p18_9_1_retry_start_rejects_superseded_recovery_run(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text("P18.9.1"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )
    assert recovery["latest_failed_run_id"] == run_4

    run_5 = _claim_next_projected_run(kanban_db, projected, pid=6505)
    _block_projected_run(
        kanban_db,
        projected,
        run_5,
        reason="synthetic P18.9.1 later run superseded prior recovery",
        kind="transient",
    )
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda projection, enabled=True: _ready_worker_credential_probe(),
    )

    result = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo explícitamente el retry de P18.9.1.",
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="START_P18_9_1_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("superseded recovery must not spawn"),
    )

    assert result["retry_start_status"] == "blocked"
    assert result["blocker_code"] == "KANBAN_RETRY_SOURCE_GAP"
    assert "latest failed run no longer matches" in result["blocker_detail"]
    assert result["retry_source"]["latest_run_id"] == run_5
    assert pr.load_current_ticket_recovery_action_record(projection_record=authority)[
        "latest_failed_run_id"
    ] == run_4


def test_current_p18_9_1_recovery_blocks_completed_or_active_execution(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    active = _start_p18_9_1_execution(pr, monkeypatch, pid=6601)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6601)
    active_result = pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text("P18.9.1"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )
    assert active_result["recovery_status"] == "blocked"
    assert active_result["blocker_code"] == "WORKFLOW_RECOVERY_ACTION_GAP"
    assert active_result["execution_started"] is False
    assert not pr.recovery_action_record_path_for_ticket("P18.9.1").exists()

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.complete_task(
            conn,
            projected["kanban_task_id"],
            summary=(
                "Summary\nP18.9.1 implementation completed.\nFiles inspected\n- synthetic\n"
                "Files modified\n- synthetic\nTests/commands run\n- synthetic\n"
                "Decisions made\n- synthetic\nLimitations\n- awaits review"
            ),
            metadata={"files_modified": ["synthetic"], "Git_mutation": False},
            expected_run_id=active["kanban_run_id"],
        )
    finally:
        conn.close()

    completed = pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text("P18.9.1"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )
    assert completed["recovery_status"] == "blocked"
    assert completed["blocker_code"] == "WORKFLOW_RECOVERY_ACTION_GAP"
    assert completed["execution_started"] is False
    assert not pr.recovery_action_record_path_for_ticket("P18.9.1").exists()


def test_terminal_acceptance_preserves_historical_review_prepare_contract(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _generation, projected, _started, review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    accepted = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )
    authority = _projection_authority_record(projected)
    original_contract = dict(review["acceptance_contract"])
    monkeypatch.setattr(
        pr,
        "_p18_9_0_acceptance_contract",
        lambda: _drifted_acceptance_contract(pr, original_contract),
    )

    validated_prepare = pr.load_p18_9_0_review_prepare_record(projection_record=authority)
    validated_acceptance = pr.load_p18_9_0_review_acceptance_record(
        projection_record=authority,
        review_prepare_record=validated_prepare,
    )

    assert validated_prepare is not None
    assert validated_prepare["acceptance_contract_SHA256"] == review["acceptance_contract_SHA256"]
    assert validated_prepare["acceptance_contract"] == original_contract
    assert validated_acceptance is not None
    assert validated_acceptance["review_acceptance_action_SHA256"] == (
        accepted["review_acceptance_action_SHA256"]
    )


def test_historical_review_prepare_contract_requires_terminal_acceptance(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _generation, projected, _started, review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    authority = _projection_authority_record(projected)
    original_contract = dict(review["acceptance_contract"])
    monkeypatch.setattr(
        pr,
        "_p18_9_0_acceptance_contract",
        lambda: _drifted_acceptance_contract(pr, original_contract),
    )

    with pytest.raises(pr.ProductRuntimeConflict) as excinfo:
        pr.load_p18_9_0_review_prepare_record(projection_record=authority)

    message = str(excinfo.value)
    assert "review-preparation record acceptance_contract_SHA256 mismatch" in message
    assert "expected_historical=" + review["acceptance_contract_SHA256"] in message


def test_review_prepare_contract_tampering_still_blocks_with_terminal_acceptance(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _generation, projected, _started, review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    accepted = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )
    authority = _projection_authority_record(projected)
    tampered = dict(pr.load_p18_9_0_review_prepare_record(projection_record=authority) or {})
    tampered["acceptance_contract_SHA256"] = "f" * 64
    tampered["review_prepare_action_SHA256"] = pr._review_prepare_record_digest(tampered)

    with pytest.raises(pr.ProductRuntimeConflict) as excinfo:
        pr.validate_p18_9_0_review_prepare_record(
            tampered,
            projection_record=authority,
        )

    message = str(excinfo.value)
    assert "review-preparation record acceptance_contract_SHA256 mismatch" in message
    assert "persisted=" + "f" * 64 in message
    assert "expected_historical=" + review["acceptance_contract_SHA256"] in message
    assert accepted["review_acceptance_action_SHA256"] == (
        pr.load_p18_9_0_review_acceptance_record(projection_record=authority)[
            "review_acceptance_action_SHA256"
        ]
    )


def test_accept_current_ticket_review_requires_prepared_review_authority(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    _project_via_runtime()

    from hermes_cli.agent_platform import product_runtime as pr

    result = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )

    assert result["review_acceptance_status"] == "blocked"
    assert result["blocker_code"] == "REVIEW_PREPARE_AUTHORITY_GAP"
    assert result["review_acceptance_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["Git_mutation"] is False
    assert not pr.p18_9_0_review_acceptance_record_path().exists()


def test_prepare_current_ticket_review_replays_acceptance_after_closure(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _generation, _projected, _started, review = _prepare_completed_review_package(monkeypatch)

    from hermes_cli.agent_platform import product_runtime as pr

    accepted = pr.accept_current_ticket_review(
        human_acceptance_text=pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT,
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    )
    replay = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="PREPARE_P18_9_0_REVIEW",
    )

    assert replay["idempotent_replay"] is True
    assert replay["review_acceptance_status"] == "accepted"
    assert replay["review_acceptance_action_SHA256"] == accepted["review_acceptance_action_SHA256"]
    assert replay["review_prepare_action_SHA256"] == review["review_prepare_action_SHA256"]
    assert replay["P18_9_0_closed"] is True
    assert replay["next_ticket_id"] == "P18.9.1"


def test_prepare_current_ticket_review_blocks_without_structural_completion_detail(
    projection_home,
    monkeypatch,
) -> None:
    _install_execution_profile(monkeypatch, projection_home)
    _approve_current_ticket()
    projected = _project_via_runtime()

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda projection, enabled=True: _ready_worker_credential_probe(),
    )
    started = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 4321,
    )

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        now = int(time.time())
        conn.execute(
            "UPDATE tasks SET status = 'done', completed_at = ?, current_run_id = NULL, "
            "claim_lock = NULL, claim_expires = NULL, worker_pid = NULL, result = NULL "
            "WHERE id = ?",
            (now, projected["kanban_task_id"]),
        )
        conn.execute(
            "UPDATE task_runs SET status = 'done', outcome = 'completed', ended_at = ?, "
            "summary = NULL, metadata = NULL, error = NULL WHERE id = ?",
            (now, started["kanban_run_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_0_REVIEW"

    result = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="PREPARE_P18_9_0_REVIEW",
    )

    assert result["review_prepare_status"] == "blocked"
    assert result["blocker_code"] == "KANBAN_COMPLETION_RESULT_DETAIL_GAP"
    assert result["review_preparation_recorded"] is False
    assert result["dispatch_performed"] is False
    assert result["Git_mutation"] is False
    assert not pr.p18_9_0_review_prepare_record_path().exists()


def test_chat_tool_prepares_current_ticket_review_with_explicit_request(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}

    def fake_prepare_current_ticket_review(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM,
            "schema_version": pr.PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
            "policy_id": pr.PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID,
            "review_prepare_status": "prepared_pending_human_acceptance",
            "review_preparation_recorded": True,
            "ticket_id": "P18.9.0",
            "successful_run_id": 3,
            "human_acceptance_required": True,
            "human_acceptance_recorded": False,
            "git_handoff_required": False,
            "git_handoff_state": "not_required_for_ticket_result",
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
            "human_smoke_marker": "PEPPER-REVIEW-PREPARE-ACTION-READY-FOR-HUMAN-SMOKE",
            "next_action": {"id": "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"},
        }

    monkeypatch.setattr(pr, "prepare_current_ticket_review", fake_prepare_current_ticket_review)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-REVIEW-PREPARED-PENDING-HUMAN-ACCEPTANCE",
            "workflow_status": "review_prepared_pending_human_acceptance",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_completed_not_dispatched",
            "execution_state": "no_active_executions",
            "validation_state": "review_prepared_pending_human_acceptance",
            "review_state": "prepared_pending_human_acceptance",
            "git_handoff_state": "not_required_for_ticket_result",
            "next_action": {"id": "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"},
        },
    )

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.0 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "PREPARE_P18_9_0_REVIEW",
            },
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "prepare_current_ticket_review"
    assert result["human_request_text"] == "Prepare P18.9.0 review validation now"
    assert result["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert result["workflow_status"] == "review_prepared_pending_human_acceptance"
    assert result["validation_state"] == "review_prepared_pending_human_acceptance"
    assert result["review_state"] == "prepared_pending_human_acceptance"
    assert result["next_action"]["id"] == "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert captured == {
        "project_id": "PEPPER",
        "ticket_id": "P18.9.0",
        "next_action_id": "PREPARE_P18_9_0_REVIEW",
    }


def test_chat_tool_binds_current_user_task_as_review_prepare_request_when_arg_omitted(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = "Prepara la validacion de review de P18.9.0."

    def fake_prepare_current_ticket_review(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_REVIEW_PREPARE_ACTION_SOURCE_SYSTEM,
            "schema_version": pr.PEPPER_REVIEW_PREPARE_ACTION_SCHEMA_VERSION,
            "policy_id": pr.PEPPER_REVIEW_PREPARE_ACTION_POLICY_ID,
            "review_prepare_status": "prepared_pending_human_acceptance",
            "review_preparation_recorded": True,
            "ticket_id": "P18.9.0",
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "prepare_current_ticket_review", fake_prepare_current_ticket_review)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-REVIEW-PREPARED-PENDING-HUMAN-ACCEPTANCE",
            "workflow_status": "review_prepared_pending_human_acceptance",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_completed_not_dispatched",
            "execution_state": "no_active_executions",
            "validation_state": "review_prepared_pending_human_acceptance",
            "review_state": "prepared_pending_human_acceptance",
            "git_handoff_state": "not_required_for_ticket_result",
            "next_action": {"id": "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"},
        },
    )

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "PREPARE_P18_9_0_REVIEW",
            },
            user_task=human_text,
        )
    )

    assert result["success"] is True
    assert result["human_request_text"] == human_text
    assert captured == {
        "project_id": "PEPPER",
        "ticket_id": "P18.9.0",
        "next_action_id": "PREPARE_P18_9_0_REVIEW",
    }


def test_chat_tool_accepts_current_ticket_review_with_exact_human_acceptance(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT

    def fake_accept_current_ticket_review(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM,
            "schema_version": pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION,
            "policy_id": pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID,
            "review_acceptance_status": "accepted",
            "review_acceptance_recorded": True,
            "ticket_id": "P18.9.0",
            "ticket_closed": True,
            "P18_9_0_closed": True,
            "validation_state": "review_accepted",
            "review_state": "accepted",
            "workflow_status": "completed",
            "next_ticket_id": "P18.9.1",
            "next_ticket_title": "Pepper Design System",
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
            "next_action": {"id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"},
        }

    monkeypatch.setattr(pr, "accept_current_ticket_review", fake_accept_current_ticket_review)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": None,
            "workflow_state": "P18.9.0-COMPLETED",
            "workflow_status": "completed",
            "approval_state": "no_pending_approvals",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "p18_9_0_closed_next_ticket_ready",
            "execution_state": "no_active_executions",
            "validation_state": "review_accepted",
            "review_state": "accepted",
            "git_handoff_state": "not_required_for_ticket_result",
            "next_action": {"id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "accept_current_ticket_review",
            {
                "human_acceptance_text": human_text,
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
            },
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "accept_current_ticket_review"
    assert result["human_acceptance_text"] == human_text
    assert result["review_acceptance_status"] == "accepted"
    assert result["workflow_status"] == "completed"
    assert result["validation_state"] == "review_accepted"
    assert result["review_state"] == "accepted"
    assert result["next_action"]["id"] == "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert captured == {
        "human_acceptance_text": human_text,
        "acceptor_id": "pepper-chat-human",
        "project_id": "PEPPER",
        "ticket_id": "P18.9.0",
        "next_action_id": "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
    }


def test_chat_tool_binds_current_user_task_as_review_acceptance_when_arg_omitted(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = pr.PEPPER_CURRENT_REVIEW_ACCEPTANCE_TEXT

    def fake_accept_current_ticket_review(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SOURCE_SYSTEM,
            "schema_version": pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_SCHEMA_VERSION,
            "policy_id": pr.PEPPER_REVIEW_HUMAN_ACCEPTANCE_ACTION_POLICY_ID,
            "review_acceptance_status": "accepted",
            "review_acceptance_recorded": True,
            "ticket_id": "P18.9.0",
            "ticket_closed": True,
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "accept_current_ticket_review", fake_accept_current_ticket_review)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": None,
            "workflow_state": "P18.9.0-COMPLETED",
            "workflow_status": "completed",
            "approval_state": "no_pending_approvals",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "p18_9_0_closed_next_ticket_ready",
            "execution_state": "no_active_executions",
            "validation_state": "review_accepted",
            "review_state": "accepted",
            "git_handoff_state": "not_required_for_ticket_result",
            "next_action": {"id": "GENERATE_P18_9_1_REQUIRES_SEPARATE_HUMAN_ACTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "accept_current_ticket_review",
            {
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE",
            },
            user_task=human_text,
        )
    )

    assert result["success"] is True
    assert result["human_acceptance_text"] == human_text
    assert captured["human_acceptance_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.0"
    assert captured["next_action_id"] == "AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE"


@pytest.mark.parametrize(
    ("user_task", "expected_error"),
    [
        (None, "human_acceptance_text is required"),
        ("¿Acepto la review de P18.9.0?", "must not be a question"),
        ("Acepto la review de P18.9.0", "exact explicit P18.9.0 review acceptance"),
        (
            "Acepto explícitamente la review de P18.9.1 y el resultado preparado para aceptación humana.",
            "exact explicit P18.9.0 review acceptance",
        ),
    ],
)
def test_chat_tool_rejects_missing_or_unsafe_user_task_review_acceptance(
    monkeypatch,
    user_task,
    expected_error,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "accept_current_ticket_review",
        lambda **_kwargs: pytest.fail("review acceptance backend must not be called"),
    )

    result = json.loads(
        handle_function_call(
            "accept_current_ticket_review",
            {},
            user_task=user_task,
        )
    )

    assert result["success"] is False
    assert expected_error in result["error"]


@pytest.mark.parametrize(
    ("user_task", "expected_error"),
    [
        (None, "human_request_text is required"),
        ("Should we prepare P18.9.0 review?", "must not be a question"),
        ("Tal vez preparar la revision de P18.9.0", "ambiguous"),
        ("Prepare P18.9.1 review validation now", "targets a different ticket"),
        ("Summarize P18.9.0", "explicit P18.9.0 review preparation"),
    ],
)
def test_chat_tool_rejects_missing_or_unsafe_user_task_review_prepare_request(
    monkeypatch,
    user_task,
    expected_error,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "prepare_current_ticket_review",
        lambda **_kwargs: pytest.fail("review preparation backend must not be called"),
    )

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {},
            user_task=user_task,
        )
    )

    assert result["success"] is False
    assert expected_error in result["error"]


def test_chat_tool_starts_current_ticket_execution_with_explicit_authorization(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}

    def fake_start_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_WORKER_START_ACTION_POLICY_ID,
            "start_status": "started",
            "ticket_id": "P18.9.0",
            "dispatch_performed": True,
            "execution_started": True,
            "worker_execution": True,
            "Kanban_dispatch": True,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "start_current_ticket_execution", fake_start_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-EXECUTING",
            "workflow_status": "executing",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_dispatched",
            "execution_state": "active_executions",
            "next_action": {"id": "MONITOR_P18_9_0_EXECUTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "human_authorization_text": "Start P18.9.0 execution now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            },
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "start_current_ticket_execution"
    assert result["workflow_status"] == "executing"
    assert captured["human_authorization_text"] == "Start P18.9.0 execution now"
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.0"
    assert captured["next_action_id"] == "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"


def test_chat_tool_binds_current_user_task_as_start_authorization_when_arg_omitted(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = "Autorizo explícitamente el inicio de ejecución de P18.9.0."

    def fake_start_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_WORKER_START_ACTION_POLICY_ID,
            "start_status": "started",
            "ticket_id": "P18.9.0",
            "dispatch_performed": True,
            "execution_started": True,
            "worker_execution": True,
            "Kanban_dispatch": True,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "start_current_ticket_execution", fake_start_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-EXECUTING",
            "workflow_status": "executing",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_dispatched",
            "execution_state": "active_executions",
            "next_action": {"id": "MONITOR_P18_9_0_EXECUTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            },
            user_task=human_text,
        )
    )

    assert result["success"] is True
    assert result["human_authorization_text"] == human_text
    assert captured["human_authorization_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.0"
    assert captured["next_action_id"] == "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"


def test_chat_tool_binds_generic_current_ticket_start_authorization(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = "Start P18.9.1 execution now"

    def fake_start_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_WORKER_START_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_WORKER_START_ACTION_POLICY_ID,
            "start_status": "started",
            "ticket_id": "P18.9.1",
            "dispatch_performed": True,
            "execution_started": True,
            "worker_execution": True,
            "Kanban_dispatch": True,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "start_current_ticket_execution", fake_start_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.1",
            "workflow_state": "P18.9.1-EXECUTING",
            "workflow_status": "executing",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_dispatched",
            "execution_state": "active_executions",
            "next_action": {"id": "MONITOR_P18_9_1_EXECUTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "project_id": "PEPPER",
                "ticket_id": "P18.9.1",
                "next_action_id": "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            },
            user_task=human_text,
        )
    )

    assert result["success"] is True
    assert result["human_authorization_text"] == human_text
    assert result["ticket_id"] == "P18.9.1"
    assert captured["human_authorization_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.1"
    assert captured["next_action_id"] == "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"


def test_chat_tool_rejects_stale_ticket_start_when_context_is_generic_current(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "start_current_ticket_execution",
        lambda **_kwargs: pytest.fail("start backend must not be called"),
    )
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.1",
            "workflow_state": "P18.9.1-QUEUED-NOT-EXECUTING",
            "workflow_status": "queued",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_projection_ready_not_dispatched",
            "execution_state": "not_started",
            "next_action": {
                "id": "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
                "target_ticket_id": "P18.9.1",
            },
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "human_authorization_text": "Start P18.9.0 execution now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.1",
                "next_action_id": "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            },
        )
    )

    assert result["success"] is False
    assert "targets a different ticket" in result["error"]


def test_chat_tool_rejects_retry_text_for_initial_current_ticket_generically(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "start_current_ticket_execution",
        lambda **_kwargs: pytest.fail("start backend must not be called"),
    )
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.1",
            "workflow_state": "P18.9.1-QUEUED-NOT-EXECUTING",
            "workflow_status": "queued",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_projection_ready_not_dispatched",
            "execution_state": "not_started",
            "next_action": {
                "id": "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
                "target_ticket_id": "P18.9.1",
            },
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "human_authorization_text": "Retry P18.9.1 execution now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.1",
                "next_action_id": "START_P18_9_1_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
            },
        )
    )

    assert result["success"] is False
    assert "initial execution start authorization must not be retry authorization" in result["error"]
    assert "P18.9.0 retry-start" not in result["error"]


@pytest.mark.parametrize(
    "human_text",
    [
        "Autorizo explícitamente el retry de P18.9.0.",
        "Reintenta P18.9.0.",
        "Inicia el segundo intento de P18.9.0.",
    ],
)
def test_chat_tool_routes_explicit_retry_start_authorization_to_start_tool(
    monkeypatch,
    human_text,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}

    def fake_start_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_RETRY_START_ACTION_POLICY_ID,
            "start_status": "started",
            "retry_start_status": "started",
            "ticket_id": "P18.9.0",
            "retry_start_authorization_recorded": True,
            "retry_execution_started": True,
            "retry_execution_count": 1,
            "dispatch_performed": True,
            "execution_started": True,
            "worker_execution": True,
            "Kanban_dispatch": True,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "start_current_ticket_execution", fake_start_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-EXECUTING",
            "workflow_status": "executing",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_dispatched",
            "execution_state": "active_executions",
            "recovery_state": "not_required",
            "next_action": {"id": "MONITOR_P18_9_0_EXECUTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
            },
            user_task=human_text,
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "start_current_ticket_execution"
    assert result["human_authorization_text"] == human_text
    assert result["workflow_status"] == "executing"
    assert result["retry_execution_count"] == 1
    assert captured["human_authorization_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.0"
    assert captured["next_action_id"] == "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"


def test_chat_tool_recovers_current_ticket_execution_with_explicit_authorization(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT

    def fake_recover_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_RECOVERY_ACTION_POLICY_ID,
            "P18_6_policy_id": "pepper-retry-incident-rollback-workflow-v1",
            "runtime_boundary_classification": "RECOVERY_DECISION_ONLY",
            "recovery_status": "retry_pending",
            "ticket_id": "P18.9.0",
            "future_retry_prepared": True,
            "future_task_skills": [],
            "future_retry_capability_surface": "pepper_repository",
            "unresolved_Hermes_task_skills": [],
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "retry_execution_count": 0,
            "automatic_retry_count": 0,
            "Kanban_requeue_calls": 0,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "recover_current_ticket_execution", fake_recover_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-RETRY-PENDING-NOT-DISPATCHED",
            "workflow_status": "retry_pending",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_retry_prepared_not_dispatched",
            "execution_state": "no_active_executions",
            "recovery_state": "retry_pending",
            "failure_category": "worker_bootstrap_failure",
            "failure_summary": "worker exited during bootstrap",
            "next_action": {"id": "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "recover_current_ticket_execution",
            {
                "human_authorization_text": human_text,
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "RECOVER_P18_9_0_EXECUTION",
            },
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "recover_current_ticket_execution"
    assert result["workflow_status"] == "retry_pending"
    assert result["future_retry_prepared"] is True
    assert result["future_task_skills"] == []
    assert result["future_retry_capability_surface"] == "pepper_repository"
    assert result["retry_execution_count"] == 0
    assert result["Kanban_requeue_calls"] == 0
    assert captured["human_authorization_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.0"
    assert captured["next_action_id"] == "RECOVER_P18_9_0_EXECUTION"


def test_chat_tool_binds_current_user_task_as_recovery_authorization_when_arg_omitted(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = pr.PEPPER_CURRENT_EXECUTION_RECOVERY_AUTHORIZATION_TEXT

    def fake_recover_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_RECOVERY_ACTION_POLICY_ID,
            "recovery_status": "retry_pending",
            "ticket_id": "P18.9.0",
            "future_retry_prepared": True,
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "recover_current_ticket_execution", fake_recover_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-RETRY-PENDING-NOT-DISPATCHED",
            "workflow_status": "retry_pending",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_retry_prepared_not_dispatched",
            "execution_state": "no_active_executions",
            "recovery_state": "retry_pending",
            "failure_category": "worker_bootstrap_failure",
            "failure_summary": "worker exited during bootstrap",
            "next_action": {"id": "START_P18_9_0_RETRY_REQUIRES_HUMAN_AUTHORIZATION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "recover_current_ticket_execution",
            {
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "RECOVER_P18_9_0_EXECUTION",
            },
            user_task=human_text,
        )
    )

    assert result["success"] is True
    assert result["human_authorization_text"] == human_text
    assert captured["human_authorization_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.0"
    assert captured["next_action_id"] == "RECOVER_P18_9_0_EXECUTION"


def test_chat_tool_recovers_current_p18_9_1_execution_with_generic_authorization(
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    captured = {}
    human_text = pr.governed_ticket_recovery_authorization_text("P18.9.1")

    def fake_recover_current_ticket_execution(**kwargs):
        captured.update(kwargs)
        return {
            "source_system": pr.PEPPER_RECOVERY_ACTION_SOURCE_SYSTEM,
            "schema_version": 1,
            "policy_id": pr.PEPPER_RECOVERY_ACTION_POLICY_ID,
            "recovery_status": "retry_pending",
            "ticket_id": "P18.9.1",
            "future_retry_prepared": True,
            "dispatch_performed": False,
            "execution_started": False,
            "worker_execution": False,
            "Kanban_dispatch": False,
            "Git_mutation": False,
            "auto_retry": False,
            "auto_rollback": False,
        }

    monkeypatch.setattr(pr, "recover_current_ticket_execution", fake_recover_current_ticket_execution)
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.1",
            "workflow_state": "P18.9.1-EXECUTION-FAILED-RECOVERY-REQUIRED",
            "workflow_status": "execution_failed",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_execution_terminal",
            "execution_state": "no_active_executions",
            "recovery_state": "recovery_required",
            "failure_category": "blocked",
            "failure_summary": "WORKSPACE_PATH_ESCAPE",
            "next_action": {"id": "RECOVER_P18_9_1_EXECUTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "recover_current_ticket_execution",
            {
                "human_authorization_text": human_text,
                "project_id": "PEPPER",
                "ticket_id": "P18.9.1",
                "next_action_id": "RECOVER_P18_9_1_EXECUTION",
            },
        )
    )

    assert result["success"] is True
    assert result["source_tool"] == "recover_current_ticket_execution"
    assert result["ticket_id"] == "P18.9.1"
    assert captured["human_authorization_text"] == human_text
    assert captured["project_id"] == "PEPPER"
    assert captured["ticket_id"] == "P18.9.1"
    assert captured["next_action_id"] == "RECOVER_P18_9_1_EXECUTION"


@pytest.mark.parametrize(
    ("user_task", "expected_error"),
    [
        (None, "human_authorization_text is required"),
        ("¿Autorizo recuperar P18.9.0?", "must not be a question"),
        ("Autorizo iniciar P18.9.0", "explicit execution recovery authorization text is required"),
        (
            "Autorizo explícitamente la recuperación de la ejecución fallida de P18.9.1.",
            "targets a different ticket",
        ),
    ],
)
def test_chat_tool_rejects_missing_or_unsafe_user_task_recovery_authorization(
    monkeypatch,
    user_task,
    expected_error,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "recover_current_ticket_execution",
        lambda **_kwargs: pytest.fail("recovery backend must not be called"),
    )
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-EXECUTION-FAILED-RECOVERY-REQUIRED",
            "workflow_status": "execution_failed",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_execution_terminal",
            "execution_state": "no_active_executions",
            "recovery_state": "recovery_required",
            "failure_category": "worker_bootstrap_failure",
            "failure_summary": "worker exited during bootstrap",
            "next_action": {"id": "RECOVER_P18_9_0_EXECUTION"},
        },
    )

    result = json.loads(
        handle_function_call(
            "recover_current_ticket_execution",
            {},
            user_task=user_task,
        )
    )

    assert result["success"] is False
    assert expected_error in result["error"]


@pytest.mark.parametrize(
    ("user_task", "expected_error"),
    [
        (None, "human_authorization_text is required"),
        ("Should we start P18.9.0 execution?", "must not be a question"),
        ("¿Podemos reintentarlo?", "must not be a question"),
        ("¿Está listo para retry?", "must not be a question"),
        ("Tal vez iniciar P18.9.0", "ambiguous"),
        ("Parece que ya se puede volver a ejecutar.", "ambiguous"),
        ("Reintenta P18.9.0, por favor", "initial execution start authorization must not be retry authorization"),
        (
            "Autorizo explícitamente la recuperación de la ejecución fallida de P18.9.0.",
            "must not be recovery authorization",
        ),
        ("Start P18.9.1 execution now", "targets a different ticket"),
    ],
)
def test_chat_tool_rejects_missing_or_unsafe_user_task_start_authorization(
    monkeypatch,
    user_task,
    expected_error,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "start_current_ticket_execution",
        lambda **_kwargs: pytest.fail("start backend must not be called"),
    )
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-QUEUED-NOT-EXECUTING",
            "workflow_status": "queued",
            "approval_state": "ticket_approved",
            "pending_approval_count": 0,
            "pending_ticket_approval_count": 0,
            "queue_state": "kanban_projection_ready_not_dispatched",
            "execution_state": "not_started",
            "next_action": {
                "id": "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
                "target_ticket_id": "P18.9.0",
            },
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {},
            user_task=user_task,
        )
    )

    assert result["success"] is False
    assert expected_error in result["error"]


def test_chat_tool_rejects_ambiguous_execution_start_question(monkeypatch) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from hermes_cli.agent_platform import product_runtime as pr
    from model_tools import handle_function_call

    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {
            "current_ticket_id": "P18.9.0",
            "workflow_state": "P18.9.0-QUEUED-NOT-EXECUTING",
            "workflow_status": "queued",
            "queue_state": "kanban_projection_ready_not_dispatched",
            "execution_state": "not_started",
            "next_action": {
                "id": "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
                "target_ticket_id": "P18.9.0",
            },
        },
    )

    result = json.loads(
        handle_function_call(
            "start_current_ticket_execution",
            {"human_authorization_text": "Should we start P18.9.0 execution?"},
        )
    )

    assert result["success"] is False
    assert "must not be a question" in result["error"]
