"""HarnessInputPackage renderer for manual H0/H1 harness use.

The renderer returns strings only. It performs no file I/O, no filesystem
traversal, no subprocess calls, no shell execution, no network/API/MCP/provider
calls, no harness execution, no OpenCode execution, no source inspection, no
persistence, and no Git mutation.
"""

from __future__ import annotations

from typing import Tuple

from .contracts import HarnessInputPackage, RenderResult, RenderedPackage, RendererConfig
from .markdown_sections import (
    boundary_block_section,
    document_title,
    expected_outputs_section,
    generic_section,
    limitations_section,
    manual_harness_instruction_section,
    metadata_table,
    not_created_register_section,
    paragraph_section,
    path_scope_section,
    reporting_format_section,
    stop_rules_section,
)


H0_USER_OPERATED_HARNESS = "H0_user_operated_harness"
H1_METADATA_ADAPTER_DESIGN = "H1_metadata_adapter_design"
H2_CONTROLLED_EXECUTION_ADAPTER_BLOCKED = "H2_controlled_execution_adapter_blocked"
H3_AUTONOMOUS_ORCHESTRATION_ADAPTER_BLOCKED = "H3_autonomous_orchestration_adapter_blocked"

_ALLOWED_LEVELS: Tuple[str, ...] = (H0_USER_OPERATED_HARNESS, H1_METADATA_ADAPTER_DESIGN)
_BLOCKED_LEVELS: Tuple[str, ...] = (
    H2_CONTROLLED_EXECUTION_ADAPTER_BLOCKED,
    H3_AUTONOMOUS_ORCHESTRATION_ADAPTER_BLOCKED,
)

_DEFAULT_NOT_CREATED: Tuple[str, ...] = (
    "no harness execution",
    "no OpenCode execution from AGENT PLATFORM",
    "no adapter implementation",
    "no executable adapter",
    "no automatic dispatch",
    "no HarnessOutputPackage intake",
    "no review checklist execution",
    "no integration checklist execution",
    "no CommitCandidate rendering",
    "no provider/auth/API/MCP activation",
    "no source loading or source inspection",
    "no product/Siamese source inspection",
    "no external source content inspection",
    "no Git mutation",
)

_DEFAULT_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "The user manually copies this package into the external harness.",
    "AGENT PLATFORM does not execute the harness.",
    "AGENT PLATFORM does not dispatch this package automatically.",
    "The harness output must be pasted back manually.",
    "Harness output is not trusted until reviewed.",
    "No Git mutation is allowed by this package.",
    "Never use git add .",
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


def _target_warnings(target: str, requested_level: str) -> Tuple[str, ...]:
    normalized = target.casefold()
    warnings = []
    if normalized == "opencode" and requested_level != H0_USER_OPERATED_HARNESS:
        warnings.append("OpenCode is rendered as H0 manual unless a later exact gate authorizes otherwise.")
    if "hermes" in normalized:
        warnings.append("Hermes runtime/Cadence is blocked; any Hermes reference is manual or conceptual only.")
    if any(token in normalized for token in ("provider", "auth", "api", "mcp")):
        warnings.append("Target harness implies provider/auth/API/MCP; activation remains blocked.")
    return tuple(warnings)


def _effective_level(target: str, requested_level: str) -> str:
    if target.casefold() == "opencode" and requested_level not in _BLOCKED_LEVELS:
        return H0_USER_OPERATED_HARNESS
    return requested_level


def _level_blockers(level: str) -> Tuple[str, ...]:
    if level in _BLOCKED_LEVELS:
        return (f"{level} is blocked and must not execute.",)
    if level not in _ALLOWED_LEVELS:
        return (f"Unknown harness level {level}; treat as blocked until reviewed.",)
    if level == H1_METADATA_ADAPTER_DESIGN:
        return ("H1 is metadata adapter design only; no adapter implementation or execution.",)
    return ()


def render_harness_input_package(
    package: HarnessInputPackage,
    config: RendererConfig | None = None,
) -> RenderResult:
    """Render a HarnessInputPackage for manual copy/paste use."""

    effective_config = config or RendererConfig()
    requested_level = package.harness_level or H0_USER_OPERATED_HARNESS
    level = _effective_level(package.harness_target, requested_level)
    safe_allowed_paths, path_git_warnings = _remove_disallowed_git_add(
        package.path_scope.allowed_paths
    )
    warnings = (
        _target_warnings(package.harness_target, requested_level)
        + path_git_warnings
    )
    if level in _BLOCKED_LEVELS:
        warnings += (f"{level} is blocked and rendered as non-executable.",)
    elif level not in _ALLOWED_LEVELS:
        warnings += (f"Unknown harness level {level}; rendered as blocked until reviewed.",)
    if not package.path_scope.allowed_paths:
        warnings += ("Allowed paths unknown; rendered package warns instead of inventing paths.",)
    if not package.path_scope.blocked_paths:
        warnings += ("Blocked paths missing; conservative default blockers are rendered.",)
    if not package.prompt_body.strip():
        warnings += ("Prompt body is empty; package is incomplete for manual harness use.",)
    blockers = _level_blockers(level) + _clean_items(package.boundary_block.statements) + _clean_items(
        package.stop_rule_block.stop_rules
    )
    not_created = _DEFAULT_NOT_CREATED + _clean_items(package.not_created_register)
    limitations = _clean_items(package.limitations) or (
        "Rendered package is manual copy/paste text only.",
        "Harness output remains untrusted until future manual intake and review.",
    )

    sections = [
        document_title(f"HarnessInputPackage - {package.harness_target}"),
        metadata_table(
            (
                ("Package kind", "HarnessInputPackage"),
                ("Package ID", package.package_id),
                ("Harness target", package.harness_target),
                ("Harness level", level),
                ("Requested harness level", requested_level),
                ("WorkPacket reference", package.work_packet_ref),
                ("Platform", effective_config.platform_name),
                ("Render posture", effective_config.safety_posture.value),
            )
        ),
        generic_section("Harness level boundary", _level_blockers(level) or ("H0/H1 manual or design-only rendering posture preserved.",), "harness level boundary missing; treat as blocked"),
        generic_section("Renderer warnings", warnings, "no renderer warnings"),
        manual_harness_instruction_section(
            _DEFAULT_BOUNDARY_STATEMENTS + package.manual_harness_instructions.instructions
        ),
        paragraph_section("Prompt body", package.prompt_body),
        generic_section("Mandatory context refs", package.mandatory_context_refs, "mandatory context refs not supplied"),
        generic_section("Forbidden context refs", package.forbidden_context_refs, "forbidden context refs not supplied; conservative blockers apply"),
        path_scope_section(safe_allowed_paths, package.path_scope.blocked_paths),
        expected_outputs_section(package.expected_outputs),
        stop_rules_section(package.stop_rule_block.stop_rules),
        reporting_format_section(package.reporting_format.expected_headings),
        boundary_block_section(_DEFAULT_BOUNDARY_STATEMENTS + package.boundary_block.statements),
        not_created_register_section(not_created),
        limitations_section(limitations),
    ]
    rendered_text = "\n\n".join(sections).strip() + "\n"
    rendered_package = RenderedPackage(
        package_kind="HarnessInputPackage",
        rendered_text=rendered_text,
        render_format=effective_config.render_format,
        safety_posture=effective_config.safety_posture,
    )
    return RenderResult(
        rendered_text=rendered_text,
        render_format=effective_config.render_format,
        package_kind="HarnessInputPackage",
        warnings=warnings,
        blockers=blockers,
        not_created_register=not_created,
        limitations=limitations,
        rendered_package=rendered_package,
    )
