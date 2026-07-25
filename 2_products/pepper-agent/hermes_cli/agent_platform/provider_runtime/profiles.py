"""Immutable registry for governed provider-runtime profiles."""

from __future__ import annotations

from types import MappingProxyType

from hermes_cli.agent_platform.provider_runtime.contracts import ProviderRuntimeProfile


OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE = ProviderRuntimeProfile()

_PROVIDER_RUNTIME_PROFILES = MappingProxyType({
    OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE.profile_id: OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE
})


class UnknownProviderRuntimeProfileError(ValueError):
    """Raised when a requested provider-runtime profile is not registered."""


def get_provider_runtime_profile(profile_id: str) -> ProviderRuntimeProfile:
    """Resolve an immutable provider-runtime profile by exact ID."""

    try:
        return _PROVIDER_RUNTIME_PROFILES[str(profile_id).strip()]
    except KeyError as exc:
        raise UnknownProviderRuntimeProfileError(
            "unknown provider-runtime profile"
        ) from exc


def list_provider_runtime_profiles() -> tuple[ProviderRuntimeProfile, ...]:
    """Return registered provider-runtime profiles in deterministic order."""

    return tuple(
        _PROVIDER_RUNTIME_PROFILES[key] for key in sorted(_PROVIDER_RUNTIME_PROFILES)
    )


def list_provider_runtime_profile_ids() -> tuple[str, ...]:
    """Return registered provider-runtime profile IDs in deterministic order."""

    return tuple(sorted(_PROVIDER_RUNTIME_PROFILES))


__all__ = [
    "OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE",
    "UnknownProviderRuntimeProfileError",
    "get_provider_runtime_profile",
    "list_provider_runtime_profile_ids",
    "list_provider_runtime_profiles",
]
