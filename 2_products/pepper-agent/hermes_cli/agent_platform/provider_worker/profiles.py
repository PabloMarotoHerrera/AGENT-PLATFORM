"""Immutable registry for governed bounded provider-worker profiles."""

from __future__ import annotations

from types import MappingProxyType

from hermes_cli.agent_platform.provider_worker.contracts import (
    BoundedProviderWorkerProfile,
)


class ProviderWorkerError(RuntimeError):
    """Base class for bounded provider-worker errors."""

    error_code = "provider_worker_error"

    def __init__(
        self,
        *,
        worker_profile_id: str | None = None,
        provider_profile_id: str | None = None,
        validation_category: str | None = None,
    ) -> None:
        self.worker_profile_id = worker_profile_id
        self.provider_profile_id = provider_profile_id
        self.validation_category = validation_category
        fragments = [f"code={self.error_code}"]
        if worker_profile_id is not None:
            fragments.append(f"worker_profile_id={worker_profile_id}")
        if provider_profile_id is not None:
            fragments.append(f"provider_profile_id={provider_profile_id}")
        if validation_category is not None:
            fragments.append(f"validation_category={validation_category}")
        super().__init__(" ".join(fragments))


class UnknownProviderWorkerProfileError(ProviderWorkerError):
    """Raised when a requested worker profile is not registered."""

    error_code = "unknown_provider_worker_profile"


OPENAI_CODEX_BOUNDED_PROVIDER_WORKER_PROFILE = BoundedProviderWorkerProfile()

_PROVIDER_WORKER_PROFILES = MappingProxyType({
    OPENAI_CODEX_BOUNDED_PROVIDER_WORKER_PROFILE.profile_id: (
        OPENAI_CODEX_BOUNDED_PROVIDER_WORKER_PROFILE
    )
})


def get_provider_worker_profile(profile_id: str) -> BoundedProviderWorkerProfile:
    """Resolve an immutable bounded worker profile by exact ID."""

    try:
        return _PROVIDER_WORKER_PROFILES[str(profile_id).strip()]
    except KeyError as exc:
        raise UnknownProviderWorkerProfileError(
            worker_profile_id=str(profile_id),
            validation_category="unknown_profile",
        ) from exc


def list_provider_worker_profiles() -> tuple[BoundedProviderWorkerProfile, ...]:
    """Return registered bounded worker profiles in deterministic order."""

    return tuple(
        _PROVIDER_WORKER_PROFILES[key] for key in sorted(_PROVIDER_WORKER_PROFILES)
    )


def list_provider_worker_profile_ids() -> tuple[str, ...]:
    """Return registered bounded worker profile IDs in deterministic order."""

    return tuple(sorted(_PROVIDER_WORKER_PROFILES))


__all__ = [
    "OPENAI_CODEX_BOUNDED_PROVIDER_WORKER_PROFILE",
    "ProviderWorkerError",
    "UnknownProviderWorkerProfileError",
    "get_provider_worker_profile",
    "list_provider_worker_profile_ids",
    "list_provider_worker_profiles",
]
