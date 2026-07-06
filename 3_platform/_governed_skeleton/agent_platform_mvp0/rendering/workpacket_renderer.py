"""Compact WorkPacket renderer for MVP-0.

The renderer returns strings only. It performs no file I/O, no filesystem
traversal, no subprocess calls, no shell execution, no network/API/MCP/provider
calls, no harness execution, no source inspection, no persistence, and no Git
mutation.
"""

from __future__ import annotations

from typing import Tuple

from .contracts import (
    CompactWorkPacket,
    RenderFormat,
    RenderResult,
    RenderedPackage,
    RendererConfig,
)
from .markdown_sections import (
    allowed_scope_section,
    blocked_scope_section,
    boundary_block_section,
    context_refs_section,
    document_title,
    evidence_refs_section,
    expected_outputs_section,
    generic_section,
    limitations_section,
    mandatory_inputs_section,
    metadata_table,
    not_created_register_section,
    objective_section,
    optional_inputs_section,
    paragraph_section,
    path_scope_section,
    reporting_format_section,
    stop_rules_section,
)


_REQUIRED_WORKPACKET_STATEMENTS: Tuple[str, ...] = (
    "This WorkPacket is manual execution only.",
    "This WorkPacket is not automatic dispatch.",
    "This WorkPacket does not activate agent runtime.",
    "This WorkPacket does not execute tools/providers/MCP.",
    "This WorkPacket does not mutate Git.",
    "User remains final execution and Git authority.",
)

_DEFAULT_NOT_CREATED: Tuple[str, ...] = (
    "no HarnessOutputPackage intake",
    "no review checklist execution",
    "no IntegrationSummary rendering",
    "no CommitCandidate rendering",
    "no harness execution",
    "no OpenCode execution from AGENT PLATFORM",
    "no provider/auth/API/MCP activation",
    "no source loading or source inspection",
    "no product/Siamese source inspection",
    "no external source content inspection",
    "no persistence/vector DB/graph DB/embeddings",
    "no Git mutation",
)


def _clean_items(items: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(str(item).strip() for item in items if str(item).strip())


def _remove_disallowed_git_add(items: Tuple[str, ...]) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    safe_items = []
    warnings = []
    for item in _clean_items(items):
        if "git add ." in item.casefold():
            warnings.append("Removed broad Git staging command from allowed rendered content.")
            continue
        safe_items.append(item)
    return tuple(safe_items), tuple(warnings)


def _warnings_for_packet(work_packet: CompactWorkPacket) -> Tuple[str, ...]:
    warnings = []
    if not work_packet.target_artifacts:
        warnings.append("Target artifacts not supplied; rendered package cannot invent targets.")
    if not work_packet.path_scope.allowed_paths:
        warnings.append("Allowed paths unknown; rendered package warns instead of inventing paths.")
    if not work_packet.path_scope.blocked_paths:
        warnings.append("Blocked paths missing; conservative default blockers are rendered.")
    if not work_packet.blocked_scope:
        warnings.append("Blocked scope missing; conservative warning is rendered.")
    return tuple(warnings)


def render_compact_workpacket(
    work_packet: CompactWorkPacket,
    config: RendererConfig | None = None,
) -> RenderResult:
    """Render a CompactWorkPacket as inert markdown/text."""

    effective_config = config or RendererConfig()
    safe_allowed_scope, git_warnings = _remove_disallowed_git_add(work_packet.allowed_scope)
    safe_allowed_paths, path_git_warnings = _remove_disallowed_git_add(
        work_packet.path_scope.allowed_paths
    )
    warnings = _warnings_for_packet(work_packet) + git_warnings + path_git_warnings
    not_created = _DEFAULT_NOT_CREATED + _clean_items(work_packet.not_created_register)
    limitations = _clean_items(work_packet.limitations) or (
        "Rendered text is advisory and manual only.",
        "Rendering does not dispatch, execute, review, integrate, persist, or mutate Git.",
    )
    blockers = _clean_items(work_packet.boundary_block.statements) + _clean_items(
        work_packet.stop_rule_block.stop_rules
    )

    sections = [
        document_title(work_packet.title or "Compact WorkPacket"),
        metadata_table(
            (
                ("Package kind", "CompactWorkPacket"),
                ("Ticket / WorkPacket ID", work_packet.work_packet_id),
                ("Platform", effective_config.platform_name),
                ("Product vision", effective_config.product_vision_name),
                ("Render posture", effective_config.safety_posture.value),
                ("Render format", effective_config.render_format.value),
            )
        ),
        objective_section(work_packet.objective),
        paragraph_section("Scope", work_packet.scope),
        generic_section("Target artifacts", work_packet.target_artifacts, "target artifacts not supplied"),
        allowed_scope_section(safe_allowed_scope),
        blocked_scope_section(work_packet.blocked_scope),
        mandatory_inputs_section(work_packet.mandatory_inputs),
        optional_inputs_section(work_packet.optional_inputs),
        context_refs_section(
            work_packet.context_refs.mandatory_context_refs,
            work_packet.context_refs.optional_context_refs,
            work_packet.context_refs.forbidden_context_refs,
            work_packet.context_refs.memory_refs,
        ),
        evidence_refs_section(
            work_packet.evidence_refs,
            work_packet.validation_refs,
            work_packet.security_refs,
        ),
        path_scope_section(safe_allowed_paths, work_packet.path_scope.blocked_paths),
        generic_section("Harness expectations", work_packet.harness_expectations, "harness expectations not supplied; harness remains manual"),
        generic_section("Acceptance criteria", work_packet.acceptance_criteria, "acceptance criteria not supplied"),
        boundary_block_section(_REQUIRED_WORKPACKET_STATEMENTS + work_packet.boundary_block.statements),
        stop_rules_section(work_packet.stop_rule_block.stop_rules),
        expected_outputs_section(work_packet.expected_outputs),
        reporting_format_section(work_packet.reporting_format.expected_headings),
        not_created_register_section(not_created),
        limitations_section(limitations),
    ]
    rendered_text = "\n\n".join(sections).strip() + "\n"
    rendered_package = RenderedPackage(
        package_kind="CompactWorkPacket",
        rendered_text=rendered_text,
        render_format=effective_config.render_format,
        safety_posture=effective_config.safety_posture,
    )
    return RenderResult(
        rendered_text=rendered_text,
        render_format=effective_config.render_format,
        package_kind="CompactWorkPacket",
        warnings=warnings,
        blockers=blockers,
        not_created_register=not_created,
        limitations=limitations,
        rendered_package=rendered_package,
    )
