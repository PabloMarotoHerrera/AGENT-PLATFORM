"""Validated, credential-free AGENT PLATFORM product configuration."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    StringConstraints,
    field_validator,
)


StableIdentifier = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$"),
]
NonEmptyString = Annotated[str, StringConstraints(min_length=1)]
CommitSha = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{40}$")]


class FeatureState(StrEnum):
    """Serializable product capability states."""

    ENABLED = "enabled"
    DISABLED = "disabled"
    UNAVAILABLE = "unavailable"
    EXPERIMENTAL = "experimental"


class ProductConfiguration(BaseModel):
    """Safe product metadata consumed by AGENT PLATFORM UI surfaces."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1]
    product_id: StableIdentifier
    product_display_name: NonEmptyString
    product_version: NonEmptyString
    upstream_product_name: NonEmptyString
    upstream_version: NonEmptyString
    upstream_commit: CommitSha
    feature_flags: dict[StableIdentifier, FeatureState]
    extension_modules: tuple[StableIdentifier, ...]
    documentation_url: AnyHttpUrl | None
    support_url: AnyHttpUrl | None

    @field_validator("extension_modules")
    @classmethod
    def reject_duplicate_extensions(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("extension_modules must contain unique identifiers")
        return value

    @field_validator("documentation_url", "support_url")
    @classmethod
    def reject_url_credentials(cls, value: AnyHttpUrl | None) -> AnyHttpUrl | None:
        if value is not None and (
            value.username is not None or value.password is not None
        ):
            raise ValueError("product URLs must not contain credentials")
        return value


_PRODUCT_DEFAULTS = {
    "schema_version": 1,
    "product_id": "agent-platform-hermes",
    "product_display_name": "AGENT PLATFORM Hermes",
    "product_version": "0.1.0-dev",
    "upstream_product_name": "Hermes Agent",
    "upstream_version": "0.18.2",
    "upstream_commit": "9de9c25f620ff7f1ce0fd5457d596052d5159596",
    "feature_flags": {
        "agent_platform.product_ui": FeatureState.EXPERIMENTAL,
    },
    "extension_modules": (
        "agent_platform.ui.overview",
        "agent_platform.ui.projects",
        "agent_platform.ui.project_detail",
        "agent_platform.ui.ticket_detail",
        "agent_platform.ui.approvals",
        "agent_platform.ui.approval_detail",
        "agent_platform.ui.executions",
        "agent_platform.ui.execution_detail",
        "agent_platform.ui.settings",
    ),
    "documentation_url": None,
    "support_url": None,
}


def load_product_configuration() -> ProductConfiguration:
    """Return a newly validated copy of the tracked product defaults.

    P12.6 deliberately has no environment, user-config, managed-scope or
    provider override tier. Future sources require an explicit contract change.
    """

    return ProductConfiguration.model_validate(_PRODUCT_DEFAULTS)


def get_feature_state(
    configuration: ProductConfiguration,
    feature_id: str,
) -> FeatureState:
    """Resolve absent features to the safe disabled state."""

    return configuration.feature_flags.get(feature_id, FeatureState.DISABLED)
