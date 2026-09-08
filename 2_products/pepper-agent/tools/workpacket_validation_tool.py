"""Governed WorkPacket validation command tool for Pepper workers.

This tool is only exposed for dispatcher-spawned Pepper governed workers.  It
does not accept arbitrary shell text; workers can list exact command IDs derived
from the active WorkPacket and then run one of those IDs with ``shell=False``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
import hashlib
import json
from pathlib import Path
import shlex
import shutil
import sys
from types import SimpleNamespace
from typing import Any

from tools import governed_workpacket_file_guard as file_guard
from tools.registry import registry, tool_error, tool_result


GOVERNED_VALIDATION_POLICY_ID = "pepper-governed-workpacket-validation-command-tool-v1"
REVIEW_PREPARE_VALIDATION_AUTHORITY_POLICY_ID = "pepper-review-prepare-validation-authority-v1"

WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE = "WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE"
WORKPACKET_VALIDATION_COMMAND_DENIED = "WORKPACKET_VALIDATION_COMMAND_DENIED"
WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED = "WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED"
WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE = "WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE"
WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT = "WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT"
REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED = "REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED"

_COMMAND_ID_PREFIX = "GVCMD"
_DEFAULT_TIMEOUT_SECONDS = 120
_PACKAGE_TARGETS = (
    ("web", "2_products/pepper-agent/web"),
    ("desktop", "2_products/pepper-agent/apps/desktop"),
    ("ui-tui", "2_products/pepper-agent/ui-tui"),
)
_FRONTEND_TEST_SUFFIXES = (".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")
_MAX_FRONTEND_TEST_FILES = 25
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
_FORBIDDEN_SHELL_MARKERS = ("||", "&&", "<<", ">>", "$(", "${")
_FORBIDDEN_SHELL_TOKENS = ("|", "&", ";", ">", "<", "`")
_FORBIDDEN_SCRIPT_TOKENS = frozenset(
    {"rm", "rmdir", "del", "curl", "wget", "powershell", "pwsh"}
)
_REVIEW_PREPARE_VALIDATION_AUTHORITY_DIGEST_ALGORITHM = (
    "pepper-review-prepare-validation-authority-sha256-v1"
)
_REVIEW_PREPARE_VALIDATION_RESULT_DIGEST_ALGORITHM = (
    "pepper-review-prepare-validation-result-sha256-v1"
)
_REVIEW_PREPARE_COMMAND_MANIFEST_DIGEST_ALGORITHM = (
    "pepper-review-prepare-validation-command-manifest-sha256-v1"
)
_REVIEW_PREPARE_CURRENT_RUN_BINDING_DIGEST_ALGORITHM = (
    "pepper-review-prepare-current-terminal-run-binding-sha256-v1"
)
_WORKPACKET_VALIDATION_EXECUTION_PLAN_DIGEST_ALGORITHM = (
    "pepper-workpacket-validation-execution-plan-sha256-v1"
)
_PACKAGE_SCRIPT_IDENTITY_DIGEST_ALGORITHM = (
    "pepper-workpacket-package-script-identity-sha256-v1"
)
_ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-acceptance-contract-sha256-v1"
)
_KANBAN_COMPLETION_RESULT_DIGEST_ALGORITHM = (
    "agent-platform-pepper-p18-9-0-kanban-completion-result-sha256-v1"
)


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
    execution_plan: tuple[dict[str, Any], ...] = ()
    execution_plan_SHA256: str | None = None


@dataclass(frozen=True)
class _LaunchSpec:
    effective_argv: tuple[str, ...]
    working_directory: str
    timeout_seconds: int
    expected_exit_codes: tuple[int, ...]
    max_stdout_bytes: int
    max_stderr_bytes: int


def check_governed_workpacket_validation_requirements() -> bool:
    """Expose the tool whenever the active process is a governed worker.

    Authority and runtime failures must be returned by the handler as bounded
    JSON tool results so the model can repair or block through the normal
    Hermes tool loop. Hiding the schema here strands the worker with no
    validation surface and encourages a plain-text stop.
    """

    return file_guard.governed_worker_enabled()


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
    if not specs:
        specs.extend(_frontend_package_test_specs(authority, work_packet))
    return _finalize_command_specs(tuple(specs))


def review_prepare_validation_requirements(
    acceptance_contract: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], ...]:
    """Return canonical executable validation requirements for review PREPARE."""

    if not isinstance(acceptance_contract, Mapping):
        return ()
    requirements: list[dict[str, Any]] = []
    seen: set[tuple[str | None, str]] = set()
    for source_key in ("work_packet_validation_steps", "validation_steps"):
        steps = acceptance_contract.get(source_key)
        if not isinstance(steps, list):
            continue
        for index, step in enumerate(steps, start=1):
            requirement = _review_validation_requirement_from_step(
                step,
                source_key=source_key,
                index=index,
            )
            if requirement is None:
                continue
            key = (
                requirement.get("validation_id"),
                requirement["source_command"],
            )
            if key in seen:
                continue
            seen.add(key)
            requirements.append(requirement)
    return tuple(requirements)


def review_prepare_validation_result_records(
    completion: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    records: list[dict[str, Any]] = []
    containers: list[Any] = [completion]
    metadata = completion.get("run_metadata") if isinstance(completion, Mapping) else None
    if isinstance(metadata, Mapping):
        containers.append(metadata)
        nested = metadata.get("workpacket_validation")
        if isinstance(nested, Mapping):
            containers.append(nested)
    for container in containers:
        for key in (
            "workpacket_validation_results",
            "validation_command_results",
            "validation_results",
            "command_results",
            "results",
        ):
            value = container.get(key) if isinstance(container, Mapping) else None
            if isinstance(value, list):
                records.extend(item for item in value if isinstance(item, dict))
    return tuple(records)


def review_prepare_validation_result_matches_requirement(
    result: Mapping[str, Any],
    requirement: Mapping[str, Any],
    *,
    acceptance_contract: Mapping[str, Any],
) -> bool:
    if not _validation_result_digest_valid_for_matching(result):
        return False
    command = result.get("command") if isinstance(result.get("command"), Mapping) else {}
    result_command = _normalized_validation_command(
        command.get("source_command")
        or result.get("source_command")
        or result.get("command")
    )
    if result_command != requirement["source_command"]:
        return False
    expected_validation_id = requirement.get("validation_id")
    observed_validation_id = command.get("validation_id") or result.get("validation_id")
    if expected_validation_id and observed_validation_id != expected_validation_id:
        return False
    for key in ("ticket_id", "work_packet_id", "work_packet_SHA256"):
        expected = acceptance_contract.get(key)
        if expected is not None and result.get(key) != expected:
            return False
    disposition = str(result.get("disposition") or "").strip().casefold()
    success = _strict_bool_metadata_value(result.get("success"))
    if requirement.get("not_applicable") or requirement.get("manual"):
        return disposition in {"not_applicable", "not-applicable", "skipped"} and success is not False
    if success is not True or disposition != "passed":
        return False
    if _strict_bool_metadata_value(result.get("process_started")) is not True:
        return False
    exit_code = _int_or_none(result.get("exit_code"))
    expected_exit_codes = tuple(requirement.get("expected_exit_codes") or (0,))
    return exit_code in expected_exit_codes


def review_prepare_validation_contract_satisfied(
    completion: Mapping[str, Any],
    acceptance_contract: Mapping[str, Any] | None,
) -> bool:
    if not isinstance(completion, Mapping) or not isinstance(acceptance_contract, Mapping):
        return False
    metadata = completion.get("run_metadata")
    observation = completion.get("validation_observation_reference")
    if _metadata_strict_bool(metadata, "validation_infrastructure_failure") is True:
        return False
    if isinstance(observation, Mapping) and _metadata_strict_bool(
        observation,
        "infrastructure_failure",
        "validation_infrastructure_failure",
    ) is True:
        return False
    for container in (metadata, observation):
        validation_passed = _metadata_strict_bool(
            container,
            "validation_passed",
            "execution_validation_passed",
        )
        if validation_passed is False:
            return False
    for container in (metadata, completion):
        closure_complete = _metadata_strict_bool(
            container,
            "validation_complete",
            "validation_closed",
            "validation_closure_complete",
        )
        if closure_complete is False:
            return False
    requirements = review_prepare_validation_requirements(acceptance_contract)
    if not requirements:
        return any(
            _metadata_strict_bool(
                container,
                "validation_passed",
                "execution_validation_passed",
            )
            is True
            for container in (metadata, observation, completion)
        )
    results = review_prepare_validation_result_records(completion)
    if not results:
        return False
    return all(
        any(
            review_prepare_validation_result_matches_requirement(
                result,
                requirement,
                acceptance_contract=acceptance_contract,
            )
            for result in results
        )
        for requirement in requirements
    )


def validate_review_prepare_validation_authority(
    *,
    authority: file_guard.WorkPacketFileAuthority,
    projection: Mapping[str, Any],
    completion: Mapping[str, Any],
    acceptance_contract: Mapping[str, Any],
    requested_project_id: str | None,
    requested_ticket_id: str | None,
    requested_next_action_id: str | None,
    authorized_specs: tuple[GovernedValidationCommandSpec, ...],
) -> None:
    """Validate PREPARE authority independently from product runtime request guards."""

    _ = authorized_specs
    if not isinstance(projection, Mapping):
        raise ValueError("projection authority is unavailable")
    if not isinstance(completion, Mapping):
        raise ValueError("completion authority is unavailable")
    if not isinstance(acceptance_contract, Mapping):
        raise ValueError("acceptance contract authority is unavailable")
    if not requested_project_id or not requested_ticket_id or not requested_next_action_id:
        raise ValueError("explicit PREPARE action identity is required")

    project_id = _required_text(projection, "project_id")
    ticket_id = _required_text(projection, "ticket_id")
    expected_action = _review_prepare_action_id(ticket_id)
    _require_equal("requested project", requested_project_id, project_id)
    _require_equal("requested ticket", requested_ticket_id, ticket_id)
    _require_equal("requested PREPARE action", requested_next_action_id, expected_action)
    _require_equal("WorkPacket authority ticket", authority.ticket_id, ticket_id)

    _require_equal("contract project", acceptance_contract.get("project_id"), project_id)
    _require_equal("contract ticket", acceptance_contract.get("ticket_id"), ticket_id)
    for key, authority_value in (
        ("ticket_spec_SHA256", authority.ticket_spec_SHA256),
        ("work_packet_id", authority.work_packet_id),
        ("work_packet_SHA256", authority.work_packet_SHA256),
    ):
        _require_equal(f"projection {key}", projection.get(key), authority_value)
        _require_equal(f"acceptance contract {key}", acceptance_contract.get(key), authority_value)
    _require_equal(
        "projection projection_SHA256",
        projection.get("projection_SHA256"),
        authority.projection_SHA256,
    )
    _require_equal(
        "completion board",
        completion.get("kanban_board_slug"),
        projection.get("kanban_board_slug"),
    )
    _require_equal(
        "completion task",
        completion.get("kanban_task_id"),
        projection.get("kanban_task_id"),
    )
    if completion.get("blocker_code"):
        raise ValueError("completion has a blocker")
    run_id = _int_or_none(completion.get("run_id"))
    if run_id is None:
        raise ValueError("completion run_id is unavailable")
    current_run_id = _int_or_none(completion.get("kanban_task_current_run_id"))
    if current_run_id is not None:
        raise ValueError("completion is not terminal/current")
    if not _completion_is_terminal_for_prepare(completion):
        raise ValueError("completion is not terminal/current")
    _validate_canonical_current_terminal_run_binding(projection, completion)

    completion_sha = completion.get("kanban_completion_result_SHA256")
    if isinstance(completion_sha, str) and completion_sha:
        expected_completion_sha = _digest_payload(
            _KANBAN_COMPLETION_RESULT_DIGEST_ALGORITHM,
            {
                key: value
                for key, value in completion.items()
                if key != "kanban_completion_result_SHA256"
            },
        )
        _require_equal("completion digest", completion_sha, expected_completion_sha)
    contract_sha = acceptance_contract.get("acceptance_contract_SHA256")
    if isinstance(contract_sha, str) and contract_sha:
        expected_contract_sha = _digest_payload(
            _ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM,
            {
                key: value
                for key, value in acceptance_contract.items()
                if key != "acceptance_contract_SHA256"
            },
        )
        _require_equal("acceptance contract digest", contract_sha, expected_contract_sha)
    criteria_sha = acceptance_contract.get("criteria_revision_SHA256")
    if isinstance(criteria_sha, str) and criteria_sha:
        expected_criteria_sha = _criteria_revision_digest_if_possible(acceptance_contract)
        if expected_criteria_sha is not None:
            _require_equal("criteria revision digest", criteria_sha, expected_criteria_sha)


def run_review_prepare_validation_commands(
    *,
    projection: Mapping[str, Any],
    completion: Mapping[str, Any],
    acceptance_contract: Mapping[str, Any],
    worker_env: Mapping[str, str],
    requirements: tuple[Mapping[str, Any], ...] | None = None,
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    """Resolve, authorize, and run review-PREPARE validation commands.

    This is the canonical PREPARE validation authority path used by product
    runtime. It derives exact command specs, never accepts arbitrary shell text,
    and runs only through the same shell-free substrate used by the worker tool.
    """

    normalized_requirements = tuple(
        dict(requirement)
        for requirement in (
            requirements
            if requirements is not None
            else review_prepare_validation_requirements(acceptance_contract)
        )
    )
    authority, work_packet = resolve_governed_workpacket_validation_authority(worker_env)
    specs = build_governed_validation_command_specs(authority, work_packet)
    try:
        validate_review_prepare_validation_authority(
            authority=authority,
            projection=projection,
            completion=completion,
            acceptance_contract=acceptance_contract,
            requested_project_id=requested_project_id,
            requested_ticket_id=requested_ticket_id,
            requested_next_action_id=requested_next_action_id,
            authorized_specs=specs,
        )
    except ValueError as exc:
        return _review_prepare_validation_denied_result(
            normalized_requirements,
            failure_detail=f"{REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED}: {exc}",
        )
    results: list[dict[str, Any]] = []
    selected: list[tuple[dict[str, Any], GovernedValidationCommandSpec]] = []
    reusable: list[tuple[dict[str, Any], dict[str, Any]]] = []
    missing: list[dict[str, Any]] = []
    existing_results = review_prepare_validation_result_records(completion)
    for requirement in normalized_requirements:
        spec = _review_prepare_validation_spec_for_requirement(
            specs,
            requirement,
        )
        if spec is None and not (
            requirement.get("manual") or requirement.get("not_applicable")
        ):
            missing.append(requirement)
            continue
        existing = next(
            (
                result
                for result in existing_results
                if review_prepare_validation_result_matches_requirement(
                    result,
                    requirement,
                    acceptance_contract=acceptance_contract,
                )
            ),
            None,
        )
        if existing is not None:
            reusable.append((requirement, existing))
            continue
        if spec is None:
            missing.append(requirement)
            continue
        selected.append((requirement, spec))
    authority_record = build_review_prepare_validation_authority_record(
        projection=projection,
        completion=completion,
        acceptance_contract=acceptance_contract,
        requirements=normalized_requirements,
        authorized_specs=tuple(spec for _requirement, spec in selected),
        workpacket_capability_specs=specs,
        requested_project_id=requested_project_id,
        requested_ticket_id=requested_ticket_id,
        requested_next_action_id=requested_next_action_id,
    )
    for requirement, existing in reusable:
        results.append(
            review_prepare_validation_result_record(
                existing,
                requirement=requirement,
                authority_record=authority_record,
                reused_existing_evidence=True,
            )
        )
    if missing:
        return {
            "validation_executed": False,
            "validation_complete": len(results) == len(normalized_requirements),
            "validation_passed": None,
            "validation_command_results": results,
            "review_prepare_validation_authority": authority_record,
            "review_prepare_validation_authority_SHA256": authority_record[
                "review_prepare_validation_authority_SHA256"
            ],
            "missing_requirements": [
                review_prepare_validation_requirement_public(item) for item in missing
            ],
            "failure_detail": "missing governed validation command specs for acceptance-contract requirements",
        }
    validation_passed = True
    failure_detail = None
    for requirement, spec in selected:
        try:
            result = json.loads(_run_command(authority, spec))
        except Exception as exc:  # pragma: no cover - defensive runtime guard
            result = {
                "success": False,
                "error": f"review-preparation validation command failed: {exc}",
                "ticket_id": acceptance_contract.get("ticket_id"),
                "work_packet_id": acceptance_contract.get("work_packet_id"),
                "work_packet_SHA256": acceptance_contract.get("work_packet_SHA256"),
                "command": _public_command(spec),
                "disposition": "failed",
                "exit_code": None,
                "process_started": False,
            }
        record = review_prepare_validation_result_record(
            result,
            requirement=requirement,
            authority_record=authority_record,
        )
        results.append(record)
        if not review_prepare_validation_result_matches_requirement(
            record,
            requirement,
            acceptance_contract=acceptance_contract,
        ):
            validation_passed = False
            failure_detail = _safe_text(
                record.get("error")
                or record.get("failure_reason")
                or record.get("disposition")
                or "validation command did not satisfy requirement",
                limit=300,
            )
            break
    return {
        "validation_executed": bool(selected),
        "validation_complete": len(results) == len(normalized_requirements),
        "validation_passed": validation_passed and len(results) == len(normalized_requirements),
        "validation_command_results": results,
        "review_prepare_validation_authority": authority_record,
        "review_prepare_validation_authority_SHA256": authority_record[
            "review_prepare_validation_authority_SHA256"
        ],
        "missing_requirements": [],
        "failure_detail": failure_detail,
    }


def build_review_prepare_validation_authority_record(
    *,
    projection: Mapping[str, Any],
    completion: Mapping[str, Any],
    acceptance_contract: Mapping[str, Any],
    requirements: tuple[Mapping[str, Any], ...],
    authorized_specs: tuple[GovernedValidationCommandSpec, ...] = (),
    workpacket_capability_specs: tuple[GovernedValidationCommandSpec, ...] | None = None,
    requested_project_id: str | None = None,
    requested_ticket_id: str | None = None,
    requested_next_action_id: str | None = None,
) -> dict[str, Any]:
    command_manifest = _review_prepare_authorized_command_manifest(authorized_specs)
    capability_manifest = _review_prepare_authorized_command_manifest(
        workpacket_capability_specs if workpacket_capability_specs is not None else authorized_specs,
    )
    command_manifest_sha = _digest_payload(
        _REVIEW_PREPARE_COMMAND_MANIFEST_DIGEST_ALGORITHM,
        {"commands": command_manifest},
    )
    capability_manifest_sha = _digest_payload(
        _REVIEW_PREPARE_COMMAND_MANIFEST_DIGEST_ALGORITHM,
        {"commands": capability_manifest, "manifest_kind": "workpacket_capability"},
    )
    current_run_binding = _canonical_current_terminal_run_binding(projection, completion)
    record = {
        "schema_version": 1,
        "authority_kind": "review_prepare_validation",
        "policy_id": REVIEW_PREPARE_VALIDATION_AUTHORITY_POLICY_ID,
        "project_id": acceptance_contract.get("project_id"),
        "ticket_id": acceptance_contract.get("ticket_id"),
        "ticket_spec_SHA256": acceptance_contract.get("ticket_spec_SHA256"),
        "work_packet_id": acceptance_contract.get("work_packet_id"),
        "work_packet_SHA256": acceptance_contract.get("work_packet_SHA256"),
        "projection_SHA256": projection.get("projection_SHA256"),
        "kanban_board_slug": projection.get("kanban_board_slug"),
        "kanban_task_id": projection.get("kanban_task_id"),
        "run_id": completion.get("run_id"),
        "current_terminal_run_binding": current_run_binding,
        "current_terminal_run_binding_SHA256": (
            _digest_payload(
                _REVIEW_PREPARE_CURRENT_RUN_BINDING_DIGEST_ALGORITHM,
                current_run_binding,
            )
            if current_run_binding is not None
            else None
        ),
        "kanban_completion_result_SHA256": completion.get("kanban_completion_result_SHA256"),
        "acceptance_contract_SHA256": acceptance_contract.get("acceptance_contract_SHA256"),
        "criteria_revision_SHA256": acceptance_contract.get("criteria_revision_SHA256"),
        "requested_project_id": requested_project_id,
        "requested_ticket_id": requested_ticket_id,
        "requested_next_action_id": requested_next_action_id,
        "command_execution_authorized": True,
        "command_execution_authority": "explicit_human_review_preparation_action",
        "capability_not_authority": True,
        "workpacket_capability_manifest": capability_manifest,
        "workpacket_capability_manifest_SHA256": capability_manifest_sha,
        "review_prepare_authorized_command_manifest": command_manifest,
        "review_prepare_authorized_command_manifest_SHA256": command_manifest_sha,
        "authorized_command_manifest": command_manifest,
        "authorized_command_manifest_SHA256": command_manifest_sha,
        "requirements": [
            review_prepare_validation_requirement_public(item) for item in requirements
        ],
    }
    record["review_prepare_validation_authority_SHA256"] = _digest_payload(
        _REVIEW_PREPARE_VALIDATION_AUTHORITY_DIGEST_ALGORITHM,
        record,
    )
    return record


def review_prepare_validation_requirement_public(
    requirement: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "validation_id": requirement.get("validation_id"),
        "source_command": requirement.get("source_command"),
        "expected_exit_codes": list(requirement.get("expected_exit_codes") or (0,)),
        "source_key": requirement.get("source_key"),
        "not_applicable": bool(requirement.get("not_applicable")),
        "manual": bool(requirement.get("manual")),
    }


def review_prepare_validation_result_record(
    result: Mapping[str, Any],
    *,
    requirement: Mapping[str, Any],
    authority_record: Mapping[str, Any],
    reused_existing_evidence: bool = False,
) -> dict[str, Any]:
    record = dict(result) if isinstance(result, Mapping) else {"success": False}
    command = record.get("command")
    if not isinstance(command, Mapping):
        command = {
            "validation_id": requirement.get("validation_id"),
            "source_command": requirement.get("source_command"),
            "expected_exit_codes": list(requirement.get("expected_exit_codes") or (0,)),
        }
        record["command"] = command
    record.setdefault("ticket_id", authority_record.get("ticket_id"))
    record.setdefault("work_packet_id", authority_record.get("work_packet_id"))
    record.setdefault("work_packet_SHA256", authority_record.get("work_packet_SHA256"))
    if reused_existing_evidence:
        evidence, evidence_sha = _immutable_existing_validation_evidence(record)
        evidence_command = evidence.get("command")
        if not isinstance(evidence_command, Mapping):
            evidence_command = command
        record = {
            "success": evidence.get("success"),
            "policy_id": evidence.get("policy_id"),
            "ticket_id": evidence.get("ticket_id"),
            "work_packet_id": evidence.get("work_packet_id"),
            "work_packet_SHA256": evidence.get("work_packet_SHA256"),
            "command": dict(evidence_command),
            "source_command": evidence.get("source_command"),
            "validation_id": evidence.get("validation_id"),
            "disposition": evidence.get("disposition"),
            "failure_reason": evidence.get("failure_reason"),
            "exit_code": evidence.get("exit_code"),
            "process_started": evidence.get("process_started"),
            "validation_result_SHA256": evidence_sha,
            "reused_validation_evidence": evidence,
            "reused_validation_evidence_SHA256": evidence_sha,
        }
        record["review_prepare_validation_evidence_mode"] = "existing_evidence_reused"
        record["review_prepare_validation_acceptance_authority_SHA256"] = authority_record[
            "review_prepare_validation_authority_SHA256"
        ]
        record["review_prepare_validation_acceptance_authority"] = dict(authority_record)
        record["review_prepare_validation_reuse_SHA256"] = _digest_payload(
            _REVIEW_PREPARE_VALIDATION_RESULT_DIGEST_ALGORITHM,
            {
                key: value
                for key, value in record.items()
                if key != "review_prepare_validation_reuse_SHA256"
            },
        )
        return record
    else:
        record["review_prepare_validation_authority_SHA256"] = authority_record[
            "review_prepare_validation_authority_SHA256"
        ]
        record["review_prepare_validation_authority"] = dict(authority_record)
    record["validation_result_SHA256"] = _digest_payload(
        _REVIEW_PREPARE_VALIDATION_RESULT_DIGEST_ALGORITHM,
        {key: value for key, value in record.items() if key != "validation_result_SHA256"},
    )
    return record


def _review_prepare_validation_denied_result(
    requirements: tuple[Mapping[str, Any], ...],
    *,
    failure_detail: str,
) -> dict[str, Any]:
    return {
        "validation_executed": False,
        "validation_complete": False,
        "validation_passed": False,
        "process_started": False,
        "validation_command_results": [],
        "review_prepare_validation_authority": None,
        "review_prepare_validation_authority_SHA256": None,
        "missing_requirements": [
            review_prepare_validation_requirement_public(item) for item in requirements
        ],
        "failure_detail": failure_detail,
        "error_code": REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED,
    }


def _review_prepare_authorized_command_manifest(
    specs: tuple[GovernedValidationCommandSpec, ...],
) -> list[dict[str, Any]]:
    return [_command_manifest_entry(spec) for spec in specs]


def _command_manifest_entry(command: GovernedValidationCommandSpec) -> dict[str, Any]:
    return {
        "command_id": command.command_id,
        "validation_id": command.validation_id,
        "source": command.source,
        "source_command": command.source_command,
        "working_directory": command.working_directory,
        "expected_exit_codes": list(command.expected_exit_codes),
        "execution_plan_SHA256": command.execution_plan_SHA256,
        "execution_plan": [_public_plan_step(step) for step in _command_plan(command)],
    }


def _validation_result_payload_digest(record: Mapping[str, Any]) -> str:
    return _digest_payload(
        _REVIEW_PREPARE_VALIDATION_RESULT_DIGEST_ALGORITHM,
        {
            key: value
            for key, value in record.items()
            if key != "validation_result_SHA256"
        },
    )


def _immutable_existing_validation_evidence(
    result: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    source = result
    nested = result.get("reused_validation_evidence")
    if (
        result.get("review_prepare_validation_evidence_mode") == "existing_evidence_reused"
        and isinstance(nested, Mapping)
    ):
        source = nested
    evidence = dict(source)
    observed_sha = str(evidence.get("validation_result_SHA256") or "").strip()
    expected_sha = _validation_result_payload_digest(evidence)
    if observed_sha and observed_sha != expected_sha:
        raise ValueError("existing validation evidence digest mismatch")
    if not observed_sha:
        evidence["validation_result_SHA256"] = expected_sha
    return evidence, observed_sha or expected_sha


def _validation_result_digest_valid_for_matching(result: Mapping[str, Any]) -> bool:
    if not isinstance(result, Mapping):
        return False
    if result.get("review_prepare_validation_evidence_mode") == "existing_evidence_reused":
        try:
            _evidence, evidence_sha = _immutable_existing_validation_evidence(result)
        except ValueError:
            return False
        for key in ("validation_result_SHA256", "reused_validation_evidence_SHA256"):
            value = str(result.get(key) or "").strip()
            if value and value != evidence_sha:
                return False
        reuse_sha = str(result.get("review_prepare_validation_reuse_SHA256") or "").strip()
        if reuse_sha:
            expected_reuse_sha = _digest_payload(
                _REVIEW_PREPARE_VALIDATION_RESULT_DIGEST_ALGORITHM,
                {
                    key: value
                    for key, value in result.items()
                    if key != "review_prepare_validation_reuse_SHA256"
                },
            )
            if reuse_sha != expected_reuse_sha:
                return False
        return True
    observed_sha = str(result.get("validation_result_SHA256") or "").strip()
    if not observed_sha:
        return True
    return observed_sha == _validation_result_payload_digest(result)


def _canonical_current_terminal_run_binding(
    projection: Mapping[str, Any],
    completion: Mapping[str, Any],
) -> dict[str, Any] | None:
    board = str(projection.get("kanban_board_slug") or "").strip()
    task_id = str(projection.get("kanban_task_id") or "").strip()
    if not board or not task_id:
        return None
    try:
        from hermes_cli import kanban_db

        conn = kanban_db.connect(board=board)
    except Exception:
        return None
    try:
        task = kanban_db.get_task(conn, task_id)
        if task is None:
            return None
        runs = kanban_db.list_runs(conn, task_id)
        if not runs:
            return None
        active_run_ids = [
            int(run.id)
            for run in runs
            if getattr(run, "ended_at", None) is None
            and str(getattr(run, "status", "") or "").strip()
        ]
        latest = runs[-1]
        binding = {
            "kanban_board_slug": board,
            "kanban_task_id": task_id,
            "task_status": getattr(task, "status", None),
            "task_current_run_id": getattr(task, "current_run_id", None),
            "active_run_ids": active_run_ids,
            "terminal_run_id": int(latest.id),
            "terminal_run_status": str(getattr(latest, "status", "") or "").strip().casefold(),
            "terminal_run_outcome": str(getattr(latest, "outcome", "") or "").strip().casefold(),
            "terminal_run_ended_at": getattr(latest, "ended_at", None),
            "completion_run_id": completion.get("run_id"),
            "completion_run_status": str(completion.get("run_status") or "").strip().casefold(),
            "completion_run_outcome": str(completion.get("run_outcome") or "").strip().casefold(),
        }
        return binding
    finally:
        conn.close()


def _validate_canonical_current_terminal_run_binding(
    projection: Mapping[str, Any],
    completion: Mapping[str, Any],
) -> None:
    binding = _canonical_current_terminal_run_binding(projection, completion)
    if binding is None:
        raise ValueError("canonical Kanban current terminal run authority is unavailable")
    if binding["active_run_ids"] or binding["task_current_run_id"] is not None:
        raise ValueError("canonical current Kanban task still has an active run")
    if _int_or_none(completion.get("run_id")) != binding["terminal_run_id"]:
        raise ValueError("completion run_id is not the current terminal Kanban run")
    completion_status = str(completion.get("run_status") or "").strip().casefold()
    if completion_status and completion_status != binding["terminal_run_status"]:
        raise ValueError("completion run_status does not match current terminal Kanban run")
    completion_outcome = str(completion.get("run_outcome") or "").strip().casefold()
    if completion_outcome and completion_outcome != binding["terminal_run_outcome"]:
        raise ValueError("completion run_outcome does not match current terminal Kanban run")


def _required_text(container: Mapping[str, Any], key: str) -> str:
    value = str(container.get(key) or "").strip()
    if not value:
        raise ValueError(f"{key} is unavailable")
    return value


def _require_equal(label: str, observed: Any, expected: Any) -> None:
    if str(observed or "").strip() != str(expected or "").strip():
        raise ValueError(f"{label} mismatch")


def _review_prepare_action_id(ticket_id: str) -> str:
    token = "".join(ch if ch.isalnum() else "_" for ch in str(ticket_id).strip())
    return f"PREPARE_{token.upper()}_REVIEW"


def _completion_is_terminal_for_prepare(completion: Mapping[str, Any]) -> bool:
    status = str(completion.get("run_status") or "").strip().casefold()
    outcome = str(completion.get("run_outcome") or "").strip().casefold()
    terminal_class = str(completion.get("terminal_outcome_class") or "").strip().casefold()
    return (
        status in {"done", "completed"}
        or outcome == "completed"
        or terminal_class == "validated_review_required"
    )


def _criteria_revision_digest_if_possible(contract: Mapping[str, Any]) -> str | None:
    required = (
        "ticket_spec_SHA256",
        "work_packet_SHA256",
        "acceptance_criteria",
        "validation_steps",
        "response_contract",
    )
    if any(key not in contract for key in required):
        return None
    payload = {key: contract[key] for key in required}
    return _digest_payload(
        f"{_ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM}:criteria-revision-v1",
        payload,
    )


def _review_validation_requirement_from_step(
    step: Any,
    *,
    source_key: str,
    index: int,
) -> dict[str, Any] | None:
    validation_id = None
    command = None
    expected_exit_codes: tuple[int, ...] = (0,)
    not_applicable = False
    manual = False
    if isinstance(step, Mapping):
        optional = _strict_bool_metadata_value(step.get("optional"))
        if optional is True:
            return None
        kind = str(step.get("kind") or "").strip().casefold()
        manual = kind == "manual"
        validation_id = str(
            step.get("validation_id") or step.get("id") or f"{source_key}:{index}"
        ).strip()
        command = (
            step.get("command")
            or step.get("validation_command")
            or step.get("source_command")
        )
        if manual and not command:
            return None
        applicability = str(
            step.get("applicability") or step.get("disposition") or ""
        ).strip().casefold().replace("-", "_").replace(" ", "_")
        not_applicable = applicability == "not_applicable"
        expected_values = step.get("expected_exit_codes") or step.get("expected_exit_code")
        if isinstance(expected_values, list | tuple):
            parsed = tuple(
                value for value in (_int_or_none(item) for item in expected_values) if value is not None
            )
            if parsed:
                expected_exit_codes = parsed
        else:
            parsed = _int_or_none(expected_values)
            if parsed is not None:
                expected_exit_codes = (parsed,)
    elif isinstance(step, str):
        validation_id = f"{source_key}:{index}"
        command = step
    else:
        return None
    source_command = _normalized_validation_command(command)
    if not source_command:
        return None
    if source_command.casefold().replace("-", "_").replace(" ", "_") == "not_applicable":
        not_applicable = True
    return {
        "validation_id": validation_id or None,
        "source_command": source_command,
        "expected_exit_codes": expected_exit_codes,
        "not_applicable": not_applicable,
        "manual": manual,
        "source_key": source_key,
    }


def _review_prepare_validation_spec_for_requirement(
    specs: tuple[GovernedValidationCommandSpec, ...],
    requirement: Mapping[str, Any],
) -> GovernedValidationCommandSpec | None:
    if requirement.get("manual") or requirement.get("not_applicable"):
        return None
    for spec in specs:
        if _normalized_validation_command(spec.source_command) != requirement["source_command"]:
            continue
        expected_validation_id = requirement.get("validation_id")
        if expected_validation_id and spec.validation_id != expected_validation_id:
            continue
        return spec
    return None


def _workpacket_package_command_step_spec(
    authority: file_guard.WorkPacketFileAuthority,
    step: Any,
    *,
    index: int,
) -> GovernedValidationCommandSpec | None:
    command = _step_command(step)
    if not command:
        return None
    parsed = _workpacket_package_command_plan(
        authority,
        command,
        expected_exit_codes=_step_expected_exit_codes(step),
    )
    if parsed is None:
        return None
    plan, working_directory, runtime_reason = parsed
    first_argv = tuple(plan[0]["effective_argv"]) if plan else ()
    return GovernedValidationCommandSpec(
        command_id="",
        validation_id=_step_validation_id(step, index=index),
        source="workpacket.validation_steps.package_command",
        source_command=command,
        effective_argv=first_argv,
        working_directory=working_directory,
        timeout_seconds=_DEFAULT_TIMEOUT_SECONDS,
        expected_exit_codes=_step_expected_exit_codes(step),
        runtime_available=runtime_reason is None,
        runtime_unavailable_reason=runtime_reason,
        execution_plan=plan,
    )


def _workpacket_package_command_plan(
    authority: file_guard.WorkPacketFileAuthority,
    source_command: str,
    *,
    expected_exit_codes: tuple[int, ...],
) -> tuple[tuple[dict[str, Any], ...], str, str | None] | None:
    left, separator, right = source_command.partition("&&")
    if separator != "&&":
        return None
    if "&&" in right:
        return None
    try:
        left_tokens = tuple(shlex.split(left.strip(), posix=True))
        right_tokens = tuple(shlex.split(right.strip(), posix=True))
    except ValueError:
        return None
    if len(left_tokens) != 2 or left_tokens[0] != "cd" or not right_tokens:
        return None
    package_rel = _safe_relative_command_path(left_tokens[1])
    package_targets = {package_rel for _name, package_rel in _PACKAGE_TARGETS}
    if package_rel is None or package_rel not in package_targets:
        return None
    workspace_root = Path(authority.resolved_workspace_root).resolve()
    working_directory_path = (workspace_root / package_rel).resolve()
    try:
        working_directory_path.relative_to(workspace_root)
    except ValueError:
        return None
    if not working_directory_path.is_dir():
        return None
    if not _package_path_in_workpacket_scope(authority, package_rel):
        return None
    requested = _package_script_request(right_tokens)
    if requested is None:
        return None
    script_name, extra_args = requested
    script = _package_script(working_directory_path, script_name)
    if script is None:
        return None
    node_path = _resolve_node_executable()
    plan = _package_script_execution_plan(
        authority,
        workspace_root,
        package_rel,
        working_directory_path,
        script_name=script_name,
        script=script,
        extra_args=extra_args,
        expected_exit_codes=expected_exit_codes,
        node_path=node_path,
    )
    if plan is None:
        return None
    runtime_reason = None
    if node_path is None:
        runtime_reason = "node executable not found"
    else:
        missing_entries = [
            str(step.get("cli_entry") or "package CLI")
            for step in plan
            if step.get("runtime_unavailable_reason")
        ]
        if missing_entries:
            runtime_reason = f"package CLI entry not found: {', '.join(missing_entries[:3])}"
    return plan, working_directory_path.as_posix(), runtime_reason


def _package_script_request(tokens: tuple[str, ...]) -> tuple[str, tuple[str, ...]] | None:
    if not _package_command_tokens_shell_safe(tokens):
        return None
    if tokens[:2] == ("npm", "test"):
        script_name = "test"
        args = _tokens_after_optional_separator(tokens[2:])
    elif len(tokens) >= 3 and tokens[:2] == ("npm", "run"):
        script_name = tokens[2]
        args = _tokens_after_optional_separator(tokens[3:])
    else:
        return None
    if script_name in {"", "install", "exec", "x"}:
        return None
    if any(_looks_like_env_assignment(token) for token in args):
        return None
    return script_name, args


def _package_script_execution_plan(
    authority: file_guard.WorkPacketFileAuthority,
    workspace_root: Path,
    package_rel: str,
    package_dir: Path,
    *,
    script_name: str,
    script: str,
    extra_args: tuple[str, ...],
    expected_exit_codes: tuple[int, ...],
    node_path: Path | None,
) -> tuple[dict[str, Any], ...] | None:
    segments = _package_script_segments(script)
    if segments is None:
        return None
    if extra_args and len(segments) != 1:
        return None
    package_script_identity = _package_script_identity(package_rel, script_name, script, package_dir)
    plan: list[dict[str, Any]] = []
    for segment_index, segment in enumerate(segments, start=1):
        appended_args = extra_args if segment_index == len(segments) else ()
        step = _package_script_segment_plan(
            authority,
            workspace_root,
            package_rel,
            package_dir,
            segment,
            extra_args=appended_args,
            expected_exit_codes=expected_exit_codes,
            node_path=node_path,
            package_script_identity=package_script_identity,
        )
        if step is None:
            return None
        plan.append(step)
    return tuple(plan)


def _package_script_segments(script: str) -> tuple[tuple[str, ...], ...] | None:
    if any(marker in script for marker in ("||", "<<", ">>", "$(", "${")):
        return None
    try:
        tokens = tuple(shlex.split(script, posix=True))
    except ValueError:
        return None
    if not tokens:
        return None
    if any(token in _FORBIDDEN_SHELL_TOKENS for token in tokens):
        return None
    if any(_looks_like_env_assignment(token) for token in tokens):
        return None
    segments: list[tuple[str, ...]] = []
    current: list[str] = []
    for token in tokens:
        if token == "&&":
            if not current:
                return None
            segments.append(tuple(current))
            current = []
            continue
        current.append(token)
    if not current:
        return None
    segments.append(tuple(current))
    return tuple(segments)


def _package_script_segment_plan(
    authority: file_guard.WorkPacketFileAuthority,
    workspace_root: Path,
    package_rel: str,
    package_dir: Path,
    segment: tuple[str, ...],
    *,
    extra_args: tuple[str, ...],
    expected_exit_codes: tuple[int, ...],
    node_path: Path | None,
    package_script_identity: dict[str, Any],
) -> dict[str, Any] | None:
    if not segment:
        return None
    tool_name = segment[0]
    if tool_name == "vitest":
        if len(segment) < 2 or segment[1] != "run":
            return None
        args = (*segment[2:], *extra_args)
        scoped = _review_prepare_package_command_scope_tokens(package_rel, args)
        if scoped is None:
            return None
        if scoped:
            try:
                _validate_command_paths(authority, scoped)
            except Exception:
                return None
        module_entry = "vitest/vitest.mjs"
        argv_tail = ("run", *args)
    elif tool_name == "tsc":
        if extra_args or segment not in {("tsc", "-p", ".", "--noEmit"), ("tsc", "-b")}:
            return None
        module_entry = "typescript/lib/tsc.js"
        argv_tail = segment[1:]
    elif tool_name == "vite":
        if extra_args or segment != ("vite", "build"):
            return None
        module_entry = "vite/bin/vite.js"
        argv_tail = segment[1:]
    else:
        return None
    entry = _resolve_node_module_entry(workspace_root, package_dir, module_entry)
    runtime_reason = None if entry is not None else f"{module_entry} not found"
    return {
        "subcommand_id": "",
        "effective_argv": (
            node_path.as_posix() if node_path is not None else "node",
            entry.as_posix() if entry is not None else f"node_modules/{module_entry}",
            *argv_tail,
        ),
        "working_directory": package_dir.as_posix(),
        "timeout_seconds": _DEFAULT_TIMEOUT_SECONDS,
        "expected_exit_codes": list(expected_exit_codes),
        "cli_entry": module_entry,
        "runtime_unavailable_reason": runtime_reason,
        **package_script_identity,
    }


def _package_command_tokens_shell_safe(tokens: tuple[str, ...]) -> bool:
    if not tokens:
        return False
    if any(any(marker in token for marker in _FORBIDDEN_SHELL_MARKERS) for token in tokens):
        return False
    if any(token in _FORBIDDEN_SHELL_TOKENS for token in tokens):
        return False
    lowered = tuple(token.casefold() for token in tokens)
    if any(token in {"git", "docker", "graphify", "pnpm", "yarn", "corepack"} for token in lowered):
        return False
    if lowered[:2] in {("npm", "install"), ("npm", "exec")}:
        return False
    if lowered and lowered[0] == "npx":
        return False
    return not any(_looks_like_env_assignment(token) for token in tokens)


def _looks_like_env_assignment(token: str) -> bool:
    if "=" not in token:
        return False
    name = token.split("=", 1)[0]
    return bool(name) and (name[0].isalpha() or name[0] == "_") and all(
        ch.isalnum() or ch == "_" for ch in name
    )


def _tokens_after_optional_separator(tokens: tuple[str, ...]) -> tuple[str, ...]:
    if tokens and tokens[0] == "--":
        return tokens[1:]
    return tokens


def _review_prepare_package_command_scope_tokens(
    package_rel: str,
    args: tuple[str, ...],
) -> tuple[str, ...] | None:
    scoped: list[str] = []
    for token in args:
        if token == "--" or token.startswith("-"):
            continue
        raw_candidate = token.split("::", 1)[0]
        candidate = _safe_relative_command_path(raw_candidate)
        if candidate is None:
            normalized = str(raw_candidate or "").replace("\\", "/")
            if "/" in normalized or normalized.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
                return None
            continue
        if "/" not in candidate and not candidate.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
            continue
        if not candidate.startswith(f"{package_rel}/"):
            candidate = f"{package_rel}/{candidate}"
        scoped.append(candidate)
    return tuple(scoped)


def _safe_relative_command_path(value: Any) -> str | None:
    rel = str(value or "").replace("\\", "/").strip()
    if not rel or rel.startswith("/") or ":" in rel:
        return None
    if rel.startswith("./") or rel.startswith("../") or rel in {".", ".."}:
        return None
    if any(part in {"", ".", ".."} for part in rel.split("/")):
        return None
    return rel


def _package_path_in_workpacket_scope(
    authority: file_guard.WorkPacketFileAuthority,
    package_rel: str,
) -> bool:
    if _path_is_authorized(authority, package_rel):
        return True
    prefix = f"{package_rel}/"
    return any(str(pattern).strip().startswith(prefix) for pattern in authority.allowed_paths)


def _package_script_identity(
    package_rel: str,
    script_name: str,
    script: str,
    package_dir: Path,
) -> dict[str, Any]:
    package_json_sha = _file_sha256(package_dir / "package.json")
    identity = {
        "package_relative_path": package_rel,
        "package_script_name": script_name,
        "package_script": script,
        "package_script_SHA256": hashlib.sha256(script.encode("utf-8")).hexdigest(),
        "package_json_SHA256": package_json_sha,
    }
    identity["package_script_identity_SHA256"] = _digest_payload(
        _PACKAGE_SCRIPT_IDENTITY_DIGEST_ALGORITHM,
        identity,
    )
    return identity


def _file_sha256(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    return hashlib.sha256(data).hexdigest()


def _normalized_validation_command(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _strict_bool_metadata_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _metadata_strict_bool(container: Any, *keys: str) -> bool | None:
    if not isinstance(container, Mapping):
        return None
    for key in keys:
        if key in container:
            return _strict_bool_metadata_value(container.get(key))
    return None


def _int_or_none(value: object) -> int | None:
    try:
        return int(value) if value not in {None, ""} else None
    except (TypeError, ValueError):
        return None


def _safe_text(value: object, *, limit: int) -> str:
    return str(value or "").replace("\x00", "")[:limit]


def _digest_payload(algorithm: str, payload: Mapping[str, Any]) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(f"{algorithm}\n{data}".encode("utf-8")).hexdigest()


def _finalize_command_specs(
    specs: tuple[GovernedValidationCommandSpec, ...],
) -> tuple[GovernedValidationCommandSpec, ...]:
    finalized: list[GovernedValidationCommandSpec] = []
    for index, spec in enumerate(specs, start=1):
        command_id = f"{_COMMAND_ID_PREFIX}-{index:03d}"
        assigned = replace(spec, command_id=command_id)
        if assigned.execution_plan:
            plan = tuple(
                {
                    **step,
                    "subcommand_id": f"{command_id}.{step_index}",
                }
                for step_index, step in enumerate(assigned.execution_plan, start=1)
            )
            assigned = replace(assigned, execution_plan=plan)
        assigned = replace(
            assigned,
            execution_plan_SHA256=_execution_plan_digest(assigned),
        )
        finalized.append(assigned)
    return tuple(finalized)


def _execution_plan_digest(command: GovernedValidationCommandSpec) -> str:
    return _digest_payload(
        _WORKPACKET_VALIDATION_EXECUTION_PLAN_DIGEST_ALGORITHM,
        {
            "command_id": command.command_id,
            "validation_id": command.validation_id,
            "source_command": command.source_command,
            "working_directory": command.working_directory,
            "expected_exit_codes": list(command.expected_exit_codes),
            "execution_plan": [_public_plan_step(step) for step in _command_plan(command)],
        },
    )


def _command_plan(command: GovernedValidationCommandSpec) -> tuple[dict[str, Any], ...]:
    if command.execution_plan:
        return command.execution_plan
    return ({
        "subcommand_id": f"{command.command_id}.1",
        "effective_argv": command.effective_argv,
        "working_directory": command.working_directory,
        "timeout_seconds": command.timeout_seconds,
        "expected_exit_codes": list(command.expected_exit_codes),
    },)


def _public_plan_step(step: Mapping[str, Any]) -> dict[str, Any]:
    package_identity = {
        key: step.get(key)
        for key in (
            "package_relative_path",
            "package_script_name",
            "package_script",
            "package_script_SHA256",
            "package_json_SHA256",
            "package_script_identity_SHA256",
        )
        if step.get(key) is not None
    }
    return {
        "subcommand_id": step.get("subcommand_id"),
        "effective_argv": list(step.get("effective_argv") or ()),
        "working_directory": step.get("working_directory"),
        "timeout_seconds": step.get("timeout_seconds"),
        "expected_exit_codes": list(step.get("expected_exit_codes") or (0,)),
        "cli_entry": step.get("cli_entry"),
        "package_script_identity": package_identity or None,
    }


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
    for index, step in enumerate(tuple(getattr(work_packet, "validation_steps", ()) or ()), start=1):
        command = _step_command(step)
        if not command:
            continue
        package_spec = _workpacket_package_command_step_spec(authority, step, index=index)
        if package_spec is not None:
            specs.append(package_spec)
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
                validation_id=_step_validation_id(step, index=index),
                source="workpacket.validation_steps.command",
                source_command=command,
                effective_argv=tuple(argv),
                working_directory=authority.resolved_workspace_root.as_posix(),
                timeout_seconds=_DEFAULT_TIMEOUT_SECONDS,
                expected_exit_codes=_step_expected_exit_codes(step),
            )
        )
    return tuple(specs)


def _step_command(step: Any) -> str:
    if isinstance(step, Mapping):
        value = step.get("command") or step.get("validation_command") or step.get("source_command")
    else:
        value = getattr(step, "command", None)
    return _normalized_validation_command(value)


def _step_validation_id(step: Any, *, index: int) -> str:
    if isinstance(step, Mapping):
        value = step.get("validation_id") or step.get("id")
    else:
        value = getattr(step, "validation_id", None)
    text = str(value or "").strip()
    return text or f"validation:{index}"


def _step_expected_exit_codes(step: Any) -> tuple[int, ...]:
    value = None
    if isinstance(step, Mapping):
        value = step.get("expected_exit_codes") or step.get("expected_exit_code")
    parsed: tuple[int, ...] = ()
    if isinstance(value, list | tuple):
        parsed = tuple(
            item for item in (_int_or_none(candidate) for candidate in value) if item is not None
        )
    else:
        parsed_value = _int_or_none(value)
        if parsed_value is not None:
            parsed = (parsed_value,)
    return parsed or (0,)


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


def _run_command(
    authority: file_guard.WorkPacketFileAuthority,
    command: GovernedValidationCommandSpec,
) -> str:
    drift_reason = _script_identity_drift_reason(command)
    if drift_reason is not None:
        return tool_result(
            success=False,
            policy_id=GOVERNED_VALIDATION_POLICY_ID,
            work_packet_id=authority.work_packet_id,
            work_packet_SHA256=authority.work_packet_SHA256,
            ticket_id=authority.ticket_id,
            command=_public_command(command),
            disposition="blocked",
            failure_reason="script_identity_drift",
            error_code=WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT,
            error_detail=drift_reason,
            exit_code=None,
            process_started=False,
            execution_plan_SHA256=command.execution_plan_SHA256,
            subcommand_results=[],
            subcommand_count=len(_command_plan(command)),
            completed_subcommand_count=0,
            all_subcommands_passed=False,
        )
    if not command.runtime_available:
        return tool_result(
            success=False,
            policy_id=GOVERNED_VALIDATION_POLICY_ID,
            work_packet_id=authority.work_packet_id,
            work_packet_SHA256=authority.work_packet_SHA256,
            ticket_id=authority.ticket_id,
            command=_public_command(command),
            disposition="blocked",
            error_code=WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE,
            error_detail=command.runtime_unavailable_reason,
            process_started=False,
            execution_plan_SHA256=command.execution_plan_SHA256,
        )
    plan = _command_plan(command)
    if command.execution_plan:
        subcommand_results: list[dict[str, Any]] = []
        for step in plan:
            result = _run_launch_payload(
                authority,
                command_public=_public_command(command),
                step_public=_public_plan_step(step),
                effective_argv=tuple(step.get("effective_argv") or ()),
                working_directory=str(step.get("working_directory") or command.working_directory),
                timeout_seconds=int(step.get("timeout_seconds") or command.timeout_seconds),
                expected_exit_codes=tuple(step.get("expected_exit_codes") or command.expected_exit_codes),
            )
            subcommand_results.append(result)
            if result.get("success") is not True:
                break
        all_passed = len(subcommand_results) == len(plan) and all(
            item.get("success") is True for item in subcommand_results
        )
        last = subcommand_results[-1] if subcommand_results else {}
        return tool_result(
            success=all_passed,
            policy_id=GOVERNED_VALIDATION_POLICY_ID,
            work_packet_id=authority.work_packet_id,
            work_packet_SHA256=authority.work_packet_SHA256,
            ticket_id=authority.ticket_id,
            command=_public_command(command),
            disposition="passed" if all_passed else "failed",
            failure_reason="none" if all_passed else last.get("failure_reason", "subcommand_failed"),
            exit_code=last.get("exit_code"),
            process_started=any(item.get("process_started") is True for item in subcommand_results),
            subcommand_results=subcommand_results,
            subcommand_count=len(plan),
            completed_subcommand_count=len(subcommand_results),
            all_subcommands_passed=all_passed,
            execution_plan_SHA256=command.execution_plan_SHA256,
        )
    result = _run_launch_payload(
        authority,
        command_public=_public_command(command),
        step_public=_public_plan_step(plan[0]),
        effective_argv=command.effective_argv,
        working_directory=command.working_directory,
        timeout_seconds=command.timeout_seconds,
        expected_exit_codes=command.expected_exit_codes,
    )
    return tool_result(**result, execution_plan_SHA256=command.execution_plan_SHA256)


def _script_identity_drift_reason(
    command: GovernedValidationCommandSpec,
) -> str | None:
    for step in _command_plan(command):
        package_rel = step.get("package_relative_path")
        script_name = step.get("package_script_name")
        expected_script = step.get("package_script")
        if not package_rel or not script_name:
            continue
        package_dir = Path(str(step.get("working_directory") or ""))
        current_script = _package_script(package_dir, str(script_name))
        if current_script is None:
            return f"package script {package_rel}:{script_name} is unavailable"
        if current_script != expected_script:
            return f"package script {package_rel}:{script_name} changed after authorization"
        current_identity = _package_script_identity(
            str(package_rel),
            str(script_name),
            current_script,
            package_dir,
        )
        for key in (
            "package_script_SHA256",
            "package_json_SHA256",
            "package_script_identity_SHA256",
        ):
            if current_identity.get(key) != step.get(key):
                return f"package script {package_rel}:{script_name} identity drifted"
    return None


def _run_launch_payload(
    authority: file_guard.WorkPacketFileAuthority,
    *,
    command_public: dict[str, Any],
    step_public: dict[str, Any],
    effective_argv: tuple[str, ...],
    working_directory: str,
    timeout_seconds: int,
    expected_exit_codes: tuple[int, ...],
) -> dict[str, Any]:
    try:
        from hermes_cli.agent_platform.work_packet import validation_command_runner as vcr

        launch_spec = _LaunchSpec(
            effective_argv=effective_argv,
            working_directory=working_directory,
            timeout_seconds=timeout_seconds,
            expected_exit_codes=expected_exit_codes,
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
        return {
            "success": False,
            "error": f"{WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED}: {exc}",
            "error_code": WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED,
            "command": command_public,
            "subcommand": step_public,
            "disposition": "failed",
            "failure_reason": "policy_denied",
            "exit_code": None,
            "process_started": False,
        }

    return {
        "success": disposition.value == "passed",
        "policy_id": GOVERNED_VALIDATION_POLICY_ID,
        "work_packet_id": authority.work_packet_id,
        "work_packet_SHA256": authority.work_packet_SHA256,
        "ticket_id": authority.ticket_id,
        "command": command_public,
        "subcommand": step_public,
        "disposition": disposition.value,
        "failure_reason": reason.value,
        "exit_code": launch.exit_code,
        "process_started": launch.process_started,
        "terminate_requested": launch.terminate_requested,
        "kill_requested": launch.kill_requested,
        "stdout": stdout.model_dump(mode="json"),
        "stderr": stderr.model_dump(mode="json"),
    }


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
        "execution_plan_SHA256": command.execution_plan_SHA256,
        "execution_plan_kind": "sequential" if command.execution_plan else "single",
        "subcommand_count": len(_command_plan(command)),
    }


def _ticket_type(work_packet: Any) -> str:
    source_ticket = getattr(work_packet, "source_ticket", None)
    value = getattr(source_ticket, "ticket_type", None)
    return str(getattr(value, "value", value) or "").strip().lower()


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
    path_like = (
        "/" in raw
        or "\\" in raw
        or ":" in raw
        or raw.endswith((".py", ".ts", ".tsx", ".js", ".jsx"))
    )
    if not path_like:
        return None
    rel = _safe_relative_command_path(raw)
    if rel is None:
        raise ValueError(f"validation command path is unsafe: {raw}")
    return rel


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


def _handle(args: dict[str, Any], task_id: str | None = None, **_kwargs: Any) -> str:
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
    "REVIEW_PREPARE_VALIDATION_AUTHORITY_POLICY_ID",
    "WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE",
    "WORKPACKET_VALIDATION_COMMAND_DENIED",
    "WORKPACKET_VALIDATION_COMMAND_POLICY_DENIED",
    "WORKPACKET_VALIDATION_RUNTIME_UNAVAILABLE",
    "WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT",
    "REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED",
    "GovernedValidationCommandSpec",
    "build_review_prepare_validation_authority_record",
    "build_governed_validation_command_specs",
    "check_governed_workpacket_validation_requirements",
    "review_prepare_validation_contract_satisfied",
    "review_prepare_validation_requirement_public",
    "review_prepare_validation_requirements",
    "review_prepare_validation_result_matches_requirement",
    "review_prepare_validation_result_record",
    "review_prepare_validation_result_records",
    "resolve_governed_workpacket_validation_authority",
    "run_review_prepare_validation_commands",
    "validate_review_prepare_validation_authority",
    "workpacket_validation_tool",
]
