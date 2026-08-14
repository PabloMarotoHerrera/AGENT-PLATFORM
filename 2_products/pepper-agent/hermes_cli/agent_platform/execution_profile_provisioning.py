"""Pepper-owned provisioning for governed execution profiles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_HERMES_PROVIDER_ID,
)
from hermes_cli.agent_platform.workflow.work_packet_kanban_projection import (
    PEPPER_EXECUTION_PROFILES_POLICY_ID,
    PEPPER_EXECUTION_PROFILES_POLICY_REVISION,
    classify_pepper_execution_profile,
)
from hermes_cli.profiles import (
    create_profile,
    get_profile_dir,
    list_profiles,
    normalize_profile_name,
    read_profile_meta,
)


PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME = "pepper-implementation-product"
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_DESCRIPTION = (
    "Pepper product implementation execution profile"
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_ROLE = "implementation_product"
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STORED_TOOLSETS = (
    "pepper_repository",
    "file",
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STORED_SENTINELS = ("no_mcp",)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_EFFECTIVE_TOOLSETS = (
    "kanban",
    "pepper_repository",
    "file",
    "pepper_validation",
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_CONFIG_TOOLSETS = (
    *PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STORED_TOOLSETS,
    *PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STORED_SENTINELS,
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_MODEL = "gpt-5.5"
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_API_MODE = "codex_responses"
PEPPER_IMPLEMENTATION_PRODUCT_PROVIDER_RUNTIME_PROFILE_ID = (
    "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
)
PEPPER_IMPLEMENTATION_PRODUCT_WORKER_PROFILE_ID = (
    "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
)
PEPPER_IMPLEMENTATION_PRODUCT_CREDENTIAL_POLICY_REVISION = (
    "provider-runtime-v1.provider-worker-v1.provider-credential-v1"
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_FORBIDDEN_TOOLSETS = (
    "terminal",
    "process",
    "code_execution",
    "debugging",
    "delegation",
    "mcp",
    "git",
    "docker",
    "graphify",
    "setup",
    "auth",
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STATUS_COMMAND = (
    "hermes agent-platform profile status pepper-implementation-product"
)
PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_PROVISION_COMMAND = (
    "hermes agent-platform profile provision pepper-implementation-product"
)

READY_FOR_HUMAN_PROVISIONING = "READY_FOR_HUMAN_PROVISIONING"
READY_FOR_P18_9_1_PROJECTION = "READY_FOR_P18_9_1_PROJECTION"
HUMAN_PROFILE_SELECTION_REQUIRED = "HUMAN_PROFILE_SELECTION_REQUIRED"
CANONICAL_PROFILE_CONTRACT_MISMATCH = "CANONICAL_PROFILE_CONTRACT_MISMATCH"
NON_CANONICAL_IMPLEMENTATION_PROFILE_PRESENT = (
    "NON_CANONICAL_IMPLEMENTATION_PROFILE_PRESENT"
)
PROFILE_PROVISIONED = "PROFILE_PROVISIONED"
PROFILE_ALREADY_PRESENT = "PROFILE_ALREADY_PRESENT"


class PepperExecutionProfileProvisioningError(RuntimeError):
    """Secret-free failure for governed execution profile provisioning."""

    error_code = "pepper_execution_profile_provisioning_error"

    def __init__(
        self,
        validation_category: str,
        diagnostics: dict[str, Any] | None = None,
    ) -> None:
        self.validation_category = _safe_text(validation_category)
        self.diagnostics = diagnostics or {}
        super().__init__(
            f"code={self.error_code} validation_category={self.validation_category}"
        )


def canonical_pepper_implementation_profile_contract() -> dict[str, Any]:
    """Return the secret-free canonical implementation profile contract."""

    return {
        "profile_name": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        "description": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_DESCRIPTION,
        "role": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_ROLE,
        "policy_id": PEPPER_EXECUTION_PROFILES_POLICY_ID,
        "policy_revision": PEPPER_EXECUTION_PROFILES_POLICY_REVISION,
        "stored_toolsets": list(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STORED_TOOLSETS),
        "stored_sentinels": list(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STORED_SENTINELS),
        "config_toolsets": list(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_CONFIG_TOOLSETS),
        "effective_worker_toolsets": list(
            PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_EFFECTIVE_TOOLSETS
        ),
        "runtime_injected_toolsets": ["pepper_validation"],
        "dispatcher_injected_toolsets": ["kanban"],
        "forbidden_toolsets": list(
            PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_FORBIDDEN_TOOLSETS
        ),
        "provider": OPENAI_CODEX_HERMES_PROVIDER_ID,
        "model": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_MODEL,
        "api_mode": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_API_MODE,
        "credential_profile_id": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "credential_policy_revision": PEPPER_IMPLEMENTATION_PRODUCT_CREDENTIAL_POLICY_REVISION,
        "provider_runtime_profile_id": PEPPER_IMPLEMENTATION_PRODUCT_PROVIDER_RUNTIME_PROFILE_ID,
        "worker_profile_id": PEPPER_IMPLEMENTATION_PRODUCT_WORKER_PROFILE_ID,
        "credential_resolution_source": "canonical_governed_home",
        "legacy_auth_json_used": False,
        "API_key_fallback_used": False,
        "credential_pool_fallback_used": False,
        "provision_command": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_PROVISION_COMMAND,
        "status_command": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STATUS_COMMAND,
    }


def inspect_pepper_implementation_profile_provisioning() -> dict[str, Any]:
    """Inspect local profiles without creating or mutating any profile."""

    contract = canonical_pepper_implementation_profile_contract()
    roster = _classified_profile_roster()
    candidates = _implementation_candidates(roster)
    candidate_names = [item["canonical_name"] for item in candidates]
    canonical_dir = get_profile_dir(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME)
    canonical_exists = canonical_dir.is_dir()
    canonical_validation = (
        validate_pepper_implementation_profile_contract(canonical_dir)
        if canonical_exists
        else _missing_profile_validation(canonical_dir)
    )

    if len(candidates) > 1:
        status = HUMAN_PROFILE_SELECTION_REQUIRED
    elif canonical_exists and canonical_validation["ok"] is not True:
        status = CANONICAL_PROFILE_CONTRACT_MISMATCH
    elif len(candidates) == 1:
        status = (
            READY_FOR_P18_9_1_PROJECTION
            if candidate_names == [PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME]
            else NON_CANONICAL_IMPLEMENTATION_PROFILE_PRESENT
        )
    else:
        status = READY_FOR_HUMAN_PROVISIONING

    return {
        "status": status,
        "canonical_profile": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        "canonical_profile_exists": canonical_exists,
        "canonical_profile_path": str(canonical_dir),
        "candidate_count": len(candidates),
        "candidate_profiles": candidate_names,
        "available_profile_count": len(roster),
        "available_profiles": roster,
        "canonical_profile_validation": canonical_validation,
        "contract": contract,
        "provision_command": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_PROVISION_COMMAND,
        "projection_performed": False,
        "dispatch_performed": False,
        "worker_execution": False,
        "Git_mutation": False,
        "Docker_invocation": False,
        "Graphify_invocation": False,
    }


def provision_pepper_implementation_profile() -> dict[str, Any]:
    """Create the single canonical implementation profile, or verify it exists."""

    inspection = inspect_pepper_implementation_profile_provisioning()
    status = inspection["status"]
    if status == READY_FOR_P18_9_1_PROJECTION:
        return {
            **inspection,
            "provisioning_status": PROFILE_ALREADY_PRESENT,
            "created": False,
        }
    if status == HUMAN_PROFILE_SELECTION_REQUIRED:
        raise PepperExecutionProfileProvisioningError(
            "human_profile_selection_required",
            diagnostics=inspection,
        )
    if status == CANONICAL_PROFILE_CONTRACT_MISMATCH:
        raise PepperExecutionProfileProvisioningError(
            "canonical_profile_contract_mismatch",
            diagnostics=inspection,
        )
    if status == NON_CANONICAL_IMPLEMENTATION_PROFILE_PRESENT:
        raise PepperExecutionProfileProvisioningError(
            "non_canonical_implementation_profile_present",
            diagnostics=inspection,
        )

    profile_dir = create_profile(
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        no_alias=True,
        no_skills=True,
        description=PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_DESCRIPTION,
    )
    _write_canonical_profile_config(profile_dir)

    validation = validate_pepper_implementation_profile_contract(profile_dir)
    if validation["ok"] is not True:
        raise PepperExecutionProfileProvisioningError(
            "created_profile_contract_mismatch",
            diagnostics=validation,
        )
    return {
        **inspect_pepper_implementation_profile_provisioning(),
        "provisioning_status": PROFILE_PROVISIONED,
        "created": True,
    }


def validate_pepper_implementation_profile_contract(
    profile_dir: Path | None = None,
) -> dict[str, Any]:
    """Validate the canonical implementation profile without reading secrets."""

    contract = canonical_pepper_implementation_profile_contract()
    profile_dir = profile_dir or get_profile_dir(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME)
    reasons: list[str] = []
    if not profile_dir.is_dir():
        reasons.append("profile_directory_missing")
        return _validation_result(profile_dir, contract, reasons)

    config = _read_profile_config(profile_dir, reasons)
    meta = read_profile_meta(profile_dir)
    if str(meta.get("description") or "").strip() != (
        PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_DESCRIPTION
    ):
        reasons.append("description_mismatch")

    model_cfg = config.get("model") if isinstance(config, dict) else None
    if not isinstance(model_cfg, dict):
        reasons.append("model_config_missing")
    else:
        expected_model = {
            "provider": contract["provider"],
            "default": contract["model"],
            "api_mode": contract["api_mode"],
        }
        for key, expected in expected_model.items():
            actual = str(model_cfg.get(key) or "").strip()
            if actual != expected:
                reasons.append(f"model_{key}_mismatch")

    cli_toolsets = _profile_config_cli_toolsets(config)
    if cli_toolsets != list(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_CONFIG_TOOLSETS):
        reasons.append("config_cli_toolsets_mismatch")
    forbidden = sorted(
        set(cli_toolsets) & set(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_FORBIDDEN_TOOLSETS)
    )
    if forbidden:
        reasons.append("forbidden_toolsets:" + ",".join(forbidden))
    if "pepper_validation" in cli_toolsets:
        reasons.append("pepper_validation_must_be_runtime_injected")
    if "kanban" in cli_toolsets:
        reasons.append("kanban_must_be_dispatcher_injected")

    profile_stub = {
        "name": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        "path": profile_dir,
        "description": str(meta.get("description") or ""),
        "is_default": False,
    }
    classification = classify_pepper_execution_profile(profile_stub)
    if classification.get("role") != PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_ROLE:
        reasons.append("role_mismatch")
    if classification.get("worker_assignable") is not True:
        reasons.append("worker_not_assignable")
    for reason in classification.get("rejection_reasons") or []:
        if str(reason) not in reasons:
            reasons.append(str(reason))

    runtime = None
    try:
        from hermes_cli.agent_platform.worker_credentials import (
            resolve_pepper_governed_executor_profile_runtime,
        )

        runtime = resolve_pepper_governed_executor_profile_runtime(
            PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
            profile_dir=profile_dir,
            require_assignable_roster_profile=False,
        )
    except Exception as exc:
        reasons.append(
            "provider_runtime_unresolved:" + _safe_text(
                getattr(exc, "validation_category", exc.__class__.__name__)
            )
        )
    else:
        expected_runtime = {
            "provider": contract["provider"],
            "model": contract["model"],
            "api_mode": contract["api_mode"],
            "credential_profile_id": contract["credential_profile_id"],
            "credential_policy_revision": contract["credential_policy_revision"],
            "provider_runtime_profile_id": contract["provider_runtime_profile_id"],
            "worker_profile_id": contract["worker_profile_id"],
        }
        for key, expected in expected_runtime.items():
            if runtime.get(key) != expected:
                reasons.append(f"runtime_{key}_mismatch")

    result = _validation_result(profile_dir, contract, reasons)
    result.update({
        "description": str(meta.get("description") or ""),
        "config_cli_toolsets": cli_toolsets,
        "classification": classification,
        "provider_runtime": _public_runtime(runtime),
    })
    return result


def assert_pepper_implementation_profile(profile_name: str) -> str:
    """Validate the only governed implementation profile id accepted here."""

    normalized = normalize_profile_name(str(profile_name or ""))
    if normalized != PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME:
        raise PepperExecutionProfileProvisioningError("execution_profile_mismatch")
    return normalized


def _classified_profile_roster() -> list[dict[str, Any]]:
    try:
        profiles = list_profiles()
    except Exception as exc:
        raise PepperExecutionProfileProvisioningError(
            "profile_roster_unavailable",
            diagnostics={"detail": _safe_text(exc)},
        ) from exc
    return [classify_pepper_execution_profile(profile) for profile in profiles]


def _implementation_candidates(roster: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in roster
        if item.get("role") == PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_ROLE
        and item.get("worker_assignable") is True
    ]


def _canonical_profile_config() -> dict[str, Any]:
    contract = canonical_pepper_implementation_profile_contract()
    return {
        "model": {
            "provider": contract["provider"],
            "default": contract["model"],
            "api_mode": contract["api_mode"],
        },
        "platform_toolsets": {
            "cli": list(PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_CONFIG_TOOLSETS),
        },
    }


def _write_canonical_profile_config(profile_dir: Path) -> None:
    import yaml

    config_path = profile_dir / "config.yaml"
    with config_path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(
            _canonical_profile_config(),
            stream,
            sort_keys=False,
            default_flow_style=False,
        )


def _read_profile_config(profile_dir: Path, reasons: list[str]) -> dict[str, Any]:
    config_path = profile_dir / "config.yaml"
    if not config_path.is_file():
        reasons.append("config_yaml_missing")
        return {}
    try:
        import yaml

        with config_path.open("r", encoding="utf-8") as stream:
            loaded = yaml.safe_load(stream) or {}
        if not isinstance(loaded, dict):
            reasons.append("config_yaml_not_object")
            return {}
        return loaded
    except Exception:
        reasons.append("config_yaml_unreadable")
        return {}


def _profile_config_cli_toolsets(config: dict[str, Any]) -> list[str]:
    platform_toolsets = config.get("platform_toolsets") if isinstance(config, dict) else None
    if not isinstance(platform_toolsets, dict):
        return []
    cli_toolsets = platform_toolsets.get("cli")
    if not isinstance(cli_toolsets, list):
        return []
    return [str(item).strip() for item in cli_toolsets if str(item).strip()]


def _validation_result(
    profile_dir: Path,
    contract: dict[str, Any],
    reasons: list[str],
) -> dict[str, Any]:
    return {
        "ok": not reasons,
        "canonical_profile": PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
        "profile_path": str(profile_dir),
        "rejection_reasons": reasons,
        "contract": contract,
        "legacy_auth_json_used": False,
        "API_key_fallback_used": False,
        "credential_pool_fallback_used": False,
        "projection_performed": False,
        "dispatch_performed": False,
        "worker_execution": False,
        "Git_mutation": False,
        "Docker_invocation": False,
        "Graphify_invocation": False,
    }


def _missing_profile_validation(profile_dir: Path) -> dict[str, Any]:
    return _validation_result(
        profile_dir,
        canonical_pepper_implementation_profile_contract(),
        ["profile_directory_missing"],
    )


def _public_runtime(runtime: dict[str, Any] | None) -> dict[str, Any] | None:
    if not runtime:
        return None
    keys = (
        "provider",
        "model",
        "api_mode",
        "credential_profile_id",
        "credential_policy_revision",
        "provider_runtime_profile_id",
        "worker_profile_id",
        "executor_config_source",
    )
    return {key: runtime[key] for key in keys if key in runtime}


def _safe_text(value: object) -> str:
    return "".join(character for character in str(value) if 32 <= ord(character) < 127)[
        :120
    ]


__all__ = [
    "CANONICAL_PROFILE_CONTRACT_MISMATCH",
    "HUMAN_PROFILE_SELECTION_REQUIRED",
    "NON_CANONICAL_IMPLEMENTATION_PROFILE_PRESENT",
    "PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME",
    "PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_PROVISION_COMMAND",
    "PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_STATUS_COMMAND",
    "PROFILE_ALREADY_PRESENT",
    "PROFILE_PROVISIONED",
    "PepperExecutionProfileProvisioningError",
    "READY_FOR_HUMAN_PROVISIONING",
    "READY_FOR_P18_9_1_PROJECTION",
    "assert_pepper_implementation_profile",
    "canonical_pepper_implementation_profile_contract",
    "inspect_pepper_implementation_profile_provisioning",
    "provision_pepper_implementation_profile",
    "validate_pepper_implementation_profile_contract",
]
