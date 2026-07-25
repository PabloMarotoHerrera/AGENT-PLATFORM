"""Internal temp-projection lease boundary for provider credentials."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES,
    MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    PROVIDER_CREDENTIAL_SCHEMA_VERSION,
    ProviderCredentialDeliveryLease,
    ProviderCredentialLeaseCleanup,
    ProviderCredentialProvider,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionBackend,
    load_openai_codex_oauth_credential,
    promote_openai_codex_oauth_credential,
)
from hermes_cli.agent_platform.runtime_adapter.path_containment import (
    assert_existing_path_contained,
    assert_path_chain_safe,
    validate_safe_path_segment,
    validate_trusted_base_root,
)


LEASE_MARKER_NAME = ".agent-platform-provider-credential-lease.json"
_MAX_REMOVED_PATHS = 512


class ProviderCredentialDeliveryError(RuntimeError):
    """Base class for bounded credential-delivery errors."""

    error_code = "provider_credential_delivery_error"

    def __init__(self, *, validation_category: str, detail: str | None = None) -> None:
        self.validation_category = _safe_text(validation_category)
        self.detail = _safe_text(detail) if detail else None
        fragments = [
            f"code={self.error_code}",
            f"validation_category={self.validation_category}",
        ]
        if self.detail:
            fragments.append(f"detail={self.detail}")
        super().__init__(" ".join(fragments))


class InvalidProviderCredentialLeaseError(ProviderCredentialDeliveryError):
    error_code = "invalid_provider_credential_lease"


class ProviderCredentialLeaseCleanupError(ProviderCredentialDeliveryError):
    error_code = "provider_credential_lease_cleanup_error"


@dataclass(frozen=True, slots=True, repr=False)
class ProviderCredentialProjection:
    """Internal projection details for trusted runtime composition only."""

    lease_ref: ProviderCredentialDeliveryLease
    projected_hermes_home: Path
    auth_file_path: Path
    environment_items: tuple[tuple[str, str], ...]

    def __repr__(self) -> str:
        return (
            "ProviderCredentialProjection("
            f"lease_id={self.lease_ref.lease_id!r}, "
            f"environment_keys={tuple(key for key, _value in self.environment_items)!r})"
        )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_text(value: object) -> str:
    return "".join(character for character in str(value) if 32 <= ord(character) < 127)[
        :120
    ]


def _format_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _new_lease_id() -> str:
    return f"lease.{uuid.uuid4().hex}"


def _validate_lease_id(lease_id: str) -> str:
    return validate_safe_path_segment(lease_id)


def _validate_ttl_ms(ttl_ms: int) -> int:
    ttl = int(ttl_ms)
    if ttl <= 0 or ttl > MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS:
        raise InvalidProviderCredentialLeaseError(
            validation_category="ttl_out_of_bounds"
        )
    return ttl


def _validate_provider(
    provider: ProviderCredentialProvider | str,
) -> ProviderCredentialProvider:
    try:
        resolved = (
            provider
            if isinstance(provider, ProviderCredentialProvider)
            else ProviderCredentialProvider(provider)
        )
    except ValueError:
        raise InvalidProviderCredentialLeaseError(
            validation_category="provider_mismatch"
        ) from None
    if resolved is not ProviderCredentialProvider.OPENAI_CODEX:
        raise InvalidProviderCredentialLeaseError(
            validation_category="provider_mismatch"
        )
    return resolved


def _lease_store_root(lease_root: Path) -> Path:
    if not lease_root.exists():
        lease_root.mkdir(parents=True)
    return validate_trusted_base_root(lease_root)


def _lease_directory(lease_root: Path, lease_id: str) -> Path:
    root = validate_trusted_base_root(lease_root)
    provider_segment = validate_safe_path_segment(OPENAI_CODEX_CREDENTIAL_STORE_ID)
    safe_lease_id = _validate_lease_id(lease_id)
    lease_dir = root / provider_segment / safe_lease_id
    assert_path_chain_safe(lease_dir, containment_root=root)
    return lease_dir


def _active_lease_markers(lease_root: Path) -> tuple[Path, ...]:
    root = validate_trusted_base_root(lease_root)
    provider_dir = root / OPENAI_CODEX_CREDENTIAL_STORE_ID
    if not provider_dir.exists():
        return ()
    contained = assert_existing_path_contained(provider_dir, containment_root=root)
    markers: list[Path] = []
    for child in contained.iterdir():
        if not child.is_dir():
            continue
        marker = child / LEASE_MARKER_NAME
        if marker.exists():
            assert_existing_path_contained(marker, containment_root=root)
            markers.append(marker)
    return tuple(markers)


def _write_marker(lease_dir: Path, lease_ref: ProviderCredentialDeliveryLease) -> None:
    marker = {
        "schema_version": PROVIDER_CREDENTIAL_SCHEMA_VERSION,
        "credential_store_id": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "provider": ProviderCredentialProvider.OPENAI_CODEX.value,
        "lease_id": lease_ref.lease_id,
        "runtime_id": lease_ref.runtime_id,
        "correlation_id": lease_ref.correlation_id,
        "created_at_utc": _format_utc(lease_ref.created_at_utc),
        "expires_at_utc": _format_utc(lease_ref.expires_at_utc),
        "automatic_refresh": False,
        "refresh_on_lease_acquisition": False,
        "refresh_writeback": False,
    }
    marker_path = lease_dir / LEASE_MARKER_NAME
    marker_path.write_text(
        json.dumps(marker, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _load_marker(
    lease_dir: Path, lease_ref: ProviderCredentialDeliveryLease
) -> dict[str, Any]:
    marker_path = lease_dir / LEASE_MARKER_NAME
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ProviderCredentialLeaseCleanupError(
            validation_category="marker_unreadable",
            detail=exc.__class__.__name__,
        ) from None
    if not isinstance(marker, dict):
        raise ProviderCredentialLeaseCleanupError(
            validation_category="marker_not_object"
        )
    expected = {
        "credential_store_id": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "provider": ProviderCredentialProvider.OPENAI_CODEX.value,
        "lease_id": lease_ref.lease_id,
        "runtime_id": lease_ref.runtime_id,
        "correlation_id": lease_ref.correlation_id,
    }
    for key, value in expected.items():
        if marker.get(key) != value:
            raise ProviderCredentialLeaseCleanupError(
                validation_category=f"{key}_mismatch"
            )
    return marker


def create_openai_codex_credential_lease(
    *,
    trusted_store_root: Path,
    trusted_lease_root: Path,
    runtime_id: str,
    correlation_id: str,
    provider: ProviderCredentialProvider
    | str = ProviderCredentialProvider.OPENAI_CODEX,
    lease_id: str | None = None,
    ttl_ms: int = MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    now: datetime | None = None,
    protection_backend: StoreProtectionBackend | None = None,
) -> ProviderCredentialProjection:
    """Create a temporary HERMES_HOME projection for one trusted runtime."""

    _validate_provider(provider)
    ttl = _validate_ttl_ms(ttl_ms)
    root = _lease_store_root(trusted_lease_root)
    if len(_active_lease_markers(root)) >= MAX_ACTIVE_PROVIDER_CREDENTIAL_LEASES:
        raise InvalidProviderCredentialLeaseError(
            validation_category="active_lease_limit"
        )
    credential = load_openai_codex_oauth_credential(
        trusted_store_root,
        protection_backend=protection_backend,
        now=now,
    )
    created_at = (now or _utc_now()).astimezone(timezone.utc)
    expires_at = created_at + timedelta(milliseconds=ttl)
    minimum_valid_until = expires_at + timedelta(
        milliseconds=MIN_PROVIDER_CREDENTIAL_REMAINING_LIFETIME_MS
    )
    if credential.expires_at_utc <= created_at:
        raise InvalidProviderCredentialLeaseError(
            validation_category="credential_expired"
        )
    if credential.expires_at_utc < minimum_valid_until:
        raise InvalidProviderCredentialLeaseError(
            validation_category="credential_near_expiry"
        )
    chosen_lease_id = _validate_lease_id(lease_id or _new_lease_id())
    lease_dir = _lease_directory(root, chosen_lease_id)
    if lease_dir.exists():
        raise InvalidProviderCredentialLeaseError(
            validation_category="lease_already_exists"
        )
    projected_home = lease_dir / "hermes-home"
    assert_path_chain_safe(projected_home, containment_root=root)
    lease_ref = ProviderCredentialDeliveryLease(
        lease_id=chosen_lease_id,
        runtime_id=runtime_id,
        correlation_id=correlation_id,
        created_at_utc=created_at,
        expires_at_utc=expires_at,
    )
    projected_home.mkdir(parents=True)
    try:
        promote_openai_codex_oauth_credential(
            projected_home,
            credential,
            protection_backend=protection_backend,
            now=now,
        )
        _write_marker(lease_dir, lease_ref)
    except Exception:
        if lease_dir.exists():
            _remove_tree(lease_dir, root)
        raise
    return ProviderCredentialProjection(
        lease_ref=lease_ref,
        projected_hermes_home=projected_home,
        auth_file_path=projected_home / "auth.json",
        environment_items=(("HERMES_HOME", str(projected_home)),),
    )


def assert_openai_codex_credential_lease_current(
    lease_ref: ProviderCredentialDeliveryLease,
    *,
    now: datetime | None = None,
) -> ProviderCredentialDeliveryLease:
    """Return the pathless lease ref if it is still within its TTL."""

    observed = (now or _utc_now()).astimezone(timezone.utc)
    if observed >= lease_ref.expires_at_utc:
        raise InvalidProviderCredentialLeaseError(validation_category="lease_expired")
    return lease_ref


def release_openai_codex_credential_lease(
    *,
    trusted_lease_root: Path,
    lease_ref: ProviderCredentialDeliveryLease,
    runtime_id: str,
    correlation_id: str,
    provider: ProviderCredentialProvider
    | str = ProviderCredentialProvider.OPENAI_CODEX,
) -> ProviderCredentialLeaseCleanup:
    """Release one marked credential projection by local deletion."""

    _validate_provider(provider)
    if runtime_id != lease_ref.runtime_id:
        raise ProviderCredentialLeaseCleanupError(
            validation_category="runtime_id_mismatch"
        )
    if correlation_id != lease_ref.correlation_id:
        raise ProviderCredentialLeaseCleanupError(
            validation_category="correlation_id_mismatch"
        )
    root = validate_trusted_base_root(trusted_lease_root)
    lease_dir = _lease_directory(root, lease_ref.lease_id)
    if not lease_dir.exists():
        return ProviderCredentialLeaseCleanup(
            lease_id=lease_ref.lease_id,
            status="not_found",
            removed_item_count=0,
            residue_item_count=0,
        )
    contained_lease_dir = assert_existing_path_contained(
        lease_dir, containment_root=root
    )
    _load_marker(contained_lease_dir, lease_ref)
    removed_count = _remove_tree(contained_lease_dir, root)
    residue_count = _remove_empty_provider_dir(root)
    return ProviderCredentialLeaseCleanup(
        lease_id=lease_ref.lease_id,
        status="released",
        removed_item_count=removed_count,
        residue_item_count=residue_count,
    )


def _remove_empty_provider_dir(lease_root: Path) -> int:
    provider_dir = lease_root / OPENAI_CODEX_CREDENTIAL_STORE_ID
    if not provider_dir.exists():
        return 0
    if any(provider_dir.iterdir()):
        return sum(1 for _entry in provider_dir.iterdir())
    provider_dir.rmdir()
    return 0


def _remove_tree(path: Path, containment_root: Path) -> int:
    root = validate_trusted_base_root(containment_root)
    target = assert_existing_path_contained(path, containment_root=root)
    if target == root:
        raise ProviderCredentialLeaseCleanupError(
            validation_category="refuse_root_delete"
        )
    paths: list[Path] = []
    seen: set[Path] = set()

    def remember(candidate: Path) -> None:
        if candidate in seen:
            return
        seen.add(candidate)
        paths.append(candidate)

    for current_root, dir_names, file_names in os.walk(
        target, topdown=False, followlinks=False
    ):
        current = Path(current_root)
        for file_name in file_names:
            candidate = current / file_name
            assert_existing_path_contained(candidate, containment_root=root)
            remember(candidate)
        for dir_name in dir_names:
            candidate = current / dir_name
            assert_existing_path_contained(candidate, containment_root=root)
            remember(candidate)
        remember(current)
        if len(paths) > _MAX_REMOVED_PATHS:
            raise ProviderCredentialLeaseCleanupError(
                validation_category="lease_tree_too_large"
            )
    removed = 0
    for candidate in paths:
        try:
            if candidate.is_dir() and not candidate.is_symlink():
                candidate.rmdir()
            else:
                candidate.unlink()
            removed += 1
        except OSError as exc:
            raise ProviderCredentialLeaseCleanupError(
                validation_category="remove_failed",
                detail=exc.__class__.__name__,
            ) from None
    return removed


__all__ = [
    "LEASE_MARKER_NAME",
    "InvalidProviderCredentialLeaseError",
    "ProviderCredentialDeliveryError",
    "ProviderCredentialLeaseCleanupError",
    "ProviderCredentialProjection",
    "assert_openai_codex_credential_lease_current",
    "create_openai_codex_credential_lease",
    "release_openai_codex_credential_lease",
]
