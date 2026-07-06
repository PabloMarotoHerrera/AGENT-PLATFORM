"""Inert boundary metadata for MVP-0.

This module defines blocked surfaces only. It performs no runtime
initialization, reads no files, executes no commands, calls no network,
creates no adapters, persists no state, and mutates no Git.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .contracts import Mvp0ActivationLevel, Mvp0BlockedReason


@dataclass(frozen=True)
class Mvp0BoundaryPolicy:
    """Package-level boundary metadata for the non-executing MVP-0 skeleton."""

    policy_id: str = "mvp0_boundary_policy_metadata_only"
    activation_level: Mvp0ActivationLevel = Mvp0ActivationLevel.P8_L2_LOCAL_NON_EXECUTING_SURFACE
    allowed_posture: str = "metadata-only, non-executing, human-reviewed"
    blocked_surface_names: Tuple[str, ...] = ()
    blocked_reasons: Tuple[Mvp0BlockedReason, ...] = ()
    human_review_required: bool = True


_BLOCKED_SURFACES: Tuple[str, ...] = (
    "runtime activation",
    "autonomous orchestration",
    "automatic dispatch",
    "automatic reviewer assignment",
    "automatic integration",
    "Git mutation",
    "git add .",
    "provider/auth/API/MCP - no provider and no MCP",
    "credentials/secrets/.env",
    "OpenCode execution - no OpenCode execution",
    "Graphify execution/rerun - no Graphify execution",
    "GBrain runtime",
    "GStack execution",
    "Hermes runtime",
    "Cadence",
    "live connectors",
    "product/Siamese source",
    "external source content inspection",
    "persistence DB",
    "vector DB / graph DB",
    "telemetry/event streaming",
    "Cognitive Semantic System substrate selection",
    "Git boundary - no Git mutation",
)

_BLOCKED_REASONS: Tuple[Mvp0BlockedReason, ...] = (
    Mvp0BlockedReason.RUNTIME_ACTIVATION_BLOCKED,
    Mvp0BlockedReason.AUTONOMOUS_ORCHESTRATION_BLOCKED,
    Mvp0BlockedReason.AUTOMATIC_DISPATCH_BLOCKED,
    Mvp0BlockedReason.AUTOMATIC_REVIEW_BLOCKED,
    Mvp0BlockedReason.AUTOMATIC_INTEGRATION_BLOCKED,
    Mvp0BlockedReason.GIT_MUTATION_BLOCKED,
    Mvp0BlockedReason.PROVIDER_API_MCP_BLOCKED,
    Mvp0BlockedReason.CREDENTIAL_USE_BLOCKED,
    Mvp0BlockedReason.OPENCODE_EXECUTION_BLOCKED,
    Mvp0BlockedReason.GRAPHIFY_EXECUTION_BLOCKED,
    Mvp0BlockedReason.GBRAIN_RUNTIME_BLOCKED,
    Mvp0BlockedReason.GSTACK_EXECUTION_BLOCKED,
    Mvp0BlockedReason.HERMES_RUNTIME_BLOCKED,
    Mvp0BlockedReason.CADENCE_BLOCKED,
    Mvp0BlockedReason.LIVE_CONNECTOR_BLOCKED,
    Mvp0BlockedReason.PRODUCT_SOURCE_BLOCKED,
    Mvp0BlockedReason.SOURCE_LOADING_BLOCKED,
    Mvp0BlockedReason.PERSISTENCE_BLOCKED,
    Mvp0BlockedReason.VECTOR_GRAPH_DB_BLOCKED,
    Mvp0BlockedReason.SUBSTRATE_SELECTION_BLOCKED,
)

DEFAULT_MVP0_BOUNDARY_POLICY = Mvp0BoundaryPolicy(
    blocked_surface_names=_BLOCKED_SURFACES,
    blocked_reasons=_BLOCKED_REASONS,
)


def blocked_surfaces() -> Tuple[str, ...]:
    """Return blocked surface names without reading files or executing tools."""

    return DEFAULT_MVP0_BOUNDARY_POLICY.blocked_surface_names


def is_surface_blocked(surface_name: str) -> bool:
    """Return whether a named surface is blocked by inert metadata."""

    normalized = surface_name.casefold()
    return any(normalized in item.casefold() for item in _BLOCKED_SURFACES)
