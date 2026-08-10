"""Tests for the protected Pepper product-configuration dashboard boundary."""

import json
import warnings

import pytest
from fastapi.testclient import TestClient

warnings.filterwarnings(
    "ignore",
    message='Field "model_like" has conflict with protected namespace "model_".',
    category=UserWarning,
)

from hermes_cli.agent_platform.product_config import PRODUCT_UI_EXTENSION_MODULE_IDS
from hermes_cli import web_server


@pytest.fixture
def dashboard_client():
    previous_host = getattr(web_server.app.state, "bound_host", None)
    previous_port = getattr(web_server.app.state, "bound_port", None)
    previous_auth_required = getattr(web_server.app.state, "auth_required", None)
    web_server.app.state.bound_host = "127.0.0.1"
    web_server.app.state.bound_port = 9119
    web_server.app.state.auth_required = False
    client = TestClient(web_server.app, base_url="http://127.0.0.1:9119")
    yield client
    web_server.app.state.bound_host = previous_host
    web_server.app.state.bound_port = previous_port
    if previous_auth_required is None:
        delattr(web_server.app.state, "auth_required")
    else:
        web_server.app.state.auth_required = previous_auth_required


def _auth_headers():
    return {"X-Hermes-Session-Token": web_server._SESSION_TOKEN}


def test_integrated_route_returns_validated_credential_free_shape(dashboard_client):
    response = dashboard_client.get(
        "/api/agent-platform/product-configuration",
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "schema_version": 1,
        "product_id": "pepper",
        "product_display_name": "Pepper",
        "product_version": "0.1.0-dev",
        "upstream_product_name": "Hermes Agent",
        "upstream_version": "0.19.0",
        "upstream_commit": "3ef6bbd201263d354fd83ec55b3c306ded2eb72a",
        "feature_flags": {"agent_platform.product_ui": "enabled"},
        "extension_modules": list(PRODUCT_UI_EXTENSION_MODULE_IDS),
        "documentation_url": None,
        "support_url": None,
    }
    serialized = json.dumps(body).lower()
    assert all(
        term not in serialized
        for term in ("api_key", "token", "credential", "provider")
    )


def test_integrated_route_uses_existing_dashboard_authentication(dashboard_client):
    path = "/api/agent-platform/product-configuration"

    assert dashboard_client.get(path).status_code == 401
    response = dashboard_client.get(path, headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["feature_flags"]["agent_platform.product_ui"] == "enabled"
    assert response.json()["extension_modules"] == list(PRODUCT_UI_EXTENSION_MODULE_IDS)


def test_controlled_approval_routes_list_detail_and_reject(dashboard_client):
    from tools import write_approval as wa

    record = wa.stage_write(
        wa.MEMORY,
        {"action": "add", "target": "user", "content": "Remember bounded fact"},
        summary="Remember bounded fact",
        origin="foreground",
    )

    list_response = dashboard_client.get(
        "/api/agent-platform/approvals",
        headers=_auth_headers(),
    )
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["source_system"] == "hermes-write-approval"
    assert [item["id"] for item in body["approvals"]] == [record["id"]]
    assert "payload" not in json.dumps(body).lower()

    detail_response = dashboard_client.get(
        f"/api/agent-platform/approvals/{record['id']}",
        headers=_auth_headers(),
    )
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["approval"]["id"] == record["id"]
    assert detail["evidence"]

    decision_response = dashboard_client.post(
        f"/api/agent-platform/approvals/{record['id']}/decision",
        headers=_auth_headers(),
        json={"decision": "reject"},
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["status"] == "rejected"
    assert wa.get_pending(wa.MEMORY, record["id"]) is None


def test_controlled_execution_routes_project_universal_and_exact_sources(dashboard_client):
    from hermes_cli import kanban_db

    kanban_db.init_db()
    conn = kanban_db.connect()
    try:
        task_id = kanban_db.create_task(
            conn,
            title="Controlled execution route smoke",
            body="Bounded task body",
            created_by="test",
        )
        conn.execute(
            """
            INSERT INTO task_runs (
                task_id, profile, step_key, status, claim_lock, claim_expires,
                worker_pid, max_runtime_seconds, last_heartbeat_at, started_at,
                ended_at, outcome, summary, metadata, error
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                "review-profile",
                None,
                "done",
                "private-claim",
                None,
                12345,
                None,
                None,
                1_700_000_000,
                1_700_000_010,
                "completed",
                "private summary",
                json.dumps({"provider": "private"}),
                None,
            ),
        )
        conn.commit()
        run_id = conn.execute("SELECT id FROM task_runs WHERE task_id = ?", (task_id,)).fetchone()["id"]
    finally:
        conn.close()

    collection_response = dashboard_client.get(
        "/api/agent-platform/executions",
        headers=_auth_headers(),
    )
    assert collection_response.status_code == 200
    collection = collection_response.json()
    assert collection["source_system"] == "pepper-controlled-execution"
    assert collection["manual_opencode_copy_required"] is False
    assert collection["human_git_authority"] == "preserved"
    assert any(item["task_id"] == task_id and item["id"] == run_id for item in collection["executions"])
    assert "private-claim" not in json.dumps(collection)

    detail_response = dashboard_client.get(
        f"/api/agent-platform/executions/{run_id}?board=default&task={task_id}",
        headers=_auth_headers(),
    )
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["task"]["id"] == task_id
    assert detail["runs"][0]["id"] == run_id
    assert detail["control"]["git_handoff_state"] == "human_git_authority_preserved"
    assert detail["runs"][0]["claim_lock"] is None

    start_response = dashboard_client.post(
        "/api/agent-platform/executions/start",
        headers=_auth_headers(),
        json={"board_slug": "default", "task_id": task_id},
    )
    assert start_response.status_code == 200
    start = start_response.json()
    assert start["dispatch_performed"] is False
    assert start["manual_opencode_ticket_copy_required"] is False
    assert start["human_git_authority"] == "preserved"


def test_workflow_control_route_closes_p18_7_gaps_and_records_human_smoke(dashboard_client):
    response = dashboard_client.get(
        "/api/agent-platform/workflow-control",
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "controlled_default"
    assert body["manual_chat_control_required"] is False
    assert body["manual_opencode_ticket_copy_required"] is False
    assert body["manual_opencode_result_copy_required"] is False
    assert body["automatic_git_add"] is False
    assert body["automatic_git_commit"] is False
    assert body["automatic_git_push"] is False
    assert {gap["id"] for gap in body["closed_gaps"]} == {
        "P18-8-GAP-001",
        "P18-8-GAP-002",
        "P18-8-GAP-003",
        "P18-8-GAP-004",
        "P18-8-GAP-005",
    }
    assert body["remaining_blockers"] == []
    assert body["blocker_count"] == 0
    assert body["ready_requires_human_smoke"] is False
    assert body["human_cutover_smoke"] == "HUMAN_P18_8_CUTOVER_SMOKE_PASS"
    assert body["P18_R_ready"] is True
    assert body["next_action"]["id"] == "P18_R_READY_FOR_HUMAN_AUTHORIZATION"


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_product_configuration_boundary_is_read_only(dashboard_client, method):
    response = getattr(dashboard_client, method)(
        "/api/agent-platform/product-configuration",
        headers=_auth_headers(),
    )

    assert response.status_code == 405
