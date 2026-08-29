from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
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
_P18_9_2_TITLE = "Control Center Overview"
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


def _p18_9_2_workflow(**overrides):
    data = _workflow(
        current_ticket_id=None,
        current_ticket_title=None,
        next_ticket_id="P18.9.2",
        next_ticket_title=_P18_9_2_TITLE,
        workflow_state="P18.9.1-COMPLETED",
        workflow_status="completed",
        queue_state="p18_9_1_closed_next_ticket_ready",
        closed_predecessor_ticket_id="P18.9.1",
        validation_state="review_accepted",
        review_state="accepted",
        P18_9_ticket_generated=True,
        next_ticket_ready=True,
        next_ticket_generated=False,
        next_action={
            "id": "GENERATE_P18_9_2_REQUIRES_SEPARATE_HUMAN_ACTION",
            "label": f"Generate governed P18.9.2 {_P18_9_2_TITLE}.",
            "target_ticket_id": "P18.9.2",
            "target_ticket_title": _P18_9_2_TITLE,
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


def _node_import_meta_resolve(
    node: str,
    cwd: Path,
    specifier: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            node,
            "--input-type=module",
            "-e",
            "try { console.log(await import.meta.resolve(process.argv[1])); } "
            "catch (err) { console.error(err.code + ': ' + err.message); process.exit(1); }",
            specifier,
        ],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def _make_directory_reparse_point_or_skip(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target, target_is_directory=True)
        return
    except (OSError, NotImplementedError) as exc:
        symlink_error = exc
    if sys.platform == "win32":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return
        pytest.skip(f"directory junction creation unavailable: {result.stderr}")
    pytest.skip(f"directory symlink creation unavailable: {symlink_error}")


def _make_file_symlink_or_skip(link: Path, target: Path | str) -> None:
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"file symlink creation unavailable: {exc}")


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


def _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch):
    _install_implementation_profile(monkeypatch, projection_home)
    bridge.generate_current_ticket(workflow=_p18_9_2_workflow())
    generation = bridge.load_generation_record(ticket_id="P18.9.2")
    assert generation is not None

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (_p18_9_2_workflow(), None),
    )
    approved = pr.apply_approval_decision(
        "P18.9.2",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )
    assert approved["status"] == "approved"
    projected = pr.project_current_approved_workpacket_to_kanban(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="P18_9_2_APPROVED_NO_EXECUTION",
    )
    projection_record = _projection_authority_record(projected)
    queued = pr.build_workflow_control_snapshot()
    assert queued["current_ticket_id"] == "P18.9.2"
    assert queued["workflow_status"] == "queued"
    assert queued["workflow_state"] == "P18.9.2-QUEUED-NOT-EXECUTING"
    assert queued["next_action"]["id"] == (
        "START_P18_9_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    )

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
    monkeypatch.setattr(
        pr,
        "_projection_requires_scratch_source_materialization",
        lambda _projection_record: True,
    )

    def dependency_gap(_projection, _workspace, *, env_overlay=None, source_root=None):
        _ = env_overlay, source_root
        raise pr.ProductRuntimeDependencyGap(
            pr.DEPENDENCY_MATERIALIZATION_FAILED,
            "dependency source contains an unsafe symlinked file",
        )

    monkeypatch.setattr(pr, "_materialize_pepper_governed_scratch_source", dependency_gap)
    immediate = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.2 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="START_P18_9_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("dependency gap must block before spawn"),
    )
    assert immediate["start_status"] == "blocked"
    assert immediate["blocker_code"] == pr.IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP
    assert immediate["dispatch_performed"] is True
    assert immediate["execution_started"] is False
    assert immediate["worker_execution"] is False
    assert immediate["worker_process_started"] is False
    assert immediate["Git_mutation"] is False

    failed = pr.build_workflow_control_snapshot()
    assert failed["current_ticket_id"] == "P18.9.2"
    assert failed["workflow_status"] == "execution_failed"
    assert failed["workflow_state"] == "P18.9.2-EXECUTION-FAILED-RECOVERY-REQUIRED"
    assert failed["recovery_state"] == "recovery_required"
    assert failed["blocker_count"] == 1
    assert failed["active_execution_count"] == 0
    assert failed["next_action"]["id"] == "RECOVER_P18_9_2_EXECUTION"

    missing_recovery_retry = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo retry de P18.9.2.",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("retry must require recovery first"),
    )
    assert missing_recovery_retry["retry_start_status"] == "blocked"
    assert missing_recovery_retry["blocker_code"] == "RECOVERY_AUTHORITY_GAP"
    assert missing_recovery_retry["retry_start_authorization_recorded"] is False
    assert not pr.retry_start_record_path_for_ticket("P18.9.2").exists()

    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text("P18.9.2"),
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="RECOVER_P18_9_2_EXECUTION",
    )
    assert recovery["recovery_status"] == "retry_pending"
    assert recovery["governed_workflow_transition"] == "FAILED->RETRY_PENDING"
    assert recovery["future_retry_requires_separate_start_authorization"] is True
    assert recovery["retry_execution_started"] is False
    assert recovery["retry_execution_count"] == 0
    assert recovery["dispatch_performed"] is False
    assert recovery["worker_execution"] is False
    assert recovery["Kanban_dispatch"] is False
    assert recovery["auto_retry"] is False
    assert recovery["Git_mutation"] is False

    retry_pending = pr.build_workflow_control_snapshot()
    assert retry_pending["current_ticket_id"] == "P18.9.2"
    assert retry_pending["workflow_status"] == "retry_pending"
    assert retry_pending["workflow_state"] == "P18.9.2-RETRY-PENDING-NOT-DISPATCHED"
    assert retry_pending["queue_state"] == "kanban_retry_prepared_not_dispatched"
    assert retry_pending["recovery_state"] == "retry_pending"
    assert retry_pending["active_execution_count"] == 0
    assert retry_pending["worker_execution"] is False
    assert retry_pending["Kanban_dispatch"] is False
    assert retry_pending["blocker_count"] == 0
    assert retry_pending["remaining_blockers"] == []
    assert retry_pending["worker_lifecycle"]["historical_lifecycle_blocker_consumed"] is True
    assert retry_pending["next_action"]["id"] == (
        "START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    )
    retry_pending_replay = pr.build_workflow_control_snapshot()
    assert {
        key: retry_pending[key]
        for key in (
            "current_ticket_id",
            "workflow_status",
            "workflow_state",
            "queue_state",
            "recovery_state",
            "active_execution_count",
            "blocker_count",
            "remaining_blockers",
            "next_action",
            "failure_category",
            "failure_summary",
        )
    } == {
        key: retry_pending_replay[key]
        for key in (
            "current_ticket_id",
            "workflow_status",
            "workflow_state",
            "queue_state",
            "recovery_state",
            "active_execution_count",
            "blocker_count",
            "remaining_blockers",
            "next_action",
            "failure_category",
            "failure_summary",
        )
    }

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.worker_pid is None
        assert task.current_run_id is None
        assert task.last_failure_error
        assert pr.DEPENDENCY_MATERIALIZATION_FAILED in task.last_failure_error
        assert len(runs) == 1
        assert runs[0].status == "gave_up"
        assert runs[0].outcome == "gave_up"
        assert pr.DEPENDENCY_MATERIALIZATION_FAILED in (runs[0].error or "")
        run_id = runs[0].id
    finally:
        conn.close()

    return SimpleNamespace(
        pr=pr,
        kanban_db=kanban_db,
        projected=projected,
        projection_record=projection_record,
        immediate=immediate,
        failed=failed,
        recovery=recovery,
        retry_pending=retry_pending,
        failed_run_id=run_id,
    )


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
            "policy_id": pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_POLICY_ID,
            "source_materialized": True,
            "ticket_id": _projection["ticket_id"],
            "work_packet_id": _projection["work_packet_id"],
            "work_packet_SHA256": _projection["work_packet_SHA256"],
            "ticket_spec_SHA256": _projection["ticket_spec_SHA256"],
            "projection_SHA256": _projection["projection_SHA256"],
            "workspace_root": str(workspace_path),
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


def _write_p18_9_1_terminal_candidate_fixture(
    pr,
    projection_home: Path,
    workspace: Path,
) -> None:
    source_root = projection_home / "terminal-candidate-source"
    nav_relative_path = "2_products/pepper-agent/web/src/agent-platform/shell/navigation.ts"
    modified_files = {
        nav_relative_path: (
            "export const nav = 'canonical';\n",
            "export const nav = 'canonical';\nexport const p18_9_1_terminal = true;\n",
        ),
        "2_products/pepper-agent/web/src/agent-platform/shell/routing.ts": (
            "export const route = 'canonical';\n",
            "export const route = 'compact-navigation';\n",
        ),
        "2_products/pepper-agent/web/src/agent-platform/shell/compact-nav.ts": (
            "export const compact = false;\n",
            "export const compact = true;\n",
        ),
    }
    for relative_path, (source_text, workspace_text) in modified_files.items():
        _write_fixture_file(source_root, relative_path, source_text)
        _write_fixture_file(workspace, relative_path, workspace_text)
    _write_fixture_file(
        workspace,
        "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt",
        "Synthetic terminal candidate report.\n",
    )
    manifest_path = workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {
            "source_materialized": True,
            "dependency_substrate_materialized": True,
            "dependency_substrate_kind": "synthetic_test_fixture",
            "dependency_install_performed": False,
            "canonical_package_lock_materialized": False,
            "manifest_path": str(manifest_path),
            "product_diff_excluded_roots": ["2_products/pepper-agent/node_modules"],
        }
    manifest.update(
        {
            "source_root": str(source_root),
            "workspace_root": str(workspace),
            "writable_allowed_paths": [
                "2_products/pepper-agent/web/src/agent-platform/shell/**",
            ],
        }
    )
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_p18_9_2_terminal_candidate_fixture(
    pr,
    projection_home: Path,
    workspace: Path,
) -> dict:
    source_root = projection_home / "p18-9-2-terminal-candidate-source"
    modified_files = {
        "2_products/pepper-agent/web/src/agent-platform/runtime-overview/contract.ts": (
            "export interface RuntimeOverview { status: string }\n",
            "export interface RuntimeOverview {\n"
            "  currentWork: string\n"
            "  nextGovernedAction: string\n"
            "  needsAttention: string[]\n"
            "  execution: string\n"
            "  governedState: string\n"
            "}\n",
        ),
        "2_products/pepper-agent/web/src/agent-platform/runtime-overview/runtime-overview-page.tsx": (
            "export function RuntimeOverviewPage() { return null }\n",
            "export function RuntimeOverviewPage() {\n"
            "  return (\n"
            "    <section aria-label=\"Control Center Overview\">\n"
            "      <h2>Current Work</h2>\n"
            "      <h2>Next Governed Action</h2>\n"
            "      <h2>Needs Attention</h2>\n"
            "      <h2>Execution</h2>\n"
            "      <h2>Governed State</h2>\n"
            "    </section>\n"
            "  )\n"
            "}\n",
        ),
        "2_products/pepper-agent/web/src/agent-platform/runtime-overview/runtime-overview.test.tsx": (
            "import { expect, test } from 'vitest'\n",
            "import { expect, test } from 'vitest'\n"
            "test('renders Current Work', () => expect('Current Work').toContain('Current'))\n"
            "test('renders Next Governed Action', () => expect('Next Governed Action').toContain('Governed'))\n"
            "test('renders Needs Attention', () => expect('Needs Attention').toContain('Attention'))\n"
            "test('renders Execution', () => expect('Execution').toContain('Execution'))\n"
            "test('renders Governed State', () => expect('Governed State').toContain('State'))\n",
        ),
    }
    for relative_path, (source_text, workspace_text) in modified_files.items():
        _write_fixture_file(source_root, relative_path, source_text)
        _write_fixture_file(workspace, relative_path, workspace_text)
    manifest_path = workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({
        "source_root": str(source_root),
        "workspace_root": str(workspace),
        "writable_allowed_paths": [
            "2_products/pepper-agent/web/src/agent-platform/runtime-overview/**",
        ],
    })
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "source_root": source_root,
        "workspace_root": workspace,
        "modified_files": modified_files,
        "manifest_path": manifest_path,
    }


def _finish_projected_run_as_review_required_terminal(
    kanban_db,
    projected: dict,
    run_id: int,
    *,
    summary: str,
    block_kind: str | None = "needs_input",
    task_status: str = "blocked",
    error: str | None = None,
    metadata: dict | None = None,
) -> None:
    now = int(time.time())
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        conn.execute(
            "UPDATE tasks SET status = ?, current_run_id = NULL, "
            "worker_pid = NULL, claim_lock = NULL, claim_expires = NULL, "
            "last_failure_error = NULL, block_kind = ?, block_recurrences = 1 "
            "WHERE id = ? AND current_run_id = ?",
            (task_status, block_kind, projected["kanban_task_id"], run_id),
        )
        conn.execute(
            "UPDATE task_runs SET status = 'blocked', outcome = 'blocked', summary = ?, "
            "error = ?, metadata = ?, ended_at = ?, claim_lock = NULL, claim_expires = NULL, "
            "worker_pid = NULL WHERE id = ?",
            (
                summary,
                error,
                json.dumps(metadata, ensure_ascii=False) if metadata else None,
                now,
                run_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def _start_recovered_p18_9_2_retry_for_test(
    state,
    monkeypatch,
    *,
    pid: int = 6792,
) -> dict:
    _patch_synthetic_scratch_materialization(monkeypatch, state.pr)
    monkeypatch.setattr(state.kanban_db, "_pid_alive", lambda live_pid: int(live_pid) == pid)
    retry = state.pr.start_current_ticket_execution(
        human_authorization_text="Autorizo retry de P18.9.2.",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: pid,
    )
    assert retry["retry_start_status"] == "started"
    assert retry["kanban_run_id"] == state.failed_run_id + 1
    return retry


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


def _first_projection_allowed_directory(projected: dict) -> str:
    generation = bridge.load_generation_record(ticket_id=projected["ticket_id"])
    assert generation is not None
    work_packet = generation["work_packet_compilation_result"]["work_packet"]
    allowed_paths = work_packet["repository_scope"]["allowed_paths"]
    for pattern in allowed_paths:
        text = str(pattern)
        if text.endswith("/**"):
            return text[:-3].rstrip("/")
    return str(allowed_paths[0]).rstrip("/")


def _activate_p18_9_1_governed_autonomy_for_test(
    pr,
    monkeypatch,
) -> dict:
    activation = pr.activate_current_ticket_governed_autonomy(
        human_request_text=(
            "Activate 01AH governed autonomy status for P18.9.1 without live lineage activation."
        ),
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )
    monkeypatch.setattr(
        pr,
        "_executor_provider_readiness",
        lambda profile_name: _ready_executor_provider_payload(profile_name),
    )
    return {"activation": activation}


_P18_9_1_REVIEW_CHANGES_FEEDBACK = "\n".join([
    "ISSUE 1: Primary Pepper groups must be exactly control, work, agents, automation, resources, system. No seventh top-level Extensions group. Extension/plugin functionality must remain reachable via existing architecture.",
    "ISSUE 2: Contextual detail routes must be reachable and absent from primary navigation item output. Tests must prove the actual distinction behaviorally.",
    "ISSUE 3: Do not expand source-text inspection testing.",
    "PRESERVE: Lead Agent label; compact IA direction; inherited Hermes surfaces mapped into Pepper; existing router; existing plugin loader; existing extension registry; protected /agent-platform ownership; route compatibility.",
    "EXCLUDE: P18.9.1-implementation-report.txt must not become canonical product content.",
])

_P18_9_1_HANDOFF_BRANCH = "p18-manual-to-hermes-workflow-migration"
_P18_9_1_HANDOFF_COMMITS = (
    "dc77d92",
    "467f3b412ddd51a237fc76ff5f297e0347308755",
)
_P18_9_1_LIVE_HANDOFF_RUN_ID = 11
_P18_9_1_LIVE_CANDIDATE_SHA256 = (
    "25538ecce152199221b25fde58631e63d7f3729fe1efe4bcb96ed107141ca86b"
)
_P18_9_1_LIVE_REVIEW_DECISION_SHA256 = (
    "f2b9a510bbcf1d1fe8d8f4d3c5ce04b6484e6d2868e9276d736bb1ec1ab7a38d"
)
_P18_9_1_LIVE_HANDOFF_COMMITS = (
    "dc77d92e3c01d45a5d13db0161f79c5297ea33b7",
    "467f3b412ddd51a237fc76ff5f297e0347308755",
)
_P18_9_1_POST_HANDOFF_CAPABILITY_HEAD = "8e383a878007894fb72c77e317a9a92b7ceeb4fa"
_P18_9_1_HANDOFF_APPROVED_PATHS = (
    "2_products/pepper-agent/web/src/agent-platform/shell/navigation.ts",
    "2_products/pepper-agent/web/src/agent-platform/shell/shell.test.tsx",
)
_P18_9_1_HANDOFF_EXCLUDED_PATHS = (
    "2_products/pepper-agent/package-lock.json",
    "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt",
)
_P18_9_2_HANDOFF_BRANCH = "p18-9-2-control-center-overview"
_P18_9_2_HANDOFF_PARENT = "1234567890abcdef1234567890abcdef12345678"
_P18_9_2_HANDOFF_COMMIT = "abcdef1234567890abcdef1234567890abcdef12"
_P18_9_2_HANDOFF_CANDIDATE_PATHS = (
    "2_products/pepper-agent/web/src/agent-platform/runtime-overview/contract.ts",
    "2_products/pepper-agent/web/src/agent-platform/runtime-overview/runtime-overview-page.tsx",
    "2_products/pepper-agent/web/src/agent-platform/runtime-overview/runtime-overview.test.tsx",
)


def _p18_9_1_handoff_git_snapshot(
    *,
    branch: str = _P18_9_1_HANDOFF_BRANCH,
    head: str = _P18_9_1_HANDOFF_COMMITS[-1],
) -> dict[str, object]:
    return {
        "available": True,
        "read_only": True,
        "shell": False,
        "branch": branch,
        "head": head,
        "status_branch": f"## {branch}...origin/{branch}",
        "status_counts": {"modified": 1},
        "status_entries": [" M 2_products/pepper-agent/package-lock.json"],
        "skipped_status_entries": {},
    }


def _p18_9_2_handoff_git_snapshot(
    *,
    branch: str = _P18_9_2_HANDOFF_BRANCH,
    head: str = _P18_9_2_HANDOFF_PARENT,
    remote_head: str | None = _P18_9_2_HANDOFF_PARENT,
    path_SHA256: dict[str, str] | None = None,
    status_entries: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    entries = status_entries
    if entries is None:
        entries = [
            {
                "status": "??",
                "path": "2_products/pepper-agent/.runtime-logs/session.log",
            },
        ]
    return {
        "available": True,
        "read_only": True,
        "shell": False,
        "branch": branch,
        "head": head,
        "remote_head": remote_head,
        "status_branch": f"## {branch}...origin/{branch}",
        "status_counts": {"??": len(entries)},
        "status_entries": entries,
        "skipped_status_entries": {},
        "path_SHA256": path_SHA256 or {},
    }


def _write_json_authority_record(path: Path, record: dict) -> None:
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _install_current_roadmap_authority_drift_for_test(monkeypatch) -> None:
    original = bridge.resolve_roadmap_ticket_authority

    def drifted(ticket_id: str) -> dict[str, object]:
        authority = dict(original(ticket_id))
        if ticket_id in {"P18.9.1", "P18.9.2"}:
            contract = json.loads(json.dumps(authority.get("ticket_contract") or {}))
            contract["objective"] = f"Evolved current objective for {ticket_id}."
            authority["ticket_contract"] = contract
            authority["roadmap_purpose"] = f"Evolved current purpose for {ticket_id}."
        return authority

    monkeypatch.setattr(bridge, "resolve_roadmap_ticket_authority", drifted)


def _install_legacy_governed_autonomy_activation_shape_for_test(
    pr,
    projection_record: dict,
) -> dict:
    path = pr.governed_autonomy_activation_record_path_for_ticket("P18.9.1")
    record = json.loads(path.read_text(encoding="utf-8"))
    record.update({
        "same_authority_delegation_status": "blocked_metadata_only",
        "same_authority_delegation_authorized": False,
        "same_authority_delegation_blocker_code": "A2A_RUNTIME_UNAVAILABLE_WITHOUT_TASK_LOCAL_AUTHORITY",
        "same_authority_delegation_blocker_detail": (
            "No canonical OpenCode/A2A dispatcher is available; task-local delegation requires "
            "a separate 01AH-scoped authority that still cannot activate live lineage."
        ),
        "opencode_runtime_dispatcher_found": False,
        "delegate_task_runtime_kind": "local_subagent_not_opencode_a2a",
        "live_lineage_activation_authorized": False,
        "live_lineage_activation_status": "blocked_requires_separate_authority",
        "live_lineage_activation_blocker_code": "LIVE_LINEAGE_ACTIVATION_AUTHORITY_GAP",
        "live_lineage_activation_blocker_detail": (
            f"{projection_record['ticket_id']} live lineage activation, retry execution, and run creation "
            "require separate human/runtime authority."
        ),
        "human_smoke_marker": pr.PEPPER_LEGACY_GOVERNED_AUTONOMY_READY_MARKER,
    })
    record["activation_action_SHA256"] = pr._governed_autonomy_activation_record_digest(
        record
    )
    _write_json_authority_record(path, record)
    runtime_path = pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.1")
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    runtime["activation_action_SHA256"] = record["activation_action_SHA256"]
    runtime["runtime_state_SHA256"] = pr._governed_autonomy_runtime_record_digest(runtime)
    _write_json_authority_record(runtime_path, runtime)
    return record


def _accepted_p18_9_1_review_for_handoff(
    projection_home,
    monkeypatch,
    *,
    pids: tuple[int, int, int] = (6955, 6956, 6957),
) -> tuple[object, dict, dict, dict, dict]:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )
    fixture = _start_p18_9_1_validated_review_ready_run_7(
        pr,
        projection_home,
        projected,
        monkeypatch,
        pids=pids,
    )
    accepted = pr.submit_current_ticket_review_decision(
        decision="accept",
        feedback="Human accepts the validated P18.9.1 candidate for human Git handoff.",
        reviewed_run_id=fixture["run_7"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert accepted["review_decision"] == "accept"
    assert accepted["workflow_status"] == "review_accepted_pending_human_git_handoff"
    return pr, projected, authority, fixture, accepted


def _p18_9_1_handoff_completion_kwargs(
    accepted: dict,
    *,
    commits: tuple[str, ...] = _P18_9_1_HANDOFF_COMMITS,
    approved_paths: tuple[str, ...] = _P18_9_1_HANDOFF_APPROVED_PATHS,
    excluded_paths: tuple[str, ...] = _P18_9_1_HANDOFF_EXCLUDED_PATHS,
    branch: str = _P18_9_1_HANDOFF_BRANCH,
    git_snapshot: dict[str, object] | None = None,
    **overrides,
) -> dict[str, object]:
    final_snapshot = git_snapshot or _p18_9_1_handoff_git_snapshot(
        branch=branch,
        head=commits[-1],
    )
    data: dict[str, object] = {
        "reviewed_run_id": int(accepted["reviewed_run_id"]),
        "reviewed_candidate_SHA256": accepted["reviewed_candidate_SHA256"],
        "review_decision_SHA256": accepted["review_decision_SHA256"],
        "commits": commits,
        "branch": branch,
        "push_attestation": "Human pushed the handoff branch to origin.",
        "approved_committed_paths": approved_paths,
        "excluded_paths": excluded_paths,
        "validation_evidence": (
            "Human validation completed for the accepted P18.9.1 candidate after Git handoff.",
        ),
        "human_attested_evidence": (
            "Human attests the second handoff commit contains exactly the approved shell paths.",
        ),
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
        "next_action_id": "PREPARE_P18_9_1_HUMAN_GIT_HANDOFF",
        "git_snapshot_fn": lambda: final_snapshot,
    }
    data.update(overrides)
    return data


def _evidence_item(result: dict, evidence_id: str) -> dict:
    matches = [
        item
        for item in result["verification_evidence"]
        if item.get("id") == evidence_id
    ]
    assert len(matches) == 1
    return matches[0]


def _start_p18_9_1_validated_review_ready_run_7(
    pr,
    projection_home: Path,
    projected: dict,
    monkeypatch,
    *,
    pids: tuple[int, int, int] = (6915, 6916, 6917),
) -> dict:
    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    live_pids = set(pids)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) in live_pids)
    run_5_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 before synthetic validated review fixture run 7.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: pids[0],
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = run_5_started["kanban_run_id"]
    assert run_5 == run_4 + 1
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary="synthetic run 5 terminal before review-ready run 7",
    )
    run_6_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Start synthetic fresh P18.9.1 governed run 6 before review fixture.",
        strategy="DIRECT",
        fresh_execution_request_text="Launch synthetic fresh governed P18.9.1 run 6 before review fixture.",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: pids[1],
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_6 = run_6_started["kanban_run_id"]
    assert run_6 == run_5 + 1
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_6,
        status="blocked",
        outcome="blocked",
        summary="synthetic run 6 terminal before review-ready run 7",
    )
    run_7_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Start synthetic fresh P18.9.1 governed run 7 for review fixture.",
        strategy="DIRECT",
        fresh_execution_request_text="Launch synthetic fresh governed P18.9.1 run 7 for review fixture.",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: pids[2],
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_7 = run_7_started["kanban_run_id"]
    assert run_7 == run_6 + 1
    run_7_workspace = Path(run_7_started["workspace_path"])
    _write_p18_9_1_terminal_candidate_fixture(pr, projection_home, run_7_workspace)
    run_7_summary = (
        "worker process started; candidate produced; workpacket_validation invoked; "
        "validation infrastructure failure = false; product validation failure = false; "
        "governed V2 validation passed; 7 files, 123 tests passed; "
        "Git mutation authority = false; terminal reason: review-required because "
        "canonical repository merge is human-only."
    )
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_7,
        status="blocked",
        outcome="blocked",
        summary=run_7_summary,
    )
    runtime_state = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=_projection_authority_record(projected),
    )
    assert runtime_state is not None
    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["validated_candidate_review_required"] is True
    assert status["terminal_run_id"] == run_7
    return {
        "run_4": run_4,
        "run_5": run_5,
        "run_6": run_6,
        "run_7": run_7,
        "run_7_workspace": run_7_workspace,
        "run_7_runtime_state": runtime_state,
        "status": status,
    }


def _write_governed_autonomy_activation_record_for_test(pr, record: dict) -> None:
    path = pr.governed_autonomy_activation_record_path_for_ticket(str(record["ticket_id"]))
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _legacy_runtime_limited_governed_autonomy_activation_record(pr, record: dict) -> dict:
    legacy = json.loads(json.dumps(record))
    ticket_id = legacy["ticket_id"]
    legacy.update({
        "same_authority_delegation_status": "blocked_metadata_only",
        "same_authority_delegation_authorized": False,
        "same_authority_delegation_blocker_code": "A2A_RUNTIME_UNAVAILABLE_WITHOUT_TASK_LOCAL_AUTHORITY",
        "same_authority_delegation_blocker_detail": (
            "No canonical OpenCode/A2A dispatcher is available; task-local delegation requires "
            "a separate 01AH-scoped authority that still cannot activate live lineage."
        ),
        "opencode_runtime_dispatcher_found": False,
        "delegate_task_runtime_kind": "local_subagent_not_opencode_a2a",
        "live_lineage_activation_authorized": False,
        "live_lineage_activation_status": "blocked_requires_separate_authority",
        "live_lineage_activation_blocker_code": "LIVE_LINEAGE_ACTIVATION_AUTHORITY_GAP",
        "live_lineage_activation_blocker_detail": (
            f"{ticket_id} live lineage activation, retry execution, and run creation "
            "require separate human/runtime authority."
        ),
        "human_smoke_marker": pr.PEPPER_LEGACY_GOVERNED_AUTONOMY_READY_MARKER,
    })
    legacy.pop("activation_action_SHA256", None)
    legacy["activation_action_SHA256"] = pr._governed_autonomy_activation_record_digest(legacy)
    return legacy


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


def test_dependency_substrate_materializes_internal_symlinked_files_as_physical_copies(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    web_package_rel = "2_products/pepper-agent/web"
    root_modules_rel = "2_products/pepper-agent/node_modules"
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/src/agent-platform/shell/scratch-validation.test.ts",
        "test('safe internal dependency symlink', () => {})\n",
    )
    target = _write_fixture_file(
        source_root,
        f"{root_modules_rel}/vitest/dist/vitest.mjs",
        "export const materialized = 'physical dependency copy';\n",
    )
    symlinked_entry = source_root / f"{root_modules_rel}/vitest/vitest.mjs"
    _make_file_symlink_or_skip(symlinked_entry, Path("dist/vitest.mjs"))
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            f"{web_package_rel}/src/agent-platform/shell/scratch-validation.test.ts",
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

    scratch_vitest = workspace / f"{root_modules_rel}/vitest/vitest.mjs"
    assert symlinked_entry.is_symlink()
    assert scratch_vitest.is_file()
    assert not scratch_vitest.is_symlink()
    assert scratch_vitest.read_text(encoding="utf-8") == target.read_text(encoding="utf-8")
    substrate = record["dependency_substrates"][0]
    assert substrate["dependency_sentinel_SHA256"]["vitest/vitest.mjs"] == (
        substrate["scratch_dependency_sentinel_SHA256"]["vitest/vitest.mjs"]
    )


def test_dependency_substrate_rejects_symlinked_files_that_escape_dependency_root(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    web_package_rel = "2_products/pepper-agent/web"
    root_modules_rel = "2_products/pepper-agent/node_modules"
    package_test = _write_fixture_file(
        source_root,
        f"{web_package_rel}/src/agent-platform/shell/scratch-validation.test.ts",
        "test('escaping dependency symlink', () => {})\n",
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    symlinked_entry = source_root / f"{root_modules_rel}/vitest/vitest.mjs"
    symlinked_entry.parent.mkdir(parents=True, exist_ok=True)
    _make_file_symlink_or_skip(symlinked_entry, package_test)
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            f"{web_package_rel}/src/agent-platform/shell/scratch-validation.test.ts",
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
    assert exc_info.value.dependency_code == pr.DEPENDENCY_MATERIALIZATION_FAILED
    assert "unsafe symlinked file" in str(exc_info.value)
    assert not (workspace / f"{root_modules_rel}/vitest/vitest.mjs").exists()


@pytest.mark.parametrize(
    ("case", "expected_message"),
    (
        ("broken", "unsafe symlinked file"),
        ("cyclic", "unsafe symlinked file"),
        ("non_regular_fifo", "symlinked file target is not a file"),
    ),
)
def test_dependency_substrate_rejects_invalid_symlinked_files(
    tmp_path,
    case: str,
    expected_message: str,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    source_root = tmp_path / "source"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    web_package_rel = "2_products/pepper-agent/web"
    root_modules_rel = "2_products/pepper-agent/node_modules"
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/package.json",
        json.dumps({"scripts": {"test": "vitest run"}}),
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/src/agent-platform/shell/scratch-validation.test.ts",
        "test('invalid dependency symlink', () => {})\n",
    )
    _write_fixture_file(
        source_root,
        f"{root_modules_rel}/vitest/vitest.mjs",
        "export const vitest = true;\n",
    )
    symlinked_entry = source_root / f"{root_modules_rel}/.bin/bad-link"
    symlinked_entry.parent.mkdir(parents=True, exist_ok=True)
    if case == "broken":
        _make_file_symlink_or_skip(symlinked_entry, Path("missing-target.js"))
    elif case == "cyclic":
        _make_file_symlink_or_skip(symlinked_entry, Path("bad-link"))
    else:
        if not hasattr(os, "mkfifo"):
            pytest.skip("host does not support FIFO creation")
        fifo_target = source_root / f"{root_modules_rel}/.cache/fifo-target"
        fifo_target.parent.mkdir(parents=True, exist_ok=True)
        os.mkfifo(fifo_target)
        _make_file_symlink_or_skip(symlinked_entry, Path("../.cache/fifo-target"))
    authority = _source_materialization_authority(
        workspace,
        allowed_paths=(
            f"{web_package_rel}/src/agent-platform/shell/scratch-validation.test.ts",
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

    assert symlinked_entry.is_symlink()
    assert exc_info.value.external_code == pr.IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP
    assert exc_info.value.dependency_code == pr.DEPENDENCY_MATERIALIZATION_FAILED
    assert expected_message in str(exc_info.value)
    assert not (workspace / f"{root_modules_rel}/.bin/bad-link").exists()


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
    _make_directory_reparse_point_or_skip(linked_package, workspace_package)
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


def test_dependency_substrate_recreates_package_local_and_workspace_dependency_topology(
    tmp_path,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    node = shutil.which("node")
    if node is None:
        pytest.skip("node executable unavailable for import.meta.resolve proof")

    source_root = tmp_path / "source"
    workspace_before = tmp_path / "workspace-before"
    workspace_after = tmp_path / "workspace-after"
    workspace_before.mkdir()
    workspace_after.mkdir()
    web_package_rel = "2_products/pepper-agent/web"
    root_modules_rel = "2_products/pepper-agent/node_modules"

    _write_fixture_file(
        source_root,
        f"{web_package_rel}/package.json",
        json.dumps({
            "name": "web",
            "type": "module",
            "scripts": {"test": "vitest run"},
            "dependencies": {
                "@hermes/shared": "file:../apps/shared",
                "@nous-research/ui": "0.18.2",
            },
        }),
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/src/agent-platform/shell/shell.test.tsx",
        "test('fixture', () => {})\n",
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/apps/shared/package.json",
        json.dumps({
            "name": "@hermes/shared",
            "type": "module",
            "exports": {".": "./src/index.js"},
        }),
    )
    _write_fixture_file(
        source_root,
        "2_products/pepper-agent/apps/shared/src/index.js",
        "export const shared = true;\n",
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/node_modules/@nous-research/ui/package.json",
        json.dumps({
            "name": "@nous-research/ui",
            "type": "module",
            "exports": {
                ".": "./dist/index.js",
                "./ui/*": "./dist/ui/*.js",
            },
        }),
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/node_modules/@nous-research/ui/dist/index.js",
        "export const ui = true;\n",
    )
    _write_fixture_file(
        source_root,
        f"{web_package_rel}/node_modules/@nous-research/ui/dist/ui/components/badge.js",
        "export const Badge = 'badge';\n",
    )
    for sentinel in (
        "vitest/vitest.mjs",
        "vite/package.json",
        "react/package.json",
        "react-dom/package.json",
        "@vitejs/plugin-react/package.json",
    ):
        _write_fixture_file(source_root, f"{root_modules_rel}/{sentinel}", "{}\n")

    shared_package = source_root / "2_products/pepper-agent/apps/shared"
    linked_package = source_root / f"{root_modules_rel}/@hermes/shared"
    linked_package.parent.mkdir(parents=True, exist_ok=True)
    _make_directory_reparse_point_or_skip(linked_package, shared_package)

    canonical_web = source_root / web_package_rel
    assert _node_import_meta_resolve(node, canonical_web, "@hermes/shared").returncode == 0
    assert (
        _node_import_meta_resolve(
            node,
            canonical_web,
            "@nous-research/ui/ui/components/badge",
        ).returncode
        == 0
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
    allowed_paths = (
        f"{web_package_rel}/src/agent-platform/shell/shell.test.tsx",
    )

    before_authority = _source_materialization_authority(
        workspace_before,
        allowed_paths=allowed_paths,
    )
    pr._materialize_workpacket_scratch_source_tree(before_authority, source_root=source_root)
    pr._copy_dependency_substrate_root(
        source_root / root_modules_rel,
        workspace_before / root_modules_rel,
        source_root=source_root,
        workspace_root=workspace_before,
        package_rel=web_package_rel,
        authority=before_authority,
        required_package_names=frozenset(),
    )
    before_web = workspace_before / web_package_rel
    assert _node_import_meta_resolve(node, before_web, "@hermes/shared").returncode != 0
    assert (
        _node_import_meta_resolve(
            node,
            before_web,
            "@nous-research/ui/ui/components/badge",
        ).returncode
        != 0
    )

    after_authority = _source_materialization_authority(
        workspace_after,
        allowed_paths=allowed_paths,
    )
    pr._materialize_workpacket_scratch_source_tree(after_authority, source_root=source_root)
    record = pr._materialize_workpacket_dependency_substrate(
        after_authority,
        work_packet,
        source_root=source_root,
    )

    after_web = workspace_after / web_package_rel
    shared_result = _node_import_meta_resolve(node, after_web, "@hermes/shared")
    ui_result = _node_import_meta_resolve(
        node,
        after_web,
        "@nous-research/ui/ui/components/badge",
    )
    assert shared_result.returncode == 0, shared_result.stderr
    assert ui_result.returncode == 0, ui_result.stderr
    assert "node_modules/@hermes/shared/src/index.js" in shared_result.stdout.replace("\\", "/")
    assert "web/node_modules/@nous-research/ui" in ui_result.stdout.replace("\\", "/")
    assert (workspace_after / "2_products/pepper-agent/apps/shared/src/index.js").is_file()
    assert (workspace_after / f"{root_modules_rel}/@hermes/shared/src/index.js").is_file()
    assert (
        workspace_after
        / f"{web_package_rel}/node_modules/@nous-research/ui/dist/ui/components/badge.js"
    ).is_file()
    assert not (workspace_after / f"{root_modules_rel}/@hermes/shared").is_symlink()
    assert record["dependency_install_performed"] is False
    assert record["canonical_package_lock_materialized"] is False
    assert record["local_package_sources_materialized"] is True
    assert record["local_package_source_copied_file_count"] >= 2
    assert sorted(record["product_diff_excluded_roots"]) == [
        "2_products/pepper-agent/node_modules",
        "2_products/pepper-agent/web/node_modules",
    ]
    assert shared_package.joinpath("src/index.js").read_text(encoding="utf-8") == (
        "export const shared = true;\n"
    )


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


def test_chat_tool_prepares_approved_successor_execution_projection(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    bridge.generate_current_ticket(workflow=_p18_9_2_workflow())
    record = bridge.load_generation_record(ticket_id="P18.9.2")
    assert record is not None

    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (_p18_9_2_workflow(), None),
    )
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    decision = json.loads(
        handle_function_call(
            "decide_pending_approval",
            {
                "decision": "approve",
                "human_decision_text": "Approve P18.9.2",
                "approval_id": "P18.9.2",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "APPROVE_P18_9_2",
                "ticket_spec_sha256": record["ticket_spec_SHA256"],
                "work_packet_id": record["work_packet_id"],
                "work_packet_sha256": record["work_packet_SHA256"],
            },
        )
    )
    approved_snapshot = pr.build_workflow_control_snapshot()

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_execution",
            {
                "human_request_text": "Prepare P18.9.2 execution.",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "P18_9_2_APPROVED_NO_EXECUTION",
            },
        )
    )
    queued_snapshot = pr.build_workflow_control_snapshot()
    projection_record = projection.load_kanban_projection_record(ticket_id="P18.9.2")

    assert decision["success"] is True
    assert decision["workflow_status"] == "ticket_approved"
    assert decision["current_ticket_id"] == "P18.9.2"
    assert approved_snapshot["current_ticket_id"] == "P18.9.2"
    assert approved_snapshot["workflow_status"] == "ticket_approved"
    assert approved_snapshot["next_action"]["id"] == "P18_9_2_APPROVED_NO_EXECUTION"
    assert approved_snapshot["successor_ticket_generated_not_activated"] is False

    assert result["success"] is True
    assert result["source_tool"] == "prepare_current_ticket_execution"
    assert result["ticket_id"] == "P18.9.2"
    assert result["ticket_spec_SHA256"] == record["ticket_spec_SHA256"]
    assert result["work_packet_id"] == record["work_packet_id"]
    assert result["work_packet_SHA256"] == record["work_packet_SHA256"]
    assert result["current_ticket_id"] == "P18.9.2"
    assert result["workflow_status"] == "queued"
    assert result["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert result["next_action"]["id"] == "START_P18_9_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert result["assignee_profile"] == _IMPLEMENTATION_PROFILE
    assert result["execution_profile_role"] == "implementation_product"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False

    assert projection_record is not None
    assert queued_snapshot["current_ticket_id"] == "P18.9.2"
    assert queued_snapshot["workflow_status"] == "queued"
    assert queued_snapshot["queue_state"] == "kanban_projection_ready_not_dispatched"
    assert queued_snapshot["next_action"]["id"] == "START_P18_9_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert queued_snapshot["successor_ticket_generated_not_activated"] is False
    assert queued_snapshot["worker_execution"] is False
    assert queued_snapshot["Kanban_dispatch"] is False
    assert queued_snapshot["Git_mutation"] is False


def test_approved_successor_dependency_materialization_failure_survives_fresh_reconstruction(
    projection_home,
    monkeypatch,
) -> None:
    _install_implementation_profile(monkeypatch, projection_home)
    bridge.generate_current_ticket(workflow=_p18_9_2_workflow())
    generation = bridge.load_generation_record(ticket_id="P18.9.2")
    assert generation is not None

    from hermes_cli import kanban_db
    from hermes_cli.agent_platform import product_runtime as pr

    monkeypatch.setattr(
        pr,
        "_p18_9_0_generation_overlay",
        lambda: (_p18_9_2_workflow(), None),
    )
    approved = pr.apply_approval_decision(
        "P18.9.2",
        pr.ApprovalDecisionRequest(decision="approve", actor="human.p18.9"),
    )
    assert approved["status"] == "approved"
    projected = pr.project_current_approved_workpacket_to_kanban(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="P18_9_2_APPROVED_NO_EXECUTION",
    )
    queued_before_start = pr.build_workflow_control_snapshot()
    assert queued_before_start["current_ticket_id"] == "P18.9.2"
    assert queued_before_start["workflow_status"] == "queued"
    assert queued_before_start["workflow_state"] == "P18.9.2-QUEUED-NOT-EXECUTING"
    assert queued_before_start["next_action"]["id"] == (
        "START_P18_9_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    )

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
    monkeypatch.setattr(
        pr,
        "_projection_requires_scratch_source_materialization",
        lambda _projection_record: True,
    )

    def dependency_gap(_projection, _workspace, *, env_overlay=None, source_root=None):
        _ = env_overlay, source_root
        raise pr.ProductRuntimeDependencyGap(
            pr.DEPENDENCY_MATERIALIZATION_FAILED,
            "dependency source contains an unsafe symlinked file",
        )

    monkeypatch.setattr(pr, "_materialize_pepper_governed_scratch_source", dependency_gap)
    immediate = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.2 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="START_P18_9_2_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("dependency gap must block before spawn"),
    )
    assert immediate["start_status"] == "blocked"
    assert immediate["blocker_code"] == pr.IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP
    assert immediate["dispatch_performed"] is True
    assert immediate["execution_started"] is False
    assert immediate["worker_execution"] is False
    assert immediate["worker_process_started"] is False
    assert immediate["worker_pid_recorded"] is False
    assert immediate["Git_mutation"] is False

    fresh = pr.build_workflow_control_snapshot()
    replay = pr.build_workflow_control_snapshot()
    assert fresh["current_ticket_id"] == "P18.9.2"
    assert fresh["workflow_status"] == "execution_failed"
    assert fresh["workflow_state"] == "P18.9.2-EXECUTION-FAILED-RECOVERY-REQUIRED"
    assert fresh["queue_state"] == "kanban_execution_terminal"
    assert fresh["execution_state"] == "no_active_executions"
    assert fresh["active_execution_count"] == 0
    assert fresh["worker_execution"] is False
    assert fresh["Kanban_dispatch"] is True
    assert fresh["recovery_state"] == "recovery_required"
    assert fresh["next_action"]["id"] == "RECOVER_P18_9_2_EXECUTION"
    assert fresh["Git_mutation"] is False
    assert {
        key: fresh[key]
        for key in (
            "current_ticket_id",
            "workflow_status",
            "workflow_state",
            "queue_state",
            "execution_state",
            "active_execution_count",
            "worker_execution",
            "Kanban_dispatch",
            "recovery_state",
            "next_action",
        )
    } == {
        key: replay[key]
        for key in (
            "current_ticket_id",
            "workflow_status",
            "workflow_state",
            "queue_state",
            "execution_state",
            "active_execution_count",
            "worker_execution",
            "Kanban_dispatch",
            "recovery_state",
            "next_action",
        )
    }

    record = pr.load_p18_9_0_execution_start_record()
    assert record is not None
    assert record["ticket_id"] == "P18.9.2"
    assert record["execution_started"] is False
    assert record["worker_execution"] is False
    assert record["worker_process_started"] is False
    assert record["Git_mutation"] is False
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.worker_pid is None
        assert task.current_run_id is None
        assert task.consecutive_failures == 1
        assert task.last_failure_error
        assert pr.DEPENDENCY_MATERIALIZATION_FAILED in task.last_failure_error
    finally:
        conn.close()

    recovery = pr.recover_current_ticket_execution(
        human_authorization_text=pr.governed_ticket_recovery_authorization_text("P18.9.2"),
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="RECOVER_P18_9_2_EXECUTION",
    )
    assert recovery["recovery_status"] == "retry_pending"
    assert recovery["ticket_id"] == "P18.9.2"
    assert recovery["dispatch_performed"] is False
    assert recovery["execution_started"] is False
    assert recovery["worker_execution"] is False
    assert recovery["Kanban_dispatch"] is False
    assert recovery["future_retry_requires_separate_start_authorization"] is True
    assert recovery["auto_retry"] is False
    assert recovery["auto_rollback"] is False
    assert recovery["Git_mutation"] is False

    retry_pending = pr.build_workflow_control_snapshot()
    assert retry_pending["current_ticket_id"] == "P18.9.2"
    assert retry_pending["workflow_status"] == "retry_pending"
    assert retry_pending["workflow_state"] == "P18.9.2-RETRY-PENDING-NOT-DISPATCHED"
    assert retry_pending["active_execution_count"] == 0
    assert retry_pending["worker_execution"] is False
    assert retry_pending["Kanban_dispatch"] is False
    assert retry_pending["recovery_state"] == "retry_pending"
    assert retry_pending["next_action"]["id"] == (
        "START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    )
    assert retry_pending["Git_mutation"] is False


def test_approved_successor_recovered_historical_blocker_allows_retry_start(
    projection_home,
    monkeypatch,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    pr = state.pr
    kanban_db = state.kanban_db
    retry_path = pr.retry_start_record_path_for_ticket("P18.9.2")
    assert not retry_path.exists()

    replay = pr.build_workflow_control_snapshot()
    assert replay["workflow_status"] == "retry_pending"
    assert replay["recovery_state"] == "retry_pending"
    assert replay["next_action"]["id"] == (
        "START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    )
    assert replay["failure_summary"] == state.recovery["failure_summary"]
    assert replay["worker_lifecycle"]["historical_lifecycle_blocker_consumed"] is True

    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6789)
    retry = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo retry de P18.9.2.",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda _task, _workspace, board=None: 6789,
    )

    assert retry["blocker_code"] != "WORKFLOW_BLOCKER_PRESENT"
    assert retry["source_system"] == pr.PEPPER_RETRY_START_ACTION_SOURCE_SYSTEM
    assert retry["retry_start_status"] == "started"
    assert retry["retry_start_authorization_recorded"] is True
    assert retry["recovery_action_SHA256"] == state.recovery["recovery_action_SHA256"]
    assert retry["recovery_cycle_id"] == state.recovery["recovery_cycle_id"]
    assert retry["previous_attempt_count"] == 1
    assert retry["next_attempt_number"] == 2
    assert retry["latest_failed_run_id"] == state.failed_run_id
    assert retry["failure_summary"] == state.recovery["failure_summary"]
    assert retry["dispatch_performed"] is True
    assert retry["execution_started"] is True
    assert retry["worker_execution"] is True
    assert retry["worker_process_started"] is True
    assert retry["retry_execution_started"] is True
    assert retry["retry_execution_count"] == 1
    assert retry["automatic_retry_count"] == 0
    assert retry["new_kanban_task_created"] is False
    assert retry["Git_mutation"] is False
    assert retry["auto_retry"] is False
    assert retry["next_action"]["id"] == "MONITOR_P18_9_2_EXECUTION"

    record = pr.load_current_ticket_retry_start_record(
        projection_record=state.projection_record,
        recovery_record=pr.load_current_ticket_recovery_action_record(
            projection_record=state.projection_record,
        ),
    )
    assert record is not None
    assert record["retry_start_authorization_SHA256"] == retry["retry_start_authorization_SHA256"]
    assert record["latest_failed_run_id"] == state.failed_run_id
    assert retry_path.exists()

    conn = kanban_db.connect(board=state.projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, state.projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, state.projected["kanban_task_id"])
        events = kanban_db.list_events(conn, state.projected["kanban_task_id"])
        assert task is not None
        assert task.status == "running"
        assert task.current_run_id == retry["kanban_run_id"]
        assert task.worker_pid == 6789
        assert len(runs) == 2
        assert [run.id for run in runs] == [state.failed_run_id, retry["kanban_run_id"]]
        assert runs[0].status == "gave_up"
        assert runs[0].outcome == "gave_up"
        assert pr.DEPENDENCY_MATERIALIZATION_FAILED in (runs[0].error or "")
        assert runs[1].status == "running"
        assert runs[1].ended_at is None
        assert any(event.kind == "gave_up" for event in events)
        assert any(event.kind == "retry_prepared" for event in events)
    finally:
        conn.close()

    executing = pr.build_workflow_control_snapshot()
    assert executing["workflow_status"] == "executing"
    assert executing["queue_state"] == "kanban_dispatched"
    assert executing["execution_state"] == "active_executions"
    assert executing["active_execution_count"] == 1
    assert executing["recovery_state"] == "not_required"
    assert executing["retry_state"] == "retry_executing"
    assert executing["retry_start_authority"]["previous_attempt_count"] == 1
    assert executing["retry_start_authority"]["next_attempt_number"] == 2


def test_approved_successor_recovered_retry_rejects_later_failed_run_stale_recovery(
    projection_home,
    monkeypatch,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    pr = state.pr
    kanban_db = state.kanban_db

    conn = kanban_db.connect(board=state.projected["kanban_board_slug"])
    try:
        assert kanban_db.unblock_task(conn, state.projected["kanban_task_id"])
        claimed = kanban_db.claim_task(
            conn,
            state.projected["kanban_task_id"],
            claimer="pepper-worker-retry-start-action",
        )
        assert claimed is not None
        workspace = kanban_db.resolve_workspace(
            claimed,
            board=state.projected["kanban_board_slug"],
        )
        kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
        kanban_db._set_worker_pid(conn, claimed.id, 24680)
        old_expiry = int(time.time()) - 6300
        conn.execute(
            "UPDATE tasks SET claim_expires = ?, last_heartbeat_at = NULL, "
            "skills = ? WHERE id = ?",
            (old_expiry, json.dumps([]), claimed.id),
        )
        conn.execute(
            "UPDATE task_runs SET claim_expires = ?, last_heartbeat_at = NULL WHERE id = ?",
            (old_expiry, claimed.current_run_id),
        )
        conn.commit()
        later_run_id = int(claimed.current_run_id)
    finally:
        conn.close()

    monkeypatch.setenv("HERMES_KANBAN_CRASH_GRACE_SECONDS", "0")
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda _pid: False)
    fresh = pr.build_workflow_control_snapshot()
    assert fresh["workflow_status"] == "execution_failed"
    assert fresh["recovery_state"] == "recovery_required"
    assert fresh["next_action"]["id"] == "RECOVER_P18_9_2_EXECUTION"

    conn = kanban_db.connect(board=state.projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, state.projected["kanban_task_id"])
        assert [run.id for run in runs] == [state.failed_run_id, later_run_id]
    finally:
        conn.close()

    retry = pr.start_current_ticket_execution(
        human_authorization_text="Autorizo retry de P18.9.2.",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("stale recovery must block before spawn"),
    )

    assert retry["retry_start_status"] == "blocked"
    assert retry["blocker_code"] == "KANBAN_RETRY_SOURCE_GAP"
    assert retry["retry_start_authorization_recorded"] is False
    assert "latest failed run no longer matches recovery authority" in retry["blocker_detail"]
    assert retry["worker_process_started"] is False
    assert not pr.retry_start_record_path_for_ticket("P18.9.2").exists()


def test_review_required_p18_9_2_retry_reconstructs_to_governed_review_boundary(
    projection_home,
    monkeypatch,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    pr = state.pr
    kanban_db = state.kanban_db
    retry = _start_recovered_p18_9_2_retry_for_test(state, monkeypatch, pid=6792)
    _write_p18_9_2_terminal_candidate_fixture(
        pr,
        projection_home,
        Path(retry["workspace_path"]),
    )
    summary = (
        "review-required: P18.9.2 Control Center Overview implementation is ready "
        "for human/code review; focused governed frontend validation passed "
        "(GVCMD-001, 36 tests)."
    )
    _finish_projected_run_as_review_required_terminal(
        kanban_db,
        state.projected,
        retry["kanban_run_id"],
        summary=summary,
    )

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["readiness"] == "governed_autonomy_validated_candidate_review_ready"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["workflow_state"] == (
        "P18.9.2-GOVERNED-AUTONOMY-AWAITING-HUMAN-GIT-HANDOFF"
    )
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["recovery_state"] == "not_required"
    assert workflow["blocker_count"] == 0, {
        "blocker_count": workflow["blocker_count"],
        "remaining_blocker_count": len(workflow["remaining_blockers"]),
        "remaining_blockers": workflow["remaining_blockers"],
        "governed_autonomy_blocker_code": workflow.get("governed_autonomy", {}).get(
            "blocker_code"
        ),
        "top_blocker_code": workflow.get("blocker_code"),
    }
    assert workflow["terminal_outcome_class"] == "validated_review_required"
    assert workflow["validated_candidate_review_required"] is True
    assert workflow["candidate_changes_available"] is True
    assert workflow["candidate_changes_reference"]["files_changed"] == 3
    assert workflow["git_handoff_required"] is True
    assert workflow["git_handoff_state"] == "human_git_authority_preserved"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
    assert workflow["next_action"]["required_human_action"] == (
        "review_validation_preparation_and_human_git_handoff"
    )
    assert workflow.get("dispatch_performed", False) is False
    assert workflow["execution_started"] is False
    assert workflow["worker_execution"] is False
    assert workflow["Git_mutation"] is False
    assert workflow["auto_retry"] is False

    review = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert review["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert review["review_preparation_recorded"] is True
    assert review["ticket_id"] == "P18.9.2"
    assert review["successful_run_id"] == retry["kanban_run_id"]
    assert review["successful_run_status"] == "blocked"
    assert review["successful_run_outcome"] == "blocked"
    assert review["acceptance_contract"]["ticket_id"] == "P18.9.2"
    assert review["kanban_completion_result"]["terminal_outcome_class"] == (
        "validated_review_required"
    )
    assert "terminal_review_boundary_evidence" in review["kanban_completion_result"][
        "completion_detail_sources"
    ]
    assert review["git_handoff_required"] is True
    assert review["git_handoff_state"] == "human_git_authority_preserved"
    assert review["dispatch_performed"] is False
    assert review["execution_started"] is False
    assert review["Kanban_dispatch"] is False
    assert review["Git_mutation"] is False
    assert pr.review_prepare_record_path_for_ticket("P18.9.2").exists()

    conn = kanban_db.connect(board=state.projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, state.projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, state.projected["kanban_task_id"])
        terminal_run = next(run for run in runs if run.id == retry["kanban_run_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.block_kind == "needs_input"
        assert task.current_run_id is None
        assert task.worker_pid is None
        assert terminal_run.status == "blocked"
        assert terminal_run.outcome == "blocked"
        assert terminal_run.error is None
    finally:
        conn.close()


def test_lead_agent_tool_prepares_p18_9_2_review_from_current_ticket_authority(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6794,
    )
    pr = state.pr

    before = pr.build_workflow_control_snapshot()
    assert before["current_ticket_id"] == "P18.9.2"
    assert before["workflow_status"] == "execution_completed"
    assert before["review_state"] == "ready_for_review_validation"
    assert before["recovery_state"] == "not_required"
    assert before["blocker_count"] == 0
    assert before["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
        )
    )

    assert result["success"] is True, result
    assert result["source_tool"] == "prepare_current_ticket_review"
    assert result["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert result["ticket_id"] == "P18.9.2"
    assert result["successful_run_id"] == retry["kanban_run_id"]
    assert result["successful_run_status"] == "blocked"
    assert result["successful_run_outcome"] == "blocked"
    assert result["acceptance_contract"]["ticket_id"] == "P18.9.2"
    assert result["acceptance_contract"]["work_packet_id"] == state.projection_record[
        "work_packet_id"
    ]
    assert result["kanban_completion_result"]["run_id"] == retry["kanban_run_id"]
    assert result["kanban_completion_result"]["terminal_outcome_class"] == (
        "validated_review_required"
    )
    assert result["git_handoff_required"] is True
    assert result["git_handoff_state"] == "human_git_authority_preserved"
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False

    direct_replay = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert direct_replay["idempotent_replay"] is True
    assert direct_replay["review_prepare_action_SHA256"] == result[
        "review_prepare_action_SHA256"
    ]


def _p18_9_2_review_ready_for_tool_test(projection_home, monkeypatch, *, pid: int):
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    retry = _start_recovered_p18_9_2_retry_for_test(state, monkeypatch, pid=pid)
    state.candidate_fixture = _write_p18_9_2_terminal_candidate_fixture(
        state.pr,
        projection_home,
        Path(retry["workspace_path"]),
    )
    _finish_projected_run_as_review_required_terminal(
        state.kanban_db,
        state.projected,
        retry["kanban_run_id"],
        summary=(
            "review-required: P18.9.2 Control Center Overview implementation is ready "
            "for human/code review; focused governed frontend validation passed."
        ),
    )
    return state, retry


def _p18_9_2_changes_requested_revision_pending_fixture(
    projection_home,
    monkeypatch,
    *,
    first_pid: int = 6810,
):
    state, run_13 = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=first_pid,
    )
    pr = state.pr
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    prepared_13 = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    changed_13 = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback="Human requests P18.9.2 changes limited to runtime-overview-page.tsx.",
        reviewed_run_id=run_13["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("prepared review bridge must not spawn"),
    )
    revision_request = changed_13["review_revision_request_reference"]
    pending_workflow = pr.build_workflow_control_snapshot()
    assert pending_workflow["workflow_status"] == (
        "review_changes_requested_revision_pending_continuation"
    )
    assert pending_workflow["next_action"]["id"] == "CONTINUE_P18_9_2_GOVERNED_AUTONOMY"

    return SimpleNamespace(
        state=state,
        pr=pr,
        run_13=run_13,
        prepared_13=prepared_13,
        changed_13=changed_13,
        revision_request=revision_request,
    )


def _p18_9_2_active_revision_fixture(
    projection_home,
    monkeypatch,
    *,
    first_pid: int = 6810,
    revision_pid: int = 6811,
):
    fixture = _p18_9_2_changes_requested_revision_pending_fixture(
        projection_home,
        monkeypatch,
        first_pid=first_pid,
    )
    state = fixture.state
    pr = fixture.pr
    revision_request = fixture.revision_request

    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(
        state.kanban_db,
        "_pid_alive",
        lambda pid: int(pid) == revision_pid,
    )
    started_14 = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Start the bounded P18.9.2 review-revision run.",
        strategy="DIRECT",
        resume_pending_fresh_execution_request_SHA256=revision_request[
            "fresh_execution_request_SHA256"
        ],
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: revision_pid,
        project_id="PEPPER",
        ticket_id="P18.9.2",
    )
    assert started_14["kanban_run_id"] == fixture.run_13["kanban_run_id"] + 1
    active_workflow = pr.build_workflow_control_snapshot()
    assert active_workflow["workflow_status"] == "executing"
    assert active_workflow["active_execution_count"] == 1
    assert active_workflow["next_action"]["id"] == "MONITOR_P18_9_2_EXECUTION"

    return SimpleNamespace(
        state=state,
        pr=pr,
        run_13=fixture.run_13,
        prepared_13=fixture.prepared_13,
        changed_13=fixture.changed_13,
        revision_request=revision_request,
        started_14=started_14,
    )


def _p18_9_2_two_round_changes_requested_fixture(
    projection_home,
    monkeypatch,
    *,
    first_pid: int = 6810,
    revision_pid: int = 6811,
    terminal_task_status: str = "blocked",
):
    fixture = _p18_9_2_active_revision_fixture(
        projection_home,
        monkeypatch,
        first_pid=first_pid,
        revision_pid=revision_pid,
    )
    state = fixture.state
    pr = fixture.pr
    started_14 = fixture.started_14

    state.candidate_fixture = _write_p18_9_2_terminal_candidate_fixture(
        pr,
        projection_home,
        Path(started_14["workspace_path"]),
    )
    _finish_projected_run_as_review_required_terminal(
        state.kanban_db,
        state.projected,
        started_14["kanban_run_id"],
        summary=(
            "review-required: P18.9.2 Control Center Overview fresh revision is ready "
            "for human/code review; governed frontend validation passed (GVCMD-001, 41 tests)."
        ),
        task_status=terminal_task_status,
    )
    return SimpleNamespace(
        state=state,
        pr=pr,
        run_13=fixture.run_13,
        prepared_13=fixture.prepared_13,
        changed_13=fixture.changed_13,
        revision_request=fixture.revision_request,
        started_14=started_14,
    )


def _p18_9_2_prepared_review_candidate_fixture(
    projection_home,
    monkeypatch,
    *,
    pid: int = 6820,
):
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=pid,
    )
    review = state.pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    candidate_files = review["kanban_completion_result"]["candidate_changes_reference"][
        "files"
    ]
    return SimpleNamespace(
        state=state,
        pr=state.pr,
        retry=retry,
        review=review,
        candidate_files=candidate_files,
        candidate_paths=[item["path"] for item in candidate_files],
        candidate_fixture=state.candidate_fixture,
    )


def _accepted_p18_9_2_review_for_handoff_prepare(
    projection_home,
    monkeypatch,
    *,
    pid: int = 6840,
):
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=pid,
    )
    accepted = fixture.pr.submit_current_ticket_review_decision(
        decision="accept",
        feedback="Human accepts the validated P18.9.2 candidate for human Git handoff.",
        reviewed_run_id=fixture.retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("accept must not spawn"),
    )
    assert accepted["review_decision"] == "accept"
    assert accepted["workflow_status"] == "review_accepted_pending_human_git_handoff"
    assert accepted["reviewed_run_id"] == fixture.retry["kanban_run_id"]
    assert accepted["review_prepare_action_SHA256"] == fixture.review[
        "review_prepare_action_SHA256"
    ]
    assert accepted["review_package_SHA256"] == fixture.review["review_package_SHA256"]
    assert tuple(sorted(fixture.candidate_paths)) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    accepted_record = fixture.pr.load_current_ticket_review_decision_record(
        projection_record=fixture.pr._load_current_projection_record(),
    )
    assert accepted_record is not None
    return SimpleNamespace(
        **fixture.__dict__,
        accepted=accepted,
        accepted_record=accepted_record,
    )


def _p18_9_2_candidate_hash_maps(candidate_files) -> tuple[dict[str, str], dict[str, str]]:
    source_hashes = {item["path"]: item["source_SHA256"] for item in candidate_files}
    candidate_hashes = {item["path"]: item["workspace_SHA256"] for item in candidate_files}
    return source_hashes, candidate_hashes


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_isolated_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def _create_isolated_source_checkout(
    *,
    source_root: Path,
    checkout_root: Path,
    candidate_paths: tuple[str, ...],
) -> None:
    for relative_path in candidate_paths:
        source_path = source_root / relative_path
        target_path = checkout_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
    _run_isolated_git(checkout_root, "init", "-b", _P18_9_2_HANDOFF_BRANCH)
    _run_isolated_git(checkout_root, "config", "user.name", "Pepper Test Human")
    _run_isolated_git(checkout_root, "config", "user.email", "pepper-test@example.invalid")
    _run_isolated_git(checkout_root, "add", "--", *candidate_paths)
    _run_isolated_git(checkout_root, "commit", "-m", "source baseline")


def _materialize_candidate_files_as_human(
    *,
    scratch_root: Path,
    checkout_root: Path,
    candidate_paths: tuple[str, ...],
) -> None:
    for relative_path in candidate_paths:
        scratch_path = scratch_root / relative_path
        target_path = checkout_root / relative_path
        shutil.copy2(scratch_path, target_path)


def test_p18_9_2_prepare_human_git_handoff_uses_p17_7_without_execution(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6841,
    )
    pr = fixture.pr
    inspection = pr.inspect_current_ticket_review_candidate(
        operation="list",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        reviewed_run_id=fixture.retry["kanban_run_id"],
        review_package_SHA256=fixture.review["review_package_SHA256"],
        review_prepare_action_SHA256=fixture.review["review_prepare_action_SHA256"],
    )
    assert inspection["inspection_status"] == "available"
    assert inspection["inspection_boundary_state"] == "accepted_pending_human_git_handoff"
    assert tuple(inspection["candidate_paths"]) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    source_hashes, candidate_hashes = _p18_9_2_candidate_hash_maps(
        fixture.candidate_files
    )

    prepared = pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=source_hashes,
        ),
    )

    assert prepared["handoff_preparation_recorded"] is True
    assert prepared["idempotent_replay"] is False
    assert prepared["reviewed_run_id"] == fixture.retry["kanban_run_id"]
    assert prepared["reviewed_candidate_SHA256"] == fixture.accepted[
        "reviewed_candidate_SHA256"
    ]
    assert prepared["review_decision_SHA256"] == fixture.accepted["review_decision_SHA256"]
    assert prepared["review_package_SHA256"] == fixture.review["review_package_SHA256"]
    assert prepared["P17_7_handoff_policy_id"] == (
        "pepper-exact-review-bound-non-executing-human-git-handoff-v1"
    )
    assert prepared["P17_7_handoff_state"] == "completed"
    assert prepared["P17_7_handoff_decision"] == "approved"
    assert tuple(prepared["candidate_paths"]) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    assert prepared["candidate_count"] == 3
    assert prepared["added_count"] == 0
    assert prepared["modified_count"] == 3
    assert prepared["deleted_count"] == 0
    assert prepared["branch"] == _P18_9_2_HANDOFF_BRANCH
    assert prepared["remote_name"] == "origin"
    assert prepared["expected_parent_commit"] == _P18_9_2_HANDOFF_PARENT
    assert prepared["commit_message"] == "P18.9.2 Control Center Overview"
    assert prepared["materialization_required"] is True
    assert prepared["materialization_strategy"] == (
        "explicit_cross_checkout_human_powershell_copy_from_trusted_scratch"
    )
    assert prepared["materialization_source_workspace"]["scratch_workspace_root"] == str(
        fixture.candidate_fixture["workspace_root"]
    )
    assert prepared["tolerated_untracked_exclusions"] == [
        "2_products/pepper-agent/.runtime-logs/**"
    ]
    assert prepared["preflight_dirty_status"]["status"] == "ok"
    assert prepared["preflight_dirty_status"]["tolerated_untracked_paths"] == [
        "2_products/pepper-agent/.runtime-logs/session.log"
    ]
    assert prepared["preflight_dirty_status"]["unexpected_dirty_path_count"] == 0
    assert prepared["canonical_source_mutation_by_Pepper"] is False
    assert prepared["human_git_handoff_state"] == "prepared_pending_human_execution"
    assert prepared["workflow_status"] == "review_accepted_pending_human_git_handoff"
    assert prepared["governed_workflow_state"] == "awaiting_human_git_handoff"
    assert prepared["ticket_closed"] is False
    assert prepared["next_ticket_generated"] is False
    assert prepared["dispatch_performed"] is False
    assert prepared["execution_started"] is False
    assert prepared["worker_execution"] is False
    assert prepared["Kanban_dispatch"] is False
    assert prepared["Git_commands_executed"] == 0
    assert prepared["Docker_commands_executed"] == 0
    assert prepared["Graphify_commands_executed"] == 0
    assert prepared["Git_mutation"] is False
    assert prepared["auto_retry"] is False
    assert prepared["auto_rollback"] is False
    assert prepared["next_action"]["id"] == "COMPLETE_P18_9_2_HUMAN_GIT_HANDOFF"

    record = pr.load_current_ticket_human_git_handoff_prepare_record(
        projection_record=pr._load_current_projection_record(),
        review_decision_record=fixture.accepted_record,
    )
    assert record is not None
    assert record["handoff_prepare_record_SHA256"] == prepared[
        "handoff_prepare_record_SHA256"
    ]
    assert record["P17_7_handoff_result_SHA256"] == prepared[
        "P17_7_handoff_result_SHA256"
    ]
    p17_result = record["P17_7_human_git_handoff_result"]
    assert p17_result["Git_commands_executed"] == 0
    assert p17_result["staging_performed"] is False
    assert p17_result["commit_performed"] is False
    assert p17_result["push_performed"] is False
    assert p17_result["automatic_staging_authorized"] is False
    assert p17_result["automatic_commit_authorized"] is False
    assert p17_result["automatic_push_authorized"] is False
    assert record["P17_7_rendered_powershell_SHA256"] == p17_result[
        "rendered_powershell_SHA256"
    ]
    assert record["rendered_powershell_SHA256"] != p17_result[
        "rendered_powershell_SHA256"
    ]
    package = p17_result["package"]
    assert package["branch_name"] == _P18_9_2_HANDOFF_BRANCH
    assert package["remote_name"] == "origin"
    assert package["expected_parent_commit"] == _P18_9_2_HANDOFF_PARENT
    assert tuple(
        candidate["relative_path"] for candidate in package["candidates"]
    ) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    assert tuple(package["post_commit_expectation"]["expected_candidate_paths"]) == (
        _P18_9_2_HANDOFF_CANDIDATE_PATHS
    )
    stage_commands = [
        command for command in package["commands"] if command["kind"] == "stage_path"
    ]
    assert [command["argv"] for command in stage_commands] == [
        ["git", "add", "--", path] for path in _P18_9_2_HANDOFF_CANDIDATE_PATHS
    ]
    assert all(
        command["automatic_execution_authorized"] is False
        for command in package["commands"]
    )
    materialization_plan = record["human_candidate_materialization_plan"]
    assert materialization_plan["materialization_required"] is True
    assert materialization_plan["cross_checkout_strategy"][
        "scratch_workspace_may_differ_from_git_checkout"
    ] is True
    assert tuple(materialization_plan["candidate_paths"]) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    assert {
        item["relative_path"]: item["source_SHA256"]
        for item in materialization_plan["candidates"]
    } == source_hashes
    assert {
        item["relative_path"]: item["accepted_candidate_SHA256"]
        for item in materialization_plan["candidates"]
    } == candidate_hashes
    assert {
        item["relative_path"]: item["target_materialization_state"]
        for item in materialization_plan["candidates"]
    } == {path: "target_at_expected_source" for path in _P18_9_2_HANDOFF_CANDIDATE_PATHS}
    rendered = record["rendered_handoff_powershell"]
    assert "Resolve-C12MaterializationPath" in rendered
    assert "wsl.exe wslpath" in rendered
    assert "Get-FileHash -Algorithm SHA256" in rendered
    assert "Copy-Item -LiteralPath $ScratchCandidatePath -Destination $TargetPath -Force" in rendered
    assert "post-materialization SHA mismatch" in rendered
    assert "Assert-C12StatusPolicy" in rendered
    assert "2_products/pepper-agent/.runtime-logs/**" in rendered
    assert "package-lock.json" not in rendered
    assert "git add ." not in rendered.lower()
    assert "git add -- $Candidate.RelativePath" in rendered

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "review_accepted_pending_human_git_handoff"
    assert workflow["human_git_handoff_state"] == "prepared_pending_human_execution"
    assert workflow["git_handoff_state"] == "human_git_authority_preserved"
    assert workflow["ticket_closed"] is False
    assert workflow["next_ticket_generated"] is False
    assert workflow["next_action"]["id"] == "COMPLETE_P18_9_2_HUMAN_GIT_HANDOFF"
    assert workflow["human_git_handoff_prepare_authority"]["candidate_paths"] == list(
        _P18_9_2_HANDOFF_CANDIDATE_PATHS
    )
    assert workflow["human_git_handoff_prepare_authority"]["materialization_required"] is True
    assert workflow["materialization_required"] is True
    assert workflow["tolerated_untracked_exclusions"] == [
        "2_products/pepper-agent/.runtime-logs/**"
    ]
    assert workflow["current_ticket_human_git_handoff_prepare"][
        "P17_7_handoff_result_SHA256"
    ] == prepared["P17_7_handoff_result_SHA256"]
    assert "human_git_handoff_completion_authority" not in workflow

    replay = pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("prepare replay must not inspect Git"),
    )
    assert replay["idempotent_replay"] is True
    assert replay["handoff_prepare_record_SHA256"] == prepared[
        "handoff_prepare_record_SHA256"
    ]


def test_p18_9_2_prepare_human_git_handoff_requires_accepted_review(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6842,
    )

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("accepted-review gap must stop before Git inspection"),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "ACCEPTED_REVIEW_AUTHORITY_GAP"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert not fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_prepare_human_git_handoff_blocks_review_package_drift(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6843,
    )
    _tamper_p18_9_2_review_prepare_record(fixture.pr, "review_package")

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("review-package drift must stop before Git inspection"),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "ACCEPTED_REVIEW_AUTHORITY_GAP"
    assert blocked["reviewed_run_id"] is None
    assert blocked["reviewed_candidate_SHA256"] is None
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert not fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_prepare_human_git_handoff_blocks_accepted_binding_drift(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6844,
    )
    drifted_review = dict(fixture.accepted_record)
    drifted_review["review_package_SHA256"] = "6" * 64
    monkeypatch.setattr(
        fixture.pr,
        "load_current_ticket_review_decision_record",
        lambda *, projection_record=None, allow_historical_mismatch=False: drifted_review,
    )

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("accepted binding drift must stop before Git inspection"),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "ACCEPTED_REVIEW_CANDIDATE_BINDING_MISMATCH"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert not fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_prepare_human_git_handoff_blocks_workflow_gap(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6845,
    )
    workflow = fixture.pr.build_workflow_control_snapshot()
    workflow.update({
        "workflow_status": "executing",
        "active_execution_count": 1,
        "execution_state": "active_executions",
    })
    monkeypatch.setattr(fixture.pr, "build_workflow_control_snapshot", lambda: workflow)

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("workflow gap must stop before Git inspection"),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "HUMAN_GIT_HANDOFF_PREPARE_ACTION_GAP"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert not fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_prepare_human_git_handoff_blocks_after_completion(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6846,
    )
    monkeypatch.setattr(
        fixture.pr,
        "load_current_ticket_human_git_handoff_completion_record",
        lambda *, projection_record=None, review_decision_record=None: {
            "completion_record_SHA256": "f" * 64,
        },
    )

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("completed handoff must stop before Git inspection"),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "HUMAN_GIT_HANDOFF_ALREADY_COMPLETED"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert not fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_prepare_human_git_handoff_supersedes_c11_prepare_record(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6847,
    )
    source_hashes, _candidate_hashes = _p18_9_2_candidate_hash_maps(
        fixture.candidate_files
    )
    prepared = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=source_hashes,
        ),
    )
    path = fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2")
    old_record = json.loads(path.read_text(encoding="utf-8"))
    old_record["schema_version"] = 1
    for key in (
        "human_candidate_materialization_plan",
        "materialization_plan_SHA256",
        "materialization_required",
        "materialization_strategy",
        "materialization_source_workspace",
        "materialization_candidate_entries",
        "tolerated_untracked_exclusions",
        "unexpected_dirty_path_policy",
        "preflight_dirty_status",
        "P17_7_rendered_handoff_powershell",
        "P17_7_rendered_powershell_SHA256",
        "canonical_source_mutation_by_Pepper",
    ):
        old_record.pop(key, None)
    old_record["rendered_powershell_SHA256"] = old_record["P17_7_handoff_result_SHA256"]
    old_record["handoff_prepare_record_SHA256"] = (
        fixture.pr._human_git_handoff_prepare_record_digest(old_record)
    )
    path.write_text(
        json.dumps(old_record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    regenerated = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=source_hashes,
        ),
    )

    assert regenerated["handoff_preparation_recorded"] is True
    assert regenerated["idempotent_replay"] is False
    assert regenerated["handoff_prepare_record_SHA256"] != prepared[
        "handoff_prepare_record_SHA256"
    ]
    assert regenerated["review_decision_SHA256"] == fixture.accepted[
        "review_decision_SHA256"
    ]
    assert regenerated["reviewed_candidate_SHA256"] == fixture.accepted[
        "reviewed_candidate_SHA256"
    ]
    assert regenerated["materialization_required"] is True
    history_path = fixture.pr.human_git_handoff_prepare_history_path_for_ticket("P18.9.2")
    history_text = history_path.read_text(encoding="utf-8")
    assert "superseded_or_invalid_human_git_handoff_prepare_authority" in history_text
    assert '"schema_version": 1' in history_text


def test_p18_9_2_prepare_human_git_handoff_blocks_source_sha_mismatch(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6848,
    )
    source_hashes, _candidate_hashes = _p18_9_2_candidate_hash_maps(
        fixture.candidate_files
    )
    mismatched = dict(source_hashes)
    mismatched[_P18_9_2_HANDOFF_CANDIDATE_PATHS[0]] = "0" * 64

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=mismatched,
        ),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "MATERIALIZATION_SOURCE_SHA_MISMATCH"
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False
    assert blocked["canonical_source_mutation_by_Pepper"] is False
    assert not fixture.pr.human_git_handoff_prepare_record_path_for_ticket("P18.9.2").exists()


@pytest.mark.parametrize(
    ("status_entries", "expected_status", "expected_tracked", "expected_untracked"),
    [
        (
            [
                {
                    "status": "??",
                    "path": "2_products/pepper-agent/.runtime-logs/session.log",
                },
            ],
            "ok",
            [],
            [],
        ),
        (
            [
                {
                    "status": " M",
                    "path": "2_products/pepper-agent/package-lock.json",
                },
            ],
            "blocked_unexpected_remainder",
            ["2_products/pepper-agent/package-lock.json"],
            [],
        ),
        (
            [
                {
                    "status": " M",
                    "path": "2_products/pepper-agent/tests/hermes_cli/test_agent_platform_lead_agent_workflow_context.py",
                },
            ],
            "blocked_unexpected_remainder",
            [
                "2_products/pepper-agent/tests/hermes_cli/test_agent_platform_lead_agent_workflow_context.py"
            ],
            [],
        ),
        (
            [
                {
                    "status": "??",
                    "path": "2_products/pepper-agent/web/src/agent-platform/runtime-overview/unbound.tmp",
                },
            ],
            "blocked_unexpected_remainder",
            [],
            [
                "2_products/pepper-agent/web/src/agent-platform/runtime-overview/unbound.tmp"
            ],
        ),
    ],
)
def test_p18_9_2_prepare_human_git_handoff_exclusion_dirty_status_policy(
    projection_home,
    monkeypatch,
    status_entries,
    expected_status,
    expected_tracked,
    expected_untracked,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6849,
    )
    source_hashes, _candidate_hashes = _p18_9_2_candidate_hash_maps(
        fixture.candidate_files
    )

    prepared = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=source_hashes,
            status_entries=status_entries,
        ),
    )

    assert prepared["handoff_preparation_recorded"] is True
    dirty_status = prepared["preflight_dirty_status"]
    assert dirty_status["status"] == expected_status
    assert [item["path"] for item in dirty_status["unexpected_tracked_paths"]] == expected_tracked
    assert [item["path"] for item in dirty_status["unexpected_untracked_paths"]] == expected_untracked
    assert dirty_status["policy"]["package_lock_modification_blocks_handoff"] is True
    assert dirty_status["policy"]["arbitrary_untracked_paths_block_handoff"] is True
    assert dirty_status["policy"][
        "tolerated_untracked_runtime_exclusions_may_remain_unstaged"
    ] is True
    rendered = prepared["rendered_handoff_powershell"]
    assert "2_products/pepper-agent/.runtime-logs/**" in rendered
    assert "git add -- $Candidate.RelativePath" in rendered
    assert ".runtime-logs/session.log" not in rendered


def test_p18_9_2_prepare_human_git_handoff_blocks_candidate_exclusion_overlap(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6850,
    )
    source_hashes, _candidate_hashes = _p18_9_2_candidate_hash_maps(
        fixture.candidate_files
    )
    monkeypatch.setattr(
        fixture.pr,
        "PEPPER_HUMAN_GIT_HANDOFF_TOLERATED_UNTRACKED_EXCLUSIONS",
        (_P18_9_2_HANDOFF_CANDIDATE_PATHS[0],),
    )

    blocked = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=source_hashes,
        ),
    )

    assert blocked["handoff_preparation_recorded"] is False
    assert blocked["blocker_code"] == "HANDOFF_EXCLUSION_CONFLICTS_WITH_CANDIDATE_PATH"
    assert blocked["Git_commands_executed"] == 0
    assert blocked["Git_mutation"] is False


def test_p18_9_2_cross_checkout_human_materialization_and_staging_isolated_git(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _accepted_p18_9_2_review_for_handoff_prepare(
        projection_home,
        monkeypatch,
        pid=6851,
    )
    source_hashes, candidate_hashes = _p18_9_2_candidate_hash_maps(
        fixture.candidate_files
    )
    prepared = fixture.pr.prepare_current_ticket_human_git_handoff(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            path_SHA256=source_hashes,
        ),
    )
    assert prepared["materialization_required"] is True

    checkout_root = projection_home / "isolated-human-git-checkout"
    scratch_root = fixture.candidate_fixture["workspace_root"]
    source_root = fixture.candidate_fixture["source_root"]
    assert checkout_root != scratch_root
    _create_isolated_source_checkout(
        source_root=source_root,
        checkout_root=checkout_root,
        candidate_paths=_P18_9_2_HANDOFF_CANDIDATE_PATHS,
    )

    before_diff = _run_isolated_git(
        checkout_root,
        "diff",
        "--name-only",
        "--",
        *_P18_9_2_HANDOFF_CANDIDATE_PATHS,
    )
    assert before_diff == ""
    for relative_path in _P18_9_2_HANDOFF_CANDIDATE_PATHS:
        assert _sha256_path(checkout_root / relative_path) == source_hashes[relative_path]

    _materialize_candidate_files_as_human(
        scratch_root=scratch_root,
        checkout_root=checkout_root,
        candidate_paths=_P18_9_2_HANDOFF_CANDIDATE_PATHS,
    )

    after_diff = _run_isolated_git(
        checkout_root,
        "diff",
        "--name-only",
        "--",
        *_P18_9_2_HANDOFF_CANDIDATE_PATHS,
    ).splitlines()
    assert tuple(after_diff) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    for relative_path in _P18_9_2_HANDOFF_CANDIDATE_PATHS:
        assert _sha256_path(checkout_root / relative_path) == candidate_hashes[relative_path]

    _run_isolated_git(checkout_root, "add", "--", *_P18_9_2_HANDOFF_CANDIDATE_PATHS)
    staged = _run_isolated_git(checkout_root, "diff", "--staged", "--name-only").splitlines()
    assert tuple(staged) == _P18_9_2_HANDOFF_CANDIDATE_PATHS
    _run_isolated_git(checkout_root, "commit", "-m", prepared["commit_message"])
    commit_sha = _run_isolated_git(checkout_root, "rev-parse", "HEAD")

    monkeypatch.setattr(
        fixture.pr,
        "_human_git_handoff_completion_successor_authority",
        lambda _binding: {
            "ticket_id": "P18.9.3",
            "ticket_title": "Post-Control Center Continuation",
            "next_action_id": "GENERATE_P18_9_3_REQUIRES_SEPARATE_HUMAN_ACTION",
            "canonical_roadmap_authority": "synthetic-test-authority",
            "roadmap_authority_path": "tests/fixtures/p18-9-3.md",
            "roadmap_authority_section": "P18.9.3",
            "dependency_ticket_ids": ("P18.9.2",),
            "roadmap_purpose": "Synthetic successor for isolated C12 completion admissibility.",
            "predecessor_ticket_id": "P18.9.2",
            "readiness_state": "ready",
            "authority_source": "test_fixture",
            "ticket_contract": {},
        },
    )
    completed = fixture.pr.complete_current_ticket_human_git_handoff(
        reviewed_run_id=fixture.accepted["reviewed_run_id"],
        reviewed_candidate_SHA256=fixture.accepted["reviewed_candidate_SHA256"],
        review_decision_SHA256=fixture.accepted["review_decision_SHA256"],
        commits=(commit_sha,),
        branch=_P18_9_2_HANDOFF_BRANCH,
        push_attestation="Human isolated test pushed the exact materialized candidate branch.",
        approved_committed_paths=_P18_9_2_HANDOFF_CANDIDATE_PATHS,
        excluded_paths=("2_products/pepper-agent/.runtime-logs/**",),
        validation_evidence=(
            "Isolated C12 test verified materialized SHA256 values and staged path set.",
        ),
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="COMPLETE_P18_9_2_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: _p18_9_2_handoff_git_snapshot(
            head=commit_sha,
            remote_head=commit_sha,
            path_SHA256=candidate_hashes,
            status_entries=[
                {
                    "status": "??",
                    "path": "2_products/pepper-agent/.runtime-logs/session.log",
                },
            ],
        ),
    )

    assert completed["handoff_completion_recorded"] is True, (
        completed.get("blocker_code"),
        completed.get("blocker_detail"),
    )
    assert completed["approved_committed_paths"] == list(_P18_9_2_HANDOFF_CANDIDATE_PATHS)
    assert completed["Git_commands_executed"] == 0
    assert completed["Git_mutation"] is False


def test_lead_agent_tool_prepares_p18_9_2_review_without_optional_guards(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6795,
    )

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {"human_request_text": "Prepare P18.9.2 review validation now"},
        )
    )

    assert result["success"] is True, result
    assert result["ticket_id"] == "P18.9.2"
    assert result["successful_run_id"] == retry["kanban_run_id"]
    record = state.pr.load_current_ticket_review_prepare_record(
        projection_record=state.projection_record,
    )
    assert record is not None
    assert record["requested_project_id"] is None
    assert record["requested_ticket_id"] is None
    assert record["requested_next_action_id"] is None
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False


@pytest.mark.parametrize(
    ("request_args", "expected_error"),
    [
        (
            {
                "human_request_text": "Prepare P18.9.0 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
            "targets a different ticket",
        ),
        (
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER-STALE",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
            "bounded to project PEPPER",
        ),
        (
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.0",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
            "bounded to ticket P18.9.2",
        ),
        (
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_0_REVIEW",
            },
            "review preparation requires PREPARE_P18_9_2_REVIEW",
        ),
    ],
)
def test_lead_agent_tool_rejects_mismatched_p18_9_2_review_prepare_authority(
    projection_home,
    monkeypatch,
    request_args,
    expected_error,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    state, _retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6796,
    )

    result = json.loads(handle_function_call("prepare_current_ticket_review", request_args))

    assert result["success"] is False
    assert expected_error in result["error"]
    assert not state.pr.review_prepare_record_path_for_ticket("P18.9.2").exists()
    workflow = state.pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
    assert workflow.get("dispatch_performed", False) is False
    assert workflow["execution_started"] is False
    assert workflow["worker_execution"] is False
    assert workflow["Git_mutation"] is False


def test_lead_agent_read_surfaces_reconstruct_prepared_p18_9_2_review_after_tool_prepare(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6797,
    )

    before = json.loads(handle_function_call("get_workflow_control", {}))
    assert before["workflow_status"] == "execution_completed"
    assert before["review_state"] == "ready_for_review_validation"
    assert before["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
    before_candidate_changes = before["workflow_control"]["candidate_changes_reference"]
    assert before_candidate_changes["files_changed"] == 3

    prepared = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
        )
    )
    assert prepared["success"] is True, prepared
    assert prepared["idempotent_replay"] is False
    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert prepared["successful_run_id"] == retry["kanban_run_id"]
    assert prepared["work_packet_id"] == state.projection_record["work_packet_id"]
    assert prepared["work_packet_id"] != "WP-DEFAULT-T_B6BAF825"
    assert prepared["work_packet_SHA256"] == state.projection_record["work_packet_SHA256"]
    assert state.pr.review_prepare_record_path_for_ticket("P18.9.2").exists()
    current_projection = state.pr._load_current_projection_record()
    assert current_projection["ticket_id"] == "P18.9.2", current_projection
    assert state.pr.load_current_ticket_review_prepare_record(
        projection_record=current_projection,
    ) is not None
    direct_snapshot = state.pr.build_workflow_control_snapshot()
    assert direct_snapshot["review_state"] == "prepared_pending_human_acceptance", direct_snapshot

    workflow = json.loads(handle_function_call("get_workflow_control", {}))
    review_status = json.loads(handle_function_call("get_review_status", {}))
    next_action = json.loads(handle_function_call("get_next_action", {}))

    for result in (workflow, review_status):
        assert result["success"] is True
        assert result["validation_state"] == "review_prepared_pending_human_acceptance"
        assert result["review_state"] == "prepared_pending_human_acceptance"
        assert result["recovery_state"] == "not_required"
        assert result["human_acceptance_required"] is True
        assert result["human_acceptance_recorded"] is False
        assert result["git_handoff_required"] is True
        assert result["git_handoff_state"] == "human_git_authority_preserved"
        assert result["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"
        assert result["next_action"]["required_human_action"] == "human_review_decision"
        assert result["next_action"]["target_ticket_id"] == "P18.9.2"
        assert result["Git_mutation"] is False

    assert workflow["workflow_status"] == "review_prepared_pending_human_acceptance"
    assert workflow["workflow_state"] == "P18.9.2-REVIEW-PREPARED-PENDING-HUMAN-ACCEPTANCE"
    assert workflow["active_execution_count"] == 0
    assert workflow["workflow_control"]["candidate_changes_reference"] == before_candidate_changes
    assert workflow["review_prepare_authority"]["review_prepare_action_SHA256"] == prepared[
        "review_prepare_action_SHA256"
    ]
    assert next_action["success"] is True
    assert next_action["workflow_status"] == "review_prepared_pending_human_acceptance"
    assert next_action["review_state"] == "prepared_pending_human_acceptance"
    assert next_action["human_acceptance_required"] is True
    assert next_action["human_acceptance_recorded"] is False
    assert next_action["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"
    assert next_action["Git_mutation"] is False

    repeated_workflow = json.loads(handle_function_call("get_workflow_control", {}))
    assert repeated_workflow["workflow_status"] == workflow["workflow_status"]
    assert repeated_workflow["review_state"] == workflow["review_state"]
    assert repeated_workflow["next_action"] == workflow["next_action"]

    replay = state.pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert replay["idempotent_replay"] is True
    assert replay["review_prepare_action_SHA256"] == prepared[
        "review_prepare_action_SHA256"
    ]
    assert replay["dispatch_performed"] is False
    assert replay["execution_started"] is False
    assert replay["Git_mutation"] is False


@pytest.mark.parametrize(
    "tamper_kind",
    [
        "digest",
        "ticket",
        "work_packet_id",
        "work_packet_sha",
        "projection_sha",
        "run_id",
        "completion_result",
        "review_package",
        "acceptance_contract",
        "criteria_revision",
        "candidate_materialization",
    ],
)
def test_p18_9_2_review_prepare_overlay_fails_closed_for_stale_or_malformed_authority(
    projection_home,
    monkeypatch,
    tamper_kind,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    state, _retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6798,
    )
    prepared = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
        )
    )
    assert prepared["success"] is True, prepared
    _tamper_p18_9_2_review_prepare_record(state.pr, tamper_kind)

    projection = state.pr._load_current_projection_record()
    with pytest.raises(state.pr.ProductRuntimeConflict):
        state.pr.load_current_ticket_review_prepare_record(projection_record=projection)

    workflow = state.pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
    assert workflow["blocker_count"] >= 1
    assert any(
        "REVIEW-PREPARE-AUTHORITY" in str(blocker.get("id"))
        and blocker.get("status") == "blocked_by_invalid_review_prepare_authority"
        for blocker in workflow["remaining_blockers"]
    )
    assert "review_prepare_authority" not in workflow
    assert workflow["execution_started"] is False
    assert workflow["worker_execution"] is False
    assert workflow["Git_mutation"] is False


def test_p18_9_0_review_prepare_compatibility_does_not_shadow_current_p18_9_2(
    projection_home,
    monkeypatch,
) -> None:
    state, _retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6799,
    )
    legacy_path = state.pr.review_prepare_record_path_for_ticket("P18.9.0")
    legacy_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_path.write_text(json.dumps({"ticket_id": "P18.9.0"}) + "\n", encoding="utf-8")

    workflow = state.pr.build_workflow_control_snapshot()

    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
    assert workflow["blocker_count"] == 0
    assert "review_prepare_authority" not in workflow


def test_p18_9_2_review_decision_supersedes_prepared_review_overlay(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6800,
    )
    prepared = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.2 review validation now",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
        )
    )
    assert prepared["success"] is True, prepared
    prepared_workflow = state.pr.build_workflow_control_snapshot()
    assert prepared_workflow["review_state"] == "prepared_pending_human_acceptance"
    assert prepared_workflow["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"

    decision = state.pr.submit_current_ticket_review_decision(
        decision="accept",
        feedback="Human accepts the validated P18.9.2 run candidate for human Git handoff.",
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
    )

    assert decision["review_decision"] == "accept"
    assert decision["dispatch_performed"] is False
    assert decision["execution_started"] is False
    assert decision["Git_mutation"] is False
    workflow = state.pr.build_workflow_control_snapshot()
    assert workflow["review_prepare_authority"]["review_prepare_action_SHA256"] == prepared[
        "review_prepare_action_SHA256"
    ]
    assert workflow["review_decision_recorded"] is True
    assert workflow["review_decision_required"] is False
    assert workflow["workflow_status"] == "review_accepted_pending_human_git_handoff"
    assert workflow["review_state"] == "accepted"
    assert workflow["validation_state"] == "review_accepted"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_HUMAN_GIT_HANDOFF"
    assert workflow["next_action"]["required_human_action"] == "human_git_handoff"
    assert workflow["human_acceptance_required"] is False
    assert workflow["human_acceptance_recorded"] is True
    assert workflow["execution_started"] is False
    assert workflow["worker_execution"] is False
    assert workflow["Git_mutation"] is False


def test_p18_9_2_prepared_review_reject_records_no_revision_or_execution(
    projection_home,
    monkeypatch,
) -> None:
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6801,
    )
    pr = state.pr
    prepared = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance"

    rejected = pr.submit_current_ticket_review_decision(
        decision="reject",
        feedback="Human rejects the validated P18.9.2 candidate and requests no further execution.",
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("reject must not spawn"),
    )

    assert rejected["review_decision"] == "reject"
    assert rejected["review_source_authority_kind"] == "review_prepare"
    assert rejected["review_prepare_action_SHA256"] == prepared["review_prepare_action_SHA256"]
    assert rejected["review_validation_decision"] == "cancelled"
    assert rejected["review_state"] == "rejected"
    assert rejected["review_revision_request_reference"] is None
    assert rejected["revision_attempt_started"] is False
    assert rejected["dispatch_performed"] is False
    assert rejected["execution_started"] is False
    assert rejected["Git_mutation"] is False
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "review_rejected_no_execution"
    assert workflow["review_state"] == "rejected"
    assert workflow["next_action"]["id"] == "P18_9_2_REVIEW_REJECTED_NO_EXECUTION"
    assert not pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_prepared_review_changes_requested_derives_pending_revision_authority(
    projection_home,
    monkeypatch,
) -> None:
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6801,
    )
    pr = state.pr
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    prepared = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance"
    before = pr.build_workflow_control_snapshot()
    assert before["review_decision_required"] is True
    assert before.get("review_decision_recorded") is not True
    assert not pr.governed_autonomy_activation_record_path_for_ticket("P18.9.2").exists()

    changed = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback="Human requests P18.9.2 changes limited to runtime-overview-page.tsx.",
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("prepared review bridge must not spawn"),
    )

    assert changed["review_decision"] == "changes_requested"
    assert changed["review_source_authority_kind"] == "review_prepare"
    assert changed["review_prepare_action_SHA256"] == prepared["review_prepare_action_SHA256"]
    assert changed["review_package_SHA256"] == prepared["review_package_SHA256"]
    assert changed["review_validation_decision"] == "needs_correction"
    assert changed["review_state"] == "correction_required"
    assert changed["workflow_status"] == "review_changes_requested_revision_pending_continuation"
    assert changed["revision_attempt_started"] is False
    assert changed["revision_kanban_run_id"] is None
    assert changed["dispatch_performed"] is False
    assert changed["execution_started"] is False
    assert changed["worker_execution"] is False
    assert changed["Kanban_dispatch"] is False
    assert changed["Git_mutation"] is False
    revision_request = changed["review_revision_request_reference"]
    assert revision_request["fresh_execution_provenance"] == "human_review_changes_requested"
    assert revision_request["prior_terminal_run_id"] == retry["kanban_run_id"]
    assert revision_request["review_prepare_action_SHA256"] == prepared["review_prepare_action_SHA256"]
    assert revision_request["review_package_SHA256"] == prepared["review_package_SHA256"]
    assert revision_request["reviewed_candidate_SHA256"] == changed["reviewed_candidate_SHA256"]
    assert revision_request["review_decision_identity_SHA256"] == changed[
        "review_decision_identity_SHA256"
    ]
    assert revision_request["revision_source_base"] == "current_canonical_source"
    assert revision_request["reviewed_candidate_copied_to_revision_base"] is False
    assert changed["next_action"]["id"] == "CONTINUE_P18_9_2_GOVERNED_AUTONOMY"
    assert changed["next_action"]["required_human_action"] == (
        "governed_review_revision_continuation"
    )
    assert changed["next_action"]["fresh_execution_request_SHA256"] == revision_request[
        "fresh_execution_request_SHA256"
    ]

    activation = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=state.pr._load_current_projection_record(),
    )
    assert activation is not None
    assert activation["review_revision_activation_derived_from_review_decision"] is True
    runtime = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=state.pr._load_current_projection_record(),
        activation_record=activation,
    )
    assert runtime is not None
    assert runtime["governed_autonomy_runtime_status"] == (
        "review_revision_request_recorded_pending_continuation"
    )
    assert runtime["runtime_decision"] == "DIRECT"
    assert runtime["fresh_execution_requested"] is True
    assert runtime["fresh_execution_request_SHA256"] == revision_request[
        "fresh_execution_request_SHA256"
    ]
    assert runtime["fresh_execution_request_reference"] == revision_request
    assert runtime["dispatch_performed"] is False
    assert runtime["execution_started"] is False
    assert runtime["Git_mutation"] is False

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["review_decision_recorded"] is True
    assert workflow["review_decision_required"] is False
    assert workflow["workflow_status"] == "review_changes_requested_revision_pending_continuation"
    assert workflow["review_state"] == "correction_required"
    assert workflow["revision_attempt_started"] is False
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_2_GOVERNED_AUTONOMY"
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow.get("next_ticket_id") != "P18.9.3"
    assert workflow["Git_mutation"] is False

    replay = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback="Human requests P18.9.2 changes limited to runtime-overview-page.tsx.",
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("review decision replay must not spawn"),
    )
    assert replay["idempotent_replay"] is True
    assert replay["review_decision_SHA256"] == changed["review_decision_SHA256"]

    with pytest.raises(pr.ProductRuntimeConflict, match="different review decision"):
        pr.submit_current_ticket_review_decision(
            decision="reject",
            feedback="Human rejects the same P18.9.2 reviewed run.",
            reviewed_run_id=retry["kanban_run_id"],
            project_id="PEPPER",
            ticket_id="P18.9.2",
            next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("conflict must not spawn"),
        )


def test_p18_9_2_prepared_review_changes_requested_reuses_stop_for_human_history(
    projection_home,
    monkeypatch,
) -> None:
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6802,
    )
    pr = state.pr
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    prepared = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance"

    activation = pr.activate_current_ticket_governed_autonomy(
        human_request_text="I explicitly authorize governed autonomy activation status for P18.9.2.",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
    )
    assert activation["governed_autonomy_activation_recorded"] is True
    stop = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Stop for human after P18.9.2 activation without execution.",
        strategy="STOP_FOR_HUMAN",
        project_id="PEPPER",
        ticket_id="P18.9.2",
    )
    assert stop["runtime_decision"] == "STOP_FOR_HUMAN"
    assert stop["governed_autonomy_runtime_status"] == "blocked_stop_for_human"
    assert stop["dispatch_performed"] is False
    assert stop["execution_started"] is False
    assert stop["Git_mutation"] is False

    changed = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback="Human requests P18.9.2 changes limited to runtime-overview-page.tsx.",
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("prepared review bridge must not spawn"),
    )
    assert changed["review_decision"] == "changes_requested"
    assert changed["revision_attempt_started"] is False
    assert changed["revision_attempt_result"]["previous_runtime_state_SHA256"] == stop[
        "runtime_state_SHA256"
    ]
    assert changed["revision_attempt_result"]["budget_segment_previous_runtime_state_SHA256"] == stop[
        "runtime_state_SHA256"
    ]
    assert changed["revision_attempt_result"]["activation_created_from_review_decision"] is False
    assert changed["dispatch_performed"] is False
    assert changed["execution_started"] is False
    assert changed["Git_mutation"] is False


def test_p18_9_2_prepared_review_changes_requested_rejects_wrong_run(
    projection_home,
    monkeypatch,
) -> None:
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6803,
    )
    pr = state.pr
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    with pytest.raises(pr.ProductRuntimeConflict, match="review decision targets run"):
        pr.submit_current_ticket_review_decision(
            decision="changes_requested",
            feedback="Human requests P18.9.2 changes limited to runtime-overview-page.tsx.",
            reviewed_run_id=retry["kanban_run_id"] + 100,
            project_id="PEPPER",
            ticket_id="P18.9.2",
            next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("wrong run must not spawn"),
        )
    assert not pr.review_decision_record_path_for_ticket("P18.9.2").exists()
    assert not pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_review_decision_fails_closed_after_prepared_authority_drift(
    projection_home,
    monkeypatch,
) -> None:
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6804,
    )
    pr = state.pr
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    changed = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback="Human requests P18.9.2 changes limited to runtime-overview-page.tsx.",
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("prepared review bridge must not spawn"),
    )
    assert changed["review_decision"] == "changes_requested"

    _tamper_p18_9_2_review_prepare_record(pr, "review_package")

    with pytest.raises(pr.ProductRuntimeConflict):
        pr.load_current_ticket_review_decision_record(
            projection_record=pr._load_current_projection_record(),
        )


def test_p18_9_2_prepared_review_changes_requested_blocks_scope_expansion(
    projection_home,
    monkeypatch,
) -> None:
    state, retry = _p18_9_2_review_ready_for_tool_test(
        projection_home,
        monkeypatch,
        pid=6805,
    )
    pr = state.pr
    monkeypatch.setattr(pr, "_executor_provider_readiness", _ready_executor_provider_payload)
    pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    blocked = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback=(
            "Human requests P18.9.2 changes limited to runtime-overview-page.tsx and "
            "also asks to modify 2_products/pepper-agent/package-lock.json."
        ),
        reviewed_run_id=retry["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("authority expansion must not spawn"),
    )

    assert blocked["blocker_code"] == "REVIEW_FEEDBACK_REQUIRES_AUTHORITY_EXPANSION"
    assert blocked["authority_expansion_required"] is True
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_mutation"] is False
    assert not pr.review_decision_record_path_for_ticket("P18.9.2").exists()
    assert not pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.2").exists()


def test_p18_9_2_review_ready_terminal_triage_task_does_not_self_block_prepare(
    projection_home,
    monkeypatch,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    pr = state.pr
    retry = _start_recovered_p18_9_2_retry_for_test(state, monkeypatch, pid=6809)
    _write_p18_9_2_terminal_candidate_fixture(
        pr,
        projection_home,
        Path(retry["workspace_path"]),
    )
    _finish_projected_run_as_review_required_terminal(
        state.kanban_db,
        state.projected,
        retry["kanban_run_id"],
        summary=(
            "review-required: P18.9.2 Control Center Overview implementation is ready "
            "for human/code review; focused governed frontend validation passed."
        ),
        task_status="triage",
    )

    workflow = pr.build_workflow_control_snapshot()

    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["workflow_state"] == (
        "P18.9.2-GOVERNED-AUTONOMY-AWAITING-HUMAN-GIT-HANDOFF"
    )
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["recovery_state"] == "not_required"
    assert workflow["active_execution_count"] == 0
    assert workflow["terminal_outcome_class"] == "validated_review_required"
    assert workflow["validated_candidate_review_required"] is True
    assert workflow["candidate_changes_available"] is True
    assert workflow["blocker_count"] == 0, workflow["remaining_blockers"]
    assert workflow["remaining_blockers"] == []
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
    assert workflow["review_decision_required"] is False
    assert workflow["review_decision_recorded"] is False
    assert workflow["human_acceptance_required"] is False
    assert workflow["human_acceptance_recorded"] is False

    prepared = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert prepared["review_preparation_recorded"] is True
    assert prepared["successful_run_id"] == retry["kanban_run_id"]
    assert prepared["kanban_completion_result"]["run_id"] == retry["kanban_run_id"]
    assert prepared["kanban_completion_result"]["terminal_outcome_class"] == (
        "validated_review_required"
    )
    assert prepared["human_acceptance_required"] is True
    assert prepared["human_acceptance_recorded"] is False
    assert prepared["dispatch_performed"] is False
    assert prepared["execution_started"] is False
    assert prepared["Git_mutation"] is False
    after_prepare = pr.build_workflow_control_snapshot()
    assert after_prepare["review_decision_required"] is True
    assert after_prepare["review_decision_recorded"] is False
    assert after_prepare["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"


def test_p18_9_2_pending_revision_blocks_premature_second_review_prepare(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_changes_requested_revision_pending_fixture(
        projection_home,
        monkeypatch,
        first_pid=6806,
    )
    pr = fixture.pr

    blocked = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    assert blocked["review_prepare_status"] == "blocked"
    assert blocked["review_preparation_recorded"] is False
    assert blocked["blocker_code"] == "PEPPER_REVIEW_PREPARE_ACTION_GAP"
    assert "execution_completed" in blocked["blocker_detail"]
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_mutation"] is False
    current_prepare = json.loads(
        pr.review_prepare_record_path_for_ticket("P18.9.2").read_text(encoding="utf-8")
    )
    assert current_prepare["review_prepare_action_SHA256"] == fixture.prepared_13[
        "review_prepare_action_SHA256"
    ]
    current_decision = json.loads(
        pr.review_decision_record_path_for_ticket("P18.9.2").read_text(encoding="utf-8")
    )
    assert current_decision["review_decision_SHA256"] == fixture.changed_13[
        "review_decision_SHA256"
    ]
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "review_changes_requested_revision_pending_continuation"
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_2_GOVERNED_AUTONOMY"


def test_p18_9_2_active_corrective_run_blocks_review_prepare_without_rotation(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_active_revision_fixture(
        projection_home,
        monkeypatch,
        first_pid=6807,
        revision_pid=6808,
    )
    pr = fixture.pr

    blocked = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    assert blocked["review_prepare_status"] == "blocked"
    assert blocked["review_preparation_recorded"] is False
    assert blocked["blocker_code"] == "PEPPER_REVIEW_PREPARE_ACTION_GAP"
    assert "execution_completed" in blocked["blocker_detail"]
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_mutation"] is False
    current_prepare = json.loads(
        pr.review_prepare_record_path_for_ticket("P18.9.2").read_text(encoding="utf-8")
    )
    assert current_prepare["review_prepare_action_SHA256"] == fixture.prepared_13[
        "review_prepare_action_SHA256"
    ]
    assert not pr.review_decision_record_path_for_ticket("P18.9.2").exists()
    decision_history = [
        json.loads(line)["record"]
        for line in pr.review_decision_history_path_for_ticket("P18.9.2").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    assert any(
        item["review_decision_SHA256"] == fixture.changed_13["review_decision_SHA256"]
        for item in decision_history
    )
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "executing"
    assert workflow["active_execution_count"] == 1
    assert workflow["next_action"]["id"] == "MONITOR_P18_9_2_EXECUTION"


def test_p18_9_2_corrective_candidate_allows_second_review_round(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_two_round_changes_requested_fixture(
        projection_home,
        monkeypatch,
        first_pid=6812,
        revision_pid=6813,
    )
    pr = fixture.pr

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["workflow_state"] == (
        "P18.9.2-GOVERNED-AUTONOMY-AWAITING-HUMAN-GIT-HANDOFF"
    )
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["active_execution_count"] == 0
    assert workflow["blocker_count"] == 0, {
        "blocker_count": workflow["blocker_count"],
        "remaining_blocker_count": len(workflow["remaining_blockers"]),
        "remaining_blockers": workflow["remaining_blockers"],
        "governed_autonomy_blocker_code": workflow.get("governed_autonomy", {}).get(
            "blocker_code"
        ),
        "top_blocker_code": workflow.get("blocker_code"),
    }
    assert workflow["remaining_blockers"] == []
    assert workflow["human_acceptance_required"] is False
    assert workflow.get("human_acceptance_recorded") is not True
    assert workflow.get("review_decision_required") is not True
    assert workflow.get("review_decision_recorded") is not True
    assert workflow["terminal_outcome_class"] == "validated_review_required"
    assert workflow["governed_autonomy"]["terminal_run_id"] == fixture.started_14[
        "kanban_run_id"
    ]
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"

    prepared_14 = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    assert prepared_14["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert prepared_14["review_preparation_recorded"] is True
    assert prepared_14["successful_run_id"] == fixture.started_14["kanban_run_id"]
    assert prepared_14["successful_run_id"] != fixture.run_13["kanban_run_id"]
    assert prepared_14["review_prepare_action_SHA256"] != fixture.prepared_13[
        "review_prepare_action_SHA256"
    ]
    assert prepared_14["review_package_SHA256"] != fixture.prepared_13[
        "review_package_SHA256"
    ]
    assert prepared_14["kanban_completion_result"]["run_id"] == fixture.started_14[
        "kanban_run_id"
    ]
    assert prepared_14["kanban_completion_result"]["terminal_outcome_class"] == (
        "validated_review_required"
    )
    assert prepared_14["human_acceptance_required"] is True
    assert prepared_14["human_acceptance_recorded"] is False
    assert prepared_14["Git_mutation"] is False
    assert prepared_14["dispatch_performed"] is False
    assert prepared_14["execution_started"] is False
    assert prepared_14["Kanban_dispatch"] is False

    after_prepare = pr.build_workflow_control_snapshot()
    assert after_prepare["workflow_status"] == "review_prepared_pending_human_acceptance"
    assert after_prepare["review_decision_required"] is True
    assert after_prepare["review_decision_recorded"] is False
    assert after_prepare["human_acceptance_required"] is True
    assert after_prepare["human_acceptance_recorded"] is False
    assert after_prepare["review_prepare_authority"]["successful_run_id"] == (
        fixture.started_14["kanban_run_id"]
    )
    assert after_prepare["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"

    replay = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert replay["idempotent_replay"] is True
    assert replay["review_prepare_action_SHA256"] == prepared_14[
        "review_prepare_action_SHA256"
    ]

    history_path = pr.review_prepare_history_path_for_ticket("P18.9.2")
    history = [
        json.loads(line)["record"]
        for line in history_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert any(
        item["review_prepare_action_SHA256"]
        == fixture.prepared_13["review_prepare_action_SHA256"]
        for item in history
    )
    decision_history_path = pr.review_decision_history_path_for_ticket("P18.9.2")
    decision_history = [
        json.loads(line)["record"]
        for line in decision_history_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert any(
        item["review_decision_SHA256"] == fixture.changed_13["review_decision_SHA256"]
        for item in decision_history
    )
    runtime_history_path = pr.governed_autonomy_runtime_history_path_for_ticket("P18.9.2")
    runtime_history = [
        json.loads(line)["record"]
        for line in runtime_history_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert any(
        item["fresh_execution_request_SHA256"]
        == fixture.revision_request["fresh_execution_request_SHA256"]
        and item["governed_autonomy_runtime_status"]
        == "review_revision_request_recorded_pending_continuation"
        for item in runtime_history
    )
    assert not pr.review_decision_record_path_for_ticket("P18.9.2").exists()
    current_runtime = json.loads(
        pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.2").read_text(
            encoding="utf-8"
        )
    )
    assert current_runtime["kanban_run_id"] == fixture.started_14["kanban_run_id"]
    assert current_runtime["fresh_execution_request_SHA256"] == fixture.revision_request[
        "fresh_execution_request_SHA256"
    ]
    assert current_runtime["governed_autonomy_runtime_status"] != (
        "review_revision_request_recorded_pending_continuation"
    )


def test_p18_9_2_tool_prepare_uses_second_round_terminal_authority(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    fixture = _p18_9_2_two_round_changes_requested_fixture(
        projection_home,
        monkeypatch,
        first_pid=6814,
        revision_pid=6815,
    )

    result = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.2 review validation for the fresh revision.",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
        )
    )

    assert result["success"] is True, result
    assert result["idempotent_replay"] is False
    assert result["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert result["successful_run_id"] == fixture.started_14["kanban_run_id"]
    assert result["successful_run_id"] != fixture.run_13["kanban_run_id"]
    assert result["review_prepare_action_SHA256"] != fixture.prepared_13[
        "review_prepare_action_SHA256"
    ]
    assert result["review_package_SHA256"] != fixture.prepared_13[
        "review_package_SHA256"
    ]
    assert result["dispatch_performed"] is False
    assert result["execution_started"] is False
    assert result["Git_mutation"] is False


def test_p18_9_2_round_two_review_ready_triage_task_tool_path_prepares_fresh_review(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    fixture = _p18_9_2_two_round_changes_requested_fixture(
        projection_home,
        monkeypatch,
        first_pid=6818,
        revision_pid=6819,
        terminal_task_status="triage",
    )

    workflow_control = json.loads(handle_function_call("get_workflow_control", {}))
    review_status = json.loads(handle_function_call("get_review_status", {}))
    next_action = json.loads(handle_function_call("get_next_action", {}))

    for result in (workflow_control, review_status, next_action):
        assert result["success"] is True
        assert result["review_state"] == "ready_for_review_validation"
        assert result["validation_state"] == "execution_completed_pending_validation"
        assert result["next_action"]["id"] == "PREPARE_P18_9_2_REVIEW"
        assert result["Git_mutation"] is False
    for result in (workflow_control, next_action):
        assert result["current_ticket_id"] == "P18.9.2"
        assert result["workflow_status"] == "execution_completed"
    assert workflow_control["active_execution_count"] == 0
    assert workflow_control["workflow_control"]["blocker_count"] == 0
    assert workflow_control["workflow_control"]["remaining_blockers"] == []
    assert review_status["review_decision_required"] is False
    assert review_status["review_decision_recorded"] is False
    assert review_status["human_acceptance_required"] is False
    assert review_status["human_acceptance_recorded"] is False

    prepared = json.loads(
        handle_function_call(
            "prepare_current_ticket_review",
            {
                "human_request_text": "Prepare P18.9.2 review validation for the fresh revision.",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "next_action_id": "PREPARE_P18_9_2_REVIEW",
            },
        )
    )

    assert prepared["success"] is True, prepared
    assert prepared["idempotent_replay"] is False
    assert prepared["review_prepare_status"] == "prepared_pending_human_acceptance"
    assert prepared["successful_run_id"] == fixture.started_14["kanban_run_id"]
    assert prepared["successful_run_id"] != fixture.run_13["kanban_run_id"]
    assert prepared["review_prepare_action_SHA256"] != fixture.prepared_13[
        "review_prepare_action_SHA256"
    ]
    assert prepared["review_package_SHA256"] != fixture.prepared_13[
        "review_package_SHA256"
    ]
    assert prepared["dispatch_performed"] is False
    assert prepared["execution_started"] is False
    assert prepared["Git_mutation"] is False

    fresh_review = json.loads(handle_function_call("get_review_status", {}))
    fresh_next_action = json.loads(handle_function_call("get_next_action", {}))
    for result in (fresh_review, fresh_next_action):
        assert result["success"] is True
        assert result["review_state"] == "prepared_pending_human_acceptance"
        assert result["review_decision_required"] is True
        assert result["human_acceptance_required"] is True
        assert result["human_acceptance_recorded"] is False
        assert result["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"
        assert result["Git_mutation"] is False
    assert fresh_review["review_decision_recorded"] is False
    assert fresh_next_action["workflow_status"] == "review_prepared_pending_human_acceptance"


def test_p18_9_2_current_review_candidate_list_content_diff_and_aggregate_flow(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6821,
    )
    pr = fixture.pr
    page_path = (
        "2_products/pepper-agent/web/src/agent-platform/runtime-overview/"
        "runtime-overview-page.tsx"
    )
    page_entry = next(item for item in fixture.candidate_files if item["path"] == page_path)

    listed = pr.inspect_current_ticket_review_candidate(
        operation="list",
        project_id="PEPPER",
        ticket_id="P18.9.2",
        reviewed_run_id=fixture.review["successful_run_id"],
        review_package_SHA256=fixture.review["review_package_SHA256"],
        review_prepare_action_SHA256=fixture.review["review_prepare_action_SHA256"],
    )

    assert listed["inspection_status"] == "available"
    assert listed["review_package_SHA256"] == fixture.review["review_package_SHA256"]
    assert listed["review_prepare_action_SHA256"] == fixture.review[
        "review_prepare_action_SHA256"
    ]
    assert listed["reviewed_run_id"] == fixture.retry["kanban_run_id"]
    assert listed["candidate_file_count"] == 3
    assert listed["candidate_paths"] == fixture.candidate_paths
    assert [item["path"] for item in listed["candidate_files"]] == fixture.candidate_paths
    assert listed["integrity_validation_result"] == "passed"
    assert listed["WorkPacket_scope_validation_result"] == "passed"
    assert listed["Git_mutation"] is False
    assert listed["dispatch_performed"] is False
    assert listed["worker_execution"] is False
    assert listed["review_state_mutation"] is False
    assert listed["candidate_mutation"] is False

    content_1 = pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=page_path,
    )
    content_2 = pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=page_path,
    )
    assert content_1["inspection_status"] == "content_available"
    assert content_1["content"] == content_2["content"]
    assert content_1["source_SHA256"] == page_entry["source_SHA256"]
    assert content_1["candidate_SHA256"] == page_entry["workspace_SHA256"]
    assert content_1["candidate_byte_count"] == len(
        (fixture.candidate_fixture["workspace_root"] / page_path).read_bytes()
    )
    assert content_1["content_truncated"] is False
    assert content_1["content_complete"] is True
    for marker in (
        "Current Work",
        "Next Governed Action",
        "Needs Attention",
        "Execution",
        "Governed State",
    ):
        assert marker in content_1["content"]

    diff_1 = pr.inspect_current_ticket_review_candidate(
        operation="diff",
        candidate_path=page_path,
    )
    diff_2 = pr.inspect_current_ticket_review_candidate(
        operation="diff",
        candidate_path=page_path,
    )
    assert diff_1["inspection_status"] == "diff_available"
    assert diff_1["unified_diff"] == diff_2["unified_diff"]
    assert diff_1["diff_truncated"] is False
    assert diff_1["diff_complete"] is True
    assert f"--- a/{page_path}" in diff_1["unified_diff"]
    assert f"+++ b/{page_path}" in diff_1["unified_diff"]
    assert "-export function RuntimeOverviewPage() { return null }" in diff_1[
        "unified_diff"
    ]
    assert "+      <h2>Current Work</h2>" in diff_1["unified_diff"]

    aggregate = pr.inspect_current_ticket_review_candidate(operation="aggregate_diff")
    assert aggregate["inspection_status"] == "aggregate_diff_available"
    assert aggregate["diff_truncated"] is False
    for candidate_path in fixture.candidate_paths:
        assert f"+++ b/{candidate_path}" in aggregate["unified_diff"]
    assert "test('renders Current Work'" in aggregate["unified_diff"]

    truncated = pr.inspect_current_ticket_review_candidate(
        operation="diff",
        candidate_path=page_path,
        max_bytes=120,
    )
    assert truncated["diff_truncated"] is True
    assert truncated["diff_complete"] is False
    assert truncated["retained_diff_byte_count"] <= 120

    after = pr.build_workflow_control_snapshot()
    assert after["review_state"] == "prepared_pending_human_acceptance"
    assert after["review_decision_recorded"] is False
    assert after["next_action"]["id"] == "SUBMIT_P18_9_2_REVIEW_DECISION"
    assert after["Git_mutation"] is False


def test_p18_9_2_current_review_candidate_tool_path_full_inspection_flow(
    projection_home,
    monkeypatch,
) -> None:
    import tools.pepper_workflow_tools  # noqa: F401
    from model_tools import handle_function_call

    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6822,
    )

    status = json.loads(handle_function_call("get_review_status", {}))
    assert status["success"] is True
    assert status["review_state"] == "prepared_pending_human_acceptance"
    assert status["review_decision_recorded"] is False

    listed = json.loads(
        handle_function_call(
            "inspect_current_ticket_review_candidate",
            {
                "operation": "list",
                "project_id": "PEPPER",
                "ticket_id": "P18.9.2",
                "reviewed_run_id": fixture.review["successful_run_id"],
                "review_package_SHA256": fixture.review["review_package_SHA256"],
            },
        )
    )
    assert listed["success"] is True, listed
    assert listed["inspection_status"] == "available"
    assert [item["path"] for item in listed["candidate_files"]] == fixture.candidate_paths

    diffs = []
    for candidate_path in fixture.candidate_paths:
        inspected = json.loads(
            handle_function_call(
                "inspect_current_ticket_review_candidate",
                {"operation": "diff", "candidate_path": candidate_path},
            )
        )
        assert inspected["success"] is True, inspected
        assert inspected["inspection_status"] == "diff_available"
        assert inspected["candidate_path"] == candidate_path
        assert inspected["Git_mutation"] is False
        assert inspected["dispatch_performed"] is False
        assert inspected["worker_execution"] is False
        diffs.append(inspected["unified_diff"])

    combined = "\n".join(diffs)
    for marker in (
        "Current Work",
        "Next Governed Action",
        "Needs Attention",
        "Execution",
        "Governed State",
        "test('renders Current Work'",
    ):
        assert marker in combined

    fresh_status = json.loads(handle_function_call("get_review_status", {}))
    assert fresh_status["success"] is True
    assert fresh_status["review_state"] == "prepared_pending_human_acceptance"
    assert fresh_status["review_decision_recorded"] is False
    assert fresh_status["Git_mutation"] is False


def test_p18_9_2_review_candidate_inspection_rejects_unbound_and_guard_mismatches(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6823,
    )
    pr = fixture.pr

    wrong_path = pr.inspect_current_ticket_review_candidate(
        operation="diff",
        candidate_path="2_products/pepper-agent/web/src/agent-platform/runtime-overview/not-bound.tsx",
    )
    assert wrong_path["inspection_status"] == "blocked"
    assert wrong_path["blocker_code"] == "CANDIDATE_PATH_NOT_AUTHORIZED"

    traversal = pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path="../outside.txt",
    )
    assert traversal["inspection_status"] == "blocked"
    assert traversal["blocker_code"] == "PATH_CONTAINMENT_BLOCKER"

    wrong_run = pr.inspect_current_ticket_review_candidate(
        operation="list",
        reviewed_run_id=fixture.review["successful_run_id"] + 1,
    )
    assert wrong_run["inspection_status"] == "blocked"
    assert wrong_run["blocker_code"] == "REVIEW_RUN_GUARD_MISMATCH"

    wrong_package = pr.inspect_current_ticket_review_candidate(
        operation="list",
        review_package_SHA256="0" * 64,
    )
    assert wrong_package["inspection_status"] == "blocked"
    assert wrong_package["blocker_code"] == "REVIEW_PACKAGE_GUARD_MISMATCH"

    wrong_ticket = pr.inspect_current_ticket_review_candidate(
        operation="list",
        ticket_id="P18.9.1",
    )
    assert wrong_ticket["inspection_status"] == "blocked"
    assert wrong_ticket["blocker_code"] == "TICKET_GUARD_MISMATCH"


@pytest.mark.parametrize(
    ("side", "blocker_detail"),
    [
        ("source", "source SHA256 drifted"),
        ("candidate", "workspace SHA256 drifted"),
    ],
)
def test_p18_9_2_review_candidate_inspection_fails_closed_on_hash_drift(
    projection_home,
    monkeypatch,
    side: str,
    blocker_detail: str,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6824,
    )
    pr = fixture.pr
    rel = fixture.candidate_paths[0]
    root = (
        fixture.candidate_fixture["source_root"]
        if side == "source"
        else fixture.candidate_fixture["workspace_root"]
    )
    (root / rel).write_text(blocker_detail + "\n", encoding="utf-8")

    result = pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=rel,
    )

    assert result["inspection_status"] == "blocked"
    assert result["blocker_code"] == "CANDIDATE_INTEGRITY_BLOCKER"
    assert result["Git_mutation"] is False


def test_p18_9_2_review_candidate_inspection_historical_package_cannot_shadow_current(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_two_round_changes_requested_fixture(
        projection_home,
        monkeypatch,
        first_pid=6825,
        revision_pid=6826,
        terminal_task_status="triage",
    )
    current = fixture.pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    listed = fixture.pr.inspect_current_ticket_review_candidate(operation="list")
    assert listed["inspection_status"] == "available"
    assert listed["reviewed_run_id"] == fixture.started_14["kanban_run_id"]
    assert listed["review_package_SHA256"] == current["review_package_SHA256"]
    assert listed["review_package_SHA256"] != fixture.prepared_13[
        "review_package_SHA256"
    ]

    historical_guard = fixture.pr.inspect_current_ticket_review_candidate(
        operation="list",
        review_package_SHA256=fixture.prepared_13["review_package_SHA256"],
    )
    assert historical_guard["inspection_status"] == "blocked"
    assert historical_guard["blocker_code"] == "REVIEW_PACKAGE_GUARD_MISMATCH"


def test_p18_9_2_review_candidate_inspection_rejects_symlink_escape(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6827,
    )
    rel = fixture.candidate_paths[1]
    expected_text = fixture.candidate_fixture["modified_files"][rel][1]
    outside = projection_home / "outside-candidate.tsx"
    outside.write_text(expected_text, encoding="utf-8")
    candidate_path = fixture.candidate_fixture["workspace_root"] / rel
    candidate_path.unlink()
    _make_file_symlink_or_skip(candidate_path, outside)

    result = fixture.pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=rel,
    )

    assert result["inspection_status"] == "blocked"
    assert result["blocker_code"] == "PATH_CONTAINMENT_BLOCKER"
    assert result["Git_mutation"] is False


def test_p18_9_2_review_candidate_inspection_missing_candidate_fails_closed(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6828,
    )
    rel = fixture.candidate_paths[1]
    (fixture.candidate_fixture["workspace_root"] / rel).unlink()

    result = fixture.pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=rel,
    )

    assert result["inspection_status"] == "blocked"
    assert result["blocker_code"] == "CANDIDATE_INTEGRITY_BLOCKER"


def test_p18_9_2_review_candidate_inspection_workspace_escape_fails_closed(
    projection_home,
    monkeypatch,
) -> None:
    fixture = _p18_9_2_prepared_review_candidate_fixture(
        projection_home,
        monkeypatch,
        pid=6830,
    )
    manifest_path = fixture.candidate_fixture["manifest_path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["workspace_root"] = str(projection_home / "outside-candidate-workspace")
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    result = fixture.pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=fixture.candidate_paths[0],
    )

    assert result["inspection_status"] == "blocked"
    assert result["blocker_code"] == "CANDIDATE_INTEGRITY_BLOCKER"
    assert result["Git_mutation"] is False


def test_p18_9_2_review_candidate_inspection_binary_candidate_is_metadata_only(
    projection_home,
    monkeypatch,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    retry = _start_recovered_p18_9_2_retry_for_test(state, monkeypatch, pid=6829)
    candidate_fixture = _write_p18_9_2_terminal_candidate_fixture(
        state.pr,
        projection_home,
        Path(retry["workspace_path"]),
    )
    binary_rel = (
        "2_products/pepper-agent/web/src/agent-platform/runtime-overview/"
        "overview-artifact.bin"
    )
    source_binary = candidate_fixture["source_root"] / binary_rel
    candidate_binary = candidate_fixture["workspace_root"] / binary_rel
    source_binary.parent.mkdir(parents=True, exist_ok=True)
    candidate_binary.parent.mkdir(parents=True, exist_ok=True)
    source_binary.write_bytes(b"\x00source\x01")
    candidate_binary.write_bytes(b"\x00candidate\x02")
    _finish_projected_run_as_review_required_terminal(
        state.kanban_db,
        state.projected,
        retry["kanban_run_id"],
        summary=(
            "review-required: P18.9.2 Control Center Overview implementation is ready "
            "for human/code review; governed frontend validation passed."
        ),
    )
    review = state.pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert review["kanban_completion_result"]["candidate_changes_reference"][
        "files_changed"
    ] == 4

    content = state.pr.inspect_current_ticket_review_candidate(
        operation="content",
        candidate_path=binary_rel,
    )
    diff = state.pr.inspect_current_ticket_review_candidate(
        operation="diff",
        candidate_path=binary_rel,
    )

    for result in (content, diff):
        assert result["inspection_status"] == "metadata_only"
        assert result["candidate_path"] == binary_rel
        assert result["candidate_text_supported"] is False
        assert result["Git_mutation"] is False
    assert content["content"] is None
    assert diff["unified_diff"] is None


@pytest.mark.parametrize(
    ("decision", "expected_status", "expected_review_state"),
    [
        ("accept", "review_accepted_pending_human_git_handoff", "accepted"),
        ("reject", "review_rejected_no_execution", "rejected"),
        (
            "changes_requested",
            "review_changes_requested_revision_pending_continuation",
            "correction_required",
        ),
    ],
)
def test_p18_9_2_second_round_review_decisions_target_fresh_run(
    projection_home,
    monkeypatch,
    decision,
    expected_status,
    expected_review_state,
) -> None:
    fixture = _p18_9_2_two_round_changes_requested_fixture(
        projection_home,
        monkeypatch,
        first_pid=6816,
        revision_pid=6817,
    )
    pr = fixture.pr
    prepared_14 = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )

    reviewed = pr.submit_current_ticket_review_decision(
        decision=decision,
        feedback=f"Human {decision.replace('_', ' ')} for the P18.9.2 fresh revision.",
        reviewed_run_id=fixture.started_14["kanban_run_id"],
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="SUBMIT_P18_9_2_REVIEW_DECISION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("second-round decision must not spawn"),
    )

    assert reviewed["review_decision"] == decision
    assert reviewed["reviewed_run_id"] == fixture.started_14["kanban_run_id"]
    assert reviewed["reviewed_run_id"] != fixture.run_13["kanban_run_id"]
    assert reviewed["review_source_authority_kind"] == "review_prepare"
    assert reviewed["review_prepare_action_SHA256"] == prepared_14[
        "review_prepare_action_SHA256"
    ]
    assert reviewed["review_package_SHA256"] == prepared_14["review_package_SHA256"]
    assert reviewed["workflow_status"] == expected_status
    assert reviewed["review_state"] == expected_review_state
    assert reviewed["dispatch_performed"] is False
    assert reviewed["execution_started"] is False
    assert reviewed["Git_mutation"] is False
    if decision == "changes_requested":
        revision_request = reviewed["review_revision_request_reference"]
        assert revision_request["prior_terminal_run_id"] == fixture.started_14[
            "kanban_run_id"
        ]
        assert revision_request["fresh_execution_request_SHA256"] != fixture.revision_request[
            "fresh_execution_request_SHA256"
        ]
        assert reviewed["next_action"]["id"] == "CONTINUE_P18_9_2_GOVERNED_AUTONOMY"
    else:
        assert reviewed["review_revision_request_reference"] is None


def _tamper_p18_9_2_review_prepare_record(pr, tamper_kind: str) -> None:
    path = pr.review_prepare_record_path_for_ticket("P18.9.2")
    record = json.loads(path.read_text(encoding="utf-8"))
    recompute_digest = True
    if tamper_kind == "digest":
        record["review_prepare_action_SHA256"] = "0" * 64
        recompute_digest = False
    elif tamper_kind == "ticket":
        record["ticket_id"] = "P18.9.0"
    elif tamper_kind == "work_packet_id":
        record["work_packet_id"] = "WP-DEFAULT-T_B6BAF825"
    elif tamper_kind == "work_packet_sha":
        record["work_packet_SHA256"] = "1" * 64
    elif tamper_kind == "projection_sha":
        record["projection_SHA256"] = "2" * 64
    elif tamper_kind == "run_id":
        record["successful_run_id"] = int(record["successful_run_id"]) + 100
    elif tamper_kind == "completion_result":
        record["kanban_completion_result_SHA256"] = "3" * 64
    elif tamper_kind == "review_package":
        record["review_package_SHA256"] = "6" * 64
    elif tamper_kind == "acceptance_contract":
        record["acceptance_contract_SHA256"] = "4" * 64
    elif tamper_kind == "criteria_revision":
        record["criteria_revision_SHA256"] = "5" * 64
    elif tamper_kind == "candidate_materialization":
        record["kanban_completion_result"]["candidate_changes_reference"]["files_changed"] = 99
    else:  # pragma: no cover - guards future parametrization edits
        raise AssertionError(f"unknown tamper kind: {tamper_kind}")
    if recompute_digest:
        record["review_prepare_action_SHA256"] = pr._review_prepare_record_digest(record)
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_p18_9_2_dependency_materialization_failure_remains_recovery_required(
    projection_home,
    monkeypatch,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    workflow = state.pr.build_workflow_control_snapshot()

    assert workflow["workflow_status"] == "retry_pending"
    assert workflow["recovery_state"] == "retry_pending"
    assert workflow["next_action"]["id"] == "START_P18_9_2_RETRY_REQUIRES_HUMAN_AUTHORIZATION"
    assert workflow.get("terminal_outcome_class") != "validated_review_required"
    assert not state.pr.review_prepare_record_path_for_ticket("P18.9.2").exists()


@pytest.mark.parametrize(
    ("summary", "block_kind", "write_candidate", "run_error"),
    (
        (
            "review-required: P18.9.2 is ready for human/code review.",
            "needs_input",
            True,
            None,
        ),
        (
            "review-required: validation passed, but tests failed during final check.",
            "needs_input",
            True,
            None,
        ),
        (
            "review-required: P18.9.2 implementation is ready; validation passed.",
            "capability",
            True,
            None,
        ),
        (
            "review-required: P18.9.2 implementation is ready; validation passed.",
            "needs_input",
            False,
            None,
        ),
        (
            "review-required: P18.9.2 implementation is ready; validation passed.",
            "needs_input",
            True,
            "worker failed after reporting review-required",
        ),
    ),
)
def test_p18_9_2_review_required_terminal_fails_closed_without_review_authority(
    projection_home,
    monkeypatch,
    summary,
    block_kind,
    write_candidate,
    run_error,
) -> None:
    state = _recovered_p18_9_2_dependency_failure_fixture(projection_home, monkeypatch)
    pr = state.pr
    retry = _start_recovered_p18_9_2_retry_for_test(state, monkeypatch, pid=6793)
    if write_candidate:
        _write_p18_9_2_terminal_candidate_fixture(
            pr,
            projection_home,
            Path(retry["workspace_path"]),
        )
    _finish_projected_run_as_review_required_terminal(
        state.kanban_db,
        state.projected,
        retry["kanban_run_id"],
        summary=summary,
        block_kind=block_kind,
        error=run_error,
    )

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] == "P18.9.2"
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["workflow_state"] == "P18.9.2-RETRY-EXECUTION-FAILED-RECOVERY-REQUIRED"
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_2_EXECUTION"
    assert workflow.get("terminal_outcome_class") != "validated_review_required"
    assert workflow.get("validated_candidate_review_required") is not True
    assert workflow.get("dispatch_performed", False) is False
    assert workflow["execution_started"] is False
    assert workflow["worker_execution"] is False
    assert workflow["Git_mutation"] is False

    blocked_review = pr.prepare_current_ticket_review(
        project_id="PEPPER",
        ticket_id="P18.9.2",
        next_action_id="PREPARE_P18_9_2_REVIEW",
    )
    assert blocked_review["review_prepare_status"] == "blocked"
    assert blocked_review["review_preparation_recorded"] is False
    assert blocked_review["dispatch_performed"] is False
    assert blocked_review["Git_mutation"] is False
    assert not pr.review_prepare_record_path_for_ticket("P18.9.2").exists()


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


def test_current_ticket_dependency_materialization_gap_blocks_before_worker_spawn(
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
    monkeypatch.setattr(
        pr,
        "_preflight_pepper_governed_worker_credentials",
        lambda _projection_record, *, enabled=True: _ready_worker_credential_probe(),
    )
    monkeypatch.setattr(
        pr,
        "_projection_requires_scratch_source_materialization",
        lambda _projection_record: True,
    )

    def dependency_gap(_projection, _workspace, *, env_overlay=None, source_root=None):
        _ = env_overlay, source_root
        raise pr.ProductRuntimeDependencyGap(
            pr.DEPENDENCY_MATERIALIZATION_FAILED,
            "dependency source contains an unsafe symlinked file",
        )

    monkeypatch.setattr(pr, "_materialize_pepper_governed_scratch_source", dependency_gap)

    result = pr.start_current_ticket_execution(
        human_authorization_text="Start P18.9.0 execution now",
        project_id="PEPPER",
        ticket_id="P18.9.0",
        next_action_id="START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("dependency gap must block before spawn"),
    )
    workflow = pr.build_workflow_control_snapshot()

    assert result["start_status"] == "blocked"
    assert result["blocker_code"] == pr.IMPLEMENTATION_SCRATCH_VALIDATION_DEPENDENCY_GAP
    assert result["blocker_detail"].startswith(
        f"{pr.DEPENDENCY_MATERIALIZATION_FAILED}:"
    )
    assert result["dispatch_performed"] is True
    assert result["execution_started"] is False
    assert result["worker_execution"] is False
    assert result["worker_process_started"] is False
    assert result["worker_pid_recorded"] is False
    assert result["Git_mutation"] is False
    assert result["next_action"]["id"] == "START_P18_9_0_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION"
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["workflow_state"] == "P18.9.0-EXECUTION-FAILED-RECOVERY-REQUIRED"
    assert workflow["active_execution_count"] == 0
    assert workflow["worker_execution"] is False
    assert workflow["Kanban_dispatch"] is True
    assert workflow["Git_mutation"] is False
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["next_action"]["id"] == "RECOVER_P18_9_0_EXECUTION"

    record = pr.load_p18_9_0_execution_start_record()
    assert record is not None
    assert record["execution_started"] is False
    assert record["worker_execution"] is False
    assert record["worker_process_started"] is False
    assert record["Git_mutation"] is False
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "blocked"
        assert task.worker_pid is None
        assert task.current_run_id is None
        assert task.consecutive_failures == 1
        assert task.last_failure_error
        assert pr.DEPENDENCY_MATERIALIZATION_FAILED in task.last_failure_error
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


def test_current_p18_9_1_governed_autonomy_activation_is_status_only(
    projection_home,
    monkeypatch,
    tmp_path,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db
    import tools.pepper_workflow_tools as pepper_tools

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    failed = pr.build_workflow_control_snapshot()
    assert failed["workflow_status"] == "execution_failed"
    assert failed["recovery_state"] == "recovery_required"
    assert failed["next_action"]["id"] == "RECOVER_P18_9_1_EXECUTION"
    assert failed["blocker_count"] == 1

    not_activated = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert not_activated["governed_autonomy_activation_recorded"] is False
    assert not_activated["governed_autonomy_status"] == "not_activated"
    assert not_activated["live_lineage_activation_authorized"] is False
    assert not_activated["dispatch_performed"] is False
    assert not_activated["runs"][-1]["id"] == run_4

    activation_text = (
        "Activate 01AH governed autonomy status for P18.9.1 without live lineage activation."
    )
    activation = json.loads(pepper_tools._activate_current_ticket_governed_autonomy({
        "human_request_text": activation_text,
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
        "next_action_id": "RECOVER_P18_9_1_EXECUTION",
    }))

    assert activation["success"] is True
    assert activation["governed_autonomy_status"] == "activation_recorded_live_lineage_blocked"
    assert activation["governed_autonomy_activation_recorded"] is True
    assert activation["governed_autonomy_activation_origin"] == "current_human_activation"
    assert activation["legacy_activation_compatibility_applied"] is False
    assert activation["historical_activation_record_preserved"] is False
    assert activation["effective_live_lineage_activation_authorized"] is True
    assert activation["additional_human_activation_required"] is False
    assert activation["same_authority_subset_validated"] is True
    assert activation["authority_derivation_source"] == "server_side_current_ticket_projection_and_kanban_run"
    assert activation["01AH_envelope_lifecycle_classification"] == "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE"
    assert activation["backend_derived_live_authority_SHA256"] == activation[
        "governed_autonomy_envelope_SHA256"
    ]
    assert activation["same_authority_delegation_status"] == (
        "canonical_hermes_delegate_task_available_with_parent_agent"
    )
    assert activation["same_authority_delegation_authorized"] is True
    assert activation["A2A_dispatch_performed"] is False
    assert activation["live_lineage_activation_authorized"] is True
    assert activation["live_lineage_activation_status"] == "active_authority_ready_for_continuation"
    assert activation["lineage_dispatch_performed"] is False
    assert activation["dispatch_performed"] is False
    assert activation["execution_started"] is False
    assert activation["worker_execution"] is False
    assert activation["Kanban_dispatch"] is False
    assert activation["Git_mutation"] is False
    assert activation["auto_retry"] is False
    assert activation["auto_rollback"] is False
    assert activation["kanban_run_count"] == 3
    assert activation["runs"][-1]["id"] == run_4

    record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert record is not None
    assert record["ticket_id"] == "P18.9.1"
    assert record["governed_autonomy_envelope_SHA256"] == activation[
        "governed_autonomy_envelope_SHA256"
    ]
    assert record["backend_derived_live_authority_SHA256"] == activation[
        "governed_autonomy_envelope_SHA256"
    ]
    assert record["capability_gap_SHA256"] is None
    assert record["continuation_lineage_SHA256"] is None
    assert "governed_autonomy_envelope" not in record
    assert "capability_gap" not in record
    assert "continuation_lineage" not in record
    authority_reference = record["governed_autonomy_envelope_reference"]
    assert authority_reference["authority_kind"] == "backend_derived_live_authority"
    assert authority_reference["single_agent_result_SHA256"] is None
    assert authority_reference["allocation_SHA256"] is None
    assert authority_reference["profile_SHA256"] is None
    assert authority_reference["source_run_id"] == run_4
    assert authority_reference["active_execution_count"] == 0
    assert record["capability_gap_reference"] is None
    assert record["continuation_lineage_reference"] is None
    assert pr.governed_autonomy_activation_record_path_for_ticket("P18.9.1").exists()
    assert not pr.governed_autonomy_activation_record_path_for_ticket("P18.9.0").exists()

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "execution_failed"
    assert workflow["recovery_state"] == "recovery_required"
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow["blocker_count"] == 1
    assert workflow["governed_autonomy_status"] == "activation_recorded_live_lineage_blocked"
    assert workflow["governed_autonomy"]["activation_action_SHA256"] == activation[
        "activation_action_SHA256"
    ]
    assert workflow["governed_autonomy"]["legacy_activation_compatibility_applied"] is False
    assert workflow["governed_autonomy"]["same_authority_delegation_status"] == (
        "canonical_hermes_delegate_task_available_with_parent_agent"
    )
    assert workflow["A2A_dispatch_performed"] is False

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["idempotent_replay"] is True
    assert status["legacy_activation_compatibility_applied"] is False
    assert status["activation_action_SHA256"] == activation["activation_action_SHA256"]
    assert status["runs"][-1]["id"] == run_4

    tool_status = json.loads(pepper_tools._get_governed_autonomy_status({
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
    }))
    assert tool_status["success"] is True
    assert tool_status["governed_autonomy_envelope_SHA256"] == activation[
        "governed_autonomy_envelope_SHA256"
    ]
    workflow_control = json.loads(pepper_tools._get_workflow_control({}))
    assert workflow_control["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow_control["governed_autonomy"]["same_authority_delegation_authorized"] is True

    replay = pr.activate_current_ticket_governed_autonomy(
        human_request_text=activation_text,
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )
    assert replay["idempotent_replay"] is True
    assert replay["activation_action_SHA256"] == activation["activation_action_SHA256"]

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
    finally:
        conn.close()


def test_current_p18_9_1_legacy_governed_autonomy_activation_promotes_effective_authority(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    current_record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert current_record is not None
    legacy_record = _legacy_runtime_limited_governed_autonomy_activation_record(
        pr,
        current_record,
    )
    _write_governed_autonomy_activation_record_for_test(pr, legacy_record)
    path = pr.governed_autonomy_activation_record_path_for_ticket("P18.9.1")
    preserved_bytes = path.read_bytes()

    loaded = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert loaded is not None
    assert loaded["activation_action_SHA256"] == legacy_record["activation_action_SHA256"]
    assert loaded["live_lineage_activation_authorized"] is False
    assert loaded["live_lineage_activation_status"] == "blocked_requires_separate_authority"
    assert loaded["live_lineage_activation_blocker_code"] == "LIVE_LINEAGE_ACTIVATION_AUTHORITY_GAP"

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["activation_action_SHA256"] == legacy_record["activation_action_SHA256"]
    assert status["governed_autonomy_activation_origin"] == "legacy_compatible_human_activation"
    assert status["legacy_activation_compatibility_applied"] is True
    assert status["historical_activation_record_preserved"] is True
    assert status["historical_runtime_limitation_classification"] == (
        "LEGACY_ACTIVATION_RUNTIME_CAPABILITY_LIMITATION"
    )
    assert status["effective_live_lineage_activation_authorized"] is True
    assert status["live_lineage_activation_authorized"] is True
    assert status["historical_live_lineage_activation_authorized"] is False
    assert status["live_lineage_activation_status"] == "active_authority_ready_for_continuation"
    assert status["additional_human_activation_required"] is False
    assert status["authority_revalidated"] is True
    assert status["backend_derived_live_authority_SHA256"] == (
        legacy_record["backend_derived_live_authority_SHA256"]
    )
    assert status["runs"][-1]["id"] == run_4

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow["governed_autonomy_live_lineage_activation_authorized"] is True
    assert workflow["effective_live_lineage_activation_authorized"] is True
    assert workflow["governed_autonomy"]["legacy_activation_compatibility_applied"] is True
    assert workflow["governed_autonomy"]["historical_activation_record_preserved"] is True
    assert workflow["governed_autonomy"]["same_authority_delegation_authorized"] is True

    replay = pr.activate_current_ticket_governed_autonomy(
        human_request_text=legacy_record["human_request_text"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="RECOVER_P18_9_1_EXECUTION",
    )
    assert replay["idempotent_replay"] is True
    assert replay["activation_action_SHA256"] == legacy_record["activation_action_SHA256"]
    assert path.read_bytes() == preserved_bytes


def test_current_p18_9_1_direct_continuation_accepts_legacy_compatible_activation(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    current_record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert current_record is not None
    legacy_record = _legacy_runtime_limited_governed_autonomy_activation_record(
        pr,
        current_record,
    )
    _write_governed_autonomy_activation_record_for_test(pr, legacy_record)
    path = pr.governed_autonomy_activation_record_path_for_ticket("P18.9.1")
    preserved_bytes = path.read_bytes()

    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6707)
    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 from the legacy compatible human activation.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6707,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert result["runtime_decision"] == "DIRECT"
    assert result["governed_autonomy_runtime_status"] == "direct_execution_continuation_started"
    assert result["kanban_run_created"] is True
    assert result["kanban_run_id"] == run_4 + 1
    assert result["source_run_id"] == run_4
    assert result["process_continuation_count"] == 1
    assert result["legacy_human_recovery_retry_micro_gates_required"] is False
    assert path.read_bytes() == preserved_bytes


@pytest.mark.parametrize(
    "human_request_text",
    (
        "",
        "I do not authorize governed autonomy for P18.9.1.",
    ),
)
def test_current_p18_9_1_legacy_governed_autonomy_activation_rejects_invalid_human_authority(
    projection_home,
    monkeypatch,
    human_request_text,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    current_record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert current_record is not None
    legacy_record = _legacy_runtime_limited_governed_autonomy_activation_record(
        pr,
        current_record,
    )
    legacy_record["human_request_text"] = human_request_text
    legacy_record.pop("activation_action_SHA256")
    legacy_record["activation_action_SHA256"] = pr._governed_autonomy_activation_record_digest(
        legacy_record
    )
    _write_governed_autonomy_activation_record_for_test(pr, legacy_record)

    with pytest.raises(pr.ProductRuntimeConflict) as excinfo:
        pr.load_current_ticket_governed_autonomy_activation_record(
            projection_record=authority,
        )
    assert "human authorization is invalid" in str(excinfo.value)


def test_current_p18_9_1_legacy_governed_autonomy_activation_rejects_authority_sha_mismatch(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    current_record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert current_record is not None
    legacy_record = _legacy_runtime_limited_governed_autonomy_activation_record(
        pr,
        current_record,
    )
    legacy_record["backend_derived_live_authority_SHA256"] = "f" * 64
    legacy_record.pop("activation_action_SHA256")
    legacy_record["activation_action_SHA256"] = pr._governed_autonomy_activation_record_digest(
        legacy_record
    )
    _write_governed_autonomy_activation_record_for_test(pr, legacy_record)

    with pytest.raises(pr.ProductRuntimeAuthorityMismatch) as excinfo:
        pr.load_current_ticket_governed_autonomy_activation_record(
            projection_record=authority,
        )
    assert str(excinfo.value) == "CONTINUATION_AUTHORITY_MISMATCH"
    assert excinfo.value.diagnostics["reason"] == "legacy_activation_field_mismatch"


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("ticket_spec_SHA256", "b" * 64),
        ("work_packet_id", "WP-P18-9-1-R0001-mismatch"),
        ("work_packet_SHA256", "c" * 64),
        ("projection_SHA256", "d" * 64),
        ("kanban_task_id", "t_mismatch"),
        ("assignee_profile", "pepper-mismatched-profile"),
        ("selected_profile", "pepper-mismatched-profile"),
    ),
)
def test_current_p18_9_1_legacy_governed_autonomy_activation_rejects_scope_mismatch(
    projection_home,
    monkeypatch,
    field,
    value,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    current_record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert current_record is not None
    legacy_record = _legacy_runtime_limited_governed_autonomy_activation_record(
        pr,
        current_record,
    )
    legacy_record[field] = value
    legacy_record.pop("activation_action_SHA256")
    legacy_record["activation_action_SHA256"] = pr._governed_autonomy_activation_record_digest(
        legacy_record
    )
    _write_governed_autonomy_activation_record_for_test(pr, legacy_record)

    with pytest.raises((pr.ProductRuntimeConflict, pr.ProductRuntimeAuthorityMismatch)):
        pr.load_current_ticket_governed_autonomy_activation_record(
            projection_record=authority,
        )


def test_current_p18_9_1_governed_autonomy_direct_starts_same_authority_run_5(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    activation = _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)["activation"]
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6505)
    spawn_calls: list[dict] = []

    def spawn(task, workspace, board=None, env_overlay=None):
        spawn_calls.append({
            "task_id": task.id,
            "workspace": workspace,
            "board": board,
            "env_overlay": env_overlay,
        })
        return 6505

    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 under the active same-authority execution plane.",
        strategy="DIRECT",
        spawn_fn=spawn,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert len(spawn_calls) == 1
    assert spawn_calls[0]["task_id"] == projected["kanban_task_id"]
    assert spawn_calls[0]["board"] == projected["kanban_board_slug"]
    assert spawn_calls[0]["env_overlay"]["HERMES_AGENT_PLATFORM_WORKPACKET_ID"] == (
        projected["work_packet_id"]
    )
    assert result["runtime_decision"] == "DIRECT"
    assert result["governed_autonomy_runtime_status"] == "direct_execution_continuation_started"
    assert result["kanban_run_created"] is True
    assert result["kanban_run_id"] == run_4 + 1
    assert result["source_run_id"] == run_4
    assert result["historical_source_run_immutable"] is True
    assert result["process_continuation_count"] == 1
    assert result["dispatch_performed"] is True
    assert result["execution_started"] is True
    assert result["worker_execution"] is True
    assert result["worker_process_started"] is True
    assert result["Kanban_dispatch"] is True
    assert result["lineage_dispatch_performed"] is True
    assert result["legacy_human_recovery_retry_micro_gates_required"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["auto_rollback"] is False
    assert result["human_smoke_marker"] == pr.PEPPER_GOVERNED_AUTONOMY_READY_MARKER
    assert result["live_autonomous_continuation_marker"] == (
        pr.PEPPER_GOVERNED_AUTONOMY_LIVE_CONTINUATION_MARKER
    )
    assert result["current_invocation_side_effects"]["dispatch_performed"] is True
    request_ref = result["latest_decision_evidence"]["direct_execution_request_reference"]
    assert request_ref["governed_autonomy_continuation_reason"] == (
        pr.PEPPER_GOVERNED_AUTONOMY_INTERNAL_CONTINUATION_REASON
    )
    assert request_ref["dispatcher_primitive"] == (
        "kanban_db.unblock_task+kanban_db.claim_task+resolve_workspace+_default_spawn"
    )
    dispatch_ref = result["latest_decision_evidence"]["direct_execution_result_reference"]
    assert dispatch_ref["kanban_run_id"] == run_4 + 1
    assert dispatch_ref["source_materialization_reference"]["dependency_install_performed"] is False

    assert not pr.recovery_action_record_path_for_ticket("P18.9.1").exists()
    assert not pr.retry_start_record_path_for_ticket("P18.9.1").exists()
    assert not pr.p18_9_0_recovery_action_record_path().exists()

    record = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
        activation_record=pr.load_current_ticket_governed_autonomy_activation_record(
            projection_record=authority,
        ),
    )
    assert record is not None
    assert record["runtime_state_SHA256"] == result["runtime_state_SHA256"]
    assert record["activation_action_SHA256"] == activation["activation_action_SHA256"]
    assert record["provider_readiness_reference"]["provider"] == "openai-codex"
    assert record["provider_readiness_reference"]["model"] == "gpt-5.5"
    assert record["provider_readiness_reference"]["credential_profile_id"] == (
        "openai-codex.primary"
    )

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "running"
        assert task.current_run_id == run_4 + 1
        assert task.worker_pid == 6505
        body = json.loads(task.body or "{}")
        assert body["governed_autonomy_continuation_authorized"] is True
        assert body["governed_autonomy_activation_action_SHA256"] == activation[
            "activation_action_SHA256"
        ]
        assert body["governed_autonomy_source_run_id"] == run_4
        assert runs[-2].id == run_4
        assert runs[-2].status == "blocked"
        assert runs[-1].id == run_4 + 1
        assert runs[-1].status == "running"
        assert (Path(task.workspace_path) / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).is_file()
    finally:
        conn.close()

    replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Probe while the same governed run is already active.",
        strategy="DIRECT",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("active replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert replay["idempotent_replay"] is True
    assert replay["non_consuming_observation"] is True
    assert replay["process_continuation_count"] == 1
    assert replay["kanban_run_id"] == run_4 + 1

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "executing"
    assert workflow["active_execution_count"] == 1
    assert workflow["next_action"]["id"] == "MONITOR_P18_9_1_EXECUTION"
    assert workflow["governed_autonomy"]["kanban_run_created"] is True
    assert workflow["governed_autonomy"]["kanban_run_id"] == run_4 + 1
    assert workflow["governed_autonomy"]["live_autonomous_continuation_marker"] == (
        pr.PEPPER_GOVERNED_AUTONOMY_LIVE_CONTINUATION_MARKER
    )


def test_current_p18_9_1_governed_autonomy_reconciles_owned_terminal_validation_failure(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6515)
    started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 under governed autonomy for terminal reconciliation.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6515,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = started["kanban_run_id"]
    assert run_5 == run_4 + 1

    workspace = Path(started["workspace_path"])
    _write_p18_9_1_terminal_candidate_fixture(pr, projection_home, workspace)
    failure = (
        "workpacket_validation action list failed: TypeError: _handle() got an "
        "unexpected keyword argument 'session_id'"
    )
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary=failure,
    )

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["governed_autonomy_runtime_status"] == (
        "direct_execution_terminal_blocked_validation_repairable"
    )
    assert status["terminal_run_reconciled"] is True
    assert status["terminal_run_id"] == run_5
    assert status["validation_infrastructure_failure"] is True
    assert status["blocker_code"] == "GOVERNED_AUTONOMY_VALIDATION_INFRASTRUCTURE_REPAIRABLE"
    assert status["source_materialization_reference"]["dependency_install_performed"] is False
    candidate_paths = {
        item["path"]
        for item in status["candidate_changes_reference"]["files"]
    }
    assert (
        "2_products/pepper-agent/web/src/agent-platform/shell/navigation.ts"
        in candidate_paths
    )
    assert (
        "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt"
        in candidate_paths
    )

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "governed_autonomy_validation_repairable"
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow["governed_autonomy"]["terminal_run_reconciled"] is True
    assert workflow["governed_autonomy"]["validation_infrastructure_failure"] is True

    replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Observe terminal governed run without creating another run.",
        strategy="DIRECT",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("terminal replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert replay["idempotent_replay"] is True
    assert replay["non_consuming_observation"] is True
    assert replay["observation_status"] == "governed_autonomy_execution_terminal_reconciled"
    assert replay["terminal_run_id"] == run_5

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_5
        assert all(run.id != run_5 + 1 for run in runs)
    finally:
        conn.close()

    run_6 = _claim_next_projected_run(kanban_db, projected, pid=6626)
    assert run_6 == run_5 + 1
    _block_projected_run(
        kanban_db,
        projected,
        run_6,
        reason="synthetic newer blocked run must supersede terminal replay authority",
        kind="transient",
    )

    status_after_unowned = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status_after_unowned["authority_revalidated"] is False
    assert status_after_unowned["continuation_eligible"] is False
    assert status_after_unowned["effective_authority_diagnostics"]["reason"] == (
        "newer_unowned_source_run"
    )

    with pytest.raises(pr.ProductRuntimeAuthorityMismatch) as excinfo:
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Do not replay an owned terminal run after a newer unowned run.",
            strategy="DIRECT",
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("mismatch must not spawn"),
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )
    assert excinfo.value.diagnostics["reason"] == "newer_unowned_source_run"
    assert excinfo.value.diagnostics["owned_governed_run_id"] == run_5
    assert excinfo.value.diagnostics["current_source_run_id"] == run_6

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_6
        assert all(run.id != run_6 + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_terminal_validation_block_not_worker_start_failed(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6616)
    started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 under governed autonomy before terminal validation block.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6616,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = started["kanban_run_id"]
    assert run_5 == run_4 + 1

    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary=(
            "governed validation ran; shell tests passed but non-shell suites blocked "
            "because @hermes/shared and @nous-research/ui could not resolve"
        ),
    )

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["governed_autonomy_runtime_status"] == "direct_execution_terminal_blocked"
    assert status["terminal_run_reconciled"] is True
    assert status["terminal_run_id"] == run_5
    assert status["validation_infrastructure_failure"] is False

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "governed_autonomy_validation_blocked"
    assert workflow["validation_state"] == "governed_autonomy_validation_blocked"
    assert workflow["execution_state"] == "no_active_executions"
    assert "worker start failed" not in workflow["next_action"]["label"]
    assert "terminal validation blockage" in workflow["next_action"]["label"]
    assert workflow["governed_autonomy"]["terminal_run_id"] == run_5


def test_current_p18_9_1_governed_autonomy_terminal_validated_candidate_routes_to_handoff(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    live_pids = {6815, 6816, 6817}
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) in live_pids)

    run_5_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 before synthetic run 7 validated candidate.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6815,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = run_5_started["kanban_run_id"]
    assert run_5 == run_4 + 1
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary="synthetic terminal run 5 requires a fresh governed attempt",
    )

    run_6_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Start synthetic fresh P18.9.1 governed run 6.",
        strategy="DIRECT",
        fresh_execution_request_text="Launch synthetic fresh governed P18.9.1 run 6.",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6816,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_6 = run_6_started["kanban_run_id"]
    assert run_6 == run_5 + 1
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_6,
        status="blocked",
        outcome="blocked",
        summary="synthetic terminal run 6 requires a final fresh governed attempt",
    )

    run_7_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Start synthetic fresh P18.9.1 governed run 7.",
        strategy="DIRECT",
        fresh_execution_request_text="Launch synthetic fresh governed P18.9.1 run 7.",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6817,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_7 = run_7_started["kanban_run_id"]
    assert run_7 == run_6 + 1
    run_7_workspace = Path(run_7_started["workspace_path"])
    _write_p18_9_1_terminal_candidate_fixture(pr, projection_home, run_7_workspace)
    run_7_manifest = (
        run_7_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes()
    run_7_summary = (
        "worker process started; candidate produced; workpacket_validation invoked; "
        "validation infrastructure failure = false; product validation failure = false; "
        "governed V2 validation passed; 7 files, 123 tests passed; "
        "Git mutation authority = false; terminal reason: review-required because "
        "canonical repository merge is human-only."
    )
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_7,
        status="blocked",
        outcome="blocked",
        summary=run_7_summary,
    )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs_before = kanban_db.list_runs(conn, projected["kanban_task_id"])
        run_7_before = next(run for run in runs_before if run.id == run_7)
        run_7_snapshot = {
            "id": run_7_before.id,
            "status": run_7_before.status,
            "outcome": run_7_before.outcome,
            "summary": run_7_before.summary,
            "error": run_7_before.error,
            "ended_at": run_7_before.ended_at,
        }
    finally:
        conn.close()

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["governed_autonomy_runtime_status"] == (
        "direct_execution_terminal_validated_review_required"
    )
    assert status["terminal_run_reconciled"] is True
    assert status["terminal_run_id"] == run_7
    assert status["validation_infrastructure_failure"] is False
    assert status["validated_candidate_review_required"] is True
    assert status["candidate_changes_available"] is True
    assert status["candidate_changes_reference"]["files_changed"] == 4
    assert status["candidate_changes_reference"]["modified_file_count"] == 3
    assert status["candidate_changes_reference"]["created_file_count"] == 1
    assert status["validation_observation_reference"]["validation_passed"] is True
    assert status["blocker_code"] is None
    assert status["next_action"]["id"] == (
        pr.governed_ticket_lifecycle_action_ids("P18.9.1")["review_prepare"]
    )
    assert status["Git_mutation"] is False

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["readiness"] == "governed_autonomy_validated_candidate_review_ready"
    assert workflow["workflow_state"] == (
        "P18.9.1-GOVERNED-AUTONOMY-AWAITING-HUMAN-GIT-HANDOFF"
    )
    assert workflow["workflow_status"] == "execution_completed"
    assert workflow["validation_state"] == "execution_completed_pending_validation"
    assert workflow["review_state"] == "ready_for_review_validation"
    assert workflow["recovery_state"] == "not_required"
    assert workflow["governed_workflow_state"] == "awaiting_human_git_handoff"
    assert workflow["git_handoff_required"] is True
    assert workflow["git_handoff_state"] == "human_git_authority_preserved"
    assert workflow["next_action"]["id"] == status["next_action"]["id"]
    assert workflow["next_action"]["required_human_action"] == (
        "review_validation_preparation_and_human_git_handoff"
    )
    assert "human review" in workflow["next_action"]["label"]
    assert "Git handoff" in workflow["next_action"]["label"]
    assert workflow["governed_autonomy"]["terminal_run_id"] == run_7
    assert workflow["governed_autonomy"]["validated_candidate_review_required"] is True
    assert workflow["governed_autonomy"]["validation_infrastructure_failure"] is False

    replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Reconcile synthetic run 7 without creating run 8.",
        strategy="DIRECT",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("run 7 replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert replay["idempotent_replay"] is True
    assert replay["terminal_run_id"] == run_7
    assert replay["validated_candidate_review_required"] is True
    assert replay["next_action"]["id"] == status["next_action"]["id"]
    assert replay["Git_mutation"] is False

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs_after = kanban_db.list_runs(conn, projected["kanban_task_id"])
        run_7_after = next(run for run in runs_after if run.id == run_7)
        assert [run.id for run in runs_after] == [run.id for run in runs_before]
        assert runs_after[-1].id == run_7
        assert all(run.id != run_7 + 1 for run in runs_after)
        assert {
            "id": run_7_after.id,
            "status": run_7_after.status,
            "outcome": run_7_after.outcome,
            "summary": run_7_after.summary,
            "error": run_7_after.error,
            "ended_at": run_7_after.ended_at,
        } == run_7_snapshot
    finally:
        conn.close()
    assert (
        run_7_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes() == run_7_manifest


def test_current_p18_9_1_governed_autonomy_terminal_product_validation_failure_stays_blocked(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6825)
    started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 before genuine product validation failure.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6825,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = started["kanban_run_id"]
    assert run_5 == run_4 + 1
    _write_p18_9_1_terminal_candidate_fixture(
        pr,
        projection_home,
        Path(started["workspace_path"]),
    )
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary=(
            "candidate produced; workpacket_validation invoked; validation infrastructure "
            "failure = false; product validation failure = true; validation failed; "
            "tests failed; review-required text alone must not bypass failure handling"
        ),
    )

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["governed_autonomy_runtime_status"] == "direct_execution_terminal_blocked"
    assert status["terminal_run_reconciled"] is True
    assert status["terminal_run_id"] == run_5
    assert status["validation_infrastructure_failure"] is False
    assert status["candidate_changes_available"] is True
    assert status["validated_candidate_review_required"] is False
    assert status["validation_observation_reference"]["validation_passed"] is False
    assert status["blocker_code"] == "GOVERNED_AUTONOMY_TERMINAL_RUN_BLOCKED"

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "governed_autonomy_validation_blocked"
    assert workflow["validation_state"] == "governed_autonomy_validation_blocked"
    assert workflow["review_state"] == "candidate_available_validation_blocked"
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow["governed_autonomy"]["validated_candidate_review_required"] is False


def test_current_p18_9_1_review_accept_routes_to_human_git_handoff_without_execution(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )
    fixture = _start_p18_9_1_validated_review_ready_run_7(
        pr,
        projection_home,
        projected,
        monkeypatch,
    )

    accepted = pr.submit_current_ticket_review_decision(
        decision="accept",
        feedback="Human accepts the validated P18.9.1 run 7 candidate for human Git handoff.",
        reviewed_run_id=fixture["run_7"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert accepted["review_decision"] == "accept"
    assert accepted["review_validation_decision"] == "accept"
    assert accepted["review_state"] == "accepted"
    assert accepted["governed_workflow_state"] == "awaiting_human_git_handoff"
    assert accepted["dispatch_performed"] is False
    assert accepted["execution_started"] is False
    assert accepted["Git_mutation"] is False

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "review_accepted_pending_human_git_handoff"
    assert workflow["review_state"] == "accepted"
    assert workflow["git_handoff_required"] is True
    assert workflow["git_handoff_state"] == "human_git_authority_preserved"
    assert workflow["next_action"]["id"] == "PREPARE_P18_9_1_HUMAN_GIT_HANDOFF"

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == fixture["run_7"]
        assert all(run.id != fixture["run_7"] + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_human_git_handoff_completion_closes_ticket_and_exposes_successor(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority, fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
    )
    from hermes_cli import kanban_db

    review_record_path = pr.review_decision_record_path_for_ticket("P18.9.1")
    review_record_before = review_record_path.read_bytes()
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        run_7_before = next(
            run
            for run in kanban_db.list_runs(conn, projected["kanban_task_id"])
            if run.id == fixture["run_7"]
        )
        run_7_snapshot = {
            "id": run_7_before.id,
            "status": run_7_before.status,
            "outcome": run_7_before.outcome,
            "summary": run_7_before.summary,
            "error": run_7_before.error,
            "ended_at": run_7_before.ended_at,
        }
        run_ids_before = [run.id for run in kanban_db.list_runs(conn, projected["kanban_task_id"])]
    finally:
        conn.close()
    expected_successor = bridge.resolve_canonical_next_ticket({
        "project_id": "PEPPER",
        "project_name": "Pepper",
        "macroproject_id": authority["macroproject_id"],
        "macroproject_title": "Pepper Product Personalization",
        "current_ticket_id": None,
        "closed_predecessor_ticket_id": "P18.9.1",
        "workflow_status": "completed",
        "workflow_state": "P18.9.1-COMPLETED",
    }).asdict()

    completed = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(accepted),
    )

    assert completed["handoff_completion_recorded"] is True
    assert completed["idempotent_replay"] is False
    assert completed["human_git_handoff_state"] == "completed"
    assert completed["review_state"] == "accepted"
    assert completed["validation_state"] == "review_accepted"
    assert completed["recovery_state"] == "not_required"
    assert completed["execution_state"] == "no_active_executions"
    assert completed["workflow_status"] == "completed"
    assert completed["governed_workflow_state"] == "completed"
    assert completed["ordered_commit_SHAs"] == list(_P18_9_1_HANDOFF_COMMITS)
    assert completed["ordered_commit_count"] == 2
    assert completed["final_commit_SHA"] == _P18_9_1_HANDOFF_COMMITS[-1]
    assert completed["branch"] == _P18_9_1_HANDOFF_BRANCH
    assert completed["approved_committed_paths"] == list(_P18_9_1_HANDOFF_APPROVED_PATHS)
    assert completed["excluded_paths"] == list(_P18_9_1_HANDOFF_EXCLUDED_PATHS)
    assert completed["ticket_closed"] is True
    assert completed["closed_predecessor_ticket_id"] == "P18.9.1"
    assert completed["next_ticket_ready"] is True
    assert completed["next_ticket_id"] == "P18.9.2"
    assert completed["next_ticket_title"] == "Control Center Overview"
    assert completed["next_ticket_id"] == expected_successor["ticket_id"]
    assert completed["next_ticket_authority"]["ticket_id"] == expected_successor["ticket_id"]
    assert completed["next_ticket_authority"]["ticket_title"] == "Control Center Overview"
    assert completed["next_ticket_authority"]["roadmap_authority_path"] == (
        bridge.CANONICAL_IMPLEMENTATION_ROADMAP_AUTHORITY_PATH
    )
    assert completed["next_action"]["id"] == expected_successor["next_action_id"]
    assert completed["generic_ticket_completion_path_reused"] is True
    assert completed["P17_human_git_handoff_authority_reused"] is True
    assert completed["P18_governed_transition_reused"] is True
    assert completed["dispatch_performed"] is False
    assert completed["execution_started"] is False
    assert completed["worker_execution"] is False
    assert completed["Kanban_dispatch"] is False
    assert completed["Git_commands_executed"] == 0
    assert completed["Git_mutation"] is False
    assert completed["Docker_commands_executed"] == 0
    assert completed["Graphify_commands_executed"] == 0
    assert not {
        "commit_file_set",
        "upstream_containment",
        "commit_ancestry",
    } & {item["id"] for item in completed["verification_evidence"]}
    assert {item["id"] for item in completed["machine_verification_evidence"]} == {
        "current_branch",
        "final_commit_head",
        "working_tree_status",
    }
    final_head_evidence = _evidence_item(completed, "final_commit_head")
    assert final_head_evidence["classification"] == "MACHINE_VERIFIED"
    assert final_head_evidence["relationship"] == "exact_current_head"
    assert final_head_evidence["expected"] == _P18_9_1_HANDOFF_COMMITS[-1]
    assert final_head_evidence["observed"] == _P18_9_1_HANDOFF_COMMITS[-1]

    record = pr.load_current_ticket_human_git_handoff_completion_record(
        projection_record=authority,
    )
    assert record is not None
    assert record["completion_record_SHA256"] == completed["completion_record_SHA256"]
    assert record["completion_order_evidence"]["multi_commit_handoff"] is True
    assert pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1").exists()
    assert review_record_path.read_bytes() == review_record_before

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["current_ticket_id"] is None
    assert workflow["closed_predecessor_ticket_id"] == "P18.9.1"
    assert workflow["workflow_status"] == "completed"
    assert workflow["governed_workflow_state"] == "completed"
    assert workflow["human_git_handoff_state"] == "completed"
    assert workflow["next_ticket_id"] == expected_successor["ticket_id"]
    assert workflow["next_ticket_title"] == "Control Center Overview"
    assert workflow["next_action"]["id"] == expected_successor["next_action_id"]
    assert workflow["Git_mutation"] is False

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs_after = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert [run.id for run in runs_after] == run_ids_before
        run_7_after = next(run for run in runs_after if run.id == fixture["run_7"])
        assert {
            "id": run_7_after.id,
            "status": run_7_after.status,
            "outcome": run_7_after.outcome,
            "summary": run_7_after.summary,
            "error": run_7_after.error,
            "ended_at": run_7_after.ended_at,
        } == run_7_snapshot
    finally:
        conn.close()

    replay = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            git_snapshot={"available": False},
            git_snapshot_fn=lambda: pytest.fail("handoff completion replay must not inspect Git"),
        ),
    )
    assert replay["idempotent_replay"] is True
    assert replay["completion_record_SHA256"] == completed["completion_record_SHA256"]

    with pytest.raises(pr.ProductRuntimeConflict):
        pr.complete_current_ticket_human_git_handoff(
            **_p18_9_1_handoff_completion_kwargs(
                accepted,
                commits=(_P18_9_1_HANDOFF_COMMITS[-1],),
                git_snapshot_fn=lambda: pytest.fail("conflicting replay must stop before Git inspection"),
            ),
        )


def test_current_p18_9_1_human_git_handoff_completion_accepts_historical_advanced_head(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, authority, _fixture, _accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
        pids=(7005, 7006, 7007),
    )
    review_record = pr.load_current_ticket_review_decision_record(
        projection_record=authority,
    )
    assert review_record is not None
    live_review = json.loads(json.dumps(review_record))
    live_review.update({
        "reviewed_run_id": _P18_9_1_LIVE_HANDOFF_RUN_ID,
        "reviewed_candidate_SHA256": _P18_9_1_LIVE_CANDIDATE_SHA256,
        "review_decision_SHA256": _P18_9_1_LIVE_REVIEW_DECISION_SHA256,
        "reviewed_candidate_reference": {
            "candidate_source": "live_p18_9_1_historical_handoff_fixture",
            "historical_reviewed_run_id": _P18_9_1_LIVE_HANDOFF_RUN_ID,
        },
    })
    monkeypatch.setattr(
        pr,
        "load_current_ticket_review_decision_record",
        lambda *, projection_record=None, allow_historical_mismatch=False: live_review,
    )
    advanced_head_snapshot = _p18_9_1_handoff_git_snapshot(
        branch=_P18_9_1_HANDOFF_BRANCH,
        head=_P18_9_1_POST_HANDOFF_CAPABILITY_HEAD,
    )

    completed = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            live_review,
            commits=_P18_9_1_LIVE_HANDOFF_COMMITS,
            git_snapshot=advanced_head_snapshot,
        ),
    )

    assert completed["handoff_completion_recorded"] is True
    assert "blocker_code" not in completed
    assert completed["human_git_handoff_state"] == "completed"
    assert completed["workflow_status"] == "completed"
    assert completed["governed_workflow_state"] == "completed"
    assert completed["reviewed_run_id"] == _P18_9_1_LIVE_HANDOFF_RUN_ID
    assert completed["reviewed_candidate_SHA256"] == _P18_9_1_LIVE_CANDIDATE_SHA256
    assert completed["review_decision_SHA256"] == _P18_9_1_LIVE_REVIEW_DECISION_SHA256
    assert completed["ordered_commit_SHAs"] == list(_P18_9_1_LIVE_HANDOFF_COMMITS)
    assert completed["final_commit_SHA"] == _P18_9_1_LIVE_HANDOFF_COMMITS[-1]
    final_head_evidence = _evidence_item(completed, "final_commit_head")
    assert final_head_evidence == {
        "id": "final_commit_head",
        "classification": "MACHINE_OBSERVED",
        "expected": _P18_9_1_LIVE_HANDOFF_COMMITS[-1],
        "observed": _P18_9_1_POST_HANDOFF_CAPABILITY_HEAD,
        "relationship": "current_head_differs_from_final_handoff_commit",
        "verification_scope": "current_head_only",
        "source": "pepper_repository_tools.git_read_only_inspection",
    }
    evidence_ids = {item["id"] for item in completed["verification_evidence"]}
    assert "HUMAN_GIT_HANDOFF_HEAD_MISMATCH" not in evidence_ids
    assert not {
        "commit_ancestry",
        "commit_file_set",
        "commit_reachability",
        "upstream_containment",
    } & evidence_ids
    assert {item["id"] for item in completed["machine_verification_evidence"]} == {
        "current_branch",
        "working_tree_status",
    }
    assert completed["Git_mutation"] is False
    assert completed["execution_started"] is False
    assert completed["Kanban_dispatch"] is False

    replay = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            live_review,
            commits=_P18_9_1_LIVE_HANDOFF_COMMITS,
            git_snapshot_fn=lambda: pytest.fail("historical replay must not inspect Git"),
        ),
    )
    assert replay["idempotent_replay"] is True
    assert replay["completion_identity_SHA256"] == completed["completion_identity_SHA256"]

    with pytest.raises(pr.ProductRuntimeConflict):
        pr.complete_current_ticket_human_git_handoff(
            **_p18_9_1_handoff_completion_kwargs(
                live_review,
                commits=(_P18_9_1_LIVE_HANDOFF_COMMITS[-1],),
                git_snapshot_fn=lambda: pytest.fail("historical conflict must stop before Git"),
            ),
        )


def test_current_p18_9_1_human_git_handoff_completion_wrong_branch_fails_closed(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, _authority, _fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
        pids=(7015, 7016, 7017),
    )

    blocked = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            git_snapshot=_p18_9_1_handoff_git_snapshot(
                branch="p18-wrong-branch",
                head=_P18_9_1_HANDOFF_COMMITS[-1],
            ),
        ),
    )

    assert blocked["handoff_completion_recorded"] is False
    assert blocked["blocker_code"] == "HUMAN_GIT_HANDOFF_BRANCH_MISMATCH"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Kanban_dispatch"] is False
    assert blocked["Git_mutation"] is False
    assert not pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1").exists()


def test_current_p18_9_1_human_git_handoff_completion_accepts_single_commit(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, authority, _fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
        pids=(6965, 6966, 6967),
    )

    completed = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            commits=(_P18_9_1_HANDOFF_COMMITS[-1],),
        ),
    )

    assert completed["handoff_completion_recorded"] is True
    assert completed["ordered_commit_SHAs"] == [_P18_9_1_HANDOFF_COMMITS[-1]]
    assert completed["ordered_commit_count"] == 1
    record = pr.load_current_ticket_human_git_handoff_completion_record(
        projection_record=authority,
    )
    assert record is not None
    assert record["completion_order_evidence"]["multi_commit_handoff"] is False


def test_current_p18_9_1_human_git_handoff_completion_requires_accepted_review(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    blocked = pr.complete_current_ticket_human_git_handoff(
        reviewed_run_id=11,
        reviewed_candidate_SHA256="a" * 64,
        review_decision_SHA256="b" * 64,
        commits=_P18_9_1_HANDOFF_COMMITS,
        branch=_P18_9_1_HANDOFF_BRANCH,
        push_attestation="Human pushed the handoff branch to origin.",
        approved_committed_paths=_P18_9_1_HANDOFF_APPROVED_PATHS,
        excluded_paths=_P18_9_1_HANDOFF_EXCLUDED_PATHS,
        validation_evidence=("Human validation completed.",),
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="PREPARE_P18_9_1_HUMAN_GIT_HANDOFF",
        git_snapshot_fn=lambda: pytest.fail("accepted-review gap must stop before Git inspection"),
    )

    assert blocked["handoff_completion_recorded"] is False
    assert blocked["blocker_code"] == "ACCEPTED_REVIEW_AUTHORITY_GAP"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_mutation"] is False
    assert not pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1").exists()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.list_runs(conn, projected["kanban_task_id"]) == []
    finally:
        conn.close()


def test_current_p18_9_1_human_git_handoff_completion_rejects_review_mismatches(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, _authority, _fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
        pids=(6975, 6976, 6977),
    )

    wrong_run = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            reviewed_run_id=int(accepted["reviewed_run_id"]) + 1,
            git_snapshot_fn=lambda: pytest.fail("run mismatch must stop before Git inspection"),
        ),
    )
    wrong_candidate = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            reviewed_candidate_SHA256="c" * 64,
            git_snapshot_fn=lambda: pytest.fail("candidate mismatch must stop before Git inspection"),
        ),
    )
    wrong_review = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            review_decision_SHA256="d" * 64,
            git_snapshot_fn=lambda: pytest.fail("review mismatch must stop before Git inspection"),
        ),
    )

    assert wrong_run["blocker_code"] == "HUMAN_GIT_HANDOFF_REVIEWED_RUN_MISMATCH"
    assert wrong_candidate["blocker_code"] == "HUMAN_GIT_HANDOFF_CANDIDATE_DIGEST_MISMATCH"
    assert wrong_review["blocker_code"] == "HUMAN_GIT_HANDOFF_REVIEW_DECISION_DIGEST_MISMATCH"
    assert not pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1").exists()


def test_current_p18_9_1_human_git_handoff_completion_requires_no_active_execution(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority, _fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
        pids=(6985, 6986, 6987),
    )

    from hermes_cli import kanban_db

    active_pid = 6988
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == active_pid)
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        assert kanban_db.unblock_task(conn, projected["kanban_task_id"])
        claimed = kanban_db.claim_task(
            conn,
            projected["kanban_task_id"],
            claimer="synthetic-active-handoff-blocker",
        )
        assert claimed is not None
        workspace = kanban_db.resolve_workspace(claimed, board=projected["kanban_board_slug"])
        kanban_db.set_workspace_path(conn, claimed.id, str(workspace))
        kanban_db._set_worker_pid(conn, claimed.id, active_pid)
    finally:
        conn.close()

    blocked = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            git_snapshot_fn=lambda: pytest.fail("active execution must stop before Git inspection"),
        ),
    )

    assert blocked["handoff_completion_recorded"] is False
    assert blocked["blocker_code"] == "EXECUTION_ALREADY_ACTIVE"
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_mutation"] is False
    assert not pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1").exists()


def test_current_p18_9_1_human_git_handoff_completion_exclusions_cannot_be_promoted(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, _authority, _fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
        pids=(6995, 6996, 6997),
    )

    promoted_lockfile = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            approved_paths=(
                *_P18_9_1_HANDOFF_APPROVED_PATHS,
                "2_products/pepper-agent/package-lock.json",
            ),
            git_snapshot_fn=lambda: pytest.fail("excluded lockfile promotion must stop before Git"),
        ),
    )
    promoted_report = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(
            accepted,
            approved_paths=(
                *_P18_9_1_HANDOFF_APPROVED_PATHS,
                "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt",
            ),
            git_snapshot_fn=lambda: pytest.fail("excluded report promotion must stop before Git"),
        ),
    )

    assert promoted_lockfile["blocker_code"] == "HUMAN_GIT_HANDOFF_EXCLUDED_PATH_PROMOTED"
    assert "2_products/pepper-agent/package-lock.json" in promoted_lockfile["referenced_paths"]
    assert promoted_report["blocker_code"] == "HUMAN_GIT_HANDOFF_EXCLUDED_PATH_PROMOTED"
    assert (
        "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt"
        in promoted_report["referenced_paths"]
    )
    assert not pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1").exists()


def test_p18_9_1_live_shape_human_git_handoff_completion_request_accepts_human_evidence(
    projection_home,
) -> None:
    from hermes_cli.agent_platform import product_runtime as pr

    request = pr.CurrentTicketHumanGitHandoffCompletionRequest(
        reviewed_run_id=_P18_9_1_LIVE_HANDOFF_RUN_ID,
        reviewed_candidate_SHA256=_P18_9_1_LIVE_CANDIDATE_SHA256,
        review_decision_SHA256=_P18_9_1_LIVE_REVIEW_DECISION_SHA256,
        commits=_P18_9_1_LIVE_HANDOFF_COMMITS,
        branch="p18-manual-to-hermes-workflow-migration",
        push_attestation="Human pushed origin/p18-manual-to-hermes-workflow-migration.",
        approved_committed_paths=(
            "web/src/agent-platform/shell/navigation.ts",
            "web/src/agent-platform/shell/shell.test.tsx",
        ),
        excluded_paths=(
            "package-lock.json",
            "P18.9.1-implementation-report.txt",
        ),
        validation_evidence=(
            "Human-attested current branch and HEAD match the pushed handoff evidence.",
        ),
        human_attested_evidence=(
            "Second commit contains exactly navigation.ts and shell.test.tsx.",
        ),
        project_id="PEPPER",
        ticket_id="P18.9.1",
        next_action_id="PREPARE_P18_9_1_HUMAN_GIT_HANDOFF",
    )

    assert request.reviewed_run_id == _P18_9_1_LIVE_HANDOFF_RUN_ID
    assert request.commits == _P18_9_1_LIVE_HANDOFF_COMMITS
    assert request.branch == "p18-manual-to-hermes-workflow-migration"


def test_current_p18_9_1_review_changes_requested_starts_same_authority_revision_segment(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )
    fixture = _start_p18_9_1_validated_review_ready_run_7(
        pr,
        projection_home,
        projected,
        monkeypatch,
        pids=(6925, 6926, 6927),
    )
    run_7_runtime = fixture["run_7_runtime_state"]
    assert run_7_runtime["process_continuation_count"] >= 3
    authority = _projection_authority_record(projected)
    activation = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert activation is not None
    budget_stop_request = pr.CurrentTicketGovernedAutonomyContinuationRequest(
        runtime_goal="Synthetic ordinary continuation observed exhausted prior segment budget.",
        strategy="STOP_FOR_HUMAN",
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    exhausted_previous_segment = pr._build_governed_autonomy_runtime_stop_record(
        request=budget_stop_request,
        projection=authority,
        activation=activation,
        previous=run_7_runtime,
        runtime_decision="STOP_FOR_HUMAN",
        blocker_code="GOVERNED_AUTONOMY_PROCESS_CONTINUATION_BUDGET_EXHAUSTED",
        blocker_detail="process continuation budget is exhausted",
        validation_failed=False,
        provider_readiness=_ready_executor_provider_payload(),
    )
    exhausted_previous_segment["process_continuation_count"] = exhausted_previous_segment[
        "budget_limits"
    ]["max_continuations"]
    counts = {
        key: exhausted_previous_segment[key]
        for key in (
            "process_continuation_count",
            "self_repair_count",
            "task_local_tool_candidate_count",
            "command_evaluation_count",
            "A2A_delegation_count",
            "validation_failure_count",
        )
    }
    exhausted_previous_segment["budget_remaining"] = (
        pr._governed_autonomy_runtime_budget_remaining(
            exhausted_previous_segment["budget_limits"],
            counts,
            no_progress_count=exhausted_previous_segment["no_progress_count"],
        )
    )
    exhausted_previous_segment["budget_exhausted"] = True
    exhausted_previous_segment.pop("runtime_state_SHA256", None)
    exhausted_previous_segment["runtime_state_SHA256"] = (
        pr._governed_autonomy_runtime_record_digest(exhausted_previous_segment)
    )
    pr._persist_governed_autonomy_runtime_state(exhausted_previous_segment)

    from hermes_cli import kanban_db

    revision_pid = 6928
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == revision_pid)
    run_7_manifest = (
        fixture["run_7_workspace"] / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes()
    changed = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback=_P18_9_1_REVIEW_CHANGES_FEEDBACK,
        reviewed_run_id=fixture["run_7"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: revision_pid,
    )

    assert changed["review_decision"] == "changes_requested"
    assert changed["review_validation_decision"] == "needs_correction"
    assert changed["review_state"] == "correction_required"
    assert changed["same_authority_revision"] is True
    assert changed["capability_not_authority"] is True
    assert changed["human_review_input_authority_expansion"] is False
    assert changed["revision_attempt_started"] is True
    assert changed["revision_kanban_run_id"] == fixture["run_7"] + 1
    revision_result = changed["revision_attempt_result"]
    assert revision_result["dispatch_performed"] is True
    assert revision_result["execution_started"] is True
    assert revision_result["process_continuation_count"] == 1
    assert revision_result["budget_exhausted"] is False
    assert revision_result["budget_segment_reference"]["budget_segment_origin"] == (
        "human_review_changes_requested"
    )
    revision_request = changed["review_revision_request_reference"]
    assert revision_request["fresh_execution_provenance"] == "human_review_changes_requested"
    assert revision_request["prior_terminal_run_id"] == fixture["run_7"]
    assert revision_request["revision_source_base"] == "current_canonical_source"
    assert revision_request["reviewed_candidate_copied_to_revision_base"] is False

    runtime_after = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
    )
    assert runtime_after is not None
    assert runtime_after["previous_runtime_state_SHA256"] == exhausted_previous_segment[
        "runtime_state_SHA256"
    ]
    assert runtime_after["process_continuation_count"] == 1
    assert runtime_after["budget_segment_previous_runtime_state_SHA256"] == (
        exhausted_previous_segment["runtime_state_SHA256"]
    )
    assert run_7_runtime["process_continuation_count"] >= 3

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        events = kanban_db.list_events(conn, projected["kanban_task_id"])
        assert task is not None
        assert task.status == "running"
        assert task.current_run_id == fixture["run_7"] + 1
        assert task.worker_pid == revision_pid
        assert [run.id for run in runs][-2:] == [fixture["run_7"], fixture["run_7"] + 1]
        body = json.loads(task.body or "{}")
        assert body["fresh_execution_provenance"] == "human_review_changes_requested"
        assert body["reviewed_run_id"] == fixture["run_7"]
        assert body["revision_source_base"] == "current_canonical_source"
        assert any(
            event.kind == "governed_autonomy_continuation_prepared"
            and event.payload.get("fresh_execution_provenance")
            == "human_review_changes_requested"
            and event.payload.get("reviewed_run_id") == fixture["run_7"]
            for event in events
        )
    finally:
        conn.close()
    revision_workspace = Path(revision_result["workspace_path"])
    assert not (
        revision_workspace
        / "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt"
    ).exists()
    assert (
        fixture["run_7_workspace"] / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes() == run_7_manifest

    replay = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback=_P18_9_1_REVIEW_CHANGES_FEEDBACK,
        reviewed_run_id=fixture["run_7"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("review decision replay must not spawn"),
    )
    assert replay["idempotent_replay"] is True
    assert replay["revision_kanban_run_id"] == fixture["run_7"] + 1
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs_after_replay = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert [run.id for run in runs_after_replay][-2:] == [
            fixture["run_7"],
            fixture["run_7"] + 1,
        ]
        assert all(run.id != fixture["run_7"] + 2 for run in runs_after_replay)
    finally:
        conn.close()


def test_terminal_completed_predecessor_evidence_requires_more_than_approval(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    with pytest.raises(pr.ProductRuntimeConflict, match="execution-start authority is absent"):
        pr.load_terminal_completed_predecessor_evidence("P18.9.1")


def test_historical_projection_validation_requires_explicit_generation_and_decision(
    projection_home,
    monkeypatch,
) -> None:
    _pr, _projected, projection_authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )
    historical_authority = bridge.load_historical_approved_predecessor_generation_authority(
        ticket_id="P18.9.1",
    )
    assert historical_authority is not None
    generation = historical_authority["generation_record"]
    decision = historical_authority["approval_decision_record"]
    _install_current_roadmap_authority_drift_for_test(monkeypatch)

    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        bridge.load_generation_record(ticket_id="P18.9.1")

    with pytest.raises(
        projection.WorkPacketKanbanProjectionConflict,
        match="generation authority must be supplied",
    ):
        projection.load_kanban_projection_record(
            ticket_id="P18.9.1",
            decision_record=decision,
            allow_terminal_completed_predecessor_historical=True,
        )

    with pytest.raises(
        projection.WorkPacketKanbanProjectionConflict,
        match="approval decision authority must be supplied",
    ):
        projection.load_kanban_projection_record(
            ticket_id="P18.9.1",
            generation_record=generation,
            allow_terminal_completed_predecessor_historical=True,
        )

    validated = projection.load_kanban_projection_record(
        ticket_id="P18.9.1",
        generation_record=generation,
        decision_record=decision,
        allow_terminal_completed_predecessor_historical=True,
    )
    assert validated is not None
    assert validated["ticket_id"] == "P18.9.1"
    assert validated["projection_SHA256"] == projection_authority["projection_SHA256"]

    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        projection.project_current_approved_workpacket_to_kanban(
            workflow=_approved_workflow_for_record(generation),
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )


def test_historical_terminal_completed_predecessor_traverses_to_rejected_successor(
    projection_home,
    monkeypatch,
) -> None:
    pr, _projected, _authority, _fixture, accepted = _accepted_p18_9_1_review_for_handoff(
        projection_home,
        monkeypatch,
    )
    projection_authority = projection.load_kanban_projection_record(ticket_id="P18.9.1")
    assert projection_authority is not None
    legacy_activation = _install_legacy_governed_autonomy_activation_shape_for_test(
        pr,
        projection_authority,
    )
    assert legacy_activation["live_lineage_activation_authorized"] is False

    with pytest.raises(
        pr.ProductRuntimeConflict,
        match="human Git handoff completion is absent",
    ):
        pr.load_terminal_completed_predecessor_evidence("P18.9.1")

    completed = pr.complete_current_ticket_human_git_handoff(
        **_p18_9_1_handoff_completion_kwargs(accepted),
    )
    generation_workflow = pr.build_workflow_control_snapshot()
    generated = bridge.generate_current_ticket(workflow=generation_workflow)
    rejected = bridge.apply_ticket_approval_decision(
        ticket_id="P18.9.2",
        decision="reject",
        actor="historical-human",
    )
    _install_current_roadmap_authority_drift_for_test(monkeypatch)

    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        bridge.load_generation_record(ticket_id="P18.9.1")
    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        bridge.load_generation_record(ticket_id="P18.9.2")
    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        bridge.apply_ticket_approval_decision(
            ticket_id="P18.9.1",
            decision="approve",
            actor="historical-human",
        )
    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        projection.load_kanban_projection_record(ticket_id="P18.9.1")
    historical_authority = bridge.load_historical_approved_predecessor_generation_authority(
        ticket_id="P18.9.1",
    )
    assert historical_authority is not None
    historical_projection = projection.load_kanban_projection_record(
        ticket_id="P18.9.1",
        generation_record=historical_authority["generation_record"],
        decision_record=historical_authority["approval_decision_record"],
        allow_terminal_completed_predecessor_historical=True,
    )
    assert historical_projection is not None
    with pytest.raises(pr.ProductRuntimeAuthorityMismatch) as current_activation_error:
        pr.load_current_ticket_governed_autonomy_activation_record(
            projection_record=historical_projection,
        )
    assert current_activation_error.value.diagnostics["reason"] == (
        "current_backend_stable_authority_unavailable"
    )
    assert current_activation_error.value.diagnostics["detail"] == (
        "generated authority canonical_next_ticket_authority mismatch"
    )

    evidence = pr.load_terminal_completed_predecessor_evidence("P18.9.1")
    assert evidence is not None
    assert evidence["verdict"] == "HISTORICAL_TERMINAL_COMPLETED_PREDECESSOR_TRAVERSAL_READY"
    assert evidence["current_actionable_authority"] is False
    assert evidence["generation_record"]["ticket_id"] == "P18.9.1"
    assert evidence["approval_decision_record"]["decision"] == "approve"
    assert evidence["kanban_projection_record"]["ticket_id"] == "P18.9.1"
    assert evidence["execution_start_record"]["ticket_id"] == "P18.9.1"
    assert evidence["governed_autonomy_activation_record"]["ticket_id"] == "P18.9.1"
    assert evidence["governed_autonomy_activation_record"]["live_lineage_activation_authorized"] is False
    assert evidence["governed_autonomy_runtime_state"]["ticket_id"] == "P18.9.1"
    assert evidence["review_decision_record"]["review_decision"] == "accept"
    assert evidence["human_git_handoff_completion_record"]["workflow_status"] == "completed"

    with pytest.raises(bridge.TicketArchitectBridgeConflict):
        projection.project_current_approved_workpacket_to_kanban(
            workflow=_approved_workflow_for_record(evidence["generation_record"]),
            requested_project_id="PEPPER",
            requested_ticket_id="P18.9.1",
            requested_next_action_id="P18_9_1_APPROVED_NO_EXECUTION",
        )

    review_path = pr.review_decision_record_path_for_ticket("P18.9.1")
    original_review = review_path.read_bytes()
    review_record = json.loads(original_review.decode("utf-8"))
    review_record["reviewed_candidate_SHA256"] = "0" * 64
    review_record["review_decision_SHA256"] = pr._review_decision_record_digest(review_record)
    _write_json_authority_record(review_path, review_record)
    with pytest.raises(pr.ProductRuntimeConflict, match="review candidate"):
        pr.load_terminal_completed_predecessor_evidence("P18.9.1")
    review_path.write_bytes(original_review)

    handoff_path = pr.human_git_handoff_completion_record_path_for_ticket("P18.9.1")
    original_handoff = handoff_path.read_bytes()
    handoff_record = json.loads(original_handoff.decode("utf-8"))
    handoff_record["workflow_status"] = "tampered_completed"
    handoff_record["completion_record_SHA256"] = (
        pr._human_git_handoff_completion_record_digest(handoff_record)
    )
    _write_json_authority_record(handoff_path, handoff_record)
    with pytest.raises(pr.ProductRuntimeConflict, match="workflow_status mismatch"):
        pr.load_terminal_completed_predecessor_evidence("P18.9.1")
    handoff_path.write_bytes(original_handoff)

    loaded_rejected = bridge.load_generation_record(
        ticket_id="P18.9.2",
        allow_terminal_rejected_historical=True,
    )
    snapshot = pr.build_workflow_control_snapshot()

    assert completed["closed_predecessor_ticket_id"] == "P18.9.1"
    assert generated["ticket_id"] == "P18.9.2"
    assert rejected["status"] == "rejected"
    assert loaded_rejected is not None
    assert snapshot["current_ticket_id"] is None
    assert snapshot["generated_successor_ticket_id"] == "P18.9.2"
    assert snapshot["workflow_state"] == "P18.9.2-AWAITING-CORRECTION"
    assert snapshot["workflow_status"] == "awaiting_correction"
    assert snapshot["pending_ticket_approval_count"] == 0
    assert snapshot["next_action"]["id"] == "REVISE_P18_9_2"
    traversal = snapshot["historical_terminal_completed_predecessor_traversal"]
    assert traversal["verdict"] == "HISTORICAL_TERMINAL_COMPLETED_PREDECESSOR_TRAVERSAL_READY"
    assert traversal["current_actionable_authority"] is False
    assert snapshot["ticket_execution_authorized"] is False
    assert snapshot["WorkPacket_execution_authorized"] is False
    assert snapshot["runtime_execution_authorized"] is False
    assert snapshot["worker_execution"] is False
    assert snapshot["Kanban_dispatch"] is False
    assert snapshot["Git_mutation"] is False


def test_current_p18_9_1_review_changes_requested_requires_same_workpacket_authority(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )
    fixture = _start_p18_9_1_validated_review_ready_run_7(
        pr,
        projection_home,
        projected,
        monkeypatch,
        pids=(6935, 6936, 6937),
    )

    blocked = pr.submit_current_ticket_review_decision(
        decision="changes_requested",
        feedback=(
            _P18_9_1_REVIEW_CHANGES_FEEDBACK
            + " Also modify 2_products/pepper-agent/package-lock.json."
        ),
        reviewed_run_id=fixture["run_7"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("authority expansion must not spawn"),
    )

    assert blocked["blocker_code"] == "REVIEW_FEEDBACK_REQUIRES_AUTHORITY_EXPANSION"
    assert blocked["authority_expansion_required"] is True
    assert blocked["dispatch_performed"] is False
    assert blocked["execution_started"] is False
    assert blocked["Git_mutation"] is False
    assert not pr.review_decision_record_path_for_ticket("P18.9.1").exists()

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == fixture["run_7"]
        assert all(run.id != fixture["run_7"] + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_review_reject_records_no_execution(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )
    fixture = _start_p18_9_1_validated_review_ready_run_7(
        pr,
        projection_home,
        projected,
        monkeypatch,
        pids=(6945, 6946, 6947),
    )

    rejected = pr.submit_current_ticket_review_decision(
        decision="reject",
        feedback="Human rejects the validated P18.9.1 candidate and requests no further execution.",
        reviewed_run_id=fixture["run_7"],
        project_id="PEPPER",
        ticket_id="P18.9.1",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("reject must not spawn"),
    )

    assert rejected["review_decision"] == "reject"
    assert rejected["review_validation_decision"] == "cancelled"
    assert rejected["review_state"] == "rejected"
    assert rejected["dispatch_performed"] is False
    assert rejected["execution_started"] is False
    assert rejected["Git_mutation"] is False
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "review_rejected_no_execution"
    assert workflow["review_state"] == "rejected"
    assert workflow["next_action"]["id"] == "P18_9_1_REVIEW_REJECTED_NO_EXECUTION"

    from hermes_cli import kanban_db

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == fixture["run_7"]
        assert all(run.id != fixture["run_7"] + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_fresh_execution_after_terminal_run_is_idempotent(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    activation = _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)["activation"]
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6515)
    started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 under governed autonomy before fresh replay proof.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6515,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = started["kanban_run_id"]
    assert run_5 == run_4 + 1

    run_5_workspace = Path(started["workspace_path"])
    _write_p18_9_1_terminal_candidate_fixture(pr, projection_home, run_5_workspace)
    run_5_manifest = (
        run_5_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes()
    run_5_failure = "GOVERNED_AUTONOMY_TERMINAL_RUN_BLOCKED: historical terminal run"
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary=run_5_failure,
    )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        run_5_before = next(
            run
            for run in kanban_db.list_runs(conn, projected["kanban_task_id"])
            if run.id == run_5
        )
        run_5_snapshot = {
            "id": run_5_before.id,
            "status": run_5_before.status,
            "outcome": run_5_before.outcome,
            "summary": run_5_before.summary,
            "error": run_5_before.error,
            "ended_at": run_5_before.ended_at,
        }
    finally:
        conn.close()

    plain_continue = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Observe terminal governed run without requesting a fresh attempt.",
        strategy="DIRECT",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("plain continue must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert plain_continue["idempotent_replay"] is True
    assert plain_continue["observation_status"] == "governed_autonomy_execution_terminal_reconciled"
    assert plain_continue["terminal_run_id"] == run_5
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_5
        assert all(run.id != run_5 + 1 for run in runs)
    finally:
        conn.close()

    fresh_request_text = (
        "Launch a fresh P18.9.1 governed execution after corrected runtime substrate."
    )
    spawn_calls: list[dict] = []

    def spawn(task, workspace, board=None, env_overlay=None):
        spawn_calls.append({
            "task_id": task.id,
            "workspace": workspace,
            "board": board,
            "env_overlay": env_overlay,
        })
        return 6616

    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6616)
    fresh = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Start the explicitly requested fresh same-authority P18.9.1 attempt.",
        strategy="DIRECT",
        fresh_execution_request_text=fresh_request_text,
        spawn_fn=spawn,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert len(spawn_calls) == 1
    assert fresh["idempotent_replay"] is False
    assert fresh["governed_autonomy_runtime_status"] == "direct_execution_continuation_started"
    assert fresh["kanban_run_created"] is True
    assert fresh["kanban_run_id"] == run_5 + 1
    assert fresh["fresh_execution_requested"] is True
    assert fresh["execution_attempt_reason"] == pr.PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON
    assert fresh["prior_terminal_run_id"] == run_5
    assert fresh["fresh_execution_request_reference"]["prior_terminal_run_id"] == run_5
    assert fresh["source_run_id"] == run_4
    assert fresh["work_packet_id"] == projected["work_packet_id"]
    assert fresh["work_packet_SHA256"] == projected["work_packet_SHA256"]
    assert fresh["Git_mutation"] is False
    assert fresh["auto_retry"] is False
    assert fresh["auto_rollback"] is False
    assert spawn_calls[0]["env_overlay"]["HERMES_AGENT_PLATFORM_WORKPACKET_ID"] == (
        projected["work_packet_id"]
    )
    fresh_workspace = Path(fresh["workspace_path"])
    assert fresh_workspace != run_5_workspace
    assert (fresh_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).is_file()
    assert not (
        fresh_workspace
        / "2_products/pepper-agent/web/src/agent-platform/shell/P18.9.1-implementation-report.txt"
    ).exists()

    runtime_record = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
        activation_record=pr.load_current_ticket_governed_autonomy_activation_record(
            projection_record=authority,
        ),
    )
    assert runtime_record is not None
    assert runtime_record["activation_action_SHA256"] == activation["activation_action_SHA256"]
    assert runtime_record["fresh_execution_request_SHA256"] == fresh[
        "fresh_execution_request_SHA256"
    ]
    assert runtime_record["prior_terminal_run_id"] == run_5

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        events = kanban_db.list_events(conn, projected["kanban_task_id"])
        run_5_after = next(run for run in runs if run.id == run_5)
        assert task is not None
        assert task.status == "running"
        assert task.current_run_id == run_5 + 1
        assert task.worker_pid == 6616
        assert [run.id for run in runs][-2:] == [run_5, run_5 + 1]
        assert {
            "id": run_5_after.id,
            "status": run_5_after.status,
            "outcome": run_5_after.outcome,
            "summary": run_5_after.summary,
            "error": run_5_after.error,
            "ended_at": run_5_after.ended_at,
        } == run_5_snapshot
        body = json.loads(task.body or "{}")
        assert body["fresh_execution_requested"] is True
        assert body["fresh_execution_request_SHA256"] == fresh["fresh_execution_request_SHA256"]
        assert body["execution_attempt_reason"] == pr.PEPPER_GOVERNED_AUTONOMY_FRESH_EXECUTION_REASON
        assert body["prior_terminal_run_id"] == run_5
        assert any(
            event.kind == "governed_autonomy_continuation_prepared"
            and isinstance(event.payload.get("fresh_execution_request_reference"), dict)
            and event.payload["fresh_execution_request_reference"]["prior_terminal_run_id"] == run_5
            for event in events
        )
    finally:
        conn.close()
    assert (
        run_5_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes() == run_5_manifest

    active_replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Replay the same fresh request while the new run is active.",
        strategy="DIRECT",
        fresh_execution_request_text=fresh_request_text,
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("active fresh replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert active_replay["idempotent_replay"] is True
    assert active_replay["observation_status"] == "governed_autonomy_execution_already_active"
    assert active_replay["kanban_run_id"] == run_5 + 1

    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5 + 1,
        status="blocked",
        outcome="blocked",
        summary="fresh attempt terminalized in offline duplicate-replay fixture",
    )
    terminal_replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Replay the same fresh request after its run reached terminal state.",
        strategy="DIRECT",
        fresh_execution_request_text=fresh_request_text,
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("duplicate fresh request must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert terminal_replay["idempotent_replay"] is True
    assert terminal_replay["fresh_execution_duplicate_suppressed"] is True
    assert terminal_replay["fresh_execution_request_SHA256"] == fresh[
        "fresh_execution_request_SHA256"
    ]
    assert terminal_replay["terminal_run_id"] == run_5 + 1

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert [run.id for run in runs][-2:] == [run_5, run_5 + 1]
        assert all(run.id != run_5 + 2 for run in runs)
        run_5_after_duplicate = next(run for run in runs if run.id == run_5)
        assert {
            "id": run_5_after_duplicate.id,
            "status": run_5_after_duplicate.status,
            "outcome": run_5_after_duplicate.outcome,
            "summary": run_5_after_duplicate.summary,
            "error": run_5_after_duplicate.error,
            "ended_at": run_5_after_duplicate.ended_at,
        } == run_5_snapshot
    finally:
        conn.close()
    assert (
        run_5_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes() == run_5_manifest


def test_current_p18_9_1_governed_autonomy_fresh_preparation_blocker_is_unconsumed(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6715)
    started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 under governed autonomy before a prep blocker.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6715,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = started["kanban_run_id"]
    assert run_5 == run_4 + 1
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary="terminal run available before a synthetic source-state blocker",
    )
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        conn.execute(
            "UPDATE tasks SET status = 'todo' WHERE id = ?",
            (projected["kanban_task_id"],),
        )
        conn.commit()
    finally:
        conn.close()

    fresh_request_text = "Launch a fresh P18.9.1 attempt after fixing source state."
    blocked = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Attempt fresh execution while the projected task is not ready.",
        strategy="DIRECT",
        fresh_execution_request_text=fresh_request_text,
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("prep blocker must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert blocked["governed_autonomy_runtime_status"] == "blocked_stop_for_human"
    assert blocked["blocker_code"] == "KANBAN_GOVERNED_AUTONOMY_SOURCE_GAP"
    assert blocked["kanban_run_created"] is False
    assert blocked["dispatch_performed"] is False
    assert blocked["fresh_execution_requested"] is False
    assert blocked["fresh_execution_request_SHA256"] is None
    assert blocked["execution_attempt_reason"] is None
    assert blocked["prior_terminal_run_id"] is None
    assert blocked["validation_failure_count"] == 0
    pending_ref = blocked["latest_decision_evidence"][
        "fresh_execution_request_reference"
    ]
    assert pending_ref["fresh_execution_requested"] is True
    assert pending_ref["prior_terminal_run_id"] == run_5

    record = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
    )
    assert record is not None
    assert record["fresh_execution_requested"] is False
    assert record["fresh_execution_request_SHA256"] is None
    assert record["validation_failure_count"] == 0
    assert not pr._governed_autonomy_fresh_execution_request_already_consumed(
        record,
        pending_ref,
    )

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert [run.id for run in runs][-1] == run_5
        assert all(run.id != run_5 + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_resumes_legacy_pending_fresh_request_from_triage(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    activation_result = _activate_p18_9_1_governed_autonomy_for_test(
        pr,
        monkeypatch,
    )
    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    live_pids = {6725, 6726, 6727}
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) in live_pids)

    run_5_started = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Continue P18.9.1 before reproducing a terminal triage source.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6725,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_5 = run_5_started["kanban_run_id"]
    assert run_5 == run_4 + 1
    _block_projected_run(
        kanban_db,
        projected,
        run_5,
        reason="synthetic governed run 5 needs input before a fresh attempt",
        kind="needs_input",
    )

    first_fresh = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Create run 6 as a first same-authority fresh execution.",
        strategy="DIRECT",
        fresh_execution_request_text="Launch a first fresh P18.9.1 governed attempt.",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6726,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    run_6 = first_fresh["kanban_run_id"]
    assert run_6 == run_5 + 1
    run_6_workspace = Path(first_fresh["workspace_path"])
    run_6_manifest = (
        run_6_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes()
    _block_projected_run(
        kanban_db,
        projected,
        run_6,
        reason="synthetic governed run 6 repeated needs-input block routes to triage",
        kind="needs_input",
    )

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task_before = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs_before = kanban_db.list_runs(conn, projected["kanban_task_id"])
        events_before = kanban_db.list_events(conn, projected["kanban_task_id"])
        run_6_before = next(run for run in runs_before if run.id == run_6)
        run_6_snapshot = {
            "id": run_6_before.id,
            "status": run_6_before.status,
            "outcome": run_6_before.outcome,
            "summary": run_6_before.summary,
            "error": run_6_before.error,
            "ended_at": run_6_before.ended_at,
        }
        assert task_before is not None
        assert task_before.status == "triage"
        assert any(
            event.kind == "block_loop_detected" and event.run_id == run_6
            for event in events_before
        )
    finally:
        conn.close()

    activation = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert activation is not None
    assert activation["activation_action_SHA256"] == activation_result["activation"][
        "activation_action_SHA256"
    ]
    previous_runtime = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
        activation_record=activation,
    )
    assert previous_runtime is not None
    effective_authority = pr._resolve_effective_current_governed_autonomy_authority(
        projection=authority,
        activation=activation,
        previous=previous_runtime,
    )
    terminal_reconciliation = pr._governed_autonomy_runtime_terminal_reconciliation(
        previous_runtime,
        effective_authority=effective_authority,
    )
    assert terminal_reconciliation is not None
    assert terminal_reconciliation["terminal_run_id"] == run_6

    pending_request_text = (
        "Start a fresh governed P18.9.1 execution because the governed validation "
        "dependency substrate has been materially corrected since terminal run 6. "
        "Preserve all previous runs as immutable historical evidence. Create a new "
        "workspace from current canonical source and execute using the corrected "
        "Pepper worker and native Hermes conversation loop."
    )
    pending_request = pr.CurrentTicketGovernedAutonomyContinuationRequest(
        runtime_goal=(
            "Start and monitor one fresh governed execution attempt for P18.9.1 "
            "under existing canonical authority."
        ),
        strategy="DIRECT",
        fresh_execution_request_text=pending_request_text,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    pending_ref = pr._governed_autonomy_fresh_execution_request_reference(
        pending_request,
        projection=authority,
        activation=activation,
        terminal_reconciliation=terminal_reconciliation,
    )
    assert pending_ref is not None
    assert pending_ref["human_request_text_SHA256"] == (
        "f5b743d309ab84df5a4ee736b0f951797a5d1a43a453ae260204de8042c967ad"
    )
    pending_ref = dict(pending_ref)
    pending_ref["fresh_execution_request_SHA256"] = (
        "e3b52f46b77e46374beb0608632304765a4654edd48e99bb74747a66214a9bc3"
    )
    legacy_pending_record = pr._governed_autonomy_runtime_base_record(
        request=pending_request,
        projection=authority,
        activation=activation,
        previous=previous_runtime,
        runtime_decision="DIRECT",
        runtime_status="blocked_stop_for_human",
        latest_decision_evidence={
            "decision": "DIRECT",
            "direct_execution_request_reference": {
                "task_prepare_status": "blocked",
                "blocker_code": "KANBAN_GOVERNED_AUTONOMY_SOURCE_GAP",
                "blocker_detail": "projected Kanban task status is triage",
            },
            "blocker_code": "KANBAN_GOVERNED_AUTONOMY_SOURCE_GAP",
            "blocker_detail": "projected Kanban task status is triage",
            "fresh_execution_request_reference": pending_ref,
        },
        provider_readiness=_ready_executor_provider_payload(),
        process_continuation_increment=0,
        validation_failure_increment=activation["governed_autonomy_budget"][
            "max_no_progress_iterations"
        ],
        blocker_code="KANBAN_GOVERNED_AUTONOMY_SOURCE_GAP",
        blocker_detail="projected Kanban task status is triage",
        next_human_action=(
            "human authority required to resolve governed autonomy dispatch preparation"
        ),
        fresh_execution_request=pending_ref,
    )
    pr._persist_governed_autonomy_runtime_state(legacy_pending_record)
    assert legacy_pending_record["fresh_execution_requested"] is True
    assert legacy_pending_record["fresh_execution_request_SHA256"] == pending_ref[
        "fresh_execution_request_SHA256"
    ]
    assert legacy_pending_record["kanban_run_created"] is False
    assert legacy_pending_record["dispatch_performed"] is False
    assert legacy_pending_record["budget_exhausted"] is True
    assert not pr._governed_autonomy_fresh_execution_request_already_consumed(
        legacy_pending_record,
        pending_ref,
    )

    intervening_budget_stop = pr._build_governed_autonomy_runtime_stop_record(
        request=pr.CurrentTicketGovernedAutonomyContinuationRequest(
            runtime_goal=(
                "Record the exhausted budget observation that previously hid the "
                "pending fresh request."
            ),
            strategy="DIRECT",
            resume_pending_fresh_execution_request_SHA256=pending_ref[
                "fresh_execution_request_SHA256"
            ],
            project_id="PEPPER",
            ticket_id="P18.9.1",
        ),
        projection=authority,
        activation=activation,
        previous=legacy_pending_record,
        runtime_decision="STOP_FOR_HUMAN",
        blocker_code="GOVERNED_AUTONOMY_VALIDATION_FAILURE_BUDGET_EXHAUSTED",
        blocker_detail="validation failure budget is exhausted",
        validation_failed=False,
        provider_readiness=_ready_executor_provider_payload(),
        extra_evidence={"fresh_execution_request_reference": pending_ref},
    )
    pr._persist_governed_autonomy_runtime_state(intervening_budget_stop)
    assert intervening_budget_stop["fresh_execution_requested"] is False
    assert intervening_budget_stop["previous_runtime_state_SHA256"] == legacy_pending_record[
        "runtime_state_SHA256"
    ]

    missing_sha = "0" * 64
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Try an arbitrary pending request identity.",
            strategy="DIRECT",
            resume_pending_fresh_execution_request_SHA256=missing_sha,
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("missing SHA must not spawn"),
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )
    with pytest.raises(pr.ProductRuntimeConflict):
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Try a mismatched pending request identity and text.",
            strategy="DIRECT",
            fresh_execution_request_text=pending_request_text + " Mismatched.",
            resume_pending_fresh_execution_request_SHA256=pending_ref[
                "fresh_execution_request_SHA256"
            ],
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("mismatch must not spawn"),
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )
    assert pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
        activation_record=activation,
    )["runtime_state_SHA256"] == intervening_budget_stop["runtime_state_SHA256"]
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs_after_failed_identity = kanban_db.list_runs(
            conn,
            projected["kanban_task_id"],
        )
        assert [run.id for run in runs_after_failed_identity] == [
            run.id for run in runs_before
        ]
    finally:
        conn.close()

    spawn_calls: list[dict] = []

    def spawn(task, workspace, board=None, env_overlay=None):
        spawn_calls.append({
            "task_id": task.id,
            "workspace": workspace,
            "board": board,
            "env_overlay": env_overlay,
        })
        return 6727

    resumed = pr.continue_current_ticket_governed_autonomy(
        runtime_goal=(
            "Resume the already-recorded fresh P18.9.1 request by identity from triage."
        ),
        strategy="DIRECT",
        resume_pending_fresh_execution_request_SHA256=pending_ref[
            "fresh_execution_request_SHA256"
        ],
        spawn_fn=spawn,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert len(spawn_calls) == 1
    assert resumed["idempotent_replay"] is False
    assert resumed["governed_autonomy_runtime_status"] == "direct_execution_continuation_started"
    assert resumed["kanban_run_created"] is True
    assert resumed["kanban_run_id"] == run_6 + 1
    assert resumed["fresh_execution_requested"] is True
    assert resumed["fresh_execution_request_SHA256"] == pending_ref[
        "fresh_execution_request_SHA256"
    ]
    assert resumed["latest_decision_evidence"][
        "fresh_execution_request_recognition_status"
    ] == "pending_fresh_execution_request_resolved"
    assert resumed["latest_decision_evidence"][
        "fresh_execution_request_matched_record_source"
    ] == "history"
    assert resumed["latest_decision_evidence"][
        "fresh_execution_request_matched_lineage_distance"
    ] == 1
    assert resumed["prior_terminal_run_id"] == run_6
    prep_ref = resumed["latest_decision_evidence"]["direct_execution_request_reference"]
    assert prep_ref["task_prepare_status"] == "prepared"
    assert prep_ref["task_triage_specified"] is True
    assert prep_ref["task_unblocked"] is False
    assert prep_ref["kanban_task_status_after_prepare"] == "ready"
    assert prep_ref["fresh_execution_request_reference"][
        "fresh_execution_request_SHA256"
    ] == pending_ref["fresh_execution_request_SHA256"]
    assert spawn_calls[0]["env_overlay"]["HERMES_AGENT_PLATFORM_WORKPACKET_ID"] == (
        projected["work_packet_id"]
    )
    resumed_workspace = Path(resumed["workspace_path"])
    assert resumed_workspace != run_6_workspace
    assert (resumed_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST).is_file()
    assert (
        run_6_workspace / pr.PEPPER_SCRATCH_SOURCE_MATERIALIZATION_MANIFEST
    ).read_bytes() == run_6_manifest

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task_after = kanban_db.get_task(conn, projected["kanban_task_id"])
        runs_after = kanban_db.list_runs(conn, projected["kanban_task_id"])
        events_after = kanban_db.list_events(conn, projected["kanban_task_id"])
        run_6_after = next(run for run in runs_after if run.id == run_6)
        assert task_after is not None
        assert task_after.status == "running"
        assert task_after.current_run_id == run_6 + 1
        assert task_after.worker_pid == 6727
        assert [run.id for run in runs_after][-2:] == [run_6, run_6 + 1]
        assert {
            "id": run_6_after.id,
            "status": run_6_after.status,
            "outcome": run_6_after.outcome,
            "summary": run_6_after.summary,
            "error": run_6_after.error,
            "ended_at": run_6_after.ended_at,
        } == run_6_snapshot
        body = json.loads(task_after.body or "{}")
        assert body["fresh_execution_request_SHA256"] == pending_ref[
            "fresh_execution_request_SHA256"
        ]
        assert body["prior_terminal_run_id"] == run_6
        assert body["fresh_execution_attempt_number"] == len(runs_before) + 1
        assert any(event.kind == "specified" for event in events_after)
        assert any(
            event.kind == "governed_autonomy_continuation_prepared"
            and event.payload.get("task_triage_specified") is True
            and event.payload["fresh_execution_request_reference"][
                "fresh_execution_request_SHA256"
            ] == pending_ref["fresh_execution_request_SHA256"]
            for event in events_after
        )
    finally:
        conn.close()

    active_replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Replay the resumed fresh request while its run is active.",
        strategy="DIRECT",
        resume_pending_fresh_execution_request_SHA256=pending_ref[
            "fresh_execution_request_SHA256"
        ],
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("active replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert active_replay["idempotent_replay"] is True
    assert active_replay["observation_status"] == "governed_autonomy_execution_already_active"
    assert active_replay["kanban_run_id"] == run_6 + 1

    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_6 + 1,
        status="blocked",
        outcome="blocked",
        summary="resumed fresh attempt terminalized in duplicate suppression fixture",
    )
    terminal_replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Replay the resumed fresh request after it terminalized.",
        strategy="DIRECT",
        resume_pending_fresh_execution_request_SHA256=pending_ref[
            "fresh_execution_request_SHA256"
        ],
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("terminal replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert terminal_replay["idempotent_replay"] is True
    assert terminal_replay["fresh_execution_duplicate_suppressed"] is True
    assert terminal_replay["fresh_execution_request_SHA256"] == pending_ref[
        "fresh_execution_request_SHA256"
    ]
    assert terminal_replay["terminal_run_id"] == run_6 + 1

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        final_runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert [run.id for run in final_runs][-2:] == [run_6, run_6 + 1]
        assert all(run.id != run_6 + 2 for run in final_runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_fresh_execution_fails_closed_on_authority_mismatch(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    run_5 = _claim_next_projected_run(kanban_db, projected, pid=6715)
    assert run_5 == run_4 + 1
    _block_projected_run(
        kanban_db,
        projected,
        run_5,
        reason="unowned run superseded same-authority fresh execution source",
        kind="transient",
    )

    with pytest.raises(pr.ProductRuntimeAuthorityMismatch) as excinfo:
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Attempt fresh execution after authority drift.",
            strategy="DIRECT",
            fresh_execution_request_text=(
                "Launch a fresh P18.9.1 governed execution after corrected runtime substrate."
            ),
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("authority mismatch must not spawn"),
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )

    assert str(excinfo.value) == "CONTINUATION_AUTHORITY_MISMATCH"
    assert excinfo.value.diagnostics["reason"] == "newer_unowned_source_run"
    assert not pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.1").exists()
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_5
        assert all(run.id != run_5 + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_unifies_owned_terminal_run_after_a2a_history(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    activation = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert activation is not None
    historical_request = pr.CurrentTicketGovernedAutonomyContinuationRequest(
        runtime_goal="Historical A2A-shaped governed autonomy provenance.",
        strategy="A2A_DELEGATION",
        delegate_goal="Historical same-authority child delegation completed.",
        delegate_paths=(_first_projection_allowed_directory(projected),),
        delegate_requested_operations=("read_file",),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    historical_runtime = pr._governed_autonomy_runtime_base_record(
        request=historical_request,
        projection=authority,
        activation=activation,
        previous=None,
        runtime_decision="A2A_DELEGATION",
        runtime_status="a2a_delegation_completed",
        latest_decision_evidence={
            "decision": "A2A_DELEGATION",
            "historical_a2a_runtime_record": True,
        },
        provider_readiness=_ready_executor_provider_payload(),
        process_continuation_increment=0,
        delegation_increment=1,
        next_autonomous_action="continue governed autonomy from historical A2A provenance",
    )
    pr._persist_governed_autonomy_runtime_state(historical_runtime)

    prep = pr._prepare_current_ticket_governed_autonomy_task_for_dispatch(
        projection=authority,
        activation=activation,
        envelope=SimpleNamespace(
            envelope_SHA256=activation["governed_autonomy_envelope_SHA256"],
        ),
    )
    assert prep["task_prepare_status"] == "prepared"
    run_5 = _claim_next_projected_run(kanban_db, projected, pid=6815)
    assert run_5 == run_4 + 1

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        task = kanban_db.get_task(conn, projected["kanban_task_id"])
        assert task is not None
        workspace = Path(task.workspace_path)
    finally:
        conn.close()
    _write_p18_9_1_terminal_candidate_fixture(pr, projection_home, workspace)
    failure = (
        "workpacket_validation action list failed: TypeError: _handle() got an "
        "unexpected keyword argument 'session_id'"
    )
    _finish_projected_run_as_terminal(
        kanban_db,
        projected,
        run_5,
        status="blocked",
        outcome="blocked",
        summary=failure,
    )

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["authority_revalidated"] is True
    assert status["effective_live_lineage_activation_authorized"] is True
    assert status["continuation_eligible"] is True
    assert status["terminal_run_reconciled"] is True
    assert status["terminal_run_id"] == run_5
    assert status["effective_authority_diagnostics"]["activation_source_run_id"] == run_4
    ownership = status["effective_authority_diagnostics"]["owned_lineage_state"]
    assert ownership["owned_governed_run_id"] == run_5
    latest_probe = ownership["latest_run_ownership_probe"]
    assert latest_probe["owned"] is True
    assert {item["classification"] for item in latest_probe["comparisons"]} >= {
        "STABLE_AUTHORITY",
        "HISTORICAL_PROVENANCE",
        "RUNTIME_RECORD_STATE",
    }

    workflow = pr.build_workflow_control_snapshot()
    assert workflow["workflow_status"] == "governed_autonomy_validation_repairable"
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow["governed_autonomy_continuation_eligible"] is True

    replay = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Reconcile owned terminal run 5 without creating run 6.",
        strategy="DIRECT",
        spawn_fn=lambda *_args, **_kwargs: pytest.fail("terminal replay must not spawn"),
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert replay["authority_revalidated"] is True
    assert replay["idempotent_replay"] is True
    assert replay["non_consuming_observation"] is True
    assert replay["observation_status"] == "governed_autonomy_execution_terminal_reconciled"
    assert replay["terminal_run_id"] == run_5

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_5
        assert all(run.id != run_5 + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_tool_rejects_caller_supplied_authority(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db
    import tools.pepper_workflow_tools as pepper_tools

    _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    activation = json.loads(pepper_tools._activate_current_ticket_governed_autonomy({
        "human_request_text": (
            "Activate 01AH governed autonomy status for P18.9.1 without live lineage activation."
        ),
        "governed_autonomy_envelope": {"caller": "supplied"},
        "capability_gap": {"caller": "supplied"},
        "continuation_lineage": {"caller": "supplied"},
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
        "next_action_id": "RECOVER_P18_9_1_EXECUTION",
    }))
    assert activation["success"] is False
    assert "derives authority server-side" in activation["error"]
    assert "governed_autonomy_envelope" in activation["error"]
    assert not pr.governed_autonomy_activation_record_path_for_ticket("P18.9.1").exists()

    continuation = json.loads(pepper_tools._continue_current_ticket_governed_autonomy({
        "runtime_goal": "Try to continue with model-supplied authority.",
        "governed_autonomy_envelope": {"caller": "supplied"},
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
    }))
    assert continuation["success"] is False
    assert "persisted server-derived authority" in continuation["error"]

    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    raw_child_authority = json.loads(pepper_tools._continue_current_ticket_governed_autonomy({
        "runtime_goal": "Try to continue with model-supplied A2A child authority.",
        "strategy": "A2A_DELEGATION",
        "delegate_goal": "Inspect the delegated area.",
        "delegate_paths": ["2_products/pepper-agent/web/src/agent-platform/shell"],
        "delegate_requested_operations": ["codebase_inspection"],
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
    }))
    assert raw_child_authority["success"] is False
    assert "derive server-side" in raw_child_authority["error"]
    assert "delegate_requested_operations" in raw_child_authority["error"]


def test_current_p18_9_1_governed_autonomy_rejects_tampered_authority_digest(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    record = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert record is not None
    record["governed_autonomy_envelope_reference"]["source_run_count"] += 1
    record["activation_action_SHA256"] = pr._governed_autonomy_activation_record_digest(record)
    _write_governed_autonomy_activation_record_for_test(pr, record)

    with pytest.raises(pr.ProductRuntimeConflict) as excinfo:
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Attempt continuation with a tampered persisted authority digest.",
            strategy="DIRECT",
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )

    assert "authority reference digest mismatch" in str(excinfo.value)
    assert not pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.1").exists()
    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_4
        assert all(run.id != 5 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_rejects_stale_authority_after_new_blocked_run(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    run_5 = _claim_next_projected_run(kanban_db, projected, pid=6404)
    assert run_5 == run_4 + 1
    _block_projected_run(
        kanban_db,
        projected,
        run_5,
        reason="synthetic newer P18.9.1 blocked run superseded activation authority",
        kind="transient",
    )

    with pytest.raises(pr.ProductRuntimeAuthorityMismatch) as excinfo:
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Attempt continuation under stale source-run authority.",
            strategy="DIRECT",
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )

    assert str(excinfo.value) == "CONTINUATION_AUTHORITY_MISMATCH"
    diagnostics = excinfo.value.diagnostics
    assert diagnostics["blocker_code"] == "CONTINUATION_AUTHORITY_MISMATCH"
    assert diagnostics["activation_source_run_id"] == run_4
    assert diagnostics["current_source_run_id"] == run_5
    assert diagnostics["activation_authority_SHA256"] != diagnostics[
        "current_authority_SHA256"
    ]
    assert not pr.governed_autonomy_runtime_state_path_for_ticket("P18.9.1").exists()

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_5
        assert all(run.id != 6 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_rejects_active_foreign_execution(
    projection_home,
    monkeypatch,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    run_5 = _claim_next_projected_run(kanban_db, projected, pid=6825)
    assert run_5 == run_4 + 1
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6825)

    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["authority_revalidated"] is False
    assert status["continuation_eligible"] is False
    assert status["effective_authority_diagnostics"]["reason"] == (
        "unowned_active_execution_present"
    )

    with pytest.raises(pr.ProductRuntimeAuthorityMismatch) as excinfo:
        pr.continue_current_ticket_governed_autonomy(
            runtime_goal="Do not continue across an active foreign run.",
            strategy="DIRECT",
            spawn_fn=lambda *_args, **_kwargs: pytest.fail("mismatch must not spawn"),
            project_id="PEPPER",
            ticket_id="P18.9.1",
        )
    assert excinfo.value.diagnostics["reason"] == "unowned_active_execution_present"
    assert excinfo.value.diagnostics["current_active_run_ids"] == [run_5]

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_5
        assert all(run.id != run_5 + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_self_extension_stops_without_01ah_envelope(
    projection_home,
    monkeypatch,
    tmp_path,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    evidence = _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    allowed_dir = _first_projection_allowed_directory(projected)
    helper_path = f"{allowed_dir}/autonomy_runtime_helper.py"

    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Repair the failed run with a task-local helper under the active authority.",
        observed_failure="Missing task-local helper for offline inspection.",
        requested_capability="task local helper",
        strategy="TASK_LOCAL_SELF_EXTENSION",
        task_local_tool_name="autonomy_runtime_helper",
        task_local_language="python",
        task_local_implementation_path=helper_path,
        task_local_source_text="print('01AI runtime helper ok')\n",
        task_local_command=f"python {helper_path}",
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert evidence["activation"]["01AH_envelope_lifecycle_classification"] == "01AH_ENVELOPE_WRONG_LIFECYCLE_PHASE"
    assert result["runtime_decision"] == "STOP_FOR_HUMAN"
    assert result["governed_autonomy_runtime_status"] == "blocked_stop_for_human"
    assert result["blocker_code"] == "TASK_LOCAL_SELF_EXTENSION_01AH_ENVELOPE_GAP"
    assert result["authority_revalidated"] is True
    assert result["legacy_human_recovery_retry_micro_gates_required"] is False
    assert result["source_run_id"] == run_4
    assert result["kanban_run_count"] == 3
    assert result["self_repair_count"] == 0
    assert result["task_local_tool_candidate_count"] == 0
    assert result["command_evaluation_count"] == 0
    assert result["validation_failure_count"] == 1
    assert result["A2A_dispatch_performed"] is False
    assert result["dispatch_performed"] is False
    assert result["Kanban_dispatch"] is False
    assert result["Git_mutation"] is False
    assert result["auto_retry"] is False
    assert result["latest_decision_evidence"]["authority_kind"] == "backend_derived_live_authority"

    record = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
    )
    assert record is not None
    assert record["runtime_state_SHA256"] == result["runtime_state_SHA256"]
    assert "governed_autonomy_envelope" not in record
    assert "task_local_source_text" not in record
    assert "tool_candidate_reference" not in record["latest_decision_evidence"]
    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["governed_autonomy_runtime"]["runtime_state_SHA256"] == result[
        "runtime_state_SHA256"
    ]

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_4
        assert all(run.id != 5 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_a2a_uses_injected_delegate_runner(
    projection_home,
    monkeypatch,
    tmp_path,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    allowed_dir = _first_projection_allowed_directory(projected)
    calls: list[dict] = []

    def delegate_runner(**kwargs):
        calls.append(kwargs)
        return {
            "status": "completed",
            "summary": "offline injected Hermes delegate_task result",
            "api_calls": 0,
        }

    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Delegate bounded offline inspection under the active authority.",
        strategy="A2A_DELEGATION",
        delegate_goal="Inspect only the delegated allowed path and summarize.",
        delegate_runner=delegate_runner,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert len(calls) == 1
    assert calls[0]["role"] == "leaf"
    assert calls[0]["background"] is False
    assert allowed_dir in calls[0]["context"]["delegate_paths"]
    assert calls[0]["context"]["delegate_requested_operations"] == [
        "list_directory",
        "read_file",
    ]
    assert calls[0]["context"]["child_authority_source"] == "backend_derived_parent_authority"
    assert calls[0]["context"]["git_mutation"] is False
    assert calls[0]["context"]["provider_dispatch_count"] == 0
    assert calls[0]["context"]["model_inference_count"] == 0
    assert result["runtime_decision"] == "A2A_DELEGATION"
    assert result["governed_autonomy_runtime_status"] == "a2a_delegation_completed"
    assert result["A2A_dispatch_performed"] is True
    assert result["A2A_delegation_count"] == 1
    assert result["source_run_id"] == run_4
    assert result["provider_dispatch_count"] == 0
    assert result["model_inference_count"] == 0
    assert result["Git_mutation"] is False
    request_ref = result["latest_decision_evidence"]["a2a_delegation_request_reference"]
    assert request_ref["runtime_kind"] == "hermes_delegate_task"
    assert request_ref["opencode_provider_route"] == "opencode-zen"
    assert request_ref["delegate_paths_source"] == "backend_allowed_paths"
    assert request_ref["delegate_requested_operations_source"] == "backend_goal_classification"
    assert request_ref["git_mutation"] is False
    result_ref = result["latest_decision_evidence"]["a2a_delegation_result_reference"]
    assert result_ref["status"] == "completed"

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_4
        assert all(run.id != 5 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_a2a_resolves_canonical_delegate_task_when_runner_omitted(
    projection_home,
    monkeypatch,
    tmp_path,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db
    from tools import delegate_tool
    from tools.registry import registry

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    allowed_dir = _first_projection_allowed_directory(projected)
    parent_agent = SimpleNamespace(
        _delegate_depth=0,
        _memory_manager=None,
        session_id="parent-session",
        model="gpt-5.5",
        provider="openai-codex",
        base_url="https://example.invalid/v1",
        api_key="test-key",
        enabled_toolsets=["file", "terminal", "web", "delegation"],
        disabled_toolsets=[],
        valid_tool_names=["read_file", "write_file", "terminal", "delegate_task"],
    )
    build_calls: list[dict] = []
    run_calls: list[dict] = []

    def build_child_agent(**kwargs):
        build_calls.append(kwargs)
        return SimpleNamespace(
            session_id="child-session",
            _delegate_role=kwargs["role"],
        )

    def run_single_child(task_index, goal, child=None, parent_agent=None, **_kwargs):
        run_calls.append({
            "task_index": task_index,
            "goal": goal,
            "child": child,
            "parent_agent": parent_agent,
        })
        return {
            "task_index": task_index,
            "status": "completed",
            "summary": "canonical Hermes delegate_task fake provider result",
            "api_calls": 0,
            "duration_seconds": 0,
            "_child_role": getattr(child, "_delegate_role", None),
        }

    monkeypatch.setattr(delegate_tool, "_build_child_agent", build_child_agent)
    monkeypatch.setattr(delegate_tool, "_run_single_child", run_single_child)
    entry = registry.get_entry("delegate_task")
    assert entry is not None
    assert entry.toolset == "delegation"

    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Delegate through the canonical Hermes A2A runtime under the active authority.",
        strategy="A2A_DELEGATION",
        delegate_goal="Inspect only the delegated allowed path and summarize.",
        delegate_parent_agent=parent_agent,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert len(build_calls) == 1
    assert len(run_calls) == 1
    build_call = build_calls[0]
    delegated_parent = build_call["parent_agent"]
    assert delegated_parent.enabled_toolsets == []
    assert delegated_parent.valid_tool_names == []
    assert delegated_parent.model == "gpt-5.5"
    assert build_call["role"] == "leaf"
    assert '"parent_authority_SHA256"' in build_call["context"]
    assert allowed_dir in build_call["context"]
    assert run_calls[0]["parent_agent"].enabled_toolsets == []

    assert result["runtime_decision"] == "A2A_DELEGATION"
    assert result["governed_autonomy_runtime_status"] == "a2a_delegation_completed"
    assert result["A2A_dispatch_performed"] is True
    assert result["A2A_delegation_count"] == 1
    assert result["source_run_id"] == run_4
    assert result["legacy_human_recovery_retry_micro_gates_required"] is False
    assert result["provider_dispatch_count"] == 0
    assert result["model_inference_count"] == 0
    assert result["Git_mutation"] is False
    request_ref = result["latest_decision_evidence"]["a2a_delegation_request_reference"]
    assert request_ref["runner_source"] == "canonical_hermes_delegate_task"
    assert request_ref["canonical_runtime_classification"] == "HERMES_CANONICAL_A2A_FOUND"
    assert request_ref["delegate_paths_source"] == "backend_allowed_paths"
    assert request_ref["delegate_requested_operations_source"] == "backend_goal_classification"
    assert request_ref["delegate_task_registered"] is True
    assert request_ref["delegate_task_toolset"] == "delegation"
    assert request_ref["opencode_provider_profile_found"] is True
    assert request_ref["opencode_delegate_registration_status"] == "provider_profile_only_not_delegate_tool"
    result_ref = result["latest_decision_evidence"]["a2a_delegation_result_reference"]
    assert result_ref["status"] == "completed"
    assert result_ref["result_shape"] == "json_string"
    assert result_ref["result_count"] == 1
    assert result_ref["api_call_count"] == 0
    assert "fake provider result" in result_ref["summary_excerpt"]

    record = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
    )
    assert record is not None
    assert "delegate_result" not in record
    assert record["latest_decision_evidence"]["a2a_delegation_result_reference"]["result_count"] == 1

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_4
        assert all(run.id != 5 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_a2a_denies_out_of_scope_child_authority(
    projection_home,
    monkeypatch,
    tmp_path,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    called = False

    def delegate_runner(**_kwargs):
        nonlocal called
        called = True
        raise AssertionError("delegate runner must not be called")

    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Attempt an out-of-scope child delegation.",
        strategy="A2A_DELEGATION",
        delegate_goal="Inspect a forbidden path.",
        delegate_paths=("outside/scope.txt",),
        delegate_requested_operations=("read_file",),
        delegate_runner=delegate_runner,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert called is False
    assert result["runtime_decision"] == "STOP_FOR_HUMAN"
    assert result["governed_autonomy_runtime_status"] == "blocked_stop_for_human"
    assert result["blocker_code"] == "A2A_CHILD_AUTHORITY_PATH_OUT_OF_SCOPE"
    assert result["validation_failure_count"] == 1
    assert result["A2A_delegation_count"] == 0
    assert result["A2A_dispatch_performed"] is False
    assert result["source_run_id"] == run_4

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_4
        assert all(run.id != 5 for run in runs)
    finally:
        conn.close()


@pytest.mark.parametrize("operation", ("git_mutation", "package_install", "docker", "graphify"))
def test_current_p18_9_1_governed_autonomy_a2a_denies_privileged_child_operations(
    projection_home,
    monkeypatch,
    operation,
) -> None:
    pr, projected, _authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    allowed_dir = _first_projection_allowed_directory(projected)
    called = False

    def delegate_runner(**_kwargs):
        nonlocal called
        called = True
        raise AssertionError("delegate runner must not be called")

    result = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Attempt a privileged child delegation.",
        strategy="A2A_DELEGATION",
        delegate_goal="Run a privileged child operation.",
        delegate_paths=(allowed_dir,),
        delegate_requested_operations=(operation,),
        delegate_runner=delegate_runner,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )

    assert called is False
    assert result["runtime_decision"] == "STOP_FOR_HUMAN"
    assert result["governed_autonomy_runtime_status"] == "blocked_stop_for_human"
    assert result["blocker_code"] == "A2A_CHILD_AUTHORITY_OPERATION_DENIED"
    assert result["process_continuation_count"] == 0
    assert result["A2A_delegation_count"] == 0
    assert result["A2A_dispatch_performed"] is False
    assert result["source_run_id"] == run_4

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-1].id == run_4
        assert all(run.id != run_4 + 1 for run in runs)
    finally:
        conn.close()


def test_current_p18_9_1_governed_autonomy_status_reconstructs_runtime_after_restart(
    projection_home,
    monkeypatch,
    tmp_path,
) -> None:
    pr, projected, authority = _closed_p18_9_0_with_projected_p18_9_1(
        projection_home,
        monkeypatch,
    )

    from hermes_cli import kanban_db

    run_4 = _force_p18_9_1_blocked_run_4(pr, kanban_db, projected, monkeypatch)
    _activate_p18_9_1_governed_autonomy_for_test(pr, monkeypatch)
    activation = pr.load_current_ticket_governed_autonomy_activation_record(
        projection_record=authority,
    )
    assert activation is not None
    legacy_request = pr.CurrentTicketGovernedAutonomyContinuationRequest(
        runtime_goal="Historical metadata-only direct active-authority probe.",
        strategy="DIRECT",
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    first = pr._governed_autonomy_runtime_base_record(
        request=legacy_request,
        projection=authority,
        activation=activation,
        previous=None,
        runtime_decision="DIRECT",
        runtime_status="direct_continuation_recorded",
        latest_decision_evidence={"decision": "DIRECT", "historical_metadata_only": True},
        provider_readiness=_ready_executor_provider_payload(),
        process_continuation_increment=1,
        next_autonomous_action="historical metadata probe",
    )
    pr._persist_governed_autonomy_runtime_state(first)
    second = pr._governed_autonomy_runtime_base_record(
        request=legacy_request,
        projection=authority,
        activation=activation,
        previous=first,
        runtime_decision="DIRECT",
        runtime_status="direct_continuation_recorded",
        latest_decision_evidence={"decision": "DIRECT", "historical_metadata_only": True},
        provider_readiness=_ready_executor_provider_payload(),
        process_continuation_increment=1,
        next_autonomous_action="historical metadata probe",
    )
    legacy_dispatch_keys = (
        "kanban_run_created",
        "dispatch_performed",
        "execution_started",
        "worker_execution",
        "worker_process_started",
        "Kanban_dispatch",
        "lineage_dispatch_performed",
        "A2A_dispatch_performed",
    )
    for key in legacy_dispatch_keys:
        second.pop(key, None)
    second["current_invocation_side_effects"] = {
        key: value
        for key, value in second["current_invocation_side_effects"].items()
        if key not in legacy_dispatch_keys
    }
    second["human_smoke_marker"] = pr.PEPPER_LEGACY_GOVERNED_AUTONOMY_READY_MARKER
    second.pop("runtime_state_SHA256")
    second["runtime_state_SHA256"] = pr._governed_autonomy_runtime_record_digest(second)
    pr._persist_governed_autonomy_runtime_state(second)

    assert second["process_continuation_count"] == 2
    persisted = pr.load_current_ticket_governed_autonomy_runtime_state(
        projection_record=authority,
    )
    assert persisted is not None
    assert persisted["previous_runtime_state_SHA256"] == first["runtime_state_SHA256"]
    assert persisted["runtime_state_SHA256"] == second["runtime_state_SHA256"]
    assert "dispatch_performed" not in persisted
    status = pr.get_current_ticket_governed_autonomy_status(
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert status["governed_autonomy_runtime"]["runtime_state_SHA256"] == second[
        "runtime_state_SHA256"
    ]
    assert status["recorded_process_continuation_count"] == 2
    assert status["governed_autonomy_runtime"]["recorded_process_continuation_count"] == 2
    assert status["process_continuation_count"] == 0
    assert status["governed_autonomy_runtime"]["process_continuation_count"] == 0
    assert status["dispatch_performed"] is False
    assert status["governed_autonomy_runtime"]["dispatch_performed"] is False
    workflow = pr.build_workflow_control_snapshot()
    assert workflow["next_action"]["id"] == "CONTINUE_P18_9_1_GOVERNED_AUTONOMY"
    assert workflow["governed_autonomy"]["runtime_state_SHA256"] == second[
        "runtime_state_SHA256"
    ]
    assert workflow["governed_autonomy"]["recorded_process_continuation_count"] == 2
    assert workflow["governed_autonomy"]["process_continuation_count"] == 0

    _patch_synthetic_scratch_materialization(monkeypatch, pr)
    monkeypatch.setattr(kanban_db, "_pid_alive", lambda pid: int(pid) == 6606)
    resumed = pr.continue_current_ticket_governed_autonomy(
        runtime_goal="Resume with the first real direct governed continuation after restart.",
        strategy="DIRECT",
        spawn_fn=lambda _task, _workspace, board=None, env_overlay=None: 6606,
        project_id="PEPPER",
        ticket_id="P18.9.1",
    )
    assert resumed["previous_runtime_state_SHA256"] == second["runtime_state_SHA256"]
    assert resumed["process_continuation_count"] == 1
    assert resumed["recorded_process_continuation_count"] == 1
    assert resumed["kanban_run_id"] == run_4 + 1
    assert resumed["live_autonomous_continuation_marker"] == (
        pr.PEPPER_GOVERNED_AUTONOMY_LIVE_CONTINUATION_MARKER
    )

    conn = kanban_db.connect(board=projected["kanban_board_slug"])
    try:
        runs = kanban_db.list_runs(conn, projected["kanban_task_id"])
        assert runs[-2].id == run_4
        assert runs[-1].id == run_4 + 1
        assert runs[-1].status == "running"
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
        ("Acepto la review de P18.9.0", "exact explicit current-ticket review acceptance"),
        (
            "Acepto explícitamente la review de P18.9.1 y el resultado preparado para aceptación humana.",
            "exact explicit current-ticket review acceptance",
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
        ("Summarize P18.9.0", "explicit current-ticket review preparation"),
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
    monkeypatch.setattr(
        pr,
        "build_lead_agent_operational_context",
        lambda: {"current_ticket_id": "P18.9.0"},
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
