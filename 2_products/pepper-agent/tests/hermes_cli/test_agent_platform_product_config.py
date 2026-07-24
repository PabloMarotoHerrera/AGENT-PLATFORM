"""Tests for the Pepper product configuration trust boundary."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.product_config import (
    FeatureState,
    ProductConfiguration,
    get_feature_state,
    load_product_configuration,
)


def test_tracked_defaults_form_the_validated_dual_version_contract():
    configuration = load_product_configuration()

    assert configuration.schema_version == 1
    assert configuration.product_id == "pepper"
    assert configuration.product_display_name == "Pepper"
    assert configuration.product_version == "0.1.0-dev"
    assert configuration.upstream_product_name == "Hermes Agent"
    assert configuration.upstream_version == "0.19.0"
    assert (
        configuration.upstream_commit
        == "3ef6bbd201263d354fd83ec55b3c306ded2eb72a"
    )
    assert (
        configuration.feature_flags["agent_platform.product_ui"]
        is FeatureState.DISABLED
    )
    assert configuration.extension_modules == ()


def test_absent_features_default_to_disabled():
    configuration = load_product_configuration()

    assert (
        get_feature_state(configuration, "agent_platform.future")
        is FeatureState.DISABLED
    )
    assert (
        get_feature_state(configuration, "agent_platform.product_ui")
        is FeatureState.DISABLED
    )


@pytest.mark.parametrize(
    "forbidden_field", ["api_key", "token", "providers", "credential_path"]
)
def test_unknown_secret_or_provider_fields_are_rejected(forbidden_field):
    payload = load_product_configuration().model_dump(mode="json")
    payload[forbidden_field] = "synthetic-value"

    with pytest.raises(ValidationError):
        ProductConfiguration.model_validate(payload)


def test_invalid_configuration_and_duplicate_extensions_are_rejected():
    payload = load_product_configuration().model_dump(mode="json")
    payload["schema_version"] = 2
    payload["extension_modules"] = [
        "agent_platform.example",
        "agent_platform.example",
    ]

    with pytest.raises(ValidationError):
        ProductConfiguration.model_validate(payload)


@pytest.mark.parametrize("url_field", ["documentation_url", "support_url"])
def test_product_urls_reject_embedded_credentials(url_field):
    payload = load_product_configuration().model_dump(mode="json")
    payload[url_field] = (
        "https://synthetic-user:synthetic-password@example.invalid/docs"
    )

    with pytest.raises(ValidationError):
        ProductConfiguration.model_validate(payload)


def test_environment_and_user_configuration_have_no_precedence(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    hermes_home.mkdir()
    (hermes_home / "config.yaml").write_text(
        "product_display_name: synthetic-user-override\n",
        encoding="utf-8",
    )
    before = set(Path(hermes_home).iterdir())
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setenv("AGENT_PLATFORM_PRODUCT_DISPLAY_NAME", "synthetic-env-override")

    configuration = load_product_configuration()

    assert configuration.product_display_name == "Pepper"
    assert set(Path(hermes_home).iterdir()) == before
