"""Stdin/stdout runtime for one controlled provider-worker request."""

from __future__ import annotations

import os
from pathlib import Path
import sys
from datetime import datetime, timezone
from typing import Any, BinaryIO, Callable

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials.delivery import (
    ProviderCredentialProjection,
    assert_openai_codex_credential_lease_current,
    create_openai_codex_credential_lease,
    release_openai_codex_credential_lease,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionBackend,
    default_openai_codex_credential_store_root,
    load_openai_codex_oauth_credential,
    read_openai_codex_credential_status,
)
from hermes_cli.agent_platform.provider_runtime.contracts import (
    ProviderRuntimeResolutionRequest,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    BoundedProviderWorkerRequest,
    ProviderWorkerResolutionRequest,
)
from hermes_cli.agent_platform.provider_worker.protocol import (
    deserialize_worker_request,
    serialize_worker_result,
)
from hermes_cli.agent_platform.provider_worker.resolution import (
    resolve_provider_worker_profile,
)
from hermes_cli.agent_platform.provider_worker_gate.contracts import (
    GOVERNED_CREDENTIAL_LEASE_TTL_MS,
    GateCheckpoint,
    GateLocalFailureCategory,
    OPENAI_CODEX_ENDPOINT,
    ProviderWorkerGateResult,
)
from hermes_cli.agent_platform.provider_worker_gate.single_dispatch import (
    build_local_gate_failure_result,
    build_provider_worker_gate_request,
    run_openai_codex_single_dispatch,
    with_gate_cleanup_status,
)


ClientFactory = Callable[[OpenAICodexOAuthCredential], Any]


class ProviderWorkerGateRuntimeError(RuntimeError):
    """Bounded runtime error that omits paths, environment values and secrets."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"code={code}")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime values must be timezone-aware")
    return value.astimezone(timezone.utc)


def _append_checkpoint(
    checkpoints: list[GateCheckpoint],
    checkpoint: GateCheckpoint,
) -> None:
    if checkpoint not in checkpoints:
        checkpoints.append(checkpoint)


def _runtime_local_failure_category(exc: Exception) -> GateLocalFailureCategory:
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return "local_environment_import_failure"
    if isinstance(exc, FileNotFoundError):
        return "local_environment_missing_file"
    if isinstance(exc, PermissionError):
        return "local_environment_permission_failure"
    if isinstance(exc, ValueError):
        return "local_request_validation_failure"
    return "local_internal_unknown"


def create_openai_codex_client(credential: OpenAICodexOAuthCredential) -> Any:
    """Create the governed OpenAI client with SDK retries disabled."""

    from openai import OpenAI

    return OpenAI(
        api_key=credential.access_token.get_secret_value(),
        base_url=OPENAI_CODEX_ENDPOINT,
        max_retries=0,
    )


def run_controlled_worker_request(
    worker_request: BoundedProviderWorkerRequest,
    *,
    trusted_store_root: Path,
    trusted_lease_root: Path,
    client_factory: ClientFactory | None = None,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> ProviderWorkerGateResult:
    """Acquire one lease, validate readiness, dispatch once and release the lease."""

    evaluated_at = _utc(now or _utc_now())
    gate_request = build_provider_worker_gate_request(
        worker_request,
        requested_at_utc=evaluated_at,
    )
    checkpoints: list[GateCheckpoint] = []
    _append_checkpoint(checkpoints, "request_validated")
    projection: ProviderCredentialProjection | None = None
    result: ProviderWorkerGateResult | None = None
    cleanup_exception: Exception | None = None
    try:
        projection = create_openai_codex_credential_lease(
            trusted_store_root=trusted_store_root,
            trusted_lease_root=trusted_lease_root,
            runtime_id=worker_request.runtime_id,
            correlation_id=worker_request.correlation_id,
            ttl_ms=GOVERNED_CREDENTIAL_LEASE_TTL_MS,
            now=now,
            protection_backend=protection_backend,
        )
        assert_openai_codex_credential_lease_current(projection.lease_ref, now=now)
        credential_status = read_openai_codex_credential_status(
            trusted_store_root,
            protection_backend=protection_backend,
            now=now,
        )
        evaluated_at = projection.lease_ref.created_at_utc
        gate_request = build_provider_worker_gate_request(
            worker_request,
            requested_at_utc=evaluated_at,
            usage_record_id=gate_request.usage_record_id,
        )
        provider_resolution_request = ProviderRuntimeResolutionRequest(
            runtime_id=worker_request.runtime_id,
            correlation_id=worker_request.correlation_id,
            requested_by=worker_request.requested_by,
            evaluated_at_utc=evaluated_at,
            credential_status=credential_status,
            credential_lease_ref=projection.lease_ref,
        )
        resolve_provider_worker_profile(
            ProviderWorkerResolutionRequest(
                worker_profile_id=worker_request.profile_id,
                provider_resolution_request=provider_resolution_request,
                evaluated_at_utc=evaluated_at,
            )
        )
        credential = load_openai_codex_oauth_credential(
            projection.projected_hermes_home,
            protection_backend=protection_backend,
            now=now,
        )
        _append_checkpoint(checkpoints, "client_construction_started")
        try:
            client = (client_factory or create_openai_codex_client)(credential)
        except Exception as exc:
            result = build_local_gate_failure_result(
                gate_request=gate_request,
                started_at_utc=evaluated_at,
                completed_at_utc=_utc(now or _utc_now()),
                checkpoints=checkpoints,
                failure_phase="client_construction",
                local_failure_category="local_client_construction_failure",
                exception=exc,
                temporary_credential_lease_exists=projection is not None,
                temporary_projected_hermes_home_present=projection is not None,
            )
        else:
            _append_checkpoint(checkpoints, "client_constructed")
            result = run_openai_codex_single_dispatch(
                gate_request,
                client=client,
                now=evaluated_at,
                initial_checkpoints=tuple(checkpoints),
            )
    except Exception as exc:
        if result is None:
            result = build_local_gate_failure_result(
                gate_request=gate_request,
                started_at_utc=evaluated_at,
                completed_at_utc=_utc(now or _utc_now()),
                checkpoints=checkpoints,
                failure_phase="preflight",
                local_failure_category=_runtime_local_failure_category(exc),
                exception=exc,
                temporary_credential_lease_exists=projection is not None,
                temporary_projected_hermes_home_present=projection is not None,
            )
    finally:
        if projection is not None:
            try:
                release_openai_codex_credential_lease(
                    trusted_lease_root=trusted_lease_root,
                    lease_ref=projection.lease_ref,
                    runtime_id=worker_request.runtime_id,
                    correlation_id=worker_request.correlation_id,
                )
            except Exception as exc:
                cleanup_exception = exc
    if result is None:
        raise ProviderWorkerGateRuntimeError("result_unavailable")
    if projection is not None:
        return with_gate_cleanup_status(
            result,
            cleanup_status="failed" if cleanup_exception is not None else "passed",
            cleanup_exception=cleanup_exception,
        )
    return result


def run_controlled_worker_payload(
    payload: bytes,
    *,
    trusted_store_root: Path,
    trusted_lease_root: Path,
    client_factory: ClientFactory | None = None,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> ProviderWorkerGateResult:
    """Deserialize one request frame and run it through the controlled gate."""

    return run_controlled_worker_request(
        deserialize_worker_request(payload),
        trusted_store_root=trusted_store_root,
        trusted_lease_root=trusted_lease_root,
        client_factory=client_factory,
        protection_backend=protection_backend,
        now=now,
    )


def run_worker_stdio(
    *,
    trusted_store_root: Path,
    trusted_lease_root: Path,
    stdin: BinaryIO | None = None,
    stdout: BinaryIO | None = None,
    client_factory: ClientFactory | None = None,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> ProviderWorkerGateResult:
    """Read one worker request from stdin and write one worker result to stdout."""

    input_stream = stdin if stdin is not None else sys.stdin.buffer
    output_stream = stdout if stdout is not None else sys.stdout.buffer
    result = run_controlled_worker_payload(
        input_stream.read(),
        trusted_store_root=trusted_store_root,
        trusted_lease_root=trusted_lease_root,
        client_factory=client_factory,
        protection_backend=protection_backend,
        now=now,
    )
    output_stream.write(serialize_worker_result(result.worker_result))
    output_stream.flush()
    return result


def _default_lease_root() -> Path:
    configured = os.environ.get("PEPPER_PROVIDER_WORKER_GATE_LEASE_ROOT", "").strip()
    if configured:
        return Path(configured)
    hermes_home = os.environ.get("HERMES_HOME", "").strip()
    if not hermes_home:
        raise ProviderWorkerGateRuntimeError("HERMES_HOME_required")
    return Path(hermes_home) / "agent-platform" / "provider-worker-gate-leases"


def main() -> int:
    store_root = default_openai_codex_credential_store_root()
    lease_root = _default_lease_root()
    run_worker_stdio(trusted_store_root=store_root, trusted_lease_root=lease_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "ProviderWorkerGateRuntimeError",
    "create_openai_codex_client",
    "run_controlled_worker_payload",
    "run_controlled_worker_request",
    "run_worker_stdio",
]
