"""Governed WorkPacket validation command tool for Pepper workers.

This tool is only exposed for dispatcher-spawned Pepper governed workers.  It
does not accept arbitrary shell text; workers can list exact command IDs derived
from the active WorkPacket and then run one of those IDs with ``shell=False``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
import shlex
import shutil
import sys
from types import SimpleNamespace
from typing import Any, Mapping

from tools import governed_workpacket_file_guard as file_guard
from tools.registry import registry, tool_error, tool_result


GOVERNED_VALIDATION_POLICY_ID = "pepper-governed-workpacket-validation-command-tool-v1"

WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE = "WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE"
WORKPACKET_VALIDATION_COMMAND_DENIED = "WORKPACKET_VALIDATION_COMMAND_DENIED"
WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED = "WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED"
WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE = "WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE"

_COMMAND_ID_PREFIX = "GVCMD"
_MAX_FRONTEND_TEST_FILES = 64
_DEFAULT_TIMEOUT_SECONDS = 120
_FRONTEND_TEST_SUFFIXES = (
    ".test.ts",
    ".test.tsx",
    ".spec.ts",
    ".spec.tsx",
)
_PACKAGE_TARGETS = (
    ("web", "2_products/pepper-agent/web"),
    ("desktop", "2_products/pepper-agent/apps/desktop"),
    ("ui-tui", "2_products/pepper-agent/ui-tui"),
)
_PROTECTED_PATHS = (
    ".git/**",
    ".opencode/**",
    ".agents/**",
    "AGENTS.md",
    "graphify-out/**",
    "4_external/sources/**",
    "2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json",
)
_PROTECTED_COMPONENTS = frozenset({"node_modules"})
_PROTECTED_FILENAMES = frozenset({"package-lock.json"})
_FORBIDDEN_SCRIPT_TOKENS = {
    "git",
    "docker",
    "graphify",
    "npm",
    "npx",
    "pnpm",
    "yarn",
    "corepack",
    "pip",
}
_FORBIDDEN_SHELL_MARKERS = ("||", "&&", "<<", ">>", "$(", "${")
_FORBIDDEN_SHELL_TOKENS = ("|", "&", ";", ">", "<", "`")


@dataclass(frozen=True)
class GovernedValidationCommandSpec:
    command_id: str
    validation_id: str
    source: str
    source_command: str
    effective_argv: tuple[str, ...]
    working_directory: str
    timeout_seconds: int = _DEFAULT_TIMEOUT_SECONDS
    expected_exit_codes: tuple[int, ...] = (0,)
    runtime_available: bool = True
    runtime_unavailable_reason: str | None = None


@dataclass(frozen=True)
class _LaunchSpec:
    effective_argv: tuple[str, ...]
    working_directory: str
    timeout_seconds: int
    expected_exit_codes: tuple[int, ...]
    max_stdout_bytes: int
    max_stderr_bytes: int


def check_governed_workpacket_validation_requirements() -> bool:
    """Return True when the active process has runnable governed commands."""

    if not file_guard.governed_worker_enabled():
        return False
    try:
        authority, work_packet = resolve_governed_workpacket_validation_authority()
        return bool(build_governed_validation_command_specs(authority, work_packet))
    except Exception:
        return False


def workpacket_validation_tool(
    action: str = "list",
    command_id: str | None = None,
    task_id: str | None = None,
) -> str:
    """List or run exact governed validation commands for the active WorkPacket."""

    _ = task_id
    normalized_action = str(action or "list").strip().lower()
    if normalized_action not in {"list", "run"}:
        return tool_error(
            f"{WORKPACKET_VALIDATION_COMMAND_DENIED}: action must be 'list' or 'run'",
            error_code=WORKPACKET_VALIDATION_COMMAND_DENIED,
        )
    try:
        authority, work_packet = resolve_governed_workpacket_validation_authority()
        commands = build_governed_validation_command_specs(authority, work_packet)
    except Exception as exc:
        return tool_error(
            f"{WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE}: {exc}",
            error_code=WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE,
        )

    if normalized_action == "list":
        return tool_result(
            success=True,
            policy_id=GOVERNED_VALIDATION_POLICY_ID,
            work_packet_id=authority.work_packet_id,
            work_packet_SHA256=authority.work_packet_SHA256,
            ticket_id=authority.ticket_id,
            command_count=len(commands),
            commands=[_public_command(command) for command in commands],
        )

    selected_id = str(command_id or "").strip()
    if not selected_id:
        return tool_error(
            f"{WORKPACKET_VALIDATION_COMMAND_DENIED}: command_id is required for run",
            error_code=WORKPACKET_VALIDATION_COMMAND_DENIED,
        )
    selected = next(
        (command for command in commands if command.command_id == selected_id),
        None,
    )
    if selected is None:
        return tool_error(
            f"{WORKPACKET_VALIDATION_COMMAND_DENIED}: command_id is not authorized for this WorkPacket",
            error_code=WORKPACKET_VALIDATION_COMMAND_DENIED,
            command_id=selected_id,
        )
    return _run_command(authority, selected)


def resolve_governed_workpacket_validation_authority(
    env: Mapping[str, str] | None = None,
) -> tuple[file_guard.WorkPacketFileAuthority, Any]:
    """Resolve active governed WorkPacket authority and return its WorkPacket."""

    authority = file_guard.resolve_governed_workpacket_file_authority(env)
    if authority.generation_record_path is None:
        raise file_guard.WorkPacketAuthorityUnavailable(
            "generation record path is unavailable"
        )
    generation = json.loads(authority.generation_record_path.read_text(encoding="utf-8"))
    try:
        from hermes_cli.agent_platform.work_packet import WorkPacketCompilationResult

        compilation = WorkPacketCompilationResult.model_validate(
            generation["work_packet_compilation_result"]
        )
    except Exception as exc:
        raise file_guard.WorkPacketAuthorityUnavailable(
            "WorkPacket compilation evidence is unavailable"
        ) from exc
    work_packet = compilation.work_packet
    if work_packet.work_packet_id != authority.work_packet_id:
        raise file_guard.WorkPacketAuthorityUnavailable("WorkPacket ID mismatch")
    if work_packet.work_packet_SHA256 != authority.work_packet_SHA256:
        raise file_guard.WorkPacketAuthorityUnavailable("WorkPacket digest mismatch")
    if work_packet.ticket_id != authority.ticket_id:
        raise file_guard.WorkPacketAuthorityUnavailable("WorkPacket ticket mismatch")
    if _ticket_type(work_packet) != "implementation":
        raise file_guard.WorkPacketAuthorityUnavailable(
            "governed validation command authority requires an implementation WorkPacket"
        )
    return authority, work_packet


def build_governed_validation_command_specs(
    authority: file_guard.WorkPacketFileAuthority,
    work_packet: Any,
) -> tuple[GovernedValidationCommandSpec, ...]:
    """Build exact command specs from WorkPacket and repository package authority."""

    specs: list[GovernedValidationCommandSpec] = []
    specs.extend(_workpacket_command_step_specs(authority, work_packet))
    specs.extend(_frontend_package_test_specs(authority, work_packet))
    return tuple(
        replace(spec, command_id=f"{_COMMAND_ID_PREFIX}-{index:03d}")
        for index, spec in enumerate(specs, start=1)
    )


def _workpacket_command_step_specs(
    authority: file_guard.WorkPacketFileAuthority,
    work_packet: Any,
) -> tuple[GovernedValidationCommandSpec, ...]:
    try:
        from hermes_cli.agent_platform.work_packet import validation_command_runner as vcr
    except Exception:
        return ()

    runtime_binding = SimpleNamespace(
        resolved_python_executable=Path(sys.executable).resolve(strict=True).as_posix()
    )
    specs: list[GovernedValidationCommandSpec] = []
    for step in tuple(getattr(work_packet, "validation_steps", ()) or ()):
        command = str(getattr(step, "command", "") or "").strip()
        if not command:
            continue
        try:
            _module, argv = vcr._parse_command(  # noqa: SLF001 - deliberate substrate reuse
                source_command=command,
                runtime_binding=runtime_binding,
            )
            _validate_command_paths(authority, argv[3:])
        except Exception:
            continue
        specs.append(
            GovernedValidationCommandSpec(
                command_id="",
                validation_id=str(getattr(step, "validation_id", "validation")),
                source="workpacket.validation_steps.command",
                source_command=command,
                effective_argv=tuple(argv),
                working_directory=authority.resolved_workspace_root.as_posix(),
                timeout_seconds=_DEFAULT_TIMEOUT_SECONDS,
            )
        )
    return tuple(specs)


def _frontend_package_test_specs(
    authority: file_guard.WorkPacketFileAuthority,
    work_packet: Any,
) -> tuple[GovernedValidationCommandSpec, ...]:
    specs: list[GovernedValidationCommandSpec] = []
    validation_id = _validation_id_for_derived_tests(work_packet)
    for package_name, package_rel in _PACKAGE_TARGETS:
        package_dir = authority.resolved_workspace_root / package_rel
        script = _package_script(package_dir, "test")
        if script is None or _safe_package_test_script_tokens(script) is None:
            continue
        test_files = _authorized_package_test_files(authority, package_rel)
        if not test_files:
            continue
        node_path = _resolve_node_executable()
        vitest_path = _resolve_node_module_entry(
            authority.resolved_workspace_root,
            package_dir,
            "vitest/vitest.mjs",
        )
        runtime_reason = None
        if node_path is None:
            runtime_reason = "node executable not found"
        elif vitest_path is None:
            runtime_reason = "vitest package entry not found"
        test_args = tuple(
            Path(rel).relative_to(package_rel).as_posix()
            for rel in test_files[:_MAX_FRONTEND_TEST_FILES]
        )
        argv = (
            node_path.as_posix() if node_path is not None else "node",
            vitest_path.as_posix()
            if vitest_path is not None
            else "node_modules/vitest/vitest.mjs",
            "run",
            *test_args,
        )
        specs.append(
            GovernedValidationCommandSpec(
                command_id="",
                validation_id=validation_id,
                source=f"package:{package_name}:scripts.test",
                source_command=" ".join(("vitest", "run", *test_args)),
                effective_argv=argv,
                working_directory=package_dir.as_posix(),
                timeout_seconds=_DEFAULT_TIMEOUT_SECONDS,
                runtime_available=runtime_reason is None,
                runtime_unavailable_reason=runtime_reason,
            )
        )
    return tuple(specs)


def _run_command(
    authority: file_guard.WorkPacketFileAuthority,
    command: GovernedValidationCommandSpec,
) -> str:
    if not command.runtime_available:
        return tool_result(
            success=False,
            policy_id=GOVERNED_VALIDATION_POLICY_ID,
            work_packet_id=authority.work_packet_id,
            command=_public_command(command),
            disposition="blocked",
            error_code=WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE,
            error_detail=command.runtime_unavailable_reason,
            process_started=False,
        )
    try:
        from hermes_cli.agent_platform.work_packet import validation_command_runner as vcr

        launch_spec = _LaunchSpec(
            effective_argv=command.effective_argv,
            working_directory=command.working_directory,
            timeout_seconds=command.timeout_seconds,
            expected_exit_codes=command.expected_exit_codes,
            max_stdout_bytes=vcr.MAX_STDOUT_BYTES,
            max_stderr_bytes=vcr.MAX_STDERR_BYTES,
        )
        environment = vcr._minimal_environment()  # noqa: SLF001 - substrate reuse
        environment["CI"] = "1"
        launch = vcr._launch_and_capture(  # noqa: SLF001 - deliberate substrate reuse
            launch_spec,
            environment,
        )
        stdout = vcr._captured_stream(  # noqa: SLF001 - deliberate substrate reuse
            vcr.ValidationCommandStreamKind.STDOUT,
            launch.stdout_raw,
            vcr.RETAINED_STDOUT_BYTES,
            raw_byte_count=launch.stdout_raw_byte_count,
            raw_SHA256=launch.stdout_raw_SHA256,
        )
        stderr = vcr._captured_stream(  # noqa: SLF001 - deliberate substrate reuse
            vcr.ValidationCommandStreamKind.STDERR,
            launch.stderr_raw,
            vcr.RETAINED_STDERR_BYTES,
            raw_byte_count=launch.stderr_raw_byte_count,
            raw_SHA256=launch.stderr_raw_SHA256,
        )
        disposition, reason = vcr._disposition_for_launch(launch_spec, launch)  # noqa: SLF001
    except Exception as exc:
        return tool_error(
            f"{WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED}: {exc}",
            error_code=WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED,
            command_id=command.command_id,
        )

    return tool_result(
        success=disposition.value == "passed",
        policy_id=GOVERNED_VALIDATION_POLICY_ID,
        work_packet_id=authority.work_packet_id,
        work_packet_SHA256=authority.work_packet_SHA256,
        ticket_id=authority.ticket_id,
        command=_public_command(command),
        disposition=disposition.value,
        failure_reason=reason.value,
        exit_code=launch.exit_code,
        process_started=launch.process_started,
        terminate_requested=launch.terminate_requested,
        kill_requested=launch.kill_requested,
        stdout=stdout.model_dump(mode="json"),
        stderr=stderr.model_dump(mode="json"),
    )


def _public_command(command: GovernedValidationCommandSpec) -> dict[str, Any]:
    return {
        "command_id": command.command_id,
        "validation_id": command.validation_id,
        "source": command.source,
        "source_command": command.source_command,
        "working_directory": command.working_directory,
        "timeout_seconds": command.timeout_seconds,
        "expected_exit_codes": list(command.expected_exit_codes),
        "runtime_available": command.runtime_available,
        "runtime_unavailable_reason": command.runtime_unavailable_reason,
    }


def _ticket_type(work_packet: Any) -> str:
    source_ticket = getattr(work_packet, "source_ticket", None)
    value = getattr(source_ticket, "ticket_type", None)
    return str(getattr(value, "value", value) or "").strip().lower()


def _validation_id_for_derived_tests(work_packet: Any) -> str:
    fallback = "derived-frontend-tests"
    for step in tuple(getattr(work_packet, "validation_steps", ()) or ()):
        validation_id = str(getattr(step, "validation_id", "") or "").strip()
        if validation_id:
            fallback = validation_id
        text = " ".join(
            str(getattr(step, name, "") or "")
            for name in ("description", "expected_result")
        ).casefold()
        if validation_id and "test" in text:
            return validation_id
    return fallback


def _package_script(package_dir: Path, script_name: str) -> str | None:
    package_json = package_dir / "package.json"
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return None
    value = scripts.get(script_name)
    if not isinstance(value, str):
        return None
    return value.strip() or None


def _safe_package_test_script_tokens(script: str) -> tuple[str, ...] | None:
    if any(marker in script for marker in _FORBIDDEN_SHELL_MARKERS):
        return None
    try:
        tokens = tuple(shlex.split(script, posix=True))
    except ValueError:
        return None
    if tokens != ("vitest", "run"):
        return None
    lowered = {token.casefold() for token in tokens}
    if lowered & _FORBIDDEN_SCRIPT_TOKENS:
        return None
    if any(token in _FORBIDDEN_SHELL_TOKENS for token in tokens):
        return None
    return tokens


def _authorized_package_test_files(
    authority: file_guard.WorkPacketFileAuthority,
    package_rel: str,
) -> tuple[str, ...]:
    package_prefix = f"{package_rel}/"
    discovered: set[str] = set()
    for pattern in authority.allowed_paths:
        candidate = str(pattern).strip()
        if not candidate.startswith(package_prefix):
            continue
        if candidate.endswith("/**"):
            base_rel = candidate[:-3]
            base_path = authority.resolved_workspace_root / base_rel
            if not base_path.is_dir():
                continue
            for path in base_path.rglob("*"):
                if not path.is_file() or not _is_frontend_test_file(path.name):
                    continue
                rel = path.relative_to(authority.resolved_workspace_root).as_posix()
                if _path_is_authorized(authority, rel):
                    discovered.add(rel)
            continue
        if _is_frontend_test_file(candidate):
            path = authority.resolved_workspace_root / candidate
            if path.is_file() and _path_is_authorized(authority, candidate):
                discovered.add(candidate)
    return tuple(sorted(discovered))


def _validate_command_paths(
    authority: file_guard.WorkPacketFileAuthority,
    argv_tail: tuple[str, ...],
) -> None:
    for token in argv_tail:
        rel = _command_path_token(token)
        if rel is None:
            continue
        if not _path_is_authorized(authority, rel):
            raise ValueError(
                f"validation command path is outside WorkPacket scope: {rel}"
            )


def _command_path_token(token: str) -> str | None:
    raw = str(token or "").strip()
    if not raw or raw.startswith("-") or raw == "no:cacheprovider":
        return None
    raw = raw.split("::", 1)[0]
    if "/" not in raw and not raw.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
        return None
    return raw


def _path_is_authorized(
    authority: file_guard.WorkPacketFileAuthority,
    path: str,
) -> bool:
    rel = path.replace("\\", "/").strip()
    if (
        not rel
        or rel.startswith("/")
        or any(part in {"", ".", ".."} for part in rel.split("/"))
    ):
        return False
    lowered = tuple(part.casefold() for part in rel.split("/") if part)
    if any(part in _PROTECTED_COMPONENTS for part in lowered):
        return False
    if lowered and lowered[-1] in _PROTECTED_FILENAMES:
        return False
    if _first_matching_pattern(rel, (*_PROTECTED_PATHS, *authority.forbidden_paths)):
        return False
    return _first_matching_pattern(rel, authority.allowed_paths) is not None


def _first_matching_pattern(path: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        if _matches_pattern(path, pattern):
            return pattern
    return None


def _matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        base = pattern[:-3]
        return path == base or path.startswith(f"{base}/")
    return path == pattern


def _is_frontend_test_file(path: str) -> bool:
    return path.endswith(_FRONTEND_TEST_SUFFIXES)


def _resolve_node_executable() -> Path | None:
    raw = shutil.which("node")
    if not raw:
        return None
    try:
        path = Path(raw).resolve(strict=True)
    except OSError:
        return None
    return path if path.is_file() else None


def _resolve_node_module_entry(
    workspace_root: Path,
    package_dir: Path,
    module_entry: str,
) -> Path | None:
    for base in (package_dir, workspace_root / "2_products/pepper-agent", workspace_root):
        candidate = base / "node_modules" / module_entry
        try:
            resolved = candidate.resolve(strict=True)
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    return None


_SCHEMA = {
    "name": "workpacket_validation",
    "description": (
        "List or run exact validation command IDs authorized for the active "
        "governed Pepper implementation WorkPacket. Does not accept shell "
        "commands, Git, Docker, Graphify, package installs, or arbitrary process spawning."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list", "run"],
                "description": (
                    "Use list to inspect exact command IDs; use run with a "
                    "listed command_id."
                ),
            },
            "command_id": {
                "type": "string",
                "description": "Exact command_id returned by action=list. Required for action=run.",
            },
        },
        "required": ["action"],
        "additionalProperties": False,
    },
}


def _handle(args: dict[str, Any], task_id: str | None = None) -> str:
    return workpacket_validation_tool(
        action=str(args.get("action") or "list"),
        command_id=args.get("command_id"),
        task_id=task_id,
    )


registry.register(
    name="workpacket_validation",
    toolset="pepper_validation",
    schema=_SCHEMA,
    handler=_handle,
    check_fn=check_governed_workpacket_validation_requirements,
    emoji="✅",
    max_result_size_chars=100_000,
)


__all__ = [
    "GOVERNED_VALIDATION_POLICY_ID",
    "WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE",
    "WORKPACKET_VALIDATION_COMMAND_DENIED",
    "WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED",
    "WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE",
    "GovernedValidationCommandSpec",
    "build_governed_validation_command_specs",
    "check_governed_workpacket_validation_requirements",
    "resolve_governed_workpacket_validation_authority",
    "workpacket_validation_tool",
]
