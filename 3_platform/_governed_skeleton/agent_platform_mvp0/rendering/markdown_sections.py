"""Pure markdown section helpers for inert MVP-0 rendering."""

from __future__ import annotations

from typing import Iterable, Tuple


_CONSERVATIVE_BLOCKED_PATHS: Tuple[str, ...] = (
    "product/Siamese source",
    "external source contents",
    "4_external/sources contents",
    "raw generated outputs",
    "secrets and credentials",
    ".env and provider auth material",
    "token stores, browser auth, local credential stores, and API keys",
    "Git mutation paths or broad staging commands",
)


def _clean(value: object) -> str:
    return str(value).replace("\r", " ").replace("\n", " ").strip()


def _bullet_lines(items: Iterable[object], warning: str) -> str:
    values = tuple(_clean(item) for item in items if _clean(item))
    if not values:
        return f"- WARNING: {warning}"
    return "\n".join(f"- {item}" for item in values)


def document_title(title: str) -> str:
    return f"# {_clean(title)}"


def metadata_table(rows: Iterable[Tuple[str, object]]) -> str:
    lines = ["| Field | Value |", "| --- | --- |"]
    for key, value in rows:
        safe_key = _clean(key).replace("|", "\\|")
        safe_value = _clean(value).replace("|", "\\|")
        lines.append(f"| {safe_key} | {safe_value} |")
    return "\n".join(lines)


def generic_section(title: str, items: Iterable[object], warning: str) -> str:
    return f"## {_clean(title)}\n\n{_bullet_lines(items, warning)}"


def paragraph_section(title: str, text: str) -> str:
    body = _clean(text) or "WARNING: no content supplied."
    return f"## {_clean(title)}\n\n{body}"


def objective_section(objective: str) -> str:
    return paragraph_section("Objective", objective)


def allowed_scope_section(items: Iterable[object]) -> str:
    return generic_section("Allowed scope", items, "allowed scope unknown; do not infer permission")


def blocked_scope_section(items: Iterable[object]) -> str:
    return generic_section(
        "Blocked scope",
        items,
        "blocked scope missing; apply conservative default blockers",
    )


def mandatory_inputs_section(items: Iterable[object]) -> str:
    return generic_section("Mandatory inputs", items, "mandatory inputs not supplied")


def optional_inputs_section(items: Iterable[object]) -> str:
    return generic_section("Optional inputs", items, "optional inputs not supplied")


def context_refs_section(
    mandatory_refs: Iterable[object],
    optional_refs: Iterable[object] = (),
    forbidden_refs: Iterable[object] = (),
    memory_refs: Iterable[object] = (),
) -> str:
    sections = [
        "## Context / Memory refs",
        "",
        "### Mandatory context refs",
        _bullet_lines(mandatory_refs, "mandatory context refs not supplied"),
        "",
        "### Optional context refs",
        _bullet_lines(optional_refs, "optional context refs not supplied"),
        "",
        "### Memory refs",
        _bullet_lines(memory_refs, "memory refs not supplied; no memory runtime is implied"),
        "",
        "### Forbidden context refs",
        _bullet_lines(forbidden_refs, "forbidden refs not supplied; apply conservative blockers"),
    ]
    return "\n".join(sections)


def evidence_refs_section(
    evidence_refs: Iterable[object],
    validation_refs: Iterable[object] = (),
    security_refs: Iterable[object] = (),
) -> str:
    sections = [
        "## Evidence / Validation / Security refs",
        "",
        "### Evidence refs",
        _bullet_lines(evidence_refs, "evidence refs not supplied; evidence does not decide"),
        "",
        "### Validation refs",
        _bullet_lines(validation_refs, "validation refs not supplied; no validation is executed"),
        "",
        "### Security refs",
        _bullet_lines(security_refs, "security refs not supplied; security blockers remain active"),
    ]
    return "\n".join(sections)


def path_scope_section(allowed_paths: Iterable[object], blocked_paths: Iterable[object]) -> str:
    blocked = tuple(_clean(item) for item in blocked_paths if _clean(item))
    if not blocked:
        blocked = _CONSERVATIVE_BLOCKED_PATHS
    sections = [
        "## Path scope",
        "",
        "### Allowed paths",
        _bullet_lines(allowed_paths, "allowed paths unknown; do not invent paths"),
        "",
        "### Blocked paths",
        _bullet_lines(blocked, "blocked paths missing; conservative blockers applied"),
    ]
    return "\n".join(sections)


def boundary_block_section(statements: Iterable[object]) -> str:
    return generic_section("Boundary statements", statements, "boundary statements missing; stop and review")


def stop_rules_section(stop_rules: Iterable[object]) -> str:
    return generic_section("Stop rules", stop_rules, "stop rules missing; stop and review")


def expected_outputs_section(items: Iterable[object]) -> str:
    return generic_section("Expected outputs", items, "expected outputs not supplied")


def reporting_format_section(headings: Iterable[object]) -> str:
    return generic_section("Required reporting format", headings, "reporting format not supplied")


def manual_harness_instruction_section(instructions: Iterable[object]) -> str:
    return generic_section(
        "Manual harness instructions",
        instructions,
        "manual harness instructions missing; do not execute harness",
    )


def not_created_register_section(items: Iterable[object]) -> str:
    return generic_section(
        "Not created / not approved register",
        items,
        "not-created register missing; assume runtime, adapters, execution, and Git mutation are not approved",
    )


def limitations_section(items: Iterable[object]) -> str:
    return generic_section("Limitations", items, "limitations not supplied; treat output as bounded advisory text")
