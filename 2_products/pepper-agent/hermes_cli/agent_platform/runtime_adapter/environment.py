"""Pure runtime environment sanitization for governed runtime profiles."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath, PureWindowsPath
from types import MappingProxyType

from hermes_cli.agent_platform.runtime_adapter.profiles import (
    DASHBOARD_ENVIRONMENT_POLICY_ID,
    TEST_ENVIRONMENT_POLICY_ID,
    RuntimeProfileDefinition,
)


_MAX_SOURCE_ENVIRONMENT_ENTRIES = 4096
_MAX_OUTPUT_ENVIRONMENT_ENTRIES = 128
_MAX_ENVIRONMENT_NAME_CHARACTERS = 256
_MAX_ENVIRONMENT_VALUE_CHARACTERS = 16_384
_MAX_EXPLICIT_PATH_ENTRIES = 16
_MAX_PATH_CHARACTERS = 4096
_MAX_EXCLUDED_SENSITIVE_NAMES = 64
_WINDOWS_TOTAL_ENVIRONMENT_CHARACTERS = 30_000
_POSIX_TOTAL_ENVIRONMENT_CHARACTERS = 131_072

_MANAGED_VARIABLE_NAMES = (
    "HERMES_HOME",
    "HOME",
    "USERPROFILE",
    "APPDATA",
    "LOCALAPPDATA",
    "TEMP",
    "TMP",
    "TMPDIR",
)
_WINDOWS_EXTRA_MANAGED_VARIABLE_NAMES = ("HOMEDRIVE", "HOMEPATH")
_FIXED_ENVIRONMENT_ITEMS = (
    ("PYTHONIOENCODING", "utf-8"),
    ("PYTHONDONTWRITEBYTECODE", "1"),
    ("PYTHONUNBUFFERED", "1"),
    ("PYTHONUTF8", "1"),
)
_WINDOWS_BOOTSTRAP_NAMES = ("SystemRoot", "WINDIR")

_DENIED_PREFIXES = (
    "AWS_",
    "AZURE_",
    "GOOGLE_",
    "OPENAI_",
    "ANTHROPIC_",
    "COHERE_",
    "MISTRAL_",
    "GROQ_",
    "HF_",
    "HUGGINGFACE_",
    "GITHUB_",
    "GITLAB_",
    "GH_",
    "MCP_",
    "NPM_",
    "PYPI_",
)
_DENIED_SUFFIXES = (
    "_API_KEY",
    "_TOKEN",
    "_SECRET",
    "_PASSWORD",
    "_CREDENTIAL",
    "_CREDENTIALS",
)
_DENIED_EXACT_NAMES = frozenset({
    "DATABASE_URL",
    "KUBECONFIG",
    "SSH_AUTH_SOCK",
    "SSH_AGENT_PID",
    "GIT_ASKPASS",
    "GIT_CONFIG_GLOBAL",
    "GIT_CONFIG_SYSTEM",
    "GIT_SSH_COMMAND",
    "GIT_EXEC_PATH",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
    "PYTHONPATH",
    "PYTHONHOME",
    "VIRTUAL_ENV",
    "CONDA_PREFIX",
    "CONDA_DEFAULT_ENV",
    "PIP_CONFIG_FILE",
    "NODE_OPTIONS",
    "NODE_PATH",
    "LD_PRELOAD",
    "LD_LIBRARY_PATH",
    "DYLD_INSERT_LIBRARIES",
    "DYLD_LIBRARY_PATH",
})
_PROVIDER_PREFIXES = (
    "AWS_",
    "AZURE_",
    "GOOGLE_",
    "OPENAI_",
    "ANTHROPIC_",
    "COHERE_",
    "MISTRAL_",
    "GROQ_",
    "HF_",
    "HUGGINGFACE_",
)


class RuntimeEnvironmentError(RuntimeError):
    """Base class for bounded runtime-environment errors."""

    error_code = "runtime_environment_error"

    def __init__(
        self,
        *,
        profile_id: str | None = None,
        policy_id: str | None = None,
        variable_name: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.profile_id = profile_id
        self.policy_id = policy_id
        self.variable_name = variable_name
        self.validation_category = validation_category
        fragments = [f"code={self.error_code}"]
        if profile_id is not None:
            fragments.append(f"profile_id={profile_id}")
        if policy_id is not None:
            fragments.append(f"policy_id={policy_id}")
        if variable_name is not None:
            fragments.append(f"variable_name={_safe_name(variable_name)}")
        if validation_category is not None:
            fragments.append(f"validation_category={validation_category}")
        super().__init__(" ".join(fragments))


class UnknownEnvironmentPolicyError(RuntimeEnvironmentError):
    error_code = "unknown_environment_policy"


class InvalidRuntimeEnvironmentPathError(RuntimeEnvironmentError):
    error_code = "invalid_runtime_environment_path"


class InvalidRuntimeEnvironmentVariableError(RuntimeEnvironmentError):
    error_code = "invalid_runtime_environment_variable"


class MissingRuntimeBootstrapVariableError(RuntimeEnvironmentError):
    error_code = "missing_runtime_bootstrap_variable"


class ForbiddenRuntimeEnvironmentVariableError(RuntimeEnvironmentError):
    error_code = "forbidden_runtime_environment_variable"


class RuntimeEnvironmentTooLargeError(RuntimeEnvironmentError):
    error_code = "runtime_environment_too_large"


class RuntimePlatformFamily(StrEnum):
    """Explicit platform family selected by a trusted caller boundary."""

    WINDOWS = "windows"
    POSIX = "posix"


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeEnvironmentPaths:
    """Adapter-controlled runtime path values supplied by P14.4."""

    hermes_home: str
    home: str
    user_profile: str
    app_data: str
    local_app_data: str
    temp: str
    files_root: str | None

    def __repr__(self) -> str:
        supplied = [
            name
            for name, value in (
                ("hermes_home", self.hermes_home),
                ("home", self.home),
                ("user_profile", self.user_profile),
                ("app_data", self.app_data),
                ("local_app_data", self.local_app_data),
                ("temp", self.temp),
                ("files_root", self.files_root),
            )
            if value is not None
        ]
        return f"RuntimeEnvironmentPaths(fields={tuple(supplied)!r})"


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeEnvironmentPolicyDefinition:
    """Tracked environment policy attached to a runtime profile."""

    policy_id: str
    allow_explicit_path_entries: bool
    managed_files_root_required: bool

    def __repr__(self) -> str:
        return (
            "RuntimeEnvironmentPolicyDefinition("
            f"policy_id={self.policy_id!r}, "
            f"allow_explicit_path_entries={self.allow_explicit_path_entries!r}, "
            f"managed_files_root_required={self.managed_files_root_required!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeEnvironmentSanitizationReport:
    """Secret-free environment sanitization evidence for later normalization."""

    profile_id: str
    environment_policy_id: str
    platform_family: RuntimePlatformFamily
    source_variable_count: int
    output_variable_count: int
    inherited_variable_names: tuple[str, ...]
    managed_variable_names: tuple[str, ...]
    fixed_variable_names: tuple[str, ...]
    explicit_path_entry_count: int
    excluded_variable_count: int
    excluded_sensitive_variable_names: tuple[str, ...]
    managed_home_bound: bool
    managed_files_root_required: bool
    managed_files_root_supplied: bool
    provider_variables_present_in_output: bool

    def __post_init__(self) -> None:
        for field_name in (
            "inherited_variable_names",
            "managed_variable_names",
            "fixed_variable_names",
            "excluded_sensitive_variable_names",
        ):
            values = getattr(self, field_name)
            if values != tuple(sorted(values)):
                raise ValueError(f"{field_name} must be sorted")
        if len(self.excluded_sensitive_variable_names) > _MAX_EXCLUDED_SENSITIVE_NAMES:
            raise ValueError("excluded_sensitive_variable_names is too large")
        if self.provider_variables_present_in_output:
            raise ValueError("provider variables must not be present in output")

    def __repr__(self) -> str:
        return (
            "RuntimeEnvironmentSanitizationReport("
            f"profile_id={self.profile_id!r}, "
            f"environment_policy_id={self.environment_policy_id!r}, "
            f"platform_family={self.platform_family.value!r}, "
            f"source_variable_count={self.source_variable_count}, "
            f"output_variable_count={self.output_variable_count}, "
            f"excluded_variable_count={self.excluded_variable_count})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class SanitizedRuntimeEnvironment:
    """Immutable sanitized environment output for P14.2 launch plans."""

    profile_id: str
    environment_policy_id: str
    platform_family: RuntimePlatformFamily
    items: tuple[tuple[str, str], ...]
    report: RuntimeEnvironmentSanitizationReport

    def __post_init__(self) -> None:
        items = tuple((key, value) for key, value in self.items)
        _validate_output_items(
            items, self.platform_family, self.profile_id, self.environment_policy_id
        )
        object.__setattr__(self, "items", items)

    def __repr__(self) -> str:
        return (
            "SanitizedRuntimeEnvironment("
            f"profile_id={self.profile_id!r}, "
            f"environment_policy_id={self.environment_policy_id!r}, "
            f"platform_family={self.platform_family.value!r}, "
            f"item_count={len(self.items)})"
        )

    def as_mapping(self) -> dict[str, str]:
        """Return a new mutable mapping copy for a future launch plan."""

        return dict(self.items)


def sanitize_runtime_environment(
    *,
    profile: RuntimeProfileDefinition,
    platform_family: RuntimePlatformFamily,
    source_environment: Mapping[str, str],
    paths: RuntimeEnvironmentPaths,
    explicit_path_entries: tuple[str, ...] = (),
) -> SanitizedRuntimeEnvironment:
    """Build a deterministic, secret-free child environment from explicit input."""

    if not isinstance(platform_family, RuntimePlatformFamily):
        platform_family = RuntimePlatformFamily(platform_family)
    policy = _environment_policy_for(profile)
    _validate_source_environment(source_environment, platform_family, profile, policy)
    _validate_paths(paths, platform_family, policy, profile)
    path_entries = _validate_explicit_path_entries(
        explicit_path_entries,
        platform_family,
        policy,
        profile,
    )

    excluded_sensitive_names = _sensitive_source_names(source_environment)
    output: dict[str, str] = {}
    inherited_names: list[str] = []

    if platform_family is RuntimePlatformFamily.WINDOWS:
        bootstrap_value = _windows_bootstrap_value(source_environment, profile, policy)
        for key in _WINDOWS_BOOTSTRAP_NAMES:
            output[key] = bootstrap_value
            inherited_names.append(key)

    managed = _managed_environment_items(paths, platform_family)
    output.update(dict(managed))
    output.update(dict(_FIXED_ENVIRONMENT_ITEMS))

    if path_entries:
        separator = ";" if platform_family is RuntimePlatformFamily.WINDOWS else ":"
        output["PATH"] = separator.join(path_entries)

    output_items = tuple(
        sorted(output.items(), key=lambda item: _sort_key(item[0], platform_family))
    )
    _validate_output_items(
        output_items, platform_family, profile.profile_ref.profile_id, policy.policy_id
    )
    _validate_no_denied_output(output_items, profile, policy)
    report = RuntimeEnvironmentSanitizationReport(
        profile_id=profile.profile_ref.profile_id,
        environment_policy_id=policy.policy_id,
        platform_family=platform_family,
        source_variable_count=len(source_environment),
        output_variable_count=len(output_items),
        inherited_variable_names=tuple(sorted(inherited_names)),
        managed_variable_names=tuple(sorted(key for key, _value in managed)),
        fixed_variable_names=tuple(
            sorted(key for key, _value in _FIXED_ENVIRONMENT_ITEMS)
        ),
        explicit_path_entry_count=len(path_entries),
        excluded_variable_count=len(excluded_sensitive_names),
        excluded_sensitive_variable_names=tuple(
            excluded_sensitive_names[:_MAX_EXCLUDED_SENSITIVE_NAMES]
        ),
        managed_home_bound=_managed_home_bound(output, paths, platform_family),
        managed_files_root_required=policy.managed_files_root_required,
        managed_files_root_supplied=paths.files_root is not None,
        provider_variables_present_in_output=_provider_variable_present(output_items),
    )
    return SanitizedRuntimeEnvironment(
        profile_id=profile.profile_ref.profile_id,
        environment_policy_id=policy.policy_id,
        platform_family=platform_family,
        items=output_items,
        report=report,
    )


def _environment_policy_for(
    profile: RuntimeProfileDefinition,
) -> RuntimeEnvironmentPolicyDefinition:
    policy = _ENVIRONMENT_POLICY_BY_ID.get(profile.profile_ref.environment_policy_id)
    if policy is None:
        raise UnknownEnvironmentPolicyError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=profile.profile_ref.environment_policy_id,
        )
    return policy


def _validate_source_environment(
    source_environment: Mapping[str, str],
    platform_family: RuntimePlatformFamily,
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    if len(source_environment) > _MAX_SOURCE_ENVIRONMENT_ENTRIES:
        raise RuntimeEnvironmentTooLargeError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category="source_environment_entry_count",
        )
    seen_windows_names: set[str] = set()
    for key in source_environment:
        _validate_environment_name(key, profile, policy)
        if platform_family is RuntimePlatformFamily.WINDOWS:
            normalized = key.casefold()
            if normalized in seen_windows_names:
                raise InvalidRuntimeEnvironmentVariableError(
                    profile_id=profile.profile_ref.profile_id,
                    policy_id=policy.policy_id,
                    variable_name=key,
                    validation_category="duplicate_source_variable",
                )
            seen_windows_names.add(normalized)


def _validate_environment_name(
    name: str,
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    if not isinstance(name, str) or not name:
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category="empty_variable_name",
        )
    if len(name) > _MAX_ENVIRONMENT_NAME_CHARACTERS:
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category="variable_name_too_long",
        )
    if "=" in name:
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name=name,
            validation_category="variable_name_contains_equals",
        )
    if _has_nul_or_control(name):
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name=name,
            validation_category="variable_name_control_character",
        )


def _validate_environment_value(
    name: str,
    value: str,
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    if not isinstance(value, str):
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name=name,
            validation_category="variable_value_not_text",
        )
    if len(value) > _MAX_ENVIRONMENT_VALUE_CHARACTERS:
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name=name,
            validation_category="variable_value_too_long",
        )
    if "\x00" in value:
        raise InvalidRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name=name,
            validation_category="variable_value_nul",
        )


def _validate_paths(
    paths: RuntimeEnvironmentPaths,
    platform_family: RuntimePlatformFamily,
    policy: RuntimeEnvironmentPolicyDefinition,
    profile: RuntimeProfileDefinition,
) -> None:
    path_fields = (
        ("hermes_home", paths.hermes_home),
        ("home", paths.home),
        ("user_profile", paths.user_profile),
        ("app_data", paths.app_data),
        ("local_app_data", paths.local_app_data),
        ("temp", paths.temp),
    )
    for field_name, value in path_fields:
        _validate_lexical_path(field_name, value, platform_family, profile, policy)
    if paths.files_root is None:
        if policy.managed_files_root_required:
            raise InvalidRuntimeEnvironmentPathError(
                profile_id=profile.profile_ref.profile_id,
                policy_id=policy.policy_id,
                validation_category="files_root_required",
            )
    else:
        _validate_lexical_path(
            "files_root", paths.files_root, platform_family, profile, policy
        )


def _validate_lexical_path(
    field_name: str,
    value: str,
    platform_family: RuntimePlatformFamily,
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    if not isinstance(value, str) or not value:
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_empty",
        )
    if len(value) > _MAX_PATH_CHARACTERS:
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_too_long",
        )
    if _has_nul_or_control(value):
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_control_character",
        )
    if platform_family is RuntimePlatformFamily.WINDOWS:
        _validate_windows_path(field_name, value, profile, policy)
    else:
        _validate_posix_path(field_name, value, profile, policy)


def _validate_windows_path(
    field_name: str,
    value: str,
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    normalized = value.casefold()
    if normalized.startswith(("\\\\", "//", "\\?\\", "//?//", "\\.\\", "//.//")):
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_unsupported_windows_path",
        )
    path = PureWindowsPath(value)
    if not path.is_absolute() or not path.drive:
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_not_absolute",
        )
    if ".." in path.parts:
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_parent_segment",
        )


def _validate_posix_path(
    field_name: str,
    value: str,
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    path = PurePosixPath(value)
    if not path.is_absolute():
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_not_absolute",
        )
    if ".." in path.parts:
        raise InvalidRuntimeEnvironmentPathError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category=f"{field_name}_parent_segment",
        )


def _validate_explicit_path_entries(
    explicit_path_entries: tuple[str, ...],
    platform_family: RuntimePlatformFamily,
    policy: RuntimeEnvironmentPolicyDefinition,
    profile: RuntimeProfileDefinition,
) -> tuple[str, ...]:
    entries = tuple(explicit_path_entries)
    if entries and not policy.allow_explicit_path_entries:
        raise ForbiddenRuntimeEnvironmentVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name="PATH",
            validation_category="explicit_path_not_allowed",
        )
    if len(entries) > _MAX_EXPLICIT_PATH_ENTRIES:
        raise RuntimeEnvironmentTooLargeError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            variable_name="PATH",
            validation_category="explicit_path_entry_count",
        )
    seen: set[str] = set()
    for entry in entries:
        _validate_lexical_path("path_entry", entry, platform_family, profile, policy)
        key = (
            entry.casefold()
            if platform_family is RuntimePlatformFamily.WINDOWS
            else entry
        )
        if key in seen:
            raise InvalidRuntimeEnvironmentVariableError(
                profile_id=profile.profile_ref.profile_id,
                policy_id=policy.policy_id,
                variable_name="PATH",
                validation_category="duplicate_path_entry",
            )
        seen.add(key)
    return entries


def _windows_bootstrap_value(
    source_environment: Mapping[str, str],
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> str:
    lookup = {key.casefold(): key for key in source_environment}
    source_name = lookup.get("systemroot") or lookup.get("windir")
    if source_name is None:
        raise MissingRuntimeBootstrapVariableError(
            profile_id=profile.profile_ref.profile_id,
            policy_id=policy.policy_id,
            validation_category="windows_bootstrap_missing",
        )
    value = source_environment[source_name]
    _validate_environment_value(source_name, value, profile, policy)
    return value


def _managed_environment_items(
    paths: RuntimeEnvironmentPaths,
    platform_family: RuntimePlatformFamily,
) -> tuple[tuple[str, str], ...]:
    items = [
        ("HERMES_HOME", paths.hermes_home),
        ("HOME", paths.home),
        ("USERPROFILE", paths.user_profile),
        ("APPDATA", paths.app_data),
        ("LOCALAPPDATA", paths.local_app_data),
        ("TEMP", paths.temp),
        ("TMP", paths.temp),
        ("TMPDIR", paths.temp),
    ]
    if platform_family is RuntimePlatformFamily.WINDOWS:
        drive, home_path = _windows_drive_and_home_path(paths.user_profile)
        items.extend((("HOMEDRIVE", drive), ("HOMEPATH", home_path)))
    return tuple(items)


def _windows_drive_and_home_path(user_profile: str) -> tuple[str, str]:
    path = PureWindowsPath(user_profile)
    drive = path.drive
    suffix = user_profile[len(drive) :]
    if not suffix:
        suffix = "\\"
    elif not suffix.startswith(("\\", "/")):
        suffix = "\\" + suffix
    return drive, suffix


def _validate_output_items(
    items: tuple[tuple[str, str], ...],
    platform_family: RuntimePlatformFamily,
    profile_id: str,
    policy_id: str,
) -> None:
    if len(items) > _MAX_OUTPUT_ENVIRONMENT_ENTRIES:
        raise RuntimeEnvironmentTooLargeError(
            profile_id=profile_id,
            policy_id=policy_id,
            validation_category="output_environment_entry_count",
        )
    seen: set[str] = set()
    total_characters = 0
    for key, value in items:
        fake_profile = _ErrorProfile(profile_id)
        fake_policy = _ErrorPolicy(policy_id)
        _validate_environment_name(key, fake_profile, fake_policy)
        _validate_environment_value(key, value, fake_profile, fake_policy)
        normalized = (
            key.casefold() if platform_family is RuntimePlatformFamily.WINDOWS else key
        )
        if normalized in seen:
            raise InvalidRuntimeEnvironmentVariableError(
                profile_id=profile_id,
                policy_id=policy_id,
                variable_name=key,
                validation_category="duplicate_output_variable",
            )
        seen.add(normalized)
        total_characters += len(key) + len(value) + 2
    limit = (
        _WINDOWS_TOTAL_ENVIRONMENT_CHARACTERS
        if platform_family is RuntimePlatformFamily.WINDOWS
        else _POSIX_TOTAL_ENVIRONMENT_CHARACTERS
    )
    if total_characters > limit:
        raise RuntimeEnvironmentTooLargeError(
            profile_id=profile_id,
            policy_id=policy_id,
            validation_category="output_environment_total_size",
        )


def _validate_no_denied_output(
    items: tuple[tuple[str, str], ...],
    profile: RuntimeProfileDefinition,
    policy: RuntimeEnvironmentPolicyDefinition,
) -> None:
    for key, _value in items:
        normalized = key.upper()
        if _is_denied_name(normalized):
            raise ForbiddenRuntimeEnvironmentVariableError(
                profile_id=profile.profile_ref.profile_id,
                policy_id=policy.policy_id,
                variable_name=key,
                validation_category="denied_output_variable",
            )


def _sensitive_source_names(source_environment: Mapping[str, str]) -> tuple[str, ...]:
    names = [key for key in source_environment if _is_denied_name(key.upper())]
    return tuple(sorted(names, key=str.upper))


def _is_denied_name(normalized_name: str) -> bool:
    return (
        normalized_name in _DENIED_EXACT_NAMES
        or any(normalized_name.startswith(prefix) for prefix in _DENIED_PREFIXES)
        or any(normalized_name.endswith(suffix) for suffix in _DENIED_SUFFIXES)
    )


def _provider_variable_present(items: tuple[tuple[str, str], ...]) -> bool:
    for key, _value in items:
        normalized = key.upper()
        if any(normalized.startswith(prefix) for prefix in _PROVIDER_PREFIXES):
            return True
    return False


def _managed_home_bound(
    output: Mapping[str, str],
    paths: RuntimeEnvironmentPaths,
    platform_family: RuntimePlatformFamily,
) -> bool:
    required = {
        "HERMES_HOME": paths.hermes_home,
        "HOME": paths.home,
        "USERPROFILE": paths.user_profile,
        "APPDATA": paths.app_data,
        "LOCALAPPDATA": paths.local_app_data,
        "TEMP": paths.temp,
        "TMP": paths.temp,
        "TMPDIR": paths.temp,
    }
    if platform_family is RuntimePlatformFamily.WINDOWS:
        drive, home_path = _windows_drive_and_home_path(paths.user_profile)
        required["HOMEDRIVE"] = drive
        required["HOMEPATH"] = home_path
    return all(output.get(key) == value for key, value in required.items())


def _sort_key(name: str, platform_family: RuntimePlatformFamily) -> str:
    return name.casefold() if platform_family is RuntimePlatformFamily.WINDOWS else name


def _safe_name(name: str) -> str:
    return "".join(character for character in name if 32 <= ord(character) < 127)[:128]


def _has_nul_or_control(value: str) -> bool:
    return any(ord(character) < 32 for character in value)


@dataclass(frozen=True, slots=True)
class _ErrorProfile:
    profile_id: str

    @property
    def profile_ref(self):
        return self


@dataclass(frozen=True, slots=True)
class _ErrorPolicy:
    policy_id: str


_ENVIRONMENT_POLICIES = (
    RuntimeEnvironmentPolicyDefinition(
        policy_id=TEST_ENVIRONMENT_POLICY_ID,
        allow_explicit_path_entries=False,
        managed_files_root_required=False,
    ),
    RuntimeEnvironmentPolicyDefinition(
        policy_id=DASHBOARD_ENVIRONMENT_POLICY_ID,
        allow_explicit_path_entries=True,
        managed_files_root_required=True,
    ),
)
_ENVIRONMENT_POLICY_BY_ID = MappingProxyType({
    policy.policy_id: policy for policy in _ENVIRONMENT_POLICIES
})
