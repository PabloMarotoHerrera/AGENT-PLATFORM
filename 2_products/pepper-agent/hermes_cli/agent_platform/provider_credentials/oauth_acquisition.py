"""Internal fixed OAuth-acquisition boundary for OpenAI Codex credentials."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from hermes_cli.agent_platform.provider_credentials.contracts import (
    ProviderCredentialAcquisitionPlan,
    ProviderCredentialAcquisitionResult,
)


_FIXED_ARGV_SUFFIX = (
    "-m",
    "hermes_cli.main",
    "auth",
    "add",
    "openai-codex",
    "--type",
    "oauth",
)
_FIXED_ENVIRONMENT_KEYS = (
    "HERMES_HOME",
    "HOME",
    "USERPROFILE",
    "APPDATA",
    "LOCALAPPDATA",
    "PYTHONIOENCODING",
    "PYTHONUTF8",
)


class ProviderCredentialOAuthAcquisitionError(RuntimeError):
    """Base class for bounded OAuth-acquisition errors."""

    error_code = "provider_credential_oauth_acquisition_error"

    def __init__(self, *, validation_category: str) -> None:
        self.validation_category = _safe_text(validation_category)
        super().__init__(
            f"code={self.error_code} validation_category={self.validation_category}"
        )


class InvalidProviderCredentialOAuthPlanError(ProviderCredentialOAuthAcquisitionError):
    error_code = "invalid_provider_credential_oauth_plan"


@dataclass(frozen=True, slots=True, repr=False)
class ResolvedOpenAICodexOAuthAcquisition:
    """Internal resolved command details for trusted composition only."""

    public_plan: ProviderCredentialAcquisitionPlan
    command_argv: tuple[str, ...]
    working_directory: Path
    environment_items: tuple[tuple[str, str], ...]

    def __repr__(self) -> str:
        return (
            "ResolvedOpenAICodexOAuthAcquisition("
            f"argv_suffix={self.public_plan.command_argv_suffix!r}, "
            f"environment_keys={self.public_plan.environment_keys!r})"
        )


def _safe_text(value: object) -> str:
    return "".join(character for character in str(value) if 32 <= ord(character) < 127)[
        :120
    ]


def _validate_trusted_root(path: Path, *, category: str) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        raise InvalidProviderCredentialOAuthPlanError(validation_category=category)
    try:
        resolved = candidate.resolve(strict=False)
    except (OSError, RuntimeError):
        raise InvalidProviderCredentialOAuthPlanError(
            validation_category=f"{category}_resolve_failed"
        ) from None
    if resolved == Path(resolved.anchor):
        raise InvalidProviderCredentialOAuthPlanError(
            validation_category=f"{category}_filesystem_root"
        )
    return resolved


def build_openai_codex_oauth_acquisition_plan(
    *,
    product_root: Path,
    trusted_acquisition_root: Path,
) -> ResolvedOpenAICodexOAuthAcquisition:
    """Build the only allowed Hermes command for Codex ChatGPT OAuth."""

    product_dir = _validate_trusted_root(
        product_root, category="product_root_not_absolute"
    )
    acquisition_root = _validate_trusted_root(
        trusted_acquisition_root,
        category="acquisition_root_not_absolute",
    )
    isolated_home = acquisition_root / "home"
    public_plan = ProviderCredentialAcquisitionPlan(
        command_argv_suffix=_FIXED_ARGV_SUFFIX,
        environment_keys=_FIXED_ENVIRONMENT_KEYS,
    )
    return ResolvedOpenAICodexOAuthAcquisition(
        public_plan=public_plan,
        command_argv=("python", *_FIXED_ARGV_SUFFIX),
        working_directory=product_dir,
        environment_items=(
            ("HERMES_HOME", str(isolated_home)),
            ("HOME", str(isolated_home)),
            ("USERPROFILE", str(isolated_home)),
            ("APPDATA", str(acquisition_root / "appdata")),
            ("LOCALAPPDATA", str(acquisition_root / "localappdata")),
            ("PYTHONIOENCODING", "utf-8"),
            ("PYTHONUTF8", "1"),
        ),
    )


def run_openai_codex_oauth_acquisition(
    plan: ResolvedOpenAICodexOAuthAcquisition,
    *,
    executor: Callable[[Sequence[str], dict[str, str], Path], object] | None = None,
) -> ProviderCredentialAcquisitionResult:
    """Run only through an explicitly injected executor; default is dry-run."""

    if executor is None:
        return ProviderCredentialAcquisitionResult(
            execution_attempted=False,
            completed=False,
            message="OAuth acquisition execution disabled by default",
        )
    env = {key: value for key, value in plan.environment_items}
    result = executor(plan.command_argv, env, plan.working_directory)
    exit_code = int(getattr(result, "returncode", 0) or 0)
    stdout = getattr(result, "stdout", b"") or b""
    stderr = getattr(result, "stderr", b"") or b""
    return ProviderCredentialAcquisitionResult(
        execution_attempted=True,
        completed=exit_code == 0,
        exit_code=exit_code,
        stdout_bytes=len(stdout),
        stderr_bytes=len(stderr),
        message="OAuth acquisition executor completed",
    )


__all__ = [
    "InvalidProviderCredentialOAuthPlanError",
    "ProviderCredentialOAuthAcquisitionError",
    "ResolvedOpenAICodexOAuthAcquisition",
    "build_openai_codex_oauth_acquisition_plan",
    "run_openai_codex_oauth_acquisition",
]
