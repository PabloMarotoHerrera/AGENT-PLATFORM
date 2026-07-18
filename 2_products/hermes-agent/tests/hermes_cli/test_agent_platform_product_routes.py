"""Tests for the protected product-configuration dashboard boundary."""

import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from hermes_cli import web_server
from hermes_cli.agent_platform.routes import router


ACTIVATED_PRODUCT_MODULES = [
    "agent_platform.ui.overview",
    "agent_platform.ui.projects",
    "agent_platform.ui.project_detail",
    "agent_platform.ui.ticket_detail",
    "agent_platform.ui.approvals",
    "agent_platform.ui.approval_detail",
    "agent_platform.ui.executions",
    "agent_platform.ui.execution_detail",
    "agent_platform.ui.settings",
]


@pytest.fixture
def dashboard_client():
    previous_host = getattr(web_server.app.state, "bound_host", None)
    previous_port = getattr(web_server.app.state, "bound_port", None)
    web_server.app.state.bound_host = "127.0.0.1"
    web_server.app.state.bound_port = 9119
    client = TestClient(web_server.app, base_url="http://127.0.0.1:9119")
    yield client
    web_server.app.state.bound_host = previous_host
    web_server.app.state.bound_port = previous_port


def test_standalone_route_returns_validated_credential_free_shape():
    app = FastAPI()
    app.include_router(router)

    response = TestClient(app).get("/api/agent-platform/product-configuration")

    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == 1
    assert body["product_id"] == "agent-platform-hermes"
    assert set(body) == {
        "schema_version",
        "product_id",
        "product_display_name",
        "product_version",
        "upstream_product_name",
        "upstream_version",
        "upstream_commit",
        "feature_flags",
        "extension_modules",
        "documentation_url",
        "support_url",
    }
    assert body["feature_flags"]["agent_platform.product_ui"] == "experimental"
    assert body["extension_modules"] == ACTIVATED_PRODUCT_MODULES
    serialized = json.dumps(body).lower()
    assert all(
        term not in serialized
        for term in ("api_key", "token", "credential", "provider")
    )


def test_integrated_route_uses_existing_dashboard_authentication(dashboard_client):
    path = "/api/agent-platform/product-configuration"

    assert dashboard_client.get(path).status_code == 401
    response = dashboard_client.get(
        path,
        headers={"X-Hermes-Session-Token": web_server._SESSION_TOKEN},
    )
    assert response.status_code == 200
    assert (
        response.json()["feature_flags"]["agent_platform.product_ui"] == "experimental"
    )


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_product_configuration_boundary_is_read_only(method):
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    assert (
        getattr(client, method)("/api/agent-platform/product-configuration").status_code
        == 405
    )
