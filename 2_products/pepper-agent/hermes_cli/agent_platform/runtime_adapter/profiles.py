"""Tracked runtime profiles for the governed Hermes runtime adapter."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

from hermes_cli.agent_platform.runtime_adapter.contracts import (
    PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID,
    TEST_LIFECYCLE_PROBE_PROFILE_ID,
    RuntimeProfileRef,
    RuntimeTimeoutPolicy,
    RuntimeWorkspaceBinding,
)
from hermes_cli.agent_platform.runtime_adapter.enums import (
    RuntimeProfileClass,
    RuntimeRetentionPolicy,
)


TEST_ENVIRONMENT_POLICY_ID = "runtime.environment.test.lifecycle_probe.v1"
DASHBOARD_ENVIRONMENT_POLICY_ID = "runtime.environment.pepper.dashboard.provider_null.v1"
TEST_WORKSPACE_POLICY_ID = "runtime.workspace.test.lifecycle_probe.v1"
DASHBOARD_WORKSPACE_POLICY_ID = "runtime.workspace.pepper.dashboard.provider_null.v1"
TEST_READINESS_POLICY_ID = "runtime.readiness.test.lifecycle_probe.v1"
DASHBOARD_READINESS_POLICY_ID = "runtime.readiness.pepper.dashboard.provider_null.v1"
TEST_SHUTDOWN_POLICY_ID = "runtime.shutdown.test.lifecycle_probe.v1"
DASHBOARD_SHUTDOWN_POLICY_ID = "runtime.shutdown.pepper.dashboard.provider_null.v1"
DASHBOARD_FILES_ROOT_POLICY_ID = "runtime.files.pepper.dashboard.locked.v1"

REGISTERED_ENVIRONMENT_POLICY_IDS = (
    TEST_ENVIRONMENT_POLICY_ID,
    DASHBOARD_ENVIRONMENT_POLICY_ID,
)


class RuntimeProfileRegistryError(RuntimeError):
    """Base class for bounded runtime-profile registry errors."""

    error_code = "runtime_profile_registry_error"

    def __init__(
        self,
        *,
        profile_id: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.profile_id = profile_id
        self.validation_category = validation_category
        fragments = [f"code={self.error_code}"]
        if profile_id is not None:
            fragments.append(f"profile_id={profile_id}")
        if validation_category is not None:
            fragments.append(f"validation_category={validation_category}")
        super().__init__(" ".join(fragments))


class UnknownRuntimeProfileError(RuntimeProfileRegistryError):
    """Raised when a stable runtime profile ID is not registered."""

    error_code = "unknown_runtime_profile"


class InvalidRuntimeProfileDefinitionError(RuntimeProfileRegistryError):
    """Raised when a tracked profile definition violates P14 invariants."""

    error_code = "invalid_runtime_profile_definition"


class RuntimeExecutableSelector(StrEnum):
    """Logical executable selectors resolved by later governed tickets."""

    CURRENT_PRODUCT_PYTHON = "current_product_python"


class RuntimeArgumentSelector(StrEnum):
    """Logical argument selectors resolved by later governed tickets."""

    LIFECYCLE_PROBE = "lifecycle_probe"
    PEPPER_DASHBOARD_PROVIDER_NULL = "pepper_dashboard_provider_null"


class RuntimeExecutionScope(StrEnum):
    """Execution scopes authorized for tracked P14 runtime profiles."""

    INERT_TEST_ONLY = "inert_test_only"
    P14_8_ONLY = "p14_8_only"


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeProfileDefinition:
    """Internal immutable runtime profile definition."""

    profile_ref: RuntimeProfileRef
    executable_selector: RuntimeExecutableSelector
    argument_selector: RuntimeArgumentSelector
    execution_scope: RuntimeExecutionScope
    timeout_policy: RuntimeTimeoutPolicy
    default_workspace_binding: RuntimeWorkspaceBinding

    def __repr__(self) -> str:
        return (
            "RuntimeProfileDefinition("
            f"profile_id={self.profile_ref.profile_id!r}, "
            f"profile_class={self.profile_ref.profile_class.value!r}, "
            f"execution_scope={self.execution_scope.value!r}, "
            f"environment_policy_id={self.profile_ref.environment_policy_id!r}, "
            f"workspace_policy_id={self.profile_ref.workspace_policy_id!r}, "
            f"readiness_policy_id={self.profile_ref.readiness_policy_id!r}, "
            f"shutdown_policy_id={self.profile_ref.shutdown_policy_id!r}, "
            f"files_root_policy_id={self.profile_ref.files_root_policy_id!r})"
        )


def get_runtime_profile(profile_id: str) -> RuntimeProfileDefinition:
    """Return one tracked runtime profile or fail closed."""

    profile = _PROFILE_BY_ID.get(profile_id)
    if profile is None:
        raise UnknownRuntimeProfileError(profile_id=profile_id)
    return profile


def list_runtime_profiles() -> tuple[RuntimeProfileDefinition, ...]:
    """Return tracked runtime profiles in deterministic registry order."""

    return _PROFILE_DEFINITIONS


def list_runtime_profile_ids() -> tuple[str, ...]:
    """Return tracked runtime profile IDs in deterministic registry order."""

    return tuple(profile.profile_ref.profile_id for profile in _PROFILE_DEFINITIONS)


def _build_profiles() -> tuple[RuntimeProfileDefinition, ...]:
    profiles = (
        RuntimeProfileDefinition(
            profile_ref=RuntimeProfileRef(
                profile_id=TEST_LIFECYCLE_PROBE_PROFILE_ID,
                profile_class=RuntimeProfileClass.TEST_LIFECYCLE_PROBE,
                environment_policy_id=TEST_ENVIRONMENT_POLICY_ID,
                workspace_policy_id=TEST_WORKSPACE_POLICY_ID,
                readiness_policy_id=TEST_READINESS_POLICY_ID,
                shutdown_policy_id=TEST_SHUTDOWN_POLICY_ID,
                files_root_policy_id=None,
            ),
            executable_selector=RuntimeExecutableSelector.CURRENT_PRODUCT_PYTHON,
            argument_selector=RuntimeArgumentSelector.LIFECYCLE_PROBE,
            execution_scope=RuntimeExecutionScope.INERT_TEST_ONLY,
            timeout_policy=RuntimeTimeoutPolicy(
                readiness_timeout_ms=5000,
                graceful_shutdown_timeout_ms=2000,
                forced_termination_timeout_ms=5000,
                poll_interval_ms=100,
                max_stdout_bytes=65_536,
                max_stderr_bytes=65_536,
            ),
            default_workspace_binding=RuntimeWorkspaceBinding(
                workspace_policy_id=TEST_WORKSPACE_POLICY_ID,
                retention_policy=RuntimeRetentionPolicy.REMOVE_ON_TERMINAL,
                require_managed_files_root=False,
            ),
        ),
        RuntimeProfileDefinition(
            profile_ref=RuntimeProfileRef(
                profile_id=PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID,
                profile_class=RuntimeProfileClass.PEPPER_DASHBOARD_PROVIDER_NULL,
                environment_policy_id=DASHBOARD_ENVIRONMENT_POLICY_ID,
                workspace_policy_id=DASHBOARD_WORKSPACE_POLICY_ID,
                readiness_policy_id=DASHBOARD_READINESS_POLICY_ID,
                shutdown_policy_id=DASHBOARD_SHUTDOWN_POLICY_ID,
                files_root_policy_id=DASHBOARD_FILES_ROOT_POLICY_ID,
            ),
            executable_selector=RuntimeExecutableSelector.CURRENT_PRODUCT_PYTHON,
            argument_selector=RuntimeArgumentSelector.PEPPER_DASHBOARD_PROVIDER_NULL,
            execution_scope=RuntimeExecutionScope.P14_8_ONLY,
            timeout_policy=RuntimeTimeoutPolicy(
                readiness_timeout_ms=30_000,
                graceful_shutdown_timeout_ms=5000,
                forced_termination_timeout_ms=10_000,
                poll_interval_ms=250,
                max_stdout_bytes=262_144,
                max_stderr_bytes=262_144,
            ),
            default_workspace_binding=RuntimeWorkspaceBinding(
                workspace_policy_id=DASHBOARD_WORKSPACE_POLICY_ID,
                retention_policy=RuntimeRetentionPolicy.REMOVE_ON_TERMINAL,
                require_managed_files_root=True,
            ),
        ),
    )
    _validate_profiles(profiles)
    return profiles


def _validate_profiles(profiles: tuple[RuntimeProfileDefinition, ...]) -> None:
    profile_ids = [profile.profile_ref.profile_id for profile in profiles]
    if len(profile_ids) != len(set(profile_ids)):
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="duplicate_profile_id"
        )
    if tuple(profile_ids) != (
        TEST_LIFECYCLE_PROBE_PROFILE_ID,
        PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID,
    ):
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="unexpected_profile_order"
        )

    environment_policy_ids = set(REGISTERED_ENVIRONMENT_POLICY_IDS)
    for profile in profiles:
        profile_ref = profile.profile_ref
        if profile_ref.environment_policy_id not in environment_policy_ids:
            raise InvalidRuntimeProfileDefinitionError(
                profile_id=profile_ref.profile_id,
                validation_category="unknown_environment_policy_id",
            )
        if profile_ref.profile_class is RuntimeProfileClass.TEST_LIFECYCLE_PROBE:
            _validate_test_profile(profile)
        elif (
            profile_ref.profile_class
            is RuntimeProfileClass.PEPPER_DASHBOARD_PROVIDER_NULL
        ):
            _validate_dashboard_profile(profile)
        else:
            raise InvalidRuntimeProfileDefinitionError(
                profile_id=profile_ref.profile_id,
                validation_category="unauthorized_profile_class",
            )


def _validate_test_profile(profile: RuntimeProfileDefinition) -> None:
    if profile.profile_ref.profile_id != TEST_LIFECYCLE_PROBE_PROFILE_ID:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="test_profile_id"
        )
    if profile.argument_selector is not RuntimeArgumentSelector.LIFECYCLE_PROBE:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="test_argument_selector"
        )
    if profile.execution_scope is not RuntimeExecutionScope.INERT_TEST_ONLY:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="test_execution_scope"
        )
    if profile.profile_ref.files_root_policy_id is not None:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="test_files_root_policy"
        )
    if profile.default_workspace_binding.require_managed_files_root:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="test_managed_files_root"
        )


def _validate_dashboard_profile(profile: RuntimeProfileDefinition) -> None:
    if profile.profile_ref.profile_id != PEPPER_DASHBOARD_PROVIDER_NULL_PROFILE_ID:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="dashboard_profile_id"
        )
    if (
        profile.argument_selector
        is not RuntimeArgumentSelector.PEPPER_DASHBOARD_PROVIDER_NULL
    ):
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="dashboard_argument_selector"
        )
    if profile.execution_scope is not RuntimeExecutionScope.P14_8_ONLY:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="dashboard_execution_scope"
        )
    if profile.profile_ref.files_root_policy_id != DASHBOARD_FILES_ROOT_POLICY_ID:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="dashboard_files_root_policy"
        )
    if not profile.default_workspace_binding.require_managed_files_root:
        raise InvalidRuntimeProfileDefinitionError(
            validation_category="dashboard_managed_files_root"
        )


_PROFILE_DEFINITIONS = _build_profiles()
_PROFILE_BY_ID = MappingProxyType({
    profile.profile_ref.profile_id: profile for profile in _PROFILE_DEFINITIONS
})
