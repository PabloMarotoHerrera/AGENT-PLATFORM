"""CLI commands for Pepper agent-platform credential/profile authority."""

from __future__ import annotations

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_HERMES_PROVIDER_ID,
)
from hermes_cli.agent_platform.provider_credentials.provisioning import (
    OPENAI_CODEX_PRIMARY_PROVISION_COMMAND,
    assert_openai_codex_primary_profile,
    provision_openai_codex_primary,
    read_openai_codex_primary_status,
)
from hermes_cli.agent_platform.execution_profile_provisioning import (
    PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME,
    assert_pepper_implementation_profile,
    inspect_pepper_implementation_profile_provisioning,
    provision_pepper_implementation_profile,
)
from hermes_constants import display_hermes_home


def agent_platform_command(args) -> int:
    """Dispatch the top-level ``hermes agent-platform`` namespace."""

    action = getattr(args, "agent_platform_action", "")
    if action == "auth":
        return _agent_platform_auth_command(args)
    if action == "profile":
        return _agent_platform_profile_command(args)
    print("usage: hermes agent-platform {auth,profile} ...")
    return 1


def _agent_platform_auth_command(args) -> int:
    action = getattr(args, "agent_platform_auth_action", "")
    if action == "add":
        return _agent_platform_auth_add_command(args)
    if action == "status":
        return _agent_platform_auth_status_command(args)
    print("usage: hermes agent-platform auth add openai-codex.primary")
    return 1


def _agent_platform_profile_command(args) -> int:
    action = getattr(args, "agent_platform_profile_action", "")
    if action == "status":
        return _agent_platform_profile_status_command(args)
    if action == "provision":
        return _agent_platform_profile_provision_command(args)
    print(
        "usage: hermes agent-platform profile {status,provision} "
        f"{PEPPER_IMPLEMENTATION_PRODUCT_PROFILE_NAME}"
    )
    return 1


def _agent_platform_auth_add_command(args) -> int:
    profile_id = assert_openai_codex_primary_profile(getattr(args, "profile", ""))
    print("Provisioning Pepper governed OpenAI Codex OAuth credential.")
    print(f"  Credential profile: {profile_id}")
    print(f"  Provider: {OPENAI_CODEX_HERMES_PROVIDER_ID}")
    print("  OAuth flow: ChatGPT device-code login")
    print()
    status = provision_openai_codex_primary()
    print()
    print("Governed Codex OAuth credential saved.")
    print(f"  Credential profile: {status.credential_ref.store_id}")
    print(
        "  Store: "
        f"{display_hermes_home()}/agent-platform/provider-credentials/"
        f"{OPENAI_CODEX_CREDENTIAL_STORE_ID}/auth.json"
    )
    return 0


def _agent_platform_auth_status_command(args) -> int:
    profile_id = assert_openai_codex_primary_profile(getattr(args, "profile", ""))
    status = read_openai_codex_primary_status()
    print(f"Credential profile: {profile_id}")
    print(f"Provider: {OPENAI_CODEX_HERMES_PROVIDER_ID}")
    print(f"Configured: {'yes' if status.configured else 'no'}")
    print(f"Durable store valid: {'yes' if status.durable_store_valid else 'no'}")
    print(f"Token pair present: {'yes' if status.token_pair_present else 'no'}")
    if status.expires_at_utc is not None:
        print(f"Expires at UTC: {status.expires_at_utc.isoformat()}")
    return 0


def _print_profile_inspection(inspection: dict) -> None:
    contract = inspection["contract"]
    print(f"Execution profile: {inspection['canonical_profile']}")
    print(f"Status: {inspection['status']}")
    print(f"Profile exists: {'yes' if inspection['canonical_profile_exists'] else 'no'}")
    print(f"Candidate count: {inspection['candidate_count']}")
    if inspection["candidate_profiles"]:
        print("Candidate profiles: " + ", ".join(inspection["candidate_profiles"]))
    print("Stored toolsets: " + ", ".join(contract["stored_toolsets"]))
    print("Stored sentinels: " + ", ".join(contract["stored_sentinels"]))
    print("Effective worker toolsets: " + ", ".join(contract["effective_worker_toolsets"]))
    print(f"Provider: {contract['provider']}")
    print(f"Model: {contract['model']}")
    print(f"API mode: {contract['api_mode']}")
    print(f"Credential profile: {contract['credential_profile_id']}")
    print(f"Provider runtime profile: {contract['provider_runtime_profile_id']}")
    print(f"Worker profile: {contract['worker_profile_id']}")


def _agent_platform_profile_status_command(args) -> int:
    assert_pepper_implementation_profile(getattr(args, "profile", ""))
    _print_profile_inspection(inspect_pepper_implementation_profile_provisioning())
    return 0


def _agent_platform_profile_provision_command(args) -> int:
    profile_id = assert_pepper_implementation_profile(getattr(args, "profile", ""))
    print("Provisioning Pepper governed implementation execution profile.")
    print(f"  Execution profile: {profile_id}")
    result = provision_pepper_implementation_profile()
    print(f"  Provisioning status: {result['provisioning_status']}")
    print(f"  Profile path: {result['canonical_profile_path']}")
    return 0


__all__ = [
    "OPENAI_CODEX_PRIMARY_PROVISION_COMMAND",
    "agent_platform_command",
]
