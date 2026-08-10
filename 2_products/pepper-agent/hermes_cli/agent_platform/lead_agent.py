"""Pepper Lead Agent chat contract for controlled default mode.

This module contains only the product-local chat binding metadata used by the
dashboard PTY child and the TUI gateway. It does not create a second session,
approval, execution, worker, provider, or Git authority path.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import Any

from hermes_cli.agent_platform.provider_credentials.contracts import (
    MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS,
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    ProviderCredentialDeliveryLease,
)
from hermes_cli.agent_platform.provider_worker.contracts import (
    OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
    OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
    ProviderWorkerResolutionRequest,
)


PEPPER_LEAD_AGENT_ENV = "HERMES_AGENT_PLATFORM_CHAT_MODE"
PEPPER_LEAD_AGENT_MODE = "pepper-lead-agent"
PEPPER_LEAD_AGENT_PLATFORM = "pepper-dashboard"
PEPPER_LEAD_AGENT_PROVIDER = "openai-codex"
PEPPER_LEAD_AGENT_MODEL = "gpt-5.5"
PEPPER_LEAD_AGENT_API_MODE = "codex_responses"
PEPPER_LEAD_AGENT_TOOLSETS: list[str] = ["pepper_workflow"]
PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE = OPENAI_CODEX_CREDENTIAL_STORE_ID
PEPPER_LEAD_AGENT_SOURCE = "pepper-governed-openai-codex-oauth"
PEPPER_LEAD_AGENT_PROVISION_COMMAND = (
    "hermes agent-platform auth add openai-codex.primary"
)
_PEPPER_RUNTIME_ID = "runtime.pepper-lead-agent"
_PEPPER_CORRELATION_ID = "correlation.pepper-lead-agent"


class PepperLeadAgentProviderUnavailable(RuntimeError):
    """Secret-free Pepper governed-provider readiness failure."""

    error_code = "pepper_governed_provider_unavailable"

    def __init__(self, validation_category: str) -> None:
        self.validation_category = _safe_text(validation_category)
        super().__init__(
            "Pepper Lead Agent provider unavailable: governed credential "
            f"profile {PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE} required "
            f"(validation_category={self.validation_category})."
        )


def _safe_text(value: object) -> str:
    return "".join(character for character in str(value) if 32 <= ord(character) < 127)[
        :120
    ]


def pepper_lead_agent_enabled(env: Mapping[str, str] | None = None) -> bool:
    """Return True when the current TUI process is the Pepper chat child."""

    raw = str((env or os.environ).get(PEPPER_LEAD_AGENT_ENV, "") or "")
    normalized = raw.strip().lower().replace("_", "-")
    return normalized in {PEPPER_LEAD_AGENT_MODE, "pepper-lead", "pepper"}


def pepper_lead_agent_env() -> dict[str, str]:
    """Environment overlay for the dashboard-spawned Pepper chat child."""

    return {PEPPER_LEAD_AGENT_ENV: PEPPER_LEAD_AGENT_MODE}


def pepper_lead_agent_branding() -> dict[str, str]:
    """Skin-branding override for the Pepper chat TUI."""

    return {
        "agent_name": "Pepper Lead Agent",
        "welcome": "Pepper controlled default mode is active. Ask about approvals, executions, workflow state, or the next governed handoff.",
        "response_label": " Pepper ",
        "help_header": "Pepper controlled commands",
    }


def pepper_lead_agent_setup_sections() -> list[dict[str, Any]]:
    """Setup panel rows for Pepper's governed provider binding."""

    return [
        {
            "text": (
                "Pepper Lead Agent provider unavailable: governed credential "
                "profile openai-codex.primary is required before this chat "
                "can start a session."
            )
        },
        {
            "title": "Actions",
            "rows": [
                [
                    PEPPER_LEAD_AGENT_PROVISION_COMMAND,
                    "provision openai-codex.primary in the governed store",
                ],
                ["Refresh /chat", "start Pepper Lead Agent after authentication"],
                ["Ctrl+C", "exit this chat process"],
            ],
        },
    ]


def pepper_lead_agent_system_prompt() -> str:
    """Stable per-session instructions for the Pepper conversational surface."""

    return "\n".join(
        [
            "You are Pepper Lead Agent, the conversational control surface for Pepper controlled default mode.",
            "Authority: Pepper governed workflow tools are the source of truth for project, ticket, approvals, executions, workflow-control, review, recovery, Git handoff, and next-action state.",
            f"Provider authority: {OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID} ({PEPPER_LEAD_AGENT_PROVIDER}/{PEPPER_LEAD_AGENT_MODEL}, {PEPPER_LEAD_AGENT_API_MODE}).",
            f"Worker handoff substrate: {OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID} plus the P15/P17 controlled execution contracts.",
            "Before answering any operational-state question, call the relevant Pepper workflow tool: get_current_project, get_current_ticket, get_workflow_control, get_pending_approvals, get_execution_status, get_review_status, or get_next_action.",
            "Do not infer the active governed project from cwd, repository name, conversation text, stale session memory, or prompt guesses. The governed project identity is tool-backed and distinct from the repository directory.",
            "Do not tell the user to inspect or copy dashboard state when a Pepper workflow tool can read the same governed state directly.",
            "If a field is genuinely unavailable, name the exact unavailable field and still report the current tool-backed next action.",
            "If there is no active governed ticket, say 'no active governed ticket' and report the tool-backed next action. If approval or execution counts are zero, say 'no pending approvals' or 'no active executions'.",
            "Do not present generic Hermes model setup, /model setup, OpenRouter setup, OpenAI API-key setup, or ~/.hermes/.env provider setup as the Pepper chat path.",
            "Do not run arbitrary shell commands, dispatch direct workers, call tools to mutate files, auto-approve approvals, retry execution, roll back execution, or stage, commit, or push Git.",
            "Preserve Ticket Factory and human approval boundaries: approvals require explicit human dashboard decisions, execution handoff stays governed, and Git remains human-only.",
        ]
    )


def resolve_pepper_lead_agent_runtime(
    *,
    protection_backend: Any = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Resolve the fixed Pepper Lead Agent runtime without generic fallbacks."""

    credential = _load_governed_openai_codex_credential(
        protection_backend=protection_backend,
        now=now,
    )

    return {
        "provider": PEPPER_LEAD_AGENT_PROVIDER,
        "model": PEPPER_LEAD_AGENT_MODEL,
        "base_url": OPENAI_CODEX_PROVIDER_ENDPOINT,
        "api_key": credential.access_token.get_secret_value(),
        "api_mode": PEPPER_LEAD_AGENT_API_MODE,
        "source": PEPPER_LEAD_AGENT_SOURCE,
        "credential_profile_id": PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE,
        "provider_runtime_profile_id": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        "worker_profile_id": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
    }


def _load_governed_openai_codex_credential(
    *,
    protection_backend: Any = None,
    now: datetime | None = None,
):
    from hermes_cli.agent_platform.provider_credentials.store import (
        default_openai_codex_credential_store_root,
        load_openai_codex_oauth_credential,
        read_openai_codex_credential_status,
    )
    from hermes_cli.agent_platform.provider_runtime.contracts import (
        ProviderRuntimeResolutionRequest,
    )
    from hermes_cli.agent_platform.provider_worker.resolution import (
        resolve_provider_worker_profile,
    )

    observed = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    store_root = default_openai_codex_credential_store_root()
    status = read_openai_codex_credential_status(
        store_root,
        protection_backend=protection_backend,
        now=observed,
    )
    if not status.configured:
        raise PepperLeadAgentProviderUnavailable("governed_credential_absent")
    lease = ProviderCredentialDeliveryLease(
        lease_id="lease.pepper-lead-agent-readiness",
        runtime_id=_PEPPER_RUNTIME_ID,
        correlation_id=_PEPPER_CORRELATION_ID,
        created_at_utc=observed,
        expires_at_utc=observed
        + timedelta(milliseconds=MAX_PROVIDER_CREDENTIAL_LEASE_TTL_MS),
    )
    provider_request = ProviderRuntimeResolutionRequest(
        profile_id=OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
        runtime_id=_PEPPER_RUNTIME_ID,
        correlation_id=_PEPPER_CORRELATION_ID,
        requested_by="pepper-lead-agent",
        evaluated_at_utc=observed,
        credential_status=status,
        credential_lease_ref=lease,
    )
    resolve_provider_worker_profile(
        ProviderWorkerResolutionRequest(
            worker_profile_id=OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
            provider_resolution_request=provider_request,
            evaluated_at_utc=observed,
        )
    )
    return load_openai_codex_oauth_credential(
        store_root,
        protection_backend=protection_backend,
        now=observed,
    )


def pepper_lead_agent_runtime_status() -> dict[str, Any]:
    """Credential-free readiness projection for setup.runtime_check."""

    try:
        runtime = resolve_pepper_lead_agent_runtime()
    except Exception as exc:
        return {
            "ok": False,
            "provider": PEPPER_LEAD_AGENT_PROVIDER,
            "model": PEPPER_LEAD_AGENT_MODEL,
            "source": PEPPER_LEAD_AGENT_SOURCE,
            "credential_profile_id": PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE,
            "error": str(exc),
            "provider_runtime_profile_id": OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID,
            "worker_profile_id": OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID,
        }
    return {
        "ok": True,
        "provider": runtime["provider"],
        "model": runtime["model"],
        "source": runtime["source"],
        "credential_profile_id": runtime["credential_profile_id"],
        "provider_runtime_profile_id": runtime["provider_runtime_profile_id"],
        "worker_profile_id": runtime["worker_profile_id"],
    }


__all__ = [
    "PEPPER_LEAD_AGENT_API_MODE",
    "PEPPER_LEAD_AGENT_CREDENTIAL_PROFILE",
    "PEPPER_LEAD_AGENT_ENV",
    "PEPPER_LEAD_AGENT_MODE",
    "PEPPER_LEAD_AGENT_MODEL",
    "PEPPER_LEAD_AGENT_PLATFORM",
    "PEPPER_LEAD_AGENT_PROVISION_COMMAND",
    "PEPPER_LEAD_AGENT_PROVIDER",
    "PEPPER_LEAD_AGENT_SOURCE",
    "PEPPER_LEAD_AGENT_TOOLSETS",
    "PepperLeadAgentProviderUnavailable",
    "pepper_lead_agent_branding",
    "pepper_lead_agent_enabled",
    "pepper_lead_agent_env",
    "pepper_lead_agent_runtime_status",
    "pepper_lead_agent_setup_sections",
    "pepper_lead_agent_system_prompt",
    "resolve_pepper_lead_agent_runtime",
]
