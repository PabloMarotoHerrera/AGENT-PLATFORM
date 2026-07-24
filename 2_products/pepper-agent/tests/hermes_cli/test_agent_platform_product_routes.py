"""Tests for the protected Pepper product-configuration dashboard boundary."""

import json

import pytest
from fastapi.testclient import TestClient

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
        "feature_flags": {"agent_platform.product_ui": "disabled"},
        "extension_modules": [],
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
    assert response.json()["feature_flags"]["agent_platform.product_ui"] == "disabled"


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_product_configuration_boundary_is_read_only(dashboard_client, method):
    response = getattr(dashboard_client, method)(
        "/api/agent-platform/product-configuration",
        headers=_auth_headers(),
    )

    assert response.status_code == 405
