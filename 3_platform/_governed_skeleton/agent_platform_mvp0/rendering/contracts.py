"""Stdlib-only contracts for inert MVP-0 package rendering.

These contracts are render metadata only. They do not read files, write files,
traverse the filesystem, execute commands, call networks, call providers,
activate MCP, execute harnesses, execute OpenCode, execute Graphify, activate
GBrain/GStack/Hermes, inspect source, persist state, or mutate Git.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple


class RenderFormat(str, Enum):
    """Supported inert render formats."""

    MARKDOWN = "markdown"
    TEXT = "text"


class RenderSafetyPosture(str, Enum):
    """Renderer safety posture vocabulary."""

    LOCAL_INERT_TEMPLATE_RENDERING_ONLY = "local_inert_template_rendering_only"
    NO_HARNESS_EXECUTION = "no_harness_execution"
    NO_EXTERNAL_RUNTIME_ACTIVATION = "no_external_runtime_activation"
    NO_GIT_MUTATION = "no_git_mutation"


@dataclass(frozen=True)
class RendererConfig:
    """Configuration for inert rendering only."""

    render_format: RenderFormat = RenderFormat.MARKDOWN
    platform_name: str = "AGENT PLATFORM"
    product_vision_name: str = "Siamese"
    safety_posture: RenderSafetyPosture = (
        RenderSafetyPosture.LOCAL_INERT_TEMPLATE_RENDERING_ONLY
    )
    include_boundary_block: bool = True
    include_stop_rules: bool = True
    include_not_created_register: bool = True
    no_runtime_activation: bool = True
    no_harness_execution: bool = True
    no_provider_auth_api_mcp: bool = True
    no_git_mutation: bool = True
    no_product_source_inspection: bool = True
    no_source_loading: bool = True
    no_external_source_inspection: bool = True
    no_external_candidate_execution: bool = True


@dataclass(frozen=True)
class RenderBoundaryBlock:
    """Boundary statements that must travel with rendered packages."""

    statements: Tuple[str, ...] = (
        "No runtime activation is approved.",
        "No automatic dispatch is approved.",
        "No harness execution is approved.",
        "No OpenCode execution from AGENT PLATFORM is approved.",
        "No provider/auth/API/MCP activation is approved.",
        "No tool execution is approved.",
        "No agent execution is approved.",
        "No source loading or source inspection is approved.",
        "No product/Siamese source inspection is approved.",
        "No external source content inspection is approved.",
        "No Graphify/GBrain/GStack/Hermes execution is approved.",
        "No persistence, vector DB, graph DB, or embeddings are approved.",
        "No Git mutation is approved.",
        "Never use git add .",
    )


@dataclass(frozen=True)
class StopRuleBlock:
    """Stop rules rendered into WorkPackets and harness packages."""

    stop_rules: Tuple[str, ...] = (
        "Stop if work requires harness execution or automatic dispatch.",
        "Stop if work requires provider/auth/API/MCP activation.",
        "Stop if work requires tool, agent, task, or handoff execution.",
        "Stop if work requires source loading or source inspection.",
        "Stop if work requires product/Siamese source inspection.",
        "Stop if work requires external source content inspection.",
        "Stop if work requires secrets, credentials, .env, provider configs, token stores, browser auth, local credential stores, or API keys.",
        "Stop if work requires Graphify/GBrain/GStack/Hermes/OpenCode execution, import, configuration, adoption, runtime, or Cadence.",
        "Stop if work requires persistence, vector DB, embeddings, graph DB, ontology runtime, telemetry, or event streaming.",
        "Stop if work requires generated output tracking, source tracking expansion, publication, or Git mutation.",
        "Stop if work would render or treat git add . as an allowed command.",
    )


@dataclass(frozen=True)
class ContextRefBlock:
    """Context and memory reference metadata for rendering."""

    mandatory_context_refs: Tuple[str, ...] = ()
    optional_context_refs: Tuple[str, ...] = ()
    forbidden_context_refs: Tuple[str, ...] = (
        "secrets and credentials",
        ".env and provider auth material",
        "product/Siamese source",
        "external source contents",
        "raw generated outputs",
    )
    memory_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class PathScopeBlock:
    """Allowed and blocked paths supplied by an already validated caller."""

    allowed_paths: Tuple[str, ...] = ()
    blocked_paths: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ReportingFormatBlock:
    """Expected response headings for manual output."""

    expected_headings: Tuple[str, ...] = (
        "Summary",
        "Files changed",
        "Verification",
        "Risks and blockers",
        "Next steps",
    )


@dataclass(frozen=True)
class ManualHarnessInstructionBlock:
    """Manual harness instructions for H0/H1 package rendering."""

    instructions: Tuple[str, ...] = (
        "The user manually copies this package into the external harness.",
        "AGENT PLATFORM does not execute the harness.",
        "AGENT PLATFORM does not dispatch this package automatically.",
        "The harness output must be pasted back manually.",
        "Harness output is not trusted until reviewed.",
        "No Git mutation is allowed by this package.",
        "Never use git add .",
    )


@dataclass(frozen=True)
class CompactWorkPacket:
    """Canonical compact WorkPacket renderable object."""

    work_packet_id: str
    title: str
    objective: str
    scope: str
    target_artifacts: Tuple[str, ...] = ()
    allowed_scope: Tuple[str, ...] = ()
    blocked_scope: Tuple[str, ...] = ()
    mandatory_inputs: Tuple[str, ...] = ()
    optional_inputs: Tuple[str, ...] = ()
    context_refs: ContextRefBlock = field(default_factory=ContextRefBlock)
    evidence_refs: Tuple[str, ...] = ()
    validation_refs: Tuple[str, ...] = ()
    security_refs: Tuple[str, ...] = ()
    path_scope: PathScopeBlock = field(default_factory=PathScopeBlock)
    boundary_block: RenderBoundaryBlock = field(default_factory=RenderBoundaryBlock)
    stop_rule_block: StopRuleBlock = field(default_factory=StopRuleBlock)
    harness_expectations: Tuple[str, ...] = ()
    acceptance_criteria: Tuple[str, ...] = ()
    reporting_format: ReportingFormatBlock = field(default_factory=ReportingFormatBlock)
    expected_outputs: Tuple[str, ...] = ()
    not_created_register: Tuple[str, ...] = ()
    limitations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class HarnessInputPackage:
    """Canonical harness input package object for manual external harness use."""

    package_id: str
    harness_target: str
    harness_level: str = "H0_user_operated_harness"
    work_packet_ref: str = "work_packet_ref_metadata_only"
    prompt_body: str = ""
    mandatory_context_refs: Tuple[str, ...] = ()
    forbidden_context_refs: Tuple[str, ...] = ()
    path_scope: PathScopeBlock = field(default_factory=PathScopeBlock)
    expected_outputs: Tuple[str, ...] = ()
    reporting_format: ReportingFormatBlock = field(default_factory=ReportingFormatBlock)
    boundary_block: RenderBoundaryBlock = field(default_factory=RenderBoundaryBlock)
    stop_rule_block: StopRuleBlock = field(default_factory=StopRuleBlock)
    manual_harness_instructions: ManualHarnessInstructionBlock = field(
        default_factory=ManualHarnessInstructionBlock
    )
    not_created_register: Tuple[str, ...] = ()
    limitations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RenderedPackage:
    """Canonical renderer output object."""

    package_kind: str
    rendered_text: str
    render_format: RenderFormat = RenderFormat.MARKDOWN
    safety_posture: RenderSafetyPosture = (
        RenderSafetyPosture.LOCAL_INERT_TEMPLATE_RENDERING_ONLY
    )


@dataclass(frozen=True)
class RenderResult:
    """Canonical render operation output."""

    rendered_text: str
    render_format: RenderFormat
    package_kind: str
    warnings: Tuple[str, ...] = ()
    blockers: Tuple[str, ...] = ()
    not_created_register: Tuple[str, ...] = ()
    limitations: Tuple[str, ...] = ()
    rendered_package: RenderedPackage | None = None
