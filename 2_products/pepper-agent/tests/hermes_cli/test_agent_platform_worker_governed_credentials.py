from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials.store import (
    StoreProtectionReport,
    default_openai_codex_credential_store_root,
    promote_openai_codex_oauth_credential,
)
from hermes_cli.agent_platform.worker_credentials import (
    PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION,
    PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE,
    PEPPER_GOVERNED_WORKER_BLOCKER_CODE,
    PEPPER_GOVERNED_WORKER_READY_MARKER,
    PEPPER_GOVERNED_WORKER_SOURCE,
    GovernedWorkerCredentialBinding,
    PepperGovernedWorkerCredentialError,
    pepper_governed_worker_env,
    probe_pepper_governed_worker_credentials,
    resolve_pepper_governed_worker_runtime,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)
_EXECUTOR_PROFILE = "pepper-architecture-product"
_IMPLEMENTATION_PROFILE = "test-implementation-product"
_WORK_PACKET_ID = "WP-P18-9-0-R0001-123456789abc"
_WORK_PACKET_SHA256 = "a" * 64
_TICKET_SPEC_SHA256 = "b" * 64
_PROJECTION_SHA256 = "c" * 64


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


def synthetic_access_token(*, exp_delta: timedelta = timedelta(hours=1)) -> str:
    payload = {
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + exp_delta).timestamp()),
    }
    body = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return "header." + body + ".signature"


def write_governed_store(root: Path, *, access_token: str) -> None:
    promote_openai_codex_oauth_credential(
        root,
        OpenAICodexOAuthCredential(
            access_token=access_token,
            refresh_token="governed-refresh-token",
            last_refresh_utc=NOW,
            expires_at_utc=NOW + timedelta(hours=1),
        ),
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )


def _write_profile_config(profile_home: Path, *, provider: str = "openai-codex", model: str = "gpt-5.5", api_mode: str = "codex_responses") -> None:
    profile_home.mkdir(parents=True, exist_ok=True)
    (profile_home / "config.yaml").write_text(
        "\n".join([
            "model:",
            f"  provider: {provider}",
            f"  default: {model}",
            f"  api_mode: {api_mode}",
        ]) + "\n",
        encoding="utf-8",
    )


def _binding(*, profile_name: str = _EXECUTOR_PROFILE, task_id: str = "t_f762b8e0") -> GovernedWorkerCredentialBinding:
    return GovernedWorkerCredentialBinding(
        project_id="PEPPER",
        ticket_id="P18.9.0",
        work_packet_id=_WORK_PACKET_ID,
        work_packet_SHA256=_WORK_PACKET_SHA256,
        ticket_spec_SHA256=_TICKET_SPEC_SHA256,
        kanban_task_id=task_id,
        executor_profile=profile_name,
        provider="openai-codex",
        model="gpt-5.5",
        api_mode="codex_responses",
        credential_profile_id="openai-codex.primary",
        provider_runtime_profile_id="provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
        worker_profile_id="worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
        credential_policy_revision=PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION,
        runtime_id=f"runtime.test.{task_id}",
        correlation_id=f"correlation.test.{task_id}",
        lease_id=f"lease.test.{task_id}",
        base_url=OPENAI_CODEX_PROVIDER_ENDPOINT,
        profile_assignment_policy_id="pepper-execution-profiles-v1",
        profile_assignment_policy_revision="1",
        projection_SHA256=_PROJECTION_SHA256,
    )


def _write_authority_records(root_home: Path, *, profile_name: str = _EXECUTOR_PROFILE) -> dict[str, Path]:
    authority_dir = root_home / "agent-platform" / "worker-authority-test"
    authority_dir.mkdir(parents=True, exist_ok=True)
    generation = {
        "ticket_id": "P18.9.0",
        "work_packet_id": _WORK_PACKET_ID,
        "work_packet_SHA256": _WORK_PACKET_SHA256,
        "ticket_spec_SHA256": _TICKET_SPEC_SHA256,
    }
    approval = {"ticket_id": "P18.9.0", "status": "approved"}
    projection = {
        **generation,
        "projection_SHA256": _PROJECTION_SHA256,
        "assignee_profile": profile_name,
    }
    paths = {
        "generation": authority_dir / "generation.json",
        "approval": authority_dir / "approval.json",
        "projection": authority_dir / "projection.json",
    }
    paths["generation"].write_text(json.dumps(generation), encoding="utf-8")
    paths["approval"].write_text(json.dumps(approval), encoding="utf-8")
    paths["projection"].write_text(json.dumps(projection), encoding="utf-8")
    return paths


def _worker_env(
    root_home: Path,
    task_id: str = "t_f762b8e0",
    *,
    profile_name: str = _EXECUTOR_PROFILE,
    provider: str = "openai-codex",
    model: str = "gpt-5.5",
    api_mode: str = "codex_responses",
) -> dict[str, str]:
    profile_home = root_home / "profiles" / profile_name
    profile_home.mkdir(parents=True, exist_ok=True)
    _write_profile_config(profile_home, provider=provider, model=model, api_mode=api_mode)
    env = {
        "HERMES_HOME": str(profile_home),
        "HERMES_PROFILE": profile_name,
        "HERMES_KANBAN_TASK": task_id,
    }
    env.update(pepper_governed_worker_env(binding=_binding(profile_name=profile_name, task_id=task_id)))
    authority_paths = _write_authority_records(root_home, profile_name=profile_name)
    env.update({
        "HERMES_AGENT_PLATFORM_GENERATION_RECORD_PATH": str(authority_paths["generation"]),
        "HERMES_AGENT_PLATFORM_APPROVAL_DECISION_RECORD_PATH": str(authority_paths["approval"]),
        "HERMES_AGENT_PLATFORM_KANBAN_PROJECTION_RECORD_PATH": str(authority_paths["projection"]),
    })
    return env


def test_worker_resolver_uses_governed_root_not_profile_auth_json(
    tmp_path: Path,
) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    profile_home = Path(env["HERMES_HOME"])
    profile_home.mkdir(parents=True, exist_ok=True)
    profile_legacy_token = synthetic_access_token(exp_delta=timedelta(hours=2))
    (profile_home / "auth.json").write_text(
        json.dumps(
            {
                "version": 1,
                "active_provider": "openai-codex",
                "providers": {
                    "openai-codex": {
                        "tokens": {
                            "access_token": profile_legacy_token,
                            "refresh_token": "profile-refresh-token",
                        }
                    }
                },
                "credential_pool": {
                    "openai-codex": [
                        {
                            "access_token": profile_legacy_token,
                            "refresh_token": "pool-refresh-token",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    governed_token = synthetic_access_token()
    write_governed_store(
        default_openai_codex_credential_store_root(root_home),
        access_token=governed_token,
    )

    probe = probe_pepper_governed_worker_credentials(
        env=env,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )
    runtime = resolve_pepper_governed_worker_runtime(
        env=env,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert "api_key" not in probe
    assert probe["credential_resolution_source"] == "canonical_governed_home"
    assert runtime["api_key"] == governed_token
    assert runtime["api_key"] != profile_legacy_token
    assert runtime["base_url"] == OPENAI_CODEX_PROVIDER_ENDPOINT
    assert runtime["source"] == PEPPER_GOVERNED_WORKER_SOURCE
    assert runtime["credential_profile_id"] == "openai-codex.primary"
    assert runtime["executor_profile"] == _EXECUTOR_PROFILE
    assert runtime["work_packet_id"] == _WORK_PACKET_ID
    assert runtime["credential_policy_revision"] == PEPPER_GOVERNED_CREDENTIAL_POLICY_REVISION
    assert runtime["legacy_auth_json_used"] is False
    assert runtime["API_key_fallback_used"] is False
    assert runtime["credential_pool_fallback_used"] is False
    assert runtime["credential_refresh_calls_per_request_maximum"] == 0
    assert runtime["human_smoke_marker"] == PEPPER_GOVERNED_WORKER_READY_MARKER


def test_worker_resolver_accepts_different_selected_executor_profile(tmp_path: Path) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home, profile_name=_IMPLEMENTATION_PROFILE)
    governed_token = synthetic_access_token()
    write_governed_store(
        default_openai_codex_credential_store_root(root_home),
        access_token=governed_token,
    )

    runtime = resolve_pepper_governed_worker_runtime(
        env=env,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert runtime["executor_profile"] == _IMPLEMENTATION_PROFILE
    assert runtime["api_key"] == governed_token
    assert runtime["credential_profile_id"] == "openai-codex.primary"


def test_worker_resolver_fails_when_selected_profile_path_missing(tmp_path: Path) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    profile_home = Path(env["HERMES_HOME"])
    for child in profile_home.iterdir():
        child.unlink()
    profile_home.rmdir()

    with pytest.raises(PepperGovernedWorkerCredentialError) as exc_info:
        probe_pepper_governed_worker_credentials(
            env=env,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    assert exc_info.value.validation_category == "selected_profile_path_unavailable"


@pytest.mark.parametrize(
    ("provider", "model", "api_mode", "expected_category"),
    [
        ("anthropic", "gpt-5.5", "codex_responses", "provider_runtime_profile_unavailable"),
        ("openai-codex", "gpt-5.4", "codex_responses", "provider_runtime_profile_unavailable"),
        ("openai-codex", "gpt-5.5", "chat_completions", "provider_runtime_profile_unavailable"),
    ],
)
def test_worker_resolver_fails_when_profile_runtime_drifts(
    tmp_path: Path,
    provider: str,
    model: str,
    api_mode: str,
    expected_category: str,
) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home, provider=provider, model=model, api_mode=api_mode)

    with pytest.raises(PepperGovernedWorkerCredentialError) as exc_info:
        probe_pepper_governed_worker_credentials(
            env=env,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    assert exc_info.value.validation_category == expected_category


def test_worker_resolver_fails_when_credential_profile_drifts(tmp_path: Path) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    env["HERMES_AGENT_PLATFORM_CREDENTIAL_STORE_ID"] = "openai-codex.other"

    with pytest.raises(PepperGovernedWorkerCredentialError) as exc_info:
        probe_pepper_governed_worker_credentials(
            env=env,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    assert exc_info.value.validation_category == "hermes_agent_platform_credential_store_id_mismatch"


def test_worker_resolver_rejects_stale_workpacket_binding(tmp_path: Path) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    env["HERMES_AGENT_PLATFORM_WORKPACKET_SHA256"] = "d" * 64

    with pytest.raises(PepperGovernedWorkerCredentialError) as exc_info:
        resolve_pepper_governed_worker_runtime(
            env=env,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    assert exc_info.value.validation_category == "generation_record_work_packet_SHA256_mismatch"


def test_legacy_auth_and_api_key_do_not_fallback_when_governed_store_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    profile_home = Path(env["HERMES_HOME"])
    (profile_home / "auth.json").write_text(
        json.dumps({"access_token": synthetic_access_token()}),
        encoding="utf-8",
    )
    env["OPENAI_API_KEY"] = "SHOULD_NOT_BE_USED"
    monkeypatch.setenv("OPENAI_API_KEY", "SHOULD_NOT_BE_USED")

    with pytest.raises(PepperGovernedWorkerCredentialError) as exc_info:
        resolve_pepper_governed_worker_runtime(
            env=env,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    assert exc_info.value.validation_category == "governed_credential_absent"


def test_codex_auth_resolver_bypasses_generic_store_for_governed_worker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    from hermes_cli import auth
    from hermes_cli.agent_platform import worker_credentials

    monkeypatch.setattr(
        auth,
        "_read_codex_tokens",
        lambda *_args, **_kwargs: pytest.fail("generic auth.json must not be read"),
    )
    monkeypatch.setattr(
        auth,
        "_pool_codex_access_token",
        lambda *_args, **_kwargs: pytest.fail("credential pool must not be read"),
    )
    monkeypatch.setattr(
        worker_credentials,
        "resolve_pepper_governed_worker_runtime",
        lambda: {
            "provider": "openai-codex",
            "base_url": OPENAI_CODEX_PROVIDER_ENDPOINT,
            "api_key": "governed-access-token",
            "source": PEPPER_GOVERNED_WORKER_SOURCE,
            "last_refresh": None,
            "auth_mode": "chatgpt",
        },
    )

    resolved = auth.resolve_codex_runtime_credentials(force_refresh=True)

    assert resolved["api_key"] == "governed-access-token"
    assert resolved["source"] == PEPPER_GOVERNED_WORKER_SOURCE


def test_codex_auth_resolver_fails_bounded_without_generic_setup_guidance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root_home = tmp_path / "hermes-root"
    env = _worker_env(root_home)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    from hermes_cli import auth
    from hermes_cli.agent_platform import worker_credentials

    def fail_governed_worker():
        raise PepperGovernedWorkerCredentialError("governed_credential_absent")

    monkeypatch.setattr(
        worker_credentials,
        "resolve_pepper_governed_worker_runtime",
        fail_governed_worker,
    )

    with pytest.raises(auth.AuthError) as exc_info:
        auth.resolve_codex_runtime_credentials()

    assert exc_info.value.code == PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE
    assert exc_info.value.provider == "openai-codex"
    assert exc_info.value.relogin_required is False
    assert PEPPER_GOVERNED_WORKER_BLOCKER_CODE in str(exc_info.value)
    assert "hermes auth" not in str(exc_info.value).lower()
    assert "hermes model" not in str(exc_info.value).lower()


def test_codex_auth_resolver_fails_closed_for_invalid_worker_binding(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile_home = tmp_path / "hermes-root" / "profiles" / _EXECUTOR_PROFILE
    profile_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HERMES_HOME", str(profile_home))
    monkeypatch.setenv("HERMES_PROFILE", _EXECUTOR_PROFILE)
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_GOVERNED_WORKER", "wrong-worker")

    from hermes_cli import auth

    monkeypatch.setattr(
        auth,
        "_read_codex_tokens",
        lambda *_args, **_kwargs: pytest.fail("generic auth.json must not be read"),
    )

    with pytest.raises(auth.AuthError) as exc_info:
        auth.resolve_codex_runtime_credentials()

    assert exc_info.value.code == PEPPER_GOVERNED_WORKER_AUTH_ERROR_CODE
    assert exc_info.value.provider == "openai-codex"
    assert exc_info.value.relogin_required is False
    assert PEPPER_GOVERNED_WORKER_BLOCKER_CODE in str(exc_info.value)
    assert "worker_binding_invalid" in str(exc_info.value)
    assert "hermes auth" not in str(exc_info.value).lower()
    assert "hermes model" not in str(exc_info.value).lower()
