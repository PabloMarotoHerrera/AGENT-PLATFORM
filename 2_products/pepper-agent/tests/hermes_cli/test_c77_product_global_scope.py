"""Product HTTP authority against real isolated generation/projection/stores."""

import asyncio
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from hermes_cli import web_server as ws
from hermes_constants import (
    get_hermes_home,
    set_hermes_home_override,
    reset_hermes_home_override,
)
from tests.hermes_cli.test_c65_retry_material_revision import (
    flow as flow,
    projection_home as projection_home,
)
from tests.hermes_cli.test_c66_invalid_validation_command_revision import (
    evidence as evidence,
)
from tests.hermes_cli.test_c69_zero_change_decision import completed as completed

PROFILES = [
    "",
    "pepper-architecture-product",
    "pepper-implementation-product",
    "unknown-profile",
    "../../alternate",
]
pytestmark = pytest.mark.parametrize("flow", ["executable"], indirect=True)


@pytest.fixture
def product(completed, monkeypatch, tmp_path):
    from hermes_cli import profiles

    f = completed
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(profiles, "_get_profiles_root", lambda: f.home / "profiles")
    monkeypatch.setattr(profiles, "_get_default_hermes_home", lambda: f.home)
    for name in PROFILES[1:3]:
        home = f.home / "profiles" / name
        home.mkdir(parents=True, exist_ok=True)
        (home / "config.yaml").write_text(
            "model:\n  provider: unconfigured-test-provider\n  default: profile-chat-model\n"
        )
    f.client = TestClient(ws.app)
    f.client.headers[ws._SESSION_HEADER_NAME] = ws._SESSION_TOKEN
    return f


@pytest.mark.parametrize("selected", PROFILES)
def test_same_governed_authority_for_all_selector_values(product, selected):
    c = product.client
    expected = c.get("/api/agent-platform/workflow-control").json()
    actual = c.get("/api/agent-platform/workflow-control", params={"profile": selected})
    assert actual.status_code == 200, actual.text
    actual = actual.json()
    assert actual["current_ticket_id"] == product.p["ticket_id"]
    for key in [
        "project_id",
        "current_ticket_id",
        "workflow_status",
        "next_action",
        "approval_state",
        "execution_state",
        "validation_state",
        "review_state",
    ]:
        assert actual[key] == expected[key], key
    # The actual durable projection (including spec/WP hashes) is resolved
    # inside the HTTP handler, not copied into a synthetic mocked response.
    from hermes_cli.agent_platform import product_runtime as pr

    with ws._pepper_product_scope():
        p = pr._load_current_projection_record()
    for key in [
        "ticket_spec_SHA256",
        "work_packet_SHA256",
        "work_packet_id",
        "projection_SHA256",
    ]:
        assert p[key] == product.p[key]


@pytest.mark.parametrize("selected", PROFILES)
def test_execution_list_detail_and_prepare_use_product(product, selected):
    c, p = product.client, product.p
    params = {"board": p["kanban_board_slug"], "task": p["kanban_task_id"]}
    path = "/api/agent-platform/executions"
    expected = c.get(path, params=params)
    actual = c.get(path, params={**params, "profile": selected})
    assert actual.status_code == expected.status_code == 200
    assert actual.json() == expected.json()
    path += "/" + str(product.run_id)
    assert (
        c.get(path, params={**params, "profile": selected}).json()
        == c.get(path, params=params).json()
    )
    body = {"board_slug": params["board"], "task_id": params["task"]}
    expected = c.post("/api/agent-platform/executions/start", json=body)
    assert expected.status_code == 200, expected.text
    # A syntactically valid legacy body.profile is compatibility data only.
    actual = c.post(
        "/api/agent-platform/executions/start",
        params={"profile": selected},
        json={**body, "profile": "unknown-profile"},
    )
    assert actual.status_code == 200, actual.text
    assert actual.json() == expected.json()
    assert actual.json()["dispatch_performed"] is False


def test_approval_decision_cannot_write_into_named_store(product):
    from tools import write_approval as wa

    canonical = wa.stage_write(
        wa.MEMORY,
        {"action": "add", "content": "product"},
        summary="product approval",
        origin="foreground",
    )
    named = product.home / "profiles" / PROFILES[1]
    token = set_hermes_home_override(named)
    try:
        local = wa.stage_write(
            wa.MEMORY,
            {"action": "add", "content": "local"},
            summary="local approval",
            origin="foreground",
        )
    finally:
        reset_hermes_home_override(token)
    c = product.client
    expected = c.get("/api/agent-platform/approvals").json()
    for selected in PROFILES:
        assert (
            c.get("/api/agent-platform/approvals", params={"profile": selected}).json()
            == expected
        )
    path = "/api/agent-platform/approvals/" + canonical["id"]
    assert c.get(path, params={"profile": PROFILES[1]}).status_code == 200
    response = c.post(
        path + "/decision", params={"profile": PROFILES[1]}, json={"decision": "reject"}
    )
    assert response.status_code == 200, response.text
    assert wa.get_pending(wa.MEMORY, canonical["id"]) is None
    token = set_hermes_home_override(named)
    try:
        assert wa.get_pending(wa.MEMORY, local["id"]) is not None
    finally:
        reset_hermes_home_override(token)
    assert (
        c.post(
            "/api/agent-platform/approvals/" + local["id"] + "/decision",
            params={"profile": PROFILES[1]},
            json={"decision": "reject"},
        ).status_code
        == 404
    )


def test_nested_context_and_exception_restore_profile(product):
    named = product.home / "profiles" / PROFILES[1]
    token = set_hermes_home_override(named)
    try:
        with pytest.raises(RuntimeError):
            with ws._pepper_product_scope():
                assert get_hermes_home() == product.home
                raise RuntimeError("test")
        assert get_hermes_home() == named
        assert (
            ws.get_agent_platform_workflow_control(PROFILES[1])["current_ticket_id"]
            == product.p["ticket_id"]
        )
        assert get_hermes_home() == named
    finally:
        reset_hermes_home_override(token)


def test_status_scope_survives_await_without_affecting_profile_task(
    product, monkeypatch
):
    async def status(profile=None):
        assert profile is None
        await asyncio.sleep(0)
        return {"home": str(get_hermes_home())}

    monkeypatch.setattr(ws, "get_status", status)

    async def exercise():
        named = product.home / "profiles" / PROFILES[1]
        token = set_hermes_home_override(named)
        try:
            a, b = await asyncio.gather(
                ws.get_agent_platform_runtime_status(), status()
            )
            assert a["home"] == str(product.home)
            assert b["home"] == str(named)
        finally:
            reset_hermes_home_override(token)

    asyncio.run(exercise())


def test_profile_config_and_provider_deficiency_do_not_erase_workflow(product):
    c = product.client
    before = c.get("/api/agent-platform/workflow-control").json()
    for selected in PROFILES[1:3]:
        response = c.get("/api/config/raw", params={"profile": selected})
        assert response.status_code == 200, response.text
        assert "unconfigured-test-provider" in response.json()["yaml"]
        assert (
            c.get(
                "/api/agent-platform/workflow-control", params={"profile": selected}
            ).json()["current_ticket_id"]
            == before["current_ticket_id"]
        )


def test_governed_ticket_approval_is_the_same_human_boundary(
    product, monkeypatch, tmp_path
):
    from hermes_cli.agent_platform import product_runtime as pr
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge

    # A second, empty isolated product root proves this is not tied to the
    # completed fixture's ticket, revision or current state.
    home = tmp_path / "next-product"
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.setenv("HERMES_KANBAN_HOME", str(home))
    generated = pr.generate_current_governed_ticket(
        project_id="PEPPER", ticket_id="P18.9.0", next_action_id="GENERATE_P18_9_0"
    )
    path = "/api/agent-platform/approvals/" + generated["ticket_id"]
    c = product.client
    expected = c.get(path).json()
    assert expected["approval"]["request_type"] == "ticket_approval"
    for selected in PROFILES:
        assert c.get(path, params={"profile": selected}).json() == expected
    decision = c.post(
        path + "/decision",
        params={"profile": PROFILES[1]},
        json={"decision": "approve"},
    )
    assert decision.status_code == 200, decision.text
    assert decision.json()["ticket_execution_authorized"] is False
    assert bridge.load_generation_record(ticket_id=generated["ticket_id"])[
        "ticket_spec_SHA256"
    ]
    for selected in PROFILES:
        replay = c.post(
            path + "/decision",
            params={"profile": selected},
            json={"decision": "approve"},
        )
        assert replay.status_code == 200, replay.text
        assert replay.json()["idempotent_replay"] is True
