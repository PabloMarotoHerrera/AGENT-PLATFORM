"""``hermes agent-platform`` subcommand parser."""

from __future__ import annotations

from typing import Callable

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
)


def build_agent_platform_parser(subparsers, *, cmd_agent_platform: Callable) -> None:
    """Attach Pepper agent-platform governance commands to ``subparsers``."""

    parser = subparsers.add_parser(
        "agent-platform",
        help="Manage Pepper agent-platform governance",
    )
    agent_platform_subparsers = parser.add_subparsers(dest="agent_platform_action")

    auth_parser = agent_platform_subparsers.add_parser(
        "auth",
        help="Manage governed agent-platform credentials",
    )
    auth_subparsers = auth_parser.add_subparsers(dest="agent_platform_auth_action")

    auth_add = auth_subparsers.add_parser(
        "add",
        help="Provision a governed provider credential",
    )
    auth_add.add_argument(
        "profile",
        choices=[OPENAI_CODEX_CREDENTIAL_STORE_ID],
        help="Governed credential profile id",
    )
    auth_add.set_defaults(func=cmd_agent_platform)

    auth_status = auth_subparsers.add_parser(
        "status",
        help="Show governed credential status",
    )
    auth_status.add_argument(
        "profile",
        choices=[OPENAI_CODEX_CREDENTIAL_STORE_ID],
        help="Governed credential profile id",
    )
    auth_status.set_defaults(func=cmd_agent_platform)

    auth_parser.set_defaults(func=cmd_agent_platform)
    parser.set_defaults(func=cmd_agent_platform)


__all__ = ["build_agent_platform_parser"]
