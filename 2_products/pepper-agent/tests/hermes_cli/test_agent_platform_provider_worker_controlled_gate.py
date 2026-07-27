from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from io import BytesIO
import json
from pathlib import Path
from typing import Any

import pytest

from hermes_cli.agent_platform import provider_failure_policy as fp
from hermes_cli.agent_platform.provider_credentials.contracts import (
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionReport,
    promote_openai_codex_oauth_credential,
)
from hermes_cli.agent_platform.provider_worker import (
    BoundedProviderWorkerRequest,
    ProviderWorkerResultState,
)
from hermes_cli.agent_platform.provider_worker.protocol import (
    deserialize_worker_result,
    serialize_worker_request,
)
from hermes_cli.agent_platform.provider_worker_gate import runtime as gate_runtime
from hermes_cli.agent_platform.provider_worker_gate.runtime import (
    run_controlled_worker_request,
    run_worker_stdio,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


class FakeProtectionBackend:
    def prepare_directory(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return StoreProtectionReport("store_directory", "test", True)

    def prepare_file(self, path: Path):
        return StoreProtectionReport("auth_file", "test", True)

    def validate_directory(self, path: Path):
        if not path.is_dir():
            raise AssertionError("missing directory")
        return StoreProtectionReport("store_directory", "test", True)

    def validate_file(self, path: Path):
        if not path.is_file():
            raise AssertionError("missing file")
        return StoreProtectionReport("auth_file", "test", True)


class ClosingEventStream(list):
    def __init__(self, events: list[dict[str, Any]]):
        super().__init__(events)
        self.closed = False

    def close(self) -> None:
        self.closed = True


class RecordingResponses:
    def __init__(self, events: list[dict[str, Any]]) -> None:
        self.events = events
        self.create_calls: list[dict[str, Any]] = []
        self.last_stream: ClosingEventStream | None = None

    def create(self, **kwargs: Any) -> ClosingEventStream:
        self.create_calls.append(kwargs)
        self.last_stream = ClosingEventStream(self.events)
        return self.last_stream


class RecordingClient:
    def __init__(self, responses: RecordingResponses) -> None:
        self.responses = responses


def synthetic_access_token() -> str:
    payload = {
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + timedelta(hours=1)).timestamp()),
    }
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    body = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return "header." + body + ".signature"


def write_store(root: Path) -> None:
    promote_openai_codex_oauth_credential(
        root,
        OpenAICodexOAuthCredential(
            access_token=synthetic_access_token(),
            refresh_token="synthetic-refresh-token",
            last_refresh_utc=NOW,
            expires_at_utc=NOW + timedelta(hours=1),
        ),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )


def worker_request() -> BoundedProviderWorkerRequest:
    return BoundedProviderWorkerRequest(
        request_id="request.runtime",
        runtime_id="runtime.runtime",
        correlation_id="corr.runtime",
        requested_by="p15.7.runtime-test",
        submitted_at_utc=NOW,
        user_content="Reply with exactly: PEPPER_P15_7_OK",
    )


def success_events() -> list[dict[str, Any]]:
    return [
        {"type": "response.output_text.delta", "delta": "PEPPER_P15_7_OK"},
        {
            "type": "response.completed",
            "response": {
                "id": "resp.runtime",
                "status": "completed",
                "usage": {"input_tokens": 10, "output_tokens": 2},
            },
        },
    ]


def test_controlled_runtime_acquires_one_lease_dispatches_once_and_releases(
    tmp_path: Path,
) -> None:
    store_root = tmp_path / "source-store"
    lease_root = tmp_path / "leases"
    write_store(store_root)
    responses = RecordingResponses(success_events())

    result = run_controlled_worker_request(
        worker_request(),
        trusted_store_root=store_root,
        trusted_lease_root=lease_root,
        client_factory=lambda _credential: RecordingClient(responses),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert "max_output_tokens" not in responses.create_calls[0]
    assert responses.create_calls[0]["store"] is False
    assert responses.create_calls[0]["stream"] is True
    assert result.worker_result.state is ProviderWorkerResultState.COMPLETED
    assert result.worker_result.output_text == "PEPPER_P15_7_OK"
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert responses.last_stream is not None
    assert responses.last_stream.closed is True
    assert lease_root.exists()
    assert list(lease_root.iterdir()) == []


def test_stdio_runtime_reads_one_request_and_writes_one_result(tmp_path: Path) -> None:
    store_root = tmp_path / "source-store"
    lease_root = tmp_path / "leases"
    write_store(store_root)
    responses = RecordingResponses(success_events())
    output = BytesIO()

    result = run_worker_stdio(
        trusted_store_root=store_root,
        trusted_lease_root=lease_root,
        stdin=BytesIO(serialize_worker_request(worker_request())),
        stdout=output,
        client_factory=lambda _credential: RecordingClient(responses),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )
    restored = deserialize_worker_result(output.getvalue())

    assert result.worker_result == restored
    assert restored.state is ProviderWorkerResultState.COMPLETED
    assert restored.output_text == "PEPPER_P15_7_OK"
    assert len(responses.create_calls) == 1


def test_runtime_client_construction_failure_is_zero_dispatch_and_releases(
    tmp_path: Path,
) -> None:
    store_root = tmp_path / "source-store"
    lease_root = tmp_path / "leases"
    write_store(store_root)

    def raise_client(_credential: OpenAICodexOAuthCredential) -> RecordingClient:
        raise RuntimeError("synthetic client construction failure")

    result = run_controlled_worker_request(
        worker_request(),
        trusted_store_root=store_root,
        trusted_lease_root=lease_root,
        client_factory=raise_client,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert result.worker_result.state is ProviderWorkerResultState.FAILED
    assert result.dispatch_evidence.responses_create_call_count == 0
    assert result.diagnostics.provider_dispatches_for_attempt == 0
    assert result.diagnostics.failure_phase == "client_construction"
    assert (
        result.diagnostics.local_failure_category == "local_client_construction_failure"
    )
    assert result.diagnostics.safe_exception_class == "RuntimeError"
    assert result.diagnostics.cleanup_status == "passed"
    assert result.failure_record is not None
    assert result.failure_record.stage is fp.ProviderFailureStage.PREFLIGHT
    assert result.failure_record.provider_dispatch_count == 0
    assert "client_construction_started" in result.diagnostics.checkpoints
    assert "client_constructed" not in result.diagnostics.checkpoints
    assert "cleanup_completed" in result.diagnostics.checkpoints
    assert lease_root.exists()
    assert list(lease_root.iterdir()) == []


def test_runtime_cleanup_failure_preserves_dispatch_counters(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store_root = tmp_path / "source-store"
    lease_root = tmp_path / "leases"
    write_store(store_root)
    responses = RecordingResponses(success_events())

    def raise_cleanup(**_kwargs: Any) -> None:
        raise PermissionError("synthetic cleanup failure")

    monkeypatch.setattr(
        gate_runtime,
        "release_openai_codex_credential_lease",
        raise_cleanup,
    )

    result = run_controlled_worker_request(
        worker_request(),
        trusted_store_root=store_root,
        trusted_lease_root=lease_root,
        client_factory=lambda _credential: RecordingClient(responses),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert len(responses.create_calls) == 1
    assert result.worker_result.state is ProviderWorkerResultState.COMPLETED
    assert result.dispatch_evidence.responses_create_call_count == 1
    assert result.diagnostics.provider_dispatches_for_attempt == 1
    assert result.diagnostics.cleanup_status == "failed"
    assert (
        result.diagnostics.cleanup_failure_category
        == "local_environment_permission_failure"
    )
    assert result.diagnostics.cleanup_safe_exception_class == "PermissionError"
    assert result.failure_record is None
    assert "cleanup_completed" in result.diagnostics.checkpoints


def test_runtime_source_has_no_oauth_acquisition_retry_or_fallback_authority() -> None:
    from hermes_cli.agent_platform.provider_worker_gate import runtime

    source = Path(runtime.__file__).read_text(encoding="utf-8")
    assert "auth add" not in source
    assert "device" not in source.lower()
    assert "run_codex_stream(" not in source
    assert "run_codex_create_stream_fallback" not in source
    assert "responses.stream" not in source
    assert "max_output_tokens=" not in source
    assert "max_retries=0" in source
