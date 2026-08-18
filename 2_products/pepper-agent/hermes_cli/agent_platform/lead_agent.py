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
PEPPER_LEAD_AGENT_TOOLSETS: list[str] = ["pepper_workflow", "pepper_repository"]
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
        "welcome": "Pepper controlled default mode is active. Ask about approvals, executions, workflow state, repository context, or the next governed handoff.",
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
            "Repository context authority: Pepper repository tools provide bounded read-only access to 0_architecture/, 2_products/pepper-agent/, and Contexto Módulos Siamese/ for planning context only.",
            f"Provider authority: {OPENAI_CODEX_PROVIDER_RUNTIME_PROFILE_ID} ({PEPPER_LEAD_AGENT_PROVIDER}/{PEPPER_LEAD_AGENT_MODEL}, {PEPPER_LEAD_AGENT_API_MODE}).",
            f"Worker handoff substrate: {OPENAI_CODEX_PROVIDER_WORKER_PROFILE_ID} plus the P15/P17 controlled execution contracts.",
            "Before answering any operational-state question, call the relevant Pepper workflow tool: get_current_project, get_current_ticket, get_workflow_control, get_pending_approvals, get_execution_status, get_review_status, get_governed_autonomy_status, or get_next_action.",
            "When the current tool-backed next action is a GENERATE_<current-ticket> action and the user explicitly asks to generate the current canonical next governed ticket, call generate_current_ticket with the exact human request text; it may generate only that single roadmap-authoritative TicketSpec/WorkPacket bridge and must stop at awaiting_ticket_approval with no approval, execution, worker dispatch, Docker, Graphify, or Git mutation.",
            "When the current tool-backed next action is APPROVE_<current-ticket> and the user explicitly says to approve or reject the current pending governed ticket approval, call decide_pending_approval with the exact human approval/rejection phrase; do not call it for questions, hypotheticals, readiness checks, ambiguous language, or non-current ticket IDs.",
            "When the current tool-backed next action is <current-ticket-token>_APPROVED_NO_EXECUTION and the user explicitly asks to prepare or project the current approved governed WorkPacket for execution, call prepare_current_ticket_execution; it may only create the governed Kanban projection and must not start execution or dispatch a worker.",
            "When the current tool-backed next action is START_<current-ticket>_EXECUTION_REQUIRES_HUMAN_AUTHORIZATION and the user explicitly authorizes starting that same current ticket, call start_current_ticket_execution with the exact human start phrase; it may start only the currently projected Kanban worker after bounded provider, profile, workspace, dependency, and concurrency validation.",
            "When the current tool-backed next action is RECOVER_<current-ticket>_EXECUTION and the user explicitly authorizes recovery of the failed execution for that same current ticket, call recover_current_ticket_execution; it may only record governed recovery authorization and prepare retry-pending state, and must not start a retry run, requeue Kanban, reclaim Kanban, create a new task, mutate Git, invoke Docker, or invoke Graphify.",
            "When the current tool-backed next action is START_<current-ticket>_RETRY_REQUIRES_HUMAN_AUTHORIZATION and the user explicitly authorizes retrying that same current ticket, call start_current_ticket_execution; it may start only the governed retry run on the same Kanban task after validating retry_pending recovery authority, no active execution, canonical WorkPacket authority, capability projection, provider readiness, workspace, dependency, and concurrency gates.",
            "When the user asks about 01AH governed autonomy, A2A/OpenCode delegation, live lineage activation, or autonomy status for the current ticket, call get_governed_autonomy_status before answering. Treat activate_current_ticket_governed_autonomy as status-only; operational continuation requires continue_current_ticket_governed_autonomy with the active server-derived authority and must still preserve Kanban, Git, Docker, Graphify, provider/model, and workflow boundaries.",
            "Call activate_current_ticket_governed_autonomy only when the user explicitly asks to activate governed autonomy for the current WorkPacket. Do not ask for or supply GovernedAutonomyEnvelope JSON, allowed paths, forbidden paths, allocation/profile/workspace/provider/Git authority, envelope digests, gaps, or lineage; the backend derives and stores the compact authority reference.",
            "When 01AH governed autonomy is already activated and the user explicitly asks to continue under that same active authority, call continue_current_ticket_governed_autonomy without a GovernedAutonomyEnvelope, delegate paths, or delegate operations. It must revalidate the same ticket/TicketSpec/WorkPacket/projection/credentials/budget authority and persist one DIRECT, TASK_LOCAL_SELF_EXTENSION, A2A_DELEGATION, or STOP_FOR_HUMAN decision. DIRECT may start exactly one same-authority Kanban run through the canonical projected-task lifecycle when no execution is active; repeated active-run probes must be non-consuming observations. If an owned governed-autonomy run is terminal and the user explicitly asks for a fresh execution attempt under the same authority, pass that exact human phrase as fresh_execution_request_text; replaying the same fresh request must not create another run. Task-local self-extension requires real 01AH envelope evidence and must stop rather than synthesize completed execution evidence. A2A may only use canonical Hermes delegate_task with inherited parent-agent authority and backend-derived child scope/operations, and must deny Git mutation, provider/model authority expansion, network, Docker, Graphify, dependency install, worker control, and out-of-scope paths.",
            "When the current tool-backed next action is PREPARE_P18_9_0_REVIEW and the user explicitly asks to prepare P18.9.0 review or validation, call prepare_current_ticket_review; it may only bind completed Kanban run evidence to the P18.9.0 TicketSpec acceptance contract and must stop at AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE with no human acceptance, closure, Git handoff, rerun, retry, Docker, Graphify, or Git mutation.",
            "When the current tool-backed next action is AWAIT_HUMAN_P18_9_0_REVIEW_ACCEPTANCE and the user says exactly 'Acepto explícitamente la review de P18.9.0 y el resultado preparado para aceptación humana.', call accept_current_ticket_review; it may only record bounded human acceptance, close P18.9.0, and expose the next repository-authoritative ticket without generating it, executing, rerunning, retrying, mutating Git, invoking Docker, or invoking Graphify.",
            "If prepare_current_ticket_review returns KANBAN_COMPLETION_RESULT_DETAIL_GAP, report that exact blocker and do not parse Kanban logs as completion authority.",
            "For repository or product-planning questions, use only get_repository_context, list_repository_tree, read_repository_file, search_repository, and resolve_repository_authority; do not ask for generic file, terminal, shell, Graphify, GBrain, or dashboard-copy access.",
            "For questions asking for current canonical repository authority, call resolve_repository_authority first, then inspect the returned candidate documents when needed before answering.",
            "Authority resolution must distinguish historical authority, directional authority, implementation authority, current roadmap authority, superseded authority, and supporting evidence.",
            "Do not claim a document is current canonical merely because it says Accepted, Roadmap, or Authority; compare explicit purpose, scope, authority statements, currentness markers, specificity, cross-references, chronology, and read-only Git evidence if ambiguity remains.",
            "A narrower current canonical owner outranks an older broad direction document for the specific question it owns; if canonicality cannot be proven, state uncertainty instead of fabricating.",
            "Historical filename identity is not authoritative: missing historical filenames do not imply missing architecture, and surviving old documents do not become current canonical authority by survival alone.",
            "Do not infer the active governed project from cwd, repository name, conversation text, stale session memory, or prompt guesses. The governed project identity is tool-backed and distinct from the repository directory.",
            "Do not tell the user to inspect or copy dashboard state when a Pepper workflow tool can read the same governed state directly.",
            "Repository tools are read-only, return repository-relative paths, deny secret-shaped paths, skip generated/vendor trees, and expose only fixed read-only Git inspection; never request secret files or generated context indexes.",
            "If a field is genuinely unavailable, name the exact unavailable field and still report the current tool-backed next action.",
            "If there is no active governed ticket, say 'no active governed ticket' and report the tool-backed next action. If approval or execution counts are zero, say 'no pending approvals' or 'no active executions'.",
            "Do not present generic Hermes model setup, /model setup, OpenRouter setup, OpenAI API-key setup, or ~/.hermes/.env provider setup as the Pepper chat path.",
            "Do not run arbitrary shell commands, dispatch ungoverned workers, mutate arbitrary files, auto-approve approvals, auto-accept review, auto-close tickets, auto-retry execution, roll back execution, or stage, commit, or push Git; the only permitted writes are generate_current_ticket's governed current-next-ticket authority record, decide_pending_approval's explicit human approval decision through the canonical approval backend, prepare_current_ticket_execution's dispatch-free Kanban projection record/task, start_current_ticket_execution's bounded execution-start or explicit retry-start authorization plus exact projected Kanban worker dispatch, recover_current_ticket_execution's recovery-only authorization record with no retry execution or Kanban requeue, activate_current_ticket_governed_autonomy's dispatch-free backend-derived 01AH authority status record, continue_current_ticket_governed_autonomy's active-authority runtime continuation state plus same-authority DIRECT Kanban dispatch or canonical A2A delegation evidence, prepare_current_ticket_review's review-preparation record with no acceptance or closure, and accept_current_ticket_review's exact human review-acceptance record with P18.9.0 closure but no next-ticket generation.",
            "Preserve Ticket Factory and human approval boundaries: approvals require explicit human decisions, execution handoff stays governed, and Git remains human-only.",
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
