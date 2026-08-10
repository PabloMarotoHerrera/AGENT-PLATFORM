"""Pepper-owned provisioning adapter for the governed Codex credential."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_HERMES_PROVIDER_ID,
    ProviderCredentialStatus,
)
from hermes_cli.agent_platform.provider_credentials.oauth_acquisition import (
    build_openai_codex_oauth_acquisition_plan,
    run_openai_codex_oauth_acquisition,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionBackend,
    default_openai_codex_credential_store_root,
    extract_openai_codex_oauth_credential_from_auth_store_payload,
    promote_openai_codex_oauth_credential,
    read_openai_codex_credential_status,
)


OPENAI_CODEX_PRIMARY_PROVISION_COMMAND = (
    "hermes agent-platform auth add openai-codex.primary"
)


class GovernedCodexProvisioningError(RuntimeError):
    """Secret-free provisioning failure for the governed Codex profile."""

    error_code = "governed_codex_provisioning_error"

    def __init__(self, validation_category: str) -> None:
        self.validation_category = _safe_text(validation_category)
        super().__init__(
            f"code={self.error_code} validation_category={self.validation_category}"
        )


OAuthExecutor = Callable[[Sequence[str], dict[str, str], Path], object]


def _safe_text(value: object) -> str:
    return "".join(character for character in str(value) if 32 <= ord(character) < 127)[
        :120
    ]


def _default_product_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _interactive_oauth_executor(
    argv: Sequence[str],
    acquisition_env: dict[str, str],
    cwd: Path,
) -> subprocess.CompletedProcess:
    child_env = os.environ.copy()
    child_env.update(acquisition_env)
    return subprocess.run(
        list(argv),
        cwd=str(cwd),
        env=child_env,
        check=False,
    )


def read_openai_codex_primary_status(
    *,
    protection_backend: StoreProtectionBackend | None = None,
    now: Any = None,
) -> ProviderCredentialStatus:
    """Return a secret-free status for the governed Codex primary profile."""

    return read_openai_codex_credential_status(
        default_openai_codex_credential_store_root(),
        protection_backend=protection_backend,
        now=now,
    )


def provision_openai_codex_primary(
    *,
    product_root: Path | None = None,
    acquisition_root: Path | None = None,
    executor: OAuthExecutor | None = None,
    protection_backend: StoreProtectionBackend | None = None,
    now: Any = None,
) -> ProviderCredentialStatus:
    """Acquire OAuth in a temporary home, then promote into openai-codex.primary."""

    if acquisition_root is None:
        with tempfile.TemporaryDirectory(prefix="pepper-codex-oauth-") as tmp_dir:
            return _provision_openai_codex_primary_from_acquisition_root(
                product_root=product_root,
                acquisition_root=Path(tmp_dir),
                executor=executor,
                protection_backend=protection_backend,
                now=now,
            )
    return _provision_openai_codex_primary_from_acquisition_root(
        product_root=product_root,
        acquisition_root=acquisition_root,
        executor=executor,
        protection_backend=protection_backend,
        now=now,
    )


def _provision_openai_codex_primary_from_acquisition_root(
    *,
    product_root: Path | None,
    acquisition_root: Path,
    executor: OAuthExecutor | None,
    protection_backend: StoreProtectionBackend | None,
    now: Any,
) -> ProviderCredentialStatus:
    plan = build_openai_codex_oauth_acquisition_plan(
        product_root=product_root or _default_product_root(),
        trusted_acquisition_root=acquisition_root,
    )
    result = run_openai_codex_oauth_acquisition(
        plan,
        executor=executor or _interactive_oauth_executor,
    )
    if not result.completed:
        raise GovernedCodexProvisioningError("oauth_acquisition_failed")

    acquisition_home = dict(plan.environment_items).get("HERMES_HOME", "")
    if not acquisition_home:
        raise GovernedCodexProvisioningError("acquisition_home_missing")
    acquisition_auth_file = Path(acquisition_home) / "auth.json"
    if not acquisition_auth_file.is_file():
        raise GovernedCodexProvisioningError("acquisition_auth_store_missing")
    try:
        acquisition_payload = json.loads(
            acquisition_auth_file.read_text(encoding="utf-8")
        )
    except Exception:
        raise GovernedCodexProvisioningError("acquisition_auth_store_unreadable") from None

    credential = extract_openai_codex_oauth_credential_from_auth_store_payload(
        acquisition_payload,
        now=now,
    )
    return promote_openai_codex_oauth_credential(
        default_openai_codex_credential_store_root(),
        credential,
        protection_backend=protection_backend,
        now=now,
    )


def assert_openai_codex_primary_profile(profile_id: str) -> str:
    """Validate the only governed Codex profile accepted by Pepper."""

    normalized = str(profile_id or "").strip()
    if normalized != OPENAI_CODEX_CREDENTIAL_STORE_ID:
        raise GovernedCodexProvisioningError("credential_profile_mismatch")
    return normalized


__all__ = [
    "GovernedCodexProvisioningError",
    "OPENAI_CODEX_HERMES_PROVIDER_ID",
    "OPENAI_CODEX_PRIMARY_PROVISION_COMMAND",
    "assert_openai_codex_primary_profile",
    "provision_openai_codex_primary",
    "read_openai_codex_primary_status",
]
