from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform import provider_worker as pw
from hermes_cli.agent_platform import provider_worker_gate as gate


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_worker_request() -> pw.BoundedProviderWorkerRequest:
    return pw.BoundedProviderWorkerRequest(
        request_id="request.gate.contracts",
        runtime_id="runtime.gate.contracts",
        correlation_id="corr.gate.contracts",
        requested_by="p15.7.contract-test",
        submitted_at_utc=NOW,
        user_content="Reply with exactly: PEPPER_P15_7_OK",
    )


def test_gate_policy_pins_single_worker_single_dispatch_identity() -> None:
    policy = gate.ProviderWorkerGatePolicy()

    assert policy.gate_id == "gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1"
    assert policy.provider == "openai-codex"
    assert policy.authentication == "chatgpt_oauth"
    assert policy.endpoint == "https://chatgpt.com/backend-api/codex"
    assert policy.model_id == "gpt-5.5"
    assert policy.transport == "codex_responses"
    assert (
        policy.provider_runtime_profile_id
        == "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"
    )
    assert (
        policy.worker_profile_id
        == "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert (
        policy.accounting_policy_id
        == "accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert (
        policy.failure_policy_id
        == "failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1"
    )
    assert policy.credential_store_id == "openai-codex.primary"
    assert policy.maximum_concurrent_workers == 1
    assert policy.maximum_concurrent_requests_per_worker == 1
    assert policy.maximum_requests_per_worker_lifetime == 1
    assert policy.maximum_provider_dispatches_per_request == 1
    assert policy.responses_create_call_maximum == 1
    assert policy.SDK_max_retries == 0
    assert policy.worker_retry_attempts == 0
    assert policy.worker_fallback_attempts == 0
    assert policy.credential_refresh_calls_per_request == 0
    assert policy.model_list_calls_per_request == 0
    assert policy.wire_max_output_tokens_allowed is False
    assert policy.credential_lease_ttl_ms == 300_000
    assert policy.minimum_remaining_credential_lifetime_ms == 300_000
    assert policy.local_expected_output == "PEPPER_P15_7_OK"
    assert policy.local_exact_output_validation_required is True
    assert policy.automatic_retry_allowed is False
    assert policy.automatic_fallback_allowed is False
    assert policy.credential_rotation_allowed is False
    assert policy.tools_allowed is False
    assert policy.MCP_allowed is False


def test_gate_request_rejects_caller_overrides_and_mismatched_profiles() -> None:
    request = gate.build_provider_worker_gate_request(
        make_worker_request(),
        requested_at_utc=NOW,
    )
    assert request.system_instruction == gate.OPENAI_CODEX_P15_7_SYSTEM_INSTRUCTION
    assert request.stream_requested is True
    assert request.usage_record_id.startswith("usage-")

    payload = request.model_dump()
    payload["model"] = "forbidden"
    with pytest.raises(ValidationError):
        gate.ProviderWorkerGateRequest(**payload)

    worker_payload = request.worker_request.model_dump()
    worker_payload["profile_id"] = "worker.other"
    payload = request.model_dump()
    payload["worker_request"] = worker_payload
    with pytest.raises(ValidationError):
        gate.ProviderWorkerGateRequest(**payload)


def test_gate_contracts_are_immutable_and_source_has_no_retry_or_fallback_calls() -> (
    None
):
    policy = gate.ProviderWorkerGatePolicy()
    with pytest.raises(ValidationError):
        gate.ProviderWorkerGatePolicy(model_id="gpt-4.1")
    with pytest.raises(ValidationError):
        policy.SDK_max_retries = 1

    package_root = Path(gate.__file__).resolve().parent
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(package_root.glob("*.py"))
    )
    assert "run_codex_stream(" not in source
    assert "run_codex_create_stream_fallback" not in source
    assert "responses.stream" not in source
    assert "time.sleep" not in source
    assert "asyncio.sleep" not in source
    assert "max_retries=2" not in source


def test_gate_diagnostics_reject_inconsistent_zero_dispatch_stream_phase() -> None:
    with pytest.raises(ValidationError):
        gate.ProviderWorkerGateDiagnostics(
            provider_dispatches_for_attempt=0,
            failure_phase="stream",
        )

    diagnostics = gate.ProviderWorkerGateDiagnostics(
        checkpoints=("request_validated", "dispatch_started"),
        provider_dispatches_for_attempt=1,
        failure_phase="dispatch",
        local_failure_category="provider_failure_delegated_to_p15_6",
        safe_exception_class="SyntheticError",
        safe_exception_module="tests.synthetic",
    )
    assert diagnostics.raw_exception_retained is False
    assert diagnostics.traceback_retained is False
    assert diagnostics.provider_text_retained is False
    assert diagnostics.provider_headers_retained is False
    assert diagnostics.provider_response_id_retained is False
