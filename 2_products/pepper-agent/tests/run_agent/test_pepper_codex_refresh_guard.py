from __future__ import annotations


def _agent_for_refresh(*, platform: str):
    from run_agent import AIAgent

    agent = AIAgent.__new__(AIAgent)
    agent.api_mode = "codex_responses"
    agent.provider = "openai-codex"
    agent.platform = platform
    agent.api_key = "active-token"
    agent.base_url = "https://chatgpt.com/backend-api/codex"
    agent._client_kwargs = {"api_key": agent.api_key, "base_url": agent.base_url}
    agent._replace_primary_openai_client = lambda reason: True
    return agent


def test_pepper_codex_refresh_does_not_call_legacy_resolver(monkeypatch):
    from run_agent import AIAgent

    def fail_legacy_resolver(**_kwargs):
        raise AssertionError("legacy Codex resolver must not be used in Pepper mode")

    monkeypatch.setattr(
        "hermes_cli.auth.resolve_codex_runtime_credentials",
        fail_legacy_resolver,
    )

    assert (
        AIAgent._try_refresh_codex_client_credentials(
            _agent_for_refresh(platform="pepper-dashboard"),
            force=True,
        )
        is False
    )


def test_generic_codex_refresh_keeps_existing_legacy_resolver(monkeypatch):
    from run_agent import AIAgent

    calls: list[dict] = []

    def fake_legacy_resolver(**kwargs):
        calls.append(kwargs)
        return {
            "api_key": "active-token",
            "base_url": "https://chatgpt.com/backend-api/codex",
        }

    monkeypatch.setattr(
        "hermes_cli.auth.resolve_codex_runtime_credentials",
        fake_legacy_resolver,
    )

    assert (
        AIAgent._try_refresh_codex_client_credentials(
            _agent_for_refresh(platform="tui"),
            force=True,
        )
        is True
    )
    assert calls == [
        {"refresh_if_expiring": False},
        {"force_refresh": True},
    ]
